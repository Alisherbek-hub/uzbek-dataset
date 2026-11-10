# 1-Topshiriq: O'zgarmas o'zgaruvchi e'lon qilish: 'val' kalit so'zi
## Topshiriq sharti:
Dasturda foydalanuvchining ID raqami va ro'yxatdan o'tgan sanasini o'zgarmas (read-only) shaklda e'lon qiling. Ularni chop eting.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val userId: Long = 100452L
    val registrationDate: String = "2026-03-15"
    
    println("Foydalanuvchi ID: $userId")
    println("Ro'yxatdan o'tgan sana: $registrationDate")
}
```

## Tushuntirish va Mantiq:
Kotlinda 'val' (value) kalit so'zi o'zgarmas o'zgaruvchi e'lon qilish uchun ishlatiladi. Java tilidagi 'final' kalit so'ziga to'g'ri keladi. Bir marta qiymat biriktirilgach, uni qayta o'zgartirib bo'lmaydi, bu esa ko'p oqimli (multithreaded) muhitda immutability (o'zgarmaslik) tamoyilini ta'minlaydi.

## Ishlash natijasi:
```text
Foydalanuvchi ID: 100452
Ro'yxatdan o'tgan sana: 2026-03-15
```


# 2-Topshiriq: O'zgaruvchan qiymatlar: 'var' kalit so'zi bilan ishlash
## Topshiriq sharti:
Onlayn do'konda xarid savatidagi tovarlar soni va umumiy summani saqlovchi o'zgaruvchilar e'lon qiling. Yangi mahsulot qo'shilganda ularning qiymatini oshiring va yangilangan natijani chiqaring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    var itemCount: Int = 3
    var totalAmount: Double = 150.0
    
    println("Boshlang'ich holat: Mahsulotlar: $itemCount ta, Jami: $$totalAmount")
    
    // Yangi mahsulot qo'shildi
    itemCount += 2
    totalAmount += 95.5
    
    println("Yangilangan holat: Mahsulotlar: $itemCount ta, Jami: $$totalAmount")
}
```

## Tushuntirish va Mantiq:
'var' (variable) o'zgaruvchan kattaliklarni e'lon qilishda qo'llaniladi. Uning qiymati dastur bajarilishi davomida istalgancha qayta belgilanishi mumkin, ammo uning ma'lumot turi o'zgarmas bo'lib qoladi (masalan, Int turidagi o'zgaruvchiga String yozib bo'lmaydi).

## Ishlash natijasi:
```text
Boshlang'ich holat: Mahsulotlar: 3 ta, Jami: $150.0
Yangilangan holat: Mahsulotlar: 5 ta, Jami: $245.5
```


# 3-Topshiriq: Tipni avtomatik aniqlash (Type Inference)
## Topshiriq sharti:
O'zgaruvchi turini aniq (explicit) ko'rsatmasdan turli tiplardagi o'zgaruvchilarni e'lon qiling. Kotlin kompilyatori ularning turini qanday aniqlaganini tekshirib ko'ring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val siteName = "TechUzbekistan"
    val visitorCount = 45000
    val rating = 4.95
    val isActive = true
    
    println("Sayt nomi: $siteName (Turi: ${siteName::class.simpleName})")
    println("Tashrif buyuruvchilar: $visitorCount (Turi: ${visitorCount::class.simpleName})")
    println("Reyting: $rating (Turi: ${rating::class.simpleName})")
    println("Faol: $isActive (Turi: ${isActive::class.simpleName})")
}
```

## Tushuntirish va Mantiq:
Kotlin kuchli statik tiplashtirilgan til bo'lishiga qaramay, 'Type Inference' (tur xulosasi) xususiyatiga ega. Agar boshlang'ich qiymat berilsa, kompilyator kontekstga qarab o'zgaruvchi turini avtomatik ravishda belgilaydi. '::class.simpleName' orqali o'zgaruvchining Kotlin klass turi aniqlanadi.

## Ishlash natijasi:
```text
Sayt nomi: TechUzbekistan (Turi: String)
Tashrif buyuruvchilar: 45000 (Turi: Int)
Reyting: 4.95 (Turi: Double)
Faol: true (Turi: Boolean)
```


# 4-Topshiriq: Butun sonli tiplar: Byte va Short bilan xotirani tejash
## Topshiriq sharti:
Sensor qurilmasidan keluvchi batareya quvvati foizi (0..100) va harorat qiymatini (-50..50) minimal xotira egallaydigan tiplarda saqlang.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val batteryPercentage: Byte = 85
    val ambientTemp: Short = -15
    
    println("Batareya quvvati: $batteryPercentage%")
    println("Atrof-muhit harorati: $ambientTemp°C")
    println("Byte min: ${Byte.MIN_VALUE}, max: ${Byte.MAX_VALUE}")
    println("Short min: ${Short.MIN_VALUE}, max: ${Short.MAX_VALUE}")
}
```

## Tushuntirish va Mantiq:
Byte 8-bitli butun son bo'lib (-128 dan 127 gacha), Short 16-bitli son (-32768 dan 32767 gacha). IoT yoki xotira cheklangan tizimlarda Int (32-bit) o'rniga Byte yoki Short qo'llash katta massivlarda xotiradan foydalanish samaradorligini 2-4 barobar oshiradi.

## Ishlash natijasi:
```text
Batareya quvvati: 85%
Atrof-muhit harorati: -15°C
Byte min: -128, max: 127
Short min: -32768, max: 32767
```


# 5-Topshiriq: Katta sonlar: Long turi va L prefiksi
## Topshiriq sharti:
Dunyo aholisi soni va yorug'likning 1 yilda bosib o'tadigan masofasini (metrlarda) Long turida saqlang va ekranga chiqaring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val worldPopulation: Long = 8_100_000_000L
    val lightYearMeters: Long = 9_460_730_472_580_800L
    
    println("Dunyo aholisi: $worldPopulation kishi")
    println("1 yorug'lik yili: $lightYearMeters metr")
}
```

## Tushuntirish va Mantiq:
32-bitli Int maksimal ~2.14 milliardgacha qiymat saqlay oladi. Undan katta qiymatlar uchun 64-bitli Long kerak. Kotlinda Long literallar oxiriga 'L' qo'shiladi. Shuningdek, o'qishni osonlashtirish uchun raqamlar orasiga pastki chiziq '_' qo'yish mumkin.

## Ishlash natijasi:
```text
Dunyo aholisi: 8100000000 kishi
1 yorug'lik yili: 9460730472580800 metr
```


# 6-Topshiriq: Suzuvchi nuqtali sonlar: Float vs Double aniqligi
## Topshiriq sharti:
Doiraning yuzi va radiusini hisoblashda Float (32-bit) va Double (64-bit) aniqlik farqlarini solishtiring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val piFloat: Float = 3.141592653589793f
    val piDouble: Double = 3.141592653589793
    
    println("Float aniqligi : $piFloat")
    println("Double aniqligi: $piDouble")
    
    val radius = 5.0
    val areaFloat = (piFloat * radius * radius).toFloat()
    val areaDouble = piDouble * radius * radius
    
    println("Yuza (Float): $areaFloat")
    println("Yuza (Double): $areaDouble")
}
```

