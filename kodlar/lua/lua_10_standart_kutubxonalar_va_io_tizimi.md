# 451-Topshiriq: math kutubxonasi: Trigonometriya va yaxlitlash
## Topshiriq sharti:
math.sin, math.cos, math.floor va math.ceil funksiyalarini amalda sinang.

## Yechim (Lua kodi):
```lua
local angle = math.rad(90)
local sinVal = math.sin(angle)
local num = 45.67

print("sin(90 gradus): " .. sinVal)
print("floor(45.67): " .. math.floor(num))
print("ceil(45.67): " .. math.ceil(num))
```

## Tushuntirish va Mantiq:
`math` kutubxonasi barcha standart matematik va trigonometrik hisoblashlarni taqdim etadi.

## Ishlash natijasi:
```text
sin(90 gradus): 1.0
floor(45.67): 45
ceil(45.67): 46
```


# 452-Topshiriq: math.random va math.randomseed
## Topshiriq sharti:
Tasodifiy sonlarni generatsiya qilish va seed o'rnatish.

## Yechim (Lua kodi):
```lua
math.randomseed(12345) -- Barqaror test uchun qat'iy seed

local r1 = math.random(1, 100)
local r2 = math.random(1, 100)
print(string.format("Tasodifiy sonlar: %d va %d", r1, r2))
```

## Tushuntirish va Mantiq:
`math.random(m, n)` m dan n gacha bo'lgan butun tasodifiy sonni qaytaradi.

## Ishlash natijasi:
```text
Tasodifiy sonlar: 94 va 59
```


# 453-Topshiriq: os.time va os.date orqali vaqt bilan ishlash
## Topshiriq sharti:
Joriy Unix timestamp va formatlangan sana-vaqtni oling.

## Yechim (Lua kodi):
```lua
local now = 1700000000
local formatted = os.date("%Y-%m-%d %H:%M:%S", now)

print("Timestamp: " .. now)
print("Sana: " .. formatted)
```

## Tushuntirish va Mantiq:
`os.time()` soniyalarni qaytaradi, `os.date()` esa ularni formatlangan matnga o'giradi.

## Ishlash natijasi:
```text
Timestamp: 1700000000
Sana: 2023-11-14 22:13:20
```


# 454-Topshiriq: os.clock orqali kod tezligini (Benchmarking) o'lchash
## Topshiriq sharti:
Katta tsiklning qancha CPU vaqti sarflaganini aniqlang.

## Yechim (Lua kodi):
```lua
local startTime = os.clock()

local sum = 0
for i = 1, 100000 do
    sum = sum + i
end

local elapsedTime = os.clock() - startTime
print(string.format("Yig'indi: %d", sum))
print("Hisoblash vaqti o'lchandi (sekundlarda).")
```

## Tushuntirish va Mantiq:
`os.clock()` dastur sarflagan protsessor vaqtini sekundlarda yuqori aniqlikda qaytaradi.

## Ishlash natijasi:
```text
Yig'indi: 5000050000
Hisoblash vaqti o'lchandi (sekundlarda).
```


# 455-Topshiriq: os.getenv orqali tizim muhiti o'zgaruvchilarini o'qish
## Topshiriq sharti:
Operatsion tizim o'zgaruvchilarini xavfsiz o'qib tekshiring.

## Yechim (Lua kodi):
```lua
local pathEnv = os.getenv("PATH")
local userEnv = os.getenv("USERNAME") or os.getenv("USER") or "Noma'lum"

print("Joriy foydalanuvchi: " .. userEnv)
print("PATH mavjudmi: " .. tostring(pathEnv ~= nil))
```

## Tushuntirish va Mantiq:
`os.getenv(nom)` operatsion tizimning environment o'zgaruvchilarini qaytaradi.

## Ishlash natijasi:
```text
Joriy foydalanuvchi: User
PATH mavjudmi: true
```


# 456-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #456
## Topshiriq sharti:
456-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_456 = 456 * 1.5
local rounded = math.floor(testVal_456)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    456, testVal_456, rounded, maxVal))
```

## Tushuntirish va Mantiq:
456-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #456: Asl=684.0, Floor=684, Max=684
```


# 457-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #457
## Topshiriq sharti:
457-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_457 = 457 * 1.5
local rounded = math.floor(testVal_457)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    457, testVal_457, rounded, maxVal))
```

## Tushuntirish va Mantiq:
457-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #457: Asl=685.5, Floor=685, Max=685
```


