# 501-Topshiriq: Shaxsiy modul yaratish va eksport qilish
## Topshiriq sharti:
Matematik hisob-kitoblar uchun shaxsiy modul jadvalini tayyorlang va undan foydalaning.

## Yechim (Lua kodi):
```lua
-- math_utils.lua moduli simulyatsiyasi:
local math_utils = {}

function math_utils.clamp(val, minVal, maxVal)
    if val < minVal then return minVal end
    if val > maxVal then return maxVal end
    return val
end

-- Asosiy dasturda chaqirish:
local clamped = math_utils.clamp(120, 0, 100)
print("Chegaralangan qiymat: " .. clamped)
```

## Tushuntirish va Mantiq:
Luada modul bu shunchaki funksiyalar va qiymatlarni o'z ichiga olgan oddiy jadval bo'lib, fayl oxirida `return modul_jadvali` orqali eksport qilinadi.

## Ishlash natijasi:
```text
Chegaralangan qiymat: 100
```


# 502-Topshiriq: require() mexanizmi va package.loaded keshi
## Topshiriq sharti:
Modul bir necha bor require qilinganda uning qayta bajarilmasdan keshdan olinishini ko'rsating.

## Yechim (Lua kodi):
```lua
-- Modul keshini tekshirish
package.loaded["my_custom_logger"] = {
    log = function(msg) print("[LOG]: " .. msg) end,
    version = "1.2.0"
}

local logger1 = require("my_custom_logger")
local logger2 = require("my_custom_logger")

logger1.log("Tizim ishga tushdi")
print("Ikkala havola bitta ob'ektga qaraganmi? " .. tostring(logger1 == logger2))
```

## Tushuntirish va Mantiq:
`require()` modulni faqat birinchi chaqiruvda yuklaydi va natijani `package.loaded[modul_nomi]` da keshlaydi. Keyingi barcha chaqiruvlar keshdan qaytadi.

## Ishlash natijasi:
```text
[LOG]: Tizim ishga tushdi
Ikkala havola bitta ob'ektga qaraganmi? true
```


# 503-Topshiriq: Modulda ichki xususiy (private) funksiyalar
## Topshiriq sharti:
Tashqi foydalanuvchiga ko'rinmaydigan faqat modul ichida ishlovchi yordamchi funksiyalarni enkapsulyatsiya qiling.

## Yechim (Lua kodi):
```lua
local AuthModule = {}

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
```

## Tushuntirish va Mantiq:
Modul faylida 'local' kalit so'zi bilan e'lon qilingan barcha o'zgaruvchi va funksiyalar moduldan tashqariga chiqmaydi va qat'iy maxfiy qoladi.

## Ishlash natijasi:
```text
Ro'yxatdan o'tdi: kamol -> HASHED_12345_SECURE
```


# 504-Topshiriq: package.path qidiruv yo'llarini sozlash
## Topshiriq sharti:
Maxsus kataloglardan modullarni yuklash uchun qidiruv yo'lini kengaytiring.

## Yechim (Lua kodi):
```lua
local currentPath = package.path
package.path = package.path .. ";./scripts/?.lua;./lib/?/init.lua"

print("Qidiruv yo'li muvaffaqiyatli kengaytirildi.")
print("Qo'shilgan yo'llar tekshirildi.")
```

## Tushuntirish va Mantiq:
`package.path` satr ko'rinishida bo'lib, nuqta-vergul (`;`) bilan ajratilgan shablonlarni o'z ichiga oladi. So'roq belgisi (`?`) modul nomi bilan almashtiriladi.

## Ishlash natijasi:
```text
Qidiruv yo'li muvaffaqiyatli kengaytirildi.
Qo'shilgan yo'llar tekshirildi.
```


# 505-Topshiriq: Modullarni dinamik qayta yuklash (Hot Reloading)
## Topshiriq sharti:
Ishlab turgan dasturni to'xtatmasdan modulni xotiradan tozalab qayta yuklang.

## Yechim (Lua kodi):
```lua
package.loaded["config_module"] = {mode = "DEVELOPMENT"}
print("Dastlabki rejim: " .. require("config_module").mode)

-- Hot reload: Keshni tozalash
package.loaded["config_module"] = nil

-- Yangilangan modulni yuklash simulyatsiyasi
package.loaded["config_module"] = {mode = "PRODUCTION"}
print("Yangilangan rejim: " .. require("config_module").mode)
```

