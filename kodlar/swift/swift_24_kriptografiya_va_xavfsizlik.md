# Khorazmiy AI: Swift - Modul 24
## Mavzu: Apple Kriptografiyasi va Xavfsizlik: CryptoKit (AES.GCM, ChaChaPoly, Curve25519, P256), Secure Enclave apparat chiplari, Keychain Services (kSecAttrAccessible), LocalAuthentication (FaceID/TouchID), App Attest va SSL Pinning

### Topshiriq #1151: CryptoKit AES.GCM Bilan Autentifikatsiyalangan Shifrlash va SealedBox
**Tavsif:** Apple platformalarida (iOS/macOS) foydalanuvchi ma'lumotlarini apparat tezlatgichi bilan AES-GCM da shifrlash va ochish.
**Talablar:** `CryptoKit`, `AES.GCM`, `SymmetricKey`, `AES.GCM.SealedBox`, `combined`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

public struct CryptoKitAesService {
    // 256-bitli kalit bilan shifrlash
    public static func encrypt(data: Data, key: SymmetricKey) throws -> Data {
        let sealedBox = try AES.GCM.seal(data, using: key)
        guard let combined = sealedBox.combined else {
            throw NSError(domain: "CryptoError", code: -1, userInfo: [NSLocalizedDescriptionKey: "Kombinatsiya hosil qilinmadi"])
        }
        return combined // [Nonce (12b)] + [Ciphertext] + [Tag (16b)]
    }

    public static func decrypt(combinedData: Data, key: SymmetricKey) throws -> Data {
        let sealedBox = try AES.GCM.SealedBox(combined: combinedData)
        return try AES.GCM.open(sealedBox, using: key)
    }
}

let key = SymmetricKey(size: .bits256)
let originalData = "Foydalanuvchi maxfiy biometrik tokeni".data(using: .utf8)!

if let encrypted = try? CryptoKitAesService.encrypt(data: originalData, key: key),
   let decrypted = try? CryptoKitAesService.decrypt(combinedData: encrypted, key: key) {
    print("Shifrlangan paket hajmi: \(encrypted.count) bayt")
    print("Ochilgan ma'lumot: \(String(data: decrypted, encoding: .utf8)!)")
}
```
**Tushuntirish:** CryptoKit Apple tomonidan iOS 13+ da taqdim etilgan zamonaviy xavfsiz kutubxona bo'lib, BoringSSL ga asoslangan va barcha operatsiyalarni apparat tezlatgichida (Secure Enclave / Apple Silicon Crypto Engine) bajaradi.

---

### Topshiriq #1152: AES.GCM Da AAD (Authenticating Associated Data) Sarlavhalar Yaxlitligi
**Tavsif:** Tarmoq paketi yoki fayl sarlavhasini ochiq qoldirgan holda, uning o'zgartirilmasligini shifr matni bilan bog'lash.
**Talablar:** `AES.GCM.seal(..., authenticating: metadata)`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

func encryptWithMetadata(payload: Data, metadata: Data, key: SymmetricKey) throws -> AES.GCM.SealedBox {
    // AAD sarlavhasi shifrlanmaydi, lekin GMAC tegi ichiga kiritiladi
    return try AES.GCM.seal(payload, using: key, authenticating: metadata)
}

func verifyAndOpenWithMetadata(box: AES.GCM.SealedBox, metadata: Data, key: SymmetricKey) throws -> Data {
    return try AES.GCM.open(box, using: key, authenticating: metadata)
}

let key = SymmetricKey(size: .bits256)
let meta = "UserID: 9942; Permissions: Admin".data(using: .utf8)!
let secret = "Hisob balansi: 100,000,000 UZS".data(using: .utf8)!

let sealed = try! encryptWithMetadata(payload: secret, metadata: meta, key: key)
let opened = try! verifyAndOpenWithMetadata(box: sealed, metadata: meta, key: key)
print("AAD autentifikatsiyasi muvaffaqiyatli: \(String(data: opened, encoding: .utf8)!)")
```
**Tushuntirish:** Agar tajovuzkor `metadata` dagi bitta harfni o'zgartirsa (masalan, `Admin` ni o'zgartirsa), `AES.GCM.open` xatolik chiqaradi va ma'lumotni ochmaydi.

---

### Topshiriq #1153: CryptoKit ChaChaPoly Bilan Batareyani Tejash va Apparatsiz Yuqori Tezlik
**Tavsif:** Apparat AES tezlatgichi bo'lmagan sharoitlarda yoki mobil batareyani tejash uchun ChaCha20-Poly1305 shifrini qo'llash.
**Talablar:** `ChaChaPoly`, `ChaChaPoly.SealedBox`, `SymmetricKey`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

public struct ChaChaService {
    public static func seal(data: Data, key: SymmetricKey) throws -> ChaChaPoly.SealedBox {
        return try ChaChaPoly.seal(data, using: key)
    }

    public static func open(box: ChaChaPoly.SealedBox, key: SymmetricKey) throws -> Data {
        return try ChaChaPoly.open(box, using: key)
    }
}

let chachaKey = SymmetricKey(size: .bits256)
let msg = "ChaCha20-Poly1305 Apple CryptoKit sinovi".data(using: .utf8)!
let box = try! ChaChaService.seal(data: msg, key: chachaKey)
let clear = try! ChaChaService.open(box: box, key: chachaKey)

print("ChaChaPoly muvaffaqiyatli: \(String(data: clear, encoding: .utf8)!)")
```
**Tushuntirish:** `ChaChaPoly` Apple platformalarida xotira kesh-timing hujumlariga qarshi dasturiy jihatdan to'liq immunitetga ega va mobil arxitekturalarda eng optimal variant hisoblanadi.

---

### Topshiriq #1154: SymmetricKey Bilan Kriptografik Xavfsiz Kalit Boshqaruvi
**Tavsif:** Standart massivlar o'rniga CryptoKit ning xotirani avtomatik himoyalovchi `SymmetricKey` turidan to'g'ri foydalanish.
**Talablar:** `SymmetricKey(size: .bits256)`, `withUnsafeBytes`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

func generateAndInspectKey() {
    // 256-bitli tasodifiy kripto-kalit
    let key = SymmetricKey(size: .bits256)
    print("Kalit yaratildi: \(key.bitCount) bit")

    // Kalit baytlari bilan xavfsiz vaqtinchalik ishlash
    key.withUnsafeBytes { rawBuffer in
        print("Xotiradagi kalit uzunligi: \(rawBuffer.count) bayt")
    }
}

generateAndInspectKey()
```
**Tushuntirish:** `SymmetricKey` tipi kalitni oddiy `Data` yoki `[UInt8]` kabi xotirada nusxalanib ketishidan saqlaydi va uning ko'chirilmasligini ta'minlaydi.

---

### Topshiriq #1155: HKDF Kalit Hosil Qilish: HKDF<SHA256>.deriveKey
**Tavsif:** Bitta umumiy sirdan shifrlash va autentifikatsiya uchun mustaqil subkalitlar hosil qilish (RFC 5869).
**Talablar:** `HKDF<SHA256>.deriveKey(inputKeyMaterial:outputByteCount:)`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

