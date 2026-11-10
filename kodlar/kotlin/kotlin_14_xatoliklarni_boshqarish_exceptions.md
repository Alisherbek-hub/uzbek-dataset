# 651-Topshiriq: Try-Catch ifoda sifatida (Try-Catch as an Expression)
## Topshiriq sharti:
Matnni son ga o'tkazishda 'try-catch' ifodasidan foydalanib, xato holatida standart qiymat biriktiring.

## Yechim (Kotlin kodi):
```kotlin
fun parseIntegerSafe(input: String): Int {
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
}
```

## Tushuntirish va Mantiq:
Kotlinda 'try-catch' oddiy bayonot (statement) emas, balki qiymat qaytaruvchi ifodadir (expression). 'try' bloki muvaffaqiyatli yakunlansa uning oxirgi qatori, agar istisno yuz bersa 'catch' blokining oxirgi qatori o'zgaruvchiga birikadi.

## Ishlash natijasi:
```text
Yaroqli: 100
Yaroqsiz: -1
```


# 652-Topshiriq: Finally bloki va uning qiymat qaytarmaslik qoidasi
## Topshiriq sharti:
'finally' bloki har qanday holatda ham bajarilishi, lekin 'try-catch' ifodasining qaytish qiymatiga ta'sir qilmasligini namoyish qiling.

## Yechim (Kotlin kodi):
```kotlin
fun testFinally(): Int {
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
}
```

## Tushuntirish va Mantiq:
'finally' bloki resurslarni yopish yoki tozalash amallari uchun mo'ljallangan va xatolik bo'lishi yoki bo'lmasligidan qat'i nazar doimo ishga tushadi. Ammo uning ichidagi ifodalar 'try-catch' ifodasining natijaviy qiymatini o'zgartirmaydi.

## Ishlash natijasi:
```text
Try bloki bajarildi
Finally bloki har doim bajariladi!
Qaytarilgan qiymat: 10
```


# 653-Topshiriq: Throw ifoda sifatida va Nothing tipi
## Topshiriq sharti:
Elvis operatori bilan birgalikda 'throw' ishlatib, 'Nothing' turining xususiyatini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
fun getRequiredEnv(key: String): String {
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
}
```

## Tushuntirish va Mantiq:
Kotlinda 'throw' ham ifoda hisoblanadi va uning turi 'Nothing' dir. 'Nothing' barcha ma'lumot turlarining eng quyi (bottom) subtipi bo'lganligi sababli, 'val name: String = input ?: throw ...' ifodasi 100% tip xavfsizligini ta'minlaydi.

## Ishlash natijasi:
```text
Ushlangan istisno: Muhit o'zgaruvchisi topilmadi: NON_EXISTING_ENV_VAR_2026
```


# 654-Topshiriq: Shaxsiy istisno sinfi (Custom Exception)
## Topshiriq sharti:
O'z biznes xatoliklaringiz uchun maxsus xatolik kodiga ega 'CustomException' e'lon qiling.

## Yechim (Kotlin kodi):
```kotlin
class InsufficientBalanceException(
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
}
```

## Tushuntirish va Mantiq:
Kotlinda shaxsiy istisnolar 'Exception' yoki 'RuntimeException' dan meros olish orqali yaratiladi. Konstruktorda qo'shimcha biznes maydonlarini (currentBalance, requestedAmount) saqlash xatoni to'g'ri qayta ishlashga yordam beradi.

## Ishlash natijasi:
```text
[XATOLIK]: Mablag' yetarli emas! Mavjud: $50.0, So'ralgan: $100.0
Yetishmayotgan summa: $50.0
```


# 655-Topshiriq: Kotlinda Checked Exceptions yo'qligi va falsafasi
## Topshiriq sharti:
Java dagi majburiy 'throws IOException' cheklovi Kotlinda nima uchun yo'qligini tushuntiring.

## Yechim (Kotlin kodi):
```kotlin
import java.io.File
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
}
```

## Tushuntirish va Mantiq:
Kotlin 'Checked Exceptions' konsepsiyasidan ataylab voz kechgan (C# va zamonaviy tillar kabi). Java dagi majburiy 'throws' va bo'sh 'catch' bloklari kod sifatini pasaytiradi. Kotlinda dasturchi qayerda xatolikni ushlash mantiqiy bo'lsa, o'sha joyda o'z ixtiyori bilan 'try-catch' yozadi.

## Ishlash natijasi:
```text
Fayl xatosi ushlandi: Fayl topilmadi: non_existent_file.txt
```


# 656-Topshiriq: Java bilan integratsiya: @Throws annotatsiyasi
## Topshiriq sharti:
Kotlinda yozilgan metoddan Java kodi 'checked exception' ni ushlashi uchun '@Throws' annotatsiyasini qo'llang.

## Yechim (Kotlin kodi):
```kotlin
import java.io.IOException

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
}
```

## Tushuntirish va Mantiq:
'@Throws(ExceptionClass::class)' annotatsiyasi Kotlin bayt-kodiga Java uchun 'throws ExceptionClass' metod signaturasini qo'shib beradi. Bu Java dasturchilari ushbu metodni chaqirganda kompilyatsiya darajasida xatolikni ushlashini talab qiladi.

## Ishlash natijasi:
```text
Ushlandi: Xavfsiz ulanish talab etiladi: http://insecure.uz
```


# 657-Topshiriq: Kotlin Result turi asoslari: runCatching
## Topshiriq sharti:
Xatolik yuz berishi mumkin bo'lgan operatsiyani 'runCatching' orqali o'rab, 'Result<T>' obyektini hosil qiling.

## Yechim (Kotlin kodi):
```kotlin
fun divideSafe(a: Int, b: Int): Result<Int> {
    return runCatching { a / b }
}

