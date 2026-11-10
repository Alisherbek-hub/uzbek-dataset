# 451-Topshiriq: Scope funksiyalari umumiy jadvali va farqlari
## Topshiriq sharti:
Kotlindagi 5 ta scope funksiyasining (let, run, with, apply, also) kontekst obyekti (this vs it) va qaytish qiymatini ko'rsatuvchi dastur yozing.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val sample = "Kotlin"

    // 1. let: 'it', lambda natijasi qaytadi
    val letRes = sample.let { it.length }

    // 2. run: 'this', lambda natijasi qaytadi
    val runRes = sample.run { length }

    // 3. with: 'this', lambda natijasi qaytadi (oddiy funksiya)
    val withRes = with(sample) { uppercase() }

    // 4. apply: 'this', kontekst obyekti (sample) qaytadi
    val applyRes = sample.apply { println("apply ichida: $this") }

    // 5. also: 'it', kontekst obyekti (sample) qaytadi
    val alsoRes = sample.also { println("also ichida: $it") }

    println("let: $letRes, run: $runRes, with: $withRes, apply: $applyRes, also: $alsoRes")
}
```

## Tushuntirish va Mantiq:
Kotlinda 5 ta scope funksiyasi mavjud bo'lib, ular ikki asosiy mezon bo'yicha farqlanadi: 1) Kontekst obyektiga murojaat usuli ('this' yoki 'it'); 2) Qaytish qiymati (kontekst obyektining o'zi yoki lambda blokining yakuniy natijasi).

## Ishlash natijasi:
```text
apply ichida: Kotlin
also ichida: Kotlin
let: 6, run: 6, with: KOTLIN, apply: Kotlin, also: Kotlin
```


# 452-Topshiriq: 'let' funksiyasi: Null tekshiruvi va xavfsiz chaqiruv (?.)
## Topshiriq sharti:
Nullable o'zgaruvchini faqat null bo'lmagandagina bajarish uchun '?.let' dan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
fun printUserEmail(email: String?) {
    email?.let { validEmail ->
        println("Email mavjud: $validEmail")
        println("Domen: ${validEmail.substringAfter("@")}")
    } ?: println("Email kiritilmagan.")
}

fun main() {
    printUserEmail("anvar@pochta.uz")
    printUserEmail(null)
}
```

## Tushuntirish va Mantiq:
'?.let' idiomasi Kotlin dasturchilarining eng sevimli usulidir. Agar obyekt null bo'lmasa, blok ichida u avtomatik ravishda non-null o'zgaruvchi ('validEmail' yoki 'it') sifatida qabul qilinadi.

## Ishlash natijasi:
```text
Email mavjud: anvar@pochta.uz
Domen: pochta.uz
Email kiritilmagan.
```


# 453-Topshiriq: 'let' bilan ma'lumotlarni o'zgartirish (Transformation)
## Topshiriq sharti:
Satrni butun songa o'tkazib, uning kvadratini hisoblovchi 'let' zanjirini tuzing.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val rawNumber = "25"
    
    val square = rawNumber.let { it.toInt() }.let { it * it }
    println("'$rawNumber' ning kvadrati: $square")
}
```

## Tushuntirish va Mantiq:
'let' lambda natijasini qaytarganligi sababli, u ma'lumotlarni bir turdan ikkinchi turga bosqichma-bosqich o'tkazishda (mapping) juda qulaydir.

## Ishlash natijasi:
```text
'25' ning kvadrati: 625
```


# 454-Topshiriq: 'apply' funksiyasi: Obyektni initsializatsiya qilish (Builder pattern analogi)
## Topshiriq sharti:
Yangi yaratilgan obyekt xususiyatlarini 'apply { ... }' orqali sozlab, tayyor obyektni qabul qiling.

## Yechim (Kotlin kodi):
```kotlin
class DatabaseConnection {
    var host: String = ""
    var port: Int = 0
    var database: String = ""
}

fun main() {
    val connection = DatabaseConnection().apply {
        host = "192.168.1.50"
        port = 5432
        database = "production_db"
    }

    println("Baza: ${connection.host}:${connection.port}/${connection.database}")
}
```

## Tushuntirish va Mantiq:
'apply' funksiyasi kontekst obyektiga 'this' orqali murojaat qiladi va blok yakunida o'sha o'zgartirilgan obyektning o'zini qaytaradi. Bu Android da View lar, Intent lar va sozlamalarni bir joyda chiroyli initsializatsiya qilishda asosiy vositadir.

## Ishlash natijasi:
```text
Baza: 192.168.1.50:5432/production_db
```


# 455-Topshiriq: 'also' funksiyasi: Qo'shimcha ta'sirlar (Side-effects) va Logging
## Topshiriq sharti:
Asosiy hisoblash oqimini to'xtatmasdan oraliq logging yozish uchun 'also' dan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
fun calculateDiscountedPrice(price: Double, discountPercent: Double): Double {
    return (price * (1 - discountPercent / 100.0)).also { finalPrice ->
        println("[LOG]: Asl narx: $$price, Chegirma: $discountPercent%, Yakuniy: $$finalPrice")
    }
}

fun main() {
    val result = calculateDiscountedPrice(200.0, 15.0)
    println("Qaytarilgan summa: $$result")
}
```

## Tushuntirish va Mantiq:
'also' xuddi 'apply' kabi obyektning o'zini qaytaradi, lekin kontekst obyektiga 'it' orqali murojaat qiladi. U asosan logging, oraliq tekshiruvlar yoki yon ta'sirlar (side-effects) qo'shish uchun ishlatiladi.

## Ishlash natijasi:
```text
[LOG]: Asl narx: $200.0, Chegirma: 15.0%, Yakuniy: $170.0
Qaytarilgan summa: $170.0
```


# 456-Topshiriq: 'run' funksiyasi: Obyekt ustida amallar bajarib natija hisoblash
## Topshiriq sharti:
Obyekt parametrlaridan foydalanib xulosaviy hisobot hosil qilishda 'run' ni qo'llang.

## Yechim (Kotlin kodi):
```kotlin
class ServerService(val host: String, val port: Int) {
    fun ping(): Boolean = true
}

fun main() {
    val service = ServerService("api.uz", 443)

    val statusMessage = service.run {
        val isAlive = ping()
        "Server: $host:$port holati: " + if (isAlive) "Faol (Online)" else "O'chiq"
    }

    println(statusMessage)
}
```