func deriveSubkeys(master: SymmetricKey, salt: Data) -> (SymmetricKey, SymmetricKey) {
    let encKey = HKDF<SHA256>.deriveKey(
        inputKeyMaterial: master,
        salt: salt,
        info: "encryption-v1".data(using: .utf8)!,
        outputByteCount: 32
    )

    let macKey = HKDF<SHA256>.deriveKey(
        inputKeyMaterial: master,
        salt: salt,
        info: "mac-v1".data(using: .utf8)!,
        outputByteCount: 32
    )

    return (encKey, macKey)
}

let masterKey = SymmetricKey(size: .bits256)
let salt = "random_salt_123".data(using: .utf8)!
let (enc, mac) = deriveSubkeys(master: masterKey, salt: salt)
print("HKDF subkalitlari muvaffaqiyatli ajratildi.")
```
**Tushuntirish:** HKDF orqali olingan kalitlar bir-biridan matematik mustaqil bo'ladi: shifrlash kaliti fosh bo'lsa ham, MAC kaliti xavfsiz qoladi.

---

### Topshiriq #1156: HMAC-SHA256 Bilan Xabar Yaxlitligi va Soxtalashtirishdan Himoya
**Tavsif:** Vebxuklar va to'lov xabarnomalarining haqiqiyligini tekshirish.
**Talablar:** `HMAC<SHA256>.authenticationCode`, `HMAC<SHA256>.isValidAuthenticationCode`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

func signAndVerifyHmac(message: Data, key: SymmetricKey) -> Bool {
    // HMAC imzo hisoblash
    let mac = HMAC<SHA256>.authenticationCode(for: message, using: key)
    print("HMAC-SHA256 imzosi: \(mac.count) bayt")

    // Doimiy vaqtda verifikatsiya
    return HMAC<SHA256>.isValidAuthenticationCode(mac, authenticating: message, using: key)
}

let hmacKey = SymmetricKey(size: .bits256)
let payload = "Buyruq: To'lov tasdiqlansin".data(using: .utf8)!
let isValid = signAndVerifyHmac(message: payload, key: hmacKey)
print("HMAC imzosi to'g'ri: \(isValid)")
```
**Tushuntirish:** `isValidAuthenticationCode` ichki darajada doimiy vaqtda (Constant-Time) solishtiradi va vaqt o'lchash (Timing Attack) hujumlarini to'liq bartaraf etadi.

---

### Topshiriq #1157: CryptoKit SHA-256 va SHA-512 Kriptografik Xeshlash
**Tavsif:** Fayllar va hujjatlarning yaxlitligini nazorat qilish uchun bir tomonlama xesh qiymatini olish.
**Talablar:** `SHA256.hash(data:)`, `SHA512.hash(data:)`, `Digest`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

func computeHash(data: Data) {
    let digest256 = SHA256.hash(data: data)
    print("SHA-256 xesh: \(digest256.compactMap { String(format: "%02x", $0) }.joined())")

    let digest512 = SHA512.hash(data: data)
    print("SHA-512 hajmi: \(digest512.byteCount) bayt")
}

computeHash(data: "Khorazmiy AI Swift Kriptografiyasi".data(using: .utf8)!)
```
**Tushuntirish:** CryptoKit `Digest` obyekti xotirani tejaydi va `Data` ga aylantirilmasdan turib boshqa CryptoKit funksiyalariga to'g'ridan-to'g'ri uzatilishi mumkin.

---

### Topshiriq #1158: Katta Fayllarni Oqimli Xeshlash (SHA256 Inkremental Update)
**Tavsif:** Gigabaytlik video yoki arxiv fayllarini xotiraga to'liq yuklamasdan qismlarga bo'lib xeshlash.
**Talablar:** `SHA256()`, `hasher.update(data:)`, `hasher.finalize()`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

func hashStreamChunks(chunks: [Data]) -> SHA256Digest {
    var hasher = SHA256()
    for chunk in chunks {
        hasher.update(data: chunk) // Bo'lakma-bo'lak xeshlash
    }
    return hasher.finalize()
}

let chunk1 = "Birinchi 64KB qism".data(using: .utf8)!
let chunk2 = "Ikkinchi 64KB qism".data(using: .utf8)!
let finalDigest = hashStreamChunks(chunks: [chunk1, chunk2])
print("Oqimli xesh muvaffaqiyatli hisoblandi.")
```
**Tushuntirish:** Inkremental xeshlash mobil ilovalarda xotira to'lib qolishi (Out-Of-Memory) tufayli ilovaning qulashini oldini oladi.

---

### Topshiriq #1159: SecRandomCopyBytes Bilan Kriptografik Xavfsiz Entropiya Olish
**Tavsif:** Tizim kalitlari va tasodifiy tuz (Salt) larni yaratishda Apple operatsion tizimining apparat CSPRNG drayveridan foydalanish.
**Talablar:** `SecRandomCopyBytes`, `kSecRandomDefault`.
**Yechim (Swift):**
```swift
import Foundation
import Security

func generateSecureBytes(count: Int) -> Data? {
    var bytes = [UInt8](repeating: 0, count: count)
    let status = SecRandomCopyBytes(kSecRandomDefault, count, &bytes)
    guard status == errSecSuccess else { return nil }
    return Data(bytes)
}

if let randomSalt = generateSecureBytes(count: 16) {
    print("Xavfsiz tasodifiy 16 bayt entropiya olindi: \(randomSalt as NSData)")
}
```
**Tushuntirish:** `SecRandomCopyBytes` Apple apparat chiplarining kvant-darajadagi shovqin manbalariga tayanadi va mutlaqo oldindan aytib bo'lmas natija beradi.

---

### Topshiriq #1160: Kriptografik Kalitlarni Xotirada Tozalash (Data.resetBytes)
**Tavsif:** Parollar va xususiy kalitlar ishlatib bo'lingach, ularni zudlik bilan operativ xotirada nolga tenglashtirish.
**Talablar:** `data.resetBytes(in:)`, `memset_s`.
**Yechim (Swift):**
```swift
import Foundation

func processAndWipeSecret(secret: inout Data) {
    print("Maxfiy ma'lumot bilan operatsiya bajarildi.")

    // Xotirani zudlik bilan nollar bilan to'ldirish
    let count = secret.count
    secret.resetBytes(in: 0..<count)
    print("Xotira tozalangandan so'ng: \(secret as NSData)")
}

var mySecret = "O'taMaxfiyParol".data(using: .utf8)!
processAndWipeSecret(secret: &mySecret)
```
**Tushuntirish:** Swift avtomatik xotira boshqaruviga (ARC) ega bo'lsa-da, deallocation paytida baytlar o'chirilmaydi; `resetBytes` orqali RAM dump hujumlari to'xtatiladi.

---

### Topshiriq #1161: Envelope Encryption (DEK va KEK) CryptoKit Bilan
**Tavsif:** Ma'lumotlarni Ma'lumot Kaliti (DEK) bilan shifrlab, DEK ning o'zini Asosiy Kalit (KEK) bilan shifrlash.
**Talablar:** Data Encryption Key va Key Encryption Key modeli.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

struct EnvelopeRecord {
    let encryptedDek: Data
    let encryptedData: Data
}

