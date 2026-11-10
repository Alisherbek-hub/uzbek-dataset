# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

data_03 = [
    (
        101,
        "If ifoda sifatida (If as an Expression)",
        "Kotlinda ternar operatori (? :) o'rniga 'if-else' ifodasidan foydalanib ikki sonning kattasini toping.",
        """fun main() {
    val a = 15
    val b = 28
    
    // Java dagi 'a > b ? a : b' o'rniga Kotlinda:
    val max = if (a > b) a else b
    
    println("a = $a, b = $b")
    println("Kattasi: $max")
}""",
        "Kotlinda an'anaviy ternar operatori 'condition ? then : else' mavjud emas, chunki oddiy 'if' bayonot (statement) emas, balki ifoda (expression) sifatida qiymat qaytara oladi. Bu til sintaksisini ixcham va bir xil uslubda saqlaydi.",
        """a = 15, b = 28
Kattasi: 28"""
    ),
    (
        102,
        "Ko'p qatorli If ifodasi va blokdan qiymat qaytishi",
        "Murakkab if-else blokida hisoblashlar va logging o'tkazib, har bir blokning oxirgi qatoridagi qiymatni o'zgaruvchiga biriktiring.",
        """fun main() {
    val score = 88
    
    val grade = if (score >= 90) {
        println("[BAHOLASH]: A'lo natija qayd etildi")
        "A"
    } else if (score >= 80) {
        println("[BAHOLASH]: Yaxshi natija qayd etildi")
        "B"
    } else if (score >= 70) {
        println("[BAHOLASH]: Qoniqarli natija qayd etildi")
        "C"
    } else {
        println("[BAHOLASH]: Qoniqarsiz natija")
        "F"
    }
    
    println("Talabaning yakuniy bahosi: $grade")
}""",
        "Kotlinda agar 'if' bloki bir nechta satrlardan iborat bo'lsa, o'sha blokning eng oxirgi qatoridagi ifoda uning natijaviy qaytish qiymati hisoblanadi. Hech qanday 'return' so'zi yozilmaydi.",
        """[BAHOLASH]: Yaxshi natija qayd etildi
Talabaning yakuniy bahosi: B"""
    ),
    (
        103,
        "When ifodasi asoslari (Oddiy qiymatlarni solishtirish)",
        "Hafta kuni raqamiga (1..7) qarab kun nomini qaytaruvchi 'when' ifodasini yozing.",
        """fun getDayName(dayNumber: Int): String {
    return when (dayNumber) {
        1 -> "Dushanba"
        2 -> "Seshanba"
        3 -> "Chorshanba"
        4 -> "Payshanba"
        5 -> "Juma"
        6 -> "Shanba"
        7 -> "Yakshanba"
        else -> "Noto'g'ri kun raqami"
    }
}

fun main() {
    println("3-kun: ${getDayName(3)}")
    println("5-kun: ${getDayName(5)}")
    println("9-kun: ${getDayName(9)}")
}""",
        "Kotlindagi 'when' Java ning 'switch' operatorini to'liq almashtiradi va undan ancha qudratlidir. Har bir shoxobchadan keyin 'break' yozish shart emas, mos kelgan shoxobcha bajarilgach 'when' darhol yakunlanadi.",
        """3-kun: Chorshanba
5-kun: Juma
9-kun: Noto'g'ri kun raqami"""
    ),
    (
        104,
        "Bir nechta shartlarni bitta shoxobchada birlashtirish",
        "Dam olish kunlari va ish kunlarini vergul bilan ajratilgan shartlar orqali aniqlang.",
        """fun checkDayType(day: String): String {
    return when (day.lowercase()) {
        "shanba", "yakshanba" -> "Dam olish kuni"
        "dushanba", "seshanba", "chorshanba", "payshanba", "juma" -> "Ish kuni"
        else -> "Noma'lum kun"
    }
}

fun main() {
    println("Juma: ${checkDayType("Juma")}")
    println("Yakshanba: ${checkDayType("Yakshanba")}")
    println("Bayram: ${checkDayType("Bayram")}")
}""",
        "'when' shoxobchasida bir nechta qiymatlarni vergul ',' bilan ajratib ko'rsatish mumkin. Agar berilgan argument sanab o'tilgan qiymatlardan birontasiga teng bo'lsa, o'sha blok ishga tushadi.",
        """Juma: Ish kuni
Yakshanba: Dam olish kuni
Bayram: Noma'lum kun"""
    ),
    (
        105,
        "When va oraliqlar (Range matching with 'in')",
        "Foydalanuvchining yoshiga qarab uning ijtimoiy toifasini 'in 0..12' kabi diapazonlar yordamida aniqlang.",
        """fun categorizeAge(age: Int): String {
    return when (age) {
        in 0..2 -> "Chaqaloq"
        in 3..6 -> "Bog'cha yoshi"
        in 7..17 -> "Maktab o'quvchisi"
        in 18..29 -> "Talaba / Yoshlar"
        in 30..60 -> "Katta yoshli"
        in 61..120 -> "Nuroniy"
        else -> "Yaroqsiz yosh"
    }
}

fun main() {
    println("5 yosh: ${categorizeAge(5)}")
    println("21 yosh: ${categorizeAge(21)}")
    println("65 yosh: ${categorizeAge(65)}")
}""",
        "'in min..max' operatori qiymatning berilgan oraliqqa tegishli ekanligini tekshiradi. Kotlinda 'when' ichida bunday tekshiruvlar kodni juda toza va tabiiy o'qiladigan holatga keltiradi.",
        """5 yosh: Bog'cha yoshi
21 yosh: Talaba / Yoshlar
65 yosh: Nuroniy"""
    ),
    (
        106,
        "When va tur tekshiruvi (Type checking with 'is')",
        "Har xil turdagi obyektlarni tahlil qilib, ularning turiga mos amallarni bajaring va smart cast imkoniyatini ko'ring.",
        """fun describeData(data: Any): String {
    return when (data) {
        is String -> "Satr, belgilar soni: ${data.length}"
        is Int -> "Butun son, 2 karra kattasi: ${data * 2}"
        is Double -> "O'nlik son, yaxlitlangani: ${Math.round(data)}"
        is List<*> -> "Ro'yxat, elementlar soni: ${data.size}"
        else -> "Boshqa tur: ${data::class.simpleName}"
    }
}

fun main() {
    println(describeData("Kotlin dasturlash"))
    println(describeData(25))
    println(describeData(14.8))
    println(describeData(listOf(1, 2, 3, 4)))
}""",
        "'is Type' tekshiruvi orqali 'when' blokida obyektning turi aniqlanadi. Mos kelgan shoxobcha ichida o'zgaruvchi avtomatik ravishda o'sha turga Smart Cast bo'ladi, masalan 'data.length' yoki 'data.size' to'g'ridan-to'g'ri chaqiriladi.",
        """Satr, belgilar soni: 17
Butun son, 2 karra kattasi: 50
O'nlik son, yaxlitlangani: 15
Ro'yxat, elementlar soni: 4"""
    ),
    (
        107,
        "Argumentsiz When ifodasi (When without argument)",
        "Hech qanday argument uzatmasdan, bir nechta mustaqil mantiqiy shartlarni tekshiruvchi 'when' yozing.",
        """fun assessWeather(temp: Double, isRaining: Boolean): String {
    return when {
        temp < 0 && isRaining -> "Muzlama va qor aralash yomg'ir! Ehtiyot bo'ling."
        temp < 0 -> "Sovuq ayozli havo, qalin kiyining."
        isRaining -> "Iliq yomg'ir yog'moqda, soyabon oling."
        temp > 35 -> "Juda issiq havo, ko'proq suv iching."
        else -> "Yoqimli me'yoriy ob-havo."
    }
}

fun main() {
    println(assessWeather(-2.0, true))
    println(assessWeather(18.0, true))
    println(assessWeather(24.0, false))
}""",
        "Argumentsiz 'when' (ya'ni 'when { ... }') Kotlinda 'if - else if - else' konstruksiyasining to'liq va o'qishga oson o'rnini bosuvchi usuldir. Har bir shoxobcha ixtiyoriy boolean ifodani o'z ichiga oladi.",
        """Muzlama va qor aralash yomg'ir! Ehtiyot bo'ling.
Iliq yomg'ir yog'moqda, soyabon oling.
Yoqimli me'yoriy ob-havo."""
    ),
    (
        108,
        "When ichida mahalliy o'zgaruvchi e'lon qilish",
        "Kotlin 1.3+ da kiritilgan 'when (val x = ...)' sintaksisi yordamida hisoblangan qiymatni faqat 'when' doirasida saqlang.",
        """fun processApiResponse(responseCode: Int): String {
    return when (val statusFamily = responseCode / 100) {
        2 -> "Muvaffaqiyatli ($responseCode): 2xx oilasi"
        3 -> "Qayta yo'naltirish ($responseCode): 3xx oilasi"
        4 -> "Mijoz xatoligi ($responseCode): 4xx oilasi"
        5 -> "Server xatoligi ($responseCode): 5xx oilasi"
        else -> "Noma'lum status oilasi: $statusFamily"
    }
}

fun main() {
    println(processApiResponse(200))
    println(processApiResponse(404))
    println(processApiResponse(503))
}""",
        "'when (val x = expression)' sintaksisi hisoblangan natijani faqat shu 'when' bloki ichida ko'rinadigan o'zgaruvchiga biriktiradi. Bu global yoki tashqi doirada keraksiz o'zgaruvchilar paydo bo'lishining oldini oladi.",
        """Muvaffaqiyatli (200): 2xx oilasi
Mijoz xatoligi (404): 4xx oilasi
Server xatoligi (503): 5xx oilasi"""
    ),
    (
        109,
        "Yopiq oraliq bo'yicha For sikli (Closed Range ..)",
        "1 dan 5 gacha bo'lgan barcha sonlar kvadratini '..' operatori orqali chop eting.",
        """fun main() {
    println("1 dan 5 gacha kvadratlar:")
    for (i in 1..5) {
        val square = i * i
        println("$i ning kvadrati: $square")
    }
}""",
        "'1..5' yopiq oraliq (closed range) yaratadi, ya'ni ikkala chegara ham (1 va 5) siklga to'liq kiritiladi. 'for (i in range)' Kotlinda massiv indekslarisiz xatosiz va toza sikl aylanishini ta'minlaydi.",
        """1 dan 5 gacha kvadratlar:
1 ning kvadrati: 1
2 ning kvadrati: 4
3 ning kvadrati: 9
4 ning kvadrati: 16
5 ning kvadrati: 25"""
    ),
    (
        110,
        "Yarim ochiq oraliq: 'until' operatori",
        "Oxirgi qiymatni hisobga olmagan holda 0 dan 5 gacha aylanuvchi sikl yarating.",
        """fun main() {
    println("0 until 5 sikli:")
    for (i in 0 until 5) {
        print("$i ")
    }
    println()
}""",
        "'until' operatori yarim ochiq oraliq (half-open range) hosil qiladi: '[start, end)'. Masalan, '0 until 5' da sonlar 0, 1, 2, 3, 4 bo'ladi, 5 esa kirmaydi. Bu 0-indeksli massivlar bilan ishlashda ayniqsa mos keladi.",
        """0 until 5 sikli:
0 1 2 3 4"""
    ),
    (
        111,
        "Kamayish tartibidagi sikl: 'downTo' operatori",
        "10 dan 1 gacha teskari sanovchi sikl tuzing.",
        """fun main() {
    println("Teskari hisoblash boshlandi:")
    for (i in 5 downTo 1) {
        println("Qolgan vaqt: $i...")
    }
    println("Start!")
}""",
        "Kotlinda kamayish tartibidagi sikl uchun '5..1' deb yozib bo'lmaydi (chunki standart diapazon faqat o'sish tartibida ishlaydi). Buning o'rniga maxsus 'downTo' infix funksiyasi qo'llaniladi.",
        """Teskari hisoblash boshlandi:
Qolgan vaqt: 5...
Qolgan vaqt: 4...
Qolgan vaqt: 3...
Qolgan vaqt: 2...
Qolgan vaqt: 1...
Start!"""
    ),
    (
        112,
        "Qadam bilan sakrash: 'step' operatori",
        "1 dan 20 gacha bo'lgan toq sonlarni 'step 2' orqali ekranga chiqaring.",
        """fun main() {
    print("Toq sonlar: ")
    for (i in 1..15 step 2) {
        print("$i ")
    }
    println()
    
    print("Teskari qadam: ")
    for (i in 20 downTo 10 step 3) {
        print("$i ")
    }
    println()
}""",
        "'step N' operatori sikl hisoblagichining har qadamda nechtaga o'zgarishini belgilaydi. Uni '..' hamda 'downTo' bilan birgalikda ishlatish mumkin.",
        """Toq sonlar: 1 3 5 7 9 11 13 15 
Teskari qadam: 20 17 14 11"""
    ),
    (
        113,
        "Belgilar diapazoni (Char Ranges)",
        "Ingliz alifbosidagi bosh harflarni 'A'..'Z' oralig'i orqali aylanib chiqish dasturini tuzing.",
        """fun main() {
    print("Alifbo harflari (har 4-harf): ")
    for (ch in 'A'..'Z' step 4) {
        print("$ch ")
    }
    println()
    
    val target = 'K'
    println("'$target' harfi 'A'..'Z' oralig'idami: ${target in 'A'..'Z'}")
}""",
        "Kotlinda harflar (Char) ham 'Comparable' bo'lganligi sababli 'A'..'Z' shaklida qonuniy diapazon tashkil etadi. Bu belgilar bilan ishlashda va validatsiyada nihoyatda qulaydir.",
        """Alifbo harflari (har 4-harf): A E I M Q U Y 
'K' harfi 'A'..'Z' oralig'idami: true"""
    ),
    (
        114,
        "Ro'yxat indekslari bo'yicha For sikli (indices)",
        "Kolleksiya elementlariga ularning indeksi orqali xavfsiz murojaat qilish uchun '.indices' dan foydalaning.",
        """fun main() {
    val languages = listOf("Kotlin", "Java", "Python", "Swift")
    
    println("Dasturlash tillari:")
    for (i in languages.indices) {
        println("${i + 1}-o'rin: ${languages[i]}")
    }
}""",
        "'.indices' xususiyati kolleksiyaning '0 until size' oralig'ini qaytaradi. Bu massiv hajmidan oshib ketish xavfini butunlay bartaraf etadi.",
        """Dasturlash tillari:
1-o'rin: Kotlin
2-o'rin: Java
3-o'rin: Python
4-o'rin: Swift"""
    ),
    (
        115,
        "Indeks va Elementni birdaniga olish: withIndex()",
        "Destrukturlash sintaksisi orqali ham indeks, ham qiymatni bitta 'for' siklida oling.",
        """fun main() {
    val cities = listOf("Toshkent", "Samarqand", "Buxoro", "Xiva")
    
    for ((index, city) in cities.withIndex()) {
        println("Indeks [$index] -> Shahar: $city")
    }
}""",
        "'cities.withIndex()' har bir qadamda 'IndexedValue(index, value)' obyektini beradi va Kotlindagi juftlik destrukturizatsiyasi '(index, city)' tufayli ikkita alohida o'zgaruvchiga ajraladi.",
        """Indeks [0] -> Shahar: Toshkent
Indeks [1] -> Samarqand
Indeks [2] -> Shahar: Buxoro
Indeks [3] -> Shahar: Xiva"""
    ),
    (
        116,
        "While sikli bilan shartli takrorlash",
        "Raqamning raqamlari yig'indisini 'while' sikli orqali hisoblang.",
        """fun sumOfDigits(number: Int): Int {
    var n = Math.abs(number)
    var sum = 0
    while (n > 0) {
        sum += n % 10
        n /= 10
    }
    return sum
}

fun main() {
    val testNum = 4582
    println("$testNum raqamlari yig'indisi: ${sumOfDigits(testNum)}")
}""",
        "'while' sikli berilgan mantiqiy shart to'g'ri (true) bo'lib turgunga qadar blokni takroran bajaradi. Shart bajarilishdan oldin tekshiriladi.",
        """4582 raqamlari yig'indisi: 19"""
    ),
    (
        117,
        "Do-While sikli va o'zgaruvchilar ko'rinish sohasi (Scope)",
        "Kotlinda 'do-while' sikli tanasida e'lon qilingan o'zgaruvchi 'while' shartida ko'rinishini namoyish qiling.",
        """fun main() {
    var attempt = 0
    
    do {
        // Kotlinda bu o'zgaruvchi pastdagi while shartida ham ko'rinadi!
        val randomNum = (1..10).random()
        attempt++
        println("$attempt-urinish: Hosil bo'lgan son: $randomNum")
    } while (randomNum != 7)
    
    println("7 soni $attempt ta urinishda topildi!")
}""",
        "Java va C++ da 'do' bloki ichida e'lon qilingan o'zgaruvchi 'while (condition)' qismida ko'rinmaydi. Ammo Kotlin tilida qulaylik uchun 'do' ichidagi o'zgaruvchilar 'while' shartiga to'g'ridan-to'g'ri ta'sir qila oladi.",
        """1-urinish: Hosil bo'lgan son: 3
2-urinish: Hosil bo'lgan son: 9
3-urinish: Hosil bo'lgan son: 7
7 soni 3 ta urinishda topildi!"""
    ),
    (
        118,
        "Ichma-ich sikllar va yorliqli to'xtatish (Labeled break)",
        "Ikki o'lchovli matritsada qidirilayotgan qiymat topilganda tashqi siklni ham darhol to'xtatuvchi 'break@label' dan foydalaning.",
        """fun main() {
    val matrix = arrayOf(
        intArrayOf(1, 2, 3),
        intArrayOf(4, 99, 6),
        intArrayOf(7, 8, 9)
    )
    
    val target = 99
    var foundRow = -1
    var foundCol = -1
    
    outerLoop@ for (i in matrix.indices) {
        for (j in matrix[i].indices) {
            if (matrix[i][j] == target) {
                foundRow = i
                foundCol = j
                break@outerLoop // Butun tashqi siklni to'xtatadi
            }
        }
    }
    
    println("Nishon $target topildi: Qator=$foundRow, Ustun=$foundCol")
}""",
        "Kotlinda har qanday ifodani yorliq (label) bilan nomlash mumkin: 'labelName@'. 'break@outerLoop' oddiy break kabi faqat ichki siklni emas, balki belgilangan tashqi siklni ham to'liq to'xtatadi.",
        """Nishon 99 topildi: Qator=1, Ustun=1"""
    ),
    (
        119,
        "Yorliqli davom ettirish (Labeled continue)",
        "Ichki sikldagi ma'lum shartda tashqi siklning keyingi iteratsiyasiga o'tish uchun 'continue@label' dan foydalaning.",
        """fun main() {
    outer@ for (i in 1..3) {
        for (j in 1..3) {
            if (i == 2 && j == 2) {
                println("Tashqi sikl keyingi qadamiga o'tish (i=$i, j=$j)")
                continue@outer
            }
            println("i = $i, j = $j")
        }
    }
}""",
        "'continue@outer' buyrug'i joriy ichki siklni to'xtatib, belgilangan tashqi siklning keyingi qadamiga o'tishni ta'minlaydi.",
        """i = 1, j = 1
i = 1, j = 2
i = 1, j = 3
i = 2, j = 1
Tashqi sikl keyingi qadamiga o'tish (i=2, j=2)
i = 3, j = 1
i = 3, j = 2
i = 3, j = 3"""
    ),
    (
        120,
        "Lambdadan qaytish: Mahalliy return (return@forEach)",
        "'forEach' sikli ichida faqat joriy elementni o'tkazib yuborish (continue ga o'xshash) uchun yorliqli return qo'llang.",
        """fun main() {
    val numbers = listOf(1, 2, 3, 4, 5)
    
    println("forEach sikli boshlandi:")
    numbers.forEach { num ->
        if (num == 3) {
            // return@forEach joriy elementni o'tkazib yuboradi (continue kabi)
            return@forEach
        }
        println("Element: $num")
    }
    println("Sikl muvaffaqiyatli yakunlandi.")
}""",
        "Kotlinda oddiy 'return' tashqi funksiyadan chiqib ketishga olib keladi (non-local return). Agar faqat lambda blokidan chiqish kerak bo'lsa, funksiya nomi bilan 'return@forEach' belgilanadi.",
        """forEach sikli boshlandi:
Element: 1
Element: 2
Element: 4
Element: 5
Sikl muvaffaqiyatli yakunlandi."""
    ),
    (
        121,
        "Massivda element borligini 'in' bilan tekshirish",
        "Elementlar ro'yxatida ma'lum qiymat bor-yo'qligini 'in' va '!in' operatorlari orqali tekshiring.",
        """fun main() {
    val allowedRoles = listOf("ADMIN", "MANAGER", "EDITOR")
    
    val user1Role = "MANAGER"
    val user2Role = "GUEST"
    
    println("$user1Role ruxsat etilganmi: ${user1Role in allowedRoles}")
    println("$user2Role taqiqlanganmi: ${user2Role !in allowedRoles}")
}""",
        "'in' operatori kolleksiyalarda 'contains(item)' metodiga kompilyatsiya bo'ladi. Bu kodni SQL yoki matematik tushunchalarga juda yaqinlashtiradi.",
        """MANAGER ruxsat etilganmi: true
GUEST taqiqlanganmi: true"""
    ),
    (
        122,
        "Kolleksiyani shart bo'yicha bo'laklash (chunked va windowed)",
        "Katta ro'yxatni 3 tadan elementli kichik qismlarga bo'lib aylanib chiqing.",
        """fun main() {
    val items = (1..10).toList()
    
    val chunks = items.chunked(3)
    println("3 tadan bo'lingan qismlar:")
    for (batch in chunks) {
        println("Paket: $batch, Yig'indisi: ${batch.sum()}")
    }
}""",
        "'chunked(size)' funksiyasi ro'yxatni ko'rsatilgan hajmga ko'ra kichik guruhlarga ajratadi. Bu ma'lumotlar bazasiga ommaviy yozishda (batch insert) keng qo'llaniladi.",
        """3 tadan bo'lingan qismlar:
Paket: [1, 2, 3], Yig'indisi: 6
Paket: [4, 5, 6], Yig'indisi: 15
Paket: [7, 8, 9], Yig'indisi: 24
Paket: [10], Yig'indisi: 10"""
    ),
    (
        123,
        "Fibonachchi ketma-ketligini generatsiya qilish",
        "While sikli yordamida dastlabki N ta Fibonachchi sonlarini hisoblang.",
        """fun generateFibonacci(count: Int): List<Long> {
    val result = mutableListOf<Long>()
    var a = 0L
    var b = 1L
    var i = 0
    
    while (i < count) {
        result.add(a)
        val next = a + b
        a = b
        b = next
        i++
    }
    return result
}

fun main() {
    println("Dastlabki 8 ta Fibonachchi soni: ${generateFibonacci(8)}")
}""",
        "Fibonachchi sonlarini hisoblashda o'zgaruvchilarni navbatma-navbat yangilash va 'while' sikli orqali chegaraga yetguncha ro'yxat to'ldirish klassik algoritmik yondashuvdir.",
        """Dastlabki 8 ta Fibonachchi soni: [0, 1, 1, 2, 3, 5, 8, 13]"""
    ),
    (
        124,
        "Tub sonlarni aniqlash (Is Prime Number)",
        "For sikli va oraliqlar yordamida berilgan sonning tub (prime) ekanligini samarali tekshiring.",
        """fun isPrime(n: Int): Boolean {
    if (n <= 1) return false
    if (n == 2) return true
    if (n % 2 == 0) return false
    
    val limit = Math.sqrt(n.toDouble()).toInt()
    for (i in 3..limit step 2) {
        if (n % i == 0) return false
    }
    return true
}

fun main() {
    val testNumbers = listOf(2, 7, 12, 19, 29, 35)
    for (num in testNumbers) {
        println("$num tub sonmi: ${isPrime(num)}")
    }
}""",
        "Sonning tubligini tekshirishda faqat ildizgacha (sqrt(n)) bo'lgan toq sonlarni 'step 2' orqali tekshirish algoritm tezligini sezilarli oshiradi.",
        """2 tub sonmi: true
7 tub sonmi: true
12 tub sonmi: false
19 tub sonmi: true
29 tub sonmi: true
35 tub sonmi: false"""
    ),
    (
        125,
        "Shartli yig'indi: repeat() funksiyasi",
        "Kotlindagi standart 'repeat(n)' inline funksiyasidan foydalanib amallarni takrorlang.",
        """fun main() {
    var counter = 0
    repeat(5) { iteration ->
        counter += (iteration + 1)
        println("Qadam $iteration: Yangi yig'indi: $counter")
    }
}""",
        "'repeat(n) { index -> ... }' funksiyasi 0 dan n-1 gacha bo'lgan an'anaviy 'for (i in 0 until n)' siklining zamonaviy, ixcham funksional shaklidir.",
        """Qadam 0: Yangi yig'indi: 1
Qadam 1: Yangi yig'indi: 3
Qadam 2: Yangi yig'indi: 6
Qadam 3: Yangi yig'indi: 10
Qadam 4: Yangi yig'indi: 15"""
    ),
    (
        126,
        "Ko'p shartli chegirma hisoblagich (when ifodasi)",
        "Xaridorning xarid summasi va uning a'zolik darajasiga qarab chegirma foizini hisoblang.",
        """enum class Membership { REGULAR, SILVER, GOLD, PLATINUM }

fun calculateDiscount(amount: Double, membership: Membership): Double {
    return when {
        membership == Membership.PLATINUM -> 0.25 // 25%
        membership == Membership.GOLD && amount > 1000 -> 0.20 // 20%
        membership == Membership.GOLD -> 0.15 // 15%
        membership == Membership.SILVER && amount > 500 -> 0.10 // 10%
        membership == Membership.SILVER -> 0.05 // 5%
        amount > 2000 -> 0.07 // Oddiy mijoz katta xarid
        else -> 0.0
    }
}

fun main() {
    println("Chegirma 1: ${calculateDiscount(1200.0, Membership.GOLD) * 100}%")
    println("Chegirma 2: ${calculateDiscount(300.0, Membership.SILVER) * 100}%")
    println("Chegirma 3: ${calculateDiscount(2500.0, Membership.REGULAR) * 100}%")
}""",
        "Argumentsiz 'when' mantiqiy shartlar ketma-ketligini yuqoridan pastga baholaydi va birinchi to'g'ri kelgan shart natijasini qaytaradi.",
        """Chegirma 1: 20.0%
Chegirma 2: 5.0%
Chegirma 3: 7.0%"""
    ),
    (
        127,
        "Ikki o'lchovli massivni formatlab jadval ko'rinishida chop etish",
        "Kopaytirish jadvalining 1 dan 5 gacha qismini chiroyli formatda chop eting.",
        """fun main() {
    println("KOPAYTIRISH JADVALI (1..5):")
    for (i in 1..5) {
        for (j in 1..5) {
            print(String.format("%4d", i * j))
        }
        println()
    }
}""",
        "Ichma-ich 'for' sikllari ikki o'lchovli ma'lumotlar va matritsalarni aks ettirishda standart vositadir. 'String.format(\"%4d\")' ustunlar tekisligini ta'minlaydi.",
        """KOPAYTIRISH JADVALI (1..5):
   1   2   3   4   5
   2   4   6   8  10
   3   6   9  12  15
   4   8  12  16  20
   5  10  15  20  25"""
    ),
    (
        128,
        "Shartli boshqaruv: Harflar soni va so'z uzunligini solishtirish",
        "Matndagi eng uzun so'zni sikl va shartlar yordamida toping.",
        """fun findLongestWord(sentence: String): String {
    val words = sentence.split(" ")
    var longest = ""
    for (w in words) {
        val cleanWord = w.filter { it.isLetter() }
        if (cleanWord.length > longest.length) {
            longest = cleanWord
        }
    }
    return longest
}

fun main() {
    val text = "Kotlin dasturlash tili zamonaviy ilovalarni tez va sifatli yaratadi"
    println("Eng uzun so'z: ${findLongestWord(text)}")
}""",
        "Kolleksiya ustida sikl aylanib, shart asosida eng katta/kichik elementni saqlab borish asosiy dasturlash andozalaridan biridir.",
        """Eng uzun so'z: dasturlash"""
    ),
    (
        129,
        "Raqamlar teskarisini hosil qilish (Reversing an integer)",
        "Matnga o'girmasdan, sof arifmetik 'while' sikli bilan sonni teskari o'giring.",
        """fun reverseNumber(number: Int): Int {
    var n = number
    var reversed = 0
    while (n != 0) {
        val digit = n % 10
        reversed = reversed * 10 + digit
        n /= 10
    }
    return reversed
}

fun main() {
    println("12345 teskarisi: ${reverseNumber(12345)}")
    println("-987 teskarisi: ${reverseNumber(-987)}")
}""",
        "Arifmetik qoldiq '%' va bo'lish '/' orqali xotirada ortiqcha satr obyektlari yaratmasdan xotiradan yuksak unum bilan foydalanish mumkin.",
        """12345 teskarisi: 54321
-987 teskarisi: -789"""
    ),
    (
        130,
        "Sikl davomida xavfsiz to'plash: Running fold / scan",
        "Sonlar ro'yxatida har bir qadamdagi umumiy yig'indini (running sum) 'scan' orqali hosil qiling.",
        """fun main() {
    val dailySteps = listOf(3000, 4500, 5000, 6000)
    
    // Kotlin standart kutubxonasidagi running sum:
    val cumulativeSteps = dailySteps.scan(0) { total, next -> total + next }
    
    println("Kunlik qadamlar: $dailySteps")
    println("Kümülyativ qadamlar: $cumulativeSteps")
}""",
        "'scan' (yoki 'runningFold') har bir iteratsiya oraliq natijasini yangi ro'yxatga qo'shib boradi. Bu grafiklar chizish va o'sish dinamikasini hisoblashda qulaydir.",
        """Kunlik qadamlar: [3000, 4500, 5000, 6000]
Kümülyativ qadamlar: [0, 3000, 7500, 12500, 18500]"""
    ),
    (
        131,
        "Shartli belgilash: Maxsus buyruqlarni tahlil qilish",
        "Terminal buyruqlarini (start, stop, pause, restart) 'when' orqali boshqaring.",
        """fun executeCommand(command: String): String {
    return when (command.trim().lowercase()) {
        "start" -> "Tizim ishga tushirildi."
        "stop" -> "Tizim butunlay to'xtatildi."
        "pause" -> "Tizim vaqtincha to'xtatib turildi."
        "restart" -> "Tizim qayta yuklanmoqda..."
        else -> "Noma'lum buyruq: '$command'. Yordam uchun 'help' deb yozing."
    }
}

fun main() {
    println(executeCommand(" START "))
    println(executeCommand("pause"))
    println(executeCommand("shutdown"))
}""",
        "Satrlarni tozalash ('trim().lowercase()') va 'when' orqali moslashtirish buyruqlar satri interfeyslarida (CLI) juda ko'p qo'llaniladi.",
        """Tizim ishga tushirildi.
Tizim vaqtincha to'xtatib turildi.
Noma'lum buyruq: 'shutdown'. Yordam uchun 'help' deb yozing."""
    ),
    (
        132,
        "Murakkab shartlar: Soliq stavkalari shkalasi (Progressive Tax)",
        "Oylik maoshga nisbatan progressiv daromad solig'ini 'when' yordamida hisoblang.",
        """fun calculateTax(salary: Double): Double {
    return when {
        salary <= 3_000_000 -> 0.0 // Soliqsiz minimum
        salary <= 8_000_000 -> (salary - 3_000_000) * 0.12
        else -> (5_000_000 * 0.12) + (salary - 8_000_000) * 0.20
    }
}

fun main() {
    println("2.5 mln soliq: " + calculateTax(2_500_000.0))
    println("6.0 mln soliq: " + calculateTax(6_000_000.0))
    println("12.0 mln soliq: " + calculateTax(12_000_000.0))
}""",
        "Progressiv stavkalarda har bir pog'onaga alohida shart qo'yiladi va qoldiq summa bo'yicha hisob-kitob amalga oshiriladi.",
        """2.5 mln soliq: 0.0
6.0 mln soliq: 360000.0
12.0 mln soliq: 1400000.0"""
    ),
    (
        133,
        "Sikllar bilan qidirish: Ikkinchi eng katta sonni topish",
        "Bir marta o'tishda (O(N) vaqt) massivdagi 2-eng katta elementni aniqlang.",
        """fun findSecondLargest(numbers: IntArray): Int? {
    if (numbers.size < 2) return null
    var first = Int.MIN_VALUE
    var second = Int.MIN_VALUE
    
    for (n in numbers) {
        if (n > first) {
            second = first
            first = n
        } else if (n > second && n != first) {
            second = n
        }
    }
    return if (second == Int.MIN_VALUE) null else second
}

fun main() {
    val arr = intArrayOf(12, 35, 1, 10, 35, 34)
    println("Ikkinchi eng katta son: ${findSecondLargest(arr)}")
}""",
        "Bir o'tishda massiv elementlarini saralamasdan solishtirish algoritmik samaradorlikni ta'minlaydi va xotirani tejaydi.",
        """Ikkinchi eng katta son: 34"""
    ),
    (
        134,
        "Shartli zanjir: Uchburchak mavjudligini tekshirish",
        "Berilgan uchta kesma uzunligidan uchburchak yasash mumkinligini va uning turini (teng tomonli, teng yonli, turli tomonli) aniqlang.",
        """fun classifyTriangle(a: Double, b: Double, c: Double): String {
    // Uchburchak tengsizligi
    if (a + b <= c || a + c <= b || b + c <= a) {
        return "Bunday tomonlar bilan uchburchak mavjud emas!"
    }
    
    return when {
        a == b && b == c -> "Teng tomonli uchburchak"
        a == b || b == c || a == c -> "Teng yonli uchburchak"
        else -> "Turli tomonli uchburchak"
    }
}

fun main() {
    println(classifyTriangle(5.0, 5.0, 5.0))
    println(classifyTriangle(5.0, 5.0, 8.0))
    println(classifyTriangle(3.0, 4.0, 5.0))
    println(classifyTriangle(1.0, 2.0, 10.0))
}""",
        "Avval geometrik mavjudlik sharti tekshiriladi, so'ngra 'when' yordamida tomonlar tengligi bo'yicha toifalarga ajratiladi.",
        """Teng tomonli uchburchak
Teng yonli uchburchak
Turli tomonli uchburchak
Bunday tomonlar bilan uchburchak mavjud emas!"""
    ),
    (
        135,
        "Sikl yordamida Faktorial hisoblash (Katta sonlar bilan)",
        "Faktorialni hisoblashda BigInteger ishlatib, katta qiymatlarni aniq toping.",
        """import java.math.BigInteger

fun calculateFactorial(n: Int): BigInteger {
    var result = BigInteger.ONE
    for (i in 2..n) {
        result = result.multiply(BigInteger.valueOf(i.toLong()))
    }
    return result
}

fun main() {
    println("5! = ${calculateFactorial(5)}")
    println("20! = ${calculateFactorial(20)}")
}""",
        "20! kabi katta sonlar standart Long doirasidan chiqib ketadi (overflow). BigInteger sikl ichida to'lib toshishsiz cheksiz aniqlik beradi.",
        """5! = 120
20! = 2432902008176640000"""
    ),
    (
        136,
        "Sikllarda filtrlash va xaritalash: Anagrammalarni aniqlash",
        "Ikki satr bir xil harflardan tashkil topganligini (anagramma) sikl va saralash orqali tekshiring.",
        """fun isAnagram(s1: String, s2: String): Boolean {
    val clean1 = s1.lowercase().filter { it.isLetter() }.toCharArray().sorted()
    val clean2 = s2.lowercase().filter { it.isLetter() }.toCharArray().sorted()
    return clean1 == clean2
}

fun main() {
    println(isAnagram("tok", "kot"))
    println(isAnagram("Listen", "Silent"))
    println(isAnagram("Kitob", "Daftar"))
}""",
        "Satrlarni harflar massiviga o'tkazib saralash va ularning tengligini tekshirish anagrammalarni aniqlashning eng ishonchli usulidir.",
        """true
true
false"""
    ),
    (
        137,
        "Do-While bilan PIN kod tekshirish simulyatori",
        "Foydalanuvchi to'g'ri PIN kodni kiritguncha yoki urinishlar soni (3 ta) tugaguncha siklni davom ettiring.",
        """fun simulatePinEntry(enteredPins: List<String>): String {
    val correctPin = "7788"
    var attempts = 0
    var isSuccess = false
    
    do {
        val currentPin = enteredPins.getOrNull(attempts) ?: break
        attempts++
        println("$attempts-urinish kiritildi: $currentPin")
        if (currentPin == correctPin) {
            isSuccess = true
            break
        }
    } while (attempts < 3)
    
    return if (isSuccess) "Kirishga ruxsat berildi!" else "Karta bloklandi!"
}

fun main() {
    println(simulatePinEntry(listOf("1111", "2222", "7788")))
    println("---")
    println(simulatePinEntry(listOf("0000", "1234", "9999")))
}""",
        "'do-while' sikli kamida bir marta bajarilishi shart bo'lgan autentifikatsiya jarayonlarida urinishlar soni bilan qat'iy nazorat qilinadi.",
        """1-urinish kiritildi: 1111
2-urinish kiritildi: 2222
3-urinish kiritildi: 7788
Kirishga ruxsat berildi!
---
1-urinish kiritildi: 0000
2-urinish kiritildi: 1234
3-urinish kiritildi: 9999
Karta bloklandi!"""
    ),
    (
        138,
        "Belgilar chastotasi lug'atini (Histogram) sikl orqali yasash",
        "Matndagi har bir harf necha marta takrorlanganini hisoblang.",
        """fun charFrequency(text: String): Map<Char, Int> {
    val frequencyMap = mutableMapOf<Char, Int>()
    for (ch in text.lowercase()) {
        if (ch.isLetter()) {
            val count = frequencyMap.getOrDefault(ch, 0)
            frequencyMap[ch] = count + 1
        }
    }
    return frequencyMap
}

fun main() {
    val freq = charFrequency("Dasturlash")
    println("Harflar uchrash soni: $freq")
}""",
        "'frequencyMap.getOrDefault(ch, 0) + 1' andozasi matn tahlili va ma'lumotlar statistikasida asosiy hisoblash mexanizmidir.",
        """Harflar uchrash soni: {d=1, a=3, s=2, t=1, u=1, r=1, l=1, h=1}"""
    ),
    (
        139,
        "Shartli boshqaruv: HTTP Status kodlari tahlili",
        "Web so'rov statusiga qarab foydalanuvchiga to'g'ri o'zbekcha yo'riqnoma chiqaring.",
        """fun handleHttpStatus(code: Int): String {
    return when (code) {
        200 -> "Muvaffaqiyatli bajarildi (OK)."
        201 -> "Yangi resurs yaratildi (Created)."
        400 -> "So'rovda xatolik mavjud (Bad Request)."
        401 -> "Tizimga kirish talab etiladi (Unauthorized)."
        403 -> "Ushbu amalni bajarishga huquqingiz yo'q (Forbidden)."
        404 -> "Sahifa yoki resurs topilmadi (Not Found)."
        500 -> "Serverning ichki xatoligi (Internal Server Error)."
        else -> "Noma'lum status kodi: $code"
    }
}

fun main() {
    println(handleHttpStatus(200))
    println(handleHttpStatus(404))
    println(handleHttpStatus(500))
}""",
        "REST API va HTTP mijoz dasturlarida status kodlariga ko'ra oqimni yo'naltirish 'when' ifodasi orqali aniq va tartibli yoziladi.",
        """Muvaffaqiyatli bajarildi (OK).
Sahifa yoki resurs topilmadi (Not Found).
Serverning ichki xatoligi (Internal Server Error)."""
    ),
    (
        140,
        "Sikl bilan berilgan sonning bo'luvchilarini topish",
        "Berilgan musbat butun sonning barcha bo'luvchilarini 'for' sikli orqali aniqlang.",
        """fun findDivisors(n: Int): List<Int> {
    val divisors = mutableListOf<Int>()
    for (i in 1..n) {
        if (n % i == 0) {
            divisors.add(i)
        }
    }
    return divisors
}

fun main() {
    println("24 ning bo'luvchilari: ${findDivisors(24)}")
    println("17 ning bo'luvchilari: ${findDivisors(17)}")
}""",
        "Modul (%) amali orqali qoldiqsiz bo'linish holati tekshiriladi va natijalar dinamik ro'yxatga yig'iladi.",
        """24 ning bo'luvchilari: [1, 2, 3, 4, 6, 8, 12, 24]
17 ning bo'luvchilari: [1, 17]"""
    ),
    (
        141,
        "Matritsaning bosh diagonalini hisoblash",
        "Kvadrat matritsaning bosh va yordamchi diagonallari yig'indisini bitta siklda toping.",
        """fun main() {
    val matrix = arrayOf(
        intArrayOf(1, 2, 3),
        intArrayOf(4, 5, 6),
        intArrayOf(7, 8, 9)
    )
    
    val n = matrix.size
    var mainDiagonalSum = 0
    var antiDiagonalSum = 0
    
    for (i in 0 until n) {
        mainDiagonalSum += matrix[i][i]
        antiDiagonalSum += matrix[i][n - 1 - i]
    }
    
    println("Bosh diagonal yig'indisi (1 + 5 + 9): $mainDiagonalSum")
    println("Yordamchi diagonal yig'indisi (3 + 5 + 7): $antiDiagonalSum")
}""",
        "Kvadrat matritsada bitta 'for (i in 0 until n)' siklida 'matrix[i][i]' orqali bosh, 'matrix[i][n - 1 - i]' orqali esa yordamchi diagonal olinadi. Murakkablik O(N).",
        """Bosh diagonal yig'indisi (1 + 5 + 9): 15
Yordamchi diagonal yig'indisi (3 + 5 + 7): 15"""
    ),
    (
        142,
        "Shartli sikl: Eng katta umumiy bo'luvchi (EKUB / GCD)",
        "Evklid algoritmini 'while' sikli yordamida amalga oshiring.",
        """fun gcd(a: Int, b: Int): Int {
    var num1 = Math.abs(a)
    var num2 = Math.abs(b)
    while (num2 != 0) {
        val temp = num2
        num2 = num1 % num2
        num1 = temp
    }
    return num1
}

fun main() {
    println("EKUB(48, 18) = ${gcd(48, 18)}")
    println("EKUB(100, 25) = ${gcd(100, 25)}")
}""",
        "Evklid algoritmi modulli bo'lish orqali ikki sonning eng katta umumiy bo'luvchisini logarifmik qadamda (O(log(min(a,b)))) topadi.",
        """EKUB(48, 18) = 6
EKUB(100, 25) = 25"""
    ),
    (
        143,
        "Eng kichik umumiy karrali (EKUK / LCM)",
        "EKUB formulasidan foydalanib EKUK = (a * b) / EKUB(a, b) ni hisoblang.",
        """fun lcm(a: Int, b: Int): Long {
    val g = gcd(a, b)
    return (a.toLong() * b.toLong()) / g
}

fun main() {
    println("EKUK(12, 18) = ${lcm(12, 18)}")
    println("EKUK(7, 5) = ${lcm(7, 5)}")
}""",
        "Ko'paytirish paytida son chegaradan chiqmasligi uchun 'a.toLong() * b.toLong()' qilinadi va avval topilgan GCD funksiyasiga bo'linadi.",
        """EKUK(12, 18) = 36
EKUK(7, 5) = 35"""
    ),
    (
        144,
        "Sikl bilan matndagi qavslar to'g'riligini tekshirish (Balanced Parentheses)",
        "Matndagi '(' va ')' qavslarining to'g'ri ochilib yopilganligini sikl va hisoblagich bilan tekshiring.",
        """fun isBalanced(expression: String): Boolean {
    var balance = 0
    for (ch in expression) {
        if (ch == '(') balance++
        else if (ch == ')') balance--
        
        if (balance < 0) return false // Yopuvchi qavs erta keldi
    }
    return balance == 0
}

fun main() {
    println(isBalanced("(a + b) * (c - d)"))
    println(isBalanced("((a + b) * c"))
    println(isBalanced(")a + b("))
}""",
        "Sikl davomida hisoblagich 0 dan pastga tushib ketsa, qavslar ketma-ketligi buzilgan hisoblanadi. Yakunda hisoblagich aniq 0 bo'lishi kerak.",
        """true
false
false"""
    ),
    (
        145,
        "Murakkab oraliq tekshiruvi: Sana oralig'i va ish kuni",
        "Berilgan sana oy boshiga, o'rtasiga yoki oxiriga to'g'ri kelishini 'when' bilan aniqlang.",
        """fun monthPeriod(dayOfMonth: Int): String {
    return when (dayOfMonth) {
        in 1..10 -> "Oyning birinchi dekadasi (boshi)"
        in 11..20 -> "Oyning o'rtasi"
        in 21..31 -> "Oyning oxiri (yakuniy hisobot davri)"
        else -> "Yaroqsiz sana"
    }
}

fun main() {
    println("5-sana: ${monthPeriod(5)}")
    println("17-sana: ${monthPeriod(17)}")
    println("28-sana: ${monthPeriod(28)}")
}""",
        "Taqvim va hisobot tizimlarida oylik intervallarni 'in 1..10' kabi diapazonlar bilan tekshirish kodni ixcham va xatosiz qiladi.",
        """5-sana: Oyning birinchi dekadasi (boshi)
17-sana: Oyning o'rtasi
28-sana: Oyning oxiri (yakuniy hisobot davri)"""
    ),
    (
        146,
        "Kolleksiyadagi dublikatlarni topish va olib tashlash",
        "Sikl yordamida ro'yxatdagi takrorlangan elementlarni aniqlang.",
        """fun findDuplicates(items: List<String>): Set<String> {
    val seen = mutableSetOf<String>()
    val duplicates = mutableSetOf<String>()
    
    for (item in items) {
        if (!seen.add(item)) {
            duplicates.add(item)
        }
    }
    return duplicates
}

fun main() {
    val fruits = listOf("Olma", "Anor", "Nok", "Olma", "Uzum", "Anor")
    println("Takrorlangan mevalar: ${findDuplicates(fruits)}")
}""",
        "'Set.add(element)' metodi agar element to'plamda mavjud bo'lmasa true, mavjud bo'lsa false qaytaradi. Bu orqali dublikatlar O(N) vaqtda oson topiladi.",
        """Takrorlangan mevalar: [Olma, Anor]"""
    ),
    (
        147,
        "Shartli saralash: Bubble Sort (Pufakchali saralash)",
        "For sikllari va shartli almashtirish (swap) yordamida massivni o'sish tartibida saralang.",
        """fun bubbleSort(arr: IntArray) {
    val n = arr.size
    for (i in 0 until n - 1) {
        var swapped = false
        for (j in 0 until n - 1 - i) {
            if (arr[j] > arr[j + 1]) {
                val temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp
                swapped = true
            }
        }
        if (!swapped) break
    }
}

fun main() {
    val array = intArrayOf(64, 34, 25, 12, 22, 11, 90)
    bubbleSort(array)
    println("Saralangan massiv: ${array.joinToString()}")
}""",
        "Bubble sort algoritmi qo'shni elementlarni solishtirib joyini almashtiradi. 'swapped' bayrog'i massiv erta saralangan holatda ortiqcha iteratsiyalarni to'xtatadi.",
        """Saralangan massiv: 11, 12, 22, 25, 34, 64, 90"""
    ),
    (
        148,
        "Bankomat (ATM) tranzaksiyalar oqimi simulyatori",
        "Foydalanuvchi hisobidan pul yechish va balansni to'ldirish buyruqlarini boshqarish tizimini 'when' bilan yozing.",
        """sealed class AtmCommand {
    data class Deposit(val amount: Double) : AtmCommand()
    data class Withdraw(val amount: Double) : AtmCommand()
    object CheckBalance : AtmCommand()
}

fun processAtm(currentBalance: Double, command: AtmCommand): Double {
    return when (command) {
        is AtmCommand.Deposit -> {
            val newBalance = currentBalance + command.amount
            println("Hisob to'ldirildi: +$$command.amount | Yangi balans: $$newBalance")
            newBalance
        }
        is AtmCommand.Withdraw -> {
            if (currentBalance >= command.amount) {
                val newBalance = currentBalance - command.amount
                println("Pul yechildi: -$$command.amount | Yangi balans: $$newBalance")
                newBalance
            } else {
                println("Yetarli mablag' yo'q! So'ralgan: $$command.amount, Balans: $$currentBalance")
                currentBalance
            }
        }
        is AtmCommand.CheckBalance -> {
            println("Joriy balans: $$currentBalance")
            currentBalance
        }
    }
}

fun main() {
    var balance = 500.0
    balance = processAtm(balance, AtmCommand.CheckBalance)
    balance = processAtm(balance, AtmCommand.Deposit(200.0))
    balance = processAtm(balance, AtmCommand.Withdraw(800.0))
    balance = processAtm(balance, AtmCommand.Withdraw(300.0))
}""",
        "Sealed class va 'when' kombinatsiyasi biznes jarayonlarida to'liq xavfsiz holat mashinasini (State Machine) shakllantirish imkonini beradi.",
        """Joriy balans: $500.0
Hisob to'ldirildi: +$200.0 | Yangi balans: $700.0
Yetarli mablag' yo'q! So'ralgan: $800.0, Balans: $700.0
Pul yechildi: -$300.0 | Yangi balans: $400.0"""
    ),
    (
        149,
        "Shartli o'yin tsikli (Game Loop) va hayotlar soni",
        "O'yinchining harakatlarini tahlil qilib, to'siqlarga urilganda jonlarini kamaytiruvchi va 0 bo'lganda o'yinni to'xtatuvchi tsikl tuzing.",
        """fun runGameSession(events: List<String>) {
    var lives = 3
    var score = 0
    
    println("O'yin boshlandi! Jonlar soni: $lives")
    for (event in events) {
        when (event) {
            "COIN" -> {
                score += 10
                println("Tanga olindi (+10 ball). Jami: $score")
            }
            "MONSTER" -> {
                lives--
                println("Maxluqqa urildi! 1 jon yo'qotildi. Qoldi: $lives")
                if (lives <= 0) {
                    println("Barcha jonlar tugadi! O'YIN TUGADI (GAME OVER).")
                    break
                }
            }
            "BONUS_LIFE" -> {
                lives++
                println("Bonus jon olindi! Jonlar soni: $lives")
            }
        }
    }
    println("Yakuniy ball: $score | Qolgan jonlar: $lives")
}

fun main() {
    val gameEvents = listOf("COIN", "COIN", "MONSTER", "COIN", "MONSTER", "MONSTER", "COIN")
    runGameSession(gameEvents)
}""",
        "O'yin mantig'ida sikl har bir hodisani (event) qabul qilib, o'yinchi holatini (lives, score) yangilaydi va kritik shartlarda siklni 'break' bilan to'xtatadi.",
        """O'yin boshlandi! Jonlar soni: 3
Tanga olindi (+10 ball). Jami: 10
Tanga olindi (+10 ball). Jami: 20
Maxluqqa urildi! 1 jon yo'qotildi. Qoldi: 2
Tanga olindi (+10 ball). Jami: 30
Maxluqqa urildi! 1 jon yo'qotildi. Qoldi: 1
Maxluqqa urildi! 1 jon yo'qotildi. Qoldi: 0
Barcha jonlar tugadi! O'YIN TUGADI (GAME OVER).
Yakuniy ball: 30 | Qolgan jonlar: 0"""
    ),
    (
        150,
        "Boshqaruv oqimlari bo'yicha to'liq amaliy xulosa",
        "If, when, for, while, ranges va labeling imkoniyatlarini birlashtirgan ma'lumotlar tahlilchisi hisobotini shakllantiring.",
        """fun main() {
    val transactionData = listOf(150, -20, 450, 0, -80, 1200, -500, 300)
    
    var totalIncome = 0
    var totalExpense = 0
    var transactionCount = 0
    
    for ((index, amount) in transactionData.withIndex()) {
        val category = when {
            amount > 1000 -> "Katta daromad"
            amount > 0 -> "Oddiy daromad"
            amount == 0 -> "Nol tranzaksiya"
            amount < -200 -> "Katta xarajat"
            else -> "Kichik xarajat"
        }
        
        if (amount > 0) {
            totalIncome += amount
        } else {
            totalExpense += Math.abs(amount)
        }
        transactionCount++
        println("Tranzaksiya #${index + 1}: $amount UZS ($category)")
    }
    
    val netBalance = totalIncome - totalExpense
    val financialStatus = if (netBalance > 0) "Foydali (Ijobiy)" else "Zararli (Salbiy)"
    
    println(\"\"\"
        ==============================
        MOLIYAVIY HISOBOT
        ==============================
        Jami amallar: $transactionCount ta
        Umumiy kirim: $totalIncome UZS
        Umumiy chiqim: $totalExpense UZS
        Sof balans: $netBalance UZS
        Holat: $financialStatus
        ==============================
    \"\"\".trimIndent())
}""",
        "Ushbu yakuniy topshiriqda shartli mantiq (if-else expression), 'when' oraliq shartlari, 'for withIndex()' sikli va formatlash imkoniyatlari to'liq integratsiya qilindi.",
        """Tranzaksiya #1: 150 UZS (Oddiy daromad)
Tranzaksiya #2: -20 UZS (Kichik xarajat)
Tranzaksiya #3: 450 UZS (Oddiy daromad)
Tranzaksiya #4: 0 UZS (Nol tranzaksiya)
Tranzaksiya #5: -80 UZS (Kichik xarajat)
Tranzaksiya #6: 1200 UZS (Katta daromad)
Tranzaksiya #7: -500 UZS (Katta xarajat)
Tranzaksiya #8: 300 UZS (Oddiy daromad)
==============================
MOLIYAVIY HISOBOT
==============================
Jami amallar: 8 ta
Umumiy kirim: 2100 UZS
Umumiy chiqim: 600 UZS
Sof balans: 1500 UZS
Holat: Foydali (Ijobiy)
=============================="""
    )
]

for item in data_03:
    n, title, condition, sol, exp, res = item
    tasks.append(format_task(n, title, condition, sol, exp, res))

save_file("kotlin_03_boshqaruv_oqimlari_va_shartlar.md", tasks)
