# -*- coding: utf-8 -*-
"""
Generator for Lua Topics 01 - 05 (Tasks 1 to 250)
19-til: Lua
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

def build_topic_01():
    tasks = []
    
    # 1
    tasks.append((
        1,
        "Lokal o'zgaruvchi e'lon qilish: 'local' kalit so'zi",
        "O'yin qahramonining ismi va boshlang'ich salomatlik darajasini 'local' kalit so'zi orqali e'lon qiling hamda konsolga chiqaring.",
        """local playerName = "Alpomish"
local health = 100

print("Qahramon ismi: " .. playerName)
print("Salomatlik darajasi: " .. health .. "%")
""",
        "Lua tilida 'local' kalit so'zi o'zgaruvchini joriy blok (fayl, funksiya yoki sikl) doirasida e'lon qiladi. Lokal o'zgaruvchilar xotira va bajarilish tezligi jihatidan global o'zgaruvchilardan ancha ustun bo'lib, ular virtual mashina registrlarida saqlanadi.",
        """Qahramon ismi: Alpomish
Salomatlik darajasi: 100%"""
    ))

    # 2
    tasks.append((
        2,
        "Global va lokal o'zgaruvchilar tafovuti",
        "Bitta blok ichida bir xil nomli lokal va global o'zgaruvchilarni e'lon qilib, ularning qamrov doirasini ko'rsating.",
        """globalScore = 500 -- Global o'zgaruvchi

do
    local globalScore = 150 -- Faqat ushbu blok ichida amal qiluvchi lokal o'zgaruvchi
    print("Blok ichidagi lokal ball: " .. globalScore)
end

print("Tashqi global ball: " .. globalScore)
""",
        "Lua tilida o'zgaruvchi oldiga 'local' qo'yilmasa, u avtomatik ravishda global muhitga (_G jadvaliga) tushadi. 'do ... end' bloki mustaqil ko'rinish doirasini hosil qiladi va tashqi o'zgaruvchilarni shadowed (soyalangan) holatga keltiradi.",
        """Blok ichidagi lokal ball: 150
Tashqi global ball: 500"""
    ))

    # 3
    tasks.append((
        3,
        "'nil' qiymati va o'zgaruvchini tozalash",
        "Lokal o'zgaruvchiga dastlab qiymat bering, so'ngra unga nil o'zlashtirib, qiymat o'chirilganligini isbotlang.",
        """local temporarySession = "SESSION_TOKEN_XYZ883"
print("Dastlabki sessiya: " .. tostring(temporarySession))

-- Sessiyani yakunlash va xotirani bo'shatish
temporarySession = nil
print("Yakunlangan sessiya: " .. tostring(temporarySession))

if temporarySession == nil then
    print("Sessiya muvaffaqiyatli o'chirildi.")
end
""",
        "Lua tilida 'nil' boshqa tillardagi 'null' yoki 'None' tushunchasiga to'g'ri keladi. Har qanday e'lon qilinmagan yoki o'chirilgan o'zgaruvchi nil qiymatiga ega bo'ladi. O'zgaruvchiga nil biriktirish xotirada Garbage Collector uchun ob'ektni yaroqsiz qilib belgilaydi.",
        """Dastlabki sessiya: SESSION_TOKEN_XYZ883
