# 651-Topshiriq: Extensions asoslari: Mavjud turni kengaytirish
## Topshiriq sharti:
Swift-dagi standart Double turiga masofalarni metrga o'giruvchi hisoblangan xususiyatlar qo'shing.

## Yechim (Swift kodi):
```swift
import Foundation

extension Double {
    var km: Double { self * 1000.0 }
    var m: Double { self }
    var cm: Double { self / 100.0 }
}

let marathon = 42.195.km
let height = 185.0.cm

print("Marafon: \(marathon) metr")
print("Bo'y: \(height) metr")
```

## Tushuntirish va Mantiq:
Kengaytma (Extension) — bu manba kodi sizda bo'lmagan mavjud sinf, struktura, enum yoki protokolga yangi metodlar, hisoblangan xususiyatlar va initsializatorlar qo'shish mexanizmidir.

## Ishlash natijasi:
```text
Marafon: 42195.0 metr
Bo'y: 1.85 metr
```


# 652-Topshiriq: Nima uchun Extensions da saqlanuvchi maydonlar (stored properties) mumkin emas
## Topshiriq sharti:
Kengaytmada yangi 'var x: Int = 0' yozib bo'lmasligining xotira sababini tushuntiring.

## Yechim (Swift kodi):
```swift
import Foundation

class BaseAppConfig {
    var version = "1.0"
}

extension BaseAppConfig {
    // var newField: Int = 10 // KOMPILYATSIYA XATOSI: Extensions must not contain stored properties
    
    // Faqat hisoblangan xususiyat ruxsat etiladi:
    var fullVersionDescription: String {
        return "Ilova versiyasi: v\(version)"
    }
}

let cfg = BaseAppConfig()
print(cfg.fullVersionDescription)
```

## Tushuntirish va Mantiq:
Chunki ob'ektning Heap yoki Stack-dagi xotira hajmi va tekislanishi asosiy e'londa belgilanadi. Kengaytmalarda yangi saqlanuvchi maydon qo'shish mavjud xotira strukturasini buzib yuborgan bo'lardi.

## Ishlash natijasi:
```text
Ilova versiyasi: v1.0
```


# 653-Topshiriq: mutating metodlar qo'shish struct va enum larda
## Topshiriq sharti:
Int turiga o'z qiymatini kvadratga oshiruvchi 'mutating' metod qo'shing.

## Yechim (Swift kodi):
```swift
import Foundation

extension Int {
    mutating func square() {
        self = self * self
    }
}

var number = 5
number.square()
print("Kvadrat: \(number)")
```

## Tushuntirish va Mantiq:
Qiymat turlarini kengaytirganda o'zgaruvchi qiymatini mutatsiyaga uchratuvchi metodlar boshiga 'mutating' qo'yiladi.

## Ishlash natijasi:
```text
Kvadrat: 25
```


# 654-Topshiriq: Initsializatorlar qo'shish: Initializers in Extensions
## Topshiriq sharti:
Struct-ga maxsus initsializator qo'shib, avtomatik memberwise initsializatorni saqlab qoling.

## Yechim (Swift kodi):
```swift
import Foundation

struct CoordinatePoint {
    var x: Double
    var y: Double
}

extension CoordinatePoint {
    init(originWithOffset offset: Double) {
        self.init(x: offset, y: offset)
    }
}

let p1 = CoordinatePoint(x: 10, y: 20) // Memberwise init saqlanib qolgan!
let p2 = CoordinatePoint(originWithOffset: 5.0)

print("p1: (\(p1.x), \(p1.y)), p2: (\(p2.x), \(p2.y))")
```

## Tushuntirish va Mantiq:
Agar maxsus initsializator extension ichida yozilsa, Swift struct-ning avtomatik memberwise konstruktorini o'chirib yubormaydi.

## Ishlash natijasi:
```text
p1: (10.0, 20.0), p2: (5.0, 5.0)
```


# 655-Topshiriq: Subscript lar qo'shish
## Topshiriq sharti:
String turiga butun sonli indeks orqali belgi qaytaruvchi qulay subscript qo'shing.

## Yechim (Swift kodi):
```swift
import Foundation

extension String {
    subscript(offset: Int) -> Character? {
        guard offset >= 0 && offset < count else { return nil }
        let idx = index(startIndex, offsetBy: offset)
        return self[idx]
    }
}

let word = "Khorazmiy"
print("0-belgi: \(word[0] ?? " ")")
print("4-belgi: \(word[4] ?? " ")")
```

## Tushuntirish va Mantiq:
Extension orqali kiritilgan subscriptlar mavjud tiplardan foydalanishni ancha qulay qiladi.

## Ishlash natijasi:
```text
0-belgi: K
4-belgi: a
```


# 656-Topshiriq: Ichki turlar qo'shish (Nested Types in Extensions)
## Topshiriq sharti:
Int turiga sonning ishorasini bildiruvchi yangi ichki Enum qo'shing.

## Yechim (Swift kodi):
```swift
import Foundation

extension Int {
    enum Sign {
        case negative, zero, positive
    }
    
    var sign: Sign {
        if self < 0 { return .negative }
        if self == 0 { return .zero }
        return .positive
    }
}

let testNum = -42
print("-42 ishorasi: \(testNum.sign)")
```

## Tushuntirish va Mantiq:
Extension ichida yangi enum, struct yoki sinflarni e'lon qilib, ularni tegishli tip nomlari fazosida birlashtirish mumkin.

