# 401-Topshiriq: coroutine.create va coroutine.resume asoslari
## Topshiriq sharti:
Oddiy korutina yaratib uning ishlashini va boshqaruvini namoyish qiling.

## Yechim (Lua kodi):
```lua
local co = coroutine.create(function()
    print("Korutina boshlandi!")
    coroutine.yield()
    print("Korutina qayta tiklandi!")
end)

print("Holat (boshida): " .. coroutine.status(co))
coroutine.resume(co)
print("Holat (yield dan keyin): " .. coroutine.status(co))
coroutine.resume(co)
print("Holat (tugagach): " .. coroutine.status(co))
```

## Tushuntirish va Mantiq:
Korutina `coroutine.create` bilan yaratilganda 'suspended' holatda bo'ladi. `coroutine.resume` uni ishga tushiradi, `coroutine.yield` esa to'xtatib turadi.

## Ishlash natijasi:
```text
Holat (boshida): suspended
Korutina boshlandi!
Holat (yield dan keyin): suspended
Korutina qayta tiklandi!
Holat (tugagach): dead
```


# 402-Topshiriq: yield orqali qiymat uzatish va qabul qilish
## Topshiriq sharti:
Korutinadan asosiy oqimga ma'lumotlar qaytarish mexanizmini ko'rsating.

## Yechim (Lua kodi):
```lua
local co = coroutine.create(function(startVal)
    print("Korutinaga kirdi: " .. startVal)
    local nextVal = coroutine.yield("BIRINCHI_NATIJA")
    print("Ikkinchi qabul: " .. nextVal)
    return "YAKUNIY_JAVOB"
end)

local ok1, res1 = coroutine.resume(co, 100)
print("Asosiy oqim oldi: " .. res1)

local ok2, res2 = coroutine.resume(co, 200)
print("Asosiy oqim oldi: " .. res2)
```

## Tushuntirish va Mantiq:
`coroutine.yield(...)` ga berilgan parametrlar `coroutine.resume` ning qaytaruvchi qiymatlari bo'ladi va aksincha.

## Ishlash natijasi:
```text
Korutinaga kirdi: 100
Asosiy oqim oldi: BIRINCHI_NATIJA
Ikkinchi qabul: 200
Asosiy oqim oldi: YAKUNIY_JAVOB
```


# 403-Topshiriq: coroutine.wrap yordamida qulay generator yasash
## Topshiriq sharti:
Fibonachchi sonlarini cheksiz generatsiya qiluvchi iterator yozing.

## Yechim (Lua kodi):
```lua
local function fibGenerator()
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
```

## Tushuntirish va Mantiq:
`coroutine.wrap` oddiy funksiya qaytaradi, uni har gal chaqirganda ichki korutinaning keyingi `yield` qiymati qaytadi.

## Ishlash natijasi:
```text
Fib #1: 0
Fib #2: 1
Fib #3: 1
Fib #4: 2
Fib #5: 3
Fib #6: 5
```


# 404-Topshiriq: Producer-Consumer andozasi korutinalar bilan
## Topshiriq sharti:
Ishlab chiqaruvchi (Producer) va Iste'molchi (Consumer) o'rtasidagi ma'lumot almashinuvini modellashtiring.

## Yechim (Lua kodi):
```lua
local function producer()
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
```

## Tushuntirish va Mantiq:
Kooperativ ko'p vazifalilikda producer ma'lumot tayyorlab yield qiladi, consumer esa uni o'qib ishlaydi.

## Ishlash natijasi:
```text
Producer mahsulot yaratdi: #1
Consumer mahsulotni qabul qildi: Paket_1
Producer mahsulot yaratdi: #2
Consumer mahsulotni qabul qildi: Paket_2
Producer mahsulot yaratdi: #3
Consumer mahsulotni qabul qildi: Paket_3
```