Yakunlangan sessiya: nil
Sessiya muvaffaqiyatli o'chirildi."""
    ))

    # 4
    tasks.append((
        4,
        "Boolean qiymatlari va Luada rostlik qoidalari",
        "Lua tilida 0 soni, bo'sh satr, false va nil qiymatlarining mantiqiy ifodadagi xatti-harakatini tekshiring.",
        """local function testCondition(value, name)
    if value then
        print(name .. " -> ROST (true)")
    else
        print(name .. " -> YOLG'ON (false)")
    end
end

testCondition(true, "true")
testCondition(false, "false")
testCondition(nil, "nil")
testCondition(0, "0 soni")
testCondition("", "Bo'sh satr ('')")
""",
        "Dasturlash tillari orasida Lua o'ziga xos qoidaga ega: FAQATGINA 'false' va 'nil' qiymatlari yolg'on hisoblanadi. Son '0' va bo'sh satr '\"\"' Luada haqiqiy (truthy) deb baholanadi. Bu C yoki Python dasturchilari ko'p adashadigan muhim nuqtadir.",
        """true -> ROST (true)
false -> YOLG'ON (false)
nil -> YOLG'ON (false)
0 soni -> ROST (true)
Bo'sh satr ('') -> ROST (true)"""
    ))

    # 5
    tasks.append((
        5,
        "Number turi: Butun sonlar (Integers)",
        "O'yinchining tangalar soni va tajriba ballarini butun son sifatida e'lon qiling hamda arifmetik oshiring.",
        """local goldCoins = 1500
local expPoints = 320

goldCoins = goldCoins + 250
expPoints = expPoints + 80

print("Jami oltin tangalar: " .. goldCoins)
print("Jami tajriba ballari: " .. expPoints)
print("Oltin turi: " .. math.type(goldCoins))
""",
        "Lua 5.3 versiyasidan boshlab 'number' turi ichki 64-bitli butun sonlar (integer) va 64-bitli suzuvchi nuqtali sonlar (float) ga ajratildi. 'math.type()' funksiyasi raqamning aynan butun (integer) yoki kasr (float) ekanligini ko'rsatadi.",
        """Jami oltin tangalar: 1750
Jami tajriba ballari: 400
Oltin turi: integer"""
    ))

    # 6
    tasks.append((
        6,
        "Number turi: Suzuvchi nuqtali sonlar (Floats)",
        "Dvigatel harorati va bosimini o'lchovchi datchik ma'lumotlarini haqiqiy sonlar sifatida hisoblang.",
        """local temperature = 98.6
local pressure = 101.325

local combinedIndex = temperature * 0.4 + pressure * 0.6
print(string.format("Temperatura: %.2f C", temperature))
print(string.format("Bosim: %.3f kPa", pressure))
print(string.format("Umumiy ko'rsatkich: %.4f", combinedIndex))
print("Temperatura son turi: " .. math.type(temperature))
""",
        "Suzuvchi nuqtali sonlar IEEE 754 standartiga mos keladi. string.format yordamida kasr sonlarni ma'lum bir aniqlikda formatlash mumkin. math.type kasr sonlar uchun 'float' qiymatini qaytaradi.",
        """Temperatura: 98.60 C
Bosim: 101.325 kPa
Umumiy ko'rsatkich: 100.2350
Temperatura son turi: float"""
    ))

    # 7
    tasks.append((
        7,
        "type() funksiyasi orqali dinamik turlarni aniqlash",
        "Lua-dagi asosiy turlarni o'zgaruvchilarga biriktirib, type() funksiyasi orqali ularning turini ekranga chiqaring.",
        """local values = {
    nil,
    true,
    42,
    "Salom Dunyo",
    {1, 2, 3},
    print,
    coroutine.create(function() end)
}

local labels = {"nil", "boolean", "number", "string", "table", "function", "thread"}

for i = 1, #values do
    print(string.format("Qiymat: %-12s -> type(): %s", labels[i], type(values[i])))
end
""",
        "Lua dinamik tiplangan tildir: o'zgaruvchilar emas, qiymatlar tipga ega. 'type()' funksiyasi har doim qiymatning turini bildiruvchi satr qaytaradi ('nil', 'boolean', 'number', 'string', 'table', 'function', 'thread', 'userdata').",
        """Qiymat: nil          -> type(): nil
Qiymat: boolean      -> type(): boolean
Qiymat: number       -> type(): number
Qiymat: string       -> type(): string
Qiymat: table        -> type(): table
Qiymat: function     -> type(): function
Qiymat: thread       -> type(): thread"""
    ))

    # 8
    tasks.append((
        8,
        "Arifmetik qo'shish va ayirish amallari",
        "Do'kondagi xarid savati summasini, yetkazib berish haqi va chegirma miqdorini hisoblang.",
        """local cartTotal = 245000
local deliveryFee = 20000
local discount = 35000

local finalPrice = cartTotal + deliveryFee - discount
print("Savat narxi: " .. cartTotal .. " so'm")
print("Yetkazish: +" .. deliveryFee .. " so'm")
print("Chegirma: -" .. discount .. " so'm")
print("Yakuniy to'lov: " .. finalPrice .. " so'm")
""",
        "Lua tili standart arifmetik operatorlarni qo'llab-quvvatlaydi. Qo'shish (+) va ayirish (-) butun sonlar ustida bajarilganda natija integer, kasr sonlar aralashganda esa float bo'ladi.",
        """Savat narxi: 245000 so'm
Yetkazish: +20000 so'm
Chegirma: -35000 so'm
Yakuniy to'lov: 230000 so'm"""
    ))

    # 9
    tasks.append((
        9,
        "Ko'paytirish va haqiqiy bo'lish (/) operatori",
        "Mahsulot narxini miqdoriga ko'paytiring va umumiy xarajatni 4 nafar do'st o'rtasida teng taqsimlang.",
        """local itemPrice = 17500
local quantity = 6
local totalCost = itemPrice * quantity
local friendsCount = 4

local perPerson = totalCost / friendsCount
print("Jami summa: " .. totalCost .. " so'm")
print("Har bir kishi to'laydigan ulush: " .. perPerson .. " so'm")
print("Ulush turi: " .. math.type(perPerson))
""",
        "Lua 5.3+ versiyalarida oddiy bo'lish (/) operatori har doim suzuvchi nuqtali son (float) qaytaradi, hatto sonlar qoldiqsiz bo'linsa ham (masalan, 105000 / 4 = 26250.0).",
        """Jami summa: 105000 so'm
Har bir kishi to'laydigan ulush: 26250.0 so'm
Ulush turi: float"""
    ))

    # 10
    tasks.append((
        10,
        "Butun sonli bo'lish (Floor Division //) operatori",
        "Berilgan soniyalar miqdorini to'liq daqiqa va soatlarga aylantirishda // operatoridan foydalaning.",
        """local totalSeconds = 7385

local hours = totalSeconds // 3600
local remainingSeconds = totalSeconds % 3600
local minutes = remainingSeconds // 60
local seconds = remainingSeconds % 60

print(string.format("Jami vaqt: %d soniya", totalSeconds))
print(string.format("Natija: %02d:%02d:%02d", hours, minutes, seconds))
print("Soat turi: " .. math.type(hours))
""",
        "Floor division (//) operatori bo'lish natijasini pastga qarab eng yaqin butun songa yaxlitlaydi. Agar ikkala operand ham integer bo'lsa, natija ham qat'iy integer bo'ladi.",
        """Jami vaqt: 7385 soniya
Natija: 02:03:05
Soat turi: integer"""
    ))

    # 11 - 50 tasks for Topic 1
    topic1_data = [
        (11, "Qoldiqli bo'lish: Modul (%) operatori",
         "O'yin inventaridagi narsalarni har bir qatorda 8 tadan joylashtirish uchun elementning ustun indeksini toping.",
         """local slotIndex = 27
local itemsPerRow = 8

local row = slotIndex // itemsPerRow
local col = slotIndex % itemsPerRow

print("Slot indeksi: " .. slotIndex)
print("Qator raqami: " .. row)
print("Ustun raqami: " .. col)
""",
         "Modul (%) operatori bo'lishdan qolgan qoldiqni hisoblaydi. Luada modul manfiy sonlar uchun ham matematik jihatdan to'g'ri ishlaydi: a % b har doim b ishorasidagi natijani beradi.",
         """Slot indeksi: 27\nQator raqami: 3\nUstun raqami: 3"""),

        (12, "Darajaga ko'tarish operatori (^)",
         "Bank omonatining murakkab foiz hisobini darajaga ko'tarish (^) orqali amalga oshiring.",
         """local principal = 10000000 -- Boshlang'ich summa (10 mln)
local annualRate = 0.18        -- Yillik 18%
local years = 3

local finalAmount = principal * ((1 + annualRate) ^ years)
print(string.format("Boshlang'ich summa: %d so'm", principal))
print(string.format("%d yildan keyingi summa: %.2f so'm", years, finalAmount))
""",
         "Lua tilida darajaga ko'tarish uchun maxsus '^' operatori mavjud. Har qanday darajaga ko'tarish amali float natija beradi.",
         """Boshlang'ich summa: 10000000 so'm\n3 yildan keyingi summa: 16430320.00 so'm"""),

        (13, "Satr literallari: Bittalik va ikkitalik qo'shtirnoqlar",
         "Ikkitalik va bittalik qo'shtirnoqlar yordamida ichida tirnoq qatnashgan jumlalarni e'lon qiling.",
         """local msg1 = 'Alisher aytdi: "Dasturlash - kelajak kasbi."'
local msg2 = "Kitob nomi: 'Al-Xorazmiy merosi'"

print(msg1)
print(msg2)
""",
         "Luada bittalik ('') va ikkitalik (\"\") qo'shtirnoqlar o'rtasida semantik farq yo'q. Biri ikkinchisining ichida qulay ishlatilishi mumkin.",
         """Alisher aytdi: "Dasturlash - kelajak kasbi."\nKitob nomi: 'Al-Xorazmiy merosi'"""),

        (14, "Ko'p qatorli satrlar: [[ ... ]] sintaksisi",
         "SQL so'rovini yoki HTML shablonini ko'p qatorli satr blokida yozing.",
         """local query = [[
SELECT id, username, email, balance 
FROM users 
WHERE status = 'ACTIVE' 
ORDER BY registered_at DESC;
]]

print("SQL so'rovi:")
print(query)
""",
         "Lua tilida [[ va ]] qavslari ko'p qatorli (multiline) satrlarni hech qanday escape belgilarisiz yozish imkonini beradi.",
         """SQL so'rovi:\nSELECT id, username, email, balance \nFROM users \nWHERE status = 'ACTIVE' \nORDER BY registered_at DESC;"""),

        (15, "Satr konkatenatsiyasi (..) operatori",
         "Foydalanuvchining ismi, familiyasi va yoshini '..' operatori orqali birlashtirib profil matnini hosil qiling.",
         """local firstName = "Ibrohim"
local lastName = "Karimov"
local age = 22

local profile = firstName .. " " .. lastName .. ", yoshi: " .. age
print(profile)
""",
         "Luada satrlarni birlashtirish uchun '..' (ikki nuqta) operatori ishlatiladi. Agar operand son bo'lsa, Lua uni avtomatik ravishda satrga o'giradi.",
         """Ibrohim Karimov, yoshi: 22"""),

        (16, "Uzunlik operatori (#) satrlar uchun",
         "Parol uzunligini '#' operatori yordamida tekshirib, xavfsizlik darajasini aniqlang.",
         """local password = "SuperSecret_Pass2026!"
local passLength = #password

print("Parol: " .. password)
print("Uzunligi: " .. passLength .. " bayt")

if passLength >= 12 then
    print("Xavfsizlik darajasi: Kuchli")
else
    print("Xavfsizlik darajasi: Qoniqarsiz")
end
""",
         "'#' operatori satr oldiga qo'yilganda uning baytlardagi uzunligini qaytaradi. ASCII belgilari uchun bayt soni belgi soniga teng bo'ladi.",
         """Parol: SuperSecret_Pass2026!\nUzunligi: 21 bayt\nXavfsizlik darajasi: Kuchli"""),

        (17, "Mantiqiy 'and' operatori va qisqa tutashuv (short-circuit)",
         "Foydalanuvchi tizimga kirganligi va uning balansi yetarli ekanligini 'and' operatori orqali baholang.",
         """local isLoggedIn = true
local userBalance = 15000
local requiredPrice = 10000

local canPurchase = isLoggedIn and (userBalance >= requiredPrice)
print("Xarid qilish imkoni bormi? " .. tostring(canPurchase))
""",
         "'and' operatori birinchi ifoda yolg'on (false/nil) bo'lsa, ikkinchisini hisoblamasdan darhol birinchisini qaytaradi. Aks holda ikkinchi qiymatni qaytaradi.",
         """Xarid qilish imkoni bormi? true"""),

        (18, "Mantiqiy 'or' operatori va birlamchi (default) qiymat berish",
         "Foydalanuvchi laqabini aniqlang; agar kiritilmagan (nil) bo'lsa, 'Mehmon' so'zini biriktiring.",
         """local userInput = nil
local activeNick = userInput or "Mehmon"

print("Joriy laqab: " .. activeNick)

userInput = "KiberBot"
activeNick = userInput or "Mehmon"
print("Yangilangan laqab: " .. activeNick)
""",
         "Lua tilida 'a or b' idiomi keng qo'llaniladi. Agar 'a' mavjud bo'lsa (truthy), 'a' olinadi, aks holda birlamchi 'b' qiymati tanlanadi.",
         """Joriy laqab: Mehmon\nYangilangan laqab: KiberBot"""),

        (19, "Mantiqiy 'not' operatori va inkor",
         "O'yin xaritasi yuklangan yoki yuklanmaganligini 'not' operatori orqali tekshiring.",
         """local isMapLoaded = false

if not isMapLoaded then
    print("Xarita hali yuklanmadi. Yuklash jarayoni boshlanmoqda...")
    isMapLoaded = true
end

print("Yakuniy holat: " .. tostring(isMapLoaded))
""",
         "'not' operatori har doim qat'iy boolean qiymat (true yoki false) qaytaradi. Agar operand false yoki nil bo'lsa true, boshqa barcha holatlarda false qaytaradi.",
         """Xarita hali yuklanmadi. Yuklash jarayoni boshlanmoqda...\nYakuniy holat: true"""),

        (20, "Ternary operator simulyatsiyasi: (cond and a or b)",
         "Talabaning o'rtacha baliga qarab uning stipendiya olish yoki olmasligini bitta qatorda aniqlang.",
         """local gpa = 4.7
local status = (gpa >= 4.0) and "Stipendiya berilsin" or "Stipendiya yo'q"

print("Talaba balli: " .. gpa)
print("Qaror: " .. status)
""",
         "Lua-da C/JS dagi `cond ? a : b` ternar operatori o'rniga `cond and a or b` konstruksiyasi ishlatiladi. Diqqat: 'a' qiymati hech qachon false yoki nil bo'lmasligi kerak.",
         """Talaba balli: 4.7\nQaror: Stipendiya berilsin"""),

        (21, "Parallel o'zlashtirish (Multiple Assignment)",
         "Bitta buyruq orqali bir nechta o'zgaruvchilarga mos ravishda qiymatlar bering.",
         """local x, y, z = 10, 25, 50

print("x = " .. x)
print("y = " .. y)
print("z = " .. z)
""",
         "Lua bir nechta o'zgaruvchilarga bitta operatorda parallel qiymat yuklash imkonini beradi. O'ng tarafdagi barcha ifodalar avval hisoblanadi, so'ngra chap tarafdagi o'zgaruvchilarga biriktiriladi.",
         """x = 10\ny = 25\nz = 50"""),

        (22, "Qiymatlarni almashtirish (Swap idiomasi)",
         "Qo'shimcha vaqtinchalik o'zgaruvchisiz ikkita o'zgaruvchining qiymatini almashtiring.",
         """local player1 = "Sherzod"
local player2 = "Dilshod"

print("Almashishdan oldin: P1=" .. player1 .. ", P2=" .. player2)

player1, player2 = player2, player1

print("Almashgandan keyin: P1=" .. player1 .. ", P2=" .. player2)
""",
         "Lua-da `a, b = b, a` orqali hech qanday temp o'zgaruvchisiz qiymatlarni oson va xavfsiz almashtirish mumkin.",
         """Almashishdan oldin: P1=Sherzod, P2=Dilshod\nAlmashgandan keyin: P1=Dilshod, P2=Sherzod"""),

        (23, "Ortiqcha va yetishmayotgan qiymatlarni o'zlashtirish",
         "O'zgaruvchilar soni qiymatlar sonidan kam yoki ko'p bo'lganda nima sodir bo'lishini namoyish qiling.",
         """local a, b, c = 1, 2
print("a=" .. tostring(a) .. ", b=" .. tostring(b) .. ", c=" .. tostring(c))

local d, e = 10, 20, 30
print("d=" .. tostring(d) .. ", e=" .. tostring(e))
""",
         "Agar qiymatlar soni kam bo'lsa, yetishmayotgan o'zgaruvchilar 'nil' qabul qiladi. Agar ortiqcha qiymat berilsa, ular shunchaki inobatga olinmaydi.",
         """a=1, b=2, c=nil\nd=10, e=20"""),

        (24, "tonumber() funksiyasi va sonlarga o'tkazish",
         "Foydalanuvchi tomonidan kiritilgan matnli sonlarni haqiqiy son turiga o'giring va tekshiring.",
         """local strNum1 = "1250"
local strNum2 = "45.75"
local invalidStr = "ABC12"

local n1 = tonumber(strNum1)
local n2 = tonumber(strNum2)
local n3 = tonumber(invalidStr)

print("n1: " .. tostring(n1) .. ", turi: " .. math.type(n1))
print("n2: " .. tostring(n2) .. ", turi: " .. math.type(n2))
print("n3: " .. tostring(n3))
""",
         "'tonumber()' satrni muvaffaqiyatli songa aylantirsa son qaytaradi, noto'g'ri format bo'lsa xatolik chiqarmasdan 'nil' qaytaradi.",
         """n1: 1250, turi: integer\nn2: 45.75, turi: float\nn3: nil"""),

        (25, "tostring() funksiyasi va satrga o'tkazish",
         "Har xil turdagi qiymatlarni tostring() yordamida matn ko'rinishiga o'giring.",
         """local num = 99
local flag = true
local empty = nil

print("Matnli son: " .. tostring(num))
print("Matnli boolean: " .. tostring(flag))
print("Matnli nil: " .. tostring(empty))
""",
         "'tostring()' har qanday Lua qiymatini ekranga chiqarish mumkin bo'lgan satr ko'rinishiga aylantiradi.",
         """Matnli son: 99\nMatnli boolean: true\nMatnli nil: nil"""),

        (26, "O'n oltilik (Hexadecimal) sonlar bilan ishlash",
         "RGB rang kodini hexadecimal formatda e'lon qiling va uning o'nlik qiymatini ko'rsating.",
         """local colorRed = 0xFF0000
local colorGreen = 0x00FF00
local colorBlue = 0x0000FF

print(string.format("Qizil rang o'nlikda: %d", colorRed))
print(string.format("Yashil rang o'nlikda: %d", colorGreen))
print(string.format("Ko'k rang o'nlikda: %d", colorBlue))
""",
         "Lua 0x prefiksi orqali o'n oltilik sonlarni qabul qiladi va ularni avtomatik tarzda butun son (integer) sifatida saqlaydi.",
         """Qizil rang o'nlikda: 16711680\nYashil rang o'nlikda: 65280\nKo'k rang o'nlikda: 255"""),

        (27, "Ilmiy formatdagi (Scientific notation) sonlar",
         "Katta va kichik fizik o'zgarmaslarni ilmiy formatda (masalan, yorug'lik tezligi) e'lon qiling.",
         """local speedOfLight = 3.0e8     -- 300,000,000 m/s
local electronMass = 9.109e-31   -- kg

print(string.format("Yorug'lik tezligi: %.0f m/s", speedOfLight))
print(string.format("Elektron massasi: %e kg", electronMass))
print("Turi: " .. math.type(speedOfLight))
""",
         "Lua ilmiy formatdagi eksponent sonlarni (e yoki E) float sifatida taniydi.",
         """Yorug'lik tezligi: 300000000 m/s\nElektron massasi: 9.109000e-31 kg\nTuri: float"""),

        (28, "Satr ichidagi escape ketma-ketliklari",
         "Tabulyatsiya (\\t), yangi qator (\\n) va tirnoq belgilaridan foydalanib jadvalli matn chiqaring.",
         """local tableText = "ID\\tIsm\\t\\tBall\\n1\\tRustam\\t\\t95\\n2\\tMadina\\t\\t98"
print(tableText)
""",
         "Lua satrlarida \\n yangi qator, \\t tabulyatsiya, \\\" qo'shtirnoq va \\\\ teskari slesh belgilari escape qilinadi.",
         """ID\tIsm\t\tBall\n1\tRustam\t\t95\n2\tMadina\t\t98"""),

        (29, "Bayt kodlari orqali belgilarni ifodalash (\\xXX)",
         "ASCII va maxsus belgilarni o'n oltilik bayt kodi orqali satrga joylang.",
         """local message = "\\x4C\\x75\\x61\\x20\\x35\\x2E\\x34"
print("Kodlangan satr: " .. message)
""",
         "\\x prefiksi orqali istalgan 8-bitli baytni satr ichida belgilash mumkin (masalan \\x4C = 'L').",
         """Kodlangan satr: Lua 5.4"""),

        (30, "Butun sonlarning chegaralari: math.maxinteger va math.mininteger",
         "64-bitli arxitekturadagi butun sonlarning eng katta va eng kichik qiymatlarini chiqaring.",
         """local maxInt = math.maxinteger
local minInt = math.mininteger

print("Maksimal butun son: " .. maxInt)
print("Minimal butun son: " .. minInt)
""",
         "Lua 5.3+ da `math.maxinteger` ($2^{63}-1$) va `math.mininteger` ($-2^{63}$) konstantalari mavjud.",
         """Maksimal butun son: 9223372036854775807\nMinimal butun son: -9223372036854775808"""),

        (31, "Integer overflow va aylanma o'tish (wrap-around)",
         "Maksimal butun songa 1 qo'shganda sodir bo'ladigan holatni tahlil qiling.",
         """local maxVal = math.maxinteger
local overflowVal = maxVal + 1

print("Maksimal qiymat: " .. maxVal)
print("Overflowdan keyin: " .. overflowVal)
print("Bu math.mininteger ga tengmi? " .. tostring(overflowVal == math.mininteger))
""",
         "Lua 5.3+ da butun sonlar arifmetikasi ikki darajali to'ldiruvchi (two's complement wrap-around) asosida aylanadi: maxinteger + 1 natijasi mininteger bo'ladi.",
         """Maksimal qiymat: 9223372036854775807\nOverflowdan keyin: -9223372036854775808\nBu math.mininteger ga tengmi? true"""),

        (32, "Bitwise AND (&) operatori",
         "Bayroqlar (flags) tizimida ruxsatnomalarni bitwise & orqali tekshiring.",
         """local READ_PERMISSION  = 0x01 -- 0001
local WRITE_PERMISSION = 0x02 -- 0010
local EXEC_PERMISSION  = 0x04 -- 0100

local userRights = 0x05 -- 0101 (READ + EXEC)

local canRead = (userRights & READ_PERMISSION) ~= 0
local canWrite = (userRights & WRITE_PERMISSION) ~= 0

print("O'qish huquqi bormi? " .. tostring(canRead))
print("Yozish huquqi bormi? " .. tostring(canWrite))
""",
         "Lua 5.3 dan boshlab bitwise & operatori qo'shildi. U bitma-bit AND amalini bajaradi.",
         """O'qish huquqi bormi? true\nYozish huquqi bormi? false"""),

        (33, "Bitwise OR (|) operatori",
         "Bir nechta huquq bayroqlarini bitwise | yordamida birlashtiring.",
         """local FLAG_A = 1 -- 0001
local FLAG_B = 2 -- 0010
local FLAG_C = 8 -- 1000

local combined = FLAG_A | FLAG_B | FLAG_C
print("Birlashtirilgan qiymat: " .. combined)
print(string.format("Hex: 0x%X", combined))
""",
         "Bitwise OR (|) barcha berilgan bitlarni birlashtiradi.",
         """Birlashtirilgan qiymat: 11\nHex: 0xB"""),

        (34, "Bitwise XOR (~) operatori",
         "Ikkita son o'rtasida bitwise XOR (~) amalini qo'llab qiymatni shifrlang va qayta tiklang.",
         """local secretKey = 0x5A
local originalData = 0x3F

local encrypted = originalData ~ secretKey
local decrypted = encrypted ~ secretKey

print(string.format("Asl qiymat: 0x%X", originalData))
print(string.format("Shifrlangan: 0x%X", encrypted))
print(string.format("Qayta tiklangan: 0x%X", decrypted))
""",
         "XOR (~) operatori ikkita bir xil kalit bilan qo'llanganda asl qiymatni qaytaradi.",
         """Asl qiymat: 0x3F\nShifrlangan: 0x65\nQayta tiklangan: 0x3F"""),

        (35, "Bitwise NOT (~) unar operatori",
         "Butun sonning barcha bitlarini teskarisiga o'giring.",
         """local value = 0
local inverted = ~value

print("Boshlang'ich: " .. value)
print("Inversiya: " .. inverted)
""",
         "Luada unar ~ operatori sonning barcha bitlarini inversiya qiladi (~0 = -1).",
         """Boshlang'ich: 0\nInversiya: -1"""),

        (36, "Bitwise chapga siljitish (<<)",
         "Sonni 2 ning darajasiga tezkor ko'paytirish uchun << operatoridan foydalaning.",
         """local num = 5
local shifted = num << 3 -- 5 * 2^3 = 40

print("Boshlang'ich: " .. num)
print("3 bit chapga: " .. shifted)
""",
         "<< operatori bitlarni chapga siljitadi va bo'sh joylarni 0 bilan to'ldiradi.",
         """Boshlang'ich: 5\n3 bit chapga: 40"""),

        (37, "Bitwise o'ngga siljitish (>>)",
         "Sonni 2 ning darajasiga bo'lish uchun >> operatoridan foydalaning.",
         """local num = 64
local shifted = num >> 2 -- 64 / 4 = 16

print("Boshlang'ich: " .. num)
print("2 bit o'ngga: " .. shifted)
""",
         ">> operatori bitlarni o'ngga siljitadi.",
         """Boshlang'ich: 64\n2 bit o'ngga: 16"""),

        (38, "Lua 5.4 To-be-closed o'zgaruvchilar: <close>",
         "Blok tugaganda avtomatik yopiluvchi maxsus resurs ob'ektini yarating.",
         """local resource = setmetatable({}, {
    __close = function(self, err)
        print("Resurs avtomatik yopildi! Xato bormi: " .. tostring(err ~= nil))
    end
})

do
    local res <close> = resource
    print("Resurs bilan ishlamoqda...")
end

print("Blokdan tashqariga chiqildi.")
""",
         "Lua 5.4 da kiritilgan `<close>` atributi o'zgaruvchi o'z skopini tark etganda uning `__close` metametodini kafolatli chaqiradi (RAII konsepsiyasi).",
         """Resurs bilan ishlamoqda...\nResurs avtomatik yopildi! Xato bormi: false\nBlokdan tashqariga chiqildi."""),

        (39, "Lua 5.4 Doimiy o'zgaruvchilar: <const>",
         "Qiymatini o'zgartirib bo'lmaydigan o'zgarmas kattalikni <const> bilan belgilang.",
         """local MAX_PLAYERS <const> = 50
print("Maksimal o'yinchilar: " .. MAX_PLAYERS)

-- MAX_PLAYERS = 60 -- Kompilyatsiya xatosi beradi!
print("O'zgarmas xavfsiz e'lon qilindi.")
""",
         "`<const>` atributi o'zgaruvchiga qayta qiymat berishni kompilyatsiya vaqtidayoq taqiqlaydi.",
         """Maksimal o'yinchilar: 50\nO'zgarmas xavfsiz e'lon qilindi."""),

        (40, "O'zgaruvchilar ko'rinish doirasi: do ... end bloklari",
         "Katta skriptlarda xotirani tejash va o'zgaruvchilarni izolyatsiya qilish uchun bloklardan foydalaning.",
         """local mainResult = 0

do
    local step1 = 10 * 5
    local step2 = step1 + 25
    mainResult = step2 * 2
end

-- print(step1) -- nil bo'ladi, xotiradan o'chirilgan
print("Yakuniy natija: " .. mainResult)
""",
         "`do ... end` lokal o'zgaruvchilarning hayot davomiyligini qisqartiradi va xotirani tezroq bo'shatishga yordam beradi.",
         """Yakuniy natija: 150"""),

        (41, "O'zgaruvchilar soyalanishi (Variable Shadowing)",
         "Ichki blokdagi bir xil nomli o'zgaruvchining tashqi o'zgaruvchiga ta'sir qilmasligini ko'rsating.",
         """local x = "Tashqi qiymat"

do
    local x = "Ichki qiymat"
    print("Ichkarida x: " .. x)
end

print("Tashqarida x: " .. x)
""",
         "Ichki blokdagi 'local x' tashqi 'x' ni vaqtincha berkitadi, lekin uni o'zgartirmaydi.",
         """Ichkarida x: Ichki qiymat\nTashqarida x: Tashqi qiymat"""),

        (42, "_G global jadvali orqali murojaat qilish",
         "Global muhit jadvalida saqlanuvchi qiymatlarni dinamik kalit orqali o'qing.",
         """myGlobalConfig = "PRODUCTION_SERVER_V2"

local keyName = "myGlobalConfig"
print("Kalit orqali o'qilgan qiymat: " .. _G[keyName])
print("_G turi: " .. type(_G))
""",
         "Lua tilida barcha global o'zgaruvchilar `_G` nomli oddiy jadval ichida saqlanadi.",
         """Kalit orqali o'qilgan qiymat: PRODUCTION_SERVER_V2\n_G turi: table"""),

        (43, "_VERSION o'zgaruvchisi orqali versiyani tekshirish",
         "Joriy ishlayotgan Lua interpretatorining versiyasini aniqlang.",
         """print("Joriy Lua versiyasi: " .. _VERSION)

if _VERSION == "Lua 5.4" or _VERSION == "Lua 5.3" then
    print("Zamonaviy Lua versiyasi faol.")
else
    print("Klassik yoki moslashtirilgan Lua muhiti.")
end
""",
         "`_VERSION` global o'zgaruvchisi interpretator nomi va versiyasini o'z ichiga oladi.",
         """Joriy Lua versiyasi: Lua 5.4\nZamonaviy Lua versiyasi faol."""),

        (44, "Satr va sonni avtomatik aylantirish (Coercion)",
         "Luada satr va son o'rtasidagi arifmetik amallarni va uning xavflarini ko'rsating.",
         """local s = "100"
local n = 50

local result = s + n -- Avtomatik satrni songa o'giradi
print("s + n natijasi: " .. result)
print("s .. n natijasi: " .. (s .. n))
""",
         "Lua arifmetik amallarda satrlarni avtomatik ravishda songa o'giradi. Ammo bu yashirin xatolarga sabab bo'lishi mumkinligi uchun explicit tonumber() ishlatish tavsiya etiladi.",
         """s + n natijasi: 150.0\ns .. n natijasi: 10050"""),

        (45, "NaN va Infinity bilan ishlash",
         "0 ga bo'lish va noaniq matematik amallar natijasini tahlil qiling.",
         """local inf = 1.0 / 0.0
local negInf = -1.0 / 0.0
local nan = 0.0 / 0.0

print("Cheksizlik: " .. inf)
print("Manfiy cheksizlik: " .. negInf)
print("NaN: " .. nan)
print("NaN o'ziga tengmi? " .. tostring(nan == nan))
""",
         "IEEE 754 bo'yicha NaN hech narsaga, hatto o'ziga ham teng emas (`nan == nan` har doim false).",
         """Cheksizlik: inf\nManfiy cheksizlik: -inf\nNaN: nan\nNaN o'ziga tengmi? false"""),

        (46, "Suzuvchi nuqtali sonlarning aniqligi (Epsilon)",
         "Kasr sonlarni taqqoslashda to'g'ridan-to'g'ri tenglik o'rniga epsilon aniqligidan foydalaning.",
         """local a = 0.1 + 0.2
local b = 0.3

print("To'g'ridan-to'g'ri tengmi? " .. tostring(a == b))

local EPSILON = 1e-9
local isEqual = math.abs(a - b) < EPSILON
print("Epsilon bilan tengmi? " .. tostring(isEqual))
""",
         "Suzuvchi nuqtali sonlar kompyuter xotirasida ikkilik kasr sifatida saqlangani uchun noaniqlik paydo bo'ladi.",
         """To'g'ridan-to'g'ri tengmi? false\nEpsilon bilan tengmi? true"""),

        (47, "UTF-8 satrlar: Bayt uzunligi va belgi soni farqi",
         "Kirill yoki maxsus belgili satrning bayt uzunligi va haqiqiy belgilar sonini taqqoslang.",
         """local text = "O'zbekiston"
local utf8Text = "Ал-Хоразмий"

print("Lotincha bayt hajmi: " .. #text)
print("Kirillcha bayt hajmi: " .. #utf8Text)
print("Kirillcha belgilar soni: " .. utf8.len(utf8Text))
""",
         "'#' operatori baytlarni sanaydi. UTF-8 belgilar 2-4 bayt egallagani uchun `utf8.len()` funksiyasi ishlatiladi.",
         """Lotincha bayt hajmi: 11\nKirillcha bayt hajmi: 21\nKirillcha belgilar soni: 11"""),

        (48, "utf8 standart kutubxonasi va kodlar",
         "Satrdagi har bir UTF-8 belgining kod nuqtasini (codepoint) ekranga chiqaring.",
         """local word = "Ilm"

for p, c in utf8.codes(word) do
    print(string.format("Pozitsiya: %d, Codepoint: %d, Belgi: %s", p, c, utf8.char(c)))
end
""",
         "`utf8.codes` har bir UTF-8 belgini xavfsiz aylanib chiqish imkonini beradi.",
         """Pozitsiya: 1, Codepoint: 73, Belgi: I\nPozitsiya: 2, Codepoint: 108, Belgi: l\nPozitsiya: 3, Codepoint: 109, Belgi: m"""),

        (49, "Amallar ustuvorligi (Operator Precedence)",
         "Turli arifmetik va mantiqiy operatorlarning hisoblanish tartibini qavslar bilan boshqaring.",
         """local val1 = 5 + 3 * 2 ^ 3
local val2 = ((5 + 3) * 2) ^ 2

print("val1 (standart tartib): " .. val1)
print("val2 (qavslar bilan): " .. val2)
""",
         "Luada ustuvorlik tartibi: ^ > unar (not, #, -, ~) > *, /, //, % > +, - > .. > taqqoslash > and > or.",
         """val1 (standart tartib): 29.0\nval2 (qavslar bilan): 256.0"""),

        (50, "Kompleks vazifa: O'yinchi holatini boshqarish moduli",
         "O'yinchining to'liq ma'lumotlarini o'zgaruvchilar orqali ifodalab, hisob-kitoblarni amalga oshiring.",
         """local username = "Temur_Malik"
local level = 15
local health = 85.5
local isAlive = health > 0
local armor = 20

local incomingDamage = 35
local actualDamage = math.max(0, incomingDamage - armor)
health = health - actualDamage

print("Foydalanuvchi: " .. username)
print("Daraja: " .. level)
print("Yetkazilgan haqiqiy zarar: " .. actualDamage)
print(string.format("Qolgan salomatlik: %.1f", health))
print("Tirikmi: " .. tostring(health > 0))
""",
         "Barcha o'rganilgan asosiy tiplar (string, number, boolean) va operatorlar birlashtirilib, xavfsiz va aniq mantiq hosil qilindi.",
         """Foydalanuvchi: Temur_Malik\nDaraja: 15\nYetkazilgan haqiqiy zarar: 15\nQolgan salomatlik: 70.5\nTirikmi: true""")
    ]

    for item in topic1_data:
        tasks.append(item)

    save_file("lua_01_asoslar_tiplar_va_ozgaruvchilar.md", [format_task(*t) for t in tasks])

if __name__ == "__main__":
    build_topic_01()
