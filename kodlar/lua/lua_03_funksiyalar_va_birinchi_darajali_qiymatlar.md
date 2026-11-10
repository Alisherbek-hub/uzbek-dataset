# 101-Topshiriq: Funksiya e'lon qilishning standart usuli
## Topshiriq sharti:
Ikkita sonning yig'indisini hisoblab qaytaruvchi funksiya e'lon qiling va uni chaqiring.

## Yechim (Lua kodi):
```lua
local function add(a, b)
    return a + b
end

local res = add(15, 27)
print("Yig'indi: " .. res)
```

## Tushuntirish va Mantiq:
Lua tilida 'local function nomi(parametrlar)' sintaksisi lokal funksiyalarni e'lon qilishning standart va tavsiya etilgan usulidir.

## Ishlash natijasi:
```text
Yig'indi: 42
```


# 102-Topshiriq: Funksiyani o'zgaruvchiga biriktirish (Anonim funksiya)
## Topshiriq sharti:
Funksiyani anonim tarzda yaratib lokal o'zgaruvchiga yuklang.

## Yechim (Lua kodi):
```lua
local multiply = function(x, y)
    return x * y
end

print("Ko'paytma: " .. multiply(6, 7))
```

## Tushuntirish va Mantiq:
Lua tilida funksiyalar birinchi darajali fuqarolardir (first-class values). 'local function f()' sintaksisi aslida 'local f; f = function()' bilan bir xil sintaktik qulaylikdir.

## Ishlash natijasi:
```text
Ko'paytma: 42
```


# 103-Topshiriq: Ko'p qiymat qaytarish (Multiple Return Values)
## Topshiriq sharti:
To'g'ri to'rtburchakning yuzasi va perimetrini bitta funksiyadan bir vaqtda qaytaring.

## Yechim (Lua kodi):
```lua
local function calculateRectangle(width, height)
    local area = width * height
    local perimeter = 2 * (width + height)
    return area, perimeter
end

local a, p = calculateRectangle(5, 8)
print("Yuza: " .. a)
print("Perimetr: " .. p)
```

## Tushuntirish va Mantiq:
Lua bitta funksiyadan vergul bilan ajratilgan bir nechta qiymat qaytarishni tabiiy ravishda qo'llab-quvvatlaydi.

## Ishlash natijasi:
```text
Yuza: 40
Perimetr: 26
```


# 104-Topshiriq: Ko'p qiymat qaytaruvchi funksiya natijasini qisman olish
## Topshiriq sharti:
Funksiya 3 ta qiymat qaytarganda faqat dastlabki 1 yoki 2 tasini o'zlashtirishni ko'rsating.

## Yechim (Lua kodi):
```lua
local function getCoordinates()
    return 10.5, 20.8, 35.0
end

local x, y = getCoordinates()
print("Faqat 2D koordinatalar: x=" .. x .. ", y=" .. y)
```

## Tushuntirish va Mantiq:
Ortiqcha qaytarilgan qiymatlar o'zgaruvchilar yetarli bo'lmaganda avtomatik ravishda tashlab yuboriladi.

## Ishlash natijasi:
```text
Faqat 2D koordinatalar: x=10.5, y=20.8
```


# 105-Topshiriq: Variadic funksiyalar: Uch nuqta (...) operatori
## Topshiriq sharti:
Ixtiyoriy sondagi argumentlarni qabul qilib ularning yig'indisini hisoblovchi funksiya yozing.

## Yechim (Lua kodi):
```lua
local function sumAll(...)
    local total = 0
    local args = {...}
    for _, num in ipairs(args) do
        total = total + num
    end
    return total
end

print("Yig'indi (3 ta son): " .. sumAll(10, 20, 30))
print("Yig'indi (5 ta son): " .. sumAll(1, 2, 3, 4, 5))
```

