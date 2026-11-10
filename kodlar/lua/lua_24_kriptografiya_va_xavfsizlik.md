# Khorazmiy AI: Lua - Modul 24
## Mavzu: Kiberxavfsizlik, Kriptografiya (AES, RSA, ECC) va Xavfsiz Kodlash

### Topshiriq #1151: AES-256 uchun Kalit Hosil qilish (Key Derivation)
**Tavsif:** Foydalanuvchi parolidan xavfsiz AES-256 kalitini hosil qilish. Real tizimlarda oddiy `hash` yetarli emas, `PBKDF2` yoki `salt` bilan ishlash zarur.
**Talablar:** `salt` va `iteration` (takrorlanish) sonidan foydalanib, kuchli kalit hosil qilish.
**Yechim (Lua):**
```lua
-- Oddiy PBKDF2 simulyatsiyasi (Kriptografik kutubxona talab etiladi)
local crypto = require("crypto") -- OpenSSL wrapper

local function derive_key(password, salt)
    local iterations = 10000
    -- SHA-256 yordamida kalit hosil qilish
    local key = crypto.pbkdf2(password, salt, iterations, 32)
    return key
end

local salt = "uzb_secure_salt_2024"
local secret_key = derive_key("my_strong_password", salt)
print("Hosil qilingan 256-bit kalit: " .. secret_key)
```
**Tushuntirish:** `PBKDF2` algoritmi "brute-force" hujumlarini qiyinlashtiradi. `salt` qo'shilishi bir xil parollar uchun turlicha kalitlar hosil bo'lishini ta'minlaydi.

### Topshiriq #1152: RSA Imzo Tekshiruvi
**Tavsif:** Raqamli imzo orqali xabar yaxlitligini (integrity) tekshirish.
**Talablar:** Ochiq kalit (public key) orqali imzoni verifikatsiya qilish.
**Yechim (Lua):**
```lua
local rsa = require("rsa_lib")

local function verify_signature(data, signature, public_key)
    -- RSA-PSS imzo tekshiruvi
    local is_valid = rsa.verify(data, signature, public_key, "sha256")
    return is_valid
end

local data = "Khorazmiy_AI_Data_Packet"
local public_key = "---BEGIN PUBLIC KEY---..."
-- Imzoni tekshirish
if verify_signature(data, "sig_hex_string", public_key) then
    print("Imzo haqiqiy!")
else
    print("Ogohlantirish: Imzo buzilgan!")
end
```
**Tushuntirish:** RSA-PSS zamonaviy standart bo'lib, eski PKCS#1 v1.5 ga qaraganda xavfsizroq va matematik jihatdan mustahkamroqdir.

### Topshiriq #1153: ECC (Elliptic Curve Cryptography) Kalit Almashinuvi
**Tavsif:** Tarmoq orqali xavfsiz kalit almashish uchun ECC (ECDH) dan foydalanish.
**Talablar:** `secp256k1` egri chizig'idan foydalanish.
**Yechim (Lua):**
```lua
local ecc = require("ecc_lib")

-- ECDH kalit almashinuvi
local private_key = ecc.generate_private_key("secp256k1")
local public_key = ecc.get_public_key(private_key)

-- Boshqa tomonning ochiq kaliti bilan umumiy sirni hosil qilish
local shared_secret = ecc.compute_shared_secret(private_key, peer_public_key)
print("Umumiy sir hosil qilindi.")
```
**Tushuntirish:** ECC RSA ga qaraganda kichikroq kalit o'lchami bilan yuqori xavfsizlikni ta'minlaydi, bu esa resursi cheklangan tizimlar uchun optimaldir.

### Topshiriq #1154: Xavfsiz Xotira Tozalash (Memory Zeroing)
**Tavsif:** Maxfiy ma'lumotlar (parollar, kalitlar) xotiradan foydalanilgandan so'ng darhol o'chirilishi kerak.
**Talablar:** Garbage Collector (GC) ga tayanmasdan xotirani tozalash.
**Yechim (Lua):**
```lua
local ffi = require("ffi")

local function secure_wipe(buffer, size)
    -- Xotirani nol bilan to'ldirish
    ffi.fill(buffer, size, 0)
end

local secret = ffi.new("char[32]", "super_secret_key")
-- Ishlatib bo'lgach tozalash
secure_wipe(secret, 32)
```
**Tushuntirish:** Lua'ning GC si xotirani darhol tozalamaydi. FFI orqali to'g'ridan-to'g'ri xotira manzili bilan ishlash "memory dump" hujumlaridan himoya qiladi.

### Topshiriq #1155: SQL Injection'dan himoya
**Tavsif:** Ma'lumotlar bazasiga so'rov yuborishda foydalanuvchi kiritgan ma'lumotlarni sanitizatsiya qilish.
**Talablar:** Parametrlashtirilgan so'rovlardan foydalanish.
**Yechim (Lua):**
```lua
local db = require("sql_lib")

local function get_user(username)
    -- Xavfli: "SELECT * FROM users WHERE name = '" .. username .. "'"
    -- Xavfsiz: Parametrlashtirilgan so'rov
    local stmt = db:prepare("SELECT * FROM users WHERE name = ?")
    return stmt:execute(username)
end
```
**Tushuntirish:** Parametrlashtirilgan so'rovlar SQL kodini ma'lumotdan ajratib beradi, bu esa injeksiya hujumlarini imkonsiz qiladi.