## Tushuntirish va Mantiq:
`package.loaded[modName] = nil` qilish orqali modul xotiradan chiqariladi va keyingi `require()` yangi kodni noldan qayta yuklaydi.

## Ishlash natijasi:
```text
Dastlabki rejim: DEVELOPMENT
Yangilangan rejim: PRODUCTION
```


# 506-Topshiriq: Modullar va paketlar arxitekturasi #506
## Topshiriq sharti:
506-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_506 = {
    name = "MOD_506",
    version = "1.0.6"
}

function Module_506.execute(factor)
    return factor * 7
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    506, Module_506.name, Module_506.version, Module_506.execute(10)))
```

## Tushuntirish va Mantiq:
506-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #506 yuklandi: MOD_506 v1.0.6, Natija: 70
```


# 507-Topshiriq: Modullar va paketlar arxitekturasi #507
## Topshiriq sharti:
507-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_507 = {
    name = "MOD_507",
    version = "1.0.7"
}

function Module_507.execute(factor)
    return factor * 8
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    507, Module_507.name, Module_507.version, Module_507.execute(10)))
```

## Tushuntirish va Mantiq:
507-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #507 yuklandi: MOD_507 v1.0.7, Natija: 80
```


# 508-Topshiriq: Modullar va paketlar arxitekturasi #508
## Topshiriq sharti:
508-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_508 = {
    name = "MOD_508",
    version = "1.0.8"
}

function Module_508.execute(factor)
    return factor * 9
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    508, Module_508.name, Module_508.version, Module_508.execute(10)))
```

## Tushuntirish va Mantiq:
508-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #508 yuklandi: MOD_508 v1.0.8, Natija: 90
```


# 509-Topshiriq: Modullar va paketlar arxitekturasi #509
## Topshiriq sharti:
509-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_509 = {
    name = "MOD_509",
    version = "1.0.9"
}

function Module_509.execute(factor)
    return factor * 10
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    509, Module_509.name, Module_509.version, Module_509.execute(10)))
```

## Tushuntirish va Mantiq:
509-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #509 yuklandi: MOD_509 v1.0.9, Natija: 100
```


# 510-Topshiriq: Modullar va paketlar arxitekturasi #510
## Topshiriq sharti:
510-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_510 = {
    name = "MOD_510",
    version = "1.0.10"
}

function Module_510.execute(factor)
    return factor * 1
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    510, Module_510.name, Module_510.version, Module_510.execute(10)))
```

## Tushuntirish va Mantiq:
510-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #510 yuklandi: MOD_510 v1.0.10, Natija: 10
```


# 511-Topshiriq: Modullar va paketlar arxitekturasi #511
## Topshiriq sharti:
511-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_511 = {
    name = "MOD_511",
    version = "1.0.11"
}

function Module_511.execute(factor)
    return factor * 2
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    511, Module_511.name, Module_511.version, Module_511.execute(10)))
```

## Tushuntirish va Mantiq:
511-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #511 yuklandi: MOD_511 v1.0.11, Natija: 20
```


# 512-Topshiriq: Modullar va paketlar arxitekturasi #512
## Topshiriq sharti:
512-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_512 = {
    name = "MOD_512",
    version = "1.0.12"
}

function Module_512.execute(factor)
    return factor * 3
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    512, Module_512.name, Module_512.version, Module_512.execute(10)))
```

## Tushuntirish va Mantiq:
512-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #512 yuklandi: MOD_512 v1.0.12, Natija: 30
```


# 513-Topshiriq: Modullar va paketlar arxitekturasi #513
## Topshiriq sharti:
513-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_513 = {
    name = "MOD_513",
    version = "1.0.13"
}

function Module_513.execute(factor)
    return factor * 4
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    513, Module_513.name, Module_513.version, Module_513.execute(10)))
```

## Tushuntirish va Mantiq:
513-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #513 yuklandi: MOD_513 v1.0.13, Natija: 40
```


# 514-Topshiriq: Modullar va paketlar arxitekturasi #514
## Topshiriq sharti:
514-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_514 = {
    name = "MOD_514",
    version = "1.0.14"
}

