# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

data_09 = [
    (
        401,
        "Lambda ifodalari asoslari va sintaksisi",
        "Ikki sonni qo'shuvchi va matnni formatlovchi oddiy lambda ifodalarini e'lon qiling va chaqiring.",
        """fun main() {
    // To'liq sintaksis:
    val sumLambda: (Int, Int) -> Int = { a: Int, b: Int -> a + b }
    
    // Tur xulosasi (Type inference) bilan:
    val greetLambda = { name: String -> "Salom, $name!" }

    println("5 + 7 = ${sumLambda(5, 7)}")
    println(greetLambda("Otabek"))
}""",
        "Kotlinda lambda ifodalari har doim jingalak qavslar '{ ... }' ichida yoziladi. Parametrlar '->' belgisidan oldin, funksiya tanasi esa '->' dan keyin joylashadi. Oxirgi qatordagi ifoda avtomatik ravishda qaytish qiymati hisoblanadi.",
        """5 + 7 = 12
Salom, Otabek!"""
    ),
    (
        402,
        "Yagona parametr va 'it' yashirin identifikatori",
        "Bitta parametrli lambdada parametr nomini yozmasdan 'it' so'zi orqali murojaat qilish imkoniyatini ko'rsating.",
        """fun main() {
    val numbers = listOf(1, 2, 3, 4, 5)
    
    // '{ n -> n * 2 }' o'rniga ixcham '{ it * 2 }':
    val doubled = numbers.map { it * 2 }
    
    val evens = numbers.filter { it % 2 == 0 }

    println("Ikki barobar oshirilgan: $doubled")
    println("Juft sonlar: $evens")
}""",
        "Agar lambda ifodasi faqat bitta parametr qabul qilsa, dasturchi unga nom berishi shart emas. Kotlin kompilyatori avtomatik ravishda ushbu parametrni 'it' deb nomlaydi.",
        """Ikki barobar oshirilgan: [2, 4, 6, 8, 10]
Juft sonlar: [2, 4]"""
    ),
    (
        403,
        "Tashqi lambda sintaksisi (Trailing Lambda Syntax)",
        "Agar funksiyaning oxirgi parametri lambda bo'lsa, uni dumaloq qavslardan tashqariga chiqarish qoidasini qo'llang.",
        """fun performCalculation(a: Int, b: Int, operation: (Int, Int) -> Int): Int {
    return operation(a, b)
}

fun main() {
    // 1. Qavs ichida uzatish (an'anaviy):
    val res1 = performCalculation(10, 5, { x, y -> x - y })

    // 2. Trailing lambda (Kotlinga xos qulay uslub):
    val res2 = performCalculation(10, 5) { x, y ->
        x * y
    }

    println("Ayirma: $res1")
    println("Ko'paytma: $res2")
}""",
        "Kotlinda agar funksiyaning oxirgi parametri funksional tur (lambda) bo'lsa, lambda ifodasini dumaloq qavslar tashqarisiga chiqarish tavsiya etiladi. Agar funksiya faqat bitta parametr qabul qilsa va u lambda bo'lsa, dumaloq qavslar butunlay tashlab ketiladi.",
        """Ayirma: 5
Ko'paytma: 50"""
    ),
    (
        404,
        "Yuqori tartibli funksiya (Higher-Order Function) yaratish",
        "O'z parametrida funksiya qabul qiluvchi va natijani filtrlovchi yuqori tartibli funksiya yozing.",
        """fun modifyAndPrint(numbers: List<Int>, transformer: (Int) -> String) {
    for (n in numbers) {
        val result = transformer(n)
        println("O'zgartirildi: $result")
    }
}

fun main() {
    val items = listOf(10, 25, 50)
    modifyAndPrint(items) { "Son: $it (Qoldiq: ${it % 3})" }
}""",
        "Yuqori tartibli funksiya (Higher-Order Function) deb boshqa funksiyalarni parametr sifatida qabul qiluvchi yoki o'zidan funksiya qaytaruvchi funksiyalarga aytiladi.",
        """O'zgartirildi: Son: 10 (Qoldiq: 1)
O'zgartirildi: Son: 25 (Qoldiq: 1)
O'zgartirildi: Son: 50 (Qoldiq: 2)"""
    ),
    (
        405,
        "Funksiyadan funksiya qaytarish (Factory of Functions)",
        "Berilgan prefiks bilan matn chiquvchi yangi funksiya generatsiya qiluvchi fabrika tuzing.",
        """fun createLogger(tag: String): (String) -> Unit {
    return { message ->
        println("[$tag]: $message")
    }
}

fun main() {
    val authLog = createLogger("AUTH")
    val networkLog = createLogger("NETWORK")

    authLog("Foydalanuvchi tizimga kirdi")
    networkLog("200 OK javob qaytdi")
}""",
        "Funksiyadan yangi funksiya qaytarish orqali konfiguratsiyalangan yordamchi funksiyalarni dinamik generatsiya qilish mumkin.",
        """[AUTH]: Foydalanuvchi tizimga kirdi
[NETWORK]: 200 OK javob qaytdi"""
    ),
    (
        406,
        "Murakkab signaturalarni soddalashtirish: 'typealias'",
        "Ko'p parametrli funksiya turlarini o'qishli qilish uchun 'typealias' e'lon qiling.",
        """typealias ValidationRule = (input: String) -> Boolean
typealias ErrorHandler = (errorCode: Int, reason: String) -> Unit

fun validateForm(text: String, rule: ValidationRule, onError: ErrorHandler) {
    if (rule(text)) {
        println("Forma to'g'ri to'ldirilgan: $text")
    } else {
        onError(400, "Maydon validatsiyadan o'tmadi")
    }
}

fun main() {
    val notBlankRule: ValidationRule = { it.isNotBlank() }
    val printError: ErrorHandler = { code, msg -> println("[XATO $code]: $msg") }

    validateForm("Toshkent", notBlankRule, printError)
    validateForm("", notBlankRule, printError)
}""",
        "'typealias' yangi tur yaratmaydi, balki mavjud murakkab funksiya turiga qisqa va qulay nom beradi. Bu kodning arxitekturasini o'ta tushunarli qiladi.",
        """Forma to'g'ri to'ldirilgan: Toshkent
[XATO 400]: Maydon validatsiyadan o'tmadi"""
    ),
    (
        407,
        "Inline funksiyalar asoslari: 'inline' modifikatori",
        "Har safar yangi funksional obyekt yaratilishini oldini olish uchun 'inline' kalit so'zidan foydalaning.",
        """inline fun measureTime(block: () -> Unit) {
    val start = System.currentTimeMillis()
    block()
    val end = System.currentTimeMillis()
    println("Bajarilish vaqti: ${end - start} ms")
}

fun main() {
    measureTime {
        var sum = 0L
        for (i in 1..100_000) sum += i
        println("Hisoblash yakunlandi: $sum")
    }
}""",
        "Kotlinda har bir lambda bayt-kod darajasida anonim sinf nusxasi (Function obyekt) yaratadi. Agar funksiya 'inline' qilinsa, kompilyator lambdaning ichidagi kodni to'g'ridan-to'g'ri chaqirilgan joyga nusxalaydi (inlining). Bu xotira va GC yukini nolga tushiradi.",
        """Hisoblash yakunlandi: 5000050000
Bajarilish vaqti: o'lchanadi."""
    ),
    (
        408,
        "Inlineni cheklash: 'noinline' modifikatori",
        "Inline funksiyaga kelgan bir nechta lambdadan faqat bittasini saqlash uchun 'noinline' dan foydalaning.",
        """inline fun executeBoth(
    inlineLambda: () -> Unit,
    noinline savedLambda: () -> Unit
) {
    inlineLambda()
    // savedLambda ni boshqa metodga yoki o'zgaruvchiga uzatish mumkin:
    storeCallback(savedLambda)
}

fun storeCallback(callback: () -> Unit) {
    println("[SAQLANDI]: Callback xotiraga olindi")
    callback()
}

fun main() {
    executeBoth(
        inlineLambda = { println("1. Inline lambda to'g'ridan-to'g'ri ishga tushdi") },
        savedLambda = { println("2. Saqlangan lambda chaqirildi") }
    )
}""",
        "Inline qilingan lambdalarni o'zgaruvchiga biriktirib yoki boshqa non-inline funksiyaga uzatib bo'lmaydi. Agar ba'zi parametrlar saqlanishi kerak bo'lsa, ular 'noinline' bilan belgilanadi.",
        """1. Inline lambda to'g'ridan-to'g'ri ishga tushdi
[SAQLANDI]: Callback xotiraga olindi
2. Saqlangan lambda chaqirildi"""
    ),
    (
        409,
        "Non-local return va inline funksiyalar",
        "Inline funksiyalar ichidagi lambdadan to'g'ridan-to'g'ri tashqi funksiyadan 'return' qilib chiqish imkoniyatini ko'rsating.",
        """inline fun checkConditions(numbers: List<Int>, predicate: (Int) -> Boolean) {
    for (n in numbers) {
        if (predicate(n)) return // Non-local return! Tashqi main funksiyadan ham chiqishi mumkin!
    }
}

fun runAnalysis() {
    val list = listOf(1, 3, 5, 8, 9)
    checkConditions(list) {
        if (it % 2 == 0) {
            println("Juft son ($it) topildi, butun analiz to'xtatildi!")
            return // runAnalysis dan chiqadi!
        }
        false
    }
    println("Bu qatorga yetib kelinmadi.")
}

fun main() {
    runAnalysis()
    println("Dastur yakunlandi.")
}""",
        "Oddiy lambdalarda 'return' yozish taqiqlangan. Ammo 'inline' funksiyalarda lambda kodining o'zi to'g'ridan-to'g'ri funksiya tanasiga ko'chirilishi sababli, unda 'return' ishlatilsa, u butun tashqi funksiyani yakunlaydi (Non-local return).",
        """Juft son (8) topildi, butun analiz to'xtatildi!
Dastur yakunlandi."""
    ),
    (
        410,
        "Lokal bo'lmagan returndan himoyalanish: 'crossinline'",
        "Lambdani boshqa ijro kontekstida (masalan Runnable ichida) chaqirish va xavfli non-local returnni taqiqlash uchun 'crossinline' ni qo'llang.",
        """inline fun runAsync(crossinline task: () -> Unit) {
    val runnable = Runnable {
        task() // Boshqa obyekt ichida chaqirilmoqda
    }
    Thread(runnable).start()
}

fun main() {
    runAsync {
        println("Parallel oqimda bajarildi.")
        // return // Kompilyatsiya xatosi: 'return' is not allowed here (crossinline taqiqlaydi)
    }
    Thread.sleep(50)
}""",
        "Agar inline funksiya ichida lambda boshqa oqim yoki anonim obyekt ichiga uzatilsa, undan 'return' qilish butun tashqi funksiyani buzib yuborishi mumkin. 'crossinline' modifikatori lambdani inline qilishni saqlagan holda unda no-local return ishlatilishini qat'iy taqiqlaydi.",
        """Parallel oqimda bajarildi."""
    ),
    (
        411,
        "Yopilishlar (Closures) va o'zgaruvchilarni qamrab olish",
        "Lambda tashqi doiradagi 'var' o'zgaruvchini qamrab olib, har safar chaqirilganda uni oshirib borishini ko'rsating.",
        """fun createCounter(): () -> Int {
    var count = 0
    return {
        count++
        count
    }
}

fun main() {
    val c1 = createCounter()
    val c2 = createCounter()

    println("c1: ${c1()}")
    println("c1: ${c1()}")
    println("c2: ${c2()}")
    println("c1: ${c1()}")
}""",
        "Kotlinda lambda o'zi yaratilgan muhitdagi o'zgaruvchilarni (closures) saqlab qoladi. Har bir 'createCounter()' alohida 'count' yacheykasiga ega bo'lib, mustaqil ishlaydi.",
        """c1: 1
c1: 2
c2: 1
c1: 3"""
    ),
    (
        412,
        "Funksional kompozitsiya (compose) va zanjir",
        "Ikki funksiyani ketma-ket birlashtiruvchi kompozitsiya funksiyasini yozing.",
        """fun <A, B, C> compose(f: (B) -> C, g: (A) -> B): (A) -> C {
    return { x -> f(g(x)) }
}

fun main() {
    val doubleIt = { x: Int -> x * 2 }
    val toText = { x: Int -> "Natija: $x" }

    val doubleAndText = compose(toText, doubleIt)
    println(doubleAndText(21))
}""",
        "Matematik f(g(x)) prinsipiga ko'ra ikki funksiya bitta yangi zanjirli funksiyaga aylanadi.",
        """Natija: 42"""
    ),
    (
        413,
        "Karriylash (Currying) funksiyalari",
        "Ko'p parametrli funksiyani bitta parametrdan qabul qiluvchi zanjirli funksiyalarga aylantiring.",
        """fun <A, B, C> curry(f: (A, B) -> C): (A) -> (B) -> C {
    return { a -> { b -> f(a, b) } }
}

fun main() {
    val sum = { a: Int, b: Int -> a + b }
    val curriedSum = curry(sum)

    val addFive = curriedSum(5)
    println("5 + 10 = ${addFive(10)}")
    println("5 + 20 = ${addFive(20)}")
}""",
        "Currying (Haskell Curry sharafiga nomlangan) bir nechta argumentli funksiyani bitta argumentli funksiyalar ketma-ketligiga bo'lib beradi.",
        """5 + 10 = 15
5 + 20 = 25"""
    ),
    (
        414,
        "Qisman qo'llash (Partial Application)",
        "Funksiyaning birinchi parametrini oldindan belgilab, yangi bir parametrli funksiya hosil qiling.",
        """fun <A, B, R> partiallyApply(f: (A, B) -> R, a: A): (B) -> R {
    return { b -> f(a, b) }
}

fun multiply(x: Double, y: Double): Double = x * y

fun main() {
    val taxMultiplier = partiallyApply(::multiply, 1.12) // 12% soliq ko'paytiruvchisi
    println("100 soliq bilan: ${taxMultiplier(100.0)}")
    println("250 soliq bilan: ${taxMultiplier(250.0)}")
}""",
        "Qisman qo'llash orqali umumiy algoritmlardan ma'lum bir biznes qoidasi uchun ixtisoslashgan kichik funksiyalar yasaladi.",
        """100 soliq bilan: 112.0
250 soliq bilan: 280.0"""
    ),
    (
        415,
        "Lambda receiver bilan (Lambda with Receiver)",
        "Blok ichida ob'ekt xususiyatlariga 'this' orqali to'g'ridan-to'g'ri murojaat qilish imkoniyatini ko'rsating.",
        """class HtmlBuilder {
    val content = StringBuilder()

    fun h1(text: String) { content.append("<h1>$text</h1>\n") }
    fun p(text: String) { content.append("<p>$text</p>\n") }
}

fun html(init: HtmlBuilder.() -> Unit): String {
    val builder = HtmlBuilder()
    builder.init() // Receiver sifatida chaqiriladi
    return builder.content.toString()
}

fun main() {
    val page = html {
        h1("Xush kelibsiz!")
        p("Kotlin DSL imkoniyatlari juda boy.")
    }

    println(page)
}""",
        "'Type.() -> Unit' sintaksisi Kotlinda DSL (Domain Specific Language) qurishning negizidir. Lambda tanasida ushbu tur 'this' ga aylanadi.",
        """<h1>Xush kelibsiz!</h1>
<p>Kotlin DSL imkoniyatlari juda boy.</p>"""
    ),
    (
        416,
        "Yorliqli return bilan lambdadan mahalliy chiqish",
        "Non-inline lambdada faqat o'sha sikl qadamidan chiqish uchun 'return@label' dan foydalaning.",
        """fun main() {
    val list = listOf("olma", "banan", "nok", "uzum")

    list.forEach myLabel@ {
        if (it == "nok") return@myLabel // continue vazifasini o'taydi
        println("Meva: $it")
    }

    println("Sikl to'liq yakunlandi.")
}""",
        "Yorliq berish 'return@myLabel' lambdadan mahalliy (local) chiqishni ta'minlaydi va tashqi funksiya normal ishlashda davom etadi.",
        """Meva: olma
Meva: banan
Meva: uzum
Sikl to'liq yakunlandi."""
    ),
    (
        417,
        "Shartli predikatlarni birlashtirish: And va Or funksiyalari",
        "Ikki predikatni birlashtiruvchi yuqori tartibli mantiqiy funksiyalar yozing.",
        """fun <T> combineAnd(p1: (T) -> Boolean, p2: (T) -> Boolean): (T) -> Boolean {
    return { item -> p1(item) && p2(item) }
}

fun main() {
    val isEven = { x: Int -> x % 2 == 0 }
    val isPositive = { x: Int -> x > 0 }

    val isPositiveEven = combineAnd(isEven, isPositive)

    println("4: ${isPositiveEven(4)}")
    println("-4: ${isPositiveEven(-4)}")
    println("5: ${isPositiveEven(5)}")
}""",
        "Predikat funksiyalarni mantiqiy kompozitsiya qilish orqali murakkab ma'lumotlar filtrlarini dinamik yig'ish mumkin.",
        """4: true
-4: false
5: false"""
    ),
    (
        418,
        "Funksional quvur: pipe operatori",
        "Qiymatni ketma-ket bir nechta funksiyalar orqali o'tkazuvchi 'pipe' kengaytmasini yozing.",
        """infix fun <T, R> T.pipe(transform: (T) -> R): R = transform(this)

fun main() {
    val result = "  125  "
        .pipe { it.trim() }
        .pipe { it.toInt() }
        .pipe { it * 2 }

    println("Quvur natijasi: $result")
}""",
        "Elixir yoki F# kabi tillardagi pipe '|>' operatorini Kotlinda bitta kichik infix funksiya bilan yaratish mumkin.",
        """Quvur natijasi: 250"""
    ),
    (
        419,
        "Shaxsiy 'filter' inline funksiyasini yozish",
        "Standart kutubxonadagi 'filter' kabi xotirani tejovchi shaxsiy inline funksiya tuzing.",
        """inline fun <T> customFilter(list: List<T>, predicate: (T) -> Boolean): List<T> {
    val result = ArrayList<T>()
    for (item in list) {
        if (predicate(item)) {
            result.add(item)
        }
    }
    return result
}

fun main() {
    val numbers = listOf(1, 2, 3, 4, 5, 6)
    val evens = customFilter(numbers) { it % 2 == 0 }
    println("Juft sonlar: $evens")
}""",
        "Kolleksiyalarni aylanib chiquvchi yuqori tartibli funksiyalarni 'inline' qilish bayt-kodda siklga aylanadi va hech qanday ortiqcha lambda obyekti yaratilmaydi.",
        """Juft sonlar: [2, 4, 6]"""
    ),
    (
        420,
        "Shaxsiy 'map' inline funksiyasini yozish",
        "Kolleksiya elementlarini boshqa turga o'tkazuvchi shaxsiy 'inline customMap' funksiyasini tuzing.",
        """inline fun <T, R> customMap(list: List<T>, transform: (T) -> R): List<R> {
    val result = ArrayList<R>(list.size)
    for (item in list) {
        result.add(transform(item))
    }
    return result
}

fun main() {
    val words = listOf("Salom", "Dunyo", "Kotlin")
    val lengths = customMap(words) { it.length }
    println("So'z uzunliklari: $lengths")
}""",
        "'inline' tufayli 'customMap' ichidagi 'transform' lambdasi har bir element uchun obyekt ajratmasdan, to'g'ridan-to'g'ri bayt-kodga kiritiladi.",
        """So'z uzunliklari: [5, 5, 6]"""
    ),
    (
        421,
        "Funksional xatolar bilan: Result qaytaruvchi Pipeline",
        "Har bir qadam muvaffaqiyatsiz bo'lsa darhol xatoni to'xtatuvchi funksional zanjir.",
        """sealed class FlowResult<out T> {
    data class Success<T>(val value: T) : FlowResult<T>()
    data class Failure(val error: String) : FlowResult<Nothing>()
}

inline fun <T, R> FlowResult<T>.flatMap(transform: (T) -> FlowResult<R>): FlowResult<R> {
    return when (this) {
        is FlowResult.Success -> transform(this.value)
        is FlowResult.Failure -> this
    }
}

fun main() {
    val parse = { s: String ->
        val n = s.toIntOrNull()
        if (n != null) FlowResult.Success(n) else FlowResult.Failure("Son emas: $s")
    }

    val validatePositive = { n: Int ->
        if (n > 0) FlowResult.Success(n) else FlowResult.Failure("Musbat emas: $n")
    }

    val res1 = FlowResult.Success("45").flatMap(parse).flatMap(validatePositive)
    val res2 = FlowResult.Success("-10").flatMap(parse).flatMap(validatePositive)

    println("Natija 1: $res1")
    println("Natija 2: $res2")
}""",
        "Monadalar va 'flatMap' zanjiri orqali har bir qadam xavfsiz tekshiriladi va xatoliklar istisnosiz qayta ishlanadi.",
        """Natija 1: Success(value=45)
Natija 2: Failure(error=Musbat emas: -10)"""
    ),
    (
        422,
        "Shaxsiy 'repeat' inline funksiyasi",
        "Standart 'repeat' funksiyasining ishlash mexanizmini o'zingiz realizatsiya qiling.",
        """inline fun customRepeat(times: Int, action: (Int) -> Unit) {
    for (i in 0 until times) {
        action(i)
    }
}

fun main() {
    customRepeat(3) {
        println("Qadam #${it + 1}")
    }
}""",
        "'customRepeat' inline funksiya bo'lgani sababli, uning ichidagi for sikli chaqirilgan joyga to'g'ridan-to'g'ri joylashadi.",
        """Qadam #1
Qadam #2
Qadam #3"""
    ),
    (
        423,
        "Lambdalar bilan Keshlovchi xotira o'rami (Memoization)",
        "Yuqori tartibli funksiya orqali qimmat hisoblash natijasini saqlovchi dekorator tuzing.",
        """fun <T, R> ((T) -> R).memoized(): (T) -> R {
    val cache = mutableMapOf<T, R>()
    return { param ->
        cache.getOrPut(param) { this(param) }
    }
}

fun main() {
    val slowFactorial = { n: Int ->
        var res = 1L
        for (i in 2..n) res *= i
        res
    }.memoized()

    println("5! = ${slowFactorial(5)}")
    println("5! (keshdan) = ${slowFactorial(5)}")
}""",
        "Funksiya turlari ustiga kengaytma funksiyalar ('((T) -> R).memoized()') yozish orqali ixtiyoriy lambdani boyitish mumkin.",
        """5! = 120
5! (keshdan) = 120"""
    ),
    (
        424,
        "Funksiya argumentlarini teskari o'girish (Flip Arguments)",
        "Ikki parametrli funksiyaning parametrlari tartibini almashtiruvchi yuqori tartibli yordamchi.",
        """fun <A, B, R> flip(f: (A, B) -> R): (B, A) -> R {
    return { b, a -> f(a, b) }
}

fun main() {
    val divide = { a: Double, b: Double -> a / b }
    val flippedDivide = flip(divide)

    println("10 / 2 = ${divide(10.0, 2.0)}")
    println("2 / 10 = ${flippedDivide(2.0, 10.0)}")
}""",
        "Funksional parametrlarni aylantirish orqali mavjud metodlarni yangi interfeyslarga moslashtirish osonlashadi.",
        """10 / 2 = 5.0
2 / 10 = 5.0"""
    ),
    (
        425,
        "Shaxsiy 'forEachIndexed' inline funksiyasi",
        "Indeks va elementni bir vaqtda uzatuvchi inline sikl funksiyasini yozing.",
        """inline fun <T> Iterable<T>.customForEachIndexed(action: (index: Int, item: T) -> Unit) {
    var index = 0
    for (item in this) {
        action(index++, item)
    }
}

fun main() {
    val languages = listOf("Kotlin", "Rust", "Go")
    languages.customForEachIndexed { idx, lang ->
        println("$idx -> $lang")
    }
}""",
        "Iterable ustida 'inline' kengaytma yozish orqali ortiqcha obyektlarsiz yuqori unumdorlikka erishiladi.",
        """0 -> Kotlin
1 -> Rust
2 -> Go"""
    ),
    (
        426,
        "Shartli chaqiruv: Lambdada vaqtinchalik o'zgaruvchilarni cheklash",
        "Anonim blok ichida xotirada faqat bitta hisoblash natijasini qoldirish.",
        """fun main() {
    val result = run {
        val rawInput = " 98765 "
        val cleaned = rawInput.trim()
        val num = cleaned.toInt()
        num * 2
    }

    println("Natija: $result")
}""",
        "'run { ... }' orqali oraliq o'zgaruvchilar (rawInput, cleaned, num) tashqi doirani ifloslantirmasdan, faqat yakuniy natija qaytariladi.",
        """Natija: 197530"""
    ),
    (
        427,
        "Funksional predikatlar: Predikatlarni inkor qilish (Not Predicate)",
        "Berilgan ixtiyoriy predikatning teskarisini qaytaruvchi yuqori tartibli funksiya.",
        """fun <T> notPredicate(predicate: (T) -> Boolean): (T) -> Boolean {
    return { item -> !predicate(item) }
}

fun main() {
    val isPositive = { x: Int -> x > 0 }
    val isNotPositive = notPredicate(isPositive)

    println("5 musbat emasmi: ${isNotPositive(5)}")
    println("-2 musbat emasmi: ${isNotPositive(-2)}")
}""",
        "Predikatlarni inkor qilish orqali mavjud tekshiruvlardan teskari qoidalarni oson generatsiya qilish mumkin.",
        """5 musbat emasmi: false
-2 musbat emasmi: true"""
    ),
    (
        428,
        "Inline funksiyalarda Rekursiyaning taqiqlanishi",
        "Nima uchun inline funksiya o'zini o'zi chaqira olmasligini (cheksiz kod ko'payishi) tushuntiring.",
        """// inline fun infiniteInline() { infiniteInline() } // Kompilyatsiya xatosi!

fun regularRecursion(n: Int): Int {
    if (n <= 1) return 1
    return n * regularRecursion(n - 1)
}

fun main() {
    println("Faktorial (oddiy rekursiya): ${regularRecursion(4)}")
}""",
        "Kompilyator inline funksiya tanasini chaqirilgan joyga nusxalaydi. Agar inline funksiya o'zini chaqirsa, cheksiz nusxalash yuzaga keladi. Shu sababli Kotlin kompilyatori inline funksiyalarda rekursiyani qat'iyan man etadi.",
        """Faktorial (oddiy rekursiya): 24"""
    ),
    (
        429,
        "Tranzaksiya o'rami: Inline tranzaksiya bajaruvchisi",
        "Operatsiyani xavfsiz tranzaksiya ichida bajaruvchi inline funksiya tuzing.",
        """inline fun <T> runInTransaction(txName: String, block: () -> T): T {
    println("[TRANZAKSIYA BOSHLANDI]: $txName")
    return try {
        val result = block()
        println("[TRANZAKSIYA TASDIQLANDI (COMMIT)]: $txName")
        result
    } catch (e: Exception) {
        println("[TRANZAKSIYA BEKOR QILINDI (ROLLBACK)]: ${e.message}")
        throw e
    }
}

fun main() {
    val output = runInTransaction("Foydalanuvchini Saqlash") {
        "Foydalanuvchi ma'lumotlari bazaga yozildi"
    }
    println("Natija: $output")
}""",
        "Resurslarni boshqarish va tranzaksiyalarni o'rab bajarishda inline funksiyalar hech qanday ortiqcha xotira sarflamasdan ishlaydi.",
        """[TRANZAKSIYA BOSHLANDI]: Foydalanuvchini Saqlash
[TRANZAKSIYA TASDIQLANDI (COMMIT)]: Foydalanuvchini Saqlash
Natija: Foydalanuvchi ma'lumotlari bazaga yozildi"""
    ),
    (
        430,
        "Shaxsiy 'takeWhile' inline funksiyasi",
        "Shart to'g'ri bo'lib turguncha elementlarni yig'uvchi inline funksiya yozing.",
        """inline fun <T> List<T>.customTakeWhile(predicate: (T) -> Boolean): List<T> {
    val result = mutableListOf<T>()
    for (item in this) {
        if (!predicate(item)) break
        result.add(item)
    }
    return result
}

fun main() {
    val numbers = listOf(2, 4, 6, 7, 8, 10)
    val leadingEvens = numbers.customTakeWhile { it % 2 == 0 }
    println("Birinchi toq songacha bo'lgan juftlar: $leadingEvens")
}""",
        "Shart buzilishi bilan 'break' qilib to'xtatuvchi xavfsiz inline filtrlash.",
        """Birinchi toq songacha bo'lgan juftlar: [2, 4, 6]"""
    ),
    (
        431,
        "Funksiyalar ro'yxatini ketma-ket bajarish",
        "Bir nechta lambdani ro'yxatga olib, navbatma-navbat bitta qiymatga qo'llash.",
        """fun main() {
    val pipeline: List<(Int) -> Int> = listOf(
        { it + 10 },
        { it * 2 },
        { it - 5 }
    )

    var value = 5
    for (fn in pipeline) {
        value = fn(value)
    }

    println("Yakuniy natija ((5 + 10) * 2 - 5): $value")
}""",
        "Funksiyalarni ma'lumot kabi massivda saqlash va ularni siklda ishlatish funksional arxitekturaning kuchli imkoniyatidir.",
        """Yakuniy natija ((5 + 10) * 2 - 5): 25"""
    ),
    (
        432,
        "Lambdada parametrlarni e'tiborsiz qoldirish: Pastki chiziq '_'",
        "Kerak bo'lmagan lambda parametrlarini pastki chiziq orqali belgilash.",
        """fun main() {
    val map = mapOf("A" to 1, "B" to 2, "C" to 3)

    // Faqat qiymat kerak bo'lganda kalitni '_' qilamiz:
    map.forEach { (_, value) ->
        println("Qiymat: $value")
    }
}""",
        "Agar lambda parametrlaridan biri ishlatilmasa, '_' qo'yish orqali xotira va kod o'qilishi tejaladi.",
        """Qiymat: 1
Qiymat: 2
Qiymat: 3"""
    ),
    (
        433,
        "Shaxsiy 'groupBy' inline funksiyasi analogi",
        "Elementlarni berilgan kalit funksiyasi bo'yicha guruhlovchi yordamchi funksiya.",
        """inline fun <T, K> List<T>.customGroupBy(keySelector: (T) -> K): Map<K, List<T>> {
    val result = mutableMapOf<K, MutableList<T>>()
    for (item in this) {
        val key = keySelector(item)
        val group = result.getOrPut(key) { mutableListOf() }
        group.add(item)
    }
    return result
}

fun main() {
    val words = listOf("olma", "anor", "behi", "banan", "shaftoli")
    val grouped = words.customGroupBy { it.first() }
    println("Bosh harfi bo'yicha guruhlar: $grouped")
}""",
        "Elementlarni 'keySelector' lambdasi orqali xaritada guruhlash amaliyotda juda ko'p qo'llaniladi.",
        """Bosh harfi bo'yicha guruhlar: {o=[olma], a=[anor], b=[behi, banan], s=[shaftoli]}"""
    ),
    (
        434,
        "Inline funksiya bilan Xavfsiz Resurs yopish: Shaxsiy 'use' funksiyasi",
        "Resurs bilan ish tugagach 'close()' chaqiruvchi shaxsiy inline funksiya tuzing.",
        """import java.io.Closeable

inline fun <T : Closeable?, R> T.customUse(block: (T) -> R): R {
    try {
        return block(this)
    } finally {
        this?.close()
    }
}

class DemoResource : Closeable {
    fun operate() = println("Resurs bilan xavfsiz ish bajarildi.")
    override fun close() = println("Resurs yopildi.")
}

fun main() {
    DemoResource().customUse { res ->
        res.operate()
    }
}""",
        "Kotlindagi standart 'use' funksiyasi aynan shu inline arxitekturada qurilgan va resurslarni oqib ketishidan (memory leak) himoya qiladi.",
        """Resurs bilan xavfsiz ish bajarildi.
Resurs yopildi."""
    ),
    (
        435,
        "Funksional Valyuta Formatlash: Lambda orqali konvertor",
        "Har xil valyutalar uchun formatlovchi lambdalar xaritasi tuzing.",
        """fun main() {
    val formatters: Map<String, (Double) -> String> = mapOf(
        "UZS" to { "%,.0f so'm".format(it) },
        "USD" to { "$%,.2f".format(it) },
        "EUR" to { "€%,.2f".format(it) }
    )

    val amount = 1500000.0
    println(formatters["UZS"]?.invoke(amount))
    println(formatters["USD"]?.invoke(125.50))
}""",
        "Lambdalarni 'Map' da saqlash orqali Strategy patternini sinflarsiz, juda qisqa va qulay shakllantirish mumkin.",
        """1,500,000 so'm
$125.50"""
    ),
    (
        436,
        "Shaxsiy 'zip' inline funksiyasi",
        "Ikki ro'yxatni berilgan transformator lambda orqali juftlovchi funksiya.",
        """inline fun <T, U, R> List<T>.customZip(other: List<U>, transform: (T, U) -> R): List<R> {
    val size = Math.min(this.size, other.size)
    val result = ArrayList<R>(size)
    for (i in 0 until size) {
        result.add(transform(this[i], other[i]))
    }
    return result
}

fun main() {
    val names = listOf("Ali", "Vali", "G'ani")
    val scores = listOf(90, 85, 95)

    val combined = names.customZip(scores) { name, score -> "$name: $score ball" }
    println("Natijalar: $combined")
}""",
        "Ikki ro'yxatni parallel birlashtirishda inline lambda yordamida ortiqcha obyektlar ajratilmaydi.",
        """Natijalar: [Ali: 90 ball, Vali: 85 ball, G'ani: 95 ball]"""
    ),
    (
        437,
        "Funksiyalarda rekursiv yig'uvchi (Accumulator)",
        "Lambda bilan yig'uvchi orqali elementlarni umumlashtirish.",
        """fun <T, R> List<T>.customFold(initial: R, operation: (acc: R, item: T) -> R): R {
    var accumulator = initial
    for (item in this) {
        accumulator = operation(accumulator, item)
    }
    return accumulator
}

fun main() {
    val numbers = listOf(1, 2, 3, 4)
    val sum = numbers.customFold(0) { acc, num -> acc + num }
    val product = numbers.customFold(1) { acc, num -> acc * num }

    println("Yig'indi: $sum")
    println("Ko'paytma: $product")
}""",
        "'fold' funksiyasi funksional dasturlashning eng universal funksiyalaridan biri bo'lib, har qanday ro'yxatni bitta qiymatga keltirishga qodir.",
        """Yig'indi: 10
Ko'paytma: 24"""
    ),
    (
        438,
        "Inline funksiya bilan Profiling va Hisobot",
        "Vazifa nomini va uning ishlash statistikasini inline orqali qayd etish.",
        """inline fun <T> profileTask(name: String, block: () -> T): T {
    val start = System.nanoTime()
    val result = block()
    val duration = (System.nanoTime() - start) / 1_000_000.0
    println("[METRIKA]: '$name' bajarildi: %.3f ms".format(duration))
    return result
}

fun main() {
    val data = profileTask("Massiv saralash") {
        (1..1000).toList().shuffled().sorted()
    }
    println("Saralangan hajm: ${data.size}")
}""",
        "Yuqori aniqlikdagi vaqt o'lchovlari inline tufayli hech qanday sekinlashuvsiz ishlaydi.",
        """Saralangan hajm: 1000"""
    ),
    (
        439,
        "Shaxsiy 'partition' inline funksiyasi",
        "Ro'yxatni berilgan shartga ko'ra ikkiga (mos kelganlar va kelmaganlar) ajratuvchi funksiya.",
        """inline fun <T> List<T>.customPartition(predicate: (T) -> Boolean): Pair<List<T>, List<T>> {
    val first = ArrayList<T>()
    val second = ArrayList<T>()
    for (element in this) {
        if (predicate(element)) first.add(element) else second.add(element)
    }
    return Pair(first, second)
}

fun main() {
    val numbers = listOf(10, 15, 20, 25, 30)
    val (evens, odds) = numbers.customPartition { it % 2 == 0 }

    println("Juftlar: $evens")
    println("Toqlar: $odds")
}""",
        "Bitta sikl ichida ro'yxatni ikkiga ajratish va destrukturizatsiya orqali qabul qilish.",
        """Juftlar: [10, 20, 30]
Toqlar: [15, 25]"""
    ),
    (
        440,
        "Funksional DSL: Oddiy SQL WHERE shartlari quruvchisi",
        "Lambda receiver bilan sodda filtrlash ifodalari yaratish.",
        """class SqlConditionBuilder {
    val conditions = mutableListOf<String>()

    infix fun String.eq(value: Any) {
        conditions.add("$this = '$value'")
    }

    infix fun String.gt(value: Number) {
        conditions.add("$this > $value")
    }
}

fun where(block: SqlConditionBuilder.() -> Unit): String {
    val builder = SqlConditionBuilder()
    builder.block()
    return builder.conditions.joinToString(" AND ")
}

fun main() {
    val sqlWhere = where {
        "status" eq "ACTIVE"
        "age" gt 18
    }

    println("WHERE sharti: $sqlWhere")
}""",
        "Infix funksiyalar va lambda with receiver birlashganda to'laqonli SQL DSL hosil bo'ladi.",
        """WHERE sharti: status = 'ACTIVE' AND age > 18"""
    ),
    (
        441,
        "Shaxsiy 'distinctBy' inline funksiyasi",
        "Elementlarning ma'lum bir xususiyati bo'yicha yagonaligini saqlovchi funksiya.",
        """inline fun <T, K> List<T>.customDistinctBy(selector: (T) -> K): List<T> {
    val set = HashSet<K>()
    val list = ArrayList<T>()
    for (e in this) {
        val key = selector(e)
        if (set.add(key)) {
            list.add(e)
        }
    }
    return list
}

data class ClientItem(val id: Int, val name: String)

fun main() {
    val clients = listOf(
        ClientItem(1, "Ali"),
        ClientItem(2, "Vali"),
        ClientItem(1, "Ali (Dublikat)")
    )

    val unique = clients.customDistinctBy { it.id }
    println("Yagona mijozlar: $unique")
}""",
        "'selector' lambdasi bo'yicha kalit olinadi va HashSet orqali tezkor tekshiriladi.",
        """Yagona mijozlar: [ClientItem(id=1, name=Ali), ClientItem(id=2, name=Vali)]"""
    ),
    (
        442,
        "Lambdada istisnolarni xavfsiz boshqarish: catchingTransformer",
        "Transformatsiyada xato yuz berganda dasturni to'xtatmaydigan yuqori tartibli o'ram.",
        """fun <T, R> safeTransform(item: T, transform: (T) -> R): R? {
    return try {
        transform(item)
    } catch (e: Exception) {
        println("[OGOHLANTIRISH]: '${e.message}' xatosi ushlandi")
        null
    }
}

fun main() {
    val s1 = safeTransform("123") { it.toInt() }
    val s2 = safeTransform("abc") { it.toInt() }

    println("Natija 1: $s1")
    println("Natija 2: $s2")
}""",
        "Xatoliklarni ushlab, natijani 'R?' holatida xavfsiz qaytaruvchi funksional o'ram.",
        """Natija 1: 123
[OGOHLANTIRISH]: 'For input string: "abc"' xatosi ushlandi
Natija 2: null"""
    ),
    (
        443,
        "Funksional taqqoslash zanjiri: Multi-Comparator",
        "Bir nechta lambdalar orqali ketma-ket solishtirish.",
        """data class ProductRecord(val category: String, val price: Double, val name: String)

fun main() {
    val products = listOf(
        ProductRecord("Elektronika", 300.0, "Telefon"),
        ProductRecord("Elektronika", 150.0, "Naushnik"),
        ProductRecord("Kiyim", 50.0, "Ko'ylak")
    )

    val sorted = products.sortedWith(
        compareBy<ProductRecord> { it.category }
            .thenBy { it.price }
    )

    sorted.forEach { println("${it.category} | ${it.name} | $$${it.price}") }
}""",
        "'compareBy' va 'thenBy' yuqori tartibli komparatorlari orqali ko'p pog'onali tartiblash.",
        """Elektronika | Naushnik | $150.0
Elektronika | Telefon | $300.0
Kiyim | Ko'ylak | $50.0"""
    ),
    (
        444,
        "Shaxsiy 'maxByOrNull' inline funksiyasi",
        "Berilgan hisoblanuvchi mezon bo'yicha eng katta elementni topuvchi inline funksiya.",
        """inline fun <T, R : Comparable<R>> List<T>.customMaxBy(selector: (T) -> R): T? {
    if (isEmpty()) return null
    var maxElem = this[0]
    var maxValue = selector(maxElem)
    for (i in 1 until size) {
        val e = this[i]
        val v = selector(e)
        if (v > maxValue) {
            maxElem = e
            maxValue = v
        }
    }
    return maxElem
}

fun main() {
    val cities = listOf("Xiva", "Samarqand", "Toshkent", "Buxoro")
    val longestCity = cities.customMaxBy { it.length }
    println("Eng uzun shahar nomi: $longestCity")
}""",
        "Eng katta elementni bitta o'tishda (O(N)) qo'shimcha obyekt ajratmasdan topish.",
        """Eng uzun shahar nomi: Samarqand"""
    ),
    (
        445,
        "Funksional Event Dispatcher (Voqealar tarqatuvchisi)",
        "Voqea turlari bo'yicha lambdalar ro'yxatini saqlovchi va chaqiruvchi tizim.",
        """class EventDispatcher {
    private val handlers = mutableMapOf<String, MutableList<(String) -> Unit>>()

    fun on(event: String, handler: (String) -> Unit) {
        handlers.getOrPut(event) { mutableListOf() }.add(handler)
    }

    fun emit(event: String, payload: String) {
        handlers[event]?.forEach { it(payload) }
    }
}

fun main() {
    val dispatcher = EventDispatcher()
    dispatcher.on("USER_LOGIN") { println("[LOG]: Foydalanuvchi kirdi: $it") }
    dispatcher.on("USER_LOGIN") { println("[NOTIF]: Xush kelibsiz xabari tayyorlandi") }

    dispatcher.emit("USER_LOGIN", "jasur_dev")
}""",
        "Funksiyalar ro'yxati orqali reaktiv hodisalarni boshqarish arxitekturasi.",
        """[LOG]: Foydalanuvchi kirdi: jasur_dev
[NOTIF]: Xush kelibsiz xabari tayyorlandi"""
    ),
    (
        446,
        "Shaxsiy 'all' va 'any' inline funksiyalari",
        "Kolleksiya shartga to'liq mos kelishini yoki kamida bittasi mosligini tekshiruvchi inline funksiyalar.",
        """inline fun <T> List<T>.customAll(predicate: (T) -> Boolean): Boolean {
    for (item in this) if (!predicate(item)) return false
    return true
}

inline fun <T> List<T>.customAny(predicate: (T) -> Boolean): Boolean {
    for (item in this) if (predicate(item)) return true
    return false
}

fun main() {
    val numbers = listOf(2, 4, 6, 8)
    println("Barchasi juftmi: ${numbers.customAll { it % 2 == 0 }}")
    println("7 bormi: ${numbers.customAny { it == 7 }}")
}""",
        "Qisqa tutashuv (short-circuit) bilan birinchi mos kelmagan yoki mos kelgan elementda darhol to'xtash.",
        """Barchasi juftmi: true
7 bormi: false"""
    ),
    (
        447,
        "Funksional Valyuta Hisoblash Pipeline",
        "Narxlarni filtrlovchi, chegirma beruvchi va formatlovchi to'liq funksional quvur.",
        """fun main() {
    val prices = listOf(50.0, 120.0, 30.0, 250.0, 80.0)

    val finalReceipt = prices
        .filter { it >= 50.0 } // Faqat 50 dan kattalari
        .map { it * 0.90 } // 10% chegirma
        .sortedDescending()
        .map { "Narx: $%,.2f".format(it) }

    println("Chegirmali mahsulotlar:")
    finalReceipt.forEach { println(" - $it") }
}""",
        "Standart kutubxona yuqori tartibli funksiyalari orqali ma'lumotlarni o'zgartirish oqimi.",
        """Chegirmali mahsulotlar:
 - Narx: $225.00
 - Narx: $108.00
 - Narx: $72.00
 - Narx: $45.00"""
    ),
    (
        448,
        "Shaxsiy 'count' inline funksiyasi",
        "Berilgan shartga mos keluvchi elementlar sonini sanovchi inline funksiya.",
        """inline fun <T> List<T>.customCount(predicate: (T) -> Boolean): Int {
    var count = 0
    for (item in this) {
        if (predicate(item)) count++
    }
    return count
}

fun main() {
    val words = listOf("Kotlin", "Java", "C++", "Python", "Swift")
    val countLongWords = words.customCount { it.length > 4 }
    println("4 belgidan uzun so'zlar: $countLongWords ta")
}""",
        "Hisoblagichni oshirib boruvchi samarali inline sanagich.",
        """4 belgidan uzun so'zlar: 3 ta"""
    ),
    (
        449,
        "Funksiyalarda yordamchi konfigurator: configure",
        "Obyektni lambda orqali konfiguratsiya qilib qaytaruvchi umumiy generik funksiya.",
        """inline fun <T> configure(target: T, block: T.() -> Unit): T {
    target.block()
    return target
}

class ServerSettings {
    var host: String = ""
    var port: Int = 0
}

fun main() {
    val settings = configure(ServerSettings()) {
        host = "127.0.0.1"
        port = 8080
    }

    println("Server: ${settings.host}:${settings.port}")
}""",
        "Kotlin 'apply' ga o'xshash qulay initsializatsiya andozasi.",
        """Server: 127.0.0.1:8080"""
    ),
    (
        450,
        "Funksional dasturlash va lambdalar bo'yicha to'liq amaliy xulosa: Buyurtmalar Tahlili",
        "Lambdalar, High-order functions, Trailing lambda, typealias, inline, noinline va crossinline imkoniyatlarini bitta yaxlit modulda jamlang.",
        """typealias OrderPredicate = (amount: Double) -> Boolean
typealias ReceiptPrinter = (id: String, finalTotal: Double) -> Unit

inline fun processOrdersPipeline(
    orderIds: List<String>,
    amounts: List<Double>,
    filterRule: OrderPredicate,
    noinline printer: ReceiptPrinter,
    crossinline onComplete: () -> Unit
) {
    println("=== BUYURTMALAR QU VURI BOSHLANDI ===")
    for (i in orderIds.indices) {
        val amount = amounts[i]
        if (filterRule(amount)) {
            val totalWithTax = amount * 1.12 // 12% soliq
            printer(orderIds[i], totalWithTax)
        }
    }
    
    // crossinline callback:
    Thread {
        onComplete()
    }.start()
}

fun main() {
    val ids = listOf("ORD-1", "ORD-2", "ORD-3")
    val amounts = listOf(40.0, 150.0, 80.0)

    val printReceipt: ReceiptPrinter = { id, total ->
        println(" - Buyurtma $id tasdiqlandi: $%,.2f".format(total))
    }

    processOrdersPipeline(
        ids, amounts,
        filterRule = { it >= 50.0 }, // Trailing lambda / predicate
        printer = printReceipt,
        onComplete = { println("Barcha buyurtmalar muvaffaqiyatli ishlandi!") }
    )
    Thread.sleep(100)
}""",
        "Ushbu yakuniy topshiriqda talab qilingan barcha funksional vositalar: Lambdalar, Trailing lambda, typealias ('OrderPredicate', 'ReceiptPrinter'), inline funksiya, noinline parametri va crossinline oqim chaqiruvi to'liq uyg'unlashdi.",
        """=== BUYURTMALAR QU VURI BOSHLANDI ===
 - Buyurtma ORD-2 tasdiqlandi: $168.00
 - Buyurtma ORD-3 tasdiqlandi: $89.60
Barcha buyurtmalar muvaffaqiyatli ishlandi!"""
    )
]

for item in data_09:
    n, title, condition, sol, exp, res = item
    tasks.append(format_task(n, title, condition, sol, exp, res))

save_file("kotlin_09_funksional_dasturlash_va_lambdalar.md", tasks)