fun main() {
    val r1 = divideSafe(10, 2)
    val r2 = divideSafe(10, 0)

    println("r1 muvaffaqiyatlimi: ${r1.isSuccess}, qiymat: ${r1.getOrNull()}")
    println("r2 muvaffaqiyatsizmi: ${r2.isFailure}, xato: ${r2.exceptionOrNull()?.message}")
}
```

## Tushuntirish va Mantiq:
'runCatching { ... }' bloki har qanday 'Throwable' istisnosini ushlab, natijani 'Result<T>' inline qiymat sinfiga joylaydi. Bu istisnolar o'rniga funksional ma'lumotlar bilan ishlash imkonini beradi.

## Ishlash natijasi:
```text
r1 muvaffaqiyatlimi: true, qiymat: 5
r2 muvaffaqiyatsizmi: true, xato: / by zero
```


# 658-Topshiriq: Result qiymatini olish: getOrDefault va getOrElse
## Topshiriq sharti:
Muvaffaqiyatsiz operatsiyada standart zaxira qiymat yoki hisoblangan zaxirani olish.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val failureResult: Result<Int> = runCatching { "not_a_number".toInt() }

    val val1 = failureResult.getOrDefault(0)
    val val2 = failureResult.getOrElse { exception ->
        println("[OGOHLANTIRISH]: '${exception.message}' yuz berdi. 100 qaytarilmoqda.")
        100
    }

    println("getOrDefault: $val1")
    println("getOrElse: $val2")
}
```

## Tushuntirish va Mantiq:
'getOrDefault' tayyor zaxirani beradi, 'getOrElse' esa xatolik sababini (Throwable) ko'rib chiqib dinamik zaxira qiymat hisoblash imkoniyatini taqdim etadi.

## Ishlash natijasi:
```text
[OGOHLANTIRISH]: 'For input string: "not_a_number"' yuz berdi. 100 qaytarilmoqda.
getOrDefault: 0
getOrElse: 100
```


# 659-Topshiriq: Result ustida transformatsiya: map va mapCatching
## Topshiriq sharti:
Muvaffaqiyatli Result ichidagi qiymatni o'zgartirish va transformatsiyadagi yangi xatoliklarni ushlash.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val successInput: Result<String> = Result.success("150")

    val mapped: Result<Int> = successInput.map { it.toInt() * 2 }
    println("Mapped natija: ${mapped.getOrNull()}")

    val riskyInput: Result<String> = Result.success("abc")
    // mapCatching agar lambda ichida xato bo'lsa, uni ham Failure ga aylantiradi:
    val safeMapped: Result<Int> = riskyInput.mapCatching { it.toInt() * 2 }
    println("safeMapped muvaffaqiyatlimi: ${safeMapped.isSuccess}")
}
```

## Tushuntirish va Mantiq:
'map' faqat qiymatni o'zgartiradi (agar transformatsiyada xato bo'lsa dastur to'xtaydi), 'mapCatching' esa transformatsiyada yuzaga keladigan har qanday yangi istisnolarni ham 'Result.failure' ga o'rab beradi.

## Ishlash natijasi:
```text
Mapped natija: 300
safeMapped muvaffaqiyatlimi: false
```


# 660-Topshiriq: Result ni qayta tiklash: recover va recoverCatching
## Topshiriq sharti:
Muvaffaqiyatsiz Result ni zaxira operatsiyasi orqali yana muvaffaqiyatli holatga keltiring.

## Yechim (Kotlin kodi):
```kotlin
fun fetchFromCache(): Result<String> = Result.failure(RuntimeException("Kesh bo'sh"))
fun fetchFromNetwork(): String = "Serverdan yuklangan ma'lumot"

fun main() {
    val finalData = fetchFromCache().recover {
        println("[TIKLASH]: Kesh topilmadi, zaxira tarmoqdan yuklanmoqda...")
        fetchFromNetwork()
    }

    println("Yakuniy ma'lumot: ${finalData.getOrNull()}")
}
```

## Tushuntirish va Mantiq:
'recover' faqat 'Failure' holatida ishga tushadi va xatolikni bartaraf qilib natijani yangi 'Result.success' ga aylantiradi.

## Ishlash natijasi:
```text
[TIKLASH]: Kesh topilmadi, zaxira tarmoqdan yuklanmoqda...
Yakuniy ma'lumot: Serverdan yuklangan ma'lumot
```


# 661-Topshiriq: Result natijasini ajratish: fold metodi
## Topshiriq sharti:
Muvaffaqiyat va xatolik holatlarini bitta 'fold(onSuccess, onFailure)' ifodasi bilan qayta ishlang.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val result: Result<Double> = runCatching { 100.0 / 4.0 }

    val message = result.fold(
        onSuccess = { value -> "Amal muvaffaqiyatli: $value" },
        onFailure = { error -> "Amal muvaffaqiyatsiz: ${error.message}" }
    )

    println(message)
}
```