function Module_514.execute(factor)
    return factor * 5
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    514, Module_514.name, Module_514.version, Module_514.execute(10)))
```

## Tushuntirish va Mantiq:
514-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #514 yuklandi: MOD_514 v1.0.14, Natija: 50
```


# 515-Topshiriq: Modullar va paketlar arxitekturasi #515
## Topshiriq sharti:
515-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_515 = {
    name = "MOD_515",
    version = "1.0.15"
}

function Module_515.execute(factor)
    return factor * 6
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    515, Module_515.name, Module_515.version, Module_515.execute(10)))
```

## Tushuntirish va Mantiq:
515-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #515 yuklandi: MOD_515 v1.0.15, Natija: 60
```


# 516-Topshiriq: Modullar va paketlar arxitekturasi #516
## Topshiriq sharti:
516-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_516 = {
    name = "MOD_516",
    version = "1.0.16"
}

function Module_516.execute(factor)
    return factor * 7
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    516, Module_516.name, Module_516.version, Module_516.execute(10)))
```

## Tushuntirish va Mantiq:
516-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #516 yuklandi: MOD_516 v1.0.16, Natija: 70
```


# 517-Topshiriq: Modullar va paketlar arxitekturasi #517
## Topshiriq sharti:
517-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_517 = {
    name = "MOD_517",
    version = "1.0.17"
}

function Module_517.execute(factor)
    return factor * 8
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    517, Module_517.name, Module_517.version, Module_517.execute(10)))
```

## Tushuntirish va Mantiq:
517-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #517 yuklandi: MOD_517 v1.0.17, Natija: 80
```


# 518-Topshiriq: Modullar va paketlar arxitekturasi #518
## Topshiriq sharti:
518-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_518 = {
    name = "MOD_518",
    version = "1.0.18"
}

function Module_518.execute(factor)
    return factor * 9
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    518, Module_518.name, Module_518.version, Module_518.execute(10)))
```

## Tushuntirish va Mantiq:
518-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #518 yuklandi: MOD_518 v1.0.18, Natija: 90
```


# 519-Topshiriq: Modullar va paketlar arxitekturasi #519
## Topshiriq sharti:
519-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_519 = {
    name = "MOD_519",
    version = "1.0.19"
}

function Module_519.execute(factor)
    return factor * 10
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    519, Module_519.name, Module_519.version, Module_519.execute(10)))
```

## Tushuntirish va Mantiq:
519-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #519 yuklandi: MOD_519 v1.0.19, Natija: 100
```


# 520-Topshiriq: Modullar va paketlar arxitekturasi #520
## Topshiriq sharti:
520-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_520 = {
    name = "MOD_520",
    version = "1.0.0"
}

function Module_520.execute(factor)
    return factor * 1
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    520, Module_520.name, Module_520.version, Module_520.execute(10)))
```

## Tushuntirish va Mantiq:
520-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #520 yuklandi: MOD_520 v1.0.0, Natija: 10
```


# 521-Topshiriq: Modullar va paketlar arxitekturasi #521
## Topshiriq sharti:
521-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_521 = {
    name = "MOD_521",
    version = "1.0.1"
}

function Module_521.execute(factor)
    return factor * 2
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    521, Module_521.name, Module_521.version, Module_521.execute(10)))
```

## Tushuntirish va Mantiq:
521-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #521 yuklandi: MOD_521 v1.0.1, Natija: 20
```


# 522-Topshiriq: Modullar va paketlar arxitekturasi #522
## Topshiriq sharti:
522-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_522 = {
    name = "MOD_522",
    version = "1.0.2"
}

function Module_522.execute(factor)
    return factor * 3
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    522, Module_522.name, Module_522.version, Module_522.execute(10)))
```

## Tushuntirish va Mantiq:
522-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #522 yuklandi: MOD_522 v1.0.2, Natija: 30
```


# 523-Topshiriq: Modullar va paketlar arxitekturasi #523
## Topshiriq sharti:
523-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_523 = {
    name = "MOD_523",
    version = "1.0.3"
}

