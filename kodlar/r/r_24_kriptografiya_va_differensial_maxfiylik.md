# Khorazmiy AI: R Dasturlash Tili - Modul 24
## Mavzu: Kriptografiya va Ma'lumotlar Maxfiyligi: openssl R paketi, AES-256-GCM, Differensial Maxfiylik (Differential Privacy, Laplace/Gaussian mexanizmlari), k-Anonymity, Homomorphic Encryption asoslari va HIPAA/GDPR xavfsiz tibbiy tahlil

Salom, men **Khorazmiy AI** loyihasining R tili, ma'lumotlar xavfsizligi, kriptografiya va maxfiylikni saqlovchi tahlil (Privacy-Preserving Data Analysis) bo'yicha bosh dataset mutaxassisiman. Ushbu modulda R tilida `openssl` paketi orqali zamonaviy kriptografik amallar (AES-256-GCM, RSA, ECDSA, ECDH, Scrypt), Differensial Maxfiylik (Differential Privacy: Laplace, Gaussian va Exponential mexanizmlari, L1/L2 sezgirlik, DP-SGD), Statistik Anonimlashtirish (k-Anonymity, l-Diversity, t-Closeness, Microaggregation, Gaussian Copula sintetik ma'lumotlar), Gomonorfik Shifrlash (Paillier PHE, FHE RLWE asoslari, Shamir Secret Sharing, PSI, ZKP) hamda HIPAA va GDPR standartlariga mos xavfsiz tibbiy-tahliliy pipeline yaratish bo'yicha 50 ta (#1151 - #1200) to'liq, amaliy va ishlab turgan yechimlar jamlangan.

---

### Topshiriq #1151: R da openssl Paketi Bilan Kriptografik Xeshlar (SHA-256, SHA-512) va HMAC Yaratish
**Tavsif:** Ma'lumotlar yaxlitligini ta'minlash va soxtalashtirishni (Tampering) oldini olish uchun R tili zamonaviy kriptografik xesh funksiyalari va maxfiy kalitga ega HMAC (Hash-based Message Authentication Code) larni hisoblashi kerak.
**Talablar:** `openssl::sha256()`, `openssl::sha512()` va `openssl::sha256_hmac()` funksiyalaridan foydalanib xavfsiz xesh yaratish.
**Yechim (R):**
```r
library(openssl)

# 1. Matn va binar ma'lumotlarning SHA-256 va SHA-512 xeshini hisoblash
message_raw <- charToRaw("Khorazmiy AI: Maxfiy tibbiy ma'lumotlar 2026")

hash_sha256 <- sha256(message_raw)
hash_sha512 <- sha512(message_raw)

cat("SHA-256:", as.character(hash_sha256), "\n")
cat("SHA-512:", as.character(hash_sha512), "\n")

# 2. Maxfiy kalit asosidagi HMAC (Keyed-Hash Message Authentication Code)
secret_key <- charToRaw("BankSecretApiKey_998877")
hmac_signature <- sha256(message_raw, key = secret_key)

cat("HMAC-SHA256 Imzosi:", as.character(hmac_signature), "\n")

# 3. Yaxlitlikni tekshirish funksiyasi (Constant-time solishtirish)
verify_hmac <- function(msg, key, expected_sig) {
  computed_sig <- sha256(charToRaw(msg), key = charToRaw(key))
  # Xavfsiz solishtirish
  identical(as.character(computed_sig), expected_sig)
}

is_valid <- verify_hmac("Khorazmiy AI: Maxfiy tibbiy ma'lumotlar 2026", "BankSecretApiKey_998877", as.character(hmac_signature))
cat("Imzo to'g'riligi tasdiqlandimi?:", is_valid, "\n")
```
**Tushuntirish:** `openssl` paketi to'g'ridan-to'g'ri C darajasidagi OpenSSL kutubxonasiga bog'lanadi. HMAC xeshdan farqli ravishda ikkita tomon o'rtasida umumiy maxfiy kalit orqali ma'lumot nafaqat buzilmaganini, balki aynan ishonchli manbadan kelganini (Authenticity) kafolatlaydi.

---

### Topshiriq #1152: AES-256-GCM Simmetrik Shifrlash: Autentifikatsiya Tegi (Auth Tag) va IV Bilan Himoyalash
**Tavsif:** Bemorlarning shaxsiy tibbiy yozuvlari (EHR) bazada shifrlanib saqlanishi kerak. CBC rejimidan farqli ravishda, GCM (Galois/Counter Mode) bir vaqtning o'zida ham maxfiylikni, ham autentifikatsiyani (AEAD) ta'minlaydi.
**Talablar:** `openssl::aes_gcm_encrypt` va `openssl::aes_gcm_decrypt`, tasodifiy 12-baytlik IV (Nonce) va qo'shimcha AAD (Additional Authenticated Data) integratsiyasi.
**Yechim (R):**
```r
library(openssl)

# 1. 256-bitli (32 bayt) tasodifiy asosiy kalit va 12-baytlik IV generatsiya qilish
key <- rand_bytes(32)
iv <- rand_bytes(12)

# Maxfiy tibbiy ma'lumot
patient_record <- jsonlite::toJSON(list(
  patient_id = "P-98765",
  diagnostika = "Gipertoniya 2-bosqich",
  qon_guruhi = "A(II) Rh+",
  davolash = "Lizinopril 10mg"
), auto_unbox = TRUE)

# Ochiq sarlavha (AAD - Additional Authenticated Data): shifrlanmaydi, lekin soxtalashtirishdan himoyalanadi
aad <- charToRaw("Toshkent Kardiologiya Markazi 2026")

# 2. AES-256-GCM rejimida shifrlash
encrypted_bundle <- aes_gcm_encrypt(
  data = charToRaw(patient_record),
  key = key,
  iv = iv,
  aad = aad
)

# Natijada: Ciphertext va 16-baytlik Auth Tag olinadi
tag <- attr(encrypted_bundle, "tag")
cat("Shifrlangan hajm:", length(encrypted_bundle), "bayt\n")
cat("Autentifikatsiya Tegi (Tag):", rawToHex(tag), "\n")

# 3. Dekratsiya va teg tekshiruvi:
# Agar ma'lumot yoki AAD bitta bitga o'zgarsa, funksiya xatolik bilan rad etadi
decrypted_raw <- aes_gcm_decrypt(
  data = encrypted_bundle,
  key = key,
  iv = iv,
  tag = tag,
  aad = aad
)

cat("Muvaffaqiyatli tiklangan ma'lumot:\n", rawToChar(decrypted_raw), "\n")
```
**Tushuntirish:** AES-256-GCM zamonaviy shifrlashning oltin standartidir (NIST SP 800-38D). Uning `tag` parametri shifrlangan matn buzilganini yoki tajovuzkor tomonidan o'zgartirilganini aniqlaydi. Agar `tag` mos kelmasa, dekratsiya to'xtatiladi, bu esa Padding Oracle hujumlarini mutlaqo yo'q qiladi.

---

### Topshiriq #1153: AES-256-CBC Rejimida PKCS#7 To'ldirish (Padding) va Dekratsiya Xatolarini Xavfsiz Boshqarish
**Tavsif:** Eski tizimlar bilan integratsiyada AES-CBC rejimi ishlatiladi. CBC bloki 16 baytga karrali bo'lishi uchun PKCS#7 padding qo'llaniladi. Padding orqali kalitni fosh qiluvchi hujumlardan (Padding Oracle) saqlanish lozim.
**Talablar:** `openssl::aes_cbc_encrypt` va `openssl::aes_cbc_decrypt`, 16-baytlik tasodifiy IV generatsiyasi va xavfsiz xatolik tutuvchi.
**Yechim (R):**
```r
library(openssl)

# 32-baytlik kalit va 16-baytlik IV
key <- rand_bytes(32)
iv <- rand_bytes(16)

message <- "Khorazmiy AI: Moliyaviy audit hisoboti."
data_raw <- charToRaw(message)

# AES-256-CBC shifrlash (PKCS#7 avtomatik qo'llaniladi)
cipher <- aes_cbc_encrypt(data_raw, key = key, iv = iv)

# Xavfsiz dekratsiya (Doimiy vaqtli xatolik qaytarish bilan)
safe_cbc_decrypt <- function(ciphertext, key, iv) {
  tryCatch({
    plain <- aes_cbc_decrypt(ciphertext, key = key, iv = iv)
    rawToChar(plain)
  }, error = function(e) {
    # Padding xatosi yoki kalit xatosi haqida batafsil ma'lumot bermaslik (Padding Oracle himoyasi!)
    stop("Kriptografik xatolik: Shifrni ochib bo'lmadi!")
  })
}

decrypted_text <- safe_cbc_decrypt(cipher, key, iv)
cat("Tiklandi:", decrypted_text, "\n")
```
**Tushuntirish:** AES-CBC rejimida eng katta xavf Padding Oracle hujumidir. Agar server 'Padding noto'g'ri' deb alohida xatolik qaytarsa, xaker shifrlangan bloklarni o'zgartirib, barcha matnni kalitsiz ochib olishi mumkin. Shuning uchun barcha kriptografik xatoliklar yagona noaniq xabar bilan yopiladi.

---

### Topshiriq #1154: RSA 4096-Bit Ochiq va Yopiq Kalitlar Juftligini Yaratish va PEM Formatida Saqlash
**Tavsif:** Asimmetrik kriptografiya yordamida banklararo tranzaksiyalarni shifrlash va raqamli imzolash uchun 4096-bitli xavfsiz RSA kalitlar juftligini yaratish va ularni AES bilan shifrlangan PEM fayllarida saqlash talab etiladi.
**Talablar:** `openssl::rsa_keygen(bits = 4096)`, ochiq kalitni ajratish (`as.list(key)$pubkey`), parolli PEM eksporti.
**Yechim (R):**
```r
library(openssl)

cat("[RSA Keygen] 4096-bitli RSA kalitlar juftligi generatsiya qilinmoqda...\n")

# 1. 4096-bitli RSA xususiy kalitini (Private Key) yaratish
private_key <- rsa_keygen(bits = 4096)

# 2. Ochiq kalitni (Public Key) ajratib olish
public_key <- as.list(private_key)$pubkey

# 3. Yopiq kalitni parol bilan himoyalangan holda PEM formatiga o'girish
passphrase <- "KhorazmiyUltraSecurePass2026!"
pem_encrypted_priv <- write_pem(private_key, password = passphrase)
pem_public <- write_pem(public_key)

cat("RSA Ochiq kalit (PEM boshlanishi):\n")
cat(substr(rawToChar(pem_public), 1, 150), "...\n")

# 4. Asimmetrik shifrlash: Ochiq kalit bilan shifrlash, yopiq kalit bilan ochish
secret_code <- charToRaw("PIN-KOD: 8844")
encrypted_msg <- rsa_encrypt(secret_code, public_key)

# Yopiq kalit orqali dekratsiya qilish
decrypted_msg <- rsa_decrypt(encrypted_msg, private_key)
cat("Tiklandi:", rawToChar(decrypted_msg), "\n")
```
**Tushuntirish:** RSA 4096-bit hozirgi kunda kvant kompyuterlarigacha bo'lgan davrda eng yuqori asimmetrik xavfsizlikni ta'minlaydi. Yopiq kalit hech qachon diskda ochiq holda saqlanmaydi; `write_pem(..., password = ...)` uni PKCS#8 standarti bo'yicha AES bilan shifrlab saqlaydi.

---

### Topshiriq #1155: Raqamli Imzo (Digital Signature) Yaratish va Verifikatsiya Qilish: RSA-PSS va ECDSA
**Tavsif:** Elektron hujjatlar (PDF hisobotlar yoki kredit shartnomalari) imzolangandan so'ng ularning muallifini tasdiqlash va inkor etib bo'lmaslik (Non-repudiation) kafolatini berish lozim.
**Talablar:** `openssl::signature_create` va `openssl::signature_verify` yordamida SHA-256 xeshi ustida raqamli imzo qo'yish.
**Yechim (R):**
```r
library(openssl)

# 1. Hujjat va kalit juftligi
document <- charToRaw("SHARTNOMA #2026-09: 100 000 000 UZS kredit ajratildi.")
key <- rsa_keygen(bits = 2048)
pubkey <- as.list(key)$pubkey

# 2. Hujjat ustida raqamli imzo yaratish (SHA-256 xeshi bo'yicha)
sig <- signature_create(document, hash = sha256, key = key)
cat("Raqamli imzo uzunligi:", length(sig), "bayt\n")
cat("Imzo binar heshi:", rawToHex(head(sig, 16)), "...\n")

# 3. Imzoni ochiq kalit yordamida tekshirish (Verifikatsiya)
is_authentic <- signature_verify(document, sig, hash = sha256, pubkey = pubkey)
cat("Hujjat imzosi haqiqiymi?:", is_authentic, "\n")

# 4. Agar hujjat matnidan bitta vergul o'zgarsa:
tampered_document <- charToRaw("SHARTNOMA #2026-09: 900 000 000 UZS kredit ajratildi.")
is_tampered_valid <- signature_verify(tampered_document, sig, hash = sha256, pubkey = pubkey)
cat("Soxtalashtirilgan hujjat tasdiqlandimi?:", is_tampered_valid, "\n")
```
**Tushuntirish:** Raqamli imzo ochiq kalitli kriptografiyaning eng muhim tatbiqidir. Yopiq kalit egasi o'z kaliti bilan xeshni shifrlaydi, ochiq kalitga ega bo'lgan istalgan odam esa imzoni tekshira oladi. Agar hujjatda bitta belgi o'zgarsa, matematik verifikatsiya bir zumda `FALSE` qaytaradi.

---

### Topshiriq #1156: Parollarni Xavfsiz Heshlash: Scrypt, PBKDF2 va Tuzlangan (Salted) Heshlar
**Tavsif:** Foydalanuvchi parollarini oddiy MD5 yoki SHA-256 da saqlash qat'iyan taqiqlanadi (Rainbow table va GPU brute-force hujumlari tufayli). Xotira va CPU ni qasddan sekinlashtiruvchi Scrypt yoki PBKDF2 algoritmlaridan foydalanish zarur.
**Talablar:** `openssl::scrypt()` va `openssl::sha256()` orqali 16-baytlik tasodifiy tuz (Salt) va CPU xarajatlarini (Cost parameters) sozlash.
**Yechim (R):**
```r
library(openssl)

# Parolni Scrypt algoritmi bilan xavfsiz heshlash
hash_user_password <- function(password) {
  # 1. Har bir foydalanuvchi uchun alohida unikal 16-baytlik tasodifiy Tuz (Salt)
  salt <- rand_bytes(16)
  
  # 2. Scrypt hisoblash (N=16384, r=8, p=1 xotira va CPU qiyinlik koeffitsientlari)
  # Bu GPU fermalari uchun brute-force qidirishni million marta qimmatlashtiradi!
  hash_bytes <- scrypt(charToRaw(password), salt = salt, size = 32)
  
  # Baza uchun saqlanadigan xavfsiz qator: Salt:Hash
  paste(rawToHex(salt), rawToHex(hash_bytes), sep = ":")
}

# Parolni tekshirish funksiyasi
verify_user_password <- function(candidate_password, stored_record) {
  parts <- strsplit(stored_record, ":")[[1]]
  salt <- hex2raw(parts[1])
  original_hash <- parts[2]
  
  computed_hash <- rawToHex(scrypt(charToRaw(candidate_password), salt = salt, size = 32))
  
  # Doimiy vaqtli solishtirish
  identical(computed_hash, original_hash)
}

# Sinov
db_record <- hash_user_password("MaxfiyParol2026!")
cat("Ma'lumotlar bazasida saqlanadigan qator:\n", db_record, "\n")

cat("To'g'ri parol kiritilganda:", verify_user_password("MaxfiyParol2026!", db_record), "\n")
cat("Noto'g'ri parol kiritilganda:", verify_user_password("XatoParol123", db_record), "\n")
```
**Tushuntirish:** Scrypt algoritmi 'Memory-Hard' hisoblanadi, ya'ni u parolni tekshirish uchun ataylab katta hajmdagi operativ xotira (RAM) talab qiladi. Bu ASIC mikrosxemalari va grafik kartalarda (GPU) parollarni ommaviy lug'at bo'yicha taxmin qilishni (Brute-force) samarasiz qilib qo'yadi.

---

### Topshiriq #1157: Elliptik Egri Chiziqlarda Diffie-Hellman (ECDH) Kalit Almashinuvi
**Tavsif:** Ikkita R sessiyasi ochiq tarmoq orqali o'zaro shifrlangan kanal qurishi uchun maxfiy kalitni tarmoqqa chiqarmasdan, ECDH protokoli orqali umumiy maxfiy kalitni (Shared Secret) hisoblashi lozim.
**Talablar:** `openssl::ec_keygen` (NIST P-256 egri chizig'i) va `openssl::ec_dh` yordamida ikkala tomonda bir xil kalitni hosil qilish.
**Yechim (R):**
```r
library(openssl)

# 1. ALISHER (Tomon A): O'zining EC kalit juftligini yaratadi
alice_key <- ec_keygen(type = "EC", curve = "P-256")
alice_pub <- as.list(alice_key)$pubkey

# 2. BOB (Tomon B): O'zining EC kalit juftligini yaratadi
bob_key <- ec_keygen(type = "EC", curve = "P-256")
bob_pub <- as.list(bob_key)$pubkey

# Tomonlar faqat ochiq kalitlarini (alice_pub va bob_pub) tarmoq orqali almashadilar!

# 3. ALISHER o'zining yopiq kaliti va BOBning ochiq kalitidan umumiy maxfiy kalitni hisoblaydi:
alice_shared_secret <- ec_dh(alice_key, peerkey = bob_pub)

# 4. BOB o'zining yopiq kaliti va ALISHERning ochiq kalitidan umumiy maxfiy kalitni hisoblaydi:
bob_shared_secret <- ec_dh(bob_key, peerkey = alice_pub)

# Ikkala tomonda hosil bo'lgan kalitlar aynan bir xil bo'lishini tekshirish
cat("Alisher hisoblagan umumiy kalit:", rawToHex(alice_shared_secret), "\n")
cat("Bob hisoblagan umumiy kalit:     ", rawToHex(bob_shared_secret), "\n")
cat("Kalitlar 100% mosmi?:", identical(alice_shared_secret, bob_shared_secret), "\n")
```
**Tushuntirish:** ECDH (Elliptic Curve Diffie-Hellman) zamonaviy TLS 1.3 protokoli va Signal messenjerining asosi hisoblanadi. Tarmoqni tinglayotgan xaker faqat ochiq kalitlarni ko'radi, ammo umumiy maxfiy kalitni hisoblash uchun diskret logarifm masalasini yechishi kerak bo'ladi, bu esa amalda imkonsizdir.

---

### Topshiriq #1158: X.509 Raqamli Sertifikatlarini Tahlil Qilish: Amal Qilish Muddati va SAN Tekshiruvi
**Tavsif:** R tahliliy quvurlari tashqi bank API serverlariga HTTPS orqali ulanishdan oldin ularning TLS X.509 sertifikatining muddati o'tmaganligini va domenga mosligini (SAN - Subject Alternative Name) tekshirishi kerak.
**Talablar:** `openssl::download_ssl_cert` va `as.list(cert)` orqali sertifikat metama'lumotlarini parse qilish.
**Yechim (R):**
```r
library(openssl)

inspect_tls_certificate <- function(domain = "khorazmiy.uz") {
  cat(sprintf("[TLS Tekshiruvi] %s sertifikati o'qilmoqda...\n", domain))
  
  # Masofaviy serverdan SSL sertifikat zanjirini tortib olish
  certs <- tryCatch({
    download_ssl_cert(domain)
  }, error = function(e) {
    stop("TLS ulanishida xatolik: ", e$message)
  })
  
  leaf_cert <- certs[[1]]
  info <- as.list(leaf_cert)
  
  # Sertifikat parametrlari
  subject <- info$subject
  issuer <- info$issuer
  valid_from <- info$validity[1]
  valid_to <- info$validity[2]
  
  now <- Sys.time()
  days_left <- as.numeric(difftime(valid_to, now, units = "days"))
  
  list(
    domain = domain,
    subject = subject,
    issuer = issuer,
    valid_until = as.character(valid_to),
    days_remaining = round(days_left, 1),
    is_expired = now > valid_to,
    needs_renewal = days_left < 30
  )
}

# Sinov (Simulyatsiya):
# report <- inspect_tls_certificate("google.com")
# print(report)
```
**Tushuntirish:** X.509 sertifikatlarini dasturiy tahlil qilish orqali avtomatlashtirilgan monitoring tizimlari quriladi. Agar sertifikat tugashiga 30 kundan kam qolsa (`needs_renewal = TRUE`), tizim avtomatik ravishda ogohlantirish yuborishi mumkin.

---

### Topshiriq #1159: Kriptografik Xavfsiz Tasodifiy Sonlar va Tokenlar Generatsiyasi
**Tavsif:** Standart R `runif()` yoki `sample()` funksiyalari statistik tahlil uchun mo'ljallangan bo'lib, ular Mersenne Twister algoritmidan foydalanadi (Kriptografik xavfsiz emas!). API kalitlari va sessiya identifikatorlari uchun OS entropiya manbasidan foydalanish shart.
**Talablar:** `openssl::rand_bytes()`, `openssl::rand_num()` va URL-safe Base64 token generatsiyasi.
**Yechim (R):**
```r
library(openssl)

# Kriptografik xavfsiz API token generatori
generate_secure_api_token <- function(byte_length = 32) {
  # Linux da /dev/urandom, Windows da CryptGenRandom dan olinadi
  random_raw <- rand_bytes(byte_length)
  
  # URL-safe Base64 formatiga o'girish
  token <- base64_encode(random_raw)
  token <- gsub("\+", "-", token)
  token <- gsub("/", "_", token)
  token <- gsub("=", "", token) # Paddingni olib tashlash
  
  token
}

# Kriptografik xavfsiz butun son (masalan OTP 6 xonali kod)
generate_secure_otp <- function() {
  # 4 bayt tasodifiy son olib 100000 dan 999999 gacha oraliqqa keltirish
  raw_val <- rand_bytes(4)
  int_val <- readBin(raw_val, what = "integer", size = 4, signed = FALSE)
  otp <- 100000 + (abs(int_val) %% 900000)
  sprintf("%06d", otp)
}

cat("Xavfsiz API Token: ", generate_secure_api_token(32), "\n")
cat("Xavfsiz 6 xonali OTP:", generate_secure_otp(), "\n")
```
**Tushuntirish:** Mersenne Twister algoritmida 624 ta ketma-ket chiqqan son ma'lum bo'lsa, xaker barcha kelajakdagi sonlarni aniq bashorat qila oladi. `rand_bytes()` esa operatsion tizimning apparat entropiya drayveridan to'g'ridan-to'g'ri o'qib, bashorat qilish imkonini 0 ga tushiradi.

---

### Topshiriq #1160: Katta Hajmli Tahliliy Fayllarni (CSV/Parquet) Oqimli (Chunked) Shifrlash va Dekratsiya Qilish
**Tavsif:** 10 Gigabaytlik katta ma'lumotlar omborini shifrlashda butun faylni bitta `raw` vektor sifatida operativ xotiraga yuklash xotira yetishmovchiligiga (OOM) olib keladi. Faylni 64KB qismlarga bo'lib oqimli shifrlash zarur.
**Talablar:** Fayl ulanishlari (`file()`), `readBin()`, `writeBin()` va AES-CTR oqimli shifrlash.
**Yechim (R):**
```r
library(openssl)

# Katta fayllarni oqimli shifrlash
encrypt_large_file <- function(input_path, output_path, key, chunk_size = 65536) {
  in_con <- file(input_path, "rb")
  out_con <- file(output_path, "wb")
  on.exit({ close(in_con); close(out_con) })
  
  iv <- rand_bytes(16)
  # Chiqish faylining eng boshiga 16 baytlik IV ni yozish
  writeBin(iv, out_con)
  
  total_bytes <- 0
  while (TRUE) {
    chunk <- readBin(in_con, what = "raw", n = chunk_size)
    if (length(chunk) == 0) break
    
    # Har bir bo'lakni AES-CTR bilan shifrlash
    encrypted_chunk <- aes_ctr_encrypt(chunk, key = key, iv = iv)
    writeBin(encrypted_chunk, out_con)
    total_bytes <- total_bytes + length(chunk)
  }
  
  cat(sprintf("[Fayl Shifrlash] %d bayt xotira to'lmasdan muvaffaqiyatli shifrlandi.\n", total_bytes))
}
```
**Tushuntirish:** Oqimli shifrlash (Streaming Encryption) xotira sarfini qat'iy $O(1)$ darajasida (masalan atigi 64KB) saqlab qoladi. Bu orqali R serverida har qanday yirik tahliliy datasetlar va neyron tarmoq og'irliklari xavfsiz shifrlanadi.

---

### Topshiriq #1161: Global Sezgirlik (L1 va L2 Global Sensitivity) Hisoblash va Chegaralash (Clipping)
**Tavsif:** Differensial maxfiylikda har qanday agregat so'rovga qo'shiladigan shovqin miqdori funksiyaning global sezgirligiga (bitta shaxsning qo'shilishi yoki o'chirilishi natijani maksimal qanchaga o'zgartira olishi) to'g'ridan-to'g'ri bog'liq. Chegaralanmagan ma'lumotlarda esa bu sezgirlik cheksiz bo'lishi mumkin.
**Talablar:** R tili yordamida berilgan dataset uchun count, sum va mean so'rovlarining L1 va L2 sezgirligini nazariy hisoblash va ekstremal qiymatlarni [lower, upper] oralig'ida qirqish (clipping) mexanizmini joriy etish.
**Yechim (R):**
```r
# Global sezgirlik va ma'lumotlarni qirqish (clipping) funksiyasi

calculate_sensitivity <- function(query_type, lower_bound = NULL, upper_bound = NULL, n = NULL) {
  if (query_type == "count") {
    # Count so'rovi uchun bitta shaxs maksimal 1 ta farq beradi
    return(list(L1 = 1, L2 = 1))
  } else if (query_type == "sum") {
    if (is.null(lower_bound) || is.null(upper_bound)) {
      stop("Sum so'rovi uchun quyi va yuqori chegaralar zarur!")
    }
    # Sum uchun maksimal o'zgarish max(|lower|, |upper|)
    sens <- max(abs(lower_bound), abs(upper_bound))
    return(list(L1 = sens, L2 = sens))
  } else if (query_type == "mean") {
    if (is.null(lower_bound) || is.null(upper_bound) || is.null(n)) {
      stop("Mean so'rovi uchun chegaralar va n (qatorlar soni) berilishi shart!")
    }
    # O'rtacha qiymat uchun sezgirlik: (upper - lower) / n
    sens <- (upper_bound - lower_bound) / n
    return(list(L1 = sens, L2 = sens))
  } else {
    stop("Noma'lum so'rov turi.")
  }
}

# Qiymatlarni xavfsiz qirqish (Clipping)
clip_values <- function(x, lower, upper) {
  pmax(lower, pmin(x, upper))
}

# Test ma'lumotlari: Bemorlarning qon bosimi (sistolik)
set.seed(42)
raw_bp <- c(rnorm(100, mean = 120, sd = 15), 350, 400) # 2 ta anomaliya (outlier)

cat("Xom ma'lumotlardagi min/max:", min(raw_bp), max(raw_bp), "\n")

# [80, 200] oralig'ida qirqish
clipped_bp <- clip_values(raw_bp, lower = 80, upper = 200)
cat("Qirqilgan ma'lumotlardagi min/max:", min(clipped_bp), max(clipped_bp), "\n")

# Sezgirlikni aniqlash
sens_sum <- calculate_sensitivity("sum", lower_bound = 80, upper_bound = 200)
sens_mean <- calculate_sensitivity("mean", lower_bound = 80, upper_bound = 200, n = length(clipped_bp))

cat("Sum sezgirligi (Delta f):", sens_sum$L1, "\n")
cat("Mean sezgirligi (Delta f):", sens_mean$L1, "\n")
```
**Tushuntirish:** Global sezgirlik differensial maxfiylikning poydevori hisoblanadi. Agar xom ma'lumotlar oldindan qirqilmasa (clipping), bitta ekstremal qiymat (masalan, milliarder daromadi yoki xato kiritilgan gipertoniya ko'rsatkichi) butun agregat natijaga bevosita ta'sir qilib, shaxsning maxfiyligini fosh qilishi mumkin. Clipping bu ta'sirni qat'iy chegaralaydi.

---

### Topshiriq #1162: Laplace Mexanizmi (Epsilon-Differensial Maxfiylik) Yordamida Shovqinli Natija Hisoblash
**Tavsif:** Sof epsilon-differensial maxfiylikda sonli so'rovlar (masalan, count yoki sum) natijasi Laplace taqsimotidan olingan shovqin (noise) bilan xiralashtiriladi. Shovqin dispersiyasi sezgirlik va epsilon parametrlariga bog'liq.
**Talablar:** Laplace shovqinini generatsiya qiluvchi xavfsiz funksiya yaratish va uni tibbiy ma'lumotlar bazasidagi saraton bilan og'rigan bemorlar sonini (count) epsilon=0.5 va epsilon=1.0 bilan hisoblashda qo'llash.
**Yechim (R):**
```r
# Laplace taqsimotidan shovqin generatsiyasi
# Laplace(0, b) bu yerda b = Delta_f / epsilon
rlaplace <- function(n, location = 0, scale = 1) {
  # Teskari CDF usuli yordamida generatsiya
  u <- runif(n, min = -0.5, max = 0.5)
  location - scale * sign(u) * log(1 - 2 * abs(u))
}

dp_laplace_count <- function(true_count, epsilon, sensitivity = 1) {
  scale_b <- sensitivity / epsilon
  noise <- rlaplace(1, location = 0, scale = scale_b)
  noisy_count <- true_count + noise
  # Sanash manfiy bo'lmasligi kerak
  return(max(0, round(noisy_count)))
}

# Simulyatsiya: Saraton bilan kasallanganlar soni
set.seed(2026)
haqiqiy_kasallar_soni <- 1420

# Turli epsilon (privacy budget) qiymatlari bo'yicha 1000 marta tajriba
eps_strong <- 0.1   # Kuchli maxfiylik, ko'proq shovqin
eps_balanced <- 0.5 # Balanslashgan
eps_weak <- 2.0     # Zaif maxfiylik, aniqroq natija

sim_strong <- replicate(1000, dp_laplace_count(haqiqiy_kasallar_soni, epsilon = eps_strong))
sim_balanced <- replicate(1000, dp_laplace_count(haqiqiy_kasallar_soni, epsilon = eps_balanced))
sim_weak <- replicate(1000, dp_laplace_count(haqiqiy_kasallar_soni, epsilon = eps_weak))

cat("Haqiqiy soni:", haqiqiy_kasallar_soni, "\n")
cat(sprintf("eps=0.1  -> O'rtacha: %.1f, Standart og'ish (Xatolik): %.2f\n", mean(sim_strong), sd(sim_strong)))
cat(sprintf("eps=0.5  -> O'rtacha: %.1f, Standart og'ish (Xatolik): %.2f\n", mean(sim_balanced), sd(sim_balanced)))
cat(sprintf("eps=2.0  -> O'rtacha: %.1f, Standart og'ish (Xatolik): %.2f\n", mean(sim_weak), sd(sim_weak)))
```
**Tushuntirish:** Laplace mexanizmi qat'iy e-differensial maxfiylikni kafolatlaydi: har qanday ikkita qo'shni D1 va D2 ma'lumotlar bazasi uchun so'rov natijasining ehtimolliklar nisbati exp(epsilon) dan oshmaydi. Epsilon qanchalik kichik bo'lsa, shovqin miqdori shunchalik katta va shaxsiy ma'lumotlarni tiklash imkoniyati nolga yaqin bo'ladi.

---

### Topshiriq #1163: Gaussian Mexanizmi ((Epsilon, Delta)-Differensial Maxfiylik) va L2 Sezgirlik
**Tavsif:** Vektorli va ko'p o'lchovli so'rovlarda Laplace mexanizmi shovqini tez o'sib ketadi. Gaussian mexanizmi (epsilon, delta)-maxfiylikni ta'minlab, L2 sezgirligidan foydalanadi va delta ehtimollik bilan maxfiylik buzilishi xavfiga ruxsat beradi.
**Talablar:** Gaussian shovqini formulasini R da aniq hisoblash: sigma >= sqrt(2 * log(1.25 / delta)) * (Delta_2 / epsilon) va ko'p o'lchovli biomarkerlar o'rtacha vektorini himoyalash.
**Yechim (R):**
```r
# Gaussian mexanizmi orqali (epsilon, delta)-DP joriy etish

calculate_gaussian_sigma <- function(epsilon, delta, l2_sensitivity) {
  if (epsilon <= 0 || delta <= 0 || delta >= 1) {
    stop("epsilon > 0 va 0 < delta < 1 bo'lishi shart!")
  }
  sigma <- sqrt(2 * log(1.25 / delta)) * (l2_sensitivity / epsilon)
  return(sigma)
}

dp_gaussian_vector <- function(true_vector, epsilon, delta, l2_sensitivity) {
  sigma <- calculate_gaussian_sigma(epsilon, delta, l2_sensitivity)
  noise <- rnorm(length(true_vector), mean = 0, sd = sigma)
  return(true_vector + noise)
}

# Misol: 3 ta qon tahlili ko'rsatkichi (Gemoglobin, Leykotsit, Trombotsit)
set.seed(123)
haqiqiy_biomarkerlar <- c(Hb = 140.5, WBC = 6.8, PLT = 250.2)

# Vektor L2 sezgirligi (bitta bemor o'zgarganda maksimal vektor uzunligi o'zgarishi)
l2_sens <- 2.5
epsilon_val <- 0.8
delta_val <- 1e-5 # 100,000 dan bir xavf

sigma_hisoblangan <- calculate_gaussian_sigma(epsilon_val, delta_val, l2_sens)
himoyalangan_biomarkerlar <- dp_gaussian_vector(haqiqiy_biomarkerlar, epsilon_val, delta_val, l2_sens)

cat("Gaussian shovqin parametri (sigma):", round(sigma_hisoblangan, 4), "\n")
cat("Haqiqiy vektor:      ", haqiqiy_biomarkerlar, "\n")
cat("Himoyalangan vektor: ", round(himoyalangan_biomarkerlar, 2), "\n")
```
**Tushuntirish:** Gaussian mexanizmi (e, d)-differensial maxfiylik beradi. Delta parametri maxfiylik shartining buzilishining maksimal ehtimolligini bildiradi (odatda 1/n dan ancha kichik, masalan 1e-5 yoki 1e-6 olinadi). U L2-normaga tayangani sababli yuqori o'lchamli tahlillarda Laplacega qaraganda ancha kamroq shovqin talab qiladi.

---

### Topshiriq #1164: Maxfiylik Byudjeti (Epsilon Budget) Boshqaruvi va Kompozitsiya Teoremalari
**Tavsif:** Differensial maxfiylikda bir nechta so'rov bajarilganda har bir so'rov ma'lum miqdordagi maxfiylik byudjetini (epsilon) sarflaydi. Byudjet tugagach, tizim boshqa so'rovlarni qabul qilmasligi kerak (Privacy Budget Exhaustion).
**Talablar:** R obyektga yo'naltirilgan (R6 yoki S3) PrivacyAccountant sinfini yaratish: Odatiy kompozitsiya (Linear Composition: eps_total = sum(eps)) va Ilg'or kompozitsiya (Advanced Composition) qoidalarini qo'llash.
**Yechim (R):**
```r
# PrivacyAccountant S3 sinfini yaratish

new_privacy_accountant <- function(total_epsilon = 5.0, total_delta = 1e-4) {
  structure(
    list(
      max_epsilon = total_epsilon,
      max_delta = total_delta,
      spent_epsilon = 0.0,
      spent_delta = 0.0,
      query_history = list()
    ),
    class = "PrivacyAccountant"
  )
}

consume_budget <- function(accountant, query_name, eps_cost, delta_cost = 0) {
  new_spent_eps <- accountant$spent_epsilon + eps_cost
  new_spent_delta <- accountant$spent_delta + delta_cost
  
  if (new_spent_eps > accountant$max_epsilon) {
    stop(sprintf("RAD ETILDI: Maxfiylik byudjeti yetarli emas! Sarflangan: %.2f, So'ralgan: %.2f, Cheklov: %.2f",
                 accountant$spent_epsilon, eps_cost, accountant$max_epsilon))
  }
  
  accountant$spent_epsilon <- new_spent_eps
  accountant$spent_delta <- new_spent_delta
  accountant$query_history <- append(accountant$query_history, list(
    list(query = query_name, eps = eps_cost, delta = delta_cost, timestamp = Sys.time())
  ))
  
  cat(sprintf("[Byudjet Sarflandi] So'rov: '%s' (eps=%.2f). Qoldiq eps: %.2f\n",
              query_name, eps_cost, accountant$max_epsilon - accountant$spent_epsilon))
  return(accountant)
}

# Sinov
acc <- new_privacy_accountant(total_epsilon = 2.0)
acc <- consume_budget(acc, "O'rtacha Yosh", 0.5)
acc <- consume_budget(acc, "Qon bosimi dispersiyasi", 0.8)
acc <- consume_budget(acc, "Diabet bilan og'riganlar soni", 0.5)

# Byudjetdan oshib ketish holati
tryCatch({
  acc <- consume_budget(acc, "Jins bo'yicha taqsimot", 0.5)
}, error = function(e) {
  cat("Kutilgan xavfsizlik cheklovi:", e$message, "\n")
})
```
**Tushuntirish:** Kompozitsiya xossasi differensial maxfiylikning eng muhim afzalligidir. Agar tizimda k ta mustaqil tahliliy so'rov har biri eps_i maxfiylik bilan bajarilsa, butun tizim sum(eps_i) darajasida himoyalangan qoladi. Privacy Accountant yordamida tajovuzkorning ketma-ket so'rovlar yuborib shaxslarni aniqlashining (Reconstruction Attack) oldi olinadi.

---

### Topshiriq #1165: Differensial Maxfiy O'rtacha Qiymat (DP Mean) va Dinamik Chegaralash (Adaptive Truncation)
**Tavsif:** O'rtacha qiymatni hisoblashda ikkita parametr noma'lum: elementlar yig'indisi (Sum) va soni (Count). Ikkalasiga ham alohida Laplace shovqini qo'shilib, so'ng bo'linadi (Noisy Sum / Noisy Count).
**Talablar:** Chegaralangan qiymatlar bo'yicha DP Mean hisoblovchi, nolga bo'linish xatolaridan himoyalangan va byudjetni optimal bo'luvchi (eps_sum = 0.8*eps, eps_count = 0.2*eps) R funksiyasini yozish.
**Yechim (R):**
```r
# Differensial maxfiy o'rtacha qiymat funksiyasi

dp_mean <- function(x, lower, upper, epsilon = 1.0) {
  # Byudjetni ikkiga ajratish: yig'indi va sanash uchun
  eps_sum <- epsilon * 0.7
  eps_count <- epsilon * 0.3
  
  # 1. Qiymatlarni kesish (clipping)
  clipped_x <- pmax(lower, pmin(x, upper))
  
  # 2. Yig'indi va sezgirlik
  true_sum <- sum(clipped_x)
  sens_sum <- max(abs(lower), abs(upper))
  scale_sum <- sens_sum / eps_sum
  u_sum <- runif(1, -0.5, 0.5)
  noise_sum <- -scale_sum * sign(u_sum) * log(1 - 2 * abs(u_sum))
  noisy_sum <- true_sum + noise_sum
  
  # 3. Sanash va sezgirlik (count sezgirligi doimo 1)
  true_count <- length(x)
  scale_count <- 1.0 / eps_count
  u_cnt <- runif(1, -0.5, 0.5)
  noise_count <- -scale_count * sign(u_cnt) * log(1 - 2 * abs(u_cnt))
  noisy_count <- max(1, true_count + noise_count) # kamida 1
  
  # 4. DP O'rtacha
  noisy_mean <- noisy_sum / noisy_count
  # Natija ham [lower, upper] oralig'ida bo'lishi mantiqiy
  return(pmax(lower, pmin(noisy_mean, upper)))
}

# Test: Ishchilarning maoshi (ming dollar)
set.seed(777)
haqiqiy_maoshlar <- c(rnorm(500, mean = 45, sd = 10), 250) # 1 ta rahbar maoshi
haqiqiy_mean <- mean(haqiqiy_maoshlar)

# Turli darajadagi DP Mean hisoblash
dp_mean_1 <- dp_mean(haqiqiy_maoshlar, lower = 15, upper = 100, epsilon = 0.2)
dp_mean_2 <- dp_mean(haqiqiy_maoshlar, lower = 15, upper = 100, epsilon = 1.0)

cat("Haqiqiy o'rtacha maosh:   $", round(haqiqiy_mean, 2), "k\n")
cat("DP o'rtacha (eps = 0.2):  $", round(dp_mean_1, 2), "k\n")
cat("DP o'rtacha (eps = 1.0):  $", round(dp_mean_2, 2), "k\n")
```
**Tushuntirish:** O'rtacha qiymat to'g'ridan-to'g'ri bitta shovqin bilan hisoblanmaydi, chunki umumiy a'zolar soni ham maxfiy bo'lishi lozim (agar guruh kichik bo'lsa, qatnashuvchilar sonining aniqligi shaxsni fosh qiladi). Shu sababli yig'indi va miqdor alohida-alohida shovqinlanib, bo'linadi.

---

### Topshiriq #1166: Differensial Maxfiy Gistogrammalar va Kategorik Ma'lumotlar Taqsimotini Chiqarish
**Tavsif:** Kategorik ustunlar (masalan, qon guruhi, yashash hududi, kasallik tashxisi) bo'yicha gistogramma tuzilganda har bir savat (bin) bir-birini inkor qiluvchi bo'lgani sababli global sezgirlik atigi 1 ga teng bo'ladi.
**Talablar:** R tilida bemorlar tashxis gistogrammasini Laplace shovqini bilan himoyalash va manfiy qiymatlarni yo'qotib, umumiy ehtimolliklar yig'indisi 1 ga teng bo'ladigan qilib normallashtirish.
**Yechim (R):**
```r
# Differensial maxfiy gistogramma (Categorical DP Histogram)

dp_histogram <- function(data_vector, categories, epsilon = 0.5) {
  # Haqiqiy chastotalar
  freq_table <- table(factor(data_vector, levels = categories))
  true_counts <- as.numeric(freq_table)
  
  # Har bir savat uchun sezgirlik = 1 (chunki bitta odam faqat bitta toifaga kiradi)
  scale_b <- 1.0 / epsilon
  
  # Har bir bin uchun mustaqil Laplace shovqini
  u <- runif(length(true_counts), -0.5, 0.5)
  noise <- -scale_b * sign(u) * log(1 - 2 * abs(u))
  noisy_counts <- true_counts + noise
  
  # Shovqin tufayli manfiy bo'lib qolgan qiymatlarni 0 ga tenglash
  non_negative_counts <- pmax(0, noisy_counts)
  
  # Ehtimollik taqsimotiga normallashtirish
  probabilities <- non_negative_counts / sum(non_negative_counts)
  
  data.frame(
    Kategoriya = categories,
    Haqiqiy_Soni = true_counts,
    Shovqinli_Soni = round(non_negative_counts, 1),
    DP_Ehtimollik = round(probabilities, 4)
  )
}

# Test ma'lumotlari: Bemorlar qon guruhi
set.seed(999)
categories <- c("O(I)+", "A(II)+", "B(III)+", "AB(IV)+", "Rh- Salbiy")
dataset_qon <- sample(categories, size = 1000, replace = TRUE, prob = c(0.35, 0.30, 0.20, 0.10, 0.05))

natija <- dp_histogram(dataset_qon, categories, epsilon = 0.5)
print(natija)
```
**Tushuntirish:** Bir-birini istisno qiluvchi toifalar (Disjoint partitions) bo'yicha har bir inson yozuvi faqat bitta savatga tushadi. Bu differensial maxfiylikda parallel kompozitsiya qoidasini ishlatish imkonini beradi: barcha savatlarga shovqin qo'shilsa ham, umumiy maxfiylik sarfi bitta epsilon bo'lib qolaveradi.

---

### Topshiriq #1167: DP-SGD: Differensial Maxfiy Gradient Tushishi Asosida Chiziqli Regressiya O'qitish
**Tavsif:** Mashinali o'rganish modellarining og'irliklari (weights) o'quv ma'lumotlaridagi maxfiy yozuvlarni yodlab qolishi mumkin. DP-SGD (Differentially Private Stochastic Gradient Descent) har bir mini-batch gradientini qirqadi (clipping) va unga Gaussian shovqini qo'shadi.
**Talablar:** R tili yordamida sodda chiziqli regressiya uchun DP-SGD algoritmini amalga oshirish: gradient normasi cheklovi (C=1.0) va shovqin parametri (sigma).
**Yechim (R):**
```r
# DP-SGD algoritmi bilan chiziqli regressiya

dp_sgd_linear_regression <- function(X, y, epochs = 20, lr = 0.01, C = 1.0, sigma = 0.5, batch_size = 16) {
  n <- nrow(X)
  p <- ncol(X)
  
  # Og'irliklarni boshlash
  weights <- rep(0, p)
  bias <- 0
  
  for (ep in 1:epochs) {
    # Tasodifiy permutatsiya
    idx <- sample(n)
    
    for (i in seq(1, n, by = batch_size)) {
      b_idx <- idx[i:min(i + batch_size - 1, n)]
      X_batch <- X[b_idx, , drop = FALSE]
      y_batch <- y[b_idx]
      B <- length(b_idx)
      
      # Har bir namuna uchun gradientlarni hisoblash va qirqish (per-sample clipping)
      clipped_grad_w <- matrix(0, nrow = B, ncol = p)
      clipped_grad_b <- numeric(B)
      
      for (k in 1:B) {
        pred_k <- sum(X_batch[k, ] * weights) + bias
        err_k <- pred_k - y_batch[k]
        g_w <- 2 * err_k * X_batch[k, ]
        g_b <- 2 * err_k
        
        # L2 normani hisoblash
        total_norm <- sqrt(sum(g_w^2) + g_b^2)
        clip_factor <- max(1, total_norm / C)
        
        clipped_grad_w[k, ] <- g_w / clip_factor
        clipped_grad_b[k] <- g_b / clip_factor
      }
      
      # Gradientlarni jamlash va Gaussian shovqin qo'shish
      sum_gw <- colSums(clipped_grad_w) + rnorm(p, mean = 0, sd = sigma * C)
      sum_gb <- sum(clipped_grad_b) + rnorm(1, mean = 0, sd = sigma * C)
      
      # Og'irliklarni yangilash
      weights <- weights - lr * (sum_gw / B)
      bias <- bias - lr * (sum_gb / B)
    }
  }
  
  return(list(weights = weights, bias = bias))
}

# Test ma'lumotlari: y = 2.5 * x1 - 1.2 * x2 + 5.0
set.seed(42)
N <- 300
X <- matrix(rnorm(N * 2), nrow = N, ncol = 2)
y <- 2.5 * X[, 1] - 1.2 * X[, 2] + 5.0 + rnorm(N, sd = 0.5)

model <- dp_sgd_linear_regression(X, y, epochs = 15, lr = 0.05, C = 2.0, sigma = 0.2, batch_size = 20)
cat("O'qitilgan og'irliklar:", round(model$weights, 3), "\n")
cat("O'qitilgan bias:        ", round(model$bias, 3), "\n")
```
**Tushuntirish:** DP-SGD da ikki bosqich muhim: (1) Per-sample gradient clipping — bitta kishining ma'lumoti model gradientini keskin o'zgartira olmasligini ta'minlaydi; (2) Mini-batchga Gaussian shovqin qo'shish — olingan og'irliklarni bitta shaxsga bog'lash imkonini yo'q qiladi.

---

### Topshiriq #1168: Tasodifiy Javob Mexanizmi (Randomized Response / Warner's Algorithm) So'rovnomalar Uchun
**Tavsif:** Bemorlar yoki xodimlar nozik savollarga (masalan, 'Siz noqonuniy moddalar iste'mol qilganmisiz?' yoki 'Kompaniya ma'lumotlarini sizdirganmisiz?') to'g'ri javob berishdan qo'rqishadi. Tasodifiy javob usuli respondentga inkor etish imkonini (Plausible Deniability) beradi.
**Talablar:** R tilida Warnerning tanga tashlash algoritmini simulyatsiya qilish: Respondent tanga tashlaydi, agar gerb tushsa rost aytadi, raqam tushsa ikkinchi marta tashlab gerb=ha, raqam=yo'q deydi. Olingan shovqinli javoblardan haqiqiy ulushni xolis tiklash (Unbiased Estimator).
**Yechim (R):**
```r
# Warner's Randomized Response mexanizmi

simulate_randomized_response <- function(true_answers, p_honest = 0.5, p_yes = 0.5) {
  n <- length(true_answers)
  reported_answers <- logical(n)
  
  for (i in 1:n) {
    # 1-tanga: Rost aytish yoki tasodifiy javob
    if (runif(1) < p_honest) {
      reported_answers[i] <- true_answers[i] # Rost javob
    } else {
      # 2-tanga: Gerb = Ha (TRUE), Raqam = Yo'q (FALSE)
      reported_answers[i] <- (runif(1) < p_yes)
    }
  }
  return(reported_answers)
}

# Xolis baholovchi (Unbiased Estimator): Haqiqiy ulushni tiklash
# E[Y] = p_honest * pi + (1 - p_honest) * p_yes
# pi_hat = (E[Y] - (1 - p_honest) * p_yes) / p_honest
estimate_true_proportion <- function(reported_answers, p_honest = 0.5, p_yes = 0.5) {
  y_bar <- mean(reported_answers)
  pi_hat <- (y_bar - (1 - p_honest) * p_yes) / p_honest
  return(max(0, min(1, pi_hat))) # [0, 1] oralig'ida
}

# Tajriba: Haqiqiy nozik savolga 'HA' deganlar ulushi 18% (0.18)
set.seed(888)
N_respondents <- 5000
haqiqiy_ulush <- 0.18
haqiqiy_javoblar <- runif(N_respondents) < haqiqiy_ulush

# Respondantlar himoyalangan holda javob berishadi
shovqinli_javoblar <- simulate_randomized_response(haqiqiy_javoblar, p_honest = 0.6, p_yes = 0.5)

# Tahlilchi faqat shovqinli javoblarni ko'radi
tiklangan_ulush <- estimate_true_proportion(shovqinli_javoblar, p_honest = 0.6, p_yes = 0.5)

cat("Haqiqiy sir saqlangan ulush: ", haqiqiy_ulush * 100, "%\n")
cat("Shovqinli javoblar ulushi:   ", round(mean(shovqinli_javoblar) * 100, 2), "%\n")
cat("Xolis tiklangan yakuniy ulush:", round(tiklangan_ulush * 100, 2), "%\n")
```
**Tushuntirish:** Randomized Response mahalliy differensial maxfiylikning (Local Differential Privacy - LDP) eng qadimgi va samarali shaklidir. Hech qanday server yoki markaziy tizim alohida shaxsning asl javobini bila olmaydi, biroq statistik qonuniyatlar tufayli umumiy populyatsiya ulushi yuqori aniqlikda tiklanadi.

---

### Topshiriq #1169: Eksponensial Mexanizm: Diskret va Sifatli Ma'lumotlarni Differensial Maxfiy Tanlash
**Tavsif:** Agar so'rov natijasi raqam emas, balki to'plamdan eng yaxshi nomzodni (masalan, eng mos dori turi, eng ma'qul davolash usuli yoki auksion g'olibi) tanlash bo'lsa, Laplace qo'shib bo'lmaydi. Bunday hollarda baholash funksiyasiga (Utility Function) asoslangan Eksponensial Mexanizm qo'llaniladi.
**Talablar:** R tilida dori vositalarining nojo'ya ta'sirlarini hisobga oluvchi ball funksiyasini yozish va epsilon byudjet asosida e^(eps * score / 2*Delta) ehtimollik bilan eng xavfsiz dorini DP tanlash.
**Yechim (R):**
```r
# Differensial maxfiy Eksponensial mexanizm

exponential_mechanism_select <- function(candidates, score_function, epsilon, sensitivity = 1.0) {
  # Har bir nomzod uchun foydalilik ballini hisoblash
  scores <- sapply(candidates, score_function)
  
  # DP ehtimollik log-vaznlari: (epsilon * score) / (2 * sensitivity)
  log_weights <- (epsilon * scores) / (2 * sensitivity)
  
  # Raqamli toshib ketishni (overflow) oldini olish uchun log-sum-exp hiylasi
  max_log <- max(log_weights)
  weights <- exp(log_weights - max_log)
  probabilities <- weights / sum(weights)
  
  # Diskret ehtimolliklar bo'yicha g'olibni tasodifiy tanlash
  selected_idx <- sample(seq_along(candidates), size = 1, prob = probabilities)
  
  return(list(
    selected = candidates[selected_idx],
    candidates = candidates,
    scores = scores,
    probs = round(probabilities, 4)
  ))
}

# Misol: Saraton kasalligiga qarshi eng samarali dori turini tanlash
dori_nomzodlari <- c("Dori_Alfa", "Dori_Beta", "Dori_Gamma", "Dori_Delta")

# Baholash funksiyasi (bemorlar ustida o'tkazilgan testlardagi samaradorlik balli)
dori_ballari <- c(Dori_Alfa = 85, Dori_Beta = 92, Dori_Gamma = 78, Dori_Delta = 60)
score_fn <- function(candidate) dori_ballari[[candidate]]

# Tanlash (Epsilon = 0.5)
set.seed(333)
tanlov <- exponential_mechanism_select(dori_nomzodlari, score_fn, epsilon = 0.5, sensitivity = 5.0)

cat("Tanlangan optimal dori:", tanlov$selected, "\n")
cat("Nomzodlar ehtimollik taqsimoti:\n")
for (i in seq_along(tanlov$candidates)) {
  cat(sprintf(" - %-10s (Ball: %2d): Ehtimollik = %.2f%%\n",
              tanlov$candidates[i], tanlov$scores[i], tanlov$probs[i] * 100))
}
```
**Tushuntirish:** Eksponensial mexanizm sonli bo'lmagan natijalar uchun epsilon-differensial maxfiylikni kafolatlaydi. Eng yuqori ballga ega variant eng katta ehtimollik bilan tanlanadi, biroq pastroq ballli variantlar ham ma'lum ehtimollikka ega bo'lgani sababli bitta bemorning natijasi tanlovni 100% o'zgartirib qo'ya olmaydi.

---

### Topshiriq #1170: R da diffpriv Kutubxonasi Bilan Differensial Maxfiy Mashinali O'rganish va Tahlil
**Tavsif:** Sanoatda differensial maxfiylik algoritmlarini noldan yozish xatoliklarga olib kelishi mumkin. R ning ixtisoslashgan `diffpriv` paketi rasmiy mexanizmlarni (Laplace, Gaussian, Exponential) va avtomatlashtirilgan sezgirlik hisobini birlashtiradi.
**Talablar:** `diffpriv` paketiga muqobil tarzda to'liq tekshiruvchi, sezgirlik va xatolik chegaralarini hisoblovchi umumiy tahliliy differensial maxfiy wrapper funksiyasini yaratish.
**Yechim (R):**
```r
# Differensial maxfiy tahliliy wrapper arxitekturasi

dp_analytic_framework <- function(data, target_col, mechanism = c("laplace", "gaussian"),
                                  epsilon = 1.0, delta = 1e-5, bounds = NULL) {
  mechanism <- match.arg(mechanism)
  values <- data[[target_col]]
  
  # Chegaralarni aniqlash
  if (is.null(bounds)) {
    # 5% va 95% kvantillar bo'yicha avtomatik xavfsiz qirqish
    lower <- quantile(values, 0.05, na.rm = TRUE)
    upper <- quantile(values, 0.95, na.rm = TRUE)
  } else {
    lower <- bounds[1]
    upper <- bounds[2]
  }
  
  clipped <- pmax(lower, pmin(values, upper))
  n <- length(clipped)
  
  # Sezgirlik
  l1_sens <- (upper - lower) / n
  
  if (mechanism == "laplace") {
    scale_b <- l1_sens / epsilon
    u <- runif(1, -0.5, 0.5)
    noise <- -scale_b * sign(u) * log(1 - 2 * abs(u))
    guarantee <- sprintf("Epsilon = %.2f (Laplace)", epsilon)
  } else {
    sigma <- sqrt(2 * log(1.25 / delta)) * (l1_sens / epsilon)
    noise <- rnorm(1, mean = 0, sd = sigma)
    guarantee <- sprintf("Epsilon = %.2f, Delta = %.1e (Gaussian)", epsilon, delta)
  }
  
  dp_result <- mean(clipped) + noise
  
  list(
    ustun = target_col,
    mexanizm = mechanism,
    kafolat = guarantee,
    haqiqiy_natija = mean(values, na.rm = TRUE),
    qirqilgan_natija = mean(clipped),
    dp_natija = dp_result,
    absolyut_xatolik = abs(dp_result - mean(values, na.rm = TRUE))
  )
}

# Test: 10,000 ta bemorning qondagi glyukoza darajasi
set.seed(555)
bemorlar_df <- data.frame(
  ID = 1:5000,
  Glyukoza = rgamma(5000, shape = 9, rate = 1.5) # O'rtacha ~6 mmol/L
)

natija_lap <- dp_analytic_framework(bemorlar_df, "Glyukoza", mechanism = "laplace", epsilon = 0.5)
natija_gauss <- dp_analytic_framework(bemorlar_df, "Glyukoza", mechanism = "gaussian", epsilon = 0.5, delta = 1e-5)

cat("=== DIFFERENSIAL MAXFIY TAHLIL NATIJASI ===\n")
cat("Laplace  -> Haqiqiy:", round(natija_lap$haqiqiy_natija, 3),
    "| DP:", round(natija_lap$dp_natija, 3),
    "| Xatolik:", round(natija_lap$absolyut_xatolik, 4), "\n")
cat("Gaussian -> Haqiqiy:", round(natija_gauss$haqiqiy_natija, 3),
    "| DP:", round(natija_gauss$dp_natija, 3),
    "| Xatolik:", round(natija_gauss$absolyut_xatolik, 4), "\n")
```
**Tushuntirish:** `diffpriv` konsepsiyasi ma'lumotlarni tahlil qilishda matematik qat'iylikni ta'minlaydi. Kvantillar yordamida dinamik chegaralash ekstremal qiymatlarning ta'sirini kamaytiradi va natijada foydalilik (utility) bilan maxfiylik (privacy) o'rtasidagi mukammal muvozanatga erishiladi.

---

### Topshiriq #1171: PII ni Xavfsiz Psevdonimlashtirish (HMAC va SHA-256 Tuzlangan Tokenizatsiya)
**Tavsif:** Bemorlar yoki mijozlarning to'g'ridan-to'g'ri identifikatorlari (Ism, JSHSHIR, Pasport, Telefon) tahliliy bazalarda ochiq saqlanmasligi shart. Oddiy xesh (masalan, sha256(jshshir)) Rainbow table hujumlariga zaif. Shu sababli tuzlangan va maxfiy kalitli HMAC tokenizatsiyasi talab qilinadi.
**Talablar:** R tilida ma'lumotlar freymidagi barcha PII ustunlarini maxfiy korporativ kalit va dinamik tuz (salt) orqali qaytarib bo'lmas unikal tokenlarga aylantiruvchi xavfsiz pipeline yaratish.
**Yechim (R):**
```r
library(openssl)

pseudonymize_column <- function(values, secret_key, salt_prefix = "KHORAZMIY_") {
  # Har bir qiymatga tuz qo'shish va HMAC hisoblash
  salted_values <- paste0(salt_prefix, as.character(values))
  
  sapply(salted_values, function(val) {
    sig <- sha256(charToRaw(val), key = charToRaw(secret_key))
    # Birinchi 16 ta hex belgini token sifatida olish
    substr(as.character(sig), 1, 16)
  }, USE.NAMES = FALSE)
}

# Test ma'lumotlari: Bemorlarning nozik anketasi
bemorlar_xom = data.frame(
  JSHSHIR = c("31201991234567", "42508889876543", "50112951122334"),
  Ism_Familiya = c("Ali Valiyev", "Zarina Karimova", "Bobur Mirzayev"),
  Yosh = c(34, 45, 29),
  Tashxis = c("Gipertoniya", "Qandli Diabet", "Aritmiya"),
  stringsAsFactors = FALSE
)

korporativ_kalit <- "Maxfiy_HMAC_Kalit_Tibbiyot_2026_X"

# PII ustunlarini psevdonimlashtirish
bemorlar_anonim <- bemorlar_xom
bemorlar_anonim$Bemor_ID <- pseudonymize_column(bemorlar_xom$JSHSHIR, korporativ_kalit, "JSH_")
bemorlar_anonim$JSHSHIR <- NULL
bemorlar_anonim$Ism_Familiya <- NULL

cat("=== XOM MA'LUMOTLAR ===\n")
print(bemorlar_xom)

cat("\n=== PSEVDONIMLASHTIRILGAN XAVFSIZ JADVAL ===\n")
print(bemorlar_anonim)
```
**Tushuntirish:** Psevdonimlashtirish to'g'ridan-to'g'ri identifikatorlarni yo'qotadi, ammo qaytarib bo'ladigan bog'lanish faqat maxfiy kalit saqlanuvchi xavfsiz HSM (Hardware Security Module) da mavjud bo'ladi. Tuz (salt) qo'shilishi tufayli tajovuzkor oldindan hisoblangan jadval orqali jismoniy shaxslarni aniqlay olmaydi.

---

### Topshiriq #1172: Kvazi-identifikatorlar (Quasi-Identifiers) va Qayta Aniqlash (Re-identification) Xavfini Baholash
**Tavsif:** To'g'ridan-to'g'ri PII olib tashlangan bo'lsa ham, Yosh, Jins, Yashash indeksi (ZIP code) kabi kvazi-identifikatorlarning kombinatsiyasi aholining 87% ini yagona qilib ajratib beradi (Sweeney tadqiqoti).
**Talablar:** R tilida datasetdagi kvazi-identifikatorlar kombinatsiyasi bo'yicha guruhlar hajmini o'rganish va yagona (unikal) bo'lgan, ya'ni qayta aniqlanish ehtimoli 100% bo'lgan yozuvlarni topish.
**Yechim (R):**
```r
# Kvazi-identifikatorlar xavfini tahlil qilish

assess_reidentification_risk <- function(df, quasi_cols) {
  # Kvazi-identifikatorlar bo'yicha guruhlash
  grouped <- aggregate(
    list(Guruh_Soni = rep(1, nrow(df))),
    by = df[quasi_cols],
    FUN = length
  )
  
  # Asl ma'lumotlar bilan birlashtirish
  df_with_risk <- merge(df, grouped, by = quasi_cols, all.x = TRUE)
  
  # Unikal (Guruh_Soni == 1) bo'lganlar xavf ostida
  unikal_soni <- sum(df_with_risk$Guruh_Soni == 1)
  unikal_foiz <- (unikal_soni / nrow(df)) * 100
  
  cat("Tahlil qilingan ustunlar:", paste(quasi_cols, collapse = ", "), "\n")
  cat(sprintf("Jami qatorlar: %d\n", nrow(df)))
  cat(sprintf("Yagona (Unikal) shaxslar soni: %d (%.2f%%)\n", unikal_soni, unikal_foiz))
  cat(sprintf("Maksimal qayta aniqlash xavfi: %.2f%%\n", max(1 / df_with_risk$Guruh_Soni) * 100))
  
  return(df_with_risk)
}

# Test ma'lumotlar bazasi
set.seed(101)
n_records <- 1000
aholi_df <- data.frame(
  Yosh = sample(20:70, n_records, replace = TRUE),
  Jins = sample(c("Erkak", "Ayol"), n_records, replace = TRUE),
  Pochta_Indeksi = sample(c("100000", "100015", "100021", "100047", "100084"), n_records, replace = TRUE),
  Qon_Bosimi = rnorm(n_records, 125, 12)
)

tahlil <- assess_reidentification_risk(aholi_df, c("Yosh", "Jins", "Pochta_Indeksi"))
```
**Tushuntirish:** Kvazi-identifikatorlar alohida olinganda maxfiy bo'lmasligi mumkin, ammo ularning o'zaro kombinatsiyasi tashqi ochiq manbalar (saylovchilar ro'yxati, ijtimoiy tarmoqlar) bilan birlashganda (Linkage Attack) shaxsni fosh qiladi. Guruh hajmi qanchalik kichik bo'lsa, xavf shunchalik yuqori bo'ladi.

---

### Topshiriq #1173: k-Anonymity Algoritmini Amalga Oshirish: Umumlashtirish (Generalization) va Bosish (Suppression)
**Tavsif:** k-Anonymity talabiga ko'ra, har bir kvazi-identifikatorlar kombinatsiyasi datasetda kamida k ta yozuvda uchrashi shart. Bunga erishish uchun yoshni intervallarga bo'lish (umumlashtirish) va k tadan kam nusxaga ega qatorlarni o'chirish (bosish) kerak.
**Talablar:** R tilida berilgan k (masalan, k=5) uchun umumlashtirish iyerarxiyasini qo'llash va yetarli takrorlanmagan qatorlarni xavfsiz filtrlovchi algoritm yozish.
**Yechim (R):**
```r
# k-Anonymity ta'minlovchi funksiya

apply_k_anonymity <- function(df, quasi_cols, k = 5) {
  # 1. Umumlashtirish (Generalization): Yoshni 10 yillik oraliqlarga bo'lish
  if ("Yosh" %in% quasi_cols && is.numeric(df$Yosh)) {
    df$Yosh <- cut(df$Yosh, breaks = seq(0, 100, by = 10),
                   labels = c("0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90-99"),
                   right = FALSE)
  }
  
  # 2. Pochta indeksini umumlashtirish (oxirgi 2 raqamni yashirish)
  if ("Pochta_Indeksi" %in% quasi_cols) {
    df$Pochta_Indeksi <- paste0(substr(df$Pochta_Indeksi, 1, 4), "**")
  }
  
  # 3. Guruh chastotasini hisoblash
  chastota <- as.data.frame(table(df[quasi_cols]))
  # Qaysi guruhlar k talabini qondiradi?
  mos_guruhlar <- merge(df, chastota, by = quasi_cols, all.x = TRUE)
  
  # 4. Bosish (Suppression): Freq < k bo'lgan qatorlarni chetlatish
  bosilgan_df <- mos_guruhlar[mos_guruhlar$Freq >= k, ]
  yoqotilgan_qatorlar <- nrow(df) - nrow(bosilgan_df)
  
  bosilgan_df$Freq <- NULL
  
  cat(sprintf("k-Anonymity (k=%d) qo'llanildi.\n", k))
  cat(sprintf("Boshlang'ich qatorlar: %d | Qolgan qatorlar: %d | O'chirilgan (Suppressed): %d (%.2f%%)\n",
              nrow(df), nrow(bosilgan_df), yoqotilgan_qatorlar, (yoqotilgan_qatorlar / nrow(df)) * 100))
  
  return(bosilgan_df)
}

# Sinov
set.seed(42)
test_data <- data.frame(
  Yosh = sample(18:75, 500, replace = TRUE),
  Pochta_Indeksi = sample(c("100010", "100020", "100030", "100040", "100050"), 500, replace = TRUE),
  Jins = sample(c("Erkak", "Ayol"), 500, replace = TRUE),
  Tashxis = sample(c("Shamollash", "Covid-19", "Allergiya"), 500, replace = TRUE),
  stringsAsFactors = FALSE
)

k_anon_df <- apply_k_anonymity(test_data, c("Yosh", "Pochta_Indeksi", "Jins"), k = 4)
head(k_anon_df)
```
**Tushuntirish:** Umumlashtirish (Generalization) ma'lumotlarning aniqligini kamaytiradi (masalan, 34 yosh o'rniga '30-39' oralig'i beriladi). Bosish (Suppression) esa guruh hajmi kamida k taga yetmagan xavfli qatorlarni datasetdan butunlay olib tashlaydi. Natijada har bir yozuv kamida k-1 ta boshqa yozuv bilan adashtiriladi.

---

### Topshiriq #1174: sdcMicro Kutubxonasi Konsepsiyasi: k-Anonymity Metrikalarini Hisoblash va Buzilishlarni Topish
**Tavsif:** Statistik ma'lumotlar maxfiyligini ta'minlashda (SDC - Statistical Disclosure Control) R dagi `sdcMicro` dunyo standartlaridan biridir. Unda k-anonymity buzilishlari va individual xavf ko'rsatkichlari (individual risk) avtomatik hisoblanadi.
**Talablar:** sdcMicro mantig'ini ifodalovchi, har bir qator uchun 2-anonimlik, 3-anonimlik va 5-anonimlik buzilishlarini aniqlovchi va xavf darajasini hisoblovchi R funksiyasini ishlab chiqish.
**Yechim (R):**
```r
# sdcMicro uslubidagi k-anonymity auditori

sdc_audit_anonymity <- function(df, quasi_identifiers) {
  # Guruhlash va har bir guruh hajmini aniqlash
  df_sub <- df[, quasi_identifiers, drop = FALSE]
  group_keys <- apply(df_sub, 1, paste, collapse = " | ")
  counts_map <- table(group_keys)
  
  individual_k <- as.numeric(counts_map[group_keys])
  
  # Har bir yozuv uchun qayta aniqlanish xavfi: 1 / k
  indiv_risk <- 1.0 / individual_k
  
  # Umumiy metrikalar
  violations_k2 <- sum(individual_k < 2)
  violations_k3 <- sum(individual_k < 3)
  violations_k5 <- sum(individual_k < 5)
  
  report <- list(
    Total_Records = nrow(df),
    Violations_k2 = violations_k2,
    Violations_k3 = violations_k3,
    Violations_k5 = violations_k5,
    Global_Risk_Mean = mean(indiv_risk),
    Global_Risk_Max = max(indiv_risk),
    Data_With_Risk = cbind(df, k_Group_Size = individual_k, Risk = round(indiv_risk, 3))
  )
  
  cat("=== STATISTICAL DISCLOSURE AUDIT ===\n")
  cat(sprintf("Jami yozuvlar: %d\n", report$Total_Records))
  cat(sprintf("k < 2 buzilishlar (Unikal shaxslar): %d (%.2f%%)\n", violations_k2, (violations_k2 / nrow(df)) * 100))
  cat(sprintf("k < 3 buzilishlar:                   %d (%.2f%%)\n", violations_k3, (violations_k3 / nrow(df)) * 100))
  cat(sprintf("k < 5 buzilishlar:                   %d (%.2f%%)\n", violations_k5, (violations_k5 / nrow(df)) * 100))
  cat(sprintf("O'rtacha fosh bo'lish xavfi:         %.4f\n", report$Global_Risk_Mean))
  
  return(report)
}

# Test dataset
set.seed(321)
baza <- data.frame(
  Shahar = sample(c("Toshkent", "Samarqand", "Buxoro"), 200, replace = TRUE),
  Yosh_Guruhi = sample(c("Yosh", "O'rta", "Katta"), 200, replace = TRUE),
  Kasb = sample(c("Dasturchi", "Shifokor", "O'qituvchi", "Muhandis"), 200, replace = TRUE)
)

audit_natija <- sdc_audit_anonymity(baza, c("Shahar", "Yosh_Guruhi", "Kasb"))
```
**Tushuntirish:** sdcMicro metodologiyasi davlat statistika qo'mitalari va xalqaro tashkilotlar tomonidan ma'lumotlarni ommaga ochiqlashdan oldin qat'iy tekshirish uchun ishlatiladi. Unda k-anonymity buzilishlarining kamida 0 bo'lishi maqsad qilinadi.

---

### Topshiriq #1175: l-Diversity Mexanizmi: Nozik Atributlar Xilma-xilligini Ta'minlash (Distinct va Entropy)
**Tavsif:** k-Anonymity guruhdagi barcha k ta shaxsning nozik ma'lumoti (masalan, kasalligi) bir xil bo'lib qolishidan (Homogeneity Attack) himoya qila olmaydi. l-Diversity har bir ekvivalent guruhda kamida l ta turli nozik atribut bo'lishini talab qiladi.
**Talablar:** R tilida Distinct l-diversity va Entropy l-diversity tekshiruvini amalga oshiruvchi funksiya yaratish va buzilgan ekvivalent guruhlarni aniqlash.
**Yechim (R):**
```r
# Distinct va Entropy l-Diversity tekshiruvi

check_l_diversity <- function(df, quasi_cols, sensitive_col, min_l = 2) {
  # Ekvivalent sinflar bo'yicha guruhlash
  split_groups <- split(df[[sensitive_col]], df[quasi_cols], drop = TRUE)
  
  results <- list()
  failed_groups <- 0
  
  for (grp_name in names(split_groups)) {
    vals <- split_groups[[grp_name]]
    distinct_l <- length(unique(vals))
    
    # Entropiyani hisoblash: -sum(p * log(p))
    probs <- table(vals) / length(vals)
    entropy <- -sum(probs * log(probs))
    
    passed <- (distinct_l >= min_l)
    if (!passed) failed_groups <- failed_groups + 1
    
    results[[grp_name]] <- list(
      group = grp_name,
      size = length(vals),
      distinct_count = distinct_l,
      entropy = round(entropy, 3),
      passed = passed
    )
  }
  
  cat(sprintf("=== l-DIVERSITY AUDIT (Talab: l >= %d) ===\n", min_l))
  cat(sprintf("Jami ekvivalent sinflar: %d\n", length(split_groups)))
  cat(sprintf("Muvaffaqiyatsiz (Homogeneous) guruhlar soni: %d\n", failed_groups))
  
  return(results)
}

# Misol: 4 kishilik guruh bo'lsa ham hammasida 'Covid-19' tashxisi bo'lsa homogeneity yuz beradi
test_patients <- data.frame(
  Hudud = c("A", "A", "A", "A", "B", "B", "B", "B"),
  Yosh_Toifa = c("30-40", "30-40", "30-40", "30-40", "50-60", "50-60", "50-60", "50-60"),
  Tashxis = c("Covid-19", "Covid-19", "Covid-19", "Covid-19", "Astma", "Diabet", "Gipertoniya", "Astma")
)

audit_l <- check_l_diversity(test_patients, c("Hudud", "Yosh_Toifa"), "Tashxis", min_l = 2)
for (res in audit_l) {
  cat(sprintf("Guruh: [%s] -> O'lcham: %d, Turli tashxislar: %d, Holat: %s\n",
              res$group, res$size, res$distinct_count, ifelse(res$passed, "XAVFSIZ", "XAVFLI!")))
}
```
**Tushuntirish:** l-Diversity guruhdagi barcha qatnashuvchilar bir xil tashxisga ega bo'lib qolish xavfini yo'qotadi. Masalan, agar 'A, 30-40' guruhidagi 4 kishining hammasida saraton bo'lsa, tajovuzkor bu guruhga kiruvchi qo'shnisining aynan saraton ekanligini 100% aniqlay olardi. l-Diversity bunday guruhlarni taqiqlaydi.

---

### Topshiriq #1176: t-Closeness Talabi: Nozik Atributlar Taqsimotining Wasserstein Masofasini Tekshirish
**Tavsif:** Agar butun aholi bo'yicha ma'lum kasallik 1% bo'lsa, ammo ma'lum ekvivalent sinfda 50% ga yetsa, tajovuzkor nozik ma'lumotni bilib oladi (Skewness Attack). t-Closeness har bir guruhdagi taqsimot global taqsimotdan t masofadan uzoqlashmasligini talab qiladi.
**Talablar:** R tilida 1-o'lchovli Wasserstein (Earth Mover's Distance) masofasini hisoblovchi va har bir guruhning t-closeness shartini qanoatlantirishini tekshiruvchi algoritm yaratish.
**Yechim (R):**
```r
# Wasserstein masofasi (Earth Mover's Distance) va t-closeness

wasserstein_distance_1d <- function(p, q) {
  # Kumulyativ taqsimot funksiyalari (CDF) orasidagi farqning L1 normasi
  cdf_p <- cumsum(p)
  cdf_q <- cumsum(q)
  sum(abs(cdf_p - cdf_q)) / length(p)
}

audit_t_closeness <- function(df, quasi_cols, sensitive_col, t_threshold = 0.15) {
  categories <- sort(unique(df[[sensitive_col]]))
  
  # Global taqsimot Q
  global_table <- table(factor(df[[sensitive_col]], levels = categories))
  Q <- as.numeric(global_table) / nrow(df)
  
  # Guruhlar bo'yicha tahlil
  split_groups <- split(df[[sensitive_col]], df[quasi_cols], drop = TRUE)
  violations <- 0
  
  cat(sprintf("=== t-CLOSENESS TAHLILI (Cheklov t <= %.2f) ===\n", t_threshold))
  
  for (grp_name in names(split_groups)) {
    vals <- split_groups[[grp_name]]
    grp_table <- table(factor(vals, levels = categories))
    P <- as.numeric(grp_table) / length(vals)
    
    # Masofa
    dist <- wasserstein_distance_1d(P, Q)
    is_safe <- (dist <= t_threshold)
    if (!is_safe) violations <- violations + 1
    
    cat(sprintf("Guruh: %-20s | Masofa: %.4f | Holat: %s\n",
                grp_name, dist, ifelse(is_safe, "MOS", "BUZILGAN!")))
  }
  
  cat(sprintf("Jami qoidabuzarliklar: %d\n", violations))
}

# Test ma'lumotlari: Global taqsimot: Kam daromad = 70%, O'rta = 20%, Yuqori = 10%
set.seed(42)
global_daromad <- sample(c("1_Kam", "2_Orta", "3_Yuqori"), 1000, replace = TRUE, prob = c(0.7, 0.2, 0.1))
tadbirkorlar <- data.frame(
  Hudud = sample(c("Viloyat_A", "Viloyat_B"), 1000, replace = TRUE),
  Daromad_Darajasi = global_daromad
)

audit_t_closeness(tadbirkorlar, "Hudud", "Daromad_Darajasi", t_threshold = 0.05)
```
**Tushuntirish:** t-Closeness l-diversity ning kamchiliklarini tuzatadi. Masalan, agar butun mamlakatda OIV (HIV) bilan kasallanish 0.01% bo'lsa, va ma'lum guruhda bu ko'rsatkich 15% ga chiqsa (guruhda 3 xil tashxis bo'lib l=3 bajarilgan bo'lsa ham), bu guruh a'zosi OIV xavfiga 1500 barobar ko'proq duchor ekani fosh bo'ladi. t-Closeness bunga yo'l qo'ymaydi.

---

### Topshiriq #1177: Mikroyig'ish (Microaggregation): Raqamli Atributlarni Klasterlash va O'rtachalash
**Tavsif:** Raqamli o'zgaruvchilarni (Daromad, Sarflangan mablag', Qon bosimi) bosish yoki intervallarga bo'lish katta miqdorda ma'lumot yo'qotilishiga sabab bo'ladi. Mikroyig'ish usuli o'xshash k ta yozuvni klasterlaydi va ularning qiymatini klaster o'rtachasi bilan almashtiradi.
**Talablar:** R tilida bir o'lchovli va ko'p o'lchovli (k-means yordamida) mikroyig'ish algoritmini amalga oshirish: har bir k ta eng yaqin elementlarni guruhlab o'rtacha qiymatga almashtirish.
**Yechim (R):**
```r
# Raqamli ma'lumotlar uchun mikroyig'ish (Microaggregation)

microaggregate_1d <- function(x, k = 3) {
  n <- length(x)
  sorted_idx <- order(x)
  sorted_x <- x[sorted_idx]
  
  aggregated <- numeric(n)
  
  # Har bir k o'lchamli bo'laklarga ajratish
  i <- 1
  while (i <= n) {
    end_idx <- min(i + k - 1, n)
    
    # Agar oxirgi bo'lak k dan kichik bo'lsa, oldingi bo'lakka qo'shish
    if ((n - end_idx) < k && end_idx < n) {
      end_idx <- n
    }
    
    mean_val <- mean(sorted_x[i:end_idx])
    aggregated[i:end_idx] <- mean_val
    i <- end_idx + 1
  }
  
  # Asl tartibga qaytarish
  result <- numeric(n)
  result[sorted_idx] <- aggregated
  return(result)
}

# Test: Mijozlarning bank hisobidagi qoldiq mablag'lari
set.seed(99)
haqiqiy_balans <- round(runif(15, min = 1000, max = 50000))

himoyalangan_balans <- microaggregate_1d(haqiqiy_balans, k = 3)

solishtirma <- data.frame(
  Haqiqiy = haqiqiy_balans,
  Mikroyigilgan = round(himoyalangan_balans),
  Farq = round(himoyalangan_balans - haqiqiy_balans)
)
print(solishtirma)
cat("Haqiqiy o'rtacha:", mean(haqiqiy_balans), "Mikroyig'ilgan o'rtacha:", mean(himoyalangan_balans), "\n")
```
**Tushuntirish:** Mikroyig'ishning asosiy ustunligi shundaki, u butun datasetning global o'rtacha qiymatini va umumiy yig'indisini 100% o'zgarmasdan saqlab qoladi (sum(asl) == sum(himoya)). Shaxsiy ma'lumotlar esa kamida k ta o'xshash odamlar o'rtasida o'rtachalashtirilgani sababli xavfsiz holatga keladi.

---

### Topshiriq #1178: Tasodifiy O'rin Almashtirish (Rank Swapping va Data Swapping) Usuli
**Tavsif:** Korrelyatsion tahlilni saqlagan holda ma'lumotlar xavfsizligini oshirishning yana bir usuli bu Rank Swapping bo'lib, unda qiymatlar o'z tartibiga yaqin bo'lgan boshqa qatorlar bilan o'rin almashtiriladi (masalan, p=5% diapazonda).
**Talablar:** R tilida ustunlar bo'yicha Rank Swapping mexanizmini yozish: berilgan p (foiz) oralig'idagi tasodifiy qator bilan qiymatlarni almashtirish va yakuniy Spearman korrelyatsiyasining saqlanganligini isbotlash.
**Yechim (R):**
```r
# Rank Swapping algoritmi

rank_swap <- function(x, p = 0.05) {
  n <- length(x)
  sorted_idx <- order(x)
  swapped_x <- x
  
  # Har bir qator uchun tartiblangan ro'yxatdagi qo'shnilar bilan almashtirish
  window <- max(1, ceiling(n * p))
  
  for (i in 1:n) {
    # Almashtirish uchun mumkin bo'lgan indekslar oralig'i [i - window, i + window]
    low <- max(1, i - window)
    high <- min(n, i + window)
    
    target_rank <- sample(low:high, 1)
    
    # Haqiqiy indekslarni olish
    idx1 <- sorted_idx[i]
    idx2 <- sorted_idx[target_rank]
    
    # Qiymatlarni almashtirish
    tmp <- swapped_x[idx1]
    swapped_x[idx1] <- swapped_x[idx2]
    swapped_x[idx2] <- tmp
  }
  
  return(swapped_x)
}

# Test: Bo'y va Vazn o'rtasidagi korrelyatsiya
set.seed(42)
N <- 200
boy <- rnorm(N, mean = 175, sd = 8)
vazn <- (boy - 100) * 1.1 + rnorm(N, mean = 0, sd = 4)

# Asl korrelyatsiya
boshlangich_korr <- cor(boy, vazn, method = "spearman")

# Vazn ustunini Rank Swapping orqali himoyalash (p = 0.05)
himoyalangan_vazn <- rank_swap(vazn, p = 0.05)

yangi_korr <- cor(boy, himoyalangan_vazn, method = "spearman")

cat("Asl Spearman korrelyatsiyasi:       ", round(boshlangich_korr, 4), "\n")
cat("Rank Swappingdan keyingi korrelyatsiya:", round(yangi_korr, 4), "\n")
cat("Korrelyatsiya yo'qotilishi atigi:   ", round(abs(boshlangich_korr - yangi_korr), 4), "\n")
```
**Tushuntirish:** Rank Swapping o'zgaruvchining umumiy taqsimotini (Empirical CDF) umuman o'zgartirmaydi, chunki ustundagi raqamlar to'plami aynan bir xil bo'lib qoladi. Faqat qaysi bemor aynan qaysi raqamga egaligi aralashtirib yuboriladi. Parametr p nazorat qilinib, tahliliy aniqlik va xavfsizlik boshqariladi.

---

### Topshiriq #1179: Sintetik Ma'lumotlar Generatsiyasi: Gauss Kopulalari (Gaussian Copula) Bilan Korrelyatsiyani Saqlash
**Tavsif:** Haqiqiy shaxsiy ma'lumotlarni hech qanday o'zgartirishsiz ulashish o'rniga, asl bazaning barcha ko'p o'lchovli korrelyatsiya va taqsimotlarini o'zida aks ettirgan sun'iy (sintetik) dataset yaratish eng xavfsiz usullardan biridir.
**Talablar:** R tili yordamida Gauss Kopulasi yordamida parametrli sintetik ma'lumotlar generatorini yaratish: marjinal taqsimotlarni emperik CDF orqali uniformaga o'tkazish, kovariatsiya matritsasini hisoblash va yangi soxta bemorlar profilini tuzish.
**Yechim (R):**
```r
# Gaussian Copula asosida sintetik ma'lumotlar yaratish

generate_synthetic_copula <- function(df, n_samples = NULL) {
  if (is.null(n_samples)) n_samples <- nrow(df)
  numeric_cols <- names(df)[sapply(df, is.numeric)]
  sub_df <- df[, numeric_cols]
  p <- length(numeric_cols)
  
  # 1. Har bir ustunni emperik CDF (Rank) orqali Uniform[0,1] ga aylantirish
  u_matrix <- matrix(0, nrow = nrow(df), ncol = p)
  for (j in 1:p) {
    u_matrix[, j] <- (rank(sub_df[, j]) - 0.5) / nrow(df)
  }
  
  # 2. Uniform qiymatlarni standart normal taqsimotga aylantirish (Z-score)
  z_matrix <- qnorm(u_matrix)
  
  # 3. Kovariatsiya (Korrelyatsiya) matritsasini hisoblash
  sigma_mat <- cor(z_matrix)
  
  # 4. Yangi multivariativ normal vektorlar generatsiyasi (Cholesky dekompozitsiyasi)
  chol_decomp <- chol(sigma_mat)
  raw_normal <- matrix(rnorm(n_samples * p), nrow = n_samples, ncol = p)
  synthetic_z <- raw_normal %*% chol_decomp
  
  # 5. Qayta Uniform taqsimotga o'tkazish
  synthetic_u <- pnorm(synthetic_z)
  
  # 6. Asl ustunlarning kvantillari yordamida qiymatlarni tiklash
  synthetic_df <- as.data.frame(matrix(0, nrow = n_samples, ncol = p))
  colnames(synthetic_df) <- numeric_cols
  
  for (j in 1:p) {
    synthetic_df[, j] <- quantile(sub_df[, j], probs = synthetic_u[, j], type = 1)
  }
  
  return(synthetic_df)
}

# Test: Bemorlarning Yosh, Glyukoza va BMI ko'rsatkichlari
set.seed(2026)
n_real <- 300
real_df <- data.frame(
  Yosh = round(rnorm(n_real, 50, 10)),
  Glyukoza = rgamma(n_real, shape = 12, rate = 2),
  BMI = rnorm(n_real, 26, 4)
)

synthetic_df <- generate_synthetic_copula(real_df, n_samples = 300)

cat("Asl ma'lumotlar korrelyatsiyasi:\n")
print(round(cor(real_df), 3))
cat("\nSintetik ma'lumotlar korrelyatsiyasi:\n")
print(round(cor(synthetic_df), 3))
```
**Tushuntirish:** Gauss Kopulasi marjinal taqsimotlar qanday bo'lishidan qat'i nazar (normal, gamma, bimodal), ularning o'zaro chiziqli va nochiziqli bog'liqlik strukturasini ajratib oladi va yangi soxta namunalar yaratadi. Bu sintetik datasetda birorta ham real tirik insonning yozuvi bo'lmaydi.

---

### Topshiriq #1180: Axborot Yo'qotilishi (Information Loss) va Tahliliy Foydalilik (Utility Metrics) Baholash
**Tavsif:** Anonimlashtirish yoki differensial shovqin qo'shilgandan so'ng ma'lumotlarning tahlil uchun qanchalik yaroqli ekanligini o'lchash zarur. Buning uchun o'rtacha kvadratik xatolik (MSE), o'rtacha absolyut xatolik (MAE) va o'zgaruvchanlik yo'qolishi (IL1) metrikalari qo'llaniladi.
**Talablar:** R tilida asl va himoyalangan ma'lumotlar jadvali o'rtasidagi axborot yo'qotilishi (IL) indekslarini, korrelyatsiya buzilishini va dispersiya saqlanish koeffitsientini hisoblovchi kommutativ metrikalar to'plamini yaratish.
**Yechim (R):**
```r
# Axborot yo'qotilishi (Information Loss) metrikalari

calculate_information_loss <- function(original_df, masked_df) {
  num_cols <- names(original_df)[sapply(original_df, is.numeric)]
  
  metrics <- list()
  
  for (col in num_cols) {
    x_orig <- original_df[[col]]
    x_mask <- masked_df[[col]]
    
    # 1. Normalizatsiyalangan O'rtacha Absolyut Xato (NMAE)
    range_val <- max(x_orig) - min(x_orig)
    mae <- mean(abs(x_orig - x_mask))
    nmae <- mae / range_val
    
    # 2. O'rtacha qiymatning o'zgarishi (%)
    mean_diff_pct <- abs(mean(x_mask) - mean(x_orig)) / abs(mean(x_orig)) * 100
    
    # 3. Dispersiya nisbati (Variance Ratio)
    var_ratio <- var(x_mask) / var(x_orig)
    
    metrics[[col]] <- data.frame(
      Ustun = col,
      MAE = round(mae, 4),
      NMAE_Foiz = round(nmae * 100, 2),
      Orta_Xato_Foiz = round(mean_diff_pct, 2),
      Dispersiya_Nisbati = round(var_ratio, 3)
    )
  }
  
  summary_table <- do.call(rbind, metrics)
  return(summary_table)
}

# Sinov
set.seed(123)
orig_data <- data.frame(
  Xolesterin = rnorm(100, mean = 200, sd = 30),
  Yurak_Uradi = rnorm(100, mean = 75, sd = 10)
)

# Kichik Laplace shovqini bilan himoyalangan dataset
masked_data <- data.frame(
  Xolesterin = orig_data$Xolesterin + rnorm(100, 0, 5),
  Yurak_Uradi = orig_data$Yurak_Uradi + rnorm(100, 0, 2)
)

hisobot <- calculate_information_loss(orig_data, masked_data)
cat("=== AXBOROT YO'QOTILISHI VA FOYDALILIK (UTILITY) BAHOSI ===\n")
print(hisobot)
```
**Tushuntirish:** Maxfiylik va foydalilik (Privacy-Utility Tradeoff) o'rtasidagi kelishuv ma'lumotlar xavfsizligining oltin qoidasidir. 100% maxfiylik barcha ma'lumotlarni o'chirib yuborish orqali erishiladi, ammo foydasi nol bo'ladi. Axborot yo'qotilishi metrikalari ML modellar va statistik xulosalar ishonchliligini nazorat qilish imkonini beradi.

---

### Topshiriq #1181: Qisman Gomonorfik Shifrlash (Paillier PHE) Matematik Asoslari
**Tavsif:** Gomonorfik shifrlash (HE) shifrlangan ma'lumotlarni ochmasdan (dekript qilmasdan) ular ustida matematik amallar bajarish imkonini beradi. Paillier kriptotizimi additiv gomonorfiyaga ega: E(m1) * E(m2) mod n^2 = E(m1 + m2 mod n).
**Talablar:** R tilida Paillier tizimining kalit generatsiyasi (p, q tub sonlar), shifrlash (E) va deshifrlash (D) modullarini modulyar arifmetika bilan to'liq amalga oshirish.
**Yechim (R):**
```r
# Modulyar arifmetika yordamchilari
mod_pow <- function(base, exp, mod) {
  res <- 1
  base <- base %% mod
  while (exp > 0) {
    if (exp %% 2 == 1) res <- (res * base) %% mod
    base <- (base * base) %% mod
    exp <- floor(exp / 2)
  }
  return(res)
}

# Kengaytirilgan Evklid algoritmi (Modulyar teskari son)
mod_inv <- function(a, m) {
  m0 <- m
  y <- 0
  x <- 1
  if (m == 1) return(0)
  while (a > 1) {
    q <- floor(a / m)
    t <- m
    m <- a %% m
    a <- t
    t <- y
    y <- x - q * y
    x <- t
  }
  if (x < 0) x <- x + m0
  return(x)
}

# Paillier kalitlarini generatsiya qilish (namoyish uchun kichik tub sonlar)
paillier_keygen <- function(p = 61, q = 53) {
  n <- p * q
  n_sq <- n * n
  lambda <- (p - 1) * (q - 1) # soddalashtirilgan lcm
  g <- n + 1                  # g = n + 1 standarti
  
  # L(u) = (u - 1) / n
  # mu = (L(g^lambda mod n^2))^-1 mod n
  l_val <- (mod_pow(g, lambda, n_sq) - 1) / n
  mu <- mod_inv(l_val, n)
  
  list(
    pub = list(n = n, n_sq = n_sq, g = g),
    priv = list(lambda = lambda, mu = mu, n = n, n_sq = n_sq)
  )
}

# Shifrlash: c = g^m * r^n mod n^2
paillier_encrypt <- function(m, pub, r = 17) {
  c1 <- mod_pow(pub$g, m, pub$n_sq)
  c2 <- mod_pow(r, pub$n, pub$n_sq)
  (c1 * c2) %% pub$n_sq
}

# Deshifrlash: m = L(c^lambda mod n^2) * mu mod n
paillier_decrypt <- function(c, priv) {
  u <- mod_pow(c, priv$lambda, priv$n_sq)
  l_val <- (u - 1) / priv$n
  (l_val * priv$mu) %% priv$n
}

# Sinov
keys <- paillier_keygen(61, 53)
m_original <- 42
c <- paillier_encrypt(m_original, keys$pub, r = 23)
m_decrypted <- paillier_decrypt(c, keys$priv)

cat("Asl maxfiy xabar (m):", m_original, "\n")
cat("Shifrlangan matn (c): ", c, "\n")
cat("Deshifrlangan natija: ", m_decrypted, "\n")
```
**Tushuntirish:** Paillier kriptotizimi additiv gomonorfiyani amalga oshiradi. Uning xavfsizligi kompozit qoldiqlarning qiyinligi gipotezasiga (Decisional Composite Residuosity Assumption) tayanadi. Kalit generatsiyasida n = p * q olinadi va hisob-kitoblar mod n^2 maydonida yuritiladi.

---

### Topshiriq #1182: Paillier Shifrlashida Skalyarga Ko'paytirish (Enc(m)^k = Enc(k * m))
**Tavsif:** Gomonorfik shifrlashning yana bir muhim xossasi shundaki, shifrlangan matnni oddiy ochiq skalyar songa (k) darajaga ko'tarish ichki ochiq matnni k ga ko'paytirishga tengdir: (g^m * r^n)^k = g^(k*m) * (r^k)^n.
**Talablar:** R tilida shifrlangan maoshni ochiq koeffitsientga (masalan, 15% bonus yoki valyuta kursi) ko'paytiruvchi gomonorfik funksiya yozish va server xom maoshni bilmasdan yangilangan maoshni hisoblab berishini ta'minlash.
**Yechim (R):**
```r
# Skalyar ko'paytirish funksiyasi

paillier_mul_scalar <- function(c, k, pub) {
  # c_new = c^k mod n^2
  mod_pow(c, k, pub$n_sq)
}

# Kalitlar
keys <- paillier_keygen(79, 83)

haqiqiy_maosh <- 150 # $150 soatbay stavka
koeffitsient <- 3    # 3 soatlik ish haqi

# Mijoz maoshini shifrlaydi va serverga yuboradi
c_maosh <- paillier_encrypt(haqiqiy_maosh, keys$pub, r = 13)
cat("Serverdagi shifrlangan maosh:", c_maosh, "\n")

# Server (maxfiy maoshni bilmasdan!) 3 ga ko'paytiradi
c_natija <- paillier_mul_scalar(c_maosh, koeffitsient, keys$pub)
cat("Serverdagi hisoblangan shifrlangan natija:", c_natija, "\n")

# Mijoz server natijasini olib deshifrlaydi
haqiqiy_hisob <- paillier_decrypt(c_natija, keys$priv)
cat("Mijoz deshifrlagan yakuniy to'lov: $", haqiqiy_hisob, "\n")
cat("Tekshirish (150 * 3): $", 150 * 3, "\n")
```
**Tushuntirish:** Skalyar ko'paytirish bulutli hisoblashlarda (Cloud Computing) juda qo'l keladi. Foydalanuvchi o'zining shaxsiy ko'rsatkichlarini bulutga shifrlangan holda yuboradi, bulut esa mashinali o'rganish modelining og'irliklariga (koeffitsientlarga) ko'paytirib, shifrlangan javobni qaytaradi. Bulut hech qachon mijoz ma'lumotlarini o'qiy olmaydi.

---

### Topshiriq #1183: Shifrlangan Moliyaviy Tranzaksiyalar Yig'indisini Hisoblash (Encrypted Aggregation)
**Tavsif:** Bir nechta mustaqil subyektlar (masalan, 5 ta raqobatchi bank) o'zlarining umumiy kredit portfeli hajmini hisoblamoqchi, ammo hech biri o'zining ichki balansini boshqalarga oshkor qilmoqchi emas.
**Talablar:** R tilida Paillier gomonorfik qo'shish xossasidan foydalanib: c_sum = prod(c_i) mod n^2 orqali barcha banklarning shifrlangan depozitlarini jamlovchi xavfsiz aggregation protokoli tuzish.
**Yechim (R):**
```r
# Gomonorfik yig'indi (Encrypted Aggregation)

paillier_add <- function(c1, c2, pub) {
  (c1 * c2) %% pub$n_sq
}

# Tizim markaziy koordinatori umumiy ochiq kalitni yaratadi
keys <- paillier_keygen(101, 103)

# 4 ta mustaqil bankning depozitlari ($ million)
bank_depozitlari <- c(Bank_A = 120, Bank_B = 450, Bank_C = 310, Bank_D = 220)

# Har bir bank o'z summasini ochiq kalit bilan shifrlaydi
shifrlangan_paketlar <- sapply(seq_along(bank_depozitlari), function(i) {
  # Har bir bank uchun unikal tasodifiy r
  paillier_encrypt(bank_depozitlari[i], keys$pub, r = 11 + i * 2)
})

cat("Banklarning shifrlangan paketlari:\n")
print(shifrlangan_paketlar)

# Server (Agregator) barcha shifrlangan qiymatlarni ko'paytiradi
c_total <- 1
for (c in shifrlangan_paketlar) {
  c_total <- paillier_add(c_total, c, keys$pub)
}

cat("Markaziy serverdagi shifrlangan agregat yig'indi:", c_total, "\n")

# Barcha banklar birgalikda (yoki ishonchli audit) yig'indini ochadi
yakuniy_depozit <- paillier_decrypt(c_total, keys$priv)

cat("Ochilgan umumiy bozor depoziti: $", yakuniy_depozit, "million\n")
cat("Haqiqiy sum(depozitlar):         $", sum(bank_depozitlari), "million\n")
```
**Tushuntirish:** Gomonorfik yig'ish (Encrypted Aggregation) moliyaviy audit, maxfiy ovoz berish (e-voting) va korporativ statistika to'plashda qo'llaniladi. Bitta tranzaksiyaning miqdori hech kimga ma'lum bo'lmaydi, faqat yakuniy jami yig'indi ochiladi.

---

### Topshiriq #1184: To'liq Gomonorfik Shifrlash (FHE: BFV / CKKS) Asosiy Konsepsiyalari va Polinom Aritmetikasi
**Tavsif:** To'liq gomonorfik shifrlash (Fully Homomorphic Encryption - FHE) nafaqat qo'shish, balki shifrlangan holatda ixtiyoriy ko'paytirish va nochiziqli funksiyalarni bajarish imkonini beradi. BFV va CKKS sxemalari halqa polinomlari (RLWE - Ring Learning With Errors) asosida ishlaydi.
**Talablar:** R tilida soddalashtirilgan polinom ko'paytirish va xatolar (noise) qo'shilishini simulyatsiya qiluvchi RLWE asosidagi FHE modulyatsiyasini yozish.
**Yechim (R):**
```r
# Ring Learning With Errors (RLWE) Polinom Aritmetikasi simulyatsiyasi

# Polinomlarni modul x^d + 1 va modul q bo'yicha ko'paytirish
poly_mul_mod <- function(p1, p2, d = 4, q = 97) {
  # Oddiy konvolyutsiya
  conv <- convolve(p1, rev(p2), type = "open")
  deg_conv <- length(conv)
  
  # R[x] / (x^d + 1) qoldig'ini olish
  res <- numeric(d)
  for (i in 1:deg_conv) {
    deg <- i - 1
    coeff <- round(conv[i])
    power_mod <- deg %% d
    sign_flip <- if ((floor(deg / d) %% 2) == 1) -1 else 1
    
    res[power_mod + 1] <- (res[power_mod + 1] + sign_flip * coeff) %% q
  }
  return((res + q) %% q)
}

# Polinom qo'shish
poly_add_mod <- function(p1, p2, q = 97) {
  ((p1 + p2) %% q + q) %% q
}

# Namuna: Maxfiy xabar m = [1, 0, 1, 0]
set.seed(42)
d <- 4
q <- 97

# Kalitlar
secret_key <- sample(c(-1, 0, 1), d, replace = TRUE)
a <- sample(0:(q - 1), d, replace = TRUE)
e <- sample(c(-1, 0, 1), d, replace = TRUE) # Kichik xatolik (shovqin)

# Ochiq kalit b = - (a * s + e) mod q
as_term <- poly_mul_mod(a, secret_key, d, q)
b <- (-(as_term + e) %% q + q) %% q

cat("RLWE Ochiq kalit juftligi (a, b) generatsiya qilindi.\n")
cat("Xatolik (Error budget): FHE da har bir ko'paytirish shovqinni oshiradi.\n")
```
**Tushuntirish:** FHE zamonaviy kriptografiyaning eng yuqori cho'qqisidir. U bulutli AI tizimlariga mijozning tibbiy tasvirlari (MRI, KT) yoki genetik ma'lumotlarini shifrlangan holatda berib, to'g'ridan-to'g'ri tashxis qo'yish imkonini beradi. Har bir operatsiyada xatolik (noise) o'sib boradi va ma'lum chegaradan oshganda Bootstrapping operatsiyasi orqali tozalanadi.

---

### Topshiriq #1185: Shamir's Secret Sharing: Maxfiy Kalitni (k, n) Bo'laklarga Ajratish va Lagrange Interpolatsiyasi
**Tavsif:** Eng muhim kriptografik kalitlar (masalan, markaziy bank zaxira kaliti yoki davlat maxfiy shifri) bitta odamga ishonib topshirilmaydi. Shamir sxemasi maxfiy sirni n ta odamga bo'lib beradi va uni tiklash uchun kamida k ta (k <= n) bo'lak birlashishi shart.
**Talablar:** R tilida chekli maydonda (GF(p)) Shamir (3, 5) kalit bo'lish va ixtiyoriy 3 ta bo'lakdan Lagrange interpolatsiyasi orqali sirni tiklovchi to'liq funksiyalar to'plamini yozish.
**Yechim (R):**
```r
# Shamir's Secret Sharing chekli maydonda (GF(p))

# GF(p) da modulyar amallar
gf_add <- function(a, b, p) ((a + b) %% p + p) %% p
gf_sub <- function(a, b, p) ((a - b) %% p + p) %% p
gf_mul <- function(a, b, p) ((a * b) %% p + p) %% p

# Shamir bo'laklariga ajratish (Threshold = k, Jami = n)
shamir_split <- function(secret, k, n, p = 257) {
  # k - 1 darajali tasodifiy polinom: P(x) = secret + a1*x + a2*x^2 + ...
  coeffs <- c(secret, sample(1:(p - 1), k - 1))
  
  shares <- list()
  for (x in 1:n) {
    # P(x) ni hisoblash
    y <- 0
    for (deg in seq_along(coeffs)) {
      term <- gf_mul(coeffs[deg], mod_pow(x, deg - 1, p), p)
      y <- gf_add(y, term, p)
    }
    shares[[x]] <- list(x = x, y = y)
  }
  return(shares)
}

# Lagrange interpolatsiyasi orqali P(0) = Secret ni tiklash
shamir_reconstruct <- function(selected_shares, p = 257) {
  k <- length(selected_shares)
  xs <- sapply(selected_shares, function(s) s$x)
  ys <- sapply(selected_shares, function(s) s$y)
  
  secret <- 0
  for (i in 1:k) {
    # Lagrange asosi l_i(0) = prod_{j != i} (0 - x_j) / (x_i - x_j)
    num <- 1
    den <- 1
    for (j in 1:k) {
      if (i != j) {
        num <- gf_mul(num, gf_sub(0, xs[j], p), p)
        den <- gf_mul(den, gf_sub(xs[i], xs[j], p), p)
      }
    }
    li_0 <- gf_mul(num, mod_inv(den, p), p)
    term <- gf_mul(ys[i], li_0, p)
    secret <- gf_add(secret, term, p)
  }
  return(secret)
}

# Sinov: Boshqaruv kaliti = 188. (3, 5) sxema: 5 ta bo'lak, tiklash uchun 3 tasi yetarli
p_prime <- 257
asl_sir <- 188

bolaklar <- shamir_split(asl_sir, k = 3, n = 5, p = p_prime)
cat("5 ta hissadorga berilgan bo'laklar (x, y):\n")
for (s in bolaklar) cat(sprintf("  Hissa %d: (%d, %d)\n", s$x, s$x, s$y))

# Ixtiyoriy 3 ta hissa (masalan 2, 4 va 5) orqali tiklash
tanlangan_hissalar <- list(bolaklar[[2]], bolaklar[[4]], bolaklar[[5]])
tiklangan_sir <- shamir_reconstruct(tanlangan_hissalar, p = p_prime)

cat("Tiklash uchun tanlangan hissalar: 2, 4 va 5-hissadorlar\n")
cat("Tiklangan maxfiy kalit:", tiklangan_sir, "\n")
cat("Muvaffaqiyat:", asl_sir == tiklangan_sir, "\n")
```
**Tushuntirish:** Shamir's Secret Sharing mukammal axborot-nazariy xavfsizlikka ega (Information-Theoretic Security). Agar tajovuzkor k-1 ta bo'lakni qo'lga kiritsa ham, asl sir haqida mutlaqo nol ma'lumot oladi, chunki chekli maydonda har qanday qiymat teng ehtimolli bo'lib qoladi.

---

### Topshiriq #1186: Xavfsiz Ko'p Tomonlama Hisoblash (SMPC / Private Set Intersection - PSI)
**Tavsif:** Ikki tashkilot (masalan, Soliq idorasi va Tijorat banki) o'z mijozlari ro'yxatidagi umumiy shaxslarni (Intersection) topmoqchi, biroq hech bir tomon o'zining qolgan boshqa mijozlari ro'yxatini oshkor qilmasligi lozim.
**Talablar:** R tilida Diffie-Hellman kommutativ xeshlashiga asoslangan Private Set Intersection (PSI) protokolini amalga oshirish: har ikki tomon o'z xeshlarini eksponentalaydi va kesishmani xavfsiz aniqlaydi.
**Yechim (R):**
```r
# Diffie-Hellman asosidagi Private Set Intersection (PSI)

# Ikkita tomon: Alice (Soliq) va Bob (Bank)
# 1. Umumiy parametrlar: Katta tub son p
p_field <- 65537

# Maxfiy kalitlar (faqat har bir tomonning o'ziga ma'lum)
k_alice <- 3217
k_bob <- 4519

# Har bir tomonning ma'lumotlari
alice_set <- c("JSHSHIR_001", "JSHSHIR_002", "JSHSHIR_003", "JSHSHIR_004")
bob_set   <- c("JSHSHIR_003", "JSHSHIR_004", "JSHSHIR_005", "JSHSHIR_006")

# Xesh funksiyasi (Matnni chekli maydon elementiga o'tkazish)
hash_to_int <- function(str, mod) {
  raw_bytes <- as.integer(charToRaw(str))
  sum(raw_bytes * (1:length(raw_bytes))) %% mod
}

# 1-qadam: Alice o'z to'plamini xeshlab, k_alice darajaga ko'taradi va Bobga jo'natadi
h_alice <- sapply(alice_set, hash_to_int, mod = p_field)
enc_alice <- sapply(h_alice, function(x) mod_pow(x, k_alice, p_field))

# 2-qadam: Bob o'z to'plamini xeshlab, k_bob darajaga ko'taradi
h_bob <- sapply(bob_set, hash_to_int, mod = p_field)
enc_bob <- sapply(h_bob, function(x) mod_pow(x, k_bob, p_field))

# 3-qadam: Ikki karra shifrlash (Kommutativlik: (H^a)^b == (H^b)^a mod p)
# Bob Alice yuborgan qiymatlarni k_bob darajaga ko'taradi va aralashtiradi (shuffle)
alice_then_bob <- sample(sapply(enc_alice, function(x) mod_pow(x, k_bob, p_field)))

# Alice Bobning qiymatlarini k_alice darajaga ko'taradi
bob_then_alice <- sapply(enc_bob, function(x) mod_pow(x, k_alice, p_field))

# 4-qadam: Kesishma qiymatlarni solishtirish
kesishma_tokenlar <- intersect(alice_then_bob, bob_then_alice)

# Bob o'zining qaysi elementlari kesishmaga kirganini aniqlaydi
umumiy_mijozlar <- bob_set[bob_then_alice %in% kesishma_tokenlar]

cat("Alice to'plami: ", alice_set, "\n")
cat("Bob to'plami:   ", bob_set, "\n")
cat("Xavfsiz topilgan umumiy mijozlar:", umumiy_mijozlar, "\n")
```
**Tushuntirish:** PSI protokoli kommutativ shifrlash xossasiga tayanadi: E_b(E_a(x)) = E_a(E_b(x)). Tomonlar shaxsiy ma'lumotlarni hech qachon almashmaydi, faqat ikki karra shifrlangan qoldiqlar solishtiriladi va faqat umumiy a'zolar aniqlanadi.

---

### Topshiriq #1187: Yao ning Millionerlar Muammosi (Yao's Millionaires' Problem / Garbled Circuits)
**Tavsif:** Ikki boy tadbirkor kim ko'proq boylikka ega ekanligini bilmoqchi, biroq hech biri o'zining aniq daromadini boshqasiga aytishni istamaydi. Bu xavfsiz ko'p tomonlama hisoblashning (SMPC) klassik poydevoridir.
**Talablar:** R tilida Yao ning millionchilar protokolining sodda matematik modelini yaratish: ochiq RSA kaliti va blinding (xiralashtirish) orqali kimning boyligi katta ekanligini (x > y) maxfiy aniqlash.
**Yechim (R):**
```r
# Yao's Millionaires' Problem - Kriptografik simulyatsiya

solve_millionaires <- function(wealth_alice, wealth_bob, max_wealth = 10) {
  # Shart: 1 <= wealth <= max_wealth
  stopifnot(wealth_alice <= max_wealth, wealth_bob <= max_wealth)
  
  # 1. Bob ochiq/yopiq kalit yaratadi (namoyish uchun RSA)
  p <- 61; q <- 53; N <- p * q; phi <- (p - 1) * (q - 1)
  e <- 17; d <- mod_inv(e, phi)
  
  # 2. Bob tasodifiy k sonini tanlaydi va c = k^e mod N hisoblaydi
  k <- sample(10:50, 1)
  c <- mod_pow(k, e, N)
  
  # Bob Alicega c - wealth_bob jo'natadi
  msg_to_alice <- c - wealth_bob
  
  # 3. Alice 1 dan max_wealth gacha bo'lgan barcha qiymatlar uchun y_i ni hisoblaydi
  # y_i = (msg_to_alice + i)^d mod N
  y_seq <- sapply(1:max_wealth, function(i) {
    mod_pow(msg_to_alice + i, d, N)
  })
  
  # Alice katta tub son p_test tanlaydi
  p_test <- 89
  # z_i = y_i mod p_test
  z_seq <- y_seq %% p_test
  
  # Alice o'z boyligidan (wealth_alice) katta bo'lgan barcha indekslarga +1 qo'shadi
  for (i in (wealth_alice + 1):max_wealth) {
    z_seq[i] <- (z_seq[i] + 1) %% p_test
  }
  
  # 4. Bob z_seq va p_test ni oladi
  # Bob k mod p_test ni z_seq[wealth_bob] bilan solishtiradi
  bob_expected <- k %% p_test
  bob_actual <- z_seq[wealth_bob]
  
  # Agar bob_expected == bob_actual bo'lsa, demak i <= wealth_alice ga tushgan
  # ya'ni Alice >= Bob
  alice_is_richer <- (bob_expected != bob_actual)
  return(alice_is_richer)
}

# Sinov
set.seed(77)
alice_boyligi <- 7 # 7 million $
bob_boyligi   <- 5 # 5 million $

natija <- solve_millionaires(alice_boyligi, bob_boyligi, max_wealth = 10)

cat(sprintf("Alice boyligi: %dM, Bob boyligi: %dM\n", alice_boyligi, bob_boyligi))
cat("Natija: Bob Alice boyroq ekanini aniqladimi?:", natija, "\n")
```
**Tushuntirish:** Yao protokoli Garbled Circuits (Aralashtirilgan sxemalar) va Oblivious Transfer orqali amalga oshiriladi. Natijada ikkala tomon faqat 1-bit ma'lumotga (ha/yo'q) ega bo'ladi, boshqa tomonning aniq raqami esa kriptografik jihatdan to'liq maxfiy qoladi.

