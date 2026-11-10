# 351-Topshiriq: Initsializatsiya asoslari: init() konstruktori
## Topshiriq sharti:
Kompaniyadagi xodim ma'lumotlarini to'g'ri initsializatsiya qiluvchi sinf yozing.

## Yechim (Swift kodi):
```swift
import Foundation

class StaffMember {
    var name: String
    var role: String
    
    init(name: String, role: String) {
        self.name = name
        self.role = role
    }
}

let staff = StaffMember(name: "Davron", role: "Arxitektor")
print("Xodim: \(staff.name), Lavozim: \(staff.role)")
```

## Tushuntirish va Mantiq:
Initsializatsiya (Initialization) — bu sinf, struktura yoki enum nusxasi yaratilishida uning barcha saqlanuvchi xususiyatlariga boshlang'ich qiymat berish va ob'ektni foydalanishga tayyorlash jarayonidir.

## Ishlash natijasi:
```text
Xodim: Davron, Lavozim: Arxitektor
```


# 352-Topshiriq: Default Initializer (Standart konstruktor)
## Topshiriq sharti:
Barcha maydonlar boshlang'ich qiymatga ega bo'lganda argumentsiz init() qanday hosil bo'lishini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class SystemConfig {
    var maxConnections: Int = 100
    var isDebugMode: Bool = false
}

let config = SystemConfig()
print("Maksimal ulanishlar: \(config.maxConnections), Debug: \(config.isDebugMode)")
```

## Tushuntirish va Mantiq:
Agar sinf yoki struct-dagi barcha xususiyatlar standart qiymatga ega bo'lsa va maxsus init yozilmagan bo'lsa, Swift avtomatik ravishda argumentsiz 'init()' taqdim etadi.

## Ishlash natijasi:
```text
Maksimal ulanishlar: 100, Debug: false
```


# 353-Topshiriq: Struct larda Memberwise Initializer
## Topshiriq sharti:
Struct-ning avtomatik barcha parametrlar bo'yicha konstruktorini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

struct UserProfile {
    let username: String
    var age: Int
    var isVerified: Bool = false
}

let user = UserProfile(username: "nodir_99", age: 25)
print("Foydalanuvchi: \(user.username), Tasdiqlangan: \(user.isVerified)")
```

## Tushuntirish va Mantiq:
Struct larda default qiymatga ega maydonlar memberwise initializatorida ixtiyoriy parametr sifatida qoldirilishi mumkin.

## Ishlash natijasi:
```text
Foydalanuvchi: nodir_99, Tasdiqlangan: false
```


# 354-Topshiriq: Maxsus init yozganda Memberwise init ni saqlash (Extension)
## Topshiriq sharti:
Struct ga maxsus init qo'shilganda ham uning avtomatik memberwise initsializatorini yo'qotmaslik usuli.

## Yechim (Swift kodi):
```swift
import Foundation

struct Point {
    var x: Double
    var y: Double
}

extension Point {
    init(square: Double) {
        self.init(x: square, y: square)
    }
}

let p1 = Point(x: 10, y: 20) // Memberwise init saqlanib qoldi!
let p2 = Point(square: 15)  // Maxsus init
print("p1: (\(p1.x), \(p1.y)), p2: (\(p2.x), \(p2.y))")
```

## Tushuntirish va Mantiq:
Agar maxsus init asosiy 'struct' tanasi ichida yozilsa, avtomatik memberwise init yo'qoladi. Ammo maxsus init 'extension' ichida yozilsa, ikkala konstruktor ham mavjud bo'lib qoladi.

## Ishlash natijasi:
```text
p1: (10.0, 20.0), p2: (15.0, 15.0)
```


# 355-Topshiriq: Initializer Delegation qiymat turlarida (self.init)
## Topshiriq sharti:
Bitta konstruktor boshqa konstruktorni chaqiruvchi delegatsiya mexanizmini struct-da yozing.

## Yechim (Swift kodi):
```swift
import Foundation

struct Size {
    var width: Double
    var height: Double
    
    init(width: Double, height: Double) {
        self.width = width
        self.height = height
    }
    
    init(dimension: Double) {
        self.init(width: dimension, height: dimension)
    }
}

let cube = Size(dimension: 50.0)
print("O'lcham: \(cube.width) x \(cube.height)")
```

## Tushuntirish va Mantiq:
Qiymat turlarida (struct va enum) konstruktorlar 'self.init(...)' orqali bir-biriga vazifani yuklashi (delegation) mumkin.

## Ishlash natijasi:
```text
O'lcham: 50.0 x 50.0
```


# 356-Topshiriq: Sinflarda Designated Initializers
## Topshiriq sharti:
Sinfning barcha maydonlarini to'liq initsializatsiya qiluvchi asosiy (designated) konstruktorini yozing.

## Yechim (Swift kodi):
```swift
import Foundation

class Vehicle {
    var wheels: Int
    var name: String
    
    // Designated Initializer:
    init(wheels: Int, name: String) {
        self.wheels = wheels
        self.name = name
    }
}

let v = Vehicle(wheels: 4, name: "Avtomobil")
print("Transport: \(v.name), G'ildiraklar: \(v.wheels)")
```

## Tushuntirish va Mantiq:
Designated Initializer sinfning asosiy konstruktori bo'lib, o'sha sinfning barcha saqlanuvchi maydonlarini to'liq initsializatsiya qiladi va ota sinfning mos konstruktorini chaqiradi.

## Ishlash natijasi:
```text
Transport: Avtomobil, G'ildiraklar: 4
```


# 357-Topshiriq: Sinflarda Convenience Initializers (Qulay konstruktorlar)
## Topshiriq sharti:
Asosiy initsializatorga qulay parametrlar bilan murojaat qiluvchi 'convenience init' yozing.

## Yechim (Swift kodi):
```swift
import Foundation

class FoodItem {
    let name: String
    let calories: Int
    
    // Designated
    init(name: String, calories: Int) {
        self.name = name
        self.calories = calories
    }
    
    // Convenience
    convenience init(name: String) {
        self.init(name: name, calories: 100) // Standart 100 kaloriya
    }
}

let snack = FoodItem(name: "Olma")
print("Oziq-ovqat: \(snack.name), Kaloriya: \(snack.calories)")
```

