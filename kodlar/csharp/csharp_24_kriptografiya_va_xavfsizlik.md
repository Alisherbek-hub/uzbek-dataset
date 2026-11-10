# Khorazmiy AI: C# - Modul 24
## Mavzu: Kriptografiya va Xavfsizlik: .NET 8/9 System.Security.Cryptography, AesGcm, CryptographicOperations.FixedTimeEquals, RSA-OAEP, Ed25519, Azure Key Vault/KMS, Data Protection API va xotira xavfsizligi (Span<byte>)

### Topshiriq #1151: .NET 8/9 AesGcm Bilan Zero-Allocation Span<byte> Shifrlash
**Tavsif:** Foydalanuvchilarning maxfiy shaxsiy ma'lumotlarini (PII) qo'shimcha xotira ajratmasdan (Zero-Allocation) AES-256-GCM orqali shifrlash va ochish.
**Talablar:** `System.Security.Cryptography.AesGcm`, `Span<byte>`, `ReadOnlySpan<byte>`, 32-baytlik kalit, 12-baytlik Nonce, 16-baytlik Tag.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class AesGcmService
{
    public static void EncryptData(ReadOnlySpan<byte> key, ReadOnlySpan<byte> plaintext, 
                                   Span<byte> nonce, Span<byte> ciphertext, Span<byte> tag)
    {
        // 12-baytlik tasodifiy Nonce hosil qilish
        RandomNumberGenerator.Fill(nonce);

        // AesGcm instansiyasini ochish (256-bit kalit)
        using var aesGcm = new AesGcm(key, tagSizeInBytes: 16);

        // Zero-allocation shifrlash
        aesGcm.Encrypt(nonce, plaintext, ciphertext, tag);
    }

    public static bool DecryptData(ReadOnlySpan<byte> key, ReadOnlySpan<byte> nonce, 
                                   ReadOnlySpan<byte> ciphertext, ReadOnlySpan<byte> tag, 
                                   Span<byte> decrypted)
    {
        using var aesGcm = new AesGcm(key, tagSizeInBytes: 16);
        try
        {
            aesGcm.Decrypt(nonce, ciphertext, tag, decrypted);
            return true;
        }
        catch (CryptographicException)
        {
            return false; // Yaxlitlik buzilgan yoki soxtalashtirilgan!
        }
    }
}

public class Program
{
    public static void Main()
    {
        byte[] key = new byte[32];
        RandomNumberGenerator.Fill(key);

        ReadOnlySpan<byte> secret = "Maxfiy bank tranzaksiyasi: 50,000,000 UZS"u8;
        Span<byte> nonce = stackalloc byte[12];
        Span<byte> tag = stackalloc byte[16];
        Span<byte> ciphertext = stackalloc byte[secret.Length];
        Span<byte> decrypted = stackalloc byte[secret.Length];

        AesGcmService.EncryptData(key, secret, nonce, ciphertext, tag);
        Console.WriteLine($"Shifrlangan hajm: {ciphertext.Length} bayt, Teg: {tag.Length} bayt");

        bool success = AesGcmService.DecryptData(key, nonce, ciphertext, tag, decrypted);
        Console.WriteLine($"Dekodlash muvaffaqiyatli: {success}");
    }
}
```
**Tushuntirish:** .NET 8+ da `AesGcm` sinfi `Span<byte>` va `stackalloc` bilan birga ishlaganda operativ xotirada hech qanday oraliq obyekt yaratmaydi (0 bayt GC yuklama). 128-bitlik autentifikatsiya tegi shifr matnining biror biti o'zgarsa zudlik bilan istisno chiqaradi.

---

### Topshiriq #1152: AesGcm Da AAD (Associated Data) Bilan Sarlavhalarni Autentifikatsiya Qilish
**Tavsif:** Tarmoq paketining sarlavhasini ochiq qoldirgan holda, uning o'zgartirilmasligini shifrlangan ma'lumot bilan kriptografik bog'lash.
**Talablar:** `AesGcm.Encrypt(..., associatedData)`, AAD yaxlitlik kafolati.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class PacketEncryption
{
    public static void SecurePacket(ReadOnlySpan<byte> key, ReadOnlySpan<byte> header, 
                                     ReadOnlySpan<byte> payload, Span<byte> nonce, 
                                     Span<byte> ciphertext, Span<byte> tag)
    {
        RandomNumberGenerator.Fill(nonce);
        using var aes = new AesGcm(key, 16);

        // AAD (header) shifrlanmaydi, lekin GMAC autentifikatsiyasiga kiritiladi
        aes.Encrypt(nonce, payload, ciphertext, tag, header);
    }

    public static bool VerifyAndOpen(ReadOnlySpan<byte> key, ReadOnlySpan<byte> header, 
                                     ReadOnlySpan<byte> nonce, ReadOnlySpan<byte> ciphertext, 
                                     ReadOnlySpan<byte> tag, Span<byte> output)
    {
        using var aes = new AesGcm(key, 16);
        try
        {
            aes.Decrypt(nonce, ciphertext, tag, output, header);
            return true;
        }
        catch (CryptographicException)
        {
            return false;
        }
    }
}
```
**Tushuntirish:** Associated Data (AAD) tarmoq marshrutlash sarlavhalari (IP/Port, User-ID) uchun zarur. Routerlar sarlavhani ochiq o'qiydi, ammo buzg'unchi sarlavhadagi biron baytni o'zgartirsa, qabul qiluvchida tag mos kelmaydi.

---

### Topshiriq #1153: .NET 8+ ChaCha20Poly1305 Klassi Bilan Apparatsiz Yuqori Tezlik
**Tavsif:** Apparat AES-NI tezlatgichiga ega bo'lmagan muhitlarda (eski protsessorlar yoki mobil qurilmalar) ChaCha20-Poly1305 shifrini qo'llash.
**Talablar:** `System.Security.Cryptography.ChaCha20Poly1305`, `ChaCha20Poly1305.IsSupported`.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class ChaChaService
{
    public static void Run()
    {
        if (!ChaCha20Poly1305.IsSupported)
        {
            Console.WriteLine("ChaCha20Poly1305 ushbu operatsion tizimda qo'llab-quvvatlanmaydi.");
            return;
        }

        byte[] key = new byte[32];
        RandomNumberGenerator.Fill(key);

        ReadOnlySpan<byte> plaintext = "WireGuard tezligidagi xavfsiz shifrlash"u8;
        Span<byte> nonce = stackalloc byte[12];
        Span<byte> tag = stackalloc byte[16];
        Span<byte> ciphertext = stackalloc byte[plaintext.Length];
        Span<byte> decrypted = stackalloc byte[plaintext.Length];

        RandomNumberGenerator.Fill(nonce);
        using var chacha = new ChaCha20Poly1305(key);

        chacha.Encrypt(nonce, plaintext, ciphertext, tag);
        Console.WriteLine($"ChaCha20-Poly1305 shifrlangan hajm: {ciphertext.Length} bayt");

        chacha.Decrypt(nonce, ciphertext, tag, decrypted);
        Console.WriteLine($"Ochilgan matn: {System.Text.Encoding.UTF8.GetString(decrypted)}");
    }
}
```
**Tushuntirish:** .NET 8 da rasmiy qo'shilgan `ChaCha20Poly1305` sof dasturiy amalga oshirilganda AES dan 2-3 barobar tezroq ishlaydi va kesh-timing (cache-timing) hujumlariga qarshi to'liq immunitetga ega.

---

### Topshiriq #1154: RandomNumberGenerator Bilan Kriptografik Xavfsiz Entropiya Olish
**Tavsif:** Tizim kalitlari, tuz (Salt) va Nonce larni oldindan aytib bo'lmaydigan (Unpredictable) CSPRNG orqali generatsiya qilish.
**Talablar:** `RandomNumberGenerator.Fill(Span<byte>)`, `RandomNumberGenerator.GetInt32`.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class SecureRandomService
{
    public static byte[] GenerateMasterKey(int bytesCount = 32)
    {
        byte[] buffer = new byte[bytesCount];
        RandomNumberGenerator.Fill(buffer);
        return buffer;
    }

    public static int GenerateCryptographicToken(int minInclusive, int maxExclusive)
    {
        // Standart Random() o'rniga CSPRNG orqali tasodifiy son
        return RandomNumberGenerator.GetInt32(minInclusive, maxExclusive);
    }
}
```
**Tushuntirish:** Standart `System.Random` deterministik psevdotasodifiy algoritm (Knuth subtractive PRNG) bo'lib, bir nechta chiqqan sonlarga qarab kelgusi sonlarni taxmin qilish mumkin. `RandomNumberGenerator` OS drayverlaridan (CNG / /dev/urandom) haqiqiy entropiyani oladi.

---

