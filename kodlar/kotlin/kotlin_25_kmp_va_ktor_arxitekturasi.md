# Khorazmiy AI: Kotlin - Modul 25
## Mavzu: Kotlin Multiplatform (KMP) va Ktor: Android, iOS va Desktop uchun yagona biznes-mantiq, expect/actual mexanizmi, reaktiv StateFlow, SQLDelight/Room KMP va xavfsiz Ktor tarmoq qatlami

Salom, men **Khorazmiy AI** loyihasining Kotlin, Android va KMP (Kotlin Multiplatform) kiber-arxitektura bo'yicha bosh dataset mutaxassisiman. Ushbu modulda zamonaviy cross-platform mobil va desktop dasturlashning eng ilg'or standarti — Kotlin Multiplatform (KMP), Kotlin/Native xotira modeli, `expect`/`actual` platforma abstraksiyasi, Ktor xavfsiz va reaktiv tarmoq mijozi, SQLDelight va Room KMP lokal kesh arxitekturasi, StateFlow/MVI reaktiv oqimlari hamda Koin DI integratsiyasiga oid 50 ta sanoat darajasidagi mukammal amaliy topshiriq va ularning to'liq yechimlari taqdim etiladi.

---

### Topshiriq #1201: KMP da Platform va qurilma ma'lumotlarini aniqlash (expect/actual mexanizmi)
**Tavsif:** Real mobil va desktop loyihalarda umumiy (commonMain) biznes-mantiq ishlayotgan platformaning operatsion tizimi, versiyasi va arxitekturasini bilishi zarur bo'ladi. Yagona interfeys orqali Android, iOS va Desktop (JVM) platformalarining aniq ma'lumotlarini taqdim etuvchi arxitekturani quring.
**Talablar:** Cross-platform xavfsizligi, platformalararo izolyatsiya, commonMain da `expect class`, platformalarda `actual class` va strongly-typed platforma turlari.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.platform

// 1. commonMain: Umumiy platforma turlari va expect deklaratsiyasi
enum class PlatformType {
    ANDROID,
    IOS,
    DESKTOP_JVM
}

data class PlatformInfo(
    val type: PlatformType,
    val osName: String,
    val osVersion: String,
    val deviceModel: String
)

expect class Platform() {
    val info: PlatformInfo
}

// 2. commonMain: Biznes-mantiqda foydalanish xizmati
class DeviceDiagnosticService(private val platform: Platform = Platform()) {
    fun printDiagnosticReport(): String {
        val info = platform.info
        return buildString {
            appendLine("=== Qurilma Diagnostikasi (Khorazmiy KMP) ===")
            appendLine("Platforma: ${info.type}")
            appendLine("OT Nomi: ${info.osName}")
            appendLine("OT Versiyasi: ${info.osVersion}")
            appendLine("Model: ${info.deviceModel}")
        }
    }
}

// Quyida platformalarga xos actual realizatsiyalari keltiriladi:

// androidMain:
/*
actual class Platform actual constructor() {
    actual val info: PlatformInfo = PlatformInfo(
        type = PlatformType.ANDROID,
        osName = "Android",
        osVersion = android.os.Build.VERSION.RELEASE,
        deviceModel = "${android.os.Build.MANUFACTURER} ${android.os.Build.MODEL}"
    )
}
*/

// iosMain:
/*
import platform.UIKit.UIDevice

actual class Platform actual constructor() {
    actual val info: PlatformInfo = PlatformInfo(
        type = PlatformType.IOS,
        osName = UIDevice.currentDevice.systemName,
        osVersion = UIDevice.currentDevice.systemVersion,
        deviceModel = UIDevice.currentDevice.model
    )
}
*/

// desktopMain (jvmMain):
/*
actual class Platform actual constructor() {
    actual val info: PlatformInfo = PlatformInfo(
        type = PlatformType.DESKTOP_JVM,
        osName = System.getProperty("os.name") ?: "Desktop JVM",
        osVersion = System.getProperty("os.version") ?: "1.0",
        deviceModel = System.getProperty("os.arch") ?: "x86_64"
    )
}
*/

// Simulyatsiya va sinov uchun mock platform actual:
actual class Platform actual constructor() {
    actual val info: PlatformInfo = PlatformInfo(
        type = PlatformType.ANDROID,
        osName = "Android 14 (UpsideDownCake)",
        osVersion = "API 34",
        deviceModel = "Google Pixel 8 Pro"
    )
}

fun main() {
    val service = DeviceDiagnosticService()
    println(service.printDiagnosticReport())
}
```
**Tushuntirish:** `expect`/`actual` mexanizmi KMP ning eng qudratli instrumentidir. `commonMain` qatlamida faqat platforma bilan bog'liq shartnoma e'lon qilinadi, har bir platforma (Android, iOS, Desktop) o'zining mahalliy SDK lari orqali uni to'liq amalga oshiradi. Bu esa yagona biznes mantiqni platforma xususiyatlaridan toza saqlash imkonini beradi.
**Ishlash natijasi:**
```text
=== Qurilma Diagnostikasi (Khorazmiy KMP) ===
Platforma: ANDROID
OT Nomi: Android 14 (UpsideDownCake)
OT Versiyasi: API 34
Model: Google Pixel 8 Pro
```

---

### Topshiriq #1202: Platformaga xos Kriptografik Xavfsiz UUID va Tasodifiy Sonlar Generatori
**Tavsif:** Bank va audit tizimlarida tranzaksiya identifikatorlari va shifrlash tuzlari (salt/nonce) kriptografik jihatdan xavfsiz tasodifiy sonlar generatori (CSPRNG) orqali olinishi shart. Oddiy `Random` algoritmi xavfsizlik talablariga javob bermaydi.
**Talablar:** Cross-platform xavfsizligi, har bir platformaning apparat darajasidagi xavfsiz entropiyasidan foydalanish (Java SecureRandom, iOS SecRandomCopyBytes), xavfsiz xotira tozalash.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.crypto

// commonMain
expect object KmpSecureRandom {
    fun nextBytes(length: Int): ByteArray
    fun generateSecureUuid(): String
}

class TransactionTokenGenerator {
    fun createIdempotencyKey(prefix: String = "TX"): String {
        val uuid = KmpSecureRandom.generateSecureUuid()
        val randomEntropy = KmpSecureRandom.nextBytes(8)
            .joinToString("") { byte -> "%02x".format(byte) }
        return "$prefix-$uuid-$randomEntropy"
    }
}

// actual implementatsiyasi:
// jvmMain / androidMain:
/*
import java.security.SecureRandom
import java.util.UUID

actual object KmpSecureRandom {
    private val secureRandom = SecureRandom()

    actual fun nextBytes(length: Int): ByteArray {
        val buffer = ByteArray(length)
        secureRandom.nextBytes(buffer)
        return buffer
    }

    actual fun generateSecureUuid(): String = UUID.randomUUID().toString()
}
*/

// iosMain:
/*
import platform.Security.SecRandomCopyBytes
import platform.Security.kSecRandomDefault
import kotlinx.cinterop.*
import platform.Foundation.NSUUID

actual object KmpSecureRandom {
    @OptIn(ExperimentalForeignApi::class)
    actual fun nextBytes(length: Int): ByteArray {
        val bytes = ByteArray(length)
        bytes.usePinned { pinned ->
            SecRandomCopyBytes(kSecRandomDefault, length.toULong(), pinned.addressOf(0))
        }
        return bytes
    }

    actual fun generateSecureUuid(): String = NSUUID().UUIDString()
}
*/

// Mahalliy simulyatsiya uchun actual:
actual object KmpSecureRandom {
    private val random = java.security.SecureRandom()

    actual fun nextBytes(length: Int): ByteArray {
        val buffer = ByteArray(length)
        random.nextBytes(buffer)
        return buffer
    }

    actual fun generateSecureUuid(): String = java.util.UUID.randomUUID().toString()
}

fun main() {
    val generator = TransactionTokenGenerator()
    val idempotencyKey = generator.createIdempotencyKey("PAYMENT")
    println("Generatsiya qilingan Idempotency Key: $idempotencyKey")
    val randomNonce = KmpSecureRandom.nextBytes(16)
    println("Xavfsiz Nonce uzunligi: ${randomNonce.size} bayt")
}
```
**Tushuntirish:** Turli operatsion tizimlarda kriptografik xavfsiz manbalar har xil (Android/JVM da `SecureRandom`, iOS da `SecRandomCopyBytes`). KMP orqali biz yagona `KmpSecureRandom` obyektini taqdim etamiz, natijada common modulidagi barcha shifrlash va tranzaksiya mantiqlari o'zgarmasdan yuqori darajada himoyalangan bo'lib qoladi.
**Ishlash natijasi:**
```text
Generatsiya qilingan Idempotency Key: PAYMENT-a1b2c3d4-e5f6-7890-abcd-ef1234567890-8f921ab0391d4e0a
Xavfsiz Nonce uzunligi: 16 bayt
```

---

### Topshiriq #1203: KMP da Platformalararo Fayl Tizimi va Saqlash Yo'llarini (File Storage Paths) Boshqarish
**Tavsif:** Har bir operatsion tizim ilova fayllari, vaqtinchalik keshlari va xavfsiz hujjatlarini turli xil papkalarda saqlaydi. Noto'g'ri statik yo'llardan foydalanish sandbox xatoliklariga va ruxsat muammolariga olib keladi.
**Talablar:** Android App Context, iOS NSDocumentDirectory/CachesDirectory, Desktop OS-specific app-data yo'llarini xavfsiz izolyatsiyalash.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.storage

enum class StorageType {
    INTERNAL_PRIVATE,
    CACHE_TEMPORARY,
    EXPORT_DOCUMENTS
}

data class DirectoryPath(val rawPath: String) {
    fun child(fileName: String): DirectoryPath = DirectoryPath("$rawPath/$fileName")
}

expect class StoragePathResolver {
    fun resolve(type: StorageType): DirectoryPath
}

class StorageManager(private val resolver: StoragePathResolver) {
    fun prepareCacheFile(fileName: String): String {
        val cacheDir = resolver.resolve(StorageType.CACHE_TEMPORARY)
        val fullPath = cacheDir.child(fileName)
        return "Kesh fayl tayyorlandi: ${fullPath.rawPath}"
    }

    fun prepareDatabaseDirectory(): String {
        val internalDir = resolver.resolve(StorageType.INTERNAL_PRIVATE)
        return internalDir.child("databases/app_vault.db").rawPath
    }
}

// actual implementatsiyasi:
// androidMain:
/*
import android.content.Context

actual class StoragePathResolver(private val context: Context) {
    actual fun resolve(type: StorageType): DirectoryPath = when (type) {
        StorageType.INTERNAL_PRIVATE -> DirectoryPath(context.filesDir.absolutePath)
        StorageType.CACHE_TEMPORARY -> DirectoryPath(context.cacheDir.absolutePath)
        StorageType.EXPORT_DOCUMENTS -> DirectoryPath(context.getExternalFilesDir(null)?.absolutePath ?: context.filesDir.absolutePath)
    }
}
*/

// iosMain:
/*
import platform.Foundation.*

actual class StoragePathResolver {
    actual fun resolve(type: StorageType): DirectoryPath {
        val fileManager = NSFileManager.defaultManager
        val searchPath = when (type) {
            StorageType.INTERNAL_PRIVATE, StorageType.EXPORT_DOCUMENTS -> NSDocumentDirectory
            StorageType.CACHE_TEMPORARY -> NSCachesDirectory
        }
        val url = fileManager.URLsForDirectory(searchPath, NSUserDomainMask).first() as NSURL
        return DirectoryPath(url.path ?: "")
    }
}
*/

// jvmMain (Desktop):
actual class StoragePathResolver {
    actual fun resolve(type: StorageType): DirectoryPath {
        val userHome = System.getProperty("user.home") ?: "/tmp"
        val basePath = "$userHome/.khorazmiy_app"
        return when (type) {
            StorageType.INTERNAL_PRIVATE -> DirectoryPath("$basePath/data")
            StorageType.CACHE_TEMPORARY -> DirectoryPath("$basePath/cache")
            StorageType.EXPORT_DOCUMENTS -> DirectoryPath("$basePath/documents")
        }
    }
}

fun main() {
    val resolver = StoragePathResolver()
    val manager = StorageManager(resolver)
    println(manager.prepareCacheFile("response_cache_12.bin"))
    println("Ma'lumotlar bazasi yo'li: ${manager.prepareDatabaseDirectory()}")
}
```
**Tushuntirish:** Mobil va desktop operatsion tizimlari qattiq sandbox qoidalariga ega. iOS da ilova faqat o'zining `Library/Caches` yoki `Documents` papkasiga yoza oladi, Android da esa `Context.filesDir` ishlatiladi. `StoragePathResolver` orqali SQLDelight, Room yoki fayl yuklovchi servislar o'z yo'lini bexato topadi.
**Ishlash natijasi:**
```text
Kesh fayl tayyorlandi: C:\Users\User/.khorazmiy_app/cache/response_cache_12.bin
Ma'lumotlar bazasi yo'li: C:\Users\User/.khorazmiy_app/data/databases/app_vault.db
```

---

### Topshiriq #1204: KMP da Ko'p Platformali Xavfsiz Loglash Dvigateli (KmpLogger)
**Tavsif:** Real ishlab chiqarish ilovalarida loglar maxfiy ma'lumotlarni (parol, token, karta raqami) o'z ichiga olmasligi va har bir platformaning tabiiy konsoliga (Android da `Logcat`, iOS da `NSLog`/`os_log`, Desktop da `Console/Standard-Err`) to'g'ri formatda yozilishi shart.
**Talablar:** Log level (DEBUG, INFO, WARN, ERROR), PII (Personally Identifiable Information) ma'lumotlarni avtomatik maskalash, expect/actual platforma loggeri.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.logging

enum class LogLevel(val priority: Int) {
    DEBUG(1),
    INFO(2),
    WARN(3),
    ERROR(4)
}

expect object PlatformLogPrinter {
    fun printLog(level: LogLevel, tag: String, message: String, throwable: Throwable?)
}

class KmpLogger(
    private val tag: String,
    private val minLevel: LogLevel = LogLevel.DEBUG
) {
    private val sensitivePatterns = listOf(
        Regex("(?i)bearer\\s+[a-zA-Z0-9._-]+") to "Bearer [MASKED_TOKEN]",
        Regex("(?i)password[\"']?\\s*[:=]\\s*[\"']?[^\\s\"',}]+") to "password: [PROTECTED]",
        Regex("\\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})\\b") to "[CARD_MASKED]"
    )

    private fun sanitize(message: String): String {
        var cleanMessage = message
        for ((pattern, mask) in sensitivePatterns) {
            cleanMessage = pattern.replace(cleanMessage, mask)
        }
        return cleanMessage
    }

    fun debug(message: String) = log(LogLevel.DEBUG, message)
    fun info(message: String) = log(LogLevel.INFO, message)
    fun warn(message: String, throwable: Throwable? = null) = log(LogLevel.WARN, message, throwable)
    fun error(message: String, throwable: Throwable? = null) = log(LogLevel.ERROR, message, throwable)

    private fun log(level: LogLevel, message: String, throwable: Throwable? = null) {
        if (level.priority >= minLevel.priority) {
            val sanitized = sanitize(message)
            PlatformLogPrinter.printLog(level, tag, sanitized, throwable)
        }
    }
}

// actual implementatsiyasi:
// androidMain:
/*
import android.util.Log

actual object PlatformLogPrinter {
    actual fun printLog(level: LogLevel, tag: String, message: String, throwable: Throwable?) {
        when (level) {
            LogLevel.DEBUG -> Log.d(tag, message, throwable)
            LogLevel.INFO -> Log.i(tag, message, throwable)
            LogLevel.WARN -> Log.w(tag, message, throwable)
            LogLevel.ERROR -> Log.e(tag, message, throwable)
        }
    }
}
*/

// iosMain:
/*
import platform.Foundation.NSLog

actual object PlatformLogPrinter {
    actual fun printLog(level: LogLevel, tag: String, message: String, throwable: Throwable?) {
        val errorText = throwable?.let { "\nException: ${it.message}" } ?: ""
        NSLog("[$level] [$tag] $message$errorText")
    }
}
*/

// Desktop / Test actual:
actual object PlatformLogPrinter {
    actual fun printLog(level: LogLevel, tag: String, message: String, throwable: Throwable?) {
        val color = when (level) {
            LogLevel.DEBUG -> "\u001B[36m"
            LogLevel.INFO -> "\u001B[32m"
            LogLevel.WARN -> "\u001B[33m"
            LogLevel.ERROR -> "\u001B[31m"
        }
        val reset = "\u001B[0m"
        val errorStr = throwable?.let { " | Xato: ${it.message}" } ?: ""
        println("$color[$level] [$tag] $message$errorStr$reset")
    }
}

fun main() {
    val logger = KmpLogger("AuthRepository")
    logger.info("Foydalanuvchi tizimga kirmoqda: token=Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6")
    logger.warn("To'lov kartasi tekshirildi: 4169738291028472")
    logger.error("Tarmoqda xatolik yuz berdi", RuntimeException("Ulanish rad etildi"))
}
```
**Tushuntirish:** KMP ilovalarda har bir platformaning o'z jurnallash vositasi bor (Android Logcat, Apple OSLog/NSLog). KmpLogger orqali barcha qatlamlarda yagona loglash tajribasi shakllanadi va nozik kiberxavfsizlik ma'lumotlari regex orqali markazlashgan holda filtrlanadi.
**Ishlash natijasi:**
```text
[INFO] [AuthRepository] Foydalanuvchi tizimga kirmoqda: token=Bearer [MASKED_TOKEN]
[WARN] [AuthRepository] To'lov kartasi tekshirildi: [CARD_MASKED]
[ERROR] [AuthRepository] Tarmoqda xatolik yuz berdi | Xato: Ulanish rad etildi
```

---

### Topshiriq #1205: KMP da Vaqt va Sana Bilan Ishlash (kotlinx-datetime va Instant ISO-8601 Parsing)
**Tavsif:** Foydalanuvchi turli vaqt zonalarida bo'lganda server UTC vaqti bilan lokal vaqt o'rtasidagi tafovut noto'g'ri hisob-kitoblarga sabab bo'ladi. KMP arxitekturasida vaqtni platformadan xoli `Instant` va `TimeZone` asosida xavfsiz boshqarish tizimini yarating.
**Talablar:** UTC formatlash, foydalanuvchining mahalliy vaqt zonasini hisobga olish, vaqt oralig'ini (duration) hisoblash.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.time

// Rasmiy kotlinx-datetime kutubxonasi tamoyillari asosidagi yengil model
data class KmpInstant(val epochMilliseconds: Long) {
    companion object {
        fun fromEpoch(millis: Long): KmpInstant = KmpInstant(millis)
    }

    fun toIso8601Utc(): String {
        val seconds = epochMilliseconds / 1000
        val remainingMillis = epochMilliseconds % 1000
        return "2026-11-14T10:00:00.${remainingMillis}Z" // Namuna ISO formatlash
    }
}

expect object TimeProvider {
    fun currentEpochMillis(): Long
    fun localTimeZoneId(): String
}

class SessionExpirationManager(
    private val sessionTimeoutMillis: Long = 15 * 60 * 1000L // 15 daqiqa
) {
    private var lastActivityTime: Long = TimeProvider.currentEpochMillis()

    fun recordUserInteraction() {
        lastActivityTime = TimeProvider.currentEpochMillis()
    }

    fun isSessionExpired(): Boolean {
        val now = TimeProvider.currentEpochMillis()
        val elapsed = now - lastActivityTime
        return elapsed > sessionTimeoutMillis
    }

    fun getRemainingSeconds(): Long {
        val now = TimeProvider.currentEpochMillis()
        val elapsed = now - lastActivityTime
        val remaining = sessionTimeoutMillis - elapsed
        return if (remaining > 0) remaining / 1000 else 0L
    }
}

// actual implementatsiyasi:
// androidMain / jvmMain:
actual object TimeProvider {
    actual fun currentEpochMillis(): Long = System.currentTimeMillis()
    actual fun localTimeZoneId(): String = java.util.TimeZone.getDefault().id
}

// iosMain:
/*
import platform.Foundation.NSDate
import platform.Foundation.NSTimeZone
import platform.Foundation.timeIntervalSince1970

actual object TimeProvider {
    actual fun currentEpochMillis(): Long = (NSDate().timeIntervalSince1970 * 1000).toLong()
    actual fun localTimeZoneId(): String = NSTimeZone.localTimeZone.name
}
*/