# 405-Topshiriq: Kooperativ Task Scheduler (Vazifalar boshqaruvchisi)
## Topshiriq sharti:
Bir nechta mustaqil korutinalarni navbatma-navbat bajaruvchi oddiy rejalashtiruvchi yozing.

## Yechim (Lua kodi):
```lua
local tasks = {
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
```

## Tushuntirish va Mantiq:
Round-robin kooperativ rejalashtiruvchi hech qanday OS qulflarisiz engil vazifalar almashinuvini ta'minlaydi.

## Ishlash natijasi:
```text
[Vazifa A] Ishlamoqda 1
[Vazifa B] Ishlamoqda 1
[Vazifa A] Ishlamoqda 2
[Vazifa B] Ishlamoqda 2
Barcha vazifalar yakunlandi!
```


# 406-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #406
## Topshiriq sharti:
406-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_406 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 406, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_406, 1)
print(msg1)
local _, msg2 = coroutine.resume(co_406)
print(msg2)
```

## Tushuntirish va Mantiq:
406-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #406 Qadam 1: 1
Korutina #406 Qadam 2: 2
```


# 407-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #407
## Topshiriq sharti:
407-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_407 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 407, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_407, 2)
print(msg1)
local _, msg2 = coroutine.resume(co_407)
print(msg2)
```

## Tushuntirish va Mantiq:
407-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #407 Qadam 1: 2
Korutina #407 Qadam 2: 4
```


# 408-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #408
## Topshiriq sharti:
408-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_408 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 408, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_408, 3)
print(msg1)
local _, msg2 = coroutine.resume(co_408)
print(msg2)
```

## Tushuntirish va Mantiq:
408-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #408 Qadam 1: 3
Korutina #408 Qadam 2: 6
```


# 409-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #409
## Topshiriq sharti:
409-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_409 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 409, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_409, 4)
print(msg1)
local _, msg2 = coroutine.resume(co_409)
print(msg2)
```

## Tushuntirish va Mantiq:
409-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #409 Qadam 1: 4
Korutina #409 Qadam 2: 8
```


# 410-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #410
## Topshiriq sharti:
410-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_410 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 410, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_410, 5)
print(msg1)
local _, msg2 = coroutine.resume(co_410)
print(msg2)
```

## Tushuntirish va Mantiq:
410-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #410 Qadam 1: 5
Korutina #410 Qadam 2: 10
```


# 411-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #411
## Topshiriq sharti:
411-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_411 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 411, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_411, 6)
print(msg1)
local _, msg2 = coroutine.resume(co_411)
print(msg2)
```

## Tushuntirish va Mantiq:
411-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #411 Qadam 1: 6
Korutina #411 Qadam 2: 12
```


# 412-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #412
## Topshiriq sharti:
412-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_412 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 412, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_412, 7)
print(msg1)
local _, msg2 = coroutine.resume(co_412)
print(msg2)
```

## Tushuntirish va Mantiq:
412-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #412 Qadam 1: 7
Korutina #412 Qadam 2: 14
```


# 413-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #413
## Topshiriq sharti:
413-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_413 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 413, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_413, 1)
print(msg1)
local _, msg2 = coroutine.resume(co_413)
print(msg2)
```

## Tushuntirish va Mantiq:
413-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #413 Qadam 1: 1
Korutina #413 Qadam 2: 2
```


# 414-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #414
## Topshiriq sharti:
414-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_414 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 414, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_414, 2)
print(msg1)
local _, msg2 = coroutine.resume(co_414)
print(msg2)
```

## Tushuntirish va Mantiq:
414-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #414 Qadam 1: 2
Korutina #414 Qadam 2: 4
```


# 415-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #415
## Topshiriq sharti:
415-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_415 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 415, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_415, 3)
print(msg1)
local _, msg2 = coroutine.resume(co_415)
print(msg2)
```

## Tushuntirish va Mantiq:
415-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #415 Qadam 1: 3
Korutina #415 Qadam 2: 6
```