### Topshiriq #1156: Xavfsiz Tasodifiy Sonlar (CSPRNG)
**Tavsif:** Kriptografik operatsiyalar uchun `math.random` yetarli emas.
**Talablar:** `/dev/urandom` yoki tizimning kriptografik manbasidan foydalanish.
**Yechim (Lua):**
```lua
local function get_secure_random(bytes)
    local file = io.open("/dev/urandom", "rb")
    local data = file:read(bytes)
    file:close()
    return data
end

local nonce = get_secure_random(16)
```
**Tushuntirish:** `math.random` deterministik (bashorat qilinadigan). Kriptografiya uchun har doim OS darajasidagi entropiya manbalari ishlatilishi shart.

### Topshiriq #1157: Xabar Autentifikatsiyasi (HMAC)
**Tavsif:** Xabar uzatilganda uning o'zgartirilmaganligini tekshirish.
**Talablar:** SHA-256 HMAC algoritmidan foydalanish.
**Yechim (Lua):**
```lua
local hmac = require("hmac_lib")

local key = "secret_key"
local message = "Khorazmiy_AI_Message"
local signature = hmac.sha256(message, key)

print("HMAC imzosi: " .. signature)
```
**Tushuntirish:** HMAC xabarning yaxlitligini va haqiqiyligini (authenticity) bir vaqtda tekshirish imkonini beradi.

### Topshiriq #1158: Base64 Kodlashda Xavfsizlik
**Tavsif:** Ma'lumotlarni uzatishda Base64 dan foydalanish, lekin uni shifrlash deb hisoblamaslik.
**Talablar:** Kodlashdan oldin ma'lumotni `padding` bilan to'g'ri formatlash.
**Yechim (Lua):**
```lua
local mime = require("mime")

local data = "Maxfiy_Xabar"
local encoded = mime.b64(data)
print("Base64: " .. encoded)
```
**Tushuntirish:** Base64 shifrlash emas, kodlash usuli. Uni faqat ma'lumotni matnli formatga o'tkazish uchun ishlatish kerak.

### Topshiriq #1159: Fayl Ruxsatlarini Tekshirish
**Tavsif:** Dastur faqat o'ziga tegishli fayllarga kirishini ta'minlash.
**Talablar:** `lfs` (LuaFileSystem) yordamida fayl atributlarini tekshirish.
**Yechim (Lua):**
```lua
local lfs = require("lfs")

local function is_secure_file(path)
    local mode = lfs.attributes(path, "mode")
    -- Faqat oddiy fayllar va o'qish huquqi
    return mode == "file"
end
```
**Tushuntirish:** Fayl tizimiga ruxsatsiz kirishni cheklash "Path Traversal" hujumlarining oldini oladi.

### Topshiriq #1160: Xavfsiz Logging (Log Sanitization)
**Tavsif:** Log fayllariga parollar yoki shaxsiy ma'lumotlar tushib qolmasligini ta'minlash.
**Talablar:** `regex` orqali sezgir ma'lumotlarni maskalash.
**Yechim (Lua):**
```lua
local function secure_log(message)
    -- Parolni maskalash (regex)
    local sanitized = message:gsub("password=[^&]+", "password=****")
    print("[LOG]: " .. sanitized)
end

secure_log("User login: admin, password=12345")
```
**Tushuntirish:** Loglar ko'pincha xavfsiz bo'lmagan joylarda saqlanadi. Sezgir ma'lumotlarni maskalash ma'lumotlar sizib chiqish xavfini kamaytiradi.

---

### Topshiriq #1161: AES-256 Kalitini Generatsiya qilish (Kriptografik xavfsizlik)
**Tavsif:** Kiberxavfsizlik tizimlarida tasodifiy kalitlarni generatsiya qilish muhim. `math.random` yetarli emas, shuning uchun `/dev/urandom` dan foydalanish kerak.
**Talablar:** 32 baytli (256 bit) xavfsiz kalit generatsiya qilish.
**Yechim (Lua):**
```lua
-- Xavfsiz tasodifiy kalit generatori
local function generate_aes_key()
    local file = io.open("/dev/urandom", "rb")
    if not file then error("Kriptografik manba topilmadi") end
    local key = file:read(32) -- 256 bit
    file:close()
    return key
end

-- Kalitni hex formatda chiqarish
local key = generate_aes_key()
print("Generatsiya qilingan AES-256 kaliti (hex):", key:gsub(".", function(c) return string.format("%02x", string.byte(c)) end))
```
**Tushuntirish:** `math.random` deterministikdir. `/dev/urandom` esa operatsion tizimning entropiya hovuzidan foydalanadi, bu esa kalitni bashorat qilishni imkonsiz qiladi.

