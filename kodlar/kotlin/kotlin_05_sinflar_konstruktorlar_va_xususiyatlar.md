# 201-Topshiriq: Asosiy konstruktor (Primary Constructor) va xususiyatlar
## Topshiriq sharti:
Sinf e'lonining o'zida 'val' va 'var' parametrlari bilan asosiy konstruktor yarating va obyekt hosil qiling.

## Yechim (Kotlin kodi):
```kotlin
class Laptop(val brand: String, val ramGb: Int, var price: Double)

fun main() {
    val myLaptop = Laptop("Dell", 16, 1200.0)
    println("Noutbuk brendi: ${myLaptop.brand}")
    println("Operativ xotira: ${myLaptop.ramGb} GB")
    println("Boshlang'ich narx: $$${myLaptop.price}")
    
    myLaptop.price = 1100.0 // var o'zgaradi
    println("Yangi narx: $$${myLaptop.price}")
}
```

## Tushuntirish va Mantiq:
Kotlinda asosiy konstruktor (primary constructor) to'g'ridan-to'g'ri sinf nomidan keyin e'lon qilinadi. Parametrlar oldiga 'val' yoki 'var' qo'yilsa, Kotlin avtomatik ravishda sinf xususiyatlarini (fields/properties) va ularning getter/setter metodlarini generatsiya qiladi.

## Ishlash natijasi:
```text
Noutbuk brendi: Dell
Operativ xotira: 16 GB
Boshlang'ich narx: $1200.0
Yangi narx: $1100.0
```


# 202-Topshiriq: Initsializatsiya bloki: 'init' bloki va parametrlarni tekshirish
## Topshiriq sharti:
Asosiy konstruktordan kelgan ma'lumotlarni tekshirish (validatsiya) uchun 'init' blokidan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
class BankAccount(val accountNumber: String, initialBalance: Double) {
    var balance: Double = initialBalance
        private set // Balansni tashqaridan to'g'ridan-to'g'ri o'zgartirib bo'lmaydi

    init {
        require(accountNumber.isNotBlank()) { "Hisob raqami bo'sh bo'lishi mumkin emas!" }
        require(initialBalance >= 0) { "Boshlang'ich balans manfiy bo'lishi mumkin emas!" }
        println("[TIZIM]: Hisob ochildi: $accountNumber, Boshlang'ich balans: $$initialBalance")
    }
}

fun main() {
    val acc = BankAccount("UZB-778899", 500.0)
    println("Hisob balansi: $${acc.balance}")
}
```

## Tushuntirish va Mantiq:
Kotlinda asosiy konstruktor o'z ichida kod bajara olmaydi. Initsializatsiya paytida biror tekshiruv yoki mantiq bajarish kerak bo'lsa, 'init' bloklari ishlatiladi. 'init' bloki obyekt xotirada yaratilishi bilanoq darhol ishga tushadi.

## Ishlash natijasi:
```text
[TIZIM]: Hisob ochildi: UZB-778899, Boshlang'ich balans: $500.0
Hisob balansi: $500.0
```


# 203-Topshiriq: Bir nechta 'init' bloklarining ketma-ketligi
## Topshiriq sharti:
Sinf ichida bir nechta 'init' bloklari va xususiyatlar e'lon qilinganda ularning yuqoridan pastga bajarilish tartibini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
class Order(val orderId: Int) {
    val firstProp = "Birinchi xususiyat".also { println(it) }

    init {
        println("1-init bloki: OrderId = $orderId")
    }

    val secondProp = "Ikkinchi xususiyat".also { println(it) }

    init {
        println("2-init bloki: Barcha xususiyatlar tayyor")
    }
}

fun main() {
    val order = Order(101)
}
```

## Tushuntirish va Mantiq:
Kotlinda 'init' bloklari va xususiyat initsializatorlari sinf tanasida qanday ketma-ketlikda yozilgan bo'lsa, xuddi shu tartibda (yuqoridan pastga qarab) qat'iy bajariladi.

## Ishlash natijasi:
```text
Birinchi xususiyat
1-init bloki: OrderId = 101
Ikkinchi xususiyat
2-init bloki: Barcha xususiyatlar tayyor
```


# 204-Topshiriq: Ikkilamchi konstruktor (Secondary Constructor)
## Topshiriq sharti:
Asosiy konstruktorga qo'shimcha ravishda 'constructor' kalit so'zi bilan ikkilamchi konstruktor yarating.

## Yechim (Kotlin kodi):
```kotlin
class Student(val name: String, val age: Int) {
    var email: String = ""

    // Ikkilamchi konstruktor asosiy konstruktorga 'this()' orqali murojaat qilishi shart
    constructor(name: String, age: Int, email: String) : this(name, age) {
        this.email = email
        println("Ikkilamchi konstruktor chaqirildi: Email = $email")
    }
}

fun main() {
    val s1 = Student("Alisher", 20)
    val s2 = Student("Nodira", 22, "nodira@edu.uz")
    
    println("Talaba 1: ${s1.name}, yoshi: ${s1.age}")
    println("Talaba 2: ${s2.name}, yoshi: ${s2.age}, email: ${s2.email}")
}
```

## Tushuntirish va Mantiq:
Agar sinfda asosiy (primary) konstruktor mavjud bo'lsa, har bir ikkilamchi (secondary) konstruktor 'this(...)' kalit so'zi orqali bevosita yoki bilvosita asosiy konstruktorga delegatsiya qilishi shart.

## Ishlash natijasi:
```text
Ikkilamchi konstruktor chaqirildi: Email = nodira@edu.uz
Talaba 1: Alisher, yoshi: 20
Talaba 2: Nodira, yoshi: 22, email: nodira@edu.uz
```


# 205-Topshiriq: Faqat ikkilamchi konstruktorga ega bo'lgan sinf
## Topshiriq sharti:
Asosiy konstruktori bo'lmagan, faqat 'constructor' bilan e'lon qilingan sinfni va uning 'super()' chaqiruvini namoyish qiling.

## Yechim (Kotlin kodi):
```kotlin
open class View {
    constructor(context: String) {
        println("View ota sinf konstruktori: $context")
    }
}

class CustomButton : View {
    constructor(context: String) : super(context) {
        println("CustomButton 1-konstruktori")
    }
    
    constructor(context: String, style: Int) : super(context) {
        println("CustomButton 2-konstruktori: Style=$style")
    }
}

fun main() {
    val btn = CustomButton("MainActivity", 42)
}
```

## Tushuntirish va Mantiq:
Android dagi 'View' komponentlarida bo'lgani kabi, agar sinfda primary constructor e'lon qilinmasa, har bir secondary constructor ota sinfning konstruktorini 'super(...)' orqali chaqiradi.

## Ishlash natijasi:
```text
View ota sinf konstruktori: MainActivity
CustomButton 2-konstruktori: Style=42
```


# 206-Topshiriq: Maxsus Getter (Custom Getter) va Hisoblanuvchi xususiyatlar
## Topshiriq sharti:
Xotirada maydon (field) egallamasdan, chaqirilgan paytda hisoblanadigan 'val' xususiyatini yarating.

## Yechim (Kotlin kodi):
```kotlin
class Rectangle(val width: Double, val height: Double) {
    // Hisoblanuvchi xususiyat (Backing field yo'q)
    val area: Double
        get() = width * height

    val isSquare: Boolean
        get() = width == height
}

fun main() {
    val rect = Rectangle(5.0, 8.0)
    println("To'g'ri to'rtburchak: ${rect.width}x${rect.height}")
    println("Yuzasi: ${rect.area}")
    println("Kvadratmi: ${rect.isSquare}")
}
```

## Tushuntirish va Mantiq:
Kotlinda 'val prop: Type get() = expression' sintaksisi orqali xususiyatga maxsus getter biriktiriladi. Bunday xususiyatlar xotirada joy olmaydi, har safar chaqirilganda metod kabi ishlab natija qaytaradi.

## Ishlash natijasi:
```text
To'g'ri to'rtburchak: 5.0x8.0
Yuzasi: 40.0
Kvadratmi: false
```


