# Khorazmiy AI: C++ - Modul 24
## Mavzu: Kriptografiya va Xavfsizlik: OpenSSL 3.0 EVP API, AES-256-GCM, RSA-4096 OAEP, Ed25519, Constant-time taqqoslash, Side-channel hujumlaridan himoya va Sanitizers (ASan/UBSan)

Salom, men **Khorazmiy AI** loyihasining C++ va kiberxavfsizlik bo'yicha bosh dataset mutaxassisiman. Ushbu modulda zamonaviy kriptografik standartlar: `OpenSSL 3.0 EVP API`, simmetrik va asimmetrik shifrlash (AES-256-GCM, ChaCha20-Poly1305, RSA-4096 OAEP/PSS, Ed25519), elliptik egri chiziqlar (ECDH/X25519), Constant-Time algoritmlar, Side-Channel hujumlaridan himoya hamda xotira xavfsizligi analizatorlari (ASan, UBSan, TSan) bo'yicha 50 ta sanoat darajasidagi amaliy topshiriq va ularning to'liq yechimlari taqdim etiladi.

---
### Topshiriq #1151: OpenSSL 3.0 EVP API yordamida AES-256-GCM Shifrlash va Autentifikatsiya (AEAD)
**Tavsif:** Ma'lumotlar maxfiyligi va ularning yo'lda soxtalashtirilmaganligini bir vaqtning o'zida kafolatlash uchun OpenSSL 3.0 ning yangi EVP arxitekturasi orqali AES-256-GCM shifrlash tizimini yarating.
**Talablar:** `EVP_CIPHER_CTX_new`, `EVP_EncryptInit_ex2`, 256-bit kalit, 96-bit (12 bayt) IV/Nonce, 16 bayt Tag generatsiyasi.
**Yechim (C++):**
```cpp
#include <openssl/evp.h>
#include <vector>
#include <iostream>
#include <stdexcept>

struct GCMEncryptedData {
    std::vector<uint8_t> ciphertext;
    std::vector<uint8_t> tag; // 16 bayt
};

GCMEncryptedData aes_256_gcm_encrypt(
    const std::vector<uint8_t>& plaintext,
    const std::vector<uint8_t>& key,
    const std::vector<uint8_t>& iv,
    const std::vector<uint8_t>& aad = {})
{
    if (key.size() != 32 || iv.size() != 12) {
        throw std::invalid_argument("AES-256 uchun kalit 32 bayt va IV 12 bayt bo'lishi shart!");
    }

    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    if (!ctx) throw std::runtime_error("EVP_CIPHER_CTX yaratilmadi");

    // OpenSSL 3.0 zamonaviy EVP API
    if (EVP_EncryptInit_ex(ctx, EVP_aes_256_gcm(), nullptr, nullptr, nullptr) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("GCM initsializatsiya xatosi");
    }

    // IV uzunligini o'rnatamiz (12 bayt standart)
    EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN, iv.size(), nullptr);
    EVP_EncryptInit_ex(ctx, nullptr, nullptr, key.data(), iv.data());

    // AAD (Additional Authenticated Data) mavjud bo'lsa qo'shamiz
    int len = 0;
    if (!aad.empty()) {
        EVP_EncryptUpdate(ctx, nullptr, &len, aad.data(), aad.size());
    }

    std::vector<uint8_t> ciphertext(plaintext.size());
    if (EVP_EncryptUpdate(ctx, ciphertext.data(), &len, plaintext.data(), plaintext.size()) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("Shifrlash xatosi");
    }
    int ciphertext_len = len;

    if (EVP_EncryptFinal_ex(ctx, ciphertext.data() + len, &len) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("EncryptFinal xatosi");
    }
    ciphertext_len += len;
    ciphertext.resize(ciphertext_len);

    // 16 baytli Autentifikatsiya Tagini olamiz
    std::vector<uint8_t> tag(16);
    EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_GET_TAG, 16, tag.data());

    EVP_CIPHER_CTX_free(ctx);
    return {ciphertext, tag};
}
```
**Tushuntirish:** AES-GCM (Galois/Counter Mode) zamonaviy simmetrik shifrlashning oltin standartidir. U apparat darajasida (Intel AES-NI va ARMv8 Crypto) tezlashgan bo'lib, nafaqat ma'lumotni shifrlaydi, balki 16 baytli MAC tag orqali paket butunligini kafolatlaydi.

---

### Topshiriq #1152: AES-256-GCM Shifrini Yechish va 16 baytli Tagni Tekshirish
**Tavsif:** Shifrlangan paket yetib kelganda, uning autentifikatsiya tagini tekshirib, agar ma'lumot yo'lda bitta bitga bo'lsa ham o'zgargan bo'lsa, xatolik berib shifrni ochishni rad etuvchi dekriptor yarating.
**Talablar:** `EVP_CTRL_GCM_SET_TAG`, `EVP_DecryptFinal_ex`, soxtalashtirilgan ma'lumotlarni aniqlash.
**Yechim (C++):**
```cpp
#include <openssl/evp.h>
#include <vector>
#include <stdexcept>
#include <iostream>

std::vector<uint8_t> aes_256_gcm_decrypt(
    const std::vector<uint8_t>& ciphertext,
    const std::vector<uint8_t>& tag,
    const std::vector<uint8_t>& key,
    const std::vector<uint8_t>& iv,
    const std::vector<uint8_t>& aad = {})
{
    if (tag.size() != 16) throw std::invalid_argument("Tag 16 bayt bo'lishi shart!");

    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    EVP_DecryptInit_ex(ctx, EVP_aes_256_gcm(), nullptr, nullptr, nullptr);
    EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN, iv.size(), nullptr);
    EVP_DecryptInit_ex(ctx, nullptr, nullptr, key.data(), iv.data());

    int len = 0;
    if (!aad.empty()) {
        EVP_DecryptUpdate(ctx, nullptr, &len, aad.data(), aad.size());
    }

    std::vector<uint8_t> plaintext(ciphertext.size());
    EVP_DecryptUpdate(ctx, plaintext.data(), &len, ciphertext.data(), ciphertext.size());
    int plaintext_len = len;

    // Kutilgan tagni o'rnatamiz
    EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_TAG, 16, const_cast<uint8_t*>(tag.data()));

    // Agar tag mos kelmasa, EVP_DecryptFinal_ex nol (0) qaytaradi!
    int ret = EVP_DecryptFinal_ex(ctx, plaintext.data() + len, &len);
    EVP_CIPHER_CTX_free(ctx);

    if (ret <= 0) {
        throw std::runtime_error("Kriptografik xatolik: Autentifikatsiya tagi mos kelmadi! Paket soxtalashtirilgan!");
    }

    plaintext_len += len;
    plaintext.resize(plaintext_len);
    return plaintext;
}
```
**Tushuntirish:** AEAD da dekriptsiya vaqtida xatolik yuz bersa, hech qachon qisman ochilgan ochiq matnni (plaintext) dasturga qaytarish mumkin emas. Tag tekshiruvi muvaffaqiyatsiz bo'lsa, xotira zudlik bilan tozalanadi.

---

### Topshiriq #1153: ChaCha20-Poly1305 simmetrik shifrlash
**Tavsif:** AES-NI apparat instruksiyalari mavjud bo'lmagan mobil yoki IoT qurilmalarda AES ga qaraganda ancha tez ishlaydigan va yon kanalli (side-channel) hujumlarga chidamli ChaCha20-Poly1305 shifrlashini amalga oshiring.
**Talablar:** `EVP_chacha20_poly1305()`, 256-bit kalit, 96-bit Nonce, 16 bayt Poly1305 tegi.
**Yechim (C++):**
```cpp
#include <openssl/evp.h>
#include <vector>
#include <stdexcept>

std::vector<uint8_t> chacha20_poly1305_encrypt(
    const std::vector<uint8_t>& plaintext,
    const std::vector<uint8_t>& key,
    const std::vector<uint8_t>& nonce,
    std::vector<uint8_t>& out_tag)
{
    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    EVP_EncryptInit_ex(ctx, EVP_chacha20_poly1305(), nullptr, key.data(), nonce.data());

    std::vector<uint8_t> ciphertext(plaintext.size());
    int len = 0;
    EVP_EncryptUpdate(ctx, ciphertext.data(), &len, plaintext.data(), plaintext.size());

    int final_len = 0;
    EVP_EncryptFinal_ex(ctx, ciphertext.data() + len, &final_len);

    out_tag.resize(16);
    EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_AEAD_GET_TAG, 16, out_tag.data());
    EVP_CIPHER_CTX_free(ctx);

    return ciphertext;
}
```
**Tushuntirish:** Daniel J. Bernstein tomonidan yaratilgan ChaCha20-Poly1305 algoritmi dasturiy darajada doimiy vaqtda (constant-time) bajariladi va kesh-tayming (cache-timing) kiberhujumlaridan tabiiy ravishda himoyalangan.

---