## Tushuntirish va Mantiq:
'fold' metodi Result bilan ishlashning eng toza funksional usuli bo'lib, har ikkala ssenariyni (Success va Failure) bir vaqtning o'zida qamrab oladi.

## Ishlash natijasi:
```text
Amal muvaffaqiyatli: 25.0
```


# 662-Topshiriq: Istisnolarni zanjirlash (Exception Chaining / Cause)
## Topshiriq sharti:
Past darajadagi xatolikni ushlab, uni yuqori darajadagi biznes istisnoga 'cause' sifatida o'rab qayta tashlang.

## Yechim (Kotlin kodi):
```kotlin
class DatabaseUnavailableException(message: String, cause: Throwable) : Exception(message, cause)

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
}
```

## Tushuntirish va Mantiq:
Istisnolarni zanjirlash ('cause' parametri) xatolikning ildiz sababini yo'qotmasdan yuqori qatlamlarga tushunarli biznes xabarlarini yetkazish imkonini beradi.

## Ishlash natijasi:
```text
Biznes xatosi: Asosiy baza bilan aloqa yo'q!
Asl sababi (Cause): Ulanish rad etildi: Port 5432 yopiq
```


# 663-Topshiriq: Bir nechta catch bloklari va ularning tartibi
## Topshiriq sharti:
Umumiy Exception dan oldin maxsus aniq istisnolarni tartibli ushlash.

## Yechim (Kotlin kodi):
```kotlin
fun processInput(s: String) {
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
}
```

## Tushuntirish va Mantiq:
Kotlinda 'catch' bloklari yuqoridan pastga baholanadi. Aniqroq subklass istisnolar doimo umumiy 'Exception' dan yuqorida turishi shart.

## Ishlash natijasi:
```text
Format xatosi: Raqam kiriting!
Matematik xato: Nolga bo'lish mumkin emas!
100 / 25 = 4
```


# 664-Topshiriq: Xatoliklarni qayta tashlash (Rethrowing Exceptions)
## Topshiriq sharti:
Xatolikni logga yozib, so'ngra yuqori qatlamlarga qayta uzatish ('throw e').

## Yechim (Kotlin kodi):
```kotlin
fun criticalOperation() {
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
}
```

## Tushuntirish va Mantiq:
'throw e' orqali oraliq qatlamda audit/log yozib, xatolikni global xatoliklar boshqaruvchisiga (Global Error Handler) yo'naltirish mumkin.

## Ishlash natijasi:
```text
[MONITORING LOG]: Kritik xato qayd etildi: Baza diski to'ldi
Yuqori daraja boshqaruvchisi xatoni ushladi: Baza diski to'ldi
```


# 665-Topshiriq: Parametrlarni qat'iy tekshirish: require va requireNotNull
## Topshiriq sharti:
Argument noto'g'ri bo'lganda 'IllegalArgumentException' tashlovchi standart Kotlin metodlari.

## Yechim (Kotlin kodi):
```kotlin
fun registerMember(name: String, age: Int) {
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
}
```

## Tushuntirish va Mantiq:
'require(shart) { xabar }' funksiyasi argumentlarni validatsiya qilish uchun Kotlindagi standart shartnoma (precondition) hisoblanadi.

## Ishlash natijasi:
```text
A'zo qabul qilindi: Olim, 20 yosh
Validatsiya rad etildi: A'zolik uchun yosh kamida 18 bo'lishi shart! Kiritildi: 16
```


# 666-Topshiriq: Obyekt holatini tekshirish: check va checkNotNull
## Topshiriq sharti:
Sinfning ichki holati noto'g'ri bo'lganda 'IllegalStateException' tashlovchi metodlar.

## Yechim (Kotlin kodi):
```kotlin
class FlightBooking {
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
}
```

## Tushuntirish va Mantiq:
'check(shart)' metodi argumentlar uchun emas, balki obyektning o'zining joriy holati amallarni bajarishga tayyorligini tekshirish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Holat xatosi ushlandi: Chipta tasdiqlanmagan! Avval to'lovni bajaring.
```


# 667-Topshiriq: Kritik to'xtatish: error funksiyasi
## Topshiriq sharti:
Qonuniy ravishda hech qachon yetib kelmasligi kerak bo'lgan kod qismida 'error()' chaqirish.

## Yechim (Kotlin kodi):
```kotlin
fun processOrderStatus(statusCode: Int): String {
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
}
```

## Tushuntirish va Mantiq:
'error(message)' funksiyasi 'throw IllegalStateException(message)' ning qisqa standart shakli bo'lib, 'Nothing' qaytaradi.

## Ishlash natijasi:
```text
Status 1: Yangi
Kritik xato ushlandi: Noma'lum status kodi uchradi: 99. Dasturiy xatolik!
```


# 668-Topshiriq: Resurslarni xavfsiz yopish: use funksiyasi
## Topshiriq sharti:
Fayl yoki ulanish bilan ishlashda istisno bo'lsa ham 'close()' chaqirilishini 'use' bilan ta'minlash.

## Yechim (Kotlin kodi):
```kotlin
import java.io.StringReader

fun readFirstLine(text: String): String {
    // StringReader AutoCloseable hisoblanadi:
    return StringReader(text).use { reader ->
        reader.readLines().firstOrNull() ?: ""
    }
}