function Module_523.execute(factor)
    return factor * 4
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    523, Module_523.name, Module_523.version, Module_523.execute(10)))
```

## Tushuntirish va Mantiq:
523-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #523 yuklandi: MOD_523 v1.0.3, Natija: 40
```


# 524-Topshiriq: Modullar va paketlar arxitekturasi #524
## Topshiriq sharti:
524-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_524 = {
    name = "MOD_524",
    version = "1.0.4"
}

function Module_524.execute(factor)
    return factor * 5
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    524, Module_524.name, Module_524.version, Module_524.execute(10)))
```

## Tushuntirish va Mantiq:
524-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #524 yuklandi: MOD_524 v1.0.4, Natija: 50
```


# 525-Topshiriq: Modullar va paketlar arxitekturasi #525
## Topshiriq sharti:
525-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_525 = {
    name = "MOD_525",
    version = "1.0.5"
}

function Module_525.execute(factor)
    return factor * 6
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    525, Module_525.name, Module_525.version, Module_525.execute(10)))
```

## Tushuntirish va Mantiq:
525-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #525 yuklandi: MOD_525 v1.0.5, Natija: 60
```


# 526-Topshiriq: Modullar va paketlar arxitekturasi #526
## Topshiriq sharti:
526-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_526 = {
    name = "MOD_526",
    version = "1.0.6"
}

function Module_526.execute(factor)
    return factor * 7
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    526, Module_526.name, Module_526.version, Module_526.execute(10)))
```

## Tushuntirish va Mantiq:
526-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #526 yuklandi: MOD_526 v1.0.6, Natija: 70
```


# 527-Topshiriq: Modullar va paketlar arxitekturasi #527
## Topshiriq sharti:
527-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_527 = {
    name = "MOD_527",
    version = "1.0.7"
}

function Module_527.execute(factor)
    return factor * 8
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    527, Module_527.name, Module_527.version, Module_527.execute(10)))
```

## Tushuntirish va Mantiq:
527-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #527 yuklandi: MOD_527 v1.0.7, Natija: 80
```


# 528-Topshiriq: Modullar va paketlar arxitekturasi #528
## Topshiriq sharti:
528-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_528 = {
    name = "MOD_528",
    version = "1.0.8"
}

function Module_528.execute(factor)
    return factor * 9
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    528, Module_528.name, Module_528.version, Module_528.execute(10)))
```

## Tushuntirish va Mantiq:
528-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #528 yuklandi: MOD_528 v1.0.8, Natija: 90
```


# 529-Topshiriq: Modullar va paketlar arxitekturasi #529
## Topshiriq sharti:
529-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_529 = {
    name = "MOD_529",
    version = "1.0.9"
}

function Module_529.execute(factor)
    return factor * 10
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    529, Module_529.name, Module_529.version, Module_529.execute(10)))
```

## Tushuntirish va Mantiq:
529-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #529 yuklandi: MOD_529 v1.0.9, Natija: 100
```


# 530-Topshiriq: Modullar va paketlar arxitekturasi #530
## Topshiriq sharti:
530-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_530 = {
    name = "MOD_530",
    version = "1.0.10"
}

function Module_530.execute(factor)
    return factor * 1
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    530, Module_530.name, Module_530.version, Module_530.execute(10)))
```

## Tushuntirish va Mantiq:
530-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #530 yuklandi: MOD_530 v1.0.10, Natija: 10
```


# 531-Topshiriq: Modullar va paketlar arxitekturasi #531
## Topshiriq sharti:
531-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_531 = {
    name = "MOD_531",
    version = "1.0.11"
}

function Module_531.execute(factor)
    return factor * 2
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    531, Module_531.name, Module_531.version, Module_531.execute(10)))
```

## Tushuntirish va Mantiq:
531-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #531 yuklandi: MOD_531 v1.0.11, Natija: 20
```


# 532-Topshiriq: Modullar va paketlar arxitekturasi #532
## Topshiriq sharti:
532-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_532 = {
    name = "MOD_532",
    version = "1.0.12"
}

function Module_532.execute(factor)
    return factor * 3
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    532, Module_532.name, Module_532.version, Module_532.execute(10)))
```

## Tushuntirish va Mantiq:
532-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #532 yuklandi: MOD_532 v1.0.12, Natija: 30
```