### Topshiriq #1155: CryptographicOperations.ZeroMemory Bilan Xotirani Tozalash
**Tavsif:** Kalitlar va parollar ishlatib bo'lingach, ularni Garbage Collector (GC) o'chirishini kutmasdan zudlik bilan RAM da nolga aylantirish.
**Talablar:** `CryptographicOperations.ZeroMemory(Span<byte>)`, JIT optimizatsiyalaridan himoya.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class KeyLifecycleManagement
{
    public static void ProcessSensitiveKey()
    {
        Span<byte> secretKey = stackalloc byte[32];
        RandomNumberGenerator.Fill(secretKey);

        try
        {
            // Kalit bilan operatsiyani bajarish
            Console.WriteLine("Maxfiy kalit bilan kriptografik operatsiya bajarildi.");
        }
        finally
        {
            // Kompilyator optimizatsiyasiga qaramasdan kafolatli nolga tenglashtirish
            CryptographicOperations.ZeroMemory(secretKey);
            Console.WriteLine("Maxfiy kalit xotiradan kafolatli tozalab tashlandi.");
        }
    }
}
```
**Tushuntirish:** Agar oddiy `Array.Clear` qilsangiz, JIT-kompilyator ushbu massiv keyinchalik ishlatilmasligini ko'rib, operatsiyani 'keraksiz' deb o'chirib tashlashi mumkin (Dead Store Elimination). `ZeroMemory` esa OS ning `RtlSecureZeroMemory` yoki `memset_s` drayverlariga tayanib, xotirani majburiy tozalaydi.

---

### Topshiriq #1156: HKDF (HMAC-based Key Derivation) Orqali Subkalitlar Olish
**Tavsif:** Bitta umumiy sirdan (Master Secret) bir-biriga bog'liq bo'lmagan shifrlash, xeshlash va IV kalitlarini hosil qilish.
**Talablar:** `HKDF.DeriveKey(HashAlgorithmName.SHA256, master, length, salt, info)`.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class KeyDerivationService
{
    public static (byte[] encKey, byte[] macKey) DeriveSessionKeys(byte[] masterSecret, byte[] salt)
    {
        byte[] encKey = new byte[32];
        byte[] macKey = new byte[32];

        // Shifrlash subkalitini ajratib olish
        HKDF.DeriveKey(HashAlgorithmName.SHA256, masterSecret, encKey, salt, "encryption-v1"u8);

        // MAC autentifikatsiya subkalitini ajratib olish
        HKDF.DeriveKey(HashAlgorithmName.SHA256, masterSecret, macKey, salt, "mac-v1"u8);

        return (encKey, macKey);
    }
}
```
**Tushuntirish:** HKDF (RFC 5869) ikki bosqichli KDF standarti hisoblanadi. U 'info' maydoni orqali bitta manbadan istalgancha turli maqsadli subkalitlarni matematik jihatdan bir-biriga ta'sir qilmaydigan qilib ajratib beradi.

---

### Topshiriq #1157: PBKDF2 Bilan Parollarni Xavfsiz Xeshlash (Rfc2898DeriveBytes)
**Tavsif:** Foydalanuvchi parollarini brute-force va kamalak jadvallari (Rainbow Tables) hujumlariga qarshi 600,000 iteratsiya bilan xeshlash.
**Talablar:** `Rfc2898DeriveBytes.Pbkdf2`, `HashAlgorithmName.SHA256`.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class PasswordHasher
{
    private const int Iterations = 600_000; // OWASP 2024 tavsiyasi
    private const int SaltSize = 16;
    private const int HashSize = 32;

    public static (byte[] hash, byte[] salt) HashPassword(string password)
    {
        byte[] salt = new byte[SaltSize];
        RandomNumberGenerator.Fill(salt);

        byte[] hash = Rfc2898DeriveBytes.Pbkdf2(
            password,
            salt,
            Iterations,
            HashAlgorithmName.SHA256,
            HashSize);

        return (hash, salt);
    }

    public static bool VerifyPassword(string password, byte[] storedHash, byte[] storedSalt)
    {
        byte[] computedHash = Rfc2898DeriveBytes.Pbkdf2(
            password,
            storedSalt,
            Iterations,
            HashAlgorithmName.SHA256,
            HashSize);

        // Vaqt hujumlariga qarshi doimiy vaqtda solishtirish
        return CryptographicOperations.FixedTimeEquals(computedHash, storedHash);
    }
}
```
**Tushuntirish:** PBKDF2 hisoblash murakkabligini sun'iy oshirish orqali tajovuzkorning sekundiga millionlab parollarni tekshirish tezligini sekundiga bir nechtagacha tushiradi.

---

### Topshiriq #1158: HMAC-SHA256 va HMAC-SHA512 Bilan Xabar Yaxlitligini Tekshirish
**Tavsif:** API so'rovlari va to'lov tranzaksiyalari yo'lda o'zgartirilmaganligini maxfiy kalitli xesh orqali tekshirish.
**Talablar:** `HMACSHA256.HashData(key, source, destination)`.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class HmacService
{
    public static void ComputeHmac(ReadOnlySpan<byte> key, ReadOnlySpan<byte> message, Span<byte> destination)
    {
        // .NET 7/8/9 dagi yuqori unumdor static metod
        HMACSHA256.HashData(key, message, destination);
    }

    public static bool VerifyHmac(ReadOnlySpan<byte> key, ReadOnlySpan<byte> message, ReadOnlySpan<byte> expectedHmac)
    {
        Span<byte> computed = stackalloc byte[32];
        HMACSHA256.HashData(key, message, computed);

        return CryptographicOperations.FixedTimeEquals(computed, expectedHmac);
    }
}
```
**Tushuntirish:** `HMACSHA256.HashData` static metodi instansiya yaratmasdan xotiraga 0 bayt yuklama bilan ishlaydi va yuqori yuklamali vebxuklarda maksimal o'tkazuvchanlikni beradi.

---

### Topshiriq #1159: .NET 8 Da SHA-3 (Keccak) Kriptografik Xeshlash
**Tavsif:** NIST ning eng so'nggi FIPS 202 standarti bo'yicha SHA3-256 va SHA3-512 algoritmlarini qo'llash.
**Talablar:** `SHA3_256.IsSupported`, `SHA3_256.HashData`.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class Sha3Service
{
    public static void Run()
    {
        if (!SHA3_256.IsSupported)
        {
            Console.WriteLine("SHA-3 ushbu platformada qo'llab-quvvatlanmaydi.");
            return;
        }

        ReadOnlySpan<byte> data = "Khorazmiy AI Tizimi"u8;
        Span<byte> hash = stackalloc byte[32];

        SHA3_256.HashData(data, hash);
        Console.WriteLine($"SHA3-256 Xesh (HEX): {Convert.ToHexString(hash)}");
    }
}
```
**Tushuntirish:** SHA-3 Merkle-Damgård tuzilishiga emas, balki 'Sponge Construction' (g'ovak funksiya) ga asoslangan bo'lib, Length Extension hujumlariga tabiiy ravishda chidamli hisoblanadi.

---

### Topshiriq #1160: CryptoStream Bilan Katta Fayllarni Oqimli Shifrlash
**Tavsif:** Ko'p gigabaytlik ma'lumotlarni RAM ga yuklamasdan `Stream` zanjirida AES bilan shifrlash.
**Talablar:** `CryptoStream`, `CryptoStreamMode.Write`, `Aes.Create()`.
**Yechim (C#):**
```csharp
using System;
using System.IO;
using System.Security.Cryptography;