## Ishlash natijasi:
```text
-42 ishorasi: negative
```


# 657-Topshiriq: Protokolga moslikni Extension orqali qabul qilish
## Topshiriq sharti:
Sinf kodini modulli qilish uchun protokolni alohida extensionda qabul qiling.

## Yechim (Swift kodi):
```swift
import Foundation

class UserAccount {
    let username: String
    init(username: String) { self.username = username }
}

extension UserAccount: CustomStringConvertible {
    var description: String {
        return "Foydalanuvchi: @\(username)"
    }
}

let user = UserAccount(username: "nodir_dev")
print(user)
```

## Tushuntirish va Mantiq:
iOS dasturlashda Clean Code qoidasi: har bir protokol alohida extensionda qabul qilinadi, bu asosiy sinf kodini yengil saqlaydi.

## Ishlash natijasi:
```text
Foydalanuvchi: @nodir_dev
```


# 658-Topshiriq: Standart turga amaliy metod: Int.times
## Topshiriq sharti:
Ruby dasturlash tilidagi kabi amalni N marta bajaruvchi closure metodini Int ga qo'shing.

## Yechim (Swift kodi):
```swift
import Foundation

extension Int {
    func times(_ action: () -> Void) {
        guard self > 0 else { return }
        for _ in 1...self {
            action()
        }
    }
}

3.times {
    print("Swift ajoyib!")
}
```

## Tushuntirish va Mantiq:
Standart sonli tiplarga funktsional yordamchi metodlar qo'shish ilova kodini juda o'qiluvchan qiladi.

## Ishlash natijasi:
```text
Swift ajoyib!
Swift ajoyib!
Swift ajoyib!
```


# 659-Topshiriq: Shartli kengaytmalar: extension Array where Element == String
## Topshiriq sharti:
Faqat satrlar massiviga tegishli bo'lgan yangi metod qo'shing.

## Yechim (Swift kodi):
```swift
import Foundation

extension Array where Element == String {
    func joinWithComma() -> String {
        return self.joined(separator: ", ")
    }
}

let tech = ["Swift", "SwiftUI", "CoreML"]
print("Texnologiyalar: \(tech.joinWithComma())")

let numbers = [1, 2, 3]
// numbers.joinWithComma() // KOMPILYATSIYA XATOSI: Int uchun bu metod mavjud emas!
```

## Tushuntirish va Mantiq:
'where Element == Tip' sharti metodni faqat mos keluvchi aniq to'plamlar uchungina faollashtiradi.

## Ishlash natijasi:
```text
Texnologiyalar: Swift, SwiftUI, CoreML
```


# 660-Topshiriq: Protokol kengaytmalari (Protocol Extensions): Default Implementation
## Topshiriq sharti:
Barcha mos tiplar uchun umumiy standart metod tana qismini taqdim eting.

## Yechim (Swift kodi):
```swift
import Foundation

protocol Loggable {
    var identifier: String { get }
}

extension Loggable {
    func printLog() {
        print("[LOG]: Ob'ekt ID=\(identifier)")
    }
}

struct DeviceModel: Loggable {
    let identifier: String
}

let dev = DeviceModel(identifier: "DEV_991")
dev.printLog()
```

## Tushuntirish va Mantiq:
Protocol Extension barcha qabul qiluvchi tiplarga avtomatik ravishda tayyor metod logikasini beradi.

## Ishlash natijasi:
```text
[LOG]: Ob'ekt ID=DEV_991
```


# 661-Topshiriq: Static vs Dynamic Dispatch protokol extensionlarida
## Topshiriq sharti:
Protokol deklaratsiyasida bor va yo'q metodlar qanday chaqirilishini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

protocol Animal {
    func sound() // Deklaratsiyada BOR -> Dynamic Dispatch
}

extension Animal {
    func sound() { print("Umumiy ovoz") }
    func sleep() { print("Uxlamoqda...") } // Deklaratsiyada YO'Q -> Static Dispatch!
}

struct Dog: Animal {
    func sound() { print("Vov-vov!") }
    func sleep() { print("It uxlamoqda...") }
}

let d = Dog()
d.sound()

let a: any Animal = Dog()
a.sound() // Vov-vov (Dynamic)
a.sleep() // Uxlamoqda... (Static dispatch protokol extensionidagi asl metodga tushadi!)
```

## Tushuntirish va Mantiq:
Agar metod protokol tanasida e'lon qilingan bo'lsa, u VTable orqali dinamik chaqiriladi. Agar faqat extensionda bo'lsa, Static Dispatch tufayli ko'rsatkich turiga qarab chaqiriladi.

## Ishlash natijasi:
```text
Vov-vov!
Vov-vov!
Uxlamoqda...
```


# 662-Topshiriq: Optional turini kengaytirish: isNilOrEmpty
## Topshiriq sharti:
Optional String uchun eng mashhur va qulay tekshiruv xususiyatini yozing.

## Yechim (Swift kodi):
```swift
import Foundation

extension Optional where Wrapped == String {
    var isNilOrEmpty: Bool {
        switch self {
        case .none:
            return true
        case .some(let str):
            return str.trimmingCharacters(in: .whitespaces).isEmpty
        }
    }
}

let s1: String? = nil
let s2: String? = "   "
let s3: String? = "Swift"