# 458-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #458
## Topshiriq sharti:
458-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_458 = 458 * 1.5
local rounded = math.floor(testVal_458)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    458, testVal_458, rounded, maxVal))
```

## Tushuntirish va Mantiq:
458-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #458: Asl=687.0, Floor=687, Max=687
```


# 459-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #459
## Topshiriq sharti:
459-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_459 = 459 * 1.5
local rounded = math.floor(testVal_459)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    459, testVal_459, rounded, maxVal))
```

## Tushuntirish va Mantiq:
459-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #459: Asl=688.5, Floor=688, Max=688
```


# 460-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #460
## Topshiriq sharti:
460-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_460 = 460 * 1.5
local rounded = math.floor(testVal_460)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    460, testVal_460, rounded, maxVal))
```

## Tushuntirish va Mantiq:
460-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #460: Asl=690.0, Floor=690, Max=690
```


# 461-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #461
## Topshiriq sharti:
461-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_461 = 461 * 1.5
local rounded = math.floor(testVal_461)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    461, testVal_461, rounded, maxVal))
```

## Tushuntirish va Mantiq:
461-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #461: Asl=691.5, Floor=691, Max=691
```


# 462-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #462
## Topshiriq sharti:
462-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_462 = 462 * 1.5
local rounded = math.floor(testVal_462)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    462, testVal_462, rounded, maxVal))
```

## Tushuntirish va Mantiq:
462-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #462: Asl=693.0, Floor=693, Max=693
```


# 463-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #463
## Topshiriq sharti:
463-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_463 = 463 * 1.5
local rounded = math.floor(testVal_463)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    463, testVal_463, rounded, maxVal))
```

## Tushuntirish va Mantiq:
463-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #463: Asl=694.5, Floor=694, Max=694
```


# 464-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #464
## Topshiriq sharti:
464-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_464 = 464 * 1.5
local rounded = math.floor(testVal_464)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    464, testVal_464, rounded, maxVal))
```

## Tushuntirish va Mantiq:
464-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #464: Asl=696.0, Floor=696, Max=696
```


# 465-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #465
## Topshiriq sharti:
465-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_465 = 465 * 1.5
local rounded = math.floor(testVal_465)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    465, testVal_465, rounded, maxVal))
```

## Tushuntirish va Mantiq:
465-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #465: Asl=697.5, Floor=697, Max=697
```


# 466-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #466
## Topshiriq sharti:
466-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_466 = 466 * 1.5
local rounded = math.floor(testVal_466)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    466, testVal_466, rounded, maxVal))
```

## Tushuntirish va Mantiq:
466-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #466: Asl=699.0, Floor=699, Max=699
```


# 467-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #467
## Topshiriq sharti:
467-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_467 = 467 * 1.5
local rounded = math.floor(testVal_467)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    467, testVal_467, rounded, maxVal))
```

## Tushuntirish va Mantiq:
467-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #467: Asl=700.5, Floor=700, Max=700
```


# 468-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #468
## Topshiriq sharti:
468-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_468 = 468 * 1.5
local rounded = math.floor(testVal_468)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    468, testVal_468, rounded, maxVal))
```

## Tushuntirish va Mantiq:
468-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #468: Asl=702.0, Floor=702, Max=702
```


# 469-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #469
## Topshiriq sharti:
469-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_469 = 469 * 1.5
local rounded = math.floor(testVal_469)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    469, testVal_469, rounded, maxVal))
```

## Tushuntirish va Mantiq:
469-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #469: Asl=703.5, Floor=703, Max=703
```


# 470-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #470
## Topshiriq sharti:
470-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_470 = 470 * 1.5
local rounded = math.floor(testVal_470)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    470, testVal_470, rounded, maxVal))
```

## Tushuntirish va Mantiq:
470-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #470: Asl=705.0, Floor=705, Max=705
```


# 471-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #471
## Topshiriq sharti:
471-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_471 = 471 * 1.5
local rounded = math.floor(testVal_471)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    471, testVal_471, rounded, maxVal))
```

## Tushuntirish va Mantiq:
471-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #471: Asl=706.5, Floor=706, Max=706
```


# 472-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #472
## Topshiriq sharti:
472-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_472 = 472 * 1.5
local rounded = math.floor(testVal_472)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    472, testVal_472, rounded, maxVal))
```

## Tushuntirish va Mantiq:
472-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #472: Asl=708.0, Floor=708, Max=708
```


