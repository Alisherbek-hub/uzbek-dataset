# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

data_06 = [
    (
        251,
        "Merosxo'rlik asoslari: 'open' kalit so'zi",
        "Kotlinda sinflar sukut bo'yicha yopiq (final) ekanligini va ota sinfni 'open' qilish zaruratini ko'rsating.",
        """open class Vehicle(val brand: String, val maxSpeed: Int) {
    fun showSpecs() {
        println("Brend: $brand | Maksimal tezlik: $maxSpeed km/soat")
    }
}

class Car(brand: String, maxSpeed: Int, val doorsCount: Int) : Vehicle(brand, maxSpeed)

fun main() {
    val myCar = Car("Chevrolet", 200, 4)
    myCar.showSpecs()
    println("Eshiklar soni: ${myCar.doorsCount}")
}""",
        "Kotlinda barcha sinflar va metodlar sukut bo'yicha 'final' (meros olish taqiqlangan) hisoblanadi. Bu 'Effective Java' kitobidagi 'Merosxo'rlik uchun loyihalang yoki uni taqiqlang' tamoyiliga tayanadi. Boshqa sinf undan meros olishi uchun ota sinf oldiga 'open' kalit so'zi qo'yilishi shart.",
        """Brend: Chevrolet | Maksimal tezlik: 200 km/soat
Eshiklar soni: 4"""
    ),
    (
        252,
        "Metodlarni qayta yozish: 'open fun' va 'override'",
        "Ota sinfdagi metodni bola sinfda o'zgartirish (override) uchun 'open' va 'override' modifikatorlaridan foydalaning.",
        """open class Animal(val name: String) {
    open fun makeSound() {
        println("$name tovush chiqarmoqda...")
    }
}

class Dog(name: String) : Animal(name) {
    override fun makeSound() {
        println("$name: Vov-vov!")
    }
}

class Cat(name: String) : Animal(name) {
    override fun makeSound() {
        println("$name: Miyov!")
    }
}

fun main() {
    val dog = Dog("Olapar")
    val cat = Cat("Mosh")
    
    dog.makeSound()
    cat.makeSound()
}""",
        "Ota sinfdagi oddiy metodlar ham sukut bo'yicha final bo'ladi. Bola sinfda ularni yangilash uchun metod oldiga 'open' qo'yiladi, bola sinfda esa 'override' kalit so'zi yozilishi majburiydir. Bu tasodifiy metod mos kelishlaridan asraydi.",
        """Olapar: Vov-vov!
Mosh: Miyov!"""
    ),
    (
        253,
        "Ota sinf metodini chaqirish: 'super' kalit so'zi",
        "Bola sinf metodida ota sinf logikasini saqlab qolgan holda qo'shimcha xatti-harakat qo'shing.",
        """open class Worker(val name: String) {
    open fun performWork() {
        println("$name ishni boshladi.")
    }
}

class Developer(name: String, val language: String) : Worker(name) {
    override fun performWork() {
        super.performWork() // Ota sinf metodini chaqirish
        println("$name $language tilida kod yozmoqda.")
    }
}

fun main() {
    val dev = Developer("Bobur", "Kotlin")
    dev.performWork()
}""",
        "'super.methodName()' sintaksisi bola sinfdan ota sinfning asl realizatsiyasini chaqirish uchun ishlatiladi. Bu merosxo'rlikda umumiy kodni kengaytirish imkonini beradi.",
        """Bobur ishni boshladi.
Bobur Kotlin tilida kod yozmoqda."""
    ),
    (
        254,
        "Xususiyatlarni (Properties) override qilish",
        "Ota sinfdagi 'open val' xususiyatini bola sinfda boshqacha qiymat yoki hisoblash bilan qayta yozing.",
        """open class Shape {
    open val vertexCount: Int = 0
}

class Triangle : Shape() {
    override val vertexCount: Int = 3
}

class Pentagon : Shape() {
    override val vertexCount: Int = 5
}

fun main() {
    val t = Triangle()
    val p = Pentagon()
    
    println("Uchburchak uchlari: ${t.vertexCount}")
    println("Beshburchak uchlari: ${p.vertexCount}")
}""",
        "Kotlinda nafaqat funksiyalar, balki xususiyatlar ham 'open' bo'lishi va 'override' qilinishi mumkin. Muhim qoida: 'val' xususiyatni bola sinfda 'var' qilib kengaytirish mumkin, lekin 'var' ni 'val' qilib toraytirib bo'lmaydi.",
        """Uchburchak uchlari: 3
Beshburchak uchlari: 5"""
    ),
    (
        255,
        "Mavhum sinflar (Abstract Classes) va mavhum a'zolar",
        "To'g'ridan-to'g'ri nusxa olib bo'lmaydigan 'abstract class' e'lon qilib, uning mavhum metodini realizatsiya qiling.",
        """abstract class GraphicElement {
    abstract val name: String
    abstract fun draw()

    fun logElement() {
        println("[LOG]: Chizilmoqda: $name")
    }
}

class Circle(override val name: String, val radius: Double) : GraphicElement() {
    override fun draw() {
        logElement()
        println("O doira chizildi (radius: $radius)")
    }
}

fun main() {
    // val g = GraphicElement() // Kompilyatsiya xatosi: Cannot create an instance of an abstract class
    val circle = Circle("QizilDoira", 10.0)
    circle.draw()
}""",
        "'abstract class' umumiy andoza bo'lib, uning nusxasini yaratib bo'lmaydi. U o'z ichida ham to'liq yozilgan oddiy metodlarni, ham bola sinflar majburiy yozishi kerak bo'lgan 'abstract' metodlarni saqlaydi. Abstrakt a'zolarga 'open' yozish shart emas, ular avtomatik ochiqdir.",
        """[LOG]: Chizilmoqda: QizilDoira
O doira chizildi (radius: 10.0)"""
    ),
    (
        256,
        "Interfeyslar (Interfaces) asoslari",
        "Metod shartnomalarini belgilovchi 'interface' e'lon qiling va uni sinfda amalga oshiring.",
        """interface Printable {
    fun printDocument()
}

class Invoice(val id: String, val total: Double) : Printable {
    override fun printDocument() {
        println("Hisob-faktura chop etildi: #$id, Jami: $$total")
    }
}

fun main() {
    val doc: Printable = Invoice("INV-2026-01", 340.0)
    doc.printDocument()
}""",
        "Interfeyslar xulq-atvor shartnomalarini ifodalaydi. Klasslar faqat bitta ota sinfdan meros olishi mumkin, ammo istalgancha ko'p interfeyslarni (multiple interface inheritance) amalga oshira oladi.",
        """Hisob-faktura chop etildi: #INV-2026-01, Jami: $340.0"""
    ),
    (
        257,
        "Interfeysda standart realizatsiya (Default Implementation)",
        "Interfeys metodiga tanasi bilan standart xatti-harakat yozing va bola sinfda uni xohishga ko'ra o'zgartiring.",
        """interface Loggable {
    fun log(message: String) {
        println("[STANDART LOG]: $message")
    }
}

class DefaultService : Loggable

class CustomService : Loggable {
    override fun log(message: String) {
        println("[MAXSUS LOG]: >>> $message <<<")
    }
}

fun main() {
    val s1 = DefaultService()
    val s2 = CustomService()
    
    s1.log("Server ishga tushdi")
    s2.log("Muhim ogohlantirish")
}""",
        "Kotlinda interfeys metodlari standart tanaga ega bo'lishi mumkin. Agar sinf uni override qilmasa, interfeysdagi standart realizatsiya avtomatik ravishda ishlaydi.",
        """[STANDART LOG]: Server ishga tushdi
[MAXSUS LOG]: >>> Muhim ogohlantirish <<<"""
    ),
    (
        258,
        "Interfeysda xususiyatlar (Properties in Interfaces)",
        "Interfeysda mavhum va hisoblanuvchi xususiyatlar e'lon qiling (backing field bo'lmasligi qoidasi).",
        """interface Named {
    val firstName: String
    val lastName: String

    // Hisoblanuvchi xususiyat (Backing field yo'q):
    val fullName: String
        get() = "$firstName $lastName"
}

class Client(override val firstName: String, override val lastName: String) : Named

fun main() {
    val client = Client("Dilshod", "Alimov")
    println("Mijoz to'liq ismi: ${client.fullName}")
}""",
        "Interfeyslarda ham xususiyatlar e'lon qilish mumkin. Biroq interfeys holat saqlay olmaydi (backing field bo'lmaydi). Shuning uchun xususiyat yoki mavhum bo'ladi, yoki unga maxsus getter yoziladi.",
        """Mijoz to'liq ismi: Dilshod Alimov"""
    ),
    (
        259,
        "Bir nechta interfeysdan meros olish va to'qnashuvlarni yechish",
        "Ikki xil interfeysda bir xil nomli standart metod bo'lganda 'super<A>' va 'super<B>' orqali to'qnashuvni hal qiling.",
        """interface UIComponent {
    fun render() {
        println("UIComponent rendering...")
    }
}

interface WebWidget {
    fun render() {
        println("WebWidget HTML rendering...")
    }
}

class CustomButton : UIComponent, WebWidget {
    override fun render() {
        // Ikkala ota interfeysning render metodlarini alohida chaqirish:
        super<UIComponent>.render()
        super<WebWidget>.render()
        println("CustomButton rendering yakunlandi.")
    }
}

fun main() {
    val btn = CustomButton()
    btn.render()
}""",
        "Agar sinf bir nechta interfeysdan bir xil nomli metodlarni qabul qilsa, kompilyator xatolik beradi. Dasturchi ushbu metodni 'override' qilib, 'super<InterfaceName>.method()' sintaksisi orqali aynan qaysi ota interfeys logikasi chaqirilishini ko'rsatishi shart.",
        """UIComponent rendering...
WebWidget HTML rendering...
CustomButton rendering yakunlandi."""
    ),
    (
        260,
        "Qayta yozishni to'xtatish: 'final override'",
        "Ota sinfdan kelgan 'open' metodni bola sinfda override qilib, undan keyingi subklasslar uchun uni 'final' qilib yoping.",
        """open class BaseController {
    open fun initialize() {
        println("Asosiy initsializatsiya")
    }
}

open class SecuredController : BaseController() {
    // Endi SecuredController dan meros oluvchilar initialize() ni override qila olmaydi
    final override fun initialize() {
        println("Xavfsiz initsializatsiya (Qat'iy yopilgan)")
    }
}

class AppController : SecuredController() {
    // override fun initialize() -> Kompilyatsiya xatosi: 'initialize' in 'SecuredController' is final
}

fun main() {
    val controller = SecuredController()
    controller.initialize()
}""",
        "Kotlinda 'override' qilingan metod sukut bo'yicha yana 'open' bo'lib qoladi. Keyingi avlod sinflarida ushbu metod qayta o'zgartirilmasligini ta'minlash uchun 'final override' birikmasi qo'llaniladi.",
        """Xavfsiz initsializatsiya (Qat'iy yopilgan)"""
    ),
    (
        261,
        "Polimorfizm va dinamik bog'lanish (Polymorphism & Dynamic Dispatch)",
        "Ota interfeys havolasi orqali har xil bola obyektlarning metodlarini chaqirish.",
        """interface PaymentMethod {
    fun processPayment(amount: Double)
}

class CreditCardPayment : PaymentMethod {
    override fun processPayment(amount: Double) {
        println("Kredit karta orqali $$amount yechildi.")
    }
}

class CryptoPayment : PaymentMethod {
    override fun processPayment(amount: Double) {
        println("Kriptovalyuta tarmog'ida $$amount tasdiqlandi.")
    }
}

fun checkout(payment: PaymentMethod, total: Double) {
    payment.processPayment(total)
}

fun main() {
    val p1: PaymentMethod = CreditCardPayment()
    val p2: PaymentMethod = CryptoPayment()
    
    checkout(p1, 150.0)
    checkout(p2, 300.0)
}""",
        "Polimorfizm dasturni umumiy abstraksiyalar (PaymentMethod) orqali yozishga imkon beradi. Ish vaqtida (runtime) aynan qaysi haqiqiy obyekt turganiga qarab kerakli metod chaqiriladi (Dynamic Dispatch).",
        """Kredit karta orqali $150.0 yechildi.
Kriptovalyuta tarmog'ida $300.0 tasdiqlandi."""
    ),
    (
        262,
        "Konstruktorlar zanjiri va bajarilish tartibi",
        "Merosxo'rlik zanjirida ota sinf va bola sinf konstruktorlarining bajarilish ketma-ketligini ko'rsating.",
        """open class GrandParent(val familyName: String) {
    init {
        println("1. GrandParent init: $familyName")
    }
}

open class Parent(familyName: String, val city: String) : GrandParent(familyName) {
    init {
        println("2. Parent init: Shaxar=$city")
    }
}

class Child(familyName: String, city: String, val age: Int) : Parent(familyName, city) {
    init {
        println("3. Child init: Yoshi=$age")
    }
}

fun main() {
    val c = Child("Qodirovlar", "Buxoro", 12)
}""",
        "Obyekt yaratilayotganda eng birinchi bo'lib eng yuqoridagi ota sinf (GrandParent) konstruktori va init bloki, so'ng o'rta ota sinf (Parent) va eng oxirida bola sinf (Child) ning konstruktori bajariladi.",
        """1. GrandParent init: Qodirovlar
2. Parent init: Shaxar=Buxoro
3. Child init: Yoshi=12"""
    ),
    (
        263,
        "Interfeyslarni meros qilib olish (Interface Inheritance)",
        "Bitta interfeys boshqa interfeysdan meros olishini va uni kengaytirishini namoyish qiling.",
        """interface Reader {
    fun read(): String
}

interface Writer {
    fun write(content: String)
}

// Ikkala interfeysni birlashtiruvchi yangi interfeys:
interface ReadWriteDevice : Reader, Writer {
    fun sync()
}

class MemoryCard : ReadWriteDevice {
    private var data = "Standart fayl"

    override fun read(): String = data
    override fun write(content: String) { data = content }
    override fun sync() { println("Xotira sinxronlandi.") }
}

fun main() {
    val card = MemoryCard()
    card.write("Yangi ma'lumot")
    println("O'qildi: ${card.read()}")
    card.sync()
}""",
        "Kotlinda interfeyslar boshqa bir nechta interfeyslarni meros qilib olishi mumkin. Natijada quyi sinf ushbu barcha interfeyslardagi shartnomalarni to'liq bajarishi kerak bo'ladi.",
        """O'qildi: Yangi ma'lumot
Xotira sinxronlandi."""
    ),
    (
        264,
        "Funksional interfeyslar: SAM (Single Abstract Method) interfeys",
        "'fun interface' kalit so'zi orqali Kotlin SAM interfeysini e'lon qilib, unga lambda uzatish.",
        """fun interface EventFilter {
    fun accept(event: String): Boolean
}

fun filterEvents(events: List<String>, filter: EventFilter): List<String> {
    return events.filter { filter.accept(it) }
}

fun main() {
    val rawEvents = listOf("LOGIN_SUCCESS", "LOGOUT", "LOGIN_FAILED", "PAYMENT_DONE")
    
    // SAM konvertatsiyasi: anonim sinf o'rniga to'g'ridan-to'g'ri lambda!
    val logins = filterEvents(rawEvents) { it.startsWith("LOGIN") }
    
    println("Kirish hodisalari: $logins")
}""",
        "'fun interface' yagona mavhum metodga ega interfeys (SAM) bo'lib, uning obyektini to'g'ridan-to'g'ri lambda orqali hosil qilish imkonini beradi. Bu kodni juda toza va ixcham qiladi.",
        """Kirish hodisalari: [LOGIN_SUCCESS, LOGIN_FAILED]"""
    ),
    (
        265,
        "Merosxo'rlikda Smart Cast imkoniyati",
        "Ota sinf turi sifatida qabul qilingan o'zgaruvchini 'is' tekshiruvidan keyin bola sinf metodlari bilan ishlatish.",
        """open class Media
class Audio(val bitrate: Int) : Media() {
    fun playAudio() = "Audio yangramoqda ($bitrate kbps)"
}
class Video(val resolution: String) : Media() {
    fun playVideo() = "Video namoyish etilmoqda ($resolution)"
}

fun playMedia(media: Media) {
    when (media) {
        is Audio -> println(media.playAudio()) // Audio ga avtomatik smart cast
        is Video -> println(media.playVideo()) // Video ga avtomatik smart cast
        else -> println("Noma'lum media turi")
    }
}

fun main() {
    playMedia(Audio(320))
    playMedia(Video("4K Ultra HD"))
}""",
        "Kotlinda 'is SubClass' tekshiruvi polimorfik iyerarxiyalarda o'zgaruvchini darhol o'sha bola sinfga smart cast qiladi va casting xatolarini bartaraf etadi.",
        """Audio yangramoqda (320 kbps)
Video namoyish etilmoqda (4K Ultra HD)"""
    ),
    (
        266,
        "Abstrakt sinfda template method andozasi (Template Method Pattern)",
        "Umumiy algoritmni ota abstrakt sinfda yozib, qadamlarni bola sinflarga yuklang.",
        """abstract class DataParser {
    // Shablon metod:
    fun parseData(rawInput: String) {
        val sanitized = sanitize(rawInput)
        val parsed = executeParse(sanitized)
        save(parsed)
    }

    private fun sanitize(input: String): String = input.trim()
    
    // Bola sinflar amalga oshirishi shart bo'lgan mavhum qadam:
    abstract fun executeParse(cleanInput: String): String

    private fun save(data: String) {
        println("[SAQLANDI]: $data")
    }
}

class CsvParser : DataParser() {
    override fun executeParse(cleanInput: String): String {
        return "CSV qatorlari ajratildi: [${cleanInput.replace(",", " | ")}]"
    }
}

fun main() {
    val parser = CsvParser()
    parser.parseData("  olma,nok,uzum  ")
}""",
        "Template Method andozasida algoritm skeleti ota sinfning umumiy metodida belgilanadi, o'zgaruvchan qadamlar esa abstrakt metodlar orqali subklasslarga delegatsiya qilinadi.",
        """[SAQLANDI]: CSV qatorlari ajratildi: [olma | nok | uzum]"""
    ),
    (
        267,
        "Interfeysda shartli delegatsiya: 'by' kalit so'zi",
        "Sinf interfeysni o'zi yozmasdan, tayyor obyektga 'by delegate' orqali delegatsiya qilsin.",
        """interface Logger {
    fun log(msg: String)
}

class ConsoleLogger : Logger {
    override fun log(msg: String) {
        println("[CONSOLE]: $msg")
    }
}

// Class Delegation: AppService Logger interfeysini ConsoleLogger ga topshiradi
class AppService(loggerDelegate: Logger) : Logger by loggerDelegate {
    fun doSomething() {
        log("Xizmat o'z ishini bajardi")
    }
}

fun main() {
    val logger = ConsoleLogger()
    val app = AppService(logger)
    
    app.doSomething()
    app.log("To'g'ridan-to'g'ri log chaqirildi")
}""",
        "Kotlinda sinf darajasidagi delegatsiya 'class A : Interface by delegateObject' sintaksisi bilan amalga oshiriladi. Bu 'Merosxo'rlikdan ko'ra kompozitsiyani afzal biling' (Favor composition over inheritance) tamoyilini til darajasida qulaylashtiradi.",
        """[CONSOLE]: Xizmat o'z ishini bajardi
[CONSOLE]: To'g'ridan-to'g'ri log chaqirildi"""
    ),
    (
        268,
        "Abstrakt xususiyatlar bilan hisob-kitoblar",
        "Ota sinfda soliq stavkasini abstrakt qoldirib, bola sinflarda to'lovlarni hisoblang.",
        """abstract class Employee(val name: String, val baseSalary: Double) {
    abstract val taxRate: Double

    fun netSalary(): Double {
        return baseSalary * (1 - taxRate)
    }
}

class StandardEmployee(name: String, baseSalary: Double) : Employee(name, baseSalary) {
    override val taxRate: Double = 0.12 // 12%
}

class ExpatEmployee(name: String, baseSalary: Double) : Employee(name, baseSalary) {
    override val taxRate: Double = 0.20 // 20%
}

fun main() {
    val emp1 = StandardEmployee("Javohir", 10_000_000.0)
    val emp2 = ExpatEmployee("Jon", 10_000_000.0)
    
    println("${emp1.name} sof maoshi: %,.0f UZS".format(emp1.netSalary()))
    println("${emp2.name} sof maoshi: %,.0f UZS".format(emp2.netSalary()))
}""",
        "Abstrakt xususiyatlar orqali har bir toifadagi xodim uchun mos keluvchi koeffitsiyentlar majburiy qilinadi va umumiy hisob-kitob ota sinfning 'netSalary()' metodida markazlashgan holda qoladi.",
        """Javohir sof maoshi: 8,800,000 UZS
Jon sof maoshi: 8,000,000 UZS"""
    ),
    (
        269,
        "Merosxo'rlikda tenglikni (equals) to'g'ri taqqoslash",
        "Bola sinflar obyektlarini taqqoslashda 'other !is BaseClass' tekshiruvining o'rni.",
        """open class Item(val id: Long) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is Item) return false
        return this.id == other.id
    }

    override fun hashCode(): Int = id.hashCode()
}

class Book(id: Long, val title: String) : Item(id)

fun main() {
    val item1 = Item(100L)
    val book1 = Book(100L, "Kotlin In Action")
    
    println("item1 == book1: ${item1 == book1}")
}""",
        "Merosxo'rlikda 'equals' ni qayta yozishda simmetriya va tranzitivlik qoidalariga qat'iy amal qilinishi shart. Odatda faqat birlamchi identifikator (id) tekshiriladi.",
        """item1 == book1: true"""
    ),
    (
        270,
        "Interfeysda xususiyatlar delegatsiyasi",
        "Interfeysdan kelgan xususiyatni sinf ichida 'by lazy' orqali amalga oshirish.",
        """interface HeavyDataLoader {
    val data: List<String>
}

class RemoteDataLoader : HeavyDataLoader {
    override val data: List<String> by lazy {
        println("--> Masofaviy ma'lumotlar yuklanmoqda...")
        listOf("Yozuv 1", "Yozuv 2", "Yozuv 3")
    }
}

fun main() {
    val loader = RemoteDataLoader()
    println("Obyekt tayyor.")
    println("Yuklangan ma'lumotlar: ${loader.data}")
}""",
        "Interfeysdagi mavhum 'val data' xususiyatini quyi sinfda 'by lazy' delegatsiyasi orqali amalga oshirish mumkin. Bu interfeys kontraktiga to'liq mos keladi.",
        """Obyekt tayyor.
--> Masofaviy ma'lumotlar yuklanmoqda...
Yuklangan ma'lumotlar: [Yozuv 1, Yozuv 2, Yozuv 3]"""
    ),
    (
        271,
        "Abstrakt sinf konstruktorida 'open' metodni chaqirish xavfi",
        "Ota sinf konstruktorida 'open' metodni chaqirish bola sinf xususiyatlari hali initsializatsiya bo'lmasdan oldin ishlash xavfini tushuntiring.",
        """open class Base {
    open val size: Int = 10

    init {
        // DIQQAT: Ota sinf konstruktorida open xususiyatni ishlatish:
        println("Base init: size = $size")
    }
}

class Sub : Base() {
    override val size: Int = 20
}

fun main() {
    val s = Sub()
    println("Sub yaratilgandan so'ng size: ${s.size}")
}""",
        "Kotlinda ota sinf konstruktori bola sinf xususiyatlari initsializatsiya bo'lishidan oldin ishlaydi. Agar ota sinf konstruktori 'open' a'zoga murojaat qilsa, u hali initsializatsiya bo'lmagan sukut qiymatini (0 yoki null) ko'radi. Shu sababli konstruktorda 'open' metodlarni chaqirish qat'iyan tavsiya etilmaydi.",
        """Base init: size = 0
Sub yaratilgandan so'ng size: 20"""
    ),
    (
        272,
        "Interfeys orqali hodisalarni tarqatish: Observer Pattern",
        "Interfeys yordamida tinglovchilar (Observers) ro'yxatini boshqaring.",
        """interface OrderListener {
    fun onOrderPlaced(orderId: String)
}

class OrderDispatcher {
    private val listeners = mutableListOf<OrderListener>()

    fun addListener(l: OrderListener) = listeners.add(l)

    fun placeOrder(orderId: String) {
        println("Buyurtma berildi: $orderId")
        listeners.forEach { it.onOrderPlaced(orderId) }
    }
}

class SmsNotifier : OrderListener {
    override fun onOrderPlaced(orderId: String) {
        println("SMS: Sizning buyurtmangiz #$orderId qabul qilindi.")
    }
}

fun main() {
    val dispatcher = OrderDispatcher()
    dispatcher.addListener(SmsNotifier())
    dispatcher.placeOrder("ORD-9911")
}""",
        "Observer andozasi obyektlar o'rtasida bo'sh bog'lanishni (loose coupling) ta'minlaydi: 'OrderDispatcher' tinglovchilarning ichki tuzilishini bilmaydi, faqat 'OrderListener' interfeysini chaqiradi.",
        """Buyurtma berildi: ORD-9911
SMS: Sizning buyurtmangiz #ORD-9911 qabul qilindi."""
    ),
    (
        273,
        "Ko'p pog'onali merosxo'rlik zanjiri (Multilevel Inheritance)",
        "3 darajali merosxo'rlik iyerarxiyasida xususiyatlarning uzatilishini ko'rsating.",
        """open class LivingOrganism {
    fun breathe() = "Nafas olmoqda"
}

open class Mammal : LivingOrganism() {
    fun feedMilk() = "Sut emizmoqda"
}

class Human(val name: String) : Mammal() {
    fun speak() = "$name gapirmoqda"
}

fun main() {
    val person = Human("Anvar")
    println(person.breathe())
    println(person.feedMilk())
    println(person.speak())
}""",
        "Kotlinda sinflar faqat bitta ota sinfga ega bo'lishi mumkin (single inheritance), ammo zanjir bo'yicha cheksiz darajada pastga qarab chuqurlashishi mumkin.",
        """Nafas olmoqda
Sut emizmoqda
Anvar gapirmoqda"""
    ),
    (
        274,
        "Interfeysda ichki yordamchi modellar e'lon qilish",
        "Interfeys ichida unga tegishli 'Result' yoki 'Status' modellarini joylashtiring.",
        """interface AuthProvider {
    sealed class Result {
        data class Success(val token: String) : Result()
        data class Failure(val error: String) : Result()
    }

    fun authenticate(credentials: String): Result
}

class TokenAuthProvider : AuthProvider {
    override fun authenticate(credentials: String): AuthProvider.Result {
        return if (credentials == "valid_key") {
            AuthProvider.Result.Success("JWT_SECURE_TOKEN_XYZ")
        } else {
            AuthProvider.Result.Failure("Kalit noto'g'ri")
        }
    }
}

fun main() {
    val auth = TokenAuthProvider()
    val res = auth.authenticate("valid_key")
    when (res) {
        is AuthProvider.Result.Success -> println("Token: ${res.token}")
        is AuthProvider.Result.Failure -> println("Xato: ${res.error}")
    }
}""",
        "Interfeys ichida uning domenga tegishli modellarini e'lon qilish kodni modulli, tushunarli va yuqori darajada bog'langan (cohesive) saqlashga xizmat qiladi.",
        """Token: JWT_SECURE_TOKEN_XYZ"""
    ),
    (
        275,
        "Abstrakt sinfda statik metodlar: Companion object merosi",
        "Abstrakt sinf ichidagi companion object orqali umumiy yordamchi fabrika yaratish.",
        """abstract class DatabaseEntity(val id: Long) {
    companion object {
        fun isValidId(id: Long): Boolean = id > 0
    }
}

class UserEntity(id: Long, val name: String) : DatabaseEntity(id)

fun main() {
    println("ID 105 yaroqlimi: ${DatabaseEntity.isValidId(105L)}")
    println("ID -5 yaroqlimi: ${DatabaseEntity.isValidId(-5L)}")
}""",
        "Abstrakt sinf ichidagi 'companion object' uning barcha bola sinflari uchun umumiy statik vositalarni taqdim etadi.",
        """ID 105 yaroqlimi: true
ID -5 yaroqlimi: false"""
    ),
    (
        276,
        "Interfeyslarni filtrlash: filterIsInstance()",
        "Turli interfeyslarni amalga oshirgan obyektlar ro'yxatidan faqat kerakli interfeysga moslarini ajratib oling.",
        """interface Flyable {
    fun fly()
}

class Bird : Flyable {
    override fun fly() = println("Qush osmonda uchmoqda")
}

class Airplane : Flyable {
    override fun fly() = println("Samolyot parvoz qilmoqda")
}

class Car {
    fun drive() = println("Mashina yo'lda yurmoqda")
}

fun main() {
    val mixedList: List<Any> = listOf(Bird(), Car(), Airplane())
    
    val flyingObjects: List<Flyable> = mixedList.filterIsInstance<Flyable>()
    
    println("Uchuvchi obyektlar soni: ${flyingObjects.size}")
    flyingObjects.forEach { it.fly() }
}""",
        "'filterIsInstance<T>()' ro'yxatdagi elementlarni berilgan tur (yoki interfeys) bo'yicha filtrlab, natijani to'g'ridan-to'g'ri o'sha turdagi ro'yxat sifatida qaytaradi.",
        """Uchuvchi obyektlar soni: 2
Qush osmonda uchmoqda
Samolyot parvoz qilmoqda"""
    ),
    (
        277,
        "Merosxo'rlikda xususiyat ko'rinishini kengaytirish",
        "Ota sinfdagi 'protected' a'zoni bola sinfda 'public' qilib qayta yozish.",
        """open class CoreModule {
    protected open fun internalApi(): String = "Maxfiy yadro javobi"
}

class PublicFacade : CoreModule() {
    // protected ni public qilib kengaytirish ruxsat etilgan:
    public override fun internalApi(): String {
        return super.internalApi() + " [Ommaga ochildi]"
    }
}

fun main() {
    val facade = PublicFacade()
    println(facade.internalApi())
}""",
        "Kotlinda 'override' qilayotganda metodning ko'rinish darajasini kengaytirish mumkin (masalan, protected dan public ga), lekin toraytirib bo'lmaydi (public dan private ga o'tkazib bo'lmaydi).",
        """Maxfiy yadro javobi [Ommaga ochildi]"""
    ),
    (
        278,
        "Interfeysda ziddiyatli xususiyatlar (Property Conflicts)",
        "Ikki interfeysda bir xil nomli xususiyat e'lon qilinganda ularni bitta xususiyat bilan hal qilish.",
        """interface NamedA { val title: String }
interface NamedB { val title: String }

class ArticleHeader(override val title: String) : NamedA, NamedB

fun main() {
    val header = ArticleHeader("Kotlin 2.0 yangiliklari")
    println("Sarlavha: ${header.title}")
}""",
        "Agar ikki interfeys bir xil nom va turdagi xususiyatni talab qilsa, bola sinfdagi bitta 'override val' ikkala interfeys shartini ham birdaniga qanoatlantiradi.",
        """Sarlavha: Kotlin 2.0 yangiliklari"""
    ),
    (
        279,
        "Merosxo'rlikda toString() metodini bosqichma-bosqich yig'ish",
        "Har bir darajadagi xususiyatlarni 'super.toString()' orqali qo'shib borish.",
        """open class BaseEntity(val id: Long) {
    override fun toString(): String = "id=$id"
}

class ProductEntity(id: Long, val sku: String) : BaseEntity(id) {
    override fun toString(): String = "ProductEntity(${super.toString()}, sku='$sku')"
}

fun main() {
    val p = ProductEntity(45L, "SKU-9900")
    println(p)
}""",
        "'super.toString()' chaqiruvi orqali ota sinf ma'lumotlarini bola sinf matnli tavsifiga xavfsiz qo'shish mumkin.",
        """ProductEntity(id=45, sku='SKU-9900')"""
    ),
    (
        280,
        "Interfeyslar bilan Strategy Pattern (Strategiya andozasi)",
        "Turli siqish (compression) algoritmlarini interfeys orqali almashtirish.",
        """interface CompressionStrategy {
    fun compress(files: List<String>): String
}

class ZipCompression : CompressionStrategy {
    override fun compress(files: List<String>): String = "ZIP arxivi: ${files.size} ta fayl"
}

class RarCompression : CompressionStrategy {
    override fun compress(files: List<String>): String = "RAR arxivi: ${files.size} ta fayl"
}

class Archiver(var strategy: CompressionStrategy) {
    fun createArchive(files: List<String>) {
        println(strategy.compress(files))
    }
}

fun main() {
    val archiver = Archiver(ZipCompression())
    archiver.createArchive(listOf("f1.txt", "f2.txt"))
    
    archiver.strategy = RarCompression()
    archiver.createArchive(listOf("f3.txt"))
}""",
        "Strategy andozasi algoritmlar oilasini interfeys ortiga yashirib, ish vaqtida ularni erkin almashtirish imkonini beradi.",
        """ZIP arxivi: 2 ta fayl
RAR arxivi: 1 ta fayl"""
    ),
    (
        281,
        "Abstrakt sinfda xususiyatlarni hisoblash formulasini o'rnatish",
        "Geometrik shakllar perimetrini abstrakt metodlar orqali markaziy formulaga kiritish.",
        """abstract class Polygon {
    abstract fun getSides(): List<Double>

    fun calculatePerimeter(): Double {
        return getSides().sum()
    }
}

class Quadrilateral(val a: Double, val b: Double, val c: Double, val d: Double) : Polygon() {
    override fun getSides(): List<Double> = listOf(a, b, c, d)
}

fun main() {
    val quad = Quadrilateral(3.0, 4.0, 5.0, 6.0)
    println("To'rtburchak perimetri: ${quad.calculatePerimeter()}")
}""",
        "Ota sinf umumiy hisoblash formulasini bitta joyda saqlaydi, bola sinf esa faqat o'ziga xos tomonlar ro'yxatini qaytaradi.",
        """To'rtburchak perimetri: 18.0"""
    ),
    (
        282,
        "Interfeysda ko'p qirrali meros: Dekoratordan foydalanish",
        "Interfeysni o'rab oluvchi va uning xatti-harakatini boyituvchi Decorator klassini yozing.",
        """interface Notifier {
    fun send(message: String)
}

class EmailNotifier : Notifier {
    override fun send(message: String) = println("Email yuborildi: $message")
}

class LoggingNotifierDecorator(val delegate: Notifier) : Notifier {
    override fun send(message: String) {
        println("[LOG]: Xabar yuborish boshlanmoqda...")
        delegate.send(message)
        println("[LOG]: Xabar yuborish yakunlandi.")
    }
}

fun main() {
    val base = EmailNotifier()
    val decorated = LoggingNotifierDecorator(base)
    decorated.send("Tizim yangilandi")
}""",
        "Decorator andozasi obyektning asl tuzilishini o'zgartirmasdan, uni o'rab oluvchi sinf orqali qo'shimcha xatti-harakat beradi.",
        """[LOG]: Xabar yuborish boshlanmoqda...
Email yuborildi: Tizim yangilandi
[LOG]: Xabar yuborish yakunlandi."""
    ),
    (
        283,
        "Merosxo'rlikda 'sealed interface' bilan turlarni cheklash",
        "Faqat ma'lum bir fayl ichidagi sinflargina amalga oshira oladigan 'sealed interface' tuzing.",
        """sealed interface NetworkState {
    object Idle : NetworkState
    object Loading : NetworkState
    data class Success(val data: String) : NetworkState
    data class Error(val message: String) : NetworkState
}

fun renderState(state: NetworkState): String = when (state) {
    is NetworkState.Idle -> "Kutish holati"
    is NetworkState.Loading -> "Yuklanmoqda..."
    is NetworkState.Success -> "Muvaffaqiyatli: ${state.data}"
    is NetworkState.Error -> "Xatolik: ${state.message}"
}

fun main() {
    println(renderState(NetworkState.Loading))
    println(renderState(NetworkState.Success("Foydalanuvchi ma'lumotlari")))
}""",
        "'sealed interface' o'zining barcha realizatsiyalarini kompilyatsiya vaqtida qat'iy ma'lum qiladi. Natijada 'when' ifodalarida 'else' tarmog'iga mutlaqo ehtiyoj qolmaydi.",
        """Yuklanmoqda...
Muvaffaqiyatli: Foydalanuvchi ma'lumotlari"""
    ),
    (
        284,
        "Sinf delegatsiyasida metodni qisman qayta yozish (Overriding Delegated Methods)",
        "'by' bilan delegatsiya qilingan interfeysning faqat bitta metodini o'zingiz xohlagancha o'zgartiring.",
        """interface Greeter {
    fun sayHello()
    fun sayGoodbye()
}

class EnglishGreeter : Greeter {
    override fun sayHello() = println("Hello!")
    override fun sayGoodbye() = println("Goodbye!")
}

class UzbekCustomGreeter(delegate: Greeter) : Greeter by delegate {
    // Faqat sayHello() ni o'zgartiramiz, sayGoodbye() esa delegate ga ketadi:
    override fun sayHello() = println("Assalomu alaykum!")
}

fun main() {
    val greeter = UzbekCustomGreeter(EnglishGreeter())
    greeter.sayHello()
    greeter.sayGoodbye()
}""",
        "Sinf delegatsiyasida barcha metodlar avtomatik delegatga yo'naltiriladi, ammo xohlagan metodni 'override' qilib maxsus xatti-harakat berish mumkin.",
        """Assalomu alaykum!
Goodbye!"""
    ),
    (
        285,
        "Abstrakt sinflar va Interfeyslar solishtiruvi",
        "Holat (state) saqlash zarur bo'lganda abstrakt sinf, faqat xatti-harakat kerak bo'lganda interfeys tanlanishini ko'rsating.",
        """abstract class BaseRepository(val connectionString: String) {
    fun connect() = println("Baza ulandi: $connectionString")
}

interface CrudOperations<T> {
    fun save(item: T)
    fun findById(id: Long): T?
}

class UserRepository(conn: String) : BaseRepository(conn), CrudOperations<String> {
    override fun save(item: String) = println("Foydalanuvchi saqlandi: $item")
    override fun findById(id: Long): String? = "User_$id"
}

fun main() {
    val repo = UserRepository("postgres://localhost:5432")
    repo.connect()
    repo.save("Olimjon")
    println("Topildi: ${repo.findById(10L)}")
}""",
        "Abstrakt sinf konstruktor va holat (fields) saqlay oladi, ammo sinf faqat bitta ota klassga ega bo'lishi mumkin. Interfeyslar holat saqlamaydi, ammo ko'plab interfeyslarni bitta sinfga ulash mumkin.",
        """Baza ulandi: postgres://localhost:5432
Foydalanuvchi saqlandi: Olimjon
Topildi: User_10"""
    ),
    (
        286,
        "Merosxo'rlik va Xotira: Obyekt havolalari va Garbage Collector",
        "Ota sinf va bola sinf havolalarini xavfsiz boshqarish.",
        """open class LargeObject(val tag: String)
class SpecializedObject(tag: String, val extraData: String) : LargeObject(tag)

fun main() {
    var ref: LargeObject? = SpecializedObject("TAG_1", "Og'ir ma'lumotlar")
    println("Tag: ${ref?.tag}")
    
    // Xotirani tozalash uchun havolani uzish:
    ref = null
    println("Havola uzildi: $ref")
}""",
        "Polimorfizmda bola sinf obyektiga ota sinf havolasi orqali murojaat qilish odatiy holdir. Obyekt xotiradan tozalanishi uchun barcha faol havolalar null ga aylanishi kerak.",
        """Tag: TAG_1
Havola uzildi: null"""
    ),
    (
        287,
        "Interfeysda generik cheklovlar bilan polimorfizm",
        "Comparable interfeysini kengaytiruvchi umumiy saralovchi servis tuzing.",
        """interface MinMaxFinder<T : Comparable<T>> {
    fun findMin(list: List<T>): T? = list.minOrNull()
    fun findMax(list: List<T>): T? = list.maxOrNull()
}

class NumberAnalyzer : MinMaxFinder<Int>

fun main() {
    val analyzer = NumberAnalyzer()
    val scores = listOf(78, 92, 65, 88)
    
    println("Eng past ball: ${analyzer.findMin(scores)}")
    println("Eng yuqori ball: ${analyzer.findMax(scores)}")
}""",
        "Generik interfeyslar 'T : Comparable<T>' kabi yuqori chegaralar orqali ma'lumotlar turini cheklaydi va xavfsiz taqqoslashni kafolatlaydi.",
        """Eng past ball: 65
Eng yuqori ball: 92"""
    ),
    (
        288,
        "Merosxo'rlikda keshni tozalash qoidalari",
        "Bola sinf yangi ma'lumot qo'shganda ota sinfning umumiy keshini tozalashi.",
        """open class CacheableRepository {
    protected var isCacheDirty = false

    fun readCache() {
        if (isCacheDirty) {
            println("[KESH]: Kesh eskirgan, yangilanmoqda...")
            isCacheDirty = false
        } else {
            println("[KESH]: Kesh toza.")
        }
    }
}

class ProductRepository : CacheableRepository() {
    fun addProduct(name: String) {
        println("Mahsulot qo'shildi: $name")
        isCacheDirty = true // Ota sinf xususiyatini yangilash
    }
}

fun main() {
    val repo = ProductRepository()
    repo.readCache()
    repo.addProduct("Monitor")
    repo.readCache()
}""",
        "'protected' modifikatori orqali ota sinfning ichki holatini bola sinflar uchun ochiq, ammo tashqi dunyodan yopiq saqlash mumkin.",
        """[KESH]: Kesh toza.
Mahsulot qo'shildi: Monitor
[KESH]: Kesh eskirgan, yangilanmoqda..."""
    ),
    (
        289,
        "Interfeyslarni kompozitsiya bilan boyitish: Mixin analogi",
        "Interfeyslardagi standart metodlar orqali sinflarga qo'shimcha xatti-harakat (mixin) qo'shish.",
        """interface JsonSerializable {
    fun toJson(): String = "{\\"type\\": \\"${this::class.simpleName}\\"}"
}

interface Auditable {
    fun getCreatedDate(): String = "2026-11-08"
}

class SystemConfig : JsonSerializable, Auditable

fun main() {
    val config = SystemConfig()
    println(config.toJson())
    println("Yaratilgan sana: ${config.getCreatedDate()}")
}""",
        "Kotlinda interfeyslar standart metodlarga ega bo'lganligi sababli, boshqa tillardagi 'traits' yoki 'mixins' imkoniyatini bemalol bajaradi.",
        """{"type": "SystemConfig"}
Yaratilgan sana: 2026-11-08"""
    ),
    (
        290,
        "Merosxo'rlikda deep copy (Chuqur nusxa) polimorfizmi",
        "Ota sinf interfeysida 'clone/copy' shartnomasini e'lon qilish.",
        """interface Copyable<T> {
    fun makeCopy(): T
}

data class Node(val id: Int, val name: String) : Copyable<Node> {
    override fun makeCopy(): Node = this.copy()
}

fun main() {
    val n1 = Node(1, "BoshTugun")
    val n2 = n1.makeCopy()
    
    println("Nusxa: $n2 (Bir xil obyektmi: ${n1 === n2})")
}""",
        "Obyektlarni mustaqil klonlash uchun 'Copyable<T>' generik interfeysi orqali polimorfik nusxalash amalga oshiriladi.",
        """Nusxa: Node(id=1, name=BoshTugun) (Bir xil obyektmi: false)"""
    ),
    (
        291,
        "Shartli chaqiruv: Ota sinf abstraksiyasida xatoliklarni qayta ishlash",
        "Barcha xizmat sinflari uchun xavfsiz bajaruvchi umumiy ota sinf yarating.",
        """abstract class SafeService {
    fun <T> executeSafely(actionName: String, block: () -> T): T? {
        return try {
            block()
        } catch (e: Exception) {
            println("[$actionName] da xatolik yuz berdi: ${e.message}")
            null
        }
    }
}

class PaymentService : SafeService() {
    fun pay(amount: Double) = executeSafely("To'lov") {
        if (amount <= 0) throw IllegalArgumentException("Summa xato")
        "To'lov muvaffaqiyatli: $$amount"
    }
}

fun main() {
    val service = PaymentService()
    println(service.pay(100.0))
    println(service.pay(-50.0))
}""",
        "Ota sinfda xatoliklarni ushlovchi umumiy shablon yaratish kod takrorlanishining oldini oladi.",
        """To'lov muvaffaqiyatli: $100.0
[To'lov] da xatolik yuz berdi: Summa xato
null"""
    ),
    (
        292,
        "Interfeysda kontraktlar va tekshiruvlar",
        "Interfeys standart metodida argumentlarni tekshirish (require/check).",
        """interface Validator<T> {
    fun isValid(item: T): Boolean

    fun validateOrThrow(item: T) {
        require(isValid(item)) { "Element validatsiyadan o'tmadi: $item" }
    }
}

class PositiveNumberValidator : Validator<Int> {
    override fun isValid(item: Int): Boolean = item > 0
}

fun main() {
    val valId = PositiveNumberValidator()
    valId.validateOrThrow(15)
    println("15 muvaffaqiyatli tekshirildi.")
    
    try {
        valId.validateOrThrow(-3)
    } catch (e: IllegalArgumentException) {
        println("Xatolik ushlandi: ${e.message}")
    }
}""",
        "Interfeysdagi standart metod 'validateOrThrow' mavhum 'isValid' ga tayanib o'z ichida tekshiruv o'tkaza oladi.",
        """15 muvaffaqiyatli tekshirildi.
Xatolik ushlandi: Element validatsiyadan o'tmadi: -3"""
    ),
    (
        293,
        "Merosxo'rlik zanjirida konstruktorni yashirish va subklass yaratish",
        "Ota sinf konstruktorini 'protected' qilib, faqat subklasslar orqali yaratilishini ta'minlash.",
        """open class RestrictedBase protected constructor(val secretKey: String)

class AuthorizedSubClass(key: String) : RestrictedBase(key) {
    fun printKey() = println("Kalit: $secretKey")
}

fun main() {
    // val b = RestrictedBase("test") // Xato: protected constructor
    val sub = AuthorizedSubClass("SECRET_XYZ_99")
    sub.printKey()
}""",
        "'protected constructor' sinfning to'g'ridan-to'g'ri tashqaridan yaratilishini taqiqlaydi va faqat subklasslar orqali yaratilishga ruxsat beradi.",
        """Kalit: SECRET_XYZ_99"""
    ),
    (
        294,
        "Interfeysda yagona metod va Kotlin Lambdasi bilan qulaylik",
        "Custom Comparator interfeysi o'rniga Kotlin lambda komparatorlaridan foydalanish.",
        """data class CarItem(val name: String, val horsePower: Int)

fun main() {
    val cars = listOf(
        CarItem("Nexia", 85),
        CarItem("Malibu", 250),
        CarItem("Gentra", 107)
    )
    
    // Comparator interfeysi lambda orqali beriladi:
    val sortedCars = cars.sortedWith { c1, c2 -> c1.horsePower.compareTo(c2.horsePower) }
    
    println("Ot kuchi bo'yicha saralangan:")
    sortedCars.forEach { println(" - ${it.name}: ${it.horsePower} ot kuchi") }
}""",
        "Java dagi 'java.util.Comparator' Kotlinda SAM interfeys sifatida qabul qilinadi va to'g'ridan-to'g'ri ixcham lambda orqali uzatiladi.",
        """Ot kuchi bo'yicha saralangan:
 - Nexia: 85 ot kuchi
 - Gentra: 107 ot kuchi
 - Malibu: 250 ot kuchi"""
    ),
    (
        295,
        "Merosxo'rlikda o'zgaruvchilar shadowing muammosi",
        "Ota sinf va bola sinfda bir xil nomli mahalliy o'zgaruvchilarni adashtirmaslik qoidasi.",
        """open class SuperUser(val role: String) {
    open fun printRole() = println("SuperUser roli: $role")
}

class AdminUser : SuperUser("ADMIN") {
    override fun printRole() {
        val role = "LOCAL_OVERRIDE"
        println("Mahalliy o'zgaruvchi: $role | Sinf xususiyati: ${this.role}")
    }
}

fun main() {
    val admin = AdminUser()
    admin.printRole()
}""",
        "Agar funksiya ichidagi parametr yoki mahalliy o'zgaruvchi sinf xususiyati bilan bir xil nomlansa, xususiyatga murojaat qilish uchun 'this.property' yozilishi kerak.",
        """Mahalliy o'zgaruvchi: LOCAL_OVERRIDE | Sinf xususiyati: ADMIN"""
    ),
    (
        296,
        "To'lov shlyuzlari arxitekturasi: Payme, Click va Uzum (Amaliy Polimorfizm)",
        "O'zbekiston to'lov tizimlari uchun umumiy interfeys va uning alohida amalga oshirilishi.",
        """interface PaymentGateway {
    val providerName: String
    fun initPayment(amount: Double, orderId: String): Boolean
}

class PaymeGateway : PaymentGateway {
    override val providerName: String = "PAYME"
    override fun initPayment(amount: Double, orderId: String): Boolean {
        println("[$providerName]: Buyurtma $orderId uchun %,.0f UZS tranzaksiya ochildi.".format(amount))
        return true
    }
}

class ClickGateway : PaymentGateway {
    override val providerName: String = "CLICK"
    override fun initPayment(amount: Double, orderId: String): Boolean {
        println("[$providerName]: USSD/Web so'rov yuborildi: %,.0f UZS.".format(amount))
        return true
    }
}

fun main() {
    val gateways: List<PaymentGateway> = listOf(PaymeGateway(), ClickGateway())
    
    for (gw in gateways) {
        gw.initPayment(150_000.0, "ORD-7744")
    }
}""",
        "Polimorfik interfeys orqali ilovaga yangi to'lov tizimlarini qo'shish mavjud kodni o'zgartirmasdan amalga oshiriladi (Open-Closed Principle).",
        """[PAYME]: Buyurtma ORD-7744 uchun 150,000 UZS tranzaksiya ochildi.
[CLICK]: USSD/Web so'rov yuborildi: 150,000 UZS."""
    ),
    (
        297,
        "UI komponentlar iyerarxiyasi (Android View tizimi analogi)",
        "Umumiy 'View' ota sinfidan 'TextView' va 'Button' hosil qiling.",
        """abstract class BaseView(val id: Int) {
    abstract fun draw()
}

class TextView(id: Int, var text: String) : BaseView(id) {
    override fun draw() = println("TextView #$id chizildi: '$text'")
}

class ButtonView(id: Int, var title: String, val onClick: () -> Unit) : BaseView(id) {
    override fun draw() = println("ButtonView #$id chizildi: [$title]")
    fun click() = onClick()
}

fun main() {
    val views: List<BaseView> = listOf(
        TextView(1, "Xush kelibsiz!"),
        ButtonView(2, "Kirish") { println("Tizimga kirish bosildi") }
    )
    
    views.forEach { it.draw() }
}""",
        "Android Jetpack va an'anaviy Android View tizimida barcha UI elementlari 'View' umumiy ota sinfidan meros oladi va o'zining 'draw/measure' metodlarini override qiladi.",
        """TextView #1 chizildi: 'Xush kelibsiz!'
ButtonView #2 chizildi: [Kirish]"""
    ),
    (
        298,
        "Transport vositalari parki (Fleet Management)",
        "Abstrakt transport sinfi, yonilg'i sarfi va harakatlanish logikasini birlashtiring.",
        """abstract class Transport(val licensePlate: String, val fuelCapacity: Double) {
    abstract fun calculateRange(): Double
    fun printInfo() {
        println("Raqam: $licensePlate | Bosib o'tish masofasi: ${calculateRange()} km")
    }
}

class ElectricBus(plate: String, batteryKwh: Double) : Transport(plate, batteryKwh) {
    override fun calculateRange(): Double = fuelCapacity * 1.5 // 1 kVt = 1.5 km
}

class DieselTruck(plate: String, tankLiters: Double) : Transport(plate, tankLiters) {
    override fun calculateRange(): Double = (fuelCapacity / 30.0) * 100.0 // 30L/100km
}

fun main() {
    val bus = ElectricBus("01 A 777 AA", 200.0)
    val truck = DieselTruck("10 B 888 BB", 300.0)
    
    bus.printInfo()
    truck.printInfo()
}""",
        "Transport modellari o'zlarining energiya turiga qarab yurish masofasini har xil hisoblaydi, ammo umumiy park nazorati bitta 'Transport' tipi ostida birlashadi.",
        """Raqam: 01 A 777 AA | Bosib o'tish masofasi: 300.0 km
Raqam: 10 B 888 BB | Bosib o'tish masofasi: 1000.0 km"""
    ),
    (
        299,
        "Xavfsizlik ruxsatnomalari tizimi (RBAC interfeyslari)",
        "Foydalanuvchi huquqlarini interfeyslar kombinatsiyasi orqali boshqaring.",
        """interface ReadPermission { fun canRead(): Boolean = true }
interface WritePermission { fun canWrite(): Boolean = true }
interface DeletePermission { fun canDelete(): Boolean = true }

class GuestUser : ReadPermission
class SuperAdmin : ReadPermission, WritePermission, DeletePermission

fun main() {
    val guest: Any = GuestUser()
    val admin: Any = SuperAdmin()
    
    println("Mehmon o'qiy oladimi: ${guest is ReadPermission}")
    println("Mehmon o'chira oladimi: ${guest is DeletePermission}")
    println("Admin o'chira oladimi: ${admin is DeletePermission}")
}""",
        "Marker va huquq interfeyslari 'is InterfaceName' orqali rollarga asoslangan kirish huquqlarini (Role-Based Access Control) xavfsiz tekshiradi.",
        """Mehmon o'qiy oladimi: true
Mehmon o'chira oladimi: false
Admin o'chira oladimi: true"""
    ),
    (
        300,
        "Merosxo'rlik va interfeyslar bo'yicha to'liq amaliy xulosa",
        "Open class, abstract class, interface, super chaqiruvi va sinf delegatsiyasini bitta yaxlit korxona dasturida jamlang.",
        """interface AuditTrail {
    fun record(action: String)
}

class SystemAudit : AuditTrail {
    override fun record(action: String) {
        println("[AUDIT]: $action (Vaqt: 2026-11-08)")
    }
}

abstract class BaseEnterpriseService(val serviceName: String, audit: AuditTrail) : AuditTrail by audit {
    abstract fun execute(): Boolean

    fun runService() {
        record("Servis ishga tushirildi: $serviceName")
        val success = execute()
        record("Servis yakunlandi. Holat: $success")
    }
}

class PayrollProcessingService(audit: AuditTrail) : BaseEnterpriseService("OylikTo'lovServisi", audit) {
    override fun execute(): Boolean {
        println("Xodimlarga oylik maoshlar tarqatilmoqda...")
        return true
    }
}

fun main() {
    val audit = SystemAudit()
    val payroll = PayrollProcessingService(audit)
    payroll.runService()
}""",
        "Ushbu yakuniy topshiriqda mavzuning barcha asosiy ustunlari: Abstrakt sinf, interfeys, delegatsiya ('by audit'), polimorfik bajarilish va shablon metod bitta professional korxona servisida birlashtirildi.",
        """[AUDIT]: Servis ishga tushirildi: OylikTo'lovServisi (Vaqt: 2026-11-08)
Xodimlarga oylik maoshlar tarqatilmoqda...
[AUDIT]: Servis yakunlandi. Holat: true (Vaqt: 2026-11-08)"""
    )
]

for item in data_06:
    n, title, condition, sol, exp, res = item
    tasks.append(format_task(n, title, condition, sol, exp, res))

save_file("kotlin_06_merosxorlik_va_interfeyslar.md", tasks)
