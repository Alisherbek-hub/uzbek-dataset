# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks_data = [
    (
        351,
        "Initsializatsiya asoslari: init() konstruktori",
        "Kompaniyadagi xodim ma'lumotlarini to'g'ri initsializatsiya qiluvchi sinf yozing.",
        """import Foundation

class StaffMember {
    var name: String
    var role: String
    
    init(name: String, role: String) {
        self.name = name
        self.role = role
    }
}

let staff = StaffMember(name: "Davron", role: "Arxitektor")
print("Xodim: \\(staff.name), Lavozim: \\(staff.role)")
""",
        "Initsializatsiya (Initialization) — bu sinf, struktura yoki enum nusxasi yaratilishida uning barcha saqlanuvchi xususiyatlariga boshlang'ich qiymat berish va ob'ektni foydalanishga tayyorlash jarayonidir.",
        """Xodim: Davron, Lavozim: Arxitektor"""
    ),
    (
        352,
        "Default Initializer (Standart konstruktor)",
        "Barcha maydonlar boshlang'ich qiymatga ega bo'lganda argumentsiz init() qanday hosil bo'lishini ko'rsating.",
        """import Foundation

class SystemConfig {
    var maxConnections: Int = 100
    var isDebugMode: Bool = false
}

let config = SystemConfig()
print("Maksimal ulanishlar: \\(config.maxConnections), Debug: \\(config.isDebugMode)")
""",
        "Agar sinf yoki struct-dagi barcha xususiyatlar standart qiymatga ega bo'lsa va maxsus init yozilmagan bo'lsa, Swift avtomatik ravishda argumentsiz 'init()' taqdim etadi.",
        """Maksimal ulanishlar: 100, Debug: false"""
    ),
    (
        353,
        "Struct larda Memberwise Initializer",
        "Struct-ning avtomatik barcha parametrlar bo'yicha konstruktorini ko'rsating.",
        """import Foundation

struct UserProfile {
    let username: String
    var age: Int
    var isVerified: Bool = false
}

let user = UserProfile(username: "nodir_99", age: 25)
print("Foydalanuvchi: \\(user.username), Tasdiqlangan: \\(user.isVerified)")
""",
        "Struct larda default qiymatga ega maydonlar memberwise initializatorida ixtiyoriy parametr sifatida qoldirilishi mumkin.",
        """Foydalanuvchi: nodir_99, Tasdiqlangan: false"""
    ),
    (
        354,
        "Maxsus init yozganda Memberwise init ni saqlash (Extension)",
        "Struct ga maxsus init qo'shilganda ham uning avtomatik memberwise initsializatorini yo'qotmaslik usuli.",
        """import Foundation

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
print("p1: (\\(p1.x), \\(p1.y)), p2: (\\(p2.x), \\(p2.y))")
""",
        "Agar maxsus init asosiy 'struct' tanasi ichida yozilsa, avtomatik memberwise init yo'qoladi. Ammo maxsus init 'extension' ichida yozilsa, ikkala konstruktor ham mavjud bo'lib qoladi.",
        """p1: (10.0, 20.0), p2: (15.0, 15.0)"""
    ),
    (
        355,
        "Initializer Delegation qiymat turlarida (self.init)",
        "Bitta konstruktor boshqa konstruktorni chaqiruvchi delegatsiya mexanizmini struct-da yozing.",
        """import Foundation

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
print("O'lcham: \\(cube.width) x \\(cube.height)")
""",
        "Qiymat turlarida (struct va enum) konstruktorlar 'self.init(...)' orqali bir-biriga vazifani yuklashi (delegation) mumkin.",
        """O'lcham: 50.0 x 50.0"""
    ),
    (
        356,
        "Sinflarda Designated Initializers",
        "Sinfning barcha maydonlarini to'liq initsializatsiya qiluvchi asosiy (designated) konstruktorini yozing.",
        """import Foundation

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
print("Transport: \\(v.name), G'ildiraklar: \\(v.wheels)")
""",
        "Designated Initializer sinfning asosiy konstruktori bo'lib, o'sha sinfning barcha saqlanuvchi maydonlarini to'liq initsializatsiya qiladi va ota sinfning mos konstruktorini chaqiradi.",
        """Transport: Avtomobil, G'ildiraklar: 4"""
    ),
    (
        357,
        "Sinflarda Convenience Initializers (Qulay konstruktorlar)",
        "Asosiy initsializatorga qulay parametrlar bilan murojaat qiluvchi 'convenience init' yozing.",
        """import Foundation

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
print("Oziq-ovqat: \\(snack.name), Kaloriya: \\(snack.calories)")
""",
        "'convenience' kalit so'zi bilan belgilangan konstruktorlar yordamchi bo'lib, ular oxir-oqibat o'sha sinfning Designated konstruktoriga murojaat qilishi shart.",
        """Oziq-ovqat: Olma, Kaloriya: 100"""
    ),
    (
        358,
        "Sinflarda Initializer Delegation qoidalari",
        "Designated yuqoriga (super.init), Convenience yonboshga (self.init) murojaat qilish qoidasini ko'rsating.",
        """import Foundation

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
print("ID: \\(child.id), Nomi: \\(child.name)")
""",
        "Qoida 1: Designated init to'g'ridan-to'g'ri ota sinfning designated initini chaqirishi shart. Qoida 2: Convenience init o'z sinfining boshqa initini chaqirishi shart va oxiri designated initga borishi shart.",
        """ID: 0, Nomi: Yordamchi"""
    ),
    (
        359,
        "Ikki bosqichli initsializatsiya (Two-Phase Initialization)",
        "1-faza (barcha maydonlar to'lishi) va 2-faza (self to'liq tayyor bo'lishi) qoidalarini amalda ko'rsating.",
        """import Foundation

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
        print("Smartfon: Serial=\\(serialNumber), OS=\\(osVersion)")
    }
}

let phone = Smartphone(serial: "APL_2026", os: "iOS 18")
""",
        "Swift xotira xavfsizligini 2 bosqichli initsializatsiya bilan kafolatlaydi: 1-bosqichda barcha maydonlarga qiymat beriladi; 2-bosqichda esa metodlar va self bilan amallar bajarishga ruxsat etiladi.",
        """Smartfon: Serial=APL_2026, OS=iOS 18"""
    ),
    (
        360,
        "Xavfsizlik tekshiruvi: super.init dan oldin o'z maydonlarini to'ldirish",
        "O'z xususiyatlariga qiymat bermasdan super.init chaqirilsa yuzaga keladigan xatoni tushuntiring.",
        """import Foundation

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
print("Servis ID: \\(a.serviceID), Kalit: \\(a.apiKey)")
""",
        "Swift-da bola sinf o'zining barcha yangi maydonlariga qiymat biriktirmasdan oldin super.init() ni chaqira olmaydi.",
        """Servis ID: SRV_1, Kalit: KEY_XYZ"""
    ),
    (
        361,
        "Meros olingan xususiyatlarni override qilishda initsializator",
        "Ota sinf konstruktorini 'override init' kalit so'zi bilan qayta yozing.",
        """import Foundation

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
print("Shakl: \\(t.name), Tomonlar soni: \\(t.sides)")
""",
        "Agar subclass ota sinfining Designated konstruktori bilan aynan bir xil parametrli konstruktor yozsa, 'override' kalit so'zini qo'yish shart.",
        """Shakl: Uchburchak, Tomonlar soni: 3"""
    ),
    (
        362,
        "Avtomatik initsializator merosxo'rligi qoidalari",
        "Subclass o'ziga yangi designated init qo'shmasa, ota sinfning barcha initlarini avtomatik meros qilib olishini ko'rsating.",
        """import Foundation

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
print("Bike1: \\(bike1.color), Bike2: \\(bike2.color)")
""",
        "Agar subclass hech qanday yangi designated init yozmasa, u ota sinfning barcha designated va convenience konstruktorlarini to'liq avtomatik meros oladi.",
        """Bike1: Qizil, Bike2: Oq"""
    ),
    (
        363,
        "Failable Initializer (init?): Muvaffaqiyatsiz bo'ladigan konstruktor",
        "Noto'g'ri oraliqdagi harorat berilganda nil qaytaruvchi konstruktor yozing.",
        """import Foundation

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

print("Valid: \\(validT != nil)")
print("Invalid: \\(invalidT != nil)")
""",
        "'init?' konstruktori parametrlar talabga mos kelmaganda initsializatsiyani bekor qilib 'nil' qaytaradi. Natija esa 'T?' (Optional) bo'ladi.",
        """Valid: true
Invalid: false"""
    ),
    (
        364,
        "Enum larda Failable Initializer",
        "Enum ning 'init?(rawValue:)' avtomatik failable initsializatori qanday ishlashini ko'rsating.",
        """import Foundation

enum HTTPStatusCode: Int {
    case ok = 200
    case notFound = 404
    case serverError = 500
}

let success = HTTPStatusCode(rawValue: 200)
let unknown = HTTPStatusCode(rawValue: 999)

print("200 holati: \\(String(describing: success))")
print("999 holati: \\(String(describing: unknown))")
""",
        "Swift RawRepresentable enum lari uchun avtomatik ravishda 'init?(rawValue:)' failable konstruktorini taqdim etadi.",
        """200 holati: Optional(HTTPStatusCode.ok)
999 holati: nil"""
    ),
    (
        365,
        "Failable Initializer larning tarqalishi (Propagation)",
        "Murakkab ob'ekt ichki failable init xato berganda o'zi ham nil qaytarishini ko'rsating.",
        """import Foundation

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

print("c1 muvaffaqiyatlimi? \\(c1 != nil)")
print("c2 muvaffaqiyatlimi? \\(c2 != nil)")
""",
        "Failable initsializatorlar zanjirida har qanday bo'g'indagi nosozlik butun initsializatsiya jarayonining 'nil' bilan yakunlanishiga sabab bo'ladi.",
        """c1 muvaffaqiyatlimi? true
c2 muvaffaqiyatlimi? false"""
    ),
    (
        366,
        "Failable init ni Non-failable ga aylantirib override qilish",
        "Subclass ota sinfning muvaffaqiyatsiz bo'lishi mumkin bo'lgan initini kafolatli muvaffaqiyatliga aylantirsin.",
        """import Foundation

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
print("SafeDocument matni: \\(doc.text)")
""",
        "Subclass ota sinfning 'init?' ini oddiy kafolatlangan 'init' qilib override qilishi mumkin (ammo teskarisi mumkin emas).",
        """SafeDocument matni: Standart matn"""
    ),
    (
        367,
        "Majburiy initsializatorlar: required init",
        "Barcha subclass lar albatta qayta yozishi shart bo'lgan konstruktorni e'lon qiling.",
        """import Foundation

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
""",
        "'required' kalit so'zi barcha voris sinflarga ushbu konstruktorni majburiy realizatsiya qilish talabini qo'yadi. Voris sinfda 'override' so'zi yozilmaydi, yana 'required' deb davom etiladi.",
        """BaseView initsializatsiya qilindi.
CustomButtonView tayyorlandi."""
    ),
    (
        368,
        "Xatolik tashlovchi initsializator: init() throws",
        "Noto'g'ri parametrlar kiritilganda aniq xato tashlovchi konstruktor tuzing.",
        """import Foundation

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
    print("Muvaffaqiyatli server: \\(conf.host):\\(conf.port)")
    let _ = try NetworkConfiguration(host: "", port: 80)
} catch {
    print("Initsializatsiyada xatolik: \\(error)")
}
""",
        "'init() throws' konstruktori xato sababini aniq ko'rsatish zarur bo'lganda 'init?' dan afzalroqdir.",
        """Muvaffaqiyatli server: khorazmiy.uz:8080
Initsializatsiyada xatolik: missingHost"""
    ),
    (
        369,
        "Yopiq initsializator: private init()",
        "Tashqaridan yangi nusxa olinishini cheklab, Singleton yaratish.",
        """import Foundation

class SystemLogger {
    static let shared = SystemLogger()
    
    private init() {
        print("SystemLogger yagona nusxasi ishga tushdi.")
    }
    
    func log(_ msg: String) {
        print("[LOG]: \\(msg)")
    }
}

SystemLogger.shared.log("Tizim barqaror ishlamoqda.")
""",
        "'private init()' tashqi kod tomonidan 'SystemLogger()' deb yangi nusxa olinishini to'liq taqiqlaydi.",
        """SystemLogger yagona nusxasi ishga tushdi.
[LOG]: Tizim barqaror ishlamoqda."""
    ),
    (
        370,
        "Xotirani tozalash asoslari: deinit sintaksisi",
        "Sinf ob'ekti xotiradan bo'shatilganda resurs tozalanishini ko'rsating.",
        """import Foundation

class DatabaseConnection {
    let connectionID: Int
    
    init(id: Int) {
        self.connectionID = id
        print("Ulanish #\\(connectionID) ochildi.")
    }
    
    deinit {
        print("Ulanish #\\(connectionID) xavfsiz yopildi.")
    }
}

do {
    let conn = DatabaseConnection(id: 42)
    print("Ulanishdan foydalanilmoqda...")
}
print("Blok tugadi.")
""",
        "'deinit' faqat sinflarda (class) bo'lib, ob'ekt xotiradan butunlay o'chirilishidan oldin avtomatik chaqiriladi.",
        """Ulanish #42 ochildi.
Ulanishdan foydalanilmoqda...
Ulanish #42 xavfsiz yopildi.
Blok tugadi."""
    ),
    (
        371,
        "Deinit chaqirilish tartibi (Subclass avval, Superclass keyin)",
        "Merosxo'rlik zanjirida deinit teskari tartibda chaqirilishini isbotlang.",
        """import Foundation

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
""",
        "Swift avval bola sinfning deinitializatorini, so'ngra ota sinfning deinitializatorini avtomatik zanjirli chaqiradi.",
        """2. AdvancedWorker deinit chaqirildi.
1. BaseWorker deinit chaqirildi."""
    ),
    (
        372,
        "Resurslarni deinit da tozalash: Taymerni bekor qilish",
        "Sinf xotiradan o'chganda fondagi taymerni to'xtatuvchi toza arxitektura.",
        """import Foundation

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
""",
        "Deinit resurs sizib ketishi (resource leak) va fon vazifalarining osilib qolishini oldini oluvchi eng muhim himoyadir.",
        """Monitoring boshlandi.
Monitoring to'xtatildi va xotira tozalandi."""
    ),
    (
        373,
        "Closure yordamida standart xususiyat qiymatini initsializatsiya qilish",
        "Murakkab massivni closure orqali boshlang'ich qiymat bilan to'ldiring.",
        """import Foundation

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
print("Kataklar: \\(chess.boardColors)")
""",
        "'{ ... }()' darhol bajariluvchi closure xususiyatga murakkab hisob-kitoblar natijasini boshlang'ich qiymat qilib berish imkonini beradi.",
        """Kataklar: ["Oq", "Qora", "Qora", "Oq"]"""
    ),
    (
        374,
        "Initsializatsiyada parametr nomlari va yorliqlari",
        "Har xil parametr yorliqlariga ega bir nechta initsializatorlar e'lon qiling.",
        """import Foundation

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
print("Magenta red: \\(magenta.red), Gray red: \\(gray.red)")
""",
        "Initsializatorlar ham oddiy funksiyalar kabi turli xil argument yorliqlariga ega bo'lishi mumkin.",
        """Magenta red: 1.0, Gray red: 0.5"""
    ),
    (
        375,
        "Standart parametr qiymatlari bilan bitta universal init",
        "Bir nechta parametrga default berib turli chaqiruvlarni qanoatlantiring.",
        """import Foundation

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
print("q1 timeout: \\(q1.timeout), q2 timeout: \\(q2.timeout)")
""",
        "Standart parametr qiymatlari orqali bir nechta ortiqcha init yozishdan qutulish mumkin.",
        """q1 timeout: 30, q2 timeout: 10"""
    ),
    (
        376,
        "init! (Implicitly Unwrapped Failable Initializer)",
        "Muvaffaqiyatsiz bo'lsa nil beradigan, ammo muvaffaqiyatli bo'lsa majburiy ochilgan (T!) ko'rinishida qaytadigan konstruktor.",
        """import Foundation

struct Identifier {
    let value: String
    
    init!(value: String) {
        if value.isEmpty { return nil }
        self.value = value
    }
}

let id: Identifier = Identifier(value: "USER_001")
print("ID qiymati: \\(id.value)")
""",
        "'init!' failable init kabi nil qaytarishi mumkin, lekin muvaffaqiyatli bo'lsa uni unwrap qilmasdan to'g'ridan-to'g'ri ishlatishga ruxsat beradi.",
        """ID qiymati: USER_001"""
    ),
    (
        377,
        "Generic turlarda initsializatorlar",
        "Generik struktura uchun parametrlar turini qabul qiluvchi konstruktor yozing.",
        """import Foundation

struct KeyValueContainer<K: Hashable, V> {
    let key: K
    let value: V
    
    init(key: K, value: V) {
        self.key = key
        self.value = value
    }
}

let pair = KeyValueContainer(key: "ID", value: 1004)
print("Juftlik: \\(pair.key) -> \\(pair.value)")
""",
        "Generik initsializatorlar berilgan qiymatlarga qarab K va V turlarini avtomatik ravishda aniqlaydi.",
        """Juftlik: ID -> 1004"""
    ),
    (
        378,
        "Maxsus Decoder initsializatori: init(from decoder: Decoder)",
        "Decodable protokoli orqali JSON dan ma'lumotlarni qo'lda qabul qiluvchi konstruktor yozing.",
        """import Foundation

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

let json = \"\"\"{"user_name": "Ulugbek", "score": 95}\"\"\".data(using: .utf8)!
if let user = try? JSONDecoder().decode(UserRecord.self, from: json) {
    print("Dekodlandi: \\(user.username), Ball: \\(user.score)")
}
""",
        "'init(from decoder:)' orqali JSON kalitlarini va tiplarini moslashtiruvchi to'liq boshqaruvga ega bo'linadi.",
        """Dekodlandi: Ulugbek, Ball: 95"""
    ),
    (
        379,
        "Initsializatsiyada 'defer' operatori",
        "Konstruktor ishlash jarayonida defer bloki qachon ishga tushishini ko'rsating.",
        """import Foundation

class InitTracer {
    init() {
        defer { print("3. Initsializatsiya yakunlandi (defer).") }
        print("1. Initsializatsiya boshlandi.")
        print("2. Parametrlar o'rnatildi.")
    }
}

let _ = InitTracer()
""",
        "Init ichidagi 'defer' bloki konstruktor tanasi to'liq yakunlanib ob'ekt xotiraga tayyor bo'lish paytida ijro etiladi.",
        """1. Initsializatsiya boshlandi.
2. Parametrlar o'rnatildi.
3. Initsializatsiya yakunlandi (defer)."""
    ),
    (
        380,
        "Failable init dan erta 'return nil' qilish",
        "Shart qanoatlantirilmaganda hech qanday ortiqcha xotira sarflamay darhol chiqish.",
        """import Foundation

struct NonEmptyString {
    let content: String
    
    init?(content: String) {
        guard !content.trimmingCharacters(in: .whitespaces).isEmpty else {
            return nil
        }
        self.content = content
    }
}

print("Bo'sh matn: \\(String(describing: NonEmptyString(content: "   ")))")
print("To'la matn: \\(String(describing: NonEmptyString(content: "Swift")?.content))")
""",
        "Failable konstruktorda xatolik aniqlanishi bilan 'return nil' qilinadi va ob'ekt yaratilishi bekor qilinadi.",
        """Bo'sh matn: nil
To'la matn: Optional("Swift")"""
    ),
    (
        381,
        "Initsializatsiya paytida hisoblangan xususiyatlarga murojaat cheklovlari",
        "Barcha maydonlar to'liq qiymat olguncha getter larni chaqirib bo'lmasligini tushuntiring.",
        """import Foundation

class CircleCalc {
    var radius: Double
    var diameter: Double { radius * 2 }
    
    init(radius: Double) {
        self.radius = radius
        // Bu yerda self.radius qiymat olgandan keyingina self.diameter ga murojaat qilish mumkin:
        print("Diametr: \\(self.diameter)")
    }
}

let _ = CircleCalc(radius: 7.0)
""",
        "Swift-da hisoblangan xususiyatlarga murojaat qilish 2-faza (Phase 2) hisoblanadi va saqlanuvchi maydonlar to'liq qiymat olgachgina ruxsat etiladi.",
        """Diametr: 14.0"""
    ),
    (
        382,
        "Init paytida self ni tashqariga parametr qilib uzatish cheklovi",
        "Nima uchun 1-bosqich tugamasdan self ni boshqa metodga berib bo'lmasligini ko'rsating.",
        """import Foundation

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
""",
        "Kompilyator ob'ekt to'liq yaratilib bitmaguncha (Phase 1 yakunlanmaguncha) uning ko'rsatkichini boshqa joyga uzatishni taqiqlaydi.",
        """Mijoz ro'yxatga olindi."""
    ),
    (
        383,
        "Convenience init orqali keshdan ob'ekt qaytarish cheklovi",
        "Init doimo yangi ob'ekt yaratishga majburligi sababli, keshdan qaytarish uchun Fabrika metodi afzalligini tushuntiring.",
        """import Foundation

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
print("r1 === r2: \\(r1 === r2)")
""",
        "Swift-da oddiy konstruktorlar (init) yangi instansiya ajratishga majbur. Agar mavjud keshdan ob'ekt qaytarish kerak bo'lsa, 'static factory method' ishlatiladi.",
        """r1 === r2: true"""
    ),
    (
        384,
        "Initsializatorda inout parametrlarini ishlatish",
        "Tashqi o'zgaruvchi qiymatini kamaytirib ob'ektni initsializatsiya qilish.",
        """import Foundation

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
print("Chipta 1 o'rni: \\(t1.seatNumber), Chipta 2 o'rni: \\(t2.seatNumber)")
""",
        "Konstruktorda ham 'inout' parametrlari orqali tashqi resurs hisoblagichlarini parallel yangilab borish mumkin.",
        """Chipta 1 o'rni: 1, Chipta 2 o'rni: 2"""
    ),
    (
        385,
        "Subclass convenience init ota sinf designated initini chaqira olmasligi",
        "Subclass convenience faqat o'zining designated initini chaqirishi shartligini ko'rsating.",
        """import Foundation

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
print("Tur: \\(d.species), Zot: \\(d.breed)")
""",
        "Convenience konstruktor faqat o'z sinfidagi boshqa konstruktorlarga delegatsiya qila oladi, ota sinfga to'g'ridan-to'g'ri sakray olmaydi.",
        """Tur: It, Zot: Ovcharka"""
    ),
    (
        386,
        "Statik initsializatsiya (Static / Type Initialization)",
        "Sinfning statik xususiyati birinchi chaqirilganda qanday initsializatsiya bo'lishini ko'rsating.",
        """import Foundation

class DatabaseDriver {
    static let connectionPool: String = {
        print("Baza drayveri initsializatsiya qilindi!")
        return "POOLED_CONNECTIONS"
    }()
}

print("Dastur ishga tushdi.")
print("Resurs: \\(DatabaseDriver.connectionPool)")
""",
        "Swift-da statik xususiyatlar birinchi murojaat paytida (lazily) va thread-safe tarzda 'swift_once' orqali initsializatsiya qilinadi.",
        """Dastur ishga tushdi.
Baza drayveri initsializatsiya qilindi!
Resurs: POOLED_CONNECTIONS"""
    ),
    (
        387,
        "Deinit ichida resurs tozalash xavfsizligi",
        "Ob'ekt o'chirilishida xotirani xavfsiz nolga tenglashtirish.",
        """import Foundation

class MemoryBuffer {
    var size: Int
    init(size: Int) {
        self.size = size
        print("Xotira buferi (\\(size) bayt) ajratildi.")
    }
    deinit {
        print("Xotira buferi tozalandi.")
    }
}

do {
    let _ = MemoryBuffer(size: 1024)
}
""",
        "Deinit resurslarni tozalash uchun ideal va yagona kafolatlangan joydir.",
        """Xotira buferi (1024 bayt) ajratildi.
Xotira buferi tozalandi."""
    ),
    (
        388,
        "Deinit ichida o'ziga yangi strong havola (Zombie Object) hosil qilishdan saqlanish",
        "Deinit paytida self ni global massivga qo'shish qat'iyan taqiqlanganligini tushuntiring.",
        """import Foundation

class SafeDeinitWorker {
    let id: Int = 1
    deinit {
        print("Xavfsiz tozalash: self hech qanday global o'zgaruvchiga uzatilmaydi.")
    }
}

do {
    let _ = SafeDeinitWorker()
}
""",
        "Agar deinit ichida 'globalArray.append(self)' qilinsa, o'layotgan ob'ekt qayta tiriltirilishga uriniladi (Resurrecting), bu Swift-da qat'iy fatal xatoga olib keladi.",
        """Xavfsiz tozalash: self hech qanday global o'zgaruvchiga uzatilmaydi."""
    ),
    (
        389,
        "Initsializatorda precondition qo'llash",
        "Xavfsiz port raqamini tekshiruvchi kafolatli initsializator.",
        """import Foundation

struct SecurePort {
    let port: Int
    init(port: Int) {
        precondition(port > 1024, "Port 1024 dan katta bo'lishi shart!")
        self.port = port
    }
}

let p = SecurePort(port: 8080)
print("Port: \\(p.port)")
""",
        "Initsializatorda 'precondition' dasturning kritik invariantlarini tekshirishda ishlatiladi.",
        """Port: 8080"""
    ),
    (
        390,
        "Bir nechta Failable initsializatorlar kombinatsiyasi",
        "Matndan yoki sondan failable initsializatsiya qiluvchi rang modeli.",
        """import Foundation

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
print("Rang 1: \\(c1?.hex ?? ""), Rang 2: \\(c2?.hex ?? "")")
""",
        "Turli kiruvchi ma'lumotlar uchun alohida-alohida failable konstruktorlar taqdim etish keng tarqalgan amaliyotdir.",
        """Rang 1: #FF5733, Rang 2: #00FF00"""
    ),
    (
        391,
        "Ota sinfdan meros olingan required init larni bajarish",
        "Subclass o'zining yangi designated initini yozganda ham required initni amalga oshirishga majburligi.",
        """import Foundation

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
print("Vidjet nomi: \\(w.title)")
""",
        "Agar subclass yangi designated init yozsa, ota sinfning barcha 'required' konstruktorlarini qayta yozishi shart bo'ladi.",
        """Widget yaratildi.
Vidjet nomi: Standart vidjet"""
    ),
    (
        392,
        "Merosxo'rlikda super.init parametrlarini hisoblab uzatish",
        "Ota sinf initsializatoriga hisoblangan qiymatlarni uzating.",
        """import Foundation

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
print("Kub hajmi: \\(cube.volume)")
""",
        "super.init parametrlariga arifmetik ifodalar va hisoblangan qiymatlarni to'g'ridan-to'g'ri uzatish mumkin.",
        """Kub hajmi: 27.0"""
    ),
    (
        393,
        "Struct ichidagi Struct initsializatsiyasi",
        "Ichma-ich tuzilmalarni chiroyli parametrlar bilan konstruktorda yig'ish.",
        """import Foundation

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
print("Joy: \\(place.name), Lat: \\(place.coords.lat)")
""",
        "Konstruktorlar ichki ob'ektlarni yashirib, foydalanuvchiga qulay tashqi interfeys taqdim etishi mumkin.",
        """Joy: Xiva, Lat: 41.3783"""
    ),
    (
        394,
        "Initsializatsiya paytida xotirani to'liq tozalash",
        "Xavfsiz ma'lumotlarni saqlashdan oldin xotira tozaligini ta'minlash.",
        """import Foundation

struct SecretNote {
    let note: String
    init(note: String) {
        self.note = note
    }
}

let note = SecretNote(note: "Maxfiy matn")
print("Eslatma: \\(note.note)")
""",
        "Initsializatsiya qat'iy ma'lumot yaxlitligini ta'minlaydi.",
        """Eslatma: Maxfiy matn"""
    ),
    (
        395,
        "Kechiktirilgan initsializatsiya o'zgarmaslar (Deferred let initialization)",
        "Shartli tarmoqlanishda har bir yo'lda 'let' maydoniga faqat bitta marta qiymat berish.",
        """import Foundation

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
print("Timeout: \\(conf.timeout)s")
""",
        "Swift kompilyatori har bir shart tarmog'ida 'let' maydoniga aynan bir marta qiymat biriktirilganini qat'iy tekshiradi.",
        """Timeout: 5s"""
    ),
    (
        396,
        "Qaytuvchi qiymatsiz failable initsializatorni tekshirish",
        "Failable initsializator orqali ob'ekt yaratilganini guard bilan tekshirish.",
        """import Foundation

struct PortNumber {
    let value: Int
    init?(value: Int) {
        guard value > 0 && value < 65536 else { return nil }
        self.value = value
    }
}

func configurePort(raw: Int) {
    guard let port = PortNumber(value: raw) else {
        print("Noto'g'ri port raqami: \\(raw)")
        return
    }
    print("Port sozlandi: \\(port.value)")
}

configurePort(raw: 443)
configurePort(raw: 99999)
""",
        "Failable initsializatorlar guard let bilan birlashganda xavfsiz oqimni shakllantiradi.",
        """Port sozlandi: 443
Noto'g'ri port raqami: 99999"""
    ),
    (
        397,
        "Initsializatorda xususiyat kuzatuvchilari ishlamasligi va uni chetlab o'tish",
        "Agar initsializatsiya paytida didSet harakati kerak bo'lsa, alohida metod chaqirish usuli.",
        """import Foundation

class TemperatureSensor {
    var reading: Double = 0.0 {
        didSet { logReading() }
    }
    
    init(initialReading: Double) {
        self.reading = initialReading
        logReading() // Init ichida qo'lda chaqiriladi!
    }
    
    func logReading() {
        print("Sensor ko'rsatkichi: \\(reading)°C")
    }
}

let _ = TemperatureSensor(initialReading: 24.5)
""",
        "Initsializatsiya paytida didSet ishlamaganligi sababli, boshlang'ich log yoki harakat kerak bo'lsa uni Phase 2 da qo'lda chaqirish lozim.",
        """Sensor ko'rsatkichi: 24.5°C"""
    ),
    (
        398,
        "Failable initsializatorlar bilan massivni to'ldirish (compactMap)",
        "Matnlar ro'yxatidan faqat failable init muvaffaqiyatli bo'lganlarini yig'ing.",
        """import Foundation

struct UserID {
    let id: Int
    init?(raw: String) {
        guard let num = Int(raw), num > 0 else { return nil }
        self.id = num
    }
}

let rawIDs = ["101", "-5", "abc", "205", "0"]
let validIDs = rawIDs.compactMap { UserID(raw: $0) }

print("Valid IDlar soni: \\(validIDs.count)")
for item in validIDs {
    print("- ID #\\(item.id)")
}
""",
        "'compactMap' failable initsializatorlar bilan mukammal ishlaydi va nil qaytganlarini tashlab yuboradi.",
        """Valid IDlar soni: 2
- ID #101
- ID #205"""
    ),
    (
        399,
        "Convenience init orqali konfiguratsiya ob'ektini qabul qilish",
        "Katta konfiguratsiya strukturasini qabul qilib maydonlarga tarqatuvchi qulay konstruktor.",
        """import Foundation

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
print("Baza: \\(dm.user)@\\(dm.host):\\(dm.port)")
""",
        "Parametrlar ob'ektini qabul qiluvchi convenience initsializatorlar API dizaynini juda qulay qiladi.",
        """Baza: admin@localhost:5432"""
    ),
    (
        400,
        "Amaliy loyiha: Tarmoq soketi sessiyasi boshqaruvchisi (Init zanjiri va Deinit xavfsizligi)",
        "Sessiyani initsializatsiya qiluvchi (designated/convenience/failable), uning holatini boshqaruvchi va deinit da soketni kafolatli yopuvchi yaxlit modul.",
        """import Foundation

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
        print("SOKET OCHILDI: [\\(host):\\(port)] Token: \\(token)")
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
        print("Ma'lumot uzatildi: '\\(message)'")
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
""",
        "Ushbu yakuniy amaliy loyihada Designated init, Convenience init, Failable tekshiruv va Deinit tozalash mexanizmlari to'liq real tizim sifatida yaratildi.",
        """SOKET OCHILDI: [socket.khorazmiy.uz:443] Token: SSL_SECURE_TOKEN_2026
Ma'lumot uzatildi: 'PING_PAYLOAD'
DEINIT: Soket resurslari xavfsiz tozalandi.
Sessiya ko'rinish sohasidan chiqdi."""
    )
]

tasks = [format_task(*t) for t in tasks_data]
save_file("swift_08_initialization_va_deinit.md", tasks)