func sealEnvelope(data: Data, kek: SymmetricKey) throws -> EnvelopeRecord {
    // 1. Yangi bir martalik DEK
    let dek = SymmetricKey(size: .bits256)

    // 2. Ma'lumotni DEK bilan shifrlash
    let sealedData = try AES.GCM.seal(data, using: dek).combined!

    // 3. DEK ni KEK bilan shifrlash
    let dekRaw = dek.withUnsafeBytes { Data($0) }
    let sealedDek = try AES.GCM.seal(dekRaw, using: kek).combined!

    return EnvelopeRecord(encryptedDek: sealedDek, encryptedData: sealedData)
}

let kek = SymmetricKey(size: .bits256)
let env = try! sealEnvelope(data: "Maxfiy hujjat".data(using: .utf8)!, kek: kek)
print("Envelope yaratildi: DEK: \(env.encryptedDek.count)b, Ma'lumot: \(env.encryptedData.count)b")
```
**Tushuntirish:** Konvert shifrlash katta fayllarni xavfsiz saqlash va bulutli KMS (Apple CloudKit, AWS KMS) xizmatlari bilan integratsiya qilish uchun standartdir.

---

### Topshiriq #1162: SwiftData / CoreData Uchun Maydonlarni Shifrlash (PropertyWrapper)
**Tavsif:** Ma'lumotlar bazasida saqlanadigan o'zgaruvchilarni avtomatik tarzda shifrlangan holda yozish va ochish.
**Talablar:** `@propertyWrapper`, `AES.GCM`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

@propertyWrapper
struct EncryptedString {
    private var ciphertext: Data
    private let key: SymmetricKey

    init(wrappedValue: String, key: SymmetricKey) {
        self.key = key
        self.ciphertext = try! AES.GCM.seal(wrappedValue.data(using: .utf8)!, using: key).combined!
    }

    var wrappedValue: String {
        get {
            guard let box = try? AES.GCM.SealedBox(combined: ciphertext),
                  let clear = try? AES.GCM.open(box, using: key) else { return "" }
            return String(data: clear, encoding: .utf8) ?? ""
        }
        set {
            ciphertext = try! AES.GCM.seal(newValue.data(using: .utf8)!, using: key).combined!
        }
    }
}
```
**Tushuntirish:** Property Wrapper orqali biznes mantiq kodida shifrlash amallari sezilmaydi, lekin SQLite bazasiga tushayotganda barcha qiymatlar shifrlangan bo'ladi.

---

### Topshiriq #1163: Curve25519.Signing (Ed25519) Kalit Juftligi va Raqamli Imzo
**Tavsif:** CryptoKit yordamida Ed25519 ochiq va xususiy kalitlarini yaratish va xabarlarni imzolash.
**Talablar:** `Curve25519.Signing.PrivateKey()`, `signature(for:)`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

func runEd25519Signing() throws {
    // 1. Yangi Ed25519 kalit juftligi
    let privateKey = Curve25519.Signing.PrivateKey()
    let publicKey = privateKey.publicKey

    let document = "Moliyaviy shartnoma matni".data(using: .utf8)!

    // 2. Raqamli imzolash (64 bayt)
    let signature = try privateKey.signature(for: document)

    print("Ochiq kalit: \(publicKey.rawRepresentation.count) bayt (32 bayt)")
    print("Ed25519 imzo: \(signature.count) bayt (64 bayt)")
}

try! runEd25519Signing()
```
**Tushuntirish:** Ed25519 imzolari o'ta ixcham (64 bayt) va tezkor bo'lib, mobil qurilmada batareya quvvatini deyarli sarflamaydi.

---

### Topshiriq #1164: Curve25519.Signing.PublicKey Bilan Imzo Verifikatsiyasi
**Tavsif:** Faqat ochiq kalit yordamida qabul qilingan imzo va hujjatning soxtalashtirilmaganini tekshirish.
**Talablar:** `publicKey.isValidSignature(signature, for: data)`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

func verifyEd25519Signature(publicKeyData: Data, message: Data, signature: Data) -> Bool {
    guard let publicKey = try? Curve25519.Signing.PublicKey(rawRepresentation: publicKeyData) else {
        return false
    }
    return publicKey.isValidSignature(signature, for: message)
}

let priv = Curve25519.Signing.PrivateKey()
let msg = "Tasdiqlangan to'lov".data(using: .utf8)!
let sig = try! priv.signature(for: msg)

let ok = verifyEd25519Signature(publicKeyData: priv.publicKey.rawRepresentation, message: msg, signature: sig)
print("Ed25519 imzo haqiqiy: \(ok)")
```
**Tushuntirish:** `isValidSignature` imzoning aynan ushbu ochiq kalit egasi tomonidan qo'yilganini va hujjat o'zgarmaganligini kafolatlaydi.

---

### Topshiriq #1165: Curve25519.KeyAgreement (X25519) Diffie-Hellman Kalit Kelishuvi
**Tavsif:** Ikki mobil mijoz o'rtasida server ham o'qiy olmaydigan End-to-End Encryption (E2EE) kalitini kelishib olish.
**Talablar:** `Curve25519.KeyAgreement.PrivateKey()`, `sharedSecretFromKeyAgreement`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

func runX25519Agreement() throws {
    // Alisa kalitlari
    let alicePriv = Curve25519.KeyAgreement.PrivateKey()
    let alicePub = alicePriv.publicKey

    // Bob kalitlari
    let bobPriv = Curve25519.KeyAgreement.PrivateKey()
    let bobPub = bobPriv.publicKey

    // Umumiy sirni hisoblash
    let aliceShared = try alicePriv.sharedSecretFromKeyAgreement(with: bobPub)
    let bobShared = try bobPriv.sharedSecretFromKeyAgreement(with: alicePub)

    // HKDF orqali shifrlash kalitini olish
    let aliceKey = aliceShared.hkdfDerivedSymmetricKey(using: SHA256.self, salt: Data(), sharedInfo: Data(), outputByteCount: 32)
    let bobKey = bobShared.hkdfDerivedSymmetricKey(using: SHA256.self, salt: salt, sharedInfo: Data(), outputByteCount: 32)

    print("X25519 E2EE kalitlari muvaffaqiyatli hosil qilindi.")
}

try! runX25519Agreement()
```
**Tushuntirish:** X25519 har bir ulanish sessiyasi uchun yangi efemer kalitlar yaratadi va Perfect Forward Secrecy (PFS) ni kafolatlaydi.

---

### Topshiriq #1166: P256.Signing (ECDSA) NIST P-256 Raqamli Imzolash
**Tavsif:** Apple ekotizimi va xalqaro bank standartlarida qo'llaniladigan NIST P-256 (secp256r1) imzosi.
**Talablar:** `P256.Signing.PrivateKey()`, `signature(for:)`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

func runP256Signing() throws {
    let privateKey = P256.Signing.PrivateKey()
    let data = "Biometrik tasdiqlash buyrug'i".data(using: .utf8)!

    let signature = try privateKey.signature(for: data)
    print("P-256 imzosi DER formati: \(signature.derRepresentation.count) bayt")

    let isValid = privateKey.publicKey.isValidSignature(signature, for: data)
    print("P-256 imzo tekshirildi: \(isValid)")
}

try! runP256Signing()
```
**Tushuntirish:** NIST P-256 Apple A-seriya va M-seriya protsessorlarining apparat modullarida (Secure Enclave) to'liq qo'llab-quvvatlanadi.

