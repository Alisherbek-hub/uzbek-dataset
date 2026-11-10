# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

data_01 = [
    (
        1,
        "O'zgarmas o'zgaruvchi e'lon qilish: 'val' kalit so'zi",
        "Dasturda foydalanuvchining ID raqami va ro'yxatdan o'tgan sanasini o'zgarmas (read-only) shaklda e'lon qiling. Ularni chop eting.",
        """fun main() {
    val userId: Long = 100452L
    val registrationDate: String = "2026-03-15"
    
    println("Foydalanuvchi ID: $userId")
    println("Ro'yxatdan o'tgan sana: $registrationDate")
}""",
        "Kotlinda 'val' (value) kalit so'zi o'zgarmas o'zgaruvchi e'lon qilish uchun ishlatiladi. Java tilidagi 'final' kalit so'ziga to'g'ri keladi. Bir marta qiymat biriktirilgach, uni qayta o'zgartirib bo'lmaydi, bu esa ko'p oqimli (multithreaded) muhitda immutability (o'zgarmaslik) tamoyilini ta'minlaydi.",
        """Foydalanuvchi ID: 100452
Ro'yxatdan o'tgan sana: 2026-03-15"""
    ),
    (
        2,
        "O'zgaruvchan qiymatlar: 'var' kalit so'zi bilan ishlash",
        "Onlayn do'konda xarid savatidagi tovarlar soni va umumiy summani saqlovchi o'zgaruvchilar e'lon qiling. Yangi mahsulot qo'shilganda ularning qiymatini oshiring va yangilangan natijani chiqaring.",
        """fun main() {
    var itemCount: Int = 3
    var totalAmount: Double = 150.0
    
    println("Boshlang'ich holat: Mahsulotlar: $itemCount ta, Jami: $$totalAmount")
    
    // Yangi mahsulot qo'shildi
    itemCount += 2
    totalAmount += 95.5
    
    println("Yangilangan holat: Mahsulotlar: $itemCount ta, Jami: $$totalAmount")
}""",
        "'var' (variable) o'zgaruvchan kattaliklarni e'lon qilishda qo'llaniladi. Uning qiymati dastur bajarilishi davomida istalgancha qayta belgilanishi mumkin, ammo uning ma'lumot turi o'zgarmas bo'lib qoladi (masalan, Int turidagi o'zgaruvchiga String yozib bo'lmaydi).",
        """Boshlang'ich holat: Mahsulotlar: 3 ta, Jami: $150.0
Yangilangan holat: Mahsulotlar: 5 ta, Jami: $245.5"""
    ),
    (
        3,
        "Tipni avtomatik aniqlash (Type Inference)",
        "O'zgaruvchi turini aniq (explicit) ko'rsatmasdan turli tiplardagi o'zgaruvchilarni e'lon qiling. Kotlin kompilyatori ularning turini qanday aniqlaganini tekshirib ko'ring.",
        """fun main() {
    val siteName = "TechUzbekistan"
    val visitorCount = 45000
    val rating = 4.95
    val isActive = true
    
    println("Sayt nomi: $siteName (Turi: ${siteName::class.simpleName})")
    println("Tashrif buyuruvchilar: $visitorCount (Turi: ${visitorCount::class.simpleName})")
    println("Reyting: $rating (Turi: ${rating::class.simpleName})")
    println("Faol: $isActive (Turi: ${isActive::class.simpleName})")
}""",
        "Kotlin kuchli statik tiplashtirilgan til bo'lishiga qaramay, 'Type Inference' (tur xulosasi) xususiyatiga ega. Agar boshlang'ich qiymat berilsa, kompilyator kontekstga qarab o'zgaruvchi turini avtomatik ravishda belgilaydi. '::class.simpleName' orqali o'zgaruvchining Kotlin klass turi aniqlanadi.",
        """Sayt nomi: TechUzbekistan (Turi: String)
Tashrif buyuruvchilar: 45000 (Turi: Int)
Reyting: 4.95 (Turi: Double)
Faol: true (Turi: Boolean)"""
    ),
    (
        4,
        "Butun sonli tiplar: Byte va Short bilan xotirani tejash",
        "Sensor qurilmasidan keluvchi batareya quvvati foizi (0..100) va harorat qiymatini (-50..50) minimal xotira egallaydigan tiplarda saqlang.",
        """fun main() {
    val batteryPercentage: Byte = 85
    val ambientTemp: Short = -15
    
    println("Batareya quvvati: $batteryPercentage%")
    println("Atrof-muhit harorati: $ambientTemp°C")
    println("Byte min: ${Byte.MIN_VALUE}, max: ${Byte.MAX_VALUE}")
    println("Short min: ${Short.MIN_VALUE}, max: ${Short.MAX_VALUE}")
}""",
        "Byte 8-bitli butun son bo'lib (-128 dan 127 gacha), Short 16-bitli son (-32768 dan 32767 gacha). IoT yoki xotira cheklangan tizimlarda Int (32-bit) o'rniga Byte yoki Short qo'llash katta massivlarda xotiradan foydalanish samaradorligini 2-4 barobar oshiradi.",
        """Batareya quvvati: 85%
Atrof-muhit harorati: -15°C
Byte min: -128, max: 127
Short min: -32768, max: 32767"""
    ),
    (
        5,
        "Katta sonlar: Long turi va L prefiksi",
        "Dunyo aholisi soni va yorug'likning 1 yilda bosib o'tadigan masofasini (metrlarda) Long turida saqlang va ekranga chiqaring.",
        """fun main() {
    val worldPopulation: Long = 8_100_000_000L
    val lightYearMeters: Long = 9_460_730_472_580_800L
    
    println("Dunyo aholisi: $worldPopulation kishi")
    println("1 yorug'lik yili: $lightYearMeters metr")
}""",
        "32-bitli Int maksimal ~2.14 milliardgacha qiymat saqlay oladi. Undan katta qiymatlar uchun 64-bitli Long kerak. Kotlinda Long literallar oxiriga 'L' qo'shiladi. Shuningdek, o'qishni osonlashtirish uchun raqamlar orasiga pastki chiziq '_' qo'yish mumkin.",
        """Dunyo aholisi: 8100000000 kishi
1 yorug'lik yili: 9460730472580800 metr"""
    ),
    (
        6,
        "Suzuvchi nuqtali sonlar: Float vs Double aniqligi",
        "Doiraning yuzi va radiusini hisoblashda Float (32-bit) va Double (64-bit) aniqlik farqlarini solishtiring.",
        """fun main() {
    val piFloat: Float = 3.141592653589793f
    val piDouble: Double = 3.141592653589793
    
    println("Float aniqligi : $piFloat")
    println("Double aniqligi: $piDouble")
    
    val radius = 5.0
    val areaFloat = (piFloat * radius * radius).toFloat()
    val areaDouble = piDouble * radius * radius
    
    println("Yuza (Float): $areaFloat")
    println("Yuza (Double): $areaDouble")
}""",
        "Float 32-bit bo'lib, taxminan 6-7 ta o'nlik raqam aniqligini beradi va uning qiymati 'f' yoki 'F' bilan tugashi shart. Double esa 64-bit bo'lib, 15-16 ta raqam aniqligini kafolatlaydi. Kotlinda sukut bo'yicha barcha suzuvchi nuqtali sonlar Double hisoblanadi.",
        """Float aniqligi : 3.1415927
Double aniqligi: 3.141592653589793
Yuza (Float): 78.53982
Yuza (Double): 78.53981633974483"""
    ),
    (
        7,
        "Belgilar bilan ishlash: Char turi va amallar",
        "Belgining harf, raqam yoki maxsus belgi ekanligini aniqlovchi va uning Unicode kodini ko'rsatuvchi dastur yozing.",
        """fun main() {
    val ch1: Char = 'A'
    val ch2: Char = '7'
    val ch3: Char = '\u2764' // Yurak belgisi
    
    println("Belgi 1: $ch1, Harfmi: ${ch1.isLetter()}, Kodi: ${ch1.code}")
    println("Belgi 2: $ch2, Raqammi: ${ch2.isDigit()}, Kodi: ${ch2.code}")
    println("Belgi 3: $ch3, Unicode kodi: ${ch3.code}")
}""",
        "Kotlinda Char bitta 16-bitli Unicode belgisini ifodalaydi va yakka tirnoq ' ' ichiga olinadi. Java dan farqli o'laroq, Char turini to'g'ridan-to'g'ri butun son sifatida ishlatib bo'lmaydi; uning kodini olish uchun '.code' xususiyatidan foydalaniladi.",
        """Belgi 1: A, Harfmi: true, Kodi: 65
Belgi 2: 7, Raqammi: true, Kodi: 55
Belgi 3: ❤, Unicode kodi: 10084"""
    ),
    (
        8,
        "Mantiqiy amallar va qisqa tutashuv (Short-circuit evaluation)",
        "Foydalanuvchining tizimga kirish huquqini tekshiruvchi mantiqiy ifoda tuzing. Unda '&&' va '||' operatorlarining ishlash mexanizmini ko'rsating.",
        """fun checkAccess(isAdmin: Boolean, isRegistered: Boolean, hasActiveToken: Boolean): Boolean {
    // Agar isAdmin true bo'lsa, qolgan shartlar tekshirilmasdan darhol true qaytadi
    return isAdmin || (isRegistered && hasActiveToken)
}

fun main() {
    val access1 = checkAccess(isAdmin = true, isRegistered = false, hasActiveToken = false)
    val access2 = checkAccess(isAdmin = false, isRegistered = true, hasActiveToken = true)
    val access3 = checkAccess(isAdmin = false, isRegistered = true, hasActiveToken = false)
    
    println("Admin huquqi: $access1")
    println("Oddiy faol foydalanuvchi: $access2")
    println("Muddati tugagan foydalanuvchi: $access3")
}""",
        "Kotlinda mantiqiy '&&' (va) hamda '||' (yoki) operatorlari qisqa tutashuv (short-circuit) tamoyili asosida ishlaydi. '||' operatorida birinchi operand true bo'lsa, ikkinchisi hisoblanmaydi. '&&' da esa birinchi operand false bo'lsa, qolgani tashlab ketiladi.",
        """Admin huquqi: true
Oddiy faol foydalanuvchi: true
Muddati tugagan foydalanuvchi: false"""
    ),
    (
        9,
        "String shablonlari (String Templates) va hisoblashlar",
        "Matn ichida o'zgaruvchilarni va arifmetik amallarni $ va ${} orqali integratsiya qilish dasturini tuzing.",
        """fun main() {
    val mahsulot = "Noutbuk"
    val narx = 1200
    val soliqFoizi = 12
    
    println("Mahsulot: $mahsulot")
    println("Narxi: $narx AQSH dollari")
    println("Soliq bilan jami: ${narx + (narx * soliqFoizi / 100)} AQSH dollari")
    println("Belgi narxi: \$$narx (valyuta belgisi chiqishi uchun)")
}""",
        "Kotlinda satr ichiga o'zgaruvchi qiymatini kiritish uchun '$o_zgaruvchi' sintaksisi ishlatiladi. Agar ifoda yoki arifmetik amal bajarish kerak bo'lsa, '${ifoda}' shaklida qavslar qo'llaniladi. Dollar belgisining o'zini chiqarish uchun esa '\\$' yoki \"${'$'}\" yoziladi.",
        """Mahsulot: Noutbuk
Narxi: 1200 AQSH dollari
Soliq bilan jami: 1344 AQSH dollari
Belgi narxi: $1200 (valyuta belgisi chiqishi uchun)"""
    ),
    (
        10,
        "Ko'p qatorli matnlar (Raw Strings) va trimIndent()",
        "Ko'p qatorli JSON ma'lumotini raw string (\"\"\") yordamida formatlab, keraksiz bo'shliqlarni 'trimIndent()' bilan olib tashlang.",
        """fun main() {
    val jsonResponse = \"\"\"
        {
            "status": "success",
            "code": 200,
            "data": {
                "server": "Toshkent-01",
                "uptime": "99.9%"
            }
        }
    \"\"\".trimIndent()
    
    println(jsonResponse)
}""",
        "Kotlinda uchlik qo'shtirnoq '\"\"\"' bilan o'ralgan matnlar escape belgilarini talab qilmaydi va asl formatini saqlaydi. 'trimIndent()' funksiyasi barcha qatorlar uchun umumiy bo'lgan chap bo'shliqlarni olib tashlaydi, bu esa kodni chiroyli va o'qishli saqlashga imkon beradi.",
        """{
    "status": "success",
    "code": 200,
    "data": {
        "server": "Toshkent-01",
        "uptime": "99.9%"
    }
}"""
    ),
    (
        11,
        "Chegara bo'shliqlarini boshqarish: trimMargin()",
        "Ko'p qatorli SQL so'rovini maxsus belgi (masalan, '|') yordamida tekislab, 'trimMargin()' orqali formatlang.",
        """fun main() {
    val tableName = "mijozlar"
    val query = \"\"\"
        |SELECT id, ism, balans
        |FROM $tableName
        |WHERE balans > 0
        |ORDER BY balans DESC;
    \"\"\".trimMargin("|")
    
    println(query)
}""",
        "'trimMargin()' funksiyasi har bir qatorda ko'rsatilgan belgigacha (standart bo'yicha '|') bo'lgan barcha bo'shliqlarni olib tashlaydi. Bu ko'p qatorli matnlarni koddagi indentatsiya chuqurligidan qat'i nazar chetga tekislashda qulay vositadir.",
        """SELECT id, ism, balans
FROM mijozlar
WHERE balans > 0
ORDER BY balans DESC;"""
    ),
    (
        12,
        "Aniq sonli konvertatsiya (Explicit Type Conversion)",
        "Kotlinda Java kabi avtomatik tip kengayishi (implicit widening) mavjud emasligini namoyish qiling va toInt(), toLong(), toDouble() metodlaridan foydalaning.",
        """fun main() {
    val intValue: Int = 42
    // val longValue: Long = intValue // Kompilyatsiya xatosi: Type mismatch
    val longValue: Long = intValue.toLong()
    val doubleValue: Double = intValue.toDouble()
    val byteValue: Byte = intValue.toByte()
    
    println("Int qiymat: $intValue")
    println("Long qiymat: $longValue")
    println("Double qiymat: $doubleValue")
    println("Byte qiymat: $byteValue")
}""",
        "Kotlin tip xavfsizligiga qat'iy rioya qiladi. Kichik turdagi sonlar (masalan, Int) katta turdagi o'zgaruvchilarga (masalan, Long yoki Double) avtomatik o'tmaydi. Har bir konvertatsiya dasturchi tomonidan aniq 'toXxx()' metodlari orqali chaqirilishi shart, bu yashirin noaniqliklarning oldini oladi.",
        """Int qiymat: 42
Long qiymat: 42
Double qiymat: 42.0
Byte qiymat: 42"""
    ),
    (
        13,
        "Matndan songa o'tkazish va xavfsiz konvertatsiya: toIntOrNull()",
        "Foydalanuvchi kiritgan matnli yoshni xavfsiz tarzda Int turiga o'tkazing va xato kiritilganda dastur qulashini oldini oling.",
        """fun parseUserAge(input: String): Int {
    val age = input.toIntOrNull()
    return age ?: 0 // Agar null bo'lsa, 0 qaytaradi
}

fun main() {
    val inputValid = "28"
    val inputInvalid = "yigirma sakkiz"
    
    println("To'g'ri kiritish: ${parseUserAge(inputValid)}")
    println("Noto'g'ri kiritish: ${parseUserAge(inputInvalid)}")
}""",
        "'toInt()' metodi son bo'lmagan matnda 'NumberFormatException' tashlaydi. 'toIntOrNull()' esa xato bo'lsa dasturni to'xtatmay, 'null' qaytaradi. Elvis operatori '?:' bilan birgalikda bu juda qulay va xavfsiz konvertatsiya andozasidir.",
        """To'g'ri kiritish: 28
Noto'g'ri kiritish: 0"""
    ),
    (
        14,
        "Belgini uning raqam qiymatiga o'tkazish: digitToInt()",
        "Char turidagi raqam belgisini ('0'..'9') haqiqiy arifmetik Int songa aylantiruvchi zamonaviy Kotlinga xos metodni qo'llang.",
        """fun main() {
    val charDigit: Char = '9'
    
    // Eski/noto'g'ri usul: charDigit.code - bu 57 (ASCII kod) beradi
    val asciiCode = charDigit.code
    
    // Kotlin 1.5+ zamonaviy usul:
    val realNumber = charDigit.digitToInt()
    
    println("Belgi: '$charDigit'")
    println("ASCII kodi: $asciiCode")
    println("Haqiqiy raqam qiymati: $realNumber")
    println("Hisoblash: $realNumber * 5 = ${realNumber * 5}")
}""",
        "Kotlinda belgining ASCII/Unicode kodini olish (char.code) va uning son qiymatini olish (char.digitToInt()) qat'iy farqlanadi. 'digitToInt()' agar belgi haqiqatan ham '0'..'9' oralig'ida bo'lsa uning haqiqiy raqam qiymatini qaytaradi, aks holda 'IllegalArgumentException' beradi.",
        """Belgi: '9'
ASCII kodi: 57
Haqiqiy raqam qiymati: 9
Hisoblash: 9 * 5 = 45"""
    ),
    (
        15,
        "O'n oltilik (Hexadecimal) va ikkilik (Binary) literallar",
        "Turli sanoq tizimlaridagi sonlarni (ikkilik '0b', o'n oltilik '0x') e'lon qiling va ularni o'nlik tizimda chop eting.",
        """fun main() {
    val hexValue = 0x1A // 16-lik tizimda 1A = 26
    val binaryValue = 0b10110 // 2-lik tizimda 10110 = 22
    val mask = 0xFF_00 // 65280
    
    println("Hex 0x1A: $hexValue")
    println("Binary 0b10110: $binaryValue")
    println("Mask 0xFF00: $mask")
    println("Hex formatda qayta chiqarish: ${hexValue.toString(16).uppercase()}")
}""",
        "Kotlinda o'n oltilik sonlar '0x' prefiksi bilan, ikkilik sonlar esa '0b' prefiksi bilan yoziladi. Kotlinda sakkizlik (octal) literallar qo'llab-quvvatlanmaydi. '.toString(radix)' funksiyasi orqali sonni istalgan sanoq sistemasida satrga aylantirish mumkin.",
        """Hex 0x1A: 26
Binary 0b10110: 22
Mask 0xFF00: 65280
Hex formatda qayta chiqarish: 1A"""
    ),
    (
        16,
        "Bit darajasidagi amallar (Bitwise operations)",
        "Kotlinda 'shl', 'shr', 'and', 'or', 'xor', 'inv' infix funksiyalaridan foydalanib bitlar ustida amallar bajaring.",
        """fun main() {
    val a = 0b0011 // 3
    val b = 0b0101 // 5
    
    println("a AND b: ${a and b}") // 0b0001 = 1
    println("a OR b : ${a or b}")  // 0b0111 = 7
    println("a XOR b: ${a xor b}") // 0b0110 = 6
    println("a SHL 1: ${a shl 1}") // 0b0110 = 6
    println("b SHR 1: ${b shr 1}") // 0b0010 = 2
    println("a INV  : ${a.inv()}") // bitwise inverting
}""",
        "Java dagi bitwise operatorlar (&, |, ^, <<, >>) o'rniga Kotlinda o'qishga qulay infix funksiyalar ishlatiladi: 'and', 'or', 'xor', 'shl' (chapga surish), 'shr' (o'ngga surish), 'ushr' (ishorasiz o'ngga surish) va 'inv()' (inkor).",
        """a AND b: 1
a OR b : 7
a XOR b: 6
a SHL 1: 6
b SHR 1: 2
a INV  : -4"""
    ),
    (
        17,
        "Ishorasiz butun sonlar (Unsigned Integers): UByte, UInt, ULong",
        "Faqat musbat sonlarni saqlovchi va xotirani to'liq musbat diapazon uchun ishlatuvchi UInt va UByte turlarini sinab ko'ring.",
        """fun main() {
    val unsignedByte: UByte = 250u
    val unsignedInt: UInt = 4_000_000_000u
    val unsignedLong: ULong = 18_000_000_000_000_000_000uL
    
    println("UByte qiymat: $unsignedByte (Maksimal: ${UByte.MAX_VALUE})")
    println("UInt qiymat: $unsignedInt (Maksimal: ${UInt.MAX_VALUE})")
    println("ULong qiymat: $unsignedLong (Maksimal: ${ULong.MAX_VALUE})")
}""",
        "Kotlin 'inline value classes' asosida qurilgan 'Unsigned' (ishorasiz) son turlarini taqdim etadi: UByte (0..255), UShort (0..65535), UInt (0..4.29 mlrd) va ULong. Ularni ifodalash uchun son oxiriga 'u' yoki 'uL' suffiksi qo'yiladi.",
        """UByte qiymat: 250 (Maksimal: 255)
UInt qiymat: 4000000000 (Maksimal: 4294967295)
ULong qiymat: 18000000000000000000 (Maksimal: 18446744073709551615)"""
    ),
    (
        18,
        "Konstanta qiymatlar: 'const val' va kompilyatsiya vaqtidagi konstantalar",
        "Kompilyatsiya vaqtida (compile-time) hisoblanuvchi 'const val' o'zgaruvchilarini e'lon qiling va uning oddiy 'val' dan farqini tushuntiring.",
        """const val APP_VERSION = "2.4.0"
const val MAX_RETRY_COUNT = 3

fun main() {
    val runtimeDate = java.time.LocalDate.now().toString()
    
    println("Ilova versiyasi: $APP_VERSION")
    println("Urinishlar limiti: $MAX_RETRY_COUNT")
    println("Ishga tushgan sana: $runtimeDate")
}""",
        "'const val' faqat kompilyatsiya vaqtida ma'lum bo'ladigan primitiv tiplar yoki String uchun qo'llaniladi va faylning yuqori darajasida (top-level) yoki 'object' ichida e'lon qilinadi. U bayt-kodda to'g'ridan-to'g'ri almashtiriladi (inlining), oddiy 'val' esa ish vaqtida (runtime) ham hisoblanishi mumkin.",
        """Ilova versiyasi: 2.4.0
Urinishlar limiti: 3
Ishga tushgan sana: 2026-11-08"""
    ),
    (
        19,
        "Any turi: Kotlindagi eng yuqori umumiy tip",
        "Har qanday ma'lumot turini qabul qila oladigan 'Any' turidagi o'zgaruvchini yarating va uning standart metodlarini tekshiring.",
        """fun printObjectInfo(obj: Any) {
    println("Obyekt: $obj | Klass: ${obj::class.simpleName} | HashCode: ${obj.hashCode()}")
}

fun main() {
    printObjectInfo(100)
    printObjectInfo("Salom Dunyo")
    printObjectInfo(true)
    printObjectInfo(3.14)
}""",
        "Kotlinda 'Any' barcha null bo'lmagan (non-nullable) tiplarning ota sinfidir (Java dagi 'Object' ga o'xshash). Har bir Kotlin klassi Any dan meros oladi va unda 3 ta asosiy metod mavjud: 'equals()', 'hashCode()' va 'toString()'.",
        """Obyekt: 100 | Klass: Int | HashCode: 100
Obyekt: Salom Dunyo | Klass: String | HashCode: 2068999330
Obyekt: true | Klass: Boolean | HashCode: 1231
Obyekt: 3.14 | Klass: Double | HashCode: 219930624"""
    ),
    (
        20,
        "Unit turi: Qiymat qaytarmaydigan funksiyalar",
        "Hech qanday ma'noli qiymat qaytarmaydigan funksiyalarda 'Unit' turining vazifasini ko'rsating.",
        """fun logMessage(message: String): Unit {
    println("[LOG]: $message")
    // return Unit yozish shart emas, avtomatik qaytadi
}

fun main() {
    val result: Unit = logMessage("Tizim muvaffaqiyatli yuklandi.")
    println("Qaytgan qiymat turi: ${result::class.simpleName}")
}""",
        "Java dagi 'void' dan farqli o'laroq, Kotlin da 'Unit' haqiqiy singleton obyekt hisoblanadi. Agar funksiya qiymat qaytarmasa, u sukut bo'yicha 'Unit' turini qaytaradi. Bu generiklar va funksional dasturlashda bir xillikni (consistency) ta'minlaydi.",
        """[LOG]: Tizim muvaffaqiyatli yuklandi.
Qaytgan qiymat turi: Unit"""
    ),
    (
        21,
        "Nothing turi: Hech qachon tugamaydigan yoki istisno tashlovchi ifodalar",
        "Funksiya xatolik tashlaganda yoki cheksiz sikl bo'lganda 'Nothing' turining qanday ishlatilishini ko'rsating.",
        """fun failWithError(message: String): Nothing {
    throw IllegalStateException("Kritik xatolik: $message")
}

fun main() {
    val isDatabaseConnected = false
    
    try {
        if (!isDatabaseConnected) {
            failWithError("Baza bilan aloqa yo'q!")
        }
    } catch (e: Exception) {
        println("Ushlangan istisno: ${e.message}")
    }
}""",
        "'Nothing' Kotlindagi barcha tiplarning quyi (bottom) tipidir va uning hech qanday nusxasi bo'lishi mumkin emas. U funksiya hech qachon normal yakunlanmasligini (istisno tashlaydi yoki cheksiz to'xtaydi) kompilyatorga bildirish uchun xizmat qiladi.",
        """Ushlangan istisno: Kritik xatolik: Baza bilan aloqa yo'q!"""
    ),
    (
        22,
        "Primitiv tiplar va obyekt o'rash (Autoboxing) tushunchasi",
        "Kotlinda barcha tiplar obyekt sifatida ko'rinsa-da, bayt-kod darajasida qachon Java primitiviga (int), qachon o'ralgan obyektga (Integer) aylanishini solishtiring.",
        """fun main() {
    val primitiveInt: Int = 10 // Bayt-kodda int bo'ladi
    val nullableInt: Int? = 10 // Bayt-kodda java.lang.Integer ga aylanadi
    
    println("primitiveInt: $primitiveInt")
    println("nullableInt: $nullableInt")
    println("Tenglik tekshiruvi: ${primitiveInt == nullableInt}")
}""",
        "Kotlinda kod yozayotganda barcha tiplar obyektga o'xshaydi. Ammo Kotlin kompilyatori (K2) optimallashtirish o'tkazadi: agar o'zgaruvchi null bo'lmasa (Int), u JVM da tez ishlaydigan oddiy primitiv 'int' ga kompilyatsiya bo'ladi. Agar o'zgaruvchi nullable (Int?) bo'lsa yoki generiklarda ishlatilsa, obyekt o'rami (Integer) hosil bo'ladi.",
        """primitiveInt: 10
nullableInt: 10
Tenglik tekshiruvi: true"""
    ),
    (
        23,
        "Math kutubxonasi yordamida matematik amallar",
        "Kotlinda 'kotlin.math' kutubxonasidagi maxsus funksiyalar (sqrt, pow, round, ceil, floor) yordamida murakkab hisob-kitob bajaring.",
        """import kotlin.math.*

fun main() {
    val number = 25.0
    val power = 3.0
    val piVal = PI
    
    println("Kvadrat ildiz: ${sqrt(number)}")
    println("Darajaga ko'tarish: ${number.pow(power)}")
    println("Shiftga yaxlitlash (ceil): ${ceil(4.1)}")
    println("Polga yaxlitlash (floor): ${floor(4.9)}")
    println("Eng yaqiniga yaxlitlash (round): ${round(4.6)}")
    println("Sinus(pi / 2): ${sin(piVal / 2)}")
}""",
        "'kotlin.math' to'plami Kotlin platformasiga xos bo'lib, Java ning 'Math' kutubxonasini to'liq almashtiradi va Kotlin Multiplatform (KMP) doirasida Android, iOS va Web platformalarida bir xil ishlaydi.",
        """Kvadrat ildiz: 5.0
Darajaga ko'tarish: 15625.0
Shiftga yaxlitlash (ceil): 5.0
Polga yaxlitlash (floor): 4.0
Eng yaqiniga yaxlitlash (round): 5.0
Sinus(pi / 2): 1.0"""
    ),
    (
        24,
        "String qidirish va tahlil qilish metodlari",
        "Elektron pochta manzilini tahlil qilib, foydalanuvchi nomi va domen qismini ajratib oling.",
        """fun main() {
    val email = "dilshod.rahimov@example.uz"
    
    val atIndex = email.indexOf('@')
    val username = email.substring(0, atIndex)
    val domain = email.substring(atIndex + 1)
    val isUzDomain = email.endsWith(".uz")
    
    println("To'liq email: $email")
    println("Foydalanuvchi nomi: $username")
    println("Domen: $domain")
    println(".uz zonasidami: $isUzDomain")
}""",
        "Kotlinda String boy standart metodlar to'plamiga ega: 'indexOf', 'substring', 'startsWith', 'endsWith', 'contains' va boshqalar. Bu metodlar matnlarni xavfsiz va samarali tahlil qilish imkonini beradi.",
        """To'liq email: dilshod.rahimov@example.uz
Foydalanuvchi nomi: dilshod.rahimov
Domen: example.uz
.uz zonasidami: true"""
    ),
    (
        25,
        "Satrlarni almashtirish va tozalash: replace() va split()",
        "Vergullar bilan ajratilgan mahsulotlar ro'yxatini tozalab, massivga ajrating va formatlang.",
        """fun main() {
    val rawInput = "  olma,  nok , uzum, shaftoli , anor  "
    val cleaned = rawInput.trim()
    val fruits = cleaned.split(",").map { it.trim().replaceFirstChar { char -> char.uppercase() } }
    
    println("Tozalangan va formatlangan ro'yxat:")
    fruits.forEachIndexed { index, fruit ->
        println("${index + 1}. $fruit")
    }
}""",
        "'split()' satrni berilgan ajratuvchi bo'yicha bo'laklaydi. 'trim()' boshidagi va oxiridagi bo'shliqlarni olib tashlaydi. 'replaceFirstChar()' esa Kotlinda belgining faqat birinchi harfini katta qilishning tavsiya etilgan zamonaviy usulidir.",
        """Tozalangan va formatlangan ro'yxat:
1. Olma
2. Nok
3. Uzum
4. Shaftoli
5. Anor"""
    ),
    (
        26,
        "Formatlangan satrlar: String.format()",
        "Valyuta summasi va sanani aniq 2 ta o'nlik xonali va ustunli qilib 'String.format()' yordamida ekranga chiqaring.",
        """fun main() {
    val clientName = "Anvar Karimov"
    val balance = 1254300.5678
    val discount = 7.5
    
    val formatted = String.format("Mijoz: %-15s | Balans: %,.2f so'm | Chegirma: %5.1f%%", clientName, balance, discount)
    println(formatted)
}""",
        "'String.format()' Java dagi formatlash mexanizmidan foydalanadi: '%,.2f' sonlarni mingliklarga ajratib (vergul bilan) va 2 ta o'nlik raqam bilan chiqaradi, '%-15s' chap tomondan tekislangan 15 ta belgili satr hosil qiladi.",
        """Mijoz: Anvar Karimov   | Balans: 1,254,300.57 so'm | Chegirma:   7.5%"""
    ),
    (
        27,
        "Belgilar ketma-ketligini solishtirish: equals vs ==",
        "Kotlinda strukturaviy tenglik (==) va referensial tenglik (===) farqini namoyish qiling.",
        """fun main() {
    val str1 = "Kotlin"
    val str2 = "Kot" + "lin"
    val str3 = String(charArrayOf('K', 'o', 't', 'l', 'i', 'n'))
    
    println("str1 == str2: ${str1 == str2}")       // Strukturaviy qiymat tengligi (equals)
    println("str1 === str2: ${str1 === str2}")     // Xotiradagi bir xil havola (String pool)
    println("str1 == str3: ${str1 == str3}")       // Qiymati teng
    println("str1 === str3: ${str1 === str3}")     // Xotirada turli xil obyektlar
}""",
        "Kotlinda '==' operatori avtomatik ravishda '.equals()' metodini chaqiradi va null-safe ishlaydi. '===' operatori esa xotiradagi manzillarni (referensiyalarni) solishtiradi. Java dan farqli o'laroq, satrlarni qiymat bo'yicha solishtirish uchun '==' qo'llanilishi eng to'g'ri yo'ldir.",
        """str1 == str2: true
str1 === str2: true
str1 == str3: true
str1 === str3: false"""
    ),
    (
        28,
        "Mantiqiy shartlar zanjiri va ustuvorlik (Operator Precedence)",
        "Murakkab mantiqiy ifodaning hisoblanish tartibini qavslar va operatorlar ustuvorligi orqali tekshiring.",
        """fun main() {
    val hasTicket = true
    val hasVipPass = false
    val isBanned = false
    val isSecurityPassed = true
    
    // && operatori || ga qaraganda yuqori ustuvorlikka ega
    val canEnterWithoutParentheses = hasVipPass || hasTicket && !isBanned && isSecurityPassed
    val canEnterExplicit = hasVipPass || (hasTicket && (!isBanned) && isSecurityPassed)
    
    println("Kirish mumkinmi (odatiy): $canEnterWithoutParentheses")
    println("Kirish mumkinmi (aniq qavsli): $canEnterExplicit")
}""",
        "Mantiqiy amallarda '!' (inkor) eng yuqori, keyin '&&' (va), va eng past ustuvorlikka '||' (yoki) ega. Tushunmovchiliklarni oldini olish va kod tozaligi uchun murakkab ifodalarni har doim qavslar bilan ajratish tavsiya etiladi.",
        """Kirish mumkinmi (odatiy): true
Kirish mumkinmi (aniq qavsli): true"""
    ),
    (
        29,
        "O'zgaruvchilar doirasi (Variable Scope) va soyalash (Shadowing)",
        "Ichki blokda tashqi blokdagi o'zgaruvchi nomini qayta ishlatish (shadowing) holatini namoyish qiling.",
        """fun main() {
    val x = 100
    println("Asosiy doiradagi x: $x")
    
    run {
        val x = 200 // Tashqi x ni soyalaydi (shadows)
        println("Ichki blokdagi x: $x")
    }
    
    println("Yana asosiy x: $x")
}""",
        "Kotlinda ichki bloklarda (masalan, if, for yoki lambda ichida) tashqi o'zgaruvchi bilan bir xil nomli yangi o'zgaruvchi e'lon qilinishi 'variable shadowing' deyiladi. Bu xato emas, lekin kodni chalkashtirmaslik uchun undan ehtiyotkorlik bilan foydalanish lozim.",
        """Asosiy doiradagi x: 100
Ichki blokdagi x: 200
Yana asosiy x: 100"""
    ),
    (
        30,
        "Arifmetik qisqartirilgan amallar (Compound Assignment Operators)",
        "+=, -=, *=, /= va %= operatorlarining xatti-harakatini tekshiring.",
        """fun main() {
    var score = 50
    score += 25 // score = score + 25
    println("Qo'shishdan so'ng: $score")
    
    score -= 15 // score = score - 15
    println("Ayirishdan so'ng: $score")
    
    score *= 2  // score = score * 2
    println("Ko'paytirishdan so'ng: $score")
    
    score /= 4  // butun sonli bo'lish
    println("Bo'lishdan so'ng: $score")
    
    score %= 7  // qoldiq
    println("Qoldiqdan so'ng: $score")
}""",
        "Murakkab biriktirish operatorlari amaliyotda kodni qisqartiradi va barcha arifmetik amallar uchun ishlaydi. Butun sonlarni bo'lishda natija doimo pastga qarab butun qismgacha kesiladi.",
        """Qo'shishdan so'ng: 75
Ayirishdan so'ng: 60
Ko'paytirishdan so'ng: 120
Bo'lishdan so'ng: 30
Qoldiqdan so'ng: 2"""
    ),
    (
        31,
        "Prefix va Postfix inkrement/dekrement farqlari",
        "++var va var++ amallarining amaldagi hisoblash ketma-ketligini solishtiring.",
        """fun main() {
    var a = 5
    var b = 5
    
    val prefixResult = ++a // Avval qiymat oshadi, keyin biriktiriladi
    val postfixResult = b++ // Avval eski qiymat biriktiriladi, keyin o'zgaruvchi oshadi
    
    println("Prefix natija: $prefixResult, a ning yakuniy qiymati: $a")
    println("Postfix natija: $postfixResult, b ning yakuniy qiymati: $b")
}""",
        "Prefix inkrement (++a) o'zgaruvchini avval 1 taga oshirib so'ngra yangi qiymatni ifodaga uzatadi. Postfix inkrement (b++) esa avval mavjud eski qiymatni ifodaga qaytarib, shundan keyingina o'zgaruvchini oshiradi.",
        """Prefix natija: 6, a ning yakuniy qiymati: 6
Postfix natija: 5, b ning yakuniy qiymati: 6"""
    ),
    (
        32,
        "Taqqoslash operatorlari (Comparison Operators)",
        ">, <, >=, <= operatorlarining turli ma'lumot turlari (sonlar va satrlar) bilan ishlashini tekshiring.",
        """fun main() {
    val speedLimit = 60
    val currentSpeed = 75
    val isOverSpeed = currentSpeed > speedLimit
    
    val word1 = "Olma"
    val word2 = "Banan"
    val isAlphabetical = word1 < word2 // Leksikografik taqqoslash
    
    println("Tezlik oshdimi: $isOverSpeed")
    println("'$word1' '$word2' dan oldin keladimi: $isAlphabetical")
}""",
        "Kotlinda taqqoslash operatorlari nafaqat sonlar uchun, balki 'Comparable' interfeysini implementatsiya qilgan har qanday obyekt (jumladan String) uchun ham ishlaydi. Satrlar leksikografik (alfabit bo'yicha) taqqoslanadi.",
        """Tezlik oshdimi: true
'Olma' 'Banan' dan oldin keladimi: false"""
    ),
    (
        33,
        "Ko'p satrli String ichida dollar belgisini chiqarish",
        "Moliyaviy shablonda valyuta belgisi ($) va o'zgaruvchilarni to'g'ri kombinatsiya qiling.",
        """fun main() {
    val price = 49.99
    val plan = "Premium"
    
    val message = \"\"\"
        Tarif: $plan
        Oylik to'lov: ${'$'}$price
        Yillik to'lov: ${'$'}${price * 12}
    \"\"\".trimIndent()
    
    println(message)
}""",
        "Kotlinda string template ichida dollar belgisini to'g'ridan-to'g'ri chop etish uchun '${'$'}' ifodasi eng ishonchli va xatosiz usul hisoblanadi. Bu ayniqsa raw string (\"\"\") ichida qulaydir.",
        """Tarif: Premium
Oylik to'lov: $49.99
Yillik to'lov: $599.88"""
    ),
    (
        34,
        "Sonlarning chegaraviy qiymatlari (Overflow va Underflow)",
        "Int tipining maksimal qiymatiga 1 qo'shilganda nima yuz berishini tekshiring.",
        """fun main() {
    var maxInt = Int.MAX_VALUE
    println("Int MAX: $maxInt")
    
    maxInt += 1 // Overflow (to'lib toshish)
    println("MAX + 1: $maxInt")
    
    var minInt = Int.MIN_VALUE
    minInt -= 1 // Underflow
    println("MIN - 1: $minInt")
}""",
        "Standart arifmetikada butun son chegaradan oshib ketganda xatolik (exception) tashlanmaydi, balki ikkilik sanoq doirasida aylanib (wrap-around) manfiy qutbga o'tib ketadi. Katta moliyaviy hisoblarda bu jiddiy xato keltirib chiqarishi mumkin, shuning uchun Long yoki BigInteger ishlatiladi.",
        """Int MAX: 2147483647
MAX + 1: -2147483648
MIN - 1: 2147483647"""
    ),
    (
        35,
        "Katta aniqlikdagi hisob-kitoblar: BigDecimal",
        "Moliyaviy valyuta hisob-kitoblarida suzuvchi nuqta noaniqligini yo'qotish uchun BigDecimal dan foydalaning.",
        """import java.math.BigDecimal

fun main() {
    val doubleSum = 0.1 + 0.2
    println("Double bilan: $doubleSum") // 0.30000000000000004
    
    val bigDecimal1 = BigDecimal("0.1")
    val bigDecimal2 = BigDecimal("0.2")
    val preciseSum = bigDecimal1 + bigDecimal2
    
    println("BigDecimal bilan: $preciseSum") // 0.3
}""",
        "Double va Float sonlar IEEE 754 ikkilik suzuvchi nuqta formati sababli ba'zi o'nlik kasrlarni noaniq saqlaydi. Bank va savdo tizimlarida mutlaq aniqlik uchun 'BigDecimal' qo'llaniladi. Kotlinda BigDecimal uchun '+' va '*' operatorlari haddan tashqari yuklangan (overloaded).",
        """Double bilan: 0.30000000000000004
BigDecimal bilan: 0.3"""
    ),
    (
        36,
        "Tipni aniqlash: 'is' operatori va Type Checking",
        "Berilgan noma'lum o'zgaruvchi qaysi ma'lumot turiga tegishli ekanligini 'is' operatori orqali aniqlang.",
        """fun identifyType(item: Any): String {
    return when (item) {
        is String -> "Matn turi, uzunligi: ${item.length}"
        is Int -> "Butun son: $item, kvadrati: ${item * item}"
        is Boolean -> "Mantiqiy qiymat: $item"
        is Double -> "Kasr son: $item"
        else -> "Noma'lum tur"
    }
}

fun main() {
    println(identifyType("Salom"))
    println(identifyType(8))
    println(identifyType(true))
    println(identifyType(15.75))
}""",
        "'is' operatori o'zgaruvchining ma'lum bir sinf yoki interfeysga tegishli ekanligini tekshiradi (Java dagi 'instanceof'). Kotlinda bu tekshiruvdan so'ng kompilyator o'zgaruvchini avtomatik ravishda o'sha turga o'tkazadi (Smart Cast).",
        """Matn turi, uzunligi: 5
Butun son: 8, kvadrati: 64
Mantiqiy qiymat: true
Kasr son: 15.75"""
    ),
    (
        37,
        "Xavfsiz va xavfli tip konvertatsiyasi: 'as' vs 'as?'",
        "Obyektni boshqa turga o'tkazishda 'ClassCastException' oldini olish uchun xavfsiz 'as?' operatorini qo'llang.",
        """fun main() {
    val obj: Any = "Kotlin tili"
    
    // Xavfsiz cast:
    val str: String? = obj as? String
    val number: Int? = obj as? Int // Natija null bo'ladi, xato tashlamaydi
    
    println("Matnga aylantirish: $str")
    println("Songa aylantirish: $number")
}""",
        "'as' operatori xavfli hisoblanadi: agar obyekt ko'rsatilgan turga mos kelmasa, 'ClassCastException' yuz beradi. 'as?' esa xavfsiz (safe cast) bo'lib, muvaffaqiyatsiz bo'lsa xato tashlamasdan 'null' qaytaradi.",
        """Matnga aylantirish: Kotlin tili
Songa aylantirish: null"""
    ),
    (
        38,
        "Massivlar bilan dastlabki tanishuv: arrayOf va IntArray",
        "Kotlinda umumiy massiv (Array<T>) va primitiv massiv (IntArray) yaratib, ularning elementlarini chop eting.",
        """fun main() {
    val names: Array<String> = arrayOf("Ali", "Vali", "G'ani")
    val numbers: IntArray = intArrayOf(10, 20, 30, 40)
    
    println("Ismlar soni: ${names.size}")
    println("Birinchi ism: ${names[0]}")
    println("Sonlar yig'indisi: ${numbers.sum()}")
}""",
        "Kotlinda 'Array<T>' Java dagi 'T[]' ga to'g'ri keladi va obyektlar massividir. 'IntArray', 'ByteArray', 'DoubleArray' kabi maxsus turlar esa Java primitiv massivlariga (int[], byte[]) kompilyatsiya bo'ladi va ortiqcha obyekt yaratmasdan xotirani tejaydi.",
        """Ismlar soni: 3
Birinchi ism: Ali
Sonlar yig'indisi: 100"""
    ),
    (
        39,
        "O'zgarmas qiymatlarni birlashtirish va yangi satr yaratish",
        "Bir nechta o'zgaruvchilarni qo'shib, to'liq profil kartasini hosil qiling.",
        """fun main() {
    val firstName = "Ziyoda"
    val lastName = "Toshmatova"
    val age = 22
    val job = "Android Dasturchi"
    
    val profileCard = "Xodim: $firstName $lastName | Yoshi: $age | Kasbi: $job"
    println(profileCard)
}""",
        "Kotlinda satrlarni birlashtirishda '+' operatoridan ko'ra satr shablonlari ($) afzalroq. Bu kodni ixchamlashtiradi va ichki 'StringBuilder' orqali yuqori unumdorlik bilan ishlaydi.",
        """Xodim: Ziyoda Toshmatova | Yoshi: 22 | Kasbi: Android Dasturchi"""
    ),
    (
        40,
        "Sana va vaqt bilan ishlash (Java Time API interop)",
        "Kotlinda zamonaviy Java 'java.time' kutubxonasidan foydalanib joriy vaqtni formatlang.",
        """import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

fun main() {
    val now = LocalDateTime.parse("2026-11-08T15:30:00")
    val formatter = DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm")
    val formattedDate = now.format(formatter)
    
    println("Formatlangan sana: $formattedDate")
}""",
        "Kotlin JVM muhitida Java ning barcha standart kutubxonalari bilan 100% integratsiyaga ega. 'java.time.LocalDateTime' va 'DateTimeFormatter' zamonaviy va xavfsiz sana bilan ishlash standartidir.",
        """Formatlangan sana: 08.11.2026 15:30"""
    ),
    (
        41,
        "Baytlardan Gigabaytga: Disk hajmini hisoblash",
        "Fayl hajmi baytlarda berilgan. Uni kilobayt, megabayt va gigabaytga o'tkazib, 2 ta o'nlik xonagacha formatlab chiqaring.",
        """fun formatFileSize(bytes: Long): String {
    val kb = bytes / 1024.0
    val mb = kb / 1024.0
    val gb = mb / 1024.0
    
    return when {
        gb >= 1.0 -> String.format("%.2f GB", gb)
        mb >= 1.0 -> String.format("%.2f MB", mb)
        kb >= 1.0 -> String.format("%.2f KB", kb)
        else -> "$bytes B"
    }
}

fun main() {
    println(formatFileSize(500L))
    println(formatFileSize(204800L))
    println(formatFileSize(157286400L))
    println(formatFileSize(5368709120L))
}""",
        "Katta hajmdagi baytlarni hisoblashda Long va Double turlari kombinatsiyasidan foydalaniladi. Bo'lish amali '1024.0' orqali bajarilganda natija avtomatik ravishda Double ga aylanadi.",
        """500 B
200.00 KB
150.00 MB
5.00 GB"""
    ),
    (
        42,
        "Harorat konvertori: Selsiy va Farengeyt",
        "Selsiy shkalasidagi haroratni Farengeytga (F = C * 9/5 + 32) va aksincha hisoblovchi dastur yozing.",
        """fun celsiusToFahrenheit(c: Double): Double = (c * 9.0 / 5.0) + 32.0
fun fahrenheitToCelsius(f: Double): Double = (f - 32.0) * 5.0 / 9.0

fun main() {
    val tempC = 25.0
    val tempF = celsiusToFahrenheit(tempC)
    val convertedBackC = fahrenheitToCelsius(tempF)
    
    println("$tempC°C = $tempF°F")
    println("$tempF°F = $convertedBackC°C")
}""",
        "Arifmetik amallarda aniqlikni saqlash uchun '9.0 / 5.0' deb yoziladi. Agar '9 / 5' deb yozilsa, butun sonli bo'lish sodir bo'lib natija 1 ga teng bo'lib qoladi va xato hisoblanadi.",
        """25.0°C = 77.0°F
77.0°F = 25.0°C"""
    ),
    (
        43,
        "Valyuta konvertori va yaxlitlash",
        "So'mdan AQSH dollariga va yevroga o'tkazuvchi valyuta kalkulyatorini yarating.",
        """fun convertCurrency(uzsAmount: Double, rate: Double): Double {
    return uzsAmount / rate
}

fun main() {
    val uzsAmount = 15_000_000.0
    val usdRate = 12800.0
    val eurRate = 13900.0
    
    val inUsd = convertCurrency(uzsAmount, usdRate)
    val inEur = convertCurrency(uzsAmount, eurRate)
    
    println("So'm miqdori: %,.0f UZS".format(uzsAmount))
    println("AQSH dollari: $%,.2f".format(inUsd))
    println("Yevro: €%,.2f".format(inEur))
}""",
        "Valyuta konvertatsiyasida Double turidan foydalanib, natijani 'format()' metodi orqali chiroyli va qulay vizual ko'rinishga keltirish amaliy dasturlashda keng qo'llaniladi.",
        """So'm miqdori: 15,000,000 UZS
AQSH dollari: $1,171.88
Yevro: €1,079.14"""
    ),
    (
        44,
        "Kompilyatsiya vaqtidagi tekshiruvlar: Type Safety tamoyillari",
        "Kotlinda har xil tiplarni bir-biriga tasodifiy biriktirish kompilyator tomonidan qanday to'xtatilishini tushuntiring.",
        """fun main() {
    val activeCount: Int = 10
    // val text: String = activeCount // Kompilyatsiya xatosi: Type mismatch
    val text: String = activeCount.toString() // To'g'ri usul
    
    println("Matnga aylangan son: $text")
}""",
        "Kotlin kuchli tiplashgan (strongly typed) tildir. Yashirin konvertatsiyalarga yo'l qo'yilmaydi. Har qanday tur o'zgarishi dasturchi irodasi bilan aniq ko'rsatilishi kerak.",
        """Matnga aylangan son: 10"""
    ),
    (
        45,
        "Bo'sh satrlarni tekshirish: isEmpty() va isBlank() farqi",
        "Matn bo'shligini tekshirishda 'isEmpty' va 'isBlank' farqini misollar orqali ko'rsating.",
        """fun main() {
    val str1 = ""
    val str2 = "   "
    val str3 = "Kotlin"
    
    println("str1: isEmpty = ${str1.isEmpty()}, isBlank = ${str1.isBlank()}")
    println("str2: isEmpty = ${str2.isEmpty()}, isBlank = ${str2.isBlank()}")
    println("str3: isEmpty = ${str3.isEmpty()}, isBlank = ${str3.isBlank()}")
}""",
        "'isEmpty()' faqat satr uzunligi aniq 0 bo'lgandagina true qaytaradi. 'isBlank()' esa satr bo'sh bo'lsa yoki faqatgina probel, tab, yangi qator kabi ko'rinmas bo'shliqlardan iborat bo'lsa ham true qaytaradi. Forma validatsiyasida 'isBlank()' ko'proq ishlatiladi.",
        """str1: isEmpty = true, isBlank = true
str2: isEmpty = false, isBlank = true
str3: isEmpty = false, isBlank = false"""
    ),
    (
        46,
        "Vaqt oraliqlarini hisoblash: Sekundlarni Soat:Minut:Sekund ga o'tkazish",
        "Jami berilgan sekundlarni (masalan, video davomiyligi) 'HH:mm:ss' formatiga keltiruvchi algoritm yozing.",
        """fun formatDuration(totalSeconds: Int): String {
    val hours = totalSeconds / 3600
    val minutes = (totalSeconds % 3600) / 60
    val seconds = totalSeconds % 60
    
    return String.format("%02d:%02d:%02d", hours, minutes, seconds)
}

fun main() {
    println(formatDuration(45))
    println(formatDuration(3675))
    println(formatDuration(7322))
}""",
        "Butun sonli bo'lish (/) va modul (%) operatorlari vaqt oraliqlarini ajratishda asosiy vosita hisoblanadi. '%02d' format belgisi agar son 1 xonali bo'lsa oldiga 0 qo'shib beradi.",
        """00:00:45
01:01:15
02:02:02"""
    ),
    (
        47,
        "BMI (Tana massasi indeksi) hisoblagich dasturi",
        "Vazn (kg) va bo'y (metr) asosida BMI (BMI = vazn / bo'y^2) ko'rsatkichini hisoblang va xulosa chiqaring.",
        """fun calculateBMI(weightKg: Double, heightM: Double): Pair<Double, String> {
    val bmi = weightKg / (heightM * heightM)
    val status = when {
        bmi < 18.5 -> "Vazn yetishmasligi"
        bmi < 25.0 -> "Normal vazn"
        bmi < 30.0 -> "Ortiqcha vazn"
        else -> "Semizlik"
    }
    return Pair(bmi, status)
}

fun main() {
    val (bmi, status) = calculateBMI(72.5, 1.78)
    println("BMI indeksi: ${String.format("%.1f", bmi)}")
    println("Holat: $status")
}""",
        "Funksiyadan birdaniga 2 ta qiymat qaytarish uchun 'Pair' va destrukturizatsiya '(bmi, status)' sintaksisi qo'llanildi. Bu kodni toza va tushunarli qiladi.",
        """BMI indeksi: 22.9
Holat: Normal vazn"""
    ),
    (
        48,
        "Bank depozit hisob-kitobi: Murakkab foiz (Compound Interest)",
        "Boshlang'ich summa, yillik foiz va yillar soni asosida murakkab foiz bilan yakuniy summani hisoblang: A = P * (1 + r)^n.",
        """import kotlin.math.pow

fun calculateCompoundInterest(principal: Double, annualRate: Double, years: Int): Double {
    val rateDecimal = annualRate / 100.0
    return principal * (1.0 + rateDecimal).pow(years.toDouble())
}

fun main() {
    val deposit = 10_000_000.0 // 10 mln so'm
    val rate = 21.0 // 21%
    val durationYears = 3
    
    val total = calculateCompoundInterest(deposit, rate, durationYears)
    val profit = total - deposit
    
    println("Boshlang'ich depozit: %,.0f UZS".format(deposit))
    println("$durationYears yildan keyin jami: %,.0f UZS".format(total))
    println("Sof daromad: %,.0f UZS".format(profit))
}""",
        "Murakkab foiz formulasi moliya sohasida klassik hisoblanadi. Kotlinda '.pow()' funksiyasi 'kotlin.math' to'plamidan chaqiriladi va Double parametrlar bilan ishlaydi.",
        """Boshlang'ich depozit: 10,000,000 UZS
3 yildan keyin jami: 17,715,610 UZS
Sof daromad: 7,715,610 UZS"""
    ),
    (
        49,
        "Matnlarni tekshirish: Palindromlikni aniqlash",
        "Berilgan so'z yoki iboraning chapdan ham, o'ngdan ham bir xil o'qilishini (palindrom) tekshiruvchi dastur tuzing.",
        """fun isPalindrome(text: String): Boolean {
    val cleanText = text.lowercase().filter { it.isLetterOrDigit() }
    return cleanText == cleanText.reversed()
}

fun main() {
    val test1 = "Kiyik"
    val test2 = "Aziza"
    val test3 = "Dasturchi"
    val test4 = "A man, a plan, a canal: Panama"
    
    println("'$test1' palindrommi: ${isPalindrome(test1)}")
    println("'$test2' palindrommi: ${isPalindrome(test2)}")
    println("'$test3' palindrommi: ${isPalindrome(test3)}")
    println("'$test4' palindrommi: ${isPalindrome(test4)}")
}""",
        "'filter { it.isLetterOrDigit() }' yordamida tinish belgilari va bo'shliqlar chiqarib tashlanadi. '.reversed()' metodi satrni teskarisiga aylantiradi. '==' bilan ularning bir xilligi taqqoslanadi.",
        """'Kiyik' palindrommi: true
'Aziza' palindrommi: true
'Dasturchi' palindrommi: false
'A man, a plan, a canal: Panama' palindrommi: true"""
    ),
    (
        50,
        "Umumiy jamlama: Foydalanuvchi ma'lumotlari hisoboti",
        "Turli ma'lumot turlari (String, Int, Double, Boolean) va formatlash imkoniyatlarini birlashtirib, to'liq hisobot kartasini shakllantiring.",
        """fun main() {
    val developerName = "Sardor Aliyev"
    val completedProjects = 14
    val hourlyRate = 35.50
    val totalHoursWorked = 160.0
    val isVerified = true
    
    val grossSalary = hourlyRate * totalHoursWorked
    val taxRate = 0.12
    val netSalary = grossSalary * (1 - taxRate)
    
    val report = \"\"\"
        ==================================================
        ISHLAB CHIQARUVCHI HISOBOTI
        ==================================================
        Ism: $developerName ${if (isVerified) "[Tasdiqlangan]" else "[Tasdiqlanmagan]"}
        Bajarilgan loyihalar: $completedProjects ta
        Ishlangan vaqt: $totalHoursWorked soat
        Soatlik stavka: $${hourlyRate}/soat
        --------------------------------------------------
        Yalpi daromad (Gross): $${"%,.2f".format(grossSalary)}
        Soliq (12%): $${"%,.2f".format(grossSalary * taxRate)}
        Sof daromad (Net): $${"%,.2f".format(netSalary)}
        ==================================================
    \"\"\".trimIndent()
    
    println(report)
}""",
        "Ushbu yakuniy topshiriqda 'val' o'zgaruvchilari, 'Double', 'Int', 'Boolean', 'String' turlari, arifmetik amallar, shartli matn interpolatsiyasi 'if' ifodasi hamda raw string formatlash imkoniyatlari uyg'unlashtirildi.",
        """==================================================
ISHLAB CHIQARUVCHI HISOBOTI
==================================================
Ism: Sardor Aliyev [Tasdiqlangan]
Bajarilgan loyihalar: 14 ta
Ishlangan vaqt: 160.0 soat
Soatlik stavka: $35.5/soat
--------------------------------------------------
Yalpi daromad (Gross): $5,680.00
Soliq (12%): $681.60
Sof daromad (Net): $4,998.40
=================================================="""
    )
]

for item in data_01:
    n, title, condition, sol, exp, res = item
    tasks.append(format_task(n, title, condition, sol, exp, res))

save_file("kotlin_01_asoslar_tiplar_va_ozgaruvchilar.md", tasks)
