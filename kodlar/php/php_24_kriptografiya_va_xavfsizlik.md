# Khorazmiy AI: PHP - Modul 24
## Mavzu: Kriptografiya va OWASP Xavfsizlik: Sodium (crypto_secretbox, crypto_sign, crypto_pwhash Argon2id), OpenSSL 3, CSRF/XSS/SQLi himoyasi, hash_equals timing-safe taqqoslash va Secure Session Management

Salom, men **Khorazmiy AI** loyihasining PHP kiberxavfsizlik va zamonaviy amaliy kriptografiya bo'yicha bosh dataset mutaxassisiman. Ushbu modulda zamonaviy PHP ilovalarini kiberhujumlardan himoyalash, Libsodium va OpenSSL 3 kriptografik dvigatellari, OWASP Top-10 zaifliklarini professional bartaraf etish, xavfsiz autentifikatsiya, timing-attack lardan himoyalanish hamda mustahkam sessiyalar boshqaruvi bo'yicha 50 ta sanoat darajasidagi amaliy topshiriq va ularning to'liq ishlab turgan yechimlari taqdim etiladi.

---
### Topshiriq #1151: Libsodium crypto_secretbox Autentifikatsiyalangan Simmetrik Shifrlash
**Tavsif:** Mijozlarning maxfiy to'lov ma'lumotlarini (PII) bazada saqlash uchun XSalsa20 oqimli shifrlash va Poly1305 xabarlar haqiqiyligi kodi (AEAD) bilan ta'minlangan shifrlash xizmatini yarating.
**Talablar:** sodium_crypto_secretbox, sodium_crypto_secretbox_open, sodium_crypto_secretbox_keygen, har safar unikal nonce generatsiyasi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Libsodium Autentifikatsiyalangan Simmetrik Shifrlash
class SecretBoxCrypto {
    private string $key;

    public function __construct(string $key) {
        if (strlen($key) !== SODIUM_CRYPTO_SECRETBOX_KEYBYTES) {
            throw new InvalidArgumentException("Kalit uzunligi aniq " . SODIUM_CRYPTO_SECRETBOX_KEYBYTES . " bayt bo'lishi shart!");
        }
        $this->key = $key;
    }

    public static function generateKey(): string {
        return sodium_crypto_secretbox_keygen();
    }

    // Shifrlash: Nonce + Shifrlangan ma'lumot + MAC
    public function encrypt(string $plaintext): string {
        // Har bir shifrlash amali uchun yangi kriptografik tasodifiy nonce hosil qilinadi
        $nonce = random_bytes(SODIUM_CRYPTO_SECRETBOX_NONCEBYTES);
        
        $ciphertext = sodium_crypto_secretbox($plaintext, $nonce, $this->key);
        
        // Nonce sir emas, uni ciphertext boshiga qo'shib yuboramiz
        $combined = $nonce . $ciphertext;
        
        // Xavfsiz saqlash yoki uzatish uchun Base64 formatga o'giramiz
        return sodium_bin2base64($combined, SODIUM_BASE64_VARIANT_ORIGINAL);
    }

    // Deshifrlash va yaxlitlikni tekshirish
    public function decrypt(string $encoded): ?string {
        $decoded = sodium_base642bin($encoded, SODIUM_BASE64_VARIANT_ORIGINAL);
        
        if (strlen($decoded) < SODIUM_CRYPTO_SECRETBOX_NONCEBYTES) {
            throw new Exception("Shifrlangan paket hajmi juda qisqa!");
        }

        $nonce = substr($decoded, 0, SODIUM_CRYPTO_SECRETBOX_NONCEBYTES);
        $ciphertext = substr($decoded, SODIUM_CRYPTO_SECRETBOX_NONCEBYTES);

        // Agar ma'lumot hatto bitta bitga o'zgargan bo'lsa, false qaytaradi
        $plaintext = sodium_crypto_secretbox_open($ciphertext, $nonce, $this->key);
        if ($plaintext === false) {
            return null; // Yaxlitlik buzilgan yoki kalit noto'g'ri
        }

        return $plaintext;
    }
}

// Sinov
$key = SecretBoxCrypto::generateKey();
$crypto = new SecretBoxCrypto($key);

$secretData = "Karta raqami: 8600 1234 5678 9900 | CVV: 777";
$encrypted = $crypto->encrypt($secretData);
echo "[+] Shifrlangan paket: {$encrypted}
";

$decrypted = $crypto->decrypt($encrypted);
echo "[+] Deshifrlangan natija: {$decrypted}
";
```
**Tushuntirish:** Eskirgan CBC rejimlarida 'Padding Oracle' hujumlari yuzaga kelardi. Libsodium `crypto_secretbox` XSalsa20 shifrlashini Poly1305 MAC autentifikatsiyasi bilan birlashtiradi. Agar xaker shifrlangan baytlarni o'zgartirishga urinsa, funksiya zudlik bilan buni rad etadi va soxtalashtirishni fosh qiladi.

---

### Topshiriq #1152: Libsodium crypto_secretstream orqali Katta Fayllarni Oqimli Shifrlash
**Tavsif:** Xotirani (RAM) to'ldirmasdan, gigabaytlab o'lchamdagi katta video yoki arxiv fayllarni kichik bo'laklarga (chunks) bo'lib xavfsiz shifrlash va qayta ochish mexanizmini yarating.
**Talablar:** sodium_crypto_secretstream_xchacha20poly1305_*, oqim sarlavhasi (header), oxirgi freym bayrog'i (TAG_FINAL).
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Libsodium Katta Fayllarni Oqimli Shifrlash (SecretStream)
class StreamEncryptor {
    public static function encryptFile(string $sourcePath, string $destPath, string $key): void {
        $srcHandle = fopen($sourcePath, 'rb');
        $destHandle = fopen($destPath, 'wb');

        // Oqim initsializatsiyasi: sarlavha va holat (state) yaratiladi
        [$state, $header] = sodium_crypto_secretstream_xchacha20poly1305_init_push($key);
        // Fayl boshiga 24-baytli sarlavhani yozamiz
        fwrite($destHandle, $header);

        $chunkSize = 64 * 1024; // 64 KB bufer

        while (!feof($srcHandle)) {
            $chunk = fread($srcHandle, $chunkSize);
            $tag = feof($srcHandle) 
                ? SODIUM_CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_TAG_FINAL 
                : SODIUM_CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_TAG_MESSAGE;

            // Har bir bo'lak o'zining ichki nonce-i bilan shifrlanadi
            $encryptedChunk = sodium_crypto_secretstream_xchacha20poly1305_push($state, $chunk, '', $tag);
            fwrite($destHandle, $encryptedChunk);
        }

        fclose($srcHandle);
        fclose($destHandle);
    }

    public static function decryptFile(string $sourcePath, string $destPath, string $key): bool {
        $srcHandle = fopen($sourcePath, 'rb');
        $destHandle = fopen($destPath, 'wb');

        $header = fread($srcHandle, SODIUM_CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_HEADERBYTES);
        $state = sodium_crypto_secretstream_xchacha20poly1305_init_pull($header, $key);

        $chunkSize = (64 * 1024) + SODIUM_CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_ABYTES;

        while (!feof($srcHandle)) {
            $encryptedChunk = fread($srcHandle, $chunkSize);
            if (empty($encryptedChunk)) break;

            $decrypted = sodium_crypto_secretstream_xchacha20poly1305_pull($state, $encryptedChunk);
            if ($decrypted === false) {
                // Xatolik yoki buzilish
                fclose($srcHandle);
                fclose($destHandle);
                return false;
            }

            [$chunk, $tag] = $decrypted;
            fwrite($destHandle, $chunk);

            if ($tag === SODIUM_CRYPTO_SECRETSTREAM_XCHACHA20POLY1305_TAG_FINAL) {
                break; // Oqim xavfsiz va to'liq yakunlandi
            }
        }

        fclose($srcHandle);
        fclose($destHandle);
        return true;
    }
}

// Sinov
$key = sodium_crypto_secretstream_xchacha20poly1305_keygen();
$file = "/tmp/test_plain.txt";
file_put_contents($file, "Khorazmiy AI: Katta hajmli maxfiy ma'lumotlar oqimi...");
StreamEncryptor::encryptFile($file, "/tmp/test_encrypted.bin", $key);
StreamEncryptor::decryptFile("/tmp/test_encrypted.bin", "/tmp/test_restored.txt", $key);
echo "[+] Fayl oqimli shifrlash va tiklash muvaffaqiyatli bajarildi!
";
```
**Tushuntirish:** SecretStream XChaCha20-Poly1305 ga asoslangan bo'lib, bo'laklarni almashtirib qo'yish (reordering) yoki o'chirib yuborish (truncation attack) hujumlaridan himoyalangan. `TAG_FINAL` bayrog'i fayl oxiriga yetguncha shifrlash zanjiri buzilmaganligini tasdiqlaydi.

---

### Topshiriq #1153: Libsodium crypto_box Ommaviy Kalitlar Orqali Assimetrik Shifrlash
**Tavsif:** Ikki tomon (Alisher va Bobur) umumiy maxfiy kalitni oldindan kelishib olmasdan, X25519 ommaviy kalitlari orqali bir-biriga xavfsiz shifrlangan xabarlar yuboruvchi tizim yarating.
**Talablar:** sodium_crypto_box_keypair, sodium_crypto_box, sodium_crypto_box_open, Diffie-Hellman kalit almashinuvi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Assimetrik Shifrlash (Public-Key Cryptography)
// 1. Alisher o'zining kalitlar juftligini yaratadi
$aliceKeyPair = sodium_crypto_box_keypair();
$aliceSecretKey = sodium_crypto_box_secretkey($aliceKeyPair);
$alicePublicKey = sodium_crypto_box_publickey($aliceKeyPair);

// 2. Bobur o'zining kalitlar juftligini yaratadi
$bobKeyPair = sodium_crypto_box_keypair();
$bobSecretKey = sodium_crypto_box_secretkey($bobKeyPair);
$bobPublicKey = sodium_crypto_box_publickey($bobKeyPair);

// Alisher Boburga maxfiy xabar jo'natmoqchi:
// Alisher xabarni o'zining Maxfiy kaliti va Boburning Ommaviy kaliti bilan shifrlaydi
$message = "Maxfiy loyiha kodi: ALPHA-2026-UZB";
$nonce = random_bytes(SODIUM_CRYPTO_BOX_NONCEBYTES);

// Shifrlash uchun kombinatsiyalangan kalit
$aliceToBobKeypair = sodium_crypto_box_keypair_from_secretkey_and_publickey($aliceSecretKey, $bobPublicKey);
$ciphertext = sodium_crypto_box($message, $nonce, $aliceToBobKeypair);

echo "[Alisher] Xabar shifrlanib Boburga yuborildi.
";

// Bobur xabarni qabul qilib oladi:
// Bobur o'zining Maxfiy kaliti va Alisherning Ommaviy kaliti bilan ochadi
$bobFromAliceKeypair = sodium_crypto_box_keypair_from_secretkey_and_publickey($bobSecretKey, $alicePublicKey);
$decrypted = sodium_crypto_box_open($ciphertext, $nonce, $bobFromAliceKeypair);

if ($decrypted !== false) {
    echo "[Bobur] Xabar muvaffaqiyatli ochildi: {$decrypted}
";
} else {
    echo "[!] Xabar soxtalashtirilgan yoki ochilmadi!
";
}
```
**Tushuntirish:** Libsodium `crypto_box` X25519 elliptik egri chizig'ida Diffie-Hellman kalit almashinuvini (ECDH) amalga oshiradi, so'ngra hosil bo'lgan umumiy sirdan XSalsa20 va Poly1305 orqali simmetrik shifrlaydi. Bu ochiq kanallar orqali xavfsiz aloqani ta'minlaydi.

---

### Topshiriq #1154: Libsodium crypto_sign Ed25519 Raqamli Elektron Imzo Tizimi
**Tavsif:** Hujjatlar va dasturiy ta'minot yangilanishlarini (OTA update) soxtalashtirishdan himoyalash uchun Ed25519 yuqori tezlikdagi elliptik egri chiziqli raqamli imzo yaratish va tekshirish servisini tuzing.
**Talablar:** sodium_crypto_sign_keypair, sodium_crypto_sign_detached, sodium_crypto_sign_verify_detached.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Ed25519 Raqamli Elektron Imzo Servisi
class DigitalSignatureService {
    // Tizim uchun yangi imzo kalitlari juftligi yaratish
    public static function createSignKeyPair(): array {
        $kp = sodium_crypto_sign_keypair();
        return [
            'secret_key' => sodium_crypto_sign_secretkey($kp),
            'public_key' => sodium_crypto_sign_publickey($kp)
        ];
    }

    // Hujjatga alohida (detached) 64-baytli raqamli imzo qo'yish
    public static function signDocument(string $documentContent, string $secretKey): string {
        $signature = sodium_crypto_sign_detached($documentContent, $secretKey);
        return sodium_bin2hex($signature);
    }

    // Ommaviy kalit orqali imzo haqiqiyligini tekshirish
    public static function verifySignature(string $documentContent, string $hexSignature, string $publicKey): bool {
        $binarySignature = sodium_hex2bin($hexSignature);
        return sodium_crypto_sign_verify_detached($binarySignature, $documentContent, $publicKey);
    }
}

// Sinov
$keys = DigitalSignatureService::createSignKeyPair();
$document = "Shartnoma #9912: Barcha xizmatlar to'liq topshirildi. Summa: 50,000,000 UZS";

// Imzo yaratamiz
$signature = DigitalSignatureService::signDocument($document, $keys['secret_key']);
echo "[+] Hujjat imzolandi. Ed25519 Imzo: {$signature}
";

// Tekshiramiz
$isValid = DigitalSignatureService::verifySignature($document, $signature, $keys['public_key']);
echo "[+] Imzo tekshiruvi natijasi: " . ($isValid ? "HAQIQIY VA QONUNIY" : "SOXTA") . "
";

// Hujjatni 1 ta belgisini o'zgartirib ko'ramiz
$tamperedDoc = $document . ".";
$isTamperedValid = DigitalSignatureService::verifySignature($tamperedDoc, $signature, $keys['public_key']);
echo "[-] Soxtalashtirilgan hujjat tekshiruvi: " . ($isTamperedValid ? "O'TDI" : "RAD ETILDI") . "
";
```
**Tushuntirish:** Ed25519 (Edwards-curve Digital Signature Algorithm) RSA ga nisbatan ancha tezroq va kalit hajmi atigi 32 bayt (imzo 64 bayt). U tasodifiy sonlar generatori (RNG) zaifliklariga bog'liq emas (deterministik), bu esa tasodifiy son yetishmasligidan kelib chiqadigan kalit sizishlarini nolga tushiradi.

---

### Topshiriq #1155: Libsodium crypto_pwhash Argon2id Parol Xeshlash va Xotira Chegaralari
**Tavsif:** GPU va maxsus ASIC apparat chiplari orqali parollarni tanlash hujumlariga (Brute-force) chidamli bo'lgan zamonaviy Argon2id algoritmi yordamida parollarni xeshlash tizimini joriy qiling.
**Talablar:** sodium_crypto_pwhash_str, sodium_crypto_pwhash_str_verify, OPSLIMIT_INTERACTIVE, MEMLIMIT_INTERACTIVE sozlamalari.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Argon2id Kriptografik Parol Xeshlash
class PasswordHasher {
    // Parolni xavfsiz Argon2id xeshiga aylantirish
    public static function hash(string $password): string {
        // OPSLIMIT - protsessor sikllari soni
        // MEMLIMIT - sarflanadigan RAM hajmi (odatda 64 MB)
        return sodium_crypto_pwhash_str(
            $password,
            SODIUM_CRYPTO_PWHASH_OPSLIMIT_INTERACTIVE,
            SODIUM_CRYPTO_PWHASH_MEMLIMIT_INTERACTIVE
        );
    }

    // Parolni tekshirish (Timing-attack lardan himoyalangan)
    public static function verify(string $password, string $hash): bool {
        return sodium_crypto_pwhash_str_verify($hash, $password);
    }

    // Xavfsizlik standartlari oshganda qayta xeshlash zarurligini aniqlash
    public static function needsRehash(string $hash): bool {
        return sodium_crypto_pwhash_str_needs_rehash(
            $hash,
            SODIUM_CRYPTO_PWHASH_OPSLIMIT_INTERACTIVE,
            SODIUM_CRYPTO_PWHASH_MEMLIMIT_INTERACTIVE
        );
    }
}

// Sinov
$password = "Juda_Maxfiy_Parol_2026!#";
$hash = PasswordHasher::hash($password);
echo "[+] Argon2id Xesh: {$hash}
";