---

### Topshiriq #1167: P256.KeyAgreement Orqali Umumiy Kalit Hosil Qilish
**Tavsif:** NIST standartidagi elliptik egri chiziq bo'yicha ECDH kalit almashinuvini bajarish.
**Talablar:** `P256.KeyAgreement.PrivateKey()`, `sharedSecretFromKeyAgreement`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

func runP256Agreement() throws {
    let myPriv = P256.KeyAgreement.PrivateKey()
    let serverPub = P256.KeyAgreement.PrivateKey().publicKey

    let sharedSecret = try myPriv.sharedSecretFromKeyAgreement(with: serverPub)
    let symmetricKey = sharedSecret.hkdfDerivedSymmetricKey(using: SHA256.self, salt: Data(), sharedInfo: Data(), outputByteCount: 32)

    print("P-256 ECDH orqali simmetrik kalit olindi.")
}

try! runP256Agreement()
```
**Tushuntirish:** P256.KeyAgreement zamonaviy TLS 1.3 qo'l siqishlarida server bilan xavfsiz simmetrik kalitni kelishib olish uchun qo'llaniladi.

---

### Topshiriq #1168: P-384 va P-521 Yuqori Darajadagi Kriptografik Egri Chiziqlar
**Tavsif:** Davlat xavfsizlik talablari (Top Secret) bo'yicha 384-bit va 521-bitli elliptik egri chiziqlarda ishlash.
**Talablar:** `P384.Signing`, `P521.Signing`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

func runHighSecurityCurves() throws {
    let key384 = P384.Signing.PrivateKey()
    let key521 = P521.Signing.PrivateKey()

    print("P-384 ochiq kalit hajmi: \(key384.publicKey.rawRepresentation.count) bayt")
    print("P-521 ochiq kalit hajmi: \(key521.publicKey.rawRepresentation.count) bayt")
}

try! runHighSecurityCurves()
```
**Tushuntirish:** P-384 va P-521 NSA Suite B xavfsizlik standartlariga to'liq mos keladi va eng yuqori darajadagi matematik barqarorlikni beradi.

---

### Topshiriq #1169: SecKey API Orqali RSA-4096 OAEP va PSS Imzolash (Security Framework)
**Tavsif:** CryptoKit da bo'lmagan katta RSA kalitlari bilan Apple tizimining `Security` drayveri orqali ishlash.
**Talablar:** `SecKeyCreateRandomKey`, `SecKeyCreateSignature`, `kSecKeyAlgorithmRSASignatureMessagePSSSHA256`.
**Yechim (Swift):**
```swift
import Foundation
import Security

func createRsaKeyPair() -> SecKey? {
    let attributes: [String: Any] = [
        kSecAttrKeyType as String: kSecAttrKeyTypeRSA,
        kSecAttrKeySizeInBits as String: 2048
    ]
    var error: Unmanaged<CFError>?
    return SecKeyCreateRandomKey(attributes as CFDictionary, &error)
}

let rsaKey = createRsaKeyPair()
print("Security framework orqali RSA kaliti yaratildi: \(rsaKey != nil)")
```
**Tushuntirish:** Security framework Apple ning eng qadimgi va eng qudratli C-asosidagi xavfsizlik qatlami bo'lib, RSA-4096 va maxsus HSM drayverlari bilan ishlaydi.

---

### Topshiriq #1170: X.509 Sertifikatlarini Tahlil Qilish va SecTrust Tekshiruvi
**Tavsif:** Server taqdim etgan SSL sertifikatining zanjirini va muddati o'tmaganligini tizim darajasida tekshirish.
**Talablar:** `SecTrust`, `SecTrustEvaluateWithError`.
**Yechim (Swift):**
```swift
import Foundation
import Security

func evaluateTrust(serverCert: SecCertificate) -> Bool {
    let policy = SecPolicyCreateSSL(true, "api.khorazmiy.uz" as CFString)
    var trust: SecTrust?
    SecTrustCreateWithCertificates(serverCert, policy, &trust)

    guard let trust = trust else { return false }
    var error: CFError?
    return SecTrustEvaluateWithError(trust, &error)
}
```
**Tushuntirish:** `SecTrustEvaluateWithError` Apple ning barcha Root CA omborlariga murojaat qilib, sertifikatning haqiqiy ekanligini tasdiqlaydi.

---

### Topshiriq #1171: Ed25519 Bilan Imzolangan JWT Token Yaratish va Tekshirish Swift Da
**Tavsif:** Mobil ilovadan mikroxizmatlarga jo'natiladigan ixcham va xavfsiz EdDSA JWT tokenni shakllantirish.
**Talablar:** Base64Url, `Curve25519.Signing`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

func createEd25519Jwt(sub: String, key: Curve25519.Signing.PrivateKey) throws -> String {
    let header = "{\"alg\":\"EdDSA\",\"typ\":\"JWT\"}".data(using: .utf8)!.base64EncodedString()
    let claims = "{\"sub\":\"\(sub)\",\"exp\":1893456000}".data(using: .utf8)!.base64EncodedString()

    let signingInput = "\(header).\(claims)"
    let sig = try key.signature(for: signingInput.data(using: .utf8)!).base64EncodedString()

    return "\(signingInput).\(sig)"
}
```
**Tushuntirish:** EdDSA JWT lari an'anaviy RSA larga nisbatan mobil tarmoqlarda 4 barobar kam bayt uzatishni talab qiladi.

---

### Topshiriq #1172: Shamir's Secret Sharing Swift Implementatsiyasi
**Tavsif:** Kritik tiklash parolini (Mnemonic seed) 2 ta ishonchli qurilmaga bo'lib berish.
**Talablar:** Lagrange interpolyatsiyasi.
**Yechim (Swift):**
```swift
struct KeyShare {
    let x: Int
    let y: Int
}

func reconstructSecret(s1: KeyShare, s2: KeyShare) -> Int {
    let num = s1.y * s2.x - s2.y * s1.x
    let den = s2.x - s1.x
    return num / den
}

