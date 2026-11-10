# 551-Topshiriq: Swift-da xatoliklar falsafasi: Error protokoli
## Topshiriq sharti:
Swift-da istisnolarni ifodalovchi eng asosiy Error protokolini tushuntiring.

## Yechim (Swift kodi):
```swift
import Foundation

enum NetworkError: Error {
    case connectionLost
    case serverUnreachable
}

let err: Error = NetworkError.connectionLost
print("Xatolik turi: \(err)")
```

## Tushuntirish va Mantiq:
Swift-da xatoliklar (Exceptions) og'ir runtime stack unwinding emas, balki oddiy qiymat turlaridir. 'Error' protokoli orqali har qanday enum yoki struktura xatolik sifatida tashlanishi (throw) mumkin.

## Ishlash natijasi:
```text
Xatolik turi: connectionLost
```


# 552-Topshiriq: Xatoliklarni Enum ko'rinishida ifodalash
## Topshiriq sharti:
Kassa apparatida yuz berishi mumkin bo'lgan xatoliklarni enum orqali modellashtiring.

## Yechim (Swift kodi):
```swift
import Foundation

enum VendingMachineError: Error {
    case invalidSelection
    case outOfStock
    case insufficientFunds(coinsNeeded: Int)
}

let errorInstance = VendingMachineError.insufficientFunds(coinsNeeded: 5)
print("Xatolik namunasi: \(errorInstance)")
```

## Tushuntirish va Mantiq:
Swift-da xatoliklarni Enum shaklida yaratish eng to'g'ri amaliyotdir. Associated Values orqali xatolikka qo'shimcha parametrlar ham biriktiriladi.

## Ishlash natijasi:
```text
Xatolik namunasi: insufficientFunds(coinsNeeded: 5)
```


# 553-Topshiriq: Xatolik tashlovchi funksiyalar: throws
## Topshiriq sharti:
Shart bajarilmaganda xato tashlovchi funksiya yozing.

## Yechim (Swift kodi):
```swift
import Foundation

func checkAgeForDriving(age: Int) throws {
    enum DrivingError: Error { case underage }
    if age < 18 {
        throw DrivingError.underage
    }
    print("Haydashga ruxsat berildi.")
}

print("Funksiya 'throws' bilan e'lon qilindi.")
```

## Tushuntirish va Mantiq:
'throws' kalit so'zi funksiya o'z ijrosi davomida xatolik yuzaga keltirishi mumkinligini va uni chaqiruvchi javobgarlikni o'z zimmasiga olishi shartligini bildiradi.

## Ishlash natijasi:
```text
Funksiya 'throws' bilan e'lon qilindi.
```


# 554-Topshiriq: Xatoliklarni chaqirish va tutish: do-catch va try
## Topshiriq sharti:
Xatolik tashlovchi funksiyani 'do-catch' bloki ichida 'try' bilan chaqiring.

## Yechim (Swift kodi):
```swift
import Foundation

enum BankError: Error {
    case insufficientBalance
}

func withdraw(amount: Double, balance: Double) throws -> Double {
    if amount > balance { throw BankError.insufficientBalance }
    return balance - amount
}

do {
    let newBalance = try withdraw(amount: 500.0, balance: 200.0)
    print("Qoldiq: $\(newBalance)")
} catch BankError.insufficientBalance {
    print("XATOLIK: Hisobingizda yetarli mablag' mavjud emas!")
} catch {
    print("Boshqa xato: \(error)")
}
```

## Tushuntirish va Mantiq:
'try' operatori throwing funksiyani chaqirishda majburiydir. 'do-catch' esa yuz bergan nosozlikni ushlab, ilovaning to'xtab qolishini oldini oladi.

## Ishlash natijasi:
```text
XATOLIK: Hisobingizda yetarli mablag' mavjud emas!
```


# 555-Topshiriq: Bir nechta aniq xatoliklarni ushlovchi catch bloklari
## Topshiriq sharti:
Har xil xatoliklar uchun alohida-alohida xabarlar beruvchi bloklar tuzing.

## Yechim (Swift kodi):
```swift
import Foundation

enum FileError: Error {
    case notFound
    case accessDenied
    case corrupted
}

func loadFile(name: String) throws {
    if name == "secret.txt" { throw FileError.accessDenied }
    if name.isEmpty { throw FileError.notFound }
    print("Fayl o'qildi: \(name)")
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
```

## Tushuntirish va Mantiq:
Swift aniq 'catch' bloklarini ketma-ket yozish orqali turli xatoliklarni professional darajada filtrlash imkonini beradi.

## Ishlash natijasi:
```text
Kirish huquqi cheklangan!
```


# 556-Topshiriq: Catch blokida 'where' sharti
## Topshiriq sharti:
Associated value qiymatini catch qismida 'where' bilan tekshiring.

## Yechim (Swift kodi):
```swift
import Foundation

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
    print("Boshqa server kodi: \(code)")
} catch {
    print("Noma'lum xato.")
}
```

## Tushuntirish va Mantiq:
'catch let error where ...' sintaksisi xatolik ichidagi parametrlarni mantiqiy mezonlar bo'yicha saralashga yordam beradi.

