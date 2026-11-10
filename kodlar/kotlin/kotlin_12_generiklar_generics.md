# 551-Topshiriq: Generik sinf (Generic Class) asoslari
## Topshiriq sharti:
Har qanday turdagi bitta obyektni o'z ichida saqlovchi va xavfsiz qaytaruvchi 'Box<T>' generik sinfini yarating.

## Yechim (Kotlin kodi):
```kotlin
class Box<T>(val value: T) {
    fun getItem(): T = value
}

fun main() {
    val intBox: Box<Int> = Box(100)
    val strBox: Box<String> = Box("Kotlin Generics")

    println("IntBox qiymati: ${intBox.getItem()}")
    println("StrBox qiymati: ${strBox.getItem()}")
}
```

## Tushuntirish va Mantiq:
Kotlinda generiklar (Generics) tiplar ustida parametrlash imkonini beradi. 'Box<T>' sinfida 'T' harfi tur parametri (type parameter) bo'lib, obyekt yaratilayotganda haqiqiy turga ('Int', 'String') aylanadi va to'liq tur xavfsizligini ta'minlaydi.

## Ishlash natijasi:
```text
IntBox qiymati: 100
StrBox qiymati: Kotlin Generics
```


# 552-Topshiriq: Generik funksiya (Generic Function) e'lon qilish
## Topshiriq sharti:
Berilgan elementni ro'yxat ko'rinishida o'rab beruvchi generik funksiya yozing.

## Yechim (Kotlin kodi):
```kotlin
fun <T> singletonList(item: T): List<T> {
    return listOf(item)
}

fun main() {
    val l1 = singletonList(42)
    val l2 = singletonList("Salom")

    println("Sonlar ro'yxati: $l1 (turi: ${l1[0]::class.simpleName})")
    println("Satrlar ro'yxati: $l2 (turi: ${l2[0]::class.simpleName})")
}
```

## Tushuntirish va Mantiq:
Generik funksiyalarda tur parametri 'fun <T>' shaklida funksiya nomidan oldin e'lon qilinadi. Kompilyator funksiyaga uzatilgan argument orqali 'T' ning aniq turini avtomatik aniqlaydi (Type Argument Inference).

## Ishlash natijasi:
```text
Sonlar ro'yxati: [42] (turi: Int)
Satrlar ro'yxati: [Salom] (turi: String)
```


# 553-Topshiriq: Kovariantlik asoslari: 'out' modifikatori (Declaration-site Covariance)
## Topshiriq sharti:
Kotlinda 'out' kalit so'zi yordamida ishlab chiqaruvchi (Producer) sinf yarating va subtyping munosabatini tekshiring.

## Yechim (Kotlin kodi):
```kotlin
// 'out T' faqat qiymat ishlab chiqaradi (qaytaradi), parametr sifatida qabul qilmaydi
interface Producer<out T> {
    fun produce(): T
}

class StringProducer : Producer<String> {
    override fun produce(): String = "Mahsulot matni"
}

fun main() {
    val strProducer: Producer<String> = StringProducer()
    // Kovariantlik tufayli Producer<String> Producer<Any> ga to'g'ridan-to'g'ri biriktiriladi:
    val anyProducer: Producer<Any> = strProducer

    println("Ishlab chiqarildi: ${anyProducer.produce()}")
}
```

## Tushuntirish va Mantiq:
Java da 'List<String>' ni 'List<Object>' ga biriktirib bo'lmaydi (invariance). Kotlinda esa 'out' modifikatori (Declaration-site variance) orqali sinf kovariant deb e'lon qilinadi: agar A B ning subklass bo'lsa, 'Producer<A>' ham 'Producer<B>' ning subklassi bo'ladi. 'out' turdagi parametr faqat metodlarning qaytish turida (out position) bo'lishi shart.

## Ishlash natijasi:
```text
Ishlab chiqarildi: Mahsulot matni
```


# 554-Topshiriq: Kontravariantlik asoslari: 'in' modifikatori (Contravariance)
## Topshiriq sharti:
Kotlinda 'in' kalit so'zi yordamida faqat ma'lumot qabul qiluvchi (Consumer) interfeys tuzing.

## Yechim (Kotlin kodi):
```kotlin
// 'in T' faqat ma'lumot qabul qiladi (iste'molchi), qiymat qaytarmaydi
interface Consumer<in T> {
    fun consume(item: T)
}

class AnyPrinter : Consumer<Any> {
    override fun consume(item: Any) {
        println("[PRINT]: $item")
    }
}

fun main() {
    val anyConsumer: Consumer<Any> = AnyPrinter()
    // Kontravariantlik tufayli Consumer<Any> Consumer<String> ga biriktiriladi!
    val strConsumer: Consumer<String> = anyConsumer

    strConsumer.consume("Maxsus satr")
}
```

## Tushuntirish va Mantiq:
'in' modifikatori kontravariantlikni (Contravariance) ifodalaydi. U subtyping yo'nalishini teskarisiga aylantiradi: agar String Any ning bolasi bo'lsa, 'Consumer<Any>' 'Consumer<String>' ning bolasi (subtype) hisoblanadi. Parametr faqat metod argumentlarida (in position) kelishi shart.

## Ishlash natijasi:
```text
[PRINT]: Maxsus satr
```


# 555-Topshiriq: Invariantlik (Invariance) va xatoliklar
## Topshiriq sharti:
'out' yoki 'in' qo'yilmagan oddiy generik sinflar qat'iy invariant ekanligini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
class Container<T>(var value: T)