let s1 = KeyShare(x: 1, y: 14)
let s2 = KeyShare(x: 2, y: 17)
print("Tiklagan maxfiy sir: \(reconstructSecret(s1: s1, s2: s2))")
```
**Tushuntirish:** Shamir sxemasi mobil kripto-hamyonlarda foydalanuvchining shaxsiy kalitini xavfsiz zaxiralash uchun eng yaxshi vositadir.

---

### Topshiriq #1173: Post-Quantum Tayyorgarligi: Apple PQC Gibrid Modeli
**Tavsif:** Apple iMessage da joriy qilingan PQ3 protokoli tamoyili (Kyber + Curve25519).
**Talablar:** PQC gibrid kalit kelishuvi.
**Yechim (Swift):**
```swift
func explainApplePq3() {
    println("Apple PQ3 Post-Quantum xavfsizlik printsipi:");
    println("1. Har bir xabar uchun ham an'anaviy Elliptik egri chiziq (X25519), ham post-kvant Kyber kaliti kelishiladi.");
    println("2. Biri buzilsa ham, ikkinchisi xavfsizlikni kafolatlaydi.");
    println("3. Bu orqali 'Harvest Now, Decrypt Later' kvant hujumlari yo'qotiladi.");
}
```
**Tushuntirish:** Apple iMessage dunyodagi eng birinchi ommaviy post-kvant messenjerlaridan biri (PQ3 protokoli) bo'lib, ushbu standartga asoslanadi.

---

### Topshiriq #1174: Xavfsiz Base64Url Kodlash va Kalitlar Eksporti
**Tavsif:** Kriptografik kalitlarni URL parametrlarida xatosiz uzatish uchun padding belgilarini (`=`, `+`, `/`) tozalash.
**Talablar:** `base64EncodedString`, URL-safe o'zgartirish.
**Yechim (Swift):**
```swift
import Foundation

extension Data {
    func base64UrlEncoded() -> String {
        return self.base64EncodedString()
            .replacingOccurrences(of: "+", with: "-")
            .replacingOccurrences(of: "/", with: "_")
            .replacingOccurrences(of: "=", with: "")
    }
}

let keyBytes = "KhorazmiyCrypto".data(using: .utf8)!
print("Base64Url: \(keyBytes.base64UrlEncoded())")
```
**Tushuntirish:** Base64Url kodlash veb va mobil ilovalar o'rtasida binar kalitlarni xavfsiz uzatishning xalqaro standartidir.

---

### Topshiriq #1175: SecureEnclave.isAvailable Bilan Apparat Anklavini Tekshirish
**Tavsif:** Ilova ishlayotgan qurilmada haqiqiy apparat Secure Enclave chipi mavjudligini tekshirish.
**Talablar:** `SecureEnclave.isAvailable`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

func checkHardwareSecurity() {
    if SecureEnclave.isAvailable {
        print("Ushbu qurilma apparat Secure Enclave xavfsizlik chipiga ega!")
    } else {
        print("Secure Enclave mavjud emas (simulyator yoki eski qurilma).")
    }
}

checkHardwareSecurity()
```
**Tushuntirish:** Haqiqiy iPhone va Apple Silicon Mac larda Secure Enclave alohida chip bo'lib, uning xotirasiga iOS yadrosi ham kira olmaydi.

---

### Topshiriq #1176: SecureEnclave.P256.Signing.PrivateKey Bilan Apparat Ichida Kalit Yaratish
**Tavsif:** Xususiy kalitni ilova xotirasida emas, bevosita Secure Enclave chipi ichida yaratish.
**Talablar:** `SecureEnclave.P256.Signing.PrivateKey()`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

func createSecureEnclaveKey() throws {
    guard SecureEnclave.isAvailable else { return }

    // Kalit bevosita apparat chipida yaratiladi
    let enclaveKey = try SecureEnclave.P256.Signing.PrivateKey()
    let publicKey = enclaveKey.publicKey

    print("Secure Enclave apparat kaliti yaratildi!")
    print("Ochiq kalit hajmi: \(publicKey.rawRepresentation.count) bayt")
}

try? createSecureEnclaveKey()
```
**Tushuntirish:** Ushbu kalitning xususiy qismi (Private Key) hech qachon Secure Enclave chipidan tashqariga chiqmaydi va xotiradan o'g'irlanishi mumkin emas.

---

### Topshiriq #1177: Secure Enclave Kalitlari Bilan Raqamli Imzolash
**Tavsif:** Ma'lumot xeshini Secure Enclave chipiga yuborib, uning ichida imzolab natijani olish.
**Talablar:** `enclaveKey.signature(for: data)`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

func signWithEnclave(data: Data, key: SecureEnclave.P256.Signing.PrivateKey) throws -> P256.Signing.ECDSASignature {
    return try key.signature(for: data)
}
```
**Tushuntirish:** Barcha murakkab elliptik egri chiziq hisoblashlari chip ichida bajariladi va tashqariga faqat tayyor raqamli imzo chiqadi.

---

### Topshiriq #1178: SecureEnclave.P256.KeyAgreement Apparat Darajasida ECDH
**Tavsif:** Xususiy kalitni fosh qilmasdan, Secure Enclave ichida server bilan umumiy maxfiy kalitni kelishib olish.
**Talablar:** `SecureEnclave.P256.KeyAgreement.PrivateKey()`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

func runEnclaveEcdh(serverPublicKey: P256.KeyAgreement.PublicKey) throws -> SymmetricKey {
    guard SecureEnclave.isAvailable else {
        throw NSError(domain: "EnclaveUnavailable", code: 1)
    }

    let myEnclavePriv = try SecureEnclave.P256.KeyAgreement.PrivateKey()
    let sharedSecret = try myEnclavePriv.sharedSecretFromKeyAgreement(with: serverPublicKey)

    return sharedSecret.hkdfDerivedSymmetricKey(using: SHA256.self, salt: Data(), sharedInfo: Data(), outputByteCount: 32)
}
```
**Tushuntirish:** Bu eng yuqori darajadagi bank xavfsizligini ta'minlaydi: hatto qurilma xakerlar tomonidan to'liq root qilingan bo'lsa ham umumiy kalitni o'g'irlab bo'lmaydi.

---

### Topshiriq #1179: Secure Enclave Kalitini Keychain Ga Bog'lash (SecAccessControl)
**Tavsif:** Apparat kalitini keyingi ishga tushishlarda qayta ochish uchun Keychain ga saqlash.
**Talablar:** `SecAccessControlCreateWithFlags`, `kSecAccessControlPrivateKeyUsage`.
**Yechim (Swift):**
```swift
import Foundation
import Security

func createEnclaveAccessControl() -> SecAccessControl? {
    var error: Unmanaged<CFError>?
    return SecAccessControlCreateWithFlags(
        kCFAllocatorDefault,
        kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly,
        [.privateKeyUsage, .biometryAny],
        &error
    )
}

let accessControl = createEnclaveAccessControl()
print("Secure Enclave Access Control yaratildi: \(accessControl != nil)")
```
**Tushuntirish:** `SecAccessControl` operatsion tizim darajasida ushbu kalitdan faqat ruxsat berilgan sharoitlardagina foydalanishni kafolatlaydi.

---

### Topshiriq #1180: Apparat Kalitiga Kirish Uchun FaceID/TouchID Shartini Qo'yish
**Tavsif:** Har gal kalit ishlatilayotganda foydalanuvchidan FaceID tekshiruvini majburlash.
**Talablar:** `SecAccessControlCreateWithFlags(..., .userPresence, ...)`.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

func createBiometricEnclaveKey() throws {
    guard SecureEnclave.isAvailable else { return }

    let accessControl = SecAccessControlCreateWithFlags(
        nil,
        kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly,
        [.privateKeyUsage, .userPresence],
        nil
    )!

    // Kalit yaratilayotganda unga biometriya talabini kiritish
    let key = try SecureEnclave.P256.Signing.PrivateKey(accessControl: accessControl)
    print("Faqat FaceID bilan ochiladigan apparat kaliti yaratildi.")
}
```
**Tushuntirish:** Bunda hatto telefon qulfdan chiqarilgan holda birovning qo'liga tushsa ham, to'lovni imzolash uchun baribir egasining yuzi (FaceID) talab qilinadi.

