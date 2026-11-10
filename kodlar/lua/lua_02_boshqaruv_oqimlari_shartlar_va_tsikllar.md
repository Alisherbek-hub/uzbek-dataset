# 51-Topshiriq: Oddiy if-then sharti
## Topshiriq sharti:
O'yinchining tangalari soni yetarli bo'lganda yangi qurol xarid qilish imkonini tekshiring.

## Yechim (Lua kodi):
```lua
local coins = 120
local swordCost = 100

if coins >= swordCost then
    print("Xarid muvaffaqiyatli amalga oshirildi! Qilich olindi.")
end
```

## Tushuntirish va Mantiq:
Lua tilida shartli operator 'if <shart> then ... end' ko'rinishida yoziladi. Qavslar majburiy emas.

## Ishlash natijasi:
```text
Xarid muvaffaqiyatli amalga oshirildi! Qilich olindi.
```


# 52-Topshiriq: if-then-else to'liq tarmoqlanishi
## Topshiriq sharti:
Foydalanuvchining yoshiga qarab kirish huquqini belgilang.

## Yechim (Lua kodi):
```lua
local age = 16

if age >= 18 then
    print("Tizimga to'liq kirish ruxsat etildi.")
else
    print("Kechirasiz, yoshingiz 18 dan kichik. Kirish taqiqlangan.")
end
```

## Tushuntirish va Mantiq:
Shart yolg'on (false yoki nil) bo'lsa, 'else' qismidagi ko'rsatmalar bajariladi.

## Ishlash natijasi:
```text
Kechirasiz, yoshingiz 18 dan kichik. Kirish taqiqlangan.
```


# 53-Topshiriq: if-then-elseif-else ko'p tarmoqli zanjiri
## Topshiriq sharti:
Talabaning imtihon balliga qarab bahosini (A, B, C, F) aniqlang.

## Yechim (Lua kodi):
```lua
local score = 84

if score >= 90 then
    print("Baho: A (A'lo)")
elseif score >= 80 then
    print("Baho: B (Yaxshi)")
elseif score >= 70 then
    print("Baho: C (Qoniqarli)")
else
    print("Baho: F (Qoniqarsiz)")
end
```

## Tushuntirish va Mantiq:
Lua-da 'elseif' bitta so'z sifatida yoziladi (Python dagi elif yoki C dagi else if kabi).

## Ishlash natijasi:
```text
Baho: B (Yaxshi)
```


# 54-Topshiriq: Ichma-ich shartli bloklar (Nested if)
## Topshiriq sharti:
Foydalanuvchi tizimda ro'yxatdan o'tganligi va ikki bosqichli autentifikatsiyadan (2FA) o'tganligini tekshiring.

## Yechim (Lua kodi):
```lua
local isAuthenticated = true
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
```

## Tushuntirish va Mantiq:
Shartli bloklarni bir-birining ichiga istalgan chuqurlikda joylashtirish mumkin.

## Ishlash natijasi:
```text
Xavfsiz boshqaruv paneliga xush kelibsiz!
```


# 55-Topshiriq: while tsikli asoslari
## Topshiriq sharti:
1 dan 5 gacha bo'lgan sonlarni while tsikli yordamida ekranga chiqaring.

## Yechim (Lua kodi):
```lua
local count = 1

while count <= 5 do
    print("Hisoblagich: " .. count)
    count = count + 1
end
```

## Tushuntirish va Mantiq:
while tsikli shart true ekan, o'z tanasini qayta-qayta bajaradi. Har bir qadamda hisoblagichni oshirib borish lozim.

## Ishlash natijasi:
```text
Hisoblagich: 1
Hisoblagich: 2
Hisoblagich: 3
Hisoblagich: 4
Hisoblagich: 5
```


# 56-Topshiriq: while tsiklida orqaga sanash (Countdown)
## Topshiriq sharti:
Raketa uchirilishi oldidan 5 dan 1 gacha teskari sanang va 'Start!' deb xabar bering.

## Yechim (Lua kodi):
```lua
local timer = 5

while timer > 0 do
    print("Uchirishga qoldi: " .. timer)
    timer = timer - 1
end

print("Start! Raketa fazoga ko'tarildi!")
```

## Tushuntirish va Mantiq:
Teskari qadamli while tsikllarida shart belgilangan pastki chegaragacha kamayib boradi.

## Ishlash natijasi:
```text
Uchirishga qoldi: 5
Uchirishga qoldi: 4
Uchirishga qoldi: 3
Uchirishga qoldi: 2
Uchirishga qoldi: 1
Start! Raketa fazoga ko'tarildi!
```


# 57-Topshiriq: repeat-until tsikli (Post-condition)
## Topshiriq sharti:
repeat-until tsikli yordamida kamida bir marta bajariladigan kod yozing.

## Yechim (Lua kodi):
```lua
local attempts = 0

repeat
    attempts = attempts + 1
    print("Ulanish urinishi: #" .. attempts)
until attempts >= 3

print("Maksimal urinishlarga yetildi.")
```

