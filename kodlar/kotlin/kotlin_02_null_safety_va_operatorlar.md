# 51-Topshiriq: Null xavfsizligi asoslari: Non-nullable va Nullable turlar
## Topshiriq sharti:
Kotlinda o'zgaruvchiga null qiymat berishga urinishda kompilyatsiya xatosi yuzaga kelishini va '?' belgisi bilan nullable turni to'g'ri e'lon qilishni namoyish eting.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val nonNullString: String = "Kotlin"
    // val invalid: String = null // Kompilyatsiya xatosi: Null can not be a value of a non-null type String
    
    val nullableString: String? = null
    val validNullable: String? = "Toshkent"
    
    println("Non-null qiymat: $nonNullString")
    println("Nullable (null): $nullableString")
    println("Nullable (mavjud): $validNullable")
}
```

## Tushuntirish va Mantiq:
Kotlinda ma'lumotlar turlari sukut bo'yicha null qiymat qabul qilmaydi (non-nullable). Agar o'zgaruvchida null saqlanishi kerak bo'lsa, tur nomidan keyin aniq so'roq belgisi '?' qo'yiladi (masalan, 'String?'). Bu orqali Kotlin 'NullPointerException' xatoligini kompilyatsiya bosqichidayoq bartaraf etadi.

## Ishlash natijasi:
```text
Non-null qiymat: Kotlin
Nullable (null): null
Nullable (mavjud): Toshkent
```


# 52-Topshiriq: Xavfsiz chaqiruv operatori: Safe Call (?.)
## Topshiriq sharti:
Nullable satr uzunligini dastur qulamasdan (crash bo'lmasdan) xavfsiz olish uchun '?.' operatoridan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
fun printLength(text: String?) {
    val length: Int? = text?.length
    println("Matn: '$text' -> Uzunligi: $length")
}

fun main() {
    printLength("Salom")
    printLength(null)
}
```

## Tushuntirish va Mantiq:
Safe call operatori '?.' chap tomondagi obyekt null emasligini tekshiradi: agar obyekt null bo'lmasa, uning xususiyatini yoki metodini chaqiradi; agar obyekt null bo'lsa, xatolik tashlamasdan butun ifoda natijasi sifatida 'null' qaytaradi. Shu sababli 'text?.length' natijasining turi 'Int?' bo'ladi.

## Ishlash natijasi:
```text
Matn: 'Salom' -> Uzunligi: 5
Matn: 'null' -> Uzunligi: null
```


# 53-Topshiriq: Zanjirli xavfsiz chaqiruvlar (Chained Safe Calls)
## Topshiriq sharti:
Ichma-ich joylashgan obyektlar zanjirida (Foydalanuvchi -> Manzil -> Shahar -> Nomi) null xavfsizligini ta'minlang.

## Yechim (Kotlin kodi):
```kotlin
class City(val name: String)
class Address(val city: City?)
class User(val id: Int, val address: Address?)

fun main() {
    val user1 = User(1, Address(City("Samarqand")))
    val user2 = User(2, Address(null))
    val user3 = User(3, null)
    
    println("User 1 shahar: ${user1.address?.city?.name}")
    println("User 2 shahar: ${user2.address?.city?.name}")
    println("User 3 shahar: ${user3.address?.city?.name}")
}
```

## Tushuntirish va Mantiq:
Zanjirli xavfsiz chaqiruvlarda ('user?.address?.city?.name') zanjirning istalgan bo'g'inida null uchrasa, butun ifoda to'xtaydi va darhol 'null' qaytadi. Bu Java dagi ko'p sonli 'if (obj != null && obj.getX() != null)' tekshiruvlarini bir qator toza kodga aylantiradi.

## Ishlash natijasi:
```text
User 1 shahar: Samarqand
User 2 shahar: null
User 3 shahar: null
```


# 54-Topshiriq: Elvis operatori (?:) bilan zaxira qiymat berish
## Topshiriq sharti:
Nullable o'zgaruvchi null bo'lganda standart (default) qiymatni qaytarish uchun Elvis '?:' operatoridan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
fun getUserDisplayName(username: String?): String {
    return username ?: "Mehmon (Anonim)"
}

fun main() {
    println(getUserDisplayName("anvar_99"))
    println(getUserDisplayName(null))
}
```

## Tushuntirish va Mantiq:
Elvis operatori '?:' (nomi mashhur qo'shiqchi Elvis Preslining soch turmagiga o'xshashligi uchun berilgan) chap tarafdagi qiymat null bo'lmasa uni o'zini, agar null bo'lsa o'ng tarafdagi qiymatni qaytaradi. Natija har doim non-nullable 'String' bo'ladi.

## Ishlash natijasi:
```text
anvar_99
Mehmon (Anonim)
```


# 55-Topshiriq: Elvis operatori bilan funksiyadan erta chiqish (Early Return)
## Topshiriq sharti:
Funksiyaga uzatilgan majburiy parametr null bo'lsa, Elvis operatori yordamida funksiyani darhol to'xtating.

## Yechim (Kotlin kodi):
```kotlin
fun processOrder(orderId: String?, amount: Double) {
    val id = orderId ?: run {
        println("Xatolik: Buyurtma ID ko'rsatilmagan! Jarayon to'xtatildi.")
        return
    }
    
    println("Buyurtma qabul qilindi: ID=$id, Summa=$$amount")
}

fun main() {
    processOrder("ORD-5541", 120.0)
    processOrder(null, 50.0)
}
```

## Tushuntirish va Mantiq:
Kotlinda 'return' ifoda (expression) hisoblanganligi sababli uni Elvis operatorining o'ng tomonida 'orderId ?: return' ko'rinishida yozish mumkin. Bu 'Guard Clause' andozasini nihoyatda ixcham amalga oshirishga yordam beradi.

## Ishlash natijasi:
```text
Buyurtma qabul qilindi: ID=ORD-5541, Summa=$120.0
Xatolik: Buyurtma ID ko'rsatilmagan! Jarayon to'xtatildi.
```


# 56-Topshiriq: Elvis operatori bilan istisno tashlash (throw expression)
## Topshiriq sharti:
Majburiy konfiguratsiya parametri mavjud bo'lmaganda darhol aniq istisno (exception) tashlash uchun '?: throw' sintaksisini qo'llang.

## Yechim (Kotlin kodi):
```kotlin
fun getApiBaseUrl(configUrl: String?): String {
    return configUrl ?: throw IllegalArgumentException("Konfiguratsiyada API manzili topilmadi!")
}

fun main() {
    val validUrl = getApiBaseUrl("https://api.example.uz/v1")
    println("API manzili: $validUrl")
    
    try {
        getApiBaseUrl(null)
    } catch (e: IllegalArgumentException) {
        println("Ushlangan istisno: ${e.message}")
    }
}
```

## Tushuntirish va Mantiq:
Kotlinda 'throw' ham ifoda (Nothing turiga ega) bo'lgani sababli '?: throw ...' sintaksisi qonuniy hisoblanadi. Agar qiymat null bo'lsa, darhol istisno otiladi, aks holda o'zgaruvchi non-nullable sifatida qabul qilinadi.

## Ishlash natijasi:
```text
API manzili: https://api.example.uz/v1
Ushlangan istisno: Konfiguratsiyada API manzili topilmadi!
```


# 57-Topshiriq: Not-null assertion operatori: '!!'
## Topshiriq sharti:
O'zgaruvchining null emasligiga mutlaq ishonch bo'lganda '!!' operatoridan foydalanish va null holatda nima yuz berishini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val text: String? = "Muhim xabar"
    val guaranteedText: String = text!! // Xavfsiz, chunki null emas
    println("Matn: $guaranteedText")
    
    val dangerousNull: String? = null
    try {
        val boom: String = dangerousNull!! // NullPointerException tashlaydi
    } catch (e: NullPointerException) {
        println("Kutilgan NPE yuz berdi: ${e::class.simpleName}")
    }
}
```

## Tushuntirish va Mantiq:
'!!' operatori har qanday nullable turni (T?) majburiy ravishda non-nullable (T) turiga o'tkazadi. Agar qiymat null bo'lsa, darhol 'NullPointerException' tashlanadi. Professional amaliyotda bu operatordan qochish va o'rniga '?.' yoki '?:' ishlatish tavsiya etiladi.