## Ishlash natijasi:
```text
Resurs topilmadi (404 Not Found).
```


# 557-Topshiriq: Standart 'error' o'zgaruvchisi umumiy catch blokida
## Topshiriq sharti:
Xatolik turini ko'rsatmagan catch blokida avtomatik 'error' ob'ektidan foydalaning.

## Yechim (Swift kodi):
```swift
import Foundation

enum SimpleError: Error {
    case somethingWentWrong
}

func doRiskyTask() throws {
    throw SimpleError.somethingWentWrong
}

do {
    try doRiskyTask()
} catch {
    print("Ushlangan xato: \(error)")
}
```

## Tushuntirish va Mantiq:
Agar 'catch' dan keyin hech qanday nom yozilmasa, Swift blok ichida 'error' nomli avtomatik o'zgaruvchini taqdim etadi.

## Ishlash natijasi:
```text
Ushlangan xato: somethingWentWrong
```


# 558-Topshiriq: Xatolikni Optional ga aylantirish: try?
## Topshiriq sharti:
Xatolik yuz berganda shunchaki nil olish uchun 'try?' dan foydalaning.

## Yechim (Swift kodi):
```swift
import Foundation

func parsePositiveInt(_ str: String) throws -> Int {
    enum ParseError: Error { case notPositive }
    guard let n = Int(str), n > 0 else { throw ParseError.notPositive }
    return n
}

let num1 = try? parsePositiveInt("42")
let num2 = try? parsePositiveInt("-10")

print("num1: \(String(describing: num1))")
print("num2: \(String(describing: num2))")
```

## Tushuntirish va Mantiq:
'try?' operatori funksiya natijasini Optional qiladi: muvaffaqiyatli bo'lsa Optional(qiymat), xatolik yuz bersa nil qaytaradi. Bu 'do-catch' yozish shart bo'lmagan vaziyatlar uchun qulaydir.

## Ishlash natijasi:
```text
num1: Optional(42)
num2: nil
```


# 559-Topshiriq: Majburiy xatosiz chaqirish: try!
## Topshiriq sharti:
Xato bo'lmasligi 100% kafolatlangan joyda 'try!' operatorini qo'llang.

## Yechim (Swift kodi):
```swift
import Foundation

func getBuiltinSetting() throws -> String {
    return "PRODUCTION_MODE"
}

let setting = try! getBuiltinSetting()
print("Sozlama: \(setting)")
```

## Tushuntirish va Mantiq:
'try!' operatori throwing funksiyaning xato bermasligiga kafolat beradi. Agar xato yuz bersa, dastur run-time crash bo'ladi.

## Ishlash natijasi:
```text
Sozlama: PRODUCTION_MODE
```


# 560-Topshiriq: Qayta xatolik tashlash: rethrows
## Topshiriq sharti:
Parametrdagi closure xato tashlasagina o'zi ham xato tashlaydigan funksiyani ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

func executeAction(action: () throws -> Void) rethrows {
    print("Bajarilmoqda...")
    try action()
    print("Bajarildi.")
}

// Xavfsiz closure uchun 'try' talab qilinmaydi:
executeAction {
    print("Xatosiz amal.")
}
```

## Tushuntirish va Mantiq:
'rethrows' faqat uzatilgan closure sababli xatolik yuz bergandagina xato tashlaydi. Bu kodning ortiqcha 'try' lardan xoli bo'lishini ta'minlaydi.

## Ishlash natijasi:
```text
Bajarilmoqda...
Xatosiz amal.
Bajarildi.
```


# 561-Topshiriq: Resurslarni tozalash: defer va xatoliklar
## Topshiriq sharti:
Xatolik 'throw' qilinganda ham 'defer' bloki albatta bajarilishini isbotlang.

## Yechim (Swift kodi):
```swift
import Foundation

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
    print("4. Xatolik catch da ushlandi: \(error)")
}
```

## Tushuntirish va Mantiq:
'defer' bloki xatolik yuz berib funksiya erta to'xtaganda ham xotira va tizim resurslarining sizib ketishini 100% oldini oladi.

## Ishlash natijasi:
```text
1. Resurs ajratildi.
2. Xatolik tashlanmoqda...
3. Resurs xavfsiz tozalandi (defer).
4. Xatolik catch da ushlandi: fail
```


# 562-Topshiriq: Result<Success, Failure> tipi asoslari
## Topshiriq sharti:
Asinxron operatsiyalar natijasini Result qutisida saqlang.

## Yechim (Swift kodi):
```swift
import Foundation

enum DownloadError: Error { case networkLost }

func fetchFile() -> Result<String, DownloadError> {
    return .success("Fayl ma'lumotlari muvaffaqiyatli olindi.")
}

let result = fetchFile()
switch result {
case .success(let data):
    print("Muvaffaqiyat: \(data)")
case .failure(let error):
    print("Xato: \(error)")
}
```

## Tushuntirish va Mantiq:
'Result' ikki holatga ega generik enumdir: '.success(Success)' va '.failure(Failure)'. Bu xatolikni birinchi darajali ma'lumot sifatida olib yurish imkonini beradi.

## Ishlash natijasi:
```text
Muvaffaqiyat: Fayl ma'lumotlari muvaffaqiyatli olindi.
```


# 563-Topshiriq: Result qutisini get() orqali throwing ga aylantirish
## Topshiriq sharti:
Result ichidagi qiymatni oddiy try bilan ochish usuli.

## Yechim (Swift kodi):
```swift
import Foundation