fun main() {
    val stringContainer: Container<String> = Container("Matn")
    // val anyContainer: Container<Any> = stringContainer 
    // Kompilyatsiya xatosi: Type mismatch! Required: Container<Any>, Found: Container<String>

    println("Invariant qiymat: ${stringContainer.value}")
}
```

## Tushuntirish va Mantiq:
Agar generik parametr oldiga 'in' yoki 'out' qo'yilmasa, u 'invariant' hisoblanadi (masalan 'MutableList<T>' yoki 'Array<T>'). Chunki 'var' xususiyatga ega bo'lgan sinfda unga yangi qiymat yozish ham, o'qish ham mumkin. Agar 'Container<String>' ni 'Container<Any>' deb olishga ruxsat berilsa, unga butun son yozib qo'yish xavfi tug'iladi.

## Ishlash natijasi:
```text
Invariant qiymat: Matn
```


# 556-Topshiriq: Use-site variance: Tur proyeksiyalari (Type Projections with 'out')
## Topshiriq sharti:
Invariant bo'lgan massivdan faqat o'qish uchun 'Array<out Number>' proyeksiyasidan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
fun printNumbers(numbers: Array<out Number>) {
    // Faqat o'qish mumkin:
    for (n in numbers) {
        print("$n ")
    }
    println()
    // numbers[0] = 100 // Xato: out bo'lgani uchun yozish taqiqlangan!
}

fun main() {
    val ints: Array<Int> = arrayOf(1, 2, 3, 4)
    // Array<Int> ni Array<out Number> ga xavfsiz uzatish mumkin:
    printNumbers(ints)
}
```

## Tushuntirish va Mantiq:
Sinf e'lon qilingan joyda invariant bo'lsa ham ('Array<T>'), uni metod parametrida 'Array<out Number>' deb cheklash 'Use-site variance' deyiladi. Bu Java dagi '? extends Number' ning to'liq va tushunarli muqobilidir.

## Ishlash natijasi:
```text
1 2 3 4
```


# 557-Topshiriq: Use-site variance: Tur proyeksiyalari bilan 'in'
## Topshiriq sharti:
Massivga element yozish uchun 'Array<in Int>' proyeksiyasidan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
fun fillWithZeros(arr: Array<in Int>, count: Int) {
    for (i in 0 until count) {
        arr[i] = 0 // Faqat yozish mumkin
    }
}

fun main() {
    val objects: Array<Any> = arrayOf("A", "B", "C")
    // Array<Any> ga Array<in Int> sifatida xavfsiz yoziladi:
    fillWithZeros(objects, 2)

    println("Natija: ${objects.joinToString()}")
}
```

## Tushuntirish va Mantiq:
'Array<in Int>' Java dagi '? super Integer' ga to'g'ri keladi. Bu massivga kamida Int yoki uning ota turlarini yozish xavfsiz ekanligini kompilyatorga tasdiqlaydi.

## Ishlash natijasi:
```text
Natija: 0, 0, C
```


# 558-Topshiriq: Star-projection (Yulduzcha proyeksiyasi '*'): Noma'lum tur
## Topshiriq sharti:
Turi noma'lum bo'lgan ro'yxat elementlari sonini va birinchi elementini xavfsiz chop etish uchun 'List<*>' dan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
fun printListInfo(list: List<*>) {
    println("Ro'yxat hajmi: ${list.size}")
    if (list.isNotEmpty()) {
        val firstItem: Any? = list[0]
        println("Birinchi element: $firstItem")
    }
}

fun main() {
    printListInfo(listOf(10, 20, 30))
    printListInfo(listOf("Toshkent", "Buxoro"))
}
```

## Tushuntirish va Mantiq:
'List<*>' (star projection) Java dagi 'List<?>' ga to'g'ri keladi. Bu generik argument turi noma'lum ekanligini, ammo tur xavfsizligini saqlash kerakligini bildiradi. O'qilganda qiymatlar 'Any?' sifatida olinadi.

## Ishlash natijasi:
```text
Ro'yxat hajmi: 3
Birinchi element: 10
Ro'yxat hajmi: 2
Birinchi element: Toshkent
```


# 559-Topshiriq: Tur o'chirilishi (Type Erasure) va uning oqibatlari
## Topshiriq sharti:
JVM da ish vaqtida generik turlar o'chib ketishini va 'is List<String>' tekshiruvi nega xatolik berishini tushuntiring.

## Yechim (Kotlin kodi):
```kotlin
fun checkType(list: List<Any>) {
    // if (list is List<String>) // Kompilyatsiya xatosi: Cannot check for instance of erased type
    if (list.isNotEmpty() && list[0] is String) {
        println("Ro'yxatning birinchi elementi matn: ${list[0]}")
    } else {
        println("Ro'yxat matnli emas yoki bo'sh")
    }
}

fun main() {
    checkType(listOf("Kotlin", "2.0"))
    checkType(listOf(1, 2, 3))
}
```

## Tushuntirish va Mantiq:
JVM platformasida orqaga moslik uchun barcha generik parametrlar kompilyatsiyadan so'ng o'chirib tashlanadi (Type Erasure). Ish vaqtida (runtime) 'List<String>' va 'List<Int>' ikkalasi ham oddiy 'List' ga aylanadi. Shuning uchun 'is List<String>' deb to'g'ridan-to'g'ri tekshirib bo'lmaydi.

## Ishlash natijasi:
```text
Ro'yxatning birinchi elementi matn: Kotlin
Ro'yxat matnli emas yoki bo'sh
```


# 560-Topshiriq: Reified Type Parameters: Tur o'chirilishini chetlab o'tish
## Topshiriq sharti:
'inline fun <reified T>' orqali ish vaqtida generik turini to'liq saqlab qoluvchi filtr funksiyasini yozing.

## Yechim (Kotlin kodi):
```kotlin
inline fun <reified T> filterByType(list: List<Any>): List<T> {
    val result = mutableListOf<T>()
    for (item in list) {
        if (item is T) { // reified bo'lgani uchun 'is T' qonuniy!
            result.add(item)
        }
    }
    return result
}

fun main() {
    val mixedList = listOf(1, "Salom", 2.5, "Dunyo", 42)

    val strings: List<String> = filterByType(mixedList)
    val ints: List<Int> = filterByType(mixedList)

    println("Faqat satrlar: $strings")
    println("Faqat butun sonlar: $ints")
}
```

## Tushuntirish va Mantiq:
'reified' (asliga keltirilgan) modifikatori faqat 'inline' funksiyalarda ishlaydi. Kompilyator funksiyani chaqirilgan joyga to'g'ridan-to'g'ri ko'chirgani sababli, 'T' o'rniga aniq 'String.class' yoki 'Integer.class' qo'yiladi. Bu 'is T' va 'T::class' kabi amallarni bajarishga to'liq ruxsat beradi.

## Ishlash natijasi:
```text
Faqat satrlar: [Salom, Dunyo]
Faqat butun sonlar: [1, 42]
```