## Tushuntirish va Mantiq:
Float 32-bit bo'lib, taxminan 6-7 ta o'nlik raqam aniqligini beradi va uning qiymati 'f' yoki 'F' bilan tugashi shart. Double esa 64-bit bo'lib, 15-16 ta raqam aniqligini kafolatlaydi. Kotlinda sukut bo'yicha barcha suzuvchi nuqtali sonlar Double hisoblanadi.

## Ishlash natijasi:
```text
Float aniqligi : 3.1415927
Double aniqligi: 3.141592653589793
Yuza (Float): 78.53982
Yuza (Double): 78.53981633974483
```


# 7-Topshiriq: Belgilar bilan ishlash: Char turi va amallar
## Topshiriq sharti:
Belgining harf, raqam yoki maxsus belgi ekanligini aniqlovchi va uning Unicode kodini ko'rsatuvchi dastur yozing.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val ch1: Char = 'A'
    val ch2: Char = '7'
    val ch3: Char = '❤' // Yurak belgisi
    
    println("Belgi 1: $ch1, Harfmi: ${ch1.isLetter()}, Kodi: ${ch1.code}")
    println("Belgi 2: $ch2, Raqammi: ${ch2.isDigit()}, Kodi: ${ch2.code}")
    println("Belgi 3: $ch3, Unicode kodi: ${ch3.code}")
}
```

## Tushuntirish va Mantiq:
Kotlinda Char bitta 16-bitli Unicode belgisini ifodalaydi va yakka tirnoq ' ' ichiga olinadi. Java dan farqli o'laroq, Char turini to'g'ridan-to'g'ri butun son sifatida ishlatib bo'lmaydi; uning kodini olish uchun '.code' xususiyatidan foydalaniladi.

## Ishlash natijasi:
```text
Belgi 1: A, Harfmi: true, Kodi: 65
Belgi 2: 7, Raqammi: true, Kodi: 55
Belgi 3: ❤, Unicode kodi: 10084
```


# 8-Topshiriq: Mantiqiy amallar va qisqa tutashuv (Short-circuit evaluation)
## Topshiriq sharti:
Foydalanuvchining tizimga kirish huquqini tekshiruvchi mantiqiy ifoda tuzing. Unda '&&' va '||' operatorlarining ishlash mexanizmini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
fun checkAccess(isAdmin: Boolean, isRegistered: Boolean, hasActiveToken: Boolean): Boolean {
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
}
```

## Tushuntirish va Mantiq:
Kotlinda mantiqiy '&&' (va) hamda '||' (yoki) operatorlari qisqa tutashuv (short-circuit) tamoyili asosida ishlaydi. '||' operatorida birinchi operand true bo'lsa, ikkinchisi hisoblanmaydi. '&&' da esa birinchi operand false bo'lsa, qolgani tashlab ketiladi.

## Ishlash natijasi:
```text
Admin huquqi: true
Oddiy faol foydalanuvchi: true
Muddati tugagan foydalanuvchi: false
```


# 9-Topshiriq: String shablonlari (String Templates) va hisoblashlar
## Topshiriq sharti:
Matn ichida o'zgaruvchilarni va arifmetik amallarni $ va ${} orqali integratsiya qilish dasturini tuzing.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val mahsulot = "Noutbuk"
    val narx = 1200
    val soliqFoizi = 12
    
    println("Mahsulot: $mahsulot")
    println("Narxi: $narx AQSH dollari")
    println("Soliq bilan jami: ${narx + (narx * soliqFoizi / 100)} AQSH dollari")
    println("Belgi narxi: \$$narx (valyuta belgisi chiqishi uchun)")
}
```

## Tushuntirish va Mantiq:
Kotlinda satr ichiga o'zgaruvchi qiymatini kiritish uchun '$o_zgaruvchi' sintaksisi ishlatiladi. Agar ifoda yoki arifmetik amal bajarish kerak bo'lsa, '${ifoda}' shaklida qavslar qo'llaniladi. Dollar belgisining o'zini chiqarish uchun esa '\$' yoki "${'$'}" yoziladi.

## Ishlash natijasi:
```text
Mahsulot: Noutbuk
Narxi: 1200 AQSH dollari
Soliq bilan jami: 1344 AQSH dollari
Belgi narxi: $1200 (valyuta belgisi chiqishi uchun)
```


# 10-Topshiriq: Ko'p qatorli matnlar (Raw Strings) va trimIndent()
## Topshiriq sharti:
Ko'p qatorli JSON ma'lumotini raw string (""") yordamida formatlab, keraksiz bo'shliqlarni 'trimIndent()' bilan olib tashlang.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val jsonResponse = """
        {
            "status": "success",
            "code": 200,
            "data": {
                "server": "Toshkent-01",
                "uptime": "99.9%"
            }
        }
    """.trimIndent()
    
    println(jsonResponse)
}
```