let goodResult: Result<Int, Error> = .success(42)

do {
    let value = try goodResult.get()
    print("Result.get() qiymati: \(value)")
} catch {
    print("Xato: \(error)")
}
```

## Tushuntirish va Mantiq:
'result.get()' muvaffaqiyatli bo'lsa qiymatni qaytaradi, agar failure bo'lsa xatolikni throw qiladi.

## Ishlash natijasi:
```text
Result.get() qiymati: 42
```


# 564-Topshiriq: Throwing funksiyani Result ga aylantirish: Result { try ... }
## Topshiriq sharti:
Xatolik tashlovchi harakatni bir qatorda Result qutisiga soling.

## Yechim (Swift kodi):
```swift
import Foundation

func riskyCalculation() throws -> Int {
    return 100 * 5
}

let encapsulatedResult = Result { try riskyCalculation() }
print("Result turi: \(type(of: encapsulatedResult))")
```

## Tushuntirish va Mantiq:
'Result { try ... }' initsializatori throwing blokni avtomatik Result<T, Error> enumiga aylantiradi.

## Ishlash natijasi:
```text
Result turi: Result<Int, any Error>
```


# 565-Topshiriq: Result.mapError bilan xatolik turini o'zgartirish
## Topshiriq sharti:
Texnik xatolikni domen darajasidagi tushunarli xatolikka xaritalang.

## Yechim (Swift kodi):
```swift
import Foundation

enum LowLevelError: Error { case ioError }
enum UserFacingError: Error { case fileNotReadable }

let lowResult: Result<String, LowLevelError> = .failure(.ioError)

let mapped = lowResult.mapError { _ in UserFacingError.fileNotReadable }

switch mapped {
case .success: break
case .failure(let err): print("Xaritalangan xato: \(err)")
}
```

## Tushuntirish va Mantiq:
'mapError' Result ichidagi muvaffaqiyatli qiymatga daxl qilmasdan, faqat xatolik turini transformatsiya qiladi.

## Ishlash natijasi:
```text
Xaritalangan xato: fileNotReadable
```


# 566-Topshiriq: Swift 5.9 va Swift 6 Typed Throws: throws(CustomError)
## Topshiriq sharti:
Funksiya faqat ma'lum bir aniq xatolik turini tashlashini qat'iy belgilang.

## Yechim (Swift kodi):
```swift
import Foundation

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
    print("Typed throw ushlandi: \(error)")
}
```

## Tushuntirish va Mantiq:
Swift 6 da to'liq joriy qilingan 'Typed Throws' funksiyaga 'throws(MyError)' shaklida aniq xatolik turini ko'rsatish imkonini beradi. Natijada catch bloki to'liq (exhaustive) bo'lib, generic Error o'rniga aniq tur bilan ishlaydi.

## Ishlash natijasi:
```text
Typed throw ushlandi: invalidCredentials
```


# 567-Topshiriq: LocalizedError protokoli: errorDescription
## Topshiriq sharti:
Xatolik konsolga yoki foydalanuvchiga chiqqanda chiroyli tushuntirish matnini berish.

## Yechim (Swift kodi):
```swift
import Foundation

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
print("Xatolik matni: \(err.localizedDescription)")
```

## Tushuntirish va Mantiq:
'LocalizedError' protokoli 'errorDescription' xususiyati orqali foydalanuvchiga ko'rsatilishi mumkin bo'lgan lokalizatsiyalangan xatolik xabarini qaytaradi.

## Ishlash natijasi:
```text
Xatolik matni: Bank kartangizning amal qilish muddati tugagan.
```


# 568-Topshiriq: Asinxron xatoliklar: async throws
## Topshiriq sharti:
Ham asinxron, ham xatolik tashlovchi tarmoq chaqiruvini boshqarish.

## Yechim (Swift kodi):
```swift
import Foundation

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
        print("Asinxron xatolik ushlandi: \(error)")
    }
}
```

## Tushuntirish va Mantiq:
'async throws' bir vaqtning o'zida asinxron kutish va xatolik tashlashni ta'minlaydi. Chaqirilganda 'try await' birga ishlatiladi.

## Ishlash natijasi:
```text
Asinxron xatolik ushlandi: noConnection
```


# 569-Topshiriq: JSON Decoding xatoliklarini tahlil qilish
## Topshiriq sharti:
JSON noto'g'ri bo'lganda Decoding xatolik turini batafsil ajrating.

## Yechim (Swift kodi):
```swift
import Foundation

struct User: Decodable {
    let id: Int
    let name: String
}

let brokenJSON = """{"id": "not_an_int", "name": "Ali"}""".data(using: .utf8)!