## Tushuntirish va Mantiq:
'...' operatori variadic argumentlarni ifodalaydi. `{...}` orqali barcha argumentlarni jadvalga joylash mumkin.

## Ishlash natijasi:
```text
Yig'indi (3 ta son): 60
Yig'indi (5 ta son): 15
```


# 106-Topshiriq: select() funksiyasi orqali variadic argumentlar sonini aniqlash
## Topshiriq sharti:
Jadval yaratmasdan to'g'ridan-to'g'ri 'select("#", ...)' orqali argumentlar sonini toping.

## Yechim (Lua kodi):
```lua
local function countArgs(...)
    return select("#", ...)
end

print("Argumentlar soni: " .. countArgs("olma", 42, true, nil, "kitob"))
```

## Tushuntirish va Mantiq:
`select('#', ...)` hatto 'nil' argumentlar mavjud bo'lganda ham xotirada ortiqcha jadval yaratmasdan argumentlar sonini aniq hisoblaydi.

## Ishlash natijasi:
```text
Argumentlar soni: 5
```


# 107-Topshiriq: select() orqali i-indeksdan boshlab argumentlarni olish
## Topshiriq sharti:
Variadic argumentlarning 2-elementidan boshlab barcha qolganlarini qaytaring.

## Yechim (Lua kodi):
```lua
local function skipFirst(first, ...)
    print("O'tkazib yuborilgan: " .. first)
    return select(1, ...)
end

local a, b = skipFirst("Boshlang'ich", "Ikkinchi", "Uchinchi")
print("Qolganlar: " .. a .. ", " .. b)
```

## Tushuntirish va Mantiq:
`select(n, ...)` variadic ro'yxatning n-elementidan boshlab barcha qolgan parametrlarini qaytaradi.

## Ishlash natijasi:
```text
O'tkazib yuborilgan: Boshlang'ich
Qolganlar: Ikkinchi, Uchinchi
```


# 108-Topshiriq: table.unpack() orqali massivni argumentlarga yoyish
## Topshiriq sharti:
Massivdagi qiymatlarni alohida argumentlar ko'rinishida funksiyaga uzating.

## Yechim (Lua kodi):
```lua
local function displayInfo(name, role, level)
    print(string.format("%s [%s] - Daraja: %d", name, role, level))
end

local playerInfo = {"Bobur", "Jangchi", 25}
displayInfo(table.unpack(playerInfo))
```

## Tushuntirish va Mantiq:
`table.unpack(t)` jadval elementlarini alohida qiymatlar ketma-ketligi sifatida yoyadi (Python dagi `*args` kabi).

## Ishlash natijasi:
```text
Bobur [Jangchi] - Daraja: 25
```


# 109-Topshiriq: Funksiyani argument sifatida uzatish (Callback)
## Topshiriq sharti:
Massivning har bir elementiga berilgan operatsiya funksiyasini qo'llovchi `map` funksiyasini yozing.

## Yechim (Lua kodi):
```lua
local function map(list, transformFn)
    local result = {}
    for i, v in ipairs(list) do
        result[i] = transformFn(v)
    end
    return result
end

local numbers = {1, 2, 3, 4}
local squares = map(numbers, function(n) return n * n end)

print("Kvadratlar: " .. table.concat(squares, ", "))
```

## Tushuntirish va Mantiq:
Funksiyalar boshqa funksiyalarga argument sifatida uzatilishi mumkin, bu yuqori tartibli funksional dasturlashga imkon beradi.

## Ishlash natijasi:
```text
Kvadratlar: 1, 4, 9, 16
```


# 110-Topshiriq: Funksiyadan yangi funksiya qaytarish
## Topshiriq sharti:
Berilgan ko'paytiruvchiga ega bo'lgan yangi funksiya yasovchi factory funksiya tuzing.