fun main() {
    val content = readFirstLine("Birinchi qator\nIkkinchi qator")
    println("O'qilgan qator: $content")
}
```

## Tushuntirish va Mantiq:
'use' bloki Java dagi 'try-with-resources' ning Kotlin analogi bo'lib, xatolik yuz berganda ham resurs xavfsiz yopiladi.

## Ishlash natijasi:
```text
O'qilgan qator: Birinchi qator
```


# 669-Topshiriq: Result ro'yxati ustida amallar: Barcha muvaffaqiyatlilarni yig'ish
## Topshiriq sharti:
List<Result<T>> ro'yxatidan faqat muvaffaqiyatli natijalarni ajratib olish.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val results: List<Result<Int>> = listOf(
        runCatching { "10".toInt() },
        runCatching { "xato".toInt() },
        runCatching { "30".toInt() }
    )

    val successfulValues: List<Int> = results.mapNotNull { it.getOrNull() }

    println("Muvaffaqiyatli qiymatlar: $successfulValues")
}
```

## Tushuntirish va Mantiq:
'mapNotNull { it.getOrNull() }' xatoliklarni e'tiborsiz qoldirib faqat to'g'ri natijalarni ajratib beradi.

## Ishlash natijasi:
```text
Muvaffaqiyatli qiymatlar: [10, 30]
```


# 670-Topshiriq: Shaxsiy xatoliklar iyerarxiyasi: Sealed Class bilan modellashtirish
## Topshiriq sharti:
Istisnolarni tashlamasdan, ma'lumot sifatida qaytaruvchi muhrlangan xatoliklar tuzilmasi.

## Yechim (Kotlin kodi):
```kotlin
sealed interface DomainError {
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
}
```

## Tushuntirish va Mantiq:
Zamonaviy arxitekturada istisnolar faqat kutilmagan holatlar uchun qoldirilib, biznes xatoliklari 'Result' yoki 'Sealed Class' ma'lumotlari sifatida qaytariladi.

## Ishlash natijasi:
```text
Natija muvaffaqiyatlimi: false
```


# 671-Topshiriq: Xatoliklarni tiklash: Result.getOrThrow()
## Topshiriq sharti:
Muvaffaqiyatsiz Result ichidagi asl xatolikni qayta tashlash.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val res: Result<Int> = runCatching { 10 / 0 }

    try {
        val value = res.getOrThrow()
        println("Qiymat: $value")
    } catch (e: ArithmeticException) {
        println("Asl istisno getOrThrow orqali tashlandi: ${e.message}")
    }
}
```

## Tushuntirish va Mantiq:
'getOrThrow()' muvaffaqiyatli bo'lsa qiymatni, xato bo'lsa o'sha xatolikni to'g'ridan-to'g'ri otadi.

## Ishlash natijasi:
```text
Asl istisno getOrThrow orqali tashlandi: / by zero
```


# 672-Topshiriq: Shartli boshqaruv: Xatoliklarni qayta ishlash zanjiri
## Topshiriq sharti:
Bir nechta bosqichda Result orqali xavfsiz hisoblash.

## Yechim (Kotlin kodi):
```kotlin
fun parseDiscount(raw: String): Result<Double> = runCatching { raw.toDouble() }
fun applyTax(amount: Double): Result<Double> = runCatching {
    require(amount >= 0) { "Manfiy narx" }
    amount * 1.12
}

fun main() {
    val finalPrice = parseDiscount("100.0")
        .mapCatching { applyTax(it).getOrThrow() }
        .getOrDefault(0.0)

    println("Yakuniy summa: $$finalPrice")
}
```

## Tushuntirish va Mantiq:
Zanjirli Result operatsiyalari butun jarayon davomida xatolar yuz bersa darhol to'xtashni kafolatlaydi.

## Ishlash natijasi:
```text
Yakuniy summa: $112.0
```


# 673-Topshiriq: Foydalanuvchi kiritishini ko'p qoidali tekshirish
## Topshiriq sharti:
Barcha xatoliklarni bitta ro'yxatga yig'ib foydalanuvchiga taqdim etish.

## Yechim (Kotlin kodi):
```kotlin
fun validatePassword(p: String): List<String> {
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
}
```

## Tushuntirish va Mantiq:
Bitta xatoda to'xtamasdan, barcha xatoliklarni to'plab ko'rsatish foydalanuvchi tajribasini (UX) yaxshilaydi.

## Ishlash natijasi:
```text
Topilgan xatoliklar soni: 3 ta
 - Parol kamida 8 belgidan iborat bo'lishi kerak
 - Kamida 1 ta raqam bo'lishi kerak
 - Kamida 1 ta bosh harf bo'lishi kerak
```


# 674-Topshiriq: Kritik StackTrace ma'lumotlarini o'qish
## Topshiriq sharti:
Istisnoning stek izini (stack trace) dasturiy ravishda tahlil qilish.

## Yechim (Kotlin kodi):
```kotlin
fun produceError() {
    throw RuntimeException("Sinov xatoligi")
}

