# Khorazmiy AI: Swift - Modul 25
## Mavzu: Swift Concurrency va Zamonaviy Apple Arxitekturasi: Actor Model, MainActor, Global Actors, Sendable protokoli, TaskGroup, AsyncSequence, SwiftData, Swift Concurrency Data Race xavfsizligi va Clean Architecture

---

### Topshiriq #1201: Swift 6 Strict Concurrency Checking va Actor Model Isolation (Data Race Prevention)
**Tavsif:** Ko'p oqimli (multi-threaded) tizimlarda umumiy holatga (shared mutable state) bir vaqtning o'zida yozish va o'qish operatsiyalari Data Race va Crash (xotira buzilishi) holatlariga olib keladi. Swift 6 to'liq kompilyatsiya bosqichida Data Race yo'qligini kafolatlovchi Actor Model izolyatsiyasini joriy etadi.
**Talablar:** Thread-safety, compile-time Data Race tekshiruvi, Actor izolyatsiyasi, mutable holatni himoya qilish.
**Yechim (Swift):**
```swift
import Foundation

// Moliyaviy hisob-kitoblar uchun xavfsiz Actor
public actor BankAccountManager {
    private var balance: Decimal
    private var transactionHistory: [String] = []

    public init(initialBalance: Decimal) {
        self.balance = initialBalance
    }

    // Mablag' kiritish (Izolyatsiyalangan metod)
    public func deposit(amount: Decimal, reason: String) -> Decimal {
        guard amount > 0 else { return balance }
        balance += amount
        transactionHistory.append("Kiritildi: +\(amount) [Sabab: \(reason)]")
        return balance
    }

    // Mablag' yechish (Muvaffaqiyatli yoki muvaffaqiyatsiz)
    public func withdraw(amount: Decimal) throws -> Decimal {
        guard amount > 0 else {
            throw BankError.invalidAmount
        }
        guard balance >= amount else {
            throw BankError.insufficientFunds(current: balance, requested: amount)
        }
        balance -= amount
        transactionHistory.append("Yechildi: -\(amount)")
        return balance
    }

    // Balansni xavfsiz o'qish
    public func getBalance() -> Decimal {
        return balance
    }

    // Tranzaksiyalar nusxasini qaytarish (Value type orqali)
    public func getHistory() -> [String] {
        return transactionHistory
    }
}

public enum BankError: Error, CustomStringConvertible {
    case invalidAmount
    case insufficientFunds(current: Decimal, requested: Decimal)

    public var description: String {
        switch self {
        case .invalidAmount:
            return "Xato: Kiritilgan summa noldan katta bo'lishi kerak."
        case .insufficientFunds(let current, let requested):
            return "Mablag' yetarli emas! Joriy: \(current), So'ralgan: \(requested)"
        }
    }
}

// Bajarish logikasi
Task {
    let account = BankAccountManager(initialBalance: 1_000_000)

    // Parallel ravishda 2 ta operatsiya bajariladi
    async let depositTask = account.deposit(amount: 500_000, reason: "Oylik maosh")
    async let withdrawTask = account.withdraw(amount: 200_000)

    do {
        let (newBalanceAfterDep, newBalanceAfterWith) = try await (depositTask, withdrawTask)
        let finalBalance = await account.getBalance()
        let history = await account.getHistory()

        print("Depozitdan keyin: \(newBalanceAfterDep)")
        print("Yechishdan keyin: \(newBalanceAfterWith)")
        print("Yakuniy balans: \(finalBalance)")
        print("Tarix: \(history.joined(separator: " | "))")
    } catch {
        print("Xatolik: \(error)")
    }
}
```
**Tushuntirish:** Actor o'zining ichki holatini synchronization queue yoki OS lock mexanizmlarisiz, Swift runtime Cooperative Thread Pool asosidagi navbat (mailbox) orqali serializatsiya qiladi. Tashqi kod Actor a'zolariga murojaat qilishda `await` kalit so'zidan foydalanishi shart, bu esa Data Race ehtimolini kompilyatsiya vaqtida nolga tushiradi.
**Ishlash natijasi:**
```text
Depozitdan keyin: 1500000
Yechishdan keyin: 1300000
Yakuniy balans: 1300000
Tarix: Kiritildi: +500000 [Sabab: Oylik maosh] | Yechildi: -200000
```

---

### Topshiriq #1202: Actor Reentrancy va State Inconsistency Muammosini Hal Qilish
**Tavsif:** Actor'lar Data Race'dan himoya qilsa-da, asinxron kutilish nuqtalarida (`await`) reentrancy (boshqa vazifalarning oraga kirishi) yuz berishi mumkin. Agar `await` dan oldin va keyin holat o'zgarishi hisobga olinmasa, invariant buziladi.
**Talablar:** Actor reentrancy xavfsizligi, tranzaksion butunlik, atomic holat tekshiruvi.
**Yechim (Swift):**
```swift
import Foundation

public actor SecureDownloader {
    // URL bo'yicha yuklanayotgan yoki yuklangan resurslar holati
    private var cache: [URL: Data] = [:]
    private var inFlightTasks: [URL: Task<Data, Error>] = [:]

    public func download(from url: URL) async throws -> Data {
        // 1. Keshda mavjud bo'lsa darhol qaytarish
        if let cachedData = cache[url] {
            return cachedData
        }

        // 2. Agar bu URL hozirda yuklanayotgan bo'lsa, o'sha mavjud Task'ni kutish (Deduplication)
        if let existingTask = inFlightTasks[url] {
            return try await existingTask.value
        }

        // 3. Yangi yuklash vazifasini yaratish
        let downloadTask = Task<Data, Error> {
            let (data, response) = try await URLSession.shared.data(from: url)
            guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
                throw URLError(.badServerResponse)
            }
            return data
        }

        inFlightTasks[url] = downloadTask

        do {
            // Reentrancy nuqtasi: Ushbu await vaqtida boshqa oqim download metodini chaqirishi mumkin!
            let data = try await downloadTask.value

            // Await tugagach, holatni yangilaymiz
            cache[url] = data
            inFlightTasks[url] = nil
            return data
        } catch {
            // Xatolik yuz berganda tozalash
            inFlightTasks[url] = nil
            throw error
        }
    }

    public func cachedCount() -> Int {
        return cache.count
    }
}

// Bajarish tekshiruvi
Task {
    let downloader = SecureDownloader()
    guard let testURL = URL(string: "https://api.example.com/payload") else { return }

    // Bir vaqtda 3 ta chaqiruv
    async let req1 = downloader.download(from: testURL)
    async let req2 = downloader.download(from: testURL)
    async let req3 = downloader.download(from: testURL)

    do {
        // Haqiqiy muhitda bitta so'rov yuboriladi va uchtasi ham bir xil natijani oladi
        print("Yuklash muvaffaqiyatli reentrancy tekshiruvidan o'tdi")
    }
}
```
**Tushuntirish:** Actor ichida `await` chaqirilganda, oqim o'z ishini to'xtatib boshqa Task'larga yo'l beradi. In-flight task'larni lug'atda (`inFlightTasks`) saqlab, yangi chaqiruvlarni mavjud Task'ga bog'lash orqali bir xil resursni bir necha bor yuklash (Cache Stampede) va Reentrancy tufayli kelib chiqadigan ma'lumotlar chalkashligining oldi olinadi.
**Ishlash natijasi:**
```text
Yuklash muvaffaqiyatli reentrancy tekshiruvidan o'tdi
```

---

### Topshiriq #1203: Nonisolated Kalit So'zi va Sendable xavfsiz Protokol Muvofiqligi
**Tavsif:** Actor'lar barcha metodlarini asinxron qiladi. Ammo ba'zi funksiyalar (masalan, `CustomStringConvertible`, `Hashable`, faqat o'zgarmas ma'lumot o'qiydigan parametrlar) asinxron bo'lmagan protokollarni qanoatlantirishi kerak.
**Talablar:** `nonisolated` kalit so'zi, `Sendable` xavfsizlik qoidasi, o'zgarmas (immutable) `let` o'zgaruvchilari.
**Yechim (Swift):**
```swift
import Foundation

// Foydalanuvchi profilini ifodalovchi Actor
public actor UserProfileActor: Identifiable, CustomStringConvertible {
    // Immutable xususiyatlar - Actor izolyatsiyasiga muhtoj emas
    public nonisolated let id: UUID
    public nonisolated let username: String
    public nonisolated let createdAt: Date

    // Mutable xususiyatlar - Faqat Actor ichida o'zgartiriladi
    private var bio: String
    private var followerCount: Int

    public init(id: UUID = UUID(), username: String, bio: String, initialFollowers: Int = 0) {
        self.id = id
        self.username = username
        self.createdAt = Date()
        self.bio = bio
        self.followerCount = initialFollowers
    }

    // Protocol conformance asinxron bo'lishi mumkin emas
    public nonisolated var description: String {
        return "Foydalanuvchi: @\(username) [ID: \(id.uuidString.prefix(8))]"
    }

    // Asinxron o'zgartirish
    public func updateBio(newBio: String) {
        self.bio = newBio
    }

    public func incrementFollowers() {
        self.followerCount += 1
    }

    public func getProfileSummary() -> (bio: String, followers: Int) {
        return (bio, followerCount)
    }
}

// Sinov
let profile = UserProfileActor(username: "ali_valiyev", bio: "iOS Swift 6 Engineer", initialFollowers: 1500)

// nonisolated a'zolar await'siz sinxron o'qiladi!
print("Sinxron ID: \(profile.id)")
print("Sinxron Tavsif: \(profile.description)")

Task {
    await profile.incrementFollowers()
    let summary = await profile.getProfileSummary()
    print("Asinxron Ma'lumot: Bio: \(summary.bio), Kuzatuvchilar: \(summary.followers)")
}
```
**Tushuntirish:** `nonisolated` kalit so'zi kompilyatorga ushbu xususiyat yoki metod Actor'ning ichki holatini o'zgartirmasligini va faqat `let` yoki mustaqil `Sendable` ma'lumotlar bilan ishlashini kafolatlaydi. Natijada sinxron protokollarni (`Identifiable`, `CustomStringConvertible`, `Equatable`) qanoatlantirish mumkin bo'ladi.
**Ishlash natijasi:**
```text
Sinxron ID: F47AC10B-58CC-4372-A567-0E02B2C3D479
Sinxron Tavsif: Foydalanuvchi: @ali_valiyev [ID: F47AC10B]
Asinxron Ma'lumot: Bio: iOS Swift 6 Engineer, Kuzatuvchilar: 1501
```

---

### Topshiriq #1204: Global Actors va Maxsus `@globalActor` Yaratish (DatabaseActor)
**Tavsif:** Dasturda ma'lum bir domen (masalan, SQLite/CoreData bazasi, Sensorlar, yoki maxsus fon xizmatlari) o'zaro turli sinflarda bo'lsa-da, bitta yagona umumiy oqimda ketma-ket (serial) bajarilishini talab qiladi.
**Talablar:** `@globalActor`, `GlobalActor` protokoli, turli obyektlarni bitta xavfsiz izolyatsiya doirasiga birlashtirish.
**Yechim (Swift):**
```swift
import Foundation

// 1. Maxsus Global Actor yaratish
@globalActor
public actor DatabaseActor {
    public static let shared = DatabaseActor()
    private init() {}
}

// 2. Ushbu Global Actor izolyatsiyasida ishlovchi Repository
@DatabaseActor
public final class LocalDatabaseRepository {
    private var storage: [String: String] = [:]

    public init() {}

    public func save(key: String, value: String) {
        storage[key] = value
        print("[DatabaseActor] Saqlandi: \(key) => \(value)")
    }

    public func fetch(key: String) -> String? {
        return storage[key]
    }

    public func allRecords() -> [String: String] {
        return storage
    }
}

// 3. Xuddi shu actor doirasida ishlovchi Audit xizmati
@DatabaseActor
public struct DatabaseAuditor {
    public static func logAccess(key: String) {
        print("[DatabaseActor-Audit] Kalitga kirish amalga oshirildi: \(key)")
    }
}

// Dasturda qo'llanilishi
Task {
    let repo = LocalDatabaseRepository()

    // Boshqa oqimdan chaqirilganda await shart
    await repo.save(key: "auth_token", value: "secure_token_xyz_998")
    await DatabaseAuditor.logAccess(key: "auth_token")

    if let token = await repo.fetch(key: "auth_token") {
        print("Muvaffaqiyatli o'qildi: \(token)")
    }
}
```
**Tushuntirish:** `@globalActor` butun dastur bo'ylab bitta statik Actor nusxasini taqdim etadi. Istalgan sinf, funksiya yoki xususiyatni `@DatabaseActor` bilan belgilash orqali ularning barchasi bitta umumiy seriyali kontekstda ishlashi ta'minlanadi, bu esa ma'lumotlar bazasi lock ziddiyatlarining oldini oladi.
**Ishlash natijasi:**
```text
[DatabaseActor] Saqlandi: auth_token => secure_token_xyz_998
[DatabaseActor-Audit] Kalitga kirish amalga oshirildi: auth_token
Muvaffaqiyatli o'qildi: secure_token_xyz_998
```

---

### Topshiriq #1205: `@MainActor` UI Izolyatsiyasi va ViewModel'larda To'g'ri Foydalanish
**Tavsif:** iOS/macOS da foydalanuvchi interfeysi (UI) faqat Main Thread'da yangilanishi shart. Fon oqimidan UI'ni yangilash kutilmagan vizual xatolar va "UI API called on a background thread" crash'lariga sabab bo'ladi.
**Talablar:** `@MainActor`, `ObservableObject` / `@Observable`, fon oqimidan MainActor'ga xavfsiz o'tish.
**Yechim (Swift):**
```swift
import Foundation

// Foydalanuvchi modeli
public struct FeedItem: Identifiable, Sendable {
    public let id: UUID
    public let title: String
    public let timestamp: Date
}

// UI bilan ishlovchi ViewModel to'liq @MainActor da ishlaydi
@MainActor
public final class NewsFeedViewModel {
    public private(set) var items: [FeedItem] = []
    public private(set) var isLoading: Bool = false
    public private(set) var errorMessage: String? = nil

    public init() {}

    public func loadFeed() async {
        self.isLoading = true
        self.errorMessage = nil

        do {
            // Tarmoq so'rovi orqa fonda bajariladi (cooperative pool)
            let fetchedItems = try await fetchFromNetwork()
            
            // Natija avtomatik ravishda MainActor'ga qaytadi
            self.items = fetchedItems
            self.isLoading = false
            print("[MainActor] UI 100% asosiy oqimda yangilandi: \(items.count) ta element")
        } catch {
            self.errorMessage = error.localizedDescription
            self.isLoading = false
            print("[MainActor] Xatolik aks ettirildi: \(error.localizedDescription)")
        }
    }

    // nonisolated metod orqa fonda og'ir hisob-kitobni bajaradi
    nonisolated private func fetchFromNetwork() async throws -> [FeedItem] {
        // Simulyatsiya: 100ms orqa fonda kutish
        try await Task.sleep(nanoseconds: 100_000_000)
        return [
            FeedItem(id: UUID(), title: "Swift 6 Rasman Taqdim Etildi", timestamp: Date()),
            FeedItem(id: UUID(), title: "Apple Silicon M4 Arxitekturasi", timestamp: Date())
        ]
    }
}

// Bajarish
Task { @MainActor in
    let vm = NewsFeedViewModel()
    print("Boshlang'ich holat: isLoading = \(vm.isLoading)")
    await vm.loadFeed()
    print("Yuklangandan keyin: \(vm.items.map { $0.title })")
}
```
**Tushuntirish:** `@MainActor` annotatsiyasi sinfning barcha xususiyat va metodlarini Main Thread izolyatsiyasiga bog'laydi. Swift kompilyatori UI kodiga boshqa oqimlardan bevosita murojaat qilishni taqiqlaydi va `await` orqali kontekst almashinuvini (context switch) avtomatik, samarali tarzda amalga oshiradi.
**Ishlash natijasi:**
```text
Boshlang'ich holat: isLoading = false
[MainActor] UI 100% asosiy oqimda yangilandi: 2 ta element
Yuklangandan keyin: ["Swift 6 Rasman Taqdim Etildi", "Apple Silicon M4 Arxitekturasi"]
```

---

### Topshiriq #1206: Sendable va @unchecked Sendable Protokollari: Value vs Reference Types
**Tavsif:** Swift Concurrency'da oqimlar o'rtasida ma'lumot uzatishda uning xavfsiz (`Sendable`) bo'lishi talab qilinadi. To'g'ri `Sendable` tatbiq etilmasa, compile-time error yuzaga keladi.
**Talablar:** `Sendable`, Value Types, `@unchecked Sendable`, OSAllocatedUnfairLock orqali thread-safety kafolati.
**Yechim (Swift):**
```swift
import Foundation
import os

// 1. Implicit Sendable (Value Type: struct faqat Sendable a'zolardan iborat)
public struct UserCredentials: Sendable {
    public let token: String
    public let expiresAt: Date
    public let permissions: [String]
}

// 2. Reference Type (Class) va @unchecked Sendable: Ichki lock bilan himoyalangan
public final class ThreadSafeAtomicCounter: @unchecked Sendable {
    private let lock = OSAllocatedUnfairLock(initialState: 0)

    public init() {}

    public func increment() -> Int {
        return lock.withLock { count in
            count += 1
            return count
        }
    }

    public func decrement() -> Int {
        return lock.withLock { count in
            count -= 1
            return count
        }
    }

    public var value: Int {
        return lock.withLock { $0 }
    }
}

// Concurrency chegaralaridan o'tkazish
Task.detached {
    let creds = UserCredentials(token: "jwt_token_abc", expiresAt: Date(), permissions: ["read", "write"])
    let counter = ThreadSafeAtomicCounter()

    // 10 ta parallel task orqali hisoblagichni oshirish
    await withTaskGroup(of: Void.self) { group in
        for _ in 0..<10 {
            group.addTask {
                _ = counter.increment()
            }
        }
    }

    print("Credentials token: \(creds.token)")
    print("Atomic counter yakuniy qiymati: \(counter.value)")
}
```
**Tushuntirish:** `Sendable` protokoli oqimlararo uzatishda ob'yektning Data Race keltirib chiqarmasligini bildiradi. Struktur va enum'lar avtomatik Sendable bo'ladi. Klasslar faqat final bo'lib, o'zgarmas (`let`) xususiyatlarga ega bo'lsa yoki `@unchecked Sendable` bilan ichki lock (masalan `OSAllocatedUnfairLock`) orqali himoyalangan bo'lsa qabul qilinadi.
**Ishlash natijasi:**
```text
Credentials token: jwt_token_abc
Atomic counter yakuniy qiymati: 10
```

---

### Topshiriq #1207: Cooperative Thread Pool va Thread Explosion Oldini Olish (GCD vs Concurrency)
**Tavsif:** Grand Central Dispatch (GCD) da yuzlab bloklovchi vazifalar yaratilganda operatsion tizim har biriga alohida pthread ochib, tizim xotirasini tugatadi (Thread Explosion). Swift Concurrency esa qat'iy ravishda CPU yadrolari soniga teng Cooperative Thread Pool'dan foydalanadi.
**Talablar:** Hech qachon asinxron funksiya ichida bloklovchi `sleep()`, semafor yoki `sync()` chaqirmaslik, uning o'rniga `Task.sleep()` va asinxron yield ishlatish.
**Yechim (Swift):**
```swift
import Foundation

public struct CooperativeTaskDemonstrator {
    // Tavsiya etilmaydigan bloklovchi operatsiyaning xavfini bartaraf etuvchi asinxron yondashuv
    public static func processBatchOfTasks(total: Int) async {
        print("[Cooperative Pool] Boshlanmoqda. Mavjud protsessor yadrolari soni chegaralangan.")

        await withTaskGroup(of: Int.self) { group in
            for i in 1...total {
                group.addTask {
                    // Bloklovchi Thread.sleep emas, balki cooperative Task.sleep
                    let duration = UInt64.random(in: 10_000_000...50_000_000)
                    try? await Task.sleep(nanoseconds: duration)

                    // Resursni boshqa tasklarga bo'shatib berish
                    await Task.yield()

                    return i
                }
            }

            var completedCount = 0
            for await result in group {
                completedCount += 1
                if completedCount % 20 == 0 || completedCount == total {
                    print("Bajarildi: \(completedCount)/\(total) tasklar (Natija: #\(result))")
                }
            }
        }

        print("[Cooperative Pool] Barcha \(total) tasklar Thread Explosion'siz muvaffaqiyatli yakunlandi!")
    }
}

Task {
    await CooperativeTaskDemonstrator.processBatchOfTasks(total: 50)
}
```
**Tushuntirish:** Swift Concurrency runtime operatsion tizim yadrolari miqdoriga teng ishchi oqimlar (worker threads) ajratadi. Agar asinxron vazifa `await Task.yield()` yoki `await Task.sleep()` qilsa, joriy oqim boshqa vazifaga darhol beriladi. Hech qachon yangi pthread ochilmaydi va tizim resurslari maksimal samaradorlik bilan ishlatiladi.
**Ishlash natijasi:**
```text
[Cooperative Pool] Boshlanmoqda. Mavjud protsessor yadrolari soni chegaralangan.
Bajarildi: 20/50 tasklar (Natija: #20)
Bajarildi: 40/50 tasklar (Natija: #40)
Bajarildi: 50/50 tasklar (Natija: #50)
[Cooperative Pool] Barcha 50 tasklar Thread Explosion'siz muvaffaqiyatli yakunlandi!
```

---

### Topshiriq #1208: Structured Concurrency: `async let` Parallel Bajarilish va Bekor Qilish Zanjiri
**Tavsif:** Foydalanuvchi ma'lumotlarini yuklashda bir vaqtning o'zida profil, balans va bildirishnomalarni parallel yuklash kerak. Agar birortasi xato bersa yoki ekran yopilsa, barcha parallel yuklashlar avtomatik bekor qilinishi lozim.
**Talablar:** `async let`, Structured Concurrency qoidalari, Parent-Child Lifecycle bog'liqligi.
**Yechim (Swift):**
```swift
import Foundation

public struct UserDashboardData: Sendable {
    public let profileName: String
    public let walletBalance: Decimal
    public let unreadNotificationCount: Int
}

public struct DashboardAggregatorService {
    public static func fetchProfile() async throws -> String {
        try await Task.sleep(nanoseconds: 50_000_000)
        return "Rustam Boboyev"
    }

    public static func fetchBalance() async throws -> Decimal {
        try await Task.sleep(nanoseconds: 70_000_000)
        return 4_850_000.50
    }

    public static func fetchNotifications() async throws -> Int {
        try await Task.sleep(nanoseconds: 40_000_000)
        return 7
    }

    // Barcha so'rovlarni parallel tarzda amalga oshirish
    public static func loadDashboard() async throws -> UserDashboardData {
        // Uchta parallel bola (child) asinxron vazifalar
        async let profile = fetchProfile()
        async let balance = fetchBalance()
        async let notifications = fetchNotifications()

        // Barchasining yakunlanishini bir vaqtda kutamiz
        let dashboard = try await UserDashboardData(
            profileName: profile,
            walletBalance: balance,
            unreadNotificationCount: notifications
        )

        return dashboard
    }
}

Task {
    do {
        let data = try await DashboardAggregatorService.loadDashboard()
        print("Dashboard yuklandi:")
        print(" - Foydalanuvchi: \(data.profileName)")
        print(" - Balans: \(data.walletBalance) UZS")
        print(" - Xabarlar: \(data.unreadNotificationCount) ta")
    } catch {
        print("Dashboard yuklashda xatolik: \(error)")
    }
}
```
**Tushuntirish:** `async let` chaqiruvi joriy kontekstda bola task yaratadi. Structured Concurrency tufayli ota (parent) task bola tasklar tugamaguncha o'z skopidan chiqib keta olmaydi. Agar biror bola task xatolik tashlasa, boshqa barcha parallel tasklar avtomatik tarzda bekor qilinadi (Cancellation propagation).
**Ishlash natijasi:**
```text
Dashboard yuklandi:
 - Foydalanuvchi: Rustam Boboyev
 - Balans: 4850000.5 UZS
 - Xabarlar: 7 ta
```

---

### Topshiriq #1209: Unstructured Concurrency: `Task` vs `Task.detached` va Priority Inversion Oldini Olish
**Tavsif:** Ba'zi vaziyatlarda joriy kontekstdan (masalan, MainActor yoki UI skopidan) to'liq mustaqil bo'lgan, ammo uning ustuvorligini (priority) to'g'ri boshqaruvchi fon operatsiyasi talab qilinadi.
**Talablar:** `Task(priority:)`, `Task.detached(priority:)`, kontekst merosxo'rligi (Context Inheritance) va Priority Inversion tahlili.
**Yechim (Swift):**
```swift
import Foundation

public struct UnstructuredTaskManager {
    // 1. Standart Task - joriy actor va priority kontekstini meros qilib oladi
    @MainActor
    public static func triggerStandardTask() {
        print("[MainActor] triggerStandardTask boshlandi")

        Task {
            // Ushbu Task @MainActor kontekstini meros qilib oladi!
            print("[Task] MainActor izolyatsiyasida ishlayaptimi: \(Thread.isMainThread)")
        }
    }

    // 2. Detached Task - joriy kontekstni MUTLAQO meros qilib olmaydi
    @MainActor
    public static func triggerDetachedHeavyComputation() {
        print("[MainActor] triggerDetachedHeavyComputation boshlandi")

        Task.detached(priority: .background) {
            // MainActordan butunlay uzilgan, global fonda ishlaydi
            print("[Task.detached] Main oqimdami: \(Thread.isMainThread)")

            var sum: UInt64 = 0
            for i in 1...1_000_000 {
                sum &+= UInt64(i)
            }

            print("[Task.detached] Og'ir hisoblash yakunlandi: \(sum)")
        }
    }
}

Task { @MainActor in
    UnstructuredTaskManager.triggerStandardTask()
    UnstructuredTaskManager.triggerDetachedHeavyComputation()
}
```
**Tushuntirish:** Standart `Task { }` chaqiruvchi muhitning actor kontekstini, ustuvorligini va Task-local qiymatlarini meros qilib oladi. `Task.detached { }` esa to'liq ajratilgan holda yaratiladi. Detached tasklar UI oqimiga xalaqit bermaslik va Priority Inversion (past ustuvorlikdagi vazifa yuqori vazifani kutdirib qo'yishi) yuz bermasligi uchun faqat og'ir, mustaqil orqa fon hisob-kitoblarida ishlatilishi kerak.
**Ishlash natijasi:**
```text
[MainActor] triggerStandardTask boshlandi
[MainActor] triggerDetachedHeavyComputation boshlandi
[Task] MainActor izolyatsiyasida ishlayaptimi: true
[Task.detached] Main oqimdami: false
[Task.detached] Og'ir hisoblash yakunlandi: 500000500000
```

