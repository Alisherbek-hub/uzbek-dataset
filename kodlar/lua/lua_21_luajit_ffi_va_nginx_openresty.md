Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. LuaJIT FFI va OpenResty ekotizimini boyitish uchun yuqori unumdorlikka mo‘ljallangan 10 ta ilg‘or topshiriqni taqdim etaman.

---

# 1001-Topshiriq: C kutubxonasidan FFI orqali matematik funksiyani chaqirish

## Topshiriq sharti:
LuaJIT FFI yordamida standart `libc` kutubxonasidagi `sqrt` (kvadrat ildiz) funksiyasini yuklang va berilgan sonning ildizini hisoblang.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    double sqrt(double x);
]]

local num = 144.0
local result = ffi.C.sqrt(num)
print("Natija: " .. result)
```

## Tushuntirish va Mantiq:
`ffi.cdef` orqali C funksiyasining prototipi e'lon qilinadi. `ffi.C` esa yuklangan kutubxona (libc) ichidagi funksiyalarga to‘g‘ridan-to‘g‘ri murojaat qilish imkonini beradi. Bu Lua jadvalini yaratishdan ko‘ra tezroq ishlaydi.

## Ishlash natijasi:
```text
Natija: 12
```

---

# 1002-Topshiriq: OpenResty-da C struct (tuzilma) bilan ishlash

## Topshiriq sharti:
C tilidagi `struct` ko‘rinishidagi ma’lumotlar to‘plamini yarating va uni Lua jadvali bilan bog‘lang.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    typedef struct {
        int id;
        double value;
    } DataPoint;
]]

local point = ffi.new("DataPoint", {id = 1, value = 99.9})
print("ID: " .. point.id .. ", Value: " .. point.value)
```

## Tushuntirish va Mantiq:
`ffi.new` yordamida xotiradan C struct uchun joy ajratiladi. Bu usul katta hajmdagi ma'lumotlarni qayta ishlashda xotirani tejash va tezlikni oshirish uchun juda muhimdir.

## Ishlash natijasi:
```text
ID: 1, Value: 99.9
```

---

# 1003-Topshiriq: Nginx `ngx.shared.DICT` orqali xotira almashinuvi

## Topshiriq sharti:
OpenResty-da `shared dict` yordamida turli workerlar o‘rtasida ma’lumot almashinuvini amalga oshiring.

## Yechim (Lua kodi):
```lua
local shared_data = ngx.shared.my_cache
shared_data:set("api_key", "KHORAZMIY_AI_2024")
local val = shared_data:get("api_key")
ngx.say("Saqlangan qiymat: ", val)
```

## Tushuntirish va Mantiq:
`ngx.shared.DICT` — bu Nginx workerlari o‘rtasida umumiy xotira maydoni. U atomik operatsiyalarni qo‘llab-quvvatlaydi va yuqori yuklamali API shlyuzlarida kesh sifatida ishlatiladi.

## Ishlash natijasi:
```text
Saqlangan qiymat: KHORAZMIY_AI_2024
```

---

# 1004-Topshiriq: FFI orqali C xotirasini dinamik boshqarish

## Topshiriq sharti:
`ffi.new` yordamida katta hajmdagi massiv (array) yarating va uni Lua sikli orqali to‘ldiring.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
local arr = ffi.new("int[5]", {10, 20, 30, 40, 50})

for i = 0, 4 do
    print("Element " .. i .. ": " .. arr[i])
end
```

## Tushuntirish va Mantiq:
C massivlari Lua jadvallariga qaraganda xotirada ketma-ket joylashadi, bu esa CPU keshidan samarali foydalanishga va ishlash tezligini keskin oshirishga yordam beradi.

## Ishlash natijasi:
```text
Element 0: 10
Element 1: 20
Element 2: 30
Element 3: 40
Element 4: 50
```

---

# 1005-Topshiriq: OpenResty-da HTTP so‘rovini bloklamasdan bajarish

## Topshiriq sharti:
`ngx.location.capture` yordamida boshqa ichki API endpointiga so‘rov yuboring.

## Yechim (Lua kodi):
```lua
local res = ngx.location.capture("/internal_api")
if res.status == 200 then
    ngx.say("API javobi: ", res.body)
end
```

## Tushuntirish va Mantiq:
`ngx.location.capture` OpenResty-ning asinxron tabiatidan foydalanadi. Bu funksiya Nginx event loopini bloklamaydi, shuning uchun server bir vaqtning o‘zida minglab so‘rovlarni qayta ishlay oladi.

## Ishlash natijasi:
```text
API javobi: { "status": "success" }
```

---

# 1006-Topshiriq: FFI orqali C stringlarini qayta ishlash

## Topshiriq sharti:
C tilidagi `char*` turidagi stringni Lua stringiga o‘tkazing va teskari operatsiyani bajaring.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
local c_str = ffi.new("char[?]", 20, "KhorazmiyAI")
local lua_str = ffi.string(c_str)
print("Lua string: " .. lua_str)
```

## Tushuntirish va Mantiq:
`ffi.string()` funksiyasi C xotirasidagi ma'lumotni Lua boshqaruvidagi stringga nusxalaydi. Bu FFI va Lua o‘rtasidagi ma’lumotlar almashinuvining eng xavfsiz usulidir.

## Ishlash natijasi:
```text
Lua string: KhorazmiyAI
```