fun main() {
    try {
        produceError()
    } catch (e: Exception) {
        val topFrame = e.stackTrace.firstOrNull()
        println("Xatolik yuz bergan fayl: ${topFrame?.fileName}, qator: ${topFrame?.lineNumber}")
    }
}
```

## Tushuntirish va Mantiq:
Disk raskadrovka va telemetriya tizimlarida stack trace orqali xato manzilini aniqlash.

## Ishlash natijasi:
```text
Xatolik yuz bergan fayl: gen_14_xatoliklar.py, qator: ko'rsatiladi.
```


# 675-Topshiriq: Kotlinda Suppressed Exceptions (Bostirilgan istisnolar)
## Topshiriq sharti:
'use' bloki ichida asosiy xato bilan birga resurs yopilishidagi xatoni ham saqlash.

## Yechim (Kotlin kodi):
```kotlin
class FaultyResource : AutoCloseable {
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
}
```

## Tushuntirish va Mantiq:
Kotlindaki 'use' bloki Java ning 'try-with-resources' kabi bostirilgan istisnolarni (suppressed exceptions) yo'qotmasdan saqlaydi.

## Ishlash natijasi:
```text
Bosh xatolik: Asosiy ish xatosi
Bostirilgan xatolar: [Yopilishdagi xato]
```


# 676-Topshiriq: Shartli tiklash: recover orqali muqobil manbaga o'tish
## Topshiriq sharti:
Birinchi manba xato berganda ikkinchisiga xavfsiz o'tish.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val result = runCatching {
        throw RuntimeException("Server 1 ishlamadi")
    }.recover {
        "Server 2 muvaffaqiyatli javob berdi"
    }

    println("Natija: ${result.getOrNull()}")
}
```

## Tushuntirish va Mantiq:
'recover' orqali zaxira serverlarga ulanish juda ixcham amalga oshiriladi.

## Ishlash natijasi:
```text
Natija: Server 2 muvaffaqiyatli javob berdi
```


# 677-Topshiriq: Xatoliklarni logga yozish: onFailure va onSuccess metodlari
## Topshiriq sharti:
Result ustida faqat hodisaga mos harakatni bajarish.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val successRes = Result.success("Ma'lumotlar saqlandi")
    val failRes = Result.failure<String>(IllegalArgumentException("Noto'g'ri parametr"))

    successRes.onSuccess { println("[MUVAFFAQIN]: $it") }
    failRes.onFailure { println("[XATOLIK]: ${it.message}") }
}
```

## Tushuntirish va Mantiq:
'onSuccess' va 'onFailure' ifodalari kodni toza va o'qishli saqlashda yordam beradi.

## Ishlash natijasi:
```text
[MUVAFFAQIN]: Ma'lumotlar saqlandi
[XATOLIK]: Noto'g'ri parametr
```


# 678-Topshiriq: Shaxsiy xatolik konvertori (Exception Translator)
## Topshiriq sharti:
Texnik istisnolarni foydalanuvchiga mos o'zbekcha xabarlarga o'tkazuvchi funksiya.

## Yechim (Kotlin kodi):
```kotlin
fun toUserFriendlyMessage(e: Throwable): String {
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
}
```

## Tushuntirish va Mantiq:
Foydalanuvchiga texnik xatoliklarni (Stack trace) ko'rsatmasdan, xavfsiz va tushunarli o'zbekcha xabarlar berish.

## Ishlash natijasi:
```text
Internet bilan aloqa mavjud emas.
Kiritilgan ma'lumotlarda xatolik bor: Yosh 0 dan kichik
```


# 679-Topshiriq: Xatoliklarni chetlab o'tish: ignoreErrors yordamchisi
## Topshiriq sharti:
Muhim bo'lmagan xatoliklarni konsolga log qilib, dasturni to'xtatmaslik.

## Yechim (Kotlin kodi):
```kotlin
inline fun ignoreErrors(action: () -> Unit) {
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
}
```

## Tushuntirish va Mantiq:
Kesh tozalash kabi ikkinchi darajali operatsiyalarda xatoni o'tkazib yuborish.

## Ishlash natijasi:
```text
Vaqtinchalik fayl tozalanmoqda...
[E'TIBORSIZ QOLDIRILDI]: Fayl topilmadi
Dastur davom etmoqda.
```


# 680-Topshiriq: Result bilan ko'p qadamli hisob-kitob
## Topshiriq sharti:
Har bir qadamda xatoliklarni ushlab yakuniy hisobot chiqarish.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val calculation = runCatching { "20".toInt() }
        .mapCatching { it * 5 }
        .mapCatching { it / 2 }

    println("Hisoblash: ${calculation.getOrNull()}")
}
```

## Tushuntirish va Mantiq:
Funksional metodlar zanjiri orqali xavfsiz hisob-kitoblar.

## Ishlash natijasi:
```text
Hisoblash: 50
```


# 681-Topshiriq: Xatoliklarni sanash: Error Metrics Tracker
## Topshiriq sharti:
Dasturda yuz bergan xatoliklarni turlari bo'yicha sanab boruvchi sinf.

## Yechim (Kotlin kodi):
```kotlin
class ErrorTracker {
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
}
```

## Tushuntirish va Mantiq:
Tizimda yuz berayotgan xatoliklar chastotasini kuzatib borish.

## Ishlash natijasi:
```text
Xatoliklar statistikasi: {IllegalArgumentException=2, NullPointerException=1}
```


# 682-Topshiriq: Shaxsiy Timeout Istisnosi
## Topshiriq sharti:
Amal belgilangan vaqt ichida bajarilmaganda tashlanadigan shaxsiy istisno.

## Yechim (Kotlin kodi):
```kotlin
class OperationTimeoutException(val timeoutMs: Long) : Exception("Operatsiya $timeoutMs ms ichida yakunlanmadi!")

fun main() {
    try {
        throw OperationTimeoutException(5000L)
    } catch (e: OperationTimeoutException) {
        println("Vaqt chegarasi xatosi: ${e.message}")
    }
}
```

## Tushuntirish va Mantiq:
Tarmoq va operatsiyalar chegarasini boshqarish uchun shaxsiy istisno.

## Ishlash natijasi:
```text
Vaqt chegarasi xatosi: Operatsiya 5000 ms ichida yakunlanmadi!
```


# 683-Topshiriq: Try-Catch da resurslarni qo'lda tozalash
## Topshiriq sharti:
Oddiy try-finally orqali qulfni (Lock) har doim ochish.

## Yechim (Kotlin kodi):
```kotlin
class DummyLock {
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
}
```

## Tushuntirish va Mantiq:
Ko'p oqimli dasturlashda 'finally { lock.unlock() }' qat'iy qoidadir.

## Ishlash natijasi:
```text
Resurs qulflindi
Xavfsiz operatsiya bajarilmoqda
Resurs qulfdan chiqarildi
```


# 684-Topshiriq: Result ichidagi qiymatni tekshirib yangi xato tashlash
## Topshiriq sharti:
Result qiymati biznes shartiga to'g'ri kelmasa uni Failure ga aylantirish.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val result = runCatching { 45 }
        .mapCatching {
            if (it < 50) throw IllegalArgumentException("Ball 50 dan past bo'lmasligi kerak!")
            it
        }

    println("Muvaffaqiyatlimi: ${result.isSuccess}")
    println("Xatolik: ${result.exceptionOrNull()?.message}")
}
```

## Tushuntirish va Mantiq:
'mapCatching' ichida 'throw' qilish orqali muvaffaqiyatli Result ni xatolikka aylantirish.

## Ishlash natijasi:
```text
Muvaffaqiyatlimi: false
Xatolik: Ball 50 dan past bo'lmasligi kerak!
```


# 685-Topshiriq: Shaxsiy API Status Istisnosi
## Topshiriq sharti:
HTTP status kodlarini o'zida saqlovchi istisno sinfi.

## Yechim (Kotlin kodi):
```kotlin
class ApiException(val statusCode: Int, message: String) : Exception("API Xatosi ($statusCode): $message")