print("s1: \(s1.isNilOrEmpty)")
print("s2: \(s2.isNilOrEmpty)")
print("s3: \(s3.isNilOrEmpty)")
```

## Tushuntirish va Mantiq:
'extension Optional where Wrapped == String' orqali ixtiyoriy matnlar bo'shligini bir satrda xavfsiz tekshirish mumkin.

## Ishlash natijasi:
```text
s1: true
s2: true
s3: false
```


# 663-Topshiriq: Sequence ga yig'indi metodini qo'shish: sum()
## Topshiriq sharti:
Barcha raqamli to'plamlar uchun umumiy 'sum()' metodini yozing.

## Yechim (Swift kodi):
```swift
import Foundation

extension Sequence where Element: AdditiveArithmetic {
    func sum() -> Element {
        return reduce(.zero, +)
    }
}

let numbers = [10, 20, 30, 40]
print("Jami yig'indi: \(numbers.sum())")

let doubles = [1.5, 2.5, 3.0]
print("Haqiqiy sonlar yig'indisi: \(doubles.sum())")
```

## Tushuntirish va Mantiq:
'AdditiveArithmetic' protokoli '.zero' va '+' operatorini taqdim etadi, bu barcha sonli ketma-ketliklarga sum() berish imkonini yaratadi.

## Ishlash natijasi:
```text
Jami yig'indi: 100
Haqiqiy sonlar yig'indisi: 7.0
```


# 664-Topshiriq: Same-file private a'zolarga extension dan kirish ruxsatnomasi
## Topshiriq sharti:
Swift 4+ qoidasiga ko'ra bir xil fayldagi private a'zolar extensionga ochiq ekanligini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class SecretUser {
    private var token = "TOP_SECRET_123"
}

extension SecretUser {
    func printTokenForDebug() {
        // Bir xil fayl ichida bo'lgani sababli private xususiyatga kira oladi:
        print("Xavfsiz token: \(token)")
    }
}

let u = SecretUser()
u.printTokenForDebug()
```

## Tushuntirish va Mantiq:
Swift 4 dan boshlab, asosiy deklaratsiya bilan bitta faylda joylashgan extensionlar o'sha sinfning barcha 'private' maydonlariga to'liq kira oladi.

## Ishlash natijasi:
```text
Xavfsiz token: TOP_SECRET_123
```


# 665-Topshiriq: String uchun Base64 kodlash va dekodlash extensioni
## Topshiriq sharti:
Matnni Base64 formatiga o'tkazuvchi va qayta tiklovchi yordamchi.

## Yechim (Swift kodi):
```swift
import Foundation

extension String {
    func toBase64() -> String {
        return Data(self.utf8).base64EncodedString()
    }
    
    func fromBase64() -> String? {
        guard let data = Data(base64Encoded: self) else { return nil }
        return String(data: data, encoding: .utf8)
    }
}

let plain = "Khorazmiy AI"
let encoded = plain.toBase64()
let decoded = encoded.fromBase64()

print("Kodlangan: \(encoded)")
print("Qayta tiklangan: \(decoded ?? "")")
```

## Tushuntirish va Mantiq:
Extensionlar orqali ma'lumotlarni kodlash va o'zgartirish funksiyalarini String ichiga toza joylashtirish mumkin.

## Ishlash natijasi:
```text
Kodlangan: S2hvcmF6bXlpIEFJ
Qayta tiklangan: Khorazmiy AI
```


# 666-Topshiriq: Task ga soniyalarda kutish extensionini qo'shish
## Topshiriq sharti:
Nanosekundlar o'rniga qulay soniya kiritish imkonini beruvchi Task kengaytmasi.

## Yechim (Swift kodi):
```swift
import Foundation

extension Task where Success == Never, Failure == Never {
    static func sleep(seconds: Double) async throws {
        let nanoseconds = UInt64(seconds * 1_000_000_000)
        try await Task.sleep(nanoseconds: nanoseconds)
    }
}

print("Task.sleep(seconds:) qulay asinxron yordamchisi yaratildi.")
```

## Tushuntirish va Mantiq:
Swift Concurrency turlariga extension orqali qulay yordamchi metodlar qo'shish eng yaxshi amaliyotdir.

## Ishlash natijasi:
```text
Task.sleep(seconds:) qulay asinxron yordamchisi yaratildi.
```


# 667-Topshiriq: Date turini formatlovchi extension
## Topshiriq sharti:
Date ob'ektini qulay satr ko'rinishida formatlab beruvchi xususiyat.

## Yechim (Swift kodi):
```swift
import Foundation

extension Date {
    func toString(format: String = "yyyy-MM-dd") -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = format
        return formatter.string(from: self)
    }
}

let today = Date()
print("Sana formati: \(today.toString())")
```

## Tushuntirish va Mantiq:
Foundation-ning Date turiga dateFormat parametrli kengaytma qo'shish ilovaning barcha qismlarida sana formatlashni markazlashtiradi.

## Ishlash natijasi:
```text
Sana formati: 2026-11-08
```


# 668-Topshiriq: Kolleksiyaga xavfsiz subscript extensioni
## Topshiriq sharti:
Indeks chegaradan chiqib ketganda halokatga uchramasdan nil beruvchi xavfsiz massiv kengaytmasi.

## Yechim (Swift kodi):
```swift
import Foundation

extension Collection {
    subscript(safe index: Index) -> Element? {
        return indices.contains(index) ? self[index] : nil
    }
}

let arr = [10, 20, 30]
print("Indeks 1: \(arr[safe: 1] ?? -1)")
print("Indeks 99: \(arr[safe: 99] ?? -1)")
```