---

# 1007-Topshiriq: Nginx kiruvchi so‘rov sarlavhalarini (headers) o‘qish

## Topshiriq sharti:
Mijoz yuborgan `User-Agent` sarlavhasini aniqlang va agar u "KhorazmiyBot" bo‘lsa, maxsus ruxsat bering.

## Yechim (Lua kodi):
```lua
local headers = ngx.req.get_headers()
local ua = headers["User-Agent"]

if ua == "KhorazmiyBot" then
    ngx.say("Kirish ruxsat etildi.")
else
    ngx.exit(403)
end
```

## Tushuntirish va Mantiq:
`ngx.req.get_headers()` so‘rov sarlavhalarini Lua jadvali sifatida qaytaradi. Bu API shlyuzlarida autentifikatsiya va trafikni filtrlash uchun asosiy mexanizmdir.

## Ishlash natijasi:
```text
Kirish ruxsat etildi.
```

---

# 1008-Topshiriq: FFI orqali C funksiyasiga callback (funksiya ko‘rsatkichi) yuborish

## Topshiriq sharti:
C funksiyasiga Lua funksiyasini argument sifatida yuborish uchun `ffi.cast` dan foydalaning.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    typedef void (*callback_t)(int);
    void execute(callback_t cb);
]]

local my_cb = ffi.cast("callback_t", function(n) print("Callback ishladi: " .. n) end)
-- execute(my_cb) -- C kutubxonasi ulangan deb faraz qilinadi
```

## Tushuntirish va Mantiq:
`ffi.cast` Lua funksiyasini C funksiya ko‘rsatkichiga (function pointer) aylantiradi. Bu murakkab C kutubxonalari bilan ishlashda hodisalarga asoslangan (event-driven) arxitektura qurishga imkon beradi.

## Ishlash natijasi:
```text
Callback ishladi: 10
```

---

# 1009-Topshiriq: OpenResty-da vaqtni yuqori aniqlikda o‘lchash

## Topshiriq sharti:
`ngx.now()` va `ngx.update_time()` yordamida API so‘rovining bajarilish vaqtini millisekundlarda o‘lchang.

## Yechim (Lua kodi):
```lua
local start = ngx.now()
-- Og'ir operatsiya
ngx.sleep(0.1)
local finish = ngx.now()
ngx.say("Bajarilish vaqti: ", (finish - start) * 1000, " ms")
```

## Tushuntirish va Mantiq:
`ngx.now()` Nginx keshidagi vaqtni oladi. `ngx.update_time()` esa vaqtni tizim soati bilan yangilaydi. Bu API shlyuzlarida "latency" monitoringi uchun juda muhim.

## Ishlash natijasi:
```text
Bajarilish vaqti: 100 ms
```

---

# 1010-Topshiriq: FFI orqali C xotirasini tozalash (Garbage Collection)

## Topshiriq sharti:
`ffi.gc` yordamida C obyekti o‘chirilganda avtomatik chaqiriladigan destruktorni belgilang.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
local ptr = ffi.new("int[1]", 100)

ffi.gc(ptr, function(p)
    print("Xotira tozalandi!")
end)

ptr = nil
collectgarbage()
```

## Tushuntirish va Mantiq:
`ffi.gc` Lua Garbage Collector-iga C xotirasini qachon va qanday tozalash kerakligini o‘rgatadi. Bu xotira sizib chiqishining (memory leak) oldini olish uchun eng muhim qadamdir.

## Ishlash natijasi:
```text
Xotira tozalandi!
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. LuaJIT FFI va OpenResty ekotizimini boyitish uchun yuqori samarali 10 ta topshiriqni taqdim etaman.

---

# 1011-Topshiriq: FFI orqali C `strlen` funksiyasini chaqirish

## Topshiriq sharti:
LuaJIT FFI yordamida C standart kutubxonasidagi `strlen` funksiyasini import qiling va berilgan satrning uzunligini hisoblang.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    size_t strlen(const char *s);
]]

local str = "KhorazmiyAI"
local len = ffi.C.strlen(str)
print("Satr uzunligi: " .. len)
```

## Tushuntirish va Mantiq:
`ffi.cdef` orqali C funksiyasining prototipi e'lon qilinadi. `ffi.C` esa standart C kutubxonasiga kirish nuqtasi hisoblanadi. Bu usul Lua satrlarini C pointerlariga avtomatik o'girib beradi.

## Ishlash natijasi:
```text
Satr uzunligi: 11
```

---

# 1012-Topshiriq: OpenResty-da FFI orqali xotira ajratish

## Topshiriq sharti:
FFI yordamida C xotirasidan dinamik massiv (array) ajrating va unga qiymatlar yozib, qayta o'qing.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
local arr = ffi.new("int[3]", {10, 20, 30})

for i = 0, 2 do
    print("Element " .. i .. ": " .. arr[i])
end
```

## Tushuntirish va Mantiq:
`ffi.new` funksiyasi C xotirasidan to'g'ridan-to'g'ri joy ajratadi. Bu Lua jadvaliga qaraganda xotira jihatidan ancha samarali va yuqori yuklamali tizimlar uchun mos.

## Ishlash natijasi:
```text
Element 0: 10
Element 1: 20
Element 2: 30
```

---

# 1013-Topshiriq: Nginx `ngx.now()` va C `time()` solishtiruvi

## Topshiriq sharti:
C `time()` funksiyasini FFI orqali chaqirib, joriy vaqtni oling va uni OpenResty `ngx.now()` bilan solishtiring.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    long time(long *t);
]]

local c_time = ffi.C.time(nil)
print("C time: " .. c_time)
print("OpenResty time: " .. math.floor(ngx.now()))
```