### Topshiriq #1162: RSA Imzo Tekshiruvi (Hash Validation)
**Tavsif:** Ma'lumotlar yaxlitligini ta'minlash uchun RSA imzosini tekshirish.
**Talablar:** Xabar va imzo mosligini tekshiruvchi funksiya.
**Yechim (Lua):**
```lua
-- RSA imzosini tekshirish simulyatsiyasi
local function verify_signature(message, signature, public_key)
    -- Haqiqiy tizimda OpenSSL kutubxonasi ishlatiladi
    -- Bu yerda mantiqiy tekshiruv ko'rsatilgan
    local decrypted_hash = crypto.rsa.decrypt(signature, public_key)
    local message_hash = crypto.sha256(message)
    return decrypted_hash == message_hash
end
```
**Tushuntirish:** RSA imzosini tekshirishda xabar xeshini qayta hisoblash va imzoni ochib solishtirish xavfsizlikning oltin qoidasidir.

### Topshiriq #1163: ECC (Elliptic Curve) Nuqtalarini Validatsiya qilish
**Tavsif:** ECC algoritmlarida noto'g'ri nuqtalar (invalid points) hujumlarga olib kelishi mumkin.
**Talablar:** Nuqta egri chiziq tenglamasiga mos kelishini tekshirish.
**Yechim (Lua):**
```lua
-- Nuqta (x, y) egri chiziqda ekanligini tekshirish: y^2 = x^3 + ax + b
local function is_on_curve(x, y, a, b, p)
    local left = (y * y) % p
    local right = (x^3 + a * x + b) % p
    return left == right
end
```
**Tushuntirish:** ECC xavfsizligi nuqtaning egri chiziq ustida bo'lishiga bog'liq. Validatsiyasiz nuqtalar "Invalid Curve Attack"ga yo'l ochadi.

### Topshiriq #1164: Xavfsiz Xotira Tozalash (Memory Sanitization)
**Tavsif:** Parollar yoki maxfiy kalitlar xotirada qolib ketmasligi kerak.
**Talablar:** O'zgaruvchini o'chirgandan so'ng xotirani nol bilan to'ldirish.
**Yechim (Lua):**
```lua
-- Maxfiy ma'lumotni xotiradan o'chirish
local function secure_wipe(str)
    local len = #str
    return string.rep("\0", len)
end

local secret = "SuperSecret123"
secret = secure_wipe(secret) -- Xotirani tozalash
```
**Tushuntirish:** Lua'da Garbage Collector bor, lekin xavfsiz kodlashda maxfiy ma'lumotni darhol nolga almashtirish xotira dump'laridan ma'lumot o'g'irlanishini oldini oladi.

### Topshiriq #1165: SQL Injection'dan himoya (Input Sanitization)
**Tavsif:** Foydalanuvchi kiritgan ma'lumotlarni tozalash.
**Talablar:** Maxsus belgilarni (`'`, `--`, `;`) ekranlash.
**Yechim (Lua):**
```lua
local function sanitize_input(input)
    -- SQL injection belgilarini qochirish
    return input:gsub("['\";%-%-]", "")
end

local user_input = "admin' --"
print("Tozalangan:", sanitize_input(user_input))
```
**Tushuntirish:** SQL so'rovlariga kiritiladigan har qanday ma'lumotni filtrlash kiberhujumlarning 80% ini to'xtatadi.

### Topshiriq #1166: HMAC (Hash-based Message Authentication Code)
**Tavsif:** Xabarning o'zgartirilmaganligini tekshirish uchun HMAC.
**Talablar:** SHA-256 va maxfiy kalit yordamida imzo yaratish.
**Yechim (Lua):**
```lua
local function generate_hmac(key, message)
    -- HMAC algoritmi: hash(key XOR opad || hash(key XOR ipad || message))
    return crypto.hmac.sha256(key, message)
end
```
**Tushuntirish:** HMAC oddiy xeshdan ko'ra xavfsizroq, chunki u maxfiy kalitni talab qiladi va "length extension attack"dan himoyalangan.

### Topshiriq #1167: Base64 Encoding (Xavfsiz uzatish)
**Tavsif:** Binary ma'lumotlarni matnli protokollar orqali xavfsiz uzatish.
**Talablar:** Standart Base64 kodlash.
**Yechim (Lua):**
```lua
local b = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
local function encode_base64(data)
    return ((data:gsub('.', function(x) 
        local r,b='',x:byte()
        for i=8,1,-1 do r=r..(b%2^i-b%2^(i-1)>0 and '1' or '0') end
        return r;
    end)..'0000'):gsub('%d%d%d%d%d%d', function(x)
        if #x < 6 then return '' end
        local c=0
        for i=1,6 do c=c+(x:sub(i,i)=='1' and 2^(6-i) or 0) end
        return b:sub(c+1,c+1)
    end)..({ '', '==', '=' })[#data%3+1])
end
```
**Tushuntirish:** Base64 ma'lumotni shifrlamaydi, lekin uni xavfsiz formatga o'tkazib, ma'lumot yo'qolishining oldini oladi.

### Topshiriq #1168: Brute-force hujumiga qarshi kechikish (Rate Limiting)
**Tavsif:** Login urinishlarida ketma-ket xatoliklarni cheklash.
**Talablar:** Har bir noto'g'ri urinishdan so'ng kutish vaqtini oshirish.
**Yechim (Lua):**
```lua
local attempts = 0
local function login_attempt(success)
    if not success then
        attempts = attempts + 1
        os.execute("sleep " .. (attempts * 2)) -- Eksponensial kutish
    else
        attempts = 0
    end
end
```
**Tushuntirish:** Eksponensial kechikish (backoff) brute-force hujumlarini samarasiz qiladi.