## Tushuntirish va Mantiq:
Collection protokoliga [safe: index] subscriptini qo'shish nafaqat Array, balki barcha Swift to'plamlari uchun avtomatik ishlaydi.

## Ishlash natijasi:
```text
Indeks 1: 20
Indeks 99: -1
```


# 669-Topshiriq: Extension orqali Factory uslubidagi ranglar
## Topshiriq sharti:
Ilova dizayn ranglarini static hisoblangan xususiyatlar bilan kengaytirish.

## Yechim (Swift kodi):
```swift
import Foundation

struct BrandColor {
    let hex: String
}

extension BrandColor {
    static let primaryBlue = BrandColor(hex: "#0055FF")
    static let accentOrange = BrandColor(hex: "#FF8800")
}

let current = BrandColor.primaryBlue
print("Tanlangan brend rangi: \(current.hex)")
```

## Tushuntirish va Mantiq:
SwiftUI-dagi Color.primary, Color.accent aynan extension ichidagi static xususiyatlar asosida tashkil etilgan.

## Ishlash natijasi:
```text
Tanlangan brend rangi: #0055FF
```


# 670-Topshiriq: Extension da metodlarni override qilish mumkin emasligi
## Topshiriq sharti:
Sinf metodlarini extension ichida override qilish nima sababdan cheklanganini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class Vehicle {
    func drive() { print("Oddiy harakat") }
}

class FastVehicle: Vehicle {}

// extension FastVehicle {
//     override func drive() {} // XATO: Overriding declarations in extensions is not supported
// }

print("Sinf metodlarini override qilish faqat asosiy sinf tanasida bo'lishi shart.")
```

## Tushuntirish va Mantiq:
Swift arxitekturasida extensionlar VTable jadvalini qayta tuzishga qatnashmaydi, shu sababli metodlarni override qilish faqat asosiy sinf tanasida amalga oshiriladi.

## Ishlash natijasi:
```text
Sinf metodlarini override qilish faqat asosiy sinf tanasida bo'lishi shart.
```


# 671-Topshiriq: Sonlarni Rim raqamlariga aylantiruvchi Int extensioni
## Topshiriq sharti:
Int sonini Rim raqamlari matniga o'giruvchi qiziqarli algoritmik kengaytma.

## Yechim (Swift kodi):
```swift
import Foundation