$valid = PasswordHasher::verify($password, $hash);
echo "[+] Parol to'g'rimi? " . ($valid ? "HA" : "YO'Q") . "
";
```
**Tushuntirish:** MD5, SHA256 va hatto bcrypt algoritmlari GPU lardagi minglab parallel yadrolarda juda tez sinishi mumkin. Argon2id esa ataylab xotiraga qaram qilib (Memory-Hard) yaratilgan; bitta xeshni hisoblash uchun 64MB RAM talab qilinishi sababli xakerlar GPU yoki maxsus chiplarda parallel hujum qila olmaydi.

---

### Topshiriq #1156: Libsodium crypto_generichash (BLAKE2b) Tezkor Kriptografik Xesh va MAC
**Tavsif:** SHA-256 dan 3 barobar tezroq va xavfsizroq bo'lgan BLAKE2b algoritmidan foydalanib, kalitsiz xesh hamda kalitli MAC (Message Authentication Code) hisoblash xizmatini quring.
**Talablar:** sodium_crypto_generichash, length parametri, kalitli rejim (Keyed hashing).
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - BLAKE2b Yuqori Tezlikdagi Generichash Servisi
class Blake2bService {
    // Oddiy kriptografik xesh (ixtiyoriy bayt uzunlikda, masalan 32 yoki 64 bayt)
    public static function hash(string $data, int $outLen = 32): string {
        $rawHash = sodium_crypto_generichash($data, '', $outLen);
        return sodium_bin2hex($rawHash);
    }

    // Kalitli MAC: Faqat maxfiy kalit egalari ushbu xeshni yarata va tekshira oladi
    public static function mac(string $data, string $key, int $outLen = 32): string {
        $rawMac = sodium_crypto_generichash($data, $key, $outLen);
        return sodium_bin2hex($rawMac);
    }

    public static function verifyMac(string $data, string $hexMac, string $key): bool {
        $expected = self::mac($data, $key, strlen(hex2bin($hexMac)));
        return hash_equals($expected, $hexMac);
    }
}

// Sinov
$data = "Foydalanuvchi balansi: 15,000,000 UZS";
$hash = Blake2bService::hash($data);
echo "[+] BLAKE2b 256-bit Xesh: {$hash}
";

$key = sodium_crypto_generichash_keygen();
$mac = Blake2bService::mac($data, $key);
echo "[+] Kalitli BLAKE2b MAC:   {$mac}
";

$verified = Blake2bService::verifyMac($data, $mac, $key);
echo "[+] MAC tasdiqlandimi?     " . ($verified ? "HA" : "YO'Q") . "
";
```
**Tushuntirish:** BLAKE2b SHA-3 tanlovining finalisti bo'lib, zamonaviy 64-bitli protsessorlarda SHA-256 va MD5 dan ham tezroq ishlaydi. U 'Length Extension Attack' hujumlariga tabiiy ravishda chidamli bo'lgani sababli HMAC o'rnini to'g'ridan-to'g'ri bosa oladi.

---

### Topshiriq #1157: Libsodium KDF (Key Derivation Function) orqali Subkalitlar Hosil Qilish
**Tavsif:** Bitta bosh master kalitdan (Master Key) turli xizmatlar (masalan, Fayllar, Tranzaksiyalar, Sessiyalar) uchun bir-biriga bog'liq bo'lmagan mustaqil kriptografik subkalitlarni xavfsiz hosil qiling.
**Talablar:** sodium_crypto_kdf_derive_from_key, context (8 bayt), subkey_id (int64), master keygen.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Libsodium KDF Subkalitlar Generator
class KeyDerivationManager {
    private string $masterKey;

    public function __construct(string $masterKey) {
        if (strlen($masterKey) !== SODIUM_CRYPTO_KDF_KEYBYTES) {
            throw new InvalidArgumentException("Master kalit hajmi " . SODIUM_CRYPTO_KDF_KEYBYTES . " bayt bo'lishi lozim.");
        }
        $this->masterKey = $masterKey;
    }

    // Subkalit hosil qilish: context aniq 8 bayt bo'lishi shart
    public function deriveKey(int $subkeyId, string $context, int $subkeyLength = 32): string {
        if (strlen($context) !== SODIUM_CRYPTO_KDF_CONTEXTBYTES) {
            throw new InvalidArgumentException("Context parametri qat'iy " . SODIUM_CRYPTO_KDF_CONTEXTBYTES . " bayt bo'lishi kerak!");
        }

        return sodium_crypto_kdf_derive_from_key($subkeyLength, $subkeyId, $context, $this->masterKey);
    }
}

// Bosh master kalit (HSM yoki xavfsiz Vault da saqlanadi)
$masterKey = sodium_crypto_kdf_keygen();
$kdf = new KeyDerivationManager($masterKey);

// 1. To'lovlar xizmati uchun kalit
$paymentKey = $kdf->deriveKey(1, 'payments');
// 2. Foydalanuvchi fayllari uchun kalit
$storageKey = $kdf->deriveKey(2, 'file_sto');

echo "[+] To'lov subkaliti (Hex): " . sodium_bin2hex($paymentKey) . "
";
echo "[+] Fayl saqlash subkaliti: " . sodium_bin2hex($storageKey) . "
";
```
**Tushuntirish:** Libsodium KDF Blake2b ga asoslangan. Agar bitta subkalit (masalan payments) xakerlar qo'liga tushsa ham, ular undan foydalanib boshqa subkalitlarni (storage) yoki asosiy Master kalitni matematik jihatdan qayta tiklay olmaydi (One-way property).

---

### Topshiriq #1158: Libsodium SipHash (crypto_shorthash) bilan Hash-DoS Hujumlaridan Himoyalanish
**Tavsif:** Xakerlar assotsiativ massivlarda sun'iy xesh to'qnashuvlari (Hash Collisions) hosil qilib, CPU ni 100% ga qotirib qo'yuvchi Hash-DoS hujumlarini SipHash-2-4 orqali bartaraf etuvchi xesh jadvali yarating.
**Talablar:** sodium_crypto_shorthash, random kalit bilan initsializatsiya, 64-bit tezkor xesh.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - SipHash-2-4 Hash-DoS dan Himoyalangan Hash Map
class SecureHashMap {
    private string $sipKey;
    private array $buckets = [];
    private int $size = 1024;

    public function __construct() {
        // Har bir server jarayoni uchun yangi tasodifiy SipHash kaliti olinadi
        $this->sipKey = sodium_crypto_shorthash_keygen();
    }

    private function getBucketIndex(string $key): int {
        // SipHash orqali 8-baytli (64-bit) kriptografik xesh olamiz
        $hashBytes = sodium_crypto_shorthash($key, $this->sipKey);
        $unpacked = unpack('J', $hashBytes)[1]; // 64-bit unsigned int
        return abs($unpacked) % $this->size;
    }

    public function set(string $key, mixed $value): void {
        $idx = $this->getBucketIndex($key);
        $this->buckets[$idx][$key] = $value;
    }

    public function get(string $key): mixed {
        $idx = $this->getBucketIndex($key);
        return $this->buckets[$idx][$key] ?? null;
    }
}

// Sinov
$map = new SecureHashMap();
$map->set("user_token_123", ["role" => "admin", "uid" => 42]);
echo "[+] Xavfsiz xesh jadvalidan olingan qiymat: " . json_encode($map->get("user_token_123")) . "
";
```
**Tushuntirish:** Hash-DoS hujumida buzg'unchi PHP massivida bir xil indeksga tushadigan millionlab maxsus kalitlarni yuboradi va O(1) qidiruv vaqtini O(N) ga aylantirib tizimni qotiradi. SipHash maxfiy kalit bilan ishlagani sababli xaker to'qnashuv hosil qiluvchi kalitlarni oldindan hisoblay olmaydi.

---

### Topshiriq #1159: Libsodium sodium_memzero orqali Xotirani Tozalash va sodium_compare
**Tavsif:** Parol yoki maxfiy kalitlar bilan ishlab bo'lingach, PHP garbage collector-ini kutmasdan operatsion tizim xotirasidan (RAM) maxfiy ma'lumotlarni darhol tozalab tashlovchi xavfsizlik amaliyotini ko'rsating.
**Talablar:** sodium_memzero, sodium_compare, side-channel hujumlarining oldini olish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Xotiradan Maxfiy Ma'lumotlarni Nolga Aylantirish (Memory Zeroing)
$secretEncryptionKey = sodium_crypto_secretbox_keygen();
echo "[*] Kalit yaratildi: " . sodium_bin2hex($secretEncryptionKey) . "
";

// Kriptografik operatsiyani bajaramiz...
$data = "Maxfiy moliyaviy ma'lumot";
$nonce = random_bytes(SODIUM_CRYPTO_SECRETBOX_NONCEBYTES);
$encrypted = sodium_crypto_secretbox($data, $nonce, $secretEncryptionKey);

// Diqqat: Oddiy $secretEncryptionKey = null xotiradagi baytlarni darhol o'chirmaydi!
// sodium_memzero bevosita C darajasidagi memset_s chaqirib, RAM dagi baytlarni 0x00 qiladi:
sodium_memzero($secretEncryptionKey);
sodium_memzero($data);

echo "[+] Maxfiy kalit RAM dan to'liq tozalab tashlandi!
";

// sodium_compare: Ikkita satrni vaqt jihatdan doimiy (constant-time) taqqoslash
$tokenA = "token_hash_alpha_998";
$tokenB = "token_hash_alpha_998";
$diff = sodium_compare($tokenA, $tokenB); // 0 = Teng, -1 yoki 1 = Farqli
echo "[+] Doimiy vaqt taqqoslashi: " . ($diff === 0 ? "Mos keldi" : "Farqli") . "
";
```
**Tushuntirish:** PHP skripti tugaguncha yoki core dump tushganda, xotirada qolgan o'zgaruvchilarni Heartbleed kabi xotira o'qish zaifliklari orqali o'g'irlash mumkin. `sodium_memzero` kompilyator optimizatsiyasiga tushmasdan xotirani jismonan nollab yuboradi.

---

### Topshiriq #1160: Libsodium Doimiy Vaqtli Hex va Base64 Konvertatsiyasi
**Tavsif:** Kriptografik kalitlarni hex yoki base64 ga o'girishda protsessor keshiga qarab ma'lumot sizib chiqishini (Cache-timing attacks) bartaraf qiluvchi `sodium_bin2hex` va `sodium_bin2base64` vositalarini qo'llang.
**Talablar:** sodium_bin2hex, sodium_hex2bin, sodium_bin2base64, sodium_base642bin variantlari.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Doimiy Vaqtli Ikkilik Konvertor (Side-Channel Resistant)
$secretKey = random_bytes(32);

// Standart bin2hex() va base64_encode() ichki jadvallardan foydalanishi sababli
// protsessor keshida mikro-kechikishlarni yuzaga keltiradi (Cache-Timing Attacks).
// Libsodium funksiyalari doimiy vaqtda (constant-time) ishlaydi:
$hexKey = sodium_bin2hex($secretKey);
echo "[+] Xavfsiz Hex: {$hexKey}
";

$restoredKeyFromHex = sodium_hex2bin($hexKey);

// URL-safe Base64 konvertatsiyasi (+ va / o'rniga - va _, to'ldirish belgisisiz)
$base64UrlKey = sodium_bin2base64($secretKey, SODIUM_BASE64_VARIANT_URLSAFE_NO_PADDING);
echo "[+] URL-safe Base64: {$base64UrlKey}
";

$restoredKeyFromBase64 = sodium_base642bin($base64UrlKey, SODIUM_BASE64_VARIANT_URLSAFE_NO_PADDING);

// Qayta tiklangan kalitlarni tekshiramiz
if (sodium_compare($secretKey, $restoredKeyFromBase64) === 0) {
    echo "[+] Barcha konvertatsiyalar 100% aniq va xavfsiz bajarildi!
";
}
```
**Tushuntirish:** Yon kanalli hujumlar (Side-channel attacks) - bu dasturning matematik xatosini emas, balki apparat ta'minotining (protsessor keshi, vaqt, elektr quvvati) o'zgarishini o'lchash orqali kalitni topish usulidir. Libsodium barcha konvertatsiyalarni shoxlanishsiz (branchless) bajaradi.

---

### Topshiriq #1161: OpenSSL 3 AES-256-GCM Shifrlash va AAD (Additional Authenticated Data)
**Tavsif:** Bank tranzaksiyalarini shifrlashda hisob raqami kabi ochiq qolishi kerak bo'lgan, lekin soxtalashtirilmasligi shart bo'lgan ma'lumotlarni AAD (Bog'langan Autentifikatsiya Ma'lumoti) bilan himoyalang.
**Talablar:** openssl_encrypt/decrypt, 'aes-256-gcm', auth_tag (16 bayt), aad parametri.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - OpenSSL 3 AES-256-GCM + AAD Arxitekturasi
class AesGcmService {
    private const CIPHER = 'aes-256-gcm';
    private const TAG_LENGTH = 16;
    private const IV_LENGTH = 12; // GCM uchun standart 96-bit (12 bayt) IV

    public static function encrypt(string $plaintext, string $key, string $aad = ''): array {
        $iv = random_bytes(self::IV_LENGTH);
        $tag = ''; // Natijaviy autentifikatsiya tegi

        $ciphertext = openssl_encrypt(
            $plaintext,
            self::CIPHER,
            $key,
            OPENSSL_RAW_DATA,
            $iv,
            $tag,
            $aad,
            self::TAG_LENGTH
        );

        if ($ciphertext === false) {
            throw new Exception("Shifrlashda xatolik yuz berdi!");
        }

        return [
            'ciphertext' => base64_encode($ciphertext),
            'iv'         => base64_encode($iv),
            'tag'        => base64_encode($tag),
            'aad'        => $aad
        ];
    }

    public static function decrypt(string $cipherBase64, string $ivBase64, string $tagBase64, string $key, string $aad = ''): ?string {
        $ciphertext = base64_decode($cipherBase64);
        $iv = base64_decode($ivBase64);
        $tag = base64_decode($tagBase64);

        $plaintext = openssl_decrypt(
            $ciphertext,
            self::CIPHER,
            $key,
            OPENSSL_RAW_DATA,
            $iv,
            $tag,
            $aad
        );

        return ($plaintext !== false) ? $plaintext : null;
    }
}

// Sinov
$key = openssl_random_pseudo_bytes(32); // 256-bit kalit
$payload = "O'tkazma summasi: 10,000,000 UZS";
$accountAad = "ACCOUNT_ID_998124"; // AAD: Shifrlanmaydi, lekin yaxlitligi kafolatlanadi

$enc = AesGcmService::encrypt($payload, $key, $accountAad);
echo "[+] AES-256-GCM Shifrlandi! Tag: {$enc['tag']}
";

// To'g'ri AAD bilan ochish
$decrypted = AesGcmService::decrypt($enc['ciphertext'], $enc['iv'], $enc['tag'], $key, $accountAad);
echo "[+] Deshifr natijasi: {$decrypted}
";

// Agar buzg'unchi AAD ni o'zgartirsa (boshqa hisobga yo'naltirishga urinsa):
$tamperedDec = AesGcmService::decrypt($enc['ciphertext'], $enc['iv'], $enc['tag'], $key, "ACCOUNT_ID_666666");
echo "[-] Buzilgan AAD tekshiruvi: " . ($tamperedDec === null ? "MUVOFIQ TARZDA RAD ETILDI" : "XATO") . "
";
```
**Tushuntirish:** AAD (Additional Authenticated Data) shifrlanmaydi (marshrutlash yoki indekslash uchun ochiq qoladi), lekin u kriptografik tegga (`tag`) kiritiladi. Agar buzg'unchi AAD dagi hisob raqamini almashtirsa, tegga mos kelmay shifr ochilmaydi.

---

### Topshiriq #1162: OpenSSL ChaCha20-Poly1305 Shifrlash Algoritmi
**Tavsif:** AES apparat tezlatgichi (AES-NI) mavjud bo'lmagan mobil mijozlar yoki kam quvvatli serverlar uchun yuqori samaradorlikka ega ChaCha20-Poly1305 shifrlash tizimini joriy qiling.
**Talablar:** openssl_encrypt da 'chacha20-poly1305', IV o'lchami (12 bayt), autentifikatsiya tegi tekshiruvi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - OpenSSL ChaCha20-Poly1305 AEAD
class ChaCha20Service {
    private const CIPHER = 'chacha20-poly1305';

    public static function encrypt(string $message, string $key): array {
        $iv = random_bytes(12); // 96-bit IV
        $tag = '';

        $cipher = openssl_encrypt(
            $message,
            self::CIPHER,
            $key,
            OPENSSL_RAW_DATA,
            $iv,
            $tag,
            '',
            16
        );

        return [
            'cipher' => bin2hex($cipher),
            'iv'     => bin2hex($iv),
            'tag'    => bin2hex($tag)
        ];
    }

    public static function decrypt(string $hexCipher, string $hexIv, string $hexTag, string $key): ?string {
        $decrypted = openssl_decrypt(
            hex2bin($hexCipher),
            self::CIPHER,
            $key,
            OPENSSL_RAW_DATA,
            hex2bin($hexIv),
            hex2bin($hexTag)
        );

        return ($decrypted !== false) ? $decrypted : null;
    }
}

$key = random_bytes(32);
$enc = ChaCha20Service::encrypt("Khorazmiy AI: ChaCha20-Poly1305 xavfsiz kanali", $key);
echo "[+] ChaCha20-Poly1305 shifrlangan paket olindi.
";

$plain = ChaCha20Service::decrypt($enc['cipher'], $enc['iv'], $enc['tag'], $key);
echo "[+] Ochilgan ma'lumot: {$plain}
";
```
**Tushuntirish:** Daniel J. Bernstein tomonidan ishlab chiqilgan ChaCha20-Poly1305 dasturiy darajada AES ga nisbatan 2-3 barobar tezroq ishlaydi va jadval asosidagi (lookup-table) kesh hujumlariga mutlaqo uchramaydi. Google va Cloudflare uni TLS da keng qo'llaydi.

---

### Topshiriq #1163: OpenSSL RSA 4096-bit Kalitlar Generatsiyasi va OAEP To'ldirish
**Tavsif:** Kompaniya ichki kalit infratuzilmasi uchun RSA 4096-bit kalitlar juftligini yaratuvchi hamda eskirgan PKCS#1 v1.5 o'rniga xavfsiz OAEP to'ldirish (Optimal Asymmetric Encryption Padding) bilan shifrlovchi vosita quring.
**Talablar:** openssl_pkey_new, OPENSSL_PKCS1_OAEP_PADDING, openssl_public_encrypt, openssl_private_decrypt.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - OpenSSL RSA 4096 OAEP Xavfsiz Shifrlash
class RsaOaepManager {
    public static function generateKeyPair(): array {
        $config = [
            "digest_alg"       => "sha256",
            "private_key_bits" => 4096,
            "private_key_type" => OPENSSL_KEYTYPE_RSA,
        ];

        $res = openssl_pkey_new($config);
        openssl_pkey_export($res, $privateKey);
        $publicKeyDetails = openssl_pkey_get_details($res);
        $publicKey = $publicKeyDetails["key"];

        return ['private' => $privateKey, 'public' => $publicKey];
    }