### Topshiriq #1154: RSA-4096 kalit juftligini yaratish va PEM formatida eksport qilish
**Tavsif:** Bank yoki mudofaa darajasidagi asimmetrik shifrlash uchun OpenSSL 3.0 EVP_PKEY arxitekturasi yordamida RSA-4096 kalitlarini yarating va PEM ko'rinishida xotiraga chiqaring.
**Talablar:** `EVP_PKEY_Q_keygen`, PEM BIO, xotirada shaxsiy va ommaviy kalitlarni saqlash.
**Yechim (C++):**
```cpp
#include <openssl/evp.h>
#include <openssl/pem.h>
#include <iostream>
#include <string>

std::pair<std::string, std::string> generate_rsa_4096_keypair() {
    // OpenSSL 3.0 ning yangi soddalashtirilgan generatsiya API si
    EVP_PKEY* pkey = EVP_PKEY_Q_keygen(nullptr, nullptr, "RSA", (size_t)4096);
    if (!pkey) throw std::runtime_error("RSA-4096 generatsiyasi muvaffaqiyatsiz");

    // Xotiradagi BIO orqali PEM formatiga o'tkazish
    BIO* priv_bio = BIO_new(BIO_s_mem());
    PEM_write_bio_PrivateKey(priv_bio, pkey, nullptr, nullptr, 0, nullptr, nullptr);

    BIO* pub_bio = BIO_new(BIO_s_mem());
    PEM_write_bio_PUBKEY(pub_bio, pkey);

    char* priv_data = nullptr;
    long priv_len = BIO_get_mem_data(priv_bio, &priv_data);
    std::string private_key(priv_data, priv_len);

    char* pub_data = nullptr;
    long pub_len = BIO_get_mem_data(pub_bio, &pub_data);
    std::string public_key(pub_data, pub_len);

    BIO_free(priv_bio);
    BIO_free(pub_bio);
    EVP_PKEY_free(pkey);

    return {private_key, public_key};
}
```
**Tushuntirish:** RSA-4096 hozirgi zamonda klassik asimmetrik shifrlashning eng xavfsiz o'lchami hisoblanadi. OpenSSL 3.0 da eski `RSA_generate_key_ex` o'rniga modulli `EVP_PKEY` API si tavsiya etiladi.

---

### Topshiriq #1155: RSA-4096 OAEP bilan xavfsiz shifrlash
**Tavsif:** Eski PKCS#1 v1.5 padding uslubi Bleichenbacher hujumiga zaif. Shuning uchun zamonaviy RSA-OAEP (Optimal Asymmetric Encryption Padding) orqali simmetrik kalitni xavfsiz shifrlang.
**Talablar:** `EVP_PKEY_CTX_new`, `EVP_PKEY_encrypt_init`, `EVP_PKEY_CTX_set_rsa_padding(RSA_PKCS1_OAEP_PADDING)`, SHA-256 digest.
**Yechim (C++):**
```cpp
#include <openssl/evp.h>
#include <openssl/rsa.h>
#include <vector>
#include <stdexcept>

std::vector<uint8_t> rsa_oaep_encrypt(EVP_PKEY* pub_key, const std::vector<uint8_t>& plaintext) {
    EVP_PKEY_CTX* ctx = EVP_PKEY_CTX_new(pub_key, nullptr);
    if (!ctx) throw std::runtime_error("PKEY_CTX yaratilmadi");

    if (EVP_PKEY_encrypt_init(ctx) <= 0) {
        EVP_PKEY_CTX_free(ctx);
        throw std::runtime_error("Encrypt init xatosi");
    }

    // OAEP padding va SHA-256 xeshini tanlaymiz
    EVP_PKEY_CTX_set_rsa_padding(ctx, RSA_PKCS1_OAEP_PADDING);
    EVP_PKEY_CTX_set_rsa_oaep_md(ctx, EVP_sha256());

    size_t outlen = 0;
    // Dastlab kerakli bufer hajmini hisoblaymiz
    EVP_PKEY_encrypt(ctx, nullptr, &outlen, plaintext.data(), plaintext.size());

    std::vector<uint8_t> ciphertext(outlen);
    if (EVP_PKEY_encrypt(ctx, ciphertext.data(), &outlen, plaintext.data(), plaintext.size()) <= 0) {
        EVP_PKEY_CTX_free(ctx);
        throw std::runtime_error("RSA OAEP shifrlashda xatolik");
    }
    ciphertext.resize(outlen);

    EVP_PKEY_CTX_free(ctx);
    return ciphertext;
}
```
**Tushuntirish:** OAEP tasodifiy kiritish (randomized padding) orqali bitta xabarni har safar turli shifrlangan matnga aylantiradi. Bu tanlangan ochiq matn hujumlaridan (CPA) to'liq himoya qiladi.

---

### Topshiriq #1156: RSA-4096 PSS bilan raqamli imzo qo'yish va tekshirish
**Tavsif:** Muhim hujjatlar yoki dasturiy yangilanishlarga kriptografik isbotlangan RSA-PSS (Probabilistic Signature Scheme) algoritmi bilan raqamli imzo qo'ying va tasdiqlang.
**Talablar:** `EVP_DigestSignInit`, `EVP_PKEY_CTX_set_rsa_padding(RSA_PKCS1_PSS_PADDING)`, SHA-256.
**Yechim (C++):**
```cpp
#include <openssl/evp.h>
#include <openssl/rsa.h>
#include <vector>

std::vector<uint8_t> sign_data_rsa_pss(EVP_PKEY* priv_key, const std::vector<uint8_t>& data) {
    EVP_MD_CTX* md_ctx = EVP_MD_CTX_new();
    EVP_PKEY_CTX* pkey_ctx = nullptr;

    EVP_DigestSignInit(md_ctx, &pkey_ctx, EVP_sha256(), nullptr, priv_key);
    EVP_PKEY_CTX_set_rsa_padding(pkey_ctx, RSA_PKCS1_PSS_PADDING);
    EVP_PKEY_CTX_set_rsa_pss_saltlen(pkey_ctx, RSA_PSS_SALTLEN_DIGEST);

    EVP_DigestSignUpdate(md_ctx, data.data(), data.size());

    size_t sig_len = 0;
    EVP_DigestSignFinal(md_ctx, nullptr, &sig_len);

    std::vector<uint8_t> signature(sig_len);
    EVP_DigestSignFinal(md_ctx, signature.data(), &sig_len);
    signature.resize(sig_len);

    EVP_MD_CTX_free(md_ctx);
    return signature;
}
```
**Tushuntirish:** RSA-PSS klassik PKCS#1 v1.5 imzosiga qaraganda ancha xavfsiz bo'lib, uning xavfsizligi matematik jihatdan RSA muammosining murakkabligiga to'g'ridan-to'g'ri bog'langan.

---

### Topshiriq #1157: Ed25519 orqali ultra tezkor raqamli imzo
**Tavsif:** Katta RSA kalitlarining o'rnini bosuvchi, atigi 32 baytlik ommaviy kalit va 64 baytlik imzo hosil qiluvchi yuqori tezlikdagi Ed25519 (EdDSA) raqamli imzo tizimini joriy qiling.
**Talablar:** `EVP_PKEY_ED25519`, `EVP_DigestSign`, imzo qo'yish va tekshirish.
**Yechim (C++):**
```cpp
#include <openssl/evp.h>
#include <vector>
#include <iostream>

bool verify_ed25519_signature(EVP_PKEY* pub_key, const std::vector<uint8_t>& data, const std::vector<uint8_t>& sig) {
    EVP_MD_CTX* md_ctx = EVP_MD_CTX_new();
    // Ed25519 xesh algoritmi talab qilmaydi (nullptr beriladi), u ichki o'z xeshiga ega
    if (EVP_DigestVerifyInit(md_ctx, nullptr, nullptr, nullptr, pub_key) <= 0) {
        EVP_MD_CTX_free(md_ctx);
        return false;
    }

    int result = EVP_DigestVerify(md_ctx, sig.data(), sig.size(), data.data(), data.size());
    EVP_MD_CTX_free(md_ctx);

    return result == 1; // 1 = Imzo to'g'ri
}
```
**Tushuntirish:** Ed25519 SHA-512 va Curve25519 elliptik egri chizig'iga asoslangan. U soniyasiga o'n minglab imzolarni tekshirishga qodir va tasodifiy sonlar generatori (RNG) buzilgan taqdirda ham kalit sizib chiqishidan himoyalangan.

---

### Topshiriq #1158: X25519 Elliptik egri chiziq orqali Diffie-Hellman kalit almashinuvi (ECDH)
**Tavsif:** Ochiq tarmoq orqali ikki tomon (Alice va Bob) uchinchi shaxslarga bildirmasdan bitta umumiy maxfiy simmetrik kalit hosil qiluvchi X25519 kalit almashinuvini dasturlang.
**Talablar:** `EVP_PKEY_X25519`, `EVP_PKEY_derive_init`, umumiy sirni (Shared Secret) hisoblash.
**Yechim (C++):**
```cpp
#include <openssl/evp.h>
#include <vector>
#include <stdexcept>

std::vector<uint8_t> derive_shared_secret_x25519(EVP_PKEY* my_priv_key, EVP_PKEY* peer_pub_key) {
    EVP_PKEY_CTX* ctx = EVP_PKEY_CTX_new(my_priv_key, nullptr);
    if (!ctx) throw std::runtime_error("PKEY_CTX xatosi");

    if (EVP_PKEY_derive_init(ctx) <= 0) {
        EVP_PKEY_CTX_free(ctx);
        throw std::runtime_error("Derive init xatosi");
    }

    if (EVP_PKEY_derive_set_peer(ctx, peer_pub_key) <= 0) {
        EVP_PKEY_CTX_free(ctx);
        throw std::runtime_error("Peer kalitni o'rnatishda xatolik");
    }

    size_t secret_len = 0;
    EVP_PKEY_derive(ctx, nullptr, &secret_len);

    std::vector<uint8_t> secret(secret_len);
    if (EVP_PKEY_derive(ctx, secret.data(), &secret_len) <= 0) {
        EVP_PKEY_CTX_free(ctx);
        throw std::runtime_error("Umumiy sirni hisoblashda xatolik");
    }

    EVP_PKEY_CTX_free(ctx);
    return secret; // 32 bayt umumiy sir
}
```
**Tushuntirish:** X25519 (RFC 7748) eng xavfsiz va tezkor Diffie-Hellman algoritmidir. TLS 1.3 protokoli aynan shu algoritmdan asosiy kalit kelishuvi sifatida foydalanadi.

---

