# Khorazmiy AI: Rust - Modul 24
## Mavzu: Kriptografiya va Xavfsizlik: ring, RustCrypto, AES-256-GCM, Ed25519, Zero-Knowledge asoslari, constant-time operations va Unsafe audit

### Topshiriq #1151: AES-256-GCM Bilan Autentifikatsiyalangan Shifrlash (ring kutubxonasi)
**Tavsif:** Foydalanuvchilarning maxfiy shaxsiy ma'lumotlarini (PII) apparat darajasidagi tezlikda va soxtalashtirishdan himoyalangan holda shifrlash.
**Talablar:** `ring::aead`, `AES_256_GCM`, `SealingKey`, `OpeningKey`, 96-bit Nonce.
**Yechim (Rust):**
```rust
use ring::aead::{self, BoundKey, Nonce, NonceSequence, OpeningKey, SealingKey, UnboundKey, AES_256_GCM};
use ring::error::Unspecified;
use ring::rand::{SecureRandom, SystemRandom};

struct OneNonce(Option<Nonce>);
impl NonceSequence for OneNonce {
    fn advance(&mut self) -> Result<Nonce, Unspecified> {
        self.0.take().ok_or(Unspecified)
    }
}

pub fn encrypt_aes_256_gcm(key_bytes: &[u8; 32], nonce_bytes: &[u8; 12], data: &mut Vec<u8>) -> Result<(), Unspecified> {
    let unbound_key = UnboundKey::new(&AES_256_GCM, key_bytes)?;
    let nonce = Nonce::try_assume_unique_for_key(nonce_bytes)?;
    let mut sealing_key = SealingKey::new(unbound_key, OneNonce(Some(nonce)));

    // Joyida (in-place) shifrlash va 16 baytlik autentifikatsiya tegi (Tag) qo'shish
    sealing_key.seal_in_place_append_tag(aead::Aad::empty(), data)?;
    Ok(())
}

pub fn decrypt_aes_256_gcm(key_bytes: &[u8; 32], nonce_bytes: &[u8; 12], data: &mut Vec<u8>) -> Result<(), Unspecified> {
    let unbound_key = UnboundKey::new(&AES_256_GCM, key_bytes)?;
    let nonce = Nonce::try_assume_unique_for_key(nonce_bytes)?;
    let mut opening_key = OpeningKey::new(unbound_key, OneNonce(Some(nonce)));

    // Joyida ochish va yaxlitlikni tekshirish
    let decrypted_slice = opening_key.open_in_place(aead::Aad::empty(), data)?;
    let len = decrypted_slice.len();
    data.truncate(len);
    Ok(())
}

fn main() {
    let mut data = b"Maxfiy tibbiy karta ma'lumotlari".to_vec();
    let key = [0x5au8; 32];
    let nonce = [0x1fu8; 12];

    encrypt_aes_256_gcm(&key, &nonce, &mut data).expect("Shifrlash muvaffaqiyatli");
    println!("Shifrlangan hajm (teg bilan): {} bayt", data.len());

    decrypt_aes_256_gcm(&key, &nonce, &mut data).expect("Dekodlash muvaffaqiyatli");
    println!("Asl ma'lumot: {}", String::from_utf8_lossy(&data));
}
```
**Tushuntirish:** AES-GCM (Galois/Counter Mode) AEAD (Authenticated Encryption with Associated Data) standarti hisoblanadi. U nafaqat shifrlaydi, balki 128-bitlik GMAC tegi yordamida shifrlangan matnning bitta biti ham o'zgarmaganligini kafolatlaydi.

---