# 416-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #416
## Topshiriq sharti:
416-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_416 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 416, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_416, 4)
print(msg1)
local _, msg2 = coroutine.resume(co_416)
print(msg2)
```

## Tushuntirish va Mantiq:
416-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #416 Qadam 1: 4
Korutina #416 Qadam 2: 8
```


# 417-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #417
## Topshiriq sharti:
417-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_417 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 417, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_417, 5)
print(msg1)
local _, msg2 = coroutine.resume(co_417)
print(msg2)
```

## Tushuntirish va Mantiq:
417-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #417 Qadam 1: 5
Korutina #417 Qadam 2: 10
```


# 418-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #418
## Topshiriq sharti:
418-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_418 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 418, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_418, 6)
print(msg1)
local _, msg2 = coroutine.resume(co_418)
print(msg2)
```

## Tushuntirish va Mantiq:
418-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #418 Qadam 1: 6
Korutina #418 Qadam 2: 12
```


# 419-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #419
## Topshiriq sharti:
419-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_419 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 419, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_419, 7)
print(msg1)
local _, msg2 = coroutine.resume(co_419)
print(msg2)
```

## Tushuntirish va Mantiq:
419-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #419 Qadam 1: 7
Korutina #419 Qadam 2: 14
```


# 420-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #420
## Topshiriq sharti:
420-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_420 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 420, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_420, 1)
print(msg1)
local _, msg2 = coroutine.resume(co_420)
print(msg2)
```

## Tushuntirish va Mantiq:
420-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #420 Qadam 1: 1
Korutina #420 Qadam 2: 2
```


# 421-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #421
## Topshiriq sharti:
421-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_421 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 421, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_421, 2)
print(msg1)
local _, msg2 = coroutine.resume(co_421)
print(msg2)
```

## Tushuntirish va Mantiq:
421-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #421 Qadam 1: 2
Korutina #421 Qadam 2: 4
```


# 422-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #422
## Topshiriq sharti:
422-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_422 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 422, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_422, 3)
print(msg1)
local _, msg2 = coroutine.resume(co_422)
print(msg2)
```

## Tushuntirish va Mantiq:
422-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #422 Qadam 1: 3
Korutina #422 Qadam 2: 6
```


# 423-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #423
## Topshiriq sharti:
423-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_423 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 423, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_423, 4)
print(msg1)
local _, msg2 = coroutine.resume(co_423)
print(msg2)
```

## Tushuntirish va Mantiq:
423-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #423 Qadam 1: 4
Korutina #423 Qadam 2: 8
```


# 424-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #424
## Topshiriq sharti:
424-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_424 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 424, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_424, 5)
print(msg1)
local _, msg2 = coroutine.resume(co_424)
print(msg2)
```

## Tushuntirish va Mantiq:
424-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #424 Qadam 1: 5
Korutina #424 Qadam 2: 10
```


# 425-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #425
## Topshiriq sharti:
425-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_425 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 425, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_425, 6)
print(msg1)
local _, msg2 = coroutine.resume(co_425)
print(msg2)
```

## Tushuntirish va Mantiq:
425-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #425 Qadam 1: 6
Korutina #425 Qadam 2: 12
```


# 426-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #426
## Topshiriq sharti:
426-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_426 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 426, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_426, 7)
print(msg1)
local _, msg2 = coroutine.resume(co_426)
print(msg2)
```

## Tushuntirish va Mantiq:
426-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #426 Qadam 1: 7
Korutina #426 Qadam 2: 14
```


# 427-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #427
## Topshiriq sharti:
427-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_427 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 427, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_427, 1)
print(msg1)
local _, msg2 = coroutine.resume(co_427)
print(msg2)
```

## Tushuntirish va Mantiq:
427-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #427 Qadam 1: 1
Korutina #427 Qadam 2: 2
```