## Ishlash natijasi:
```text
Matn: Muhim xabar
Kutilgan NPE yuz berdi: NullPointerException
```


# 58-Topshiriq: Smart Casts: Null tekshiruvidan keyin avtomatik tur o'zgarishi
## Topshiriq sharti:
Oddiy 'if (text != null)' shartidan so'ng Kotlin kompilyatori o'zgaruvchini avtomatik ravishda non-null turiga o'tkazishini namoyish qiling.

## Yechim (Kotlin kodi):
```kotlin
fun printUpperCase(text: String?) {
    if (text != null) {
        // Bu blok ichida text avtomatik ravishda 'String' turiga aylanadi (Smart Cast)
        // Hech qanday text?. yoki text!! kerak emas
        println("Katta harflar: ${text.uppercase()}")
    } else {
        println("Matn mavjud emas (null)")
    }
}

fun main() {
    printUpperCase("alisher navoiy")
    printUpperCase(null)
}
```

## Tushuntirish va Mantiq:
Kotlining aqlli kompilyatori (K2) boshqaruv oqimini (control flow) tahlil qiladi. 'if (text != null)' bloki ichida 'text' o'zgaruvchisining null bo'lishi imkonsiz ekanini tushunadi va dasturchi qo'shimcha amallar bajarmasdan to'g'ridan-to'g'ri 'text.uppercase()' metodini chaqirishga ruxsat beradi.

## Ishlash natijasi:
```text
Katta harflar: ALISHER NAVOIY
Matn mavjud emas (null)
```


# 59-Topshiriq: Val vs Var o'zgaruvchilarda Smart Cast cheklovlari
## Topshiriq sharti:
'var' o'zgaruvchilarda boshqa oqim yoki metod o'zgartirishi mumkinligi sababli Smart Cast nima uchun ishlamasligini va yechimini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
class ProfileManager {
    var bio: String? = "Android muhandisi"

    fun displayBio() {
        // var ustida to'g'ridan-to'g'ri smart cast ishlamasligi mumkin:
        // if (bio != null) { println(bio.length) } -> Smart cast impossible if bio is mutable
        
        // Yechim: mahalliy 'val' ga nusxalash
        val localBio = bio
        if (localBio != null) {
            println("Bio uzunligi: ${localBio.length} belgi")
        }
    }
}

fun main() {
    val manager = ProfileManager()
    manager.displayBio()
}
```

## Tushuntirish va Mantiq:
Klass xususiyati bo'lgan 'var' o'zgaruvchilar ustida Kotlin Smart Cast qila olmaydi, chunki tekshiruv va foydalanish oralig'ida boshqa oqim (thread) uni 'null' qilib qo'yishi mumkin. Buni hal qilish uchun qiymat mahalliy o'zgarmas 'val' o'zgaruvchiga olinadi yoki 'let' funksiyasi qo'llaniladi.

## Ishlash natijasi:
```text
Bio uzunligi: 17 belgi
```


# 60-Topshiriq: Safe call va let funksiyasi kombinatsiyasi: ?.let { ... }
## Topshiriq sharti:
Obyekt faqat null bo'lmagandagina bir guruh amallarni bajarish uchun eng mashhur Kotlin idiomasi bo'lgan '?.let' ni qo'llang.

## Yechim (Kotlin kodi):
```kotlin
fun sendNotification(email: String?) {
    email?.let { validEmail ->
        println("Xabarnoma yuborildi: $validEmail")
        println("Email server tekshirildi.")
    } ?: println("Email manzili ko'rsatilmagan, xabarnoma bekor qilindi.")
}

fun main() {
    sendNotification("javohir@company.uz")
    sendNotification(null)
}
```

## Tushuntirish va Mantiq:
'?.let' idiomasi Kotlinda eng ko'p ishlatiladigan null-safe andozalardan biridir. Agar obyekt null bo'lmasa, let bloki bajariladi va ichida qiymat 'it' (yoki nomlangan o'zgaruvchi) sifatida non-nullable bo'ladi. Elvis operatori bilan qo'shilganda to'liq 'if-else' o'rnini bosadi.

## Ishlash natijasi:
```text
Xabarnoma yuborildi: javohir@company.uz
Email server tekshirildi.
Email manzili ko'rsatilmagan, xabarnoma bekor qilindi.
```


# 61-Topshiriq: Xavfsiz tip konvertatsiyasi: 'as?' operatori
## Topshiriq sharti:
Har qanday obyektni (Any) kerakli turga xavfsiz o'tkazing va mos kelmasa 'null' qabul qiling.

## Yechim (Kotlin kodi):
```kotlin
fun processNumericData(input: Any) {
    val number: Int? = input as? Int
    if (number != null) {
        println("Muvaffaqiyatli Int: ${number * 10}")
    } else {
        println("Ogohlantirish: '$input' Int tipiga mos kelmadi!")
    }
}

fun main() {
    processNumericData(45)
    processNumericData("Yuz")
    processNumericData(true)
}
```

## Tushuntirish va Mantiq:
'as?' operatori (safe cast) agar obyekt ko'rsatilgan turga mansub bo'lsa uni o'sha turga aylantiradi, aks holda hech qanday 'ClassCastException' tashlamasdan 'null' qaytaradi.

## Ishlash natijasi:
```text
Muvaffaqiyatli Int: 450
Ogohlantirish: 'Yuz' Int tipiga mos kelmadi!
Ogohlantirish: 'true' Int tipiga mos kelmadi!
```


# 62-Topshiriq: Kolleksiyalardan null qiymatlarni tozalash: filterNotNull()
## Topshiriq sharti:
Tarkibida null elementlar bo'lgan ro'yxatdan faqat toza, null bo'lmagan qiymatlarni ajratib oling.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val mixedList: List<String?> = listOf("Toshkent", null, "Samarqand", null, "Buxoro", "Xiva")
    
    val nonNullList: List<String> = mixedList.filterNotNull()
    
    println("Asl ro'yxat hajmi: ${mixedList.size}")
    println("Tozalangan ro'yxat: $nonNullList (hajmi: ${nonNullList.size})")
}
```

## Tushuntirish va Mantiq:
'filterNotNull()' funksiyasi 'List<T?>' turidagi ro'yxatni qabul qilib, undagi barcha null qiymatlarni tashlab yuboradi va natijada sof 'List<T>' (non-nullable elementlar) qaytaradi. Bu Kotlin kolleksiyalar kutubxonasining muhim imkoniyatidir.

## Ishlash natijasi:
```text
Asl ro'yxat hajmi: 6
Tozalangan ro'yxat: [Toshkent, Samarqand, Buxoro, Xiva] (hajmi: 4)
```


# 63-Topshiriq: Nullable ro'yxat va ro'yxatdagi nullable elementlar farqi
## Topshiriq sharti:
'List<String?>', 'List<String>?' va 'List<String?>?' turlari orasidagi farqlarni amalda ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    // 1. Ro'yxat o'zi mavjud, lekin elementlari null bo'lishi mumkin:
    val list1: List<String?> = listOf("A", null, "B")
    
    // 2. Ro'yxatning o'zi null bo'lishi mumkin, lekin ichidagi elementlar har doim non-null:
    val list2: List<String>? = null
    
    // 3. Ham ro'yxatning o'zi, ham uning elementlari null bo'lishi mumkin:
    val list3: List<String?>? = null
    
    println("List1 elementlari: $list1")
    println("List2 o'lchami: ${list2?.size ?: 0}")
    println("List3 nullmi: ${list3 == null}")
}
```

## Tushuntirish va Mantiq:
Kotlinda so'roq belgisi '?' qayerga qo'yilishiga qarab ma'no tubdan o'zgaradi: 'List<T?>' ro'yxatning o'zi null emasligini bildiradi; 'List<T>?' ro'yxatning o'zi bo'lmasligi (null) mumkinligini bildiradi; 'List<T?>?' esa ikkala darajada ham null bo'lishi mumkinligini ifodalaydi.

## Ishlash natijasi:
```text
List1 elementlari: [A, null, B]
List2 o'lchami: 0
List3 nullmi: true
```


# 64-Topshiriq: Shartli tekshiruvlar bilan requireNotNull() funksiyasi
## Topshiriq sharti:
Argumentning null emasligini talab qiluvchi va xato bo'lsa 'IllegalArgumentException' tashlovchi 'requireNotNull' funksiyasidan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
fun registerUser(name: String?, nationalId: String?) {
    val validId = requireNotNull(nationalId) { "Ro'yxatdan o'tish uchun pasport/ID raqami talab qilinadi!" }
    val validName = requireNotNull(name) { "Foydalanuvchi ismi kiritilishi shart!" }
    
    println("Foydalanuvchi ro'yxatga olindi: $validName, ID: $validId")
}

fun main() {
    registerUser("Rustam", "AA1234567")
    try {
        registerUser("Kamola", null)
    } catch (e: IllegalArgumentException) {
        println("Xatolik ushlandi: ${e.message}")
    }
}
```