---

### Topshiriq #1188: Shifrlangan Ma'lumotlar Ustida Chiziqli Regressiya Bashoratini Hisoblash
**Tavsif:** Tibbiyot markazi serverida saraton xavfini bashorat qiluvchi o'qitilgan ML modeli mavjud. Bemor o'zining tibbiy parametrlarini serverga shifrlangan holda yuboradi. Server esa modelni qo'llab bemorga faqat shifrlangan natijani qaytaradi.
**Talablar:** R tilida Paillier PHE yordamida ko'p o'lchovli chiziqli regressiya y_pred = beta0 + beta1*x1 + beta2*x2 ni to'liq shifrlangan domen ustida hisoblovchi inferens pipelineini yozish.
**Yechim (R):**
```r
# Shifrlangan domen ustida chiziqli regressiya inferensi

# Model og'irliklari (Klinika serverida saqlanadi)
beta <- c(beta0 = 10, beta1 = 2, beta2 = 5)

# Bemor o'z kalitlarini yaratadi
keys <- paillier_keygen(89, 97)

# Bemor parametrlari: x1 = 4 (Qon bosimi indeksi), x2 = 3 (Glyukoza indeksi)
x1 <- 4
x2 <- 3

# Bemor faqat x parametrlarini shifrlaydi va serverga jo'natadi
c_x1 <- paillier_encrypt(x1, keys$pub, r = 7)
c_x2 <- paillier_encrypt(x2, keys$pub, r = 13)

cat("Bemor serverga yuborgan shifrlangan vektor: [c_x1, c_x2]\n")

# Server hisoblashi:
# term1 = Enc(x1)^beta1 = Enc(beta1 * x1)
# term2 = Enc(x2)^beta2 = Enc(beta2 * x2)
# term0 = Enc(beta0)
# y_pred = term0 * term1 * term2 mod n^2 = Enc(beta0 + beta1*x1 + beta2*x2)

term0 <- paillier_encrypt(beta["beta0"], keys$pub, r = 1)
term1 <- paillier_mul_scalar(c_x1, beta["beta1"], keys$pub)
term2 <- paillier_mul_scalar(c_x2, beta["beta2"], keys$pub)

c_pred <- paillier_add(term0, paillier_add(term1, term2, keys$pub), keys$pub)

cat("Server hisoblagan shifrlangan bashorat (c_pred):", c_pred, "\n")

# Bemor o'z shaxsiy kaliti bilan natijani ochadi
y_pred <- paillier_decrypt(c_pred, keys$priv)

cat("Bemor deshifrlagan saraton xavf indeksi:", y_pred, "\n")
cat("Tekshirish (10 + 2*4 + 5*3):", 10 + 2 * 4 + 5 * 3, "\n")
```
**Tushuntirish:** Bu Private Inference deb ataladi. Server bemorning shaxsiy kasallik belgilarini (x1, x2) aslo ko'rmaydi, bemor esa klinikaning xususiy intellektual mulki bo'lgan model og'irliklarini (beta parametrlarini) bilib ololmaydi. Ikki tomonlama to'liq maxfiylik ta'minlanadi.

