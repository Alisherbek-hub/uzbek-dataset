# 1-Topshiriq: O'zgarmas kattalik: 'let' kalit so'zi
## Topshiriq sharti:
iOS ilovasida foydalanuvchining o'zgarmas identifikatori (userId) va ilova versiyasini e'lon qiling hamda ularni konsolga chiqaring.

## Yechim (Swift kodi):
```swift
import Foundation

let userID: String = "USR_9921_AZ"
let appVersion: String = "2.4.0"

print("Foydalanuvchi ID: \(userID)")
print("Ilova versiyasi: \(appVersion)")
```

## Tushuntirish va Mantiq:
Swift tilida 'let' kalit so'zi o'zgarmas (constant) kattaliklarni e'lon qilish uchun xizmat qiladi. Bir marta qiymat berilgach, uni o'zgartirib bo'lmaydi. Swift xavfsiz va barqaror kod yozish uchun iloji boricha o'zgarmas 'let' dan foydalanishni tavsiya qiladi.

## Ishlash natijasi:
```text
Foydalanuvchi ID: USR_9921_AZ
Ilova versiyasi: 2.4.0
```


# 2-Topshiriq: O'zgaruvchan qiymat: 'var' kalit so'zi
## Topshiriq sharti:
Foydalanuvchining hisob balansini e'lon qiling, unga pul tushumi va xarid amallarini qo'llab, qiymatni yangilang.

## Yechim (Swift kodi):
```swift
import Foundation

var accountBalance: Double = 150.00
print("Boshlang'ich balans: $\(accountBalance)")

// Pul tushumi
accountBalance += 50.75
print("Tushumdan keyin: $\(accountBalance)")

// Xarid amalga oshirildi
accountBalance -= 32.50
print("Xariddan keyingi yakuniy balans: $\(accountBalance)")
```

## Tushuntirish va Mantiq:
Swift-da 'var' (variable) kalit so'zi o'zgaruvchan qiymatlarni yaratishda ishlatiladi. Uning qiymati dastur davomida bir necha bor yangilanishi mumkin, biroq uning turi dastlabki e'lon qilingan turda qat'iy saqlanadi.

## Ishlash natijasi:
```text
Boshlang'ich balans: $150.0
Tushumdan keyin: $200.75
Xariddan keyingi yakuniy balans: $168.25
```


# 3-Topshiriq: Tipni avtomatik aniqlash (Type Inference)
## Topshiriq sharti:
O'zgaruvchilarga turini aniq yozmasdan turli qiymatlar biriktiring va Swift kompilyatori qanday tip berganini tahlil qiling.

## Yechim (Swift kodi):
```swift
import Foundation

let platformName = "Apple iOS"
let releaseYear = 2024
let performanceScore = 98.75
let isProductionReady = true

print("Platforma: \(platformName), turi: \(type(of: platformName))")
print("Yil: \(releaseYear), turi: \(type(of: releaseYear))")
print("Ball: \(performanceScore), turi: \(type(of: performanceScore))")
print("Tayyor: \(isProductionReady), turi: \(type(of: isProductionReady))")
```

## Tushuntirish va Mantiq:
Swift kuchli 'Type Inference' (tiplarni avtomatik chiqarish) mexanizmiga ega. Kompilyator berilgan boshlang'ich qiymatga qarab turini o'zi belgilaydi. 'type(of:)' funksiyasi o'zgaruvchining dinamik turini aniqlash imkonini beradi.

## Ishlash natijasi:
```text
Platforma: Apple iOS, turi: String
Yil: 2024, turi: Int
Ball: 98.75, turi: Double
Tayyor: true, turi: Bool
```


# 4-Topshiriq: Aniq tip ko'rsatish (Explicit Type Annotation)
## Topshiriq sharti:
Xotira va arxitektura jihatidan aniqlik kiritish maqsadida o'zgaruvchilarga aniq tip ko'rsatib e'lon qiling.

## Yechim (Swift kodi):
```swift
import Foundation

let cityName: String = "Toshkent"
let population: Int = 3000000
let averageTemperature: Float = 24.5
let hasMetro: Bool = true

print("Shahar: \(cityName), Aholi: \(population), Harorat: \(averageTemperature)C, Metro: \(hasMetro)")
```

## Tushuntirish va Mantiq:
Aniq tip ko'rsatish (Type Annotation) o'zgaruvchi nomidan keyin ikki nuqta (:) va tip nomini yozish orqali amalga oshiriladi. Bu kod o'qiluvchanligini oshiradi va noaniqliklarning oldini oladi.

## Ishlash natijasi:
```text
Shahar: Toshkent, Aholi: 3000000, Harorat: 24.5C, Metro: true
```


# 5-Topshiriq: Butun son turlari va ularning chegaralari (Int, UInt)
## Topshiriq sharti:
Swift-dagi Int, UInt va ularning xotira o'lchamlari (8, 16, 32, 64-bit) hamda minimal/maksimal chegaralarini tekshiring.

## Yechim (Swift kodi):
```swift
import Foundation

let minInt8 = Int8.min
let maxInt8 = Int8.max
let maxUInt8 = UInt8.max
let maxInt64 = Int64.max

print("Int8 oralig'i: \(minInt8) dan \(maxInt8) gacha")
print("UInt8 maksimal qiymati: \(maxUInt8)")
print("Int64 maksimal qiymati: \(maxInt64)")
```

## Tushuntirish va Mantiq:
Swift butun sonlar uchun turli o'lchamdagi tiplarni taqdim etadi: Int8, Int16, Int32, Int64 hamda ularning manfiy bo'lmagan ko'rinishlari UInt8, UInt16 va h.k. Oddiy 'Int' joriy platforma arxitekturasiga mos ravishda 64-bitli tizimda Int64 o'lchamiga teng bo'ladi.

## Ishlash natijasi:
```text
Int8 oralig'i: -128 dan 127 gacha
UInt8 maksimal qiymati: 255
Int64 maksimal qiymati: 9223372036854775807
```


# 6-Topshiriq: Haqiqiy sonlar: Double va Float aniqligi
## Topshiriq sharti:
Double (64-bit) va Float (32-bit) turlarining o'nlik kasr qismidagi aniqlik farqini ko'rsatuvchi dastur yozing.

## Yechim (Swift kodi):
```swift
import Foundation

let piDouble: Double = 3.14159265358979323846
let piFloat: Float = 3.14159265358979323846

print("Double aniqligi: \(piDouble)")
print("Float aniqligi:  \(piFloat)")
```