## Tushuntirish va Mantiq:
repeat-until tsikli shartni oxirida tekshiradi. Shuning uchun tana kamida 1 marta bajarilishi kafolatlanadi. 'until' sharti true bo'lganda tsikl to'xtaydi.

## Ishlash natijasi:
```text
Ulanish urinishi: #1
Ulanish urinishi: #2
Ulanish urinishi: #3
Maksimal urinishlarga yetildi.
```


# 58-Topshiriq: repeat-until da o'zgaruvchilar ko'rinish doirasi
## Topshiriq sharti:
repeat bloki ichida e'lon qilingan lokal o'zgaruvchining until shartida ko'rinishini isbotlang.

## Yechim (Lua kodi):
```lua
local sum = 0

repeat
    local step = 10
    sum = sum + step
    print("Joriy yig'indi: " .. sum)
until step > 5 -- 'step' o'zgaruvchisi until shartida bemalol ko'rinadi!
```

## Tushuntirish va Mantiq:
Lua tilining noyob xususiyati: repeat bloki ichida 'local' bilan e'lon qilingan o'zgaruvchi 'until' ifodasining o'zida ham amal qiladi.

## Ishlash natijasi:
```text
Joriy yig'indi: 10
```


# 59-Topshiriq: Raqamli for tsikli: Standart qadam (step = 1)
## Topshiriq sharti:
1 dan 4 gacha sonlarni va ularning kvadratlarini for tsiklida chiqaring.

## Yechim (Lua kodi):
```lua
for i = 1, 4 do
    print(string.format("%d ning kvadrati: %d", i, i * i))
end
```

## Tushuntirish va Mantiq:
Raqamli for sintaksisi: `for var = start, stop, step do ... end`. Agar `step` ko'rsatilmasa, standart ravishda 1 ga teng bo'ladi.

## Ishlash natijasi:
```text
1 ning kvadrati: 1
2 ning kvadrati: 4
3 ning kvadrati: 9
4 ning kvadrati: 16
```


# 60-Topshiriq: Raqamli for tsikli: Maxsus qadam (step = 2)
## Topshiriq sharti:
2 dan 10 gacha bo'lgan juft sonlarni for tsiklida qadamni 2 qilib chiqaring.

## Yechim (Lua kodi):
```lua
for i = 2, 10, 2 do
    print("Juft son: " .. i)
end
```

## Tushuntirish va Mantiq:
Uchinchi parametr qadam miqdorini belgilaydi. Bu yerda i har safar 2 taga oshadi.

## Ishlash natijasi:
```text
Juft son: 2
Juft son: 4
Juft son: 6
Juft son: 8
Juft son: 10
```


# 61-Topshiriq: Raqamli for tsikli: Manfiy qadam (Teskari sanash)
## Topshiriq sharti:
10 dan 0 gacha 3 qadam bilan orqaga sanovchi dastur yozing.

## Yechim (Lua kodi):
```lua
for i = 10, 0, -3 do
    print("Qiymat: " .. i)
end
```

## Tushuntirish va Mantiq:
Manfiy qadamda tsikl hisoblagich ikkinchi parametrdan kichik bo'lib qolmaguncha davom etadi.

## Ishlash natijasi:
```text
Qiymat: 10
Qiymat: 7
Qiymat: 4
Qiymat: 1
```


# 62-Topshiriq: for hisoblagichining xususiy lokal tabiati
## Topshiriq sharti:
Tashqi o'zgaruvchi va for hisoblagichi bir xil nomga ega bo'lganda ularning mustaqilligini ko'rsating.

## Yechim (Lua kodi):
```lua
local i = 999

for i = 1, 3 do
    print("Sikl ichida i: " .. i)
end

print("Sikl tugagach tashqi i: " .. i)
```

## Tushuntirish va Mantiq:
for tsikli hisoblagichi avtomatik ravishda siklga tegishli alohida lokal o'zgaruvchi bo'lib, tashqi o'zgaruvchiga aslo daxl qilmaydi.

## Ishlash natijasi:
```text
Sikl ichida i: 1
Sikl ichida i: 2
Sikl ichida i: 3
Sikl tugagach tashqi i: 999
```


# 63-Topshiriq: break operatori bilan tsiklni muddatidan oldin to'xtatish
## Topshiriq sharti:
1 dan 100 gacha sonlar orasida birinchi bo'lib 7 ga va 5 ga bo'linuvchi musbat sonni topib tsiklni to'xtating.

## Yechim (Lua kodi):
```lua
local target = nil

for i = 1, 100 do
    if i % 7 == 0 and i % 5 == 0 then
        target = i
        break -- Tsiklni to'xtatish
    end
end

print("Topilgan birinchi son: " .. target)
```