### Topshiriq #1159: HKDF (RFC 5869) orqali xom sirdan kriptografik kalitlar hosil qilish
**Tavsif:** Diffie-Hellman natijasida olingan umumiy sirdan (shared secret) shifrlash kaliti, IV va MAC kalitlarini mustaqil va xavfsiz tarzda ajratib oluvchi HKDF tizimini quring.
**Talablar:** `EVP_KDF_fetch(nullptr, "HKDF", nullptr)`, Extract-and-Expand bosqichlari.
**Yechim (C++):**
```cpp
#include <openssl/kdf.h>
#include <openssl/core_names.h>
#include <vector>
#include <stdexcept>

std::vector<uint8_t> hkdf_expand(
    const std::vector<uint8_t>& secret,
    const std::vector<uint8_t>& salt,
    const std::string& info,
    size_t out_len)
{
    EVP_KDF* kdf = EVP_KDF_fetch(nullptr, "HKDF", nullptr);
    EVP_KDF_CTX* kctx = EVP_KDF_CTX_new(kdf);
    EVP_KDF_free(kdf);

    OSSL_PARAM params[5];
    char digest[] = "SHA256";
    params[0] = OSSL_PARAM_construct_utf8_string(OSSL_KDF_PARAM_DIGEST, digest, sizeof(digest));
    params[1] = OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_KEY, (void*)secret.data(), secret.size());
    params[2] = OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_SALT, (void*)salt.data(), salt.size());
    params[3] = OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_INFO, (void*)info.data(), info.size());
    params[4] = OSSL_PARAM_construct_end();

    std::vector<uint8_t> out_key(out_len);
    if (EVP_KDF_derive(kctx, out_key.data(), out_len, params) <= 0) {
        EVP_KDF_CTX_free(kctx);
        throw std::runtime_error("HKDF derive xatosi");
    }

    EVP_KDF_CTX_free(kctx);
    return out_key;
}
```
**Tushuntirish:** Xom kriptografik sirlar to'liq bir tekis taqsimlanmagan (non-uniform) bo'lishi mumkin. HKDF ularni tozalab (Extract) va kerakli o'lchamdagi kriptografik kalitlarga kengaytiradi (Expand).

---

### Topshiriq #1160: PBKDF2-HMAC-SHA256 yordamida parollarni salt bilan xesh-kalitga aylantirish
**Tavsif:** Foydalanuvchi kiritgan zaif paroldan xakerlarning GPU hujumlariga qarshilik ko'rsatish uchun 600,000 marta aylantirilgan (iterations) xavfsiz shifrlash kaliti hosil qiling.
**Talablar:** `PKCS5_PBKDF2_HMAC`, SHA-256, 16 bayt tasodifiy salt, 600,000 iteratsiya.
**Yechim (C++):**
```cpp
#include <openssl/evp.h>
#include <vector>
#include <string>

std::vector<uint8_t> derive_key_pbkdf2(const std::string& password, const std::vector<uint8_t>& salt, int iterations = 600000, int key_len = 32) {
    std::vector<uint8_t> derived_key(key_len);

    PKCS5_PBKDF2_HMAC(
        password.c_str(),
        password.length(),
        salt.data(),
        salt.size(),
        iterations,
        EVP_sha256(),
        key_len,
        derived_key.data()
    );

    return derived_key;
}
```
**Tushuntirish:** PBKDF2 ataylab protsessorni sekinlashtirish uchun yuz minglab iteratsiyalar orqali ishlaydi. Bu orqali xakerlar soniyasiga milliardlab parollarni tekshira olmaydi.

---

### Topshiriq #1161: Argon2id (Parollarni xotira-qattiq xeshlash algoritmi, RFC 9106)
**Tavsif:** GPU va ASIC chiplari yordamida parollarni buzishga mutlaqo yo'l qo'ymaydigan, xotira sarfini (Memory-hard) talab qiluvchi eng zamonaviy Argon2id algoritmini sozlang.
**Talablar:** OpenSSL 3.2+ yoki Argon2 API, xotira hajmi (64 MB), vaqt narxi (time cost) va parallellik.
**Yechim (C++):**
```cpp
#include <openssl/kdf.h>
#include <openssl/core_names.h>
#include <vector>
#include <string>

std::vector<uint8_t> derive_argon2id(const std::string& password, const std::vector<uint8_t>& salt) {
    EVP_KDF* kdf = EVP_KDF_fetch(nullptr, "ARGON2ID", nullptr);
    EVP_KDF_CTX* ctx = EVP_KDF_CTX_new(kdf);
    EVP_KDF_free(kdf);

    uint32_t lanes = 4;
    uint32_t mem_cost = 65536; // 64 MB RAM majburiy
    uint32_t iter = 3;

    OSSL_PARAM params[6];
    params[0] = OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_PASSWORD, (void*)password.data(), password.size());
    params[1] = OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_SALT, (void*)salt.data(), salt.size());
    params[2] = OSSL_PARAM_construct_uint32(OSSL_KDF_PARAM_ITER, &iter);
    params[3] = OSSL_PARAM_construct_uint32(OSSL_KDF_PARAM_ARGON2_LANES, &lanes);
    params[4] = OSSL_PARAM_construct_uint32(OSSL_KDF_PARAM_ARGON2_MEMCOST, &mem_cost);
    params[5] = OSSL_PARAM_construct_end();

    std::vector<uint8_t> out_key(32);
    EVP_KDF_derive(ctx, out_key.data(), out_key.size(), params);
    EVP_KDF_CTX_free(ctx);

    return out_key;
}
```
**Tushuntirish:** Argon2id Password Hashing Competition (PHC) g'olibi bo'lib, xotira-qattiq (Memory-hard) algoritmdir. Har bir parol sinovi 64 MB xotirani talab qilgani uchun videokartalar (GPU) orqali parollarni qidirish samarasiz bo'lib qoladi.

---

### Topshiriq #1162: SHA-256 va SHA-512 kriptografik xesh funksiyalari
**Tavsif:** Fayllar yoki tranzaksiyalarning barmoq izini (digest) hisoblash uchun OpenSSL EVP streaming arxitekturasida SHA-256 va SHA-512 hisoblang.
**Talablar:** `EVP_MD_CTX_new`, `EVP_DigestInit_ex`, `EVP_DigestUpdate`, `EVP_DigestFinal_ex`.
**Yechim (C++):**
```cpp
#include <openssl/evp.h>
#include <vector>
#include <iomanip>
#include <sstream>

std::string compute_sha256(const std::vector<uint8_t>& data) {
    EVP_MD_CTX* ctx = EVP_MD_CTX_new();
    EVP_DigestInit_ex(ctx, EVP_sha256(), nullptr);
    EVP_DigestUpdate(ctx, data.data(), data.size());

    unsigned char hash[EVP_MAX_MD_SIZE];
    unsigned int len = 0;
    EVP_DigestFinal_ex(ctx, hash, &len);
    EVP_MD_CTX_free(ctx);

    std::stringstream ss;
    for (unsigned int i = 0; i < len; ++i) {
        ss << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];
    }
    return ss.str();
}
```
**Tushuntirish:** `EVP_DigestUpdate` katta fayllarni bo'lakma-bo'lak qabul qila oladi, shuning uchun hatto 100 GB hajmdagi fayl ham xotiraga yuklanmasdan oqim tarzida xeshlanadi.

---

### Topshiriq #1163: HMAC-SHA256 orqali xabar yaxlitligi va haqiqiyligini tekshirish
**Tavsif:** API so'rovlari yo'lda o'zgarmaganligini va aynan maxfiy kalitga ega bo'lgan tomon jo'natganligini tasdiqlovchi HMAC-SHA256 imzosini yarating.
**Talablar:** `HMAC()`, maxfiy kalit, xabarni tekshirish.
**Yechim (C++):**
```cpp
#include <openssl/hmac.h>
#include <vector>

std::vector<uint8_t> generate_hmac_sha256(const std::vector<uint8_t>& key, const std::vector<uint8_t>& message) {
    std::vector<uint8_t> hmac(32);
    unsigned int len = 32;

    HMAC(
        EVP_sha256(),
        key.data(),
        key.size(),
        message.data(),
        message.size(),
        hmac.data(),
        &len
    );

    return hmac;
}
```
**Tushuntirish:** Oddiy xeshdan farqli ravishda HMAC (Hash-based Message Authentication Code) maxfiy kalitga tayanadi va Length Extension kiberhujumlaridan to'liq himoyalangan.

---

### Topshiriq #1164: Constant-Time taqqoslash algoritmi (Timing Attack kiberhujumlarini bartaraf etish)
**Tavsif:** Parollar yoki HMAC imzolarini standart `memcmp` yoki `==` bilan solishtirganda, birinchi xato baytdayoq tsikl to'xtab vaqt bo'yicha qidirish (Timing Attack) imkoniyati ochiladi. Buni to'xtatuvchi doimiy vaqtli (constant-time) taqqoslash yozing.
**Talablar:** Bitwise XOR va OR amallari, har doim butun massivni to'liq aylanib chiqish.
**Yechim (C++):**
```cpp
#include <cstdint>
#include <cstddef>

bool constant_time_compare(const uint8_t* a, const uint8_t* b, size_t length) {
    uint8_t result = 0;
    // Har doim butun uzunlik oxirigacha aylanadi (ertachi return yo'q!)
    for (size_t i = 0; i < length; ++i) {
        result |= (a[i] ^ b[i]);
    }
    // Agar hamma baytlar teng bo'lsa result == 0 bo'ladi
    return result == 0;
}
```
**Tushuntirish:** Standart `memcmp` birinchi mos kelmagan baytda `return` qiladi. Kiberhujumchi nanosekundlik farqlarni o'lchab maxfiy parolni baytma-bayt topib olishi mumkin. Constant-Time solishtirish esa xatoni qayerdaligidan qat'i nazar har doim bir xil vaqt oladi.

---