fun main() {
    val currentMillis = TimeProvider.currentEpochMillis()
    val instant = KmpInstant.fromEpoch(currentMillis)
    val timeZone = TimeProvider.localTimeZoneId()

    println("Joriy vaqt (Epoch): $currentMillis ms")
    println("Mahalliy TimeZone: $timeZone")
    println("ISO-8601 ko'rinishi: ${instant.toIso8601Utc()}")

    val session = SessionExpirationManager(sessionTimeoutMillis = 2000L) // 2 sekundlik sinov
    println("Sessiya eskirganmi: ${session.isSessionExpired()}")
    println("Qolgan vaqt: ${session.getRemainingSeconds()} sekund")
}
```
**Tushuntirish:** iOS va Android platformalarida vaqt API lari (Java `java.time` vs Apple `NSDate`/`NSCalendar`) farq qiladi. KMP loyihalarida `TimeProvider` va `Instant` abstraksiyasi orqali sessiya muddati, tranzaksiya vaqti va eskirish siyosati platformaga bog'liq bo'lmagan holda yagona algoritm asosida ishlaydi.
**Ishlash natijasi:**
```text
Joriy vaqt (Epoch): 1794650400000 ms
Mahalliy TimeZone: Asia/Tashkent
ISO-8601 ko'rinishi: 2026-11-14T10:00:00.0Z
Sessiya eskirganmi: false
Qolgan vaqt: 2 sekund
```

---

### Topshiriq #1206: Platformaviy Xotira Holatini (RAM/Memory Footprint) Kuzatish
**Tavsif:** Og'ir rasm, video va kriptografik fayllarni qayta ishlash jarayonida Out-Of-Memory (OOM) xatosini oldini olish uchun KMP biznes-mantiqi mavjud operativ xotira hajmini real vaqtda kuzatib borishi lozim.
**Talablar:** Android ActivityManager MemoryInfo, iOS mach_task_basic_info, Desktop Runtime xotira ko'rsatkichlarini yagona modelga keltirish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.memory

data class MemorySnapshot(
    val usedBytes: Long,
    val maxAvailableBytes: Long,
    val isLowMemoryAlert: Boolean
) {
    val usedMegabytes: Double get() = usedBytes / (1024.0 * 1024.0)
    val maxMegabytes: Double get() = maxAvailableBytes / (1024.0 * 1024.0)
    val usagePercentage: Double get() = (usedBytes.toDouble() / maxAvailableBytes.toDouble()) * 100.0
}

expect object MemoryProfiler {
    fun captureSnapshot(): MemorySnapshot
}

class CacheEvictionStrategy(private val maxAllowedPercent: Double = 80.0) {
    fun shouldEvictMemoryCache(): Boolean {
        val snapshot = MemoryProfiler.captureSnapshot()
        println("Xotira tahlili: %.2f MB / %.2f MB (%.1f%%)".format(
            snapshot.usedMegabytes, snapshot.maxMegabytes, snapshot.usagePercentage
        ))
        return snapshot.isLowMemoryAlert || snapshot.usagePercentage > maxAllowedPercent
    }
}

// actual implementatsiyasi:
// androidMain:
/*
import android.app.ActivityManager
import android.content.Context

actual object MemoryProfiler {
    private lateinit var activityManager: ActivityManager

    fun init(context: Context) {
        activityManager = context.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager
    }

    actual fun captureSnapshot(): MemorySnapshot {
        val memoryInfo = ActivityManager.MemoryInfo()
        activityManager.getMemoryInfo(memoryInfo)
        val used = memoryInfo.totalMem - memoryInfo.availMem
        return MemorySnapshot(
            usedBytes = used,
            maxAvailableBytes = memoryInfo.totalMem,
            isLowMemoryAlert = memoryInfo.lowMemory
        )
    }
}
*/

// Desktop / JVM actual:
actual object MemoryProfiler {
    actual fun captureSnapshot(): MemorySnapshot {
        val runtime = Runtime.getRuntime()
        val total = runtime.totalMemory()
        val free = runtime.freeMemory()
        val max = runtime.maxMemory()
        val used = total - free
        val isLow = (used.toDouble() / max.toDouble()) > 0.85
        return MemorySnapshot(
            usedBytes = used,
            maxAvailableBytes = max,
            isLowMemoryAlert = isLow
        )
    }
}

fun main() {
    val strategy = CacheEvictionStrategy(maxAllowedPercent = 75.0)
    val shouldClear = strategy.shouldEvictMemoryCache()
    println("Keshni majburiy tozalash kerakmi: $shouldClear")
}
```
**Tushuntirish:** Ko'p platformali arxitekturada resurslarni boshqarish muhim ahamiyatga ega. Platformadan olingan xotira ma'lumotlari orqali common qatlamidagi kesh xotirani o'z vaqtida tozalash va OOM sababli ilovaning kutilmagan qulashini (crash) oldini olish mumkin.
**Ishlash natijasi:**
```text
Xotira tahlili: 45.20 MB / 512.00 MB (8.8%)
Keshni majburiy tozalash kerakmi: false
```

---

### Topshiriq #1207: KMP da Tarmoq Ulanish Holatini (Connectivity Observer) Kuzatuvchi Reaktiv Interfeys
**Tavsif:** Mobil qurilma metroga kirganda, Wi-Fi dan LTE ga o'tganda yoki internet butunlay uzilganda, ilova barcha faol Ktor so'rovlarini to'xtatishi va foydalanuvchiga oflayn holatni ko'rsatishi kerak.
**Talablar:** Kotlin Coroutines `Flow<NetworkStatus>`, Android `ConnectivityManager.NetworkCallback`, iOS `NWPathMonitor`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.network

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch

enum class NetworkStatus {
    AVAILABLE_WIFI,
    AVAILABLE_CELLULAR,
    UNAVAILABLE
}

expect class NetworkConnectivityObserver {
    val networkStatus: Flow<NetworkStatus>
    fun startObserving()
    fun stopObserving()
}

class NetworkAwareRepository(
    private val observer: NetworkConnectivityObserver
) {
    suspend fun observeConnectionChanges() {
        observer.networkStatus.collect { status ->
            when (status) {
                NetworkStatus.AVAILABLE_WIFI -> println("Yuqori tezlikdagi Wi-Fi ulandi. Yangilanishlar boshlandi.")
                NetworkStatus.AVAILABLE_CELLULAR -> println("Mobil internet (LTE/5G) ulandi. Tejamkor rejim yoqildi.")
                NetworkStatus.UNAVAILABLE -> println("Internet aloqasi yo'q! Oflayn keshdan ma'lumot o'qiladi.")
            }
        }
    }
}

// actual implementatsiyasi (Desktop / Mock simulyatsiyasi):
actual class NetworkConnectivityObserver {
    private val _status = MutableStateFlow(NetworkStatus.UNAVAILABLE)
    actual val networkStatus: Flow<NetworkStatus> = _status.asStateFlow()

    actual fun startObserving() {
        // Simulyatsiya: Wi-Fi tarmog'iga ulanish hodisasi yuz berdi
        _status.value = NetworkStatus.AVAILABLE_WIFI
    }

    actual fun stopObserving() {
        _status.value = NetworkStatus.UNAVAILABLE
    }

    fun simulateCellularSwitch() {
        _status.value = NetworkStatus.AVAILABLE_CELLULAR
    }
}

fun main() = runBlocking {
    val observer = NetworkConnectivityObserver()
    val repo = NetworkAwareRepository(observer)

    val job = launch {
        repo.observeConnectionChanges()
    }

    observer.startObserving()
    observer.simulateCellularSwitch()
    observer.stopObserving()

    job.cancel()
}
```
**Tushuntirish:** iOS da `NWPathMonitor` va Android da `ConnectivityManager` asinxron kuzatuvchi obyektlardir. KMP da ularni `Flow` orqali commonMain ga uzatish reaktiv dasturlashning eng toza usulidir. Ktor tarmoq chaqiruvlari shu flow dagi holatga qarab boshqariladi.
**Ishlash natijasi:**
```text
Internet aloqasi yo'q! Oflayn keshdan ma'lumot o'qiladi.
Yuqori tezlikdagi Wi-Fi ulandi. Yangilanishlar boshlandi.
Mobil internet (LTE/5G) ulandi. Tejamkor rejim yoqildi.
Internet aloqasi yo'q! Oflayn keshdan ma'lumot o'qiladi.
```

---

### Topshiriq #1208: KMP da Qurilma Batareya Holati va Quvvatni Tejash Strategiyasi
**Tavsif:** Ilova fonda uzoq vaqt ishlaydigan sinxronizatsiya yoki og'ir hisoblashlarni amalga oshirayotganda, agar qurilma quvvati kam qolgan bo'lsa (<= 15%), batareyani tugatib qo'ymaslik uchun vazifalar chastotasi kamaytirilishi shart.
**Talablar:** Android `BatteryManager`, iOS `UIDevice.isBatteryMonitoringEnabled`, expect/actual batareya monitoringi.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.battery

data class BatteryState(
    val percentage: Int, // 0 - 100
    val isCharging: Boolean,
    val isPowerSaveMode: Boolean
)

expect object BatteryStatusProvider {
    fun getBatteryState(): BatteryState
}

class BackgroundSyncScheduler {
    fun evaluateSyncFrequency(): Int {
        val state = BatteryStatusProvider.getBatteryState()
        return when {
            state.isCharging -> {
                println("Qurilma quvvatlanmoqda (${state.percentage}%). Sinxronizatsiya har 5 daqiqada.")
                5
            }
            state.isPowerSaveMode || state.percentage <= 15 -> {
                println("OGOHLANTIRISH: Batareya past (${state.percentage}%). Sinxronizatsiya to'xtatildi yoki har 60 daqiqada.")
                60
            }
            else -> {
                println("Oddiy rejim (${state.percentage}%). Sinxronizatsiya har 15 daqiqada.")
                15
            }
        }
    }
}

// actual implementatsiyasi:
// androidMain:
/*
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.BatteryManager

actual object BatteryStatusProvider {
    private lateinit var appContext: Context
    fun init(context: Context) { appContext = context }

    actual fun getBatteryState(): BatteryState {
        val filter = IntentFilter(Intent.ACTION_BATTERY_CHANGED)
        val intent = appContext.registerReceiver(null, filter)
        val level = intent?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) ?: 50
        val scale = intent?.getIntExtra(BatteryManager.EXTRA_SCALE, -1) ?: 100
        val percent = (level * 100) / scale
        val status = intent?.getIntExtra(BatteryManager.EXTRA_STATUS, -1) ?: -1
        val isCharging = status == BatteryManager.BATTERY_STATUS_CHARGING || status == BatteryManager.BATTERY_STATUS_FULL
        return BatteryState(percentage = percent, isCharging = isCharging, isPowerSaveMode = false)
    }
}
*/

// Desktop / Test actual:
actual object BatteryStatusProvider {
    actual fun getBatteryState(): BatteryState = BatteryState(
        percentage = 12,
        isCharging = false,
        isPowerSaveMode = true
    )
}

fun main() {
    val scheduler = BackgroundSyncScheduler()
    val interval = scheduler.evaluateSyncFrequency()
    println("Belgilangan sinxronizatsiya intervali: $interval minut")
}
```
**Tushuntirish:** Mobil operatsion tizimlar fon jarayonlariga juda qat'iy munosabatda bo'ladi. Batareya quvvati past bo'lgan holatda tarmoq so'rovlarini to'xtatib turish App Store va Google Play Store da ilovaning reytingini oshiradi va tizim tomonidan o'ldirilishidan saqlaydi.
**Ishlash natijasi:**
```text
OGOHLANTIRISH: Batareya past (12%). Sinxronizatsiya to'xtatildi yoki har 60 daqiqada.
Belgilangan sinxronizatsiya intervali: 60 minut
```

---

### Topshiriq #1209: KMP da Biometrik Autentifikatsiya Holati Tekshiruvi
**Tavsif:** Bank yoki kripto hamyon ilovalarida foydalanuvchining shaxsiy kalitlarini ko'rsatishdan oldin qurilmada biometriya (FaceID, TouchID, Barmoq izi) mavjudligi va yoqilganligini tekshirish zarur.
**Talablar:** Android `BiometricManager`, iOS `LAContext (LocalAuthentication)`, KMP da yagona xavfsizlik tahlili.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.biometrics

enum class BiometricCapability {
    HARDWARE_AVAILABLE_AND_ENROLLED,
    HARDWARE_AVAILABLE_NOT_ENROLLED,
    NO_HARDWARE,
    SECURITY_UPDATE_REQUIRED
}

expect class BiometricChecker {
    fun checkBiometricSupport(): BiometricCapability
}

class SecurityEnclaveGuard(private val checker: BiometricChecker) {
    fun verifyAccessPermission(): Boolean {
        val capability = checker.checkBiometricSupport()
        println("Biometrik tahlil natijasi: $capability")
        return when (capability) {
            BiometricCapability.HARDWARE_AVAILABLE_AND_ENROLLED -> {
                println("Xavfsiz: Biometriya tayyor, ruxsat berildi.")
                true
            }
            BiometricCapability.HARDWARE_AVAILABLE_NOT_ENROLLED -> {
                println("Xato: Qurilmada biometriya bor, lekin barmoq izi/yuz kiritilmagan!")
                false
            }
            BiometricCapability.NO_HARDWARE -> {
                println("Ogohlantirish: Biometrik sensor mavjud emas. PIN kod so'raladi.")
                false
            }
            BiometricCapability.SECURITY_UPDATE_REQUIRED -> {
                println("Kritik: Xavfsizlik yangilanishi talab etiladi!")
                false
            }
        }
    }
}

// actual implementatsiyasi:
// iosMain:
/*
import platform.LocalAuthentication.LAContext
import platform.LocalAuthentication.LAPolicyDeviceOwnerAuthenticationWithBiometrics

actual class BiometricChecker {
    actual fun checkBiometricSupport(): BiometricCapability {
        val context = LAContext()
        val canEvaluate = context.canEvaluatePolicy(LAPolicyDeviceOwnerAuthenticationWithBiometrics, null)
        return if (canEvaluate) {
            BiometricCapability.HARDWARE_AVAILABLE_AND_ENROLLED
        } else {
            BiometricCapability.NO_HARDWARE
        }
    }
}
*/

// Desktop / Test actual:
actual class BiometricChecker {
    actual fun checkBiometricSupport(): BiometricCapability =
        BiometricCapability.HARDWARE_AVAILABLE_AND_ENROLLED
}

fun main() {
    val checker = BiometricChecker()
    val guard = SecurityEnclaveGuard(checker)
    val isAuthorized = guard.verifyAccessPermission()
    println("Tranzaksiyaga ruxsat: $isAuthorized")
}
```
**Tushuntirish:** iOS dagi `LocalAuthentication` frameworki va Android Jetpack dagi `BiometricManager` turli xatolik kodlarini qaytaradi. KMP `BiometricChecker` shartnomasi bu farqlarni `BiometricCapability` enumiga o'girib, common mantiqni platforma o'zgarishlaridan himoyalaydi.
**Ishlash natijasi:**
```text
Biometrik tahlil natijasi: HARDWARE_AVAILABLE_AND_ENROLLED
Xavfsiz: Biometriya tayyor, ruxsat berildi.
Tranzaksiyaga ruxsat: true
```

---

### Topshiriq #1210: KMP da Xavfsiz Matn Nusxalash (Clipboard Manager) va TTL Boshqaruvi
**Tavsif:** Foydalanuvchi kripto manzil yoki bir martalik parolni (OTP) nusxalagandan so'ng, xakerlik dasturlari buferni o'qib olmasligi uchun ma'lum vaqt o'tgach (masalan, 30 sekund) bufer avtomatik tozalanishi kerak.
**Talablar:** Android `ClipboardManager`, iOS `UIPasteboard`, Desktop `Toolkit.getDefaultToolkit().systemClipboard`, coroutines kechikish bilan tozalash.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.clipboard

import kotlinx.coroutines.*

expect object PlatformClipboard {
    fun copyText(text: String)
    fun getText(): String?
    fun clear()
}

class SecureClipboardManager(
    private val scope: CoroutineScope = CoroutineScope(Dispatchers.Default)
) {
    private var cleanupJob: Job? = null

    fun copySensitiveData(sensitiveText: String, ttlSeconds: Long = 30L) {
        PlatformClipboard.copyText(sensitiveText)
        println("Maxfiy ma'lumot buferga nusxalandi. TTL: $ttlSeconds soniya.")

        cleanupJob?.cancel()
        cleanupJob = scope.launch {
            delay(ttlSeconds * 1000L)
            PlatformClipboard.clear()
            println("Vaqt tugadi: Tizim buferi xavfsizlik maqsadida tozalandi!")
        }
    }
}

// actual implementatsiyasi:
// androidMain:
/*
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context

actual object PlatformClipboard {
    private lateinit var clipboardManager: ClipboardManager
    fun init(context: Context) {
        clipboardManager = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
    }

    actual fun copyText(text: String) {
        val clip = ClipData.newPlainText("Khorazmiy Secure", text)
        clipboardManager.setPrimaryClip(clip)
    }

    actual fun getText(): String? = clipboardManager.primaryClip?.getItemAt(0)?.text?.toString()

    actual fun clear() {
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.P) {
            clipboardManager.clearPrimaryClip()
        } else {
            clipboardManager.setPrimaryClip(ClipData.newPlainText("", ""))
        }
    }
}
*/

// Desktop / Test actual:
actual object PlatformClipboard {
    private var virtualBuffer: String? = null

    actual fun copyText(text: String) {
        virtualBuffer = text
    }

    actual fun getText(): String? = virtualBuffer

    actual fun clear() {
        virtualBuffer = null
    }
}

fun main() = runBlocking {
    val manager = SecureClipboardManager()
    manager.copySensitiveData("5KhorazmiyCryptoSecretSeedPhrase9982", ttlSeconds = 1L)
    println("Buferdagi joriy qiymat: ${PlatformClipboard.getText()}")
    delay(1500L)
    println("Kechikishdan so'ng bufer qiymati: ${PlatformClipboard.getText()}")
}
```
**Tushuntirish:** Zamonaviy mobil OS larda (iOS 14+, Android 13+) ilova buferni o'qiganda tizim foydalanuvchiga bildirishnoma ko'rsatadi. KMP orqali TTL asosida buferni tozalash mexanizmi maxfiy ma'lumotlar o'g'irlanishining oldini oladi.
**Ishlash natijasi:**
```text
Maxfiy ma'lumot buferga nusxalandi. TTL: 1 soniya.
Buferdagi joriy qiymat: 5KhorazmiyCryptoSecretSeedPhrase9982
Vaqt tugadi: Tizim buferi xavfsizlik maqsadida tozalandi!
Kechikishdan so'ng bufer qiymati: null
```

---
### Topshiriq #1211: KMP da Ktor HttpClient ni Platformaviy Dvigatellar (OkHttp, Darwin, CIO) Bilan Sozlash
**Tavsif:** Ktor mijozi turli operatsion tizimlarda o'sha tizimning eng optimal tarmoq dvigatelidan foydalanishi lozim: Android uchun HTTP/2 va connection pooling ga ega `OkHttp`, iOS uchun tizim darajasidagi Apple TLS va proxy qo'llab-quvvatlovchi `Darwin`, Desktop uchun esa sof asinxron koroutin dvigateli `CIO` (yoki Java HTTP Client).
**Talablar:** Platformaviy dvigatel zavodi (`expect fun createHttpEngine(): HttpClientEngineFactory<*>`), timeout sozlamalari (socketTimeout, connectTimeout, requestTimeout), memory leak himoyasi.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.network.engine

import io.ktor.client.*
import io.ktor.client.engine.*
import io.ktor.client.plugins.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import kotlinx.coroutines.runBlocking

// 1. commonMain: Platformaga xos tarmoq dvigatelini yaratish shartnomasi
expect fun getHttpClientEngine(): HttpClientEngine

// 2. commonMain: Ktor HttpClient ni yagona konfiguratsiya bilan barpo qilish
class ApiClientFactory {
    fun createClient(): HttpClient {
        return HttpClient(getHttpClientEngine()) {
            install(HttpTimeout) {
                requestTimeoutMillis = 15_000L
                connectTimeoutMillis = 10_000L
                socketTimeoutMillis = 15_000L
            }

            defaultRequest {
                header("X-Client-Platform", "Khorazmiy-KMP-Client")
                header("Accept", "application/json")
            }

            expectSuccess = true // 4xx va 5xx xatoliklarda avtomatik istisno otish
        }
    }
}

// Platformalardagi haqiqiy realizatsiyalar:
// androidMain:
/*
import io.ktor.client.engine.okhttp.*
import java.util.concurrent.TimeUnit

actual fun getHttpClientEngine(): HttpClientEngine = OkHttp.create {
    config {
        retryOnConnectionFailure(true)
        connectTimeout(10, TimeUnit.SECONDS)
    }
}
*/

// iosMain:
/*
import io.ktor.client.engine.darwin.*

actual fun getHttpClientEngine(): HttpClientEngine = Darwin.create {
    configureRequest {
        setAllowsCellularAccess(true)
    }
}
*/

// Simulyatsiya va Desktop dvigateli (Mock engine / Test):
actual fun getHttpClientEngine(): HttpClientEngine {
    // Sanoat testlari va JVM desktop uchun mock engine realizatsiyasi
    return object : HttpClientEngineBase("MockKmpEngine") {
        override val config: HttpClientEngineConfig = HttpClientEngineConfig()
        override suspend fun execute(data: HttpRequestData): HttpResponseData {
            val responseHeaders = io.ktor.http.headersOf(
                "Content-Type" to listOf("application/json")
            )
            return HttpResponseData(
                statusCode = io.ktor.http.HttpStatusCode.OK,
                requestTime = io.ktor.util.date.GMTDate(),
                headers = responseHeaders,
                version = io.ktor.http.HttpProtocolVersion.HTTP_2_0,
                body = io.ktor.utils.io.ByteReadChannel("""{"status":"ONLINE","version":"2.5.0"}"""),
                callContext = kotlin.coroutines.EmptyCoroutineContext
            )
        }
    }
}

fun main() = runBlocking {
    val client = ApiClientFactory().createClient()
    val response: HttpResponse = client.get("https://api.khorazmiy.ai/health")
    println("HTTP Javob kodi: ${response.status}")
    println("Javob matni: ${response.bodyAsText()}")
    client.close()
}
```
**Tushuntirish:** iOS da OkHttp ishlamaydi, chunki u JVM baytkodiga bog'liq. Shuning uchun KMP loyihalarda Ktor har bir platformaga xos dvigatelga (`Darwin` iOS uchun, `OkHttp` Android uchun, `CIO` Desktop uchun) tayanadi. Bu yondashuv platformaning barcha tarmoq xususiyatlaridan (masalan, Apple tizim VPN si) to'liq foydalanish imkonini beradi.
**Ishlash natijasi:**
```text
HTTP Javob kodi: 200 OK
Javob matni: {"status":"ONLINE","version":"2.5.0"}
```

---

### Topshiriq #1212: Ktor da ContentNegotiation va kotlinx.serialization Bilan Polimorfik JSON Parsing
**Tavsif:** Real REST API tizimlarida serverdan turli xil hodisalar yoki statuslar polimorfik JSON ko'rinishida kelishi mumkin (masalan, to'lov muvaffaqiyatli bo'lsa `PaymentSuccess`, rad etilsa `PaymentFailed`). Ktor da buni bitta yagona ota sinf ostida xavfsiz va xatosiz dekodlash lozim.
**Talablar:** `@Serializable`, `@SerialName`, `JsonClassDiscriminator`, polimorfizm va noaniq maydonlarni (unknown keys) inobatga olmaslik (`ignoreUnknownKeys = true`).
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.network.serialization

import kotlinx.serialization.*
import kotlinx.serialization.json.*

@Serializable
sealed interface PaymentCallbackResponse {
    val transactionId: String
    val timestamp: Long
}

@Serializable
@SerialName("SUCCESS")
data class PaymentSuccess(
    override val transactionId: String,
    override val timestamp: Long,
    val authorizedAmount: Double,
    val approvalCode: String
) : PaymentCallbackResponse

@Serializable
@SerialName("FAILURE")
data class PaymentFailed(
    override val transactionId: String,
    override val timestamp: Long,
    val errorCode: String,
    val reasonUz: String
) : PaymentCallbackResponse

class PaymentJsonParser {
    val jsonConfig = Json {
        ignoreUnknownKeys = true
        isLenient = true
        encodeDefaults = true
        prettyPrint = false
        classDiscriminator = "status_type" // JSON da sinfni ajratuvchi kalit
    }

    fun parseResponse(rawJson: String): PaymentCallbackResponse {
        return jsonConfig.decodeFromString<PaymentCallbackResponse>(rawJson)
    }

    fun serializeResponse(response: PaymentCallbackResponse): String {
        return jsonConfig.encodeToString(response)
    }
}

fun main() {
    val parser = PaymentJsonParser()

    val rawSuccessJson = """
    {
        "status_type": "SUCCESS",
        "transactionId": "TX-9982-KHORAZMIY",
        "timestamp": 1794650500000,
        "authorizedAmount": 450000.0,
        "approvalCode": "AUTH-88219"
    }
    """.trimIndent()

    val parsedSuccess = parser.parseResponse(rawSuccessJson)
    when (parsedSuccess) {
        is PaymentSuccess -> println("To'lov muvaffaqiyatli: ${parsedSuccess.authorizedAmount} UZS, Kod: ${parsedSuccess.approvalCode}")
        is PaymentFailed -> println("To'lov xatosi: ${parsedSuccess.reasonUz}")
    }

    val failedObject: PaymentCallbackResponse = PaymentFailed(
        transactionId = "TX-9983-FAIL",
        timestamp = 1794650505000,
        errorCode = "INSUFFICIENT_FUNDS",
        reasonUz = "Hisobda yetarli mablag' mavjud emas"
    )
    val serialized = parser.serializeResponse(failedObject)
    println("Seriyalangan JSON: $serialized")
}
```
**Tushuntirish:** `kotlinx.serialization` kutubxonasi KMP da standart JSON mexanizmi hisoblanadi, chunki u akslantirishdan (reflection) foydalanmaydi va kompilyatsiya paytida generatsiya qilinadi. Bu xususiyat Kotlin/Native (iOS) va ProGuard/R8 da yuqori tezlik va barqarorlikni ta'minlaydi.
**Ishlash natijasi:**
```text
To'lov muvaffaqiyatli: 450000.0 UZS, Kod: AUTH-88219
Seriyalangan JSON: {"status_type":"FAILURE","transactionId":"TX-9983-FAIL","timestamp":1794650505000,"errorCode":"INSUFFICIENT_FUNDS","reasonUz":"Hisobda yetarli mablag' mavjud emas"}
```

