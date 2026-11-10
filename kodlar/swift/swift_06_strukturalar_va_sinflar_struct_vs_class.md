# 251-Topshiriq: Struct e'lon qilish va instansiya olish
## Topshiriq sharti:
Geografik nuqtani ifodalovchi struct yarating va uning parametrlarini o'qing.

## Yechim (Swift kodi):
```swift
import Foundation

struct GPSLocation {
    var latitude: Double
    var longitude: Double
}

let toshkent = GPSLocation(latitude: 41.2995, longitude: 69.2401)
print("Kenglik: \(toshkent.latitude), Uzunlik: \(toshkent.longitude)")
```

## Tushuntirish va Mantiq:
Swift-da 'struct' qiymat turi (Value Type) bo'lib, ob'ektga yo'naltirilgan va funktsional modellarni tuzishda asosiy qurilish bloki hisoblanadi.

## Ishlash natijasi:
```text
Kenglik: 41.2995, Uzunlik: 69.2401
```


# 252-Topshiriq: Class e'lon qilish va instansiya olish
## Topshiriq sharti:
Foydalanuvchi akkauntini ifodalovchi sinf va uning initsializatorini yozing.

## Yechim (Swift kodi):
```swift
import Foundation

class UserAccount {
    var username: String
    var email: String
    
    init(username: String, email: String) {
        self.username = username
        self.email = email
    }
}

let account = UserAccount(username: "bekzod", email: "bekzod@khorazmiy.uz")
print("Foydalanuvchi: \(account.username), Pochta: \(account.email)")
```

## Tushuntirish va Mantiq:
'class' havola turi (Reference Type) bo'lib, o'z xususiyatlari uchun initsializator talab qiladi va umumiy xotirani bir nechta manbalar bilan bo'lishish imkonini beradi.

## Ishlash natijasi:
```text
Foydalanuvchi: bekzod, Pochta: bekzod@khorazmiy.uz
```


# 253-Topshiriq: Qiymat turi (Value Type) semantikasi: Nusxalash
## Topshiriq sharti:
Struct boshqa o'zgaruvchiga berilganda asl nusxaga daxl qilmasdan mustaqil nusxa olinishini isbotlang.

## Yechim (Swift kodi):
```swift
import Foundation

struct ScoreBoard {
    var points: Int
}

var original = ScoreBoard(points: 100)
var copy = original

copy.points = 250

print("Asl ball: \(original.points)")
print("Nusxa ball: \(copy.points)")
```

## Tushuntirish va Mantiq:
Struct-lar 'Value Type' bo'lgani sababli, qiymat berilganda butun ma'lumot to'liq xotira nusxasi sifatida ko'chiriladi. Biriga kiritilgan o'zgarish ikkinchisiga mutlaqo ta'sir qilmaydi.

## Ishlash natijasi:
```text
Asl ball: 100
Nusxa ball: 250
```


# 254-Topshiriq: Havola turi (Reference Type) semantikasi: Xotira ko'rsatkichi
## Topshiriq sharti:
Class nusxasi boshqa o'zgaruvchiga berilganda ikkalasi ham bitta xotiraga murojaat qilishini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class GameSession {
    var score: Int = 100
}

let session1 = GameSession()
let session2 = session1 // Havola nusxalandi

session2.score = 500

print("session1 ball: \(session1.score)")
print("session2 ball: \(session2.score)")
```

## Tushuntirish va Mantiq:
Sinflar 'Reference Type' bo'lib, o'zgaruvchilar asl ma'lumotni emas, balki Heap xotirasidagi manzilni (pointer) saqlaydi. Bitta havola orqali o'zgartirilgan ma'lumot barcha havolalarda aks etadi.

## Ishlash natijasi:
```text
session1 ball: 500
session2 ball: 500
```


# 255-Topshiriq: Avtomatik a'zolik initsializatori (Memberwise Initializer)
## Topshiriq sharti:
Struct konstruktor yozilmasa ham barcha maydonlar uchun avtomatik initsializator olishini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

struct FlightInfo {
    let flightNumber: String
    let origin: String
    let destination: String
    var delayMinutes: Int = 0
}

let flight = FlightInfo(flightNumber: "HY-101", origin: "Toshkent", destination: "Urganch")
print("Parvoz: \(flight.flightNumber), Kechikish: \(flight.delayMinutes) daqiqa")
```

## Tushuntirish va Mantiq:
Swift kompilyatori struct lar uchun barcha parametrlar bo'yicha 'memberwise initializer'ni avtomatik ravishda generatsiya qiladi.

## Ishlash natijasi:
```text
Parvoz: HY-101, Kechikish: 0 daqiqa
```


# 256-Topshiriq: Class larda initsializatorning majburiyligi
## Topshiriq sharti:
Class larda default qiymati bo'lmagan maydonlar uchun 'init' yozilishi shart ekanligini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class ServerConnection {
    let host: String
    let port: Int
    
    init(host: String, port: Int) {
        self.host = host
        self.port = port
    }
}

let conn = ServerConnection(host: "api.khorazmiy.uz", port: 443)
print("Ulandi: \(conn.host):\(conn.port)")
```

## Tushuntirish va Mantiq:
Sinflar avtomatik memberwise initializer ololmaydi. Barcha saqlanuvchi xususiyatlar initsializatsiya jarayonida aniq qiymat olishi shart.

## Ishlash natijasi:
```text
Ulandi: api.khorazmiy.uz:443
```


# 257-Topshiriq: mutating metodlar: Struct ichki holatini o'zgartirish
## Topshiriq sharti:
Struct metodida xususiyatlarni o'zgartirish uchun 'mutating' kalit so'zini qo'llang.

## Yechim (Swift kodi):
```swift
import Foundation

struct Counter {
    var count: Int = 0
    
    mutating func increment() {
        count += 1
    }
    
    mutating func reset() {
        count = 0
    }
}