extension Int {
    func toRoman() -> String {
        let mapping: [(int: Int, roman: String)] = [
            (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
        ]
        var num = self
        var result = ""
        for pair in mapping {
            while num >= pair.int {
                result += pair.roman
                num -= pair.int
            }
        }
        return result
    }
}

print("9 Rim raqamida: \(9.toRoman())")
print("14 Rim raqamida: \(14.toRoman())")
```

## Tushuntirish va Mantiq:
Algoritmik hisob-kitoblarni mos tur extensioniga joylashtirish kod ergonomikasini sezilarli oshiradi.

## Ishlash natijasi:
```text
9 Rim raqamida: IX
14 Rim raqamida: XIV
```


# 672-Topshiriq: Shartli Equatable mosligi: extension Pair: Equatable
## Topshiriq sharti:
Faqat ichki elementlari Equatable bo'lgandagina generik turga Equatable qo'shish.

## Yechim (Swift kodi):
```swift
import Foundation

struct Pair<T> {
    let first: T
    let second: T
}

extension Pair: Equatable where T: Equatable {}

let p1 = Pair(first: 1, second: 2)
let p2 = Pair(first: 1, second: 2)
print("p1 == p2: \(p1 == p2)")
```

## Tushuntirish va Mantiq:
Conditional Conformance orqali generik strukturalar faqat kerakli shart qanoatlantirilgandagina protokolga moslashadi.

## Ishlash natijasi:
```text
p1 == p2: true
```


# 673-Topshiriq: Dictionary ga yangi xususiyat: hasKey(_:)
## Topshiriq sharti:
Lug'atda kalit mavjudligini xavfsiz tekshiruvchi sodda metod.

## Yechim (Swift kodi):
```swift
import Foundation

extension Dictionary {
    func hasKey(_ key: Key) -> Bool {
        return self[key] != nil
    }
}

let capitals = ["UZ": "Toshkent", "FR": "Parij"]
print("UZ bormi? \(capitals.hasKey("UZ"))")
print("US bormi? \(capitals.hasKey("US"))")
```

## Tushuntirish va Mantiq:
Lug'atlarga qulay yordamchi metodlar qo'shish shartli tekshiruvlarni qisqartiradi.

## Ishlash natijasi:
```text
UZ bormi? true
US bormi? false
```


# 674-Topshiriq: String dan raqamlarni ajratuvchi digitsOnly xususiyati
## Topshiriq sharti:
Matndagi faqat sonlarni qaytaruvchi hisoblangan xususiyat.

## Yechim (Swift kodi):
```swift
import Foundation

extension String {
    var digitsOnly: String {
        return self.filter { $0.isNumber }
    }
}

let rawPhone = "+998 (90) 555-12-34"
print("Faqat raqamlar: \(rawPhone.digitsOnly)")
```

## Tushuntirish va Mantiq:
Matnlarni tozalash (sanitization) kengaytmalari biznes ilovalarida ajralmas hisoblanadi.

## Ishlash natijasi:
```text
Faqat raqamlar: 998905551234
```


# 675-Topshiriq: Protokol kengaytmasi zanjiri (Chained Extensions)
## Topshiriq sharti:
Bitta protokolga ketma-ket bir nechta extension orqali imkoniyatlar qo'shish.

## Yechim (Swift kodi):
```swift
import Foundation

protocol IdentifiableEntity { var id: String { get } }

extension IdentifiableEntity {
    func printID() { print("ID: \(id)") }
}

extension IdentifiableEntity {
    var hasValidID: Bool { !id.isEmpty }
}

struct RecordItem: IdentifiableEntity { let id: String }
let item = RecordItem(id: "REC_01")
print("Validmi? \(item.hasValidID)")
```

## Tushuntirish va Mantiq:
Extensionlar protokol imkoniyatlarini bir nechta mustaqil fayllarda bosqichma-bosqich kengaytirish imkonini beradi.

## Ishlash natijasi:
```text
Validmi? true
```


# 676-Topshiriq: Extension orqali DTO ni Domain Model ga aylantirish
## Topshiriq sharti:
Xom server strukturasidan biznes modelini hosil qiluvchi initsializator.

## Yechim (Swift kodi):
```swift
import Foundation

struct UserDTO { let first_name: String; let last_name: String }
struct UserModel { let fullName: String }

extension UserModel {
    init(dto: UserDTO) {
        self.fullName = "\(dto.first_name) \(dto.last_name)"
    }
}

let dto = UserDTO(first_name: "Aziz", last_name: "Valiyev")
let model = UserModel(dto: dto)
print("Model to'liq ismi: \(model.fullName)")
```

## Tushuntirish va Mantiq:
Modellar orasidagi konversiya initsializatorlarini extension ichida saqlash qatlamlar sofligini (Clean Architecture) saqlaydi.

## Ishlash natijasi:
```text
Model to'liq ismi: Aziz Valiyev
```


# 677-Topshiriq: URL ga xavfsiz parametr qo'shish extensioni
## Topshiriq sharti:
URL manziliga yangi query parametrini qo'shib yangi URL qaytaruvchi metod.

## Yechim (Swift kodi):
```swift
import Foundation

extension URL {
    func appendingQuery(name: String, value: String) -> URL {
        guard var components = URLComponents(url: self, resolvingAgainstBaseURL: true) else {
            return self
        }
        var items = components.queryItems ?? []
        items.append(URLQueryItem(name: name, value: value))
        components.queryItems = items
        return components.url ?? self
    }
}

let base = URL(string: "https://api.khorazmiy.uz/v1")!
let withQuery = base.appendingQuery(name: "lang", value: "uz")
print("URL: \(withQuery.absoluteString)")
```

## Tushuntirish va Mantiq:
Foundation URLComponents bilan ishlovchi extension xavfsiz URL yaratishni ta'minlaydi.

## Ishlash natijasi:
```text
URL: https://api.khorazmiy.uz/v1?lang=uz
```


# 678-Topshiriq: Clean Code: Qachon Extension ishlatish kerak
## Topshiriq sharti:
Extensionlardan to'g'ri foydalanish qoidalarini namoyish etish.

## Yechim (Swift kodi):
```swift
import Foundation

class OrderManager {
    var ordersCount = 0
}

// 1. Protokol uchun alohida extension:
extension OrderManager: CustomStringConvertible {
    var description: String { "Buyurtmalar soni: \(ordersCount)" }
}

// 2. Yordamchi metodlar uchun alohida extension:
extension OrderManager {
    func resetOrders() { ordersCount = 0 }
}

let om = OrderManager()
print(om)
```

## Tushuntirish va Mantiq:
Extensionlar kodni fayllar bo'yicha toza bo'lishiga, har bir javobgarlikni alohida saqlashga xizmat qiladi.

## Ishlash natijasi:
```text
Buyurtmalar soni: 0
```


# 679-Topshiriq: Bool xususiyatini teskarisiga o'giruvchi toggled() metodi
## Topshiriq sharti:
Qiymatni o'zgartirmasdan, yangi teskari qiymat qaytaruvchi Bool extensioni.

## Yechim (Swift kodi):
```swift
import Foundation

extension Bool {
    func toggled() -> Bool {
        return !self
    }
}

let flag = true
print("Toggled: \(flag.toggled())")
```

## Tushuntirish va Mantiq:
Oddiy va qulay funktsional metodlar kod ravonligini oshiradi.

## Ishlash natijasi:
```text
Toggled: false
```


# 680-Topshiriq: Array elementlarini guruhlab bo'lish
## Topshiriq sharti:
Massivni juftliklarga ajratuvchi extension.

## Yechim (Swift kodi):
```swift
import Foundation

extension Array {
    func pairs() -> [(Element, Element)] {
        var result = [(Element, Element)]()
        for i in stride(from: 0, to: count - 1, by: 2) {
            result.append((self[i], self[i + 1]))
        }
        return result
    }
}

let list = [1, 2, 3, 4]
print("Juftliklar: \(list.pairs())")
```

## Tushuntirish va Mantiq:
Kolleksiyalarni tahlil qilishda qadamli kengaytmalar juda samarali.

## Ishlash natijasi:
```text
Juftliklar: [(1, 2), (3, 4)]
```


# 681-Topshiriq: String dagi har bir so'z bosh harfini katta qilish: titleCased
## Topshiriq sharti:
Sarlavha formatini hosil qiluvchi String kengaytmasi.

## Yechim (Swift kodi):
```swift
import Foundation

extension String {
    var titleCased: String {
        return self.capitalized
    }
}

print("swift tili darslari".titleCased)
```

## Tushuntirish va Mantiq:
Matnlarni formatlash xususiyatlari UI qatlamida muntazam kerak bo'ladi.

## Ishlash natijasi:
```text
Swift Tili Darslari
```


# 682-Topshiriq: Double sonni so'm valyutasiga formatlovchi extension
## Topshiriq sharti:
Pul miqdorini minglik bo'shliqlar bilan chiroyli formatlash.

## Yechim (Swift kodi):
```swift
import Foundation

extension Double {
    func toUZS() -> String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .decimal
        formatter.groupingSeparator = " "
        let formatted = formatter.string(from: NSNumber(value: self)) ?? "\(self)"
        return "\(formatted) so'm"
    }
}

