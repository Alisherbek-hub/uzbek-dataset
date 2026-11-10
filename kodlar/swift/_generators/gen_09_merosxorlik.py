# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks_data = [
    (
        401,
        "Merosxo'rlik asoslari (Subclassing): Ota va bola sinf",
        "Asosiy 'Person' sinfidan 'Student' sinfini meros qilib oling va qo'shimcha xususiyat qo'shing.",
        """import Foundation

class Person {
    var name: String
    init(name: String) { self.name = name }
    
    func introduce() {
        print("Salom, mening ismim \\(name).")
    }
}

class Student: Person {
    var studentID: String
    
    init(name: String, studentID: String) {
        self.studentID = studentID
        super.init(name: name)
    }
}

let s = Student(name: "Kamola", studentID: "STU-8821")
s.introduce()
print("ID raqami: \\(s.studentID)")
""",
        "Swift-da sinflar boshqa sinfdan meros (inherit) olishi mumkin. Bola sinf (subclass) ota sinfning (superclass) barcha metodlari va xususiyatlariga ega bo'ladi.",
        """Salom, mening ismim Kamola.
ID raqami: STU-8821"""
    ),
    (
        402,
        "Swift-da umumiy ildiz sinf yo'qligi (Root Class)",
        "Boshqa tillardan (masalan, Java yoki C#) farqli o'laroq, Swift sinflari hech qanday standart ota sinfsiz mustaqil yaratilishini ko'rsating.",
        """import Foundation

class IndependentEntity {
    var identifier = UUID()
}

let entity = IndependentEntity()
print("Mustaqil ob'ekt yaratildi: \\(entity.identifier)")
""",
        "Swift-da barcha sinflar uchun umumiy bo'lgan bitta ildiz klass (masalan, Java Object) yo'q. Agar ota sinf ko'rsatilmasa, sinf mustaqil 'Base Class' (baza sinfi) hisoblanadi.",
        """Mustaqil ob'ekt yaratildi: UUID"""
    ),
    (
        403,
        "Metodlarni qayta yozish: override func",
        "Ota sinfdagi ovoz chiqarish metodini bola sinfda maxsuslashtiring.",
        """import Foundation

class Animal {
    func makeSound() {
        print("Hayvon umumiy tovush chiqarmoqda.")
    }
}

class Cat: Animal {
    override func makeSound() {
        print("Miyov-miyov!")
    }
}

let cat = Cat()
cat.makeSound()
""",
        "Ota sinfdan meros olingan metodni o'zgartirish uchun 'override' kalit so'zi yoziladi. Kompilyator ota sinfda aynan shunday metod mavjudligini qat'iy tekshiradi.",
        """Miyov-miyov!"""
    ),
    (
        404,
        "Ota sinf metodini chaqirish: super.metod()",
        "Ota sinfning asl metodini to'liq o'chirib yubormay, unga qo'shimcha xatti-harakat qo'shing.",
        """import Foundation

class Printer {
    func printDocument() {
        print("Hujjat qog'ozga chop etilmoqda.")
    }
}

class ColorPrinter: Printer {
    override func printDocument() {
        print("[Rangli kartridj faollashtirildi]")
        super.printDocument() // Ota sinf metodini chaqirish
    }
}

let cp = ColorPrinter()
cp.printDocument()
""",
        "'super.metod()' orqali ota sinfdagi original mantiqni chaqirib, uning ustiga yangi imkoniyatlar qo'shish mumkin.",
        """[Rangli kartridj faollashtirildi]
Hujjat qog'ozga chop etilmoqda."""
    ),
    (
        405,
        "Xususiyatlarni (Properties) override qilish",
        "Ota sinf xususiyatining getter va setterini subclass da kengaytiring.",
        """import Foundation

class Car {
    var currentSpeed: Double = 0.0
    var description: String {
        return "Tezlik: \\(currentSpeed) km/soat"
    }
}

class Supercar: Car {
    override var description: String {
        return super.description + " (Sport rejimi yoqilgan)"
    }
}

let sc = Supercar()
sc.currentSpeed = 280.0
print(sc.description)
""",
        "Subclass ota sinfdan meros olingan hisoblangan yoki saqlanuvchi xususiyatlarning getter va setterlarini override qilishi mumkin.",
        """Tezlik: 280.0 km/soat (Sport rejimi yoqilgan)"""
    ),
    (
        406,
        "Xususiyat kuzatuvchilarini (Property Observers) override qilish",
        "Ota sinfdagi oddiy saqlanuvchi xususiyatga bola sinfda didSet kuzatuvchisini qo'shing.",
        """import Foundation

class ProgressTracker {
    var percent: Int = 0
}

class LoggingTracker: ProgressTracker {
    override var percent: Int {
        didSet {
            print("LOG: Jarayon \\(percent)% ga yetdi.")
        }
    }
}

let tracker = LoggingTracker()
tracker.percent = 50
tracker.percent = 100
""",
        "Subclass ota sinf maydoniga o'zining shaxsiy 'willSet' yoki 'didSet' kuzatuvchisini biriktirishi mumkin.",
        """LOG: Jarayon 50% ga yetdi.
LOG: Jarayon 100% ga yetdi."""
    ),
    (
        407,
        "Subscript larni override qilish",
        "Ota sinfdagi massiv subscriptini bola sinfda xavfsizroq formatda qayta yozing.",
        """import Foundation

class NumberContainer {
    var items = [10, 20, 30]
    subscript(index: Int) -> Int {
        return items[index]
    }
}

class MultipliedContainer: NumberContainer {
    override subscript(index: Int) -> Int {
        return super[index] * 10
    }
}

let mc = MultipliedContainer()
print("Indeks 1 qiymati: \\(mc[1])")
""",
        "Subscript-lar ham oddiy metodlar kabi subclass larda 'override subscript' orqali modifikatsiya qilinadi.",
        """Indeks 1 qiymati: 200"""
    ),
    (
        408,
        "Qayta yozishni taqiqlash: final kalit so'zi",
        "Sinf, metod yoki xususiyatni meros olinishi va override qilinishidan butunlay himoyalang.",
        """import Foundation

class SecurityGateway {
    final func verifyCertificate() -> Bool {
        return true
    }
}

final class FixedValidator: SecurityGateway {
    // override func verifyCertificate() // XATO: Cannot override final method
}

// class ExtendedValidator: FixedValidator // XATO: Cannot inherit from final class

let validator = FixedValidator()
print("Sertifikat holati: \\(validator.verifyCertificate())")
""",
        "'final' kalit so'zi sinfning meros olinishini, yoki alohida metod/xususiyatning override qilinishini taqiqlaydi. Bu xavfsizlikni oshiradi va Static Dispatch tufayli dasturni tezlashtiradi.",
        """Sertifikat holati: true"""
    ),
    (
        409,
        "Tipni tekshirish operatori: is",
        "Kolleksiyadagi ob'ektlarning qaysi subclass ga tegishli ekanligini 'is' orqali tekshiring.",
        """import Foundation

class MediaItem {
    let title: String
    init(title: String) { self.title = title }
}

class Movie: MediaItem {
    let director: String
    init(title: String, director: String) { self.director = director; super.init(title: title) }
}

class Song: MediaItem {
    let artist: String
    init(title: String, artist: String) { self.artist = artist; super.init(title: title) }
}

let library: [MediaItem] = [
    Movie(title: "Inception", director: "Nolan"),
    Song(title: "Billie Jean", artist: "Jackson")
]

var movieCount = 0
for item in library {
    if item is Movie { movieCount += 1 }
}
print("Filmlar soni: \\(movieCount)")
""",
        "'is' operatori ob'ekt ko'rsatilgan sinfga yoki uning vorisiga tegishli ekanligini tekshiradi va Bool natija beradi.",
        """Filmlar soni: 1"""
    ),
    (
        410,
        "Pastga xavfsiz quyish: as?",
        "Ota sinf ko'rsatkichini bola sinf turiga 'as?' orqali xavfsiz o'giring.",
        """import Foundation

let media: MediaItem = Movie(title: "Interstellar", director: "Nolan")

if let movie = media as? Movie {
    print("Film nomi: \\(movie.title), Rejissyor: \\(movie.director)")
}

if let song = media as? Song {
    print("Qo'shiq: \\(song.artist)")
} else {
    print("Bu musiqa emas, film!")
}
""",
        "'as?' operatori (Conditional Downcasting) ob'ektni bola sinf turiga aylantirishga urinadi, agar mos kelmasa dastur halokatiga yo'l qo'ymay 'nil' qaytaradi.",
        """Film nomi: Interstellar, Rejissyor: Nolan
Bu musiqa emas, film!"""
    ),
    (
        411,
        "Majburiy pastga quyish: as!",
        "Turi 100% aniq bo'lgan holatda 'as!' bilan tezkor ochish.",
        """import Foundation

let item: MediaItem = Song(title: "Imagine", artist: "John Lennon")
let definiteSong = item as! Song

print("Ijrochi: \\(definiteSong.artist)")
""",
        "'as!' operatori majburiy quyishni amalga oshiradi. Agar ob'ekt kutilgan sinfga tegishli bo'lmasa, dastur Run-Time Crash beradi.",
        """Ijrochi: John Lennon"""
    ),
    (
        412,
        "Yuqoriga quyish: as (Upcasting)",
        "Bola sinf ob'ektini ota sinf turi sifatida qabul qiling.",
        """import Foundation

let specificMovie = Movie(title: "Avatar", director: "Cameron")
let generalizedMedia: MediaItem = specificMovie as MediaItem

print("Umumiy media: \\(generalizedMedia.title)")
""",
        "Bola sinf doimo ota sinfning to'liq imkoniyatlarini o'z ichiga olganligi sababli, yuqoriga quyish (upcasting) 100% xavfsiz va kafolatlangan amaldir.",
        """Umumiy media: Avatar"""
    ),
    (
        413,
        "Polimorfizm amaliyotda (Polymorphism in Action)",
        "Bitta umumiy ota sinf massivida turli xil voris ob'ektlarning o'z xatti-harakatlarini chaqiring.",
        """import Foundation

class GraphicElement {
    func render() { print("Umumiy grafik chizildi.") }
}

class ButtonElement: GraphicElement {
    override func render() { print("Tugma (Button) chizildi.") }
}

class TextFieldElement: GraphicElement {
    override func render() { print("Kiritish maydoni (TextField) chizildi.") }
}

let canvas: [GraphicElement] = [ButtonElement(), TextFieldElement(), ButtonElement()]

for element in canvas {
    element.render()
}
""",
        "Polimorfizm — bu bir xil interfeys (render) orqali turli sinf ob'ektlarining o'ziga xos xatti-harakatlarini namoyish etish qobiliyatidir.",
        """Tugma (Button) chizildi.
Kiritish maydoni (TextField) chizildi.
Tugma (Button) chizildi."""
    ),
    (
        414,
        "Dinamik jo'natish (Dynamic Dispatch) va VTable",
        "Swift ish vaqtida qaysi metodni chaqirishni Virtual Method Table orqali qanday aniqlashini ko'rsating.",
        """import Foundation

class BaseCalculator {
    func compute(a: Int, b: Int) -> Int { a + b }
}

class MultiplyCalculator: BaseCalculator {
    override func compute(a: Int, b: Int) -> Int { a * b }
}

func executeCalculation(calc: BaseCalculator, x: Int, y: Int) {
    // VTable orqali ish vaqtida haqiqiy compute tanlanadi:
    print("Natija: \\(calc.compute(a: x, b: y))")
}

executeCalculation(calc: BaseCalculator(), x: 4, y: 5)
executeCalculation(calc: MultiplyCalculator(), x: 4, y: 5)
""",
        "Dinamik jo'natish (Dynamic Dispatch) ish vaqtida ob'ektning haqiqiy turini aniqlab, uning VTable jadvalidagi mos funksiya manziliga o'tadi.",
        """Natija: 9
Natija: 20"""
    ),
    (
        415,
        "Ko'p bosqichli merosxo'rlik zanjiri (Grandparent -> Parent -> Child)",
        "Uch qavatli sinf ierarxiyasida xususiyatlar va metodlarning to'planishini ko'rsating.",
        """import Foundation

class Organism {
    let isAlive = true
}

class Mammal: Organism {
    let hasWarmBlood = true
}

class Dolphin: Mammal {
    let canSwim = true
}

let dolphin = Dolphin()
print("Tirikmi? \\(dolphin.isAlive)")
print("Issiq qonlimi? \\(dolphin.hasWarmBlood)")
print("Suzadimi? \\(dolphin.canSwim)")
""",
        "Bola sinf o'zidan yuqoridagi barcha ota va bobo sinflarning xususiyatlarini to'liq meros qilib oladi.",
        """Tirikmi? true
Issiq qonlimi? true
Suzadimi? true"""
    ),
    (
        416,
        "Abstrakt sinf simulyatsiyasi (fatalError bilan)",
        "Swift-da 'abstract' kalit so'zi yo'qligini va uni qanday xavfsiz simulyatsiya qilishni ko'rsating.",
        """import Foundation

class AbstractDatabase {
    func connect() {
        fatalError("Bu metod subclass lar tomonidan override qilinishi shart!")
    }
}

class PostgreSQLDatabase: AbstractDatabase {
    override func connect() {
        print("PostgreSQL serveriga muvaffaqiyatli ulandi.")
    }
}

let db = PostgreSQLDatabase()
db.connect()
""",
        "Swift-da 'abstract' so'zi yo'q. Dasturchilar ota sinfda 'fatalError' qo'yish orqali voris sinflarga metodni override qilish majburiyatini yuklaydilar (yoki protokollar qo'llashadi).",
        """PostgreSQL serveriga muvaffaqiyatli ulandi."""
    ),
    (
        417,
        "open vs public kirish darajalari",
        "Boshqa modullarda meros olish imkoniyatini beruvchi 'open' va cheklovchi 'public' farqini tushuntiring.",
        """import Foundation

// O'z moduli doirasida:
open class FrameworkBase {
    open func customizableBehavior() {
        print("Boshqa modulda ham override qilinishi mumkin.")
    }
    
    public func fixedBehavior() {
        print("Boshqa modulda faqat chaqiriladi, override qilinmaydi.")
    }
}

let fw = FrameworkBase()
fw.customizableBehavior()
fw.fixedBehavior()
""",
        "'open' — eng yuqori ruxsat darajasi bo'lib, unga boshqa modullar (masalan, framework) dan turib ham subclassing qilish va metodlarini override qilish mumkin. 'public' esa faqat foydalanishga ruxsat beradi, subclassingni taqiqlaydi.",
        """Boshqa modulda ham override qilinishi mumkin.
Boshqa modulda faqat chaqiriladi, override qilinmaydi."""
    ),
    (
        418,
        "Dinamik Self tipi: Self",
        "Metod o'zi chaqirilgan aniq bola sinf turini qaytarishi uchun 'Self' dan foydalaning.",
        """import Foundation

class CopyableClass {
    required init() {}
    
    func clone() -> Self {
        return type(of: self).init()
    }
}

class SubCopyable: CopyableClass {}

let original = SubCopyable()
let duplicate = original.clone()

print("Klon turi to'g'rimi? \\(type(of: duplicate) == SubCopyable.self)")
""",
        "Katta harfli 'Self' joriy ob'ektning aniq dinamik turini ifodalaydi va metodlar zanjirida aniq turni saqlab qolish imkonini beradi.",
        """Klon turi to'g'rimi? true"""
    ),
    (
        419,
        "Template Method Pattern merosxo'rlikda",
        "Algoritm skeletini ota sinfda belgilab, aniq bosqichlarni subclass larga qoldiring.",
        """import Foundation

class ReportGenerator {
    func generate() {
        gatherData()
        formatReport()
        export()
    }
    
    func gatherData() { print("1. Ma'lumotlar yig'ildi.") }
    func formatReport() { print("2. Standart matn formati berildi.") }
    func export() { print("3. Fayl saqlandi.") }
}

class PDFReportGenerator: ReportGenerator {
    override func formatReport() {
        print("2. [PDF] Maxsus vizual PDF sahifalash formati qo'llanildi.")
    }
}

let pdf = PDFReportGenerator()
pdf.generate()
""",
        "Template Method naqshida ota sinf butun jarayon oqimini nazorat qiladi, bola sinflar esa alohida qadamlarni moslashtiradi.",
        """1. Ma'lumotlar yig'ildi.
2. [PDF] Maxsus vizual PDF sahifalash formati qo'llanildi.
3. Fayl saqlandi."""
    ),
    (
        420,
        "Strategy Pattern sinflar polimorfizmi orqali",
        "To'lov strategiyasini polimorfik sinflar orqali dinamik almashtiring.",
        """import Foundation

class PaymentStrategy {
    func pay(amount: Double) {
        print("$\\(amount) to'landi.")
    }
}

class CreditCardPayment: PaymentStrategy {
    override func pay(amount: Double) {
        print("Bank kartasi orqali $\\(amount) yechildi.")
    }
}

class CryptoPayment: PaymentStrategy {
    override func pay(amount: Double) {
        print("Kriptovalyuta orqali $\\(amount) to'landi.")
    }
}

class Checkout {
    var strategy: PaymentStrategy
    init(strategy: PaymentStrategy) { self.strategy = strategy }
    func completePurchase(amount: Double) { strategy.pay(amount: amount) }
}

let cart = Checkout(strategy: CreditCardPayment())
cart.completePurchase(amount: 150.0)
cart.strategy = CryptoPayment()
cart.completePurchase(amount: 150.0)
""",
        "Strategy Pattern orqali xatti-harakatlar sinflarga ajratiladi va ular ish vaqtida qulay almashtiriladi.",
        """Bank kartasi orqali $150.0 yechildi.
Kriptovalyuta orqali $150.0 to'landi."""
    ),
    (
        421,
        "Kompozitsiya vs Merosxo'rlik (Composition over Inheritance)",
        "Merosxo'rlik o'rniga komponentlarni birlashtirish orqali afzallikni ko'rsating.",
        """import Foundation

class GPSModule {
    func getCoordinates() -> String { "41.2995, 69.2401" }
}

class CameraModule {
    func takePhoto() -> String { "FOTO_DATA" }
}

class Smartphone {
    let gps = GPSModule()
    let camera = CameraModule()
}

let phone = Smartphone()
print("GPS: \\(phone.gps.getCoordinates())")
print("Kamera: \\(phone.camera.takePhoto())")
""",
        "'Composition over Inheritance' tamoyili qat'iy sinflar daraxtidan ko'ra, kichik mustaqil qismlarni ob'ekt ichiga yig'ishni tavsiya qiladi.",
        """GPS: 41.2995, 69.2401
Kamera: FOTO_DATA"""
    ),
    (
        422,
        "Liskov Almashtirish Qoidasi (LSP - SOLID)",
        "Ota sinf kutilyotgan joyga ixtiyoriy subclass ni tizim buzilmasdan qo'yish mumkinligini isbotlang.",
        """import Foundation

class NotificationSender {
    func send(text: String) {
        print("Xabarnoma: \\(text)")
    }
}

class PushSender: NotificationSender {
    override func send(text: String) {
        print("[APNS Push]: \\(text)")
    }
}

func broadcast(sender: NotificationSender) {
    sender.send(text: "Yangi yangilanish mavjud!")
}

broadcast(sender: NotificationSender())
broadcast(sender: PushSender())
""",
        "LSP qoidasiga ko'ra, har qanday subclass o'z ota sinfi o'rnida kutilmagan nojo'ya ta'sirlarsiz to'liq ishlay olishi shart.",
        """Xabarnoma: Yangi yangilanish mavjud!
[APNS Push]: Yangi yangilanish mavjud!"""
    ),
    (
        423,
        "Statik vs Klass metodlarini override qilish",
        "Sinflarda 'static func' override qilib bo'lmasligi, 'class func' esa ruxsat etilishini ko'rsating.",
        """import Foundation

class ServerHost {
    class func serverType() -> String { "Umumiy Host" }
    static func defaultPort() -> Int { 80 }
}

class CloudHost: ServerHost {
    override class func serverType() -> String { "Bulutli Host" }
    // override static func defaultPort() // XATO: Cannot override static method
}

print(ServerHost.serverType())
print(CloudHost.serverType())
""",
        "'class func' dinamik jo'natishga ega bo'lib, subclass tomonidan override qilinishi mumkin. 'static func' esa yakuniy (final) hisoblanadi.",
        """Umumiy Host
Bulutli Host"""
    ),
    (
        424,
        "Devirtualization va final class optimizatsiyasi",
        "final sinflarda kompilyator VTable ni butunlay o'chirib Direct Call ga o'tishini tushuntiring.",
        """import Foundation

final class HighSpeedCalculator {
    func add(_ a: Int, _ b: Int) -> Int { a + b }
}

let calc = HighSpeedCalculator()
print("Devirtualized natija: \\(calc.add(10, 20))")
""",
        "'final' sinfda metodlar override qilinmasligi kafolatlanganligi bois, Swift LLVM optimizatori 'Devirtualization' amalini bajaradi va chaqiruvlarni to'g'ridan-to'g'ri manzilga ulaydi.",
        """Devirtualized natija: 30"""
    ),
    (
        425,
        "Dinamik turni aniqlash: type(of:)",
        "Ota sinf ko'rsatkichi ortidagi haqiqiy klass nomini chop eting.",
        """import Foundation

class BaseBox {}
class SpecialBox: BaseBox {}

let b: BaseBox = SpecialBox()
print("O'zgaruvchi deklaratsiya turi: BaseBox")
print("Haqiqiy dinamik turi: \\(type(of: b))")
""",
        "'type(of:)' funksiyasi ish vaqtida ob'ektning Heap-dagi haqiqiy metama'lumotini tekshirib aniq turini ko'rsatadi.",
        """O'zgaruvchi deklaratsiya turi: BaseBox
Haqiqiy dinamik turi: SpecialBox"""
    ),
    (
        426,
        "Xatoliklarni boshqarishda Polimorfizm: Throwing metodlarni override qilish",
        "Subclass ota sinfdagi throwing metodni xatosiz non-throwing qilib override qilishi mumkinligini ko'rsating.",
        """import Foundation

class RemoteService {
    func execute() throws -> String { "Remote javob" }
}

class LocalMockService: RemoteService {
    override func execute() -> String { // throws olib tashlandi, bu xavfsizroq!
        return "Mock javob"
    }
}

let mock = LocalMockService()
let result = mock.execute() // try talab qilinmaydi!
print(result)
""",
        "Subclass ota sinfdagi throwing metodni non-throwing qilib toraytirishi mumkin (chunki bu chaqiruvchi uchun xavfsizroq), ammo aksincha qila olmaydi.",
        """Mock javob"""
    ),
    (
        427,
        "NSObject va Objective-C bilan merosxo'rlik",
        "Apple tizim kutubxonalari bilan ishlashda NSObject dan meros olish.",
        """import Foundation

class AppleCompatibleBridge: NSObject {
    @objc func ping() -> String {
        return "PONG_OBJC"
    }
}

let bridge = AppleCompatibleBridge()
print("Bridge javobi: \\(bridge.ping())")
""",
        "Foundation-ning ko'plab eski UIKit/AppKit drayverlari bilan ishlash uchun 'NSObject' asosiy sinfidan meros olish talab etiladi.",
        """Bridge javobi: PONG_OBJC"""
    ),
    (
        428,
        "Merosxo'rlik zanjirida Deinit nazorati",
        "Uch qavatli ierarxiyada resurslar tozalanishini kuzating.",
        """import Foundation

class LayerA { deinit { print("LayerA tozalandi") } }
class LayerB: LayerA { deinit { print("LayerB tozalandi") } }
class LayerC: LayerB { deinit { print("LayerC tozalandi") } }

do {
    let _ = LayerC()
}
""",
        "Deinit har doim eng pastki boladan boshlanib eng yuqori otagacha tartib bilan ishlaydi.",
        """LayerC tozalandi
LayerB tozalandi
LayerA tozalandi"""
    ),
    (
        429,
        "Polimorfik massivni filtrlash: compactMap va as?",
        "Media to'plamidan faqat filmlarni ajratib oling.",
        """import Foundation

let mixedMedia: [MediaItem] = [
    Movie(title: "Matrix", director: "Wachowskis"),
    Song(title: "Yesterday", artist: "Beatles"),
    Movie(title: "Gladiator", director: "Scott")
]

let allMovies = mixedMedia.compactMap { $0 as? Movie }
print("Filmlar soni: \\(allMovies.count)")
for m in allMovies {
    print("- \\(m.title)")
}
""",
        "'compactMap { $0 as? T }' polimorfik massivdan aniq bir subclass nusxalarini saralab olishning eng qisqa va qulay usulidir.",
        """Filmlar soni: 2
- Matrix
- Gladiator"""
    ),
    (
        430,
        "Ota sinf xususiyatiga yangi qiymat berish va super.init",
        "Merosxo'rlikda ota maydonni to'g'ri o'zgartirish tartibi.",
        """import Foundation

class AccountBase {
    var currency: String
    init(currency: String) { self.currency = currency }
}

class VIPAccount: AccountBase {
    init() {
        super.init(currency: "USD")
    }
}

let vip = VIPAccount()
print("Valyuta: \\(vip.currency)")
""",
        "Ikki bosqichli initsializatsiya qoidasiga binoan, ota maydonlarni o'zgartirish faqat super.init() chaqirilgandan keyin ruxsat etiladi.",
        """Valyuta: USD"""
    ),
    (
        431,
        "Merosxo'rlikda private vs fileprivate a'zolar",
        "Subclass ota sinfning 'private' a'zolariga to'g'ridan-to'g'ri kira olmasligini ko'rsating.",
        """import Foundation

class BankVault {
    private var internalCode = "SECRET"
    fileprivate var securityLevel = 5
}

class SubVault: BankVault {
    func printLevel() {
        // print(internalCode) // XATO: 'internalCode' is inaccessible due to 'private' protection level
        print("Xavfsizlik darajasi: \\(securityLevel)")
    }
}

let sv = SubVault()
sv.printLevel()
""",
        "'private' xususiyat hatto subclass uchun ham butunlay yopiq bo'ladi. 'fileprivate' esa bitta fayl ichidagi subclass larga ochiq bo'ladi.",
        """Xavfsizlik darajasi: 5"""
    ),
    (
        432,
        "Class Cluster Pattern (Sinflar klasteri)",
        "Ota sinf konstruktori yoki fabrikasi orqali tegishli maxsus subclass larni qaytarish.",
        """import Foundation

class UITheme {
    class func theme(for isNight: Bool) -> UITheme {
        return isNight ? DarkTheme() : LightTheme()
    }
    func backgroundColor() -> String { "Oq" }
}

class LightTheme: UITheme {
    override func backgroundColor() -> String { "Oq" }
}

class DarkTheme: UITheme {
    override func backgroundColor() -> String { "Qora" }
}

let activeTheme = UITheme.theme(for: true)
print("Fon rangi: \\(activeTheme.backgroundColor())")
""",
        "Class Cluster naqshida tashqi kod yagona ota interfeys bilan muloqot qiladi, parda ortida esa kerakli aniq subclass ishlaydi.",
        """Fon rangi: Qora"""
    ),
    (
        433,
        "Polimorfizm orqali hisoblash logikasi",
        "Turli ishchilarning oylik maoshini polimorfik hisoblash moduli.",
        """import Foundation

class Worker {
    let name: String
    init(name: String) { self.name = name }
    func calculateSalary() -> Double { 0.0 }
}

class SalariedWorker: Worker {
    let monthly: Double
    init(name: String, monthly: Double) {
        self.monthly = monthly
        super.init(name: name)
    }
    override func calculateSalary() -> Double { monthly }
}

class HourlyWorker: Worker {
    let hours: Double
    let rate: Double
    init(name: String, hours: Double, rate: Double) {
        self.hours = hours; self.rate = rate
        super.init(name: name)
    }
    override func calculateSalary() -> Double { hours * rate }
}

let staff: [Worker] = [
    SalariedWorker(name: "Anvar", monthly: 3000.0),
    HourlyWorker(name: "Bobur", hours: 160, rate: 15.0)
]

for w in staff {
    print("\\(w.name) maoshi: $\\(w.calculateSalary())")
}
""",
        "Polimorfizm orqali yangi ishchi turlarini qo'shish mavjud hisoblash kodini o'zgartirmasdan osonlikcha amalga oshiriladi (Open-Closed Principle).",
        """Anvar maoshi: $3000.0
Bobur maoshi: $2400.0"""
    ),
    (
        434,
        "Polimorfizm bilan UI hodisalarini tarqatish",
        "Hodisalar (Events) ierarxiyasini polimorfik boshqaruvchi tizim.",
        """import Foundation

class AppEvent {
    let timestamp = Date()
    func logEvent() { print("Umumiy hodisa yuz berdi.") }
}

class LoginEvent: AppEvent {
    let username: String
    init(username: String) { self.username = username }
    override func logEvent() { print("Tizimga kirish: \\(username)") }
}

let events: [AppEvent] = [LoginEvent(username: "bekzod_01")]
events.first?.logEvent()
""",
        "Hodisalar ierarxiyasi tahlil va audit tizimlarida keng qo'llaniladi.",
        """Tizimga kirish: bekzod_01"""
    ),
    (
        435,
        "Override metod parametrlarining mosligi",
        "Subclass metod parametrlari va qaytish turi ota sinf bilan to'liq mos bo'lishi shartligini ko'rsating.",
        """import Foundation

class ServiceBase {
    func handle(command: String) -> Bool {
        return true
    }
}

class SecureService: ServiceBase {
    override func handle(command: String) -> Bool {
        print("Xavfsizlik tekshiruvi: \\(command)")
        return super.handle(command: command)
    }
}

let s = SecureService()
_ = s.handle(command: "PING")
""",
        "Metod imzosi (signature) to'liq mos kelmagan holda 'override' yozilsa kompilyator xato beradi.",
        """Xavfsizlik tekshiruvi: PING"""
    ),
    (
        436,
        "Merosxo'rlikda xususiyat getteri orqali ota qiymatni modifikatsiya qilish",
        "Ota sinf matnini katta harflarda qaytaruvchi subclass getteri.",
        """import Foundation

class PlainMessage {
    var text: String
    init(text: String) { self.text = text }
}

class UppercaseMessage: PlainMessage {
    override var text: String {
        get { super.text.uppercased() }
        set { super.text = newValue }
    }
}

let msg = UppercaseMessage(text: "salom do'stlar")
print(msg.text)
""",
        "Hisoblangan xususiyat ota sinfning saqlanuvchi xususiyatini o'rab olib yangi format berishi mumkin.",
        """SALOM DO'STLAR"""
    ),
    (
        437,
        "Merosxo'rlikda konstruktor delegatsiyasi zanjiri",
        "Ota va bola initsializatorlari ketma-ketligini tahlil qilish.",
        """import Foundation

class RootItem {
    var id: Int
    init(id: Int) {
        self.id = id
        print("RootItem initsializatsiya qilindi.")
    }
}

class SubItem: RootItem {
    var tag: String
    init(id: Int, tag: String) {
        self.tag = tag
        super.init(id: id)
        print("SubItem initsializatsiya qilindi.")
    }
}

let _ = SubItem(id: 1, tag: "TAG_A")
""",
        "Konstruktorlar zanjirida maydonlar xavfsiz to'ldirilib, nazorat ierarxiya bo'yicha yuqoriga uzatiladi.",
        """RootItem initsializatsiya qilindi.
SubItem initsializatsiya qilindi."""
    ),
    (
        438,
        "Subclass da yangi metodlar va ota sinf metodlarini uyg'unlashtirish",
        "Ota sinfdan kelgan tayyor imkoniyatlarga qo'shimcha yangi metodlar qo'shish.",
        """import Foundation

class BasicMath {
    func add(_ a: Int, _ b: Int) -> Int { a + b }
}

class AdvancedMath: BasicMath {
    func power(_ base: Int, _ exponent: Int) -> Int {
        var res = 1
        for _ in 0..<exponent { res *= base }
        return res
    }
}

let am = AdvancedMath()
print("Qo'shish: \\(am.add(3, 4))")
print("Daraja: \\(am.power(2, 3))")
""",
        "Merosxo'rlik mavjud kodni qayta ishlatish (code reuse) va uni yangi metodlar bilan boyitishning qulay vositasidir.",
        """Qo'shish: 7
Daraja: 8"""
    ),
    (
        439,
        "Merosxo'rlikda maydonlar nomining to'qnashuvi (Name Shadowing)",
        "Bola sinfda ota sinfdagi nom bilan bir xil xususiyat e'lon qilib bo'lmasligi va uni override qilish shartligi.",
        """import Foundation

class BaseBoxItem {
    var weight: Double = 1.0
}

class HeavyBoxItem: BaseBoxItem {
    override var weight: Double {
        get { super.weight * 2.0 }
        set { super.weight = newValue }
    }
}

let hb = HeavyBoxItem()
print("Og'irlik: \\(hb.weight) kg")
""",
        "Swift bir xil nomli yangi maydon e'lon qilishni taqiqlaydi; uni faqat 'override' orqali o'zgartirish mumkin.",
        """Og'irlik: 2.0 kg"""
    ),
    (
        440,
        "Polimorfizm va Kortejlar kombinatsiyasi",
        "Har xil sinf obyektlarini juftlikda qabul qilib qayta ishlash.",
        """import Foundation

let pair: (MediaItem, MediaItem) = (
    Movie(title: "Dunyo", director: "Rejissyor"),
    Song(title: "Kuy", artist: "Bastakor")
)

print("1-element filmmi? \\(pair.0 is Movie)")
print("2-element qo'shiqmi? \\(pair.1 is Song)")
""",
        "Kortejlar va kolleksiyalar polimorfik sinflarni tur xavfsizligi saqlangan holda birga olib yurish imkonini beradi.",
        """1-element filmmi? true
2-element qo'shiqmi? true"""
    ),
    (
        441,
        "Merosxo'rlik zanjirida ob'ekt hajmining o'sishi",
        "Har bir subclass yangi maydonlar qo'shishi bilan xotiradagi hajm kengayishini tushuntiring.",
        """import Foundation

class BaseSmall { var a: Int = 1 }
class MediumChild: BaseSmall { var b: Int = 2 }
class LargeChild: MediumChild { var c: Int = 3 }

let l = LargeChild()
print("Barcha qatlamlar ma'lumotlari: \\(l.a), \\(l.b), \\(l.c)")
""",
        "Sinflar Heap-da ota sinf xususiyatlari bilan birga o'z maydonlarini yagona yaxlit xotira blokida saqlaydi.",
        """Barcha qatlamlar ma'lumotlari: 1, 2, 3"""
    ),
    (
        442,
        "Merosxo'rlikda final metod chaqiruvining tezligi",
        "Kompilyator final metodlarga VTable orqali emas, to'g'ridan-to'g'ri chaqiruv qo'yishini ko'rsatish.",
        """import Foundation

class CalculationCore {
    final func computeFast() -> Int {
        return 42 * 2
    }
}

let core = CalculationCore()
print("Tezkor hisoblash: \\(core.computeFast())")
""",
        "Final kalit so'zi Dynamic Dispatch xarajatlarini nolga tushiradi.",
        """Tezkor hisoblash: 84"""
    ),
    (
        443,
        "Polimorfizm orqali JSON serializatsiyasi",
        "Turli modellar umumiy ota sinf interfeysi orqali lug'atga o'girilishi.",
        """import Foundation

class ExportableEntity {
    func toDictionary() -> [String: Any] {
        return ["type": "generic"]
    }
}

class UserExport: ExportableEntity {
    let name: String
    init(name: String) { self.name = name }
    override func toDictionary() -> [String: Any] {
        return ["type": "user", "name": name]
    }
}

let list: [ExportableEntity] = [UserExport(name: "Ali")]
print("Eksport: \\(list.first?.toDictionary() ?? [:])")
""",
        "Polimorfik eksport modullari tizimni yangi ma'lumot turlari uchun juda moslashuvchan qiladi.",
        """Eksport: ["name": "Ali", "type": "user"]"""
    ),
    (
        444,
        "Merosxo'rlikda do'stona metodlar arxitekturasi",
        "Ota sinf yordamchi metodlarini subclass larga xizmat qilishi.",
        """import Foundation

class BaseValidator {
    func checkNotEmpty(_ text: String) -> Bool {
        return !text.isEmpty
    }
}

class FormValidator: BaseValidator {
    func validateForm(name: String, email: String) -> Bool {
        return checkNotEmpty(name) && checkNotEmpty(email)
    }
}

let fv = FormValidator()
print("Forma to'g'rimi? \\(fv.validateForm(name: "Ali", email: "ali@uz.net"))")
""",
        "Umumiy validatsiya qoidalari ota sinfda jamlanishi kod takrorlanishini keskin kamaytiradi.",
        """Forma to'g'rimi? true"""
    ),
    (
        445,
        "Polimorfizm va switch-case bilan tiplarni ajratish",
        "Baza sinfi massividagi ob'ektlarni switch-case pattern matching orqali tahlil qilish.",
        """import Foundation

let items: [MediaItem] = [
    Movie(title: "Interstellar", director: "Nolan"),
    Song(title: "Yesterday", artist: "Beatles")
]

for item in items {
    switch item {
    case let movie as Movie:
        print("Film: '\\(movie.title)', Rejissyor: \\(movie.director)")
    case let song as Song:
        print("Qo'shiq: '\\(song.title)', Ijrochi: \\(song.artist)")
    default:
        print("Noma'lum media")
    }
}
""",
        "Switch-case da 'case let x as Subclass' pattern matchingi tiplarni ajratishning eng toza usullaridan biridir.",
        """Film: 'Interstellar', Rejissyor: Nolan
Qo'shiq: 'Yesterday', Ijrochi: Beatles"""
    ),
    (
        446,
        "Merosxo'rlikda ota va bola metodlarini parametrlari orqali overloading qilish",
        "Subclass da ota sinfdagi bilan bir xil nomli, ammo har xil parametrli yangi metod yozish (override emas!).",
        """import Foundation

class BaseLogger {
    func log(_ msg: String) { print("[BASE]: \\(msg)") }
}

class ExtendedLogger: BaseLogger {
    func log(_ msg: String, tag: String) {
        print("[\\(tag)]: \\(msg)")
    }
}

let el = ExtendedLogger()
el.log("Oddiy xabar")
el.log("Tizimli xabar", tag: "INFO")
""",
        "Agar metod parametrlari har xil bo'lsa, bu 'override' emas, balki 'overloading' hisoblanadi va 'override' so'zi yozilmaydi.",
        """[BASE]: Oddiy xabar
[INFO]: Tizimli xabar"""
    ),
    (
        447,
        "Merosxo'rlikda ota sinfning lazy xususiyatlariga munosabat",
        "Subclass ota sinfdagi lazy maydonga murojaat qilganda uning qanday initsializatsiya bo'lishi.",
        """import Foundation

class ParentService {
    lazy var data = "Og'ir ma'lumotlar"
}

class ChildService: ParentService {}

let cs = ChildService()
print("Data: \\(cs.data)")
""",
        "Lazy xususiyatlar ham oddiy saqlanuvchi xususiyatlar kabi meros olinadi va birinchi murojaatda hisoblanadi.",
        """Data: Og'ir ma'lumotlar"""
    ),
    (
        448,
        "Merosxo'rlikda konstruktorlar polimorfizmi",
        "Required initsializator orqali istalgan subclass instansiyasini dinamik yaratish.",
        """import Foundation

class VehicleFactory {
    required init() {}
    func drive() { print("Harakatlanmoqda...") }
}

class TruckFactory: VehicleFactory {
    override func drive() { print("Yuk mashinasi yuk tashimoqda...") }
}

func createAndDrive(factoryType: VehicleFactory.Type) {
    let instance = factoryType.init()
    instance.drive()
}

createAndDrive(factoryType: TruckFactory.self)
""",
        "'T.Type' metatipi va 'required init' birgalikda to'liq polimorfik ob'ektlar fabrikasini yaratishga imkon beradi.",
        """Yuk mashinasi yuk tashimoqda..."""
    ),
    (
        449,
        "Merosxo'rlikda xotiradan to'g'ri o'chirilishni kafolatlash",
        "Polimorfik havola orqali o'chirilganda ham butun ierarxiya tozalanishi.",
        """import Foundation

class ResA { deinit { print("ResA deinit") } }
class ResB: ResA { deinit { print("ResB deinit") } }

do {
    let _: ResA = ResB()
}
""",
        "Swift-da C++ dan farqli ravishda barcha deinitializatorlar avtomatik virtualdir; ota sinf ko'rsatkichi orqali ham bola sinf to'liq tozalanadi.",
        """ResB deinit
ResA deinit"""
    ),
    (
        450,
        "Amaliy loyiha: Polimorfik transport logistika tizimi",
        "Base Vehicle, Truck, CargoPlane va Drone sinflaridan iborat, yuk hajmini hisoblovchi, marshrut belgilovchi va VTable orqali dinamik jo'natiluvchi to'liq logistika moduli.",
        """import Foundation

class TransportVehicle {
    let model: String
    let maxCapacityKg: Double
    
    init(model: String, maxCapacityKg: Double) {
        self.model = model
        self.maxCapacityKg = maxCapacityKg
    }
    
    func dispatchDelivery(destination: String, cargoWeight: Double) -> Bool {
        guard cargoWeight <= maxCapacityKg else {
            print("RAD ETILDI: '\\(model)' yuk ko'tara olmaydi! (Maks: \\(maxCapacityKg) kg, So'ralgan: \\(cargoWeight) kg)")
            return false
        }
        print("LOGISTIKA: '\\(model)' \\(destination) shahriga \\(cargoWeight) kg yuk bilan jo'natildi.")
        return true
    }
}

class FreightTruck: TransportVehicle {
    let trailerCount: Int
    init(model: String, capacity: Double, trailers: Int) {
        self.trailerCount = trailers
        super.init(model: model, maxCapacityKg: capacity)
    }
    
    override func dispatchDelivery(destination: String, cargoWeight: Double) -> Bool {
        print("[Avtotrassa marshruti rejalashtirilmoqda...]")
        return super.dispatchDelivery(destination: destination, cargoWeight: cargoWeight)
    }
}

class CargoPlane: TransportVehicle {
    let flightCode: String
    init(model: String, capacity: Double, flightCode: String) {
        self.flightCode = flightCode
        super.init(model: model, maxCapacityKg: capacity)
    }
    
    override func dispatchDelivery(destination: String, cargoWeight: Double) -> Bool {
        print("[Aviatsiya havo koridori tasdiqlandi: \\(flightCode)]")
        return super.dispatchDelivery(destination: destination, cargoWeight: cargoWeight)
    }
}

class DeliveryDrone: TransportVehicle {
    override func dispatchDelivery(destination: String, cargoWeight: Double) -> Bool {
        print("[Avtonom dron GPS traektoriyasini chizmoqda...]")
        return super.dispatchDelivery(destination: destination, cargoWeight: cargoWeight)
    }
}

let fleet: [TransportVehicle] = [
    FreightTruck(model: "MAN TGS", capacity: 20000.0, trailers: 1),
    CargoPlane(model: "Boeing 747F", capacity: 100000.0, flightCode: "HY-CARGO-9"),
    DeliveryDrone(model: "AirDrop-X", capacity: 5.0)
]

print("=== LOGISTIKA MARKAZI DISPETCHERI ===")
_ = fleet[0].dispatchDelivery(destination: "Samarqand", cargoWeight: 15000.0)
_ = fleet[1].dispatchDelivery(destination: "Frankfurt", cargoWeight: 85000.0)
_ = fleet[2].dispatchDelivery(destination: "Toshkent City", cargoWeight: 12.0) // Og'ir yuk, rad etiladi!
""",
        "Ushbu yakuniy loyihada merosxo'rlik, metodlarni override qilish, super chaqiruvlari, polimorfizm va xavfsizlik chegaralari to'liq qamrab olindi.",
        """=== LOGISTIKA MARKAZI DISPETCHERI ===
[Avtotrassa marshruti rejalashtirilmoqda...]
LOGISTIKA: 'MAN TGS' Samarqand shahriga 15000.0 kg yuk bilan jo'natildi.
[Aviatsiya havo koridori tasdiqlandi: HY-CARGO-9]
LOGISTIKA: 'Boeing 747F' Frankfurt shahriga 85000.0 kg yuk bilan jo'natildi.
[Avtonom dron GPS traektoriyasini chizmoqda...]
RAD ETILDI: 'AirDrop-X' yuk ko'tara olmaydi! (Maks: 5.0 kg, So'ralgan: 12.0 kg)"""
    )
]

tasks = [format_task(*t) for t in tasks_data]
save_file("swift_09_merosxorlik_va_polimorfizm.md", tasks)