var c = Counter()
c.increment()
c.increment()
print("Hisob: \(c.count)")
c.reset()
print("Tiklandi: \(c.count)")
```

## Tushuntirish va Mantiq:
Struct xususiyatlari standart holda o'zgarmas deb qaraladi. Ularni o'zgartiruvchi metodlar boshiga 'mutating' qo'yilishi shart, bu metod self o'rniga yangi o'zgargan nusxa qo'yishini bildiradi.

## Ishlash natijasi:
```text
Hisob: 2
Tiklandi: 0
```


# 258-Topshiriq: Nima uchun class metodlariga 'mutating' kerak emas
## Topshiriq sharti:
Class instansiyasida metodlar to'g'ridan-to'g'ri maydonlarni o'zgartira olishini tushuntiring.

## Yechim (Swift kodi):
```swift
import Foundation

class LightSwitch {
    var isOn: Bool = false
    
    func flip() {
        isOn.toggle() // mutating shart emas!
    }
}

let light = LightSwitch()
light.flip()
print("Chiroq yondimi? \(light.isOn)")
```

## Tushuntirish va Mantiq:
Sinflar havola turi bo'lgani sababli, metod chaqirilganda ob'ektning Heap-dagi xotirasi o'zgaradi, havola o'zgarmaydi. Shu sababli class larda 'mutating' talab qilinmaydi.

## Ishlash natijasi:
```text
Chiroq yondimi? true
```


# 259-Topshiriq: let bilan e'lon qilingan struct o'zgarmasligi
## Topshiriq sharti:
Konstanta struct-ning hatto 'var' maydonlarini ham o'zgartirib bo'lmasligini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

struct Point {
    var x: Int
    var y: Int
}

let fixedPoint = Point(x: 10, y: 20)
// fixedPoint.x = 30 // Kompilyatsiya xatosi: Cannot assign to property: 'fixedPoint' is a 'let' constant

print("O'zgarmas nuqta: (\(fixedPoint.x), \(fixedPoint.y))")
```

## Tushuntirish va Mantiq:
Agar struct 'let' bilan e'lon qilinsa, uning butun tanasi va barcha ichki xususiyatlari o'zgarmas (immutable) bo'lib qoladi.

## Ishlash natijasi:
```text
O'zgarmas nuqta: (10, 20)
```


# 260-Topshiriq: let bilan e'lon qilingan class maydonlarini o'zgartirish
## Topshiriq sharti:
Konstanta class ko'rsatkichining ichki o'zgaruvchan maydonlari mutatsiyaga ochiq ekanligini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class Player {
    var level: Int = 1
}

let constantPlayer = Player()
constantPlayer.level = 5 // Muvaffaqiyatli o'zgaradi!
// constantPlayer = Player() // Xato: havolaning o'zini o'zgartirib bo'lmaydi

print("O'yinchi darajasi: \(constantPlayer.level)")
```

## Tushuntirish va Mantiq:
'let constantPlayer' faqat xotira ko'rsatkichining o'zgarmasligini kafolatlaydi, ko'rsatkich ishora qilayotgan ob'ektning ichki 'var' maydonlari esa o'zgartirilishi mumkin.

## Ishlash natijasi:
```text
O'yinchi darajasi: 5
```


# 261-Topshiriq: Identiklik operatorlari (=== va !==) faqat sinflar uchun
## Topshiriq sharti:
Ikki havola bir xil xotira manziliga tegishli ekanligini '===' orqali tekshiring.

## Yechim (Swift kodi):
```swift
import Foundation

class Document {
    let title: String
    init(title: String) { self.title = title }
}

let doc1 = Document(title: "Shartnoma")
let doc2 = doc1
let doc3 = Document(title: "Shartnoma")

print("doc1 === doc2: \(doc1 === doc2)")
print("doc1 === doc3: \(doc1 === doc3)")
```

## Tushuntirish va Mantiq:
'===' operatori faqat sinflar uchun mavjud bo'lib, ikkala ko'rsatkich aynan bitta ob'ektga ishora qilayotganini tekshiradi. Struct lar qiymat turi bo'lgani uchun ularga '===' qo'llanmaydi.

## Ishlash natijasi:
```text
doc1 === doc2: true
doc1 === doc3: false
```


# 262-Topshiriq: Equatable protokoli va qiymat tengligi (==)
## Topshiriq sharti:
Struct parametrlarining qiymat tengligini '==' operatori bilan tekshiring.

## Yechim (Swift kodi):
```swift
import Foundation

struct Dimension: Equatable {
    let width: Double
    let height: Double
}

let d1 = Dimension(width: 1920, height: 1080)
let d2 = Dimension(width: 1920, height: 1080)

print("O'lchamlar tengmi? \(d1 == d2)")
```

## Tushuntirish va Mantiq:
Swift struct larida agar barcha xususiyatlar Equatable bo'lsa, 'Equatable' protokolini e'lon qilish orqali '==' operatori avtomatik sintezlanadi.

## Ishlash natijasi:
```text
O'lchamlar tengmi? true
```


# 263-Topshiriq: Copy-on-Write (CoW) mexanizmi
## Topshiriq sharti:
Swift-dagi massivlar faqat o'zgarish kiritilgandagina haqiqiy xotira nusxasini yaratishini tushuntiring.

## Yechim (Swift kodi):
```swift
import Foundation

var array1 = [1, 2, 3, 4, 5]
var array2 = array1 // Shu paytda ikkalasi ham bitta xotira buferiga qaraydi!

array2.append(6) // Aynan shu mutatsiya paytida array2 uchun yangi xotira ajratiladi (CoW)

print("Array 1: \(array1)")
print("Array 2: \(array2)")
```

## Tushuntirish va Mantiq:
Copy-on-Write — Swift massivlari va to'plamlarining xotira samaradorligi siri. Nusxalanganda xotira ko'chirilmaydi, faqat ikkinchi nusxaga yozish amalga oshirilgandagina haqiqiy xotira ko'chiriladi.

## Ishlash natijasi:
```text
Array 1: [1, 2, 3, 4, 5]
Array 2: [1, 2, 3, 4, 5, 6]
```


# 264-Topshiriq: Maxsus Struct uchun Copy-on-Write yaratish
## Topshiriq sharti:
'isKnownUniquelyReferenced' funksiyasi orqali o'z shaxsiy CoW ma'lumot tuzilmangizni yozing.

## Yechim (Swift kodi):
```swift
import Foundation