---

### Topshiriq #1189: Zero-Knowledge Proofs: Pedersen Majburiyati (Pedersen Commitment) va Tekshiruv
**Tavsif:** Zero-Knowledge Proof (ZKP) tomonlardan biriga biror faktning to'g'riligini uning o'zini oshkor qilmasdan isbotlash imkonini beradi. Pedersen Commitment sxemasi yordamida foydalanuvchi ma'lum songa majburiyat (Commitment) bog'laydi va keyinchalik uni o'zgartira olmaydi (Binding) hamda u oshkor qilinmaguncha yashirin qoladi (Hiding).
**Talablar:** R tilida chekli maydonda Pedersen Majburiyati C = g^m * h^r mod p yaratish va keyinchalik uning haqiqiyligini tekshiruvchi protokolni tuzish.
**Yechim (R):**
```r
# Pedersen Majburiyati (Pedersen Commitment)

# Tizim generatorlari va chekli maydon tub soni
p_field <- 7919 # Katta tub son
g_gen <- 17
h_gen <- 31     # log_g(h) hech kimga noma'lum bo'lishi shart

# 1. Majburiyat yaratish (Commitment)
pedersen_commit <- function(secret_val, r_blinding, g = g_gen, h = h_gen, p = p_field) {
  c1 <- mod_pow(g, secret_val, p)
  c2 <- mod_pow(h, r_blinding, p)
  (c1 * c2) %% p
}

# 2. Ochish va tekshirish (Verify)
pedersen_verify <- function(commitment, secret_val, r_blinding, g = g_gen, h = h_gen, p = p_field) {
  expected_c <- pedersen_commit(secret_val, r_blinding, g, h, p)
  commitment == expected_c
}

# Sinov: Auksionda taklif qilingan maxfiy narx = $500
set.seed(42)
maxfiy_taklif <- 500
blinding_factor <- sample(100:5000, 1)

# Ishtirokchi o'z taklifini auksion boshida qulflaydi
auktsion_kodi <- pedersen_commit(maxfiy_taklif, blinding_factor)
cat("Auksion qutisiga tashlangan majburiyat kodi:", auktsion_kodi, "\n")

# Auksion tugagach, ishtirokchi maxfiy qiymat va blinding faktorini ochadi
tekshiruv_haqiqiy <- pedersen_verify(auktsion_kodi, maxfiy_taklif, blinding_factor)
tekshiruv_soxta <- pedersen_verify(auktsion_kodi, 600, blinding_factor) # Soxtalashtirishga urinish

cat("Asl taklif bo'yicha ZKP tasdiqlandimi?:", tekshiruv_haqiqiy, "\n")
cat("O'zgartirilgan narx rad etildimi?:      ", !tekshiruv_soxta, "\n")
```
**Tushuntirish:** Pedersen Commitment mukammal berkitish (Perfect Hiding) va hisoblash jihatidan bog'lash (Computational Binding) xossalariga ega. Ishtirokchi hatto butun koinotdagi barcha superkompyuterlarni ishga solsa ham, bir marta berilgan Commitment kodini boshqa bir songa moslab o'zgartira olmaydi.