## Tushuntirish va Mantiq:
Double 64-bitli suzuvchi nuqtali son bo'lib, kamida 15 ta o'nlik raqam aniqligini ta'minlaydi. Float esa 32-bitli bo'lib, atigi 6 ta raqam aniqligiga ega. Swift-da default suzuvchi son turi Double hisoblanadi.

## Ishlash natijasi:
```text
Double aniqligi: 3.141592653589793
Float aniqligi:  3.1415927
```


# 7-Topshiriq: Mantiqiy tur (Bool) va uning 'toggle()' metodi
## Topshiriq sharti:
Tizimda Wi-Fi ulanish holatini ifodalovchi Bool o'zgaruvchi oling va uni toggle() orqali teskarisiga o'zgartiring.

## Yechim (Swift kodi):
```swift
import Foundation

var isWifiConnected: Bool = false
print("Boshlang'ich holat: \(isWifiConnected)")

isWifiConnected.toggle()
print("toggle() qilingandan keyin: \(isWifiConnected)")

isWifiConnected.toggle()
print("Yana toggle() qilingandan keyin: \(isWifiConnected)")
```

## Tushuntirish va Mantiq:
Bool turi mantiqiy 'true' yoki 'false' qiymatlarini qabul qiladi. 'toggle()' metodi o'zgaruvchining qiymatini to'g'ridan-to'g'ri teskarisiga o'giradi (true bo'lsa false, false bo'lsa true).

## Ishlash natijasi:
```text
Boshlang'ich holat: false
toggle() qilingandan keyin: true
Yana toggle() qilingandan keyin: false
```


# 8-Topshiriq: Character va String asoslari
## Topshiriq sharti:
Alohida belgilar (Character) va belgilar ketma-ketligi (String) bilan ishlashni ko'rsatuvchi kod yozing.

## Yechim (Swift kodi):
```swift
import Foundation

let letter: Character = "A"
let heart: Character = "❤️"
let word: String = "Salom"

var greeting = word
greeting.append(" ")
greeting.append(letter)
greeting.append(" ")
greeting.append(heart)

print("Natija: \(greeting)")
```

## Tushuntirish va Mantiq:
Swift-da bitta belgi 'Character' turiga mansub bo'lib, u bitta kengaytirilgan grafema klasterini ifodalaydi (shu jumladan emojilar). 'String' esa belgilar to'plamidir. 'append' metodi orqali String-ga Character yoki boshqa String-ni qo'shish mumkin.

## Ishlash natijasi:
```text
Natija: Salom A ❤️
```


# 9-Topshiriq: String interpolyatsiyasi va ifodalarni kiritish
## Topshiriq sharti:
String interpolyatsiyasi ichida nafaqat o'zgaruvchilarni, balki arifmetik hisob-kitoblarni ham joylashtiring.

## Yechim (Swift kodi):
```swift
import Foundation

let itemName = "MacBook Pro"
let quantity = 3
let unitPrice = 1999.99

let invoice = "Mahsulot: \(itemName), Miqdor: \(quantity) ta, Jami summa: $\(Double(quantity) * unitPrice)"
print(invoice)
```

## Tushuntirish va Mantiq:
String interpolyatsiyasi \(...) sintaksisi orqali matn ichiga qiymatlar, o'zgaruvchilar va har qanday ifodani joylash imkonini beradi. Swift buni ish vaqtida avtomatik hisoblab matnga aylantiradi.

## Ishlash natijasi:
```text
Mahsulot: MacBook Pro, Miqdor: 3 ta, Jami summa: $5999.97
```


# 10-Topshiriq: Ko'p qatorli matnlar (Multiline String Literals)
## Topshiriq sharti:
Uchta qo'shtirnoq yordamida formatlangan shartnoma matnini konsolga chiqaring.

## Yechim (Swift kodi):
```swift
import Foundation

let termsOfService = """
FOYDALANISH SHARTLARI:
1. Maxfiylik qat'iy himoyalanadi.
2. Shaxsiy ma'lumotlar uchinchi shaxslarga berilmaydi.
3. Tizim 24/7 rejimida uzluksiz ishlaydi.
"""

print(termsOfService)
```

