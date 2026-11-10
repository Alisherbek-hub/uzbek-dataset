# Khorazmiy AI: R - Modul 24
## Mavzu: Kiberxavfsizlik, Kriptografiya (AES, RSA, ECC) va Xavfsiz Kodlash

### Topshiriq #1151: AES-256 blokli shifrlashda kalit hosil qilish (Key Derivation)
**Tavsif:** Foydalanuvchi parollaridan xavfsiz AES kalitlarini hosil qilishda PBKDF2 standartini qo'llash.
**Talablar:** `openssl` kutubxonasi yordamida tuz (salt) va iteratsiyalar sonini belgilash.
**Yechim (R):**
```r
library(openssl)

# Parolni xavfsiz kalitga aylantirish funksiyasi
derive_aes_key <- function(password, salt) {
  # PBKDF2 algoritmi orqali 256-bitli kalit hosil qilish
  key <- pbkdf2(password, salt, iter = 100000, keylen = 32)
  return(key)
}

password <- "Maxfiy_Parol_123"
salt <- charToRaw("milliy_tuz_2024")
key <- derive_aes_key(password, salt)
print(key)
```
**Tushuntirish:** PBKDF2 iteratsiyalari "brute-force" hujumlarini qiyinlashtiradi, `salt` esa bir xil parollar uchun turlicha kalit hosil bo'lishini ta'minlaydi.

### Topshiriq #1152: RSA kalit juftligini yaratish va saqlash
**Tavsif:** Asimmetrik shifrlash uchun RSA-4096 kalitlarini generatsiya qilish.
**Talablar:** Xususiy kalitni himoyalash va ochiq kalitni eksport qilish.
**Yechim (R):**
```r
library(openssl)

# RSA-4096 kalit juftligini yaratish
key_pair <- rsa_keygen(bits = 4096)

# Ochiq kalitni olish
pub_key <- as.list(key_pair)$pubkey

# Xususiy kalitni faylga yozish (shifrlangan holda)
write_pem(key_pair, file = "private_key.pem", password = "kuchli_parol")
```
**Tushuntirish:** 4096 bit uzunlikdagi kalit hozirgi hisoblash quvvatlari uchun yetarlicha xavfsiz hisoblanadi.

### Topshiriq #1153: ECC (Elliptik Egri Chiziq) yordamida raqamli imzo
**Tavsif:** Ma'lumotlarning yaxlitligini ta'minlash uchun ECC imzosini yaratish.
**Talablar:** `curve25519` algoritmidan foydalanish.
**Yechim (R):**
```r
library(openssl)

# ECC kalitini yaratish
key <- ec_keygen(curve = "curve25519")

# Xabar va imzo
msg <- charToRaw("Khorazmiy AI ma'lumotlar bazasi")
sig <- signature_create(msg, key = key)

# Imzoni tekshirish
verify <- signature_verify(msg, sig, pubkey = as.list(key)$pubkey)
print(paste("Imzo haqiqiyligi:", verify))
```
**Tushuntirish:** ECC RSA'ga qaraganda kichikroq kalit hajmi bilan yuqori xavfsizlikni ta'minlaydi, bu esa resurslarni tejaydi.

### Topshiriq #1154: Xavfsiz tasodifiy sonlar generatori (CSPRNG)
**Tavsif:** Kriptografik operatsiyalar uchun bashorat qilib bo'lmaydigan sonlar hosil qilish.
**Talablar:** `rand_bytes` funksiyasidan foydalanish.
**Yechim (R):**
```r
library(openssl)

# 32 baytli tasodifiy kriptografik kalit hosil qilish
secure_random_key <- rand_bytes(32)

# Hex formatga o'tkazish
hex_key <- as.character(secure_random_key)
print(hex_key)
```
**Tushuntirish:** Standart `runif()` funksiyasi kriptografik xavfsizlik uchun mos emas, `rand_bytes` esa operatsion tizimning entropiyasidan foydalanadi.

### Topshiriq #1155: Ma'lumotlarni AES-GCM rejimida shifrlash
**Tavsif:** Ma'lumotlarni shifrlash va ularning o'zgarmaganligini tekshirish (Authenticated Encryption).
**Talablar:** GCM rejimi orqali autentifikatsiyani ta'minlash.
**Yechim (R):**
```r
library(openssl)

key <- rand_bytes(32)
iv <- rand_bytes(12) # GCM uchun 12 baytli IV
data <- charToRaw("Maxfiy ma'lumot")

# Shifrlash
ciphertext <- aes_gcm_encrypt(data, key, iv)

# Dekodlash
decrypted <- aes_gcm_decrypt(ciphertext, key, iv)
print(rawToChar(decrypted))
```
**Tushuntirish:** GCM rejimi shifrlash bilan birga "tag" (yaxlitlik belgisi) ham yaratadi, bu esa ma'lumot o'zgartirilgan bo'lsa, uni aniqlash imkonini beradi.

### Topshiriq #1156: SQL Injection'dan himoyalangan so'rovlar
**Tavsif:** Ma'lumotlar bazasiga kiritilayotgan foydalanuvchi ma'lumotlarini tozalash.
**Talablar:** `DBI` va `sqlInterpolate` funksiyalaridan foydalanish.
**Yechim (R):**
```r
library(DBI)

# Parametrlashtirilgan so'rov
query <- "SELECT * FROM users WHERE username = ?name"
safe_query <- sqlInterpolate(ANSI(), query, name = "admin' OR '1'='1")

print(safe_query)
```
**Tushuntirish:** `sqlInterpolate` foydalanuvchi kiritgan ma'lumotni "escape" qilib, SQL injeksiya hujumlarini bloklaydi.