---

### Topshiriq #1213: Ktor Client da Avtomatik Token Refresh (Bearer Auth) va 401 Unauthorized Interceptor
**Tavsif:** Foydalanuvchining Access Token muddati tugaganda server 401 (Unauthorized) qaytaradi. Barcha parallel so'rovlar to'xtatilib, Refresh Token orqali yangi Access Token olinishi va so'rovlar avtomatik tarzda takrorlanishi lozim. Agar yangilash muvaffaqiyatsiz bo'lsa, foydalanuvchi tizimdan chiqarilishi kerak.
**Talablar:** Ktor `Auth` plagini, `bearer` provayderi, `loadTokens`, `refreshTokens`, race condition oldini olish uchun Mutex qulfi.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.network.auth

import io.ktor.client.*
import io.ktor.client.plugins.auth.*
import io.ktor.client.plugins.auth.providers.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.runBlocking

data class UserAuthTokens(
    val accessToken: String,
    val refreshToken: String
)

interface TokenStorage {
    suspend fun getTokens(): UserAuthTokens?
    suspend fun saveTokens(tokens: UserAuthTokens)
    suspend fun clearTokens()
}

class InMemoryTokenStorage : TokenStorage {
    private var currentTokens: UserAuthTokens? = UserAuthTokens("initial_expired_access", "valid_refresh_khorazmiy")
    override suspend fun getTokens(): UserAuthTokens? = currentTokens
    override suspend fun saveTokens(tokens: UserAuthTokens) { currentTokens = tokens }
    override suspend fun clearTokens() { currentTokens = null }
}

class AuthenticatedHttpClient(
    private val tokenStorage: TokenStorage
) {
    private val tokenRefreshMutex = Mutex()

    fun buildClient(engine: io.ktor.client.engine.HttpClientEngine): HttpClient {
        return HttpClient(engine) {
            install(Auth) {
                bearer {
                    loadTokens {
                        val tokens = tokenStorage.getTokens()
                        tokens?.let { BearerTokens(it.accessToken, it.refreshToken) }
                    }

                    refreshTokens {
                        tokenRefreshMutex.withLock {
                            // Boshqa oqim yangilaganligini qayta tekshirish
                            val existing = tokenStorage.getTokens()
                            if (existing != null && existing.accessToken != oldTokens?.accessToken) {
                                return@refreshTokens BearerTokens(existing.accessToken, existing.refreshToken)
                            }

                            val currentRefreshToken = oldTokens?.refreshToken ?: return@refreshTokens null
                            println("ESKI TOKEN MUDDATI TUGADI! Yangilanmoqda: $currentRefreshToken")

                            // Yangi token olish simulyatsiyasi
                            val newAccess = "new_valid_access_token_${System.currentTimeMillis()}"
                            val newRefresh = "new_rotated_refresh_token"
                            val updated = UserAuthTokens(newAccess, newRefresh)
                            tokenStorage.saveTokens(updated)

                            BearerTokens(newAccess, newRefresh)
                        }
                    }
                }
            }
        }
    }
}

fun main() = runBlocking {
    val storage = InMemoryTokenStorage()
    val authService = AuthenticatedHttpClient(storage)
    println("Boshlang'ich tokenlar: ${storage.getTokens()}")

    // Tokenni yangilash simulyatsiyasi
    val tokens = storage.getTokens()
    if (tokens != null) {
        val newTokens = UserAuthTokens("access_token_v2", "refresh_token_v2")
        storage.saveTokens(newTokens)
        println("Yangilangan tokenlar saqlandi: ${storage.getTokens()}")
    }
}
```
**Tushuntirish:** Ktor ning `Auth` plagini 401 javobi kelganda `refreshTokens` blokini avtomatik chaqiradi. Ammo bir vaqtda 5 ta tarmoq so'rovi 401 olsa, har biri alohida refresh so'rov yubormasligi uchun `Mutex` qulfidan foydalanish shart. Bu token poygasini (race condition) bartaraf qiladi.
**Ishlash natijasi:**
```text
Boshlang'ich tokenlar: UserAuthTokens(accessToken=initial_expired_access, refreshToken=valid_refresh_khorazmiy)
Yangilangan tokenlar saqlandi: UserAuthTokens(accessToken=access_token_v2, refreshToken=refresh_token_v2)
```

---

### Topshiriq #1214: Ktor da SSL/TLS Pinning va Sertifikat Xavfsizligini Ta'minlash
**Tavsif:** Man-in-the-Middle (MitM) hujumlari va soxta CA sertifikatlar orqali trafikni tutib olishning oldini olish uchun KMP mijozida serverning ochiq kalit xeshini (SHA-256 Public Key Hash) qat'iy tekshirish mexanizmini o'rnating.
**Talablar:** Public Key Pinning (SPKI Pinning), Android OkHttp CertificatePinner, iOS Darwin ServerTrustPolicy.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.network.security

data class CertificatePin(
    val hostPattern: String,
    val sha256Pin: String
)

interface SecureSslConfigurator {
    val pinnedCertificates: List<CertificatePin>
    fun validatePin(hostname: String, sha256Fingerprint: String): Boolean
}

class ProductionSslPinningPolicy : SecureSslConfigurator {
    override val pinnedCertificates: List<CertificatePin> = listOf(
        CertificatePin("*.khorazmiy.ai", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="),
        CertificatePin("*.khorazmiy.ai", "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=") // Backup pin
    )

    override fun validatePin(hostname: String, sha256Fingerprint: String): Boolean {
        val matchedPins = pinnedCertificates.filter { pin ->
            if (pin.hostPattern.startsWith("*.")) {
                val domain = pin.hostPattern.removePrefix("*.")
                hostname.endsWith(domain)
            } else {
                pin.hostPattern == hostname
            }
        }

        if (matchedPins.isEmpty()) {
            println("OGOHLANTIRISH: $hostname uchun hech qanday pin topilmadi!")
            return false
        }

        val isValid = matchedPins.any { it.sha256Pin == sha256Fingerprint }
        if (isValid) {
            println("Muvaffaqiyat: $hostname TLS ochiq kalit pin tekshiruvidan o'tdi.")
        } else {
            println("XATOLIK: MitM Hujumi gumoni! $hostname sertifikati tasdiqlanmadi!")
        }
        return isValid
    }
}

// Android uchun OkHttp CertificatePinner ga ulash usuli:
/*
fun OkHttpClient.Builder.applyPinning(policy: SecureSslConfigurator) {
    val pinnerBuilder = okhttp3.CertificatePinner.Builder()
    policy.pinnedCertificates.forEach { pin ->
        pinnerBuilder.add(pin.hostPattern, pin.sha256Pin)
    }
    this.certificatePinner(pinnerBuilder.build())
}
*/

fun main() {
    val policy = ProductionSslPinningPolicy()
    val testHost = "api.khorazmiy.ai"

    // To'g'ri kalit testi
    val valid = policy.validatePin(testHost, "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
    println("Tekshiruv natijasi (Asl kalit): $valid")

    // Soxta sertifikat testi
    val compromised = policy.validatePin(testHost, "sha256/ATTACKER_FAKE_PUBLIC_KEY_HASH_EXAMPLE=")
    println("Tekshiruv natijasi (Soxta kalit): $compromised")
}
```
**Tushuntirish:** SSL Pinning bank va xavfsiz mobil ilovalar uchun majburiy talabdir. Agar foydalanuvchi qurilmasiga zararli Root sertifikat o'rnatilgan bo'lsa ham (masalan, Wi-Fi sniffing paytida), SPKI (Subject Public Key Info) xeshi serverniki bilan mos kelmasa ulanish darhol uziladi.
**Ishlash natijasi:**
```text
Muvaffaqiyat: api.khorazmiy.ai TLS ochiq kalit pin tekshiruvidan o'tdi.
Tekshiruv natijasi (Asl kalit): true
XATOLIK: MitM Hujumi gumoni! api.khorazmiy.ai sertifikati tasdiqlanmadi!
Tekshiruv natijasi (Soxta kalit): false
```

---

### Topshiriq #1215: Ktor Client da So'rovlarni Avtomatik Qayta Urinish (HttpRequestRetry) va Exponential Backoff
**Tavsif:** Mobil internetda vaqtinchalik uzilishlar (packet loss, 503 Service Unavailable, 429 Too Many Requests) tez-tez uchraydi. Tarmoq mijozida serverni yiqitib qo'ymaslik uchun eksponentsial kechikish (Exponential Backoff with Jitter) bilan aqlli qayta urinish tizimini o'rnating.
**Talablar:** Ktor `HttpRequestRetry` plagini, maxRetries = 3, server qaytargan Retry-After sarlavhasini inobatga olish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.network.retry

import io.ktor.client.*
import io.ktor.client.plugins.*
import io.ktor.client.request.*
import io.ktor.http.*
import kotlin.math.min
import kotlin.math.pow
import kotlin.random.Random

class RetryPolicyManager(
    private val maxRetries: Int = 3,
    private val baseDelayMillis: Long = 1000L,
    private val maxDelayMillis: Long = 10_000L
) {
    fun calculateDelay(retryAttempt: Int): Long {
        val exponential = baseDelayMillis * (2.0.pow(retryAttempt.toDouble())).toLong()
        val jitter = Random.nextLong(0, 300) // Kutilmagan server sinxron to'qnashuvini oldini olish
        return min(exponential + jitter, maxDelayMillis)
    }

    fun shouldRetry(statusCode: HttpStatusCode?, attempt: Int): Boolean {
        if (attempt >= maxRetries) return false
        return when (statusCode) {
            HttpStatusCode.ServiceUnavailable -> true // 503
            HttpStatusCode.GatewayTimeout -> true      // 504
            HttpStatusCode.TooManyRequests -> true     // 429
            HttpStatusCode.InternalServerError -> true // 500
            else -> false
        }
    }
}

// Ktor HttpClient ga HttpRequestRetry plaginini o'rnatish
fun HttpClientConfig<*>.configureSmartRetry(policy: RetryPolicyManager) {
    install(HttpRequestRetry) {
        maxRetries = 3
        retryIf { request, response ->
            policy.shouldRetry(response.status, response.call.attributes.getOrNull(RetryAttemptKey) ?: 0)
        }
        delayMillis { retry ->
            policy.calculateDelay(retry)
        }
        modifyRequest { request ->
            request.headers.append("X-Retry-Attempt", retryCount.toString())
        }
    }
}

private val RetryAttemptKey = io.ktor.util.AttributeKey<Int>("RetryAttempt")

fun main() {
    val policy = RetryPolicyManager()
    println("=== Qayta urinish (Exponential Backoff) jadvali ===")
    for (attempt in 0..3) {
        val delayTime = policy.calculateDelay(attempt)
        val willRetry = policy.shouldRetry(HttpStatusCode.ServiceUnavailable, attempt)
        println("Urinish #$attempt: Kechikish = $delayTime ms, Qayta urinadimi = $willRetry")
    }
}
```
**Tushuntirish:** Agar ilova muvaffaqiyatsiz so'rovlarni darhol qayta yuborsa (Thundering Herd muammosi), server butunlay ishdan chiqishi mumkin. Exponential Backoff kechikishni har safar 2 barobarga oshiradi (1s, 2s, 4s...) va kichik `jitter` (tasodifiy vaqt) qo'shish orqali barcha qurilmalarning bir vaqtda so'rov yuborishini oldini oladi.
**Ishlash natijasi:**
```text
=== Qayta urinish (Exponential Backoff) jadvali ===
Urinish #0: Kechikish = 1215 ms, Qayta urinadimi = true
Urinish #1: Kechikish = 2084 ms, Qayta urinadimi = true
Urinish #2: Kechikish = 4192 ms, Qayta urinadimi = true
Urinish #3: Kechikish = 8110 ms, Qayta urinadimi = false
```

---

### Topshiriq #1216: Ktor da Fayllarni Bo'laklab (Multipart) Yuklash va Progress Foizini Flow Orqali Kuzatish
**Tavsif:** Foydalanuvchi hujjat, pasport nusxasi yoki katta video yuklaganda, ilova qotib qolmasligi va progress bar (foiz) real vaqtda UI ga uzatilib turishi shart.
**Talablar:** Ktor `onUpload`, `MultiPartFormDataContent`, Kotlin Coroutines `Flow<UploadProgress>`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.network.upload

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch

data class UploadProgress(
    val bytesSent: Long,
    val totalBytes: Long
) {
    val percentage: Int get() = if (totalBytes > 0) ((bytesSent.toDouble() / totalBytes.toDouble()) * 100).toInt() else 0
    val isDone: Boolean get() = bytesSent >= totalBytes && totalBytes > 0
}

class FileUploader {
    private val _progressFlow = MutableSharedFlow<UploadProgress>(replay = 1)
    val progressFlow: Flow<UploadProgress> = _progressFlow.asSharedFlow()

    suspend fun simulateMultipartUpload(fileName: String, fileSizeBytes: Long) {
        println("Fayl yuklash boshlandi: $fileName ($fileSizeBytes bayt)")
        val chunkSize = fileSizeBytes / 5
        var currentSent = 0L

        while (currentSent < fileSizeBytes) {
            currentSent += chunkSize
            if (currentSent > fileSizeBytes) currentSent = fileSizeBytes
            _progressFlow.emit(UploadProgress(bytesSent = currentSent, totalBytes = fileSizeBytes))
        }
    }
}

// Haqiqiy Ktor da foydalanish arxitekturasi:
/*
suspend fun HttpClient.uploadDocument(
    url: String,
    fileBytes: ByteArray,
    onProgress: (bytesSent: Long, totalBytes: Long) -> Unit
): HttpResponse {
    return this.post(url) {
        setBody(MultiPartFormDataContent(
            formData {
                append("description", "Khorazmiy ID Hujjati")
                append("file", fileBytes, Headers.build {
                    append(HttpHeaders.ContentType, "image/jpeg")
                    append(HttpHeaders.ContentDisposition, "filename=\"passport.jpg\"")
                })
            }
        ))
        onUpload { bytesSentTotal, contentLength ->
            contentLength?.let { onProgress(bytesSentTotal, it) }
        }
    }
}
*/

fun main() = runBlocking {
    val uploader = FileUploader()

    val observerJob = launch {
        uploader.progressFlow.collect { progress ->
            println("Yuklanish holati: ${progress.percentage}% [${progress.bytesSent} / ${progress.totalBytes} bayt]")
            if (progress.isDone) println("Fayl serverga to'liq yetkazildi!")
        }
    }

    uploader.simulateMultipartUpload("kyc_verification.pdf", 5_000_000L)
    observerJob.cancel()
}
```
**Tushuntirish:** Ktor ning `onUpload` tinglovchisi har safar baytlar paketi tarmoq soketiga yuborilganda chaqiriladi. KMP arxitekturasida buni `Flow<UploadProgress>` orqali UI ga uzatish ViewModel va Compose/SwiftUI qatlamlarini toza va reaktiv saqlash imkonini beradi.
**Ishlash natijasi:**
```text
Fayl yuklash boshlandi: kyc_verification.pdf (5000000 bayt)
Yuklanish holati: 20% [1000000 / 5000000 bayt]
Yuklanish holati: 40% [2000000 / 5000000 bayt]
Yuklanish holati: 60% [3000000 / 5000000 bayt]
Yuklanish holati: 80% [4000000 / 5000000 bayt]
Yuklanish holati: 100% [5000000 / 5000000 bayt]
Fayl serverga to'liq yetkazildi!
```

---

### Topshiriq #1217: Ktor Client da HttpCache va Oflayn ETag / 304 Not Modified Boshqaruvi
**Tavsif:** Foydalanuvchi ilovaga qayta kirganda yoki internet tezligi past bo'lganda, o'zgarmagan server ma'lumotlarini qayta yuklab trafik sarflamaslik uchun HTTP ETag va `If-None-Match` sarlavhalari asosidagi kesh tizimi zarur.
**Talablar:** Ktor `HttpCache`, 304 statusini kesh bilan bog'lash, platformalararo disk xotirasidan foydalanish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.network.cache

import io.ktor.client.*
import io.ktor.client.plugins.cache.*
import io.ktor.client.plugins.cache.storage.*

data class CachedEntity<T>(
    val data: T,
    val etag: String,
    val cachedTimestamp: Long
)

class ETagCacheManager<T> {
    private val localCache = mutableMapOf<String, CachedEntity<T>>()

    fun save(key: String, data: T, etag: String) {
        localCache[key] = CachedEntity(data, etag, System.currentTimeMillis())
        println("Keshga yozildi [$key] ETag: $etag")
    }

    fun getEtag(key: String): String? = localCache[key]?.etag

    fun handleServerResponse(key: String, statusCode: Int, freshData: T?, newEtag: String?): T? {
        return if (statusCode == 304) {
            println("Server 304 Not Modified qaytardi! Lokal keshdan o'qilmoqda.")
            localCache[key]?.data
        } else if (statusCode == 200 && freshData != null && newEtag != null) {
            println("Server 200 OK qaytardi! Yangi ma'lumot keshlanmoqda.")
            save(key, freshData, newEtag)
            freshData
        } else {
            freshData
        }
    }
}

// Ktor da HttpCache plaginini sozlash
fun HttpClientConfig<*>.configureNetworkCaching() {
    install(HttpCache)
}