final class Storage {
    var data: String
    init(data: String) { self.data = data }
}

struct CustomBuffer {
    private var storage: Storage
    
    init(data: String) {
        self.storage = Storage(data: data)
    }
    
    var data: String {
        get { storage.data }
        set {
            if !isKnownUniquelyReferenced(&storage) {
                print("CoW: Yangi xotira nusxasi yaratildi!")
                storage = Storage(data: newValue)
            } else {
                print("CoW: Mavjud xotira joyida yangilandi.")
                storage.data = newValue
            }
        }
    }
}

var buf1 = CustomBuffer(data: "Boshlang'ich")
var buf2 = buf1
buf2.data = "Yangilangan"
```

## Tushuntirish va Mantiq:
'isKnownUniquelyReferenced' havola hisoblagichi 1 ga tengligini tekshiradi. Agar ob'ektni bir nechta manba ushlab turgan bo'lsa, xavfsiz yangi nusxa ajratiladi.

## Ishlash natijasi:
```text
CoW: Yangi xotira nusxasi yaratildi!
```


# 265-Topshiriq: Merosxo'rlik: Faqat sinflar meros olishi mumkin
## Topshiriq sharti:
Baza sinfidan yangi sinf meros olib metodni kengaytirishini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class Vehicle {
    var speed: Int = 0
    func makeNoise() {
        print("Transport harakatlanmoqda.")
    }
}

class Train: Vehicle {
    override func makeNoise() {
        print("Chux-chux! Poezd signali.")
    }
}

let t = Train()
t.makeNoise()
```

## Tushuntirish va Mantiq:
Swift-da merosxo'rlik (Inheritance) faqat sinflar uchun xos. Struct-lar boshqa struct-dan meros ololmaydi, faqat protokollarni qabul qila oladi.

## Ishlash natijasi:
```text
Chux-chux! Poezd signali.
```


# 266-Topshiriq: deinit faqat sinflarda mavjud
## Topshiriq sharti:
Class ob'ekti xotiradan o'chganda deinit bloki chaqirilishini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class TempResource {
    let id: Int
    init(id: Int) {
        self.id = id
        print("Resurs #\(id) yaratildi.")
    }
    deinit {
        print("Resurs #\(id) xotiradan tozalandi.")
    }
}

do {
    let _ = TempResource(id: 101)
}
print("Skopdan chiqildi.")
```

## Tushuntirish va Mantiq:
'deinit' (deinitializer) ob'ektning havola hisoblagichi nolga tushganda avtomatik chaqiriladi. Struct larda esa deinit bo'lmaydi, chunki ular skopdan chiqishi bilan stakdan darhol uchib ketadi.

## Ishlash natijasi:
```text
Resurs #101 yaratildi.
Resurs #101 xotiradan tozalandi.
Skopdan chiqildi.
```


# 267-Topshiriq: Xotira taqsimlanishi: Stack (Struct) vs Heap (Class)
## Topshiriq sharti:
Struct stekda tezkor saqlanishini va class esa Heap da havola orqali yashashini tushuntiring.

## Yechim (Swift kodi):
```swift
import Foundation

struct StackAllocated {
    let a: Int
    let b: Int
}

class HeapAllocated {
    let a: Int
    let b: Int
    init(a: Int, b: Int) { self.a = a; self.b = b }
}

let s = StackAllocated(a: 1, b: 2)
let h = HeapAllocated(a: 1, b: 2)

print("Struct va Class instansiyalari muvaffaqiyatli ishga tushirildi.")
```

## Tushuntirish va Mantiq:
Stek (Stack) xotirasi juda tezkor bo'lib, unga CPU ko'rsatkichi surilishi orqali xotira ajratiladi. Heap xotirasi esa erkin dinamik hudud bo'lib, xotira izlash va havola hisoblash (ARC) xarajatlarini talab qiladi.

## Ishlash natijasi:
```text
Struct va Class instansiyalari muvaffaqiyatli ishga tushirildi.
```


# 268-Topshiriq: Ko'p oqimli muhitda Struct xavfsizligi (Thread-Safety)
## Topshiriq sharti:
Struct qiymat nusxalanishi tufayli oqimlar o'rtasida poyga holati (Data Race) keltirib chiqarmasligini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

struct WorkData {
    var counter: Int
}

let originalData = WorkData(counter: 0)

// Har bir yangi oqim o'zining mustaqil nusxasini oladi:
var threadOneCopy = originalData
threadOneCopy.counter += 10

var threadTwoCopy = originalData
threadTwoCopy.counter += 20

print("Oqim 1: \(threadOneCopy.counter)")
print("Oqim 2: \(threadTwoCopy.counter)")
print("Asl holat: \(originalData.counter)")
```

## Tushuntirish va Mantiq:
Struct lar har bir oqimga yangi xotira nusxasi sifatida uzatilganligi bois, ular o'zaro bir-birining xotirasini buzish xavfidan xoli (thread-safe by default).

## Ishlash natijasi:
```text
Oqim 1: 10
Oqim 2: 20
Asl holat: 0
```


# 269-Topshiriq: Apple tavsiyalari: Qachon Struct va qachon Class
## Topshiriq sharti:
Apple muhandislari tavsiya etgan tanlov tamoyillarini kodda ifodalang.

## Yechim (Swift kodi):
```swift
import Foundation

// Standart holda DOIMO Struct ishlatiladi:
struct UserModel {
    let id: UUID
    let name: String
}

// Faqat umumiy holat va identiklik kerak bo'lganda Class ishlatiladi:
class AudioHardwareManager {
    static let shared = AudioHardwareManager()
    private init() {}
    func playTone() { print("Ovoz yangradi") }
}

AudioHardwareManager.shared.playTone()
```

## Tushuntirish va Mantiq:
Swift falsafasiga ko'ra, standart holda (by default) modellar uchun STRUCT tanlanadi. Faqat ob'ektning yagona identifikatori (identity) va resurslarni boshqarish zarur bo'lgandagina CLASS ishlatiladi.

## Ishlash natijasi:
```text
Ovoz yangradi
```


# 270-Topshiriq: Struct ichida Class ob'ektini saqlash
## Topshiriq sharti:
Struct ichidagi class havolasi nusxalanganida qanday xatti-harakat sodir bo'lishini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class Engine {
    var horsepower = 200
}