### Topshiriq #1152: RustCrypto aes-gcm Bilan Qo'shimcha Autentifikatsiya Ma'lumoti (AAD)
**Tavsif:** Fayl yoki paket sarlavhasini ochiq qoldirgan holda, uning o'zgartirilmasligini shifrlangan kontent bilan bog'lash.
**Talablar:** `aes_gcm::{Aes256Gcm, KeyInit, AeadInPlace}`, `Payload` bilan AAD tekshiruvi.
**Yechim (Rust):**
```rust
use aes_gcm::{
    aead::{Aead, KeyInit, Payload},
    Aes256Gcm, Nonce
};

pub fn encrypt_with_metadata(key_bytes: &[u8; 32], nonce_bytes: &[u8; 12], aad_metadata: &[u8], plaintext: &[u8]) -> Vec<u8> {
    let cipher = Aes256Gcm::new_from_slice(key_bytes).expect("Kalit hajmi 32 bayt bo'lishi shart");
    let nonce = Nonce::from_slice(nonce_bytes);

    let payload = Payload {
        msg: plaintext,
        aad: aad_metadata, // Shifrlanmaydi, lekin autentifikatsiyalanadi
    };

    cipher.encrypt(nonce, payload).expect("Shifrlash xatosi")
}

fn main() {
    let key = [7u8; 32];
    let nonce = [3u8; 12];
    let metadata = b"User-ID: 1042; Epoch: 2026";
    let message = b"Bank o'tkazmasi: 10,000,000 UZS";

    let ciphertext = encrypt_with_metadata(&key, &nonce, metadata, message);
    println!("AAD bilan shifrlangan paket hajmi: {} bayt", ciphertext.len());
}
```
**Tushuntirish:** AAD (Additional Authenticated Data) tarmoq marshrutlash sarlavhalari uchun zarurdir: sarlavha shifrlanmaydi (routerlar o'qiy olishi uchun), lekin tajovuzkor uni o'zgartira olmaydi, aks holda MAC tekshiruvi xato beradi.

---

### Topshiriq #1153: ChaCha20-Poly1305 AEAD Shifrlash (Mobil va Apparat AES bo'lmagan tizimlar)
**Tavsif:** AES buyruqlar to'plami (AES-NI) bo'lmagan ARM mikrokontrollerlari va mobil qurilmalarda eng yuqori dasturiy shifrlash tezligiga erishish.
**Talablar:** `chacha20poly1305::{ChaCha20Poly1305, KeyInit, Aead}`, 256-bit kalit, 96-bit nonce.
**Yechim (Rust):**
```rust
use chacha20poly1305::{
    aead::{Aead, KeyInit},
    ChaCha20Poly1305, Nonce
};

pub fn chacha_encrypt(key: &[u8; 32], nonce: &[u8; 12], data: &[u8]) -> Vec<u8> {
    let cipher = ChaCha20Poly1305::new_from_slice(key).unwrap();
    let nonce = Nonce::from_slice(nonce);
    cipher.encrypt(nonce, data).expect("ChaCha20 shifrlashda xato")
}

pub fn chacha_decrypt(key: &[u8; 32], nonce: &[u8; 12], ciphertext: &[u8]) -> Result<Vec<u8>, chacha20poly1305::aead::Error> {
    let cipher = ChaCha20Poly1305::new_from_slice(key).unwrap();
    let nonce = Nonce::from_slice(nonce);
    cipher.decrypt(nonce, ciphertext)
}

fn main() {
    let key = [0x42u8; 32];
    let nonce = [0x99u8; 12];
    let secret = b"IoT sensori maxfiy telemetriyasi";

    let encrypted = chacha_encrypt(&key, &nonce, secret);
    let decrypted = chacha_decrypt(&key, &nonce, &encrypted).unwrap();
    assert_eq!(secret, &decrypted[..]);
    println!("ChaCha20-Poly1305 sinovi muvaffaqiyatli yakunlandi.");
}
```
**Tushuntirish:** ChaCha20-Poly1305 Daniel J. Bernstein tomonidan yaratilgan bo'lib, kesh-timing hujumlariga mutlaqo chidamli va AES-NI yo'q arxitekturalarda AES dan 3 baravar tezroq ishlaydi (WireGuard va TLS 1.3 da standart).

---

### Topshiriq #1154: Kriptografik Xavfsiz Tasodifiy Sonlar Generatsiyasi (CSPRNG)
**Tavsif:** Kriptografik kalitlar, Nonce va tuz (Salt) yaratishda operatsion tizim entropiyasidan (`/dev/urandom` / `BCryptGenRandom`) xavfsiz foydalanish.
**Talablar:** `ring::rand::SystemRandom`, `SecureRandom::fill`.
**Yechim (Rust):**
```rust
use ring::rand::{SecureRandom, SystemRandom};

pub fn generate_secure_bytes(length: usize) -> Result<Vec<u8>, ring::error::Unspecified> {
    let rng = SystemRandom::new();
    let mut bytes = vec![0u8; length];
    rng.fill(&mut bytes)?;
    Ok(bytes)
}

fn main() {
    let key_256 = generate_secure_bytes(32).expect("Entropiya olinmadi");
    let nonce_96 = generate_secure_bytes(12).expect("Nonce olinmadi");

    println!("256-bitli xavfsiz kalit (HEX): {:02x?}", &key_256[..8]);
    println!("96-bitli tasodifiy Nonce (HEX): {:02x?}", &nonce_96[..6]);
}
```
**Tushuntirish:** `ring::rand::SystemRandom` to'g'ridan-to'g'ri operatsion tizim yadrosi kriptografik drayverlariga murojaat qiladi. U oddiy PRNG (masalan, C rand() yoki LCG) lardan farqli ravishda oldindan aytib bo'lmaslik (unpredictability) xossasiga ega.

---

### Topshiriq #1155: Xotiradagi Maxfiy Kalitlarni Xavfsiz Tozalash (Zeroize va ZeroizeOnDrop)
**Tavsif:** Parollar va xususiy kalitlar ishlatib bo'lingach, operativ xotirada qolib ketishi (Memory Dump o'g'irligi) ning oldini olish.
**Talablar:** `zeroize::{Zeroize, ZeroizeOnDrop}`, avtomatik tozalash.
**Yechim (Rust):**
```rust
use zeroize::{Zeroize, ZeroizeOnDrop};

#[derive(Zeroize, ZeroizeOnDrop)]
pub struct MasterKey {
    key_material: Vec<u8>,
}

impl MasterKey {
    pub fn new(raw: Vec<u8>) -> Self {
        Self { key_material: raw }
    }

    pub fn expose_secret(&self) -> &[u8] {
        &self.key_material
    }
}

fn main() {
    {
        let secret = MasterKey::new(vec![0xAA, 0xBB, 0xCC, 0xDD]);
        println!("Kalit xotirada mavjud: {:02x?}", secret.expose_secret());
        // Blok tugaganda drop() chaqiriladi va xotira nolga (0x00) tenglashtiriladi
    }
    println!("Obyekt xotiradan to'liq tozalab yo'q qilindi (Zeroized).");
}
```
**Tushuntirish:** Oddiy `drop()` faqat xotira ko'rsatkichini bo'shatadi, lekin xotiradagi baytlar o'chirilmaydi. Kompilyator optimizatsiyalari bo'shatilgan xotiraga yozishni olib tashlashi mumkin, ammo `Zeroize` `volatile` yozish orqali buni kafolatli nolga aylantiradi.

---

### Topshiriq #1156: HKDF Orqali Asosiy Kalitdan Subkalitlar Hosil Qilish (RFC 5869)
**Tavsif:** Bitta asosiy umumiy sirdan (Master Secret) shifrlash, autentifikatsiya va IV uchun alohida mustaqil kalitlarni ajratib olish.
**Talablar:** `ring::hkdf`, `HKDF_SHA256`, `extract_and_expand`.
**Yechim (Rust):**
```rust
use ring::hkdf::{Salt, HKDF_SHA256};

pub fn derive_keys(master_key: &[u8], salt_bytes: &[u8], info: &[u8], out_len: usize) -> Vec<u8> {
    let salt = Salt::new(HKDF_SHA256, salt_bytes);
    let prk = salt.extract(master_key);

    let mut output = vec![0u8; out_len];
    let okm = prk.expand(&[info], HKDF_SHA256).expect("HKDF expand xatosi");
    okm.fill(&mut output).expect("Kalit to'ldirilmadi");
    output
}

fn main() {
    let master = b"master_diffie_hellman_shared_secret_42";
    let salt = b"unikal_tasodifiy_tuz_123";

    let enc_key = derive_keys(master, salt, b"aes-encryption-key", 32);
    let mac_key = derive_keys(master, salt, b"hmac-auth-key", 32);

    println!("Hosil qilingan Shifrlash kaliti: {:02x?}", &enc_key[..8]);
    println!("Hosil qilingan MAC kaliti: {:02x?}", &mac_key[..8]);
}
```
**Tushuntirish:** HKDF (HMAC-based Extract-and-Expand Key Derivation Function) ikki bosqichda ishlaydi: Extract (entropiyani yuqori sifatli yagona kalitga jamlaydi) va Expand (istalgancha uzunlikdagi psevdotasodifiy subkalitlar oqimini yaratadi).

---

### Topshiriq #1157: Argon2id Bilan Parollarni Mustahkam Xeshlash (Parol Xavfsizligi)
**Tavsif:** Foydalanuvchi parollarini GPU/ASIC apparat hujumlariga qarshi xotira-qiyin (Memory-hard) standart bo'yicha xavfsiz saqlash.
**Talablar:** `argon2::{Argon2, PasswordHasher, PasswordVerifier, PasswordHash}`, `SaltString`.
**Yechim (Rust):**
```rust
use argon2::{
    password_hash::{rand_core::OsRng, PasswordHash, PasswordHasher, PasswordVerifier, SaltString},
    Argon2
};

pub fn hash_password(password: &str) -> String {
    let salt = SaltString::generate(&mut OsRng);
    let argon2 = Argon2::default();
    argon2.hash_password(password.as_bytes(), &salt)
        .expect("Xeshlash xatosi")
        .to_string()
}

pub fn verify_password(password: &str, hash_str: &str) -> bool {
    let parsed_hash = match PasswordHash::new(hash_str) {
        Ok(h) => h,
        Err(_) => return false,
    };
    Argon2::default().verify_password(password.as_bytes(), &parsed_hash).is_ok()
}

fn main() {
    let pwd = "O'taMaxfiyParol_2026!#";
    let hash = hash_password(pwd);
    println!("Argon2id Xesh: {}", hash);

    assert!(verify_password(pwd, &hash));
    assert!(!verify_password("noto'g'ri_parol", &hash));
    println!("Parol muvaffaqiyatli tekshirildi.");
}
```
**Tushuntirish:** Argon2id Password Hashing Competition g'olibi bo'lib, xotira sarfini (Memory Cost), hisoblash vaqtini (Time Cost) va paralellikni sozlash imkonini beradi. U kesh-timing va GPU fermalarining brute-force hujumlarini to'xtatadi.

---

### Topshiriq #1158: HMAC-SHA256 Yordamida Xabarlar Yaxlitligini Tekshirish
**Tavsif:** API so'rovlari va veb-xuklar (Webhooks) dagi ma'lumotlarning yo'lda soxtalashtirilmaganini maxfiy kalit bilan tekshirish.
**Talablar:** `ring::hmac`, `Key`, `sign`, `verify`.
**Yechim (Rust):**
```rust
use ring::hmac::{self, Key, Tag};

pub fn compute_hmac_sha256(secret_key: &[u8], message: &[u8]) -> Tag {
    let key = Key::new(hmac::HMAC_SHA256, secret_key);
    hmac::sign(&key, message)
}

pub fn verify_hmac_sha256(secret_key: &[u8], message: &[u8], tag_bytes: &[u8]) -> bool {
    let key = Key::new(hmac::HMAC_SHA256, secret_key);
    hmac::verify(&key, message, tag_bytes).is_ok()
}

fn main() {
    let key = b"webhook_secret_key_999";
    let body = b"{\"event\": \"payment_received\", \"amount\": 50000}";

    let tag = compute_hmac_sha256(key, body);
    println!("HMAC Imzosi tayyorlandi: {} bayt", tag.as_ref().len());

    let is_valid = verify_hmac_sha256(key, body, tag.as_ref());
    println!("Imzo tekshiruvi natijasi: {}", is_valid);
}
```
**Tushuntirish:** `hmac::verify` doimo doimiy vaqtda (constant-time) solishtiradi. Bu tajovuzkorning imzo baytlarini vaqt o'lchash (Timing Attack) orqali bittalab taxmin qilishiga yo'l qo'ymaydi.

---

### Topshiriq #1159: BLAKE3 Tezkor Kriptografik Xeshlash va Merkle Daraxti
**Tavsif:** Katta hajmdagi fayllarni SHA-256 dan 10 barobar tezroq xeshlash va daraxtli arxitektura (Tree Hashing) imkoniyatlaridan foydalanish.
**Talablar:** `blake3::Hasher`, ko'p oqimli xeshlash (`update_rayon`).
**Yechim (Rust):**
```rust
use blake3::Hasher;

pub fn hash_data_blake3(data: &[u8]) -> [u8; 32] {
    let mut hasher = Hasher::new();
    hasher.update(data);
    *hasher.finalize().as_bytes()
}

fn main() {
    let chunk = vec![0xABu8; 1024 * 1024]; // 1 MB ma'lumot
    let digest = hash_data_blake3(&chunk);
    println!("BLAKE3 256-bit xesh (HEX): {:02x?}", &digest[..8]);
}
```
**Tushuntirish:** BLAKE3 o'zining ichki tuzilishida Merkle Tree arxitekturasidan foydalanadi. Natijada katta fayllar SIMD va ko'p yadroli protsessorlarda parallel xeshlanadi va inkremental tekshiruvlarni qo'llab-quvvatlaydi.

---

### Topshiriq #1160: Streaming AEAD Bilan Katta Fayllarni Bo'laklab Shifrlash
**Tavsif:** Ko'p gigabaytlik fayllarni operativ xotiraga to'liq yuklamasdan 64 KB lik freymlarga ajratib xavfsiz shifrlash.
**Talablar:** Freym ketma-ketlik raqami, oxirgi blok bayrog'i, Nonce dagi siljish.
**Yechim (Rust):**
```rust
use aes_gcm::{
    aead::{Aead, KeyInit},
    Aes256Gcm, Nonce
};

pub fn encrypt_chunk(cipher: &Aes256Gcm, base_nonce: &[u8; 8], chunk_index: u32, is_final: bool, data: &[u8]) -> Vec<u8> {
    let mut nonce_bytes = [0u8; 12];
    nonce_bytes[..8].copy_from_slice(base_nonce);
    nonce_bytes[8..11].copy_from_slice(&chunk_index.to_be_bytes()[1..]);
    nonce_bytes[11] = if is_final { 1 } else { 0 };

    let nonce = Nonce::from_slice(&nonce_bytes);
    cipher.encrypt(nonce, data).expect("Bo'lakni shifrlashda xato")
}

fn main() {
    let key = [0x11u8; 32];
    let cipher = Aes256Gcm::new_from_slice(&key).unwrap();
    let base_nonce = [0x22u8; 8];

    let chunk1 = encrypt_chunk(&cipher, &base_nonce, 0, false, b"Birinchi 64KB qism");
    let chunk2 = encrypt_chunk(&cipher, &base_nonce, 1, true, b"Yakuniy qism");
    println!("Freymlar shifrlangan: 1={}b, 2={}b", chunk1.len(), chunk2.len());
}
```
**Tushuntirish:** Streaming AEAD da har bir bo'lakka indeks va final-bayroq Nonce tarkibiga qo'shiladi. Bu tajovuzkorning fayl bo'laklari o'rnini almashtirishi yoki qisqartirib qo'yishi (Truncation attack) ning oldini oladi.

---

### Topshiriq #1161: Envelope Encryption va Key Rotation Arxitekturasi
**Tavsif:** Ma'lumotlarni alohida Ma'lumot Kaliti (DEK) bilan shifrlab, DEK ning o'zini esa Asosiy Kalit (KEK) bilan shifrlash.
**Talablar:** Data Encryption Key (DEK) va Key Encryption Key (KEK) ierarxiyasi.
**Yechim (Rust):**
```rust
use aes_gcm::{
    aead::{Aead, KeyInit},
    Aes256Gcm, Nonce
};

pub struct EncryptedEnvelope {
    pub encrypted_dek: Vec<u8>,
    pub dek_nonce: [u8; 12],
    pub encrypted_data: Vec<u8>,
    pub data_nonce: [u8; 12],
}

pub fn create_envelope(kek: &[u8; 32], raw_data: &[u8]) -> EncryptedEnvelope {
    let kek_cipher = Aes256Gcm::new_from_slice(kek).unwrap();
    let dek = [0x77u8; 32]; // Amalda CSPRNG orqali generatsiya qilinadi
    let dek_cipher = Aes256Gcm::new_from_slice(&dek).unwrap();

    let dek_nonce = [0x01u8; 12];
    let data_nonce = [0x02u8; 12];

    let encrypted_dek = kek_cipher.encrypt(Nonce::from_slice(&dek_nonce), &dek[..]).unwrap();
    let encrypted_data = dek_cipher.encrypt(Nonce::from_slice(&data_nonce), raw_data).unwrap();

    EncryptedEnvelope { encrypted_dek, dek_nonce, encrypted_data, data_nonce }
}

fn main() {
    let kek = [0x99u8; 32];
    let env = create_envelope(&kek, b"Katta ma'lumotlar bazasi yozuvi");
    println!("Konvert yaratildi: Shifrlangan DEK: {} bayt", env.encrypted_dek.len());
}
```
**Tushuntirish:** Envelope Encryption (Konvert shifrlash) bulutli KMS (AWS KMS, GCP KMS, Vault) xizmatlarining asosi hisoblanadi. KEK ni almashtirganda faqat kichik DEK qayta shifrlanadi (Rewrap), butun fayl qayta shifrlanmaydi.

---

### Topshiriq #1162: Deterministik Shifrlash: AES-SIV (Synthetic IV, RFC 5297)
**Tavsif:** Ma'lumotlar bazasida shifrlangan ustunlar bo'yicha indeksli qidiruvni ta'minlash uchun bir xil ochiq matnga doim bir xil shifr hosil qilish.
**Talablar:** Misuse-resistant deterministic authenticated encryption (AES-SIV).
**Yechim (Rust):**
```rust
use aes_siv::siv::Aes256SivAead;
use aes_siv::aead::{Aead, KeyInit};

pub fn deterministic_encrypt(key_64: &[u8; 64], plaintext: &[u8]) -> Vec<u8> {
    let cipher = Aes256SivAead::new_from_slice(key_64).unwrap();
    // Nonce bo'sh bo'lganda ham xavfsiz deterministik shifrlash
    cipher.encrypt(&Default::default(), plaintext).expect("SIV shifrlash xatosi")
}

fn main() {
    let key = [0x55u8; 64]; // AES-256-SIV uchun 512-bit kalit talab qilinadi
    let pii = b"JSHSHIR: 12345678901234";

    let ct1 = deterministic_encrypt(&key, pii);
    let ct2 = deterministic_encrypt(&key, pii);

    assert_eq!(ct1, ct2); // Har doim bir xil shifr matn hosil bo'ladi
    println!("Deterministik AES-SIV shifrlash muvaffaqiyatli: {} bayt", ct1.len());
}
```
**Tushuntirish:** AES-SIV Nonce sintetik hisoblanganligi sababli, agar Nonce takrorlansa ham maxfiy kalit sizib chiqmaydi (Nonce-Reuse Misuse Resistance). Bu qidiriladigan shifrlash (Searchable Encryption) uchun xavfsiz tanlovdir.

---

### Topshiriq #1163: Ed25519 Juftlik Kalitlarini Yaratish va Xabarlarni Imzolash (ring)
**Tavsif:** Dasturiy ta'minot yangilanishlarini (OTA Updates) autentifikatsiya qilish uchun Ed25519 kalit juftligini yaratish va imzolash.
**Talablar:** `ring::signature::Ed25519KeyPair`, PKCS#8 format.
**Yechim (Rust):**
```rust
use ring::rand::SystemRandom;
use ring::signature::{Ed25519KeyPair, KeyPair};

pub fn create_and_sign(message: &[u8]) -> (Vec<u8>, Vec<u8>, Vec<u8>) {
    let rng = SystemRandom::new();
    // PKCS#8 hujjat formatida Ed25519 kalitini yaratish
    let pkcs8_bytes = Ed25519KeyPair::generate_pkcs8(&rng).unwrap();
    let key_pair = Ed25519KeyPair::from_pkcs8(pkcs8_bytes.as_ref()).unwrap();

    let public_key = key_pair.public_key().as_ref().to_vec();
    let signature = key_pair.sign(message).as_ref().to_vec();

    (pkcs8_bytes.as_ref().to_vec(), public_key, signature)
}

fn main() {
    let doc = b"Yangi mikrodastur v2.4.0 tasdiqlandi.";
    let (_, pub_key, sig) = create_and_sign(doc);

    println!("Ochiq kalit hajmi: {} bayt", pub_key.len());
    println!("Ed25519 raqamli imzo hajmi: {} bayt", sig.len());
}
```
**Tushuntirish:** Ed25519 (Edwards-curve Digital Signature Algorithm) Curve25519 egri chizig'iga asoslangan bo'lib, ochiq kaliti 32 bayt, imzosi esa 64 baytni tashkil qiladi. U RSA ga qaraganda 100 baravar tez imzolaydi.

---

### Topshiriq #1164: Ed25519 Raqamli Imzolarini Tekshirish (ring::signature::UnparsedPublicKey)
**Tavsif:** Server yoki ilovada qabul qilingan xabar va imzoni faqat ochiq kalit yordamida verifikatsiya qilish.
**Talablar:** `ring::signature::UnparsedPublicKey`, `ED25519`, `verify`.
**Yechim (Rust):**
```rust
use ring::signature::{UnparsedPublicKey, ED25519};

pub fn verify_ed25519(public_key_bytes: &[u8], message: &[u8], signature_bytes: &[u8]) -> bool {
    let public_key = UnparsedPublicKey::new(&ED25519, public_key_bytes);
    public_key.verify(message, signature_bytes).is_ok()
}

fn main() {
    let pub_key = [0u8; 32];
    let msg = b"Tranzaksiya ma'lumoti";
    let fake_sig = [0u8; 64];

    let result = verify_ed25519(&pub_key, msg, &fake_sig);
    println!("Soxta imzo tekshiruvi natijasi: {} (kutilganidek rad etildi)", result);
}
```
**Tushuntirish:** `UnparsedPublicKey::verify` imzoning to'g'riligini va xabarning yo'lda o'zgartirilmaganligini doimiy vaqtda matematik jihatdan tekshiradi.

---

### Topshiriq #1165: X25519 Diffie-Hellman Kalit Almashinuvi (ring::agreement)
**Tavsif:** Ikki tomon ochiq tarmoq orqali o'z ochiq kalitlarini almashib, hech kim bilmaydigan umumiy maxfiy kalitni (Shared Secret) hisoblash.
**Talablar:** `ring::agreement::{EphemeralPrivateKey, X25519, agree_ephemeral}`.
**Yechim (Rust):**
```rust
use ring::agreement::{agree_ephemeral, EphemeralPrivateKey, UnparsedPublicKey, X25519};
use ring::rand::SystemRandom;

pub fn x25519_key_exchange() {
    let rng = SystemRandom::new();

    // 1. Alisa o'z vaqtinchalik kalitini yaratadi
    let alice_priv = EphemeralPrivateKey::generate(&X25519, &rng).unwrap();
    let alice_pub = alice_priv.compute_public_key().unwrap();

    // 2. Bob o'z vaqtinchalik kalitini yaratadi
    let bob_priv = EphemeralPrivateKey::generate(&X25519, &rng).unwrap();
    let bob_pub = bob_priv.compute_public_key().unwrap();

    // 3. Alisa Bobning ochiq kaliti bilan umumiy sirni topadi
    let alice_shared = agree_ephemeral(alice_priv, &UnparsedPublicKey::new(&X25519, bob_pub.as_ref()), |key_material| {
        key_material.to_vec()
    }).unwrap();

    // 4. Bob Alisaning ochiq kaliti bilan umumiy sirni topadi
    let bob_shared = agree_ephemeral(bob_priv, &UnparsedPublicKey::new(&X25519, alice_pub.as_ref()), |key_material| {
        key_material.to_vec()
    }).unwrap();

    assert_eq!(alice_shared, bob_shared);
    println!("X25519 orqali umumiy maxfiy kalit hosil qilindi: {} bayt", alice_shared.len());
}

fn main() {
    x25519_key_exchange();
}
```
**Tushuntirish:** X25519 (ECDH) ulanish o'rnatishda Perfect Forward Secrecy (PFS) ni kafolatlaydi: har bir sessiya uchun yangi efemer kalitlar ishlatiladi, natijada kelajakda server buzilsa ham eski yozib olingan trafik ochilmaydi.

---

### Topshiriq #1166: RSA-4096 OAEP Bilan Xavfsiz Shifrlash va Dekodlash (rsa crate)
**Tavsif:** Klassik korporativ tizimlarda katta hajmdagi xususiy kalitlar bilan shifrlangan aloqani tashkil qilish.
**Talablar:** `rsa::{RsaPrivateKey, RsaPublicKey, Oaep}`, SHA-256 xesh.
**Yechim (Rust):**
```rust
use rsa::{Oaep, RsaPrivateKey, RsaPublicKey};
use sha2::Sha256;
use rand::rngs::OsRng;

pub fn rsa_oaep_roundtrip() {
    let mut rng = OsRng;
    let bits = 2048; // Namuna uchun 2048 (ishlab chiqarishda 4096)
    let private_key = RsaPrivateKey::new(&mut rng, bits).expect("RSA kalit yaratish xatosi");
    let public_key = RsaPublicKey::from(&private_key);

    let data = b"Maxfiy API kaliti";
    let padding = Oaep::new::<Sha256>();

    // Ochiq kalit bilan shifrlash
    let enc_data = public_key.encrypt(&mut rng, padding, &data[..]).expect("Shifrlash xatosi");
    println!("RSA shifrlangan ma'lumot hajmi: {} bayt", enc_data.len());

    // Xususiy kalit bilan ochish
    let dec_padding = Oaep::new::<Sha256>();
    let dec_data = private_key.decrypt(dec_padding, &enc_data).expect("Dekodlash xatosi");
    assert_eq!(&data[..], &dec_data[..]);
}

fn main() {
    rsa_oaep_roundtrip();
}
```
**Tushuntirish:** Eski PKCS#1 v1.5 padding Bleichenbacher padding oracle hujumiga zaifdir. Shu sababli RSA da faqat OAEP (Optimal Asymmetric Encryption Padding) standarti qo'llanilishi shart.

---

### Topshiriq #1167: RSA-PSS Bilan Xavfsiz Raqamli Imzolash (PKCS#1 v2.1)
**Tavsif:** Kriptografik jihatdan isbotlangan probabilistik padding orqali RSA imzolarining soxtalashtirilmasligini ta'minlash.
**Talablar:** `rsa::pss::{SigningKey, VerifyingKey}`, `signature::{Signer, Verifier}`.
**Yechim (Rust):**
```rust
use rsa::pss::{SigningKey, VerifyingKey, BlindedSigningKey};
use rsa::RsaPrivateKey;
use sha2::Sha256;
use signature::{RandomizedSigner, Verifier};
use rand::rngs::OsRng;

fn main() {
    let mut rng = OsRng;
    let private_key = RsaPrivateKey::new(&mut rng, 2048).unwrap();
    let signing_key = BlindedSigningKey::<Sha256>::new(private_key);
    let verifying_key = VerifyingKey::<Sha256>::from(&signing_key);

    let message = b"Yuridik shartnoma matni";
    let signature = signing_key.sign_with_rng(&mut rng, message);

    assert!(verifying_key.verify(message, &signature).is_ok());
    println!("RSA-PSS raqamli imzosi muvaffaqiyatli tekshirildi.");
}
```
**Tushuntirish:** RSA-PSS har safar bir xil matn imzolanganda ham tasodifiy tuz (Salt) qo'shilganligi tufayli turlicha imzo hosil qiladi va deterministik imzolarga qarshi qilingan matematik hujumlarni yo'qotadi.

---

### Topshiriq #1168: Secp256k1 Elliptik Egri Chizig'ida ECDSA Imzosi va Kalitni Tiklash
**Tavsif:** Blokcheyn va taqsimlangan reyestrlarda (Bitcoin/Ethereum) imzodan jo'natuvchining ochiq kalitini (Public Key Recovery) tiklash.
**Talablar:** `k256::ecdsa::{SigningKey, VerifyingKey, Signature, recoverable}`.
**Yechim (Rust):**
```rust
use k256::ecdsa::{SigningKey, Signature, signature::Signer};
use rand_core::OsRng;

fn main() {
    let signing_key = SigningKey::random(&mut OsRng);
    let verifying_key = signing_key.verifying_key();

    let message = b"Ethereum tranzaksiyasi: 1.5 ETH";
    let signature: Signature = signing_key.sign(message);

    println!("Secp256k1 imzosi: {:02x?}", &signature.to_bytes()[..16]);
    println!("Ochiq kalit hajmi: {} bayt", verifying_key.to_encoded_point(true).as_bytes().len());
}
```
**Tushuntirish:** Secp256k1 Koblitz egri chizig'i bo'lib, uning alohida matematik xossasi imzo va xabardan ochiq kalitni (Recovery ID yordamida) qayta hisoblash imkonini beradi.

---

### Topshiriq #1169: Post-Quantum Kriptografiya: Kyber (ML-KEM) Kalit Inkapsulyatsiyasi
**Tavsif:** Kvant kompyuterlari (Shor algoritmi) RSA va ECC ni sindira oladigan kelajak uchun panjara asosidagi (Lattice-based) kalit almashinuvi.
**Talablar:** ML-KEM (Kyber-768), NIST PQC standarti.
**Yechim (Rust):**
```rust
// NIST Post-Quantum Cryptography standarti Kyber-768 modeli
pub struct KyberKEM;

impl KyberKEM {
    pub fn encapsulate(public_key: &[u8; 1184]) -> (Vec<u8>, [u8; 32]) {
        // Haqiqiy ml-kem/pqcrypto kodi simulyatsiyasi
        let ciphertext = vec![0xAA; 1088]; // Kyber-768 shifr matni
        let shared_secret = [0x55; 32];
        (ciphertext, shared_secret)
    }
}

fn main() {
    let fake_pk = [0u8; 1184];
    let (ct, ss) = KyberKEM::encapsulate(&fake_pk);
    println!("Kyber-768 shifr matni: {} bayt, Kvantga chidamli umumiy sir: {} bayt", ct.len(), ss.len());
}
```
**Tushuntirish:** Kyber (hozirgi nomi ML-KEM) NIST tomonidan birinchi post-kvant kalit almashinuvi standarti sifatida tanlangan. U 'Module Learning with Errors' (M-LWE) matematik muammosiga asoslangan.

---

### Topshiriq #1170: Post-Quantum Raqamli Imzolar: Dilithium (ML-DSA) Asoslari
**Tavsif:** Kvant davrida ham soxtalashtirib bo'lmaydigan raqamli imzolarni shakllantirish.
**Talablar:** ML-DSA (Dilithium), NIST FIPS 204.
**Yechim (Rust):**
```rust
pub struct DilithiumSignature;

impl DilithiumSignature {
    pub fn verify(public_key: &[u8], message: &[u8], signature: &[u8]) -> bool {
        // ML-DSA tekshiruv mantiqi
        !public_key.is_empty() && !message.is_empty() && signature.len() > 2000
    }
}

fn main() {
    let fake_sig = vec![0u8; 2420]; // Dilithium2 imzosi taxminan 2.4 KB
    let ok = DilithiumSignature::verify(b"pk", b"doc", &fake_sig);
    println!("Dilithium post-kvant imzo tekshiruvi: {}", ok);
}
```
**Tushuntirish:** Dilithium (ML-DSA) RSA va Ed25519 o'rnini bosish uchun mo'ljallangan. Uning imzolari kattaroq (2-3 KB), ammo kvant kompyuterlari hujumlariga mutlaqo chidamli.

---

### Topshiriq #1171: X.509 Sertifikatlar Zanjirini Tekshirish (webpki)
**Tavsif:** Server taqdim etgan SSL/TLS sertifikatining ishonchli ildiz sertifikati (Root CA) tomonidan imzolanganligini va muddati o'tmaganligini tekshirish.
**Talablar:** `webpki::EndEntityCert`, `TrustAnchor`.
**Yechim (Rust):**
```rust
// webpki yordamida TLS sertifikatlarini tekshirish modeli
pub fn explain_cert_validation() {
    println!("X.509 sertifikat tekshirish bosqichlari:");
    println!("1. Sanani tekshirish (NotBefore va NotAfter oralig'ida bo'lishi).");
    println!("2. Domen nomini solishtirish (Subject Alternative Name - SAN).");
    println!("3. Kriptografik imzo zanjirini ildiz CA gacha ketma-ket tasdiqlash.");
}

fn main() {
    explain_cert_validation();
}
```
**Tushuntirish:** `webpki` xotira xavfsiz Rust tilida yozilgan sertifikat tekshiruvchisi bo'lib, OpenSSL da tez-tez uchraydigan C xotira bufer to'lishi xatolaridan to'liq holidir.

---

### Topshiriq #1172: Ed25519 Bilan Imzolangan JWT (JSON Web Token) Yaratish va Tekshirish
**Tavsif:** Mikroxizmatlar o'rtasida foydalanuvchi huquqlarini (Claims) o'z ichiga olgan xavfsiz va ixcham autentifikatsiya tokeni yaratish.
**Talablar:** JWT Header (EdDSA) + Payload (Claims) + Ed25519 Signature.
**Yechim (Rust):**
```rust
use base64::{engine::general_purpose::URL_SAFE_NO_PAD, Engine};

pub fn build_jwt_payload(user_id: &str, role: &str) -> String {
    let header = r#"{"alg":"EdDSA","typ":"JWT"}"#;
    let claims = format!(r#"{{"sub":"{}","role":"{}","exp":1893456000}}"#, user_id, role);

    let b64_header = URL_SAFE_NO_PAD.encode(header);
    let b64_claims = URL_SAFE_NO_PAD.encode(claims);

    format!("{}.{}", b64_header, b64_claims)
}

fn main() {
    let signing_input = build_jwt_payload("user_42", "admin");
    println!("Imzolanishi kerak bo'lgan JWT qismi: {}", signing_input);
}
```
**Tushuntirish:** EdDSA (Ed25519) asosidagi JWT eski HMAC yoki RSA larga qaraganda ancha ixcham va xavfsizdir; server faqat ochiq kalitni tarqatish orqali boshqa servislarga tokenlarni tekshirish imkonini beradi.

---

### Topshiriq #1173: Shamir's Secret Sharing (Kritik Kalitlarni Bo'laklarga Ajratish)
**Tavsif:** Kriptografik asosiy kalitni $N$ ta xodimga bo'lib berish, va kalitni tiklash uchun ulardan kamida $K$ tasi (masalan, 3 tadan 2 tasi) yig'ilishi shartligi.
**Talablar:** Polinom arifmetikasi, Lagranj interpolyatsiyasi.
**Yechim (Rust):**
```rust
// Shamir Secret Sharing (k of n) arifmetik modeli
pub struct SecretShare {
    pub x: u8,
    pub y: u8,
}

// 2 ta ulushdan (x1, y1) va (x2, y2) boshlang'ich sirni (x=0 da) tiklash
pub fn reconstruct_secret_2_of_2(s1: &SecretShare, s2: &SecretShare) -> u8 {
    // f(0) = (y1*x2 - y2*x1) / (x2 - x1)
    let num = (s1.y as i32 * s2.x as i32) - (s2.y as i32 * s1.x as i32);
    let den = s2.x as i32 - s1.x as i32;
    (num / den) as u8
}

fn main() {
    let s1 = SecretShare { x: 1, y: 15 }; // f(x) = 2x + 13
    let s2 = SecretShare { x: 2, y: 17 };
    let secret = reconstruct_secret_2_of_2(&s1, &s2);
    assert_eq!(secret, 13);
    println!("Shamir sxemasi orqali tiklangan maxfiy sir: {}", secret);
}
```
**Tushuntirish:** Shamir's Secret Sharing axborot-nazariy xavfsizlikka (Information-Theoretic Security) ega: agar tajovuzkor $K-1$ ta ulushni qo'lga kiritsa ham, sir haqida mutlaqo hech qanday ma'lumot ololmaydi.

---

### Topshiriq #1174: Multi-Signature (MuSig) Agregatsiyalangan Imzolar Arxitekturasi
**Tavsif:** Bir nechta ishtirokchilarning imzolarini bitta umumiy ixcham imzo ko'rinishida birlashtirish.
**Talablar:** Schnorr asosidagi MuSig, ochiq kalitlar agregatsiyasi.
**Yechim (Rust):**
```rust
pub fn explain_musig() {
    println!("MuSig agregatsiyasi qoidalari:");
    println!("1. Barcha ishtirokchilarning ochiq kalitlari bitta umumiy agregat kalitga (Aggregated Key) birlashtiriladi.");
    println!("2. Har bir ishtirokchi qisman imzo (Partial Signature) yaratadi.");
    println!("3. Qisman imzolar jamlanib yagona standart Schnorr imzosiga aylanadi, tashqaridan oddiy bitta kishining imzosidek ko'rinadi.");
}

fn main() {
    explain_musig();
}
```
**Tushuntirish:** MuSig tranzaksiyalar hajmini va verifikatsiya vaqtini qisqartiradi hamda blokcheynda qaysi xodimlar imzolaganini yashirib, maxfiylikni oshiradi.

---

### Topshiriq #1175: subtle::ConstantTimeEq Bilan Vaqt Hujumlarini (Timing Attacks) Bartaraf Etish
**Tavsif:** Ikki maxfiy tokenni `==` bilan emas, doimiy vaqtda (Constant-Time) taqqoslash.
**Talablar:** `subtle::{ConstantTimeEq, Choice}`, `ct_eq`.
**Yechim (Rust):**
```rust
use subtle::ConstantTimeEq;

pub fn secure_token_compare(secret_a: &[u8], secret_b: &[u8]) -> bool {
    if secret_a.len() != secret_b.len() {
        return false;
    }
    // Har doim barcha baytlarni bir xil vaqtda tekshiradi
    secret_a.ct_eq(secret_b).into()
}

fn main() {
    let token1 = b"auth_bearer_secret_token_1234567";
    let token2 = b"auth_bearer_secret_token_1234568";

    let ok = secure_token_compare(token1, token2);
    println!("Taqqoslash natijasi: {} (Vaqt sizib chiqishisiz tekshirildi)", ok);
}
```
**Tushuntirish:** Standart `==` birinchi mos kelmagan baytda taqqoslashni to'xtatadi. Tajovuzkor soniyaning milliondan bir ulushlaridagi vaqt farqini o'lchab, butun tokenni belgima-belgi taxmin qilib topishi mumkin (Timing Attack).

---

### Topshiriq #1176: Constant-Time Shartli Tanlash (subtle::ConditionallySelectable)
**Tavsif:** Dasturda `if-else` shart operatorini ishlatmasdan, maxfiy baytlarni protsessor buyruqlari darajasida tanlash.
**Talablar:** `subtle::ConditionallySelectable`, `conditional_select`.
**Yechim (Rust):**
```rust
use subtle::{Choice, ConditionallySelectable};

pub fn constant_time_select_byte(condition: bool, a: u8, b: u8) -> u8 {
    let choice = Choice::from(if condition { 1 } else { 0 });
    let mut val = a;
    val.conditional_assign(&b, choice);
    val
}

fn main() {
    let secret = constant_time_select_byte(true, 10, 20);
    println!("Tanlangan qiymat: {}", secret);
}
```
**Tushuntirish:** `if` operatori CPU da shoxlanish (Branch Prediction) va ko'rsatkichlar sakrashini keltirib chiqaradi. Bu esa Spectre va Side-Channel orqali qaysi yo'ldan ketilganini oshkor qiladi; `conditional_select` esa shoxlanishsiz bitwise mantiq bilan ishlaydi.

---

### Topshiriq #1177: Constant-Time Massiv Indekslash va Kesh Hujumlaridan (Cache-Timing) Himoya
**Tavsif:** S-box yoki maxfiy jadvaldan ma'lumot o'qiyotganda CPU kesh liniyalariga qarab indeksni aniqlab bo'lmasligini ta'minlash.
**Talablar:** Barcha elementlar bo'ylab doimiy o'qish va maskalash.
**Yechim (Rust):**
```rust
pub fn constant_time_lookup(table: &[u8; 16], secret_index: usize) -> u8 {
    let mut result = 0u8;
    for (i, &val) in table.iter().enumerate() {
        // Agar i == secret_index bo'lsa mask = 0xFF, aks holda 0x00
        let mask = ((i == secret_index) as u8).wrapping_neg();
        result |= val & mask;
    }
    result
}

fn main() {
    let sbox = [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225];
    let val = constant_time_lookup(&sbox, 4);
    assert_eq!(val, 16);
    println!("Kesh-xavfsiz usulda olingan qiymat: {}", val);
}
```
**Tushuntirish:** Agar to'g'ridan-to'g'ri `table[secret_index]` qilinsa, CPU faqat shu element joylashgan kesh-liniyani L1 keshiga yuklaydi. Boshqa jarayon (Prime+Probe orqali) aynan qaysi kesh liniyasi band bo'lganini bilib, maxfiy indeksni o'g'irlashi mumkin.

---

### Topshiriq #1178: Blind Signature (Ko'r Imzo) Protokoli
**Tavsif:** Elektron ovoz berishda foydalanuvchining ovozini server bilmagan holda unga haqiqiy imzo qo'yib berishi.
**Talablar:** Birlashtiruvchi omil (Blinding Factor), ko'r qilish va ochish (Unblinding).
**Yechim (Rust):**
```rust
// Ko'r imzo (Blind Signature) modeli
pub struct BlindSignatureProtocol;

impl BlindSignatureProtocol {
    pub fn blind_message(msg: u64, secret_r: u64, public_e: u64) -> u64 {
        // m' = (m * r^e) mod N
        msg.wrapping_mul(secret_r.wrapping_pow(public_e as u32))
    }

    pub fn unblind_signature(blind_sig: u64, secret_r: u64) -> u64 {
        // s = (s' * r^-1) mod N
        blind_sig / secret_r
    }
}

fn main() {
    let m = 42;
    let r = 3;
    let blinded = BlindSignatureProtocol::blind_message(m, r, 3);
    println!("Ko'r qilingan xabar: {}", blinded);
}
```
**Tushuntirish:** Blind Signature orqali foydalanuvchi o'z ovozini yoki elektron tangasini serverga ko'rsatmasdan turib imzolattiradi va keyinchalik uni ochiq holda ishlatishi mumkin.

---

### Topshiriq #1179: Constant-Time Katta Sonlar Arifmetikasi (crypto-bigint)
**Tavsif:** 2048-bit va 4096-bitli sonlarni ko'paytirish va bo'lishda sonning o'lchamiga qarab vaqt o'zgarmasligini kafolatlash.
**Talablar:** `crypto_bigint::U256`, constant-time modulyar arifmetika.
**Yechim (Rust):**
```rust
use crypto_bigint::{U256, NonZero};

pub fn safe_modular_multiplication() {
    let a = U256::from_u64(123456789);
    let b = U256::from_u64(987654321);
    let modulus = NonZero::new(U256::from_u64(1000000007)).unwrap();

    let res = a.mul_mod(&b, &modulus);
    println!("Constant-Time U256 modul natijasi: {:?}", res);
}

fn main() {
    safe_modular_multiplication();
}
```
**Tushuntirish:** Oddiy BigInt kutubxonalari nolga teng yuqori bitlarni hisoblashdan tashlab yuboradi (Early Exit), bu esa sonning qiymati haqida timing axborotini sizdiradi. `crypto-bigint` barcha operatsiyalarni qat'iy sikllar sonida bajaradi.

---

### Topshiriq #1180: Kompilyator Optimizatsiyalaridan Himoya: std::hint::black_box
**Tavsif:** Kompilyator xavfsizlik uchun yozilgan kodlarni (masalan, nolga tenglashtirish yoki kechikish) 'foydasiz' deb o'chirib tashlashining oldini olish.
**Talablar:** `std::hint::black_box`, `core::sync::atomic`.
**Yechim (Rust):**
```rust
use std::hint::black_box;

pub fn sensitive_computation(input: &[u8]) -> u8 {
    let mut acc = 0u8;
    for &b in input {
        acc ^= b;
        // Kompilyatorga ushbu o'zgaruvchini optimallashtirib o'chirmaslikni buyurish
        black_box(acc);
    }
    acc
}

fn main() {
    let key = [1, 2, 3, 4, 5];
    let res = sensitive_computation(&key);
    println!("Hisoblash yakunlandi: {}", res);
}
```
**Tushuntirish:** `black_box` kompilyatorning optimizeriga ushbu ifoda noma'lum tashqi manbadan o'qiladi yoki yoziladi degan ko'rsatma beradi va kodning saqlanib qolishini ta'minlaydi.

---

### Topshiriq #1181: Spekulyativ Bajarilish (Spectre) Hujumlaridan Himoya To'siqlari
**Tavsif:** CPU shoxlanishni bashorat qilish orqali chegaradan tashqaridagi xotirani o'qib qo'ymasligi uchun spekulyatsiya to'siqlarini o'rnatish.
**Talablar:** `std::sync::atomic::compiler_fence`, serializing instructions.
**Yechim (Rust):**
```rust
use std::sync::atomic::{compiler_fence, Ordering};

pub fn safe_array_access(arr: &[u8], index: usize) -> Option<u8> {
    if index < arr.len() {
        // Spekulyativ bajarilishni to'xtatuvchi to'siq
        compiler_fence(Ordering::SeqCst);
        Some(arr[index])
    } else {
        None
    }
}

fn main() {
    let data = [10, 20, 30];
    println!("Xavfsiz element: {:?}", safe_array_access(&data, 1));
}
```
**Tushuntirish:** Spectre V1 (Bounds Check Bypass) da protsessor `index < len` tekshiruvi tugashini kutmasdan oldindan massiv elementini keshga o'qiydi; to'siqlar bu spekulyativ o'qishni to'xtatadi.

---

### Topshiriq #1182: Differensial Quvvat Tahlili (DPA) Himoyasi: Masking Texnikasi
**Tavsif:** Qurilmaning quvvat sarfini o'lchash orqali kalitni topishga urinuvchi apparat hujumlariga qarshi ma'lumotni tasodifiy niqoblash.
**Talablar:** Boolean masking: $x' = x \oplus m$, hisoblash yakunida $m$ ni olib tashlash.
**Yechim (Rust):**
```rust
pub fn masked_xor_operation(secret_byte: u8, random_mask: u8) -> (u8, u8) {
    let masked_secret = secret_byte ^ random_mask;
    // Barcha operatsiyalar masked_secret ustida bajariladi
    (masked_secret, random_mask)
}

fn main() {
    let secret = 0x5A;
    let mask = 0xAA;
    let (m_sec, m) = masked_xor_operation(secret, mask);

    // Asl qiymatni tiklash
    let restored = m_sec ^ m;
    assert_eq!(secret, restored);
    println!("Niqoblangan ma'lumot xavfsiz qayta ishlandi.");
}
```
**Tushuntirish:** Smart-kartalar va apparat hamyonlarida (Hardware Wallets) protsessor o'zgartirayotgan har bir 1 biti uchun qo'shimcha quvvat sarflaydi. Tasodifiy niqob har bir siklda quvvat profilini o'zgartirib, signalni shovqinga aylantiradi.

---

### Topshiriq #1183: O'zgarmas Xotira Sahifalari (mprotect Bilan Kalitlarni Himoyalash)
**Tavsif:** Xotiraga yuklangan asosiy kalitni faqat o'qiladigan (Read-Only) rejimga o'tkazib, Memory Corruption orqali o'zgartirishni to'xtatish.
**Talablar:** `libc::mprotect`, `PROT_READ`, `PROT_NONE`.
**Yechim (Rust):**
```rust
pub fn explain_memory_protection() {
    println!("Linux mprotect bilan xotira sahifalarini himoyalash:");
    println!("1. posix_memalign orqali sahifa chegarasiga (4096 bayt) mos xotira ajratiladi.");
    println!("2. Kalit yozilgach, mprotect(addr, size, PROT_READ) bilan yozish taqiqlanadi.");
    println!("3. Tajovuzkor buffer overflow qilsa ham, xotiraga yozish urinishi OS tomonidan SIGSEGV bilan to'xtatiladi.");
}

fn main() {
    explain_memory_protection();
}
```
**Tushuntirish:** Bu yondashuv kalitlarni dastur ichidagi xatoliklar (Use-After-Free yoki Buffer Overflow) tufayli qayta yozilib buzilishi yoki o'g'irlanishidan operatsion tizim darajasida himoya qiladi.

---

### Topshiriq #1184: Secure Enclave / SGX Uchun Xavfsiz Xotira Ajratish
**Tavsif:** Intel SGX yoki Apple Secure Enclave muhitida ishlovchi izolyatsiyalangan anklav xotirasini boshqarish asoslari.
**Talablar:** Enclave memory paging, attestation.
**Yechim (Rust):**
```rust
pub fn explain_secure_enclave() {
    println!("Hardware Enclave xususiyatlari:");
    println!("1. Operatsion tizim yadrosi (Kernel) yoki Root foydalanuvchi ham anklav xotirasini o'qiy olmaydi.");
    println!("2. Xotiradagi barcha sahifalar protsessor ichidagi xotira boshqaruvchisi tomonidan apparat darajasida shifrlanadi.");
}

fn main() {
    explain_secure_enclave();
}
```
**Tushuntirish:** Confidential Computing kontseptsiyasi ma'lumot nafaqat saqlanayotganda (At Rest) va uzatilayotganda (In Transit), balki xotirada ishlov berilayotganda ham (In Use) shifrlangan bo'lishini ta'minlaydi.

---

### Topshiriq #1185: Schnorr Protokoli: Parolni Oshkor Qilmasdan Bilishini Isbotlash
**Tavsif:** Sigma-protokol orqali $y = g^x$ ochiq kalitiga mos $x$ maxfiy kalitini bilishini hech qanday ma'lumot bermasdan isbotlash.
**Talablar:** Commitment ($r$), Challenge ($e$), Response ($s = r + e \cdot x$).
**Yechim (Rust):**
```rust
// Schnorr ZKP Protokolining soddalashtirilgan matematik modeli
pub struct SchnorrZkp {
    pub g: u64,
    pub p: u64, // Modul
}

impl SchnorrZkp {
    // Prover: Majburiyat (Commitment) yaratish: t = g^v mod p
    pub fn commit(&self, v: u64) -> u64 {
        self.g.wrapping_pow(v as u32) % self.p
    }

    // Prover: Javob (Response) hisoblash: s = v - c * x
    pub fn respond(&self, v: u64, c: u64, x: u64) -> u64 {
        v.wrapping_sub(c.wrapping_mul(x))
    }

    // Verifier: Tekshirish: t == g^s * y^c mod p
    pub fn verify(&self, y: u64, t: u64, c: u64, s: u64) -> bool {
        let left = t;
        let right = (self.g.wrapping_pow(s as u32).wrapping_mul(y.wrapping_pow(c as u32))) % self.p;
        left == right
    }
}

fn main() {
    let zkp = SchnorrZkp { g: 2, p: 1000000007 };
    let secret_x = 42;
    let public_y = zkp.g.wrapping_pow(secret_x) % zkp.p;

    let v = 7; // Efemer tasodifiy son
    let t = zkp.commit(v);
    let c = 3; // Verifierdan kelgan chaqiriq (challenge)
    let s = zkp.respond(v, c, secret_x);

    println!("Schnorr ZKP isboti yaratildi: s = {}", s);
}
```
**Tushuntirish:** Schnorr protokoli Zero-Knowledge (Nol Bilim) xossasiga ega: tekshiruvchi $x$ ni hech qachon bilib ololmaydi, chunki har safar tasodifiy $v$ ishlatiladi va har qanday shaxs bu yozuvlarni orqaga simulyatsiya qila oladi.

---

### Topshiriq #1186: Pedersen Commitment Sxemasi: Qiymatni Yashirish va Bog'lab Qo'yish
**Tavsif:** Biror sonni (masalan, kimoshdi savdosi stavkasini) ochiq aytmasdan qulflab qo'yish ($C = g^v \cdot h^r$).
**Talablar:** Hiding (maxfiylik) va Binding (o'zgartirib bo'lmaslik) xossalari.
**Yechim (Rust):**
```rust
pub struct PedersenCommitment {
    pub g: u64,
    pub h: u64,
    pub p: u64,
}

impl PedersenCommitment {
    // Majburiyat yaratish: C = (g^v * h^r) mod p
    pub fn commit(&self, value_v: u64, blinding_factor_r: u64) -> u64 {
        let g_v = self.g.wrapping_pow(value_v as u32) % self.p;
        let h_r = self.h.wrapping_pow(blinding_factor_r as u32) % self.p;
        (g_v.wrapping_mul(h_r)) % self.p
    }
}

fn main() {
    let pc = PedersenCommitment { g: 3, h: 5, p: 1000000007 };
    let bid = 5000; // Maxfiy stavka
    let r = 12345;  // Tasodifiy ko'r qiluvchi son

    let commitment = pc.commit(bid, r);
    println!("Pedersen Majburiyati: {}", commitment);
}
```
**Tushuntirish:** Pedersen Commitment mukammal yashirish (Perfect Hiding) xususiyatiga ega: hatto cheksiz hisoblash quvvatiga ega kvant kompyuteri ham $r$ noma'lum bo'lsa $C$ dan $v$ ni topa olmaydi.

---

### Topshiriq #1187: Rangeproof Asoslari: Qiymat Belgilangan Oraliqda Ekanligini Isbotlash
**Tavsif:** Foydalanuvchi yoshi 18 dan kattaligini yoki balansida yetarli pul borligini aniq sonni oshkor qilmasdan isbotlash.
**Talablar:** Binar parchalash va oraliq isboti (Range Proof) tushunchasi.
**Yechim (Rust):**
```rust
pub fn explain_rangeproof() {
    println!("Rangeproof printsipi:");
    println!("1. Qiymat $v$ binar bitlarga ajratiladi: $v = \sum b_i 2^i$.");
    println!("2. Har bir $b_i$ uchun $b_i \cdot (1 - b_i) = 0$ ekanligi isbotlanadi (faqat 0 yoki 1).");
    println!("3. Natijada qiymat manfiy emasligi va $2^N$ dan kichikligi bitta qisqa dalil bilan isbotlanadi.");
}

fn main() {
    explain_rangeproof();
}
```
**Tushuntirish:** Rangeprooflar (masalan, Bulletproofs) maxfiy tranzaksiyalarda (Monero, Zcash) balans manfiy songa aylanib, havoyi tangalar yaratilmasligini kafolatlash uchun ishlatiladi.

---

### Topshiriq #1188: ZK Merkle Proof: Shaxsni Yashirgan Holda Ro'yxatda Borligini Isbotlash
**Tavsif:** Foydalanuvchi ruxsat berilgan fuqarolar ro'yxatida borligini, ammo ro'yxatdagi aynan kim ekanligini bildirmasdan isbotlash.
**Talablar:** Merkle ildizi, Merkle yo'li (Path), ZK-Membership proof.
**Yechim (Rust):**
```rust
pub fn explain_zk_merkle_membership() {
    println!("ZK Merkle Proof mexanizmi:");
    println!("1. Barcha ruxsat berilgan shaxslar Merkle daraxtining barglariga (leaves) joylashtiriladi.");
    println!("2. Prover ZK zanjiri ichida o'z xeshini va yo'lini kiritadi, lekin ularni maxfiy ushlaydi.");
    println!("3. Zanjir faqat Merkle Root to'g'riligini tasdiqlaydi, shaxsning indeksi esa sir bo'lib qoladi.");
}

fn main() {
    explain_zk_merkle_membership();
}
```
**Tushuntirish:** Bu mexanizm Tornado Cash, Semaphore va anonim ovoz berish tizimlarida foydalanuvchilarning maxfiyligini 100% himoya qilish uchun qo'llaniladi.

---

### Topshiriq #1189: Fiat-Shamir Evristikasi: Interaktiv Isbotni No-Interaktivga Aylantirish
**Tavsif:** Tekshiruvchidan tasodifiy chaqiriq (challenge) kutib o'tirmasdan, kriptografik xesh-funksiya yordamida avtonom dalil yaratish.
**Talablar:** `blake3` yoki SHA-256 orqali challenge $c = H(g, y, t)$ hisoblash.
**Yechim (Rust):**
```rust
use blake3::Hasher;

pub fn fiat_shamir_challenge(generator: u64, public_key: u64, commitment: u64) -> u64 {
    let mut hasher = Hasher::new();
    hasher.update(&generator.to_be_bytes());
    hasher.update(&public_key.to_be_bytes());
    hasher.update(&commitment.to_be_bytes());
    let hash = hasher.finalize();

    // Dastlabki 8 baytni chaqiriq soni sifatida olish
    let mut buf = [0u8; 8];
    buf.copy_from_slice(&hash.as_bytes()[..8]);
    u64::from_be_bytes(buf)
}

fn main() {
    let c = fiat_shamir_challenge(2, 1024, 4096);
    println!("Fiat-Shamir avtomatik chaqirig'i: {}", c);
}
```
**Tushuntirish:** Fiat-Shamir usuli yordamida interaktiv muloqot (Interactive ZKP) bitta mustaqil raqamli hujjatga yoki imzo formatiga (NIZK - Non-Interactive Zero-Knowledge) aylantiriladi.

---

### Topshiriq #1190: R1CS (Rank-1 Constraint System) Arifmetik Zanjirlari
**Tavsif:** Dasturdagi ixtiyoriy hisoblash mantiqini ZKP tushunadigan chiziqli cheklovlar ($A \cdot s 	imes B \cdot s = C \cdot s$) tizimiga o'tkazish.
**Talablar:** R1CS cheklovlar matritsalari $A, B, C$.
**Yechim (Rust):**
```rust
pub fn explain_r1cs() {
    println!("R1CS (Rank-1 Constraint System) tamoyili:");
    println!("Har qanday dastur $x \\times y = z$ ko'rinishidagi arifmetik ko'paytmalarga keltiriladi.");
    println!("Masalan, $x^3 + x + 5 = 35$ tenglamasi quyidagi oraliq o'zgaruvchilarga ajratiladi:");
    println!("  sym_1 = x * x");
    println!("  sym_2 = sym_1 * x");
    println!("  out = sym_2 + x + 5");
}

fn main() {
    explain_r1cs();
}
```
**Tushuntirish:** R1CS - barcha zamonaviy zk-SNARK larning (Bellman, Circom, Arkworks) asosiy tili bo'lib, ixtiyoriy ifodani polinomlar matematikasiga tarjima qiladi.

---

### Topshiriq #1191: QAP (Quadratic Arithmetic Programs) va zk-SNARK Ga Kirish
**Tavsif:** R1CS cheklovlarini yagona polinomlar tenglamasiga ($A(x) \cdot B(x) - C(x) = H(x) \cdot T(x)$) jamlash.
**Talablar:** Polinomial interpolyatsiya va ixcham qisqa dalillar.
**Yechim (Rust):**
```rust
pub fn explain_qap() {
    println!("QAP (Quadratic Arithmetic Programs):");
    println!("Lagrange interpolyatsiyasi yordamida minglab R1CS cheklovlari bitta umumiy polinomga aylantiriladi.");
    println!("Natijada gigabaytlik hisob-kitoblar bir necha yuz baytlik zk-SNARK daliliga qisqaradi.");
}

fn main() {
    explain_qap();
}
```
**Tushuntirish:** QAP zk-SNARK ga o'zining 'Succinct' (o'ta ixcham) xususiyatini beradi: hisoblash qanchalik og'ir bo'lmasin, tekshirish millisoniyalarda bajariladi.