## Tushuntirish va Mantiq:
'break' operatori eng yaqin tashqi tsiklni darhol to'xtatadi va boshqaruvni sikldan keyingi qatorga uzatadi.

## Ishlash natijasi:
```text
Topilgan birinchi son: 35
```


# 64-Topshiriq: Ichma-ich tsikllardan chiqish
## Topshiriq sharti:
2 o'lchamli qidiruvda kerakli nuqta topilganda bayroq (flag) orqali barcha tsikllardan chiqing.

## Yechim (Lua kodi):
```lua
local found = false
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
```

## Tushuntirish va Mantiq:
Luada break faqat joriy sikldan chiqaradi. Tashqi siklni ham to'xtatish uchun mantiqiy bayroq yoki goto ishlatiladi.

## Ishlash natijasi:
```text
Topildi: x=3, y=4
```


# 65-Topshiriq: goto va ::label:: teglari (Lua 5.2+)
## Topshiriq sharti:
goto operatori yordamida xatolik yuz berganda tozalash kodiga sakrashni amalga oshiring.

## Yechim (Lua kodi):
```lua
local status = "ERROR_TIMEOUT"

print("Jarayon boshlandi...")
if status == "ERROR_TIMEOUT" then
    goto cleanup
end

print("Bu qator bajarilmaydi")

::cleanup::
print("Resurslar tozalandi va xavfsiz yakunlandi.")
```

## Tushuntirish va Mantiq:
Lua 5.2 versiyasida `goto label` va `::label::` sintaksisi qo'shildi. U leksik doira qoidalariga qat'iy bo'ysunadi.

## Ishlash natijasi:
```text
Jarayon boshlandi...
Resurslar tozalandi va xavfsiz yakunlandi.
```


# 66-Topshiriq: goto yordamida 'continue' operatorini simulyatsiya qilish
## Topshiriq sharti:
Tsiklda faqat toq sonlarni chiqarish uchun juft sonlarda iteratsiyani o'tkazib yuboring.

## Yechim (Lua kodi):
```lua
for i = 1, 6 do
    if i % 2 == 0 then
        goto continue
    end
    print("Toq son: " .. i)
    ::continue::
end
```

## Tushuntirish va Mantiq:
Lua tilida tayyor 'continue' kalit so'zi yo'q. Tsikl oxiriga label qo'yib goto orqali continue funksionalligi yaratiladi.

## Ishlash natijasi:
```text
Toq son: 1
Toq son: 3
Toq son: 5
```


# 67-Topshiriq: pairs() yordamida lug'atni (hash table) aylanib chiqish
## Topshiriq sharti:
O'yinchining parametrlar jadvalidagi barcha kalit va qiymatlarni ekranga chiqaring.

## Yechim (Lua kodi):
```lua
local stats = {
    mana = 250,
    speed = 14.5,
    rank = "Mayor",
    stamina = 100
}

for key, val in pairs(stats) do
    print(string.format("Kalit: %-8s -> Qiymat: %s", key, tostring(val)))
end
```

## Tushuntirish va Mantiq:
`pairs()` iteratori jadvaldagi barcha elementlarni kalit-qiymat ko'rinishida aylanib chiqadi (tartib ixtiyoriy xesh tartibida bo'ladi).

## Ishlash natijasi:
```text
Kalit: mana     -> Qiymat: 250
Kalit: speed    -> Qiymat: 14.5
Kalit: rank     -> Qiymat: Mayor
Kalit: stamina  -> Qiymat: 100
```


# 68-Topshiriq: ipairs() yordamida ketma-ket massivni aylanib chiqish
## Topshiriq sharti:
Shaharlar ro'yxatini tartib raqami bilan birgalikda ekranga chiqaring.

## Yechim (Lua kodi):
```lua
local cities = {"Samarqand", "Buxoro", "Xiva", "Toshkent"}

for index, cityName in ipairs(cities) do
    print(string.format("%d-shahar: %s", index, cityName))
end
```

## Tushuntirish va Mantiq:
`ipairs()` faqat 1 dan boshlanuvchi ketma-ket butun sonli indekslar bo'yicha qat'iy tartibda aylanadi. Birinchi uchragan nil qiymatida to'xtaydi.

## Ishlash natijasi:
```text
1-shahar: Samarqand
2-shahar: Buxoro
3-shahar: Xiva
4-shahar: Toshkent
```


# 69-Topshiriq: Bo'sh jadval ustida tsiklning xatti-harakati
## Topshiriq sharti:
Bo'sh jadval berilganda pairs va ipairs tsikllarining to'g'ri ishlashini tekshiring.

## Yechim (Lua kodi):
```lua
local emptyTable = {}
local count = 0

for _ in pairs(emptyTable) do
    count = count + 1
end

print("Bo'sh jadvaldagi iteratsiyalar soni: " .. count)
```

## Tushuntirish va Mantiq:
Bo'sh jadval ustida iteratsiya hech qachon ishga tushmaydi va xatoliksiz darhol yakunlanadi.