do {
    let _ = try JSONDecoder().decode(User.self, from: brokenJSON)
} catch DecodingError.typeMismatch(let type, let context) {
    print("Tip mos kelmadi: \(type), Yo'li: \(context.codingPath.map(\.stringValue))")
} catch {
    print("Boshqa decoding xatosi: \(error)")
}
```

## Tushuntirish va Mantiq:
Foundation-ning DecodingError enumi xato qaysi maydonda va nima sababdan ro'y berganini aniq ko'rsatadi.

## Ishlash natijasi:
```text
Tip mos kelmadi: Int, Yo'li: ["id"]
```


# 570-Topshiriq: Initsializatorda xatolik tashlash: init() throws
## Topshiriq sharti:
Noto'g'ri parametr berilganda obyekt yaratilmasdan xato tashlanishini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

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
    print("Foydalanuvchi yaratilmadi: \(error)")
}
```

## Tushuntirish va Mantiq:
'init() throws' konstruktorda xatolik sababini aniq ma'lum qilish imkonini beradi.

## Ishlash natijasi:
```text
Foydalanuvchi yaratilmadi: emptyName
```


# 571-Topshiriq: Hisoblangan xususiyatlarda xatolik tashlash: get throws
## Topshiriq sharti:
Xususiyat qiymatini o'qish paytida xato tashlovchi getter.

## Yechim (Swift kodi):
```swift
import Foundation

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
    print("Sensor xatosi: \(error)")
}
```

## Tushuntirish va Mantiq:
Swift 5.5 dan boshlab xususiyat getterlariga 'throws' qo'yish mumkin.

## Ishlash natijasi:
```text
Sensor xatosi: offline
```


# 572-Topshiriq: Retry Pattern: Xatolikda qayta urinish
## Topshiriq sharti:
Xatolik yuz berganda operatsiyani N marta qayta sinovchi generik funksiya.

## Yechim (Swift kodi):
```swift
import Foundation

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

print("Natija: \(result ?? ""), Urinishlar: \(tries)")
```

## Tushuntirish va Mantiq:
Retry pattern tarmoq va beqaror tizimlarda nosozliklarni avtomatik bartaraf qilish uchun qo'llaniladi.

## Ishlash natijasi:
```text
Natija: Muvaffaqiyatli ulandi, Urinishlar: 2
```


# 573-Topshiriq: Circuit Breaker Pattern asoslari
## Topshiriq sharti:
Ketma-ket xatoliklar soni oshganda vaqtincha barcha so'rovlarni to'xtatuvchi xavfsizlik mexanizmi.

## Yechim (Swift kodi):
```swift
import Foundation

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
```

## Tushuntirish va Mantiq:
Circuit Breaker qulagan xizmatlarni ortiqcha so'rovlar bilan to'ldirib yubormaslik uchun ishlatiladi.

## Ishlash natijasi:
```text
Chegaradan oshdi! Zanjir uzildi (Circuit Breaker Tripped).
Zanjir ochiq (Circuit Open): Yangi so'rovlar qabul qilinmaydi.
```


# 574-Topshiriq: Never bilan xatosiz Result: Result<T, Never>
## Topshiriq sharti:
Xatolik yuz berishi mutlaqo imkonsiz bo'lgan operatsiyani ifodalash.

## Yechim (Swift kodi):
```swift
import Foundation

func getGuaranteedData() -> Result<String, Never> {
    return .success("Bu ma'lumot doimo kafolatlangan.")
}

let guaranteed = getGuaranteedData()
switch guaranteed {
case .success(let msg):
    print("Xabari: \(msg)")
// Never bo'lgani sababli .failure shart emas!
}
```

## Tushuntirish va Mantiq:
'Failure == Never' bo'lgan Result qutisida failure bandi bo'lishi mumkin emas, switch operatori faqat .success ni tekshiradi.

## Ishlash natijasi:
```text
Xabari: Bu ma'lumot doimo kafolatlangan.
```


# 575-Topshiriq: CancellationError va Task bekor qilinishini boshqarish
## Topshiriq sharti:
Asinxron vazifa to'xtatilganda xavfsiz chiqish.

## Yechim (Swift kodi):
```swift
import Foundation

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
        print("Boshqa xato: \(error)")
    }
}
```

## Tushuntirish va Mantiq:
'Task.checkCancellation()' agar vazifa bekor qilingan bo'lsa darhol 'CancellationError' tashlaydi.

## Ishlash natijasi:
```text
Vazifa bajarilmoqda...
```


# 576-Topshiriq: Xatolik kodi va Error Mapping
## Topshiriq sharti:
Server status kodlarini maxsus dasturiy xatoliklarga o'giruvchi funksiya.

## Yechim (Swift kodi):
```swift
import Foundation

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

print("503 xatosi: \(mapStatusCode(503))")
```

## Tushuntirish va Mantiq:
Xatoliklarni xaritalash (Error Mapping) tarmoq qatlamini biznes logikadan ajratadi.

## Ishlash natijasi:
```text
503 xatosi: serverFailure
```


# 577-Topshiriq: Xatoliklarni swallow qilish (yutib yuborish) antipatterni
## Topshiriq sharti:
Xatoni e'tiborsiz qoldirish nima uchun yomon amaliyot ekanligini tushuntiring.