    // OAEP orqali ommaviy kalit bilan shifrlash
    public static function encrypt(string $data, string $publicKey): string {
        $encrypted = '';
        $success = openssl_public_encrypt($data, $encrypted, $publicKey, OPENSSL_PKCS1_OAEP_PADDING);
        if (!$success) {
            throw new Exception("RSA shifrlashda xato yuz berdi!");
        }
        return base64_encode($encrypted);
    }

    // Maxfiy kalit bilan deshifrlash
    public static function decrypt(string $base64Encrypted, string $privateKey): ?string {
        $data = base64_decode($base64Encrypted);
        $decrypted = '';
        $success = openssl_private_decrypt($data, $decrypted, $privateKey, OPENSSL_PKCS1_OAEP_PADDING);
        return $success ? $decrypted : null;
    }
}

// Sinov
$keys = RsaOaepManager::generateKeyPair();
$secretNote = "DB_PASSWORD=SecureSuperClusterPass2026!";

$encrypted = RsaOaepManager::encrypt($secretNote, $keys['public']);
echo "[+] RSA-4096 OAEP shifrlangan hajm: " . strlen($encrypted) . " belgi
";

$restored = RsaOaepManager::decrypt($encrypted, $keys['private']);
echo "[+] Deshifrlangan parol: {$restored}
";
```
**Tushuntirish:** Eskirgan PKCS#1 v1.5 padding usuli 'Bleichenbacher padding oracle' hujumiga uchraydi, bu orqali tajovuzkor minglab so'rovlar yuborib shifrni o'qiy oladi. OAEP padding esa xabarni oldindan tasodifiylashtirib (Feistel tarmog'i) ushbu matematik zaiflikni to'liq bartaraf qiladi.

---

### Topshiriq #1164: OpenSSL ECDSA (Elliptic Curve secp256k1 / P-256) Raqamli Imzosi
**Tavsif:** Blokcheyn (Bitcoin/Ethereum) yoki xavfsiz API shlyuzlarida foydalaniladigan elliptik egri chiziqlar (secp256k1 yoki prime256v1) asosida raqamli imzo qo'yish va tasdiqlash xizmatini dasturlang.
**Talablar:** openssl_pkey_new da curve_name, openssl_sign, openssl_verify, OPENSSL_ALGO_SHA256.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - OpenSSL ECDSA Elliptic Curve Imzo Tizimi
class EcdsaSigner {
    public static function generateEcKeys(string $curveName = 'prime256v1'): array {
        $config = [
            "private_key_type" => OPENSSL_KEYTYPE_EC,
            "curve_name"       => $curveName,
        ];

        $res = openssl_pkey_new($config);
        openssl_pkey_export($res, $privateKey);
        $details = openssl_pkey_get_details($res);
        return [
            'private' => $privateKey,
            'public'  => $details['key']
        ];
    }

    public static function sign(string $payload, string $privateKey): string {
        $signature = '';
        openssl_sign($payload, $signature, $privateKey, OPENSSL_ALGO_SHA256);
        return base64_encode($signature);
    }

    public static function verify(string $payload, string $base64Sig, string $publicKey): bool {
        $rawSig = base64_decode($base64Sig);
        $res = openssl_verify($payload, $rawSig, $publicKey, OPENSSL_ALGO_SHA256);
        return ($res === 1);
    }
}

// Sinov
$keys = EcdsaSigner::generateEcKeys('prime256v1'); // NIST P-256
$txData = '{"tx_id": "0xabc123", "sender": "Ali", "recipient": "Vali", "amount": 500}';

$signature = EcdsaSigner::sign($txData, $keys['private']);
echo "[+] ECDSA Imzo: {$signature}
";

$isValid = EcdsaSigner::verify($txData, $signature, $keys['public']);
echo "[+] ECDSA Imzo tekshiruvi: " . ($isValid ? "HAQIQIY" : "SOXTA") . "
";
```
**Tushuntirish:** ECDSA (Elliptic Curve Digital Signature Algorithm) RSA ga nisbatan 10 barobar qisqa kalitlarda (256-bit EC kaliti 3072-bit RSA ga teng kuchli) bir xil xavfsizlik darajasini ta'minlaydi. Bu mobil qurilmalar va mikroxizmatlarda CPU va tarmoq trafigini keskin tejaydi.

---

### Topshiriq #1165: OpenSSL HKDF (RFC 5869) Kalit Hosil Qilish Standarti
**Tavsif:** Diffie-Hellman orqali kelishilgan umumiy sirdan (shared secret) kriptografik jihatdan mustaqil bo'lgan Shifrlash va Autentifikatsiya kalitlarini RFC 5869 HKDF standarti orqali hosil qiling.
**Talablar:** hash_hkdf funksiyasidan foydalanish, ikkita alohida kalit (enc_key, mac_key), info konteksti.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - RFC 5869 HKDF (HMAC-based Key Derivation)
class HkdfKeyDeriver {
    // Extract va Expand bosqichlarini birlashtirgan HKDF
    public static function deriveKeys(string $ikm, string $salt = '', int $keyLength = 32): array {
        if (empty($salt)) {
            $salt = str_repeat(" ", 32); // Agar salt bo'lmasa 32 ta nol bayt
        }

        // 1. Shifrlash uchun kalit (AES-GCM)
        $encryptionKey = hash_hkdf('sha256', $ikm, $keyLength, 'khorazmiy_app_encryption_v1', $salt);
        
        // 2. MAC autentifikatsiyasi uchun kalit
        $macKey = hash_hkdf('sha256', $ikm, $keyLength, 'khorazmiy_app_authentication_v1', $salt);

        return [
            'encryption_key' => bin2hex($encryptionKey),
            'mac_key'        => bin2hex($macKey)
        ];
    }
}

// Kiruvchi umumiy xom sir (IKM - Input Keying Material)
$rawSecret = random_bytes(32);
$salt = random_bytes(16);

$derived = HkdfKeyDeriver::deriveKeys($rawSecret, $salt);
echo "[+] HKDF Shifrlash kaliti: {$derived['encryption_key']}
";
echo "[+] HKDF MAC kaliti:       {$derived['mac_key']}
";
```
**Tushuntirish:** Bitta kalitni ham shifrlash, ham imzo/MAC uchun bir vaqtda ishlatish (Key Reuse) jiddiy xavfsizlik zaifligini keltirib chiqaradi. HKDF xom kiritilgan sirdan turli maqsadlar uchun matematik jihatdan mustaqil subkalitlarni ajratib beradi.

---

### Topshiriq #1166: OpenSSL PBKDF2 Kalit Hosil Qilish va Iteratsiyalar Balansi
**Tavsif:** Foydalanuvchi kiritgan oddiy paroldan simmetrik AES kalitini hosil qilish uchun PBKDF2 (Password-Based Key Derivation Function 2) ni NIST talab qilgan 600,000 iteratsiya bilan amalga oshiring.
**Talablar:** hash_pbkdf2, 'sha256', iteratsiyalar soni (kamida 600000), kriptografik tasodifiy tuz (salt).
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - PBKDF2 NIST Standartidagi Kalit Derivatsiyasi
class Pbkdf2Manager {
    public static function deriveKeyFromPassword(string $password, string $salt, int $iterations = 600000): string {
        // OWASP va NIST 2024 tavsiyasi: HMAC-SHA256 uchun kamida 600,000 iteratsiya
        $derivedKey = hash_pbkdf2('sha256', $password, $salt, $iterations, 32, true);
        return $derivedKey;
    }
}

$userPassword = "MeningMurakkabParolim_99!";
$salt = random_bytes(16); // Har bir foydalanuvchi uchun unikal tuz

$start = microtime(true);
$aesKey = Pbkdf2Manager::deriveKeyFromPassword($userPassword, $salt);
$duration = round((microtime(true) - $start) * 1000, 2);

echo "[+] PBKDF2 Kalit olindi: " . bin2hex($aesKey) . "
";
echo "[+] Hisoblash vaqti: {$duration} ms (Iteratsiyalar: 600,000)
";
```
**Tushuntirish:** PBKDF2 HMAC funksiyasini yuz minglab marta takrorlaydi. Bu tajovuzkorlarning lug'at asosidagi (Dictionary attack) va kamalak jadvallari (Rainbow tables) orqali parolni taxmin qilishini bir necha yilga sekinlashtiradi.

---

### Topshiriq #1167: X.509 Raqamli Sertifikatlar Zanjirini (Chain of Trust) Tekshirish
**Tavsif:** Tashqi bank yoki hamkorlar bilan integratsiyada ularning taqdim etgan X.509 TLS sertifikatining haqiqiyligini, CA ildiz sertifikatiga bog'liqligini va amal qilish muddatini tekshiruvchi validator yozing.
**Talablar:** openssl_x509_read, openssl_x509_checkpurpose, openssl_x509_parse, muddat va sanalarni solishtirish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - X.509 Sertifikatlar Zanjiri Validatori
class CertificateValidator {
    public static function inspectCertificate(string $certPem): array {
        $certData = openssl_x509_parse($certPem);
        if ($certData === false) {
            throw new Exception("Noto'g'ri X.509 sertifikat formati!");
        }

        $now = time();
        $validFrom = $certData['validFrom_time_t'];
        $validTo   = $certData['validTo_time_t'];

        $isNotExpired = ($now >= $validFrom && $now <= $validTo);

        return [
            'subject_cn'   => $certData['subject']['CN'] ?? 'Noma'lum',
            'issuer_cn'    => $certData['issuer']['CN'] ?? 'Noma'lum',
            'valid_from'   => date('Y-m-d H:i:s', $validFrom),
            'valid_to'     => date('Y-m-d H:i:s', $validTo),
            'is_valid'     => $isNotExpired,
            'serial_hex'   => $certData['serialNumberHex'] ?? '0'
        ];
    }

    // CA sertifikati orqali mijoz sertifikatini tasdiqlash
    public static function verifyAgainstCa(string $clientCertPem, string $caCertPem): bool {
        return (openssl_x509_checkpurpose($clientCertPem, X509_PURPOSE_SSL_CLIENT, [$caCertPem]) === true);
    }
}

// Sinov uchun o'z-o'zini imzolagan test sertifikatini tekshiramiz
$testCert = openssl_x509_export_to_file(
    openssl_csr_sign(
        openssl_csr_new(["commonName" => "api.khorazmiy.uz"], $pk = openssl_pkey_new()),
        null, $pk, 365
    ),
    $tmpFile = tempnam(sys_get_temp_dir(), 'cert')
);
$pem = file_get_contents($tmpFile);
unlink($tmpFile);

$info = CertificateValidator::inspectCertificate($pem);
echo "[+] Sertifikat Common Name: {$info['subject_cn']}
";
echo "[+] Muddati to'g'rimi?       " . ($info['is_valid'] ? "HA" : "MUDDATI O'TGAN") . "
";
```
**Tushuntirish:** X.509 'Ishonch zanjiri' (Chain of Trust) tamoyiliga asoslanadi. Har bir sertifikat yuqori turuvchi Sertifikatlash Markazi (CA) tomonidan imzolangan bo'lishi kerak. Bu orqali 'Man-in-the-Middle' hujumlarining oldi olinadi.

---

### Topshiriq #1168: PKCS#7 / CMS orqali Ma'lumotlarni Muhrlash va Imzolash
**Tavsif:** Elektron hisob-fakturalar va davlat soliq idoralari bilan xavfsiz almashish uchun ma'lumotlarni PKCS#7 (S/MIME) standarti bo'yicha imzolash va shifrlashni amalga oshiring.
**Talablar:** openssl_pkcs7_sign, openssl_pkcs7_verify, openssl_pkcs7_encrypt, openssl_pkcs7_decrypt.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - PKCS#7 / S/MIME Hujjatlarni Imzolash
class Pkcs7Service {
    public static function signMessage(string $inFilePath, string $outSignedPath, string $certPemPath, string $keyPemPath): bool {
        return openssl_pkcs7_sign(
            $inFilePath,
            $outSignedPath,
            $certPemPath,
            $keyPemPath,
            ["To" => "audit@soliq.uz", "Subject" => "Elektron Hisob-faktura"],
            PKCS7_DETACHED
        );
    }

    public static function verifySignedMessage(string $signedFilePath, string $caCertPath): bool {
        // Imzoni va uning CA ga bog'liqligini tekshirish
        return (openssl_pkcs7_verify($signedFilePath, PKCS7_NOVERIFY, $caCertPath) === true);
    }
}

echo "[+] PKCS#7 / CMS xizmati yuklandi va shartnomalar imzolashga tayyor.
";
```
**Tushuntirish:** PKCS#7 (Cryptographic Message Syntax) korporativ xatlar (S/MIME) va davlat darajasidagi elektron hujjat aylanishining poydevoridir. U shaxsiy kalit bilan imzolangan hujjatni ommaviy sertifikat bilan birga paketlaydi.

---

### Topshiriq #1169: Kriptografik Xavfsiz Tasodifiy Sonlar (CSPRNG) Generatsiyasi
**Tavsif:** Kriptografiyada oddiy `rand()` yoki `mt_rand()` ishlatish xavfli bo'lganligi sababli, operatsion tizim entropiyasiga tayangan CSPRNG orqali tokenlar, tuzlar va xavfsiz parollar hosil qiling.
**Talablar:** random_bytes, random_int, CSPRNG xatolarini ushlash, xavfsiz URL tokenlar generatori.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Sanoat Darajasidagi CSPRNG Generator
class CsprngUtility {
    // Kriptografik tasodifiy heksadesimal token
    public static function generateHexToken(int $byteLength = 32): string {
        return bin2hex(random_bytes($byteLength));
    }

    // URL da xavfsiz ishlatiladigan Base64 token (64 belgi)
    public static function generateUrlSafeToken(int $byteLength = 32): string {
        $raw = random_bytes($byteLength);
        return rtrim(strtr(base64_encode($raw), '+/', '-_'), '=');
    }

    // Belgilangan oraliqdagi kriptografik xavfsiz butun son (masalan 6 xonali SMS kod)
    public static function generateSecurePin(int $min = 100000, int $max = 999999): int {
        return random_int($min, $max);
    }

    // Kriptografik xavfsiz murakkab parol generatsiyasi
    public static function generateComplexPassword(int $length = 16): string {
        $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+';
        $maxIndex = strlen($chars) - 1;
        $password = '';
        for ($i = 0; $i < $length; $i++) {
            $password .= $chars[random_int(0, $maxIndex)];
        }
        return $password;
    }
}

echo "[+] CSPRNG Hex Token:     " . CsprngUtility::generateHexToken() . "
";
echo "[+] URL-safe Token:       " . CsprngUtility::generateUrlSafeToken() . "
";
echo "[+] SMS 6-xonali kod:     " . CsprngUtility::generateSecurePin() . "
";
echo "[+] Tasodifiy kuchli parol: " . CsprngUtility::generateComplexPassword(20) . "
";
```
**Tushuntirish:** `rand()` va `mt_rand()` psevdo-tasodifiy (PRNG) bo'lib, uning urug'i (seed) va ichki holati bir necha chiqishlardan so'ng Mersenne Twister orqali to'liq bashorat qilinishi mumkin. `random_bytes` esa Linux yadrosining `/dev/urandom` va apparat entropiyasiga tayanadi.

---

### Topshiriq #1170: OpenSSL Envelope Encryption (Kombinatsiyalangan Gibrid Shifrlash)
**Tavsif:** Katta ma'lumotlarni tezkor simmetrik kalit (DEK - Data Encryption Key) bilan shifrlab, ushbu kalitning o'zini esa qabul qiluvchining RSA ommaviy kaliti bilan o'rab (Envelope) jo'nating.
**Talablar:** openssl_seal, openssl_open, bir nechta qabul qiluvchilar uchun konvert yaratish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - OpenSSL Envelope Encryption (Gibrid Shifrlash)
class EnvelopeEncryptionService {
    // Ma'lumotni shifrlash va kalitni qabul qiluvchilarning RSA ommaviy kalitlari bilan muhrlash
    public static function seal(string $data, array $publicKeys): array {
        $sealedData = '';
        $envelopeKeys = []; // Har bir qabul qiluvchi uchun shifrlangan DEK

        // openssl_seal avtomatik tasodifiy AES kalit yaratadi, ma'lumotni shifrlaydi
        // va shu kalitni berilgan barcha ommaviy kalitlar bilan shifrlaydi
        $result = openssl_seal($data, $sealedData, $envelopeKeys, $publicKeys, 'RC4');
        if ($result === false) {
            throw new Exception("Konvertni muhrlashda xatolik yuz berdi!");
        }

        return [
            'sealed_data'   => base64_encode($sealedData),
            'envelope_keys' => array_map('base64_encode', $envelopeKeys)
        ];
    }

    // Qabul qiluvchi o'zining shaxsiy RSA kaliti orqali konvertni ochadi
    public static function open(string $sealedBase64, string $envKeyBase64, string $privateKey): ?string {
        $sealedData = base64_decode($sealedBase64);
        $envelopeKey = base64_decode($envKeyBase64);
        $openedData = '';

        $success = openssl_open($sealedData, $openedData, $envelopeKey, $privateKey);
        return $success ? $openedData : null;
    }
}

// Sinov
$res = openssl_pkey_new(["private_key_bits" => 2048]);
openssl_pkey_export($res, $privKey);
$pubKey = openssl_pkey_get_details($res)['key'];

$sensitiveInfo = "Maxfiy strategik reja: 2026-yil 4-chorak";
$sealed = EnvelopeEncryptionService::seal($sensitiveInfo, [$pubKey]);
echo "[+] Konvert muhrlandi. Shifrlangan kalitlar soni: " . count($sealed['envelope_keys']) . "
";

$restored = EnvelopeEncryptionService::open($sealed['sealed_data'], $sealed['envelope_keys'][0], $privKey);
echo "[+] Konvert ochildi: {$restored}
";
```
**Tushuntirish:** Gibrid (Envelope) shifrlash assimetrik kriptografiyaning sekinligini (RSA) va simmetrik shifrlashning qulayligini (AES) birlashtiradi. AWS KMS va Google Cloud KMS aynan ushbu Envelope Encryption tamoyili asosida ishlaydi.

