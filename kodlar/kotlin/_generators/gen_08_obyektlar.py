# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

data_08 = [
    (
        351,
        "Singleton andozasi: 'object' deklaratsiyasi",
        "Kotlinda bitta kalit so'z bilan xavfsiz va xotirada yagona nusxada yaratiladigan Singleton obyektini e'lon qiling.",
        """object DatabaseManager {
    var connectionCount = 0

    fun connect() {
        connectionCount++
        println("Baza bilan ulanish o'rnatildi. Faol ulanishlar: $connectionCount")
    }

    fun disconnect() {
        if (connectionCount > 0) connectionCount--
        println("Ulanish uzildi. Faol ulanishlar: $connectionCount")
    }
}

fun main() {
    DatabaseManager.connect()
    DatabaseManager.connect()
    DatabaseManager.disconnect()
}""",
        "Kotlinda 'object' kalit so'zi Singleton (yagona nusxa) yaratadi. Bu obyekt birinchi marta murojaat qilingandagina tembel yuklanadi (lazy) va JVM sinf yuklovchisi (ClassLoader) tufayli 100% ko'p oqimli xavfsiz (thread-safe) hisoblanadi. Java dagi murakkab 'double-checked locking' kodiga umuman hojat qolmaydi.",
        """Baza bilan ulanish o'rnatildi. Faol ulanishlar: 1
Baza bilan ulanish o'rnatildi. Faol ulanishlar: 2
Ulanish uzildi. Faol ulanishlar: 1"""
    ),
    (
        352,
        "Singleton va Java bilan moslik: @JvmStatic va @JvmField",
        "Kotlindagi 'object' a'zolarini Java dan statik metod va maydon kabi to'g'ridan-to'g'ri chaqirish imkonini bering.",
        """object AppConstants {
    @JvmField
    val APP_NAME = "SuperApp"

    @JvmStatic
    fun getFullVersion(): String = "2.4.0-PROD"
}

fun main() {
    println("Ilova nomi: ${AppConstants.APP_NAME}")
    println("Versiya: ${AppConstants.getFullVersion()}")
}""",
        "'@JvmStatic' annotatsiyasi Kotlin obyektidagi metodni bayt-kod darajasida haqiqiy statik metodga aylantiradi. '@JvmField' esa getter/setter yaratmasdan to'g'ridan-to'g'ri ochiq 'public static final' maydon hosil qiladi.",
        """Ilova nomi: SuperApp
Versiya: 2.4.0-PROD"""
    ),
    (
        353,
        "Companion Object asoslari",
        "Sinf ichida statik metodlar vazifasini o'tovchi hamroh obyekt (companion object) yarating.",
        """class MathUtils {
    companion object {
        fun square(n: Int): Int = n * n
        fun cube(n: Int): Int = n * n * n
    }
}

fun main() {
    // Sinf nomi orqali to'g'ridan-to'g'ri chaqiriladi:
    println("5 ning kvadrati: ${MathUtils.square(5)}")
    println("3 ning kubi: ${MathUtils.cube(3)}")
}""",
        "'companion object' sinf ichidagi yagona maxsus obyektdir. Uning a'zolari Java dagi statik metodlar kabi to'g'ridan-to'g'ri 'SinfNomi.metod()' shaklida chaqiriladi.",
        """5 ning kvadrati: 25
3 ning kubi: 27"""
    ),
    (
        354,
        "Nomlangan Companion Object",
        "Companion object ga maxsus nom bering va unga o'sha nom orqali ham murojaat qiling.",
        """class HttpClient {
    companion object Factory {
        fun createDefault(): HttpClient {
            println("Standart HttpClient yaratildi")
            return HttpClient()
        }
    }
}

fun main() {
    val client1 = HttpClient.createDefault()
    val client2 = HttpClient.Factory.createDefault()
}""",
        "Companion object ga ixtiyoriy nom berish mumkin (masalan 'Factory'). Agar nom berilmasa, uning sukut bo'yicha nomi 'Companion' bo'ladi.",
        """Standart HttpClient yaratildi
Standart HttpClient yaratildi"""
    ),
    (
        355,
        "Companion Object interfeyslarni amalga oshirishi",
        "Companion object ga interfeys ulab, uni polimorfik fabrika sifatida ishlating.",
        """interface JsonParser<T> {
    fun parse(json: String): T
}

data class Profile(val username: String) {
    companion object : JsonParser<Profile> {
        override fun parse(json: String): Profile {
            // Oddiy parse simulyatsiyasi
            val name = json.substringAfter(":").trim().removeSurrounding("\\"")
            return Profile(name)
        }
    }
}

fun <T> decode(json: String, parser: JsonParser<T>): T {
    return parser.parse(json)
}

fun main() {
    val userProfile = decode("username: \\"shavkat\\"", Profile)
    println("Profil: ${userProfile.username}")
}""",
        "Companion object haqiqiy obyekt bo'lgani sababli, u interfeyslarni erkin amalga oshira oladi. Natijada sinf nomining o'zini ('Profile') to'g'ridan-to'g'ri 'JsonParser<Profile>' parametri sifatida uzatish mumkin bo'ladi.",
        """Profil: shavkat"""
    ),
    (
        356,
        "Companion Object ga Kengaytma Funksiya (Extension) yozish",
        "Mavjud sinfning companion object siga tashqaridan yangi yordamchi metod qo'shing.",
        """class Car(val model: String) {
    companion object
}

// Tashqaridan kengaytma:
fun Car.Companion.createSedan(): Car {
    return Car("Sedan")
}

fun main() {
    val car = Car.createSedan()
    println("Avtomobil: ${car.model}")
}""",
        "Agar sinf ichida bo'sh 'companion object' e'lon qilib qo'yilsa, kelajakda boshqa modullardan unga statikdek tuyuluvchi kengaytma funksiyalar ('Car.Companion.method()') qo'shish mumkin.",
        """Avtomobil: Sedan"""
    ),
    (
        357,
        "Anonim Obyektlar: 'object' ifodasi (Object Expression)",
        "Interfeysning bir martalik realizatsiyasini 'object : Interface' sintaksisi orqali yarating.",
        """interface OnClickListener {
    fun onClick(viewId: Int)
}

fun main() {
    val buttonListener = object : OnClickListener {
        override fun onClick(viewId: Int) {
            println("Tugma bosildi! ID = $viewId")
        }
    }

    buttonListener.onClick(105)
}""",
        "'object expression' Java dagi anonim ichki sinflarning (anonymous inner class) o'rnini bosadi. U har safar bajarilganda yangi obyekt hosil qiladi.",
        """Tugma bosildi! ID = 105"""
    ),
    (
        358,
        "Anonim obyektda tashqi o'zgaruvchilarni ushlash (Closure)",
        "Java dan farqli o'laroq, Kotlin anonim obyektlari tashqi 'var' o'zgaruvchilarni bemalol o'zgartira olishini ko'rsating.",
        """fun main() {
    var clickCount = 0

    val counterObject = object {
        fun doClick() {
            clickCount++ // Tashqi var o'zgaruvchi to'g'ridan-to'g'ri oshiriladi!
            println("Jami bosishlar: $clickCount")
        }
    }

    counterObject.doClick()
    counterObject.doClick()
    println("Yakuniy soni: $clickCount")
}""",
        "Java da anonim sinflar faqat 'final' o'zgaruvchilarga kira oladi. Kotlinda esa 'closure' to'liq qo'llab-quvvatlanadi: tashqi 'var' o'zgaruvchilar 'Ref' o'ramiga olinib, anonim obyekt ichida erkin o'zgartiriladi.",
        """Jami bosishlar: 1
Jami bosishlar: 2
Yakuniy soni: 2"""
    ),
    (
        359,
        "Nomsiz obyektlar (Ad-hoc Objects) mahalliy ma'lumotlar to'plami",
        "Hech qanday interfeys yoki sinf ko'rsatmasdan shunchaki bir nechta xususiyatli mahalliy obyekt yarating.",
        """fun main() {
    val coordinates = object {
        val x = 15.5
        val y = 24.8
        fun calculateDistance() = Math.sqrt(x * x + y * y)
    }

    println("X: ${coordinates.x}, Y: ${coordinates.y}")
    println("Masofa: %.2f".format(coordinates.calculateDistance()))
}""",
        "Kotlinda 'object { ... }' sintaksisi bilan nomsiz bir martalik yordamchi obyektlar yaratish mumkin. Bu faqat mahalliy yoki xususiy (private) doirada ishlaydi.",
        """X: 15.5, Y: 24.8
Masofa: 29.25"""
    ),
    (
        360,
        "Sinf Delegatsiyasi asoslari: 'by' kalit so'zi",
        "Merosxo'rlikdan qochib, tayyor interfeys obyektiga ishonch bildirish (Delegation) mexanizmini yozing.",
        """interface Printer {
    fun printData(content: String)
}

class StandardPrinter : Printer {
    override fun printData(content: String) {
        println("[PRINT]: $content")
    }
}

// SecurePrinter Printer interfeysi vazifasini ichki delegatga topshiradi:
class SecurePrinter(val delegate: Printer) : Printer by delegate

fun main() {
    val base = StandardPrinter()
    val secure = SecurePrinter(base)
    
    secure.printData("Maxfiy shartnoma matni")
}""",
        "Sinf delegatsiyasi ('class B(val a: A) : A by a') Kotlinning eng go'zal xususiyatlaridan biridir. Barcha 'Printer' metodlari avtomatik ravishda delegatga yo'naltiriladi va dasturchi har bir metodni qo'lda o'rab o'tirishdan xalos bo'ladi.",
        """[PRINT]: Maxfiy shartnoma matni"""
    ),
    (
        361,
        "Delegatsiya qilingan metodlarni qisman qayta yozish",
        "Sinf delegatsiyasida faqat ma'lum bir metodni o'zgartirib, qolganlarini delegatda qoldiring.",
        """interface TaskRunner {
    fun runTask(name: String)
    fun stopTask(name: String)
}

class DefaultTaskRunner : TaskRunner {
    override fun runTask(name: String) = println("Vazifa bajarilmoqda: $name")
    override fun stopTask(name: String) = println("Vazifa to'xtatildi: $name")
}

class LoggingTaskRunner(runner: TaskRunner) : TaskRunner by runner {
    // Faqat runTask ni kengaytiramiz:
    override fun runTask(name: String) {
        println("[LOG]: Vazifa boshlanishi qayd etildi: $name")
        // stopTask() esa to'g'ridan-to'g'ri DefaultTaskRunner ga ketadi
    }
}

fun main() {
    val runner = LoggingTaskRunner(DefaultTaskRunner())
    runner.runTask("Zaxiralash")
    runner.stopTask("Zaxiralash")
}""",
        "Klass delegatsiyasida xohlagan metodni 'override' qilib shaxsiy mantiq qo'shish mumkin, qolgan barcha metodlar esa avtomatik tarzda berilgan delegat orqali ishlayveradi.",
        """[LOG]: Vazifa boshlanishi qayd etildi: Zaxiralash
Vazifa to'xtatildi: Zaxiralash"""
    ),
    (
        362,
        "Xususiyat Delegatsiyasi asoslari: 'by' sintaksisi",
        "Xususiyatga o'qish va yozish amallarini maxsus sinfga topshiruvchi xususiyat delegatini qo'llang.",
        """import kotlin.reflect.KProperty

class UpperCaseDelegate {
    private var value: String = ""

    operator fun getValue(thisRef: Any?, property: KProperty<*>): String {
        return value
    }

    operator fun setValue(thisRef: Any?, property: KProperty<*>, newValue: String) {
        value = newValue.uppercase()
    }
}

class UserTag {
    var tag: String by UpperCaseDelegate()
}

fun main() {
    val u = UserTag()
    u.tag = "android_developer"
    println("Tag qiymati: ${u.tag}")
}""",
        "Xususiyat delegatsiyasida 'var x: Type by Delegate()' deb yozilganda, uning getteri 'Delegate.getValue()' ga, setteri esa 'Delegate.setValue()' ga kompilyatsiya bo'ladi.",
        """Tag qiymati: ANDROID_DEVELOPER"""
    ),
    (
        363,
        "Tembel yuklash oqim xavfsizligi darajalari: LazyThreadSafetyMode",
        "'by lazy' ning uch xil xavfsizlik rejimini (SYNCHRONIZED, PUBLICATION, NONE) tahlil qiling.",
        """class LazyModesDemo {
    // 1. Standart SYNCHRONIZED: ko'p oqimli muhitda to'liq qulflash (Thread-safe)
    val syncVal: String by lazy(LazyThreadSafetyMode.SYNCHRONIZED) {
        "Xavfsiz qiymat"
    }

    // 2. NONE: Hech qanday qulflash yo'q, eng tezkor, lekin faqat bitta oqimda xavfsiz (masalan Android UI Main Thread)
    val fastVal: String by lazy(LazyThreadSafetyMode.NONE) {
        "Tezkor qiymat"
    }
}

fun main() {
    val demo = LazyModesDemo()
    println("Sync: ${demo.syncVal}")
    println("Fast: ${demo.fastVal}")
}""",
        "Sukut bo'yicha 'by lazy' barcha oqimlarni sinxronlashtiradi (SYNCHRONIZED). Agar xususiyat faqat bitta oqimda (masalan Android UI thread) ishlatilishi aniq bo'lsa, 'LazyThreadSafetyMode.NONE' tanlanib, sinxronizatsiya ortiqcha xarajati tejaladi.",
        """Sync: Xavfsiz qiymat
Fast: Tezkor qiymat"""
    ),
    (
        364,
        "Xususiyatlarni kuzatish: Delegates.observable amaliyoti",
        "Har safar narx o'zgarganda log yozuvchi va yangi narxni ko'rsatuvchi dastur yozing.",
        """import kotlin.properties.Delegates

class StockPrice {
    var price: Double by Delegates.observable(100.0) { prop, old, new ->
        val diff = new - old
        val change = if (diff >= 0) "+$$diff" else "-$${-diff}"
        println("[BIRJA]: ${prop.name} o'zgardi: $$old -> $$new ($change)")
    }
}

fun main() {
    val stock = StockPrice()
    stock.price = 105.5
    stock.price = 98.0
}""",
        "'Delegates.observable' o'zgarish sodir bo'lgandan so'ng chaqiriladi. Bu MVVM arxitekturasida ma'lumotlar o'zgarganda UI ni qayta chizishga xabar berishda juda qulaydir.",
        """[BIRJA]: price o'zgardi: $100.0 -> $105.5 (+$5.5)
[BIRJA]: price o'zgardi: $105.5 -> $98.0 (-$7.5)"""
    ),
    (
        365,
        "O'zgarishni tekshirib qabul qilish: Delegates.vetoable",
        "Foydalanuvchi yoshi faqat oshishi mumkin bo'lgan, kamaytirishga urinishda o'zgarishni bekor qiluvchi xususiyat yarating.",
        """import kotlin.properties.Delegates

class PersonAge {
    var age: Int by Delegates.vetoable(18) { _, old, new ->
        new >= old // Faqat yangi yosh eski yoshdan katta yoki teng bo'lsa qabul qilinadi
    }
}

fun main() {
    val p = PersonAge()
    println("Boshlang'ich yosh: ${p.age}")
    
    p.age = 22
    println("22 berilganda: ${p.age}")
    
    p.age = 15 // Rad etiladi, eski qiymat 22 saqlanadi
    println("15 berilganda (rad etildi): ${p.age}")
}""",
        "'Delegates.vetoable' o'zgarish amalga oshishidan oldin ishga tushadi. Agar berilgan lambda 'false' qaytarsa, yangi qiymat biriktirilmaydi va xususiyat eskicha qoladi.",
        """Boshlang'ich yosh: 18
22 berilganda: 22
15 berilganda (rad etildi): 22"""
    ),
    (
        366,
        "Delegatsiya orqali Keshlovchi xususiyat yaratish",
        "Qiymatni ma'lum vaqt oralig'ida keshda saqlovchi shaxsiy delegat klassini yozing.",
        """import kotlin.reflect.KProperty

class TimeCachedDelegate<T>(val durationMs: Long, val provider: () -> T) {
    private var cached: T? = null
    private var lastTime: Long = 0

    operator fun getValue(thisRef: Any?, property: KProperty<*>): T {
        val now = System.currentTimeMillis()
        if (cached == null || (now - lastTime) > durationMs) {
            cached = provider()
            lastTime = now
            println("[KESH]: '${property.name}' yangilandi.")
        }
        return cached!!
    }
}

class CurrencyMonitor {
    val usdRate: Double by TimeCachedDelegate(500L) { 12800.0 }
}

fun main() {
    val monitor = CurrencyMonitor()
    println("1-olish: ${monitor.usdRate}")
    println("2-olish: ${monitor.usdRate}")
}""",
        "Shaxsiy delegat sinflari orqali kesh, log, validatsiya va boshqa ko'plab takrorlanuvchi operatsiyalarni barcha sinflar uchun qayta ishlatiluvchi holga keltirish mumkin.",
        """[KESH]: 'usdRate' yangilandi.
1-olish: 12800.0
2-olish: 12800.0"""
    ),
    (
        367,
        "Shaxsiy Shifrlangan Xususiyat Delegati",
        "Xususiyatga yozilayotgan ma'lumotni shifrlab saqlovchi, o'qilayotganda esa deshirflab beruvchi delegat yozing.",
        """import kotlin.reflect.KProperty
import java.util.Base64

class EncryptedStringDelegate {
    private var cipherText: String = ""

    operator fun getValue(thisRef: Any?, property: KProperty<*>): String {
        return String(Base64.getDecoder().decode(cipherText))
    }

    operator fun setValue(thisRef: Any?, property: KProperty<*>, value: String) {
        cipherText = Base64.getEncoder().encodeToString(value.toByteArray())
    }
}

class UserSecret {
    var pinCode: String by EncryptedStringDelegate()
}

fun main() {
    val secret = UserSecret()
    secret.pinCode = "9876_PIN"
    
    println("Deshifrlangan holda o'qish: ${secret.pinCode}")
}""",
        "Xususiyat delegatlari ichki xotira yacheykasida ma'lumotni mutlaqo boshqa formatda (masalan, Base64 yoki shifrlangan baytlar) saqlab, tashqariga oddiy String kabi ko'rinishi mumkin.",
        """Deshifrlangan holda o'qish: 9876_PIN"""
    ),
    (
        368,
        "Kolleksiyalarda Class Delegation bilan Read-Only himoyasi",
        "MutableList ni o'rab olib, tashqariga faqat 'List' interfeysini delegatsiya qiluvchi xavfsiz to'plam sinfini tuzing.",
        """class SafeCollection<T>(private val inner: MutableList<T>) : List<T> by inner {
    fun addSecure(item: T) {
        println("Element qo'shildi: $item")
        inner.add(item)
    }
}

fun main() {
    val safeList = SafeCollection(mutableListOf("A", "B"))
    safeList.addSecure("C")
    
    println("To'plam o'lchami: ${safeList.size}")
    println("2-indeks: ${safeList[2]}")
}""",
        "'SafeCollection' to'liq 'List<T>' interfeysini o'zida mujassamlashtiradi, ammo tashqariga 'add/remove' metodlarini bermaydi, faqat o'zining xavfsiz 'addSecure' metodiga ruxsat beradi.",
        """Element qo'shildi: C
To'plam o'lchami: 3
2-indeks: C"""
    ),
    (
        369,
        "Xususiyat nomini avtomatik olish (KProperty.name)",
        "Delegat ichida o'zgaruvchining haqiqiy nomini 'property.name' orqali o'qib, uni ma'lumotlar bazasi ustuniga moslash.",
        """import kotlin.reflect.KProperty

class Column(val defaultValue: String) {
    operator fun getValue(thisRef: Any?, property: KProperty<*>): String {
        return "[USTUN_${property.name.uppercase()}]: $defaultValue"
    }
}

class TableModel {
    val username: String by Column("anonim")
    val email: String by Column("yoq@mail.uz")
}

fun main() {
    val table = TableModel()
    println(table.username)
    println(table.email)
}""",
        "'KProperty<*>' parametri delegatga qaysi xususiyat ustida ishlayotganligini (uning nomi, qaytish turi, annotatsiyalari) to'liq taqdim etadi.",
        """[USTUN_USERNAME]: anonim
[USTUN_EMAIL]: yoq@mail.uz"""
    ),
    (
        370,
        "Singleton bilan Markaziy Sozlamalar Boshqaruvi (AppConfig)",
        "Barcha tizim sozlamalarini o'zida saqlovchi va xavfsiz o'zgartiruvchi Singleton sinf.",
        """object AppConfig {
    var environment: String = "staging"
    var isDebugEnabled: Boolean = true
    var maxUploadSizeMb: Int = 25

    fun printSummary() {
        println("=== SOZLAMALAR: Env=$environment | Debug=$isDebugEnabled | MaxUpload=${maxUploadSizeMb}MB ===")
    }
}

fun main() {
    AppConfig.printSummary()
    AppConfig.environment = "production"
    AppConfig.isDebugEnabled = false
    AppConfig.printSummary()
}""",
        "Global holatni boshqarishda 'object' yagona markaz vazifasini bajaradi va butun ilova bo'ylab bir xil manzilga ega bo'ladi.",
        """=== SOZLAMALAR: Env=staging | Debug=true | MaxUpload=25MB ===
=== SOZLAMALAR: Env=production | Debug=false | MaxUpload=25MB ==="""
    ),
    (
        371,
        "Companion Object da Private konstruktor va Fabrika metodi",
        "Sinf konstruktorini butunlay yashirib, ob'ektlarni faqat companion object metodlari orqali yaratish.",
        """class UserAccount private constructor(val id: Long, val role: String) {
    companion object {
        fun createStandardUser(id: Long): UserAccount {
            return UserAccount(id, "STANDARD_USER")
        }

        fun createAdminUser(id: Long): UserAccount {
            return UserAccount(id, "SUPER_ADMIN")
        }
    }
}

fun main() {
    val standard = UserAccount.createStandardUser(101L)
    val admin = UserAccount.createAdminUser(1L)
    
    println("Standard foydalanuvchi roli: ${standard.role}")
    println("Admin foydalanuvchi roli: ${admin.role}")
}""",
        "Konstruktorni 'private' qilish va companion object ichida aniq nomli metodlar ochish (Factory Method Pattern) kodni chalkashliklardan tozalaydi.",
        """Standard foydalanuvchi roli: STANDARD_USER
Admin foydalanuvchi roli: SUPER_ADMIN"""
    ),
    (
        372,
        "Delegatsiya bilan Ko'p interfeysli adapter (Adapter Pattern)",
        "Mavjud sinfni yangi interfeysga moslashtirish uchun sinf delegatsiyasidan foydalaning.",
        """interface OldSystem {
    fun legacyRequest(): String
}

interface ModernSystem {
    fun modernRequest(): String
}

class LegacyService : OldSystem {
    override fun legacyRequest(): String = "Eski protokol ma'lumoti"
}

class SystemAdapter(val legacy: OldSystem) : ModernSystem {
    override fun modernRequest(): String {
        return "Moslashtirildi: [${legacy.legacyRequest()}]"
    }
}

fun main() {
    val adapter = SystemAdapter(LegacyService())
    println(adapter.modernRequest())
}""",
        "Adapter andozasi eskirgan sinf bilan zamonaviy interfeys o'rtasida muammosiz ko'prik yaratadi.",
        """Moslashtirildi: [Eski protokol ma'lumoti]"""
    ),
    (
        373,
        "Delegates.notNull() bilan kechiktirilgan initsializatsiya",
        "Primitiv turlar uchun kechiktirilgan initsializatsiya delegatsiyasidan foydalanish.",
        """import kotlin.properties.Delegates

class ServerPortConfig {
    var port: Int by Delegates.notNull()
}

fun main() {
    val config = ServerPortConfig()
    config.port = 8080
    println("Sozlangan port: ${config.port}")
}""",
        "'lateinit' primitiv tiplarda (Int, Double) ishlamagani uchun 'Delegates.notNull<Int>()' yagona xavfsiz alternativadir.",
        """Sozlangan port: 8080"""
    ),
    (
        374,
        "Anonim Obyekt bir vaqtning o'zida bir nechta interfeysni amalga oshirishi",
        "Bitta anonim obyekt ifodasi orqali ikki xil interfeysni birdaniga amalga oshiring.",
        """interface Clickable { fun click() }
interface Hoverable { fun hover() }

fun setupUiElement(element: Any) {
    if (element is Clickable) element.click()
    if (element is Hoverable) element.hover()
}

fun main() {
    // Birdaniga ikkita interfeysni amalga oshiruvchi anonim obyekt:
    val interactiveElement = object : Clickable, Hoverable {
        override fun click() = println("Element bosildi.")
        override fun hover() = println("Sichqoncha kursor olib kelindi.")
    }

    setupUiElement(interactiveElement)
}""",
        "Kotlinda 'object : InterfaceA, InterfaceB' orqali birdaniga bir nechta interfeyslarni anonim tarzda realizatsiya qilish mumkin.",
        """Element bosildi.
Sichqoncha kursor olib kelindi."""
    ),
    (
        375,
        "Obyekt ifodasi funksiyadan xususiy (private) qaytishi",
        "Xususiy funksiyadan anonim obyekt qaytganda uning barcha a'zolari to'g'ridan-to'g'ri ko'rinishi.",
        """class WindowManager {
    private fun createInternalHelper() = object {
        val windowId = "WIN-9900"
        fun minimize() = println("Oyna yashirildi: $windowId")
    }

    fun execute() {
        val helper = createInternalHelper()
        println("Helper ID: ${helper.windowId}")
        helper.minimize()
    }
}

fun main() {
    val wm = WindowManager()
    wm.execute()
}""",
        "Agar anonim obyekt 'private' funksiyadan qaytsa, sinf ichida uning barcha xususiyat va metodlari saqlanib qoladi (tur yo'qolmaydi).",
        """Helper ID: WIN-9900
Oyna yashirildi: WIN-9900"""
    ),
    (
        376,
        "Shaxsiy delegat: Chegaralangan sonlar delegati",
        "O'zgaruvchiga qiymat yozilayotganda uni minimal va maksimal oraliqqa 'coerceIn' orqali moslovchi delegat yozing.",
        """import kotlin.reflect.KProperty

class ClampedInt(val min: Int, val max: Int, initial: Int) {
    private var actualValue = initial.coerceIn(min, max)

    operator fun getValue(thisRef: Any?, property: KProperty<*>): Int = actualValue

    operator fun setValue(thisRef: Any?, property: KProperty<*>, value: Int) {
        actualValue = value.coerceIn(min, max)
    }
}

class GameCharacter {
    var health: Int by ClampedInt(0, 100, 100)
}

fun main() {
    val hero = GameCharacter()
    println("Boshlang'ich jon: ${hero.health}")
    
    hero.health = 150 // 100 da to'xtaydi
    println("150 berilganda: ${hero.health}")
    
    hero.health = -20 // 0 da to'xtaydi
    println("-20 berilganda: ${hero.health}")
}""",
        "Har safar setter yozmasdan, bitta 'ClampedInt' delegati orqali butun loyihadagi barcha sonli xususiyatlarni chegaralash mumkin.",
        """Boshlang'ich jon: 100
150 berilganda: 100
-20 berilganda: 0"""
    ),
    (
        377,
        "Klass delegatsiyasi bilan Kesh o'rami (Cache Decorator)",
        "Repository interfeysini delegatsiya qilib, so'rovlarni xotirada keshlovchi dekorator klassi yarating.",
        """interface DataStore {
    fun fetch(key: String): String
}

class NetworkDataStore : DataStore {
    override fun fetch(key: String): String {
        println("[TARMOQ]: '$key' serverdan olinmoqda...")
        return "DATA_FOR_$key"
    }
}

class CachedDataStore(val realStore: DataStore) : DataStore by realStore {
    private val memory = mutableMapOf<String, String>()

    override fun fetch(key: String): String {
        return memory.getOrPut(key) {
            realStore.fetch(key)
        }
    }
}

fun main() {
    val store = CachedDataStore(NetworkDataStore())
    println("1-so'rov: " + store.fetch("kurs"))
    println("2-so'rov: " + store.fetch("kurs")) // Keshdan
}""",
        "Sinf delegatsiyasi orqali mavjud servislarga kesh, log yoki xavfsizlik funksiyalarini shaffof ravishda ulash mumkin.",
        """[TARMOQ]: 'kurs' serverdan olinmoqda...
1-so'rov: DATA_FOR_kurs
2-so'rov: DATA_FOR_kurs"""
    ),
    (
        378,
        "Singleton bilan Service Locator andozasi",
        "Servislarni nomi yoki interfeysi bo'yicha markaziy registrda saqlovchi sodda Dependency Injection analogi.",
        """object ServiceLocator {
    private val services = mutableMapOf<String, Any>()

    fun <T : Any> register(name: String, service: T) {
        services[name] = service
    }

    @Suppress("UNCHECKED_CAST")
    fun <T : Any> get(name: String): T {
        return services[name] as T
    }
}

class AuthService { fun login() = println("Foydalanuvchi kirdi.") }

fun main() {
    ServiceLocator.register("auth", AuthService())
    
    val auth: AuthService = ServiceLocator.get("auth")
    auth.login()
}""",
        "Service Locator andozasi kichik tizimlarda Dagger yoki Koin kabi og'ir kutubxonalarsiz ham xizmatlarni markazdan boshqarish imkonini beradi.",
        """Foydalanuvchi kirdi."""
    ),
    (
        379,
        "Xususiyat delegatida shartli hisob-kitoblar",
        "O'qilgan har safar vaqtni hisoblab, sekundiga qarab natija beruvchi delegat.",
        """import kotlin.reflect.KProperty

class TimestampDelegate {
    operator fun getValue(thisRef: Any?, property: KProperty<*>): String {
        return "Joriy vaqt: ${System.currentTimeMillis()}"
    }
}

class MonitorCard {
    val lastPing: String by TimestampDelegate()
}

fun main() {
    val monitor = MonitorCard()
    println(monitor.lastPing)
}""",
        "Delegat faqat xotiradagi qiymatni emas, har safar dinamik o'zgaruvchi hisob-kitobni ham qaytara oladi.",
        """Joriy vaqt ko'rsatiladi."""
    ),
    (
        380,
        "Companion Object va Singleton xatti-harakatining uyg'unligi",
        "Sinfning yagona global nusxasini companion object orqali taqdim etish.",
        """class GlobalTheme private constructor(val name: String) {
    companion object {
        val DEFAULT = GlobalTheme("Standard_Light")
        val DARK = GlobalTheme("Night_Dark")
    }
}

fun main() {
    val t1 = GlobalTheme.DEFAULT
    val t2 = GlobalTheme.DEFAULT
    
    println("Mavzu: ${t1.name}")
    println("Bir xil obyektmi: ${t1 === t2}")
}""",
        "Companion object ichida oldindan tayyorlangan singleton nusxalarni (predefined instances) saqlash resurslarni tejaydi.",
        """Mavzu: Standard_Light
Bir xil obyektmi: true"""
    ),
    (
        381,
        "Shaxsiy delegatda o'zgarishlar audit logi",
        "Xususiyatga yangi qiymat berilganda eski va yangi qiymatni faylga yoki konsolga audit qilib borish.",
        """import kotlin.reflect.KProperty

class AuditedValue<T>(private var currentValue: T) {
    operator fun getValue(thisRef: Any?, property: KProperty<*>): T = currentValue

    operator fun setValue(thisRef: Any?, property: KProperty<*>, newValue: T) {
        println("[AUDIT]: '${property.name}' maydoni o'zgardi. Eski: $currentValue -> Yangi: $newValue")
        currentValue = newValue
    }
}

class BankRecord {
    var status: String by AuditedValue("YANGI")
}

fun main() {
    val record = BankRecord()
    record.status = "TASDIQLANDI"
    record.status = "YOPILDI"
}""",
        "Har bir xususiyat o'zgarishini kuzatish biznes va audit xavfsizligida markaziy o'rin tutadi.",
        """[AUDIT]: 'status' maydoni o'zgardi. Eski: YANGI -> Yangi: TASDIQLANDI
[AUDIT]: 'status' maydoni o'zgardi. Eski: TASDIQLANDI -> Yangi: YOPILDI"""
    ),
    (
        382,
        "Sinf delegatsiyasi orqali xavfsiz to'plam: Set bilan takrorlanishlarni cheklash",
        "Set interfeysiga delegatsiya qilib, qo'shimcha statistikani hisoblang.",
        """class TrackedSet<T>(private val inner: MutableSet<T> = mutableSetOf()) : Set<T> by inner {
    var addAttempts = 0
        private set

    fun addTracked(item: T): Boolean {
        addAttempts++
        return inner.add(item)
    }
}

fun main() {
    val set = TrackedSet<String>()
    set.addTracked("Olma")
    set.addTracked("Olma") // Dublikat
    set.addTracked("Anor")
    
    println("To'plamdagi elementlar: $set")
    println("Jami urinishlar soni: ${set.addAttempts}")
}""",
        "Mavjud Set interfeysiga to'liq mos kelgan holda ichki hisoblagichni kengaytirish.",
        """To'plamdagi elementlar: [Olma, Anor]
Jami urinishlar soni: 3"""
    ),
    (
        383,
        "Obyekt ifodasi bilan bir nechta hodisalarni ushlovchi Listener",
        "Grafik interfeysdagi sichqoncha hodisalarini bitta obyektda tuting.",
        """interface MouseListener {
    fun onEnter()
    fun onExit()
}

class ViewComponent {
    var listener: MouseListener? = null
}

fun main() {
    val comp = ViewComponent()
    comp.listener = object : MouseListener {
        override fun onEnter() = println("Sichqoncha kirdi.")
        override fun onExit() = println("Sichqoncha chiqdi.")
    }

    comp.listener?.onEnter()
    comp.listener?.onExit()
}""",
        "Ko'p metodli interfeyslarda 'object expression' barcha metodlarni bir joyda toza amalga oshirishga imkon beradi.",
        """Sichqoncha kirdi.
Sichqoncha chiqdi."""
    ),
    (
        384,
        "Delegatda xususiyat tipini cheklash",
        "Faqat ma'lum bir sinf a'zolari uchun ishlaydigan delegat yozish.",
        """import kotlin.reflect.KProperty

class OwnerSpecificDelegate {
    operator fun getValue(thisRef: WindowManager, property: KProperty<*>): String {
        return "WindowManager ga xos xususiyat"
    }
}

class WindowManager {
    val title: String by OwnerSpecificDelegate()
}

fun main() {
    val wm = WindowManager()
    println(wm.title)
}""",
        "'thisRef: WindowManager' deb yozish orqali delegat faqat ushbu aniq sinf ichidagina ishlatilishi mumkinligini ta'minlash mumkin.",
        """WindowManager ga xos xususiyat"""
    ),
    (
        385,
        "Singleton bilan Xotira hajmini boshqarish",
        "Ilova doirasida ishlatilayotgan xotirani hisoblovchi Singleton xizmat.",
        """object MemoryTracker {
    private var allocatedBytes: Long = 0

    fun allocate(bytes: Long) {
        allocatedBytes += bytes
        println("Xotira ajratildi: +$bytes B | Jami: $allocatedBytes B")
    }

    fun free(bytes: Long) {
        allocatedBytes = (allocatedBytes - bytes).coerceAtLeast(0)
        println("Xotira bo'shatildi: -$bytes B | Jami: $allocatedBytes B")
    }
}

fun main() {
    MemoryTracker.allocate(1024)
    MemoryTracker.allocate(2048)
    MemoryTracker.free(1024)
}""",
        "Global resurslarni xavfsiz boshqarishda yagona 'object' doimo ishonchli nazoratchi bo'ladi.",
        """Xotira ajratildi: +1024 B | Jami: 1024 B
Xotira ajratildi: +2048 B | Jami: 3072 B
Xotira bo'shatildi: -1024 B | Jami: 2048 B"""
    ),
    (
        386,
        "Shaxsiy delegat: Nullable zaxira delegati",
        "Agar qiymat null bo'lsa zaxiradagi hisoblagichdan oluvchi delegat.",
        """import kotlin.reflect.KProperty

class FallbackDelegate<T>(val fallback: T) {
    private var actual: T? = null

    operator fun getValue(thisRef: Any?, property: KProperty<*>): T {
        return actual ?: fallback
    }

    operator fun setValue(thisRef: Any?, property: KProperty<*>, value: T) {
        actual = value
    }
}

class SystemConfig {
    var port: Int by FallbackDelegate(8080)
}

fun main() {
    val config = SystemConfig()
    println("Standart port: ${config.port}")
    
    config.port = 9000
    println("Yangilangan port: ${config.port}")
}""",
        "Standart zaxira qiymatini xususiyat darajasida xavfsiz saqlash.",
        """Standart port: 8080
Yangilangan port: 9000"""
    ),
    (
        387,
        "Companion Object orqali Konfiguratsiyani o'qish",
        "Sinfning companion object ida fayl yoki muhitdan o'qib beruvchi fabrika yozing.",
        """class DatabaseConfig(val url: String, val poolSize: Int) {
    companion object {
        fun fromEnvironment(): DatabaseConfig {
            val host = System.getenv("DB_HOST") ?: "localhost"
            return DatabaseConfig("jdbc:postgresql://$host:5432/db", 10)
        }
    }
}

fun main() {
    val conf = DatabaseConfig.fromEnvironment()
    println("Baza manzili: ${conf.url} (Hovuz: ${conf.poolSize})")
}""",
        "Konfiguratsiyani muhitdan (Environment) o'qib sinf yaratishda companion object eng qulay yondashuvdir.",
        """Baza manzili: jdbc:postgresql://localhost:5432/db (Hovuz: 10)"""
    ),
    (
        388,
        "Klass delegatsiyasi bilan Xatoliklarni qayta urinish (Retry Decorator)",
        "Interfeys metodlarini xato yuz berganda avtomatik qayta takrorlovchi dekorator.",
        """interface ApiService {
    fun call(): String
}

class FlakyApiService : ApiService {
    private var count = 0
    override fun call(): String {
        count++
        if (count < 2) throw RuntimeException("Aloqa uzildi")
        return "Muvaffaqiyatli server ma'lumoti"
    }
}

class RetryApiService(val delegate: ApiService) : ApiService by delegate {
    override fun call(): String {
        return try {
            delegate.call()
        } catch (e: Exception) {
            println("[RETRY]: Qayta urinilmoqda...")
            delegate.call()
        }
    }
}

fun main() {
    val service = RetryApiService(FlakyApiService())
    println("Natija: " + service.call())
}""",
        "Dekorator orqali mavjud servis kodini buzmasdan qayta urinish (retry) funksiyasi qo'shildi.",
        """[RETRY]: Qayta urinilmoqda...
Natija: Muvaffaqiyatli server ma'lumoti"""
    ),
    (
        389,
        "Obyekt ifodasi bilan Thread yaratish va ishga tushirish",
        "Java Runnable interfeysini anonim obyekt orqali ishlatish.",
        """fun main() {
    val task = object : Runnable {
        override fun run() {
            println("Alohida oqimda vazifa bajarildi.")
        }
    }

    val thread = Thread(task)
    thread.start()
    thread.join()
}""",
        "Java kutubxonalari bilan ishlashda 'object : Runnable' klassik oqim yaratish usulidir.",
        """Alohida oqimda vazifa bajarildi."""
    ),
    (
        390,
        "Shaxsiy delegatda o'zgaruvchilarni sinxronlashtirish: SynchronizedDelegate",
        "Xususiyatga murojaat va yozishni qulflash orqali ko'p oqimli xavfsiz qilish.",
        """import kotlin.reflect.KProperty

class SynchronizedValue<T>(private var value: T) {
    private val lock = Any()

    operator fun getValue(thisRef: Any?, property: KProperty<*>): T {
        synchronized(lock) {
            return value
        }
    }

    operator fun setValue(thisRef: Any?, property: KProperty<*>, newValue: T) {
        synchronized(lock) {
            value = newValue
        }
    }
}

class SharedCounter {
    var count: Int by SynchronizedValue(0)
}

fun main() {
    val counter = SharedCounter()
    counter.count = 42
    println("Sinxronlangan hisoblagich: ${counter.count}")
}""",
        "Xususiyat darajasida 'synchronized(lock)' blokini delegatga o'rash xavfsiz parallel dasturlashni ta'minlaydi.",
        """Sinxronlangan hisoblagich: 42"""
    ),
    (
        391,
        "Delegatsiya bilan o'chirilgan elementlar axlat qutisi (Recycle Bin)",
        "Ro'yxatdan o'chirilgan elementlarni alohida qutiga saqlab boruvchi delegat sinf.",
        """class TrashBinList<T>(private val inner: MutableList<T> = mutableListOf()) : MutableList<T> by inner {
    val trash = mutableListOf<T>()

    override fun removeAt(index: Int): T {
        val removed = inner.removeAt(index)
        trash.add(removed)
        return removed
    }
}

fun main() {
    val list = TrashBinList<String>()
    list.add("Hujjat 1")
    list.add("Hujjat 2")
    
    list.removeAt(0)
    println("Faol ro'yxat: $list")
    println("Axlat qutisi: ${list.trash}")
}""",
        "Sinf delegatsiyasi orqali 'removeAt' funksiyasi boyitildi va o'chirilgan ma'lumotlar saqlab qolindi.",
        """Faol ro'yxat: [Hujjat 2]
Axlat qutisi: [Hujjat 1]"""
    ),
    (
        392,
        "Companion Object da xususiyatlarni destrukturlash",
        "Sinf darajasidagi konstantalarni guruhlab olish.",
        """class Dimensions {
    companion object {
        const val WIDTH = 1920
        const val HEIGHT = 1080
    }
}

fun main() {
    println("Ruxsat: ${Dimensions.WIDTH}x${Dimensions.HEIGHT}")
}""",
        "Statik o'lchovlar va konstantalar bitta markaziy 'companion object' ichida ixcham saqlanadi.",
        """Ruxsat: 1920x1080"""
    ),
    (
        393,
        "Singleton bilan Hodisalar Shinasini (EventBus) yaratish",
        "Ilova bo'ylab hodisalarni tarqatuvchi markaziy EventBus.",
        """object SimpleEventBus {
    private val subscribers = mutableListOf<(String) -> Unit>()

    fun subscribe(action: (String) -> Unit) {
        subscribers.add(action)
    }

    fun post(event: String) {
        subscribers.forEach { it(event) }
    }
}

fun main() {
    SimpleEventBus.subscribe { println("[TINGLOVCHI 1]: $it") }
    SimpleEventBus.subscribe { println("[TINGLOVCHI 2]: $it") }

    SimpleEventBus.post("USER_LOGGED_IN")
}""",
        "EventBus arxitekturasi turli modullar o'rtasida to'g'ridan-to'g'ri bog'liqliksiz aloqa o'rnatish imkonini beradi.",
        """[TINGLOVCHI 1]: USER_LOGGED_IN
[TINGLOVCHI 2]: USER_LOGGED_IN"""
    ),
    (
        394,
        "Delegatda faqat bir marta yozilishi mumkin bo'lgan xususiyat (WriteOnce)",
        "Qiymat faqat bir marta biriktirilishi mumkin bo'lgan, ikkinchi marta o'zgartirish taqiqlangan delegat yozing.",
        """import kotlin.reflect.KProperty

class WriteOnce<T> {
    private var value: T? = null

    operator fun getValue(thisRef: Any?, property: KProperty<*>): T {
        return value ?: throw IllegalStateException("'${property.name}' hali initsializatsiya qilinmagan!")
    }

    operator fun setValue(thisRef: Any?, property: KProperty<*>, newValue: T) {
        if (value != null) {
            throw IllegalStateException("'${property.name}' ga faqat bir marta qiymat berish mumkin!")
        }
        value = newValue
    }
}

class RegistrationToken {
    var token: String by WriteOnce()
}

fun main() {
    val reg = RegistrationToken()
    reg.token = "TOKEN_XYZ_123"
    println("Token: ${reg.token}")
    
    try {
        reg.token = "NEW_TOKEN"
    } catch (e: IllegalStateException) {
        println("Xatolik ushlandi: ${e.message}")
    }
}""",
        "Xavfsizlik va bir martalik kalitlar uchun 'WriteOnce' delegati ikkinchi yozish urinishini qat'iy to'xtatadi.",
        """Token: TOKEN_XYZ_123
Xatolik ushlandi: 'token' ga faqat bir marta qiymat berish mumkin!"""
    ),
    (
        395,
        "Klass delegatsiyasi bilan unumdorlik metrikalarini yig'ish",
        "Har bir operatsiya bajarilish vaqtini o'lchovchi profiler dekoratori.",
        """interface DataProcessor {
    fun process(data: String)
}

class RealProcessor : DataProcessor {
    override fun process(data: String) {
        Thread.sleep(10) // Ish simulyatsiyasi
        println("Ma'lumot qayta ishlandi: $data")
    }
}

class ProfilingProcessor(val delegate: DataProcessor) : DataProcessor by delegate {
    override fun process(data: String) {
        val start = System.currentTimeMillis()
        delegate.process(data)
        val duration = System.currentTimeMillis() - start
        println("[PROFILER]: Sarflangan vaqt: $duration ms")
    }
}

fun main() {
    val processor = ProfilingProcessor(RealProcessor())
    processor.process("Moliya hisoboti")
}""",
        "Sinf delegatsiyasi orqali biznes kodga tegmasdan profiling va monitoring qatlami qo'shildi.",
        """Ma'lumot qayta ishlandi: Moliya hisoboti
[PROFILER]: Sarflangan vaqt o'lchanadi."""
    ),
    (
        396,
        "Shaxsiy delegat: Satr uzunligini tekshirish",
        "Satr ma'lum uzunlikdan oshmasligini kafolatlovchi maxsus delegat.",
        """import kotlin.reflect.KProperty

class MaxLengthString(val maxLen: Int, initial: String = "") {
    private var value = initial.take(maxLen)

    operator fun getValue(thisRef: Any?, property: KProperty<*>): String = value

    operator fun setValue(thisRef: Any?, property: KProperty<*>, newValue: String) {
        value = newValue.take(maxLen)
    }
}

class SmsPayload {
    var message: String by MaxLengthString(10)
}

fun main() {
    val sms = SmsPayload()
    sms.message = "Assalomu alaykum dunyo"
    println("Kesilgan matn (max 10 belgi): '${sms.message}'")
}""",
        "Tashqi tizimlar chegarasiga moslash uchun xususiyat qiymati avtomatik ravishda kesiladi.",
        """Kesilgan matn (max 10 belgi): 'Assalomu a'"""
    ),
    (
        397,
        "Companion object da reified generik metod",
        "Sinf companion object i ichida reified generik bilan JSON yoki tur tahlilini qilish.",
        """class ModelRegistry {
    companion object {
        inline fun <reified T> getModelName(): String {
            return "Model: ${T::class.simpleName}"
        }
    }
}

fun main() {
    println(ModelRegistry.getModelName<String>())
    println(ModelRegistry.getModelName<Int>())
}""",
        "Companion object ichidagi 'inline fun <reified T>' metodlar orqali ish vaqtida tiplar haqida to'liq ma'lumot olish mumkin.",
        """Model: String
Model: Int"""
    ),
    (
        398,
        "Obyekt ifodasi bilan Taqqoslash komparatori tuzish",
        "Kolleksiyani saralash uchun maxsus anonim 'Comparator' obyektidan foydalanish.",
        """import java.util.Collections

fun main() {
    val words = mutableListOf("olma", "nok", "uzumlar", "anjir")

    // Anonim comparator:
    val lengthComparator = object : Comparator<String> {
        override fun compare(s1: String, s2: String): Int {
            return s1.length.compareTo(s2.length)
        }
    }

    words.sortWith(lengthComparator)
    println("Uzunligi bo'yicha saralangan: $words")
}""",
        "Anonim obyektlar Java interfeyslarini implementatsiya qilishda to'liq va o'qishli nazorat beradi.",
        """Uzunligi bo'yicha saralangan: [nok, olma, anjir, uzumlar]"""
    ),
    (
        399,
        "Klass delegatsiyasi bilan Immutability himoyasi",
        "MutableMap ni ichkarida saqlab, tashqariga faqat Map interfeysini delegatsiya qilish.",
        """class ReadOnlyDictionary(private val map: MutableMap<String, String>) : Map<String, String> by map {
    fun internalUpdate(key: String, value: String) {
        map[key] = value
    }
}

fun main() {
    val dict = ReadOnlyDictionary(mutableMapOf("salom" to "hello"))
    dict.internalUpdate("kitob", "book")
    
    println("Lug'at: $dict")
    println("salom tarjimasi: ${dict["salom"]}")
}""",
        "Tashqi kod 'dict' ni o'zgartira olmaydi, faqat 'ReadOnlyDictionary' ning ichki xavfsiz metodlari yangilay oladi.",
        """Lug'at: {salom=hello, kitob=book}
salom tarjimasi: hello"""
    ),
    (
        400,
        "Obyektlar va delegatsiya bo'yicha to'liq amaliy xulosa: Xavfsiz Xotira va Monitoring Tizimi",
        "Singleton object, Companion object, Object expression, Class delegation va Property delegation imkoniyatlarini bitta yaxlit tizimda birlashtiring.",
        """import kotlin.properties.Delegates

interface AuditService {
    fun logAudit(action: String)
}

object CentralAuditManager : AuditService {
    override fun logAudit(action: String) {
        println("[MARKAZIY AUDIT]: $action (2026-11-08)")
    }
}

interface Vault {
    fun readSecret(): String
}

class SecureVault(val key: String, audit: AuditService) : Vault, AuditService by audit {
    var accessCounter: Int by Delegates.observable(0) { _, old, new ->
        logAudit("Vault ga kirish soni: $old -> $new")
    }

    override fun readSecret(): String {
        accessCounter++
        return "MAXFIY_PAROL_XYZ"
    }

    companion object Factory {
        fun createDefault(): SecureVault {
            return SecureVault("DEF_KEY", CentralAuditManager)
        }
    }
}

fun main() {
    val vault = SecureVault.createDefault()
    println("Maxfiy ma'lumot: " + vault.readSecret())
    println("Maxfiy ma'lumot: " + vault.readSecret())
}""",
        "Ushbu yakuniy topshiriqda Singleton ('object CentralAuditManager'), Companion Object ('Factory'), Class Delegation ('by audit') va Property Delegation ('by Delegates.observable') yaxlit tizimda professional birlashtirildi.",
        """[MARKAZIY AUDIT]: Vault ga kirish soni: 0 -> 1 (2026-11-08)
Maxfiy ma'lumot: MAXFIY_PAROL_XYZ
[MARKAZIY AUDIT]: Vault ga kirish soni: 1 -> 2 (2026-11-08)
Maxfiy ma'lumot: MAXFIY_PAROL_XYZ"""
    )
]

for item in data_08:
    n, title, condition, sol, exp, res = item
    tasks.append(format_task(n, title, condition, sol, exp, res))

save_file("kotlin_08_obyektlar_va_delegatsiya.md", tasks)