# 207-Topshiriq: Maxsus Setter va Backing Field ('field' kalit so'zi)
## Topshiriq sharti:
O'zgaruvchiga qiymat biriktirilayotganda manfiy sonlarni tekshiruvchi maxsus setter yozing.

## Yechim (Kotlin kodi):
```kotlin
class Thermometer {
    var celsius: Double = 0.0
        set(value) {
            if (value < -273.15) {
                println("Xatolik: Mutlaq noldan past harorat bo'lishi mumkin emas!")
            } else {
                field = value // field - bu asl xotira yacheykasi
            }
        }
}

fun main() {
    val t = Thermometer()
    t.celsius = 25.0
    println("Harorat: ${t.celsius}°C")
    
    t.celsius = -300.0 // Qabul qilinmaydi
    println("Harorat o'zgarmadi: ${t.celsius}°C")
}
```

## Tushuntirish va Mantiq:
Kotlinda maxsus setter ichida qiymatni saqlash uchun maxsus 'field' identifikatoridan (backing field) foydalaniladi. Agar 'celsius = value' deb yozilsa, setter yana o'zini chaqirib 'StackOverflowError' yuzaga keladi.

## Ishlash natijasi:
```text
Harorat: 25.0°C
Xatolik: Mutlaq noldan past harorat bo'lishi mumkin emas!
Harorat o'zgarmadi: 25.0°C
```


# 208-Topshiriq: Getter va Setter ko'rinish doirasi (Visibility)
## Topshiriq sharti:
Tashqaridan faqat o'qiladigan, lekin faqat sinf ichidan o'zgartiriladigan xususiyat yarating ('private set').

## Yechim (Kotlin kodi):
```kotlin
class Counter {
    var count: Int = 0
        private set // Getter public, lekin setter private

    fun increment() {
        count++
    }

    fun reset() {
        count = 0
    }
}

fun main() {
    val counter = Counter()
    counter.increment()
    counter.increment()
    println("Hisoblagich: ${counter.count}")
    
    // counter.count = 10 // Kompilyatsiya xatosi: Cannot assign to 'count': the setter is private
}
```

## Tushuntirish va Mantiq:
'private set' sintaksisi inkapsulyatsiyaning oltin qoidasidir: xususiyat tashqaridan xavfsiz o'qilishi mumkin (read-only), lekin uni o'zgartirish huquqi faqat sinfning o'z metodlariga beriladi.

## Ishlash natijasi:
```text
Hisoblagich: 2
```


# 209-Topshiriq: Backing Property andozasi (Inkapsulyatsiya)
## Topshiriq sharti:
Tashqariga o'zgarmas 'List' taqdim etuvchi, lekin ichkarida 'MutableList' saqlovchi klassik arxitektura andozasini qo'llang.

## Yechim (Kotlin kodi):
```kotlin
class ShoppingCart {
    // Maxfiy o'zgaruvchan ro'yxat:
    private val _items = mutableListOf<String>()

    // Ommaviy o'zgarmas ro'yxat:
    val items: List<String>
        get() = _items

    fun addItem(item: String) {
        _items.add(item)
        println("Qo'shildi: $item")
    }
}

fun main() {
    val cart = ShoppingCart()
    cart.addItem("Non")
    cart.addItem("Sut")
    
    println("Savatdagi mahsulotlar: ${cart.items}")
    // cart.items.add("Qand") // Kompilyatsiya xatosi: List da 'add' yo'q
}
```

## Tushuntirish va Mantiq:
Android ViewModel va zamonaviy arxitekturada '_items' (backing property) private qilib olinadi, tashqariga esa o'zgarmas 'items' interfeysi orqali uzatiladi. Bu tashqi kodning ichki holatni buzishining oldini oladi.

## Ishlash natijasi:
```text
Qo'shildi: Non
Qo'shildi: Sut
Savatdagi mahsulotlar: [Non, Sut]
```


# 210-Topshiriq: Xususiyatlarni kechiktirib yuklash: 'lateinit var'
## Topshiriq sharti:
Dependency Injection va Testlarda xususiyatni keyinchalik initsializatsiya qilish imkoniyatini 'lateinit' orqali namoyish qiling.

## Yechim (Kotlin kodi):
```kotlin
class AnalyticsTracker {
    lateinit var trackerId: String

    fun initialize(id: String) {
        trackerId = id
    }

    fun logEvent(event: String) {
        if (::trackerId.isInitialized) {
            println("[$trackerId] Hodisa yozildi: $event")
        } else {
            println("Xatolik: Tracker hali initsializatsiya qilinmagan!")
        }
    }
}

fun main() {
    val tracker = AnalyticsTracker()
    tracker.logEvent("App_Open")
    
    tracker.initialize("UA-998822")
    tracker.logEvent("Button_Click")
}
```

## Tushuntirish va Mantiq:
'lateinit var' faqat null bo'lmagan obyekt turlari uchun ishlatiladi. Bu konstruktor chaqirilayotgan paytda qiymat mavjud bo'lmagan, lekin keyinchalik aniq biriktiriladigan holatlarda (masalan Android View lar yoki Dagger/Hilt) qo'llaniladi.

## Ishlash natijasi:
```text
Xatolik: Tracker hali initsializatsiya qilinmagan!
[UA-998822] Hodisa yozildi: Button_Click
```


# 211-Topshiriq: Tembel xususiyatlar: 'val ... by lazy'
## Topshiriq sharti:
Og'ir resursni faqat birinchi chaqirilganda yuklash va natijani saqlab qolish uchun 'by lazy' dan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
class DatabaseConfig {
    val connectionString: String by lazy {
        println("--> Og'ir baza konfiguratsiyasi yuklanmoqda...")
        "jdbc:postgresql://localhost:5432/main_db"
    }
}

fun main() {
    val config = DatabaseConfig()
    println("Konfig obyekti mavjud.")
    
    println("1-chaqiruv: ${config.connectionString}")
    println("2-chaqiruv: ${config.connectionString}")
}
```

## Tushuntirish va Mantiq:
'by lazy' xususiyat faqat birinchi marta murojaat qilinganda hisoblanadi. Olingan natija xotirada saqlanadi (keshlanadi) va keyingi barcha murojaatlarda darhol qaytariladi. Bu faqat 'val' bilan ishlaydi.

## Ishlash natijasi:
```text
Konfig obyekti mavjud.
--> Og'ir baza konfiguratsiyasi yuklanmoqda...
1-chaqiruv: jdbc:postgresql://localhost:5432/main_db
2-chaqiruv: jdbc:postgresql://localhost:5432/main_db
```


# 212-Topshiriq: Maxfiy konstruktor (Private Constructor)
## Topshiriq sharti:
Konstruktorga tashqaridan kirishni taqiqlab, faqat fabrika metodi orqali obyekt yaratilishini ta'minlang.

## Yechim (Kotlin kodi):
```kotlin
class SecretVault private constructor(val code: String) {
    companion object {
        fun createVault(masterKey: String): SecretVault? {
            return if (masterKey == "ADMIN_PASS_2026") {
                SecretVault("VAULT_AUTHORIZED")
            } else {
                null
            }
        }
    }
}

fun main() {
    // val v = SecretVault("test") // Kompilyatsiya xatosi: Cannot access '<init>': it is private
    val vault1 = SecretVault.createVault("not_correct")
    val vault2 = SecretVault.createVault("ADMIN_PASS_2026")
    
    println("Noto'g'ri kalit bilan ombor: $vault1")
    println("To'g'ri kalit bilan ombor: ${vault2?.code}")
}
```

## Tushuntirish va Mantiq:
Sinf konstruktorini 'private constructor()' qilib yashirish Factory Pattern va Singleton yaratishda obyektlarning noto'g'ri yoki ruxsatsiz yaratilishini oldini oladi.

## Ishlash natijasi:
```text
Noto'g'ri kalit bilan ombor: null
To'g'ri kalit bilan ombor: VAULT_AUTHORIZED
```


# 213-Topshiriq: Ichki sinflar: 'inner class' vs Statik ichki sinflar
## Topshiriq sharti:
Kotlinda oddiy ichki sinf statik ekanligini, tashqi sinf xususiyatlariga kirish uchun esa 'inner' modifikatori kerakligini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
class OuterClass(val outerName: String) {
    // Statik ichki sinf (sukut bo'yicha):
    class NestedClass {
        fun greet() = "NestedClass salomi (tashqi klassga kirmaydi)"
    }

    // Haqiqiy ichki sinf (tashqi sinf obyektiga bog'langan):
    inner class InnerClass {
        fun greetOuter() = "InnerClass tashqi klass nomini o'qidi: $outerName"
    }
}

fun main() {
    val nested = OuterClass.NestedClass()
    println(nested.greet())
    
    val outer = OuterClass("Toshkent-Bosh-Ofis")
    val inner = outer.InnerClass()
    println(inner.greetOuter())
}
```