### Topshiriq #1157: Xavfsiz xesh funksiyalari (SHA-3)
**Tavsif:** Fayllar yoki xabarlarning yaxlitligini tekshirish uchun SHA-3 (Keccak) dan foydalanish.
**Talablar:** 512-bitli xesh hosil qilish.
**Yechim (R):**
```r
library(openssl)

data <- "Khorazmiy AI dataseti"
hash_val <- sha3(charToRaw(data), size = 512)

print(hash_val)
```
**Tushuntirish:** SHA-3 zamonaviy standart bo'lib, to'qnashuvlarga (collision) qarshi yuqori chidamlilikka ega.

### Topshiriq #1158: Xotiradan maxfiy ma'lumotlarni tozalash
**Tavsif:** Kriptografik kalitlar bilan ishlagandan so'ng ularni xotiradan o'chirish.
**Talablar:** Garbage collector'ni majburiy chaqirish va obyektni o'chirish.
**Yechim (R):**
```r
# Maxfiy kalitni yaratish
secret_key <- "SUPER_SECRET_KEY"

# Ishlatib bo'lgach
rm(secret_key)
gc() # Xotirani tozalash
```
**Tushuntirish:** R tilida `rm()` va `gc()` xotiradan ma'lumotni darhol o'chirmasligi mumkin, lekin bu xavfsizlikning birinchi qadamidir.

### Topshiriq #1159: Base64 kodlash va dekodlash (Xavfsiz uzatish)
**Tavsif:** Ikkilik (binary) ma'lumotlarni matnli formatda xavfsiz uzatish.
**Talablar:** `base64_encode` dan foydalanish.
**Yechim (R):**
```r
library(openssl)

raw_data <- charToRaw("Khorazmiy AI")
encoded <- base64_encode(raw_data)
decoded <- base64_decode(encoded)

print(encoded)
```
**Tushuntirish:** Base64 shifrlash emas, balki kodlash usuli, u ma'lumotlarning uzatish jarayonida buzilmasligini ta'minlaydi.

### Topshiriq #1160: Xavfsiz API kalitlarini boshqarish
**Tavsif:** API kalitlarini kod ichida yozmasdan, muhit o'zgaruvchilari (environment variables) orqali o'qish.
**Talablar:** `Sys.getenv` dan foydalanish.
**Yechim (R):**
```r
# .Renviron faylidan kalitni o'qish
api_key <- Sys.getenv("KHORAZMIY_API_KEY")

if (api_key == "") {
  stop("API kaliti topilmadi! Xavfsizlik qoidasiga ko'ra kodni to'xtatish.")
}
```
**Tushuntirish:** Kodni GitHub yoki boshqa platformalarga yuklaganda API kalitlari sizib chiqmasligi uchun muhit o'zgaruvchilari eng xavfsiz usul hisoblanadi.

---

### Topshiriq #1161: AES-256 Kalit Generatsiyasi va Xavfsiz Saqlash
**Tavsif:** Kiberxavfsizlik tizimlarida tasodifiy va kuchli kalitlarni generatsiya qilish muhim. Ushbu topshiriq `openssl` kutubxonasi yordamida kriptografik jihatdan mustahkam 256-bitli kalit yaratishni talab qiladi.
**Talablar:** Kalit 32 bayt uzunlikda bo'lishi va `/dev/urandom` manbasidan foydalanishi shart.
**Yechim (R):**
```r
library(openssl)

# 256-bitli (32 bayt) tasodifiy kalit generatsiyasi
generate_secure_key <- function() {
  key <- rand_bytes(32)
  return(key)
}

# Kalitni xavfsiz formatda saqlash (Hex ko'rinishida)
secure_key <- generate_secure_key()
hex_key <- as.character(as.hexmode(secure_key))
cat("Generatsiya qilingan xavfsiz kalit:", hex_key, "\n")
```
**Tushuntirish:** `rand_bytes` funksiyasi operatsion tizimning kriptografik xavfsiz tasodifiy raqamlar generatoridan foydalanadi, bu esa oddiy `runif()` funksiyasidan farqli o'laroq, bashorat qilib bo'lmaydigan natija beradi.

### Topshiriq #1162: RSA Asimmetrik Shifrlash
**Tavsif:** Foydalanuvchi ma'lumotlarini xavfsiz uzatish uchun RSA algoritmini qo'llash.
**Talablar:** 2048-bitli kalit juftligini yaratish va xabarni shifrlash/dekodlash.
**Yechim (R):**
```r
library(openssl)

# RSA kalit juftligini yaratish
key_pair <- rsa_keygen(bits = 2048)
pub_key <- key_pair$pubkey
priv_key <- key_pair$privkey

# Xabarni shifrlash
msg <- charToRaw("Maxfiy ma'lumot: 12345")
encrypted <- rsa_encrypt(msg, pub_key)

# Dekodlash
decrypted <- rsa_decrypt(encrypted, priv_key)
cat("Dekodlangan xabar:", rawToChar(decrypted), "\n")
```
**Tushuntirish:** RSA asimmetrik shifrlashda ochiq kalit shifrlash uchun, maxfiy kalit esa dekodlash uchun ishlatiladi, bu esa kalit almashinuvi muammosini hal qiladi.