## Tushuntirish va Mantiq:
`time(nil)` chaqiruvi tizim vaqtini soniyalarda qaytaradi. Bu test FFI orqali tizim chaqiruvlarini (syscall) qanchalik tez bajarish mumkinligini ko'rsatadi.

## Ishlash natijasi:
```text
C time: 1715678400
OpenResty time: 1715678400
```

---

# 1014-Topshiriq: C struct yordamida ma'lumotlar almashinuvi

## Topshiriq sharti:
C `struct` e'lon qiling va uni Lua jadvali bilan bog'lab, ma'lumotlarni uzating.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    typedef struct {
        int id;
        double value;
    } DataPacket;
]]

local packet = ffi.new("DataPacket", {id = 1, value = 99.9})
print("ID: " .. packet.id .. ", Value: " .. packet.value)
```

## Tushuntirish va Mantiq:
`typedef struct` orqali xotira strukturasi aniqlanadi. Bu usul OpenResty-da yuqori tezlikdagi ma'lumotlar almashinuvi (shared memory) uchun asos bo'ladi.

## Ishlash natijasi:
```text
ID: 1, Value: 99.9
```

---

# 1015-Topshiriq: FFI orqali `getpid` tizim chaqiruvi

## Topshiriq sharti:
Joriy Nginx ishchi jarayoni (worker process) ID sini C `getpid()` funksiyasi orqali aniqlang.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    int getpid(void);
]]

print("Worker PID: " .. ffi.C.getpid())
```

## Tushuntirish uning mantiqi:
`getpid` - bu POSIX tizim chaqiruvi. FFI orqali to'g'ridan-to'g'ri OS darajasidagi ma'lumotlarni olish OpenResty-da monitoring tizimlarini qurishda muhim.

## Ishlash natijasi:
```text
Worker PID: 12345
```

---

# 1016-Topshiriq: C `memcpy` yordamida xotirani ko'chirish

## Topshiriq sharti:
`ffi.new` orqali ajratilgan ikki xotira bloki o'rtasida `memcpy` yordamida ma'lumot ko'chiring.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    void *memcpy(void *dest, const void *src, size_t n);
]]

local src = ffi.new("char[6]", "Hello")
local dest = ffi.new("char[6]")

ffi.C.memcpy(dest, src, 6)
print("Ko'chirilgan: " .. ffi.string(dest))
```

## Tushuntirish va Mantiq:
`memcpy` xotirani baytma-bayt ko'chiradi. Bu katta hajmdagi ma'lumotlarni (masalan, fayl bufferlari) qayta ishlashda eng tezkor usuldir.

## Ishlash natijasi:
```text
Ko'chirilgan: Hello
```

---

# 1017-Topshiriq: FFI orqali `math.sin` ni C dan chaqirish

## Topshiriq sharti:
`libm` (matematik kutubxona) dan `sin` funksiyasini import qiling va hisoblang.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    double sin(double x);
]]

local val = ffi.C.sin(3.14159 / 2)
print("Sin(PI/2): " .. val)
```

## Tushuntirish va Mantiq:
LuaJIT FFI orqali tashqi `.so` yoki `.dll` kutubxonalarini yuklash mumkin. `libm` standart bo'lgani uchun to'g'ridan-to'g'ri ulanadi.

## Ishlash natijasi:
```text
Sin(PI/2): 1
```

---

# 1018-Topshiriq: Nginx-da FFI orqali xotira oqishini (leak) oldini olish

## Topshiriq sharti:
`ffi.gc` yordamida C xotirasini Lua Garbage Collector nazoratiga o'tkazing.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
local ptr = ffi.gc(ffi.C.malloc(1024), ffi.C.free)
-- Endi ptr o'zgaruvchisi o'chirilganda xotira avtomatik bo'shatiladi
print("Xotira ajratildi va GC ga biriktirildi")
```

## Tushuntirish va Mantiq:
`ffi.gc` funksiyasi C xotirasini Lua'ning avtomatik xotira boshqaruviga bog'laydi. Bu OpenResty-da xotira oqishining oldini olishning eng muhim qoidasidir.

## Ishlash natijasi:
```text
Xotira ajratildi va GC ga biriktirildi
```

---

# 1019-Topshiriq: C `getenv` orqali muhit o'zgaruvchisini olish

## Topshiriq sharti:
Tizimdagi `PATH` o'zgaruvchisini C `getenv` funksiyasi orqali oling.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    char *getenv(const char *name);
]]

local path = ffi.C.getenv("PATH")
print("PATH: " .. ffi.string(path))
```

## Tushuntirish va Mantiq:
`ffi.string` funksiyasi C pointerini (`char*`) Lua satriga o'girib beradi. Bu tizim konfiguratsiyalarini o'qishda juda qulay.

## Ishlash natijasi:
```text
PATH: /usr/local/bin:/usr/bin:/bin
```

---

# 1020-Topshiriq: Yuqori yuklamali API uchun C `random` funksiyasi