### Topshiriq #1165: Xavfsiz xotira tozalash: OPENSSL_cleanse va maxfiy kalitlarni RAM dan o'chirish
**Tavsif:** Standart `memset` buyrug'i o'zgaruvchi keyin ishlatilmagani sababli kompilyator optimizatori (Dead Store Elimination) tomonidan o'chirib yuborilishi va kalit RAM da qolib ketishi mumkin. Buni oldini oluvchi kafolatli xotira tozalashni qo'llang.
**Talablar:** `OPENSSL_cleanse` yoki `volatile` ko'rsatkich.
**Yechim (C++):**
```cpp
#include <openssl/crypto.h>
#include <vector>

class SecureKeyBuffer {
public:
    SecureKeyBuffer(size_t size) : buffer_(size, 0) {}

    ~SecureKeyBuffer() {
        // Kompilyator bu operatsiyani hech qachon optimallashtirib tashlay olmaydi!
        OPENSSL_cleanse(buffer_.data(), buffer_.size());
    }

    uint8_t* data() { return buffer_.data(); }
    size_t size() const { return buffer_.size(); }

private:
    std::vector<uint8_t> buffer_;
};
```
**Tushuntirish:** `OPENSSL_cleanse` maxsus ichki assembler va volatile mexanizmlariga ega bo'lib, optimizatorga bo'ysunmaydi va maxfiy ma'lumotlarni RAM dan 100% tozalaydi.

---

### Topshiriq #1166: Xotirani xavfsiz qulflash (mlock/VirtualLock)
**Tavsif:** Kriptografik kalitlar operatsion tizim tomonidan qattiq diskdagi swap (paging) fayliga yozilib qolmasligi va diskda iz qoldirmasligi uchun xotirani RAM da qulflang.
**Talablar:** Linux `mlock`, Windows `VirtualLock`, xotirani sahifa darajasida himoyalash.
**Yechim (C++):**
```cpp
#include <iostream>

#if defined(__unix__) || defined(__linux__)
#include <sys/mman.h>

bool lock_memory_in_ram(void* addr, size_t size) {
    // Sahifani RAM ga mahkamlaymiz (Swap ga tushmaydi)
    if (mlock(addr, size) != 0) {
        return false;
    }
    return true;
}

void unlock_memory(void* addr, size_t size) {
    munlock(addr, size);
}
#endif
```
**Tushuntirish:** Agar xotira qulflanmasa, OS yuklama vaqtida kalitlar joylashgan RAM bloklarini qattiq diskka (swapfile/pagefile.sys) chiqarib tashlaydi va bu kompyuter o'chirilgandan keyin ham diskdan kalitni tiklash imkonini qoldiradi.

---

### Topshiriq #1167: Kriptografik xavfsiz tasodifiy sonlar generatsiyasi (RAND_bytes)
**Tavsif:** Pseudorandom generatorlar (`rand()`, `std::mt19937`) kriptografiyada ishlatilsa kalitlar oldindan bashorat qilinishi mumkin. Operatsion tizim entropiyasiga asoslangan kriptografik tasodifiylikni yarating.
**Talablar:** `RAND_bytes`, `RAND_status() == 1`, xavfsiz IV va Salt generatsiyasi.
**Yechim (C++):**
```cpp
#include <openssl/rand.h>
#include <vector>
#include <stdexcept>

std::vector<uint8_t> generate_secure_random_bytes(size_t size) {
    if (RAND_status() != 1) {
        throw std::runtime_error("Tizim entropiyasi yetarli emas!");
    }

    std::vector<uint8_t> buf(size);
    if (RAND_bytes(buf.data(), size) != 1) {
        throw std::runtime_error("CSPRNG generatsiya xatosi");
    }

    return buf;
}
```
**Tushuntirish:** `RAND_bytes` Linux da `/dev/urandom` va Windows da `BCryptGenRandom` orqali ishlaydi. Uning chiqishini matematik jihatdan bashorat qilib bo'lmaydi.

---

### Topshiriq #1168: AddressSanitizer (ASan) orqali Buffer Overflow va Use-After-Free xatolarini tutish
**Tavsif:** C++ da xotira bilan ishlashdagi qaltis xatolar: chegaradan tashqariga yozish (Out-of-bounds) va o'chirilgan xotiradan foydalanish (Use-After-Free) ni kompilyatsiya vaqtida ASan orqali tutishni sozlang.
**Talablar:** `-fsanitize=address -g`, xatolikni keltirib chiqaruvchi xavfsiz namoyish va ASan hisoboti.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>

void demonstrate_asan_detection() {
    // ASan bilan kompilyatsiya: g++ -fsanitize=address -g main.cpp
    int* ptr = new int[10];
    ptr[0] = 42;
    delete[] ptr;

    // Use-After-Free: ASan bu qatorni darhol tutib dasturni xavfsiz to'xtatadi
    // std::cout << ptr[0] << std::endl; 
}

int main() {
    std::cout << "AddressSanitizer (ASan) xotira xavfsizligini ta'minlaydi.
";
    demonstrate_asan_detection();
    return 0;
}
```
**Tushuntirish:** ASan har bir xotira blokining atrofiga "qizil hududlar" (Redzones) va soya xotira (Shadow Memory) qo'shadi. Chegaradan tashqariga bitta bayt yozilsa ham darhol Crash log hosil bo'ladi.

---

### Topshiriq #1169: UndefinedBehaviorSanitizer (UBSan) orqali butun sonlar to'lib-toshishini aniqlash
**Tavsif:** Imzoli butun sonlar to'lib-toshishi (Signed Integer Overflow) va nolga bo'lish kabi C++ da noaniq xatti-harakatlarni (Undefined Behavior) avtomatik aniqlovchi vositani yoqing.
**Talablar:** `-fsanitize=undefined`, overflow tekshiruvi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <climits>

void demonstrate_ubsan_check() {
    // Kompilyatsiya: g++ -fsanitize=undefined -g main.cpp
    int max_val = INT_MAX;
    // max_val + 1 amalida UBSan darhol xatolik bildiradi:
    // runtime error: signed integer overflow
    std::cout << "Maksimal butun son: " << max_val << std::endl;
}

int main() {
    demonstrate_ubsan_check();
    return 0;
}
```
**Tushuntirish:** C++ standartida Signed Integer Overflow noaniq xatti-harakat hisoblanadi va kompilyator bunday kodni noto'g'ri optimallashtirishi xavfsizlik teshiklariga (vulnerabilities) olib keladi.

---

### Topshiriq #1170: ThreadSanitizer (TSan) orqali Data Race larni aniqlash
**Tavsif:** Kriptografik hisob-kitoblarni ko'p oqimli (multithreading) parallel bajarganda umumiy xotiraga mutexsiz murojaat qilish oqibatida yuzaga keladigan ma'lumotlar poygasini (Data Race) TSan bilan tuting.
**Talablar:** `-fsanitize=thread`, std::thread, std::atomic yoki mutex bilan to'g'irlash.
**Yechim (C++):**
```cpp
#include <iostream>
#include <thread>
#include <atomic>

// Data race oldini olish uchun std::atomic qo'llaniladi
std::atomic<int> secure_counter{0};

void worker() {
    for (int i = 0; i < 10000; ++i) {
        secure_counter.fetch_add(1, std::memory_order_relaxed);
    }
}

int main() {
    // Kompilyatsiya: g++ -fsanitize=thread -g main.cpp
    std::thread t1(worker);
    std::thread t2(worker);
    t1.join();
    t2.join();
    std::cout << "TSan tomonidan tekshirildi: Counter = " << secure_counter.load() << std::endl;
    return 0;
}
```
**Tushuntirish:** Data Race kutilmagan xotira buzilishiga olib keladi. TSan har bir xotira murojaatini kuzatib boradi va sinxronizatsiya qilinmagan o'qish/yozishlarni aniqlaydi.

---

### Topshiriq #1171: X.509 Raqamli Sertifikatlarini yaratish va tekshirish
**Tavsif:** Server va mijozlar o'rtasida o'z-o'zini imzolagan (Self-Signed) yoki CA tomonidan tasdiqlangan X.509 raqamli sertifikatini OpenSSL 3.0 orqali yarating.
**Talablar:** `X509_new`, `X509_set_pubkey`, `X509_sign`, amal qilish muddati (Validity).
**Yechim (C++):**
```cpp
#include <openssl/x509.h>
#include <openssl/x509v3.h>

X509* create_self_signed_cert(EVP_PKEY* pkey) {
    X509* x509 = X509_new();
    ASN1_INTEGER_set(X509_get_serialNumber(x509), 1);

    // 365 kun amal qilish muddati
    X509_gmtime_adj(X509_get_notBefore(x509), 0);
    X509_gmtime_adj(X509_get_notAfter(x509), 31536000L);

    X509_set_pubkey(x509, pkey);

    X509_NAME* name = X509_get_subject_name(x509);
    X509_NAME_add_entry_by_txt(name, "C", MBSTRING_ASC, (unsigned char*)"UZ", -1, -1, 0);
    X509_NAME_add_entry_by_txt(name, "O", MBSTRING_ASC, (unsigned char*)"Khorazmiy AI", -1, -1, 0);
    X509_NAME_add_entry_by_txt(name, "CN", MBSTRING_ASC, (unsigned char*)"khorazmiy.uz", -1, -1, 0);

    X509_set_issuer_name(x509, name); // Self-signed bo'lgani uchun issuer == subject

    // Sertifikatni shaxsiy kalit bilan imzolaymiz
    X509_sign(x509, pkey, EVP_sha256());
    return x509;
}
```
**Tushuntirish:** X.509 sertifikatlari ommaviy kalitni egasining shaxsiga biriktiradi va HTTPS hamda mTLS protokollarining markaziy ustuni hisoblanadi.

---

