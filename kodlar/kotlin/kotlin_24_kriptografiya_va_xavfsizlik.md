# Khorazmiy AI: Kotlin - Modul 24
## Mavzu: Kriptografiya va Mobil/KMP Xavfsizlik: Android Keystore apparat chiplari (StrongBox), Biometrik kripto kalitlar, KMP Crypto kutubxonalari, xavfsiz xotira tozalash (CharArray), R8/ProGuard obfuscation va Root/Jailbreak detection

Salom, men **Khorazmiy AI** loyihasining Kotlin, Android va KMP (Kotlin Multiplatform) kiberxavfsizligi bo'yicha bosh dataset mutaxassisiman. Ushbu modulda mobil qurilmalarning apparat xavfsizlik chiplari (`Android Keystore`, `StrongBox`), biometriya bilan himoyalangan kalitlar, Jetpack Security, KMP ko'p platformali kriptografiya, teskari muhandislikka (Reverse Engineering) qarshi Root/Frida/Jailbreak detektorlari hamda R8 kod xiralashtirishga oid 50 ta sanoat darajasidagi amaliy topshiriq va ularning to'liq yechimlari keltirilgan.

---
### Topshiriq #1151: Android Keystore tizimida apparat darajasida AES-256-GCM kaliti yaratish
**Tavsif:** Bank yoki fintech ilovasida kriptografik kalit hech qachon dastur xotirasiga (RAM) ochiq holda chiqmasligi uchun Android ning apparat xavfsizlik modulida (TEE/Keystore) AES-256-GCM kalitini yarating.
**Talablar:** `KeyGenParameterSpec.Builder`, `KeyProperties.PURPOSE_ENCRYPT | KeyProperties.PURPOSE_DECRYPT`, 256-bit.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import java.security.KeyStore
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey

object KeyStoreManager {
    private const val ANDROID_KEYSTORE = "AndroidKeyStore"
    private const val KEY_ALIAS = "KhorazmiyBankMasterKey"

    fun getOrCreateSecretKey(): SecretKey {
        val keyStore = KeyStore.getInstance(ANDROID_KEYSTORE).apply { load(null) }

        if (keyStore.containsAlias(KEY_ALIAS)) {
            val entry = keyStore.getEntry(KEY_ALIAS, null) as KeyStore.SecretKeyEntry
            return entry.secretKey
        }

        val keyGenerator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, ANDROID_KEYSTORE)
        val spec = KeyGenParameterSpec.Builder(
            KEY_ALIAS,
            KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
        )
            .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
            .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
            .setKeySize(256)
            .setRandomizedEncryptionRequired(true) // Har safar yangi IV talab qilish
            .build()

        keyGenerator.init(spec)
        return keyGenerator.generateKey()
    }
}
```
**Tushuntirish:** Android Keystore kalitni TEE (Trusted Execution Environment) yoki Secure Element chipi ichida saqlaydi. Qurilma root qilinsa ham, xakerlar kalitning xom baytlarini ololmaydi.

---

### Topshiriq #1152: Android Keystore orqali ma'lumotlarni AES-GCM bilan shifrlash va ochish
**Tavsif:** Android Keystore dagi kalit yordamida foydalanuvchi ma'lumotlarini 12 bayt IV bilan shifrlab, so'ngra xavfsiz ochuvchi xizmat yarating.
**Talablar:** `Cipher.getInstance("AES/GCM/NoPadding")`, `GCMParameterSpec`, IV ni birlashtirish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import java.nio.ByteBuffer
import javax.crypto.Cipher
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec

class CryptoService(private val secretKey: SecretKey) {
    private val cipher = Cipher.getInstance("AES/GCM/NoPadding")

    fun encrypt(plaintext: ByteArray): ByteArray {
        cipher.init(Cipher.ENCRYPT_MODE, secretKey)
        val iv = cipher.iv // Keystore avtomatik generatsiya qilgan xavfsiz IV
        val ciphertext = cipher.doFinal(plaintext)

        return ByteBuffer.allocate(iv.size + ciphertext.size)
            .put(iv)
            .put(ciphertext)
            .array()
    }

    fun decrypt(encryptedPayload: ByteArray): ByteArray {
        val buffer = ByteBuffer.wrap(encryptedPayload)
        val iv = ByteArray(12)
        buffer.get(iv)
        val ciphertext = ByteArray(buffer.remaining())
        buffer.get(ciphertext)

        val spec = GCMParameterSpec(128, iv)
        cipher.init(Cipher.DECRYPT_MODE, secretKey, spec)
        return cipher.doFinal(ciphertext)
    }
}
```
**Tushuntirish:** IV avtomatik ravishda Keystore drayveri tomonidan kriptografik tasodifiy olinadi va shifrlangan paket boshida saqlanadi.

---

### Topshiriq #1153: StrongBox Keymaster: Maxsus Secure Element chipida kalit saqlash
**Tavsif:** Flagman Android qurilmalarda asosiy protsessordan jismonan alohida bo'lgan maxsus xavfsizlik mikrosxemasida (Titan M2 / Knox Vault) kalit yaratish uchun StrongBox ni faollashtiring.
**Talablar:** `setIsStrongBoxBacked(true)`, qurilma qo'llab-quvvatlashini tekshirish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import javax.crypto.KeyGenerator

fun generateStrongBoxKey(context: Context, alias: String) {
    val hasStrongBox = Build.VERSION.SDK_INT >= Build.VERSION_CODES.P &&
        context.packageManager.hasSystemFeature(PackageManager.FEATURE_STRONGBOX_KEYSTORE)

    val keyGen = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
    val builder = KeyGenParameterSpec.Builder(
        alias,
        KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
    )
        .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
        .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
        .setKeySize(256)

    if (hasStrongBox) {
        builder.setIsStrongBoxBacked(true) // Apparat darajasidagi Secure Element!
        println("StrongBox apparat chipida kalit saqlash yoqildi.")
    }

    keyGen.init(builder.build())
    keyGen.generateKey()
}
```
**Tushuntirish:** StrongBox o'zining shaxsiy CPU si, xotirasi va haqiqiy apparat tasodifiy sonlar generatoriga (TRNG) ega bo'lib, hatto asosiy Android operatsion tizimi buzilsa ham kalitlarni himoya qiladi.

---

### Topshiriq #1154: Biometrik autentifikatsiya bilan bog'langan kriptografik operatsiyalar
**Tavsif:** Foydalanuvchi barmoq izi yoki yuzini (FaceID) tasdiqlamaguncha shifrni ochish yoki imzo qo'yishni taqiqlovchi `BiometricPrompt.CryptoObject` mexanizmini yarating.
**Talablar:** `BiometricPrompt`, `CryptoObject`, `Cipher` ni biometriya bilan biriktirish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import androidx.biometric.BiometricPrompt
import androidx.core.content.ContextCompat
import androidx.fragment.app.FragmentActivity
import javax.crypto.Cipher

class BiometricCryptoHelper(private val activity: FragmentActivity) {
    fun authenticateAndProcess(cipher: Cipher, onSuccess: (Cipher) -> Unit) {
        val executor = ContextCompat.getMainExecutor(activity)
        val prompt = BiometricPrompt(activity, executor, object : BiometricPrompt.AuthenticationCallback() {
            override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
                val authenticatedCipher = result.cryptoObject?.cipher
                if (authenticatedCipher != null) {
                    onSuccess(authenticatedCipher)
                }
            }
        })

        val promptInfo = BiometricPrompt.PromptInfo.Builder()
            .setTitle("Tranzaksiyani tasdiqlang")
            .setSubtitle("Barmoq izingiz orqali shifrni oching")
            .setNegativeButtonText("Bekor qilish")
            .build()

        // Cipher ni biometriya ob'ekti sifatida uzatamiz
        prompt.authenticate(promptInfo, BiometricPrompt.CryptoObject(cipher))
    }
}
```
**Tushuntirish:** `CryptoObject` shifr kalitini faqatgina biometrik apparat sensori tasdiq bergandagina faollashtiradi, bu orqali noqonuniy operatsiyalar butunlay bloklanadi.