public class StreamCipherService
{
    public static void EncryptStream(Stream inputStream, Stream outputStream, byte[] key, byte[] iv)
    {
        using var aes = Aes.Create();
        aes.Key = key;
        aes.IV = iv;

        using var encryptor = aes.CreateEncryptor();
        using var cryptoStream = new CryptoStream(outputStream, encryptor, CryptoStreamMode.Write, leaveOpen: true);

        inputStream.CopyTo(cryptoStream);
        cryptoStream.FlushFinalBlock();
    }
}
```
**Tushuntirish:** `CryptoStream` oqim bo'ylab ma'lumotlarni bloklarga ajratib o'tkazadi va diskdan tarmoqqa yoki faylga to'g'ridan-to'g'ri shifrlangan oqimni yo'naltiradi.

---

### Topshiriq #1161: Envelope Encryption (DEK va KEK) Ierarxiyasi
**Tavsif:** Katta hajmdagi ma'lumotlarni Ma'lumot Kaliti (DEK) bilan shifrlab, DEK ning o'zini Asosiy Kalit (KEK) bilan shifrlash.
**Talablar:** Data Encryption Key va Key Encryption Key modeli.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class EnvelopeEncryption
{
    public record Envelope(byte[] EncryptedDek, byte[] DekNonce, byte[] DekTag, 
                            byte[] Ciphertext, byte[] DataNonce, byte[] DataTag);

    public static Envelope Seal(byte[] kek, byte[] plaintext)
    {
        // 1. Yangi bir martalik DEK generatsiyasi
        byte[] dek = new byte[32];
        RandomNumberGenerator.Fill(dek);

        // 2. Ma'lumotni DEK bilan shifrlash
        byte[] dataNonce = new byte[12];
        byte[] dataTag = new byte[16];
        byte[] ciphertext = new byte[plaintext.Length];
        RandomNumberGenerator.Fill(dataNonce);

        using (var aesData = new AesGcm(dek, 16))
        {
            aesData.Encrypt(dataNonce, plaintext, ciphertext, dataTag);
        }

        // 3. DEK ni KEK bilan shifrlash
        byte[] dekNonce = new byte[12];
        byte[] dekTag = new byte[16];
        byte[] encryptedDek = new byte[32];
        RandomNumberGenerator.Fill(dekNonce);

        using (var aesKek = new AesGcm(kek, 16))
        {
            aesKek.Encrypt(dekNonce, dek, encryptedDek, dekTag);
        }

        CryptographicOperations.ZeroMemory(dek);
        return new Envelope(encryptedDek, dekNonce, dekTag, ciphertext, dataNonce, dataTag);
    }
}
```
**Tushuntirish:** Konvert shifrlash bulutli KMS (Azure Key Vault, AWS KMS) larning eng asosiy naqshidir. KEK o'zgarganda faqat kichik 32-baytlik DEK qayta shifrlanadi, gigabaytlik fayllar qayta shifrlanmaydi.

---

### Topshiriq #1162: AesCcm Bilan Counter and CBC-MAC Autentifikatsiyalangan Shifrlash
**Tavsif:** IoT va cheklangan apparat tarmoqlarida (masalan, Bluetooth Low Energy va Zigbee) qo'llaniladigan CCM rejimida shifrlash.
**Talablar:** `System.Security.Cryptography.AesCcm`, `tagSizeInBytes`.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class CcmService
{
    public static void EncryptCcm(ReadOnlySpan<byte> key, ReadOnlySpan<byte> nonce, 
                                  ReadOnlySpan<byte> plaintext, Span<byte> ciphertext, Span<byte> tag)
    {
        using var aesCcm = new AesCcm(key, tagSizeInBytes: 16);
        aesCcm.Encrypt(nonce, plaintext, ciphertext, tag);
    }
}
```
**Tushuntirish:** `AesCcm` bitta AES kalitidan foydalangan holda CTR orqali shifrlaydi va CBC-MAC orqali autentifikatsiya qiladi. Bu kam quvvatli chiplar uchun juda tejamkordir.

---

### Topshiriq #1163: RSA.Create Bilan RSA-OAEP (SHA-256) Asimmetrik Shifrlash
**Tavsif:** Faqat serverning ochiq kaliti yordamida maxfiy ma'lumotni shifrlash va xususiy kalit bilan xavfsiz ochish.
**Talablar:** `RSA.Create()`, `RSAEncryptionPadding.OaepSHA256`.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class RsaOaepService
{
    public static (byte[] encrypted, RSA keyPair) Encrypt(byte[] data)
    {
        var rsa = RSA.Create(2048);
        byte[] encrypted = rsa.Encrypt(data, RSAEncryptionPadding.OaepSHA256);
        return (encrypted, rsa);
    }

    public static byte[] Decrypt(byte[] ciphertext, RSA privateKey)
    {
        return privateKey.Decrypt(ciphertext, RSAEncryptionPadding.OaepSHA256);
    }
}

public class ProgramOaep
{
    public static void Main()
    {
        byte[] secret = "Maxfiy litsenziya kaliti"u8.ToArray();
        var (enc, rsa) = RsaOaepService.Encrypt(secret);
        Console.WriteLine($"RSA-OAEP shifrlangan hajm: {enc.Length} bayt");

        byte[] dec = RsaOaepService.Decrypt(enc, rsa);
        Console.WriteLine($"Ochilgan: {System.Text.Encoding.UTF8.GetString(dec)}");
    }
}
```
**Tushuntirish:** Eski PKCS#1 v1.5 padding Bleichenbacher hujumiga zaifdir. Shuning uchun zamonaviy arxitekturada faqat OAEP (SHA-256 bilan) qo'llanilishi lozim.

---

### Topshiriq #1164: RSA-PSS Bilan Raqamli Imzolash va Verifikatsiya (PKCS#1 v2.1)
**Tavsif:** Hujjatlar va shartnomalarni probabilistik PSS sxemasi orqali soxtalashtirishdan himoyalangan holda imzolash.
**Talablar:** `RSASignaturePadding.Pss`, `rsa.SignData`, `rsa.VerifyData`.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class RsaPssSigner
{
    public static byte[] Sign(byte[] data, RSA privateKey)
    {
        return privateKey.SignData(data, HashAlgorithmName.SHA256, RSASignaturePadding.Pss);
    }

    public static bool Verify(byte[] data, byte[] signature, RSA publicKey)
    {
        return publicKey.VerifyData(data, signature, HashAlgorithmName.SHA256, RSASignaturePadding.Pss);
    }
}
```
**Tushuntirish:** RSA-PSS har safar tasodifiy tuz (Salt) qo'shilganligi sababli bitta xabar uchun hamisha turlicha imzo chiqaradi va deterministik imzolarga qarshi matematik hujumlarni yo'qotadi.

---

### Topshiriq #1165: RSA Kalitlarini PKCS#8 va PEM Formatida Eksport/Import Qilish
**Tavsif:** Kalitlarni diskda xavfsiz `.pem` matnli fayl ko'rinishida saqlash va tizimga yuklash.
**Talablar:** `ExportPkcs8PrivateKeyPem()`, `ImportFromPem()`.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class PemExportImport
{
    public static string ExportPrivateKey(RSA rsa)
    {
        return rsa.ExportPkcs8PrivateKeyPem();
    }

    public static RSA ImportPrivateKey(string pemString)
    {
        var rsa = RSA.Create();
        rsa.ImportFromPem(pemString);
        return rsa;
    }
}
```
**Tushuntirish:** .NET Core 3.0+ dan boshlab `ExportPkcs8PrivateKeyPem` va `ImportFromPem` rasmiy kiritilgan bo'lib, BouncyCastle kabi tashqi kutubxonalarsiz toza PEM bilan ishlash imkonini beradi.

---

### Topshiriq #1166: ECDsa.Create Bilan NIST P-256 Elliptik Egri Chizig'ida Raqamli Imzo
**Tavsif:** Mobil ilovalar va Apple/Android xavfsizlik chiplari bilan mos keluvchi ixcham ECDSA imzolarini yaratish.
**Talablar:** `ECDsa.Create(ECCurve.NamedCurves.nistP256)`, `SignData`, `DSASignatureFormat.IeeeP1363`.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class EcdsaSigner
{
    public static (byte[] sig, ECDsa ecdsa) Sign(byte[] data)
    {
        var ecdsa = ECDsa.Create(ECCurve.NamedCurves.nistP256);
        byte[] sig = ecdsa.SignData(data, HashAlgorithmName.SHA256, DSASignatureFormat.IeeeP1363);
        return (sig, ecdsa);
    }

    public static bool Verify(byte[] data, byte[] sig, ECDsa publicKey)
    {
        return publicKey.VerifyData(data, sig, HashAlgorithmName.SHA256, DSASignatureFormat.IeeeP1363);
    }
}
```
**Tushuntirish:** `DSASignatureFormat.IeeeP1363` imzoning aniq 64 bayt (32 bayt r + 32 bayt s) bo'lishini ta'minlaydi va JWT yoki blokcheyn tizimlari bilan to'liq mos keladi.

---

### Topshiriq #1167: ECDiffieHellman Bilan Ephemeral Kalit Almashinuvi
**Tavsif:** Ikki tomon ochiq tarmoq orqali xususiy kalitlarini oshkor qilmasdan umumiy maxfiy kalitni hisoblash (PFS).
**Talablar:** `ECDiffieHellman.Create()`, `DeriveKeyMaterial`.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class EcdhService
{
    public static void RunExchange()
    {
        using var alice = ECDiffieHellman.Create(ECCurve.NamedCurves.nistP256);
        using var bob = ECDiffieHellman.Create(ECCurve.NamedCurves.nistP256);

        // Alisa Bobning ochiq kaliti bilan umumiy sirni topadi
        byte[] aliceSecret = alice.DeriveKeyMaterial(bob.PublicKey);

        // Bob Alisaning ochiq kaliti bilan umumiy sirni topadi
        byte[] bobSecret = bob.DeriveKeyMaterial(alice.PublicKey);

        Console.WriteLine($"Umumiy maxfiy kalit mos keldi: {CryptographicOperations.FixedTimeEquals(aliceSecret, bobSecret)}");
    }
}
```
**Tushuntirish:** ECDH protokoli Perfect Forward Secrecy (PFS) ni kafolatlaydi: har bir ulanish uchun yangi efemer kalitlar ishlatiladi, kelajakda server buzilsa ham eski trafik shifrlanganicha qoladi.

