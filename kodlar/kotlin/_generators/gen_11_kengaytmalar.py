# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

data_11 = [
    (
        501,
        "Kengaytma funksiya (Extension Function) asoslari",
        "Mavjud 'String' sinfiga o'zgartirish kiritmasdan, satrning birinchi harfini katta qiluvchi kengaytma funksiya yozing.",
        """fun String.capitalizeWords(): String {
    return this.split(" ").joinToString(" ") { word ->
        word.replaceFirstChar { if (it.isLowerCase()) it.titlecase() else it.toString() }
    }
}

fun main() {
    val title = "kotlin dasturlash tili"
    // To'g'ridan-to'g'ri String metodidek chaqiriladi:
    val formatted = title.capitalizeWords()
    println("Natija: $formatted")
}""",
        "Kotlinda 'ReceiverType.funName()' sintaksisi orqali uchinchi tomon kutubxonalari yoki standart sinflarga (String, List va h.k.) meros olmasdan yangi metodlar qo'shish mumkin. Funksiya ichida 'this' kengaytirilayotgan obyektni (receiver) ifodalaydi.",
        """Natija: Kotlin Dasturlash Tili"""
    ),
    (
        502,
        "Kengaytma xususiyatlar (Extension Properties)",
        "Satrning oxirgi belgisini va uning o'rtacha indeksini hisoblab beruvchi kengaytma xususiyatlarini e'lon qiling.",
        """val String.lastChar: Char?
    get() = if (isNotEmpty()) this[length - 1] else null

val String.middleIndex: Int
    get() = length / 2

fun main() {
    val word = "Samarqand"
    println("Oxirgi belgi: ${word.lastChar}")
    println("O'rtacha indeks: ${word.middleIndex} (Belgi: '${word[word.middleIndex]}')")
}""",
        "Kengaytma xususiyatlar xotirada maydon (backing field) saqlamaydi, shuning uchun ularda boshlang'ich qiymat biriktirib bo'lmaydi. Ular faqat maxsus 'get()' (va agar var bo'lsa 'set()') orqali amalga oshiriladi.",
        """Oxirgi belgi: d
O'rtacha indeks: 4 (Belgi: 'r')"""
    ),
    (
        503,
        "Nullable Receiver bilan kengaytmalar: String?.orEmpty() analogi",
        "Obyekt 'null' bo'lganda ham xavfsiz chaqirilishi mumkin bo'lgan shaxsiy kengaytma funksiya tuzing.",
        """fun String?.safeDefault(defaultVal: String): String {
    // this null bo'lishi mumkin!
    return if (this == null || this.isBlank()) defaultVal else this
}

fun main() {
    val str1: String? = "Haqiqiy ma'lumot"
    val str2: String? = "   "
    val str3: String? = null

    // Safe call (?.) siz to'g'ridan-to'g'ri nuqta bilan chaqiriladi:
    println("str1: ${str1.safeDefault("Standart")}")
    println("str2: ${str2.safeDefault("Standart")}")
    println("str3: ${str3.safeDefault("Standart")}")
}""",
        "Receiver turi 'String?' kabi nullable bo'lsa, funksiya obyekt null bo'lganda ham xatosiz chaqiriladi. Funksiya tanasida 'this == null' tekshiruvi o'tkaziladi. Bu foydalanuvchiga '?.' operatorisiz kod yozish qulayligini beradi.",
        """str1: Haqiqiy ma'lumot
str2: Standart
str3: Standart"""
    ),
    (
        504,
        "Statik bog'lanish (Static Resolution): Polimorfizm yo'qligi",
        "Kengaytma funksiyalar polimorfik emas, balki e'lon qilingan statik tur bo'yicha kompilyatsiya qilinishini namoyish eting.",
        """open class Shape
class Circle : Shape()

fun Shape.getName() = "Shakl (Shape)"
fun Circle.getName() = "Doira (Circle)"

fun printShapeName(s: Shape) {
    // s ning ish vaqtidagi turi Circle bo'lsa ham, Shape.getName chaqiriladi!
    println(s.getName())
}

fun main() {
    val myCircle: Shape = Circle()
    printShapeName(myCircle)
}""",
        "Kengaytma funksiyalar sinf ichiga yangi a'zo kiritmaydi, balki statik Java metodiga aylanadi ('FileNameKt.getName(shape)'). Shu sababli, virtual metodlardan farqli o'laroq, kengaytma funksiyalar ish vaqtidagi (runtime) obyektga emas, o'zgaruvchining e'lon qilingan statik tipiga qarab chaqiriladi.",
        """Shakl (Shape)"""
    ),
    (
        505,
        "Sinf a'zosi va Kengaytma to'qnashuvi: A'zo har doim ustun",
        "Agar kengaytma funksiya sinfdagi mavjud a'zo metod bilan bir xil nom va signaturaga ega bo'lsa nima sodir bo'lishini ko'rsating.",
        """class ExampleClass {
    fun printMessage() {
        println("Sinfning o'z a'zo metodi (Member function)")
    }
}

// Bir xil signaturadagi kengaytma:
fun ExampleClass.printMessage() {
    println("Kengaytma metodi (Extension)")
}

fun main() {
    val ex = ExampleClass()
    ex.printMessage() // Sinf a'zosi chaqiriladi!
}""",
        "Kotlinda qat'iy qoida mavjud: Agar kengaytma funksiya va a'zo funksiyaning nomi va parametrlari bir xil bo'lsa, kompilyator doimo sinf a'zosi foydasiga qaror qiladi (Member always wins). Kengaytma chaqirilmaydi va ogohlantirish beriladi.",
        """Sinfning o'z a'zo metodi (Member function)"""
    ),
    (
        506,
        "Generik kengaytma funksiyalar (Generic Extensions)",
        "Ixtiyoriy turdagi ro'yxatning o'rtasidagi elementni oluvchi generik kengaytma tuzing.",
        """fun <T> List<T>.middleOrNull(): T? {
    if (isEmpty()) return null
    return this[size / 2]
}

fun main() {
    val numbers = listOf(10, 20, 30, 40, 50)
    val names = listOf("Ali", "Vali", "G'ani")

    println("Sonlar o'rtasi: ${numbers.middleOrNull()}")
    println("Ismlar o'rtasi: ${names.middleOrNull()}")
    println("Bo'sh ro'yxat: ${emptyList<Int>().middleOrNull()}")
}""",
        "'fun <T> List<T>.method()' sintaksisi orqali ixtiyoriy turdagi kolleksiyalarga umumiy yordamchi funksiyalar qo'shish mumkin.",
        """Sonlar o'rtasi: 30
Ismlar o'rtasi: Vali
Bo'sh ro'yxat: null"""
    ),
    (
        507,
        "Kengaytmalar bilan Operatorlarni qayta yuklash",
        "Mavjud sinflar ustida arifmetik operatorlarni (masalan String * Int) kengaytma orqali yarating.",
        """operator fun String.times(n: Int): String {
    return this.repeat(n.coerceAtLeast(0))
}

fun main() {
    val dash = "-" * 20
    val star = "* " * 5

    println(dash)
    println(star)
    println("Kotlin " * 3)
}""",
        "'operator fun Receiver.plus/times' kabi kengaytmalar orqali istalgan mavjud sinflar ustida Kotlin operatorlarini yuklash mumkin.",
        """--------------------
* * * * * 
Kotlin Kotlin Kotlin """
    ),
    (
        508,
        "Infix Kengaytma Funksiyalar",
        "Matn boshqa matn bilan tugashini tekshiruvchi chiroyli 'infix' kengaytma yozing.",
        """infix fun String.hasExtension(ext: String): Boolean {
    return this.endsWith(".$ext", ignoreCase = true)
}

fun main() {
    val file1 = "report.pdf"
    val file2 = "archive.ZIP"

    println("file1 PDF mi: ${file1 hasExtension "pdf"}")
    println("file2 ZIP mi: ${file2 hasExtension "zip"}")
    println("file1 PNG mi: ${file1 hasExtension "png"}")
}""",
        "'infix fun Receiver.method(arg)' sintaksisi orqali tabiiy tilga yaqin, qavslarsiz va nuqtasiz chaqiriladigan kengaytmalar yoziladi.",
        """file1 PDF mi: true
file2 ZIP mi: true
file1 PNG mi: false"""
    ),
    (
        509,
        "Sinf ichida e'lon qilingan Kengaytmalar (Member Extensions)",
        "Boshqa bir sinf ichida e'lon qilingan va faqat shu sinf kontekstida ko'rinadigan kengaytmani tushuntiring.",
        """class HttpHeader(val name: String, val value: String)

class HttpResponse {
    // HttpResponse ichida e'lon qilingan kengaytma:
    fun HttpHeader.format(): String {
        return "$name: $value (Response ichida formatlandi)"
    }

    fun render(header: HttpHeader) {
        println(header.format()) // Faqat shu sinf ichida ishlaydi
    }
}

fun main() {
    val header = HttpHeader("Content-Type", "application/json")
    val response = HttpResponse()
    response.render(header)
    
    // header.format() // Tashqaridan chaqirib bo'lmaydi!
}""",
        "Sinf ichida e'lon qilingan kengaytma ikkita receiver ga ega bo'ladi: Dispatch Receiver (tashqi sinf 'HttpResponse') va Extension Receiver ('HttpHeader'). U tashqi dunyodan himoyalangan bo'ladi.",
        """Content-Type: application/json (Response ichida formatlandi)"""
    ),
    (
        510,
        "Sonlar ustida Kengaytma Xususiyatlar: Vaqt oraliqlari DSL",
        "Int sonlariga '.seconds', '.minutes', '.hours' kengaytmalarini qo'shib millisekundlarga o'tkazing.",
        """val Int.seconds: Long
    get() = this * 1000L

val Int.minutes: Long
    get() = this.seconds * 60L

val Int.hours: Long
    get() = this.minutes * 60L

fun main() {
    val timeout = 5.seconds
    val syncInterval = 2.minutes
    val sessionTtl = 1.hours

    println("5 sekund: $timeout ms")
    println("2 daqiqa: $syncInterval ms")
    println("1 soat: $sessionTtl ms")
}""",
        "Primitiv turlar ustidagi kengaytma xususiyatlar juda chiroyli va o'qishli vaqt hamda hajm DSL larini tuzishga imkon beradi.",
        """5 sekund: 5000 ms
2 daqiqa: 120000 ms
1 soat: 3600000 ms"""
    ),
    (
        511,
        "Valyuta summasini chiroyli formatlovchi Double kengaytmasi",
        "Ixtiyoriy son ustida chaqiriladigan '.toFormattedUzs()' kengaytmasini yozing.",
        """fun Double.toFormattedUzs(): String {
    return String.format("%,.2f UZS", this)
}

fun main() {
    val balance = 12543000.75
    val fee = 5000.0
    
    println("Balans: ${balance.toFormattedUzs()}")
    println("Komissiya: ${fee.toFormattedUzs()}")
}""",
        "Double turiga moliyaviy formatlash kengaytmasini berish orqali barcha hisob-kitob sahifalarida kod takrorlanishining oldi olinadi.",
        """Balans: 12,543,000.75 UZS
Komissiya: 5,000.00 UZS"""
    ),
    (
        512,
        "Kolleksiyalarda xavfsiz indekslash: getOrDefaultOrNull",
        "List ustida chegaradan chiqib ketish xavfini yo'qotuvchi shaxsiy kengaytma funksiya tuzing.",
        """fun <T> List<T>.secondOr(default: T): T {
    return if (size >= 2) this[1] else default
}

fun main() {
    val fullList = listOf("A", "B", "C")
    val shortList = listOf("X")

    println("fullList ikkinchisi: ${fullList.secondOr("STANDART")}")
    println("shortList ikkinchisi: ${shortList.secondOr("STANDART")}")
}""",
        "Generik ro'yxat kengaytmasi orqali xavfsiz biznes qoidalari o'rnatiladi.",
        """fullList ikkinchisi: B
shortList ikkinchisi: STANDART"""
    ),
    (
        513,
        "Matndan raqamlarni ajratib oluvchi String kengaytmasi",
        "Satrdan barcha begona belgilarni olib tashlab faqat raqamlarini qaytaruvchi metod yozing.",
        """fun String.onlyDigits(): String {
    return this.filter { it.isDigit() }
}

fun main() {
    val phone = "+998 (90) 123-45-67"
    val card = "8600 1234 5678 9900"

    println("Tozalangan telefon: ${phone.onlyDigits()}")
    println("Tozalangan karta: ${card.onlyDigits()}")
}""",
        "Foydalanuvchi kiritgan telefon va karta raqamlarini tozalashda bunday String kengaytmasi loyiha bo'ylab juda faol ishlatiladi.",
        """Tozalangan telefon: 998901234567
Tozalangan karta: 8600123456789900"""
    ),
    (
        514,
        "Generik Cheklovli Kengaytma (Extension with Generic Constraints)",
        "Faqat raqamli (Number) ro'yxatlar ustida ishlovchi kvadratlar yig'indisi kengaytmasini yozing.",
        """fun <T : Number> Iterable<T>.sumOfSquares(): Double {
    var sum = 0.0
    for (element in this) {
        val v = element.toDouble()
        sum += v * v
    }
    return sum
}

fun main() {
    val intList = listOf(1, 2, 3)
    val doubleList = listOf(1.5, 2.5)

    println("Int lar kvadratlari yig'indisi (1+4+9): ${intList.sumOfSquares()}")
    println("Double lar kvadratlari yig'indisi: ${doubleList.sumOfSquares()}")
}""",
        "'<T : Number>' yuqori chegarasi orqali kengaytma faqat sonli kolleksiyalar uchun ochiladi, masalan List<String> ustida bu metod chaqirilmaydi.",
        """Int lar kvadratlari yig'indisi (1+4+9): 14.0
Double lar kvadratlari yig'indisi: 8.5"""
    ),
    (
        515,
        "Shaxsiy 'chunked' kengaytmasini yozish",
        "Ro'yxatni berilgan hajmda kichik guruhlarga bo'luvchi qulay kengaytma tuzing.",
        """fun <T> List<T>.splitIntoBatches(batchSize: Int): List<List<T>> {
    require(batchSize > 0) { "Paket hajmi musbat bo'lishi kerak" }
    val batches = mutableListOf<List<T>>()
    for (i in indices step batchSize) {
        val end = (i + batchSize).coerceAtMost(size)
        batches.add(subList(i, end))
    }
    return batches
}

fun main() {
    val items = listOf(1, 2, 3, 4, 5, 6, 7, 8)
    val batched = items.splitIntoBatches(3)
    println("3 tadan guruhlar: $batched")
}""",
        "Katta massivlarni ommaviy yuklash (Batch processing) uchun shaxsiy kengaytma funksiyasi.",
        """3 tadan guruhlar: [[1, 2, 3], [4, 5, 6], [7, 8]]"""
    ),
    (
        516,
        "Sana formati kengaytmasi (LocalDate extension)",
        "Java LocalDate obyektiga o'zbekcha sana formatini beruvchi kengaytma qo'shing.",
        """import java.time.LocalDate
import java.time.format.DateTimeFormatter

fun LocalDate.toUzbekString(): String {
    val formatter = DateTimeFormatter.ofPattern("dd-MMMM, yyyy")
    return this.format(formatter)
}

fun main() {
    val date = LocalDate.of(2026, 11, 8)
    println("Formatlangan sana: ${date.toUzbekString()}")
}""",
        "Tashqi kutubxona sinflarini (masalan java.time) o'zgartirmasdan loyihaga mos formatlash kengaytmalari qo'shiladi.",
        """Formatlangan sana: 08-November, 2026"""
    ),
    (
        517,
        "Matnni xavfsiz kesish: truncate kengaytmasi",
        "Satr berilgan uzunlikdan oshsa oxiriga '...' qo'yib kesuvchi String kengaytmasi.",
        """fun String.truncate(maxLength: Int): String {
    return if (length <= maxLength) this else take(maxLength) + "..."
}

fun main() {
    val shortText = "Salom"
    val longText = "Kotlin dasturlash tili zamonaviy ilovalarni tez va sifatli yaratadi"

    println(shortText.truncate(15))
    println(longText.truncate(15))
}""",
        "UI da kartalar va sarlavhalarni chegaralangan uzunlikda ko'rsatishda juda mashhur kengaytma.",
        """Salom
Kotlin dasturla..."""
    ),
    (
        518,
        "Kengaytma bilan Obyektni JSON matniga o'girish",
        "Map ustida '.toJsonString()' kengaytmasini amalga oshirish.",
        """fun Map<String, Any?>.toJsonString(): String {
    val pairs = entries.joinToString(",") { (k, v) ->
        val formattedVal = if (v is String) "\\"v\\"" else "$v"
        "\\"$k\\":$formattedVal"
    }
    return "{$pairs}"
}

fun main() {
    val data = mapOf("id" to 101, "role" to "admin")
    println(data.toJsonString())
}""",
        "Map larni JSON ko'rinishida formatlash kengaytmasi.",
        """{"id":101,"role":"admin"}"""
    ),
    (
        519,
        "Baytlardan KB, MB, GB ga o'tkazuvchi Long kengaytmasi",
        "Long soniga '.toReadableSize()' kengaytmasini berish.",
        """fun Long.toReadableSize(): String {
    val kb = this / 1024.0
    val mb = kb / 1024.0
    val gb = mb / 1024.0
    return when {
        gb >= 1.0 -> "%.2f GB".format(gb)
        mb >= 1.0 -> "%.2f MB".format(mb)
        kb >= 1.0 -> "%.2f KB".format(kb)
        else -> "$this B"
    }
}

fun main() {
    println(512L.toReadableSize())
    println(10485760L.toReadableSize())
    println(21474836480L.toReadableSize())
}""",
        "Fayl va xotira hajmlarini foydalanuvchiga tushunarli matnga o'tkazuvchi kengaytma.",
        """512 B
10.00 MB
20.00 GB"""
    ),
    (
        520,
        "Shaxsiy 'swap' massiv kengaytmasi",
        "IntArray ustida ikki indeksdagi elementlar o'rnini almashtiruvchi kengaytma yozing.",
        """fun IntArray.swap(i: Int, j: Int) {
    val temp = this[i]
    this[i] = this[j]
    this[j] = temp
}

fun main() {
    val arr = intArrayOf(10, 20, 30)
    arr.swap(0, 2)
    println("Almashtirilgandan so'ng: ${arr.joinToString()}")
}""",
        "Algoritmik masalalarda (saralash) massiv kengaytmasi kodni ancha toza qiladi.",
        """Almashtirilgandan so'ng: 30, 20, 10"""
    ),
    (
        521,
        "Kengaytma yordamida URL parametrlarini qo'shish",
        "String URL ga yangi query parametr qo'shuvchi zanjirli kengaytma.",
        """fun String.addQueryParam(key: String, value: String): String {
    val separator = if (contains("?")) "&" else "?"
    return "$this$separator$key=$value"
}

fun main() {
    val url = "https://api.test.uz/search"
        .addQueryParam("q", "kotlin")
        .addQueryParam("page", "1")

    println("Yakuniy URL: $url")
}""",
        "Matnlarni zanjirli boyitish orqali tarmoq so'rovlarini shakllantirish.",
        """Yakuniy URL: https://api.test.uz/search?q=kotlin&page=1"""
    ),
    (
        522,
        "Kengaytma xususiyat bilan Doira perimetri",
        "Doira sinfiga tashqaridan '.circumference' xususiyatini qo'shing.",
        """class Circle(val radius: Double)

val Circle.circumference: Double
    get() = 2 * Math.PI * radius

fun main() {
    val c = Circle(5.0)
    println("Doira aylanasi uzunligi: %.2f".format(c.circumference))
}""",
        "Mavjud geometrik modellarga tashqi hisoblanuvchi xususiyatlar biriktirish.",
        """Doira aylanasi uzunligi: 31.42"""
    ),
    (
        523,
        "Email validatsiya kengaytmasi",
        "String ustida '.isValidEmail()' tekshiruvini amalga oshiring.",
        """fun String.isValidEmail(): Boolean {
    val regex = "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\\\.[A-Za-z]{2,}\$".toRegex()
    return this.matches(regex)
}

fun main() {
    println("test@mail.uz yaroqlimi: ${"test@mail.uz".isValidEmail()}")
    println("not_email yaroqlimi: ${"not_email".isValidEmail()}")
}""",
        "Regulyar ifodalar (Regex) asosida String ga forma validatsiya xususiyatini berish.",
        """test@mail.uz yaroqlimi: true
not_email yaroqlimi: false"""
    ),
    (
        524,
        "Kolleksiyadagi elementlarni almashtirish: replaceIf kengaytmasi",
        "Shartga mos kelgan elementlarni yangi qiymat bilan almashtiruvchi kengaytma tuzing.",
        """fun <T> List<T>.replaceIf(predicate: (T) -> Boolean, replacement: T): List<T> {
    return map { if (predicate(it)) replacement else it }
}

fun main() {
    val numbers = listOf(1, -2, 3, -4, 5)
    val nonNegative = numbers.replaceIf({ it < 0 }, 0)
    println("Manfiylar 0 ga almashtirildi: $nonNegative")
}""",
        "Immutability saqlagan holda ro'yxat elementlarini shartli almashtiruvchi generik kengaytma.",
        """Manfiylar 0 ga almashtirildi: [1, 0, 3, 0, 5]"""
    ),
    (
        525,
        "Char ustida kengaytma: Unli harf ekanligini tekshirish",
        "Belgi unli harf ekanligini aniqlovchi '.isVowel()' kengaytmasini yozing.",
        """fun Char.isVowel(): Boolean {
    return this.lowercaseChar() in listOf('a', 'e', 'i', 'o', 'u', 'o', 'e')
}

fun main() {
    println("'A' unlimi: ${'A'.isVowel()}")
    println("'b' unlimi: ${'b'.isVowel()}")
}""",
        "Primitiv Char turi ustida fonetik tahlil kengaytmasi.",
        """'A' unlimi: true
'b' unlimi: false"""
    ),
    (
        526,
        "Kengaytma bilan O'lchov birliklari konvertatsiyasi: Masofalar",
        "Metrlarni kilometr, santimetr va millimetrga o'tkazuvchi Double kengaytmalari.",
        """val Double.km: Double get() = this / 1000.0
val Double.cm: Double get() = this * 100.0
val Double.mm: Double get() = this * 1000.0

fun main() {
    val distanceM = 2500.0
    println("$distanceM m = ${distanceM.km} km")
    println("1.5 m = ${1.5.cm} cm")
}""",
        "O'lchov birliklarini ifodalovchi toza kengaytma xususiyatlari.",
        """2500.0 m = 2.5 km
1.5 m = 150.0 cm"""
    ),
    (
        527,
        "Nullable kolleksiyani xavfsiz tozalash: orEmptyList kengaytmasi",
        "Nullable List bo'sh bo'lganda 'emptyList()' qaytaruvchi kengaytma.",
        """fun <T> List<T>?.orEmptyCustom(): List<T> {
    return this ?: emptyList()
}

fun main() {
    val nullList: List<String>? = null
    val safeList = nullList.orEmptyCustom()
    println("Xavfsiz ro'yxat o'lchami: ${safeList.size}")
}""",
        "Standart kutubxonadagi 'orEmpty()' analogini o'rganish.",
        """Xavfsiz ro'yxat o'lchami: 0"""
    ),
    (
        528,
        "Stringni shifrlash va deshifrlash kengaytmalari (Base64)",
        "Satr ustida to'g'ridan-to'g'ri '.encodeBase64()' va '.decodeBase64()' chaqirish.",
        """import java.util.Base64

fun String.encodeBase64(): String = Base64.getEncoder().encodeToString(this.toByteArray())
fun String.decodeBase64(): String = String(Base64.getDecoder().decode(this))

fun main() {
    val original = "Maxfiy Token 2026"
    val encoded = original.encodeBase64()
    val decoded = encoded.decodeBase64()

    println("Shifrlangan: $encoded")
    println("Tiklandi: $decoded")
}""",
        "Kodlash va shifrlash amallarini String kengaytmasiga aylantirish.",
        """Shifrlangan: TWF4Zml5IFRva2VuIDIwMjY=
Tiklandi: Maxfiy Token 2026"""
    ),
    (
        529,
        "Kolleksiyaning o'rtacha qiymatini yaxlitlab beruvchi kengaytma",
        "Int ro'yxatining o'rtacha qiymatini yaxlitlab chiqarish.",
        """fun List<Int>.roundedAverage(): Int {
    if (isEmpty()) return 0
    return Math.round(this.average()).toInt()
}

fun main() {
    val marks = listOf(85, 90, 78, 92)
    println("Yaxlitlangan o'rtacha baho: ${marks.roundedAverage()}")
}""",
        "Hisoblash logikasini umumiy kolleksiya kengaytmasiga joylash.",
        """Yaxlitlangan o'rtacha baho: 86"""
    ),
    (
        530,
        "Kengaytma orqali Map kalitlarini teskari o'girish (Invert Map)",
        "Map dagi kalit va qiymatlar o'rnini almashtiruvchi kengaytma funksiya.",
        """fun <K, V> Map<K, V>.invert(): Map<V, K> {
    return entries.associate { (k, v) -> v to k }
}

fun main() {
    val codes = mapOf("UZ" to "Uzbekistan", "FR" to "France")
    val inverted = codes.invert()
    println("Teskari xarita: $inverted")
}""",
        "Kengaytma orqali Map ma'lumotlarini teskari o'girish.",
        """Teskari xarita: {Uzbekistan=UZ, France=FR}"""
    ),
    (
        531,
        "Matndan HTML teglarni tozalash kengaytmasi",
        "Stringdagi barcha HTML teglarni (<p>, <b>) tozalovchi kengaytma.",
        """fun String.stripHtml(): String {
    return this.replace(Regex("<[^>]*>"), "")
}

fun main() {
    val htmlText = "<p>Salom <b>Dunyo</b>! <a href='#'>Havola</a></p>"
    println("Tozalangan: ${htmlText.stripHtml()}")
}""",
        "Web parsing va matn tahlilida HTML tozalash kengaytmasi.",
        """Tozalangan: Salom Dunyo! Havola"""
    ),
    (
        532,
        "Kolleksiya ustida 'takeLastOrAll' kengaytmasi",
        "Ro'yxatdan oxirgi N ta elementni xavfsiz olish.",
        """fun <T> List<T>.takeLastOrAll(n: Int): List<T> {
    return if (size <= n) this else takeLast(n)
}

fun main() {
    val list = listOf(1, 2, 3, 4, 5)
    println(list.takeLastOrAll(3))
    println(list.takeLastOrAll(10))
}""",
        "Chegaradan chiqib ketish xavfisiz oxirgi elementlarni ajratish.",
        """[3, 4, 5]
[1, 2, 3, 4, 5]"""
    ),
    (
        533,
        "Double sonini Foiz ko'rinishida formatlash",
        "0.15 sonini '15.0%' shaklida chiqaruvchi kengaytma.",
        """fun Double.toPercentageString(decimals: Int = 1): String {
    return String.format("%.${decimals}f%%", this * 100)
}

fun main() {
    println(0.125.toPercentageString())
    println(0.07.toPercentageString(2))
}""",
        "Statistika va moliya sohasida ko'p ishlatiladigan kengaytma.",
        """12.5%
7.00%"""
    ),
    (
        534,
        "StringBuilder ustida qatorma-qator qo'shish kengaytmasi",
        "StringBuilder ga bir nechta satrlarni qator tashlab qo'shuvchi kengaytma.",
        """fun StringBuilder.appendLines(vararg lines: String): StringBuilder {
    for (line in lines) {
        this.append(line).append("\n")
    }
    return this
}

fun main() {
    val sb = StringBuilder().appendLines("Birinchi qator", "Ikkinchi qator", "Uchinchi qator")
    println(sb.toString())
}""",
        "StringBuilder ga qulay qator qo'shish kengaytmasi.",
        """Birinchi qator
Ikkinchi qator
Uchinchi qator"""
    ),
    (
        535,
        "Kengaytma bilan telefon raqamini formatlash",
        "Toza 12 xonali raqamni '+998 (90) 123-45-67' ko'rinishiga keltirish.",
        """fun String.toFormattedUzPhone(): String {
    val d = this.filter { it.isDigit() }
    if (d.length != 12) return this
    return "+${d.substring(0, 3)} (${d.substring(3, 5)}) ${d.substring(5, 8)}-${d.substring(8, 10)}-${d.substring(10, 12)}"
}

fun main() {
    val raw = "998901234567"
    println("Formatlangan telefon: ${raw.toFormattedUzPhone()}")
}""",
        "O'zbekiston telefon raqamlari formatini avtomatlashtirish.",
        """Formatlangan telefon: +998 (90) 123-45-67"""
    ),
    (
        536,
        "Kolleksiyadagi ikkita element o'rnini almashtirib yangi ro'yxat olish",
        "O'zgarmas List ustida yangi almashtirilgan ro'yxat qaytaruvchi kengaytma.",
        """fun <T> List<T>.swapped(i: Int, j: Int): List<T> {
    val m = this.toMutableList()
    val temp = m[i]
    m[i] = m[j]
    m[j] = temp
    return m.toList()
}

fun main() {
    val original = listOf("A", "B", "C")
    val modified = original.swapped(0, 2)
    println("Original: $original")
    println("Almashtirilgan: $modified")
}""",
        "Immutability tamoyiliga to'liq mos keluvchi ro'yxat elementlari almashtirgichi.",
        """Original: [A, B, C]
Almashtirilgan: [C, B, A]"""
    ),
    (
        537,
        "Shartli kengaytma: Satr faqat raqamlardan iboratligini tekshirish",
        "String ustida '.isNumeric()' kengaytmasini yozish.",
        """fun String.isNumeric(): Boolean {
    return this.isNotEmpty() && this.all { it.isDigit() }
}

fun main() {
    println("12345: ${"12345".isNumeric()}")
    println("12a45: ${"12a45".isNumeric()}")
}""",
        "Kompakt va tezkor raqamli tekshiruv kengaytmasi.",
        """12345: true
12a45: false"""
    ),
    (
        538,
        "Int sonining Tub (Prime) ekanligini aniqlovchi kengaytma",
        "Int ustida to'g'ridan-to'g'ri '.isPrime()' metodini chaqirish.",
        """fun Int.isPrime(): Boolean {
    if (this <= 1) return false
    for (i in 2..Math.sqrt(this.toDouble()).toInt()) {
        if (this % i == 0) return false
    }
    return true
}

fun main() {
    println("17 tubmi: ${17.isPrime()}")
    println("24 tubmi: ${24.isPrime()}")
}""",
        "Arifmetik tekshiruvlarni qulay kengaytma shaklida taqdim etish.",
        """17 tubmi: true
24 tubmi: false"""
    ),
    (
        539,
        "Kolleksiyadagi elementlarning foiz ulushini hisoblovchi kengaytma",
        "Ro'yxatdagi har bir element butunning necha foizini tashkil qilishini topish.",
        """fun List<Double>.toPercentages(): List<Double> {
    val total = sum()
    if (total == 0.0) return map { 0.0 }
    return map { (it / total) * 100 }
}

fun main() {
    val parts = listOf(20.0, 30.0, 50.0)
    val p = parts.toPercentages()
    println("Foiz ulushlari: $p")
}""",
        "Statistik hisob-kitoblar uchun qulay kolleksiya kengaytmasi.",
        """Foiz ulushlari: [20.0, 30.0, 50.0]"""
    ),
    (
        540,
        "String ustida 'slugify' kengaytmasi (SEO URL yaratish)",
        "Sarlavhani xavfsiz URL manziliga aylantiruvchi kengaytma yozing.",
        """fun String.toSlug(): String {
    return this.lowercase()
        .replace(Regex("[^a-z0-9\\\\s]"), "")
        .trim()
        .replace(Regex("\\\\s+"), "-")
}

fun main() {
    val title = "Kotlin 2.0 yangiliklari va Imkoniyatlari!"
    println("Slug URL: ${title.toSlug()}")
}""",
        "Veb va blog dasturlarida SEO-mos slug manzilini yaratish kengaytmasi.",
        """Slug URL: kotlin-20-yangiliklari-va-imkoniyatlari"""
    ),
    (
        541,
        "Kengaytma bilan O'lchov birliklari: Harorat Selsiy va Farengeyt",
        "Double soniga '.toFahrenheit()' va '.toCelsius()' kengaytmalarini berish.",
        """fun Double.toFahrenheit(): Double = this * 9.0 / 5.0 + 32.0
fun Double.toCelsius(): Double = (this - 32.0) * 5.0 / 9.0

fun main() {
    val c = 25.0
    val f = c.toFahrenheit()
    println("$c°C = $f°F")
    println("$f°F = ${f.toCelsius()}°C")
}""",
        "Harorat o'lchov birliklari o'rtasida toza konvertatsiya.",
        """25.0°C = 77.0°F
77.0°F = 25.0°C"""
    ),
    (
        542,
        "Kolleksiyadagi tasodifiy elementni xavfsiz olish: randomOrNull kengaytmasi",
        "Bo'sh ro'yxatlarda xato bermaydigan tasodifiy element oluvchi kengaytma.",
        """fun <T> List<T>.customRandomOrNull(): T? {
    return if (isEmpty()) null else this[(0 until size).random()]
}

fun main() {
    val empty = emptyList<String>()
    println("Bo'sh ro'yxat tasodifiy: ${empty.customRandomOrNull()}")
    
    val items = listOf("Osh", "Shashlik", "Manti")
    println("Tasodifiy taom: ${items.customRandomOrNull()}")
}""",
        "Xatoliklarsiz tasodifiy element tanlash kengaytmasi.",
        """Bo'sh ro'yxat tasodifiy: null
Tasodifiy taom: tanlanadi."""
    ),
    (
        543,
        "Kengaytma orqali Stringni yashirish (Masking / Obfuscation)",
        "Karta raqamining o'rtasidagi raqamlarni yashiruvchi kengaytma yozing.",
        """fun String.maskCardNumber(): String {
    val digits = this.filter { it.isDigit() }
    if (digits.length != 16) return this
    return "${digits.substring(0, 4)} **** **** ${digits.substring(12)}"
}

fun main() {
    val rawCard = "8600123456789988"
    println("Niqoblangan karta: ${rawCard.maskCardNumber()}")
}""",
        "Xavfsizlik va konfidensiallik uchun matnni niqoblash kengaytmasi.",
        """Niqoblangan karta: 8600 **** **** 9988"""
    ),
    (
        544,
        "Shaxsiy 'filterNot' kengaytmasi",
        "Berilgan shartga mos kelmaydigan elementlarni olib qoluvchi kengaytma funksiya.",
        """fun <T> Iterable<T>.customFilterNot(predicate: (T) -> Boolean): List<T> {
    return this.filter { !predicate(it) }
}

fun main() {
    val numbers = listOf(1, 2, 3, 4, 5, 6)
    val notEvens = numbers.customFilterNot { it % 2 == 0 }
    println("Juft bo'lmaganlar: $notEvens")
}""",
        "Teskari mantiqiy filtrlash kengaytmasi.",
        """Juft bo'lmaganlar: [1, 3, 5]"""
    ),
    (
        545,
        "Int oraliqlari (Range) ustida tasodifiy son olish kengaytmasi",
        "IntRange ustida qulay kengaytma yozish.",
        """fun IntRange.sample(): Int {
    return (first..last).random()
}

fun main() {
    val range = 1..100
    println("Diapazondan son: ${range.sample()}")
}""",
        "Diapazonlar bilan ishlashni soddalashtiruvchi kengaytma.",
        """Diapazondan son: tanlanadi."""
    ),
    (
        546,
        "Stringni CamelCase dan Snake_Case ga o'tkazish kengaytmasi",
        "Satrdagi bosh harflar oldidan pastki chiziq qo'yuvchi kengaytma tuzing.",
        """fun String.toSnakeCase(): String {
    return this.replace(Regex("(?<=.)(?=[A-Z])"), "_").lowercase()
}

fun main() {
    val camel = "userNameAndAddress"
    println("Snake case: ${camel.toSnakeCase()}")
}""",
        "Ma'lumotlar bazasi va dasturlash konvensiyalari orasidagi nomlash konvertori.",
        """Snake case: user_name_and_address"""
    ),
    (
        547,
        "Kolleksiyaning Medianasini (Median) hisoblovchi kengaytma",
        "Saralangan tartibda o'rta qiymatni aniqlovchi Double/Int kengaytmasi.",
        """fun List<Int>.median(): Double {
    if (isEmpty()) return 0.0
    val sorted = sorted()
    val mid = sorted.size / 2
    return if (sorted.size % 2 == 1) {
        sorted[mid].toDouble()
    } else {
        (sorted[mid - 1] + sorted[mid]) / 2.0
    }
}

fun main() {
    val l1 = listOf(5, 1, 9)
    val l2 = listOf(1, 2, 8, 10)
    println("Mediana 1: ${l1.median()}")
    println("Mediana 2: ${l2.median()}")
}""",
        "Statistik medianani aniq hisoblash kengaytmasi.",
        """Mediana 1: 5.0
Mediana 2: 5.0"""
    ),
    (
        548,
        "Matnda so'zlar sonini hisoblovchi String kengaytmasi",
        "Bo'shliqlarga qarab haqiqiy so'zlar sonini hisoblash.",
        """fun String.wordCount(): Int {
    return if (this.isBlank()) 0 else this.trim().split(Regex("\\\\s+")).size
}

fun main() {
    val text = "  Kotlin   dasturlash   tili  "
    println("So'zlar soni: ${text.wordCount()} ta")
}""",
        "Ko'p bo'shliqlar va yangi qatorlarni to'g'ri hisobga oluvchi matn tahlili.",
        """So'zlar soni: 3 ta"""
    ),
    (
        549,
        "Kolleksiya ustida 'countBy' kengaytmasi",
        "Kolleksiyadagi har bir element xususiyat bo'yicha nechtadan uchrashini hisoblash.",
        """fun <T, K> Iterable<T>.customCountBy(keySelector: (T) -> K): Map<K, Int> {
    val map = mutableMapOf<K, Int>()
    for (item in this) {
        val key = keySelector(item)
        map[key] = map.getOrDefault(key, 0) + 1
    }
    return map
}

fun main() {
    val words = listOf("olma", "anor", "behi", "olcha", "banan")
    val countByInitial = words.customCountBy { it.first() }
    println("Bosh harf bo'yicha soni: $countByInitial")
}""",
        "Guruhlab statistik hisoblash kengaytmasi.",
        """Bosh harf bo'yicha soni: {o=2, a=1, b=2}"""
    ),
    (
        550,
        "Kengaytmalar bo'yicha to'liq amaliy xulosa: Korporativ Matn va Ma'lumotlarni Qayta Ishlash",
        "Extension functions, Extension properties, Nullable receiver extensions, Generics va Operator overloading ni birlashtirgan to'liq xizmat.",
        """// 1. Kengaytma xususiyat
val String.isStrongPassword: Boolean
    get() = length >= 8 && any { it.isDigit() } && any { it.isUpperCase() }

// 2. Nullable receiver kengaytma funksiya
fun String?.normalizePhone(): String {
    if (this == null) return "NO_PHONE"
    val digits = this.filter { it.isDigit() }
    return if (digits.length == 9) "+998$digits" else if (digits.length == 12) "+$digits" else "INVALID_PHONE"
}

// 3. Generik kengaytma funksiya
fun <T> List<T>.preview(count: Int = 2): String {
    val taken = take(count).joinToString(", ")
    val remaining = size - count
    return if (remaining > 0) "[$taken ... va yana $remaining ta]" else "[$taken]"
}

// 4. Operator kengaytma
operator fun String.times(n: Int): String = this.repeat(n.coerceAtLeast(0))

fun main() {
    val rawPhone: String? = "90 123 45 67"
    val passwordInput = "SecurePass2026"
    val userList = listOf("Jasur", "Sardor", "Nodir", "Alisher", "Malika")

    println("=" * 35)
    println("Parol mustahkammi: ${passwordInput.isStrongPassword}")
    println("Normallashtirilgan telefon: ${rawPhone.normalizePhone()}")
    println("Foydalanuvchilar ko'rinishi: ${userList.preview(3)}")
    println("=" * 35)
}""",
        "Ushbu yakuniy topshiriqda mavzuning barcha asosiy tamoyillari: Kengaytma xususiyati (isStrongPassword), Nullable receiver (normalizePhone), Generik kengaytma (preview) va Operator kengaytmasi (*) korporativ ma'lumotlar tahlilchisi misolida mukammal birlashtirildi.",
        """===================================
Parol mustahkammi: true
Normallashtirilgan telefon: +998901234567
Foydalanuvchilar ko'rinishi: [Jasur, Sardor, Nodir ... va yana 2 ta]
==================================="""
    )
]

for item in data_11:
    n, title, condition, sol, exp, res = item
    tasks.append(format_task(n, title, condition, sol, exp, res))

save_file("kotlin_11_kengaytmalar_extension_functions.md", tasks)