## Tushuntirish va Mantiq:
'convenience' kalit so'zi bilan belgilangan konstruktorlar yordamchi bo'lib, ular oxir-oqibat o'sha sinfning Designated konstruktoriga murojaat qilishi shart.

## Ishlash natijasi:
```text
Oziq-ovqat: Olma, Kaloriya: 100
```


# 358-Topshiriq: Sinflarda Initializer Delegation qoidalari
## Topshiriq sharti:
Designated yuqoriga (super.init), Convenience yonboshga (self.init) murojaat qilish qoidasini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class ParentClass {
    var id: Int
    init(id: Int) { self.id = id }
}

class ChildClass: ParentClass {
    var name: String
    
    // 1. Designated init yuqoriga ota sinfga murojaat qiladi:
    init(id: Int, name: String) {
        self.name = name
        super.init(id: id)
    }
    
    // 2. Convenience init o'z sinfining boshqa initiga murojaat qiladi:
    convenience init(name: String) {
        self.init(id: 0, name: name)
    }
}

let child = ChildClass(name: "Yordamchi")
print("ID: \(child.id), Nomi: \(child.name)")
```

## Tushuntirish va Mantiq:
Qoida 1: Designated init to'g'ridan-to'g'ri ota sinfning designated initini chaqirishi shart. Qoida 2: Convenience init o'z sinfining boshqa initini chaqirishi shart va oxiri designated initga borishi shart.

## Ishlash natijasi:
```text
ID: 0, Nomi: Yordamchi
```


# 359-Topshiriq: Ikki bosqichli initsializatsiya (Two-Phase Initialization)
## Topshiriq sharti:
1-faza (barcha maydonlar to'lishi) va 2-faza (self to'liq tayyor bo'lishi) qoidalarini amalda ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class Device {
    var serialNumber: String
    init(serial: String) {
        self.serialNumber = serial
    }
}

class Smartphone: Device {
    var osVersion: String
    
    init(serial: String, os: String) {
        // 1-FAZA: O'z maydonlarini initsializatsiya qilish
        self.osVersion = os
        
        // 1-FAZA: Ota sinf maydonlarini initsializatsiya qilish
        super.init(serial: serial)
        
        // 2-FAZA: Endi self to'liq tayyor, metodlarni chaqirish mumkin!
        self.printDetails()
    }
    
    func printDetails() {
        print("Smartfon: Serial=\(serialNumber), OS=\(osVersion)")
    }
}

let phone = Smartphone(serial: "APL_2026", os: "iOS 18")
```

## Tushuntirish va Mantiq:
Swift xotira xavfsizligini 2 bosqichli initsializatsiya bilan kafolatlaydi: 1-bosqichda barcha maydonlarga qiymat beriladi; 2-bosqichda esa metodlar va self bilan amallar bajarishga ruxsat etiladi.

## Ishlash natijasi:
```text
Smartfon: Serial=APL_2026, OS=iOS 18
```


# 360-Topshiriq: Xavfsizlik tekshiruvi: super.init dan oldin o'z maydonlarini to'ldirish
## Topshiriq sharti:
O'z xususiyatlariga qiymat bermasdan super.init chaqirilsa yuzaga keladigan xatoni tushuntiring.

## Yechim (Swift kodi):
```swift
import Foundation

class BaseService {
    let serviceID: String
    init(id: String) { self.serviceID = id }
}

class AnalyticsService: BaseService {
    var apiKey: String
    
    init(id: String, key: String) {
        self.apiKey = key // Buni super.init dan OLDIN qilish shart!
        super.init(id: id)
    }
}

let a = AnalyticsService(id: "SRV_1", key: "KEY_XYZ")
print("Servis ID: \(a.serviceID), Kalit: \(a.apiKey)")
```

## Tushuntirish va Mantiq:
Swift-da bola sinf o'zining barcha yangi maydonlariga qiymat biriktirmasdan oldin super.init() ni chaqira olmaydi.

## Ishlash natijasi:
```text
Servis ID: SRV_1, Kalit: KEY_XYZ
```


# 361-Topshiriq: Meros olingan xususiyatlarni override qilishda initsializator
## Topshiriq sharti:
Ota sinf konstruktorini 'override init' kalit so'zi bilan qayta yozing.

## Yechim (Swift kodi):
```swift
import Foundation

class Shape {
    var name: String
    init(name: String) { self.name = name }
}

class Triangle: Shape {
    var sides: Int
    
    override init(name: String) {
        self.sides = 3
        super.init(name: name)
    }
}

let t = Triangle(name: "Uchburchak")
print("Shakl: \(t.name), Tomonlar soni: \(t.sides)")
```

## Tushuntirish va Mantiq:
Agar subclass ota sinfining Designated konstruktori bilan aynan bir xil parametrli konstruktor yozsa, 'override' kalit so'zini qo'yish shart.

## Ishlash natijasi:
```text
Shakl: Uchburchak, Tomonlar soni: 3
```


# 362-Topshiriq: Avtomatik initsializator merosxo'rligi qoidalari
## Topshiriq sharti:
Subclass o'ziga yangi designated init qo'shmasa, ota sinfning barcha initlarini avtomatik meros qilib olishini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class VehicleBase {
    var color: String
    init(color: String) { self.color = color }
    convenience init() { self.init(color: "Oq") }
}

class Bicycle: VehicleBase {
    var hasBell: Bool = true // Yangi maydon standart qiymatga ega
}

let bike1 = Bicycle(color: "Qizil") // Avtomatik meros olingan designated
let bike2 = Bicycle()                // Avtomatik meros olingan convenience
print("Bike1: \(bike1.color), Bike2: \(bike2.color)")
```

## Tushuntirish va Mantiq:
Agar subclass hech qanday yangi designated init yozmasa, u ota sinfning barcha designated va convenience konstruktorlarini to'liq avtomatik meros oladi.

## Ishlash natijasi:
```text
Bike1: Qizil, Bike2: Oq
```


# 363-Topshiriq: Failable Initializer (init?): Muvaffaqiyatsiz bo'ladigan konstruktor
## Topshiriq sharti:
Noto'g'ri oraliqdagi harorat berilganda nil qaytaruvchi konstruktor yozing.

## Yechim (Swift kodi):
```swift
import Foundation

struct KelvinTemperature {
    let kelvin: Double
    