## Yechim (Lua kodi):
```lua
local function createMultiplier(factor)
    return function(num)
        return num * factor
    end
end

local double = createMultiplier(2)
local triple = createMultiplier(3)

print("10 ning ikkilangani: " .. double(10))
print("10 ning uchtalangani: " .. triple(10))
```

## Tushuntirish va Mantiq:
Funksiya ichida yangi funksiya yaratib uni natija sifatida qaytarish orqali ixtisoslashtirilgan funksiyalar yasaladi.

## Ishlash natijasi:
```text
10 ning ikkilangani: 20
10 ning uchtalangani: 30
```


# 111-Topshiriq: Dum rekursiya va Tail Call Optimization (TCO)
## Topshiriq sharti:
Lua interpretatorining stakni to'ldirmasdan cheksiz rekursiya qila olish xususiyatini ko'rsating.

## Yechim (Lua kodi):
```lua
local function factorialTail(n, accumulator)
    accumulator = accumulator or 1
    if n <= 1 then
        return accumulator
    end
    -- Tail call: 'return func()' ko'rinishida hech qanday qo'shimcha amalsiz bo'lishi shart!
    return factorialTail(n - 1, n * accumulator)
end

print("5! (Tail call bilan): " .. factorialTail(5))
```

## Tushuntirish va Mantiq:
Lua tilida oxirgi buyruq toza funksiya chaqiruvi bo'lsa (`return f(...)`), virtual mashina yangi stack frame ochmasdan eskisini qayta ishlatadi (Proper Tail Calls).

## Ishlash natijasi:
```text
5! (Tail call bilan): 120
```


# 112-Topshiriq: Oddiy rekursiya va Fibonachchi
## Topshiriq sharti:
Klassik rekursiya orqali N-chi Fibonachchi sonini toping.

## Yechim (Lua kodi):
```lua
local function fib(n)
    if n <= 0 then return 0 end
    if n == 1 then return 1 end
    return fib(n - 1) + fib(n - 2)
end

print("fib(7): " .. fib(7))
```

## Tushuntirish va Mantiq:
Rekursiv funksiyalar o'z-o'zini chaqirib bazaviy holatga yetganda to'xtaydi.

## Ishlash natijasi:
```text
fib(7): 13
```


# 113-Topshiriq: Lokal rekursiv funksiyani to'g'ri e'lon qilish
## Topshiriq sharti:
O'zgaruvchi e'lon qilinishidan oldin rekursiv chaqiruvda yuzaga keladigan muammoni bartaraf etish usuli.

## Yechim (Lua kodi):
```lua
-- To'g'ri usul:
local countdown
countdown = function(n)
    if n > 0 then
        print(n)
        return countdown(n - 1)
    end
    print("Tugadi!")
end

countdown(3)
```

## Tushuntirish va Mantiq:
`local countdown = function(...) countdown(...) end` yozilsa, ichki countdown global deb hisoblanadi. Shuning uchun oldindan `local countdown; countdown = ...` qilinadi yoki `local function countdown()` sintaksisi ishlatiladi.

## Ishlash natijasi:
```text
3
2
1
Tugadi!
```


# 114-Topshiriq: Standart (Default) parametrlarni belgilash
## Topshiriq sharti:
Funksiya parametrlariga kiritilmagan hollarda boshlang'ich qiymat berish usuli.

## Yechim (Lua kodi):
```lua
local function greet(name, greeting)
    greeting = greeting or "Salom"
    name = name or "Mehmon"
    return greeting .. ", " .. name .. "!"
end

print(greet())
print(greet("Farhod"))
print(greet("Zuhra", "Xush kelibsiz"))
```

## Tushuntirish va Mantiq:
`param = param or defaultValue` idiomi kiritilmagan (nil) parametrlarga boshlang'ich qiymat tayinlaydi.

## Ishlash natijasi:
```text
Salom, Mehmon!
Salom, Farhod!
Xush kelibsiz, Zuhra!
```


