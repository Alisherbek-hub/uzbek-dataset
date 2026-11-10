# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

data_04 = [
    (
        151,
        "Standart parametrlar (Default Arguments)",
        "Foydalanuvchiga xabar yuboruvchi funksiya yarating. Agar mavzu va ustuvorlik berilmasa, ularga standart qiymatlar berilsin.",
        """fun sendMessage(text: String, subject: String = "Umumiy", priority: Int = 1) {
    println("Xabar: '$text' | Mavzu: $subject | Ustuvorlik: $priority")
}

fun main() {
    sendMessage("Bugun yig'ilish soat 15:00 da")
    sendMessage("Parolni tiklash kodi", "Xavfsizlik", 5)
}""",
        "Kotlinda funksiya parametrlariga standart (default) qiymatlar berish mumkin. Bu Java dagi kabi o'nlab 'overload' (ortiqcha yuklangan) metodlar yozish zaruratini butunlay yo'qotadi.",
        """Xabar: 'Bugun yig'ilish soat 15:00 da' | Mavzu: Umumiy | Ustuvorlik: 1
Xabar: 'Parolni tiklash kodi' | Mavzu: Xavfsizlik | Ustuvorlik: 5"""
    ),
    (
        152,
        "Nomlangan argumentlar (Named Arguments)",
        "Ko'p parametrli funksiyani chaqirishda parametr nomlarini aniq ko'rsatib, parametrlar tartibini o'zgartiring.",
        """fun createUserProfile(username: String, email: String, isActive: Boolean = true, role: String = "User") {
    println("Profil: $username | Email: $email | Faol: $isActive | Rol: $role")
}

fun main() {
    // Argumentlar parametr nomi orqali ixtiyoriy tartibda uzatiladi:
    createUserProfile(
        role = "SuperAdmin",
        username = "nodir_dev",
        email = "nodir@tech.uz"
    )
}""",
        "Nomlangan argumentlar kodning o'qilishini keskin yaxshilaydi. Ayniqsa bir nechta bir xil turdagi (masalan, bir nechta Boolean yoki String) parametrlarga ega funksiyalarda qiymatlarni adashtirib yuborishning oldini oladi.",
        """Profil: nodir_dev | Email: nodir@tech.uz | Faol: true | Rol: SuperAdmin"""
    ),
    (
        153,
        "Java mosligi: @JvmOverloads annotatsiyasi",
        "Kotlinda standart parametrlarga ega funksiyani Java kodidan ham bir nechta variantda chaqirish uchun '@JvmOverloads' annotatsiyasini qo'llang.",
        """class NotificationManager {
    @JvmOverloads
    fun notify(message: String, channel: String = "SMS", repeatCount: Int = 1) {
        println("Bildirishnoma: '$message' | Kanal: $channel | Takror: $repeatCount marta")
    }
}

fun main() {
    val manager = NotificationManager()
    manager.notify("Balans kam qoldi")
    manager.notify("Tizim yangilandi", "Push")
    manager.notify("Parol o'zgardi", "Email", 2)
}""",
        "'@JvmOverloads' annotatsiyasi Kotlin kompilyatoriga Java uchun avtomatik tarzda barcha kombinatsiyalardagi ortiqcha yuklangan metodlarni (overloaded methods) bayt-kod darajasida generatsiya qilishni buyuradi.",
        """Bildirishnoma: 'Balans kam qoldi' | Kanal: SMS | Takror: 1 marta
Bildirishnoma: 'Tizim yangilandi' | Kanal: Push | Takror: 1 marta
Bildirishnoma: 'Parol o'zgardi' | Kanal: Email | Takror: 2 marta"""
    ),
    (
        154,
        "Yakka ifodali funksiyalar (Single-Expression Functions)",
        "Funksiya tanasi bitta arifmetik ifodadan iborat bo'lganda jingalak qavslarsiz va 'return' so'zisiz yozing.",
        """fun calculateCircleArea(radius: Double): Double = Math.PI * radius * radius

fun getGreeting(name: String): String = "Assalomu alaykum, $name!"

fun main() {
    println("Radius 4 doira yuzi: ${calculateCircleArea(4.0)}")
    println(getGreeting("Farhod"))
}""",
        "Agar funksiya faqat bitta ifodadan iborat bo'lsa, '=' belgisi orqali to'g'ridan-to'g'ri biriktiriladi. Qaytish turi ham Type Inference tufayli avtomatik aniqlanishi mumkin.",
        """Radius 4 doira yuzi: 50.26548245743669
Assalomu alaykum, Farhod!"""
    ),
    (
        155,
        "O'zgaruvchan sondagi argumentlar: 'vararg' kalit so'zi",
        "Ixtiyoriy sondagi butun sonlarni qabul qilib, ularning o'rtacha qiymatini hisoblovchi funksiya yozing.",
        """fun calculateAverage(vararg numbers: Double): Double {
    if (numbers.isEmpty()) return 0.0
    return numbers.sum() / numbers.size
}

fun main() {
    println("3 ta son o'rtachasi: " + calculateAverage(10.0, 20.0, 30.0))
    println("5 ta son o'rtachasi: " + calculateAverage(5.0, 15.0, 25.0, 35.0, 45.0))
    println("Bo'sh parametr: " + calculateAverage())
}""",
        "'vararg' kalit so'zi parametrga istalgancha (0 yoki undan ko'p) argumentlar uzatish imkonini beradi. Funksiya ichida 'vararg' parametri oddiy massiv (DoubleArray yoki Array<T>) kabi ko'rinadi.",
        """3 ta son o'rtachasi: 20.0
5 ta son o'rtachasi: 25.0
Bo'sh parametr: 0.0"""
    ),
    (
        156,
        "Massivni vararg ga uzatish: Yoyish operatori (Spread Operator *)",
        "Mavjud massiv elementlarini 'vararg' qabul qiluvchi funksiyaga yulduzcha '*' operatori orqali uzating.",
        """fun printLogEntries(prefix: String, vararg logs: String) {
    for (log in logs) {
        println("[$prefix]: $log")
    }
}

fun main() {
    val dailyLogs = arrayOf("Server ishga tushdi", "Baza ulandi", "Foydalanuvchi kirdi")
    
    // Spread operator '*' massivni alohida argumentlarga yoyadi:
    printLogEntries("INFO", *dailyLogs, "Kesh tozalandi")
}""",
        "Kotlinda massivni 'vararg' qabul qiluvchi metodga to'g'ridan-to'g'ri berib bo'lmaydi. Massiv nomi oldiga yoyish (spread) operatori '*' qo'yilib, massiv elementlari alohida argumentlar sifatida uzatiladi.",
        """[INFO]: Server ishga tushdi
[INFO]: Baza ulandi
[INFO]: Foydalanuvchi kirdi
[INFO]: Kesh tozalandi"""
    ),
    (
        157,
        "Infix funksiyalar: Qavslarsiz va nuqtasiz chaqiruv",
        "Ikki nuqta orasidagi masofani hisoblovchi yoki yangi obyekt hosil qiluvchi 'infix' funksiya e'lon qiling.",
        """data class Point(val x: Int, val y: Int)

infix fun Point.distanceTo(other: Point): Double {
    val dx = (this.x - other.x).toDouble()
    val dy = (this.y - other.y).toDouble()
    return Math.sqrt(dx * dx + dy * dy)
}

fun main() {
    val p1 = Point(0, 0)
    val p2 = Point(3, 4)
    
    // Infix chaqiruv: nuqta va qavslarsiz!
    val distance = p1 distanceTo p2
    
    println("Masofa: $distance")
}""",
        "'infix' kalit so'zi bilan e'lon qilingan funksiyalar yagona parametrga ega bo'lishi va a'zo yoki kengaytma funksiya bo'lishi shart. Ular 'p1 distanceTo p2' kabi tabiiy tilga yaqin chaqiriladi (masalan, standart kutubxonadagi 'a to b').",
        """Masofa: 5.0"""
    ),
    (
        158,
        "Quyruq rekursiyasi: 'tailrec' modifikatori va stek optimizatsiyasi",
        "Katta sonlar bilan rekursiv faktorial hisoblashda 'StackOverflowError' oldini olish uchun 'tailrec' dan foydalaning.",
        """import java.math.BigInteger

tailrec fun factorialTailrec(n: Long, accumulator: BigInteger = BigInteger.ONE): BigInteger {
    if (n <= 1L) return accumulator
    return factorialTailrec(n - 1L, accumulator.multiply(BigInteger.valueOf(n)))
}

fun main() {
    // tailrec siklga aylanadi va hech qanday stack overflow bo'lmaydi
    val result = factorialTailrec(100L)
    println("100! ning uzunligi: ${result.toString().length} ta raqam")
    println("10! = ${factorialTailrec(10L)}")
}""",
        "'tailrec' modifikatori agar funksiyaning eng oxirgi amali faqat o'zini chaqirish bo'lsa (tail call), rekursiyani oddiy tezkor 'while' sikliga aylantirib kompilyatsiya qiladi. Bu stek to'lib qolish xavfini bartaraf qiladi.",
        """100! ning uzunligi: 158 ta raqam
10! = 3628800"""
    ),
    (
        159,
        "Fayl darajasidagi funksiyalar (Top-Level Functions)",
        "Hech qanday klass yaratmasdan to'g'ridan-to'g'ri fayl ichida mustaqil yordamchi funksiyalar e'lon qiling.",
        """fun formatCurrency(amount: Double): String {
    return "%,.2f UZS".format(amount)
}

fun calculateVat(amount: Double): Double {
    return amount * 0.12
}

fun main() {
    val price = 1_250_000.0
    val vat = calculateVat(price)
    
    println("Narx: ${formatCurrency(price)}")
    println("QQS (12%): ${formatCurrency(vat)}")
}""",
        "Kotlinda Java dagi kabi majburiy statik yordamchi sinflar (masalan 'StringUtils' yoki 'MathUtils') yaratish shart emas. Funksiyalarni faylning yuqori darajasida (top-level) to'g'ridan-to'g'ri yozish mumkin.",
        """Narx: 1,250,000.00 UZS
QQS (12%): 150,000.00 UZS"""
    ),
    (
        160,
        "Mahalliy funksiyalar (Local Functions)",
        "Katta funksiya ichida faqat o'sha funksiyaga kerak bo'ladigan ichma-ich yordamchi funksiya yarating va tashqi o'zgaruvchilardan foydalaning.",
        """fun processUserRegistration(name: String, email: String, age: Int) {
    // Ichki mahalliy funksiya (Local function)
    fun validateField(value: String, fieldName: String) {
        if (value.isBlank()) {
            throw IllegalArgumentException("$fieldName bo'sh bo'lishi mumkin emas!")
        }
    }
    
    validateField(name, "Ism")
    validateField(email, "Email")
    
    if (age < 18) {
        println("Foydalanuvchi voyaga yetmagan: $name")
        return
    }
    
    println("Ro'yxatdan o'tish tasdiqlandi: $name ($email)")
}

fun main() {
    processUserRegistration("Sardor", "sardor@dev.uz", 24)
}""",
        "Kotlinda funksiya ichida boshqa funksiyalarni e'lon qilish mumkin. Mahalliy funksiyalar tashqi funksiyaning barcha o'zgaruvchilariga to'g'ridan-to'g'ri kirish huquqiga ega bo'lib (closure), kodning takrorlanishini yo'qotadi.",
        """Ro'yxatdan o'tish tasdiqlandi: Sardor (sardor@dev.uz)"""
    ),
    (
        161,
        "Operatorlarni qayta yuklash: '+' (plus) operatori",
        "Ikki o'lchovli koordinatalarni 'p1 + p2' shaklida qo'shish imkoniyatini 'operator fun plus' orqali yarating.",
        """data class Vector2D(val x: Double, val y: Double) {
    operator fun plus(other: Vector2D): Vector2D {
        return Vector2D(this.x + other.x, this.y + other.y)
    }
}

fun main() {
    val v1 = Vector2D(3.0, 5.0)
    val v2 = Vector2D(2.0, 4.0)
    
    val sum = v1 + v2 // plus operatori chaqiriladi
    println("v1: $v1")
    println("v2: $v2")
    println("v1 + v2: $sum")
}""",
        "Kotlinda oldindan belgilangan maxsus operator nomlari mavjud (plus, minus, times, div va h.k.). Funksiya oldiga 'operator' kalit so'zini qo'yish orqali standart operatorlar o'z sinflaringiz uchun moslashtiriladi.",
        """v1: Vector2D(x=3.0, y=5.0)
v2: Vector2D(x=2.0, y=4.0)
v1 + v2: Vector2D(x=5.0, y=9.0)"""
    ),
    (
        162,
        "Ko'paytirish va bo'lish operatorlari: '*' va '/'",
        "Moliyaviy ob'ektni butun songa ko'paytirish ('Money * 3') operatorini yarating.",
        """data class Money(val amount: Double, val currency: String) {
    operator fun times(multiplier: Int): Money {
        return Money(this.amount * multiplier, this.currency)
    }
    
    operator fun div(divisor: Int): Money {
        require(divisor != 0) { "0 ga bo'lish mumkin emas!" }
        return Money(this.amount / divisor, this.currency)
    }
}

fun main() {
    val salary = Money(500.0, "USD")
    val bonusQuarter = salary * 3
    val splitPayment = salary / 2
    
    println("3 oylik maosh: $bonusQuarter")
    println("Yarim to'lov: $splitPayment")
}""",
        "'times' ko'paytirish (*), 'div' bo'lish (/) amallarini ifodalaydi. Kotlin tur xavfsizligi doirasida har xil tiplarni bir-biriga ko'paytirish operatorlarini ham e'lon qilish mumkin.",
        """3 oylik maosh: Money(amount=1500.0, currency=USD)
Yarim to'lov: Money(amount=250.0, currency=USD)"""
    ),
    (
        163,
        "Indekslash operatorlarini yuklash: get va set",
        "O'z shaxsiy sinfingizni massiv kabi 'obj[index]' va 'obj[index] = value' shaklida ishlatish uchun 'get' va 'set' operatorlarini yozing.",
        """class KeyValueStore {
    private val storage = mutableMapOf<String, String>()

    operator fun get(key: String): String? {
        return storage[key]
    }

    operator fun set(key: String, value: String) {
        storage[key] = value
    }
}

fun main() {
    val store = KeyValueStore()
    
    // set operatori chaqiriladi:
    store["theme"] = "dark"
    store["language"] = "uz"
    
    // get operatori chaqiriladi:
    println("Mavzu: ${store["theme"]}")
    println("Til: ${store["language"]}")
    println("Shrift: ${store["font"]}")
}""",
        "'operator fun get(key)' massiv yoki xaritalardagi kabi kvadrat qavslar 'obj[key]' orqali o'qishni, 'operator fun set(key, value)' esa 'obj[key] = value' orqali yozishni ta'minlaydi.",
        """Mavzu: dark
Til: uz
Shrift: null"""
    ),
    (
        164,
        "Obyektni funksiya kabi chaqirish: invoke operatori",
        "Sinf nusxasini xuddi funksiya kabi to'g'ridan-to'g'ri qavslar bilan 'instance()' chaqirish uchun 'operator fun invoke' dan foydalaning.",
        """class PasswordValidator(val minLength: Int) {
    operator fun invoke(password: String): Boolean {
        return password.length >= minLength && password.any { it.isDigit() }
    }
}

fun main() {
    val validator = PasswordValidator(minLength = 8)
    
    // Obyekt nomi bilan to'g'ridan-to'g'ri chaqirish:
    println("12345 yaroqlimi: ${validator("12345")}")
    println("SecurePass99 yaroqlimi: ${validator("SecurePass99")}")
}""",
        "'operator fun invoke' har qanday klass nusxasiga funksiya xususiyatini beradi. Bu ayniqsa Clean Architecture arxitekturasidagi 'UseCase' (Use Case) sinflarida juda keng qo'llaniladi.",
        """12345 yaroqlimi: false
SecurePass99 yaroqlimi: true"""
    ),
    (
        165,
        "Taqqoslash operatorini qayta yuklash: compareTo",
        "Sinf obyektlarini '>', '<', '>=', '<=' operatorlari bilan solishtirish uchun 'Comparable' va 'compareTo' dan foydalaning.",
        """data class Player(val name: String, val score: Int) : Comparable<Player> {
    override operator fun compareTo(other: Player): Int {
        return this.score.compareTo(other.score)
    }
}

fun main() {
    val p1 = Player("Temur", 1500)
    val p2 = Player("Anvar", 1850)
    
    println("Temurning bali Anvarnikidan kattami: ${p1 > p2}")
    println("Anvar kuchliroqmi: ${p2 > p1}")
}""",
        "'compareTo' metodini qayta yuklash orqali barcha solishtirish operatorlari (>, <, >=, <=) avtomatik ravishda ishga tushadi. Bu kodni juda qisqa va tabiiy qiladi.",
        """Temurning bali Anvarnikidan kattami: false
Anvar kuchliroqmi: true"""
    ),
    (
        166,
        "Tenglik va tegishlilik operatorlari: contains (in) operatori",
        "O'z to'plamingiz yoki oraliq sinfingiz uchun 'in' operatorini 'operator fun contains' orqali yarating.",
        """class NumberRange(val min: Int, val max: Int) {
    operator fun contains(value: Int): Boolean {
        return value in min..max
    }
}

fun main() {
    val safeZone = NumberRange(10, 50)
    
    println("25 xavfsiz hududdami: ${25 in safeZone}")
    println("75 xavfsiz hududdami: ${75 in safeZone}")
}""",
        "'operator fun contains' metodini yozish orqali sinf ustida 'in' va '!in' operatorlari to'liq ishlay boshlaydi.",
        """25 xavfsiz hududdami: true
75 xavfsiz hududdami: false"""
    ),
    (
        167,
        "Iteratsiya operatori: iterator yuklash",
        "O'z maxsus sinfingizni 'for' siklida aylanib chiqish imkoniyatini 'operator fun iterator' orqali ta'minlang.",
        """class Sentence(val text: String) {
    operator fun iterator(): Iterator<String> {
        return text.split(" ").iterator()
    }
}

fun main() {
    val quote = Sentence("Har bir kun yangi imkoniyat")
    
    println("Gapdagi so'zlar:")
    for (word in quote) {
        println(" - $word")
    }
}""",
        "Kotlinda 'for (item in obj)' ishlashi uchun 'obj' da 'operator fun iterator(): Iterator<T>' mavjud bo'lishi kifoya. Hech qanday murakkab interfeyslarni meros qilib olish shart emas.",
        """Gapdagi so'zlar:
 - Har
 - bir
 - kun
 - yangi
 - imkoniyat"""
    ),
    (
        168,
        "Unar operatorlar: unaryMinus, not va inc",
        "Koordinatani teskari ishoraga aylantirish uchun '-p' unar minus operatorini yarating.",
        """data class Coordinate(val x: Int, val y: Int) {
    operator fun unaryMinus(): Coordinate = Coordinate(-x, -y)
    operator fun not(): Boolean = (x == 0 && y == 0)
}

fun main() {
    val pt = Coordinate(10, -25)
    val inverted = -pt
    val origin = Coordinate(0, 0)
    
    println("Asl koordinata: $pt")
    println("Teskari ishora: $inverted")
    println("origin nol nuqtadami (!origin): ${!origin}")
}""",
        "'unaryMinus' unar minus (-obj) operatorini, 'not' esa inkor (!obj) operatorini ifodalaydi.",
        """Asl koordinata: Coordinate(x=10, y=-25)
Teskari ishora: Coordinate(x=-10, y=25)
origin nol nuqtadami (!origin): true"""
    ),
    (
        169,
        "Rekursiyada xotirani tejash: Memorizatsiya (Memoization)",
        "Funksiya chaqiruvlari natijalarini keshlab boruvchi yuqori unumdor rekursiv hisoblagich tuzing.",
        """val fibMemo = mutableMapOf<Int, Long>()

fun fibMemoized(n: Int): Long {
    if (n <= 1) return n.toLong()
    return fibMemo.getOrPut(n) {
        fibMemoized(n - 1) + fibMemoized(n - 2)
    }
}

fun main() {
    println("Fib(10) = ${fibMemoized(10)}")
    println("Fib(40) = ${fibMemoized(40)}")
}""",
        "'getOrPut' funksiyasi agar kalit xaritada mavjud bo'lsa uni qaytaradi, aks holda berilgan hisoblashni bajarib keshga yozadi. Bu eksponentsial O(2^N) rekursiyani chiziqli O(N) ga tushiradi.",
        """Fib(10) = 55
Fib(40) = 102334155"""
    ),
    (
        170,
        "Funksiya turlari (Function Types) va parametr sifatida uzatish",
        "Boshqa bir funksiyani argument sifatida qabul qiluvchi va natijani o'zgartiruvchi funksiya yozing.",
        """fun applyOperation(a: Int, b: Int, operation: (Int, Int) -> Int): Int {
    return operation(a, b)
}

fun main() {
    val sum = applyOperation(10, 5) { x, y -> x + y }
    val product = applyOperation(10, 5) { x, y -> x * y }
    
    println("Yig'indi: $sum")
    println("Ko'paytma: $product")
}""",
        "Kotlinda funksiyalar 'birinchi darajali fuqarolar' (First-Class Citizens) hisoblanadi. '(Int, Int) -> Int' funksiya turini ifodalaydi va parametr sifatida erkin uzatiladi.",
        """Yig'indi: 15
Ko'paytma: 50"""
    ),
    (
        171,
        "Funksiyadan funksiya qaytarish (Returning Functions)",
        "Berilgan parametrga ko'ra yangi soliq hisoblagich funksiyasini qaytaruvchi fabrika funksiyasini tuzing.",
        """fun createMultiplier(factor: Double): (Double) -> Double {
    return { value -> value * factor }
}

fun main() {
    val doubleCalculator = createMultiplier(2.0)
    val tripleCalculator = createMultiplier(3.0)
    
    println("15 * 2 = ${doubleCalculator(15.0)}")
    println("15 * 3 = ${tripleCalculator(15.0)}")
}""",
        "Yuqori tartibli funksiyalar (High-Order Functions) nafaqat funksiyani qabul qilishi, balki o'zidan yangi funksiyani qaytarishi ham mumkin.",
        """15 * 2 = 30.0
15 * 3 = 45.0"""
    ),
    (
        172,
        "Funksiya havolasi (Function References) :: operatori",
        "Mavjud oddiy funksiyani '::' operatori orqali yuqori tartibli funksiyaga havola qilib uzating.",
        """fun isEven(n: Int): Boolean = n % 2 == 0

fun main() {
    val numbers = listOf(1, 2, 3, 4, 5, 6, 7, 8)
    
    // Lambda o'rniga funksiya havolasi:
    val evens = numbers.filter(::isEven)
    
    println("Juft sonlar: $evens")
}""",
        "'::functionName' sintaksisi funksiyaning o'ziga havola (reference) beradi. Bu '{ isEven(it) }' lambdasining to'liq va o'qishga juda qulay analogidir.",
        """Juft sonlar: [2, 4, 6, 8]"""
    ),
    (
        173,
        "Konstruktor havolasi (Constructor Reference)",
        "Yangi obyektlar yaratishda '::ClassName' konstruktor havolasidan foydalaning.",
        """data class Person(val name: String)

fun main() {
    val names = listOf("Dilnoza", "Jasur", "Ravshan")
    
    // Har bir nomdan Person obyekti yaratish:
    val people = names.map(::Person)
    
    println("Obyektlar ro'yxati: $people")
}""",
        "'::Person' konstruktorga havola bo'lib, 'Person(name)' chaqiruvini har bir element uchun avtomatik bajaradi.",
        """Obyektlar ro'yxati: [Person(name=Dilnoza), Person(name=Jasur), Person(name=Ravshan)]"""
    ),
    (
        174,
        "Anonim funksiyalar (Anonymous Functions)",
        "Qaytish turini aniq ko'rsatish va mahalliy return xususiyatidan foydalanish uchun anonim funksiya yozing.",
        """fun main() {
    val numbers = listOf(1, 2, 3, 4, 5)
    
    // Anonim funksiya:
    val doubled = numbers.map(fun(item: Int): Int {
        if (item == 3) return 0 // Faqat anonim funksiyadan qaytadi
        return item * 2
    })
    
    println("Natija: $doubled")
}""",
        "Anonim funksiyalarda 'return' so'zi faqat o'sha funksiyadan chiqadi, lambdalardagi kabi butun tashqi funksiyadan chiqib ketish xavfi bo'lmaydi.",
        """Natija: [2, 4, 0, 8, 10]"""
    ),
    (
        175,
        "Kengaytma funksiyalar bilan Infix kombinatsiyasi",
        "Matnlarni birlashtiruvchi shaxsiy infix kengaytma funksiyasini e'lon qiling.",
        """infix fun String.joinedWith(other: String): String {
    return "$this - $other"
}

fun main() {
    val result = "Toshkent" joinedWith "Samarqand"
    println("Marshrut: $result")
}""",
        "Kengaytma funksiyani 'infix' qilish orqali istalgan sinflar ustida chiroyli DSL sintaksisi yaratish mumkin.",
        """Marshrut: Toshkent - Samarqand"""
    ),
    (
        176,
        "Funksiyalarda moslashuvchan konfiguratsiya andozasi",
        "Lambda argumenti orqali parametrlar sozlamasini sozlovchi konfigurator yarating.",
        """class HttpConfig {
    var timeoutMs: Int = 5000
    var retries: Int = 3
    var userAgent: String = "KotlinClient/2.0"
}

fun createHttpClient(init: HttpConfig.() -> Unit): HttpConfig {
    val config = HttpConfig()
    config.init()
    return config
}

fun main() {
    val clientConfig = createHttpClient {
        timeoutMs = 10000
        retries = 5
    }
    
    println("Timeout: ${clientConfig.timeoutMs}ms | Qayta urinish: ${clientConfig.retries} | User-Agent: ${clientConfig.userAgent}")
}""",
        "'HttpConfig.() -> Unit' receiver bilan lambda (lambda with receiver) deb ataladi. U DSL qurishda asosiy vosita bo'lib, blok ichida 'this' orqali to'g'ridan-to'g'ri maydonlarga murojaat qilish imkonini beradi.",
        """Timeout: 10000ms | Qayta urinish: 5 | User-Agent: KotlinClient/2.0"""
    ),
    (
        177,
        "Murakkab rekursiya: Qidiruv daraxtida chuqurlik bo'yicha qidirish (DFS)",
        "Daraxtdagi nishon qiymatni rekursiv topuvchi funksiya yozing.",
        """class SimpleNode(val value: Int, val children: List<SimpleNode> = emptyList())

fun searchTree(root: SimpleNode, target: Int): Boolean {
    if (root.value == target) return true
    for (child in root.children) {
        if (searchTree(child, target)) return true
    }
    return false
}

fun main() {
    val tree = SimpleNode(1, listOf(
        SimpleNode(2),
        SimpleNode(3, listOf(SimpleNode(4), SimpleNode(5)))
    ))
    
    println("4 topildimi: ${searchTree(tree, 4)}")
    println("9 topildimi: ${searchTree(tree, 9)}")
}""",
        "Chuqurlik bo'yicha qidirish (DFS) daraxt strukturalarini rekursiv tahlil qilishda standart algoritm bo'lib, har bir tugun va uning bolalarini ketma-ket tekshiradi.",
        """4 topildimi: true
9 topildimi: false"""
    ),
    (
        178,
        "Funksiyalarda ko'p qaytish qiymati: Triple va Custom Data Class",
        "Bitta funksiyadan bir vaqtning o'zida minimum, maksimum va o'rtacha qiymatni qaytaring.",
        """data class Statistics(val min: Int, val max: Int, val average: Double)

fun calculateStats(numbers: List<Int>): Statistics {
    require(numbers.isNotEmpty()) { "Ro'yxat bo'sh bo'lmasligi kerak" }
    return Statistics(
        min = numbers.minOrNull() ?: 0,
        max = numbers.maxOrNull() ?: 0,
        average = numbers.average()
    )
}

fun main() {
    val data = listOf(14, 28, 5, 92, 47, 33)
    val (min, max, avg) = calculateStats(data)
    
    println("Minimal: $min | Maksimal: $max | O'rtacha: $avg")
}""",
        "Kotlinda bir nechta qiymat qaytarish uchun maxsus 'data class' yoki 'Pair'/'Triple' ishlatiladi va destrukturizatsiya orqali osongina qabul qilinadi.",
        """Minimal: 5 | Maksimal: 92 | O'rtacha: 36.5"""
    ),
    (
        179,
        "Shartli chaqiruv: Funksiyani xavfsiz zanjirlash",
        "Transformatsiya qiluvchi funksiyalarni bitta oqimda ketma-ket ishlatish.",
        """fun normalizeText(input: String): String = input.trim().lowercase()
fun removePunctuation(input: String): String = input.filter { it.isLetterOrDigit() || it.isWhitespace() }
fun capitalizeWords(input: String): String = input.split(" ").joinToString(" ") { it.replaceFirstChar { c -> c.uppercase() } }

fun main() {
    val rawText = "  !!!Assalomu   alaykum, dunyo!  "
    val clean = capitalizeWords(removePunctuation(normalizeText(rawText)))
    println("Tozalangan matn: '$clean'")
}""",
        "Kichik, bitta vazifani bajaruvchi toza funksiyalarni (pure functions) bir-biriga uzatish kodning testlanuvchanligini va modulliligini ta'minlaydi.",
        """Tozalangan matn: 'Assalomu Alaykum Dunyo'"""
    ),
    (
        180,
        "Vararg va Named Argument kombinatsiyasi",
        "Vararg parametridan keyin keluvchi boshqa parametrlarni nomlangan argument sifatida uzatish.",
        """fun renderMenu(vararg items: String, header: String = "MENYU", footer: String = "Tamom") {
    println("=== $header ===")
    for ((index, item) in items.withIndex()) {
        println("${index + 1}. $item")
    }
    println("--- $footer ---")
}

fun main() {
    renderMenu("Osh", "Manti", "Shashlik", header = "MILLIY TAOMLAR", footer = "Yoqimli ishtaha")
}""",
        "Agar funksiyada 'vararg' dan keyin boshqa parametrlar kelsa, ularni faqat nomlangan argument (named argument) sintaksisi orqali uzatish mumkin.",
        """=== MILLIY TAOMLAR ===
1. Osh
2. Manti
3. Shashlik
--- Yoqimli ishtaha ---"""
    ),
    (
        181,
        "Funksiya kompozitsiyasi (Function Composition)",
        "Ikki funksiyani bitta yangi funksiyaga birlashtiruvchi infix kompozitsiya operatorini tuzing.",
        """infix fun <A, B, C> ((B) -> C).compose(other: (A) -> B): (A) -> C {
    return { x -> this(other(x)) }
}

fun main() {
    val multiplyByTwo = { x: Int -> x * 2 }
    val addTen = { x: Int -> x + 10 }
    
    // (x * 2) + 10
    val combined = addTen compose multiplyByTwo
    
    println("Natija (5 * 2 + 10): ${combined(5)}")
}""",
        "Funksiya kompozitsiyasi matematik f(g(x)) prinsipiga asoslanadi va yuqori darajadagi abstraksiyani ta'minlaydi.",
        """Natija (5 * 2 + 10): 20"""
    ),
    (
        182,
        "Rekursiyada oraliq to'xtash shartlari: Akkerman funksiyasi",
        "Chuqur rekursiya va hisoblash chegaralarini tekshiruvchi Akkerman funksiyasini yozing.",
        """fun ackermann(m: Long, n: Long): Long {
    return when {
        m == 0L -> n + 1L
        m > 0L && n == 0L -> ackermann(m - 1L, 1L)
        else -> ackermann(m - 1L, ackermann(m, n - 1L))
    }
}

fun main() {
    println("Ackermann(2, 2) = ${ackermann(2L, 2L)}")
    println("Ackermann(3, 2) = ${ackermann(3L, 2L)}")
}""",
        "Akkerman funksiyasi o'zining tez o'suvchi xarakteri bilan mashhur bo'lib, rekursiya nazariyasida muhim o'rin tutadi.",
        """Ackermann(2, 2) = 7
Ackermann(3, 2) = 29"""
    ),
    (
        183,
        "Amaliy tekshiruvchi: Parol mustahkamligini baholovchi funksiyalar to'plami",
        "Har bir qoidani alohida predikat funksiya sifatida e'lon qilib, parolni baholang.",
        """fun hasMinLength(p: String): Boolean = p.length >= 8
fun hasUppercase(p: String): Boolean = p.any { it.isUpperCase() }
fun hasDigit(p: String): Boolean = p.any { it.isDigit() }
fun hasSpecialChar(p: String): Boolean = p.any { !it.isLetterOrDigit() }

fun evaluatePasswordStrength(password: String): Int {
    val rules = listOf(::hasMinLength, ::hasUppercase, ::hasDigit, ::hasSpecialChar)
    return rules.count { rule -> rule(password) }
}

fun main() {
    println("pass123 bali: ${evaluatePasswordStrength("pass123")}/4")
    println("Pass123! bali: ${evaluatePasswordStrength("Pass123!")}/4")
}""",
        "Predikat funksiyalar ro'yxati 'listOf(::fn1, ::fn2)' orqali barcha qoidalarni bir joyda dinamik tekshirish juda qulay va kengaytiriluvchandir.",
        """pass123 bali: 2/4
Pass123! bali: 4/4"""
    ),
    (
        184,
        "Shartli xatolar bilan: Funksiyada parametrlarni assert qilish",
        "Kutubxona standartidagi 'check()' va 'require()' funksiyalarini parametrlar himoyasida qo'llang.",
        """fun transferFunds(senderBalance: Double, amount: Double) {
    require(amount > 0) { "O'tkazma summasi musbat bo'lishi shart!" }
    check(senderBalance >= amount) { "Balansda yetarli mablag' mavjud emas!" }
    
    println("Muvaffaqiyatli o'tkazildi: $$amount")
}

fun main() {
    transferFunds(100.0, 45.0)
    try {
        transferFunds(50.0, -10.0)
    } catch (e: IllegalArgumentException) {
        println("Xato: ${e.message}")
    }
}""",
        "'require()' noto'g'ri argumentlarda 'IllegalArgumentException', 'check()' esa noto'g'ri holatda 'IllegalStateException' tashlaydi.",
        """Muvaffaqiyatli o'tkazildi: $45.0
Xato: O'tkazma summasi musbat bo'lishi shart!"""
    ),
    (
        185,
        "Kompilyatsiya vaqtidagi konstantalar bilan standart argumentlar",
        "Standart parametr sifatida 'const val' qiymatlarini belgilash.",
        """const val DEFAULT_TIMEOUT = 3000
const val DEFAULT_MAX_RETRIES = 3

fun executeHttpRequest(url: String, timeout: Int = DEFAULT_TIMEOUT, retries: Int = DEFAULT_MAX_RETRIES) {
    println("So'rov: $url | Timeout: ${timeout}ms | Urinishlar: $retries")
}

fun main() {
    executeHttpRequest("https://api.test.uz/data")
}""",
        "Kompilyatsiya konstantalari standart parametrlar sifatida foydalanilganda bayt-kod darajasida to'g'ridan-to'g'ri joylashtiriladi.",
        """So'rov: https://api.test.uz/data | Timeout: 3000ms | Urinishlar: 3"""
    ),
    (
        186,
        "Shartli bajarish: Predikat argumenti bilan qidiruv",
        "Berilgan shartga mos keluvchi birinchi indeksni qaytaruvchi shaxsiy qidiruv funksiyasini yozing.",
        """fun <T> findFirstMatchingIndex(list: List<T>, predicate: (T) -> Boolean): Int {
    for (i in list.indices) {
        if (predicate(list[i])) return i
    }
    return -1
}

fun main() {
    val scores = listOf(45, 60, 85, 92, 55)
    val indexFirstA = findFirstMatchingIndex(scores) { it >= 90 }
    println("90 dan yuqori birinchi ball indeksi: $indexFirstA")
}""",
        "Generik predikat '(T) -> Boolean' ixtiyoriy turdagi kolleksiyalarni bitta moslashuvchan funksiya bilan filtrlash imkonini beradi.",
        """90 dan yuqori birinchi ball indeksi: 3"""
    ),
    (
        187,
        "Rekursiya bilan Palindromni tekshirish",
        "Qatorning palindrom ekanligini quyruq rekursiyasi orqali aniqlang.",
        """tailrec fun isPalindromeRecursive(text: String, start: Int = 0, end: Int = text.length - 1): Boolean {
    if (start >= end) return true
    if (text[start] != text[end]) return false
    return isPalindromeRecursive(text, start + 1, end - 1)
}

fun main() {
    println("madam palindrommi: ${isPalindromeRecursive("madam")}")
    println("kotlin palindrommi: ${isPalindromeRecursive("kotlin")}")
}""",
        "Bosh va oxir ko'rsatkichlarini bir qadamdan surib borish orqali yangi satr obyektlari yaratmasdan xotirani tejash mumkin.",
        """madam palindrommi: true
kotlin palindrommi: false"""
    ),
    (
        188,
        "Funksiyalar va Ko'p o'lchovli matritsalarni ko'paytirish",
        "Ikki matritsani qoidalarga ko'ra ko'paytiruvchi funksiya yozing.",
        """fun multiplyMatrices(a: Array<IntArray>, b: Array<IntArray>): Array<IntArray> {
    val rowsA = a.size
    val colsA = a[0].size
    val colsB = b[0].size
    
    val result = Array(rowsA) { IntArray(colsB) }
    
    for (i in 0 until rowsA) {
        for (j in 0 until colsB) {
            for (k in 0 until colsA) {
                result[i][j] += a[i][k] * b[k][j]
            }
        }
    }
    return result
}

fun main() {
    val m1 = arrayOf(intArrayOf(1, 2), intArrayOf(3, 4))
    val m2 = arrayOf(intArrayOf(2, 0), intArrayOf(1, 2))
    val res = multiplyMatrices(m1, m2)
    
    println("Natijaviy matritsa:")
    for (row in res) {
        println(row.joinToString(" "))
    }
}""",
        "Matritsalarni ko'paytirish chiziqli algebraning asosi bo'lib, uchta ichma-ich sikl orqali hisoblanadi.",
        """Natijaviy matritsa:
4 4
10 8"""
    ),
    (
        189,
        "Funksiyalarda cheksiz argumentlar: Birlashtirish (Merging)",
        "Bir nechta ro'yxatlarni 'vararg' orqali qabul qilib, bitta birlashgan saralangan ro'yxat hosil qiling.",
        """fun mergeSortedLists(vararg lists: List<Int>): List<Int> {
    return lists.flatMap { it }.sorted()
}

fun main() {
    val merged = mergeSortedLists(
        listOf(10, 30, 50),
        listOf(5, 15, 25),
        listOf(1, 100)
    )
    println("Birlashtirilgan ro'yxat: $merged")
}""",
        "'flatMap' har bir kichik ro'yxatni bitta oqimga yoyadi va '.sorted()' yakuniy natijani tartiblaydi.",
        """Birlashtirilgan ro'yxat: [1, 5, 10, 15, 25, 30, 50, 100]"""
    ),
    (
        190,
        "Funksiya bilan Binar qidiruv (Binary Search)",
        "Saralangan massivda logarifmik vaqtda element qidiruvchi rekursiv funksiya yozing.",
        """tailrec fun binarySearch(arr: IntArray, target: Int, low: Int = 0, high: Int = arr.size - 1): Int {
    if (low > high) return -1
    val mid = low + (high - low) / 2
    return when {
        arr[mid] == target -> mid
        arr[mid] > target -> binarySearch(arr, target, low, mid - 1)
        else -> binarySearch(arr, target, mid + 1, high)
    }
}

fun main() {
    val sortedArr = intArrayOf(2, 5, 8, 12, 16, 23, 38, 56, 72, 91)
    val index = binarySearch(sortedArr, 23)
    println("23 soni indeksi: $index")
}""",
        "Binar qidiruv har qadamda qidiruv maydonini ikkiga bo'ladi. 'tailrec' tufayli u O(log N) vaqtda va qo'shimcha steksiz ishlaydi.",
        """23 soni indeksi: 5"""
    ),
    (
        191,
        "Shartli logika: Funksiyani xatodan himoyalangan o'rash",
        "Funksiya bajarilish vaqtini (execution time) o'lchovchi yuqori tartibli o'lchov funksiyasi tuzing.",
        """fun <T> measureExecutionTime(taskName: String, block: () -> T): T {
    val startTime = System.currentTimeMillis()
    val result = block()
    val endTime = System.currentTimeMillis()
    println("[$taskName] bajarildi: ${endTime - startTime} ms")
    return result
}

fun main() {
    val sum = measureExecutionTime("Millionlik hisob") {
        (1..1_000_000).map { it.toLong() }.sum()
    }
    println("Yig'indi natijasi: $sum")
}""",
        "Yuqori tartibli o'lchov funksiyalari orqali profiling, logging va tranzaksiya o'ramlari juda qulay tashkil etiladi.",
        """[Millionlik hisob] bajarildi: 35 ms
Yig'indi natijasi: 500000500000"""
    ),
    (
        192,
        "Funksiyalarda yashirin konvertatsiya: Infix bilan juftlik hosil qilish",
        "Kotlindaki 'to' operatori kabi o'z shaxsiy 'bogla' infix funksiyangizni yozing.",
        """infix fun <A, B> A.bogla(that: B): Pair<A, B> = Pair(this, that)

fun main() {
    val pair1 = "O'zbekiston" bogla "Toshkent"
    val pair2 = "Fransiya" bogla "Parij"
    
    println("Juftlik 1: $pair1")
    println("Juftlik 2: $pair2")
}""",
        "Kotlindagi mashhur 'mapOf(\"A\" to 1)' sintaksisi aynan shu ko'rinishdagi standart 'public infix fun <A, B> A.to(that: B): Pair<A, B>' kengaytmasi asosida ishlaydi.",
        """Juftlik 1: (O'zbekiston, Toshkent)
Juftlik 2: (Fransiya, Parij)"""
    ),
    (
        193,
        "Funksiyalarda xavfsiz qiymat olish: runCatching bilan o'rash",
        "Stringni Double songa o'tkazuvchi va xato bo'lsa standart zaxirani qaytaruvchi bitta qatorli funksiya yozing.",
        """fun parseAmountOrDefault(raw: String, defaultAmount: Double = 0.0): Double {
    return runCatching { raw.toDouble() }.getOrDefault(defaultAmount)
}

fun main() {
    println("Yaroqli: " + parseAmountOrDefault("150.75"))
    println("Yaroqsiz: " + parseAmountOrDefault("not_a_number", 10.0))
}""",
        "'runCatching { ... }.getOrDefault(...)' ifodasi xatoliklar yuz berishi mumkin bo'lgan konvertatsiyalarda klassik try-catch bloklarini qisqartiradi.",
        """Yaroqli: 150.75
Yaroqsiz: 10.0"""
    ),
    (
        194,
        "Matematik qatorlar yig'indisini hisoblash",
        "Eyler sonini (e = 1/0! + 1/1! + 1/2! + ...) N ta hadgacha rekursiv hisoblovchi funksiya yozing.",
        """fun calculateEulerConstant(terms: Int): Double {
    var e = 0.0
    var factorial = 1.0
    for (i in 0 until terms) {
        if (i > 0) factorial *= i
        e += 1.0 / factorial
    }
    return e
}

fun main() {
    println("Eyler soni (10 had): ${calculateEulerConstant(10)}")
    println("Haqiqiy Math.E:     ${Math.E}")
}""",
        "Matematik qatorlarni hisoblashda oldingi qadam faktorialini keshlab borish har safar boshidan hisoblashning oldini oladi.",
        """Eyler soni (10 had): 2.7182815255731922
Haqiqiy Math.E:     2.718281828459045"""
    ),
    (
        195,
        "Funksiya bilan satrlarni shifrlash (Sezar shifri)",
        "Matndagi harflarni K qadamga surib shifrlaydigan funksiya tuzing.",
        """fun caesarCipher(text: String, shift: Int): String {
    val k = shift % 26
    return text.map { ch ->
        when (ch) {
            in 'a'..'z' -> 'a' + (ch - 'a' + k) % 26
            in 'A'..'Z' -> 'A' + (ch - 'A' + k) % 26
            else -> ch
        }
    }.joinToString("")
}

fun main() {
    val encrypted = caesarCipher("Hello Kotlin 2026", 3)
    val decrypted = caesarCipher(encrypted, 26 - 3)
    
    println("Shifrlangan: $encrypted")
    println("Asliga qaytarilgan: $decrypted")
}""",
        "Belgilar arifmetikasi va qoldiq moduli (%) shifrlash va matnlarni kodlashda qulay va xatosiz ishlaydi.",
        """Shifrlangan: Khoor Nrwolq 2026
Asliga qaytarilgan: Hello Kotlin 2026"""
    ),
    (
        196,
        "Funksiyalarda dinamik SQL parametrlarini shakllantirish",
        "Vararg va named argumentlar orqali dinamik SELECT so'rovi generatsiya qiluvchi funksiya tuzing.",
        """fun buildSelectQuery(table: String, vararg columns: String, whereClause: String? = null): String {
    val cols = if (columns.isNotEmpty()) columns.joinToString(", ") else "*"
    val base = "SELECT $cols FROM $table"
    return if (whereClause != null) "$base WHERE $whereClause" else base
}

fun main() {
    println(buildSelectQuery("users"))
    println(buildSelectQuery("products", "id", "name", "price", whereClause = "price > 100"))
}""",
        "Moslashuvchan standart parametrlar va 'vararg' orqali dastur ichida qulay va ixcham Query Builder vositalarini yaratish mumkin.",
        """SELECT * FROM users
SELECT id, name, price FROM products WHERE price > 100"""
    ),
    (
        197,
        "Amaliy Kesh Decoratori: Funksiyalarni xotira bilan kengaytirish",
        "Ixtiyoriy bitta parametrli qimmat hisoblash funksiyasini avtomatik xotirada saqlovchi o'ram (memoizer) yozing.",
        """fun <P, R> memoize(fn: (P) -> R): (P) -> R {
    val cache = mutableMapOf<P, R>()
    return { param: P ->
        cache.getOrPut(param) {
            println("[KESH YOZILMOQDA]: Parametr=$param")
            fn(param)
        }
    }
}

fun main() {
    val heavySquare = memoize<Int, Int> { it * it }
    
    println("Natija 1: " + heavySquare(10))
    println("Natija 2: " + heavySquare(10)) // Keshdan olinadi
}""",
        "Yuqori tartibli generik 'memoize' funksiyasi funksional dasturlashning eng kuchli andozalaridan bo'lib, ixtiyoriy hisoblashni keshlay oladi.",
        """[KESH YOZILMOQDA]: Parametr=10
Natija 1: 100
Natija 2: 100"""
    ),
    (
        198,
        "Funksiyalarda qayta urinish (Retry Mechanism)",
        "Xatolik yuz berganda operatsiyani berilgan urinishlar sonicha takrorlovchi funksiya yozing.",
        """fun <T> retry(maxAttempts: Int = 3, block: () -> T): T {
    var lastException: Exception? = null
    for (attempt in 1..maxAttempts) {
        try {
            return block()
        } catch (e: Exception) {
            lastException = e
            println("Urinish #$attempt muvaffaqiyatsiz bo'ldi: ${e.message}")
        }
    }
    throw lastException ?: IllegalStateException("Noma'lum xatolik")
}

fun main() {
    var failCount = 2
    val result = retry(maxAttempts = 3) {
        if (failCount > 0) {
            failCount--
            throw RuntimeException("Aloqa uzildi")
        }
        "Tarmoq muvaffaqiyatli ulandi!"
    }
    println("Yakuniy natija: $result")
}""",
        "Tarmoq so'rovlari va beqaror tashqi servislarga ulanishda 'retry' andozasi dastur barqarorligini ta'minlashning asosiy vositasidir.",
        """Urinish #1 muvaffaqiyatsiz bo'ldi: Aloqa uzildi
Urinish #2 muvaffaqiyatsiz bo'ldi: Aloqa uzildi
Yakuniy natija: Tarmoq muvaffaqiyatli ulandi!"""
    ),
    (
        199,
        "Shartli Pipeline: Funksional ma'lumotlar quvuri (Data Pipeline)",
        "Matnni bosqichma-bosqich o'zgartiruvchi transformatsiyalar zanjirini yarating.",
        """fun applyPipeline(initialText: String, vararg transformers: (String) -> String): String {
    var result = initialText
    for (t in transformers) {
        result = t(result)
    }
    return result
}

fun main() {
    val output = applyPipeline(
        "   Salom Kotlin 2026!  ",
        { it.trim() },
        { it.uppercase() },
        { it.replace("2026", "2.0") }
    )
    println("Pipeline natijasi: '$output'")
}""",
        "Vararg funksiyalar ro'yxati orqali ma'lumotlarni bosqichma-bosqich tozalash va o'zgartirish (Pipeline/ETL) juda sodda va o'qishli amalga oshiriladi.",
        """Pipeline natijasi: 'SALOM KOTLIN 2.0!'"""
    ),
    (
        200,
        "Funksiyalar bo'yicha to'liq amaliy xulosa: Buyurtma hisoblagich tizimi",
        "Standart parametrlar, nomlangan argumentlar, varargs, infix va single-expression funksiyalarni bitta yaxlit tizimda birlashtiring.",
        """data class CartItem(val name: String, val price: Double, val quantity: Int)

fun createItem(name: String, price: Double, qty: Int = 1): CartItem = CartItem(name, price, qty)

infix fun CartItem.withDiscount(discountPercent: Double): CartItem {
    val newPrice = this.price * (1 - discountPercent / 100.0)
    return this.copy(price = newPrice)
}

fun checkoutOrder(client: String, vararg items: CartItem, deliveryCost: Double = 20.0): String {
    val subtotal = items.sumOf { it.price * it.quantity }
    val total = subtotal + deliveryCost
    
    val itemsList = items.joinToString("\n") { " - ${it.name} (${it.quantity} dona) x $$it.price" }
    
    return \"\"\"
        ==============================
        BUYURTMA CHEKI
        Mijoz: $client
        ------------------------------
        Mahsulotlar:
        $itemsList
        ------------------------------
        Oraliq summa: $$subtotal
        Yetkazib berish: $$deliveryCost
        JAMI TO'LOV: $$total
        ==============================
    \"\"\".trimIndent()
}

fun main() {
    val item1 = createItem("Noutbuk", 1000.0) withDiscount 10.0 // 900.0
    val item2 = createItem("Sichqoncha", 30.0, qty = 2)
    val item3 = createItem("Klaviatura", 70.0)
    
    val receipt = checkoutOrder(
        client = "Alisher Zokirov",
        item1, item2, item3,
        deliveryCost = 15.0
    )
    
    println(receipt)
}""",
        "Ushbu yakuniy topshiriqda talab qilingan barcha funksional mexanizmlar (Default arguments, Named arguments, Varargs, Single-expression, Infix) professional buyurtma cheki misolida birlashtirildi.",
        """==============================
BUYURTMA CHEKI
Mijoz: Alisher Zokirov
------------------------------
Mahsulotlar:
 - Noutbuk (1 dona) x $900.0
 - Sichqoncha (2 dona) x $30.0
 - Klaviatura (1 dona) x $70.0
------------------------------
Oraliq summa: $1030.0
Yetkazib berish: $15.0
JAMI TO'LOV: $1045.0
=============================="""
    )
]

for item in data_04:
    n, title, condition, sol, exp, res = item
    tasks.append(format_task(n, title, condition, sol, exp, res))

save_file("kotlin_04_funksiyalar_va_standart_argumentlar.md", tasks)