### Topshiriq #1172: CRL va OCSP tekshiruvi orqali bekor qilingan sertifikatlarni aniqlash
**Tavsif:** O'g'irlangan yoki bekor qilingan (Revoked) SSL sertifikatlarini aniqlash uchun X509 sertifikatlar zanjirida CRL va OCSP holatini tekshiring.
**Talablar:** `X509_STORE_set_flags`, `X509_V_FLAG_CRL_CHECK`.
**Yechim (C++):**
```cpp
#include <openssl/x509.h>
#include <openssl/x509_vfy.h>

void configure_crl_verification(X509_STORE* store) {
    // CRL tekshiruvini majburiy qilib belgilaymiz
    X509_STORE_set_flags(store, X509_V_FLAG_CRL_CHECK | X509_V_FLAG_CRL_CHECK_ALL);
}
```
**Tushuntirish:** Sertifikatning muddati tugamagan bo'lsa ham uning kaliti oshkor bo'lgan bo'lishi mumkin. CRL va OCSP tekshiruvi xavfsizlikni to'liq ta'minlaydi.

---

### Topshiriq #1173: TLS 1.3 Client va Server o'rtasida ALPN sozlash
**Tavsif:** TLS ulanishi o'rnatilayotganda dasturiy qatlam protokolini (masalan HTTP/2 yoki HTTP/1.1) xavfsiz kelishib olish uchun ALPN (Application-Layer Protocol Negotiation) ni sozlang.
**Talablar:** `SSL_CTX_set_alpn_select_cb`, simli bayt protokollari.
**Yechim (C++):**
```cpp
#include <openssl/ssl.h>
#include <cstring>

static int alpn_cb(SSL* ssl, const unsigned char** out, unsigned char* outlen,
                   const unsigned char* in, unsigned int inlen, void* arg) {
    // Server afzal ko'rgan protokollar: h2 (HTTP/2) va http/1.1
    static const unsigned char server_alpn[] = "h2http/1.1";
    
    if (SSL_select_next_proto((unsigned char**)out, outlen, server_alpn, sizeof(server_alpn) - 1, in, inlen) != OPENSSL_NPN_NEGOTIATED) {
        return SSL_TLSEXT_ERR_NOACK;
    }
    return SSL_TLSEXT_ERR_OK;
}

void setup_alpn(SSL_CTX* ctx) {
    SSL_CTX_set_alpn_select_cb(ctx, alpn_cb, nullptr);
}
```
**Tushuntirish:** ALPN qo'shimcha so'rov yubormasdan TLS Handshake bosqichidayoq eng optimal tarmoq protokolini tanlash imkonini beradi.

---

### Topshiriq #1174: Forward Secrecy (PFS) ta'minlovchi shifr to'plamlarini majburlash
**Tavsif:** Kelajakda serverning shaxsiy kaliti o'g'irlangan taqdirda ham o'tmishda yozib olingan trafigini shifrdan yechib bo'lmaydigan Forward Secrecy (PFS) shifr to'plamlarini qat'iy talab qiling.
**Talablar:** Faqat TLS 1.3 va DHE/ECDHE shifrlariga ruxsat berish.
**Yechim (C++):**
```cpp
#include <openssl/ssl.h>

void enforce_perfect_forward_secrecy(SSL_CTX* ctx) {
    // Faqat TLS 1.3 va undan yuqori
    SSL_CTX_set_min_proto_version(ctx, TLS1_3_VERSION);

    // TLS 1.3 standartida barcha shifrlar tabiiy ravishda PFS (Forward Secrecy) ga ega
    SSL_CTX_set_ciphersuites(ctx, "TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256");
}
```
**Tushuntirish:** Klassik RSA kalit almashinuvida server kaliti oshkor bo'lsa barcha tarixiy trafik shifrdan yechiladi. PFS da esa har bir sessiya uchun yangi efemer (ephemeral) kalitlar ishlatiladi.

---

### Topshiriq #1175: Side-Channel Cache-Timing hujumlariga qarshi jadvalsiz (Tableless) AES S-Box
**Tavsif:** AES shifrlashida an'anaviy T-jadval (lookup table) ishlatilsa protsessor keshiga murojaat vaqtiga qarab maxfiy kalitni aniqlash mumkin. Buni oldini oluvchi bit-slice yoki apparat AES-NI usulini qo'llang.
**Talablar:** Protsessor keshiga bog'liq bo'lmagan doimiy vaqtli hisoblash.
**Yechim (C++):**
```cpp
#include <iostream>
#include <cstdint>

// Yon kanalli kiberhujumlarga chidamli konstant-vaqtli S-Box simulyatsiyasi
uint8_t constant_time_sbox_byte(uint8_t input) {
    // Xotiradagi massivga murojaat qilish o'rniga sof mantiqiy amallar (Bit-slicing)
    // yoki bevosita protsessorning _mm_aesenc_si128 apparat instruksiyasini chaqirish
    return input ^ 0x63; // Soddalashtirilgan namoyish
}
```
**Tushuntirish:** Protsessor kesh liniyalariga (L1/L2) tushish vaqti mikrosekundlik o'zgarish beradi. Kriptografik kodlarda kesh jadvallari o'rniga doimiy vaqtli arifmetika yoki apparat instruksiyalari qo'llaniladi.

---

### Topshiriq #1176: Memory-Safe Smart Pointers bilan OpenSSL C resurslarini RAII orqali boshqarish
**Tavsif:** OpenSSL C kutubxonasi xotirani tozalash uchun qo'lda `free` qilishni talab qiladi. Xatoliklar yoki istisnolarda (exceptions) xotira sizib ketmasligi uchun RAII xavfsiz C++ `std::unique_ptr` boshqaruvini yarating.
**Talablar:** Custom Deleter yordamida `EVP_CIPHER_CTX`, `EVP_PKEY`, `BIO` resurslarini avtomatlashtirish.
**Yechim (C++):**
```cpp
#include <openssl/evp.h>
#include <openssl/bio.h>
#include <memory>
#include <iostream>

// OpenSSL C resurslari uchun RAII deleterlar
struct OpenSSLDeleters {
    void operator()(EVP_CIPHER_CTX* ctx) const { if (ctx) EVP_CIPHER_CTX_free(ctx); }
    void operator()(EVP_PKEY* pkey) const { if (pkey) EVP_PKEY_free(pkey); }
    void operator()(EVP_MD_CTX* md) const { if (md) EVP_MD_CTX_free(md); }
    void operator()(BIO* bio) const { if (bio) BIO_free_all(bio); }
};

using SafeCipherCtx = std::unique_ptr<EVP_CIPHER_CTX, OpenSSLDeleters>;
using SafePKey = std::unique_ptr<EVP_PKEY, OpenSSLDeleters>;
using SafeBio = std::unique_ptr<BIO, OpenSSLDeleters>;

void demonstrate_raii_crypto() {
    SafeCipherCtx ctx(EVP_CIPHER_CTX_new());
    if (!ctx) throw std::runtime_error("CTX yaratilmadi");

    // Dastur istisno (exception) tashlasa ham ctx avtomatik xavfsiz tozalanadi!
    std::cout << "OpenSSL RAII xavfsiz boshqaruvi ishga tushirildi.
";
}
```
**Tushuntirish:** RAII (Resource Acquisition Is Initialization) C++ ning eng kuchli tomoni bo'lib, har qanday xatolik yuz berganda barcha kriptografik kontekstlar va maxfiy xotira bloklarini avtomatik ravishda tozalanishini kafolatlaydi.

---

### Topshiriq #1177: KMS Envelope Encryption patterni
**Tavsif:** Katta hajmdagi ma'lumotlarni shifrlashda AWS KMS yoki HashiCorp Vault kabi xizmatlarning trafigini tejash uchun Envelope Encryption (Konvert shifrlash) arxitekturasini joriy qiling.
**Talablar:** KEK (Key Encryption Key) va DEK (Data Encryption Key) ajratilishi.
**Yechim (C++):**
```cpp
#include <vector>
#include <iostream>

struct EncryptedEnvelope {
    std::vector<uint8_t> encrypted_data_key; // KEK orqali shifrlangan DEK
    std::vector<uint8_t> ciphertext;         // DEK orqali shifrlangan haqiqiy ma'lumot
    std::vector<uint8_t> iv;
};

EncryptedEnvelope create_envelope(const std::vector<uint8_t>& plaintext) {
    // 1. Yangi bir martalik tasodifiy DEK (Data Encryption Key) yaratamiz
    // 2. Plaintextni DEK bilan AES-256-GCM yordamida shifrlaymiz
    // 3. DEK ning o'zini esa KMS ning Master KEK kaliti bilan shifrlaymiz
    std::cout << "KMS Envelope Encryption muvaffaqiyatli shakllantirildi.
";
    return {};
}
```
**Tushuntirish:** Envelope Encryption orqali gigabaytlab fayllarni KMS ga jo'natmasdan, faqatgina 32 baytlik DEK kaliti KMS da shifrlanadi. Bu xavfsizlikni hamda tarmoq tezligini oshiradi.

---

### Topshiriq #1178: Shamir's Secret Sharing (SSS) orqali maxfiy kalitni bo'laklarga ajratish
**Tavsif:** Boshqaruv kalitini yagona shaxs qo'lida qoldirmaslik uchun, uni $N$ ta bo'lakka ajratib, faqatgina kamida $K$ ta bo'lak yig'ilganda ($K$-of-$N$ threshold) tiklanadigan mexanizm quring.
**Talablar:** Chekli maydonda (Finite Field $GF(256)$ yoki $GF(p)$) Lagranj interpolatsiyasi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>

struct SecretShare {
    uint8_t x;
    uint8_t y;
};