## Ishlash natijasi:
```text
Bo'sh jadvaldagi iteratsiyalar soni: 0
```


# 70-Topshiriq: 1 dan N gacha sonlar yig'indisini hisoblash
## Topshiriq sharti:
1 dan 100 gacha sonlar yig'indisini for tsikli orqali hisoblang.

## Yechim (Lua kodi):
```lua
local N = 100
local totalSum = 0

for i = 1, N do
    totalSum = totalSum + i
end

print(string.format("1 dan %d gacha yig'indi: %d", N, totalSum))
```

## Tushuntirish va Mantiq:
Klassik arifmetik progressiya yig'indisi iterativ ravishda hisoblandi.

## Ishlash natijasi:
```text
1 dan 100 gacha yig'indi: 5050
```


# 71-Topshiriq: Faktorialni iterativ hisoblash
## Topshiriq sharti:
Berilgan 6 sonining faktorialini (6!) while tsikli orqali hisoblang.

## Yechim (Lua kodi):
```lua
local n = 6
local fact = 1
local temp = n

while temp > 1 do
    fact = fact * temp
    temp = temp - 1
end

print(string.format("%d! faktoriali: %d", n, fact))
```

## Tushuntirish va Mantiq:
Faktorial iterativ tsikl yordamida tezkor hisoblanadi va xotira stegi to'lib ketishidan saqlaydi.

## Ishlash natijasi:
```text
6! faktoriali: 720
```


# 72-Topshiriq: Tub sonlarni aniqlash algoritmi
## Topshiriq sharti:
Berilgan sonning tub (prime) ekanligini for tsikli orqali tekshiring.

## Yechim (Lua kodi):
```lua
local function isPrime(num)
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
```

## Tushuntirish va Mantiq:
Tublikni tekshirishda bo'luvchilarni $\sqrt{N}$ gacha tekshirish optimal hisoblash hisoblanadi.

## Ishlash natijasi:
```text
29 soni tubmi? true
```


# 73-Topshiriq: Karra jadvalini chiqaruvchi ichma-ich for
## Topshiriq sharti:
1 dan 3 gacha bo'lgan kichik karra jadvalini formatlab chiqaring.

## Yechim (Lua kodi):
```lua
for i = 1, 3 do
    local row = ""
    for j = 1, 3 do
        row = row .. string.format("%d x %d = %d\t", i, j, i * j)
    end
    print(row)
end
```

## Tushuntirish va Mantiq:
Ichma-ich tsikllar matritsalar va ko'p o'lchamli hisob-kitoblarni amalga oshirishda asosiy vositadir.

## Ishlash natijasi:
```text
1 x 1 = 1	1 x 2 = 2	1 x 3 = 3	
2 x 1 = 2	2 x 2 = 4	2 x 3 = 6	
3 x 1 = 3	3 x 2 = 6	3 x 3 = 9
```


# 74-Topshiriq: Fibonacci ketma-ketligini generatsiya qilish
## Topshiriq sharti:
Dastlabki 8 ta Fibonacci sonini tsikl yordamida toping.

## Yechim (Lua kodi):
```lua
local a, b = 0, 1
local result = {}

for _ = 1, 8 do
    table.insert(result, a)
    a, b = b, a + b
end

print("Fibonacci ketma-ketligi: " .. table.concat(result, ", "))
```

## Tushuntirish va Mantiq:
Lua-dagi ko'p qiymatli o'zlashtirish `a, b = b, a + b` Fibonachchi hisoblashni juda qulay qiladi.

## Ishlash natijasi:
```text
Fibonacci ketma-ketligi: 0, 1, 1, 2, 3, 5, 8, 13
```


# 75-Topshiriq: Massivdagi eng katta va eng kichik qiymatni topish
## Topshiriq sharti:
Ro'yxatdagi min va max qiymatlarni bitta tsiklda aniqlang.

## Yechim (Lua kodi):
```lua
local numbers = {45, 12, 89, 3, 67, 104, 23}

local minVal = numbers[1]
local maxVal = numbers[1]

for i = 2, #numbers do
    if numbers[i] < minVal then minVal = numbers[i] end
    if numbers[i] > maxVal then maxVal = numbers[i] end
end

print("Minimal qiymat: " .. minVal)
print("Maksimal qiymat: " .. maxVal)
```

## Tushuntirish va Mantiq:
Massivdagi ekstremum qiymatlar $O(N)$ chiziqli murakkablikda topiladi.

## Ishlash natijasi:
```text
Minimal qiymat: 3
Maksimal qiymat: 104
```


# 76-Topshiriq: Massiv elementlarini teskari o'girish (Reverse in-place)
## Topshiriq sharti:
Qo'shimcha massiv ochmasdan mavjud massivni joyida teskari qiling.

## Yechim (Lua kodi):
```lua
local arr = {10, 20, 30, 40, 50}
local len = #arr

for i = 1, len // 2 do
    arr[i], arr[len - i + 1] = arr[len - i + 1], arr[i]
end

print("Teskari massiv: " .. table.concat(arr, ", "))
```

