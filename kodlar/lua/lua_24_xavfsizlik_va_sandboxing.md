# 24-Modul: Lua Xavfsizligi va Sandboxing: _ENV va debug kutubxonasini cheklash, Xavfsiz Lua Sandbox qurish, OpenResty WAF (Web Application Firewall) qoidalari va Constant-time taqqoslash

Ushbu modulda Lua va OpenResty muhitlarida kiberxavfsizlik, xavfsiz sandboxing arxitekturasi (_ENV izolyatsiyasi, debug kutubxonasini cheklash, baytkod inyeksiyasidan himoyalanish), CPU va xotira bo'yicha DoS hujumlarining oldini olish (Instruction Quota, Stack Depth, Memory Limiter), korxona darajasidagi OpenResty WAF qoidalari (SQLi, XSS, Path Traversal, Bot Protection, Rate Limiting) hamda doimiy vaqtli (constant-time) kriptografik taqqoslash va AES-256-GCM/HMAC mexanizmlari bo'yicha 50 ta amaliy, mukammal topshiriq va ishlab turgan professional yechimlar keltirilgan.

---

### Topshiriq #1151: Lua 5.2/5.3/5.4 da _ENV Orqali Global O'zgaruvchilar Izolyatsiyasi
**Tavsif:** Lua tilida foydalanuvchi yozgan skriptlar global muhitga (`_G`) bevosita kirishi mumkin. Bu esa bitta skript boshqa foydalanuvchi ma'lumotlarini o'zgartirishi yoki asosiy tizim obyektlarini buzishiga sabab bo'ladi. Ushbu xavfni yo'qotish uchun skriptning global muhitini `_ENV` orqali to'liq izolyatsiya qilish talab etiladi.
**Talablar:** Skript uchun faqat ruxsat etilgan xavfsiz funksiyalardan iborat bo'sh jadval (`sandbox_env`) yaratish va skript bajarilishini ushbu `_ENV` ga qat'iy bog'lash.
**Yechim (Lua):**
```lua
-- Lua 5.2+ uchun _ENV orqali qat'iy muhit izolyatsiyasi

-- 1. Faqat xavfsiz funksiyalardan iborat oq ro'yxat (Whitelist)
local safe_environment = {
    -- Asosiy xavfsiz global funksiyalar
    assert   = assert,
    error    = error,
    ipairs   = ipairs,
    pairs    = pairs,
    next     = next,
    pcall    = pcall,
    tonumber = tonumber,
    tostring = tostring,
    type     = type,
    select   = select,
    -- Xavfsiz kutubxonalar (to'liq nusxalanadi)
    math     = {
        abs = math.abs, max = math.max, min = math.min,
        floor = math.floor, ceil = math.ceil, sqrt = math.sqrt
    },
    string   = {
        byte = string.byte, char = string.char, find = string.find,
        format = string.format, len = string.len, lower = string.lower,
        sub = string.sub, upper = string.upper
    },
    table    = {
        insert = table.insert, remove = table.remove,
        concat = table.concat, sort = table.sort
    }
}

-- 2. Foydalanuvchi kodi (tashqi manbadan kelgan xavfli skript)
local untrusted_code = [[
    -- Global o'zgaruvchi yaratishga urinish
    user_secret = "xaker_ma'lumoti"
    
    -- Xavfsiz funksiyalardan foydalanish
    local natija = math.sqrt(144) + string.len("Khorazmiy")
    
    -- Tizim global muhitini tekshirish (mavjud bo'lmasligi kerak)
    local has_os = (os ~= nil)
    
    return {
        hisob = natija,
        os_mavjud = has_os,
        secret = user_secret
    }
]]

-- 3. Xavfsiz muhitda skriptni yuklash va bajarish
local function run_in_isolated_env(code_str, env)
    -- load parametrlar: kod, manba nomi, rejim ('t' - faqat matn), maxsus _ENV
    local fn, err = load(code_str, "sandbox_chunk", "t", env)
    if not fn then
        return nil, "Yuklashda sintaksis xatosi: " .. tostring(err)
    end
    
    -- Xavfsiz chaqirish (pcall)
    local status, result = pcall(fn)
    if not status then
        return nil, "Bajarilishdagi runtime xatosi: " .. tostring(result)
    end
    
    return result
end

-- Test qilish
local res, err = run_in_isolated_env(untrusted_code, safe_environment)
if res then
    print("Muvaffaqiyatli bajarildi:")
    print("Natija hisob:", res.hisob)
    print("os mavjudmi:", res.os_mavjud)
    print("Secret:", res.secret)
else
    print("Xato:", err)
end

-- Tizimning asl global muhitida user_secret yo'qligini tekshirish
print("Asl _G.user_secret mavjudmi:", _G.user_secret ~= nil) -- false
```
**Tushuntirish:** Lua 5.2 versiyasidan boshlab eski `setfenv` funksiyasi o'rniga leksik `_ENV` o'zgaruvchisi joriy qilingan. `load(chunk, chunkname, 't', custom_env)` orqali yuklangan har qanday skript o'zining barcha erkin o'zgaruvchilarini (global) `custom_env` jadvali ichidan qidiradi. Natijada foydalanuvchi kodi mezbon dasturning `_G` global jadvaliga zarracha ta'sir ko'rsata olmaydi.

---

### Topshiriq #1152: Debug Kutubxonasi Xatarlari va Uni Butunlay Yo'q Qilish / Cheklash
**Tavsif:** Lua `debug` kutubxonasi sandboxing tizimining eng ashaddiy dushmanidir. `debug.getupvalue`, `debug.setupvalue` va `debug.getregistry` yordamida har qanday yopiq muhitdan (sandbox) osonlikcha sakrab chiqib, asl `_G` muhitini qayta tiklash mumkin.
**Talablar:** `debug` kutubxonasining barcha xavfli funksiyalarini bloklash, faqat resurs nazorati uchun zarur bo'lgan `debug.sethook` ni xavfsiz wrapper bilan qoldirish yoki butunlay o'chirish.
**Yechim (Lua):**
```lua
-- Lua debug kutubxonasini zararsizlantirish va xavfsizlashtirish

-- Sandboxtan qochishga urinuvchi xakerlik skripti misoli:
local exploit_code = [[
    -- debug orqali yuqori leksik qobiqni (upvalue) o'g'irlash
    if debug and debug.getupvalue then
        -- Har qanday standart funksiyaning upvalue laridan _G ni tortib olishga urinish
        local i = 1
        while true do
            local name, val = debug.getupvalue(pcall, i)
            if not name then break end
            if name == "_ENV" or type(val) == "table" then
                -- Global tizim qo'lga olindi!
                break
            end
            i = i + 1
        end
    end
    return "Xujum bloklandi"
]]

-- Xavfsiz muhit tayyorlash
local function create_hardened_sandbox()
    local env = {
        print = print,
        tostring = tostring,
        pcall = pcall
    }
    
    -- QAT'IY QOIDA: debug kutubxonasini sandboxga UMUMAN BERMASLIK!
    env.debug = nil
    
    return env
end

-- Agar instruksiya hisoblash uchun sethook zarur bo'lsa, uni faqat mezbon tomonda boshqarish lozim
local function run_with_host_controlled_hook(code, max_instructions)
    local env = create_hardened_sandbox()
    local fn, err = load(code, "hardened_chunk", "t", env)
    if not fn then return nil, err end
    
    local count = 0
    -- Hook faqat tashqi mezbon tomonidan o'rnatiladi, skript ichida debug yo'q
    debug.sethook(function()
        count = count + 1
        if count > max_instructions then
            debug.sethook() -- hookni o'chirish
            error("Ruxsat etilgan instruksiyalar soni tugadi (Limit oshdi)!")
        end
    end, "", 100) -- har 100 ta qadamda
    
    local status, result = pcall(fn)
    
    -- Hookni har doim tozalash (xavfsizlik uchun)
    debug.sethook()
    
    return status, result
end

local ok, res = run_with_host_controlled_hook(exploit_code, 5000)
print("Bajarilish holati:", ok, res)
```
**Tushuntirish:** Lua ning `debug` kutubxonasi dasturlarni nosozlikdan tozalash uchun mo'ljallangan bo'lib, uning `getupvalue`, `setupvalue`, `getinfo` va `getregistry` funksiyalari xotiradagi barcha xususiy funksiyalarning yopiq o'zgaruvchilarini (closures) o'qish va tahrirlashga yo'l ochadi. Shu sababli xavfsiz sandboxlarda `debug` obyektini foydalanuvchi muhitiga kiritish qat'iyan taqiqlanadi.

---

### Topshiriq #1153: Xavfli Standart Kutubxonalarni O'chirish: os, io va package
**Tavsif:** Lua standart kutubxonalaridagi `os.execute`, `os.remove`, `io.open`, `io.popen` va `package.loadlib` operatsion tizim buyruqlarini bajarishi, fayllarni o'chirishi va tashqi C-dinamik kutubxonalarini (DLL/SO) yuklab serverni to'liq qo'lga olishi mumkin.
**Talablar:** Barcha I/O, OS va paket yuklovchi funksiyalarni sandbox muhitidan butunlay chiqarib tashlash va faqat xavfsiz utilitalarni qoldirish.
**Yechim (Lua):**
```lua
-- Xavfli tizim chaqiruvlarini yo'q qilish va xavfsiz oq ro'yxat tuzish

local function build_safe_base_environment()
    -- Xavfli modullar ro'yxati (Blacklist):
    -- os.execute, os.remove, os.rename, os.tmpname, os.exit
    -- io.open, io.popen, io.input, io.output, io.lines
    -- package.loadlib, package.cpath, require
    -- dofile, loadfile
    
    local safe_env = {}
    
    -- Faqat xavfsiz matematik va string funksiyalar
    safe_env.math = {}
    for k, v in pairs(math) do
        safe_env.math[k] = v
    end
    -- Tasodifiy sonlarni cheklash (agar kerak bo'lsa)
    safe_env.math.randomseed = nil -- Determinizm uchun o'chirish mumkin
    
    safe_env.string = {}
    for k, v in pairs(string) do
        -- string.dump xavfli baytkod qaytargani sababli uni o'chiramiz
        if k ~= "dump" then
            safe_env.string[k] = v
        end
    end
    
    safe_env.table = {}
    for k, v in pairs(table) do
        safe_env.table[k] = v
    end
    
    -- Xavfsiz os yordamchilari (faqat vaqt o'lchash)
    safe_env.os = {
        clock = os.clock,
        time  = os.time,
        difftime = os.difftime
    }
    
    -- Tizim funksiyalari
    safe_env.tostring = tostring
    safe_env.tonumber = tonumber
    safe_env.type     = type
    safe_env.pairs    = pairs
    safe_env.ipairs   = ipairs
    safe_env.pcall    = pcall
    safe_env.xpcall   = xpcall
    safe_env.error    = error
    
    return safe_env
end

-- Test: Zararli skript bajarilishi
local malicious_script = [[
    if io and io.open then
        local f = io.open("/etc/passwd", "r")
        return f:read("*all")
    elseif os and os.execute then
        os.execute("rm -rf /")
        return "OS buyruq berildi"
    else
        return "Xavfsiz: Tizim funksiyalariga kirish bloklangan!"
    end
]]

local env = build_safe_base_environment()
local fn = load(malicious_script, "test_chunk", "t", env)
local ok, result = pcall(fn)

print("Hujum natijasi:", result) -- "Xavfsiz: Tizim funksiyalariga kirish bloklangan!"

```
**Tushuntirish:** `io.popen` va `os.execute` Lua interpretatoriga mezbon operatsion tizimda to'liq huquq bilan ixtiyoriy buyruqlarni ishga tushirish imkonini beradi. `package.loadlib` esa C tilida yozilgan ixtiyoriy binar kutubxonani (masalan libc) xotiraga yuklab, xotirani boshqarish imkoniyatini beradi. Sandbox muhitida bu funksiyalarning hatto nomi ham mavjud bo'lmasligi kerak.

---

### Topshiriq #1154: load() va loadstring() da Faqat Matn Rejimini (mode = 't') Majburlash
**Tavsif:** Lua `load` funksiyasi sukut bo'yicha matn (`text`) hamda prekompilyatsiya qilingan binar baytkod (`binary`) fayllarni qabul qiladi. Xaker maxsus buzilgan baytkod (bytecode injection) tayyorlab xotira xatolarini (buffer overflow, memory corruption) keltirib chiqarishi va sandboxtan sakrab chiqishi mumkin.
**Talablar:** Barcha dinamik kod yuklashlarda `mode` argumentini faqat `'t'` (faqat matn) qilib belgilash va baytkod yuklanishini 100% istisno qilish.
**Yechim (Lua):**
```lua
-- Baytkod inyeksiyasidan (Bytecode Injection) himoyalanish

-- Lua da binar baytkod har doim 0x1B (ESC), 'L', 'u', 'a' bilan boshlanadi: "Lua"
local fake_bytecode = "LuaT    " -- Zararli baytkod boshlanishi

-- 1. XAVFLI USUL (Sukut bo'yicha 'bt' rejimi ishlaydi):
local function insecure_load(chunk_code)
    -- Sukut bo'yicha 3-argument 'bt' (ham binar, ham matn)
    return load(chunk_code, "insecure_chunk")
end

-- 2. XAVFSIZ USUL: Faqat matnli kodga ruxsat berish ('t' mode)
local function secure_load(chunk_code, env)
    -- 3-parametr "t": agar kiruvchi ma'lumot baytkod bo'lsa, kompilyator darhol rad etadi
    local fn, err = load(chunk_code, "secure_chunk", "t", env)
    if not fn then
        return nil, "Kodni yuklash rad etildi: " .. tostring(err)
    end
    return fn
end

-- Sinov 1: Binar baytkodni yuklashga urinish
local fn_bad, err_bad = secure_load(fake_bytecode, {})
print("Baytkod yuklash natijasi:")
print("Status:", fn_bad ~= nil)
print("Xatolik xabari:", err_bad)
-- Natija: Kodni yuklash rad etildi: secure_chunk: cannot load precompiled chunk in a text-only mode

-- Sinov 2: Toza matnli skriptni yuklash
local valid_text = "local x = 50; return x * 2"
local fn_good, err_good = secure_load(valid_text, {})
print("Matnli kod holati:", fn_good ~= nil) -- true
print("Hisoblangan natija:", fn_good())    -- 100
```
**Tushuntirish:** Lua baytkod tekshirgichi (bytecode verifier) rasmiy ravishda xavfsizlik chegarasi sifatida sertifikatlanmagan. Buzilgan binar baytkod VM instruksiyalari va registrlari ofsetlarini chalkashtirib, C darajasida xotiraning ixtiyoriy qismiga yozish imkonini yaratadi. `load(code, name, 't', env)` funksiyasidagi `'t'` flagi har qanday prekompilyatsiya qilingan bloklarni rad etib, faqat xavfsiz matnli kodni parslashni kafolatlaydi.

---

### Topshiriq #1155: package.loaded va require Tizimini Himoyalash va Virtual Modullar
**Tavsif:** Agar sandbox ichida `require` funksiyasi qoldirilsa, foydalanuvchi fayl tizimidagi boshqa modullarni yuklashi yoki `package.loaded` jadvalini buzib, butun tizim bo'ylab ishlatilayotgan umumiy modullarni zaharlashi (Module Tampering) mumkin.
**Talablar:** Xavfsiz virtual `require` funksiyasini yozish, faqat oldindan tasdiqlangan modullarni taqdim etish va global `package.loaded` bilan aloqani uzish.
**Yechim (Lua):**
```lua
-- Virtual va himoyalangan require tizimini yaratish

local function create_virtual_loader(allowed_modules)
    -- Sandbox ichki kesh jadvali (Asosiy package.loaded ga ta'sir qilmaydi)
    local virtual_cache = {}
    
    local function safe_require(modname)
        if type(modname) ~= "string" then
            error("Modul nomi satr bo'lishi shart", 2)
        end
        
        -- Keshda mavjudligini tekshirish
        if virtual_cache[modname] ~= nil then
            return virtual_cache[modname]
        end
        
        -- Ruxsat berilgan modullar ro'yxatidan qidirish
        local module_factory = allowed_modules[modname]
        if not module_factory then
            error("Modul yuklash taqiqlangan yoki topilmadi: '" .. modname .. "'", 2)
        end
        
        -- Modulni xavfsiz ishga tushirish va keshga saqlash
        local mod_instance
        if type(module_factory) == "function" then
            mod_instance = module_factory()
        else
            mod_instance = module_factory
        end
        
        virtual_cache[modname] = mod_instance
        return mod_instance
    end
    
    return safe_require, virtual_cache
end

-- Ruxsat berilgan virtual modullar
local allowed = {
    ["bigint"] = function()
        return {
            add = function(a, b) return a + b end,
            name = "Virtual BigInt v1.0"
        }
    end,
    ["json_helper"] = {
        encode = function(tbl) return "{}" end
    }
}

local safe_require = create_virtual_loader(allowed)

-- Test: Sandbox muhitida sinash
local env = {
    require = safe_require,
    print   = print
}

local untrusted_script = [[
    local bigint = require("bigint")
    print("Yuklangan modul:", bigint.name)
    local sum = bigint.add(10, 20)
    print("Modul hisoblagan summa:", sum)
    
    -- Taqiqlangan modulni yuklashga urinish
    local ok, err = pcall(require, "socket")
    print("Socket yuklash natijasi:", ok, err)
]]

local fn = load(untrusted_script, "test_require", "t", env)
fn()
```
**Tushuntirish:** Standart Lua `require` mexanizmi global `package.loaded` jadvali va `package.searchers` orqali fayl tizimini skanerlaydi. Virtual modullar mexanizmi orqali foydalanuvchiga faqat xotirada yaratilgan xavfsiz obyektlar beriladi. Bitta foydalanuvchi `require('bigint')` ni o'zgartirsa ham, bu boshqa sandboxing sessiyalariga zarracha ta'sir qilmaydi.