struct Car {
    var brand: String
    var engine: Engine
}

var car1 = Car(brand: "Sedan", engine: Engine())
var car2 = car1

car2.engine.horsepower = 350

print("Car 1 dvigatel kuchi: \(car1.engine.horsepower)")
print("Car 2 dvigatel kuchi: \(car2.engine.horsepower)")
```

## Tushuntirish va Mantiq:
Agar Struct ichida Class havolasi bo'lsa, struct nusxalanganda havola ham nusxalanadi va ikkala struct bitta dvigatelga qarab qoladi. Bunga 'Mixed Semantics' deyiladi.

## Ishlash natijasi:
```text
Car 1 dvigatel kuchi: 350
Car 2 dvigatel kuchi: 350
```


# 271-Topshiriq: Class ichida Struct saqlash va inkapsulyatsiya
## Topshiriq sharti:
Class ichidagi struct qiymatini xavfsiz boshqarish modulini tuzing.

## Yechim (Swift kodi):
```swift
import Foundation

struct UserStats {
    var wins: Int = 0
    var losses: Int = 0
}

class PlayerAccount {
    var stats = UserStats()
    
    func recordWin() {
        stats.wins += 1
    }
}

let p = PlayerAccount()
p.recordWin()
print("G'alabalar soni: \(p.stats.wins)")
```

## Tushuntirish va Mantiq:
Class o'z ichida qiymat turlarini saqlab, biznes mantiqni toza inkapsulyatsiya qilishi mumkin.

## Ishlash natijasi:
```text
G'alabalar soni: 1
```


# 272-Topshiriq: Ichki turlar (Nested Types) struct va sinflarda
## Topshiriq sharti:
Struktura ichida maxsus enum yoki boshqa yordamchi tuzilmalarni joylashtiring.

## Yechim (Swift kodi):
```swift
import Foundation

struct DeviceInfo {
    enum FormFactor {
        case phone
        case tablet
        case laptop
    }
    
    let modelName: String
    let form: FormFactor
}

let dev = DeviceInfo(modelName: "iPad Pro", form: .tablet)
print("Qurilma: \(dev.modelName), Shakli: \(dev.form)")
```

## Tushuntirish va Mantiq:
Ichki turlar (Nested Types) kod nomlari fazosini toza saqlashga va tegishli turlarni o'z kontekstida guruhlashga xizmat qiladi.

## Ishlash natijasi:
```text
Qurilma: iPad Pro, Shakli: tablet
```


# 273-Topshiriq: CustomStringConvertible bilan chiroyli konsol chiqishi
## Topshiriq sharti:
Struct chop etilganda maxsus matn ko'rinishida chiqishini ta'minlang.

## Yechim (Swift kodi):
```swift
import Foundation

struct Book: CustomStringConvertible {
    let title: String
    let author: String
    
    var description: String {
        return "Kitob: '\(title)' (Muallif: \(author))"
    }
}

let b = Book(title: "O'tkan kunlar", author: "Abdulla Qodiriy")
print(b)
```

## Tushuntirish va Mantiq:
'CustomStringConvertible' protokolining 'description' xususiyati ob'ekt konsolga yoki String interpolyatsiyasiga kiritilganda qanday ko'rinishini belgilaydi.

## Ishlash natijasi:
```text
Kitob: 'O'tkan kunlar' (Muallif: Abdulla Qodiriy)
```


# 274-Topshiriq: Codable bilan JSON ga aylanishi
## Topshiriq sharti:
Struct ma'lumotlarini JSON formatiga avtomatik serializatsiya qiling.

## Yechim (Swift kodi):
```swift
import Foundation

struct ProductPayload: Codable {
    let sku: String
    let price: Double
}

let prod = ProductPayload(sku: "APPLE_M3", price: 1299.99)
let encoder = JSONEncoder()
if let jsonData = try? encoder.encode(prod),
   let jsonString = String(data: jsonData, encoding: .utf8) {
    print("JSON natijasi: \(jsonString)")
}
```

## Tushuntirish va Mantiq:
Swift-da barcha maydonlari Codable bo'lgan struct larda JSON kodlash va dekodlash to'liq avtomatik amalga oshiriladi.

## Ishlash natijasi:
```text
JSON natijasi: {"sku":"APPLE_M3","price":1299.99}
```


# 275-Topshiriq: O'zgarmas ma'lumotlar modeli (Immutable Model)
## Topshiriq sharti:
Faqat 'let' maydonlaridan iborat mutatsiyasiz toza ma'lumot tuzilmasi yarating.

## Yechim (Swift kodi):
```swift
import Foundation

struct TransactionRecord {
    let transactionID: String
    let timestamp: Date
    let amount: Double
}

let tx = TransactionRecord(transactionID: "TX_9901", timestamp: Date(), amount: 75.0)
print("Tranzaksiya qaydi: \(tx.transactionID) - $\(tx.amount)")
```

## Tushuntirish va Mantiq:
O'zgarmas modellar dastur xavfsizligini kafolatlaydi: bir marta yaratilgan ma'lumotni hech kim o'zgartira olmaydi.

## Ishlash natijasi:
```text
Tranzaksiya qaydi: TX_9901 - $75.0
```


# 276-Topshiriq: Sinf instansiyasini chuqur nusxalash (Deep Copy)
## Topshiriq sharti:
Class ob'ektining xotiradagi barcha ma'lumotlari bilan alohida yangi nusxasini yaratuvchi metod yozing.

## Yechim (Swift kodi):
```swift
import Foundation

class ProfileSettings {
    var darkMode: Bool
    
    init(darkMode: Bool) { self.darkMode = darkMode }
    
    func copy() -> ProfileSettings {
        return ProfileSettings(darkMode: self.darkMode)
    }
}

let original = ProfileSettings(darkMode: false)
let cloned = original.copy()

cloned.darkMode = true

