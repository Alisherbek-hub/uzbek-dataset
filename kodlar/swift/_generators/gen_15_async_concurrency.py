# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks_data = [
    (
        701,
        "Swift Modern Concurrency inqilobi va async/await",
        "Eski callback hell (ichma-ich completion handlerlar) o'rniga toza asinxron funksiya yozing.",
        """import Foundation

func fetchUserData() async -> String {
    return "Foydalanuvchi ma'lumotlari yuklandi"
}

Task {
    let data = await fetchUserData()
    print("Natija: \\(data)")
}
""",
        "Swift 5.5 da joriy qilingan zamonaviy Concurrency tizimi 'async/await' orqali asinxron kodni xuddi oddiy ketma-ket (sinxron) kod kabi oson va xatosiz o'qiladigan formatga keltirdi.",
        """Natija: Foydalanuvchi ma'lumotlari yuklandi"""
    ),
    (
        702,
        "To'xtatish nuqtasi (Suspension Point) tushunchasi",
        "await chaqirilgan joyda oqim (thread) boshqa vazifalar uchun bo'shatilishini ko'rsating.",
        """import Foundation

func performBackgroundCalculation() async -> Int {
    try? await Task.sleep(nanoseconds: 10_000_000) // 10ms to'xtatish nuqtasi
    return 42 * 2
}

Task {
    print("Hisoblash boshlandi...")
    let result = await performBackgroundCalculation() // Suspension point
    print("Natija olindi: \\(result)")
}
""",
        "'await' kalit so'zi potentsial to'xtatish nuqtasini (Suspension Point) bildiradi. Bu paytda joriy oqim to'sib (block) qo'yilmaydi, balki tizim unda boshqa vazifalarni bajarishda davom etadi.",
        """Hisoblash boshlandi...
Natija olindi: 84"""
    ),
    (
        703,
        "Ketma-ket asinxron chaqiruvlar (Sequential async)",
        "Biri ikkinchisiga bog'liq bo'lgan ikkita asinxron so'rovni ketma-ket bajaring.",
        """import Foundation

func fetchUserID() async -> Int { return 1004 }
func fetchUserName(for id: Int) async -> String { return "Murod (ID: \\(id))" }

Task {
    let id = await fetchUserID()
    let name = await fetchUserName(for: id)
    print("Mijoz: \\(name)")
}
""",
        "Ketma-ket 'await' chaqiruvlari avval birinchi operatsiya to'liq yakunlanishini kutadi, so'ngra uning natijasi bilan keyingisiga o'tadi.",
        """Mijoz: Murod (ID: 1004)"""
    ),
    (
        704,
        "Parallel asinxron bajarilish: async let",
        "Bir-biriga bog'liq bo'lmagan ikkita asinxron operatsiyani bir vaqtda parallel ishga tushiring.",
        """import Foundation

func loadNews() async -> String { "Yangiliklar ro'yxati" }
func loadWeather() async -> String { "Quyoshli, 25°C" }

Task {
    async let news = loadNews()
    async let weather = loadWeather()
    
    // Ikkalasi parallel bajariladi va ikkalasi kutib olinadi:
    let (n, w) = await (news, weather)
    print("Bosh sahifa: [\\(n)] va [\\(w)]")
}
""",
        "'async let' ota task ichida bola vazifa ochib, uni darhol fonda parallel ishga tushiradi. Keyinchalik natija kerak bo'lganda 'await' bilan kutib olinadi.",
        """Bosh sahifa: [Yangiliklar ro'yxati] va [Quyoshli, 25°C]"""
    ),
    (
        705,
        "Strukturalangan konkurentlik: Task ierarxiyasi",
        "Ota Task bekor bo'lganda yoki xato berganda barcha bola tasklar avtomatik tozalanishini tushuntiring.",
        """import Foundation

func fetchDashboard() async -> String {
    async let stats = "Statistika"
    async let chart = "Grafik"
    return await "\\(stats) + \\(chart)"
}

Task {
    let dash = await fetchDashboard()
    print("Dashboard tayyor: \\(dash)")
}
""",
        "Structured Concurrency (Strukturalangan Konkurentlik) qoidasiga ko'ra, har bir asinxron harakat aniq ko'rinish sohasiga (scope) bog'langan bo'lib, ota vazifasiz mustaqil osilib qolmaydi (no leaks).",
        """Dashboard tayyor: Statistika + Grafik"""
    ),
    (
        706,
        "Asosiy Task yaratish: Task { ... }",
        "Sinxron kod ichidan yangi asinxron kontekst ochuvchi Task blokini e'lon qiling.",
        """import Foundation

func startApp() {
    print("1. Sinxron boshlanish.")
    Task {
        print("2. Asinxron vazifa bajarilmoqda.")
    }
    print("3. Sinxron davom etmoqda.")
}

startApp()
""",
        "'Task { ... }' joriy kontekst parametrlarini (actor, priority) meros qilib oluvchi yangi asinxron vazifani ishga tushiradi.",
        """1. Sinxron boshlanish.
3. Sinxron davom etmoqda.
2. Asinxron vazifa bajarilmoqda."""
    ),
    (
        707,
        "Alohida vazifa: Task.detached { ... }",
        "Ota kontekst parametrlarini (Actor, Priority) meros qilib olmaydigan mustaqil vazifani ishga tushiring.",
        """import Foundation

Task.detached(priority: .background) {
    print("Mustaqil fon vazifasi fonda ishga tushdi.")
}
""",
        "'Task.detached' joriy muhitga mutlaqo bog'liq bo'lmagan, to'liq ajratilgan yangi mustaqil vazifa yaratadi.",
        """Mustaqil fon vazifasi fonda ishga tushdi."""
    ),
    (
        708,
        "Task ustuvorliklari (TaskPriority)",
        "Yuqori va past ustuvorlikdagi vazifalarni e'lon qiling.",
        """import Foundation

Task(priority: .userInitiated) {
    print("Foydalanuvchi kutayotgan yuqori ustuvorlikli vazifa.")
}

Task(priority: .background) {
    print("Past ustuvorlikli fon vazifasi.")
}
""",
        "Swift Task lari operatsion tizim rejalashtiruvchisi (scheduler) uchun .high, .userInitiated, .medium, .utility, .background kabi ustuvorlik darajalarini qabul qiladi.",
        """Foydalanuvchi kutayotgan yuqori ustuvorlikli vazifa.
Past ustuvorlikli fon vazifasi."""
    ),
    (
        709,
        "Task.sleep va zamonaviy Duration API (Swift 5.7+)",
        "Vazifani soniyalar bo'yicha to'xtatib turish.",
        """import Foundation

Task {
    print("Taymer boshlandi.")
    try? await Task.sleep(for: .milliseconds(50))
    print("50ms o'tdi.")
}
""",
        "Swift 5.7 dan boshlab 'Task.sleep(for: .seconds(2))' ko'rinishidagi zamonaviy Duration API qo'shildi, bu nanosekundlar o'rniga tushunarli birliklardan foydalanish imkonini beradi.",
        """Taymer boshlandi.
50ms o'tdi."""
    ),
    (
        710,
        "Dinamik parallel vazifalar guruhi: withTaskGroup",
        "Noma'lum sondagi so'rovlarni TaskGroup orqali bir vaqtda parallel bajaring.",
        """import Foundation

func fetchMultipleItems(ids: [Int]) async -> [String] {
    await withTaskGroup(of: String.self) { group in
        for id in ids {
            group.addTask {
                return "Element #\\(id)"
            }
        }
        var results = [String]()
        for await item in group {
            results.append(item)
        }
        return results
    }
}

Task {
    let all = await fetchMultipleItems(ids: [1, 2, 3])
    print("Yuklanganlar soni: \\(all.count)")
}
""",
        "'withTaskGroup' dinamik miqdordagi parallel vazifalarni boshqarish uchun strukturalangan guruh hosil qiladi va ularning natijalarini 'for await' tsiklida to'playdi.",
        """Yuklanganlar soni: 3"""
    ),
    (
        711,
        "Xatolik tashlovchi vazifalar guruhi: withThrowingTaskGroup",
        "Guruqdagi vazifalardan biri xato tashlaganda butun guruh xavfsiz to'xtashini ko'rsating.",
        """import Foundation

enum GroupError: Error { case failure }

func runThrowingGroup() async throws -> [Int] {
    try await withThrowingTaskGroup(of: Int.self) { group in
        group.addTask { return 10 }
        group.addTask { return 20 }
        
        var results = [Int]()
        for try await val in group {
            results.append(val)
        }
        return results
    }
}

Task {
    let res = try? await runThrowingGroup()
    print("Guruh natijalari yig'indisi: \\((res ?? []).reduce(0, +))")
}
""",
        "'withThrowingTaskGroup' agar biror vazifada xatolik yuz bersa, uni darhol 'throw' qiladi va guruhdagi qolgan parallel vazifalarni avtomatik bekor qiladi.",
        """Guruh natijalari yig'indisi: 30"""
    ),
    (
        712,
        "Task Cancellation: Kooperativ bekor qilish",
        "Task bekor qilinganini 'Task.isCancelled' orqali tekshirib erta to'xtating.",
        """import Foundation

let task = Task {
    for i in 1...1000 {
        if Task.isCancelled {
            print("Vazifa bekor qilindi, tsikldan chiqildi (qadam: \\(i)).")
            return
        }
    }
}

task.cancel()
""",
        "Swift-da Task bekor qilinishi 'kooperativ' (hamkorlikka asoslangan) bo'lib, vazifa tashqaridan zo'rlik bilan o'ldirilmaydi, balki o'z ichida muntazam tekshirib xavfsiz chiqishi lozim.",
        """Vazifa bekor qilindi, tsikldan chiqildi (qadam: 1)."""
    ),
    (
        713,
        "Majburiy bekor tekshiruvi: try Task.checkCancellation()",
        "Bekor qilingan taqdirda darhol CancellationError tashlovchi tekshiruv.",
        """import Foundation

func heavyProcess() async throws {
    try Task.checkCancellation()
    print("Og'ir jarayon muvaffaqiyatli bajarildi.")
}

Task {
    do {
        try await heavyProcess()
    } catch {
        print("Xato ushlandi: \\(error)")
    }
}
""",
        "'Task.checkCancellation()' agar joriy task bekor qilingan bo'lsa, 'CancellationError' tashlaydi va kodning keyingi satrlariga o'tishni to'xtatadi.",
        """Og'ir jarayon muvaffaqiyatli bajarildi."""
    ),
    (
        714,
        "withTaskCancellationHandler bilan resurslarni to'xtatish",
        "Task bekor qilingan zahoti tashqi soket yoki faylni to'xtatuvchi handler.",
        """import Foundation

func performCancellableTask() async {
    await withTaskCancellationHandler {
        print("Asosiy ish bajarilmoqda...")
    } onCancel: {
        print("ON_CANCEL: Bekor qilish signali ushlandi!")
    }
}

Task {
    await performCancellableTask()
}
""",
        "'withTaskCancellationHandler' asosiy asinxron blok va u bekor qilingan paytda darhol boshqa oqimda chaqiriluvchi 'onCancel' blokini birlashtiradi.",
        """Asosiy ish bajarilmoqda..."""
    ),
    (
        715,
        "Asinxron ketma-ketliklar: AsyncSequence va 'for await'",
        "Kelajakda bosqichma-bosqich yetib keladigan ma'lumotlarni asinxron tsiklda o'qing.",
        """import Foundation

struct CounterSequence: AsyncSequence {
    typealias Element = Int
    
    struct AsyncIterator: AsyncIteratorProtocol {
        var count = 1
        mutating func next() async -> Int? {
            guard count <= 3 else { return nil }
            let val = count
            count += 1
            return val
        }
    }
    
    func makeAsyncIterator() -> AsyncIterator { AsyncIterator() }
}

Task {
    for await number in CounterSequence() {
        print("Olingan son: \\(number)")
    }
}
""",
        "'AsyncSequence' xuddi oddiy Sequence kabi ishlaydi, faqat uning 'next()' metodi 'async' hisoblanadi va 'for await' tsikli bilan iste'mol qilinadi.",
        """Olingan son: 1
Olingan son: 2
Olingan son: 3"""
    ),
    (
        716,
        "Asinxron Oqim: AsyncStream<Element>",
        "Tugmalar bosilishi yoki sensor signallarini xavfsiz AsyncStream ga aylantiring.",
        """import Foundation

func makeNumbersStream() -> AsyncStream<Int> {
    AsyncStream { continuation in
        continuation.yield(10)
        continuation.yield(20)
        continuation.yield(30)
        continuation.finish()
    }
}

Task {
    for await value in makeNumbersStream() {
        print("Stream qiymati: \\(value)")
    }
}
""",
        "'AsyncStream' kloujerlar va eski callback tizimlarini zamonaviy 'AsyncSequence' oqimiga aylantirishning eng qulay va kuchli vositasidir.",
        """Stream qiymati: 10
Stream qiymati: 20
Stream qiymati: 30"""
    ),
    (
        717,
        "AsyncStream da to'xtatish: onTermination",
        "Oqim iste'molchisi tsikldan chiqqanda resursni tozalash.",
        """import Foundation

let stream = AsyncStream<String> { continuation in
    continuation.onTermination = { termination in
        print("Stream yakunlandi: \\(termination)")
    }
    continuation.yield("Xabar 1")
    continuation.finish()
}

Task {
    for await msg in stream {
        print("Xabar: \\(msg)")
    }
}
""",
        "'continuation.onTermination' oqim tugatilganda (finish) yoki iste'molchi bekor qilganda chaqiriladi.",
        """Xabar: Xabar 1
Stream yakunlandi: finished"""
    ),
    (
        718,
        "Eski callback kodni asinxron qilish: withCheckedContinuation",
        "Klassik completion handlerli funksiyani zamonaviy async funksiyaga o'rang.",
        """import Foundation

func legacyFetch(completion: @escaping (String) -> Void) {
    DispatchQueue.global().async {
        completion("Eski tizim ma'lumotlari")
    }
}

func modernFetch() async -> String {
    await withCheckedContinuation { continuation in
        legacyFetch { result in
            continuation.resume(returning: result)
        }
    }
}

Task {
    let data = await modernFetch()
    print("Modernlashtirilgan javob: \\(data)")
}
""",
        "'withCheckedContinuation' chaqiruvchi oqimni to'xtatib turadi va 'continuation.resume' chaqirilganda natijani qaytarib oqimni uyg'otadi. U aynan bir marta chaqirilishini tekshiradi.",
        """Modernlashtirilgan javob: Eski tizim ma'lumotlari"""
    ),
    (
        719,
        "withCheckedThrowingContinuation bilan xatolikli eski kodni o'rash",
        "Muvaffaqiyat yoki xatolik bilan tugaydigan eski kodni async throws ga aylantirish.",
        """import Foundation

func legacyAPI(completion: @escaping (String?, Error?) -> Void) {
    completion("Muvaffaqiyatli API javobi", nil)
}

func modernAPI() async throws -> String {
    try await withCheckedThrowingContinuation { continuation in
        legacyAPI { text, error in
            if let err = error {
                continuation.resume(throwing: err)
            } else if let t = text {
                continuation.resume(returning: t)
            }
        }
    }
}

Task {
    let result = try? await modernAPI()
    print("Natija: \\(result ?? "")")
}
""",
        "'withCheckedThrowingContinuation' xatoliklarni 'resume(throwing:)' orqali oddiy 'throws' tizimiga xavfsiz ulaydi.",
        """Natija: Muvaffaqiyatli API javobi"""
    ),
    (
        720,
        "Continuation aynan bir marta chaqirilishi qoidasi (Exact-once resumption)",
        "Continuation ni ikki marta resume qilish halokatli crash berishini tushuntiring.",
        """import Foundation

func safeContinuationCall() async -> Int {
    await withCheckedContinuation { continuation in
        continuation.resume(returning: 100)
        // continuation.resume(returning: 200) // CRASH: SWIFT CHECKED CONTINUATION VIOLATION!
    }
}

Task {
    let val = await safeContinuationCall()
    print("Xavfsiz qiymat: \\(val)")
}
""",
        "CheckedContinuation har bir tarmoqda AYNAN BIR MARTA chaqirilishi shart. Agar u chaqirilmay unutilsa — oqim abadiy qotib qoladi (hang); agar ikki marta chaqirilsa — dastur crash bo'ladi.",
        """Xavfsiz qiymat: 100"""
    ),
    (
        721,
        "Task Mahalliy Qiymatlari: @TaskLocal",
        "Butun asinxron zanjir bo'ylab parametr uzatmasdan yagona identifikatorni olib yurish.",
        """import Foundation

enum LoggingContext {
    @TaskLocal static var traceID: String?
}

func performSubTask() async {
    print("SubTask traceID: \\(LoggingContext.traceID ?? "Mavjud emas")")
}

Task {
    await LoggingContext.$traceID.withValue("TRACE_9981") {
        print("Boshlang'ich traceID: \\(LoggingContext.traceID ?? "")")
        await performSubTask()
    }
}
""",
        "'@TaskLocal' joriy Task va uning barcha bola vazifalarida ko'rinadigan maxsus xotira hududini taqdim etadi (Request ID, Trace ID larni saqlashda juda qulay).",
        """Boshlang'ich traceID: TRACE_9981
SubTask traceID: TRACE_9981"""
    ),
    (
        722,
        "Asinxron Timeout pattern: Task poygasi",
        "Agar vazifa berilgan vaqt ichida yakunlanmasa timeout xatosi tashlovchi yordamchi.",
        """import Foundation

enum TimeoutError: Error { case timedOut }

func withTimeout<T>(seconds: Double, operation: @escaping () async throws -> T) async throws -> T {
    try await withThrowingTaskGroup(of: T.self) { group in
        group.addTask {
            return try await operation()
        }
        group.addTask {
            try await Task.sleep(nanoseconds: UInt64(seconds * 1_000_000_000))
            throw TimeoutError.timedOut
        }
        
        let result = try await group.next()!
        group.cancelAll()
        return result
    }
}

Task {
    do {
        let res = try await withTimeout(seconds: 1.0) { () -> String in
            return "Tezkor natija"
        }
        print("Vaqtida olindi: \\(res)")
    } catch {
        print("Xato: \\(error)")
    }
}
""",
        "TaskGroup ichida vazifa va taymer poygasini tashkil etib, birinchisi yakunlangach ikkinchisini bekor qilish orqali toza 'timeout' hosil qilinadi.",
        """Vaqtida olindi: Tezkor natija"""
    ),
    (
        723,
        "Thread Explosion muammosining yo'q qilinishi",
        "Eski GCD da yuzlab oqimlar ochilib xotira tugashining Swift Concurrency da qanday hal bo'lganini tushuntiring.",
        """import Foundation

print("Swift Concurrency protsessor yadrolari soniga teng bitta umumiy kooperativ oqimlar hovuzidan (Cooperative Thread Pool) foydalanadi.")
""",
        "Grand Central Dispatch (GCD) da har bir bloklangan vazifa uchun yangi OS thread ochilib tizim qotib qolardi (Thread Explosion). Swift Concurrency esa qat'iy ravishda CPU yadrolari sonidan ortiq oqim yaratmaydi.",
        """Swift Concurrency protsessor yadrolari soniga teng bitta umumiy kooperativ oqimlar hovuzidan (Cooperative Thread Pool) foydalanadi."""
    ),
    (
        724,
        "Boshqa vazifalarga navbat berish: Task.yield()",
        "Uzoq davom etuvchi hisob-kitob tsiklida protsessorni boshqa vazifalarga bo'shatib berish.",
        """import Foundation

func computeHeavyLoop() async {
    for i in 1...3 {
        print("Qadam \\(i) bajarildi.")
        await Task.yield() // Protsessorni boshqalarga vaqtincha beradi
    }
}

Task {
    await computeHeavyLoop()
}
""",
        "'Task.yield()' joriy vazifaning to'xtatish nuqtasi bo'lib, xuddi shu oqimdagi boshqa navbatda turgan vazifalarga zudlik bilan navbat beradi.",
        """Qadam 1 bajarildi.
Qadam 2 bajarildi.
Qadam 3 bajarildi."""
    ),
    (
        725,
        "TaskGroup ichida birinchi muvaffaqiyatli natijani olib qolganlarini bekor qilish (Race pattern)",
        "Bir nechta server keshlaridan eng birinchi kelgan javobni qabul qiling.",
        """import Foundation

func fetchFastestMirror() async -> String {
    await withTaskGroup(of: String.self) { group in
        group.addTask { "Server A (Tez)" }
        group.addTask { "Server B (Sekin)" }
        
        let firstResult = await group.next() ?? "Xato"
        group.cancelAll()
        return firstResult
    }
}

Task {
    let fastest = await fetchFastestMirror()
    print("Eng birinchi kelgan: \\(fastest)")
}
""",
        "Eng birinchi natija olingach 'group.cancelAll()' chaqirilsa, boshqa fondagi operatsiyalar resurs sarflamasdan darhol to'xtatiladi.",
        """Eng birinchi kelgan: Server A (Tez)"""
    ),
    (
        726,
        "Asinxron URLSession chaqiruvlari",
        "Tarmoqdan ma'lumot yuklashning zamonaviy asinxron usuli.",
        """import Foundation

func fetchAPIStatus() async -> Int {
    return 200 // Mock URLSession javobi
}

Task {
    let status = await fetchAPIStatus()
    print("HTTP Status: \\(status)")
}
""",
        "Foundation-dagi 'URLSession.shared.data(from:)' asinxron metod bo'lib, zamonaviy Concurrency tizimi bilan mukammal ishlaydi.",
        """HTTP Status: 200"""
    ),
    (
        727,
        "SwiftUI-dagi .task modifikatori falsafasi",
        "Ekranga chiqqanda boshlanib, ekrandan ketganda avtomatik bekor bo'luvchi vazifa.",
        """import Foundation

print("SwiftUI-dagi '.task' ko'rinish hayot tsikliga (lifecycle) qat'iy bog'langan va avtomatik bekor qilinadi.")
""",
        "SwiftUI dagi .task modifikatori view ekrandan yo'qolganda fondagi yuklanishlarni avtomatik 'cancel()' qiladi, bu xotira sizishini oldini oladi.",
        """SwiftUI-dagi '.task' ko'rinish hayot tsikliga (lifecycle) qat'iy bog'langan va avtomatik bekor qilinadi."""
    ),
    (
        728,
        "Asinxron xotira modeli: Stack Frames vs Heap Task Context",
        "To'xtatilgan asinxron funksiya stakda emas, balki Heap-dagi Task xotirasida saqlanishini tushuntiring.",
        """import Foundation

print("Asinxron funksiyalar to'xtatilganda (suspend) ularning freymi stakdan xotira uyumiga (Heap) ko'chiriladi.")
""",
        "Oddiy sinxron funksiya stakda yashaydi. Asinxron funksiya esa 'await' nuqtasida oqimni bo'shatishi kerakligi sababli, uning freymi Heap-dagi maxsus Continuation blokiga o'tkaziladi.",
        """Asinxron funksiyalar to'xtatilganda (suspend) ularning freymi stakdan xotira uyumiga (Heap) ko'chiriladi."""
    ),
    (
        729,
        "TaskGroup da cheklangan paralellik (Concurrency Limiting)",
        "Bir vaqtning o'zida maksimal 2 ta parallel vazifa bajarilishini ta'minlovchi oqim.",
        """import Foundation

func runThrottledTasks(items: [Int]) async {
    await withTaskGroup(of: Void.self) { group in
        var index = 0
        let maxConcurrent = 2
        
        while index < items.count && index < maxConcurrent {
            let item = items[index]
            group.addTask { print("Ishlandi: \\(item)") }
            index += 1
        }
        
        for await _ in group {
            if index < items.count {
                let item = items[index]
                group.addTask { print("Ishlandi: \\(item)") }
                index += 1
            }
        }
    }
}

Task {
    await runThrottledTasks(items: [1, 2, 3, 4])
}
""",
        "Ushbu naqsh serverni haddan tashqari parallel so'rovlar bilan yuklab qo'ymaslik (throttling) uchun ishlatiladi.",
        """Ishlandi: 1
Ishlandi: 2
Ishlandi: 3
Ishlandi: 4"""
    ),
    (
        730,
        "AsyncSequence ustida transformatsiyalar: map va filter",
        "Asinxron oqim elementlarini funktsional zanjirda saralash.",
        """import Foundation

Task {
    let stream = AsyncStream<Int> { continuation in
        for i in 1...4 { continuation.yield(i) }
        continuation.finish()
    }
    
    for await doubled in stream.map({ $0 * 2 }) {
        print("Ikkilangan stream: \\(doubled)")
    }
}
""",
        "AsyncSequence Swift-ning barcha standart yuqori tartibli funktsional metodlarini (map, filter, reduce) asinxron tarzda qo'llab-quvvatlaydi.",
        """Ikkilangan stream: 2
Ikkilangan stream: 4
Ikkilangan stream: 6
Ikkilangan stream: 8"""
    ),
    (
        731,
        "Asinxron rekursiya",
        "Daraxtsimon tugunlarni asinxron rekursiv aylanib chiqish.",
        """import Foundation

func asyncSumTree(depth: Int) async -> Int {
    guard depth > 0 else { return 0 }
    async let left = asyncSumTree(depth: depth - 1)
    async let right = asyncSumTree(depth: depth - 1)
    return await (left + right) + depth
}

Task {
    let total = await asyncSumTree(depth: 2)
    print("Daraxt summasi: \\(total)")
}
""",
        "Asinxron funksiyalar rekursiyada ham to'liq xavfsiz va parallel ishlay oladi.",
        """Daraxt summasi: 4"""
    ),
    (
        732,
        "withUnsafeContinuation va unumdorlik",
        "Tekshiruvlarsiz eng maksimal tezkor continuation chaqiruvi.",
        """import Foundation

func fastAsyncNumber() async -> Int {
    await withUnsafeContinuation { continuation in
        continuation.resume(returning: 777)
    }
}

Task {
    let n = await fastAsyncNumber()
    print("Unsafe continuation natijasi: \\(n)")
}
""",
        "'withUnsafeContinuation' 'Checked' versiyadagi tekshiruv xarajatlarini chetlab o'tib, maksimal apparat unumdorligini beradi (faqat kod 100% ishonchli bo'lganda ishlatiladi).",
        """Unsafe continuation natijasi: 777"""
    ),
    (
        733,
        "AsyncThrowingStream bilan xatolikli oqim",
        "Oqim davomida xatolik yuz berganda uni uzatish.",
        """import Foundation

enum StreamFault: Error { case brokenConnection }

let faultyStream = AsyncThrowingStream<String, Error> { continuation in
    continuation.yield("Ma'lumot 1")
    continuation.finish(throwing: StreamFault.brokenConnection)
}

Task {
    do {
        for try await item in faultyStream {
            print("Olingan: \\(item)")
        }
    } catch {
        print("Oqimda xatolik: \\(error)")
    }
}
""",
        "'AsyncThrowingStream' xatolik tashlashi mumkin bo'lgan real vaqtli oqimlarni boshqaradi.",
        """Olingan: Ma'lumot 1
Oqimda xatolik: brokenConnection"""
    ),
    (
        734,
        "Asinxron keshlovchi mexanizm",
        "Asinxron yuklangan natijani qayta yuklamasdan keshdan berish.",
        """import Foundation

class AsyncCache {
    private var cachedValue: String?
    
    func getData() async -> String {
        if let val = cachedValue { return val }
        let fetched = "Keshlandi"
        cachedValue = fetched
        return fetched
    }
}

Task {
    let c = AsyncCache()
    print(await c.getData())
}
""",
        "Asinxron operatsiyalar natijalarini xotirada saqlash ilova tezligini oshiradi.",
        """Keshlandi"""
    ),
    (
        735,
        "Swift Concurrency da defer ning LIFO tabiati",
        "Asinxron funksiyada defer qanday ishlashini amalda tekshirish.",
        """import Foundation

func asyncWithDefer() async {
    defer { print("Async Defer 1 (oxirgi)") }
    defer { print("Async Defer 2 (birinchi)") }
    print("Asinxron ish bajarildi.")
}

Task {
    await asyncWithDefer()
}
""",
        "Asinxron funksiyalarda ham 'defer' qat'iy ravishda LIFO tartibida eng oxirida ishlaydi.",
        """Asinxron ish bajarildi.
Async Defer 2 (birinchi)
Async Defer 1 (oxirgi)"""
    ),
    (
        736,
        "Asinxron boshqaruvda Task.sleep ning bekor bo'lishi",
        "Kutish paytida Task bekor qilinsa darhol CancellationError otilishini ko'rsatish.",
        """import Foundation

let sleepingTask = Task {
    do {
        try await Task.sleep(nanoseconds: 1_000_000_000)
    } catch is CancellationError {
        print("Uyqu bekor qilindi!")
    } catch {}
}

sleepingTask.cancel()
""",
        "'Task.sleep' kutish vaqtida bekor qilish signali kelsa, uyquni davom ettirmay darhol CancellationError tashlaydi.",
        """Uyqu bekor qilindi!"""
    ),
    (
        737,
        "AsyncSequence dan birinchi elementni olish",
        "Asinxron oqimning eng birinchi qiymatini xavfsiz kutib olish.",
        """import Foundation

let simpleStream = AsyncStream<Int> { continuation in
    continuation.yield(99)
    continuation.finish()
}

Task {
    for await first in simpleStream {
        print("Birinchi element: \\(first)")
        break
    }
}
""",
        "Asinxron tsiklda 'break' qilish oqimni avtomatik to'xtatadi.",
        """Birinchi element: 99"""
    ),
    (
        738,
        "Task ustuvorligini meros olish (Priority Escalation)",
        "Yuqori ustuvorlikdagi task past ustuvorlikdagi natijani kutganda nima bo'lishi.",
        """import Foundation

print("Swift Concurrency tizimi 'Priority Inversion' muammosining oldini olish uchun past task ustuvorligini avtomatik oshiradi (Priority Escalation).")
""",
        "Agar yuqori ustuvorlikdagi Task (.userInitiated) pastroq vazifaning (.background) natijasini kutayotgan bo'lsa, tizim kutish vaqtini kamaytirish uchun past vazifaning ham darajasini vaqtincha ko'taradi.",
        """Swift Concurrency tizimi 'Priority Inversion' muammosining oldini olish uchun past task ustuvorligini avtomatik oshiradi (Priority Escalation)."""
    ),
    (
        739,
        "Bir nechta async let natijalarini xatolik bilan kutish",
        "Ikkita parallel chaqiruvdan biri xato bersa darhol catch ga o'tish.",
        """import Foundation

func faultyLoad() async throws -> String {
    enum LoadErr: Error { case bad }
    throw LoadErr.bad
}

func okLoad() async -> String { "OK" }

Task {
    do {
        async let a = faultyLoad()
        async let b = okLoad()
        let _ = try await (a, b)
    } catch {
        print("Parallel xato ushlandi: \\(error)")
    }
}
""",
        "'async let' zanjirida 'try await (a, b)' chaqirilganda birinchi uchragan xatolik ushlanadi va ikkinchi vazifa bekor qilinadi.",
        """Parallel xato ushlandi: bad"""
    ),
    (
        740,
        "Asinxron funksiyadan bir nechta qiymat qaytarish: Tuple",
        "Asinxron chaqiruv natijalarini kortej shaklida olish.",
        """import Foundation

func fetchCoordinates() async -> (lat: Double, lng: Double) {
    return (41.2995, 69.2401)
}

Task {
    let loc = await fetchCoordinates()
    print("Kenglik: \\(loc.lat), Uzunlik: \\(loc.lng)")
}
""",
        "Asinxron funksiyalar ham oddiy funksiyalar kabi barcha Swift turlarini qaytara oladi.",
        """Kenglik: 41.2995, Uzunlik: 69.2401"""
    ),
    (
        741,
        "AsyncStream orqali hodisalar buferlash strategiyasi",
        "Oqim qabul qila olmay qolganida eng yangilarini saqlab eskilarini tashlash (Buffering Policy).",
        """import Foundation

let bufferedStream = AsyncStream<Int>(bufferingPolicy: .bufferingNewest(2)) { continuation in
    continuation.yield(1)
    continuation.yield(2)
    continuation.yield(3) // 1 o'chib ketadi
    continuation.finish()
}

Task {
    for await n in bufferedStream {
        print("Buferdan: \\(n)")
    }
}
""",
        "'AsyncStream.Continuation.BufferingPolicy' xotirani tejash uchun .unbounded, .bufferingNewest(N) yoki .bufferingOldest(N) strategiyalarini beradi.",
        """Buferdan: 2
Buferdan: 3"""
    ),
    (
        742,
        "Task ning sinxron kod bilan aloqasi: Task.init",
        "Sinxron metod ichidan asinxron natijani UI ga uzatish arxitekturasi.",
        """import Foundation

func buttonTapped() {
    Task {
        let msg = "Asinxron hisoblangan xabar"
        print("UI ga yetkazildi: \\(msg)")
    }
}

buttonTapped()
""",
        "Tugma bosilishi (UI hodisalari) sinxron funksiya bo'ladi, ulardan asinxron dunyoga o'tish ko'prigi 'Task { ... }' hisoblanadi.",
        """UI ga yetkazildi: Asinxron hisoblangan xabar"""
    ),
    (
        743,
        "Asinxron takrorlanuvchi Taymer yaratish",
        "AsyncStream yordamida har N soniyada chiquvchi hodisalar manbai.",
        """import Foundation

func timerStream(ticks: Int) -> AsyncStream<Int> {
    AsyncStream { continuation in
        Task {
            for i in 1...ticks {
                continuation.yield(i)
            }
            continuation.finish()
        }
    }
}

Task {
    for await tick in timerStream(ticks: 2) {
        print("Signal: #\\(tick)")
    }
}
""",
        "AsyncStream orqali zamonaviy reaktiv hodisalar oqimini yaratish juda qulaydir.",
        """Signal: #1
Signal: #2"""
    ),
    (
        744,
        "Asinxron funksiyada 'nonisolated' kontekst",
        "Actorga bog'lanmagan erkin asinxron funksiya.",
        """import Foundation

nonisolated func freeAsyncMethod() async -> String {
    return "Har qanday actor dan tashqaridagi erkin chaqiruv"
}

Task {
    print(await freeAsyncMethod())
}
""",
        "'nonisolated' kalit so'zi asinxron funksiyaning hech qanday maxsus oqim yoki actor ga bog'lanmasdan erkin ijro etilishini bildiradi.",
        """Har qanday actor dan tashqaridagi erkin chaqiruv"""
    ),
    (
        745,
        "Strukturalangan konkurentlikda o'zgaruvchilar mutatsiyasining oldi olinishi",
        "Parallel bloklar ichida bitta tashqi o'zgaruvchini o'zgartirish nima uchun taqiqlanganligini ko'rsating.",
        """import Foundation

print("Swift Concurrency parallel vazifalar ichida tashqi 'var' o'zgaruvchilarni mutatsiyaga uchratishni taqiqlaydi (Data Race xavfi).")
""",
        "Parallel kodda ma'lumotlar faqat 'return' orqali qaytariladi yoki xavfsiz Actor lar orqali himoyalanadi.",
        """Swift Concurrency parallel vazifalar ichida tashqi 'var' o'zgaruvchilarni mutatsiyaga uchratishni taqiqlaydi (Data Race xavfi)."""
    ),
    (
        746,
        "Task ichida bekor qilish holatini saqlab qolish",
        "Vazifa bekor bo'lsa ham oxirgi tozalash ishlarini bajarish.",
        """import Foundation

let cleanerTask = Task {
    if Task.isCancelled {
        print("Vazifa bekor holatida tozalash ishlarini yakunladi.")
    }
}
cleanerTask.cancel()
""",
        "Kooperativlik prinsipi vazifaga bekor bo'lganda ham xavfsiz tozalash imkoniyatini qoldiradi.",
        """Vazifa bekor holatida tozalash ishlarini yakunladi."""
    ),
    (
        747,
        "AsyncSequence dan massiv hosil qiluvchi umumiy extension",
        "Asinxron ketma-ketlikni to'liq massivga yig'uvchi qulay yordamchi.",
        """import Foundation

extension AsyncSequence {
    func collectAll() async rethrows -> [Element] {
        var results = [Element]()
        for try await item in self {
            results.append(item)
        }
        return results
    }
}

Task {
    let stream = AsyncStream<String> { c in
        c.yield("A"); c.yield("B"); c.finish()
    }
    let all = await stream.collectAll()
    print("Yig'ilgan massiv: \\(all)")
}
""",
        "Asinxron oqimlarni oddiy massivlarga yig'ish extensioni kodni juda soddalashtiradi.",
        """Yig'ilgan massiv: ["A", "B"]"""
    ),
    (
        748,
        "Task.detached da ustuvorlikni aniq belgilash",
        "Muhim fondagi hisoblashni alohida ustuvorlik bilan chiqarish.",
        """import Foundation

Task.detached(priority: .utility) {
    print("Utility ustuvorlikda fon vazifasi bajarildi.")
}
""",
        "Detached vazifalar tizim resurslaridan mustaqil foydalanish zarur bo'lganda qo'llaniladi.",
        """Utility ustuvorlikda fon vazifasi bajarildi."""
    ),
    (
        749,
        "Asinxron xatoliklar zanjiri va stacktrace",
        "Ketma-ket asinxron xatoliklarning qayerda ushlanishi.",
        """import Foundation

func stepA() async throws { throw URLError(.timedOut) }
func stepB() async throws { try await stepA() }

Task {
    do {
        try await stepB()
    } catch {
        print("Zanjirdagi asinxron xatolik: \\(error)")
    }
}
""",
        "Asinxron xatoliklar 'try await' zanjiri bo'ylab to'g'ri yuqoriga uzatiladi.",
        """Zanjirdagi asinxron xatolik: The operation couldn’t be completed. (NSURLErrorDomain error -1001.)"""
    ),
    (
        750,
        "Amaliy loyiha: Parallel yuklash, kesh va real vaqtli monitoring tizimi",
        "TaskGroup, AsyncStream, withCheckedContinuation, Timeout va Cancellation mexanizmlarini to'liq o'z ichiga olgan reaktiv monitoring moduli.",
        """import Foundation

struct SensorTelemetry: Sendable {
    let sensorID: String
    let value: Double
    let timestamp: Date
}

class TelemetryCollector {
    func readSensorData(id: String) async -> SensorTelemetry {
        // Simulyatsiya qilingan asinxron o'qish
        return SensorTelemetry(sensorID: id, value: Double.random(in: 20...30), timestamp: Date())
    }
    
    func streamTelemetry(sensorIDs: [String]) -> AsyncStream<SensorTelemetry> {
        AsyncStream { continuation in
            let task = Task {
                await withTaskGroup(of: SensorTelemetry.self) { group in
                    for id in sensorIDs {
                        group.addTask {
                            return await self.readSensorData(id: id)
                        }
                    }
                    for await reading in group {
                        continuation.yield(reading)
                    }
                }
                continuation.finish()
            }
            
            continuation.onTermination = { _ in
                task.cancel()
                print("Monitoring oqimi to'xtatildi.")
            }
        }
    }
}

let collector = TelemetryCollector()
let sensorIDs = ["TEMP_ROOM_1", "TEMP_ROOM_2", "TEMP_ROOM_3"]

print("=== REAL VAQTLI SENSOR MONITORINGI ISHGA TUSHDI ===")
Task {
    for await telemetry in collector.streamTelemetry(sensorIDs: sensorIDs) {
        let valFormatted = String(format: "%.1f°C", telemetry.value)
        print("[TELEMETRIYA]: Sensor \\(telemetry.sensorID) -> \\(valFormatted)")
    }
    print("Barcha sensorlar ma'lumotlari muvaffaqiyatli qabul qilindi.")
}
""",
        "Ushbu yakuniy loyihada 'TaskGroup', 'AsyncStream', 'Sendable', 'onTermination' va kooperativ bekor qilish birlashtirilib, sanoat darajasidagi real vaqtli telemetriya tizimi qurildi.",
        """=== REAL VAQTLI SENSOR MONITORINGI ISHGA TUSHDI ===
[TELEMETRIYA]: Sensor TEMP_ROOM_1 -> 25.4°C
[TELEMETRIYA]: Sensor TEMP_ROOM_2 -> 22.8°C
[TELEMETRIYA]: Sensor TEMP_ROOM_3 -> 28.1°C
Barcha sensorlar ma'lumotlari muvaffaqiyatli qabul qilindi.
Monitoring oqimi to'xtatildi."""
    )
]

tasks = [format_task(*t) for t in tasks_data]
save_file("swift_15_async_await_va_structured_concurrency.md", tasks)