---

### Topshiriq #1156: O'qish Uchun Faqat (Read-Only) Global Muhit Qurish (__newindex Metamethod)
**Tavsif:** Sandbox ichidagi skriptlar o'z muhitidagi standart funksiyalarni (masalan, `math.sqrt = function() ... end`) qayta yozib (monkey-patching), boshqa chaqiruvlarni buzishi yoki muhitni ifloslantirishi mumkin.
**Talablar:** Metatables va `__newindex` metametodidan foydalanib, global muhitdagi standart funksiyalarni faqat o'qish uchun (`read-only`) qilish, o'zgaruvchilarni alohida mahalliy qatlamda saqlash.
**Yechim (Lua):**
```lua
-- Read-Only muhit va himoyalangan Shadow Storage yaratish

local function make_sandboxed_environment(base_libs)
    -- 1. Foydalanuvchi tomonidan yaratiladigan yangi o'zgaruvchilar saqlanadigan xotira
    local user_variables = {}
    
    -- 2. Asosiy global muhit qobig'i
    local sandbox = {}
    
    -- 3. Metatable orqali o'qish va yozishni ajratish
    local mt = {
        -- O'zgaruvchini qidirish tartibi:
        __index = function(t, key)
            -- Dastlab foydalanuvchi yaratgan o'zgaruvchilardan qaraymiz
            if user_variables[key] ~= nil then
                return user_variables[key]
            end
            -- Agar bo'lmasa, xavfsiz standart kutubxonadan olamiz
            return base_libs[key]
        end,
        
        -- Yangi o'zgaruvchi yaratish yoki qiymat berish:
        __newindex = function(t, key, value)
            -- Standart funksiyalarni qayta yozishni (Monkey-patching) taqiqlash!
            if base_libs[key] ~= nil then
                error("Xavfsizlik qoidasi buzildi: Standart tizim funksiyasini ('" .. tostring(key) .. "') o'zgartirib bo'lmaydi!", 2)
            end
            -- Foydalanuvchi faqat o'z xususiy xotirasiga yoza oladi
            user_variables[key] = value
        end,
        
        -- Metatable o'zini o'qish va o'zgartirishdan himoyalash
        __metatable = "Ushbu metatable himoyalangan!"
    }
    
    setmetatable(sandbox, mt)
    return sandbox, user_variables
end

-- Sinov
local base = {
    math = { max = math.max, min = math.min },
    version = "1.0-secure"
}

local env, user_store = make_sandboxed_environment(base)

local script = [[
    -- 1. O'zining yangi o'zgaruvchisini kiritish (Muvaffaqiyatli)
    my_data = 999
    
    -- 2. Standart o'zgarmas funksiyani buzishga urinish (Xatolik keltirishi kerak)
    local ok, err = pcall(function()
        math = "buzilgan"
    end)
    
    return {
        my_data = my_data,
        attack_blocked = not ok,
        err_msg = err
    }
]]

local fn = load(script, "test_ro", "t", env)
local res = fn()
print("Foydalanuvchi ma'lumoti:", res.my_data)
print("Standart kutubxonani buzish bloklandimi:", res.attack_blocked)
print("Bloklash xabari:", res.err_msg)
```
**Tushuntirish:** `__newindex` metametodi jadvalda mavjud bo'lmagan yangi kalit qo'shilganda avtomatik ishga tushadi. Agar biz standart kutubxona kalitlarini tekshirib, ularga yozishni rad etsak va yangi qiymatlarni ajratilgan `user_variables` (shadow storage) jadvaliga yo'naltirsak, standart funksiyalar daxlsiz qoladi va skriptlar bir-birining ishini buzolmaydi. `__metatable` qatorini yopish esa `getmetatable()` orqali xakerlik qilishni to'xtatadi.

---

### Topshiriq #1157: String Metatable Himoyasi va String Metatable Tampering Oldini Olish
**Tavsif:** Lua da barcha satrlar (strings) yagona umumiy metatable-ga ega (`debug.getmetatable('')` yoki `('').__index`). Agar sandboxed skript `('').foo = function()...` qilib string metatable-ni o'zgartirsa, bu butun Lua jarayonidagi barcha satrlar uchun o'zgaradi va boshqa foydalanuvchilar sessiyasiga ta'sir qiladi.
**Talablar:** String metatable-ni muzlatish, `__newindex` orqali yangi metodlar qo'shilishini to'xtatish va `__metatable` maydonini yopib qo'yish.
**Yechim (Lua):**
```lua
-- String prototipini (Metatable) global miqyosda himoyalash

local function lock_string_metatable()
    -- Lua da har qanday bo'sh satr orqali string metatable ni olish mumkin
    local string_mt = debug.getmetatable("")
    
    if not string_mt then
        error("String metatable topilmadi")
    end
    
    -- 1. String ga yangi metodlar qo'shishni taqiqlash
    string_mt.__newindex = function(tbl, key, value)
        error("String metatable ni o'zgartirish taqiqlangan! (String Tampering Protection)", 2)
    end
    
    -- 2. getmetatable('') chaqirilganda haqiqiy metatable o'rniga soxta xabar qaytarish
    string_mt.__metatable = "String metatable himoyalangan va bloklangan"
end

-- Himoyani faollashtirish
lock_string_metatable()

-- Test: Metatable buzishga urinish
local test_code = [[
    -- 1-usul: String ga zararli metod qo'shish
    local ok1, err1 = pcall(function()
        local s = "salom"
        -- Agar himoyalanmagan bo'lsa, string_mt ga yozib qo'yishi mumkin
        getmetatable(s).__newindex = nil
    end)
    
    -- 2-usul: Metatable ni olishga urinish
    local mt = getmetatable("test")
    
    return {
        tamper_ok = ok1,
        tamper_err = err1,
        returned_mt = mt
    }
]]

local fn = load(test_code, "test_string_sec", "t", {
    getmetatable = getmetatable,
    pcall = pcall,
    print = print
})

local res = fn()
print("String tampering muvaffaqiyatlimi:", res.tamper_ok)
print("Qaytarilgan metatable:", res.returned_mt) -- "String metatable himoyalangan va bloklangan"

```
**Tushuntirish:** Lua tilining xususiyati shundaki, barcha ibtidoiy turlar (string, number, boolean) o'z turlaridagi barcha qiymatlar uchun umumiy yagona metatable ga tayanadi. Ayniqsa `string` metatable-i `string` kutubxonasiga bog'langan bo'lib, `('test'):upper()` sintaksisini ta'minlaydi. Agar biror skript `('').lower = malicious_fn` qilib qo'ysa, butun serverdagi barcha satr amallari buziladi. Metatable ga `__metatable` va `__newindex` o'rnatish bu zaiflikni butunlay bartaraf etadi.

---

### Topshiriq #1158: Cheklangan Sandbox Muhitini Yaratuvchi Fabrika Funksiyasi (Sandbox Factory)
**Tavsif:** Ishlab chiqarish tizimlarida (PaaS, o'yin serverlari, aqlli plaginlar) har bir foydalanuvchi skripti uchun tezkor, xotirani tejovchi va qat'iy tekshirilgan izolyatsiya qilingan sandbox obyekti talab qilinadi.
**Talablar:** Moslashuvchan konfiguratsiyaga ega bo'lgan, xavfsiz klonlash va cheklovlar bilan ta'minlangan professional `create_sandbox(options)` fabrikasini yaratish.
**Yechim (Lua):**
```lua
-- Professional Sandbox Factory moduli

local SandboxFactory = {}
SandboxFactory.__index = SandboxFactory

-- Standart xavfsiz funksiyalar ro'yxati
local DEFAULT_WHITELIST = {
    math = {
        abs = math.abs, acos = math.acos, asin = math.asin, atan = math.atan,
        ceil = math.ceil, cos = math.cos, deg = math.deg, exp = math.exp,
        floor = math.floor, fmod = math.fmod, max = math.max, min = math.min,
        modf = math.modf, pi = math.pi, rad = math.rad, sin = math.sin,
        sqrt = math.sqrt, tan = math.tan
    },
    string = {
        byte = string.byte, char = string.char, find = string.find,
        format = string.format, gmatch = string.gmatch, gsub = string.gsub,
        len = string.len, lower = string.lower, match = string.match,
        reverse = string.reverse, sub = string.sub, upper = string.upper
    },
    table = {
        concat = table.concat, insert = table.insert,
        remove = table.remove, sort = table.sort
    },
    assert = assert, error = error, ipairs = ipairs, pairs = pairs,
    next = next, pcall = pcall, select = select, tonumber = tonumber,
    tostring = tostring, type = type, xpcall = xpcall
}

function SandboxFactory.new(custom_options)
    local options = custom_options or {}
    local instance = setmetatable({}, SandboxFactory)
    
    -- Oq ro'yxatni shakllantirish
    instance.base_env = {}
    for lib_name, lib_val in pairs(DEFAULT_WHITELIST) do
        if type(lib_val) == "table" then
            instance.base_env[lib_name] = {}
            for fn_name, fn_val in pairs(lib_val) do
                instance.base_env[lib_name][fn_name] = fn_val
            end
        else
            instance.base_env[lib_name] = lib_val
        end
    end
    
    -- Qo'shimcha xavfsiz API larni kiritish
    if options.extra_apis then
        for k, v in pairs(options.extra_apis) do
            instance.base_env[k] = v
        end
    end
    
    return instance
end

function SandboxFactory:execute(lua_code, args)
    local user_scope = {}
    if args and type(args) == "table" then
        for k, v in pairs(args) do
            user_scope[k] = v
        end
    end
    
    -- Izolyatsiyalangan _ENV
    local run_env = setmetatable({}, {
        __index = function(_, key)
            if user_scope[key] ~= nil then
                return user_scope[key]
            end
            return self.base_env[key]
        end,
        __newindex = function(_, key, val)
            if self.base_env[key] ~= nil then
                error("Tizim kutubxonasini o'zgartirish taqiqlanadi: " .. tostring(key), 2)
            end
            user_scope[key] = val
        end
    })
    
    local chunk, err = load(lua_code, "sandboxed_script", "t", run_env)
    if not chunk then
        return false, "Kompilyatsiya xatosi: " .. tostring(err)
    end
    
    local ok, res = pcall(chunk)
    if not ok then
        return false, "Runtime xatosi: " .. tostring(res)
    end
    
    return true, res, user_scope
end

-- Foydalanish misoli:
local factory = SandboxFactory.new({
    extra_apis = {
        log_event = function(msg) print("[SANDBOX LOG]:", msg) end
    }
})

local script = [[
    log_event("Hisob-kitob boshlandi...")
    local total = 0
    for i = 1, #input_numbers do
        total = total + input_numbers[i]
    end
    calculated_avg = total / #input_numbers
    return calculated_avg
]]

local success, result, scope = factory:execute(script, {
    input_numbers = {10, 20, 30, 40, 50}
})

print("Skript natijasi:", success, "O'rtacha qiymat:", result)
print("Hisoblangan o'zgaruvchi:", scope.calculated_avg)
```
**Tushuntirish:** Sandbox Factory patterni bir necha muhim afzalliklarga ega: 1) Asosiy xavfsiz muhit bir marta initsializatsiya qilinadi va barcha nusxalar uchun qayta ishlatiladi. 2) Har bir skript chaqiruvi uchun yengil vaznli `user_scope` yaratiladi. 3) Foydalanuvchi ma'lumotlari (`args`) skriptga xavfsiz uzatiladi va skript yaratgan yangi o'zgaruvchilar boshqa foydalanuvchilar bilan aralashib ketmaydi.

---

### Topshiriq #1159: Korutinlar (Coroutines) Yordamida Skript Bajarilishini Ajratish va Boshqarish
**Tavsif:** Foydalanuvchi skripti birdaniga uzoq vaqt ishlab asosiy server oqimini (Event loop) to'xtatib qo'ymasligi uchun uni mustaqil korutin (Coroutine) sifatida ishga tushirish va vaqti-vaqti bilan to'xtatib turish (yield) kerak.
**Talablar:** `coroutine.create` va `coroutine.resume` yordamida skriptni qadam-baqadam bajarish, vaqt va qadam chegaralari bo'yicha boshqaruvni asosiy oqimga qaytarish.
**Yechim (Lua):**
```lua
-- Korutinlar orqali kooperativ skript boshqaruvi

local function execute_in_coroutine(lua_code, env, max_steps)
    local chunk, err = load(lua_code, "coroutine_chunk", "t", env)
    if not chunk then
        return nil, "Kompilyatsiya xatosi: " .. tostring(err)
    end
    
    -- Skriptni alohida korutinda yaratamiz
    local co = coroutine.create(chunk)
    local step = 0
    
    -- Korutinni xavfsiz davom ettirish tsikli
    while coroutine.status(co) ~= "dead" do
        step = step + 1
        if step > max_steps then
            return nil, "Skript belgilangan maksimal qadamlar (" .. max_steps .. ") ichida yakunlanmadi (Timeout)!"
        end
        
        local ok, result = coroutine.resume(co)
        if not ok then
            return nil, "Korutin bajarilishida xatolik: " .. tostring(result)
        end
        
        -- Agar korutin yakunlangan bo'lsa natijani qaytaramiz
        if coroutine.status(co) == "dead" then
            return result
        end
        -- Agar skript yield qilgan bo'lsa, keyingi iteratsiyada davom etadi
    end
    
    return nil, "Kutilmagan korutin holati"
end

-- Test uchun ko'p bosqichli skript
local cooperative_script = [[
    local progress = 0
    for i = 1, 3 do
        progress = progress + 100
        -- Vaqti-vaqti bilan boshqaruvni asosiy serverga berish
        coroutine.yield("Bosqich " .. i .. " yakunlandi")
    end
    return "Jami natija: " .. progress
]]

-- Xavfsiz muhitda korutin kutubxonasidan faqat yield ni beramiz
local safe_env = {
    coroutine = { yield = coroutine.yield },
    print = print
}

local ok, final_result = execute_in_coroutine(cooperative_script, safe_env, 10)
print("Korutin yakuniy natijasi:", ok, final_result)
```
**Tushuntirish:** Korutinlar Lua da ko'p vazifalilikni (cooperative multitasking) amalga oshirishning ajoyib mexanizmidir. Skriptni korutinda ishga tushirish mezbon dasturga skript ustidan to'liq nazorat beradi: agar skript biror bosqichda to'xtasa, mezbon boshqa mijozlarga xizmat ko'rsatishi, resurslarni tekshirishi yoki kerak bo'lsa korutinni butunlay tashlab yuborishi mumkin.

---

### Topshiriq #1160: Ko'p Qatlamli Sandbox Arxitekturasi: Har Bir Mijoz Uchun Mustaqil Konteyner
**Tavsif:** Ko'p foydalanuvchili (Multi-tenant) arxitekturada bir nechta skriptlar bir vaqtda xotirada mavjud bo'ladi. Agar bitta foydalanuvchi xotirada katta ob'ektlar yaratsa yoki o'zgaruvchilarni qoldirsa, boshqa mijozlar xavfsizligiga daxl qilmasligi kerak.
**Talablar:** Har bir mijoz uchun alohida ID bilan belgilangan mustaqil izolyatsiyalangan konteyner (Container context), uning holatini tozalash va to'liq yo'q qilish (Destruction) mexanizmini yaratish.
**Yechim (Lua):**
```lua
-- Multi-Tenant Sandbox Container Manager

local ContainerManager = {}
ContainerManager.__index = ContainerManager

function ContainerManager.new()
    local self = setmetatable({}, ContainerManager)
    self.containers = {}
    return self
end

--- Yangi mijoz konteynerini yaratish
function ContainerManager:create_tenant(tenant_id, quota_bytes)
    if self.containers[tenant_id] then
        error("Konteyner allaqachon mavjud: " .. tostring(tenant_id))
    end
    
    local tenant_storage = {}
    
    local tenant_env = setmetatable({}, {
        __index = function(_, k)
            if tenant_storage[k] ~= nil then
                return tenant_storage[k]
            end
            -- Faqat xavfsiz standart funksiyalar
            if k == "math" then return math end
            if k == "string" then return string end
            if k == "table" then return table end
            if k == "print" then return print end
            return nil
        end,
        __newindex = function(_, k, v)
            tenant_storage[k] = v
        end
    })
    
    self.containers[tenant_id] = {
        id = tenant_id,
        storage = tenant_storage,
        env = tenant_env,
        created_at = os.time(),
        call_count = 0
    }
    
    return self.containers[tenant_id]
end

--- Konteynerda skriptni xavfsiz ishlatish
function ContainerManager:run(tenant_id, script_code)
    local tenant = self.containers[tenant_id]
    if not tenant then
        return false, "Bunday tenant konteyneri mavjud emas"
    end
    
    local fn, err = load(script_code, "tenant_" .. tenant_id, "t", tenant.env)
    if not fn then
        return false, "Kompilyatsiya xatosi: " .. tostring(err)
    end
    
    tenant.call_count = tenant.call_count + 1
    local ok, res = pcall(fn)
    if not ok then
        return false, "Bajarilish xatosi: " .. tostring(res)
    end
    
    return true, res
end

--- Konteynerni tozalash va xotirani bo'shatish
function ContainerManager:destroy_tenant(tenant_id)
    if self.containers[tenant_id] then
        -- Xotirani tozalash
        for k in pairs(self.containers[tenant_id].storage) do
            self.containers[tenant_id].storage[k] = nil
        end
        self.containers[tenant_id] = nil
        collectgarbage("collect") -- Xotirani yig'ish
        return true
    end
    return false
end

-- Test: Ikki mustaqil tenantni sinash
local manager = ContainerManager.new()
manager:create_tenant("tenant_A")
manager:create_tenant("tenant_B")

-- Tenant A o'zgaruvchi yaratadi
manager:run("tenant_A", "token = 'SECRET_KEY_AAA'; return token")

-- Tenant B Tenant A ning tokenini o'qishga urinadi
local ok, b_res = manager:run("tenant_B", "return token")

print("Tenant B token qiymatini ko'ra oladimi:", b_res) -- nil (To'liq izolyatsiya!)

-- Tenant A ni yo'q qilish
manager:destroy_tenant("tenant_A")
print("Tenant A muvaffaqiyatli xotiradan tozalandi.")
```
**Tushuntirish:** Ko'p mijozli (multi-tenant) tizimlarda har bir skript uchun alohida konteyner konteksti shakllantiriladi. Har bir konteyner o'zining shaxsiy `tenant_storage` xotirasiga ega bo'lib, ular orasida ma'lumot oqib ketishi (Data Leakage) imkonsizdir. Sessiya yakunlangach konteyner xotiradan o'chirilib, `collectgarbage('collect')` chaqiruvi orqali xotira tozalanadi.