## Tushuntirish va Mantiq:
Ikkala tomondan o'rtaga qarab elementlarni swap qilish xotirani tejaydi.

## Ishlash natijasi:
```text
Teskari massiv: 50, 40, 30, 20, 10
```


# 77-Topshiriq: Palindrom satrni tekshirish
## Topshiriq sharti:
Berilgan so'zning chapdan va o'ngdan bir xil o'qilishini tsikl orqali tekshiring.

## Yechim (Lua kodi):
```lua
local function isPalindrome(str)
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
```

## Tushuntirish va Mantiq:
`string.sub(str, i, i)` orqali bittalik belgi olinadi va taqqoslanadi.

## Ishlash natijasi:
```text
kiyik palindrommi? true
kitob palindrommi? false
```


# 78-Topshiriq: Sonning raqamlari yig'indisini hisoblash
## Topshiriq sharti:
Butun sonning barcha raqamlari yig'indisini while tsikli yordamida toping.

## Yechim (Lua kodi):
```lua
local num = 9845
local temp = num
local sum = 0

while temp > 0 do
    sum = sum + (temp % 10)
    temp = temp // 10
end

print(string.format("%d ning raqamlar yig'indisi: %d", num, sum))
```

## Tushuntirish va Mantiq:
Modul 10 oxirgi raqamni ajratadi, butun bo'lish (// 10) esa uni o'chiradi.

## Ishlash natijasi:
```text
9845 ning raqamlar yig'indisi: 26
```


# 79-Topshiriq: Matndagi unli harflarni sanash
## Topshiriq sharti:
O'zbek tilidagi unli harflar sonini for tsiklida sanang.

## Yechim (Lua kodi):
```lua
local text = "Al-Xorazmiy algoritmlar asoschisi"
local vowels = {a=true, e=true, i=true, o=true, u=true}
local count = 0

for i = 1, #text do
    local char = string.lower(string.sub(text, i, i))
    if vowels[char] then
        count = count + 1
    end
end

print("Jami unli harflar: " .. count)
```

## Tushuntirish va Mantiq:
Jadvalda xesh-qidiruv $O(1)$ bo'lgani sababli unli harflarni tekshirish juda tez ishlaydi.

## Ishlash natijasi:
```text
Jami unli harflar: 11
```


# 80-Topshiriq: Chiziqli qidiruv (Linear Search)
## Topshiriq sharti:
Massivda qidirilayotgan qiymatning birinchi uchragan indeksini toping.

## Yechim (Lua kodi):
```lua
local items = {"olma", "anor", "anjir", "uzum", "shaftoli"}
local target = "uzum"
local foundIdx = -1

for i = 1, #items do
    if items[i] == target then
        foundIdx = i
        break
    end
end

print(string.format("'%s' indeksi: %d", target, foundIdx))
```

## Tushuntirish va Mantiq:
Chiziqli qidiruv saralanmagan ro'yxatlarda maqsadli elementni ketma-ket taqqoslaydi.

## Ishlash natijasi:
```text
'uzum' indeksi: 4
```


# 81-Topshiriq: Ikkilik qidiruv (Binary Search)
## Topshiriq sharti:
Saralangan massivda logarifmik vaqtda $O(\log N)$ elementni toping.

## Yechim (Lua kodi):
```lua
local sorted = {11, 23, 35, 47, 59, 71, 83, 95}
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
```

## Tushuntirish va Mantiq:
Ikkilik qidiruv har qadamda qidiruv sohasini 2 barobar qisqartiradi.

## Ishlash natijasi:
```text
71 soni indeksi: 6
```


# 82-Topshiriq: Pufakchali saralash (Bubble Sort)
## Topshiriq sharti:
Klassik pufakchali saralash algoritmini Luada amalga oshiring.

## Yechim (Lua kodi):
```lua
local arr = {64, 34, 25, 12, 22, 11, 90}
local n = #arr

for i = 1, n do
    for j = 1, n - i do
        if arr[j] > arr[j + 1] then
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
        end
    end
end

print("Saralangan massiv: " .. table.concat(arr, ", "))
```

## Tushuntirish va Mantiq:
Bubble Sort ketma-ket qo'shni elementlarni taqqoslab, kattalarini oxiriga 'qalqitadi'.

## Ishlash natijasi:
```text
Saralangan massiv: 11, 12, 22, 25, 34, 64, 90
```


# 83-Topshiriq: Tanlash orqali saralash (Selection Sort)
## Topshiriq sharti:
Eng kichik elementni topib boshiga joylashtiruvchi saralash algoritmi.

## Yechim (Lua kodi):
```lua
local arr = {29, 10, 14, 37, 13}
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
```

## Tushuntirish va Mantiq:
Selection Sort har bir tashqi iteratsiyada qolgan qismning minimalini topadi.