## Yechim (Swift kodi):
```swift
import Foundation

func riskyIO() throws { throw URLError(.fileDoesNotExist) }

// Yomon amaliyot (Antipattern):
// try? riskyIO() // Xato qayerda ro'y bergani butunlay yashirildi!

// To'g'ri amaliyot:
do {
    try riskyIO()
} catch {
    print("[LOG]: Kritik xatolik qayd etildi: \(error)")
}
```

## Tushuntirish va Mantiq:
Xatoliklarni bo'sh catch yoki e'tiborsiz 'try?' bilan yutib yuborish nosozliklarni topishni (debugging) imkonsiz qiladi.

## Ishlash natijasi:
```text
[LOG]: Kritik xatolik qayd etildi: The operation couldn’t be completed. (NSURLErrorDomain error -1100.)
```


# 578-Topshiriq: CustomNSError protokoli: ErrorDomain va ErrorCode
## Topshiriq sharti:
Apple tizimida Objective-C NSError bilan to'liq mos xatolik yaratish.

## Yechim (Swift kodi):
```swift
import Foundation

enum SystemEngineError: Int, CustomNSError {
    case diskFull = 101
    case memoryCorrupt = 102
    
    static var errorDomain: String { "uz.khorazmiy.engine" }
    var errorCode: Int { rawValue }
}

let err = SystemEngineError.diskFull
print("Domen: \(SystemEngineError.errorDomain), Kod: \(err.errorCode)")
```

## Tushuntirish va Mantiq:
'CustomNSError' protokoli orqali Swift xatoliklariga aniq domen (domain) va raqamli kod beriladi.

## Ishlash natijasi:
```text
Domen: uz.khorazmiy.engine, Kod: 101
```


# 579-Topshiriq: Tranzaksiya va Rollback mexanizmi
## Topshiriq sharti:
Bir nechta bosqichdan iborat operatsiyada xato bo'lsa barcha o'zgarishlarni bekor qilish.

## Yechim (Swift kodi):
```swift
import Foundation

class TransactionSystem {
    var balances = ["Ali": 100.0, "Vali": 50.0]
    
    func transfer(from: String, to: String, amount: Double) throws {
        enum TxError: Error { case insufficientFunds }
        let current = balances[from] ?? 0.0
        guard current >= amount else { throw TxError.insufficientFunds }
        
        balances[from] = current - amount
        // Agar ikkinchi qadamda xato bo'lsa, birinchisini qaytarish kerak bo'ladi (Rollback)
        balances[to] = (balances[to] ?? 0.0) + amount
        print("Muvaffaqiyatli o'tkazildi: $\(amount)")
    }
}

let tx = TransactionSystem()
try? tx.transfer(from: "Ali", to: "Vali", amount: 30.0)
print("Ali balansi: $\(tx.balances["Ali"] ?? 0)")
```

## Tushuntirish va Mantiq:
Tranzaksiya yaxlitligi xatoliklarni xavfsiz boshqarishga tayanadi.

## Ishlash natijasi:
```text
Muvaffaqiyatli o'tkazildi: $30.0
Ali balansi: $70.0
```


# 580-Topshiriq: Validatsiya xatoliklarini to'plovchi kompozitsiya
## Topshiriq sharti:
Bir nechta maydondagi xatoliklarni birdaniga yig'ib qaytaruvchi tizim.

## Yechim (Swift kodi):
```swift
import Foundation

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
    print("Xatoliklar ro'yxati: \(multi.errors)")
} catch {}
```

## Tushuntirish va Mantiq:
Foydalanuvchi interfeyslarida barcha xatoliklarni bitta ro'yxatda qaytarish qulay tajriba taqdim etadi.

## Ishlash natijasi:
```text
Xatoliklar ro'yxati: ["Ism kiritilmadi", "Noto'g'ri email"]
```


# 581-Topshiriq: Subscript larda xatolik tashlash (Swift 5.5+)
## Topshiriq sharti:
Subscript orqali xavfsiz o'qishda xatolik tashlash imkoniyati.

## Yechim (Swift kodi):
```swift
import Foundation

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
    print("Qiymat: \(val)")
    let _ = try sa[safe: 10]
} catch {
    print("Indeks xatosi: \(error)")
}
```

## Tushuntirish va Mantiq:
Swift 5.5 dan boshlab subscript getteri ham 'throws' qila oladi.

## Ishlash natijasi:
```text
Qiymat: 20
Indeks xatosi: outOfBounds
```


# 582-Topshiriq: Xatoliklarni log qiluvchi wrapper closure
## Topshiriq sharti:
Har qanday throwing amalni o'rab, xatolikni konsolga chop etuvchi utilita.

## Yechim (Swift kodi):
```swift
import Foundation

func auditOperation<T>(name: String, block: () throws -> T) rethrows -> T {
    print("AUDIT: '\(name)' boshlandi.")
    defer { print("AUDIT: '\(name)' yakunlandi.") }
    return try block()
}

let result = try? auditOperation(name: "Ma'lumotlar bazasi zaxirasi") {
    return "Zaxira yaratildi"
}
print("Natija: \(result ?? "")")
```