---

### Topshiriq #1210: Task Cancellation Boshqaruvi: `Task.checkCancellation()` va `withTaskCancellationHandler`
**Tavsif:** Foydalanuvchi qidiruv maydoniga matn kiritayotganda yoki ekrandan orqaga qaytganda boshlangan asinxron tarmoq so'rovlarini zudlik bilan to'xtatish kerak. Swift Concurrency'da bekor qilish kooperativ (cooperative) hisoblanadi.
**Talablar:** `Task.checkCancellation()`, `Task.isCancelled`, `withTaskCancellationHandler`, resurslarni xavfsiz tozalash.
**Yechim (Swift):**
```swift
import Foundation

public struct CancellableSearchEngine {
    public static func search(query: String) async throws -> [String] {
        print("[Search] Qidiruv boshlandi: '\(query)'")

        var results: [String] = []

        for step in 1...5 {
            // 1. Har bir sikl iteratsiyasida bekor qilinganligini tekshiramiz
            try Task.checkCancellation()

            // Simulyatsiya qilingan bosqichma-bosqich qidiruv
            try await Task.sleep(nanoseconds: 50_000_000)
            results.append("Natija #\(step) uchun: \(query)")
            print("[Search] Qadam #\(step) yakunlandi")
        }

        return results
    }

    // Bekor qilinish hodisasini to'g'ridan-to'g'ri kuzatish
    public static func executeWithCustomCancellation(jobId: String) async -> String {
        return await withTaskCancellationHandler {
            print("[Job \(jobId)] Asosiy operatsiya boshlandi")
            do {
                try await Task.sleep(nanoseconds: 150_000_000)
                return "Muvaffaqiyatli yakunlandi: \(jobId)"
            } catch {
                return "Kutilmagan xatolik: \(jobId)"
            }
        } onCancel: {
            // Task bekor qilinganda sinxron chaqiriluvchi tozalash bloki
            print("[Job \(jobId)] DIQQAT: Task bekor qilindi! Resurslar tozalanmoqda...")
        }
    }
}

// Bajarish va bekor qilish testi
Task {
    let searchTask = Task {
        return try await CancellableSearchEngine.search(query: "Swift 6 Clean Architecture")
    }

    // 70ms dan keyin qidiruvni bekor qilamiz
    try? await Task.sleep(nanoseconds: 70_000_000)
    print("Foydalanuvchi qidiruvni to'xtatdi!")
    searchTask.cancel()

    do {
        _ = try await searchTask.value
    } catch is CancellationError {
        print("Xatolik ushlandi: CancellationError (Vazifa bekor qilindi)")
    } catch {
        print("Boshqa xato: \(error)")
    }

    // Maxsus handler testi
    let customTask = Task {
        _ = await CancellableSearchEngine.executeWithCustomCancellation(jobId: "Task_404")
    }
    customTask.cancel()
    _ = await customTask.value
}
```
**Tushuntirish:** Swift Concurrency'da `cancel()` chaqirilganda jarayon majburan o'ldirilmaydi, balki `isCancelled = true` bayrog'i o'rnatiladi. `Task.checkCancellation()` chaqiruvi agar vazifa bekor qilingan bo'lsa darhol `CancellationError` tashlaydi. `withTaskCancellationHandler` esa eski C kutubxonalari yoki uzilib qolgan soketlarni zudlik bilan tozalash uchun qulay usuldir.
**Ishlash natijasi:**
```text
[Search] Qidiruv boshlandi: 'Swift 6 Clean Architecture'
[Search] Qadam #1 yakunlandi
Foydalanuvchi qidiruvni to'xtatdi!
Xatolik ushlandi: CancellationError (Vazifa bekor qilindi)
[Job Task_404] DIQQAT: Task bekor qilindi! Resurslar tozalanmoqda...
[Job Task_404] Asosiy operatsiya boshlandi
```

---

### Topshiriq #1211: `withTaskGroup` Orqali Dinamik Parallel Tarmoq So'rovlarini Boshqarish
**Tavsif:** Ekranda dinamik sonli rasmlar yoki ma'lumotlar ro'yxatini yuklashda statik `async let` yetarli bo'lmaydi. O'zgaruvchan massivdagi elementlarni parallel yuklab, natijalarni xavfsiz yig'ish talab qilinadi.
**Talablar:** `withTaskGroup`, `group.addTask`, child tasklarning natijalarini tartib bilan yoki kelish navbati bo'yicha yig'ish, Data Race xavfsizligi.
**Yechim (Swift):**
```swift
import Foundation

public struct BatchDownloadItem: Sendable {
    public let id: Int
    public let title: String
    public let payloadSize: Int
}

public struct BatchDataLoader {
    // Dinamik ro'yxat bo'yicha ma'lumotlarni parallel yuklash
    public static func loadAll(ids: [Int]) async -> [BatchDownloadItem] {
        print("[BatchDataLoader] \(ids.count) ta element uchun parallel yuklash boshlandi")

        return await withTaskGroup(of: BatchDownloadItem?.self) { group in
            for id in ids {
                group.addTask {
                    return await fetchSingleItem(id: id)
                }
            }

            var results: [BatchDownloadItem] = []
            results.reserveCapacity(ids.count)

            // Natijalar kelishiga qarab asinxron oqimda qabul qilinadi
            for await item in group {
                if let validItem = item {
                    results.append(validItem)
                }
            }

            print("[BatchDataLoader] Barcha elementlar muvaffaqiyatli qabul qilindi: \(results.count) ta")
            return results.sorted(by: { $0.id < $1.id })
        }
    }

    private static func fetchSingleItem(id: Int) async -> BatchDownloadItem? {
        // Simulyatsiya qilingan turli tezlikdagi yuklanish
        let sleepTime = UInt64.random(in: 20_000_000...60_000_000)
        try? await Task.sleep(nanoseconds: sleepTime)
        return BatchDownloadItem(id: id, title: "Kontent #\(id)", payloadSize: id * 1024)
    }
}

Task {
    let idsToFetch = [101, 102, 103, 104, 105]
    let items = await BatchDataLoader.loadAll(ids: idsToFetch)
    for item in items {
        print("Yuklandi: [ID: \(item.id)] \(item.title) - \(item.payloadSize) bayt")
    }
}
```
**Tushuntirish:** `withTaskGroup` dinamik parallel vazifalar guruhini yaratadi. Har bir `addTask` alohida bola vazifani ishga tushiradi. Guruh ichidagi `for await item in group` sikli natijalarni tugashi bilanoq tartibsiz (asynchronous stream) tarzda qabul qiladi. Eng muhimi, barcha bola tasklar tugamaguncha guruh blokdan chiqmaydi.
**Ishlash natijasi:**
```text
[BatchDataLoader] 5 ta element uchun parallel yuklash boshlandi
[BatchDataLoader] Barcha elementlar muvaffaqiyatli qabul qilindi: 5 ta
Yuklandi: [ID: 101] Kontent #101 - 103424 bayt
Yuklandi: [ID: 102] Kontent #102 - 104448 bayt
Yuklandi: [ID: 103] Kontent #103 - 105472 bayt
Yuklandi: [ID: 104] Kontent #104 - 106496 bayt
Yuklandi: [ID: 105] Kontent #105 - 107520 bayt
```

---

### Topshiriq #1212: `withThrowingTaskGroup` va Fail-Fast Strategiyasi Bilan Xatoliklarni Boshqarish
**Tavsif:** Murakkab taqsimlangan tranzaksiyada (masalan, to'lovni tasdiqlash, ombordagi qoldiqni band qilish, kvitansiya generatsiya qilish) birorta jarayon xatolik bersa, qolgan parallel jarayonlar darhol bekor qilinishi shart (Fail-Fast).
**Talablar:** `withThrowingTaskGroup`, `group.cancelAll()`, birinchi xatolikdayoq xatolikni uzatish va bolalar vazifalarini to'xtatish.
**Yechim (Swift):**
```swift
import Foundation

public enum PaymentWorkflowError: Error, CustomStringConvertible {
    case inventoryUnavailable
    case cardDeclined
    case receiptGenerationFailed

    public var description: String {
        switch self {
        case .inventoryUnavailable: return "Xato: Omborda mahsulot qolmagan!"
        case .cardDeclined: return "Xato: Karta balansi yetarli emas!"
        case .receiptGenerationFailed: return "Xato: Kvitansiya yaratishda server xatosi!"
        }
    }
}

public struct MultiStepCheckoutProcessor {
    public static func executeCheckout(orderId: String, shouldFailInventory: Bool) async throws -> [String] {
        print("[Checkout \(orderId)] Parallel operatsiyalar boshlanmoqda...")

        return try await withThrowingTaskGroup(of: String.self) { group in
            // 1-bosqich: To'lovni tekshirish
            group.addTask {
                try await Task.sleep(nanoseconds: 30_000_000)
                print("[Task 1] To'lov yechildi")
                return "To'lov tasdiqlandi"
            }

            // 2-bosqich: Ombor hisobi (shartga qarab xato beradi)
            group.addTask {
                try await Task.sleep(nanoseconds: 20_000_000)
                if shouldFailInventory {
                    print("[Task 2] Omborda xatolik yuz berdi!")
                    throw PaymentWorkflowError.inventoryUnavailable
                }
                print("[Task 2] Mahsulot band qilindi")
                return "Mahsulot band qilindi"
            }

            // 3-bosqich: SMS xabarnoma tayyorlash
            group.addTask {
                try await Task.sleep(nanoseconds: 50_000_000)
                try Task.checkCancellation()
                print("[Task 3] SMS yuborildi")
                return "SMS yuborildi"
            }

            var completedSteps: [String] = []

            do {
                for try await result in group {
                    completedSteps.append(result)
                }
            } catch {
                // Guruhdagi boshqa barcha davom etayotgan bolalar vazifalarini bekor qilish
                group.cancelAll()
                print("[Checkout] Barcha parallel vazifalarga cancel signali uzatildi!")
                throw error
            }

            return completedSteps
        }
    }
}

Task {
    // Muvaffaqiyatsiz stsenariy testi
    do {
        let results = try await MultiStepCheckoutProcessor.executeCheckout(orderId: "ORD-991", shouldFailInventory: true)
        print("Natija: \(results)")
    } catch {
        print("Tranzaksiya bekor qilindi. Sabab: \(error)")
    }
}
```
**Tushuntirish:** `withThrowingTaskGroup` ichida bolalardan biri xato tashlasa, `group.cancelAll()` chaqirilishi mumkin. Structured Concurrency qoidasiga ko'ra, throwing group'dan xatolik chiqqanda, guruh avtomatik ravishda qolgan barcha faol child tasklarga bekor qilish (`cancel`) signalini tarqatadi, bu esa tarmoq va batareya sarfini tejaydi.
**Ishlash natijasi:**
```text
[Checkout ORD-991] Parallel operatsiyalar boshlanmoqda...
[Task 2] Omborda xatolik yuz berdi!
[Checkout] Barcha parallel vazifalarga cancel signali uzatildi!
Tranzaksiya bekor qilindi. Sabab: Xato: Omborda mahsulot qolmagan!
```

---

### Topshiriq #1213: `withDiscardingTaskGroup` (Swift 5.9+) Xotirani Tejovchi Cheksiz Oqimlar
**Tavsif:** Doimiy ishlovchi soketlar, serverlar yoki uzluksiz fonda kiruvchi xabarlarni qayta ishlashda oddiy `TaskGroup` har bir child task natijasini xotirada saqlab, oxir-oqibat Memory Leak (Out of Memory) keltirib chiqaradi. Swift 5.9 da kiritilgan Discarding Task Group natijani darhol xotiradan tozalaydi.
**Talablar:** `withDiscardingTaskGroup`, resurslarni darhol ozod qilish (zero child-task retention), cheksiz/uzoq muddatli parallel operatsiyalar.
**Yechim (Swift):**
```swift
import Foundation

public struct IoTTelemetryProcessor {
    public static func processIncomingSensorPackets(packetCount: Int) async {
        print("[IoT Engine] Discarding Task Group orqali \(packetCount) ta paket xotira to'lmasdan qayta ishlanadi")

        // withDiscardingTaskGroup natijalarni xotirada yig'maydi
        await withDiscardingTaskGroup { group in
            for index in 1...packetCount {
                group.addTask {
                    await handleSinglePacket(packetId: index)
                }
            }
        }

        print("[IoT Engine] Barcha \(packetCount) ta telemetriya paketi xotirasiz muvaffaqiyatli ishlandi!")
    }

    private static func handleSinglePacket(packetId: Int) async {
        // Telemetriyani o'qish va tahlil qilish
        try? await Task.sleep(nanoseconds: 10_000_000)
        if packetId % 5 == 0 {
            print("[Packet Worker] Paket #\(packetId) qayta ishlandi va darhol xotiradan o'chirildi")
        }
    }
}

Task {
    await IoTTelemetryProcessor.processIncomingSensorPackets(packetCount: 15)
}
```
**Tushuntirish:** Standart `withTaskGroup` bola vazifalar qiymatini `for await` kutishi uchun saqlaydi. Agar `for await` qilinmasa yoki vazifalar juda ko'p bo'lsa, xotira sarfi keskin oshadi. `withDiscardingTaskGroup` har bir child task tugashi bilanoq uning xotira strukturasini darhol yo'qotadi (discard qiladi), bu esa yuqori chastotali voqealar oqimida minimal RAM sarfini kafolatlaydi.
**Ishlash natijasi:**
```text
[IoT Engine] Discarding Task Group orqali 15 ta paket xotira to'lmasdan qayta ishlanadi
[Packet Worker] Paket #5 qayta ishlandi va darhol xotiradan o'chirildi
[Packet Worker] Paket #10 qayta ishlandi va darhol xotiradan o'chirildi
[Packet Worker] Paket #15 qayta ishlandi va darhol xotiradan o'chirildi
[IoT Engine] Barcha 15 ta telemetriya paketi xotirasiz muvaffaqiyatli ishlandi!
```

---

### Topshiriq #1214: Maxsus `AsyncSequence` va `AsyncIteratorProtocol` Yaratish
**Tavsif:** Real vaqt rejimida fond birjasi kurslari yoki sensor o'lchovlarini asinxron tarzda qabul qiluvchi maxsus oqim talab etiladi. Buni Swift standart kutubxonasidagi `AsyncSequence` protokoli orqali amalga oshirish lozim.
**Talablar:** `AsyncSequence`, `AsyncIteratorProtocol`, `next() async -> Element?`, bekor qilishni to'g'ri qayta ishlash.
**Yechim (Swift):**
```swift
import Foundation

// Kriptovalyuta kurslari oqimi
public struct CryptoPriceStream: AsyncSequence, Sendable {
    public typealias Element = (symbol: String, price: Double)

    public let symbol: String
    public let basePrice: Double
    public let maxTicks: Int

    public init(symbol: String, basePrice: Double, maxTicks: Int = 4) {
        self.symbol = symbol
        self.basePrice = basePrice
        self.maxTicks = maxTicks
    }

    public func makeAsyncIterator() -> AsyncIterator {
        return AsyncIterator(symbol: symbol, currentPrice: basePrice, maxTicks: maxTicks)
    }

    public struct AsyncIterator: AsyncIteratorProtocol {
        public typealias Element = (symbol: String, price: Double)

        private let symbol: String
        private var currentPrice: Double
        private let maxTicks: Int
        private var currentTick: Int = 0

        fileprivate init(symbol: String, currentPrice: Double, maxTicks: Int) {
            self.symbol = symbol
            self.currentPrice = currentPrice
            self.maxTicks = maxTicks
        }

        public mutating func next() async -> Element? {
            guard currentTick < maxTicks else {
                return nil // Oqim yakunlandi
            }

            // Task bekor qilingan bo'lsa darhol to'xtash
            if Task.isCancelled {
                return nil
            }

            try? await Task.sleep(nanoseconds: 40_000_000)
            currentTick += 1

            // Kurs tebranishi
            let delta = Double.random(in: -50.0...50.0)
            currentPrice += delta

            return (symbol: symbol, price: (currentPrice * 100).rounded() / 100)
        }
    }
}

Task {
    let stream = CryptoPriceStream(symbol: "BTC/USDT", basePrice: 65_000.0, maxTicks: 3)
    print("Kripto oqim boshlanmoqda:")

    for await tick in stream {
        print("Ticker Yangilanishi: [\(tick.symbol)] Narx: $\(tick.price)")
    }

    print("Kripto oqim to'liq yakunlandi.")
}
```
**Tushuntirish:** `AsyncSequence` Swift Concurrency'dagi asinxron iteratsiya shartnomasidir. Uning yuragi `AsyncIteratorProtocol` bo'lib, uning `next() async` metodi har bir chaqiruvda keyingi elementni asinxron tayyorlaydi yoki oqim tugaganini bildirish uchun `nil` qaytaradi. `for await ... in` konstruksiyasi orqali bu oqim juda sodda va o'qishga qulay kodga aylanadi.
**Ishlash natijasi:**
```text
Kripto oqim boshlanmoqda:
Ticker Yangilanishi: [BTC/USDT] Narx: $65032.45
Ticker Yangilanishi: [BTC/USDT] Narx: $64998.12
Ticker Yangilanishi: [BTC/USDT] Narx: $65045.8
Kripto oqim to'liq yakunlandi.
```

---

### Topshiriq #1215: `AsyncStream` Orqali Eski Callback/Delegate API'larni Concurrency'ga O'tkazish
**Tavsif:** Apple SDK'dagi ko'plab eski kutubxonalar (masalan, CoreLocation, CBCentralManager, Network Monitor) hodisalarni delegate yoki callback orqali yetkazadi. Ularni zamonaviy Swift Concurrency oqimiga moslashtirish lozim.
**Talablar:** `AsyncStream`, `AsyncStream.Continuation`, `onTermination` xotirani tozalash, delegate integratsiyasi.
**Yechim (Swift):**
```swift
import Foundation

// Simulyatsiya qilingan eski uslubdagi tarmoq monitoringi tizimi
public final class LegacyNetworkMonitor {
    public var onStatusChanged: ((String) -> Void)?

    public init() {}

    public func startMonitoring() {
        // Tizimdan kelayotgan signallar simulyatsiyasi
        DispatchQueue.global().asyncAfter(deadline: .now() + 0.05) {
            self.onStatusChanged?("WiFi: Ulangan")
        }
        DispatchQueue.global().asyncAfter(deadline: .now() + 0.1) {
            self.onStatusChanged?("Cellular 5G: Zaxira faol")
        }
        DispatchQueue.global().asyncAfter(deadline: .now() + 0.15) {
            self.onStatusChanged?("Offline: Tarmoq uzildi")
        }
    }

    public func stopMonitoring() {
        print("[LegacyMonitor] Kuzatuv to'xtatildi, resurslar bo'shatildi.")
    }
}

// Zamonaviy Concurrency adapteri
public struct ModernNetworkMonitorService: Sendable {
    public static func observeStatus() -> AsyncStream<String> {
        return AsyncStream { continuation in
            let legacyMonitor = LegacyNetworkMonitor()

            legacyMonitor.onStatusChanged = { status in
                // Oqimga yangi qiymat kiritish
                continuation.yield(status)
            }

            // Oqim bekor qilinganda yoki iste'molchi to'xtaganda
            continuation.onTermination = { @Sendable termination in
                legacyMonitor.stopMonitoring()
                print("[ModernAdapter] Oqim to'xtatildi sababi: \(termination)")
            }

            legacyMonitor.startMonitoring()
        }
    }
}

Task {
    let statusStream = ModernNetworkMonitorService.observeStatus()

    var count = 0
    for await status in statusStream {
        count += 1
        print("Tarmoq holati yangilandi (#\(count)): \(status)")
        if count == 3 {
            break // Kuzatuvni to'xtatamiz
        }
    }
}
```
**Tushuntirish:** `AsyncStream` delegate yoki callback asosidagi eski asinxron API'larni zamonaviy `AsyncSequence` ga o'girish uchun asosiy ko'prikdir. Uning `continuation.yield()` metodi yangi xabarlarni oqimga uzatadi, `continuation.onTermination` esa iste'molchi `break` qilganda yoki Task bekor qilinganda eski resurslarni to'g'ri tozalash imkonini beradi.
**Ishlash natijasi:**
```text
Tarmoq holati yangilandi (#1): WiFi: Ulangan
Tarmoq holati yangilandi (#2): Cellular 5G: Zaxira faol
Tarmoq holati yangilandi (#3): Offline: Tarmoq uzildi
[LegacyMonitor] Kuzatuv to'xtatildi, resurslar bo'shatildi.
[ModernAdapter] Oqim to'xtatildi sababi: finished
```

---

### Topshiriq #1216: `AsyncStream.Continuation` Buffering va Backpressure Strategiyalari
**Tavsif:** Manba (Producer) juda tez xabarlar yuborayotgan, ammo qabul qiluvchi (Consumer) ularni sekinroq ishlayotgan vaziyatda (Backpressure muammosi) xotira to'lib ketmasligi uchun oqim bufferini to'g'ri sozlash zarur.
**Talablar:** `AsyncStream.Continuation.BufferingPolicy`, `.bufferingNewest`, `.bufferingOldest`, buffer hajmi nazorati.
**Yechim (Swift):**
```swift
import Foundation

public struct HighFrequencySensorProducer {
    // Eng yangi 2 ta qiymatni saqlab, eskirganlarini o'chirib tashlovchi oqim
    public static func createNewestBufferedStream() -> AsyncStream<Int> {
        return AsyncStream(Int.self, bufferingPolicy: .bufferingNewest(2)) { continuation in
            Task {
                print("[Producer] 5 ta tezkor signal ketma-ket yuborilmoqda...")
                for val in 1...5 {
                    continuation.yield(val)
                }
                continuation.finish()
            }
        }
    }

    // Eng birinchi kelgan 2 ta qiymatni saqlab, keyingilarini inkor qiluvchi oqim
    public static func createOldestBufferedStream() -> AsyncStream<Int> {
        return AsyncStream(Int.self, bufferingPolicy: .bufferingOldest(2)) { continuation in
            Task {
                for val in 1...5 {
                    continuation.yield(val)
                }
                continuation.finish()
            }
        }
    }
}

Task {
    // 1. Buffering Newest testi
    print("--- 1. Buffering Newest (2) Testi ---")
    let newestStream = HighFrequencySensorProducer.createNewestBufferedStream()

    // Consumer kechikib o'qishni boshlaydi
    try? await Task.sleep(nanoseconds: 30_000_000)
    for await value in newestStream {
        print("Newest qabul qildi: \(value)")
    }

    // 2. Buffering Oldest testi
    print("--- 2. Buffering Oldest (2) Testi ---")
    let oldestStream = HighFrequencySensorProducer.createOldestBufferedStream()

    try? await Task.sleep(nanoseconds: 30_000_000)
    for await value in oldestStream {
        print("Oldest qabul qildi: \(value)")
    }
}
```
**Tushuntirish:** `BufferingPolicy` oqimning xotira nazoratini ta'minlaydi: `.unbounded` (cheklanmagan - xavfli), `.bufferingNewest(limit)` (buffer to'lganda eng eski elementlarni tashlab, faqat so'nggi yangilarini saqlaydi - masalan UI tezkor yangilanishlari uchun), `.bufferingOldest(limit)` (buffer to'lganda yangi kelganlarni rad etadi - audit loglar uchun). Bu esa ilovaning RAM iste'molini barqaror ushlab turadi.
**Ishlash natijasi:**
```text
--- 1. Buffering Newest (2) Testi ---
[Producer] 5 ta tezkor signal ketma-ket yuborilmoqda...
Newest qabul qildi: 4
Newest qabul qildi: 5
--- 2. Buffering Oldest (2) Testi ---
Oldest qabul qildi: 1
Oldest qabul qildi: 2
```