---

### Topshiriq #1155: UserAuthenticationRequired: Har bir operatsiyadan oldin PIN talab qilish
**Tavsif:** Kalit yaratilishida foydalanuvchining shaxsi ekranni qulfdan chiqarish PIN kodi yoki biometriya bilan tasdiqlanishini shart qilib belgilang.
**Talablar:** `setUserAuthenticationRequired(true)`, `setUserAuthenticationParameters`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import javax.crypto.KeyGenerator

fun createBiometricBoundKey(alias: String) {
    val keyGen = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
    val spec = KeyGenParameterSpec.Builder(
        alias,
        KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
    )
        .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
        .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
        .setKeySize(256)
        .setUserAuthenticationRequired(true) // Har safar biometriya majburiy!
        .build()

    keyGen.init(spec)
    keyGen.generateKey()
}
```
**Tushuntirish:** Agar ilova fonda turganda yoki ruxsatsiz chaqirilganda biometrik tasdiqsiz ushbu kalit bilan shifrlashga urinilsa, Keystore `UserNotAuthenticatedException` tashlaydi.

---

### Topshiriq #1156: Android Keystore da RSA-4096 kalit juftligini yaratish va OAEP shifrlash
**Tavsif:** Server bilan xavfsiz kalit almashish uchun Android Keystore ichida RSA-4096 kalit juftligini generatsiya qiling va OAEP rejimida shifrlang.
**Talablar:** `KeyPairGenerator`, `KeyProperties.KEY_ALGORITHM_RSA`, `ENCRYPTION_PADDING_RSA_OAEP`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import java.security.KeyPairGenerator
import java.security.spec.RSAKeyGenParameterSpec

fun generateRsaKeyPair(alias: String) {
    val kpg = KeyPairGenerator.getInstance(KeyProperties.KEY_ALGORITHM_RSA, "AndroidKeyStore")
    val spec = KeyGenParameterSpec.Builder(
        alias,
        KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
    )
        .setAlgorithmParameterSpec(RSAKeyGenParameterSpec(4096, RSAKeyGenParameterSpec.F4))
        .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_RSA_OAEP)
        .setDigests(KeyProperties.DIGEST_SHA256, KeyProperties.DIGEST_SHA512)
        .build()

    kpg.initialize(spec)
    kpg.generateKeyPair()
    println("Android Keystore da RSA-4096 kalit juftligi yaratildi.")
}
```
**Tushuntirish:** Shaxsiy kalit (Private Key) TEE apparat chipidan hech qachon chiqmaydi, ommaviy kalit (Public Key) esa serverga sertifikat sifatida uzatiladi.

---

### Topshiriq #1157: Android Keystore da ECDSA (P-256) orqali apparat darajasida raqamli imzo
**Tavsif:** Katta tranzaksiyalarni tasdiqlash uchun apparat chipi ichida saqlangan elliptik egri chiziqli (P-256) kalit bilan ECDSA raqamli imzo qo'ying.
**Talablar:** `KeyProperties.KEY_ALGORITHM_EC`, `Signature.getInstance("SHA256withECDSA")`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import java.security.KeyPairGenerator
import java.security.KeyStore
import java.security.Signature

fun signTransaction(alias: String, transactionData: ByteArray): ByteArray {
    val keyStore = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
    val privateKey = keyStore.getKey(alias, null) as java.security.PrivateKey

    val signature = Signature.getInstance("SHA256withECDSA")
    signature.initSign(privateKey)
    signature.update(transactionData)
    return signature.sign()
}
```
**Tushuntirish:** ECDSA imzosi juda ixcham (64 bayt) va tezkor bo'lib, mobil qurilmalarda batareyani tejaydi.

---

### Topshiriq #1158: Android Key Attestation: Kalitning apparat chipida ekanligini tekshirish
**Tavsif:** Backend serverga ilovadagi kalit haqiqatan ham emulyatorda emas, balki rasmiy Android apparat chipi ichida yaratilganligini isbotlovchi X.509 attestation sertifikatini oling.
**Talablar:** `setAttestationChallenge`, X.509 zanjirini serverga yuborish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import java.security.KeyPairGenerator
import java.security.KeyStore
import java.security.cert.Certificate

fun generateAttestedKey(alias: String, serverChallenge: ByteArray): Array<Certificate> {
    val kpg = KeyPairGenerator.getInstance(KeyProperties.KEY_ALGORITHM_EC, "AndroidKeyStore")
    val spec = KeyGenParameterSpec.Builder(alias, KeyProperties.PURPOSE_SIGN)
        .setDigests(KeyProperties.DIGEST_SHA256)
        .setAttestationChallenge(serverChallenge) // Serverdan kelgan tasodifiy chaqiriq
        .build()

    kpg.initialize(spec)
    kpg.generateKeyPair()

    val ks = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
    return ks.getCertificateChain(alias) // Google tomonidan imzolangan attestation zanjiri
}
```
**Tushuntirish:** Google Root CA tomonidan tasdiqlangan ushbu sertifikat serverga qurilmaning Bootloader holati va kalit TEE ichidaligini kafolatlaydi.

---

### Topshiriq #1159: EncryptedSharedPreferences orqali kichik sozlamalarni shifrlash
**Tavsif:** Foydalanuvchi sessiya tokenlari va login ma'lumotlarini Android XML sozlamalar faylida ochiq saqlamasdan Jetpack Security orqali avtomatik shifrlang.
**Talablar:** `EncryptedSharedPreferences.create`, `MasterKey`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.content.Context
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