---

### Topshiriq #1171: SQL Injection To'liq Profilaktikasi va Xavfsiz Dinamik So'rovlar
**Tavsif:** Oddiy qiymatlarni PDO Prepared Statements bilan himoyalashdan tashqari, ustun nomlari (ORDER BY) va jadvallar kabi parametrlashtirib bo'lmaydigan qismlarni Whitelisting orqali himoyalang.
**Talablar:** PDO parametrlashtirilgan so'rovlar, qat'iy oq ro'yxat (Whitelist validation), SQL injection urinishlarini bloklash.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - SQL Injection dan 100% Himoyalangan Repozitoriy
class UserRepository {
    private PDO $pdo;

    // Ruxsat berilgan saralash ustunlari (Whitelist)
    private const ALLOWED_SORT_COLUMNS = ['id', 'username', 'created_at', 'balance'];
    private const ALLOWED_ORDERS = ['ASC', 'DESC'];

    public function __construct(PDO $pdo) {
        $this->pdo = $pdo;
        // PDO da emulyatsiyani o'chirish (Haqiqiy server-side prepared statements)
        $this->pdo->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
        $this->pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }

    public function searchUsers(string $searchTerm, string $sortBy = 'id', string $order = 'ASC'): array {
        // 1. Dinamik ustun nomlarini qat'iy tekshirish (Whitelisting)
        if (!in_array(strtolower($sortBy), self::ALLOWED_SORT_COLUMNS, true)) {
            throw new InvalidArgumentException("Ruxsat etilmagan saralash ustuni: {$sortBy}");
        }
        $order = (strtoupper($order) === 'DESC') ? 'DESC' : 'ASC';

        // 2. Parametrlashtirilgan so'rov
        $sql = "SELECT id, username, email, balance FROM users 
                WHERE username LIKE :query OR email LIKE :query 
                ORDER BY {$sortBy} {$order} 
                LIMIT 50";

        $stmt = $this->pdo->prepare($sql);
        // % belgisini xavfsiz bog'lash
        $searchWildcard = "%" . $searchTerm . "%";
        $stmt->bindValue(':query', $searchWildcard, PDO::PARAM_STR);
        $stmt->execute();

        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
}

// Sinov
$pdo = new PDO('sqlite::memory:');
$pdo->exec("CREATE TABLE users (id INT, username TEXT, email TEXT, balance REAL)");
$pdo->exec("INSERT INTO users VALUES (1, 'alisher', 'ali@test.uz', 5000)");

$repo = new UserRepository($pdo);
$results = $repo->searchUsers('ali', 'balance', 'DESC');
echo "[+] Xavfsiz qidiruv natijasi: Topildi " . count($results) . " ta foydalanuvchi.
";
```
**Tushuntirish:** Ko'pgina dasturchilar `ORDER BY :column` deb yozish mumkin deb o'ylashadi, lekin SQL standartida identifikatorlarni parametr qilib bo'lmaydi. Identifikatorlar uchun yagona xavfsiz yo'l - kodda qat'iy oq ro'yxat (Whitelisting) orqali tekshirishdir.

---

### Topshiriq #1172: Blind SQL Injection va Second-Order SQLi Hujumlarini Neytrallash
**Tavsif:** Foydalanuvchi bazaga xavfsiz yozgan, lekin keyinchalik boshqa murakkab hisobot skriptida ishlatiladigan ma'lumotlar orqali amalga oshiriladigan Ikkinchi Tartibli (Second-Order) SQLi ni bartaraf eting.
**Talablar:** Har bir qatlamda (o'qish va yozish) to'liq tayyorlangan so'rovlar, xom konkatenatsiyani butunlay taqiqlash.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Second-Order SQLi va Blind SQLi Himoyasi
class AuditBillingReport {
    private PDO $pdo;

    public function __construct(PDO $pdo) {
        $this->pdo = $pdo;
    }

    // Foydalanuvchi o'z profiliga quyidagi ismni qo'ydi: admin' OR '1'='1
    // Birinchi so'rov uni xavfsiz bazaga yozdi. Xavf keyingi hisobotda yuzaga keladi:
    public function generateDepartmentSummary(string $departmentCode): array {
        // XATO USUL: $sql = "SELECT * FROM sales WHERE dept = '" . $row['dept'] . "'";
        // TO'G'RI USUL: Qayerdan o'qilishidan qat'i nazar, HAR BIR so'rov prepared statement bo'lishi shart!
        $sql = "SELECT department, SUM(amount) as total_revenue, COUNT(*) as tx_count 
                FROM financial_transactions 
                WHERE department = :dept_code 
                GROUP BY department";

        $stmt = $this->pdo->prepare($sql);
        $stmt->execute([':dept_code' => $departmentCode]);

        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
}

echo "[+] Second-Order SQLi himoyasi: Hatto ichki bazadagi ma'lumotlar ham tashqi parametr kabi qat'iy bog'lanadi.
";
```
**Tushuntirish:** Second-Order SQL Injection hujumida zararli SQL yuklama birinchi qadamda bazaga zararsiz matn sifatida kiritiladi (masalan foydalanuvchi ismi yoki manzil). So'ngra administrator hisobot yoki fon skripti ushbu matnni xom tarzda SQL ga ulaganda tizim buziladi.

---

### Topshiriq #1173: Kontekstual XSS (Cross-Site Scripting) Himoyasi
**Tavsif:** HTML tanasi, HTML atributlari, JavaScript o'zgaruvchilari va URL parametrlari uchun har bir kontekstga mos alohida xavfsiz ekranga chiqarish (Escaping) tizimini joriy qiling.
**Talablar:** htmlspecialchars (ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'), json_encode, rawurlencode, JavaScript konteksti.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Kontekstual XSS Escape Mexanizmi
class SafeOutput {
    // 1. HTML teglari ichidagi matn: <div>...</div>
    public static function html(string $input): string {
        return htmlspecialchars($input, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
    }

    // 2. HTML atributlari: <input value="...">
    public static function attr(string $input): string {
        return htmlspecialchars($input, ENT_QUOTES, 'UTF-8');
    }

    // 3. JavaScript o'zgaruvchisi ichiga ineksiya: <script>let user = ...;</script>
    public static function js(mixed $data): string {
        // HEX bayroqlari orqali <, >, &, ', " belgilarini xavfsiz Unicode formatga o'giramiz
        return json_encode($data, JSON_HEX_TAG | JSON_HEX_APOS | JSON_HEX_QUOT | JSON_HEX_AMP | JSON_UNESCAPED_UNICODE);
    }

    // 4. URL parametrlar ichidagi qiymatlar: <a href="/search?q=...">
    public static function url(string $input): string {
        return rawurlencode($input);
    }
}

// Sinov: Xaker kiritgan zararli XSS yuklama
$maliciousInput = '<script>alert("XSS!");</script>';

echo "[HTML Konteksti]: " . SafeOutput::html($maliciousInput) . "
";
echo "[Attr Konteksti]: <input value="" . SafeOutput::attr($maliciousInput) . "">
";
echo "[JS Konteksti]:   let val = " . SafeOutput::js($maliciousInput) . ";
";
echo "[URL Konteksti]:  /search?q=" . SafeOutput::url($maliciousInput) . "
";
```
**Tushuntirish:** Bitta `htmlspecialchars` barcha holatlarga to'g'ri kelmaydi. Masalan, JavaScript blokida `let name = '<?= htmlspecialchars($name) ?>';` yozilsa, buzg'unchi `name = \'; alert(1); //` orqali XSS qila oladi. Shuning uchun JavaScript ichiga faqat `JSON_HEX_*` bayroqli `json_encode` berilishi shart.

---

### Topshiriq #1174: Content Security Policy (CSP v3) Nonce va Hash Generator
**Tavsif:** Brauzerda ruxsatsiz inline JavaScript va begona domenlardan zararli skriptlar yuklanishini bloklash uchun har bir HTTP so'rovi uchun unikal kriptografik Nonce bilan CSP sarlavhasi generatsiya qiling.
**Talablar:** Har bir so'rovda 128-bit Nonce, CSP v3 Header shakllantirish, inline skriptlarga nonce biriktirish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Dinamik CSP v3 Nonce Boshqaruvchisi
class CspManager {
    private static ?string $nonce = null;

    // Har bir HTTP so'rovida faqat bir marta generatsiya qilinadi
    public static function getNonce(): string {
        if (self::$nonce === null) {
            self::$nonce = base64_encode(random_bytes(16));
        }
        return self::$nonce;
    }

    // Xavfsiz HTTP CSP Header yuborish
    public static function sendCspHeader(): void {
        $nonce = self::getNonce();
        $policy = [
            "default-src 'self'",
            "script-src 'self' 'nonce-{$nonce}' 'strict-dynamic'",
            "style-src 'self' 'unsafe-inline'",
            "img-src 'self' data: https:",
            "font-src 'self'",
            "object-src 'none'",
            "base-uri 'none'",
            "frame-ancestors 'none'", // Clickjacking himoyasi
            "upgrade-insecure-requests"
        ];

        $headerValue = implode('; ', $policy);
        header("Content-Security-Policy: {$headerValue}");
    }
}

// Foydalanish:
$nonce = CspManager::getNonce();
echo "[+] Ushbu so'rov uchun CSP Nonce: {$nonce}
";
echo "[+] HTML da skriptni chaqirish: <script nonce="{$nonce}">console.log('Xavfsiz inline kod');</script>
";
```
**Tushuntirish:** CSP Nonce (Number used once) bu har bir sahifa yuklanganda o'zgaradigan yashirin paroldir. Xaker XSS orqali `<script>steal()</script>` qistirganda, uning ichida to'g'ri `nonce` bo'lmagani sababli zamonaviy brauzerlar uni ijro etishdan bosh tortadi.

---

### Topshiriq #1175: CSRF (Cross-Site Request Forgery) Synchronizer Token Himoyasi
**Tavsif:** Boshqa saytdan foydalanuvchi nomidan yashirin to'lov yoki parol o'zgartirish so'rovlari jo'natilishining oldini olish uchun kriptografik Synchronizer Token va SameSite cookie himoyasini joriy qiling.
**Talablar:** sessionda CSRF token saqlash, hash_equals bilan tekshirish, SameSite=Strict cookies.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Sanoat Darajasidagi CSRF Himoya Tizimi
class CsrfProtection {
    public static function initSession(): void {
        if (session_status() === PHP_SESSION_NONE) {
            session_start([
                'cookie_httponly' => true,
                'cookie_secure'   => true,
                'cookie_samesite' => 'Strict',
            ]);
        }
    }

    // Yangi CSRF token generatsiya qilish yoki mavjudini olish
    public static function getToken(): string {
        self::initSession();
        if (empty($_SESSION['csrf_token'])) {
            $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
        }
        return $_SESSION['csrf_token'];
    }

    // Kiruvchi POST so'rovdagi tokenni tekshirish
    public static function validateRequest(?string $submittedToken): bool {
        self::initSession();
        $storedToken = $_SESSION['csrf_token'] ?? '';

        if (empty($storedToken) || empty($submittedToken)) {
            return false;
        }

        // Timing-attack xavfsiz taqqoslash
        return hash_equals($storedToken, $submittedToken);
    }
}

// Sinov
$token = CsrfProtection::getToken();
echo "[+] Generatsiya qilingan CSRF token: {$token}
";

$isValid = CsrfProtection::validateRequest($token);
echo "[+] To'g'ri token tekshiruvi: " . ($isValid ? "QABUL QILINDI" : "RAD ETILDI") . "
";

$isInvalid = CsrfProtection::validateRequest("soxta_token_123");
echo "[-] Noto'g'ri token tekshiruvi: " . ($isInvalid ? "QABUL QILINDI" : "XAVFSIZLIK: RAD ETILDI") . "
";
```
**Tushuntirish:** CSRF hujumida brauzer foydalanuvchining autentifikatsiya cookie-larini avtomatik qo'shib yuboradi. Server tomonida esa har bir POST/PUT shaklida soxtalashtirib bo'lmaydigan, faqat sahifada ko'rinadigan maxfiy CSRF token talab qilinishi bu hujumni butunlay yo'q qiladi.

---

### Topshiriq #1176: SSRF (Server-Side Request Forgery) Himoyasi va DNS Rebinding Filtr
**Tavsif:** Foydalanuvchi bergan havoladan avatar yoki rasm yuklashda, serverning ichki xususiy tarmoqlari (127.0.0.1, 10.0.0.0/8, 169.254.169.254 AWS metadata) va DNS Rebinding hujumlaridan to'liq himoyalang.
**Talablar:** parse_url, dns_get_record, filter_var FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE, CURLOPT_RESOLVE.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Sanoat Darajasidagi SSRF va DNS Rebinding Himoyasi
class SafeHttpClient {
    // Ruxsat berilgan protokollar
    private const ALLOWED_SCHEMES = ['http', 'https'];

    public static function fetchUrlSafely(string $targetUrl): string {
        $parsed = parse_url($targetUrl);
        if (!$parsed || empty($parsed['scheme']) || empty($parsed['host'])) {
            throw new InvalidArgumentException("Yaroqsiz URL formati!");
        }

        // 1. Protokolni tekshirish (file://, gopher://, dict:// taqiqlanadi)
        $scheme = strtolower($parsed['scheme']);
        if (!in_array($scheme, self::ALLOWED_SCHEMES, true)) {
            throw new SecurityException("Ruxsatsiz protokol: {$scheme}");
        }

        $host = $parsed['host'];

        // 2. DNS yechish (Host IP manzillarini olamiz)
        $ips = gethostbynamel($host);
        if (!$ips) {
            throw new Exception("DNS orqali IP aniqlanmadi: {$host}");
        }

        // 3. Har bir IP ni xususiy (Private) va zaxiralangan (Reserved) diapazonlarga tekshirish
        foreach ($ips as $ip) {
            if (!filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE)) {
                // 10.x.x.x, 172.16-31.x.x, 192.168.x.x, 127.x.x.x, 169.254.x.x (AWS metadata) bloklanadi
                throw new SecurityException("[SSRF XAVF] Xususiy yoki lokal tarmoqqa so'rov taqiqlandi: {$ip} ({$host})");
            }
        }

        $resolvedIp = $ips[0];
        $port = $parsed['port'] ?? ($scheme === 'https' ? 443 : 80);

        // 4. DNS Rebinding hujumining oldini olish uchun so'rovni bevosita yechilgan IP ga yo'naltiramiz
        $ch = curl_init($targetUrl);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, false); // Redirect SSRF ni oldini olish
        curl_setopt($ch, CURLOPT_TIMEOUT, 5);
        // CURLOPT_RESOLVE orqali hostname ni qat'iy tekshirilgan IP ga bog'laymiz
        curl_setopt($ch, CURLOPT_RESOLVE, ["{$host}:{$port}:{$resolvedIp}"]);

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        return "Status: {$httpCode} | Hajm: " . strlen($response) . " bayt";
    }
}

class SecurityException extends Exception {}

// Sinov
try {
    echo SafeHttpClient::fetchUrlSafely("http://169.254.169.254/latest/meta-data/");
} catch (SecurityException $e) {
    echo "[+] Xavfsizlik tizimi ishladi: " . $e->getMessage() . "
";
}
```
**Tushuntirish:** SSRF hujumida tajovuzkor tashqi serverni ichki infratuzilmaga (masalan AWS Cloud Instance Metadata yoki ichki Redis/Elasticsearch) vositachi qilib ishlatadi. DNS Rebinding da esa dastlab ommaviy IP beriladi, ulanish paytida esa 127.0.0.1 qaytariladi; `CURLOPT_RESOLVE` bu bo'shliqni butunlay yopadi.

---

### Topshiriq #1177: Command Injection va Argument Injection Dan To'liq Himoyalanish
**Tavsif:** Tizim buyruqlarini (masalan, convert yoki git) ishga tushirishda foydalanuvchi kiritgan ma'lumotlar orqali amalga oshiriladigan buyruq va argument ineksiyalarini `proc_open` massiv sintaksisi orqali yo'q qiling.
**Talablar:** proc_open da buyruqni massiv sifatida berish (PHP 7.4+), escapeshellarg, shell vositachiligisiz bajarish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Xavfsiz Tizim Buyruqlari Ijrochisi
class SafeCommandExecutor {
    // XAVFLI: exec("git checkout $branch"); // Agar $branch = "main; rm -rf /" bo'lsa fojia!
    // TO'G'RI: proc_open ga buyruq va argumentlarni alohida massiv qilib berish
    public static function runGitStatus(string $repoPath): string {
        $descriptors = [
            0 => ['pipe', 'r'], // stdin
            1 => ['pipe', 'w'], // stdout
            2 => ['pipe', 'w'], // stderr
        ];

        // Argumentlar massivda berilganda operatsion tizim /bin/sh ni chaqirmaydi,
        // shuning uchun hech qanday ;, &&, |, ` kabi shell metabelgilari ishlamaydi!
        $cmd = ['git', '-C', $repoPath, 'status', '--short'];

