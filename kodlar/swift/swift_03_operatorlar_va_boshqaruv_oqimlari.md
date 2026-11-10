# 101-Topshiriq: Arifmetik operatorlar (+, -, *, /, %)
## Topshiriq sharti:
Do'kon xaridlari uchun umumiy summa, chegirma, soliq va qoldiqni arifmetik operatorlar yordamida hisoblang.

## Yechim (Swift kodi):
```swift
import Foundation

let subtotal = 120.0
let taxRate = 0.12
let tax = subtotal * taxRate
let discount = 15.0
let total = (subtotal + tax) - discount

let items = 17
let boxCapacity = 5
let fullBoxes = items / boxCapacity
let remainingItems = items % boxCapacity

print("Jami summa: $\(total)")
print("To'liq qutilar: \(fullBoxes) ta, Qoldiq tovarlar: \(remainingItems) ta")
```

## Tushuntirish va Mantiq:
Swift standart arifmetik operatorlarni taqdim etadi: qo'shish (+), ayirish (-), ko'paytirish (*), bo'lish (/) va butunli qoldiq (%). Bo'lish amali butun sonlarda butun qismini oladi.

## Ishlash natijasi:
```text
Jami summa: $119.4
To'liq qutilar: 3 ta, Qoldiq tovarlar: 2 ta
```


# 102-Topshiriq: Murakkab biriktirish operatorlari (Compound Assignment: +=, -=, *=, /=)
## Topshiriq sharti:
O'yinchining tangalari va ko'paytiruvchisini (multiplier) qisqa biriktirish operatorlari bilan o'zgartiring.

## Yechim (Swift kodi):
```swift
import Foundation

var coins = 50
coins += 25  // 75
coins -= 10  // 65
coins *= 2   // 130
coins /= 5   // 26

print("Yakuniy tangalar soni: \(coins)")
```

## Tushuntirish va Mantiq:
Murakkab biriktirish operatorlari hisoblash va natijani o'sha o'zgaruvchiga qayta yozish amallarini bitta ifodada birlashtiradi.

## Ishlash natijasi:
```text
Yakuniy tangalar soni: 26
```


# 103-Topshiriq: Taqqoslash operatorlari (Comparison Operators)
## Topshiriq sharti:
Ikki serverning javob tezligini (latency) o'zaro taqqoslang.

## Yechim (Swift kodi):
```swift
import Foundation

let serverSpeedA = 45
let serverSpeedB = 60

print("A va B tengmi? \(serverSpeedA == serverSpeedB)")
print("A va B teng emasmi? \(serverSpeedA != serverSpeedB)")
print("A tezroqmi (kichikroq latency)? \(serverSpeedA < serverSpeedB)")
print("A sekinroqmi? \(serverSpeedA > serverSpeedB)")
```

## Tushuntirish va Mantiq:
Taqqoslash operatorlari (==, !=, <, >, <=, >=) ikkita qiymatni solishtirib Bool natija (true yoki false) qaytaradi.

## Ishlash natijasi:
```text
A va B tengmi? false
A va B teng emasmi? true
A tezroqmi (kichikroq latency)? true
A sekinroqmi? false
```


# 104-Topshiriq: Ternary shart operatori (Ternary Conditional Operator)
## Topshiriq sharti:
Foydalanuvchining balliga qarab 'O'tdi' yoki 'Yiqildi' statusini ternary operator orqali belgilang.

## Yechim (Swift kodi):
```swift
import Foundation

let score = 78
let resultStatus = score >= 60 ? "Muvaffaqiyatli o'tdi" : "Imtihondan yiqildi"

print("Imtihon natijasi: \(resultStatus)")
```

## Tushuntirish va Mantiq:
Ternary operator 'shart ? qiymat1 : qiymat2' shaklida ishlaydi. U uchta operandga ega yagona operator bo'lib, oddiy if-else o'rnini bitta toza qatorda bosadi.

## Ishlash natijasi:
```text
Imtihon natijasi: Muvaffaqiyatli o'tdi
```


# 105-Topshiriq: Mantiqiy operatorlar: NOT (!), AND (&&), OR (||)
## Topshiriq sharti:
Foydalanuvchining tizimga kirish huquqini bir nechta mantiqiy shartlar bilan tekshiring.

## Yechim (Swift kodi):
```swift
import Foundation

let hasValidPassword = true
let hasTwoFactorAuth = false
let isAdministrator = true

let canLogin = (hasValidPassword && hasTwoFactorAuth) || isAdministrator
print("Tizimga kirishga ruxsat: \(canLogin)")
print("Parol noto'g'rimi? \(!hasValidPassword)")
```