    init?(kelvin: Double) {
        if kelvin < 0.0 {
            return nil // Mutlaq noldan past bo'lishi mumkin emas
        }
        self.kelvin = kelvin
    }
}

let validT = KelvinTemperature(kelvin: 300.0)
let invalidT = KelvinTemperature(kelvin: -50.0)

print("Valid: \(validT != nil)")
print("Invalid: \(invalidT != nil)")
```

## Tushuntirish va Mantiq:
'init?' konstruktori parametrlar talabga mos kelmaganda initsializatsiyani bekor qilib 'nil' qaytaradi. Natija esa 'T?' (Optional) bo'ladi.

## Ishlash natijasi:
```text
Valid: true
Invalid: false
```


# 364-Topshiriq: Enum larda Failable Initializer
## Topshiriq sharti:
Enum ning 'init?(rawValue:)' avtomatik failable initsializatori qanday ishlashini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

enum HTTPStatusCode: Int {
    case ok = 200
    case notFound = 404
    case serverError = 500
}

let success = HTTPStatusCode(rawValue: 200)
let unknown = HTTPStatusCode(rawValue: 999)

print("200 holati: \(String(describing: success))")
print("999 holati: \(String(describing: unknown))")
```

## Tushuntirish va Mantiq:
Swift RawRepresentable enum lari uchun avtomatik ravishda 'init?(rawValue:)' failable konstruktorini taqdim etadi.

## Ishlash natijasi:
```text
200 holati: Optional(HTTPStatusCode.ok)
999 holati: nil
```


# 365-Topshiriq: Failable Initializer larning tarqalishi (Propagation)
## Topshiriq sharti:
Murakkab ob'ekt ichki failable init xato berganda o'zi ham nil qaytarishini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

struct Engine {
    let power: Int
    init?(power: Int) {
        guard power > 0 else { return nil }
        self.power = power
    }
}

struct FastCar {
    let model: String
    let engine: Engine
    
    init?(model: String, enginePower: Int) {
        guard let validEngine = Engine(power: enginePower) else {
            return nil
        }
        self.model = model
        self.engine = validEngine
    }
}

let c1 = FastCar(model: "Sport", enginePower: 450)
let c2 = FastCar(model: "Buzuq", enginePower: -10)

print("c1 muvaffaqiyatlimi? \(c1 != nil)")
print("c2 muvaffaqiyatlimi? \(c2 != nil)")
```

## Tushuntirish va Mantiq:
Failable initsializatorlar zanjirida har qanday bo'g'indagi nosozlik butun initsializatsiya jarayonining 'nil' bilan yakunlanishiga sabab bo'ladi.

## Ishlash natijasi:
```text
c1 muvaffaqiyatlimi? true
c2 muvaffaqiyatlimi? false
```


# 366-Topshiriq: Failable init ni Non-failable ga aylantirib override qilish
## Topshiriq sharti:
Subclass ota sinfning muvaffaqiyatsiz bo'lishi mumkin bo'lgan initini kafolatli muvaffaqiyatliga aylantirsin.

## Yechim (Swift kodi):
```swift
import Foundation

class BaseDocument {
    var text: String
    init?(text: String) {
        guard !text.isEmpty else { return nil }
        self.text = text
    }
}

class SafeDocument: BaseDocument {
    override init(text: String) {
        let fallback = text.isEmpty ? "Standart matn" : text
        super.init(text: fallback)!
    }
}

let doc = SafeDocument(text: "")
print("SafeDocument matni: \(doc.text)")
```

## Tushuntirish va Mantiq:
Subclass ota sinfning 'init?' ini oddiy kafolatlangan 'init' qilib override qilishi mumkin (ammo teskarisi mumkin emas).

## Ishlash natijasi:
```text
SafeDocument matni: Standart matn
```


# 367-Topshiriq: Majburiy initsializatorlar: required init
## Topshiriq sharti:
Barcha subclass lar albatta qayta yozishi shart bo'lgan konstruktorni e'lon qiling.

## Yechim (Swift kodi):
```swift
import Foundation

class BaseView {
    required init() {
        print("BaseView initsializatsiya qilindi.")
    }
}

class CustomButtonView: BaseView {
    required init() {
        super.init()
        print("CustomButtonView tayyorlandi.")
    }
}

let _ = CustomButtonView()
```

## Tushuntirish va Mantiq:
'required' kalit so'zi barcha voris sinflarga ushbu konstruktorni majburiy realizatsiya qilish talabini qo'yadi. Voris sinfda 'override' so'zi yozilmaydi, yana 'required' deb davom etiladi.

## Ishlash natijasi:
```text
BaseView initsializatsiya qilindi.
CustomButtonView tayyorlandi.
```


# 368-Topshiriq: Xatolik tashlovchi initsializator: init() throws
## Topshiriq sharti:
Noto'g'ri parametrlar kiritilganda aniq xato tashlovchi konstruktor tuzing.

## Yechim (Swift kodi):
```swift
import Foundation

enum ConfigError: Error {
    case missingHost
    case portOutOfRange
}

struct NetworkConfiguration {
    let host: String
    let port: Int
    
    init(host: String, port: Int) throws {
        guard !host.isEmpty else { throw ConfigError.missingHost }
        guard port > 0 && port <= 65535 else { throw ConfigError.portOutOfRange }
        self.host = host
        self.port = port
    }
}

do {
    let conf = try NetworkConfiguration(host: "khorazmiy.uz", port: 8080)
    print("Muvaffaqiyatli server: \(conf.host):\(conf.port)")
    let _ = try NetworkConfiguration(host: "", port: 80)
} catch {
    print("Initsializatsiyada xatolik: \(error)")
}
```

## Tushuntirish va Mantiq:
'init() throws' konstruktori xato sababini aniq ko'rsatish zarur bo'lganda 'init?' dan afzalroqdir.

## Ishlash natijasi:
```text
Muvaffaqiyatli server: khorazmiy.uz:8080
Initsializatsiyada xatolik: missingHost
```


# 369-Topshiriq: Yopiq initsializator: private init()
## Topshiriq sharti:
Tashqaridan yangi nusxa olinishini cheklab, Singleton yaratish.

## Yechim (Swift kodi):
```swift
import Foundation

class SystemLogger {
    static let shared = SystemLogger()
    