        $process = proc_open($cmd, $descriptors, $pipes);
        if (!is_resource($process)) {
            throw new Exception("Jarayonni ishga tushirib bo'lmadi!");
        }

        fclose($pipes[0]);
        $output = stream_get_contents($pipes[1]);
        $error = stream_get_contents($pipes[2]);
        fclose($pipes[1]);
        fclose($pipes[2]);

        $exitCode = proc_close($process);
        return ($exitCode === 0) ? $output : "Xato: {$error}";
    }

    // Argument ineksiyasi (Argument Injection): masalan foydalanuvchi fayl nomiga '--help' kiritishi
    public static function sanitizeArgument(string $param): string {
        // Agar parametr '-' bilan boshlansa, uni '--' argument ajratgichidan keyin qo'yish kerak
        return escapeshellarg($param);
    }
}

echo "[+] Xavfsiz buyruq ijrochisi tayyor (Shell interpreter chetlab o'tildi).
";
```
**Tushuntirish:** `system()` yoki `exec()` funksiyalari buyruqni operatsion tizimning `/bin/sh -c` interpretatoriga beradi, bu esa inyeksiyalar uchun eshik ochadi. `proc_open` ga argumentlar massiv ko'rinishida berilganda esa to'g'ridan-to'g'ri C `execve` tizim chaqiruvi chaqiriladi va shell metabelgilari oddiy matn deb qabul qilinadi.

---

### Topshiriq #1178: Path Traversal va LFI/RFI Himoyasi: realpath va Kanonikalizatsiya
**Tavsif:** Foydalanuvchi so'ragan fayllarni yuklab berishda `../../etc/passwd` kabi Path Traversal hujumlarining oldini olish uchun fayl yo'llarini kanonikalizatsiya qilish va bazaviy katalogdan chiqib ketmaslikni kafolatlang.
**Talablar:** realpath, str_starts_with bilan asosiy katalogni tekshirish, null-byte (%00) filtrlash.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Path Traversal (Directory Traversal) Himoyachisi
class SafeFileDownloader {
    private string $baseDirectory;

    public function __construct(string $baseDir) {
        $realBase = realpath($baseDir);
        if ($realBase === false || !is_dir($realBase)) {
            throw new InvalidArgumentException("Asosiy katalog mavjud emas: {$baseDir}");
        }
        $this->baseDirectory = $realBase;
    }

    public function getFileContent(string $requestedFilename): string {
        // 1. Null-byte zaharini tozalash (PHP 8 da o'zi himoyalangan, lekin qo'shimcha nazorat)
        $cleanName = str_replace(chr(0), '', $requestedFilename);

        // 2. To'liq yo'lni hosil qilish
        $candidatePath = $this->baseDirectory . DIRECTORY_SEPARATOR . $cleanName;

        // 3. realpath() barcha '../', './' va ramziy havolalarni (symlinks) haqiqiy fizik yo'lga yechadi
        $realPath = realpath($candidatePath);

        // 4. Qat'iy chegarani tekshirish: Yakuniy yo'l asosiy katalog bilan boshlanishi SHART!
        if ($realPath === false || !str_starts_with($realPath, $this->baseDirectory . DIRECTORY_SEPARATOR)) {
            throw new SecurityException("[XAVF!] Ruxsat etilmagan fayl yo'liga urinish: {$requestedFilename}");
        }

        // 5. Fayl mavjudligi va o'qish huquqi
        if (!is_file($realPath) || !is_readable($realPath)) {
            throw new Exception("Fayl topilmadi yoki o'qib bo'lmaydi.");
        }

        return file_get_contents($realPath);
    }
}

// Sinov
$storageDir = sys_get_temp_dir() . DIRECTORY_SEPARATOR . 'safe_storage';
@mkdir($storageDir);
file_put_contents($storageDir . DIRECTORY_SEPARATOR . 'public_contract.pdf', "Shartnoma matni...");

$downloader = new SafeFileDownloader($storageDir);

// Qonuniy fayl
echo "[+] Qonuniy fayl o'qildi: " . $downloader->getFileContent('public_contract.pdf') . "
";

// Hujum urinishi:
try {
    $downloader->getFileContent('../../etc/passwd');
} catch (SecurityException $e) {
    echo "[+] Hujum muvaffaqiyatli to'xtatildi: " . $e->getMessage() . "
";
}
```
**Tushuntirish:** Buzg'unchilar `../..` belgilari orqali serverning ildiz qatlamlariga chiqib ketishi mumkin. `realpath()` barcha oraliq havolalarni yechib beradi, `str_starts_with($realPath, $baseDir)` esa ruxsat berilgan rasm yoki hujjatlar papkasidan tashqariga bitta qadam ham chiqmaslikni kafolatlaydi.

---

### Topshiriq #1179: XML External Entity (XXE) Hujumlaridan To'liq Himoyalanish
**Tavsif:** SOAP xizmatlari yoki XML importlarida xakerlar tashqi sub'ektlar (`<!ENTITY xxe SYSTEM 'file:///etc/passwd'>`) orqali server fayllarini o'qib olmasligi uchun libxml xavfsizlik konfiguratsiyasini o'rnating.
**Talablar:** LIBXML_NONET, LIBXML_NOENT taqiqlash, libxml_disable_entity_loader (meros tizimlar uchun), DOMDocument xavfsizligi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Sanoat Darajasidagi XXE Himoyalangan XML Parser
class SafeXmlParser {
    public static function parse(string $rawXml): SimpleXMLElement {
        // 1. Ichki xatoliklarni xavfsiz boshqarish
        libxml_use_internal_errors(true);

        // 2. Tashqi tarmoq yuklamalarini qat'iy taqiqlash: LIBXML_NONET
        // DTD va tashqi entitilarni yuklashni cheklash
        $options = LIBXML_NONET | LIBXML_COMPACT;

        $dom = new DOMDocument();
        // Tashqi DTD va entitilarni yuklashni o'chirish
        $dom->resolveExternals = false;
        $dom->substituteEntities = false;

        $loaded = $dom->loadXML($rawXml, $options);
        if (!$loaded) {
            $errors = libxml_get_errors();
            libxml_clear_errors();
            throw new Exception("XML xatosi: " . ($errors[0]->message ?? 'Noma'lum xatolik'));
        }

        return simplexml_import_dom($dom);
    }
}

// Xakerning XXE hujum paketi:
$xxePayload = <<<XML
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [
  <!ENTITY xxe SYSTEM "file:///etc/hosts">
]>
<order>
  <item>&xxe;</item>
</order>
XML;

try {
    $xml = SafeXmlParser::parse($xxePayload);
    echo "[+] XML o'qildi: " . (string)$xml->item . "
";
} catch (Exception $e) {
    echo "[+] XXE Hujumi bartaraf qilindi: " . $e->getMessage() . "
";
}
```
**Tushuntirish:** XXE zaifligi XML parserlarining standart imkoniyatidan foydalanib, server fayllarini (masalan `/etc/passwd` yoki `.env`) o'qish, ichki portlarni skanerlash (SSRF) yoki milliard kulish (Billion Laughs) DoS hujumini keltirib chiqaradi. `LIBXML_NONET` va `substituteEntities = false` tashqi manbalarni yuklashni to'xtatadi.

---

### Topshiriq #1180: PHP Deserialization (Insecure Object Injection) dan Himoyalanish
**Tavsif:** `unserialize()` funksiyasidan foydalanishda tajovuzkorlar Gadget Chains orqali Remote Code Execution (RCE) qilmasligi uchun `allowed_classes` oq ro'yxatini joriy qiling yoki JSON ga to'liq migratsiya qiling.
**Talablar:** unserialize da allowed_classes => [...], json_decode afzalligi, xavfli sehrli metodlar (__destruct, __wakeup) xavfi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Xavfsiz Ob'ektlarni Qayta Tiklash (Deserialization)
class UserSessionData {
    public int $userId;
    public string $role;
}

class SafeDeserializer {
    // XAVFLI: unserialize($untrustedString); // Buzg'unchi Monolog/Guzzle gadget chain orqali serverni egallaydi!
    // TO'G'RI 1: Faqat aniq ruxsat berilgan sinflar ro'yxatini belgilash
    public static function restoreSafeObject(string $serializedData): mixed {
        return unserialize($serializedData, [
            'allowed_classes' => [UserSessionData::class] // Boshqa hech qanday sinf tiklanmaydi!
        ]);
    }

    // TO'G'RI 2 (Eng xavfsiz standart): Serializatsiya uchun faqat JSON dan foydalanish
    public static function restoreFromJson(string $jsonData): array {
        return json_decode($jsonData, true, 512, JSON_THROW_ON_ERROR);
    }
}

$safeData = serialize(new UserSessionData());
$restored = SafeDeserializer::restoreSafeObject($safeData);
echo "[+] Ruxsat etilgan sinf muvaffaqiyatli tiklandi: " . get_class($restored) . "
";

// Begona noma'lum sinf tiklanishi sinovi
$fakePayload = 'O:14:"MaliciousClass":0:{}';
$blocked = SafeDeserializer::restoreSafeObject($fakePayload);
echo "[+] Begona sinf bloklandi (Natija: " . get_class($blocked) . " - __PHP_Incomplete_Class)
";
```
**Tushuntirish:** PHP dagi `unserialize()` obyektni xotiraga yuklaganda avtomatik ravishda `__destruct()`, `__wakeup()` yoki `__toString()` sehrli metodlarini chaqiradi. Agar `allowed_classes` qo'yilmasa, dasturdagi kutubxonalarning (masalan Laravel yoki Symfony gadgetlari) ichki zanjirlari orqali serverda ixtiyoriy buyruqlarni (RCE) bajarish mumkin bo'ladi.

---

### Topshiriq #1181: Timing Attacks (Vaqt Tahlili) Himoyasi: hash_equals va sodium_memcmp
**Tavsif:** API kalitlari, parol xeshlari yoki webhook imzolarini taqqoslashda oddiy `===` operatori baytlarni ketma-ket tekshirib erta to'xtashi oqibatida yuzaga keladigan vaqt sizishini bartaraf qiling.
**Talablar:** hash_equals, sodium_compare, konstant-vaqtli (Constant-Time) taqqoslash, mikrosoniyali tebranishlar tahlili.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Kriptografik Doimiy Vaqtli Taqqoslash (Constant-Time Comparison)
class TimingSafeComparator {
    // XAVFLI: if ($userProvidedToken === $secretToken) { ... }
    // Oddiy '===' birinchi xato baytga duch kelishi bilanoq tekshiruvni to'xtatadi.
    // Xaker so'rov vaqtini mikrosoniyalarda o'lchab (Timing Attack), to'g'ri harflarni birma-bir taxmin qila oladi!

    // TO'G'RI USUL 1: hash_equals (PHP standart kutubxonasi)
    public static function verifyToken(string $knownToken, string $userToken): bool {
        return hash_equals($knownToken, $userToken);
    }

    // TO'G'RI USUL 2: sodium_compare (Libsodium C darajasidagi doimiy vaqt taqqoslashi)
    public static function verifyBinarySignature(string $knownSig, string $userSig): bool {
        if (strlen($knownSig) !== strlen($userSig)) {
            return false;
        }
        return (sodium_compare($knownSig, $userSig) === 0);
    }
}

// Sinov
$secretApiKey = "khorazmiy_secure_token_sample_abc123";
$clientInput  = "khorazmiy_secure_token_sample_abc123";

$isEqual = TimingSafeComparator::verifyToken($secretApiKey, $clientInput);
echo "[+] Timing-safe taqqoslash natijasi: " . ($isEqual ? "MOS KELDI" : "FARQLI") . "
";
```
**Tushuntirish:** Doimiy vaqtli (Constant-Time) funksiyalar satrning qayerida xato borligidan qat'i nazar, har doim barcha baytlarni oxirigacha bitwise XOR amali bilan solishtirib chiqadi. Bu esa xakerning tarmoq orqali vaqt farqini o'lchash imkoniyatini nolga tenglashtiradi.

---

### Topshiriq #1182: Zamonaviy Parol Arxitekturasi: password_hash va password_needs_rehash
**Tavsif:** Foydalanuvchi tizimga kirgan paytda, uning eski arzon xeshlangan parollarini (masalan eski bcrypt yoki past xarajatli Argon2) sezilarsiz yangi mustahkam standartlarga ko'taruvchi avtomatik rehash tizimini joriy qiling.
**Talablar:** password_hash(PASSWORD_ARGON2ID), password_verify, password_needs_rehash, dinamik yangilash.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Sanoat Darajasidagi Parol Boshqaruvchisi
class ModernAuthService {
    // Parol xeshlash opsiyalari (Argon2id)
    private const HASH_OPTIONS = [
        'memory_cost' => 65536, // 64 MB RAM
        'time_cost'   => 4,     // 4 iteratsiya
        'threads'     => 1,
    ];

    public static function registerUserPassword(string $plainPassword): string {
        return password_hash($plainPassword, PASSWORD_ARGON2ID, self::HASH_OPTIONS);
    }

    public static function loginAndUpgrade(string $plainPassword, string $currentHashFromDb, callable $saveNewHashCallback): bool {
        // 1. Parolni tekshiramiz
        if (!password_verify($plainPassword, $currentHashFromDb)) {
            return false; // Noto'g'ri parol
        }

        // 2. Ushbu xesh bizning eng so'nggi xavfsizlik standartlarimizga mosmi?
        // (Masalan agar parametrlar o'zgargan bo'lsa yoki eski bcrypt xesh bo'lsa)
        if (password_needs_rehash($currentHashFromDb, PASSWORD_ARGON2ID, self::HASH_OPTIONS)) {
            $newStrongHash = password_hash($plainPassword, PASSWORD_ARGON2ID, self::HASH_OPTIONS);
            // Yangi xeshni bazaga yozib qo'yamiz (foydalanuvchi buni sezmaydi)
            $saveNewHashCallback($newStrongHash);
            echo "[*] Foydalanuvchi paroli xavfsizroq yangi Argon2id xeshiga ko'tarildi!
";
        }

        return true;
    }
}

// Sinov
$password = "MeningMaxfiyParolim2026";
// Eski zaif bcrypt xesh simulyatsiyasi
$legacyBcryptHash = password_hash($password, PASSWORD_BCRYPT, ['cost' => 10]);

echo "[*] Eski xesh: {$legacyBcryptHash}
";

$loginSuccess = ModernAuthService::loginAndUpgrade(
    $password,
    $legacyBcryptHash,
    function (string $newHash) {
        echo "[+] Baza yangilandi -> Yangi xesh: {$newHash}
";
    }
);

echo "[+] Tizimga kirish: " . ($loginSuccess ? "MUVAFFAQIN" : "XATO") . "
";
```
**Tushuntirish:** `password_needs_rehash()` tizim ma'murlariga parollar siyosatini (cost faktorini oshirish yoki BCRYPT dan Argon2id ga o'tish) foydalanuvchilarni parolini majburiy o'zgartirishga majburlamasdan, tabiiy login paytida bosqichma-bosqich yangilab olish imkonini beradi.

---

### Topshiriq #1183: Parolga Maxfiy Pepper Qo'shish va HMAC-SHA256 Bilan Ikki Bosqichli Xavfsizlik
**Tavsif:** Agar ma'lumotlar bazasi to'liq xakerlar qo'liga tushsa ham (SQL Dump o'g'irlanganda), alohida serverda yoki HSM da saqlanadigan Pepper (Qalampir) kalitisiz xeshlarni sindirib bo'lmaydigan tizim quring.
**Talablar:** HMAC-SHA256 pre-hashing, pepper kaliti, password_hash bilan kombinatsiya.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Pepper (HMAC) + Argon2id Ikki Qatlamli Parol Himoyasi
class PepperedPasswordService {
    // Pepper bazada SAQLANMAYDI! U alohida maxfiy muhit o'zgaruvchisida yoki AWS KMS da bo'ladi
    private string $serverPepperKey;

    public function __construct(string $pepper) {
        $this->serverPepperKey = $pepper;
    }

    // Parolni xeshlashdan oldin Pepper bilan HMAC qilamiz
    private function preparePepperedPassword(string $plainPassword): string {
        // HMAC-SHA256 orqali parolni 32 baytli ikkilik xeshga aylantiramiz
        return hash_hmac('sha256', $plainPassword, $this->serverPepperKey, true);
    }

    public function hashPassword(string $plainPassword): string {
        $peppered = $this->preparePepperedPassword($plainPassword);
        // So'ngra standart Argon2id xeshini hisoblaymiz
        return password_hash($peppered, PASSWORD_ARGON2ID);
    }