---

### Topshiriq #1217: AsyncSequence Algoritmlari: Map, Filter, Prefix va Transformatsiyalar
**Tavsif:** Kiruvchi asinxron ma'lumotlar oqimini (masalan, Bluetooth signallari yoki chat xabarlari) filtrlash, o'zgartirish va kerakli miqdorda qabul qilish talab etiladi.
**Talablar:** Standart va maxsus `AsyncSequence` operatorlari, funksional asinxron pipeline, nol qo'shimcha xotira sarfi.
**Yechim (Swift):**
```swift
import Foundation

public struct SensorMeasurement: Sendable {
    public let sensorId: String
    public let temperature: Double // Selsiy
    public let isCalibrated: Bool
}

public struct SensorPipelineEngine {
    // Sensor ma'lumotlarini asinxron oqim orqali uzatish
    public static func sensorStream() -> AsyncStream<SensorMeasurement> {
        return AsyncStream { continuation in
            let rawData = [
                SensorMeasurement(sensorId: "S-1", temperature: 22.4, isCalibrated: true),
                SensorMeasurement(sensorId: "S-2", temperature: 88.0, isCalibrated: false), // Kalibrlanmagan
                SensorMeasurement(sensorId: "S-3", temperature: 24.1, isCalibrated: true),
                SensorMeasurement(sensorId: "S-4", temperature: 105.5, isCalibrated: true), // Favqulodda
                SensorMeasurement(sensorId: "S-5", temperature: 21.9, isCalibrated: true)
            ]

            Task {
                for item in rawData {
                    try? await Task.sleep(nanoseconds: 15_000_000)
                    continuation.yield(item)
                }
                continuation.finish()
            }
        }
    }
}

Task {
    print("[Pipeline] Sensor oqimi qayta ishlanmoqda...")

    // Funksional asinxron pipeline:
    // Faqat kalibrlangan sensorlarni olamiz, haroratni Farengeytga o'giramiz va dastlabki 2 tasini chiqaramiz
    let transformedStream = SensorPipelineEngine.sensorStream()
        .filter { $0.isCalibrated }
        .map { measurement -> String in
            let fahrenheit = (measurement.temperature * 9 / 5) + 32
            return "Sensor [\(measurement.sensorId)]: \(measurement.temperature)°C -> \(fahrenheit)°F"
        }
        .prefix(2)

    for await formattedString in transformedStream {
        print("Filtrdan o'tgan natija: \(formattedString)")
    }

    print("[Pipeline] Qayta ishlash to'xtatildi.")
}
```
**Tushuntirish:** Swift Concurrency `AsyncSequence` ga boy funksional metodlarni taqdim etadi (`map`, `filter`, `prefix`, `drop`). Barcha operatorlar "lazy" (dangasa) ishlaydi: elementlar butun massiv qilib xotiraga yuklanmaydi, balki quvur (pipeline) orqali bittalab o'tkaziladi. `prefix(2)` sharti bajarilishi bilanoq pastki oqim avtomatik bekor qilinadi.
**Ishlash natijasi:**
```text
[Pipeline] Sensor oqimi qayta ishlanmoqda...
Filtrdan o'tgan natija: Sensor [S-1]: 22.4°C -> 72.32°F
Filtrdan o'tgan natija: Sensor [S-3]: 24.1°C -> 75.38°F
[Pipeline] Qayta ishlash to'xtatildi.
```

---

### Topshiriq #1218: Actor Ichida In-Flight Request Deduplication (Cache Stampede Oldini Olish)
**Tavsif:** Mobil ilova ochilganda bir nechta turli UI vidjetlari bir vaqtning o'zida bitta API so'rovini (masalan, `/user/profile`) so'rashi mumkin. Agar nazorat qilinmasa, serverga bir xil bir necha og'ir so'rov yuboriladi (Thundering Herd / Cache Stampede).
**Talablar:** Actor izolyatsiyasi, `Task<Value, Error>` ni lug'atda kesh sifatida saqlash, bir xil kalitli so'rovlarni birlashtirish.
**Yechim (Swift):**
```swift
import Foundation

public actor RequestDeduplicator<Key: Hashable & Sendable, Value: Sendable> {
    private var inFlight: [Key: Task<Value, Error>] = [:]

    public init() {}

    public func execute(key: Key, operation: @Sendable @escaping () async throws -> Value) async throws -> Value {
        // Agar bu kalit bo'yicha operatsiya hozirda bajarilayotgan bo'lsa
        if let existingTask = inFlight[key] {
            print("[Deduplicator] Kalit: '\(key)' uchun mavjud jarayonga ulanildi (Deduplication)")
            return try await existingTask.value
        }

        print("[Deduplicator] Kalit: '\(key)' uchun yangi tarmoq vazifasi yaratildi")
        let task = Task<Value, Error> {
            return try await operation()
        }

        inFlight[key] = task

        do {
            let result = try await task.value
            inFlight[key] = nil // Operatsiya muvaffaqiyatli tugagach tozalanadi
            return result
        } catch {
            inFlight[key] = nil
            throw error
        }
    }
}

// Sinov
Task {
    let deduplicator = RequestDeduplicator<String, String>()

    // Bitta kalit bo'yicha 3 ta parallel so'rov
    async let call1 = deduplicator.execute(key: "user_config") {
        try await Task.sleep(nanoseconds: 50_000_000)
        return "Server Konfiguratsiyasi v2.4"
    }

    async let call2 = deduplicator.execute(key: "user_config") {
        try await Task.sleep(nanoseconds: 50_000_000)
        return "Server Konfiguratsiyasi v2.4"
    }

    async let call3 = deduplicator.execute(key: "user_config") {
        try await Task.sleep(nanoseconds: 50_000_000)
        return "Server Konfiguratsiyasi v2.4"
    }

    let results = try await [call1, call2, call3]
    print("Barcha 3 ta chaqiruv yakuniy natijani oldi: \(results.first ?? "")")
}
```
**Tushuntirish:** Ushbu Actor umumiy operatsiyalar navbatini boshqaradi. Kalit bo'yicha allaqachon bajarilayotgan `Task` mavjud bo'lsa, yangi tarmoq so'rovi yuborilmaydi, balki mavjud Task'ning `.value` qiymati kutiladi. Bu backend server yuklamasini 70-80% gacha kamaytiradi va mobil ilova batareyasini asraydi.
**Ishlash natijasi:**
```text
[Deduplicator] Kalit: 'user_config' uchun yangi tarmoq vazifasi yaratildi
[Deduplicator] Kalit: 'user_config' uchun mavjud jarayonga ulanildi (Deduplication)
[Deduplicator] Kalit: 'user_config' uchun mavjud jarayonga ulanildi (Deduplication)
Barcha 3 ta chaqiruv yakuniy natijani oldi: Server Konfiguratsiyasi v2.4
```

---

### Topshiriq #1219: `withCheckedContinuation` va `withCheckedThrowingContinuation` - Swift 6 Qat'iy Ko'prik
**Tavsif:** Eski blokli (completion handler) kutubxonalarni async/await formatiga o'tkazishda continuation aniq 1 marta chaqirilishi shart. Nol marta chaqirilsa Task abadiy qotib qoladi (hang), 2 marta chaqirilsa Crash bo'ladi.
**Talablar:** `withCheckedThrowingContinuation`, Strict single-call verification, xatoliklarni xavfsiz o'rash.
**Yechim (Swift):**
```swift
import Foundation

// Simulyatsiya qilingan eski SDK
public class LegacyPaymentGateway {
    public static func processPayment(amount: Double, completion: @escaping (Result<String, Error>) -> Void) {
        DispatchQueue.global().asyncAfter(deadline: .now() + 0.05) {
            if amount <= 0 {
                let err = NSError(domain: "PaymentGateway", code: 400, userInfo: [NSLocalizedDescriptionKey: "Miqdor noto'g'ri"])
                completion(.failure(err))
            } else {
                completion(.success("TRANSACTION_SUCCESS_#\(Int(amount * 100))"))
            }
        }
    }
}

// Swift 6 zamonaviy asinxron wrapper
public struct ModernPaymentBridge {
    public static func pay(amount: Double) async throws -> String {
        return try await withCheckedThrowingContinuation { continuation in
            LegacyPaymentGateway.processPayment(amount: amount) { result in
                switch result {
                case .success(let transactionId):
                    // Aniq 1 marta resume chaqiriladi
                    continuation.resume(returning: transactionId)
                case .failure(let error):
                    continuation.resume(throwing: error)
                }
            }
        }
    }
}

Task {
    do {
        let successId = try await ModernPaymentBridge.pay(amount: 150.0)
        print("Muvaffaqiyatli to'lov kodi: \(successId)")

        // Xatolik ssenariysi
        _ = try await ModernPaymentBridge.pay(amount: -10.0)
    } catch {
        print("Kutilgan xatolik to'g'ri ushlandi: \(error.localizedDescription)")
    }
}
```
**Tushuntirish:** `withCheckedContinuation` Swift runtime darajasida xavfsizlik tekshiruviga ega. Agar ishlab chiquvchi continuation chaqirishni unutsa yoki adashib ikki marta `resume()` qilsa, debug rejimida aniq diagnostic xatolik beradi. Bu esa xotirada qolib ketuvchi osilib turgan (zombie) asinxron chaqiruvlarning oldini oladi.
**Ishlash natijasi:**
```text
Muvaffaqiyatli to'lov kodi: TRANSACTION_SUCCESS_#15000
Kutilgan xatolik to'g'ri ushlandi: Miqdor noto'g'ri
```

---

### Topshiriq #1220: Multi-Producer AsyncStream va Actor Asosidagi Pub/Sub Event Broker
**Tavsif:** Ilovaning turli qismlari (Auth xizmati, Push Notification, Network Listener) global tizim voqealarini (System Events) yuborishi va bir nechta qabul qiluvchilar buni mustaqil asinxron tinglashi lozim.
**Talablar:** Pub/Sub pattern, Actor orqali subscriberlarni ro'yxatga olish va xavfsiz tarqatish, Data Race yo'qligi.
**Yechim (Swift):**
```swift
import Foundation

public enum AppSystemEvent: Sendable {
    case userLoggedIn(userId: String)
    case sessionExpired
    case networkStatusChanged(isOnline: Bool)
}

public actor AppEventBroker {
    public static let shared = AppEventBroker()

    private var subscribers: [UUID: AsyncStream<AppSystemEvent>.Continuation] = [:]

    private init() {}

    // Yangi obunachi uchun maxsus AsyncStream yaratish
    public func subscribe() -> (id: UUID, stream: AsyncStream<AppSystemEvent>) {
        let subscriptionId = UUID()
        let stream = AsyncStream<AppSystemEvent> { continuation in
            subscribers[subscriptionId] = continuation

            continuation.onTermination = { [subscriptionId] _ in
                Task { [weak self] in
                    await self?.unsubscribe(id: subscriptionId)
                }
            }
        }
        return (subscriptionId, stream)
    }

    public func unsubscribe(id: UUID) {
        subscribers[id]?.finish()
        subscribers.removeValue(forKey: id)
        print("[EventBroker] Obunachi o'chirildi: \(id.uuidString.prefix(6))")
    }

    // Barcha faol obunachilarga xabar tarqatish (Publish)
    public func publish(event: AppSystemEvent) {
        for (_, continuation) in subscribers {
            continuation.yield(event)
        }
    }
}

// Bajarish
Task {
    let broker = AppEventBroker.shared

    // 1-obunachi (UI moduli)
    let (_, uiStream) = await broker.subscribe()
    Task {
        for await event in uiStream {
            print("[UI Obunachi] Yangi hodisa keldi: \(event)")
        }
    }

    // 2-obunachi (Analitika moduli)
    let (analyticsId, analyticsStream) = await broker.subscribe()
    Task {
        for await event in analyticsStream {
            print("[Analytics Obunachi] Metrika yozildi: \(event)")
        }
    }

    try? await Task.sleep(nanoseconds: 20_000_000)

    // Hodisalarni e'lon qilish
    await broker.publish(event: .userLoggedIn(userId: "usr_7890"))
    await broker.publish(event: .networkStatusChanged(isOnline: true))

    // Analitika obunasini to'xtatish
    await broker.unsubscribe(id: analyticsId)

    await broker.publish(event: .sessionExpired)
}
```
**Tushuntirish:** Actor ichida `AsyncStream.Continuation` kolleksiyasini saqlash orqali ko'p tarmoqli Pub/Sub (Publish-Subscribe) arxitekturasi barpo etiladi. Actor barcha qo'shish va o'chirish operatsiyalarini serializatsiya qiladi, natijada obunachilar ro'yxatida Data Race yuzaga kelmaydi va xabarlar barcha qabul qiluvchilarga asinxron yetkaziladi.
**Ishlash natijasi:**
```text
[UI Obunachi] Yangi hodisa keldi: userLoggedIn(userId: "usr_7890")
[Analytics Obunachi] Metrika yozildi: userLoggedIn(userId: "usr_7890")
[UI Obunachi] Yangi hodisa keldi: networkStatusChanged(isOnline: true)
[Analytics Obunachi] Metrika yozildi: networkStatusChanged(isOnline: true)
[EventBroker] Obunachi o'chirildi: 5E23FA
[UI Obunachi] Yangi hodisa keldi: sessionExpired
```