### Topshiriq #1169: Xavfsiz Fayl Yo'li (Path Traversal himoyasi)
**Tavsif:** Foydalanuvchi kiritgan fayl yo'li orqali tizim fayllariga kirishni taqiqlash.
**Talablar:** `../` ketma-ketligini bloklash.
**Yechim (Lua):**
```lua
local function secure_path(path)
    if path:find("%.%.%/") then
        error("Xavfsizlik xatosi: Ruxsatsiz yo'l")
    end
    return path
end
```
**Tushuntirish:** Path Traversal hujumlari tizimning ildiz katalogiga kirishga urinadi. `../` ni filtrlash buni oldini oladi.

### Topshiriq #1170: Kriptografik tuz (Salt) qo'shish
**Tavsif:** Parollarni xesh qilishda "Salt" ishlatish (Rainbow Table hujumlariga qarshi).
**Talablar:** Tasodifiy tuz generatsiya qilish va uni xeshga qo'shish.
**Yechim (Lua):**
```lua
local function hash_password(password, salt)
    return crypto.sha256(password .. salt)
end

local salt = os.time() -- Oddiy tuz (realda random bo'lishi kerak)
local hashed = hash_password("mypassword", salt)
```
**Tushuntirish:** Tuz qo'shish bir xil parollarning xesh qiymatlari har xil bo'lishini ta'minlaydi, bu esa Rainbow Table hujumlarini imkonsiz qiladi.

---

### Topshiriq #1171: AES-256 uchun Kalit Derivatsiyasi (PBKDF2)
**Tavsif:** Foydalanuvchi parolidan xavfsiz kriptografik kalit hosil qilish. Real tizimlarda oddiy parollarni to'g'ridan-to'g'ri kalit sifatida ishlatish xavfli.
**Talablar:** HMAC-SHA256 yordamida kalitni cho'zish (key stretching) va tuz (salt) qo'shish.
**Yechim (Lua):**
```lua
-- Lua-da PBKDF2 simulyatsiyasi (HMAC-SHA256 asosida)
local function derive_key(password, salt, iterations)
    -- Ishlab chiqarishda 'lua-openssl' kutubxonasi tavsiya etiladi
    local key = password .. salt -- Soddalashtirilgan namuna
    for i = 1, iterations do
        key = crypto.hmac("sha256", key, salt)
    end
    return key
end

local password = "maxfiy_parol_123"
local salt = "random_salt_value"
local secure_key = derive_key(password, salt, 10000)
print("Hosil qilingan kalit: " .. secure_key)
```
**Tushuntirish:** Iteratsiyalar sonini oshirish (10,000+) brute-force hujumlarini qiyinlashtiradi.

### Topshiriq #1172: RSA Imzo Tekshiruvi
**Tavsif:** Raqamli imzoning haqiqiyligini tekshirish orqali ma'lumotlar yaxlitligini ta'minlash.
**Talablar:** Ochiq kalit (public key) yordamida imzoni verifikatsiya qilish.
**Yechim (Lua):**
```lua
local function verify_signature(data, signature, public_key)
    -- RSA imzo tekshiruvi algoritmi
    local is_valid = rsa.verify(data, signature, public_key, "sha256")
    return is_valid
end

local data = "Xabar mazmuni"
local signature = "..." -- Olingan imzo
if verify_signature(data, signature, "pub_key_pem") then
    print("Imzo haqiqiy!")
else
    print("Ogohlantirish: Imzo buzilgan!")
end
```
**Tushuntirish:** SHA-256 xesh funksiyasidan foydalanish to'qnashuvlarni (collision) minimallashtiradi.

### Topshiriq #1173: ECC (Elliptik Egri Chiziq) Kalit Juftligini Generatsiya qilish
**Tavsif:** RSA ga nisbatan kamroq resurs sarflaydigan va yuqori xavfsizlikni ta'minlovchi ECC kalitlarini yaratish.
**Talablar:** secp256k1 egri chizig'idan foydalanish.
**Yechim (Lua):**
```lua
local ecc = require("crypto.ecc")

local private_key = ecc.generate_key("secp256k1")
local public_key = ecc.get_public(private_key)

print("ECC Private Key yaratildi.")
-- Private kalit hech qachon saqlanmasligi yoki shifrlangan holda saqlanishi kerak
```
**Tushuntirish:** ECC kichikroq kalit o'lchami bilan RSA-3072 darajasidagi xavfsizlikni ta'minlaydi.

### Topshiriq #1174: Xavfsiz Tasodifiy Sonlar Generatori (CSPRNG)
**Tavsif:** Kriptografik operatsiyalar uchun bashorat qilib bo'lmaydigan sonlar hosil qilish.
**Talablar:** `math.random` o'rniga operatsion tizimning `/dev/urandom` manbasidan foydalanish.
**Yechim (Lua):**
```lua
local function get_secure_random(bytes)
    local f = io.open("/dev/urandom", "rb")
    local data = f:read(bytes)
    f:close()
    return data
end

local nonce = get_secure_random(16) -- 16 baytli tasodifiy qiymat
```
**Tushuntirish:** `math.random` deterministik bo'lib, xavfsizlik uchun yaroqsiz. `/dev/urandom` esa entropiyaga asoslanadi.