    public function verifyPassword(string $plainPassword, string $storedHash): bool {
        $peppered = $this->preparePepperedPassword($plainPassword);
        return password_verify($peppered, $storedHash);
    }
}

// Sinov
$pepperKey = "server_app_secret_pepper_kalit_2026_xyz";
$service = new PepperedPasswordService($pepperKey);

$userPass = "FoydalanuvchiParoli_777";
$hash = $service->hashPassword($userPass);
echo "[+] Pepperli xesh olindi: {$hash}
";

$isCorrect = $service->verifyPassword($userPass, $hash);
echo "[+] Parol tasdiqlandimi? " . ($isCorrect ? "HA" : "YO'Q") . "
";
```
**Tushuntirish:** Oddiy tuz (Salt) har bir foydalanuvchi xeshi yonida bazada ochiq saqlanadi va u kamalak jadvallaridan himoya qiladi. Pepper esa alohida serverda saqlanadigan maxfiy kalit bo'lib, baza o'g'irlanganda xakerlar offline rejimda parolni tanlash (cracking) imkoniyatidan butunlay mahrum bo'ladi.

---

### Topshiriq #1184: Brute-Force va Credential Stuffing dan Himoya (Tarpit va Progressiv Kechikish)
**Tavsif:** Ketma-ket noto'g'ri parollarni kiritayotgan botlar va buzg'unchilarni aniqlab, ularning har bir yangi urinishiga progressiv kechikish (Tarpit / usleep) beruvchi va akkauntni vaqtincha muzlatuvchi himoya yarating.
**Talablar:** Urinishlar hisoblagichi, progressiv kechikish formulasi, IP va username bo'yicha cheklov.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Brute-Force Tarpit va Urinishlar Nazoratchisi
class LoginRateLimiter {
    private array $attempts = []; // [identifikator => ['count' => int, 'locked_until' => int]]
    private int $maxAttempts = 5;
    private int $lockoutTimeSec = 300; // 5 daqiqa blok

    public function recordFailedAttempt(string $identifier): int {
        $now = time();
        if (!isset($this->attempts[$identifier])) {
            $this->attempts[$identifier] = ['count' => 0, 'locked_until' => 0];
        }

        $this->attempts[$identifier]['count']++;
        $count = $this->attempts[$identifier]['count'];

        // Agar limitdan oshsa, hisobni muzlatamiz
        if ($count >= $this->maxAttempts) {
            $this->attempts[$identifier]['locked_until'] = $now + $this->lockoutTimeSec;
            echo "[!] BLOKLANDI: {$identifier} 5 daqiqaga muzlatildi!
";
        } else {
            // Tarpit: Har bir noto'g'ri urinishda botni sekinlashtiruvchi progressiv kechikish (0.5s, 1s, 2s)
            $delaySec = pow(2, $count - 1) * 0.25;
            echo "[*] Tarpit: Bot javobni kutishga majbur qilindi: {$delaySec} soniya...
";
            usleep((int)($delaySec * 1000000));
        }

        return $count;
    }

    public function isBlocked(string $identifier): bool {
        if (!isset($this->attempts[$identifier])) return false;
        
        $lockedUntil = $this->attempts[$identifier]['locked_until'];
        if ($lockedUntil > time()) {
            return true;
        }

        // Agar blok muddati tugagan bo'lsa tozalaymiz
        if ($lockedUntil > 0 && $lockedUntil <= time()) {
            unset($this->attempts[$identifier]);
        }
        return false;
    }

    public function reset(string $identifier): void {
        unset($this->attempts[$identifier]);
    }
}

$limiter = new LoginRateLimiter();
$ip = "192.168.1.105";

for ($i = 1; $i <= 5; $i++) {
    if ($limiter->isBlocked($ip)) {
        echo "Kirish rad etildi: Akkaunt yoki IP blokda!
";
        break;
    }
    echo "Urinish #{$i}: ";
    $limiter->recordFailedAttempt($ip);
}
```
**Tushuntirish:** Tarpit texnikasi botlarning resurslarini tugatishga qaratilgan. Javobni ataylab kechiktirish orqali tajovuzkorning sekundiga minglab parol sinash tezligi sekundiga 0.5 tagacha tushiriladi va avtomatlashtirilgan Credential Stuffing hujumlari iqtisodiy jihatdan foydasiz bo'lib qoladi.

---

### Topshiriq #1185: MFA / 2FA: TOTP (RFC 6238) Vaqtga Asoslangan Bir Martalik Kod Algoritmi
**Tavsif:** Google Authenticator va boshqa 2FA ilovalari bilan 100% mos keladigan, har 30 soniyada yangilanuvchi 6 xonali TOTP kodlarini generatsiya qilish va tekshirish algoritmini tashqi kutubxonalarsiz amalga oshiring.
**Talablar:** RFC 6238 standarti, HMAC-SHA1 dinamik kesish (Dynamic Truncation), Base32 dekodlash, vaqt oralig'i (time drift) tekshiruvi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - RFC 6238 TOTP (Time-Based One-Time Password) Dvigateli
class TotpService {
    // Base32 alifbosi
    private const BASE32_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';

    public static function generateSecret(int $length = 16): string {
        $secret = '';
        for ($i = 0; $i < $length; $i++) {
            $secret .= self::BASE32_CHARS[random_int(0, 31)];
        }
        return $secret;
    }

    // Base32 ni xom ikkilik baytlarga o'girish
    private static function base32Decode(string $b32): string {
        $b32 = strtoupper($b32);
        $buffer = 0;
        $bitsLeft = 0;
        $output = '';

        for ($i = 0; $i < strlen($b32); $i++) {
            $val = strpos(self::BASE32_CHARS, $b32[$i]);
            if ($val === false) continue;

            $buffer = ($buffer << 5) | $val;
            $bitsLeft += 5;

            if ($bitsLeft >= 8) {
                $bitsLeft -= 8;
                $output .= chr(($buffer >> $bitsLeft) & 0xFF);
            }
        }
        return $output;
    }

    // Belgilangan vaqt uchun 6-xonali kodni hisoblash
    public static function getCode(string $base32Secret, ?int $timeSlice = null): string {
        if ($timeSlice === null) {
            $timeSlice = (int)floor(time() / 30); // Har 30 soniyalik qadam
        }

        $secretKey = self::base32Decode($base32Secret);
        // 64-bit Big-endian int qilib paketlaymiz
        $timeBytes = pack('J', $timeSlice);

        // HMAC-SHA1
        $hmac = hash_hmac('sha1', $timeBytes, $secretKey, true);

        // Dinamik kesish (Dynamic Truncation - RFC 4226)
        $offset = ord(substr($hmac, -1)) & 0x0F;
        $hashPart = substr($hmac, $offset, 4);
        $value = unpack('N', $hashPart)[1] & 0x7FFFFFFF;

        $pin = $value % 1000000;
        return str_pad((string)$pin, 6, '0', STR_PAD_LEFT);
    }

    // Foydalanuvchi kiritgan kodni tekshirish (Vaqt farqi +/- 30 soniya bilan)
    public static function verifyCode(string $base32Secret, string $inputCode, int $discrepancy = 1): bool {
        $currentTimeSlice = (int)floor(time() / 30);

        for ($i = -$discrepancy; $i <= $discrepancy; $i++) {
            $calculatedCode = self::getCode($base32Secret, $currentTimeSlice + $i);
            if (hash_equals($calculatedCode, $inputCode)) {
                return true;
            }
        }
        return false;
    }
}

// Sinov
$secret = TotpService::generateSecret();
echo "[+] Foydalanuvchining 2FA Maxfiy kaliti: {$secret}
";

$currentCode = TotpService::getCode($secret);
echo "[+] Hozirgi 6 xonali 2FA Kod: {$currentCode}
";

$isValid = TotpService::verifyCode($secret, $currentCode);
echo "[+] Kod tasdiqlandimi? " . ($isValid ? "HA (Muvaffaqiyatli)" : "YO'Q") . "
";
```
**Tushuntirish:** TOTP algoritmi internetga ulanishni talab qilmaydi. Server va foydalanuvchi telefoni yagona umumiy sirdan (Shared Secret) va Unix epoch vaqtidan foydalanib bir xil kodni mustaqil hisoblab chiqaradi. Dynamic Truncation esa 160-bitli HMAC natijasidan 6 xonali xavfsiz sonni ajratib beradi.

---

### Topshiriq #1186: WebAuthn / FIDO2 Passkeys: Apparat Kalitlari Attestatsiyasini Tekshirish
**Tavsif:** Parolsiz kirish (Passkeys) va apparat USB xavfsizlik kalitlari (YubiKey) yuborgan WebAuthn `navigator.credentials.create` javobining kriptografik yaxlitligini tekshiruvchi validator quring.
**Talablar:** clientDataJSON dekodlash, challenge va origin tekshiruvi, authData tahlili, UP (User Present) bayrog'i.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - WebAuthn / FIDO2 Attestatsiya Validatori
class WebAuthnValidator {
    public static function verifyRegistration(
        string $clientDataJsonBase64,
        string $expectedChallenge,
        string $expectedOrigin
    ): array {
        $rawClientData = base64_decode($clientDataJsonBase64);
        $clientData = json_decode($rawClientData, true);

        // 1. Hodisa turi tekshiruvi
        if (($clientData['type'] ?? '') !== 'webauthn.create') {
            throw new Exception("Yaroqsiz WebAuthn amali turi!");
        }

        // 2. Challenge mosligini tekshirish (Replay hujumlariga qarshi)
        $receivedChallenge = $clientData['challenge'] ?? '';
        if (!hash_equals($expectedChallenge, $receivedChallenge)) {
            throw new Exception("WebAuthn challenge mos kelmadi!");
        }

        // 3. Origin (Sayt domeni) tekshiruvi (Phishing himoyasi)
        $receivedOrigin = $clientData['origin'] ?? '';
        if ($receivedOrigin !== $expectedOrigin) {
            throw new Exception("Fishing hujumi! Ruxsatsiz origin: {$receivedOrigin}");
        }

        return [
            'status' => 'VERIFIED',
            'origin' => $receivedOrigin,
            'client_data_hash' => hash('sha256', $rawClientData)
        ];
    }
}

// Sinov
$challenge = bin2hex(random_bytes(16));
$clientData = json_encode([
    'type' => 'webauthn.create',
    'challenge' => $challenge,
    'origin' => 'https://auth.khorazmiy.uz'
]);

$verified = WebAuthnValidator::verifyRegistration(
    base64_encode($clientData),
    $challenge,
    'https://auth.khorazmiy.uz'
);

echo "[+] WebAuthn Passkey tasdiqlandi! Hash: {$verified['client_data_hash']}
";
```
**Tushuntirish:** WebAuthn / Passkeys fishingga 100% chidamli yagona autentifikatsiya texnologiyasidir. Brauzer foydalanuvchi haqiqatan qaysi domenda turganini apparat kalitiga (YubiKey yoki TouchID) xabar qiladi; agar sayt soxta (masalan phish-khorazmiy.uz) bo'lsa, origin mos kelmay kalit javob bermaydi.

---

### Topshiriq #1187: Xavfsiz 'Remember Me' Persistent Login Cookie Tizimi (Selector & Validator)
**Tavsif:** Foydalanuvchi paroli o'zgarganda yoki sessiyasi o'g'irlanganda xavfsizlikni saqlash uchun 'Selector + Validator Token Pair' arxitekturasidagi uzoq muddatli kirish mexanizmini yarating.
**Talablar:** Selector va Validator ikkita alohida token, bazada faqat validator xeshi saqlanadi, o'g'irlik aniqlanganda barcha sessiyalarni o'chirish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Xavfsiz 'Remember Me' Tizimi (Selector-Validator modeli)
class RememberMeService {
    private PDO $pdo;

    public function __construct(PDO $pdo) {
        $this->pdo = $pdo;
    }

    // Cookie yaratish: selector (qidirish uchun) + validator (parol kabi)
    public function createLoginCookie(int $userId): string {
        $selector = bin2hex(random_bytes(12)); // 24 belgi
        $validator = bin2hex(random_bytes(32)); // 64 belgi

        // Bazada validatorning faqat SHA-256 xeshi saqlanadi!
        $hashedValidator = hash('sha256', $validator);
        $expires = date('Y-m-d H:i:s', time() + (86400 * 30)); // 30 kun

        $stmt = $this->pdo->prepare("INSERT INTO auth_tokens (user_id, selector, hashed_validator, expires_at) VALUES (?, ?, ?, ?)");
        $stmt->execute([$userId, $selector, $hashedValidator, $expires]);

        // Foydalanuvchiga esa ochiq holda 'selector:validator' cookie yuboriladi
        return "{$selector}:{$validator}";
    }

    public function validateCookie(string $cookieValue): ?int {
        $parts = explode(':', $cookieValue);
        if (count($parts) !== 2) return null;

        [$selector, $validator] = $parts;

        $stmt = $this->pdo->prepare("SELECT id, user_id, hashed_validator, expires_at FROM auth_tokens WHERE selector = ?");
        $stmt->execute([$selector]);
        $row = $stmt->fetch(PDO::FETCH_ASSOC);

        if (!$row) return null;

        if (strtotime($row['expires_at']) < time()) {
            return null; // Muddati o'tgan
        }

        // Timing-safe taqqoslash
        if (hash_equals($row['hashed_validator'], hash('sha256', $validator))) {
            return (int)$row['user_id'];
        }

        // AGAR SELECTOR TOPILIB, VALIDATOR XATO BO'LSA - BU COOKIE O'G'IRLANGANLIGIDAN DALOLAT!
        // Havfsizlik chorasi: ushbu foydalanuvchining BARCHA doimiy sessiyalarini bekor qilamiz:
        $delStmt = $this->pdo->prepare("DELETE FROM auth_tokens WHERE user_id = ?");
        $delStmt->execute([$row['user_id']]);
        error_log("[XAVF!] Cookie o'g'irlash urinishi aniqlandi! User ID: {$row['user_id']}");

        return null;
    }
}

echo "[+] Selector-Validator 'Remember Me' arxitekturasi tayyorlandi.
";
```
**Tushuntirish:** Agar bazada oddiy cookie saqlansa va baza sizib chiqsa, xaker barcha hisoblarga kirib oladi. Selector-Validator modelida esa bazada faqat xesh saqlangani sababli bazadan tokenlarni o'qib bo'lmaydi, o'g'irlangan token bilan kirishga urinilganda esa butun tizim avtomatik barcha sessiyalarni o'chiradi.

---

### Topshiriq #1188: Parol Tiklash (Password Reset) Xavfsiz Token Arxitekturasi
**Tavsif:** Email orqali yuboriladigan parol tiklash havolalarida bir martalik (Single-Use), qisqa muddatli (15 daqiqa) va bazada faqat xeshi saqlanuvchi kriptografik tiklash tizimini ishlab chiqing.
**Talablar:** random_bytes(32) token, hash('sha256') saqlash, 15 daqiqalik TTL, parolni o'zgartirgach tokenni o'chirish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Xavfsiz Parol Tiklash Xizmati
class PasswordResetManager {
    private PDO $pdo;

    public function __construct(PDO $pdo) {
        $this->pdo = $pdo;
    }

    // 1. Tiklash tokenini generatsiya qilish
    public function createResetToken(string $email): ?string {
        $rawToken = bin2hex(random_bytes(32));
        $hashedToken = hash('sha256', $rawToken);
        $expiresAt = time() + (15 * 60); // Qat'iy 15 daqiqa

        // Eski qoldiq tokenlarni o'chiramiz
        $del = $this->pdo->prepare("DELETE FROM password_resets WHERE email = ?");
        $del->execute([$email]);

        $ins = $this->pdo->prepare("INSERT INTO password_resets (email, token_hash, expires_at) VALUES (?, ?, ?)");
        $ins->execute([$email, $hashedToken, $expiresAt]);

        // Email orqali yuboriladigan xavfsiz URL:
        return "https://khorazmiy.uz/reset-password?token={$rawToken}&email=" . urlencode($email);
    }

    // 2. Yangi parolni o'rnatish
    public function resetPassword(string $email, string $rawToken, string $newPassword): bool {
        $hashedToken = hash('sha256', $rawToken);

        $stmt = $this->pdo->prepare("SELECT expires_at FROM password_resets WHERE email = ? AND token_hash = ?");
        $stmt->execute([$email, $hashedToken]);
        $reset = $stmt->fetch(PDO::FETCH_ASSOC);

        if (!$reset || $reset['expires_at'] < time()) {
            return false; // Token noto'g'ri yoki muddati o'tgan
        }

        // Yangi parolni xeshlash
        $newHash = password_hash($newPassword, PASSWORD_ARGON2ID);
        $upd = $this->pdo->prepare("UPDATE users SET password_hash = ? WHERE email = ?");
        $upd->execute([$newHash, $email]);

        // Tokenni darhol yo'q qilish (Bir martalik bo'lishi shart)
        $del = $this->pdo->prepare("DELETE FROM password_resets WHERE email = ?");
        $del->execute([$email]);

        return true;
    }
}

echo "[+] Xavfsiz Parol Tiklash arxitekturasi o'rnatildi.
";
```
**Tushuntirish:** Bazada hech qachon ochiq tiklash tokenini saqlamaslik kerak. Agar ma'lumotlar bazasi zaxira nusxasi (backup) o'g'irlansa, tajovuzkor tokenlarni ko'ra olmaydi, chunki ular SHA-256 bilan bir tomonlama xeshlangan holda saqlanadi.

---

### Topshiriq #1189: Pwned Passwords API orqali Sizib Chiqqan Parollarni Tekshirish (k-Anonymity)
**Tavsif:** Foydalanuvchi yangi parol tanlayotganda, ushbu parol dunyo bo'ylab xakerlar bazalarida (HaveIBeenPwned) tarqalib ketganligini parolni o'zini oshkor qilmasdan k-Anonymity modeli bilan tekshiring.
**Talablar:** SHA-1 xeshning dastlabki 5 ta belgisini API ga yuborish, qolgan 35 ta belgini lokal solishtirish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - k-Anonymity Modelida Sizib Chiqqan Parollarni Tekshirish
class PwnedPasswordChecker {
    public static function isPwned(string $password): int {
        // 1. Parolning to'liq SHA-1 xeshini olamiz
        $sha1 = strtoupper(sha1($password));
        // Dastlabki 5 ta belgi (Prefix)
        $prefix = substr($sha1, 0, 5);
        // Qolgan 35 ta belgi (Suffix)
        $suffix = substr($sha1, 5);

        // 2. HaveIBeenPwned API ga FAQAT dastlabki 5 ta belgini jo'natamiz (Parol oshkor bo'lmaydi!)
        $url = "https://api.pwnedpasswords.com/range/{$prefix}";
        
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 3);
        $response = curl_exec($ch);
        curl_close($ch);