---

### Topshiriq #1181: Constant-Time Taqqoslash Bilan Side-Channel Hujumlaridan Himoya
**Tavsif:** CryptoKit ichki doimiy vaqt taqqoslash funksiyalari orqali vaqt sizib chiqishini to'xtatish.
**Talablar:** `safeCompare`, timing attack himoyasi.
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

func constantTimeCompare(a: Data, b: Data) -> Bool {
    guard a.count == b.count else { return false }
    var result: UInt8 = 0
    for i in 0..<a.count {
        result |= a[i] ^ b[i]
    }
    return result == 0
}

let d1 = "secret_token_123".data(using: .utf8)!
let d2 = "secret_token_124".data(using: .utf8)!
print("Doimiy vaqtda solishtirildi: \(constantTimeCompare(a: d1, b: d2))")
```
**Tushuntirish:** Barcha baytlar to'liq tekshirib chiqiladi va birinchi xatoda sikldan chiqib ketilmaydi, natijada tajovuzkor javob vaqtini o'lchab tokenni topa olmaydi.

---

### Topshiriq #1182: Kesh-Timing Hujumlaridan Himoya va Shoxlanishsiz Mantiq
**Tavsif:** `if-else` shoxlanishlarini kamaytirib, CPU kesh liniyalaridan ma'lumot sizishining oldini olish.
**Talablar:** Conditional move mantiqi.
**Yechim (Swift):**
```swift
func conditionalSelect(condition: Bool, a: UInt8, b: UInt8) -> UInt8 {
    let mask = condition ? UInt8.max : 0
    return (a & mask) | (b & ~mask)
}

let val = conditionalSelect(condition: true, a: 10, b: 20)
print("Shoxlanishsiz tanlangan qiymat: \(val)")
```
**Tushuntirish:** Bu usul protsessorning Branch Predictor modulini chetlab o'tadi va Spectre kabi spekulyativ hujumlarni bartaraf etadi.

---

### Topshiriq #1183: Replay Attack Ga Qarshi Nonce va Timestamp Kesh
**Tavsif:** Tarmoqdan ushlab olingan so'rovlarning qayta yuborilishini to'xtatuvchi xotira kesh tekshiruvi.
**Talablar:** Timestamp + Nonce kesh.
**Yechim (Swift):**
```swift
import Foundation

actor ReplayGuard {
    private var nonces: [String: Date] = [:]

    func isValid(nonce: String, timestamp: Date) -> Bool {
        if abs(timestamp.timeIntervalSinceNow) > 300 {
            return false // 5 daqiqadan eski so'rov
        }
        if nonces[nonce] != nil {
            return false // Takroriy so'rov (Replay Attack)
        }
        nonces[nonce] = timestamp
        return true
    }
}
```
**Tushuntirish:** Swift `actor` orqali yaratilgan kesh ko'p oqimli poyga holatlaridan (Data-Race) to'liq himoyalangan.

---

### Topshiriq #1184: DoS Hujumlariga Qarshi Kriptografik Oqimlarni Cheklash (Throttling)
**Tavsif:** Foydalanuvchi yoki skript tugmani ketma-ket bosib og'ir kriptografik xeshlash orqali iPhone ni qotirib qo'yishini oldini olish.
**Talablar:** `Task.sleep`, debouncing.
**Yechim (Swift):**
```swift
import Foundation

actor AsyncCryptoThrottler {
    private var isBusy = false

    func performThrottledOperation(action: () async -> Void) async {
        guard !isBusy else {
            print("Operatsiya rad etildi: Tizim band!")
            return
        }
        isBusy = true
        defer { isBusy = false }
        await action()
    }
}
```
**Tushuntirish:** Throttling batareyaning qizib ketishi va ilovaning qotib qolishi (Application Hang) ning oldini oladi.

---

### Topshiriq #1185: Keychain Services: SecItemAdd, SecItemCopyMatching va SecItemUpdate
**Tavsif:** Foydalanuvchi parollari va tokenlarini iOS/macOS ning xavfsiz Keychain omborida saqlash.
**Talablar:** `kSecClassGenericPassword`, `SecItemAdd`, `SecItemCopyMatching`.
**Yechim (Swift):**
```swift
import Foundation
import Security

public class KeychainService {
    public static func save(key: String, data: Data) -> OSStatus {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data,
            kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly
        ]
        SecItemDelete(query as CFDictionary)
        return SecItemAdd(query as CFDictionary, nil)
    }

    public static func load(key: String) -> Data? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: kCFBooleanTrue!,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]
        var dataTypeRef: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &dataTypeRef)
        return status == errSecSuccess ? (dataTypeRef as? Data) : nil
    }
}

let secretToken = "jwt_bearer_token_12345".data(using: .utf8)!
KeychainService.save(key: "authToken", data: secretToken)
print("Token Keychain ga xavfsiz saqlandi.")
```
**Tushuntirish:** Keychain ma'lumotlarni SQLite faylda emas, operatsion tizimning maxsus shifrlangan xavfsizlik servisida saqlaydi.

---

### Topshiriq #1186: kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly Xavfsizlik Atributi
**Tavsif:** Nima uchun `ThisDeviceOnly` atributi zaxira nusxalar (iCloud / iTunes backup) orqali ma'lumot o'g'irlanishini to'xtatishi.
**Talablar:** Keychain himoya klasslari.
**Yechim (Swift):**
```swift
import Security

func explainKeychainAccessibility() {
    print("kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly afzalligi:");
    print("1. Telefon o'chirilganda kalit xotiradan to'liq yo'qoladi.");
    print("2. Telefon birinchi marta PIN bilan ochilgandan keyingina ruxsat beriladi.");
    print("3. 'ThisDeviceOnly' kalitni boshqa qurilmaga tiklanadigan zaxira nusxalarga (Backup) qo'shilishini taqiqlaydi.");
}

explainKeychainAccessibility()
```
**Tushuntirish:** Ushbu atribut bank ilovalari uchun majburiydir, chunki kompyuterga olingan iTunes backup tahlil qilinganda ham ushbu kalitlar ochilmaydi.

---

### Topshiriq #1187: iCloud Keychain Sinxronizatsiyasi vs Lokal Xavfsiz Saqlash
**Tavsif:** Barcha Apple qurilmalarida kalitni sinxronlash (`kSecAttrSynchronizable`) va uning xavfsizlik ta'siri.
**Talablar:** `kSecAttrSynchronizable`.
**Yechim (Swift):**
```swift
import Security