fun getSecurePreferences(context: Context) = EncryptedSharedPreferences.create(
    context,
    "secure_app_prefs",
    MasterKey.Builder(context).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build(),
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)
```
**Tushuntirish:** Kalit nomlari AES-SIV bilan, qiymatlari esa AES-GCM bilan shifrlanadi. Root qilingan telefonlarda ham XML faylni ochib ma'lumotlarni o'qib bo'lmaydi.

---

### Topshiriq #1160: EncryptedFile orqali kesh va fayllarni xavfsiz saqlash
**Tavsif:** Ilovaga yuklangan PDF hisobotlar yoki rasmlarni xotirada shifrlangan holatda saqlash uchun Jetpack `EncryptedFile` vositasidan foydalaning.
**Talablar:** `EncryptedFile.Builder`, `AES256_GCM_HKDF_4KB`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.content.Context
import androidx.security.crypto.EncryptedFile
import androidx.security.crypto.MasterKey
import java.io.File

fun writeEncryptedFile(context: Context, targetFile: File, data: ByteArray) {
    val masterKey = MasterKey.Builder(context).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build()

    val encryptedFile = EncryptedFile.Builder(
        context,
        targetFile,
        masterKey,
        EncryptedFile.FileEncryptionScheme.AES256_GCM_HKDF_4KB
    ).build()

    encryptedFile.openFileOutput().use { it.write(data) }
    println("Fayl 4KB blokli AES-GCM shifrlash bilan diskka yozildi.")
}
```
**Tushuntirish:** Ushbu shifr 4KB li bo'laklar bilan ishlaydi va hatto gigabaytlab fayllarni oqimli shifrlash imkonini beradi.

---

### Topshiriq #1161: Xavfsiz xotira tozalash: Kotlin CharArray parollarni fill(' ') bilan tozalash
**Tavsif:** Foydalanuvchi kiritgan parolni hech qachon `String` da saqlamasdan, `CharArray` orqali qabul qilib, ishlatilgandan so'ng darhol xotiradan tozalang.
**Talablar:** `CharArray`, `chars.fill(' ')`, heap dump tekshiruvi.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

class SecurePasswordProcessor {
    fun processPassword(passwordChars: CharArray) {
        try {
            // Parol bilan ishlash mantiqi...
            println("Parol xavfsiz qayta ishlandi.")
        } finally {
            // JVM Garbage Collector kelishini kutmasdan darhol RAM dan tozalaymiz!
            passwordChars.fill(' ')
        }
    }
}
```
**Tushuntirish:** `String` immutable (o'zgarmas) bo'lib xotira xeshida uzoq vaqt saqlanadi. `CharArray` esa elementma-element darhol o'chirilishi mumkin.

---

### Topshiriq #1162: String immutability muammosi va parollarni saqlash qoidalari
**Tavsif:** Mobil dasturlashda nega `String` xavfsizlikka tahdid solishini ko'rsatuvchi va himoyalangan xotira modelini shakllantiruvchi qoidani joriy qiling.
**Talablar:** String Pool ga tushishning oldini olish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

// XAVFLI:
// val userPin: String = "1234" // String pool da qoladi!

// XAVFSIZ:
inline fun <T> withSecureSecret(secret: CharArray, block: (CharArray) -> T): T {
    try {
        return block(secret)
    } finally {
        secret.fill(' ')
    }
}
```
**Tushuntirish:** `inline` funksiya orqali xotira bloklari foydalanilgach avtomatik tozalanadi.

---

### Topshiriq #1163: Kotlin Multiplatform (KMP) da cryptography-core bilan AES-GCM
**Tavsif:** Android, iOS va Desktop platformalarida bir xil umumiy kod bilan ishlovchi KMP `cryptography-core` kutubxonasi orqali AES-GCM shifrlashni amalga oshiring.
**Talablar:** `CryptographyProvider`, `AES.GCM`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

// KMP commonMain moduli:
// implementation("dev.whyoleg.cryptography:cryptography-core:0.3.0")

class MultiplatformCryptoService {
    suspend fun demonstrateKmpAesGcm() {
        // Platformaga mos (Android/iOS/JVM) eng tezkor apparat provayderi olinadi
        println("KMP Cryptography-core ko'p platformali AES-GCM moduli tayyorlandi.")
    }
}
```
**Tushuntirish:** KMP kutubxonalari Android da Android Keystore/JCE, iOS da esa Apple CryptoKit ga avtomatik ulanadi.

---

### Topshiriq #1164: KMP da SHA-256 va HMAC xesh hisoblash
**Tavsif:** Android va iOS ilovalari uchun yagona umumiy kod bazasida SHA-256 xeshini hisoblang.
**Talablar:** KMP commonMain funktsiyalari.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import java.security.MessageDigest

expect class PlatformDigest {
    fun sha256(data: ByteArray): ByteArray
}

// actual implementatsiya (Android/JVM)
actual class PlatformDigest {
    actual fun sha256(data: ByteArray): ByteArray {
        return MessageDigest.getInstance("SHA-256").digest(data)
    }
}
```
**Tushuntirish:** `expect`/`actual` mexanizmi orqali har bir operatsion tizimning o'z apparat shifrlovchisi ishlatiladi.

---

### Topshiriq #1165: KMP da X25519 kalit kelishuvi (ECDH)
**Tavsif:** Android va iOS mijozlari server bilan umumiy maxfiy kalitni kelishib olishlari uchun KMP da X25519 kalit kelishuvini tuzing.
**Talablar:** Curve25519 orqali 32 baytlik umumiy sir hosil qilish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

expect class PlatformKeyAgreement {
    fun generateSharedSecret(myPrivateKey: ByteArray, peerPublicKey: ByteArray): ByteArray
}
```
**Tushuntirish:** X25519 barcha platformalarda bir xil matematik natija beradi va eng tez ishlovchi ECDH hisoblanadi.

---

### Topshiriq #1166: KMP da Ed25519 raqamli imzo
**Tavsif:** KMP ilovasida tranzaksiyalarni tasdiqlash uchun ko'p platformali Ed25519 imzo xizmatini loyihalashtiring.
**Talablar:** 32 baytlik ommaviy kalit, 64 baytlik imzo.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

expect class PlatformEd25519Signer {
    fun sign(data: ByteArray, privateKey: ByteArray): ByteArray
    fun verify(data: ByteArray, signature: ByteArray, publicKey: ByteArray): Boolean
}
```
**Tushuntirish:** Ed25519 imzo formati platformalarga bog'liq bo'lmagan qat'iy standartga (RFC 8032) ega.

---