fun main() {
    try {
        throw ApiException(404, "Foydalanuvchi topilmadi")
    } catch (e: ApiException) {
        println("Status: ${e.statusCode} | Xabar: ${e.message}")
    }
}
```

## Tushuntirish va Mantiq:
REST API mijoz dasturlarida status kodlariga ko'ra xatoliklarni boshqarish.

## Ishlash natijasi:
```text
Status: 404 | Xabar: API Xatosi (404): Foydalanuvchi topilmadi
```


# 686-Topshiriq: Xatoliklarni ro'yxatga oluvchi xavfsiz Mapper
## Topshiriq sharti:
Kolleksiyadagi har bir elementni o'tkazib, xatolilarini alohida to'plash.

## Yechim (Kotlin kodi):
```kotlin
fun <T, R> mapWithErrors(items: List<T>, transform: (T) -> R): Pair<List<R>, List<Throwable>> {
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
}
```

## Tushuntirish va Mantiq:
Ommaviy konvertatsiyalarda xatoliklarni yo'qotmasdan ajratib olish.

## Ishlash natijasi:
```text
Muvaffaqiyatli sonlar: [10, 30]
Xatoliklar soni: 2 ta
```


# 687-Topshiriq: Kritik xatoliklarda tizimni to'xtatuvchi assert funksiyasi
## Topshiriq sharti:
Rivojlantirish muhitida shart buzilganda darhol xatolik tashlovchi 'assert()'.

## Yechim (Kotlin kodi):
```kotlin
fun calculateArea(w: Int, h: Int): Int {
    assert(w > 0 && h > 0) { "Eni va bo'yi musbat bo'lishi shart" }
    return w * h
}

fun main() {
    println("Yuza: ${calculateArea(5, 4)}")
}
```

## Tushuntirish va Mantiq:
'assert()' JVM da '-ea' parametri bilan ishga tushganda tekshiruv o'tkazadi.

## Ishlash natijasi:
```text
Yuza: 20
```


# 688-Topshiriq: Shartli Tiklash: Nullable o'rniga Result ishlatish qulayligi
## Topshiriq sharti:
Nima uchun xato sababi kerak bo'lganda 'null' emas 'Result' tanlanadi.

## Yechim (Kotlin kodi):
```kotlin
fun divideVerbose(a: Int, b: Int): Result<Int> {
    return if (b == 0) Result.failure(ArithmeticException("0 ga bo'lish mumkin emas"))
    else Result.success(a / b)
}

fun main() {
    val res = divideVerbose(10, 0)
    println("Nega xato bo'ldi: ${res.exceptionOrNull()?.message}")
}
```

## Tushuntirish va Mantiq:
Nullable faqat 'yo'q' degan ma'noni beradi, 'Result' esa nima uchun xato bo'lganligini (sababini) saqlaydi.

## Ishlash natijasi:
```text
Nega xato bo'ldi: 0 ga bo'lish mumkin emas
```


# 689-Topshiriq: Ko'p xatoliklarni ushlovchi CompositeException analogi
## Topshiriq sharti:
Bir nechta istisnolarni bitta umumiy obyektda birlashtirish.

## Yechim (Kotlin kodi):
```kotlin
class CompositeException(val exceptions: List<Throwable>) : Exception("Bir nechta xatolik yuz berdi: ${exceptions.size} ta")

