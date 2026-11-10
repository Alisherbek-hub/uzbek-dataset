# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks_data = [
    (
        751,
        "Data Race nima va multithreading muammolari",
        "Bir vaqtda ikki oqim bitta xotiraga yozishga uringanda ma'lumotlar buzilishini tushuntiring.",
        """import Foundation

class UnsafeCounter {
    var count = 0
    func increment() { count += 1 }
}

print("Klassik sinflarda bir nechta oqim bir vaqtda increment() qilsa, Data Race (poyga) yuzaga keladi.")
""",
        "Data Race — bu ikki yoki undan ortiq parallel oqimlar aynan bir vaqtda bitta xotira manziliga murojaat qilganda va ulardan kamida bittasi yozish (write) amalini bajarganda yuzaga keladigan og'ir xatodir.",
        """Klassik sinflarda bir nechta oqim bir vaqtda increment() qilsa, Data Race (poyga) yuzaga keladi."""
    ),
    (
        752,
        "Actor kalit so'zi va Actor modeli",
        "O'z ichki holatini avtomatik himoyalovchi birinchi Actor turini yarating.",
        """import Foundation

actor SafeCounter {
    private var count = 0
    
    func increment() -> Int {
        count += 1
        return count
    }
}

Task {
    let counter = SafeCounter()
    let current = await counter.increment()
    print("Xavfsiz hisob: \\(current)")
}
""",
        "Swift-da 'actor' havola turi (Reference Type) bo'lib, xuddi class kabi ishlaydi, ammo o'zining ichki holatiga faqat bitta oqim bir vaqtning o'zida kirishini kafolatlaydi.",
        """Xavfsiz hisob: 1"""
    ),
    (
        753,
        "Actor Isolation: Majburiy await",
        "Actor a'zolariga tashqaridan murojaat qilganda kompilyator 'await' ni nima uchun talab qilishini ko'rsating.",
        """import Foundation

actor BankVault {
    var goldBars = 50
    func inspectVault() -> Int { goldBars }
}

Task {
    let vault = BankVault()
    // goldBars to'g'ridan-to'g'ri o'qilmaydi, faqat await bilan:
    let bars = await vault.inspectVault()
    print("Ombordagi oltinlar soni: \\(bars)")
}
""",
        "Actor tashqarisidan uning metod yoki xususiyatlariga murojaat qilinganda navbat kutish (suspension point) bo'lishi mumkin. Shu sababli 'await' yozilishi shartdir.",
        """Ombordagi oltinlar soni: 50"""
    ),
    (
        754,
        "Actor Reentrancy muammosi",
        "Actor ichida await bo'lgan paytda boshqa vazifa kirib holatni o'zgartirishi mumkinligini tushuntiring.",
        """import Foundation

actor ImageDownloader {
    private var cache: [String: String] = [:]
    
    func getImage(url: String) async -> String {
        if let cached = cache[url] { return cached }
        // To'xtatish nuqtasi: bu paytda boshqa so'rov ham kelishi mumkin!
        try? await Task.sleep(nanoseconds: 5_000_000)
        let downloaded = "RASM_DATA_\\(url)"
        cache[url] = downloaded
        return downloaded
    }
}

Task {
    let downloader = ImageDownloader()
    print(await downloader.getImage(url: "cat.png"))
}
""",
        "Actor Reentrancy: Actor metodida 'await' to'xtatish nuqtasi bo'lsa, kutish davomida actor boshqa chaqiruvlarni qabul qilishi mumkin. Shu bois await dan keyin holat o'zgarmagan deb ko'r-ko'rona ishonmaslik kerak.",
        """RASM_DATA_cat.png"""
    ),
    (
        755,
        "nonisolated kalit so'zi",
        "Actor ichida sinxron va oqimni to'xtatmaydigan, o'zgarmas ma'lumotlarni await siz o'qish.",
        """import Foundation

actor ServerNode {
    let nodeID: String // O'zgarmas 'let' maydon
    var activeConnections = 0
    
    init(id: String) { self.nodeID = id }
    
    nonisolated func getNodeIdentifier() -> String {
        return "Node: \\(nodeID)"
    }
}

let node = ServerNode(id: "TOSHKENT_01")
// nonisolated metodni 'await' siz to'g'ridan-to'g'ri chaqirish mumkin:
print(node.getNodeIdentifier())
""",
        "'nonisolated' deb belgilangan metodlar actor ning umumiy navbatiga tushmasdan to'g'ridan-to'g'ri sinxron chaqiriladi. Ular faqat o'zgarmas (immutable) 'let' maydonlar bilan ishlay oladi.",
        """Node: TOSHKENT_01"""
    ),
    (
        756,
        "Global Actors va @MainActor",
        "Foydalanuvchi interfeysini (UI) boshqaruvchi asosiy oqim xavfsizligi.",
        """import Foundation

@MainActor
class ProfileViewModel {
    var title = "Bosh Sahifa"
    
    func updateTitle(_ newTitle: String) {
        self.title = newTitle
        print("UI asosiy oqimda yangilandi: \\(title)")
    }
}

Task { @MainActor in
    let vm = ProfileViewModel()
    vm.updateTitle("Yangi Profil")
}
""",
        "'@MainActor' barcha UI o'zgarishlari va metodlarning faqat va faqat operatsion tizimning Asosiy Oqimida (Main Thread) xavfsiz bajarilishini kafolatlaydi.",
        """UI asosiy oqimda yangilandi: Yangi Profil"""
    ),
    (
        757,
        "MainActor.run { ... } orqali asosiy oqimga sakrash",
        "Fonda ishlayotgan vazifadan turib UI ga tezkor ma'lumot yetkazish.",
        """import Foundation

Task.detached {
    // Fondagi og'ir hisoblash
    let computedData = 42 * 10
    
    await MainActor.run {
        print("Asosiy oqimda UI ga berildi: \\(computedData)")
    }
}
""",
        "'MainActor.run' ixtiyoriy fon oqimidan turib asosiy oqimda (Main Thread) qisqa kod blokini xavfsiz bajarish imkonini beradi.",
        """Asosiy oqimda UI ga berildi: 420"""
    ),
    (
        758,
        "Maxsus Global Actor yaratish: @globalActor",
        "O'z shaxsiy global oqim izolyatsiyasini hosil qilish.",
        """import Foundation

@globalActor
actor DatabaseActor {
    static let shared = DatabaseActor()
}

@DatabaseActor
class DatabaseController {
    func performQuery() {
        print("Baza so'rovi DatabaseActor umumiy oqimida bajarildi.")
    }
}

Task {
    let db = DatabaseController()
    await db.performQuery()
}
""",
        "'@globalActor' butun ilova bo'ylab turli sinf va funksiyalarni bitta umumiy maxsus oqimda (actor) sinxronlashtirish imkonini beradi.",
        """Baza so'rovi DatabaseActor umumiy oqimida bajarildi."""
    ),
    (
        759,
        "Sendable protokoli asoslari",
        "Oqimlar orasida erkin uzatilishi xavfsiz bo'lgan ma'lumot turlarini ko'rsating.",
        """import Foundation

struct UserTelemetry: Sendable {
    let id: Int
    let eventName: String
}

let telem = UserTelemetry(id: 1, eventName: "APP_LAUNCH")
print("Sendable turi oqimlararo xavfsiz: \\(telem.eventName)")
""",
        "'Sendable' protokoli — bu qiymat o'zgaruvchanlikdan xoli bo'lib, parallel oqimlar orasida poyga xatolarisiz uzatilishi mumkinligini tasdiqlovchi shartnomadir.",
        """Sendable turi oqimlararo xavfsiz: APP_LAUNCH"""
    ),
    (
        760,
        "Qaysi tiplar avtomatik Sendable hisoblanadi",
        "Value types, o'zgarmas turlar va Actor larning tabiiy Sendable tabiati.",
        """import Foundation

// 1. Struct (agar barcha maydonlari Sendable bo'lsa) avtomatik Sendable
struct Point: Sendable { let x: Double; let y: Double }

// 2. Enum avtomatik Sendable
enum Direction: Sendable { case north, south }

// 3. Har qanday Actor o'z ichki holatini himoya qilgani sababli avtomatik Sendable
actor Worker: Sendable {}

print("Barcha uch tur tabiiy ravishda oqimlararo xavfsizdir.")
""",
        "Qiymat turlari (Value types) to'liq nusxalanishi tufayli, Actor lar esa ichki himoyasi tufayli tabiiy ravishda Sendable hisoblanadi.",
        """Barcha uch tur tabiiy ravishda oqimlararo xavfsizdir."""
    ),
    (
        761,
        "Qaysi tiplar Sendable EMAS",
        "Oddiy sinflar nima sababdan Sendable bo'la olmasligini ko'rsating.",
        """import Foundation

class SharedUser {
    var name = "Ali"
}

// let user = SharedUser()
// Parallel oqimga bu sinfni uzatish Swift 6 da QAT'IY XATOLIK!
print("Oddiy sinflar (mutable reference types) Sendable emas, chunki ular poyga (Data Race) keltirib chiqaradi.")
""",
        "O'zgaruvchan maydonli oddiy sinflar parallel oqimlar orasida xavfsiz emas, chunki ikkala oqim ham bir vaqtda uning xotirasini buzishi mumkin.",
        """Oddiy sinflar (mutable reference types) Sendable emas, chunki ular poyga (Data Race) keltirib chiqaradi."""
    ),
    (
        762,
        "@Sendable Closures qoidalari",
        "Parallel oqimga uzatiladigan kloujer tashqi o'zgaruvchan qiymatlarni o'zgartira olmasligi.",
        """import Foundation

var mutableNumber = 10

let sendableClosure: @Sendable (Int) -> Int = { x in
    // mutableNumber += 1 // XATO: Mutation of captured var in a '@Sendable' closure
    return x * 2
}

print("Hisob: \\(sendableClosure(5))")
""",
        "'@Sendable' closure faqat o'zgarmas nusxalarni (let) capture qila oladi, tashqi 'var' o'zgaruvchilarni mutatsiyaga uchratish taqiqlanadi.",
        """Hisob: 10"""
    ),
    (
        763,
        "@unchecked Sendable va qo'lda qulf (Lock) bilan himoya",
        "Ichki NSLock orqali qo'lda himoyalangan sinfni kompilyatorga @unchecked Sendable deb bildirish.",
        """import Foundation

final class ManualThreadSafeBox: @unchecked Sendable {
    private var value: Int = 0
    private let lock = NSLock()
    
    func add() {
        lock.lock()
        defer { lock.unlock() }
        value += 1
    }
    
    func get() -> Int {
        lock.lock()
        defer { lock.unlock() }
        return value
    }
}

let box = ManualThreadSafeBox()
box.add()
print("Qulf orqali qiymat: \\(box.get())")
""",
        "'@unchecked Sendable' dasturchi kompilyatorga: 'Men bu sinfni ichida NSLock orqali o'zim to'liq xavfsiz qilganman, ogohlantirish berma' deb kafolat berishidir.",
        """Qulf orqali qiymat: 1"""
    ),
    (
        764,
        "Swift 6 Complete Concurrency tekshiruvi",
        "Swift 6 da barcha global o'zgaruvchilar va ma'lumotlar oqimi kompilyatsiya vaqtida qat'iy tekshirilishi.",
        """import Foundation

// Swift 6 da global o'zgaruvchi faqat let yoki MainActor ga tegishli bo'lishi shart:
@MainActor var globalUIState = "Tayyor"

print("Swift 6 ma'lumotlar poygasini to'liq kompilyatsiya vaqtida yo'q qiladi.")
""",
        "Swift 6 ning asosiy maqsadi — 'Data-race safety by default'. Dastur ishga tushmasdan turib, kompilyatsiya vaqtidayoq barcha ko'p oqimli xatolar qizil chiziq bilan to'xtatiladi.",
        """Swift 6 ma'lumotlar poygasini to'liq kompilyatsiya vaqtida yo'q qiladi."""
    ),
    (
        765,
        "Actor bilan Bank hisobi (Bank Account Actor)",
        "Pul yechish va to'ldirishni to'liq data-race xavfisiz boshqaruvchi klassik Actor.",
        """import Foundation

actor BankAccount {
    private(set) var balance: Double
    
    init(opening: Double) { self.balance = opening }
    
    func deposit(amount: Double) {
        balance += amount
    }
    
    func withdraw(amount: Double) -> Bool {
        guard balance >= amount else { return false }
        balance -= amount
        return true
    }
}

Task {
    let account = BankAccount(opening: 500.0)
    await account.deposit(amount: 200.0)
    let ok = await account.withdraw(amount: 100.0)
    print("Muvaffaqiyatli: \\(ok), Balans: $\\(await account.balance)")
}
""",
        "Bir vaqtning o'zida yuzlab oqimlar pul yechishga urinsa ham, Actor ularni birma-bir navbat bilan bajarib balans buzilishini 100% oldini oladi.",
        """Muvaffaqiyatli: true, Balans: $600.0"""
    ),
    (
        766,
        "Actor bilan Kesh boshqaruvchisi (ImageCache Actor)",
        "Rasmlarni parallel oqimlarda xavfsiz keshlovchi Actor.",
        """import Foundation

actor ImageCache {
    private var storage: [String: String] = [:]
    
    func cache(image: String, forKey key: String) {
        storage[key] = image
    }
    
    func image(forKey key: String) -> String? {
        return storage[key]
    }
}

Task {
    let cache = ImageCache()
    await cache.cache(image: "FOTO_1", forKey: "avatar")
    print("Keshdan olindi: \\(await cache.image(forKey: "avatar") ?? "")")
}
""",
        "Lug'at (Dictionary) ko'p oqimda xavfli bo'lganligi bois, uni Actor ichiga o'rash orqali xavfsiz yuqori unumli kesh yaratiladi.",
        """Keshdan olindi: FOTO_1"""
    ),
    (
        767,
        "Actor larda deinit va sinxron tozalash",
        "Actor deinit bloki sinxron bo'lib, unda await talab qilinmasligini ko'rsating.",
        """import Foundation

actor TempWorker {
    let id: Int
    init(id: Int) { self.id = id }
    
    deinit {
        // deinit doimo nonisolated va sinxron ishlaydi!
        print("TempWorker #\\(id) xotiradan tozalandi.")
    }
}

do {
    let _ = TempWorker(id: 101)
}
""",
        "Actor-ning deinitializatori ob'ekt xotiradan o'chirilayotgan paytda boshqa hech kim unga murojaat qila olmasligi kafolatlanganligi bois nonisolated tarzda ishlaydi.",
        """TempWorker #101 xotiradan tozalandi."""
    ),
    (
        768,
        "Actor larda initsializatsiya paytida await talab etilmasligi",
        "Konstruktor ichida actor isolation hali kuchga kirmaganligi sababli to'g'ridan-to'g'ri qiymat berish.",
        """import Foundation

actor DeviceSession {
    var status: String
    
    init(initialStatus: String) {
        // Bu yerda await shart emas, chunki ob'ekt hali tashqi dunyoga ochilmagan:
        self.status = initialStatus
    }
}

let session = DeviceSession(initialStatus: "Boshlandi")
print("Actor xavfsiz initsializatsiya qilindi.")
""",
        "Initsializatsiya vaqtida 'self' hali faqat bitta oqim qo'lida bo'ladi, shu bois xususiyatlar to'g'ridan-to'g'ri o'rnatiladi.",
        """Actor xavfsiz initsializatsiya qilindi."""
    ),
    (
        769,
        "Actor va Protokol mosligi (Actor Protocol Conformance)",
        "Actor ga protokolni biriktirish va uning metodlarini bajarish.",
        """import Foundation

protocol StatusProvider {
    func getStatus() async -> String
}

actor ServiceEngine: StatusProvider {
    func getStatus() async -> String {
        return "ONLINE"
    }
}

Task {
    let engine: any StatusProvider = ServiceEngine()
    print("Servis holati: \\(await engine.getStatus())")
}
""",
        "Actor protokol talablarini qabul qilishi mumkin, bunda protokol metodlari asinxron ('async') deb e'lon qilinishi maqsadga muvofiqdir.",
        """Servis holati: ONLINE"""
    ),
    (
        770,
        "Thread Sanitizer (TSan) bilan xavfsizlik kafolati",
        "Xcode da Thread Sanitizer vositasi qanday qilib poyga holatlarini ushlashini tushuntiring.",
        """import Foundation

print("Xcode Thread Sanitizer (TSan) ish vaqtida parallel oqimlar o'rtasidagi har qanday ruxsatsiz xotira to'qnashuvini aniqlab beradi.")
""",
        "TSan kompilyatorga xotira murojaatlarini kuzatuvchi kod qo'shadi va Swift Concurrency qoidalariga rioya etilishini amalda tasdiqlaydi.",
        """Xcode Thread Sanitizer (TSan) ish vaqtida parallel oqimlar o'rtasidagi har qanday ruxsatsiz xotira to'qnashuvini aniqlab beradi."""
    ),
    (
        771,
        "Logging Actor: Faylga navbat bilan yozuvchi audit mexanizmi",
        "Log xabarlarini tartib bilan, bir-biriga xalaqit bermasdan yozuvchi Actor.",
        """import Foundation

actor FileLogger {
    private var logs: [String] = []
    
    func log(_ message: String) {
        logs.append("[\\(Date())]: \\(message)")
        print("LOG YOZILDI: \\(message)")
    }
}

Task {
    let logger = FileLogger()
    await logger.log("Foydalanuvchi tizimga kirdi")
    await logger.log("So'rov yakunlandi")
}
""",
        "Logging Actor barcha oqimlardan kelayotgan xabarlarni xavfsiz navbatga qo'yib, log fayllari buzilishini oldini oladi.",
        """LOG YOZILDI: Foydalanuvchi tizimga kirdi
LOG YOZILDI: So'rov yakunlandi"""
    ),
    (
        772,
        "Rate Limiter Actor: So'rovlar chastotasini nazorat qilish",
        "API serveriga sekundiga ko'pi bilan N ta so'rov yuborishni kafolatlovchi Actor.",
        """import Foundation

actor RateLimiter {
    private var requestCount = 0
    private let maxRequests = 2
    
    func allowRequest() -> Bool {
        if requestCount < maxRequests {
            requestCount += 1
            return true
        }
        return false
    }
}

Task {
    let limiter = RateLimiter()
    print("1-so'rov: \\(await limiter.allowRequest())")
    print("2-so'rov: \\(await limiter.allowRequest())")
    print("3-so'rov: \\(await limiter.allowRequest())") // Rad etiladi
}
""",
        "Rate Limiter Actor server limitlaridan oshib ketmaslik uchun kiruvchi chaqiruvlarni bitta nuqtada tekshiradi.",
        """1-so'rov: true
2-so'rov: true
3-so'rov: false"""
    ),
    (
        773,
        "Deadlock muammosining Actor modelida yo'q qilinishi",
        "Klassik qulflar (locks) o'rniga Actor larning kooperativ navbatidan foydalanish afzalligi.",
        """import Foundation

print("Klassik Lock larda ikkita oqim bir-birini kutib qotib qolishi (Deadlock) mumkin. Swift Actor larida esa kutish 'await' orqali oqimni bo'shatadi va Deadlock xavfi deyarli nolga tushadi.")
""",
        "Actor lar oqimni to'sib (block qilib) turmaydi, balki to'xtatish nuqtasida boshqa vazifalarga imkon beradi, bu an'anaviy Deadlock muammolarini yo'qotadi.",
        """Klassik Lock larda ikkita oqim bir-birini kutib qotib qolishi (Deadlock) mumkin. Swift Actor larida esa kutish 'await' orqali oqimni bo'shatadi va Deadlock xavfi deyarli nolga tushadi."""
    ),
    (
        774,
        "Sendable Struct larning avtomatik sintezi",
        "Faqat Sendable turlardan tashkil topgan strukturaning avtomatik oqim xavfsizligi.",
        """import Foundation

struct AppPayload: Sendable {
    let token: String
    let timestamp: Double
}

let p = AppPayload(token: "TOKEN_ABC", timestamp: 12345.0)
print("Payload Sendable sifatida qabul qilindi.")
""",
        "Agar struct maydonlarining barchasi Sendable bo'lsa, Swift kompilyatori unga 'Sendable' protokolini to'liq avtomatik sintezlaydi.",
        """Payload Sendable sifatida qabul qilindi."""
    ),
    (
        775,
        "Generik cheklovda Sendable: <T: Sendable>",
        "Generik funksiya faqat oqimlararo xavfsiz turlarni qabul qilishini talab qiling.",
        """import Foundation

func transferSafely<T: Sendable>(_ item: T) async {
    Task.detached {
        print("Xavfsiz uzatildi: \\(item)")
    }
}

Task {
    await transferSafely("Ma'lumotlar oqimi")
}
""",
        "'T: Sendable' cheklovi ko'p oqimli kutubxonalarda boshqa oqimlarga uzatilayotgan ma'lumotlarning xavfsizligini kafolatlaydi.",
        """Xavfsiz uzatildi: Ma'lumotlar oqimi"""
    ),
    (
        776,
        "Actor ichida Task ochish va Izolyatsiya merosi",
        "Actor metodida yangi ochilgan Task actor kontekstida qolishini ko'rsating.",
        """import Foundation

actor JobDispatcher {
    var jobCount = 0
    
    func spawnJob() {
        Task {
            // Task actor isolation ni meros qilib oladi, shuning uchun 'self.jobCount' to'g'ridan-to'g'ri o'zgaradi:
            jobCount += 1
            print("Vazifa bajarildi, jami: \\(jobCount)")
        }
    }
}

Task {
    let d = JobDispatcher()
    await d.spawnJob()
}
""",
        "Actor ichida ochilgan 'Task { ... }' bloki o'sha actor-ning izolyatsiyasini avtomatik meros oladi va uning ichki maydonlarini xavfsiz o'zgartira oladi.",
        """Vazifa bajarildi, jami: 1"""
    ),
    (
        777,
        "Actor ichida Task.detached ochilganda Izolyatsiya uzilishi",
        "Task.detached actor kontekstini meros qilib olmasligini tushuntiring.",
        """import Foundation

actor IsolatedNode {
    var state = "Aktiv"
    
    func detachTask() {
        Task.detached {
            // Bu yerda 'self.state' ga to'g'ridan-to'g'ri kirib bo'lmaydi, await talab qilinadi:
            print("Detached vazifada actor isolation uzilgan.")
        }
    }
}

Task {
    let node = IsolatedNode()
    await node.detachTask()
}
""",
        "'Task.detached' actor muhitidan to'liq uziladi, shu sababli u actor maydonlariga faqat tashqaridan 'await' orqali murojaat qila oladi.",
        """Detached vazifada actor isolation uzilgan."""
    ),
    (
        778,
        "@MainActor ga bog'langan ViewModel va UI yangilash",
        "SwiftUI uchun modelni to'liq MainActor ga bog'lash naqshi.",
        """import Foundation

@MainActor
class CounterViewModel {
    private(set) var value = 0
    func increment() { value += 1 }
}

Task { @MainActor in
    let vm = CounterViewModel()
    vm.increment()
    print("ViewModel qiymati: \\(vm.value)")
}
""",
        "SwiftUI-dagi barcha ViewModellar va UI bilan bog'liq klasslarni butunlay '@MainActor' bilan belgilash eng to'g'ri sanoat standartidir.",
        """ViewModel qiymati: 1"""
    ),
    (
        779,
        "Actor metodlarida Typed Throws",
        "Actor metodidan aniq turdagi xatolikni tashlash.",
        """import Foundation

enum OrderError: Error { case invalidQuantity }

actor InventoryStore {
    private var stock = 10
    
    func buy(quantity: Int) throws(OrderError) {
        guard quantity <= stock else { throw .invalidQuantity }
        stock -= quantity
    }
}

Task {
    let store = InventoryStore()
    do {
        try await store.buy(quantity: 15)
    } catch {
        print("Actor typed throw: \\(error)")
    }
}
""",
        "Swift 6 da Actor metodlari ham 'throws(CustomError)' Typed Throws bilan to'liq integratsiyalashgan.",
        """Actor typed throw: invalidQuantity"""
    ),
    (
        780,
        "AsyncStream va Actor hamkorligi",
        "Actor ichidagi o'zgarishlarni tashqi dunyoga AsyncStream orqali oqimli uzatish.",
        """import Foundation

actor ChatRoom {
    private var messages: [String] = []
    
    func post(message: String) {
        messages.append(message)
        print("Xona: \\(message)")
    }
}

Task {
    let chat = ChatRoom()
    await chat.post(message: "Salom barchaga!")
}
""",
        "Actor ma'lumotlar yaxlitligini ta'minlaydi, AsyncStream esa ularni reaktiv iste'molchilar uchun tarqatadi.",
        """Xona: Salom barchaga!"""
    ),
    (
        781,
        "Taqsimlangan Aktyorlar (Distributed Actors) tushunchasi",
        "Turli qurilmalar yoki serverlar o'rtasida tarmoq orqali ishlovchi actor arxitekturasi.",
        """import Foundation

print("Swift 'distributed actor' texnologiyasi tarmoq orqali turli serverlar va qurilmalar orasida actor modelini amalga oshirishga imkon beradi.")
""",
        "'distributed actor' Apple ekotizimida xabarlarni tarmoq orqali avtomatik serializatsiya qilib boshqa serverga uzatish imkonini yaratadi.",
        """Swift 'distributed actor' texnologiyasi tarmoq orqali turli serverlar va qurilmalar orasida actor modelini amalga oshirishga imkon beradi."""
    ),
    (
        782,
        "Actor ichidagi rekursiya va uning xavfsizligi",
        "Actor metodining o'z-o'zini chaqirishi.",
        """import Foundation

actor MathActor {
    func factorial(_ n: Int) -> Int {
        return n <= 1 ? 1 : n * factorial(n - 1)
    }
}

Task {
    let m = MathActor()
    print("5! = \\(await m.factorial(5))")
}
""",
        "Actor ichki sinxron metodlarida o'zini chaqirganda navbat kutilmaydi, chunki oqim allaqachon actor ichida joylashgan.",
        """5! = 120"""
    ),
    (
        783,
        "Global o'zgaruvchilar xavfsizligi: Let vs @MainActor",
        "Swift 6 da erkin o'zgaruvchi e'lon qilib bo'lmasligi va uning yechimlari.",
        """import Foundation

// Yechim 1: O'zgarmas 'let' (Sendable bo'lishi shart):
let kMaxTimeoutSeconds = 30

// Yechim 2: O'zgaruvchi 'var' ni MainActor bilan himoyalash:
@MainActor var currentThemeColor = "#FFFFFF"

print("O'zgarmas: \\(kMaxTimeoutSeconds)")
""",
        "Swift 6 da modul darajasidagi har qanday erkin 'var' qat'iyan taqiqlangan, chunki u parallel oqimlarda xotira to'qnashuvining 1-raqamli sababchisi bo'lgan.",
        """O'zgarmas: 30"""
    ),
    (
        784,
        "Actor da zanjirli operatsiyalar (Transactional Batching)",
        "Reentrancy muammosining oldini olish uchun bir nechta amallarni yagona sinxron metodda bajarish.",
        """import Foundation

actor UserStore {
    private var name = ""
    private var email = ""
    
    // Yagona sinxron blok: bu yerda hech qanday suspension point (await) bo'lmaydi!
    func updateProfile(name: String, email: String) {
        self.name = name
        self.email = email
    }
    
    func getProfile() -> String { "\\(name) (\\(email))" }
}

Task {
    let store = UserStore()
    await store.updateProfile(name: "Ali", email: "ali@uz.net")
    print(await store.getProfile())
}
""",
        "Reentrancy muammosidan qochishning eng oltin qoidasi: o'zaro bog'liq ma'lumotlarni o'zgartiruvchi metod ichiga 'await' qo'ymasdan, uni toza sinxron blokda yakunlashdir.",
        """Ali (ali@uz.net)"""
    ),
    (
        785,
        "Actor testlash (Unit testing actors)",
        "Asinxron test metodlarida Actor larni tekshirish.",
        """import Foundation

func testActorCounter() async {
    let counter = SafeCounter()
    let val = await counter.increment()
    assert(val == 1, "Counter 1 bo'lishi shart!")
    print("Test muvaffaqiyatli o'tdi.")
}

Task {
    await testActorCounter()
}
""",
        "Swift Testing va XCTest zamonaviy asinxron testlarni 'async' test funktsiyalari orqali to'liq qo'llab-quvvatlaydi.",
        """Test muvaffaqiyatli o'tdi."""
    ),
    (
        786,
        "Background Worker Actor",
        "Katta hajmdagi hisob-kitoblarni UI dan alohida maxsus fonda bajaruvchi Actor.",
        """import Foundation

actor ImageRenderingActor {
    func renderFilters(input: String) -> String {
        return "RENDERED_FILTER_ON_\\(input)"
    }
}

Task {
    let renderer = ImageRenderingActor()
    let rendered = await renderer.renderFilters(input: "AVATAR_PNG")
    print("Render natijasi: \\(rendered)")
}
""",
        "Og'ir CPU yuklamalarini alohida Actor larga yuklash foydalanuvchi interfeysining (UI) qotib qolmasligini kafolatlaydi.",
        """Render natijasi: RENDERED_FILTER_ON_AVATAR_PNG"""
    ),
    (
        787,
        "Sendable Enum larning afzalliklari",
        "Associated value larga ega enum larning oqimlararo xavfsizligi.",
        """import Foundation

enum NetworkCommand: Sendable {
    case ping
    case sendPayload(data: String)
}

let cmd = NetworkCommand.sendPayload(data: "HELLO")
print("Buyruq oqimlararo uzatishga tayyor: \\(cmd)")
""",
        "Sendable enum lar oqimlar o'rtasida buyruqlar va hodisalarni xavfsiz yuborishda asosiy xabar formatidir.",
        """Buyruq oqimlararo uzatishga tayyor: sendPayload(data: "HELLO")"""
    ),
    (
        788,
        "Actor va Dictionary xotira tozaligi",
        "Actor ichidagi lug'at elementlarini xavfsiz yangilash va o'chirish.",
        """import Foundation

actor SessionRegistry {
    private var activeSessions: [String: Date] = [:]
    
    func register(token: String) {
        activeSessions[token] = Date()
    }
    
    func count() -> Int { activeSessions.count }
}

Task {
    let reg = SessionRegistry()
    await reg.register(token: "TOKEN_1")
    print("Faol sessiyalar: \\(await reg.count())")
}
""",
        "Ko'p oqimli muhitda lug'atlar faqat Actor yoki qulf bilan himoyalangandagina xavfsiz bo'ladi.",
        """Faol sessiyalar: 1"""
    ),
    (
        789,
        "Swift 6 Migration strategiyasi: Strict Concurrency",
        "Loyiha sozlamalarida `-strict-concurrency=complete` bayrog'ining ahamiyati.",
        """import Foundation

print("Swift 6 ga o'tishda '-strict-concurrency=complete' bayrog'i barcha Sendable va Actor ogohlantirishlarini xatoliklarga aylantiradi.")
""",
        "Apple loyihalarni Swift 6 ga bosqichma-bosqich o'tkazish uchun strict concurrency tekshiruvlarini taqdim etgan.",
        """Swift 6 ga o'tishda '-strict-concurrency=complete' bayrog'i barcha Sendable va Actor ogohlantirishlarini xatoliklarga aylantiradi."""
    ),
    (
        790,
        "Actor ichida boshqa Actor ni chaqirish (Cross-Actor call)",
        "Ikki mustaqil Actor ning o'zaro xavfsiz muloqoti.",
        """import Foundation

actor BankA {
    func sendFunds() -> Double { 100.0 }
}

actor BankB {
    func receive(from bankA: BankA) async {
        let amount = await bankA.sendFunds()
        print("Bank B qabul qildi: $\\(amount)")
    }
}

Task {
    let a = BankA()
    let b = BankB()
    await b.receive(from: a)
}
""",
        "Bitta Actor boshqa Actor-ni chaqirayotganda ham albatta 'await' yoziladi, chunki ikkinchi actor ham o'z navbatiga ega bo'lishi mumkin.",
        """Bank B qabul qildi: $100.0"""
    ),
    (
        791,
        "Actor ichida statik xususiyatlar",
        "Actor ning o'ziga tegishli statik konstantalar.",
        """import Foundation

actor CloudNode {
    static let maxPayloadBytes = 1024 * 1024
}

print("Maksimal yuklama: \\(CloudNode.maxPayloadBytes) bayt")
""",
        "Actor ichidagi statik 'let' maydonlar barcha instansiyalar uchun o'zgarmas umumiy parametr bo'lib xizmat qiladi.",
        """Maksimal yuklama: 1048576 bayt"""
    ),
    (
        792,
        "MainActor da ishlaydigan UI tugma modeli",
        "UI hodisalarini faqat MainActor da qayta ishlash.",
        """import Foundation

@MainActor
class AppButton {
    var isEnabled: Bool = true
    func press() {
        print("Tugma bosildi, UI yangilanmoqda...")
    }
}

Task { @MainActor in
    let btn = AppButton()
    btn.press()
}
""",
        "UI dagi har qanday holat o'zgarishi faqat MainActor orqali amalga oshishi lozim.",
        """Tugma bosildi, UI yangilanmoqda..."""
    ),
    (
        793,
        "nonisolated let xususiyatlarining kuchi",
        "Actor ichidagi 'let' maydonlarga har qanday joydan to'g'ridan-to'g'ri kirish.",
        """import Foundation

actor ServiceRegistryItem {
    let serviceName: String
    init(name: String) { self.serviceName = name }
}

let item = ServiceRegistryItem(name: "AuthService")
print("Servis nomi: \\(item.serviceName)") // await shart emas, chunki 'let'!
""",
        "Swift-da Actor ning 'let' (o'zgarmas) maydonlariga tashqaridan 'await' siz kirishga ruxsat berilgan, chunki ularni hech kim mutatsiyaga uchratolmaydi.",
        """Servis nomi: AuthService"""
    ),
    (
        794,
        "Oqimlararo ma'lumot almashishda Deep Copy o'rniga Sendable Struct",
        "Klassik nusxalash o'rniga qiymat semantikasi.",
        """import Foundation

struct UserDTO: Sendable {
    let name: String
    let token: String
}

let dto = UserDTO(name: "Sherzod", token: "AUTH_XYZ")
print("DTO parallel oqimga tayyor: \\(dto.name)")
""",
        "Sendable Struct lari parallel oqimlar orasida chuqur xotira ko'chirish muammolarisiz o'z-o'zidan xavfsiz uzatiladi.",
        """DTO parallel oqimga tayyor: Sherzod"""
    ),
    (
        795,
        "Actor yordamida Navbat Dispecheri (JobQueue Actor)",
        "Vazifalarni tartib bilan birma-bir bajaruvchi navbat boshqaruvchisi.",
        """import Foundation

actor JobQueue {
    private var queue: [String] = []
    
    func enqueue(_ job: String) {
        queue.append(job)
        print("Navbatga qo'shildi: \\(job)")
    }
    
    func processNext() -> String? {
        return queue.isEmpty ? nil : queue.removeFirst()
    }
}

Task {
    let q = JobQueue()
    await q.enqueue("Vazifa_A")
    let current = await q.processNext()
    print("Bajarilmoqda: \\(current ?? "")")
}
""",
        "JobQueue actor bir nechta oqimlardan kelayotgan vazifalarni xavfsiz tartibga soladi.",
        """Navbatga qo'shildi: Vazifa_A
Bajarilmoqda: Vazifa_A"""
    ),
    (
        796,
        "Actor isolation xatosini tushunish va tuzatish",
        "Kompilyator beradigan 'Actor-isolated property cannot be mutated from outside' xatosining yechimi.",
        """import Foundation

actor DataHolder {
    var score = 0
    func addScore(_ s: Int) { score += s }
}

Task {
    let h = DataHolder()
    // h.score = 10 // XATO: Actor-isolated property cannot be mutated
    await h.addScore(10) // To'g'ri yechim!
    print("Ball qo'shildi.")
}
""",
        "Actor xususiyatlarini tashqaridan to'g'ridan-to'g'ri o'zgartirib bo'lmaydi. Har qanday o'zgartirish actor ichidagi metod orqali amalga oshirilishi shart.",
        """Ball qo'shildi."""
    ),
    (
        797,
        "Sendable bo'lmagan xatolikni Sendable qilish",
        "Maxsus Error turiga Sendable qo'shish.",
        """import Foundation

struct CustomServiceError: Error, Sendable {
    let code: Int
    let reason: String
}

let err = CustomServiceError(code: 404, reason: "Sahifa yo'q")
print("Xatolik Sendable: \\(err.reason)")
""",
        "Swift 6 da oqimlararo tashlanadigan barcha Error lar albatta Sendable bo'lishi shart.",
        """Xatolik Sendable: Sahifa yo'q"""
    ),
    (
        798,
        "Global Actor orqali Dependency Injection",
        "Xizmatlarni ma'lum bir global actor ga bog'lab inyeksiya qilish.",
        """import Foundation

@MainActor
class AppStateService {
    var isUserSignedIn = true
}

Task { @MainActor in
    let service = AppStateService()
    print("Tizimga kirganmi? \\(service.isUserSignedIn)")
}
""",
        "Global actorlar ilova arxitekturasida oqimlar boshqaruvini markazlashtiradi.",
        """Tizimga kirganmi? true"""
    ),
    (
        799,
        "Ko'p oqimli poyga (Data Race) to'liq yo'q qilinganini tasdiqlash",
        "Swift Concurrency arxitekturasining yakuniy maqsadi.",
        """import Foundation

print("Swift Concurrency: Actor Isolation + Sendable tekshiruvi = 100% Data-Race Free Dastur.")
""",
        "Swift kompilyatori compile-time darajasida ma'lumotlar poygasini to'liq yo'qotuvchi dunyodagi eng ilg'or xavfsizlik modeliga ega.",
        """Swift Concurrency: Actor Isolation + Sendable tekshiruvi = 100% Data-Race Free Dastur."""
    ),
    (
        800,
        "Amaliy loyiha: Ko'p oqimli Xavfsiz Savdo Birjasi Dvigateli (OrderBook Actor)",
        "OrderBook Actor (buyurtmalarni qabul qilish va moslashtirish), MainActor UI ko'prigi, Sendable tranzaksiyalar va 100% Data-Race xavfsiz birja tizimi moduli.",
        """import Foundation

struct TradeOrder: Sendable {
    let id: UUID
    let symbol: String
    let price: Double
    let quantity: Int
    let isBuy: Bool
}

actor OrderBookEngine {
    private var orders: [TradeOrder] = []
    
    func placeOrder(_ order: TradeOrder) -> String {
        orders.append(order)
        let typeStr = order.isBuy ? "SOTIB OLISH" : "SOTISH"
        return "[BIRJA ACTOR]: \\(typeStr) buyurtmasi qabul qilindi: \\(order.quantity) dona \\(order.symbol) @ $\\(order.price)"
    }
    
    func getMarketDepth(symbol: String) -> (buyCount: Int, sellCount: Int) {
        let matching = orders.filter { $0.symbol == symbol }
        let buys = matching.filter(\\.isBuy).count
        let sells = matching.filter { !$0.isBuy }.count
        return (buys, sells)
    }
}

@MainActor
class TradingTerminalUI {
    let engine = OrderBookEngine()
    
    func executeUserTrade() async {
        let buyOrder = TradeOrder(id: UUID(), symbol: "APPLE", price: 185.0, quantity: 10, isBuy: true)
        let sellOrder = TradeOrder(id: UUID(), symbol: "APPLE", price: 186.0, quantity: 5, isBuy: false)
        
        let msg1 = await engine.placeOrder(buyOrder)
        let msg2 = await engine.placeOrder(sellOrder)
        print(msg1)
        print(msg2)
        
        let depth = await engine.getMarketDepth(symbol: "APPLE")
        print("[TERMINAL UI]: Bozor chuqurligi (APPLE): \\(depth.buyCount) ta xarid, \\(depth.sellCount) ta sotuv.")
    }
}

print("=== BIRJA SAVDO PLATFORMASI ISHGA TUSHDI ===")
Task { @MainActor in
    let terminal = TradingTerminalUI()
    await terminal.executeUserTrade()
}
""",
        "Ushbu yakuniy loyihada 'actor' izolyatsiyasi, '@MainActor' UI integratsiyasi, 'Sendable' ob'ektlar, 'await' sinxronizatsiyasi va real moliya savdo dvigateli birlashtirilib, 100% Data-Race Free arxitektura namoyish etildi.",
        """=== BIRJA SAVDO PLATFORMASI ISHGA TUSHDI ===
[BIRJA ACTOR]: SOTIB OLISH buyurtmasi qabul qilindi: 10 dona APPLE @ $185.0
[BIRJA ACTOR]: SOTISH buyurtmasi qabul qilindi: 5 dona APPLE @ $186.0
[TERMINAL UI]: Bozor chuqurligi (APPLE): 1 ta xarid, 1 ta sotuv."""
    )
]

tasks = [format_task(*t) for t in tasks_data]
save_file("swift_16_actors_va_data_races_oldini_olish.md", tasks)