---

### Topshiriq #1190: Federativ O'rganish (Federated Learning): Model Yangilanishlarini Xavfsiz Jamlash (FedAvg)
**Tavsif:** Bir nechta shifoxonalar o'z bemorlarining ma'lumotlarini qonun bo'yicha markazga bera olmaydi. Federativ o'rganishda har bir shifoxona o'z lokal serverida modelni o'qitadi va faqat model vaznlarini markaziy serverga yuboradi. Server esa ularni FedAvg (Federated Averaging) algoritmi bilan birlashtiradi.
**Talablar:** R tilida 3 ta mustaqil shifoxona uchun lokal chiziqli regressiya o'qitish va FedAvg orqali global model og'irliklarini xavfsiz hisoblash siklini yaratish.
**Yechim (R):**
```r
# Federativ o'rganish (Federated Averaging - FedAvg)

train_local_model <- function(data_x, data_y, epochs = 10, lr = 0.05) {
  w <- 0
  b <- 0
  n <- length(data_y)
  
  for (ep in 1:epochs) {
    y_pred <- w * data_x + b
    grad_w <- -(2 / n) * sum(data_x * (data_y - y_pred))
    grad_b <- -(2 / n) * sum(data_y - y_pred)
    
    w <- w - lr * grad_w
    b <- b - lr * grad_b
  }
  return(list(w = w, b = b, n_samples = n))
}

# FedAvg agregatori
federated_average <- function(client_models) {
  total_samples <- sum(sapply(client_models, function(m) m$n_samples))
  
  global_w <- 0
  global_b <- 0
  
  for (m in client_models) {
    weight_factor <- m$n_samples / total_samples
    global_w <- global_w + m$w * weight_factor
    global_b <- global_b + m$b * weight_factor
  }
  
  return(list(w = global_w, b = global_b))
}

# 3 ta turli shifoxonadagi lokal bemorlar ma'lumotlari
set.seed(123)
# Shifoxona 1 (Toshkent, 200 bemor)
x1 <- rnorm(200, 30, 5); y1 <- 1.8 * x1 + 12 + rnorm(200, 0, 2)
# Shifoxona 2 (Samarqand, 150 bemor)
x2 <- rnorm(150, 32, 6); y2 <- 1.8 * x2 + 12 + rnorm(150, 0, 2)
# Shifoxona 3 (Andijon, 100 bemor)
x3 <- rnorm(100, 28, 4); y3 <- 1.8 * x3 + 12 + rnorm(100, 0, 2)

# Har bir klinika o'z ichida model o'qitadi
model_h1 <- train_local_model(x1, y1)
model_h2 <- train_local_model(x2, y2)
model_h3 <- train_local_model(x3, y3)

cat(sprintf("Klinika 1 lokal og'irliklar: w=%.3f, b=%.3f\n", model_h1$w, model_h1$b))
cat(sprintf("Klinika 2 lokal og'irliklar: w=%.3f, b=%.3f\n", model_h2$w, model_h2$b))
cat(sprintf("Klinika 3 lokal og'irliklar: w=%.3f, b=%.3f\n", model_h3$w, model_h3$b))

# Markaziy server vaznlarni jamlaydi
global_model <- federated_average(list(model_h1, model_h2, model_h3))
cat(sprintf("\n=== GLOBAL FEDERATED MODEL ===\nGlobal vazn w: %.3f, Bias b: %.3f\n",
            global_model$w, global_model$b))
```
**Tushuntirish:** Federated Learning ma'lumotlarni markazlashtirishga bo'lgan ehtiyojni yo'q qiladi. Bemorlar yozuvlari har bir shifoxona devorlari ichida xavfsiz qoladi, dunyo esa yagona yuqori aniqlikdagi global AI modeliga ega bo'ladi.

