# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks_data = [
    (
        551,
        "Swift-da xatoliklar falsafasi: Error protokoli",
        "Swift-da istisnolarni ifodalovchi eng asosiy Error protokolini tushuntiring.",
        """import Foundation

enum NetworkError: Error {
    case connectionLost
    case serverUnreachable
}

let err: Error = NetworkError.connectionLost
print("Xatolik turi: \\(err)")
""",
        "Swift-da xatoliklar (Exceptions) og'ir runtime stack unwinding emas, balki oddiy qiymat turlaridir. 'Error' protokoli orqali har qanday enum yoki struktura xatolik sifatida tashlanishi (throw) mumkin.",
        """Xatolik turi: connectionLost"""
    ),
    (
        552,
        "Xatoliklarni Enum ko'rinishida ifodalash",
        "Kassa apparatida yuz berishi mumkin bo'lgan xatoliklarni enum orqali modellashtiring.",
        """import Foundation

enum VendingMachineError: Error {
    case invalidSelection
    case outOfStock
    case insufficientFunds(coinsNeeded: Int)
}

let errorInstance = VendingMachineError.insufficientFunds(coinsNeeded: 5)
print("Xatolik namunasi: \\(errorInstance)")
""",
        "Swift-da xatoliklarni Enum shaklida yaratish eng to'g'ri amaliyotdir. Associated Values orqali xatolikka qo'shimcha parametrlar ham biriktiriladi.",
        """Xatolik namunasi: insufficientFunds(coinsNeeded: 5)"""
    ),
    (
        553,
        "Xatolik tashlovchi funksiyalar: throws",
        "Shart bajarilmaganda xato tashlovchi funksiya yozing.",
        """import Foundation

func checkAgeForDriving(age: Int) throws {
    enum DrivingError: Error { case underage }
    if age < 18 {
        throw DrivingError.underage
    }
    print("Haydashga ruxsat berildi.")
}

print("Funksiya 'throws' bilan e'lon qilindi.")
""",
        "'throws' kalit so'zi funksiya o'z ijrosi davomida xatolik yuzaga keltirishi mumkinligini va uni chaqiruvchi javobgarlikni o'z zimmasiga olishi shartligini bildiradi.",
        """Funksiya 'throws' bilan e'lon qilindi."""
    ),
    (
        554,
        "Xatoliklarni chaqirish va tutish: do-catch va try",
        "Xatolik tashlovchi funksiyani 'do-catch' bloki ichida 'try' bilan chaqiring.",
        """import Foundation

enum BankError: Error {
    case insufficientBalance
}

func withdraw(amount: Double, balance: Double) throws -> Double {
    if amount > balance { throw BankError.insufficientBalance }
    return balance - amount
}

do {
    let newBalance = try withdraw(amount: 500.0, balance: 200.0)
    print("Qoldiq: $\\(newBalance)")
} catch BankError.insufficientBalance {
    print("XATOLIK: Hisobingizda yetarli mablag' mavjud emas!")
} catch {
    print("Boshqa xato: \\(error)")
}
""",
        "'try' operatori throwing funksiyani chaqirishda majburiydir. 'do-catch' esa yuz bergan nosozlikni ushlab, ilovaning to'xtab qolishini oldini oladi.",
        """XATOLIK: Hisobingizda yetarli mablag' mavjud emas!"""
    ),
    (
        555,
        "Bir nechta aniq xatoliklarni ushlovchi catch bloklari",
        "Har xil xatoliklar uchun alohida-alohida xabarlar beruvchi bloklar tuzing.",
        """import Foundation

enum FileError: Error {
    case notFound
    case accessDenied
    case corrupted
}

func loadFile(name: String) throws {
    if name == "secret.txt" { throw FileError.accessDenied }
    if name.isEmpty { throw FileError.notFound }
    print("Fayl o'qildi: \\(name)")
}

do {
    try loadFile(name: "secret.txt")
} catch FileError.notFound {
    print("Fayl topilmadi.")
} catch FileError.accessDenied {
    print("Kirish huquqi cheklangan!")
} catch {
    print("Kutilmagan nosozlik.")
}
""",
        "Swift aniq 'catch' bloklarini ketma-ket yozish orqali turli xatoliklarni professional darajada filtrlash imkonini beradi.",
        """Kirish huquqi cheklangan!"""
    ),
    (
        556,
        "Catch blokida 'where' sharti",
        "Associated value qiymatini catch qismida 'where' bilan tekshiring.",
        """import Foundation

enum ServerAPIError: Error {
    case status(code: Int)
}

func queryServer() throws {
    throw ServerAPIError.status(code: 404)
}

do {
    try queryServer()
} catch ServerAPIError.status(let code) where code == 404 {
    print("Resurs topilmadi (404 Not Found).")
} catch ServerAPIError.status(let code) {
    print("Boshqa server kodi: \\(code)")
} catch {
    print("Noma'lum xato.")
}
""",
        "'catch let error where ...' sintaksisi xatolik ichidagi parametrlarni mantiqiy mezonlar bo'yicha saralashga yordam beradi.",
        """Resurs topilmadi (404 Not Found)."""
    ),
    (
        557,
        "Standart 'error' o'zgaruvchisi umumiy catch blokida",
        "Xatolik turini ko'rsatmagan catch blokida avtomatik 'error' ob'ektidan foydalaning.",
        """import Foundation

enum SimpleError: Error {
    case somethingWentWrong
}

func doRiskyTask() throws {
    throw SimpleError.somethingWentWrong
}

do {
    try doRiskyTask()
} catch {
    print("Ushlangan xato: \\(error)")
}
""",
        "Agar 'catch' dan keyin hech qanday nom yozilmasa, Swift blok ichida 'error' nomli avtomatik o'zgaruvchini taqdim etadi.",
        """Ushlangan xato: somethingWentWrong"""
    ),
    (
        558,
        "Xatolikni Optional ga aylantirish: try?",
        "Xatolik yuz berganda shunchaki nil olish uchun 'try?' dan foydalaning.",
        """import Foundation

func parsePositiveInt(_ str: String) throws -> Int {
    enum ParseError: Error { case notPositive }
    guard let n = Int(str), n > 0 else { throw ParseError.notPositive }
    return n
}

let num1 = try? parsePositiveInt("42")
let num2 = try? parsePositiveInt("-10")

print("num1: \\(String(describing: num1))")
print("num2: \\(String(describing: num2))")
""",
        "'try?' operatori funksiya natijasini Optional qiladi: muvaffaqiyatli bo'lsa Optional(qiymat), xatolik yuz bersa nil qaytaradi. Bu 'do-catch' yozish shart bo'lmagan vaziyatlar uchun qulaydir.",
        """num1: Optional(42)
num2: nil"""
    ),
    (
        559,
        "Majburiy xatosiz chaqirish: try!",
        "Xato bo'lmasligi 100% kafolatlangan joyda 'try!' operatorini qo'llang.",
        """import Foundation

func getBuiltinSetting() throws -> String {
    return "PRODUCTION_MODE"
}

let setting = try! getBuiltinSetting()
print("Sozlama: \\(setting)")
""",
        "'try!' operatori throwing funksiyaning xato bermasligiga kafolat beradi. Agar xato yuz bersa, dastur run-time crash bo'ladi.",
        """Sozlama: PRODUCTION_MODE"""
    ),
    (
        560,
        "Qayta xatolik tashlash: rethrows",
        "Parametrdagi closure xato tashlasagina o'zi ham xato tashlaydigan funksiyani ko'rsating.",
        """import Foundation

func executeAction(action: () throws -> Void) rethrows {
    print("Bajarilmoqda...")
    try action()
    print("Bajarildi.")
}

// Xavfsiz closure uchun 'try' talab qilinmaydi:
executeAction {
    print("Xatosiz amal.")
}
""",
        "'rethrows' faqat uzatilgan closure sababli xatolik yuz bergandagina xato tashlaydi. Bu kodning ortiqcha 'try' lardan xoli bo'lishini ta'minlaydi.",
        """Bajarilmoqda...
Xatosiz amal.
Bajarildi."""
    ),
    (
        561,
        "Resurslarni tozalash: defer va xatoliklar",
        "Xatolik 'throw' qilinganda ham 'defer' bloki albatta bajarilishini isbotlang.",
        """import Foundation

enum TaskError: Error { case fail }

func performWithResource() throws {
    print("1. Resurs ajratildi.")
    defer {
        print("3. Resurs xavfsiz tozalandi (defer).")
    }
    print("2. Xatolik tashlanmoqda...")
    throw TaskError.fail
}

do {
    try performWithResource()
} catch {
    print("4. Xatolik catch da ushlandi: \\(error)")
}
""",
        "'defer' bloki xatolik yuz berib funksiya erta to'xtaganda ham xotira va tizim resurslarining sizib ketishini 100% oldini oladi.",
        """1. Resurs ajratildi.
2. Xatolik tashlanmoqda...
3. Resurs xavfsiz tozalandi (defer).
4. Xatolik catch da ushlandi: fail"""
    ),
    (
        562,
        "Result<Success, Failure> tipi asoslari",
        "Asinxron operatsiyalar natijasini Result qutisida saqlang.",
        """import Foundation

enum DownloadError: Error { case networkLost }

func fetchFile() -> Result<String, DownloadError> {
    return .success("Fayl ma'lumotlari muvaffaqiyatli olindi.")
}

let result = fetchFile()
switch result {
case .success(let data):
    print("Muvaffaqiyat: \\(data)")
case .failure(let error):
    print("Xato: \\(error)")
}
""",
        "'Result' ikki holatga ega generik enumdir: '.success(Success)' va '.failure(Failure)'. Bu xatolikni birinchi darajali ma'lumot sifatida olib yurish imkonini beradi.",
        """Muvaffaqiyat: Fayl ma'lumotlari muvaffaqiyatli olindi."""
    ),
    (
        563,
        "Result qutisini get() orqali throwing ga aylantirish",
        "Result ichidagi qiymatni oddiy try bilan ochish usuli.",
        """import Foundation

let goodResult: Result<Int, Error> = .success(42)

do {
    let value = try goodResult.get()
    print("Result.get() qiymati: \\(value)")
} catch {
    print("Xato: \\(error)")
}
""",
        "'result.get()' muvaffaqiyatli bo'lsa qiymatni qaytaradi, agar failure bo'lsa xatolikni throw qiladi.",
        """Result.get() qiymati: 42"""
    ),
    (
        564,
        "Throwing funksiyani Result ga aylantirish: Result { try ... }",
        "Xatolik tashlovchi harakatni bir qatorda Result qutisiga soling.",
        """import Foundation

func riskyCalculation() throws -> Int {
    return 100 * 5
}

let encapsulatedResult = Result { try riskyCalculation() }
print("Result turi: \\(type(of: encapsulatedResult))")
""",
        "'Result { try ... }' initsializatori throwing blokni avtomatik Result<T, Error> enumiga aylantiradi.",
        """Result turi: Result<Int, any Error>"""
    ),
    (
        565,
        "Result.mapError bilan xatolik turini o'zgartirish",
        "Texnik xatolikni domen darajasidagi tushunarli xatolikka xaritalang.",
        """import Foundation

enum LowLevelError: Error { case ioError }
enum UserFacingError: Error { case fileNotReadable }

let lowResult: Result<String, LowLevelError> = .failure(.ioError)

let mapped = lowResult.mapError { _ in UserFacingError.fileNotReadable }

switch mapped {
case .success: break
case .failure(let err): print("Xaritalangan xato: \\(err)")
}
""",
        "'mapError' Result ichidagi muvaffaqiyatli qiymatga daxl qilmasdan, faqat xatolik turini transformatsiya qiladi.",
        """Xaritalangan xato: fileNotReadable"""
    ),
    (
        566,
        "Swift 5.9 va Swift 6 Typed Throws: throws(CustomError)",
        "Funksiya faqat ma'lum bir aniq xatolik turini tashlashini qat'iy belgilang.",
        """import Foundation

enum AuthenticationError: Error {
    case invalidCredentials
    case tokenExpired
}

// Swift 5.9+ / Swift 6 Typed Throws:
func login(token: String) throws(AuthenticationError) {
    if token.isEmpty {
        throw .invalidCredentials
    }
}

do {
    try login(token: "")
} catch {
    // error o'zgaruvchisining turi 'AuthenticationError' ekanligi kafolatlangan!
    print("Typed throw ushlandi: \\(error)")
}
""",
        "Swift 6 da to'liq joriy qilingan 'Typed Throws' funksiyaga 'throws(MyError)' shaklida aniq xatolik turini ko'rsatish imkonini beradi. Natijada catch bloki to'liq (exhaustive) bo'lib, generic Error o'rniga aniq tur bilan ishlaydi.",
        """Typed throw ushlandi: invalidCredentials"""
    ),
    (
        567,
        "LocalizedError protokoli: errorDescription",
        "Xatolik konsolga yoki foydalanuvchiga chiqqanda chiroyli tushuntirish matnini berish.",
        """import Foundation

enum PaymentError: LocalizedError {
    case cardExpired
    
    var errorDescription: String? {
        switch self {
        case .cardExpired:
            return "Bank kartangizning amal qilish muddati tugagan."
        }
    }
}

let err = PaymentError.cardExpired
print("Xatolik matni: \\(err.localizedDescription)")
""",
        "'LocalizedError' protokoli 'errorDescription' xususiyati orqali foydalanuvchiga ko'rsatilishi mumkin bo'lgan lokalizatsiyalangan xatolik xabarini qaytaradi.",
        """Xatolik matni: Bank kartangizning amal qilish muddati tugagan."""
    ),
    (
        568,
        "Asinxron xatoliklar: async throws",
        "Ham asinxron, ham xatolik tashlovchi tarmoq chaqiruvini boshqarish.",
        """import Foundation

enum NetworkStateError: Error { case noConnection }

func fetchDataAsync() async throws -> String {
    let connected = false
    if !connected { throw NetworkStateError.noConnection }
    return "Ma'lumotlar"
}

Task {
    do {
        let _ = try await fetchDataAsync()
    } catch {
        print("Asinxron xatolik ushlandi: \\(error)")
    }
}
""",
        "'async throws' bir vaqtning o'zida asinxron kutish va xatolik tashlashni ta'minlaydi. Chaqirilganda 'try await' birga ishlatiladi.",
        """Asinxron xatolik ushlandi: noConnection"""
    ),
    (
        569,
        "JSON Decoding xatoliklarini tahlil qilish",
        "JSON noto'g'ri bo'lganda Decoding xatolik turini batafsil ajrating.",
        """import Foundation

struct User: Decodable {
    let id: Int
    let name: String
}

let brokenJSON = \"\"\"{"id": "not_an_int", "name": "Ali"}\"\"\".data(using: .utf8)!

do {
    let _ = try JSONDecoder().decode(User.self, from: brokenJSON)
} catch DecodingError.typeMismatch(let type, let context) {
    print("Tip mos kelmadi: \\(type), Yo'li: \\(context.codingPath.map(\\.stringValue))")
} catch {
    print("Boshqa decoding xatosi: \\(error)")
}
""",
        "Foundation-ning DecodingError enumi xato qaysi maydonda va nima sababdan ro'y berganini aniq ko'rsatadi.",
        """Tip mos kelmadi: Int, Yo'li: ["id"]"""
    ),
    (
        570,
        "Initsializatorda xatolik tashlash: init() throws",
        "Noto'g'ri parametr berilganda obyekt yaratilmasdan xato tashlanishini ko'rsating.",
        """import Foundation

enum UserCreationError: Error {
    case emptyName
}

struct ValidUser {
    let name: String
    init(name: String) throws {
        guard !name.isEmpty else { throw UserCreationError.emptyName }
        self.name = name
    }
}

do {
    let _ = try ValidUser(name: "")
} catch {
    print("Foydalanuvchi yaratilmadi: \\(error)")
}
""",
        "'init() throws' konstruktorda xatolik sababini aniq ma'lum qilish imkonini beradi.",
        """Foydalanuvchi yaratilmadi: emptyName"""
    ),
    (
        571,
        "Hisoblangan xususiyatlarda xatolik tashlash: get throws",
        "Xususiyat qiymatini o'qish paytida xato tashlovchi getter.",
        """import Foundation

enum SensorError: Error { case offline }

struct SmartSensor {
    var isOnline = false
    
    var temperature: Double {
        get throws {
            guard isOnline else { throw SensorError.offline }
            return 22.5
        }
    }
}

let sensor = SmartSensor()
do {
    let _ = try sensor.temperature
} catch {
    print("Sensor xatosi: \\(error)")
}
""",
        "Swift 5.5 dan boshlab xususiyat getterlariga 'throws' qo'yish mumkin.",
        """Sensor xatosi: offline"""
    ),
    (
        572,
        "Retry Pattern: Xatolikda qayta urinish",
        "Xatolik yuz berganda operatsiyani N marta qayta sinovchi generik funksiya.",
        """import Foundation

func retry<T>(attempts: Int, task: () throws -> T) throws -> T {
    var lastError: Error?
    for _ in 1...attempts {
        do {
            return try task()
        } catch {
            lastError = error
        }
    }
    throw lastError!
}

var tries = 0
let result = try? retry(attempts: 3) { () -> String in
    tries += 1
    if tries < 2 { throw URLError(.timedOut) }
    return "Muvaffaqiyatli ulandi"
}

print("Natija: \\(result ?? ""), Urinishlar: \\(tries)")
""",
        "Retry pattern tarmoq va beqaror tizimlarda nosozliklarni avtomatik bartaraf qilish uchun qo'llaniladi.",
        """Natija: Muvaffaqiyatli ulandi, Urinishlar: 2"""
    ),
    (
        573,
        "Circuit Breaker Pattern asoslari",
        "Ketma-ket xatoliklar soni oshganda vaqtincha barcha so'rovlarni to'xtatuvchi xavfsizlik mexanizmi.",
        """import Foundation

class CircuitBreaker {
    private var failureCount = 0
    private let threshold = 2
    var isOpen = false
    
    func execute(action: () throws -> Void) throws {
        if isOpen {
            print("Zanjir ochiq (Circuit Open): Yangi so'rovlar qabul qilinmaydi.")
            return
        }
        do {
            try action()
            failureCount = 0
        } catch {
            failureCount += 1
            if failureCount >= threshold {
                isOpen = true
                print("Chegaradan oshdi! Zanjir uzildi (Circuit Breaker Tripped).")
            }
            throw error
        }
    }
}

let cb = CircuitBreaker()
struct DummyError: Error {}

for _ in 1...3 {
    try? cb.execute { throw DummyError() }
}
""",
        "Circuit Breaker qulagan xizmatlarni ortiqcha so'rovlar bilan to'ldirib yubormaslik uchun ishlatiladi.",
        """Chegaradan oshdi! Zanjir uzildi (Circuit Breaker Tripped).
Zanjir ochiq (Circuit Open): Yangi so'rovlar qabul qilinmaydi."""
    ),
    (
        574,
        "Never bilan xatosiz Result: Result<T, Never>",
        "Xatolik yuz berishi mutlaqo imkonsiz bo'lgan operatsiyani ifodalash.",
        """import Foundation

func getGuaranteedData() -> Result<String, Never> {
    return .success("Bu ma'lumot doimo kafolatlangan.")
}

let guaranteed = getGuaranteedData()
switch guaranteed {
case .success(let msg):
    print("Xabari: \\(msg)")
// Never bo'lgani sababli .failure shart emas!
}
""",
        "'Failure == Never' bo'lgan Result qutisida failure bandi bo'lishi mumkin emas, switch operatori faqat .success ni tekshiradi.",
        """Xabari: Bu ma'lumot doimo kafolatlangan."""
    ),
    (
        575,
        "CancellationError va Task bekor qilinishini boshqarish",
        "Asinxron vazifa to'xtatilganda xavfsiz chiqish.",
        """import Foundation

func longTask() async throws {
    try Task.checkCancellation()
    print("Vazifa bajarilmoqda...")
}

Task {
    do {
        try await longTask()
    } catch is CancellationError {
        print("Vazifa bekor qilindi.")
    } catch {
        print("Boshqa xato: \\(error)")
    }
}
""",
        "'Task.checkCancellation()' agar vazifa bekor qilingan bo'lsa darhol 'CancellationError' tashlaydi.",
        """Vazifa bajarilmoqda..."""
    ),
    (
        576,
        "Xatolik kodi va Error Mapping",
        "Server status kodlarini maxsus dasturiy xatoliklarga o'giruvchi funksiya.",
        """import Foundation

enum DomainError: Error {
    case unauthorized
    case serverFailure
    case unknown
}

func mapStatusCode(_ code: Int) -> DomainError {
    switch code {
    case 401, 403: return .unauthorized
    case 500...599: return .serverFailure
    default: return .unknown
    }
}

print("503 xatosi: \\(mapStatusCode(503))")
""",
        "Xatoliklarni xaritalash (Error Mapping) tarmoq qatlamini biznes logikadan ajratadi.",
        """503 xatosi: serverFailure"""
    ),
    (
        577,
        "Xatoliklarni swallow qilish (yutib yuborish) antipatterni",
        "Xatoni e'tiborsiz qoldirish nima uchun yomon amaliyot ekanligini tushuntiring.",
        """import Foundation

func riskyIO() throws { throw URLError(.fileDoesNotExist) }

// Yomon amaliyot (Antipattern):
// try? riskyIO() // Xato qayerda ro'y bergani butunlay yashirildi!

// To'g'ri amaliyot:
do {
    try riskyIO()
} catch {
    print("[LOG]: Kritik xatolik qayd etildi: \\(error)")
}
""",
        "Xatoliklarni bo'sh catch yoki e'tiborsiz 'try?' bilan yutib yuborish nosozliklarni topishni (debugging) imkonsiz qiladi.",
        """[LOG]: Kritik xatolik qayd etildi: The operation couldn’t be completed. (NSURLErrorDomain error -1100.)"""
    ),
    (
        578,
        "CustomNSError protokoli: ErrorDomain va ErrorCode",
        "Apple tizimida Objective-C NSError bilan to'liq mos xatolik yaratish.",
        """import Foundation

enum SystemEngineError: Int, CustomNSError {
    case diskFull = 101
    case memoryCorrupt = 102
    
    static var errorDomain: String { "uz.khorazmiy.engine" }
    var errorCode: Int { rawValue }
}

let err = SystemEngineError.diskFull
print("Domen: \\(SystemEngineError.errorDomain), Kod: \\(err.errorCode)")
""",
        "'CustomNSError' protokoli orqali Swift xatoliklariga aniq domen (domain) va raqamli kod beriladi.",
        """Domen: uz.khorazmiy.engine, Kod: 101"""
    ),
    (
        579,
        "Tranzaksiya va Rollback mexanizmi",
        "Bir nechta bosqichdan iborat operatsiyada xato bo'lsa barcha o'zgarishlarni bekor qilish.",
        """import Foundation

class TransactionSystem {
    var balances = ["Ali": 100.0, "Vali": 50.0]
    
    func transfer(from: String, to: String, amount: Double) throws {
        enum TxError: Error { case insufficientFunds }
        let current = balances[from] ?? 0.0
        guard current >= amount else { throw TxError.insufficientFunds }
        
        balances[from] = current - amount
        // Agar ikkinchi qadamda xato bo'lsa, birinchisini qaytarish kerak bo'ladi (Rollback)
        balances[to] = (balances[to] ?? 0.0) + amount
        print("Muvaffaqiyatli o'tkazildi: $\\(amount)")
    }
}

let tx = TransactionSystem()
try? tx.transfer(from: "Ali", to: "Vali", amount: 30.0)
print("Ali balansi: $\\(tx.balances["Ali"] ?? 0)")
""",
        "Tranzaksiya yaxlitligi xatoliklarni xavfsiz boshqarishga tayanadi.",
        """Muvaffaqiyatli o'tkazildi: $30.0
Ali balansi: $70.0"""
    ),
    (
        580,
        "Validatsiya xatoliklarini to'plovchi kompozitsiya",
        "Bir nechta maydondagi xatoliklarni birdaniga yig'ib qaytaruvchi tizim.",
        """import Foundation

struct MultiValidationError: Error {
    let errors: [String]
}

func validateRegistration(name: String, email: String) throws {
    var collected = [String]()
    if name.isEmpty { collected.append("Ism kiritilmadi") }
    if !email.contains("@") { collected.append("Noto'g'ri email") }
    
    if !collected.isEmpty {
        throw MultiValidationError(errors: collected)
    }
}

do {
    try validateRegistration(name: "", email: "bad_mail")
} catch let multi as MultiValidationError {
    print("Xatoliklar ro'yxati: \\(multi.errors)")
} catch {}
""",
        "Foydalanuvchi interfeyslarida barcha xatoliklarni bitta ro'yxatda qaytarish qulay tajriba taqdim etadi.",
        """Xatoliklar ro'yxati: ["Ism kiritilmadi", "Noto'g'ri email"]"""
    ),
    (
        581,
        "Subscript larda xatolik tashlash (Swift 5.5+)",
        "Subscript orqali xavfsiz o'qishda xatolik tashlash imkoniyati.",
        """import Foundation

struct SecureArray {
    let items = [10, 20, 30]
    enum ArrayError: Error { case outOfBounds }
    
    subscript(safe index: Int) -> Int {
        get throws {
            guard index >= 0 && index < items.count else { throw ArrayError.outOfBounds }
            return items[index]
        }
    }
}

let sa = SecureArray()
do {
    let val = try sa[safe: 1]
    print("Qiymat: \\(val)")
    let _ = try sa[safe: 10]
} catch {
    print("Indeks xatosi: \\(error)")
}
""",
        "Swift 5.5 dan boshlab subscript getteri ham 'throws' qila oladi.",
        """Qiymat: 20
Indeks xatosi: outOfBounds"""
    ),
    (
        582,
        "Xatoliklarni log qiluvchi wrapper closure",
        "Har qanday throwing amalni o'rab, xatolikni konsolga chop etuvchi utilita.",
        """import Foundation

func auditOperation<T>(name: String, block: () throws -> T) rethrows -> T {
    print("AUDIT: '\\(name)' boshlandi.")
    defer { print("AUDIT: '\\(name)' yakunlandi.") }
    return try block()
}

let result = try? auditOperation(name: "Ma'lumotlar bazasi zaxirasi") {
    return "Zaxira yaratildi"
}
print("Natija: \\(result ?? "")")
""",
        "Audit funksiyalari kodni shaffof va kuzatuvchan qiladi.",
        """AUDIT: 'Ma\'lumotlar bazasi zaxirasi' boshlandi.
AUDIT: 'Ma\'lumotlar bazasi zaxirasi' yakunlandi.
Natija: Zaxira yaratildi"""
    ),
    (
        583,
        "Ko'p oqimli muhitda Sendable Error xavfsizligi",
        "Parallel oqimlararo uzatiluvchi xatoliklar Sendable bo'lishi talabi.",
        """import Foundation

struct ThreadError: Error, Sendable {
    let code: Int
}

let err = ThreadError(code: 503)
print("Sendable xatolik parallel oqimlarda xavfsiz uzatiladi: \\(err.code)")
""",
        "Swift 6 da barcha Actor va Task lar orasida tashlanadigan Error lar 'Sendable' bo'lishi qat'iy talab qilinadi.",
        """Sendable xatolik parallel oqimlarda xavfsiz uzatiladi: 503"""
    ),
    (
        584,
        "Sanitizatsiya: Ichki xatoliklarni xavfsizlantirish",
        "Serverdagi maxfiy SQL yoki xotira xatolarini foydalanuvchiga ko'rsatmasdan xavfsiz xabarga aylantirish.",
        """import Foundation

func sanitizeError(_ error: Error) -> String {
    // Maxfiy ma'lumotlarni yashirish
    return "Xizmatda vaqtinchalik nosozlik yuz berdi. Qaytadan urinib ko'ring."
}

let userMsg = sanitizeError(URLError(.cannotConnectToHost))
print("Foydalanuvchiga ko'rsatiladigan matn: \\(userMsg)")
""",
        "Xavfsizlik talablariga ko'ra ichki drayver xatolari loglanadi, ammo foydalanuvchiga umumiy xavfsiz xabar beriladi.",
        """Foydalanuvchiga ko'rsatiladigan matn: Xizmatda vaqtinchalik nosozlik yuz berdi. Qaytadan urinib ko'ring."""
    ),
    (
        585,
        "Standart kutubxona xatolari bilan ishlash: POSIXError",
        "Tizim darajasidagi fayl va ruxsat xatoliklarini ushlash.",
        """import Foundation

let posix = POSIXError(.EACCES)
print("Tizim kodi: \\(posix.code.rawValue)")
""",
        "Swift Foundation operatsion tizim POSIX xatoliklarini to'liq integratsiya qilgan.",
        """Tizim kodi: 13"""
    ),
    (
        586,
        "Xatoliklarni zanjirli tekshirish",
        "Bir nechta throwing funksiyalarni bitta do blokida sinab ko'rish.",
        """import Foundation

func stepOne() throws { print("1-qadam OK") }
func stepTwo() throws { print("2-qadam OK") }

do {
    try stepOne()
    try stepTwo()
} catch {
    print("Zanjirda xato: \\(error)")
}
""",
        "Bitta do bloki ichida bir nechta try chaqiruvlari ketma-ket yozilishi mumkin; birinchisi xato bersa darhol catch ga sakraydi.",
        """1-qadam OK
2-qadam OK"""
    ),
    (
        587,
        "Custom Xatolik sinfi (Class-based Error)",
        "Merosxo'rlikka ega bo'lgan klass xatoliklar ierarxiyasi.",
        """import Foundation

class BaseAppError: Error {
    let timestamp = Date()
}

class DatabaseTimeoutError: BaseAppError {}

let e = DatabaseTimeoutError()
print("Sinf asosidagi xatolik: \\(type(of: e))")
""",
        "Xatoliklar sinf sifatida ham yaratilishi mumkin, biroq Swift-da enum va struct lar ancha yengil va afzalroqdir.",
        """Sinf asosidagi xatolik: DatabaseTimeoutError"""
    ),
    (
        588,
        "Throwing funksiyada defer ning o'rni",
        "Funksiya muvaffaqiyatli bo'lsa ham, xato bilan to'xtasa ham bajariluvchi defer bloki.",
        """import Foundation

func trackedExecution() throws {
    defer { print("Auditor: Harakat qaydnomasi saqlandi.") }
    print("Asosiy ish bajarildi.")
}

try? trackedExecution()
""",
        "Defer throwing arxitekturasida resurslarni tozalash va audit uchun eng asosiy vositadir.",
        """Asosiy ish bajarildi.
Auditor: Harakat qaydnomasi saqlandi."""
    ),
    (
        589,
        "Failable initsializator va throwing initsializator taqqoslanishi",
        "Qachon init? va qachon init throws tanlash lozimligini ko'rsating.",
        """import Foundation

struct UserByInit {
    let name: String
    init?(optionalName: String) {
        guard !optionalName.isEmpty else { return nil }
        self.name = optionalName
    }
}

print("Oddiy holatlarda init?, aniq xato sababi kerak bo'lsa init throws tanlanadi.")
""",
        "Init? sabab muhim bo'lmaganda tanlanadi, agar chaqiruvchiga nima sababdan to'xtagani kerak bo'lsa throws tanlanadi.",
        """Oddiy holatlarda init?, aniq xato sababi kerak bo'lsa init throws tanlanadi."""
    ),
    (
        590,
        "Result ichidagi qiymatni o'zgartiruvchi: Result.map",
        "Muvaffaqiyat qiymatini o'zgartirish.",
        """import Foundation

let res: Result<Int, Error> = .success(10)
let mapped = res.map { $0 * 5 }

print("Mapped result: \\(try? mapped.get() ?? 0)")
""",
        "Result.map agar natija success bo'lsa ichidagi qiymatni o'zgartiradi.",
        """Mapped result: 50"""
    ),
    (
        591,
        "Result ichidagi qiymatni filtrlovchi utilita",
        "Shart bajarilmasa failure ga o'giruvchi extension.",
        """import Foundation

extension Result {
    func filter(predicate: (Success) -> Bool, error: Failure) -> Result<Success, Failure> {
        switch self {
        case .success(let val):
            return predicate(val) ? self : .failure(error)
        case .failure:
            return self
        }
    }
}

enum CustomErr: Error { case notMatching }
let filtered = Result<Int, CustomErr>.success(5).filter(predicate: { $0 > 10 }, error: .notMatching)
print("Filtrlandi: \\(filtered)")
""",
        "Kengaytmalar orqali Result turi funktsional operatorlar bilan boyitiladi.",
        """Filtrlandi: failure(main.CustomErr.notMatching)"""
    ),
    (
        592,
        "Asinxron ketma-ketlikda xatoliklar (AsyncSequence throws)",
        "Oqimli ma'lumot kelayotganda xatolikni ushlash.",
        """import Foundation

print("AsyncSequence elementlari xatolik tashlashi mumkin va 'for try await' bilan o'qiladi.")
""",
        "AsyncSequence orqali tokenlar oqimi o'qilayotganda tarmoq uzilsa 'for try await' catch ga tushadi.",
        """AsyncSequence elementlari xatolik tashlashi mumkin va 'for try await' bilan o'qiladi."""
    ),
    (
        593,
        "Xatoliklarni metama'lumot bilan boyituvchi wrapper",
        "Xatolik qaysi fayl va qatorda ro'y berganini qayd etuvchi model.",
        """import Foundation

struct ContextualError: Error {
    let underlyingError: Error
    let file: String
    let line: Int
}

let wrapped = ContextualError(underlyingError: URLError(.badURL), file: "Network.swift", line: 42)
print("Xato manzili: \\(wrapped.file):\\(wrapped.line)")
""",
        "Xatolik kontekstini yozib borish nosozliklarni izlashda tengsiz yordam beradi.",
        """Xato manzili: Network.swift:42"""
    ),
    (
        594,
        "Shartli xato tashlovchi assert o'rnini bosuvchi funksiya",
        "Ishlab chiqish muhitida nosozlikni aniq xato sifatida tashlash.",
        """import Foundation

func requireCondition(_ condition: Bool, error: Error) throws {
    if !condition { throw error }
}

print("Shart tekshiruvi tayyorlandi.")
""",
        "Kodni xavfsiz invariantlar bilan to'ldirish nosozliklarni erta aniqlaydi.",
        """Shart tekshiruvi tayyorlandi."""
    ),
    (
        595,
        "Swift 5.9 Typed throws va Exhaustive Catch",
        "Aniq xatolik turi ko'rsatilganda kompilyator barcha holatlarni tekshirishni talab qilishi.",
        """import Foundation

enum DiskState: Error { case full, corrupted }

func writeData() throws(DiskState) {
    throw .full
}

do {
    try writeData()
} catch .full {
    print("Disk to'la!")
} catch .corrupted {
    print("Disk buzilgan!")
}
// 'default' yoki umumiy 'catch' shart emas, chunki DiskState to'liq yopildi!
""",
        "Swift 5.9 Typed Throws ning eng katta ustunligi: barcha xatolik holatlari switch kabi to'liq (exhaustive) yopilgach, umumiy catch yozish talab etilmaydi.",
        """Disk to'la!"""
    ),
    (
        596,
        "Xatolikni qayta ishlashda LIFO defer zanjiri",
        "Xatolik ro'y bergan paytda bir nechta defer larning teskari tartibda bajarilishi.",
        """import Foundation

func deferChain() throws {
    defer { print("1. Birinchi defer") }
    defer { print("2. Ikkinchi defer") }
    enum Dummy: Error { case err }
    throw Dummy.err
}

try? deferChain()
""",
        "Defer bloklari doimo LIFO tartibida resurslarni tozalaydi.",
        """2. Ikkinchi defer
1. Birinchi defer"""
    ),
    (
        597,
        "Tarmoq holati xatolarini foydalanuvchiga formatlash",
        "Foydalanuvchi interfeysi uchun qulay xatolik matnlarini tayyorlash.",
        """import Foundation

func formatErrorForUI(_ error: Error) -> String {
    if let urlError = error as? URLError, urlError.code == .notConnectedToInternet {
        return "Internet aloqasi yo'q. Wi-Fi ni tekshiring."
    }
    return "Noma'lum xatolik yuz berdi."
}

let msg = formatErrorForUI(URLError(.notConnectedToInternet))
print(msg)
""",
        "Foydalanuvchi tajribasida (UX) tushunarli xabarlar ko'rsatish eng muhim qoidadir.",
        """Internet aloqasi yo'q. Wi-Fi ni tekshiring."""
    ),
    (
        598,
        "Non-throwing metodni throwing bilan override qilib bo'lmasligi",
        "Merosxo'rlikda xavfsizlik cheklovining buzilmasligini tushuntiring.",
        """import Foundation

class BaseTask {
    func run() { print("Xavfsiz baza vazifa") }
}

class ExtendedTask: BaseTask {
    // override func run() throws // KOMPILYATSIYA XATOSI!
}

print("Ota sinfda throws bo'lmasa, bola sinf unga throws qo'sha olmaydi.")
""",
        "Chunki ota sinfni kutayotgan mijoz kod 'try' siz chaqiradi. Agar subclass xato tashlasa butun arxitektura buziladi.",
        """Ota sinfda throws bo'lmasa, bola sinf unga throws qo'sha olmaydi."""
    ),
    (
        599,
        "Xatolik ob'ektining Hashable bo'lishi",
        "Xatoliklarni Set yoki Dictionary ga solish imkoniyati.",
        """import Foundation

enum UniqueError: Error, Hashable {
    case timeout(code: Int)
}

var seenErrors: Set<UniqueError> = []
seenErrors.insert(.timeout(code: 408))
seenErrors.insert(.timeout(code: 408))
print("Unikal xatolar soni: \\(seenErrors.count)")
""",
        "Hashable xatoliklar bir xil xatoliklarni qayta-qayta loglamaslikda juda qulaydir.",
        """Unikal xatolar soni: 1"""
    ),
    (
        600,
        "Amaliy loyiha: Foydalanuvchi to'lovi va Bank API xatoliklarini to'liq boshqaruvchi tranzaksiya moduli",
        "Kredit karta, balans, server xatoliklari, LocalizedError va Retry mexanizmini o'z ichiga olgan mukammal to'lov tranzaksiyasi arxitekturasi.",
        """import Foundation

enum PaymentGatewayError: LocalizedError {
    case invalidCard(number: String)
    case insufficientFunds(required: Double, available: Double)
    case networkTimeout
    
    var errorDescription: String? {
        switch self {
        case .invalidCard(let num):
            return "Noto'g'ri karta raqami: \\(num)"
        case .insufficientFunds(let req, let avail):
            return "Mablag' yetarli emas! Kerak: $\\(req), Mavjud: $\\(avail)"
        case .networkTimeout:
            return "Bank serveri bilan aloqa vaqti tugadi."
        }
    }
}

class PaymentProcessor {
    var userBalance = 300.0
    
    func executeTransaction(cardNumber: String, amount: Double) throws {
        guard cardNumber.count == 16 else {
            throw PaymentGatewayError.invalidCard(number: cardNumber)
        }
        guard amount <= userBalance else {
            throw PaymentGatewayError.insufficientFunds(required: amount, available: userBalance)
        }
        
        userBalance -= amount
        print("TO'LOV MUVAFFAQIShI: $\\(amount) yechildi. Yangi balans: $\\(userBalance)")
    }
}

let processor = PaymentProcessor()

print("=== TO'LOV JARAYONI ===")
do {
    try processor.executeTransaction(cardNumber: "8600123456789012", amount: 150.0)
    try processor.executeTransaction(cardNumber: "8600123456789012", amount: 500.0) // Mablag' yetarli emas
} catch let error as PaymentGatewayError {
    print("[XATOLIK]: \\(error.localizedDescription)")
} catch {
    print("[BOSHQARILMAGAN XATO]: \\(error)")
}
""",
        "Ushbu yakuniy loyihada 'Error', 'LocalizedError', 'throws', 'do-catch' va 'guard' mexanizmlari real bank tranzaksiyasi xavfsizligini 100% ta'minladi.",
        """=== TO'LOV JARAYONI ===
TO'LOV MUVAFFAQIShI: $150.0 yechildi. Yangi balans: $150.0
[XATOLIK]: Mablag' yetarli emas! Kerak: $500.0, Mavjud: $150.0"""
    )
]

tasks = [format_task(*t) for t in tasks_data]
save_file("swift_12_xatoliklarni_boshqarish_error_handling.md", tasks)