## Tushuntirish va Mantiq:
'run' kontekst obyektiga 'this' orqali murojaat qiladi va lambda natijasini qaytaradi. Bu bir vaqtning o'zida obyekt xususiyatlarini o'qish va natijaviy qiymatni hisoblab chiqarish uchun eng yaxshi tanlovdir.

## Ishlash natijasi:
```text
Server: api.uz:443 holati: Faol (Online)
```


# 457-Topshiriq: Argumentsiz 'run' bloki: Mahalliy doira (Local Scope) yaratish
## Topshiriq sharti:
Hech qanday obyektsiz, shunchaki o'zgaruvchilar ko'rinish sohasini chegaralash uchun 'run { ... }' dan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val totalDiscount = run {
        val baseDiscount = 5.0
        val loyaltyBonus = 2.5
        val promoBonus = 3.0
        baseDiscount + loyaltyBonus + promoBonus
    }

    println("Jami chegirma: $totalDiscount%")
}
```

## Tushuntirish va Mantiq:
Argumentsiz 'run { ... }' bloki oddiy kod guruhini bajaradi va oxirgi ifoda natijasini qaytaradi. Unda e'lon qilingan vaqtinchalik o'zgaruvchilar blok tugashi bilan xotiradan tozalanadi.

## Ishlash natijasi:
```text
Jami chegirma: 10.5%
```


# 458-Topshiriq: 'with' funksiyasi: Mavjud obyekt metodlarini takrorlarsiz chaqirish
## Topshiriq sharti:
Bir xil obyekt nomini qayta-qayta yozmaslik uchun 'with(object) { ... }' dan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
class Canvas {
    fun drawLine(x1: Int, y1: Int, x2: Int, y2: Int) = println("Chiziq: ($x1,$y1) -> ($x2,$y2)")
    fun drawCircle(x: Int, y: Int, r: Int) = println("Doira markazi: ($x,$y), radius: $r")
    fun render() = "Chizma tayyor"
}

fun main() {
    val canvas = Canvas()

    val result = with(canvas) {
        drawLine(0, 0, 10, 10)
        drawCircle(5, 5, 20)
        render()
    }

    println("Natija: $result")
}
```

## Tushuntirish va Mantiq:
'with' kengaytma funksiya emas, balki oddiy standart funksiyadir: 'with(receiver) { ... }'. U mavjud non-null obyekt a'zolarini uning nomisiz ('this' orqali) guruhlab chaqirishda ishlatiladi.

## Ishlash natijasi:
```text
Chiziq: (0,0) -> (10,10)
Doira markazi: (5,5), radius: 20
Natija: Chizma tayyor
```


# 459-Topshiriq: this vs it: To'g'ri tanlov va nomlash imkoniyati
## Topshiriq sharti:
'this' ga asoslangan (run, apply) va 'it' ga asoslangan (let, also) funksiyalarni taqqoslang.

## Yechim (Kotlin kodi):
```kotlin
class Profile(var name: String, var city: String)

fun main() {
    val p = Profile("Aziz", "Samarqand")

    // 'it' ni o'zimiz xohlagan nom bilan nomlash mumkin:
    p.let { user ->
        println("Foydalanuvchi: ${user.name}, Shahar: ${user.city}")
    }

    // 'this' esa o'zgaruvchisiz to'g'ridan-to'g'ri xususiyatlarga kiradi:
    p.apply {
        name = "Azizbek"
        city = "Toshkent"
    }

    println("Yangilangan profil: ${p.name}, ${p.city}")
}
```

## Tushuntirish va Mantiq:
Agar obyekt metodlari chaqirilayotgan bo'lsa, 'this' (apply, run) qulay. Agar obyekt boshqa bir funksiyaga argument sifatida uzatilayotgan bo'lsa yoki o'zgaruvchiga aniq nom berish zarur bo'lsa, 'it' (let, also) afzalroqdir.

## Ishlash natijasi:
```text
Foydalanuvchi: Aziz, Shahar: Samarqand
Yangilangan profil: Azizbek, Toshkent
```


# 460-Topshiriq: Scope funksiyalarini zanjirlash (Chaining Scope Functions)
## Topshiriq sharti:
apply, also va let funksiyalarini bitta toza oqimda birlashtiring.

## Yechim (Kotlin kodi):
```kotlin
class OrderBuilder {
    var orderId: String = ""
    var itemsCount: Int = 0
}

fun main() {
    val summary = OrderBuilder()
        .apply {
            orderId = "ORD-7788"
            itemsCount = 4
        }
        .also {
            println("[AUDIT]: Buyurtma #${it.orderId} xotirada yaratildi.")
        }
        .let {
            "Tayyorlangan buyurtma: ID=${it.orderId}, Mahsulotlar: ${it.itemsCount} ta"
        }

    println(summary)
}
```

## Tushuntirish va Mantiq:
Scope funksiyalarini o'rinli zanjirlash obyektni sozlash (apply), audit qilish (also) va natijani shakllantirishni (let) juda chiroyli va o'qishli quvurga aylantiradi.

## Ishlash natijasi:
```text
[AUDIT]: Buyurtma #ORD-7788 xotirada yaratildi.
Tayyorlangan buyurtma: ID=ORD-7788, Mahsulotlar: 4 ta
```


# 461-Topshiriq: Ichma-ich Scope funksiyalari va 'this' chalkashligi
## Topshiriq sharti:
Ichma-ich 'apply' yoki 'run' ishlatilganda tashqi va ichki 'this' larni yorliq (@label) orqali ajratish.

## Yechim (Kotlin kodi):
```kotlin
class Window(val title: String) {
    class Button(val text: String)

    fun setup() {
        val btn = Button("OK").apply {
            // text - Button ning text xususiyati
            // Window ning title xususiyatiga murojaat:
            println("Tugma: $text oyna sarlavhasi: ${this@Window.title} ga qo'yildi")
        }
    }
}

fun main() {
    val win = Window("Asosiy Dastur")
    win.setup()
}
```

## Tushuntirish va Mantiq:
Ichma-ich 'this' kontekstlarida tashqi sinf yoki scope ga murojaat qilish uchun 'this@OuterName' yorlig'idan foydalaniladi. Kod tushunarsiz bo'lib ketmasligi uchun chuqur ichma-ich scope funksiyalaridan qochish tavsiya etiladi.