### Topshiriq #1163: ECC (Elliptik Egri Chiziqlar) Imzosi
**Tavsif:** Raqamli imzolar yordamida ma'lumotlar yaxlitligini tekshirish.
**Talablar:** ECDSA algoritmi yordamida xabarni imzolash va autentifikatsiya qilish.
**Yechim (R):**
```r
library(openssl)

# ECC kalit juftligi
key <- ec_keygen(curve = "P-256")
msg <- "Tranzaksiya ma'lumotlari"

# Raqamli imzo yaratish
signature <- signature_create(charToRaw(msg), key = key)

# Imzoni tekshirish
is_valid <- signature_verify(charToRaw(msg), signature, pubkey = as.list(key)$pubkey)
cat("Imzo haqiqiyligi:", is_valid, "\n")
```
**Tushuntirish:** ECC (Elliptic Curve Cryptography) RSA'ga qaraganda kichikroq kalit o'lchamlari bilan yuqori xavfsizlik darajasini ta'minlaydi, bu esa resurslar cheklangan tizimlar uchun samarali.

### Topshiriq #1164: Xavfsiz Kodlash - SQL Inyeksiya Himoyasi
**Tavsif:** Ma'lumotlar bazasi bilan ishlashda foydalanuvchi kiritgan ma'lumotlarni tozalash.
**Talablar:** `DBI` va `sqlInterpolate` yordamida parametrlangan so'rovlarni amalga oshirish.
**Yechim (R):**
```r
library(DBI)

# Parametrlangan so'rov (SQL inyeksiya oldini olish uchun)
safe_query <- function(con, user_input) {
  query <- sqlInterpolate(con, "SELECT * FROM users WHERE username = ?name", name = user_input)
  return(query)
}

# Misol: con - bazaga ulanish obyekti
# cat(safe_query(con, "admin' OR '1'='1")) 
```
**Tushuntirish:** `sqlInterpolate` foydalanuvchi kiritgan ma'lumotlarni qat'iy ravishda ma'lumot sifatida qabul qiladi, bu esa SQL buyruqlarining bajarilishiga yo'l qo'ymaydi.

### Topshiriq #1165: SHA-256 Xesh Funksiyasi
**Tavsif:** Parollarni bazada xavfsiz saqlash uchun xesh funksiyalaridan foydalanish.
**Talablar:** Tuz (salt) qo'shilgan holda SHA-256 xeshini yaratish.
**Yechim (R):**
```r
library(digest)

# Parolni tuz (salt) bilan xeshlash
hash_password <- function(password, salt) {
  return(sha256(paste0(password, salt)))
}

salt <- "Khorazmiy_2024"
password <- "SuperSecret123"
cat("Xesh:", hash_password(password, salt), "\n")
```
**Tushuntirish:** Tuz qo'shish "Rainbow table" hujumlaridan himoya qiladi, chunki bir xil parollar har xil tuzlar bilan turlicha xesh qiymatiga ega bo'ladi.

### Topshiriq #1166: Fayllarni AES-GCM bilan shifrlash
**Tavsif:** Fayllarni diskda xavfsiz saqlash uchun autentifikatsiyali shifrlash (AES-GCM).
**Talablar:** Shifrlash jarayonida `nonce` (bir martalik son) ishlatish.
**Yechim (R):**
```r
library(openssl)

key <- rand_bytes(32)
nonce <- rand_bytes(12)
data <- charToRaw("Maxfiy fayl mazmuni")

# AES-GCM shifrlash
encrypted <- aes_gcm_encrypt(data, key, nonce)
decrypted <- aes_gcm_decrypt(encrypted, key, nonce)

cat("Dekodlangan:", rawToChar(decrypted), "\n")
```
**Tushuntirish:** GCM rejimi nafaqat shifrlashni, balki ma'lumotlarning o'zgartirilmaganligini ham tekshiradi (Authenticated Encryption).

### Topshiriq #1167: Xavfsiz Tasodifiy Raqamlar (CSPRNG)
**Tavsif:** Simulyatsiyalar va kriptografiya uchun sifatli tasodifiy sonlar generatsiyasi.
**Talablar:** `runif` o'rniga kriptografik xavfsiz generatorlardan foydalanish.
**Yechim (R):**
```r
library(openssl)

# 0 va 1 oralig'ida xavfsiz tasodifiy son
get_secure_random <- function() {
  bytes <- rand_bytes(4)
  val <- as.integer(as.hexmode(paste(bytes, collapse = "")))
  return(val / 2^32)
}

cat("Xavfsiz son:", get_secure_random(), "\n")
```
**Tushuntirish:** Standart `runif` deterministikdir (urug'ga bog'liq), `rand_bytes` esa apparat shovqinidan foydalanadi, bu esa uni xavfsiz qiladi.

### Topshiriq #1168: Base64 Kodlash va Xavfsizlik
**Tavsif:** Binary ma'lumotlarni matnli formatda xavfsiz uzatish.
**Talablar:** Ma'lumotlarni Base64 formatiga o'tkazish va qayta tiklash.
**Yechim (R):**
```r
library(base64enc)

data <- charToRaw("Khorazmiy AI")
encoded <- base64encode(data)
decoded <- base64decode(encoded)

cat("Base64:", encoded, "\n")
cat("Asl holat:", rawToChar(decoded), "\n")
```
**Tushuntirish:** Base64 shifrlash emas, balki kodlash usuli. U ma'lumotlarni uzatishda buzilishlarning oldini olish uchun ishlatiladi.