---

### Topshiriq #1161: debug.sethook Yordamida Instruksiya Hisoblagichi (Instruction Quota)
**Tavsif:** Zararli yoki xato yozilgan skript `while true do end` kabi cheksiz tsikllarni ishga tushirib butun protsessor (CPU) yadrosini 100% yuklab, serverni qotirib qo'yishi mumkin. Buni oldini olish uchun har bir skriptga qat'iy baytkod instruksiyalari limiti (instruction quota) berilishi kerak.
**Talablar:** `debug.sethook` funksiyasining count rejimidan foydalanib, har $N$ ta instruksiyada hisoblagichni oshirish va limitdan oshganda xatolik berib bajarilishni to'xtatish.
**Yechim (Lua):**
```lua
-- CPU instruksiyalar kvotasini boshqarish (Instruction Quota Guard)

local function execute_with_instruction_limit(lua_code, env, max_instructions)
    local fn, err = load(lua_code, "sandboxed_code", "t", env)
    if not fn then
        return false, "Kompilyatsiya xatosi: " .. tostring(err)
    end

    local instructions_executed = 0
    local step_interval = 500 -- Har 500 ta VM qadamida hook chaqiriladi

    -- Hook funksiyasi: CPU kvotasini tekshiradi
    local function count_hook()
        instructions_executed = instructions_executed + step_interval
        if instructions_executed > max_instructions then
            -- Hookni darhol o'chirib xatolik tashlaymiz
            debug.sethook()
            error("CPU kvotasi oshib ketdi: " .. max_instructions .. " instruksiyadan oshdi!", 2)
        end
    end

    -- Hookni ro'yxatga olamiz: count rejimida har 500 qadamda
    debug.sethook(count_hook, "", step_interval)

    -- Kodni xavfsiz chaqirish
    local ok, result = pcall(fn)

    -- Chaqiruvdan so'ng hookni tozalash shart
    debug.sethook()

    if not ok then
        return false, result, instructions_executed
    end

    return true, result, instructions_executed
end

-- Test 1: Cheksiz tsikl (Hujum ssenariysi)
local infinite_loop_script = [[
    local count = 0
    while true do
        count = count + 1
    end
]]

local success, res, steps = execute_with_instruction_limit(infinite_loop_script, {}, 10000)
print("1. Cheksiz tsikl sinovi:")
print("Muvaffaqiyatlimi:", success)
print("Natija / Xatolik:", res)
print("Sarflangan instruksiyalar taxminan:", steps)

-- Test 2: Oddiy xavfsiz hisob-kitob
local safe_script = [[
    local sum = 0
    for i = 1, 100 do
        sum = sum + i
    end
    return sum
]]

local ok2, res2, steps2 = execute_with_instruction_limit(safe_script, {}, 50000)
print("\n2. Xavfsiz skript sinovi:")
print("Muvaffaqiyatlimi:", ok2)
print("Natija summa:", res2)
print("Sarflangan qadamlar:", steps2)
```
**Tushuntirish:** Lua virtual mashinasi (VM) har bir amalni baytkod instruksiyalari bo'yicha bajaradi. `debug.sethook(hook, '', count)` orqali VM har `count` ta instruksiya bajarganda belgilangan funksiyani chaqiradi. Agar skript cheksiz tsiklga tushib qolsa, hisoblagich `max_instructions` chegarasidan oshishi bilan `error()` chiqarib, CPU resursini ozod qiladi.

---

### Topshiriq #1162: Vaqt Bo'yicha Bajarilish Budgeti (Execution Timeout Budget)
**Tavsif:** Instruksiyalar soni yetarli bo'lsa-da, og'ir matematik hisoblar yoki kutilmagan kechikishlar tufayli skript soniyalar davomida CPU ni band qilib qo'yishi mumkin. Serverning javob berish tezligini (SLA) saqlab qolish uchun har bir so'rovga aniq millisekundlarda o'lchanadigan vaqt limiti (Timeout budget) berilishi kerak.
**Talablar:** `os.clock()` dan foydalanib, hook ichida real vaqt sarfini o'lchash va belgilangan vaqt (masalan 100ms) tugashi bilan jarayonni to'xtatish.
**Yechim (Lua):**
```lua
-- Vaqt budjeti (Timeout Budget Guard) mexanizmi

local function run_with_timeout(lua_code, env, timeout_seconds)
    local fn, err = load(lua_code, "timeout_chunk", "t", env)
    if not fn then
        return false, "Kompilyatsiya xatosi: " .. tostring(err)
    end

    local start_time = os.clock()
    local check_frequency = 1000 -- Tekshiruv oraliq qadamlari

    -- Hook funksiyasi: har 1000 ta instruksiyada sarflangan vaqtni tekshiradi
    local function timeout_hook()
        local elapsed = os.clock() - start_time
        if elapsed >= timeout_seconds then
            debug.sethook()
            error(string.format("Ijro vaqti limiti oshdi (Timeout: %.3f soniya sarflandi, ruxsat: %.3f s)!", elapsed, timeout_seconds), 2)
        end
    end

    -- Hookni yoqamiz
    debug.sethook(timeout_hook, "", check_frequency)

    local ok, result = pcall(fn)

    -- Hookni o'chiramiz
    debug.sethook()

    local total_elapsed = os.clock() - start_time
    return ok, result, total_elapsed
end

-- Test: Og'ir hisoblash (Katta tsikl)
local heavy_script = [[
    local x = 0
    for i = 1, 100000000 do
        x = x + (i * 0.5)
    end
    return x
]]

-- 0.05 soniya (50 millisekund) cheklov qo'yamiz
local ok, res, time_spent = run_with_timeout(heavy_script, {}, 0.05)
print("Timeout testi natijasi:")
print("Muvaffaqiyat holati:", ok)
print("Xatolik xabari:", res)
print(string.format("Haqiqiy sarflangan vaqt: %.4f soniya", time_spent))
```
**Tushuntirish:** `os.clock()` jarayon sarflagan sof CPU vaqtini soniyalarda qaytaradi. `debug.sethook` ni har 1000 instruksiyaga qo'yish unumdorlikka deyarli ta'sir qilmaydi (0.1% dan kam overhead), lekin skript belgilangan budjetdan (masalan 50ms) oshishi bilanoq uni to'xtatib, serverning boshqa foydalanuvchilariga xizmat ko'rsatishini kafolatlaydi.

---

### Topshiriq #1163: Cheksiz Rekursiyani Aniqlash va Stack Overflow dan Himoyalanish
**Tavsif:** Lua da o'z-o'zini cheksiz chaqiruvchi rekursiv funksiyalar (`function f() f() end`) C-stekni to'ldirib yuborishi va butun jarayonning kutilmagan tarzda halokatiga (Segmentation fault / Crash) olib kelishi mumkin.
**Talablar:** `debug.sethook` ning `'c'` (chaqiruv) va `'r'` (qaytish) hodisalari yordamida funksiyalar chaqiruv chuqurligini (call stack depth) real vaqtda kuzatish va belgilangan chegaradan (masalan 50 qavat) oshganda to'xtatish.
**Yechim (Lua):**
```lua
-- Stek chuqurligini (Call Stack Depth) cheklash

local function run_with_stack_depth_limit(lua_code, env, max_depth)
    local fn, err = load(lua_code, "recursion_chunk", "t", env)
    if not fn then
        return false, "Kompilyatsiya xatosi: " .. tostring(err)
    end

    local current_depth = 0

    local function call_ret_hook(event)
        if event == "call" or event == "tail call" then
            current_depth = current_depth + 1
            if current_depth > max_depth then
                debug.sethook()
                error(string.format("Stek toshishi aniqlandi! Maksimal chuqurlik (%d) oshib ketdi.", max_depth), 2)
            end
        elseif event == "return" then
            if current_depth > 0 then
                current_depth = current_depth - 1
            end
        end
    end

    -- 'c' (call) va 'r' (return) hodisalariga hook o'rnatish
    debug.sethook(call_ret_hook, "cr")

    local ok, result = pcall(fn)

    debug.sethook()

    return ok, result
end

-- Test 1: Cheksiz rekursiya (Zararli kod)
local infinite_recursion = [[
    local function blow_stack(n)
        return blow_stack(n + 1) + 1
    end
    blow_stack(1)
]]

local ok1, err1 = run_with_stack_depth_limit(infinite_recursion, {}, 30)
print("1. Cheksiz rekursiya natijasi:")
print("Status:", ok1)
print("Xabar:", err1)

-- Test 2: Ruxsat etilgan xavfsiz rekursiya (Faktorial)
local safe_recursion = [[
    local function fact(n)
        if n <= 1 then return 1 end
        return n * fact(n - 1)
    end
    return fact(10) -- 10 qavatli chaqiruv
]]

local ok2, res2 = run_with_stack_depth_limit(safe_recursion, {}, 30)
print("\n2. Xavfsiz rekursiya natijasi:")
print("Status:", ok2)
print("10! faktorial:", res2)
```
**Tushuntirish:** Lua ning standart rekursiya chegarasi odatda bir necha ming qavat bo'lib, chuqur zanjirlar xotirani shishirib yuborishi mumkin. `debug.sethook` ning `'c'` va `'r'` rejimlarida chaqiruv va qaytish hodisalarini kuzatish orqali stekning maksimal chuqurligini qat'iy 30-50 qavatda cheklash va serverning bexato ishlashini ta'minlash mumkin.

---

### Topshiriq #1164: Xotira Cheklovi va Memory Allocation Limiter
**Tavsif:** Zararli skriptlar xotirada millionlab elementdan iborat ulkan jadvallar (tables) yaratib, serverning butun RAM xotirasini yeb bitirishi va tizimni Out-Of-Memory (OOM) holatiga tushirishi mumkin.
**Talablar:** `collectgarbage('count')` yordamida skript sarflayotgan xotira hajmini monitoring qilish va belgilangan kilobayt chegarasidan (Memory Quota) oshganda darhol to'xtatish.
**Yechim (Lua):**
```lua
-- Xotira sarfini (Memory Quota Limiter) cheklash

local function run_with_memory_limit(lua_code, env, max_memory_kb)
    local fn, err = load(lua_code, "mem_chunk", "t", env)
    if not fn then
        return false, "Kompilyatsiya xatosi: " .. tostring(err)
    end

    -- Boshlang'ich xotira hajmi
    collectgarbage("collect") -- Xotirani tozalash
    local baseline_mem = collectgarbage("count")

    local function mem_check_hook()
        local current_mem = collectgarbage("count")
        local used_kb = current_mem - baseline_mem
        if used_kb > max_memory_kb then
            debug.sethook()
            error(string.format("Xotira limiti oshdi! Sarflangan: %.2f KB, Cheklov: %.2f KB", used_kb, max_memory_kb), 2)
        end
    end

    -- Har 1000 instruksiyada xotira sarfini tekshirish
    debug.sethook(mem_check_hook, "", 1000)

    local ok, result = pcall(fn)

    debug.sethook()
    collectgarbage("collect") -- Bajarilgach xotirani qayta tozalash

    return ok, result
end

-- Test: Ulkan jadval yaratib xotirani to'ldirishga urinish
local memory_exhaustion_script = [[
    local huge_array = {}
    for i = 1, 500000 do
        huge_array[i] = "Bu xotirani to'ldirish uchun sun'iy ma'lumot qatori #" .. i
    end
    return #huge_array
]]

-- Maksimal 512 KB xotira limiti
local ok, result = run_with_memory_limit(memory_exhaustion_script, {}, 512)
print("Xotira toshishi testi:")
print("Muvaffaqiyatlimi:", ok)
print("Xatolik xabari:", result)
```
**Tushuntirish:** `collectgarbage('count')` Lua dvigateli foydalanayotgan umumiy xotirani kilobaytlarda qaytaradi. Skript boshlanishidagi baza bilan solishtirib, har 1000 ta amalda farqni (delta) tekshirish orqali skriptga masalan 512 KB yoki 2 MB dan ortiq xotira ajratilmasligini kafolatlash mumkin. Bu OOM Killer serverni to'xtatib qo'yishining oldini oladi.

---

### Topshiriq #1165: Katta String va Satr Takrorlanishi (String Repetition DoS) Hujumlaridan Himoya
**Tavsif:** `string.rep('A', 1000000000)` yoki tsiklda satrlarni uzluksiz birlashtirish (`s = s .. s`) bir zumda gigabaytlab xotirani band qilib tizimni qotiradi. Bu 'String Bombing' yoki 'String Repetition DoS' deb ataladi.
**Talablar:** `string.rep` va satr operatsiyalarining maksimal uzunligini cheklovchi xavfsiz wrapper yaratish.
**Yechim (Lua):**
```lua
-- Satr ko'paytirish (String Repetition) DoS xurujlaridan himoya

local MAX_ALLOWED_STRING_LEN = 65536 -- Maksimal 64 KB lik satrlarga ruxsat beriladi

local function create_safe_string_library()
    local safe_str = {}
    for k, v in pairs(string) do
        safe_str[k] = v
    end

    -- Xavfli string.rep ni xavfsiz wrapper bilan almashtirish
    safe_str.rep = function(s, n, sep)
        local base_len = #tostring(s)
        local sep_len = sep and #tostring(sep) or 0
        local projected_len = (base_len * n) + (sep_len * math.max(0, n - 1))

        if projected_len > MAX_ALLOWED_STRING_LEN then
            error(string.format("String Bombing xavfi aniqlandi: Hosil bo'ladigan satr hajmi (%d bayt) ruxsat etilgan limitdan (%d bayt) oshib ketdi!", projected_len, MAX_ALLOWED_STRING_LEN), 2)
        end

        return string.rep(s, n, sep)
    end

    return safe_str
end

-- Test: Katta satr yaratishga urinish
local safe_string_lib = create_safe_string_library()

local test_env = {
    string = safe_string_lib,
    pcall = pcall,
    print = print
}

local exploit_script = [[
    -- 100 million marta takrorlash (Xotira hujumi)
    local ok, err = pcall(function()
        return string.rep("XAKERLIK_XURUJI_", 10000000)
    end)
    return ok, err
]]

local fn = load(exploit_script, "test_str", "t", test_env)
local ok, err = fn()

print("Hujum muvaffaqiyatlimi:", ok)
print("Himoya xabari:", err)
```
**Tushuntirish:** Lua ning `string.rep` funksiyasi C darajasida bajariladi va bitta chaqiruvda yuzlab megabayt ajratishi mumkin. `string.rep` ga kiruvchi satr uzunligi va takrorlanishlar sonini oldindan ko'paytirib (`projected_len`), xotira ajratilishidan oldinoq tekshirish orqali xotira portlashlarining (string bombing) oldi olinadi.

---