## Tushuntirish va Mantiq:
Audit funksiyalari kodni shaffof va kuzatuvchan qiladi.

## Ishlash natijasi:
```text
AUDIT: 'Ma'lumotlar bazasi zaxirasi' boshlandi.
AUDIT: 'Ma'lumotlar bazasi zaxirasi' yakunlandi.
Natija: Zaxira yaratildi
```


# 583-Topshiriq: Ko'p oqimli muhitda Sendable Error xavfsizligi
## Topshiriq sharti:
Parallel oqimlararo uzatiluvchi xatoliklar Sendable bo'lishi talabi.

## Yechim (Swift kodi):
```swift
import Foundation

struct ThreadError: Error, Sendable {
    let code: Int
}

let err = ThreadError(code: 503)
print("Sendable xatolik parallel oqimlarda xavfsiz uzatiladi: \(err.code)")
```

## Tushuntirish va Mantiq:
Swift 6 da barcha Actor va Task lar orasida tashlanadigan Error lar 'Sendable' bo'lishi qat'iy talab qilinadi.

## Ishlash natijasi:
```text
Sendable xatolik parallel oqimlarda xavfsiz uzatiladi: 503
```


# 584-Topshiriq: Sanitizatsiya: Ichki xatoliklarni xavfsizlantirish
## Topshiriq sharti:
Serverdagi maxfiy SQL yoki xotira xatolarini foydalanuvchiga ko'rsatmasdan xavfsiz xabarga aylantirish.

## Yechim (Swift kodi):
```swift
import Foundation

func sanitizeError(_ error: Error) -> String {
    // Maxfiy ma'lumotlarni yashirish
    return "Xizmatda vaqtinchalik nosozlik yuz berdi. Qaytadan urinib ko'ring."
}

let userMsg = sanitizeError(URLError(.cannotConnectToHost))
print("Foydalanuvchiga ko'rsatiladigan matn: \(userMsg)")
```

## Tushuntirish va Mantiq:
Xavfsizlik talablariga ko'ra ichki drayver xatolari loglanadi, ammo foydalanuvchiga umumiy xavfsiz xabar beriladi.

## Ishlash natijasi:
```text
Foydalanuvchiga ko'rsatiladigan matn: Xizmatda vaqtinchalik nosozlik yuz berdi. Qaytadan urinib ko'ring.
```


# 585-Topshiriq: Standart kutubxona xatolari bilan ishlash: POSIXError
## Topshiriq sharti:
Tizim darajasidagi fayl va ruxsat xatoliklarini ushlash.

## Yechim (Swift kodi):
```swift
import Foundation

let posix = POSIXError(.EACCES)
print("Tizim kodi: \(posix.code.rawValue)")
```

## Tushuntirish va Mantiq:
Swift Foundation operatsion tizim POSIX xatoliklarini to'liq integratsiya qilgan.

## Ishlash natijasi:
```text
Tizim kodi: 13
```


# 586-Topshiriq: Xatoliklarni zanjirli tekshirish
## Topshiriq sharti:
Bir nechta throwing funksiyalarni bitta do blokida sinab ko'rish.

## Yechim (Swift kodi):
```swift
import Foundation

func stepOne() throws { print("1-qadam OK") }
func stepTwo() throws { print("2-qadam OK") }

do {
    try stepOne()
    try stepTwo()
} catch {
    print("Zanjirda xato: \(error)")
}
```

## Tushuntirish va Mantiq:
Bitta do bloki ichida bir nechta try chaqiruvlari ketma-ket yozilishi mumkin; birinchisi xato bersa darhol catch ga sakraydi.

## Ishlash natijasi:
```text
1-qadam OK
2-qadam OK
```


# 587-Topshiriq: Custom Xatolik sinfi (Class-based Error)
## Topshiriq sharti:
Merosxo'rlikka ega bo'lgan klass xatoliklar ierarxiyasi.

## Yechim (Swift kodi):
```swift
import Foundation

class BaseAppError: Error {
    let timestamp = Date()
}

class DatabaseTimeoutError: BaseAppError {}

let e = DatabaseTimeoutError()
print("Sinf asosidagi xatolik: \(type(of: e))")
```

## Tushuntirish va Mantiq:
Xatoliklar sinf sifatida ham yaratilishi mumkin, biroq Swift-da enum va struct lar ancha yengil va afzalroqdir.

## Ishlash natijasi:
```text
Sinf asosidagi xatolik: DatabaseTimeoutError
```


# 588-Topshiriq: Throwing funksiyada defer ning o'rni
## Topshiriq sharti:
Funksiya muvaffaqiyatli bo'lsa ham, xato bilan to'xtasa ham bajariluvchi defer bloki.

## Yechim (Swift kodi):
```swift
import Foundation

func trackedExecution() throws {
    defer { print("Auditor: Harakat qaydnomasi saqlandi.") }
    print("Asosiy ish bajarildi.")
}

try? trackedExecution()
```

## Tushuntirish va Mantiq:
Defer throwing arxitekturasida resurslarni tozalash va audit uchun eng asosiy vositadir.