## Ishlash natijasi:
```text
Tugma: OK oyna sarlavhasi: Asosiy Dastur ga qo'yildi
```


# 462-Topshiriq: Shartli boshqaruv: takeIf bilan let kombinatsiyasi
## Topshiriq sharti:
Faqat ma'lum bir shart bajarilgandagina amalni davom ettirish uchun 'takeIf { ... }?.let { ... }' dan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
fun processBonus(score: Int) {
    score.takeIf { it >= 80 }?.let { validScore ->
        val bonus = validScore * 10
        println("A'lo ball ($validScore)! Bonus berildi: $$bonus")
    } ?: println("Ball ($score) bonus olish uchun yetarli emas.")
}

fun main() {
    processBonus(95)
    processBonus(60)
}
```

## Tushuntirish va Mantiq:
'takeIf' va 'let' kombinatsiyasi an'anaviy 'if (score >= 80)' bloklarining toza va ifodali funksional muqobilidir.

## Ishlash natijasi:
```text
A'lo ball (95)! Bonus berildi: $950
Ball (60) bonus olish uchun yetarli emas.
```


# 463-Topshiriq: Kolleksiyalarni sozlashda 'apply' ning qo'llanilishi
## Topshiriq sharti:
Yangi ro'yxat yoki to'plamni yaratib, unga elementlar qo'shish va darhol qaytarish.

## Yechim (Kotlin kodi):
```kotlin
fun getInitializedList(): List<String> {
    return mutableListOf<String>().apply {
        add("Olma")
        add("Anor")
        add("Uzum")
    }
}

fun main() {
    val fruits = getInitializedList()
    println("Meva ro'yxati: $fruits")
}
```

## Tushuntirish va Mantiq:
'mutableListOf<T>().apply { add(...) }' orqali vaqtinchalik o'zgaruvchi e'lon qilmasdan bitta ifodada to'ldirilgan to'plamni qaytarish mumkin.

## Ishlash natijasi:
```text
Meva ro'yxati: [Olma, Anor, Uzum]
```


# 464-Topshiriq: Vaqtinchalik o'zgaruvchilarni saqlashda 'also' afzalligi
## Topshiriq sharti:
Ikki o'zgaruvchi qiymatini uchinchi vaqtinchalik 'temp' o'zgaruvchisisiz almashtirish (Swap).

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    var a = 10
    var b = 20

    // also yordamida bitta qatorda swap qilish:
    a = b.also { b = a }

    println("a = $a, b = $b")
}
```

## Tushuntirish va Mantiq:
'b.also { b = a }' ifodasida 'b' ning eski qiymati also ning natijasi sifatida saqlanib, 'a' ga biriktiriladi, ichkarida esa 'b' ga 'a' ning qiymati yoziladi.

## Ishlash natijasi:
```text
a = 20, b = 10
```


# 465-Topshiriq: Fayl yoki Oqimlar bilan ishlashda 'use' va 'apply'
## Topshiriq sharti:
StringBuilder ni 'apply' orqali to'ldirib, natijani olish.

## Yechim (Kotlin kodi):
```kotlin
fun generateInvoiceText(client: String, amount: Double): String {
    return StringBuilder().apply {
        append("MIJOZ: $client
")
        append("SUMMA: $$amount
")
        append("HOLAT: TO'LANDI
")
    }.toString()
}

fun main() {
    val invoice = generateInvoiceText("Sherzod", 450.0)
    println(invoice)
}
```

## Tushuntirish va Mantiq:
StringBuilder ustida 'apply' qo'llash har safar 'sb.append()' deb yozish o'rniga to'g'ridan-to'g'ri 'append()' chaqirish qulayligini beradi.

## Ishlash natijasi:
```text
MIJOZ: Sherzod
SUMMA: $450.0
HOLAT: TO'LANDI
```


# 466-Topshiriq: Xavfsiz konfiguratsiya: Nullable ob'ektda 'run' chaqiruvi
## Topshiriq sharti:
Agar obyekt null bo'lsa null qaytaruvchi '?.' va 'run' kombinatsiyasi.

## Yechim (Kotlin kodi):
```kotlin
class CustomerInfo(val name: String, val balance: Double)

fun formatCustomer(info: CustomerInfo?): String {
    return info?.run {
        "Mijoz: $name, Balans: %,.2f UZS".format(balance)
    } ?: "Mijoz haqida ma'lumot yo'q"
}

fun main() {
    println(formatCustomer(CustomerInfo("Bobur", 500000.0)))
    println(formatCustomer(null))
}
```

## Tushuntirish va Mantiq:
'?.run' null tekshiruvini 'run' ning 'this' qulayligi bilan birlashtiradi.

## Ishlash natijasi:
```text
Mijoz: Bobur, Balans: 500,000.00 UZS
Mijoz haqida ma'lumot yo'q
```