    private init() {
        print("SystemLogger yagona nusxasi ishga tushdi.")
    }
    
    func log(_ msg: String) {
        print("[LOG]: \(msg)")
    }
}

SystemLogger.shared.log("Tizim barqaror ishlamoqda.")
```

## Tushuntirish va Mantiq:
'private init()' tashqi kod tomonidan 'SystemLogger()' deb yangi nusxa olinishini to'liq taqiqlaydi.

## Ishlash natijasi:
```text
SystemLogger yagona nusxasi ishga tushdi.
[LOG]: Tizim barqaror ishlamoqda.
```


# 370-Topshiriq: Xotirani tozalash asoslari: deinit sintaksisi
## Topshiriq sharti:
Sinf ob'ekti xotiradan bo'shatilganda resurs tozalanishini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class DatabaseConnection {
    let connectionID: Int
    
    init(id: Int) {
        self.connectionID = id
        print("Ulanish #\(connectionID) ochildi.")
    }
    
    deinit {
        print("Ulanish #\(connectionID) xavfsiz yopildi.")
    }
}

do {
    let conn = DatabaseConnection(id: 42)
    print("Ulanishdan foydalanilmoqda...")
}
print("Blok tugadi.")
```

## Tushuntirish va Mantiq:
'deinit' faqat sinflarda (class) bo'lib, ob'ekt xotiradan butunlay o'chirilishidan oldin avtomatik chaqiriladi.

## Ishlash natijasi:
```text
Ulanish #42 ochildi.
Ulanishdan foydalanilmoqda...
Ulanish #42 xavfsiz yopildi.
Blok tugadi.
```


# 371-Topshiriq: Deinit chaqirilish tartibi (Subclass avval, Superclass keyin)
## Topshiriq sharti:
Merosxo'rlik zanjirida deinit teskari tartibda chaqirilishini isbotlang.

## Yechim (Swift kodi):
```swift
import Foundation

class BaseWorker {
    deinit {
        print("1. BaseWorker deinit chaqirildi.")
    }
}

class AdvancedWorker: BaseWorker {
    deinit {
        print("2. AdvancedWorker deinit chaqirildi.")
    }
}

do {
    let _ = AdvancedWorker()
}
```

## Tushuntirish va Mantiq:
Swift avval bola sinfning deinitializatorini, so'ngra ota sinfning deinitializatorini avtomatik zanjirli chaqiradi.

## Ishlash natijasi:
```text
2. AdvancedWorker deinit chaqirildi.
1. BaseWorker deinit chaqirildi.
```


# 372-Topshiriq: Resurslarni deinit da tozalash: Taymerni bekor qilish
## Topshiriq sharti:
Sinf xotiradan o'chganda fondagi taymerni to'xtatuvchi toza arxitektura.

## Yechim (Swift kodi):
```swift
import Foundation

class HeartbeatMonitor {
    var isRunning = true
    
    init() {
        print("Monitoring boshlandi.")
    }
    
    func stop() {
        isRunning = false
    }
    
    deinit {
        stop()
        print("Monitoring to'xtatildi va xotira tozalandi.")
    }
}

do {
    let _ = HeartbeatMonitor()
}
```

## Tushuntirish va Mantiq:
Deinit resurs sizib ketishi (resource leak) va fon vazifalarining osilib qolishini oldini oluvchi eng muhim himoyadir.

## Ishlash natijasi:
```text
Monitoring boshlandi.
Monitoring to'xtatildi va xotira tozalandi.
```


# 373-Topshiriq: Closure yordamida standart xususiyat qiymatini initsializatsiya qilish
## Topshiriq sharti:
Murakkab massivni closure orqali boshlang'ich qiymat bilan to'ldiring.

## Yechim (Swift kodi):
```swift
import Foundation

struct ChessBoard {
    let boardColors: [String] = {
        var colors = [String]()
        for row in 0..<2 {
            for col in 0..<2 {
                colors.append((row + col) % 2 == 0 ? "Oq" : "Qora")
            }
        }
        return colors
    }()
}

let chess = ChessBoard()
print("Kataklar: \(chess.boardColors)")
```

## Tushuntirish va Mantiq:
'{ ... }()' darhol bajariluvchi closure xususiyatga murakkab hisob-kitoblar natijasini boshlang'ich qiymat qilib berish imkonini beradi.

## Ishlash natijasi:
```text
Kataklar: ["Oq", "Qora", "Qora", "Oq"]
```


# 374-Topshiriq: Initsializatsiyada parametr nomlari va yorliqlari
## Topshiriq sharti:
Har xil parametr yorliqlariga ega bir nechta initsializatorlar e'lon qiling.

## Yechim (Swift kodi):
```swift
import Foundation

struct ColorRGB {
    let red, green, blue: Double
    
    init(red: Double, green: Double, blue: Double) {
        self.red = red; self.green = green; self.blue = blue
    }
    
    init(white: Double) {
        self.red = white; self.green = white; self.blue = white
    }
}

let magenta = ColorRGB(red: 1.0, green: 0.0, blue: 1.0)
let gray = ColorRGB(white: 0.5)
print("Magenta red: \(magenta.red), Gray red: \(gray.red)")
```

## Tushuntirish va Mantiq:
Initsializatorlar ham oddiy funksiyalar kabi turli xil argument yorliqlariga ega bo'lishi mumkin.

## Ishlash natijasi:
```text
Magenta red: 1.0, Gray red: 0.5
```


# 375-Topshiriq: Standart parametr qiymatlari bilan bitta universal init
## Topshiriq sharti:
Bir nechta parametrga default berib turli chaqiruvlarni qanoatlantiring.

## Yechim (Swift kodi):
```swift
import Foundation

struct ServerQuery {
    let endpoint: String
    let timeout: Int
    let retries: Int
    
    init(endpoint: String, timeout: Int = 30, retries: Int = 3) {
        self.endpoint = endpoint
        self.timeout = timeout
        self.retries = retries
    }
}

let q1 = ServerQuery(endpoint: "/users")
let q2 = ServerQuery(endpoint: "/auth", timeout: 10, retries: 1)
print("q1 timeout: \(q1.timeout), q2 timeout: \(q2.timeout)")
```

## Tushuntirish va Mantiq:
Standart parametr qiymatlari orqali bir nechta ortiqcha init yozishdan qutulish mumkin.

