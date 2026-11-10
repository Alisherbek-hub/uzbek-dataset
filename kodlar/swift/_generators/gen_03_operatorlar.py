# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks_data = [
    (
        101,
        "Arifmetik operatorlar (+, -, *, /, %)",
        "Do'kon xaridlari uchun umumiy summa, chegirma, soliq va qoldiqni arifmetik operatorlar yordamida hisoblang.",
        """import Foundation

let subtotal = 120.0
let taxRate = 0.12
let tax = subtotal * taxRate
let discount = 15.0
let total = (subtotal + tax) - discount

let items = 17
let boxCapacity = 5
let fullBoxes = items / boxCapacity
let remainingItems = items % boxCapacity

print("Jami summa: $\\(total)")
print("To'liq qutilar: \\(fullBoxes) ta, Qoldiq tovarlar: \\(remainingItems) ta")
""",
        "Swift standart arifmetik operatorlarni taqdim etadi: qo'shish (+), ayirish (-), ko'paytirish (*), bo'lish (/) va butunli qoldiq (%). Bo'lish amali butun sonlarda butun qismini oladi.",
        """Jami summa: $119.4
To'liq qutilar: 3 ta, Qoldiq tovarlar: 2 ta"""
    ),
    (
        102,
        "Murakkab biriktirish operatorlari (Compound Assignment: +=, -=, *=, /=)",
        "O'yinchining tangalari va ko'paytiruvchisini (multiplier) qisqa biriktirish operatorlari bilan o'zgartiring.",
        """import Foundation

var coins = 50
coins += 25  // 75
coins -= 10  // 65
coins *= 2   // 130
coins /= 5   // 26

print("Yakuniy tangalar soni: \\(coins)")
""",
        "Murakkab biriktirish operatorlari hisoblash va natijani o'sha o'zgaruvchiga qayta yozish amallarini bitta ifodada birlashtiradi.",
        """Yakuniy tangalar soni: 26"""
    ),
    (
        103,
        "Taqqoslash operatorlari (Comparison Operators)",
        "Ikki serverning javob tezligini (latency) o'zaro taqqoslang.",
        """import Foundation

let serverSpeedA = 45
let serverSpeedB = 60

print("A va B tengmi? \\(serverSpeedA == serverSpeedB)")
print("A va B teng emasmi? \\(serverSpeedA != serverSpeedB)")
print("A tezroqmi (kichikroq latency)? \\(serverSpeedA < serverSpeedB)")
print("A sekinroqmi? \\(serverSpeedA > serverSpeedB)")
""",
        "Taqqoslash operatorlari (==, !=, <, >, <=, >=) ikkita qiymatni solishtirib Bool natija (true yoki false) qaytaradi.",
        """A va B tengmi? false
A va B teng emasmi? true
A tezroqmi (kichikroq latency)? true
A sekinroqmi? false"""
    ),
    (
        104,
        "Ternary shart operatori (Ternary Conditional Operator)",
        "Foydalanuvchining balliga qarab 'O'tdi' yoki 'Yiqildi' statusini ternary operator orqali belgilang.",
        """import Foundation

let score = 78
let resultStatus = score >= 60 ? "Muvaffaqiyatli o'tdi" : "Imtihondan yiqildi"

print("Imtihon natijasi: \\(resultStatus)")
""",
        "Ternary operator 'shart ? qiymat1 : qiymat2' shaklida ishlaydi. U uchta operandga ega yagona operator bo'lib, oddiy if-else o'rnini bitta toza qatorda bosadi.",
        """Imtihon natijasi: Muvaffaqiyatli o'tdi"""
    ),
    (
        105,
        "Mantiqiy operatorlar: NOT (!), AND (&&), OR (||)",
        "Foydalanuvchining tizimga kirish huquqini bir nechta mantiqiy shartlar bilan tekshiring.",
        """import Foundation

let hasValidPassword = true
let hasTwoFactorAuth = false
let isAdministrator = true

let canLogin = (hasValidPassword && hasTwoFactorAuth) || isAdministrator
print("Tizimga kirishga ruxsat: \\(canLogin)")
print("Parol noto'g'rimi? \\(!hasValidPassword)")
""",
        "&& (mantiqiy KO'PAYTIRISH) ikkala tomon true bo'lgandagina true beradi, || (mantiqiy QO'SHISH) esa kamida bittasi true bo'lsa kifoya, ! esa qiymatni teskarisiga o'giradi.",
        """Tizimga kirishga ruxsat: true
Parol noto'g'rimi? false"""
    ),
    (
        106,
        "Qisqa tutashuv (Short-Circuit Evaluation)",
        "Mantiqiy operatorlarda ikkinchi shart qachon tekshirilmasdan qolishini ko'rsating.",
        """import Foundation

func checkHeavyDatabase() -> Bool {
    print("OGOHLANTIRISH: Og'ir baza tekshirildi!")
    return true
}

let isGuest = false

// Birinchi shart false bo'lgani uchun checkHeavyDatabase() umuman chaqirilmaydi!
if isGuest && checkHeavyDatabase() {
    print("Xush kelibsiz")
} else {
    print("So'rov rad etildi (baza chaqirilmadi).")
}
""",
        "Swift mantiqiy ifodalarda qisqa tutashuvdan foydalanadi: '&&' amali chap tomon false bo'lsa, o'ng tomonni hisoblab o'tirmaydi.",
        """So'rov rad etildi (baza chaqirilmadi)."""
    ),
    (
        107,
        "Yopiq oraliq operatori (Closed Range: a...b)",
        "1 dan 5 gacha bo'lgan barcha sonlarni yopiq oraliq yordamida ekranga chiqaring.",
        """import Foundation

let closedRange = 1...5
print("Oraliq chegaralari: \\(closedRange.lowerBound) dan \\(closedRange.upperBound) gacha")

for num in closedRange {
    print("Son: \\(num)")
}
""",
        "'a...b' operatori a dan b gacha bo'lgan barcha qiymatlarni (b ni ham qo'shgan holda) o'z ichiga oladi.",
        """Oraliq chegaralari: 1 dan 5 gacha
Son: 1
Son: 2
Son: 3
Son: 4
Son: 5"""
    ),
    (
        108,
        "Yarim ochiq oraliq operatori (Half-Open Range: a..<b)",
        "Massiv indekslari bo'ylab yarim ochiq oraliq bilan xavfsiz aylaning.",
        """import Foundation

let names = ["Ali", "Vali", "Sami", "Gani"]
let range = 0..<names.count

for i in range {
    print("Indeks \\(i): \\(names[i])")
}
""",
        "'a..<b' operatori a dan b gacha bo'lgan qiymatlarni oladi, ammo b ning o'zini kiritmaydi. Bu 0 dan boshlanuvchi massiv indekslari uchun idealdir.",
        """Indeks 0: Ali
Indeks 1: Vali
Indeks 2: Sami
Indeks 3: Gani"""
    ),
    (
        109,
        "Bir tomonlama oraliq operatorlari (One-Sided Ranges)",
        "Massivdan muayyan indeksdan boshlab oxirigacha bo'lgan qismini bir tomonlama oraliq bilan oling.",
        """import Foundation

let devices = ["iPhone", "iPad", "MacBook", "Apple Watch", "Apple Vision"]

let fromIndex2 = devices[2...]
let upToIndex2 = devices[..<2]

print("2-indeksdan oxirigacha: \\(Array(fromIndex2))")
print("2-indeksgacha: \\(Array(upToIndex2))")
""",
        "Bir tomonlama oraliqlar ('2...', '...2', '..<2') massivlarni tilimlashda (slicing) juda qulay bo'lib, chegaralardan birini avtomatik to'plam uzunligiga moslaydi.",
        """2-indeksdan oxirigacha: ["MacBook", "Apple Watch", "Apple Vision"]
2-indeksgacha: ["iPhone", "iPad"]"""
    ),
    (
        110,
        "Oraliqda mavjudlikni tekshirish: contains va ~=",
        "Foydalanuvchi yoshi yosh toifasi oralig'iga kirishini tekshiring.",
        """import Foundation

let teenagerRange = 13...19
let age = 16

print("contains: \\(teenagerRange.contains(age))")
print("~= operatori: \\(teenagerRange ~= age)")
""",
        "'range.contains(x)' orqali qiymat oraliqda bor-yo'qligi tekshiriladi. '~=' esa pattern matching operatori bo'lib, switch-case ichida ham ayni shu mantiq ishlaydi.",
        """contains: true
~= operatori: true"""
    ),
    (
        111,
        "if-else shartli tarmoqlanishi",
        "Haroratga qarab ob-havo tavsiyasini if-else yordamida bering.",
        """import Foundation

let temperature = 32

if temperature > 30 {
    print("Kun juda issiq, ko'proq suv iching.")
} else {
    print("Ob-havo me'yorida.")
}
""",
        "Swift-da 'if' shartidan so'ng qavs () qo'yish majburiy emas, biroq bajariluvchi kod jingalak qavs ({ }) ichida bo'lishi qat'iy talab qilinadi.",
        """Kun juda issiq, ko'proq suv iching."""
    ),
    (
        112,
        "if - else if - else ko'p tarmoqli boshqaruv",
        "Talabaning bahosiga qarab darajasini (A, B, C, F) aniqlang.",
        """import Foundation

let score = 84

if score >= 90 {
    print("Daraja: A (A'lo)")
} else if score >= 80 {
    print("Daraja: B (Yaxshi)")
} else if score >= 70 {
    print("Daraja: C (Qoniqarli)")
} else {
    print("Daraja: F (Qoniqarsiz)")
}
""",
        "Ko'p tarmoqli shartlar yuqoridan pastga ketma-ket tekshiriladi va birinchi to'g'ri kelgan blok bajarilishi bilan qolganlari o'tkazib yuboriladi.",
        """Daraja: B (Yaxshi)"""
    ),
    (
        113,
        "Swift 5.9 If va Switch ifodalari (Expressions)",
        "Swift 5.9-da qo'shilgan 'if' ni to'g'ridan-to'g'ri o'zgaruvchiga qiymat sifatida biriktirish imkoniyatidan foydalaning.",
        """import Foundation

let speed = 110
let warningMessage = if speed > 100 {
    "Diqqat! Tezlik oshirildi."
} else {
    "Tezlik me'yorida."
}

print(warningMessage)
""",
        "Swift 5.9 dan boshlab 'if' va 'switch' faqat operator (statement) emas, balki qiymat qaytaruvchi ifoda (expression) sifatida ham ishlay oladi.",
        """Diqqat! Tezlik oshirildi."""
    ),
    (
        114,
        "switch-case asoslari va to'liqlik (exhaustiveness)",
        "Hafta kuni raqamiga qarab kun nomini chop etuvchi to'liq switch tuzing.",
        """import Foundation

let dayNumber = 3

switch dayNumber {
case 1:
    print("Dushanba")
case 2:
    print("Seshanba")
case 3:
    print("Chorshanba")
default:
    print("Boshqa kun")
}
""",
        "Swift-da 'switch' to'liq (exhaustive) bo'lishi shart, ya'ni mumkin bo'lgan barcha holatlar qamrab olinishi yoki 'default' bloki yozilishi shart. C tilidan farqli ravishda avtomatik 'break' bo'ladi.",
        """Chorshanba"""
    ),
    (
        115,
        "switch-case da bir nechta qiymatni guruhlash",
        "Harflar unli yoki undosh ekanligini vergul bilan guruhlangan case larda tekshiring.",
        """import Foundation

let letter: Character = "e"

switch letter {
case "a", "e", "i", "o", "u":
    print("'\\(letter)' - unli tovush.")
default:
    print("'\\(letter)' - undosh tovush yoki boshqa belgi.")
}
""",
        "Bitta 'case' bandida vergul bilan bir nechta qiymatni ko'rsatish mumkin, agar ulardan biri mos kelsa case bloki bajariladi.",
        """'e' - unli tovush."""
    ),
    (
        116,
        "switch-case da oraliqlar (Interval Matching)",
        "Tovarlar narxining toifasini oraliqlar bo'yicha switch yordamida aniqlang.",
        """import Foundation

let itemPrice = 250

switch itemPrice {
case 0..<50:
    print("Hamyonbop toifa")
case 50..<200:
    print("O'rta toifa")
case 200...1000:
    print("Premium toifa")
default:
    print("Eksklyuziv narx")
}
""",
        "Swift switch operatori oraliqlar ('0..<50', '200...1000') bilan to'g'ridan-to'g'ri moslashishni qo'llab-quvvatlaydi.",
        """Premium toifa"""
    ),
    (
        117,
        "switch-case da Tuple Pattern Matching",
        "2D koordinata tekisligida nuqtaning qaysi o'qda yoki koordinata boshida yotganini aniqlang.",
        """import Foundation

let point = (0, 5)

switch point {
case (0, 0):
    print("Koordinata boshi")
case (_, 0):
    print("X o'qida yotibdi")
case (0, _):
    print("Y o'qida yotibdi")
case (-2...2, -2...2):
    print("Markaziy kvadrat ichida")
default:
    print("Tekislikning boshqa nuqtasida")
}
""",
        "Tuple-larni switch orqali tekshirish juda qulay. '_' belgisi har qanday qiymatga mos keladi.",
        """Y o'qida yotibdi"""
    ),
    (
        118,
        "switch-case da Value Binding (let)",
        "Tuple ichidagi qiymatni case ichida yangi o'zgaruvchiga bog'lab oling.",
        """import Foundation

let anotherPoint = (2, 0)

switch anotherPoint {
case (let x, 0):
    print("X o'qida yotadi, x qiymati: \\(x)")
case (0, let y):
    print("Y o'qida yotadi, y qiymati: \\(y)")
case let (x, y):
    print("Ixtiyoriy nuqta: (\\(x), \\(y))")
}
""",
        "Value Binding orqali case mos kelganida uning bir yoki bir nechta qismini vaqtinchalik o'zgarmasga (let) biriktirib blok ichida ishlatish mumkin.",
        """X o'qida yotadi, x qiymati: 2"""
    ),
    (
        119,
        "switch-case da 'where' shartli filtrlash",
        "Nuqta koordinatalari tengligini (x == y yoki x == -y) where bandi bilan tekshiring.",
        """import Foundation

let point = (4, -4)

switch point {
case let (x, y) where x == y:
    print("Nuqta x == y to'g'ri chizig'ida: (\\(x), \\(y))")
case let (x, y) where x == -y:
    print("Nuqta x == -y to'g'ri chizig'ida: (\\(x), \\(y))")
case let (x, y):
    print("Oddiy nuqta: (\\(x), \\(y))")
}
""",
        "'where' kalit so'zi case bandiga qo'shimcha dinamik mantiqiy shart qo'shish imkonini beradi.",
        """Nuqta x == -y to'g'ri chizig'ida: (4, -4)"""
    ),
    (
        120,
        "Murakkab naqshlar: bir nechta qiymatni bog'lash",
        "Ikki xil holatda bir xil o'zgaruvchini bog'lovchi arxitekturaviy switch yozing.",
        """import Foundation

enum OrderStatus {
    case processing(stage: String)
    case inTransit(stage: String)
    case delivered
}

let current = OrderStatus.processing(stage: "Omborda qadoqlanmoqda")

switch current {
case .processing(let info), .inTransit(let info):
    print("Jarayon davom etmoqda: \\(info)")
case .delivered:
    print("Yetkazib berildi.")
}
""",
        "Swift bir nechta case larni birlashtirganda ham ularning ichki parametrlarini bir xil nomli bitta o'zgaruvchiga bog'lashga ruxsat beradi.",
        """Jarayon davom etmoqda: Omborda qadoqlanmoqda"""
    ),
    (
        121,
        "fallthrough operatori",
        "Case bajarilgandan keyin keyingi case ga ataylab o'tib ketishni ko'rsating.",
        """import Foundation

let number = 5
var description = "Raqam \\(number):"

switch number {
case 2, 3, 5, 7:
    description += " tub son,"
    fallthrough
case 1...10:
    description += " 1 dan 10 gacha oraliqda."
default:
    description += " boshqa son."
}

print(description)
""",
        "'fallthrough' operatori o'zidan keyingi case shartini tekshirmasdan to'g'ridan-to'g'ri uning ichidagi kodni ham ijro etadi. C tilidagi standart switch xatti-harakatini hosil qiladi.",
        """Raqam 5: tub son, 1 dan 10 gacha oraliqda."""
    ),
    (
        122,
        "for-in tsikli: Oraliqlar bo'ylab iteratsiya",
        "Kvadratlar jadvalini for-in orqali chop eting.",
        """import Foundation

for i in 1...4 {
    print("\\(i) ning kvadrati = \\(i * i)")
}
""",
        "'for-in' tsikli to'plamlar, massivlar yoki oraliqlar bo'ylab ketma-ket yurishning eng sodda va samarali usulidir.",
        """1 ning kvadrati = 1
2 ning kvadrati = 4
3 ning kvadrati = 9
4 ning kvadrati = 16"""
    ),
    (
        123,
        "for-in tsiklida massiv va lug'atlar bo'ylab aylanish",
        "Lug'atdagi kalit va qiymatlarni for-in tsiklida tuple sifatida oling.",
        """import Foundation

let exchangeRates = ["USD": 12800, "EUR": 13900]

for (currency, rate) in exchangeRates {
    print("Valyuta: \\(currency) -> \\(rate) so'm")
}
""",
        "Lug'at bo'ylab for-in aylanganda har bir element (key, value) korteji shaklida taqdim etiladi.",
        """Valyuta: USD -> 12800 so'm
Valyuta: EUR -> 13900 so'm"""
    ),
    (
        124,
        "Indeks va elementni birga olish: enumerated()",
        "Ro'yxatdagi elementlarni tartib raqami bilan birgalikda chiqaring.",
        """import Foundation

let tasks = ["Kod yozish", "Testlash", "Deploy qilish"]

for (index, task) in tasks.enumerated() {
    print("\\(index + 1). \\(task)")
}
""",
        "'enumerated()' metodi har bir element uchun (offset, element) juftligidan iborat ketma-ketlik hosil qiladi.",
        """1. Kod yozish
2. Testlash
3. Deploy qilish"""
    ),
    (
        125,
        "Qadamli tsikl: stride(from:to:by:) va stride(from:through:by:)",
        "0 dan 10 gacha 2 qadam bilan va 10 dan 0 gacha kamayuvchi tsikl tuzing.",
        """import Foundation

print("To (ochiq):")
for n in stride(from: 0, to: 10, by: 3) {
    print(n, terminator: " ")
}
print("\nThrough (yopiq):")
for n in stride(from: 10, through: 0, by: -5) {
    print(n, terminator: " ")
}
print()
""",
        "'stride(from:to:by:)' oxirgi chegarani olmaydi, 'stride(from:through:by:)' esa oxirgi chegarani ham qamrab oladi.",
        """To (ochiq):
0 3 6 9 
Through (yopiq):
10 5 0"""
    ),
    (
        126,
        "for-in tsiklida 'where' filtri",
        "Massivdagi faqat juft sonlarni tsikl sarlavhasidayoq filtrlang.",
        """import Foundation

let numbers = [12, 17, 24, 33, 40, 55]

for n in numbers where n % 2 == 0 {
    print("Juft son: \\(n)")
}
""",
        "Swift for-in tsikliga 'where' shartini qo'shish imkonini beradi. Shart qanoatlantirilmagan elementlar uchun tsikl tanasi umuman kirmaydi.",
        """Juft son: 12
Juft son: 24
Juft son: 40"""
    ),
    (
        127,
        "Tsiklda indeks o'rniga '_' ishlatish",
        "Amalni shunchaki 3 marta takrorlash uchun indeks o'zgaruvchisidan voz keching.",
        """import Foundation

for _ in 1...3 {
    print("Khorazmiy AI - Yangi Avlod Dasturchilari!")
}
""",
        "Agar tsikl hisoblagichining qiymati blok ichida kerak bo'lmasa, uni '_' bilan almashtirish xotira va kompilyator uchun optimallashuv beradi.",
        """Khorazmiy AI - Yangi Avlod Dasturchilari!
Khorazmiy AI - Yangi Avlod Dasturchilari!
Khorazmiy AI - Yangi Avlod Dasturchilari!"""
    ),
    (
        128,
        "while tsikli: Old shartli takrorlanish",
        "Son 100 dan oshmaguncha uni 2 ga ko'paytirib boruvchi while tsikli yozing.",
        """import Foundation

var value = 5

while value < 100 {
    print("Joriy: \\(value)")
    value *= 2
}

print("Yakuniy: \\(value)")
""",
        "'while' tsikli har bir qadamdan oldin shartni tekshiradi. Agar shart dastlab false bo'lsa, tsikl tanasi biror marta ham bajarilmaydi.",
        """Joriy: 5
Joriy: 10
Joriy: 20
Joriy: 40
Joriy: 80
Yakuniy: 160"""
    ),
    (
        129,
        "repeat-while tsikli: So'nggi shartli takrorlanish",
        "Shart oxirida tekshiriladigan va kamida 1 marta albatta ishlaydigan tsiklni ko'rsating.",
        """import Foundation

var counter = 10

repeat {
    print("repeat-while tanasi ishladi, counter = \\(counter)")
    counter += 1
} while counter < 5

print("Tsikldan keyin.")
""",
        "'repeat-while' boshqa tillardagi 'do-while' ga teng. Shart false bo'lsa ham uning tanasi kamida bir marta bajariladi.",
        """repeat-while tanasi ishladi, counter = 10
Tsikldan keyin."""
    ),
    (
        130,
        "break operatori orqali tsikldan chiqish",
        "Qidirilayotgan qiymat topilganda tsiklni darhol to'xtating.",
        """import Foundation

let targets = ["Kitob", "Daftar", "Qalam", "O'chirg'ich"]

for item in targets {
    if item == "Qalam" {
        print("Topildi: \\(item)! Qidiruv to'xtatildi.")
        break
    }
    print("Tekshirildi: \\(item)")
}
""",
        "'break' operatori o'zi joylashgan eng yaqin tsikl ijrosini shu zahotiyoq butunlay yakunlaydi.",
        """Tekshirildi: Kitob
Tekshirildi: Daftar
Topildi: Qalam! Qidiruv to'xtatildi."""
    ),
    (
        131,
        "continue operatori",
        "Toq sonlarni tashlab o'tib faqat musbatlarini qayta ishlang.",
        """import Foundation

for i in 1...6 {
    if i % 2 != 0 {
        continue // Toq son bo'lsa keyingi iteratsiyaga o'tadi
    }
    print("Ishlandi: \\(i)")
}
""",
        "'continue' operatori joriy iteratsiyaning qolgan qismini o'tkazib yuborib, darhol tsiklning navbatdagi bosqichiga o'tadi.",
        """Ishlandi: 2
Ishlandi: 4
Ishlandi: 6"""
    ),
    (
        132,
        "Belgilangan tsikllar (Labeled Statements)",
        "Ichma-ich tsikllarda tashqi tsiklni to'g'ridan-to'g'ri to'xtatuvchi yorliq (label) qo'llang.",
        """import Foundation

outerLoop: for i in 1...3 {
    for j in 1...3 {
        if i == 2 && j == 2 {
            print("Ichki nuqtadan tashqi tsikl to'xtatildi! i=\\(i), j=\\(j)")
            break outerLoop
        }
        print("i=\\(i), j=\\(j)")
    }
}
""",
        "Swift tsikllarga 'nom:' ko'rinishida yorliq berish imkonini beradi. 'break outerLoop' yoki 'continue outerLoop' orqali ichki chuqurlikdan to'g'ridan-to'g'ri tashqi tsiklni boshqarish mumkin.",
        """i=1, j=1
i=1, j=2
i=1, j=3
i=2, j=1
Ichki nuqtadan tashqi tsikl to'xtatildi! i=2, j=2"""
    ),
    (
        133,
        "Tsikl ichida 'guard' bilan saralash",
        "Tsiklda noto'g'ri elementlarni 'guard' orqali erta chiqarib yuboring.",
        """import Foundation

let emails: [String?] = ["ali@mail.uz", nil, "not-valid", "sami@gmail.com"]

for item in emails {
    guard let email = item, email.contains("@") else {
        continue
    }
    print("To'g'ri pochta: \\(email)")
}
""",
        "Tsikl ichida guard yordamida shart qanoatlantirilmaganda 'continue' qilish juda qulay va ixchamdir.",
        """To'g'ri pochta: ali@mail.uz
To'g'ri pochta: sami@gmail.com"""
    ),
    (
        134,
        "Enum qiymatlarini switch bilan to'liq tahlil qilish",
        "Yo'nalish kompasini Enum va switch yordamida dasturlang.",
        """import Foundation

enum Direction {
    case north, south, east, west
}

let heading = Direction.north

switch heading {
case .north:
    print("Shimol tomonga yo'naltirilgan.")
case .south:
    print("Janub tomonga yo'naltirilgan.")
case .east:
    print("Sharq tomonga yo'naltirilgan.")
case .west:
    print("G'arb tomonga yo'naltirilgan.")
}
""",
        "Enum barcha holatlari switch-da yozilsa, 'default' bandi talab qilinmaydi va kelajakda yangi holat qo'shilsa kompilyator uni talab qilib xato ko'rsatadi.",
        """Shimol tomonga yo'naltirilgan."""
    ),
    (
        135,
        "Swift 5.9 Switch Expression bilan qiymat qaytarish",
        "Switch orqali holatga qarab to'g'ridan-to'g'ri o'zgaruvchiga matn qiymatini biriktiring.",
        """import Foundation

enum NetworkSpeed {
    case slow, normal, ultraFast
}

let speed = NetworkSpeed.ultraFast

let latencyText = switch speed {
case .slow: "Yuqori kechikish (150ms+)"
case .normal: "Oddiy tezlik (40ms)"
case .ultraFast: "Minimal kechikish (<5ms)"
}

print(latencyText)
""",
        "Swift 5.9 da 'switch' ifoda sifatida ishlay oladi, har bir case bitta qiymatni avtomatik qaytaradi.",
        """Minimal kechikish (<5ms)"""
    ),
    (
        136,
        "Bitwise operatorlar: AND (&), OR (|), XOR (^)",
        "Bayt darajasidagi bit operatsiyalarini bajaring.",
        """import Foundation

let byteA: UInt8 = 0b1100_1010
let byteB: UInt8 = 0b1010_0101

let bitAnd = byteA & byteB
let bitOr = byteA | byteB
let bitXor = byteA ^ byteB

print("AND: 0b\\(String(bitAnd, radix: 2))")
print("OR:  0b\\(String(bitOr, radix: 2))")
print("XOR: 0b\\(String(bitXor, radix: 2))")
""",
        "Bit darajasidagi amallar past darajadagi dasturlash, kriptografiya va tarmoq protokollarida keng qo'llaniladi.",
        """AND: 0b10000000
OR:  0b11101111
XOR: 0b1101111"""
    ),
    (
        137,
        "Bitwise NOT (~) operatori",
        "Barcha bitlarni teskarisiga o'giruvchi NOT operatorini ko'rsating.",
        """import Foundation

let initialBits: UInt8 = 0b0000_1111
let invertedBits = ~initialBits

print("Asl bitlar:     0b00001111")
print("Inverted (NOT): 0b\\(String(invertedBits, radix: 2))")
""",
        "Bitwise NOT (~) barcha 0 larni 1 ga, 1 larni 0 ga aylantiradi.",
        """Asl bitlar:     0b00001111
Inverted (NOT): 0b11110000"""
    ),
    (
        138,
        "Bitwise Shift operatorlari (<<, >>)",
        "Sonni 2 ga ko'paytirish va bo'lishning eng tezkor apparat usulini ko'rsating.",
        """import Foundation

let baseValue: UInt8 = 4 // 0b0000_0100

let shiftedLeft = baseValue << 2   // 4 * 4 = 16
let shiftedRight = baseValue >> 1  // 4 / 2 = 2

print("Chapga 2 bit: \\(shiftedLeft)")
print("O'ngga 1 bit: \\(shiftedRight)")
""",
        "Chapga siljitish (<<) sonni 2 ning darajalariga ko'paytiradi, o'ngga siljitish (>>) esa 2 ning darajalariga bo'ladi.",
        """Chapga 2 bit: 16
O'ngga 1 bit: 2"""
    ),
    (
        139,
        "Maxsus operator yaratish (Custom Operator)",
        "Ikki sonning darajasini hisoblovchi '**' maxsus operatorini e'lon qiling.",
        """import Foundation

infix operator **

func ** (base: Double, power: Double) -> Double {
    return pow(base, power)
}

let result = 2.0 ** 8.0
print("2 ning 8-darajasi: \\(result)")
""",
        "Swift dasturchiga o'zining shaxsiy operatorlarini (prefix, infix, postfix) e'lon qilish va ularning ustunligini belgilash imkonini beradi.",
        """2 ning 8-darajasi: 256.0"""
    ),
    (
        140,
        "Operator ustunligi va guruhlash (Precedence)",
        "Arifmetik amallarning bajarilish ketma-ketligini ko'rsatuvchi dastur tuzing.",
        """import Foundation

let rawCalc = 2 + 3 * 4
let groupedCalc = (2 + 3) * 4

print("rawCalc (ko'paytirish ustun): \\(rawCalc)")
print("groupedCalc (qavs ustun): \\(groupedCalc)")
""",
        "Swift matematikadagi standart operatorlar ustunligiga qat'iy amal qiladi. Qavslar ustunlikni o'zgartiradi.",
        """rawCalc (ko'paytirish ustun): 14
groupedCalc (qavs ustun): 20"""
    ),
    (
        141,
        "Identiklik operatorlari: === va !==",
        "Ikki havola aynan bitta xotira ob'ektiga ishora qilayotganini tekshiring.",
        """import Foundation

class Session {
    let token = "TOKEN_ABC"
}

let s1 = Session()
let s2 = s1
let s3 = Session()

print("s1 === s2: \\(s1 === s2)")
print("s1 === s3: \\(s1 === s3)")
""",
        "'===' operatori ikkita havola xotirada aynan bitta manzilga (instance) ishora qilayotganini tekshiradi (faqat class larda ishlaydi).",
        """s1 === s2: true
s1 === s3: false"""
    ),
    (
        142,
        "Pattern Matching operatori: ~= ning imkoniyatlari",
        "Maxsus struct uchun ~= operatorini qayta yuklab (overload), switch-case da ishlatishni ko'rsating.",
        """import Foundation

struct AgeCategory {
    let minAge: Int
    let maxAge: Int
    
    static func ~= (category: AgeCategory, age: Int) -> Bool {
        return age >= category.minAge && age <= category.maxAge
    }
}

let childCategory = AgeCategory(minAge: 0, maxAge: 12)
let currentAge = 8

switch currentAge {
case childCategory:
    print("Bola toifasiga to'g'ri keladi.")
default:
    print("Boshqa toifa.")
}
""",
        "'~=' operatorini qayta yuklash orqali ixtiyoriy turdagi ob'ektlarni switch-case da pattern matching bilan solishtirish mumkin.",
        """Bola toifasiga to'g'ri keladi."""
    ),
    (
        143,
        "Tsikllarda teskari tartibda yurish: reversed()",
        "Ortga hisoblashni 'reversed()' orqali bajaring.",
        """import Foundation

for i in (1...5).reversed() {
    print("\\(i)...", terminator: " ")
}
print("Start!")
""",
        "'reversed()' to'plamni nusxalamasdan, uning ustida teskari ko'rinish (ReversedCollection) hosil qiladi.",
        """5... 4... 3... 2... 1... Start!"""
    ),
    (
        144,
        "Ikkita ketma-ketlikni juftlash: zip()",
        "Talabalar va ularning baholarini bitta tsiklda zip yordamida birlashtiring.",
        """import Foundation

let students = ["Ali", "Vali", "Sami"]
let marks = [95, 87, 92]

for (name, mark) in zip(students, marks) {
    print("\\(name): \\(mark) ball")
}
""",
        "'zip(seq1, seq2)' ikkita ketma-ketlikdan juftliklar ketma-ketligini hosil qiladi. Ular uzunligi har xil bo'lsa, qisqaroqiga qarab to'xtaydi.",
        """Ali: 95 ball
Vali: 87 ball
Sami: 92 ball"""
    ),
    (
        145,
        "Cheksiz tsikllarni xavfsiz boshqarish",
        "while true tsiklini xavfsiz to'xtatish mexanizmini yozing.",
        """import Foundation

var attempts = 0

while true {
    attempts += 1
    if attempts >= 3 {
        print("Maksimal urinishlar soniga yetdi, chiqildi.")
        break
    }
}
""",
        "'while true' tsikli cheksiz ishlaydi va uning ichida albatta 'break' yoki 'return' sharti bo'lishi shart.",
        """Maksimal urinishlar soniga yetdi, chiqildi."""
    ),
    (
        146,
        "Murakkab shartlar va qavslarning roli",
        "Chegirma berish uchun murakkab mantiqiy formulani tahlil qiling.",
        """import Foundation

let isLoyal = true
let isWeekend = false
let cartAmount = 120.0

let getDiscount = (isLoyal || isWeekend) && cartAmount > 100.0
print("Chegirma beriladimi? \\(getDiscount)")
""",
        "Mantiqiy ifodalarda qavslar birinchi bo'lib hisoblanadi va kodning noaniq talqin qilinishini oldini oladi.",
        """Chegirma beriladimi? true"""
    ),
    (
        147,
        "@unknown default: Kelajakdagi enum holatlarini xavfsiz kutib olish",
        "Kelajakda tizimga yangi enum qiymatlari qo'shilganda ogohlantirish beruvchi @unknown default ni ko'rsating.",
        """import Foundation

enum NetworkType {
    case wifi
    case cellular
    case ethernet
}

let conn = NetworkType.wifi

switch conn {
case .wifi:
    print("Wi-Fi tarmog'i")
case .cellular:
    print("Mobil tarmoq")
@unknown default:
    print("Yangi yoki noma'lum tarmoq turi")
}
""",
        "'@unknown default' switch to'liq bo'lsa-da, kelajakda yangi enum holatlari qo'shilsa kompilyator ogohlantirish (warning) berishi uchun qo'yiladi.",
        """Wi-Fi tarmog'i"""
    ),
    (
        148,
        "Tsikl ichida 'defer' operatorining ishlash tartibi",
        "Har bir iteratsiya tugaganda bajariluvchi defer blokini ko'rsating.",
        """import Foundation

for i in 1...3 {
    defer {
        print("Iteratsiya \\(i) yakunlandi.")
    }
    print("Iteratsiya \\(i) bajarilmoqda...")
}
""",
        "'defer' bloki o'zi yozilgan skopdan (scope) chiqish oldidan doimo ijro etiladi.",
        """Iteratsiya 1 bajarilmoqda...
Iteratsiya 1 yakunlandi.
Iteratsiya 2 bajarilmoqda...
Iteratsiya 2 yakunlandi.
Iteratsiya 3 bajarilmoqda...
Iteratsiya 3 yakunlandi."""
    ),
    (
        149,
        "Fibonachchi ketma-ketligini tsiklda hisoblash",
        "Boshqaruv oqimlari orqali dastlabki 7 ta Fibonachchi sonlarini hisoblang.",
        """import Foundation

var a = 0
var b = 1
var sequence = [a, b]

for _ in 2..<7 {
    let next = a + b
    sequence.append(next)
    a = b
    b = next
}

print("Fibonachchi ketma-ketligi: \\(sequence)")
""",
        "Tsikllar va arifmetik amallarning birgalikdagi klassik hisoblash algoritmi.",
        """Fibonachchi ketma-ketligi: [0, 1, 1, 2, 3, 5, 8]"""
    ),
    (
        150,
        "Amaliy loyiha: Boshqaruv oqimlari orqali ATM (Bankomat) simulyatori",
        "Foydalanuvchi pin kodi, balansi, operatsiyalarini (yechish, to'ldirish) boshqaruvchi to'liq ATM moduli.",
        """import Foundation

enum ATMAction {
    case checkBalance
    case withdraw(amount: Double)
    case deposit(amount: Double)
    case exit
}

var currentBalance = 1000.0
let operations: [ATMAction] = [
    .checkBalance,
    .withdraw(amount: 300.0),
    .withdraw(amount: 900.0), // Yetarli mablag' yo'q
    .deposit(amount: 150.0),
    .exit
]

atmLoop: for action in operations {
    switch action {
    case .checkBalance:
        print("Joriy balans: $\\(currentBalance)")
    case .withdraw(let amount) where amount <= currentBalance:
        currentBalance -= amount
        print("Muvaffaqiyatli yechildi: $\\(amount). Qoldiq: $\\(currentBalance)")
    case .withdraw(let amount):
        print("Xatolik: Balansda yetarli mablag' yo'q! So'ralgan: $\\(amount), Mavjud: $\\(currentBalance)")
    case .deposit(let amount):
        currentBalance += amount
        print("Hisob to'ldirildi: $\\(amount). Yangi balans: $\\(currentBalance)")
    case .exit:
        print("Seans yakunlandi. Xayr!")
        break atmLoop
    }
}
""",
        "Ushbu yakuniy loyihada 'switch-case', 'where' filtri, 'break labeledStatement', enum associated values va arifmetik amallar mukammal tizimda jamlandi.",
        """Joriy balans: $1000.0
Muvaffaqiyatli yechildi: $300.0. Qoldiq: $700.0
Xatolik: Balansda yetarli mablag' yo'q! So'ralgan: $900.0, Mavjud: $700.0
Hisob to'ldirildi: $150.0. Yangi balans: $850.0
Seans yakunlandi. Xayr!"""
    )
]

tasks = [format_task(*t) for t in tasks_data]
save_file("swift_03_operatorlar_va_boshqaruv_oqimlari.md", tasks)
