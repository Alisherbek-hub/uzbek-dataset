# -*- coding: utf-8 -*-
"""
Generator for Lua Topics 02, 03, 04, 05 (Tasks 51 to 250)
19-til: Lua
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

def build_topic_02():
    tasks = []
    
    # 51..100
    tasks_data = [
        (51, "Oddiy if-then sharti",
         "O'yinchining tangalari soni yetarli bo'lganda yangi qurol xarid qilish imkonini tekshiring.",
         """local coins = 120
local swordCost = 100

if coins >= swordCost then
    print("Xarid muvaffaqiyatli amalga oshirildi! Qilich olindi.")
end
""",
         "Lua tilida shartli operator 'if <shart> then ... end' ko'rinishida yoziladi. Qavslar majburiy emas.",
         """Xarid muvaffaqiyatli amalga oshirildi! Qilich olindi."""),

        (52, "if-then-else to'liq tarmoqlanishi",
         "Foydalanuvchining yoshiga qarab kirish huquqini belgilang.",
         """local age = 16

if age >= 18 then
    print("Tizimga to'liq kirish ruxsat etildi.")
else
    print("Kechirasiz, yoshingiz 18 dan kichik. Kirish taqiqlangan.")
end
""",
         "Shart yolg'on (false yoki nil) bo'lsa, 'else' qismidagi ko'rsatmalar bajariladi.",
         """Kechirasiz, yoshingiz 18 dan kichik. Kirish taqiqlangan."""),

        (53, "if-then-elseif-else ko'p tarmoqli zanjiri",
         "Talabaning imtihon balliga qarab bahosini (A, B, C, F) aniqlang.",
         """local score = 84

if score >= 90 then
    print("Baho: A (A'lo)")
elseif score >= 80 then
    print("Baho: B (Yaxshi)")
elseif score >= 70 then
    print("Baho: C (Qoniqarli)")
else
    print("Baho: F (Qoniqarsiz)")
end
""",
         "Lua-da 'elseif' bitta so'z sifatida yoziladi (Python dagi elif yoki C dagi else if kabi).",
         """Baho: B (Yaxshi)"""),

        (54, "Ichma-ich shartli bloklar (Nested if)",
         "Foydalanuvchi tizimda ro'yxatdan o'tganligi va ikki bosqichli autentifikatsiyadan (2FA) o'tganligini tekshiring.",
         """local isAuthenticated = true
local has2FA = true

if isAuthenticated then
    if has2FA then
        print("Xavfsiz boshqaruv paneliga xush kelibsiz!")
    else
        print("Iltimos, 2FA kodini kiriting.")
    end
else
    print("Avval tizimga kiring.")
end
""",
         "Shartli bloklarni bir-birining ichiga istalgan chuqurlikda joylashtirish mumkin.",
         """Xavfsiz boshqaruv paneliga xush kelibsiz!"""),

        (55, "while tsikli asoslari",
         "1 dan 5 gacha bo'lgan sonlarni while tsikli yordamida ekranga chiqaring.",
         """local count = 1

while count <= 5 do
    print("Hisoblagich: " .. count)
    count = count + 1
end
""",
         "while tsikli shart true ekan, o'z tanasini qayta-qayta bajaradi. Har bir qadamda hisoblagichni oshirib borish lozim.",
         """Hisoblagich: 1\nHisoblagich: 2\nHisoblagich: 3\nHisoblagich: 4\nHisoblagich: 5"""),

        (56, "while tsiklida orqaga sanash (Countdown)",
         "Raketa uchirilishi oldidan 5 dan 1 gacha teskari sanang va 'Start!' deb xabar bering.",
         """local timer = 5

while timer > 0 do
    print("Uchirishga qoldi: " .. timer)
    timer = timer - 1
end