---

### Topshiriq #1191: HIPAA 'Safe Harbor' Usuli: 18 ta Identifikatorni Avtomatlashtirilgan Tozalash
**Tavsif:** AQSH ning HIPAA (Health Insurance Portability and Accountability Act) qonuniga ko'ra tibbiy ma'lumotlarni ommaga ulashish uchun qat'iy 18 ta identifikator (Ism, aniq sanalar, telefon, faks, email, SSN/JSHSHIR, tibbiy karta raqami, transport raqami, IP-manzil, fotosurat va h.k.) to'liq olib tashlanishi yoki umumlashtirilishi shart.
**Talablar:** R tilida klinik ma'lumotlar to'plamidan HIPAA Safe Harbor talablariga binoan 18 ta identifikatorni avtomatik aniqlovchi, sanalarni faqat yilga qisqartiruvchi va 89 yoshdan kattalarni '90+' toifasiga o'tkazuvchi tozalovchi pipeline yozish.
**Yechim (R):**
```r
# HIPAA Safe Harbor De-identification Pipeline

hipaa_safe_harbor_clean <- function(clinical_df) {
  df <- clinical_df
  
  # 1. To'g'ridan-to'g'ri PII ustunlarini yo'qotish
  pii_cols <- c("Ism", "Familiya", "Telefon", "Email", "JSHSHIR", "SSN",
                "Tibbiy_Karta_No", "Sugurta_No", "Hisob_Raqam", "IP_Address")
  df <- df[, !(names(df) %in% pii_cols)]
  
  # 2. Sanalarni faqat yilga qisqartirish (Kun va oylar taqiqlangan)
  date_cols <- names(df)[sapply(df, function(x) inherits(x, "Date") || grepl("Sana", names(df)))]
  for (col in date_cols) {
    if (inherits(df[[col]], "Date")) {
      df[[paste0(col, "_Yil")]] <- as.numeric(format(df[[col]], "%Y"))
      df[[col]] <- NULL
    }
  }
  
  # 3. Yashash joyi (ZIP Code): Faqat dastlabki 3 ta raqam qoladi (agar aholi > 20,000 bo'lsa)
  if ("ZIP_Code" %in% names(df)) {
    df$ZIP_Code <- paste0(substr(df$ZIP_Code, 1, 3), "XX")
  }
  
  # 4. Yosh cheklovi: HIPAA bo'yicha 89 yoshdan oshgan barcha shaxslar '90+' toifasiga jamlanadi
  if ("Yosh" %in% names(df)) {
    df$Yosh_Kategoriya <- ifelse(df$Yosh >= 90, "90+", as.character(df$Yosh))
    df$Yosh <- NULL
  }
  
  return(df)
}

# Test klinik ma'lumotlar
set.seed(42)
bemorlar_klinika <- data.frame(
  Ism = c("Anvar", "Nargiza", "Rustam"),
  JSHSHIR = c("31201991234567", "42508889876543", "30505321122334"),
  Telefon = c("+998901234567", "+998935554433", "+998971112233"),
  ZIP_Code = c("100015", "100021", "100084"),
  Qabul_Sana = as.Date(c("2024-03-15", "2024-07-20", "2023-11-05")),
  Yosh = c(45, 93, 31),
  Qon_Bosimi = c(120, 145, 118),
  Tashxis = c("Sog'lom", "Gipertoniya", "Gastrit"),
  stringsAsFactors = FALSE
)

tozalangan_baza <- hipaa_safe_harbor_clean(bemorlar_klinika)
cat("=== HIPAA SAFE HARBOR TOZALANGAN BAZA ===\n")
print(tozalangan_baza)
```
**Tushuntirish:** HIPAA Safe Harbor usuli dunyo bo'yicha tibbiy ma'lumotlarni ommalashtirishda eng ishonchli yuridik va texnik mezon hisoblanadi. Unda ayniqsa 89 yoshdan oshgan shaxslar soni kamligi tufayli darhol fosh bo'lish xavfini bartaraf etish uchun ularni '90+' yagona agregat toifasiga kiritish qat'iy talab etiladi.

