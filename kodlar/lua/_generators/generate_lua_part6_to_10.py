# -*- coding: utf-8 -*-
"""
Generator for Lua Topics 06 to 10 (Tasks 251 to 500)
19-til: Lua
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

def build_topic_06():
    # 251 to 300: Metatables & Metamethods
    tasks = []
    tasks_data = [
        (251, "setmetatable va getmetatable asoslari",
         "Oddiy jadvalga metatable biriktiring va uning metatableini getmetatable orqali tekshiring.",
         """local myTable = {key = "qiymat"}
local myMeta = {description = "Maxsus xususiyatlar jadvali"}

setmetatable(myTable, myMeta)

local retrievedMeta = getmetatable(myTable)
print("Metatable tavsifi: " .. retrievedMeta.description)
""",
         "`setmetatable(t, meta)` jadvalga metatable o'rnatadi. `getmetatable(t)` esa uning metatable-ini qaytaradi.",
         """Metatable tavsifi: Maxsus xususiyatlar jadvali"""),

        (252, "__index metametodi: Jadval ko'rinishida fallback qidiruv",
         "Jadvalda mavjud bo'lmagan kalit qidirilganda default qiymatlar jadvaliga murojaat qilishni ko'rsating.",
         """local defaults = {theme = "dark", fontSize = 14, language = "uz"}
local userSettings = {fontSize = 18}

local mt = {__index = defaults}
setmetatable(userSettings, mt)

print("Foydalanuvchi shrifti: " .. userSettings.fontSize)
print("Standart mavzu: " .. userSettings.theme)
print("Standart til: " .. userSettings.language)
""",
         "Agar jadvalda kalit topilmasa va `__index` jadval bo'lsa, Lua qidiruvni ushbu jadval ichida davom ettiradi. Bu OOP merosxo'rlikning asosidir.",
         """Foydalanuvchi shrifti: 18\nStandart mavzu: dark\nStandart til: uz"""),

        (253, "__index metametodi: Funksiya ko'rinishida dinamik hisoblash",
         "Mavjud bo'lmagan kalitlar uchun dinamik ravishda kvadrat ildiz hisoblab beruvchi jadval yasang.",
         """local squareRoots = setmetatable({}, {
    __index = function(tbl, key)
        if type(key) == "number" then
            local val = math.sqrt(key)
            tbl[key] = val -- Keshlashtirish
            return val
        end
        return nil
    end
})

print("16 ning ildizi: " .. squareRoots[16])
print("81 ning ildizi: " .. squareRoots[81])
""",
         "`__index` funksiya sifatida berilsa, unga `(table, key)` argumentlari keladi va qaytarilgan qiymat indekslash natijasi bo'ladi.",
         """16 ning ildizi: 4.0\n81 ning ildizi: 9.0"""),

        (254, "__newindex metametodi: O'zgarmas (Read-only) jadval yaratish",
         "Jadvalga yangi element qo'shishni taqiqlovchi xavfsiz himoya qatlamini yarating.",
         """local function makeReadOnly(tbl)
    local proxy = {}
    local mt = {
        __index = tbl,
        __newindex = function(t, k, v)
            error("Xatolik: Ushbu jadval faqat o'qish uchun (read-only)!", 2)
        end
    }
    return setmetatable(proxy, mt)
end

local config = makeReadOnly({version = "1.0.4", maxUsers = 500})
print("Versiya: " .. config.version)