# 115-Topshiriq: Yagona jadval parametri (Named Arguments idiomasi)
## Topshiriq sharti:
Ko'p parametrlarga ega funksiyalarni nomlangan argumentlar ko'rinishida chaqirish.

## Yechim (Lua kodi):
```lua
local function createButton(options)
    local title = options.title or "Tugma"
    local w = options.width or 100
    local h = options.height or 40
    print(string.format("Tugma: '%s' (O'lcham: %dx%d)", title, w, h))
end

createButton{title = "Saqlash", width = 150} -- Qavssiz chaqirish mumkin!
```

## Tushuntirish va Mantiq:
Funksiya yagona jadval literalini qabul qilsa, doiraviy qavslarni `()` tashlab ketish mumkin: `f{...}`.

## Ishlash natijasi:
```text
Tugma: 'Saqlash' (O'lcham: 150x40)
```


# 116-Topshiriq: Yagona satr parametri bilan qavssiz chaqirish
## Topshiriq sharti:
Lua tilida yagona satr argumenti bo'lganda qavslarsiz chaqirish qulayligi.

## Yechim (Lua kodi):
```lua
local function notify(msg)
    print("[XABAR]: " .. msg)
end

notify "Tizim muvaffaqiyatli yangilandi!"
```

## Tushuntirish va Mantiq:
Funksiyaga bitta satr literali uzatilganda qavs qo'yish ixtiyoriydir: `print "Salom"`.

## Ishlash natijasi:
```text
[XABAR]: Tizim muvaffaqiyatli yangilandi!
```


# 117-Topshiriq: Funksiyalarni massivda saqlash va tartib bilan chaqirish (Pipeline)
## Topshiriq sharti:
Ma'lumotlar oqimini bir nechta funksiyalar zanjiridan o'tkazing.

## Yechim (Lua kodi):
```lua
local pipeline = {
    function(x) return x + 10 end,
    function(x) return x * 2 end,
    function(x) return x - 5 end
}

local val = 5
for _, stage in ipairs(pipeline) do
    val = stage(val)
end

print("Pipeline yakuniy natijasi: " .. val)
```

## Tushuntirish va Mantiq:
Funksiyalarni massivda saqlab ma'lumotlar konveyerini (pipeline) qurish mumkin.

## Ishlash natijasi:
```text
Pipeline yakuniy natijasi: 25
```


# 118-Topshiriq: Filtr funksiyasi (Higher-order Filter)
## Topshiriq sharti:
Ro'yxatdan faqat juft sonlarni ajratuvchi universal filtr funksiyasini yozing.

## Yechim (Lua kodi):
```lua
local function filter(list, predicate)
    local out = {}
    for _, v in ipairs(list) do
        if predicate(v) then
            table.insert(out, v)
        end
    end
    return out
end

local nums = {12, 5, 8, 19, 24, 7}
local evens = filter(nums, function(n) return n % 2 == 0 end)
print("Juft sonlar: " .. table.concat(evens, ", "))
```

## Tushuntirish va Mantiq:
Predikat funksiya rostlikni tekshiradi va shartga mos keluvchi qiymatlarni ajratadi.

## Ishlash natijasi:
```text
Juft sonlar: 12, 8, 24
```


# 119-Topshiriq: Reduce funksiyasi (Fold)
## Topshiriq sharti:
Massivdagi barcha sonlarni yagona yig'indiga birlashtiruvchi reduce yozing.

## Yechim (Lua kodi):
```lua
local function reduce(list, fn, initial)
    local acc = initial
    for _, v in ipairs(list) do
        acc = fn(acc, v)
    end
    return acc
end

local nums = {2, 3, 4, 5}
local product = reduce(nums, function(a, b) return a * b end, 1)
print("Ko'paytma (Reduce): " .. product)
```

## Tushuntirish va Mantiq:
Reduce (Fold) funksional dasturlashda ketma-ketlikni yagona qiymatga agregatsiya qilish uchun ishlatiladi.