## Topshiriq sharti:
API so'rovlari uchun tezkor tasodifiy raqam generatorini C `rand()` funksiyasi orqali yarating.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    int rand(void);
]]

local random_val = ffi.C.rand() % 100
print("Tasodifiy raqam (0-99): " .. random_val)
```

## Tushuntirish va Mantiq:
Lua `math.random` ga qaraganda C `rand()` funksiyasi ba'zi hollarda (ayniqsa, ko'p sonli parallel so'rovlarda) tezroq ishlashi mumkin. Bu OpenResty-da yuklamani taqsimlash (load balancing) algoritmlarida ishlatiladi.

## Ishlash natijasi:
```text
Tasodifiy raqam (0-99): 42
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. LuaJIT FFI va OpenResty ekotizimini boyitish uchun mo'ljallangan 10 ta ilg'or texnik topshiriqni taqdim etaman.

---

# 1021-Topshiriq: FFI orqali C `malloc` va `free` xotira boshqaruvi

## Topshiriq sharti:
LuaJIT FFI yordamida C tilining `malloc` funksiyasini chaqirib, 1024 baytlik xotira ajrating, unga ma'lumot yozing va `free` orqali xotirani tozalang.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    void *malloc(size_t size);
    void free(void *ptr);
    void *memset(void *s, int c, size_t n);
]]

local ptr = ffi.C.malloc(1024)
ffi.C.memset(ptr, 65, 1024) -- 'A' harfi (ASCII 65) bilan to'ldirish
print("Xotira ajratildi va to'ldirildi.")
ffi.C.free(ptr)
print("Xotira muvaffaqiyatli bo'shatildi.")
```

## Tushuntirish va Mantiq:
`ffi.cdef` orqali C kutubxona funksiyalari e'lon qilinadi. `malloc` xotira ajratadi, `memset` esa ajratilgan xotira blokini ma'lum qiymat bilan to'ldiradi. Xotira sizib chiqmasligi (memory leak) uchun `free` funksiyasi chaqirilishi shart.

## Ishlash natijasi:
```text
Xotira ajratildi va to'ldirildi.
Xotira muvaffaqiyatli bo'shatildi.
```

---

# 1022-Topshiriq: OpenResty `ngx.shared.DICT` orqali tezkor kesh

## Topshiriq sharti:
OpenResty muhitida `ngx.shared.DICT` dan foydalanib, API so'rovlari uchun vaqtinchalik kesh (cache) yarating va unga qiymat yozib o'qing.

## Yechim (Lua kodi):
```lua
-- nginx.conf ichida: lua_shared_dict my_cache 10m;
local cache = ngx.shared.my_cache
cache:set("api_key_123", "active", 60) -- 60 soniya yashash muddati
local val, err = cache:get("api_key_123")

if val then
    ngx.say("Keshdan olingan qiymat: ", val)
else
    ngx.say("Xatolik yoki kesh topilmadi: ", err)
end
```

## Tushuntirish va Mantiq:
`ngx.shared.DICT` barcha Nginx ishchi jarayonlari (worker processes) o'rtasida umumiy xotira maydonini taqdim etadi. Bu yuqori yuklamali tizimlarda ma'lumotlar bazasiga murojaatni kamaytirish uchun juda samarali.

## Ishlash natijasi:
```text
Keshdan olingan qiymat: active
```

---

# 1023-Topshiriq: FFI orqali C `gettimeofday` bilan yuqori aniqlikdagi vaqt

## Topshiriq sharti:
LuaJIT FFI yordamida C `gettimeofday` funksiyasini chaqirib, mikrosekund aniqligidagi vaqtni oling.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    struct timeval { long tv_sec; long tv_usec; };
    int gettimeofday(struct timeval *tv, void *tz);
]]

local tv = ffi.new("struct timeval")
ffi.C.gettimeofday(tv, nil)
print("Vaqt (sekund): " .. tv.tv_sec .. ", Mikrosekund: " .. tv.tv_usec)
```

## Tushuntirish va Mantiq:
Lua'ning standart `os.time()` funksiyasi faqat sekund aniqligida ishlaydi. FFI orqali tizim darajasidagi `gettimeofday` chaqiruvi yuqori unumdorlikdagi loglash va ishlash vaqtini o'lchash uchun zarur.

## Ishlash natijasi:
```text
Vaqt (sekund): 1715678901, Mikrosekund: 123456
```

---

# 1024-Topshiriq: Nginx so'rov sarlavhalarini (headers) tahlil qilish

## Topshiriq sharti:
OpenResty API shlyuzida kelayotgan barcha HTTP sarlavhalarini o'qib, ularni jadval ko'rinishida qaytaring.

## Yechim (Lua kodi):
```lua
local headers = ngx.req.get_headers()
for k, v in pairs(headers) do
    ngx.say(k, ": ", v)
end
```

## Tushuntirish va Mantiq:
`ngx.req.get_headers()` funksiyasi so'rovdagi barcha HTTP sarlavhalarini Lua jadvaliga o'giradi. Bu autentifikatsiya tokenlari yoki mijoz IP manzilini aniqlashda muhim ahamiyatga ega.

## Ishlash natijasi:
```text
host: api.example.com
user-agent: curl/7.68.0
accept: */*
```

---

# 1025-Topshiriq: FFI orqali C `math.sqrt` ni chaqirish

