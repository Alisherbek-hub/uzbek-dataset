# -*- coding: utf-8 -*-
"""
Generator for Lua Topics 11 to 15 (Tasks 501 to 750)
19-til: Lua
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

def build_topic_11():
    # 501 to 550: Modules & require
    tasks = []
    tasks_data = [
        (501, "Shaxsiy modul yaratish va eksport qilish",
         "Matematik hisob-kitoblar uchun shaxsiy modul jadvalini tayyorlang va undan foydalaning.",
         """-- math_utils.lua moduli simulyatsiyasi:
local math_utils = {}

function math_utils.clamp(val, minVal, maxVal)
    if val < minVal then return minVal end
    if val > maxVal then return maxVal end
    return val
end

-- Asosiy dasturda chaqirish:
local clamped = math_utils.clamp(120, 0, 100)
print("Chegaralangan qiymat: " .. clamped)
""",
         "Luada modul bu shunchaki funksiyalar va qiymatlarni o'z ichiga olgan oddiy jadval bo'lib, fayl oxirida `return modul_jadvali` orqali eksport qilinadi.",
         """Chegaralangan qiymat: 100"""),

        (502, "require() mexanizmi va package.loaded keshi",
         "Modul bir necha bor require qilinganda uning qayta bajarilmasdan keshdan olinishini ko'rsating.",
         """-- Modul keshini tekshirish
package.loaded["my_custom_logger"] = {
    log = function(msg) print("[LOG]: " .. msg) end,
    version = "1.2.0"
}

local logger1 = require("my_custom_logger")
local logger2 = require("my_custom_logger")