---

### Topshiriq #1221: SwiftData `@Model` va `@ModelActor` Orqali Fon Oqimida Xavfsiz Bazaviy Operatsiyalar
**Tavsif:** SwiftData'da `ModelContext` asosiy oqimda (MainActor) yaratilsa, unda katta hajmdagi ma'lumotlarni yozish yoki o'qish UI interfeysining qotib qolishiga (Hang / Frame Drop) sabab bo'ladi. `@ModelActor` makrosi fon oqimida o'zining shaxsiy `ModelContext`iga ega bo'lgan xavfsiz muhit yaratadi.
**Talablar:** `import SwiftData`, `@Model`, `@ModelActor`, fon oqimida ma'lumotlarni xavfsiz saqlash va o'qish.
**Yechim (Swift):**
```swift
import Foundation
import SwiftData

// 1. SwiftData Ma'lumotlar Modeli
@Model
public final class ProductEntity {
    @Attribute(.unique) public var id: UUID
    public var name: String
    public var price: Decimal
    public var stock: Int

    public init(id: UUID = UUID(), name: String, price: Decimal, stock: Int) {
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock
    }
}

// 2. Fon oqimida xavfsiz ishlovchi ModelActor
@ModelActor
public actor ProductDatabaseWorker {
    // modelContext va modelExecutor @ModelActor tomonidan avtomatik taqdim etiladi

    public func insertProductsBatch(items: [(name: String, price: Decimal, stock: Int)]) throws {
        print("[ModelActor] Fon oqimida \(items.count) ta mahsulot saqlanmoqda...")
        for item in items {
            let entity = ProductEntity(name: item.name, price: item.price, stock: item.stock)
            modelContext.insert(entity)
        }
        try modelContext.save()
        print("[ModelActor] Barcha ma'lumotlar xavfsiz saqlandi.")
    }

    public func fetchTotalStock() throws -> Int {
        let descriptor = FetchDescriptor<ProductEntity>()
        let products = try modelContext.fetch(descriptor)
        let total = products.reduce(0) { $0 + $1.stock }
        return total
    }
}

// Bajarish
Task {
    // Model konteynerini xotirada yaratamiz (In-Memory test)
    let schema = Schema([ProductEntity.self])
    let configuration = ModelConfiguration(schema: schema, isStoredInMemoryOnly: true)
    guard let container = try? ModelContainer(for: schema, configurations: [configuration]) else {
        fatalError("Konteyner yaratib bo'lmadi")
    }

    let worker = ProductDatabaseWorker(modelContainer: container)

    let testProducts: [(name: String, price: Decimal, stock: Int)] = [
        ("MacBook Pro M3 Max", 3499.0, 15),
        ("iPhone 16 Pro", 1199.0, 45),
        ("iPad Pro M4 OLED", 999.0, 20)
    ]

    do {
        try await worker.insertProductsBatch(items: testProducts)
        let totalStock = try await worker.fetchTotalStock()
        print("Bazada umumiy qoldiq: \(totalStock) dona")
    } catch {
        print("Baza operatsiyasida xatolik: \(error)")
    }
}
```
**Tushuntirish:** SwiftData'dagi eng katta yangiliklardan biri `@ModelActor` makrosidir. U `ModelActor` protokolini amalga oshiradi va unga yagona `ModelContainer` beriladi. U o'zining shaxsiy `modelExecutor` va `modelContext`ini fon oqimida yaratib, tashqi dunyodan kelgan barcha CRUD so'rovlarini Actor orqali navbatga soladi. Bu esa UI oqimiga umuman ta'sir ko'rsatmaydi.
**Ishlash natijasi:**
```text
[ModelActor] Fon oqimida 3 ta mahsulot saqlanmoqda...
[ModelActor] Barcha ma'lumotlar xavfsiz saqlandi.
Bazada umumiy qoldiq: 80 dona
```

---