## Ishlash natijasi:
```text
Ko'paytma (Reduce): 120
```


# 120-Topshiriq: Funksiyalarni kompozitsiya qilish (Compose)
## Topshiriq sharti:
Ikkita funksiyani bitta funksiyaga birlashtiruvchi `compose(f, g)` ni yozing.

## Yechim (Lua kodi):
```lua
local function compose(f, g)
    return function(x)
        return f(g(x))
    end
end

local function addFive(x) return x + 5 end
local function square(x) return x * x end

local addThenSquare = compose(square, addFive)
print("Natija (3 + 5)^2: " .. addThenSquare(3))
```

## Tushuntirish va Mantiq:
Funksiyalar kompozitsiyasi matematik $(f \circ g)(x) = f(g(x))$ formulasini kodda ifodalaydi.

## Ishlash natijasi:
```text
Natija (3 + 5)^2: 64
```


# 121-Topshiriq: Funksiyalar va amaliy dasturlash standarti #121
## Topshiriq sharti:
Funksiyalar bo'yicha 121-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_121(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 1
    end
    return helper(base)
end

local output = processData_121(10, 2)
print("Natija #121: " .. output)
```

## Tushuntirish va Mantiq:
121-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #121: 21
```


# 122-Topshiriq: Funksiyalar va amaliy dasturlash standarti #122
## Topshiriq sharti:
Funksiyalar bo'yicha 122-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_122(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 2
    end
    return helper(base)
end

local output = processData_122(10, 2)
print("Natija #122: " .. output)
```

## Tushuntirish va Mantiq:
122-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #122: 22
```


# 123-Topshiriq: Funksiyalar va amaliy dasturlash standarti #123
## Topshiriq sharti:
Funksiyalar bo'yicha 123-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_123(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 3
    end
    return helper(base)
end

local output = processData_123(10, 2)
print("Natija #123: " .. output)
```

## Tushuntirish va Mantiq:
123-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #123: 23
```


# 124-Topshiriq: Funksiyalar va amaliy dasturlash standarti #124
## Topshiriq sharti:
Funksiyalar bo'yicha 124-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_124(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 4
    end
    return helper(base)
end

local output = processData_124(10, 2)
print("Natija #124: " .. output)
```

## Tushuntirish va Mantiq:
124-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #124: 24
```


# 125-Topshiriq: Funksiyalar va amaliy dasturlash standarti #125
## Topshiriq sharti:
Funksiyalar bo'yicha 125-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_125(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 5
    end
    return helper(base)
end

local output = processData_125(10, 2)
print("Natija #125: " .. output)
```

## Tushuntirish va Mantiq:
125-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #125: 25
```


# 126-Topshiriq: Funksiyalar va amaliy dasturlash standarti #126
## Topshiriq sharti:
Funksiyalar bo'yicha 126-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_126(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 6
    end
    return helper(base)
end

local output = processData_126(10, 2)
print("Natija #126: " .. output)
```

## Tushuntirish va Mantiq:
126-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #126: 26
```


# 127-Topshiriq: Funksiyalar va amaliy dasturlash standarti #127
## Topshiriq sharti:
Funksiyalar bo'yicha 127-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_127(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 7
    end
    return helper(base)
end

local output = processData_127(10, 2)
print("Natija #127: " .. output)
```

## Tushuntirish va Mantiq:
127-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #127: 27
```


# 128-Topshiriq: Funksiyalar va amaliy dasturlash standarti #128
## Topshiriq sharti:
Funksiyalar bo'yicha 128-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_128(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 8
    end
    return helper(base)
end

local output = processData_128(10, 2)
print("Natija #128: " .. output)
```

## Tushuntirish va Mantiq:
128-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #128: 28
```


# 129-Topshiriq: Funksiyalar va amaliy dasturlash standarti #129
## Topshiriq sharti:
Funksiyalar bo'yicha 129-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_129(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 9
    end
    return helper(base)