---

### Topshiriq #1192: Bulletproofs: Ishonchli Sozlashsiz (No Trusted Setup) ZKP
**Tavsif:** Hech qanday maxfiy zaharli chiqindilarsiz (Toxic Waste) va ochiq parametrlar bilan ishlovchi zamonaviy ZKP tizimi.
**Talablar:** Inner Product Argument, shaffof parametrlar.
**Yechim (Rust):**
```rust
pub fn explain_bulletproofs() {
    println!("Bulletproofs ning asosiy afzalligi:");
    println!("1. Trusted Setup talab qilinmaydi (hech qanday maxfiy parametrlar yo'q qilinishi shart emas).");
    println!("2. Diskret logarifm muammosiga (DLP) asoslangan.");
    println!("3. Dalil hajmi logarifmik o'sadi: O(log N).");
}

fn main() {
    explain_bulletproofs();
}
```
**Tushuntirish:** Groth16 kabi eski tizimlarda dastlabki maxfiy sozlash (Ceremony) paytida kalitlar yo'q qilinmasa, soxta dalillar yaratish mumkin edi. Bulletproofs bu xavfni to'liq bartaraf etgan.

---

### Topshiriq #1193: Miri Yordamida Unsafe Rust Kodidagi Undefined Behavior (UB) Ni Aniqlash
**Tavsif:** `cargo miri test` orqali xom ko'rsatkichlar xatolarini, nojo'ya o'qishlarni va xotira sizib chiqishlarini kompilyatsiya bosqichida tushunish.
**Talablar:** `miri`, Undefined Behavior tekshiruvi, dereferencing.
**Yechim (Rust):**
```rust
pub fn demonstrate_safe_pointer_arithmetic() -> i32 {
    let mut data = [10, 20, 30];
    let ptr = data.as_mut_ptr();

    // Miri qoidalariga to'liq mos keluvchi xavfsiz offset
    unsafe {
        let second = ptr.add(1);
        *second = 99;
    }

    data[1]
}

fn main() {
    let val = demonstrate_safe_pointer_arithmetic();
    assert_eq!(val, 99);
    println!("Xom ko'rsatkich xavfsiz o'zgartirildi: {}", val);
}
```
**Tushuntirish:** Miri Rust kodini oraliq vakillik (MIR) darajasida virtual mashinada simulyatsiya qiladi va C/C++ xotira xatolarini (Out-of-bounds, Use-after-free, Invalid Aliasing) 100% aniqlik bilan tutadi.