## Tushuntirish va Mantiq:
Kotlinda sinf ichida e'lon qilingan klass sukut bo'yicha statikdir (Java dagi 'static class' ga to'g'ri keladi). Agar tashqi sinf xususiyatlariga murojaat qilish kerak bo'lsa, 'inner' kalit so'zi qo'yiladi.

## Ishlash natijasi:
```text
NestedClass salomi (tashqi klassga kirmaydi)
InnerClass tashqi klass nomini o'qidi: Toshkent-Bosh-Ofis
```


# 214-Topshiriq: Modul darajasidagi ko'rinish: 'internal' modifikatori
## Topshiriq sharti:
Faqat bitta kompilyatsiya moduli doirasida ko'rinadigan 'internal' klass va metodlarni tushuntiring.

## Yechim (Kotlin kodi):
```kotlin
internal class InternalService {
    internal fun performInternalTask(): String {
        return "Modul ichidagi maxfiy vazifa bajarildi."
    }
}

fun main() {
    val service = InternalService()
    println(service.performInternalTask())
}
```

## Tushuntirish va Mantiq:
'internal' modifikatori Kotlinga xos bo'lib, Java da uning to'g'ridan-to'g'ri analogi yo'q. U obyekt faqat bir xil modul (masalan bitta Gradle/Maven moduli yoki kutubxona) ichida ko'rinishini kafolatlaydi.

## Ishlash natijasi:
```text
Modul ichidagi maxfiy vazifa bajarildi.
```


# 215-Topshiriq: Konstruktor parametrlariga standart qiymatlar berish
## Topshiriq sharti:
Asosiy konstruktorda standart parametrlar yordamida har xil kombinatsiyalarda obyekt yasash.

## Yechim (Kotlin kodi):
```kotlin
class ServerConfig(
    val host: String = "localhost",
    val port: Int = 8080,
    val isSecure: Boolean = false
)

fun main() {
    val conf1 = ServerConfig()
    val conf2 = ServerConfig("api.production.uz", isSecure = true)
    val conf3 = ServerConfig(port = 9000)
    
    println("Conf 1: ${conf1.host}:${conf1.port} (SSL: ${conf1.isSecure})")
    println("Conf 2: ${conf2.host}:${conf2.port} (SSL: ${conf2.isSecure})")
    println("Conf 3: ${conf3.host}:${conf3.port} (SSL: ${conf3.isSecure})")
}
```

## Tushuntirish va Mantiq:
Asosiy konstruktorda standart argumentlar bo'lsa, Kotlin kompilyatori bir qator qulay chaqiruvlarni ta'minlaydi va Builder patterniga deyarli ehtiyoj qoldirmaydi.

## Ishlash natijasi:
```text
Conf 1: localhost:8080 (SSL: false)
Conf 2: api.production.uz:8080 (SSL: true)
Conf 3: localhost:9000 (SSL: false)
```


# 216-Topshiriq: Xususiyat kuzatuvchisi: Delegates.observable
## Topshiriq sharti:
Xususiyat qiymati o'zgarganda avtomatik xabar beruvchi 'Delegates.observable' xususiyat delegatsiyasidan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
import kotlin.properties.Delegates

class UserSettings {
    var theme: String by Delegates.observable("light") { prop, old, new ->
        println("[SOZLAMA]: '${prop.name}' o'zgardi: '$old' -> '$new'")
    }
}

fun main() {
    val settings = UserSettings()
    println("Boshlang'ich mavzu: ${settings.theme}")
    
    settings.theme = "dark"
    settings.theme = "high-contrast"
}
```

## Tushuntirish va Mantiq:
'Delegates.observable' xususiyatga yangi qiymat biriktirilishi bilanoq maxsus lambdani chaqiradi. Lambda ichida xususiyat nomi, eski qiymat va yangi qiymat taqdim etiladi.

## Ishlash natijasi:
```text
Boshlang'ich mavzu: light
[SOZLAMA]: 'theme' o'zgardi: 'light' -> 'dark'
[SOZLAMA]: 'theme' o'zgardi: 'dark' -> 'high-contrast'
```


# 217-Topshiriq: Shartli o'zgarish: Delegates.vetoable
## Topshiriq sharti:
Agar yangi qiymat ma'lum bir qoidaga mos kelmasa, o'zgarishni bekor qiluvchi 'Delegates.vetoable' dan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
import kotlin.properties.Delegates

class PlayerProfile {
    // Ball faqat oshishi mumkin, kamayishi taqiqlanadi
    var score: Int by Delegates.vetoable(0) { _, old, new ->
        if (new >= old) {
            true // O'zgarish qabul qilindi
        } else {
            println("Rad etildi: Yangi ball ($new) eski balldan ($old) kichik bo'lishi mumkin emas!")
            false // O'zgarish bekor qilindi
        }
    }
}

fun main() {
    val player = PlayerProfile()
    player.score = 50
    println("Joriy ball: ${player.score}")
    
    player.score = 75
    println("Joriy ball: ${player.score}")
    
    player.score = 30 // Rad etiladi
    println("Yakuniy ball: ${player.score}")
}
```

## Tushuntirish va Mantiq:
'Delegates.vetoable' delegatsiyasi yangi qiymat berilganda tekshiruvchi predikatni ishga tushiradi. Agar predikat false qaytarsa, xususiyat o'zgarishsiz o'zining eski qiymatida qoladi.

## Ishlash natijasi:
```text
Joriy ball: 50
Joriy ball: 75
Rad etildi: Yangi ball (30) eski balldan (75) kichik bo'lishi mumkin emas!
Yakuniy ball: 75
```


# 218-Topshiriq: Xususiyatlarni boshqa xususiyatga delegatsiya qilish
## Topshiriq sharti:
Eski xususiyat nomini yangisiga '::targetProperty' orqali yo'naltirib (deprecated transition) orqaga moslikni saqlang.

## Yechim (Kotlin kodi):
```kotlin
class ApiClient {
    var newEndpoint: String = "https://api.v2.domain.uz"

    // Eski xususiyat yangisiga yo'naltirilgan:
    @Deprecated("newEndpoint dan foydalaning")
    var oldEndpoint: String by this::newEndpoint
}

fun main() {
    val client = ApiClient()
    println("Eski xususiyat orqali o'qish: ${client.oldEndpoint}")
    
    client.oldEndpoint = "https://api.v2-updated.domain.uz"
    println("Yangi xususiyat qiymati: ${client.newEndpoint}")
}
```

## Tushuntirish va Mantiq:
Kotlin 1.4 dan boshlab xususiyatni boshqa xususiyatga 'by this::target' sintaksisi orqali delegatsiya qilish mumkin. Bu API larni refaktoring qilishda eski mijozlar uchun muammosiz o'tishni ta'minlaydi.

## Ishlash natijasi:
```text
Eski xususiyat orqali o'qish: https://api.v2.domain.uz
Yangi xususiyat qiymati: https://api.v2-updated.domain.uz
```


# 219-Topshiriq: Xususiyatlarni Map da saqlash (Map Delegation)
## Topshiriq sharti:
Dinamik JSON yoki konfiguratsiya lug'atini to'g'ridan-to'g'ri sinf xususiyatlariga 'by map' orqali bog'lang.