# 467-Topshiriq: Shartli logging: also yordamida oraliq natijani konsolga chiqarish
## Topshiriq sharti:
Kolleksiya ustidagi operatsiyalar zanjirida har bir oraliq holatni chop etish.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val numbers = listOf(5, 12, 8, 21, 3)

    val finalResult = numbers
        .filter { it > 5 }
        .also { println("[FILTERDAN SO'NG]: $it") }
        .map { it * 2 }
        .also { println("[MAPDAN SO'NG]: $it") }
        .sum()

    println("Yakuniy yig'indi: $finalResult")
}
```

## Tushuntirish va Mantiq:
'also' kolleksiyalar zanjirini buzmasdan debug ma'lumotlarini kuzatib borishda eng yaxshi yechimdir.

## Ishlash natijasi:
```text
[FILTERDAN SO'NG]: [12, 8, 21]
[MAPDAN SO'NG]: [24, 16, 42]
Yakuniy yig'indi: 82
```


# 468-Topshiriq: Scope funksiyalarda qaytish qiymati: Ob'ekt qaytishi vs Natija qaytishi
## Topshiriq sharti:
apply (obyekt) va run (natija) orasidagi qaytish qiymati farqini bitta sinfda namoyish qiling.

## Yechim (Kotlin kodi):
```kotlin
class UserDraft(var username: String)

fun main() {
    val draft = UserDraft("dasturchi_01")

    val applyReturn: UserDraft = draft.apply {
        username = "dasturchi_02"
    }

    val runReturn: String = draft.run {
        "Foydalanuvchi nomi: $username"
    }

    println("applyReturn turi: ${applyReturn::class.simpleName}")
    println("runReturn turi: ${runReturn::class.simpleName}")
}
```

## Tushuntirish va Mantiq:
'apply' har doim chaqirilgan obyektning o'zini ('UserDraft') qaytaradi. 'run' esa eng oxirgi ifoda natijasini ('String') qaytaradi.

## Ishlash natijasi:
```text
applyReturn turi: UserDraft
runReturn turi: String
```


# 469-Topshiriq: Android View Binding analogi: 'with' bilan elementlarni boshqarish
## Topshiriq sharti:
UI komponentlariga qiymat biriktirishda 'with' dan foydalanish.

## Yechim (Kotlin kodi):
```kotlin
class FakeBinding {
    var titleText = ""
    var subtitleText = ""
    var isVisible = false
}

fun main() {
    val binding = FakeBinding()

    with(binding) {
        titleText = "Bosh Sahifa"
        subtitleText = "Eng so'nggi yangiliklar"
        isVisible = true
    }

    println("UI Holati: '${binding.titleText}', Ko'rinadimi: ${binding.isVisible}")
}
```

## Tushuntirish va Mantiq:
Android dasturlashda 'ViewBinding' bilan ishlashda har bir view oldiga 'binding.' so'zini yozmaslik uchun 'with(binding) { ... }' standarti qo'llaniladi.

## Ishlash natijasi:
```text
UI Holati: 'Bosh Sahifa', Ko'rinadimi: true
```


# 470-Topshiriq: Scope funksiyalari orqali xavfsiz kesh initsializatsiyasi
## Topshiriq sharti:
Kesh xaritasini 'apply' orqali to'ldirib, o'zgarmas 'Map' ga o'tkazish.

## Yechim (Kotlin kodi):
```kotlin
fun loadSystemDictionary(): Map<String, String> {
    return mutableMapOf<String, String>().apply {
        put("ERR_01", "Baza ulanish xatosi")
        put("ERR_02", "Tarmoq uzilishi")
        put("ERR_03", "Avtorizatsiya xatosi")
    }.toMap() // O'zgarmas holatga o'tkazish
}

fun main() {
    val dict = loadSystemDictionary()
    println("Kesh xatolari: ${dict["ERR_01"]}")
}
```

## Tushuntirish va Mantiq:
O'zgaruvchan to'plamni 'apply' bilan to'ldirib, '.toMap()' orqali tashqariga o'zgarmas xavfsiz Map taqdim etiladi.

## Ishlash natijasi:
```text
Kesh xatolari: Baza ulanish xatosi
```


# 471-Topshiriq: Shartli parametrlar: takeUnless bilan also kombinatsiyasi
## Topshiriq sharti:
Agar qiymat ma'lum holatda bo'lmasa xabar berish.

## Yechim (Kotlin kodi):
```kotlin
fun checkDiskSpace(freeSpaceGb: Int) {
    freeSpaceGb.takeUnless { it < 5 }?.also {
        println("[TIZIM]: Disk maydoni yetarli ($it GB).")
    } ?: println("[OGOHLANTIRISH]: Disk to'lib bormoqda!")
}

fun main() {
    checkDiskSpace(20)
    checkDiskSpace(3)
}
```

## Tushuntirish va Mantiq:
'takeUnless' shart qanoatlantirilmaganda qiymatni saqlab qoladi va 'also' bilan xavfsiz log yoziladi.

## Ishlash natijasi:
```text
[TIZIM]: Disk maydoni yetarli (20 GB).
[OGOHLANTIRISH]: Disk to'lib bormoqda!
```


# 472-Topshiriq: Scope funksiyalarda xatoliklarni ushlash (try-catch run)
## Topshiriq sharti:
runCatching standart funksiyasining scope funksiyalari bilan uyg'unligi.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val raw = "450"

    val parsed = raw.runCatching {
        toInt()
    }.getOrDefault(0)

    println("Muvaffaqiyatli son: $parsed")
}
```

## Tushuntirish va Mantiq:
'runCatching' ichki blokda istisno yuz berganda uni ushlaydi va 'getOrDefault' orqali zaxira qiymat beradi.

## Ishlash natijasi:
```text
Muvaffaqiyatli son: 450
```


# 473-Topshiriq: Shaxsiy Scope funksiyasi yozish mexanizmi
## Topshiriq sharti:
O'zingizning shaxsiy 'customApply' yoki 'customLet' funksiyangizni kengaytma sifatida yozing.

## Yechim (Kotlin kodi):
```kotlin
inline fun <T> T.customApply(block: T.() -> Unit): T {
    block()
    return this
}

class CarConfig {
    var color = "Oq"
}

fun main() {
    val car = CarConfig().customApply {
        color = "Qora"
    }

    println("Mashina rangi: ${car.color}")
}
```

## Tushuntirish va Mantiq:
Kotlindagi barcha standart scope funksiyalari aynan shu ko'rinishdagi oddiy generik inline kengaytma funksiyalardir.

## Ishlash natijasi:
```text
Mashina rangi: Qora
```


# 474-Topshiriq: Scope funksiyasi yordamida ob'ekt nusxasini o'zgartirish
## Topshiriq sharti:
Data class ning 'copy' metodini 'let' ichida ishlatish.

## Yechim (Kotlin kodi):
```kotlin
data class PlayerState(val name: String, val level: Int)

fun main() {
    val player = PlayerState("Nodir", 1)

    val updatedPlayer = player.let {
        it.copy(level = it.level + 1)
    }

    println("Eski holat: $player")
    println("Yangi holat: $updatedPlayer")
}
```

## Tushuntirish va Mantiq:
'let' ichida 'it.copy()' chaqirib, yangilangan nusxani qaytarish juda qulaydir.

## Ishlash natijasi:
```text
Eski holat: PlayerState(name=Nodir, level=1)
Yangi holat: PlayerState(name=Nodir, level=2)
```


# 475-Topshiriq: Zanjirda ob'ektni tekshirish: let va check kombinatsiyasi
## Topshiriq sharti:
Obyekt maydonlarini tekshirib, xato bo'lsa istisno tashlash.

## Yechim (Kotlin kodi):
```kotlin
class TransactionRequest(val amount: Double)

fun validateTransaction(req: TransactionRequest?) {
    req?.let {
        check(it.amount > 0) { "Summa noldan katta bo'lishi shart!" }
        println("Tranzaksiya yaroqli: $$${it.amount}")
    } ?: println("So'rov null bo'lishi mumkin emas")
}

fun main() {
    validateTransaction(TransactionRequest(150.0))
}
```

## Tushuntirish va Mantiq:
'req?.let' faqat mavjud obyekt ustida tekshiruvlarni toza o'tkazishga yordam beradi.

## Ishlash natijasi:
```text
Tranzaksiya yaroqli: $150.0
```


# 476-Topshiriq: Scope funksiyalarida ortiqcha murakkablikdan qochish qoidasi
## Topshiriq sharti:
Ketma-ket 5 ta scope funksiyasini yozish kod o'qilishini buzishini va to'g'ri yechimni ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
// NOTO'G'RI (Antipattern): haddan tashqari chigallashtirilgan scope funksiyalari
// a.let { it.run { this.also { ... } } }

// TO'G'RI: Oddiy va tushunarli yondashuv
fun processClient(name: String, email: String) {
    val cleanName = name.trim()
    val cleanEmail = email.trim().lowercase()

    println("Mijoz ro'yxatga olindi: $cleanName ($cleanEmail)")
}

fun main() {
    processClient("  Farrux  ", "  FARRUX@DEV.UZ  ")
}
```

## Tushuntirish va Mantiq:
Kotlin rasmiy tavsiyasiga ko'ra, scope funksiyalari kodni soddalashtirish uchun xizmat qilishi kerak. Agar ular kodni o'qishni qiyinlashtirsa, oddiy mahalliy o'zgaruvchilardan foydalanish lozim.

## Ishlash natijasi:
```text
Mijoz ro'yxatga olindi: Farrux (farrux@dev.uz)
```


# 477-Topshiriq: Builder obyekti bilan DSL yaratishda 'apply'
## Topshiriq sharti:
Daraxtsimon menyu obyektini 'apply' orqali yasash.

## Yechim (Kotlin kodi):
```kotlin
class MenuItem(val name: String) {
    val subItems = mutableListOf<MenuItem>()
    fun subItem(name: String, block: MenuItem.() -> Unit = {}) {
        subItems.add(MenuItem(name).apply(block))
    }
}

fun main() {
    val menu = MenuItem("Bosh Sahifa").apply {
        subItem("Fayl") {
            subItem("Yangi")
            subItem("Ochish")
        }
        subItem("Yordam")
    }

    println("Asosiy menyu: ${menu.name}, Qismlar: ${menu.subItems.map { it.name }}")
}
```

## Tushuntirish va Mantiq:
Ichma-ich 'apply' yordamida daraxtsimon menyular yoki konfiguratsiya obyektlari tabiiy hosil qilinadi.

## Ishlash natijasi:
```text
Asosiy menyu: Bosh Sahifa, Qismlar: [Fayl, Yordam]
```


# 478-Topshiriq: Shartli boshqaruv: with ichida ko'p qatorli hisoblash
## Topshiriq sharti:
Geometrik ob'ekt parametrlari bilan murakkab formula hisoblash.

## Yechim (Kotlin kodi):
```kotlin
class Cylinder(val radius: Double, val height: Double)

fun main() {
    val cylinder = Cylinder(3.0, 5.0)

    val volume = with(cylinder) {
        val baseArea = Math.PI * radius * radius
        baseArea * height
    }

    println("Silindr hajmi: %.2f".format(volume))
}
```

## Tushuntirish va Mantiq:
'with' obyektdan kerakli parametrlarni o'qib, lokal o'zgaruvchilar bilan hisoblashni toza bajaradi.

## Ishlash natijasi:
```text
Silindr hajmi: 141.37
```


# 479-Topshiriq: Scope funksiyalarda 'return' ning xavfi
## Topshiriq sharti:
Inline bo'lgan let/run ichida ehtiyotsiz qo'yilgan 'return' butun funksiyadan chiqarib yuborishini tushuntiring.

## Yechim (Kotlin kodi):
```kotlin
fun checkList(items: List<String>) {
    items.forEach { item ->
        item.let {
            if (it == "STOP") {
                println("STOP uchradi, to'xtatildi.")
                return // DIQQAT: checkList funksiyasidan to'liq chiqib ketadi!
            }
        }
        println("Element: $item")
    }
    println("Tugadi.")
}

fun main() {
    checkList(listOf("A", "B", "STOP", "C"))
}
```

## Tushuntirish va Mantiq:
Scope funksiyalari inline bo'lganligi sababli, ularning ichidagi oddiy 'return' butun tashqi funksiyani to'xtatadi. Agar faqat joriy qadamdan chiqish kerak bo'lsa, 'return@let' yoziladi.

## Ishlash natijasi:
```text
Element: A
Element: B
STOP uchradi, to'xtatildi.
```


# 480-Topshiriq: Kolleksiyalar bilan ishlashda 'also' orqali statistika yozish
## Topshiriq sharti:
Filtrlash natijasida nechta element qolganini o'sha zanjir ichida qayd etish.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val scores = listOf(45, 88, 92, 55, 74, 99)

    val passedScores = scores
        .filter { it >= 70 }
        .also { println("[STATISTIKA]: Imtihondan o'tganlar soni: ${it.size} ta") }
        .sortedDescending()

    println("Yuqori ballar: $passedScores")
}
```

## Tushuntirish va Mantiq:
'also' operatsiyalar oqimini buzmagan holda oraliq statistikani chiqarish imkonini beradi.

## Ishlash natijasi:
```text
[STATISTIKA]: Imtihondan o'tganlar soni: 4 ta
Yuqori ballar: [99, 92, 88, 74]
```


# 481-Topshiriq: Shaxsiy 'customRun' funksiyasi yaratish
## Topshiriq sharti:
Receiver ustida 'run' funksiyasining analogini tuzing.

## Yechim (Kotlin kodi):
```kotlin
inline fun <T, R> T.customRun(block: T.() -> R): R {
    return block()
}

fun main() {
    val text = "Kotlin 2.0"
    val lengthPlusFive = text.customRun {
        length + 5
    }

    println("Natija: $lengthPlusFive")
}
```

## Tushuntirish va Mantiq:
'customRun' receiver parametrida 'T.() -> R' qabul qiladi va uning natijasini qaytaradi.

## Ishlash natijasi:
```text
Natija: 15
```


# 482-Topshiriq: Scope funksiyalari bilan DTO dan Domen modeliga o'tish
## Topshiriq sharti:
Tashqi API modelini domenga o'tkazishda 'run' dan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
data class UserApiDto(val first_name: String, val last_name: String, val birth_year: Int)
data class UserDomainModel(val fullName: String, val age: Int)

fun mapToDomain(dto: UserApiDto): UserDomainModel {
    return dto.run {
        UserDomainModel(
            fullName = "$first_name $last_name",
            age = 2026 - birth_year
        )
    }
}

fun main() {
    val apiData = UserApiDto("Jamshid", "Karimov", 2000)
    val domainData = mapToDomain(apiData)

    println("Domen model: $domainData")
}
```

## Tushuntirish va Mantiq:
'dto.run { ... }' orqali har safar 'dto.first_name', 'dto.last_name' deb yozmasdan to'g'ridan-to'g'ri yangi model yasash mumkin.

## Ishlash natijasi:
```text
Domen model: UserDomainModel(fullName=Jamshid Karimov, age=26)
```


# 483-Topshiriq: Shaxsiy 'customAlso' funksiyasi yozish
## Topshiriq sharti:
Obyekt ustida amal bajarib o'zini qaytaruvchi 'also' ning analogi.

## Yechim (Kotlin kodi):
```kotlin
inline fun <T> T.customAlso(block: (T) -> Unit): T {
    block(this)
    return this
}

fun main() {
    val message = "Salom Dunyo".customAlso {
        println("Matn uzunligi: ${it.length}")
    }

    println("Qaytarilgan matn: $message")
}
```

## Tushuntirish va Mantiq:
'customAlso' argument sifatida '(T) -> Unit' qabul qilib, yakunda 'this' ni qaytaradi.

## Ishlash natijasi:
```text
Matn uzunligi: 11
Qaytarilgan matn: Salom Dunyo
```


# 484-Topshiriq: Scope funksiyalar bilan vaqtinchalik hisoblagich keshini tozalash
## Topshiriq sharti:
Obyekt ma'lumotlarini o'qib, keshni tozalab natijani qaytarish.

## Yechim (Kotlin kodi):
```kotlin
class SessionDataStore {
    private val buffer = mutableListOf("Log 1", "Log 2")

    fun flushAndGetLogs(): List<String> {
        return buffer.toList().also {
            buffer.clear()
            println("[KESH TOZALANDI]")
        }
    }
}

fun main() {
    val store = SessionDataStore()
    val logs = store.flushAndGetLogs()

    println("Olingan loglar: $logs")
    println("Qayta olish (bo'sh bo'lishi kerak): ${store.flushAndGetLogs()}")
}
```

## Tushuntirish va Mantiq:
'buffer.toList().also { buffer.clear() }' andozasi xotiradagi ma'lumotlarni o'qib, darhol keshni tozalashda juda qulaydir.

## Ishlash natijasi:
```text
[KESH TOZALANDI]
Olingan loglar: [Log 1, Log 2]
[KESH TOZALANDI]
Qayta olish (bo'sh bo'lishi kerak): []
```


# 485-Topshiriq: Scope funksiyalari va Destrukturizatsiya
## Topshiriq sharti:
Pair yoki data class obyektini 'let' ichida destrukturlab olish.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val userCoordinates = Pair(41.311081, 69.240562)

    val formatted = userCoordinates.let { (lat, lon) ->
        "Kenglik: $lat, Uzunlik: $lon"
    }

    println(formatted)
}
```

## Tushuntirish va Mantiq:
'let { (a, b) -> ... }' destrukturizatsiya bilan ajoyib birlashadi va parametrlarga alohida o'zgaruvchilar ochmasdan ishlash imkonini beradi.

## Ishlash natijasi:
```text
Kenglik: 41.311081, Uzunlik: 69.240562
```


# 486-Topshiriq: Scope funksiyalarida oraliq tekshiruvlar: require va let
## Topshiriq sharti:
Obyekt maydonlarini validatsiya qilib, so'ngra ishlatish.

## Yechim (Kotlin kodi):
```kotlin
class PaymentPayload(val amount: Double, val currency: String)

fun processPayment(payload: PaymentPayload?) {
    payload?.let {
        require(it.amount > 0) { "Summa xato" }
        require(it.currency.isNotBlank()) { "Valyuta kiritilmagan" }
        println("To'lov bajarildi: $$it.amount (${it.currency})")
    } ?: println("Payload mavjud emas")
}

fun main() {
    processPayment(PaymentPayload(50.0, "USD"))
}
```

## Tushuntirish va Mantiq:
Null xavfsizligi va 'require' tekshiruvlari '?.let' ichida tartibli joylashadi.

## Ishlash natijasi:
```text
To'lov bajarildi: $50.0 (USD)
```


# 487-Topshiriq: Scope funksiyalar yordamida chuqur obyektlarni yangilash
## Topshiriq sharti:
Ichki maydonlarni 'apply' orqali o'zgartirish.

## Yechim (Kotlin kodi):
```kotlin
class CarEngine { var horsepower: Int = 0 }
class MotorVehicle { val engine = CarEngine() }

fun main() {
    val vehicle = MotorVehicle().apply {
        engine.apply {
            horsepower = 150
        }
    }

    println("Dvigatel quvvati: ${vehicle.engine.horsepower} ot kuchi")
}
```

## Tushuntirish va Mantiq:
Bir nechta obyektlarning xususiyatlarini bitta initsializatsiya blokida tartibli sozlash.

## Ishlash natijasi:
```text
Dvigatel quvvati: 150 ot kuchi
```


# 488-Topshiriq: Scope funksiyalarda shartli qiymat: if-else o'rnida let
## Topshiriq sharti:
Nullable stringni tozalab, bo'sh bo'lmasa ishlatish.

## Yechim (Kotlin kodi):
```kotlin
fun getCleanedName(input: String?): String {
    return input?.trim()?.takeIf { it.isNotEmpty() }?.let {
        "Foydalanuvchi: $it"
    } ?: "Noma'lum foydalanuvchi"
}

fun main() {
    println(getCleanedName("  Sarvar  "))
    println(getCleanedName("   "))
    println(getCleanedName(null))
}
```

## Tushuntirish va Mantiq:
'trim()', 'takeIf', 'let' va '?:' kombinatsiyasi matnlarni xavfsiz tozalashning eng professional usulidir.

## Ishlash natijasi:
```text
Foydalanuvchi: Sarvar
Noma'lum foydalanuvchi
Noma'lum foydalanuvchi
```


# 489-Topshiriq: Shaxsiy 'customWith' funksiyasi yaratish
## Topshiriq sharti:
Standart 'with' funksiyasining ishlash mexanizmini shaxsiy dasturlash orqali amalga oshiring.

## Yechim (Kotlin kodi):
```kotlin
inline fun <T, R> customWith(receiver: T, block: T.() -> R): R {
    return receiver.block()
}

fun main() {
    val sb = StringBuilder("Boshlanish")
    val result = customWith(sb) {
        append(" -> O'rtasi")
        append(" -> Yakun")
        toString()
    }

    println(result)
}
```

## Tushuntirish va Mantiq:
'customWith' birinchi parametrda receiver qabul qilib, uning ustida 'block()' ni chaqiradi va natijani qaytaradi.

## Ishlash natijasi:
```text
Boshlanish -> O'rtasi -> Yakun
```


# 490-Topshiriq: Scope funksiyalari orqali ma'lumotlar bazasi tranzaksiyasini yopish
## Topshiriq sharti:
Ulanishni 'apply' bilan sozlab, 'also' bilan commit qilish.

## Yechim (Kotlin kodi):
```kotlin
class MockDbConnection {
    var isConnected = false
    fun commit() = println("Tranzaksiya commit qilindi.")
}

fun main() {
    val conn = MockDbConnection()
        .apply { isConnected = true }
        .also { it.commit() }

    println("Ulanish holati: ${conn.isConnected}")
}
```

## Tushuntirish va Mantiq:
Obyekt holatini o'zgartirish va darhol tegishli operatsiyani chaqirish.

## Ishlash natijasi:
```text
Tranzaksiya commit qilindi.
Ulanish holati: true
```


# 491-Topshiriq: Scope funksiyalarda xotirani tejash: Inline xarakteri
## Topshiriq sharti:
Barcha scope funksiyalari (let, run, with, apply, also) inline ekanligi va bytecodedagi ko'rinishini tushuntiring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    // Bu kodlar bayt-kodda hech qanday lambda yoki sinf yaratmaydi:
    val a = 10.let { it * 2 }
    val b = 20.run { this + 5 }

    println("a = $a, b = $b")
}
```

## Tushuntirish va Mantiq:
Kotlin standart kutubxonasidagi barcha 5 ta scope funksiyasi 'inline' qilib yozilgan. Ular ish vaqtida (runtime) hech qanday qo'shimcha obyekt ajratmaydi va to'g'ridan-to'g'ri oddiy Java kodi kabi tez ishlaydi.

## Ishlash natijasi:
```text
a = 20, b = 25
```


# 492-Topshiriq: Scope funksiyalari bilan ko'p bosqichli hisoblash
## Topshiriq sharti:
Har bir bosqichni 'let' orqali keyingisiga uzatish.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val total = 100
        .let { it + 50 }  // 150
        .let { it * 2 }   // 300
        .let { it - 20 }  // 280

    println("Ko'p bosqichli hisoblash: $total")
}
```

## Tushuntirish va Mantiq:
'let' zanjirlari orqali hisoblash qadamlarini qat'iy ketma-ketlikda tashkil etish mumkin.

## Ishlash natijasi:
```text
Ko'p bosqichli hisoblash: 280
```


# 493-Topshiriq: Scope funksiyalarda obyektni vaqtinchalik o'zgartirish va tiklash
## Topshiriq sharti:
Obyekt parametrini o'zgartirib amal bajarish, so'ngra eski holatiga qaytarish.

## Yechim (Kotlin kodi):
```kotlin
class AppTheme { var isDarkMode = false }

fun main() {
    val theme = AppTheme()
    println("Boshlang'ich: ${theme.isDarkMode}")

    val screenshot = theme.apply { isDarkMode = true }.run {
        "Qorong'i mavzuda skrinshot olindi"
    }.also {
        theme.isDarkMode = false // Tiklash
    }

    println(screenshot)
    println("Tiklangandan so'ng: ${theme.isDarkMode}")
}
```

## Tushuntirish va Mantiq:
Scope funksiyalari o'zgarishlar, operatsiyalar va resursni tiklashni bitta ifodada birlashtiradi.

## Ishlash natijasi:
```text
Boshlang'ich: false
Qorong'i mavzuda skrinshot olindi
Tiklangandan so'ng: false
```


# 494-Topshiriq: Scope funksiyalari bilan JSON ob'ekti shakllantirish
## Topshiriq sharti:
Map ni 'apply' orqali to'ldirib, JSON formatida chop etish.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val jsonMap = mutableMapOf<String, Any>().apply {
        put("user_id", 101)
        put("username", "alisher_dev")
        put("is_active", true)
    }

    println("JSON ma'lumotlari: $jsonMap")
}
```

## Tushuntirish va Mantiq:
Lug'at parametrlarini toza va ixcham to'ldirish.

## Ishlash natijasi:
```text
JSON ma'lumotlari: {user_id=101, username=alisher_dev, is_active=true}
```


# 495-Topshiriq: Scope funksiyalarda matn shablonlari bilan ishlash
## Topshiriq sharti:
Hisoblangan qiymatni darhol matnga aylantirish.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val orderSummary = 450.0.run {
        val tax = this * 0.12
        val total = this + tax
        "Oraliq: $$this, Soliq: $$tax, Jami: $$total"
    }

    println(orderSummary)
}
```