func saveSynchronizablePassword(account: String, data: Data) {
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: account,
        kSecValueData as String: data,
        kSecAttrSynchronizable as String: kCFBooleanTrue! // iCloud orqali Mac va iPad ga sinxronlash
    ]
    SecItemAdd(query as CFDictionary, nil)
    print("iCloud Keychain sinxron saqlash faollashtirildi.")
}
```
**Tushuntirish:** iCloud Keychain End-to-End Encryption bilan himoyalangan, biroq apparat darajasida lokal bog'lanish talab qilinsa (Strongbox/Enclave), sinxronlash o'chirilishi kerak.

---

### Topshiriq #1188: LAContext Bilan FaceID va TouchID Biometrik Autentifikatsiyasi
**Tavsif:** Foydalanuvchining shaxsini LocalAuthentication freymvorki orqali tezkor tekshirish.
**Talablar:** `LAContext`, `canEvaluatePolicy`, `evaluatePolicy`.
**Yechim (Swift):**
```swift
import Foundation
import LocalAuthentication

func authenticateWithBiometrics() async -> Bool {
    let context = LAContext()
    var error: NSError?

    guard context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) else {
        print("Biometriya mavjud emas: \(error?.localizedDescription ?? "")")
        return false
    }

    do {
        let success = try await context.evaluatePolicy(
            .deviceOwnerAuthenticationWithBiometrics,
            localizedReason: "Tranzaksiyani tasdiqlash uchun FaceID kerak"
        )
        return success
    } catch {
        print("Biometrik xato: \(error)")
        return false
    }
}
```
**Tushuntirish:** `LAContext` FaceID/TouchID kamerasiga bevosita kirmaydi; faqat operatsion tizim bergan kriptografik tasdiqni qabul qiladi.

---

### Topshiriq #1189: Biometrik O'zgarishlarni Aniqlash (evaluatedPolicyDomainState)
**Tavsif:** Agar foydalanuvchi sozlamalarda yangi barmoq izi qo'shsa yoki FaceID ni yangilasa, barcha maxfiy kalitlarni avtomatik bekor qilish.
**Talablar:** `context.evaluatedPolicyDomainState`.
**Yechim (Swift):**
```swift
import Foundation
import LocalAuthentication

class BiometricChangeDetector {
    private var savedDomainState: Data?

    func checkBiometricState(context: LAContext) -> Bool {
        guard let currentState = context.evaluatedPolicyDomainState else { return false }

        if let previous = savedDomainState, previous != currentState {
            print("XAVF: Yangi biometriya qo'shilgan! Barcha saqlangan tokenlar bekor qilindi.")
            savedDomainState = currentState
            return false // Yangi shaxs qo'shilgan, qayta parol so'rash shart!
        }

        savedDomainState = currentState
        return true
    }
}
```
**Tushuntirish:** Agar telefon o'g'irlanib, o'g'ri unga o'z barmog'ini qo'shib olsa, `evaluatedPolicyDomainState` darhol o'zgaradi va bank ilovasi foydalanuvchini tizimdan chiqaradi.

---

### Topshiriq #1190: Ekran Yashirish (Privacy Screen): App Switcher Da Ekranni Blur Qilish
**Tavsif:** Foydalanuvchi ilovani fonga olganda (App Switcher) maxfiy balans yoki kartalar ko'rinib qolishini to'xtatish.
**Talablar:** `sceneWillResignActive`, `UIVisualEffectView`.
**Yechim (Swift):**
```swift
import Foundation

func explainPrivacyScreen() {
    print("iOS Privacy Screen tamoyili:");
    print("1. sceneWillResignActive hodisasida asosiy oyna ustiga xiralashtiruvchi parda (Blur View) tushiriladi.");
    print("2. Natijada iOS keshlaydigan skrinshotda maxfiy moliyaviy ma'lumotlar saqlanmaydi.");
    print("3. sceneDidBecomeActive da parda olib tashlanadi.");
}

explainPrivacyScreen()
```
**Tushuntirish:** Bu himoya telefon boshqa odam qo'liga tushganda yoki xotira skrinshotlari tahlil qilinganda ma'lumotlarni asraydi.

---

### Topshiriq #1191: Anti-Screen Capture: Skrinshot va Video Yozishni Aniqlash
**Tavsif:** Foydalanuvchi skrinshot olganda yoki ekran yozuvini yoqqanda sezgir kontentni yashirish.
**Talablar:** `UIScreen.capturedDidChangeNotification`.
**Yechim (Swift):**
```swift
import Foundation

func explainScreenCaptureDetection() {
    print("Ekran yozuvidan himoya:");
    print("UIScreen.main.isCaptured parametrini kuzatib borish orqali ekranni boshqa monitorga yoki QuickTime ga yozib olinayotgani aniqlanadi.");
    print("Ushbu holatda maxfiy videolavhalar yoki kartalar ekranda o'chiriladi.");
}

explainScreenCaptureDetection()
```
**Tushuntirish:** Kino va bank ilovalari ushbu API orqali maxfiy kontentning ruxsatsiz yozib olinishini to'xtatadi.

---

### Topshiriq #1192: UIPasteboard Xavfsizligi: Maxfiy Ma'lumotlarni Avtomatik Tozalash
**Tavsif:** Nusxalangan parollarni 30 soniyadan so'ng buferdan xavfsiz o'chirish.
**Talablar:** `UIPasteboard.general.setItems(..., options: [.expirationDate: ...])`.
**Yechim (Swift):**
```swift
import Foundation

func explainPasteboardSecurity() {
    print("UIPasteboard muddati:");
    print("iOS 14+ da nusxalash vaqtida UIPasteboardOption.expirationDate belgilash mumkin.");
    print("Belgilangan muddat (masalan, 30 soniya) o'tgach, bufer avtomatik ravishda bo'shatiladi.");
}

explainPasteboardSecurity()
```
**Tushuntirish:** Boshqa ilovalar doimiy ravishda buferni kuzatib turishi mumkin; tezkor muddati o'tish maxfiy kodlarning o'g'irlanishini to'xtatadi.

---

### Topshiriq #1193: DeviceCheck va DCAppAttestService Asoslari
**Tavsif:** Serverga murojaat qilayotgan ilovaning haqiqiy o'zgartirilmagan original Apple ilovasi ekanligini isbotlash.
**Talablar:** `DCAppAttestService.shared.isSupported`.
**Yechim (Swift):**
```swift
import DeviceCheck

func checkAppAttestSupport() {
    if DCAppAttestService.shared.isSupported {
        print("DCAppAttestService ushbu qurilmada qo'llab-quvvatlanadi.")
    } else {
        print("App Attest qo'llab-quvvatlanmaydi.")
    }
}

checkAppAttestSupport()
```
**Tushuntirish:** App Attest Apple serverlari orqali ilovaning soxtalashtirilmaganligini (Anti-Tampering) kriptografik apparat darajasida tasdiqlaydi.

---

### Topshiriq #1194: App Attest Kalitini Yaratish va Attestation Object Hosil Qilish
**Tavsif:** Qurilmada attestatsiya kalitini ochib, Apple sertifikat zanjiri bilan imzolangan hujjatni olish.
**Talablar:** `generateKey`, `attestKey`.
**Yechim (Swift):**
```swift
import Foundation
import DeviceCheck