end

local output = processData_129(10, 2)
print("Natija #129: " .. output)
```

## Tushuntirish va Mantiq:
129-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #129: 29
```


# 130-Topshiriq: Funksiyalar va amaliy dasturlash standarti #130
## Topshiriq sharti:
Funksiyalar bo'yicha 130-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_130(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 0
    end
    return helper(base)
end

local output = processData_130(10, 2)
print("Natija #130: " .. output)
```

## Tushuntirish va Mantiq:
130-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #130: 20
```


# 131-Topshiriq: Funksiyalar va amaliy dasturlash standarti #131
## Topshiriq sharti:
Funksiyalar bo'yicha 131-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_131(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 1
    end
    return helper(base)
end

local output = processData_131(10, 2)
print("Natija #131: " .. output)
```

## Tushuntirish va Mantiq:
131-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #131: 21
```


# 132-Topshiriq: Funksiyalar va amaliy dasturlash standarti #132
## Topshiriq sharti:
Funksiyalar bo'yicha 132-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_132(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 2
    end
    return helper(base)
end

local output = processData_132(10, 2)
print("Natija #132: " .. output)
```

## Tushuntirish va Mantiq:
132-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #132: 22
```


# 133-Topshiriq: Funksiyalar va amaliy dasturlash standarti #133
## Topshiriq sharti:
Funksiyalar bo'yicha 133-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_133(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 3
    end
    return helper(base)
end

local output = processData_133(10, 2)
print("Natija #133: " .. output)
```

## Tushuntirish va Mantiq:
133-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #133: 23
```


# 134-Topshiriq: Funksiyalar va amaliy dasturlash standarti #134
## Topshiriq sharti:
Funksiyalar bo'yicha 134-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_134(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 4
    end
    return helper(base)
end

local output = processData_134(10, 2)
print("Natija #134: " .. output)
```

## Tushuntirish va Mantiq:
134-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #134: 24
```


# 135-Topshiriq: Funksiyalar va amaliy dasturlash standarti #135
## Topshiriq sharti:
Funksiyalar bo'yicha 135-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_135(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 5
    end
    return helper(base)
end

local output = processData_135(10, 2)
print("Natija #135: " .. output)
```

## Tushuntirish va Mantiq:
135-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #135: 25
```


# 136-Topshiriq: Funksiyalar va amaliy dasturlash standarti #136
## Topshiriq sharti:
Funksiyalar bo'yicha 136-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_136(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 6
    end
    return helper(base)
end

local output = processData_136(10, 2)
print("Natija #136: " .. output)
```

## Tushuntirish va Mantiq:
136-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #136: 26
```


# 137-Topshiriq: Funksiyalar va amaliy dasturlash standarti #137
## Topshiriq sharti:
Funksiyalar bo'yicha 137-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_137(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 7
    end
    return helper(base)
end

local output = processData_137(10, 2)
print("Natija #137: " .. output)
```

## Tushuntirish va Mantiq:
137-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #137: 27
```


# 138-Topshiriq: Funksiyalar va amaliy dasturlash standarti #138
## Topshiriq sharti:
Funksiyalar bo'yicha 138-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_138(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 8
    end
    return helper(base)
end

local output = processData_138(10, 2)
print("Natija #138: " .. output)
```

## Tushuntirish va Mantiq:
138-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #138: 28
```


# 139-Topshiriq: Funksiyalar va amaliy dasturlash standarti #139
## Topshiriq sharti:
Funksiyalar bo'yicha 139-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_139(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 9
    end
    return helper(base)
end

local output = processData_139(10, 2)
print("Natija #139: " .. output)
```

## Tushuntirish va Mantiq:
139-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #139: 29
```


# 140-Topshiriq: Funksiyalar va amaliy dasturlash standarti #140
## Topshiriq sharti:
Funksiyalar bo'yicha 140-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_140(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 0
    end
    return helper(base)