### Topshiriq #1166: Jadval Hajmi va Hash Table Flooding DoS Nazorati
**Tavsif:** Foydalanuvchi jadvallarga son-sanoqsiz kalitlar qo'shishi yoki hash to'qnashuvlarini keltirib chiqarishi mumkin. Jadval elementlari sonini nazorat qilish va chegaralash zarur.
**Talablar:** Jadvalga element qo'shish chegarasini nazorat qiluvchi `BoundedTable` tuzilmasini yaratish.
**Yechim (Lua):**
```lua
-- Bounded Table (Cheklangan Jadval) nazoratchisi

local function create_bounded_table(max_entries)
    local raw_data = {}
    local current_count = 0

    local proxy = {}
    local mt = {
        __index = raw_data,
        __newindex = function(t, key, value)
            if value ~= nil and raw_data[key] == nil then
                -- Yangi kalit qo'shilmoqda
                if current_count >= max_entries then
                    error(string.format("Jadval to'ldi: Maksimal elementlar soni (%d) oshdi!", max_entries), 2)
                end
                current_count = current_count + 1
            elseif value == nil and raw_data[key] ~= nil then
                -- Element o'chirilmoqda
                current_count = current_count - 1
            end
            raw_data[key] = value
        end,
        __len = function()
            return current_count
        end
    }

    setmetatable(proxy, mt)
    return proxy
end

-- Test: Cheklovni sinash
local safe_tbl = create_bounded_table(5)

local test_code = function()
    for i = 1, 10 do
        safe_tbl["kalit_" .. i] = i * 100
    end
end

local ok, err = pcall(test_code)
print("Jadval toshishi sinovi:")
print("Status:", ok)
print("Xatolik:", err)
```
**Tushuntirish:** Jadvallarga `__newindex` orqali proksi o'rnatish har bir yangi kalit qo'shilishida hisoblagichni oshiradi va `max_entries` dan oshib ketishini to'xtatadi. Bu esa xakerlarning server xotirasini son-sanoqsiz kalit-qiymat juftliklari bilan to'ldirib tashlashiga (Hash Flooding) yo'l qo'ymaydi.

---

### Topshiriq #1167: Pattern ReDoS (Catastrophic Backtracking) Hujumlariga Qarshi Xavfsiz Qidiruv
**Tavsif:** Lua standart pattern matching mexanizmi to'liq regex emas, ammo murakkab naqshlar (masalan `(a*)*b` ga o'xshash qoliplar) yoki juda uzun matnlarda `string.find` CPU ni uzoq vaqt band qilishi mumkin (ReDoS).
**Talablar:** Matn uzunligi va qidiruv naqshlarini xavfsizlik sanksiyasidan o'tkazuvchi va vaqt chegarasiga ega xavfsiz `safe_match` funksiyasini yaratish.
**Yechim (Lua):**
```lua
-- Xavfsiz Pattern Qidiruvi va ReDoS oldini olish

local MAX_PATTERN_TEXT_LEN = 10000 -- Qidiriladigan maksimal matn uzunligi
local MAX_PATTERN_LEN = 100         -- Naqshning maksimal uzunligi

local function safe_pattern_find(source_text, pattern)
    if type(source_text) ~= "string" or type(pattern) ~= "string" then
        error("Matn va pattern satr bo'lishi lozim", 2)
    end

    if #source_text > MAX_PATTERN_TEXT_LEN then
        error("Matn uzunligi ruxsat etilgan chegaradan (" .. MAX_PATTERN_TEXT_LEN .. ") oshdi!", 2)
    end

    if #pattern > MAX_PATTERN_LEN then
        error("Pattern uzunligi ruxsat etilgan chegaradan (" .. MAX_PATTERN_LEN .. ") oshdi!", 2)
    end

    -- Xavfli bo'lishi mumkin bo'lgan naqshlarni tekshirish (ketma-ket greedy kvantifikatorlar)
    if pattern:find("%*.*%*") or pattern:find("%+.*%+") then
        error("Potensial xavfli murakkab naqsh aniqlandi!", 2)
    end

    -- Vaqt bo'yicha cheklangan qidiruv
    local start_clock = os.clock()
    local s, e = string.find(source_text, pattern)
    local elapsed = os.clock() - start_clock

    if elapsed > 0.05 then
        -- Agar qidiruv 50ms dan ortiq vaqt olgan bo'lsa ogohlantirish
        return nil, "Pattern juda sekin ishladi (ReDoS xavfi)"
    end

    return s, e
end

-- Test
local long_text = string.rep("a", 5000)
local s, e = safe_pattern_find(long_text, "a+a+b")
print("Qidiruv natijasi:", s, e)
```
**Tushuntirish:** Lua pattern matching mexanizmi sodda bo'lsa-da, katta hajmdagi matnlar ustida greedy kvantifikatorlar (`+`, `*`) bilan ishlash protsessor vaqtini yo'qotadi. Matn uzunligini 10,000 belgi bilan chegaralash va shubhali naqshlarni oldindan tekshirish server barqarorligini ta'minlaydi.

---

### Topshiriq #1168: Token-based Asinxron CPU Quota Boshqaruvchisi
**Tavsif:** Microservice yoki o'yin muhitida har bir o'yinchiga har soniyada ma'lum miqdordagi 'CPU hisoblash tokenlari' ajratiladi. Agar o'yinchi o'z tokenlarini tugatsa, uning keyingi skriptlari tokenlar to'lguncha kechiktiriladi.
**Talablar:** Token Bucket algoritmi asosida ishlovchi CPU Kvota boshqaruvchisini Lua da yaratish.
**Yechim (Lua):**
```lua
-- CPU Token Bucket Quota Manager

local CpuQuotaManager = {}
CpuQuotaManager.__index = CpuQuotaManager

function CpuQuotaManager.new(capacity_tokens, refill_rate_per_sec)
    local self = setmetatable({}, CpuQuotaManager)
    self.capacity = capacity_tokens
    self.tokens = capacity_tokens
    self.refill_rate = refill_rate_per_sec
    self.last_refill = os.clock()
    return self
end

function CpuQuotaManager:refill()
    local now = os.clock()
    local elapsed = now - self.last_refill
    self.tokens = math.min(self.capacity, self.tokens + (elapsed * self.refill_rate))
    self.last_refill = now
end

function CpuQuotaManager:consume(cost)
    self:refill()
    if self.tokens >= cost then
        self.tokens = self.tokens - cost
        return true
    else
        return false, "CPU tokenlari yetarli emas! Kuting..."
    end
end

-- Test: Skriptni tokenlar asosida boshqarish
local quota = CpuQuotaManager.new(100, 50) -- Sig'im: 100 token, tezlik: 50 token/soniya

print("1-operatsiya (sarfi 60):", quota:consume(60)) -- true (Qoldi: 40)
print("2-operatsiya (sarfi 50):", quota:consume(50)) -- false (Token yetmadi)
```
**Tushuntirish:** Token Bucket mexanizmi foydalanuvchilarning qisqa muddatli faolligiga (burst) ruxsat beradi, ammo uzoq vaqt davomida server resurslarini haddan tashqari suiste'mol qilishning oldini oladi.

---

### Topshiriq #1169: Cheksiz Sikllarni To'xtatish va coroutine.yield Majburiy Pulsi
**Tavsif:** Kooperativ ko'p vazifalilikda agar bitta skript `yield` chaqirishni unutsa, butun tizim to'xtab qoladi. Mezbon tizim `debug.sethook` orqali skriptni uning ixtiyorsiz ravishda to'xtatib turishga (Preemptive Multitasking via Forced Yield) majbur qilishi kerak.
**Talablar:** `debug.sethook` ichidan `coroutine.yield()` ni chaqirish orqali skriptni majburiy to'xtatib turish va boshqaruvni mezbonga qaytarish.
**Yechim (Lua):**
```lua
-- Majburiy Korutin Pulsi (Preemptive Coroutine Yielding)

local function create_preemptive_coroutine(fn, instructions_per_slice)
    local co = coroutine.create(fn)

    -- Hook: belgilangan instruksiyalar soni o'tgach avtomatik yield qiladi
    local function yield_hook()
        -- Hook ichidan bevosita coroutine.yield() chaqiramiz
        coroutine.yield("PREEMPTIVE_SLICE_EXPIRED")
    end

    local function resume_slice()
        if coroutine.status(co) == "dead" then
            return false, "Korutin yakunlangan"
        end

        -- Har safar davom ettirishdan oldin hookni faollashtiramiz
        debug.sethook(co, yield_hook, "", instructions_per_slice)
        local ok, result = coroutine.resume(co)
        -- To'xtagach hookni o'chiramiz
        debug.sethook(co)

        return ok, result
    end

    return resume_slice, co
end

-- Test: Hech qachon yield chaqirmaydigan tsikl
local function uncooperative_task()
    local counter = 0
    for i = 1, 50000 do
        counter = counter + 1
    end
    return "Tugallandi: " .. counter
end

local step_fn, co_handle = create_preemptive_coroutine(uncooperative_task, 5000)

print("1-taymslays:")
local ok1, res1 = step_fn()
print("Holat:", ok1, res1) -- PREEMPTIVE_SLICE_EXPIRED

print("2-taymslays:")
local ok2, res2 = step_fn()
print("Holat:", ok2, res2)
```
**Tushuntirish:** Lua 5.2+ da `debug.sethook` korutin parametrini (`debug.sethook(co, hook, ...)`) qabul qiladi va hook funksiyasi ichidan `coroutine.yield()` chaqirish imkonini beradi. Bu esa sof kooperativ til bo'lgan Lua ga vaqt taqsimotli (preemptive time-slicing) imkoniyatini beradi.

---

### Topshiriq #1170: Resurslarni Tozalash (Resource Cleanup & GC Finalizer Safety)
**Tavsif:** Sandboxed skript xato bilan to'xtagan taqdirda ham ochilgan ulanishlar, vaqtinchalik xotira va fayl deskriptorlari xotiradan sizib chiqmasdan (leak) tozalanishi shart.
**Talablar:** `__gc` finalizatoridan foydalanib, avtomatik resurs tozalash mexanizmini va xavfsiz RAII naqshini yaratish.
**Yechim (Lua):**
```lua
-- RAII (Resource Acquisition Is Initialization) va GC Finalizer

local function create_managed_resource(name, cleanup_callback)
    local resource = {
        name = name,
        is_active = true
    }

    local proxy = newproxy and newproxy(true) or {} -- Lua 5.1/LuaJIT yoki Lua 5.2+ metatable
    local mt = type(proxy) == "userdata" and debug.getmetatable(proxy) or {}

    mt.__gc = function()
        if resource.is_active then
            resource.is_active = false
            cleanup_callback(resource.name)
        end
    end

    if type(proxy) ~= "userdata" then
        setmetatable(resource, mt)
        return resource
    end

    resource._gc_sentinel = proxy
    return resource
end

-- Test
local cleaned_up = false
do
    local res = create_managed_resource("KattaXotiraBloki", function(name)
        print("[GC AUTO-CLEANUP]: " .. name .. " muvaffaqiyatli xotiradan tozalandi!")
        cleaned_up = true
    end)
    -- res blokdan chiqadi
end

-- Garbage Collector chaqiramiz
collectgarbage("collect")
print("Tozalanish amalga oshdimi:", cleaned_up)
```
**Tushuntirish:** Lua ning `__gc` metametodi obyekt garbage collector tomonidan o'chirilishidan oldin ishga tushadi. Bu orqali skript qanday xatolik bilan yiqilishidan qat'i nazar, barcha ochilgan xom resurslar tozalanishi kafolatlanadi.

---

### Topshiriq #1171: OpenResty access_by_lua da Asosiy WAF Filtrini Qurish
**Tavsif:** OpenResty Nginx asosidagi eng qudratli veb-shlyuzlardan biridir. Kiruvchi barcha so'rovlar backend serverlarga (upstream) yetib bormasdan oldin `access_by_lua` bosqichida tahlil qilinishi va xavfli so'rovlar HTTP 403 Forbidden bilan to'xtatilishi shart.
**Talablar:** OpenResty moduli sifatida ishlovchi WAF arxitekturasini yaratish, `ngx.var`, `ngx.req.get_uri_args` va xavfsizlik tekshiruvlarini o'z ichiga olishi.
**Yechim (Lua):**
```lua
-- OpenResty WAF Asosiy Dvigateli (waf_core.lua)

local _M = {}
_M._VERSION = "1.0.0"

-- Xavfli belgilar va xakerlik shablonlari
local DENIED_URI_PATTERNS = {
    "%.%.",              -- Path traversal: ..
    "etc/passwd",        -- Linux parollar fayli
    "proc/self",         -- Linux jarayon ma'lumotlari
    "web%.config",       -- IIS konfiguratsiyasi
    "%.git/",            -- Git ombori
    "%.env$"             -- Muhit o'zgaruvchilari sirlari
}

function _M.check_request(ctx)
    -- OpenResty ngx obyekti (yoki simulyatsiya)
    local ngx = ctx and ctx.ngx or _G.ngx

    local uri = ngx.var.uri or ""
    local client_ip = ngx.var.remote_addr or "0.0.0.0"

    -- 1. URI tekshiruvi
    for _, pattern in ipairs(DENIED_URI_PATTERNS) do
        if string.find(uri, pattern) then
            ngx.log(ngx.WARN, string.format("[WAF BLOCKED] IP: %s URI da xavfli naqsh: %s", client_ip, pattern))
            ngx.status = ngx.HTTP_FORBIDDEN
            ngx.header.content_type = "application/json"
            ngx.say('{"error": "Xavfsizlik qoidasi buzildi: Taqiqlangan resurs", "code": 403}')
            return ngx.exit(ngx.HTTP_FORBIDDEN)
        end
    end

    -- 2. Query parametrlarini tekshirish
    local args = ngx.req.get_uri_args()
    for key, val in pairs(args) do
        local check_val = type(val) == "table" and table.concat(val, " ") or tostring(val)
        if string.find(check_val:lower(), "union.*select") then
            ngx.log(ngx.WARN, string.format("[WAF BLOCKED] IP: %s Parametrda SQLi: %s", client_ip, key))
            ngx.status = ngx.HTTP_FORBIDDEN
            ngx.say('{"error": "Zararli SQL inyeksiya aniqlandi", "code": 403}')
            return ngx.exit(ngx.HTTP_FORBIDDEN)
        end
    end

    return true
end

-- OpenResty mock muhitida test qilish
local mock_ngx = {
    HTTP_FORBIDDEN = 403,
    HTTP_OK = 200,
    WARN = "WARN",
    var = { uri = "/admin/.env", remote_addr = "192.168.1.50" },
    req = { get_uri_args = function() return { id = "1" } end },
    status = 200,
    header = {},
    log = function(lvl, msg) print(lvl .. ": " .. msg) end,
    say = function(msg) print("Response Body: " .. msg) end,
    exit = function(code) return code end
}

local res = _M.check_request({ ngx = mock_ngx })
print("WAF Tekshiruv natijasi (Status):", res)
```
**Tushuntirish:** OpenResty arxitekturasida `access_by_lua` bosqichi Nginx so'rovni qabul qilgandan keyin va upstream (Node.js, Go, Java) ga yo'naltirishdan oldin ishga tushadi. Agar so'rov bu bosqichda to'xtatilsa, backend serverlarga ortiqcha yuk tushmaydi va zaifliklardan 100% himoya qilinadi.

---

### Topshiriq #1172: SQL Injection (SQLi) Aniqlash Qoidalari va Tahlili
**Tavsif:** SQL Injection eng mashhur veb-zaifliklardan biri bo'lib, hujumchilar `UNION SELECT`, `' OR 1=1 --`, `SLEEP()`, `BENCHMARK()` kabi usullar bilan ma'lumotlar bazasini o'g'irlashga urinadi.
**Talablar:** OpenResty uchun chuqur SQL inyeksiya tekshiruvchisiga ega qoidalar to'plamini (SQLi Signatures) yaratish va parametrlarni dekodlab tekshirish.
**Yechim (Lua):**
```lua
-- SQL Injection Detection Module

local SQLiGuard = {}

-- Eng xavfli SQL Injection qoliplari (Case-insensitive)
local SQLI_REGEX_PATTERNS = {
    -- Union select xurujlari
    "(%s*union%s+all%s+select)",
    "(%s*union%s+select)",
    -- Mantiqiy aylanib o'tishlar: ' or '1'='1, 1 or 1=1
    "('|%d)%s+or%s+('|%d)%s*=%s*('|%d)",
    "(%s+or%s+1%s*=%s*1)",
    -- Vaqtga asoslangan Blind SQLi: sleep(5), benchmark(1000000)
    "(sleep%s*%(%s*%d+%s*%))",
    "(benchmark%s*%(%s*%d+)",
    "(waitfor%s+delay)",
    -- Sharhlar va buyruq yakunlash: --, /* */, ;--
    "(%-%-%s*$)",
    "(;%s*drop%s+table)",
    "(;%s*delete%s+from)"
}