## Yechim (Kotlin kodi):
```kotlin
class DynamicProfile(val map: Map<String, Any?>) {
    val username: String by map
    val age: Int by map
    val role: String by map
}

fun main() {
    val rawData = mapOf(
        "username" to "botir_dev",
        "age" to 27,
        "role" to "TeamLead"
    )
    
    val profile = DynamicProfile(rawData)
    println("Foydalanuvchi: ${profile.username}")
    println("Yoshi: ${profile.age}")
    println("Lavozimi: ${profile.role}")
}
```

## Tushuntirish va Mantiq:
Kotlinda 'Map' va 'MutableMap' standart xususiyat delegati vazifasini bajara oladi. Xususiyat nomi Map kaliti sifatida avtomatik o'qiladi.

## Ishlash natijasi:
```text
Foydalanuvchi: botir_dev
Yoshi: 27
Lavozimi: TeamLead
```


# 220-Topshiriq: Oddiy sinf va 'toString()', 'equals()', 'hashCode()' ni qo'lda yozish
## Topshiriq sharti:
Data class ishlatmasdan, oddiy sinf uchun asosiy metodlarni o'zingiz realizatsiya qiling.

## Yechim (Kotlin kodi):
```kotlin
class Book(val isbn: String, val title: String) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is Book) return false
        return this.isbn == other.isbn
    }

    override fun hashCode(): Int {
        return isbn.hashCode()
    }

    override fun toString(): String {
        return "Book(isbn='$isbn', title='$title')"
    }
}

fun main() {
    val b1 = Book("978-0134685991", "Effective Java")
    val b2 = Book("978-0134685991", "Effective Java (Yangi nashr)")
    
    println("b1: $b1")
    println("b1 == b2 (ISBN bir xil): ${b1 == b2}")
}
```

## Tushuntirish va Mantiq:
Oddiy klasslarda 'equals' va 'hashCode' metodlarini qo'lda yozish obyektlarning qaysi biznes maydonlari bo'yicha teng hisoblanishini (masalan, faqat ISBN bo'yicha) aniq boshqarish imkonini beradi.

## Ishlash natijasi:
```text
b1: Book(isbn='978-0134685991', title='Effective Java')
b1 == b2 (ISBN bir xil): true
```


# 221-Topshiriq: Qiymat sinflari: '@JvmInline value class'
## Topshiriq sharti:
Xotirada qo'shimcha obyekt o'rami yaratmasdan tur xavfsizligini ta'minlovchi 'value class' dan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
@JvmInline
value class UserId(val id: Long)

@JvmInline
value class OrderId(val id: Long)

fun processUserOrder(user: UserId, order: OrderId) {
    println("Foydalanuvchi #${user.id} buyurtmasi #${order.id} qayta ishlanmoqda")
}

fun main() {
    val uId = UserId(1001L)
    val oId = OrderId(998877L)
    
    // processUserOrder(oId, uId) // Kompilyatsiya xatosi: Type mismatch!
    processUserOrder(uId, oId)
}
```

## Tushuntirish va Mantiq:
'value class' (inline class) faqat bitta xususiyatni o'raydi. Ish vaqtida (runtime) u to'g'ridan-to'g'ri o'ralgan primitiv qiymatga aylanadi va hech qanday obyekt ajratilmaydi, lekin kompilyatsiya bosqichida UserId va OrderId ni adashtirib yuborishdan 100% himoya qiladi.

## Ishlash natijasi:
```text
Foydalanuvchi #1001 buyurtmasi #998877 qayta ishlanmoqda
```


# 222-Topshiriq: Konstruktor parametrlarida 'val' va oddiy parametr farqi
## Topshiriq sharti:
'val' qo'yilmagan konstruktor parametri sinf ichida xususiyatga aylanmasligini namoyish qiling.

## Yechim (Kotlin kodi):
```kotlin
class Circle(radius: Double) {
    // 'radius' da 'val' yo'q, shuning uchun u tashqaridan ko'rinmaydi
    val area: Double = Math.PI * radius * radius

    fun printInfo() {
        println("Doira yuzi: $area")
        // println(radius) // Faqat init va boshlang'ich e'lonlarda ko'rinadi
    }
}

fun main() {
    val c = Circle(5.0)
    c.printInfo()
    // println(c.radius) // Kompilyatsiya xatosi: Unresolved reference: radius
}
```

## Tushuntirish va Mantiq:
Agar asosiy konstruktor parametrida 'val' yoki 'var' yozilmasa, u faqat 'init' bloklari va xususiyat initsializatorlariga uzatiladigan oddiy parametr bo'lib qoladi va sinf maydoni sifatida xotirada saqlanmaydi.

## Ishlash natijasi:
```text
Doira yuzi: 78.53981633974483
```


# 223-Topshiriq: Sinf metodlarida zanjir chaqiruvi (Method Chaining / Fluent Interface)
## Topshiriq sharti:
Metodlardan 'this' obyektini qaytarib, ketma-ket metodlar zanjirini hosil qiling.

## Yechim (Kotlin kodi):
```kotlin
class QueryBuilder {
    private var selectPart = "*"
    private var fromPart = ""
    private var wherePart = ""

    fun select(columns: String): QueryBuilder {
        this.selectPart = columns
        return this
    }

    fun from(table: String): QueryBuilder {
        this.fromPart = table
        return this
    }

    fun where(condition: String): QueryBuilder {
        this.wherePart = condition
        return this
    }

    fun build(): String {
        var query = "SELECT $selectPart FROM $fromPart"
        if (wherePart.isNotBlank()) query += " WHERE $wherePart"
        return query
    }
}

fun main() {
    val sql = QueryBuilder()
        .select("id, name, email")
        .from("users")
        .where("is_active = true")
        .build()
        
    println("Generatsiya qilingan SQL: $sql")
}
```

## Tushuntirish va Mantiq:
'return this' orqali obyektning o'zini qaytarish 'Fluent Interface' dizayn andozasini yaratadi. Kotlinda buni 'apply' scope funksiyasi bilan ham oson bajarish mumkin.

## Ishlash natijasi:
```text
Generatsiya qilingan SQL: SELECT id, name, email FROM users WHERE is_active = true
```


# 224-Topshiriq: Xususiyat initsializatsiyasida murakkab blok: run orqali qiymat berish
## Topshiriq sharti:
Xususiyatni bir nechta hisoblashlar va shartlar bilan 'run { ... }' orqali initsializatsiya qiling.

## Yechim (Kotlin kodi):
```kotlin
class SystemReport(val rawData: List<Int>) {
    val reportSummary: String = run {
        val total = rawData.sum()
        val avg = if (rawData.isNotEmpty()) rawData.average() else 0.0
        "Jami elementlar: ${rawData.size}, Yig'indi: $total, O'rtacha: %.1f".format(avg)
    }
}

fun main() {
    val report = SystemReport(listOf(10, 20, 30, 40, 50))
    println(report.reportSummary)
}
```

## Tushuntirish va Mantiq:
'val prop = run { ... }' sintaksisi xususiyat initsializatsiyasini ixcham mahalliy o'zgaruvchilar bilan toza hisoblab biriktirishga yordam beradi.

## Ishlash natijasi:
```text
Jami elementlar: 5, Yig'indi: 150, O'rtacha: 30.0
```


# 225-Topshiriq: Sinf darajasidagi konstantalar va Companion Object
## Topshiriq sharti:
Sinf bilan bog'liq bo'lgan umumiy konstantalarni 'companion object' ichida e'lon qiling.

## Yechim (Kotlin kodi):
```kotlin
class Car(val model: String) {
    companion object {
        const val WHEEL_COUNT = 4
        fun createElectricCar(model: String): Car {
            return Car("$model (Elektr)")
        }
    }
}

fun main() {
    println("Avtomobil g'ildiraklari soni: ${Car.WHEEL_COUNT}")
    val ev = Car.createElectricCar("Tesla Model 3")
    println("Model: ${ev.model}")
}
```

## Tushuntirish va Mantiq:
'companion object' sinf ichidagi yagona hamroh obyekt bo'lib, Java dagi 'static' a'zolarning to'liq o'rnini bosadi. Undagi metod va konstantalarga to'g'ridan-to'g'ri sinf nomi orqali murojaat qilinadi.

## Ishlash natijasi:
```text
Avtomobil g'ildiraklari soni: 4
Model: Tesla Model 3 (Elektr)
```


# 226-Topshiriq: Xususiyatlarni cheklovchi 'coerceIn' metodidan foydalanish
## Topshiriq sharti:
O'zgaruvchi qiymatini ruxsat etilgan minimal va maksimal chegarada ushlab turuvchi setter yozing.

## Yechim (Kotlin kodi):
```kotlin
class AudioPlayer {
    var volume: Int = 50
        set(value) {
            // Ovoz faqat 0 va 100 oralig'ida bo'lishi shart
            field = value.coerceIn(0, 100)
        }
}

fun main() {
    val player = AudioPlayer()
    println("Boshlang'ich ovoz: ${player.volume}")
    
    player.volume = 120 // 100 ga tushiriladi
    println("120 berilganda: ${player.volume}")
    
    player.volume = -15 // 0 ga ko'tariladi
    println("-15 berilganda: ${player.volume}")
}
```

## Tushuntirish va Mantiq:
'coerceIn(min, max)' metodi berilgan sonni ko'rsatilgan oraliqda qat'iy ushlab turadi. Bu setterlarda 'if-else' o'rniga juda ixcham ishlaydi.

## Ishlash natijasi:
```text
Boshlang'ich ovoz: 50
120 berilganda: 100
-15 berilganda: 0
```


# 227-Topshiriq: Shartli hisoblash: Getter ichida kesh yaratish
## Topshiriq sharti:
Getter har safar emas, faqat holat o'zgargandagina yangidan hisoblashini tashkil qiling.

## Yechim (Kotlin kodi):
```kotlin
class CachedCalculator {
    var numbers: List<Int> = emptyList()
        set(value) {
            field = value
            isCacheValid = false // Ma'lumot o'zgardi, kesh eskirgan
        }

    private var cachedSum: Int = 0
    private var isCacheValid = false

    val sum: Int
        get() {
            if (!isCacheValid) {
                println("[HISOBLASH]: Yangi yig'indi hisoblanmoqda...")
                cachedSum = numbers.sum()
                isCacheValid = true
            }
            return cachedSum
        }
}

fun main() {
    val calc = CachedCalculator()
    calc.numbers = listOf(5, 10, 15)
    
    println("Yig'indi: ${calc.sum}")
    println("Yig'indi (ikkinchi marta): ${calc.sum}")
    
    calc.numbers = listOf(1, 2)
    println("Yig'indi (o'zgargandan keyin): ${calc.sum}")
}
```

## Tushuntirish va Mantiq:
Getter ichida 'dirty flag' (kesh eskirganligi bayrog'i) orqali og'ir amallarni faqat kerak bo'lganda hisoblash unumdorlikni oshiradi.

## Ishlash natijasi:
```text
[HISOBLASH]: Yangi yig'indi hisoblanmoqda...
Yig'indi: 30
Yig'indi (ikkinchi marta): 30
[HISOBLASH]: Yangi yig'indi hisoblanmoqda...
Yig'indi (o'zgargandan keyin): 3
```


# 228-Topshiriq: Sinf nusxalari sonini hisoblovchi Companion Object
## Topshiriq sharti:
Har safar yangi obyekt yaratilganda umumiy hisoblagichni oshirib boruvchi sinf yozing.

## Yechim (Kotlin kodi):
```kotlin
class Session(val userId: String) {
    init {
        totalActiveSessions++
        println("Yangi sessiya ochildi: $userId")
    }