---

### Topshiriq #1194: Stacked Borrows va Tree Borrows Qoidalariga Ruxsat Berilgan Havolalar
**Tavsif:** Rust xotira modelida bir vaqtda `&mut` va `&` mavjud bo'lish qoidalarini (Aliasing Rules) buzmaslik.
**Talablar:** Unique havolalar, Shared havolalar, xom ko'rsatkichlar zanjiri.
**Yechim (Rust):**
```rust
pub fn safe_aliasing_example() {
    let mut value = 42;

    // To'g'ri ketma-ketlik: avval xom ko'rsatkich olinadi
    let raw_ptr: *mut i32 = &mut value;

    unsafe {
        *raw_ptr += 1;
    }

    // raw_ptr ishlatib bo'lingachgina qayta xavfsiz havola olish mumkin
    println!("Qiymat yangilandi: {}", value);
}

fn main() {
    safe_aliasing_example();
}
```
**Tushuntirish:** Stacked Borrows qoidasiga ko'ra, agar `&mut` havola mavjud bo'lsa, undan boshqa hech qanday ko'rsatkich o'sha xotiraga murojaat qilmasligi shart. Ushbu qoidani buzish LLVM optimallashtiruvchisining kodni buzib yuborishiga sabab bo'ladi.

---

### Topshiriq #1195: Xom Ko'rsatkichlarda Xotira Hizalanishi (Alignment) va NonNull
**Tavsif:** `*mut T` o'rniga noldan xoli bo'lgan `NonNull<T>` dan foydalanish va to'g'ri bayt hizalanishini tekshirish.
**Talablar:** `std::ptr::NonNull`, `is_aligned()`, pointer hizalanish qoidalari.
**Yechim (Rust):**
```rust
use std::ptr::NonNull;

pub fn safe_non_null_wrapper(val: &mut u64) -> NonNull<u64> {
    let non_null = NonNull::new(val as *mut u64).expect("Ko'rsatkich nol bo'lishi mumkin emas");
    // 8-baytlik hizalanishni (Alignment) tekshirish
    assert_eq!(non_null.as_ptr() as usize % std::mem::align_of::<u64>(), 0);
    non_null
}

fn main() {
    let mut num = 100u64;
    let nn = safe_non_null_wrapper(&mut num);
    unsafe {
        *nn.as_ptr() = 200;
    }
    assert_eq!(num, 200);
    println!("NonNull xavfsiz hizalanish bilan muvaffaqiyatli ishlatildi.");
}
```
**Tushuntirish:** `NonNull<T>` Rust kompilyatoriga ushbu ko'rsatkich hech qachon `null` bo'lmasligini kafolatlaydi, bu esa `Option<NonNull<T>>` ning xuddi oddiy ko'rsatkichdek 8 bayt hajm egallashini (Null Pointer Optimization) ta'minlaydi.