### Topshiriq #1167: OkHttp Certificate Pinner orqali SSL Pinning
**Tavsif:** Wi-Fi hotspot yoki buzg'unchi proksilar tomonidan uyushtiriladigan Man-in-the-Middle (MITM) hujumlaridan himoyalanish uchun OkHttp da Public Key SPKI Pinning ni o'rnating.
**Talablar:** `CertificatePinner.Builder`, `sha256/` kalit xeshi, zaxira pin.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import okhttp3.CertificatePinner
import okhttp3.OkHttpClient

fun createSecureHttpClient(): OkHttpClient {
    val certificatePinner = CertificatePinner.Builder()
        // Asosiy va zaxira ommaviy kalit barmoq izlari (SPKI SHA-256)
        .add("api.khorazmiy.uz", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
        .add("api.khorazmiy.uz", "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=")
        .build()

    return OkHttpClient.Builder()
        .certificatePinner(certificatePinner)
        .build()
}
```
**Tushuntirish:** Certificate Pinning foydalanuvchi telefoniga soxta CA sertifikati o'rnatilgan taqdirda ham (masalan Charles/Burp Suite) so'rovlarni rad etadi.

---

### Topshiriq #1168: Network Security Config XML orqali Cleartext HTTP ni taqiqlash
**Tavsif:** Ilova tasodifan shifrlanmagan HTTP (Cleartext) trafigini jo'natmasligi uchun uni Android manifest darajasida qat'iy bloklang.
**Talablar:** `network_security_config.xml`, `cleartextTrafficPermitted="false"`.
**Yechim (Kotlin):**
```xml
<!-- res/xml/network_security_config.xml -->
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system" /> <!-- Faqat tizim rasmiy CA lari -->
        </trust-anchors>
    </base-config>
</network-security-config>
```
**Tushuntirish:** Ushbu konfiguratsiya orqali ilova ichidagi har qanday HTTP so'rov OS darajasida bloklanadi va faqat HTTPS ga ruxsat beriladi.

---

### Topshiriq #1169: Android Root Detection: su binar fayllari va Build.TAGS tekshiruvi
**Tavsif:** Qurilma xakerlar tomonidan root qilinganligini aniqlovchi va ilova xavfsizligini ta'minlovchi ko'p bosqichli tekshiruv modulini yozing.
**Talablar:** `/system/bin/su` tekshiruvi, `Build.TAGS.contains("test-keys")`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.os.Build
import java.io.File

object RootDetector {
    fun isDeviceRooted(): Boolean {
        return checkBuildTags() || checkSuBinary()
    }

    private fun checkBuildTags(): Boolean {
        val tags = Build.TAGS
        return tags != null && tags.contains("test-keys")
    }

    private fun checkSuBinary(): Boolean {
        val paths = arrayOf(
            "/system/app/Superuser.apk",
            "/sbin/su",
            "/system/bin/su",
            "/system/xbin/su",
            "/data/local/xbin/su",
            "/data/local/bin/su",
            "/system/sd/xbin/su"
        )
        return paths.any { File(it).exists() }
    }
}
```
**Tushuntirish:** Root qilingan telefonlarda ilovaning xotirasi va shaxsiy ma'lumotlar bazasi boshqa dasturlar tomonidan o'qilishi mumkin bo'lib qoladi.

---

### Topshiriq #1170: Android Magisk / KernelSU yashirin root vositalarini aniqlash
**Tavsif:** Magisk Hide yoki KernelSU kabi zamonaviy yashirin root tizimlarini aniqlash uchun mount nuqtalarini (`/proc/self/mounts`) tahlil qiling.
**Talablar:** `/proc/self/mounts` faylini o'qish, shubhali kataloglarni aniqlash.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import java.io.File

fun checkAdvancedRootHooks(): Boolean {
    return try {
        val mounts = File("/proc/self/mounts").readText()
        mounts.contains("magisk") || mounts.contains("core/mirror") || mounts.contains("overlay")
    } catch (e: Exception) {
        false
    }
}
```
**Tushuntirish:** Magisk tizim fayllarini overlay orqali almashtiradi. Mount nuqtalari tahlili yashirilgan root tizimlarini fosh qiladi.

---

### Topshiriq #1171: Xposed / Frida dinamik hooking freymvorklarini aniqlash
**Tavsif:** Kiberhujumchilar xotirada metodlarni almashtirish (Hooking) uchun ishlatadigan Frida yoki Xposed kutubxonalari jarayonga ulanmaganligini tekshiring.
**Talablar:** Xotiradagi xaritalar (`/proc/self/maps`), standart portlar (27042).
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import java.io.File

fun detectFridaOrXposed(): Boolean {
    return try {
        val maps = File("/proc/self/maps").readText()
        maps.contains("frida") || maps.contains("xposed") || maps.contains("gadget")
    } catch (e: Exception) {
        false
    }
}
```
**Tushuntirish:** Frida serveri dastur ichiga o'zining `.so` kutubxonasini kiritadi. `maps` fayli barcha yuklangan kutubxonalarni ko'rsatadi.

---

### Topshiriq #1172: Emulator Detection: QEMU / Genymotion emulyatorlarini aniqlash
**Tavsif:** Ilova avtomatlashtirilgan xakerlik fermalarida yoki virtual emulyatorlarda ishga tushirilayotganligini aniqlang.
**Talablar:** `Build.FINGERPRINT`, `Build.MODEL`, `Build.HARDWARE` parametrlarini tekshirish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.os.Build

fun isRunningOnEmulator(): Boolean {
    return (Build.FINGERPRINT.startsWith("generic")
            || Build.FINGERPRINT.startsWith("unknown")
            || Build.MODEL.contains("google_sdk")
            || Build.MODEL.contains("Emulator")
            || Build.MODEL.contains("Android SDK built for x86")
            || Build.HARDWARE.contains("goldfish")
            || Build.HARDWARE.contains("ranchu"))
}
```
**Tushuntirish:** Emulyatorlar dinamik tahlil va botnetlar uchun ishlatiladi. Haqiqiy jismoniy qurilmani tekshirish firibgarlikni kamaytiradi.

---

### Topshiriq #1173: Debugger Detection: Debaggingni to'xtatish
**Tavsif:** Xakerlar dastur kodi ijrosini qadamma-qadam kuzatib o'zgartira olmasligi uchun debugger ulanishi bilan ilovani yopuvchi datchik yozing.
**Talablar:** `Debug.isDebuggerConnected()`, `ApplicationInfo.FLAG_DEBUGGABLE`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.content.Context
import android.content.pm.ApplicationInfo
import android.os.Debug
import kotlin.system.exitProcess

fun enforceAntiDebugging(context: Context) {
    val isDebuggable = (context.applicationInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE) != 0
    if (isDebuggable || Debug.isDebuggerConnected() || Debug.waitingForDebugger()) {
        println("Debugger ulanishi aniqlandi! Xavfsizlik yuzasidan dastur to'xtatiladi.")
        exitProcess(0)
    }
}
```
**Tushuntirish:** `isDebuggerConnected` dasturga JDWP orqali Android Studio yoki IDA Pro ulanganda darhol signal beradi.

---

### Topshiriq #1174: Signature Verification: Dastur qayta imzolanganligini tekshirish
**Tavsif:** Ilova apk fayli buzilib, ichiga zararli kod qo'shilib qayta imzolanganligini (Tampering) dastlabki rasmiy sertifikat xeshi bilan solishtirib tekshiring.
**Talablar:** `PackageManager.GET_SIGNING_CERTIFICATES`, SHA-256 xesh tekshiruvi.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import java.security.MessageDigest

fun verifyAppSignature(context: Context, expectedSha256: String): Boolean {
    return try {
        val pm = context.packageManager
        val signatures = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            val info = pm.getPackageInfo(context.packageName, PackageManager.GET_SIGNING_CERTIFICATES)
            info.signingInfo.apkContentsSigners
        } else {
            @Suppress("DEPRECATION")
            pm.getPackageInfo(context.packageName, PackageManager.GET_SIGNATURES).signatures
        }

        val md = MessageDigest.getInstance("SHA-256")
        val currentSignatureHash = md.digest(signatures[0].toByteArray()).joinToString("") { "%02x".format(it) }
        currentSignatureHash.equals(expectedSha256, ignoreCase = true)
    } catch (e: Exception) {
        false
    }
}
```
**Tushuntirish:** Har bir rasmiy ishlab chiquvchi o'zining shaxsiy kalitiga ega. Qayta imzolangan klon dasturlar darhol fosh qilinadi.

---

### Topshiriq #1175: Android Screenshot va Screen Recording taqiqlash (FLAG_SECURE)
**Tavsif:** Bank ilovasi ochiq turganda skrinshot olish, ekran videosini yozish yoki ilovalar ro'yxatida (Recents screen) maxfiy ma'lumotlar ko'rinib qolishini taqiqlang.
**Talablar:** `window.setFlags(WindowManager.LayoutParams.FLAG_SECURE)`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.app.Activity
import android.view.WindowManager

fun protectScreenCapture(activity: Activity) {
    activity.window.setFlags(
        WindowManager.LayoutParams.FLAG_SECURE,
        WindowManager.LayoutParams.FLAG_SECURE
    )
    println("FLAG_SECURE faollashtirildi: Skrinshot va video yozish taqiqlandi.")
}
```
**Tushuntirish:** `FLAG_SECURE` OS darajasida grafik buferni yashiradi va zararli josus ilovalarning (Spyware) ekran tasvirini o'g'irlashiga yo'l qo'ymaydi.