    companion object {
        var totalActiveSessions = 0
            private set
    }
}

fun main() {
    val s1 = Session("user_1")
    val s2 = Session("user_2")
    val s3 = Session("user_3")
    
    println("Jami faol sessiyalar: ${Session.totalActiveSessions}")
}
```

## Tushuntirish va Mantiq:
'companion object' xotirada bitta nusxada bo'lib, uning xususiyatlari sinfning barcha nusxalari uchun umumiy hisoblanadi.

## Ishlash natijasi:
```text
Yangi sessiya ochildi: user_1
Yangi sessiya ochildi: user_2
Yangi sessiya ochildi: user_3
Jami faol sessiyalar: 3
```


# 229-Topshiriq: Maxsus annotatsiyali xususiyatlar
## Topshiriq sharti:
Xususiyat maydoniga (field), getteriga yoki parametriga alohida annotatsiya yo'naltirish (Target use-site).

## Yechim (Kotlin kodi):
```kotlin
class PersonDto(
    @get:JvmName("getFirstNameValue")
    val firstName: String
)

fun main() {
    val p = PersonDto("Jasur")
    println("Shaxs ismi: ${p.firstName}")
}
```

## Tushuntirish va Mantiq:
Kotlinda bitta xususiyat bayt-kodda bir nechta elementga aylanadi (field, getter, setter, constructor parameter). Maxsus annotatsiyalarni aniq joyga yo'naltirish uchun '@get:', '@field:', '@param:' prefikslari qo'llaniladi.

## Ishlash natijasi:
```text
Shaxs ismi: Jasur
```


# 230-Topshiriq: Xususiyatlar va Null xavfsizligi kombinatsiyasi
## Topshiriq sharti:
Sinf xususiyatining 'null' ekanligini getter ichida boshqarish.

## Yechim (Kotlin kodi):
```kotlin
class User(val firstName: String, val lastName: String?) {
    val fullName: String
        get() = if (lastName != null) "$firstName $lastName" else firstName
}

fun main() {
    val u1 = User("Botir", "Sobirov")
    val u2 = User("Sardor", null)
    
    println("To'liq ism 1: ${u1.fullName}")
    println("To'liq ism 2: ${u2.fullName}")
}
```

## Tushuntirish va Mantiq:
Getterlar ichida null tekshiruvlarini o'tkazish orqali tashqi foydalanuvchiga toza va qulay interfeys beriladi.

## Ishlash natijasi:
```text
To'liq ism 1: Botir Sobirov
To'liq ism 2: Sardor
```


# 231-Topshiriq: Xususiyat delegatini shaxsiy yaratish: ReadWriteProperty
## Topshiriq sharti:
Kotlinda o'z shaxsiy xususiyat delegatingizni 'ReadWriteProperty' interfeysi orqali yozing.

## Yechim (Kotlin kodi):
```kotlin
import kotlin.properties.ReadWriteProperty
import kotlin.reflect.KProperty

class TrimmedString : ReadWriteProperty<Any?, String> {
    private var currentValue: String = ""

    override fun getValue(thisRef: Any?, property: KProperty<*>): String {
        return currentValue
    }

    override fun setValue(thisRef: Any?, property: KProperty<*>, value: String) {
        currentValue = value.trim()
    }
}

class Article {
    var title: String by TrimmedString()
}

fun main() {
    val article = Article()
    article.title = "   Kotlinda Zamonaviy Arxitektura   "
    println("Maqola sarlavhasi: '${article.title}'")
}
```

## Tushuntirish va Mantiq:
'ReadWriteProperty<R, T>' interfeysini realizatsiya qilish orqali xususiyatga murojaat qilinganda yoki qiymat yozilganda bajariladigan maxsus xatti-harakatlarni yaratish mumkin.

## Ishlash natijasi:
```text
Maqola sarlavhasi: 'Kotlinda Zamonaviy Arxitektura'
```


# 232-Topshiriq: Faqat o'qiladigan shaxsiy delegat: ReadOnlyProperty
## Topshiriq sharti:
Tizim parametrlarini o'qib beruvchi 'ReadOnlyProperty' delegatini yarating.

## Yechim (Kotlin kodi):
```kotlin
import kotlin.properties.ReadOnlyProperty
import kotlin.reflect.KProperty

class EnvProperty(val envKey: String, val defaultVal: String) : ReadOnlyProperty<Any?, String> {
    override fun getValue(thisRef: Any?, property: KProperty<*>): String {
        return System.getenv(envKey) ?: defaultVal
    }
}

class AppEnv {
    val activeProfile: String by EnvProperty("APP_PROFILE", "development")
}