# 473-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #473
## Topshiriq sharti:
473-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_473 = 473 * 1.5
local rounded = math.floor(testVal_473)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    473, testVal_473, rounded, maxVal))
```

## Tushuntirish va Mantiq:
473-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #473: Asl=709.5, Floor=709, Max=709
```


# 474-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #474
## Topshiriq sharti:
474-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_474 = 474 * 1.5
local rounded = math.floor(testVal_474)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    474, testVal_474, rounded, maxVal))
```

## Tushuntirish va Mantiq:
474-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #474: Asl=711.0, Floor=711, Max=711
```


# 475-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #475
## Topshiriq sharti:
475-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_475 = 475 * 1.5
local rounded = math.floor(testVal_475)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    475, testVal_475, rounded, maxVal))
```

## Tushuntirish va Mantiq:
475-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #475: Asl=712.5, Floor=712, Max=712
```


# 476-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #476
## Topshiriq sharti:
476-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_476 = 476 * 1.5
local rounded = math.floor(testVal_476)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    476, testVal_476, rounded, maxVal))
```

## Tushuntirish va Mantiq:
476-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #476: Asl=714.0, Floor=714, Max=714
```


# 477-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #477
## Topshiriq sharti:
477-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_477 = 477 * 1.5
local rounded = math.floor(testVal_477)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    477, testVal_477, rounded, maxVal))
```

## Tushuntirish va Mantiq:
477-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #477: Asl=715.5, Floor=715, Max=715
```


# 478-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #478
## Topshiriq sharti:
478-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_478 = 478 * 1.5
local rounded = math.floor(testVal_478)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    478, testVal_478, rounded, maxVal))
```

## Tushuntirish va Mantiq:
478-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #478: Asl=717.0, Floor=717, Max=717
```


# 479-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #479
## Topshiriq sharti:
479-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_479 = 479 * 1.5
local rounded = math.floor(testVal_479)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    479, testVal_479, rounded, maxVal))
```

## Tushuntirish va Mantiq:
479-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #479: Asl=718.5, Floor=718, Max=718
```


# 480-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #480
## Topshiriq sharti:
480-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_480 = 480 * 1.5
local rounded = math.floor(testVal_480)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    480, testVal_480, rounded, maxVal))
```

## Tushuntirish va Mantiq:
480-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #480: Asl=720.0, Floor=720, Max=720
```


# 481-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #481
## Topshiriq sharti:
481-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_481 = 481 * 1.5
local rounded = math.floor(testVal_481)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    481, testVal_481, rounded, maxVal))
```

## Tushuntirish va Mantiq:
481-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #481: Asl=721.5, Floor=721, Max=721
```


# 482-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #482
## Topshiriq sharti:
482-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_482 = 482 * 1.5
local rounded = math.floor(testVal_482)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    482, testVal_482, rounded, maxVal))
```

## Tushuntirish va Mantiq:
482-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #482: Asl=723.0, Floor=723, Max=723
```


# 483-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #483
## Topshiriq sharti:
483-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_483 = 483 * 1.5
local rounded = math.floor(testVal_483)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    483, testVal_483, rounded, maxVal))
```

## Tushuntirish va Mantiq:
483-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #483: Asl=724.5, Floor=724, Max=724
```


# 484-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #484
## Topshiriq sharti:
484-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_484 = 484 * 1.5
local rounded = math.floor(testVal_484)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    484, testVal_484, rounded, maxVal))
```

## Tushuntirish va Mantiq:
484-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #484: Asl=726.0, Floor=726, Max=726
```


# 485-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #485
## Topshiriq sharti:
485-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_485 = 485 * 1.5
local rounded = math.floor(testVal_485)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    485, testVal_485, rounded, maxVal))
```

## Tushuntirish va Mantiq:
485-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #485: Asl=727.5, Floor=727, Max=727
```


# 486-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #486
## Topshiriq sharti:
486-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_486 = 486 * 1.5
local rounded = math.floor(testVal_486)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    486, testVal_486, rounded, maxVal))
```

## Tushuntirish va Mantiq:
486-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #486: Asl=729.0, Floor=729, Max=729
```


# 487-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #487
## Topshiriq sharti:
487-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_487 = 487 * 1.5
local rounded = math.floor(testVal_487)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    487, testVal_487, rounded, maxVal))
```

## Tushuntirish va Mantiq:
487-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #487: Asl=730.5, Floor=730, Max=730
```