print("Start! Raketa fazoga ko'tarildi!")
""",
         "Teskari qadamli while tsikllarida shart belgilangan pastki chegaragacha kamayib boradi.",
         """Uchirishga qoldi: 5\nUchirishga qoldi: 4\nUchirishga qoldi: 3\nUchirishga qoldi: 2\nUchirishga qoldi: 1\nStart! Raketa fazoga ko'tarildi!"""),

        (57, "repeat-until tsikli (Post-condition)",
         "repeat-until tsikli yordamida kamida bir marta bajariladigan kod yozing.",
         """local attempts = 0

repeat
    attempts = attempts + 1
    print("Ulanish urinishi: #" .. attempts)
until attempts >= 3

print("Maksimal urinishlarga yetildi.")
""",
         "repeat-until tsikli shartni oxirida tekshiradi. Shuning uchun tana kamida 1 marta bajarilishi kafolatlanadi. 'until' sharti true bo'lganda tsikl to'xtaydi.",
         """Ulanish urinishi: #1\nUlanish urinishi: #2\nUlanish urinishi: #3\nMaksimal urinishlarga yetildi."""),

        (58, "repeat-until da o'zgaruvchilar ko'rinish doirasi",
         "repeat bloki ichida e'lon qilingan lokal o'zgaruvchining until shartida ko'rinishini isbotlang.",
         """local sum = 0

repeat
    local step = 10
    sum = sum + step
    print("Joriy yig'indi: " .. sum)
until step > 5 -- 'step' o'zgaruvchisi until shartida bemalol ko'rinadi!
""",
         "Lua tilining noyob xususiyati: repeat bloki ichida 'local' bilan e'lon qilingan o'zgaruvchi 'until' ifodasining o'zida ham amal qiladi.",
         """Joriy yig'indi: 10"""),

        (59, "Raqamli for tsikli: Standart qadam (step = 1)",
         "1 dan 4 gacha sonlarni va ularning kvadratlarini for tsiklida chiqaring.",
         """for i = 1, 4 do
    print(string.format("%d ning kvadrati: %d", i, i * i))
end
""",
         "Raqamli for sintaksisi: `for var = start, stop, step do ... end`. Agar `step` ko'rsatilmasa, standart ravishda 1 ga teng bo'ladi.",
         """1 ning kvadrati: 1\n2 ning kvadrati: 4\n3 ning kvadrati: 9\n4 ning kvadrati: 16"""),

        (60, "Raqamli for tsikli: Maxsus qadam (step = 2)",
         "2 dan 10 gacha bo'lgan juft sonlarni for tsiklida qadamni 2 qilib chiqaring.",
         """for i = 2, 10, 2 do
    print("Juft son: " .. i)
end
""",
         "Uchinchi parametr qadam miqdorini belgilaydi. Bu yerda i har safar 2 taga oshadi.",
         """Juft son: 2\nJuft son: 4\nJuft son: 6\nJuft son: 8\nJuft son: 10"""),

        (61, "Raqamli for tsikli: Manfiy qadam (Teskari sanash)",
         "10 dan 0 gacha 3 qadam bilan orqaga sanovchi dastur yozing.",
         """for i = 10, 0, -3 do
    print("Qiymat: " .. i)
end
""",
         "Manfiy qadamda tsikl hisoblagich ikkinchi parametrdan kichik bo'lib qolmaguncha davom etadi.",
         """Qiymat: 10\nQiymat: 7\nQiymat: 4\nQiymat: 1"""),

        (62, "for hisoblagichining xususiy lokal tabiati",
         "Tashqi o'zgaruvchi va for hisoblagichi bir xil nomga ega bo'lganda ularning mustaqilligini ko'rsating.",
         """local i = 999

for i = 1, 3 do
    print("Sikl ichida i: " .. i)
end

print("Sikl tugagach tashqi i: " .. i)
""",
         "for tsikli hisoblagichi avtomatik ravishda siklga tegishli alohida lokal o'zgaruvchi bo'lib, tashqi o'zgaruvchiga aslo daxl qilmaydi.",
         """Sikl ichida i: 1\nSikl ichida i: 2\nSikl ichida i: 3\nSikl tugagach tashqi i: 999"""),

        (63, "break operatori bilan tsiklni muddatidan oldin to'xtatish",
         "1 dan 100 gacha sonlar orasida birinchi bo'lib 7 ga va 5 ga bo'linuvchi musbat sonni topib tsiklni to'xtating.",
         """local target = nil

for i = 1, 100 do
    if i % 7 == 0 and i % 5 == 0 then
        target = i
        break -- Tsiklni to'xtatish
    end
end

print("Topilgan birinchi son: " .. target)
""",
         "'break' operatori eng yaqin tashqi tsiklni darhol to'xtatadi va boshqaruvni sikldan keyingi qatorga uzatadi.",
         """Topilgan birinchi son: 35"""),

        (64, "Ichma-ich tsikllardan chiqish",
         "2 o'lchamli qidiruvda kerakli nuqta topilganda bayroq (flag) orqali barcha tsikllardan chiqing.",
         """local found = false
local foundX, foundY = -1, -1

for x = 1, 5 do
    for y = 1, 5 do
        if x * y == 12 then
            foundX, foundY = x, y
            found = true
            break
        end
    end
    if found then
        break
    end
end

print(string.format("Topildi: x=%d, y=%d", foundX, foundY))
""",
         "Luada break faqat joriy sikldan chiqaradi. Tashqi siklni ham to'xtatish uchun mantiqiy bayroq yoki goto ishlatiladi.",
         """Topildi: x=3, y=4"""),

        (65, "goto va ::label:: teglari (Lua 5.2+)",
         "goto operatori yordamida xatolik yuz berganda tozalash kodiga sakrashni amalga oshiring.",
         """local status = "ERROR_TIMEOUT"

print("Jarayon boshlandi...")
if status == "ERROR_TIMEOUT" then
    goto cleanup
end

print("Bu qator bajarilmaydi")

::cleanup::
print("Resurslar tozalandi va xavfsiz yakunlandi.")
""",
         "Lua 5.2 versiyasida `goto label` va `::label::` sintaksisi qo'shildi. U leksik doira qoidalariga qat'iy bo'ysunadi.",
         """Jarayon boshlandi...\nResurslar tozalandi va xavfsiz yakunlandi."""),

        (66, "goto yordamida 'continue' operatorini simulyatsiya qilish",
         "Tsiklda faqat toq sonlarni chiqarish uchun juft sonlarda iteratsiyani o'tkazib yuboring.",
         """for i = 1, 6 do
    if i % 2 == 0 then
        goto continue
    end
    print("Toq son: " .. i)
    ::continue::
end
""",
         "Lua tilida tayyor 'continue' kalit so'zi yo'q. Tsikl oxiriga label qo'yib goto orqali continue funksionalligi yaratiladi.",
         """Toq son: 1\nToq son: 3\nToq son: 5"""),

        (67, "pairs() yordamida lug'atni (hash table) aylanib chiqish",
         "O'yinchining parametrlar jadvalidagi barcha kalit va qiymatlarni ekranga chiqaring.",
         """local stats = {
    mana = 250,
    speed = 14.5,
    rank = "Mayor",
    stamina = 100
}

for key, val in pairs(stats) do
    print(string.format("Kalit: %-8s -> Qiymat: %s", key, tostring(val)))
end
""",
         "`pairs()` iteratori jadvaldagi barcha elementlarni kalit-qiymat ko'rinishida aylanib chiqadi (tartib ixtiyoriy xesh tartibida bo'ladi).",
         """Kalit: mana     -> Qiymat: 250\nKalit: speed    -> Qiymat: 14.5\nKalit: rank     -> Qiymat: Mayor\nKalit: stamina  -> Qiymat: 100"""),

        (68, "ipairs() yordamida ketma-ket massivni aylanib chiqish",
         "Shaharlar ro'yxatini tartib raqami bilan birgalikda ekranga chiqaring.",
         """local cities = {"Samarqand", "Buxoro", "Xiva", "Toshkent"}

for index, cityName in ipairs(cities) do
    print(string.format("%d-shahar: %s", index, cityName))
end
""",
         "`ipairs()` faqat 1 dan boshlanuvchi ketma-ket butun sonli indekslar bo'yicha qat'iy tartibda aylanadi. Birinchi uchragan nil qiymatida to'xtaydi.",
         """1-shahar: Samarqand\n2-shahar: Buxoro\n3-shahar: Xiva\n4-shahar: Toshkent"""),

        (69, "Bo'sh jadval ustida tsiklning xatti-harakati",
         "Bo'sh jadval berilganda pairs va ipairs tsikllarining to'g'ri ishlashini tekshiring.",
         """local emptyTable = {}
local count = 0

for _ in pairs(emptyTable) do
    count = count + 1
end

print("Bo'sh jadvaldagi iteratsiyalar soni: " .. count)
""",
         "Bo'sh jadval ustida iteratsiya hech qachon ishga tushmaydi va xatoliksiz darhol yakunlanadi.",
         """Bo'sh jadvaldagi iteratsiyalar soni: 0"""),

        (70, "1 dan N gacha sonlar yig'indisini hisoblash",
         "1 dan 100 gacha sonlar yig'indisini for tsikli orqali hisoblang.",
         """local N = 100
local totalSum = 0

for i = 1, N do
    totalSum = totalSum + i
end

print(string.format("1 dan %d gacha yig'indi: %d", N, totalSum))
""",
         "Klassik arifmetik progressiya yig'indisi iterativ ravishda hisoblandi.",
         """1 dan 100 gacha yig'indi: 5050"""),

        (71, "Faktorialni iterativ hisoblash",
         "Berilgan 6 sonining faktorialini (6!) while tsikli orqali hisoblang.",
         """local n = 6
local fact = 1
local temp = n

while temp > 1 do
    fact = fact * temp
    temp = temp - 1
end

print(string.format("%d! faktoriali: %d", n, fact))
""",
         "Faktorial iterativ tsikl yordamida tezkor hisoblanadi va xotira stegi to'lib ketishidan saqlaydi.",
         """6! faktoriali: 720"""),

        (72, "Tub sonlarni aniqlash algoritmi",
         "Berilgan sonning tub (prime) ekanligini for tsikli orqali tekshiring.",
         """local function isPrime(num)
    if num <= 1 then return false end
    for i = 2, math.floor(math.sqrt(num)) do
        if num % i == 0 then
            return false
        end
    end
    return true
end

local testNum = 29
print(string.format("%d soni tubmi? %s", testNum, tostring(isPrime(testNum))))
""",
         "Tublikni tekshirishda bo'luvchilarni $\\sqrt{N}$ gacha tekshirish optimal hisoblash hisoblanadi.",
         """29 soni tubmi? true"""),

        (73, "Karra jadvalini chiqaruvchi ichma-ich for",
         "1 dan 3 gacha bo'lgan kichik karra jadvalini formatlab chiqaring.",
         """for i = 1, 3 do
    local row = ""
    for j = 1, 3 do
        row = row .. string.format("%d x %d = %d\\t", i, j, i * j)
    end
    print(row)
end
""",
         "Ichma-ich tsikllar matritsalar va ko'p o'lchamli hisob-kitoblarni amalga oshirishda asosiy vositadir.",
         """1 x 1 = 1\t1 x 2 = 2\t1 x 3 = 3\t\n2 x 1 = 2\t2 x 2 = 4\t2 x 3 = 6\t\n3 x 1 = 3\t3 x 2 = 6\t3 x 3 = 9\t"""),

        (74, "Fibonacci ketma-ketligini generatsiya qilish",
         "Dastlabki 8 ta Fibonacci sonini tsikl yordamida toping.",
         """local a, b = 0, 1
local result = {}

for _ = 1, 8 do
    table.insert(result, a)
    a, b = b, a + b
end

print("Fibonacci ketma-ketligi: " .. table.concat(result, ", "))
""",
         "Lua-dagi ko'p qiymatli o'zlashtirish `a, b = b, a + b` Fibonachchi hisoblashni juda qulay qiladi.",
         """Fibonacci ketma-ketligi: 0, 1, 1, 2, 3, 5, 8, 13"""),

        (75, "Massivdagi eng katta va eng kichik qiymatni topish",
         "Ro'yxatdagi min va max qiymatlarni bitta tsiklda aniqlang.",
         """local numbers = {45, 12, 89, 3, 67, 104, 23}

local minVal = numbers[1]
local maxVal = numbers[1]

for i = 2, #numbers do
    if numbers[i] < minVal then minVal = numbers[i] end
    if numbers[i] > maxVal then maxVal = numbers[i] end
end

print("Minimal qiymat: " .. minVal)
print("Maksimal qiymat: " .. maxVal)
""",
         "Massivdagi ekstremum qiymatlar $O(N)$ chiziqli murakkablikda topiladi.",
         """Minimal qiymat: 3\nMaksimal qiymat: 104"""),

        (76, "Massiv elementlarini teskari o'girish (Reverse in-place)",
         "Qo'shimcha massiv ochmasdan mavjud massivni joyida teskari qiling.",
         """local arr = {10, 20, 30, 40, 50}
local len = #arr

for i = 1, len // 2 do
    arr[i], arr[len - i + 1] = arr[len - i + 1], arr[i]
end

print("Teskari massiv: " .. table.concat(arr, ", "))
""",
         "Ikkala tomondan o'rtaga qarab elementlarni swap qilish xotirani tejaydi.",
         """Teskari massiv: 50, 40, 30, 20, 10"""),

        (77, "Palindrom satrni tekshirish",
         "Berilgan so'zning chapdan va o'ngdan bir xil o'qilishini tsikl orqali tekshiring.",
         """local function isPalindrome(str)
    local len = #str
    for i = 1, len // 2 do
        if string.sub(str, i, i) ~= string.sub(str, len - i + 1, len - i + 1) then
            return false
        end
    end
    return true
end

local word1 = "kiyik"
local word2 = "kitob"

print(word1 .. " palindrommi? " .. tostring(isPalindrome(word1)))
print(word2 .. " palindrommi? " .. tostring(isPalindrome(word2)))
""",
         "`string.sub(str, i, i)` orqali bittalik belgi olinadi va taqqoslanadi.",
         """kiyik palindrommi? true\nkitob palindrommi? false"""),

        (78, "Sonning raqamlari yig'indisini hisoblash",
         "Butun sonning barcha raqamlari yig'indisini while tsikli yordamida toping.",
         """local num = 9845
local temp = num
local sum = 0

while temp > 0 do
    sum = sum + (temp % 10)
    temp = temp // 10
end

print(string.format("%d ning raqamlar yig'indisi: %d", num, sum))
""",
         "Modul 10 oxirgi raqamni ajratadi, butun bo'lish (// 10) esa uni o'chiradi.",
         """9845 ning raqamlar yig'indisi: 26"""),

        (79, "Matndagi unli harflarni sanash",
         "O'zbek tilidagi unli harflar sonini for tsiklida sanang.",
         """local text = "Al-Xorazmiy algoritmlar asoschisi"
local vowels = {a=true, e=true, i=true, o=true, u=true}
local count = 0

for i = 1, #text do
    local char = string.lower(string.sub(text, i, i))
    if vowels[char] then
        count = count + 1
    end
end

print("Jami unli harflar: " .. count)
""",
         "Jadvalda xesh-qidiruv $O(1)$ bo'lgani sababli unli harflarni tekshirish juda tez ishlaydi.",
         """Jami unli harflar: 11"""),

        (80, "Chiziqli qidiruv (Linear Search)",
         "Massivda qidirilayotgan qiymatning birinchi uchragan indeksini toping.",
         """local items = {"olma", "anor", "anjir", "uzum", "shaftoli"}
local target = "uzum"
local foundIdx = -1

for i = 1, #items do
    if items[i] == target then
        foundIdx = i
        break
    end
end

print(string.format("'%s' indeksi: %d", target, foundIdx))
""",
         "Chiziqli qidiruv saralanmagan ro'yxatlarda maqsadli elementni ketma-ket taqqoslaydi.",
         """'uzum' indeksi: 4"""),

        (81, "Ikkilik qidiruv (Binary Search)",
         "Saralangan massivda logarifmik vaqtda $O(\\log N)$ elementni toping.",
         """local sorted = {11, 23, 35, 47, 59, 71, 83, 95}
local target = 71
local low, high = 1, #sorted
local foundIdx = -1

while low <= high do
    local mid = (low + high) // 2
    if sorted[mid] == target then
        foundIdx = mid
        break
    elseif sorted[mid] < target then
        low = mid + 1
    else
        high = mid - 1
    end
end

print(string.format("%d soni indeksi: %d", target, foundIdx))
""",
         "Ikkilik qidiruv har qadamda qidiruv sohasini 2 barobar qisqartiradi.",
         """71 soni indeksi: 6"""),

        (82, "Pufakchali saralash (Bubble Sort)",
         "Klassik pufakchali saralash algoritmini Luada amalga oshiring.",
         """local arr = {64, 34, 25, 12, 22, 11, 90}
local n = #arr

for i = 1, n do
    for j = 1, n - i do
        if arr[j] > arr[j + 1] then
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
        end
    end
end

print("Saralangan massiv: " .. table.concat(arr, ", "))
""",
         "Bubble Sort ketma-ket qo'shni elementlarni taqqoslab, kattalarini oxiriga 'qalqitadi'.",
         """Saralangan massiv: 11, 12, 22, 25, 34, 64, 90"""),

        (83, "Tanlash orqali saralash (Selection Sort)",
         "Eng kichik elementni topib boshiga joylashtiruvchi saralash algoritmi.",
         """local arr = {29, 10, 14, 37, 13}
local n = #arr

for i = 1, n - 1 do
    local minIdx = i
    for j = i + 1, n do
        if arr[j] < arr[minIdx] then
            minIdx = j
        end
    end
    if minIdx ~= i then
        arr[i], arr[minIdx] = arr[minIdx], arr[i]
    end
end

print("Selection sort natijasi: " .. table.concat(arr, ", "))
""",
         "Selection Sort har bir tashqi iteratsiyada qolgan qismning minimalini topadi.",
         """Selection sort natijasi: 10, 13, 14, 29, 37"""),

        (84, "Kiritish orqali saralash (Insertion Sort)",
         "Kartalarni tartiblash kabi har bir elementni o'z o'rniga joylashtiruvchi algoritm.",
         """local arr = {12, 11, 13, 5, 6}

for i = 2, #arr do
    local key = arr[i]
    local j = i - 1
    while j >= 1 and arr[j] > key do
        arr[j + 1] = arr[j]
        j = j - 1
    end
    arr[j + 1] = key
end

print("Insertion sort natijasi: " .. table.concat(arr, ", "))
""",
         "Insertion Sort kichik yoki qisman saralangan massivlarda juda yuqori samaradorlik ko'rsatadi.",
         """Insertion sort natijasi: 5, 6, 11, 12, 13"""),

        (85, "O'yin xaritasi koordinatalarini aylanib chiqish (Grid traversal)",
         "3x3 o'lchamli katakchalarning (x, y) koordinatalari bo'yicha navigatsiya.",
         """local width, height = 3, 3

for y = 1, height do
    local line = ""
    for x = 1, width do
        line = line .. string.format("[%d,%d] ", x, y)
    end
    print(line)
end
""",
         "2D o'yinlarda xarita plitkalari (tiles) aynan shu tartibda ekranga render qilinadi.",
         """[1,1] [2,1] [3,1] \n[1,2] [2,2] [3,2] \n[1,3] [2,3] [3,3] """),

        (86, "Massiv elementlarini tsiklda filtrlash",
         "Berilgan ro'yxatdan faqat musbat sonlarni ajratib oluvchi yangi massiv yarating.",
         """local rawData = {-5, 12, 0, -3, 44, 98, -17}
local positiveData = {}

for _, val in ipairs(rawData) do
    if val > 0 then
        table.insert(positiveData, val)
    end
end

print("Filtrlangan musbat sonlar: " .. table.concat(positiveData, ", "))
""",
         "Filtrlash jarayonida yangi jadvalga `table.insert()` orqali shartga mos qiymatlar to'planadi.",
         """Filtrlangan musbat sonlar: 12, 44, 98"""),

        (87, "Massiv yig'indisi va o'rtacha arifmetik qiymati",
         "O'quvchilar baholarining umumiy yig'indisi va o'rtachasini toping.",
         """local grades = {85, 90, 78, 92, 88}
local sum = 0

for _, grade in ipairs(grades) do
    sum = sum + grade
end

local average = sum / #grades
print("Jami ball: " .. sum)
print(string.format("O'rtacha baho: %.2f", average))
""",
         "Massiv uzunligi `#` operatori orqali olinadi va o'rtacha qiymat float sifatida hisoblanadi.",
         """Jami ball: 443\nO'rtacha baho: 88.60"""),

        (88, "repeat-until orqali validatsiya simulyatsiyasi",
         "To'g'ri PIN kod kiritilgunga qadar takrorlanuvchi jarayonni simulyatsiya qiling.",
         """local SECRET_PIN = 4422
local mockInputs = {1111, 2222, 4422}
local idx = 1
local enteredPin = nil

repeat
    enteredPin = mockInputs[idx]
    print("Tekshirilmoqda: " .. enteredPin)
    idx = idx + 1
until enteredPin == SECRET_PIN

print("PIN kod to'g'ri! Tizimga ruxsat berildi.")
""",
         "repeat-until shart to'g'ri bo'lmaguncha jarayonni ushlab turish uchun juda mos keladi.",
         """Tekshirilmoqda: 1111\nTekshirilmoqda: 2222\nTekshirilmoqda: 4422\nPIN kod to'g'ri! Tizimga ruxsat berildi."""),

        (89, "Ko'p shartli tekshiruvlar (and, or aralashmasi)",
         "VIP foydalanuvchilar yoki chipta sotib olgan faol obunachilarga kirish ruxsatini bering.",
         """local isVIP = false
local hasTicket = true
local isBanned = false

if not isBanned and (isVIP or hasTicket) then
    print("Muzeyga kirish ruxsati berildi.")
else
    print("Kirish taqiqlandi.")
end
""",
         "Mantiqiy ifodalarda qavslar amallar ustuvorligini boshqarish va xatoliklarning oldini olish uchun zarur.",
         """Muzeyga kirish ruxsati berildi."""),

        (90, "Dinamik o'zgaruvchi qadamli tsikl simulyatsiyasi",
         "Har bir iteratsiyada qadami ikki baravar ortuvchi eksponensial tsikl tuzing.",
         """local current = 1
local step = 1

while current <= 50 do
    print(string.format("Qiymat: %d (Qadam: %d)", current, step))
    current = current + step
    step = step * 2
end
""",
         "Raqamli for tsiklida qadam o'zgarmasdir, biroq while tsikli yordamida o'zgaruvchan qadamli jarayonlarni boshqarish mumkin.",
         """Qiymat: 1 (Qadam: 1)\nQiymat: 2 (Qadam: 2)\nQiymat: 6 (Qadam: 4)\nQiymat: 14 (Qadam: 8)\nQiymat: 30 (Qadam: 16)"""),

        (91, "Cheksiz tsikllardan xavfsiz himoyalanish",
         "while tsikliga xavfsizlik cheklovi (Safety Guard Counter) o'rnating.",
         """local counter = 0
local MAX_SAFE_STEPS = 5

while true do
    counter = counter + 1
    print("Xavfsiz qadam: " .. counter)
    if counter >= MAX_SAFE_STEPS then
        print("Xavfsizlik chegarasiga yetildi, sikl to'xtatildi.")
        break
    end
end
""",
         "Tizim osilib qolishining oldini olish uchun cheksiz tsikllarda maksimal chegara hisoblagichi o'rnatiladi.",
         """Xavfsiz qadam: 1\nXavfsiz qadam: 2\nXavfsiz qadam: 3\nXavfsiz qadam: 4\nXavfsiz qadam: 5\nXavfsizlik chegarasiga yetildi, sikl to'xtatildi."""),

        (92, "O'yin hayotiy sikli simulyatsiyasi (Game Loop Tick)",
         "3 ta kadr davomida fizika va render funksiyalarini bajaruvchi sikl yozing.",
         """local totalFrames = 3

for frame = 1, totalFrames do
    print(string.format("--- Kadr #%d ---", frame))
    print("1. O'yinchilar harakati hisoblandi")
    print("2. To'qnashuvlar tekshirildi")
    print("3. Ekran yangilandi (Render)")
end
""",
         "O'yin dvijoklarida (masalan, Roblox yoki LÖVE) asosiy tsikl kadrlar bo'yicha uzluksiz yangilanadi.",
         """--- Kadr #1 ---\n1. O'yinchilar harakati hisoblandi\n2. To'qnashuvlar tekshirildi\n3. Ekran yangilandi (Render)\n--- Kadr #2 ---\n1. O'yinchilar harakati hisoblandi\n2. To'qnashuvlar tekshirildi\n3. Ekran yangilandi (Render)\n--- Kadr #3 ---\n1. O'yinchilar harakati hisoblandi\n2. To'qnashuvlar tekshirildi\n3. Ekran yangilandi (Render)"""),

        (93, "Buyruqlar komandasi (Command dispatch table)",
         "Shartli ifodalarning o'rniga jadvalli dispatch yordamida harakatlarni bajaring.",
         """local commands = {
    attack = function() print("Qahramon qilich bilan zarba berdi!") end,
    defend = function() print("Qahramon qalqonni ko'tardi!") end,
    heal = function() print("Salomatlik 25 birlikka tiklandi!") end
}

local action = "heal"
if commands[action] then
    commands[action]()
else
    print("Noma'lum buyruq!")
end
""",
         "Lua jadvallari funksiyalarni saqlay oladi, bu esa uzun if-else zanjirlarini chiroyli qisqartiradi.",
         """Salomatlik 25 birlikka tiklandi!"""),

        (94, "Shaxmat taxtasi simulyatsiyasi (8x8 shartli matritsa)",
         "Katakchaning oq yoki qora ekanligini (x + y) % 2 orqali aniqlang.",
         """local function getSquareColor(row, col)
    return ((row + col) % 2 == 0) and "OQ" or "QORA"
end

print("A1 (1,1): " .. getSquareColor(1, 1))
print("A2 (1,2): " .. getSquareColor(1, 2))
print("B2 (2,2): " .. getSquareColor(2, 2))
""",
         "Shaxmat taxtasida koordinatalar yig'indisining juft-toqligi katakcha rangini belgilaydi.",
         """A1 (1,1): OQ\nA2 (1,2): QORA\nB2 (2,2): OQ"""),

        (95, "Paskal uchburchagining dastlabki 4 qatorini generatsiya qilish",
         "Kombinatorik hisoblar uchun Paskal uchburchagi qatorlarini hosil qiling.",
         """local triangle = {}
local numRows = 4

for i = 1, numRows do
    triangle[i] = {}
    triangle[i][1] = 1
    triangle[i][i] = 1
    for j = 2, i - 1 do
        triangle[i][j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
    end
    print(table.concat(triangle[i], " "))
end
""",
         "Paskal uchburchagida har bir ichki son o'zidan yuqoridagi ikkita sonning yig'indisiga tengdir.",
         """1\n1 1\n1 2 1\n1 3 3 1"""),

        (96, "Tsikllarda xotirani nazorat qilish va bo'shatish",
         "Tsikl davomida yaratilgan vaqtinchalik jadvallarni xotiradan tozalash.",
         """for i = 1, 3 do
    local tempData = {id = i, payload = string.rep("X", 100)}
    print(string.format("Vaqtinchalik paket #%d qayta ishlandi", tempData.id))
    tempData = nil -- Xotirada Garbage Collectorga tayyorlash
end
print("Barcha paketlar yakunlandi.")
""",
         "Lokal o'zgaruvchilar siklning har bir qadamida qayta yaratiladi va qadam tugashi bilan yaroqsiz bo'ladi.",
         """Vaqtinchalik paket #1 qayta ishlandi\nVaqtinchalik paket #2 qayta ishlandi\nVaqtinchalik paket #3 qayta ishlandi\nBarcha paketlar yakunlandi."""),

        (97, "for tsikli chegaralarining faqat bir marta hisoblanishi",
         "for tsikli boshlanishida funksiya chaqirilib, faqat bir marta hisoblanishini isbotlang.",
         """local calls = 0
local function getLimit()
    calls = calls + 1
    return 3
end

for i = 1, getLimit() do
    -- Tsikl tanasi
end

print("getLimit() necha marta chaqirildi? " .. calls)
""",
         "Lua tili for tsiklining start, stop va step ifodalarini faqat bitta marta tsikl boshlanishida hisoblab saqlab qo'yadi.",
         """getLimit() necha marta chaqirildi? 1"""),

        (98, "Satrdagi so'zlarni tsiklda ajratish",
         "Matn ichidagi so'zlarni bo'shliqlar bo'yicha for tsiklida ajrating.",
         """local sentence = "Assalomu alaykum aziz dasturchilar"
local words = {}

for word in string.gmatch(sentence, "%S+") do
    table.insert(words, word)
end

print("So'zlar soni: " .. #words)
print("Ikkinchi so'z: " .. words[2])
""",
         "`string.gmatch` Luadagi maxsus iterator bo'lib, generic for tsikli bilan mukammal ishlaydi.",
         """So'zlar soni: 4\nIkkinchi so'z: alaykum"""),

        (99, "Shartli holat mashinasi (State Machine) tsikli",
         "O'yin qahramonining holatlarini (IDLE -> RUN -> ATTACK) boshqaring.",
         """local states = {"IDLE", "RUN", "ATTACK"}

for _, state in ipairs(states) do
    if state == "IDLE" then
        print("[HOLAT] Qahramon tinch turibdi")
    elseif state == "RUN" then
        print("[HOLAT] Qahramon nishon tomon yugurmoqda")
    elseif state == "ATTACK" then
        print("[HOLAT] Qahramon dushmanga hujum qildi")
    end
end
""",
         "Holatlar mashinasi sun'iy intellekt va o'yin personajlarining xatti-harakatini boshqarishda poydevor hisoblanadi.",
         """[HOLAT] Qahramon tinch turibdi\n[HOLAT] Qahramon nishon tomon yugurmoqda\n[HOLAT] Qahramon dushmanga hujum qildi"""),

        (100, "Kompleks jang tizimi simulyatsiyasi",
         "Qahramon va maxluq o'rtasidagi to'liq navbatma-navbat jang jarayonini tsikl orqali modellashtiring.",
         """local heroHP = 60
local monsterHP = 50
local round = 1

while heroHP > 0 and monsterHP > 0 do
    monsterHP = monsterHP - 20
    if monsterHP <= 0 then
        print(string.format("Raund %d: Qahramon zarba berdi. Maxluq mag'lub bo'ldi!", round))
        break
    end
    heroHP = heroHP - 15
    print(string.format("Raund %d: Qahramon HP=%d, Maxluq HP=%d", round, heroHP, monsterHP))
    round = round + 1
end

print("Jang yakunlandi! Qahramon g'alaba qozondi.")
""",
         "Barcha boshqaruv oqimlari (while, if, break, string.format) uyg'unlikda to'liq jang tizimini amalga oshirdi.",
         """Raund 1: Qahramon HP=45, Maxluq HP=30\nRaund 2: Qahramon HP=30, Maxluq HP=10\nRaund 3: Qahramon zarba berdi. Maxluq mag'lub bo'ldi!\nJang yakunlandi! Qahramon g'alaba qozondi.""")
    ]

    for item in tasks_data:
        tasks.append(item)

    save_file("lua_02_boshqaruv_oqimlari_shartlar_va_tsikllar.md", [format_task(*t) for t in tasks])

if __name__ == "__main__":
    build_topic_02()