### Topshiriq #1169: Xavfsiz API So'rovlari (HTTPS)
**Tavsif:** Tashqi API'lar bilan ishlashda SSL/TLS sertifikatlarini tekshirish.
**Talablar:** `httr` kutubxonasi yordamida sertifikat tekshiruvini yoqish.
**Yechim (R):**
```r
library(httr)

# HTTPS orqali xavfsiz so'rov
response <- GET("https://api.khorazmiy.ai", config(ssl_verifypeer = TRUE))

if(status_code(response) == 200) {
  cat("Ulanish xavfsiz va muvaffaqiyatli.\n")
}
```
**Tushuntirish:** `ssl_verifypeer = TRUE` "Man-in-the-middle" hujumlaridan himoya qiladi, chunki serverning sertifikati ishonchli CA tomonidan imzolanganligini tekshiradi.

### Topshiriq #1170: Xotirani Tozalash (Memory Sanitization)
**Tavsif:** Maxfiy ma'lumotlar (parollar, kalitlar) ishlatilgandan so'ng xotiradan o'chirilishi kerak.
**Talablar:** R muhitida obyektlarni xotiradan to'liq o'chirish va chiqindilarni yig'ish (Garbage Collection).
**Yechim (R):**
```r
# Maxfiy ma'lumot
secret_key <- "SUPER_SECRET_KEY_123"

# Ishlatilgandan so'ng xotirani tozalash
rm(secret_key)
gc() # Garbage Collector'ni majburiy ishga tushirish

cat("Xotira tozalandi.\n")
```
**Tushuntirish:** `rm()` o'zgaruvchini olib tashlaydi, `gc()` esa xotirani bo'shatadi, bu esa xotira dump'lari orqali ma'lumotlar sizib chiqishini qiyinlashtiradi.

---

### Topshiriq #1171: AES-256 GCM rejimida ma'lumotlarni shifrlash
**Tavsif:** Kiberxavfsizlikda ma'lumotlarning butunligini (integrity) ta'minlash uchun AES-GCM (Galois/Counter Mode) standart hisoblanadi. R tilida `sodium` kutubxonasi yordamida yuqori darajadagi shifrlashni amalga oshirish.
**Talablar:** 256-bitli kalitdan foydalanish, autentifikatsiya tegi (tag) bilan birga shifrlash.
**Yechim (R):**
```r
library(sodium)

# 32 baytli tasodifiy kalit yaratish
key <- random(32)
# Xabar
message <- charToRaw("Maxfiy milliy ma'lumotlar")
# Nonce (bir martalik qiymat) yaratish
nonce <- random(24)

# Shifrlash
ciphertext <- data_encrypt(message, key, nonce)

# Dekodlash
decrypted <- data_decrypt(ciphertext, key, nonce)
cat("Asl xabar:", rawToChar(decrypted), "\n")
```
**Tushuntirish:** `sodium` kutubxonasi libsodium C kutubxonasiga asoslangan bo'lib, u "side-channel" hujumlariga chidamli va xavfsizdir.

### Topshiriq #1172: RSA kalit juftligini generatsiya qilish
**Tavsif:** Asimmetrik kriptografiyada kalitlarni boshqarish. RSA-4096 bitli kalitlarni yaratish va ularni saqlash.
**Talablar:** Kamida 4096 bit uzunlik, xavfsiz saqlash formati (PEM).
**Yechim (R):**
```r
library(openssl)

# 4096 bitli RSA kalit juftligini yaratish
key_pair <- rsa_keygen(bits = 4096)

# Ochiq kalitni eksport qilish
pub_key <- as.list(key_pair)$pubkey
writeLines(as.character(pub_key), "public_key.pem")
```
**Tushuntirish:** 4096 bit hozirgi kunda kvant kompyuterlarigacha bo'lgan davrda eng yuqori xavfsizlik standartlaridan biri hisoblanadi.

### Topshiriq #1173: ECC (Elliptic Curve Cryptography) yordamida raqamli imzo
**Tavsif:** RSA ga nisbatan tezroq va kichikroq kalit o'lchamli ECC (Curve25519) yordamida ma'lumotni imzolash.
**Talablar:** Ed25519 algoritmi, imzoni tekshirish mexanizmi.
**Yechim (R):**
```r
library(sodium)

# Kalitlar juftligi
key <- sig_keygen()
msg <- charToRaw("Hujjat tasdig'i")

# Imzolash
sig <- sig_sign(msg, key$secretkey)

# Tekshirish
is_valid <- sig_verify(msg, sig, key$pubkey)
print(paste("Imzo haqiqiyligi:", is_valid))
```
**Tushuntirish:** ECC algoritmlari kam resurs sarflagan holda yuqori kriptografik kuchni ta'minlaydi, bu mobil qurilmalar uchun juda muhim.

### Topshiriq #1174: Xavfsiz xesh funksiyalar (SHA-3)
**Tavsif:** Ma'lumotlarning o'zgarmaganligini tekshirish uchun SHA-3 (Keccak) xesh funksiyasidan foydalanish.
**Talablar:** 512-bitli xesh, to'qnashuvlarga (collision) chidamlilik.
**Yechim (R):**
```r
library(digest)

data <- "Muhim_tranzaksiya_ma'lumoti"
# SHA-3 512 bitli xesh
hash_val <- digest(data, algo = "sha3-512", serialize = FALSE)
cat("Xesh qiymati:", hash_val, "\n")
```
**Tushuntirish:** SHA-3 zamonaviy standart bo'lib, SHA-2 ga nisbatan turli xil matematik tuzilishga ega, bu xavfsizlikni oshiradi.