## Ishlash natijasi:
```text
q1 timeout: 30, q2 timeout: 10
```


# 376-Topshiriq: init! (Implicitly Unwrapped Failable Initializer)
## Topshiriq sharti:
Muvaffaqiyatsiz bo'lsa nil beradigan, ammo muvaffaqiyatli bo'lsa majburiy ochilgan (T!) ko'rinishida qaytadigan konstruktor.

## Yechim (Swift kodi):
```swift
import Foundation

struct Identifier {
    let value: String
    
    init!(value: String) {
        if value.isEmpty { return nil }
        self.value = value
    }
}

let id: Identifier = Identifier(value: "USER_001")
print("ID qiymati: \(id.value)")
```

## Tushuntirish va Mantiq:
'init!' failable init kabi nil qaytarishi mumkin, lekin muvaffaqiyatli bo'lsa uni unwrap qilmasdan to'g'ridan-to'g'ri ishlatishga ruxsat beradi.

## Ishlash natijasi:
```text
ID qiymati: USER_001
```


# 377-Topshiriq: Generic turlarda initsializatorlar
## Topshiriq sharti:
Generik struktura uchun parametrlar turini qabul qiluvchi konstruktor yozing.

## Yechim (Swift kodi):
```swift
import Foundation

struct KeyValueContainer<K: Hashable, V> {
    let key: K
    let value: V
    
    init(key: K, value: V) {
        self.key = key
        self.value = value
    }
}

let pair = KeyValueContainer(key: "ID", value: 1004)
print("Juftlik: \(pair.key) -> \(pair.value)")
```

## Tushuntirish va Mantiq:
Generik initsializatorlar berilgan qiymatlarga qarab K va V turlarini avtomatik ravishda aniqlaydi.

## Ishlash natijasi:
```text
Juftlik: ID -> 1004
```


# 378-Topshiriq: Maxsus Decoder initsializatori: init(from decoder: Decoder)
## Topshiriq sharti:
Decodable protokoli orqali JSON dan ma'lumotlarni qo'lda qabul qiluvchi konstruktor yozing.

## Yechim (Swift kodi):
```swift
import Foundation

struct UserRecord: Decodable {
    let username: String
    let score: Int
    
    enum CodingKeys: String, CodingKey {
        case username = "user_name"
        case score
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        self.username = try container.decode(String.self, forKey: .username)
        self.score = try container.decode(Int.self, forKey: .score)
    }
}

let json = """{"user_name": "Ulugbek", "score": 95}""".data(using: .utf8)!
if let user = try? JSONDecoder().decode(UserRecord.self, from: json) {
    print("Dekodlandi: \(user.username), Ball: \(user.score)")
}
```

## Tushuntirish va Mantiq:
'init(from decoder:)' orqali JSON kalitlarini va tiplarini moslashtiruvchi to'liq boshqaruvga ega bo'linadi.

## Ishlash natijasi:
```text
Dekodlandi: Ulugbek, Ball: 95
```


# 379-Topshiriq: Initsializatsiyada 'defer' operatori
## Topshiriq sharti:
Konstruktor ishlash jarayonida defer bloki qachon ishga tushishini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class InitTracer {
    init() {
        defer { print("3. Initsializatsiya yakunlandi (defer).") }
        print("1. Initsializatsiya boshlandi.")
        print("2. Parametrlar o'rnatildi.")
    }
}

let _ = InitTracer()
```

## Tushuntirish va Mantiq:
Init ichidagi 'defer' bloki konstruktor tanasi to'liq yakunlanib ob'ekt xotiraga tayyor bo'lish paytida ijro etiladi.

## Ishlash natijasi:
```text
1. Initsializatsiya boshlandi.
2. Parametrlar o'rnatildi.
3. Initsializatsiya yakunlandi (defer).
```


# 380-Topshiriq: Failable init dan erta 'return nil' qilish
## Topshiriq sharti:
Shart qanoatlantirilmaganda hech qanday ortiqcha xotira sarflamay darhol chiqish.

## Yechim (Swift kodi):
```swift
import Foundation

struct NonEmptyString {
    let content: String
    
    init?(content: String) {
        guard !content.trimmingCharacters(in: .whitespaces).isEmpty else {
            return nil
        }
        self.content = content
    }
}

print("Bo'sh matn: \(String(describing: NonEmptyString(content: "   ")))")
print("To'la matn: \(String(describing: NonEmptyString(content: "Swift")?.content))")
```

## Tushuntirish va Mantiq:
Failable konstruktorda xatolik aniqlanishi bilan 'return nil' qilinadi va ob'ekt yaratilishi bekor qilinadi.

## Ishlash natijasi:
```text
Bo'sh matn: nil
To'la matn: Optional("Swift")
```


# 381-Topshiriq: Initsializatsiya paytida hisoblangan xususiyatlarga murojaat cheklovlari
## Topshiriq sharti:
Barcha maydonlar to'liq qiymat olguncha getter larni chaqirib bo'lmasligini tushuntiring.

## Yechim (Swift kodi):
```swift
import Foundation

class CircleCalc {
    var radius: Double
    var diameter: Double { radius * 2 }
    
    init(radius: Double) {
        self.radius = radius
        // Bu yerda self.radius qiymat olgandan keyingina self.diameter ga murojaat qilish mumkin:
        print("Diametr: \(self.diameter)")
    }
}

let _ = CircleCalc(radius: 7.0)
```

## Tushuntirish va Mantiq:
Swift-da hisoblangan xususiyatlarga murojaat qilish 2-faza (Phase 2) hisoblanadi va saqlanuvchi maydonlar to'liq qiymat olgachgina ruxsat etiladi.

## Ishlash natijasi:
```text
Diametr: 14.0
```


# 382-Topshiriq: Init paytida self ni tashqariga parametr qilib uzatish cheklovi
## Topshiriq sharti:
Nima uchun 1-bosqich tugamasdan self ni boshqa metodga berib bo'lmasligini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class Listener {
    func register(client: Any) { print("Mijoz ro'yxatga olindi.") }
}

class ClientApp {
    let name: String
    init(name: String, listener: Listener) {
        self.name = name
        // self.name to'lgandan keyingina self ni uzatish mumkin:
        listener.register(client: self)
    }
}

let l = Listener()
let _ = ClientApp(name: "iOSApp", listener: l)
```