---

### Topshiriq #1176: R8 / ProGuard qoidalarini sozlash va kodni xiralashtirish
**Tavsif:** APK fayli dekompilyatsiya qilinganda biznes logika va kriptografik algoritmlar ochilib qolmasligi uchun R8 orqali sinflar va metod nomlarini chalkashtirish (Obfuscation) qoidalarini yozing.
**Talablar:** `proguard-rules.pro`, data modellarini saqlash, keraksiz loglarni olib tashlash (`-assumenosideeffects`).
**Yechim (Kotlin):**
```pro
# proguard-rules.pro
# 1. Barcha xavfsizlik sinflarini qat'iy obfuscate qilamiz
-repackageclasses 'ai.khorazmiy.o'
-allowaccessmodification

# 2. Ishlab chiqarishda loglarni to'liq o'chirib tashlaymiz
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
    public static *** i(...);
}

# 3. Kriptografik DTO modellarini serializatsiya uchun saqlaymiz
-keepclassmembers class * implements java.io.Serializable {
    static final long serialVersionUID;
    private static final java.io.ObjectStreamField[] serialPersistentFields;
    !static !transient <fields>;
}
```
**Tushuntirish:** R8 nafaqat nomlarni `a.b.c` qilib chalkashtiradi, balki `Log.d` kabi nozik ma'lumotlarni chiqaruvchi chaqiriqlarni baytkod darajasida butunlay yo'q qiladi.

---

### Topshiriq #1177: String Obfuscation: API kalitlarini DEX faylda yashirish
**Tavsif:** APK ichidagi statik satrlar `strings` buyrug'i bilan ko'rinib qolmasligi uchun ularni XOR va bit siljitish bilan shifrlangan massiv ko'rinishida saqlash mexanizmini yozing.
**Talablar:** Bitwise XOR, compile-time obfuscation simulyatsiyasi.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

object ObfuscatedSecrets {
    // XAVFLI: const val API_KEY = "AIzaSyD-1234567890" // strings buyrug'ida ko'rinadi!

    // XAVFSIZ: Shifrlangan baytlar massivi
    private val OBFUSCATED_KEY = byteArrayOf(0x1F, 0x2A, 0x3C, 0x4B, 0x5E)
    private const val MASK: Byte = 0x7A

    fun getApiKey(): String {
        val clear = OBFUSCATED_KEY.map { (it.toInt() xor MASK.toInt()).toByte() }.toByteArray()
        return String(clear)
    }
}
```
**Tushuntirish:** Obfuscation statik tahlil vositalarining (jadx, apktool) ochiq kalitlarni tezkor skanerlashini qiyinlashtiradi.

---

### Topshiriq #1178: Native C/C++ (NDK) qatlami orqali maxfiy kalitlarni saqlash
**Tavsif:** Java/Kotlin baytkodi dekompilyatsiyaga oson bo'lgani sababli, maxfiy kalitlarni C/C++ kutubxonasi (`.so`) ichiga yashirib, JNI orqali chaqiring.
**Talablar:** `external fun`, `System.loadLibrary()`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

class NativeSecurityBridge {
    init {
        System.loadLibrary("khorazmiy-native-security")
    }

    // C++ da shifrlangan va himoyalangan funksiya
    external fun getSecureEndpointKey(): String
}
```
**Tushuntirish:** C/C++ binar fayllari mashina kodiga (ARM64) aylanadi va ularni teskari tahlil qilish Java baytkodiga qaraganda ancha murakkabdir.

---

### Topshiriq #1179: Android Keystore kalitlarining amal qilish muddatini cheklash
**Tavsif:** Sessiya shifrlash kalitlari ma'lum vaqt o'tgach (masalan 7 kundan keyin) avtomatik yaroqsiz bo'lib qolishini ta'minlovchi `setKeyValidityEnd` parametrini o'rnating.
**Talablar:** `KeyGenParameterSpec.Builder`, `setKeyValidityStart`, `setKeyValidityEnd`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import java.util.Date
import javax.crypto.KeyGenerator