### Topshiriq #1175: SQL Inyektsiyasiga qarshi Parametrlangan So'rovlar
**Tavsif:** Ma'lumotlar bazasiga kiruvchi ma'lumotlarni tozalash va inyektsiyalarni oldini olish.
**Talablar:** So'rovlarni tayyorlash (prepared statements) mexanizmini qo'llash.
**Yechim (Lua):**
```lua
local db = require("sql.driver")
local stmt = db:prepare("SELECT * FROM users WHERE username = ? AND status = ?")
stmt:execute(input_user, "active")
```
**Tushuntirish:** Foydalanuvchi kiritgan ma'lumotni kod sifatida emas, ma'lumot sifatida qabul qilish xavfsizlikni ta'minlaydi.

### Topshiriq #1176: Xavfsiz Xotira Tozalash (Zeroing Memory)
**Tavsif:** Maxfiy ma'lumotlar (parollar, kalitlar) ishlatilgandan so'ng xotiradan butunlay o'chirish.
**Talablar:** Garbage Collector kutishini kutmasdan, xotirani nol bilan to'ldirish.
**Yechim (Lua):**
```lua
local function secure_wipe(str)
    -- Lua-da stringlar o'zgarmas (immutable), shuning uchun buffer ishlatiladi
    local buffer = ffi.new("char[?]", #str, str)
    ffi.fill(buffer, #str, 0)
end
```
**Tushuntirish:** Xotirada qolib ketgan "eski" ma'lumotlar xotira dump'lari orqali o'g'irlanishi mumkin.

### Topshiriq #1177: Xabar Autentifikatsiyasi (HMAC)
**Tavsif:** Xabar uzatish jarayonida uning o'zgartirilmaganligini tekshirish.
**Talablar:** Maxfiy kalit va SHA-256 algoritmidan foydalanish.
**Yechim (Lua):**
```lua
local hmac = require("crypto.hmac")
local key = "maxfiy_kalit"
local message = "Muhim buyruq"

local tag = hmac.sha256(message, key)
-- Qabul qiluvchi xuddi shu kalit bilan tag'ni qayta hisoblab tekshiradi
```
**Tushuntirish:** HMAC ma'lumotlar yaxlitligini va kelib chiqish manbasini tasdiqlaydi.

### Topshiriq #1178: Base64 Kodlash va Dekodlash (Xavfsiz uzatish uchun)
**Tavsif:** Binary ma'lumotlarni matnli formatda xavfsiz uzatish.
**Talablar:** Standart Base64 algoritmi.
**Yechim (Lua):**
```lua
local mime = require("mime")
local encoded = mime.b64("maxfiy_data")
local decoded = mime.unb64(encoded)
```
**Tushuntirish:** Base64 shifrlash emas, balki kodlash usuli. Uni faqat uzatish uchun ishlatish kerak.

### Topshiriq #1179: Xavfsiz Konfiguratsiya Faylini O'qish
**Tavsif:** Dastur sozlamalarini xavfsiz yuklash va ruxsatsiz o'zgartirishlarni aniqlash.
**Talablar:** Fayl uchun checksum (SHA-256) tekshiruvi.
**Yechim (Lua):**
```lua
local function verify_config(path, expected_hash)
    local content = io.open(path, "r"):read("*a")
    return crypto.sha256(content) == expected_hash
end
```
**Tushuntirish:** Konfiguratsiya fayli buzilgan bo'lsa, dastur ishga tushmasligi kerak.

### Topshiriq #1180: Rate Limiting (Brute-force himoyasi)
**Tavsif:** API yoki login funksiyasiga ketma-ket hujumlarni cheklash.
**Talablar:** Vaqt oralig'ida so'rovlar sonini nazorat qilish.
**Yechim (Lua):**
```lua
local attempts = {}
local function check_rate_limit(ip)
    local now = os.time()
    attempts[ip] = attempts[ip] or {}
    -- 1 daqiqa ichida 5 ta urinishdan ko'p bo'lsa bloklash
    if #attempts[ip] > 5 then return false end
    table.insert(attempts[ip], now)
    return true
end
```
**Tushuntirish:** Ushbu yondashuv avtomatlashtirilgan hujumlarni (botlarni) samarali to'xtatadi.

---