# 561-Topshiriq: Generik cheklovlar: Yuqori chegara (Upper Bound : Type)
## Topshiriq sharti:
Faqat 'Comparable' interfeysini amalga oshirgan turlar uchun ikkita qiymatning kattasini topuvchi generik metod yozing.

## Yechim (Kotlin kodi):
```kotlin
fun <T : Comparable<T>> findMaximum(a: T, b: T): T {
    return if (a > b) a else b
}

fun main() {
    println("Sonlar kattasi: ${findMaximum(15, 28)}")
    println("Satrlar kattasi: ${findMaximum("Olma", "Banan")}")
}
```

## Tushuntirish va Mantiq:
'<T : UpperBound>' sintaksisi orqali generik turga cheklov qo'yiladi. Bu yerda 'T' faqat 'Comparable' bo'lishi mumkinligi belgilangani uchun 'a > b' operatori xavfsiz ishlaydi.

## Ishlash natijasi:
```text
Sonlar kattasi: 28
Satrlar kattasi: Olma
```


# 562-Topshiriq: Ko'p shartli cheklovlar: 'where' bandi (Multiple Bounds)
## Topshiriq sharti:
Bitta generik tur bir vaqtning o'zida ikkita har xil interfeysni (masalan CharSequence va Comparable) amalga oshirishini talab qiling.

## Yechim (Kotlin kodi):
```kotlin
fun <T> processSpecialText(item: T) where T : CharSequence, T : Comparable<T> {
    if (item.length > 5) {
        println("Uzun matn: $item")
    } else {
        println("Qisqa matn: $item")
    }
}

fun main() {
    processSpecialText("O'zbekiston")
    processSpecialText("Salom")
}
```

## Tushuntirish va Mantiq:
Agar generik parametrga bir nechta yuqori chegaralar talab qilinsa, funksiya oxirida 'where T : InterfaceA, T : InterfaceB' sintaksisi qo'llaniladi.

## Ishlash natijasi:
```text
Uzun matn: O'zbekiston
Qisqa matn: Salom
```


# 563-Topshiriq: Xavfli tip o'tkazishni bostirish: @Suppress('UNCHECKED_CAST')
## Topshiriq sharti:
Kompilyator turini to'liq tekshira olmagan holatda ogohlantirishni xavfsiz o'chirish.

## Yechim (Kotlin kodi):
```kotlin
class ObjectHolder {
    private val data = mutableMapOf<String, Any>()

    fun put(key: String, value: Any) {
        data[key] = value
    }

    @Suppress("UNCHECKED_CAST")
    fun <T> get(key: String): T? {
        return data[key] as? T
    }
}

fun main() {
    val holder = ObjectHolder()
    holder.put("app_id", 1005)

    val id: Int? = holder.get("app_id")
    println("Olingan ID: $id")
}
```

## Tushuntirish va Mantiq:
Type Erasure tufayli 'as? T' tekshiruvi kompilyator tomonidan 'Unchecked cast' ogohlantirishi bilan belgilanadi. Agar dasturchi tur to'g'riligiga amin bo'lsa, '@Suppress("UNCHECKED_CAST")' annotatsiyasini qo'yadi.

## Ishlash natijasi:
```text
Olingan ID: 1005
```


# 564-Topshiriq: Generik interfeyslar va ularni amalga oshirish usullari
## Topshiriq sharti:
Repository andozasini generik interfeys orqali modellashtiring.

## Yechim (Kotlin kodi):
```kotlin
interface Repository<T, ID> {
    fun save(entity: T)
    fun findById(id: ID): T?
}

data class Customer(val id: Long, val name: String)

class CustomerRepository : Repository<Customer, Long> {
    private val store = mutableMapOf<Long, Customer>()

    override fun save(entity: Customer) {
        store[entity.id] = entity
        println("Customer saqlandi: ${entity.name}")
    }

    override fun findById(id: Long): Customer? = store[id]
}

fun main() {
    val repo = CustomerRepository()
    repo.save(Customer(1L, "Jasur"))
    println("Topildi: ${repo.findById(1L)}")
}
```

## Tushuntirish va Mantiq:
Generik interfeyslar ('Repository<T, ID>') biznes mantig'ini ma'lumotlar turidan to'liq ajratishga imkon beradi.

## Ishlash natijasi:
```text
Customer saqlandi: Jasur
Topildi: Customer(id=1, name=Jasur)
```


# 565-Topshiriq: Generik konstruktorlar va Fabrika metodlari
## Topshiriq sharti:
Sinfning o'zi generik bo'lmasa-da, uning konstruktori yoki metodlari generik bo'lishini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
class Converter {
    fun <F, T> convert(from: F, transform: (F) -> T): T {
        return transform(from)
    }
}

fun main() {
    val converter = Converter()
    val stringNumber = converter.convert(12345) { "SON_$it" }
    println("Konvertatsiya: $stringNumber")
}
```

## Tushuntirish va Mantiq:
Oddiy (no-generic) sinf ichida ham mustaqil generik metodlar e'lon qilinishi mumkin.

## Ishlash natijasi:
```text
Konvertatsiya: SON_12345
```


# 566-Topshiriq: Kovariant ro'yxatlar: Kotlinda List sukut bo'yicha out T
## Topshiriq sharti:
Nima uchun Kotlinda 'List<String>' ni 'List<Any>' ga berish xavfsiz ekanligini tushuntiring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val stringList: List<String> = listOf("A", "B", "C")
    // Kotlin standart kutubxonasida: public interface List<out E> : Collection<E>
    val anyList: List<Any> = stringList // 100% qonuniy!

    println("AnyList elementlari: $anyList")
}
```

## Tushuntirish va Mantiq:
Kotlinda standart 'List<out E>' faqat o'qish uchun mo'ljallangan (read-only). Unda 'add' yoki 'set' metodlari yo'qligi sababli, 'List<String>' ni 'List<Any>' deb qabul qilish mutlaqo xavfsizdir va 'out E' bilan belgilangan.

## Ishlash natijasi:
```text
AnyList elementlari: [A, B, C]
```