## Ishlash natijasi:
```text
Selection sort natijasi: 10, 13, 14, 29, 37
```


# 84-Topshiriq: Kiritish orqali saralash (Insertion Sort)
## Topshiriq sharti:
Kartalarni tartiblash kabi har bir elementni o'z o'rniga joylashtiruvchi algoritm.

## Yechim (Lua kodi):
```lua
local arr = {12, 11, 13, 5, 6}

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
```

## Tushuntirish va Mantiq:
Insertion Sort kichik yoki qisman saralangan massivlarda juda yuqori samaradorlik ko'rsatadi.

## Ishlash natijasi:
```text
Insertion sort natijasi: 5, 6, 11, 12, 13
```


# 85-Topshiriq: O'yin xaritasi koordinatalarini aylanib chiqish (Grid traversal)
## Topshiriq sharti:
3x3 o'lchamli katakchalarning (x, y) koordinatalari bo'yicha navigatsiya.

## Yechim (Lua kodi):
```lua
local width, height = 3, 3

for y = 1, height do
    local line = ""
    for x = 1, width do
        line = line .. string.format("[%d,%d] ", x, y)
    end
    print(line)
end
```

## Tushuntirish va Mantiq:
2D o'yinlarda xarita plitkalari (tiles) aynan shu tartibda ekranga render qilinadi.

## Ishlash natijasi:
```text
[1,1] [2,1] [3,1] 
[1,2] [2,2] [3,2] 
[1,3] [2,3] [3,3]
```


# 86-Topshiriq: Massiv elementlarini tsiklda filtrlash
## Topshiriq sharti:
Berilgan ro'yxatdan faqat musbat sonlarni ajratib oluvchi yangi massiv yarating.

## Yechim (Lua kodi):
```lua
local rawData = {-5, 12, 0, -3, 44, 98, -17}
local positiveData = {}

for _, val in ipairs(rawData) do
    if val > 0 then
        table.insert(positiveData, val)
    end
end

print("Filtrlangan musbat sonlar: " .. table.concat(positiveData, ", "))
```

## Tushuntirish va Mantiq:
Filtrlash jarayonida yangi jadvalga `table.insert()` orqali shartga mos qiymatlar to'planadi.

## Ishlash natijasi:
```text
Filtrlangan musbat sonlar: 12, 44, 98
```


# 87-Topshiriq: Massiv yig'indisi va o'rtacha arifmetik qiymati
## Topshiriq sharti:
O'quvchilar baholarining umumiy yig'indisi va o'rtachasini toping.

## Yechim (Lua kodi):
```lua
local grades = {85, 90, 78, 92, 88}
local sum = 0

for _, grade in ipairs(grades) do
    sum = sum + grade
end

local average = sum / #grades
print("Jami ball: " .. sum)
print(string.format("O'rtacha baho: %.2f", average))
```

## Tushuntirish va Mantiq:
Massiv uzunligi `#` operatori orqali olinadi va o'rtacha qiymat float sifatida hisoblanadi.

## Ishlash natijasi:
```text
Jami ball: 443
O'rtacha baho: 88.60
```


# 88-Topshiriq: repeat-until orqali validatsiya simulyatsiyasi
## Topshiriq sharti:
To'g'ri PIN kod kiritilgunga qadar takrorlanuvchi jarayonni simulyatsiya qiling.

## Yechim (Lua kodi):
```lua
local SECRET_PIN = 4422
local mockInputs = {1111, 2222, 4422}
local idx = 1
local enteredPin = nil

repeat
    enteredPin = mockInputs[idx]
    print("Tekshirilmoqda: " .. enteredPin)
    idx = idx + 1
until enteredPin == SECRET_PIN

print("PIN kod to'g'ri! Tizimga ruxsat berildi.")
```

## Tushuntirish va Mantiq:
repeat-until shart to'g'ri bo'lmaguncha jarayonni ushlab turish uchun juda mos keladi.

## Ishlash natijasi:
```text
Tekshirilmoqda: 1111
Tekshirilmoqda: 2222
Tekshirilmoqda: 4422
PIN kod to'g'ri! Tizimga ruxsat berildi.
```


# 89-Topshiriq: Ko'p shartli tekshiruvlar (and, or aralashmasi)
## Topshiriq sharti:
VIP foydalanuvchilar yoki chipta sotib olgan faol obunachilarga kirish ruxsatini bering.

## Yechim (Lua kodi):
```lua
local isVIP = false
local hasTicket = true
local isBanned = false

if not isBanned and (isVIP or hasTicket) then
    print("Muzeyga kirish ruxsati berildi.")
else
    print("Kirish taqiqlandi.")
end
```

## Tushuntirish va Mantiq:
Mantiqiy ifodalarda qavslar amallar ustuvorligini boshqarish va xatoliklarning oldini olish uchun zarur.

## Ishlash natijasi:
```text
Muzeyga kirish ruxsati berildi.
```