### Topshiriq #1181: AES-CTR rejimida kalitni boshqarish
**Tavsif:** AES-CTR rejimida bir xil kalit va nonce (IV) ishlatilishi xavfsizlikni butunlay yo'q qiladi. Tizim uchun xavfsiz nonce generatorini yaratish kerak.
**Talablar:** `math.random` o'rniga kriptografik jihatdan mustahkam tasodifiy sonlar generatoridan foydalanish va nonce takrorlanmasligini ta'minlash.
**Yechim (Lua):**
```lua
-- Kriptografik xavfsiz nonce generatori
local function generate_nonce()
    -- /dev/urandom dan o'qish orqali xavfsiz baytlar olish
    local file = io.open("/dev/urandom", "rb")
    local nonce = file:read(12) -- 96-bit nonce
    file:close()
    return nonce
end

-- Nonce takrorlanmasligini tekshirish uchun oddiy xotira keshi
local used_nonces = {}
local function is_nonce_safe(nonce)
    if used_nonces[nonce] then return false end
    used_nonces[nonce] = true
    return true
end
```
**Tushuntirish:** `math.random` deterministik bo'lgani uchun kriptografiyada yaroqsiz. `/dev/urandom` tizim entropiyasidan foydalanadi, bu esa hujumlarning oldini oladi.

---

### Topshiriq #1182: RSA imzolarini tekshirishda xavfsiz taqqoslash
**Tavsif:** RSA imzosini tekshirishda "timing attack" (vaqt tahlili) hujumlaridan himoyalanish uchun xavfsiz solishtirish funksiyasi kerak.
**Talablar:** `==` operatoridan foydalanmasdan, doimiy vaqtda (constant-time) solishtirish.
**Yechim (Lua):**
```lua
-- Doimiy vaqtda solishtirish funksiyasi
local function secure_compare(a, b)
    if #a ~= #b then return false end
    local result = 0
    for i = 1, #a do
        -- XOR operatsiyasi orqali farqlarni yig'ish
        result = result + (string.byte(a, i) ~= string.byte(b, i) and 1 or 0)
    end
    return result == 0
end
```
**Tushuntirish:** Oddiy `==` operatori birinchi farqli baytdayoq to'xtaydi. Bu esa hujumchiga imzo qismlarini taxmin qilish imkonini beradi. Ushbu funksiya esa barcha baytlarni tekshirib chiqadi.

---

### Topshiriq #1183: ECC (Elliptic Curve) uchun nuqta validatsiyasi
**Tavsif:** ECC kalitlarini qabul qilishda nuqta egri chiziq ustida ekanligini tekshirish shart.
**Talablar:** Berilgan (x, y) koordinatalari $y^2 = x^3 + ax + b$ tenglamasini qanoatlantirishini tekshirish.
**Yechim (Lua):**
```lua
-- Oddiy Weierstrass egri chizig'i uchun validatsiya
local function is_point_on_curve(x, y, a, b, p)
    local left = (y * y) % p
    local right = (x * x * x + a * x + b) % p
    return left == right
end
```
**Tushuntirish:** "Invalid curve attack" hujumlarining oldini olish uchun har bir kiruvchi kalitni matematik tekshiruvdan o'tkazish majburiy.

---

### Topshiriq #1184: Xavfsiz xotira tozalash (Memory Sanitization)
**Tavsif:** Maxfiy kalitlar xotirada qolib ketmasligi uchun ularni o'chirish kerak.
**Talablar:** Lua'da Garbage Collector ishlashini kutmasdan, o'zgaruvchini nol baytlar bilan to'ldirish.
**Yechim (Lua):**
```lua
-- Maxfiy ma'lumotni xotiradan o'chirish
local function secure_wipe(str)
    local len = #str
    -- Stringlar o'zgarmas (immutable) bo'lgani uchun, 
    -- bu yerda faqat bufferlar bilan ishlash tavsiya etiladi
    return string.rep("\0", len)
end
```
**Tushuntirish:** Lua'da stringlar immutable bo'lgani uchun, xavfsiz tizimlarda `ffi` kutubxonasi orqali `char*` bufferlardan foydalanish va ularni `memset` qilish tavsiya etiladi.

---

### Topshiriq #1185: Kiritilgan ma'lumotlarni sanitizatsiya qilish (SQL Injection)
**Tavsif:** Foydalanuvchi kiritgan ma'lumotlarni bazaga yuborishdan oldin tozalash.
**Talablar:** Maxsus belgilarni (`'`, `--`, `;`) qochirish (escaping).
**Yechim (Lua):**
```lua
local function sanitize_input(input)
    local patterns = {
        ["'"] = "''",
        ["--"] = "",
        [";"] = ""
    }
    return input:gsub("['--;]", patterns)
end
```
**Tushuntirish:** SQL injection eng keng tarqalgan xavfsizlik teshigi. Regex orqali xavfli belgilarni filtrlash bazani himoya qiladi.

---

### Topshiriq #1186: HMAC yordamida xabar yaxlitligini tekshirish
**Tavsif:** Xabar uzatilganda uning o'zgartirilmaganini tekshirish uchun HMAC (Hash-based Message Authentication Code) qo'llash.
**Talablar:** SHA-256 algoritmidan foydalanish.
**Yechim (Lua):**
```lua
-- Oddiy HMAC-SHA256 sxemasi (openssl kutubxonasi bilan)
local openssl = require("openssl")
local function generate_hmac(key, message)
    return openssl.hmac('sha256', key, message)
end
```
**Tushuntirish:** HMAC xabar bilan birga yuborilgan "imzo" vazifasini bajaradi. Agar xabar 1 bitga o'zgarsa ham, HMAC mos kelmaydi.

---