fun main() {
    val env = AppEnv()
    println("Faol profil: ${env.activeProfile}")
}
```

## Tushuntirish va Mantiq:
'ReadOnlyProperty' faqat 'val' xususiyatlar uchun mo'ljallangan bo'lib, uning ichida faqat 'getValue' metodi yoziladi.

## Ishlash natijasi:
```text
Faol profil: development
```


# 233-Topshiriq: Klass ichida operator funksiyalarini e'lon qilish
## Topshiriq sharti:
Sinf o'z ichida boshqa bir xususiyat bilan mantiqiy bog'lanuvchi 'contains' operatorini saqlasin.

## Yechim (Kotlin kodi):
```kotlin
class Team(val teamName: String) {
    private val members = mutableListOf<String>()

    fun addMember(name: String) {
        members.add(name)
    }

    operator fun contains(person: String): Boolean {
        return person in members
    }
}

fun main() {
    val mobileTeam = Team("Android Team")
    mobileTeam.addMember("Sardor")
    mobileTeam.addMember("Javohir")
    
    println("Sardor jamoada bormi: ${"Sardor" in mobileTeam}")
    println("Temur jamoada bormi: ${"Temur" in mobileTeam}")
}
```

## Tushuntirish va Mantiq:
Sinf tanasida 'operator fun' yozish ushbu sinf obyektlari ustida Kotlin operatorlarini to'g'ridan-to'g'ri ishlatish imkonini beradi.

## Ishlash natijasi:
```text
Sardor jamoada bormi: true
Temur jamoada bormi: false
```


# 234-Topshiriq: Sinf obyektlarini nusxalash va himoyalash
## Topshiriq sharti:
O'zgaruvchan ichki massivni o'zida saqlovchi sinfning chuqur nusxasini (deep copy) hosil qiluvchi metod yozing.

## Yechim (Kotlin kodi):
```kotlin
class IntMatrix(val rows: Int, val cols: Int) {
    val data = Array(rows) { IntArray(cols) }

    fun copy(): IntMatrix {
        val newMatrix = IntMatrix(rows, cols)
        for (i in 0 until rows) {
            newMatrix.data[i] = this.data[i].clone()
        }
        return newMatrix
    }
}

fun main() {
    val m1 = IntMatrix(2, 2)
    m1.data[0][0] = 42
    
    val m2 = m1.copy()
    m2.data[0][0] = 99
    
    println("m1[0][0]: ${m1.data[0][0]}")
    println("m2[0][0]: ${m2.data[0][0]}")
}
```

## Tushuntirish va Mantiq:
Ichki o'zgaruvchan massivlar mavjud bo'lganda chuqur nusxalash (deep copy) orqali obyektlar bir-birining ma'lumotlariga nojo'ya ta'sir o'tkazishining oldi olinadi.

## Ishlash natijasi:
```text
m1[0][0]: 42
m2[0][0]: 99
```


# 235-Topshiriq: Klassda xususiyatlar tengligini tekshirish uchun Identifiable interfeysi
## Topshiriq sharti:
Har bir identifikatsiyalanuvchi obyektning tengligini faqat uning 'id' si orqali aniqlash.

## Yechim (Kotlin kodi):
```kotlin
interface Identifiable {
    val id: Long
}

class Product(override val id: Long, val title: String, var price: Double) : Identifiable {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is Product) return false
        return this.id == other.id
    }

    override fun hashCode(): Int = id.hashCode()
}

fun main() {
    val p1 = Product(101L, "Klaviatura", 50.0)
    val p2 = Product(101L, "Klaviatura (Chegirmada)", 40.0)
    
    println("Mahsulotlar bitta ID ga egami: ${p1 == p2}")
}
```

## Tushuntirish va Mantiq:
Domen obyektlarida (Entity) obyektlar tengligi ularning barcha xususiyatlari bilan emas, balki birlamchi kalit (ID) bo'yicha baholanadi.

## Ishlash natijasi:
```text
Mahsulotlar bitta ID ga egami: true
```


# 236-Topshiriq: Klass ichida xavfsiz hisoblagich: Thread-safe Counter
## Topshiriq sharti:
AtomicInteger yordamida ko'p oqimli muhitda xavfsiz ishlaydigan sinf xususiyatini yarating.

## Yechim (Kotlin kodi):
```kotlin
import java.util.concurrent.atomic.AtomicInteger

class SafeCounter {
    private val atomicCount = AtomicInteger(0)

    val current: Int
        get() = atomicCount.get()

    fun incrementAndGet(): Int {
        return atomicCount.incrementAndGet()
    }
}

fun main() {
    val counter = SafeCounter()
    println("Qadam 1: ${counter.incrementAndGet()}")
    println("Qadam 2: ${counter.incrementAndGet()}")
    println("Yakuniy: ${counter.current}")
}
```

## Tushuntirish va Mantiq:
Java kutubxonasining 'AtomicInteger' klassi operativ xotirada qulflashlarsiz (lock-free) atomik amallarni ta'minlaydi va xavfsiz backing field vazifasini o'taydi.

## Ishlash natijasi:
```text
Qadam 1: 1
Qadam 2: 2
Yakuniy: 2
```


# 237-Topshiriq: Sinf xususiyatlarini kechiktirilgan hisoblash: lazy vs lateinit amaliy solishtiruvi
## Topshiriq sharti:
Ikkala yondashuvni bitta xizmat sinfida yonma-yon solishtiring.

## Yechim (Kotlin kodi):
```kotlin
class ServiceTester {
    // lateinit: faqat var, keyinchalik qo'lda biriktiriladi
    lateinit var manualClient: String

    // lazy: faqat val, birinchi murojaatda avtomatik hisoblanadi
    val lazyEngine: String by lazy {
        "Dvigatel_Yuklandi"
    }
}

fun main() {
    val tester = ServiceTester()
    tester.manualClient = "Mijoz_Sozlangan"
    
    println("Lateinit xususiyat: ${tester.manualClient}")
    println("Lazy xususiyat: ${tester.lazyEngine}")
}
```

## Tushuntirish va Mantiq:
'lateinit' tashqaridan qiymat berilishi kutilganda ishlatiladi. 'lazy' esa hisoblash formulasi yoki obyekt yaratish qoidasi ma'lum bo'lib, lekin uni dastur boshida yuklamaslik kerak bo'lganda qo'llaniladi.

## Ishlash natijasi:
```text
Lateinit xususiyat: Mijoz_Sozlangan
Lazy xususiyat: Dvigatel_Yuklandi
```


# 238-Topshiriq: Klass ichida yordamchi Typealias e'lon qilish
## Topshiriq sharti:
Murakkab parametr turini tushunarli qilish uchun sinf darajasida yoki fayl darajasida 'typealias' qo'llang.

## Yechim (Kotlin kodi):
```kotlin
typealias ClickListener = (viewId: Int, action: String) -> Unit

class ButtonController {
    var listener: ClickListener? = null

    fun triggerClick(id: Int) {
        listener?.invoke(id, "CLICK_EVENT")
    }
}

fun main() {
    val controller = ButtonController()
    controller.listener = { id, action ->
        println("Tugma bosildi: ID=$id | Harakat: $action")
    }
    
    controller.triggerClick(1005)
}
```

## Tushuntirish va Mantiq:
'typealias' yangi tur yaratmaydi, balki mavjud murakkab funksiya yoki generik turlarga qisqa va qulay taxallus (alias) beradi.

## Ishlash natijasi:
```text
Tugma bosildi: ID=1005 | Harakat: CLICK_EVENT
```


# 239-Topshiriq: Shartli boshqaruv: Obyekt holati va toString chiroyli chiqarish
## Topshiriq sharti:
Sinf holatini JSON formatiga o'xshatib 'toString()' orqali formatlang.

## Yechim (Kotlin kodi):
```kotlin
class ServerStatus(val ip: String, val uptimeHours: Int, val isActive: Boolean) {
    override fun toString(): String {
        return """
            {
                "ip": "$ip",
                "uptime": $uptimeHours,
                "active": $isActive
            }
        """.trimIndent()
    }
}