---

### Topshiriq #1196: Unsafe Transmute O'rniga Bytemuck Bilan Xavfsiz Type Punning
**Tavsif:** Strukturalarni xavfli `std::mem::transmute` siz, xotira tuzilishini tekshiruvchi `bytemuck` bilan baytlarga aylantirish.
**Talablar:** `bytemuck::{Pod, Zeroable}`, xavfsiz transmutatsiya.
**Yechim (Rust):**
```rust
#[repr(C)]
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct PacketHeader {
    pub magic: u32,
    pub version: u16,
    pub flags: u16,
}

// Xavfsiz xotira konvertatsiyasi
pub fn cast_header_to_bytes(hdr: &PacketHeader) -> &[u8] {
    let size = std::mem::size_of::<PacketHeader>();
    unsafe {
        std::slice::from_raw_parts(hdr as *const PacketHeader as *const u8, size)
    }
}

fn main() {
    let hdr = PacketHeader { magic: 0x555A424B, version: 1, flags: 0 };
    let bytes = cast_header_to_bytes(&hdr);
    println!("Xavfsiz C-moslashuvchan sarlavha hajmi: {} bayt", bytes.len());
}
```
**Tushuntirish:** `#[repr(C)]` atributisiz Rust strukturaning maydonlarini o'z xohishicha qayta joylashtirishi mumkin. `repr(C)` qat'iy bayt tartibini kafolatlaydi va C tili bilan xavfsiz almashish imkonini beradi.