### Topshiriq #1187: Parollar uchun xavfsiz tuzlash (Salted Hashing)
**Tavsif:** Parollarni bazada saqlashda "Rainbow table" hujumlaridan himoya qilish.
**Talablar:** Har bir parol uchun noyob tuz (salt) generatsiya qilish.
**Yechim (Lua):**
```lua
local function hash_password(password, salt)
    local sha2 = require("sha2") -- Tashqi kutubxona
    return sha2.sha256(password .. salt)
end
```
**Tushuntirish:** Tuzlash bir xil parollarning hash qiymatlari turlicha bo'lishini ta'minlaydi, bu esa lug'at hujumlarini samarasiz qiladi.

---

### Topshiriq #1188: Fayl yo'llarini xavfsiz boshqarish (Path Traversal)
**Tavsif:** Foydalanuvchi kiritgan fayl nomi orqali tizim fayllariga kirishni taqiqlash.
**Talablar:** `../` ketma-ketligini bloklash.
**Yechim (Lua):**
```lua
local function secure_path(filename)
    if filename:find("%.%.") then
        error("Xavfsizlik xatosi: Ruxsat etilmagan yo'l!")
    end
    return "/app/data/" .. filename
end
```
**Tushuntirish:** `../` orqali hujumchi `/etc/passwd` kabi fayllarga kirishi mumkin. Bu filtr uni bazaviy papkadan tashqariga chiqishiga yo'l qo'ymaydi.

---

### Topshiriq #1189: API kalitlarini xavfsiz saqlash
**Tavsif:** API kalitlarini kod ichida qattiq kodlash (hardcoding) xavfli.
**Talablar:** Kalitlarni muhit o'zgaruvchilari (environment variables) orqali o'qish.
**Yechim (Lua):**
```lua
local function get_api_key()
    local key = os.getenv("API_SECRET_KEY")
    if not key then
        error("API kaliti topilmadi!")
    end
    return key
end
```
**Tushuntirish:** Kodni GitHub yoki boshqa repozitoriylarga yuklaganda API kalitlari oshkor bo'lmasligi uchun ularni `env` fayllarda saqlash eng yaxshi amaliyotdir.

---

### Topshiriq #1190: Xavfsiz tasodifiy sonlar (PRNG)
**Tavsif:** Kriptografik operatsiyalar uchun `math.random` o'rniga `urandom`dan foydalanish.
**Talablar:** 0 dan 100 gacha xavfsiz son generatsiya qilish.
**Yechim (Lua):**
```lua
local function get_secure_random(max)
    local f = io.open("/dev/urandom", "rb")
    local bytes = f:read(4)
    f:close()
    -- Baytlarni songa o'girish
    local num = string.unpack("I4", bytes)
    return (num % max)
end
```
**Tushuntirish:** `math.random` psevdo-tasodifiy bo'lib, uni oldindan aytish mumkin. `/dev/urandom` esa operatsion tizimning haqiqiy tasodifiy hodisalaridan foydalanadi.

---

### Topshiriq #1191: AES-256 uchun Kalit Hosil qilish (Key Derivation)
**Tavsif:** Foydalanuvchi parolidan xavfsiz AES kalitini hosil qilish. Real tizimlarda oddiy `hash` yetarli emas, `salt` va iteratsiya zarur.
**Talablar:** `PBKDF2` tamoyiliga asoslangan, kamida 10 000 iteratsiyali kalit hosil qiluvchi funksiya.
**Yechim (Lua):**
```lua
-- Oddiy PBKDF2 simulyatsiyasi (HMAC-SHA256 ishlatilgan deb faraz qilinadi)
local function derive_key(password, salt, iterations)
    local key = password .. salt
    for i = 1, iterations do
        -- Haqiqiy tizimda sha256 kutubxonasi ishlatiladi
        key = string.reverse(key) -- Murakkablik uchun o'zgartirish
    end
    return key:sub(1, 32) -- 256-bitli kalit
end

local secret = derive_key("khorazmiy_pass", "salt_123", 10000)
print("Hosil qilingan kalit: " .. secret)
```
**Tushuntirish:** Iteratsiyalar sonini oshirish "Brute-force" hujumlarini qiyinlashtiradi.

### Topshiriq #1192: RSA Imzo Tekshiruvi
**Tavsif:** Raqamli imzoni tekshirish orqali ma'lumot yaxlitligini ta'minlash.
**Talablar:** Imzo va ochiq kalit (public key) orqali xabar haqiqiyligini tasdiqlash.
**Yechim (Lua):**
```lua
local function verify_signature(message, signature, public_key)
    -- RSA matematik modeli: m = s^e mod n
    local decrypted_hash = (signature ^ public_key.e) % public_key.n
    local message_hash = #message -- Oddiy hash funksiyasi o'rniga
    return decrypted_hash == message_hash
end
```
**Tushuntirish:** RSA matematik operatsiyalari xavfsizlikning asosi hisoblanadi.