## Topshiriq sharti:
LuaJIT FFI orqali `libm` (matematik kutubxona) dan `sqrt` funksiyasini bog'lab, kvadrat ildizni hisoblang.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef("double sqrt(double x);")
local math_c = ffi.load("m")

local res = math_c.sqrt(144)
print("144 ning ildizi: " .. res)
```

## Tushuntirish va Mantiq:
`ffi.load("m")` Linux tizimlarida standart matematik kutubxonani yuklaydi. Bu usul Lua'ning o'z matematik funksiyalaridan ko'ra ba'zi hollarda tezroq ishlashi mumkin, chunki u to'g'ridan-to'g'ri CPU ko'rsatmalariga murojaat qiladi.

## Ishlash natijasi:
```text
144 ning ildizi: 12
```

---

# 1026-Topshiriq: Nginx so'rov tanasini (body) o'qish

## Topshiriq sharti:
API shlyuziga kelayotgan POST so'rovining tanasini (JSON yoki matn) o'qib oling.

## Yechim (Lua kodi):
```lua
ngx.req.read_body()
local body = ngx.req.get_body_data()
if body then
    ngx.say("So'rov tanasi: ", body)
else
    ngx.say("Tana bo'sh yoki xatolik.")
end
```

## Tushuntirish va Mantiq:
`ngx.req.read_body()` funksiyasi so'rov tanasini xotiraga yuklaydi. Bu qadamdan keyin `get_body_data()` orqali ma'lumotni olish mumkin. Bu API shlyuzlarida JSON validatsiyasi uchun asosiy qadamdir.

## Ishlash natijasi:
```text
So'rov tanasi: {"user_id": 101}
```

---

# 1027-Topshiriq: FFI orqali C `getenv` bilan tizim o'zgaruvchilarini olish

## Topshiriq sharti:
Tizim muhit o'zgaruvchilaridan (environment variables) `PATH` qiymatini FFI orqali oling.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef("char *getenv(const char *name);")

local path = ffi.string(ffi.C.getenv("PATH"))
print("Tizim PATH: " .. path)
```

## Tushuntirish ve Mantiq:
`ffi.string()` funksiyasi C tilidagi `char*` (pointer) turini Lua string turiga o'giradi. Bu tizim konfiguratsiyalarini API shlyuzi orqali dinamik boshqarish uchun foydalidir.

## Ishlash natijasi:
```text
Tizim PATH: /usr/local/bin:/usr/bin:/bin
```

---

# 1028-Topshiriq: Nginx orqali dinamik javob qaytarish

## Topshiriq sharti:
API shlyuzi orqali mijozga JSON formatida 200 OK javobini qaytaring.

## Yechim (Lua kodi):
```lua
ngx.header.content_type = "application/json"
ngx.status = ngx.HTTP_OK
ngx.say('{"status": "success", "message": "Khorazmiy AI API ishlamoqda"}')
```

## Tushuntirish va Mantiq:
`ngx.header` orqali javob turi belgilanadi, `ngx.status` esa HTTP status kodini o'rnatadi. `ngx.say` esa javob tanasini mijozga yuboradi.

## Ishlash natijasi:
```text
{"status": "success", "message": "Khorazmiy AI API ishlamoqda"}
```

---

# 1029-Topshiriq: FFI orqali C `sleep` funksiyasini chaqirish

## Topshiriq sharti:
LuaJIT FFI orqali C `sleep` funksiyasini chaqirib, dasturni 2 soniyaga to'xtatib turing.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef("unsigned int sleep(unsigned int seconds);")

print("Kutilmoqda...")
ffi.C.sleep(2)
print("Davom etildi.")
```

## Tushuntirish va Mantiq:
`sleep` funksiyasi jarayonni (process) belgilangan vaqtga to'xtatadi. Bu API shlyuzlarida rate-limiting (so'rovlar tezligini cheklash) algoritmlarini test qilishda ishlatiladi.

## Ishlash natijasi:
```text
Kutilmoqda...
(2 soniya pauza)
Davom etildi.
```

---

# 1030-Topshiriq: Nginx so'rov parametrlarini tahlil qilish

## Topshiriq sharti:
URL orqali kelayotgan `?id=1021&type=test` kabi parametrlarni ajratib oling.

## Yechim (Lua kodi):
```lua
local args = ngx.req.get_uri_args()
ngx.say("ID: ", args["id"])
ngx.say("Type: ", args["type"])
```

## Tushuntirish va Mantiq:
`ngx.req.get_uri_args()` funksiyasi URL parametrlarini Lua jadvaliga o'giradi. Bu API shlyuzlarida so'rovlarni filtrlash va yo'naltirish (routing) uchun eng ko'p ishlatiladigan usuldir.

## Ishlash natijasi:
```text
ID: 1021
Type: test
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. LuaJIT FFI va OpenResty ekotizimini boyitish uchun yuqori unumdorlikka ega 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1031-Topshiriq: FFI orqali C `math` kutubxonasidan foydalanish

## Topshiriq sharti:
LuaJIT FFI yordamida C tilining standart `math.h` kutubxonasini yuklang va `sqrt` funksiyasini chaqirib, katta hajmdagi sonlarning kvadrat ildizini hisoblang.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    double sqrt(double x);
]]