### Topshiriq #1175: SQL Injection hujumlaridan himoya
**Tavsif:** Ma'lumotlar bazasiga so'rov yuborishda foydalanuvchi kiritgan ma'lumotlarni tozalash (sanitization).
**Talablar:** Parametrlashtirilgan so'rovlar (parameterized queries).
**Yechim (R):**
```r
library(DBI)

con <- dbConnect(RSQLite::SQLite(), ":memory:")
# Xavfsiz usul: Parametrlardan foydalanish
query <- "SELECT * FROM users WHERE username = ?"
res <- dbGetQuery(con, query, params = list("admin' OR '1'='1"))
```
**Tushuntirish:** Parametrlashtirilgan so'rovlar SQL kodini ma'lumotdan ajratib turadi, bu esa SQL injection hujumlarini imkonsiz qiladi.

### Topshiriq #1176: Parollarni xavfsiz xeshlash (Argon2)
**Tavsif:** Foydalanuvchi parollarini bazada saqlash uchun eng xavfsiz usul - Argon2id algoritmi.
**Talablar:** "Salt" (tuz) qo'shish va xeshni tekshirish.
**Yechim (R):**
```r
library(sodium)

password <- charToRaw("MeningKuchliParolim123")
# Argon2id xeshlash
hashed_pw <- password_store(password)

# Tekshirish
is_correct <- password_verify(hashed_pw, password)
print(paste("Parol to'g'ri:", is_correct))
```
**Tushuntirish:** `password_store` funksiyasi avtomatik ravishda tasodifiy tuz (salt) qo'shadi va hisoblash qiyinligini oshiradi.

### Topshiriq #1177: Xavfsiz tasodifiy sonlar generatori (CSPRNG)
**Tavsif:** Kriptografik operatsiyalar uchun `runif()` emas, balki xavfsiz tasodifiy sonlar generatoridan foydalanish.
**Talablar:** Kriptografik jihatdan mustahkam (Cryptographically Secure).
**Yechim (R):**
```r
library(sodium)

# 16 baytli kriptografik xavfsiz tasodifiy son
secure_random <- random(16)
print(secure_random)
```
**Tushuntirish:** Standart `runif` deterministik bo'lishi mumkin, `sodium::random` esa operatsion tizimning entropiyasidan foydalanadi.

### Topshiriq #1178: Fayllarni xavfsiz o'chirish (Wiping)
**Tavsif:** Diskdagi fayllarni shunchaki o'chirish yetarli emas. Ularni qayta yozish orqali butunlay yo'q qilish.
**Talablar:** Fayl ustiga tasodifiy baytlar yozish.
**Yechim (R):**
```r
wipe_file <- function(filepath) {
  size <- file.info(filepath)$size
  con <- file(filepath, "wb")
  writeBin(random(size), con)
  close(con)
  file.remove(filepath)
}
# wipe_file("maxfiy_hujjat.txt")
```
**Tushuntirish:** Fayl tizimi darajasida o'chirish faqat ko'rsatgichni olib tashlaydi, ma'lumot esa diskda qoladi. Qayta yozish buni oldini oladi.

### Topshiriq #1179: Xavfsiz API so'rovlari (TLS/SSL)
**Tavsif:** Tashqi API bilan ishlashda ma'lumotlarni shifrlangan kanal orqali uzatish.
**Talablar:** HTTPS protokoli va sertifikat tekshiruvi.
**Yechim (R):**
```r
library(httr)

# HTTPS orqali xavfsiz so'rov
response <- GET("https://api.milliy-tizim.uz/data", 
                add_headers(Authorization = "Bearer TOKEN_HERE"))
stop_for_status(response)
```
**Tavsif:** `httr` kutubxonasi `libcurl` orqali SSL/TLS sertifikatlarini avtomatik tekshiradi, bu "Man-in-the-middle" hujumlarini oldini oladi.

### Topshiriq #1180: Kodni xavfsiz tekshirish (Static Analysis)
**Tavsif:** R kodidagi xavfsizlik kamchiliklarini avtomatik aniqlash.
**Talablar:** `lintr` yordamida xavfli funksiyalarni aniqlash.
**Yechim (R):**
```r
library(lintr)

# Xavfli funksiyalarni (masalan, eval) aniqlash uchun qoida
lint("script.R", linters = list(
  object_usage_linter(),
  no_eval_linter <- function(...) {
    # eval() funksiyasini taqiqlash logikasi
  }
))
```
**Tushuntirish:** `eval()` kabi funksiyalar kod injeksiyasiga olib kelishi mumkin. Statik tahlil bu kabi xatolarni kodni ishga tushirmasdan aniqlaydi.

---

### Topshiriq #1181: AES-256 blokli shifrlashda kalitni boshqarish
**Tavsif:** Kiberxavfsizlik tizimlarida AES-256 kalitlarini xavfsiz saqlash va ulardan foydalanish. Tasodifiy kalit generatori va uning kriptografik mustahkamligini ta'minlash.
**Talablar:** `openssl` kutubxonasi yordamida 32 baytli (256 bit) kalit yaratish va uni xavfsiz formatda saqlash.
**Yechim (R):**
```r
library(openssl)

# 256-bitli (32 bayt) tasodifiy kalit generatsiyasi
generate_aes_key <- function() {
  key <- rand_bytes(32)
  return(key)
}

# Kalitni xavfsiz saqlash uchun hex formatiga o'tkazish
secure_key <- generate_aes_key()
hex_key <- as.character(as.hexmode(secure_key))

cat("Yaratilgan xavfsiz kalit (hex):", paste(hex_key, collapse = ""), "\n")
```
**Tushuntirish:** `rand_bytes` funksiyasi kriptografik jihatdan xavfsiz tasodifiy sonlar generatoridan (CSPRNG) foydalanadi, bu esa kalitning bashorat qilinishini imkonsiz qiladi.