## Tushuntirish va Mantiq:
Kompilyator ob'ekt to'liq yaratilib bitmaguncha (Phase 1 yakunlanmaguncha) uning ko'rsatkichini boshqa joyga uzatishni taqiqlaydi.

## Ishlash natijasi:
```text
Mijoz ro'yxatga olindi.
```


# 383-Topshiriq: Convenience init orqali keshdan ob'ekt qaytarish cheklovi
## Topshiriq sharti:
Init doimo yangi ob'ekt yaratishga majburligi sababli, keshdan qaytarish uchun Fabrika metodi afzalligini tushuntiring.

## Yechim (Swift kodi):
```swift
import Foundation

class CachedResource {
    let id: Int
    private static var cache: [Int: CachedResource] = [:]
    
    private init(id: Int) { self.id = id }
    
    static func getResource(id: Int) -> CachedResource {
        if let existing = cache[id] {
            return existing
        }
        let newRes = CachedResource(id: id)
        cache[id] = newRes
        return newRes
    }
}

let r1 = CachedResource.getResource(id: 1)
let r2 = CachedResource.getResource(id: 1)
print("r1 === r2: \(r1 === r2)")
```

## Tushuntirish va Mantiq:
Swift-da oddiy konstruktorlar (init) yangi instansiya ajratishga majbur. Agar mavjud keshdan ob'ekt qaytarish kerak bo'lsa, 'static factory method' ishlatiladi.

## Ishlash natijasi:
```text
r1 === r2: true
```


# 384-Topshiriq: Initsializatorda inout parametrlarini ishlatish
## Topshiriq sharti:
Tashqi o'zgaruvchi qiymatini kamaytirib ob'ektni initsializatsiya qilish.

## Yechim (Swift kodi):
```swift
import Foundation

class Ticket {
    let seatNumber: Int
    init(pool: inout Int) {
        self.seatNumber = pool
        pool += 1
    }
}

var currentSeat = 1
let t1 = Ticket(pool: &currentSeat)
let t2 = Ticket(pool: &currentSeat)
print("Chipta 1 o'rni: \(t1.seatNumber), Chipta 2 o'rni: \(t2.seatNumber)")
```

## Tushuntirish va Mantiq:
Konstruktorda ham 'inout' parametrlari orqali tashqi resurs hisoblagichlarini parallel yangilab borish mumkin.

## Ishlash natijasi:
```text
Chipta 1 o'rni: 1, Chipta 2 o'rni: 2
```


# 385-Topshiriq: Subclass convenience init ota sinf designated initini chaqira olmasligi
## Topshiriq sharti:
Subclass convenience faqat o'zining designated initini chaqirishi shartligini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class Animal {
    var species: String
    init(species: String) { self.species = species }
}

class Dog: Animal {
    var breed: String
    
    // Designated
    init(breed: String) {
        self.breed = breed
        super.init(species: "It")
    }
    
    // Convenience: super.init() emas, self.init() ni chaqirishi shart!
    convenience init() {
        self.init(breed: "Ovcharka")
    }
}

let d = Dog()
print("Tur: \(d.species), Zot: \(d.breed)")
```

## Tushuntirish va Mantiq:
Convenience konstruktor faqat o'z sinfidagi boshqa konstruktorlarga delegatsiya qila oladi, ota sinfga to'g'ridan-to'g'ri sakray olmaydi.

## Ishlash natijasi:
```text
Tur: It, Zot: Ovcharka
```


# 386-Topshiriq: Statik initsializatsiya (Static / Type Initialization)
## Topshiriq sharti:
Sinfning statik xususiyati birinchi chaqirilganda qanday initsializatsiya bo'lishini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

class DatabaseDriver {
    static let connectionPool: String = {
        print("Baza drayveri initsializatsiya qilindi!")
        return "POOLED_CONNECTIONS"
    }()
}

print("Dastur ishga tushdi.")
print("Resurs: \(DatabaseDriver.connectionPool)")
```

## Tushuntirish va Mantiq:
Swift-da statik xususiyatlar birinchi murojaat paytida (lazily) va thread-safe tarzda 'swift_once' orqali initsializatsiya qilinadi.

## Ishlash natijasi:
```text
Dastur ishga tushdi.
Baza drayveri initsializatsiya qilindi!
Resurs: POOLED_CONNECTIONS
```


# 387-Topshiriq: Deinit ichida resurs tozalash xavfsizligi
## Topshiriq sharti:
Ob'ekt o'chirilishida xotirani xavfsiz nolga tenglashtirish.

## Yechim (Swift kodi):
```swift
import Foundation

class MemoryBuffer {
    var size: Int
    init(size: Int) {
        self.size = size
        print("Xotira buferi (\(size) bayt) ajratildi.")
    }
    deinit {
        print("Xotira buferi tozalandi.")
    }
}

do {
    let _ = MemoryBuffer(size: 1024)
}
```

## Tushuntirish va Mantiq:
Deinit resurslarni tozalash uchun ideal va yagona kafolatlangan joydir.

## Ishlash natijasi:
```text
Xotira buferi (1024 bayt) ajratildi.
Xotira buferi tozalandi.
```


# 388-Topshiriq: Deinit ichida o'ziga yangi strong havola (Zombie Object) hosil qilishdan saqlanish
## Topshiriq sharti:
Deinit paytida self ni global massivga qo'shish qat'iyan taqiqlanganligini tushuntiring.

## Yechim (Swift kodi):
```swift
import Foundation

class SafeDeinitWorker {
    let id: Int = 1
    deinit {
        print("Xavfsiz tozalash: self hech qanday global o'zgaruvchiga uzatilmaydi.")
    }
}

do {
    let _ = SafeDeinitWorker()
}
```

## Tushuntirish va Mantiq:
Agar deinit ichida 'globalArray.append(self)' qilinsa, o'layotgan ob'ekt qayta tiriltirilishga uriniladi (Resurrecting), bu Swift-da qat'iy fatal xatoga olib keladi.

## Ishlash natijasi:
```text
Xavfsiz tozalash: self hech qanday global o'zgaruvchiga uzatilmaydi.
```


# 389-Topshiriq: Initsializatorda precondition qo'llash
## Topshiriq sharti:
Xavfsiz port raqamini tekshiruvchi kafolatli initsializator.