## Tushuntirish va Mantiq:
'requireNotNull(value) { lazyMessage }' standart kutubxona funksiyasi bo'lib, argument null bo'lsa xabar bilan 'IllegalArgumentException' tashlaydi. Agar null bo'lmasa, qiymatni avtomatik ravishda non-null turiga o'tkazib (Smart cast) qaytaradi.

## Ishlash natijasi:
```text
Foydalanuvchi ro'yxatga olindi: Rustam, ID: AA1234567
Xatolik ushlandi: Ro'yxatdan o'tish uchun pasport/ID raqami talab qilinadi!
```


# 65-Topshiriq: Tizim holatini tekshirish: checkNotNull() funksiyasi
## Topshiriq sharti:
Obyektning ichki holati to'g'riligini tekshirish uchun 'checkNotNull' dan foydalaning va uning 'requireNotNull' dan farqini tushuntiring.

## Yechim (Kotlin kodi):
```kotlin
class DatabaseConnection {
    private var sessionToken: String? = null

    fun connect() {
        sessionToken = "SESSION_TOKEN_98765"
    }

    fun executeQuery(sql: String) {
        val token = checkNotNull(sessionToken) { "Baza bilan ulanish o'rnatilmagan! Avval connect() chaqiring." }
        println("Sorov bajarildi: '$sql' [Token: $token]")
    }
}

fun main() {
    val db = DatabaseConnection()
    try {
        db.executeQuery("SELECT * FROM users")
    } catch (e: IllegalStateException) {
        println("Holat xatosi: ${e.message}")
    }
    
    db.connect()
    db.executeQuery("SELECT * FROM users")
}
```

## Tushuntirish va Mantiq:
'checkNotNull' funksiyasi argumentlar uchun emas, balki obyektning ichki holati (internal state) uchun ishlatiladi. Agar qiymat null bo'lsa, u 'IllegalStateException' tashlaydi.

## Ishlash natijasi:
```text
Holat xatosi: Baza bilan ulanish o'rnatilmagan! Avval connect() chaqiring.
Sorov bajarildi: 'SELECT * FROM users' [Token: SESSION_TOKEN_98765]
```


# 66-Topshiriq: Kechiktirilgan initsializatsiya: 'lateinit var' bilan ishlash
## Topshiriq sharti:
Klass o'zgaruvchisini darhol emas, keyinroq initsializatsiya qilish uchun 'lateinit' modifikatorini qo'llang.

## Yechim (Kotlin kodi):
```kotlin
class CarEngine {
    lateinit var model: String

    fun setup(modelName: String) {
        model = modelName
    }

    fun start() {
        if (::model.isInitialized) {
            println("Dvigatel ishga tushdi: $model")
        } else {
            println("Dvigatel modeli sozlanmagan!")
        }
    }
}

fun main() {
    val car = CarEngine()
    car.start()
    car.setup("V8 Turbo Twin")
    car.start()
}
```

## Tushuntirish va Mantiq:
'lateinit' faqat 'var' va non-nullable obyekt turlari uchun qo'llaniladi (Int, Double kabi primitivlarda ishlamaydi). U orqali o'zgaruvchini darhol qiymat bermasdan e'lon qilish mumkin. '::property.isInitialized' sintaksisi esa xususiyat initsializatsiya qilinganligini tekshiradi.

## Ishlash natijasi:
```text
Dvigatel modeli sozlanmagan!
Dvigatel ishga tushdi: V8 Turbo Twin
```


# 67-Topshiriq: lateinit xatoligi: UninitializedPropertyAccessException
## Topshiriq sharti:
Initsializatsiya qilinmagan 'lateinit' o'zgaruvchiga murojaat qilinganda qanday aniq xatolik yuz berishini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
class PaymentService {
    lateinit var apiKey: String

    fun process() {
        println("To'lov o'tkazilmoqda... Kalit: $apiKey")
    }
}

fun main() {
    val service = PaymentService()
    try {
        service.process()
    } catch (e: Exception) {
        println("Ushlangan istisno: ${e::class.simpleName}")
        println("Tafsilot: ${e.message}")
    }
}
```

## Tushuntirish va Mantiq:
Agar 'lateinit' o'zgaruvchiga qiymat biriktirilmasdan oldin murojaat qilinsa, Kotlin 'UninitializedPropertyAccessException' tashlaydi. Bu oddiy NPE ga qaraganda xatoning sababini ancha aniqroq tushuntirib beradi.

## Ishlash natijasi:
```text
Ushlangan istisno: UninitializedPropertyAccessException
Tafsilot: lateinit property apiKey has not been initialized
```


# 68-Topshiriq: Tembel yuklash: 'by lazy' delegatsiyasi bilan solishtirish
## Topshiriq sharti:
Qiymat faqat birinchi marta kerak bo'lgandagina hisoblanadigan 'by lazy' xususiyatini yarating.

## Yechim (Kotlin kodi):
```kotlin
class HeavyResourceLoader {
    val configuration: String by lazy {
        println("--> Og'ir konfiguratsiya fayli xotiraga yuklanmoqda...")
        "SERVER_CONFIG_READY"
    }
}

fun main() {
    val loader = HeavyResourceLoader()
    println("Loader obyekti yaratildi. Konfiguratsiya hali yuklanmadi.")
    
    println("Birinchi murojaat: ${loader.configuration}")
    println("Ikkinchi murojaat: ${loader.configuration}")
}
```

## Tushuntirish va Mantiq:
'by lazy' xususiyati faqat 'val' o'zgaruvchilari uchun ishlatiladi. Kod bloki birinchi marta xususiyatga murojaat qilingandagina bajariladi va natija keshlanadi. Keyingi barcha murojaatlarda tayyor keshdagi qiymat qaytadi. Sukut bo'yicha bu amal ko'p oqimli xavfsizdir (thread-safe).

## Ishlash natijasi:
```text
Loader obyekti yaratildi. Konfiguratsiya hali yuklanmadi.
--> Og'ir konfiguratsiya fayli xotiraga yuklanmoqda...
Birinchi murojaat: SERVER_CONFIG_READY
Ikkinchi murojaat: SERVER_CONFIG_READY
```


# 69-Topshiriq: Platform turlari (Platform Types) va Java bilan o'zaro aloqa
## Topshiriq sharti:
Java metodlaridan qaytgan tiplar Kotlinda 'T!' (platform type) sifatida ko'rinishini va undagi potensial null xavflarini tushuntiring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    // Java dagi System.getProperty() agar kalit topilmasa 'null' qaytaradi
    val javaProp = System.getProperty("non_existent_key_xyz") // Turi: String! (platform type)
    
    // Agar dasturchi uning null-safetysiga e'tibor bermay to'g'ridan-to'g'ri String deb olsa:
    val safeProp: String? = javaProp // Tavsiya etiladigan xavfsiz yondashuv
    
    println("Xususiyat qiymati: ${safeProp ?: "Topilmadi (sukut bo'yicha qiymat)"}")
}
```

## Tushuntirish va Mantiq:
Java da null-safety bo'lmaganligi sababli, Java kutubxonalaridan kelgan turlar Kotlinda 'Platform Type' (masalan 'String!') deb ataladi. Kompilyator ularni ham nullable, ham non-nullable sifatida ishlatishga ruxsat beradi, ammo xavfsizlik uchun ularni har doim aniq nullable ('String?') deb qabul qilish tavsiya etiladi.

