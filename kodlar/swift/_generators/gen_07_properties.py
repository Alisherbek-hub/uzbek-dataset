# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks_data = [
    (
        301,
        "Saqlanuvchi xususiyatlar (Stored Properties)",
        "Talaba ismi va o'qish kursi saqlanuvchi xususiyatlarini o'z ichiga olgan struktura yarating.",
        """import Foundation

struct Student {
    var name: String
    var course: Int
}

var s = Student(name: "Lola", course: 2)
print("Talaba: \\(s.name), Kurs: \\(s.course)")
s.course = 3
print("Yangi kurs: \\(s.course)")
""",
        "Saqlanuvchi xususiyat (Stored Property) — bu struktura yoki sinf nusxasi ichida saqlanadigan oddiy o'zgarmas (let) yoki o'zgaruvchan (var) qiymatdir.",
        """Talaba: Lola, Kurs: 2
Yangi kurs: 3"""
    ),
    (
        302,
        "O'zgarmas saqlanuvchi xususiyatlar (let)",
        "Tizim foydalanuvchisining ID raqami bir marta belgilangach o'zgarmasligini ta'minlang.",
        """import Foundation

struct UserProfile {
    let userID: UUID
    var nickname: String
}

let profile = UserProfile(userID: UUID(), nickname: "cyber_ali")
print("ID o'rnatildi, Taxallus: \\(profile.nickname)")
""",
        "'let' bilan belgilangan saqlanuvchi xususiyat initsializatsiyadan so'ng butunlay o'zgarmas bo'ladi va o'zgartirishga urinish kompilyatsiya xatosini beradi.",
        """ID o'rnatildi, Taxallus: cyber_ali"""
    ),
    (
        303,
        "Kechiktirilgan xususiyatlar (lazy var)",
        "Qimmat hisob-kitobni faqat birinchi marta murojaat qilinganda hisoblovchi 'lazy var' ni ko'rsating.",
        """import Foundation

class HeavyDataProvider {
    init() { print("Og'ir ma'lumotlar yuklandi!") }
    func process() -> String { return "Ma'lumot tayyor" }
}

class Dashboard {
    lazy var provider = HeavyDataProvider()
}

let dash = Dashboard()
print("Dashboard yaratildi, provider hali chaqirilmadi.")
print("Murojaat qilinmoqda: \\(dash.provider.process())")
""",
        "'lazy' xususiyat faqat unga birinchi marta murojaat qilingandagina hisoblanadi va ishga tushiriladi. Bu ilovaning boshlang'ich ochilish tezligini oshiradi.",
        """Dashboard yaratildi, provider hali chaqirilmadi.
Og'ir ma'lumotlar yuklandi!
Murojaat qilinmoqda: Ma'lumot tayyor"""
    ),
    (
        304,
        "Nima uchun lazy doimo 'var' bo'lishi shart",
        "Kechiktirilgan xususiyat 'let' bo'la olmasligining texnik sababini tushuntiring.",
        """import Foundation

class ServerSession {
    // lazy let token: String = "ABC" // Kompilyatsiya xatosi!
    lazy var token: String = {
        return "SESSION_TOKEN_123"
    }()
}

let session = ServerSession()
print("Token: \\(session.token)")
""",
        "Chunki ob'ekt initsializatsiya bo'layotgan paytda 'lazy' xususiyat hali qiymatga ega bo'lmaydi. U keyinchalik birinchi murojaatda qiymat qabul qilishi sababli doimo 'var' bo'lishi shart.",
        """Token: SESSION_TOKEN_123"""
    ),
    (
        305,
        "Hisoblangan xususiyatlar: get va set",
        "Kvadrat tomoni o'zgarganda perimetrini, perimetr o'zgarganda tomonini hisoblovchi xususiyat yozing.",
        """import Foundation

struct Square {
    var side: Double
    
    var perimeter: Double {
        get {
            return side * 4
        }
        set {
            side = newValue / 4
        }
    }
}

var sq = Square(side: 10.0)
print("Perimetr: \\(sq.perimeter)")

sq.perimeter = 80.0
print("Yangi tomon: \\(sq.side)")
""",
        "Hisoblangan xususiyatlar (Computed Properties) xotirada to'g'ridan-to'g'ri qiymat saqlamaydi, balki boshqa xususiyatlar asosida dinamik ravishda hisoblaydi (getter) va belgilaydi (setter).",
        """Perimetr: 40.0
Yangi tomon: 20.0"""
    ),
    (
        306,
        "Faqat o'qiladigan hisoblangan xususiyatlar (Read-Only)",
        "Doira radiusi orqali uning yuzini hisoblovchi ixcham get xususiyatini ko'rsating.",
        """import Foundation

struct Circle {
    var radius: Double
    
    var area: Double {
        return Double.pi * radius * radius
    }
}

let c = Circle(radius: 5.0)
print("Yuzasi: \\(String(format: "%.2f", c.area))")
""",
        "Agar hisoblangan xususiyatda faqat 'get' bo'lsa, 'get { }' so'zlarini tashlab yuborib to'g'ridan-to'g'ri tana qismini yozish mumkin.",
        """Yuzasi: 78.54"""
    ),
    (
        307,
        "newValue standarti va maxsus parametr nomi",
        "Setter da keluvchi qiymatni standart 'newValue' yoki maxsus 'newVal' orqali qabul qiling.",
        """import Foundation

struct TemperatureConverter {
    var celsius: Double
    
    var fahrenheit: Double {
        get { celsius * 1.8 + 32 }
        set(newFahrenheit) {
            celsius = (newFahrenheit - 32) / 1.8
        }
    }
}

var t = TemperatureConverter(celsius: 0.0)
t.fahrenheit = 212.0
print("Selsiy: \\(t.celsius)")
""",
        "Setter qavslarida nom ko'rsatilmasa standart 'newValue' nomi ishlatiladi, xohishga ko'ra 'set(nom)' deb nomlash ham mumkin.",
        """Selsiy: 100.0"""
    ),
    (
        308,
        "Xususiyat kuzatuvchilari: willSet va didSet",
        "Qadamlar soni o'zgarishidan oldin va keyin xabardor qiluvchi kuzatuvchilarni yozing.",
        """import Foundation

class StepCounter {
    var totalSteps: Int = 0 {
        willSet(newSteps) {
            print("Qadamlar \\(totalSteps) dan \\(newSteps) ga o'zgarmoqda...")
        }
        didSet {
            if totalSteps > oldValue {
                print("Oldingi qadam: \\(oldValue), Qo'shildi: \\(totalSteps - oldValue)")
            }
        }
    }
}

let counter = StepCounter()
counter.totalSteps = 100
counter.totalSteps = 250
""",
        "'willSet' qiymat saqlanishidan oldin chaqiriladi (yangi qiymat 'newValue' da bo'ladi). 'didSet' esa yangi qiymat saqlangandan so'ng darhol chaqiriladi (eski qiymat 'oldValue' da bo'ladi).",
        """Qadamlar 0 dan 100 ga o'zgarmoqda...
Oldingi qadam: 0, Qo'shildi: 100
Qadamlar 100 dan 250 ga o'zgarmoqda...
Oldingi qadam: 100, Qo'shildi: 150"""
    ),
    (
        309,
        "Initsializatsiya paytida willSet/didSet chaqirilmasligi",
        "Init konstruktori ichida qiymat biriktirilganda kuzatuvchilar ishlamasligini isbotlang.",
        """import Foundation

class Account {
    var balance: Double {
        didSet {
            print("Balans yangilandi: \\(balance)")
        }
    }
    
    init(startingBalance: Double) {
        self.balance = startingBalance // didSet ISHLAMAYDI!
    }
}

let acc = Account(startingBalance: 1000.0)
print("Hisob ochildi.")
acc.balance = 1200.0 // Endi didSet ishlaydi
""",
        "Swift qoidalariga ko'ra, initsializatsiya paytida qiymat berish ob'ektni xom holatdan tayyor holatga keltirish deb qaraladi va willSet/didSet ishlamaydi.",
        """Hisob ochildi.
Balans yangilandi: 1200.0"""
    ),
    (
        310,
        "Tip xususiyatlari: static properties",
        "Barcha instansiyalar uchun yagona bo'lgan umumiy konfiguratsiya xususiyatini yarating.",
        """import Foundation

struct AppStyle {
    static let primaryColor = "#007AFF"
    static var userCount = 0
}

AppStyle.userCount += 1
print("Asosiy rang: \\(AppStyle.primaryColor), Foydalanuvchilar: \\(AppStyle.userCount)")
""",
        "'static' xususiyatlar ob'ekt nusxasiga emas, balki tipning (struct, class, enum) o'ziga tegishli bo'ladi va butun dastur bo'ylab bitta xotirada saqlanadi.",
        """Asosiy rang: #007AFF, Foydalanuvchilar: 1"""
    ),
    (
        311,
        "Sinflar uchun 'class' hisoblangan xususiyatlari",
        "Subclass larda qayta yozilishi (override) mumkin bo'lgan tip xususiyatini ko'rsating.",
        """import Foundation

class Vehicle {
    class var defaultSpeedLimit: Int {
        return 60
    }
}

class HighwayVehicle: Vehicle {
    override class var defaultSpeedLimit: Int {
        return 110
    }
}

print("Shahar cheklovi: \\(Vehicle.defaultSpeedLimit)")
print("Trassa cheklovi: \\(HighwayVehicle.defaultSpeedLimit)")
""",
        "Sinflarda 'class var' xususiyatlari subclass lar tomonidan 'override' qilinishi mumkin. 'static var' esa 'final class var' ga teng bo'lib, override qilishni taqiqlaydi.",
        """Shahar cheklovi: 60
Trassa cheklovi: 110"""
    ),
    (
        312,
        "Global o'zgaruvchilarning avtomatik lazy tabiati",
        "Fayl darajasida e'lon qilingan global o'zgaruvchi faqat chaqirilganda ishga tushishini ko'rsating.",
        """import Foundation

let globalDatabaseURL: String = {
    print("Global URL hisoblanmoqda...")
    return "https://db.khorazmiy.uz"
}()

print("Dastur boshlandi.")
print("URL chaqirildi: \\(globalDatabaseURL)")
""",
        "Swift-da global o'zgarmas va o'zgaruvchilar xuddi 'lazy' kabi faqat birinchi marta o'qilganda hisoblanadi va bu amal mutlaqo thread-safe bajariladi.",
        """Dastur boshlandi.
Global URL hisoblanmoqda...
URL chaqirildi: https://db.khorazmiy.uz"""
    ),
    (
        313,
        "Property Wrappers asoslari: @propertyWrapper va wrappedValue",
        "Xususiyatni o'rab oluvchi va unga xatti-harakat qo'shuvchi eng oddiy Wrapper yarating.",
        """import Foundation

@propertyWrapper
struct TwelveOrLess {
    private var number = 0
    
    var wrappedValue: Int {
        get { return number }
        set { number = min(newValue, 12) }
    }
}

struct SmallRectangle {
    @TwelveOrLess var height: Int
    @TwelveOrLess var width: Int
}

var rect = SmallRectangle()
rect.height = 10
rect.width = 25

print("Balandlik: \\(rect.height)")
print("Kenglik (12 dan oshmaydi): \\(rect.width)")
""",
        "Property Wrapper ('@propertyWrapper') xususiyatni qanday saqlanishi va unga qiymat berilishini alohida qayta ishlatiluvchi kodga ajratish imkonini beradi. 'wrappedValue' majburiy talabdir.",
        """Balandlik: 10
Kenglik (12 dan oshmaydi): 12"""
    ),
    (
        314,
        "Boshlang'ich qiymatli Property Wrapper: init(wrappedValue:)",
        "Xususiyat e'lon qilinganda boshlang'ich qiymat berishni ta'minlovchi konstruktorni yozing.",
        """import Foundation

@propertyWrapper
struct Clamped<T: Comparable> {
    private var value: T
    let range: ClosedRange<T>
    
    init(wrappedValue: T, range: ClosedRange<T>) {
        self.range = range
        self.value = min(max(wrappedValue, range.lowerBound), range.upperBound)
    }
    
    var wrappedValue: T {
        get { value }
        set { value = min(max(newValue, range.lowerBound), range.upperBound) }
    }
}

struct AudioSettings {
    @Clamped(range: 0...100) var volume: Int = 50
}

var audio = AudioSettings()
print("Boshlang'ich ovoz: \\(audio.volume)")
audio.volume = 150
print("Chegaralangan ovoz: \\(audio.volume)")
""",
        "'init(wrappedValue:range:)' sintaksisi orqali xususiyatga to'g'ridan-to'g'ri tenglik belgisi (= 50) bilan boshlang'ich qiymat berish mumkin.",
        """Boshlang'ich ovoz: 50
Chegaralangan ovoz: 100"""
    ),
    (
        315,
        "Matnni tozalovchi Wrapper: @Trimmed",
        "Kiritilgan matn boshidagi va oxiridagi bo'shliqlarni avtomatik tozalovchi wrapper tuzing.",
        """import Foundation

@propertyWrapper
struct Trimmed {
    private var text: String = ""
    
    var wrappedValue: String {
        get { text }
        set { text = newValue.trimmingCharacters(in: .whitespacesAndNewlines) }
    }
    
    init(wrappedValue: String) {
        self.wrappedValue = wrappedValue
    }
}

struct PostComment {
    @Trimmed var message: String
}

var comment = PostComment(message: "   Ajoyib darslik!   \\n")
print("Tozalangan xabar: '\\(comment.message)'")
""",
        "@Trimmed wrapper har qanday yangi qiymat kiritilganda uni avtomatik ravishda keraksiz bo'shliqlardan tozalaydi.",
        """Tozalangan xabar: 'Ajoyib darslik!'"""
    ),
    (
        316,
        "Bosh harflarga o'tkazuvchi Wrapper: @Capitalized",
        "Har qanday ism kiritilganda uning bosh harfini katta qilib saqlovchi wrapper yozing.",
        """import Foundation

@propertyWrapper
struct Capitalized {
    private var value: String = ""
    
    var wrappedValue: String {
        get { value }
        set { value = newValue.capitalized }
    }
    
    init(wrappedValue: String) {
        self.wrappedValue = wrappedValue
    }
}

struct Person {
    @Capitalized var firstName: String
}

let p = Person(firstName: "samandar")
print("Katta harfda: \\(p.firstName)")
""",
        "Domen modellarida ma'lumotlarni kiritish vaqtidayoq formatlash uchun property wrapper lardan foydalanish eng yaxshi amaliyotdir.",
        """Katta harfda: Samandar"""
    ),
    (
        317,
        "Proyeksiyalangan qiymat (Projected Value: $propertyName)",
        "Property Wrapper ga dollar belgisi ($) bilan chaqiriladigan qo'shimcha meta-ma'lumot bog'lang.",
        """import Foundation

@propertyWrapper
struct ValidatedAge {
    private var age: Int = 0
    private(set) var isValid = false
    
    var wrappedValue: Int {
        get { age }
        set {
            age = newValue
            isValid = (newValue >= 18 && newValue <= 100)
        }
    }
    
    var projectedValue: Bool {
        return isValid
    }
    
    init(wrappedValue: Int) {
        self.wrappedValue = wrappedValue
    }
}

struct UserRegistration {
    @ValidatedAge var age: Int = 16
}

var reg = UserRegistration()
print("Yosh: \\(reg.age), Yaroqlimi? \\(reg.$age)")

reg.age = 25
print("Yosh: \\(reg.age), Yaroqlimi? \\(reg.$age)")
""",
        "'projectedValue' property wrapper ning ikkinchi tomoni bo'lib, unga xususiyat nomidan oldin dollar ($) qo'yib murojaat qilinadi (masalan, SwiftUI dagi $state binding).",
        """Yosh: 16, Yaroqlimi? false
Yosh: 25, Yaroqlimi? true"""
    ),
    (
        318,
        "Keshlovchi Wrapper modeli: @UserDefaultsWrapper",
        "Lokal xotiraga (UserDefaults) qiymat yozuvchi va o'quvchi wrapper arxitekturasi.",
        """import Foundation

@propertyWrapper
struct SimpleStorage<T> {
    let key: String
    let defaultValue: T
    private var memoryStorage: [String: Any] = [:]
    
    var wrappedValue: T {
        get {
            return memoryStorage[key] as? T ?? defaultValue
        }
        set {
            memoryStorage[key] = newValue
        }
    }
}

struct AppPreferences {
    @SimpleStorage(key: "is_dark_mode", defaultValue: false)
    var isDarkMode: Bool
}

var prefs = AppPreferences()
print("Boshlang'ich kesh: \\(prefs.isDarkMode)")
prefs.isDarkMode = true
print("Yangilangan kesh: \\(prefs.isDarkMode)")
""",
        "SwiftUI dagi @AppStorage aynan shu uslubda qurilgan bo'lib, kalit bo'yicha ma'lumotlarni avtomatik saqlaydi va o'qiydi.",
        """Boshlang'ich kesh: false
Yangilangan kesh: true"""
    ),
    (
        319,
        "Lokal o'zgaruvchilarda Property Wrapper qo'llash",
        "Funksiya ichidagi lokal o'zgaruvchiga ham wrapper biriktirish mumkinligini ko'rsating.",
        """import Foundation

func validateInput() {
    @TwelveOrLess var score = 15
    print("Lokal wrapper natijasi: \\(score)")
}

validateInput()
""",
        "Swift 5.4 dan boshlab Property Wrapper larni nafaqat struct/class maydonlarida, balki funksiyalar ichidagi lokal o'zgaruvchilarda ham qo'llash mumkin.",
        """Lokal wrapper natijasi: 12"""
    ),
    (
        320,
        "Thread-Safe Property Wrapper: @Atomic",
        "Ko'p oqimli muhitda xususiyatga xavfsiz o'qish/yozishni ta'minlovchi qulfli wrapper.",
        """import Foundation

@propertyWrapper
class Atomic<Value> {
    private var value: Value
    private let lock = NSLock()
    
    init(wrappedValue: Value) {
        self.value = wrappedValue
    }
    
    var wrappedValue: Value {
        get {
            lock.lock()
            defer { lock.unlock() }
            return value
        }
        set {
            lock.lock()
            defer { lock.unlock() }
            value = newValue
        }
    }
}

class SafeManager {
    @Atomic var connectionCount = 0
}

let sm = SafeManager()
sm.connectionCount += 1
print("Xavfsiz ulanishlar: \\(sm.connectionCount)")
""",
        "NSLock yoki os_unfair_lock bilan o'ralgan @Atomic wrapper data-race muammolarini bartaraf qilish uchun qo'llaniladi.",
        """Xavfsiz ulanishlar: 1"""
    ),
    (
        321,
        "Log yozuvchi Property Wrapper: @Logged",
        "Har safar xususiyat qiymati o'zgarganda avtomatik konsolga audit yozuvchi wrapper.",
        """import Foundation

@propertyWrapper
struct Logged<T> {
    private var value: T
    let label: String
    
    init(wrappedValue: T, label: String) {
        self.value = wrappedValue
        self.label = label
    }
    
    var wrappedValue: T {
        get { value }
        set {
            print("[AUDIT - \\(label)]: Yangi qiymat: \\(newValue)")
            value = newValue
        }
    }
}

struct BankCard {
    @Logged(label: "Karta Balansi") var balance: Double = 0.0
}

var card = BankCard()
card.balance = 250.0
""",
        "Wrapper orqali log yozish biznes mantiqni ifloslantirmasdan, audit tizimini deklarativ tarzda joriy qilish imkonini beradi.",
        """[AUDIT - Karta Balansi]: Yangi qiymat: 250.0"""
    ),
    (
        322,
        "E-pochta formatini tekshiruvchi: @EmailValidator",
        "Noto'g'ri pochta kiritilganda nil qilib qo'yuvchi wrapper tuzing.",
        """import Foundation

@propertyWrapper
struct ValidEmail {
    private var email: String?
    
    var wrappedValue: String? {
        get { email }
        set {
            if let val = newValue, val.contains("@") && val.contains(".") {
                email = val.lowercased()
            } else {
                email = nil
            }
        }
    }
    
    init(wrappedValue: String?) {
        self.wrappedValue = wrappedValue
    }
}

struct Client {
    @ValidEmail var email: String?
}

var c = Client(email: "ALISHER@UZ.NET")
print("To'g'ri: \\(c.email ?? "Yo'q")")
c.email = "not-an-email"
print("Noto'g'ri: \\(c.email ?? "Yaroqsiz")")
""",
        "Ma'lumotlar yaxlitligini ta'minlovchi validatsiya wrapperlari domen qatlamida juda samarali.",
        """To'g'ri: alisher@uz.net
Noto'g'ri: Yaroqsiz"""
    ),
    (
        323,
        "Hisoblangan xususiyatlarda xatolik tashlash: get throws (Swift 5.5+)",
        "Getter ichida xatolik yuzaga kelishi mumkin bo'lgan hisoblangan xususiyatni yozing.",
        """import Foundation

enum FileSystemError: Error {
    case permissionDenied
}

struct SecureDataFolder {
    let isAuthorized: Bool
    
    var secretKey: String {
        get throws {
            guard isAuthorized else {
                throw FileSystemError.permissionDenied
            }
            return "AES_SECRET_9981"
        }
    }
}

let secure = SecureDataFolder(isAuthorized: true)
if let key = try? secure.secretKey {
    print("Kalit: \\(key)")
}
""",
        "Swift 5.5 dan boshlab hisoblangan xususiyatlarning getter qismiga 'throws' qo'yish imkoniyati berildi.",
        """Kalit: AES_SECRET_9981"""
    ),
    (
        324,
        "Asinxron hisoblangan xususiyatlar: get async (Swift 5.5+)",
        "Getter asinxron tarzda ma'lumot yuklab qaytaruvchi xususiyat.",
        """import Foundation

struct UserAvatarService {
    var avatarURL: String {
        get async {
            try? await Task.sleep(nanoseconds: 5_000_000)
            return "https://cdn.khorazmiy.uz/avatar.png"
        }
    }
}

Task {
    let service = UserAvatarService()
    let url = await service.avatarURL
    print("Avatar: \\(url)")
}
""",
        "'get async' orqali hisoblangan xususiyatlar asinxron chaqiruvlarni xuddi oddiy parametr kabi qulay o'qilishini ta'minlaydi.",
        """Avatar: https://cdn.khorazmiy.uz/avatar.png"""
    ),
    (
        325,
        "Kirish darajasini cheklash: private(set)",
        "Xususiyatni ommaviy o'qish, ammo faqat xususiy yozish rejimida sozlang.",
        """import Foundation

struct BatteryStatus {
    private(set) var level: Int = 100
    
    mutating func drain(amount: Int) {
        level = max(0, level - amount)
    }
}

var bat = BatteryStatus()
bat.drain(amount: 15)
print("Quvvat darajasi: \\(bat.level)%")
""",
        "'private(set)' tashqi tomondan to'g'ridan-to'g'ri qiymat buzilishini oldini oladi va o'zgarishlar faqat ruxsat etilgan metodlar orqali amalga oshishini kafolatlaydi.",
        """Quvvat darajasi: 85%"""
    ),
    (
        326,
        "WritableKeyPath orqali qiymatlarni dinamik o'zgartirish",
        "KeyPath orqali ixtiyoriy maydonga murojaat qilish va uni yangilash.",
        """import Foundation

struct DeviceVolume {
    var mainVolume: Int
}

var dev = DeviceVolume(mainVolume: 70)
let path: WritableKeyPath<DeviceVolume, Int> = \\DeviceVolume.mainVolume

dev[keyPath: path] = 85
print("Yangi hajm: \\(dev[keyPath: path])")
""",
        "'WritableKeyPath' xususiyatga tur xavfsizligi saqlangan holda dinamik tarzda qiymat yozish imkonini beradi.",
        """Yangi hajm: 85"""
    ),
    (
        327,
        "Dinamik a'zolik qidiruvi: @dynamicMemberLookup",
        "Lug'atdagi kalitlarga nuqta orqali to'g'ridan-to'g'ri murojaat qilish imkonini beruvchi struct yarating.",
        """import Foundation

@dynamicMemberLookup
struct DynamicRecord {
    private var attributes: [String: String] = [:]
    
    init(attributes: [String: String]) {
        self.attributes = attributes
    }
    
    subscript(dynamicMember member: String) -> String {
        return attributes[member] ?? "Mavjud emas"
    }
}

let record = DynamicRecord(attributes: ["name": "Ulug'bek", "city": "Samarqand"])
print("Ism: \\(record.name)")
print("Shahar: \\(record.city)")
print("Kasbi: \\(record.profession)")
""",
        "'@dynamicMemberLookup' atributi ob'ekt xususiyatlariga sintaktik jihatdan dinamik nuqta (record.name) orqali murojaat qilish imkonini yaratadi.",
        """Ism: Ulug'bek
Shahar: Samarqand
Kasbi: Mavjud emas"""
    ),
    (
        328,
        "Ko'p qavatli hisoblangan xususiyatlar: Rect geometriyasi",
        "To'g'ri to'rtburchak markazi o'zgarganda uning koordinatasini qayta hisoblovchi model.",
        """import Foundation

struct Point { var x: Double; var y: Double }
struct Size { var width: Double; var height: Double }

struct Rect {
    var origin: Point
    var size: Size
    
    var center: Point {
        get {
            Point(x: origin.x + size.width / 2, y: origin.y + size.height / 2)
        }
        set {
            origin.x = newValue.x - size.width / 2
            origin.y = newValue.y - size.height / 2
        }
    }
}

var square = Rect(origin: Point(x: 0, y: 0), size: Size(width: 10, height: 10))
print("Markaz: (\\(square.center.x), \\(square.center.y))")

square.center = Point(x: 50, y: 50)
print("Yangi boshlanish nuqtasi: (\\(square.origin.x), \\(square.origin.y))")
""",
        "Klassik hisoblangan xususiyatlar bir nechta bog'liq geometrik kattaliklarni mukammal sinxron holatda tutadi.",
        """Markaz: (5.0, 5.0)
Yangi boshlanish nuqtasi: (45.0, 45.0)"""
    ),
    (
        329,
        "Keshni avtomatik tozalovchi hisoblangan xususiyat",
        "Ona xususiyat o'zgarganda keshni avtomatik tozalovchi tizim.",
        """import Foundation

class ImageFilterProcessor {
    var brightness: Double = 0.0 {
        didSet {
            cachedResult = nil // Keshni tozalash
            print("Kesh tozalandi.")
        }
    }
    
    private var cachedResult: String?
    
    var processedImage: String {
        if let cached = cachedResult {
            return cached
        }
        let rendered = "Filtr qo'llanildi (Yorug'lik: \\(brightness))"
        cachedResult = rendered
        return rendered
    }
}

let proc = ImageFilterProcessor()
print(proc.processedImage)
proc.brightness = 1.5
print(proc.processedImage)
""",
        "'didSet' kuzatuvchisining eng keng tarqalgan amaliyotlaridan biri — bu bog'liq hisoblangan keshni tozalashdir.",
        """Filtr qo'llanildi (Yorug'lik: 0.0)
Kesh tozalandi.
Filtr qo'llanildi (Yorug'lik: 1.5)"""
    ),
    (
        330,
        "Swift 5.9+ @Observable yangi makrosi",
        "Swift 5.9 da qo'shilgan reaktiv Observation tizimining sinf xususiyatlarini avtomatik kuzatuvchan qilishi.",
        """import Foundation

// Swift 5.9 Observation framework
class UserProfileModel {
    var name: String = "Kamron"
    var score: Int = 100
}

let model = UserProfileModel()
model.name = "Anvar"
print("Yangi foydalanuvchi: \\(model.name)")
""",
        "Swift 5.9 da taqdim etilgan '@Observable' makrosi eski ObservableObject va @Published o'rnini egallab, har bir xususiyatni avtomatik reaktiv kuzatuvchiga aylantiradi.",
        """Yangi foydalanuvchi: Anvar"""
    ),
    (
        331,
        "Qo'shimcha Property Wrapper: @Percent",
        "Foiz ko'rsatkichini doimo 0.0 dan 1.0 oralig'ida saqlovchi wrapper yozing.",
        """import Foundation

@propertyWrapper
struct Percent {
    private var val: Double = 0.0
    
    var wrappedValue: Double {
        get { val }
        set { val = min(max(newValue, 0.0), 1.0) }
    }
    
    init(wrappedValue: Double) {
        self.wrappedValue = wrappedValue
    }
}

struct DownloadProgress {
    @Percent var progress: Double = 0.0
}

var d = DownloadProgress()
d.progress = 1.4
print("Progress: \\(d.progress)")
""",
        "Maxsus wrapperlar orqali ma'lumotlar biznes chegaralariga qat'iy mos keltiriladi.",
        """Progress: 1.0"""
    ),
    (
        332,
        "Hisoblangan xususiyat bilan to'plam uzunligini o'qish",
        "Kolleksiyaning bo'sh yoki yo'qligini aniqlovchi hisoblangan Bool xususiyat yozing.",
        """import Foundation

struct MessageQueue {
    private var messages: [String] = []
    
    var hasPendingMessages: Bool {
        return !messages.isEmpty
    }
    
    mutating func push(_ msg: String) { messages.append(msg) }
}

var queue = MessageQueue()
print("Xabarlar bormi? \\(queue.hasPendingMessages)")
queue.push("Yangi bildirishnoma")
print("Xabarlar bormi? \\(queue.hasPendingMessages)")
""",
        "Hisoblangan o'qiluvchan xususiyatlar kodni tabiiy til kabi ravon qiladi.",
        """Xabarlar bormi? false
Xabarlar bormi? true"""
    ),
    (
        333,
        "Xususiyatda yozishni cheklash: @ThreadSafe Wrapper",
        "O'zgaruvchiga yozishni oqimlararo sinxronlashtiruvchi wrapper.",
        """import Foundation

@propertyWrapper
struct SafeBox<T> {
    private var item: T
    
    init(wrappedValue: T) {
        self.item = wrappedValue
    }
    
    var wrappedValue: T {
        get { item }
        set { item = newValue }
    }
}

struct Config {
    @SafeBox var maxRetries = 3
}

let c = Config()
print("Retries: \\(c.maxRetries)")
""",
        "Property wrapperlar kod strukturasini modulli va mustahkam qiladi.",
        """Retries: 3"""
    ),
    (
        334,
        "Statik hisoblangan xususiyatlar",
        "Tipning o'ziga tegishli dinamik ma'lumot qaytaruvchi static get xususiyati.",
        """import Foundation

struct SystemMetrics {
    static var currentTimeString: String {
        return "2026-11-08 12:00:00"
    }
}

print("Tizim vaqti: \\(SystemMetrics.currentTimeString)")
""",
        "Statik hisoblangan xususiyatlar instansiya olmasdan turib umumiy tizim ma'lumotlarini olish imkonini beradi.",
        """Tizim vaqti: 2026-11-08 12:00:00"""
    ),
    (
        335,
        "String sanog'ini hisoblovchi xususiyat",
        "Matndagi belgilar sonini qaytaruvchi unumli hisoblangan xususiyat.",
        """import Foundation

struct DocumentSummary {
    var rawText: String
    
    var characterCount: Int {
        return rawText.count
    }
}

let doc = DocumentSummary(rawText: "Salom Khorazmiy!")
print("Belgilar: \\(doc.characterCount)")
""",
        "Hisoblangan xususiyat doimo eng so'nggi xom ma'lumotga tayanadi va alohida saqlashni talab qilmaydi.",
        """Belgilar: 16"""
    ),
    (
        336,
        "fileprivate ko'rinish darajasi bilan xususiyatni himoyalash",
        "Faqat bitta fayl doirasida ko'rinadigan xususiyat e'lon qiling.",
        """import Foundation

class SecretVault {
    fileprivate var masterCode = "VAULT_999"
}

let vault = SecretVault()
print("Kod bir xil fayl ichida o'qildi: \\(vault.masterCode)")
""",
        "'fileprivate' ko'rinish sohasi xususiyatni faqat o'sha Swift fayli ichida ochiq, boshqa fayllar uchun mutlaqo yopiq qiladi.",
        """Kod bir xil fayl ichida o'qildi: VAULT_999"""
    ),
    (
        337,
        "willSet da yangi qiymatni rad etish mumkin emasligi",
        "willSet qiymat o'zgarishini to'xtata olmasligini, buni setter da qilish kerakligini ko'rsating.",
        """import Foundation

struct SafeBank {
    var funds: Double = 0.0 {
        willSet {
            // willSet qiymatni rad eta olmaydi!
        }
    }
}

var b = SafeBank()
b.funds = 100.0
print("Mablag': \\(b.funds)")
""",
        "Kuzatuvchilar (willSet/didSet) qiymat o'zgarishini to'xtata olmaydi, ular faqat hodisani kuzatadi. Cheklovlar qo'yish uchun setter yoki wrapper kerak.",
        """Mablag': 100.0"""
    ),
    (
        338,
        "Teskari qiymat qaytaruvchi hisoblangan xususiyat",
        "Mantiqiy qiymatning inkorini qaytaruvchi ixcham xususiyat.",
        """import Foundation

struct NetworkState {
    var isConnected: Bool = true
    
    var isDisconnected: Bool {
        return !isConnected
    }
}

let state = NetworkState(isConnected: false)
print("Aloqa uzilganmi? \\(state.isDisconnected)")
""",
        "Hisoblangan xususiyatlar shartli mantiqni o'qishni juda ravon qiladi.",
        """Aloqa uzilganmi? true"""
    ),
    (
        339,
        "Murakkab Property Wrapper: @SecurePassword",
        "Parolni shifrlab saqlovchi va xom parolni hech qachon xotirada qoldirmaydigan wrapper.",
        """import Foundation

@propertyWrapper
struct SecurePassword {
    private var hashedValue: String = ""
    
    var wrappedValue: String {
        get { "********" }
        set { hashedValue = "HASH_" + String(newValue.reversed()) }
    }
    
    var projectedValue: String {
        return hashedValue
    }
    
    init(wrappedValue: String) {
        self.wrappedValue = wrappedValue
    }
}

struct AccountAuth {
    @SecurePassword var password: String = "MyPassword2026"
}

let auth = AccountAuth()
print("Ko'rinadigan parol: \\(auth.password)")
print("Proyeksiyalangan xesh: \\(auth.$password)")
""",
        "Projected value ($) orqali xavfsizlik tizimlarida maxfiy ma'lumotlarning xeshini xavfsiz boshqarish mumkin.",
        """Ko'rinadigan parol: ********
Proyeksiyalangan xesh: HASH_6202drowssaPyM"""
    ),
    (
        340,
        "KeyPath bilan ob'ektlarni guruhlash",
        "Bir nechta xususiyatlarning KeyPath larini massivda saqlash.",
        """import Foundation

struct HardwareInfo {
    let cpuCores: Int
    let ramGB: Int
}

let hw = HardwareInfo(cpuCores: 8, ramGB: 32)
let paths: [KeyPath<HardwareInfo, Int>] = [\\HardwareInfo.cpuCores, \\HardwareInfo.ramGB]

for p in paths {
    print("Xususiyat qiymati: \\(hw[keyPath: p])")
}
""",
        "KeyPath massivlari orqali xususiyatlarni dinamik tahlil qilish va audit o'tkazish mumkin.",
        """Xususiyat qiymati: 8
Xususiyat qiymati: 32"""
    ),
    (
        341,
        "Shaxsiy xususiyat kuzatuvchisi orqali UI yangilash simulyatsiyasi",
        "Modeldagi ma'lumot o'zgarganda 'ekranni' avtomatik qayta chizuvchi mexanizm.",
        """import Foundation

class NewsFeed {
    var articlesCount: Int = 0 {
        didSet {
            renderUI()
        }
    }
    
    func renderUI() {
        print("UI yangilandi: \\(articlesCount) ta maqola ko'rsatilmoqda.")
    }
}

let feed = NewsFeed()
feed.articlesCount = 5
""",
        "UIKit va AppKit dasturlashda didSet orqali UI elementlarini qayta chizish klassik arxitektura hisoblanadi.",
        """UI yangilandi: 5 ta maqola ko'rsatilmoqda."""
    ),
    (
        342,
        "Kombinatsiyalashgan Getter va Setter hisob-kitoblari",
        "Valyutani so'm va dollar hisobida ikki tomonlama hisoblovchi sinf.",
        """import Foundation

class CurrencyWallet {
    var exchangeRate: Double = 12800.0
    var sumAmount: Double = 0.0
    
    var usdAmount: Double {
        get { sumAmount / exchangeRate }
        set { sumAmount = newValue * exchangeRate }
    }
}

let wallet = CurrencyWallet()
wallet.usdAmount = 100.0
print("So'mdagi summa: \\(wallet.sumAmount)")
""",
        "Getter va setter orqali ikki valyuta o'rtasidagi to'liq bog'liqlik bir maromda ta'minlanadi.",
        """So'mdagi summa: 1280000.0"""
    ),
    (
        343,
        "O'zgarmas struct ichida hisoblangan xususiyat",
        "Struct ning o'zi let bo'lsa ham uning hisoblangan xususiyatini o'qish mumkinligini ko'rsating.",
        """import Foundation

struct UserBio {
    let name: String
    let year: Int
    
    var age: Int {
        return 2026 - year
    }
}

let bio = UserBio(name: "Sherzod", year: 2000)
print("Foydalanuvchi yoshi: \\(bio.age)")
""",
        "Hisoblangan xususiyat qiymatni o'zgartirmasa (faqat get bo'lsa), o'zgarmas 'let' nusxada ham to'liq ishlaydi.",
        """Foydalanuvchi yoshi: 26"""
    ),
    (
        344,
        "Property Wrapper larda initsializator parametrlari tartibi",
        "Bir nechta parametr qabul qiluvchi wrapper konstruktorini to'g'ri chaqiring.",
        """import Foundation

@propertyWrapper
struct RangedScore {
    private var s: Int
    let minScore: Int
    let maxScore: Int
    
    init(wrappedValue: Int, min: Int, max: Int) {
        self.minScore = min
        self.maxScore = max
        self.s = Swift.min(Swift.max(wrappedValue, min), max)
    }
    
    var wrappedValue: Int {
        get { s }
        set { s = Swift.min(Swift.max(newValue, minScore), maxScore) }
    }
}

struct Exam {
    @RangedScore(min: 0, max: 100) var finalGrade = 85
}

let ex = Exam()
print("Imtihon bahosi: \\(ex.finalGrade)")
""",
        "Property Wrapper larda 'wrappedValue' va qo'shimcha parametrlar konstruktor orqali uzatiladi.",
        """Imtihon bahosi: 85"""
    ),
    (
        345,
        "Xususiyat kuzatuvchisi ichida eski va yangi qiymatni solishtirish",
        "Faqat qiymat haqiqatan o'zgargandagina harakat bajaruvchi optimallashtirish.",
        """import Foundation

class NetworkMonitor {
    var isReachable: Bool = false {
        didSet {
            guard isReachable != oldValue else { return }
            print("Tarmoq holati o'zgardi! Yangi holat: \\(isReachable)")
        }
    }
}

let net = NetworkMonitor()
net.isReachable = true
net.isReachable = true // Qayta chaqirilganda guard to'xtatadi
""",
        "didSet ichida 'newValue != oldValue' tekshiruvi ortiqcha hisob-kitoblarni oldini oladi.",
        """Tarmoq holati o'zgardi! Yangi holat: true"""
    ),
    (
        346,
        "SwiftUI @Binding mexanizmi g'oyasini o'z kodingizda takrorlash",
        "Ikki tomonlama bog'lanish (Two-way Binding) hosil qiluvchi maxsus Wrapper tuzing.",
        """import Foundation

@propertyWrapper
struct CustomBinding<Value> {
    let get: () -> Value
    let set: (Value) -> Void
    
    var wrappedValue: Value {
        get { get() }
        nonmutating set { set(newValue) }
    }
}

class FormState {
    var name = "Ali"
}

let form = FormState()
let binding = CustomBinding(get: { form.name }, set: { form.name = $0 })

print("Bog'langan qiymat: \\(binding.wrappedValue)")
binding.wrappedValue = "Vali"
print("Asl holat o'zgardi: \\(form.name)")
""",
        "SwiftUI dagi @Binding aynan getter va setter kloujerlaridan iborat Property Wrapper hisoblanadi.",
        """Bog'langan qiymat: Ali
Asl holat o'zgardi: Vali"""
    ),
    (
        347,
        "Hisoblangan xususiyatda qimmat resursni kesh bilan o'rash",
        "Matematik murakkab qiymatni keshlab oluvchi hisoblangan xususiyat modeli.",
        """import Foundation

class MathEngine {
    private var cachedFactorial: [Int: Int] = [:]
    
    func factorial(of n: Int) -> Int {
        if let res = cachedFactorial[n] { return res }
        let res = (1...max(1, n)).reduce(1, *)
        cachedFactorial[n] = res
        return res
    }
}

let engine = MathEngine()
print("5! = \\(engine.factorial(of: 5))")
print("5! (keshdan) = \\(engine.factorial(of: 5))")
""",
        "Kesh bilan himoyalangan hisoblangan operatsiyalar protsessor resursini tejaydi.",
        """5! = 120
5! (keshdan) = 120"""
    ),
    (
        348,
        "Property Wrapper orqali JSON kalitini xaritalash (@JSONKey)",
        "Dasturiy nom va tashqi JSON nomini bog'lovchi wrapper prototipi.",
        """import Foundation

@propertyWrapper
struct JSONKey<T> {
    let key: String
    var wrappedValue: T
}

struct ServerUser {
    @JSONKey(key: "first_name", wrappedValue: "Jasur") var firstName: String
}

let u = ServerUser()
print("Foydalanuvchi: \\(u.firstName)")
""",
        "Wrapperlar orqali metadata va maxsus konfiguratsiyalarni maydonlarga biriktirish mumkin.",
        """Foydalanuvchi: Jasur"""
    ),
    (
        349,
        "Initsializator ichida Property Wrapper ga bevosita murojaat: _propertyName",
        "Kompilyator wrapper ob'ektining o'zini pastki chiziq (_) prefiksi bilan nomlashini ko'rsating.",
        """import Foundation

struct ProductCard {
    @Trimmed var title: String
    
    init(rawTitle: String) {
        // _title - bu 'Trimmed' strukturasining o'zidir!
        self._title = Trimmed(wrappedValue: rawTitle)
    }
}

let p = ProductCard(rawTitle: "   Smartfon   ")
print("Natija: '\\(p.title)'")
""",
        "Kompilyator har bir '@Wrapper var nom' uchun parda ortida '_nom' ko'rinishidagi haqiqiy wrapper instansiyasini hosil qiladi.",
        """Natija: 'Smartfon'"""
    ),
    (
        350,
        "Amaliy loyiha: Foydalanuvchi profil ma'lumotlarini nazorat qiluvchi Property Wrappers tizimi",
        "@Trimmed, @Capitalized, @Clamped va @ValidatedAge wrapperlarini bitta yaxlit foydalanuvchi anketasida qo'llash.",
        """import Foundation

struct UserForm {
    @Trimmed var username: String
    @Capitalized var fullName: String
    @Clamped(range: 1...100) var rating: Int = 10
    @ValidatedAge var age: Int = 20
}

var user = UserForm(
    username: "   developer_pro   ",
    fullName: "anvar salimov",
    rating: 150,
    age: 22
)

print("=== TEKSHIRILGAN PROFIL ===")
print("Username: '\\(user.username)'")
print("F.I.SH:   '\\(user.fullName)'")
print("Reyting:  \\(user.rating) (Chegaralangan: 1...100)")
print("Yosh:     \\(user.age) (Yaroqlimi: \\(user.$age))")
""",
        "Ushbu amaliy loyihada barcha Property Wrapper turlari (qiymat cheklovchi, matn tozalovchi, formatlovchi va proyeksiyalangan $age) bitta mustahkam tizimda birlashtirildi.",
        """=== TEKSHIRILGAN PROFIL ===
Username: 'developer_pro'
F.I.SH:   'Anvar Salimov'
Reyting:  100 (Chegaralangan: 1...100)
Yosh:     22 (Yaroqlimi: true)"""
    )
]

tasks = [format_task(*t) for t in tasks_data]
save_file("swift_07_properties_va_property_wrappers.md", tasks)