## Tushuntirish va Mantiq:
Kotlinda uchlik qo'shtirnoq '"""' bilan o'ralgan matnlar escape belgilarini talab qilmaydi va asl formatini saqlaydi. 'trimIndent()' funksiyasi barcha qatorlar uchun umumiy bo'lgan chap bo'shliqlarni olib tashlaydi, bu esa kodni chiroyli va o'qishli saqlashga imkon beradi.

## Ishlash natijasi:
```text
{
    "status": "success",
    "code": 200,
    "data": {
        "server": "Toshkent-01",
        "uptime": "99.9%"
    }
}
```


# 11-Topshiriq: Chegara bo'shliqlarini boshqarish: trimMargin()
## Topshiriq sharti:
Ko'p qatorli SQL so'rovini maxsus belgi (masalan, '|') yordamida tekislab, 'trimMargin()' orqali formatlang.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val tableName = "mijozlar"
    val query = """
        |SELECT id, ism, balans
        |FROM $tableName
        |WHERE balans > 0
        |ORDER BY balans DESC;
    """.trimMargin("|")
    
    println(query)
}
```

## Tushuntirish va Mantiq:
'trimMargin()' funksiyasi har bir qatorda ko'rsatilgan belgigacha (standart bo'yicha '|') bo'lgan barcha bo'shliqlarni olib tashlaydi. Bu ko'p qatorli matnlarni koddagi indentatsiya chuqurligidan qat'i nazar chetga tekislashda qulay vositadir.

## Ishlash natijasi:
```text
SELECT id, ism, balans
FROM mijozlar
WHERE balans > 0
ORDER BY balans DESC;
```


# 12-Topshiriq: Aniq sonli konvertatsiya (Explicit Type Conversion)
## Topshiriq sharti:
Kotlinda Java kabi avtomatik tip kengayishi (implicit widening) mavjud emasligini namoyish qiling va toInt(), toLong(), toDouble() metodlaridan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val intValue: Int = 42
    // val longValue: Long = intValue // Kompilyatsiya xatosi: Type mismatch
    val longValue: Long = intValue.toLong()
    val doubleValue: Double = intValue.toDouble()
    val byteValue: Byte = intValue.toByte()
    
    println("Int qiymat: $intValue")
    println("Long qiymat: $longValue")
    println("Double qiymat: $doubleValue")
    println("Byte qiymat: $byteValue")
}
```

## Tushuntirish va Mantiq:
Kotlin tip xavfsizligiga qat'iy rioya qiladi. Kichik turdagi sonlar (masalan, Int) katta turdagi o'zgaruvchilarga (masalan, Long yoki Double) avtomatik o'tmaydi. Har bir konvertatsiya dasturchi tomonidan aniq 'toXxx()' metodlari orqali chaqirilishi shart, bu yashirin noaniqliklarning oldini oladi.

## Ishlash natijasi:
```text
Int qiymat: 42
Long qiymat: 42
Double qiymat: 42.0
Byte qiymat: 42
```


# 13-Topshiriq: Matndan songa o'tkazish va xavfsiz konvertatsiya: toIntOrNull()
## Topshiriq sharti:
Foydalanuvchi kiritgan matnli yoshni xavfsiz tarzda Int turiga o'tkazing va xato kiritilganda dastur qulashini oldini oling.

## Yechim (Kotlin kodi):
```kotlin
fun parseUserAge(input: String): Int {
    val age = input.toIntOrNull()
    return age ?: 0 // Agar null bo'lsa, 0 qaytaradi
}

fun main() {
    val inputValid = "28"
    val inputInvalid = "yigirma sakkiz"
    
    println("To'g'ri kiritish: ${parseUserAge(inputValid)}")
    println("Noto'g'ri kiritish: ${parseUserAge(inputInvalid)}")
}
```

## Tushuntirish va Mantiq:
'toInt()' metodi son bo'lmagan matnda 'NumberFormatException' tashlaydi. 'toIntOrNull()' esa xato bo'lsa dasturni to'xtatmay, 'null' qaytaradi. Elvis operatori '?:' bilan birgalikda bu juda qulay va xavfsiz konvertatsiya andozasidir.

## Ishlash natijasi:
```text
To'g'ri kiritish: 28
Noto'g'ri kiritish: 0
```


# 14-Topshiriq: Belgini uning raqam qiymatiga o'tkazish: digitToInt()
## Topshiriq sharti:
Char turidagi raqam belgisini ('0'..'9') haqiqiy arifmetik Int songa aylantiruvchi zamonaviy Kotlinga xos metodni qo'llang.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val charDigit: Char = '9'
    
    // Eski/noto'g'ri usul: charDigit.code - bu 57 (ASCII kod) beradi
    val asciiCode = charDigit.code
    
    // Kotlin 1.5+ zamonaviy usul:
    val realNumber = charDigit.digitToInt()
    
    println("Belgi: '$charDigit'")
    println("ASCII kodi: $asciiCode")
    println("Haqiqiy raqam qiymati: $realNumber")
    println("Hisoblash: $realNumber * 5 = ${realNumber * 5}")
}
```

## Tushuntirish va Mantiq:
Kotlinda belgining ASCII/Unicode kodini olish (char.code) va uning son qiymatini olish (char.digitToInt()) qat'iy farqlanadi. 'digitToInt()' agar belgi haqiqatan ham '0'..'9' oralig'ida bo'lsa uning haqiqiy raqam qiymatini qaytaradi, aks holda 'IllegalArgumentException' beradi.

## Ishlash natijasi:
```text
Belgi: '9'
ASCII kodi: 57
Haqiqiy raqam qiymati: 9
Hisoblash: 9 * 5 = 45
```


# 15-Topshiriq: O'n oltilik (Hexadecimal) va ikkilik (Binary) literallar
## Topshiriq sharti:
Turli sanoq tizimlaridagi sonlarni (ikkilik '0b', o'n oltilik '0x') e'lon qiling va ularni o'nlik tizimda chop eting.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val hexValue = 0x1A // 16-lik tizimda 1A = 26
    val binaryValue = 0b10110 // 2-lik tizimda 10110 = 22
    val mask = 0xFF_00 // 65280
    
    println("Hex 0x1A: $hexValue")
    println("Binary 0b10110: $binaryValue")
    println("Mask 0xFF00: $mask")
    println("Hex formatda qayta chiqarish: ${hexValue.toString(16).uppercase()}")
}
```

## Tushuntirish va Mantiq:
Kotlinda o'n oltilik sonlar '0x' prefiksi bilan, ikkilik sonlar esa '0b' prefiksi bilan yoziladi. Kotlinda sakkizlik (octal) literallar qo'llab-quvvatlanmaydi. '.toString(radix)' funksiyasi orqali sonni istalgan sanoq sistemasida satrga aylantirish mumkin.

## Ishlash natijasi:
```text
Hex 0x1A: 26
Binary 0b10110: 22
Mask 0xFF00: 65280
Hex formatda qayta chiqarish: 1A
```


# 16-Topshiriq: Bit darajasidagi amallar (Bitwise operations)
## Topshiriq sharti:
Kotlinda 'shl', 'shr', 'and', 'or', 'xor', 'inv' infix funksiyalaridan foydalanib bitlar ustida amallar bajaring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val a = 0b0011 // 3
    val b = 0b0101 // 5
    
    println("a AND b: ${a and b}") // 0b0001 = 1
    println("a OR b : ${a or b}")  // 0b0111 = 7
    println("a XOR b: ${a xor b}") // 0b0110 = 6
    println("a SHL 1: ${a shl 1}") // 0b0110 = 6
    println("b SHR 1: ${b shr 1}") // 0b0010 = 2
    println("a INV  : ${a.inv()}") // bitwise inverting
}
```

## Tushuntirish va Mantiq:
Java dagi bitwise operatorlar (&, |, ^, <<, >>) o'rniga Kotlinda o'qishga qulay infix funksiyalar ishlatiladi: 'and', 'or', 'xor', 'shl' (chapga surish), 'shr' (o'ngga surish), 'ushr' (ishorasiz o'ngga surish) va 'inv()' (inkor).

## Ishlash natijasi:
```text
a AND b: 1
a OR b : 7
a XOR b: 6
a SHL 1: 6
b SHR 1: 2
a INV  : -4
```


# 17-Topshiriq: Ishorasiz butun sonlar (Unsigned Integers): UByte, UInt, ULong
## Topshiriq sharti:
Faqat musbat sonlarni saqlovchi va xotirani to'liq musbat diapazon uchun ishlatuvchi UInt va UByte turlarini sinab ko'ring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val unsignedByte: UByte = 250u
    val unsignedInt: UInt = 4_000_000_000u
    val unsignedLong: ULong = 18_000_000_000_000_000_000uL
    
    println("UByte qiymat: $unsignedByte (Maksimal: ${UByte.MAX_VALUE})")
    println("UInt qiymat: $unsignedInt (Maksimal: ${UInt.MAX_VALUE})")
    println("ULong qiymat: $unsignedLong (Maksimal: ${ULong.MAX_VALUE})")
}
```

## Tushuntirish va Mantiq:
Kotlin 'inline value classes' asosida qurilgan 'Unsigned' (ishorasiz) son turlarini taqdim etadi: UByte (0..255), UShort (0..65535), UInt (0..4.29 mlrd) va ULong. Ularni ifodalash uchun son oxiriga 'u' yoki 'uL' suffiksi qo'yiladi.

## Ishlash natijasi:
```text
UByte qiymat: 250 (Maksimal: 255)
UInt qiymat: 4000000000 (Maksimal: 4294967295)
ULong qiymat: 18000000000000000000 (Maksimal: 18446744073709551615)
```


# 18-Topshiriq: Konstanta qiymatlar: 'const val' va kompilyatsiya vaqtidagi konstantalar
## Topshiriq sharti:
Kompilyatsiya vaqtida (compile-time) hisoblanuvchi 'const val' o'zgaruvchilarini e'lon qiling va uning oddiy 'val' dan farqini tushuntiring.

## Yechim (Kotlin kodi):
```kotlin
const val APP_VERSION = "2.4.0"
const val MAX_RETRY_COUNT = 3

fun main() {
    val runtimeDate = java.time.LocalDate.now().toString()
    
    println("Ilova versiyasi: $APP_VERSION")
    println("Urinishlar limiti: $MAX_RETRY_COUNT")
    println("Ishga tushgan sana: $runtimeDate")
}
```

## Tushuntirish va Mantiq:
'const val' faqat kompilyatsiya vaqtida ma'lum bo'ladigan primitiv tiplar yoki String uchun qo'llaniladi va faylning yuqori darajasida (top-level) yoki 'object' ichida e'lon qilinadi. U bayt-kodda to'g'ridan-to'g'ri almashtiriladi (inlining), oddiy 'val' esa ish vaqtida (runtime) ham hisoblanishi mumkin.

## Ishlash natijasi:
```text
Ilova versiyasi: 2.4.0
Urinishlar limiti: 3
Ishga tushgan sana: 2026-11-08
```


# 19-Topshiriq: Any turi: Kotlindagi eng yuqori umumiy tip
## Topshiriq sharti:
Har qanday ma'lumot turini qabul qila oladigan 'Any' turidagi o'zgaruvchini yarating va uning standart metodlarini tekshiring.

## Yechim (Kotlin kodi):
```kotlin
fun printObjectInfo(obj: Any) {
    println("Obyekt: $obj | Klass: ${obj::class.simpleName} | HashCode: ${obj.hashCode()}")
}

fun main() {
    printObjectInfo(100)
    printObjectInfo("Salom Dunyo")
    printObjectInfo(true)
    printObjectInfo(3.14)
}
```

## Tushuntirish va Mantiq:
Kotlinda 'Any' barcha null bo'lmagan (non-nullable) tiplarning ota sinfidir (Java dagi 'Object' ga o'xshash). Har bir Kotlin klassi Any dan meros oladi va unda 3 ta asosiy metod mavjud: 'equals()', 'hashCode()' va 'toString()'.

## Ishlash natijasi:
```text
Obyekt: 100 | Klass: Int | HashCode: 100
Obyekt: Salom Dunyo | Klass: String | HashCode: 2068999330
Obyekt: true | Klass: Boolean | HashCode: 1231
Obyekt: 3.14 | Klass: Double | HashCode: 219930624
```


# 20-Topshiriq: Unit turi: Qiymat qaytarmaydigan funksiyalar
## Topshiriq sharti:
Hech qanday ma'noli qiymat qaytarmaydigan funksiyalarda 'Unit' turining vazifasini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
fun logMessage(message: String): Unit {
    println("[LOG]: $message")
    // return Unit yozish shart emas, avtomatik qaytadi
}

fun main() {
    val result: Unit = logMessage("Tizim muvaffaqiyatli yuklandi.")
    println("Qaytgan qiymat turi: ${result::class.simpleName}")
}
```

## Tushuntirish va Mantiq:
Java dagi 'void' dan farqli o'laroq, Kotlin da 'Unit' haqiqiy singleton obyekt hisoblanadi. Agar funksiya qiymat qaytarmasa, u sukut bo'yicha 'Unit' turini qaytaradi. Bu generiklar va funksional dasturlashda bir xillikni (consistency) ta'minlaydi.

## Ishlash natijasi:
```text
[LOG]: Tizim muvaffaqiyatli yuklandi.
Qaytgan qiymat turi: Unit
```


# 21-Topshiriq: Nothing turi: Hech qachon tugamaydigan yoki istisno tashlovchi ifodalar
## Topshiriq sharti:
Funksiya xatolik tashlaganda yoki cheksiz sikl bo'lganda 'Nothing' turining qanday ishlatilishini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
fun failWithError(message: String): Nothing {
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
}
```

## Tushuntirish va Mantiq:
'Nothing' Kotlindagi barcha tiplarning quyi (bottom) tipidir va uning hech qanday nusxasi bo'lishi mumkin emas. U funksiya hech qachon normal yakunlanmasligini (istisno tashlaydi yoki cheksiz to'xtaydi) kompilyatorga bildirish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Ushlangan istisno: Kritik xatolik: Baza bilan aloqa yo'q!
```


# 22-Topshiriq: Primitiv tiplar va obyekt o'rash (Autoboxing) tushunchasi
## Topshiriq sharti:
Kotlinda barcha tiplar obyekt sifatida ko'rinsa-da, bayt-kod darajasida qachon Java primitiviga (int), qachon o'ralgan obyektga (Integer) aylanishini solishtiring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val primitiveInt: Int = 10 // Bayt-kodda int bo'ladi
    val nullableInt: Int? = 10 // Bayt-kodda java.lang.Integer ga aylanadi
    
    println("primitiveInt: $primitiveInt")
    println("nullableInt: $nullableInt")
    println("Tenglik tekshiruvi: ${primitiveInt == nullableInt}")
}
```

## Tushuntirish va Mantiq:
Kotlinda kod yozayotganda barcha tiplar obyektga o'xshaydi. Ammo Kotlin kompilyatori (K2) optimallashtirish o'tkazadi: agar o'zgaruvchi null bo'lmasa (Int), u JVM da tez ishlaydigan oddiy primitiv 'int' ga kompilyatsiya bo'ladi. Agar o'zgaruvchi nullable (Int?) bo'lsa yoki generiklarda ishlatilsa, obyekt o'rami (Integer) hosil bo'ladi.

## Ishlash natijasi:
```text
primitiveInt: 10
nullableInt: 10
Tenglik tekshiruvi: true
```


# 23-Topshiriq: Math kutubxonasi yordamida matematik amallar
## Topshiriq sharti:
Kotlinda 'kotlin.math' kutubxonasidagi maxsus funksiyalar (sqrt, pow, round, ceil, floor) yordamida murakkab hisob-kitob bajaring.

## Yechim (Kotlin kodi):
```kotlin
import kotlin.math.*

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
}
```

## Tushuntirish va Mantiq:
'kotlin.math' to'plami Kotlin platformasiga xos bo'lib, Java ning 'Math' kutubxonasini to'liq almashtiradi va Kotlin Multiplatform (KMP) doirasida Android, iOS va Web platformalarida bir xil ishlaydi.

## Ishlash natijasi:
```text
Kvadrat ildiz: 5.0
Darajaga ko'tarish: 15625.0
Shiftga yaxlitlash (ceil): 5.0
Polga yaxlitlash (floor): 4.0
Eng yaqiniga yaxlitlash (round): 5.0
Sinus(pi / 2): 1.0
```


# 24-Topshiriq: String qidirish va tahlil qilish metodlari
## Topshiriq sharti:
Elektron pochta manzilini tahlil qilib, foydalanuvchi nomi va domen qismini ajratib oling.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val email = "dilshod.rahimov@example.uz"
    
    val atIndex = email.indexOf('@')
    val username = email.substring(0, atIndex)
    val domain = email.substring(atIndex + 1)
    val isUzDomain = email.endsWith(".uz")
    
    println("To'liq email: $email")
    println("Foydalanuvchi nomi: $username")
    println("Domen: $domain")
    println(".uz zonasidami: $isUzDomain")
}
```

## Tushuntirish va Mantiq:
Kotlinda String boy standart metodlar to'plamiga ega: 'indexOf', 'substring', 'startsWith', 'endsWith', 'contains' va boshqalar. Bu metodlar matnlarni xavfsiz va samarali tahlil qilish imkonini beradi.

## Ishlash natijasi:
```text
To'liq email: dilshod.rahimov@example.uz
Foydalanuvchi nomi: dilshod.rahimov
Domen: example.uz
.uz zonasidami: true
```


# 25-Topshiriq: Satrlarni almashtirish va tozalash: replace() va split()
## Topshiriq sharti:
Vergullar bilan ajratilgan mahsulotlar ro'yxatini tozalab, massivga ajrating va formatlang.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val rawInput = "  olma,  nok , uzum, shaftoli , anor  "
    val cleaned = rawInput.trim()
    val fruits = cleaned.split(",").map { it.trim().replaceFirstChar { char -> char.uppercase() } }
    
    println("Tozalangan va formatlangan ro'yxat:")
    fruits.forEachIndexed { index, fruit ->
        println("${index + 1}. $fruit")
    }
}
```

## Tushuntirish va Mantiq:
'split()' satrni berilgan ajratuvchi bo'yicha bo'laklaydi. 'trim()' boshidagi va oxiridagi bo'shliqlarni olib tashlaydi. 'replaceFirstChar()' esa Kotlinda belgining faqat birinchi harfini katta qilishning tavsiya etilgan zamonaviy usulidir.

## Ishlash natijasi:
```text
Tozalangan va formatlangan ro'yxat:
1. Olma
2. Nok
3. Uzum
4. Shaftoli
5. Anor
```


# 26-Topshiriq: Formatlangan satrlar: String.format()
## Topshiriq sharti:
Valyuta summasi va sanani aniq 2 ta o'nlik xonali va ustunli qilib 'String.format()' yordamida ekranga chiqaring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val clientName = "Anvar Karimov"
    val balance = 1254300.5678
    val discount = 7.5
    
    val formatted = String.format("Mijoz: %-15s | Balans: %,.2f so'm | Chegirma: %5.1f%%", clientName, balance, discount)
    println(formatted)
}
```

## Tushuntirish va Mantiq:
'String.format()' Java dagi formatlash mexanizmidan foydalanadi: '%,.2f' sonlarni mingliklarga ajratib (vergul bilan) va 2 ta o'nlik raqam bilan chiqaradi, '%-15s' chap tomondan tekislangan 15 ta belgili satr hosil qiladi.

## Ishlash natijasi:
```text
Mijoz: Anvar Karimov   | Balans: 1,254,300.57 so'm | Chegirma:   7.5%
```


# 27-Topshiriq: Belgilar ketma-ketligini solishtirish: equals vs ==
## Topshiriq sharti:
Kotlinda strukturaviy tenglik (==) va referensial tenglik (===) farqini namoyish qiling.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val str1 = "Kotlin"
    val str2 = "Kot" + "lin"
    val str3 = String(charArrayOf('K', 'o', 't', 'l', 'i', 'n'))
    
    println("str1 == str2: ${str1 == str2}")       // Strukturaviy qiymat tengligi (equals)
    println("str1 === str2: ${str1 === str2}")     // Xotiradagi bir xil havola (String pool)
    println("str1 == str3: ${str1 == str3}")       // Qiymati teng
    println("str1 === str3: ${str1 === str3}")     // Xotirada turli xil obyektlar
}
```

## Tushuntirish va Mantiq:
Kotlinda '==' operatori avtomatik ravishda '.equals()' metodini chaqiradi va null-safe ishlaydi. '===' operatori esa xotiradagi manzillarni (referensiyalarni) solishtiradi. Java dan farqli o'laroq, satrlarni qiymat bo'yicha solishtirish uchun '==' qo'llanilishi eng to'g'ri yo'ldir.

## Ishlash natijasi:
```text
str1 == str2: true
str1 === str2: true
str1 == str3: true
str1 === str3: false
```


# 28-Topshiriq: Mantiqiy shartlar zanjiri va ustuvorlik (Operator Precedence)
## Topshiriq sharti:
Murakkab mantiqiy ifodaning hisoblanish tartibini qavslar va operatorlar ustuvorligi orqali tekshiring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val hasTicket = true
    val hasVipPass = false
    val isBanned = false
    val isSecurityPassed = true
    
    // && operatori || ga qaraganda yuqori ustuvorlikka ega
    val canEnterWithoutParentheses = hasVipPass || hasTicket && !isBanned && isSecurityPassed
    val canEnterExplicit = hasVipPass || (hasTicket && (!isBanned) && isSecurityPassed)
    
    println("Kirish mumkinmi (odatiy): $canEnterWithoutParentheses")
    println("Kirish mumkinmi (aniq qavsli): $canEnterExplicit")
}
```

## Tushuntirish va Mantiq:
Mantiqiy amallarda '!' (inkor) eng yuqori, keyin '&&' (va), va eng past ustuvorlikka '||' (yoki) ega. Tushunmovchiliklarni oldini olish va kod tozaligi uchun murakkab ifodalarni har doim qavslar bilan ajratish tavsiya etiladi.

## Ishlash natijasi:
```text
Kirish mumkinmi (odatiy): true
Kirish mumkinmi (aniq qavsli): true
```


# 29-Topshiriq: O'zgaruvchilar doirasi (Variable Scope) va soyalash (Shadowing)
## Topshiriq sharti:
Ichki blokda tashqi blokdagi o'zgaruvchi nomini qayta ishlatish (shadowing) holatini namoyish qiling.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val x = 100
    println("Asosiy doiradagi x: $x")
    
    run {
        val x = 200 // Tashqi x ni soyalaydi (shadows)
        println("Ichki blokdagi x: $x")
    }
    
    println("Yana asosiy x: $x")
}
```

## Tushuntirish va Mantiq:
Kotlinda ichki bloklarda (masalan, if, for yoki lambda ichida) tashqi o'zgaruvchi bilan bir xil nomli yangi o'zgaruvchi e'lon qilinishi 'variable shadowing' deyiladi. Bu xato emas, lekin kodni chalkashtirmaslik uchun undan ehtiyotkorlik bilan foydalanish lozim.

## Ishlash natijasi:
```text
Asosiy doiradagi x: 100
Ichki blokdagi x: 200
Yana asosiy x: 100
```


# 30-Topshiriq: Arifmetik qisqartirilgan amallar (Compound Assignment Operators)
## Topshiriq sharti:
+=, -=, *=, /= va %= operatorlarining xatti-harakatini tekshiring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
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
}
```

## Tushuntirish va Mantiq:
Murakkab biriktirish operatorlari amaliyotda kodni qisqartiradi va barcha arifmetik amallar uchun ishlaydi. Butun sonlarni bo'lishda natija doimo pastga qarab butun qismgacha kesiladi.

## Ishlash natijasi:
```text
Qo'shishdan so'ng: 75
Ayirishdan so'ng: 60
Ko'paytirishdan so'ng: 120
Bo'lishdan so'ng: 30
Qoldiqdan so'ng: 2
```


# 31-Topshiriq: Prefix va Postfix inkrement/dekrement farqlari
## Topshiriq sharti:
++var va var++ amallarining amaldagi hisoblash ketma-ketligini solishtiring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    var a = 5
    var b = 5
    
    val prefixResult = ++a // Avval qiymat oshadi, keyin biriktiriladi
    val postfixResult = b++ // Avval eski qiymat biriktiriladi, keyin o'zgaruvchi oshadi
    
    println("Prefix natija: $prefixResult, a ning yakuniy qiymati: $a")
    println("Postfix natija: $postfixResult, b ning yakuniy qiymati: $b")
}
```

## Tushuntirish va Mantiq:
Prefix inkrement (++a) o'zgaruvchini avval 1 taga oshirib so'ngra yangi qiymatni ifodaga uzatadi. Postfix inkrement (b++) esa avval mavjud eski qiymatni ifodaga qaytarib, shundan keyingina o'zgaruvchini oshiradi.

## Ishlash natijasi:
```text
Prefix natija: 6, a ning yakuniy qiymati: 6
Postfix natija: 5, b ning yakuniy qiymati: 6
```


# 32-Topshiriq: Taqqoslash operatorlari (Comparison Operators)
## Topshiriq sharti:
>, <, >=, <= operatorlarining turli ma'lumot turlari (sonlar va satrlar) bilan ishlashini tekshiring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val speedLimit = 60
    val currentSpeed = 75
    val isOverSpeed = currentSpeed > speedLimit
    
    val word1 = "Olma"
    val word2 = "Banan"
    val isAlphabetical = word1 < word2 // Leksikografik taqqoslash
    
    println("Tezlik oshdimi: $isOverSpeed")
    println("'$word1' '$word2' dan oldin keladimi: $isAlphabetical")
}
```

## Tushuntirish va Mantiq:
Kotlinda taqqoslash operatorlari nafaqat sonlar uchun, balki 'Comparable' interfeysini implementatsiya qilgan har qanday obyekt (jumladan String) uchun ham ishlaydi. Satrlar leksikografik (alfabit bo'yicha) taqqoslanadi.

## Ishlash natijasi:
```text
Tezlik oshdimi: true
'Olma' 'Banan' dan oldin keladimi: false
```


# 33-Topshiriq: Ko'p satrli String ichida dollar belgisini chiqarish
## Topshiriq sharti:
Moliyaviy shablonda valyuta belgisi ($) va o'zgaruvchilarni to'g'ri kombinatsiya qiling.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val price = 49.99
    val plan = "Premium"
    
    val message = """
        Tarif: $plan
        Oylik to'lov: ${'$'}$price
        Yillik to'lov: ${'$'}${price * 12}
    """.trimIndent()
    
    println(message)
}
```

## Tushuntirish va Mantiq:
Kotlinda string template ichida dollar belgisini to'g'ridan-to'g'ri chop etish uchun '${'$'}' ifodasi eng ishonchli va xatosiz usul hisoblanadi. Bu ayniqsa raw string (""") ichida qulaydir.