## Tushuntirish va Mantiq:
'run' ichida hisob-kitoblar o'tkazilib, formatlangan matn qaytariladi.

## Ishlash natijasi:
```text
Oraliq: $450.0, Soliq: $54.0, Jami: $504.0
```


# 496-Topshiriq: Scope funksiyalari bilan shartli qayta urinish (Retry helper)
## Topshiriq sharti:
Natija qoniqarsiz bo'lsa 'let' orqali zaxirani tekshirish.

## Yechim (Kotlin kodi):
```kotlin
fun fetchPrimary(): String? = null
fun fetchBackup(): String = "Zaxira ma'lumot"

fun main() {
    val result = fetchPrimary()?.let {
        "Asosiy: $it"
    } ?: run {
        "Zaxiradan olindi: ${fetchBackup()}"
    }

    println(result)
}
```

## Tushuntirish va Mantiq:
'?.let { ... } ?: run { ... }' idiomasi asosiy manba null bo'lganda zaxira manbani ishga tushirishning eng mashhur andozasidir.

## Ishlash natijasi:
```text
Zaxiradan olindi: Zaxira ma'lumot
```


# 497-Topshiriq: Scope funksiyalari orqali UI elementlarini ko'rsatish/yashirish
## Topshiriq sharti:
Holatga qarab 'apply' orqali xususiyatlarni moslash.