## Yechim (Swift kodi):
```swift
import Foundation

struct SecurePort {
    let port: Int
    init(port: Int) {
        precondition(port > 1024, "Port 1024 dan katta bo'lishi shart!")
        self.port = port
    }
}

let p = SecurePort(port: 8080)
print("Port: \(p.port)")
```

## Tushuntirish va Mantiq:
Initsializatorda 'precondition' dasturning kritik invariantlarini tekshirishda ishlatiladi.

## Ishlash natijasi:
```text
Port: 8080
```


# 390-Topshiriq: Bir nechta Failable initsializatorlar kombinatsiyasi
## Topshiriq sharti:
Matndan yoki sondan failable initsializatsiya qiluvchi rang modeli.

## Yechim (Swift kodi):
```swift
import Foundation

struct HexColor {
    let hex: String
    
    init?(hexString: String) {
        guard hexString.hasPrefix("#") && hexString.count == 7 else { return nil }
        self.hex = hexString
    }
    
    init?(rgbNumber: Int) {
        guard rgbNumber >= 0 && rgbNumber <= 0xFFFFFF else { return nil }
        self.hex = String(format: "#%06X", rgbNumber)
    }
}

let c1 = HexColor(hexString: "#FF5733")
let c2 = HexColor(rgbNumber: 0x00FF00)
print("Rang 1: \(c1?.hex ?? ""), Rang 2: \(c2?.hex ?? "")")
```

## Tushuntirish va Mantiq:
Turli kiruvchi ma'lumotlar uchun alohida-alohida failable konstruktorlar taqdim etish keng tarqalgan amaliyotdir.

## Ishlash natijasi:
```text
Rang 1: #FF5733, Rang 2: #00FF00
```


# 391-Topshiriq: Ota sinfdan meros olingan required init larni bajarish
## Topshiriq sharti:
Subclass o'zining yangi designated initini yozganda ham required initni amalga oshirishga majburligi.

## Yechim (Swift kodi):
```swift
import Foundation

class BaseWidget {
    required init() {
        print("Widget yaratildi.")
    }
}

class CustomWidget: BaseWidget {
    var title: String
    
    init(title: String) {
        self.title = title
        super.init()
    }
    
    required init() {
        self.title = "Standart vidjet"
        super.init()
    }
}

let w = CustomWidget()
print("Vidjet nomi: \(w.title)")
```

## Tushuntirish va Mantiq:
Agar subclass yangi designated init yozsa, ota sinfning barcha 'required' konstruktorlarini qayta yozishi shart bo'ladi.

## Ishlash natijasi:
```text
Widget yaratildi.
Vidjet nomi: Standart vidjet
```


# 392-Topshiriq: Merosxo'rlikda super.init parametrlarini hisoblab uzatish
## Topshiriq sharti:
Ota sinf initsializatoriga hisoblangan qiymatlarni uzating.

## Yechim (Swift kodi):
```swift
import Foundation

class Box {
    let volume: Double
    init(volume: Double) { self.volume = volume }
}

class Cube: Box {
    init(side: Double) {
        super.init(volume: side * side * side)
    }
}

let cube = Cube(side: 3.0)
print("Kub hajmi: \(cube.volume)")
```

## Tushuntirish va Mantiq:
super.init parametrlariga arifmetik ifodalar va hisoblangan qiymatlarni to'g'ridan-to'g'ri uzatish mumkin.

## Ishlash natijasi:
```text
Kub hajmi: 27.0
```


# 393-Topshiriq: Struct ichidagi Struct initsializatsiyasi
## Topshiriq sharti:
Ichma-ich tuzilmalarni chiroyli parametrlar bilan konstruktorda yig'ish.

## Yechim (Swift kodi):
```swift
import Foundation

struct LatLng { let lat: Double; let lng: Double }
struct LocationPlace {
    let name: String
    let coords: LatLng
    
    init(name: String, lat: Double, lng: Double) {
        self.name = name
        self.coords = LatLng(lat: lat, lng: lng)
    }
}

let place = LocationPlace(name: "Xiva", lat: 41.3783, lng: 60.3639)
print("Joy: \(place.name), Lat: \(place.coords.lat)")
```

## Tushuntirish va Mantiq:
Konstruktorlar ichki ob'ektlarni yashirib, foydalanuvchiga qulay tashqi interfeys taqdim etishi mumkin.

## Ishlash natijasi:
```text
Joy: Xiva, Lat: 41.3783
```


# 394-Topshiriq: Initsializatsiya paytida xotirani to'liq tozalash
## Topshiriq sharti:
Xavfsiz ma'lumotlarni saqlashdan oldin xotira tozaligini ta'minlash.

## Yechim (Swift kodi):
```swift
import Foundation

struct SecretNote {
    let note: String
    init(note: String) {
        self.note = note
    }
}

let note = SecretNote(note: "Maxfiy matn")
print("Eslatma: \(note.note)")
```

## Tushuntirish va Mantiq:
Initsializatsiya qat'iy ma'lumot yaxlitligini ta'minlaydi.

## Ishlash natijasi:
```text
Eslatma: Maxfiy matn
```


# 395-Topshiriq: Kechiktirilgan initsializatsiya o'zgarmaslar (Deferred let initialization)
## Topshiriq sharti:
Shartli tarmoqlanishda har bir yo'lda 'let' maydoniga faqat bitta marta qiymat berish.

## Yechim (Swift kodi):
```swift
import Foundation

class SessionConfig {
    let timeout: Int
    
    init(isFast: Bool) {
        if isFast {
            self.timeout = 5
        } else {
            self.timeout = 30
        }
    }
}

let conf = SessionConfig(isFast: true)
print("Timeout: \(conf.timeout)s")
```

## Tushuntirish va Mantiq:
Swift kompilyatori har bir shart tarmog'ida 'let' maydoniga aynan bir marta qiymat biriktirilganini qat'iy tekshiradi.

## Ishlash natijasi:
```text
Timeout: 5s
```


# 396-Topshiriq: Qaytuvchi qiymatsiz failable initsializatorni tekshirish
## Topshiriq sharti:
Failable initsializator orqali ob'ekt yaratilganini guard bilan tekshirish.