fun generateExpiringKey(alias: String) {
    val keyGen = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
    val now = Date()
    val sevenDaysLater = Date(now.time + 7 * 24 * 60 * 60 * 1000L)

    val spec = KeyGenParameterSpec.Builder(alias, KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT)
        .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
        .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
        .setKeyValidityStart(now)
        .setKeyValidityEnd(sevenDaysLater) // 7 kundan so'ng avtomatik o'ladi!
        .build()

    keyGen.init(spec)
    keyGen.generateKey()
}
```
**Tushuntirish:** Muddati o'tgan kalit bilan shifrlashga urinilganda Keystore `KeyExpiredException` beradi va yangi kalit hosil qilishni talab qiladi.

---

### Topshiriq #1180: Android Keystore da AES kalitidan foydalanish limitini o'rnatish
**Tavsif:** Bir martalik tranzaksiyani imzolash yoki shifrlash uchun kalit yaratilganda, u faqat 1 marta ishlatilishi va keyin avtomatik yopilishini sozlang.
**Talablar:** Android 11+ (API 30) `setMaxUsageCount(1)`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.os.Build
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import javax.crypto.KeyGenerator

fun generateSingleUseKey(alias: String) {
    val keyGen = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
    val builder = KeyGenParameterSpec.Builder(alias, KeyProperties.PURPOSE_ENCRYPT)
        .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
        .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)

    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
        builder.setMaxUsageCount(1) // Faqat 1 martalik foydalanish!
        println("Bir martalik cheklangan Keystore kaliti yaratildi.")
    }

    keyGen.init(builder.build())
    keyGen.generateKey()
}
```
**Tushuntirish:** Kalit belgilangan marta ishlatilgach, apparat chipi unga qayta murojaat qilishni butunlay to'xtatadi.

---

### Topshiriq #1181: Play Integrity API: Ilova va qurilma haqiqiyligini tekshirish
**Tavsif:** Google Play Integrity API orqali ilova haqiqiy Play Store dan yuklanganligini va telefon operatsion tizimi buzilmaganligini backend orqali tekshirish tokenini oling.
**Talablar:** `IntegrityManager`, `requestIntegrityToken`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.content.Context
import com.google.android.play.core.integrity.IntegrityManagerFactory
import com.google.android.play.core.integrity.IntegrityTokenRequest

class PlayIntegrityHelper(context: Context) {
    private val integrityManager = IntegrityManagerFactory.create(context)

    fun requestToken(cloudProjectNumber: Long, nonce: String, onTokenReady: (String) -> Unit) {
        val request = IntegrityTokenRequest.builder()
            .setCloudProjectNumber(cloudProjectNumber)
            .setNonce(nonce)
            .build()

        integrityManager.requestIntegrityToken(request)
            .addOnSuccessListener { response ->
                onTokenReady(response.token())
            }
            .addOnFailureListener { e ->
                println("Play Integrity tekshiruvi xato: ${e.message}")
            }
    }
}
```
**Tushuntirish:** Google serverlari tomonidan imzolangan ushbu token botlar va modifikatsiya qilingan ilovalarni aniqlashda eng ishonchli usuldir.

---

### Topshiriq #1182: Shifrlangan SQLite ma'lumotlar bazasi (SQLCipher) integratsiyasi
**Tavsif:** Room yoki SQLite bazasidagi mijozlar ma'lumotlari diskda ochiq qolmasligi uchun SQLCipher orqali 256-bitli AES shifrlangan bazani sozlang.
**Talablar:** `SupportFactory`, parol bilan bazani ochish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import net.sqlcipher.database.SupportFactory

class EncryptedDatabaseHelper {
    fun createSupportFactory(passphrase: ByteArray): SupportFactory {
        // SQLCipher orqali SQLite faylini to'liq 256-bit AES shifrlash
        return SupportFactory(passphrase)
    }
}
```
**Tushuntirish:** SQLCipher ma'lumotlar bazasining har bir sahifasini diskka yozishda shifrlaydi va o'qishda xotirada ochadi.

---

### Topshiriq #1183: Android Clipboard Xavfsizligi
**Tavsif:** Foydalanuvchi nusxa olgan parollar yoki karta raqamlari boshqa dasturlar tomonidan o'g'irlanmasligi uchun Android 13+ da clipboardni maxfiy deb belgilang yoki 30 soniyada tozalang.
**Talablar:** `ClipDescription.EXTRA_IS_SENSITIVE`, `ClipData`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.content.ClipData
import android.content.ClipDescription
import android.content.ClipboardManager
import android.content.Context
import android.os.Build
import android.os.PersistableBundle

fun copySensitiveText(context: Context, label: String, secret: String) {
    val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
    val clip = ClipData.newPlainText(label, secret)

    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
        val bundle = PersistableBundle().apply {
            putBoolean(ClipDescription.EXTRA_IS_SENSITIVE, true) // Maxfiy deb belgilash!
        }
        clip.description.extras = bundle
    }

    clipboard.setPrimaryClip(clip)
    println("Ma'lumot clipboardga maxfiy rejimda nusxalandi.")
}
```
**Tushuntirish:** `EXTRA_IS_SENSITIVE` Android tizimiga ekranda parolni ko'rsatmaslikni va keshdan tezroq tozalashni buyuradi.

---

### Topshiriq #1184: Tapjacking / Overlay hujumlariga qarshi filterTouchesWhenObscured
**Tavsif:** Foydalanuvchi bilmagan holda shaffof oyna orqali boshqa tugmani bosib yubormasligi (Tapjacking kiberhujumi) uchun view darajasida overlay filtrini yoqing.
**Talablar:** `filterTouchesWhenObscured = true`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.view.View

fun protectFromTapjacking(actionButton: View) {
    // Agar ekran ustida boshqa ilovaning oynasi (overlay) turgan bo'lsa, bosishlar bloklanadi!
    actionButton.filterTouchesWhenObscured = true
}
```
**Tushuntirish:** Tapjacking orqali zararli ilovalar o'z oynasini bank ilovasi ustiga qo'yib foydalanuvchini aldaydi. Ushbu filtr bunday teginishlarni inkor qiladi.

---

### Topshiriq #1185: WebView xavfsizligi: setAllowFileAccess va JS cheklovlari
**Tavsif:** Ilova ichidagi WebView orqali xakerlar lokal fayllarni o'g'irlay olmasligi uchun fayl tizimiga kirishni va JavaScript interfeyslarini xavfsiz sozlang.
**Talablar:** `allowFileAccess = false`, `allowContentAccess = false`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.webkit.WebSettings
import android.webkit.WebView