print("Asl dark mode: \(original.darkMode)")
print("Klon dark mode: \(cloned.darkMode)")
```

## Tushuntirish va Mantiq:
Sinflarda alohida mustaqil nusxa hosil qilish uchun qo'lda 'Deep Copy' metodi yoziladi.

## Ishlash natijasi:
```text
Asl dark mode: false
Klon dark mode: true
```


# 277-Topshiriq: Singleton Pattern sinf yordamida
## Topshiriq sharti:
Butun ilovada faqat bitta nusxada mavjud bo'ladigan global xizmatni yarating.

## Yechim (Swift kodi):
```swift
import Foundation

class AppConfiguration {
    static let shared = AppConfiguration()
    
    var themeName: String = "Standart Moviy"
    
    private init() {
        // Tashqaridan yangi nusxa olishni taqiqlash
    }
}

let config1 = AppConfiguration.shared
let config2 = AppConfiguration.shared

config1.themeName = "Tungi Rejim"
print("Config 2 dagi mavzu: \(config2.themeName)")
```

## Tushuntirish va Mantiq:
Swift-da 'static let shared' bir marta, thread-safe (oqimlar uchun xavfsiz) tarzda kechiktirilib initsializatsiya qilinadi. 'private init()' esa boshqa nusxalar yaratilishini cheklaydi.

## Ishlash natijasi:
```text
Config 2 dagi mavzu: Tungi Rejim
```


# 278-Topshiriq: Fabrika metodi (Factory Method) sinflarda
## Topshiriq sharti:
Turli xil foydalanuvchi sinflarini bitta markaziy metod orqali hosil qiling.

## Yechim (Swift kodi):
```swift
import Foundation

class Employee {
    let name: String
    let role: String
    init(name: String, role: String) { self.name = name; self.role = role }
    
    static func makeDeveloper(name: String) -> Employee {
        return Employee(name: name, role: "iOS Muhandisi")
    }
}

let dev = Employee.makeDeveloper(name: "Sanjar")
print("Xodim: \(dev.name), Lavozim: \(dev.role)")
```

## Tushuntirish va Mantiq:
Statik fabrika metodlari initsializatsiya jarayonini soddalashtiradi va tayyor konfiguratsiyalangan obyektlarni ishlab chiqaradi.

## Ishlash natijasi:
```text
Xodim: Sanjar, Lavozim: iOS Muhandisi
```


# 279-Topshiriq: Repository Pattern struct yordamida
## Topshiriq sharti:
Ma'lumotlar bazasi operatsiyalarini struct orqali tashkil etish.

## Yechim (Swift kodi):
```swift
import Foundation

struct UserDataRepository {
    private var storage: [Int: String] = [:]
    
    mutating func save(id: Int, name: String) {
        storage[id] = name
    }
    
    func get(id: Int) -> String? {
        return storage[id]
    }
}

var repo = UserDataRepository()
repo.save(id: 1, name: "Dilshod")
print("Topildi: \(repo.get(id: 1) ?? "")")
```

## Tushuntirish va Mantiq:
Repository pattern ma'lumotlarni saqlash va olish qatlamini biznes logikadan toza ajratadi.

## Ishlash natijasi:
```text
Topildi: Dilshod
```


# 280-Topshiriq: SwiftUI View larining struct ekanligi sababi
## Topshiriq sharti:
SwiftUI nima sababdan interfeys elementlarini struct qilganini namoyish eting.

## Yechim (Swift kodi):
```swift
import Foundation

struct CustomCardView {
    let title: String
    let isHighlighted: Bool
    
    func render() {
        print("Karta chizildi: [\(title)] (Ajratilgan: \(isHighlighted))")
    }
}

let card = CustomCardView(title: "Yangiliklar", isHighlighted: true)
card.render()
```

## Tushuntirish va Mantiq:
SwiftUI dagi View lar stakda joylashadi, juda arzon va soniyasiga minglab marta qayta yaratilganda ham deyarli xotira yuklamasi hosil qilmaydi.

## Ishlash natijasi:
```text
Karta chizildi: [Yangiliklar] (Ajratilgan: true)
```


# 281-Topshiriq: Data Transfer Object (DTO) struct modeli
## Topshiriq sharti:
Serverdan keladigan xom ma'lumotlar strukturasini modellashtiring.

## Yechim (Swift kodi):
```swift
import Foundation

struct UserDTO: Decodable {
    let user_id: Int
    let display_name: String
}

let dto = UserDTO(user_id: 88, display_name: "Ali Valiyev")
print("DTO ID: \(dto.user_id), Nomi: \(dto.display_name)")
```

## Tushuntirish va Mantiq:
DTO lar tashqi API lar bilan ma'lumot almashish uchun maxsus mo'ljallangan yengil ma'lumot tuzilmalaridir.

## Ishlash natijasi:
```text
DTO ID: 88, Nomi: Ali Valiyev
```


# 282-Topshiriq: Domain Entity class modeli
## Topshiriq sharti:
O'z identifikatoriga va murakkab xatti-harakatlarga ega bo'lgan domena ob'ekti.

## Yechim (Swift kodi):
```swift
import Foundation

class BankAccountEntity {
    let accountNumber: String
    private(set) var balance: Double
    
    init(accountNumber: String, initialBalance: Double) {
        self.accountNumber = accountNumber
        self.balance = initialBalance
    }
    
    func deposit(amount: Double) {
        guard amount > 0 else { return }
        balance += amount
    }
}

let entity = BankAccountEntity(accountNumber: "UZ998001", initialBalance: 500.0)
entity.deposit(amount: 250.0)
print("Hisob: \(entity.accountNumber), Balans: $\(entity.balance)")
```

## Tushuntirish va Mantiq:
Domain Entity o'zining yagona identifikatori (accountNumber) va himoyalangan ichki holati bilan biznes qoidalarini ta'minlaydi.

## Ishlash natijasi:
```text
Hisob: UZ998001, Balans: $750.0
```


# 283-Topshiriq: Xotira hajmini o'lchash: MemoryLayout
## Topshiriq sharti:
Struct xotirada qancha bayt egallashini MemoryLayout orqali aniqlang.

## Yechim (Swift kodi):
```swift
import Foundation

struct Point3D {
    let x: Double // 8 bayt
    let y: Double // 8 bayt
    let z: Double // 8 bayt
}