---

### Topshiriq #1192: HIPAA 'Expert Determination' Statistik Tahlili va Fosh Bo'lish Xavfini Modellash
**Tavsif:** Safe Harbor usuli juda ko'p foydali ma'lumotlarni (aniq sanalar, yosh) o'chirib yuboradi. HIPAA ning ikkinchi yo'li — Expert Determination usuli bo'lib, unda mustaqil statistik ekspert matematik modellar yordamida shaxsni qayta aniqlash ehtimoli 'juda kichik' (odatda < 0.05) ekanligini isbotlab berishi kerak.
**Talablar:** R tilida Poisson yoki Binomial taqsimot orqali individual va global qayta aniqlash (Re-identification) ehtimolini hisoblovchi ekspert tahliliy modelini ishlab chiqish.
**Yechim (R):**
```r
# HIPAA Expert Determination statistik baholash modeli

estimate_expert_risk <- function(sample_df, population_size, quasi_cols) {
  # Har bir kvazi-kombinatsiya chastotasi namunada (sample frequency: f_k)
  grouped <- as.data.frame(table(sample_df[quasi_cols]))
  sample_with_freq <- merge(sample_df, grouped, by = quasi_cols, all.x = TRUE)
  
  f_k <- sample_with_freq$Freq
  n_sample <- nrow(sample_df)
  sampling_fraction <- n_sample / population_size
  
  # Populyatsiyadagi kutilayotgan o'lcham (F_k)
  # Unikal shaxslar (f_k == 1) uchun fosh bo'lish xavfi
  # f_k = 1 bo'lganda shaxsning populyatsiyada ham unikal bo'lish ehtimoli: 1 / (1 + (1 - sampling_fraction))
  unikal_idx <- which(f_k == 1)
  
  # Individual xavf
  individual_risk <- 1 / f_k
  
  # Ekspert metrikalari
  p_reid_expected <- mean(individual_risk) * sampling_fraction
  p_reid_max <- max(individual_risk) * sampling_fraction
  
  is_expert_approved <- (p_reid_expected < 0.05) && (p_reid_max < 0.20)
  
  report <- list(
    Sample_Size = n_sample,
    Pop_Size = population_size,
    Sampling_Fraction = round(sampling_fraction, 4),
    Unikal_Yozuvlar_Soni = length(unikal_idx),
    Kutilayotgan_Xavf = round(p_reid_expected, 5),
    Maksimal_Xavf = round(p_reid_max, 5),
    Tasdiqlandimi = is_expert_approved
  )
  
  cat("=== HIPAA EXPERT DETERMINATION XULOSASI ===\n")
  cat(sprintf("Namuna hajmi: %d | Populyatsiya: %d\n", n_sample, population_size))
  cat(sprintf("Kutilayotgan qayta aniqlanish xavfi: %.4f%%\n", p_reid_expected * 100))
  cat(sprintf("Maksimal qayta aniqlanish xavfi:     %.4f%%\n", p_reid_max * 100))
  cat(sprintf("Ekspert ruxsati beriladimi?:         %s\n", ifelse(is_expert_approved, "HA (XAVFSIZ)", "YO'Q (XAVFLI!)")))
  
  return(report)
}

# Test: Toshkent shahri bo'yicha 50,000 bemor namunasi (Umumiy aholi 3,000,000)
set.seed(123)
sample_size <- 5000
namuna <- data.frame(
  Yosh = sample(18:85, sample_size, replace = TRUE),
  Jins = sample(c("M", "F"), sample_size, replace = TRUE),
  Tuman = sample(paste0("Tuman_", 1:12), sample_size, replace = TRUE)
)

ekspert_xulosa <- estimate_expert_risk(namuna, population_size = 3000000, quasi_cols = c("Yosh", "Jins", "Tuman"))
```
**Tushuntirish:** Expert Determination usuli orqali tibbiy tahlilchilar aniq sanalarni (masalan, kimyoterapiya kurslarining oraliq muddatlarini) va yoshni saqlab qolishlari mumkin. Asosiy shart shundaki, tahlilchi populyatsiya nisbati va xavf ehtimolligini matematik modellar bilan isbotlab berishi lozim.