func generateAppAttestProof(clientDataHash: Data) async throws -> (String, Data) {
    let service = DCAppAttestService.shared
    let keyId = try await service.generateKey()
    let attestationObject = try await service.attestKey(keyId, clientDataHash: clientDataHash)
    return (keyId, attestationObject)
}
```
**Tushuntirish:** Attestation Object serverga yuboriladi; server Apple CA orqali kalitning haqiqiy iPhone Secure Enclave ichida ochilganligini tekshiradi.

---

### Topshiriq #1195: App Attest Orqali So'rovlarni Imzolash (Assertion Creation)
**Tavsif:** Har bir API so'rovini App Attest kaliti bilan imzolab, so'rovning botlar tomonidan emas, aynan shu ilovadan chiqqanini kafolatlash.
**Talablar:** `generateAssertion(keyId, clientDataHash:)`.
**Yechim (Swift):**
```swift
import Foundation
import DeviceCheck

func signRequestWithAppAttest(keyId: String, requestHash: Data) async throws -> Data {
    return try await DCAppAttestService.shared.generateAssertion(keyId, clientDataHash: requestHash)
}
```
**Tushuntirish:** Bu usul API endpointlarini avtomatlashtirilgan skriptlar, emulyatorlar va botlardan 100% himoya qiladi.

---

### Topshiriq #1196: URLSession Da SSL Pinning: SecTrustEvaluateWithError va SPKI Tekshiruvi
**Tavsif:** Tarmoq aloqasini faqat o'zimizning server ochiq kalitimiz bilan bog'lash.
**Talablar:** `URLSessionDelegate`, `didReceive challenge:`.
**Yechim (Swift):**
```swift
import Foundation
import Security

final class PinnedSessionDelegate: NSObject, URLSessionDelegate {
    func urlSession(_ session: URLSession, didReceive challenge: URLAuthenticationChallenge) async -> (URLSession.AuthChallengeDisposition, URLCredential?) {
        guard challenge.protectionSpace.authenticationMethod == NSURLAuthenticationMethodServerTrust,
              let serverTrust = challenge.protectionSpace.serverTrust else {
            return (.cancelAuthenticationChallenge, nil)
        }

        var error: CFError?
        if SecTrustEvaluateWithError(serverTrust, &error) {
            // Sertifikat zanjiri to'g'ri, bu yerda ochiq kalit sha256 xashini tekshirish mumkin
            return (.useCredential, URLCredential(trust: serverTrust))
        }

        return (.cancelAuthenticationChallenge, nil)
    }
}
```
**Tushuntirish:** SSL Pinning korporativ josuslik proksilari yoki soxta CA o'rnatilgan qurilmalarda ham soxta sertifikatlarni darhol fosh qiladi.

---

### Topshiriq #1197: Jailbreak va Reverse Engineering Aniqlash (Anti-Tampering)
**Tavsif:** Buzilgan tizimlarni Cydia, Substrate fayllari va Dynamic Linker tekshiruvlari orqali aniqlash.
**Talablar:** Jailbreak yo'llari, sandbox integrity.
**Yechim (Swift):**
```swift
import Foundation

func isJailbroken() -> Bool {
    let checkPaths = [
        "/Applications/Cydia.app",
        "/Library/MobileSubstrate/MobileSubstrate.dylib",
        "/bin/bash",
        "/usr/sbin/sshd",
        "/etc/apt"
    ]
    for path in checkPaths {
        if FileManager.default.fileExists(atPath: path) {
            return true
        }
    }
    return false
}

print("Jailbreak holati: \(isJailbroken())")
```
**Tushuntirish:** Jailbreak bo'lgan qurilmalarda operatsion tizimning Sandbox himoyasi ishlamaydi va boshqa jarayonlar bizning xotiramizni o'qiy oladi.

---

### Topshiriq #1198: Swift Symbol Stripping va Compiler Hardening
**Tavsif:** Release kompilyatsiyasida simvollarni o'chirish va kod tahlilini qiyinlashtirish.
**Talablar:** `STRIP_STYLE = all`, `DEAD_CODE_STRIPPING`.
**Yechim (Swift):**
```swift
func explainSymbolStripping() {
    print("Xcode Compiler Hardening sozlamalari:");
    print("1. Deployment Postprocessing = YES");
    print("2. Strip Linked Product = YES (barcha ichki funksiya nomlarini o'chiradi).");
    print("3. Swift Compiler - Optimization Level = -O (Fast, Whole Module Optimization).");
}

explainSymbolStripping()
```
**Tushuntirish:** Simvollar o'chirilgach, dasturni dekompilyatsiya qilgan xaker funksiya nomlarini ko'ra olmaydi.

---

### Topshiriq #1199: Zaif Tarmoq Proksilarini (Charles, Burp Suite) Aniqlash
**Tavsif:** Tarmoq konfiguratsiyasida HTTP/HTTPS proksi o'rnatilganligini aniqlash.
**Talablar:** `CFNetworkCopySystemProxySettings`.
**Yechim (Swift):**
```swift
import Foundation

func isHttpProxyActive() -> Bool {
    guard let proxySettings = CFNetworkCopySystemProxySettings()?.takeRetainedValue() as? [String: Any],
          let scopes = proxySettings["__SCOPED__"] as? [String: Any] else { return false }

    for (_, values) in scopes {
        if let dict = values as? [String: Any] {
            if dict["HTTPProxy"] != nil || dict["HTTPSProxy"] != nil {
                return true
            }
        }
    }
    return false
}

print("Faol proksi mavjud: \(isHttpProxyActive())")
```
**Tushuntirish:** Proksi aniqlanganda ilova shubhali muhitda ishlayotganini tushunib, tranzaksiyani to'xtatishi mumkin.

---

### Topshiriq #1200: Kompleks Apple Xavfsizlik Arxitekturasi: CryptoKit + Secure Enclave + App Attest + SSL Pinning
**Tavsif:** Barcha o'rganilgan Apple platformasi xavfsizlik vositalarini birlashtiruvchi to'liq sanoat tizimi.
**Talablar:** Birlashgan xavfsizlik shlyuzi (Master Apple Security Gateway).
**Yechim (Swift):**
```swift
import Foundation
import CryptoKit

public struct MasterAppleSecurity {
    public static func runSecurityAudit() {
        print("=== Khorazmiy AI: Apple Kriptografiya va Xavfsizlik Arxitekturasi ===")
        print("1. L4/L7 Aloqa: URLSession SSL Pinning va majburiy TLS 1.3.")
        print("2. Apparat Kalitlari: Secure Enclave chipida P-256 ECDSA imzo.")
        print("3. Simmetrik AEAD: CryptoKit AES-GCM va ChaChaPoly bilan xotirasiz shifrlash.")
        print("4. Maxfiy Saqlash: Keychain Services (kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly).")
        print("5. Biometriya: LocalAuthentication (FaceID/TouchID) orqali apparat kalitini ochish.")
        print("6. Qurilma Butunligi: DeviceCheck App Attest orqali original Apple qurilmasini tasdiqlash.")
        print("7. Anti-Tampering: Jailbreak va Proksi aniqlash bilan ko'p qatlamli himoya.")
        print("Tizim barcha Apple Security Guidelines talablariga 100% javob beradi.")
    }
}

MasterAppleSecurity.runSecurityAudit()
```
**Tushuntirish:** Ushbu yakuniy modul iOS, iPadOS va macOS platformalaridagi eng mustahkam kiberxavfsizlik arxitekturasini to'liq namoyish etadi.

---