print("Point3D size: \(MemoryLayout<Point3D>.size) bayt")
print("Point3D stride: \(MemoryLayout<Point3D>.stride) bayt")
print("Point3D alignment: \(MemoryLayout<Point3D>.alignment) bayt")
```

## Tushuntirish va Mantiq:
'MemoryLayout<T>' yordamida har qanday struct ning stakdagi aniq xotira hajmi (size), qadam o'lchami (stride) va tekislanishini (alignment) ko'rish mumkin.

## Ishlash natijasi:
```text
Point3D size: 24 bayt
Point3D stride: 24 bayt
Point3D alignment: 8 bayt
```


# 284-Topshiriq: Static Dispatch vs Dynamic Dispatch
## Topshiriq sharti:
Struct metodlari to'g'ridan-to'g'ri chaqirilishini va class metodlari VTable orqali borishini tushuntiring.

## Yechim (Swift kodi):
```swift
import Foundation

struct FastMath {
    func square(_ n: Int) -> Int { n * n } // Static Dispatch (Direct Call)
}

class FlexibleMath {
    func square(_ n: Int) -> Int { n * n } // Dynamic Dispatch (VTable Call)
}

let fm = FastMath()
let lm = FlexibleMath()

print("Static: \(fm.square(5))")
print("Dynamic: \(lm.square(5))")
```

## Tushuntirish va Mantiq:
Struct metodlari kompilyatsiya vaqtida to'g'ridan-to'g'ri manzil bilan ulanadi (Static Dispatch), bu protsessor uchun eng tezkor chaqiruvdir. Class metodlari esa polimorfizm sababli jadval (VTable) orqali chaqiriladi.

## Ishlash natijasi:
```text
Static: 25
Dynamic: 25
```


# 285-Topshiriq: final kalit so'zi bilan Dynamic Dispatch ni tezlashtirish
## Topshiriq sharti:
Class metodiga 'final' qo'yib uni static chaqiruvga aylantiring.

## Yechim (Swift kodi):
```swift
import Foundation

class NetworkClient {
    final func ping() -> String {
        return "PONG"
    }
}

let client = NetworkClient()
print("Ping natijasi: \(client.ping())")
```

## Tushuntirish va Mantiq:
'final' kalit so'zi metodni override qilishni taqiqlaydi. Natijada kompilyator VTable o'rniga to'g'ridan-to'g'ri statik chaqiruv qo'yadi va tezlikni oshiradi.

## Ishlash natijasi:
```text
Ping natijasi: PONG
```


# 286-Topshiriq: O'lchov birliklarini struct orqali modellashtirish
## Topshiriq sharti:
Masofani metr va kilometrlarda xatosiz hisoblovchi struct tuzing.

## Yechim (Swift kodi):
```swift
import Foundation

struct Distance {
    let meters: Double
    
    var kilometers: Double { meters / 1000.0 }
    
    static func fromKilometers(_ km: Double) -> Distance {
        return Distance(meters: km * 1000.0)
    }
}

let dist = Distance.fromKilometers(42.195)
print("Metrlar: \(dist.meters) m, Kilometrlar: \(dist.kilometers) km")
```

## Tushuntirish va Mantiq:
Qiymat turlari orqali xavfsiz va aniq domen o'lchov birliklarini modellashtirish Swift-ning kuchli tomonidir.

## Ishlash natijasi:
```text
Metrlar: 42195.0 m, Kilometrlar: 42.195 km
```


# 287-Topshiriq: Apparat resurslarini boshqarishda Class
## Topshiriq sharti:
Fayl deskriptorini xavfsiz ochib-yopuvchi boshqaruvchi sinf.

## Yechim (Swift kodi):
```swift
import Foundation

class FileHandler {
    let path: String
    init(path: String) {
        self.path = path
        print("Fayl deskriptori ochildi: \(path)")
    }
    deinit {
        print("Fayl deskriptori yopildi: \(path)")
    }
}

do {
    let _ = FileHandler(path: "/var/log/sys.log")
}
```

## Tushuntirish va Mantiq:
Apparat va tizim resurslari (fayllar, soketlar) yagona hayotiy tsiklga ega bo'lganligi sababli ularni doimo sinflar boshqaradi.

## Ishlash natijasi:
```text
Fayl deskriptori ochildi: /var/log/sys.log
Fayl deskriptori yopildi: /var/log/sys.log
```


# 288-Topshiriq: Struct larda polimorfizmni protokol orqali amalga oshirish
## Topshiriq sharti:
Merosxo'rliksiz, protokol yordamida polimorfik kolleksiya hosil qiling.

## Yechim (Swift kodi):
```swift
import Foundation

protocol Drawable {
    func draw()
}

struct Circle: Drawable {
    func draw() { print("Doira chizildi") }
}

struct Square: Drawable {
    func draw() { print("Kvadrat chizildi") }
}

let shapes: [Drawable] = [Circle(), Square()]
for shape in shapes {
    shape.draw()
}
```

## Tushuntirish va Mantiq:
Swift-da sinflar ierarxiyasi o'rniga 'Protocol-Oriented Programming' (POP) qo'llaniladi, bu struct lar bilan to'liq polimorfizm beradi.

## Ishlash natijasi:
```text
Doira chizildi
Kvadrat chizildi
```


# 289-Topshiriq: Qiymat semantikasiga ega daraxt (Value-semantic Tree)
## Topshiriq sharti:
Nusxalanganida butun daraxt ajralib chiqadigan qiymatli binar daraxt.

## Yechim (Swift kodi):
```swift
import Foundation

struct BinaryNode {
    var value: Int
    var left: [BinaryNode] = [] // Struct rekursiyasida massiv qutisi ishlatiladi
    var right: [BinaryNode] = []
}

var tree1 = BinaryNode(value: 10)
tree1.left.append(BinaryNode(value: 5))

var tree2 = tree1
tree2.value = 99