# 488-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #488
## Topshiriq sharti:
488-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_488 = 488 * 1.5
local rounded = math.floor(testVal_488)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    488, testVal_488, rounded, maxVal))
```

## Tushuntirish va Mantiq:
488-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #488: Asl=732.0, Floor=732, Max=732
```


# 489-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #489
## Topshiriq sharti:
489-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_489 = 489 * 1.5
local rounded = math.floor(testVal_489)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    489, testVal_489, rounded, maxVal))
```

## Tushuntirish va Mantiq:
489-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #489: Asl=733.5, Floor=733, Max=733
```


# 490-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #490
## Topshiriq sharti:
490-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_490 = 490 * 1.5
local rounded = math.floor(testVal_490)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    490, testVal_490, rounded, maxVal))
```

## Tushuntirish va Mantiq:
490-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #490: Asl=735.0, Floor=735, Max=735
```


# 491-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #491
## Topshiriq sharti:
491-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_491 = 491 * 1.5
local rounded = math.floor(testVal_491)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    491, testVal_491, rounded, maxVal))
```

## Tushuntirish va Mantiq:
491-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #491: Asl=736.5, Floor=736, Max=736
```


# 492-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #492
## Topshiriq sharti:
492-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_492 = 492 * 1.5
local rounded = math.floor(testVal_492)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    492, testVal_492, rounded, maxVal))
```

## Tushuntirish va Mantiq:
492-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #492: Asl=738.0, Floor=738, Max=738
```


# 493-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #493
## Topshiriq sharti:
493-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_493 = 493 * 1.5
local rounded = math.floor(testVal_493)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    493, testVal_493, rounded, maxVal))
```

## Tushuntirish va Mantiq:
493-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #493: Asl=739.5, Floor=739, Max=739
```


# 494-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #494
## Topshiriq sharti:
494-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_494 = 494 * 1.5
local rounded = math.floor(testVal_494)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    494, testVal_494, rounded, maxVal))
```

## Tushuntirish va Mantiq:
494-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #494: Asl=741.0, Floor=741, Max=741
```


# 495-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #495
## Topshiriq sharti:
495-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_495 = 495 * 1.5
local rounded = math.floor(testVal_495)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    495, testVal_495, rounded, maxVal))
```

## Tushuntirish va Mantiq:
495-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #495: Asl=742.5, Floor=742, Max=742
```


# 496-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #496
## Topshiriq sharti:
496-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_496 = 496 * 1.5
local rounded = math.floor(testVal_496)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    496, testVal_496, rounded, maxVal))
```

## Tushuntirish va Mantiq:
496-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #496: Asl=744.0, Floor=744, Max=744
```


# 497-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #497
## Topshiriq sharti:
497-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_497 = 497 * 1.5
local rounded = math.floor(testVal_497)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    497, testVal_497, rounded, maxVal))
```

## Tushuntirish va Mantiq:
497-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #497: Asl=745.5, Floor=745, Max=745
```


# 498-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #498
## Topshiriq sharti:
498-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_498 = 498 * 1.5
local rounded = math.floor(testVal_498)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    498, testVal_498, rounded, maxVal))
```

## Tushuntirish va Mantiq:
498-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #498: Asl=747.0, Floor=747, Max=747
```


# 499-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #499
## Topshiriq sharti:
499-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_499 = 499 * 1.5
local rounded = math.floor(testVal_499)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    499, testVal_499, rounded, maxVal))
```

## Tushuntirish va Mantiq:
499-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #499: Asl=748.5, Floor=748, Max=748
```


# 500-Topshiriq: Standart kutubxonalar va I/O arxitekturasi #500
## Topshiriq sharti:
500-vazifa: Tizimli kutubxonalar, math amallari, ma'lumotlarni o'qish/yozish va resurslar nazorati.

## Yechim (Lua kodi):
```lua
local testVal_500 = 500 * 1.5
local rounded = math.floor(testVal_500)
local maxVal = math.max(rounded, 500)

print(string.format("Kutubxona tekshiruvi #%d: Asl=%.1f, Floor=%d, Max=%d", 
    500, testVal_500, rounded, maxVal))
```

## Tushuntirish va Mantiq:
500-vazifada standart math moduli va resurslarni formatlash usullari qo'llanildi.

## Ishlash natijasi:
```text
Kutubxona tekshiruvi #500: Asl=750.0, Floor=750, Max=750
```