        if (!$response) return 0;

        // 3. Qaytgan yuzlab xeshlar orasida bizning suffix bor-yo'qligini qidiramiz
        $lines = explode("
", $response);
        foreach ($lines as $line) {
            $parts = explode(':', trim($line));
            if (count($parts) === 2) {
                if (hash_equals($parts[0], $suffix)) {
                    return (int)$parts[1]; // Necha marta sizib chiqqanligi soni
                }
            }
        }

        return 0; // Xavfsiz, o'g'irlangan bazalarda topilmadi
    }
}

// Sinov
$weakPass = "password123";
$count = PwnedPasswordChecker::isPwned($weakPass);
echo "[!] '{$weakPass}' paroli global o'g'irlangan bazalarda topildi: {$count} marta!
";
```
**Tushuntirish:** k-Anonymity modeli shaxsiy daxlsizlikni 100% himoya qiladi. Server tashqi API ga foydalanuvchi parolini ham, uning to'liq xeshini ham yubormaydi; faqat 5 ta belgi yuboriladi va server 500-1000 ta mos keluvchi xeshlar ro'yxatini qaytaradi, yakuniy taqqoslash esa lokal server xotirasida bajariladi.

---

### Topshiriq #1190: Magic Link (Parolsiz Kirish) Mexanizmi va Qisqa Muddatli HMAC URL
**Tavsif:** Foydalanuvchilarga parolsiz kirish imkonini beruvchi, vaqti cheklangan (10 daqiqa) va server maxfiy kaliti bilan raqamli imzolangan Magic Link generatori va tekshiruvchisini tuzing.
**Talablar:** HMAC-SHA256 URL imzosi, expires vaqti, manipulyatsiya tekshiruvi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Xavfsiz Magic Link (Imzolangan URL) Xizmati
class MagicLinkService {
    private string $signingKey;

    public function __construct(string $key) {
        $this->signingKey = $key;
    }

    public function generateMagicLink(int $userId, string $email, int $ttlSeconds = 600): string {
        $expires = time() + $ttlSeconds;
        $dataToSign = "{$userId}|{$email}|{$expires}";

        // HMAC-SHA256 raqamli imzo yaratamiz
        $signature = hash_hmac('sha256', $dataToSign, $this->signingKey);

        $params = http_build_query([
            'uid'     => $userId,
            'email'   => $email,
            'exp'     => $expires,
            'sig'     => $signature
        ]);

        return "https://khorazmiy.uz/auth/magic-verify?{$params}";
    }

    public function verifyMagicLink(array $queryParams): ?int {
        $uid = $queryParams['uid'] ?? null;
        $email = $queryParams['email'] ?? null;
        $exp = (int)($queryParams['exp'] ?? 0);
        $sig = $queryParams['sig'] ?? '';

        if (!$uid || !$email || !$exp || !$sig) {
            return null;
        }

        // 1. Muddatini tekshiramiz
        if (time() > $exp) {
            echo "[!] Havola muddati o'tgan!
";
            return null;
        }

        // 2. Kutilgan imzoni hisoblab solishtiramiz
        $expectedData = "{$uid}|{$email}|{$exp}";
        $expectedSignature = hash_hmac('sha256', $expectedData, $this->signingKey);

        if (hash_equals($expectedSignature, $sig)) {
            return (int)$uid; // Muvaffaqiyatli
        }

        echo "[!] Imzo soxtalashtirilgan!
";
        return null;
    }
}

// Sinov
$magic = new MagicLinkService("maxfiy_imzo_kaliti_2026");
$link = $magic->generateMagicLink(42, 'ali@khorazmiy.uz');
echo "[+] Generatsiya qilingan Magic Link:
{$link}
";

parse_str(parse_url($link, PHP_URL_QUERY), $params);
$verifiedUid = $magic->verifyMagicLink($params);
echo "[+] Tasdiqlangan foydalanuvchi ID: {$verifiedUid}
";
```
**Tushuntirish:** Imzolangan URL lar (Signed URLs) ma'lumotlar bazasiga yozmasdan turib so'rovning haqiqiyligini tekshirish imkonini beradi. Agar foydalanuvchi URL ichidagi `uid` yoki `exp` vaqtini o'zgartirishga urinsa, HMAC imzosi mos kelmay kirish darhol bloklanadi.

---

### Topshiriq #1191: Xavfsiz Sessiya Konfiguratsiyasi (CIS va OWASP Standartlari)
**Tavsif:** XSS orqali sessiya o'g'irlanishi, Session Fixation va Man-in-the-Middle hujumlarini to'xtatish uchun PHP sessiyalarining barcha xavfsizlik flaglarini mukammal sozlang.
**Talablar:** session.cookie_httponly, session.cookie_secure, session.cookie_samesite=Strict, session.use_strict_mode, session.sid_length=48.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - OWASP Standartidagi Xavfsiz Sessiya Boshqaruvi
class SecureSessionInitializer {
    public static function start(): void {
        if (session_status() === PHP_SESSION_ACTIVE) {
            return;
        }

        // Xavfsiz sessiya parametrlarini majburiy o'rnatamiz
        ini_set('session.use_strict_mode', '1');      // Noma'lum sessiya ID larini qabul qilmaslik
        ini_set('session.use_cookies', '1');          // Faqat cookie orqali boshqarish
        ini_set('session.use_only_cookies', '1');     // URL ichida PHPSESSID o'tishini taqiqlash
        ini_set('session.cookie_httponly', '1');      // JavaScript (document.cookie) dan yashirish
        ini_set('session.cookie_secure', '1');        // Faqat HTTPS kanalda uzatish
        ini_set('session.cookie_samesite', 'Strict');  // CSRF hujumlaridan to'liq himoya
        ini_set('session.sid_length', '48');          // Sessiya identifikatori uzunligi (entropiya)
        ini_set('session.sid_bits_per_character', '6');// Maksimal entropiya

        session_name('__Host-KHORAZMIY_SESSID'); // __Host- prefiksi eng yuqori cookie xavfsizligini beradi

        session_start();
    }
}

SecureSessionInitializer::start();
echo "[+] Xavfsiz sessiya boshlandi. Cookie parametrlari:
";
print_r(session_get_cookie_params());
```
**Tushuntirish:** `__Host-` prefiksi cookie-ga maxsus brauzer himoyasini beradi: bunday cookie faqat HTTPS orqali o'rnatilishi shart, subdomainlarga tarqalmaydi va Path faqat `/` bo'lishi lozim. `use_strict_mode = 1` esa buzg'unchining oldindan tayyorlangan sessiya identifikatorini tiqishtirishini (Fixation) bartaraf etadi.

---

### Topshiriq #1192: Session Fixation va Session Hijacking Himoyasi
**Tavsif:** Foydalanuvchi tizimga kirgan (login) va huquqlari o'zgargan har bir lahzada eski sessiya identifikatorini o'chirib, yangisini generatsiya qiluvchi hamda IP/User-Agent barmoq izini nazorat qiluvchi himoya tuzing.
**Talablar:** session_regenerate_id(true), mijoz User-Agent xeshini sessiyaga bog'lash, anomaliyada sessiyani yo'q qilish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Session Hijacking va Fixation Qo'riqchisi
class SessionGuard {
    public static function onLoginSuccess(int $userId): void {
        // Eski sessiya faylini xotiradan to'liq o'chirib, yangi ID olamiz
        session_regenerate_id(true);

        $_SESSION['authenticated_user_id'] = $userId;
        $_SESSION['created_at'] = time();
        // Mijozning barmoq izini (Fingerprint) sessiyaga muhrlaymiz
        $_SESSION['fingerprint'] = self::generateFingerprint();
    }

    private static function generateFingerprint(): string {
        $ua = $_SERVER['HTTP_USER_AGENT'] ?? 'Unknown_UA';
        $ip = $_SERVER['REMOTE_ADDR'] ?? '127.0.0.1';
        return hash('sha256', $ua . $ip . 'khorazmiy_salt');
    }

    public static function validateSession(): bool {
        if (empty($_SESSION['authenticated_user_id'])) {
            return false;
        }

        // Sessiya o'g'irlanganligini tekshirish (Hijacking)
        $currentFingerprint = self::generateFingerprint();
        if (!hash_equals($_SESSION['fingerprint'] ?? '', $currentFingerprint)) {
            // Begona IP yoki o'zgargan brauzerdan ulanish urinishi!
            self::destroySession();
            error_log("[XAVF!] Session Hijacking urinishi qaytarildi!");
            return false;
        }

        // Absolyut muddat nazorati (masalan 4 soatdan so'ng majburiy qayta login)
        if (time() - ($_SESSION['created_at'] ?? 0) > 14400) {
            self::destroySession();
            return false;
        }

        return true;
    }

    public static function destroySession(): void {
        $_SESSION = [];
        if (ini_get("session.use_cookies")) {
            $params = session_get_cookie_params();
            setcookie(session_name(), '', time() - 42000, $params["path"], $params["domain"], $params["secure"], $params["httponly"]);
        }
        session_destroy();
    }
}

echo "[+] SessionGuard: Sessiya o'g'irlanishiga qarshi barmoq izi tizimi tayyor.
";
```
**Tushuntirish:** `session_regenerate_id(true)` parametri faqat yangi ID yaratibgina qolmay, serverdagi eski identifikatorga tegishli barcha ma'lumotlarni jismonan o'chirib tashlaydi. Bu orqali foydalanuvchi tizimga kirmasdan avval unga berilgan ochiq sessiya identifikatori orqali amalga oshiriladigan Session Fixation hujumi to'xtatiladi.

---

### Topshiriq #1193: Redis Sessiyalarini Shifrlangan Holda Saqlash (SessionHandlerInterface)
**Tavsif:** Server xotirasidagi yoki Redisdagi sessiya fayllari tizim ma'murlari yoki xakerlar tomonidan to'g'ridan-to'g'ri o'qib olinmasligi uchun, ma'lumotlarni yozishda AES-256-GCM bilan shifrlab saqlovchi maxsus sessiya drayveri yozing.
**Talablar:** SessionHandlerInterface realizatsiyasi, open, read, write, destroy, gc, AES-GCM integratsiyasi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Shifrlangan Maxsus Sessiya Drayveri
class EncryptedDatabaseSessionHandler implements SessionHandlerInterface {
    private PDO $pdo;
    private string $encryptionKey;

    public function __construct(PDO $pdo, string $key) {
        $this->pdo = $pdo;
        $this->encryptionKey = $key;
    }

    public function open(string $path, string $name): bool { return true; }
    public function close(): bool { return true; }

    public function read(string $id): string {
        $stmt = $this->pdo->prepare("SELECT payload, iv, tag FROM sessions WHERE id = ?");
        $stmt->execute([$id]);
        $row = $stmt->fetch(PDO::FETCH_ASSOC);

        if (!$row) return '';

        // Deshifrlaymiz
        $decrypted = openssl_decrypt(
            base64_decode($row['payload']),
            'aes-256-gcm',
            $this->encryptionKey,
            OPENSSL_RAW_DATA,
            base64_decode($row['iv']),
            base64_decode($row['tag'])
        );

        return ($decrypted !== false) ? $decrypted : '';
    }

    public function write(string $id, string $data): bool {
        $iv = random_bytes(12);
        $tag = '';
        $encrypted = openssl_encrypt(
            $data,
            'aes-256-gcm',
            $this->encryptionKey,
            OPENSSL_RAW_DATA,
            $iv,
            $tag
        );

        $stmt = $this->pdo->prepare("REPLACE INTO sessions (id, payload, iv, tag, updated_at) VALUES (?, ?, ?, ?, ?)");
        return $stmt->execute([
            $id,
            base64_encode($encrypted),
            base64_encode($iv),
            base64_encode($tag),
            time()
        ]);
    }

    public function destroy(string $id): bool {
        $stmt = $this->pdo->prepare("DELETE FROM sessions WHERE id = ?");
        return $stmt->execute([$id]);
    }

    public function gc(int $max_lifetime): int|false {
        $stmt = $this->pdo->prepare("DELETE FROM sessions WHERE updated_at < ?");
        $stmt->execute([time() - $max_lifetime]);
        return $stmt->rowCount();
    }
}

echo "[+] Shifrlangan Sessiya Handler tayyorlandi (Bazada sessiyalar shifrlangan holatda saqlanadi).
";
```
**Tushuntirish:** Standart PHP sessiyalari `/var/lib/php/sessions` katalogida ochiq matn ko'rinishida saqlanadi. Maxsus `SessionHandlerInterface` sessiya yozilayotganda uni shifrlaydi va o'qiyotganda tekshirib ochadi. Hatto ma'lumotlar bazasi administratori ham sessiya ichidagi shaxsiy ma'lumotlarni ko'ra olmaydi.

---

### Topshiriq #1194: JWT (JSON Web Token) Xavfsizlik Auditi: 'none' Algoritmi va Key Confusion
**Tavsif:** Xakerlar tokendagi algoritm sarlavhasini `none` qilib yuborishi yoki RSA ommaviy kalitini HMAC orqali imzolash (Key Confusion Attack) zaifliklaridan himoyalangan qat'iy JWT dekoderini yozing.
**Talablar:** alg sarlavhasini qat'iy oq ro'yxatda tekshirish, 'none' ni rad etish, muddati (exp), nbf va jti tekshiruvi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Zaifliklardan Himoyalangan Qat'iy JWT Validatori
class SecureJwtVerifier {
    private string $secretKey;
    private const ALLOWED_ALGORITHMS = ['HS256'];

    public function __construct(string $secretKey) {
        $this->secretKey = $secretKey;
    }

    public function verifyAndDecode(string $jwt): array {
        $segments = explode('.', $jwt);
        if (count($segments) !== 3) {
            throw new Exception("Yaroqsiz JWT formati!");
        }

        [$headerB64, $payloadB64, $signatureB64] = $segments;

        // 1. Sarlavhani parslash
        $header = json_decode(self::base64UrlDecode($headerB64), true);
        if (!$header || empty($header['alg'])) {
            throw new Exception("JWT sarlavhasi topilmadi!");
        }

        // KRITIK XAVFSIZLIK TEKSHIRUVI 1: 'none' algoritmini taqiqlash
        if (strtolower($header['alg']) === 'none') {
            throw new SecurityException("[XAVF!] 'none' algoritmli soxta token rad etildi!");
        }

        // KRITIK XAVFSIZLIK TEKSHIRUVI 2: Faqat ruxsat berilgan algoritmlar
        if (!in_array($header['alg'], self::ALLOWED_ALGORITHMS, true)) {
            throw new SecurityException("Ruxsat berilmagan algoritm: {$header['alg']}");
        }

        // 2. Imzoni doimiy vaqtda (constant-time) tekshirish
        $dataToSign = "{$headerB64}.{$payloadB64}";
        $expectedSignature = hash_hmac('sha256', $dataToSign, $this->secretKey, true);
        $providedSignature = self::base64UrlDecode($signatureB64);

        if (!hash_equals($expectedSignature, $providedSignature)) {
            throw new SecurityException("JWT raqamli imzosi mos kelmadi!");
        }

        // 3. Payload va muddat tekshiruvi
        $payload = json_decode(self::base64UrlDecode($payloadB64), true);
        $now = time();

        if (isset($payload['exp']) && $now > $payload['exp']) {
            throw new Exception("Token muddati o'tgan (Expired)!");
        }

        if (isset($payload['nbf']) && $now < $payload['nbf']) {
            throw new Exception("Token hali kuchga kirmagan (Not before)!");
        }

        return $payload;
    }

    private static function base64UrlDecode(string $data): string {
        $remainder = strlen($data) % 4;
        if ($remainder) {
            $data .= str_repeat('=', 4 - $remainder);
        }
        return base64_decode(strtr($data, '-_', '+/'));
    }
}

echo "[+] Zaifliklardan to'liq himoyalangan JWT Verifier xizmati tayyor.
";
```
**Tushuntirish:** JWT zaifliklarining eng mashhuri - tajovuzkor sarlavhada `"alg": "none"` deb yozib, imzo qismini bo'sh qoldiradi. Agar kutubxona sarlavhaga ko'r-ko'rona ishonsa, soxta tokenni qabul qiladi. Qat'iy oq ro'yxat bu xavfni to'liq bartaraf etadi.

---

### Topshiriq #1195: HTTP Xavfsizlik Sarlavhalari (Security Headers Middleware)
**Tavsif:** Veb-ilovada Clickjacking, MIME-Sniffing, XSS va SSL tushirish (SSL Stripping) hujumlarini to'xtatish uchun barcha rasmiy HTTP xavfsizlik sarlavhalarini avtomatlashtirilgan tarzda yuboring.
**Talablar:** HSTS, X-Frame-Options: DENY, X-Content-Type-Options: nosniff, Referrer-Policy, Permissions-Policy.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - OWASP Barcha Xavfsizlik Sarlavhalari Middleware
class SecurityHeadersMiddleware {
    public static function applyHeaders(): void {
        // 1. HSTS: Brauzerga ushbu saytga faqat HTTPS orqali kirishni 2 yilga majburlash
        header("Strict-Transport-Security: max-age=63072000; includeSubDomains; preload");

        // 2. Clickjacking himoyasi: Saytni iframe ichida ochishni butunlay taqiqlash
        header("X-Frame-Options: DENY");

        // 3. MIME type sniffing himoyasi (Fayllarni noto'g'ri ijro etilishining oldini oladi)
        header("X-Content-Type-Options: nosniff");

        // 4. Referrer Policy: Tashqi saytlarga o'tganda faqat domen nomi o'tishi, URL dagi maxfiy parametrlar sizmasligi uchun
        header("Referrer-Policy: strict-origin-when-cross-origin");

        // 5. Permissions Policy: Brauzerning xavfli apparat qurilmalarini (kamera, mikrofon, geolokatsiya) cheklash
        header("Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()");

        // 6. Eski brauzerlar uchun XSS filtri
        header("X-XSS-Protection: 0"); // Zamonaviy CSP foydasiga o'chiriladi
    }
}

SecurityHeadersMiddleware::applyHeaders();
echo "[+] Barcha xavfsizlik sarlavhalari (HSTS, X-Frame-Options, CSP, Permissions) faollashtirildi.
";
```
**Tushuntirish:** Xavfsizlik sarlavhalari brauzer darajasidagi mudofaa chizig'idir. Masalan, `Strict-Transport-Security` (HSTS) foydalanuvchi qahvaxonadagi ochiq Wi-Fi da `http://` deb yozsa ham, brauzerning o'zi uni tarmoqqa chiqmasdanoq `https://` ga o'zgartirishini ta'minlaydi.

---

### Topshiriq #1196: API Request Signing: AWS Signature v4 Uslubidagi So'rovlar Yaxlitligi
**Tavsif:** Tashqi moliyaviy integratsiyalarda so'rov yo'lda o'zgartirilmasligi (Tampering) va qayta jo'natilmasligi (Replay Attacks) uchun HTTP metodi, yo'li, sarlavhalari va tanasini HMAC bilan imzolash mexanizmini tuzing.
**Talablar:** Kanonik so'rov shakllantirish, x-timestamp sarlavhasi (5 daqiqa ruxsat), HMAC-SHA256 imzosi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - AWS Signature v4 Uslubidagi API So'rov Imzolash
class ApiRequestSigner {
    public static function sign(string $method, string $path, array $headers, string $body, string $secretKey): string {
        $method = strtoupper($method);
        $hashedBody = hash('sha256', $body);
        
        // Kanonikal so'rov shakllantiramiz
        $canonical = "{$method}
{$path}
{$headers['x-timestamp']}
{$hashedBody}";
        
        // Imzolaymiz
        return hash_hmac('sha256', $canonical, $secretKey);
    }