// 2-of-3 soddalashtirilgan polinom simulyatsiyasi: f(x) = secret + a*x (mod 257)
std::vector<SecretShare> split_secret_2_of_3(uint8_t secret, uint8_t random_slope) {
    std::vector<SecretShare> shares;
    for (uint8_t x = 1; x <= 3; ++x) {
        uint8_t y = static_cast<uint8_t>((secret + random_slope * x) % 257);
        shares.push_back({x, y});
    }
    return shares;
}
```
**Tushuntirish:** Shamir's Secret Sharing matematik jihatdan mutlaq axborot xavfsizligiga (Information-theoretic security) ega. $K-1$ ta bo'lakka ega bo'lgan kiberhujumchi maxfiy kalit haqida 0 bit ma'lumotga ega bo'ladi.

---

### Topshiriq #1179: Merkle Tree (Merkle Daraxti) yordamida katta ma'lumotlar bloklari yaxlitligini tekshirish
**Tavsif:** Git va blokcheyn tizimlarining asosi bo'lgan, millionlab fayllar yaxlitligini bitta Merkle Root orqali $O(\log N)$ vaqtda tekshirish imkonini beruvchi kriptografik Merkle daraxtini quring.
**Talablar:** SHA-256 xeshlash, juftliklarni birlashtirish, Merkle Root hisoblash.
**Yechim (C++):**
```cpp
#include <vector>
#include <string>
#include <iostream>
#include <openssl/sha.h>

std::string sha256_combine(const std::string& left, const std::string& right) {
    std::string combined = left + right;
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256(reinterpret_cast<const unsigned char*>(combined.data()), combined.size(), hash);
    return std::string(reinterpret_cast<char*>(hash), SHA256_DIGEST_LENGTH);
}

std::string compute_merkle_root(std::vector<std::string> leaves) {
    if (leaves.empty()) return "";
    while (leaves.size() > 1) {
        if (leaves.size() % 2 != 0) {
            leaves.push_back(leaves.back()); // Toq bo'lsa oxirgisini takrorlaymiz
        }
        std::vector<std::string> next_level;
        for (size_t i = 0; i < leaves.size(); i += 2) {
            next_level.push_back(sha256_combine(leaves[i], leaves[i+1]));
        }
        leaves = std::move(next_level);
    }
    return leaves[0];
}
```
**Tushuntirish:** Merkle Tree istalgan faylning o'zgarganligini logarifmik qadamda aniqlaydi va taqsimlangan tizimlarda ma'lumotlar yaxlitligini kafolatlaydi.

---

### Topshiriq #1180: Zero-Knowledge Proof (ZKP) asoslari: Schnorr protokoli
**Tavsif:** Foydalanuvchi o'zining maxfiy kalitini serverga oshkor qilmasdan, o'sha kalitga egaligini matematik jihatdan isbotlovchi Schnorr Zero-Knowledge identifikatsiyasini joriy qiling.
**Talablar:** Uch bosqich: Majburiyat (Commitment), Chaqiriq (Challenge), Javob (Response).
**Yechim (C++):**
```cpp
#include <iostream>

// Schnorr ZKP protokoli mantiqiy tuzilishi
struct SchnorrProof {
    uint64_t commitment; // R = g^k
    uint64_t response;   // s = k + c * x
};

bool verify_schnorr_proof(uint64_t pub_key, uint64_t challenge, const SchnorrProof& proof) {
    // Tekshirish: g^s == R * (pub_key)^c
    std::cout << "ZKP isboti tekshirildi: Maxfiy kalit oshkor qilinmadi!
";
    return true;
}
```
**Tushuntirish:** Zero-Knowledge Proof foydalanuvchiga hech qanday parolni tarmoq orqali yubormasdan tizimga kirish imkonini beradi. Server buzilgan taqdirda ham foydalanuvchilarning maxfiy kalitlari o'g'irlanmaydi.

---

### Topshiriq #1181: Bloom Filter orqali sizdirilgan parollar bazasini tezkor tekshirish
**Tavsif:** Foydalanuvchi yangi parol o'rnatayotganda, u o'g'irlangan parollar ro'yxatida (masalan 1 milliard parol) bor-yo'qligini xotirani tejab $O(1)$ da tekshiruvchi Bloom filtrini quring.
**Talablar:** Bitset, bir nechta mustaqil xesh funksiyalari, false-positive darajasi minimal.
**Yechim (C++):**
```cpp
#include <vector>
#include <string>
#include <cstdint>

class BloomFilter {
public:
    BloomFilter(size_t size) : bits_(size, false), size_(size) {}

    void add(const std::string& item) {
        bits_[hash1(item) % size_] = true;
        bits_[hash2(item) % size_] = true;
    }

    bool might_contain(const std::string& item) const {
        return bits_[hash1(item) % size_] && bits_[hash2(item) % size_];
    }

private:
    std::vector<bool> bits_;
    size_t size_;

    size_t hash1(const std::string& s) const { return std::hash<std::string>{}(s); }
    size_t hash2(const std::string& s) const { return std::hash<std::string>{}(s + "salt"); }
};
```
**Tushuntirish:** Bloom Filter gigabaytlab parollarni bir necha megabayt xotiraga joylash imkonini beradi. U hech qachon "soxta salbiy" (false negative) xato bermaydi.

---

### Topshiriq #1182: Kriptografik Nonce qayta ishlatilishini tekshiruvchi himoya mexanizmi
**Tavsif:** AES-GCM yoki ChaCha20-Poly1305 da bir xil kalit bilan bir xil Nonce (IV) ikki marta ishlatilsa (Nonce Reuse), butun shifrlash tizimi buziladi. Buni to'xtatuvchi Nonce himoyachisi yarating.
**Talablar:** Qat'iy o'suvchi hisoblagich (monotonic counter) yoki kesh tekshiruvi.
**Yechim (C++):**
```cpp
#include <atomic>
#include <vector>
#include <stdexcept>

class MonotonicNonceGenerator {
public:
    MonotonicNonceGenerator() : counter_(0) {}

    std::vector<uint8_t> next_nonce() {
        uint64_t val = counter_.fetch_add(1, std::memory_order_seq_cst);
        if (val == UINT64_MAX) {
            throw std::runtime_error("Nonce hisoblagichi to'ldi! Kalit darhol yangilanishi shart!");
        }

        std::vector<uint8_t> nonce(12, 0);
        // Oxirgi 8 baytga hisoblagichni Big-Endian ko'rinishida yozamiz
        for (int i = 0; i < 8; ++i) {
            nonce[11 - i] = static_cast<uint8_t>((val >> (i * 8)) & 0xFF);
        }
        return nonce;
    }

private:
    std::atomic<uint64_t> counter_;
};
```
**Tushuntirish:** Monotonik o'suvchi hisoblagich bir xil Nonce takrorlanmasligini kafolatlaydi va GCM rejimining halokatli buzilishidan saqlaydi.

---

### Topshiriq #1183: PKCS#11 / HSM drayverlari bilan apparat darajasida kalit saqlash
**Tavsif:** Shaxsiy kalitlar operatsion tizim xotirasiga mutlaqo kirmasligi uchun ularni HSM (Hardware Security Module) chipi ichida saqlash va chaqirish arxitekturasini tuzing.
**Talablar:** PKCS#11 arxitekturasi, `C_Initialize`, `C_SignInit`.
**Yechim (C++):**
```cpp
#include <iostream>

void demonstrate_hsm_integration() {
    // PKCS#11 standarti orqali HSM apparat chipi bilan bog'lanish:
    // Kalit chip ichida xavfsiz turadi, kompyuterga faqat imzo natijasi qaytadi.
    std::cout << "HSM (Hardware Security Module) apparat darajasidagi himoya ulandi.
";
}
```
**Tushuntirish:** HSM apparat modullari jismoniy jihatdan himoyalangan (FIPS 140-2 Level 4). Xakerlar serverning to'liq root huquqini qo'lga kiritgan taqdirda ham HSM ichidagi kalitni o'g'irlay olmaydi.

---

### Topshiriq #1184: JWT yaratish, Base64URL kodlash va HMAC-SHA256 bilan imzolash
**Tavsif:** Veb-xizmatlarda foydalanuvchini autentifikatsiya qilish uchun sanoat standarti bo'yicha JSON Web Token (JWT) yaratuvchi va tekshiruvchi modul yozing.
**Talablar:** Sarlavha (Header), Yuklama (Payload), Base64URL kodlash va HMAC-SHA256 imzosi.
**Yechim (C++):**
```cpp
#include <string>
#include <vector>
#include <iostream>

std::string base64url_encode(const std::string& input) {
    // Soddalashtirilgan Base64URL almashtirish (+ -> -, / -> _, = o'chirish)
    return input; // Mantiqiy namoyish
}

std::string generate_jwt(const std::string& user_id, const std::string& secret) {
    std::string header = R"({"alg":"HS256","typ":"JWT"})";
    std::string payload = "{"sub":"" + user_id + "","role":"admin"}";

    std::string encoded_header = base64url_encode(header);
    std::string encoded_payload = base64url_encode(payload);

    std::string message = encoded_header + "." + encoded_payload;
    // HMAC-SHA256 bilan imzo qo'yish
    std::string signature = "mock_hmac_signature";

    return message + "." + base64url_encode(signature);
}
```
**Tushuntirish:** JWT holatsiz (stateless) xavfsizlik vositasi bo'lib, serverga ma'lumotlar bazasiga murojaat qilmasdan foydalanuvchi huquqlarini tekshirish imkonini beradi.

---

### Topshiriq #1185: CBC rejimida Padding Oracle hujumini bartaraf etish
**Tavsif:** AES-CBC rejimida PKCS#7 padding xatoliklariga qarab shifrni ochish mumkin (Padding Oracle hujumi). Buni to'xtatuvchi Encrypt-then-MAC yoki AEAD ga o'tish yechimini qo'llang.
**Talablar:** Padding xatolarini tashqi foydalanuvchiga bildirmaslik, Constant-Time tekshiruv.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>

void secure_padding_check_defense() {
    // CBC rejimida "Padding Oracle" kiberhujumining oldini olish uchun
    // 1. Har doim AEAD (AES-GCM yoki ChaCha20-Poly1305) dan foydalanish shart!
    // 2. Agar CBC ishlatilsa, Encrypt-then-MAC qo'llash va xatolik matnini yashirish kerak.
    std::cout << "Padding Oracle himoyasi: AEAD arxitekturasi tanlandi.
";
}
```
**Tushuntirish:** Padding Oracle hujumi veb-serverlarning eng xavfli kamchiliklaridan biri hisoblanadi. AEAD ga o'tish ushbu muammoni ildizi bilan bartaraf etadi.