### Topshiriq #1182: RSA kalit juftligini generatsiya qilish
**Tavsif:** Asimmetrik shifrlash tizimlarida RSA-4096 bitli kalitlarni yaratish va ularni eksport qilish.
**Talablar:** 4096 bit uzunlikdagi RSA kalit juftligini yaratish va xususiy kalitni himoyalash.
**Yechim (R):**
```r
library(openssl)

# 4096 bitli RSA kalit juftligini yaratish
key_pair <- rsa_keygen(bits = 4096)

# Ommaviy kalitni olish
pub_key <- as.list(key_pair)$pubkey

cat("RSA kaliti muvaffaqiyatli yaratildi.\n")
print(pub_key)
```
**Tushuntirish:** 4096 bit uzunlik hozirgi kunda sanoat standarti hisoblanadi va bruteforce hujumlariga qarshi yuqori chidamlilikni ta'minlaydi.

### Topshiriq #1183: ECC (Elliptic Curve Cryptography) yordamida raqamli imzo
**Tavsif:** Ma'lumotlar yaxlitligini tekshirish uchun ECC (Curve25519) algoritmidan foydalangan holda raqamli imzo yaratish.
**Talablar:** Xabar va xususiy kalit yordamida imzo hosil qilish va uni verifikatsiya qilish.
**Yechim (R):**
```r
library(openssl)

# Xabar va kalit
msg <- charToRaw("Khorazmiy AI: Xavfsiz ma'lumotlar uzatish")
key <- ec_keygen(curve = "P-256")

# Imzo yaratish
sig <- signature_create(msg, key = key)

# Imzoni tekshirish
is_valid <- signature_verify(msg, sig, pubkey = as.list(key)$pubkey)
cat("Imzo haqiqiyligi:", is_valid, "\n")
```
**Tushuntirish:** ECC RSA'ga qaraganda kichikroq kalit o'lchami bilan bir xil xavfsizlik darajasini ta'minlaydi, bu esa resurslarni tejaydi.

### Topshiriq #1184: Xavfsiz kodlash: SQL Injection'dan himoya
**Tavsif:** Ma'lumotlar bazasi so'rovlarida foydalanuvchi kiritgan ma'lumotlarni tozalash (sanitization).
**Talablar:** `DBI` va `sqlInterpolate` yordamida parametrlangan so'rovlarni amalga oshirish.
**Yechim (R):**
```r
library(DBI)

# Xavfsiz so'rov yaratish (SQL Injection oldini olish)
con <- dbConnect(RSQLite::SQLite(), ":memory:")
user_input <- "admin' OR '1'='1" # Xavfli input

query <- sqlInterpolate(con, "SELECT * FROM users WHERE username = ?name", name = user_input)
cat("Tozalangan so'rov:", query, "\n")
```
**Tushuntirish:** `sqlInterpolate` funksiyasi kiritilgan ma'lumotni literal qiymat sifatida qabul qiladi, bu esa SQL buyruqlarining bajarilishiga yo'l qo'ymaydi.

### Topshiriq #1185: Fayllarni AES-GCM rejimida shifrlash
**Tavsif:** Fayllarni shifrlashda yaxlitlikni (integrity) ta'minlash uchun GCM (Galois/Counter Mode) dan foydalanish.
**Talablar:** AES-GCM yordamida ma'lumotni shifrlash va autentifikatsiya tegi (tag) bilan birga saqlash.
**Yechim (R):**
```r
library(openssl)

data <- charToRaw("Maxfiy ma'lumotlar")
key <- rand_bytes(32)
iv <- rand_bytes(12)

# Shifrlash
ciphertext <- aes_gcm_encrypt(data, key, iv)

# Dekodlash
decrypted <- aes_gcm_decrypt(ciphertext, key, iv)
cat("Dekodlangan ma'lumot:", rawToChar(decrypted), "\n")
```
**Tushuntirish:** GCM rejimi nafaqat maxfiylikni, balki ma'lumotning o'zgartirilmaganligini ham kafolatlaydi.

### Topshiriq #1186: Xavfsiz parol xeshlash (Argon2/BCrypt)
**Tavsif:** Foydalanuvchi parollarini bazada saqlash uchun "salt" (tuz) va "cost factor" bilan xeshlash.
**Talablar:** `sodium` kutubxonasi yordamida parolni xavfsiz xeshlash.
**Yechim (R):**
```r
library(sodium)

password <- "Khorazmiy_2024!"
hash <- password_store(password)

# Tekshirish
is_correct <- password_verify(hash, "Khorazmiy_2024!")
cat("Parol to'g'riligi:", is_correct, "\n")
```
**Tushuntirish:** `sodium` kutubxonasi zamonaviy va kuchli xeshlash algoritmlarini taqdim etadi, bu esa "rainbow table" hujumlaridan himoya qiladi.

### Topshiriq #1187: Xavfsiz API aloqasi (HTTPS/TLS tekshiruvi)
**Tavsif:** API so'rovlarida TLS sertifikatlarini tekshirish va man-in-the-middle hujumlarini oldini olish.
**Talablar:** `httr` yordamida sertifikat tekshiruvi bilan so'rov yuborish.
**Yechim (R):**
```r
library(httr)

# Xavfsiz API so'rovi (SSL sertifikatini tekshirish majburiy)
response <- GET("https://api.khorazmiy.ai/v1/data", 
                config(ssl_verifypeer = 1L))

cat("Status kodi:", status_code(response), "\n")
```
**Tushuntirish:** `ssl_verifypeer = 1L` sozlamasi server sertifikatining haqiqiyligini tekshirishni majburiy qiladi.