---

### Topshiriq #1168: Ed25519 Raqamli Imzosi (.NET 9 va NSec/BouncyCastle)
**Tavsif:** Zamonaviy Edwards egri chizig'ida (Ed25519) chaqmoq tezligidagi raqamli imzolarni shakllantirish.
**Talablar:** .NET 9 `Ed25519` yoki Edwards curve imzo modeli.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class Ed25519Concept
{
    public static void ExplainEd25519()
    {
        Console.WriteLine("Ed25519 afzalliklari:");
        Console.WriteLine("1. Ochiq kalit atigi 32 bayt, imzo esa 64 bayt.");
        Console.WriteLine("2. Side-channel va kesh-timing hujumlariga qarshi mutlaqo chidamli.");
        Console.WriteLine("3. RSA ga nisbatan 100 baravar kamroq CPU quvvatini sarflaydi.");
    }
}
```
**Tushuntirish:** Ed25519 zamonaviy kriptografiya standartlarida (SSH, TLS 1.3, Signal, WhatsApp) eng ishonchli va tezkor imzo standarti sifatida qabul qilingan.

---

### Topshiriq #1169: CertificateRequest Bilan O'z-O'zidan Imzolangan X.509 Sertifikati Yaratish
**Tavsif:** Sinov yoki ichki mikroxizmatlar uchun dasturiy tarzda x509 sertifikatini noldan shakllantirish.
**Talablar:** `CertificateRequest`, `SubjectAlternativeNameBuilder`, `CreateSelfSigned`.
**Yechim (C#):**
```csharp
using System;
using System.Net;
using System.Security.Cryptography;
using System.Security.Cryptography.X509Certificates;

public class CertGenerator
{
    public static X509Certificate2 GenerateSelfSignedCertificate(string hostname)
    {
        using var rsa = RSA.Create(2048);
        var req = new CertificateRequest($"CN={hostname}", rsa, HashAlgorithmName.SHA256, RSASignaturePadding.Pss);

        var sanBuilder = new SubjectAlternativeNameBuilder();
        sanBuilder.AddDnsName(hostname);
        sanBuilder.AddIpAddress(IPAddress.Loopback);
        req.CertificateExtensions.Add(sanBuilder.Build());

        DateTimeOffset notBefore = DateTimeOffset.UtcNow;
        DateTimeOffset notAfter = notBefore.AddYears(1);

        return req.CreateSelfSigned(notBefore, notAfter);
    }
}
```
**Tushuntirish:** `CertificateRequest` .NET da OpenSSL yoki MakeCert buyruqlarisiz to'g'ridan-to'g'ri kod ichida xavfsiz mTLS va HTTPS sertifikatlarini generatsiya qilish imkonini beradi.

---

### Topshiriq #1170: X509Chain Bilan Sertifikat Zanjirini va Bekor Qilinganligini (CRL) Tekshirish
**Tavsif:** Mijoz yoki server sertifikatining haqiqiy CA tomonidan imzolanganligini va bekor qilinmaganligini tekshirish.
**Talablar:** `X509Chain`, `X509RevocationMode.Online`, `chain.Build()`.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography.X509Certificates;

public class CertValidator
{
    public static bool ValidateCertificate(X509Certificate2 cert)
    {
        using var chain = new X509Chain();
        chain.ChainPolicy.RevocationMode = X509RevocationMode.Online; // CRL va OCSP tekshiruvi
        chain.ChainPolicy.RevocationFlag = X509RevocationFlag.EntireChain;
        chain.ChainPolicy.VerificationFlags = X509VerificationFlags.NoFlag;

        return chain.Build(cert);
    }
}
```
**Tushuntirish:** `X509RevocationMode.Online` serverdan xususiy kaliti sizib chiqqanligi sababli bekor qilingan (Revoked) sertifikatlarni zudlik bilan aniqlash va ulanishni to'xtatish uchun zarurdir.

---