let balance = 1500000.0
print("Formatlangan summa: \(balance.toUZS())")
```

## Tushuntirish va Mantiq:
Lokalizatsiyalangan valyuta formatlash extensioni moliya ilovalarida eng muhim komponentdir.

## Ishlash natijasi:
```text
Formatlangan summa: 1 500 000 so'm
```


# 683-Topshiriq: Array ning tasodifiy elementini tanlovchi oneRandom() xususiyati
## Topshiriq sharti:
Xavfsiz tasodifiy element qaytaruvchi massiv kengaytmasi.

## Yechim (Swift kodi):
```swift
import Foundation

extension Array {
    var oneRandom: Element? {
        return self.randomElement()
    }
}

let colors = ["Qizil", "Yashil", "Moviy"]
print("Tanlangan rang mavjudmi? \(colors.oneRandom != nil)")
```

## Tushuntirish va Mantiq:
Kolleksiya ustiga qulay sintaktik xususiyatlar qo'shish kod o'qiluvchanligini yaxshilaydi.

## Ishlash natijasi:
```text
Tanlangan rang mavjudmi? true
```


# 684-Topshiriq: Xatoliklarni tahlil qiluvchi Error extensioni
## Topshiriq sharti:
Har qanday Error ga tushunarli kod yoki sabab ajratuvchi xususiyat qo'shish.

## Yechim (Swift kodi):
```swift
import Foundation

extension Error {
    var debugLogString: String {
        return "[XATOLIK - \(type(of: self))]: \(localizedDescription)"
    }
}

let err = URLError(.timedOut)
print(err.debugLogString)
```

## Tushuntirish va Mantiq:
Error protokolini kengaytirish butun ilova bo'ylab audit va nosozliklarni tahlil qilishni birlashtiradi.

## Ishlash natijasi:
```text
[XATOLIK - URLError]: The operation couldn’t be completed. (NSURLErrorDomain error -1001.)
```


# 685-Topshiriq: Int sonining tub (Prime) ekanligini tekshiruvchi isPrime xususiyati
## Topshiriq sharti:
Matematik tub sonlik tekshiruvini Int ga integratsiya qilish.

## Yechim (Swift kodi):
```swift
import Foundation

extension Int {
    var isPrime: Bool {
        guard self > 1 else { return false }
        if self == 2 { return true }
        for i in 2...Int(Double(self).squareRoot()) {
            if self % i == 0 { return false }
        }
        return true
    }
}

print("7 tubmi? \(7.isPrime)")
print("12 tubmi? \(12.isPrime)")
```

## Tushuntirish va Mantiq:
Matematik xususiyatlar bevosita Int turining o'zida ravon o'qiladi.

## Ishlash natijasi:
```text
7 tubmi? true
12 tubmi? false
```


# 686-Topshiriq: String dagi emojilarni aniqlovchi containsEmoji xususiyati
## Topshiriq sharti:
Matnda kamida bitta emoji belgisi borligini tekshiruvchi kengaytma.

## Yechim (Swift kodi):
```swift
import Foundation

extension String {
    var containsEmoji: Bool {
        return unicodeScalars.contains { $0.properties.isEmoji }
    }
}

print("'Salom 😊' da emoji bormi? \("Salom 😊".containsEmoji)")
print("'Salom' da emoji bormi? \("Salom".containsEmoji)")
```

## Tushuntirish va Mantiq:
Unicode scalar xususiyatlari orqali emojilarni aniqlash matn tahlilida juda qulay.

## Ishlash natijasi:
```text
'Salom 😊' da emoji bormi? true
'Salom' da emoji bormi? false
```


# 687-Topshiriq: Kolleksiyaning o'rta elementini topuvchi middleElement xususiyati
## Topshiriq sharti:
Massivning aniq o'rtasida turgan elementni xavfsiz qaytarish.

## Yechim (Swift kodi):
```swift
import Foundation

extension Array {
    var middleElement: Element? {
        guard !isEmpty else { return nil }
        return self[count / 2]
    }
}

print("O'rta element: \([10, 20, 30].middleElement ?? 0)")
```

## Tushuntirish va Mantiq:
Statistik va geometrik tahlillarda medianani topish uchun qo'llaniladi.

## Ishlash natijasi:
```text
O'rta element: 20
```


# 688-Topshiriq: Double sonni yaxlitlovchi rounded(toPlaces:) metodi
## Topshiriq sharti:
Sonni berilgan verguldan keyingi xonalar sonigacha aniq yaxlitlash.

## Yechim (Swift kodi):
```swift
import Foundation

extension Double {
    func rounded(toPlaces places: Int) -> Double {
        let divisor = pow(10.0, Double(places))
        return (self * divisor).rounded() / divisor
    }
}