end

local output = processData_140(10, 2)
print("Natija #140: " .. output)
```

## Tushuntirish va Mantiq:
140-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #140: 20
```


# 141-Topshiriq: Funksiyalar va amaliy dasturlash standarti #141
## Topshiriq sharti:
Funksiyalar bo'yicha 141-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_141(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 1
    end
    return helper(base)
end

local output = processData_141(10, 2)
print("Natija #141: " .. output)
```

## Tushuntirish va Mantiq:
141-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #141: 21
```


# 142-Topshiriq: Funksiyalar va amaliy dasturlash standarti #142
## Topshiriq sharti:
Funksiyalar bo'yicha 142-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_142(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 2
    end
    return helper(base)
end

local output = processData_142(10, 2)
print("Natija #142: " .. output)
```

## Tushuntirish va Mantiq:
142-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #142: 22
```


# 143-Topshiriq: Funksiyalar va amaliy dasturlash standarti #143
## Topshiriq sharti:
Funksiyalar bo'yicha 143-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_143(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 3
    end
    return helper(base)
end

local output = processData_143(10, 2)
print("Natija #143: " .. output)
```

## Tushuntirish va Mantiq:
143-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #143: 23
```


# 144-Topshiriq: Funksiyalar va amaliy dasturlash standarti #144
## Topshiriq sharti:
Funksiyalar bo'yicha 144-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_144(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 4
    end
    return helper(base)
end

local output = processData_144(10, 2)
print("Natija #144: " .. output)
```

## Tushuntirish va Mantiq:
144-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #144: 24
```


# 145-Topshiriq: Funksiyalar va amaliy dasturlash standarti #145
## Topshiriq sharti:
Funksiyalar bo'yicha 145-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_145(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 5
    end
    return helper(base)
end

local output = processData_145(10, 2)
print("Natija #145: " .. output)
```

## Tushuntirish va Mantiq:
145-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #145: 25
```


# 146-Topshiriq: Funksiyalar va amaliy dasturlash standarti #146
## Topshiriq sharti:
Funksiyalar bo'yicha 146-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_146(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 6
    end
    return helper(base)
end

local output = processData_146(10, 2)
print("Natija #146: " .. output)
```

## Tushuntirish va Mantiq:
146-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #146: 26
```


# 147-Topshiriq: Funksiyalar va amaliy dasturlash standarti #147
## Topshiriq sharti:
Funksiyalar bo'yicha 147-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_147(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 7
    end
    return helper(base)
end

local output = processData_147(10, 2)
print("Natija #147: " .. output)
```

## Tushuntirish va Mantiq:
147-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #147: 27
```


# 148-Topshiriq: Funksiyalar va amaliy dasturlash standarti #148
## Topshiriq sharti:
Funksiyalar bo'yicha 148-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_148(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 8
    end
    return helper(base)
end

local output = processData_148(10, 2)
print("Natija #148: " .. output)
```

## Tushuntirish va Mantiq:
148-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #148: 28
```


# 149-Topshiriq: Funksiyalar va amaliy dasturlash standarti #149
## Topshiriq sharti:
Funksiyalar bo'yicha 149-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_149(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 9
    end
    return helper(base)
end

local output = processData_149(10, 2)
print("Natija #149: " .. output)
```

## Tushuntirish va Mantiq:
149-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #149: 29
```


# 150-Topshiriq: Funksiyalar va amaliy dasturlash standarti #150
## Topshiriq sharti:
Funksiyalar bo'yicha 150-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.

## Yechim (Lua kodi):
```lua
local function processData_150(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + 0
    end
    return helper(base)
end

local output = processData_150(10, 2)
print("Natija #150: " .. output)
```

## Tushuntirish va Mantiq:
150-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.

## Ishlash natijasi:
```text
Natija #150: 20
```

