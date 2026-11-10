# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

data_14 = [
    (
        651,
        "Try-Catch ifoda sifatida (Try-Catch as an Expression)",
        "Matnni son ga o'tkazishda 'try-catch' ifodasidan foydalanib, xato holatida standart qiymat biriktiring.",
        """fun parseIntegerSafe(input: String): Int {
    // Kotlinda try-catch qiymat qaytaradi:
    val result: Int = try {
        input.toInt()
    } catch (e: NumberFormatException) {
        -1
    }
    return result
}

fun main() {
    println("Yaroqli: ${parseIntegerSafe("100")}")
    println("Yaroqsiz: ${parseIntegerSafe("abc")}")
}""",
        "Kotlinda 'try-catch' oddiy bayonot (statement) emas, balki qiymat qaytaruvchi ifodadir (expression). 'try' bloki muvaffaqiyatli yakunlansa uning oxirgi qatori, agar istisno yuz bersa 'catch' blokining oxirgi qatori o'zgaruvchiga birikadi.",
        """Yaroqli: 100
Yaroqsiz: -1"""
    ),
    (
        652,
        "Finally bloki va uning qiymat qaytarmaslik qoidasi",
        "'finally' bloki har qanday holatda ham bajarilishi, lekin 'try-catch' ifodasining qaytish qiymatiga ta'sir qilmasligini namoyish qiling.",
        """fun testFinally(): Int {
    return try {
        println("Try bloki bajarildi")
        10
    } catch (e: Exception) {
        println("Catch bloki bajarildi")
        20
    } finally {
        println("Finally bloki har doim bajariladi!")
        // Finally ichidagi oxirgi qiymat qaytish qiymatiga ta'sir qilmaydi!
    }
}

fun main() {
    val value = testFinally()
    println("Qaytarilgan qiymat: $value")
}""",
        "'finally' bloki resurslarni yopish yoki tozalash amallari uchun mo'ljallangan va xatolik bo'lishi yoki bo'lmasligidan qat'i nazar doimo ishga tushadi. Ammo uning ichidagi ifodalar 'try-catch' ifodasining natijaviy qiymatini o'zgartirmaydi.",
        """Try bloki bajarildi
Finally bloki har doim bajariladi!
Qaytarilgan qiymat: 10"""
    ),
    (
        653,
        "Throw ifoda sifatida va Nothing tipi",
        "Elvis operatori bilan birgalikda 'throw' ishlatib, 'Nothing' turining xususiyatini ko'rsating.",
        """fun getRequiredEnv(key: String): String {
    val value: String? = System.getenv(key)
    // throw ifoda bo'lib, Nothing turiga ega:
    return value ?: throw IllegalStateException("Muhit o'zgaruvchisi topilmadi: $key")
}

fun main() {
    try {
        getRequiredEnv("NON_EXISTING_ENV_VAR_2026")
    } catch (e: IllegalStateException) {
        println("Ushlangan istisno: ${e.message}")
    }
}""",
        "Kotlinda 'throw' ham ifoda hisoblanadi va uning turi 'Nothing' dir. 'Nothing' barcha ma'lumot turlarining eng quyi (bottom) subtipi bo'lganligi sababli, 'val name: String = input ?: throw ...' ifodasi 100% tip xavfsizligini ta'minlaydi.",
        """Ushlangan istisno: Muhit o'zgaruvchisi topilmadi: NON_EXISTING_ENV_VAR_2026"""
    ),
    (
        654,
        "Shaxsiy istisno sinfi (Custom Exception)",
        "O'z biznes xatoliklaringiz uchun maxsus xatolik kodiga ega 'CustomException' e'lon qiling.",
        """class InsufficientBalanceException(
    val currentBalance: Double,
    val requestedAmount: Double
) : Exception("Mablag' yetarli emas! Mavjud: $$currentBalance, So'ralgan: $$requestedAmount")

fun withdraw(balance: Double, amount: Double) {
    if (amount > balance) {
        throw InsufficientBalanceException(balance, amount)
    }
    println("Pul yechildi: $$amount")
}

fun main() {
    try {
        withdraw(50.0, 100.0)
    } catch (e: InsufficientBalanceException) {
        println("[XATOLIK]: ${e.message}")
        println("Yetishmayotgan summa: $${e.requestedAmount - e.currentBalance}")
    }
}""",
        "Kotlinda shaxsiy istisnolar 'Exception' yoki 'RuntimeException' dan meros olish orqali yaratiladi. Konstruktorda qo'shimcha biznes maydonlarini (currentBalance, requestedAmount) saqlash xatoni to'g'ri qayta ishlashga yordam beradi.",
        """[XATOLIK]: Mablag' yetarli emas! Mavjud: $50.0, So'ralgan: $100.0
Yetishmayotgan summa: $50.0"""
    ),
    (
        655,
        "Kotlinda Checked Exceptions yo'qligi va falsafasi",
        "Java dagi majburiy 'throws IOException' cheklovi Kotlinda nima uchun yo'qligini tushuntiring.",
        """import java.io.File
import java.io.IOException

fun readFileContent(path: String): String {
    // Java da bu metod 'throws IOException' talab qiladi.
    // Kotlinda barcha istisnolar unchecked (ixtiyoriy ushlanadigan) hisoblanadi:
    val file = File(path)
    if (!file.exists()) throw IOException("Fayl topilmadi: $path")
    return file.readText()
}

fun main() {
    try {
        readFileContent("non_existent_file.txt")
    } catch (e: IOException) {
        println("Fayl xatosi ushlandi: ${e.message}")
    }
}""",
        "Kotlin 'Checked Exceptions' konsepsiyasidan ataylab voz kechgan (C# va zamonaviy tillar kabi). Java dagi majburiy 'throws' va bo'sh 'catch' bloklari kod sifatini pasaytiradi. Kotlinda dasturchi qayerda xatolikni ushlash mantiqiy bo'lsa, o'sha joyda o'z ixtiyori bilan 'try-catch' yozadi.",
        """Fayl xatosi ushlandi: Fayl topilmadi: non_existent_file.txt"""
    ),
    (
        656,
        "Java bilan integratsiya: @Throws annotatsiyasi",
        "Kotlinda yozilgan metoddan Java kodi 'checked exception' ni ushlashi uchun '@Throws' annotatsiyasini qo'llang.",
        """import java.io.IOException

class NetworkClient {
    @Throws(IOException::class)
    fun executeCall(url: String): String {
        if (!url.startsWith("https://")) {
            throw IOException("Xavfsiz ulanish talab etiladi: $url")
        }
        return "200 OK"
    }
}

fun main() {
    val client = NetworkClient()
    try {
        client.executeCall("http://insecure.uz")
    } catch (e: IOException) {
        println("Ushlandi: ${e.message}")
    }
}""",
        "'@Throws(ExceptionClass::class)' annotatsiyasi Kotlin bayt-kodiga Java uchun 'throws ExceptionClass' metod signaturasini qo'shib beradi. Bu Java dasturchilari ushbu metodni chaqirganda kompilyatsiya darajasida xatolikni ushlashini talab qiladi.",
        """Ushlandi: Xavfsiz ulanish talab etiladi: http://insecure.uz"""
    ),
    (
        657,
        "Kotlin Result turi asoslari: runCatching",
        "Xatolik yuz berishi mumkin bo'lgan operatsiyani 'runCatching' orqali o'rab, 'Result<T>' obyektini hosil qiling.",
        """fun divideSafe(a: Int, b: Int): Result<Int> {
    return runCatching { a / b }
}

fun main() {
    val r1 = divideSafe(10, 2)
    val r2 = divideSafe(10, 0)

    println("r1 muvaffaqiyatlimi: ${r1.isSuccess}, qiymat: ${r1.getOrNull()}")
    println("r2 muvaffaqiyatsizmi: ${r2.isFailure}, xato: ${r2.exceptionOrNull()?.message}")
}""",
        "'runCatching { ... }' bloki har qanday 'Throwable' istisnosini ushlab, natijani 'Result<T>' inline qiymat sinfiga joylaydi. Bu istisnolar o'rniga funksional ma'lumotlar bilan ishlash imkonini beradi.",
        """r1 muvaffaqiyatlimi: true, qiymat: 5
r2 muvaffaqiyatsizmi: true, xato: / by zero"""
    ),
    (
        658,
        "Result qiymatini olish: getOrDefault va getOrElse",
        "Muvaffaqiyatsiz operatsiyada standart zaxira qiymat yoki hisoblangan zaxirani olish.",
        """fun main() {
    val failureResult: Result<Int> = runCatching { "not_a_number".toInt() }

    val val1 = failureResult.getOrDefault(0)
    val val2 = failureResult.getOrElse { exception ->
        println("[OGOHLANTIRISH]: '${exception.message}' yuz berdi. 100 qaytarilmoqda.")
        100
    }

    println("getOrDefault: $val1")
    println("getOrElse: $val2")
}""",
        "'getOrDefault' tayyor zaxirani beradi, 'getOrElse' esa xatolik sababini (Throwable) ko'rib chiqib dinamik zaxira qiymat hisoblash imkoniyatini taqdim etadi.",
        """[OGOHLANTIRISH]: 'For input string: "not_a_number"' yuz berdi. 100 qaytarilmoqda.
getOrDefault: 0
getOrElse: 100"""
    ),
    (
        659,
        "Result ustida transformatsiya: map va mapCatching",
        "Muvaffaqiyatli Result ichidagi qiymatni o'zgartirish va transformatsiyadagi yangi xatoliklarni ushlash.",
        """fun main() {
    val successInput: Result<String> = Result.success("150")

    val mapped: Result<Int> = successInput.map { it.toInt() * 2 }
    println("Mapped natija: ${mapped.getOrNull()}")

    val riskyInput: Result<String> = Result.success("abc")
    // mapCatching agar lambda ichida xato bo'lsa, uni ham Failure ga aylantiradi:
    val safeMapped: Result<Int> = riskyInput.mapCatching { it.toInt() * 2 }
    println("safeMapped muvaffaqiyatlimi: ${safeMapped.isSuccess}")
}""",
        "'map' faqat qiymatni o'zgartiradi (agar transformatsiyada xato bo'lsa dastur to'xtaydi), 'mapCatching' esa transformatsiyada yuzaga keladigan har qanday yangi istisnolarni ham 'Result.failure' ga o'rab beradi.",
        """Mapped natija: 300
safeMapped muvaffaqiyatlimi: false"""
    ),
    (
        660,
        "Result ni qayta tiklash: recover va recoverCatching",
        "Muvaffaqiyatsiz Result ni zaxira operatsiyasi orqali yana muvaffaqiyatli holatga keltiring.",
        """fun fetchFromCache(): Result<String> = Result.failure(RuntimeException("Kesh bo'sh"))
fun fetchFromNetwork(): String = "Serverdan yuklangan ma'lumot"

fun main() {
    val finalData = fetchFromCache().recover {
        println("[TIKLASH]: Kesh topilmadi, zaxira tarmoqdan yuklanmoqda...")
        fetchFromNetwork()
    }

    println("Yakuniy ma'lumot: ${finalData.getOrNull()}")
}""",
        "'recover' faqat 'Failure' holatida ishga tushadi va xatolikni bartaraf qilib natijani yangi 'Result.success' ga aylantiradi.",
        """[TIKLASH]: Kesh topilmadi, zaxira tarmoqdan yuklanmoqda...
Yakuniy ma'lumot: Serverdan yuklangan ma'lumot"""
    ),
    (
        661,
        "Result natijasini ajratish: fold metodi",
        "Muvaffaqiyat va xatolik holatlarini bitta 'fold(onSuccess, onFailure)' ifodasi bilan qayta ishlang.",
        """fun main() {
    val result: Result<Double> = runCatching { 100.0 / 4.0 }

    val message = result.fold(
        onSuccess = { value -> "Amal muvaffaqiyatli: $value" },
        onFailure = { error -> "Amal muvaffaqiyatsiz: ${error.message}" }
    )

    println(message)
}""",
        "'fold' metodi Result bilan ishlashning eng toza funksional usuli bo'lib, har ikkala ssenariyni (Success va Failure) bir vaqtning o'zida qamrab oladi.",
        """Amal muvaffaqiyatli: 25.0"""
    ),
    (
        662,
        "Istisnolarni zanjirlash (Exception Chaining / Cause)",
        "Past darajadagi xatolikni ushlab, uni yuqori darajadagi biznes istisnoga 'cause' sifatida o'rab qayta tashlang.",
        """class DatabaseUnavailableException(message: String, cause: Throwable) : Exception(message, cause)

fun connectToDatabase() {
    try {
        throw java.net.ConnectException("Ulanish rad etildi: Port 5432 yopiq")
    } catch (e: java.net.ConnectException) {
        throw DatabaseUnavailableException("Asosiy baza bilan aloqa yo'q!", e)
    }
}

fun main() {
    try {
        connectToDatabase()
    } catch (e: DatabaseUnavailableException) {
        println("Biznes xatosi: ${e.message}")
        println("Asl sababi (Cause): ${e.cause?.message}")
    }
}""",
        "Istisnolarni zanjirlash ('cause' parametri) xatolikning ildiz sababini yo'qotmasdan yuqori qatlamlarga tushunarli biznes xabarlarini yetkazish imkonini beradi.",
        """Biznes xatosi: Asosiy baza bilan aloqa yo'q!
Asl sababi (Cause): Ulanish rad etildi: Port 5432 yopiq"""
    ),
    (
        663,
        "Bir nechta catch bloklari va ularning tartibi",
        "Umumiy Exception dan oldin maxsus aniq istisnolarni tartibli ushlash.",
        """fun processInput(s: String) {
    try {
        val n = s.toInt()
        val res = 100 / n
        println("100 / $n = $res")
    } catch (e: NumberFormatException) {
        println("Format xatosi: Raqam kiriting!")
    } catch (e: ArithmeticException) {
        println("Matematik xato: Nolga bo'lish mumkin emas!")
    } catch (e: Exception) {
        println("Boshqa umumiy xatolik: ${e.message}")
    }
}

fun main() {
    processInput("nol")
    processInput("0")
    processInput("25")
}""",
        "Kotlinda 'catch' bloklari yuqoridan pastga baholanadi. Aniqroq subklass istisnolar doimo umumiy 'Exception' dan yuqorida turishi shart.",
        """Format xatosi: Raqam kiriting!
Matematik xato: Nolga bo'lish mumkin emas!
100 / 25 = 4"""
    ),
    (
        664,
        "Xatoliklarni qayta tashlash (Rethrowing Exceptions)",
        "Xatolikni logga yozib, so'ngra yuqori qatlamlarga qayta uzatish ('throw e').",
        """fun criticalOperation() {
    try {
        throw IllegalStateException("Baza diski to'ldi")
    } catch (e: Exception) {
        println("[MONITORING LOG]: Kritik xato qayd etildi: ${e.message}")
        throw e // Yuqoriga qayta tashlash
    }
}

fun main() {
    try {
        criticalOperation()
    } catch (e: Exception) {
        println("Yuqori daraja boshqaruvchisi xatoni ushladi: ${e.message}")
    }
}""",
        "'throw e' orqali oraliq qatlamda audit/log yozib, xatolikni global xatoliklar boshqaruvchisiga (Global Error Handler) yo'naltirish mumkin.",
        """[MONITORING LOG]: Kritik xato qayd etildi: Baza diski to'ldi
Yuqori daraja boshqaruvchisi xatoni ushladi: Baza diski to'ldi"""
    ),
    (
        665,
        "Parametrlarni qat'iy tekshirish: require va requireNotNull",
        "Argument noto'g'ri bo'lganda 'IllegalArgumentException' tashlovchi standart Kotlin metodlari.",
        """fun registerMember(name: String, age: Int) {
    require(name.isNotBlank()) { "Ism bo'sh bo'lishi mumkin emas!" }
    require(age >= 18) { "A'zolik uchun yosh kamida 18 bo'lishi shart! Kiritildi: $age" }

    println("A'zo qabul qilindi: $name, $age yosh")
}

fun main() {
    registerMember("Olim", 20)
    try {
        registerMember("Botir", 16)
    } catch (e: IllegalArgumentException) {
        println("Validatsiya rad etildi: ${e.message}")
    }
}""",
        "'require(shart) { xabar }' funksiyasi argumentlarni validatsiya qilish uchun Kotlindagi standart shartnoma (precondition) hisoblanadi.",
        """A'zo qabul qilindi: Olim, 20 yosh
Validatsiya rad etildi: A'zolik uchun yosh kamida 18 bo'lishi shart! Kiritildi: 16"""
    ),
    (
        666,
        "Obyekt holatini tekshirish: check va checkNotNull",
        "Sinfning ichki holati noto'g'ri bo'lganda 'IllegalStateException' tashlovchi metodlar.",
        """class FlightBooking {
    var isConfirmed = false

    fun printBoardingPass() {
        check(isConfirmed) { "Chipta tasdiqlanmagan! Avval to'lovni bajaring." }
        println("Chipta chop etildi.")
    }
}

fun main() {
    val booking = FlightBooking()
    try {
        booking.printBoardingPass()
    } catch (e: IllegalStateException) {
        println("Holat xatosi ushlandi: ${e.message}")
    }
}""",
        "'check(shart)' metodi argumentlar uchun emas, balki obyektning o'zining joriy holati amallarni bajarishga tayyorligini tekshirish uchun xizmat qiladi.",
        """Holat xatosi ushlandi: Chipta tasdiqlanmagan! Avval to'lovni bajaring."""
    ),
    (
        667,
        "Kritik to'xtatish: error funksiyasi",
        "Qonuniy ravishda hech qachon yetib kelmasligi kerak bo'lgan kod qismida 'error()' chaqirish.",
        """fun processOrderStatus(statusCode: Int): String {
    return when (statusCode) {
        1 -> "Yangi"
        2 -> "To'langan"
        3 -> "Yopilgan"
        else -> error("Noma'lum status kodi uchradi: $statusCode. Dasturiy xatolik!")
    }
}

fun main() {
    println("Status 1: ${processOrderStatus(1)}")
    try {
        processOrderStatus(99)
    } catch (e: IllegalStateException) {
        println("Kritik xato ushlandi: ${e.message}")
    }
}""",
        "'error(message)' funksiyasi 'throw IllegalStateException(message)' ning qisqa standart shakli bo'lib, 'Nothing' qaytaradi.",
        """Status 1: Yangi
Kritik xato ushlandi: Noma'lum status kodi uchradi: 99. Dasturiy xatolik!"""
    ),
    (
        668,
        "Resurslarni xavfsiz yopish: use funksiyasi",
        "Fayl yoki ulanish bilan ishlashda istisno bo'lsa ham 'close()' chaqirilishini 'use' bilan ta'minlash.",
        """import java.io.StringReader

fun readFirstLine(text: String): String {
    // StringReader AutoCloseable hisoblanadi:
    return StringReader(text).use { reader ->
        reader.readLines().firstOrNull() ?: ""
    }
}

fun main() {
    val content = readFirstLine("Birinchi qator\\nIkkinchi qator")
    println("O'qilgan qator: $content")
}""",
        "'use' bloki Java dagi 'try-with-resources' ning Kotlin analogi bo'lib, xatolik yuz berganda ham resurs xavfsiz yopiladi.",
        """O'qilgan qator: Birinchi qator"""
    ),
    (
        669,
        "Result ro'yxati ustida amallar: Barcha muvaffaqiyatlilarni yig'ish",
        "List<Result<T>> ro'yxatidan faqat muvaffaqiyatli natijalarni ajratib olish.",
        """fun main() {
    val results: List<Result<Int>> = listOf(
        runCatching { "10".toInt() },
        runCatching { "xato".toInt() },
        runCatching { "30".toInt() }
    )

    val successfulValues: List<Int> = results.mapNotNull { it.getOrNull() }

    println("Muvaffaqiyatli qiymatlar: $successfulValues")
}""",
        "'mapNotNull { it.getOrNull() }' xatoliklarni e'tiborsiz qoldirib faqat to'g'ri natijalarni ajratib beradi.",
        """Muvaffaqiyatli qiymatlar: [10, 30]"""
    ),
    (
        670,
        "Shaxsiy xatoliklar iyerarxiyasi: Sealed Class bilan modellashtirish",
        "Istisnolarni tashlamasdan, ma'lumot sifatida qaytaruvchi muhrlangan xatoliklar tuzilmasi.",
        """sealed interface DomainError {
    data class NotFound(val entityId: String) : DomainError
    data class PermissionDenied(val user: String) : DomainError
    data class NetworkTimeout(val durationMs: Long) : DomainError
}

fun fetchUser(id: String): Result<String> {
    return if (id == "001") Result.success("Foydalanuvchi: Alisher")
    else Result.failure(Exception("ID topilmadi"))
}

fun main() {
    val res = fetchUser("999")
    println("Natija muvaffaqiyatlimi: ${res.isSuccess}")
}""",
        "Zamonaviy arxitekturada istisnolar faqat kutilmagan holatlar uchun qoldirilib, biznes xatoliklari 'Result' yoki 'Sealed Class' ma'lumotlari sifatida qaytariladi.",
        """Natija muvaffaqiyatlimi: false"""
    ),
    (
        671,
        "Xatoliklarni tiklash: Result.getOrThrow()",
        "Muvaffaqiyatsiz Result ichidagi asl xatolikni qayta tashlash.",
        """fun main() {
    val res: Result<Int> = runCatching { 10 / 0 }

    try {
        val value = res.getOrThrow()
        println("Qiymat: $value")
    } catch (e: ArithmeticException) {
        println("Asl istisno getOrThrow orqali tashlandi: ${e.message}")
    }
}""",
        "'getOrThrow()' muvaffaqiyatli bo'lsa qiymatni, xato bo'lsa o'sha xatolikni to'g'ridan-to'g'ri otadi.",
        """Asl istisno getOrThrow orqali tashlandi: / by zero"""
    ),
    (
        672,
        "Shartli boshqaruv: Xatoliklarni qayta ishlash zanjiri",
        "Bir nechta bosqichda Result orqali xavfsiz hisoblash.",
        """fun parseDiscount(raw: String): Result<Double> = runCatching { raw.toDouble() }
fun applyTax(amount: Double): Result<Double> = runCatching {
    require(amount >= 0) { "Manfiy narx" }
    amount * 1.12
}

fun main() {
    val finalPrice = parseDiscount("100.0")
        .mapCatching { applyTax(it).getOrThrow() }
        .getOrDefault(0.0)

    println("Yakuniy summa: $$finalPrice")
}""",
        "Zanjirli Result operatsiyalari butun jarayon davomida xatolar yuz bersa darhol to'xtashni kafolatlaydi.",
        """Yakuniy summa: $112.0"""
    ),
    (
        673,
        "Foydalanuvchi kiritishini ko'p qoidali tekshirish",
        "Barcha xatoliklarni bitta ro'yxatga yig'ib foydalanuvchiga taqdim etish.",
        """fun validatePassword(p: String): List<String> {
    val errors = mutableListOf<String>()
    if (p.length < 8) errors.add("Parol kamida 8 belgidan iborat bo'lishi kerak")
    if (p.none { it.isDigit() }) errors.add("Kamida 1 ta raqam bo'lishi kerak")
    if (p.none { it.isUpperCase() }) errors.add("Kamida 1 ta bosh harf bo'lishi kerak")
    return errors
}

fun main() {
    val errs = validatePassword("pass")
    println("Topilgan xatoliklar soni: ${errs.size} ta")
    errs.forEach { println(" - $it") }
}""",
        "Bitta xatoda to'xtamasdan, barcha xatoliklarni to'plab ko'rsatish foydalanuvchi tajribasini (UX) yaxshilaydi.",
        """Topilgan xatoliklar soni: 3 ta
 - Parol kamida 8 belgidan iborat bo'lishi kerak
 - Kamida 1 ta raqam bo'lishi kerak
 - Kamida 1 ta bosh harf bo'lishi kerak"""
    ),
    (
        674,
        "Kritik StackTrace ma'lumotlarini o'qish",
        "Istisnoning stek izini (stack trace) dasturiy ravishda tahlil qilish.",
        """fun produceError() {
    throw RuntimeException("Sinov xatoligi")
}

fun main() {
    try {
        produceError()
    } catch (e: Exception) {
        val topFrame = e.stackTrace.firstOrNull()
        println("Xatolik yuz bergan fayl: ${topFrame?.fileName}, qator: ${topFrame?.lineNumber}")
    }
}""",
        "Disk raskadrovka va telemetriya tizimlarida stack trace orqali xato manzilini aniqlash.",
        """Xatolik yuz bergan fayl: gen_14_xatoliklar.py, qator: ko'rsatiladi."""
    ),
    (
        675,
        "Kotlinda Suppressed Exceptions (Bostirilgan istisnolar)",
        "'use' bloki ichida asosiy xato bilan birga resurs yopilishidagi xatoni ham saqlash.",
        """class FaultyResource : AutoCloseable {
    fun work() { throw RuntimeException("Asosiy ish xatosi") }
    override fun close() { throw IllegalStateException("Yopilishdagi xato") }
}

fun main() {
    try {
        FaultyResource().use { it.work() }
    } catch (e: Exception) {
        println("Bosh xatolik: ${e.message}")
        println("Bostirilgan xatolar: ${e.suppressed.map { it.message }}")
    }
}""",
        "Kotlindaki 'use' bloki Java ning 'try-with-resources' kabi bostirilgan istisnolarni (suppressed exceptions) yo'qotmasdan saqlaydi.",
        """Bosh xatolik: Asosiy ish xatosi
Bostirilgan xatolar: [Yopilishdagi xato]"""
    ),
    (
        676,
        "Shartli tiklash: recover orqali muqobil manbaga o'tish",
        "Birinchi manba xato berganda ikkinchisiga xavfsiz o'tish.",
        """fun main() {
    val result = runCatching {
        throw RuntimeException("Server 1 ishlamadi")
    }.recover {
        "Server 2 muvaffaqiyatli javob berdi"
    }

    println("Natija: ${result.getOrNull()}")
}""",
        "'recover' orqali zaxira serverlarga ulanish juda ixcham amalga oshiriladi.",
        """Natija: Server 2 muvaffaqiyatli javob berdi"""
    ),
    (
        677,
        "Xatoliklarni logga yozish: onFailure va onSuccess metodlari",
        "Result ustida faqat hodisaga mos harakatni bajarish.",
        """fun main() {
    val successRes = Result.success("Ma'lumotlar saqlandi")
    val failRes = Result.failure<String>(IllegalArgumentException("Noto'g'ri parametr"))

    successRes.onSuccess { println("[MUVAFFAQIN]: $it") }
    failRes.onFailure { println("[XATOLIK]: ${it.message}") }
}""",
        "'onSuccess' va 'onFailure' ifodalari kodni toza va o'qishli saqlashda yordam beradi.",
        """[MUVAFFAQIN]: Ma'lumotlar saqlandi
[XATOLIK]: Noto'g'ri parametr"""
    ),
    (
        678,
        "Shaxsiy xatolik konvertori (Exception Translator)",
        "Texnik istisnolarni foydalanuvchiga mos o'zbekcha xabarlarga o'tkazuvchi funksiya.",
        """fun toUserFriendlyMessage(e: Throwable): String {
    return when (e) {
        is java.net.UnknownHostException -> "Internet bilan aloqa mavjud emas."
        is java.net.SocketTimeoutException -> "Server javob berish vaqti tugadi."
        is IllegalArgumentException -> "Kiritilgan ma'lumotlarda xatolik bor: ${e.message}"
        else -> "Tizimda noma'lum xatolik yuz berdi. Keyinroq urinib ko'ring."
    }
}

fun main() {
    println(toUserFriendlyMessage(java.net.UnknownHostException("api.uz")))
    println(toUserFriendlyMessage(IllegalArgumentException("Yosh 0 dan kichik")))
}""",
        "Foydalanuvchiga texnik xatoliklarni (Stack trace) ko'rsatmasdan, xavfsiz va tushunarli o'zbekcha xabarlar berish.",
        """Internet bilan aloqa mavjud emas.
Kiritilgan ma'lumotlarda xatolik bor: Yosh 0 dan kichik"""
    ),
    (
        679,
        "Xatoliklarni chetlab o'tish: ignoreErrors yordamchisi",
        "Muhim bo'lmagan xatoliklarni konsolga log qilib, dasturni to'xtatmaslik.",
        """inline fun ignoreErrors(action: () -> Unit) {
    try {
        action()
    } catch (e: Throwable) {
        println("[E'TIBORSIZ QOLDIRILDI]: ${e.message}")
    }
}

fun main() {
    ignoreErrors {
        println("Vaqtinchalik fayl tozalanmoqda...")
        throw java.io.FileNotFoundException("Fayl topilmadi")
    }
    println("Dastur davom etmoqda.")
}""",
        "Kesh tozalash kabi ikkinchi darajali operatsiyalarda xatoni o'tkazib yuborish.",
        """Vaqtinchalik fayl tozalanmoqda...
[E'TIBORSIZ QOLDIRILDI]: Fayl topilmadi
Dastur davom etmoqda."""
    ),
    (
        680,
        "Result bilan ko'p qadamli hisob-kitob",
        "Har bir qadamda xatoliklarni ushlab yakuniy hisobot chiqarish.",
        """fun main() {
    val calculation = runCatching { "20".toInt() }
        .mapCatching { it * 5 }
        .mapCatching { it / 2 }

    println("Hisoblash: ${calculation.getOrNull()}")
}""",
        "Funksional metodlar zanjiri orqali xavfsiz hisob-kitoblar.",
        """Hisoblash: 50"""
    ),
    (
        681,
        "Xatoliklarni sanash: Error Metrics Tracker",
        "Dasturda yuz bergan xatoliklarni turlari bo'yicha sanab boruvchi sinf.",
        """class ErrorTracker {
    private val errorCounts = mutableMapOf<String, Int>()

    fun record(e: Throwable) {
        val name = e::class.simpleName ?: "Unknown"
        errorCounts[name] = errorCounts.getOrDefault(name, 0) + 1
    }

    fun printStats() {
        println("Xatoliklar statistikasi: $errorCounts")
    }
}

fun main() {
    val tracker = ErrorTracker()
    tracker.record(IllegalArgumentException())
    tracker.record(NullPointerException())
    tracker.record(IllegalArgumentException())

    tracker.printStats()
}""",
        "Tizimda yuz berayotgan xatoliklar chastotasini kuzatib borish.",
        """Xatoliklar statistikasi: {IllegalArgumentException=2, NullPointerException=1}"""
    ),
    (
        682,
        "Shaxsiy Timeout Istisnosi",
        "Amal belgilangan vaqt ichida bajarilmaganda tashlanadigan shaxsiy istisno.",
        """class OperationTimeoutException(val timeoutMs: Long) : Exception("Operatsiya $timeoutMs ms ichida yakunlanmadi!")

fun main() {
    try {
        throw OperationTimeoutException(5000L)
    } catch (e: OperationTimeoutException) {
        println("Vaqt chegarasi xatosi: ${e.message}")
    }
}""",
        "Tarmoq va operatsiyalar chegarasini boshqarish uchun shaxsiy istisno.",
        """Vaqt chegarasi xatosi: Operatsiya 5000 ms ichida yakunlanmadi!"""
    ),
    (
        683,
        "Try-Catch da resurslarni qo'lda tozalash",
        "Oddiy try-finally orqali qulfni (Lock) har doim ochish.",
        """class DummyLock {
    fun lock() = println("Resurs qulflindi")
    fun unlock() = println("Resurs qulfdan chiqarildi")
}

fun main() {
    val l = DummyLock()
    l.lock()
    try {
        println("Xavfsiz operatsiya bajarilmoqda")
    } finally {
        l.unlock()
    }
}""",
        "Ko'p oqimli dasturlashda 'finally { lock.unlock() }' qat'iy qoidadir.",
        """Resurs qulflindi
Xavfsiz operatsiya bajarilmoqda
Resurs qulfdan chiqarildi"""
    ),
    (
        684,
        "Result ichidagi qiymatni tekshirib yangi xato tashlash",
        "Result qiymati biznes shartiga to'g'ri kelmasa uni Failure ga aylantirish.",
        """fun main() {
    val result = runCatching { 45 }
        .mapCatching {
            if (it < 50) throw IllegalArgumentException("Ball 50 dan past bo'lmasligi kerak!")
            it
        }

    println("Muvaffaqiyatlimi: ${result.isSuccess}")
    println("Xatolik: ${result.exceptionOrNull()?.message}")
}""",
        "'mapCatching' ichida 'throw' qilish orqali muvaffaqiyatli Result ni xatolikka aylantirish.",
        """Muvaffaqiyatlimi: false
Xatolik: Ball 50 dan past bo'lmasligi kerak!"""
    ),
    (
        685,
        "Shaxsiy API Status Istisnosi",
        "HTTP status kodlarini o'zida saqlovchi istisno sinfi.",
        """class ApiException(val statusCode: Int, message: String) : Exception("API Xatosi ($statusCode): $message")

fun main() {
    try {
        throw ApiException(404, "Foydalanuvchi topilmadi")
    } catch (e: ApiException) {
        println("Status: ${e.statusCode} | Xabar: ${e.message}")
    }
}""",
        "REST API mijoz dasturlarida status kodlariga ko'ra xatoliklarni boshqarish.",
        """Status: 404 | Xabar: API Xatosi (404): Foydalanuvchi topilmadi"""
    ),
    (
        686,
        "Xatoliklarni ro'yxatga oluvchi xavfsiz Mapper",
        "Kolleksiyadagi har bir elementni o'tkazib, xatolilarini alohida to'plash.",
        """fun <T, R> mapWithErrors(items: List<T>, transform: (T) -> R): Pair<List<R>, List<Throwable>> {
    val successes = mutableListOf<R>()
    val failures = mutableListOf<Throwable>()
    for (item in items) {
        runCatching { transform(item) }
            .onSuccess { successes.add(it) }
            .onFailure { failures.add(it) }
    }
    return Pair(successes, failures)
}

fun main() {
    val raw = listOf("10", "abc", "30", "xyz")
    val (successes, errors) = mapWithErrors(raw) { it.toInt() }

    println("Muvaffaqiyatli sonlar: $successes")
    println("Xatoliklar soni: ${errors.size} ta")
}""",
        "Ommaviy konvertatsiyalarda xatoliklarni yo'qotmasdan ajratib olish.",
        """Muvaffaqiyatli sonlar: [10, 30]
Xatoliklar soni: 2 ta"""
    ),
    (
        687,
        "Kritik xatoliklarda tizimni to'xtatuvchi assert funksiyasi",
        "Rivojlantirish muhitida shart buzilganda darhol xatolik tashlovchi 'assert()'.",
        """fun calculateArea(w: Int, h: Int): Int {
    assert(w > 0 && h > 0) { "Eni va bo'yi musbat bo'lishi shart" }
    return w * h
}

fun main() {
    println("Yuza: ${calculateArea(5, 4)}")
}""",
        "'assert()' JVM da '-ea' parametri bilan ishga tushganda tekshiruv o'tkazadi.",
        """Yuza: 20"""
    ),
    (
        688,
        "Shartli Tiklash: Nullable o'rniga Result ishlatish qulayligi",
        "Nima uchun xato sababi kerak bo'lganda 'null' emas 'Result' tanlanadi.",
        """fun divideVerbose(a: Int, b: Int): Result<Int> {
    return if (b == 0) Result.failure(ArithmeticException("0 ga bo'lish mumkin emas"))
    else Result.success(a / b)
}

fun main() {
    val res = divideVerbose(10, 0)
    println("Nega xato bo'ldi: ${res.exceptionOrNull()?.message}")
}""",
        "Nullable faqat 'yo'q' degan ma'noni beradi, 'Result' esa nima uchun xato bo'lganligini (sababini) saqlaydi.",
        """Nega xato bo'ldi: 0 ga bo'lish mumkin emas"""
    ),
    (
        689,
        "Ko'p xatoliklarni ushlovchi CompositeException analogi",
        "Bir nechta istisnolarni bitta umumiy obyektda birlashtirish.",
        """class CompositeException(val exceptions: List<Throwable>) : Exception("Bir nechta xatolik yuz berdi: ${exceptions.size} ta")

fun main() {
    val errors = listOf(IllegalArgumentException("Ism xato"), IllegalStateException("Baza o'chiq"))
    val composite = CompositeException(errors)

    println(composite.message)
    composite.exceptions.forEach { println(" - ${it::class.simpleName}: ${it.message}") }
}""",
        "Parallel yoki ommaviy operatsiyalarda barcha xatoliklarni bitta paketda yetkazish.",
        """Bir nechta xatolik yuz berdi: 2 ta
 - IllegalArgumentException: Ism xato
 - IllegalStateException: Baza o'chiq"""
    ),
    (
        690,
        "Xatoliklarni qayta ishlashda vaqtinchalik keshdan foydalanish",
        "Result muvaffaqiyatsiz bo'lsa keshdagi eski ma'lumotni olish.",
        """var lastKnownData = "Eski barqaror kesh"

fun fetchFreshData(): Result<String> = Result.failure(RuntimeException("Tarmoq xatosi"))

fun main() {
    val result = fetchFreshData().recover {
        println("[OGOHLANTIRISH]: Yangi ma'lumot yuklanmadi, keshdan olinmoqda")
        lastKnownData
    }

    println("Yakuniy ma'lumot: ${result.getOrNull()}")
}""",
        "Offline-first va barqaror arxitekturada xatoliklarni kesh bilan yumshatish.",
        """[OGOHLANTIRISH]: Yangi ma'lumot yuklanmadi, keshdan olinmoqda
Yakuniy ma'lumot: Eski barqaror kesh"""
    ),
    (
        691,
        "Xatoliklarni tekshiruvchi yordamchi: Result.mapCatching",
        "JSON matnini o'qib, ob'ektga aylantirishdagi xatoliklarni ushlash.",
        """fun main() {
    val rawJson = "{ bad_json }"
    val res = runCatching {
        if (!rawJson.startsWith("{") || !rawJson.contains(":")) {
            throw IllegalArgumentException("JSON formati noto'g'ri")
        }
        "ParsedObject"
    }

    println("Parse muvaffaqiyatlimi: ${res.isSuccess}")
    println("Xato sababi: ${res.exceptionOrNull()?.message}")
}""",
        "Parsing va formatlash operatsiyalarini Result orqali xavfsiz boshqarish.",
        """Parse muvaffaqiyatlimi: false
Xato sababi: JSON formati noto'g'ri"""
    ),
    (
        692,
        "Kritik Xatolik: OutOfMemoryError va VirtualMachineError ni ushlamaslik qoidasi",
        "Nima uchun JVM dagi Fatal xatoliklarni oddiy try-catch da ushlab yashirish xavfli ekanligini tushuntiring.",
        """fun main() {
    // Kotlinda try-catch faqat Exception larni ushlashi kerak, Error larni emas.
    try {
        println("Oddiy operatsiya bajarilmoqda")
    } catch (e: Exception) {
        println("Biznes xatosi ushlandi")
    }
}""",
        "'OutOfMemoryError', 'StackOverflowError' kabi 'VirtualMachineError' lar tizimning jismoniy buzilganligini bildiradi. Ularni 'catch (e: Throwable)' qilib ushlab yashirish dasturning noadekvat holatda qolishiga olib keladi.",
        """Oddiy operatsiya bajarilmoqda"""
    ),
    (
        693,
        "Shaxsiy Validatsiya Istisnosi bilan maydon xatolari",
        "Forma maydonlaridagi xatolarni xaritalash.",
        """class FormValidationException(val fieldErrors: Map<String, String>) : Exception("Formada xatoliklar mavjud")

fun main() {
    try {
        throw FormValidationException(mapOf("email" to "Email formati xato", "phone" to "Raqam kam"))
    } catch (e: FormValidationException) {
        println("${e.message}: ${e.fieldErrors}")
    }
}""",
        "Har bir maydon uchun xatolik matnini saqlovchi maxsus istisno.",
        """Formada xatoliklar mavjud: {email=Email formati xato, phone=Raqam kam}"""
    ),
    (
        694,
        "Result ustida tekshirish: getOrNull va elvis operatori",
        "Result natijasini oddiy Kotlin null-safety operatorlari bilan birlashtirish.",
        """fun main() {
    val result: Result<String> = Result.failure(Exception("Xatolik"))
    val displayName = result.getOrNull() ?: "Standart Foydalanuvchi"

    println("Ko'rinadigan ism: $displayName")
}""",
        "'result.getOrNull() ?:' sintaksisi Result va Elvis operatorlarining eng qulay sintezidir.",
        """Ko'rinadigan ism: Standart Foydalanuvchi"""
    ),
    (
        695,
        "Xatoliklarni ko'p qatlamli uzatish (Layered Exception Architecture)",
        "Database qatlami -> Repository qatlami -> UI qatlami o'rtasida xatoliklarni xavfsiz uzatish.",
        """sealed interface UiResult {
    data class Success(val message: String) : UiResult
    data class Error(val userMessage: String) : UiResult
}

fun fetchUiData(id: Int): UiResult {
    return runCatching {
        if (id <= 0) throw IllegalArgumentException("Yaroqsiz ID")
        "Foydalanuvchi ma'lumotlari #$id"
    }.fold(
        onSuccess = { UiResult.Success(it) },
        onFailure = { UiResult.Error("Ma'lumot yuklab bo'lmadi: ${it.message}") }
    )
}

fun main() {
    println(fetchUiData(10))
    println(fetchUiData(-1))
}""",
        "Qatlamlar orasida texnik xatoliklarni to'g'ridan-to'g'ri 'UiResult' ga o'tkazish Clean Architecture talablariga mos keladi.",
        """Success(message=Foydalanuvchi ma'lumotlari #10)
Error(userMessage=Ma'lumot yuklab bo'lmadi: Yaroqsiz ID)"""
    ),
    (
        696,
        "Shartli Tiklash: recoverCatching bilan zaxira operatsiyasidagi xatoni ham ushlash",
        "Zaxira amali ham xatolik berganda butun jarayonni Failure da saqlash.",
        """fun main() {
    val res = runCatching {
        throw RuntimeException("1-manba xato")
    }.recoverCatching {
        throw IllegalStateException("Zaxira manba ham xato berdi")
    }

    println("Yakuniy muvaffaqiyatlimi: ${res.isSuccess}")
    println("Oxirgi xatolik: ${res.exceptionOrNull()?.message}")
}""",
        "'recoverCatching' tiklash jarayonida yuz beradigan yangi istisnolarni ham xavfsiz ushlaydi.",
        """Yakuniy muvaffaqiyatlimi: false
Oxirgi xatolik: Zaxira manba ham xato berdi"""
    ),
    (
        697,
        "Xatoliklarni sanash va chegaralash: Circuit Breaker analogi",
        "Ketma-ket xatoliklar soni oshib ketganda so'rovlarni to'xtatish.",
        """class SimpleCircuitBreaker(val failureThreshold: Int = 3) {
    var failures = 0
    val isOpen: Boolean get() = failures >= failureThreshold

    fun recordFailure() { failures++ }
    fun reset() { failures = 0 }
}

fun main() {
    val breaker = SimpleCircuitBreaker(2)
    breaker.recordFailure()
    println("Ochiqmi: ${breaker.isOpen}")
    breaker.recordFailure()
    println("Ochiqmi (limitga yetdi): ${breaker.isOpen}")
}""",
        "Circuit Breaker andozasi orqali beqaror servislarni doimiy so'rovlar bilan qiynamaslik ta'minlanadi.",
        """Ochiqmi: false
Ochiqmi (limitga yetdi): true"""
    ),
    (
        698,
        "Result qiymati bilan if-else o'rnida when qo'llash",
        "Result ustida 'when' tekshiruvini qulay shakllantirish.",
        """fun main() {
    val res: Result<String> = Result.success("Muvaffaqiyatli Ma'lumot")

    when {
        res.isSuccess -> println("Natija: ${res.getOrNull()}")
        res.isFailure -> println("Xato: ${res.exceptionOrNull()?.message}")
    }
}""",
        "'when' yordamida Result holatini tahlil qilish.",
        """Natija: Muvaffaqiyatli Ma'lumot"""
    ),
    (
        699,
        "Resurslarni bir nechta 'use' orqali zanjirlash",
        "Ikki resursni ketma-ket xavfsiz ochish va yopish.",
        """import java.io.StringReader
import java.io.StringWriter

fun main() {
    StringReader("Salom").use { reader ->
        StringWriter().use { writer ->
            writer.write(reader.readText().uppercase())
            println("Natija: ${writer.toString()}")
        }
    }
}""",
        "Ikki va undan ortiq resurslarni bir vaqtning o'zida 'use' bilan xavfsiz boshqarish.",
        """Natija: SALOM"""
    ),
    (
        700,
        "Xatoliklarni boshqarish bo'yicha to'liq amaliy xulosa: To'lov Tranzaksiyalari Gateway",
        "try-catch ifodasi, throw, Nothing, custom exceptions, runCatching, Result (map, recover, fold) va use ni bitta professional to'lov shlyuzi misolida jamlang.",
        """class PaymentException(val errorCode: String, message: String) : Exception(message)

data class TransactionReceipt(val txId: String, val amount: Double, val status: String)

class PaymentGateway {
    fun processPayment(card: String, amount: Double): Result<TransactionReceipt> {
        return runCatching {
            require(card.length == 16) { "Karta raqami 16 xonali bo'lishi shart!" }
            require(amount > 0) { "To'lov summasi musbat bo'lishi shart!" }
            
            if (amount > 10_000_000.0) {
                throw PaymentException("LIMIT_EXCEEDED", "Bir martalik to'lov limiti (10 mln) oshib ketdi!")
            }
            
            TransactionReceipt("TX-998877", amount, "MUVAFFAQIN")
        }
    }
}

fun main() {
    val gateway = PaymentGateway()

    // 1. Muvaffaqiyatli tranzaksiya
    val r1 = gateway.processPayment("8600123456789900", 150_000.0)
    
    // 2. Limitdan oshgan tranzaksiya va recover orqali zaxiraga o'tish
    val r2 = gateway.processPayment("8600123456789900", 25_000_000.0)
        .recover { error ->
            println("[RECOVER]: Limit xatosi ushlandi (${error.message}). Zaxira limitga tushirildi.")
            TransactionReceipt("TX-BACKUP", 10_000_000.0, "ZAXIRA_TASDIQLANDI")
        }

    fun handleReceipt(res: Result<TransactionReceipt>) {
        res.fold(
            onSuccess = { println("Chek tayyor: ID=${it.txId}, Summa=%,.0f UZS, Holat=${it.status}".format(it.amount)) },
            onFailure = { println("To'lov butunlay rad etildi: ${it.message}") }
        )
    }

    println("=== TO'LOV 1 NATIJASI ===")
    handleReceipt(r1)

    println("=== TO'LOV 2 NATIJASI ===")
    handleReceipt(r2)
}""",
        "Ushbu yakuniy topshiriqda talab qilingan barcha xatoliklarni boshqarish vositalari: 'require' validatsiyasi, Shaxsiy istisno ('PaymentException'), 'runCatching', 'Result' qaytishi, 'recover' bilan xatolikni tuzatish va 'fold' bilan yakuniy chek chiqarish to'liq professional to'lov shlyuzida birlashtirildi.",
        """=== TO'LOV 1 NATIJASI ===
Chek tayyor: ID=TX-998877, Summa=150,000 UZS, Holat=MUVAFFAQIN
=== TO'LOV 2 NATIJASI ===
[RECOVER]: Limit xatosi ushlandi (Bir martalik to'lov limiti (10 mln) oshib ketdi!). Zaxira limitga tushirildi.
Chek tayyor: ID=TX-BACKUP, Summa=10,000,000 UZS, Holat=ZAXIRA_TASDIQLANDI"""
    )
]

for item in data_14:
    n, title, condition, sol, exp, res = item
    tasks.append(format_task(n, title, condition, sol, exp, res))

save_file("kotlin_14_xatoliklarni_boshqarish_exceptions.md", tasks)