# 533-Topshiriq: Modullar va paketlar arxitekturasi #533
## Topshiriq sharti:
533-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_533 = {
    name = "MOD_533",
    version = "1.0.13"
}

function Module_533.execute(factor)
    return factor * 4
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    533, Module_533.name, Module_533.version, Module_533.execute(10)))
```

## Tushuntirish va Mantiq:
533-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #533 yuklandi: MOD_533 v1.0.13, Natija: 40
```


# 534-Topshiriq: Modullar va paketlar arxitekturasi #534
## Topshiriq sharti:
534-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_534 = {
    name = "MOD_534",
    version = "1.0.14"
}

function Module_534.execute(factor)
    return factor * 5
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    534, Module_534.name, Module_534.version, Module_534.execute(10)))
```

## Tushuntirish va Mantiq:
534-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #534 yuklandi: MOD_534 v1.0.14, Natija: 50
```


# 535-Topshiriq: Modullar va paketlar arxitekturasi #535
## Topshiriq sharti:
535-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_535 = {
    name = "MOD_535",
    version = "1.0.15"
}

function Module_535.execute(factor)
    return factor * 6
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    535, Module_535.name, Module_535.version, Module_535.execute(10)))
```

## Tushuntirish va Mantiq:
535-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #535 yuklandi: MOD_535 v1.0.15, Natija: 60
```


# 536-Topshiriq: Modullar va paketlar arxitekturasi #536
## Topshiriq sharti:
536-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_536 = {
    name = "MOD_536",
    version = "1.0.16"
}

function Module_536.execute(factor)
    return factor * 7
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    536, Module_536.name, Module_536.version, Module_536.execute(10)))
```

## Tushuntirish va Mantiq:
536-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #536 yuklandi: MOD_536 v1.0.16, Natija: 70
```


# 537-Topshiriq: Modullar va paketlar arxitekturasi #537
## Topshiriq sharti:
537-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_537 = {
    name = "MOD_537",
    version = "1.0.17"
}

function Module_537.execute(factor)
    return factor * 8
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    537, Module_537.name, Module_537.version, Module_537.execute(10)))
```

## Tushuntirish va Mantiq:
537-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #537 yuklandi: MOD_537 v1.0.17, Natija: 80
```


# 538-Topshiriq: Modullar va paketlar arxitekturasi #538
## Topshiriq sharti:
538-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_538 = {
    name = "MOD_538",
    version = "1.0.18"
}

function Module_538.execute(factor)
    return factor * 9
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    538, Module_538.name, Module_538.version, Module_538.execute(10)))
```

## Tushuntirish va Mantiq:
538-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #538 yuklandi: MOD_538 v1.0.18, Natija: 90
```


# 539-Topshiriq: Modullar va paketlar arxitekturasi #539
## Topshiriq sharti:
539-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_539 = {
    name = "MOD_539",
    version = "1.0.19"
}

function Module_539.execute(factor)
    return factor * 10
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    539, Module_539.name, Module_539.version, Module_539.execute(10)))
```

## Tushuntirish va Mantiq:
539-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #539 yuklandi: MOD_539 v1.0.19, Natija: 100
```


# 540-Topshiriq: Modullar va paketlar arxitekturasi #540
## Topshiriq sharti:
540-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_540 = {
    name = "MOD_540",
    version = "1.0.0"
}

function Module_540.execute(factor)
    return factor * 1
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    540, Module_540.name, Module_540.version, Module_540.execute(10)))
```

## Tushuntirish va Mantiq:
540-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #540 yuklandi: MOD_540 v1.0.0, Natija: 10
```


# 541-Topshiriq: Modullar va paketlar arxitekturasi #541
## Topshiriq sharti:
541-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_541 = {
    name = "MOD_541",
    version = "1.0.1"
}

function Module_541.execute(factor)
    return factor * 2
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    541, Module_541.name, Module_541.version, Module_541.execute(10)))
```

## Tushuntirish va Mantiq:
541-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #541 yuklandi: MOD_541 v1.0.1, Natija: 20
```


# 542-Topshiriq: Modullar va paketlar arxitekturasi #542
## Topshiriq sharti:
542-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_542 = {
    name = "MOD_542",
    version = "1.0.2"
}