## Ishlash natijasi:
```text
Tarif: Premium
Oylik to'lov: $49.99
Yillik to'lov: $599.88
```


# 34-Topshiriq: Sonlarning chegaraviy qiymatlari (Overflow va Underflow)
## Topshiriq sharti:
Int tipining maksimal qiymatiga 1 qo'shilganda nima yuz berishini tekshiring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    var maxInt = Int.MAX_VALUE
    println("Int MAX: $maxInt")
    
    maxInt += 1 // Overflow (to'lib toshish)
    println("MAX + 1: $maxInt")
    
    var minInt = Int.MIN_VALUE
    minInt -= 1 // Underflow
    println("MIN - 1: $minInt")
}
```

## Tushuntirish va Mantiq:
Standart arifmetikada butun son chegaradan oshib ketganda xatolik (exception) tashlanmaydi, balki ikkilik sanoq doirasida aylanib (wrap-around) manfiy qutbga o'tib ketadi. Katta moliyaviy hisoblarda bu jiddiy xato keltirib chiqarishi mumkin, shuning uchun Long yoki BigInteger ishlatiladi.

## Ishlash natijasi:
```text
Int MAX: 2147483647
MAX + 1: -2147483648
MIN - 1: 2147483647
```


# 35-Topshiriq: Katta aniqlikdagi hisob-kitoblar: BigDecimal
## Topshiriq sharti:
Moliyaviy valyuta hisob-kitoblarida suzuvchi nuqta noaniqligini yo'qotish uchun BigDecimal dan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
import java.math.BigDecimal

fun main() {
    val doubleSum = 0.1 + 0.2
    println("Double bilan: $doubleSum") // 0.30000000000000004
    
    val bigDecimal1 = BigDecimal("0.1")
    val bigDecimal2 = BigDecimal("0.2")
    val preciseSum = bigDecimal1 + bigDecimal2
    
    println("BigDecimal bilan: $preciseSum") // 0.3
}
```