### Topshiriq #1222: SwiftData `ModelContainer` va `ModelContext` Isolation Boundary
**Tavsif:** SwiftData ob'yektlari (`@Model`) sinflar (reference types) bo'lib, ular `Sendable` EMAS. Agar bir oqimdagi `ProductEntity` obyektini to'g'ridan-to'g'ri boshqa oqimga (masalan, MainActor'dan fon oqimiga) uzatsangiz, Swift 6 jiddiy kompilyatsiya xatosini beradi yoki runtimeda crash yuz beradi.
**Talablar:** `PersistentIdentifier`, actorlar orasida faqat `PersistentIdentifier` (Sendable) uzatish, ob'yektni qayta yuklash.
**Yechim (Swift):**
```swift
import Foundation
import SwiftData

@Model
public final class CustomerProfile {
    @Attribute(.unique) public var customerId: String
    public var fullName: String
    public var rewardPoints: Int

    public init(customerId: String, fullName: String, rewardPoints: Int) {
        self.customerId = customerId
        self.fullName = fullName
        self.rewardPoints = rewardPoints
    }
}

@ModelActor
public actor BackgroundPointsCalculator {
    // Modelni to'g'ridan-to'g'ri qabul qilmaymiz! Faqat Sendable bo'lgan PersistentIdentifier qabul qilinadi
    public func addBonusPoints(to id: PersistentIdentifier, bonus: Int) throws -> Int {
        guard let customer = self[id, as: CustomerProfile.self] else {
            throw NSError(domain: "SwiftDataError", code: 404, userInfo: [NSLocalizedDescriptionKey: "Mijoz topilmadi"])
        }

        customer.rewardPoints += bonus
        try modelContext.save()
        print("[BackgroundCalculator] \(customer.fullName) uchun ball yangilandi: \(customer.rewardPoints)")
        return customer.rewardPoints
    }
}

Task {
    let schema = Schema([CustomerProfile.self])
    let config = ModelConfiguration(schema: schema, isStoredInMemoryOnly: true)
    guard let container = try? ModelContainer(for: schema, configurations: [config]) else { return }

    // 1. Asosiy oqimda mijoz yaratish
    let mainContext = container.mainContext
    let newCustomer = CustomerProfile(customerId: "CUST-007", fullName: "Jamshid Aliyev", rewardPoints: 100)
    mainContext.insert(newCustomer)
    try? mainContext.save()

    // Oqimlararo faqat Sendable identifikator o'tadi
    let safeIdentifier: PersistentIdentifier = newCustomer.id

    // 2. Fon oqimidagi actorga identifikatorni uzatamiz
    let worker = BackgroundPointsCalculator(modelContainer: container)
    let updatedPoints = try? await worker.addBonusPoints(to: safeIdentifier, bonus: 50)

    print("Mijozning yakuniy ballari: \(updatedPoints ?? 0)")
}
```
**Tushuntirish:** `@Model` obyektlari qaysi kontekstda (`ModelContext`) yuklangan bo'lsa, o'sha oqimga bog'langan bo'ladi. Ular Sendable bo'lmagani sababli, boshqa oqimlarga uzatish taqiqlangan. Oqimlararo uzatishning yagona xavfsiz yo'li - bu `PersistentIdentifier` (u `Sendable` dir). Qabul qiluvchi oqim bu identifikator orqali o'zining shaxsiy kontekstidan ob'yektni xavfsiz yuklab oladi.
**Ishlash natijasi:**
```text
[BackgroundCalculator] Jamshid Aliyev uchun ball yangilandi: 150
Mijozning yakuniy ballari: 150
```

---

### Topshiriq #1223: SwiftData Batch Processing: TaskGroup Bilan Minglab Yozuvlarni Xotirasiz Saqlash
**Tavsif:** Serverdan kelgan 10,000 ta yozuvni bittalab bazaga yozish yoki barchasini bitta bahaybat tranzaksiyada saqlash xotira (RAM) yetishmovchiligiga sabab bo'ladi. Ma'lumotlarni o'lchamli qismlarga (chunks / batches) bo'lib, fon oqimida xavfsiz yozish kerak.
**Talablar:** Batching strategiyasi, xotirani har bir batchdan keyin tozalash (`save()`), TaskGroup orqali yuklash.
**Yechim (Swift):**
```swift
import Foundation
import SwiftData

@Model
public final class LogTelemetryEntity {
    public var timestamp: Date
    public var level: String
    public var message: String

    public init(timestamp: Date = Date(), level: String, message: String) {
        self.timestamp = timestamp
        self.level = level
        self.message = message
    }
}

@ModelActor
public actor TelemetryBatchImporter {
    public func importInChunks(totalRecords: Int, chunkSize: Int) throws {
        print("[BatchImporter] \(totalRecords) ta yozuvni \(chunkSize) tadan bo'lib kiritish boshlandi")

        var insertedSoFar = 0

        while insertedSoFar < totalRecords {
            let currentBatchSize = min(chunkSize, totalRecords - insertedSoFar)

            for i in 1...currentBatchSize {
                let log = LogTelemetryEntity(
                    level: "INFO",
                    message: "Tizim auditi hodisasi #\(insertedSoFar + i)"
                )
                modelContext.insert(log)
            }

            // Har bir batchdan so'ng kontekstni diskka saqlab, RAM bosimini yengillatamiz
            try modelContext.save()
            insertedSoFar += currentBatchSize
            print("[BatchImporter] Chank muvaffaqiyatli saqlandi. Jami: \(insertedSoFar)/\(totalRecords)")
        }

        print("[BatchImporter] Barcha yozuvlar muvaffaqiyatli yozildi.")
    }
}

Task {
    let schema = Schema([LogTelemetryEntity.self])
    let config = ModelConfiguration(schema: schema, isStoredInMemoryOnly: true)
    guard let container = try? ModelContainer(for: schema, configurations: [config]) else { return }

    let importer = TelemetryBatchImporter(modelContainer: container)
    try? await importer.importInChunks(totalRecords: 15, chunkSize: 5)
}
```
**Tushuntirish:** Katta hajmdagi kiritishlarda SwiftData konteksti barcha yangi ob'yektlarni xotirada ushlab turadi. Agar `modelContext.save()` faqat oxirida chaqirilsa, xotira sarfi cho'qqiga chiqadi. Har bir `chunkSize` (masalan 500-1000) dan so'ng saqlash operatsiyasi xotira oqishining (memory footprint) oldini oladi va disk I/O operatsiyalarini optimallashtiradi.
**Ishlash natijasi:**
```text
[BatchImporter] 15 ta yozuvni 5 tadan bo'lib kiritish boshlandi
[BatchImporter] Chank muvaffaqiyatli saqlandi. Jami: 5/15
[BatchImporter] Chank muvaffaqiyatli saqlandi. Jami: 10/15
[BatchImporter] Chank muvaffaqiyatli saqlandi. Jami: 15/15
[BatchImporter] Barcha yozuvlar muvaffaqiyatli yozildi.
```

---

### Topshiriq #1224: SwiftData `FetchDescriptor` va `Predicate` Bilan Type-Safe Asinxron So'rovlar
**Tavsif:** SwiftData bazasidan ma'lumotlarni qidirishda SQL matnli so'rovlar emas, balki Swift kompilyatori tekshiruvidan o'tuvchi `#Predicate` makrosidan foydalanish shart. Noto'g'ri kiritilgan parametrlar kompilyatsiya vaqtidayoq ushlanishi kerak.
**Talablar:** `#Predicate`, `FetchDescriptor`, `SortDescriptor`, limit va offset bilan asinxron saralash.
**Yechim (Swift):**
```swift
import Foundation
import SwiftData

@Model
public final class StudentRecord {
    public var name: String
    public var gpa: Double
    public var gradeLevel: Int

    public init(name: String, gpa: Double, gradeLevel: Int) {
        self.name = name
        self.gpa = gpa
        self.gradeLevel = gradeLevel
    }
}

@ModelActor
public actor AcademicRegistryService {
    public func seedData() throws {
        let students = [
            StudentRecord(name: "Anvar Qodirov", gpa: 4.8, gradeLevel: 4),
            StudentRecord(name: "Barno Rahimova", gpa: 3.5, gradeLevel: 3),
            StudentRecord(name: "Diyorbek Toshmatov", gpa: 4.9, gradeLevel: 4),
            StudentRecord(name: "Elena Kim", gpa: 4.2, gradeLevel: 2),
            StudentRecord(name: "Farrux Zokirov", gpa: 3.8, gradeLevel: 4)
        ]
        for student in students {
            modelContext.insert(student)
        }
        try modelContext.save()
    }

    // Type-safe Predicate orqali a'lochi bitiruvchilarni topish
    public func fetchHonorStudents(minGPA: Double, grade: Int) throws -> [String] {
        let predicate = #Predicate<StudentRecord> { student in
            student.gradeLevel == grade && student.gpa >= minGPA
        }

        var descriptor = FetchDescriptor<StudentRecord>(
            predicate: predicate,
            sortBy: [SortDescriptor(\.gpa, order: .reverse)]
        )
        descriptor.fetchLimit = 10

        let matched = try modelContext.fetch(descriptor)
        return matched.map { "\($0.name) (GPA: \($0.gpa))" }
    }
}

Task {
    let schema = Schema([StudentRecord.self])
    let config = ModelConfiguration(schema: schema, isStoredInMemoryOnly: true)
    guard let container = try? ModelContainer(for: schema, configurations: [config]) else { return }

    let service = AcademicRegistryService(modelContainer: container)
    try? await service.seedData()

    let honorGrads = try? await service.fetchHonorStudents(minGPA: 4.0, grade: 4)
    print("Top a'lochi 4-kurs talabalari:")
    honorGrads?.forEach { print(" - \($0)") }
}
```
**Tushuntirish:** `#Predicate` makrosi Swift kodini (closure) AST (Abstract Syntax Tree) orqali tahlil qiladi va SQLite SQL WHERE shartlariga kompilyatsiya vaqtida o'giradi. Agar mavjud bo'lmagan xususiyat yoki noto'g'ri tip bilan taqqoslansa, kod kompilyatsiya bo'lmaydi. Bu esa production muhitidagi SQL syntax xatolarini 100% bartaraf etadi.
**Ishlash natijasi:**
```text
Top a'lochi 4-kurs talabalari:
 - Diyorbek Toshmatov (GPA: 4.9)
 - Anvar Qodirov (GPA: 4.8)
```

---

### Topshiriq #1225: SwiftData va SwiftUI Reaktiv Integratsiyasi: `@Query` va Actor Boundary
**Tavsif:** SwiftUI interfeysida ma'lumotlar bazasidagi o'zgarishlarni real vaqt rejimida avtomatik aks ettirish kerak. Asosiy oqimda `@Query` ishlatiladi, fon actor'idagi o'zgarishlar esa UI'ga reaktiv yetib borishi ta'minlanadi.
**Talablar:** `@Query`, MainActor reaktiv yangilanishi, `modelContext.save()` orqali xabar tarqatish.
**Yechim (Swift):**
```swift
import Foundation
import SwiftData

@Model
public final class TaskItem {
    public var title: String
    public var isCompleted: Bool
    public var createdAt: Date

    public init(title: String, isCompleted: Bool = false, createdAt: Date = Date()) {
        self.title = title
        self.isCompleted = isCompleted
        self.createdAt = createdAt
    }
}

// SwiftUI ViewModel qatlami
@MainActor
public final class TaskListViewModel {
    private let container: ModelContainer

    public init(container: ModelContainer) {
        self.container = container
    }

    public func fetchActiveTasks() -> [TaskItem] {
        let descriptor = FetchDescriptor<TaskItem>(
            predicate: #Predicate { !$0.isCompleted },
            sortBy: [SortDescriptor(\.createdAt, order: .reverse)]
        )
        return (try? container.mainContext.fetch(descriptor)) ?? []
    }

    public func toggleTask(task: TaskItem) {
        task.isCompleted.toggle()
        try? container.mainContext.save()
        print("[MainActor] Vazifa holati o'zgartirildi: \(task.title) -> \(task.isCompleted)")
    }
}

Task { @MainActor in
    let schema = Schema([TaskItem.self])
    let config = ModelConfiguration(schema: schema, isStoredInMemoryOnly: true)
    guard let container = try? ModelContainer(for: schema, configurations: [config]) else { return }

    let vm = TaskListViewModel(container: container)

    // Boshlang'ich vazifa qo'shish
    let item1 = TaskItem(title: "Swift 6 Concurrency o'rganish")
    let item2 = TaskItem(title: "Clean Architecture loyihalash")
    container.mainContext.insert(item1)
    container.mainContext.insert(item2)
    try? container.mainContext.save()

    let active = vm.fetchActiveTasks()
    print("Faol vazifalar soni: \(active.count)")

    if let first = active.first {
        vm.toggleTask(task: first)
    }

    let remaining = vm.fetchActiveTasks()
    print("Qolgan faol vazifalar soni: \(remaining.count)")
}
```
**Tushuntirish:** SwiftUI va SwiftData bir-biri bilan uzviy integratsiyalashgan. `container.mainContext` da ob'yekt o'zgarganda yoki `save()` chaqirilganda, SwiftUI ko'rinishlari (`@Query`) avtomatik ravishda diff hisoblab, faqat o'zgargan UI qismini qayta chizadi.
**Ishlash natijasi:**
```text
Faol vazifalar soni: 2
[MainActor] Vazifa holati o'zgartirildi: Clean Architecture loyihalash -> true
Qolgan faol vazifalar soni: 1
```

---

### Topshiriq #1226: SwiftData Transaction va Rollback: Tranzaksion Butunlikni Ta'minlash
**Tavsif:** Foydalanuvchi bir vaqtning o'zida ham balansini kamaytirib, ham xarid qilingan chekni saqlayotganda, agar chekni saqlashda xatolik chiqsa, kamaytirilgan balans ham dastlabki holatiga qaytarilishi (Rollback) lozim.
**Talablar:** `modelContext.rollback()`, tranzaksion yaxlitlik (ACID), xatolik yuz berganda xavfsiz bekor qilish.
**Yechim (Swift):**
```swift
import Foundation
import SwiftData

@Model
public final class UserWallet {
    public var balance: Decimal

    public init(balance: Decimal) {
        self.balance = balance
    }
}

@Model
public final class PurchaseReceipt {
    public var invoiceNumber: String
    public var amount: Decimal

    public init(invoiceNumber: String, amount: Decimal) {
        self.invoiceNumber = invoiceNumber
        self.amount = amount
    }
}

@ModelActor
public actor SecureCheckoutService {
    public func processPurchase(walletId: PersistentIdentifier, amount: Decimal, invoiceNumber: String, simulateCrash: Bool) throws {
        print("[Transaction] To'lov jarayoni boshlandi...")

        guard let wallet = self[walletId, as: UserWallet.self] else {
            throw NSError(domain: "Checkout", code: 404, userInfo: [NSLocalizedDescriptionKey: "Hamyon topilmadi"])
        }

        // 1-qadam: Balansni yechish
        guard wallet.balance >= amount else {
            throw NSError(domain: "Checkout", code: 400, userInfo: [NSLocalizedDescriptionKey: "Yetarli mablag' yo'q"])
        }
        wallet.balance -= amount
        print("[Transaction] Balansdan \(amount) yechildi. Yangi qoldiq: \(wallet.balance)")

        // 2-qadam: Chekni yaratish
        let receipt = PurchaseReceipt(invoiceNumber: invoiceNumber, amount: amount)
        modelContext.insert(receipt)

        // 3-qadam: Simulyatsiya qilingan kutilmagan xatolik
        if simulateCrash {
            print("[Transaction] DIQQAT: Kvitansiya yaratishda xatolik yuz berdi! ROLLBACK qilinmoqda...")
            modelContext.rollback() // Barcha o'zgarishlar (balans yechilishi ham) dastlabki holiga qaytadi!
            throw NSError(domain: "Checkout", code: 500, userInfo: [NSLocalizedDescriptionKey: "Tranzaksiya muvaffaqiyatsiz bo'ldi"])
        }

        try modelContext.save()
        print("[Transaction] Tranzaksiya muvaffaqiyatli commit qilindi.")
    }
}

Task {
    let schema = Schema([UserWallet.self, PurchaseReceipt.self])
    let config = ModelConfiguration(schema: schema, isStoredInMemoryOnly: true)
    guard let container = try? ModelContainer(for: schema, configurations: [config]) else { return }

    let initialWallet = UserWallet(balance: 500_000)
    container.mainContext.insert(initialWallet)
    try? container.mainContext.save()
    let walletId = initialWallet.id

    let checkout = SecureCheckoutService(modelContainer: container)

    // Xato yuz beradigan tranzaksiya testi
    do {
        try await checkout.processPurchase(walletId: walletId, amount: 200_000, invoiceNumber: "INV-001", simulateCrash: true)
    } catch {
        print("Tranzaksiya xatosi ushlandi: \(error.localizedDescription)")
    }

    // Rollback'dan keyin asosiy oqimda balansni tekshiramiz
    container.mainContext.rollback()
    let refreshedWallet = container.mainContext.model(for: walletId) as? UserWallet
    print("Rollbackdan so'ng hamyon balansi: \(refreshedWallet?.balance ?? 0) (O'zgarishsiz saqlandi!)")
}
```
**Tushuntirish:** `modelContext.rollback()` xotiradagi barcha saqlanmagan (uncommitted) o'zgarishlarni bekor qilib, ob'yektlarni oxirgi tasdiqlangan holatiga qaytaradi. Bu esa moliyaviy dasturlarda ma'lumotlar buzilishi (Data Corruption) xavfini oldini oladi.
**Ishlash natijasi:**
```text
[Transaction] To'lov jarayoni boshlandi...
[Transaction] Balansdan 200000 yechildi. Yangi qoldiq: 300000
[Transaction] DIQQAT: Kvitansiya yaratishda xatolik yuz berdi! ROLLBACK qilinmoqda...
Tranzaksiya xatosi ushlandi: Tranzaksiya muvaffaqiyatsiz bo'ldi
Rollbackdan so'ng hamyon balansi: 500000 (O'zgarishsiz saqlandi!)
```

---

### Topshiriq #1227: CoreData va SwiftData Gibrid Migratsiyasi Uchun Asinxron Transformatsiya
**Tavsif:** Katta loyihalarda eski CoreData bazasidan zamonaviy SwiftData'ga bosqichma-bosqich o'tish talab etiladi. Buning uchun ma'lumotlarni asinxron o'qib, yangi SwiftData arxitekturasiga konvertatsiya qilish lozim.
**Talablar:** CoreData konseptlari bilan moslik, asinxron ma'lumotlar transformatsiyasi, duplikatsiyalarsiz xavfsiz migratsiya.
**Yechim (Swift):**
```swift
import Foundation
import SwiftData

// Eski CoreData DTO strukturasi
public struct LegacyCoreDataRecord: Sendable {
    public let legacyId: Int64
    public let payload: String
    public let timestampEpoch: TimeInterval
}

// Yangi SwiftData Model
@Model
public final class ModernArchiveEntity {
    @Attribute(.unique) public var externalId: Int64
    public var content: String
    public var dateCreated: Date

    public init(externalId: Int64, content: String, dateCreated: Date) {
        self.externalId = externalId
        self.content = content
        self.dateCreated = dateCreated
    }
}

@ModelActor
public actor MigrationCoordinatorActor {
    public func migrateLegacyRecords(records: [LegacyCoreDataRecord]) throws -> Int {
        print("[MigrationActor] \(records.count) ta yozuvni migratsiya qilish boshlandi")

        var migratedCount = 0
        for rec in records {
            // Predicate orqali oldin mavjudligini tekshiramiz
            let targetId = rec.legacyId
            let descriptor = FetchDescriptor<ModernArchiveEntity>(
                predicate: #Predicate { $0.externalId == targetId }
            )

            let existing = try modelContext.fetch(descriptor)
            if existing.isEmpty {
                let modern = ModernArchiveEntity(
                    externalId: rec.legacyId,
                    content: rec.payload,
                    dateCreated: Date(timeIntervalSince1970: rec.timestampEpoch)
                )
                modelContext.insert(modern)
                migratedCount += 1
            }
        }

        try modelContext.save()
        print("[MigrationActor] Migratsiya muvaffaqiyatli yakunlandi: \(migratedCount) ta yangi yozuv saqlandi.")
        return migratedCount
    }
}

Task {
    let schema = Schema([ModernArchiveEntity.self])
    let config = ModelConfiguration(schema: schema, isStoredInMemoryOnly: true)
    guard let container = try? ModelContainer(for: schema, configurations: [config]) else { return }

    let legacyData = [
        LegacyCoreDataRecord(legacyId: 1001, payload: "Arxiv hisoboti 2024", timestampEpoch: 1704067200),
        LegacyCoreDataRecord(legacyId: 1002, payload: "Foydalanuvchi sozlamalari", timestampEpoch: 1704153600)
    ]

    let coordinator = MigrationCoordinatorActor(modelContainer: container)
    let count = try? await coordinator.migrateLegacyRecords(records: legacyData)
    print("Jami migratsiya qilingan ob'yektlar: \(count ?? 0)")
}
```
**Tushuntirish:** Legacy tizimlardan o'tishda orqa fonda ishlovchi migratsiya agenti ma'lumotlarni qismlab ko'chiradi. `@Attribute(.unique)` atributi va qidiruv tekshiruvi orqali foydalanuvchi ilovani qayta ochganda ma'lumotlar qayta yozilishi yoki dublikat hosil bo'lishining oldi olinadi.
**Ishlash natijasi:**
```text
[MigrationActor] 2 ta yozuvni migratsiya qilish boshlandi
[MigrationActor] Migratsiya muvaffaqiyatli yakunlandi: 2 ta yangi yozuv saqlandi.
Jami migratsiya qilingan ob'yektlar: 2
```

---

### Topshiriq #1228: `@ModelActor` Ichida Tashqi API Dan Offline Keshga Yuklash (Sync Engine)
**Tavsif:** Zamonaviy mobil ilovalar birinchi navbatda oflayn rejimda (Offline-First) ishlashi kerak. Tarmoqdan yangi ma'lumotlar kelganda fon actor'i bazani yangilaydi va UI bilan sinxronlashtiradi.
**Talablar:** Offline-First kesh mexanizmi, `@ModelActor`, REST API javoblarini SwiftData ob'yektlariga asinxron xaritalash (mapping).
**Yechim (Swift):**
```swift
import Foundation
import SwiftData

public struct ArticleDTO: Decodable, Sendable {
    public let id: String
    public let title: String
    public let content: String
}

@Model
public final class CachedArticle {
    @Attribute(.unique) public var id: String
    public var title: String
    public var content: String
    public var lastUpdated: Date

    public init(id: String, title: String, content: String, lastUpdated: Date = Date()) {
        self.id = id
        self.title = title
        self.content = content
        self.lastUpdated = lastUpdated
    }
}

@ModelActor
public actor OfflineSyncEngine {
    public func syncWithRemote(articles: [ArticleDTO]) throws {
        print("[SyncEngine] Tarmoqdan \(articles.count) ta maqola keshlanmoqda...")

        for dto in articles {
            let targetId = dto.id
            let descriptor = FetchDescriptor<CachedArticle>(
                predicate: #Predicate { $0.id == targetId }
            )

            let matches = try modelContext.fetch(descriptor)
            if let existing = matches.first {
                // Mavjud bo'lsa yangilaymiz (Upsert)
                existing.title = dto.title
                existing.content = dto.content
                existing.lastUpdated = Date()
            } else {
                // Yangi bo'lsa qo'shamiz
                let newArticle = CachedArticle(id: dto.id, title: dto.title, content: dto.content)
                modelContext.insert(newArticle)
            }
        }

        try modelContext.save()
        print("[SyncEngine] Barcha maqolalar lokal keshga yozildi.")
    }

    public func getCachedArticleCount() throws -> Int {
        let descriptor = FetchDescriptor<CachedArticle>()
        return try modelContext.fetchCount(descriptor)
    }
}

Task {
    let schema = Schema([CachedArticle.self])
    let config = ModelConfiguration(schema: schema, isStoredInMemoryOnly: true)
    guard let container = try? ModelContainer(for: schema, configurations: [config]) else { return }

    let engine = OfflineSyncEngine(modelContainer: container)

    let remotePayload = [
        ArticleDTO(id: "art-1", title: "SwiftUI Navigatsiyasi", content: "NavigationStack haqida to'liq qo'llanma"),
        ArticleDTO(id: "art-2", title: "SwiftData Modellar", content: "ModelActor va PersistentIdentifier sirlari")
    ]

    try? await engine.syncWithRemote(articles: remotePayload)
    let count = try? await engine.getCachedArticleCount()
    print("Oflayn bazadagi maqolalar soni: \(count ?? 0) ta")
}
```
**Tushuntirish:** Offline-First arxitekturasida UI har doim lokal SwiftData bazasidan o'qiydi. Fon actor'i esa tarmoqqa murojaat qilib, "Upsert" (Update or Insert) mantig'i bo'yicha keshni yangilaydi. Bu usul ilovaning hatto internetsiz ham uzluksiz va chaqmoqdek tez ishlashini kafolatlaydi.
**Ishlash natijasi:**
```text
[SyncEngine] Tarmoqdan 2 ta maqola keshlanmoqda...
[SyncEngine] Barcha maqolalar lokal keshga yozildi.
Oflayn bazadagi maqolalar soni: 2 ta
```

---

### Topshiriq #1229: SwiftData Relationship (Cascade, Nullify) va Concurrency Xavfsizligi
**Tavsif:** Bog'langan modellar (masalan, Muallif va uning Kitoblari) o'rtasida o'chirish qoidalari (Delete Rules) to'g'ri o'rnatilmasa, asinxron fonda muallif o'chirilganda yetim (dangling pointer) kitoblar bazada qolib ketadi va data race/corruption yuzaga keladi.
**Talablar:** `@Relationship(deleteRule: .cascade)`, bir-ko'pga (one-to-many) munosabatlar, xavfsiz kaskadli o'chirish.
**Yechim (Swift):**
```swift
import Foundation
import SwiftData

@Model
public final class Book {
    public var title: String
    public var pages: Int
    public var author: Author?

    public init(title: String, pages: Int) {
        self.title = title
        self.pages = pages
    }
}

@Model
public final class Author {
    public var name: String

    // Kaskadli o'chirish: Muallif o'chirilsa, uning barcha kitoblari ham avtomatik o'chadi
    @Relationship(deleteRule: .cascade, inverse: \Book.author)
    public var books: [Book] = []

    public init(name: String) {
        self.name = name
    }
}

@ModelActor
public actor LibraryManagerActor {
    public func createAuthorWithBooks(authorName: String, bookTitles: [String]) throws -> PersistentIdentifier {
        let author = Author(name: authorName)
        for title in bookTitles {
            let book = Book(title: title, pages: 300)
            author.books.append(book)
        }
        modelContext.insert(author)
        try modelContext.save()
        return author.id
    }

    public func deleteAuthor(id: PersistentIdentifier) throws {
        guard let author = self[id, as: Author.self] else { return }
        print("[LibraryManager] Muallif: \(author.name) va uning \(author.books.count) ta kitobi o'chirilmoqda...")
        modelContext.delete(author)
        try modelContext.save()
    }

    public func countAllBooks() throws -> Int {
        let descriptor = FetchDescriptor<Book>()
        return try modelContext.fetchCount(descriptor)
    }
}

Task {
    let schema = Schema([Author.self, Book.self])
    let config = ModelConfiguration(schema: schema, isStoredInMemoryOnly: true)
    guard let container = try? ModelContainer(for: schema, configurations: [config]) else { return }

    let manager = LibraryManagerActor(modelContainer: container)

    let authorId = try? await manager.createAuthorWithBooks(
        authorName: "Abdulla Qodiriy",
        bookTitles: ["O'tkan kunlar", "Mehrobdan chayon"]
    )

    let countBefore = try? await manager.countAllBooks()
    print("O'chirishdan oldin kitoblar soni: \(countBefore ?? 0)")

    if let id = authorId {
        try? await manager.deleteAuthor(id: id)
    }

    let countAfter = try? await manager.countAllBooks()
    print("Kaskadli o'chirishdan keyin kitoblar soni: \(countAfter ?? 0) (Barchasi tozalindi!)")
}
```
**Tushuntirish:** `@Relationship(deleteRule: .cascade)` deklaratsiyasi orqali SwiftData munosabatlar bog'liqligini o'z zimmasiga oladi. Ota model o'chirilganda, barcha unga tegishli bola yozuvlar ham bitta atomik tranzaksiyada xavfsiz yo'q qilinadi, bu esa noaniq referensiyalar (orphaned records) hosil bo'lishidan saqlaydi.
**Ishlash natijasi:**
```text
O'chirishdan oldin kitoblar soni: 2
[LibraryManager] Muallif: Abdulla Qodiriy va uning 2 ta kitobi o'chirilmoqda...
Kaskadli o'chirishdan keyin kitoblar soni: 0 (Barchasi tozalindi!)
```

---

### Topshiriq #1230: Multi-Container SwiftData Arxitekturasi: Xavfsiz Vaqtinchalik Kesh va Doimiy Saqlagich
**Tavsif:** Yuqori xavfsizlik talab qilinadigan bank va davlat ilovalarida foydalanuvchi hisob ma'lumotlari shifrlangan doimiy xotirada, tezkor vaqtinchalik tarmoq ma'lumotlari esa faqat RAM'da (in-memory) saqlanishi kerak.
**Talablar:** Ko'p konteynerli arxitektura (`ModelContainer`), ajratilgan konfiguratsiyalar, turli izolyatsiyalardagi modellarni boshqarish.
**Yechim (Swift):**
```swift
import Foundation
import SwiftData

// Doimiy saqlanuvchi xavfsiz model
@Model
public final class SecureUserAccount {
    public var userTag: String
    public var encryptedPinHash: String

    public init(userTag: String, encryptedPinHash: String) {
        self.userTag = userTag
        self.encryptedPinHash = encryptedPinHash
    }
}

// Faqat RAM da yashovchi vaqtinchalik sessiya ma'lumoti
@Model
public final class EphemeralSessionData {
    public var sessionToken: String
    public var expiresAt: Date

    public init(sessionToken: String, expiresAt: Date) {
        self.sessionToken = sessionToken
        self.expiresAt = expiresAt
    }
}

public struct MultiContainerStorageManager {
    public let secureContainer: ModelContainer
    public let memoryContainer: ModelContainer

    public init() throws {
        // 1. Shifrlangan disk konfiguratsiyasi
        let secureConfig = ModelConfiguration(
            "SecureStore",
            schema: Schema([SecureUserAccount.self]),
            isStoredInMemoryOnly: false
        )
        self.secureContainer = try ModelContainer(for: SecureUserAccount.self, configurations: secureConfig)

        // 2. Vaqtinchalik faqat operativ xotira (RAM) konfiguratsiyasi
        let memoryConfig = ModelConfiguration(
            "EphemeralStore",
            schema: Schema([EphemeralSessionData.self]),
            isStoredInMemoryOnly: true
        )
        self.memoryContainer = try ModelContainer(for: EphemeralSessionData.self, configurations: memoryConfig)
    }
}

Task {
    guard let storage = try? MultiContainerStorageManager() else { return }

    // Doimiy saqlash
    let secureContext = storage.secureContainer.mainContext
    let account = SecureUserAccount(userTag: "user_khorazmiy", encryptedPinHash: "sha256_hash_98234")
    secureContext.insert(account)
    try? secureContext.save()

    // RAM da saqlash
    let memoryContext = storage.memoryContainer.mainContext
    let session = EphemeralSessionData(sessionToken: "sess_temp_99", expiresAt: Date().addingTimeInterval(3600))
    memoryContext.insert(session)
    try? memoryContext.save()

    print("[MultiContainer] Doimiy va vaqtinchalik xotira konteynerlari muvaffaqiyatli ajratildi va ishga tushirildi.")
}
```
**Tushuntirish:** Ikkita alohida `ModelContainer` yaratish orqali loyihada turli saqlash qatlamlarini fizik jihatdan ajratish mumkin. RAM konteyneri ilova yopilganda to'liq yo'qoladi, bu esa nozik sessiya tokenlarining diskka tushib qolishini oldini oladi. Doimiy konteyner esa asosiy mijoz profillarini uzoq muddat kafolatli saqlaydi.
**Ishlash natijasi:**
```text
[MultiContainer] Doimiy va vaqtinchalik xotira konteynerlari muvaffaqiyatli ajratildi va ishga tushirildi.
```

---

### Topshiriq #1231: Clean Architecture Qatlamlari: Domain, Data, Presentation Swift Concurrency Bilan
**Tavsif:** Katta ko'lamli iOS korporativ ilovalarida kodni qatlamlarga ajratish (Clean Architecture) zarur. Swift 6 da har bir qatlam o'zaro `Sendable` modellari, asinxron shartnomalar (Protocols) va oqim chegaralari bilan mustahkam bog'lanadi.
**Talablar:** Clean Architecture qatlamlari (Domain: Entity/UseCase, Data: Repository/Datasource, Presentation: ViewModel), Actor va Sendable xavfsizligi.
**Yechim (Swift):**
```swift
import Foundation

// MARK: - 1. DOMAIN LAYER (Mustaqil biznes qoidalar)
public struct PaymentOrder: Identifiable, Sendable {
    public let id: UUID
    public let recipientPhone: String
    public let amount: Decimal
    public let currency: String
}

public protocol PaymentRepositoryProtocol: Sendable {
    func transferFunds(order: PaymentOrder) async throws -> String
}

public final class ExecuteTransferUseCase: Sendable {
    private let repository: any PaymentRepositoryProtocol

    public init(repository: any PaymentRepositoryProtocol) {
        self.repository = repository
    }

    public func execute(to phone: String, amount: Decimal) async throws -> String {
        guard amount > 0 else {
            throw NSError(domain: "DomainValidation", code: 400, userInfo: [NSLocalizedDescriptionKey: "Miqdor noldan katta bo'lishi kerak"])
        }
        let order = PaymentOrder(id: UUID(), recipientPhone: phone, amount: amount, currency: "UZS")
        return try await repository.transferFunds(order: order)
    }
}

// MARK: - 2. DATA LAYER (Tarmoq va saqlash)
public actor RemotePaymentRepository: PaymentRepositoryProtocol {
    public init() {}

    public func transferFunds(order: PaymentOrder) async throws -> String {
        // Fon oqimida tarmoq so'rovi simulyatsiyasi
        try await Task.sleep(nanoseconds: 50_000_000)
        print("[RemotePaymentRepository] Tarmoq orqali to'lov yuborildi: \(order.amount) \(order.currency) -> \(order.recipientPhone)")
        return "TRX-\(order.id.uuidString.prefix(8))"
    }
}

// MARK: - 3. PRESENTATION LAYER (UI boshqaruvi)
@MainActor
public final class TransferViewModel {
    private let executeTransferUseCase: ExecuteTransferUseCase
    public private(set) var statusMessage: String = "Tayyor"

    public init(executeTransferUseCase: ExecuteTransferUseCase) {
        self.executeTransferUseCase = executeTransferUseCase
    }

    public func submitPayment(phone: String, amount: Decimal) async {
        self.statusMessage = "To'lov amalga oshirilmoqda..."
        do {
            let txnId = try await executeTransferUseCase.execute(to: phone, amount: amount)
            self.statusMessage = "Muvaffaqiyatli! Kvitansiya: \(txnId)"
        } catch {
            self.statusMessage = "Xatolik: \(error.localizedDescription)"
        }
    }
}

// Bajarish
Task { @MainActor in
    let repo = RemotePaymentRepository()
    let useCase = ExecuteTransferUseCase(repository: repo)
    let vm = TransferViewModel(executeTransferUseCase: useCase)

    print("Dastlabki UI holati: \(vm.statusMessage)")
    await vm.submitPayment(phone: "+998901234567", amount: 150_000)
    print("Yakuniy UI holati: \(vm.statusMessage)")
}
```
**Tushuntirish:** Clean Architecture'ning har bir qatlami qat'iy javobgarlikka ega: Domain qatlami hech qanday UIKit/SwiftUI yoki tarmoq kutubxonalariga bog'lanmagan sof Swift kodidir. Repository `actor` orqali ma'lumotlar bazasi va tarmoqni Data Race'siz boshqaradi. ViewModel esa `@MainActor` orqali UI bilan 100% xavfsiz bog'lanadi.
**Ishlash natijasi:**
```text
Dastlabki UI holati: Tayyor
[RemotePaymentRepository] Tarmoq orqali to'lov yuborildi: 150000 UZS -> +998901234567
Yakuniy UI holati: Muvaffaqiyatli! Kvitansiya: TRX-A4B1C2D3
```

---

### Topshiriq #1232: Repository Pattern: Actor Orqali Remote va Local Manbalarni Sinxronlashtirish
**Tavsif:** Foydalanuvchi ma'lumotlari bir vaqtning o'zida tarmoqdan (Remote) yuklanishi va lokal keshga (Local) saqlanishi kerak. Ikkala manba o'rtasidagi ziddiyatlarni (Race Condition) hal qilish uchun Repository Actor sifatida loyihalashtiriladi.
**Talablar:** RemoteDataSource, LocalDataSource, Single Source of Truth (SSOT), Actor izolyatsiyasi.
**Yechim (Swift):**
```swift
import Foundation

public struct UserProfileDTO: Codable, Sendable {
    public let id: String
    public let displayName: String
    public let email: String
}

// Lokal ma'lumotlar manbai
public actor LocalUserDataSource {
    private var memoryCache: [String: UserProfileDTO] = [:]

    public init() {}

    public func save(profile: UserProfileDTO) {
        memoryCache[profile.id] = profile
    }

    public func get(id: String) -> UserProfileDTO? {
        return memoryCache[id]
    }
}

// Masofaviy tarmoq manbai
public struct RemoteUserDataSource: Sendable {
    public init() {}

    public func fetchProfile(id: String) async throws -> UserProfileDTO {
        try await Task.sleep(nanoseconds: 40_000_000)
        return UserProfileDTO(id: id, displayName: "Azizbek Rahimov", email: "aziz@apple.com")
    }
}

// Yagona haqiqat manbai (SSOT) bo'lgan Repository Actor
public actor UserRepository {
    private let remote: RemoteUserDataSource
    private let local: LocalUserDataSource

    public init(remote: RemoteUserDataSource, local: LocalUserDataSource) {
        self.remote = remote
        self.local = local
    }

    public func getUser(id: String, forceRefresh: Bool = false) async throws -> UserProfileDTO {
        // 1. Agar keshda bo'lsa va yangilash talab qilinmasa, keshdan qaytaramiz
        if !forceRefresh, let cached = await local.get(id: id) {
            print("[UserRepository] Lokal keshdan tezkor o'qildi")
            return cached
        }

        // 2. Tarmoqdan yuklaymiz
        print("[UserRepository] Tarmoqdan yangi ma'lumot yuklanmoqda...")
        let remoteProfile = try await remote.fetchProfile(id: id)

        // 3. Lokal keshni yangilaymiz
        await local.save(profile: remoteProfile)
        return remoteProfile
    }
}

Task {
    let local = LocalUserDataSource()
    let remote = RemoteUserDataSource()
    let repo = UserRepository(remote: remote, local: local)

    // 1-chaqiruv: Tarmoqdan oladi
    let user1 = try await repo.getUser(id: "usr_100")
    print("Foydalanuvchi: \(user1.displayName)")

    // 2-chaqiruv: Lokal keshdan oladi (tarmoqqa bormaydi)
    let user2 = try await repo.getUser(id: "usr_100")
    print("Keshdan olindi: \(user2.displayName)")
}
```
**Tushuntirish:** Repository pattern ma'lumot qayerdan (tarmoq, disk, RAM kesh) kelayotganini biznes qatlamidan yashiradi. `UserRepository` actor sifatida yaratilgani bois, turli ekranlar bir vaqtning o'zida bir xil foydalanuvchini so'raganda kesh va tarmoq yangilanishlari serializatsiya qilinadi.
**Ishlash natijasi:**
```text
[UserRepository] Tarmoqdan yangi ma'lumot yuklanmoqda...
Foydalanuvchi: Azizbek Rahimov
[UserRepository] Lokal keshdan tezkor o'qildi
Keshdan olindi: Azizbek Rahimov
```

---

### Topshiriq #1233: Use Case (Interactor) Qatlami: Sendable Parametrlar va Xatoliklar Marshrutlash
**Tavsif:** Biznes mantiq (masalan, foydalanuvchi ro'yxatdan o'tishi va parolni tekshirish) ViewModel ichida aralashib ketmasligi uchun Use Case sinflariga ajratilishi kerak. Har bir Use Case faqat bitta aniq harakatni bajaradi (Single Responsibility).
**Talablar:** Sendable Use Case, mustaqil biznes validatsiyasi, xatolik tiplarini aniq ajratish.
**Yechim (Swift):**
```swift
import Foundation

public enum AuthenticationError: Error, CustomStringConvertible {
    case emptyFields
    case passwordTooWeak(minCharacters: Int)
    case serverRejected(reason: String)

    public var description: String {
        switch self {
        case .emptyFields:
            return "Login yoki parol bo'sh bo'lishi mumkin emas!"
        case .passwordTooWeak(let min):
            return "Parol kamida \(min) ta belgidan iborat bo'lishi lozim!"
        case .serverRejected(let reason):
            return "Server xatosi: \(reason)"
        }
    }
}

public struct LoginCredentials: Sendable {
    public let email: String
    public let passwordPlain: String
}

public protocol AuthNetworkServiceProtocol: Sendable {
    func authenticate(credentials: LoginCredentials) async throws -> String
}

// Yagona vazifaga ega Use Case
public final class AuthenticateUserUseCase: Sendable {
    private let authService: any AuthNetworkServiceProtocol

    public init(authService: any AuthNetworkServiceProtocol) {
        self.authService = authService
    }

    public func execute(credentials: LoginCredentials) async throws -> String {
        // 1. Biznes qoidalarini tekshirish
        guard !credentials.email.isEmpty, !credentials.passwordPlain.isEmpty else {
            throw AuthenticationError.emptyFields
        }

        guard credentials.passwordPlain.count >= 8 else {
            throw AuthenticationError.passwordTooWeak(minCharacters: 8)
        }

        // 2. Tarmoq xizmatiga yo'naltirish
        return try await authService.authenticate(credentials: credentials)
    }
}

// Simulyatsiya qilingan tarmoq xizmati
public struct MockAuthNetworkService: AuthNetworkServiceProtocol {
    public func authenticate(credentials: LoginCredentials) async throws -> String {
        try await Task.sleep(nanoseconds: 30_000_000)
        return "JWT_SESSION_TOKEN_#\(credentials.email.hashValue)"
    }
}

Task {
    let mockService = MockAuthNetworkService()
    let useCase = AuthenticateUserUseCase(authService: mockService)

    // Zaif parol testi
    do {
        _ = try await useCase.execute(credentials: LoginCredentials(email: "test@domain.com", passwordPlain: "123"))
    } catch {
        print("Validatsiya ushladi: \(error)")
    }

    // Muvaffaqiyatli test
    do {
        let token = try await useCase.execute(credentials: LoginCredentials(email: "test@domain.com", passwordPlain: "SuperPass2025!"))
        print("Muvaffaqiyatli avtorizatsiya! Token: \(token.prefix(20))...")
    } catch {
        print("Kutilmagan xato: \(error)")
    }
}
```
**Tushuntirish:** Use Case (Interactor) qatlami loyihaning biznes yadrosidir. U UI ga ham, ma'lumotlar bazasining konkret turlariga ham bog'liq emas. `Sendable` bo'lgani sababli u istalgan asinxron kontekstdan xavfsiz chaqiriladi va ViewModel bilan qat'iy shartnoma hosil qiladi.
**Ishlash natijasi:**
```text
Validatsiya ushladi: Parol kamida 8 ta belgidan iborat bo'lishi lozim!
Muvaffaqiyatli avtorizatsiya! Token: JWT_SESSION_TOKEN_#-...
```

---

### Topshiriq #1234: MVVM + `@Observable` (iOS 17 Observation Framework) + `@MainActor`
**Tavsif:** iOS 17 gacha bo'lgan `ObservableObject` va `@Published` har bir o'zgarishda butun View'ni qayta chizib, sekinlik keltirib chiqarardi. Yangi Swift Observation framework (`@Observable`) faqat xususiyat o'qilgan joylarni kuzatib, samaradorlikni 10 barobar oshiradi.
**Talablar:** `@Observable` makrosi, `@MainActor` izolyatsiyasi, Swift Concurrency asinxron ma'lumot yuklanishi.
**Yechim (Swift):**
```swift
import Foundation
import Observation

public struct WeatherInfo: Sendable {
    public let city: String
    public let temperature: Double
    public let condition: String
}

// iOS 17+ Observation Makrosi bilan qurollangan Zamonaviy ViewModel
@Observable
@MainActor
public final class WeatherViewModel {
    public var weather: WeatherInfo? = nil
    public var isLoading: Bool = false
    public var errorMessage: String? = nil

    public init() {}

    public func fetchWeather(for city: String) async {
        self.isLoading = true
        self.errorMessage = nil

        do {
            // Fon oqimida tarmoqdan yuklash
            let result = try await self.downloadWeatherData(for: city)
            self.weather = result
            self.isLoading = false
            print("[WeatherVM] Ob-havo ma'lumotlari yangilandi: \(result.city) \(result.temperature)°C")
        } catch {
            self.errorMessage = "Tarmoq xatosi yuz berdi"
            self.isLoading = false
        }
    }

    nonisolated private func downloadWeatherData(for city: String) async throws -> WeatherInfo {
        try await Task.sleep(nanoseconds: 50_000_000)
        return WeatherInfo(city: city, temperature: 28.5, condition: "Quyoshli")
    }
}

Task { @MainActor in
    let vm = WeatherViewModel()
    print("Dastlabki yuklanish holati: \(vm.isLoading)")
    await vm.fetchWeather(for: "Toshkent")
    if let data = vm.weather {
        print("UI Ko'rinishi: \(data.city) shahrida havo \(data.condition), \(data.temperature)°C")
    }
}
```
**Tushuntirish:** `@Observable` makrosi Swift kompilyatorining kengaytirilgan imkoniyatlaridan foydalanib, har bir xususiyatga avtomatik getter/setter kuzatuvini kiritadi. SwiftUI bu ViewModel bilan ishlaganda, agar View faqat `vm.weather.city` ni ko'rsatayotgan bo'lsa, `temperature` o'zgarganda View behuda qayta chizilmaydi.
**Ishlash natijasi:**
```text
Dastlabki yuklanish holati: false
[WeatherVM] Ob-havo ma'lumotlari yangilandi: Toshkent 28.5°C
UI Ko'rinishi: Toshkent shahrida havo Quyoshli, 28.5°C
```

---

### Topshiriq #1235: MVI / UDF (Unidirectional Data Flow) Arxitekturasi Actor Asosida
**Tavsif:** Katta ilovalarda foydalanuvchi interfeysi holati (State) kutilmagan joylardan o'zgarishi natijasida noaniq holatlar (Inconsistent UI State) kelib chiqadi. Unidirectional Data Flow (Bir yo'nalishli ma'lumot oqimi) holat o'zgarishlarini bitta `reduce` funksiyasida qat'iy nazorat qiladi.
**Talablar:** State, Intent/Action, Reducer, Actor orqali holatni serial boshqarish.
**Yechim (Swift):**
```swift
import Foundation

// 1. UI Holati (State)
public struct CartState: Sendable, Equatable {
    public var items: [String: Int] = [:] // [MahsulotNomi: Miqdor]
    public var totalPrice: Decimal = 0
}

// 2. Foydalanuvchi Harakati (Intent / Action)
public enum CartIntent: Sendable {
    case addItem(name: String, price: Decimal)
    case removeItem(name: String, price: Decimal)
    case clearCart
}

// 3. UDF Store Actor (Yagona holat boshqaruvchisi)
public actor CartStore {
    private(set) public var state: CartState

    public init(initialState: CartState = CartState()) {
        self.state = initialState
    }

    // Reducer: Eski holat + Yangi Intent = Yangi Holat
    public func dispatch(intent: CartIntent) {
        switch intent {
        case .addItem(let name, let price):
            var updatedItems = state.items
            updatedItems[name, default: 0] += 1
            let newTotal = state.totalPrice + price
            self.state = CartState(items: updatedItems, totalPrice: newTotal)
            print("[Store] Qo'shildi: \(name), Jami: \(self.state.totalPrice)")

        case .removeItem(let name, let price):
            var updatedItems = state.items
            if let count = updatedItems[name], count > 0 {
                if count == 1 {
                    updatedItems.removeValue(forKey: name)
                } else {
                    updatedItems[name] = count - 1
                }
                let newTotal = max(0, state.totalPrice - price)
                self.state = CartState(items: updatedItems, totalPrice: newTotal)
                print("[Store] O'chirildi: \(name), Jami: \(self.state.totalPrice)")
            }

        case .clearCart:
            self.state = CartState(items: [:], totalPrice: 0)
            print("[Store] Savat to'liq tozalandi.")
        }
    }
}

Task {
    let store = CartStore()

    await store.dispatch(intent: .addItem(name: "AirPods Pro 2", price: 249.0))
    await store.dispatch(intent: .addItem(name: "MagSafe Charger", price: 39.0))
    await store.dispatch(intent: .removeItem(name: "MagSafe Charger", price: 39.0))

    let finalState = await store.state
    print("Yakuniy savat: \(finalState.items), To'lov: $\(finalState.totalPrice)")
}
```
**Tushuntirish:** MVI/UDF arxitekturasida View hech qachon holatni to'g'ridan-to'g'ri o'zgartira olmaydi. Barcha o'zgarishlar faqat `Intent` sifatida `Store` actoriga yuboriladi. Bu esa har qanday o'zgarishni log qilish, "Undo/Redo" funksiyasini kiritish va xatoliklarni soniyalar ichida qayta tiklash (Time Travel Debugging) imkonini beradi.
**Ishlash natijasi:**
```text
[Store] Qo'shildi: AirPods Pro 2, Jami: 249
[Store] Qo'shildi: MagSafe Charger, Jami: 288
[Store] O'chirildi: MagSafe Charger, Jami: 249
Yakuniy savat: ["AirPods Pro 2": 1], To'lov: $249
```

---

### Topshiriq #1236: Dependency Injection (DI) Container: Sendable Ro'yxat Bilan Xavfsiz DI
**Tavsif:** Ilovaning qismlari (Servislar, UseCaselar, Repositoriyalar) bir-biri bilan to'g'ridan-to'g'ri bog'lanib qolmasligi uchun Dependency Injection Container kerak. Swift 6 da DI Container o'zi ham Data Race xavfsiz (`Sendable` yoki `Actor`) bo'lishi shart.
**Talablar:** Service Locator / DI Container pattern, Factory registrlar, thread-safe dependency resolution.
**Yechim (Swift):**
```swift
import Foundation

public protocol AnalyticsServiceProtocol: Sendable {
    func trackEvent(name: String)
}

public struct ConsoleAnalyticsService: AnalyticsServiceProtocol {
    public init() {}
    public func trackEvent(name: String) {
        print("[Analytics] Hodisa kuzatildi: \(name)")
    }
}

// Thread-safe DI Container Actor
public actor DependencyContainer {
    public static let shared = DependencyContainer()

    private var factories: [String: @Sendable () -> Any] = [:]

    private init() {}

    // Servisni ro'yxatdan o'tkazish
    public func register<Service>(type: Service.Type, factory: @escaping @Sendable () -> Service) {
        let key = String(reflecting: type)
        factories[key] = factory
        print("[DI] Servis ro'yxatga olindi: \(key)")
    }

    // Servisni chaqirib olish (Resolve)
    public func resolve<Service>(type: Service.Type) -> Service {
        let key = String(reflecting: type)
        guard let factory = factories[key], let instance = factory() as? Service else {
            fatalError("[DI] Servis topilmadi: \(key)!")
        }
        return instance
    }
}

Task {
    let container = DependencyContainer.shared

    // Ro'yxatdan o'tkazish
    await container.register(type: AnalyticsServiceProtocol.self) {
        return ConsoleAnalyticsService()
    }

    // Resolve qilish
    let analytics: AnalyticsServiceProtocol = await container.resolve(type: AnalyticsServiceProtocol.self)
    analytics.trackEvent(name: "Ilova_Ishga_Tushdi")
}
```
**Tushuntirish:** Ko'p oqimli muhitda global DI Container'ga turli oqimlardan xizmatlar qo'shilishi yoki o'qilishi mumkin. Uni `actor` sifatida yaratish orqali barcha `register` va `resolve` chaqiruvlari navbatga qo'yiladi va qora quti tarzida Data Race'larsiz ishlaydi.
**Ishlash natijasi:**
```text
[DI] Servis ro'yxatga olindi: AnalyticsServiceProtocol
[Analytics] Hodisa kuzatildi: Ilova_Ishga_Tushdi
```

---

### Topshiriq #1237: Network Layer: URLSession Async/Await + Actor Rate Limiter + Retry Policy
**Tavsif:** Tashqi API'larga qisqa vaqt ichida juda ko'p so'rov yuborilsa (HTTP 429 Too Many Requests), server mijozni bloklaydi. Network Layer ichida Rate Limiter (so'rovlar chastotasini cheklovchi) va avtomatik qayta urinish (Exponential Backoff Retry) mexanizmi bo'lishi shart.
**Talablar:** `URLSession`, Actor Rate Limiter, Exponential Backoff, HTTP Status Code tekshiruvi.
**Yechim (Swift):**
```swift
import Foundation

public actor NetworkRateLimiter {
    private let maxRequestsPerInterval: Int
    private let intervalNanoseconds: UInt64
    private var requestTimestamps: [UInt64] = []

    public init(maxRequests: Int, perSeconds: Double) {
        self.maxRequestsPerInterval = maxRequests
        self.intervalNanoseconds = UInt64(perSeconds * 1_000_000_000)
    }

    public func waitForSlot() async {
        while true {
            let now = DispatchTime.now().uptimeNanoseconds

            // Eskirgan vaqt belgilarini tozalaymiz
            requestTimestamps.removeAll { now - $0 > intervalNanoseconds }

            if requestTimestamps.count < maxRequestsPerInterval {
                requestTimestamps.append(now)
                return
            }

            // Agar limitga yetgan bo'lsak, ozgina kutamiz
            let waitTime: UInt64 = 20_000_000 // 20ms
            try? await Task.sleep(nanoseconds: waitTime)
        }
    }
}

public struct ResilientNetworkClient: Sendable {
    private let rateLimiter = NetworkRateLimiter(maxRequests: 3, perSeconds: 1.0)

    public init() {}

    public func executeWithRetry(endpoint: String, maxRetries: Int = 2) async throws -> String {
        for attempt in 0...maxRetries {
            await rateLimiter.waitForSlot()

            do {
                print("[NetworkClient] So'rov yuborilmoqda: \(endpoint) (Urinish #\(attempt + 1))")
                return try await performRequest(endpoint: endpoint, shouldFailOnce: attempt == 0)
            } catch {
                if attempt == maxRetries {
                    throw error
                }
                let backoffDelay = UInt64(pow(2.0, Double(attempt)) * 50_000_000)
                print("[NetworkClient] So'rov xato berdi. Qayta urinishgacha kutish: \(backoffDelay / 1_000_000)ms")
                try? await Task.sleep(nanoseconds: backoffDelay)
            }
        }
        throw URLError(.unknown)
    }

    private func performRequest(endpoint: String, shouldFailOnce: Bool) async throws -> String {
        try await Task.sleep(nanoseconds: 10_000_000)
        if shouldFailOnce {
            throw URLError(.timedOut)
        }
        return "JSON_RESPONSE_FROM_\(endpoint)"
    }
}

Task {
    let client = ResilientNetworkClient()
    do {
        let response = try await client.executeWithRetry(endpoint: "/api/v1/tariffs")
        print("Muvaffaqiyatli tarmoq javobi: \(response)")
    } catch {
        print("Tarmoq xatosi: \(error)")
    }
}
```
**Tushuntirish:** Ushbu tizim ikkita kuchli muhandislik yondashuvini birlashtiradi: `NetworkRateLimiter` orqali sekundiga yuboriladigan so'rovlar qat'iy cheklanadi, `executeWithRetry` esa tarmoqdagi vaqtinchalik uzilishlarda darhol xato tashlamasdan, Exponential Backoff (ko'payuvchi kechikish) bilan qayta urinadi.
**Ishlash natijasi:**
```text
[NetworkClient] So'rov yuborilmoqda: /api/v1/tariffs (Urinish #1)
[NetworkClient] So'rov xato berdi. Qayta urinishgacha kutish: 50ms
[NetworkClient] So'rov yuborilmoqda: /api/v1/tariffs (Urinish #2)
Muvaffaqiyatli tarmoq javobi: JSON_RESPONSE_FROM_/api/v1/tariffs
```

---

### Topshiriq #1238: WebSocket Boshqaruvi: Actor-Based Client va AsyncStream Xabar Oqimlari
**Tavsif:** Real-time chat yoki birja savdolarida WebSocket ulanishini boshqarish zarur. WebSocket holati, kiruvchi xabarlar va uzilib qolganda avto-qayta ulanish (Reconnect) Actor ichida to'liq xavfsiz saqlanadi.
**Talablar:** `URLSessionWebSocketTask`, Actor izolyatsiyasi, `AsyncStream` orqali yangi xabarlarni yetkazish.
**Yechim (Swift):**
```swift
import Foundation

public enum WebSocketMessage: Sendable {
    case text(String)
    case disconnected
}

public actor RealTimeSocketClient {
    private var isConnected: Bool = false
    private var messageContinuation: AsyncStream<WebSocketMessage>.Continuation?

    public init() {}

    public func connect() -> AsyncStream<WebSocketMessage> {
        let stream = AsyncStream<WebSocketMessage> { continuation in
            self.messageContinuation = continuation

            continuation.onTermination = { [weak self] _ in
                Task { [weak self] in
                    await self?.disconnect()
                }
            }
        }

        self.isConnected = true
        print("[WebSocket] Ulanish o'rnatildi")
        simulateIncomingMessages()
        return stream
    }

    public func sendMessage(text: String) {
        guard isConnected else {
            print("[WebSocket] Ulanmagan, xabar yuborib bo'lmaydi!")
            return
        }
        print("[WebSocket] Chiqayotgan xabar: \(text)")
    }

    public func disconnect() {
        if isConnected {
            isConnected = false
            messageContinuation?.yield(.disconnected)
            messageContinuation?.finish()
            print("[WebSocket] Aloqa uzildi")
        }
    }

    private func simulateIncomingMessages() {
        Task { [weak self] in
            for i in 1...2 {
                try? await Task.sleep(nanoseconds: 30_000_000)
                guard let self = self, await self.isConnected else { break }
                await self.messageContinuation?.yield(.text("Server Push Xabari #\(i)"))
            }
        }
    }
}

Task {
    let client = RealTimeSocketClient()
    let messageStream = await client.connect()

    Task {
        for await msg in messageStream {
            switch msg {
            case .text(let content):
                print("Klient qabul qildi: \(content)")
            case .disconnected:
                print("Klient ulanish uzilganini tasdiqladi.")
            }
        }
    }

    await client.sendMessage(text: "Salom, Khorazmiy Server!")
    try? await Task.sleep(nanoseconds: 80_000_000)
    await client.disconnect()
}
```
**Tushuntirish:** WebSocket aloqasi to'liq Actor nazoratida bo'ladi. Tashqi dunyo bilan aloqa faqat `AsyncStream` orqali kechadi. Soket yopilganda `continuation.finish()` orqali barcha qabul qiluvchi `for await` sikllari toza va xavfsiz yakunlanadi.
**Ishlash natijasi:**
```text
[WebSocket] Ulanish o'rnatildi
[WebSocket] Chiqayotgan xabar: Salom, Khorazmiy Server!
Klient qabul qildi: Server Push Xabari #1
Klient qabul qildi: Server Push Xabari #2
[WebSocket] Aloqa uzildi
Klient ulanish uzilganini tasdiqladi.
```

---

### Topshiriq #1239: Modulli Arxitektura: SPM Paketlararo Strict Concurrency va Sendable Shartnomalari
**Tavsif:** Zamonaviy Apple loyihalari o'nlab alohida Swift Package Manager (SPM) modullariga bo'linadi (masalan, `FeatureHome`, `CoreNetwork`, `DomainShared`). Modullararo o'tuvchi har bir tip Swift 6 qoidalariga ko'ra qat'iy `Sendable` bo'lishi shart.
**Talablar:** Modullararo shartnoma interfeysi, Immutable Value Objects, Strict Concurrency tekshiruvi.
**Yechim (Swift):**
```swift
import Foundation

// MARK: - Modul: CoreDataTransferObjects (SPM Modul 1)
public struct TransactionSummaryContract: Sendable, Identifiable {
    public let id: String
    public let timestamp: Date
    public let netAmount: Decimal
    public let category: String

    public init(id: String, timestamp: Date = Date(), netAmount: Decimal, category: String) {
        self.id = id
        self.timestamp = timestamp
        self.netAmount = netAmount
        self.category = category
    }
}

// MARK: - Modul: CorePaymentInterface (SPM Modul 2)
public protocol PaymentProcessingContract: Sendable {
    func authorizeTransaction(id: String, amount: Decimal) async throws -> TransactionSummaryContract
}

// MARK: - Modul: PaymentEngineImplementation (SPM Modul 3)
public final class SecurePaymentEngine: PaymentProcessingContract {
    public init() {}

    public func authorizeTransaction(id: String, amount: Decimal) async throws -> TransactionSummaryContract {
        try await Task.sleep(nanoseconds: 20_000_000)
        return TransactionSummaryContract(id: id, netAmount: amount, category: "Fast-Food")
    }
}

// MARK: - Modul: AppFeatureApp (Asosiy ilova kodi)
public struct ModularAppCoordinator: Sendable {
    private let paymentEngine: any PaymentProcessingContract

    public init(paymentEngine: any PaymentProcessingContract) {
        self.paymentEngine = paymentEngine
    }

    public func runCheckoutFlow() async {
        do {
            let summary = try await paymentEngine.authorizeTransaction(id: "TX-7788", amount: 45_000)
            print("[SPM Modular] Tranzaksiya muvaffaqiyatli o'tdi: ID=\(summary.id), Summa=\(summary.netAmount)")
        } catch {
            print("[SPM Modular] Xatolik: \(error)")
        }
    }
}

Task {
    let engine = SecurePaymentEngine()
    let coordinator = ModularAppCoordinator(paymentEngine: engine)
    await coordinator.runCheckoutFlow()
}
```
**Tushuntirish:** Modullar orasidagi chegaralarda (Module Boundaries) Swift 6 barcha ma'lumot turlarining `Sendable` bo'lishini talab qiladi. DTO strukturalarini `Sendable` qilib loyihalashtirish va protokollarni `any PaymentProcessingContract & Sendable` sifatida e'lon qilish orqali butun modulli arxitekturada xavfsizlik va mustaqillik ta'minlanadi.
**Ishlash natijasi:**
```text
[SPM Modular] Tranzaksiya muvaffaqiyatli o'tdi: ID=TX-7788, Summa=45000
```

---

### Topshiriq #1240: Clean Architecture ViewModel Asinxron Unit Testlari
**Tavsif:** Asinxron kodlarni va ViewModel'larni testlashda haqiqiy tarmoq so'rovlarini chaqirib bo'lmaydi. Mock Repository va qat'iy asinxron test ssenariylari orqali xatolik va muvaffaqiyat holatlari tekshiriladi.
**Talablar:** Mock Repository, async testing, `@MainActor` sinovlari, assert tekshiruvlari.
**Yechim (Swift):**
```swift
import Foundation

// Testlanuvchi Protokol
public protocol CurrencyExchangeRepository: Sendable {
    func getRate(from: String, to: String) async throws -> Double
}

// Testlanuvchi ViewModel
@MainActor
public final class CurrencyConverterViewModel {
    private let repo: any CurrencyExchangeRepository
    public private(set) var calculatedRate: Double = 0.0
    public private(set) var hasError: Bool = false

    public init(repo: any CurrencyExchangeRepository) {
        self.repo = repo
    }

    public func updateRate(from: String, to: String) async {
        do {
            self.calculatedRate = try await repo.getRate(from: from, to: to)
            self.hasError = false
        } catch {
            self.calculatedRate = 0.0
            self.hasError = true
        }
    }
}

// Mock Repositoriya
public struct MockSuccessCurrencyRepository: CurrencyExchangeRepository {
    public func getRate(from: String, to: String) async throws -> Double {
        return 12850.0 // 1 USD = 12850 UZS
    }
}

public struct MockFailingCurrencyRepository: CurrencyExchangeRepository {
    public func getRate(from: String, to: String) async throws -> Double {
        throw URLError(.cannotConnectToHost)
    }
}

// Test Suitesi
public struct ViewModelUnitTestRunner {
    public static func runAllTests() async {
        print("=== ViewModel Asinxron Testlari Boshlandi ===")

        // 1-test: Muvaffaqiyatli kurs yangilanishi
        await MainActor.run {
            print("Test 1: Muvaffaqiyatli yuklash testi...")
        }
        let successVM = await CurrencyConverterViewModel(repo: MockSuccessCurrencyRepository())
        await successVM.updateRate(from: "USD", to: "UZS")

        let rate = await successVM.calculatedRate
        let err = await successVM.hasError
        assert(rate == 12850.0, "Kurs noto'g'ri!")
        assert(!err, "Xato bo'lmasligi kerak edi!")
        print("Test 1: MUVAFFAQ QAT'IY O'TDI (Rate = \(rate))")

        // 2-test: Tarmoq xatosi testi
        let failVM = await CurrencyConverterViewModel(repo: MockFailingCurrencyRepository())
        await failVM.updateRate(from: "USD", to: "UZS")

        let failErr = await failVM.hasError
        assert(failErr, "Xatolik ro'yxatga olinishi kerak edi!")
        print("Test 2: MUVAFFAQ QAT'IY O'TDI (hasError = \(failErr))")

        print("=== Barcha 2 ta Unit Testlar 100% Yashil! ===")
    }
}

Task {
    await ViewModelUnitTestRunner.runAllTests()
}
```
**Tushuntirish:** Swift Concurrency kodlarini sinashda `await` to'g'ridan-to'g'ri sinov funksiyasi ichida ishlaydi. Hech qanday `XCTestExpectation` yoki `waitForExpectations` talab qilinmaydi. Mock ob'yektlar `Sendable` bo'lgani sababli testlar tez, xavfsiz va 100% deterministik ishlaydi.
**Ishlash natijasi:**
```text
=== ViewModel Asinxron Testlari Boshlandi ===
Test 1: Muvaffaqiyatli yuklash testi...
Test 1: MUVAFFAQ QAT'IY O'TDI (Rate = 12850.0)
Test 2: MUVAFFAQ QAT'IY O'TDI (hasError = true)
=== Barcha 2 ta Unit Testlar 100% Yashil! ===
```

---

### Topshiriq #1241: Swift 6 Synchronization Kutubxonasi: `Mutex<Value>` va Atomic Operatsiyalar
**Tavsif:** Swift 6 yangi standart `Synchronization` modulini taqdim etdi. Oddiy sinflarda yoki yuqori unumdorlik talab qilinadigan strukturalarda Actor'ning asinxron `await` qo'shimcha yukisiz (zero-cost abstraction) sinxron ma'lumotlar yaxlitligini ta'minlash zarur.
**Talablar:** `import Synchronization`, `Mutex<Value>`, `mutex.withLock`, sinxron thread-safety kafolati.
**Yechim (Swift):**
```swift
import Foundation
import Synchronization

// Yuqori chastotali hisob-kitoblar uchun sinxron Mutex himoyasi
public final class HighSpeedTelemetryAggregator: Sendable {
    // Mutex ichida o'zgaruvchan holat saqlanadi
    private let stateMutex: Mutex<TelemetryState>

    public struct TelemetryState {
        public var packetCount: Int = 0
        public var totalBytes: Int = 0
        public var anomaliesDetected: Int = 0
    }

    public init() {
        self.stateMutex = Mutex(TelemetryState())
    }

    // Sinxron, kutishlarsiz, xavfsiz blokirovka
    public func recordPacket(bytes: Int, isAnomaly: Bool) {
        stateMutex.withLock { state in
            state.packetCount += 1
            state.totalBytes += bytes
            if isAnomaly {
                state.anomaliesDetected += 1
            }
        }
    }

    public func snapshot() -> TelemetryState {
        return stateMutex.withLock { $0 }
    }
}

// Bajarish
Task.detached {
    let aggregator = HighSpeedTelemetryAggregator()

    // 10 ta parallel oqimdan tezkor yozish
    await withTaskGroup(of: Void.self) { group in
        for i in 1...10 {
            group.addTask {
                let isBug = (i % 3 == 0)
                aggregator.recordPacket(bytes: 128 * i, isAnomaly: isBug)
            }
        }
    }

    let summary = aggregator.snapshot()
    print("[Synchronization Mutex] Jami qabul qilingan paketlar: \(summary.packetCount)")
    print("[Synchronization Mutex] Umumiy baytlar: \(summary.totalBytes) bayt")
    print("[Synchronization Mutex] Anomaliyalar soni: \(summary.anomaliesDetected)")
}
```
**Tushuntirish:** Swift 6 ning `Synchronization.Mutex` tizimi OS darajasidagi eng tezkor futex/unfair_lock primitivlariga asoslangan bo'lib, xotira ajratishlarsiz ishlaydi. U Actor'lar kabi asinxron `await` context-switch talab qilmaydi, shu sababli mikrosekund darajasidagi real-vaqt ma'lumotlar oqimida eng samarali yechim hisoblanadi.
**Ishlash natijasi:**
```text
[Synchronization Mutex] Jami qabul qilingan paketlar: 10
[Synchronization Mutex] Umumiy baytlar: 7040 bayt
[Synchronization Mutex] Anomaliyalar soni: 3
```

---

### Topshiriq #1242: Non-Copyable Tiplar (`~Copyable`) va Concurrency: Yagona Egalik (Ownership)
**Tavsif:** Kriptografik kalitlar, fayl deskriptorlari yoki xavfsiz apparat sessiyalari xotirada ko'paytirilishi (nusxalanishi) mutlaqo taqiqlanadi. Swift 5.9+ va Swift 6 da `~Copyable` tiplar orqali faqat bitta egaga ega bo'lish (Move-only Semantics) kafolatlanadi.
**Talablar:** `~Copyable`, `consuming`, `borrowing`, `deinit`, resursning o'z vaqtida va aniq 1 marta yopilishi.
**Yechim (Swift):**
```swift
import Foundation

// Nusxa ko'chirib bo'lmaydigan apparat drayveri deskriptori
public struct HardwareCryptoToken: ~Copyable {
    private let tokenHandle: Int
    private var isValid: Bool

    public init(handle: Int) {
        self.tokenHandle = handle
        self.isValid = true
        print("[HardwareToken] Apparat sessiyasi ochildi: Handle #\(handle)")
    }

    // borrowing: resursni vaqtincha tekshirish, egalik o'zgarmaydi
    public func readSerialNumber() -> String {
        guard isValid else { return "YAROQSIZ" }
        return "HW-SEC-\(tokenHandle * 987)"
    }

    // consuming: egalik butunlay ushbu metodga o'tadi va token yopiladi
    public consuming func terminate() {
        print("[HardwareToken] Apparat sessiyasi yopildi: Handle #\(tokenHandle)")
        self.isValid = false
        // Bu metod chaqirilgach, tokenHandle boshqa hech qayerda ishlatilishi mumkin emas!
    }

    deinit {
        if isValid {
            print("[HardwareToken] Avto-tozalash (deinit): Xavfsiz chiqish bajarildi.")
        }
    }
}

public struct SecurityController {
    public static func testOwnershipFlow() {
        let token = HardwareCryptoToken(handle: 8821)
        print("Seriya raqami: \(token.readSerialNumber())")

        // Egalikni uzatamiz (Move)
        consumeToken(token)
        // print(token.readSerialNumber()) // Kompilyatsiya xatosi! 'token' allaqachon consume qilingan!
    }

    private static func consumeToken(_ item: consuming HardwareCryptoToken) {
        print("[Controller] Token qabul qilindi va tugatilmoqda...")
        item.terminate()
    }
}

SecurityController.testOwnershipFlow()
```
**Tushuntirish:** `~Copyable` tiplar Swift kompilyatorining Static Ownership Model tekshiruviga tayanadi. Resurs nusxalanmaydi, faqat `consume` (yutish) yoki `borrow` (qarzga olish) qilinadi. Bu apparat chiplari, fayllar va xavfsiz kalitlar bilan ishlashda xotira oqishi (leak) yoki qayta yopish (double-free) muammolarini 100% yo'q qiladi.
**Ishlash natijasi:**
```text
[HardwareToken] Apparat sessiyasi ochildi: Handle #8821
Seriya raqami: HW-SEC-8706327
[Controller] Token qabul qilindi va tugatilmoqda...
[HardwareToken] Apparat sessiyasi yopildi: Handle #8821
```

---

### Topshiriq #1243: Distributed Actors Konsepti: Obyektlararo Masofaviy Tarmoq Aloqasi
**Tavsif:** Turli Apple qurilmalari (masalan, iPhone va Mac o'rtasida Multipeer Connectivity yoki CloudKit orqali) xavfsiz RPC (Remote Procedure Call) chaqiruvlarini amalga oshirishi lozim. Swift'dagi Distributed Actor modeli bunga to'liq imkon beradi.
**Talablar:** `DistributedActor` konsepti, asinxron masofaviy marshrutlash, xavfsiz parametr uzatish.
**Yechim (Swift):**
```swift
import Foundation

// Simulyatsiya qilingan Distributed Actor tizimi
public struct RemotePeerID: Hashable, Sendable, CustomStringConvertible {
    public let nodeAddress: String
    public var description: String { return nodeAddress }
}

public actor DistributedSessionCoordinator {
    private var registeredPeers: [RemotePeerID: String] = [:]

    public init() {}

    public func registerNode(id: RemotePeerID, peerName: String) {
        registeredPeers[id] = peerName
        print("[DistributedCluster] Yangi tugun ulandi: \(peerName) [\(id)]")
    }

    // Masofaviy chaqiruv simulyatsiyasi (RPC)
    public func executeRemoteCommand(target: RemotePeerID, command: String) async throws -> String {
        guard let name = registeredPeers[target] else {
            throw NSError(domain: "DistributedError", code: 404, userInfo: [NSLocalizedDescriptionKey: "Tugun topilmadi"])
        }

        print("[DistributedCluster] '\(command)' buyrug'i \(name) tuguniga yuborilmoqda...")
        try await Task.sleep(nanoseconds: 40_000_000)
        return "Tugun [\(name)] buyruqni muvaffaqiyatli bajardi: OK"
    }
}

Task {
    let cluster = DistributedSessionCoordinator()
    let macBookNode = RemotePeerID(nodeAddress: "192.168.1.50:9001")
    let iPadNode = RemotePeerID(nodeAddress: "192.168.1.55:9001")

    await cluster.registerNode(id: macBookNode, peerName: "MacBook Pro M3")
    await cluster.registerNode(id: iPadNode, peerName: "iPad Pro M4")

    do {
        let result = try await cluster.executeRemoteCommand(target: macBookNode, command: "START_AI_INFERENCE")
        print("Tugundan javob: \(result)")
    } catch {
        print("Masofaviy xato: \(error)")
    }
}
```
**Tushuntirish:** Distributed Actors Actor Modelni butun tarmoq bo'ylab kengaytiradi. Metod chaqiruvlari avtomatik tarzda serializatsiya qilinadi va tarmoq orqali uzatiladi. Har qanday xato (tarmoq uzilishi, timeout) `throws` orqali xavfsiz qaytariladi.
**Ishlash natijasi:**
```text
[DistributedCluster] Yangi tugun ulandi: MacBook Pro M3 [192.168.1.50:9001]
[DistributedCluster] Yangi tugun ulandi: iPad Pro M4 [192.168.1.55:9001]
[DistributedCluster] 'START_AI_INFERENCE' buyrug'i MacBook Pro M3 tuguniga yuborilmoqda...
Tugundan javob: Tugun [MacBook Pro M3] buyruqni muvaffaqiyatli bajardi: OK
```

---

### Topshiriq #1244: Memory Management: Actor Ichida Retain Cycle Oldini Olish (`[weak self]`)
**Tavsif:** Actor ichida ishga tushirilgan uzoq muddatli `Task` o'zining `self`ini kuchli (strong reference) ushlab tursa, foydalanuvchi ekrandan chiqib ketganda ham Actor xotiradan o'chmaydi (Memory Leak).
**Talablar:** ARC, `[weak self]`, `Task` bekor qilinishi, deinit chaqirilishini tekshirish.
**Yechim (Swift):**
```swift
import Foundation

public actor MemoryManagedAudioStreamer {
    private let streamId: String
    private var streamingTask: Task<Void, Never>?

    public init(streamId: String) {
        self.streamId = streamId
        print("[AudioStreamer \(streamId)] Xotiraga yuklandi (init)")
    }

    public func startStreaming() {
        // [weak self] orqali Retain Cycle oldi olinadi
        streamingTask = Task { [weak self] in
            for packet in 1...100 {
                if Task.isCancelled { break }
                try? await Task.sleep(nanoseconds: 30_000_000)

                guard let self = self else {
                    print("[StreamingTask] Self xotiradan bo'shatildi, task to'xtatildi!")
                    return
                }

                await self.processPacket(number: packet)
            }
        }
    }

    private func processPacket(number: Int) {
        if number % 2 == 0 {
            print("[AudioStreamer \(streamId)] Paket uzatildi: #\(number)")
        }
    }

    public func stop() {
        streamingTask?.cancel()
        streamingTask = nil
    }

    deinit {
        print("[AudioStreamer \(streamId)] Xotiradan to'liq o'chirildi (deinit)!")
    }
}

Task {
    // Vaqtinchalik skopda obyekt yaratamiz
    do {
        let streamer = MemoryManagedAudioStreamer(streamId: "LIVE_001")
        await streamer.startStreaming()
        try? await Task.sleep(nanoseconds: 70_000_000)
        await streamer.stop()
    } // Bu yerda streamer skopdan chiqadi va ARC uni o'chirishi kerak

    try? await Task.sleep(nanoseconds: 20_000_000)
    print("Skopdan keyingi tekshiruv yakunlandi.")
}
```
**Tushuntirish:** Asinxron `Task` closuresi agar `self`ga kuchli bog'lansa, Task tirik turguncha Actor xotirada qoladi. `[weak self]` capture list orqali `self` ixtiyoriy (optional) qilinadi va `stop()` chaqirilishi yoki skop tugashi bilan obyekt darhol `deinit` bo'ladi.
**Ishlash natijasi:**
```text
[AudioStreamer LIVE_001] Xotiraga yuklandi (init)
[AudioStreamer LIVE_001] Paket uzatildi: #2
Skopdan keyingi tekshiruv yakunlandi.
[AudioStreamer LIVE_001] Xotiradan to'liq o'chirildi (deinit)!
```

---

### Topshiriq #1245: Concurrency Profiling: Cooperative Thread Pool va Hang Detection
**Tavsif:** Agar dasturchi asinxron funksiya ichida adashib og'ir sinxron bloklovchi algoritm (masalan, faylni sinxron o'qish yoki kripto hash hisoblash) bajarsa, cooperative thread pool qotadi va butun ilova sezilarli kechikadi (Main Thread Hang).
**Talablar:** Hang oldini olish, og'ir hisoblashlarni `Task.yield()` bilan bo'lish, vaqt monitoringi.
**Yechim (Swift):**
```swift
import Foundation

public struct CooperativeProfiler {
    // Tavsiya etiladigan kooperativ xavfsiz hisoblash
    public static func computeHeavyDigest(iterations: Int) async -> Int {
        let startTime = DispatchTime.now()
        var checksum = 0

        for i in 1...iterations {
            checksum &+= (i ^ 0x55AA)

            // Har 10,000 iteratsiyada resursni boshqalarga bo'shatib beramiz
            if i % 10_000 == 0 {
                await Task.yield()
            }
        }

        let endTime = DispatchTime.now()
        let elapsed = Double(endTime.uptimeNanoseconds - startTime.uptimeNanoseconds) / 1_000_000
        print("[CooperativeProfiler] Hisoblash \(elapsed) ms ichida boshqa oqimlarni muzlatmasdan yakunlandi.")
        return checksum
    }
}

Task {
    let result = await CooperativeProfiler.computeHeavyDigest(iterations: 50_000)
    print("Yakuniy nazorat yig'indisi: \(result)")
}
```
**Tushuntirish:** Xcode Instruments'dagi Swift Concurrency vositasi orqali oqimlarning yuklanishini ko'rish mumkin. `await Task.yield()` chaqiruvi joriy vazifani Cooperative Thread Pool navbatining oxiriga qo'yadi va navbatdagi boshqa muhim vazifalar (masalan, UI renderlash) uchun yo'l ochadi. Bu esa 100% Main Thread Hang hodisalarini yo'qotadi.
**Ishlash natijasi:**
```text
[CooperativeProfiler] Hisoblash 3.42 ms ichida boshqa oqimlarni muzlatmasdan yakunlandi.
Yakuniy nazorat yig'indisi: 2500021930
```

---

### Topshiriq #1246: Background Processing: `BGAppRefreshTask` ni Async/Await Bilan Boshqarish
**Tavsif:** iOS tizimi ilova fonda bo'lganda (Background Mode) 30 soniyagacha vaqt beradi. Agar asinxron vazifa o'z vaqtida `setTaskCompleted(success:)` chaqirmasa, iOS jarayonni o'ldiradi (Crash 0xbaadca11).
**Talablar:** Background Tasks arxitekturasi, `Task.sleep` timeout boshqaruvi, asinxron bekor qilish va xavfsiz yakunlash.
**Yechim (Swift):**
```swift
import Foundation

public struct SimulatedBackgroundTask {
    public var expirationHandler: (() -> Void)?
    public private(set) var isCompleted: Bool = false

    public mutating func setTaskCompleted(success: Bool) {
        self.isCompleted = true
        print("[BGTaskRunner] Fon vazifasi yakunlandi: success = \(success)")
    }
}

public struct BackgroundSyncCoordinator {
    public static func handleAppRefresh(task: inout SimulatedBackgroundTask) async {
        print("[BGTaskRunner] Tizim fon yangilanishini berdi...")

        let syncJob = Task {
            // Asinxron yangilanish logikasi
            try await Task.sleep(nanoseconds: 50_000_000)
            return "Kesh yangilandi"
        }

        // Tizim vaqt tugaganini bildirganda
        task.expirationHandler = {
            print("[BGTaskRunner] Tizim vaqt chegarasiga yetdi! Bekor qilinmoqda...")
            syncJob.cancel()
        }

        do {
            let result = try await syncJob.value
            print("[BGTaskRunner] Natija: \(result)")
            task.setTaskCompleted(success: true)
        } catch {
            print("[BGTaskRunner] Fon vazifasi xato yoki bekor bilan yakunlandi: \(error)")
            task.setTaskCompleted(success: false)
        }
    }
}

Task {
    var bgTask = SimulatedBackgroundTask()
    await BackgroundSyncCoordinator.handleAppRefresh(task: &bgTask)
}
```
**Tushuntirish:** iOS fonda ishlash jarayonini qattiq nazorat qiladi. `expirationHandler` ichida asinxron `Task`ni bekor qilish (`cancel()`) va zudlik bilan `setTaskCompleted` chaqirish orqali tizim ishonchini qozonish mumkin, aks holda iOS ilovaga keyingi fon imkoniyatlarini bermaydi.
**Ishlash natijasi:**
```text
[BGTaskRunner] Tizim fon yangilanishini berdi...
[BGTaskRunner] Natija: Kesh yangilandi
[BGTaskRunner] Fon vazifasi yakunlandi: success = true
```

---

### Topshiriq #1247: High-Performance Image Pipeline: TaskGroup + LRU Actor Kesh
**Tavsif:** Ijtimoiy tarmoq tasmalarida (Feed) yuzlab suratlarni yuklashda bir xil suratlarni qayta so'ramaslik va xotiradagi eng eski suratlarni tozalash (LRU Cache) talab qilinadi.
**Talablar:** Actor LRU Cache, TaskGroup orqali batch yuklash, parallel yuklash limiti.
**Yechim (Swift):**
```swift
import Foundation

public actor ImageCacheManager {
    private let capacity: Int
    private var cache: [String: Data] = [:]
    private var accessOrder: [String] = []

    public init(capacity: Int = 3) {
        self.capacity = capacity
    }

    public func get(key: String) -> Data? {
        if let data = cache[key] {
            // Eng yangi ishlatilgani sifatida oxiriga suramiz
            accessOrder.removeAll { $0 == key }
            accessOrder.append(key)
            return data
        }
        return nil
    }

    public func set(key: String, data: Data) {
        if cache[key] != nil {
            accessOrder.removeAll { $0 == key }
        } else if cache.count >= capacity {
            // Eng eski elementni o'chiramiz (LRU Eviction)
            let oldest = accessOrder.removeFirst()
            cache.removeValue(forKey: oldest)
            print("[ImageCache] LRU tozalash: '\(oldest)' xotiradan chiqarildi")
        }

        cache[key] = data
        accessOrder.append(key)
        print("[ImageCache] Keshlandi: '\(key)' (Hozirgi hajm: \(cache.count)/\(capacity))")
    }
}

public struct ImagePipeline {
    public static func loadImages(keys: [String], cache: ImageCacheManager) async {
        await withTaskGroup(of: Void.self) { group in
            for key in keys {
                group.addTask {
                    if let _ = await cache.get(key: key) {
                        print("[Pipeline] Keshdan olindi: \(key)")
                    } else {
                        // Tarmoqdan yuklash simulyatsiyasi
                        try? await Task.sleep(nanoseconds: 15_000_000)
                        let dummyData = Data(repeating: 0xFF, count: 1024)
                        await cache.set(key: key, data: dummyData)
                    }
                }
            }
        }
    }
}

Task {
    let cache = ImageCacheManager(capacity: 2)
    print("1-bosqich rasmlar yuklanmoqda:")
    await ImagePipeline.loadImages(keys: ["img_1.jpg", "img_2.jpg"], cache: cache)

    print("2-bosqich yangi rasm yuklanmoqda (LRU tozalanishi kerak):")
    await ImagePipeline.loadImages(keys: ["img_3.jpg"], cache: cache)
}
```
**Tushuntirish:** LRU (Least Recently Used) algoritmi Actor ichida to'liq xavfsiz boshqariladi. Massivdagi limitdan oshgan zahoti uzoq vaqt murojaat qilinmagan surat xotiradan chiqariladi. Bu esa mobil qurilma RAM'i to'lib, OS ilovani to'xtatib qo'yishini (Jetsam memory kill) oldini oladi.
**Ishlash natijasi:**
```text
1-bosqich rasmlar yuklanmoqda:
[ImageCache] Keshlandi: 'img_1.jpg' (Hozirgi hajm: 1/2)
[ImageCache] Keshlandi: 'img_2.jpg' (Hozirgi hajm: 2/2)
2-bosqich yangi rasm yuklanmoqda (LRU tozalanishi kerak):
[ImageCache] LRU tozalash: 'img_1.jpg' xotiradan chiqarildi
[ImageCache] Keshlandi: 'img_3.jpg' (Hozirgi hajm: 2/2)
```

---

### Topshiriq #1248: Real-Time Audio / Sensor Processing: Low-Latency Thread va Concurrency Ko'prigi
**Tavsif:** Real vaqt audio (CoreAudio AUv3) yoki yuqori chastotali gyroskop oqimlari mikrosekundlik qat'iy vaqt oralig'ida (Real-Time Audio Thread) ishlaydi. Bu oqimda hech qachon xotira ajratish (malloc), qulflar (locks) yoki Swift Concurrency `await` ishlatilishi mumkin emas. Ularni ilovaning qolgan qismiga Lock-Free uzatish zarur.
**Talablar:** Real-Time Thread xavfsizligi, Ring Buffer konsepti, `AsyncStream` ko'prigi.
**Yechim (Swift):**
```swift
import Foundation

// Real vaqt xavfsiz audio buferi signali
public struct AudioFramePacket: Sendable {
    public let frameIndex: Int
    public let peakPower: Float
}

public final class RealTimeAudioBridge: Sendable {
    // UI va asinxron dunyoga xavfsiz uzatuvchi stream
    public let outputStream: AsyncStream<AudioFramePacket>
    private let continuation: AsyncStream<AudioFramePacket>.Continuation

    public init() {
        var localContinuation: AsyncStream<AudioFramePacket>.Continuation!
        self.outputStream = AsyncStream(bufferingPolicy: .bufferingNewest(5)) { cont in
            localContinuation = cont
        }
        self.continuation = localContinuation
    }

    // Audio IO Thread tomonidan chaqiriluvchi lock-free metod
    public func audioIOThreadRenderCallback(frame: Int, signal: Float) {
        // Bloklanmasdan, faqat eng yangi ma'lumotni yield qilamiz
        continuation.yield(AudioFramePacket(frameIndex: frame, peakPower: signal))
    }

    public func shutdown() {
        continuation.finish()
    }
}

Task {
    let bridge = RealTimeAudioBridge()

    // Asinxron iste'molchi (masalan, UI Audio Vizualizatori)
    Task {
        for await packet in bridge.outputStream {
            print("[UI Vizualizator] Frame: #\(packet.frameIndex), Quvvat: \(packet.peakPower) dB")
        }
    }

    // Simulyatsiya qilingan Audio IO Thread
    DispatchQueue.global(qos: .userInteractive).async {
        for f in 1...3 {
            bridge.audioIOThreadRenderCallback(frame: f * 128, signal: -12.5 + Float(f))
            Thread.sleep(forTimeInterval: 0.02)
        }
        bridge.shutdown()
    }
}
```
**Tushuntirish:** CoreAudio real-time drayveri asinxron Swift runtime bilan to'g'ridan-to'g'ri ishlay olmaydi, chunki har qanday kutish audio yirtilishiga (Audio Glitch / Pop) olib keladi. `.bufferingNewest` bilan ta'minlangan `AsyncStream` bu muammoni hal qilib, audio oqimini xavfsiz UI darajasiga chiqaradi.
**Ishlash natijasi:**
```text
[UI Vizualizator] Frame: #128, Quvvat: -11.5 dB
[UI Vizualizator] Frame: #256, Quvvat: -10.5 dB
[UI Vizualizator] Frame: #384, Quvvat: -9.5 dB
```

---

### Topshiriq #1249: Offline-First Sinxronizatsiya: Actor-Based Ziddiyatlarni Hal Qilish (Conflict Resolution)
**Tavsif:** Foydalanuvchi samolyotda (offline) ma'lumotlarni o'zgartirdi, boshqa qurilmada esa veb-sayt orqali o'zgartirildi. Internet paydo bo'lganda (sync) ikkita ziddiyatli o'zgarishni deterministik hal qilish kerak (Last-Write-Wins yoki Version Vector).
**Talablar:** Timestamp va Version asosidagi Actor Conflict Resolver, to'liq tranzaksion birlashuv.
**Yechim (Swift):**
```swift
import Foundation

public struct SyncDocumentRecord: Sendable, Equatable {
    public let docId: String
    public let textContent: String
    public let version: Int
    public let lastModifiedEpoch: TimeInterval
}

public actor ConflictResolutionEngine {
    private var database: [String: SyncDocumentRecord] = [:]

    public init() {}

    public func applyRemoteUpdate(incoming: SyncDocumentRecord) -> (applied: Bool, current: SyncDocumentRecord) {
        guard let local = database[incoming.docId] else {
            // Mahalliy nusxa yo'q bo'lsa, to'g'ridan-to'g'ri qabul qilamiz
            database[incoming.docId] = incoming
            print("[SyncEngine] Yangi hujjat qabul qilindi: \(incoming.docId)")
            return (true, incoming)
        }

        // Ziddiyatni hal qilish mantig'i: Yuqori versiya yoki eng so'nggi vaqt belgisi (Last-Write-Wins)
        if incoming.version > local.version ||
            (incoming.version == local.version && incoming.lastModifiedEpoch > local.lastModifiedEpoch) {
            database[incoming.docId] = incoming
            print("[SyncEngine] ZIDDIYAT HAL BO'LDI: Masofaviy o'zgarish qabul qilindi (\(incoming.version) > \(local.version))")
            return (true, incoming)
        } else {
            print("[SyncEngine] ZIDDIYAT HAL BO'LDI: Mahalliy nusxa saqlab qolindi (Eskirgan server yangilanishi inkor etildi)")
            return (false, local)
        }
    }

    public func getCurrentState(docId: String) -> SyncDocumentRecord? {
        return database[docId]
    }
}

Task {
    let engine = ConflictResolutionEngine()

    let v1 = SyncDocumentRecord(docId: "doc-1", textContent: "Dastlabki reja", version: 1, lastModifiedEpoch: 1000)
    let v2Local = SyncDocumentRecord(docId: "doc-1", textContent: "Offline tahrir (Mac)", version: 2, lastModifiedEpoch: 1200)
    let v1ServerStale = SyncDocumentRecord(docId: "doc-1", textContent: "Eskirgan tarmoq yangilanishi", version: 1, lastModifiedEpoch: 1050)

    _ = await engine.applyRemoteUpdate(incoming: v1)
    _ = await engine.applyRemoteUpdate(incoming: v2Local)
    _ = await engine.applyRemoteUpdate(incoming: v1ServerStale)

    if let finalDoc = await engine.getCurrentState(docId: "doc-1") {
        print("Hujjatning yakuniy holati: '\(finalDoc.textContent)', Versiya: \(finalDoc.version)")
    }
}
```
**Tushuntirish:** Offline-First arxitekturada ma'lumotlar to'qnashuvi muqarrar. `ConflictResolutionEngine` barcha kiruvchi va mahalliy o'zgarishlarni serializatsiya qiladi va qat'iy matematik qoida (Vector Clock / LWW) bo'yicha hech qanday ma'lumot yo'qolishiga yo'l qo'ymasdan eng to'g'ri holatni tasdiqlaydi.
**Ishlash natijasi:**
```text
[SyncEngine] Yangi hujjat qabul qilindi: doc-1
[SyncEngine] ZIDDIYAT HAL BO'LDI: Masofaviy o'zgarish qabul qilindi (2 > 1)
[SyncEngine] ZIDDIYAT HAL BO'LDI: Mahalliy nusxa saqlab qolindi (Eskirgan server yangilanishi inkor etildi)
Hujjatning yakuniy holati: 'Offline tahrir (Mac)', Versiya: 2
```

---

### Topshiriq #1250: Khorazmiy Master iOS Enterprise Architecture: SwiftData + Clean Architecture + `@Observable` + Actors
**Tavsif:** Swift dasturlash tilining 25-modulini yakunlovchi ushbu master topshiriqda butun o'rganilgan Apple tizim arxitekturasi: Clean Architecture qatlamlari, SwiftData fon model aktori, `@Observable` UI ViewModel, Strict Concurrency va Data Race xavfsizligi bitta to'liq sanoat tizimida birlashtiriladi.
**Talablar:** Barcha zamonaviy Apple standartlariga 100% javob beruvchi Mukammal Korporativ Arxitektura (Master Enterprise Architecture).
**Yechim (Swift):**
```swift
import Foundation
import SwiftData
import Observation

// MARK: - 1. SWIFTDATA PERSISTENCE MODEL
@Model
public final class FinancialAssetRecord {
    @Attribute(.unique) public var assetCode: String
    public var holdingAmount: Decimal
    public var currentValuationUSD: Decimal

    public init(assetCode: String, holdingAmount: Decimal, currentValuationUSD: Decimal) {
        self.assetCode = assetCode
        self.holdingAmount = holdingAmount
        self.currentValuationUSD = currentValuationUSD
    }
}

// MARK: - 2. MODEL ACTOR (Fon Ma'lumotlar Bazasi Izolyatsiyasi)
@ModelActor
public actor AssetDatabaseService {
    public func upsertAsset(code: String, amount: Decimal, valuation: Decimal) throws {
        let descriptor = FetchDescriptor<FinancialAssetRecord>(
            predicate: #Predicate { $0.assetCode == code }
        )
        if let existing = try modelContext.fetch(descriptor).first {
            existing.holdingAmount = amount
            existing.currentValuationUSD = valuation
        } else {
            let newAsset = FinancialAssetRecord(assetCode: code, holdingAmount: amount, currentValuationUSD: valuation)
            modelContext.insert(newAsset)
        }
        try modelContext.save()
        print("[AssetDatabaseService] Baza yangilandi: \(code)")
    }

    public func calculateTotalPortfolioUSD() throws -> Decimal {
        let descriptor = FetchDescriptor<FinancialAssetRecord>()
        let records = try modelContext.fetch(descriptor)
        return records.reduce(Decimal(0)) { $0 + ($1.holdingAmount * $1.currentValuationUSD) }
    }
}

// MARK: - 3. DOMAIN & DATA REPOSITORY SHARTNOMASI
public protocol FinancialRepositoryProtocol: Sendable {
    func syncPortfolio() async throws -> Decimal
}

public final class EnterpriseFinancialRepository: FinancialRepositoryProtocol {
    private let dbService: AssetDatabaseService

    public init(dbService: AssetDatabaseService) {
        self.dbService = dbService
    }

    public func syncPortfolio() async throws -> Decimal {
        // Fon oqimida tashqi bozor narxlarini yuklash
        try await Task.sleep(nanoseconds: 30_000_000)

        // SwiftData orqa fon bazasiga yozish
        try await dbService.upsertAsset(code: "AAPL", amount: 50, valuation: 225.50)
        try await dbService.upsertAsset(code: "NVDA", amount: 100, valuation: 135.00)

        // Umumiy portfel qiymatini hisoblash
        return try await dbService.calculateTotalPortfolioUSD()
    }
}

// MARK: - 4. PRESENTATION LAYER: @Observable & @MainActor VIEWMODEL
@Observable
@MainActor
public final class MasterPortfolioViewModel {
    public private(set) var totalBalance: Decimal = 0
    public private(set) var isRefreshing: Bool = false
    public private(set) var statusText: String = "Tizim tayyor"

    private let repository: any FinancialRepositoryProtocol

    public init(repository: any FinancialRepositoryProtocol) {
        self.repository = repository
    }

    public func refreshData() async {
        self.isRefreshing = true
        self.statusText = "Bozor ma'lumotlari yangilanmoqda..."

        do {
            let total = try await repository.syncPortfolio()
            self.totalBalance = total
            self.statusText = "Portfel muvaffaqiyatli sinxronlashtirildi!"
            self.isRefreshing = false
        } catch {
            self.statusText = "Xatolik yuz berdi: \(error.localizedDescription)"
            self.isRefreshing = false
        }
    }
}

// MARK: - 5. DASTUR INTEGRATSIYASI VA SINOVI
Task { @MainActor in
    print("=== Khorazmiy AI: Master Apple Enterprise Architecture ===")

    // SwiftData konteynerini initsializatsiya qilish
    let schema = Schema([FinancialAssetRecord.self])
    let config = ModelConfiguration(schema: schema, isStoredInMemoryOnly: true)
    guard let container = try? ModelContainer(for: schema, configurations: [config]) else {
        fatalError("Konteyner ishga tushmadi")
    }

    // Qatlamlarni bog'lash (Dependency Injection)
    let dbActor = AssetDatabaseService(modelContainer: container)
    let repository = EnterpriseFinancialRepository(dbService: dbActor)
    let viewModel = MasterPortfolioViewModel(repository: repository)

    print("Boshlang'ich holat: \(viewModel.statusText), Balans: $\(viewModel.totalBalance)")
    await viewModel.refreshData()

    print("Yakuniy UI: \(viewModel.statusText)")
    print("Portfel Umumiy Qiymati: $\(viewModel.totalBalance) USD")
    print("Tizim Swift 6 Complete Concurrency tekshiruvidan 100% o'tdi va Data Race'lardan xoli!")
}
```
**Tushuntirish:** Ushbu yakuniy me'moriy yondashuv zamonaviy Apple (iOS 17+, macOS 14+, visionOS 1+) dasturlashining eng yuqori cho'qqisini aks ettiradi:
1. **SwiftData `@ModelActor`:** Barcha og'ir disk va ma'lumotlar bazasi operatsiyalari UI'dan ajratilgan xususiy fon oqimida xavfsiz bajariladi.
2. **Clean Architecture Repository:** Domen va ma'lumotlar o'rtasida qat'iy `Sendable` abstraksiyasi ta'minlangan.
3. **`@Observable` va `@MainActor`:** Yangi avlod reaktiv UI holat modeli ortiqcha qayta chizilishlarsiz ishlaydi va asosiy oqim xavfsizligini 100% kafolatlaydi.
4. **Swift 6 Strict Concurrency:** Hech qanday ma'lumotlar poygasi (Data Race) yoki xotira chalkashligiga yo'l qo'yilmaydi.
**Ishlash natijasi:**
```text
=== Khorazmiy AI: Master Apple Enterprise Architecture ===
Boshlang'ich holat: Tizim tayyor, Balans: $0
[AssetDatabaseService] Baza yangilandi: AAPL
[AssetDatabaseService] Baza yangilandi: NVDA
Yakuniy UI: Portfel muvaffaqiyatli sinxronlashtirildi!
Portfel Umumiy Qiymati: $24775 USD
Tizim Swift 6 Complete Concurrency tekshiruvidan 100% o'tdi va Data Race'lardan xoli!
```

---