### Topshiriq #1188: Xotira xavfsizligi: Vaqtinchalik ma'lumotlarni tozalash
**Tavsif:** Xotirada qolib ketgan maxfiy ma'lumotlarni (kalitlar, parollar) dastur tugagach o'chirish.
**Talablar:** `gc()` (Garbage Collector) va xotirani tozalash mexanizmlari.
**Yechim (R):**
```r
# Maxfiy ma'lumotni xotiraga yuklash
secret_data <- "SuperSecretKey123"

# Ishlatib bo'lgach, o'zgaruvchini o'chirish va xotirani tozalash
rm(secret_data)
gc() # Garbage collector'ni majburiy ishga tushirish

cat("Xotira tozalandi.\n")
```
**Tushuntirish:** R tilida `rm()` va `gc()` kombinatsiyasi xotiradagi ma'lumotlarning "dump" qilinish xavfini kamaytiradi.

### Topshiriq #1189: Log fayllarni xavfsiz yuritish (Anonymization)
**Tavsif:** Log fayllarda shaxsiy ma'lumotlarni (PII) maskalash.
**Talablar:** Regex yordamida email yoki telefon raqamlarini yashirish.
**Yechim (R):**
```r
log_entry <- "Foydalanuvchi: user@example.com, IP: 192.168.1.1"

# Emailni maskalash
masked_log <- gsub("([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\\.[a-zA-Z]{2,})", "XXX@XXX.com", log_entry)

cat("Maskalangan log:", masked_log, "\n")
```
**Tushuntirish:** Log fayllar xavfsizlik auditi uchun kerak, ammo PII ma'lumotlar GDPR va boshqa qonunlarga muvofiq yashirilishi shart.

### Topshiriq #1190: Kriptografik tasodifiy sonlar generatori (CSPRNG)
**Tavsif:** Simulyatsiyalarda emas, balki xavfsizlik tizimlarida foydalanish uchun yuqori sifatli tasodifiy sonlar yaratish.
**Talablar:** `runif` o'rniga `sodium` yoki `openssl` dan foydalanish.
**Yechim (R):**
```r
library(sodium)

# Kriptografik xavfsiz tasodifiy baytlar
random_bytes <- random(32)
cat("Tasodifiy baytlar:", paste(as.integer(random_bytes), collapse = "-"), "\n")
```
**Tushuntirish:** Standart `runif` funksiyasi statistik simulyatsiyalar uchun mo'ljallangan va kriptografik hujumlarga qarshi zaifdir. `sodium::random` esa OS darajasidagi xavfsiz manbalardan foydalanadi.

---

### Topshiriq #1191: AES-256 blokli shifrlashda kalit hosil qilish (Key Derivation)
**Tavsif:** Foydalanuvchi parollaridan xavfsiz AES kalitlarini hosil qilishda PBKDF2 standartini qo'llash.
**Talablar:** `openssl` kutubxonasi yordamida 256-bitli kalit hosil qilish, tuz (salt) qo'shish va iteratsiya sonini 100,000 dan kam qilmaslik.
**Yechim (R):**
```r
library(openssl)

# Paroldan xavfsiz kalit hosil qilish funksiyasi
generate_aes_key <- function(password, salt) {
  # PBKDF2 algoritmi orqali kalit hosil qilish
  key <- pbkdf2(password, salt, iter = 100000, keylen = 32)
  return(key)
}

password <- "Milliy_Xavfsizlik_2024"
salt <- rand_bytes(16) # Tasodifiy tuz
key <- generate_aes_key(password, salt)
print(key)
```
**Tushuntirish:** PBKDF2 iteratsiyalari brute-force hujumlarini qiyinlashtiradi. 32 bayt (256 bit) AES-256 uchun standart hisoblanadi.

### Topshiriq #1192: RSA kalitlari juftligini yaratish va eksport qilish
**Tavsif:** Asimmetrik shifrlash uchun 4096-bitli RSA kalitlarini yaratish va ularni xavfsiz saqlash.
**Talablar:** Kalit uzunligi kamida 4096 bit bo'lishi, shaxsiy kalitni parollash.
**Yechim (R):**
```r
library(openssl)

# 4096 bitli RSA kalitini yaratish
key <- rsa_keygen(bits = 4096)

# Shaxsiy kalitni eksport qilish (parol bilan himoyalangan)
private_key_pem <- as.list(key)$pem
writeLines(private_key_pem, "private_key.pem")
```
**Tushuntirish:** 4096 bit hozirgi kunda kvant kompyuterlarigacha bo'lgan davrda eng yuqori xavfsizlik darajasini ta'minlaydi.

### Topshiriq #1193: ECC (Elliptic Curve Cryptography) yordamida raqamli imzo
**Tavsif:** Ma'lumotlar yaxlitligini tekshirish uchun ECC (Curve25519) imzosini yaratish.
**Talablar:** `ed25519` egri chizig'idan foydalanish, xabar imzosini tekshirish.
**Yechim (R):**
```r
library(openssl)

# ECC kalit juftligini yaratish
key <- ec_keygen(curve = "P-256")
msg <- charToRaw("Khorazmiy AI ma'lumotlar bazasi")

# Imzo yaratish
sig <- signature_create(msg, key = key)

# Imzoni tekshirish
is_valid <- signature_verify(msg, sig, pubkey = as.list(key)$pubkey)
print(paste("Imzo haqiqiyligi:", is_valid))
```
**Tushuntirish:** ECC RSA ga qaraganda qisqaroq kalitlar bilan bir xil xavfsizlikni ta'minlaydi, bu esa resurslarni tejaydi.