## Tushuntirish va Mantiq:
Double va Float sonlar IEEE 754 ikkilik suzuvchi nuqta formati sababli ba'zi o'nlik kasrlarni noaniq saqlaydi. Bank va savdo tizimlarida mutlaq aniqlik uchun 'BigDecimal' qo'llaniladi. Kotlinda BigDecimal uchun '+' va '*' operatorlari haddan tashqari yuklangan (overloaded).

## Ishlash natijasi:
```text
Double bilan: 0.30000000000000004
BigDecimal bilan: 0.3
```


# 36-Topshiriq: Tipni aniqlash: 'is' operatori va Type Checking
## Topshiriq sharti:
Berilgan noma'lum o'zgaruvchi qaysi ma'lumot turiga tegishli ekanligini 'is' operatori orqali aniqlang.

## Yechim (Kotlin kodi):
```kotlin
fun identifyType(item: Any): String {
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
}
```

## Tushuntirish va Mantiq:
'is' operatori o'zgaruvchining ma'lum bir sinf yoki interfeysga tegishli ekanligini tekshiradi (Java dagi 'instanceof'). Kotlinda bu tekshiruvdan so'ng kompilyator o'zgaruvchini avtomatik ravishda o'sha turga o'tkazadi (Smart Cast).

## Ishlash natijasi:
```text
Matn turi, uzunligi: 5
Butun son: 8, kvadrati: 64
Mantiqiy qiymat: true
Kasr son: 15.75
```