# 567-Topshiriq: Invariant to'plamlar: MutableList da out yo'qligi
## Topshiriq sharti:
'MutableList' nima uchun kovariant bo'la olmasligini va xatolikni amalda ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    val stringList: MutableList<String> = mutableListOf("A", "B")
    // val anyList: MutableList<Any> = stringList // Kompilyatsiya xatosi: Type mismatch!
    
    // Nima uchun taqiqlangan? Chunki agar ruxsat berilsa:
    // anyList.add(100) // String ro'yxatiga Int tushib qolardi!
    
    println("MutableList invariant: $stringList")
}
```

## Tushuntirish va Mantiq:
'MutableList<E>' o'zgaruvchan bo'lgani uchun invariantdir. Unga yangi elementlar qo'shish mumkinligi sababli, tur buzilishining oldini olish uchun kovariantlik taqiqlangan.

## Ishlash natijasi:
```text
MutableList invariant: [A, B]
```


# 568-Topshiriq: Star-projection bilan Kolleksiya bo'shligini tekshirish
## Topshiriq sharti:
Har qanday turdagi ro'yxatning bo'sh emasligini tekshiruvchi funksiya.

## Yechim (Kotlin kodi):
```kotlin
fun hasElements(collection: Collection<*>): Boolean {
    return collection.isNotEmpty()
}

fun main() {
    println("Sonlar ro'yxati: ${hasElements(listOf(1, 2))}")
    println("Bo'sh ro'yxat: ${hasElements(emptyList<String>())}")
}
```

## Tushuntirish va Mantiq:
Elementlarning aniq turi muhim bo'lmaganda (faqat hajm, bo'shlik tekshirilganda) star-projection '*' eng toza sintaksisni beradi.

## Ishlash natijasi:
```text
Sonlar ro'yxati: true
Bo'sh ro'yxat: false
```


# 569-Topshiriq: Reified Type bilan JSON Parser analogi
## Topshiriq sharti:
Sinf turini uzatmasdan to'g'ridan-to'g'ri tur bo'yicha ma'lumotni shakllantirish.

## Yechim (Kotlin kodi):
```kotlin
inline fun <reified T> createEmptyInstanceName(): String {
    return "Yangi obyekt turi: ${T::class.simpleName}"
}

fun main() {
    println(createEmptyInstanceName<String>())
    println(createEmptyInstanceName<Double>())
}
```

## Tushuntirish va Mantiq:
'reified' orqali Java dagi noqulay 'Class<T> clazz' parametrini uzatishdan butunlay xalos bo'linadi.

## Ishlash natijasi:
```text
Yangi obyekt turi: String
Yangi obyekt turi: Double
```


# 570-Topshiriq: Generik cheklovlar: Sonli arifmetika bilan ishlash
## Topshiriq sharti:
Har qanday raqamli turni qabul qilib, uning ikki karra qiymatini Double da hisoblash.

## Yechim (Kotlin kodi):
```kotlin
fun <T : Number> doubleValue(number: T): Double {
    return number.toDouble() * 2.0
}

fun main() {
    println("Int 10: ${doubleValue(10)}")
    println("Double 5.5: ${doubleValue(5.5)}")
    println("Float 3.0f: ${doubleValue(3.0f)}")
}
```

## Tushuntirish va Mantiq:
'T : Number' chegarasi barcha sonli turlarning umumiy ota sinfiga tayanadi.

## Ishlash natijasi:
```text
Int 10: 20.0
Double 5.5: 11.0
Float 3.0f: 6.0
```


# 571-Topshiriq: Kovariant Daraxt Tuguni (Covariant Tree Node)
## Topshiriq sharti:
O'zgarmas ikkilik daraxt tugunini 'out T' orqali modellashtiring.

## Yechim (Kotlin kodi):
```kotlin
class BinaryNode<out T>(val value: T, val left: BinaryNode<T>? = null, val right: BinaryNode<T>? = null)

fun main() {
    val intNode: BinaryNode<Int> = BinaryNode(10)
    // Kovariantlik tufayli BinaryNode<Number> ga biriktirish mumkin:
    val numNode: BinaryNode<Number> = intNode

    println("Tugun qiymati: ${numNode.value}")
}
```

## Tushuntirish va Mantiq:
O'zgarmas daraxt tuzilmalari 'out T' orqali to'liq polimorfik iyerarxiyalarga xizmat qila oladi.

## Ishlash natijasi:
```text
Tugun qiymati: 10
```


# 572-Topshiriq: Kontravariant Komparator (Contravariant Comparator)
## Topshiriq sharti:
Ota sinf komparatorini bola sinflar uchun ishlatish.

## Yechim (Kotlin kodi):
```kotlin
open class Animal(val weight: Double)
class Dog(weight: Double, val breed: String) : Animal(weight)

val animalWeightComparator = Comparator<Animal> { a1, a2 ->
    a1.weight.compareTo(a2.weight)
}

fun main() {
    val dogs = listOf(Dog(12.5, "Taksa"), Dog(35.0, "Ovtcharka"))
    // Comparator<in Dog> talab qilingan joyga Comparator<Animal> xavfsiz beriladi:
    val sortedDogs = dogs.sortedWith(animalWeightComparator)

    println("Vazni bo'yicha birinchi it: ${sortedDogs.first().breed}")
}
```

## Tushuntirish va Mantiq:
Java va Kotlinda 'Comparator<in T>' kontravariant bo'lib, umumiy ota sinf solishtiruvchisini barcha subklasslar uchun qayta ishlatish imkonini beradi.

## Ishlash natijasi:
```text
Vazni bo'yicha birinchi it: Taksa
```


# 573-Topshiriq: Generik Stack (To'plam) ma'lumotlar tuzilmasi
## Topshiriq sharti:
LIFO (Last-In-First-Out) tamoyilida ishlovchi xavfsiz generik Stack yarating.

## Yechim (Kotlin kodi):
```kotlin
class SimpleStack<T> {
    private val elements = mutableListOf<T>()

    fun push(item: T) = elements.add(item)
    
    fun pop(): T? {
        if (elements.isEmpty()) return null
        return elements.removeAt(elements.size - 1)
    }

    fun peek(): T? = elements.lastOrNull()
}