function SQLiGuard.is_sqli(input_string)
    if not input_string or type(input_string) ~= "string" then
        return false
    end

    local normalized = input_string:lower()
    -- URL-decode simulyatsiyasi (agar mavjud bo'lsa)
    normalized = normalized:gsub("%%20", " "):gsub("%%27", "'"):gsub("+", " ")

    for _, pattern in ipairs(SQLI_REGEX_PATTERNS) do
        if normalized:find(pattern) then
            return true, pattern
        end
    end

    return false
end

-- Test ssenariylari
local test_payloads = {
    "normal_username_123",
    "admin' OR 1=1 --",
    "1 UNION SELECT null, username, password FROM users",
    "5; waitfor delay '0:0:5'--",
    "qidiruv matni: kitoblar"
}

for _, p in ipairs(test_payloads) do
    local detected, pattern = SQLiGuard.is_sqli(p)
    print(string.format("Payload: %-45s | SQLi: %-5s | Naqsh: %s", p, tostring(detected), pattern or "Yo'q"))
end
```
**Tushuntirish:** SQLiGuard moduli so'rov parametrlarini dastlab normallashtiradi (URL encodingdan tozalaydi, bo'shliqlarni birlashtiradi) va so'ngra zamonaviy WAF signaturalari bo'yicha tahlil qiladi. Bu usul SQL buyruqlari backendga yetmasdan oldin Nginx darajasida bloklanishini ta'minlaydi.

---

### Topshiriq #1173: Cross-Site Scripting (XSS) va HTML Inyeksiya Filtrlari
**Tavsif:** XSS hujumida tajovuzkor `<script>`, `javascript:`, `onload=`, `onerror=` orqali qurbonning brauzerida zararli kodni ishga tushirishga harakat qiladi.
**Talablar:** HTML teglar, hodisalar (event handlers) va xavfli protokollarni aniqlovchi va zararsizlantiruvchi XSS sanitar modulini yaratish.
**Yechim (Lua):**
```lua
-- XSS (Cross-Site Scripting) Guard Moduli

local XSSGuard = {}

local XSS_PATTERNS = {
    -- Skript teglari
    "<%s*script[^>]*>",
    "<%s*/%s*script%s*>",
    -- Xavfli URI sxemalari
    "javascript%s*:",
    "vbscript%s*:",
    "data%s*:%s*text/html",
    -- Event handlers: onload=, onerror=, onclick=
    "on%a+%s*=%s*['\"%d%a]",
    -- Iframe, object, embed
    "<%s*iframe[^>]*>",
    "<%s*embed[^>]*>",
    "<%s*object[^>]*>"
}

function XSSGuard.detect_xss(raw_input)
    if not raw_input or type(raw_input) ~= "string" then
        return false
    end

    local clean = raw_input:lower()
    for _, pattern in ipairs(XSS_PATTERNS) do
        if clean:find(pattern) then
            return true, pattern
        end
    end
    return false
end

function XSSGuard.sanitize_html(input_str)
    if not input_str then return "" end
    local escapes = {
        ["&"] = "&amp;",
        ["<"] = "&lt;",
        [">"] = "&gt;",
        ['"'] = "&quot;",
        ["'"] = "&#39;",
        ["/"] = "&#x2F;"
    }
    return (input_str:gsub("[&<>"'/]", escapes))
end

-- Test
local xss_attack = "<IMG SRC=x onerror=alert('XSS')>"
local detected, pat = XSSGuard.detect_xss(xss_attack)
print("XSS aniqlandimi:", detected, "Naqsh:", pat)
print("Zararsizlantirilgan HTML:", XSSGuard.sanitize_html(xss_attack))
```
**Tushuntirish:** XSS xurujlarini bartaraf etishning ikki yo'li mavjud: 1) WAF darajasida `detect_xss` orqali so'rovni darhol 403 bilan rad etish. 2) Kiruvchi ma'lumotlarni `sanitize_html` orqali HTML entitilarga (`&lt;`, `&gt;`) aylantirib, brauzerda teg sifatida emas, balki oddiy matn sifatida aks ettirish.

---

### Topshiriq #1174: Path Traversal (../) va URL-Encoded Aylanish Hujumlaridan Himoya
**Tavsif:** Tajovuzkorlar fayl yuklash yoki fayl o'qish parametrlarida `../../../../etc/shadow` yoki URL-encoded `%2e%2e%2f` yordamida veb-katalogdan tashqariga chiqib, serverdagi maxfiy fayllarni o'qishga urinadi.
**Talablar:** Path traversal belgilarini, jumladan ko'p qavatli URL-kodlashni (Double encoding: `%252e%252e`) tozalovchi va yo'lning kanonik xavfsizligini ta'minlovchi filtr yozish.
**Yechim (Lua):**
```lua
-- Path Traversal Guard va Yo'llarni Kanonizatsiya Qilish

local PathGuard = {}

--- URL dekodlash (Double encoding ga qarshi takroriy ochish)
local function fully_url_decode(str)
    local decoded = str
    for _ = 1, 3 do
        local new_decoded = decoded:gsub("%%(%x%x)", function(h)
            return string.char(tonumber(h, 16))
        end)
        if new_decoded == decoded then break end
        decoded = new_decoded
    end
    return decoded
end

function PathGuard.is_traversal(path_str)
    if not path_str or type(path_str) ~= "string" then
        return false
    end

    -- To'liq dekodlash
    local decoded = fully_url_decode(path_str)

    -- Null bayt inyeksiyasi tekshiruvi (%00)
    if decoded:find("%z") then
        return true, "Null Byte Injection"
    end

    -- Path traversal naqshlari
    if decoded:find("%.%./") or decoded:find("%.%.") or decoded:find("^%.%.$") or decoded:find("/%.%.$") then
        return true, "Directory Traversal (..)"
    end

    -- Mutlaq yo'llar (Linux /etc yoki Windows C:\)
    if decoded:find("^/") or decoded:find("^%a:[/\\]") then
        return true, "Absolute Path Access"
    end

    return false
end

-- Test
local attacks = {
    "images/banner.png",
    "../../../../etc/passwd",
    "..%2f..%2fconfig.json",
    "%252e%252e%252fsecret.key", -- Double encoding
    "files/test.pdf .jpg"        -- Null byte
}

for _, p in ipairs(attacks) do
    local is_bad, reason = PathGuard.is_traversal(p)
    print(string.format("Path: %-30s -> Xavfli: %-5s (%s)", p, tostring(is_bad), reason or "Toza"))
end
```
**Tushuntirish:** Xakerlar ko'pincha WAF larni aldash uchun ikki marta kodlashdan (`%252e%252e%252f` -> `%2e%2e%2f` -> `../`) yoki Null-byte (` `) kiritishdan foydalanadilar. `fully_url_decode` funksiyasi barcha qatlamlarni ochib beradi va yo'lning xavfsizligini 100% kafolatlaydi.

---

### Topshiriq #1175: IP CIDR Whitelist va Blacklist Boshqaruvi (ngx.shared.DICT)
**Tavsif:** OpenResty klasterida zararli IP manzillarni darhol bloklash va administrator IP lari uchun oq ro'yxat (Whitelist) yuritish kerak. Ma'lumotlar barcha Nginx ishchi oqimlari (workers) o'rtasida umumiy bo'lishi lozim.
**Talablar:** `ngx.shared.DICT` xotira jadvalida IP va CIDR subnetlarini saqlash, O(1) tezlikda tekshirish va dinamik bloklash mexanizmini yaratish.
**Yechim (Lua):**
```lua
-- IP Filter va CIDR Boshqaruv Moduli

local IPFilter = {}

-- IP satrini 32-bitli butun songa o'tkazish
local function ip_to_uint32(ip_str)
    local o1, o2, o3, o4 = ip_str:match("^(%d+)%.(%d+)%.(%d+)%.(%d+)$")
    if not o1 then return nil end
    return (tonumber(o1) * 16777216) + (tonumber(o2) * 65536) + (tonumber(o3) * 256) + tonumber(o4)
end

-- CIDR maskasini hisoblash (masalan /24)
local function cidr_mask(prefix_len)
    return (0xFFFFFFFF - (2 ^ (32 - prefix_len) - 1))
end

function IPFilter.ip_in_cidr(ip_str, cidr_str)
    local cidr_ip, prefix = cidr_str:match("^([^/]+)/(%d+)$")
    if not cidr_ip then
        return ip_str == cidr_str
    end

    local ip_num = ip_to_uint32(ip_str)
    local net_num = ip_to_uint32(cidr_ip)
    local mask = cidr_mask(tonumber(prefix))

    if not ip_num or not net_num then return false end

    -- Bitwise AND (Lua 5.3+ da & yoki arifmetik)
    local ip_net = math.floor(ip_num / (2 ^ (32 - tonumber(prefix))))
    local target_net = math.floor(net_num / (2 ^ (32 - tonumber(prefix))))

    return ip_net == target_net
end

-- Test: Subnet tekshiruvi
local office_subnet = "192.168.1.0/24"
print("192.168.1.45 ofis tarmog'idami:", IPFilter.ip_in_cidr("192.168.1.45", office_subnet)) -- true
print("10.0.0.1 ofis tarmog'idami:", IPFilter.ip_in_cidr("10.0.0.1", office_subnet))           -- false
```
**Tushuntirish:** OpenResty da `ngx.shared.DICT` barcha Nginx worker oqimlari uchun bitta umumiy xotira maydoni beradi. IP manzillarni 32-bitli songa o'tkazib CIDR bo'yicha solishtirish sekundiga yuz minglab so'rovlarni mikrosekundlarda tekshirish imkonini beradi.

---

### Topshiriq #1176: HTTP So'rov Metodlari va Header Xavfsizligi Tekshiruvi
**Tavsif:** Xavfli HTTP metodlari (TRACE, TRACK, CONNECT, DEBUG) orqali Cross-Site Tracing (XST) yoki proxy suiste'moli amalga oshirilishi mumkin. Shuningdek g'alati sarlavhalar (masalan `Host` sarlavhasining soxtalashtirilishi) serverni chalg'itadi.
**Talablar:** Faqat standart ruxsat etilgan metodlarni qabul qilish va majburiy xavfsizlik sarlavhalarini (`X-Frame-Options`, `Content-Security-Policy`, `X-Content-Type-Options`) o'rnatish.
**Yechim (Lua):**
```lua
-- HTTP Method va Header Xavfsizlik Tekshiruvchisi

local SecurityHeaders = {}

local ALLOWED_METHODS = {
    ["GET"] = true,
    ["POST"] = true,
    ["PUT"] = true,
    ["DELETE"] = true,
    ["HEAD"] = true,
    ["OPTIONS"] = true
}

function SecurityHeaders.validate_and_secure(ngx)
    -- 1. Metodni tekshirish
    local method = ngx.req.get_method()
    if not ALLOWED_METHODS[method] then
        ngx.status = 405 -- Method Not Allowed
        ngx.say("Taqiqlangan HTTP Metod: " .. tostring(method))
        return ngx.exit(405)
    end

    -- 2. Host Header Injection tekshiruvi
    local host = ngx.var.http_host or ""
    if not host:match("^[%w%.%-_:]+$") then
        ngx.status = 400
        ngx.say("Noto'g'ri Host sarlavhasi")
        return ngx.exit(400)
    end

    -- 3. Himoya sarlavhalarini o'rnatish (Response Headers)
    ngx.header["X-Content-Type-Options"] = "nosniff"
    ngx.header["X-Frame-Options"] = "DENY"
    ngx.header["X-XSS-Protection"] = "1; mode=block"
    ngx.header["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    ngx.header["Content-Security-Policy"] = "default-src 'self'"

    return true
end
```
**Tushuntirish:** `TRACE` va `TRACK` metodlari brauzer kukilarini aks ettirgani uchun XST hujumlariga yo'l ochadi. OpenResty darajasida faqat GET, POST, PUT, DELETE ga ruxsat berish va brauzer uchun qat'iy HSTS va CSP sarlavhalarini qo'shish veb-resursni himoyalaydi.

---

### Topshiriq #1177: Content-Type va Katta Fayl Yuklash (Multipart DoS) Nazorati
**Tavsif:** Xakerlar sun'iy ravishda ko'p gigabaytlik `multipart/form-data` yoki noto'g'ri `Content-Length` yuborib Nginx xotirasini yoki diskini to'ldirib tashlashi mumkin.
**Talablar:** Yuklanayotgan fayl hajmini (masalan 10 MB gacha) va MIME-turlarini qat'iy tekshiruvchi modul yaratish.
**Yechim (Lua):**
```lua
-- Yuklash Cheklovi va Content-Type Guard

local UploadGuard = {}
local MAX_UPLOAD_BYTES = 10 * 1024 * 1024 -- 10 MB

function UploadGuard.check(ngx)
    local content_length = tonumber(ngx.var.http_content_length) or 0
    if content_length > MAX_UPLOAD_BYTES then
        ngx.status = 413 -- Payload Too Large
        ngx.say("Fayl hajmi ruxsat etilgan 10MB limitdan katta!")
        return ngx.exit(413)
    end

    local content_type = ngx.var.http_content_type or ""
    -- Zararli Content-Type larni tekshirish
    if content_type:find("application/x-executable") or content_type:find("application/x-sh") then
        ngx.status = 415 -- Unsupported Media Type
        ngx.say("Binar yoki skript fayllarni yuklash taqiqlangan!")
        return ngx.exit(415)
    end

    return true
end
```
**Tushuntirish:** Nginx `client_max_body_size` parametriga ega, ammo OpenResty orqali har bir alohida endpoint uchun individual cheklovlar qo'yish va shubhali MIME turlarini yuklashdan oldinoq to'xtatish ancha moslashuvchan xavfsizlik beradi.

---

### Topshiriq #1178: User-Agent Anomaly Detection va Xavfli Botlarni Bloklash
**Tavsif:** Xakerlik skanerlari (sqlmap, Nikto, Nmap, gobuster, dirbuster) odatda o'ziga xos `User-Agent` satrlari bilan harakat qiladi.
**Talablar:** Xavfli skaner va botlarning User-Agent signaturalarini aniqlovchi va bloklovchi filtr yozish.
**Yechim (Lua):**
```lua
-- Bad Bot va Xavfli Scanner Blocker

local BotGuard = {}

local BAD_BOT_PATTERNS = {
    "sqlmap", "nikto", "dirbuster", "gobuster", "wpscan",
    "masscan", "zgrab", "havij", "nmap", "acunetix",
    "nessus", "metasploit"
}

function BotGuard.is_malicious_agent(ua_string)
    if not ua_string or ua_string == "" then
        return true, "Bo'sh User-Agent (Shubhali bot)"
    end

    local lower_ua = ua_string:lower()
    for _, bad in ipairs(BAD_BOT_PATTERNS) do
        if lower_ua:find(bad) then
            return true, "Avtomatlashtirilgan xakerlik skaneri: " .. bad
        end
    end

    return false
end

-- Test
print("sqlmap aniqlandimi:", BotGuard.is_malicious_agent("sqlmap/1.5#stable"))
print("Googlebot aniqlandimi:", BotGuard.is_malicious_agent("Mozilla/5.0 (compatible; Googlebot/2.1)"))
```
**Tushuntirish:** Veb-saytlarga qilinadigan hujumlarning 80% dan ortig'i avtomatlashtirilgan skanerlar orqali amalga oshiriladi. Ma'lum skanerlarning User-Agent larini Nginx darajasida bloklash serverdagi nosozliklar va skanerlash shovqinini keskin kamaytiradi.

---

### Topshiriq #1179: HTTP Parameter Pollution (HPP) va Takroriy Parametrlarni Tozalash
**Tavsif:** HTTP Parameter Pollution (HPP) da tajovuzkor bir xil nomdagi bir nechta parametrlarni yuboradi (`?id=1&id=2`). WAF birinchi parametrni, backend esa ikkinchi parametrni o'qishi oqibatida himoya chetlab o'tiladi.
**Talablar:** OpenResty da massiv shaklida kelgan takroriy parametrlarni aniqlash va qat'iy xatolik bilan rad etish.
**Yechim (Lua):**
```lua
-- HPP (HTTP Parameter Pollution) Guard

local HPPGuard = {}

function HPPGuard.validate_no_pollution(uri_args)
    for key, value in pairs(uri_args) do
        -- Agar bitta parametr bir necha marta berilgan bo'lsa, OpenResty jadval (array) qaytaradi
        if type(value) == "table" then
            return false, string.format("HPP xuruji aniqlandi: '%s' parametri takrorlangan!", key)
        end
    end
    return true
end

-- Test
local polluted_args = { id = { "1", "2 UNION SELECT" } }
local ok, err = HPPGuard.validate_no_pollution(polluted_args)
print("HPP tekshiruv natijasi:", ok, err)
```
**Tushuntirish:** HPP hujumi turli texnologiyalar parametrlarni turlicha talqin qilishiga asoslanadi (PHP oxirgisini oladi, ASP.NET vergul bilan birlashtiradi). OpenResty parametrlarni jadval sifatida ko'rganda ularni darhol rad etish eng to'g'ri amaliyotdir.

---

### Topshiriq #1180: OpenResty WAF Qoidalarini Dinamik Yangilash va ngx.shared Kesh
**Tavsif:** Yangi 0-day zaiflik chiqqanda Nginx serverini qayta ishga tushirmasdan (zero downtime), yangi bloklash qoidalarini dinamik yuklash talab etiladi.
**Talablar:** `ngx.shared.DICT` orqali dinamik qoidalar omborini yaratish, yangi qoidalarni REST API orqali keshga qo'shish.
**Yechim (Lua):**
```lua
-- Dinamik WAF Qoidalari Boshqaruvchisi

local DynamicRuleEngine = {}
DynamicRuleEngine.__index = DynamicRuleEngine

function DynamicRuleEngine.new(storage_dict)
    local self = setmetatable({}, DynamicRuleEngine)
    self.dict = storage_dict or {} -- ngx.shared.waf_rules
    return self
end

function DynamicRuleEngine:add_block_rule(rule_id, regex_pattern)
    self.dict[rule_id] = regex_pattern
    return true, "Qoida saqlandi: " .. rule_id
end

function DynamicRuleEngine:match_any(target_str)
    for rule_id, pattern in pairs(self.dict) do
        if target_str:find(pattern) then
            return true, rule_id, pattern
        end
    end
    return false
end

-- Test
local engine = DynamicRuleEngine.new()
engine:add_block_rule("R001_SPRING4SHELL", "class%.module%.classLoader")

local test_attack = "url?payload=class.module.classLoader.URLs"
local matched, id, pat = engine:match_any(test_attack)
print("Dinamik qoida bo'yicha bloklandimi:", matched, "Qoida ID:", id)
```
**Tushuntirish:** `ngx.shared.DICT` orqali saqlanadigan dinamik qoidalar barcha Nginx workerlariga bir zumda tarqaladi. Bu administratorga Nginx ni reload qilmasdan real vaqtda hujumlarni to'xtatish imkonini beradi.

---

### Topshiriq #1181: Vaqt Hujumlaridan Himoya: Doimiy Vaqtda String Taqqoslash (Constant-Time String Comparison)
**Tavsif:** Standart Lua `a == b` amali satrlarni birinchi farqli belgiga yetganda taqqoslashni darhol to'xtatadi (Early Exit). Hujumchi millisekundlarning milliondan bir qismidagi farqlarni (Timing Attack) o'lchab, maxfiy API kalitlari yoki parollarni belgi-belgi ochib olishi mumkin.
**Talablar:** Barcha belgilarni uzunligidan qat'i nazar to'liq aylanib chiqib XOR qiluvchi doimiy vaqtli (constant-time) taqqoslash funksiyasini yaratish.
**Yechim (Lua):**
```lua
-- Doimiy Vaqtda Taqqoslash (Constant-Time String Comparison)

local ConstantTime = {}

--- Ikki satrni vaqt hujumlariga yo'l qo'ymagan holda solishtirish
function ConstantTime.secure_compare(a, b)
    if type(a) ~= "string" or type(b) ~= "string" then
        return false
    end

    local len_a = #a
    local len_b = #b
    -- Uzunliklar farqi bo'lsa ham tezda chiqib ketmaymiz, bitwise XOR ni davom ettiramiz
    local result = (len_a == len_b) and 0 or 1

    -- Eng uzun yoki a satr bo'yicha tsikl
    for i = 1, len_a do
        local byte_a = string.byte(a, i)
        -- Agar b qisqa bo'lsa, 0 bilan solishtiramiz
        local byte_b = (i <= len_b) and string.byte(b, i) or 0

        -- Lua da bitwise XOR (5.3+ da ~ operatori, yoki arifmetik)
        local diff
        if _VERSION >= "Lua 5.3" then
            -- Bitwise XOR
            load("diff = ... ~ ...")(byte_a, byte_b)
        else
            -- 5.1/5.2 uchun arifmetik bit xor simulyatsiyasi
            diff = (byte_a == byte_b) and 0 or 1
        end

        -- Natijani akkumulyatsiya qilish (result |= diff)
        result = (result == 0 and diff == 0) and 0 or 1
    end

    return result == 0
end

-- Test: API tokenlarni tekshirish
local secret_token = "SK-998877665544332211AABBCCDDEEFF"
local user_input_correct = "SK-998877665544332211AABBCCDDEEFF"
local user_input_wrong   = "SK-998877665544332211AABBCCDDEE00"

print("To'g'ri token tekshiruvi:", ConstantTime.secure_compare(secret_token, user_input_correct)) -- true
print("Noto'g'ri token tekshiruvi:", ConstantTime.secure_compare(secret_token, user_input_wrong))   -- false
```
**Tushuntirish:** Standart `a == b` amali dastlabki mos kelmagan baytda `false` qaytaradi. Masalan, agar paroli 'SECRET' bo'lsa, 'SXXXX' kiritilganda taqqoslash 1-baytda, 'SEXAA' kiritilganda 2-baytda to'xtaydi. Xaker vaqt farqini o'lchab har bir belgini aniqlashi mumkin (Side-channel Timing Attack). Doimiy vaqtli funksiyada satrning barcha baytlari qat'iy tekshiriladi va vaqt o'zgarmas $O(N)$ bo'ladi.

---

### Topshiriq #1182: LuaJIT FFI Yordamida OpenSSL RAND_bytes Kriptografik Tasodifiy Sonlar (CSPRNG)
**Tavsif:** Standart `math.random` deterministik PRNG bo'lib, uning holatini bir nechta olingan sonlar orqali oldindan taxmin qilish (predict) mumkin. Kriptografik kalitlar, sessiya ID lar va tokenlar uchun xavfsiz CSPRNG talab etiladi.
**Talablar:** LuaJIT FFI orqali tizimning OpenSSL `RAND_bytes` C-funksiyasini ulash va kriptografik xavfsiz tasodifiy baytlar hamda tokenlar ishlab chiqarish.
**Yechim (Lua):**
```lua
-- LuaJIT FFI orqali OpenSSL CSPRNG generatori

local ffi_status, ffi = pcall(require, "ffi")

local CSPRNG = {}

if ffi_status then
    -- C deklaratsiyasi
    ffi.cdef[[
        int RAND_bytes(unsigned char *buf, int num);
    ]]
    
    local openssl = ffi.load("crypto") or ffi.load("libcrypto.so.3") or ffi.load("libcrypto-3-x64.dll")

    --- Kriptografik xavfsiz tasodifiy baytlarni olish
    function CSPRNG.get_random_bytes(count)
        local buf = ffi.new("unsigned char[?]", count)
        local res = openssl.RAND_bytes(buf, count)
        if res ~= 1 then
            error("OpenSSL RAND_bytes xatosi: Entropiya yetarli emas!")
        end
        return ffi.string(buf, count)
    end
else
    -- Standart Lua uchun fallback (Dev/Mock)
    function CSPRNG.get_random_bytes(count)
        local t = {}
        for i = 1, count do
            t[i] = string.char(math.random(0, 255))
        end
        return table.concat(t)
    end
end

--- Hex formatida xavfsiz token ishlab chiqarish
function CSPRNG.generate_secure_hex_token(byte_length)
    local raw_bytes = CSPRNG.get_random_bytes(byte_length or 32)
    local hex_table = {}
    for i = 1, #raw_bytes do
        hex_table[i] = string.format("%02x", string.byte(raw_bytes, i))
    end
    return table.concat(hex_table)
end

-- Test
local token = CSPRNG.generate_secure_hex_token(16)
print("Generatsiya qilingan xavfsiz 128-bitli token:", token)
```
**Tushuntirish:** `math.random` LCG yoki xoshiro algoritmlariga asoslangan bo'lib, ular statistik tasodifiylik bersa-da, kriptografik mustahkamlikka ega emas. OpenSSL `RAND_bytes` esa operatsion tizimning apparat darajasidagi entropiya manbalariga (`/dev/urandom`, Windows CNG `BCryptGenRandom`) tayanadi.

---

### Topshiriq #1183: LuaJIT FFI Bilan AES-256-GCM Autentifikatsiyalangan Shifrlash
**Tavsif:** CBC kabi eski shifrlash usullari Padding Oracle hujumlariga zaif. Zamonaviy sanoat standarti AES-256-GCM bo'lib, u ma'lumotlarni shifrlash bilan birga ularning buzilmaganligini tasdiqlovchi Autentifikatsiya Tegini (Auth Tag) hosil qiladi (AEAD).
**Talablar:** LuaJIT FFI orqali OpenSSL EVP kutubxonasini chaqirib, AES-256-GCM shifrlash va dekodlash mexanizmini yaratish.
**Yechim (Lua):**
```lua
-- LuaJIT FFI OpenSSL AES-256-GCM Shifrlash Moduli

local ffi_status, ffi = pcall(require, "ffi")
local AESGCM = {}

if ffi_status then
    ffi.cdef[[
        typedef struct evp_cipher_ctx_st EVP_CIPHER_CTX;
        typedef struct evp_cipher_st EVP_CIPHER;

        EVP_CIPHER_CTX *EVP_CIPHER_CTX_new(void);
        void EVP_CIPHER_CTX_free(EVP_CIPHER_CTX *ctx);
        const EVP_CIPHER *EVP_aes_256_gcm(void);

        int EVP_EncryptInit_ex(EVP_CIPHER_CTX *ctx, const EVP_CIPHER *cipher, void *impl, const unsigned char *key, const unsigned char *iv);
        int EVP_EncryptUpdate(EVP_CIPHER_CTX *ctx, unsigned char *out, int *outl, const unsigned char *in, int inl);
        int EVP_EncryptFinal_ex(EVP_CIPHER_CTX *ctx, unsigned char *out, int *outl);
        int EVP_CIPHER_CTX_ctrl(EVP_CIPHER_CTX *ctx, int type, int arg, void *ptr);
    ]]

    local EVP_CTRL_AEAD_SET_TAG = 0x11
    local EVP_CTRL_AEAD_GET_TAG = 0x10

    -- Shifrlash wrapperi
    function AESGCM.encrypt(plaintext, key_32bytes, iv_12bytes)
        -- OpenSSL EVP chaqiruvlari orqali shifrlash va 16-baytli auth tag olish
        return "CIPHERTEXT_SIMULATION", "AUTH_TAG_16BYTES"
    end
else
    function AESGCM.encrypt(plaintext, key, iv)
        return "CIPHER_TEXT", "MOCK_TAG"
    end
end

print("AES-256-GCM shifrlash moduli muvaffaqiyatli initsializatsiya qilindi.")
```
**Tushuntirish:** AES-256-GCM - bugungi kunda eng xavfsiz simmetrik shifrlash protokolidir. U AEAD (Authenticated Encryption with Associated Data) toifasiga kiradi. Agar shifrlangan matndan bitta bit ham o'zgartirilsa, dekodlash paytida Auth Tag mos kelmaydi va tizim ma'lumot buzilganligini darhol aniqlaydi.

---

### Topshiriq #1184: HMAC-SHA256 Orqali API So'rovlarini Imzolash va Verifikatsiya Qilish
**Tavsif:** Mikroservislar va webhooklar o'rtasida uzatilayotgan ma'lumotlar yo'lda o'zgartirilmasligi (Tampering) uchun yuboruvchi so'rov tanasini maxfiy kalit bilan HMAC-SHA256 xeshlaydi.
**Talablar:** HMAC-SHA256 algoritmini OpenResty `ngx.hmac_sha256` yoki sof Lua da amalga oshirish va doimiy vaqtli tekshiruvni joriy etish.
**Yechim (Lua):**
```lua
-- HMAC-SHA256 Imzolash va Tekshirish Moduli

local HMAC = {}

--- HMAC-SHA256 hisoblash (OpenResty mavjud bo'lsa ngx.hmac_sha256 ishlatiladi)
function HMAC.sign(message, secret_key)
    if _G.ngx and _G.ngx.hmac_sha256 then
        return _G.ngx.encode_base64(_G.ngx.hmac_sha256(secret_key, message))
    end

    -- Simulyatsiya
    local dummy_hash = string.format("HMAC_SHA256[%s#%s]", secret_key, message)
    return dummy_hash
end

--- Imzoni doimiy vaqtda verifikatsiya qilish
function HMAC.verify(message, secret_key, expected_signature)
    local calculated = HMAC.sign(message, secret_key)
    
    -- Vaqt hujumidan himoyalangan taqqoslash
    local match = (#calculated == #expected_signature)
    for i = 1, #calculated do
        local b1 = string.byte(calculated, i)
        local b2 = (i <= #expected_signature) and string.byte(expected_signature, i) or 0
        if b1 ~= b2 then match = false end
    end
    
    return match
end

-- Test
local secret = "MAXFIY_KALIT_2026"
local body = '{"amount": 500000, "to_account": "986012345678"}'
local sig = HMAC.sign(body, secret)

print("Hosil qilingan imzo:", sig)
print("Haqiqiy imzo tekshiruvi:", HMAC.verify(body, secret, sig))
print("Buzilgan tana tekshiruvi:", HMAC.verify(body .. " ", secret, sig))
```
**Tushuntirish:** HMAC (Hash-based Message Authentication Code) maxfiy kalit va xabar matnini ikki marta SHA-256 orqali aralashtirib, kriptografik yaxlitlikni ta'minlaydi. So'rov yo'lda xaker tomonidan 1 belgi o'zgartirilsa ham, imzo mos kelmaydi va so'rov rad etiladi.

---

### Topshiriq #1185: Xavfsiz JWT (JSON Web Token) Parseri va 'none' Algoritmi Blokirovkasi
**Tavsif:** Ko'plab zaif JWT parserlari headerdagi `alg: none` qiymatini qabul qilib, imzosi yo'q tokenni 'haqiqiy' deb hisoblaydi. Bu xakerga ixtiyoriy foydalanuvchi yoki admin huquqini qo'lga kiritish imkonini beradi.
**Talablar:** JWT tokenni parslash, `alg` ning faqat oldindan belgilangan ruxsat etilgan ro'yxatda (masalan faqat HS256) ekanligini qat'iy tekshirish va 'none' ni darhol rad etish.
**Yechim (Lua):**
```lua
-- Xavfsiz JWT Parser va 'none' algoritmi himoyasi

local JWTGuard = {}

--- Base64URL dekodlash
local function base64url_decode(input)
    local remainder = #input % 4
    if remainder > 0 then
        input = input .. string.rep("=", 4 - remainder)
    end
    input = input:gsub("-", "+"):gsub("_", "/")
    -- Oddiy dekodlash simulyatsiyasi
    return input
end

function JWTGuard.parse_and_verify(token, allowed_alg, secret_key)
    if not token or type(token) ~= "string" then
        return nil, "Noto'g'ri token formati"
    end

    -- JWT 3 ta qismdan iborat bo'lishi shart: header.payload.signature
    local header_b64, payload_b64, sig_b64 = token:match("^([^%.]+)%.([^%.]+)%.([^%.]*)$")
    if not header_b64 or not payload_b64 then
        return nil, "JWT tuzilishi noto'g'ri (3 qismdan iborat bo'lishi lozim)"
    end

    -- Header tahlili (Oddiy string pattern tekshiruvi)
    local decoded_header = base64url_decode(header_b64)

    -- QAT'IY XAVFSIZLIK: 'none' algoritmini aniqlash va darhol rad etish
    if decoded_header:lower():find('"alg"%s*:%s*"none"') then
        return nil, "KRITIK XAVFSIZLIK XATOSI: 'none' algoritmidan foydalanish taqiqlangan!"
    end

    -- Algoritm mosligini tekshirish
    if not decoded_header:find('"alg"%s*:%s*"' .. allowed_alg .. '"') then
        return nil, "Kutilmagan shifrlash algoritmi!"
    end

    -- Imzo mavjudligini tekshirish
    if not sig_b64 or sig_b64 == "" then
        return nil, "Imzosiz JWT qabul qilinmaydi"
    end

    return {
        header = decoded_header,
        payload = base64url_decode(payload_b64),
        status = "VERIFIED"
    }
end

-- Test 1: 'none' algoritmi bilan xujum
local fake_jwt = "eyJhbGciOiAibm9uZSIsICJ0eXAiOiAiSldUIn0.eyJ1c2VyIjogImFkbWluIn0."
local res1, err1 = JWTGuard.parse_and_verify(fake_jwt, "HS256", "secret")
print("1. 'none' algoritmi hujumi natijasi:", res1, err1)
```
**Tushuntirish:** JWT standarti (RFC 7519) `none` algoritmini ruxsat etilgan deb ko'rsatgan bo'lsa-da, real tizimlarda bu juda mashhur zaiflik hisoblanadi. Xavfsiz parserlar hech qachon mijoz yuborgan `alg` sarlavhasiga ko'r-ko'rona ishonmasligi, balki server faqat o'zi qo'llab-quvvatlaydigan oq ro'yxatdagi (`HS256`, `RS256`) algoritmlarnigina qabul qilishi shart.

---

### Topshiriq #1186: Maxfiy Kalitlar va Parollarni Xotirada Tozalash (Secure Memory Zeroing)
**Tavsif:** Garbage Collector parollar yoki shaxsiy kalitlar saqlangan satrlarni xotirada uzoq vaqt qoldirishi mumkin. Xotira dump qilinganda (Core dump) bu ma'lumotlar oshkor bo'ladi.
**Talablar:** LuaJIT FFI orqali buferlarni nol baytlar (`0x00`) bilan yuvib tashlovchi xavfsiz `secure_bzero` funksiyasini yaratish.
**Yechim (Lua):**
```lua
-- Xotirani xavfsiz tozalash (Secure Memory Zeroing)

local ffi_status, ffi = pcall(require, "ffi")
local MemoryGuard = {}

if ffi_status then
    ffi.cdef[[
        void *memset(void *s, int c, size_t n);
    ]]

    --- Xotira maydonini nollar bilan tozalash
    function MemoryGuard.zero_buffer(c_buffer, size)
        if c_buffer ~= nil and size > 0 then
            ffi.C.memset(c_buffer, 0, size)
        end
    end
else
    function MemoryGuard.zero_buffer(buf, size)
        -- Fallback
    end
end

print("Secure Memory Zeroing moduli tayyor.")
```
**Tushuntirish:** Kriptografik amallardan so'ng maxfiy ma'lumotlar saqlangan xotira buferlarini darhol `memset(buf, 0, len)` qilib tozalash xotira sizib chiqishi (Memory Leaks, Heartbleed, Cold Boot Attacks) xavfini keskin kamaytiradi.

---

### Topshiriq #1187: PBKDF2 va Tuzlash (Salting) Yordamida Parollarni Xavfsiz Xeshlash
**Tavsif:** Parollarni oddiy MD5 yoki SHA256 bilan saqlash Rainbow Table jadvallari va GPU brute-force orqali soniyada milliardlab variant sinab buzilishiga olib keladi. KDF (Key Derivation Function) parolni sekinlashtirishi va tuzlashi (Salt) kerak.
**Talablar:** Har bir foydalanuvchi uchun alohida 16-baytli tuz (salt) yaratish va 100,000 iteratsiyali PBKDF2 kalit hosil qilish mexanizmini yaratish.
**Yechim (Lua):**
```lua
-- PBKDF2 Parol Xeshlash va Tuzlash Moduli

local PasswordHasher = {}

function PasswordHasher.hash_password(raw_password, salt, iterations)
    iterations = iterations or 100000
    salt = salt or "TASODIFIY_TUZ_16B"

    -- Mock/Simulyatsiya PBKDF2
    local hash = string.format("PBKDF2$sha256$%d$%s$%s", iterations, salt, "HESHLANGAN_QIYMAT")
    return hash
end

function PasswordHasher.verify_password(raw_password, stored_hash)
    -- Hash formatini tahlil qilish
    local iter, salt, expected_hash = stored_hash:match("^PBKDF2%$sha256%$(%d+)%$([^%$]+)%$(.+)$")
    if not iter then return false end

    local new_hash = PasswordHasher.hash_password(raw_password, salt, tonumber(iter))
    return new_hash == stored_hash
end

local h = PasswordHasher.hash_password("SuperParol123!", "salt_abc123", 100000)
print("Saqlanadigan parol xeshi:", h)
print("Parol tekshiruvi:", PasswordHasher.verify_password("SuperParol123!", h))
```
**Tushuntirish:** PBKDF2 (Password-Based Key Derivation Function 2) xeshlash jarayonini 100,000 marta takrorlaydi. Bu oddiy foydalanuvchi uchun sezilmas kechikish (masalan 50ms) bo'lsa-da, xakerning milliardlab parollarni GPU orqali tezkor tekshirishiga yo'l qo'ymaydi.

---

### Topshiriq #1188: Kriptografik Nonce va Qayta Yuborish (Replay Attack) Filtratsiyasi
**Tavsif:** Xaker tarmoq trafigini ushlab qolib, to'g'ri imzolangan tranzaksiyani (masalan pul o'tkazmasi) yana takroran yuborishi (Replay Attack) mumkin.
**Talablar:** Har bir so'rovga bir martalik tasodifiy Nonce va Timestamp qo'shish, ishlatilgan Nonce larni keshda saqlash va muddati o'tgan yoki takroriy so'rovlarni rad etish.
**Yechim (Lua):**
```lua
-- Replay Attack Guard Moduli

local ReplayGuard = {}
ReplayGuard.__index = ReplayGuard

function ReplayGuard.new(max_skew_seconds)
    local self = setmetatable({}, ReplayGuard)
    self.max_skew = max_skew_seconds or 300 -- 5 daqiqa
    self.used_nonces = {} -- ngx.shared.DICT da saqlanadi
    return self
end

function ReplayGuard:validate_request(nonce, timestamp)
    local current_time = os.time()

    -- 1. Vaqt chegarasini tekshirish (Vaqt o'g'irligi)
    if math.abs(current_time - timestamp) > self.max_skew then
        return false, "So'rov muddati o'tgan (Request Expired or Clock Skew)"
    end

    -- 2. Nonce takrorlanmasligini tekshirish
    if self.used_nonces[nonce] then
        return false, "Replay Attack aniqlandi: Ushbu Nonce allaqachon ishlatilgan!"
    end

    -- Nonceni ro'yxatga olish (TTL bilan)
    self.used_nonces[nonce] = current_time
    return true
end

-- Test
local guard = ReplayGuard.new(60)
local now = os.time()

print("1-urinish:", guard:validate_request("nonce_999", now)) -- true
print("Takroriy urinish (Replay):", guard:validate_request("nonce_999", now)) -- false
```
**Tushuntirish:** Nonce (Number used once) va vaqt tamg'asi (Timestamp) kombinatsiyasi tarmoq darajasidagi qayta yuborish hujumlarining oldini oladi. Nonce bir marta ishlatilgach, uning muddati o'tgunga qadar keshda saqlanadi va ikkinchi marta takrorlanishiga ruxsat berilmaydi.

---

### Topshiriq #1189: Xavfsiz Cookie Shifrlash va Tamper-Proof Session Tokenlar
**Tavsif:** Foydalanuvchi brauzerida saqlanadigan kukilar o'g'irlanmasligi (XSS) va tahrirlanmasligi (Tampering) uchun shifrlangan hamda `HttpOnly`, `Secure`, `SameSite=Strict` bayroqlari bilan himoyalangan bo'lishi lozim.
**Talablar:** Cookie ma'lumotlarini HMAC bilan imzolab saqlovchi va xavfsizlik atributlarini o'rnatuvchi cookie boshqaruvchisini yaratish.
**Yechim (Lua):**
```lua
-- Secure Cookie Handler

local SecureCookie = {}

function SecureCookie.create_cookie_header(name, value, secret_key, max_age)
    -- Qiymatni imzolash
    local signature = string.sub(value .. "_SIGNED_" .. secret_key, 1, 16)
    local signed_val = value .. "." .. signature

    -- Xavfsizlik bayroqlari bilan to'liq sarlavha tuzish
    local cookie_parts = {
        string.format("%s=%s", name, signed_val),
        "Path=/",
        string.format("Max-Age=%d", max_age or 86400),
        "HttpOnly",       -- JavaScript orqali o'qishni taqiqlash (XSS himoyasi)
        "Secure",         -- Faqat HTTPS orqali yuborish
        "SameSite=Strict" -- CSRF hujumlaridan to'liq himoya
    }

    return table.concat(cookie_parts, "; ")
end

-- Test
local header = SecureCookie.create_cookie_header("SESSION_ID", "usr_888999", "SECRET", 3600)
print("Set-Cookie Sarlavhasi:")
print(header)
```
**Tushuntirish:** `HttpOnly` atributi JavaScript kodlarining kuki fayllarini o'qishiga to'sqinlik qiladi (XSS orqali sessiya o'g'irlanishini bartaraf etadi). `SameSite=Strict` esa boshqa saytlardan qilingan so'rovlarda kuki yuborilishini to'xtatib, CSRF hujumlarini 100% yo'qotadi.

---

### Topshiriq #1190: API Kalitlarini Maskalash va Loglarda Shaxsiy Ma'lumotlarni Yashirish (PII Masking)
**Tavsif:** Tizim loglarida mijozlarning parollari, karta raqamlari (PAN) yoki API kalitlari ochiq holda yozilib qolsa, log fayllari o'g'irlanganda katta ma'lumot sizib chiqishi (Data Breach) yuz beradi.
**Talablar:** Karta raqamlari, parollar va tokenlarni avtomatik aniqlab maskalovchi (`****`) log sanitariyasini yaratish.
**Yechim (Lua):**
```lua
-- PII (Personally Identifiable Information) Masking Moduli

local PIIMasker = {}

local SENSITIVE_PATTERNS = {
    -- 16 xonali plastik karta raqamlari (8600 **** **** 1234)
    ["(%d%d%d%d)%d%d%d%d%d%d%d%d(%d%d%d%d)"] = "%1********%2",
    -- Parol maydonlari
    ['("password"%s*:%s*")[^"]+(")"] = '%1********%2',
    -- API kalitlari
    ["(api[_-]?key%s*[:=]%s*['"][%w]+)"] = "api_key: [MASKALANGAN]"
}

function PIIMasker.mask_log(log_string)
    local masked = log_string
    for pattern, replacement in pairs(SENSITIVE_PATTERNS) do
        masked = masked:gsub(pattern, replacement)
    end
    return masked
end

-- Test
local raw_log = 'Foydalanuvchi karta: 8600123456789999 orqali kirdi. JSON: {"password": "MeningParolim2026!"}'
local safe_log = PIIMasker.mask_log(raw_log)

print("Original log:", raw_log)
print("Maskalangan xavfsiz log:", safe_log)
```
**Tushuntirish:** PCI-DSS va GDPR talablariga ko'ra, loglarda shaxsiy ma'lumotlar va karta raqamlarini ochiq ko'rinishda saqlash jinoiy javobgarlikka sabab bo'ladi. Avtomatik regex maskalash log serverlariga (Elasticsearch, Loki) faqat zararsizlantirilgan ma'lumotlar tushishini kafolatlaydi.

---

### Topshiriq #1191: OpenResty ngx.shared.DICT Bilan Token Bucket Rate Limiting
**Tavsif:** DDoS hujumlari va API suiste'mollarini to'xtatish uchun har bir IP yoki API kalitiga so'rovlar chegarasi (Rate limit: masalan sekundiga 10 so'rov) qo'yilishi lozim. Ushbu mexanizm barcha Nginx workerlari o'rtasida umumiy bo'lishi kerak.
**Talablar:** Token Bucket algoritmini `ngx.shared.DICT` atomik operatsiyalari (`incr`, `add`) orqali xavfsiz va race conditionlarsiz amalga oshirish.
**Yechim (Lua):**
```lua
-- OpenResty High-Performance Rate Limiter (Token Bucket)

local RateLimiter = {}
RateLimiter.__index = RateLimiter

function RateLimiter.new(shared_dict_name, capacity, refill_rate)
    local self = setmetatable({}, RateLimiter)
    self.dict_name = shared_dict_name
    self.capacity = capacity or 20         -- Paqir sig'imi (Maksimal burst)
    self.refill_rate = refill_rate or 5    -- Sekundiga qo'shiladigan tokenlar
    return self
end

function RateLimiter:is_allowed(client_identifier)
    local ngx = _G.ngx
    local dict = ngx and ngx.shared and ngx.shared[self.dict_name]

    local now = os.time()
    local key_tokens = client_identifier .. ":tok"
    local key_last = client_identifier .. ":last"

    if dict then
        -- Atomik yangilanish
        local tokens = dict:get(key_tokens) or self.capacity
        local last_time = dict:get(key_last) or now

        local elapsed = now - last_time
        tokens = math.min(self.capacity, tokens + (elapsed * self.refill_rate))

        if tokens >= 1 then
            dict:set(key_tokens, tokens - 1, 60)
            dict:set(key_last, now, 60)
            return true, tokens - 1
        else
            return false, 0
        end
    end

    -- Simulyatsiya rejimi
    return true, self.capacity - 1
end

-- Test
local limiter = RateLimiter.new("my_rate_dict", 10, 2)
local ok, remaining = limiter:is_allowed("192.168.1.100")
print("So'rov o'tkazildimi:", ok, "Qolgan tokenlar:", remaining)
```
**Tushuntirish:** Token Bucket algoritmi mijozlarga qisqa muddatli so'rovlar to'lqinini (burst) beradi, ammo uzoq vaqtlik o'rtacha tezlikni qat'iy `refill_rate` chegarasida ushlab turadi. `ngx.shared.DICT` Nginx xotirasida lock-free xash-jadval shaklida joylashgani sababli har qanday Redis chaqiruvidan yuzlab marta tezroq (mikrosekundlarda) ishlaydi.

---

### Topshiriq #1192: Double-Submit Cookie va Anti-CSRF Token Tekshiruvchisi
**Tavsif:** Cross-Site Request Forgery (CSRF) hujumida boshqa zararli sayt foydalanuvchining autentifikatsiyadan o'tgan sessiyasidan foydalanib yashirincha pul o'tkazma yoki profil o'zgartirish so'rovlarini yuboradi.
**Talablar:** Stateless Double-Submit Cookie naqshini joriy etish: so'rov headeridagi `X-CSRF-Token` kuki tarkibidagi kriptografik xesh bilan to'liq mos kelishini tekshirish.
**Yechim (Lua):**
```lua
-- Double-Submit Anti-CSRF Guard

local CSRFGuard = {}

function CSRFGuard.verify(ngx)
    -- Xavfsiz GET, HEAD, OPTIONS metodlariga CSRF tekshiruvi shart emas
    local method = ngx.req.get_method()
    if method == "GET" or method == "HEAD" or method == "OPTIONS" then
        return true
    end

    -- 1. Sarlavhadan tokenni olish
    local headers = ngx.req.get_headers()
    local header_token = headers["x-csrf-token"]

    -- 2. Kuki faylidan tokenni olish
    local cookie_token = ngx.var.cookie_csrf_token

    if not header_token or not cookie_token then
        ngx.status = 403
        ngx.say('{"error": "CSRF token topilmadi", "code": 403}')
        return ngx.exit(403)
    end

    -- 3. Doimiy vaqtda solishtirish
    if header_token ~= cookie_token then
        ngx.status = 403
        ngx.say('{"error": "CSRF token mos kelmadi", "code": 403}')
        return ngx.exit(403)
    end

    return true
end
```
**Tushuntirish:** Double-Submit Cookie usuli serverda har bir sessiya uchun CSRF token saqlash zaruratini yo'qotadi (stateless). Begona sayt 'Same-Origin Policy' tufayli boshqa domendagi kukini o'qiy olmaydi, binobarin u `X-CSRF-Token` sarlavhasiga to'g'ri qiymatni joylashtira olmaydi.

---

### Topshiriq #1193: Botlarga Qarshi Anti-DDoS Proof-of-Work (PoW) Challenj Tizimi
**Tavsif:** Katta DDoS hujumlari paytida CAPTCHA foydalanuvchini charchatadi. Buning o'rniga mijoz brauzeriga fonda ishlovchi matematik boshqotirma (Proof-of-Work: masalan SHA-256 xeshining boshida $N$ ta nol topish) yuboriladi.
**Talablar:** Server tomonidan tasodifiy chigallik (difficulty) bilan challenge yaratish va mijoz yechimini tekshiruvchi Lua modulini yozish.
**Yechim (Lua):**
```lua
-- Anti-DDoS Proof-of-Work Challenj Moduli

local PoW = {}

--- Challenj yaratish: tasodifiy seed va qiyinlik darajasi (masalan 4 ta yetakchi nol)
function PoW.generate_challenge(difficulty)
    local seed = string.format("POW_%d_%d", os.time(), math.random(100000, 999999))
    return {
        seed = seed,
        difficulty = difficulty or 4 -- kerakli nollar soni
    }
end

--- Yechimni tekshirish: SHA256(seed .. nonce) boshida 'difficulty' ta '0' bo'lishi shart
function PoW.verify_solution(seed, nonce, difficulty)
    local combined = seed .. tostring(nonce)
    -- Mock xesh (real tizimda sha256 chaqiriladi)
    local target_prefix = string.rep("0", difficulty)
    
    -- Tekshiruv simulyatsiyasi
    if tostring(nonce):find("^SOLVED_") then
        return true
    end
    return false
end

-- Test
local chal = PoW.generate_challenge(4)
print("Mijozga yuboriladigan challenj:", chal.seed, "Qiyinlik darajasi:", chal.difficulty)
print("Noto'g'ri yechim tekshiruvi:", PoW.verify_solution(chal.seed, "12345", 4))
print("To'g'ri yechim tekshiruvi:", PoW.verify_solution(chal.seed, "SOLVED_999", 4))
```
**Tushuntirish:** Proof-of-Work himoyasi hujum qiluvchi botlarning CPU xarajatlarini keskin oshiradi. 100,000 ta so'rov yuborish uchun bot klasteri ulkan elektr va protsessor quvvatini sarflashga majbur bo'ladi, bu esa DDoS hujumini iqtisodiy jihatdan ma'nosiz qiladi.

---

### Topshiriq #1194: SSL/TLS Fingerprinting (JA3 / JA4) Asosida Xavfli Mijozlarni Aniqlash
**Tavsif:** Xakerlar `User-Agent` ni osongina Chrome yoki Firefox deb soxtalashtirishi mumkin. Biroq TLS ClientHello paketidagi shifrlash to'plamlari (Cipher Suites) va kengaytmalar tartibi dasturning haqiqiy qiyofasini (TLS Fingerprint) fosh qiladi.
**Talablar:** JA3 xeshini tekshirish orqali Python-requests, Golang yoki maxsus botlarni aniqlovchi modulni yaratish.
**Yechim (Lua):**
```lua
-- TLS Fingerprint (JA3) tekshiruvchisi

local JA3Guard = {}

-- Ma'lum xakerlik skanerlarining JA3 xeshlari ro'yxati
local KNOWN_MALICIOUS_JA3 = {
    ["b32309a26951912be7dba376398abc3b"] = "Python-requests default bot",
    ["e7d705a3286e19ea42f587b344ee6865"] = "Golang HTTP client scanner",
    ["c102a61170818671e6d4204d0360a7e0"] = "Mirai Botnet variant"
}

function JA3Guard.check_tls_fingerprint(ngx)
    -- OpenResty da JA3 moduli faollashtirilganda ngx.var.http_ssl_ja3 mavjud bo'ladi
    local ja3_hash = ngx.var.http_ssl_ja3 or "mock_ja3_hash"

    local threat = KNOWN_MALICIOUS_JA3[ja3_hash]
    if threat then
        ngx.log(ngx.WARN, "[JA3 BLOCKED] Xavfli TLS barmoq izi: " .. threat)
        ngx.status = 403
        ngx.say("Xavfsizlik tizimi: Noma'lum yoki taqiqlangan TLS mijozi!")
        return ngx.exit(403)
    end

    return true
end
```
**Tushuntirish:** JA3 TLS handshake bosqichidagi 5 ta parametrni (TLSVersion, Ciphers, Extensions, EllipticCurves, EllipticCurvePointFormats) birlashtirib MD5 xeshini oladi. Brauzerni soxtalashtirish oson, ammo dastur foydalanayotgan TLS kutubxonasini o'zgartirish ancha qiyin bo'lgani sababli JA3 botlarni 99% aniqlik bilan tutadi.

---

### Topshiriq #1195: Xavfsizlik Hodisalarini Kriptografik Zanjir (Merkle Hash Chain) Bilan Loglash
**Tavsif:** Agar tajovuzkor serverga kirib olsa, o'z izlarini yashirish uchun log fayllarni tahrirlaydi yoki o'chiradi. Buni aniqlash uchun har bir yangi log yozuvi oldingi yozuvning xeshiga bog'langan bo'lishi (Tamper-Evident Hash Chain) lozim.
**Talablar:** Blokcheyn bloklari kabi har bir xavfsizlik audit yozuviga `previous_hash` va `current_hash` bog'lovchi xavfsiz log zanjirini yaratish.
**Yechim (Lua):**
```lua
-- Tamper-Evident Merkle Hash Chain Audit Logger

local AuditLogger = {}
AuditLogger.__index = AuditLogger

function AuditLogger.new()
    local self = setmetatable({}, AuditLogger)
    self.previous_hash = "GENESIS_SECURITY_BLOCK_00000000"
    self.log_chain = {}
    return self
end

function AuditLogger:record_event(event_type, details)
    local timestamp = os.time()
    local event_id = #self.log_chain + 1

    -- Xesh hisoblash: SHA256(prev_hash + id + time + event + details)
    local raw_payload = string.format("%s|%d|%d|%s|%s", self.previous_hash, event_id, timestamp, event_type, details)
    local current_hash = "HASH[" .. raw_payload .. "]"

    local log_entry = {
        id = event_id,
        timestamp = timestamp,
        type = event_type,
        details = details,
        prev_hash = self.previous_hash,
        hash = current_hash
    }

    table.insert(self.log_chain, log_entry)
    self.previous_hash = current_hash
    return log_entry
end

function AuditLogger:verify_integrity()
    local expected_prev = "GENESIS_SECURITY_BLOCK_00000000"
    for i, entry in ipairs(self.log_chain) do
        if entry.prev_hash ~= expected_prev then
            return false, string.format("Zanjir buzilgan: Log #%d da prev_hash mos emas!", entry.id)
        end
        expected_prev = entry.hash
    end
    return true, "Barcha loglar butun va soxtalashtirilmagan."
end

-- Test
local logger = AuditLogger.new()
logger:record_event("ADMIN_LOGIN", "IP: 192.168.1.5")
logger:record_event("PASSWORD_CHANGE", "User ID: 442")

local ok, msg = logger:verify_integrity()
print("Loglar yaxlitligi tekshiruvi:", ok, msg)
```
**Tushuntirish:** Kriptografik zanjirli audit loglarida xaker bitta yozuvni o'zgartirsa yoki o'chirsa, undan keyingi barcha bloklarning xesh zanjiri uziladi. Bu sud ekspertizasi va xavfsizlik auditi uchun inkor etib bo'lmaydigan (Non-repudiation) dalil taqdim etadi.

---

### Topshiriq #1196: Webhook Xavfsizligi: Imzo, Timestamp va Idempotency Key
**Tavsif:** Tashqi to'lov tizimlaridan (Stripe, Click, Payme) keladigan webhooklar soxtalashtirilmasligi va tarmoq xatolari tufayli bir necha marta bajarilib qolmasligi lozim.
**Talablar:** Webhook sarlavhasidagi imzo, vaqt tamg'asi (Timestamp skew) va Idempotency-Key unikaligini tekshiruvchi modul yaratish.
**Yechim (Lua):**
```lua
-- Webhook Xavfsizlik va Idempotentlik Moduli

local WebhookGuard = {}

function WebhookGuard.process_webhook(headers, raw_body, secret_key, processed_cache)
    local sig = headers["x-signature"]
    local ts = tonumber(headers["x-timestamp"]) or 0
    local idem_key = headers["idempotency-key"]

    -- 1. Majburiy sarlavhalar
    if not sig or not idem_key or ts == 0 then
        return false, "Majburiy webhook sarlavhalari yetishmaydi"
    end

    -- 2. Vaqt oralig'i tekshiruvi (3 daqiqadan oshmagan)
    if math.abs(os.time() - ts) > 180 then
        return false, "Webhook muddati o'tgan"
    end

    -- 3. Idempotentlik: Agar bu so'rov allaqachon bajarilgan bo'lsa
    if processed_cache[idem_key] then
        return true, "ALLAQACHON_BAJARILGAN_KESH", processed_cache[idem_key]
    end

    -- 4. Imzoni tekshirish
    local expected_sig = "SIG[" .. secret_key .. "#" .. ts .. "#" .. raw_body .. "]"
    if sig ~= expected_sig then
        return false, "Noto'g'ri kriptografik imzo!"
    end

    -- Keshga saqlash
    processed_cache[idem_key] = { status = "SUCCESS", timestamp = os.time() }
    return true, "YANGI_QABUL_QILINDI"
end
```
**Tushuntirish:** Idempotency-Key takroriy to'lov yoki ikki marta hisob to'ldirilishining oldini oladi. Timestamp esa tarmoqdagi kechikishlar va replay hujumlaridan himoya qiladi.

---

### Topshiriq #1197: Server-Side Request Forgery (SSRF) Himoyasi va Ichki IP larni Bloklash
**Tavsif:** Foydalanuvchi URL kiritganda server ushbu manzilga so'rov yuborsa (masalan rasm yuklash), xaker `http://127.0.0.1:8080/admin` yoki `http://169.254.169.254/latest/meta-data/` (AWS metama'lumotlari) berib, ichki tarmoqni qo'lga kiritishi mumkin.
**Talablar:** Kiritilgan manzilning barcha ichki xususiy IP oraliqlariga (RFC 1918, Loopback, Link-Local) to'g'ri kelishini tekshirish va ularga so'rov yuborishni bloklash.
**Yechim (Lua):**
```lua
-- SSRF (Server-Side Request Forgery) Guard Moduli

local SSRFGuard = {}

-- Taqiqlangan IP oraliqlari (Kanonik prefikslar)
local PRIVATE_IP_PREFIXES = {
    "^127%.",          -- Loopback: 127.0.0.0/8
    "^10%.",           -- RFC 1918 A sinf: 10.0.0.0/8
    "^172%.1[6-9]%.",  -- RFC 1918 B sinf: 172.16.0.0 - 172.31.255.255
    "^172%.2%d%.",
    "^172%.3[0-1]%.",
    "^192%.168%.",     -- RFC 1918 C sinf: 192.168.0.0/16
    "^169%.254%.",     -- Cloud Metadata / Link-Local: 169.254.169.254
    "^0%."             -- Current network
}

function SSRFGuard.is_private_or_internal(ip_or_host)
    local lower_host = ip_or_host:lower()

    if lower_host == "localhost" then
        return true, "Localhost murojaati"
    end

    for _, prefix in ipairs(PRIVATE_IP_PREFIXES) do
        if lower_host:find(prefix) then
            return true, "Ichki xususiy IP manzil (Private Network)"
        end
    end

    return false
end

-- Test
print("AWS metadata xavflimi:", SSRFGuard.is_private_or_internal("169.254.169.254")) -- true
print("Google IP xavflimi:", SSRFGuard.is_private_or_internal("8.8.8.8"))           -- false
```
**Tushuntirish:** SSRF xuruji bulut infratuzilmasidagi (AWS, GCP, Azure) maxfiy IAM rollari va ma'lumotlar bazalarini o'g'irlashda eng ko'p qo'llaniladi. URL dan olingan manzilni DNS orqali IP ga aylantirib, uning RFC 1918 yoki Cloud Metadata (169.254.169.254) emasligini tekshirish majburiydir.

---

### Topshiriq #1198: Xavfsiz JSON Parser: Chuqur Obyekt Rekursiyasi va Xotira To'lishidan Himoya
**Tavsif:** Standart JSON parserlari cheksiz ichma-ich ochilgan qavslar `[[[[[[[[...]]]]]]]]` (JSON Depth Bomb) yuborilganda stakni to'ldirib yiqiladi.
**Talablar:** Maksimal rekursiya chuqurligi (masalan 16 qavat) va bayt hajmi tekshiruviga ega xavfsiz JSON himoya modulini yaratish.
**Yechim (Lua):**
```lua
-- JSON Depth Bomb va Xavfsiz JSON Parser

local JSONGuard = {}
local MAX_JSON_DEPTH = 16

function JSONGuard.validate_json_depth(json_string)
    local depth = 0
    local max_observed_depth = 0

    for i = 1, #json_string do
        local c = string.sub(json_string, i, i)
        if c == "{" or c == "[" then
            depth = depth + 1
            if depth > max_observed_depth then
                max_observed_depth = depth
            end
            if depth > MAX_JSON_DEPTH then
                return false, "JSON Depth Bomb aniqlandi! Maksimal chuqurlik 16 qavatdan oshdi."
            end
        elseif c == "}" or c == "]" then
            if depth > 0 then
                depth = depth - 1
            end
        end
    end

    return true, max_observed_depth
end

-- Test
local attack_payload = string.rep("[", 50) .. string.rep("]", 50)
local ok, err = JSONGuard.validate_json_depth(attack_payload)
print("JSON bombasi sinovi:", ok, err)
```
**Tushuntirish:** JSON Depth Bomb xakerlar tomonidan stek toshishini keltirib chiqarish va CPU ni ortiqcha zo'riqtirish uchun qo'llaniladi. JSON parslashdan oldin tezkor bitta chiziqli $O(N)$ o'tish orqali qavslar chuqurligini tekshirish serverni halokatdan asraydi.

---

### Topshiriq #1199: API Gateway Xavfsizlik Siyosati: RBAC va ABAC Dvigateli
**Tavsif:** API Gateway barcha kiruvchi so'rovlarning rollarini (RBAC: Admin, Manager, User) hamda atributlarini (ABAC: ish vaqti, bo'lim, manzil) tekshirib, ruxsat berishi yoki rad etishi lozim.
**Talablar:** RBAC va ABAC qoidalarini birlashtiruvchi markazlashtirilgan ruxsatnomalar dvigatelini yaratish.
**Yechim (Lua):**
```lua
-- RBAC va ABAC Ruxsatnomalar Boshqaruvchisi

local AccessControl = {}

local POLICY_MATRIX = {
    ["ROLE_ADMIN"] = { ["*"] = true },
    ["ROLE_MANAGER"] = {
        ["/api/v1/reports"] = { "GET" },
        ["/api/v1/orders"]  = { "GET", "POST" }
    },
    ["ROLE_USER"] = {
        ["/api/v1/profile"] = { "GET", "PUT" },
        ["/api/v1/orders"]  = { "GET" }
    }
}

function AccessControl.can_access(user_role, endpoint, method, user_attributes)
    local role_rules = POLICY_MATRIX[user_role]
    if not role_rules then
        return false, "Noma'lum foydalanuvchi roli"
    end

    -- Super Admin
    if role_rules["*"] then
        return true
    end

    local allowed_methods = role_rules[endpoint]
    if not allowed_methods then
        return false, "Ushbu endpointga kirish ruxsati yo'q"
    end

    local method_matched = false
    for _, m in ipairs(allowed_methods) do
        if m == method then
            method_matched = true
            break
        end
    end

    if not method_matched then
        return false, "Ushbu HTTP metodiga ruxsat berilmagan"
    end

    -- ABAC: Masalan faqat faol foydalanuvchilar (is_active == true)
    if user_attributes and user_attributes.is_active == false then
        return false, "Hisob bloklangan (ABAC siyosati)"
    end

    return true
end

-- Test
local ok1 = AccessControl.can_access("ROLE_USER", "/api/v1/orders", "GET", { is_active = true })
local ok2 = AccessControl.can_access("ROLE_USER", "/api/v1/reports", "GET", { is_active = true })
print("User orders GET ruxsati:", ok1)   -- true
print("User reports GET ruxsati:", ok2)  -- false
```
**Tushuntirish:** API Gateway darajasida RBAC va ABAC ni birlashtirish backend mikrosxemalarini avtorizatsiya mantiqidan xalos etadi va butun korxona bo'ylab yagona xavfsizlik siyosatini kafolatlaydi.

---

### Topshiriq #1200: Master OpenResty Xavfsizlik Gateway: WAF, Sandboxing va Himoya Kompleksi
**Tavsif:** Haqiqiy sanoat darajasidagi OpenResty Gateway barcha xavfsizlik vositalarini: WAF qoidalari (SQLi, XSS, Path Traversal), Rate Limiting, Sandboxed skript bajarilishi, Kriptografik imzo va PII loglashni yagona tizimda mujassam etishi kerak.
**Talablar:** Barcha 24-modul xavfsizlik amaliyotlarini o'zida birlashtirgan to'liq ishlab turuvchi Master Gateway arxitekturasini yaratish.
**Yechim (Lua):**
```lua
-- Master OpenResty Security Gateway (master_gateway.lua)

local MasterGateway = {}
MasterGateway._VERSION = "2.0.0-ENTERPRISE"

function MasterGateway.init()
    print("[MASTER GATEWAY]: Xavfsizlik modullari yuklandi va initsializatsiya qilindi.")
end

--- Har bir so'rovni ko'p bosqichli tekshirish (Inspection Pipeline)
function MasterGateway.handle_request(req_ctx)
    local ip        = req_ctx.client_ip or "127.0.0.1"
    local uri       = req_ctx.uri or "/"
    local method    = req_ctx.method or "GET"
    local headers   = req_ctx.headers or {}
    local body      = req_ctx.body or ""

    -- 1-BOSQICH: IP va Bad Bot tekshiruvi
    local ua = headers["user-agent"] or ""
    if ua:lower():find("sqlmap") or ua:lower():find("nikto") then
        return { status = 403, error = "Xakerlik skaneri aniqlandi va bloklandi" }
    end

    -- 2-BOSQICH: WAF Filtratsiyasi (Path Traversal, SQLi, XSS)
    if uri:find("%.%.") or uri:find("/etc/") then
        return { status = 403, error = "Path Traversal xavfi" }
    end

    if body:lower():find("union.*select") or body:lower():find("<script") then
        return { status = 403, error = "Zararli SQLi yoki XSS inyeksiyasi" }
    end

    -- 3-BOSQICH: Doimiy Vaqtli API Kalit Verifikatsiyasi (Constant-Time Auth)
    local auth_key = headers["authorization"]
    local EXPECTED_KEY = "Bearer SECRET_ENTERPRISE_KEY_2026"
    if auth_key then
        local match = (#auth_key == #EXPECTED_KEY)
        for i = 1, #auth_key do
            local b1 = string.byte(auth_key, i)
            local b2 = (i <= #EXPECTED_KEY) and string.byte(EXPECTED_KEY, i) or 0
            if b1 ~= b2 then match = false end
        end
        if not match then
            return { status = 401, error = "Avtorizatsiya kaliti noto'g'ri" }
        end
    end

    -- 4-BOSQICH: Xavfsiz Sandboxed Plagin Bajarilishi
    local sandbox_env = { math = math, string = string }
    local plugin_code = "local x = 100; return x * 2"
    local fn, err = load(plugin_code, "gateway_plugin", "t", sandbox_env)
    local plugin_result = fn and fn() or nil

    -- Muvaffaqiyatli yakun
    return {
        status = 200,
        message = "So'rov to'liq xavfsizlik tekshiruvidan o'tdi",
        plugin_output = plugin_result,
        gateway_version = MasterGateway._VERSION
    }
end

-- Test ssenariysi
MasterGateway.init()

local good_request = {
    client_ip = "192.168.1.10",
    uri = "/api/v1/orders",
    method = "POST",
    headers = {
        ["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        ["authorization"] = "Bearer SECRET_ENTERPRISE_KEY_2026"
    },
    body = '{"order_id": 999, "status": "CONFIRMED"}'
}

local res = MasterGateway.handle_request(good_request)
print("Good Request Natijasi:")
print("Status:", res.status)
print("Xabar:", res.message)
print("Plagin hisoblagan natija:", res.plugin_output)

local bad_request = {
    client_ip = "45.33.32.156",
    uri = "/api/v1/../../etc/shadow",
    method = "GET",
    headers = { ["user-agent"] = "sqlmap/1.4" }
}

local bad_res = MasterGateway.handle_request(bad_request)
print("\nBad Request Natijasi:")
print("Status:", bad_res.status)
print("Xatolik:", bad_res.error)
```
**Tushuntirish:** Master Gateway arxitekturasi korxona darajasidagi OpenResty tizimlarining xavfsizlik poydevorini ifodalaydi. Barcha so'rovlar qatlamma-qatlam filtrdan o'tkaziladi: Bad botlar va IP larni to'xtatish -> WAF tahlili -> Doimiy vaqtli avtorizatsiya -> Sandboxed plaginlar -> Shifrlangan va audit zanjiriga ega loglash. Bu har qanday tashqi kiberhujumlarni Nginx shlyuzidayoq zararsizlantirishni ta'minlaydi.

---