# 37-Topshiriq: Xavfsiz va xavfli tip konvertatsiyasi: 'as' vs 'as?'
## Topshiriq sharti:
Obyektni boshqa turga o'tkazishda 'ClassCastException' oldini olish uchun xavfsiz 'as?' operatorini qo'llang.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val obj: Any = "Kotlin tili"
    
    // Xavfsiz cast:
    val str: String? = obj as? String
    val number: Int? = obj as? Int // Natija null bo'ladi, xato tashlamaydi
    
    println("Matnga aylantirish: $str")
    println("Songa aylantirish: $number")
}
```

## Tushuntirish va Mantiq:
'as' operatori xavfli hisoblanadi: agar obyekt ko'rsatilgan turga mos kelmasa, 'ClassCastException' yuz beradi. 'as?' esa xavfsiz (safe cast) bo'lib, muvaffaqiyatsiz bo'lsa xato tashlamasdan 'null' qaytaradi.

## Ishlash natijasi:
```text
Matnga aylantirish: Kotlin tili
Songa aylantirish: null
```


# 38-Topshiriq: Massivlar bilan dastlabki tanishuv: arrayOf va IntArray
## Topshiriq sharti:
Kotlinda umumiy massiv (Array<T>) va primitiv massiv (IntArray) yaratib, ularning elementlarini chop eting.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val names: Array<String> = arrayOf("Ali", "Vali", "G'ani")
    val numbers: IntArray = intArrayOf(10, 20, 30, 40)
    
    println("Ismlar soni: ${names.size}")
    println("Birinchi ism: ${names[0]}")
    println("Sonlar yig'indisi: ${numbers.sum()}")
}
```