## Yechim (Kotlin kodi):
```kotlin
class UiCard {
    var isVisible = false
    var text = ""
}

fun updateCard(card: UiCard, hasError: Boolean, errorMsg: String) {
    card.apply {
        if (hasError) {
            isVisible = true
            text = errorMsg
        } else {
            isVisible = false
            text = ""
        }
    }
}

fun main() {
    val card = UiCard()
    updateCard(card, true, "Xatolik yuz berdi!")
    println("Card ko'rinishi: ${card.isVisible}, Matn: '${card.text}'")
}
```

## Tushuntirish va Mantiq:
UI elementining bir nechta xususiyatini bitta 'apply' ichida shartli yangilash.

## Ishlash natijasi:
```text
Card ko'rinishi: true, Matn: 'Xatolik yuz berdi!'
```


# 498-Topshiriq: Scope funksiyalari bilan ro'yxatni saralash va logging
## Topshiriq sharti:
Kolleksiyani saralab, darhol natijasini 'also' orqali qayd etish.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val items = listOf("Zafar", "Ali", "Kamola", "Bobur")

    val sortedItems = items.sorted().also {
        println("[SARALANDI]: ${it.joinToString(", ")}")
    }

    println("Birinchi o'rindagi: ${sortedItems.first()}")
}
```

## Tushuntirish va Mantiq:
'also' orqali yangi yaratilgan saralangan ro'yxatni konsolga xavfsiz chiqarish.

## Ishlash natijasi:
```text
[SARALANDI]: Ali, Bobur, Kamola, Zafar
Birinchi o'rindagi: Ali
```


# 499-Topshiriq: Scope funksiyalari orqali Xotira boshqaruvi va Resurslarni bo'shatish
## Topshiriq sharti:
Obyektdan foydalanib, 'also' bilan resursni xavfsiz tozalash.

## Yechim (Kotlin kodi):
```kotlin
class TemporaryBuffer {
    val data = mutableListOf("A", "B", "C")
    fun clear() = data.clear()
}