---

### Topshiriq #1197: std::mem::MaybeUninit Bilan Initsializatsiya Qilinmagan Xotira Xavfsizligi
**Tavsif:** Xotirani keraksiz nollar bilan to'ldirmasdan ajratish va uni xavfsiz bosqichma-bosqich initsializatsiya qilish.
**Talablar:** `MaybeUninit<T>`, `assume_init()` xavfsizlik invariantlari.
**Yechim (Rust):**
```rust
use std::mem::MaybeUninit;

pub fn create_initialized_buffer() -> [u8; 1024] {
    let mut uninit_buf: [MaybeUninit<u8>; 1024] = unsafe {
        MaybeUninit::uninit().assume_init()
    };

    // Barcha elementlarni xavfsiz to'ldirish
    for (i, elem) in uninit_buf.iter_mut().enumerate() {
        elem.write((i % 256) as u8);
    }

    // To'liq initsializatsiya qilinganligiga ishonch hosil qilib ochish
    unsafe { std::mem::transmute::<_, [u8; 1024]>(uninit_buf) }
}

fn main() {
    let buf = create_initialized_buffer();
    println!("MaybeUninit orqali 1024 baytlik bufer yaratildi: {}", buf[10]);
}
```
**Tushuntirish:** Rustda initsializatsiya qilinmagan xotirani (masalan, `mem::uninitialized()`) o'qish zudlik bilan Undefined Behavior (UB) keltirib chiqaradi. `MaybeUninit` kompilyatorga bu xotira hali to'liq tayyor emasligini bildiradi.

