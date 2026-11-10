# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

data_13 = [
    (
        601,
        "Kolleksiyalar iyerarxiyasi: O'zgarmas (List) vs O'zgaruvchan (MutableList)",
        "Kotlinda 'listOf()' va 'mutableListOf()' tushunchalarini va ularning xavfsizlik afzalliklarini namoyish qiling.",
        """fun main() {
    val readOnlyList: List<String> = listOf("Toshkent", "Samarqand", "Buxoro")
    // readOnlyList.add("Xiva") // Kompilyatsiya xatosi: Unresolved reference: add

    val mutableList: MutableList<String> = mutableListOf("Toshkent", "Samarqand")
    mutableList.add("Buxoro")
    mutableList.add("Xiva")

    println("Read-only ro'yxat: $readOnlyList")
    println("Mutable ro'yxat: $mutableList")
}""",
        "Kotlinda kolleksiyalar qat'iy ikkiga bo'linadi: faqat o'qish uchun mo'ljallangan (Read-Only: List, Set, Map) va o'zgartiriladigan (Mutable: MutableList, MutableSet, MutableMap). Bu ko'p oqimli dasturlashda kutilmagan o'zgarishlar va poyga holatlarining (race conditions) oldini oladi.",
        """Read-only ro'yxat: [Toshkent, Samarqand, Buxoro]
Mutable ro'yxat: [Toshkent, Samarqand, Buxoro, Xiva]"""
    ),
    (
        602,
        "To'plamlar: Set va takrorlanmas elementlar",
        "Takroriy elementlarni avtomatik olib tashlovchi 'setOf' va 'mutableSetOf' bilan ishlash.",
        """fun main() {
    val numbersWithDuplicates = listOf(1, 2, 2, 3, 4, 4, 4, 5)
    val uniqueNumbers: Set<Int> = numbersWithDuplicates.toSet()

    println("Asl ro'yxat: $numbersWithDuplicates (hajmi: ${numbersWithDuplicates.size})")
    println("Set to'plami: $uniqueNumbers (hajmi: ${uniqueNumbers.size})")
}""",
        "'Set' to'plami har bir elementning faqat bitta yagona nusxasini saqlaydi. Unga dublikat element qo'shilsa, u shunchaki e'tiborsiz qoldiriladi.",
        """Asl ro'yxat: [1, 2, 2, 3, 4, 4, 4, 5] (hajmi: 8)
Set to'plami: [1, 2, 3, 4, 5] (hajmi: 5)"""
    ),
    (
        603,
        "Lug'atlar: Map va kalit-qiymat juftliklari",
        "'mapOf' va 'to' sintaksisi orqali lug'at tuzib, qiymatlarni o'qish.",
        """fun main() {
    val countryCapitals = mapOf(
        "Uzbekistan" to "Tashkent",
        "France" to "Paris",
        "Japan" to "Tokyo"
    )

    println("O'zbekiston poytaxti: ${countryCapitals["Uzbekistan"]}")
    println("Barcha davlatlar: ${countryCapitals.keys}")
    println("Barcha poytaxtlar: ${countryCapitals.values}")
}""",
        "'Map' kalit-qiymat juftliklarini saqlaydi. 'key to value' sintaksisi 'to' infix funksiyasi orqali Pair obyektini hosil qiladi.",
        """O'zbekiston poytaxti: Tashkent
Barcha davlatlar: [Uzbekistan, France, Japan]
Barcha poytaxtlar: [Tashkent, Paris, Tokyo]"""
    ),
    (
        604,
        "Filtrlash operatsiyalari: filter va filterNot",
        "Ro'yxatdan shartga mos keluvchi va mos kelmaydigan elementlarni ajratish.",
        """fun main() {
    val temperatures = listOf(-5, 0, 12, 25, -2, 18, 30)

    val aboveZero = temperatures.filter { it > 0 }
    val freezing = temperatures.filterNot { it >= 0 }

    println("Ijobiy haroratlar: $aboveZero")
    println("Salbiy haroratlar: $freezing")
}""",
        "'filter' predikat 'true' qaytargan elementlarni, 'filterNot' esa predikat 'false' qaytargan elementlarni yangi ro'yxatga to'playdi.",
        """Ijobiy haroratlar: [12, 25, 18, 30]
Salbiy haroratlar: [-5, -2]"""
    ),
    (
        605,
        "Transformatsiya operatsiyalari: map va mapIndexed",
        "Elementlarni o'zgartirish va indeks bilan birgalikda formatlash.",
        """fun main() {
    val languages = listOf("Kotlin", "Java", "Python")

    val upperCased = languages.map { it.uppercase() }
    val numbered = languages.mapIndexed { index, name -> "${index + 1}. $name" }

    println("Katta harflar: $upperCased")
    println("Raqamlangan ro'yxat:")
    numbered.forEach { println(" $it") }
}""",
        "'map' har bir elementga berilgan lambdani qo'llab yangi ro'yxat hosil qiladi. 'mapIndexed' esa qo'shimcha ravishda element indeksini taqdim etadi.",
        """Katta harflar: [KOTLIN, JAVA, PYTHON]
Raqamlangan ro'yxat:
 1. Kotlin
 2. Java
 3. Python"""
    ),
    (
        606,
        "Null qiymatlarni filtrlash va xaritalash: mapNotNull",
        "String ro'yxatidagi raqamlarni Int ga o'tkazib, xatolilarini chetlab o'tish.",
        """fun main() {
    val rawInputs = listOf("10", "abc", "25", "40", "xyz")

    val validNumbers: List<Int> = rawInputs.mapNotNull { it.toIntOrNull() }

    println("Faqat yaroqli sonlar: $validNumbers")
}""",
        "'mapNotNull' agar lambda null qaytarsa, o'sha elementni tashlab yuboradi va toza 'List<Int>' qaytaradi.",
        """Faqat yaroqli sonlar: [10, 25, 40]"""
    ),
    (
        607,
        "Birlashtirish va Tekislash: flatMap va flatten",
        "Ichma-ich joylashgan to'plamlar ro'yxatini bitta tekis ro'yxatga aylantirish.",
        """class Department(val name: String, val employees: List<String>)

fun main() {
    val departments = listOf(
        Department("Mobil", listOf("Alisher", "Bobur")),
        Department("Backend", listOf("Jasur", "Sardor", "Nodir"))
    )

    // Barcha xodimlarni bitta tekis ro'yxatga olish:
    val allEmployees = departments.flatMap { it.employees }

    println("Kompaniya barcha xodimlari: $allEmployees")
}""",
        "'flatMap' har bir obyekt ichidagi ro'yxatni oladi va ularning barchasini bitta tekislangan umumiy ro'yxatga yoyadi.",
        """Kompaniya barcha xodimlari: [Alisher, Bobur, Jasur, Sardor, Nodir]"""
    ),
    (
        608,
        "Elementlarni tekshirish: any, all, none",
        "Kolleksiya shartlarga qanday mos kelishini bitta amalda aniqlash.",
        """fun main() {
    val ages = listOf(19, 22, 25, 30, 18)

    val allAdults = ages.all { it >= 18 }
    val anySenior = ages.any { it >= 60 }
    val noneNegative = ages.none { it < 0 }

    println("Barcha voyaga yetganmi (all): $allAdults")
    println("Nuroniy bormi (any): $anySenior")
    println("Manfiy yosh yo'qmi (none): $noneNegative")
}""",
        "'all' barcha elementlar mos bo'lsagina true, 'any' kamida bittasi mos bo'lsa true, 'none' esa birontasi ham mos bo'lmaganda true qaytaradi.",
        """Barcha voyaga yetganmi (all): true
Nuroniy bormi (any): false
Manfiy yosh yo'qmi (none): true"""
    ),
    (
        609,
        "Qidiruv operatsiyalari: find va findLast",
        "Shartga mos birinchi va oxirgi elementni topish.",
        """fun main() {
    val numbers = listOf(5, 12, 8, 25, 30, 7)

    val firstEven = numbers.find { it % 2 == 0 }
    val lastEven = numbers.findLast { it % 2 == 0 }

    println("Birinchi juft son: $firstEven")
    println("Oxirgi juft son: $lastEven")
}""",
        "'find' 'firstOrNull' ning, 'findLast' esa 'lastOrNull' ning muqobilidir. Topilmasa null qaytaradi.",
        """Birinchi juft son: 12
Oxirgi juft son: 30"""
    ),
    (
        610,
        "Juftlash va ajratish: zip va unzip",
        "Ikki mustaqil ro'yxatni juftliklarga birlashtirish va qayta ajratish.",
        """fun main() {
    val names = listOf("Ali", "Vali", "G'ani")
    val roles = listOf("Dasturchi", "Dizayner", "Menejer")

    val paired = names.zip(roles)
    println("Juftliklar: $paired")

    val (unzippedNames, unzippedRoles) = paired.unzip()
    println("Ajratilgan ismlar: $unzippedNames")
    println("Ajratilgan rollar: $unzippedRoles")
}""",
        "'zip' ikki ro'yxat elementlaridan 'List<Pair<A, B>>' hosil qiladi. 'unzip' esa ularni yana ikkita alohida ro'yxatga ajratadi.",
        """Juftliklar: [(Ali, Dasturchi), (Vali, Dizayner), (G'ani, Menejer)]
Ajratilgan ismlar: [Ali, Vali, G'ani]
Ajratilgan rollar: [Dasturchi, Dizayner, Menejer]"""
    ),
    (
        611,
        "Lug'at yasash: associateBy va associateWith",
        "Obyektlar ro'yxatidan ma'lum kalit yoki qiymat bo'yicha tezkor Map shakllantirish.",
        """data class UserRecord(val id: Int, val name: String)

fun main() {
    val users = listOf(
        UserRecord(101, "Jasur"),
        UserRecord(102, "Malika")
    )

    // associateBy: Kalit tanlanadi, qiymat esa obyektning o'zi bo'ladi
    val userMapById: Map<Int, UserRecord> = users.associateBy { it.id }

    // associateWith: Element kalit bo'ladi, qiymat esa lambda dan hisoblanadi
    val names = listOf("Toshkent", "Buxoro")
    val nameLengthMap = names.associateWith { it.length }

    println("UserMap: $userMapById")
    println("NameLengthMap: $nameLengthMap")
}""",
        "'associateBy' ID bo'yicha indekslashda, 'associateWith' esa mavjud to'plam elementlariga hisoblangan qiymat biriktirishda juda qulaydir.",
        """UserMap: {101=UserRecord(id=101, name=Jasur), 102=UserRecord(id=102, name=Malika)}
NameLengthMap: {Toshkent=8, Buxoro=6}"""
    ),
    (
        612,
        "Guruhlash operatsiyasi: groupBy",
        "Xodimlarni o'zlarining bo'limlari (department) bo'yicha avtomatik guruhlarga ajrating.",
        """data class Staff(val name: String, val department: String)

fun main() {
    val staffList = listOf(
        Staff("Alisher", "IT"),
        Staff("Nodira", "HR"),
        Staff("Sardor", "IT"),
        Staff("Kamola", "HR"),
        Staff("Temur", "Moliya")
    )

    val groupedByDept: Map<String, List<Staff>> = staffList.groupBy { it.department }

    println("Bo'limlar bo'yicha:")
    groupedByDept.forEach { (dept, members) ->
        println("[$dept]: ${members.map { it.name }}")
    }
}""",
        "'groupBy' ma'lumotlar tahlilida markaziy metod bo'lib, umumiy kalitga ega bo'lgan barcha elementlarni 'Map<Key, List<Value>>' ko'rinishida yig'adi.",
        """Bo'limlar bo'yicha:
[IT]: [Alisher, Sardor]
[HR]: [Nodira, Kamola]
[Moliya]: [Temur]"""
    ),
    (
        613,
        "Ikkiga ajratish: partition",
        "Ro'yxatni bitta o'tishda shart bo'yicha ikkita ro'yxatga (Pair<List, List>) ajratish.",
        """fun main() {
    val numbers = listOf(1, 2, 3, 4, 5, 6, 7, 8)

    val (evenNumbers, oddNumbers) = numbers.partition { it % 2 == 0 }

    println("Juft sonlar: $evenNumbers")
    println("Toq sonlar: $oddNumbers")
}""",
        "'partition' bitta predikat orqali ikkita to'liq ro'yxat qaytaradi: true bo'lganlar birinchi, false bo'lganlar ikkinchi ro'yxatga tushadi.",
        """Juft sonlar: [2, 4, 6, 8]
Toq sonlar: [1, 3, 5, 7]"""
    ),
    (
        614,
        "Agregat hisob-kitoblar: sumOf va average",
        "Obyektlar ro'yxatidagi ma'lum xususiyat bo'yicha umumiy summani hisoblang.",
        """data class CartItem(val name: String, val price: Double, val qty: Int)

fun main() {
    val cart = listOf(
        CartItem("Kitob", 45000.0, 2),
        CartItem("Qalam", 5000.0, 5),
        CartItem("Daftar", 10000.0, 3)
    )

    val totalAmount = cart.sumOf { it.price * it.qty }
    val averageItemPrice = cart.map { it.price }.average()

    println("Savatning umumiy summasi: %,.0f UZS".format(totalAmount))
    println("O'rtacha mahsulot narxi: %,.0f UZS".format(averageItemPrice))
}""",
        "'sumOf' arifmetik hisob-kitoblarni bitta lambda orqali tezkor va xotirani tejagan holda hisoblab beradi.",
        """Savatning umumiy summasi: 145,000 UZS
O'rtacha mahsulot narxi: 20,000 UZS"""
    ),
    (
        615,
        "Ekstremumlarni topish: maxByOrNull va minByOrNull",
        "Kolleksiyadagi eng qimmat va eng arzon mahsulot obyektini topish.",
        """data class Product(val title: String, val price: Double)

fun main() {
    val products = listOf(
        Product("Sichqoncha", 25.0),
        Product("Monitor", 300.0),
        Product("Klaviatura", 75.0)
    )

    val mostExpensive = products.maxByOrNull { it.price }
    val cheapest = products.minByOrNull { it.price }

    println("Eng qimmat mahsulot: ${mostExpensive?.title} ($${mostExpensive?.price})")
    println("Eng arzon mahsulot: ${cheapest?.title} ($${cheapest?.price})")
}""",
        "'maxByOrNull' berilgan hisoblash bo'yicha eng katta elementni, ro'yxat bo'sh bo'lsa null qaytaradi.",
        """Eng qimmat mahsulot: Monitor ($300.0)
Eng arzon mahsulot: Sichqoncha ($25.0)"""
    ),
    (
        616,
        "Akkumulyator: fold va boshlang'ich qiymat",
        "Boshlang'ich qiymat bilan ro'yxatni bitta satrga yoki songa umumlashtirish.",
        """fun main() {
    val numbers = listOf(1, 2, 3, 4, 5)

    // Boshlang'ich 10 ga qo'shib borish:
    val total = numbers.fold(10) { accumulator, number ->
        accumulator + number
    }

    println("Fold natijasi: $total")
}""",
        "'fold(initial) { acc, elem -> ... }' boshlang'ich qiymatdan boshlab har bir elementni akkumulyatorga qo'shib boradi.",
        """Fold natijasi: 25"""
    ),
    (
        617,
        "Akkumulyator: reduce (boshlang'ich qiymatsiz)",
        "Birinchi elementni boshlang'ich qiymat deb oluvchi 'reduce' funksiyasi.",
        """fun main() {
    val words = listOf("Kotlin", "chuqur", "o'rganish")

    val sentence = words.reduce { acc, s -> "$acc $s" }

    println("Jumlalar: $sentence")
}""",
        "'reduce' ro'yxatning birinchi elementini boshlang'ich qiymat sifatida oladi. Ro'yxat bo'sh bo'lsa 'UnsupportedOperationException' tashlaydi, shuning uchun 'reduceOrNull' tavsiya etiladi.",
        """Jumlalar: Kotlin chuqur o'rganish"""
    ),
    (
        618,
        "Oraliq akkumulyatsiyalar: runningFold va scan",
        "Har bir qadamdagi jamg'arilgan balansni ro'yxat ko'rinishida hosil qiling.",
        """fun main() {
    val cashFlows = listOf(100, -20, 50, -30)

    val runningBalance = cashFlows.runningFold(0) { currentBalance, transaction ->
        currentBalance + transaction
    }

    println("Tranzaksiyalar: $cashFlows")
    println("Balans dinamikasi: $runningBalance")
}""",
        "'runningFold' (yoki 'scan') barcha oraliq natijalarni saqlab boradi. Bu moliyaviy o'sish va grafiklar uchun juda qulay.",
        """Tranzaksiyalar: [100, -20, 50, -30]
Balans dinamikasi: [0, 100, 80, 130, 100]"""
    ),
    (
        619,
        "Qirqish va o'tkazib yuborish: take, drop, takeWhile, dropWhile",
        "Ro'yxatdan boshidan N ta olish yoki ma'lum shart tugaguncha o'tkazib yuborish.",
        """fun main() {
    val numbers = listOf(2, 4, 6, 7, 8, 10)

    println("Dastlabki 3 tasi: ${numbers.take(3)}")
    println("Dastlabki 2 tasi tashlab yuborildi: ${numbers.drop(2)}")
    println("Juft sonlar tugaguncha (takeWhile): ${numbers.takeWhile { it % 2 == 0 }}")
    println("Birinchi toq songacha tashlash (dropWhile): ${numbers.dropWhile { it % 2 == 0 }}")
}""",
        "'takeWhile' birinchi marta shart buzilishi bilanoq yig'ishni to'xtatadi. 'dropWhile' esa shart buzilgandan so'ng qolgan barcha elementlarni saqlab qoladi.",
        """Dastlabki 3 tasi: [2, 4, 6]
Dastlabki 2 tasi tashlab yuborildi: [6, 7, 8, 10]
Juft sonlar tugaguncha (takeWhile): [2, 4, 6]
Birinchi toq songacha tashlash (dropWhile): [7, 8, 10]"""
    ),
    (
        620,
        "Oyna bo'yicha surilish: windowed funksiyasi",
        "Harakatlanuvchi oyna (moving window) orqali ketma-ket elementlar guruhini tahlil qilish.",
        """fun main() {
    val temperatures = listOf(20, 22, 21, 24, 25, 23)

    // 3 kunlik o'rtacha oyna (size=3, step=1):
    val movingWindows = temperatures.windowed(size = 3, step = 1)

    println("3 kunlik oynalar: $movingWindows")
    movingWindows.forEach { window ->
        println("Oyna: $window -> O'rtacha: %.1f".format(window.average()))
    }
}""",
        "'windowed' signallar tahlili, harakatlanuvchi o'rtacha (moving average) va vaqt qatorlarini hisoblashda ishlatiladi.",
        """3 kunlik oynalar: [[20, 22, 21], [22, 21, 24], [21, 24, 25], [24, 25, 23]]
Oyna: [20, 22, 21] -> O'rtacha: 21.0
Oyna: [22, 21, 24] -> O'rtacha: 22.3
Oyna: [21, 24, 25] -> O'rtacha: 23.3
Oyna: [24, 25, 23] -> O'rtacha: 24.0"""
    ),
    (
        621,
        "Sequences (Ketma-ketliklar) va Tembel hisoblash (Lazy Evaluation)",
        "Katta hajmdagi kolleksiyalarda oraliq ro'yxatlar yaratilishini oldini olish uchun 'asSequence()' dan foydalaning.",
        """fun main() {
    val numbers = (1..100).toList()

    // Sequences orqali: elementlar bittalab butun zanjirdan o'tadi
    val result = numbers.asSequence()
        .filter { 
            it % 2 == 0 
        }
        .map { 
            it * it 
        }
        .take(3)
        .toList()

    println("Dastlabki 3 ta juft son kvadrati: $result")
}""",
        "Oddiy 'Iterable' zanjirlarida (filter, map) har bir qadam butun ro'yxatni o'z ichiga olgan yangi oraliq to'plam yaratadi (Eager evaluation). 'Sequence' esa tembel (lazy) ishlaydi: har bir element terminal operator ('toList') chaqirilgandagina bittalab barcha bosqichlardan o'tadi.",
        """Dastlabki 3 ta juft son kvadrati: [4, 16, 36]"""
    ),
    (
        622,
        "Cheksiz ketma-ketliklar: generateSequence",
        "Tugash chegarasi bo'lmagan cheksiz sonlar ketma-ketligini 'generateSequence' orqali hosil qiling.",
        """fun main() {
    // 2 ning darajalari cheksiz ketma-ketligi: 1, 2, 4, 8, 16, ...
    val powersOfTwo = generateSequence(1) { it * 2 }

    val firstFive = powersOfTwo.take(5).toList()
    val eighthPower = powersOfTwo.elementAt(7)

    println("Dastlabki 5 ta daraja: $firstFive")
    println("8-chi element (2^7): $eighthPower")
}""",
        "'generateSequence(seed) { next }' cheksiz ketma-ketlik yaratadi. 'take(n)' kabi cheklovchi operatorlar orqali kerakli miqdori olinadi.",
        """Dastlabki 5 ta daraja: [1, 2, 4, 8, 16]
8-chi element (2^7): 128"""
    ),
    (
        623,
        "Sequence va Iterable hisoblash tartibi farqi",
        "Eager va Lazy hisoblash ketma-ketligini konsolga chiqarish orqali amalda solishtiring.",
        """fun main() {
    println("--- ITERABLE (Eager) ---")
    listOf(1, 2, 3)
        .filter { println("Filter: $it"); it > 1 }
        .map { println("Map: $it"); it * 2 }

    println("--- SEQUENCE (Lazy) ---")
    sequenceOf(1, 2, 3)
        .filter { println("Seq Filter: $it"); it > 1 }
        .map { println("Seq Map: $it"); it * 2 }
        .toList()
}""",
        "Iterable avval barcha elementlarni filtrlaydi, so'ngra yangi ro'yxatni to'liq map qiladi. Sequence esa har bir elementni navbatma-navbat (vertikal tarzda) filter va map dan o'tkazadi.",
        """--- ITERABLE (Eager) ---
Filter: 1
Filter: 2
Filter: 3
Map: 2
Map: 3
--- SEQUENCE (Lazy) ---
Seq Filter: 1
Seq Filter: 2
Seq Map: 2
Seq Filter: 3
Seq Map: 3"""
    ),
    (
        624,
        "Cheksiz Fibonachchi Ketma-ketligi Sequence bilan",
        "Kotlindaki 'sequence { yield(...) }' generatori yordamida Fibonachchi sonlarini hosil qiling.",
        """fun fibonacciSequence(): Sequence<Long> = sequence {
    var a = 0L
    var b = 1L
    while (true) {
        yield(a) // Qiymatni navbatdagi qadamga uzatish
        val next = a + b
        a = b
        b = next
    }
}

fun main() {
    val fibs = fibonacciSequence().take(8).toList()
    println("Dastlabki 8 ta Fibonachchi soni: $fibs")
}""",
        "'sequence { yield(value) }' bloki Python dagi generatorlarga o'xshash bo'lib, koroutina mexanizmi asosida har safar qiymat so'ralganda bitta qadam bajaradi va to'xtab turadi.",
        """Dastlabki 8 ta Fibonachchi soni: [0, 1, 1, 2, 3, 5, 8, 13]"""
    ),
    (
        625,
        "Kolleksiyani saralash: sorted, sortedBy, sortedWith",
        "Obyektlarni bir nechta mezonlar bo'yicha tartiblash.",
        """data class Student(val name: String, val score: Double)

fun main() {
    val students = listOf(
        Student("Jasur", 85.5),
        Student("Malika", 95.0),
        Student("Alisher", 85.5)
    )

    val sortedByScoreDesc = students.sortedByDescending { it.score }
    val multiSorted = students.sortedWith(
        compareByDescending<Student> { it.score }.thenBy { it.name }
    )

    println("Ball bo'yicha kamayish:")
    multiSorted.forEach { println(" - ${it.name}: ${it.score}") }
}""",
        "'sortedWith' bir nechta shartlar ketma-ketligi (thenBy) orqali nozik va qat'iy tartiblashni amalga oshiradi.",
        """Ball bo'yicha kamayish:
 - Malika: 95.0
 - Alisher: 85.5
 - Jasur: 85.5"""
    ),
    (
        626,
        "Kolleksiyalarda o'zaro ayirma va kesishma: intersect va subtract",
        "To'plamlar ustida matematik munosabatlarni bajarish.",
        """fun main() {
    val setA = setOf(1, 2, 3, 4, 5)
    val setB = setOf(4, 5, 6, 7, 8)

    val intersection = setA intersect setB // Kesishma
    val difference = setA subtract setB   // Ayirma
    val union = setA union setB           // Birlashma

    println("Kesishma (ikkalasida ham bor): $intersection")
    println("Ayirma (faqat A da bor): $difference")
    println("Birlashma (barchasi): $union")
}""",
        "Kotlinda to'plamlar ustida matematik 'intersect', 'subtract' va 'union' infix funksiyalari mavjud.",
        """Kesishma (ikkalasida ham bor): [4, 5]
Ayirma (faqat A da bor): [1, 2, 3]
Birlashma (barchasi): [1, 2, 3, 4, 5, 6, 7, 8]"""
    ),
    (
        627,
        "Kolleksiyadagi dublikatlar sonini hisoblash",
        "Elementlarning nechtadan takrorlanganini bitta amalda chiqarish.",
        """fun main() {
    val votes = listOf("A", "B", "A", "C", "A", "B", "A")

    val voteCounts: Map<String, Int> = votes.groupingBy { it }.eachCount()

    println("Ovozlar soni: $voteCounts")
}""",
        "'groupingBy { it }.eachCount()' grouping operatsiyasini optimallashtirib, oraliq ro'yxatlar yaratmasdan bevosita har bir element sonini hisoblaydi.",
        """Ovozlar soni: {A=4, B=2, C=1}"""
    ),
    (
        628,
        "Map ustida filtrlash va xaritalash: filterKeys va mapValues",
        "Lug'atning faqat kalitlarini filtrlash va faqat qiymatlarini o'zgartirish.",
        """fun main() {
    val salariesInUsd = mapOf("Ali" to 1000.0, "Vali" to 1500.0, "G'ani" to 800.0)

    val salariesInUzs = salariesInUsd.mapValues { (_, usd) -> usd * 12800.0 }
    val highEarners = salariesInUsd.filterValues { it >= 1000.0 }

    println("So'mdagi maoshlar: $salariesInUzs")
    println("1000+ topuvchilar: $highEarners")
}""",
        "'mapValues' va 'filterValues' xaritalar bilan ishlashda kalitlarga tegmasdan faqat qiymatlar ustida amal bajaradi.",
        """So'mdagi maoshlar: {Ali=1.28E7, Vali=1.92E7, G'ani=1.024E7}
1000+ topuvchilar: {Ali=1000.0, Vali=1500.0}"""
    ),
    (
        629,
        "Kolleksiyaning faqat birinchi va oxirgi elementlarini almashtirish",
        "Birinchi va oxirgi elementni qulay olish va o'zgartirish.",
        """fun main() {
    val items = listOf("Bosh", "O'rta", "Oxir")

    println("Birinchi: ${items.first()}, Oxirgi: ${items.last()}")
    println("firstOrNull (bo'sh bo'lganda ham xavfsiz): ${emptyList<String>().firstOrNull()}")
}""",
        "'first()' va 'last()' elementlarni boshidan yoki oxiridan o'qiydi.",
        """Birinchi: Bosh, Oxirgi: Oxir
firstOrNull (bo'sh bo'lganda ham xavfsiz): null"""
    ),
    (
        630,
        "Shartli boshqaruv: chunked bilan sahifalab chiqarish",
        "Kitob qahramonlari ro'yxatini 2 tadan qilib sahifalash.",
        """fun main() {
    val heroes = listOf("Alpomish", "Go'ro'g'li", "Rustam", "Suxrob", "Avazxon")

    val pages = heroes.chunked(2)
    for ((pageNum, page) in pages.withIndex()) {
        println("Sahifa #${pageNum + 1}: $page")
    }
}""",
        "'chunked' orqali katta to'plamlarni sahifalarga (pages) ajratish juda qulaydir.",
        """Sahifa #1: [Alpomish, Go'ro'g'li]
Sahifa #2: [Rustam, Suxrob]
Sahifa #3: [Avazxon]"""
    ),
    (
        631,
        "Kolleksiyalarda qidiruv: binarySearch",
        "Saralangan ro'yxatda binar qidiruv orqali element indeksini topish.",
        """fun main() {
    val sortedNumbers = listOf(10, 20, 30, 40, 50, 60)

    val index = sortedNumbers.binarySearch(40)
    println("40 soni indeksi: $index")
}""",
        "Saralangan kolleksiyalarda 'binarySearch' logarifmik vaqtda O(log N) qidiradi.",
        """40 soni indeksi: 3"""
    ),
    (
        632,
        "Kolleksiyalarda o'zgartirilmaslikni ta'minlash: toList va toSet nusxalari",
        "Mutable to'plamdan o'zgarmas nusxa olish.",
        """fun main() {
    val mutable = mutableListOf("A", "B")
    val immutableCopy = mutable.toList() // Mustaqil yangi o'zgarmas nusxa

    mutable.add("C")

    println("Mutable ro'yxat: $mutable")
    println("Nusxa ro'yxat: $immutableCopy")
}""",
        "'toList()' orqali olingan nusxa asl ro'yxat o'zgarganda ham o'zgarishsiz qoladi.",
        """Mutable ro'yxat: [A, B, C]
Nusxa ro'yxat: [A, B]"""
    ),
    (
        633,
        "Elementlarni tasodifiy aralashtirish: shuffled",
        "Kolleksiya elementlarini tasodifiy tartibda aralashtirib yangi ro'yxat olish.",
        """fun main() {
    val cards = listOf("Tuz", "Qirol", "Dama", "Valet")
    val shuffledCards = cards.shuffled()

    println("Asl tartib: $cards")
    println("Aralashtirilgan: $shuffledCards")
}""",
        "'shuffled()' to'plam elementlarini tasodifiy tartibda aralashtiradi.",
        """Asl tartib: [Tuz, Qirol, Dama, Valet]
Aralashtirilgan: ko'rsatiladi."""
    ),
    (
        634,
        "Shartli kamayish: reduceRight va foldRight",
        "Elementlarni o'ngdan chapga qarab yig'ib borish.",
        """fun main() {
    val letters = listOf("A", "B", "C")

    val fromLeft = letters.reduce { acc, s -> "$acc-$s" }
    val fromRight = letters.reduceRight { s, acc -> "$s-$acc" }

    println("Chapdan yig'ish: $fromLeft")
    println("O'ngdan yig'ish: $fromRight")
}""",
        "'reduceRight' o'ng tomondan boshlab amallarni teskari ketma-ketlikda bajaradi.",
        """Chapdan yig'ish: A-B-C
O'ngdan yig'ish: A-B-C"""
    ),
    (
        635,
        "Kolleksiyalarda null qiymatlarni sanash",
        "Ro'yxat ichidagi null larni to'g'ri hisoblash.",
        """fun main() {
    val mixed: List<String?> = listOf("A", null, "B", null, "C", null)

    val nullCount = mixed.count { it == null }
    val validCount = mixed.count { it != null }

    println("Null elementlar: $nullCount ta")
    println("Yaroqli elementlar: $validCount ta")
}""",
        "'count { predicate }' orqali filtrlangan to'plam yaratmasdan to'g'ridan-to'g'ri sanash.",
        """Null elementlar: 3 ta
Yaroqli elementlar: 3 ta"""
    ),
    (
        636,
        "Lug'atda sukut qiymati: withDefault",
        "Map da mavjud bo'lmagan kalit so'ralganda xatoliksiz standart javob qaytarish.",
        """fun main() {
    val baseMap = mapOf("A" to 1, "B" to 2)
    val mapWithDefault = baseMap.withDefault { key -> key.length }

    println("A: ${mapWithDefault.getValue("A")}")
    println("HELLO: ${mapWithDefault.getValue("HELLO")}")
}""",
        "'withDefault' mavjud bo'lmagan kalit uchun dinamik hisoblangan qiymatni beradi.",
        """A: 1
HELLO: 5"""
    ),
    (
        637,
        "Kolleksiyadagi yagona elementni olish: single va singleOrNull",
        "To'plamda aniq bitta element borligini tekshirish.",
        """fun main() {
    val singleList = listOf("Yagona")
    val multiList = listOf("A", "B")

    println("Yagona element: ${singleList.singleOrNull()}")
    println("Ko'p elementli: ${multiList.singleOrNull()}")
}""",
        "'singleOrNull' agar ro'yxatda aniq bitta element bo'lsa uni qaytaradi, aks holda null beradi.",
        """Yagona element: Yagona
Ko'p elementli: null"""
    ),
    (
        638,
        "Shartli guruhlash: aggregate va fold in groupingBy",
        "Har bir guruh bo'yicha yig'indini hisoblash.",
        """data class Expense(val category: String, val amount: Double)

fun main() {
    val expenses = listOf(
        Expense("Oziq-ovqat", 50.0),
        Expense("Transport", 20.0),
        Expense("Oziq-ovqat", 30.0)
    )

    val totalsByCategory = expenses.groupingBy { it.category }
        .fold(0.0) { acc, expense -> acc + expense.amount }

    println("Kategoriyalar bo'yicha jami: $totalsByCategory")
}""",
        "'groupingBy { ... }.fold' katta hajmdagi xarajatlarni toifalar bo'yicha bitta qadamda hisoblaydi.",
        """Kategoriyalar bo'yicha jami: {Oziq-ovqat=80.0, Transport=20.0}"""
    ),
    (
        639,
        "Kolleksiyadagi eng ko'p takrorlangan elementni topish (Mode)",
        "Ro'yxatdagi modani (eng ko'p uchragan qiymat) aniqlash.",
        """fun <T> findMode(items: List<T>): T? {
    return items.groupingBy { it }.eachCount().maxByOrNull { it.value }?.key
}

fun main() {
    val scores = listOf(5, 3, 4, 5, 2, 5, 4, 3)
    println("Moda qiymat: ${findMode(scores)}")
}""",
        "'groupingBy' va 'eachCount' orqali modani O(N) vaqtda topish.",
        """Moda qiymat: 5"""
    ),
    (
        640,
        "Kolleksiyani teskari qilib bog'lash: zipWithNext",
        "Ketma-ket qo'shni elementlarni juftlik qilib bog'lash.",
        """fun main() {
    val points = listOf(0, 10, 25, 40)

    // Qo'shni elementlar orasidagi farqni topish:
    val diffs = points.zipWithNext { a, b -> b - a }

    println("Nuqtalar: $points")
    println("Oraliq masofalar: $diffs")
}""",
        "'zipWithNext { a, b -> ... }' har bir elementni o'zidan keyingi element bilan juftlaydi.",
        """Nuqtalar: [0, 10, 25, 40]
Oraliq masofalar: [10, 15, 15]"""
    ),
    (
        641,
        "Kolleksiyalarda indeksli qidiruv: indexOfFirst va indexOfLast",
        "Shartga mos birinchi va oxirgi element indekslarini topish.",
        """fun main() {
    val numbers = listOf(5, 12, 19, 24, 7)

    val firstEvenIdx = numbers.indexOfFirst { it % 2 == 0 }
    val lastEvenIdx = numbers.indexOfLast { it % 2 == 0 }

    println("Birinchi juft indeks: $firstEvenIdx")
    println("Oxirgi juft indeks: $lastEvenIdx")
}""",
        "Predikatga mos kelgan indeksni tezkor aniqlash.",
        """Birinchi juft indeks: 1
Oxirgi juft indeks: 3"""
    ),
    (
        642,
        "Kolleksiyadan o'chirish: removeAll va retainAll",
        "MutableList dan shart bo'yicha elementlarni olib tashlash.",
        """fun main() {
    val list = mutableListOf(1, 2, 3, 4, 5, 6)

    list.removeAll { it % 2 == 0 } // Barcha juftlarni o'chirish
    println("Faqat toqlar qoldi: $list")
}""",
        "'removeAll { predicate }' ro'yxatni joyida (in-place) tozalaydi.",
        """Faqat toqlar qoldi: [1, 3, 5]"""
    ),
    (
        643,
        "Shartli to'plash: flatMapIndexed",
        "Indeksni hisobga olgan holda ro'yxatni tekislab yoyish.",
        """fun main() {
    val items = listOf("A", "B")

    val expanded = items.flatMapIndexed { index, s ->
        listOf("$s-$index", "$s-${index + 1}")
    }

    println("Kengaytirilgan: $expanded")
}""",
        "Indeksli transformatsiyani tekislash bilan birlashtirish.",
        """Kengaytirilgan: [A-0, A-1, B-1, B-2]"""
    ),
    (
        644,
        "Kolleksiyalarda yagona kalitlar bo'yicha filtr: distinctBy",
        "Faqat ma'lum maydoni bo'yicha takrorlanmas obyektlarni qoldirish.",
        """data class Device(val id: Int, val name: String)

fun main() {
    val devices = listOf(
        Device(1, "Phone"),
        Device(2, "Tablet"),
        Device(1, "Phone (Duplicate)")
    )

    val uniqueDevices = devices.distinctBy { it.id }
    println("Yagona qurilmalar: $uniqueDevices")
}""",
        "'distinctBy' orqali ID bo'yicha takrorlanishlarni tozalash.",
        """Yagona qurilmalar: [Device(id=1, name=Phone), Device(id=2, name=Tablet)]"""
    ),
    (
        645,
        "Kolleksiyaning elementlari ko'paytmasini hisoblash",
        "Sonlar ko'paytmasini 'reduce' orqali topish.",
        """fun main() {
    val factors = listOf(2, 3, 4)
    val product = factors.reduce { acc, n -> acc * n }
    println("Ko'paytma: $product")
}""",
        "Sonlar ko'paytmasini bitta qatorda hisoblash.",
        """Ko'paytma: 24"""
    ),
    (
        646,
        "Sequence bilan fayl qatorlarini tembel o'qish simulyatsiyasi",
        "Katta matnlarni xotiraga to'liq yuklamasdan oqimda tahlil qilish.",
        """fun main() {
    val simulatedLines = sequenceOf(
        "INFO: Baza ulandi",
        "WARN: Xotira kam",
        "ERROR: Aloqa uzildi",
        "INFO: Qayta ulandi"
    )

    val firstError = simulatedLines
        .filter { it.startsWith("ERROR") }
        .firstOrNull()

    println("Birinchi xatolik: $firstError")
}""",
        "Katta hajmdagi log fayllarni 'Sequence' orqali samarali tekshirish.",
        """Birinchi xatolik: ERROR: Aloqa uzildi"""
    ),
    (
        647,
        "Kolleksiyalar bilan Shartli Matn Birlashtirish: joinTo va joinToString",
        "Chiroyli formatda prefiks va postfiks bilan matn hosil qilish.",
        """fun main() {
    val cities = listOf("Toshkent", "Samarqand", "Xiva")

    val formatted = cities.joinToString(
        separator = " -> ",
        prefix = "Marshrut: [",
        postfix = "]",
        limit = 2,
        truncated = "va boshqalar"
    )

    println(formatted)
}""",
        "'joinToString' boy parametrlari bilan matnlarni mukammal formatlaydi.",
        """Marshrut: [Toshkent -> Samarqand -> va boshqalar]"""
    ),
    (
        648,
        "Sequence bilan Murakkab Tub Sonlar Oqimi",
        "Cheksiz tub sonlar generatorini sequence orqali tuzing.",
        """fun primesSequence(): Sequence<Int> = sequence {
    var n = 2
    while (true) {
        var isPrime = true
        for (i in 2..Math.sqrt(n.toDouble()).toInt()) {
            if (n % i == 0) { isPrime = false; break }
        }
        if (isPrime) yield(n)
        n++
    }
}

fun main() {
    val firstFivePrimes = primesSequence().take(5).toList()
    println("Dastlabki 5 ta tub son: $firstFivePrimes")
}""",
        "'yield' yordamida tub sonlarni talabga ko'ra bittalab ishlab chiqaruvchi cheksiz oqim.",
        """Dastlabki 5 ta tub son: [2, 3, 5, 7, 11]"""
    ),
    (
        649,
        "Kolleksiyada o'rta arifmetik va dispersiyani hisoblash",
        "Statistik ko'rsatkichlarni bitta o'tishda hisoblash.",
        """fun main() {
    val data = listOf(10.0, 12.0, 23.0, 23.0, 16.0, 23.0, 21.0, 16.0)
    val mean = data.average()
    val variance = data.sumOf { (it - mean) * (it - mean) } / data.size

    println("O'rtacha: %.2f".format(mean))
    println("Dispersiya: %.2f".format(variance))
}""",
        "Kolleksiya operatsiyalari bilan statistik hisob-kitoblar.",
        """O'rtacha: 18.00
Dispersiya: 24.50"""
    ),
    (
        650,
        "Kolleksiyalar va operatsiyalar bo'yicha to'liq amaliy xulosa: Elektron Do'kon Tahlilchisi",
        "List, Set, Map, filter, map, flatMap, groupBy, fold, Sequences va terminal operatsiyalarni bitta yaxlit savdo tahlilida birlashtiring.",
        """data class SaleRecord(val category: String, val product: String, val amount: Double)

fun main() {
    val sales = listOf(
        SaleRecord("Elektronika", "Smartfon", 800.0),
        SaleRecord("Kiyim", "Kurtka", 120.0),
        SaleRecord("Elektronika", "Quloqchin", 50.0),
        SaleRecord("Oziq-ovqat", "Choy", 15.0),
        SaleRecord("Elektronika", "Planshet", 400.0),
        SaleRecord("Kiyim", "Shim", 60.0)
    )

    // 1. Sequence orqali katta sotuvlarni filtrlash va transformatsiya
    val topSales = sales.asSequence()
        .filter { it.amount >= 50.0 }
        .sortedByDescending { it.amount }
        .toList()

    // 2. Kategoriya bo'yicha guruhlash
    val salesByCategory = sales.groupBy { it.category }

    // 3. Har bir kategoriya bo'yicha jami summani fold orqali hisoblash
    val totalByCategory = salesByCategory.mapValues { (_, records) ->
        records.fold(0.0) { sum, r -> sum + r.amount }
    }

    // 4. Umumiy daromad
    val grandTotal = sales.sumOf { it.amount }

    println("=== SAVDO TAHLILI HISOBOTI ===")
    println("Umumiy tushum: $$grandTotal")
    println("Kategoriyalar bo'yicha tushum:")
    totalByCategory.forEach { (cat, sum) ->
        println(" - $cat: $$sum")
    }
    println("Katta sotuvlar (>= $50): ${topSales.map { "${it.product} ($${it.amount})" }}")
}""",
        "Ushbu yakuniy topshiriqda talab qilingan barcha kolleksiya amallari: Sequence, filter, map, groupBy, fold, sumOf va mapValues to'laqonli elektron savdo tahlili misolida professional birlashtirildi.",
        """=== SAVDO TAHLILI HISOBOTI ===
Umumiy tushum: $1445.0
Kategoriyalar bo'yicha tushum:
 - Elektronika: $1250.0
 - Kiyim: $180.0
 - Oziq-ovqat: $15.0
Katta sotuvlar (>= $50): [Smartfon ($800.0), Planshet ($400.0), Kurtka ($120.0), Shim ($60.0), Quloqchin ($50.0)]"""
    )
]

for item in data_13:
    n, title, condition, sol, exp, res = item
    tasks.append(format_task(n, title, condition, sol, exp, res))

save_file("kotlin_13_kolleksiyalar_va_operatsiyalar.md", tasks)