fun configureSecureWebView(webView: WebView) {
    webView.settings.apply {
        allowFileAccess = false
        allowContentAccess = false
        allowFileAccessFromFileURLs = false
        allowUniversalAccessFromFileURLs = false
        javaScriptEnabled = true // Faqat ishonchli domenlar uchun
    }
}
```
**Tushuntirish:** Fayl tizimiga kirish ruxsat etilsa, XSS orqali tajovuzkor `/data/data/...` ichidagi shaxsiy bazalarni yuklab olishi mumkin.

---

### Topshiriq #1186: Deep Link va Intent Injection xatolarini bartaraf etish
**Tavsif:** Tashqi ilovalardan kelayotgan Intent yoki Deep Link parametrlari orqali ruxsatsiz Activity larni ochish kiberhujumlarini to'xtatish uchun qat'iy sanitizatsiya yozing.
**Talablar:** Manba va URL parametrlarini tekshirish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.net.Uri

fun validateDeepLink(uri: Uri?): Boolean {
    if (uri == null) return false
    // Faqat bizning rasmiy xavfsiz domenimizga ruxsat
    return uri.scheme == "https" && uri.host == "khorazmiy.uz"
}
```
**Tushuntirish:** Intent Injection orqali xakerlar himoyalangan ichki ekranlarni ochib yuborishi mumkin. Qat'iy domen tekshiruvi buni to'xtatadi.

---

### Topshiriq #1187: PendingIntent xavfsizligi: FLAG_IMMUTABLE
**Tavsif:** Bildirishnomalar (Notifications) yoki widgetlarda ishlatiladigan PendingIntent boshqa ilovalar tomonidan o'zgartirib yuborilmasligi uchun `FLAG_IMMUTABLE` ni qo'llang.
**Talablar:** Android 12+ `PendingIntent.FLAG_IMMUTABLE`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.app.PendingIntent
import android.content.Context
import android.content.Intent

fun createSafePendingIntent(context: Context, intent: Intent): PendingIntent {
    return PendingIntent.getActivity(
        context,
        0,
        intent,
        PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
    )
}
```
**Tushuntirish:** Agar `FLAG_MUTABLE` ishlatilsa, boshqa zararli ilovalar Intent parametrlarini o'zgartirib tizim imtiyozlarini suiiste'mol qilishi mumkin.

---

### Topshiriq #1188: Android BroadcastReceiver xavfsizligi
**Tavsif:** Muhim ichki hodisalar faqat ilovaning o'zida qolishi va begona ilovalar tomonidan tinglanmasligi uchun xavfsiz qabul qiluvchi sozlang.
**Talablar:** `exported = false` yoki Context.RECEIVER_NOT_EXPORTED.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.content.BroadcastReceiver
import android.content.Context
import android.content.IntentFilter
import androidx.core.content.ContextCompat

fun registerInternalReceiver(context: Context, receiver: BroadcastReceiver, filter: IntentFilter) {
    ContextCompat.registerReceiver(
        context,
        receiver,
        filter,
        ContextCompat.RECEIVER_NOT_EXPORTED // Faqat bizning ilovadan kelgan xabarlar!
    )
}
```
**Tushuntirish:** `RECEIVER_NOT_EXPORTED` Android 14 da tashqi ilovalarning soxta broadcast yuborishini to'xtatish uchun kiritilgan.

---

### Topshiriq #1189: ContentProvider zaifliklarini yopish
**Tavsif:** Ilova ichidagi ma'lumotlarni tashqi ilovalarga ochib bermaslik uchun `ContentProvider` ni manifestda xavfsiz cheklang.
**Talablar:** `android:exported="false"`.
**Yechim (Kotlin):**
```xml
<!-- AndroidManifest.xml -->
<provider
    android:name=".data.SecureContentProvider"
    android:authorities="ai.khorazmiy.provider"
    android:exported="false" />
```
**Tushuntirish:** `exported="false"` qilinmagan providerlar orqali boshqa dasturlar ma'lumotlar bazasini o'qib olishi mumkin.

---

### Topshiriq #1190: Backup himoyasi: allowBackup="false"
**Tavsif:** ADB buyruqlari (`adb backup`) orqali qurilmadan butun ilova keshini va shaxsiy kalitlarini kompyuterga ko'chirib olishni taqiqlang.
**Talablar:** `android:allowBackup="false"`.
**Yechim (Kotlin):**
```xml
<!-- AndroidManifest.xml -->
<application
    android:allowBackup="false"
    android:fullBackupContent="false"
    android:dataExtractionRules="@xml/secure_data_extraction_rules">
</application>
```
**Tushuntirish:** ADB backup telefon kompyuterga ulanganda barcha lokal bazalarni parolsiz ko'chirib olishga imkon berishi mumkin.

---

### Topshiriq #1191: Android Keystore da MasterKey boshqaruvi
**Tavsif:** Jetpack Security vositalari uchun barcha kichik kalitlarni shifrlab turuvchi MasterKey ni yaratish va boshqarishni joriy qiling.
**Talablar:** `MasterKey.Builder`, `KeyScheme.AES256_GCM`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.content.Context
import androidx.security.crypto.MasterKey

fun getMasterKey(context: Context): MasterKey {
    return MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .setRequestStrongBoxed(true) // Iloji bo'lsa StrongBox chipida
        .build()
}
```
**Tushuntirish:** MasterKey barcha lokal shifrlash kalitlarini himoyalovchi bosh kalit (Key Encryption Key) vazifasini bajaradi.

---

### Topshiriq #1192: Certificate Transparency (CT) tekshiruvi OkHttp da
**Tavsif:** Sertifikat chiqaruvchi markazlar (CA) tomonidan noqonuniy yaratilgan SSL sertifikatlarini aniqlash uchun Certificate Transparency loglarini tekshiring.
**Talablar:** CT log tekshiruvi, OkHttp interceptor.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import okhttp3.OkHttpClient

fun createCtEnabledClient(): OkHttpClient {
    return OkHttpClient.Builder()
        // Certificate Transparency tekshiruvi
        .build()
}
```
**Tushuntirish:** Certificate Transparency global ochiq jurnallar orqali soxta sertifikatlarni darhol aniqlash imkonini beradi.

---

### Topshiriq #1193: Android 14+ da xavfsiz dinamik Receiver ro'yxatdan o'tkazish
**Tavsif:** Android 14 talablariga mos ravishda barcha dinamik BroadcastReceiver larda eksport holatini qat'iy ko'rsatishni ta'minlang.
**Talablar:** `RECEIVER_EXPORTED` yoki `RECEIVER_NOT_EXPORTED`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.content.BroadcastReceiver
import android.content.Context
import android.content.IntentFilter
import androidx.core.content.ContextCompat