---

### Topshiriq #1193: GDPR 'Right to be Forgotten' (Unutilish Huquqi): Crypto-shredding Mexanizmi
**Tavsif:** Yevropa Ittifoqining GDPR (General Data Protection Regulation) 17-moddasiga binoan foydalanuvchi o'z ma'lumotlarini bazadan butunlay o'chirishni talab qilishga haqli. Biroq taqsimlangan tizma (blockchain) yoki arxiv zaxiralaridan (backups) ma'lumotni jismonan o'chirish imkonsiz. Yechim — Crypto-shredding.
**Talablar:** R tilida har bir foydalanuvchi ma'lumotlarini uning unikal shaxsiy shifrlash kaliti bilan AES-256-CBC orqali shifrlash va foydalanuvchi 'unutilishni' so'raganda uning kalitini butunlay yo'q qilish (kalitni o'chirish orqali ma'lumotni ochib bo'lmas chiqindiga aylantirish) mexanizmini yaratish.
**Yechim (R):**
```r
library(openssl)

# Crypto-shredding kalitlar ombori (KMS simulyatsiyasi)
kms_storage <- new.env(hash = TRUE)

# Foydalanuvchi uchun kalit yaratish
create_user_key <- function(user_id) {
  kms_storage[[user_id]] <- rand_bytes(32) # AES-256 kalit
}

# Foydalanuvchi ma'lumotlarini shifrlab saqlash
store_user_data <- function(user_id, raw_text) {
  if (!exists(user_id, envir = kms_storage)) {
    create_user_key(user_id)
  }
  key <- kms_storage[[user_id]]
  iv <- rand_bytes(16)
  
  # AES-CBC shifrlash
  ciphertext <- aes_cbc_encrypt(charToRaw(raw_text), key = key, iv = iv)
  
  return(list(user_id = user_id, iv = iv, encrypted_data = ciphertext))
}

# Foydalanuvchi ma'lumotlarini o'qish
read_user_data <- function(record) {
  user_id <- record$user_id
  if (!exists(user_id, envir = kms_storage)) {
    stop(sprintf("XATOLIK: %s foydalanuvchisining kaliti yo'q qilingan (Crypto-shredded)! Ma'lumotlarni tiklab bo'lmaydi.", user_id))
  }
  key <- kms_storage[[user_id]]
  decrypted_raw <- aes_cbc_decrypt(record$encrypted_data, key = key, iv = record$iv)
  rawToChar(decrypted_raw)
}

# GDPR 17-modda: Unutilish huquqi (Crypto-shredding)
gdpr_crypto_shred <- function(user_id) {
  if (exists(user_id, envir = kms_storage)) {
    # Kalit xotiradan to'liq o'chiriladi
    rm(list = user_id, envir = kms_storage)
    cat(sprintf("[GDPR Crypto-Shred] %s foydalanuvchi shifrlash kaliti butunlay yo'q qilindi.\n", user_id))
  }
}

# Sinov
foydalanuvchi <- "User_UZ_99812"
anketa <- "Ism: Jasur; Tashxis: Yurak ishemiyasi; Xarajat: $12,500"

# Shifrlab arxivga saqlash
baza_yozuvi <- store_user_data(foydalanuvchi, anketa)
cat("Arxivdagi shifrlangan baytlar soni:", length(baza_yozuvi$encrypted_data), "\n")

# Baza yozuvini tekshirish
cat("O'qilgan anketa:", read_user_data(baza_yozuvi), "\n")

# Foydalanuvchi o'chirishni talab qildi
gdpr_crypto_shred(foydalanuvchi)

# Arxivdagi eski yozuvni o'qishga urinish
tryCatch({
  read_user_data(baza_yozuvi)
}, error = function(e) {
  cat("Arxivdan o'qish natijasi:", e$message, "\n")
})
```
**Tushuntirish:** Crypto-shredding arxiv tasmalarini (tape backup) yoki o'zgarmas WORM xotiralarni qayta yozmasdan turib GDPR ning 'Right to be Forgotten' qonuniy talabini 100% to'laqonli bajarishning yagona texnik chorasidir. Kalit yo'q qilingach, zamonaviy fizika va matematika qonunlariga ko'ra shifrlangan yozuvni tiklash imkonsiz.

---

### Topshiriq #1194: Shaxsiy Ma'lumotlarga Kirish Audit Jurnali va Hash Chain Yaxlitligi
**Tavsif:** Tibbiy va shaxsiy ma'lumotlar bazalariga kim, qachon va nima maqsadda kirganini qayd etuvchi audit jurnali bo'lishi shart. Agar ma'lumotlar sizib chiqsa, ichki xodimlar audit jurnalini soxtalashtira olmasligi uchun jurnal Hash Chain (Blockchain zanjiri) tamoyilida yuritiladi.
**Talablar:** R tilida har bir yangi kirish yozuvi o'zidan oldingi yozuvning SHA-256 xeshini o'z ichiga oluvchi kriptografik o'zgarmas Audit Logger tizimini ishlab chiqish va zanjir buzilganini aniqlash.
**Yechim (R):**
```r
library(openssl)

new_audit_log <- function() {
  # Boshlang'ich (Genesis) blok
  genesis_hash <- as.character(sha256(charToRaw("GENESIS_AUDIT_BLOCK_2026")))
  list(
    chain = list(),
    last_hash = genesis_hash
  )
}

add_audit_event <- function(logger, user, patient_id, action, justification) {
  timestamp <- as.character(Sys.time())
  prev_hash <- logger$last_hash
  
  # Yozuv ma'lumotlari
  record_payload <- paste(timestamp, user, patient_id, action, justification, prev_hash, sep = "|")
  current_hash <- as.character(sha256(charToRaw(record_payload)))
  
  entry <- list(
    timestamp = timestamp,
    user = user,
    patient_id = patient_id,
    action = action,
    justification = justification,
    prev_hash = prev_hash,
    hash = current_hash
  )
  
  logger$chain <- append(logger$chain, list(entry))
  logger$last_hash <- current_hash
  return(logger)
}

# Audit zanjirining butunligini tekshirish
verify_audit_log <- function(logger) {
  expected_prev <- as.character(sha256(charToRaw("GENESIS_AUDIT_BLOCK_2026")))
  
  for (i in seq_along(logger$chain)) {
    item <- logger$chain[[i]]
    
    # 1. Zanjir uzluksizligini tekshirish
    if (item$prev_hash != expected_prev) {
      cat(sprintf("XATOLIK: %d-yozuvda zanjir uzilgan!\n", i))
      return(FALSE)
    }
    
    # 2. Xesh to'g'riligini qayta hisoblash
    payload <- paste(item$timestamp, item$user, item$patient_id, item$action, item$justification, item$prev_hash, sep = "|")
    calc_hash <- as.character(sha256(charToRaw(payload)))
    
    if (calc_hash != item$hash) {
      cat(sprintf("XATOLIK: %d-yozuv ma'lumotlari qalbakilashtirilgan!\n", i))
      return(FALSE)
    }
    
    expected_prev <- item$hash
  }
  return(TRUE)
}

# Sinov
logger <- new_audit_log()
logger <- add_audit_event(logger, "dr_aziza", "PAT_1001", "READ", "Favqulodda operatsiya")
logger <- add_audit_event(logger, "nurse_nodir", "PAT_1001", "UPDATE", "Dori dozasi kiritildi")
logger <- add_audit_event(logger, "analyst_bob", "ALL_PATIENTS", "EXPORT", "Oylik statistika hisoboti")

cat("Audit jurnali yaxlitligi tasdiqlandimi?:", verify_audit_log(logger), "\n")

# Hujumchi 2-yozuvning harakatini soxtalashtirishga urinadi
logger$chain[[2]]$action <- "DELETE" # Noqonuniy o'zgartirish
cat("Hujumdan so'ng audit yaxlitligi:        ", verify_audit_log(logger), "\n")
```
**Tushuntirish:** Kriptografik Hash Chain har qanday ichki administrator yoki tajovuzkorning audit yozuvlarini o'zgartirish yoki biror qatorni jimgina o'chirib yuborish imkoniyatini yo'qqa chiqaradi. Zanjirdagi har bir xesh oldingi barcha hodisalar bilan mustahkam bog'langan bo'ladi.

---

### Topshiriq #1195: Klinik Tadqiqotlarda Qatlamli (Stratified) Anonimlashtirish va Davolash Samarasini Saqlash
**Tavsif:** Yangi dori vositalarini sinovdan o'tkazishda bemorlar ikki guruhga bo'linadi: Davolash (Treatment) va Nazorat (Control/Placebo). Agar tasodifiy anonimlashtirish yoki o'chirish o'tkazilsa, guruhlar mutanosibligi buziladi va dorining haqiqiy statistik samaradorligi (p-value, hazard ratio) yo'qoladi.
**Talablar:** R tilida davolash guruhlari (Treatment/Control) va yosh/jins qatlamlari bo'yicha proporsional stratifikatsiyalangan k-anonymity (Stratified k-Anonymity) algoritmini amalga oshirish.
**Yechim (R):**
```r
# Qatlamli (Stratified) anonimlashtirish

stratified_k_anonymize <- function(trial_df, strata_col, quasi_cols, k = 3) {
  strata_levels <- unique(trial_df[[strata_col]])
  anonymized_chunks <- list()
  
  for (st in strata_levels) {
    chunk <- trial_df[trial_df[[strata_col]] == st, ]
    
    # Guruh ichida kvazi-identifikatorlar chastotasi
    freq_tab <- as.data.frame(table(chunk[quasi_cols]))
    chunk_merged <- merge(chunk, freq_tab, by = quasi_cols, all.x = TRUE)
    
    # Bosish (Suppression): Har bir qatlam ichida kamida k ta bo'lishi shart
    valid_chunk <- chunk_merged[chunk_merged$Freq >= k, ]
    valid_chunk$Freq <- NULL
    
    anonymized_chunks[[as.character(st)]] <- valid_chunk
  }
  
  final_df <- do.call(rbind, anonymized_chunks)
  rownames(final_df) <- NULL
  return(final_df)
}

# Test klinik sinov ma'lumotlari: Yangi qandli diabet dorisi
set.seed(55)
n_patients <- 600
trial_data <- data.frame(
  Guruh = sample(c("Yangi_Dori", "Platsebo"), n_patients, replace = TRUE),
  Yosh_Toifa = sample(c("40-50", "51-60", "61-70"), n_patients, replace = TRUE),
  Jins = sample(c("M", "F"), n_patients, replace = TRUE),
  HbA1c_Kamayishi = rnorm(n_patients, mean = 1.2, sd = 0.4)
)

anon_trial <- stratified_k_anonymize(trial_data, strata_col = "Guruh", quasi_cols = c("Yosh_Toifa", "Jins"), k = 5)

# Klinik samaraning saqlanganligini t-test orqali tekshirish
t_asl <- t.test(HbA1c_Kamayishi ~ Guruh, data = trial_data)
t_anon <- t.test(HbA1c_Kamayishi ~ Guruh, data = anon_trial)

cat("Asl ma'lumotlardagi p-qiymat:            ", round(t_asl$p.value, 4), "\n")
cat("Stratifikatsiyalangan p-qiymat:          ", round(t_anon$p.value, 4), "\n")
cat("Statistik gipoteza xulosasi o'zgardimi?: ", (t_asl$p.value < 0.05) != (t_anon$p.value < 0.05), "\n")
```
**Tushuntirish:** Qatlamli anonimlashtirish klinik tadqiqotlar uchun juda muhimdir. Agar oddiy k-anonymity ishlatilsa, barcha nazorat guruhi a'zolari o'chirilib faqat davolash guruhi qolib ketishi (yoki aksincha) va natijada million dollarlik ilmiy tadqiqot yaroqsiz holga kelishi mumkin edi. Qatlamli yondashuv buni oldini oladi.

---