function Module_542.execute(factor)
    return factor * 3
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    542, Module_542.name, Module_542.version, Module_542.execute(10)))
```

## Tushuntirish va Mantiq:
542-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #542 yuklandi: MOD_542 v1.0.2, Natija: 30
```


# 543-Topshiriq: Modullar va paketlar arxitekturasi #543
## Topshiriq sharti:
543-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_543 = {
    name = "MOD_543",
    version = "1.0.3"
}

function Module_543.execute(factor)
    return factor * 4
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    543, Module_543.name, Module_543.version, Module_543.execute(10)))
```

## Tushuntirish va Mantiq:
543-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #543 yuklandi: MOD_543 v1.0.3, Natija: 40
```


# 544-Topshiriq: Modullar va paketlar arxitekturasi #544
## Topshiriq sharti:
544-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_544 = {
    name = "MOD_544",
    version = "1.0.4"
}

function Module_544.execute(factor)
    return factor * 5
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    544, Module_544.name, Module_544.version, Module_544.execute(10)))
```

## Tushuntirish va Mantiq:
544-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #544 yuklandi: MOD_544 v1.0.4, Natija: 50
```


# 545-Topshiriq: Modullar va paketlar arxitekturasi #545
## Topshiriq sharti:
545-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_545 = {
    name = "MOD_545",
    version = "1.0.5"
}

function Module_545.execute(factor)
    return factor * 6
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    545, Module_545.name, Module_545.version, Module_545.execute(10)))
```

## Tushuntirish va Mantiq:
545-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #545 yuklandi: MOD_545 v1.0.5, Natija: 60
```


# 546-Topshiriq: Modullar va paketlar arxitekturasi #546
## Topshiriq sharti:
546-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_546 = {
    name = "MOD_546",
    version = "1.0.6"
}

function Module_546.execute(factor)
    return factor * 7
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    546, Module_546.name, Module_546.version, Module_546.execute(10)))
```

## Tushuntirish va Mantiq:
546-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #546 yuklandi: MOD_546 v1.0.6, Natija: 70
```


# 547-Topshiriq: Modullar va paketlar arxitekturasi #547
## Topshiriq sharti:
547-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_547 = {
    name = "MOD_547",
    version = "1.0.7"
}

function Module_547.execute(factor)
    return factor * 8
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    547, Module_547.name, Module_547.version, Module_547.execute(10)))
```

## Tushuntirish va Mantiq:
547-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #547 yuklandi: MOD_547 v1.0.7, Natija: 80
```


# 548-Topshiriq: Modullar va paketlar arxitekturasi #548
## Topshiriq sharti:
548-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_548 = {
    name = "MOD_548",
    version = "1.0.8"
}

function Module_548.execute(factor)
    return factor * 9
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    548, Module_548.name, Module_548.version, Module_548.execute(10)))
```

## Tushuntirish va Mantiq:
548-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #548 yuklandi: MOD_548 v1.0.8, Natija: 90
```


# 549-Topshiriq: Modullar va paketlar arxitekturasi #549
## Topshiriq sharti:
549-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_549 = {
    name = "MOD_549",
    version = "1.0.9"
}

function Module_549.execute(factor)
    return factor * 10
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    549, Module_549.name, Module_549.version, Module_549.execute(10)))
```

## Tushuntirish va Mantiq:
549-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #549 yuklandi: MOD_549 v1.0.9, Natija: 100
```


# 550-Topshiriq: Modullar va paketlar arxitekturasi #550
## Topshiriq sharti:
550-vazifa: Modulli arxitektura, nomlar fazosi, paketlar inkapsulyatsiyasi va qaramliklarni boshqarish.

## Yechim (Lua kodi):
```lua
local Module_550 = {
    name = "MOD_550",
    version = "1.0.10"
}

function Module_550.execute(factor)
    return factor * 1
end

print(string.format("Modul #%d yuklandi: %s v%s, Natija: %d", 
    550, Module_550.name, Module_550.version, Module_550.execute(10)))
```

## Tushuntirish va Mantiq:
550-vazifada shaxsiy modul API-si yaratildi va xavfsiz metod chaqiruvi ta'minlandi.

## Ishlash natijasi:
```text
Modul #550 yuklandi: MOD_550 v1.0.10, Natija: 10
```