let pi = 3.14159265
print("Yaxlitlangan (2 xona): \(pi.rounded(toPlaces: 2))")
print("Yaxlitlangan (4 xona): \(pi.rounded(toPlaces: 4))")
```

## Tushuntirish va Mantiq:
Sonlarni formatlash va yaxlitlash moliyaviy hisob-kitoblarda xatoliklarni kamaytiradi.

## Ishlash natijasi:
```text
Yaxlitlangan (2 xona): 3.14
Yaxlitlangan (4 xona): 3.1416
```


# 689-Topshiriq: Dictionary ga invert() metodi: Kalit va qiymatlar o'rnini almashtirish
## Topshiriq sharti:
Unikal qiymatlarga ega lug'atning kalit va qiymatlarini almashtirib yangi lug'at hosil qilish.

## Yechim (Swift kodi):
```swift
import Foundation

extension Dictionary where Value: Hashable {
    func inverted() -> [Value: Key] {
        return Dictionary<Value, Key>(uniqueKeysWithValues: map { ($1, $0) })
    }
}

let dict = ["A": 1, "B": 2]
print("Teskari lug'at: \(dict.inverted())")
```

## Tushuntirish va Mantiq:
Teskari qidiruv (Reverse Lookup) jadvallarini tuzishda invert() metodi juda qulaydir.

## Ishlash natijasi:
```text
Teskari lug'at: [2: "B", 1: "A"]
```


# 690-Topshiriq: Kolleksiyada n tadan elementlarni tashlab o'tish
## Topshiriq sharti:
Har N-chi elementni tanlab oluvchi kengaytma.

## Yechim (Swift kodi):
```swift
import Foundation

extension Array {
    func every(step: Int) -> [Element] {
        guard step > 0 else { return [] }
        return stride(from: 0, to: count, by: step).map { self[$0] }
    }
}

let letters = ["A", "B", "C", "D", "E", "F"]
print("Har 2-chi element: \(letters.every(step: 2))")
```

## Tushuntirish va Mantiq:
Kolleksiya ustidagi algoritmlarni extensionga chiqarish ularni butun loyihada foydalanishga ochadi.

## Ishlash natijasi:
```text
Har 2-chi element: ["A", "C", "E"]
```


# 691-Topshiriq: Character ning unli harf ekanligini tekshiruvchi isVowel xususiyati
## Topshiriq sharti:
Belgi unli tovush ekanligini tekshirish.

## Yechim (Swift kodi):
```swift
import Foundation

extension Character {
    var isVowel: Bool {
        return "aeiouаеиоуў".contains(self.lowercased())
    }
}

print("'a' unlimi? \(Character("a").isVowel)")
print("'b' unlimi? \(Character("b").isVowel)")
```

## Tushuntirish va Mantiq:
Belgilar darajasidagi kengaytmalar matn tahlilini (NLP) sezilarli soddalashtiradi.

## Ishlash natijasi:
```text
'a' unlimi? true
'b' unlimi? false
```


# 692-Topshiriq: String dan so'zlar sonini hisoblovchi wordCount xususiyati
## Topshiriq sharti:
Matndagi bo'shliqlar bilan ajratilgan so'zlar sonini aniqlash.

## Yechim (Swift kodi):
```swift
import Foundation

extension String {
    var wordCount: Int {
        return self.split(separator: " ").count
    }
}

print("So'zlar soni: \("Swift dasturlash tili juda kuchli".wordCount)")
```

## Tushuntirish va Mantiq:
Matn statistikasi xususiyatlari kontent tahrirlovchi ilovalarda juda keraklidir.

## Ishlash natijasi:
```text
So'zlar soni: 5
```


# 693-Topshiriq: Set ga element qo'shilganda yangi to'plam qaytaruvchi inserting() metodi
## Topshiriq sharti:
O'zgarmas to'plamga yangi qiymat qo'shib yangi to'plam hosil qilish.

## Yechim (Swift kodi):
```swift
import Foundation

extension Set {
    func inserting(_ newMember: Element) -> Set<Element> {
        var copy = self
        copy.insert(newMember)
        return copy
    }
}

let s1: Set = ["A", "B"]
let s2 = s1.inserting("C")
print("s2 elementlari: \(s2.sorted())")
```

## Tushuntirish va Mantiq:
Funktsional dasturlashda o'zgarmas nusxalar bilan ishlash uchun 'inserting()' uslubidagi metodlar qo'l keladi.

## Ishlash natijasi:
```text
s2 elementlari: ["A", "B", "C"]
```


# 694-Topshiriq: String dagi maxsus belgilarni tozalovchi alphanumericOnly xususiyati
## Topshiriq sharti:
Faqat harf va raqamlarni qoldirib, qolgan belgilarni o'chirish.

## Yechim (Swift kodi):
```swift
import Foundation

extension String {
    var alphanumericOnly: String {
        return self.filter { $0.isLetter || $0.isNumber }
    }
}