fun main() {
    val status = ServerStatus("192.168.1.100", 240, true)
    println(status)
}
```

## Tushuntirish va Mantiq:
'toString()' metodini to'g'ri formatda qayta yozish dasturni disk raskadrovka qilish (debugging) va loglarda ma'lumotlarni aniq ko'rish uchun muhimdir.

## Ishlash natijasi:
```text
{
    "ip": "192.168.1.100",
    "uptime": 240,
    "active": true
}
```


# 240-Topshiriq: Sinf xususiyatlarini tekshiruvchi maxsus Validatsiya klassi
## Topshiriq sharti:
Xususiyatlarni qoidalarga asosan tekshiruvchi 'Validator' yordamchi sinfini tuzing.

## Yechim (Kotlin kodi):
```kotlin
class RegistrationForm(val email: String, val age: Int) {
    val isValid: Boolean
        get() = email.contains("@") && email.contains(".") && age >= 16
}

fun main() {
    val form1 = RegistrationForm("ali@gmail.com", 19)
    val form2 = RegistrationForm("not_an_email", 25)
    
    println("Forma 1 yaroqlimi: ${form1.isValid}")
    println("Forma 2 yaroqlimi: ${form2.isValid}")
}
```

## Tushuntirish va Mantiq:
Hisoblanuvchi xususiyatlar (computed properties) formalar va foydalanuvchi ma'lumotlarini tekshirishda juda qo'l keladi.

## Ishlash natijasi:
```text
Forma 1 yaroqlimi: true
Forma 2 yaroqlimi: false
```


# 241-Topshiriq: Klasslar va Resurslarni xavfsiz tozalash: Closeable interfeysi
## Topshiriq sharti:
Obyekt o'z ishini tugatganda resurslarni xavfsiz yopuvchi 'AutoCloseable' yoki 'Closeable' ni amalga oshiring.

## Yechim (Kotlin kodi):
```kotlin
import java.io.Closeable

class CustomResource(val name: String) : Closeable {
    init {
        println("Resurs ochildi: $name")
    }

    fun work() {
        println("Resurs bilan ish olib borilmoqda...")
    }

    override fun close() {
        println("Resurs xavfsiz yopildi: $name")
    }
}

fun main() {
    CustomResource("XotiraFayli").use { res ->
        res.work()
    }
}
```

## Tushuntirish va Mantiq:
Kotlinda 'Closeable' interfeysini realizatsiya qilgan sinflar 'use { ... }' bloki orqali ishlatilganda, blok tugashi bilan 'close()' avtomatik ravishda chaqiriladi.

## Ishlash natijasi:
```text
Resurs ochildi: XotiraFayli
Resurs bilan ish olib borilmoqda...
Resurs xavfsiz yopildi: XotiraFayli
```


# 242-Topshiriq: Konstruktor parametrida funksiya qabul qilish
## Topshiriq sharti:
Sinf o'z holati o'zgarganda xabar berish uchun konstruktorida hodisa qabul qilsin (Callback pattern).

## Yechim (Kotlin kodi):
```kotlin
class DownloadManager(val onProgress: (Int) -> Unit) {
    fun startDownload() {
        for (p in listOf(25, 50, 75, 100)) {
            onProgress(p)
        }
    }
}

fun main() {
    val manager = DownloadManager { percent ->
        println("Yuklanish foizi: $percent%")
    }
    manager.startDownload()
}
```

## Tushuntirish va Mantiq:
Konstruktor parametrida lambda funksiya qabul qilish orqali tinglovchi (listener/callback) mexanizmi juda ixcham va toza shakllanadi.

## Ishlash natijasi:
```text
Yuklanish foizi: 25%
Yuklanish foizi: 50%
Yuklanish foizi: 75%
Yuklanish foizi: 100%
```


# 243-Topshiriq: Sinf xususiyatlarida o'zaro bog'liqlik
## Topshiriq sharti:
Bitta xususiyat o'zgarganda boshqa hisoblanuvchi xususiyatlarning avtomatik yangilanishi.

## Yechim (Kotlin kodi):
```kotlin
class TemperatureConverter {
    var celsius: Double = 0.0

    var fahrenheit: Double
        get() = celsius * 9.0 / 5.0 + 32.0
        set(value) {
            celsius = (value - 32.0) * 5.0 / 9.0
        }
}

fun main() {
    val t = TemperatureConverter()
    t.celsius = 100.0
    println("100°C = ${t.fahrenheit}°F")
    
    t.fahrenheit = 32.0
    println("32°F = ${t.celsius}°C")
}
```

## Tushuntirish va Mantiq:
Ikkita harorat o'lchov birligini bitta asosiy xususiyatga (celsius) bog'lab, fahrenheit xususiyatiga getter va setter yozish orqali ikki tomonlama o'zaro bog'lanish yaratiladi.

## Ishlash natijasi:
```text
100°C = 212.0°F
32°F = 0.0°C
```


# 244-Topshiriq: Klassda tranzaksiya o'tkazish: Holatni qaytarish (Rollback)
## Topshiriq sharti:
Xatolik yuz berganda obyektning ichki holatini avvalgi nuqtaga qaytaruvchi sinf yarating.

## Yechim (Kotlin kodi):
```kotlin
class TransactionalAccount(var balance: Double) {
    fun transferWithRollback(amount: Double, failSimulation: Boolean) {
        val initialBalance = balance
        println("Tranzaksiya boshlandi: Boshlang'ich balans: $$initialBalance")
        
        balance -= amount
        
        if (failSimulation) {
            println("[XATOLIK]: Tarmoqda nosozlik! Tranzaksiya bekor qilinmoqda...")
            balance = initialBalance // Rollback
        } else {
            println("[MUVAFFAQIN]: Tranzaksiya tasdiqlandi. Yangi balans: $$balance")
        }
    }
}