fun main() {
    val count = TemporaryBuffer().run {
        data.size
    }

    println("O'qilgan elementlar soni: $count")
}
```

## Tushuntirish va Mantiq:
'run' yordamida obyekt yaratilib, kerakli qiymat olinadi va obyekt o'z doirasidan chiqib avtomatik xotiradan tozalanadi.

## Ishlash natijasi:
```text
O'qilgan elementlar soni: 3
```


# 500-Topshiriq: Scope funksiyalari bo'yicha to'liq amaliy xulosa: Mijoz Buyurtmasini Shakllantirish
## Topshiriq sharti:
let, run, with, apply va also funksiyalarini bitta yaxlit korporativ buyurtma servisida birlashtiring.

## Yechim (Kotlin kodi):
```kotlin
class Customer(val name: String, val email: String?)
class OrderItem(val name: String, val price: Double)
class Invoice {
    var invoiceId = ""
    var recipient = ""
    var totalAmount = 0.0
    val items = mutableListOf<OrderItem>()
}

fun processCheckout(customer: Customer?, rawItems: List<OrderItem>): String {
    // 1. let: Nullable mijozni tekshirish va xavfsiz boshlash
    return customer?.let { validCustomer ->
        
        // 2. apply: Yangi invoys obyektini initsializatsiya qilish
        Invoice().apply {
            invoiceId = "INV-2026-99"
            recipient = validCustomer.name
            items.addAll(rawItems)
            totalAmount = items.sumOf { it.price }
        }
        // 3. also: Audit log yozish (Side-effect)
        .also { inv ->
            println("[AUDIT]: Invoys #${inv.invoiceId} (${inv.recipient}) yaratildi. Jami: $$inv.totalAmount")
        }
        // 4. run: Invoys parametrlaridan foydalanib yakuniy hisobot matnini hosil qilish
        .run {
            // 5. with: Ichki hisobot detallarini formatlash
            with(this) {
                """
                ==============================
                RASMIY HISOB-FAKTURA
                ID: $invoiceId
                Mijoz: $recipient
                Email: ${validCustomer.email ?: "Mavjud emas"}
                Jami mahsulotlar: ${items.size} ta
                Yakuniy to'lov: $$totalAmount
                ==============================
                """.trimIndent()
            }
        }
    } ?: "XATOLIK: Mijoz ma'lumotlari topilmadi!"
}

fun main() {
    val client = Customer("Diyorbek Rahimov", "diyor@startup.uz")
    val items = listOf(
        OrderItem("Veb Dizayn", 500.0),
        OrderItem("Kotlin Backend", 800.0)
    )

    val invoiceReport = processCheckout(client, items)
    println(invoiceReport)
}
```

## Tushuntirish va Mantiq:
Ushbu yakuniy topshiriqda talab qilingan barcha 5 ta scope funksiyasi (let, apply, also, run, with) o'zining aniq maqsadiga muvofiq, bitta mukammal hisob-faktura shakllantirish jarayonida amaliy uyg'unlashdi.

## Ishlash natijasi:
```text
[AUDIT]: Invoys #INV-2026-99 (Diyorbek Rahimov) yaratildi. Jami: $1300.0
==============================
RASMIY HISOB-FAKTURA
ID: INV-2026-99
Mijoz: Diyorbek Rahimov
Email: diyor@startup.uz
Jami mahsulotlar: 2 ta
Yakuniy to'lov: $1300.0
==============================
```