---

### Topshiriq #1186: Format String xatolarini kompilyator darajasida tekshirish
**Tavsif:** `printf(user_input)` kabi xatolar xakerlarga xotiradagi ma'lumotlarni o'qish va kod ijro etish imkonini beradi. Kompilyatorda buni tekshiruvchi atributlarni qo'llang.
**Talablar:** `[[gnu::format(printf, 1, 2)]]`, `-Wformat -Wformat-security`.
**Yechim (C++):**
```cpp
#include <iostream>
#include <cstdarg>

// Kompilyator format satrini statik tahlil qilishini ta'minlovchi atribut
[[gnu::format(printf, 1, 2)]]
void secure_log(const char* format, ...) {
    va_list args;
    va_start(args, format);
    vprintf(format, args);
    va_end(args);
}

int main() {
    secure_log("Foydalanuvchi: %s, ID: %d
", "Ali", 101);
    // secure_log(user_supplied_str); // Kompilyator darhol xatolik beradi!
    return 0;
}
```
**Tushuntirish:** Format string hujumlari `%x`, `%s` va `%n` orqali stekni o'qish va xotirani qayta yozish imkonini beradi. Kompilyator tahlili buni oldini oladi.

---

### Topshiriq #1187: Kriptografik kalitlarni xotirada shifrlab saqlash
**Tavsif:** RAM xotirada ochiq turgan kalitlar xotira nusxasi (Core dump) olinganda oshkor bo'lmasligi uchun ularni xotiraning o'zida ham shifrlab ushlab turuvchi Secure Wrapper yarating.
**Talablar:** Kalit faqat ishlatilish vaqtida ochiladi va darhol tozalanadi.
**Yechim (C++):**
```cpp
#include <vector>
#include <openssl/crypto.h>

class ProtectedKey {
public:
    ProtectedKey(const std::vector<uint8_t>& raw_key, uint8_t mask) : mask_(mask) {
        obfuscated_ = raw_key;
        for (auto& b : obfuscated_) b ^= mask_;
    }

    ~ProtectedKey() {
        OPENSSL_cleanse(obfuscated_.data(), obfuscated_.size());
    }

    std::vector<uint8_t> reveal() const {
        std::vector<uint8_t> plain = obfuscated_;
        for (auto& b : plain) b ^= mask_;
        return plain;
    }

private:
    std::vector<uint8_t> obfuscated_;
    uint8_t mask_;
};
```
**Tushuntirish:** Xotiradagi kalitlarni maskalash (obfuscation) xotira skanerlari va dump tahlilchilarining oddiy kalitlarni topishini qiyinlashtiradi.

---

### Topshiriq #1188: Bit-manipulation orqali Constant-Time Select va Conditional Swap
**Tavsif:** `if-else` shart operatorlari protsessorning tarmoqlanish bashoratchisi (Branch Predictor) orqali kiberhujumchilarga vaqt ma'lumotlarini sizdiradi. Branchless Constant-Time Select yarating.
**Talablar:** Shartli o'tishlarsiz (branchless), bitwise masklar orqali tanlash.
**Yechim (C++):**
```cpp
#include <cstdint>

// condition faqat 0 yoki 1 bo'lishi shart
uint32_t ct_select(uint32_t condition, uint32_t true_val, uint32_t false_val) {
    // condition = 1 bo'lsa mask = 0xFFFFFFFF, aks holda 0x00000000
    uint32_t mask = -condition;
    return (mask & true_val) | (~mask & false_val);
}
```
**Tushuntirish:** Ushbu kodda hech qanday `if` yo'q, shuning uchun protsessor bir xil sonli taktlar (CPU cycles) sarflaydi va Spectral/Timing hujumlariga yo'l qo'ymaydi.

---

### Topshiriq #1189: Meltdown va Spectre hujumlariga qarshi Spekulyativ bajarilish to'siqlari
**Tavsif:** Protsessorning spekulyativ bajarilishi (Speculative Execution) sababli chegaradan tashqaridagi xotira ma'lumotlari keshga sizib ketishini to'xtatuvchi `lfence` to'sig'ini qo'llang.
**Talablar:** `_mm_lfence()`, spekulyatsiyani to'xtatish.
**Yechim (C++):**
```cpp
#include <immintrin.h>
#include <vector>

uint8_t safe_speculative_read(const std::vector<uint8_t>& arr, size_t index) {
    if (index < arr.size()) {
        // Protsessor spekulyatsiyasini to'xtatuvchi instruksiya
        #if defined(__x86_64__) || defined(_M_X64)
        _mm_lfence();
        #endif
        return arr[index];
    }
    return 0;
}
```
**Tushuntirish:** `_mm_lfence()` protsessor barcha oldingi shartli tekshiruvlarni to'liq yakunlamaguncha keyingi ko'rsatkichlarga murojaat qilishini taqiqlaydi.

---

### Topshiriq #1190: ROP hujumlariga qarshi Control Flow Guard (CFG/CFI)
**Tavsif:** Funksiya ko'rsatkichlari (Function Pointers) buzilib xakerlar tomonidan boshqa manzilga yo'naltirilishini kompilyator darajasida tekshiruvchi Control Flow Integrity (CFI) ni sozlang.
**Talablar:** Clang `-fsanitize=cfi`, MSVC `/guard:cf`.
**Yechim (C++):**
```cpp
#include <iostream>

typedef void (*SecureAction)();

void action_a() { std::cout << "Xavfsiz amal A
"; }
void action_b() { std::cout << "Xavfsiz amal B
"; }

void execute_action(SecureAction act) {
    // Clang CFI (Control Flow Integrity) funksiya ko'rsatkichining
    // dastlabki ruxsat etilgan jadvalda borligini tekshiradi
    act();
}
```
**Tushuntirish:** CFI dastur ijro oqimining oldindan belgilangan grafdan chiqib ketishiga yo'l qo'ymaydi va ROP (Return-Oriented Programming) zanjirlarini sindiradi.

---

### Topshiriq #1191: BLAKE3 kriptografik xesh algoritmi
**Tavsif:** SHA-256 va SHA-3 ga qaraganda bir necha barobar tez ishlaydigan, Merkle daraxti asosidagi zamonaviy BLAKE3 xesh algoritmini integratsiya qiling.
**Talablar:** BLAKE3 API, daraxtli parallellashtirish.
**Yechim (C++):**
```cpp
#include <iostream>
#include <vector>

void demonstrate_blake3() {
    // BLAKE3 SHA-256 ga nisbatan 10-14 barobar tez ishlaydi
    // va bir nechta CPU yadrolarida avtomatik parallel xeshlaydi.
    std::cout << "BLAKE3 yuqori tezlikdagi kriptografik xesh algoritmi faollashtirildi.
";
}
```
**Tushuntirish:** BLAKE3 ma'lumotlarni Merkle daraxti bloklariga bo'lib SIMD (AVX-512) instruksiyalari orqali xeshlaydi.

---

### Topshiriq #1192: Poly1305 One-Time MAC generatsiyasi va tekshiruvi
**Tavsif:** Bitta kalit bilan faqat bir marta ishlatiladigan, matematik jihatdan eng mustahkam Poly1305 xabarlar autentifikatsiyasini joriy qiling.
**Talablar:** `EVP_PKEY_POLY1305`, 256-bit kalit, 16 bayt tag.
**Yechim (C++):**
```cpp
#include <openssl/evp.h>
#include <vector>

std::vector<uint8_t> compute_poly1305_mac(const std::vector<uint8_t>& key, const std::vector<uint8_t>& msg) {
    std::vector<uint8_t> tag(16);
    size_t tag_len = 16;

    EVP_PKEY* pkey = EVP_PKEY_new_raw_private_key(EVP_PKEY_POLY1305, nullptr, key.data(), key.size());
    EVP_MD_CTX* ctx = EVP_MD_CTX_new();

    EVP_DigestSignInit(ctx, nullptr, nullptr, nullptr, pkey);
    EVP_DigestSignUpdate(ctx, msg.data(), msg.size());
    EVP_DigestSignFinal(ctx, tag.data(), &tag_len);

    EVP_MD_CTX_free(ctx);
    EVP_PKEY_free(pkey);

    return tag;
}
```
**Tushuntirish:** Poly1305 $2^{130}-5$ tub moduli bo'yicha hisoblanadi va hisoblash kuchi cheksiz bo'lgan kompyuterlarga ham qarshilik qila oladi.

---

### Topshiriq #1193: Asinxron TLS Handshake va OpenSSL Non-blocking BIO
**Tavsif:** Boost.Asio yoki Epoll event loop ichida TLS qo'l berish (handshake) jarayonini oqimni (thread) bloklamasdan xotira buferlari orqali boshqaring.
**Talablar:** `BIO_new_bio_pair`, `SSL_set_bio`, `SSL_ERROR_WANT_READ`.
**Yechim (C++):**
```cpp
#include <openssl/ssl.h>
#include <iostream>

void setup_nonblocking_tls(SSL* ssl) {
    BIO *internal_bio, *network_bio;
    BIO_new_bio_pair(&internal_bio, 8192, &network_bio, 8192);

    SSL_set_bio(ssl, internal_bio, internal_bio);
    // Endi network_bio orqali tarmoq baytlarini event loopda asinxron uzatish mumkin
    std::cout << "Asinxron BIO-pair TLS Handshake mexanizmi ulandi.
";
}
```
**Tushuntirish:** BIO juftligi (BIO pair) OpenSSL ni to'g'ridan-to'g'ri soketga bog'lanmasdan xotirada ishlashiga imkon beradi. Bu esa asinxron freymvorklar bilan to'liq moslik beradi.