## Ishlash natijasi:
```text
Xususiyat qiymati: Topilmadi (sukut bo'yicha qiymat)
```


# 70-Topshiriq: Nullable Receiver bilan kengaytma funksiyalar (Extension Functions)
## Topshiriq sharti:
Obyekt null bo'lganda ham xavfsiz chaqirilishi mumkin bo'lgan kengaytma funksiya (extension function) yozing.

## Yechim (Kotlin kodi):
```kotlin
fun String?.orDefault(defaultValue: String): String {
    return this ?: defaultValue
}

fun main() {
    val str1: String? = "Haqiqiy matn"
    val str2: String? = null
    
    // Nuqta orqali to'g'ridan-to'g'ri chaqirish mumkin, chunki receiver 'String?'
    println(str1.orDefault("Standart"))
    println(str2.orDefault("Standart"))
}
```

## Tushuntirish va Mantiq:
Kotlinda kengaytma funksiyalarni nullable tiplar ustiga ham yozish mumkin ('fun String?.method()'). Funksiya ichida 'this' havolasi null bo'lishi mumkin va ichkarida 'this == null' tekshiruvi amalga oshiriladi. Natijada foydalanuvchi '?.' operatorisiz to'g'ridan-to'g'ri chaqira oladi.

## Ishlash natijasi:
```text
Haqiqiy matn
Standart
```


# 71-Topshiriq: isNullOrEmpty() va isNullOrBlank() standart funksiyalari
## Topshiriq sharti:
Matnning null yoki bo'sh ekanligini bir vaqtning o'zida tekshiruvchi standart Kotlin metodlaridan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
fun validateInput(field: String?, name: String) {
    if (field.isNullOrBlank()) {
        println("Ogohlantirish: '$name' maydoni to'ldirilmagan!")
    } else {
        println("Muvaffaqiyatli: '$name' = '$field'")
    }
}

fun main() {
    validateInput("Ali Valiyev", "To'liq ism")
    validateInput("   ", "Manzil")
    validateInput(null, "Telefon raqami")
}
```

## Tushuntirish va Mantiq:
'isNullOrBlank()' kengaytma funksiyasi o'zgaruvchi null bo'lsa yoki faqat bo'shliqlardan iborat bo'lsa true qaytaradi. Eng muhimi, 'if (!field.isNullOrBlank())' shartidan so'ng 'field' avtomatik tarzda 'String' (non-nullable) turiga smart cast bo'ladi.

## Ishlash natijasi:
```text
Muvaffaqiyatli: 'To'liq ism' = 'Ali Valiyev'
Ogohlantirish: 'Manzil' maydoni to'ldirilmagan!
Ogohlantirish: 'Telefon raqami' maydoni to'ldirilmagan!
```


# 72-Topshiriq: takeIf va takeUnless bilan null hosil qilish
## Topshiriq sharti:
Shartga mos kelganda qiymatni saqlab qoluvchi, aks holda null qaytaruvchi 'takeIf' funksiyasini qo'llang.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val age = 17
    val legalAge = age.takeIf { it >= 18 }
    println("Voyaga yetgan yosh: $legalAge") // null
    
    val validAge = 24
    val adultAge = validAge.takeIf { it >= 18 }
    println("Voyaga yetgan yosh: $adultAge") // 24
    
    val score = 85
    val passingScore = score.takeUnless { it < 60 }
    println("O'tish bali: $passingScore")
}
```

## Tushuntirish va Mantiq:
'takeIf' berilgan predikat to'g'ri bo'lsa obyektning o'zini, yolg'on bo'lsa 'null' qaytaradi. 'takeUnless' esa uning teskarisidir. Ular Elvis operatori '?:' bilan birgalikda filtrlash va validatsiya qilishda nihoyatda qulaydir.

## Ishlash natijasi:
```text
Voyaga yetgan yosh: null
Voyaga yetgan yosh: 24
O'tish bali: 85
```


# 73-Topshiriq: Nullable Boolean bilan shartli mantiq
## Topshiriq sharti:
Boolean? (uch holatli mantiq: true, false, null) turidagi ifodani 'if' shartida to'g'ri ishlatish yo'lini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
fun checkAgreement(agreed: Boolean?) {
    // Kotlinda 'if (agreed)' yozib bo'lmaydi, chunki agreed null bo'lishi mumkin
    if (agreed == true) {
        println("Shartlarga to'liq rozi.")
    } else {
        println("Shartlar qabul qilinmagan (rad etilgan yoki belgilanmagan).")
    }
}

fun main() {
    checkAgreement(true)
    checkAgreement(false)
    checkAgreement(null)
}
```

## Tushuntirish va Mantiq:
'Boolean?' tipi uchta qiymatga ega bo'lishi mumkin: true, false yoki null. Shuning uchun 'if (b)' deb to'g'ridan-to'g'ri shartga qo'yib bo'lmaydi. Uni 'if (b == true)' deb yozish orqali null qiymat ham false sifatida xavfsiz qayta ishlanadi.

## Ishlash natijasi:
```text
Shartlarga to'liq rozi.
Shartlar qabul qilinmagan (rad etilgan yoki belgilanmagan).
Shartlar qabul qilinmagan (rad etilgan yoki belgilanmagan).
```


# 74-Topshiriq: Shartli o'zgaruvchi almashtirish: also va let farqlari
## Topshiriq sharti:
Nullable obyekt ustida xavfsiz logging va hisoblashni 'also' hamda 'let' orqali bajaring.

## Yechim (Kotlin kodi):
```kotlin
fun fetchUserAvatar(userId: Int?): String? {
    return userId?.let { id ->
        "https://cdn.example.uz/avatars/$id.png"
    }?.also { url ->
        println("[LOG]: Avatar URL tayyorlandi -> $url")
    }
}

fun main() {
    val url1 = fetchUserAvatar(101)
    val url2 = fetchUserAvatar(null)
    
    println("Natija 1: $url1")
    println("Natija 2: $url2")
}
```

## Tushuntirish va Mantiq:
'let' blokining oxirgi ifodasi natija sifatida qaytadi (transformatsiya qiladi), 'also' esa obyektning o'zini qaytaradi (asosan logging va yordamchi amallar uchun). Har ikkisi ham safe call (?.) bilan null-safe ishlaydi.

## Ishlash natijasi:
```text
[LOG]: Avatar URL tayyorlandi -> https://cdn.example.uz/avatars/101.png
Natija 1: https://cdn.example.uz/avatars/101.png
Natija 2: null
```


# 75-Topshiriq: Map kolleksiyasidan qiymat olish va null boshqaruvi
## Topshiriq sharti:
Lug'atda (Map) kalit topilmaganda 'null' qaytishini va 'getValue' hamda 'getOrDefault' metodlarini solishtiring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val currencyRates = mapOf("USD" to 12800.0, "EUR" to 13900.0)
    
    val rubRate1 = currencyRates["RUB"] // Turi: Double? (null bo'ladi)
    val rubRate2 = currencyRates.getOrDefault("RUB", 130.0) // Non-nullable
    
    println("RUB rate (odatiy get): $rubRate1")
    println("RUB rate (getOrDefault): $rubRate2")
    
    val usdRate = currencyRates.getValue("USD") // Topilmasa NoSuchElementException
    println("USD rate (getValue): $usdRate")
}
```

## Tushuntirish va Mantiq:
Kotlinda 'map[key]' sintaksisi kalit topilmasa 'null' qaytaradi. 'getOrDefault' xavfsiz zaxira qiymat beradi, 'getValue' esa agar kalit aniq bo'lishi shart bo'lsa ishlatilib, kalit yo'q bo'lsa istisno tashlaydi.

## Ishlash natijasi:
```text
RUB rate (odatiy get): null
RUB rate (getOrDefault): 130.0
USD rate (getValue): 12800.0
```