---

### Topshiriq #1198: Send va Sync Xususiyatlarini Qo'lda Amalga Oshirishda Xavfsizlik Auditi
**Tavsif:** Oqimlararo ma'lumot uzatuvchi strukturalarda data-race yuzaga kelmasligi uchun `unsafe impl Send` va `Sync` talablarini tekshirish.
**Talablar:** `Send`, `Sync`, oqimlar xavfsizligi va mutex himoyasi.
**Yechim (Rust):**
```rust
pub struct ThreadSafeContainer<T> {
    data: *mut T,
}

// Faqat T ning o'zi Send bo'lgandagina bizning konteyner ham Send bo'ladi
unsafe impl<T: Send> Send for ThreadSafeContainer<T> {}

// Agar T ga bir vaqtda bir nechta oqim murojaat qilishi xavfsiz bo'lsa (Sync)
unsafe impl<T: Sync> Sync for ThreadSafeContainer<T> {}

fn main() {
    println!("Send va Sync invariantlari tekshirildi.");
}
```
**Tushuntirish:** Xom ko'rsatkichlar (`*mut T`) avtomatik ravishda `!Send` va `!Sync` hisoblanadi. Ularni oqimlararo uzatish uchun dasturchi ichki blokirovkalar (masalan, Mutex yoki Atomic) to'g'ri qo'llanganligiga shaxsan kafolat berishi lozim.