## Tushuntirish va Mantiq:
&& (mantiqiy KO'PAYTIRISH) ikkala tomon true bo'lgandagina true beradi, || (mantiqiy QO'SHISH) esa kamida bittasi true bo'lsa kifoya, ! esa qiymatni teskarisiga o'giradi.

## Ishlash natijasi:
```text
Tizimga kirishga ruxsat: true
Parol noto'g'rimi? false
```


# 106-Topshiriq: Qisqa tutashuv (Short-Circuit Evaluation)
## Topshiriq sharti:
Mantiqiy operatorlarda ikkinchi shart qachon tekshirilmasdan qolishini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

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
```

## Tushuntirish va Mantiq:
Swift mantiqiy ifodalarda qisqa tutashuvdan foydalanadi: '&&' amali chap tomon false bo'lsa, o'ng tomonni hisoblab o'tirmaydi.

## Ishlash natijasi:
```text
So'rov rad etildi (baza chaqirilmadi).
```


# 107-Topshiriq: Yopiq oraliq operatori (Closed Range: a...b)
## Topshiriq sharti:
1 dan 5 gacha bo'lgan barcha sonlarni yopiq oraliq yordamida ekranga chiqaring.

## Yechim (Swift kodi):
```swift
import Foundation

let closedRange = 1...5
print("Oraliq chegaralari: \(closedRange.lowerBound) dan \(closedRange.upperBound) gacha")

for num in closedRange {
    print("Son: \(num)")
}
```

## Tushuntirish va Mantiq:
'a...b' operatori a dan b gacha bo'lgan barcha qiymatlarni (b ni ham qo'shgan holda) o'z ichiga oladi.

## Ishlash natijasi:
```text
Oraliq chegaralari: 1 dan 5 gacha
Son: 1
Son: 2
Son: 3
Son: 4
Son: 5
```


# 108-Topshiriq: Yarim ochiq oraliq operatori (Half-Open Range: a..<b)
## Topshiriq sharti:
Massiv indekslari bo'ylab yarim ochiq oraliq bilan xavfsiz aylaning.

## Yechim (Swift kodi):
```swift
import Foundation

let names = ["Ali", "Vali", "Sami", "Gani"]
let range = 0..<names.count

for i in range {
    print("Indeks \(i): \(names[i])")
}
```

## Tushuntirish va Mantiq:
'a..<b' operatori a dan b gacha bo'lgan qiymatlarni oladi, ammo b ning o'zini kiritmaydi. Bu 0 dan boshlanuvchi massiv indekslari uchun idealdir.

## Ishlash natijasi:
```text
Indeks 0: Ali
Indeks 1: Vali
Indeks 2: Sami
Indeks 3: Gani
```


# 109-Topshiriq: Bir tomonlama oraliq operatorlari (One-Sided Ranges)
## Topshiriq sharti:
Massivdan muayyan indeksdan boshlab oxirigacha bo'lgan qismini bir tomonlama oraliq bilan oling.

## Yechim (Swift kodi):
```swift
import Foundation

let devices = ["iPhone", "iPad", "MacBook", "Apple Watch", "Apple Vision"]

let fromIndex2 = devices[2...]
let upToIndex2 = devices[..<2]

print("2-indeksdan oxirigacha: \(Array(fromIndex2))")
print("2-indeksgacha: \(Array(upToIndex2))")
```

## Tushuntirish va Mantiq:
Bir tomonlama oraliqlar ('2...', '...2', '..<2') massivlarni tilimlashda (slicing) juda qulay bo'lib, chegaralardan birini avtomatik to'plam uzunligiga moslaydi.

## Ishlash natijasi:
```text
2-indeksdan oxirigacha: ["MacBook", "Apple Watch", "Apple Vision"]
2-indeksgacha: ["iPhone", "iPad"]
```


# 110-Topshiriq: Oraliqda mavjudlikni tekshirish: contains va ~=
## Topshiriq sharti:
Foydalanuvchi yoshi yosh toifasi oralig'iga kirishini tekshiring.

## Yechim (Swift kodi):
```swift
import Foundation

let teenagerRange = 13...19
let age = 16

print("contains: \(teenagerRange.contains(age))")
print("~= operatori: \(teenagerRange ~= age)")
```

## Tushuntirish va Mantiq:
'range.contains(x)' orqali qiymat oraliqda bor-yo'qligi tekshiriladi. '~=' esa pattern matching operatori bo'lib, switch-case ichida ham ayni shu mantiq ishlaydi.

## Ishlash natijasi:
```text
contains: true
~= operatori: true
```


# 111-Topshiriq: if-else shartli tarmoqlanishi
## Topshiriq sharti:
Haroratga qarab ob-havo tavsiyasini if-else yordamida bering.

## Yechim (Swift kodi):
```swift
import Foundation

let temperature = 32

if temperature > 30 {
    print("Kun juda issiq, ko'proq suv iching.")
} else {
    print("Ob-havo me'yorida.")
}
```

## Tushuntirish va Mantiq:
Swift-da 'if' shartidan so'ng qavs () qo'yish majburiy emas, biroq bajariluvchi kod jingalak qavs ({ }) ichida bo'lishi qat'iy talab qilinadi.

## Ishlash natijasi:
```text
Kun juda issiq, ko'proq suv iching.
```


# 112-Topshiriq: if - else if - else ko'p tarmoqli boshqaruv
## Topshiriq sharti:
Talabaning bahosiga qarab darajasini (A, B, C, F) aniqlang.

## Yechim (Swift kodi):
```swift
import Foundation

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
```

## Tushuntirish va Mantiq:
Ko'p tarmoqli shartlar yuqoridan pastga ketma-ket tekshiriladi va birinchi to'g'ri kelgan blok bajarilishi bilan qolganlari o'tkazib yuboriladi.

## Ishlash natijasi:
```text
Daraja: B (Yaxshi)
```


# 113-Topshiriq: Swift 5.9 If va Switch ifodalari (Expressions)
## Topshiriq sharti:
Swift 5.9-da qo'shilgan 'if' ni to'g'ridan-to'g'ri o'zgaruvchiga qiymat sifatida biriktirish imkoniyatidan foydalaning.

## Yechim (Swift kodi):
```swift
import Foundation

let speed = 110
let warningMessage = if speed > 100 {
    "Diqqat! Tezlik oshirildi."
} else {
    "Tezlik me'yorida."
}

print(warningMessage)
```

## Tushuntirish va Mantiq:
Swift 5.9 dan boshlab 'if' va 'switch' faqat operator (statement) emas, balki qiymat qaytaruvchi ifoda (expression) sifatida ham ishlay oladi.

## Ishlash natijasi:
```text
Diqqat! Tezlik oshirildi.
```


# 114-Topshiriq: switch-case asoslari va to'liqlik (exhaustiveness)
## Topshiriq sharti:
Hafta kuni raqamiga qarab kun nomini chop etuvchi to'liq switch tuzing.

## Yechim (Swift kodi):
```swift
import Foundation

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
```

## Tushuntirish va Mantiq:
Swift-da 'switch' to'liq (exhaustive) bo'lishi shart, ya'ni mumkin bo'lgan barcha holatlar qamrab olinishi yoki 'default' bloki yozilishi shart. C tilidan farqli ravishda avtomatik 'break' bo'ladi.

## Ishlash natijasi:
```text
Chorshanba
```


# 115-Topshiriq: switch-case da bir nechta qiymatni guruhlash
## Topshiriq sharti:
Harflar unli yoki undosh ekanligini vergul bilan guruhlangan case larda tekshiring.

## Yechim (Swift kodi):
```swift
import Foundation

let letter: Character = "e"

switch letter {
case "a", "e", "i", "o", "u":
    print("'\(letter)' - unli tovush.")
default:
    print("'\(letter)' - undosh tovush yoki boshqa belgi.")
}
```

## Tushuntirish va Mantiq:
Bitta 'case' bandida vergul bilan bir nechta qiymatni ko'rsatish mumkin, agar ulardan biri mos kelsa case bloki bajariladi.

## Ishlash natijasi:
```text
'e' - unli tovush.
```


# 116-Topshiriq: switch-case da oraliqlar (Interval Matching)
## Topshiriq sharti:
Tovarlar narxining toifasini oraliqlar bo'yicha switch yordamida aniqlang.

## Yechim (Swift kodi):
```swift
import Foundation

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
```

## Tushuntirish va Mantiq:
Swift switch operatori oraliqlar ('0..<50', '200...1000') bilan to'g'ridan-to'g'ri moslashishni qo'llab-quvvatlaydi.

## Ishlash natijasi:
```text
Premium toifa
```


# 117-Topshiriq: switch-case da Tuple Pattern Matching
## Topshiriq sharti:
2D koordinata tekisligida nuqtaning qaysi o'qda yoki koordinata boshida yotganini aniqlang.

## Yechim (Swift kodi):
```swift
import Foundation

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
```

## Tushuntirish va Mantiq:
Tuple-larni switch orqali tekshirish juda qulay. '_' belgisi har qanday qiymatga mos keladi.

## Ishlash natijasi:
```text
Y o'qida yotibdi
```


# 118-Topshiriq: switch-case da Value Binding (let)
## Topshiriq sharti:
Tuple ichidagi qiymatni case ichida yangi o'zgaruvchiga bog'lab oling.

## Yechim (Swift kodi):
```swift
import Foundation

let anotherPoint = (2, 0)

switch anotherPoint {
case (let x, 0):
    print("X o'qida yotadi, x qiymati: \(x)")
case (0, let y):
    print("Y o'qida yotadi, y qiymati: \(y)")
case let (x, y):
    print("Ixtiyoriy nuqta: (\(x), \(y))")
}
```

## Tushuntirish va Mantiq:
Value Binding orqali case mos kelganida uning bir yoki bir nechta qismini vaqtinchalik o'zgarmasga (let) biriktirib blok ichida ishlatish mumkin.

## Ishlash natijasi:
```text
X o'qida yotadi, x qiymati: 2
```


# 119-Topshiriq: switch-case da 'where' shartli filtrlash
## Topshiriq sharti:
Nuqta koordinatalari tengligini (x == y yoki x == -y) where bandi bilan tekshiring.

## Yechim (Swift kodi):
```swift
import Foundation

let point = (4, -4)

switch point {
case let (x, y) where x == y:
    print("Nuqta x == y to'g'ri chizig'ida: (\(x), \(y))")
case let (x, y) where x == -y:
    print("Nuqta x == -y to'g'ri chizig'ida: (\(x), \(y))")
case let (x, y):
    print("Oddiy nuqta: (\(x), \(y))")
}
```

## Tushuntirish va Mantiq:
'where' kalit so'zi case bandiga qo'shimcha dinamik mantiqiy shart qo'shish imkonini beradi.

## Ishlash natijasi:
```text
Nuqta x == -y to'g'ri chizig'ida: (4, -4)
```


# 120-Topshiriq: Murakkab naqshlar: bir nechta qiymatni bog'lash
## Topshiriq sharti:
Ikki xil holatda bir xil o'zgaruvchini bog'lovchi arxitekturaviy switch yozing.

## Yechim (Swift kodi):
```swift
import Foundation

enum OrderStatus {
    case processing(stage: String)
    case inTransit(stage: String)
    case delivered
}

let current = OrderStatus.processing(stage: "Omborda qadoqlanmoqda")

switch current {
case .processing(let info), .inTransit(let info):
    print("Jarayon davom etmoqda: \(info)")
case .delivered:
    print("Yetkazib berildi.")
}
```

## Tushuntirish va Mantiq:
Swift bir nechta case larni birlashtirganda ham ularning ichki parametrlarini bir xil nomli bitta o'zgaruvchiga bog'lashga ruxsat beradi.

## Ishlash natijasi:
```text
Jarayon davom etmoqda: Omborda qadoqlanmoqda
```


# 121-Topshiriq: fallthrough operatori
## Topshiriq sharti:
Case bajarilgandan keyin keyingi case ga ataylab o'tib ketishni ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

let number = 5
var description = "Raqam \(number):"

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
```

## Tushuntirish va Mantiq:
'fallthrough' operatori o'zidan keyingi case shartini tekshirmasdan to'g'ridan-to'g'ri uning ichidagi kodni ham ijro etadi. C tilidagi standart switch xatti-harakatini hosil qiladi.

## Ishlash natijasi:
```text
Raqam 5: tub son, 1 dan 10 gacha oraliqda.
```


# 122-Topshiriq: for-in tsikli: Oraliqlar bo'ylab iteratsiya
## Topshiriq sharti:
Kvadratlar jadvalini for-in orqali chop eting.

## Yechim (Swift kodi):
```swift
import Foundation

for i in 1...4 {
    print("\(i) ning kvadrati = \(i * i)")
}
```

## Tushuntirish va Mantiq:
'for-in' tsikli to'plamlar, massivlar yoki oraliqlar bo'ylab ketma-ket yurishning eng sodda va samarali usulidir.

## Ishlash natijasi:
```text
1 ning kvadrati = 1
2 ning kvadrati = 4
3 ning kvadrati = 9
4 ning kvadrati = 16
```


# 123-Topshiriq: for-in tsiklida massiv va lug'atlar bo'ylab aylanish
## Topshiriq sharti:
Lug'atdagi kalit va qiymatlarni for-in tsiklida tuple sifatida oling.

## Yechim (Swift kodi):
```swift
import Foundation

let exchangeRates = ["USD": 12800, "EUR": 13900]

for (currency, rate) in exchangeRates {
    print("Valyuta: \(currency) -> \(rate) so'm")
}
```

## Tushuntirish va Mantiq:
Lug'at bo'ylab for-in aylanganda har bir element (key, value) korteji shaklida taqdim etiladi.

## Ishlash natijasi:
```text
Valyuta: USD -> 12800 so'm
Valyuta: EUR -> 13900 so'm
```


# 124-Topshiriq: Indeks va elementni birga olish: enumerated()
## Topshiriq sharti:
Ro'yxatdagi elementlarni tartib raqami bilan birgalikda chiqaring.

## Yechim (Swift kodi):
```swift
import Foundation

let tasks = ["Kod yozish", "Testlash", "Deploy qilish"]

for (index, task) in tasks.enumerated() {
    print("\(index + 1). \(task)")
}
```

## Tushuntirish va Mantiq:
'enumerated()' metodi har bir element uchun (offset, element) juftligidan iborat ketma-ketlik hosil qiladi.

## Ishlash natijasi:
```text
1. Kod yozish
2. Testlash
3. Deploy qilish
```


# 125-Topshiriq: Qadamli tsikl: stride(from:to:by:) va stride(from:through:by:)
## Topshiriq sharti:
0 dan 10 gacha 2 qadam bilan va 10 dan 0 gacha kamayuvchi tsikl tuzing.

## Yechim (Swift kodi):
```swift
import Foundation

print("To (ochiq):")
for n in stride(from: 0, to: 10, by: 3) {
    print(n, terminator: " ")
}
print("
Through (yopiq):")
for n in stride(from: 10, through: 0, by: -5) {
    print(n, terminator: " ")
}
print()
```

## Tushuntirish va Mantiq:
'stride(from:to:by:)' oxirgi chegarani olmaydi, 'stride(from:through:by:)' esa oxirgi chegarani ham qamrab oladi.

## Ishlash natijasi:
```text
To (ochiq):
0 3 6 9 
Through (yopiq):
10 5 0
```


# 126-Topshiriq: for-in tsiklida 'where' filtri
## Topshiriq sharti:
Massivdagi faqat juft sonlarni tsikl sarlavhasidayoq filtrlang.

## Yechim (Swift kodi):
```swift
import Foundation

let numbers = [12, 17, 24, 33, 40, 55]

for n in numbers where n % 2 == 0 {
    print("Juft son: \(n)")
}
```

## Tushuntirish va Mantiq:
Swift for-in tsikliga 'where' shartini qo'shish imkonini beradi. Shart qanoatlantirilmagan elementlar uchun tsikl tanasi umuman kirmaydi.

## Ishlash natijasi:
```text
Juft son: 12
Juft son: 24
Juft son: 40
```


# 127-Topshiriq: Tsiklda indeks o'rniga '_' ishlatish
## Topshiriq sharti:
Amalni shunchaki 3 marta takrorlash uchun indeks o'zgaruvchisidan voz keching.

## Yechim (Swift kodi):
```swift
import Foundation

for _ in 1...3 {
    print("Khorazmiy AI - Yangi Avlod Dasturchilari!")
}
```

## Tushuntirish va Mantiq:
Agar tsikl hisoblagichining qiymati blok ichida kerak bo'lmasa, uni '_' bilan almashtirish xotira va kompilyator uchun optimallashuv beradi.

## Ishlash natijasi:
```text
Khorazmiy AI - Yangi Avlod Dasturchilari!
Khorazmiy AI - Yangi Avlod Dasturchilari!
Khorazmiy AI - Yangi Avlod Dasturchilari!
```


# 128-Topshiriq: while tsikli: Old shartli takrorlanish
## Topshiriq sharti:
Son 100 dan oshmaguncha uni 2 ga ko'paytirib boruvchi while tsikli yozing.

## Yechim (Swift kodi):
```swift
import Foundation

var value = 5

while value < 100 {
    print("Joriy: \(value)")
    value *= 2
}

print("Yakuniy: \(value)")
```

## Tushuntirish va Mantiq:
'while' tsikli har bir qadamdan oldin shartni tekshiradi. Agar shart dastlab false bo'lsa, tsikl tanasi biror marta ham bajarilmaydi.

## Ishlash natijasi:
```text
Joriy: 5
Joriy: 10
Joriy: 20
Joriy: 40
Joriy: 80
Yakuniy: 160
```


# 129-Topshiriq: repeat-while tsikli: So'nggi shartli takrorlanish
## Topshiriq sharti:
Shart oxirida tekshiriladigan va kamida 1 marta albatta ishlaydigan tsiklni ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

var counter = 10

repeat {
    print("repeat-while tanasi ishladi, counter = \(counter)")
    counter += 1
} while counter < 5

print("Tsikldan keyin.")
```

## Tushuntirish va Mantiq:
'repeat-while' boshqa tillardagi 'do-while' ga teng. Shart false bo'lsa ham uning tanasi kamida bir marta bajariladi.

## Ishlash natijasi:
```text
repeat-while tanasi ishladi, counter = 10
Tsikldan keyin.
```


# 130-Topshiriq: break operatori orqali tsikldan chiqish
## Topshiriq sharti:
Qidirilayotgan qiymat topilganda tsiklni darhol to'xtating.

## Yechim (Swift kodi):
```swift
import Foundation

let targets = ["Kitob", "Daftar", "Qalam", "O'chirg'ich"]

for item in targets {
    if item == "Qalam" {
        print("Topildi: \(item)! Qidiruv to'xtatildi.")
        break
    }
    print("Tekshirildi: \(item)")
}
```

## Tushuntirish va Mantiq:
'break' operatori o'zi joylashgan eng yaqin tsikl ijrosini shu zahotiyoq butunlay yakunlaydi.

## Ishlash natijasi:
```text
Tekshirildi: Kitob
Tekshirildi: Daftar
Topildi: Qalam! Qidiruv to'xtatildi.
```


# 131-Topshiriq: continue operatori
## Topshiriq sharti:
Toq sonlarni tashlab o'tib faqat musbatlarini qayta ishlang.

## Yechim (Swift kodi):
```swift
import Foundation

for i in 1...6 {
    if i % 2 != 0 {
        continue // Toq son bo'lsa keyingi iteratsiyaga o'tadi
    }
    print("Ishlandi: \(i)")
}
```

## Tushuntirish va Mantiq:
'continue' operatori joriy iteratsiyaning qolgan qismini o'tkazib yuborib, darhol tsiklning navbatdagi bosqichiga o'tadi.

## Ishlash natijasi:
```text
Ishlandi: 2
Ishlandi: 4
Ishlandi: 6
```


# 132-Topshiriq: Belgilangan tsikllar (Labeled Statements)
## Topshiriq sharti:
Ichma-ich tsikllarda tashqi tsiklni to'g'ridan-to'g'ri to'xtatuvchi yorliq (label) qo'llang.

## Yechim (Swift kodi):
```swift
import Foundation

outerLoop: for i in 1...3 {
    for j in 1...3 {
        if i == 2 && j == 2 {
            print("Ichki nuqtadan tashqi tsikl to'xtatildi! i=\(i), j=\(j)")
            break outerLoop
        }
        print("i=\(i), j=\(j)")
    }
}
```

## Tushuntirish va Mantiq:
Swift tsikllarga 'nom:' ko'rinishida yorliq berish imkonini beradi. 'break outerLoop' yoki 'continue outerLoop' orqali ichki chuqurlikdan to'g'ridan-to'g'ri tashqi tsiklni boshqarish mumkin.

## Ishlash natijasi:
```text
i=1, j=1
i=1, j=2
i=1, j=3
i=2, j=1
Ichki nuqtadan tashqi tsikl to'xtatildi! i=2, j=2
```


# 133-Topshiriq: Tsikl ichida 'guard' bilan saralash
## Topshiriq sharti:
Tsiklda noto'g'ri elementlarni 'guard' orqali erta chiqarib yuboring.

## Yechim (Swift kodi):
```swift
import Foundation

let emails: [String?] = ["ali@mail.uz", nil, "not-valid", "sami@gmail.com"]

for item in emails {
    guard let email = item, email.contains("@") else {
        continue
    }
    print("To'g'ri pochta: \(email)")
}
```

## Tushuntirish va Mantiq:
Tsikl ichida guard yordamida shart qanoatlantirilmaganda 'continue' qilish juda qulay va ixchamdir.

## Ishlash natijasi:
```text
To'g'ri pochta: ali@mail.uz
To'g'ri pochta: sami@gmail.com
```


# 134-Topshiriq: Enum qiymatlarini switch bilan to'liq tahlil qilish
## Topshiriq sharti:
Yo'nalish kompasini Enum va switch yordamida dasturlang.

## Yechim (Swift kodi):
```swift
import Foundation

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
```

## Tushuntirish va Mantiq:
Enum barcha holatlari switch-da yozilsa, 'default' bandi talab qilinmaydi va kelajakda yangi holat qo'shilsa kompilyator uni talab qilib xato ko'rsatadi.

## Ishlash natijasi:
```text
Shimol tomonga yo'naltirilgan.
```


# 135-Topshiriq: Swift 5.9 Switch Expression bilan qiymat qaytarish
## Topshiriq sharti:
Switch orqali holatga qarab to'g'ridan-to'g'ri o'zgaruvchiga matn qiymatini biriktiring.

## Yechim (Swift kodi):
```swift
import Foundation

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
```

## Tushuntirish va Mantiq:
Swift 5.9 da 'switch' ifoda sifatida ishlay oladi, har bir case bitta qiymatni avtomatik qaytaradi.

## Ishlash natijasi:
```text
Minimal kechikish (<5ms)
```


# 136-Topshiriq: Bitwise operatorlar: AND (&), OR (|), XOR (^)
## Topshiriq sharti:
Bayt darajasidagi bit operatsiyalarini bajaring.

## Yechim (Swift kodi):
```swift
import Foundation

let byteA: UInt8 = 0b1100_1010
let byteB: UInt8 = 0b1010_0101

let bitAnd = byteA & byteB
let bitOr = byteA | byteB
let bitXor = byteA ^ byteB

print("AND: 0b\(String(bitAnd, radix: 2))")
print("OR:  0b\(String(bitOr, radix: 2))")
print("XOR: 0b\(String(bitXor, radix: 2))")
```

## Tushuntirish va Mantiq:
Bit darajasidagi amallar past darajadagi dasturlash, kriptografiya va tarmoq protokollarida keng qo'llaniladi.

## Ishlash natijasi:
```text
AND: 0b10000000
OR:  0b11101111
XOR: 0b1101111
```


# 137-Topshiriq: Bitwise NOT (~) operatori
## Topshiriq sharti:
Barcha bitlarni teskarisiga o'giruvchi NOT operatorini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

let initialBits: UInt8 = 0b0000_1111
let invertedBits = ~initialBits

print("Asl bitlar:     0b00001111")
print("Inverted (NOT): 0b\(String(invertedBits, radix: 2))")
```

## Tushuntirish va Mantiq:
Bitwise NOT (~) barcha 0 larni 1 ga, 1 larni 0 ga aylantiradi.

## Ishlash natijasi:
```text
Asl bitlar:     0b00001111
Inverted (NOT): 0b11110000
```


# 138-Topshiriq: Bitwise Shift operatorlari (<<, >>)
## Topshiriq sharti:
Sonni 2 ga ko'paytirish va bo'lishning eng tezkor apparat usulini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

let baseValue: UInt8 = 4 // 0b0000_0100

let shiftedLeft = baseValue << 2   // 4 * 4 = 16
let shiftedRight = baseValue >> 1  // 4 / 2 = 2

print("Chapga 2 bit: \(shiftedLeft)")
print("O'ngga 1 bit: \(shiftedRight)")
```

## Tushuntirish va Mantiq:
Chapga siljitish (<<) sonni 2 ning darajalariga ko'paytiradi, o'ngga siljitish (>>) esa 2 ning darajalariga bo'ladi.

## Ishlash natijasi:
```text
Chapga 2 bit: 16
O'ngga 1 bit: 2
```


# 139-Topshiriq: Maxsus operator yaratish (Custom Operator)
## Topshiriq sharti:
Ikki sonning darajasini hisoblovchi '**' maxsus operatorini e'lon qiling.

## Yechim (Swift kodi):
```swift
import Foundation

infix operator **

func ** (base: Double, power: Double) -> Double {
    return pow(base, power)
}

let result = 2.0 ** 8.0
print("2 ning 8-darajasi: \(result)")
```

## Tushuntirish va Mantiq:
Swift dasturchiga o'zining shaxsiy operatorlarini (prefix, infix, postfix) e'lon qilish va ularning ustunligini belgilash imkonini beradi.

## Ishlash natijasi:
```text
2 ning 8-darajasi: 256.0
```


# 140-Topshiriq: Operator ustunligi va guruhlash (Precedence)
## Topshiriq sharti:
Arifmetik amallarning bajarilish ketma-ketligini ko'rsatuvchi dastur tuzing.

## Yechim (Swift kodi):
```swift
import Foundation

let rawCalc = 2 + 3 * 4
let groupedCalc = (2 + 3) * 4

print("rawCalc (ko'paytirish ustun): \(rawCalc)")
print("groupedCalc (qavs ustun): \(groupedCalc)")
```

## Tushuntirish va Mantiq:
Swift matematikadagi standart operatorlar ustunligiga qat'iy amal qiladi. Qavslar ustunlikni o'zgartiradi.

## Ishlash natijasi:
```text
rawCalc (ko'paytirish ustun): 14
groupedCalc (qavs ustun): 20
```


# 141-Topshiriq: Identiklik operatorlari: === va !==
## Topshiriq sharti:
Ikki havola aynan bitta xotira ob'ektiga ishora qilayotganini tekshiring.

## Yechim (Swift kodi):
```swift
import Foundation

class Session {
    let token = "TOKEN_ABC"
}

let s1 = Session()
let s2 = s1
let s3 = Session()

print("s1 === s2: \(s1 === s2)")
print("s1 === s3: \(s1 === s3)")
```

## Tushuntirish va Mantiq:
'===' operatori ikkita havola xotirada aynan bitta manzilga (instance) ishora qilayotganini tekshiradi (faqat class larda ishlaydi).

## Ishlash natijasi:
```text
s1 === s2: true
s1 === s3: false
```


# 142-Topshiriq: Pattern Matching operatori: ~= ning imkoniyatlari
## Topshiriq sharti:
Maxsus struct uchun ~= operatorini qayta yuklab (overload), switch-case da ishlatishni ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

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
```

## Tushuntirish va Mantiq:
'~=' operatorini qayta yuklash orqali ixtiyoriy turdagi ob'ektlarni switch-case da pattern matching bilan solishtirish mumkin.

## Ishlash natijasi:
```text
Bola toifasiga to'g'ri keladi.
```


# 143-Topshiriq: Tsikllarda teskari tartibda yurish: reversed()
## Topshiriq sharti:
Ortga hisoblashni 'reversed()' orqali bajaring.

## Yechim (Swift kodi):
```swift
import Foundation

for i in (1...5).reversed() {
    print("\(i)...", terminator: " ")
}
print("Start!")
```

## Tushuntirish va Mantiq:
'reversed()' to'plamni nusxalamasdan, uning ustida teskari ko'rinish (ReversedCollection) hosil qiladi.

## Ishlash natijasi:
```text
5... 4... 3... 2... 1... Start!
```


# 144-Topshiriq: Ikkita ketma-ketlikni juftlash: zip()
## Topshiriq sharti:
Talabalar va ularning baholarini bitta tsiklda zip yordamida birlashtiring.

## Yechim (Swift kodi):
```swift
import Foundation

let students = ["Ali", "Vali", "Sami"]
let marks = [95, 87, 92]

for (name, mark) in zip(students, marks) {
    print("\(name): \(mark) ball")
}
```

## Tushuntirish va Mantiq:
'zip(seq1, seq2)' ikkita ketma-ketlikdan juftliklar ketma-ketligini hosil qiladi. Ular uzunligi har xil bo'lsa, qisqaroqiga qarab to'xtaydi.

## Ishlash natijasi:
```text
Ali: 95 ball
Vali: 87 ball
Sami: 92 ball
```


# 145-Topshiriq: Cheksiz tsikllarni xavfsiz boshqarish
## Topshiriq sharti:
while true tsiklini xavfsiz to'xtatish mexanizmini yozing.

## Yechim (Swift kodi):
```swift
import Foundation

var attempts = 0

while true {
    attempts += 1
    if attempts >= 3 {
        print("Maksimal urinishlar soniga yetdi, chiqildi.")
        break
    }
}
```

## Tushuntirish va Mantiq:
'while true' tsikli cheksiz ishlaydi va uning ichida albatta 'break' yoki 'return' sharti bo'lishi shart.

## Ishlash natijasi:
```text
Maksimal urinishlar soniga yetdi, chiqildi.
```


# 146-Topshiriq: Murakkab shartlar va qavslarning roli
## Topshiriq sharti:
Chegirma berish uchun murakkab mantiqiy formulani tahlil qiling.

## Yechim (Swift kodi):
```swift
import Foundation

let isLoyal = true
let isWeekend = false
let cartAmount = 120.0

let getDiscount = (isLoyal || isWeekend) && cartAmount > 100.0
print("Chegirma beriladimi? \(getDiscount)")
```

## Tushuntirish va Mantiq:
Mantiqiy ifodalarda qavslar birinchi bo'lib hisoblanadi va kodning noaniq talqin qilinishini oldini oladi.

## Ishlash natijasi:
```text
Chegirma beriladimi? true
```


# 147-Topshiriq: @unknown default: Kelajakdagi enum holatlarini xavfsiz kutib olish
## Topshiriq sharti:
Kelajakda tizimga yangi enum qiymatlari qo'shilganda ogohlantirish beruvchi @unknown default ni ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

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
```

## Tushuntirish va Mantiq:
'@unknown default' switch to'liq bo'lsa-da, kelajakda yangi enum holatlari qo'shilsa kompilyator ogohlantirish (warning) berishi uchun qo'yiladi.

## Ishlash natijasi:
```text
Wi-Fi tarmog'i
```


# 148-Topshiriq: Tsikl ichida 'defer' operatorining ishlash tartibi
## Topshiriq sharti:
Har bir iteratsiya tugaganda bajariluvchi defer blokini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

for i in 1...3 {
    defer {
        print("Iteratsiya \(i) yakunlandi.")
    }
    print("Iteratsiya \(i) bajarilmoqda...")
}
```

## Tushuntirish va Mantiq:
'defer' bloki o'zi yozilgan skopdan (scope) chiqish oldidan doimo ijro etiladi.

## Ishlash natijasi:
```text
Iteratsiya 1 bajarilmoqda...
Iteratsiya 1 yakunlandi.
Iteratsiya 2 bajarilmoqda...
Iteratsiya 2 yakunlandi.
Iteratsiya 3 bajarilmoqda...
Iteratsiya 3 yakunlandi.
```


# 149-Topshiriq: Fibonachchi ketma-ketligini tsiklda hisoblash
## Topshiriq sharti:
Boshqaruv oqimlari orqali dastlabki 7 ta Fibonachchi sonlarini hisoblang.

## Yechim (Swift kodi):
```swift
import Foundation

var a = 0
var b = 1
var sequence = [a, b]

for _ in 2..<7 {
    let next = a + b
    sequence.append(next)
    a = b
    b = next
}

print("Fibonachchi ketma-ketligi: \(sequence)")
```

## Tushuntirish va Mantiq:
Tsikllar va arifmetik amallarning birgalikdagi klassik hisoblash algoritmi.

## Ishlash natijasi:
```text
Fibonachchi ketma-ketligi: [0, 1, 1, 2, 3, 5, 8]
```


# 150-Topshiriq: Amaliy loyiha: Boshqaruv oqimlari orqali ATM (Bankomat) simulyatori
## Topshiriq sharti:
Foydalanuvchi pin kodi, balansi, operatsiyalarini (yechish, to'ldirish) boshqaruvchi to'liq ATM moduli.

## Yechim (Swift kodi):
```swift
import Foundation

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
        print("Joriy balans: $\(currentBalance)")
    case .withdraw(let amount) where amount <= currentBalance:
        currentBalance -= amount
        print("Muvaffaqiyatli yechildi: $\(amount). Qoldiq: $\(currentBalance)")
    case .withdraw(let amount):
        print("Xatolik: Balansda yetarli mablag' yo'q! So'ralgan: $\(amount), Mavjud: $\(currentBalance)")
    case .deposit(let amount):
        currentBalance += amount
        print("Hisob to'ldirildi: $\(amount). Yangi balans: $\(currentBalance)")
    case .exit:
        print("Seans yakunlandi. Xayr!")
        break atmLoop
    }
}
```

## Tushuntirish va Mantiq:
Ushbu yakuniy loyihada 'switch-case', 'where' filtri, 'break labeledStatement', enum associated values va arifmetik amallar mukammal tizimda jamlandi.

## Ishlash natijasi:
```text
Joriy balans: $1000.0
Muvaffaqiyatli yechildi: $300.0. Qoldiq: $700.0
Xatolik: Balansda yetarli mablag' yo'q! So'ralgan: $900.0, Mavjud: $700.0
Hisob to'ldirildi: $150.0. Yangi balans: $850.0
Seans yakunlandi. Xayr!
```

