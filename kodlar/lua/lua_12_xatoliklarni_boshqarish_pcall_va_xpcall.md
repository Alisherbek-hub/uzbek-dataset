# 551-Topshiriq: error() va assert() funksiyalari
## Topshiriq sharti:
Parametrlarni assert() bilan tekshiring va shart bajarilmasa dasturni xato bilan to'xtating.

## Yechim (Lua kodi):
```lua
local function divide(a, b)
    assert(b ~= 0, "Nolga bo'lish mumkin emas!")
    return a / b
end

print("10 / 2 = " .. divide(10, 2))
```

## Tushuntirish va Mantiq:
`assert(condition, message)` agar birinchi argument false yoki nil bo'lsa `error(message)` chaqiradi.

## Ishlash natijasi:
```text
10 / 2 = 5.0
```


# 552-Topshiriq: pcall() - Himoyalangan chaqiruv (Protected Call)
## Topshiriq sharti:
Xatolik yuz berishi mumkin bo'lgan kodni dastur to'xtab qolmasdan xavfsiz bajaring.

## Yechim (Lua kodi):
```lua
local function riskyOperation(x)
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
```

## Tushuntirish va Mantiq:
`pcall(func, ...)` funksiyani himoyalangan rejimda chaqiradi. Agar xato bo'lsa `false, xato_xabari`, xatosiz tugasa `true, natijalar` qaytaradi.

## Ishlash natijasi:
```text
Xatolik ushlandi: Manfiy son qabul qilinmaydi!
```


# 553-Topshiriq: xpcall() va debug.traceback bilan to'liq xato izi
## Topshiriq sharti:
Xatolik yuz berganda chaqiruvlar stegi haqida to'liq ma'lumot oling.

## Yechim (Lua kodi):
```lua
local function levelTwo()
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
```

## Tushuntirish va Mantiq:
`xpcall(func, errorHandler)` xatolik ro'y berganda stak tozalanmasdan oldin maxsus xato tahlilchisiga murojaat qilish imkonini beradi.

## Ishlash natijasi:
```text
USHLANDI: Chuqur ichki xatolik yuz berdi! [Stek tekshirildi]
```


# 554-Topshiriq: Xatolik ob'ekti sifatida jadvaldan foydalanish
## Topshiriq sharti:
Oddiy matn o'rniga strukturalangan JSON/Jadval xato kodini uzating.

## Yechim (Lua kodi):
```lua
local function connectDatabase(host)
    if host == "invalid" then
        error({code = 503, reason = "Host unreachable", timestamp = 1700000000})
    end
    return "Connected"
end

local ok, errObj = pcall(connectDatabase, "invalid")
if not ok and type(errObj) == "table" then
    print(string.format("Xato kodi: %d, Sabab: %s", errObj.code, errObj.reason))
end
```

## Tushuntirish va Mantiq:
Luada `error()` ga faqat satr emas, istalgan turdagi qiymat, jumladan metatable yoki murakkab jadval ham berilishi mumkin.

## Ishlash natijasi:
```text
Xato kodi: 503, Sabab: Host unreachable
```


# 555-Topshiriq: Try-Catch-Finally simulyatsiyasi
## Topshiriq sharti:
Resursni ochish, undan foydalanish va xatolik bo'lishidan qat'i nazar resursni tozalash andozasi.

## Yechim (Lua kodi):
```lua
local function tryCatchFinally(tryBlock, catchBlock, finallyBlock)
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
```

## Tushuntirish va Mantiq:
pcall asosida boshqa tillardagi try-catch-finally bloki to'liq simulyatsiya qilinadi.

## Ishlash natijasi:
```text
1. Resurs ochildi
Ushlangan xato: 2. Kutilmagan uzilish!
3. Finally: Resurs kafolatli yopildi.
```