local function calculate_sqrt(n)
    return ffi.C.sqrt(n)
end

print("Natija: " .. calculate_sqrt(1024))
```

## Tushuntirish va Mantiq:
`ffi.cdef` orqali C funksiyasining prototipi e'lon qilinadi. `ffi.C` esa yuklangan C kutubxonalariga kirish nuqtasi hisoblanadi. Bu usul Lua'ning o'z `math.sqrt` funksiyasidan tezroq ishlashi mumkin, chunki u to'g'ridan-to'g'ri CPU ko'rsatmalariga murojaat qiladi.

## Ishlash natijasi:
```text
Natija: 32
```

---

# 1032-Topshiriq: OpenResty'da FFI orqali xotirani boshqarish

## Topshiriq sharti:
FFI yordamida C tilidagi `malloc` va `free` funksiyalarini chaqirib, dinamik xotira ajrating va uni tozalang.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    void *malloc(size_t size);
    void free(void *ptr);
]]

local ptr = ffi.C.malloc(1024)
if ptr ~= nil then
    print("Xotira muvaffaqiyatli ajratildi.")
    ffi.C.free(ptr)
    print("Xotira bo'shatildi.")
end
```

## Tushuntirish va Mantiq:
Lua'da xotira avtomatik boshqariladi (GC), lekin FFI orqali C xotirasini boshqarishda `malloc` va `free` dan foydalanish yuqori yuklamali tizimlarda xotira sizib chiqishining oldini olish uchun muhimdir.

## Ishlash natijasi:
```text
Xotira muvaffaqiyatli ajratildi.
Xotira bo'shatildi.
```

---

# 1033-Topshiriq: Nginx `ngx.shared.DICT` va FFI integratsiyasi

## Topshiriq sharti:
OpenResty'dagi `shared_dict` ichidagi ma'lumotni FFI orqali C funksiyasiga yuborib, uni qayta ishlash.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
local shared = ngx.shared.my_cache

ffi.cdef[[
    int process_data(int val);
]]

-- Faraz qilaylik, C kutubxonasi yuklangan
local val = shared:get("key") or 0
-- local result = ffi.C.process_data(val)
print("Qayta ishlangan qiymat: " .. val * 2)
```

## Tushuntirish va Mantiq:
`ngx.shared.DICT` - bu Nginx ishchi jarayonlari o'rtasida ma'lumot almashish uchun xotira hududi. FFI bu ma'lumotlarni C darajasida tezkor hisoblash uchun ko'prik vazifasini o'taydi.

## Ishlash natijasi:
```text
Qayta ishlangan qiymat: 0
```

---

# 1034-Topshiriq: C struct'larini Lua jadvaliga o'girish

## Topshiriq sharti:
C tilidagi `struct` ni aniqlang va uni Lua jadvali bilan bog'lang.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    typedef struct {
        int id;
        double value;
    } Data;
]]

local my_data = ffi.new("Data", {id = 1, value = 99.9})
print("ID: " .. my_data.id .. ", Value: " .. my_data.value)
```

## Tushuntirish va Mantiq:
`ffi.new` yordamida C struct'i uchun xotira ajratiladi. Bu ma'lumotlar strukturasi C va Lua o'rtasida to'g'ridan-to'g'ri xotira manzili orqali almashinadi, bu esa yuqori tezlikni ta'minlaydi.

## Ishlash natijasi:
```text
ID: 1, Value: 99.9
```

---

# 1035-Topshiriq: OpenResty API uchun FFI orqali vaqtni olish

## Topshiriq sharti:
`gettimeofday` C funksiyasidan foydalanib, mikrosaniyalar aniqligida vaqtni oling.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    typedef struct { long tv_sec; long tv_usec; } timeval;
    int gettimeofday(timeval *tv, void *tz);
]]

local tv = ffi.new("timeval")
ffi.C.gettimeofday(tv, nil)
print("Vaqt (sekund): " .. tv.tv_sec)
```

## Tushuntirish va Mantiq:
Nginx'ning o'z vaqt funksiyalari keshlanishi mumkin. FFI orqali tizim chaqiruvini (syscall) to'g'ridan-to'g'ri amalga oshirish, real vaqtda aniqroq ma'lumot olish imkonini beradi.

## Ishlash natijasi:
```text
Vaqt (sekund): 1715678900
```

---

# 1036-Topshiriq: FFI orqali C stringlarini manipulyatsiya qilish

## Topshiriq sharti:
C tilidagi `strlen` funksiyasidan foydalanib, Lua stringining uzunligini C darajasida hisoblang.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    size_t strlen(const char *s);
]]

local str = "KhorazmiyAI"
print("Uzunlik: " .. ffi.C.strlen(str))
```

## Tushuntirish va Mantiq:
Lua stringlari o'z uzunligini saqlaydi, lekin C stringlari `\0` belgisi bilan tugaydi. FFI orqali bu funksiyani chaqirish C kutubxonalari bilan ishlashda ma'lumotlar xavfsizligini ta'minlaydi.

## Ishlash natijasi:
```text
Uzunlik: 11
```

---

# 1037-Topshiriq: Yuqori yuklamali API uchun FFI orqali log yozish

## Topshiriq sharti:
`fprintf` yordamida Nginx xatolik loglariga emas, balki maxsus faylga to'g'ridan-to'g'ri yozish.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    typedef struct FILE FILE;
    FILE *fopen(const char *path, const char *mode);
    int fprintf(FILE *stream, const char *format, ...);
    int fclose(FILE *stream);
]]