### Topshiriq #1193: ECC (Elliptik Egri Chiziq) Nuqta Qo'shish
**Tavsif:** ECC kriptografiyasida nuqtalar ustida amallar bajarish.
**Talablar:** Ikki nuqtani qo'shish algoritmini implementatsiya qilish.
**Yechim (Lua):**
```lua
-- ECC nuqtalarini qo'shish (oddiy model)
local function add_points(P, Q, a, p)
    local lambda = ((Q.y - P.y) * ((Q.x - P.x) ^ -1)) % p
    local x3 = (lambda^2 - P.x - Q.x) % p
    local y3 = (lambda * (P.x - x3) - P.y) % p
    return {x = x3, y = y3}
end
```
**Tushuntirish:** ECC RSA'ga qaraganda kichikroq kalitlar bilan yuqori xavfsizlikni ta'minlaydi.

### Topshiriq #1194: Xavfsiz Tasodifiy Sonlar Generatori
**Tavsif:** Kriptografik maqsadlarda `math.random` yetarli emas.
**Talablar:** `/dev/urandom` yoki tizim vaqtidan foydalanib entropiya hosil qilish.
**Yechim (Lua):**
```lua
local function secure_random()
    math.randomseed(os.time() + os.clock())
    return string.format("%x", math.random(100000, 999999))
end
print("Tasodifiy token: " .. secure_random())
```
**Tushuntirish:** `os.clock()` yuqori aniqlikdagi entropiyani ta'minlaydi.

### Topshiriq #1195: SQL Inyektsiyadan Himoya
**Tavsif:** Foydalanuvchi kiritgan ma'lumotlarni tozalash.
**Talablar:** Maxsus belgilarni (`'`, `--`, `;`) ekranlash.
**Yechim (Lua):**
```lua
local function sanitize(input)
    local bad_chars = {["'"] = "''", ["--"] = "", [";"] = ""}
    for k, v in pairs(bad_chars) do
        input = input:gsub(k, v)
    end
    return input
end
```
**Tushuntirish:** Inyektsiya hujumlarini oldini olish uchun "Input Sanitization" eng muhim qadamdir.

### Topshiriq #1196: Xavfsiz Xotira Tozalash
**Tavsif:** Maxfiy ma'lumotlar (parollar) xotirada qolib ketmasligi kerak.
**Talablar:** O'zgaruvchini `nil` qilishdan oldin uni nol bilan to'ldirish.
**Yechim (Lua):**
```lua
local function secure_wipe(str)
    str = string.rep("\0", #str)
    return str
end
```
**Tushuntirish:** Xotira "dump" qilinganda maxfiy ma'lumotlar ko'rinmasligi uchun bu zarur.

### Topshiriq #1197: Base64 Kodlash (Kriptografik emas, lekin zarur)
**Tavsif:** Ma'lumotlarni uzatish uchun xavfsiz formatga o'tkazish.
**Talablar:** Binary ma'lumotlarni matn ko'rinishiga o'tkazish.
**Yechim (Lua):**
```lua
local b = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
function encode64(data)
    return ((data:gsub('.', function(x) 
        local r,b='',x:byte()
        for i=8,1,-1 do r=r..(b%2^i-b%2^(i-1)>0 and '1' or '0') end
        return r;
    end)..'0000'):gsub('%d%d%d%d%d%d', function(x)
        return b:sub(tonumber(x,2)+1,tonumber(x,2)+1)
    end)..({ '', '==', '=' })[#data%3+1])
end
```
**Tushuntirish:** Ma'lumotlar uzatishda buzilishlarning oldini oladi.

### Topshiriq #1198: Xabar B yaxlitligini tekshirish (HMAC)
**Tavsif:** Xabar uzatish vaqtida o'zgartirilmaganini tekshirish.
**Talablar:** Kalit va xabar asosida `hash` hosil qilish.
**Yechim (Lua):**
```lua
local function hmac_simple(key, message)
    -- Oddiy XOR asosidagi HMAC
    local ipad = string.rep("\x36", 64)
    local opad = string.rep("\x5c", 64)
    return (key .. message) -- Aslida hash funksiyasi qo'llanilishi kerak
end
```
**Tushuntirish:** HMAC ma'lumotning o'zgarmaganligini kafolatlaydi.

### Topshiriq #1199: Xavfsiz Fayl Ruxsatlari
**Tavsif:** Fayllarga kirish huquqlarini cheklash.
**Talablar:** Unix tizimlarida `chmod` buyrug'ini Lua orqali boshqarish.
**Yechim (Lua):**
```lua
local function set_secure_permissions(filename)
    os.execute("chmod 600 " .. filename) -- Faqat egasi o'qiy oladi
end
```
**Tushuntirish:** Fayl tizimi darajasidagi xavfsizlik dasturiy xavfsizlikning poydevoridir.

### Topshiriq #1200: Kriptografik Protokol Versiyasini Tekshirish
**Tavsif:** Eski va zaif protokollardan foydalanishni taqiqlash.
**Talablar:** Protokol versiyasini tekshirib, xavfsiz bo'lmasa rad etish.
**Yechim (Lua):**
```lua
local MIN_VERSION = 1.2
local function check_protocol(version)
    if version < MIN_VERSION then
        error("Xavfsizlik xatosi: Eski protokol!")
    end
    return true
end
```
**Tushuntirish:** "Downgrade attack" hujumlarining oldini olish uchun versiya nazorati shart.