# 76-Topshiriq: Xavfsiz indekslash: getOrNull() massivlar va ro'yxatlarda
## Topshiriq sharti:
Massiv chegarasidan tashqariga chiqish ('IndexOutOfBoundsException') xatosini 'getOrNull' orqali bartaraf qiling.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val topScores = listOf(98, 95, 89)
    
    // Xavfsiz indekslash:
    val first = topScores.getOrNull(0)
    val tenth = topScores.getOrNull(10) // null qaytaradi
    
    println("1-o'rin bali: $first")
    println("11-o'rin bali: ${tenth ?: "Mavjud emas"}")
}
```

## Tushuntirish va Mantiq:
'getOrNull(index)' funksiyasi agar berilgan indeks massiv yoki ro'yxat chegarasida bo'lsa elementni, aks holda dasturni buzmasdan 'null' qaytaradi. Bu foydalanuvchi kiritgan indekslar bilan ishlashda qulaydir.

## Ishlash natijasi:
```text
1-o'rin bali: 98
11-o'rin bali: Mavjud emas
```


# 77-Topshiriq: Kolleksiya boshlang'ich va oxirgi elementlarini xavfsiz olish
## Topshiriq sharti:
'firstOrNull()' va 'lastOrNull()' funksiyalarining bo'sh ro'yxatlarda xavfsiz ishlashini tekshiring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val emptyList = emptyList<String>()
    
    // emptyList.first() chaqirilsa NoSuchElementException tashlanadi
    val first = emptyList.firstOrNull()
    val last = emptyList.lastOrNull()
    
    println("Bo'sh ro'yxat birinchi elementi: $first")
    println("Bo'sh ro'yxat oxirgi elementi: $last")
    
    val numbers = listOf(10, 25, 40, 55, 60)
    val firstEven = numbers.firstOrNull { it % 2 == 0 }
    val firstLarge = numbers.firstOrNull { it > 100 }
    
    println("Birinchi juft son: $firstEven")
    println("100 dan katta son: $firstLarge")
}
```

## Tushuntirish va Mantiq:
'firstOrNull()' predikatga mos element topilmasa yoki ro'yxat butunlay bo'sh bo'lsa 'null' qaytaradi. Bu 'NoSuchElementException' xatoliklarini to'liq oldini oladi.

## Ishlash natijasi:
```text
Bo'sh ro'yxat birinchi elementi: null
Bo'sh ro'yxat oxirgi elementi: null
Birinchi juft son: 10
100 dan katta son: null
```


# 78-Topshiriq: Merosxo'rlikda (Inheritance) Null-safety qoidalari
## Topshiriq sharti:
Superklass metodining non-nullable qaytish turini subklassda nullable qilib o'zgartirish mumkin emasligini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
open class BaseService {
    open fun getName(): String {
        return "Asosiy Servis"
    }
}

class ExtendedService : BaseService() {
    // override fun getName(): String? -> Kompilyatsiya xatosi!
    // Return type is 'String?', which is not a subtype of overridden 'String'
    override fun getName(): String {
        return "Kengaytirilgan Servis"
    }
}

fun main() {
    val service: BaseService = ExtendedService()
    println("Servis nomi: ${service.getName()}")
}
```

## Tushuntirish va Mantiq:
Kotlinda merosxo'rlikda kovariantlik va tiplar xavfsizligi qat'iy saqlanadi: agar ota sinf metodi non-nullable (String) qaytarsa, bola sinf uni nullable (String?) qilib o'zgartira olmaydi, chunki ota sinf kontraktiga ko'ra natija hech qachon null bo'lmasligi shart.

## Ishlash natijasi:
```text
Servis nomi: Kengaytirilgan Servis
```


# 79-Topshiriq: Nullable Enum bilan when ifodasining to'liqligi (Exhaustive When)
## Topshiriq sharti:
Nullable Enum parametrini 'when' bilan tahlil qilishda null holati hisobga olinmasa nima bo'lishini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
enum class OrderStatus {
    PENDING, SHIPPED, DELIVERED
}

fun getStatusMessage(status: OrderStatus?): String {
    return when (status) {
        OrderStatus.PENDING -> "Buyurtma kutilmoqda"
        OrderStatus.SHIPPED -> "Buyurtma jo'natildi"
        OrderStatus.DELIVERED -> "Buyurtma yetkazib berildi"
        null -> "Buyurtma holati noma'lum"
    }
}

fun main() {
    println(getStatusMessage(OrderStatus.SHIPPED))
    println(getStatusMessage(null))
}
```

## Tushuntirish va Mantiq:
Kotlinda 'when' ifodasi barcha ehtimoliy holatlarni qamrab olishi kerak (exhaustive). Agar parametr 'OrderStatus?' (nullable) bo'lsa, enum qiymatlaridan tashqari 'null' shoxobchasi ham yozilishi shart, aks holda 'else' talab qilinadi.

## Ishlash natijasi:
```text
Buyurtma jo'natildi
Buyurtma holati noma'lum
```


# 80-Topshiriq: Xavfsiz matn konvertatsiyasi: toString() ning null xavfsizligi
## Topshiriq sharti:
Kotlinda 'null.toString()' funksiyasi 'null' satrini qaytarishini va String? ustida ishlashini tekshiring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val nullName: String? = null
    val nullNumber: Int? = null
    
    // Kotlinda Any?.toString() kengaytmasi mavjud
    println("nullName satr ko'rinishi: '${nullName.toString()}'")
    println("nullNumber satr ko'rinishi: '${nullNumber.toString()}'")
    println("Tenglik: ${nullName.toString() == "null"}")
}
```

## Tushuntirish va Mantiq:
Kotlinda 'toString()' kengaytma funksiyasi 'Any?' (nullable receiver) ustida aniqlangan. Shuning uchun obyekt null bo'lsa ham 'obj.toString()' chaqirilganda NPE otilmaydi, balki "null" satri qaytadi.

## Ishlash natijasi:
```text
nullName satr ko'rinishi: 'null'
nullNumber satr ko'rinishi: 'null'
Tenglik: true
```


# 81-Topshiriq: Nullable xususiyatlar bilan Data Class
## Topshiriq sharti:
Ixtiyoriy (optional) maydonlarga ega data class yarating va 'copy()' metodi bilan null qiymatlarni boshqaring.

## Yechim (Kotlin kodi):
```kotlin
data class UserProfile(
    val id: Long,
    val name: String,
    val phone: String? = null,
    val bio: String? = null
)

fun main() {
    val user1 = UserProfile(id = 1L, name = "Jamshid")
    val user2 = user1.copy(phone = "+998901234567", bio = "Dasturchi va kitobxon")
    
    println("User 1: $user1")
    println("User 2: $user2")
}
```

## Tushuntirish va Mantiq:
Data sinflarda nullable xususiyatlarga '= null' standart qiymatini berish orqali ixtiyoriy parametrlar yaratiladi. 'copy()' metodi esa mavjud obyektning nusxasini olib, kerakli maydonlarini (jumladan null bo'lganlarini) yangilashga imkon beradi.

## Ishlash natijasi:
```text
User 1: UserProfile(id=1, name=Jamshid, phone=null, bio=null)
User 2: UserProfile(id=1, name=Jamshid, phone=+998901234567, bio=Dasturchi va kitobxon)
```


# 82-Topshiriq: Nullable qiymatlar bilan solishtirish: compareValues()
## Topshiriq sharti:
Ikki nullable qiymatni (masalan, ikkita sanani yoki sonni) xavfsiz solishtirish dasturini tuzing.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val val1: Int? = 10
    val val2: Int? = 20
    val val3: Int? = null
    
    // null qiymat har doim non-null qiymatdan kichik hisoblanadi
    println("10 vs 20: ${compareValues(val1, val2)}")
    println("10 vs null: ${compareValues(val1, val3)}")
    println("null vs null: ${compareValues(val3, val3)}")
}
```

## Tushuntirish va Mantiq:
'compareValues(a, b)' standart kutubxona funksiyasi ikkita nullable 'Comparable' obyektni solishtiradi. Sukut bo'yicha 'null' qiymat har qanday non-null qiymatdan kichik deb baholanadi. Bu saralash (sorting) algoritmlarida juda foydalidir.

## Ishlash natijasi:
```text
10 vs 20: -1
10 vs null: 1
null vs null: 0
```


# 83-Topshiriq: Kolleksiyalarda null qiymatlar bo'yicha saralash: nullsFirst() va nullsLast()
## Topshiriq sharti:
Nullable elementlar yoki maydonlar bo'yicha ro'yxatni saralashda null larni boshiga yoki oxiriga joylashtiring.