print("Tree 1 ildiz: \(tree1.value)")
print("Tree 2 ildiz: \(tree2.value)")
```

## Tushuntirish va Mantiq:
Qiymat semantikasiga ega murakkab tuzilmalar to'liq xavfsiz va boshqa qismlarga bog'liq bo'lmagan mustaqil daraxtlar hosil qiladi.

## Ishlash natijasi:
```text
Tree 1 ildiz: 10
Tree 2 ildiz: 99
```


# 290-Topshiriq: Zanjirli o'zgarishlar: mutating metodlar zanjiri
## Topshiriq sharti:
O'zini qaytaruvchi mutating metodlar orqali struct qiymatini bosqichma-bosqich o'zgartiring.

## Yechim (Swift kodi):
```swift
import Foundation

struct PathBuilder {
    private(set) var path: String = ""
    
    mutating func addSegment(_ segment: String) -> PathBuilder {
        path += "/" + segment
        return self
    }
}

var builder = PathBuilder()
_ = builder.addSegment("api").addSegment("v1").addSegment("users")
print("Marshrut: \(builder.path)")
```

## Tushuntirish va Mantiq:
Mutating metodlar o'zgaruvchan qiymat ustida qulay zanjirli konfiguratsiyalarni bajarish imkonini beradi.

## Ishlash natijasi:
```text
Marshrut: /api/v1/users
```


# 291-Topshiriq: Class nusxasini taqqoslash: ObjectIdentifier
## Topshiriq sharti:
Obyektning xotira manziliga asoslangan unikal identifikatorini oling.

## Yechim (Swift kodi):
```swift
import Foundation

class Node {
    let name: String
    init(name: String) { self.name = name }
}

let n1 = Node(name: "A")
let n2 = n1
let n3 = Node(name: "A")

print("n1 id == n2 id: \(ObjectIdentifier(n1) == ObjectIdentifier(n2))")
print("n1 id == n3 id: \(ObjectIdentifier(n1) == ObjectIdentifier(n3))")
```

## Tushuntirish va Mantiq:
'ObjectIdentifier' klass instansiyasining xotiradagi unikal manzilini o'zgarmas identifikator sifatida qaytaradi.

## Ishlash natijasi:
```text
n1 id == n2 id: true
n1 id == n3 id: false
```


# 292-Topshiriq: Struct larda avtomatik Hashable sintezi
## Topshiriq sharti:
Struct elementlarini Set yoki Dictionary kaliti sifatida ishlatish.

## Yechim (Swift kodi):
```swift
import Foundation

struct Coordinate: Hashable {
    let x: Int
    let y: Int
}

var visitedPoints: Set<Coordinate> = []
visitedPoints.insert(Coordinate(x: 0, y: 0))
visitedPoints.insert(Coordinate(x: 1, y: 2))
visitedPoints.insert(Coordinate(x: 0, y: 0)) // Takroriy qiymat

print("Unikal nuqtalar soni: \(visitedPoints.count)")
```

## Tushuntirish va Mantiq:
Barcha maydonlari Hashable bo'lgan struct lar uchun Swift kompilyatori 'hash(into:)' va '==' metodlarini to'liq avtomatik yaratadi.

## Ishlash natijasi:
```text
Unikal nuqtalar soni: 2
```


# 293-Topshiriq: Holat mashinasi (State Machine) struct yordamida
## Topshiriq sharti:
Tizimning holatlarini xavfsiz boshqaruvchi va noqonuniy o'tishlarga yo'l qo'ymaydigan struktura.

## Yechim (Swift kodi):
```swift
import Foundation

enum MachineState {
    case idle
    case working
    case stopped
}

struct StateMachine {
    private(set) var currentState: MachineState = .idle
    
    mutating func start() {
        if currentState == .idle {
            currentState = .working
            print("Mashina ishga tushirildi.")
        }
    }
    
    mutating func stop() {
        currentState = .stopped
        print("Mashina to'xtatildi.")
    }
}

var sm = StateMachine()
sm.start()
sm.stop()
```

## Tushuntirish va Mantiq:
Qiymat turidagi holat mashinalari tizimni har doim qat'iy bashorat qilinadigan holatda ushlab turadi.

## Ishlash natijasi:
```text
Mashina ishga tushirildi.
Mashina to'xtatildi.
```


# 294-Topshiriq: Aliasing Bug muammosi va uning struct larda yo'qligi
## Topshiriq sharti:
Class larda yuzaga keladigan ko'zga ko'rinmas o'zaro o'zgartirish muammosini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class SharedConfig {
    var maxTimeout = 30
}

func updateServiceA(config: SharedConfig) {
    config.maxTimeout = 60
}

let cfg = SharedConfig()
print("Dastlabki timeout: \(cfg.maxTimeout)")
updateServiceA(config: cfg)
print("Service A yangilagandan keyingi umumiy timeout: \(cfg.maxTimeout)")
```

## Tushuntirish va Mantiq:
Sinflarda bir joydagi o'zgarish unga bog'langan barcha boshqa joylarga kutilmaganda ta'sir o'tkazadi (Aliasing Bug). Struct larda esa bu muammo ildizi bilan yo'q qilingan.

## Ishlash natijasi:
```text
Dastlabki timeout: 30
Service A yangilagandan keyingi umumiy timeout: 60
```


# 295-Topshiriq: Kompilyatsiya vaqtida struct xotirasini tejash
## Topshiriq sharti:
Maydonlar tartibining struct xotira tekislanishiga (alignment) ta'siri.

## Yechim (Swift kodi):
```swift
import Foundation

struct OptimizedStruct {
    let a: Int64  // 8 bayt
    let b: Int32  // 4 bayt
    let c: Bool   // 1 bayt (+3 bayt padding = 8 bayt)
}

print("Optimallashtirilgan hajm: \(MemoryLayout<OptimizedStruct>.size) bayt")
```

## Tushuntirish va Mantiq:
Xotira tekislanishi (Memory Alignment) sababli kattaroq turlarni boshiga qo'yish padding (bo'shliq) xarajatlarini kamaytiradi.

## Ishlash natijasi:
```text
Optimallashtirilgan hajm: 13 bayt
```


# 296-Topshiriq: Class ichida shaxsiy o'zgartirish (private(set))
## Topshiriq sharti:
Xususiyatni tashqaridan faqat o'qiladigan, ammo sinf ichidan o'zgartiriladigan qilib cheklang.