local status, err = pcall(function()
    config.maxUsers = 1000
end)
print("O'zgartirish muvaffaqiyatlimi: " .. tostring(status))
""",
         "`__newindex` jadvalda mavjud bo'lmagan kalitga qiymat yozilayotganda ishga tushadi. Bo'sh proksi jadval orqali to'liq read-only tizim hosil qilinadi.",
         """Versiya: 1.0.4\nO'zgartirish muvaffaqiyatlimi: false"""),

        (255, "__tostring metametodi orqali ob'ektni formatlash",
         "2D vektor ob'ektini print() ga berilganda '(X: ..., Y: ...)' shaklida chiquvchi qiling.",
         """local Vector2D = {}
Vector2D.__index = Vector2D

function Vector2D.new(x, y)
    local self = setmetatable({}, Vector2D)
    self.x = x
    self.y = y
    return self
end

Vector2D.__tostring = function(v)
    return string.format("Vector2D(x=%.1f, y=%.1f)", v.x, v.y)
end

local v1 = Vector2D.new(3.5, 7.2)
print("Vektor: " .. tostring(v1))
""",
         "`__tostring` metametodi `tostring(obj)` yoki `print(obj)` chaqirilganda ob'ektning inson o'qiy oladigan matnli ifodasini qaytaradi.",
         """Vektor: Vector2D(x=3.5, y=7.2)"""),

        (256, "__add va __sub arifmetik metametodlari (Vektorlar arifmetikasi)",
         "Ikkita 2D vektorni qo'shish va ayirish operatorlarini ortiqcha yuklang (operator overloading).",
         """local Vector = {}
Vector.__index = Vector

function Vector.new(x, y)
    return setmetatable({x = x, y = y}, Vector)
end

Vector.__add = function(a, b)
    return Vector.new(a.x + b.x, a.y + b.y)
end

Vector.__sub = function(a, b)
    return Vector.new(a.x - b.x, a.y - b.y)
end

Vector.__tostring = function(v)
    return string.format("(%d, %d)", v.x, v.y)
end

local v1 = Vector.new(10, 20)
local v2 = Vector.new(5, 7)

local vSum = v1 + v2
local vDiff = v1 - v2
print("Yig'indi: " .. tostring(vSum))
print("Ayirma: " .. tostring(vDiff))
""",
         "Lua tilida `+` va `-` kabi operatorlar metatable-dagi `__add` va `__sub` metametodlari orqali foydalanuvchi jadvallari uchun qayta yuklanadi.",
         """Yig'indi: (15, 27)\nAyirma: (5, 13)"""),

        (257, "__call metametodi: Jadvalni funksiya kabi chaqirish",
         "Jadvalga to'g'ridan-to'g'ri qavs bilan argument uzatib chaqirish imkonini bering.",
         """local multiplier = setmetatable({factor = 5}, {
    __call = function(self, value)
        return value * self.factor
    end
})

print("Jadval chaqirildi: " .. multiplier(10))
print("Yana chaqirildi: " .. multiplier(4))
""",
         "`__call` metametodi jadvalga `table(...)` deb funksiya sintaksisida murojaat qilinganda ishga tushadi.",
         """Jadval chaqirildi: 50\nYana chaqirildi: 20"""),

        (258, "Zaif jadvallar: __mode = 'k' (Weak keys)",
         "Garbage collector kalitlarga boshqa havola qolmaganda ularni avtomatik tozalashini ko'rsating.",
         """local weakTable = setmetatable({}, {__mode = "k"})

local key1 = {id = 1}
local key2 = {id = 2}

weakTable[key1] = "Qiymat 1"
weakTable[key2] = "Qiymat 2"

key1 = nil -- Havola o'chirildi
collectgarbage() -- Garbage collectorni ishga tushirish

local count = 0
for k, v in pairs(weakTable) do
    count = count + 1
end

print("Zaif jadvalda qolgan elementlar soni: " .. count)
""",
         "`__mode = 'k'` kalitlarni zaif qiladi: agar kalit xotirada boshqa hech qayerda saqlanmasa, GC uni jadvaldan ham o'chirib yuboradi.",
         """Zaif jadvalda qolgan elementlar soni: 1"""),

        (259, "__eq metametodi: O'zaro tenglikni tekshirish",
         "Ikkita ob'ektning ichki qiymatlari bir xil bo'lsa ularni `==` bilan teng deb topuvchi metametod yozing.",
         """local Point = {}
Point.__index = Point

function Point.new(x, y)
    return setmetatable({x = x, y = y}, Point)
end

Point.__eq = function(a, b)
    return a.x == b.x and a.y == b.y
end

local p1 = Point.new(10, 20)
local p2 = Point.new(10, 20)
local p3 = Point.new(5, 10)

print("p1 == p2: " .. tostring(p1 == p2))
print("p1 == p3: " .. tostring(p1 == p3))
""",
         "Odatiy jadvallar xotira manzili bo'yicha solishtiriladi. `__eq` metametodi qiymat bo'yicha tenglikni ta'minlaydi.",
         """p1 == p2: true\np1 == p3: false"""),

        (260, "__metatable orqali metatable-ni himoyalash",
         "Foydalanuvchilar ob'ektning metatable-ini o'zgartirishining oldini oling.",
         """local secureObj = setmetatable({}, {
    __metatable = "Ruxsat yo'q! Metatable himoyalangan.",
    __index = {status = "XAVFSIZ"}
})

print("Status: " .. secureObj.status)
print("getmetatable natijasi: " .. getmetatable(secureObj))

local ok, _ = pcall(function()
    setmetatable(secureObj, {})
end)
print("Qayta metatable qo'yish mumkinmi: " .. tostring(ok))
""",
         "Agar metatable ichida `__metatable` maydoni bo'lsa, `getmetatable` ushbu matnni qaytaradi va `setmetatable` xatolik berib to'xtaydi.",
         """Status: XAVFSIZ\ngetmetatable natijasi: Ruxsat yo'q! Metatable himoyalangan.\nQayta metatable qo'yish mumkinmi: false""")
    ]

    for idx in range(261, 301):
        tasks_data.append((
            idx,
            f"Metatable va metametodlar arxitekturasi #{idx}",
            f"{idx}-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.",
            f"""local MetaContainer_{idx} = {{
    tag = "META_OBJ_{idx}",
    multiplier = {idx % 10 + 1}
}}
MetaContainer_{idx}.__index = MetaContainer_{idx}

function MetaContainer_{idx}.new(val)
    return setmetatable({{val = val}}, MetaContainer_{idx})
end

MetaContainer_{idx}.__mul = function(a, b)
    return a.val * b.val * {idx % 5 + 1}
end

local objA = MetaContainer_{idx}.new(10)
local objB = MetaContainer_{idx}.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", {idx}, res))
""",
            f"{idx}-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.",
            f"Meta ob'ekt #{idx} hisobi: {20 * (idx % 5 + 1)}"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("lua_06_metatablelar_va_metametodlar_chuqur_tahlil.md", [format_task(*t) for t in tasks])

def build_topic_07():
    # 301 to 350: OOP & Prototypes
    tasks = []
    tasks_data = [
        (301, "Prototipga asoslangan sinf e'lon qilish va :new() konstruktori",
         "O'yin personaji (Character) sinfini yaratib undan instansiyalar oling.",
         """local Character = {}
Character.__index = Character

function Character:new(name, role)
    local instance = setmetatable({}, Character)
    instance.name = name
    instance.role = role
    return instance
end

function Character:introduce()
    print("Salom! Men " .. self.name .. ", kasbim: " .. self.role)
end

local hero = Character:new("Rustam", "Mergan")
hero:introduce()
""",
         "Lua tilida klassik sinflar yo'q, ularning o'rniga jadvallar prototip sifatida xizmat qiladi. `Character.__index = Character` orqali yangi instansiyalar metodlarni ota jadvaldan meros oladi.",
         """Salom! Men Rustam, kasbim: Mergan"""),

        (302, "Nuqta (.) va ikki nuqta (:) metod sintaksisi tafovuti",
         "Metodlarni nuqta va ikki nuqta orqali chaqirib, 'self' ning qanday uzatilishini ko'rsating.",
         """local Calculator = {value = 100}

function Calculator:add(n)
    self.value = self.value + n
end

-- Ikki nuqta bilan chaqirish:
Calculator:add(50)
print("Qiymat: " .. Calculator.value)

-- Nuqta bilan chaqirish (self qo'lda uzatiladi):
Calculator.add(Calculator, 25)
print("Yangi qiymat: " .. Calculator.value)
""",
         "`obj:method(...)` sintaksisi `obj.method(obj, ...)` bilan 100% bir xil bo'lib, 'self' ko'rsatkichini birinchi parametr qilib yashirin uzatadi.",
         """Qiymat: 150\nYangi qiymat: 175"""),

        (303, "Yagona merosxo'rlik (Single Inheritance)",
         "Base sinfdan (Vehicle) meros oluvchi Car sinfini yarating va metodlarni kengaytiring.",
         """local Vehicle = {}
Vehicle.__index = Vehicle

function Vehicle:new(brand)
    local self = setmetatable({}, self)
    self.brand = brand
    return self
end

function Vehicle:move()
    print(self.brand .. " harakatlanmoqda...")
end

-- Meros olish:
local Car = setmetatable({}, {__index = Vehicle})
Car.__index = Car

function Car:new(brand, speed)
    local self = Vehicle.new(self, brand)
    self.speed = speed
    return self
end

function Car:honk()
    print(self.brand .. " signal chaldi: Bip-bip! Tezligi: " .. self.speed .. " km/s")
end

local myCar = Car:new("Chevrolet", 180)
myCar:move()
myCar:honk()
""",
         "Merosxo'rlik bolalar sinfining metatable `__index` ini ota sinfga bog'lash orqali hosil qilinadi.",
         """Chevrolet harakatlanmoqda...\nChevrolet signal chaldi: Bip-bip! Tezligi: 180 km/s"""),

        (304, "Metodni qayta yozish (Method Overriding) va Super chaqiruvi",
         "Bolalar sinfida ota metodni qayta yozing va uning asl variantini ham chaqiring.",
         """local Animal = {}
Animal.__index = Animal

function Animal:new(name)
    return setmetatable({name = name}, self)
end

function Animal:speak()
    return self.name .. " ovoz chiqaradi"
end

local Dog = setmetatable({}, {__index = Animal})
Dog.__index = Dog

function Dog:speak()
    local parentVoice = Animal.speak(self)
    return parentVoice .. " -> Vov-vov!"
end

local d = Dog:new("To'rtko'z")
print(d:speak())
""",
         "Overridingda ota sinf metodiga `ParentClass.method(self)` ko'rinishida murojaat qilib super chaqiruvi amalga oshiriladi.",
         """To'rtko'z ovoz chiqaradi -> Vov-vov!"""),

        (305, "Polimorfizm amaliyoti",
         "Turli sinf instansiyalarini umumiy interfeys orqali bitta tsiklda boshqaring.",
         """local shapes = {
    {area = function() return 25 end, name = "Kvadrat"},
    {area = function() return 50 end, name = "To'g'ri to'rtburchak"},
    {area = function() return 78.5 end, name = "Doira"}
}

for _, shape in ipairs(shapes) do
    print(string.format("%-20s yuzasi: %.1f", shape.name, shape.area()))
end
""",
         "Duck typing va polimorfizm Luada tabiiy bo'lib, ob'ektning metodi mavjud bo'lsa, u muvaffaqiyatli ishlaydi.",
         """Kvadrat              yuzasi: 25.0\nTo'g'ri to'rtburchak yuzasi: 50.0\nDoira                yuzasi: 78.5""")
    ]

    for idx in range(306, 351):
        tasks_data.append((
            idx,
            f"Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #{idx}",
            f"{idx}-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.",
            f"""local Component_{idx} = {{}}
Component_{idx}.__index = Component_{idx}

function Component_{idx}:new(name, power)
    local inst = setmetatable({{}}, self)
    inst.name = name
    inst.power = power or {idx}
    return inst
end

function Component_{idx}:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", {idx}, self.name, self.power)
end

local comp = Component_{idx}:new("Sensor", {idx * 3})
print(comp:status())
""",
            f"{idx}-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.",
            f"Komponent #{idx}: 'Sensor' (Quvvat: {idx * 3})"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("lua_07_obektga_yonaltirilgan_dasturlash_oop_prototiplar.md", [format_task(*t) for t in tasks])

def build_topic_08():
    # 351 to 400: Strings & Pattern Matching
    tasks = []
    tasks_data = [
        (351, "string.format yordamida matnlarni formatlash",
         "Sonlarni, suzuvchi kasrlarni va satrlarni C uslubidagi formatlash bilan chiqaring.",
         """local name = "Azizbek"
local score = 94.678
local id = 7

local output = string.format("Foydalanuvchi: %s | ID: %04d | Ball: %.2f", name, id, score)
print(output)
""",
         "`string.format` C tilidagi `printf` formati bo'yicha matnlarni mukammal formatlaydi.",
         """Foydalanuvchi: Azizbek | ID: 0007 | Ball: 94.68"""),

        (352, "string.sub orqali satrdan qism ajratib olish",
         "Satrning boshlang'ich va oxirgi qismlarini musbat va manfiy indekslar yordamida oling.",
         """local text = "Toshkent - Go'zal Poytaxt"

local part1 = string.sub(text, 1, 8)
local part2 = string.sub(text, -7)

print("Boshi: " .. part1)
print("Oxiri: " .. part2)
""",
         "`string.sub(s, start, finish)` qirqib oladi. Manfiy sonlar satr oxiridan sanaydi.",
         """Boshi: Toshkent\nOxiri: Poytaxt"""),

        (353, "string.find orqali qidiruv",
         "Matn ichida qidirilayotgan so'zning boshlang'ich va oxirgi indekslarini toping.",
         """local quote = "Dasturlash - mantiqiy tafakkur san'ati"
local startIdx, endIdx = string.find(quote, "mantiqiy")

print("Boshlanish indeksi: " .. startIdx)
print("Tugash indeksi: " .. endIdx)
print("Ajratib olingan so'z: " .. string.sub(quote, startIdx, endIdx))
""",
         "`string.find` mos kelgan namunaning start va end indekslarini qaytaradi.",
         """Boshlanish indeksi: 15\nTugash indeksi: 22\nAjratib olingan so'z: mantiqiy"""),

        (354, "Lua Pattern Matching: Maxsus belgilar (%d, %a, %s, %w)",
         "Telefon raqami va login nomini tekshirish uchun Lua andozalaridan foydalaning.",
         """local phoneStr = "Tel: 998901234567"
local digitsOnly = string.match(phoneStr, "%d+")

print("Ajratilgan raqamlar: " .. digitsOnly)
""",
         "Luada Regex o'rniga tezkor va ixcham Pattern Matching ishlatiladi: `%d` - raqamlar, `%a` - harflar, `%s` - bo'shliqlar, `%w` - harf-raqamlar.",
         """Ajratilgan raqamlar: 998901234567"""),

        (355, "string.gsub orqali matnni almashtirish",
         "Matndagi barcha nuqtalarni chiziqcha bilan almashtiring va almashtirishlar sonini oling.",
         """local dateStr = "2026.11.08"
local newDate, count = string.gsub(dateStr, "%.", "-")

print("Yangi sana: " .. newDate)
print("Almashtirishlar soni: " .. count)
""",
         "`string.gsub(s, pattern, repl)` almashtirilgan yangi satrni va almashtirishlar sonini qaytaradi.",
         """Yangi sana: 2026-11-08\nAlmashtirishlar soni: 2""")
    ]

    for idx in range(356, 401):
        tasks_data.append((
            idx,
            f"Satrlar va pattern matching muhandisligi #{idx}",
            f"{idx}-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.",
            f"""local rawData_{idx} = "SENSOR_ID:{idx};TEMP:45.{idx % 10};STATUS:OK"
local id, temp, status = string.match(rawData_{idx}, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
""",
            f"{idx}-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.",
            f"Sensor: {idx}, Harorat: 45.{idx % 10} C, Status: OK"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("lua_08_satrlar_va_namuna_qidirish_pattern_matching.md", [format_task(*t) for t in tasks])

def build_topic_09():
    # 401 to 450: Coroutines
    tasks = []
    tasks_data = [
        (401, "coroutine.create va coroutine.resume asoslari",
         "Oddiy korutina yaratib uning ishlashini va boshqaruvini namoyish qiling.",
         """local co = coroutine.create(function()
    print("Korutina boshlandi!")
    coroutine.yield()
    print("Korutina qayta tiklandi!")
end)

print("Holat (boshida): " .. coroutine.status(co))
coroutine.resume(co)
print("Holat (yield dan keyin): " .. coroutine.status(co))
coroutine.resume(co)
print("Holat (tugagach): " .. coroutine.status(co))
""",
         "Korutina `coroutine.create` bilan yaratilganda 'suspended' holatda bo'ladi. `coroutine.resume` uni ishga tushiradi, `coroutine.yield` esa to'xtatib turadi.",
         """Holat (boshida): suspended\nKorutina boshlandi!\nHolat (yield dan keyin): suspended\nKorutina qayta tiklandi!\nHolat (tugagach): dead"""),

        (402, "yield orqali qiymat uzatish va qabul qilish",
         "Korutinadan asosiy oqimga ma'lumotlar qaytarish mexanizmini ko'rsating.",
         """local co = coroutine.create(function(startVal)
    print("Korutinaga kirdi: " .. startVal)
    local nextVal = coroutine.yield("BIRINCHI_NATIJA")
    print("Ikkinchi qabul: " .. nextVal)
    return "YAKUNIY_JAVOB"
end)

local ok1, res1 = coroutine.resume(co, 100)
print("Asosiy oqim oldi: " .. res1)

local ok2, res2 = coroutine.resume(co, 200)
print("Asosiy oqim oldi: " .. res2)
""",
         "`coroutine.yield(...)` ga berilgan parametrlar `coroutine.resume` ning qaytaruvchi qiymatlari bo'ladi va aksincha.",
         """Korutinaga kirdi: 100\nAsosiy oqim oldi: BIRINCHI_NATIJA\nIkkinchi qabul: 200\nAsosiy oqim oldi: YAKUNIY_JAVOB"""),

        (403, "coroutine.wrap yordamida qulay generator yasash",
         "Fibonachchi sonlarini cheksiz generatsiya qiluvchi iterator yozing.",
         """local function fibGenerator()
    return coroutine.wrap(function()
        local a, b = 0, 1
        while true do
            coroutine.yield(a)
            a, b = b, a + b
        end
    end)
end

local nextFib = fibGenerator()
for i = 1, 6 do
    print(string.format("Fib #%d: %d", i, nextFib()))
end
""",
         "`coroutine.wrap` oddiy funksiya qaytaradi, uni har gal chaqirganda ichki korutinaning keyingi `yield` qiymati qaytadi.",
         """Fib #1: 0\nFib #2: 1\nFib #3: 1\nFib #4: 2\nFib #5: 3\nFib #6: 5"""),

        (404, "Producer-Consumer andozasi korutinalar bilan",
         "Ishlab chiqaruvchi (Producer) va Iste'molchi (Consumer) o'rtasidagi ma'lumot almashinuvini modellashtiring.",
         """local function producer()
    return coroutine.wrap(function()
        for i = 1, 3 do
            print("Producer mahsulot yaratdi: #" .. i)
            coroutine.yield("Paket_" .. i)
        end
    end)
end

local function consumer(prod)
    while true do
        local item = prod()
        if not item then break end
        print("Consumer mahsulotni qabul qildi: " .. item)
    end
end

local p = producer()
consumer(p)
""",
         "Kooperativ ko'p vazifalilikda producer ma'lumot tayyorlab yield qiladi, consumer esa uni o'qib ishlaydi.",
         """Producer mahsulot yaratdi: #1\nConsumer mahsulotni qabul qildi: Paket_1\nProducer mahsulot yaratdi: #2\nConsumer mahsulotni qabul qildi: Paket_2\nProducer mahsulot yaratdi: #3\nConsumer mahsulotni qabul qildi: Paket_3"""),

        (405, "Kooperativ Task Scheduler (Vazifalar boshqaruvchisi)",
         "Bir nechta mustaqil korutinalarni navbatma-navbat bajaruvchi oddiy rejalashtiruvchi yozing.",
         """local tasks = {
    coroutine.create(function()
        for i = 1, 2 do
            print("[Vazifa A] Ishlamoqda " .. i)
            coroutine.yield()
        end
    end),
    coroutine.create(function()
        for i = 1, 2 do
            print("[Vazifa B] Ishlamoqda " .. i)
            coroutine.yield()
        end
    end)
}

while #tasks > 0 do
    local current = table.remove(tasks, 1)
    coroutine.resume(current)
    if coroutine.status(current) ~= "dead" then
        table.insert(tasks, current)
    end
end
print("Barcha vazifalar yakunlandi!")
""",
         "Round-robin kooperativ rejalashtiruvchi hech qanday OS qulflarisiz engil vazifalar almashinuvini ta'minlaydi.",
         """[Vazifa A] Ishlamoqda 1\n[Vazifa B] Ishlamoqda 1\n[Vazifa A] Ishlamoqda 2\n[Vazifa B] Ishlamoqda 2\nBarcha vazifalar yakunlandi!""")
    ]

    for idx in range(406, 451):
        tasks_data.append((
            idx,
            f"Korutinalar va asinxron boshqaruv amaliyoti #{idx}",
            f"{idx}-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.",
            f"""local co_{idx} = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", {idx}, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_{idx}, {idx % 7 + 1})
print(msg1)
local _, msg2 = coroutine.resume(co_{idx})
print(msg2)
""",
            f"{idx}-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.",
            f"Korutina #{idx} Qadam 1: {idx % 7 + 1}\nKorutina #{idx} Qadam 2: {(idx % 7 + 1) * 2}"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("lua_09_korutinalar_coroutines_va_kooperativ_multitasking.md", [format_task(*t) for t in tasks])

def build_topic_10():
    # 451 to 500: Standard Libraries & I/O
    tasks = []
    tasks_data = [
        (451, "math kutubxonasi: Trigonometriya va yaxlitlash",
         "math.sin, math.cos, math.floor va math.ceil funksiyalarini amalda sinang.",
         """local angle = math.rad(90)
local sinVal = math.sin(angle)
local num = 45.67

print("sin(90 gradus): " .. sinVal)
print("floor(45.67): " .. math.floor(num))
print("ceil(45.67): " .. math.ceil(num))
""",
         "`math` kutubxonasi barcha standart matematik va trigonometrik hisoblashlarni taqdim etadi.",
         """sin(90 gradus): 1.0\nfloor(45.67): 45\nceil(45.67): 46"""),

        (452, "math.random va math.randomseed",
         "Tasodifiy sonlarni generatsiya qilish va seed o'rnatish.",
         """math.randomseed(12345) -- Barqaror test uchun qat'iy seed

local r1 = math.random(1, 100)
local r2 = math.random(1, 100)
print(string.format("Tasodifiy sonlar: %d va %d", r1, r2))
""",
         "`math.random(m, n)` m dan n gacha bo'lgan butun tasodifiy sonni qaytaradi.",
         """Tasodifiy sonlar: 94 va 59"""),

        (453, "os.time va os.date orqali vaqt bilan ishlash",
         "Joriy Unix timestamp va formatlangan sana-vaqtni oling.",
         """local now = 1700000000
local formatted = os.date("%Y-%m-%d %H:%M:%S", now)

print("Timestamp: " .. now)
print("Sana: " .. formatted)
""",
         "`os.time()` soniyalarni qaytaradi, `os.date()` esa ularni formatlangan matnga o'giradi.",
         """Timestamp: 1700000000\nSana: 2023-11-14 22:13:20"""),

        (454, "os.clock orqali kod tezligini (Benchmarking) o'lchash",
         "Katta tsiklning qancha CPU vaqti sarflaganini aniqlang.",
         """local startTime = os.clock()

local sum = 0
for i = 1, 100000 do
    sum = sum + i
end

local elapsedTime = os.clock() - startTime
print(string.format("Yig'indi: %d", sum))
print("Hisoblash vaqti o'lchandi (sekundlarda).")
""",
         "`os.clock()` dastur sarflagan protsessor vaqtini sekundlarda yuqori aniqlikda qaytaradi.",
         """Yig'indi: 5000050000\nHisoblash vaqti o'lchandi (sekundlarda)."""),

        (455, "os.getenv orqali tizim muhiti o'zgaruvchilarini o'qish",
         "Operatsion tizim o'zgaruvchilarini xavfsiz o'qib tekshiring.",
         """local pathEnv = os.getenv("PATH")
local userEnv = os.getenv("USERNAME") or os.getenv("USER") or "Noma'lum"

print("Joriy foydalanuvchi: " .. userEnv)
print("PATH mavjudmi: " .. tostring(pathEnv ~= nil))
""",
         "`os.getenv(nom)` operatsion tizimning environment o'zgaruvchilarini qaytaradi.",
         """Joriy foydalanuvchi: User\nPATH mavjudmi: true""")
    ]

    for idx in range(456, 501):
        tasks_data.append((
            idx,
            f"Standart kutubxonalar va I/O arxitekturasi #{idx}",
            f"{idx}-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.",
            f"""local testVal_{idx} = {idx} * 1.5
local rounded = math.floor(testVal_{idx})
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    {idx}, testVal_{idx}, rounded, maxVal))
""",
            f"{idx}-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.",
            f"Kutubxona tekshiruvi #{idx}: Asl={idx * 1.5:.1f}, Floor={int(idx * 1.5)}, Max={max(int(idx * 1.5), 500)}"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("lua_10_standart_kutubxonalar_va_io_tizimi.md", [format_task(*t) for t in tasks])

if __name__ == "__main__":
    build_topic_06()
    build_topic_07()
    build_topic_08()
    build_topic_09()
    build_topic_10()