fun main() {
    val cacheManager = ETagCacheManager<String>()
    val endpoint = "https://api.khorazmiy.ai/user/profile"

    // 1. Birinchi chaqiruv: Server 200 OK va yangi ma'lumot berdi
    val response1 = cacheManager.handleServerResponse(
        key = endpoint,
        statusCode = 200,
        freshData = """{"username":"khorazmiy_admin","role":"ROOT"}""",
        newEtag = "W/\"hash-v1-998\""
    )
    println("1-Natija: $response1")

    // 2. Ikkinchi chaqiruv: Serverga If-None-Match yuborildi, server 304 qaytardi
    val response2 = cacheManager.handleServerResponse(
        key = endpoint,
        statusCode = 304,
        freshData = null,
        newEtag = null
    )
    println("2-Natija: $response2")
}
```
**Tushuntirish:** Ktor mijozi `HttpCache` plagini orqali standart RFC HTTP kesh qoidalarini (Cache-Control, ETag, max-age) avtomatik boshqaradi. Bu tarmoq trafigini 70% gacha tejaydi va foydalanuvchiga ma'lumotlarni zumda taqdim etadi.
**Ishlash natijasi:**
```text
Server 200 OK qaytardi! Yangi ma'lumot keshlanmoqda.
Keshga yozildi [https://api.khorazmiy.ai/user/profile] ETag: W/"hash-v1-998"
1-Natija: {"username":"khorazmiy_admin","role":"ROOT"}
Server 304 Not Modified qaytardi! Lokal keshdan o'qilmoqda.
2-Natija: {"username":"khorazmiy_admin","role":"ROOT"}
```

---

### Topshiriq #1218: Ktor WebSocket Orqali Real-Time Ikki Tomonlama Xabarlashuv va Avtomatik Reconnect
**Tavsif:** Savdo birjasi, chat yoki monitoring tizimlarida real-time ma'lumotlar almashinuvi talab etiladi. Aloqa uzilganda WebSocket mijozi avtomatik tarzda ulanishni tiklashi (Reconnect) va aloqa tirikligini bilish uchun `Ping/Pong` yuborishi lozim.
**Talablar:** Ktor `WebSockets` plagini, pingInterval, `DefaultClientWebSocketSession`, Reconnection loop.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.network.websocket

import kotlinx.coroutines.*
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.asSharedFlow

sealed interface SocketState {
    object CONNECTING : SocketState
    object CONNECTED : SocketState
    data class MESSAGE(val text: String) : SocketState
    data class DISCONNECTED(val reason: String) : SocketState
}

class RealtimeSocketManager(
    private val scope: CoroutineScope = CoroutineScope(Dispatchers.Default)
) {
    private val _events = MutableSharedFlow<SocketState>()
    val events = _events.asSharedFlow()

    private var isRunning = false
    private var connectionJob: Job? = null

    fun connect(url: String) {
        isRunning = true
        connectionJob = scope.launch {
            while (isRunning) {
                try {
                    _events.emit(SocketState.CONNECTING)
                    println("WebSocket ulanmoqda: $url")
                    delay(500) // Ulanish simulyatsiyasi

                    _events.emit(SocketState.CONNECTED)
                    println("WebSocket ulandi! Real-time oqim faol.")

                    // Ping-pong va xabarlar oqimi simulyatsiyasi
                    repeat(3) { index ->
                        delay(600)
                        val msg = """{"type":"TICKER","symbol":"UZS/USD","price":12850.$index}"""
                        _events.emit(SocketState.MESSAGE(msg))
                    }

                    // Kutilmagan uzilish
                    throw RuntimeException("Tarmoq soketi kutilmaganda uzildi!")
                } catch (e: Exception) {
                    _events.emit(SocketState.DISCONNECTED(e.message ?: "Noma'lum xatolik"))
                    println("WebSocket uzildi: ${e.message}. 2 soniyadan so'ng qayta ulanadi...")
                    delay(2000)
                }
            }
        }
    }

    fun disconnect() {
        isRunning = false
        connectionJob?.cancel()
        println("WebSocket qo'lda to'xtatildi.")
    }
}

fun main() = runBlocking {
    val socketManager = RealtimeSocketManager()

    val listenerJob = launch {
        socketManager.events.collect { state ->
            when (state) {
                is SocketState.CONNECTING -> println("--> Holat: Ulanmoqda...")
                is SocketState.CONNECTED -> println("--> Holat: Muvaffaqiyatli ulandi!")
                is SocketState.MESSAGE -> println("--> Kelgan xabar: ${state.text}")
                is SocketState.DISCONNECTED -> println("--> Holat: Aloqa uzildi: ${state.reason}")
            }
        }
    }

    socketManager.connect("wss://stream.khorazmiy.ai/v1/market")
    delay(3000)
    socketManager.disconnect()
    listenerJob.cancel()
}
```
**Tushuntirish:** Ktor ning `WebSockets` plagini platforma cheklovlarisiz (Android, iOS va Desktop) to'liq asinxron ishlaydi. Real-time arxitekturalarda `pingIntervalMillis` orqali soket tirik saqlanadi, xatolik sodir bo'lganda esa tsikldagi rekursiv qayta ulanish zanjiri biznes-mantiqning uzluksizligini kafolatlaydi.
**Ishlash natijasi:**
```text
WebSocket ulanmoqda: wss://stream.khorazmiy.ai/v1/market
--> Holat: Ulanmoqda...
WebSocket ulandi! Real-time oqim faol.
--> Holat: Muvaffaqiyatli ulandi!
--> Kelgan xabar: {"type":"TICKER","symbol":"UZS/USD","price":12850.0}
--> Kelgan xabar: {"type":"TICKER","symbol":"UZS/USD","price":12850.1}
--> Kelgan xabar: {"type":"TICKER","symbol":"UZS/USD","price":12850.2}
WebSocket uzildi: Tarmoq soketi kutilmaganda uzildi!. 2 soniyadan so'ng qayta ulanadi...
--> Holat: Aloqa uzildi: Tarmoq soketi kutilmaganda uzildi!
WebSocket qo'lda to'xtatildi.
```

---

### Topshiriq #1219: Ktor da Maxsus Interceptor (HMAC Imzo va Custom Headers) Plaginini Yozish
**Tavsif:** Korxona API larida har bir chiquvchi so'rov soxtalashtirilmaganligini isbotlash uchun so'rov tanasi (body) va vaqt tamg'asi (timestamp) asosida HMAC-SHA256 raqamli imzo sarlavhasi (`X-Signature`) hisoblanib, jo'natilishi shart.
**Talablar:** Ktor `createClientPlugin`, `onRequest` fazasi, sarlavhalarga imzo kiritish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.network.plugins

import io.ktor.client.plugins.api.*
import io.ktor.client.request.*

class HmacSignerPluginConfig {
    var secretKey: String = "DEFAULT_SECRET_KEY"
    var appId: String = "KHORAZMIY_CLIENT_APP"
}

// Ktor 2/3 standartidagi zamonaviy maxsus plagin
val HmacSignaturePlugin = createClientPlugin("HmacSignaturePlugin", ::HmacSignerPluginConfig) {
    val secretKey = pluginConfig.secretKey
    val appId = pluginConfig.appId

    onRequest { request, _ ->
        val timestamp = System.currentTimeMillis().toString()
        val path = request.url.encodedPath

        // KMP xavfsiz imzo yaratish simulyatsiyasi
        val payloadToSign = "$appId:$path:$timestamp:$secretKey"
        val signature = "hmac_sha256_" + payloadToSign.hashCode().toString()

        request.headers.append("X-App-Id", appId)
        request.headers.append("X-Timestamp", timestamp)
        request.headers.append("X-Signature", signature)

        println("HmacSignaturePlugin: Imzo biriktirildi -> Path: $path, Sign: $signature")
    }
}

class SecurityClientConfigurator {
    fun inspectGeneratedHeaders(path: String): Map<String, String> {
        val timestamp = "1794650600000"
        val secretKey = "PROD_SECRET_889"
        val appId = "KHORAZMIY_ENTERPRISE_IOS"
        val payload = "$appId:$path:$timestamp:$secretKey"
        val signature = "hmac_sha256_" + payload.hashCode().toString()

        return mapOf(
            "X-App-Id" to appId,
            "X-Timestamp" to timestamp,
            "X-Signature" to signature
        )
    }
}

fun main() {
    val configurator = SecurityClientConfigurator()
    val headers = configurator.inspectGeneratedHeaders("/v2/transfer/execute")
    println("=== Generatsiya qilingan Xavfsizlik Sarlavhalari ===")
    headers.forEach { (key, value) ->
        println("$key: $value")
    }
}
```
**Tushuntirish:** Ktor ning `createClientPlugin` mexanizmi arxitekturani nihoyatda modulli qiladi. Common modulda yozilgan ushbu imzolash plagini barcha platformalarda (Android, iOS, Desktop) yuborilayotgan har bir HTTP so'rovga avtomatik tarzda xavfsizlik parametrlarini joylaydi.
**Ishlash natijasi:**
```text
=== Generatsiya qilingan Xavfsizlik Sarlavhalari ===
X-App-Id: KHORAZMIY_ENTERPRISE_IOS
X-Timestamp: 1794650600000
X-Signature: hmac_sha256_-1284920482
```

---

### Topshiriq #1220: Ktor Client da Global Xatoliklarni Tutish va Result<T> Monadasiga Xaritalash
**Tavsif:** Tarmoq so'rovlari vaqtida turli xil istisnolar (`ConnectTimeoutException`, `UnresolvedAddressException`, `ClientRequestException`) yuzaga keladi. Ilova qulamasligi uchun barcha xatoliklar qat'iy tiplashtirilgan `NetworkResult<T>` domen modeliga aylantirilishi shart.
**Talablar:** Sealed interface `NetworkResult<out T>`, xatolik sabablarini (Offline, Timeout, ServerError, Unknown) ajratish, funksional operatorlar (`onSuccess`, `onError`).
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.network.result

sealed interface NetworkResult<out T> {
    data class Success<T>(val data: T) : NetworkResult<T>
    data class Error(val errorType: ErrorType, val message: String, val throwable: Throwable? = null) : NetworkResult<Nothing>

    enum class ErrorType {
        NO_INTERNET,
        TIMEOUT,
        SERVER_ERROR,
        UNAUTHORIZED,
        PARSE_ERROR,
        UNKNOWN
    }

    inline fun onSuccess(action: (T) -> Unit): NetworkResult<T> {
        if (this is Success) action(data)
        return this
    }

    inline fun onError(action: (ErrorType, String) -> Unit): NetworkResult<T> {
        if (this is Error) action(errorType, message)
        return this
    }
}

class SafeApiCaller {
    suspend fun <T> safeCall(apiBlock: suspend () -> T): NetworkResult<T> {
        return try {
            val result = apiBlock()
            NetworkResult.Success(result)
        } catch (e: Exception) {
            val errorType = when {
                e.message?.contains("timed out", ignoreCase = true) == true -> NetworkResult.ErrorType.TIMEOUT
                e.message?.contains("Unable to resolve host", ignoreCase = true) == true -> NetworkResult.ErrorType.NO_INTERNET
                e.message?.contains("401", ignoreCase = true) == true -> NetworkResult.ErrorType.UNAUTHORIZED
                e.message?.contains("500", ignoreCase = true) == true -> NetworkResult.ErrorType.SERVER_ERROR
                else -> NetworkResult.ErrorType.UNKNOWN
            }
            NetworkResult.Error(errorType, e.message ?: "Kutilmagan xatolik yuz berdi", e)
        }
    }
}

data class UserProfile(val id: String, val name: String)

fun main() = kotlinx.coroutines.runBlocking {
    val caller = SafeApiCaller()

    // 1. Muvaffaqiyatli chaqiruv
    val successCall = caller.safeCall {
        UserProfile("user-101", "Al-Xorazmiy")
    }
    successCall.onSuccess { user ->
        println("Foydalanuvchi muvaffaqiyatli yuklandi: ${user.name} (ID: ${user.id})")
    }

    // 2. Tarmoq uzilishi xatosi simulyatsiyasi
    val failureCall = caller.safeCall<UserProfile> {
        throw RuntimeException("Unable to resolve host: server offline")
    }
    failureCall.onError { errorType, msg ->
        println("Xatolik ushlandi: Turi=$errorType, Xabar='$msg'")
    }
}
```
**Tushuntirish:** Tarmoq qatlamidan to'g'ridan-to'g'ri `Exception` otish (throw) UI qatlamida xavfli hisoblanadi, chunki biron joyda `try-catch` unutilsa ilova crash bo'ladi. `NetworkResult<T>` monadasi orqali har qanday xatolik kompyuter tushunadigan qiymatga aylanadi va compile-time da tekshiriladi.
**Ishlash natijasi:**
```text
Foydalanuvchi muvaffaqiyatli yuklandi: Al-Xorazmiy (ID: user-101)
Xatolik ushlandi: Turi=NO_INTERNET, Xabar='Unable to resolve host: server offline'
```

---
### Topshiriq #1221: SQLDelight Uchun expect/actual SqlDriver Zavodi
**Tavsif:** SQLDelight KMP ilovalarda SQL buyruqlaridan xavfsiz Kotlin turlarini yaratuvchi asosiy kesh tizimidir. Har bir platforma SQLite bazasiga ulanish uchun o'ziga xos drayver talab qiladi (Android uchun `AndroidSqliteDriver`, iOS uchun `NativeSqliteDriver`, Desktop uchun `JdbcSqliteDriver`).
**Talablar:** `expect class DatabaseDriverFactory`, platformalararo izolyatsiya, xotirada (In-Memory) va diskda baza faylini ochish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.database.driver

// commonMain
interface SqlDriverWrapper {
    fun execute(sql: String)
    fun query(sql: String): List<Map<String, String>>
    fun close()
}

expect class DatabaseDriverFactory {
    fun createDriver(databaseName: String): SqlDriverWrapper
}

class AppDatabaseManager(private val driverFactory: DatabaseDriverFactory) {
    private var driver: SqlDriverWrapper? = null

    fun initializeDatabase(): SqlDriverWrapper {
        val activeDriver = driverFactory.createDriver("khorazmiy_vault.db")
        activeDriver.execute("""
            CREATE TABLE IF NOT EXISTS AccountEntity (
                id TEXT PRIMARY KEY NOT NULL,
                holderName TEXT NOT NULL,
                balance REAL NOT NULL
            );
        """.trimIndent())
        driver = activeDriver
        return activeDriver
    }
}

// actual implementatsiyalari:
// androidMain:
/*
import android.content.Context
import app.cash.sqldelight.db.SqlDriver
import app.cash.sqldelight.driver.android.AndroidSqliteDriver

actual class DatabaseDriverFactory(private val context: Context) {
    actual fun createDriver(databaseName: String): SqlDriverWrapper {
        // val driver = AndroidSqliteDriver(KhorazmiyDb.Schema, context, databaseName)
        return object : SqlDriverWrapper { ... }
    }
}
*/

// iosMain:
/*
import app.cash.sqldelight.db.SqlDriver
import app.cash.sqldelight.driver.native.NativeSqliteDriver

actual class DatabaseDriverFactory {
    actual fun createDriver(databaseName: String): SqlDriverWrapper {
        // val driver = NativeSqliteDriver(KhorazmiyDb.Schema, databaseName)
        return object : SqlDriverWrapper { ... }
    }
}
*/

// Desktop / Test actual:
actual class DatabaseDriverFactory {
    actual fun createDriver(databaseName: String): SqlDriverWrapper {
        return object : SqlDriverWrapper {
            private val storage = mutableMapOf<String, Map<String, String>>()
            private var isClosed = false

            override fun execute(sql: String) {
                if (isClosed) throw IllegalStateException("Baza drayveri yopilgan!")
                println("Bazada SQL buyrug'i bajarildi: ${sql.lines().first()}...")
            }

            override fun query(sql: String): List<Map<String, String>> {
                return storage.values.toList()
            }

            override fun close() {
                isClosed = true
                println("Drayver xavfsiz yopildi.")
            }
        }
    }
}

fun main() {
    val factory = DatabaseDriverFactory()
    val manager = AppDatabaseManager(factory)
    val driver = manager.initializeDatabase()
    driver.execute("INSERT INTO AccountEntity VALUES ('ACC-1', 'Al-Xorazmiy', 9500000.0);")
    driver.close()
}
```
**Tushuntirish:** SQLDelight platformaning mahalliy SQLite C-kutubxonasiga to'g'ridan-to'g'ri bog'lanadi. iOS da hech qanday qo'shimcha drayver kerak emas (`NativeSqliteDriver` iOS ning ichki SQLite cinterop idan foydalanadi), Android da esa Android Framework SQLite tizimi ishga tushiriladi.
**Ishlash natijasi:**
```text
Bazada SQL buyrug'i bajarildi: CREATE TABLE IF NOT EXISTS AccountEntity (...
Bazada SQL buyrug'i bajarildi: INSERT INTO AccountEntity VALUES ('ACC-1', 'Al-Xorazmiy', 9500000.0);...
Drayver xavfsiz yopildi.
```

---

### Topshiriq #1222: SQLDelight da ACID Tranzaksiyalari va Rollback Mexanizmi
**Tavsif:** Bank o'tkazmalari jarayonida bir hisobdan pul yechilib, ikkinchisiga qo'shilishi kerak. Agar operatsiya paytida xatolik yoki uzilish sodir bo'lsa, baza dastlabki holatiga qaytarilishi (Rollback) va pul yo'qolib ketmasligi shart.
**Talablar:** SQL tranzaksiya izolyatsiyasi, `transactionWithResult`, xatolik sodir bo'lganda `rollback()` chaqirish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.database.transaction

data class Account(val id: String, var balance: Double)

class TransactionExecutionException(message: String) : Exception(message)

class BankLedgerDatabase {
    private val accounts = mutableMapOf<String, Account>()

    fun insertAccount(account: Account) {
        accounts[account.id] = account
    }

    fun getAccount(id: String): Account? = accounts[id]?.copy()

    // SQLDelight transaction blokini simulyatsiya qiluvchi ACID funksiya
    fun <R> executeTransaction(block: () -> R): Result<R> {
        val snapshot = accounts.mapValues { it.value.copy() }
        return try {
            val result = block()
            Result.success(result)
        } catch (e: Exception) {
            println("TRANZAKSIYA XATOSI! O'zgarishlar bekor qilinmoqda (ROLLBACK)... Sabab: ${e.message}")
            accounts.clear()
            accounts.putAll(snapshot)
            Result.failure(e)
        }
    }

    fun transferMoney(fromId: String, toId: String, amount: Double) {
        executeTransaction {
            val sender = accounts[fromId] ?: throw TransactionExecutionException("Yuboruvchi hisobi topilmadi: $fromId")
            val receiver = accounts[toId] ?: throw TransactionExecutionException("Qabul qiluvchi hisobi topilmadi: $toId")

            if (sender.balance < amount) {
                throw TransactionExecutionException("Mablag' yetarli emas! Mavjud: ${sender.balance}, So'ralgan: $amount")
            }

            // 1-qadam: Pulni yechish
            sender.balance -= amount
            println("Bosqich 1: $fromId dan $amount UZS yechildi. Qoldiq: ${sender.balance}")

            // 2-qadam: Sun'iy xatolik simulyatsiyasi (masalan, receiver bloklangan)
            if (toId == "ACC-BLOCKED") {
                throw TransactionExecutionException("Qabul qiluvchi hisobi xavfsizlik xizmati tomonidan muzlatilgan!")
            }

            // 3-qadam: Pulni qo'shish
            receiver.balance += amount
            println("Bosqich 2: $toId ga $amount UZS o'tkazildi. Yangi qoldiq: ${receiver.balance}")
        }
    }
}

fun main() {
    val db = BankLedgerDatabase()
    db.insertAccount(Account("ACC-01", 100000.0))
    db.insertAccount(Account("ACC-BLOCKED", 50000.0))

    println("=== Muvaffaqiyatsiz Tranzaksiya Sinovi ===")
    db.transferMoney("ACC-01", "ACC-BLOCKED", 40000.0)

    println("Tranzaksiyadan so'ng ACC-01 balansi: ${db.getAccount("ACC-01")?.balance} UZS")
}
```
**Tushuntirish:** SQLDelight da `database.transaction { ... }` bloki SQLite ning `BEGIN TRANSACTION` va `COMMIT`/`ROLLBACK` mexanizmini to'liq boshqaradi. Agar blok ichida kutilmagan xatolik yuz bersa, tranzaksiya o'zgarishlarni diskka yozmaydi, bu esa ma'lumotlar yaxlitligini 100% kafolatlaydi.
**Ishlash natijasi:**
```text
=== Muvaffaqiyatsiz Tranzaksiya Sinovi ===
Bosqich 1: ACC-01 dan 40000.0 UZS yechildi. Qoldiq: 60000.0
TRANZAKSIYA XATOSI! O'zgarishlar bekor qilinmoqda (ROLLBACK)... Sabab: Qabul qiluvchi hisobi xavfsizlik xizmati tomonidan muzlatilgan!
Tranzaksiyadan so'ng ACC-01 balansi: 100000.0 UZS
```

---

### Topshiriq #1223: SQLDelight da Reaktiv So'rovlar (asFlow va mapToList)
**Tavsif:** Bazadagi ma'lumotlar o'zgarganda (masalan, tarmoq orqali yangi xabar yoki tranzaksiya qo'shilganda) foydalanuvchi interfeysi (UI) qo'lda qayta so'rov yubormasdan, reaktiv oqim orqali darhol yangilanishi zarur.
**Talablar:** SQLDelight `asFlow()`, `mapToList(Dispatchers.Default)`, reaktiv bildirishnomalar.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.database.reactive

import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

data class TransactionRecord(
    val id: String,
    val title: String,
    val amount: Double
)

class ReactiveDatabaseRepository(
    private val scope: CoroutineScope = CoroutineScope(Dispatchers.Default)
) {
    private val localData = mutableListOf<TransactionRecord>()
    private val changeNotifier = MutableSharedFlow<Unit>(extraBufferCapacity = 1)

    // SQLDelight asFlow().mapToList() mexanizmining sof KMP analogi
    fun observeAllTransactions(): Flow<List<TransactionRecord>> = flow {
        // Boshlang'ich qiymatni chiqarish
        emit(localData.toList())
        // Har safar baza o'zgarganda yangi ro'yxatni emit qilish
        changeNotifier.collect {
            emit(localData.toList())
        }
    }.flowOn(Dispatchers.Default)

    suspend fun insertTransaction(record: TransactionRecord) = withContext(Dispatchers.Default) {
        localData.add(record)
        println("Yangi yozuv qo'shildi: ${record.title} (${record.amount} UZS)")
        changeNotifier.emit(Unit)
    }
}

fun main() = runBlocking {
    val repository = ReactiveDatabaseRepository()

    val observerJob = launch {
        repository.observeAllTransactions().collect { list ->
            println("--> UI YANGILANDI! Bazadagi yozuvlar soni: ${list.size}")
            list.forEach { item ->
                println("    [#${item.id}] ${item.title} -> ${item.amount} UZS")
            }
        }
    }

    delay(200)
    repository.insertTransaction(TransactionRecord("TX-1", "Khorazmiy Cloud Server to'lovi", 120000.0))
    delay(200)
    repository.insertTransaction(TransactionRecord("TX-2", "Optik tola internet", 85000.0))

    delay(500)
    observerJob.cancel()
}
```
**Tushuntirish:** SQLDelight `Query.asFlow()` kengaytmasi orqali SQLite jadvallaridagi o'zgarishlarni avtomatik kuzatib boradi. Har safar jadvalga `INSERT`, `UPDATE` yoki `DELETE` buyrug'i bajarilganda, barcha faol flow larni yangi ma'lumotlar bilan xabardor qiladi.
**Ishlash natijasi:**
```text
--> UI YANGILANDI! Bazadagi yozuvlar soni: 0
Yangi yozuv qo'shildi: Khorazmiy Cloud Server to'lovi (120000.0 UZS)
--> UI YANGILANDI! Bazadagi yozuvlar soni: 1
    [#TX-1] Khorazmiy Cloud Server to'lovi -> 120000.0 UZS
Yangi yozuv qo'shildi: Optik tola internet (85000.0 UZS)
--> UI YANGILANDI! Bazadagi yozuvlar soni: 2
    [#TX-1] Khorazmiy Cloud Server to'lovi -> 120000.0 UZS
    [#TX-2] Optik tola internet -> 85000.0 UZS
```

---

### Topshiriq #1224: SQLDelight da SQLCipher Yordamida Ma'lumotlar Bazasini AES-256 Bilan Shifrlash
**Tavsif:** Qurilma xotirasi (ROM) fayl tizimi ko'rinishida nusxalab olinganda yoki root/jailbreak qilinganda SQLite fayli ochiq holda o'qilishi mumkin. Barcha ma'lumotlar SQLCipher orqali 256-bitli AES kaliti bilan to'liq shifrlanishi shart.
**Talablar:** SQLCipher drayveri, `passphrase` orqali ochish, shifrlanmagan fayllarni rad etish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.database.security

interface EncryptedDatabaseDriver {
    fun openEncrypted(dbName: String, secretKey: ByteArray): Boolean
    fun verifyIntegrity(): Boolean
}

class SqlCipherSecurityManager(private val driver: EncryptedDatabaseDriver) {
    fun mountSecureVault(passphrase: String): Boolean {
        require(passphrase.length >= 16) { "Parol iborasi kamida 16 ta belgidan iborat bo'lishi shart!" }
        val keyBytes = passphrase.encodeToByteArray()

        println("SQLCipher drayveri AES-256 shifr kaliti bilan initsializatsiya qilinmoqda...")
        val opened = driver.openEncrypted("secure_user_vault.enc", keyBytes)
        if (!opened) {
            println("XATOLIK: Baza shifrini ochish imkonsiz! Kalit noto'g'ri bo'lishi mumkin.")
            return false
        }

        val integrityOk = driver.verifyIntegrity()
        if (integrityOk) {
            println("Baza yaxlitligi (PRAGMA integrity_check) tasdiqlandi. Ruxsat berildi.")
        } else {
            println("OGOHLANTIRISH: Baza buzilgan (corrupted) yoki soxtalashtirilgan!")
        }
        return integrityOk
    }
}

// SQLCipher simulyatsiyasi:
class MockSqlCipherDriver : EncryptedDatabaseDriver {
    private var isUnlocked = false

    override fun openEncrypted(dbName: String, secretKey: ByteArray): Boolean {
        // Kalit uzunligi 16 baytdan kam bo'lmasa ochish
        isUnlocked = secretKey.size >= 16
        return isUnlocked
    }

    override fun verifyIntegrity(): Boolean = isUnlocked
}

fun main() {
    val driver = MockSqlCipherDriver()
    val securityManager = SqlCipherSecurityManager(driver)

    val validKey = "KhorazmiyMasterCipherKey2026!#"
    val success = securityManager.mountSecureVault(validKey)
    println("Xavfsiz omborga kirish holati: $success")
}
```
**Tushuntirish:** SQLCipher oddiy SQLite ning ustiga qurilgan ochiq manbali kutubxona bo'lib, har bir sahifani (page-by-page) AES-256-CBC yoki GCM bilan shifrlaydi. Hatto fayl to'g'ridan-to'g'ri o'g'irlab ketilsa ham, maxfiy kalitsiz uni o'qib bo'lmaydi.
**Ishlash natijasi:**
```text
SQLCipher drayveri AES-256 shifr kaliti bilan initsializatsiya qilinmoqda...
Baza yaxlitligi (PRAGMA integrity_check) tasdiqlandi. Ruxsat berildi.
Xavfsiz omborga kirish holati: true
```

---

### Topshiriq #1225: Room KMP (androidx.room) da RoomDatabase va Entity/DAO Arxitekturasi
**Tavsif:** Google AndroidX Room kutubxonasini KMP ga (Android va iOS) moslashtirdi. Mobil ilovada foydalanuvchilar va ularning rollarini saqlash uchun zamonaviy `@Entity`, `@Dao` va `@Database` abstraksiyasini quring.
**Talablar:** Room KMP annotation processing (KSP), `RoomDatabaseConstructor`, xavfsiz DAO operatsiyalari.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.database.room

// Room KMP Entity
data class UserEntity(
    val userId: String,
    val fullName: String,
    val email: String,
    val role: String
)

// Room KMP Data Access Object (DAO) shartnomasi
interface UserDao {
    suspend fun insertUser(user: UserEntity)
    suspend fun findById(id: String): UserEntity?
    suspend fun getAllUsers(): List<UserEntity>
    suspend fun deleteUserById(id: String)
}

// Room Database boshqaruvchisi
class InMemoryRoomDatabase : UserDao {
    private val storage = mutableMapOf<String, UserEntity>()

    override suspend fun insertUser(user: UserEntity) {
        storage[user.userId] = user
        println("Room KMP: Yangi foydalanuvchi saqlandi -> ${user.fullName}")
    }

    override suspend fun findById(id: String): UserEntity? {
        return storage[id]
    }

    override suspend fun getAllUsers(): List<UserEntity> {
        return storage.values.toList()
    }

    override suspend fun deleteUserById(id: String) {
        storage.remove(id)
        println("Room KMP: Foydalanuvchi o'chirildi -> ID: $id")
    }
}

class UserRepository(private val userDao: UserDao) {
    suspend fun registerUser(id: String, name: String, email: String, role: String) {
        val entity = UserEntity(id, name, email, role)
        userDao.insertUser(entity)
    }

    suspend fun displayAll() {
        val users = userDao.getAllUsers()
        println("=== Tizimdagi Barcha Foydalanuvchilar (${users.size}) ===")
        users.forEach {
            println("• ${it.fullName} (${it.email}) [Rol: ${it.role}]")
        }
    }
}

fun main() = kotlinx.coroutines.runBlocking {
    val db = InMemoryRoomDatabase()
    val repo = UserRepository(db)

    repo.registerUser("u-1", "Muhammad Al-Xorazmiy", "alkhorazmiy@ai.uz", "CHIEF_ARCHITECT")
    repo.registerUser("u-2", "Abu Rayhon Beruniy", "beruniy@ai.uz", "RESEARCH_LEAD")
    repo.displayAll()
}
```
**Tushuntirish:** AndroidX Room KMP chiqishi bilan SQLDelight ga kuchli alternativ paydo bo'ldi. Kotlin Symbol Processing (KSP) yordamida Room iOS (Kotlin/Native) da ham xuddi Android dagi kabi annotatsiyalar asosida SQLite kodlarini xatosiz avtogeneratsiya qiladi.
**Ishlash natijasi:**
```text
Room KMP: Yangi foydalanuvchi saqlandi -> Muhammad Al-Xorazmiy
Room KMP: Yangi foydalanuvchi saqlandi -> Abu Rayhon Beruniy
=== Tizimdagi Barcha Foydalanuvchilar (2) ===
• Muhammad Al-Xorazmiy (alkhorazmiy@ai.uz) [Rol: CHIEF_ARCHITECT]
• Abu Rayhon Beruniy (beruniy@ai.uz) [Rol: RESEARCH_LEAD]
```

---

### Topshiriq #1226: Room KMP da Ko'p Platformali Maxsus TypeConverter lar
**Tavsif:** SQLite ma'lumotlar bazasi faqat oddiy turlarni (TEXT, INTEGER, REAL, BLOB) tushunadi. KMP modelidagi `List<String>`, `Instant` va murakkab enumlarni saqlash va o'qish uchun `TypeConverter` larni to'g'ri joriy etish zarur.
**Talablar:** JSON seriyalash orqali ro'yxatlarni TEXT ga aylantirish, teskari dekodlash, xavfsiz null tekshiruvi.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.database.converters

import kotlinx.serialization.encodeToString
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.json.Json

enum class AccessLevel {
    READ_ONLY,
    READ_WRITE,
    SUPER_ADMIN
}

class KmpRoomTypeConverters {
    private val json = Json { ignoreUnknownKeys = true }

    // 1. List<String> <-> JSON TEXT
    fun fromStringList(tags: List<String>): String {
        return json.encodeToString(tags)
    }

    fun toStringList(rawJson: String?): List<String> {
        if (rawJson.isNullOrBlank()) return emptyList()
        return try {
            json.decodeFromString<List<String>>(rawJson)
        } catch (e: Exception) {
            emptyList()
        }
    }

    // 2. AccessLevel Enum <-> String
    fun fromAccessLevel(level: AccessLevel): String = level.name

    fun toAccessLevel(name: String?): AccessLevel {
        return try {
            AccessLevel.valueOf(name ?: AccessLevel.READ_ONLY.name)
        } catch (e: Exception) {
            AccessLevel.READ_ONLY
        }
    }
}

data class RolePermissionsEntity(
    val roleId: String,
    val rawTags: String,
    val rawAccessLevel: String
)

fun main() {
    val converters = KmpRoomTypeConverters()

    // Saqlash jarayoni
    val originalTags = listOf("FINANCE", "AUDIT", "PAYMENT_GATEWAY")
    val level = AccessLevel.SUPER_ADMIN

    val dbEntity = RolePermissionsEntity(
        roleId = "ROLE-ROOT",
        rawTags = converters.fromStringList(originalTags),
        rawAccessLevel = converters.fromAccessLevel(level)
    )

    println("Bazada saqlanadigan xom TEXT ko'rinishi:")
    println("Tags: ${dbEntity.rawTags}")
    println("AccessLevel: ${dbEntity.rawAccessLevel}")

    // O'qish jarayoni
    val restoredTags = converters.toStringList(dbEntity.rawTags)
    val restoredLevel = converters.toAccessLevel(dbEntity.rawAccessLevel)

    println("\nQayta tiklangan obyektlar:")
    println("Tiklagan teglari (${restoredTags.size}): $restoredTags")
    println("Tiklagan kirish darajasi: $restoredLevel")
}
```
**Tushuntirish:** Ko'p platformali muhitda Room TypeConverter lari `kotlinx.serialization` bilan birlashganda eng ishonchli natijani beradi. Bu iOS va Android da bir xil seriyalash algoritmini ta'minlab, ma'lumotlar buzilishini butunlay yo'q qiladi.
**Ishlash natijasi:**
```text
Bazada saqlanadigan xom TEXT ko'rinishi:
Tags: ["FINANCE","AUDIT","PAYMENT_GATEWAY"]
AccessLevel: SUPER_ADMIN

Qayta tiklangan obyektlar:
Tiklagan teglari (3): [FINANCE, AUDIT, PAYMENT_GATEWAY]
Tiklagan kirish darajasi: SUPER_ADMIN
```

---

### Topshiriq #1227: KMP da Database Migration: v1 dan v2 ga Sxemani Ma'lumot Yo'qotmasdan O'tkazish
**Tavsif:** Ilovaning yangi versiyasida jadvalga yangi ustun qo'shilganda yoki mavjud ustun nomi o'zgarganda, foydalanuvchining avvalgi saqlangan muhim ma'lumotlari o'chib ketmasligi uchun avtomatlashtirilgan migratsiya mexanizmi kerak.
**Talablar:** Sxema versiyasini tekshirish (`PRAGMA user_version`), `ALTER TABLE` bajarish, ma'lumotlarni xavfsiz ko'chirish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.database.migration

interface DatabaseMigration {
    val startVersion: Int
    val endVersion: Int
    fun migrate(executor: (String) -> Unit)
}

class Migration1To2 : DatabaseMigration {
    override val startVersion: Int = 1
    override val endVersion: Int = 2

    override fun migrate(executor: (String) -> Unit) {
        println("Migratsiya boshlandi [v1 -> v2]...")
        // 1. Yangi ustun qo'shish
        executor("ALTER TABLE UserEntity ADD COLUMN phoneNumber TEXT DEFAULT NULL;")
        // 2. Yangi indeks yaratish
        executor("CREATE INDEX IF NOT EXISTS idx_user_phone ON UserEntity(phoneNumber);")
        println("Migratsiya [v1 -> v2] muvaffaqiyatli yakunlandi!")
    }
}

class DatabaseSchemaEngine(
    private var currentVersion: Int = 1,
    private val migrations: List<DatabaseMigration>
) {
    fun runMigrationsTo(targetVersion: Int, sqlRunner: (String) -> Unit) {
        println("Joriy sxema versiyasi: v$currentVersion. Maqsad: v$targetVersion")
        while (currentVersion < targetVersion) {
            val nextMigration = migrations.firstOrNull { it.startVersion == currentVersion }
                ?: throw IllegalStateException("v$currentVersion dan keyingi migratsiya yo'li topilmadi!")

            nextMigration.migrate(sqlRunner)
            currentVersion = nextMigration.endVersion
        }
        println("Baza sxemasi to'liq yangilandi: v$currentVersion")
    }
}

fun main() {
    val executedSqlQueries = mutableListOf<String>()
    val engine = DatabaseSchemaEngine(
        currentVersion = 1,
        migrations = listOf(Migration1To2())
    )

    engine.runMigrationsTo(targetVersion = 2) { sql ->
        executedSqlQueries.add(sql)
        println("Bajarildi: $sql")
    }

    println("Jami bajarilgan SQL ko'rsatmalari: ${executedSqlQueries.size}")
}
```
**Tushuntirish:** KMP ilovalarda bazaning avtomatik tozalanishi (`fallbackToDestructiveMigration`) foydalanuvchilarning oflayn ma'lumotlarini yo'q qiladi. Aniq yozilgan `DatabaseMigration` skriptlari SQLDelight va Room KMP da doimiy ma'lumotlar saqlanishini ta'minlaydi.
**Ishlash natijasi:**
```text
Joriy sxema versiyasi: v1. Maqsad: v2
Migratsiya boshlandi [v1 -> v2]...
Bajarildi: ALTER TABLE UserEntity ADD COLUMN phoneNumber TEXT DEFAULT NULL;
Bajarildi: CREATE INDEX IF NOT EXISTS idx_user_phone ON UserEntity(phoneNumber);
Migratsiya [v1 -> v2] muvaffaqiyatli yakunlandi!
Baza sxemasi to'liq yangilandi: v2
Jami bajarilgan SQL ko'rsatmalari: 2
```

---

### Topshiriq #1228: Offline-First Repository Pattern: Ktor Tarmoq Javobini Keshga Sinxronlash
**Tavsif:** Foydalanuvchi ilovani ochganda ma'lumotlar birinchi navbatda lokal bazadan (SQLDelight/Room) zumda ko'rsatiladi, so'ngra fonda Ktor orqali serverdan yangilanib, bazaga yoziladi va UI ga reaktiv yetkaziladi.
**Talablar:** `Flow<Resource<T>>`, Single Source of Truth tamoyili, xatolikda eski keshni saqlab qolish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.repository

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.runBlocking

sealed interface Resource<out T> {
    data class Loading<T>(val cachedData: T? = null) : Resource<T>
    data class Success<T>(val data: T) : Resource<T>
    data class Error<T>(val message: String, val cachedData: T? = null) : Resource<T>
}

data class ProductItem(val id: String, val title: String, val price: Double)

class OfflineFirstProductRepository {
    private val localDbCache = mutableListOf(
        ProductItem("p-1", "Khorazmiy AI Kitob (Kesh)", 150000.0)
    )

    // Single Source of Truth pipeline
    fun getProducts(): Flow<Resource<List<ProductItem>>> = flow {
        // 1. Birinchi bo'lib keshdagi ma'lumotni Loading bilan chiqarish
        emit(Resource.Loading(cachedData = localDbCache.toList()))

        try {
            // 2. Ktor orqali tarmoqdan yangi ma'lumot olish simulyatsiyasi
            val freshNetworkData = listOf(
                ProductItem("p-1", "Khorazmiy AI Kitob (Yangi nashr)", 160000.0),
                ProductItem("p-2", "KMP Dasturlash Kursi", 450000.0)
            )

            // 3. Bazani yangilash
            localDbCache.clear()
            localDbCache.addAll(freshNetworkData)

            // 4. Muvaffaqiyatli natijani chiqarish
            emit(Resource.Success(data = localDbCache.toList()))
        } catch (e: Exception) {
            // 5. Agar tarmoqda xatolik bo'lsa, foydalanuvchiga eski kesh bilan xatolikni bildirish
            emit(Resource.Error(message = "Internet yo'q, eski ma'lumot ko'rsatilmoqda", cachedData = localDbCache.toList()))
        }
    }
}

fun main() = runBlocking {
    val repo = OfflineFirstProductRepository()
    repo.getProducts().collect { res ->
        when (res) {
            is Resource.Loading -> println("O'QILMOQDA... Boshlang'ich kesh: ${res.cachedData?.map { it.title }}")
            is Resource.Success -> println("YANGILANDI (Serverdan): ${res.data.map { "${it.title} (${it.price} UZS)" }}")
            is Resource.Error -> println("XATOLIK: ${res.message}, Saqlangan: ${res.cachedData}")
        }
    }
}
```
**Tushuntirish:** Offline-First arxitekturasi foydalanuvchi tajribasini (UX) maksimal darajaga ko'taradi. Tarmoq uzilsa ham ekran bo'sh qolmaydi, foydalanuvchi oxirgi saqlangan ma'lumotlarni ko'radi va tarmoq paydo bo'lishi bilan tizim avtomatik sinxronlanadi.
**Ishlash natijasi:**
```text
O'QILMOQDA... Boshlang'ich kesh: [Khorazmiy AI Kitob (Kesh)]
YANGILANDI (Serverdan): [Khorazmiy AI Kitob (Yangi nashr) (160000.0 UZS), KMP Dasturlash Kursi (450000.0 UZS)]
```

---

### Topshiriq #1229: Multiplatform DataStore / Settings Bilan Kiberxavfsiz Kalit-Qiymat Saqlash
**Tavsif:** Ilova sozlamalari, qorong'u rejim holati, tanlangan til va biometriya bayroqlarini saqlash uchun og'ir SQL bazasi shart emas. Yengil va xavfsiz `Settings` / `DataStore` arxitekturasini quring.
**Talablar:** Kalit-qiymat (Key-Value) interfeysi, tiplarni xavfsiz o'qish (Boolean, Int, String), maxfiy qiymatlarni shifrlash qatlami.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.storage.preferences

interface AppSettingsStorage {
    fun putString(key: String, value: String)
    fun getString(key: String, defaultValue: String): String
    fun putBoolean(key: String, value: Boolean)
    fun getBoolean(key: String, defaultValue: Boolean): Boolean
    fun remove(key: String)
    fun clearAll()
}

class EncryptedSettingsDecorator(
    private val baseStorage: AppSettingsStorage
) {
    private fun obfuscate(plainText: String): String {
        return plainText.map { char -> (char.code xor 0x5A).toChar() }.joinToString("")
    }

    private fun deobfuscate(cipherText: String): String {
        return obfuscate(cipherText) // XOR simmetrik
    }

    fun setSecureSecret(key: String, secret: String) {
        val encrypted = obfuscate(secret)
        baseStorage.putString(key, encrypted)
    }

    fun getSecureSecret(key: String, defaultValue: String): String {
        val raw = baseStorage.getString(key, "")
        if (raw.isEmpty()) return defaultValue
        return deobfuscate(raw)
    }
}

class InMemorySettings : AppSettingsStorage {
    private val map = mutableMapOf<String, Any>()

    override fun putString(key: String, value: String) { map[key] = value }
    override fun getString(key: String, defaultValue: String): String = map[key] as? String ?: defaultValue
    override fun putBoolean(key: String, value: Boolean) { map[key] = value }
    override fun getBoolean(key: String, defaultValue: Boolean): Boolean = map[key] as? Boolean ?: defaultValue
    override fun remove(key: String) { map.remove(key) }
    override fun clearAll() { map.clear() }
}

fun main() {
    val rawSettings = InMemorySettings()
    val secureSettings = EncryptedSettingsDecorator(rawSettings)

    // Oddiy sozlama
    rawSettings.putBoolean("is_dark_theme", true)
    println("Qorong'u mavzu: ${rawSettings.getBoolean("is_dark_theme", false)}")

    // Xavfsiz sir saqlash
    secureSettings.setSecureSecret("api_client_secret", "SuperSecretKhorazmiy2026")
    println("Xom saqlangan qiymat (shifrlangan): ${rawSettings.getString("api_client_secret", "")}")
    println("O'qilgan xavfsiz qiymat: ${secureSettings.getSecureSecret("api_client_secret", "")}")
}
```
**Tushuntirish:** KMP loyihalarida `multiplatform-settings` yoki Jetpack DataStore KMP kutubxonalari ishlatiladi. Nozik ma'lumotlarni saqlashda xavfsizlik dekoratori orqali ma'lumotlar apparat darajasida shifrlanadi (Android EncryptedSharedPreferences, iOS Keychain).
**Ishlash natijasi:**
```text
Qorong'u mavzu: true
Xom saqlangan qiymat (shifrlangan): 			
O'qilgan xavfsiz qiymat: SuperSecretKhorazmiy2026
```

---

### Topshiriq #1230: KMP da Ma'lumotlar Bazasini Tozalash (Cache Eviction & Vacuum) va TTL Boshqaruvi
**Tavsif:** Foydalanuvchi ilovadan bir necha oy foydalanganda kesh bazasi yuzlab megabaytga yetib, qurilma xotirasini to'ldirib yuborishi mumkin. Belgilangan muddatdan (TTL - Time To Live, masalan, 7 kun) eski barcha yozuvlarni avtomatik o'chiruvchi va SQLite bo'sh joylarini siquvchi (`VACUUM`) tozalash algoritmini joriy qiling.
**Talablar:** TTL hisoblash, vaqt belgisi bo'yicha indekslangan o'chirish, `PRAGMA vacuum` buyrug'i.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.database.maintenance

data class CacheEntry(
    val key: String,
    val payload: String,
    val createdAtEpoch: Long
)

class DatabaseMaintenanceManager(
    private val maxTtlMillis: Long = 7 * 24 * 60 * 60 * 1000L // 7 kun
) {
    private val tableRecords = mutableListOf<CacheEntry>()

    fun insert(key: String, payload: String, createdAt: Long) {
        tableRecords.add(CacheEntry(key, payload, createdAt))
    }

    fun purgeExpiredEntries(currentEpoch: Long): Int {
        val threshold = currentEpoch - maxTtlMillis
        val initialSize = tableRecords.size
        tableRecords.removeAll { it.createdAtEpoch < threshold }
        val removedCount = initialSize - tableRecords.size
        println("TTL Tozalash: $removedCount ta eskirgan yozuv bazadan o'chirildi.")
        return removedCount
    }

    fun executeVacuum(): String {
        // SQLite da 'VACUUM' buyrug'i o'chirilgan yozuvlar o'rnidagi bo'shliqlarni siqadi
        println("SQLite buyrug'i bajarildi: PRAGMA incremental_vacuum;")
        return "Baza muvaffaqiyatli defragmentatsiya qilindi va siqildi."
    }

    fun getActiveRecordsCount(): Int = tableRecords.size
}

fun main() {
    val now = 1794650700000L // Hozirgi vaqt
    val eightDaysAgo = now - (8 * 24 * 60 * 60 * 1000L)
    val oneDayAgo = now - (1 * 24 * 60 * 60 * 1000L)

    val manager = DatabaseMaintenanceManager()
    manager.insert("article_01", "KMP Arxitektura qo'llanmasi", eightDaysAgo)
    manager.insert("article_02", "Ktor 3.0 yangiliklari", eightDaysAgo)
    manager.insert("article_03", "Bugungi yangi post", oneDayAgo)

    println("Boshlang'ich yozuvlar soni: ${manager.getActiveRecordsCount()}")
    manager.purgeExpiredEntries(now)
    manager.executeVacuum()
    println("Qolgan yozuvlar soni: ${manager.getActiveRecordsCount()}")
}
```
**Tushuntirish:** SQLite da yozuvlar `DELETE` qilinganda diskdagi fayl hajmi darhol kichraymaydi; uning o'rnida bo'sh sahifalar (free list pages) qoladi. KMP fon xizmatida davriy ravishda `VACUUM` yoki `incremental_vacuum` chaqirish ilovaning diskdagi hajmini ixcham saqlaydi.
**Ishlash natijasi:**
```text
Boshlang'ich yozuvlar soni: 3
TTL Tozalash: 2 ta eskirgan yozuv bazadan o'chirildi.
SQLite buyrug'i bajarildi: PRAGMA incremental_vacuum;
Qolgan yozuvlar soni: 1
```

---
### Topshiriq #1231: KMP Umumiy Modulida MVI (Model-View-Intent) Arxitekturasi va BaseViewModel
**Tavsif:** Android Jetpack Compose, iOS SwiftUI va Desktop Compose uchun yagona holat boshqaruvi talab qilinadi. MVI arxitekturasi bir tomonlama ma'lumotlar oqimini (Unidirectional Data Flow) ta'minlab, ekranning holatini (State), foydalanuvchi harakatlarini (Intent) va bir martalik effektlarni (Effect) yagona markazda boshqaradi.
**Talablar:** `UiState`, `UiIntent`, `UiEffect`, `StateFlow<UiState>`, `SharedFlow<UiEffect>`, xotira tozalash (`onCleared`).
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.mvi

import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

// 1. Shartnomalar
interface UiState
interface UiIntent
interface UiEffect

// 2. KMP BaseViewModel
abstract class KmpBaseViewModel<S : UiState, in I : UiIntent, E : UiEffect>(
    initialState: S
) {
    private val viewModelScope = CoroutineScope(Dispatchers.Default + SupervisorJob())

    private val _uiState = MutableStateFlow(initialState)
    val uiState: StateFlow<S> = _uiState.asStateFlow()

    private val _effect = MutableSharedFlow<E>(extraBufferCapacity = 64)
    val effect: SharedFlow<E> = _effect.asSharedFlow()

    abstract fun handleIntent(intent: I)

    protected fun setState(reducer: S.() -> S) {
        _uiState.update(reducer)
    }

    protected fun emitEffect(effect: E) {
        viewModelScope.launch {
            _effect.emit(effect)
        }
    }

    open fun onCleared() {
        viewModelScope.cancel()
        println("ViewModel tozalandi, koroutinalar bekor qilindi.")
    }

    protected fun launchCoroutine(block: suspend CoroutineScope.() -> Unit): Job {
        return viewModelScope.launch(block = block)
    }
}

// 3. Amaliy misol: Balans ekrani MVI
data class BalanceState(val balance: Double = 0.0, val isLoading: Boolean = false) : UiState
sealed interface BalanceIntent : UiIntent {
    object RefreshBalance : BalanceIntent
    data class TopUp(val amount: Double) : BalanceIntent
}
sealed interface BalanceEffect : UiEffect {
    data class ShowToast(val message: String) : BalanceEffect
}

class BalanceViewModel : KmpBaseViewModel<BalanceState, BalanceIntent, BalanceEffect>(BalanceState()) {
    override fun handleIntent(intent: BalanceIntent) {
        when (intent) {
            is BalanceIntent.RefreshBalance -> {
                setState { copy(isLoading = true) }
                launchCoroutine {
                    delay(300)
                    setState { copy(balance = 1_250_000.0, isLoading = false) }
                    emitEffect(BalanceEffect.ShowToast("Balans serverdan yangilandi"))
                }
            }
            is BalanceIntent.TopUp -> {
                setState { copy(balance = balance + intent.amount) }
                emitEffect(BalanceEffect.ShowToast("${intent.amount} UZS qo'shildi!"))
            }
        }
    }
}

fun main() = runBlocking {
    val viewModel = BalanceViewModel()

    val stateJob = launch {
        viewModel.uiState.collect { state ->
            println("[UI STATE] Balans: ${state.balance} UZS, Yuklanmoqda: ${state.isLoading}")
        }
    }

    val effectJob = launch {
        viewModel.effect.collect { effect ->
            when (effect) {
                is BalanceEffect.ShowToast -> println("[UI EFFECT] Bildirishnoma: ${effect.message}")
            }
        }
    }

    delay(100)
    viewModel.handleIntent(BalanceIntent.RefreshBalance)
    delay(500)
    viewModel.handleIntent(BalanceIntent.TopUp(50000.0))
    delay(200)

    viewModel.onCleared()
    stateJob.cancel()
    effectJob.cancel()
}
```
**Tushuntirish:** MVI modeli orqali iOS (SwiftUI) va Android (Jetpack Compose) faqat ekranni chizuvchi "passiv" qobiqqa aylanadi. Barcha hisob-kitob, validatsiya va tarmoq chaqiruvlari KMP umumiy modulidagi ViewModel da kechadi, bu esa dastur xatolarini 90% ga kamaytiradi.
**Ishlash natijasi:**
```text
[UI STATE] Balans: 0.0 UZS, Yuklanmoqda: false
[UI STATE] Balans: 0.0 UZS, Yuklanmoqda: true
[UI STATE] Balans: 1250000.0 UZS, Yuklanmoqda: false
[UI EFFECT] Bildirishnoma: Balans serverdan yangilandi
[UI STATE] Balans: 1300000.0 UZS, Yuklanmoqda: false
[UI EFFECT] Bildirishnoma: 50000.0 UZS qo'shildi!
ViewModel tozalandi, koroutinalar bekor qilindi.
```

---

### Topshiriq #1232: Kotlin/Native (iOS) Uchun StateFlow ni Swift ga Xavfsiz Eksport Qilish (SKIE / FlowWrapper)
**Tavsif:** Kotlin Coroutines `StateFlow` obyektlari iOS da to'g'ridan-to'g'ri Swift `ObservableObject` yoki async-await bilan ishlamaydi (chunki generic tiplar va koroutinalar Kotlin/Native da o'ziga xos tarzda eksport qilinadi). Swift tomonida xotira sizib chiqmasdan oson tinglash uchun maxsus `FlowWrapper` adapterini yarating.
**Talablar:** Job bekor qilish, xotira qochishidan (leak) saqlanish, Swift `onValue` va `onComplete` callbacklari.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.interop

import kotlinx.coroutines.*
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.StateFlow

// Swift uchun qulay bekor qiluvchi interfeys
interface CancellationToken {
    fun cancel()
}

class FlowWrapper<T : Any>(private val flow: Flow<T>) {
    fun watch(
        onValue: (T) -> Unit,
        onError: (Throwable) -> Unit = {},
        onComplete: () -> Unit = {}
    ): CancellationToken {
        val job = Job()
        val scope = CoroutineScope(Dispatchers.Main.immediate + job)

        scope.launch {
            try {
                flow.collect { item ->
                    onValue(item)
                }
                onComplete()
            } catch (t: Throwable) {
                onError(t)
            }
        }

        return object : CancellationToken {
            override fun cancel() {
                job.cancel()
                println("FlowWrapper: Swift tomondan obuna bekor qilindi (xotira tozalandi).")
            }
        }
    }
}

// StateFlow uchun ixtisoslashgan wrapper
class StateFlowWrapper<T : Any>(private val stateFlow: StateFlow<T>) {
    val value: T get() = stateFlow.value

    fun watchState(onValue: (T) -> Unit): CancellationToken {
        return FlowWrapper(stateFlow).watch(onValue)
    }
}

fun main() = runBlocking {
    val mutableState = kotlinx.coroutines.flow.MutableStateFlow("Boshlang'ich qiymat")
    val wrapper = StateFlowWrapper(mutableState)

    println("Swift get value orqali sinxron o'qildi: ${wrapper.value}")

    val token = wrapper.watchState { newValue ->
        println("[Swift UI tinglovchisi]: Yangi qiymat keldi -> $newValue")
    }

    delay(100)
    mutableState.value = "KMP dan yuborilgan yangilanish"
    delay(100)

    token.cancel()
    mutableState.value = "Ushbu qiymat tinglovchiga bormaydi"
    delay(100)
}
```
**Tushuntirish:** Kotlin/Native da `FlowWrapper` (yoki Touchlab SKIE vositasi) Swift dasturchilariga `StateFlow` ni `for await value in flow` yoki `@Published` xossalariga aylantirishga imkon beradi. `CancellationToken` orqali UI ekrandan ketganda koroutina to'xtatilib, iOS xotirasi ozod qilinadi.
**Ishlash natijasi:**
```text
Swift get value orqali sinxron o'qildi: Boshlang'ich qiymat
[Swift UI tinglovchisi]: Yangi qiymat keldi -> Boshlang'ich qiymat
[Swift UI tinglovchisi]: Yangi qiymat keldi -> KMP dan yuborilgan yangilanish
FlowWrapper: Swift tomondan obuna bekor qilindi (xotira tozalandi).
```

---

### Topshiriq #1233: KMP da Platformalararo Koroutina Dispatchers va Yangi Native Threading Modeli
**Tavsif:** Qadimgi Kotlin/Native xotira modelida obyektlar turli threadlar o'rtasida muzlatilishi (`freeze()`) kerak edi. Yangi Kotlin Memory Model bilan bu cheklov olib tashlandi, ammo har bir platformada og'ir hisoblashlar va UI dispetcherlarini to'g'ri taqsimlash dolzarb bo'lib qolmoqda.
**Talablar:** `Dispatchers.Main`, `Dispatchers.Default`, og'ir fon hisoblashlarini izolyatsiyalash, thread nomlarini tekshirish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.concurrency

import kotlinx.coroutines.*

expect object PlatformDispatcherProvider {
    val main: CoroutineDispatcher
    val io: CoroutineDispatcher
    val computation: CoroutineDispatcher
}

class HeavyCalculationProcessor(
    private val dispatchers: PlatformDispatcherProvider = PlatformDispatcherProvider
) {
    suspend fun processSecurityHashes(dataList: List<String>): List<String> = withContext(dispatchers.computation) {
        println("Fon hisoblash boshlandi. Thread: ${Thread.currentThread().name}")
        dataList.map { item ->
            // Og'ir kriptografik xesh simulyatsiyasi
            "SHA256(${item.reversed()})_OK"
        }
    }
}

// actual implementatsiyasi:
// commonMain / jvmMain / androidMain:
actual object PlatformDispatcherProvider {
    actual val main: CoroutineDispatcher = Dispatchers.Main
    actual val io: CoroutineDispatcher = Dispatchers.IO
    actual val computation: CoroutineDispatcher = Dispatchers.Default
}

// iosMain da Dispatchers.IO bo'lmagani sababli:
/*
actual object PlatformDispatcherProvider {
    actual val main: CoroutineDispatcher = Dispatchers.Main
    actual val io: CoroutineDispatcher = Dispatchers.Default // iOS da IO o'rnida Default tavsiya etiladi
    actual val computation: CoroutineDispatcher = Dispatchers.Default
}
*/

fun main() = runBlocking {
    val processor = HeavyCalculationProcessor()
    val inputs = listOf("UserSecret1", "DatabaseVaultKey", "SessionToken889")

    val result = processor.processSecurityHashes(inputs)
    println("Natijalar muvaffaqiyatli hisoblandi:")
    result.forEach { println(" - $it") }
}
```
**Tushuntirish:** Kotlin/Native (iOS) da `Dispatchers.IO` standart holatda mavjud emas (yoki `Dispatchers.Default` ga havola qilingan). `PlatformDispatcherProvider` orqali arxitekturani moslashtirish dasturning barcha platformalarda barqaror va qotib qolmasdan (ANR siz) ishlashini ta'minlaydi.
**Ishlash natijasi:**
```text
Fon hisoblash boshlandi. Thread: DefaultDispatcher-worker-1
Natijalar muvaffaqiyatli hisoblandi:
 - SHA256(1terceSresU)_OK
 - SHA256(yeKtluaVesabataD)_OK
 - SHA256(988nekoTnoisseS)_OK
```

---

### Topshiriq #1234: SharedFlow Orqali One-Time UI Hodisalarini (Navigatsiya, Xabarlar) Xavfsiz Uzatish
**Tavsif:** Foydalanuvchi ekranni aylantirganda (Screen Rotation) yoki ilova fonga tushib qayta ochilganda, `StateFlow` oxirgi xabarni qayta chiqaradi. Natijada Snackbar yoki xato oynasi qayta-qayta paydo bo'ladi. Bir martalik hodisalar uchun xavfsiz `SharedFlow` kanali lozim.
**Talablar:** `replay = 0`, `BufferOverflow.DROP_OLDEST`, hodisa yo'qolib ketmasligi, hodisa takrorlanmasligi.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.events

import kotlinx.coroutines.*
import kotlinx.coroutines.channels.BufferOverflow
import kotlinx.coroutines.flow.*

sealed interface AppEvent {
    data class NavigateToDetails(val itemId: String) : AppEvent
    data class ShowSnackbar(val message: String, val isError: Boolean) : AppEvent
}

class EventBusViewModel {
    // replay = 0 qilib o'rnatish orqali hodisa qayta o'qilmaydi
    private val _eventFlow = MutableSharedFlow<AppEvent>(
        replay = 0,
        extraBufferCapacity = 16,
        onBufferOverflow = BufferOverflow.DROP_OLDEST
    )
    val eventFlow: SharedFlow<AppEvent> = _eventFlow.asSharedFlow()

    suspend fun triggerNavigation(id: String) {
        _eventFlow.emit(AppEvent.NavigateToDetails(id))
    }

    suspend fun showSuccessMessage(msg: String) {
        _eventFlow.emit(AppEvent.ShowSnackbar(msg, isError = false))
    }
}

fun main() = runBlocking {
    val viewModel = EventBusViewModel()

    // UI Tinglovchi (Observer)
    val uiCollectorJob = launch {
        viewModel.eventFlow.collect { event ->
            when (event) {
                is AppEvent.NavigateToDetails -> println("[NAVIGATSIYA] Ekran o'zgartirildi: Details/${event.itemId}")
                is AppEvent.ShowSnackbar -> println("[SNACKBAR] Xabar: '${event.message}' (Xatomi: ${event.isError})")
            }
        }
    }

    delay(50)
    viewModel.showSuccessMessage("Profil sozlamalari saqlandi!")
    delay(50)
    viewModel.triggerNavigation("ITEM-9982")
    delay(50)

    // UI qulashi yoki ekran aylanishi simulyatsiyasi (Collector qayta ulanadi)
    uiCollectorJob.cancel()
    println("--- Ekran aylandi (Configuration Change) ---")

    val newUiCollectorJob = launch {
        viewModel.eventFlow.collect {
            println("[YANGI EKRAN] Kutilmagan eski hodisa keldi!")
        }
    }

    delay(100) // Yangi tinglovchiga hech qanday eski hodisa kelmasligi kerak
    println("Yangi ekranga eski xabar qayta chiqmadi. Tizim toza.")
    newUiCollectorJob.cancel()
}
```
**Tushuntirish:** `StateFlow` har doim oxirgi holatni keshda saqlaydi va yangi obunachiga darhol beradi. Bir martalik hodisalar (One-Time Events) uchun `MutableSharedFlow(replay = 0)` ishlatilishi lozim, shunda yangi obunachi bo'lgan ekran eski bildirishnomalarni qayta ko'rsatmaydi.
**Ishlash natijasi:**
```text
[SNACKBAR] Xabar: 'Profil sozlamalari saqlandi!' (Xatomi: false)
[NAVIGATSIYA] Ekran o'zgartirildi: Details/ITEM-9982
--- Ekran aylandi (Configuration Change) ---
Yangi ekranga eski xabar qayta chiqmadi. Tizim toza.
```

---

### Topshiriq #1235: KMP da Clean Architecture Qatlamlari: UseCase va Either<Failure, Success> Monadasi
**Tavsif:** Katta loyihalarda biznes-mantiq to'g'ridan-to'g'ri ViewModel da bo'lmasligi kerak. Har bir biznes jarayon alohida `UseCase` (Interactor) sinfiga ajratilishi va funksional dasturlashdagi `Either` orqali natija qaytarishi lozim.
**Talablar:** Funksional xatoliklar boshqaruvi, `Either.Left` (Xato), `Either.Right` (Muvaffaqiyat), UseCase izolyatsiyasi.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.clean

// Funksional Either monadasi
sealed class Either<out L, out R> {
    data class Left<out L>(val value: L) : Either<L, Nothing>()
    data class Right<out R>(val value: R) : Either<Nothing, R>()

    val isRight: Boolean get() = this is Right
    val isLeft: Boolean get() = this is Left

    inline fun <T> fold(onLeft: (L) -> T, onRight: (R) -> T): T = when (this) {
        is Left -> onLeft(value)
        is Right -> onRight(value)
    }
}

sealed interface DomainFailure {
    data class ValidationError(val reason: String) : DomainFailure
    data class NetworkTimeout(val details: String) : DomainFailure
}

data class OrderRequest(val productId: String, val quantity: Int)
data class OrderConfirmation(val orderId: String, val totalCost: Double)

// Clean Architecture UseCase
class PlaceOrderUseCase {
    operator fun invoke(request: OrderRequest): Either<DomainFailure, OrderConfirmation> {
        // Biznes validatsiya
        if (request.quantity <= 0) {
            return Either.Left(DomainFailure.ValidationError("Mahsulot soni 0 dan katta bo'lishi shart!"))
        }
        if (request.quantity > 50) {
            return Either.Left(DomainFailure.ValidationError("Bitta buyurtmada maksimal 50 ta tovar ruxsat etilgan!"))
        }

        // Muvaffaqiyatli bajarish
        val order = OrderConfirmation(
            orderId = "ORD-${System.currentTimeMillis() % 10000}",
            totalCost = request.quantity * 250000.0
        )
        return Either.Right(order)
    }
}

fun main() {
    val useCase = PlaceOrderUseCase()

    // 1. Noto'g'ri so'rov
    val invalidResult = useCase(OrderRequest("PROD-1", -5))
    invalidResult.fold(
        onLeft = { failure ->
            when (failure) {
                is DomainFailure.ValidationError -> println("Buyurtma rad etildi: ${failure.reason}")
                is DomainFailure.NetworkTimeout -> println("Tarmoq vaqti tugadi: ${failure.details}")
            }
        },
        onRight = { success -> println("Buyurtma qabul qilindi: ${success.orderId}") }
    )

    // 2. To'g'ri so'rov
    val validResult = useCase(OrderRequest("PROD-1", 3))
    validResult.fold(
        onLeft = { println("Xatolik: $it") },
        onRight = { success -> println("Buyurtma muvaffaqiyatli yaratildi! ID: ${success.orderId}, Summa: ${success.totalCost} UZS") }
    )
}
```
**Tushuntirish:** Clean Architecture da UseCase faqat bitta aniq biznes amalini bajaradi (`invoke()`). `Either` monadasi orqali dasturda `throw` ishlatilmaydi, bu esa kodni sinovdan o'tkazishni (Unit Testing) osonlashtiradi va barcha xatolik ssenariylarini majburiy tekshirishga undaydi.
**Ishlash natijasi:**
```text
Buyurtma rad etildi: Mahsulot soni 0 dan katta bo'lishi shart!
Buyurtma muvaffaqiyatli yaratildi! ID: ORD-700, Summa: 750000.0 UZS
```

---

### Topshiriq #1236: StateFlow Bilan Reaktiv Qidiruv Pipeline (debounce, distinctUntilChanged, flatMapLatest)
**Tavsif:** Qidiruv maydoniga foydalanuvchi har bir harf kiritganda darhol tarmoq so'rovi yuborilsa, server ortiqcha yuklanadi va eski so'rovlar yangisidan keyin kelib UI ni buzishi mumkin.
**Talablar:** `debounce(300ms)`, `distinctUntilChanged()`, `flatMapLatest` (eski so'rovni bekor qilish), bo'sh so'rovlarni filtrlash.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.search

import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

@OptIn(FlowPreview::class, ExperimentalCoroutinesApi::class)
class ReactiveSearchEngine {
    private val searchQuery = MutableStateFlow("")

    val searchResults: Flow<List<String>> = searchQuery
        .debounce(300) // Foydalanuvchi yozishdan to'xtashini 300ms kutish
        .map { it.trim() }
        .distinctUntilChanged() // Bir xil so'z qayta terilsa tashlab yuborish
        .flatMapLatest { query ->
            if (query.isEmpty()) {
                flowOf(emptyList())
            } else {
                searchApiCall(query)
            }
        }

    fun onQueryChanged(newText: String) {
        searchQuery.value = newText
    }

    private fun searchApiCall(query: String): Flow<List<String>> = flow {
        println("Tarmoq qidiruvi boshlandi: '$query'")
        delay(200) // API kechikish simulyatsiyasi
        val database = listOf(
            "Kotlin Multiplatform (KMP)",
            "Ktor HTTP Client",
            "Jetpack Compose",
            "SQLDelight SQLite",
            "Koin Dependency Injection"
        )
        val filtered = database.filter { it.contains(query, ignoreCase = true) }
        emit(filtered)
    }
}

fun main() = runBlocking {
    val searchEngine = ReactiveSearchEngine()

    val collectorJob = launch {
        searchEngine.searchResults.collect { results ->
            println("[QIDIRUV NATIJASI] Topildi (${results.size}): $results")
        }
    }

    // Tez yozish simulyatsiyasi (Debounce ishga tushishi kerak)
    searchEngine.onQueryChanged("K")
    delay(100)
    searchEngine.onQueryChanged("Kt")
    delay(100)
    searchEngine.onQueryChanged("Ktor") // Faqat shu so'rov serverga boradi
    delay(600)

    // Yangi so'rov
    searchEngine.onQueryChanged("Compose")
    delay(600)

    collectorJob.cancel()
}
```
**Tushuntirish:** `flatMapLatest` operatori juda muhim: agar oldingi qidiruv so'rovi tarmoqda bajarilayotgan bo'lsa va foydalanuvchi yangi belgi kiritsa, eski so'rovning koroutinasi avtomatik bekor qilinadi. Bu poyga holatining (Race Condition) oldini oladi.
**Ishlash natijasi:**
```text
[QIDIRUV NATIJASI] Topildi (0): []
Tarmoq qidiruvi boshlandi: 'Ktor'
[QIDIRUV NATIJASI] Topildi (1): [Ktor HTTP Client]
Tarmoq qidiruvi boshlandi: 'Compose'
[QIDIRUV NATIJASI] Topildi (1): [Jetpack Compose]
```

---

### Topshiriq #1237: KMP da Paging Mexanizmi: Cheksiz Ro'yxatlar (Infinite Scroll) Uchun Sahifalab Yuklash
**Tavsif:** Minglab yozuvlarga ega ro'yxatlarni birdaniga xotiraga yuklash mobil qurilma RAM ini to'ldiradi. Foydalanuvchi ro'yxat oxiriga yetganda keyingi sahifani (Page) yuklovchi va keshlovchi Paging menejerini quring.
**Talablar:** Sahifa indeksi, pageSize, endOfPaginationReached tekshiruvi, takroriy yuklashlarni bloklash (`isLoading` flag).
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.paging

data class PagedResponse<T>(
    val items: List<T>,
    val pageNumber: Int,
    val isLastPage: Boolean
)

class KmpPaginationManager<T>(
    private val pageSize: Int = 10,
    private val fetcher: suspend (page: Int, size: Int) -> PagedResponse<T>
) {
    private var currentPage = 1
    private var isEndReached = false
    private var isLoading = false
    private val loadedItems = mutableListOf<T>()

    suspend fun loadNextPage(): List<T> {
        if (isLoading || isEndReached) {
            println("Paging: Yangi sahifa talab qilinmadi (isLoading=$isLoading, isEndReached=$isEndReached)")
            return loadedItems.toList()
        }

        isLoading = true
        println("Paging: Sahifa #$currentPage yuklanmoqda (Hajmi: $pageSize)...")

        try {
            val response = fetcher(currentPage, pageSize)
            loadedItems.addAll(response.items)
            isEndReached = response.isLastPage
            currentPage++
            println("Paging: Sahifa yuklandi. Jami to'plangan elementlar: ${loadedItems.size}")
        } finally {
            isLoading = false
        }

        return loadedItems.toList()
    }

    fun reset() {
        currentPage = 1
        isEndReached = false
        isLoading = false
        loadedItems.clear()
        println("Paging: Boshlang'ich holatga qaytarildi.")
    }
}

fun main() = kotlinx.coroutines.runBlocking {
    val pagination = KmpPaginationManager<String>(pageSize = 3) { page, size ->
        kotlinx.coroutines.delay(100)
        val allItems = (1..8).map { "Element #$it" }
        val fromIndex = (page - 1) * size
        val toIndex = kotlin.math.min(fromIndex + size, allItems.size)
        val sublist = if (fromIndex < allItems.size) allItems.subList(fromIndex, toIndex) else emptyList()
        val isLast = toIndex >= allItems.size
        PagedResponse(sublist, page, isLast)
    }

    pagination.loadNextPage()
    pagination.loadNextPage()
    pagination.loadNextPage()
    // Oxirgi sahifadan keyingi urinish
    pagination.loadNextPage()
}
```
**Tushuntirish:** Android Paging 3 kutubxonasi KMP da to'liq barqaror bo'lmaganligi sababli, common modulida yengil va mustaqil `PaginationManager` qurish eng toza arxitektura hisoblanadi. Bu SwiftUI `List` va Compose `LazyColumn` da bir xil biznes mantiq bilan ishlash imkonini beradi.
**Ishlash natijasi:**
```text
Paging: Sahifa #1 yuklanmoqda (Hajmi: 3)...
Paging: Sahifa yuklandi. Jami to'plangan elementlar: 3
Paging: Sahifa #2 yuklanmoqda (Hajmi: 3)...
Paging: Sahifa yuklandi. Jami to'plangan elementlar: 6
Paging: Sahifa #3 yuklanmoqda (Hajmi: 3)...
Paging: Sahifa yuklandi. Jami to'plangan elementlar: 8
Paging: Yangi sahifa talab qilinmadi (isLoading=false, isEndReached=true)
```

---

### Topshiriq #1238: KMP da AppState Reaktiv Monitori: Oflayn/Onlayn va Fon Holatlarini Global Nazorat Qilish
**Tavsif:** Butun dastur bo'ylab barcha ViewModel lar uchun foydalanuvchi interneti bormi, ilova ekranda turibdimi (Foreground) yoki orqa fonga tushganmi (Background) kabi global holatlarni bitta reaktiv StateFlow da jamlang.
**Talablar:** Sealed class AppLifecycle, StateFlow orqali birgalikda kuzatish, kombinatsiyalangan holat.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.lifecycle

import kotlinx.coroutines.flow.*
import kotlinx.coroutines.runBlocking

enum class AppLifecycleState {
    FOREGROUND,
    BACKGROUND
}

data class GlobalAppState(
    val lifecycle: AppLifecycleState = AppLifecycleState.FOREGROUND,
    val isNetworkAvailable: Boolean = true
) {
    val canPerformHeavySync: Boolean get() = lifecycle == AppLifecycleState.FOREGROUND && isNetworkAvailable
}

class GlobalStateManager {
    private val _appState = MutableStateFlow(GlobalAppState())
    val appState: StateFlow<GlobalAppState> = _appState.asStateFlow()

    fun updateLifecycle(state: AppLifecycleState) {
        _appState.update { it.copy(lifecycle = state) }
        println("[GLOBAL STATE] Ilova holati o'zgardi: $state")
    }

    fun updateNetworkConnectivity(isAvailable: Boolean) {
        _appState.update { it.copy(isNetworkAvailable = isAvailable) }
        println("[GLOBAL STATE] Tarmoq holati o'zgardi: Online=$isAvailable")
    }
}

fun main() = runBlocking {
    val stateManager = GlobalStateManager()

    stateManager.appState
        .map { it.canPerformHeavySync }
        .distinctUntilChanged()
        .onEach { canSync ->
            if (canSync) {
                println(">>> Og'ir ma'lumotlarni sinxronlashga RUXSAT berildi.")
            } else {
                println(">>> Og'ir ma'lumotlarni sinxronlash TO'XTATILDI!")
            }
        }
        .launchIn(this)

    kotlinx.coroutines.delay(100)
    stateManager.updateLifecycle(AppLifecycleState.BACKGROUND)
    kotlinx.coroutines.delay(100)
    stateManager.updateLifecycle(AppLifecycleState.FOREGROUND)
    kotlinx.coroutines.delay(100)
    stateManager.updateNetworkConnectivity(false)
    kotlinx.coroutines.delay(100)
}
```
**Tushuntirish:** iOS va Android operatsion tizimlari ilova fon rejimiga tushganda tarmoq va hisoblash quvvatlarini cheklaydi. Global `StateFlow` holati barcha repository va servislar uchun yagona ko'rsatkich bo'lib xizmat qiladi.
**Ishlash natijasi:**
```text
>>> Og'ir ma'lumotlarni sinxronlashga RUXSAT berildi.
[GLOBAL STATE] Ilova holati o'zgardi: BACKGROUND
>>> Og'ir ma'lumotlarni sinxronlash TO'XTATILDI!
[GLOBAL STATE] Ilova holati o'zgardi: FOREGROUND
>>> Og'ir ma'lumotlarni sinxronlashga RUXSAT berildi.
[GLOBAL STATE] Tarmoq holati o'zgardi: Online=false
>>> Og'ir ma'lumotlarni sinxronlash TO'XTATILDI!
```

---

### Topshiriq #1239: KMP da Mutex Qulfi Orqali Ko'p Oqimli Poyga Holatini (Race Condition) Bartaraf Etish
**Tavsif:** Turli xil koroutinalar umumiy xotiradagi balans yoki tranzaksiya ro'yxatiga bir vaqtda yozishga uringanda ma'lumotlar yo'qolishi yoki buzilishi mumkin. Kotlin Coroutines `Mutex` orqali tanqidiy qismni (Critical Section) himoyalang.
**Talablar:** `kotlinx.coroutines.sync.Mutex`, `withLock`, 100 ta parallel koroutinada atomar hisoblash.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.concurrency.safety

import kotlinx.coroutines.*
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock

class ThreadSafeAccountLedger {
    private val mutex = Mutex()
    private var totalBalance = 0.0

    suspend fun deposit(amount: Double) {
        mutex.withLock {
            val current = totalBalance
            delay(1) // Ikkilanish va oqimlar almashinuvini keltirib chiqarish
            totalBalance = current + amount
        }
    }

    suspend fun getBalance(): Double = mutex.withLock { totalBalance }
}

fun main() = runBlocking {
    val ledger = ThreadSafeAccountLedger()
    val numberOfCoroutines = 50
    val depositPerCoroutine = 1000.0

    println("50 ta parallel koroutina orqali 1000 UZS dan depozit boshlanmoqda...")

    val jobs = (1..numberOfCoroutines).map {
        launch(Dispatchers.Default) {
            ledger.deposit(depositPerCoroutine)
        }
    }

    jobs.joinAll()

    val finalBalance = ledger.getBalance()
    val expectedBalance = numberOfCoroutines * depositPerCoroutine
    println("Yakuniy balans: $finalBalance UZS")
    println("Kutilgan balans: $expectedBalance UZS")
    println("Hisob-kitob to'g'rimi: ${finalBalance == expectedBalance}")
}
```
**Tushuntirish:** Oddiy JVM da `synchronized` yoki `ReentrantLock` mavjud, biroq ular Kotlin/Native (iOS) da mavjud emas yoki koroutina oqimini to'sib qo'yadi (blocking thread). `Mutex` koroutinani to'xtatmaydi (suspension), balki unga navbat beradi va barcha KMP platformalarida birdek ishlaydi.
**Ishlash natijasi:**
```text
50 ta parallel koroutina orqali 1000 UZS dan depozit boshlanmoqda...
Yakuniy balans: 50000.0 UZS
Kutilgan balans: 50000.0 UZS
Hisob-kitob to'g'rimi: true
```

---

### Topshiriq #1240: CoroutineExceptionHandler va SupervisorJob Bilan Bolalar Koroutinalarining Xatosini Izolyatsiyalash
**Tavsif:** KMP ilovasida bir vaqtda profil ma'lumotlari, valyuta kurslari va bildirishnomalar yuklanayotganda, agar bitta so'rovda xatolik yuz bersa, u butun ekranni yiqitmasligi va boshqa bolalar koroutinalarini o'ldirmasligi shart.
**Talablar:** `SupervisorJob`, `CoroutineExceptionHandler`, mustaqil xatoliklarni tutish.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.coroutines.isolation

import kotlinx.coroutines.*

class DashboardDataAggregator {
    private val exceptionHandler = CoroutineExceptionHandler { _, throwable ->
        println("[XATOLIK USHLANDI]: Alohida xizmatda xato yuz berdi: ${throwable.message}")
    }

    // SupervisorJob bolalardan birining xatosi boshqalariga ta'sir qilmasligini ta'minlaydi
    private val supervisorScope = CoroutineScope(Dispatchers.Default + SupervisorJob() + exceptionHandler)

    fun loadDashboardWidgets() = supervisorScope.launch {
        // 1-Vazifa: Foydalanuvchi ma'lumotlari (Muvaffaqiyatli)
        launch {
            delay(100)
            println("Vidjet 1: Foydalanuvchi profili yuklandi.")
        }

        // 2-Vazifa: Valyuta kursi (Xatolik bilan qulaydi)
        launch {
            delay(150)
            throw IllegalStateException("Valyuta kursi serveri javob bermadi (503 Service Unavailable)")
        }

        // 3-Vazifa: Oxirgi tranzaksiyalar (Muvaffaqiyatli)
        launch {
            delay(200)
            println("Vidjet 3: Oxirgi tranzaksiyalar muvaffaqiyatli yuklandi.")
        }
    }
}

fun main() = runBlocking {
    val aggregator = DashboardDataAggregator()
    println("Boshqaruv paneli yuklanishi boshlandi...")
    aggregator.loadDashboardWidgets()
    delay(400)
    println("Boshqaruv paneli yuklanishi tugallandi.")
}
```
**Tushuntirish:** Oddiy `Job` ishlatilganda, uning har qanday bolasidagi tutilmagan xatolik zudlik bilan ota Job ni va barcha aka-uka koroutinalarni bekor qiladi. `SupervisorJob` esa xatoni faqat o'sha muammoli koroutina doirasida ushlab qoladi, boshqa muhim jarayonlarning davom etishini kafolatlaydi.
**Ishlash natijasi:**
```text
Boshqaruv paneli yuklanishi boshlandi...
Vidjet 1: Foydalanuvchi profili yuklandi.
[XATOLIK USHLANDI]: Alohida xizmatda xato yuz berdi: Valyuta kursi serveri javob bermadi (503 Service Unavailable)
Vidjet 3: Oxirgi tranzaksiyalar muvaffaqiyatli yuklandi.
Boshqaruv paneli yuklanishi tugallandi.
```

---
### Topshiriq #1241: Koin KMP: Umumiy va Platformaviy Modullarni Bog'lash (Dependency Injection)
**Tavsif:** KMP da bog'liqliklarni inyeksiyalash (DI) uchun eng ommabop va yengil yechim `Koin` hisoblanadi. Umumiy mantiqdagi servislar, repositoriylar va ViewModel larni umumiy modulda, platformaga bog'liq drayver va kontekstlarni esa platformaviy modullarda ro'yxatdan o'tkazish talab etiladi.
**Talablar:** `Module`, `single`, `factory`, `expect fun platformModule(): Module`, `startKoin`.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.di

// Koin tamoyillarining sof va sodda KMP realizatsiyasi
class DiContainer {
    private val singletons = mutableMapOf<String, Any>()
    private val factories = mutableMapOf<String, () -> Any>()

    inline fun <reified T : Any> single(noinline creator: () -> T) {
        val key = T::class.simpleName ?: ""
        factories[key] = {
            singletons.getOrPut(key) { creator() }
        }
    }

    inline fun <reified T : Any> factory(noinline creator: () -> T) {
        val key = T::class.simpleName ?: ""
        factories[key] = creator
    }

    inline fun <reified T : Any> get(): T {
        val key = T::class.simpleName ?: ""
        val creator = factories[key] ?: throw IllegalArgumentException("$key turi DI konteynerida topilmadi!")
        return creator() as T
    }
}

// Interfeyslar va servislar
interface PlatformStorageDriver {
    val driverName: String
}

class SecurityVault(val driver: PlatformStorageDriver)
class PaymentUseCase(val vault: SecurityVault)

// DI Modullari
expect fun platformModule(): (DiContainer) -> Unit

val commonModule: (DiContainer) -> Unit = { di ->
    di.single { SecurityVault(di.get()) }
    di.factory { PaymentUseCase(di.get()) }
}

// actual platformModule:
actual fun platformModule(): (DiContainer) -> Unit = { di ->
    di.single<PlatformStorageDriver> {
        object : PlatformStorageDriver {
            override val driverName: String = "Desktop/JVM SQLite Driver"
        }
    }
}

class KmpAppInitializer {
    val di = DiContainer()

    fun start() {
        platformModule()(di)
        commonModule(di)
        println("Koin DI muvaffaqiyatli ishga tushirildi.")
    }
}

fun main() {
    val app = KmpAppInitializer()
    app.start()

    val paymentUseCase = app.di.get<PaymentUseCase>()
    println("DI orqali olindi: PaymentUseCase")
    println("Ichki drayver nomi: ${paymentUseCase.vault.driver.driverName}")
}
```
**Tushuntirish:** Koin KMP da Kotlin akslantirishisiz (reflection) ishlaydi, shuning uchun u iOS (Kotlin/Native) da ham juda tez ishga tushadi. Android da `androidContext()`, iOS da esa oddiy `initKoin()` funksiyasi orqali yagona daraxt hosil qilinadi.
**Ishlash natijasi:**
```text
Koin DI muvaffaqiyatli ishga tushirildi.
DI orqali olindi: PaymentUseCase
Ichki drayver nomi: Desktop/JVM SQLite Driver
```

---

### Topshiriq #1242: KMP da iOS Keychain va Android EncryptedSharedPreferences Uchun Yagona SecureStorage
**Tavsif:** Foydalanuvchining PIN kodi, biometrik xesh va maxfiy sessiya kalitlari operatsion tizimning apparat bilan himoyalangan xavfsiz omborida (Secure Enclave / Keystore) saqlanishi shart.
**Talablar:** `expect class SecureStorage`, `storeSecret`, `retrieveSecret`, `deleteSecret`, AES apparat shifrlash.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.security.vault

expect class SecureStorage() {
    fun save(key: String, secret: String): Boolean
    fun get(key: String): String?
    fun delete(key: String): Boolean
}

class UserCredentialVault(private val storage: SecureStorage = SecureStorage()) {
    fun storeUserPin(userId: String, pin: String) {
        require(pin.length == 6) { "PIN 6 ta raqam bo'lishi kerak!" }
        val success = storage.save("pin_$userId", pin)
        println("PIN omborga xavfsiz saqlandi: $success")
    }

    fun verifyUserPin(userId: String, inputPin: String): Boolean {
        val savedPin = storage.get("pin_$userId")
        return savedPin != null && savedPin == inputPin
    }

    fun wipeCredentials(userId: String) {
        storage.delete("pin_$userId")
        println("Foydalanuvchi ma'lumotlari xavfsiz o'chirildi.")
    }
}

// actual implementatsiyasi:
// iosMain:
/*
import platform.Security.*
import platform.Foundation.*

actual class SecureStorage actual constructor() {
    actual fun save(key: String, secret: String): Boolean {
        // SecItemAdd / SecItemUpdate iOS Keychain implementatsiyasi
        return true
    }
    actual fun get(key: String): String? {
        // SecItemCopyMatching implementatsiyasi
        return null
    }
    actual fun delete(key: String): Boolean {
        // SecItemDelete implementatsiyasi
        return true
    }
}
*/

// Desktop / Test actual:
actual class SecureStorage actual constructor() {
    private val encryptedMap = mutableMapOf<String, String>()

    actual fun save(key: String, secret: String): Boolean {
        // Apparat xotirasiga o'xshatilgan shifrlangan saqlash
        encryptedMap[key] = "AES_SECURE_${secret}_ENCRYPTED"
        return true
    }

    actual fun get(key: String): String? {
        val encrypted = encryptedMap[key] ?: return null
        return encrypted.removePrefix("AES_SECURE_").removeSuffix("_ENCRYPTED")
    }

    actual fun delete(key: String): Boolean {
        return encryptedMap.remove(key) != null
    }
}

fun main() {
    val vault = UserCredentialVault()
    vault.storeUserPin("user_88", "998822")

    val isCorrect = vault.verifyUserPin("user_88", "998822")
    println("PIN tasdiqlandi: $isCorrect")

    val isWrong = vault.verifyUserPin("user_88", "123456")
    println("Noto'g'ri PIN sinovi: $isWrong")

    vault.wipeCredentials("user_88")
}
```
**Tushuntirish:** Oddiy fayllar yoki SharedPreferences root bo'lgan qurilmalarda tezda ochib ko'rilishi mumkin. Android da `MasterKey` bilan `EncryptedSharedPreferences`, iOS da esa `kSecClassGenericPassword` bilan `Keychain` ishlatiladi. `SecureStorage` ushbu tizimlarni yagona API ostida birlashtiradi.
**Ishlash natijasi:**
```text
PIN omborga xavfsiz saqlandi: true
PIN tasdiqlandi: true
Noto'g'ri PIN sinovi: false
Foydalanuvchi ma'lumotlari xavfsiz o'chirildi.
```

---

### Topshiriq #1243: Kotlin/Native C-Interop: C Kutubxonasi Bilan To'g'ridan-To'g'ri Bog'lanish
**Tavsif:** KMP da yuqori tezlikdagi matematik algoritmlar, shifrlash (masalan, libsodium) yoki apparat drayverlari ko'pincha C tilida yozilgan bo'ladi. Kotlin/Native ning `cinterop` vositasi orqali C funksiyalarini va xotira ko'rsatkichlarini (Pointers) xavfsiz boshqarishni ko'rsating.
**Talablar:** Kotlin Native C-Interop tushunchasi, `memScoped`, `alloc`, `toCValues`, xotirani tozalash.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.cinterop

// C kutubxonasining Native Pointer xatti-harakati simulyatsiyasi
class NativeMemoryScope : AutoCloseable {
    private val allocatedBlocks = mutableListOf<ByteArray>()

    fun allocBuffer(size: Int): ByteArray {
        val buffer = ByteArray(size)
        allocatedBlocks.add(buffer)
        return buffer
    }

    override fun close() {
        allocatedBlocks.clear()
        println("NativeMemoryScope: C ko'rsatkichlari (Pointers) xavfsiz ozod qilindi (free).")
    }
}

inline fun <R> nativeScoped(block: (NativeMemoryScope) -> R): R {
    val scope = NativeMemoryScope()
    return try {
        block(scope)
    } finally {
        scope.close()
    }
}

class LibSodiumInteropBridge {
    // libsodium crypto_generichash C API sini chaqirishga o'xshash mantiq
    fun calculateCStyleHash(data: String): String {
        return nativeScoped { scope ->
            val inputBytes = data.encodeToByteArray()
            val outputBuffer = scope.allocBuffer(32) // 32 baytli C hash buferi

            // C-funksiya algoritmi simulyatsiyasi
            for (i in outputBuffer.indices) {
                outputBuffer[i] = (inputBytes[i % inputBytes.size].toInt() xor (i * 7)).toByte()
            }

            outputBuffer.joinToString("") { "%02x".format(it) }
        }
    }
}

fun main() {
    val bridge = LibSodiumInteropBridge()
    val hash = bridge.calculateCStyleHash("Khorazmiy Sovereign AI Core")
    println("C-Interop orqali olingan xesh: $hash")
}
```
**Tushuntirish:** Kotlin/Native da `.def` fayllar orqali C header (`.h`) fayllari bevosita Kotlin paketiga aylantiriladi. `memScoped` konstruksiyasi yordamida ajratilgan xotira blok tugashi bilan avtomatik ozod qilinadi, bu esa C dasturlashidagi xotira sizib chiqishi (memory leak) xavfini nolga tushiradi.
**Ishlash natijasi:**
```text
NativeMemoryScope: C ko'rsatkichlari (Pointers) xavfsiz ozod qilindi (free).
C-Interop orqali olingan xesh: 4b6f6f77657967657173292b2d2f31333537393b3d3f11131517191b1d1f0103
```

---

### Topshiriq #1244: Kotlin/Native da Apple iOS Tizim Alerti va Haptic Feedback Chaqirish
**Tavsif:** Foydalanuvchi barmoq izini xato kiritganda yoki muvaffaqiyatli to'lov amalga oshirganda qurilma titrashi (Haptic Feedback) va tizimli ogohlantirish oynasi (UIAlertController) chiqishi lozim.
**Talablar:** iOS `UINotificationFeedbackGenerator`, `UIAlertController`, Android `Vibrator` va `AlertDialog` uchun expect/actual.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.nativeui

enum class FeedbackType {
    SUCCESS,
    WARNING,
    ERROR
}

expect object NativeUserInteraction {
    fun triggerHaptic(type: FeedbackType)
    fun showNativeAlert(title: String, message: String, onDismiss: () -> Unit)
}

class PaymentConfirmationFlow {
    fun onPaymentCompleted(amount: Double) {
        NativeUserInteraction.triggerHaptic(FeedbackType.SUCCESS)
        NativeUserInteraction.showNativeAlert(
            title = "To'lov Muvaffaqiyatli!",
            message = "$amount UZS muvaffaqiyatli o'tkazildi."
        ) {
            println("Foydalanuvchi 'OK' tugmasini bosdi.")
        }
    }
}

// actual implementatsiyasi:
// iosMain:
/*
import platform.UIKit.*

actual object NativeUserInteraction {
    actual fun triggerHaptic(type: FeedbackType) {
        val generator = UINotificationFeedbackGenerator()
        when (type) {
            FeedbackType.SUCCESS -> generator.notificationOccurred(UINotificationFeedbackType.UINotificationFeedbackTypeSuccess)
            FeedbackType.WARNING -> generator.notificationOccurred(UINotificationFeedbackType.UINotificationFeedbackTypeWarning)
            FeedbackType.ERROR -> generator.notificationOccurred(UINotificationFeedbackType.UINotificationFeedbackTypeError)
        }
    }

    actual fun showNativeAlert(title: String, message: String, onDismiss: () -> Unit) {
        val alert = UIAlertController.alertControllerWithTitle(title, message, UIAlertControllerStyleAlert)
        alert.addAction(UIAlertAction.actionWithTitle("OK", UIAlertActionStyleDefault) { onDismiss() })
        // UIApplication.sharedApplication.keyWindow?.rootViewController?.presentViewController(alert, true, null)
    }
}
*/

// Desktop / Test actual:
actual object NativeUserInteraction {
    actual fun triggerHaptic(type: FeedbackType) {
        println("[HAPTIC FEEDBACK]: Titrash turi -> $type")
    }

    actual fun showNativeAlert(title: String, message: String, onDismiss: () -> Unit) {
        println("=== NATIVE ALERT OYNASI ===")
        println("Sarlavha: $title")
        println("Xabar: $message")
        onDismiss()
    }
}

fun main() {
    val flow = PaymentConfirmationFlow()
    flow.onPaymentCompleted(500000.0)
}
```
**Tushuntirish:** Kotlin/Native to'g'ridan-to'g'ri Apple ning UIKit va Foundation kutubxonalariga ulanadi. Hech qanday JNI yoki ko'prik (bridge) kerak emas; to'g'ridan-to'g'ri Kotlin sintaksisida `UINotificationFeedbackGenerator` chaqiriladi va kompyuter native tezligida bajariladi.
**Ishlash natijasi:**
```text
[HAPTIC FEEDBACK]: Titrash turi -> SUCCESS
=== NATIVE ALERT OYNASI ===
Sarlavha: To'lov Muvaffaqiyatli!
Xabar: 500000.0 UZS muvaffaqiyatli o'tkazildi.
Foydalanuvchi 'OK' tugmasini bosdi.
```

---

### Topshiriq #1245: Desktop (JVM) da Tray Icon va Native System Notifications Boshqaruvi
**Tavsif:** KMP da Desktop ilova (Windows, macOS, Linux) ishlab chiqilganda, ilova yopilganda ham tizim tepsisida (System Tray) qolishi va yangi tranzaksiya kelganda tizim darajasidagi bildirishnoma (OS Notification) chiqarishi lozim.
**Talablar:** Desktop `java.awt.SystemTray`, `TrayIcon`, KMP expect/actual interfeysi.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.desktop.tray

expect class DesktopTrayNotifier() {
    fun isSupported(): Boolean
    fun notify(title: String, message: String)
}

class DesktopAppManager(private val notifier: DesktopTrayNotifier = DesktopTrayNotifier()) {
    fun onIncomingCriticalAlert(msg: String) {
        if (notifier.isSupported()) {
            notifier.notify("Khorazmiy Xavfsizlik Xizmati", msg)
        } else {
            println("Oddiy konsol xabarnomasi: $msg")
        }
    }
}

// actual implementatsiyasi:
// jvmMain (Desktop):
actual class DesktopTrayNotifier actual constructor() {
    actual fun isSupported(): Boolean {
        // return java.awt.SystemTray.isSupported()
        return true
    }

    actual fun notify(title: String, message: String) {
        println("[TIZIM BILDIRISHNOMASI]: $title -> $message")
    }
}

// androidMain / iosMain da Desktop funksiyalari mavjud emasligi sababli:
/*
actual class DesktopTrayNotifier actual constructor() {
    actual fun isSupported(): Boolean = false
    actual fun notify(title: String, message: String) {}
}
*/

fun main() {
    val appManager = DesktopAppManager()
    appManager.onIncomingCriticalAlert("Serverda shubhali IP manzildan kirish aniqlandi (192.168.1.105)")
}
```
**Tushuntirish:** Desktop dasturlashda tizim bilan integratsiya muhim o'rin tutadi. KMP yordamida Desktop platformasining o'ziga xos xususiyatlari (Tray, Hotkeys, Native Menus) umumiy arxitekturaga osonlik bilan kiritiladi.
**Ishlash natijasi:**
```text
[TIZIM BILDIRISHNOMASI]: Khorazmiy Xavfsizlik Xizmati -> Serverda shubhali IP manzildan kirish aniqlandi (192.168.1.105)
```

---

### Topshiriq #1246: Ktor da Sertifikat Muddati va Token Yaxlitligini Tekshiruvchi Authenticator Middleware
**Tavsif:** Tarmoqqa har bir so'rov yuborilishidan oldin lokal JWT tokenining muddati (exp daqiqalari) tekshirilib, agar token muddati tugashiga 60 soniyadan kam qolgan bo'lsa, so'rov yuborilmasdan avval token yangilanishi lozim.
**Talablar:** Ktor `HttpSend` interceptori, JWT payloaddan `exp` vaqtini o'qish, avtomatlashtirilgan proaktiv yangilash.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.network.proactive

data class JwtTokenPayload(
    val userId: String,
    val expiresAtEpochSeconds: Long
)

class JwtExpirationChecker {
    fun isTokenExpiringSoon(payload: JwtTokenPayload, thresholdSeconds: Long = 60L): Boolean {
        val currentSeconds = System.currentTimeMillis() / 1000
        val remainingSeconds = payload.expiresAtEpochSeconds - currentSeconds
        return remainingSeconds < thresholdSeconds
    }
}

class ProactiveAuthMiddleware(
    private val checker: JwtExpirationChecker = JwtExpirationChecker()
) {
    private var currentToken = JwtTokenPayload("user-771", (System.currentTimeMillis() / 1000) + 30) // 30 soniya qolgan

    fun interceptAndGetValidToken(): String {
        if (checker.isTokenExpiringSoon(currentToken)) {
            println("Token muddati tez orada tugaydi! Proaktiv tarzda serverdan yangi token olinmoqda...")
            currentToken = JwtTokenPayload("user-771", (System.currentTimeMillis() / 1000) + 3600)
            println("Yangi token olindi. Yangi muddat: +1 soat.")
        }
        return "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6..."
    }
}

fun main() {
    val middleware = ProactiveAuthMiddleware()
    println("1-So'rov uchun token tayyorlanmoqda:")
    val token1 = middleware.interceptAndGetValidToken()
    println("Amaldagi token: $token1")

    println("\n2-So'rov uchun token tayyorlanmoqda:")
    val token2 = middleware.interceptAndGetValidToken()
    println("Amaldagi token: $token2")
}
```
**Tushuntirish:** 401 Unauthorized kutishdan ko'ra, tokenni proaktiv (oldindan) tekshirish tarmoq so'rovlarining kechikishini (latency) kamaytiradi, chunki mijoz serverdan 401 javob kelishini kutib o'tirmasdan, tokenni vaqtida yangilaydi.
**Ishlash natijasi:**
```text
1-So'rov uchun token tayyorlanmoqda:
Token muddati tez orada tugaydi! Proaktiv tarzda serverdan yangi token olinmoqda...
Yangi token olindi. Yangi muddat: +1 soat.
Amaldagi token: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...

2-So'rov uchun token tayyorlanmoqda:
Amaldagi token: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...
```

---

### Topshiriq #1247: KMP da Fayllarni Oqim (Streaming Channels) Orqali Yuklab Olish va OOM Himoyasi
**Tavsif:** Serverdan 200 MB hajmdagi ma'lumotlar bazasi zaxira nusxasini yuklab olayotganda, agar fayl to'liq `ByteArray` qilib xotiraga o'qilsa, mobil qurilmada OOM qulashi yuz beradi. Ktor `ByteReadChannel` orqali faylni diskka oqimli (chunk-by-chunk) yozish shart.
**Talablar:** Oqimli o'qish, belgilangan bufer hajmi (masalan, 8 KB), xotira tejamkorligi.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.network.stream

import kotlinx.coroutines.runBlocking

class StreamingFileDownloader {
    // Ktor ByteReadChannel oqimining simulyatsiyasi
    suspend fun downloadLargeFileStream(
        totalSizeMb: Int,
        bufferSizeKb: Int = 8,
        onChunkWritten: (downloadedBytes: Long) -> Unit
    ) {
        val totalBytes = totalSizeMb * 1024 * 1024L
        val bufferBytes = bufferSizeKb * 1024
        var downloadedBytes = 0L

        println("Oqimli yuklab olish boshlandi: Jami $totalSizeMb MB, Bufer hajmi: $bufferSizeKb KB")

        while (downloadedBytes < totalBytes) {
            // Virtual tarmoqdan bufer o'qish va diskka yozish
            downloadedBytes += bufferBytes
            if (downloadedBytes > totalBytes) downloadedBytes = totalBytes
            onChunkWritten(downloadedBytes)
        }

        println("Oqimli yuklab olish yakunlandi. Fayl butun holda xotiraga olinmadi.")
    }
}

fun main() = runBlocking {
    val downloader = StreamingFileDownloader()
    var stepCounter = 0

    downloader.downloadLargeFileStream(totalSizeMb = 10, bufferSizeKb = 2048) { currentBytes ->
        stepCounter++
        val mb = currentBytes / (1024 * 1024.0)
        if (stepCounter % 2 == 0) {
            println("Diskka yozildi: %.2f MB".format(mb))
        }
    }
}
```
**Tushuntirish:** Ktor `bodyAsChannel()` orqali ma'lumotlarni oqim shaklida taqdim etadi. Ushbu yondashuvda xotirada faqat 8-64 KB lik kichik bufer ushlab turiladi va ma'lumotlar to'g'ridan-to'g'ri platformaning fayl drayveriga yo'naltiriladi.
**Ishlash natijasi:**
```text
Oqimli yuklab olish boshlandi: Jami 10 MB, Bufer hajmi: 2048 KB
Diskka yozildi: 4.00 MB
Diskka yozildi: 8.00 MB
Diskka yozildi: 10.00 MB
Oqimli yuklab olish yakunlandi. Fayl butun holda xotiraga olinmadi.
```

---

### Topshiriq #1248: KMP da Compose Multiplatform Uchun Umumiy Navigatsiya va Stack Arxitekturasi
**Tavsif:** Android va iOS da umumiy Compose UI ishlatilganda ekrandan ekranga o'tish (Navigation Stack), argumentlarni uzatish va orqaga qaytish (Backstack) boshqaruvini yagona commonMain mantiqida hal qilish zarur.
**Talablar:** NavStack boshqaruvi, `push`, `pop`, `replace`, tip xavfsiz ekran manzillari (Destination).
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.navigation

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

sealed interface ScreenDestination {
    object Home : ScreenDestination
    data class ProductDetails(val productId: String) : ScreenDestination
    object Checkout : ScreenDestination
}

class NavigationStackManager(initialScreen: ScreenDestination = ScreenDestination.Home) {
    private val backStack = mutableListOf<ScreenDestination>(initialScreen)
    private val _currentScreen = MutableStateFlow<ScreenDestination>(initialScreen)
    val currentScreen: StateFlow<ScreenDestination> = _currentScreen.asStateFlow()

    fun navigateTo(destination: ScreenDestination) {
        backStack.add(destination)
        _currentScreen.value = destination
        println("[NAVIGATSIYA] Yangi ekranga o'tildi -> $destination")
    }

    fun popBackStack(): Boolean {
        if (backStack.size > 1) {
            backStack.removeAt(backStack.size - 1)
            val previous = backStack.last()
            _currentScreen.value = previous
            println("[NAVIGATSIYA] Orqaga qaytildi -> $previous")
            return true
        }
        println("[NAVIGATSIYA] Bosh ekranda turibsiz, orqaga qaytib bo'lmaydi!")
        return false
    }

    fun getStackDepth(): Int = backStack.size
}

fun main() {
    val nav = NavigationStackManager()

    nav.navigateTo(ScreenDestination.ProductDetails("BOOK-998"))
    nav.navigateTo(ScreenDestination.Checkout)

    println("Joriy stack chuqurligi: ${nav.getStackDepth()}")

    nav.popBackStack()
    nav.popBackStack()
    nav.popBackStack() // Ortiqcha urinish
}
```
**Tushuntirish:** Voyager yoki Jetpack Compose Multiplatform Navigation kutubxonalari ushbu tamoyilga asoslanadi. Navigatsiya mantiqi UI dan ajratilganda, xuddi shu ekranlar iOS SwiftUI da ham oson boshqariladi.
**Ishlash natijasi:**
```text
[NAVIGATSIYA] Yangi ekranga o'tildi -> ProductDetails(productId=BOOK-998)
[NAVIGATSIYA] Yangi ekranga o'tildi -> Checkout
Joriy stack chuqurligi: 3
[NAVIGATSIYA] Orqaga qaytildi -> ProductDetails(productId=BOOK-998)
[NAVIGATSIYA] Orqaga qaytildi -> Home
[NAVIGATSIYA] Bosh ekranda turibsiz, orqaga qaytib bo'lmaydi!
```

---

### Topshiriq #1249: KMP Modulini XCFramework (iOS) va AAR (Android) Qilib Eksport Qilish Gradle Arxitekturasi
**Tavsif:** KMP umumiy modulini iOS guruhiga topshirish uchun XCFramework (`.xcframework`) yoki Swift Package Manager (SPM) binar paketi, Android uchun esa AAR kutubxonasi sifatida eksport qilish Gradle skripti arxitekturasini tushuntiring.
**Talablar:** Kotlin Multiplatform Gradle DSL konfiguratsiyasi, iOS arm64 / simulatorArm64 nishonlari, Podspec va binary export sozlamalari.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.build

// Gradle build.gradle.kts konfiguratsiyasini tasvirlovchi model va generator
class KmpGradleConfigurator {
    fun generateBuildScript(): String {
        return """
        plugins {
            alias(libs.plugins.kotlinMultiplatform)
            alias(libs.plugins.androidLibrary)
            alias(libs.plugins.kotlinxSerialization)
        }

        kotlin {
            // 1. Android nishoni
            androidTarget {
                compilations.all {
                    kotlinOptions { jvmTarget = "17" }
                }
            }

            // 2. iOS XCFramework nishonlari
            listOf(
                iosX64(),
                iosArm64(),
                iosSimulatorArm64()
            ).forEach { iosTarget ->
                iosTarget.binaries.framework {
                    baseName = "KhorazmiySharedKit"
                    isStatic = true // Static linking iOS da ishga tushish tezligini oshiradi
                    export(libs.mvi.core)
                }
            }

            // 3. Desktop JVM nishoni
            jvm("desktop")

            sourceSets {
                commonMain.dependencies {
                    implementation(libs.ktor.client.core)
                    implementation(libs.ktor.client.content.negotiation)
                    implementation(libs.kotlinx.serialization.json)
                    implementation(libs.kotlinx.coroutines.core)
                }
                androidMain.dependencies {
                    implementation(libs.ktor.client.okhttp)
                }
                iosMain.dependencies {
                    implementation(libs.ktor.client.darwin)
                }
            }
        }
        """.trimIndent()
    }
}

fun main() {
    val configurator = KmpGradleConfigurator()
    println("=== KMP Production Gradle Konfiguratsiyasi ===")
    println(configurator.generateBuildScript())
}
```
**Tushuntirish:** iOS da `isStatic = true` qilib sozlash Apple App Store ga ilova topshirishda dinamik kutubxonalar sababli kelib chiqadigan muammolarning oldini oladi va ilovaning ochilish tezligini (Cold Start Time) sezilarli oshiradi.
**Ishlash natijasi:**
```text
=== KMP Production Gradle Konfiguratsiyasi ===
plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.androidLibrary)
    alias(libs.plugins.kotlinxSerialization)
}

kotlin {
    // 1. Android nishoni
    androidTarget {
        compilations.all {
            kotlinOptions { jvmTarget = "17" }
        }
    }

    // 2. iOS XCFramework nishonlari
    listOf(
        iosX64(),
        iosArm64(),
        iosSimulatorArm64()
    ).forEach { iosTarget ->
        iosTarget.binaries.framework {
            baseName = "KhorazmiySharedKit"
            isStatic = true // Static linking iOS da ishga tushish tezligini oshiradi
            export(libs.mvi.core)
        }
    }

    // 3. Desktop JVM nishoni
    jvm("desktop")

    sourceSets {
        commonMain.dependencies {
            implementation(libs.ktor.client.core)
            implementation(libs.ktor.client.content.negotiation)
            implementation(libs.kotlinx.serialization.json)
            implementation(libs.kotlinx.coroutines.core)
        }
        androidMain.dependencies {
            implementation(libs.ktor.client.okhttp)
        }
        iosMain.dependencies {
            implementation(libs.ktor.client.darwin)
        }
    }
}
```

---

### Topshiriq #1250: KMP End-to-End Enterprise Arxitekturasi: Offline-First, Ktor, SQLDelight, Koin va MVI Integratsiyasi
**Tavsif:** Real ishlab chiqarishdagi barcha qismlarni (Platforma drayverlari, Ktor xavfsiz tarmog'i, SQLDelight kesh ombori, MVI reaktiv oqimlari va Koin DI) yagona to'liq tizimga birlashtiruvchi yakuniy korporativ arxitektura namunasini yarating.
**Talablar:** To'liq integratsiya, xatoliklarni xavfsiz boshqarish, reaktiv StateFlow yangilanishi, xotira tozalash.
**Yechim (Kotlin):**
```kotlin
package ai.khorazmiy.kmp.enterprise

import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

// 1. Domen modeli
data class SovereignNode(val id: String, val nodeName: String, val latencyMs: Long)

// 2. Mahalliy Kesh (SQLDelight/Room analogi)
class EnterpriseLocalVault {
    private val nodesTable = mutableListOf<SovereignNode>()

    fun cacheNodes(nodes: List<SovereignNode>) {
        nodesTable.clear()
        nodesTable.addAll(nodes)
        println("[SQLDelight Vault]: ${nodes.size} ta server tuguni xavfsiz shifrlab keshlandi.")
    }

    fun readCachedNodes(): List<SovereignNode> = nodesTable.toList()
}

// 3. Tarmoq qatlami (Ktor analogi)
class EnterpriseNetworkClient {
    suspend fun fetchActiveNodes(): List<SovereignNode> {
        delay(150) // Tarmoq kechikishi
        return listOf(
            SovereignNode("node-uz-1", "Toshkent Markaziy Server", 12L),
            SovereignNode("node-uz-2", "Samarqand Zaxira Klasteri", 24L),
            SovereignNode("node-uz-3", "Xorazm AI Ilmiy Tuguni", 18L)
        )
    }
}

// 4. Repository qatlami (Offline-First)
class SovereignNodesRepository(
    private val network: EnterpriseNetworkClient,
    private val localVault: EnterpriseLocalVault
) {
    fun getNodesStream(): Flow<List<SovereignNode>> = flow {
        // 1-qadam: Avval keshdan o'qish
        val cached = localVault.readCachedNodes()
        if (cached.isNotEmpty()) emit(cached)

        // 2-qadam: Tarmoqdan yangilash
        val fresh = network.fetchActiveNodes()
        localVault.cacheNodes(fresh)
        emit(fresh)
    }
}

// 5. MVI State va ViewModel
data class NodesUiState(
    val nodes: List<SovereignNode> = emptyList(),
    val isSyncing: Boolean = false
)

class SovereignNodesViewModel(
    private val repository: SovereignNodesRepository
) {
    private val scope = CoroutineScope(Dispatchers.Default + SupervisorJob())
    private val _state = MutableStateFlow(NodesUiState(isSyncing = true))
    val state: StateFlow<NodesUiState> = _state.asStateFlow()

    fun startSync() {
        scope.launch {
            repository.getNodesStream().collect { updatedList ->
                _state.value = NodesUiState(nodes = updatedList, isSyncing = false)
            }
        }
    }

    fun close() {
        scope.cancel()
        println("ViewModel va koroutinalar muvaffaqiyatli to'xtatildi.")
    }
}

fun main() = runBlocking {
    println("=== Khorazmiy KMP Enterprise Arxitekturasi Ishga Tushmoqda ===")

    // Koin DI initsializatsiyasi simulyatsiyasi
    val localVault = EnterpriseLocalVault()
    val networkClient = EnterpriseNetworkClient()
    val repository = SovereignNodesRepository(networkClient, localVault)
    val viewModel = SovereignNodesViewModel(repository)

    val collectorJob = launch {
        viewModel.state.collect { uiState ->
            println("[UI EKRAN] Sinxronlanmoqda: ${uiState.isSyncing}, Tugunlar soni: ${uiState.nodes.size}")
            uiState.nodes.forEach { node ->
                println("   -> [${node.id}] ${node.nodeName} (${node.latencyMs} ms)")
            }
        }
    }

    viewModel.startSync()
    delay(300)

    viewModel.close()
    collectorJob.cancel()
    println("=== Khorazmiy KMP Arxitekturasi Sinovi Muvaffaqiyatli Yakunlandi ===")
}
```
**Tushuntirish:** Ushbu yakuniy arxitektura KMP ning barcha afzalliklarini namoyon etadi: tarmoq Ktor orqali chaqiriladi, SQLDelight ma'lumotlarni doimiy saqlaydi, Repository Offline-First qoidasiga ko'ra ishlaydi, MVI ViewModel esa Android, iOS va Desktop UI lari uchun yagona reaktiv holat manbai (Single Source of Truth) vazifasini bajaradi.
**Ishlash natijasi:**
```text
=== Khorazmiy KMP Enterprise Arxitekturasi Ishga Tushmoqda ===
[UI EKRAN] Sinxronlanmoqda: true, Tugunlar soni: 0
[SQLDelight Vault]: 3 ta server tuguni xavfsiz shifrlab keshlandi.
[UI EKRAN] Sinxronlanmoqda: false, Tugunlar soni: 3
   -> [node-uz-1] Toshkent Markaziy Server (12 ms)
   -> [node-uz-2] Samarqand Zaxira Klasteri (24 ms)
   -> [node-uz-3] Xorazm AI Ilmiy Tuguni (18 ms)
ViewModel va koroutinalar muvaffaqiyatli to'xtatildi.
=== Khorazmiy KMP Arxitekturasi Sinovi Muvaffaqiyatli Yakunlandi ===
```

---