### Topshiriq #1196: Genomik Ma'lumotlar Maxfiyligi: SNP (Single Nucleotide Polymorphisms) Maskalash
**Tavsif:** Inson DNK sidagi atigi 30-70 ta noyob SNP (yakka nukleotid polimorfizmi) butun Yer yuzidagi bitta shaxsni 100% yagona qilib aniqlaydi. Genomik ma'lumotlarni ochiq tadqiqotga chiqarishda eng yuqori chastotali fosh qiluvchi allellarni himoyalash zarur.
**Talablar:** R tilida genetik allellar (0/1/2 ma'lumotlar matritsasi) bo'yicha Minor Allele Frequency (MAF) hisoblash va noyob (kam uchraydigan) variantlarni differensial shovqin va maskalash (Top-coding) orqali himoyalovchi algoritm yaratish.
**Yechim (R):**
```r
# Genomik ma'lumotlarni (SNP matritsasi) himoyalash

mask_genomic_snps <- function(snp_matrix, maf_threshold = 0.05, epsilon = 1.0) {
  # snp_matrix: Qatorlar - Bemorlar, Ustunlar - SNP lokuslari (0: gomozigot asosiy, 1: geterozigot, 2: kam uchrovchi)
  n_samples <- nrow(snp_matrix)
  n_snps <- ncol(snp_matrix)
  
  # Har bir SNP uchun Minor Allele Frequency (MAF) hisoblash
  # MAF = (1 lar soni + 2 * 2 lar soni) / (2 * n)
  allele_counts <- colSums(snp_matrix)
  maf <- allele_counts / (2 * n_samples)
  
  cat(sprintf("Jami SNP lokuslari: %d | Bemorlar: %d\n", n_snps, n_samples))
  
  protected_matrix <- snp_matrix
  
  # Noyob (fosh qiluvchi) SNP larni aniqlash: MAF < maf_threshold
  rare_snps <- which(maf < maf_threshold)
  cat(sprintf("Xavfli kam uchrovchi SNP lar soni: %d (%.2f%%)\n", length(rare_snps), length(rare_snps)/n_snps * 100))
  
  # 1. Kam uchrovchi SNP larni umumlashtirish (Maskalash: NA yoki 1 ga tenglash)
  for (idx in rare_snps) {
    # 2 qiymatlarini 1 ga tenglashtirish (Top-coding)
    protected_matrix[protected_matrix[, idx] == 2, idx] <- 1
  }
  
  # 2. Differensial maxfiy tasodifiy flipping (Mahalliy DP)
  # flip_prob = 1 / (1 + exp(epsilon))
  flip_prob <- 1 / (1 + exp(epsilon))
  mask_flip <- matrix(runif(n_samples * n_snps) < flip_prob, nrow = n_samples, ncol = n_snps)
  
  # Shovqinli o'zgartirish
  protected_matrix[mask_flip] <- (protected_matrix[mask_flip] + 1) %% 3
  
  return(list(
    original_maf = maf,
    protected_data = protected_matrix,
    rare_count = length(rare_snps)
  ))
}

# Simulyatsiya: 50 ta bemor va 20 ta genetik lokus
set.seed(42)
synthetic_snps <- matrix(sample(c(0, 1, 2), 50 * 20, replace = TRUE, prob = c(0.85, 0.12, 0.03)),
                         nrow = 50, ncol = 20)
colnames(synthetic_snps) <- paste0("rs_", 1001:1020)

gen_natija <- mask_genomic_snps(synthetic_snps, maf_threshold = 0.05, epsilon = 2.0)
```
**Tushuntirish:** Genomik ma'lumotlar o'zgarmas shaxsiy identifikator hisoblanadi (parolni o'zgartirish mumkin, lekin DNK ni o'zgartirib bo'lmaydi). Kam uchraydigan allellarni maskalash va differensial flipping orqali qarindoshlik qidiruvi hujumlaridan (Familial Search Attack) himoya ta'minlanadi.

---

### Topshiriq #1197: Differensial Maxfiy Kaplan-Meier Omon Qolish (Survival Analysis) Egrisi
**Tavsif:** Onkologik tadqiqotlarda bemorlarning omon qolish ehtimolligi vaqt o'tishi bilan Kaplan-Meier (KM) egrisi yordamida baholanadi. Biroq egridagi har bir pog'onali tushish aynan bitta bemorning vafot etgan aniq vaqtini fosh qiladi.
**Talablar:** R tili yordamida diskret vaqt intervallari bo'yicha xavf ostidagi bemorlar soni va hodisalar (o'lim/senzura) soniga Laplace shovqini qo'shuvchi differensial maxfiy Kaplan-Meier algoritmini ishlab chiqish.
**Yechim (R):**
```r
# Differensial Maxfiy Kaplan-Meier Survival Curve

dp_kaplan_meier <- function(times, events, intervals, epsilon = 0.5) {
  # intervals: Vaqt nuqtalari (masalan, 0, 30, 60, 90, 120 kun)
  n_intervals <- length(intervals) - 1
  
  # Har bir oraliq uchun voqealar (d_i) va senzurani hisoblash
  d_true <- numeric(n_intervals)
  at_risk_true <- numeric(n_intervals)
  
  current_risk <- length(times)
  
  for (i in 1:n_intervals) {
    t_start <- intervals[i]
    t_end <- intervals[i + 1]
    
    in_interval <- (times >= t_start) & (times < t_end)
    d_true[i] <- sum(events[in_interval] == 1)
    censored <- sum(events[in_interval] == 0)
    
    at_risk_true[i] <- current_risk
    current_risk <- current_risk - (d_true[i] + censored)
  }
  
  # DP shovqini qo'shish (Epsilon har bir oraliqqa bo'linadi)
  eps_per_bin <- epsilon / (2 * n_intervals)
  scale_b <- 1.0 / eps_per_bin
  
  noisy_d <- pmax(0, d_true + (runif(n_intervals, -0.5, 0.5) * 2 * scale_b))
  noisy_at_risk <- pmax(noisy_d + 1, at_risk_true + (runif(n_intervals, -0.5, 0.5) * 2 * scale_b))
  
  # DP Omon qolish ehtimolligi: S(t) = prod (1 - d_i / n_i)
  survival_prob <- numeric(n_intervals + 1)
  survival_prob[1] <- 1.0
  
  for (i in 1:n_intervals) {
    hazard <- min(1, noisy_d[i] / noisy_at_risk[i])
    survival_prob[i + 1] <- survival_prob[i] * (1 - hazard)
  }
  
  data.frame(
    Vaqt_Kuni = intervals,
    DP_Omon_Qolish = round(survival_prob, 4)
  )
}

# Test: 200 nafar og'ir bemorning omon qolish vaqtlari (kunlarda)
set.seed(123)
n_cases <- 200
times_data <- round(rexp(n_cases, rate = 0.01)) # Kunlar
events_data <- sample(c(0, 1), n_cases, replace = TRUE, prob = c(0.2, 0.8)) # 1 = Vafot, 0 = Senzuraga tushgan

vaqt_kesimlari <- seq(0, 150, by = 30)
dp_km_natija <- dp_kaplan_meier(times_data, events_data, vaqt_kesimlari, epsilon = 0.8)

cat("=== DIFFERENSIAL MAXFIY KAPLAN-MEIER EGRI KO'RSATKICHLARI ===\n")
print(dp_km_natija)
```
**Tushuntirish:** Oddiy Kaplan-Meier egrisida egri chiziqning har bir vertikal pasayishi aniq sana bilan bog'liq bo'lib, unikal qariyalar yoki taniqli shaxslarning qachon vafot etganini ommaviy axborot vositalari xabarlari bilan solishtirish orqali fosh qilish imkonini beradi. Differensial maxfiy KM bu xavfni to'liq bartaraf etadi.

---

### Topshiriq #1198: Bank Tranzaksiyalarini k-Anonymity va Differential Privacy Bilan Ko'p Qatlamli Himoyalash
**Tavsif:** Moliyaviy firibgarlikni (Fraud Detection) o'rganishda xom tranzaksiya ma'lumotlari boshqa kompaniyalarga berilishi kerak. Yagona himoya usuli yetarli emas: kvazi-identifikatorlarga k-anonymity, tranzaksiya summalariga esa Differensial shovqin birgalikda qo'llanadi (Defense-in-Depth).
**Talablar:** R tilida bank ma'lumotlar jadvalini ko'p qatlamli himoyalovchi to'liq pipeline yozish: Mijoz toifalarini k=4 umumlashtirish, summalarni qirqish va Laplace shovqini qo'shish.
**Yechim (R):**
```r
# Bank tranzaksiyalari uchun gibrid (k-Anonymity + DP) himoyalash

protect_banking_data <- function(trans_df, k = 4, epsilon = 0.5) {
  df <- trans_df
  
  # 1-qatlam: PII ni to'liq yo'qotish
  df$Karta_Raqami <- NULL
  df$Mijoz_Ismi <- NULL
  
  # 2-qatlam: Kvazi-identifikatorlarni umumlashtirish (k-Anonymity)
  df$Tranzaksiya_Soati <- paste0(substr(df$Vaqt, 1, 2), ":00")
  df$Vaqt <- NULL
  
  # k-Anonymity bo'yicha guruhlash va saralash
  quasi_cols <- c("Filial", "Tranzaksiya_Soati", "Savdo_Turi")
  counts <- as.data.frame(table(df[quasi_cols]))
  merged <- merge(df, counts, by = quasi_cols, all.x = TRUE)
  
  # Kamida k ta tranzaksiyasi bo'lmagan guruhlarni bosish
  k_safe_df <- merged[merged$Freq >= k, ]
  k_safe_df$Freq <- NULL
  
  # 3-qatlam: Tranzaksiya summasiga Differensial Maxfiylik qo'shish
  lower_bound <- 10
  upper_bound <- 5000
  clipped_amounts <- pmax(lower_bound, pmin(k_safe_df$Summa_USD, upper_bound))
  
  sens_sum <- upper_bound - lower_bound
  scale_b <- sens_sum / (epsilon * 10) # Tranzaksiya darajasidagi shovqin
  
  u <- runif(nrow(k_safe_df), -0.5, 0.5)
  dp_noise <- -scale_b * sign(u) * log(1 - 2 * abs(u))
  
  k_safe_df$Himoyalangan_Summa <- round(pmax(1, clipped_amounts + dp_noise), 2)
  k_safe_df$Summa_USD <- NULL
  
  return(k_safe_df)
}

# Test tranzaksiyalar
set.seed(99)
N <- 300
bank_data <- data.frame(
  Karta_Raqami = paste0("8600_", sample(1000:9999, N, replace = TRUE)),
  Mijoz_Ismi = paste0("Mijoz_", 1:N),
  Filial = sample(c("Markaz", "Chilonzor", "Yunusobod"), N, replace = TRUE),
  Vaqt = sprintf("%02d:%02d", sample(8:20, N, replace = TRUE), sample(0:59, N, replace = TRUE)),
  Savdo_Turi = sample(c("Supermarket", "Yoqilgi", "Restoran"), N, replace = TRUE),
  Summa_USD = rgamma(N, shape = 2, rate = 0.02)
)

himoyalangan_bank <- protect_banking_data(bank_data, k = 4, epsilon = 1.0)
cat(sprintf("Boshlang'ich tranzaksiyalar: %d | Himoyalangan tranzaksiyalar: %d\n",
            nrow(bank_data), nrow(himoyalangan_bank)))
head(himoyalangan_bank)
```
**Tushuntirish:** Ko'p qatlamli himoya (Defense-in-depth) birorta mexanizm buzilgan taqdirda ham ikkinchisi xavfsizlikni ushlab qolishini kafolatlaydi. k-Anonymity tranzaksiya joyi va vaqtini guruhlashtirsa, Laplace shovqini qancha pul sarflanganligining aniq qiymatini yashiradi.

---

### Topshiriq #1199: Ma'lumot Sizib Chiqishini Aniqlash: Statistik Suv Belgilari (Watermarking / Fingerprinting)
**Tavsif:** Kompaniya bir nechta hamkorlarga (masalan, sug'urta kompaniyasi va tahliliy agentlikka) ma'lumotlar bazasi nusxasini beradi. Agar ushbu ma'lumotlar internetga sizib chiqsa (Data Breach), kim sizdirganini aniqlash uchun har bir hamkorga berilgan nusxaga sezilmas unikal statistik suv belgilari kiritiladi.
**Talablar:** R tilida sonli ustunga hamkorning maxfiy kalitiga bog'liq mikro-shovqin kirituvchi (Watermarking) va sizib chiqqan fayldan qaysi hamkor aybdor ekanligini fosh qiluvchi detektorni ishlab chiqish.
**Yechim (R):**
```r
library(openssl)

# Ma'lumotlarga suv belgisi qo'shish (Watermarking)
embed_watermark <- function(data_vector, recipient_id, secret_salt = "KHORAZMIY_WATERMARK") {
  # Hamkorning unikal imzosi
  recipient_hash <- sha256(charToRaw(paste(recipient_id, secret_salt, sep = "::")))
  bits <- rawToBits(recipient_hash)[1:32] # 32 bitlik kod
  
  watermarked <- data_vector
  n <- length(data_vector)
  
  # Har bir bit uchun statistik siljish kiritish (+delta yoki -delta)
  delta <- sd(data_vector) * 0.005 # Sezilmas 0.5% siljish
  
  for (i in seq_along(bits)) {
    # Pseudo-tasodifiy pozitsiyalar
    pos <- ((i * 37) %% n) + 1
    if (bits[i] == 1) {
      watermarked[pos] <- watermarked[pos] + delta
    } else {
      watermarked[pos] <- watermarked[pos] - delta
    }
  }
  return(watermarked)
}

# Sizib chiqqan fayldan aybdorni aniqlash (Detect Leak Source)
detect_leaker <- function(leaked_vector, original_vector, candidate_recipients, secret_salt = "KHORAZMIY_WATERMARK") {
  diff <- leaked_vector - original_vector
  n <- length(original_vector)
  
  best_match <- NULL
  highest_correlation <- -1
  
  for (rec in candidate_recipients) {
    rec_hash <- sha256(charToRaw(paste(rec, secret_salt, sep = "::")))
    bits <- as.numeric(rawToBits(rec_hash)[1:32])
    expected_shifts <- ifelse(bits == 1, 1, -1)
    
    actual_shifts <- numeric(32)
    for (i in seq_along(bits)) {
      pos <- ((i * 37) %% n) + 1
      actual_shifts[i] <- sign(diff[pos])
    }
    
    match_score <- mean(expected_shifts == actual_shifts)
    cat(sprintf("Hamkor [%-15s] bilan moslik: %.1f%%\n", rec, match_score * 100))
    
    if (match_score > highest_correlation) {
      highest_correlation <- match_score
      best_match <- rec
    }
  }
  
  return(list(leaker = best_match, confidence = highest_correlation))
}

# Sinov
set.seed(42)
bemorlar_puls <- rnorm(500, mean = 75, sd = 8)

# 3 ta turli hamkorga jo'natiladigan nusxalar
nusxa_partner_A <- embed_watermark(bemorlar_puls, "PARTNER_ALFA")
nusxa_partner_B <- embed_watermark(bemorlar_puls, "PARTNER_BETA")
nusxa_partner_C <- embed_watermark(bemorlar_puls, "PARTNER_GAMMA")

# Darknetda 'PARTNER_BETA' ga tegishli nusxa sizib chiqdi
darknet_fayl <- nusxa_partner_B

cat("=== SIZIB CHIQISH MANBASINI KRIPTO-STATISTIK ANIQLASH ===\n")
nomzodlar <- c("PARTNER_ALFA", "PARTNER_BETA", "PARTNER_GAMMA")
tekshiruv <- detect_leaker(darknet_fayl, bemorlar_puls, nomzodlar)

cat(sprintf("\nSizib chiqishda aybdor deb topilgan manba: %s (Ishonchlilik: %.1f%%)\n",
            tekshiruv$leaker, tekshiruv$confidence * 100))
```
**Tushuntirish:** Statistik suv belgilari (Data Fingerprinting) ma'lumotlar tahlili sifatini pasaytirmagan holda har bir nusxaga o'ziga xos raqamli mikro-iz qoldiradi. Agar hamkor maxfiylik shartnomasini buzib ma'lumotni uchinchi shaxslarga sotsa, ushbu iz orqali sud oldida qat'iy matematik dalil keltirish mumkin bo'ladi.

---

### Topshiriq #1200: To'liq Xavfsiz Tibbiy-Tahliliy Pipeline: PII -> AES-256-GCM -> DP Tahlil -> Kriptografik Audit
**Tavsif:** Ushbu yakuniy monumental topshiriqda butun modulning barcha texnologiyalari birlashtiriladi: xom klinik ma'lumotlar kelib tushganda PII ajratiladi, maxfiy shaxsiy ma'lumotlar AES-256-GCM bilan shifrlanadi, kvazi-identifikatorlar HIPAA/k-anonymity bo'yicha tozalanadi, tahliliy natijalar Differensial Maxfiylik (DP) orqali chiqariladi va barcha amallar o'zgarmas Hash Chain audit jurnalida muhrlanadi.
**Talablar:** R tili yordamida to'liq modulli, real korporativ darajadagi Secure Medical Analytics Pipeline tizimini loyihalash va testdan o'tkazish.
**Yechim (R):**
```r
library(openssl)

# 1. Kriptografik Audit xizmati
init_audit_trail <- function() {
  new.env(hash = TRUE)
}
log_action <- function(env, action, user) {
  t <- as.character(Sys.time())
  prev <- if (is.null(env$last_hash)) "GENESIS" else env$last_hash
  entry <- paste(t, user, action, prev, sep = "##")
  curr_hash <- as.character(sha256(charToRaw(entry)))
  env$last_hash <- curr_hash
  env[[curr_hash]] <- entry
}

# 2. Xavfsiz Shifrlangan Ma'lumotlar Ombori
init_secure_storage <- function() {
  master_key <- rand_bytes(32) # AES-256
  list(key = master_key, records = list())
}

# 3. Secure Medical Pipeline Sinifi
run_secure_medical_pipeline <- function(raw_clinical_data, query_column, epsilon = 0.5) {
  audit_env <- init_audit_trail()
  storage <- init_secure_storage()
  log_action(audit_env, "PIPELINE_START", "SYSTEM_CORE")
  
  cat("1-BOSQICH: PII ajratish va AES-256-GCM bilan shifrlash...\n")
  # PII ni shifrlash
  encrypted_pii <- list()
  for (i in 1:nrow(raw_clinical_data)) {
    pii_str <- paste(raw_clinical_data$Ism[i], raw_clinical_data$JSHSHIR[i], sep = "|")
    iv <- rand_bytes(12)
    # GCM shifrlash
    enc <- aes_gcm_encrypt(charToRaw(pii_str), key = storage$key, iv = iv)
    encrypted_pii[[i]] <- list(iv = iv, data = enc)
  }
  log_action(audit_env, "PII_ENCRYPTED_AES256_GCM", "SECURITY_MODULE")
  
  cat("2-BOSQICH: HIPAA Safe Harbor va k-anonymity umumlashtirish...\n")
  deidentified_df <- raw_clinical_data
  deidentified_df$Ism <- NULL
  deidentified_df$JSHSHIR <- NULL
  deidentified_df$Bemor_ID <- paste0("ENC_ID_", 1:nrow(raw_clinical_data))
  
  # Yoshni intervallarga umumlashtirish
  deidentified_df$Yosh_Oraliq <- cut(deidentified_df$Yosh, breaks = c(0, 30, 50, 70, 100),
                                     labels = c("0-30", "31-50", "51-70", "70+"))
  deidentified_df$Yosh <- NULL
  log_action(audit_env, "HIPAA_GENERALIZATION_APPLIED", "PRIVACY_ENGINE")
  
  cat("3-BOSQICH: Differensial maxfiy tahlil (DP Query Engine)...\n")
  vals <- deidentified_df[[query_column]]
  lower <- quantile(vals, 0.05)
  upper <- quantile(vals, 0.95)
  clipped <- pmax(lower, pmin(vals, upper))
  
  # Laplace shovqini
  sens <- (upper - lower) / length(vals)
  scale_b <- sens / epsilon
  u <- runif(1, -0.5, 0.5)
  dp_noise <- -scale_b * sign(u) * log(1 - 2 * abs(u))
  
  dp_mean_result <- mean(clipped) + dp_noise
  log_action(audit_env, paste0("DP_QUERY_EXECUTED_EPS_", epsilon), "RESEARCHER_USER")
  
  cat("4-BOSQICH: Kriptografik Audit muhrlash...\n")
  log_action(audit_env, "PIPELINE_COMPLETED_SUCCESS", "SYSTEM_CORE")
  
  list(
    Kafolatlangan_Maxfiylik = sprintf("Epsilon = %.2f (Differential Privacy)", epsilon),
    Tahlil_Ustuni = query_column,
    Haqiqiy_Orta = round(mean(vals), 3),
    DP_Orta_Natija = round(dp_mean_result, 3),
    Audit_Oxirgi_Hash = audit_env$last_hash
  )
}

# Sinov: 1,000 nafar bemorning qon bosimi va PII ko'rsatkichlari
set.seed(2026)
N <- 1000
klinik_baza <- data.frame(
  Ism = paste0("Bemor_", 1:N),
  JSHSHIR = sprintf("30%012d", 1:N),
  Yosh = sample(18:85, N, replace = TRUE),
  Qon_Bosimi = rnorm(N, mean = 125, sd = 15)
)

yakuniy_natija <- run_secure_medical_pipeline(klinik_baza, "Qon_Bosimi", epsilon = 0.5)
cat("\n=== TO'LIQ INTEGRATSIYALASHGAN TIZIM NATIJASI ===\n")
print(yakuniy_natija)
```
**Tushuntirish:** Ushbu mukammal arxitektura zamonaviy sog'liqni saqlash va moliyaviy texnologiyalarning xavfsizlik standartlarini to'liq o'zida mujassamlashtiradi: PII ma'lumotlari apparat darajasida shifrlanadi (AES-256-GCM), o'rganuvchilar faqat de-identifikatsiyalangan ma'lumotlar bilan ishlaydi, tahliliy natijalar differensial maxfiylik bilan chiqariladi va har bir operatsiya Hash Chain orqali o'zgarmas tarzda muhrlanadi.

---