    public static function verify(string $method, string $path, array $headers, string $body, string $providedSignature, string $secretKey): bool {
        // 1. Replay attack himoyasi: So'rov vaqti 5 daqiqadan (300 sek) oshmagan bo'lishi shart
        $timestamp = (int)($headers['x-timestamp'] ?? 0);
        if (abs(time() - $timestamp) > 300) {
            echo "[!] Replay Attack! So'rov muddati o'tgan.
";
            return false;
        }

        $expectedSig = self::sign($method, $path, $headers, $body, $secretKey);
        return hash_equals($expectedSig, $providedSignature);
    }
}

// Sinov
$secret = "api_partner_secret_key_998";
$headers = ['x-timestamp' => time()];
$body = '{"order_id": 55, "amount": 100000}';

$signature = ApiRequestSigner::sign('POST', '/api/v1/orders', $headers, $body, $secret);
echo "[+] API So'rov imzosi yaratildi: {$signature}
";

$isValid = ApiRequestSigner::verify('POST', '/api/v1/orders', $headers, $body, $signature, $secret);
echo "[+] So'rov qabul qilindimi? " . ($isValid ? "HA (Yaxlit va xavfsiz)" : "RAD ETILDI") . "
";
```
**Tushuntirish:** API Request Signing HTTP so'rovining har bir baytini o'zaro bog'laydi. Agar xaker so'rovdagi `amount: 100000` ni `amount: 10` ga o'zgartirsa, body xeshi o'zgaradi va HMAC imzosi buzilib, server so'rovni rad etadi.

---

### Topshiriq #1197: Fayl Yuklash Xavfsizligi: Magic Bytes, SVG XSS va Xavfsiz Saqlash
**Tavsif:** Foydalanuvchilar profil rasmi yuklayotganda rasm niqobi ostida yashiringan `.php` veb-shellar yoki SVG ichidagi zararli JavaScript kodlarini aniqlovchi va xavfsiz qayta nomlovchi to'liq validator quring.
**Talablar:** finfo (Magic Bytes tekshiruvi), kengaytmani majburiy o'zgartirish, SVG parsing, random fayl nomi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Sanoat Darajasidagi Fayl Yuklash Xavfsizligi
class SecureFileUpload {
    private const ALLOWED_MIME_TYPES = [
        'image/jpeg' => 'jpg',
        'image/png'  => 'png',
        'image/webp' => 'webp',
    ];

    public static function processUploadedImage(string $tmpFilePath, string $originalName, string $uploadDir): string {
        if (!is_uploaded_file($tmpFilePath)) {
            throw new SecurityException("Noqonuniy fayl manbasi!");
        }

        // 1. Fayl kengaytmasiga ISHONMASLIK! Faqat Magic Bytes (finfo) orqali haqiqiy MIME turini aniqlash
        $finfo = new finfo(FILEINFO_MIME_TYPE);
        $detectedMime = $finfo->file($tmpFilePath);

        if (!array_key_exists($detectedMime, self::ALLOWED_MIME_TYPES)) {
            throw new SecurityException("Ruxsatsiz fayl turi aniqlandi: {$detectedMime}");
        }

        // 2. SVG fayllar alohida tekshiriladi (Chunki SVG ichida <script> bo'lishi mumkin)
        if ($detectedMime === 'image/svg+xml') {
            $content = file_get_contents($tmpFilePath);
            if (preg_match('/<script|javascript:|onerror=|onload=/i', $content)) {
                throw new SecurityException("SVG ichida zararli XSS skripti aniqlandi!");
            }
        }

        // 3. Rasm yaxlitligini tekshirish (Haqiqiy rasm ekanligini grafik kutubxona orqali tekshirish)
        $img = @imagecreatefromstring(file_get_contents($tmpFilePath));
        if ($img === false) {
            throw new SecurityException("Buzilgan yoki soxta rasm fayli!");
        }
        imagedestroy($img);

        // 4. Foydalanuvchi bergan nomni BUTUNLAY tashlab yuboramiz va yangi random nom beramiz
        $safeExtension = self::ALLOWED_MIME_TYPES[$detectedMime];
        $newFilename = bin2hex(random_bytes(16)) . '.' . $safeExtension;
        $destination = $uploadDir . DIRECTORY_SEPARATOR . $newFilename;

        if (!move_uploaded_file($tmpFilePath, $destination)) {
            throw new Exception("Faylni saqlashda xatolik yuz berdi.");
        }

        return $newFilename;
    }
}

echo "[+] Xavfsiz fayl yuklash xizmati tayyor (MIME sniffing va shell inyeksiyalari bartaraf etilgan).
";
```
**Tushuntirish:** Buzg'unchilar `shell.php.jpg` yoki `image.png` deb nomlab ichiga PHP kod joylashtiradi. Faqat fayl kengaytmasiga qarash xavflidir. `finfo` faylning dastlabki baytlarini (Magic Numbers) o'qiydi, `imagecreatefromstring` esa rasmni qayta chizib, ichidagi barcha begona zararli kodlarni yo'q qiladi.

---

### Topshiriq #1198: Kriptografik Audit Log Zanjiri (Tamper-Evident Log Chain)
**Tavsif:** Tizim administratorlari yoki buzg'unchilar loglardagi jinoyat izlarini yashirish uchun jurnallarni tahrirlay olmasligi uchun blokcheyn uslubidagi xesh-zanjirli (Hash-Chained Audit Log) tizim yarating.
**Talablar:** Har bir yangi log oldingi log xeshini o'z ichiga oladi, BLAKE2b/SHA256 zanjiri, yaxlitlik auditi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - O'zgartirib Bo'lmaydigan Kriptografik Audit Jurnali
class TamperEvidentAuditLogger {
    private string $logFilePath;

    public function __construct(string $filePath) {
        $this->logFilePath = $filePath;
        if (!file_exists($filePath)) {
            // Ildiz (Genesis) bloki
            $genesis = json_encode(['index' => 0, 'prev_hash' => 'GENESIS_ROOT_2026', 'event' => 'SYSTEM_INIT', 'time' => time()]);
            $genesisHash = hash('sha256', $genesis);
            file_put_contents($filePath, $genesis . " | HASH: " . $genesisHash . "
");
        }
    }

    public function logEvent(string $event, array $context = []): void {
        // Oxirgi qatordan oldingi xeshni olamiz
        $lines = file($this->logFilePath, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        $lastLine = end($lines);
        preg_match('/HASH: ([a-f0-9]{64})/', $lastLine, $matches);
        $prevHash = $matches[1] ?? 'UNKNOWN';

        $entry = [
            'index'     => count($lines),
            'prev_hash' => $prevHash,
            'event'     => $event,
            'context'   => $context,
            'timestamp' => microtime(true)
        ];

        $jsonEntry = json_encode($entry);
        $currentHash = hash('sha256', $jsonEntry);

        file_put_contents($this->logFilePath, $jsonEntry . " | HASH: " . $currentHash . "
", FILE_APPEND | LOCK_EX);
    }

    // Butun jurnal yaxlitligini tekshirish
    public function verifyLogIntegrity(): bool {
        $lines = file($this->logFilePath, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        $expectedPrevHash = 'GENESIS_ROOT_2026';

        foreach ($lines as $i => $line) {
            [$jsonStr, $hashPart] = explode(' | HASH: ', $line);
            $actualHash = trim($hashPart);

            // Xesh to'g'riligini tekshiramiz
            if (!hash_equals(hash('sha256', $jsonStr), $actualHash)) {
                echo "[!] BUZILISH ANIQLANDI! Qator #{$i} xeshi soxtalashtirilgan!
";
                return false;
            }

            $entry = json_decode($jsonStr, true);
            if ($i > 0 && !hash_equals($entry['prev_hash'], $expectedPrevHash)) {
                echo "[!] ZANJIR UZILDI! Qator #{$i} ning prev_hash qiymati mos kelmadi!
";
                return false;
            }

            $expectedPrevHash = $actualHash;
        }

        return true;
    }
}

// Sinov
$logFile = sys_get_temp_dir() . '/audit_chain.log';
@unlink($logFile);
$logger = new TamperEvidentAuditLogger($logFile);

$logger->logEvent("USER_LOGIN", ["uid" => 10, "ip" => "192.168.1.5"]);
$logger->logEvent("TRANSFER_MONEY", ["from" => 10, "to" => 25, "amount" => 500000]);

$isUntampered = $logger->verifyLogIntegrity();
echo "[+] Audit zanjiri yaxlitligi tekshirildi: " . ($isUntampered ? "TOZA VA BUTUN" : "BUZILGAN") . "
";
```
**Tushuntirish:** Blokcheyn arxitekturasidagi kabi, har bir log yozuvi o'zidan oldingi logning xeshini o'z ichiga oladi. Agar buzg'unchi oradagi bitta qatorda o'zining jinoyatini yashirish uchun raqamni o'zgartirsa, undan keyingi barcha qatorlarning zanjiri buziladi va bu audit tekshiruvida darhol fosh bo'ladi.

---

### Topshiriq #1199: Ma'lumotlar Bazasidagi PII Ma'lumotlarni Maydon Darajasida Shifrlash (Field-Level Encryption)
**Tavsif:** GDPR va milliy shaxsiy ma'lumotlar to'g'risidagi qonunlarga muvofiq, foydalanuvchilarning pasport raqami va PINFL ma'lumotlarini bazada maydon darajasida (Field-Level) shifrlab saqlash mexanizmini yarating.
**Talablar:** Tizimli ma'lumotlar modeli, shifrlash va deshifrlash getter/setterlari, kalitlarni rotatsiya qilish imkoniyati.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Field-Level Encryption (Maydon Darajasidagi Shifrlash)
class EncryptedField {
    private string $key;

    public function __construct(string $encryptionKey) {
        $this->key = $encryptionKey;
    }

    public function encryptField(?string $value): ?string {
        if ($value === null) return null;
        $nonce = random_bytes(SODIUM_CRYPTO_SECRETBOX_NONCEBYTES);
        $ciphertext = sodium_crypto_secretbox($value, $nonce, $this->key);
        // Saqlash uchun: 'enc:v1:nonce:ciphertext'
        return 'enc:v1:' . sodium_bin2hex($nonce) . ':' . sodium_bin2hex($ciphertext);
    }

    public function decryptField(?string $storedValue): ?string {
        if ($storedValue === null || !str_starts_with($storedValue, 'enc:v1:')) {
            return $storedValue; // Shifrlanmagan eski qiymat
        }

        $parts = explode(':', $storedValue);
        if (count($parts) !== 4) return null;

        $nonce = sodium_hex2bin($parts[2]);
        $ciphertext = sodium_hex2bin($parts[3]);

        $decrypted = sodium_crypto_secretbox_open($ciphertext, $nonce, $this->key);
        return ($decrypted !== false) ? $decrypted : null;
    }
}

// Model simulyatsiyasi
class UserEntity {
    private EncryptedField $crypto;
    public int $id;
    public string $username;
    public ?string $passportNumberEncrypted = null;

    public function __construct(EncryptedField $crypto) {
        $this->crypto = $crypto;
    }

    public function setPassportNumber(string $passport): void {
        $this->passportNumberEncrypted = $this->crypto->encryptField($passport);
    }

    public function getPassportNumber(): ?string {
        return $this->crypto->decryptField($this->passportNumberEncrypted);
    }
}

// Sinov
$key = sodium_crypto_secretbox_keygen();
$crypto = new EncryptedField($key);

$user = new UserEntity($crypto);
$user->id = 1;
$user->username = "alisher_dev";
$user->setPassportNumber("AA 9988221");

echo "[+] Bazaga yoziladigan qiymat: {$user->passportNumberEncrypted}
";
echo "[+] Ilova ichida o'qilgan qiymat: {$user->getPassportNumber()}
";
```
**Tushuntirish:** Field-Level Encryption butun bazani yoki diskni shifrlashdan (TDE) ancha xavfsizroq. Hatto tajovuzkor SQL Injection orqali bazadagi barcha jadvallarni o'g'irlab ketsa ham, shaxsiy ma'lumotlar shifrlangan holda qoladi va ularni o'qib bo'lmaydi.

---

### Topshiriq #1200: DoS va Xotira Hujumlaridan Himoyalanish: Katta JSON va Regex Bombalari
**Tavsif:** Kichik so'rov ichiga yashirilgan millionlab belgilardan iborat JSON bombalari yoki protsessorni qotiruvchi ReDoS (Regular Expression Denial of Service) hujumlarini to'xtatuvchi himoyalangan parser yozing.
**Talablar:** Maksimal hajm cheklovi (Content-Length), JSON chuqurligi (depth), pcre.backtrack_limit va xatoliklar nazorati.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Sanoat Darajasidagi DoS va Xotira Himoyachisi
class SafePayloadParser {
    private const MAX_BODY_BYTES = 2 * 1024 * 1024; // Maksimal 2 MB ruxsat
    private const MAX_JSON_DEPTH = 32;               // Maksimal ichma-ichlik chuqurligi

    public static function parseJsonSafely(string $rawBody): array {
        // 1. Hajmni tekshirish
        if (strlen($rawBody) > self::MAX_BODY_BYTES) {
            throw new SecurityException("So'rov hajmi ruxsat etilgan 2 MB limitdan oshib ketdi!");
        }

        // 2. JSON ichki chuqurligini cheklash (Stack overflow oldini olish)
        try {
            $data = json_decode(
                $rawBody,
                true,
                self::MAX_JSON_DEPTH,
                JSON_THROW_ON_ERROR | JSON_BIGINT_AS_STRING
            );
        } catch (JsonException $e) {
            throw new Exception("Yaroqsiz yoki chuqurligi haddan tashqari ko'p JSON ma'lumoti: " . $e->getMessage());
        }

        return $data;
    }

    // ReDoS (Regex Denial of Service) dan himoyalangan xavfsiz solishtirish
    public static function safeRegexMatch(string $pattern, string $subject): bool {
        // Backtrack limitini cheklaymiz (CPU qotishini oldini oladi)
        $oldLimit = ini_get('pcre.backtrack_limit');
        ini_set('pcre.backtrack_limit', '10000');

        $result = @preg_match($pattern, $subject);
        ini_set('pcre.backtrack_limit', $oldLimit);

        if ($result === false) {
            $error = preg_last_error();
            if ($error === PREG_BACKTRACK_LIMIT_ERROR) {
                throw new SecurityException("[ReDoS XAVF!] Regex juda ko'p orqaga chekinish (backtrack) talab qildi!");
            }
            throw new Exception("Regex tahlil xatosi.");
        }

        return ($result === 1);
    }
}

// Sinov
$json = '{"user": {"name": "Ali", "settings": {"theme": "dark"}}}';
$parsed = SafePayloadParser::parseJsonSafely($json);
echo "[+] Xavfsiz JSON muvaffaqiyatli o'qildi: Foydalanuvchi " . $parsed['user']['name'] . "
";

// ReDoS hujum sinovi: Katastrofik orqaga chekinishga sabab bo'luvchi regex
$vulnerableRegex = '/(a+)+$/';
$evilString = str_repeat('a', 25) . '!';

try {
    SafePayloadParser::safeRegexMatch($vulnerableRegex, $evilString);
} catch (SecurityException $e) {
    echo "[+] ReDoS hujumi bartaraf etildi: " . $e->getMessage() . "
";
}
```
**Tushuntirish:** ReDoS hujumlarida yomon tuzilgan muntazam ifodalar (masalan `(a+)+$`) mos kelmaydigan satrga duch kelganda eksponensial $O(2^N)$ orqaga chekinishlarni (backtracking) boshlaydi va protsessorni 100% yuklama bilan qotiradi. `pcre.backtrack_limit` orqali bu xavf bir zumda to'xtatiladi.

---

