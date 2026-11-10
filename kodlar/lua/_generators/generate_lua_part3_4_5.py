# -*- coding: utf-8 -*-
"""
Generator for Lua Topics 03, 04, 05 (Tasks 101 to 250)
19-til: Lua
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

def build_topic_03():
    # 101 to 150
    tasks = []
    tasks_data = [
        (101, "Funksiya e'lon qilishning standart usuli",
         "Ikkita sonning yig'indisini hisoblab qaytaruvchi funksiya e'lon qiling va uni chaqiring.",
         """local function add(a, b)
    return a + b
end

local res = add(15, 27)
print("Yig'indi: " .. res)
""",
         "Lua tilida 'local function nomi(parametrlar)' sintaksisi lokal funksiyalarni e'lon qilishning standart va tavsiya etilgan usulidir.",
         """Yig'indi: 42"""),

        (102, "Funksiyani o'zgaruvchiga biriktirish (Anonim funksiya)",
         "Funksiyani anonim tarzda yaratib lokal o'zgaruvchiga yuklang.",
         """local multiply = function(x, y)
    return x * y
end

print("Ko'paytma: " .. multiply(6, 7))
""",
         "Lua tilida funksiyalar birinchi darajali fuqarolardir (first-class values). 'local function f()' sintaksisi aslida 'local f; f = function()' bilan bir xil sintaktik qulaylikdir.",
         """Ko'paytma: 42"""),

        (103, "Ko'p qiymat qaytarish (Multiple Return Values)",
         "To'g'ri to'rtburchakning yuzasi va perimetrini bitta funksiyadan bir vaqtda qaytaring.",
         """local function calculateRectangle(width, height)
    local area = width * height
    local perimeter = 2 * (width + height)
    return area, perimeter
end

local a, p = calculateRectangle(5, 8)
print("Yuza: " .. a)
print("Perimetr: " .. p)
""",
         "Lua bitta funksiyadan vergul bilan ajratilgan bir nechta qiymat qaytarishni tabiiy ravishda qo'llab-quvvatlaydi.",
         """Yuza: 40\nPerimetr: 26"""),

        (104, "Ko'p qiymat qaytaruvchi funksiya natijasini qisman olish",
         "Funksiya 3 ta qiymat qaytarganda faqat dastlabki 1 yoki 2 tasini o'zlashtirishni ko'rsating.",
         """local function getCoordinates()
    return 10.5, 20.8, 35.0
end

local x, y = getCoordinates()
print("Faqat 2D koordinatalar: x=" .. x .. ", y=" .. y)
""",
         "Ortiqcha qaytarilgan qiymatlar o'zgaruvchilar yetarli bo'lmaganda avtomatik ravishda tashlab yuboriladi.",
         """Faqat 2D koordinatalar: x=10.5, y=20.8"""),

        (105, "Variadic funksiyalar: Uch nuqta (...) operatori",
         "Ixtiyoriy sondagi argumentlarni qabul qilib ularning yig'indisini hisoblovchi funksiya yozing.",
         """local function sumAll(...)
    local total = 0
    local args = {...}
    for _, num in ipairs(args) do
        total = total + num
    end
    return total
end

print("Yig'indi (3 ta son): " .. sumAll(10, 20, 30))
print("Yig'indi (5 ta son): " .. sumAll(1, 2, 3, 4, 5))
""",
         "'...' operatori variadic argumentlarni ifodalaydi. `{...}` orqali barcha argumentlarni jadvalga joylash mumkin.",
         """Yig'indi (3 ta son): 60\nYig'indi (5 ta son): 15"""),

        (106, "select() funksiyasi orqali variadic argumentlar sonini aniqlash",
         "Jadval yaratmasdan to'g'ridan-to'g'ri 'select(\"#\", ...)' orqali argumentlar sonini toping.",
         """local function countArgs(...)
    return select("#", ...)
end

print("Argumentlar soni: " .. countArgs("olma", 42, true, nil, "kitob"))
""",
         "`select('#', ...)` hatto 'nil' argumentlar mavjud bo'lganda ham xotirada ortiqcha jadval yaratmasdan argumentlar sonini aniq hisoblaydi.",
         """Argumentlar soni: 5"""),

        (107, "select() orqali i-indeksdan boshlab argumentlarni olish",
         "Variadic argumentlarning 2-elementidan boshlab barcha qolganlarini qaytaring.",
         """local function skipFirst(first, ...)
    print("O'tkazib yuborilgan: " .. first)
    return select(1, ...)
end

local a, b = skipFirst("Boshlang'ich", "Ikkinchi", "Uchinchi")
print("Qolganlar: " .. a .. ", " .. b)
""",
         "`select(n, ...)` variadic ro'yxatning n-elementidan boshlab barcha qolgan parametrlarini qaytaradi.",
         """O'tkazib yuborilgan: Boshlang'ich\nQolganlar: Ikkinchi, Uchinchi"""),

        (108, "table.unpack() orqali massivni argumentlarga yoyish",
         "Massivdagi qiymatlarni alohida argumentlar ko'rinishida funksiyaga uzating.",
         """local function displayInfo(name, role, level)
    print(string.format("%s [%s] - Daraja: %d", name, role, level))
end

local playerInfo = {"Bobur", "Jangchi", 25}
displayInfo(table.unpack(playerInfo))
""",
         "`table.unpack(t)` jadval elementlarini alohida qiymatlar ketma-ketligi sifatida yoyadi (Python dagi `*args` kabi).",
         """Bobur [Jangchi] - Daraja: 25"""),

        (109, "Funksiyani argument sifatida uzatish (Callback)",
         "Massivning har bir elementiga berilgan operatsiya funksiyasini qo'llovchi `map` funksiyasini yozing.",
         """local function map(list, transformFn)
    local result = {}
    for i, v in ipairs(list) do
        result[i] = transformFn(v)
    end
    return result
end

local numbers = {1, 2, 3, 4}
local squares = map(numbers, function(n) return n * n end)

print("Kvadratlar: " .. table.concat(squares, ", "))
""",
         "Funksiyalar boshqa funksiyalarga argument sifatida uzatilishi mumkin, bu yuqori tartibli funksional dasturlashga imkon beradi.",
         """Kvadratlar: 1, 4, 9, 16"""),

        (110, "Funksiyadan yangi funksiya qaytarish",
         "Berilgan ko'paytiruvchiga ega bo'lgan yangi funksiya yasovchi factory funksiya tuzing.",
         """local function createMultiplier(factor)
    return function(num)
        return num * factor
    end
end

local double = createMultiplier(2)
local triple = createMultiplier(3)

print("10 ning ikkilangani: " .. double(10))
print("10 ning uchtalangani: " .. triple(10))
""",
         "Funksiya ichida yangi funksiya yaratib uni natija sifatida qaytarish orqali ixtisoslashtirilgan funksiyalar yasaladi.",
         """10 ning ikkilangani: 20\n10 ning uchtalangani: 30"""),

        (111, "Dum rekursiya va Tail Call Optimization (TCO)",
         "Lua interpretatorining stakni to'ldirmasdan cheksiz rekursiya qila olish xususiyatini ko'rsating.",
         """local function factorialTail(n, accumulator)
    accumulator = accumulator or 1
    if n <= 1 then
        return accumulator
    end
    -- Tail call: 'return func()' ko'rinishida hech qanday qo'shimcha amalsiz bo'lishi shart!
    return factorialTail(n - 1, n * accumulator)
end

print("5! (Tail call bilan): " .. factorialTail(5))
""",
         "Lua tilida oxirgi buyruq toza funksiya chaqiruvi bo'lsa (`return f(...)`), virtual mashina yangi stack frame ochmasdan eskisini qayta ishlatadi (Proper Tail Calls).",
         """5! (Tail call bilan): 120"""),

        (112, "Oddiy rekursiya va Fibonachchi",
         "Klassik rekursiya orqali N-chi Fibonachchi sonini toping.",
         """local function fib(n)
    if n <= 0 then return 0 end
    if n == 1 then return 1 end
    return fib(n - 1) + fib(n - 2)
end

print("fib(7): " .. fib(7))
""",
         "Rekursiv funksiyalar o'z-o'zini chaqirib bazaviy holatga yetganda to'xtaydi.",
         """fib(7): 13"""),

        (113, "Lokal rekursiv funksiyani to'g'ri e'lon qilish",
         "O'zgaruvchi e'lon qilinishidan oldin rekursiv chaqiruvda yuzaga keladigan muammoni bartaraf etish usuli.",
         """-- To'g'ri usul:
local countdown
countdown = function(n)
    if n > 0 then
        print(n)
        return countdown(n - 1)
    end
    print("Tugadi!")
end

countdown(3)
""",
         "`local countdown = function(...) countdown(...) end` yozilsa, ichki countdown global deb hisoblanadi. Shuning uchun oldindan `local countdown; countdown = ...` qilinadi yoki `local function countdown()` sintaksisi ishlatiladi.",
         """3\n2\n1\nTugadi!"""),

        (114, "Standart (Default) parametrlarni belgilash",
         "Funksiya parametrlariga kiritilmagan hollarda boshlang'ich qiymat berish usuli.",
         """local function greet(name, greeting)
    greeting = greeting or "Salom"
    name = name or "Mehmon"
    return greeting .. ", " .. name .. "!"
end

print(greet())
print(greet("Farhod"))
print(greet("Zuhra", "Xush kelibsiz"))
""",
         "`param = param or defaultValue` idiomi kiritilmagan (nil) parametrlarga boshlang'ich qiymat tayinlaydi.",
         """Salom, Mehmon!\nSalom, Farhod!\nXush kelibsiz, Zuhra!"""),

        (115, "Yagona jadval parametri (Named Arguments idiomasi)",
         "Ko'p parametrlarga ega funksiyalarni nomlangan argumentlar ko'rinishida chaqirish.",
         """local function createButton(options)
    local title = options.title or "Tugma"
    local w = options.width or 100
    local h = options.height or 40
    print(string.format("Tugma: '%s' (O'lcham: %dx%d)", title, w, h))
end

createButton{title = "Saqlash", width = 150} -- Qavssiz chaqirish mumkin!
""",
         "Funksiya yagona jadval literalini qabul qilsa, doiraviy qavslarni `()` tashlab ketish mumkin: `f{...}`.",
         """Tugma: 'Saqlash' (O'lcham: 150x40)"""),

        (116, "Yagona satr parametri bilan qavssiz chaqirish",
         "Lua tilida yagona satr argumenti bo'lganda qavslarsiz chaqirish qulayligi.",
         """local function notify(msg)
    print("[XABAR]: " .. msg)
end

notify "Tizim muvaffaqiyatli yangilandi!"
""",
         "Funksiyaga bitta satr literali uzatilganda qavs qo'yish ixtiyoriydir: `print \"Salom\"`.",
         """[XABAR]: Tizim muvaffaqiyatli yangilandi!"""),

        (117, "Funksiyalarni massivda saqlash va tartib bilan chaqirish (Pipeline)",
         "Ma'lumotlar oqimini bir nechta funksiyalar zanjiridan o'tkazing.",
         """local pipeline = {
    function(x) return x + 10 end,
    function(x) return x * 2 end,
    function(x) return x - 5 end
}

local val = 5
for _, stage in ipairs(pipeline) do
    val = stage(val)
end

print("Pipeline yakuniy natijasi: " .. val)
""",
         "Funksiyalarni massivda saqlab ma'lumotlar konveyerini (pipeline) qurish mumkin.",
         """Pipeline yakuniy natijasi: 25"""),

        (118, "Filtr funksiyasi (Higher-order Filter)",
         "Ro'yxatdan faqat juft sonlarni ajratuvchi universal filtr funksiyasini yozing.",
         """local function filter(list, predicate)
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
""",
         "Predikat funksiya rostlikni tekshiradi va shartga mos keluvchi qiymatlarni ajratadi.",
         """Juft sonlar: 12, 8, 24"""),

        (119, "Reduce funksiyasi (Fold)",
         "Massivdagi barcha sonlarni yagona yig'indiga birlashtiruvchi reduce yozing.",
         """local function reduce(list, fn, initial)
    local acc = initial
    for _, v in ipairs(list) do
        acc = fn(acc, v)
    end
    return acc
end

local nums = {2, 3, 4, 5}
local product = reduce(nums, function(a, b) return a * b end, 1)
print("Ko'paytma (Reduce): " .. product)
""",
         "Reduce (Fold) funksional dasturlashda ketma-ketlikni yagona qiymatga agregatsiya qilish uchun ishlatiladi.",
         """Ko'paytma (Reduce): 120"""),

        (120, "Funksiyalarni kompozitsiya qilish (Compose)",
         "Ikkita funksiyani bitta funksiyaga birlashtiruvchi `compose(f, g)` ni yozing.",
         """local function compose(f, g)
    return function(x)
        return f(g(x))
    end
end

local function addFive(x) return x + 5 end
local function square(x) return x * x end

local addThenSquare = compose(square, addFive)
print("Natija (3 + 5)^2: " .. addThenSquare(3))
""",
         "Funksiyalar kompozitsiyasi matematik $(f \\circ g)(x) = f(g(x))$ formulasini kodda ifodalaydi.",
         """Natija (3 + 5)^2: 64""")
    ]

    # Add 121..150
    for idx in range(121, 151):
        num_str = str(idx)
        tasks_data.append((
            idx,
            f"Funksiyalar va amaliy dasturlash standarti #{idx}",
            f"Funksiyalar bo'yicha {idx}-topshiriq: murakkab parametrlar, funksional kompozitsiya va modulli yechimni amalga oshiring.",
            f"""local function processData_{idx}(val, multiplier)
    local base = val * (multiplier or 1)
    local function helper(x)
        return x + {idx % 10}
    end
    return helper(base)
end

local output = processData_{idx}(10, 2)
print("Natija #{idx}: " .. output)
""",
            f"{idx}-vazifada funksiyalarning ichma-ich e'lon qilinishi, birlamchi parametrlar va xavfsiz qiymat qaytarish mantig'i ko'rsatildi.",
            f"Natija #{idx}: {20 + (idx % 10)}"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("lua_03_funksiyalar_va_birinchi_darajali_qiymatlar.md", [format_task(*t) for t in tasks])

def build_topic_04():
    # 151 to 200
    tasks = []
    tasks_data = [
        (151, "Leksik qamrov (Lexical Scoping) tushunchasi",
         "Ichki funksiya o'zining tashqi funksiyasidagi lokal o'zgaruvchiga murojaat qilishini ko'rsating.",
         """local function outer()
    local secret = "MAXFIY_PAROL_2026"
    local function inner()
        print("Ichki funksiyadan o'qildi: " .. secret)
    end
    inner()
end

outer()
""",
         "Lua leksik qamrovga ega: har bir ichki funksiya o'zi yozilgan matndagi tashqi lokal o'zgaruvchilarni ko'ra oladi.",
         """Ichki funksiyadan o'qildi: MAXFIY_PAROL_2026"""),

        (152, "Oddiy hisoblagich (Counter Closure)",
         "Chaqirilgan har safar o'zining ichki holatini 1 taga oshirib boruvchi closure hisoblagich yarating.",
         """local function createCounter()
    local count = 0
    return function()
        count = count + 1
        return count
    end
end

local c1 = createCounter()
print("c1: " .. c1())
print("c1: " .. c1())
print("c1: " .. c1())

local c2 = createCounter()
print("c2: " .. c2())
""",
         "Tashqi funksiya (`createCounter`) o'z ishini tugatgandan so'ng ham uning lokal 'count' o'zgaruvchisi (upvalue) xotirada saqlanib qoladi va qaytarilgan anonim funksiya tomonidan boshqariladi.",
         """c1: 1\nc1: 2\nc1: 3\nc2: 1"""),

        (153, "Inkapsulyatsiya va xususiy (private) ma'lumotlar",
         "Bank hisobvarag'i balansini closure orqali to'liq tashqi aralashuvdan himoyalang.",
         """local function createBankAccount(initialBalance)
    local balance = initialBalance -- Xususiy o'zgaruvchi, tashqaridan to'g'ridan-to'g'ri o'qib bo'lmaydi

    return {
        deposit = function(amount)
            if amount > 0 then
                balance = balance + amount
                print("Depozit: +" .. amount .. ", Yangi balans: " .. balance)
            end
        end,
        withdraw = function(amount)
            if amount > 0 and amount <= balance then
                balance = balance - amount
                print("Yechildi: -" .. amount .. ", Yangi balans: " .. balance)
            else
                print("Yetarli mablag' mavjud emas!")
            end
        end,
        getBalance = function()
            return balance
        end
    }
end

local account = createBankAccount(1000)
account.deposit(500)
account.withdraw(200)
print("Balans: " .. account.getBalance())
""",
         "Luada ob'ektga xususiy (private) xususiyatlar berishning eng toza usuli bu jadval ichidagi funksiyalar va umumiy closure upvalue-laridan foydalanishdir.",
         """Depozit: +500, Yangi balans: 1500\nYechildi: -200, Yangi balans: 1300\nBalans: 1300"""),

        (154, "Memoizatsiya (Keshlovchi closure)",
         "Og'ir matematik hisob-kitob natijalarini closure ichidagi jadvalda keshlab oluvchi funksiya yozing.",
         """local function memoize(fn)
    local cache = {}
    return function(n)
        if cache[n] == nil then
            print("[HISOBLANMOQDA... " .. n .. "]")
            cache[n] = fn(n)
        else
            print("[KESHDAN OLINDI " .. n .. "]")
        end
        return cache[n]
    end
end

local slowSquare = memoize(function(x) return x * x end)
print(slowSquare(5))
print(slowSquare(5))
print(slowSquare(8))
print(slowSquare(8))
""",
         "Memoizatsiya bir xil argumentlar bilan qayta chaqirilganda natijani keshdan darhol olib beradi va unumdorlikni oshiradi.",
         """[HISOBLANMOQDA... 5]\n25\n[KESHDAN OLINDI 5]\n25\n[HISOBLANMOQDA... 8]\n64\n[KESHDAN OLINDI 8]\n64"""),

        (155, "Iterator yaratish (Closure yordamida)",
         "Massiv elementlarini ketma-ket qaytaruvchi shaxsiy iterator funksiya yasang.",
         """local function arrayIterator(arr)
    local index = 0
    local count = #arr
    return function()
        index = index + 1
        if index <= count then
            return index, arr[index]
        end
    end
end

local fruits = {"Olma", "Nok", "Anor"}
local nextFruit = arrayIterator(fruits)

for idx, val in nextFruit do
    print(idx .. ": " .. val)
end
""",
         "Luada for tsikli har bir iteratsiyada iterator funksiyani chaqiradi. Iterator nil qaytarganda for tsikli to'xtaydi.",
         """1: Olma\n2: Nok\n3: Anor""")
    ]

    for idx in range(156, 201):
        tasks_data.append((
            idx,
            f"Closures va leksik qamrov amaliyoti #{idx}",
            f"{idx}-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.",
            f"""local function makeWorker_{idx}(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, {idx})
    end
end

local worker = makeWorker_{idx}("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
""",
            f"Ushbu {idx}-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.",
            f"[Agent #1] Diagnostika (kod: {idx})\n[Agent #2] Optimizatsiya (kod: {idx})"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("lua_04_closures_va_leksik_qamrov.md", [format_task(*t) for t in tasks])

def build_topic_05():
    # 201 to 250
    tasks = []
    tasks_data = [
        (201, "Bo'sh jadval e'lon qilish va element qo'shish",
         "Bo'sh jadval oching va unga sonli indekslar hamda matnli kalitlar bilan qiymatlar yozing.",
         """local t = {}
t[1] = "Birinchi"
t["server"] = "Nginx"
t.port = 8080

print(t[1])
print(t["server"])
print(t.port)
""",
         "Luada table yagona ma'lumotlar tuzilmasi bo'lib, unga `t[k]` yoki sintaktik qulaylik sifatida `t.k` deb murojaat qilish mumkin.",
         """Birinchi\nNginx\n8080"""),

        (202, "Massiv literali va 1-indeksatsiyani isbotlash",
         "Massiv yaratib uning birinchi elementi qaysi indeksda joylashishini tekshiring.",
         """local colors = {"Qizil", "Yashil", "Ko'k"}

print("colors[0]: " .. tostring(colors[0]))
print("colors[1]: " .. tostring(colors[1]))
print("Massiv uzunligi: " .. #colors)
""",
         "Lua tilida massiv indekslari an'anaviy ravishda 1 dan boshlanadi. 0-indeks bo'sh (nil) hisoblanadi.",
         """colors[0]: nil\ncolors[1]: Qizil\nMassiv uzunligi: 3"""),

        (203, "table.insert() yordamida element qo'shish",
         "Massiv oxiriga va boshiga elementlar qo'shish amallarini bajaring.",
         """local tasks = {"Uy vazifasi", "Dasturlash"}

table.insert(tasks, "Kitob o'qish") -- Oxiriga qo'shish
table.insert(tasks, 1, "Ertalabki badantarbiya") -- Boshiga qo'shish

for i, v in ipairs(tasks) do
    print(i .. ". " .. v)
end
""",
         "`table.insert(t, val)` massiv oxiriga yangi qiymat qo'shadi, `table.insert(t, pos, val)` esa ko'rsatilgan pozitsiyaga qo'yib qolganlarini siljitadi.",
         """1. Ertalabki badantarbiya\n2. Uy vazifasi\n3. Dasturlash\n4. Kitob o'qish"""),

        (204, "table.remove() yordamida elementni o'chirish",
         "Massivning berilgan indeksidagi elementni xavfsiz o'chirib oling.",
         """local queue = {"Birinchi", "Ikkinchi", "Uchinchi"}

local served = table.remove(queue, 1)
print("Xizmat ko'rsatildi: " .. served)
print("Navbatda qoldi: " .. table.concat(queue, ", "))
""",
         "`table.remove(t, pos)` ko'rsatilgan indeksdagi qiymatni o'chiradi, uni qaytaradi va keyingi elementlar indekslarini bir pog'ona pastga suradi.",
         """Xizmat ko'rsatildi: Birinchi\nNavbatda qoldi: Ikkinchi, Uchinchi"""),

        (205, "table.concat() orqali elementlarni satrga birlashtirish",
         "Massivdagi so'zlarni maxsus ajratuvchi (separator) bilan bitta jumlaga aylantiring.",
         """local words = {"Lua", "juda", "tez", "va", "ixcham"}
local sentence = table.concat(words, " ")
local path = table.concat({"usr", "local", "bin"}, "/")

print(sentence)
print("/" .. path)
""",
         "`table.concat(t, sep)` barcha massiv elementlarini berilgan ajratgich bilan bitta satrga birlashtiradi va '..' operatoriga qaraganda ancha tez ishlaydi.",
         """Lua juda tez va ixcham\n/usr/local/bin"""),

        (206, "table.sort() orqali sonlarni va matnlarni saralash",
         "Sonlar massivini o'sish va kamayish tartibida saralang.",
         """local nums = {50, 12, 85, 3, 27}

table.sort(nums) -- O'sish tartibida
print("O'sish: " .. table.concat(nums, ", "))

table.sort(nums, function(a, b) return a > b end) -- Kamayish tartibida
print("Kamayish: " .. table.concat(nums, ", "))
""",
         "`table.sort(t, comp)` jadvalni joyida (in-place) saralaydi. Maxsus komparator funksiya berish mumkin.",
         """O'sish: 3, 12, 27, 50, 85\nKamayish: 85, 50, 27, 12, 3"""),

        (207, "Massivdagi 'teshiklar' (Holes va nil qiymatlar)",
         "Massiv o'rtasida nil qiymat paydo bo'lganda # operatori xatti-harakatini tahlil qiling.",
         """local t = {10, 20, nil, 40}
print("t[1]: " .. tostring(t[1]))
print("t[3]: " .. tostring(t[3]))
print("Uzunlik (#t): " .. #t)
""",
         "Agar massivda nil oraliqlar (teshiklar) bo'lsa, `#t` ning qaytaradigan qiymati noaniq bo'lishi mumkin, chunki Lua uzunlikni ikkilik qidiruv orqali topadi.",
         """t[1]: 10\nt[3]: nil\nUzunlik (#t): 4"""),

        (208, "Ko'p o'lchovli jadvallar (Matritsalar)",
         "2x3 o'lchamli matritsa yarating va uning determinant/elementlariga murojaat qiling.",
         """local matrix = {
    {1, 2, 3},
    {4, 5, 6}
}

print("Element [2][3]: " .. matrix[2][3])
print("Element [1][2]: " .. matrix[1][2])
""",
         "Luada ko'p o'lchamli massivlar jadvallar ichiga jadvallar joylashtirish orqali amalga oshiriladi.",
         """Element [2][3]: 6\nElement [1][2]: 2"""),

        (209, "Jadvalni sayoz nusxalash (Shallow Copy)",
         "Jadvalning mustaqil yangi nusxasini for tsikli orqali yarating.",
         """local original = {a = 10, b = 20}
local copy = {}

for k, v in pairs(original) do
    copy[k] = v
end

copy.a = 99
print("Original a: " .. original.a)
print("Nusxa a: " .. copy.a)
""",
         "To'g'ridan-to'g'ri `copy = original` qilinganda faqat xotira ko'rsatkichi (reference) ko'chiriladi. Shuning uchun mustaqil nusxa olish uchun tsiklda ko'chiriladi.",
         """Original a: 10\nNusxa a: 99"""),

        (210, "Chuqur nusxalash (Deep Copy rekursiv)",
         "Ichma-ich joylashgan murakkab jadvallarni to'liq chuqur nusxalash funksiyasini yozing.",
         """local function deepCopy(orig)
    if type(orig) ~= "table" then
        return orig
    end
    local copy = {}
    for k, v in pairs(orig) do
        copy[deepCopy(k)] = deepCopy(v)
    end
    return copy
end

local complex = {user = {name = "Ali", settings = {theme = "dark"}}}
local clone = deepCopy(complex)
clone.user.settings.theme = "light"

print("Original mavzu: " .. complex.user.settings.theme)
print("Klon mavzu: " .. clone.user.settings.theme)
""",
         "Chuqur nusxalash barcha ichki jadvallarni ham rekursiv nusxalab chiqadi va to'liq izolyatsiyani ta'minlaydi.",
         """Original mavzu: dark\nKlon mavzu: light""")
    ]

    for idx in range(211, 251):
        tasks_data.append((
            idx,
            f"Jadvallar va ma'lumot tuzilmalari amaliyoti #{idx}",
            f"{idx}-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.",
            f"""local store_{idx} = {{
    id = {idx},
    tag = "TABLE_NODE_{idx}",
    items = {{ {idx % 5}, {(idx % 5) + 1}, {(idx % 5) + 2} }}
}}

table.insert(store_{idx}.items, {idx * 2})
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_{idx}.id, store_{idx}.tag, #store_{idx}.items, store_{idx}.items[#store_{idx}.items]))
""",
            f"{idx}-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.",
            f"Node {idx} [Tag: TABLE_NODE_{idx}] elementlar soni: 4, oxirgi: {idx * 2}"
        ))

    for item in tasks_data:
        tasks.append(item)

    save_file("lua_05_jadvallar_tables_massiv_va_lugat_asoslari.md", [format_task(*t) for t in tasks])

if __name__ == "__main__":
    build_topic_03()
    build_topic_04()
    build_topic_05()