## Yechim (Kotlin kodi):
```kotlin
data class Employee(val name: String, val bonus: Double?)

fun main() {
    val employees = listOf(
        Employee("Farrux", 500.0),
        Employee("Nodir", null),
        Employee("Zafar", 1200.0),
        Employee("Malika", null)
    )
    
    val sortedNullsLast = employees.sortedWith(compareBy(nullsLast()) { it.bonus })
    println("Null lar oxirida saralash:")
    sortedNullsLast.forEach { println("${it.name}: ${it.bonus}") }
}
```

## Tushuntirish va Mantiq:
'nullsLast()' va 'nullsFirst()' komparator modifikatorlari bo'lib, null qiymatlarning saralashdagi o'rnini aniq belgilash imkonini beradi. Bu SQL dagi 'NULLS LAST / NULLS FIRST' bilan bir xil ishlaydi.

## Ishlash natijasi:
```text
Null lar oxirida saralash:
Farrux: 500.0
Zafar: 1200.0
Nodir: null
Malika: null
```


# 84-Topshiriq: Null tekshiruvida mantiqiy teskari shart: 'is not' va Smart Cast
## Topshiriq sharti:
'!is' yoki '!= null' shartlarida funksiyadan erta chiqilganda quyidagi kod qanday smart cast bo'lishini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
fun processPayload(payload: Any?) {
    if (payload !is String) {
        println("Xato: Yuborilgan ma'lumot matn emas!")
        return
    }
    
    // Bu yerga yetib kelganda payload avtomatik ravishda 'String' (va non-null)
    println("Payload uzunligi: ${payload.length}")
    println("Payload matni: ${payload.trim()}")
}

fun main() {
    processPayload("  Maxfiy ma'lumot  ")
    processPayload(12345)
    processPayload(null)
}
```

## Tushuntirish va Mantiq:
Kotlinda shartli qaytish (guard clause) dan so'ng kompilyator o'zgaruvchining qolgan doiradagi tipini aniq biladi. Agar 'payload !is String' holatida return qilinsa, pastdagi barcha kodda 'payload' to'laqonli 'String' sifatida ishlatilaveradi.

## Ishlash natijasi:
```text
Payload uzunligi: 19
Payload matni: Maxfiy ma'lumot
Xato: Yuborilgan ma'lumot matn emas!
Xato: Yuborilgan ma'lumot matn emas!
```


# 85-Topshiriq: Xavfsiz hisoblash: Nullable sonlar ustida arifmetika
## Topshiriq sharti:
Nullable Double qiymatlar bilan soliq va umumiy summani xavfsiz hisoblovchi kalkulyator tuzing.

## Yechim (Kotlin kodi):
```kotlin
fun calculateTotal(price: Double?, discount: Double?, taxPercent: Double?): Double {
    val actualPrice = price ?: 0.0
    val actualDiscount = discount ?: 0.0
    val actualTaxPercent = taxPercent ?: 12.0
    
    val discountedPrice = (actualPrice - actualDiscount).coerceAtLeast(0.0)
    val totalWithTax = discountedPrice * (1 + actualTaxPercent / 100.0)
    
    return totalWithTax
}

fun main() {
    println("To'liq berilgan: " + calculateTotal(100.0, 10.0, 12.0))
    println("Chegirmasiz: " + calculateTotal(200.0, null, 15.0))
    println("Barcha parametrlar null: " + calculateTotal(null, null, null))
}
```

## Tushuntirish va Mantiq:
Nullable sonlar bilan ishlaganda hisob-kitobdan oldin '?:' orqali standart xavfsiz qiymatlar beriladi. '.coerceAtLeast(0.0)' esa chegirma narxdan oshib ketganda manfiy son hosil bo'lishining oldini oladi.

## Ishlash natijasi:
```text
To'liq berilgan: 100.8
Chegirmasiz: 230.0
Barcha parametrlar null: 0.0
```


# 86-Topshiriq: Shartli chaqiruv: Kolleksiyadagi ob'ekt xususiyatiga xavfsiz murojaat
## Topshiriq sharti:
Ro'yxatning n-elementining ichki xususiyatini dastur qulamasdan olishni tashkil qiling.

## Yechim (Kotlin kodi):
```kotlin
class Customer(val name: String, val email: String?)

fun main() {
    val customers = listOf(
        Customer("Aziz", "aziz@mail.uz"),
        Customer("Bobur", null)
    )
    
    val emailFirst = customers.getOrNull(0)?.email?.uppercase()
    val emailSecond = customers.getOrNull(1)?.email?.uppercase()
    val emailThird = customers.getOrNull(2)?.email?.uppercase()
    
    println("1-mijoz email: $emailFirst")
    println("2-mijoz email: $emailSecond")
    println("3-mijoz email: $emailThird")
}
```

## Tushuntirish va Mantiq:
Zanjirli safe call operatori '?.' bir vaqtning o'zida ro'yxat chegarasidan chiqib ketish (getOrNull) va obyektning ichki maydonining null bo'lishi (email) xavflarini to'liq zararsizlantiradi.

## Ishlash natijasi:
```text
1-mijoz email: AZIZ@MAIL.UZ
2-mijoz email: null
3-mijoz email: null
```


# 87-Topshiriq: Null xavfsizligi va Generiklar (Generic Nullability)
## Topshiriq sharti:
Generik tip parametri sukut bo'yicha nullable ('Any?') ekanligini va uni non-null ('T : Any') qilish yo'lini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
// T sukut bo'yicha Any? (nullable)
class NullableContainer<T>(val value: T)

// T aniq Any ga cheklangan (non-nullable)
class NonNullContainer<T : Any>(val value: T)

fun main() {
    val c1 = NullableContainer<String?>("Salom")
    val c2 = NullableContainer<String?>(null) // Ruxsat etilgan
    
    val c3 = NonNullContainer<String>("Dunyo")
    // val c4 = NonNullContainer<String?>(null) // Kompilyatsiya xatosi: Type argument is not within its bounds
    
    println("Container 1: ${c1.value}")
    println("Container 2: ${c2.value}")
    println("Container 3: ${c3.value}")
}
```

## Tushuntirish va Mantiq:
Kotlinda generik <T> yozilganda, u aslida <T : Any?> deb qabul qilinadi, ya'ni T null bo'lishi mumkin. Agar faqat null bo'lmagan tiplarni qabul qilish talab etilsa, <T : Any> deb yuqori chegara (upper bound) berilishi shart.

## Ishlash natijasi:
```text
Container 1: Salom
Container 2: null
Container 3: Dunyo
```


# 88-Topshiriq: Kotlin Result turi va getOrNull()
## Topshiriq sharti:
Xatolik yuz berishi mumkin bo'lgan operatsiyani 'runCatching' orqali o'rab, natijani xavfsiz nullable ko'rinishda oling.

## Yechim (Kotlin kodi):
```kotlin
fun parsePort(portStr: String): Int? {
    val result = runCatching {
        val port = portStr.toInt()
        if (port !in 1..65535) throw IllegalArgumentException("Port chegaradan tashqarida")
        port
    }
    return result.getOrNull()
}

fun main() {
    println("8080 port: ${parsePort("8080")}")
    println("Noto'g'ri matn: ${parsePort("abc")}")
    println("Chegaradan tashqari: ${parsePort("70000")}")
}
```

## Tushuntirish va Mantiq:
'runCatching' bloki ichida tashlangan har qanday istisnoni ushlaydi va 'Result<T>' obyektini hosil qiladi. 'result.getOrNull()' esa operatsiya muvaffaqiyatli bo'lsa qiymatni, agar xato bo'lsa 'null' qaytaradi.

## Ishlash natijasi:
```text
8080 port: 8080
Noto'g'ri matn: null
Chegaradan tashqari: null
```


# 89-Topshiriq: Xususiyat delegatsiyasi: Delegates.notNull()
## Topshiriq sharti:
Primitiv tiplar (Int, Double) uchun 'lateinit' o'rniga 'Delegates.notNull()' dan foydalanishni namoyish qiling.

## Yechim (Kotlin kodi):
```kotlin
import kotlin.properties.Delegates

class GameSession {
    // Int primitiv bo'lgani uchun 'lateinit' ishlatib bo'lmaydi
    var maxPlayers: Int by Delegates.notNull()
}

fun main() {
    val session = GameSession()
    
    try {
        println(session.maxPlayers) // Hali qiymat berilmagan
    } catch (e: IllegalStateException) {
        println("Ushlangan xato: ${e.message}")
    }
    
    session.maxPlayers = 4
    println("O'yinchilar soni sozlandi: ${session.maxPlayers}")
}
```