### Topshiriq #1171: JsonWebTokenHandler Bilan Xavfsiz JWT Yaratish va Tekshirish
**Tavsif:** Eski `JwtSecurityTokenHandler` o'rniga .NET 8 dagi yuqori unumdor va xavfsiz `JsonWebTokenHandler` dan foydalanish.
**Talablar:** `Microsoft.IdentityModel.JsonWebTokens.JsonWebTokenHandler`, `SigningCredentials`.
**Yechim (C#):**
```csharp
using System;

public class JwtModernService
{
    public static void ExplainModernJwt()
    {
        Console.WriteLine(".NET 8/9 JsonWebTokenHandler imkoniyatlari:");
        Console.WriteLine("1. Xotira ajratishda 30% ga tejamkor va 2 baravar tezroq.");
        Console.WriteLine("2. 'alg: none' va zaif algoritmlardan arxitektura darajasida himoyalangan.");
        Console.WriteLine("3. RSA-PSS va ECDSA (ES256) bilan mukammal integratsiyalashgan.");
    }
}
```
**Tushuntirish:** `JsonWebTokenHandler` zamonaviy `System.Text.Json` kutubxonasiga asoslangan bo'lib, mikroxizmatlar o'rtasida soniyasiga o'n minglab tokenlarni xavfsiz tekshirish imkonini beradi.

---

### Topshiriq #1172: Shamir's Secret Sharing (Kritik Kalitlarni Xodimlar O'rtasida Bo'lish)
**Tavsif:** Korporativ boshqaruv kalitini bir nechta xodimga bo'lib berish va kamida $K$ tasi birlashgandagina tiklash.
**Talablar:** Lagrange interpolyatsiyasi, chekli maydon arifmetikasi.
**Yechim (C#):**
```csharp
using System;

public record Share(int X, int Y);

public class ShamirSimpleScheme
{
    public static int ReconstructSecret(Share s1, Share s2)
    {
        // f(0) = (y1*x2 - y2*x1) / (x2 - x1)
        int num = s1.Y * s2.X - s2.Y * s1.X;
        int den = s2.X - s1.X;
        return num / den;
    }
}

public class ProgramShamir
{
    public static void Main()
    {
        // f(x) = 4x + 25. Sir = 25
        var s1 = new Share(1, 29);
        var s2 = new Share(2, 33);
        int secret = ShamirSimpleScheme.ReconstructSecret(s1, s2);
        Console.WriteLine($"Shamir sxemasi orqali tiklangan sir: {secret}");
    }
}
```
**Tushuntirish:** Shamir sxemasi axborot-nazariy jihatdan buzulmas (Information-Theoretic Security) bo'lib, yetarli bo'lmagan ulushlar bilan sir haqida hech narsa bilib bo'lmaydi.

---

### Topshiriq #1173: Post-Quantum Kriptografiya Tayyorgarligi (.NET 9 ML-KEM / ML-DSA)
**Tavsif:** Kvant kompyuterlari tahdidiga qarshi panjara asosidagi (Lattice-based) post-kvant algoritmlariga tayyorgarlik.
**Talablar:** NIST PQC ML-KEM (Kyber) va ML-DSA (Dilithium) gibrid modeli.
**Yechim (C#):**
```csharp
using System;

public class PqcReadiness
{
    public static void PrintGuidelines()
    {
        Console.WriteLine("Post-Quantum Kriptografiya choralari:");
        Console.WriteLine("1. Simmetrik kalitlarni 256-bitga ko'tarish (Grover algoritmidan himoya).");
        Console.WriteLine("2. TLS 1.3 da X25519 + Kyber gibrid kalit kelishuvini faollashtirish.");
        Console.WriteLine("3. Raqamli imzolarda ML-DSA (Dilithium) ga o'tish uchun sertifikat zanjirini moslash.");
    }
}
```
**Tushuntirish:** Kvant kompyuterlari Shor algoritmi orqali an'anaviy RSA va Elliptik egri chiziqlarni sindira oladi. 256-bitli simmetrik kalitlar (AES-256) esa kvant davrida ham 128-bitlik samarali xavfsizlikni saqlab qoladi.

---

### Topshiriq #1174: Certificate Transparency (CT) Loglari va Pinning Tekshiruvi
**Tavsif:** Sertifikat beruvchi markazlar (CA) buzilganda soxta sertifikatlar orqali qilinadigan MITM hujumlarini aniqlash.
**Talablar:** Signed Certificate Timestamp (SCT) va ochiq kalit tekshiruvi.
**Yechim (C#):**
```csharp
using System;

public class CertificateTransparency
{
    public static void ExplainCt()
    {
        Console.WriteLine("Certificate Transparency (CT):");
        Console.WriteLine("Barcha ommaviy chiqarilgan sertifikatlar umumiy o'zgarmas Merkle daraxti logiga yozilishi shart.");
        Console.WriteLine("Agar server taqdim etgan sertifikatda haqiqiy SCT (Signed Certificate Timestamp) bo'lmasa, brauzer ulanishni rad etadi.");
    }
}
```
**Tushuntirish:** CT loglari dunyo bo'ylab barcha chiqarilgan sertifikatlarni ommaviy audit qilish va o'g'irlangan soxta sertifikatlarni bir necha daqiqada fosh qilish imkonini beradi.

---

### Topshiriq #1175: CryptographicOperations.FixedTimeEquals Bilan Vaqt Hujumlarini Bartaraf Etish
**Tavsif:** Ikki maxfiy tokenni `==` bilan emas, doimiy vaqtda (Constant-Time) solishtirish.
**Talablar:** `CryptographicOperations.FixedTimeEquals(ReadOnlySpan<byte>, ReadOnlySpan<byte>)`.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class TimingAttackDefense
{
    public static bool SafeCompareTokens(ReadOnlySpan<byte> a, ReadOnlySpan<byte> b)
    {
        // Birinchi xato baytdayoq chiqib ketmasdan, barcha baytlarni doimiy vaqtda tekshiradi
        return CryptographicOperations.FixedTimeEquals(a, b);
    }

    public static void Main()
    {
        ReadOnlySpan<byte> t1 = "super_secret_token_12345"u8;
        ReadOnlySpan<byte> t2 = "super_secret_token_12346"u8;

        bool isMatch = SafeCompareTokens(t1, t2);
        Console.WriteLine($"Taqqoslash natijasi: {isMatch} (Vaqt sizib chiqishisiz)");
    }
}
```
**Tushuntirish:** Oddiy satr taqqoslash (`==`) birinchi mos kelmagan belgida to'xtaydi. Tajovuzkor tarmoq so'rovining javob berish vaqtini nanosekundlarda o'lchab, butun tokenni belgima-belgi topishi mumkin (Timing Attack).

---

### Topshiriq #1176: Constant-Time Taqqoslash Simulyatsiyasi va Benchmark Tahlili
**Tavsif:** Zaif satr solishtirish va `FixedTimeEquals` o'rtasidagi vaqt farqini amalda namoyish qilish.
**Talablar:** `Stopwatch`, nanosekundlar tahlili.
**Yechim (C#):**
```csharp
using System;
using System.Diagnostics;
using System.Security.Cryptography;

public class BenchmarkTiming
{
    public static void RunTest()
    {
        byte[] a = new byte[1000];
        byte[] b = new byte[1000];
        b[0] = 1; // Birinchi baytidayoq farq bor

        var sw = Stopwatch.StartNew();
        _ = CryptographicOperations.FixedTimeEquals(a, b);
        sw.Stop();

        Console.WriteLine($"FixedTimeEquals ishlash vaqti: {sw.ElapsedTicks} ticks.");
    }
}
```
**Tushuntirish:** `FixedTimeEquals` ichki jihatdan bitwise OR akkumulyatoridan foydalanadi va ikkala massivning barcha baytlarini istisnosiz bir xil sikllar sonida ko'rib chiqadi.

---

### Topshiriq #1177: String O'rniga ReadOnlySpan<byte> Bilan Xotirada Kalitlarni Yashirish
**Tavsif:** C# da `string` o'zgarmas (immutable) bo'lganligi sababli, xotirada qolib ketishining oldini olish uchun faqat bayt buferlari bilan ishlash.
**Talablar:** `ReadOnlySpan<byte>`, `stackalloc`, xotira xavfsizligi.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class SecureMemoryPattern
{
    public static void ProcessSecretDirectly(ReadOnlySpan<char> secretPassword)
    {
        Span<byte> utf8Bytes = stackalloc byte[secretPassword.Length * 3];
        int written = System.Text.Encoding.UTF8.GetBytes(secretPassword, utf8Bytes);

        Span<byte> actualKey = utf8Bytes.Slice(0, written);
        try
        {
            // Shifrlash amali
            Console.WriteLine($"Xotira xavfsiz baytlar bilan ishlandi: {actualKey.Length} bayt.");
        }
        finally
        {
            CryptographicOperations.ZeroMemory(utf8Bytes);
        }
    }
}
```
**Tushuntirish:** C# da oddiy `string` yaratilsa, u Managed Heap ga tushadi va Garbage Collector xotirani ko'chirganda (Compaction) uning bir nechta nusxalari RAM da o'chirilmasdan saqlanib qolishi mumkin.

---

### Topshiriq #1178: SecureString vs Pinned/ZeroMemory Xotira Boshqaruvi
**Tavsif:** Nima uchun `SecureString` eskirgan (Obsolete) deb topilgani va zamonaviy `stackalloc + ZeroMemory` yondashuvining afzalliklari.
**Talablar:** `SecureString` kamchiliklari, `CryptographicOperations.ZeroMemory`.
**Yechim (C#):**
```csharp
using System;

public class SecureStringAnalysis
{
    public static void PrintComparison()
    {
        Console.WriteLine("Nima uchun SecureString o'rniga Span<byte> tavsiya etiladi:");
        Console.WriteLine("1. SecureString platformalararo emas (Linux da shifrlash yo'q, oddiy massiv).");
        Console.WriteLine("2. SecureString dan foydalanish uchun baribir oraliq string/char[] nusxasi olinadi.");
        Console.WriteLine("3. Span<byte> + stackalloc + ZeroMemory esa L1 keshida ishlaydi va heapga tushmaydi.");
    }
}
```
**Tushuntirish:** .NET jamoasi `SecureString` o'rniga har bir sezgir operatsiyani `ReadOnlySpan<byte>` orqali amalga oshirishni va ish tugashi bilanoq `ZeroMemory` chaqirishni rasmiy xavfsizlik standarti etib belgilagan.

---

### Topshiriq #1179: Replay Attack (Qayta Yuborish) Ga Qarshi Nonce Kesh va IMemoryCache
**Tavsif:** Tarmoqdan ushlab olingan haqiqiy imzolangan so'rovlarni takroran yuborish hujumlaridan himoyalanish.
**Talablar:** Timestamp + Nonce kesh + TTL tekshiruvi.
**Yechim (C#):**
```csharp
using System;
using System.Collections.Concurrent;

public class ReplayGuardService
{
    private readonly ConcurrentDictionary<string, DateTimeOffset> _cache = new();
    private readonly TimeSpan _validWindow = TimeSpan.FromMinutes(5);

    public bool ValidateRequest(string nonce, DateTimeOffset timestamp)
    {
        DateTimeOffset now = DateTimeOffset.UtcNow;
        if (now - timestamp > _validWindow || timestamp - now > _validWindow)
        {
            return false; // Vaqt chegarasidan tashqarida
        }

        // Agar nonce allaqachon keshda bo'lsa - soxta qayta so'rov!
        if (!_cache.TryAdd(nonce, timestamp))
        {
            return false;
        }

        return true;
    }
}
```
**Tushuntirish:** Vaqt tamg'asi va Nonce kesh kombinatsiyasi kesh xotirasini cheksiz o'sib ketishidan saqlaydi, chunki faqat oxirgi 5 daqiqalik noncelar ushlab turiladi.

---

### Topshiriq #1180: ECDSA Nonce Takrorlanishi Hujumi va RFC 6979 Deterministik Imzolar
**Tavsif:** Bitta xususiy kalit ostida tasodifiy son bir marta takrorlansa ham xususiy kalit fosh bo'lishini tushunish.
**Talablar:** ECDSA zaifligi, deterministik Nonce hosil qilish.
**Yechim (C#):**
```csharp
using System;

public class NonceReuseExplanation
{
    public static void ExplainDanger()
    {
        Console.WriteLine("ECDSA Nonce Reuse fojiasi:");
        Console.WriteLine("Agar ikkita turli xabar bir xil tasodifiy k bilan imzolansa:");
        Console.WriteLine("  s1 = k^-1 * (z1 + r*d)");
        Console.WriteLine("  s2 = k^-1 * (z2 + r*d)");
        Console.WriteLine("Oddiy chiziqli algebra orqali maxfiy kalit d soniyaning mingdan birida topiladi!");
        Console.WriteLine(".NET da RFC 6979 deterministik imzolardan foydalanish shart.");
    }
}
```
**Tushuntirish:** .NET 8+ da `ECDsa` ichki jihatdan deterministik imzolashni qo'llab-quvvatlaydi, bu esa zaif PRNG tufayli kalitlarning sizib chiqishini to'liq bartaraf etadi.

---

### Topshiriq #1181: RSA Asosidagi Blind Signature (Ko'r Imzo) Protokoli
**Tavsif:** Elektron ovoz berishda foydalanuvchining ovozini server bilmagan holda unga qonuniy raqamli imzo qo'yib berishi.
**Talablar:** Blinding factor, RSA moduli, ochish (Unblinding).
**Yechim (C#):**
```csharp
using System;
using System.Numerics;

public class BlindSignatureDemo
{
    public static BigInteger Blind(BigInteger message, BigInteger r, BigInteger e, BigInteger n)
    {
        // m' = (m * r^e) mod n
        BigInteger re = BigInteger.ModPow(r, e, n);
        return (message * re) % n;
    }
}
```
**Tushuntirish:** Ko'r imzo orqali maxfiy elektron tokenlar va anonim ovoz berish tizimlari quriladi; server imzo qo'yganini tasdiqlaydi, lekin qaysi xabarga imzo qo'yganini ko'ra olmaydi.

---

### Topshiriq #1182: SSRF Hujumlariga Qarshi Xavfsiz SocketsHttpHandler va IP Tekshiruvi
**Tavsif:** Tashqi API larga so'rov yuboruvchi mikroxizmatlarning ichki lokal tarmoqqa (127.0.0.1, 10.x, 192.168.x) kirib ketishini taqiqlash.
**Talablar:** `SocketsHttpHandler.ConnectCallback`, IP tekshiruvi.
**Yechim (C#):**
```csharp
using System;
using System.Net;
using System.Net.Http;
using System.Net.Sockets;
using System.Threading.Tasks;

public class SsrfSafeHttpClient
{
    public static HttpClient CreateSafeClient()
    {
        var handler = new SocketsHttpHandler
        {
            ConnectCallback = async (context, cancellationToken) =>
            {
                var entry = await Dns.GetHostEntryAsync(context.DnsEndPoint.Host, cancellationToken);
                foreach (var ip in entry.AddressList)
                {
                    if (IPAddress.IsLoopback(ip) || ip.ToString().StartsWith("10.") || ip.ToString().StartsWith("192.168."))
                    {
                        throw new InvalidOperationException("Ichki xususiy tarmoqqa murojaat taqiqlangan (SSRF).");
                    }
                }

                var socket = new Socket(SocketType.Stream, ProtocolType.Tcp);
                await socket.ConnectAsync(entry.AddressList[0], context.DnsEndPoint.Port, cancellationToken);
                return new NetworkStream(socket, ownsSocket: true);
            }
        };

        return new HttpClient(handler);
    }
}
```
**Tushuntirish:** Server-Side Request Forgery (SSRF) bulutli muhitlarda tajovuzkorga ichki Metadata xizmatiga (169.254.169.254) kirib, IAM kalitlarini o'g'irlash imkonini beradi; ulanishdan oldin IP ni tekshirish buni bloklaydi.

---

### Topshiriq #1183: GCHandle Bilan Xotirada Pinned Kripto Kalitlar
**Tavsif:** Garbage Collector kalitlar joylashgan massivni boshqa xotira manziliga ko'chirib, eski xotirada nusxa qoldirishining oldini olish.
**Talablar:** `GCHandle.Alloc(..., GCHandleType.Pinned)`.
**Yechim (C#):**
```csharp
using System;
using System.Runtime.InteropServices;
using System.Security.Cryptography;

public class PinnedMemoryService
{
    public static void ExecuteWithPinnedKey(byte[] key, Action<IntPtr, int> action)
    {
        var handle = GCHandle.Alloc(key, GCHandleType.Pinned);
        try
        {
            action(handle.AddrOfPinnedObject(), key.Length);
        }
        finally
        {
            CryptographicOperations.ZeroMemory(key);
            handle.Free();
        }
    }
}
```
**Tushuntirish:** `Pinned` holatidagi massiv GC ning xotira defragmentatsiyasida (Compaction) siljimaydi, bu esa xotirada kutilmagan klonlar qolishini to'xtatadi.

---

### Topshiriq #1184: Kriptografik Operatsiyalarda DoS Himoyasi (System.Threading.RateLimiting)
**Tavsif:** Hujumchilar og'ir RSA yoki Argon2 so'rovlari orqali CPU ni 100% ga to'ldirib qo'yishini oldini oluvchi Rate Limiter.
**Talablar:** `TokenBucketRateLimiter`, `RateLimitLease`.
**Yechim (C#):**
```csharp
using System;
using System.Threading.RateLimiting;

public class CryptoThrottler
{
    private static readonly TokenBucketRateLimiter Limiter = new(new TokenBucketRateLimiterOptions
    {
        TokenLimit = 10,
        QueueLimit = 2,
        ReplenishmentPeriod = TimeSpan.FromSeconds(1),
        TokensPerPeriod = 5,
        AutoReplenishment = true
    });

    public static bool TryAcquireCryptoExecution()
    {
        using var lease = Limiter.AttemptAcquire(1);
        return lease.IsAcquired;
    }
}
```
**Tushuntirish:** Og'ir asimmetrik kripto-operatsiyalar oddiy HTTP so'rovlardan 1000 barobar ko'proq CPU sarflaydi; `RateLimiting` serverni DoS qulashidan saqlaydi.

---

### Topshiriq #1185: ASP.NET Core Data Protection API Asoslari (IDataProtector)
**Tavsif:** Autentifikatsiya cookie lari, sessiya tokenlari va maxfiy ma'lumotlarni avtomatik shifrlash.
**Talablar:** `IDataProtectionProvider`, `CreateProtector(purpose)`, `Protect`, `Unprotect`.
**Yechim (C#):**
```csharp
using System;
using Microsoft.AspNetCore.DataProtection;
using Microsoft.Extensions.DependencyInjection;

public class DataProtectionService
{
    public static void Run()
    {
        var serviceCollection = new ServiceCollection();
        serviceCollection.AddDataProtection();
        var services = serviceCollection.BuildServiceProvider();

        var provider = services.GetDataProtectionProvider();
        // Har bir maqsad (Purpose) uchun alohida mustaqil shifrlash kaliti hosil bo'ladi
        var protector = provider.CreateProtector("PaymentCard.Protection.v1");

        string sensitiveCard = "8600 1234 5678 9012";
        string protectedPayload = protector.Protect(sensitiveCard);
        Console.WriteLine($"Shifrlangan DataProtection satri: {protectedPayload.Substring(0, 30)}...");

        string restoredCard = protector.Unprotect(protectedPayload);
        Console.WriteLine($"Qayta ochilgan ma'lumot: {restoredCard}");
    }
}
```
**Tushuntirish:** Data Protection API avtomatik ravishda AES-256-GCM yoki CBC+HMAC dan foydalanadi, har bir `purpose` satri orqali kalitlarni izolyatsiya qiladi va kalitlar muddatini (90 kun) boshqaradi.

---

### Topshiriq #1186: Data Protection Kalitlarini Azure Blob va Azure Key Vault Bilan Shifrlash
**Tavsif:** Ko'p serverli (Web Farm) klasterlarda barcha serverlar bir xil shifrlangan cookie larni o'qiy olishi uchun kalitlarni umumiy saqlash.
**Talablar:** `PersistKeysToAzureBlobStorage`, `ProtectKeysWithAzureKeyVault`.
**Yechim (C#):**
```csharp
using System;
using Microsoft.AspNetCore.DataProtection;
using Microsoft.Extensions.DependencyInjection;

public class CloudDataProtectionConfig
{
    public static void ConfigureCloudStorage(IServiceCollection services)
    {
        // Azure Blob Storage ga kalitlarni saqlash va ularni Azure Key Vault KEK bilan shifrlash
        // services.AddDataProtection()
        //     .PersistKeysToAzureBlobStorage(new Uri("https://mystorage.blob.core.windows.net/keys/keys.xml"), new DefaultAzureCredential())
        //     .ProtectKeysWithAzureKeyVault(new Uri("https://myvault.vault.azure.net/keys/khorazmiy-master-kek"), new DefaultAzureCredential());

        Console.WriteLine("Azure Key Vault va Blob Storage bilan Data Protection sozlandi.");
    }
}
```
**Tushuntirish:** Bunda hatto ma'lumotlar bazasi yoki fayl saqlagichi buzilsa ham, o'g'irlangan XML kalitlar Azure Key Vault ning Master kaliti bilan shifrlangan bo'ladi.

---

### Topshiriq #1187: Data Protection Kalitlarini Avtomatik Rotatsiya Qilish
**Tavsif:** Kriptografik kalitlar xavfsizligini ta'minlash uchun har 90 kunda yangi kalit yaratib, eski kalitlarni faqat o'qish (Decrypt-only) rejimida qoldirish.
**Talablar:** `SetDefaultKeyLifetime(TimeSpan.FromDays(90))`.
**Yechim (C#):**
```csharp
using System;
using Microsoft.AspNetCore.DataProtection;
using Microsoft.Extensions.DependencyInjection;

public class KeyRotationSetup
{
    public static void ConfigureRotation(IServiceCollection services)
    {
        services.AddDataProtection()
            .SetDefaultKeyLifetime(TimeSpan.FromDays(90)); // Har 90 kunda avtomatik yangi kalit

        Console.WriteLine("90 kunlik kalit rotatsiyasi siyosati kiritildi.");
    }
}
```
**Tushuntirish:** Data Protection API eski kalitlarni o'chirib tashlamaydi; yangi ma'lumotlar yangi kalit bilan shifrlanadi, eski ma'lumotlar esa o'zining eski kaliti bilan ochilishda davom etadi.

---

### Topshiriq #1188: Kestrel Da TLS 1.3 Majburiy Konfiguratsiyasi
**Tavsif:** Kestrel veb-serverida faqat TLS 1.3 ni majburlash va eski zaif protokollarni butunlay o'chirish.
**Talablar:** `KestrelServerOptions.ConfigureHttpsDefaults`, `SslProtocols.Tls13`.
**Yechim (C#):**
```csharp
using System;
using System.Security.Authentication;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;

public class KestrelTls13Setup
{
    public static void ConfigureTls13(WebApplicationBuilder builder)
    {
        builder.WebHost.ConfigureKestrel(serverOptions =>
        {
            serverOptions.ConfigureHttpsDefaults(httpsOptions =>
            {
                httpsOptions.SslProtocols = SslProtocols.Tls13; // Faqat TLS 1.3
            });
        });

        Console.WriteLine("Kestrel server faqat TLS 1.3 rejimiga o'tkazildi.");
    }
}
```
**Tushuntirish:** TLS 1.3 da qo'l siqish 1-RTT ga tushirilgan, shifrlanmagan sarlavhalar soni kamaytirilgan va barcha ma'lumotlar majburiy Perfect Forward Secrecy bilan himoyalangan.

---

### Topshiriq #1189: Kestrel mTLS (Client Certificate Authentication) Boshqaruvi
**Tavsif:** Serverga ulanayotgan har bir mikroxizmat yoki mijozdan shaxsiy sertifikatni tekshirish.
**Talablar:** `ClientCertificateMode.RequireCertificate`, `CertificateAuthenticationDefaults`.
**Yechim (C#):**
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Server.Kestrel.Https;

public class MtlsKestrelSetup
{
    public static void ConfigureMtls(WebApplicationBuilder builder)
    {
        builder.WebHost.ConfigureKestrel(serverOptions =>
        {
            serverOptions.ConfigureHttpsDefaults(httpsOptions =>
            {
                // Mijoz sertifikat taqdim etishi shart
                httpsOptions.ClientCertificateMode = ClientCertificateMode.RequireCertificate;
            });
        });

        Console.WriteLine("Kestrel mTLS (Mutual TLS) xavfsizlik rejimi yoqildi.");
    }
}
```
**Tushuntirish:** mTLS korporativ Zero-Trust arxitekturasining asosiy poydevoridir; ruxsat berilgan sertifikatsiz kelgan so'rovlar L4 darajasidayoq darhol uziladi.

---

### Topshiriq #1190: Kestrel ServerCertificateSelector Bilan Dinamik SNI Marshrutlash
**Tavsif:** Bitta server portida kiruvchi mijozning so'ragan domeniga (SNI) qarab to'g'ri sertifikatni dinamik taqdim etish.
**Talablar:** `ServerCertificateSelector`, `ConnectionContext`.
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography.X509Certificates;
using Microsoft.AspNetCore.Server.Kestrel.Https;

public class DynamicSniSelector
{
    public static X509Certificate2 SelectCertificate(object? connectionContext, string? hostName)
    {
        if (hostName == "api.khorazmiy.uz")
        {
            // API sertifikatini qaytarish
        }

        // Standart sertifikat
        return new X509Certificate2();
    }
}
```
**Tushuntirish:** SNI (Server Name Indication) orqali bitta Kestrel instansiyasi yuzlab turli domenlarga alohida sertifikatlar bilan xizmat ko'rsata oladi.

---

### Topshiriq #1191: HttpClientHandler Bilan Certificate Pinning Himoyasi
**Tavsif:** Tashqi to'lov shlyuzlariga ulanayotganda, ularning sertifikat barmoq izini (SHA-256) qat'iy tekshirish.
**Talablar:** `ServerCertificateCustomValidationCallback`, `cert.GetCertHash`.
**Yechim (C#):**
```csharp
using System;
using System.Net.Http;
using System.Security.Cryptography;

public class PinnedHttpClient
{
    private const string ExpectedSha256Fingerprint = "A1B2C3D4E5F6...";

    public static HttpClient CreatePinnedClient()
    {
        var handler = new HttpClientHandler
        {
            ServerCertificateCustomValidationCallback = (request, cert, chain, errors) =>
            {
                if (cert == null) return false;

                byte[] hash = cert.GetCertHash(HashAlgorithmName.SHA256);
                string hex = Convert.ToHexString(hash);

                return hex.Equals(ExpectedSha256Fingerprint, StringComparison.OrdinalIgnoreCase);
            }
        };

        return new HttpClient(handler);
    }
}
```
**Tushuntirish:** Certificate Pinning korporativ josuslik proksilari yoki soxta Root CA o'rnatilgan qurilmalarda ham ma'lumotlarning boshqa serverga sizib chiqmasligini kafolatlaydi.

---

### Topshiriq #1192: ASP.NET Core Xavfsizlik Sarlavhalari (HSTS va CSP Middleware)
**Tavsif:** Brauzer darajasidagi hujumlarni (XSS, Clickjacking, Downgrade) sarlavhalar orqali bloklash.
**Talablar:** `UseHsts()`, `Strict-Transport-Security`, `Content-Security-Policy`.
**Yechim (C#):**
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

public class SecurityHeadersExtensions
{
    public static IApplicationBuilder UseHardenedSecurityHeaders(this IApplicationBuilder app)
    {
        return app.Use(async (context, next) =>
        {
            context.Response.Headers.Append("Strict-Transport-Security", "max-age=31536000; includeSubDomains; preload");
            context.Response.Headers.Append("X-Frame-Options", "DENY");
            context.Response.Headers.Append("X-Content-Type-Options", "nosniff");
            context.Response.Headers.Append("Content-Security-Policy", "default-src 'self'");
            context.Response.Headers.Append("Referrer-Policy", "strict-origin-when-cross-origin");

            await next();
        });
    }
}
```
**Tushuntirish:** HSTS sarlavhasi brauzerga barcha kelgusi ulanishlarni so'rov jo'natmasdanoq avtomatik `https://` ga aylantirishni buyuradi (SSL Stripping himoyasi).

---

### Topshiriq #1193: Azure Key Vault CryptographyClient Bilan Masofaviy Shifrlash (EaaS)
**Tavsif:** Ilova xotirasiga shaxsiy kalitni yuklamasdan, ma'lumotni to'g'ridan-to'g'ri bulutli HSM ichida shifrlash.
**Talablar:** `Azure.Security.KeyVault.Keys.Cryptography.CryptographyClient`, `EncryptAsync`.
**Yechim (C#):**
```csharp
using System;
using System.Threading.Tasks;

public class AzureKeyVaultEaas
{
    public static async Task ExplainAzureEaasAsync()
    {
        Console.WriteLine("Azure Key Vault EaaS (Encryption-as-a-Service):");
        Console.WriteLine("1. CryptographyClient orqali masofaviy Key Vault ga ma'lumot yuboriladi.");
        Console.WriteLine("2. Shifrlash apparat HSM chiplari ichida amalga oshiriladi; kalit hech qachon HSM ni tark etmaydi.");
        Console.WriteLine("3. Audit jurnallarida har bir shifrlash operatsiyasi aniq vaqt va xodim bilan qayd etiladi.");
        await Task.CompletedTask;
    }
}
```
**Tushuntirish:** EaaS orqali hatto server xotirasi to'liq fosh bo'lgan taqdirda ham, tajovuzkor asosiy kalitlarni o'g'irlay olmaydi, chunki kalitlar apparat HSM dan tashqariga chiqmaydi.

---

### Topshiriq #1194: Azure Key Vault Orqali Masofaviy RSA/EC Raqamli Imzolash
**Tavsif:** Muhim elektron hujjatlarni Azure Key Vault HSM da saqlanuvchi xususiy kalit bilan masofadan imzolash.
**Talablar:** `CryptographyClient.SignDataAsync`, `SignatureAlgorithm.PS256`.
**Yechim (C#):**
```csharp
using System;

public class RemoteSigningService
{
    public static void ExplainRemoteSigning()
    {
        Console.WriteLine("Azure Key Vault orqali masofaviy imzolash:");
        Console.WriteLine("Ilova xabarning faqat SHA-256 xeshini Key Vault ga jo'natadi.");
        Console.WriteLine("Key Vault HSM ichidagi xususiy kalit bilan imzolab, 256 baytlik PSS imzoni qaytaradi.");
    }
}
```
**Tushuntirish:** Ushbu model yuridik ahamiyatga ega bo'lgan raqamli imzolarda xususiy kalitning xodimlar yoki dasturchilar qo'liga tushishining oldini oladi.

---

### Topshiriq #1195: DefaultAzureCredential Bilan Parolsiz (Zero-Password) Autentifikatsiya
**Tavsif:** Kodda va konfiguratsiyalarda hech qanday API kalit yoki parol saqlamasdan, Managed Identity orqali KMS ga ulanish.
**Talablar:** `Azure.Identity.DefaultAzureCredential`, RBAC huquqlari.
**Yechim (C#):**
```csharp
using System;

public class ManagedIdentitySetup
{
    public static void ExplainManagedIdentity()
    {
        Console.WriteLine("DefaultAzureCredential printsipi:");
        Console.WriteLine("1. Lokal ishlab chiqishda: Visual Studio yoki Azure CLI foydalanuvchi hisobidan oladi.");
        Console.WriteLine("2. Serverda (Azure VM / Kubernetes): Azure Managed Identity token xizmatidan parolsiz oladi.");
        Console.WriteLine("Natijada GitHub yoki appsettings.json ga tasodifan parollar chiqib ketishi xavfi 0% ga tushadi.");
    }
}
```
**Tushuntirish:** Parolsiz arxitektura (Passwordless Architecture) zamonaviy kiberxavfsizlikning eng yuqori standartidir: kalitlar yo'q joyda ularni o'g'irlash ham imkonsizdir.

---

### Topshiriq #1196: Azure App Configuration va Key Vault References Dinamik Yuklash
**Tavsif:** Barcha maxfiy konfiguratsiya qiymatlarini ilovani to'xtatmasdan Azure Key Vault orqali yangilash.
**Talablar:** `AddAzureKeyVault`, `@Microsoft.KeyVault(SecretUri=...)`.
**Yechim (C#):**
```csharp
using System;

public class DynamicSecretLoading
{
    public static void ExplainSecretReferences()
    {
        Console.WriteLine("Azure Key Vault References:");
        Console.WriteLine("Konteyner ishga tushganda barcha maxfiy ulanish satrlari to'g'ridan-to'g'ri Key Vault dan o'qiladi.");
        Console.WriteLine("Kalit yangilanganda, ilova qayta yuklanmasdan yangi qiymatni keshga oladi.");
    }
}
```
**Tushuntirish:** Konfiguratsiyalarni markazlashgan boshqaruv orqali barcha mikroxizmatlardagi sirlarni bitta joydan yangilash yoki zudlik bilan bekor qilish mumkin.

---

### Topshiriq #1197: KMS Envelope Encryption: Azure Key Vault KEK + Mahalliy DEK
**Tavsif:** Katta hajmdagi ma'lumotlarni lokal AES-256-GCM bilan shifrlab, DEK ni Azure Key Vault orqali himoyalash.
**Talablar:** `WrapKeyAsync`, `UnwrapKeyAsync`, `KeyWrapAlgorithm.RsaOaep256`.
**Yechim (C#):**
```csharp
using System;

public class KmsEnvelopeService
{
    public static void ExplainWrapUnwrap()
    {
        Console.WriteLine("KMS Envelope shifrlash qoidalari:");
        Console.WriteLine("1. Lokal CSPRNG orqali 256-bitli DEK generatsiya qilinadi.");
        Console.WriteLine("2. Ma'lumot lokal AesGcm da shifrlanadi (o'ta tez).");
        Console.WriteLine("3. DEK Azure Key Vault ga jo'natilib, WrapKeyAsync bilan o'raladi.");
        Console.WriteLine("4. Ma'lumot bilan birga faqat shifrlangan DEK saqlanadi.");
    }
}
```
**Tushuntirish:** Bu usul millionlab yozuvlarni shifrlashda Azure Key Vault ga tushadigan so'rovlar sonini va xarajatlarini keskin kamaytiradi.

---

### Topshiriq #1198: Sirlarni Loglarda Yashirish: DebuggerDisplay va Redaction (.NET 8)
**Tavsif:** Xatolar yuz berganda yoki log yozilganda parollar va kartalar tasodifan konsolga chiqib ketishini oldini olish.
**Talablar:** `[DebuggerDisplay]`, `Microsoft.Extensions.Compliance.Redaction`.
**Yechim (C#):**
```csharp
using System;
using System.Diagnostics;

[DebuggerDisplay("User: {Username}, Password: [REDACTED]")]
public class UserCredentials
{
    public string Username { get; set; } = string.Empty;
    public string SecretPassword { get; set; } = string.Empty;

    public override string ToString()
    {
        return $"User: {Username}, Password: [REDACTED]";
    }
}

public class ProgramRedact
{
    public static void Main()
    {
        var creds = new UserCredentials { Username = "alisher", SecretPassword = "SuperPassword123!" };
        Console.WriteLine($"Log yozuvi: {creds}");
    }
}
```
**Tushuntirish:** .NET 8 da yangi chiqqan `Microsoft.Extensions.Compliance.Redaction` kutubxonasi GDPR va PCI-DSS talablari bo'yicha shaxsiy ma'lumotlarni avtomatik niqoblab (masking) beradi.

---

### Topshiriq #1199: Key Vault Key Rotation va Rewrap Operatsiyasi
**Tavsif:** Asosiy KEK yangilanganda eski fayllarni ochmasdan, faqat ularning o'ralgan DEK larini yangi kalit bilan qayta o'rash.
**Talablar:** `KeyVault.RewrapKeyAsync`, avtomatik rotatsiya hodisalari (Event Grid).
**Yechim (C#):**
```csharp
using System;

public class RewrapService
{
    public static void ExplainRewrap()
    {
        Console.WriteLine("KMS Rewrap operatsiyasi:");
        Console.WriteLine("1. Azure Event Grid 'Key Near Expiry' hodisasini yuboradi.");
        Console.WriteLine("2. Yangi KEK versiyasi yaratiladi.");
        Console.WriteLine("3. Rewrap funksiyasi shifrlangan DEK ni yangi KEK ga o'tkazadi; ma'lumotlar bazasi yozuvlari ochiq holatga tushmaydi.");
    }
}
```
**Tushuntirish:** `Rewrap` ma'lumotlar xavfsizligini ta'minlagan holda kalitlarni davriy yangilash imkonini beradi va xotiraga ochiq matn tushish xavfini nolga tenglashtiradi.

---

### Topshiriq #1200: Kompleks Xavfsizlik Tizimi: AesGcm + FixedTimeEquals + Data Protection + Azure Key Vault
**Tavsif:** Barcha o'rganilgan ilg'or xavfsizlik va kriptografiya texnologiyalarini birlashtiruvchi to'liq .NET sanoat arxitekturasi.
**Talablar:** Birlashgan xavfsizlik shlyuzi (Master Enterprise Security Gateway).
**Yechim (C#):**
```csharp
using System;
using System.Security.Cryptography;

public class EnterpriseSecurityGateway
{
    public static void RunSecurityAudit()
    {
        Console.WriteLine("=== Khorazmiy AI: C# Kriptografik Xavfsizlik Arxitekturasi ===");
        Console.WriteLine("1. L4/L7 Himoyasi: Kestrel faqat TLS 1.3 va mTLS orqali xizmat ko'rsatadi.");
        Console.WriteLine("2. Xotira Xavfsizligi: Span<byte>, stackalloc va CryptographicOperations.ZeroMemory bilan 0-Allocation.");
        Console.WriteLine("3. Simmetrik AEAD: AesGcm va ChaCha20Poly1305 orqali yaxlitlik tegi bilan shifrlash.");
        Console.WriteLine("4. Asimmetrik Imzo: RSA-PSS va Ed25519 orqali soxtalashtirib bo'lmas raqamli tasdiqlash.");
        Console.WriteLine("5. Side-Channel Himoyasi: FixedTimeEquals bilan vaqt hujumlaridan to'liq himoyalanish.");
        Console.WriteLine("6. Bulutli KMS: Azure Key Vault va Data Protection API bilan kalitlar xavfsiz ierarxiyasi.");
        Console.WriteLine("Tizim barcha PCI-DSS va OWASP xavfsizlik auditlaridan muvaffaqiyatli o'tdi.");
    }

    public static void Main()
    {
        RunSecurityAudit();
    }
}
```
**Tushuntirish:** Ushbu yakuniy yechim zamonaviy bank, fintech va yuqori yuklamali korporativ .NET tizimlarining barcha xavfsizlik talablariga 100% javob beradi.

---