fun main() {
    val errors = listOf(IllegalArgumentException("Ism xato"), IllegalStateException("Baza o'chiq"))
    val composite = CompositeException(errors)

    println(composite.message)
    composite.exceptions.forEach { println(" - ${it::class.simpleName}: ${it.message}") }
}
```

## Tushuntirish va Mantiq:
Parallel yoki ommaviy operatsiyalarda barcha xatoliklarni bitta paketda yetkazish.

## Ishlash natijasi:
```text
Bir nechta xatolik yuz berdi: 2 ta
 - IllegalArgumentException: Ism xato
 - IllegalStateException: Baza o'chiq
```


# 690-Topshiriq: Xatoliklarni qayta ishlashda vaqtinchalik keshdan foydalanish
## Topshiriq sharti:
Result muvaffaqiyatsiz bo'lsa keshdagi eski ma'lumotni olish.

## Yechim (Kotlin kodi):
```kotlin
var lastKnownData = "Eski barqaror kesh"

fun fetchFreshData(): Result<String> = Result.failure(RuntimeException("Tarmoq xatosi"))

fun main() {
    val result = fetchFreshData().recover {
        println("[OGOHLANTIRISH]: Yangi ma'lumot yuklanmadi, keshdan olinmoqda")
        lastKnownData
    }

    println("Yakuniy ma'lumot: ${result.getOrNull()}")
}
```

## Tushuntirish va Mantiq:
Offline-first va barqaror arxitekturada xatoliklarni kesh bilan yumshatish.

## Ishlash natijasi:
```text
[OGOHLANTIRISH]: Yangi ma'lumot yuklanmadi, keshdan olinmoqda
Yakuniy ma'lumot: Eski barqaror kesh
```


# 691-Topshiriq: Xatoliklarni tekshiruvchi yordamchi: Result.mapCatching
## Topshiriq sharti:
JSON matnini o'qib, ob'ektga aylantirishdagi xatoliklarni ushlash.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val rawJson = "{ bad_json }"
    val res = runCatching {
        if (!rawJson.startsWith("{") || !rawJson.contains(":")) {
            throw IllegalArgumentException("JSON formati noto'g'ri")
        }
        "ParsedObject"
    }

    println("Parse muvaffaqiyatlimi: ${res.isSuccess}")
    println("Xato sababi: ${res.exceptionOrNull()?.message}")
}
```

## Tushuntirish va Mantiq:
Parsing va formatlash operatsiyalarini Result orqali xavfsiz boshqarish.

## Ishlash natijasi:
```text
Parse muvaffaqiyatlimi: false
Xato sababi: JSON formati noto'g'ri
```


# 692-Topshiriq: Kritik Xatolik: OutOfMemoryError va VirtualMachineError ni ushlamaslik qoidasi
## Topshiriq sharti:
Nima uchun JVM dagi Fatal xatoliklarni oddiy try-catch da ushlab yashirish xavfli ekanligini tushuntiring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    // Kotlinda try-catch faqat Exception larni ushlashi kerak, Error larni emas.
    try {
        println("Oddiy operatsiya bajarilmoqda")
    } catch (e: Exception) {
        println("Biznes xatosi ushlandi")
    }
}
```

## Tushuntirish va Mantiq:
'OutOfMemoryError', 'StackOverflowError' kabi 'VirtualMachineError' lar tizimning jismoniy buzilganligini bildiradi. Ularni 'catch (e: Throwable)' qilib ushlab yashirish dasturning noadekvat holatda qolishiga olib keladi.

## Ishlash natijasi:
```text
Oddiy operatsiya bajarilmoqda
```


# 693-Topshiriq: Shaxsiy Validatsiya Istisnosi bilan maydon xatolari
## Topshiriq sharti:
Forma maydonlaridagi xatolarni xaritalash.

## Yechim (Kotlin kodi):
```kotlin
class FormValidationException(val fieldErrors: Map<String, String>) : Exception("Formada xatoliklar mavjud")

fun main() {
    try {
        throw FormValidationException(mapOf("email" to "Email formati xato", "phone" to "Raqam kam"))
    } catch (e: FormValidationException) {
        println("${e.message}: ${e.fieldErrors}")
    }
}
```

## Tushuntirish va Mantiq:
Har bir maydon uchun xatolik matnini saqlovchi maxsus istisno.

## Ishlash natijasi:
```text
Formada xatoliklar mavjud: {email=Email formati xato, phone=Raqam kam}
```


# 694-Topshiriq: Result ustida tekshirish: getOrNull va elvis operatori
## Topshiriq sharti:
Result natijasini oddiy Kotlin null-safety operatorlari bilan birlashtirish.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val result: Result<String> = Result.failure(Exception("Xatolik"))
    val displayName = result.getOrNull() ?: "Standart Foydalanuvchi"

    println("Ko'rinadigan ism: $displayName")
}
```

## Tushuntirish va Mantiq:
'result.getOrNull() ?:' sintaksisi Result va Elvis operatorlarining eng qulay sintezidir.