# 90-Topshiriq: Dinamik o'zgaruvchi qadamli tsikl simulyatsiyasi
## Topshiriq sharti:
Har bir iteratsiyada qadami ikki baravar ortuvchi eksponensial tsikl tuzing.

## Yechim (Lua kodi):
```lua
local current = 1
local step = 1

while current <= 50 do
    print(string.format("Qiymat: %d (Qadam: %d)", current, step))
    current = current + step
    step = step * 2
end
```

## Tushuntirish va Mantiq:
Raqamli for tsiklida qadam o'zgarmasdir, biroq while tsikli yordamida o'zgaruvchan qadamli jarayonlarni boshqarish mumkin.

## Ishlash natijasi:
```text
Qiymat: 1 (Qadam: 1)
Qiymat: 2 (Qadam: 2)
Qiymat: 6 (Qadam: 4)
Qiymat: 14 (Qadam: 8)
Qiymat: 30 (Qadam: 16)
```


# 91-Topshiriq: Cheksiz tsikllardan xavfsiz himoyalanish
## Topshiriq sharti:
while tsikliga xavfsizlik cheklovi (Safety Guard Counter) o'rnating.

## Yechim (Lua kodi):
```lua
local counter = 0
local MAX_SAFE_STEPS = 5

while true do
    counter = counter + 1
    print("Xavfsiz qadam: " .. counter)
    if counter >= MAX_SAFE_STEPS then
        print("Xavfsizlik chegarasiga yetildi, sikl to'xtatildi.")
        break
    end
end
```

## Tushuntirish va Mantiq:
Tizim osilib qolishining oldini olish uchun cheksiz tsikllarda maksimal chegara hisoblagichi o'rnatiladi.

## Ishlash natijasi:
```text
Xavfsiz qadam: 1
Xavfsiz qadam: 2
Xavfsiz qadam: 3
Xavfsiz qadam: 4
Xavfsiz qadam: 5
Xavfsizlik chegarasiga yetildi, sikl to'xtatildi.
```


# 92-Topshiriq: O'yin hayotiy sikli simulyatsiyasi (Game Loop Tick)
## Topshiriq sharti:
3 ta kadr davomida fizika va render funksiyalarini bajaruvchi sikl yozing.

## Yechim (Lua kodi):
```lua
local totalFrames = 3

for frame = 1, totalFrames do
    print(string.format("--- Kadr #%d ---", frame))
    print("1. O'yinchilar harakati hisoblandi")
    print("2. To'qnashuvlar tekshirildi")
    print("3. Ekran yangilandi (Render)")
end
```

## Tushuntirish va Mantiq:
O'yin dvijoklarida (masalan, Roblox yoki LÖVE) asosiy tsikl kadrlar bo'yicha uzluksiz yangilanadi.

## Ishlash natijasi:
```text
--- Kadr #1 ---
1. O'yinchilar harakati hisoblandi
2. To'qnashuvlar tekshirildi
3. Ekran yangilandi (Render)
--- Kadr #2 ---
1. O'yinchilar harakati hisoblandi
2. To'qnashuvlar tekshirildi
3. Ekran yangilandi (Render)
--- Kadr #3 ---
1. O'yinchilar harakati hisoblandi
2. To'qnashuvlar tekshirildi
3. Ekran yangilandi (Render)
```


# 93-Topshiriq: Buyruqlar komandasi (Command dispatch table)
## Topshiriq sharti:
Shartli ifodalarning o'rniga jadvalli dispatch yordamida harakatlarni bajaring.

## Yechim (Lua kodi):
```lua
local commands = {
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
```

## Tushuntirish va Mantiq:
Lua jadvallari funksiyalarni saqlay oladi, bu esa uzun if-else zanjirlarini chiroyli qisqartiradi.

## Ishlash natijasi:
```text
Salomatlik 25 birlikka tiklandi!
```


# 94-Topshiriq: Shaxmat taxtasi simulyatsiyasi (8x8 shartli matritsa)
## Topshiriq sharti:
Katakchaning oq yoki qora ekanligini (x + y) % 2 orqali aniqlang.

## Yechim (Lua kodi):
```lua
local function getSquareColor(row, col)
    return ((row + col) % 2 == 0) and "OQ" or "QORA"
end

print("A1 (1,1): " .. getSquareColor(1, 1))
print("A2 (1,2): " .. getSquareColor(1, 2))
print("B2 (2,2): " .. getSquareColor(2, 2))
```

## Tushuntirish va Mantiq:
Shaxmat taxtasida koordinatalar yig'indisining juft-toqligi katakcha rangini belgilaydi.

## Ishlash natijasi:
```text
A1 (1,1): OQ
A2 (1,2): QORA
B2 (2,2): OQ
```


# 95-Topshiriq: Paskal uchburchagining dastlabki 4 qatorini generatsiya qilish
## Topshiriq sharti:
Kombinatorik hisoblar uchun Paskal uchburchagi qatorlarini hosil qiling.