fun main() {
    val stack = SimpleStack<String>()
    stack.push("Birinchi")
    stack.push("Ikkinchi")

    println("Oxirgi element (peek): ${stack.peek()}")
    println("Sug'urib olindi (pop): ${stack.pop()}")
    println("Qolgan oxirgi: ${stack.peek()}")
}
```

## Tushuntirish va Mantiq:
Klassik ma'lumotlar tuzilmalarini generiklar bilan xavfsiz amalga oshirish.

## Ishlash natijasi:
```text
Oxirgi element (peek): Ikkinchi
Sug'urib olindi (pop): Ikkinchi
Qolgan oxirgi: Birinchi
```


# 574-Topshiriq: Generik Pair va Custom Tuple sinflari
## Topshiriq sharti:
Ikki xil turdagi qiymatlarni bitta generik obyektda bog'lash.

## Yechim (Kotlin kodi):
```kotlin
data class KeyValue<K, V>(val key: K, val value: V)

fun main() {
    val entry = KeyValue("foydalanuvchi_id", 1009)
    println("Kalit: ${entry.key} | Qiymat: ${entry.value}")
}
```

## Tushuntirish va Mantiq:
Turli ma'lumotlar juftliklarini generik data class larda saqlash.

## Ishlash natijasi:
```text
Kalit: foydalanuvchi_id | Qiymat: 1009
```


# 575-Topshiriq: Reified Type bilan Bundle yoki Map dan xavfsiz o'qish
## Topshiriq sharti:
Android Intent/Bundle kabi xaritadan tur bo'yicha o'qib beruvchi inline yordamchi tuzing.

## Yechim (Kotlin kodi):
```kotlin
class SafeDataMap(private val map: Map<String, Any>) {
    inline fun <reified T> getTyped(key: String): T? {
        val value = map[key]
        return if (value is T) value else null
    }
}

fun main() {
    val data = SafeDataMap(mapOf("yosh" to 25, "ism" to "Alisher"))

    val age: Int? = data.getTyped("yosh")
    val wrongType: String? = data.getTyped("yosh")

    println("Yosh (Int): $age")
    println("Noto'g'ri tur so'ralganda: $wrongType")
}
```

## Tushuntirish va Mantiq:
'reified' orqali dinamik xaritalardan kerakli turni xatosiz o'qib olish.

## Ishlash natijasi:
```text
Yosh (Int): 25
Noto'g'ri tur so'ralganda: null
```


# 576-Topshiriq: Generik metodlarda standart parametrlar
## Topshiriq sharti:
Generik parametrga standart funksiya yoki qiymat biriktirish.

## Yechim (Kotlin kodi):
```kotlin
fun <T> formatList(list: List<T>, formatter: (T) -> String = { it.toString() }): String {
    return list.joinToString(", ", transform = formatter)
}

fun main() {
    val numbers = listOf(1, 2, 3)
    println(formatList(numbers))
    println(formatList(numbers) { "Son_$it" })
}
```

## Tushuntirish va Mantiq:
Generik funksiyalarda standart parametrlar kodni yanada moslashuvchan qiladi.

## Ishlash natijasi:
```text
1, 2, 3
Son_1, Son_2, Son_3
```


# 577-Topshiriq: Generiklar bilan Builder Pattern
## Topshiriq sharti:
Tur xavfsiz Builder obyektini modellashtirish.

## Yechim (Kotlin kodi):
```kotlin
class EntityBuilder<T>(val factory: () -> T) {
    fun build(): T = factory()
}

fun main() {
    val strBuilder = EntityBuilder { "Yangi Satr Obyekti" }
    println("Qurildi: ${strBuilder.build()}")
}
```

## Tushuntirish va Mantiq:
Fabrika va Builder larni generiklar orqali abstraktlashtirish.

## Ishlash natijasi:
```text
Qurildi: Yangi Satr Obyekti
```


# 578-Topshiriq: Generik cheklov bilan Minimal elementni topish
## Topshiriq sharti:
Comparable bo'lgan ro'yxatdan eng kichik qiymatni topuvchi funksiya.

## Yechim (Kotlin kodi):
```kotlin
fun <T : Comparable<T>> findMinItem(items: List<T>): T? {
    if (items.isEmpty()) return null
    var min = items[0]
    for (item in items) {
        if (item < min) min = item
    }
    return min
}

fun main() {
    println("Min son: ${findMinItem(listOf(45, 12, 89, 3))}")
    println("Min satr: ${findMinItem(listOf("Nok", "Anor", "Uzum"))}")
}
```

## Tushuntirish va Mantiq:
Comparable chegarasi bilan generic taqqoslash algoritmi.

## Ishlash natijasi:
```text
Min son: 3
Min satr: Anor
```


# 579-Topshiriq: Star-projection va Kolleksiya elementlarini sanash
## Topshiriq sharti:
Kolleksiya ichidagi null bo'lmagan elementlar sonini sanovchi generik funksiya.

## Yechim (Kotlin kodi):
```kotlin
fun countNonNull(items: Iterable<*>): Int {
    var count = 0
    for (item in items) {
        if (item != null) count++
    }
    return count
}

fun main() {
    val list = listOf(1, null, "A", null, 3.14)
    println("Null bo'lmaganlar: ${countNonNull(list)} ta")
}
```

## Tushuntirish va Mantiq:
Star-projection orqali istalgan turdagi to'plam elementlarini xavfsiz aylanib chiqish.

## Ishlash natijasi:
```text
Null bo'lmaganlar: 3 ta
```


# 580-Topshiriq: Generik Pipeline: Ma'lumotlarni o'zgartirish zanjiri
## Topshiriq sharti:
Kirish va chiqish turlari har xil bo'lgan funksional quvur.

## Yechim (Kotlin kodi):
```kotlin
class Step<I, O>(val transform: (I) -> O) {
    fun <Next> andThen(nextStep: (O) -> Next): Step<I, Next> {
        return Step { input -> nextStep(this.transform(input)) }
    }
}

fun main() {
    val pipeline = Step<String, Int> { it.length }
        .andThen { it * 10 }
        .andThen { "Natija: $it ball" }

    println(pipeline.transform("Kotlin"))
}
```

## Tushuntirish va Mantiq:
Zanjirli generik qadamlar (Monad / Pipeline) orqali ma'lumotlarni bosqichma-bosqich o'zgartirish.

## Ishlash natijasi:
```text
Natija: 60 ball
```


# 581-Topshiriq: Kovariantlikda metod parametriga 'out' turini berish cheklovi
## Topshiriq sharti:
Nima uchun 'out T' modifikatorli interfeysda 'fun add(item: T)' yozish taqiqlanganligini tushuntiring.

## Yechim (Kotlin kodi):
```kotlin
// interface InvalidProducer<out T> {
//     fun add(item: T) // Kompilyatsiya xatosi: Type parameter T is declared as 'out' but occurs in 'in' position
// }