fun main() {
    val acc = TransactionalAccount(1000.0)
    acc.transferWithRollback(200.0, failSimulation = true)
    println("Balans (xatodan so'ng): $${acc.balance}")
}
```

## Tushuntirish va Mantiq:
Obyekt ichki xususiyatlarini saqlab, xatolikda eski holatga qaytarish bank va ma'lumotlar bazasi tizimlarida ACID talablarini qondiradi.

## Ishlash natijasi:
```text
Tranzaksiya boshlandi: Boshlang'ich balans: $1000.0
[XATOLIK]: Tarmoqda nosozlik! Tranzaksiya bekor qilinmoqda...
Balans (xatodan so'ng): $1000.0
```


# 245-Topshiriq: Shaxsiy xususiyat delegati bilan xotira keshini muddati bilan yaratish (TTL Cache)
## Topshiriq sharti:
Vaqtinchalik yaroqli kesh xususiyatini shakllantiring.

## Yechim (Kotlin kodi):
```kotlin
class ExpiringValue<T>(val ttlMs: Long, val supplier: () -> T) {
    private var cachedValue: T? = null
    private var lastFetchedTime: Long = 0

    operator fun getValue(thisRef: Any?, property: kotlin.reflect.KProperty<*>): T {
        val now = System.currentTimeMillis()
        if (cachedValue == null || (now - lastFetchedTime) > ttlMs) {
            cachedValue = supplier()
            lastFetchedTime = now
            println("[KESH]: Yangilandi")
        }
        return cachedValue!!
    }
}

class Dashboard {
    val liveRate: Double by ExpiringValue(1000L) {
        12800.0
    }
}

fun main() {
    val dash = Dashboard()
    println("1-chaqiruv: ${dash.liveRate}")
    println("2-chaqiruv: ${dash.liveRate}")
}
```

## Tushuntirish va Mantiq:
Maxsus delegat xususiyatning yaroqlilik muddatini (Time-to-Live) kuzatib boradi va eskirganda yangi qiymatni qayta hisoblaydi.

## Ishlash natijasi:
```text
[KESH]: Yangilandi
1-chaqiruv: 12800.0
2-chaqiruv: 12800.0
```


# 246-Topshiriq: Sinfda murakkab holatlar boshqaruvi: State Pattern
## Topshiriq sharti:
Obyektning xususiyati uning ichki holat sinfiga qarab o'zgarishini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
interface State {
    fun handle(): String
}

class PendingState : State {
    override fun handle(): String = "Buyurtma ko'rib chiqilmoqda"
}

class ShippedState : State {
    override fun handle(): String = "Buyurtma yo'lda"
}

class ShipmentContext {
    var state: State = PendingState()

    fun printCurrentStatus() {
        println("Holat: ${state.handle()}")
    }
}

fun main() {
    val shipment = ShipmentContext()
    shipment.printCurrentStatus()
    
    shipment.state = ShippedState()
    shipment.printCurrentStatus()
}
```

## Tushuntirish va Mantiq:
State andozasi sinfning xatti-harakatini uning 'state' xususiyati o'zgarganda dinamik o'zgartirishga xizmat qiladi.

## Ishlash natijasi:
```text
Holat: Buyurtma ko'rib chiqilmoqda
Holat: Buyurtma yo'lda
```


# 247-Topshiriq: Sinf xususiyatlarida xavfsizlik: Parolni shifrlab saqlash
## Topshiriq sharti:
Parolni ochiq holda saqlamasdan, faqat xesh ko'rinishida saqlovchi sinf tuzing.

## Yechim (Kotlin kodi):
```kotlin
class SecureUser(val username: String) {
    var passwordHash: String = ""
        private set

    fun setPassword(plainText: String) {
        require(plainText.length >= 6) { "Parol kamida 6 belgidan iborat bo'lishi kerak!" }
        // Oddiy xesh simulyatsiyasi
        passwordHash = "HASH_" + plainText.hashCode().toString()
        println("Parol xavfsiz saqlandi.")
    }

    fun verifyPassword(input: String): Boolean {
        return passwordHash == "HASH_" + input.hashCode().toString()
    }
}

fun main() {
    val user = SecureUser("rustam_01")
    user.setPassword("secret123")
    
    println("To'g'ri parol: ${user.verifyPassword("secret123")}")
    println("Noto'g'ri parol: ${user.verifyPassword("wrongpass")}")
}
```

## Tushuntirish va Mantiq:
Inkapsulyatsiya tufayli maxfiy ma'lumotlar ochiq matn sifatida saqlanmaydi va faqat 'verify' metodi orqali tekshiriladi.

## Ishlash natijasi:
```text
Parol xavfsiz saqlandi.
To'g'ri parol: true
Noto'g'ri parol: false
```


# 248-Topshiriq: Sinf xususiyatlarini avtomatik ro'yxatga olish
## Topshiriq sharti:
Obyekt yaratilganda uni markaziy ro'yxatga qo'shib boruvchi mexanizm tuzing.

## Yechim (Kotlin kodi):
```kotlin
class Device(val deviceId: String) {
    init {
        Registry.register(this)
    }

    companion object Registry {
        private val devices = mutableListOf<Device>()

        fun register(device: Device) {
            devices.add(device)
            println("Yangi qurilma ro'yxatga olindi: ${device.deviceId}")
        }

        fun getAll(): List<Device> = devices.toList()
    }
}

fun main() {
    val d1 = Device("DEV-001")
    val d2 = Device("DEV-002")
    
    println("Jami qurilmalar: ${Device.getAll().size} ta")
}
```

## Tushuntirish va Mantiq:
'init' blokidan 'companion object' ning boshqaruv funksiyasini chaqirish orqali barcha obyektlar markaziy registrda avtomatik to'planadi.

## Ishlash natijasi:
```text
Yangi qurilma ro'yxatga olindi: DEV-001
Yangi qurilma ro'yxatga olindi: DEV-002
Jami qurilmalar: 2 ta
```


# 249-Topshiriq: Sinf xususiyatlarini massiv orqali initsializatsiya qilish
## Topshiriq sharti:
Asosiy konstruktorga massiv berib, ichki ko'rsatkichlarni xavfsiz nusxa bilan to'ldirish.

## Yechim (Kotlin kodi):
```kotlin
class ScoreBoard(initialScores: IntArray) {
    // Tashqi massiv o'zgarganda ichki holat buzilmasligi uchun nusxa olinadi:
    private val scores = initialScores.clone()

    val maxScore: Int
        get() = scores.maxOrNull() ?: 0

    val averageScore: Double
        get() = if (scores.isNotEmpty()) scores.average() else 0.0
}

fun main() {
    val externalArray = intArrayOf(85, 90, 78)
    val board = ScoreBoard(externalArray)
    
    externalArray[0] = 100 // Tashqi massiv o'zgartirildi
    
    println("Maksimal ball: ${board.maxScore}") // Hali ham 90 bo'lib qoladi
    println("O'rtacha ball: ${board.averageScore}")
}
```

## Tushuntirish va Mantiq:
Konstruktorga o'zgaruvchan massiv uzatilganda 'clone()' qilish 'Defensive Copy' (himoyalangan nusxa) andozasi bo'lib, ob'ektning yaxlitligini kafolatlaydi.

## Ishlash natijasi:
```text
Maksimal ball: 90
O'rtacha ball: 84.33333333333333
```


# 250-Topshiriq: Sinflar, konstruktorlar va xususiyatlar bo'yicha to'liq amaliy xulosa
## Topshiriq sharti:
Primary/Secondary konstruktorlar, init bloklari, custom getter/setter, backing property va lazy xususiyatlarni birlashtirgan Bank tizimini quring.

## Yechim (Kotlin kodi):
```kotlin
class CorporateAccount(val companyName: String, val taxId: String) {
    private val _transactions = mutableListOf<String>()
    
    val transactions: List<String>
        get() = _transactions

    var balance: Double = 0.0
        private set(value) {
            field = value
        }

    val accountTier: String by lazy {
        println("--> Kompaniya a'zolik darajasi hisoblanmoqda...")
        if (balance > 100_000.0) "VIP Korporativ" else "Standart Korporativ"
    }

    init {
        require(companyName.isNotBlank()) { "Kompaniya nomi talab qilinadi!" }
        require(taxId.length == 9) { "STIR (INN) 9 ta raqam bo'lishi shart!" }
        println("[OCHILDI]: $companyName hisob raqami ro'yxatga olindi.")
    }

    constructor(companyName: String, taxId: String, initialDeposit: Double) : this(companyName, taxId) {
        deposit(initialDeposit)
    }

    fun deposit(amount: Double) {
        require(amount > 0) { "Summa musbat bo'lishi shart" }
        balance += amount
        _transactions.add("KIRIM: +$$amount (Yangi balans: $$balance)")
    }

    fun withdraw(amount: Double) {
        require(amount > 0) { "Summa musbat bo'lishi shart" }
        check(balance >= amount) { "Mablag' yetarli emas!" }
        balance -= amount
        _transactions.add("CHIQIM: -$$amount (Yangi balans: $$balance)")
    }
}

fun main() {
    val corp = CorporateAccount("Orol Soft MCHJ", "123456789", 50000.0)
    corp.deposit(60000.0)
    corp.withdraw(10000.0)
    
    println("Kompaniya balansi: $$${corp.balance}")
    println("A'zolik darajasi: ${corp.accountTier}")
    println("Tranzaksiyalar tarixi:")
    corp.transactions.forEach { println(" $it") }
}
```

## Tushuntirish va Mantiq:
Ushbu yakuniy topshiriqda mavzuning barcha asosiy tamoyillari: Asosiy va ikkilamchi konstruktorlar, 'init' validatsiyasi, private setter, backing property ('_transactions'), hisoblanuvchi 'lazy' xususiyat to'liq mujassamlashgan.

## Ishlash natijasi:
```text
[OCHILDI]: Orol Soft MCHJ hisob raqami ro'yxatga olindi.
Kompaniya balansi: $100000.0
--> Kompaniya a'zolik darajasi hisoblanmoqda...
A'zolik darajasi: VIP Korporativ
Tranzaksiyalar tarixi:
 KIRIM: +$50000.0 (Yangi balans: $50000.0)
 KIRIM: +$60000.0 (Yangi balans: $110000.0)
 CHIQIM: -$10000.0 (Yangi balans: $100000.0)
```