## Tushuntirish va Mantiq:
Kotlinda 'Array<T>' Java dagi 'T[]' ga to'g'ri keladi va obyektlar massividir. 'IntArray', 'ByteArray', 'DoubleArray' kabi maxsus turlar esa Java primitiv massivlariga (int[], byte[]) kompilyatsiya bo'ladi va ortiqcha obyekt yaratmasdan xotirani tejaydi.

## Ishlash natijasi:
```text
Ismlar soni: 3
Birinchi ism: Ali
Sonlar yig'indisi: 100
```


# 39-Topshiriq: O'zgarmas qiymatlarni birlashtirish va yangi satr yaratish
## Topshiriq sharti:
Bir nechta o'zgaruvchilarni qo'shib, to'liq profil kartasini hosil qiling.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val firstName = "Ziyoda"
    val lastName = "Toshmatova"
    val age = 22
    val job = "Android Dasturchi"
    
    val profileCard = "Xodim: $firstName $lastName | Yoshi: $age | Kasbi: $job"
    println(profileCard)
}
```

## Tushuntirish va Mantiq:
Kotlinda satrlarni birlashtirishda '+' operatoridan ko'ra satr shablonlari ($) afzalroq. Bu kodni ixchamlashtiradi va ichki 'StringBuilder' orqali yuqori unumdorlik bilan ishlaydi.

## Ishlash natijasi:
```text
Xodim: Ziyoda Toshmatova | Yoshi: 22 | Kasbi: Android Dasturchi
```


# 40-Topshiriq: Sana va vaqt bilan ishlash (Java Time API interop)
## Topshiriq sharti:
Kotlinda zamonaviy Java 'java.time' kutubxonasidan foydalanib joriy vaqtni formatlang.

## Yechim (Kotlin kodi):
```kotlin
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

fun main() {
    val now = LocalDateTime.parse("2026-11-08T15:30:00")
    val formatter = DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm")
    val formattedDate = now.format(formatter)
    
    println("Formatlangan sana: $formattedDate")
}
```

## Tushuntirish va Mantiq:
Kotlin JVM muhitida Java ning barcha standart kutubxonalari bilan 100% integratsiyaga ega. 'java.time.LocalDateTime' va 'DateTimeFormatter' zamonaviy va xavfsiz sana bilan ishlash standartidir.

## Ishlash natijasi:
```text
Formatlangan sana: 08.11.2026 15:30
```


# 41-Topshiriq: Baytlardan Gigabaytga: Disk hajmini hisoblash
## Topshiriq sharti:
Fayl hajmi baytlarda berilgan. Uni kilobayt, megabayt va gigabaytga o'tkazib, 2 ta o'nlik xonagacha formatlab chiqaring.

## Yechim (Kotlin kodi):
```kotlin
fun formatFileSize(bytes: Long): String {
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
}
```

## Tushuntirish va Mantiq:
Katta hajmdagi baytlarni hisoblashda Long va Double turlari kombinatsiyasidan foydalaniladi. Bo'lish amali '1024.0' orqali bajarilganda natija avtomatik ravishda Double ga aylanadi.

## Ishlash natijasi:
```text
500 B
200.00 KB
150.00 MB
5.00 GB
```


# 42-Topshiriq: Harorat konvertori: Selsiy va Farengeyt
## Topshiriq sharti:
Selsiy shkalasidagi haroratni Farengeytga (F = C * 9/5 + 32) va aksincha hisoblovchi dastur yozing.

## Yechim (Kotlin kodi):
```kotlin
fun celsiusToFahrenheit(c: Double): Double = (c * 9.0 / 5.0) + 32.0
fun fahrenheitToCelsius(f: Double): Double = (f - 32.0) * 5.0 / 9.0

fun main() {
    val tempC = 25.0
    val tempF = celsiusToFahrenheit(tempC)
    val convertedBackC = fahrenheitToCelsius(tempF)
    
    println("$tempC°C = $tempF°F")
    println("$tempF°F = $convertedBackC°C")
}
```

## Tushuntirish va Mantiq:
Arifmetik amallarda aniqlikni saqlash uchun '9.0 / 5.0' deb yoziladi. Agar '9 / 5' deb yozilsa, butun sonli bo'lish sodir bo'lib natija 1 ga teng bo'lib qoladi va xato hisoblanadi.

## Ishlash natijasi:
```text
25.0°C = 77.0°F
77.0°F = 25.0°C
```


# 43-Topshiriq: Valyuta konvertori va yaxlitlash
## Topshiriq sharti:
So'mdan AQSH dollariga va yevroga o'tkazuvchi valyuta kalkulyatorini yarating.

## Yechim (Kotlin kodi):
```kotlin
fun convertCurrency(uzsAmount: Double, rate: Double): Double {
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
}
```

## Tushuntirish va Mantiq:
Valyuta konvertatsiyasida Double turidan foydalanib, natijani 'format()' metodi orqali chiroyli va qulay vizual ko'rinishga keltirish amaliy dasturlashda keng qo'llaniladi.

## Ishlash natijasi:
```text
So'm miqdori: 15,000,000 UZS
AQSH dollari: $1,171.88
Yevro: €1,079.14
```


# 44-Topshiriq: Kompilyatsiya vaqtidagi tekshiruvlar: Type Safety tamoyillari
## Topshiriq sharti:
Kotlinda har xil tiplarni bir-biriga tasodifiy biriktirish kompilyator tomonidan qanday to'xtatilishini tushuntiring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val activeCount: Int = 10
    // val text: String = activeCount // Kompilyatsiya xatosi: Type mismatch
    val text: String = activeCount.toString() // To'g'ri usul
    
    println("Matnga aylangan son: $text")
}
```