interface ValidProducer<out T> {
    fun get(): T // Qonuniy (out position)
}

fun main() {
    println("Kovariantlik qoidasi: 'out' faqat chiqish joyida bo'ladi.")
}
```

## Tushuntirish va Mantiq:
Agar 'out T' ga metod parametri (in position) berilsa, subtyping xavfsizligi buziladi. Shu sababli Kotlin kompilyatori 'Type parameter occurs in in-position' xatoligi bilan buni qat'iy to'xtatadi.

## Ishlash natijasi:
```text
Kovariantlik qoidasi: 'out' faqat chiqish joyida bo'ladi.
```


# 582-Topshiriq: @UnsafeVariance annotatsiyasi: Istisno holatlar
## Topshiriq sharti:
Kovariant sinfda qidiruv metodiga element uzatish uchun '@UnsafeVariance' dan ehtiyotkorlik bilan foydalanish.

## Yechim (Kotlin kodi):
```kotlin
interface SafeList<out E> {
    fun get(index: Int): E
    // contains metodida element qidiriladi, ammo ro'yxat o'zgarmaydi:
    fun contains(element: @UnsafeVariance E): Boolean
}

class SimpleList<out E>(private val data: List<E>) : SafeList<E> {
    override fun get(index: Int): E = data[index]
    override fun contains(element: @UnsafeVariance E): Boolean = data.contains(element)
}

fun main() {
    val list: SafeList<Number> = SimpleList(listOf(1, 2, 3))
    println("2 mavjudmi: ${list.contains(2)}")
}
```

## Tushuntirish va Mantiq:
Ba'zan o'qish uchun mo'ljallangan sinflarda (masalan Set.contains) elementni faqat solishtirish uchun qabul qilish talab etiladi. Bunday xavfsiz holatlarda '@UnsafeVariance' qo'yiladi.

## Ishlash natijasi:
```text
2 mavjudmi: true
```


# 583-Topshiriq: Generik xususiyatlar (Generic Extension Properties)
## Topshiriq sharti:
Kolleksiyaning ikkinchi elementini xavfsiz oluvchi kengaytma xususiyati.

## Yechim (Kotlin kodi):
```kotlin
val <T> List<T>.secondItem: T?
    get() = if (size >= 2) this[1] else null

fun main() {
    println("Sonlar: ${listOf(10, 20).secondItem}")
    println("Satrlar: ${listOf("Bir").secondItem}")
}
```

## Tushuntirish va Mantiq:
Kengaytma xususiyatlar ham to'liq generik bo'lishi mumkin.

## Ishlash natijasi:
```text
Sonlar: 20
Satrlar: null
```


# 584-Topshiriq: Reified Type bilan Enum qiymatlarini topish
## Topshiriq sharti:
Berilgan satr bo'yicha enum qiymatini topuvchi ixcham reified metod.

## Yechim (Kotlin kodi):
```kotlin
inline fun <reified E : Enum<E>> findEnumByName(name: String): E? {
    return enumValues<E>().firstOrNull { it.name.equals(name, ignoreCase = true) }
}

enum class Color { RED, GREEN, BLUE }

fun main() {
    val c = findEnumByName<Color>("green")
    println("Topilgan rang: $c")
}
```

## Tushuntirish va Mantiq:
'reified' generiklar yordamida enum turlarini tekshirish juda qisqa va qulay yoziladi.

## Ishlash natijasi:
```text
Topilgan rang: GREEN
```


# 585-Topshiriq: Generik Kesh xaritasi (Thread-safe Generic Cache)
## Topshiriq sharti:
Ixtiyoriy kalit va qiymatlar uchun keshlovchi generik sinf.

## Yechim (Kotlin kodi):
```kotlin
class MemoryCache<K, V> {
    private val storage = mutableMapOf<K, V>()

    fun getOrPut(key: K, supplier: () -> V): V {
        return storage.getOrPut(key, supplier)
    }
}

fun main() {
    val cache = MemoryCache<String, Int>()
    val v1 = cache.getOrPut("yosh") { 25 }
    val v2 = cache.getOrPut("yosh") { 30 }

    println("v1: $v1, v2 (keshdan): $v2")
}
```

## Tushuntirish va Mantiq:
Generik kesh sinflari loyihada barcha modellar uchun qayta ishlatiladi.

## Ishlash natijasi:
```text
v1: 25, v2 (keshdan): 25
```


# 586-Topshiriq: Generik cheklovda Rekursiv Bog'lanish (Recursive Type Bound)
## Topshiriq sharti:
Comparable<T> kabi o'zini o'zi cheklovchi generik parametrlar.

## Yechim (Kotlin kodi):
```kotlin
abstract class OrderedItem<T : OrderedItem<T>> : Comparable<T>

class PriorityTask(val priority: Int) : OrderedItem<PriorityTask>() {
    override fun compareTo(other: PriorityTask): Int {
        return this.priority.compareTo(other.priority)
    }
}

fun main() {
    val t1 = PriorityTask(1)
    val t2 = PriorityTask(2)
    println("t1 < t2: ${t1 < t2}")
}
```

## Tushuntirish va Mantiq:
Rekursiv tur chegarasi ('T : OrderedItem<T>') obyekt faqat o'zi bilan bir xil turdagi obyektlar bilan solishtirilishini kafolatlaydi.

## Ishlash natijasi:
```text
t1 < t2: true
```


# 587-Topshiriq: Generik Obyekt Fabrikasi: Provider interfeysi
## Topshiriq sharti:
Obyektlarni yaratib beruvchi generik shartnoma.

## Yechim (Kotlin kodi):
```kotlin
interface Provider<T> {
    fun get(): T
}

class StringProvider : Provider<String> {
    override fun get(): String = "Yangi Matn"
}

fun main() {
    val p: Provider<String> = StringProvider()
    println(p.get())
}
```

## Tushuntirish va Mantiq:
Dependency Injection va Factory andozalarida generik 'Provider<T>' asosiy komponentdir.

## Ishlash natijasi:
```text
Yangi Matn
```


# 588-Topshiriq: Reified Type bilan Ro'yxat elementlarini tekshirish
## Topshiriq sharti:
Ro'yxatdagi barcha elementlar ma'lum bir turga tegishli ekanligini tasdiqlash.

## Yechim (Kotlin kodi):
```kotlin
inline fun <reified T> allInstancesOf(list: List<Any>): Boolean {
    return list.all { it is T }
}