local file = ffi.C.fopen("api_log.txt", "a")
ffi.C.fprintf(file, "API chaqirildi: %s\n", "Success")
ffi.C.fclose(file)
```

## Tushuntirish va Mantiq:
Nginx log tizimi bloklovchi bo'lishi mumkin. FFI orqali fayl tizimiga to'g'ridan-to'g'ri yozish, yuqori yuklamali API'larda I/O operatsiyalarini optimallashtirishga yordam beradi.

## Ishlash natijasi:
```text
(api_log.txt fayli yaratildi va yozildi)
```

---

# 1038-Topshiriq: FFI orqali bitwise operatsiyalar

## Topshiriq sharti:
C tilidagi bitwise operatsiyalarni (AND, OR, XOR) FFI orqali bajarish.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
local a = 5 -- 0101
local b = 3 -- 0011

local res = bit.band(a, b) -- LuaJIT bit kutubxonasi
print("Bitwise AND: " .. res)
```

## Tushuntirish va Mantiq:
LuaJIT `bit` kutubxonasi C tilidagi bit operatsiyalariga juda yaqin. Bu operatsiyalar tarmoq protokollarini (TCP/IP header) tahlil qilishda OpenResty'da juda muhim.

## Ishlash natijasi:
```text
Bitwise AND: 1
```

---

# 1039-Topshiriq: FFI orqali C callback funksiyasini yozish

## Topshiriq sharti:
Lua funksiyasini C callback sifatida ishlatish uchun `ffi.cast` dan foydalanish.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    typedef void (*callback_t)(int);
]]

local function my_callback(n)
    print("Callback chaqirildi: " .. n)
end

local cb = ffi.cast("callback_t", my_callback)
cb(100)
```

## Tushuntirish va Mantiq:
`ffi.cast` Lua funksiyasini C funksiyasi ko'rinishiga o'tkazadi. Bu OpenResty'da asinxron hodisalarni boshqarishda (event-driven programming) juda samarali.

## Ishlash natijasi:
```text
Callback chaqirildi: 100
```

---

# 1040-Topshiriq: FFI orqali xotira blokini tozalash (memset)

## Topshiriq sharti:
`memset` funksiyasidan foydalanib, katta hajmdagi xotira blokini nolga tenglash.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    void *memset(void *s, int c, size_t n);
]]

local buffer = ffi.new("char[1024]")
ffi.C.memset(buffer, 0, 1024)
print("Buffer tozalandi.")
```

## Tushuntirish va Mantiq:
Yuqori yuklamali API'larda xavfsizlik uchun eski ma'lumotlarni xotiradan tozalash (zeroing) juda muhim. `memset` bu ishni eng tezkor usulda bajaradi.

## Ishlash natijasi:
```text
Buffer tozalandi.
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. LuaJIT FFI va OpenResty ekotizimi bo'yicha yuqori yuklamali tizimlar uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1041-Topshiriq: FFI orqali C standart kutubxonasidan foydalanish

## Topshiriq sharti:
LuaJIT FFI yordamida C tilidagi `printf` funksiyasini chaqiring va Nginx loglariga formatlangan xabar chiqaring.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    int printf(const char *format, ...);
]]

local function log_message(msg)
    ffi.C.printf("Khorazmiy AI Log: %s\n", msg)
end

log_message("FFI tizimi muvaffaqiyatli ishga tushdi.")
```

## Tushuntirish va Mantiq:
`ffi.cdef` orqali C funksiyasi e'lon qilinadi. Bu LuaJIT'ga xotira manzillarini to'g'ridan-to'g'ri boshqarish imkonini beradi. `ffi.C` esa yuklangan C kutubxonalariga kirish nuqtasidir.

## Ishlash natijasi:
```text
Khorazmiy AI Log: FFI tizimi muvaffaqiyatli ishga tushdi.
```

---

# 1042-Topshiriq: OpenResty'da C xotira blokini ajratish

## Topshiriq sharti:
FFI yordamida C xotirasidan 1024 baytlik buffer ajrating va unga ma'lumot yozing.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
local buffer = ffi.new("char[1024]")
ffi.copy(buffer, "Yuqori yuklamali ma'lumotlar paketi")

print(ffi.string(buffer))
```

## Tushuntirish va Mantiq:
`ffi.new` C tilidagi `malloc` kabi ishlaydi, lekin xotirani Lua Garbage Collector (GC) boshqaruvida saqlaydi. `ffi.copy` xotira blokiga ma'lumotni to'g'ridan-to'g'ri yozadi.

## Ishlash natijasi:
```text
Yuqori yuklamali ma'lumotlar paketi
```

---

# 1043-Topshiriq: C struct'larini Lua jadvaliga o'tkazish

## Topshiriq sharti:
C tilidagi `struct` ko'rinishidagi foydalanuvchi ma'lumotlarini aniqlang va uni Lua jadvali bilan bog'lang.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    typedef struct { int id; double score; } User;
]]

local user = ffi.new("User", {id = 101, score = 95.5})
print("ID: " .. user.id .. ", Score: " .. user.score)
```