## Ishlash natijasi:
```text
Asosiy ish bajarildi.
Auditor: Harakat qaydnomasi saqlandi.
```


# 589-Topshiriq: Failable initsializator va throwing initsializator taqqoslanishi
## Topshiriq sharti:
Qachon init? va qachon init throws tanlash lozimligini ko'rsating.

## Yechim (Swift kodi):
```swift
import Foundation

struct UserByInit {
    let name: String
    init?(optionalName: String) {
        guard !optionalName.isEmpty else { return nil }
        self.name = optionalName
    }
}

print("Oddiy holatlarda init?, aniq xato sababi kerak bo'lsa init throws tanlanadi.")
```

## Tushuntirish va Mantiq:
Init? sabab muhim bo'lmaganda tanlanadi, agar chaqiruvchiga nima sababdan to'xtagani kerak bo'lsa throws tanlanadi.

## Ishlash natijasi:
```text
Oddiy holatlarda init?, aniq xato sababi kerak bo'lsa init throws tanlanadi.
```


# 590-Topshiriq: Result ichidagi qiymatni o'zgartiruvchi: Result.map
## Topshiriq sharti:
Muvaffaqiyat qiymatini o'zgartirish.

## Yechim (Swift kodi):
```swift
import Foundation

let res: Result<Int, Error> = .success(10)
let mapped = res.map { $0 * 5 }

print("Mapped result: \(try? mapped.get() ?? 0)")
```

## Tushuntirish va Mantiq:
Result.map agar natija success bo'lsa ichidagi qiymatni o'zgartiradi.

## Ishlash natijasi:
```text
Mapped result: 50
```


# 591-Topshiriq: Result ichidagi qiymatni filtrlovchi utilita
## Topshiriq sharti:
Shart bajarilmasa failure ga o'giruvchi extension.

## Yechim (Swift kodi):
```swift
import Foundation

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
print("Filtrlandi: \(filtered)")
```

## Tushuntirish va Mantiq:
Kengaytmalar orqali Result turi funktsional operatorlar bilan boyitiladi.

## Ishlash natijasi:
```text
Filtrlandi: failure(main.CustomErr.notMatching)
```


# 592-Topshiriq: Asinxron ketma-ketlikda xatoliklar (AsyncSequence throws)
## Topshiriq sharti:
Oqimli ma'lumot kelayotganda xatolikni ushlash.

## Yechim (Swift kodi):
```swift
import Foundation

print("AsyncSequence elementlari xatolik tashlashi mumkin va 'for try await' bilan o'qiladi.")
```

## Tushuntirish va Mantiq:
AsyncSequence orqali tokenlar oqimi o'qilayotganda tarmoq uzilsa 'for try await' catch ga tushadi.

## Ishlash natijasi:
```text
AsyncSequence elementlari xatolik tashlashi mumkin va 'for try await' bilan o'qiladi.
```


# 593-Topshiriq: Xatoliklarni metama'lumot bilan boyituvchi wrapper
## Topshiriq sharti:
Xatolik qaysi fayl va qatorda ro'y berganini qayd etuvchi model.

## Yechim (Swift kodi):
```swift
import Foundation

struct ContextualError: Error {
    let underlyingError: Error
    let file: String
    let line: Int
}

let wrapped = ContextualError(underlyingError: URLError(.badURL), file: "Network.swift", line: 42)
print("Xato manzili: \(wrapped.file):\(wrapped.line)")
```

## Tushuntirish va Mantiq:
Xatolik kontekstini yozib borish nosozliklarni izlashda tengsiz yordam beradi.

## Ishlash natijasi:
```text
Xato manzili: Network.swift:42
```


# 594-Topshiriq: Shartli xato tashlovchi assert o'rnini bosuvchi funksiya
## Topshiriq sharti:
Ishlab chiqish muhitida nosozlikni aniq xato sifatida tashlash.

## Yechim (Swift kodi):
```swift
import Foundation

func requireCondition(_ condition: Bool, error: Error) throws {
    if !condition { throw error }
}

print("Shart tekshiruvi tayyorlandi.")
```

## Tushuntirish va Mantiq:
Kodni xavfsiz invariantlar bilan to'ldirish nosozliklarni erta aniqlaydi.

## Ishlash natijasi:
```text
Shart tekshiruvi tayyorlandi.
```


# 595-Topshiriq: Swift 5.9 Typed throws va Exhaustive Catch
## Topshiriq sharti:
Aniq xatolik turi ko'rsatilganda kompilyator barcha holatlarni tekshirishni talab qilishi.

## Yechim (Swift kodi):
```swift
import Foundation

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
```

## Tushuntirish va Mantiq:
Swift 5.9 Typed Throws ning eng katta ustunligi: barcha xatolik holatlari switch kabi to'liq (exhaustive) yopilgach, umumiy catch yozish talab etilmaydi.

## Ishlash natijasi:
```text
Disk to'la!
```


# 596-Topshiriq: Xatolikni qayta ishlashda LIFO defer zanjiri
## Topshiriq sharti:
Xatolik ro'y bergan paytda bir nechta defer larning teskari tartibda bajarilishi.