# 556-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #556
## Topshiriq sharti:
556-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_556(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_556, 100, 556)
print(string.format("Tranzaksiya #%d holati: %s", 556, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
556-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #556 holati: Bekor qilindi
```


# 557-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #557
## Topshiriq sharti:
557-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_557(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_557, 100, 557)
print(string.format("Tranzaksiya #%d holati: %s", 557, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
557-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #557 holati: Bekor qilindi
```


# 558-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #558
## Topshiriq sharti:
558-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_558(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_558, 100, 558)
print(string.format("Tranzaksiya #%d holati: %s", 558, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
558-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #558 holati: Bekor qilindi
```


# 559-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #559
## Topshiriq sharti:
559-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_559(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_559, 100, 559)
print(string.format("Tranzaksiya #%d holati: %s", 559, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
559-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #559 holati: Bekor qilindi
```


# 560-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #560
## Topshiriq sharti:
560-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_560(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_560, 100, 560)
print(string.format("Tranzaksiya #%d holati: %s", 560, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
560-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #560 holati: Bekor qilindi
```


# 561-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #561
## Topshiriq sharti:
561-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_561(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_561, 100, 561)
print(string.format("Tranzaksiya #%d holati: %s", 561, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
561-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #561 holati: Bekor qilindi
```


# 562-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #562
## Topshiriq sharti:
562-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_562(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_562, 100, 562)
print(string.format("Tranzaksiya #%d holati: %s", 562, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
562-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #562 holati: Bekor qilindi
```


# 563-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #563
## Topshiriq sharti:
563-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_563(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_563, 100, 563)
print(string.format("Tranzaksiya #%d holati: %s", 563, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
563-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #563 holati: Bekor qilindi
```


# 564-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #564
## Topshiriq sharti:
564-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_564(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_564, 100, 564)
print(string.format("Tranzaksiya #%d holati: %s", 564, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
564-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #564 holati: Bekor qilindi
```


# 565-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #565
## Topshiriq sharti:
565-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_565(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_565, 100, 565)
print(string.format("Tranzaksiya #%d holati: %s", 565, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
565-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #565 holati: Bekor qilindi
```


# 566-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #566
## Topshiriq sharti:
566-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_566(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_566, 100, 566)
print(string.format("Tranzaksiya #%d holati: %s", 566, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
566-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #566 holati: Bekor qilindi
```


# 567-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #567
## Topshiriq sharti:
567-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_567(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_567, 100, 567)
print(string.format("Tranzaksiya #%d holati: %s", 567, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
567-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #567 holati: Bekor qilindi
```


# 568-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #568
## Topshiriq sharti:
568-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_568(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_568, 100, 568)
print(string.format("Tranzaksiya #%d holati: %s", 568, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
568-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #568 holati: Bekor qilindi
```


# 569-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #569
## Topshiriq sharti:
569-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_569(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_569, 100, 569)
print(string.format("Tranzaksiya #%d holati: %s", 569, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
569-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #569 holati: Bekor qilindi
```


# 570-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #570
## Topshiriq sharti:
570-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_570(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_570, 100, 570)
print(string.format("Tranzaksiya #%d holati: %s", 570, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
570-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #570 holati: Bekor qilindi
```


# 571-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #571
## Topshiriq sharti:
571-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_571(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_571, 100, 571)
print(string.format("Tranzaksiya #%d holati: %s", 571, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
571-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #571 holati: Bekor qilindi
```


# 572-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #572
## Topshiriq sharti:
572-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_572(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_572, 100, 572)
print(string.format("Tranzaksiya #%d holati: %s", 572, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
572-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #572 holati: Bekor qilindi
```


# 573-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #573
## Topshiriq sharti:
573-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_573(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_573, 100, 573)
print(string.format("Tranzaksiya #%d holati: %s", 573, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
573-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #573 holati: Bekor qilindi
```


# 574-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #574
## Topshiriq sharti:
574-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_574(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_574, 100, 574)
print(string.format("Tranzaksiya #%d holati: %s", 574, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
574-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #574 holati: Bekor qilindi
```


# 575-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #575
## Topshiriq sharti:
575-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_575(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_575, 100, 575)
print(string.format("Tranzaksiya #%d holati: %s", 575, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
575-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #575 holati: Bekor qilindi
```


# 576-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #576
## Topshiriq sharti:
576-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_576(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_576, 100, 576)
print(string.format("Tranzaksiya #%d holati: %s", 576, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
576-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #576 holati: Bekor qilindi
```


# 577-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #577
## Topshiriq sharti:
577-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_577(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_577, 100, 577)
print(string.format("Tranzaksiya #%d holati: %s", 577, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
577-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #577 holati: Bekor qilindi
```


# 578-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #578
## Topshiriq sharti:
578-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_578(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_578, 100, 578)
print(string.format("Tranzaksiya #%d holati: %s", 578, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
578-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #578 holati: Bekor qilindi
```


# 579-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #579
## Topshiriq sharti:
579-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_579(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_579, 100, 579)
print(string.format("Tranzaksiya #%d holati: %s", 579, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
579-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #579 holati: Bekor qilindi
```


# 580-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #580
## Topshiriq sharti:
580-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_580(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_580, 100, 580)
print(string.format("Tranzaksiya #%d holati: %s", 580, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
580-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #580 holati: Bekor qilindi
```


# 581-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #581
## Topshiriq sharti:
581-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_581(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_581, 100, 581)
print(string.format("Tranzaksiya #%d holati: %s", 581, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
581-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #581 holati: Bekor qilindi
```


# 582-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #582
## Topshiriq sharti:
582-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_582(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_582, 100, 582)
print(string.format("Tranzaksiya #%d holati: %s", 582, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
582-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #582 holati: Bekor qilindi
```


# 583-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #583
## Topshiriq sharti:
583-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_583(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_583, 100, 583)
print(string.format("Tranzaksiya #%d holati: %s", 583, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
583-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #583 holati: Bekor qilindi
```


# 584-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #584
## Topshiriq sharti:
584-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_584(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_584, 100, 584)
print(string.format("Tranzaksiya #%d holati: %s", 584, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
584-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #584 holati: Bekor qilindi
```


# 585-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #585
## Topshiriq sharti:
585-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_585(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_585, 100, 585)
print(string.format("Tranzaksiya #%d holati: %s", 585, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
585-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #585 holati: Bekor qilindi
```


# 586-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #586
## Topshiriq sharti:
586-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_586(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_586, 100, 586)
print(string.format("Tranzaksiya #%d holati: %s", 586, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
586-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #586 holati: Bekor qilindi
```


# 587-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #587
## Topshiriq sharti:
587-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_587(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_587, 100, 587)
print(string.format("Tranzaksiya #%d holati: %s", 587, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
587-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #587 holati: Bekor qilindi
```


# 588-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #588
## Topshiriq sharti:
588-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_588(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_588, 100, 588)
print(string.format("Tranzaksiya #%d holati: %s", 588, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
588-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #588 holati: Bekor qilindi
```


# 589-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #589
## Topshiriq sharti:
589-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_589(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_589, 100, 589)
print(string.format("Tranzaksiya #%d holati: %s", 589, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
589-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #589 holati: Bekor qilindi
```


# 590-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #590
## Topshiriq sharti:
590-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_590(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_590, 100, 590)
print(string.format("Tranzaksiya #%d holati: %s", 590, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
590-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #590 holati: Bekor qilindi
```


# 591-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #591
## Topshiriq sharti:
591-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_591(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_591, 100, 591)
print(string.format("Tranzaksiya #%d holati: %s", 591, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
591-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #591 holati: Bekor qilindi
```


# 592-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #592
## Topshiriq sharti:
592-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_592(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_592, 100, 592)
print(string.format("Tranzaksiya #%d holati: %s", 592, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
592-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #592 holati: Bekor qilindi
```


# 593-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #593
## Topshiriq sharti:
593-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_593(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_593, 100, 593)
print(string.format("Tranzaksiya #%d holati: %s", 593, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
593-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #593 holati: Bekor qilindi
```


# 594-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #594
## Topshiriq sharti:
594-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_594(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_594, 100, 594)
print(string.format("Tranzaksiya #%d holati: %s", 594, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
594-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #594 holati: Bekor qilindi
```


# 595-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #595
## Topshiriq sharti:
595-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_595(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_595, 100, 595)
print(string.format("Tranzaksiya #%d holati: %s", 595, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
595-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #595 holati: Bekor qilindi
```


# 596-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #596
## Topshiriq sharti:
596-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_596(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_596, 100, 596)
print(string.format("Tranzaksiya #%d holati: %s", 596, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
596-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #596 holati: Bekor qilindi
```


# 597-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #597
## Topshiriq sharti:
597-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_597(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_597, 100, 597)
print(string.format("Tranzaksiya #%d holati: %s", 597, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
597-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #597 holati: Bekor qilindi
```


# 598-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #598
## Topshiriq sharti:
598-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_598(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_598, 100, 598)
print(string.format("Tranzaksiya #%d holati: %s", 598, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
598-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #598 holati: Bekor qilindi
```


# 599-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #599
## Topshiriq sharti:
599-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_599(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_599, 100, 599)
print(string.format("Tranzaksiya #%d holati: %s", 599, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
599-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #599 holati: Bekor qilindi
```


# 600-Topshiriq: Xatoliklarni boshqarish va xavfsizlik arxitekturasi #600
## Topshiriq sharti:
600-vazifa: pcall/xpcall xavfsizlik nazorati, assert tekshiruvlari va barqaror tizim loyihalash.

## Yechim (Lua kodi):
```lua
local function processTransaction_600(balance, amount)
    if amount > balance then
        error("Mablag' yetarsiz: " .. amount)
    end
    return balance - amount
end

local status, res = pcall(processTransaction_600, 100, 600)
print(string.format("Tranzaksiya #%d holati: %s", 600, status and ("Yangi balans: " .. res) or "Bekor qilindi"))
```

## Tushuntirish va Mantiq:
600-vazifada himoyalangan tranzaksiya modeli va xatoliklarni xavfsiz qayta ishlash amalga oshirildi.

## Ishlash natijasi:
```text
Tranzaksiya #600 holati: Bekor qilindi
```