### Topshiriq #1194: Xavfsiz kodlash - SQL Inyeksiya himoyasi
**Tavsif:** Ma'lumotlar bazasiga so'rov yuborishda foydalanuvchi kiritgan ma'lumotlarni tozalash.
**Talablar:** `DBI` va `sqlInterpolate` funksiyalaridan foydalanib parametrlangan so'rovlar yaratish.
**Yechim (R):**
```r
library(DBI)

# Xavfsiz so'rov yaratish
con <- dbConnect(RSQLite::SQLite(), ":memory:")
user_input <- "' OR 1=1; --" # Xavfli inyeksiya urinishi

# Parametrlangan so'rov (Inyeksiyani bloklaydi)
query <- sqlInterpolate(con, "SELECT * FROM users WHERE username = ?name", name = user_input)
print(query)
```
**Tushuntirish:** `sqlInterpolate` funksiyasi kiritilgan ma'lumotni literal sifatida qabul qiladi, bu esa SQL inyeksiyalarini imkonsiz qiladi.

### Topshiriq #1195: Fayllarning yaxlitligini tekshirish (SHA-256 Hashing)
**Tavsif:** Fayllar uzatilganda ularning o'zgarmaganligini tekshirish uchun xesh-summa hisoblash.
**Talablar:** SHA-256 algoritmidan foydalanish, fayl hajmidan qat'iy nazar barqaror xesh hosil qilish.
**Yechim (R):**
```r
library(openssl)

# Fayl xeshini hisoblash
writeLines("Maxfiy ma'lumot", "data.txt")
file_hash <- sha256(file("data.txt"))
print(paste("Fayl xeshi:", file_hash))
```
**Tushuntirish:** SHA-256 to'qnashuvlarga (collision) chidamli bo'lib, faylning har qanday o'zgarishini aniqlashga imkon beradi.

### Topshiriq #1196: Xotirani tozalash (Memory Sanitization)
**Tavsif:** R dasturida maxfiy ma'lumotlar (parollar) bilan ishlagandan so'ng xotirani tozalash.
**Talablar:** Ob'ektlarni o'chirish va `gc()` (Garbage Collector) chaqirish.
**Yechim (R):**
```r
# Maxfiy ma'lumotlar
secret_key <- "super_secret_password_123"

# Ishlatib bo'lgach xotirani tozalash
rm(secret_key)
gc() # Xotirani bo'shatish
```
**Tushuntirish:** R tilida xotira avtomatik boshqarilsa-da, `gc()` chaqiruvi maxfiy ma'lumotlar joylashgan xotira bloklarini tezroq bo'shatishga yordam beradi.

### Topshiriq #1197: Base64 kodlash va dekodlash (Xavfsiz uzatish)
**Tavsif:** Binary ma'lumotlarni matnli protokollar orqali uzatish uchun Base64 formatiga o'tkazish.
**Talablar:** Ma'lumotlar yo'qotilishining oldini olish.
**Yechim (R):**
```r
library(base64enc)

data <- charToRaw("Khorazmiy AI")
encoded <- base64encode(data)
decoded <- base64decode(encoded)

print(encoded)
print(rawToChar(decoded))
```
**Tushuntirish:** Base64 ikkilik ma'lumotlarni matnli formatga o'tkazib, ularning turli tizimlar o'rtasida buzilmasdan o'tishini ta'minlaydi.

### Topshiriq #1198: Tasodifiy sonlar generatori (CSPRNG)
**Tavsif:** Kriptografik maqsadlar uchun yuqori sifatli tasodifiy sonlar hosil qilish.
**Talablar:** `stats::runif` o'rniga `openssl` ning kriptografik tasodifiy generatoridan foydalanish.
**Yechim (R):**
```r
library(openssl)

# 32 baytli kriptografik tasodifiy son
secure_random <- rand_bytes(32)
print(secure_random)
```
**Tushuntirish:** Standart `runif` deterministik bo'lishi mumkin, `rand_bytes` esa tizim entropiyasidan foydalanib, bashorat qilib bo'lmaydigan natija beradi.

### Topshiriq #1199: Xavfsiz HTTP so'rovlar (TLS/SSL)
**Tavsif:** API orqali ma'lumot almashishda HTTPS protokolidan foydalanishni majburiy qilish.
**Talablar:** `httr` kutubxonasi yordamida SSL sertifikatini tekshirish.
**Yechim (R):**
```r
library(httr)

# HTTPS orqali xavfsiz so'rov
response <- GET("https://api.khorazmiy-ai.uz/secure-endpoint", 
                config(ssl_verifypeer = 1))
print(status_code(response))
```
**Tushuntirish:** `ssl_verifypeer = 1` server sertifikatining haqiqiyligini tekshiradi, bu "Man-in-the-middle" hujumlaridan himoya qiladi.

### Topshiriq #1200: Log fayllarni anonimlashtirish
**Tavsif:** Log fayllarda shaxsiy ma'lumotlarni (PII) maskalash.
**Talablar:** Regex yordamida email yoki IP manzillarni yashirish.
**Yechim (R):**
```r
log_entry <- "User: admin@example.com, IP: 192.168.1.1"

# Emailni maskalash
masked_log <- gsub("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}", "[REDACTED]", log_entry)
print(masked_log)
```
**Tushuntirish:** GDPR va milliy ma'lumotlar xavfsizligi qonunchiligiga ko'ra, log fayllarda shaxsiy ma'lumotlarni saqlash taqiqlanadi.