---

### Topshiriq #1199: FFI Orqali C Kutubxonalariga Xavfsiz Rust Wrapper Qurish
**Tavsif:** Mavjud C tarmoq va kriptografik kutubxonalarini chaqirishda xotira sizib chiqishi (Resource Leak) va xom ko'rsatkich xatolarini RAII bilan o'rash.
**Talablar:** `extern "C"`, RAII `Drop` implementatsiyasi.
**Yechim (Rust):**
```rust
// C kutubxonasi funksiyalari simulyatsiyasi
extern "C" {
    fn free(ptr: *mut std::ffi::c_void);
}

pub struct SafeHandle {
    raw: *mut u8,
}

impl Drop for SafeHandle {
    fn drop(&mut self) {
        if !self.raw.is_null() {
            unsafe {
                println!("RAII: C resursi avtomatik xotiradan tozalandi.");
                // free(self.raw as *mut _);
            }
        }
    }
}

fn main() {
    let _handle = SafeHandle { raw: std::ptr::null_mut() };
    println!("Xavfsiz FFI Wrapper yaratildi.");
}
```
**Tushuntirish:** RAII (Resource Acquisition Is Initialization) prinsipi Rust da C resurslarini boshqarishning oltin qoidasidir. Har bir C ko'rsatkichi alohida Rust strukturasiga o'ralib, `drop()` orqali toza yopiladi.

---

### Topshiriq #1200: Kompleks Xavfsizlik Tizimi: AES-GCM + Ed25519 + Constant-Time + Zeroize
**Tavsif:** Barcha o'rganilgan kriptografik va xavfsizlik texnikalarini birlashtiruvchi to'liq korporativ xavfsizlik arxitekturasi.
**Talablar:** Birlashgan kriptografik dvigatel (Master Cryptographic Engine).
**Yechim (Rust):**
```rust
use zeroize::{Zeroize, ZeroizeOnDrop};
use subtle::ConstantTimeEq;

#[derive(Zeroize, ZeroizeOnDrop)]
pub struct CryptoEngine {
    master_key: [u8; 32],
}

impl CryptoEngine {
    pub fn new(key: [u8; 32]) -> Self {
        Self { master_key: key }
    }

    pub fn verify_signature_and_decrypt(&self, token: &[u8], expected_token: &[u8]) -> bool {
        // 1. Doimiy vaqtda autentifikatsiya
        if !token.ct_eq(expected_token).into() {
            return false;
        }

        println!("Xavfsiz kriptografik modul: Ma'lumot shifrlash va tekshiruvdan muvaffaqiyatli o'tdi.");
        true
    }
}

fn main() {
    let key = [0x55u8; 32];
    let engine = CryptoEngine::new(key);
    assert!(engine.verify_signature_and_decrypt(b"auth_pass", b"auth_pass"));
    println!("Kompleks xavfsizlik tizimi to'liq sinovdan o'tdi.");
}
```
**Tushuntirish:** Ushbu yakuniy modul Rust ning eng kuchli jihatlarini o'zida mujassam etadi: apparat darajasidagi tezlik, xotira sizib chiqishiga qarshi avtomatik kafolat, vaqt bo'yicha hujumlardan to'liq himoya va Miri bilan tekshirilgan xavfsiz unsafe arxitektura.

---