## Yechim (Swift kodi):
```swift
import Foundation

struct PortNumber {
    let value: Int
    init?(value: Int) {
        guard value > 0 && value < 65536 else { return nil }
        self.value = value
    }
}

func configurePort(raw: Int) {
    guard let port = PortNumber(value: raw) else {
        print("Noto'g'ri port raqami: \(raw)")
        return
    }
    print("Port sozlandi: \(port.value)")
}

configurePort(raw: 443)
configurePort(raw: 99999)
```

## Tushuntirish va Mantiq:
Failable initsializatorlar guard let bilan birlashganda xavfsiz oqimni shakllantiradi.

## Ishlash natijasi:
```text
Port sozlandi: 443
Noto'g'ri port raqami: 99999
```


# 397-Topshiriq: Initsializatorda xususiyat kuzatuvchilari ishlamasligi va uni chetlab o'tish
## Topshiriq sharti:
Agar initsializatsiya paytida didSet harakati kerak bo'lsa, alohida metod chaqirish usuli.

## Yechim (Swift kodi):
```swift
import Foundation

class TemperatureSensor {
    var reading: Double = 0.0 {
        didSet { logReading() }
    }
    
    init(initialReading: Double) {
        self.reading = initialReading
        logReading() // Init ichida qo'lda chaqiriladi!
    }
    
    func logReading() {
        print("Sensor ko'rsatkichi: \(reading)°C")
    }
}

let _ = TemperatureSensor(initialReading: 24.5)
```

## Tushuntirish va Mantiq:
Initsializatsiya paytida didSet ishlamaganligi sababli, boshlang'ich log yoki harakat kerak bo'lsa uni Phase 2 da qo'lda chaqirish lozim.

## Ishlash natijasi:
```text
Sensor ko'rsatkichi: 24.5°C
```


# 398-Topshiriq: Failable initsializatorlar bilan massivni to'ldirish (compactMap)
## Topshiriq sharti:
Matnlar ro'yxatidan faqat failable init muvaffaqiyatli bo'lganlarini yig'ing.

## Yechim (Swift kodi):
```swift
import Foundation

struct UserID {
    let id: Int
    init?(raw: String) {
        guard let num = Int(raw), num > 0 else { return nil }
        self.id = num
    }
}

let rawIDs = ["101", "-5", "abc", "205", "0"]
let validIDs = rawIDs.compactMap { UserID(raw: $0) }

print("Valid IDlar soni: \(validIDs.count)")
for item in validIDs {
    print("- ID #\(item.id)")
}
```

## Tushuntirish va Mantiq:
'compactMap' failable initsializatorlar bilan mukammal ishlaydi va nil qaytganlarini tashlab yuboradi.

## Ishlash natijasi:
```text
Valid IDlar soni: 2
- ID #101
- ID #205
```


# 399-Topshiriq: Convenience init orqali konfiguratsiya ob'ektini qabul qilish
## Topshiriq sharti:
Katta konfiguratsiya strukturasini qabul qilib maydonlarga tarqatuvchi qulay konstruktor.

## Yechim (Swift kodi):
```swift
import Foundation

struct DatabaseParams {
    let host: String
    let port: Int
    let user: String
}

class DatabaseManager {
    let host: String
    let port: Int
    let user: String
    
    init(host: String, port: Int, user: String) {
        self.host = host; self.port = port; self.user = user
    }
    
    convenience init(params: DatabaseParams) {
        self.init(host: params.host, port: params.port, user: params.user)
    }
}

let params = DatabaseParams(host: "localhost", port: 5432, user: "admin")
let dm = DatabaseManager(params: params)
print("Baza: \(dm.user)@\(dm.host):\(dm.port)")
```

## Tushuntirish va Mantiq:
Parametrlar ob'ektini qabul qiluvchi convenience initsializatorlar API dizaynini juda qulay qiladi.

## Ishlash natijasi:
```text
Baza: admin@localhost:5432
```


# 400-Topshiriq: Amaliy loyiha: Tarmoq soketi sessiyasi boshqaruvchisi (Init zanjiri va Deinit xavfsizligi)
## Topshiriq sharti:
Sessiyani initsializatsiya qiluvchi (designated/convenience/failable), uning holatini boshqaruvchi va deinit da soketni kafolatli yopuvchi yaxlit modul.

## Yechim (Swift kodi):
```swift
import Foundation

class NetworkSocketSession {
    let host: String
    let port: Int
    let sessionToken: String
    private(set) var isOpen: Bool = false
    
    // Designated Initializer
    init?(host: String, port: Int, token: String) {
        guard !host.isEmpty, port > 0 && port <= 65535, !token.isEmpty else {
            print("XATO: Noto'g'ri soket parametrlari!")
            return nil
        }
        self.host = host
        self.port = port
        self.sessionToken = token
        self.isOpen = true
        print("SOKET OCHILDI: [\(host):\(port)] Token: \(token)")
    }
    
    // Convenience Initializer
    convenience init?(secureHost: String) {
        self.init(host: secureHost, port: 443, token: "SSL_SECURE_TOKEN_2026")
    }
    
    func sendData(_ message: String) {
        guard isOpen else {
            print("Soket yopiq, ma'lumot yuborilmadi.")
            return
        }
        print("Ma'lumot uzatildi: '\(message)'")
    }
    
    func close() {
        if isOpen {
            isOpen = false
            print("Soket qo'lda yopildi.")
        }
    }
    
    // Deinit kafolatli tozalash
    deinit {
        if isOpen {
            isOpen = false
            print("DEINIT: Soket resurslari xavfsiz tozalandi.")
        }
    }
}

do {
    if let session = NetworkSocketSession(secureHost: "socket.khorazmiy.uz") {
        session.sendData("PING_PAYLOAD")
    }
}
print("Sessiya ko'rinish sohasidan chiqdi.")
```

## Tushuntirish va Mantiq:
Ushbu yakuniy amaliy loyihada Designated init, Convenience init, Failable tekshiruv va Deinit tozalash mexanizmlari to'liq real tizim sifatida yaratildi.

## Ishlash natijasi:
```text
SOKET OCHILDI: [socket.khorazmiy.uz:443] Token: SSL_SECURE_TOKEN_2026
Ma'lumot uzatildi: 'PING_PAYLOAD'
DEINIT: Soket resurslari xavfsiz tozalandi.
Sessiya ko'rinish sohasidan chiqdi.
```