print("Tozalangan: \("ID-#998-AZ!".alphanumericOnly)")
```

## Tushuntirish va Mantiq:
Xavfsiz identifikatorlar yaratishda maxsus belgilarni tozalash zarurdir.

## Ishlash natijasi:
```text
Tozalangan: ID998AZ
```


# 695-Topshiriq: Array elementlarini qulay formatda chop etuvchi dumpConsole() metodi
## Topshiriq sharti:
Massivning barcha a'zolarini raqamlangan ro'yxat sifatida konsolga chiqarish.

## Yechim (Swift kodi):
```swift
import Foundation

extension Array {
    func dumpConsole() {
        for (i, val) in self.enumerated() {
            print("\(i + 1). \(val)")
        }
    }
}

["Olma", "Anor"].dumpConsole()
```

## Tushuntirish va Mantiq:
Kolleksiyalarni debug qilishda maxsus chop etish metodlari juda qulay.

## Ishlash natijasi:
```text
1. Olma
2. Anor
```


# 696-Topshiriq: Int sonining juftligini tekshiruvchi isEven va isOdd xususiyatlari
## Topshiriq sharti:
Matematik qisqa mantiqiy xususiyatlar.

## Yechim (Swift kodi):
```swift
import Foundation

extension Int {
    var isEven: Bool { self % 2 == 0 }
    var isOdd: Bool { self % 2 != 0 }
}

print("4 juftmi? \(4.isEven)")
print("7 toqmi? \(7.isOdd)")
```

## Tushuntirish va Mantiq:
Kichik, aniq va ixcham kengaytmalar butun kod bazasida tozalik yaratadi.

## Ishlash natijasi:
```text
4 juftmi? true
7 toqmi? true
```


# 697-Topshiriq: Double sonni foiz matniga o'tkazuvchi toPercentage() metodi
## Topshiriq sharti:
0.155 ni '15.5%' shaklida formatlash.

## Yechim (Swift kodi):
```swift
import Foundation

extension Double {
    func toPercentage(decimals: Int = 1) -> String {
        return String(format: "%.*f%%", decimals, self * 100.0)
    }
}

print(0.8525.toPercentage(decimals: 2))
```

## Tushuntirish va Mantiq:
Ko'rsatkichlar va analitika UI larida foiz formatlash juda qulaydir.

## Ishlash natijasi:
```text
85.25%
```


# 698-Topshiriq: Sequence dagi elementlarning mavjudligini teskari tekshirish: noneSatisfy
## Topshiriq sharti:
Barcha elementlar shartga mos kelmasligini kafolatlash.

## Yechim (Swift kodi):
```swift
import Foundation

extension Sequence {
    func noneSatisfy(_ predicate: (Element) -> Bool) -> Bool {
        return !contains(where: predicate)
    }
}

print("Manfiy sonlar yo'qmi? \([1, 2, 3].noneSatisfy { $0 < 0 })")
```

## Tushuntirish va Mantiq:
Mantiqiy ifodalarda 'noneSatisfy' 'allSatisfy' va 'contains' ni mukammal to'ldiradi.

## Ishlash natijasi:
```text
Manfiy sonlar yo'qmi? true
```


# 699-Topshiriq: String dagi qatorlar sonini hisoblovchi linesCount xususiyati
## Topshiriq sharti:
Ko'p qatorli matndagi qatorlar sanog'ini topish.

## Yechim (Swift kodi):
```swift
import Foundation

extension String {
    var linesCount: Int {
        var count = 0
        self.enumerateLines { _, _ in count += 1 }
        return count
    }
}

let poem = """
O'zbekiston go'zal diyor,
Har faslida o'z xislat bor.
"""
print("Qatorlar soni: \(poem.linesCount)")
```

## Tushuntirish va Mantiq:
'enumerateLines' satrlarni xotirada bo'laklamasdan samarali sanaydi.

## Ishlash natijasi:
```text
Qatorlar soni: 2
```


# 700-Topshiriq: Amaliy loyiha: Swift standart kutubxonasini kengaytiruvchi to'liq Professional Utility Framework moduli
## Topshiriq sharti:
String, Int, Double, Date, Collection va Optional turlariga kiritilgan barcha professional kengaytmalarni o'z ichiga olgan yaxlit kutubxona moduli.

## Yechim (Swift kodi):
```swift
import Foundation

// MARK: - String Utilities
extension String {
    var isBlank: Bool { trimmingCharacters(in: .whitespacesAndNewlines).isEmpty }
    var cleanedPhone: String { filter { $0.isNumber } }
}

// MARK: - Numeric Utilities
extension Double {
    var currencyFormatted: String {
        return String(format: "$%.2f", self)
    }
}

extension Int {
    var isEven: Bool { self % 2 == 0 }
}

// MARK: - Collection Utilities
extension Collection {
    subscript(safe index: Index) -> Element? {
        indices.contains(index) ? self[index] : nil
    }
}

// MARK: - Optional Utilities
extension Optional where Wrapped == String {
    var orDefaultText: String {
        self?.isBlank == false ? self! : "Standart ma'lumot"
    }
}

// Loyiha demonstratsiyasi:
print("=== UTILITY FRAMEWORK ISHGA TUSHDI ===")
let rawBio: String? = "   "
print("Bio: \(rawBio.orDefaultText)")

let price: Double = 249.99
print("Narx: \(price.currencyFormatted)")

let tags = ["iOS", "Swift", "SwiftUI"]
print("Tanlangan teg: \(tags[safe: 1] ?? "Yo'q")")
print("Noto'g'ri indeks: \(tags[safe: 5] ?? "Topilmadi")")
```

## Tushuntirish va Mantiq:
Ushbu yakuniy loyihada barcha asosiy Swift turlarini (String, Double, Int, Collection, Optional) professional darajada kengaytiruvchi to'liq qayta ishlatiluvchi kutubxona yaratildi.

## Ishlash natijasi:
```text
=== UTILITY FRAMEWORK ISHGA TUSHDI ===
Bio: Standart ma'lumot
Narx: $249.99
Tanlangan teg: Swift
Noto'g'ri indeks: Topilmadi
```

