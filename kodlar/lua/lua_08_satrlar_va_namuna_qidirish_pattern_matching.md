# 351-Topshiriq: string.format yordamida matnlarni formatlash
## Topshiriq sharti:
Sonlarni, suzuvchi kasrlarni va satrlarni C uslubidagi formatlash bilan chiqaring.

## Yechim (Lua kodi):
```lua
local name = "Azizbek"
local score = 94.678
local id = 7

local output = string.format("Foydalanuvchi: %s | ID: %04d | Ball: %.2f", name, id, score)
print(output)
```

## Tushuntirish va Mantiq:
`string.format` C tilidagi `printf` formati bo'yicha matnlarni mukammal formatlaydi.

## Ishlash natijasi:
```text
Foydalanuvchi: Azizbek | ID: 0007 | Ball: 94.68
```


# 352-Topshiriq: string.sub orqali satrdan qism ajratib olish
## Topshiriq sharti:
Satrning boshlang'ich va oxirgi qismlarini musbat va manfiy indekslar yordamida oling.

## Yechim (Lua kodi):
```lua
local text = "Toshkent - Go'zal Poytaxt"

local part1 = string.sub(text, 1, 8)
local part2 = string.sub(text, -7)

print("Boshi: " .. part1)
print("Oxiri: " .. part2)
```

## Tushuntirish va Mantiq:
`string.sub(s, start, finish)` qirqib oladi. Manfiy sonlar satr oxiridan sanaydi.

## Ishlash natijasi:
```text
Boshi: Toshkent
Oxiri: Poytaxt
```


# 353-Topshiriq: string.find orqali qidiruv
## Topshiriq sharti:
Matn ichida qidirilayotgan so'zning boshlang'ich va oxirgi indekslarini toping.

## Yechim (Lua kodi):
```lua
local quote = "Dasturlash - mantiqiy tafakkur san'ati"
local startIdx, endIdx = string.find(quote, "mantiqiy")

print("Boshlanish indeksi: " .. startIdx)
print("Tugash indeksi: " .. endIdx)
print("Ajratib olingan so'z: " .. string.sub(quote, startIdx, endIdx))
```

## Tushuntirish va Mantiq:
`string.find` mos kelgan namunaning start va end indekslarini qaytaradi.

## Ishlash natijasi:
```text
Boshlanish indeksi: 15
Tugash indeksi: 22
Ajratib olingan so'z: mantiqiy
```


# 354-Topshiriq: Lua Pattern Matching: Maxsus belgilar (%d, %a, %s, %w)
## Topshiriq sharti:
Telefon raqami va login nomini tekshirish uchun Lua andozalaridan foydalaning.

## Yechim (Lua kodi):
```lua
local phoneStr = "Tel: 998901234567"
local digitsOnly = string.match(phoneStr, "%d+")

print("Ajratilgan raqamlar: " .. digitsOnly)
```

## Tushuntirish va Mantiq:
Luada Regex o'rniga tezkor va ixcham Pattern Matching ishlatiladi: `%d` - raqamlar, `%a` - harflar, `%s` - bo'shliqlar, `%w` - harf-raqamlar.

## Ishlash natijasi:
```text
Ajratilgan raqamlar: 998901234567
```


# 355-Topshiriq: string.gsub orqali matnni almashtirish
## Topshiriq sharti:
Matndagi barcha nuqtalarni chiziqcha bilan almashtiring va almashtirishlar sonini oling.

## Yechim (Lua kodi):
```lua
local dateStr = "2026.11.08"
local newDate, count = string.gsub(dateStr, "%.", "-")

print("Yangi sana: " .. newDate)
print("Almashtirishlar soni: " .. count)
```

## Tushuntirish va Mantiq:
`string.gsub(s, pattern, repl)` almashtirilgan yangi satrni va almashtirishlar sonini qaytaradi.

## Ishlash natijasi:
```text
Yangi sana: 2026-11-08
Almashtirishlar soni: 2
```