# 428-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #428
## Topshiriq sharti:
428-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_428 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 428, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_428, 2)
print(msg1)
local _, msg2 = coroutine.resume(co_428)
print(msg2)
```

## Tushuntirish va Mantiq:
428-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #428 Qadam 1: 2
Korutina #428 Qadam 2: 4
```


# 429-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #429
## Topshiriq sharti:
429-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_429 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 429, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_429, 3)
print(msg1)
local _, msg2 = coroutine.resume(co_429)
print(msg2)
```

## Tushuntirish va Mantiq:
429-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #429 Qadam 1: 3
Korutina #429 Qadam 2: 6
```


# 430-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #430
## Topshiriq sharti:
430-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_430 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 430, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_430, 4)
print(msg1)
local _, msg2 = coroutine.resume(co_430)
print(msg2)
```

## Tushuntirish va Mantiq:
430-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #430 Qadam 1: 4
Korutina #430 Qadam 2: 8
```


# 431-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #431
## Topshiriq sharti:
431-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_431 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 431, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_431, 5)
print(msg1)
local _, msg2 = coroutine.resume(co_431)
print(msg2)
```

## Tushuntirish va Mantiq:
431-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #431 Qadam 1: 5
Korutina #431 Qadam 2: 10
```


# 432-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #432
## Topshiriq sharti:
432-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_432 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 432, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_432, 6)
print(msg1)
local _, msg2 = coroutine.resume(co_432)
print(msg2)
```

## Tushuntirish va Mantiq:
432-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #432 Qadam 1: 6
Korutina #432 Qadam 2: 12
```


# 433-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #433
## Topshiriq sharti:
433-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_433 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 433, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_433, 7)
print(msg1)
local _, msg2 = coroutine.resume(co_433)
print(msg2)
```

## Tushuntirish va Mantiq:
433-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #433 Qadam 1: 7
Korutina #433 Qadam 2: 14
```


# 434-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #434
## Topshiriq sharti:
434-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_434 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 434, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_434, 1)
print(msg1)
local _, msg2 = coroutine.resume(co_434)
print(msg2)
```

## Tushuntirish va Mantiq:
434-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #434 Qadam 1: 1
Korutina #434 Qadam 2: 2
```


# 435-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #435
## Topshiriq sharti:
435-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_435 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 435, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_435, 2)
print(msg1)
local _, msg2 = coroutine.resume(co_435)
print(msg2)
```

## Tushuntirish va Mantiq:
435-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #435 Qadam 1: 2
Korutina #435 Qadam 2: 4
```


# 436-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #436
## Topshiriq sharti:
436-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_436 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 436, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_436, 3)
print(msg1)
local _, msg2 = coroutine.resume(co_436)
print(msg2)
```

## Tushuntirish va Mantiq:
436-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #436 Qadam 1: 3
Korutina #436 Qadam 2: 6
```


# 437-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #437
## Topshiriq sharti:
437-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_437 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 437, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_437, 4)
print(msg1)
local _, msg2 = coroutine.resume(co_437)
print(msg2)
```

## Tushuntirish va Mantiq:
437-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #437 Qadam 1: 4
Korutina #437 Qadam 2: 8
```


# 438-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #438
## Topshiriq sharti:
438-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_438 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 438, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_438, 5)
print(msg1)
local _, msg2 = coroutine.resume(co_438)
print(msg2)
```

## Tushuntirish va Mantiq:
438-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #438 Qadam 1: 5
Korutina #438 Qadam 2: 10
```


# 439-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #439
## Topshiriq sharti:
439-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_439 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 439, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_439, 6)
print(msg1)
local _, msg2 = coroutine.resume(co_439)
print(msg2)
```

## Tushuntirish va Mantiq:
439-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #439 Qadam 1: 6
Korutina #439 Qadam 2: 12
```


# 440-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #440
## Topshiriq sharti:
440-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_440 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 440, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_440, 7)
print(msg1)
local _, msg2 = coroutine.resume(co_440)
print(msg2)
```

## Tushuntirish va Mantiq:
440-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #440 Qadam 1: 7
Korutina #440 Qadam 2: 14
```