## Ishlash natijasi:
```text
Ko'rinadigan ism: Standart Foydalanuvchi
```


# 695-Topshiriq: Xatoliklarni ko'p qatlamli uzatish (Layered Exception Architecture)
## Topshiriq sharti:
Database qatlami -> Repository qatlami -> UI qatlami o'rtasida xatoliklarni xavfsiz uzatish.

## Yechim (Kotlin kodi):
```kotlin
sealed interface UiResult {
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
}
```

## Tushuntirish va Mantiq:
Qatlamlar orasida texnik xatoliklarni to'g'ridan-to'g'ri 'UiResult' ga o'tkazish Clean Architecture talablariga mos keladi.

## Ishlash natijasi:
```text
Success(message=Foydalanuvchi ma'lumotlari #10)
Error(userMessage=Ma'lumot yuklab bo'lmadi: Yaroqsiz ID)
```


# 696-Topshiriq: Shartli Tiklash: recoverCatching bilan zaxira operatsiyasidagi xatoni ham ushlash
## Topshiriq sharti:
Zaxira amali ham xatolik berganda butun jarayonni Failure da saqlash.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val res = runCatching {
        throw RuntimeException("1-manba xato")
    }.recoverCatching {
        throw IllegalStateException("Zaxira manba ham xato berdi")
    }

    println("Yakuniy muvaffaqiyatlimi: ${res.isSuccess}")
    println("Oxirgi xatolik: ${res.exceptionOrNull()?.message}")
}
```

## Tushuntirish va Mantiq:
'recoverCatching' tiklash jarayonida yuz beradigan yangi istisnolarni ham xavfsiz ushlaydi.

## Ishlash natijasi:
```text
Yakuniy muvaffaqiyatlimi: false
Oxirgi xatolik: Zaxira manba ham xato berdi
```


# 697-Topshiriq: Xatoliklarni sanash va chegaralash: Circuit Breaker analogi
## Topshiriq sharti:
Ketma-ket xatoliklar soni oshib ketganda so'rovlarni to'xtatish.

## Yechim (Kotlin kodi):
```kotlin
class SimpleCircuitBreaker(val failureThreshold: Int = 3) {
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
}
```

## Tushuntirish va Mantiq:
Circuit Breaker andozasi orqali beqaror servislarni doimiy so'rovlar bilan qiynamaslik ta'minlanadi.

## Ishlash natijasi:
```text
Ochiqmi: false
Ochiqmi (limitga yetdi): true
```


# 698-Topshiriq: Result qiymati bilan if-else o'rnida when qo'llash
## Topshiriq sharti:
Result ustida 'when' tekshiruvini qulay shakllantirish.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val res: Result<String> = Result.success("Muvaffaqiyatli Ma'lumot")

    when {
        res.isSuccess -> println("Natija: ${res.getOrNull()}")
        res.isFailure -> println("Xato: ${res.exceptionOrNull()?.message}")
    }
}
```

## Tushuntirish va Mantiq:
'when' yordamida Result holatini tahlil qilish.

## Ishlash natijasi:
```text
Natija: Muvaffaqiyatli Ma'lumot
```


# 699-Topshiriq: Resurslarni bir nechta 'use' orqali zanjirlash
## Topshiriq sharti:
Ikki resursni ketma-ket xavfsiz ochish va yopish.

## Yechim (Kotlin kodi):
```kotlin
import java.io.StringReader
import java.io.StringWriter

fun main() {
    StringReader("Salom").use { reader ->
        StringWriter().use { writer ->
            writer.write(reader.readText().uppercase())
            println("Natija: ${writer.toString()}")
        }
    }
}
```

## Tushuntirish va Mantiq:
Ikki va undan ortiq resurslarni bir vaqtning o'zida 'use' bilan xavfsiz boshqarish.

## Ishlash natijasi:
```text
Natija: SALOM
```


# 700-Topshiriq: Xatoliklarni boshqarish bo'yicha to'liq amaliy xulosa: To'lov Tranzaksiyalari Gateway
## Topshiriq sharti:
try-catch ifodasi, throw, Nothing, custom exceptions, runCatching, Result (map, recover, fold) va use ni bitta professional to'lov shlyuzi misolida jamlang.

## Yechim (Kotlin kodi):
```kotlin
class PaymentException(val errorCode: String, message: String) : Exception(message)

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
}
```

## Tushuntirish va Mantiq:
Ushbu yakuniy topshiriqda talab qilingan barcha xatoliklarni boshqarish vositalari: 'require' validatsiyasi, Shaxsiy istisno ('PaymentException'), 'runCatching', 'Result' qaytishi, 'recover' bilan xatolikni tuzatish va 'fold' bilan yakuniy chek chiqarish to'liq professional to'lov shlyuzida birlashtirildi.

## Ishlash natijasi:
```text
=== TO'LOV 1 NATIJASI ===
Chek tayyor: ID=TX-998877, Summa=150,000 UZS, Holat=MUVAFFAQIN
=== TO'LOV 2 NATIJASI ===
[RECOVER]: Limit xatosi ushlandi (Bir martalik to'lov limiti (10 mln) oshib ketdi!). Zaxira limitga tushirildi.
Chek tayyor: ID=TX-BACKUP, Summa=10,000,000 UZS, Holat=ZAXIRA_TASDIQLANDI
```