## Yechim (Swift kodi):
```swift
import Foundation

class ScoreTracker {
    private(set) var currentScore: Int = 0
    
    func addPoints(_ p: Int) {
        guard p > 0 else { return }
        currentScore += p
    }
}

let tracker = ScoreTracker()
tracker.addPoints(50)
print("Ball: \(tracker.currentScore)")
// tracker.currentScore = 100 // Xato! Tashqaridan to'g'ridan-to'g'ri o'zgartirish taqiqlangan
```

## Tushuntirish va Mantiq:
'private(set)' maydonni tashqi dunyoga o'qish uchun ochiq (public read), ammo o'zgartirish uchun faqat sinf ichiga yopiq (private write) qiladi.

## Ishlash natijasi:
```text
Ball: 50
```


# 297-Topshiriq: Sinf metodini dinamik chaqiruvdan xoli qilish: @objc dynamic
## Topshiriq sharti:
Objective-C runtime orqali chaqiriladigan dinamik metod e'lon qiling.

## Yechim (Swift kodi):
```swift
import Foundation

class DynamicSpeaker: NSObject {
    @objc dynamic func speak() {
        print("Objective-C xabar yuborish tizimi orqali chaqirildi.")
    }
}

let sp = DynamicSpeaker()
sp.speak()
```

## Tushuntirish va Mantiq:
'@objc dynamic' Swift sinfiga Objective-C runtime ning dinamik xabar yuborish (Message Passing) mexanizmini bog'laydi.

## Ishlash natijasi:
```text
Objective-C xabar yuborish tizimi orqali chaqirildi.
```


# 298-Topshiriq: Struct yordamida konfiguratsiya ob'ektini klonlash va o'zgartirish
## Topshiriq sharti:
Mavjud struct nusxasini olib, uning faqat bitta maydonini yangilab yangi nusxa qaytaruvchi metod yozing.

## Yechim (Swift kodi):
```swift
import Foundation

struct ServerConfig {
    let host: String
    let port: Int
    let useSSL: Bool
    
    func withPort(_ newPort: Int) -> ServerConfig {
        return ServerConfig(host: self.host, port: newPort, useSSL: self.useSSL)
    }
}

let base = ServerConfig(host: "khorazmiy.uz", port: 80, useSSL: false)
let secure = base.withPort(443)

print("Base port: \(base.port)")
print("Secure port: \(secure.port)")
```

## Tushuntirish va Mantiq:
Bu naqsh 'Wither pattern' deb ataladi va o'zgarmas modellarda yangi variantlar yaratishning eng toza usulidir.

## Ishlash natijasi:
```text
Base port: 80
Secure port: 443
```


# 299-Topshiriq: Sinflarning xotirada saqlanish ierarxiyasi (Class Metadata)
## Topshiriq sharti:
Class instansiyasining o'zida 'isa' ko'rsatkichi va xususiyatlar joylashuvini tushuntiring.

## Yechim (Swift kodi):
```swift
import Foundation

class SimpleClass {
    var id: Int = 1
}

let sc = SimpleClass()
print("Class havola turi sifatida Heap xotirasida saqlanadi, uning ko'rsatkichi esa stakda joylashadi.")
```

## Tushuntirish va Mantiq:
Har bir sinf nusxasi Heap xotirada o'zining 'isa' (klass metadata ko'rsatkichi), havola hisoblagichi (retain count) va o'zgaruvchilarini saqlaydi.

## Ishlash natijasi:
```text
Class havola turi sifatida Heap xotirasida saqlanadi, uning ko'rsatkichi esa stakda joylashadi.
```


# 300-Topshiriq: Amaliy loyiha: Bank hisob raqamlari tizimi (Struct va Class birgalikda)
## Topshiriq sharti:
Tranzaksiyalarni (Struct - o'zgarmas qiymat) va Mijoz hisobini (Class - umumiy holat) birlashtiruvchi to'liq bank arxitekturasi moduli.

## Yechim (Swift kodi):
```swift
import Foundation

struct TransactionRecord: CustomStringConvertible {
    let id: UUID
    let type: String
    let amount: Double
    let date: Date
    
    var description: String {
        return "[\(type)] $\(amount) (\(id.uuidString.prefix(6))...)"
    }
}

class BankAccount {
    let accountHolder: String
    private(set) var balance: Double = 0.0
    private(set) var history: [TransactionRecord] = []
    
    init(holder: String, openingBalance: Double) {
        self.accountHolder = holder
        self.balance = openingBalance
        if openingBalance > 0 {
            addRecord(type: "BOSHLANG'ICH_DEPOZIT", amount: openingBalance)
        }
    }
    
    func deposit(amount: Double) {
        guard amount > 0 else { return }
        balance += amount
        addRecord(type: "KIRIM", amount: amount)
    }
    
    func withdraw(amount: Double) -> Bool {
        guard amount > 0 && amount <= balance else { return false }
        balance -= amount
        addRecord(type: "CHIQIM", amount: amount)
        return true
    }
    
    private func addRecord(type: String, amount: Double) {
        let tx = TransactionRecord(id: UUID(), type: type, amount: amount, date: Date())
        history.append(tx)
    }
}

let account = BankAccount(holder: "Rustam Qosimov", openingBalance: 1000.0)
account.deposit(amount: 500.0)
let success = account.withdraw(amount: 200.0)

print("Mijoz: \(account.accountHolder)")
print("Joriy balans: $\(account.balance)")
print("Operatsiya muvaffaqiyatlimi? \(success)")
print("Tranzaksiyalar soni: \(account.history.count)")
for tx in account.history {
    print("- \(tx)")
}
```

## Tushuntirish va Mantiq:
Ushbu loyihada Value semantikasi (o'zgarmas tranzaksiyalar tarixi) va Reference semantikasi (jonli hisob balansi va shaxsiy holat) optimal uyg'unlashtirildi.

## Ishlash natijasi:
```text
Mijoz: Rustam Qosimov
Joriy balans: $1300.0
Operatsiya muvaffaqiyatlimi? true
Tranzaksiyalar soni: 3
- [BOSHLANG'ICH_DEPOZIT] $1000.0 (UUID...)
- [KIRIM] $500.0 (UUID...)
- [CHIQIM] $200.0 (UUID...)
```