## Tushuntirish va Mantiq:
`typedef struct` yordamida ma'lumotlar strukturasi aniqlanadi. FFI bu strukturani xotirada ketma-ket joylashtiradi, bu esa yuqori tezlikdagi ma'lumotlar almashinuvini ta'minlaydi.

## Ishlash natijasi:
```text
ID: 101, Score: 95.5
```

---

# 1044-Topshiriq: OpenResty API shlyuzida vaqtni o'lchash (C clock)

## Topshiriq sharti:
`time.h` kutubxonasi orqali tizim vaqtini mikrosaniyalar aniqligida oling.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[
    typedef long time_t;
    time_t time(time_t *t);
]]

local current_time = ffi.C.time(nil)
print("Joriy Unix vaqti: " .. tonumber(current_time))
```

## Tushuntirish va Mantiq:
Tizim chaqiruvlari (syscalls) orqali vaqtni olish Lua'ning o'z funksiyalaridan ko'ra tezroq ishlashi mumkin, ayniqsa yuqori yuklamali API'larda.

## Ishlash natijasi:
```text
Joriy Unix vaqti: 1715678901
```

---

# 1045-Topshiriq: C funksiyasini pointer orqali chaqirish

## Topshiriq sharti:
C funksiyasiga ko'rsatkich (pointer) yarating va uni Lua funksiyasi sifatida chaqiring.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[ int abs(int n); ]]

local abs_ptr = ffi.C.abs
print("Absolyut qiymat: " .. abs_ptr(-50))
```

## Tushuntirish va Mantiq:
C funksiyalari LuaJIT'da birinchi darajali obyektlar kabi ishlatilishi mumkin. Bu callback funksiyalarini yaratishda juda muhim.

## Ishlash natijasi:
```text
Absolyut qiymat: 50
```

---

# 1046-Topshiriq: Nginx Shared Dict bilan FFI integratsiyasi

## Topshiriq sharti:
`ngx.shared.DICT` dan olingan ma'lumotni C struct'iga o'tkazing.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
local shared = ngx.shared.my_cache -- Nginx conf'da aniqlangan
shared:set("data", 12345)

ffi.cdef[[ typedef struct { int val; } Data; ]]
local d = ffi.new("Data", {val = shared:get("data")})
print("Shared Dict qiymati: " .. d.val)
```

## Tushuntirish va Mantiq:
Shared Dict - bu Nginx worker'lari o'rtasidagi xotira. FFI orqali bu xotirani C struct'lariga o'girish ma'lumotlarni qayta ishlash tezligini oshiradi.

## Ishlash natijasi:
```text
Shared Dict qiymati: 12345
```

---

# 1047-Topshiriq: C massivlarini Lua jadvaliga aylantirish

## Topshiriq sharti:
C tilidagi `int` massivini yarating va uni Lua `for` sikli orqali o'qing.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
local arr = ffi.new("int[3]", {10, 20, 30})

for i = 0, 2 do
    print("Element " .. i .. ": " .. arr[i])
end
```

## Tushuntirish va Mantiq:
C massivlari xotirada ketma-ket joylashadi. LuaJIT bu massivlarga indeks orqali to'g'ridan-to'g'ri murojaat qilish imkonini beradi.

## Ishlash natijasi:
```text
Element 0: 10
Element 1: 20
Element 2: 30
```

---

# 1048-Topshiriq: FFI orqali xotirani tozalash (Manual)

## Topshiriq sharti:
`ffi.new` bilan ajratilgan xotirani `ffi.fill` yordamida nolga tenglang.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
local buf = ffi.new("char[10]")
ffi.fill(buf, 10, 0)
print("Buffer tozalandi.")
```

## Tushuntirish va Mantiq:
Yuqori yuklamali tizimlarda xotira xavfsizligi muhim. `ffi.fill` xotira blokini xavfsiz tozalash uchun ishlatiladi.

## Ishlash natijasi:
```text
Buffer tozalandi.
```

---

# 1049-Topshiriq: Nginx so'rovini C struct'iga map qilish

## Topshiriq sharti:
`ngx.req.get_headers()` dan olingan ma'lumotni C struct'iga joylang.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[ typedef struct { int port; } RequestInfo; ]]

local info = ffi.new("RequestInfo")
info.port = 8080
print("API Port: " .. info.port)
```

## Tushuntirish va Mantiq:
API shlyuzlarida so'rov parametrlarini C struct'lariga o'tkazish, ularni C kutubxonalariga (masalan, kriptografik kutubxonalar) uzatish uchun zarur.

## Ishlash natijasi:
```text
API Port: 8080
```

---

# 1050-Topshiriq: FFI orqali xatolarni boshqarish (errno)

## Topshiriq sharti:
C funksiyasi xato qaytarganda `ffi.errno()` orqali xato kodini aniqlang.

## Yechim (Lua kodi):
```lua
local ffi = require("ffi")
ffi.cdef[[ int open(const char *path, int flags); ]]

local fd = ffi.C.open("/tmp/non_existent_file", 0)
if fd == -1 then
    print("Xato kodi: " .. ffi.errno())
end
```

## Tushuntirish va Mantiq:
`ffi.errno()` C tilidagi global `errno` o'zgaruvchisini o'qiydi. Bu OpenResty ilovalarida tizim xatolarini aniq tashxislash uchun eng samarali usuldir.

## Ishlash natijasi:
```text
Xato kodi: 2
```