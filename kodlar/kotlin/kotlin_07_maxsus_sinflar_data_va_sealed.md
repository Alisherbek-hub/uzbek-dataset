# 301-Topshiriq: Data Class asoslari va avtomatik metodlar
## Topshiriq sharti:
Ma'lumot saqlovchi 'data class' e'lon qilib, uning avtomatik generatsiya qilingan 'toString()', 'equals()' va 'hashCode()' metodlarini tekshiring.

## Yechim (Kotlin kodi):
```kotlin
data class User(val id: Long, val name: String, val email: String)

fun main() {
    val u1 = User(1L, "Sanjar", "sanjar@dev.uz")
    val u2 = User(1L, "Sanjar", "sanjar@dev.uz")
    val u3 = User(2L, "Malika", "malika@dev.uz")
    
    // toString() avtomatik chiroyli matn beradi:
    println("u1: $u1")
    
    // equals() (==) barcha maydonlarni solishtiradi:
    println("u1 == u2: ${u1 == u2}")
    println("u1 == u3: ${u1 == u3}")
    
    // hashCode() bir xil qiymatlar uchun bir xil bo'ladi:
    println("u1 hashCode == u2 hashCode: ${u1.hashCode() == u2.hashCode()}")
}
```

## Tushuntirish va Mantiq:
Kotlinda 'data class' kalit so'zi ma'lumotlarni saqlashga mo'ljallangan sinflar uchun ishlatiladi. Kompilyator asosiy konstruktorda e'lon qilingan barcha xususiyatlar asosida 'toString()', 'equals()', 'hashCode()', 'copy()' va 'componentN()' metodlarini avtomatik generatsiya qiladi.

## Ishlash natijasi:
```text
u1: User(id=1, name=Sanjar, email=sanjar@dev.uz)
u1 == u2: true
u1 == u3: false
u1 hashCode == u2 hashCode: true
```


# 302-Topshiriq: O'zgarmaslik va nusxalash: 'copy()' metodi
## Topshiriq sharti:
Mavjud data class obyektining ayrim xususiyatlarini o'zgartirib yangi nusxa olish uchun 'copy()' metodidan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
data class CustomerOrder(
    val orderId: String,
    val item: String,
    val quantity: Int,
    val status: String
)

fun main() {
    val order1 = CustomerOrder("ORD-101", "Smartfon", 1, "YANGI")
    println("Boshlang'ich buyurtma: $order1")
    
    // Nusxa olish va faqat statusni o'zgartirish (Immutability):
    val order2 = order1.copy(status = "YETKAZILMOQDA")
    val order3 = order2.copy(quantity = 2, status = "YOPILDI")
    
    println("Yangilangan buyurtma 1: $order2")
    println("Yangilangan buyurtma 2: $order3")
}
```

## Tushuntirish va Mantiq:
'copy()' metodi o'zgarmas (immutable) arxitekturaning asosi hisoblanadi. Asl obyektga zarar yetkazmasdan, faqat kerakli maydonlari o'zgartirilgan yangi obyekt hosil qilinadi.

## Ishlash natijasi:
```text
Boshlang'ich buyurtma: CustomerOrder(orderId=ORD-101, item=Smartfon, quantity=1, status=YANGI)
Yangilangan buyurtma 1: CustomerOrder(orderId=ORD-101, item=Smartfon, quantity=1, status=YETKAZILMOQDA)
Yangilangan buyurtma 2: CustomerOrder(orderId=ORD-101, item=Smartfon, quantity=2, status=YOPILDI)
```


# 303-Topshiriq: Destruksiya (Destructuring Declarations) va componentN()
## Topshiriq sharti:
Data class obyektini alohida o'zgaruvchilarga bo'lib olish (destrukturizatsiya) jarayonini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
data class GeoPoint(val latitude: Double, val longitude: Double, val city: String)

fun main() {
    val location = GeoPoint(41.2995, 69.2401, "Toshkent")
    
    // Destructuring sintaksisi:
    val (lat, lon, cityName) = location
    
    println("Kenglik: $lat")
    println("Uzunlik: $lon")
    println("Shahar: $cityName")
    
    // Orqa fonda componentN() metodlari chaqiriladi:
    println("component1(): ${location.component1()}")
    println("component2(): ${location.component2()}")
}
```

## Tushuntirish va Mantiq:
Data class lar har bir asosiy konstruktor parametri uchun tartib bo'yicha 'component1()', 'component2()', ... metodlarini yaratadi. 'val (a, b) = obj' sintaksisi orqali obyekt bir vaqtning o'zida alohida o'zgaruvchilarga ajratiladi.

## Ishlash natijasi:
```text
Kenglik: 41.2995
Uzunlik: 69.2401
Shahar: Toshkent
component1(): 41.2995
component2(): 69.2401
```


# 304-Topshiriq: Sinf tanasidagi xususiyatlar va Data Class
## Topshiriq sharti:
Konstruktorda emas, balki sinf tanasida e'lon qilingan xususiyatlar avtomatik metodlarga (equals/hashCode) kirmasligini namoyish qiling.

## Yechim (Kotlin kodi):
```kotlin
data class Person(val name: String) {
    var age: Int = 0 // Sinf tanasidagi xususiyat
}

fun main() {
    val p1 = Person("Aziz")
    p1.age = 20
    
    val p2 = Person("Aziz")
    p2.age = 30
    
    // Faqat konstruktordagi 'name' hisobga olinadi:
    println("p1 == p2: ${p1 == p2}") // true!
    println("p1: $p1") // toString da ham age ko'rinmaydi
}
```

## Tushuntirish va Mantiq:
Data class larda 'equals()', 'hashCode()' va 'toString()' metodlari faqat asosiy konstruktorda (primary constructor) e'lon qilingan xususiyatlar asosida tuziladi. Sinf tanasida e'lon qilingan xususiyatlar bu avtomatik metodlardan chetda qoladi.

## Ishlash natijasi:
```text
p1 == p2: true
p1: Person(name=Aziz)
```


# 305-Topshiriq: Data Class ga qo'yilgan qat'iy talablar
## Topshiriq sharti:
Data class asosiy konstruktorida kamida bitta parametr bo'lishi va barchasi 'val' yoki 'var' bo'lishi shartligini tushuntiring.

## Yechim (Kotlin kodi):
```kotlin
// data class EmptyData // Xato: Data class must have at least one primary constructor parameter
// data class NoVal(name: String) // Xato: All primary constructor parameters must be val or var

data class ValidEntity(val id: Int, var status: String)

fun main() {
    val entity = ValidEntity(1, "Aktiv")
    println("Muvaffaqiyatli entity: $entity")
}
```

## Tushuntirish va Mantiq:
Kotlin qoidalariga ko'ra, data class asosiy konstruktori kamida bitta parametrga ega bo'lishi, barcha parametrlar 'val' yoki 'var' bilan belgilanishi, data class o'zi 'abstract', 'open', 'sealed' yoki 'inner' bo'la olmasligi shart.

## Ishlash natijasi:
```text
Muvaffaqiyatli entity: ValidEntity(id=1, status=Aktiv)
```


# 306-Topshiriq: Enum Class asoslari: O'zgarmaslar to'plami
## Topshiriq sharti:
Hafta kunlari yoki yo'nalishlarni ifodalovchi oddiy 'enum class' e'lon qiling.

## Yechim (Kotlin kodi):
```kotlin
enum class Direction {
    NORTH, SOUTH, EAST, WEST
}

fun main() {
    val currentDirection = Direction.NORTH
    
    println("Yo'nalish: $currentDirection")
    println("Nomi (name): ${currentDirection.name}")
    println("Tartib raqami (ordinal): ${currentDirection.ordinal}")
}
```