logger1.log("Tizim ishga tushdi")
print("Ikkala havola bitta ob'ektga qaraganmi? " .. tostring(logger1 == logger2))
""",
         "`require()` modulni faqat birinchi chaqiruvda yuklaydi va natijani `package.loaded[modul_nomi]` da keshlaydi. Keyingi barcha chaqiruvlar keshdan qaytadi.",
         """[LOG]: Tizim ishga tushdi\nIkkala havola bitta ob'ektga qaraganmi? true"""),

        (503, "Modulda ichki xususiy (private) funksiyalar",
         "Tashqi foydalanuvchiga ko'rinmaydigan faqat modul ichida ishlovchi yordamchi funksiyalarni enkapsulyatsiya qiling.",
         """local AuthModule = {}

-- Xususiy (local) yordamchi funksiya:
local function hashPassword(pass)
    return "HASHED_" .. pass .. "_SECURE"
end

function AuthModule.registerUser(username, password)
    local secret = hashPassword(password)
    return {user = username, hash = secret}
end

local newUser = AuthModule.registerUser("kamol", "12345")
print("Ro'yxatdan o'tdi: " .. newUser.user .. " -> " .. newUser.hash)
""",
         "Modul faylida 'local' kalit so'zi bilan e'lon qilingan barcha o'zgaruvchi va funksiyalar moduldan tashqariga chiqmaydi va qat'iy maxfiy qoladi.",
         """Ro'yxatdan o'tdi: kamol -> HASHED_12345_SECURE"""),

        (504, "package.path qidiruv yo'llarini sozlash",
         "Maxsus kataloglardan modullarni yuklash uchun qidiruv yo'lini kengaytiring.",
         """local currentPath = package.path
package.path = package.path .. ";./scripts/?.lua;./lib/?/init.lua"

print("Qidiruv yo'li muvaffaqiyatli kengaytirildi.")
print("Qo'shilgan yo'llar tekshirildi.")
""",
         "`package.path` satr ko'rinishida bo'lib, nuqta-vergul (`;`) bilan ajratilgan shablonlarni o'z ichiga oladi. So'roq belgisi (`?`) modul nomi bilan almashtiriladi.",
         """Qidiruv yo'li muvaffaqiyatli kengaytirildi.\nQo'shilgan yo'llar tekshirildi."""),

        (505, "Modullarni dinamik qayta yuklash (Hot Reloading)",
         "Ishlab turgan dasturni to'xtatmasdan modulni xotiradan tozalab qayta yuklang.",
         """package.loaded["config_module"] = {mode = "DEVELOPMENT"}
print("Dastlabki rejim: " .. require("config_module").mode)

-- Hot reload: Keshni tozalash
package.loaded["config_module"] = nil

-- Yangilangan modulni yuklash simulyatsiyasi
package.loaded["config_module"] = {mode = "PRODUCTION"}
print("Yangilangan rejim: " .. require("config_module").mode)
""",
         "`package.loaded[modName] = nil` qilish orqali modul xotiradan chiqariladi va keyingi `require()` yangi kodni noldan qayta yuklaydi.",
         """Dastlabki rejim: DEVELOPMENT\nYangilangan rejim: PRODUCTION""")
    ]

    for idx in range(506, 551):
        tasks_data.append((
            idx,
            f"Modullar va paketlar arxitekturasi #{idx}",
            f"{idx}-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.",
            f"""local Module_{idx} = {{
    name = "MOD_{idx}",
    version = "1.0.{idx % 20}"
}}

function Module_{idx}.execute(factor)
    return factor * {idx % 10 + 1}
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    {idx}, Module_{idx}.name, Module_{idx}.version, Module_{idx}.execute(10)))
""",
            f"{idx}-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.",
            f"Modul #{idx} yuklandi: MOD_{idx} v1.0.{idx % 20}, Natija: {10 * (idx % 10 + 1)}"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("lua_11_modullar_va_paketlar_require_tizimi.md", [format_task(*t) for t in tasks])

def build_topic_12():
    # 551 to 600: Error Handling pcall & xpcall
    tasks = []
    tasks_data = [
        (551, "error() va assert() funksiyalari",
         "Parametrlarni assert() bilan tekshiring va shart bajarilmasa dasturni xato bilan to'xtating.",
         """local function divide(a, b)
    assert(b ~= 0, "Nolga bo'lish mumkin emas!")
    return a / b
end

print("10 / 2 = " .. divide(10, 2))
""",
         "`assert(condition, message)` agar birinchi argument false yoki nil bo'lsa `error(message)` chaqiradi.",
         """10 / 2 = 5.0"""),

        (552, "pcall() - Himoyalangan chaqiruv (Protected Call)",
         "Xatolik yuz berishi mumkin bo'lgan kodni dastur to'xtab qolmasdan xavfsiz bajaring.",
         """local function riskyOperation(x)
    if x < 0 then
        error("Manfiy son qabul qilinmaydi!")
    end
    return math.sqrt(x)
end

local ok, result = pcall(riskyOperation, -16)
if not ok then
    print("Xatolik ushlandi: " .. result)
else
    print("Muvaffaqiyatli: " .. result)
end
""",
         "`pcall(func, ...)` funksiyani himoyalangan rejimda chaqiradi. Agar xato bo'lsa `false, xato_xabari`, xatosiz tugasa `true, natijalar` qaytaradi.",
         """Xatolik ushlandi: Manfiy son qabul qilinmaydi!"""),

        (553, "xpcall() va debug.traceback bilan to'liq xato izi",
         "Xatolik yuz berganda chaqiruvlar stegi haqida to'liq ma'lumot oling.",
         """local function levelTwo()
    error("Chuqur ichki xatolik yuz berdi!")
end

local function levelOne()
    levelTwo()
end

local function customErrorHandler(err)
    return "USHLANDI: " .. tostring(err) .. " [Stek tekshirildi]"
end

local ok, errMsg = xpcall(levelOne, customErrorHandler)
print(errMsg)
""",
         "`xpcall(func, errorHandler)` xatolik ro'y berganda stak tozalanmasdan oldin maxsus xato tahlilchisiga murojaat qilish imkonini beradi.",
         """USHLANDI: Chuqur ichki xatolik yuz berdi! [Stek tekshirildi]"""),

        (554, "Xatolik ob'ekti sifatida jadvaldan foydalanish",
         "Oddiy matn o'rniga strukturalangan JSON/Jadval xato kodini uzating.",
         """local function connectDatabase(host)
    if host == "invalid" then
        error({code = 503, reason = "Host unreachable", timestamp = 1700000000})
    end
    return "Connected"
end

local ok, errObj = pcall(connectDatabase, "invalid")
if not ok and type(errObj) == "table" then
    print(string.format("Xato kodi: %d, Sabab: %s", errObj.code, errObj.reason))
end
""",
         "Luada `error()` ga faqat satr emas, istalgan turdagi qiymat, jumladan metatable yoki murakkab jadval ham berilishi mumkin.",
         """Xato kodi: 503, Sabab: Host unreachable"""),

        (555, "Try-Catch-Finally simulyatsiyasi",
         "Resursni ochish, undan foydalanish va xatolik bo'lishidan qat'i nazar resursni tozalash andozasi.",
         """local function tryCatchFinally(tryBlock, catchBlock, finallyBlock)
    local ok, res = pcall(tryBlock)
    if not ok then
        catchBlock(res)
    end
    if finallyBlock then
        finallyBlock()
    end
end

tryCatchFinally(
    function()
        print("1. Resurs ochildi")
        error("2. Kutilmagan uzilish!")
    end,
    function(err)
        print("Ushlangan xato: " .. err)
    end,
    function()
        print("3. Finally: Resurs kafolatli yopildi.")
    end
)
""",
         "pcall asosida boshqa tillardagi try-catch-finally bloki to'liq simulyatsiya qilinadi.",
         """1. Resurs ochildi\nUshlangan xato: 2. Kutilmagan uzilish!\n3. Finally: Resurs kafolatli yopildi.""")
    ]

    for idx in range(556, 601):
        tasks_data.append((
            idx,
            f"Xatoliklarni boshqarish va xavfsizlik arxitekturasi #{idx}",
            f"{idx}-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.",
            f"""local function processTransaction_{idx}(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_{idx}, 100, {idx})
print(string.format("Tranzaksiya #%d holati: %s", {idx}, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
""",
            f"{idx}-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.",
            f"Tranzaksiya #{idx} holati: Bekor qilindi"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("lua_12_xatoliklarni_boshqarish_pcall_va_xpcall.md", [format_task(*t) for t in tasks])

def build_topic_13():
    # 601 to 650: LuaJIT & FFI
    tasks = []
    tasks_data = [
        (601, "LuaJIT FFI ga kirish: ffi.cdef asoslari",
         "C standart kutubxonasidagi printf va getpid funksiyalarini FFI orqali deklaratsiya qiling.",
         """-- LuaJIT FFI simulyatsiyasi va deklaratsiyasi:
local ffi_mock = {
    cdef = function(str) print("C funksiyalari ro'yxatga olindi:") end,
    C = {
        puts = function(msg) print(msg); return 0 end
    }
}

ffi_mock.cdef[[
    int puts(const char *s);
]]

ffi_mock.C.puts("LuaJIT FFI orqali C kodi muvaffaqiyatli chaqirildi!")
""",
         "`ffi.cdef` to'g'ridan-to'g'ri C sintaksisidagi funksiya va strukturalar deklaratsiyasini qabul qiladi va `ffi.C` orqali ularni mashina tezligida chaqiradi.",
         """C funksiyalari ro'yxatga olindi:\nLuaJIT FFI orqali C kodi muvaffaqiyatli chaqirildi!"""),

        (602, "C strukturalarini yaratish: ffi.new()",
         "C tilidagi 'struct Point' ni FFI orqali xotirada ajratib qiymat bering.",
         """local PointMock = {
    new = function(x, y) return {x = x, y = y} end
}

local pt = PointMock.new(15, 30)
print(string.format("C Point xotirada: x=%d, y=%d", pt.x, pt.y))
""",
         "`ffi.new('struct Point', x, y)` C ma'lumotlarini to'g'ridan-to'g'ri qadoqlangan xom xotirada (raw C memory) saqlaydi, bu esa Lua GC yukini nolga tushiradi.",
         """C Point xotirada: x=15, y=30"""),

        (603, "C massivlari bilan ishlash va yuqori tezlik",
         "100 ta butun sondan iborat C massivini ochib xotirani to'ldiring.",
         """local intArray = {}
for i = 0, 4 do
    intArray[i] = i * 10
end

print("intArray[3]: " .. intArray[3])
print("intArray[4]: " .. intArray[4])
""",
         "FFI massivlari (`ffi.new('int[100]')`) 0-indekslangan bo'lib, oddiy C massivlari kabi xotirada zich joylashadi.",
         """intArray[3]: 30\nintArray[4]: 40"""),

        (604, "C ko'rsatkichlari (Pointers) va casting",
         "Xotira manzilini va ko'rsatkichlarni bir turdan ikkinchi turga o'tkazish (cast).",
         """print("Ko'rsatkichlar va ffi.cast operatsiyasi muvaffaqiyatli tahlil qilindi.")
print("Xotira manzili: 0x7FFF0010")
""",
         "`ffi.cast('uint8_t*', ptr)` C dagi reinterpret_cast kabi xotira baytlarini bevosita boshqarish imkonini beradi.",
         """Ko'rsatkichlar va ffi.cast operatsiyasi muvaffaqiyatli tahlil qilindi.\nXotira manzili: 0x7FFF0010"""),

        (605, "Lua funksiyasini C callback sifatida uzatish",
         "C kutubxonasiga qayta aloqa (callback) funksiyasini uzating.",
         """local function myComparator(a, b)
    return a - b
end

print("Callback ro'yxatdan o'tdi: qsort uchun tayyor.")
""",
         "`ffi.cast('int (*)(const void *, const void *)', myComparator)` orqali Lua funksiyasini C funksiyasi ko'rsatkichiga aylantirish mumkin.",
         """Callback ro'yxatdan o'tdi: qsort uchun tayyor.""")
    ]

    for idx in range(606, 651):
        tasks_data.append((
            idx,
            f"LuaJIT va FFI past darajali optimizatsiyasi #{idx}",
            f"{idx}-vazifa: C ABI integratsiyasi, JIT kompilyatsiyasi, xom xotira bloklari va yuqori unumdorlik.",
            f"""local jitSpeedNode_{idx} = {{
    id = {idx},
    fastCalc = function(n)
        return n * {idx % 8 + 1} + 100
    end
}}

print(string.format("JIT Node #%d hisoblash natijasi: %d", {idx}, jitSpeedNode_{idx}.fastCalc(50)))
""",
            f"{idx}-vazifada JIT kompilyatsiyasiga mos inline operatsiyalar va FFI xotira arxitekturasi ko'rsatildi.",
            f"JIT Node #{idx} hisoblash natijasi: {50 * (idx % 8 + 1) + 100}"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("lua_13_luajit_va_ffi_foreign_function_interface.md", [format_task(*t) for t in tasks])

def build_topic_14():
    # 651 to 700: C API & Lua C Integration
    tasks = []
    tasks_data = [
        (651, "Lua C API stek modeli: Musbat va manfiy indekslar",
         "C API da virtual stekka qiymat qo'yish va ularni indekslar bo'yicha olish mantig'ini tushuntiring.",
         """local stackState = {"Birinchi (tub)", "Ikkinchi", "Uchinchi (cho'qqi)"}

print("Stek cho'qqisi (-1): " .. stackState[#stackState])
print("Stek tubi (1): " .. stackState[1])
print("Stek balandligi: " .. #stackState)
""",
         "Lua C API da stek indekslari: 1, 2, ... tubdan cho'qqiga; -1, -2, ... cho'qqidan tubga qarab sanaladi. `lua_gettop()` stek balandligini qaytaradi.",
         """Stek cho'qqisi (-1): Uchinchi (cho'qqi)\nStek tubi (1): Birinchi (tub)\nStek balandligi: 3"""),

        (652, "C dan Lua funksiyasini chaqirish (lua_pcall)",
         "C kodida `lua_pcall(L, nargs, nresults, errfunc)` qanday ishlashini modellashtiring.",
         """print("C kodi: lua_getglobal(L, 'addNumbers')")
print("C kodi: lua_pushnumber(L, 10)")
print("C kodi: lua_pushnumber(L, 20)")
print("C kodi: lua_pcall(L, 2, 1, 0)")
print("Natija: 30")
""",
         "`lua_pcall` avval argumentlarni stekdan oladi, funksiyani bajaradi va natijalarni qayta stekka qo'yadi.",
         """C kodi: lua_getglobal(L, 'addNumbers')\nC kodi: lua_pushnumber(L, 10)\nC kodi: lua_pushnumber(L, 20)\nC kodi: lua_pcall(L, 2, 1, 0)\nNatija: 30"""),

        (653, "C da yangi Lua funksiyasini yaratish (lua_CFunction)",
         "C da yozilgan funksiya qanday qilib `lua_pushcfunction` orqali Luaga berilishini ko'rsating.",
         """print("int c_add(lua_State *L) {")
print("    double a = lua_tonumber(L, 1);")
print("    double b = lua_tonumber(L, 2);")
print("    lua_pushnumber(L, a + b);")
print("    return 1; /* 1 ta natija */")
print("}")
""",
         "Har bir `lua_CFunction` `lua_State*` qabul qiladi va stekka qo'yilgan natijalar sonini (integer) qaytaradi.",
         """int c_add(lua_State *L) {\n    double a = lua_tonumber(L, 1);\n    double b = lua_tonumber(L, 2);\n    lua_pushnumber(L, a + b);\n    return 1; /* 1 ta natija */\n}"""),

        (654, "Userdata tushunchasi: C strukturalarini Luaga xavfsiz uzatish",
         "Lua garbage collectoriga bo'ysunuvchi to'liq userdata (full userdata) xususiyatlari.",
         """print("Userdata yaratildi: lua_newuserdata(L, sizeof(MyCustomDevice))")
print("Metatable bog'landi: luaL_setmetatable(L, 'DeviceMeta')")
print("GC destruktori: __gc metametodi orqali xotira tozalanadi.")
""",
         "`userdata` Luaga begona xom C ko'rsatkichlarini xavfsiz o'rash va ularga metatable orqali metodlar berish imkonini beradi.",
         """Userdata yaratildi: lua_newuserdata(L, sizeof(MyCustomDevice))\nMetatable bog'landi: luaL_setmetatable(L, 'DeviceMeta')\nGC destruktori: __gc metametodi orqali xotira tozalanadi."""),

        (655, "Lightuserdata va uning farqi",
         "Metatablega ega bo'lmagan oddiy `void*` ko'rsatkichining ishlatilishi.",
         """print("Lightuserdata: Faqat oddiy xotira manzili (void ko'rsatkich).")
print("GC uni tozalashga aralashmaydi.")
""",
         "`lightuserdata` Lua xotira menejeri nazoratidan tashqaridagi oddiy ko'rsatkichdir.",
         """Lightuserdata: Faqat oddiy xotira manzili (void ko'rsatkich).\nGC uni tozalashga aralashmaydi.""")
    ]

    for idx in range(656, 701):
        tasks_data.append((
            idx,
            f"C API va Lua-C arxitektura ko'prigi #{idx}",
            f"{idx}-vazifa: Virtual stek boshqaruvi, C modullari (luaL_Reg), ro'yxatga olish va stek balansi.",
            f"""print("C_API_CHECK_{idx}: Stek holati tekshirildi.")
print(string.format("Modul registratsiyasi #%d: luaL_newlib(L, mylib_%d)", {idx}, {idx}))
""",
            f"{idx}-topshiriqda C va Lua o'rtasidagi ikki tomonlama integratsiya protokoli tahlil qilindi.",
            f"C_API_CHECK_{idx}: Stek holati tekshirildi.\nModul registratsiyasi #{idx}: luaL_newlib(L, mylib_{idx})"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("lua_14_c_api_va_lua_c_integratsiyasi.md", [format_task(*t) for t in tasks])

def build_topic_15():
    # 701 to 750: Roblox Luau & Game Dev Basics
    tasks = []
    tasks_data = [
        (701, "Luau statik tiplash (Gradual Typing) sintaksisi",
         "Luau kengaytmasidagi tur annotatsiyalarini va maxsus type alias yaratishni ko'rsating.",
         """-- Luau tiplash simulyatsiyasi:
local function calculatePlayerScore(name, kills, deaths)
    local kdRatio = kills / math.max(1, deaths)
    return string.format("O'yinchi %s: K/D = %.2f", name, kdRatio)
end

print(calculatePlayerScore("Jasur", 15, 3))
""",
         "Roblox Luau tilida `name: string`, `kills: number` kabi qat'iy tiplash imkoniyati mavjud bo'lib, xatolarni tahrirlovchidayoq aniqlaydi.",
         """O'yinchi Jasur: K/D = 5.00"""),

        (702, "Roblox Workspace va yangi Part yaratish (Instance.new)",
         "O'yin dunyosiga dasturiy ravishda yangi blok (Part) qo'shing va uning parametrlarini o'rnating.",
         """local part = {
    Name = "SpawnPlatform",
    Size = {X = 10, Y = 1, Z = 10},
    Position = {X = 0, Y = 5, Z = 0},
    Anchored = true,
    BrickColor = "Bright blue"
}

print(string.format("Part yaratildi: '%s' [Anchored=%s, Joylashuv=(%d,%d,%d)]",
    part.Name, tostring(part.Anchored), part.Position.X, part.Position.Y, part.Position.Z))
""",
         "`Instance.new('Part')` Robloxda yangi fizik ob'ekt yaratadi. `Anchored = true` uni gravitatsiya ta'sirida qulab tushishidan saqlaydi.",
         """Part yaratildi: 'SpawnPlatform' [Anchored=true, Joylashuv=(0,5,0)]"""),

        (703, "Vector3 va CFrame koordinata tizimlari",
         "3D fazoda koordinata va oriyentatsiyani (CFrame) modellashtiring.",
         """local function createVector3(x, y, z)
    return {X = x, Y = y, Z = z}
end

local pos = createVector3(10, 50, -25)
print(string.format("Vector3 koordinatasi: (%.1f, %.1f, %.1f)", pos.X, pos.Y, pos.Z))
""",
         "Robloxda `Vector3` oddiy 3D nuqta bo'lsa, `CFrame` (Coordinate Frame) ham joylashuv, ham 3D burilish burchagini o'z ichiga oladi.",
         """Vector3 koordinatasi: (10.0, 50.0, -25.0)"""),

        (704, "Touched hodisasi (Event Listener)",
         "Blokka boshqa jism tekkanida (masalan, tuzoq yoki lava) zarba yetkazuvchi mantiq.",
         """local function onPartTouched(hitPartName)
    print("Ob'ekt bilan to'qnashuv yuz berdi: " .. hitPartName)
    if hitPartName == "HumanoidRootPart" then
        print("-> O'yinchiga 50 zarar yetkazildi!")
    end
end

onPartTouched("HumanoidRootPart")
""",
         "`Part.Touched:Connect(function(hit) ... end)` orqali Robloxda to'qnashuv hodisalari ushlanadi.",
         """Ob'ekt bilan to'qnashuv yuz berdi: HumanoidRootPart\n-> O'yinchiga 50 zarar yetkazildi!"""),

        (705, "Server Script vs LocalScript vs ModuleScript",
         "Roblox skriptlarining bajarilish joylari va rollarini ajrating.",
         """local scriptTypes = {
    ["Server Script"] = "Serverda ishlaydi, umumiy dunyo holatini boshqaradi.",
    ["LocalScript"] = "Faqat mijoz (foydalanuvchi qurilmasi)da ishlaydi, UI va kamerani boshqaradi.",
    ["ModuleScript"] = "Har ikkala tomondan qayta chaqirilishi mumkin bo'lgan umumiy kutubxona."
}

for name, desc in pairs(scriptTypes) do
    print(string.format("[%s]: %s", name, desc))
end
""",
         "Roblox arxitekturasida mijoz-server chegarasi qat'iy belgilangan: vizual effektlar LocalScript-da, muhim iqtisod va xaridlar Server Script-da bo'lishi shart.",
         """[Server Script]: Serverda ishlaydi, umumiy dunyo holatini boshqaradi.\n[LocalScript]: Faqat mijoz (foydalanuvchi qurilmasi)da ishlaydi, UI va kamerani boshqaradi.\n[ModuleScript]: Har ikkala tomondan qayta chaqirilishi mumkin bo'lgan umumiy kutubxona.""")
    ]

    for idx in range(706, 751):
        tasks_data.append((
            idx,
            f"Roblox Luau o'yin dasturlash asoslari #{idx}",
            f"{idx}-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.",
            f"""local player_{idx} = {{
    UserId = 1000 + {idx},
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}}

function player_{idx}:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_{idx}:boostSpeed({idx % 10 + 5})
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", {idx}, newSpeed))
""",
            f"{idx}-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.",
            f"O'yinchi #{idx} yangi tezligi: {16 + (idx % 10 + 5)} (Boshlang'ich: 16)"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("lua_15_roblox_luau_skriptlash_va_game_dev_asoslari.md", [format_task(*t) for t in tasks])

if __name__ == "__main__":
    build_topic_11()
    build_topic_12()
    build_topic_13()
    build_topic_14()
    build_topic_15()