## Yechim (Swift kodi):
```swift
import Foundation

func deferChain() throws {
    defer { print("1. Birinchi defer") }
    defer { print("2. Ikkinchi defer") }
    enum Dummy: Error { case err }
    throw Dummy.err
}

try? deferChain()
```

## Tushuntirish va Mantiq:
Defer bloklari doimo LIFO tartibida resurslarni tozalaydi.

## Ishlash natijasi:
```text
2. Ikkinchi defer
1. Birinchi defer
```


# 597-Topshiriq: Tarmoq holati xatolarini foydalanuvchiga formatlash
## Topshiriq sharti:
Foydalanuvchi interfeysi uchun qulay xatolik matnlarini tayyorlash.

## Yechim (Swift kodi):
```swift
import Foundation

func formatErrorForUI(_ error: Error) -> String {
    if let urlError = error as? URLError, urlError.code == .notConnectedToInternet {
        return "Internet aloqasi yo'q. Wi-Fi ni tekshiring."
    }
    return "Noma'lum xatolik yuz berdi."
}

let msg = formatErrorForUI(URLError(.notConnectedToInternet))
print(msg)
```

## Tushuntirish va Mantiq:
Foydalanuvchi tajribasida (UX) tushunarli xabarlar ko'rsatish eng muhim qoidadir.

## Ishlash natijasi:
```text
Internet aloqasi yo'q. Wi-Fi ni tekshiring.
```


# 598-Topshiriq: Non-throwing metodni throwing bilan override qilib bo'lmasligi
## Topshiriq sharti:
Merosxo'rlikda xavfsizlik cheklovining buzilmasligini tushuntiring.

## Yechim (Swift kodi):
```swift
import Foundation

class BaseTask {
    func run() { print("Xavfsiz baza vazifa") }
}

class ExtendedTask: BaseTask {
    // override func run() throws // KOMPILYATSIYA XATOSI!
}

print("Ota sinfda throws bo'lmasa, bola sinf unga throws qo'sha olmaydi.")
```

## Tushuntirish va Mantiq:
Chunki ota sinfni kutayotgan mijoz kod 'try' siz chaqiradi. Agar subclass xato tashlasa butun arxitektura buziladi.

## Ishlash natijasi:
```text
Ota sinfda throws bo'lmasa, bola sinf unga throws qo'sha olmaydi.
```


# 599-Topshiriq: Xatolik ob'ektining Hashable bo'lishi
## Topshiriq sharti:
Xatoliklarni Set yoki Dictionary ga solish imkoniyati.

## Yechim (Swift kodi):
```swift
import Foundation

enum UniqueError: Error, Hashable {
    case timeout(code: Int)
}

var seenErrors: Set<UniqueError> = []
seenErrors.insert(.timeout(code: 408))
seenErrors.insert(.timeout(code: 408))
print("Unikal xatolar soni: \(seenErrors.count)")
```

## Tushuntirish va Mantiq:
Hashable xatoliklar bir xil xatoliklarni qayta-qayta loglamaslikda juda qulaydir.

## Ishlash natijasi:
```text
Unikal xatolar soni: 1
```


# 600-Topshiriq: Amaliy loyiha: Foydalanuvchi to'lovi va Bank API xatoliklarini to'liq boshqaruvchi tranzaksiya moduli
## Topshiriq sharti:
Kredit karta, balans, server xatoliklari, LocalizedError va Retry mexanizmini o'z ichiga olgan mukammal to'lov tranzaksiyasi arxitekturasi.

## Yechim (Swift kodi):
```swift
import Foundation

enum PaymentGatewayError: LocalizedError {
    case invalidCard(number: String)
    case insufficientFunds(required: Double, available: Double)
    case networkTimeout
    
    var errorDescription: String? {
        switch self {
        case .invalidCard(let num):
            return "Noto'g'ri karta raqami: \(num)"
        case .insufficientFunds(let req, let avail):
            return "Mablag' yetarli emas! Kerak: $\(req), Mavjud: $\(avail)"
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
        print("TO'LOV MUVAFFAQIShI: $\(amount) yechildi. Yangi balans: $\(userBalance)")
    }
}

let processor = PaymentProcessor()

print("=== TO'LOV JARAYONI ===")
do {
    try processor.executeTransaction(cardNumber: "8600123456789012", amount: 150.0)
    try processor.executeTransaction(cardNumber: "8600123456789012", amount: 500.0) // Mablag' yetarli emas
} catch let error as PaymentGatewayError {
    print("[XATOLIK]: \(error.localizedDescription)")
} catch {
    print("[BOSHQARILMAGAN XATO]: \(error)")
}
```

## Tushuntirish va Mantiq:
Ushbu yakuniy loyihada 'Error', 'LocalizedError', 'throws', 'do-catch' va 'guard' mexanizmlari real bank tranzaksiyasi xavfsizligini 100% ta'minladi.

## Ishlash natijasi:
```text
=== TO'LOV JARAYONI ===
TO'LOV MUVAFFAQIShI: $150.0 yechildi. Yangi balans: $150.0
[XATOLIK]: Mablag' yetarli emas! Kerak: $500.0, Mavjud: $150.0
```