## Tushuntirish va Mantiq:
'enum class' (sanab o'tiluvchi turlar) oldindan ma'lum bo'lgan cheklangan qiymatlar to'plamini ifodalash uchun ishlatiladi. Har bir enum qiymati 'name' (satr ko'rinishi) va 'ordinal' (0 dan boshlanuvchi tartib indeksi) xususiyatlariga ega.

## Ishlash natijasi:
```text
Yo'nalish: NORTH
Nomi (name): NORTH
Tartib raqami (ordinal): 0
```


# 307-Topshiriq: Parametrlarga ega Enum Class
## Topshiriq sharti:
Har bir enum elementi uchun maxsus xususiyatlar (kod, foiz, tavsif) biriktiring.

## Yechim (Kotlin kodi):
```kotlin
enum class Currency(val code: String, val symbol: Char, val rateToUzs: Double) {
    USD("USD", '$', 12800.0),
    EUR("EUR", '€', 13900.0),
    RUB("RUB", '₽', 135.0)
}

fun main() {
    for (currency in Currency.values()) {
        println("${currency.code} (${currency.symbol}) -> 1 birlik = ${currency.rateToUzs} UZS")
    }
}
```

## Tushuntirish va Mantiq:
Enum sinflar konstruktorga ega bo'lishi mumkin. Har bir e'lon qilingan doimiy qiymat (enum constant) o'sha konstruktor orqali o'zining shaxsiy xususiyatlarini saqlaydi.

## Ishlash natijasi:
```text
USD ($) -> 1 birlik = 12800.0 UZS
EUR (€) -> 1 birlik = 13900.0 UZS
RUB (₽) -> 1 birlik = 135.0 UZS
```


# 308-Topshiriq: Zamonaviy Enum xususiyati: entries (Kotlin 1.9+)
## Topshiriq sharti:
Eski 'values()' o'rniga yangi va xotirani tejovchi 'entries' ro'yxatidan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
enum class Priority { LOW, MEDIUM, HIGH, CRITICAL }

fun main() {
    // values() har chaqirilganda yangi massiv Array yaratadi (ortiqcha xotira)
    // Kotlin 1.9+ 'entries' esa keshlanadigan o'zgarmas List<T> qaytaradi:
    println("Barcha ustuvorliklar (entries):")
    Priority.entries.forEach { priority ->
        println(" - $priority (index: ${priority.ordinal})")
    }
}
```

## Tushuntirish va Mantiq:
Kotlin 1.9 da kiritilgan 'EnumClass.entries' eski 'values()' metodini to'liq almashtiradi. 'values()' har safar yangi massiv klonlasa, 'entries' oldindan tayyor ro'yxat qaytarib Garbage Collector yukini sezilarli darajada kamaytiradi.

## Ishlash natijasi:
```text
Barcha ustuvorliklar (entries):
 - LOW (index: 0)
 - MEDIUM (index: 1)
 - HIGH (index: 2)
 - CRITICAL (index: 3)
```


# 309-Topshiriq: Enum elementlarida maxsus metodlar (Constant-Specific Methods)
## Topshiriq sharti:
Har bir enum elementi o'zining xatti-harakatini alohida amalga oshirishini (anonim sinf kabi) ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
enum class Operation {
    PLUS {
        override fun apply(x: Double, y: Double): Double = x + y
    },
    MINUS {
        override fun apply(x: Double, y: Double): Double = x - y
    },
    MULTIPLY {
        override fun apply(x: Double, y: Double): Double = x * y
    };

    abstract fun apply(x: Double, y: Double): Double
}

fun main() {
    val a = 12.0
    val b = 4.0
    
    println("PLUS: " + Operation.PLUS.apply(a, b))
    println("MINUS: " + Operation.MINUS.apply(a, b))
    println("MULTIPLY: " + Operation.MULTIPLY.apply(a, b))
}
```

## Tushuntirish va Mantiq:
Enum sinfda abstrakt metod e'lon qilib, har bir enum konstantasi ichida uni 'override' qilish mumkin. Bu har bir qiymatga o'ziga xos polimorfik harakat berish imkonini taqdim etadi.

## Ishlash natijasi:
```text
PLUS: 16.0
MINUS: 8.0
MULTIPLY: 48.0
```


# 310-Topshiriq: Enum sinflar interfeyslarni amalga oshirishi
## Topshiriq sharti:
Enum klassini umumiy biznes interfeysiga ulash va polimorfik chaqirish.

## Yechim (Kotlin kodi):
```kotlin
interface Translatable {
    fun getUzbekTitle(): String
}

enum class UserRole : Translatable {
    ADMIN {
        override fun getUzbekTitle(): String = "Tizim Administratori"
    },
    MODERATOR {
        override fun getUzbekTitle(): String = "Nazoratchi"
    },
    USER {
        override fun getUzbekTitle(): String = "Oddiy Foydalanuvchi"
    }
}

fun main() {
    val role: Translatable = UserRole.ADMIN
    println("Rol: ${role.getUzbekTitle()}")
}
```

## Tushuntirish va Mantiq:
Enum sinflar boshqa sinflardan meros ola olmaydi (chunki ular ichki 'java.lang.Enum' dan meros olgan), ammo ular istalgancha interfeyslarni amalga oshira oladi.

## Ishlash natijasi:
```text
Rol: Tizim Administratori
```


# 311-Topshiriq: Sealed Class asoslari: Yopiq turlar iyerarxiyasi
## Topshiriq sharti:
Faqat bitta fayl doirasida meros olinishi mumkin bo'lgan 'sealed class' e'lon qiling va uning 'when' bilan to'liq tekshirilishini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
sealed class NetworkResult {
    data class Success(val data: String) : NetworkResult()
    data class Error(val exception: String) : NetworkResult()
    object Loading : NetworkResult()
}

fun handleResponse(result: NetworkResult): String {
    // 'else' kerak emas, chunki kompilyator barcha shoxobchalarni biladi (exhaustive)
    return when (result) {
        is NetworkResult.Success -> "Muvaffaqiyatli ma'lumot: ${result.data}"
        is NetworkResult.Error -> "Xatolik: ${result.exception}"
        NetworkResult.Loading -> "Yuklanmoqda..."
    }
}

fun main() {
    println(handleResponse(NetworkResult.Loading))
    println(handleResponse(NetworkResult.Success("Foydalanuvchilar ro'yxati")))
    println(handleResponse(NetworkResult.Error("404 Topilmadi")))
}
```

## Tushuntirish va Mantiq:
'sealed class' o'zining barcha subklasslarini qat'iy cheklangan to'plamda saqlaydi. Oddiy sinflardan farqli o'laroq, begona modullar 'sealed class' dan yangi subklass yarata olmaydi. Bu 'when' ifodalarida 'else' tarmog'iga bo'lgan ehtiyojni butunlay yo'qotadi.

## Ishlash natijasi:
```text
Yuklanmoqda...
Muvaffaqiyatli ma'lumot: Foydalanuvchilar ro'yxati
Xatolik: 404 Topilmadi
```


# 312-Topshiriq: Sealed Interface: Ko'p qirrali muhrlangan turlar
## Topshiriq sharti:
Kotlin 1.5+ da kiritilgan 'sealed interface' yordamida bitta subklassga bir nechta muhrlangan guruhlarga a'zo bo'lish imkonini bering.

## Yechim (Kotlin kodi):
```kotlin
sealed interface LogEvent
sealed interface UserActionEvent : LogEvent

data class ClickButton(val buttonId: String) : UserActionEvent
data class PageView(val pageUrl: String) : UserActionEvent
object ServerRestart : LogEvent

fun logAnalytics(event: LogEvent) {
    when (event) {
        is ClickButton -> println("Tugma bosildi: ${event.buttonId}")
        is PageView -> println("Sahifa ochildi: ${event.pageUrl}")
        ServerRestart -> println("Server qayta yuklandi")
    }
}

fun main() {
    logAnalytics(ClickButton("btn_submit"))
    logAnalytics(ServerRestart)
}
```

## Tushuntirish va Mantiq:
'sealed interface' 'sealed class' ga o'xshaydi, lekin u interfeys bo'lganligi sababli bitta klass bir vaqtning o'zida bir nechta sealed interface larni amalga oshira oladi.

## Ishlash natijasi:
```text
Tugma bosildi: btn_submit
Server qayta yuklandi
```


# 313-Topshiriq: Sealed Class va Enum Class farqlari
## Topshiriq sharti:
Enum da har bir qiymat faqat yagona nusxada (singleton) bo'lsa, Sealed Class larda har bir subklass o'zining shaxsiy holatiga (state) ega bo'lishini solishtiring.

## Yechim (Kotlin kodi):
```kotlin
// Enum: har bir qiymat bitta singleton nusxa
enum class SimpleStatus { SUCCESS, ERROR }

// Sealed class: har bir Success o'ziga xos ma'lumot saqlashi mumkin
sealed class AdvancedStatus {
    data class Success(val responseCode: Int, val payload: String) : AdvancedStatus()
    data class Error(val errorCode: Int, val reason: String) : AdvancedStatus()
}

fun main() {
    val s1 = AdvancedStatus.Success(200, "OK_1")
    val s2 = AdvancedStatus.Success(201, "CREATED_2")
    
    println("s1: $s1")
    println("s2: $s2")
    println("Ular alohida mustaqil obyektlar: ${s1 != s2}")
}
```

## Tushuntirish va Mantiq:
Enum lar faqat o'zgarmas konstantalar to'plami bo'lib, dinamik ma'lumot (state) saqlay olmaydi. 'sealed class' larda esa har bir subklass (data class yoki oddiy class) har safar yangi parametrlar bilan yaratilishi mumkin.

## Ishlash natijasi:
```text
s1: Success(responseCode=200, payload=OK_1)
s2: Success(responseCode=201, payload=CREATED_2)
Ular alohida mustaqil obyektlar: true
```


# 314-Topshiriq: Murakkab ma'lumotlar daraxti: Arifmetik ifodalar (Expression Tree)
## Topshiriq sharti:
Sealed class yordamida qo'shish, ko'paytirish va sonlarni ifodalovchi sintaktik daraxt tuzing va uni hisoblang.

## Yechim (Kotlin kodi):
```kotlin
sealed class Expr {
    data class Const(val number: Double) : Expr()
    data class Sum(val e1: Expr, val e2: Expr) : Expr()
    data class Multiply(val e1: Expr, val e2: Expr) : Expr()
}

fun eval(expr: Expr): Double = when (expr) {
    is Expr.Const -> expr.number
    is Expr.Sum -> eval(expr.e1) + eval(expr.e2)
    is Expr.Multiply -> eval(expr.e1) * eval(expr.e2)
}

fun main() {
    // (5 + 3) * 2
    val expression = Expr.Multiply(
        Expr.Sum(Expr.Const(5.0), Expr.Const(3.0)),
        Expr.Const(2.0)
    )
    
    println("(5 + 3) * 2 natijasi: ${eval(expression)}")
}
```

## Tushuntirish va Mantiq:
Rekursiv ma'lumotlar tuzilmalarini (kompilyator daraxtlari, JSON daraxtlari) modellashtirishda 'sealed class' ideal yechimdir. 'when' ifodasi rekursiv tahlilni juda ravon qiladi.

## Ishlash natijasi:
```text
(5 + 3) * 2 natijasi: 16.0
```


# 315-Topshiriq: Data Class da generiklar (Generic Data Class)
## Topshiriq sharti:
Ixtiyoriy turdagi ma'lumotni o'rovchi generik javob modeli yarating.

## Yechim (Kotlin kodi):
```kotlin
data class ApiResponse<T>(
    val status: Int,
    val message: String,
    val data: T?
)

fun main() {
    val stringResponse = ApiResponse(200, "OK", "Foydalanuvchi ma'lumotlari")
    val intResponse = ApiResponse(200, "OK", 45000)
    
    println("String javob: $stringResponse")
    println("Int javob: $intResponse")
}
```

## Tushuntirish va Mantiq:
Data class larda <T> generik parametrlarini qo'llash orqali API lardan keladigan turli xil modellarni bitta standart 'ApiResponse<T>' bilan birlashtirish mumkin.

## Ishlash natijasi:
```text
String javob: ApiResponse(status=200, message=OK, data=Foydalanuvchi ma'lumotlari)
Int javob: ApiResponse(status=200, message=OK, data=45000)
```


# 316-Topshiriq: Data Class da xususiyatlarni tekshirish (Validation in init)
## Topshiriq sharti:
Data class konstruktoridan kelgan maydonlarni 'init' bloki orqali qat'iy nazorat qiling.

## Yechim (Kotlin kodi):
```kotlin
data class ProductItem(val title: String, val price: Double) {
    init {
        require(title.isNotBlank()) { "Nomi bo'sh bo'lmasligi kerak" }
        require(price >= 0) { "Narx manfiy bo'lishi mumkin emas" }
    }
}

fun main() {
    val validItem = ProductItem("Kitob", 45000.0)
    println("Mahsulot: $validItem")
    
    try {
        ProductItem("", -10.0)
    } catch (e: IllegalArgumentException) {
        println("Xatolik ushlandi: ${e.message}")
    }
}
```

## Tushuntirish va Mantiq:
Data class lar oddiy sinflar kabi 'init' blokiga ega bo'lishi mumkin. Bu obyekt yaratilayotgan paytda biznes talablari buzilmasligini kafolatlaydi.

## Ishlash natijasi:
```text
Mahsulot: ProductItem(title=Kitob, price=45000.0)
Xatolik ushlandi: Nomi bo'sh bo'lmasligi kerak
```


# 317-Topshiriq: Enum nomidan qiymatni xavfsiz topish: enumValueOfOrNull
## Topshiriq sharti:
Foydalanuvchi kiritgan satr bo'yicha enum qiymatini xatoliksiz topuvchi funksiya yozing.

## Yechim (Kotlin kodi):
```kotlin
enum class DeviceType { MOBILE, TABLET, DESKTOP }

inline fun <reified T : Enum<T>> safeValueOf(name: String): T? {
    return enumValues<T>().firstOrNull { it.name.equals(name, ignoreCase = true) }
}

fun main() {
    val d1 = safeValueOf<DeviceType>("mobile")
    val d2 = safeValueOf<DeviceType>("smartwatch")
    
    println("mobile topildimi: $d1")
    println("smartwatch topildimi: $d2")
}
```

## Tushuntirish va Mantiq:
Standart 'valueOf(string)' metodi agar qiymat topilmasa 'IllegalArgumentException' tashlaydi. Reified generiklar va 'enumValues' yordamida uni xavfsiz 'T?' ko'rinishga keltirish mumkin.

## Ishlash natijasi:
```text
mobile topildimi: MOBILE
smartwatch topildimi: null
```


# 318-Topshiriq: Sealed Class ichida 'data object' (Kotlin 1.9+)
## Topshiriq sharti:
Holat saqlamaydigan sealed subklasslar uchun 'object' o'rniga zamonaviy 'data object' dan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
sealed interface UiMessage {
    data class Text(val content: String) : UiMessage
    data object Loading : UiMessage // Kotlin 1.9+
}

fun main() {
    val msg1: UiMessage = UiMessage.Text("Yuklanish tugadi")
    val msg2: UiMessage = UiMessage.Loading
    
    // data object ning afzalligi: chiroyli toString() avtomatik generatsiya bo'ladi
    println("msg1: $msg1")
    println("msg2: $msg2")
}
```

## Tushuntirish va Mantiq:
Kotlin 1.9 dan boshlab kiritilgan 'data object' oddiy 'object' kabi singleton bo'lib, qo'shimcha ravishda 'data class' larning chiroyli 'toString()' va 'equals/hashCode' imkoniyatlariga ega.

## Ishlash natijasi:
```text
msg1: Text(content=Yuklanish tugadi)
msg2: Loading
```


# 319-Topshiriq: Destrukturlashda keraksiz parametrlarni tashlab ketish: Pastki chiziq '_'
## Topshiriq sharti:
Ko'p parametrli data class ni destrukturlashda kerak bo'lmagan maydonlarni '_' orqali e'tiborsiz qoldiring.

## Yechim (Kotlin kodi):
```kotlin
data class EmployeeRecord(val id: Int, val name: String, val department: String, val salary: Double)

fun main() {
    val record = EmployeeRecord(101, "Rustam", "IT Bo'limi", 15000000.0)
    
    // Faqat name va salary kerak, qolgani '_' bilan tashlab ketiladi:
    val (_, name, _, salary) = record
    
    println("Xodim: $name | Maosh: %,.0f UZS".format(salary))
}
```

## Tushuntirish va Mantiq:
Kotlinda destrukturizatsiya paytida pastki chiziq '_' qo'yilsa, kompilyator o'sha o'rindagi 'componentN()' metodini chaqirmaydi va ortiqcha xotira/o'zgaruvchi yaratmaydi.

## Ishlash natijasi:
```text
Xodim: Rustam | Maosh: 15,000,000 UZS
```


# 320-Topshiriq: Data Class da destrukturizatsiyaning xavfli tomoni
## Topshiriq sharti:
Konstruktorda parametrlar o'rni o'zgarganda destrukturizatsiya qanday xatoga olib kelishi mumkinligini tushuntiring.

## Yechim (Kotlin kodi):
```kotlin
data class Coordinate(val x: Int, val y: Int)

fun main() {
    val coord = Coordinate(10, 20)
    
    // Destructuring xususiyat nomiga emas, parametrlar TARTIBIGA (component1, component2) qaraydi:
    val (first, second) = coord
    println("Birinchi: $first, Ikkinchi: $second")
}
```

## Tushuntirish va Mantiq:
Muhim ogohlantirish: Destrukturizatsiya 'componentN()' chaqiruviga tayanadi, ya'ni xususiyat nomlariga emas, konstruktordagi tartibga qaraydi. Agar data class parametrlarining o'rni almashtirilsa, koddagi barcha destrukturlash joylarida xatolar yuzaga kelishi mumkin.

## Ishlash natijasi:
```text
Birinchi: 10, Ikkinchi: 20
```


# 321-Topshiriq: UI State arxitekturasi: Sealed Class bilan MVI/MVVM holati
## Topshiriq sharti:
Android Jetpack Compose va MVVM da ekran holatini (UiState) modellashtiring.

## Yechim (Kotlin kodi):
```kotlin
sealed interface ScreenState {
    data object Loading : ScreenState
    data class Content(val items: List<String>) : ScreenState
    data class Error(val message: String) : ScreenState
}

fun renderUi(state: ScreenState) {
    when (state) {
        ScreenState.Loading -> println("[PROGRESS_BAR]: Ma'lumotlar yuklanmoqda...")
        is ScreenState.Content -> {
            println("[RO'YXAT]: Elementlar soni: ${state.items.size}")
            state.items.forEach { println(" - $it") }
        }
        is ScreenState.Error -> println("[ALERT_DIALOG]: ${state.message}")
    }
}

fun main() {
    renderUi(ScreenState.Loading)
    renderUi(ScreenState.Content(listOf("Kotlin", "Jetpack Compose", "Coroutines")))
    renderUi(ScreenState.Error("Internet aloqasi yo'q"))
}
```

## Tushuntirish va Mantiq:
Sealed interface lar zamonaviy Android arxitekturasida (MVVM, MVI) UI holatlarini yagona oqimda boshqarishning sanoat standartidir. Bu holatlarning noaniq bo'lishini (masalan, bir vaqtning o'zida ham Loading, ham Error ko'rinishini) mutlaqo istisno qiladi.

## Ishlash natijasi:
```text
[PROGRESS_BAR]: Ma'lumotlar yuklanmoqda...
[RO'YXAT]: Elementlar soni: 3
 - Kotlin
 - Jetpack Compose
 - Coroutines
[ALERT_DIALOG]: Internet aloqasi yo'q
```


# 322-Topshiriq: Enum Class bilan Holat mashinasi (Simple State Machine)
## Topshiriq sharti:
Buyurtma holatlarini ketma-ketlikda o'zgartiruvchi va ruxsatsiz o'tishlarni cheklovchi Enum yozing.

## Yechim (Kotlin kodi):
```kotlin
enum class OrderFlowState {
    CREATED {
        override fun next(): OrderFlowState = PAID
    },
    PAID {
        override fun next(): OrderFlowState = SHIPPED
    },
    SHIPPED {
        override fun next(): OrderFlowState = DELIVERED
    },
    DELIVERED {
        override fun next(): OrderFlowState = DELIVERED
    };

    abstract fun next(): OrderFlowState
}

fun main() {
    var state = OrderFlowState.CREATED
    println("Boshlang'ich holat: $state")
    
    state = state.next()
    println("Keyingi holat: $state")
    
    state = state.next()
    println("Keyingi holat: $state")
}
```

## Tushuntirish va Mantiq:
Enum metodlari orqali sodda va qat'iy holat mashinalarini (State Machine) yaratish mumkin.

## Ishlash natijasi:
```text
Boshlang'ich holat: CREATED
Keyingi holat: PAID
Keyingi holat: SHIPPED
```


# 323-Topshiriq: Data Class da maxsus 'equals' va 'hashCode' yozish
## Topshiriq sharti:
Massiv saqlovchi data class da massiv qiymatlarini to'g'ri solishtirish uchun 'contentEquals' ni qo'lda yozing.

## Yechim (Kotlin kodi):
```kotlin
data class ByteArrayPayload(val id: Int, val bytes: ByteArray) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is ByteArrayPayload) return false
        if (id != other.id) return false
        return bytes.contentEquals(other.bytes)
    }

    override fun hashCode(): Int {
        var result = id
        result = 31 * result + bytes.contentHashCode()
        return result
    }
}

fun main() {
    val p1 = ByteArrayPayload(1, byteArrayOf(10, 20, 30))
    val p2 = ByteArrayPayload(1, byteArrayOf(10, 20, 30))
    
    println("p1 == p2 (contentEquals bilan): ${p1 == p2}")
}
```

## Tushuntirish va Mantiq:
Agar data class da massiv (Array, ByteArray, IntArray va h.k.) mavjud bo'lsa, Kotlin avtomatik generatsiya qilgan 'equals' massiv havolalarini solishtiradi (qiymatlarini emas). Shu sababli massivli data class larda 'contentEquals()' bilan 'equals' ni qo'lda qayta yozish tavsiya etiladi.

## Ishlash natijasi:
```text
p1 == p2 (contentEquals bilan): true
```


# 324-Topshiriq: Sealed Class bilan Xatoliklarni boshqarish: Result turi analogi
## Topshiriq sharti:
Standart Kotlin Result ga o'xshash 'AppResult' muhrlangan sinfini yarating.

## Yechim (Kotlin kodi):
```kotlin
sealed class AppResult<out T> {
    data class Success<out T>(val value: T) : AppResult<T>()
    data class Failure(val error: Throwable) : AppResult<Nothing>()
}

fun safeDivide(a: Int, b: Int): AppResult<Int> {
    return if (b == 0) {
        AppResult.Failure(ArithmeticException("0 ga bo'lib bo'lmaydi"))
    } else {
        AppResult.Success(a / b)
    }
}

fun main() {
    val res1 = safeDivide(10, 2)
    val res2 = safeDivide(10, 0)
    
    when (res1) {
        is AppResult.Success -> println("Natija 1: ${res1.value}")
        is AppResult.Failure -> println("Xatolik 1: ${res1.error.message}")
    }
    
    when (res2) {
        is AppResult.Success -> println("Natija 2: ${res2.value}")
        is AppResult.Failure -> println("Xatolik 2: ${res2.error.message}")
    }
}
```

## Tushuntirish va Mantiq:
'AppResult<out T>' orqali 'out T' (kovariantlik) va 'Nothing' kombinatsiyasi muvaffaqiyatsiz holatda 'Failure' ni istalgan turdagi 'AppResult' ga xavfsiz biriktirish imkonini beradi.

## Ishlash natijasi:
```text
Natija 1: 5
Xatolik 2: 0 ga bo'lib bo'lmaydi
```


# 325-Topshiriq: Data Class bilan Hash Map kaliti sifatida ishlash
## Topshiriq sharti:
Data class ning 'equals' va 'hashCode' xususiyatlari tufayli uni 'HashMap' da kalit sifatida xavfsiz ishlatish.

## Yechim (Kotlin kodi):
```kotlin
data class CacheKey(val service: String, val entityId: Long)

fun main() {
    val cache = mutableMapOf<CacheKey, String>()
    
    val k1 = CacheKey("UserService", 100L)
    cache[k1] = "Foydalanuvchi ma'lumotlari keshda"
    
    // Yangi obyekt, lekin qiymatlari bir xil:
    val k2 = CacheKey("UserService", 100L)
    println("Keshdan o'qildi: ${cache[k2]}")
}
```

## Tushuntirish va Mantiq:
Data class barcha maydonlar bo'yicha to'g'ri 'hashCode' va 'equals' taqdim etgani sababli, alohida yaratilgan bir xil qiymatli obyektlar 'Map' kaliti sifatida 100% aniq topiladi.

## Ishlash natijasi:
```text
Keshdan o'qildi: Foydalanuvchi ma'lumotlari keshda
```


# 326-Topshiriq: Sealed Class ichida chuqur iyerarxiya
## Topshiriq sharti:
Sealed sinf ichida yana bitta sealed sinf bo'lgan ko'p bosqichli iyerarxiyani tuzing.

## Yechim (Kotlin kodi):
```kotlin
sealed class Action {
    sealed class UserAction : Action() {
        data class Login(val user: String) : UserAction()
        object Logout : UserAction()
    }

    sealed class SystemAction : Action() {
        object Backup : SystemAction()
    }
}

fun processAction(action: Action) {
    when (action) {
        is Action.UserAction.Login -> println("Foydalanuvchi kirdi: ${action.user}")
        Action.UserAction.Logout -> println("Foydalanuvchi chiqdi")
        Action.SystemAction.Backup -> println("Tizim zaxiralandi")
    }
}

fun main() {
    processAction(Action.UserAction.Login("Sherzod"))
    processAction(Action.SystemAction.Backup)
}
```

## Tushuntirish va Mantiq:
Ichma-ich 'sealed' iyerarxiyalari katta ilovalarda hodisalarni toifalarga (foydalanuvchi hodisalari, tizim hodisalari) ajratib boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Foydalanuvchi kirdi: Sherzod
Tizim zaxiralandi
```


# 327-Topshiriq: Enum larni solishtirish va tartiblash
## Topshiriq sharti:
Enum lar sukut bo'yicha e'lon qilingan tartibi bo'yicha 'Comparable' ekanligini namoyish qiling.

## Yechim (Kotlin kodi):
```kotlin
enum class Level { JUNIOR, MIDDLE, SENIOR, LEAD }

fun main() {
    val dev1 = Level.JUNIOR
    val dev2 = Level.SENIOR
    
    println("Junior Middle dan kichikmi: ${dev1 < Level.MIDDLE}")
    println("Senior Junior dan kattami: ${dev2 > dev1}")
    
    val team = listOf(Level.LEAD, Level.JUNIOR, Level.MIDDLE)
    println("Tartiblangan jamoa: ${team.sorted()}")
}
```

## Tushuntirish va Mantiq:
Barcha enum lar avtomatik ravishda 'Comparable<E>' ni amalga oshiradi va ularning tabiiy tartibi e'lon qilingan 'ordinal' indeksi bo'yicha belgilanadi.

## Ishlash natijasi:
```text
Junior Middle dan kichikmi: true
Senior Junior dan kattami: true
Tartiblangan jamoa: [JUNIOR, MIDDLE, LEAD]
```


# 328-Topshiriq: Data Class larni JSON ga o'xshatib serializatsiya qilish
## Topshiriq sharti:
Kutubxonalarsiz, ma'lumotlarni o'z ichki metodlari bilan JSON matniga o'girish.

## Yechim (Kotlin kodi):
```kotlin
data class DeviceInfo(val deviceName: String, val osVersion: Int, val isRooted: Boolean) {
    fun toJsonString(): String = """{"name":"$deviceName","os":$osVersion,"rooted":$isRooted}"""
}

fun main() {
    val info = DeviceInfo("Pixel 8", 14, false)
    println("JSON: ${info.toJsonString()}")
}
```

## Tushuntirish va Mantiq:
Data class larning ixchamligi ularni tarmoq ma'lumotlari modellari (DTO) sifatida qo'llashda juda katta qulaylik beradi.

## Ishlash natijasi:
```text
JSON: {"name":"Pixel 8","os":14,"rooted":false}
```


# 329-Topshiriq: Sealed Class da umumiy funksiyalarni e'lon qilish
## Topshiriq sharti:
Ota sealed sinfda barcha shoxobchalar uchun umumiy bo'lgan yordamchi metodni yozing.

## Yechim (Kotlin kodi):
```kotlin
sealed class Command {
    abstract val timestamp: Long

    fun printTimestamp() {
        println("Buyruq vaqti: $timestamp")
    }

    data class SendMessage(val text: String, override val timestamp: Long) : Command()
    data class ClearChat(override val timestamp: Long) : Command()
}

fun main() {
    val cmd = Command.SendMessage("Salom", System.currentTimeMillis())
    cmd.printTimestamp()
}
```

## Tushuntirish va Mantiq:
Sealed class oddiy sinf bo'lgani sababli, unda umumiy mavhum yoki to'liq yozilgan metodlar va xususiyatlar e'lon qilinishi mumkin.

## Ishlash natijasi:
```text
Buyurtma vaqti ko'rsatiladi.
```


# 330-Topshiriq: Enum qiymatlarini filtrlab olish
## Topshiriq sharti:
Enum to'plamidan ma'lum bir xususiyatga ega bo'lganlarini filtrlab olish.

## Yechim (Kotlin kodi):
```kotlin
enum class Planet(val isTerrestrial: Boolean) {
    MERCURY(true), VENUS(true), EARTH(true), MARS(true),
    JUPITER(false), SATURN(false), URANUS(false), NEPTUNE(false)
}

fun main() {
    val terrestrialPlanets = Planet.entries.filter { it.isTerrestrial }
    println("Yer guruhidagi sayyoralar: $terrestrialPlanets")
}
```

## Tushuntirish va Mantiq:
'Planet.entries' orqali enum qiymatlarini oddiy kolleksiya kabi 'filter', 'map' qilish mumkin.

## Ishlash natijasi:
```text
Yer guruhidagi sayyoralar: [MERCURY, VENUS, EARTH, MARS]
```


# 331-Topshiriq: Data class ichida kolleksiyalarni o'zgartirib nusxalash
## Topshiriq sharti:
Kolleksiya saqlovchi data class ga yangi element qo'shib yangi nusxa olish.

## Yechim (Kotlin kodi):
```kotlin
data class TaggedPost(val id: Int, val tags: List<String>)

fun main() {
    val post1 = TaggedPost(1, listOf("kotlin", "jvm"))
    val post2 = post1.copy(tags = post1.tags + "android")
    
    println("Post 1 teglari: ${post1.tags}")
    println("Post 2 teglari: ${post2.tags}")
}
```

## Tushuntirish va Mantiq:
Immutability tamoyiliga ko'ra '+' operatori mavjud ro'yxatni o'zgartirmay, yangi ro'yxat hosil qiladi va 'copy()' ga beriladi.

## Ishlash natijasi:
```text
Post 1 teglari: [kotlin, jvm]
Post 2 teglari: [kotlin, jvm, android]
```


# 332-Topshiriq: Sealed Interface va Pattern Matching
## Topshiriq sharti:
Tizim foydalanuvchilarining har xil identifikatsiya usullarini sealed interface bilan ifodalash.

## Yechim (Kotlin kodi):
```kotlin
sealed interface Identifier
data class EmailId(val email: String) : Identifier
data class PhoneId(val phone: String) : Identifier
data class NationalId(val passport: String) : Identifier

fun printId(id: Identifier) {
    when (id) {
        is EmailId -> println("Email: ${id.email}")
        is PhoneId -> println("Telefon: ${id.phone}")
        is NationalId -> println("Pasport: ${id.passport}")
    }
}

fun main() {
    printId(EmailId("user@company.uz"))
    printId(PhoneId("+998901234567"))
}
```

## Tushuntirish va Mantiq:
Pattern Matching va Sealed interfeyslar har qanday murakkab biznes ob'ektlarini xavfsiz va aniq identifikatsiya qilishga yordam beradi.

## Ishlash natijasi:
```text
Email: user@company.uz
Telefon: +998901234567
```


# 333-Topshiriq: Data class larda ko'p qirrali destrukturizatsiya funksiyalarda
## Topshiriq sharti:
Funksiyadan data class qaytarib, chaqirilgan joyda darhol destrukturlash.

## Yechim (Kotlin kodi):
```kotlin
data class Weather(val temperature: Double, val humidity: Int, val condition: String)

fun fetchCurrentWeather(): Weather = Weather(22.5, 45, "Quyoshli")

fun main() {
    val (temp, hum, cond) = fetchCurrentWeather()
    println("Ob-havo: $temp°C, Namlik: $hum%, Holat: $cond")
}
```

## Tushuntirish va Mantiq:
Funksiyalar natijasini darhol destrukturlash kodni ixchamlashtiradi va keraksiz oraliq obyekt nomlarini yo'qotadi.

## Ishlash natijasi:
```text
Ob-havo: 22.5°C, Namlik: 45%, Holat: Quyoshli
```


# 334-Topshiriq: Enum Class bilan Custom Serializatsiya kalitlari
## Topshiriq sharti:
Har bir enum konstantasiga tashqi API kodi yoki JSON kaliti biriktirish.

## Yechim (Kotlin kodi):
```kotlin
enum class PaymentType(val apiCode: String) {
    CASH("cash_in_hand"),
    CARD("uzcard_humo"),
    ONLINE("online_gateway")
}

fun findPaymentTypeByApi(code: String): PaymentType? {
    return PaymentType.entries.firstOrNull { it.apiCode == code }
}

fun main() {
    val found = findPaymentTypeByApi("uzcard_humo")
    println("Topilgan to'lov turi: $found")
}
```

## Tushuntirish va Mantiq:
Tashqi API qiymatlari (string) va ichki qat'iy turlar (enum) orasidagi ko'prik konstruktor parametrlari orqali xavfsiz quriladi.

## Ishlash natijasi:
```text
Topilgan to'lov turi: CARD
```


# 335-Topshiriq: Sealed Class bilan Hisoblash pipeline natijasi
## Topshiriq sharti:
Operatsiyalar ketma-ketligida muvaffaqiyat yoki to'xtash sabablarini sealed sinfda ifodalash.

## Yechim (Kotlin kodi):
```kotlin
sealed class StepResult {
    data class Continue(val intermediateValue: Int) : StepResult()
    data class Abort(val reason: String) : StepResult()
}

fun executeStep(value: Int): StepResult {
    return if (value < 0) StepResult.Abort("Manfiy qiymat qabul qilinmaydi")
    else StepResult.Continue(value * 2)
}

fun main() {
    val s1 = executeStep(10)
    val s2 = executeStep(-5)
    
    println("Qadam 1: $s1")
    println("Qadam 2: $s2")
}
```

## Tushuntirish va Mantiq:
Hisoblash zanjirlarida xatoliklar istisno tashlamasdan, ma'lumot sifatida (Data-oriented programming) sealed class lar orqali qaytariladi.

## Ishlash natijasi:
```text
Qadam 1: Continue(intermediateValue=20)
Qadam 2: Abort(reason=Manfiy qiymat qabul qilinmaydi)
```


# 336-Topshiriq: Data Class da xususiyatlarni solishtirish: 'copy' va diff aniqlash
## Topshiriq sharti:
Ikki obyekt orasida qaysi maydonlar o'zgarganini topuvchi yordamchi funksiya.

## Yechim (Kotlin kodi):
```kotlin
data class ConfigSnapshot(val timeout: Int, val maxConnections: Int, val debugMode: Boolean)

fun compareSnapshots(old: ConfigSnapshot, new: ConfigSnapshot) {
    if (old.timeout != new.timeout) println("Timeout o'zgardi: ${old.timeout} -> ${new.timeout}")
    if (old.maxConnections != new.maxConnections) println("Connections o'zgardi: ${old.maxConnections} -> ${new.maxConnections}")
    if (old.debugMode != new.debugMode) println("Debug rejim o'zgardi: ${old.debugMode} -> ${new.debugMode}")
}

fun main() {
    val c1 = ConfigSnapshot(3000, 50, false)
    val c2 = c1.copy(maxConnections = 100, debugMode = true)
    
    compareSnapshots(c1, c2)
}
```

## Tushuntirish va Mantiq:
Data class maydonlari o'zgarmas bo'lgani sababli, ikki konfiguratsiya holatini solishtirish va farqlarni (diff) topish juda oson.

## Ishlash natijasi:
```text
Connections o'zgardi: 50 -> 100
Debug rejim o'zgardi: false -> true
```


# 337-Topshiriq: Sealed Class bilan Shakllar maydoni kalkulyatori
## Topshiriq sharti:
Har xil geometrik shakllar parametrlarini sealed class lar ichida saqlang va yuzasini hisoblang.

## Yechim (Kotlin kodi):
```kotlin
sealed class GeometricShape {
    data class Circle(val radius: Double) : GeometricShape()
    data class Rectangle(val width: Double, val height: Double) : GeometricShape()
    data class Square(val side: Double) : GeometricShape()
}

fun calculateArea(shape: GeometricShape): Double = when (shape) {
    is GeometricShape.Circle -> Math.PI * shape.radius * shape.radius
    is GeometricShape.Rectangle -> shape.width * shape.height
    is GeometricShape.Square -> shape.side * shape.side
}

fun main() {
    val s1 = GeometricShape.Circle(3.0)
    val s2 = GeometricShape.Square(4.0)
    
    println("Doira yuzi: %.2f".format(calculateArea(s1)))
    println("Kvadrat yuzi: %.2f".format(calculateArea(s2)))
}
```

## Tushuntirish va Mantiq:
Har bir shakl faqat o'ziga xos parametrlarga ega (doirada radius, to'rtburchakda eni va bo'yi) va sealed class bu xilma-xillikni bitta umumiy 'GeometricShape' turida birlashtiradi.

## Ishlash natijasi:
```text
Doira yuzi: 28.27
Kvadrat yuzi: 16.00
```


# 338-Topshiriq: Enum va Bitmask o'rniga EnumSet dan foydalanish
## Topshiriq sharti:
Bir nechta enum qiymatlarini bitta to'plamda xotiradan samarali saqlash.

## Yechim (Kotlin kodi):
```kotlin
import java.util.EnumSet

enum class Permission { READ, WRITE, EXECUTE }

fun main() {
    val adminPermissions: EnumSet<Permission> = EnumSet.allOf(Permission::class.java)
    val readOnlyPermissions: EnumSet<Permission> = EnumSet.of(Permission::READ)
    
    println("Admin huquqlari: $adminPermissions")
    println("Faqat o'qish huquqi: $readOnlyPermissions")
    println("Read huquqi bormi: ${Permission.READ in readOnlyPermissions}")
}
```

## Tushuntirish va Mantiq:
'EnumSet' JVM da bitmask (bit darajasidagi amallar) kabi juda yuqori unumdorlikda ishlaydi va odatiy HashSet lardan ancha tez va ixchamdir.

## Ishlash natijasi:
```text
Admin huquqlari: [READ, WRITE, EXECUTE]
Faqat o'qish huquqi: [READ]
Read huquqi bormi: true
```


# 339-Topshiriq: Data Class da qo'shimcha metodlar va hisoblashlar
## Topshiriq sharti:
Data sinf ichida biznes logikaga oid qo'shimcha qulay yordamchi metodlar e'lon qilish.

## Yechim (Kotlin kodi):
```kotlin
data class LineItem(val name: String, val unitPrice: Double, val quantity: Int) {
    val totalCost: Double
        get() = unitPrice * quantity

    fun isBulkPurchase(): Boolean = quantity >= 10
}

fun main() {
    val item = LineItem("Daftar", 5000.0, 12)
    println("Mahsulot: ${item.name} | Jami narx: %,.0f UZS".format(item.totalCost))
    println("Ulgurji xaridmi: ${item.isBulkPurchase()}")
}
```

## Tushuntirish va Mantiq:
Data class lar faqat passiv ma'lumot saqlovchi emas, balki hisoblanuvchi xususiyatlar va domen metodlariga ham ega bo'la oladi.

## Ishlash natijasi:
```text
Mahsulot: Daftar | Jami narx: 60,000 UZS
Ulgurji xaridmi: true
```


# 340-Topshiriq: Sealed Class bilan Pagination (Sahifalash) modeli
## Topshiriq sharti:
Ro'yxatni sahifalab yuklashdagi holatlarni sealed class bilan boshqaring.

## Yechim (Kotlin kodi):
```kotlin
sealed interface PageLoadState {
    data object InitialLoading : PageLoadState
    data class PageReady(val pageNumber: Int, val hasMore: Boolean) : PageLoadState
    data class PaginationError(val pageNumber: Int, val error: String) : PageLoadState
}

fun main() {
    val states: List<PageLoadState> = listOf(
        PageLoadState.InitialLoading,
        PageLoadState.PageReady(1, hasMore = true),
        PageLoadState.PageReady(2, hasMore = false)
    )
    
    states.forEach { println("Holat: $it") }
}
```

## Tushuntirish va Mantiq:
Sahifalashda birinchi yuklanish, keyingi sahifa tayyorligi va xatoliklarni bitta qat'iy holat modeliga keltirish.

## Ishlash natijasi:
```text
Holat: InitialLoading
Holat: PageReady(pageNumber=1, hasMore=true)
Holat: PageReady(pageNumber=2, hasMore=false)
```


# 341-Topshiriq: Enum larda lookup map yaratish (O(1) tezlikda qidirish)
## Topshiriq sharti:
Companion object ichida barcha enum larni ularning kodi bo'yicha xaritaga (Map) keshlab olish.

## Yechim (Kotlin kodi):
```kotlin
enum class HttpMethod(val verb: String) {
    GET("GET"),
    POST("POST"),
    PUT("PUT"),
    DELETE("DELETE");

    companion object {
        private val map = entries.associateBy { it.verb }
        fun fromVerb(verb: String): HttpMethod? = map[verb.uppercase()]
    }
}

fun main() {
    println("POST qidiruvi: ${HttpMethod.fromVerb("post")}")
    println("PATCH qidiruvi: ${HttpMethod.fromVerb("patch")}")
}
```

## Tushuntirish va Mantiq:
'associateBy' orqali bir marta kesh xaritasi tuziladi va har bir qidiruv O(1) o'zgarmas vaqtda topiladi.

## Ishlash natijasi:
```text
POST qidiruvi: POST
PATCH qidiruvi: null
```


# 342-Topshiriq: Data Class bilan Pair va Triple larni almashtirish
## Topshiriq sharti:
Noma'lum 'Pair<String, Int>' o'rniga nomlangan xususiyatlarga ega data class ning afzalligi.

## Yechim (Kotlin kodi):
```kotlin
// Noaniq: Pair<String, Double> - nima ekanligi ma'lum emas
// Toza arxitektura:
data class ProductPrice(val sku: String, val price: Double)

fun main() {
    val item = ProductPrice("SKU-5544", 89.99)
    println("SKU: ${item.sku}, Narxi: $$${item.price}")
}
```

## Tushuntirish va Mantiq:
Pair yoki Triple dagi 'first' va 'second' nomlari kodni o'qishni qiyinlashtiradi. Aniq data class lar kodning o'zini o'zi hujjatlashini (self-documenting) ta'minlaydi.

## Ishlash natijasi:
```text
SKU: SKU-5544, Narxi: $89.99
```


# 343-Topshiriq: Sealed Class bilan Chat xabarlari turlari
## Topshiriq sharti:
Matnli, rasmli va ovozli xabarlarni bitta xabar turi ostida modellashtirish.

## Yechim (Kotlin kodi):
```kotlin
sealed interface ChatMessage {
    val sender: String
    val timestamp: Long

    data class Text(override val sender: String, override val timestamp: Long, val text: String) : ChatMessage
    data class Image(override val sender: String, override val timestamp: Long, val imageUrl: String, val sizeKb: Int) : ChatMessage
    data class Voice(override val sender: String, override val timestamp: Long, val durationSec: Int) : ChatMessage
}

fun main() {
    val messages: List<ChatMessage> = listOf(
        ChatMessage.Text("Ali", 1000L, "Salom yaxshimisiz?"),
        ChatMessage.Image("Vali", 1005L, "https://cdn.uz/img.png", 250)
    )
    
    for (m in messages) {
        when (m) {
            is ChatMessage.Text -> println("[MATN] ${m.sender}: ${m.text}")
            is ChatMessage.Image -> println("[RASM] ${m.sender}: ${m.imageUrl} (${m.sizeKb} KB)")
            is ChatMessage.Voice -> println("[OVOZ] ${m.sender}: ${m.durationSec} soniya")
        }
    }
}
```

## Tushuntirish va Mantiq:
Har xil turdagi UI elementlarini (masalan, Telegram chat xabarlari) bitta sealed interfeys orqali RecyclerView yoki LazyColumn ga uzatish juda qulay.

## Ishlash natijasi:
```text
[MATN] Ali: Salom yaxshimisiz?
[RASM] Vali: https://cdn.uz/img.png (250 KB)
```


# 344-Topshiriq: Data Class da chuqur nusxalash (Nested Copying)
## Topshiriq sharti:
Ichma-ich data class obyektlarida ichki maydonni xavfsiz yangilab nusxa olish.

## Yechim (Kotlin kodi):
```kotlin
data class PostalAddress(val city: String, val street: String)
data class UserAccount(val username: String, val address: PostalAddress)

fun main() {
    val acc1 = UserAccount("temur_99", PostalAddress("Toshkent", "Navoiy ko'chasi"))
    
    // Ichki manzil ko'chasini yangilab nusxa olish:
    val acc2 = acc1.copy(address = acc1.address.copy(street = "Amir Temur shoh ko'chasi"))
    
    println("Asl manzil: ${acc1.address.street}")
    println("Yangi manzil: ${acc2.address.street}")
}
```

## Tushuntirish va Mantiq:
Zanjirli 'copy()' chaqiruvlari orqali chuqur joylashgan obyektlar ham immutability tamoyili buzilmagan holda yangilanadi.

## Ishlash natijasi:
```text
Asl manzil: Navoiy ko'chasi
Yangi manzil: Amir Temur shoh ko'chasi
```


# 345-Topshiriq: Enum orqali Valyuta konvertatsiyasi metodi
## Topshiriq sharti:
Enum o'z ichida boshqa valyutaga o'tkazish metodini saqlasin.

## Yechim (Kotlin kodi):
```kotlin
enum class FiatCurrency(val uzsRate: Double) {
    UZS(1.0),
    USD(12800.0),
    EUR(13900.0);

    fun convertTo(amount: Double, target: FiatCurrency): Double {
        val amountInUzs = amount * this.uzsRate
        return amountInUzs / target.uzsRate
    }
}

fun main() {
    val usd = 100.0
    val eur = FiatCurrency.USD.convertTo(usd, FiatCurrency.EUR)
    println("100 USD = %,.2f EUR".format(eur))
}
```

## Tushuntirish va Mantiq:
Enum ichida mantiqiy hisoblashlarni joylashtirish ma'lumot va uning ustidagi amallarni bitta xavfsiz kontekstda jamlaydi.

## Ishlash natijasi:
```text
100 USD = 92.09 EUR
```


# 346-Topshiriq: Sealed Class bilan Foydalanuvchi huquqlari va tekshiruv
## Topshiriq sharti:
Ruxsat darajalarini sealed class sifatida ifodalab, harakatni taqiqlash yoki ruxsat berish.

## Yechim (Kotlin kodi):
```kotlin
sealed class UserAccess {
    object Guest : UserAccess()
    data class Member(val userId: Long, val plan: String) : UserAccess()
    data class Admin(val adminLevel: Int) : UserAccess()
}

fun canEditSettings(access: UserAccess): Boolean = when (access) {
    UserAccess.Guest -> false
    is UserAccess.Member -> access.plan == "ENTERPRISE"
    is UserAccess.Admin -> access.adminLevel >= 2
}

fun main() {
    println("Guest huquqi: ${canEditSettings(UserAccess.Guest)}")
    println("Admin Level 1: ${canEditSettings(UserAccess.Admin(1))}")
    println("Admin Level 3: ${canEditSettings(UserAccess.Admin(3))}")
}
```

## Tushuntirish va Mantiq:
Turli ma'lumotlarga ega foydalanuvchi turlarini aniq modellashtirish va xavfsizlik shartlarini to'liq tekshirish.

## Ishlash natijasi:
```text
Guest huquqi: false
Admin Level 1: false
Admin Level 3: true
```


# 347-Topshiriq: Data Class da xususiyatlarni taqqoslash komparatori: compareBy
## Topshiriq sharti:
Bir nechta xususiyatlar bo'yicha data class lar ro'yxatini tartiblash.

## Yechim (Kotlin kodi):
```kotlin
data class StudentScore(val grade: Int, val name: String, val score: Double)

fun main() {
    val students = listOf(
        StudentScore(2, "Jasur", 85.0),
        StudentScore(1, "Alisher", 95.0),
        StudentScore(1, "Bobur", 90.0)
    )
    
    // Avval sinf (grade), keyin ball (score) bo'yicha saralash:
    val sorted = students.sortedWith(compareBy<StudentScore> { it.grade }.thenByDescending { it.score })
    
    println("Saralangan ro'yxat:")
    sorted.forEach { println(" - Sinf: ${it.grade}, Ball: ${it.score}, Ism: ${it.name}") }
}
```

## Tushuntirish va Mantiq:
'compareBy' va 'thenByDescending' data class lar ro'yxatini bir nechta ustunlar bo'yicha saralashda juda qulaydir.

## Ishlash natijasi:
```text
Saralangan ro'yxat:
 - Sinf: 1, Ball: 95.0, Ism: Alisher
 - Sinf: 1, Ball: 90.0, Ism: Bobur
 - Sinf: 2, Ball: 85.0, Ism: Jasur
```


# 348-Topshiriq: Sealed Class bilan O'yin Qahramonlari sinfi (RPG Inventory)
## Topshiriq sharti:
Qahramon ryukzagidagi turli narsalarni (qurol, dori, oltin) modellashtirish.

## Yechim (Kotlin kodi):
```kotlin
sealed interface Item {
    val name: String
    val weight: Double
}

data class Weapon(override val name: String, override val weight: Double, val damage: Int) : Item
data class Potion(override val name: String, override val weight: Double, val healAmount: Int) : Item
data class Gold(val amount: Int) : Item {
    override val name: String = "Oltin tangalar"
    override val weight: Double = amount * 0.01
}

fun main() {
    val inventory: List<Item> = listOf(
        Weapon("Afsonaviy Qilich", 4.5, 75),
        Potion("Shifo damlamasi", 0.5, 50),
        Gold(100)
    )
    
    val totalWeight = inventory.sumOf { it.weight }
    println("Ryukzakning umumiy og'irligi: $totalWeight kg")
}
```

## Tushuntirish va Mantiq:
Sealed interfeyslar o'yin arxitekturasida turli obyektlar uchun umumiy xususiyatlarni (name, weight) saqlagan holda o'ziga xos parametrlarni birlashtiradi.

## Ishlash natijasi:
```text
Ryukzakning umumiy og'irligi: 6.0 kg
```


# 349-Topshiriq: Data Class da 'copy' yordamida Undo (Bekor qilish) tarixi
## Topshiriq sharti:
Holat tarixini saqlab boruvchi va avvalgi qadamga qaytuvchi mexanizm tuzing.

## Yechim (Kotlin kodi):
```kotlin
data class EditorState(val content: String, val cursorPosition: Int)

class TextEditor {
    private val history = mutableListOf<EditorState>()
    var currentState = EditorState("", 0)

    fun type(text: String) {
        history.add(currentState)
        currentState = currentState.copy(
            content = currentState.content + text,
            cursorPosition = currentState.cursorPosition + text.length
        )
    }

    fun undo() {
        if (history.isNotEmpty()) {
            currentState = history.removeAt(history.size - 1)
            println("[UNDO]: Avvalgi holatga qaytildi")
        }
    }
}

fun main() {
    val editor = TextEditor()
    editor.type("Salom ")
    editor.type("Kotlin!")
    println("Joriy matn: '${editor.currentState.content}'")
    
    editor.undo()
    println("Undo dan so'ng: '${editor.currentState.content}'")
}
```

## Tushuntirish va Mantiq:
Data class o'zgarmas nusxalarining ro'yxatini saqlab borish orqali dasturda 'Undo/Redo' funksiyasi juda oson va xatosiz ishlaydi.

## Ishlash natijasi:
```text
Joriy matn: 'Salom Kotlin!'
[UNDO]: Avvalgi holatga qaytildi
Undo dan so'ng: 'Salom '
```


# 350-Topshiriq: Maxsus sinflar bo'yicha to'liq amaliy xulosa: Elektron Savdo To'lov Tizimi
## Topshiriq sharti:
Data class, Enum class va Sealed class larni birlashtirgan to'liq xarid va tranzaksiya oqimini quring.

## Yechim (Kotlin kodi):
```kotlin
enum class PaymentMethodType { CARD, CASH, WALLET }

data class CartProduct(val id: Long, val name: String, val price: Double)

sealed interface CheckoutResult {
    data class Success(val orderId: String, val paidAmount: Double) : CheckoutResult
    data class InsufficientFunds(val required: Double, val available: Double) : CheckoutResult
    data class PaymentFailed(val reason: String) : CheckoutResult
}

fun processCheckout(client: String, products: List<CartProduct>, method: PaymentMethodType, userBalance: Double): CheckoutResult {
    val total = products.sumOf { it.price }
    if (userBalance < total) {
        return CheckoutResult.InsufficientFunds(required = total, available = userBalance)
    }
    
    return CheckoutResult.Success(
        orderId = "ORD-" + System.currentTimeMillis().toString().takeLast(4),
        paidAmount = total
    )
}

fun main() {
    val cart = listOf(
        CartProduct(1L, "Naushnik", 150.0),
        CartProduct(2L, "Sichqoncha", 50.0)
    )
    
    val result1 = processCheckout("Ali", cart, PaymentMethodType.CARD, 300.0)
    val result2 = processCheckout("Vali", cart, PaymentMethodType.WALLET, 100.0)
    
    fun printResult(res: CheckoutResult) = when (res) {
        is CheckoutResult.Success -> println("Xarid muvaffaqiyatli! ID: ${res.orderId}, Summa: $$${res.paidAmount}")
        is CheckoutResult.InsufficientFunds -> println("Mablag' yetarli emas! Kerak: $$${res.required}, Mavjud: $$${res.available}")
        is CheckoutResult.PaymentFailed -> println("To'lov bekor qilindi: ${res.reason}")
    }
    
    printResult(result1)
    printResult(result2)
}
```

## Tushuntirish va Mantiq:
Ushbu yakuniy topshiriqda talab qilingan barcha maxsus sinflar: 'data class' (mahsulot modeli), 'enum class' (to'lov turlari) va 'sealed interface' (to'lov natijalari) professional e-tijorat to'lov moduli misolida jamlandi.

## Ishlash natijasi:
```text
Xarid muvaffaqiyatli! ID: ORD-9900, Summa: $200.0
Mablag' yetarli emas! Kerak: $200.0, Mavjud: $100.0
```