## Tushuntirish va Mantiq:
Kotlinda 'lateinit var' primitiv turlarda (Int, Long, Boolean va h.k.) ishlamaydi. Primitiv tiplarni kechiktirib initsializatsiya qilish uchun 'Delegates.notNull<T>()' xususiyat delegatsiyasi xizmat qiladi.

## Ishlash natijasi:
```text
Ushlangan xato: Property maxPlayers should be initialized before get.
O'yinchilar soni sozlandi: 4
```


# 90-Topshiriq: Null xavfsizligi va Rekursiya: Daraxt tuzilmasini aylanib chiqish
## Topshiriq sharti:
Har bir tuguni (Node) chap va o'ng nullable bolalarga ega bo'lgan ikkilik daraxt yig'indisini xavfsiz hisoblang.

## Yechim (Kotlin kodi):
```kotlin
class TreeNode(val value: Int, val left: TreeNode? = null, val right: TreeNode? = null)

fun sumTree(node: TreeNode?): Int {
    if (node == null) return 0
    return node.value + sumTree(node.left) + sumTree(node.right)
}

fun main() {
    // Daraxt:
    //      10
    //     /      //    5    15
    //        /
    //       12
    val root = TreeNode(10, TreeNode(5), TreeNode(15, TreeNode(12), null))
    println("Daraxt elementlari yig'indisi: ${sumTree(root)}")
}
```

## Tushuntirish va Mantiq:
Rekursiv ma'lumotlar tuzilmalarida (daraxtlar, bog'langan ro'yxatlar) tugunlarning yo'qligi tabiiy ravishda 'null' bilan ifodalanadi. Baza holati 'if (node == null) return 0' orqali cheksiz rekursiya va NPE oldi olinadi.

## Ishlash natijasi:
```text
Daraxt elementlari yig'indisi: 42
```


# 91-Topshiriq: Kolleksiya assotsiatsiyasi va Null qiymatlarni filtrlash
## Topshiriq sharti:
Obyektlar ro'yxatidan ma'lum bir nullable xususiyat bo'yicha Map hosil qiling va null larni chetlab o'ting.

## Yechim (Kotlin kodi):
```kotlin
class Student(val id: Int, val passport: String?)

fun main() {
    val students = listOf(
        Student(1, "AB123"),
        Student(2, null),
        Student(3, "AC456")
    )
    
    // Faqat passport mavjud bo'lgan talabalarning Map ini tuzish
    val passportMap: Map<Int, String> = students.mapNotNull { student ->
        student.passport?.let { student.id to it }
    }.toMap()
    
    println("Passport xaritasi: $passportMap")
}
```

## Tushuntirish va Mantiq:
'mapNotNull' funksiyasi berilgan lambda natijasi null bo'lmagan elementlarnigina yangi ro'yxatga oladi. Natijada xaritada (Map) faqat yaroqli kalit-qiymat juftliklari saqlanadi.

## Ishlash natijasi:
```text
Passport xaritasi: {1=AB123, 3=AC456}
```


# 92-Topshiriq: Shartli qiymat berish: if-else ifodasi null ga qarshi
## Topshiriq sharti:
if-else ifodasini to'g'ridan-to'g'ri o'zgaruvchiga biriktirib, null ehtimolini to'liq bartaraf qiling.

## Yechim (Kotlin kodi):
```kotlin
fun formatStatus(isOnline: Boolean?, lastSeenMinutes: Int?): String {
    val statusText = if (isOnline == true) {
        "Tarmoqda (Online)"
    } else if (lastSeenMinutes != null) {
        "$lastSeenMinutes daqiqa oldin ko'rilgan"
    } else {
        "Yaqinda ko'rilmagan"
    }
    
    return statusText
}

fun main() {
    println(formatStatus(true, null))
    println(formatStatus(false, 15))
    println(formatStatus(null, null))
}
```

## Tushuntirish va Mantiq:
Kotlinda 'if' bayonot (statement) emas, balki ifoda (expression) dir, ya'ni u qiymat qaytaradi. Uning har bir tarmog'i yakuniy qiymatni taqdim etishi sababli natijaviy o'zgaruvchi 'statusText' 100% non-nullable 'String' bo'lishi kafolatlanadi.

## Ishlash natijasi:
```text
Tarmoqda (Online)
15 daqiqa oldin ko'rilgan
Yaqinda ko'rilmagan
```


# 93-Topshiriq: Nullable stringlarni birlashtirish: joinToString va null transformatsiya
## Topshiriq sharti:
Elementlar orasida null mavjud bo'lgan ro'yxatni chiroyli matnga aylantiring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val items: List<String?> = listOf("Non", null, "Sut", null, "Choy")
    
    val resultWithDefault = items.joinToString(separator = ", ") { it ?: "Mavjud emas" }
    val resultFiltered = items.filterNotNull().joinToString(separator = ", ")
    
    println("Standart bilan: $resultWithDefault")
    println("Faqat mavjudlari: $resultFiltered")
}
```

## Tushuntirish va Mantiq:
'joinToString' funksiyasiga lambda transformator uzatish mumkin. Unda har bir element null bo'lsa nima ko'rinishi ('it ?: "Mavjud emas"') belgilanadi yoki avval 'filterNotNull()' qilib tozalanadi.

## Ishlash natijasi:
```text
Standart bilan: Non, Mavjud emas, Sut, Mavjud emas, Choy
Faqat mavjudlari: Non, Sut, Choy
```


# 94-Topshiriq: Null xavfsizligi va Interfeys implementatsiyasi
## Topshiriq sharti:
Interfeysda nullable deb e'lon qilingan xususiyatni sinf ichida non-nullable qilib qat'iylashtirish.

## Yechim (Kotlin kodi):
```kotlin
interface NamedEntity {
    val name: String?
}

class ConcreteProduct(override val name: String, val price: Double) : NamedEntity

fun main() {
    val product = ConcreteProduct("Smartfon", 800.0)
    println("Mahsulot nomi: ${product.name}") // Smartfon (non-nullable String)
    println("Nomi uzunligi: ${product.name.length}") // To'g'ridan-to'g'ri chaqirish mumkin
}
```

## Tushuntirish va Mantiq:
Kotlinda subklass yoki interfeysni amalga oshiruvchi sinf ota tipdagi nullable xususiyatni ('String?') o'zida non-nullable ('String') qilib toraytirishi (narrowing) mumkin. Bu Liskov almashinish tamoyiliga (LSP) to'liq mos keladi.

## Ishlash natijasi:
```text
Mahsulot nomi: Smartfon
Nomi uzunligi: 8
```


# 95-Topshiriq: Shartli bajarish: let va run zanjirlari
## Topshiriq sharti:
Obyekt ustida bir nechta null-safe bosqichli amallarni bajarish va har bir bosqich natijasini uzatish.

## Yechim (Kotlin kodi):
```kotlin
class OrderRequest(val rawPhone: String?)

fun cleanPhoneNumber(request: OrderRequest?): String? {
    return request?.rawPhone
        ?.trim()
        ?.takeIf { it.isNotEmpty() }
        ?.replace(" ", "")
        ?.replace("-", "")
}

fun main() {
    println("Tozalangan: " + cleanPhoneNumber(OrderRequest("+998 90 123-45-67")))
    println("Bo'sh matn: " + cleanPhoneNumber(OrderRequest("   ")))
    println("Obyekt null: " + cleanPhoneNumber(null))
}
```

## Tushuntirish va Mantiq:
Funksional metodlar zanjiri ('trim', 'takeIf', 'replace') har bir qadamda '?.' orqali tekshirilib, agar biror qadamda qiymat yaroqsiz bo'lib qolsa (masalan takeIf null qaytarsa), keyingi barcha amallar xavfsiz to'xtatiladi.

## Ishlash natijasi:
```text
Tozalangan: +998901234567
Bo'sh matn: null
Obyekt null: null
```


# 96-Topshiriq: Amaliy API javobini tahlil qilish (JSON DTO Parsing)
## Topshiriq sharti:
Tashqi serverdan kelgan to'liq bo'lmagan foydalanuvchi ma'lumotlarini domendagi toza modelga o'tkazish.

## Yechim (Kotlin kodi):
```kotlin
// API dan kelgan DTO model
data class UserDto(
    val id: Long?,
    val full_name: String?,
    val is_active: Boolean?
)