fun main() {
    println("Barchasi satrmi: ${allInstancesOf<String>(listOf("A", "B", "C"))}")
    println("Barchasi satrmi (aralash): ${allInstancesOf<String>(listOf("A", 1, "C"))}")
}
```

## Tushuntirish va Mantiq:
'allInstancesOf' yordamida 'list.all { it is T }' amali reified tufayli to'liq ishlaydi.

## Ishlash natijasi:
```text
Barchasi satrmi: true
Barchasi satrmi (aralash): false
```


# 589-Topshiriq: Generik Result Wrapper: Data, Error va Loading
## Topshiriq sharti:
Ixtiyoriy ma'lumotni o'rovchi 'Resource<T>' arxitektura sinfi.

## Yechim (Kotlin kodi):
```kotlin
sealed class Resource<out T> {
    data class Success<out T>(val data: T) : Resource<T>()
    data class Error(val message: String) : Resource<Nothing>()
    object Loading : Resource<Nothing>()
}

fun main() {
    val res: Resource<String> = Resource.Success("Ma'lumotlar")
    when (res) {
        is Resource.Success -> println("Muvaffaqiyatli: ${res.data}")
        is Resource.Error -> println("Xato: ${res.message}")
        Resource.Loading -> println("Yuklanmoqda...")
    }
}
```

## Tushuntirish va Mantiq:
'Resource<out T>' kovariantligi 'Nothing' bilan birlashganda Error va Loading holatlarini ixtiyoriy 'Resource<T>' ga xavfsiz biriktirish imkonini beradi.

## Ishlash natijasi:
```text
Muvaffaqiyatli: Ma'lumotlar
```


# 590-Topshiriq: Generiklar bilan Ro'yxatni teskarisiga aylantirish
## Topshiriq sharti:
O'zgarmas generik ro'yxatni teskari o'giruvchi shaxsiy metod.

## Yechim (Kotlin kodi):
```kotlin
fun <T> List<T>.customReversed(): List<T> {
    val result = ArrayList<T>(size)
    for (i in size - 1 downTo 0) {
        result.add(this[i])
    }
    return result
}

fun main() {
    val list = listOf(1, 2, 3, 4)
    println("Teskari ro'yxat: ${list.customReversed()}")
}
```

## Tushuntirish va Mantiq:
Generik kengaytma funksiyasi orqali ixtiyoriy ro'yxatni teskarisiga o'girish.

## Ishlash natijasi:
```text
Teskari ro'yxat: [4, 3, 2, 1]
```


# 591-Topshiriq: Generik sinfda bir nechta tur parametrlari: Triplet
## Topshiriq sharti:
Uch xil turdagi qiymatlarni bitta generik obyektda birlashtiring.

## Yechim (Kotlin kodi):
```kotlin
data class Triplet<A, B, C>(val first: A, val second: B, val third: C)

fun main() {
    val info = Triplet("Foydalanuvchi", 101, true)
    println("Ism: ${info.first}, ID: ${info.second}, Faol: ${info.third}")
}
```

## Tushuntirish va Mantiq:
Uchta alohida generik parametr orqali ma'lumotlarni turlari bo'yicha bog'lash.

## Ishlash natijasi:
```text
Ism: Foydalanuvchi, ID: 101, Faol: true
```


# 592-Topshiriq: Generik Mapper interfeysi
## Topshiriq sharti:
Bitta modelni ikkinchi modelga o'tkazuvchi generik shartnoma.

## Yechim (Kotlin kodi):
```kotlin
interface Mapper<in I, out O> {
    fun map(input: I): O
}

class IntToStringMapper : Mapper<Int, String> {
    override fun map(input: Int): String = "Son qiymati: $input"
}

fun main() {
    val mapper: Mapper<Int, String> = IntToStringMapper()
    println(mapper.map(500))
}
```

## Tushuntirish va Mantiq:
'Mapper<in I, out O>' da kirish 'in', chiqish esa 'out' modifikatorlari bilan to'liq to'g'ri loyihalashtirilgan.

## Ishlash natijasi:
```text
Son qiymati: 500
```


# 593-Topshiriq: Reified Type bilan Filtr: findFirstInstance
## Topshiriq sharti:
Kolleksiyadagi ma'lum turdagi birinchi elementni qaytaruvchi inline metod.

## Yechim (Kotlin kodi):
```kotlin
inline fun <reified T> findFirstInstance(list: List<Any>): T? {
    for (item in list) {
        if (item is T) return item
    }
    return null
}

fun main() {
    val mixed = listOf(1, "Matn", 3.14)
    val str: String? = findFirstInstance(mixed)
    val dbl: Double? = findFirstInstance(mixed)

    println("Birinchi satr: $str")
    println("Birinchi double: $dbl")
}
```

## Tushuntirish va Mantiq:
'reified' orqali birinchi mos turdagi elementni topish.

## Ishlash natijasi:
```text
Birinchi satr: Matn
Birinchi double: 3.14
```


# 594-Topshiriq: Generik cheklovda Enum klassini talab qilish: <E : Enum<E>>
## Topshiriq sharti:
Faqat Enum turlari bilan ishlaydigan generik metod yozing.

## Yechim (Kotlin kodi):
```kotlin
fun <E : Enum<E>> printEnumDetails(enumConstant: E) {
    println("Enum nomi: ${enumConstant.name}, Tartibi: ${enumConstant.ordinal}")
}

enum class Status { ACTIVE, DISABLED }

fun main() {
    printEnumDetails(Status.ACTIVE)
}
```

## Tushuntirish va Mantiq:
'<E : Enum<E>>' chegarasi parametr faqat Enum turlariga mansub bo'lishini kafolatlaydi.

## Ishlash natijasi:
```text
Enum nomi: ACTIVE, Tartibi: 0
```


# 595-Topshiriq: Generik kolleksiyani birlashtirish: customFlatten
## Topshiriq sharti:
Ichma-ich ro'yxatlarni bitta tekis ro'yxatga keltiruvchi generik funksiya.

## Yechim (Kotlin kodi):
```kotlin
fun <T> List<List<T>>.customFlatten(): List<T> {
    val result = ArrayList<T>()
    for (sublist in this) {
        result.addAll(sublist)
    }
    return result
}