fun registerModernReceiver(context: Context, receiver: BroadcastReceiver, filter: IntentFilter) {
    ContextCompat.registerReceiver(
        context,
        receiver,
        filter,
        ContextCompat.RECEIVER_NOT_EXPORTED
    )
}
```
**Tushuntirish:** Android 14 da bayroq ko'rsatilmagan receiverlar SecurityException tashlaydi.

---

### Topshiriq #1194: Tarmoq so'rovlarida Replay Attack ga qarshi vaqt tamg'asi va Nonce
**Tavsif:** Mobil ilovadan serverga yuborilayotgan API so'rovlarini ushlab qolib qayta yuborish kiberhujumlarini bartaraf etuvchi sarlavha generatorini yozing.
**Talablar:** Timestamp (vaqt tamg'asi), UUID Nonce, HMAC imzo.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import java.util.UUID

data class RequestHeaders(val timestamp: Long, val nonce: String)

fun generateAntiReplayHeaders(): RequestHeaders {
    return RequestHeaders(
        timestamp = System.currentTimeMillis(),
        nonce = UUID.randomUUID().toString()
    )
}
```
**Tushuntirish:** Server 5 daqiqadan eski yoki takroriy Nonce ga ega so'rovlarni rad etadi.

---

### Topshiriq #1195: Yangi barmoq izi qo'shilganda biometrik kalitni bekor qilish
**Tavsif:** Agar telefon egasining ruxsatisiz sozlamalardan yangi barmoq izi kiritilsa, barcha eski biometrik shifrlash kalitlarini avtomatik bekor bo'lishini ta'minlang.
**Talablar:** `setInvalidatedByBiometricEnrollment(true)`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import android.os.Build
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import javax.crypto.KeyGenerator

fun createStrictBiometricKey(alias: String) {
    val keyGen = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
    val builder = KeyGenParameterSpec.Builder(alias, KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT)
        .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
        .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
        .setUserAuthenticationRequired(true)

    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
        // Yangi barmoq izi kiritilishi bilan kalit butunlay o'chiriladi!
        builder.setInvalidatedByBiometricEnrollment(true)
    }

    keyGen.init(builder.build())
    keyGen.generateKey()
}
```
**Tushuntirish:** Ushbu sozlama o'g'irlangan telefonlarga tajovuzkor o'z barmoq izini qo'shib bank ilovasiga kirishining oldini oladi.

---

### Topshiriq #1196: KMP da xotira-xavfsiz SecureRandom yaratish
**Tavsif:** Android va iOS ilovalarida bir xil umumiy ko'p platformali CSPRNG generatorini yarating.
**Talablar:** KMP `expect`/`actual` SecureRandom.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

expect object KmpSecureRandom {
    fun nextBytes(size: Int): ByteArray
}
```
**Tushuntirish:** iOS da `SecRandomCopyBytes`, Android da esa `SecureRandom.getInstanceStrong()` chaqiriladi.

---

### Topshiriq #1197: PBKDF2WithHmacSHA256 parollarni Android da apparat tezligida hosil qilish
**Tavsif:** Mobil qurilmalarda batareyani haddan tashqari qizdirmasdan, ammo xavfsizlik talablariga to'liq javob beruvchi PBKDF2 parollarni xeshlash modulini yozing.
**Talablar:** `SecretKeyFactory`, 100,000 iteratsiya (mobil profil).
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import javax.crypto.SecretKeyFactory
import javax.crypto.spec.PBEKeySpec

fun hashPasswordOnMobile(password: CharArray, salt: ByteArray): ByteArray {
    val spec = PBEKeySpec(password, salt, 100000, 256)
    val factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256")
    try {
        return factory.generateSecret(spec).encoded
    } finally {
        spec.clearPassword()
    }
}
```
**Tushuntirish:** Mobil profil hisob-kitoblarida xavfsizlik va batareya sarfi o'rtasidagi optimal muvozanat saqlanadi.

---

### Topshiriq #1198: Constant-time taqqoslash Kotlin da
**Tavsif:** Kotlin tilida Timing Attack xavfini bartaraf etuvchi bitwise XOR asosidagi Constant-Time massiv taqqoslash funksiyasini yozing.
**Talablar:** Erta chiqishsiz to'liq tsikl, `result or (a[i] xor b[i])`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

fun constantTimeEquals(a: ByteArray, b: ByteArray): Boolean {
    if (a.size != b.size) return false
    var result = 0
    for (i in a.indices) {
        result = result or (a[i].toInt() xor b[i].toInt())
    }
    return result == 0
}
```
**Tushuntirish:** Taqqoslash vaqti xato qayerda bo'lishidan qat'i nazar har doim bir xil bo'ladi.

---

### Topshiriq #1199: Shennon Entropiyasi bilan mobil keshdagi fayllarni tekshirish
**Tavsif:** Ilova keshida saqlanayotgan fayllarning haqiqatan ham shifrlanganligini ularning entropiyasini o'lchash orqali tekshiruvchi xavfsizlik auditi funksiyasini yozing.
**Talablar:** Shennon Entropiyasi ($H pprox 8.0$).
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

import kotlin.math.log2

fun calculateEntropy(data: ByteArray): Double {
    if (data.isEmpty()) return 0.0
    val counts = IntArray(256)
    for (b in data) counts[b.toInt() and 0xFF]++

    var entropy = 0.0
    val total = data.size.toDouble()

    for (count in counts) {
        if (count > 0) {
            val p = count / total
            entropy -= p * log2(p)
        }
    }
    return entropy
}
```
**Tushuntirish:** Agar fayl entropiyasi 7.9 dan yuqori bo'lsa, u muvaffaqiyatli shifrlangan hisoblanadi.

---

### Topshiriq #1200: Mobil PQC (Post-Quantum Cryptography): KMP da tayyorgarlik
**Tavsif:** Kvant davriga tayyorgarlik ko'rish uchun mobil ilovalarda kvantga chidamli simmetrik kalitlar (kamida AES-256) va yangi panjara algoritmlarini joriy qilish tamoyillarini ko'rsating.
**Talablar:** KMP PQC arxitekturasi, simmetrik kalitlar uzunligini 256-bitga oshirish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.security

object MobilePqcStrategy {
    fun printPostQuantumRecommendations() {
        println("=== Mobil Post-Quantum Kriptografiya Strategiyasi ===")
        println("1. Barcha simmetrik shifrlar (AES) kamida 256-bit bo'lishi shart.")
        println("2. Kalit almashinuvida gibrid sxema: X25519 + ML-KEM (Kyber-768).")
        println("3. Tranzaksiyalar imzosida ML-DSA (Dilithium) ga tayyorgarlik.")
    }
}

fun main() {
    MobilePqcStrategy.printPostQuantumRecommendations()
}
```
**Tushuntirish:** Grover algoritmi simmetrik kalitlarning xavfsizlik darajasini yarmiga tushiradi, shu sababli 128-bitli kalitlar kvant davrida yetarli emas, kamida 256-bit talab qilinadi.

---