// Ilova ichidagi xavfsiz Domen model
data class DomainUser(
    val id: Long,
    val name: String,
    val isActive: Boolean
)

fun mapToDomain(dto: UserDto): DomainUser {
    return DomainUser(
        id = requireNotNull(dto.id) { "Foydalanuvchi ID si bo'sh bo'lishi mumkin emas!" },
        name = dto.full_name?.takeIf { it.isNotBlank() } ?: "Noma'lum foydalanuvchi",
        isActive = dto.is_active ?: false
    )
}

fun main() {
    val validDto = UserDto(1001L, "Otabek Qodirov", true)
    val partialDto = UserDto(1002L, null, null)
    
    println("Domen 1: ${mapToDomain(validDto)}")
    println("Domen 2: ${mapToDomain(partialDto)}")
}
```

## Tushuntirish va Mantiq:
Haqiqiy Android va backend dasturlashda tashqi API modellari (DTO) hamma vaqt nullable maydonlar bilan e'lon qilinadi. Domen qatlamiga o'tishda esa barcha maydonlar 'requireNotNull' yoki Elvis operatori orqali qat'iy non-nullable holatga keltiriladi.

## Ishlash natijasi:
```text
Domen 1: DomainUser(id=1001, name=Otabek Qodirov, isActive=true)
Domen 2: DomainUser(id=1002, name=Noma'lum foydalanuvchi, isActive=false)
```


# 97-Topshiriq: Kompilyatsiya vaqtida xatoliklarni oldini olish: Type contracts
## Topshiriq sharti:
Maxsus tekshiruvchi yordamchi funksiya orqali smart cast kontraktini hosil qilish.

## Yechim (Kotlin kodi):
```kotlin
fun validateSession(token: String?): Boolean {
    return !token.isNullOrBlank() && token.startsWith("BEARER_")
}

fun main() {
    val userToken: String? = "BEARER_sec_99182"
    
    if (validateSession(userToken)) {
        // userToken tekshiruvdan o'tdi, endi undan xavfsiz foydalanamiz
        val actualToken = userToken!! // Yoki safe call
        println("Avtorizatsiya muvaffaqiyatli: $actualToken")
    } else {
        println("Avtorizatsiya rad etildi.")
    }
}
```

## Tushuntirish va Mantiq:
Yordamchi mantiqiy funksiyalar yordamida parametrlar validatsiya qilinadi. Kotlin standart kutubxonasi 'contracts' orqali bunday holatlarni kompilyator darajasida yanada aqlli bog'lay oladi.

## Ishlash natijasi:
```text
Avtorizatsiya muvaffaqiyatli: BEARER_sec_99182
```


# 98-Topshiriq: Null xavfsiz kesh mexanizmi (Cache implementation)
## Topshiriq sharti:
Kalit bo'yicha qiymatni keshdan qidiruvchi, bo'lmasa yuklab keshga yozuvchi xavfsiz xizmat yarating.

## Yechim (Kotlin kodi):
```kotlin
class SimpleCache {
    private val memory = mutableMapOf<String, String>()

    fun getOrFetch(key: String, fetcher: () -> String): String {
        val cached = memory[key]
        if (cached != null) {
            println("[KESH]: '$key' xotiradan olindi.")
            return cached
        }
        
        println("[TARMOQ]: '$key' yangidan yuklanmoqda...")
        val fresh = fetcher()
        memory[key] = fresh
        return fresh
    }
}

fun main() {
    val cache = SimpleCache()
    
    val val1 = cache.getOrFetch("kurs_usd") { "12800" }
    val val2 = cache.getOrFetch("kurs_usd") { "12850" }
    
    println("Natija 1: $val1")
    println("Natija 2: $val2")
}
```

## Tushuntirish va Mantiq:
Kesh algoritmlarida xotirada qiymat bor-yo'qligi 'memory[key] != null' orqali tekshiriladi. Smart cast tufayli 'cached' qiymat darhol qaytariladi, null bo'lsa yangi qiymat olinadi.

## Ishlash natijasi:
```text
[TARMOQ]: 'kurs_usd' yangidan yuklanmoqda...
[KESH]: 'kurs_usd' xotiradan olindi.
Natija 1: 12800
Natija 2: 12800
```


# 99-Topshiriq: Shartli qiymat zanjirlari bilan murakkab konfiguratsiya
## Topshiriq sharti:
Konfiguratsiya qiymatini bir nechta manbalardan (Buyruqlar satri -> Muhit o'zgaruvchilari -> Standart fayl) navbatma-navbat izlash.

## Yechim (Kotlin kodi):
```kotlin
fun resolveConfig(cliParam: String?, envVar: String?, defaultVal: String): String {
    return cliParam ?: envVar ?: defaultVal
}

fun main() {
    val config1 = resolveConfig("PORT=9000", "PORT=8080", "PORT=3000")
    val config2 = resolveConfig(null, "PORT=8080", "PORT=3000")
    val config3 = resolveConfig(null, null, "PORT=3000")
    
    println("Konfiguratsiya 1: $config1")
    println("Konfiguratsiya 2: $config2")
    println("Konfiguratsiya 3: $config3")
}
```

## Tushuntirish va Mantiq:
Elvis operatorlari zanjiri ('a ?: b ?: c') 'Coalescing' deb ataladi. U birinchi null bo'lmagan qiymatni topguncha chapdan o'ngga qarab ketma-ket baholanadi. Oxirgi qiymat 'defaultVal' non-nullable bo'lgani sababli butun funksiya natijasi ham kafolatlangan non-nullable bo'ladi.

## Ishlash natijasi:
```text
Konfiguratsiya 1: PORT=9000
Konfiguratsiya 2: PORT=8080
Konfiguratsiya 3: PORT=3000
```


# 100-Topshiriq: Null xavfsizligi bo'yicha to'liq amaliy xulosa
## Topshiriq sharti:
Barcha o'rganilgan operatorlarni (?., ?:, as?, filterNotNull, requireNotNull) bitta yaxlit mijoz hisobini shakllantirish jarayonida jamlang.

## Yechim (Kotlin kodi):
```kotlin
class OrderItem(val name: String, val price: Double?)
class CustomerOrder(val orderId: String?, val items: List<OrderItem?>?)

fun generateInvoice(order: CustomerOrder?): String {
    val safeOrder = requireNotNull(order) { "Buyurtma mavjud emas!" }
    val id = safeOrder.orderId ?: "NO_ID"
    
    val validItems = safeOrder.items?.filterNotNull() ?: emptyList()
    
    var totalPrice = 0.0
    val itemsSummary = StringBuilder()
    
    for (item in validItems) {
        val price = item.price ?: 0.0
        totalPrice += price
        itemsSummary.append(" - ${item.name}: $$price
")
    }
    
    return """
        INVOYS: $id
        -----------------------------
        Mahsulotlar:
        $itemsSummary-----------------------------
        Jami to'lov: $$totalPrice
    """.trimIndent()
}

fun main() {
    val sampleOrder = CustomerOrder(
        orderId = "INV-7788",
        items = listOf(
            OrderItem("Klaviatura", 45.0),
            null,
            OrderItem("Sichqoncha", 25.0),
            OrderItem("Kovrik", null)
        )
    )
    
    println(generateInvoice(sampleOrder))
}
```

## Tushuntirish va Mantiq:
Ushbu yakuniy topshiriqda talab qilingan 'requireNotNull', '?:', '?.' va 'filterNotNull()' mexanizmlari real dunyo buyurtma fakturasini hisoblashda birlashtirildi. Dastur har qanday null vaziyatida ham barqaror va xatosiz ishlaydi.

## Ishlash natijasi:
```text
INVOYS: INV-7788
-----------------------------
Mahsulotlar:
 - Klaviatura: $45.0
 - Sichqoncha: $25.0
 - Kovrik: $0.0
-----------------------------
Jami to'lov: $70.0
```