# 356-Topshiriq: Satrlar va pattern matching muhandisligi #356
## Topshiriq sharti:
356-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_356 = "SENSOR_ID:356;TEMP:45.6;STATUS:OK"
local id, temp, status = string.match(rawData_356, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
356-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 356, Harorat: 45.6 C, Status: OK
```


# 357-Topshiriq: Satrlar va pattern matching muhandisligi #357
## Topshiriq sharti:
357-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_357 = "SENSOR_ID:357;TEMP:45.7;STATUS:OK"
local id, temp, status = string.match(rawData_357, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
357-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 357, Harorat: 45.7 C, Status: OK
```


# 358-Topshiriq: Satrlar va pattern matching muhandisligi #358
## Topshiriq sharti:
358-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_358 = "SENSOR_ID:358;TEMP:45.8;STATUS:OK"
local id, temp, status = string.match(rawData_358, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
358-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 358, Harorat: 45.8 C, Status: OK
```


# 359-Topshiriq: Satrlar va pattern matching muhandisligi #359
## Topshiriq sharti:
359-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_359 = "SENSOR_ID:359;TEMP:45.9;STATUS:OK"
local id, temp, status = string.match(rawData_359, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
359-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 359, Harorat: 45.9 C, Status: OK
```


# 360-Topshiriq: Satrlar va pattern matching muhandisligi #360
## Topshiriq sharti:
360-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_360 = "SENSOR_ID:360;TEMP:45.0;STATUS:OK"
local id, temp, status = string.match(rawData_360, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
360-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 360, Harorat: 45.0 C, Status: OK
```


# 361-Topshiriq: Satrlar va pattern matching muhandisligi #361
## Topshiriq sharti:
361-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_361 = "SENSOR_ID:361;TEMP:45.1;STATUS:OK"
local id, temp, status = string.match(rawData_361, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
361-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 361, Harorat: 45.1 C, Status: OK
```


# 362-Topshiriq: Satrlar va pattern matching muhandisligi #362
## Topshiriq sharti:
362-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_362 = "SENSOR_ID:362;TEMP:45.2;STATUS:OK"
local id, temp, status = string.match(rawData_362, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
362-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 362, Harorat: 45.2 C, Status: OK
```


# 363-Topshiriq: Satrlar va pattern matching muhandisligi #363
## Topshiriq sharti:
363-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_363 = "SENSOR_ID:363;TEMP:45.3;STATUS:OK"
local id, temp, status = string.match(rawData_363, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
363-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 363, Harorat: 45.3 C, Status: OK
```


# 364-Topshiriq: Satrlar va pattern matching muhandisligi #364
## Topshiriq sharti:
364-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_364 = "SENSOR_ID:364;TEMP:45.4;STATUS:OK"
local id, temp, status = string.match(rawData_364, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
364-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 364, Harorat: 45.4 C, Status: OK
```


# 365-Topshiriq: Satrlar va pattern matching muhandisligi #365
## Topshiriq sharti:
365-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_365 = "SENSOR_ID:365;TEMP:45.5;STATUS:OK"
local id, temp, status = string.match(rawData_365, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
365-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 365, Harorat: 45.5 C, Status: OK
```


# 366-Topshiriq: Satrlar va pattern matching muhandisligi #366
## Topshiriq sharti:
366-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_366 = "SENSOR_ID:366;TEMP:45.6;STATUS:OK"
local id, temp, status = string.match(rawData_366, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
366-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 366, Harorat: 45.6 C, Status: OK
```


# 367-Topshiriq: Satrlar va pattern matching muhandisligi #367
## Topshiriq sharti:
367-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_367 = "SENSOR_ID:367;TEMP:45.7;STATUS:OK"
local id, temp, status = string.match(rawData_367, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
367-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 367, Harorat: 45.7 C, Status: OK
```


# 368-Topshiriq: Satrlar va pattern matching muhandisligi #368
## Topshiriq sharti:
368-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_368 = "SENSOR_ID:368;TEMP:45.8;STATUS:OK"
local id, temp, status = string.match(rawData_368, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
368-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 368, Harorat: 45.8 C, Status: OK
```


# 369-Topshiriq: Satrlar va pattern matching muhandisligi #369
## Topshiriq sharti:
369-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_369 = "SENSOR_ID:369;TEMP:45.9;STATUS:OK"
local id, temp, status = string.match(rawData_369, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
369-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 369, Harorat: 45.9 C, Status: OK
```


# 370-Topshiriq: Satrlar va pattern matching muhandisligi #370
## Topshiriq sharti:
370-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_370 = "SENSOR_ID:370;TEMP:45.0;STATUS:OK"
local id, temp, status = string.match(rawData_370, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
370-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 370, Harorat: 45.0 C, Status: OK
```


# 371-Topshiriq: Satrlar va pattern matching muhandisligi #371
## Topshiriq sharti:
371-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_371 = "SENSOR_ID:371;TEMP:45.1;STATUS:OK"
local id, temp, status = string.match(rawData_371, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
371-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 371, Harorat: 45.1 C, Status: OK
```


# 372-Topshiriq: Satrlar va pattern matching muhandisligi #372
## Topshiriq sharti:
372-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_372 = "SENSOR_ID:372;TEMP:45.2;STATUS:OK"
local id, temp, status = string.match(rawData_372, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
372-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 372, Harorat: 45.2 C, Status: OK
```


# 373-Topshiriq: Satrlar va pattern matching muhandisligi #373
## Topshiriq sharti:
373-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_373 = "SENSOR_ID:373;TEMP:45.3;STATUS:OK"
local id, temp, status = string.match(rawData_373, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
373-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 373, Harorat: 45.3 C, Status: OK
```


# 374-Topshiriq: Satrlar va pattern matching muhandisligi #374
## Topshiriq sharti:
374-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_374 = "SENSOR_ID:374;TEMP:45.4;STATUS:OK"
local id, temp, status = string.match(rawData_374, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
374-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 374, Harorat: 45.4 C, Status: OK
```


# 375-Topshiriq: Satrlar va pattern matching muhandisligi #375
## Topshiriq sharti:
375-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_375 = "SENSOR_ID:375;TEMP:45.5;STATUS:OK"
local id, temp, status = string.match(rawData_375, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
375-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 375, Harorat: 45.5 C, Status: OK
```


# 376-Topshiriq: Satrlar va pattern matching muhandisligi #376
## Topshiriq sharti:
376-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_376 = "SENSOR_ID:376;TEMP:45.6;STATUS:OK"
local id, temp, status = string.match(rawData_376, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
376-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 376, Harorat: 45.6 C, Status: OK
```


# 377-Topshiriq: Satrlar va pattern matching muhandisligi #377
## Topshiriq sharti:
377-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_377 = "SENSOR_ID:377;TEMP:45.7;STATUS:OK"
local id, temp, status = string.match(rawData_377, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
377-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 377, Harorat: 45.7 C, Status: OK
```


# 378-Topshiriq: Satrlar va pattern matching muhandisligi #378
## Topshiriq sharti:
378-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_378 = "SENSOR_ID:378;TEMP:45.8;STATUS:OK"
local id, temp, status = string.match(rawData_378, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
378-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 378, Harorat: 45.8 C, Status: OK
```


# 379-Topshiriq: Satrlar va pattern matching muhandisligi #379
## Topshiriq sharti:
379-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_379 = "SENSOR_ID:379;TEMP:45.9;STATUS:OK"
local id, temp, status = string.match(rawData_379, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
379-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 379, Harorat: 45.9 C, Status: OK
```


# 380-Topshiriq: Satrlar va pattern matching muhandisligi #380
## Topshiriq sharti:
380-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_380 = "SENSOR_ID:380;TEMP:45.0;STATUS:OK"
local id, temp, status = string.match(rawData_380, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
380-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 380, Harorat: 45.0 C, Status: OK
```


# 381-Topshiriq: Satrlar va pattern matching muhandisligi #381
## Topshiriq sharti:
381-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_381 = "SENSOR_ID:381;TEMP:45.1;STATUS:OK"
local id, temp, status = string.match(rawData_381, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
381-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 381, Harorat: 45.1 C, Status: OK
```


# 382-Topshiriq: Satrlar va pattern matching muhandisligi #382
## Topshiriq sharti:
382-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_382 = "SENSOR_ID:382;TEMP:45.2;STATUS:OK"
local id, temp, status = string.match(rawData_382, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
382-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 382, Harorat: 45.2 C, Status: OK
```


# 383-Topshiriq: Satrlar va pattern matching muhandisligi #383
## Topshiriq sharti:
383-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_383 = "SENSOR_ID:383;TEMP:45.3;STATUS:OK"
local id, temp, status = string.match(rawData_383, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
383-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 383, Harorat: 45.3 C, Status: OK
```


# 384-Topshiriq: Satrlar va pattern matching muhandisligi #384
## Topshiriq sharti:
384-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_384 = "SENSOR_ID:384;TEMP:45.4;STATUS:OK"
local id, temp, status = string.match(rawData_384, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
384-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 384, Harorat: 45.4 C, Status: OK
```


# 385-Topshiriq: Satrlar va pattern matching muhandisligi #385
## Topshiriq sharti:
385-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_385 = "SENSOR_ID:385;TEMP:45.5;STATUS:OK"
local id, temp, status = string.match(rawData_385, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
385-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 385, Harorat: 45.5 C, Status: OK
```


# 386-Topshiriq: Satrlar va pattern matching muhandisligi #386
## Topshiriq sharti:
386-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_386 = "SENSOR_ID:386;TEMP:45.6;STATUS:OK"
local id, temp, status = string.match(rawData_386, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
386-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 386, Harorat: 45.6 C, Status: OK
```


# 387-Topshiriq: Satrlar va pattern matching muhandisligi #387
## Topshiriq sharti:
387-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_387 = "SENSOR_ID:387;TEMP:45.7;STATUS:OK"
local id, temp, status = string.match(rawData_387, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
387-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 387, Harorat: 45.7 C, Status: OK
```


# 388-Topshiriq: Satrlar va pattern matching muhandisligi #388
## Topshiriq sharti:
388-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_388 = "SENSOR_ID:388;TEMP:45.8;STATUS:OK"
local id, temp, status = string.match(rawData_388, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
388-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 388, Harorat: 45.8 C, Status: OK
```


# 389-Topshiriq: Satrlar va pattern matching muhandisligi #389
## Topshiriq sharti:
389-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_389 = "SENSOR_ID:389;TEMP:45.9;STATUS:OK"
local id, temp, status = string.match(rawData_389, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
389-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 389, Harorat: 45.9 C, Status: OK
```


# 390-Topshiriq: Satrlar va pattern matching muhandisligi #390
## Topshiriq sharti:
390-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_390 = "SENSOR_ID:390;TEMP:45.0;STATUS:OK"
local id, temp, status = string.match(rawData_390, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
390-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 390, Harorat: 45.0 C, Status: OK
```


# 391-Topshiriq: Satrlar va pattern matching muhandisligi #391
## Topshiriq sharti:
391-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_391 = "SENSOR_ID:391;TEMP:45.1;STATUS:OK"
local id, temp, status = string.match(rawData_391, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
391-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 391, Harorat: 45.1 C, Status: OK
```


# 392-Topshiriq: Satrlar va pattern matching muhandisligi #392
## Topshiriq sharti:
392-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_392 = "SENSOR_ID:392;TEMP:45.2;STATUS:OK"
local id, temp, status = string.match(rawData_392, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
392-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 392, Harorat: 45.2 C, Status: OK
```


# 393-Topshiriq: Satrlar va pattern matching muhandisligi #393
## Topshiriq sharti:
393-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_393 = "SENSOR_ID:393;TEMP:45.3;STATUS:OK"
local id, temp, status = string.match(rawData_393, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
393-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 393, Harorat: 45.3 C, Status: OK
```


# 394-Topshiriq: Satrlar va pattern matching muhandisligi #394
## Topshiriq sharti:
394-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_394 = "SENSOR_ID:394;TEMP:45.4;STATUS:OK"
local id, temp, status = string.match(rawData_394, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
394-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 394, Harorat: 45.4 C, Status: OK
```


# 395-Topshiriq: Satrlar va pattern matching muhandisligi #395
## Topshiriq sharti:
395-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_395 = "SENSOR_ID:395;TEMP:45.5;STATUS:OK"
local id, temp, status = string.match(rawData_395, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
395-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 395, Harorat: 45.5 C, Status: OK
```


# 396-Topshiriq: Satrlar va pattern matching muhandisligi #396
## Topshiriq sharti:
396-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_396 = "SENSOR_ID:396;TEMP:45.6;STATUS:OK"
local id, temp, status = string.match(rawData_396, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
396-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 396, Harorat: 45.6 C, Status: OK
```


# 397-Topshiriq: Satrlar va pattern matching muhandisligi #397
## Topshiriq sharti:
397-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_397 = "SENSOR_ID:397;TEMP:45.7;STATUS:OK"
local id, temp, status = string.match(rawData_397, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
397-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 397, Harorat: 45.7 C, Status: OK
```


# 398-Topshiriq: Satrlar va pattern matching muhandisligi #398
## Topshiriq sharti:
398-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_398 = "SENSOR_ID:398;TEMP:45.8;STATUS:OK"
local id, temp, status = string.match(rawData_398, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
398-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 398, Harorat: 45.8 C, Status: OK
```


# 399-Topshiriq: Satrlar va pattern matching muhandisligi #399
## Topshiriq sharti:
399-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_399 = "SENSOR_ID:399;TEMP:45.9;STATUS:OK"
local id, temp, status = string.match(rawData_399, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
399-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 399, Harorat: 45.9 C, Status: OK
```


# 400-Topshiriq: Satrlar va pattern matching muhandisligi #400
## Topshiriq sharti:
400-vazifa: Murakkab matn tahlili, captures, string.gmatch va qidiruv-almashtirish amaliyoti.

## Yechim (Lua kodi):
```lua
local rawData_400 = "SENSOR_ID:400;TEMP:45.0;STATUS:OK"
local id, temp, status = string.match(rawData_400, "SENSOR_ID:(%d+);TEMP:([%d%.]+);STATUS:(%a+)")

print(string.format("Sensor: %s, Harorat: %s C, Status: %s", id, temp, status))
```

## Tushuntirish va Mantiq:
400-topshiriqda captures `(%d+)` va andozalar yordamida strukturalanmagan matndan parametrlar ajratildi.

## Ishlash natijasi:
```text
Sensor: 400, Harorat: 45.0 C, Status: OK
```