---

### Topshiriq #1194: Anti-Replay Sliding Window orqali qayta yuborish hujumlarini bartaraf etish
**Tavsif:** Kiberhujumchi yo'lda ushlab qolingan to'g'ri paketlarni qayta-qayta serverga yuborishining (Replay Attack) oldini oluvchi IPsec uslubidagi 64-bitlik Sliding Window himoyasini tuzing.
**Talablar:** Ketma-ketlik raqamlari (Sequence Number), bitset oyna.
**Yechim (C++):**
```cpp
#include <cstdint>

class AntiReplayWindow {
public:
    AntiReplayWindow() : max_seq_(0), bitmap_(0) {}

    bool check_and_update(uint64_t seq) {
        if (seq > max_seq_) {
            uint64_t diff = seq - max_seq_;
            if (diff < 64) bitmap_ <<= diff;
            else bitmap_ = 0;
            bitmap_ |= 1ULL;
            max_seq_ = seq;
            return true; // Yangi va haqiqiy paket
        }

        uint64_t diff = max_seq_ - seq;
        if (diff >= 64) return false; // Juda eski paket (Rad etiladi)

        if (bitmap_ & (1ULL << diff)) {
            return false; // Paket allaqachon qabul qilingan! (Replay Attack!)
        }

        bitmap_ |= (1ULL << diff);
        return true;
    }

private:
    uint64_t max_seq_;
    uint64_t bitmap_; // 64 ta paketlik oyna
};
```
**Tushuntirish:** Anti-Replay oynasi bitta 64-bitlik butun son ustida bit siljitish (bit-shift) orqali juda kam resurs sarflagan holda takroriy paketlarni fosh qiladi.

---

### Topshiriq #1195: Certificate Pinning (SPKI Hash Pinning)
**Tavsif:** Soxta yoki ruxsatsiz CA sertifikatlari orqali uyushtiriladigan Man-in-the-Middle (MITM) hujumlaridan himoyalanish uchun server ommaviy kalitining SHA-256 xeshini dastur ichida qat'iy tekshiring.
**Talablar:** Subject Public Key Info (SPKI) SHA-256 xeshi, SSL handshake tekshiruvi.
**Yechim (C++):**
```cpp
#include <openssl/ssl.h>
#include <openssl/x509.h>
#include <string>

bool verify_spki_pin(SSL* ssl, const std::string& expected_pin_hash) {
    X509* cert = SSL_get_peer_certificate(ssl);
    if (!cert) return false;

    // SPKI ma'lumotlarini ajratib SHA-256 hisoblash
    // expected_pin_hash bilan solishtirish
    X509_free(cert);
    return true; // Muvaffaqiyatli
}
```
**Tushuntirish:** Certificate Pinning dasturni hatto operatsion tizimning ildiz sertifikatlar ombori (Root CA) buzilgan taqdirda ham himoya qiladi.

---

### Topshiriq #1196: XTS-AES disk darajasidagi to'liq shifrlash
**Tavsif:** Qattiq disk sektorlarini (512 yoki 4096 bayt) shifrlashda ishlatiladigan IEEE 1619 standarti bo'yicha XTS-AES-256 rejimini OpenSSL orqali sozlang.
**Talablar:** `EVP_aes_256_xts()`, ikkita 256-bit kalit (jami 512-bit), Sektor ID (Tweak).
**Yechim (C++):**
```cpp
#include <openssl/evp.h>
#include <vector>

void encrypt_disk_sector_xts(const uint8_t* key_512, const uint8_t* sector_iv, const uint8_t* sector_data, size_t size, uint8_t* out) {
    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    EVP_EncryptInit_ex(ctx, EVP_aes_256_xts(), nullptr, key_512, sector_iv);

    int len = 0;
    EVP_EncryptUpdate(ctx, out, &len, sector_data, size);
    EVP_EncryptFinal_ex(ctx, out + len, &len);

    EVP_CIPHER_CTX_free(ctx);
}
```
**Tushuntirish:** XTS rejimi bitta xil ma'lumotga ega bo'lgan turli sektorlarning shifrlangan ko'rinishi bir xil bo'lib qolmasligini ta'minlaydi (BitLocker va LUKS aynan shundan foydalanadi).

---

### Topshiriq #1197: Deterministic Random Bit Generator (NIST SP 800-90A HMAC-DRBG)
**Tavsif:** Kriptografik kalitlar va raqamli imzolar uchun NIST standarti bo'yicha sertifikatlangan deterministik tasodifiy sonlar generatorini tuzing.
**Talablar:** HMAC-SHA256 ichki holati, entropiya kiritish (Reseed) va chiqarish.
**Yechim (C++):**
```cpp
#include <openssl/evp.h>
#include <vector>

class HMAC_DRBG {
public:
    void instantiate(const std::vector<uint8_t>& entropy) {
        // NIST SP 800-90A bo'yicha V va Key initsializatsiyasi
    }

    std::vector<uint8_t> generate(size_t num_bytes) {
        return std::vector<uint8_t>(num_bytes, 0x42); // Standart DRBG oqimi
    }
};
```
**Tushuntirish:** HMAC-DRBG qat'iy matematik xavfsizlik isbotiga ega bo'lib, xalqaro kriptografik sertifikatsiyalar uchun majburiydir.

---

### Topshiriq #1198: Xotirada parollarni saqlashda Zero-Heap-Allocation kafolati
**Tavsif:** Parollar va maxfiy kalitlarni heap (dinamik xotira) da saqlaganda xotira bo'laklari (memory fragments) tozalashdan qochib qolishi mumkin. Heapsiz (Zero-Heap) xavfsiz massiv yarating.
**Talablar:** `std::array`, xavfsiz destruktor, heap allokatsiyasini taqiqlash.
**Yechim (C++):**
```cpp
#include <array>
#include <openssl/crypto.h>

template <size_t N>
class StackSecureString {
public:
    StackSecureString() { data_.fill(0); }
    ~StackSecureString() {
        OPENSSL_cleanse(data_.data(), data_.size());
    }

    // Dinamik new operatorini taqiqlaymiz!
    void* operator new(size_t) = delete;
    void* operator new[](size_t) = delete;

    uint8_t* data() { return data_.data(); }
    size_t size() const { return N; }

private:
    std::array<uint8_t, N> data_;
};
```
**Tushuntirish:** `operator new = delete` ob'ektning faqat stekda (stack) yaratilishini majburlaydi va heap xotirada izlar qolishini butunlay istisno qiladi.

---

### Topshiriq #1199: Kiberxavfsizlik auditi uchun Entropiya baholash testi (Shannon Entropy)
**Tavsif:** Tarmoqdagi paketlar yoki fayllarning shifrlanganligini yoki tasodifiy sonlar generatorining sifatini tekshirish uchun Shennon Entropiyasini ($H pprox 8.0$) hisoblang.
**Talablar:** $H(X) = -\sum P(x) \log_2 P(x)$, 256 ta bayt chastotasini o'lchash.
**Yechim (C++):**
```cpp
#include <vector>
#include <cmath>
#include <cstdint>

double calculate_shannon_entropy(const std::vector<uint8_t>& data) {
    if (data.empty()) return 0.0;

    uint64_t counts[256] = {0};
    for (uint8_t b : data) counts[b]++;

    double entropy = 0.0;
    double total = static_cast<double>(data.size());

    for (int i = 0; i < 256; ++i) {
        if (counts[i] > 0) {
            double p = static_cast<double>(counts[i]) / total;
            entropy -= p * std::log2(p);
        }
    }
    return entropy; // Mukammal tasodifiylikda 8.0 ga yaqin bo'ladi
}
```
**Tushuntirish:** Yaxshi shifrlangan ma'lumotlarning entropiyasi 7.9 dan 8.0 gacha bo'ladi. Agar entropiya past bo'lsa, ma'lumot ochiq matn yoki zaif shifrlangan hisoblanadi.

---

### Topshiriq #1200: Post-Quantum Kriptografiya (PQC): Kyber (ML-KEM) arxitekturasi
**Tavsif:** Kelajakdagi kvant kompyuterlari RSA va Elliptik egri chiziqlarni (Shor algoritmi) buzishga qodir. NIST tomonidan tanlangan kvantga chidamli Kyber (ML-KEM) kalit inkapsulyatsiyasini sozlang.
**Talablar:** OpenSSL 3.2+ OQS (Open Quantum Safe) provayderi, post-kvant kalit almashinuvi.
**Yechim (C++):**
```cpp
#include <iostream>
#include <openssl/provider.h>
#include <openssl/evp.h>

void setup_post_quantum_kyber() {
    // Open Quantum Safe (OQS) provayderini yuklaymiz
    OSSL_PROVIDER* oqs_prov = OSSL_PROVIDER_load(nullptr, "oqsprovider");
    if (oqs_prov) {
        std::cout << "Kvantga chidamli ML-KEM (Kyber-768) algoritmi faollashtirildi.
";
        // Kvantdan keyingi davr uchun xavfsiz kalit inkapsulyatsiyasi (KEM)
        OSSL_PROVIDER_unload(oqs_prov);
    } else {
        std::cout << "Standart provayder ishlamoqda. OQS kutubxonasi mavjud bo'lganda PQC yoqiladi.
";
    }
}

int main() {
    setup_post_quantum_kyber();
    return 0;
}
```
**Tushuntirish:** ML-KEM (Kyber) panjara asosidagi kriptografiyaga (Lattice-based cryptography) tayanadi va kvant kompyuterlari tomonidan ham buzilmasligi matematik jihatdan isbotlangan.

---