fun main() {
    val nested = listOf(listOf(1, 2), listOf(3, 4, 5))
    println("Tekislangan ro'yxat: ${nested.customFlatten()}")
}
```

## Tushuntirish va Mantiq:
Ichma-ich ro'yxatlarni 'flatten' qilish generik kengaytmasi.

## Ishlash natijasi:
```text
Tekislangan ro'yxat: [1, 2, 3, 4, 5]
```


# 596-Topshiriq: Generiklar bilan Shartli taqqoslash: areEqual
## Topshiriq sharti:
Ikki generik obyektning tengligini tekshirish.

## Yechim (Kotlin kodi):
```kotlin
fun <T> areEqual(a: T, b: T): Boolean = a == b

fun main() {
    println("Tenglik (Int): ${areEqual(10, 10)}")
    println("Tenglik (String): ${areEqual("A", "B")}")
}
```

## Tushuntirish va Mantiq:
Generik tenglik tekshiruvi Kotlinda xavfsiz 'equals' ga kompilyatsiya bo'ladi.

## Ishlash natijasi:
```text
Tenglik (Int): true
Tenglik (String): false
```


# 597-Topshiriq: Generik Predikatlar bilan Kolleksiya bo'lish
## Topshiriq sharti:
Generik ro'yxatni predikatga ko'ra ikkiga ajratish.

## Yechim (Kotlin kodi):
```kotlin
fun <T> splitByPredicate(list: List<T>, predicate: (T) -> Boolean): Pair<List<T>, List<T>> {
    val pass = mutableListOf<T>()
    val fail = mutableListOf<T>()
    for (item in list) {
        if (predicate(item)) pass.add(item) else fail.add(item)
    }
    return Pair(pass, fail)
}

fun main() {
    val (positive, negative) = splitByPredicate(listOf(1, -2, 3, -4)) { it > 0 }
    println("Musbat: $positive | Manfiy: $negative")
}
```

## Tushuntirish va Mantiq:
Generik predikatlar bilan ma'lumotlarni saralash.

## Ishlash natijasi:
```text
Musbat: [1, 3] | Manfiy: [-2, -4]
```


# 598-Topshiriq: Kovariantlik va Kontravariantlikni birga qo'llash: Data Transformer
## Topshiriq sharti:
Kirish va chiqish kanallari bo'lgan transformator sinfi.

## Yechim (Kotlin kodi):
```kotlin
interface DataChannel<in Input, out Output> {
    fun process(item: Input): Output
}

class LengthChannel : DataChannel<String, Int> {
    override fun process(item: String): Int = item.length
}

fun main() {
    val channel: DataChannel<String, Int> = LengthChannel()
    println("Natija: ${channel.process("KotlinGenerics")}")
}
```

## Tushuntirish va Mantiq:
'in' va 'out' parametrlarini bitta interfeysda to'g'ri joylashtirish.

## Ishlash natijasi:
```text
Natija: 14
```


# 599-Topshiriq: Generik xususiyatlar bilan O'zgarmas Singleton to'plami
## Topshiriq sharti:
Bo'sh ro'yxatni generik xususiyat orqali taqdim etish.

## Yechim (Kotlin kodi):
```kotlin
val <T> emptyGenericList: List<T>
    get() = emptyList()

fun main() {
    val list1: List<String> = emptyGenericList
    val list2: List<Int> = emptyGenericList
    println("list1 bo'sh: ${list1.isEmpty()}, list2 bo'sh: ${list2.isEmpty()}")
}
```

## Tushuntirish va Mantiq:
Generik kengaytma xususiyatlari orqali bo'sh xavfsiz to'plamlarni olish.

## Ishlash natijasi:
```text
list1 bo'sh: true, list2 bo'sh: true
```


# 600-Topshiriq: Generiklar bo'yicha to'liq amaliy xulosa: Korxona Ma'lumotlar Bazasi va Resurs Repozitoriysi
## Topshiriq sharti:
Generic class, In/Out variance, Reified inline funksiya, Generic constraints va Type projections ni bitta yaxlit tizimda birlashtiring.

## Yechim (Kotlin kodi):
```kotlin
interface IdentifiableEntity<ID> {
    val id: ID
}

interface EntityReader<out T : IdentifiableEntity<*>> {
    fun readAll(): List<T>
}

class InMemoryRepository<T : IdentifiableEntity<ID>, ID : Comparable<ID>> : EntityReader<T> {
    private val storage = mutableMapOf<ID, T>()

    fun insert(entity: T) {
        storage[entity.id] = entity
        println("[SAQLANDI]: Entity #${entity.id}")
    }

    override fun readAll(): List<T> = storage.values.toList()

    fun getById(id: ID): T? = storage[id]
}

data class UserAccount(override val id: Long, val name: String) : IdentifiableEntity<Long>

inline fun <reified T : IdentifiableEntity<*>> printEntityReport(reader: EntityReader<T>) {
    val items = reader.readAll()
    println("=== HISOBOT: ${T::class.simpleName} (Jami: ${items.size} ta) ===")
    items.forEach { println(" - ID: ${it.id}") }
}

fun main() {
    val repo = InMemoryRepository<UserAccount, Long>()
    repo.insert(UserAccount(101L, "Sardor"))
    repo.insert(UserAccount(102L, "Javohir"))

    // EntityReader<UserAccount> kovariant ravishda uzatiladi:
    printEntityReport<UserAccount>(repo)
}
```

## Tushuntirish va Mantiq:
Ushbu yakuniy topshiriqda talab qilingan barcha generik vositalar: Generik klass va interfeys, 'out' kovariantligi ('EntityReader<out T>'), generik cheklovlar ('T : IdentifiableEntity<ID>', 'ID : Comparable<ID>'), hamda 'inline fun <reified T>' reified hisoboti bitta to'laqonli korxona repozitoriysida mukammal birlashtirildi.

## Ishlash natijasi:
```text
[SAQLANDI]: Entity #101
[SAQLANDI]: Entity #102
=== HISOBOT: UserAccount (Jami: 2 ta) ===
 - ID: 101
 - ID: 102
```