## Tushuntirish va Mantiq:
Kotlin kuchli tiplashgan (strongly typed) tildir. Yashirin konvertatsiyalarga yo'l qo'yilmaydi. Har qanday tur o'zgarishi dasturchi irodasi bilan aniq ko'rsatilishi kerak.

## Ishlash natijasi:
```text
Matnga aylangan son: 10
```


# 45-Topshiriq: Bo'sh satrlarni tekshirish: isEmpty() va isBlank() farqi
## Topshiriq sharti:
Matn bo'shligini tekshirishda 'isEmpty' va 'isBlank' farqini misollar orqali ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val str1 = ""
    val str2 = "   "
    val str3 = "Kotlin"
    
    println("str1: isEmpty = ${str1.isEmpty()}, isBlank = ${str1.isBlank()}")
    println("str2: isEmpty = ${str2.isEmpty()}, isBlank = ${str2.isBlank()}")
    println("str3: isEmpty = ${str3.isEmpty()}, isBlank = ${str3.isBlank()}")
}
```

## Tushuntirish va Mantiq:
'isEmpty()' faqat satr uzunligi aniq 0 bo'lgandagina true qaytaradi. 'isBlank()' esa satr bo'sh bo'lsa yoki faqatgina probel, tab, yangi qator kabi ko'rinmas bo'shliqlardan iborat bo'lsa ham true qaytaradi. Forma validatsiyasida 'isBlank()' ko'proq ishlatiladi.

## Ishlash natijasi:
```text
str1: isEmpty = true, isBlank = true
str2: isEmpty = false, isBlank = true
str3: isEmpty = false, isBlank = false
```


# 46-Topshiriq: Vaqt oraliqlarini hisoblash: Sekundlarni Soat:Minut:Sekund ga o'tkazish
## Topshiriq sharti:
Jami berilgan sekundlarni (masalan, video davomiyligi) 'HH:mm:ss' formatiga keltiruvchi algoritm yozing.

## Yechim (Kotlin kodi):
```kotlin
fun formatDuration(totalSeconds: Int): String {
    val hours = totalSeconds / 3600
    val minutes = (totalSeconds % 3600) / 60
    val seconds = totalSeconds % 60
    
    return String.format("%02d:%02d:%02d", hours, minutes, seconds)
}

fun main() {
    println(formatDuration(45))
    println(formatDuration(3675))
    println(formatDuration(7322))
}
```

## Tushuntirish va Mantiq:
Butun sonli bo'lish (/) va modul (%) operatorlari vaqt oraliqlarini ajratishda asosiy vosita hisoblanadi. '%02d' format belgisi agar son 1 xonali bo'lsa oldiga 0 qo'shib beradi.

## Ishlash natijasi:
```text
00:00:45
01:01:15
02:02:02
```


# 47-Topshiriq: BMI (Tana massasi indeksi) hisoblagich dasturi
## Topshiriq sharti:
Vazn (kg) va bo'y (metr) asosida BMI (BMI = vazn / bo'y^2) ko'rsatkichini hisoblang va xulosa chiqaring.

## Yechim (Kotlin kodi):
```kotlin
fun calculateBMI(weightKg: Double, heightM: Double): Pair<Double, String> {
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
}
```

## Tushuntirish va Mantiq:
Funksiyadan birdaniga 2 ta qiymat qaytarish uchun 'Pair' va destrukturizatsiya '(bmi, status)' sintaksisi qo'llanildi. Bu kodni toza va tushunarli qiladi.

## Ishlash natijasi:
```text
BMI indeksi: 22.9
Holat: Normal vazn
```


# 48-Topshiriq: Bank depozit hisob-kitobi: Murakkab foiz (Compound Interest)
## Topshiriq sharti:
Boshlang'ich summa, yillik foiz va yillar soni asosida murakkab foiz bilan yakuniy summani hisoblang: A = P * (1 + r)^n.

## Yechim (Kotlin kodi):
```kotlin
import kotlin.math.pow

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
}
```

## Tushuntirish va Mantiq:
Murakkab foiz formulasi moliya sohasida klassik hisoblanadi. Kotlinda '.pow()' funksiyasi 'kotlin.math' to'plamidan chaqiriladi va Double parametrlar bilan ishlaydi.

## Ishlash natijasi:
```text
Boshlang'ich depozit: 10,000,000 UZS
3 yildan keyin jami: 17,715,610 UZS
Sof daromad: 7,715,610 UZS
```


# 49-Topshiriq: Matnlarni tekshirish: Palindromlikni aniqlash
## Topshiriq sharti:
Berilgan so'z yoki iboraning chapdan ham, o'ngdan ham bir xil o'qilishini (palindrom) tekshiruvchi dastur tuzing.

## Yechim (Kotlin kodi):
```kotlin
fun isPalindrome(text: String): Boolean {
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
}
```

## Tushuntirish va Mantiq:
'filter { it.isLetterOrDigit() }' yordamida tinish belgilari va bo'shliqlar chiqarib tashlanadi. '.reversed()' metodi satrni teskarisiga aylantiradi. '==' bilan ularning bir xilligi taqqoslanadi.

## Ishlash natijasi:
```text
'Kiyik' palindrommi: true
'Aziza' palindrommi: true
'Dasturchi' palindrommi: false
'A man, a plan, a canal: Panama' palindrommi: true
```


# 50-Topshiriq: Umumiy jamlama: Foydalanuvchi ma'lumotlari hisoboti
## Topshiriq sharti:
Turli ma'lumot turlari (String, Int, Double, Boolean) va formatlash imkoniyatlarini birlashtirib, to'liq hisobot kartasini shakllantiring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val developerName = "Sardor Aliyev"
    val completedProjects = 14
    val hourlyRate = 35.50
    val totalHoursWorked = 160.0
    val isVerified = true
    
    val grossSalary = hourlyRate * totalHoursWorked
    val taxRate = 0.12
    val netSalary = grossSalary * (1 - taxRate)
    
    val report = """
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
    """.trimIndent()
    
    println(report)
}
```

## Tushuntirish va Mantiq:
Ushbu yakuniy topshiriqda 'val' o'zgaruvchilari, 'Double', 'Int', 'Boolean', 'String' turlari, arifmetik amallar, shartli matn interpolatsiyasi 'if' ifodasi hamda raw string formatlash imkoniyatlari uyg'unlashtirildi.

## Ishlash natijasi:
```text
==================================================
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
==================================================
```