## Tushuntirish va Mantiq:
Swift-da ko'p qatorli matnlar uchta qo'shtirnoq (""") bilan boshlanadi va tugaydi. Har bir qatorning chekinishi oxirgi uchta qo'shtirnoq joylashuviga nisbatan hisoblanadi.

## Ishlash natijasi:
```text
FOYDALANISH SHARTLARI:
1. Maxfiylik qat'iy himoyalanadi.
2. Shaxsiy ma'lumotlar uchinchi shaxslarga berilmaydi.
3. Tizim 24/7 rejimida uzluksiz ishlaydi.
```


# 11-Topshiriq: Xom matnlar (Raw Strings) va maxsus belgilar
## Topshiriq sharti:
Matn ichida teskari slesh (\) va qo'shtirnoqlarni escape qilmasdan to'g'ridan-to'g'ri ifodalash uchun Raw String dan foydalaning.

## Yechim (Swift kodi):
```swift
import Foundation

let regexPattern = #"\d{3}-\d{2}-\d{4}"#
let quoteInside = #"Stiv Jobs dedi: "Stay hungry, stay foolish.""#

print("Regex shabloni: \(regexPattern)")
print("Iqtibos: \(quoteInside)")
```

## Tushuntirish va Mantiq:
Swift 5-dan boshlab joriy qilingan Raw Strings (#"..."#) ichida teskari sleshlar oddiy belgi sifatida talqin qilinadi. Agar interpolyatsiya kerak bo'lsa, \#(...) shaklida yoziladi.

## Ishlash natijasi:
```text
Regex shabloni: \d{3}-\d{2}-\d{4}
Iqtibos: Stiv Jobs dedi: "Stay hungry, stay foolish."
```


# 12-Topshiriq: Sonli literallar: O'qiluvchanlik uchun pastki chiziq va sanoq tizimlari
## Topshiriq sharti:
Milliarder balansini o'qiluvchan son formatida va turli sanoq tizimlarida (ikkilik, o'n oltilik) ifodalang.

## Yechim (Swift kodi):
```swift
import Foundation

let billionDollars = 1_000_000_000
let binaryMask = 0b1010_0110
let hexColor = 0xFF_57_33

print("Milliarder balansi: \(billionDollars)")
print("Ikkilik niqob: \(binaryMask)")
print("Hex rang kodi: \(hexColor)")
```

## Tushuntirish va Mantiq:
Swift sonli literallarda raqamlar orasida pastki chiziq (_) ishlatishga ruxsat beradi, bu katta sonlarni o'qishni juda osonlashtiradi. Shuningdek 0b (ikkilik), 0o (sakkizlik) va 0x (o'n oltilik) prefikslari qo'llab-quvvatlanadi.

## Ishlash natijasi:
```text
Milliarder balansi: 1000000000
Ikkilik niqob: 166
Hex rang kodi: 16734003
```


# 13-Topshiriq: Sonli tiplarni bir-biriga aylantirish (Type Conversion)
## Topshiriq sharti:
Int va Double turlaridagi sonlarni o'zaro hisob-kitob qilish uchun to'g'ri tip konversiyasini qo'llang.

## Yechim (Swift kodi):
```swift
import Foundation

let integerCount: Int = 25
let factorRate: Double = 1.84

// Xato: integerCount * factorRate (Swift-da implicit type conversion yo'q)
let total = Double(integerCount) * factorRate
let roundedTotal = Int(total)

print("Aniq natija (Double): \(total)")
print("Yaxlitlangan (Int): \(roundedTotal)")
```

## Tushuntirish va Mantiq:
Swift xavfsizlik maqsadida har xil tiplar o'rtasida avtomatik (implicit) o'tkazishni taqiqlaydi. Amal bajarish uchun kerakli tur konstruktorini (masalan, Double(x)) chaqirish shart.

## Ishlash natijasi:
```text
Aniq natija (Double): 46.0
Yaxlitlangan (Int): 46
```


# 14-Topshiriq: Tip taxallusi: 'typealias' kalit so'zi
## Topshiriq sharti:
Murakkab yoki ma'noli tiplarni tushunarli qilish uchun typealias e'lon qiling.

## Yechim (Swift kodi):
```swift
import Foundation

typealias AudioSample = UInt16
typealias CustomerID = String

let sampleValue: AudioSample = 44100
let activeCustomer: CustomerID = "CUST-8832"

print("Audio chastotasi: \(sampleValue) Hz")
print("Mijoz ID: \(activeCustomer)")
```

## Tushuntirish va Mantiq:
'typealias' mavjud bo'lgan tipga yangi, ma'noli nom berish imkonini beradi. Bu kod arxitekturasini tushunarli qiladi va domen modellarini yaratishda juda qo'l keladi.

## Ishlash natijasi:
```text
Audio chastotasi: 44100 Hz
Mijoz ID: CUST-8832
```


# 15-Topshiriq: Kortejlar (Tuples) asoslari va dekonstruksiya
## Topshiriq sharti:
Server javob holatini (status kodi va xabari) tuple yordamida guruhlang va uni alohida o'zgaruvchilarga ajrating.

## Yechim (Swift kodi):
```swift
import Foundation

let httpResponse = (404, "Not Found")

// Indeks orqali murojaat
print("Kod: \(httpResponse.0), Xabar: \(httpResponse.1)")

// Dekonstruksiya (ajratib olish)
let (statusCode, statusMessage) = httpResponse
print("Ajratilgan: Status=\(statusCode), Izoh=\(statusMessage)")
```

## Tushuntirish va Mantiq:
Tuple bir nechta qiymatni bitta birikmaga birlashtiradi. Elementlarga nol asosidagi indekslar (.0, .1) orqali murojaat qilish yoki dekonstruksiya qilish mumkin.

## Ishlash natijasi:
```text
Kod: 404, Xabar: Not Found
Ajratilgan: Status=404, Izoh=Not Found
```


# 16-Topshiriq: Nomlangan kortejlar (Named Tuples)
## Topshiriq sharti:
Geografik koordinatalarni nomlangan kortej shaklida ifodalang va nomlari orqali chaqiring.

## Yechim (Swift kodi):
```swift
import Foundation

let tashkentCoords = (latitude: 41.2995, longitude: 69.2401, city: "Toshkent")

print("Shahar: \(tashkentCoords.city)")
print("Kenglik: \(tashkentCoords.latitude)")
print("Uzunlik: \(tashkentCoords.longitude)")
```

## Tushuntirish va Mantiq:
Tuple elementlariga nom berish orqali indeks o'rniga aniq nomlar bilan murojaat qilish mumkin bo'ladi. Bu kod tushunarliligini sezilarli oshiradi.

## Ishlash natijasi:
```text
Shahar: Toshkent
Kenglik: 41.2995
Uzunlik: 69.2401
```


# 17-Topshiriq: Funksiyadan ko'p qiymat qaytarishda Tuple qo'llash
## Topshiriq sharti:
Berilgan massivdagi eng kichik va eng katta sonni bitta funksiyada aniqlab qaytaring.

## Yechim (Swift kodi):
```swift
import Foundation

func getMinMax(numbers: [Int]) -> (min: Int, max: Int) {
    var currentMin = numbers[0]
    var currentMax = numbers[0]
    
    for num in numbers {
        if num < currentMin { currentMin = num }
        if num > currentMax { currentMax = num }
    }
    
    return (min: currentMin, max: currentMax)
}

let result = getMinMax(numbers: [14, 2, 88, 35, -5, 99, 12])
print("Minimal: \(result.min), Maksimal: \(result.max)")
```

## Tushuntirish va Mantiq:
Swift-da alohida struct yoki class yaratmasdan, tezkor ravishda bir nechta qiymatni qaytarish uchun Tuple ajoyib vositadir.

## Ishlash natijasi:
```text
Minimal: -5, Maksimal: 99
```


# 18-Topshiriq: String uzunligi va belgilar sanog'i (count)
## Topshiriq sharti:
Foydalanuvchi kiritgan parolni uzunligini va belgilar sonini tekshiring.

## Yechim (Swift kodi):
```swift
import Foundation

let userPassword = "SecretPass2026!"
let length = userPassword.count

print("Parol belgilar soni: \(length)")
if length >= 8 {
    print("Parol uzunligi xavfsizlik talablariga javob beradi.")
} else {
    print("Parol kamida 8 ta belgidan iborat bo'lishi kerak.")
}
```

## Tushuntirish va Mantiq:
Swift-da String.count xususiyati belgilar (Character) sonini to'g'ri hisoblaydi, chunki u Unicode Extended Grapheme Clusters tamoyiliga tayanadi.

## Ishlash natijasi:
```text
Parol belgilar soni: 15
Parol uzunligi xavfsizlik talablariga javob beradi.
```


# 19-Topshiriq: String bo'shligini tekshirish: isEmpty
## Topshiriq sharti:
Matn bo'sh yoki bo'sh emasligini to'g'ri tekshirish usulini yozing.

## Yechim (Swift kodi):
```swift
import Foundation

let enteredBio = ""

if enteredBio.isEmpty {
    print("Foydalanuvchi o'zi haqida ma'lumot kiritmadi.")
} else {
    print("Kiritilgan bio: \(enteredBio)")
}

let filledBio = "iOS dasturchisi"
print("Yangi holat bo'shmi? \(filledBio.isEmpty)")
```

## Tushuntirish va Mantiq:
Swift-da 'str.count == 0' deb tekshirish tavsiya etilmaydi, chunki count butun satrni sanab chiqadi. 'isEmpty' esa satr boshidagi ko'rsatkichni tekshirib O(1) vaqt ichida juda tez javob beradi.

## Ishlash natijasi:
```text
Foydalanuvchi o'zi haqida ma'lumot kiritmadi.
Yangi holat bo'shmi? false
```


# 20-Topshiriq: Stringlarni birlashtirish: '+' va 'append'
## Topshiriq sharti:
Satrlarni qo'shishning turli usullarini ko'rsatuvchi dastur yozing.

## Yechim (Swift kodi):
```swift
import Foundation

var greeting = "Xush"
greeting += " kelibsiz"

let target = ", do'stim!"
let fullMessage = greeting + target
print("Full: \(fullMessage)")

var mutableMsg = "Yuklanmoqda"
mutableMsg.append("...")
print("Append natijasi: \(mutableMsg)")
```

## Tushuntirish va Mantiq:
Swift-da satrlarni '+' operatori bilan birlashtirish yangi satr nusxasini yaratadi, 'append' metodi esa o'zgaruvchi satrning o'ziga to'g'ridan-to'g'ri yangi belgilarni qo'shadi.

## Ishlash natijasi:
```text
Full: Xush kelibsiz, do'stim!
Append natijasi: Yuklanmoqda...
```


# 21-Topshiriq: Matn registrini o'zgartirish: uppercased va lowercased
## Topshiriq sharti:
Qidiruv tizimida foydalanuvchi so'rovini bir xil registrga keltiruvchi mexanizm tuzing.

## Yechim (Swift kodi):
```swift
import Foundation

let query = "Swift 5.9 va SwiftUI"

let upper = query.uppercased()
let lower = query.lowercased()

print("Katta harflarda: \(upper)")
print("Kichik harflarda: \(lower)")
```

## Tushuntirish va Mantiq:
'uppercased()' barcha harflarni bosh harfga, 'lowercased()' esa kichik harfga o'tkazadi. Bu registrga sezgir bo'lmagan (case-insensitive) qidiruvlarda asosiy rol o'ynaydi.

## Ishlash natijasi:
```text
Katta harflarda: SWIFT 5.9 VA SWIFTUI
Kichik harflarda: swift 5.9 va swiftui
```


# 22-Topshiriq: Matn prefiks, suffiks va ichki qismini tekshirish
## Topshiriq sharti:
Fayl nomi va URL manzilini tekshiruvchi validator yozing.

## Yechim (Swift kodi):
```swift
import Foundation

let urlString = "https://khorazmiy.uz/api/v1/users"
let filename = "dataset_final.json"

let isSecure = urlString.hasPrefix("https://")
let isAPI = urlString.contains("/api/")
let isJSON = filename.hasSuffix(".json")

print("Xavfsiz ulanish: \(isSecure)")
print("API so'rovi: \(isAPI)")
print("JSON fayl: \(isJSON)")
```

## Tushuntirish va Mantiq:
'hasPrefix' boshlanishini, 'hasSuffix' tugashini, 'contains' esa satr ichida qidirilayotgan matn borligini mantiqiy qiymat sifatida qaytaradi.

## Ishlash natijasi:
```text
Xavfsiz ulanish: true
API so'rovi: true
JSON fayl: true
```


# 23-Topshiriq: Matn qismini almashtirish: replacingOccurrences
## Topshiriq sharti:
Matndagi eskirgan kalit so'zlarni yangisiga almashtiruvchi dastur yozing.

## Yechim (Swift kodi):
```swift
import Foundation

let legacyText = "Dastur Objective-C tilida yozilgan. Objective-C tezkor til."
let modernText = legacyText.replacingOccurrences(of: "Objective-C", with: "Swift")

print("Eski: \(legacyText)")
print("Yangi: \(modernText)")
```

## Tushuntirish va Mantiq:
'replacingOccurrences(of:with:)' metodi berilgan andozadagi barcha qismlarni yangi matn bilan almashtirib yangi satr qaytaradi.

## Ishlash natijasi:
```text
Eski: Dastur Objective-C tilida yozilgan. Objective-C tezkor til.
Yangi: Dastur Swift tilida yozilgan. Swift tezkor til.
```


# 24-Topshiriq: Matnni bo'laklarga ajratish: split va components
## Topshiriq sharti:
Vergul bilan ajratilgan texnologiyalar ro'yxatini massivga ajrating.

## Yechim (Swift kodi):
```swift
import Foundation

let tags = "iOS,macOS,watchOS,visionOS,tvOS"

let splitResult = tags.split(separator: ",")
print("split() natijasi turi: \(type(of: splitResult))")
for tag in splitResult {
    print("- \(tag)")
}

let componentsResult = tags.components(separatedBy: ",")
print("components() natijasi soni: \(componentsResult.count)")
```

## Tushuntirish va Mantiq:
'split(separator:)' metodi Substring lar ketma-ketligini qaytaradi (xotirani tejaydi), 'components(separatedBy:)' esa Foundation kutubxonasiga tegishli bo'lib, to'g'ridan-to'g'ri [String] massivini beradi.

## Ishlash natijasi:
```text
split() natijasi turi: Array<Substring>
- iOS
- macOS
- watchOS
- visionOS
- tvOS
components() natijasi soni: 5
```


# 25-Topshiriq: print funksiyasi parametrlari: separator va terminator
## Topshiriq sharti:
Bir nechta qiymatni maxsus ajratuvchi va qator yakuni bilan konsolga chiqaring.

## Yechim (Swift kodi):
```swift
import Foundation

print("Toshkent", "Samarqand", "Buxoro", "Xiva", separator: " -> ")
print("Yuklanmoqda: 0%", terminator: "")
print("... 50%", terminator: "")
print("... 100% [Tayyor!]")
```

## Tushuntirish va Mantiq:
Swift-da 'print()' funksiyasining 'separator' parametri elementlar orasidagi belgini, 'terminator' esa qator oxiriga nima qo'shilishini (standart holda '\n') belgilaydi.

## Ishlash natijasi:
```text
Toshkent -> Samarqand -> Buxoro -> Xiva
Yuklanmoqda: 0%... 50%... 100% [Tayyor!]
```


# 26-Topshiriq: Hujjatlashtirish izohlari (Documentation Comments)
## Topshiriq sharti:
Xcode va kompilyator uchun rasmiy formatdagi uch karra slesh (///) hujjat izohlarini yozing.

## Yechim (Swift kodi):
```swift
import Foundation

/// Foydalanuvchining oylik maoshiga soliq stavkasini hisoblaydi.
///
/// Ushbu funksiya davlat daromad solig'i stavkasi bo'yicha toza summani aniqlaydi.
/// - Parameters:
///   - grossSalary: Soliqlar ushlab qolinishidan oldingi jami maosh.
///   - taxRate: Foiz ko'rinishidagi soliq stavkasi (masalan, 0.12).
/// - Returns: Soliq ushlab qolingandan keyingi sof daromad.
func calculateNetSalary(grossSalary: Double, taxRate: Double) -> Double {
    return grossSalary * (1.0 - taxRate)
}

let net = calculateNetSalary(grossSalary: 5000.0, taxRate: 0.12)
print("Sof maosh: $\(net)")
```

## Tushuntirish va Mantiq:
Swift-da '///' belgisi bilan yozilgan izohlar Markdown sintaksisini qo'llab-quvvatlaydi. Xcode Quick Help panelida funksiya parametrlari va qaytaruvchi qiymati chiroyli hujjat ko'rinishida namoyon bo'ladi.

## Ishlash natijasi:
```text
Sof maosh: $4400.0
```


# 27-Topshiriq: Nosozliklarni aniqlash: assert va assertionFailure
## Topshiriq sharti:
Debug rejimida parametrning musbat ekanligini tasdiqlovchi assert tekshiruvini yozing.

## Yechim (Swift kodi):
```swift
import Foundation

func processOrder(count: Int) {
    assert(count > 0, "Buyurtmalar soni noldan katta bo'lishi shart!")
    print("Buyurtma qabul qilindi: \(count) dona.")
}

processOrder(count: 5)
// processOrder(count: -1) // Bu Debug muhitda dasturni to'xtatadi
```

## Tushuntirish va Mantiq:
'assert()' funksiyasi faqat Debug rejimida ishlaydi va ishlab chiqish jarayonida kutilmagan xatoliklarni erta aniqlashga xizmat qiladi. Release kompilyatsiyasida u butunlay e'tiborsiz qoldiriladi va tezlikka ta'sir qilmaydi.

## Ishlash natijasi:
```text
Buyurtma qabul qilindi: 5 dona.
```


# 28-Topshiriq: Doimiy shart tekshiruvi: precondition
## Topshiriq sharti:
Ilova doimo, hatto Release rejimida ham qanoatlantirishi shart bo'lgan invariantni tekshiring.

## Yechim (Swift kodi):
```swift
import Foundation

func divideRewards(total: Int, players: Int) -> Int {
    precondition(players > 0, "O'yinchilar soni kamida 1 ta bo'lishi shart!")
    return total / players
}

let rewardPerPerson = divideRewards(total: 1000, players: 4)
print("Har bir o'yinchiga: \(rewardPerPerson) tanga")
```

## Tushuntirish va Mantiq:
'precondition()' funksiyasi ham Debug, ham Release (agar -Ounchecked bo'lmasa) rejimlarida shartni tekshiradi. Shart bajarilmasa dastur xavfsiz tarzda darhol to'xtatiladi.

## Ishlash natijasi:
```text
Har bir o'yinchiga: 250 tanga
```


# 29-Topshiriq: Qaytarib bo'lmas to'xtatish: fatalError
## Topshiriq sharti:
Hali yozilmagan yoki dasturning mantiqan borishi mumkin bo'lmagan joyini fatalError bilan belgilang.

## Yechim (Swift kodi):
```swift
import Foundation

enum NetworkMode {
    case online
    case offline
    case mock
}

func configureNetwork(mode: NetworkMode) -> String {
    switch mode {
    case .online:
        return "Real serverga ulandi."
    case .offline:
        return "Kesh ma'lumotlari ishlatilmoqda."
    case .mock:
        return "Test ma'lumotlari faollashtirildi."
    }
}

let status = configureNetwork(mode: .online)
print(status)
```

## Tushuntirish va Mantiq:
'fatalError()' dastur ijrosini majburan to'xtatadi va xatolik matnini konsolga chiqaradi. U 'Never' turini qaytaradi, shu sababli kompilyator keyingi qatorlarni tekshirishni talab qilmaydi.

## Ishlash natijasi:
```text
Real serverga ulandi.
```


# 30-Topshiriq: Minimal va maksimal qiymatlar hamda cheksizlik
## Topshiriq sharti:
Swift-da sonlarning chegaraviy qiymatlari va cheksizlik (infinity) bilan ishlashni ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

let infDouble = Double.infinity
let negInfDouble = -Double.infinity
let notANumber = Double.nan

print("Musbat cheksizlik: \(infDouble)")
print("Manfiy cheksizlik: \(negInfDouble)")
print("NaN mi? \(notANumber.isNaN)")
print("Cheksizmi? \((100.0 / 0.0).isInfinite)")
```

## Tushuntirish va Mantiq:
Suzuvchi sonlar IEEE 754 standartiga ko'ra noldan farqli sonni nolga bo'lganda infinity (cheksizlik), 0/0 holatida esa NaN (Not a Number) qiymatini qabul qiladi.

## Ishlash natijasi:
```text
Musbat cheksizlik: inf
Manfiy cheksizlik: -inf
NaN mi? true
Cheksizmi? true
```


# 31-Topshiriq: Toshish operatorlari (Overflow Operators: &+, &-)
## Topshiriq sharti:
Chegaradan oshganda xatolik bermasdan, aylanma hisoblash imkonini beruvchi toshish operatorlarini sinab ko'ring.

## Yechim (Swift kodi):
```swift
import Foundation

var maxByte: UInt8 = 255
// maxByte += 1 // Oddiy qo'shish Run-time crash beradi!

maxByte = maxByte &+ 1
print("UInt8 255 &+ 1 natijasi: \(maxByte)")

var minByte: UInt8 = 0
minByte = minByte &- 1
print("UInt8 0 &- 1 natijasi: \(minByte)")
```

## Tushuntirish va Mantiq:
Swift standart arifmetikada chegaradan toshishni xato deb biladi. Ammo '&+', '&-', '&*' kabi maxsus 'overflow' operatorlari toshganda qiymatni aylanma ravishda qayta boshidan hisoblashga imkon beradi.

## Ishlash natijasi:
```text
UInt8 255 &+ 1 natijasi: 0
UInt8 0 &- 1 natijasi: 255
```


# 32-Topshiriq: Kechiktirilgan initsializatsiya (Deferred Initialization)
## Topshiriq sharti:
O'zgarmas 'let' qiymatini e'lon qilish paytida emas, shartli tekshiruvdan so'ng bir marta biriktiring.

## Yechim (Swift kodi):
```swift
import Foundation

let environment = "production"
let apiEndpoint: String

if environment == "production" {
    apiEndpoint = "https://api.khorazmiy.uz/v1"
} else {
    apiEndpoint = "https://staging.khorazmiy.uz/v1"
}

print("Tanlangan endpoint: \(apiEndpoint)")
```

## Tushuntirish va Mantiq:
Swift-da 'let' o'zgarmasini qiymat bermasdan e'lon qilish mumkin. Kompilyator unga kodning barcha tarmoqlarida faqat va faqat BIR marta qiymat berilishini qat'iy tekshiradi (Definite Initialization).

## Ishlash natijasi:
```text
Tanlangan endpoint: https://api.khorazmiy.uz/v1
```


# 33-Topshiriq: Tipni tekshirish: 'is' operatori
## Topshiriq sharti:
Koleksiyadagi elementlarning aniq qaysi tipga tegishli ekanligini 'is' operatori bilan tekshiring.

## Yechim (Swift kodi):
```swift
import Foundation

let mixedList: [Any] = ["Swift", 2024, true, 3.14]

for item in mixedList {
    if item is String {
        print("'\(item)' - bu String turi")
    } else if item is Int {
        print("'\(item)' - bu Int turi")
    } else if item is Bool {
        print("'\(item)' - bu Bool turi")
    } else {
        print("'\(item)' - boshqa tur")
    }
}
```

## Tushuntirish va Mantiq:
'is' operatori berilgan obyekt yoki o'zgaruvchining ko'rsatilgan tipga mos kelishini tekshiradi va mantiqiy true yoki false qaytaradi.

## Ishlash natijasi:
```text
'Swift' - bu String turi
'2024' - bu Int turi
'true' - bu Bool turi
'3.14' - boshqa tur
```


# 34-Topshiriq: Tipni quyish: 'as?' va 'as!' operatorlari
## Topshiriq sharti:
Any turidagi ma'lumotni xavfsiz (conditional) va xavfli (forced) usulda mos turga quying.

## Yechim (Swift kodi):
```swift
import Foundation

let mysteryData: Any = "Salom, Khorazmiy AI!"

// Xavfsiz quyish (as?)
if let safeString = mysteryData as? String {
    print("Muvaffaqiyatli quyildi: \(safeString.uppercased())")
}

// O'xshamaydigan turga xavfsiz quyish
let safeNumber = mysteryData as? Int
print("Son sifatida quyish natijasi: \(String(describing: safeNumber))")
```

## Tushuntirish va Mantiq:
'as?' operatori tipni xavfsiz quyishga urinadi va muvaffaqiyatsiz bo'lsa nil qaytaradi. 'as!' esa majburan quyadi va agar tip to'g'ri kelmasa dastur ishini to'xtatadi (crash).

## Ishlash natijasi:
```text
Muvaffaqiyatli quyildi: SALOM, KHORAZMIY AI!
Son sifatida quyish natijasi: nil
```


# 35-Topshiriq: Universal turlar: Any va AnyObject
## Topshiriq sharti:
Any (har qanday tip) va AnyObject (faqat class nusxalari) o'rtasidagi farqni kod orqali ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class Device {
    let model: String
    init(model: String) { self.model = model }
}

let anyItems: [Any] = [42, "Matn", Device(model: "iPhone 16 Pro")]
let classItems: [AnyObject] = [Device(model: "iPad Pro"), Device(model: "Mac Studio")]

print("Any kolleksiyasi elementlari soni: \(anyItems.count)")
print("AnyObject faqat sinf obyektlarini saqlaydi: \(classItems.count)")
```

## Tushuntirish va Mantiq:
'Any' Swift-dagi mutlaqo barcha turlarni (struct, enum, funksiya, class) saqlashi mumkin. 'AnyObject' esa faqat havola turlari (Reference types, ya'ni class instansiyalari) bilan cheklanadi.

## Ishlash natijasi:
```text
Any kolleksiyasi elementlari soni: 3
AnyObject faqat sinf obyektlarini saqlaydi: 2
```


# 36-Topshiriq: String sub-indekslash va String.Index
## Topshiriq sharti:
Swift-da matn belgilariga butun sonli indeks (masalan, str[0]) orqali emas, String.Index orqali murojaat qilishni ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

let technology = "SwiftUI"

let firstChar = technology[technology.startIndex]
let secondCharIndex = technology.index(after: technology.startIndex)
let secondChar = technology[secondCharIndex]

let lastCharIndex = technology.index(before: technology.endIndex)
let lastChar = technology[lastCharIndex]

print("Birinchi belgi: \(firstChar)")
print("Ikkinchi belgi: \(secondChar)")
print("Oxirgi belgi: \(lastChar)")
```

## Tushuntirish va Mantiq:
Swift-da belgilar har xil bayt hajmdagi Unicode klasterlaridan tashkil topganligi sababli, ixtiyoriy belgigacha borish uchun satrni skanerlash talab etiladi. Shu bois butun sonli indeks o'rniga String.Index ishlatiladi.

## Ishlash natijasi:
```text
Birinchi belgi: S
Ikkinchi belgi: w
Oxirgi belgi: I
```


# 37-Topshiriq: Substring va String o'rtasidagi xotira munosabati
## Topshiriq sharti:
Matndan kesib olingan qism (Substring) qanday qilib ota matn xotirasini bo'lishishini va uni mustaqil String ga aylantirishni ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

let fullArticle = "Swift dasturlash tili juda tezkor va zamonaviy."
let spaceIndex = fullArticle.firstIndex(of: " ") ?? fullArticle.endIndex

let firstWordSubstring: Substring = fullArticle[..<spaceIndex]
print("Substring: \(firstWordSubstring)")

// Mustaqil String ga o'tkazish
let standaloneString: String = String(firstWordSubstring)
print("Mustaqil String: \(standaloneString)")
```

## Tushuntirish va Mantiq:
Substring ota satrning xotira buferiga ishora qiladi va ortiqcha xotira nusxalashni oldini oladi. Biroq uzoq vaqt xotirada saqlash uchun uni 'String(sub)' orqali yangi mustaqil xotiraga o'tkazish tavsiya qilinadi.

## Ishlash natijasi:
```text
Substring: Swift
Mustaqil String: Swift
```


# 38-Topshiriq: Unicode Skalyarlar va Emojilar bilan ishlash
## Topshiriq sharti:
Bayroq yoki birikmali emojilarning bir nechta Unicode skalyarlaridan tashkil topganini tahlil qiling.

## Yechim (Swift kodi):
```swift
import Foundation

let flag = "🇺🇿"
print("Belgilar soni (Character count): \(flag.count)")
print("Unicode Skalyarlar soni: \(flag.unicodeScalars.count)")

for scalar in flag.unicodeScalars {
    print("Skalyar: \(scalar), Qiymati: 0x\(String(scalar.value, radix: 16, uppercase: true))")
}
```

## Tushuntirish va Mantiq:
O'zbekiston bayrog'i (🇺🇿) bitta vizual belgidan iborat, lekin uning tagida ikkita hududiy ko'rsatkich belgisi (U+1F1FA va U+1F1FF) birlashtirilgan.

## Ishlash natijasi:
```text
Belgilar soni (Character count): 1
Unicode Skalyarlar soni: 2
Skalyar: 🇺, Qiymati: 0x1F1FA
Skalyar: 🇿, Qiymati: 0x1F1FF
```


# 39-Topshiriq: String formatlash (String(format: ...))
## Topshiriq sharti:
Pul miqdorini va o'nlik kasrlarni aniq formatda ekranga chiqarish dasturini yozing.

## Yechim (Swift kodi):
```swift
import Foundation

let productPrice = 124.5
let discount = 0.155

let formattedPrice = String(format: "Narx: $%.2f", productPrice)
let formattedDiscount = String(format: "Chegirma: %.1f%%", discount * 100)

print(formattedPrice)
print(formattedDiscount)
```

## Tushuntirish va Mantiq:
Foundation-ning 'String(format:)' funksiyasi C uslubidagi formatlash specifierlaridan (masalan, %.2f) foydalanib sonlarni aniq formatlash imkonini beradi.

## Ishlash natijasi:
```text
Narx: $124.50
Chegirma: 15.5%
```


# 40-Topshiriq: Kortejni qisman qabul qilish (Wildcard '_')
## Topshiriq sharti:
Tuple-dan faqat kerakli ma'lumotni olib, keraksiz qismini e'tiborsiz qoldirishni ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

let sensorPacket = (sensorID: "TEMP_01", temperature: 28.4, batteryLevel: 92)

// sensorID va battery kerak emas, faqat haroratni olamiz:
let (_, currentTemp, _) = sensorPacket

print("Joriy harorat: \(currentTemp)°C")
```

## Tushuntirish va Mantiq:
Swift-da pastki chiziq (_) wildcard belgisi hisoblanadi. U 'bu qiymatni e'tiborsiz qoldir va unga xotira ajratma' degan ma'noni bildiradi.

## Ishlash natijasi:
```text
Joriy harorat: 28.4°C
```


# 41-Topshiriq: Murakkab tiplarni 'typealias' bilan ixchamlashtirish
## Topshiriq sharti:
Koordinata va xatolik matnidan iborat murakkab kortejga yangi tip nomi bering.

## Yechim (Swift kodi):
```swift
import Foundation

typealias GPSPoint = (latitude: Double, longitude: Double)
typealias LocationResult = (point: GPSPoint?, error: String?)

let successResult: LocationResult = ((latitude: 41.3111, longitude: 69.2797), nil)

if let loc = successResult.point {
    print("Koordinata: \(loc.latitude), \(loc.longitude)")
}
```

## Tushuntirish va Mantiq:
typealias chuqur joylashgan murakkab kortejlar va ma'lumot tuzilmalarini o'qishni sezilarli darajada soddalashtiradi.

## Ishlash natijasi:
```text
Koordinata: 41.3111, 69.2797
```


# 42-Topshiriq: Qiymatlarni o'zaro almashtirish: swapAt va swap
## Topshiriq sharti:
Ikkita o'zgaruvchi qiymatini uchinchi vaqtinchalik o'zgaruvchisiz almashtiring.

## Yechim (Swift kodi):
```swift
import Foundation

var a = 10
var b = 99

print("Oldin: a = \(a), b = \(b)")
swap(&a, &b)
print("Keyin: a = \(a), b = \(b)")
```

## Tushuntirish va Mantiq:
Swift standart kutubxonasidagi 'swap(&a, &b)' funksiyasi xotiradagi ko'rsatkichlar darajasida ikkita o'zgaruvchining qiymatini xavfsiz almashtiradi.

## Ishlash natijasi:
```text
Oldin: a = 10, b = 99
Keyin: a = 99, b = 10
```


# 43-Topshiriq: Qiymat turlari (Value types) nusxalanish semantikasi
## Topshiriq sharti:
Oddiy tiplar (Int, String) boshqa o'zgaruvchiga berilganda yangi mustaqil nusxa yaratilishini isbotlang.

## Yechim (Swift kodi):
```swift
import Foundation

var originalScore = 100
var copiedScore = originalScore

copiedScore += 50

print("Asl ball: \(originalScore)")
print("Nusxa ball: \(copiedScore)")
```

## Tushuntirish va Mantiq:
Swift-da asosiy tiplar (Int, Double, String, massivlar) barchasi 'Value types' bo'lib, o'zgaruvchiga berilganda qiymat to'liq nusxalanadi, asl qiymatga ta'sir qilmaydi.

## Ishlash natijasi:
```text
Asl ball: 100
Nusxa ball: 150
```


# 44-Topshiriq: O'zgarmas va o'zgaruvchan massivlar
## Topshiriq sharti:
'let' va 'var' yordamida massiv yaratishdagi farqni tushuntiring.

## Yechim (Swift kodi):
```swift
import Foundation

let immutableList = ["Olma", "Nok"]
// immutableList.append("Anor") // Xato! 'let' bilan e'lon qilingan kolleksiya o'zgarmasdir.

var mutableList = ["Olma", "Nok"]
mutableList.append("Anor")
print("O'zgaruvchan ro'yxat: \(mutableList)")
```

## Tushuntirish va Mantiq:
Swift-da to'plamning (massiv, lug'at) o'zgaruvchanligi uning qaysi kalit so'z bilan e'lon qilinganiga bog'liq: 'let' bo'lsa butun to'plam mutatsiyaga yopiq bo'ladi.

## Ishlash natijasi:
```text
O'zgaruvchan ro'yxat: ["Olma", "Nok", "Anor"]
```


# 45-Topshiriq: Ob'ektning ichki strukturasini tahlil qilish: dump()
## Topshiriq sharti:
O'zgaruvchining to'liq daraxtsimon tuzilishini konsolga chiqaruvchi 'dump()' funksiyasini qo'llang.

## Yechim (Swift kodi):
```swift
import Foundation

let complexData = (
    user: "Ali",
    stats: (level: 42, score: 9800),
    badges: ["Yulduz", "Lider"]
)

dump(complexData)
```

## Tushuntirish va Mantiq:
'dump()' funksiyasi ob'ektning ierarxiyasini, uning xususiyatlari va ichki qismlarini aks ettirib chiqaradi. Bu nosozliklarni izlashda (debugging) print() ga qaraganda ancha ko'proq ma'lumot beradi.

## Ishlash natijasi:
```text
▿ (3 elements)
  - user: "Ali"
  ▿ stats: (2 elements)
    - level: 42
    - score: 9800
  ▿ badges: 2 elements
    - "Yulduz"
    - "Lider"
```


# 46-Topshiriq: Konsol argumentlarini qabul qilish: CommandLine.arguments
## Topshiriq sharti:
Buyruqlar satridan berilgan argumentlarni o'qib chiquvchi dastur yozing.

## Yechim (Swift kodi):
```swift
import Foundation

let arguments = CommandLine.arguments

print("Argumentlar soni: \(arguments.count)")
print("Dasturning o'zi: \(arguments[0])")

if arguments.count > 1 {
    print("Kiritilgan birinchi argument: \(arguments[1])")
} else {
    print("Qo'shimcha argumentlar kiritilmadi.")
}
```

## Tushuntirish va Mantiq:
Swift CLI dasturlarida 'CommandLine.arguments' orqali buyruqlar satridan uzatilgan parametrlarni [String] massivi ko'rinishida o'qish mumkin.

## Ishlash natijasi:
```text
Argumentlar soni: 1
Dasturning o'zi: main
Qo'shimcha argumentlar kiritilmadi.
```


# 47-Topshiriq: Global va lokal o'zgaruvchilar ko'rinish sohasi (Scope)
## Topshiriq sharti:
O'zgaruvchining blok ichidagi va tashqarisidagi ta'sir doirasini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

let globalScopeVar = "Men globalman"

do {
    let localScopeVar = "Men faqat shu blok ichidaman"
    print("Ichki: \(globalScopeVar)")
    print("Ichki: \(localScopeVar)")
}

print("Tashqi: \(globalScopeVar)")
// print(localScopeVar) // Kompilyatsiya xatosi: localScopeVar bu yerda mavjud emas!
```

## Tushuntirish va Mantiq:
Har qanday jingalak qavs ({ }) yangi ko'rinish sohasini (scope) hosil qiladi. Lokal o'zgaruvchilar o'sha blok tugashi bilan xotiradan tozalanadi.

## Ishlash natijasi:
```text
Ichki: Men globalman
Ichki: Men faqat shu blok ichidaman
Tashqi: Men globalman
```


# 48-Topshiriq: Statik va Dinamik tiplash tushunchasi Swift kontekstida
## Topshiriq sharti:
Swift statik tiplangan til ekanligini, ammo Any orqali dinamik xatti-harakat qila olishini namoyish eting.

## Yechim (Swift kodi):
```swift
import Foundation

var strictlyTyped: Int = 100
// strictlyTyped = "Yuz" // Kompilyatsiya xatosi!

var dynamicContainer: Any = 100
print("Boshida: \(dynamicContainer) (Turi: \(type(of: dynamicContainer)))")

dynamicContainer = "Endi matnga aylandi"
print("Keyin: \(dynamicContainer) (Turi: \(type(of: dynamicContainer)))")
```

## Tushuntirish va Mantiq:
Swift qat'iy statik tildir: o'zgaruvchi turlari kompilyatsiya vaqtida to'liq aniqlanadi. 'Any' qutisi (type erasure) orqali dinamik xususiyat hosil qilinsa ham, xavfsizlik ta'minlanadi.

## Ishlash natijasi:
```text
Boshida: 100 (Turi: Int)
Keyin: Endi matnga aylandi (Turi: String)
```


# 49-Topshiriq: Swift 5.9 Typed Throws va kelajakdagi xavfsizlikka tayyorgarlik
## Topshiriq sharti:
Aniq tiplangan natijalar qaytaruvchi mustahkam arxitekturaviy tiplar yaratish.

## Yechim (Swift kodi):
```swift
import Foundation

enum AppEnvironment: String {
    case development = "DEV"
    case staging = "STAGE"
    case production = "PROD"
}

let currentEnv = AppEnvironment.production
print("Muhit nomi: \(currentEnv.rawValue)")
```

## Tushuntirish va Mantiq:
Swift tiplari kuchli xavfsizlik va aniqlik taqdim etadi. Enum orqali string xatoliklarni tiplash eng yaxshi amaliyot hisoblanadi.

## Ishlash natijasi:
```text
Muhit nomi: PROD
```


# 50-Topshiriq: Amaliy loyiha: Mijoz anketasini qayta ishlovchi profil tizimi
## Topshiriq sharti:
Foydalanuvchining shaxsiy ma'lumotlarini qabul qiluvchi, formatlovchi va hisobot tayyorlovchi yaxlit dastur tuzing.

## Yechim (Swift kodi):
```swift
import Foundation

typealias UserID = UInt32

let id: UserID = 104857
let firstName = "Akmal"
let lastName = "Rahimov"
var age: Int = 27
var isSubscribed: Bool = true
let monthlySpending: Double = 345.80

let fullName = "\(firstName) \(lastName)"
let statusTag = isSubscribed ? "PREMIUM_MIJOZ" : "ODDIY_MIJOZ"

let userReport = """
=========================================
FOYDALANUVCHI PROFIL HISOBOTI
=========================================
ID:           #\(id)
F.I.SH:       \(fullName.uppercased())
Yosh:         \(age)
Maqomi:       \(statusTag)
Oylik xarid:  \(String(format: "$%.2f", monthlySpending))
Tizim holati: Aktiv
=========================================
"""

print(userReport)
```

## Tushuntirish va Mantiq:
Ushbu amaliy topshiriqda Swift asoslarining barcha muhim jihatlari: 'let', 'var', 'typealias', String interpolyatsiyasi, ternary operator va ko'p qatorli matn formatlash bitta real loyihada birlashtirildi.

## Ishlash natijasi:
```text
=========================================
FOYDALANUVCHI PROFIL HISOBOTI
=========================================
ID:           #104857
F.I.SH:       AKMAL RAHIMOV
Yosh:         27
Maqomi:       PREMIUM_MIJOZ
Oylik xarid:  $345.80
Tizim holati: Aktiv
=========================================
```