## Yechim (Lua kodi):
```lua
local triangle = {}
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
```

## Tushuntirish va Mantiq:
Paskal uchburchagida har bir ichki son o'zidan yuqoridagi ikkita sonning yig'indisiga tengdir.

## Ishlash natijasi:
```text
1
1 1
1 2 1
1 3 3 1
```


# 96-Topshiriq: Tsikllarda xotirani nazorat qilish va bo'shatish
## Topshiriq sharti:
Tsikl davomida yaratilgan vaqtinchalik jadvallarni xotiradan tozalash.

## Yechim (Lua kodi):
```lua
for i = 1, 3 do
    local tempData = {id = i, payload = string.rep("X", 100)}
    print(string.format("Vaqtinchalik paket #%d qayta ishlandi", tempData.id))
    tempData = nil -- Xotirada Garbage Collectorga tayyorlash
end
print("Barcha paketlar yakunlandi.")
```

## Tushuntirish va Mantiq:
Lokal o'zgaruvchilar siklning har bir qadamida qayta yaratiladi va qadam tugashi bilan yaroqsiz bo'ladi.

## Ishlash natijasi:
```text
Vaqtinchalik paket #1 qayta ishlandi
Vaqtinchalik paket #2 qayta ishlandi
Vaqtinchalik paket #3 qayta ishlandi
Barcha paketlar yakunlandi.
```


# 97-Topshiriq: for tsikli chegaralarining faqat bir marta hisoblanishi
## Topshiriq sharti:
for tsikli boshlanishida funksiya chaqirilib, faqat bir marta hisoblanishini isbotlang.

## Yechim (Lua kodi):
```lua
local calls = 0
local function getLimit()
    calls = calls + 1
    return 3
end

for i = 1, getLimit() do
    -- Tsikl tanasi
end

print("getLimit() necha marta chaqirildi? " .. calls)
```

## Tushuntirish va Mantiq:
Lua tili for tsiklining start, stop va step ifodalarini faqat bitta marta tsikl boshlanishida hisoblab saqlab qo'yadi.

## Ishlash natijasi:
```text
getLimit() necha marta chaqirildi? 1
```


# 98-Topshiriq: Satrdagi so'zlarni tsiklda ajratish
## Topshiriq sharti:
Matn ichidagi so'zlarni bo'shliqlar bo'yicha for tsiklida ajrating.

## Yechim (Lua kodi):
```lua
local sentence = "Assalomu alaykum aziz dasturchilar"
local words = {}

for word in string.gmatch(sentence, "%S+") do
    table.insert(words, word)
end

print("So'zlar soni: " .. #words)
print("Ikkinchi so'z: " .. words[2])
```

## Tushuntirish va Mantiq:
`string.gmatch` Luadagi maxsus iterator bo'lib, generic for tsikli bilan mukammal ishlaydi.

## Ishlash natijasi:
```text
So'zlar soni: 4
Ikkinchi so'z: alaykum
```


# 99-Topshiriq: Shartli holat mashinasi (State Machine) tsikli
## Topshiriq sharti:
O'yin qahramonining holatlarini (IDLE -> RUN -> ATTACK) boshqaring.

## Yechim (Lua kodi):
```lua
local states = {"IDLE", "RUN", "ATTACK"}

for _, state in ipairs(states) do
    if state == "IDLE" then
        print("[HOLAT] Qahramon tinch turibdi")
    elseif state == "RUN" then
        print("[HOLAT] Qahramon nishon tomon yugurmoqda")
    elseif state == "ATTACK" then
        print("[HOLAT] Qahramon dushmanga hujum qildi")
    end
end
```

## Tushuntirish va Mantiq:
Holatlar mashinasi sun'iy intellekt va o'yin personajlarining xatti-harakatini boshqarishda poydevor hisoblanadi.

## Ishlash natijasi:
```text
[HOLAT] Qahramon tinch turibdi
[HOLAT] Qahramon nishon tomon yugurmoqda
[HOLAT] Qahramon dushmanga hujum qildi
```


# 100-Topshiriq: Kompleks jang tizimi simulyatsiyasi
## Topshiriq sharti:
Qahramon va maxluq o'rtasidagi to'liq navbatma-navbat jang jarayonini tsikl orqali modellashtiring.

## Yechim (Lua kodi):
```lua
local heroHP = 60
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
```

## Tushuntirish va Mantiq:
Barcha boshqaruv oqimlari (while, if, break, string.format) uyg'unlikda to'liq jang tizimini amalga oshirdi.

## Ishlash natijasi:
```text
Raund 1: Qahramon HP=45, Maxluq HP=30
Raund 2: Qahramon HP=30, Maxluq HP=10
Raund 3: Qahramon zarba berdi. Maxluq mag'lub bo'ldi!
Jang yakunlandi! Qahramon g'alaba qozondi.
```