# 441-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #441
## Topshiriq sharti:
441-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_441 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 441, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_441, 1)
print(msg1)
local _, msg2 = coroutine.resume(co_441)
print(msg2)
```

## Tushuntirish va Mantiq:
441-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #441 Qadam 1: 1
Korutina #441 Qadam 2: 2
```


# 442-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #442
## Topshiriq sharti:
442-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_442 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 442, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_442, 2)
print(msg1)
local _, msg2 = coroutine.resume(co_442)
print(msg2)
```

## Tushuntirish va Mantiq:
442-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #442 Qadam 1: 2
Korutina #442 Qadam 2: 4
```


# 443-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #443
## Topshiriq sharti:
443-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_443 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 443, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_443, 3)
print(msg1)
local _, msg2 = coroutine.resume(co_443)
print(msg2)
```

## Tushuntirish va Mantiq:
443-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #443 Qadam 1: 3
Korutina #443 Qadam 2: 6
```


# 444-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #444
## Topshiriq sharti:
444-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_444 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 444, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_444, 4)
print(msg1)
local _, msg2 = coroutine.resume(co_444)
print(msg2)
```

## Tushuntirish va Mantiq:
444-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #444 Qadam 1: 4
Korutina #444 Qadam 2: 8
```


# 445-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #445
## Topshiriq sharti:
445-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_445 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 445, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_445, 5)
print(msg1)
local _, msg2 = coroutine.resume(co_445)
print(msg2)
```

## Tushuntirish va Mantiq:
445-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #445 Qadam 1: 5
Korutina #445 Qadam 2: 10
```


# 446-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #446
## Topshiriq sharti:
446-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_446 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 446, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_446, 6)
print(msg1)
local _, msg2 = coroutine.resume(co_446)
print(msg2)
```

## Tushuntirish va Mantiq:
446-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #446 Qadam 1: 6
Korutina #446 Qadam 2: 12
```


# 447-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #447
## Topshiriq sharti:
447-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_447 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 447, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_447, 7)
print(msg1)
local _, msg2 = coroutine.resume(co_447)
print(msg2)
```

## Tushuntirish va Mantiq:
447-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #447 Qadam 1: 7
Korutina #447 Qadam 2: 14
```


# 448-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #448
## Topshiriq sharti:
448-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_448 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 448, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_448, 1)
print(msg1)
local _, msg2 = coroutine.resume(co_448)
print(msg2)
```

## Tushuntirish va Mantiq:
448-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #448 Qadam 1: 1
Korutina #448 Qadam 2: 2
```


# 449-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #449
## Topshiriq sharti:
449-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_449 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 449, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_449, 2)
print(msg1)
local _, msg2 = coroutine.resume(co_449)
print(msg2)
```

## Tushuntirish va Mantiq:
449-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #449 Qadam 1: 2
Korutina #449 Qadam 2: 4
```


# 450-Topshiriq: Korutinalar va asinxron boshqaruv amaliyoti #450
## Topshiriq sharti:
450-vazifa: Kooperativ korutinalar, holatni saqlash va ko'p bosqichli iteratsiya jarayoni.

## Yechim (Lua kodi):
```lua
local co_450 = coroutine.create(function(base)
    for step = 1, 2 do
        coroutine.yield(string.format("Korutina #%d Qadam %d: %d", 450, step, base * step))
    end
    return "TUGADI"
end)

local _, msg1 = coroutine.resume(co_450, 3)
print(msg1)
local _, msg2 = coroutine.resume(co_450)
print(msg2)
```

## Tushuntirish va Mantiq:
450-vazifada kooperativ yield va resume orqali to'xtatib turiluvchi hisoblashlar namoyish qilindi.

## Ishlash natijasi:
```text
Korutina #450 Qadam 1: 3
Korutina #450 Qadam 2: 6
```

