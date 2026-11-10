# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

data_12 = [
    (
        551,
        "Generik sinf (Generic Class) asoslari",
        "Har qanday turdagi bitta obyektni o'z ichida saqlovchi va xavfsiz qaytaruvchi 'Box<T>' generik sinfini yarating.",
        """class Box<T>(val value: T) {
    fun getItem(): T = value
}

fun main() {
    val intBox: Box<Int> = Box(100)
    val strBox: Box<String> = Box("Kotlin Generics")

    println("IntBox qiymati: ${intBox.getItem()}")
    println("StrBox qiymati: ${strBox.getItem()}")
}""",
        "Kotlinda generiklar (Generics) tiplar ustida parametrlash imkonini beradi. 'Box<T>' sinfida 'T' harfi tur parametri (type parameter) bo'lib, obyekt yaratilayotganda haqiqiy turga ('Int', 'String') aylanadi va to'liq tur xavfsizligini ta'minlaydi.",
        """IntBox qiymati: 100
StrBox qiymati: Kotlin Generics"""
    ),
    (
        552,
        "Generik funksiya (Generic Function) e'lon qilish",
        "Berilgan elementni ro'yxat ko'rinishida o'rab beruvchi generik funksiya yozing.",
        """fun <T> singletonList(item: T): List<T> {
    return listOf(item)
}

fun main() {
    val l1 = singletonList(42)
    val l2 = singletonList("Salom")

    println("Sonlar ro'yxati: $l1 (turi: ${l1[0]::class.simpleName})")
    println("Satrlar ro'yxati: $l2 (turi: ${l2[0]::class.simpleName})")
}""",
        "Generik funksiyalarda tur parametri 'fun <T>' shaklida funksiya nomidan oldin e'lon qilinadi. Kompilyator funksiyaga uzatilgan argument orqali 'T' ning aniq turini avtomatik aniqlaydi (Type Argument Inference).",
        """Sonlar ro'yxati: [42] (turi: Int)
Satrlar ro'yxati: [Salom] (turi: String)"""
    ),
    (
        553,
        "Kovariantlik asoslari: 'out' modifikatori (Declaration-site Covariance)",
        "Kotlinda 'out' kalit so'zi yordamida ishlab chiqaruvchi (Producer) sinf yarating va subtyping munosabatini tekshiring.",
        """// 'out T' faqat qiymat ishlab chiqaradi (qaytaradi), parametr sifatida qabul qilmaydi
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
}""",
        "Java da 'List<String>' ni 'List<Object>' ga biriktirib bo'lmaydi (invariance). Kotlinda esa 'out' modifikatori (Declaration-site variance) orqali sinf kovariant deb e'lon qilinadi: agar A B ning subklass bo'lsa, 'Producer<A>' ham 'Producer<B>' ning subklassi bo'ladi. 'out' turdagi parametr faqat metodlarning qaytish turida (out position) bo'lishi shart.",
        """Ishlab chiqarildi: Mahsulot matni"""
    ),
    (
        554,
        "Kontravariantlik asoslari: 'in' modifikatori (Contravariance)",
        "Kotlinda 'in' kalit so'zi yordamida faqat ma'lumot qabul qiluvchi (Consumer) interfeys tuzing.",
        """// 'in T' faqat ma'lumot qabul qiladi (iste'molchi), qiymat qaytarmaydi
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
}""",
        "'in' modifikatori kontravariantlikni (Contravariance) ifodalaydi. U subtyping yo'nalishini teskarisiga aylantiradi: agar String Any ning bolasi bo'lsa, 'Consumer<Any>' 'Consumer<String>' ning bolasi (subtype) hisoblanadi. Parametr faqat metod argumentlarida (in position) kelishi shart.",
        """[PRINT]: Maxsus satr"""
    ),
    (
        555,
        "Invariantlik (Invariance) va xatoliklar",
        "'out' yoki 'in' qo'yilmagan oddiy generik sinflar qat'iy invariant ekanligini ko'rsating.",
        """class Container<T>(var value: T)

fun main() {
    val stringContainer: Container<String> = Container("Matn")
    // val anyContainer: Container<Any> = stringContainer 
    // Kompilyatsiya xatosi: Type mismatch! Required: Container<Any>, Found: Container<String>

    println("Invariant qiymat: ${stringContainer.value}")
}""",
        "Agar generik parametr oldiga 'in' yoki 'out' qo'yilmasa, u 'invariant' hisoblanadi (masalan 'MutableList<T>' yoki 'Array<T>'). Chunki 'var' xususiyatga ega bo'lgan sinfda unga yangi qiymat yozish ham, o'qish ham mumkin. Agar 'Container<String>' ni 'Container<Any>' deb olishga ruxsat berilsa, unga butun son yozib qo'yish xavfi tug'iladi.",
        """Invariant qiymat: Matn"""
    ),
    (
        556,
        "Use-site variance: Tur proyeksiyalari (Type Projections with 'out')",
        "Invariant bo'lgan massivdan faqat o'qish uchun 'Array<out Number>' proyeksiyasidan foydalaning.",
        """fun printNumbers(numbers: Array<out Number>) {
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
}""",
        "Sinf e'lon qilingan joyda invariant bo'lsa ham ('Array<T>'), uni metod parametrida 'Array<out Number>' deb cheklash 'Use-site variance' deyiladi. Bu Java dagi '? extends Number' ning to'liq va tushunarli muqobilidir.",
        """1 2 3 4"""
    ),
    (
        557,
        "Use-site variance: Tur proyeksiyalari bilan 'in'",
        "Massivga element yozish uchun 'Array<in Int>' proyeksiyasidan foydalaning.",
        """fun fillWithZeros(arr: Array<in Int>, count: Int) {
    for (i in 0 until count) {
        arr[i] = 0 // Faqat yozish mumkin
    }
}

fun main() {
    val objects: Array<Any> = arrayOf("A", "B", "C")
    // Array<Any> ga Array<in Int> sifatida xavfsiz yoziladi:
    fillWithZeros(objects, 2)

    println("Natija: ${objects.joinToString()}")
}""",
        "'Array<in Int>' Java dagi '? super Integer' ga to'g'ri keladi. Bu massivga kamida Int yoki uning ota turlarini yozish xavfsiz ekanligini kompilyatorga tasdiqlaydi.",
        """Natija: 0, 0, C"""
    ),
    (
        558,
        "Star-projection (Yulduzcha proyeksiyasi '*'): Noma'lum tur",
        "Turi noma'lum bo'lgan ro'yxat elementlari sonini va birinchi elementini xavfsiz chop etish uchun 'List<*>' dan foydalaning.",
        """fun printListInfo(list: List<*>) {
    println("Ro'yxat hajmi: ${list.size}")
    if (list.isNotEmpty()) {
        val firstItem: Any? = list[0]
        println("Birinchi element: $firstItem")
    }
}

fun main() {
    printListInfo(listOf(10, 20, 30))
    printListInfo(listOf("Toshkent", "Buxoro"))
}""",
        "'List<*>' (star projection) Java dagi 'List<?>' ga to'g'ri keladi. Bu generik argument turi noma'lum ekanligini, ammo tur xavfsizligini saqlash kerakligini bildiradi. O'qilganda qiymatlar 'Any?' sifatida olinadi.",
        """Ro'yxat hajmi: 3
Birinchi element: 10
Ro'yxat hajmi: 2
Birinchi element: Toshkent"""
    ),
    (
        559,
        "Tur o'chirilishi (Type Erasure) va uning oqibatlari",
        "JVM da ish vaqtida generik turlar o'chib ketishini va 'is List<String>' tekshiruvi nega xatolik berishini tushuntiring.",
        """fun checkType(list: List<Any>) {
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
}""",
        "JVM platformasida orqaga moslik uchun barcha generik parametrlar kompilyatsiyadan so'ng o'chirib tashlanadi (Type Erasure). Ish vaqtida (runtime) 'List<String>' va 'List<Int>' ikkalasi ham oddiy 'List' ga aylanadi. Shuning uchun 'is List<String>' deb to'g'ridan-to'g'ri tekshirib bo'lmaydi.",
        """Ro'yxatning birinchi elementi matn: Kotlin
Ro'yxat matnli emas yoki bo'sh"""
    ),
    (
        560,
        "Reified Type Parameters: Tur o'chirilishini chetlab o'tish",
        "'inline fun <reified T>' orqali ish vaqtida generik turini to'liq saqlab qoluvchi filtr funksiyasini yozing.",
        """inline fun <reified T> filterByType(list: List<Any>): List<T> {
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
}""",
        "'reified' (asliga keltirilgan) modifikatori faqat 'inline' funksiyalarda ishlaydi. Kompilyator funksiyani chaqirilgan joyga to'g'ridan-to'g'ri ko'chirgani sababli, 'T' o'rniga aniq 'String.class' yoki 'Integer.class' qo'yiladi. Bu 'is T' va 'T::class' kabi amallarni bajarishga to'liq ruxsat beradi.",
        """Faqat satrlar: [Salom, Dunyo]
Faqat butun sonlar: [1, 42]"""
    ),
    (
        561,
        "Generik cheklovlar: Yuqori chegara (Upper Bound : Type)",
        "Faqat 'Comparable' interfeysini amalga oshirgan turlar uchun ikkita qiymatning kattasini topuvchi generik metod yozing.",
        """fun <T : Comparable<T>> findMaximum(a: T, b: T): T {
    return if (a > b) a else b
}

fun main() {
    println("Sonlar kattasi: ${findMaximum(15, 28)}")
    println("Satrlar kattasi: ${findMaximum("Olma", "Banan")}")
}""",
        "'<T : UpperBound>' sintaksisi orqali generik turga cheklov qo'yiladi. Bu yerda 'T' faqat 'Comparable' bo'lishi mumkinligi belgilangani uchun 'a > b' operatori xavfsiz ishlaydi.",
        """Sonlar kattasi: 28
Satrlar kattasi: Olma"""
    ),
    (
        562,
        "Ko'p shartli cheklovlar: 'where' bandi (Multiple Bounds)",
        "Bitta generik tur bir vaqtning o'zida ikkita har xil interfeysni (masalan CharSequence va Comparable) amalga oshirishini talab qiling.",
        """fun <T> processSpecialText(item: T) where T : CharSequence, T : Comparable<T> {
    if (item.length > 5) {
        println("Uzun matn: $item")
    } else {
        println("Qisqa matn: $item")
    }
}

fun main() {
    processSpecialText("O'zbekiston")
    processSpecialText("Salom")
}""",
        "Agar generik parametrga bir nechta yuqori chegaralar talab qilinsa, funksiya oxirida 'where T : InterfaceA, T : InterfaceB' sintaksisi qo'llaniladi.",
        """Uzun matn: O'zbekiston
Qisqa matn: Salom"""
    ),
    (
        563,
        "Xavfli tip o'tkazishni bostirish: @Suppress('UNCHECKED_CAST')",
        "Kompilyator turini to'liq tekshira olmagan holatda ogohlantirishni xavfsiz o'chirish.",
        """class ObjectHolder {
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
}""",
        "Type Erasure tufayli 'as? T' tekshiruvi kompilyator tomonidan 'Unchecked cast' ogohlantirishi bilan belgilanadi. Agar dasturchi tur to'g'riligiga amin bo'lsa, '@Suppress(\"UNCHECKED_CAST\")' annotatsiyasini qo'yadi.",
        """Olingan ID: 1005"""
    ),
    (
        564,
        "Generik interfeyslar va ularni amalga oshirish usullari",
        "Repository andozasini generik interfeys orqali modellashtiring.",
        """interface Repository<T, ID> {
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
}""",
        "Generik interfeyslar ('Repository<T, ID>') biznes mantig'ini ma'lumotlar turidan to'liq ajratishga imkon beradi.",
        """Customer saqlandi: Jasur
Topildi: Customer(id=1, name=Jasur)"""
    ),
    (
        565,
        "Generik konstruktorlar va Fabrika metodlari",
        "Sinfning o'zi generik bo'lmasa-da, uning konstruktori yoki metodlari generik bo'lishini ko'rsating.",
        """class Converter {
    fun <F, T> convert(from: F, transform: (F) -> T): T {
        return transform(from)
    }
}

fun main() {
    val converter = Converter()
    val stringNumber = converter.convert(12345) { "SON_$it" }
    println("Konvertatsiya: $stringNumber")
}""",
        "Oddiy (no-generic) sinf ichida ham mustaqil generik metodlar e'lon qilinishi mumkin.",
        """Konvertatsiya: SON_12345"""
    ),
    (
        566,
        "Kovariant ro'yxatlar: Kotlinda List sukut bo'yicha out T",
        "Nima uchun Kotlinda 'List<String>' ni 'List<Any>' ga berish xavfsiz ekanligini tushuntiring.",
        """fun main() {
    val stringList: List<String> = listOf("A", "B", "C")
    // Kotlin standart kutubxonasida: public interface List<out E> : Collection<E>
    val anyList: List<Any> = stringList // 100% qonuniy!

    println("AnyList elementlari: $anyList")
}""",
        "Kotlinda standart 'List<out E>' faqat o'qish uchun mo'ljallangan (read-only). Unda 'add' yoki 'set' metodlari yo'qligi sababli, 'List<String>' ni 'List<Any>' deb qabul qilish mutlaqo xavfsizdir va 'out E' bilan belgilangan.",
        """AnyList elementlari: [A, B, C]"""
    ),
    (
        567,
        "Invariant to'plamlar: MutableList da out yo'qligi",
        "'MutableList' nima uchun kovariant bo'la olmasligini va xatolikni amalda ko'rsating.",
        """fun main() {
    val stringList: MutableList<String> = mutableListOf("A", "B")
    // val anyList: MutableList<Any> = stringList // Kompilyatsiya xatosi: Type mismatch!
    
    // Nima uchun taqiqlangan? Chunki agar ruxsat berilsa:
    // anyList.add(100) // String ro'yxatiga Int tushib qolardi!
    
    println("MutableList invariant: $stringList")
}""",
        "'MutableList<E>' o'zgaruvchan bo'lgani uchun invariantdir. Unga yangi elementlar qo'shish mumkinligi sababli, tur buzilishining oldini olish uchun kovariantlik taqiqlangan.",
        """MutableList invariant: [A, B]"""
    ),
    (
        568,
        "Star-projection bilan Kolleksiya bo'shligini tekshirish",
        "Har qanday turdagi ro'yxatning bo'sh emasligini tekshiruvchi funksiya.",
        """fun hasElements(collection: Collection<*>): Boolean {
    return collection.isNotEmpty()
}

fun main() {
    println("Sonlar ro'yxati: ${hasElements(listOf(1, 2))}")
    println("Bo'sh ro'yxat: ${hasElements(emptyList<String>())}")
}""",
        "Elementlarning aniq turi muhim bo'lmaganda (faqat hajm, bo'shlik tekshirilganda) star-projection '*' eng toza sintaksisni beradi.",
        """Sonlar ro'yxati: true
Bo'sh ro'yxat: false"""
    ),
    (
        569,
        "Reified Type bilan JSON Parser analogi",
        "Sinf turini uzatmasdan to'g'ridan-to'g'ri tur bo'yicha ma'lumotni shakllantirish.",
        """inline fun <reified T> createEmptyInstanceName(): String {
    return "Yangi obyekt turi: ${T::class.simpleName}"
}

fun main() {
    println(createEmptyInstanceName<String>())
    println(createEmptyInstanceName<Double>())
}""",
        "'reified' orqali Java dagi noqulay 'Class<T> clazz' parametrini uzatishdan butunlay xalos bo'linadi.",
        """Yangi obyekt turi: String
Yangi obyekt turi: Double"""
    ),
    (
        570,
        "Generik cheklovlar: Sonli arifmetika bilan ishlash",
        "Har qanday raqamli turni qabul qilib, uning ikki karra qiymatini Double da hisoblash.",
        """fun <T : Number> doubleValue(number: T): Double {
    return number.toDouble() * 2.0
}

fun main() {
    println("Int 10: ${doubleValue(10)}")
    println("Double 5.5: ${doubleValue(5.5)}")
    println("Float 3.0f: ${doubleValue(3.0f)}")
}""",
        "'T : Number' chegarasi barcha sonli turlarning umumiy ota sinfiga tayanadi.",
        """Int 10: 20.0
Double 5.5: 11.0
Float 3.0f: 6.0"""
    ),
    (
        571,
        "Kovariant Daraxt Tuguni (Covariant Tree Node)",
        "O'zgarmas ikkilik daraxt tugunini 'out T' orqali modellashtiring.",
        """class BinaryNode<out T>(val value: T, val left: BinaryNode<T>? = null, val right: BinaryNode<T>? = null)

fun main() {
    val intNode: BinaryNode<Int> = BinaryNode(10)
    // Kovariantlik tufayli BinaryNode<Number> ga biriktirish mumkin:
    val numNode: BinaryNode<Number> = intNode

    println("Tugun qiymati: ${numNode.value}")
}""",
        "O'zgarmas daraxt tuzilmalari 'out T' orqali to'liq polimorfik iyerarxiyalarga xizmat qila oladi.",
        """Tugun qiymati: 10"""
    ),
    (
        572,
        "Kontravariant Komparator (Contravariant Comparator)",
        "Ota sinf komparatorini bola sinflar uchun ishlatish.",
        """open class Animal(val weight: Double)
class Dog(weight: Double, val breed: String) : Animal(weight)

val animalWeightComparator = Comparator<Animal> { a1, a2 ->
    a1.weight.compareTo(a2.weight)
}

fun main() {
    val dogs = listOf(Dog(12.5, "Taksa"), Dog(35.0, "Ovtcharka"))
    // Comparator<in Dog> talab qilingan joyga Comparator<Animal> xavfsiz beriladi:
    val sortedDogs = dogs.sortedWith(animalWeightComparator)

    println("Vazni bo'yicha birinchi it: ${sortedDogs.first().breed}")
}""",
        "Java va Kotlinda 'Comparator<in T>' kontravariant bo'lib, umumiy ota sinf solishtiruvchisini barcha subklasslar uchun qayta ishlatish imkonini beradi.",
        """Vazni bo'yicha birinchi it: Taksa"""
    ),
    (
        573,
        "Generik Stack (To'plam) ma'lumotlar tuzilmasi",
        "LIFO (Last-In-First-Out) tamoyilida ishlovchi xavfsiz generik Stack yarating.",
        """class SimpleStack<T> {
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
}""",
        "Klassik ma'lumotlar tuzilmalarini generiklar bilan xavfsiz amalga oshirish.",
        """Oxirgi element (peek): Ikkinchi
Sug'urib olindi (pop): Ikkinchi
Qolgan oxirgi: Birinchi"""
    ),
    (
        574,
        "Generik Pair va Custom Tuple sinflari",
        "Ikki xil turdagi qiymatlarni bitta generik obyektda bog'lash.",
        """data class KeyValue<K, V>(val key: K, val value: V)

fun main() {
    val entry = KeyValue("foydalanuvchi_id", 1009)
    println("Kalit: ${entry.key} | Qiymat: ${entry.value}")
}""",
        "Turli ma'lumotlar juftliklarini generik data class larda saqlash.",
        """Kalit: foydalanuvchi_id | Qiymat: 1009"""
    ),
    (
        575,
        "Reified Type bilan Bundle yoki Map dan xavfsiz o'qish",
        "Android Intent/Bundle kabi xaritadan tur bo'yicha o'qib beruvchi inline yordamchi tuzing.",
        """class SafeDataMap(private val map: Map<String, Any>) {
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
}""",
        "'reified' orqali dinamik xaritalardan kerakli turni xatosiz o'qib olish.",
        """Yosh (Int): 25
Noto'g'ri tur so'ralganda: null"""
    ),
    (
        576,
        "Generik metodlarda standart parametrlar",
        "Generik parametrga standart funksiya yoki qiymat biriktirish.",
        """fun <T> formatList(list: List<T>, formatter: (T) -> String = { it.toString() }): String {
    return list.joinToString(", ", transform = formatter)
}

fun main() {
    val numbers = listOf(1, 2, 3)
    println(formatList(numbers))
    println(formatList(numbers) { "Son_$it" })
}""",
        "Generik funksiyalarda standart parametrlar kodni yanada moslashuvchan qiladi.",
        """1, 2, 3
Son_1, Son_2, Son_3"""
    ),
    (
        577,
        "Generiklar bilan Builder Pattern",
        "Tur xavfsiz Builder obyektini modellashtirish.",
        """class EntityBuilder<T>(val factory: () -> T) {
    fun build(): T = factory()
}

fun main() {
    val strBuilder = EntityBuilder { "Yangi Satr Obyekti" }
    println("Qurildi: ${strBuilder.build()}")
}""",
        "Fabrika va Builder larni generiklar orqali abstraktlashtirish.",
        """Qurildi: Yangi Satr Obyekti"""
    ),
    (
        578,
        "Generik cheklov bilan Minimal elementni topish",
        "Comparable bo'lgan ro'yxatdan eng kichik qiymatni topuvchi funksiya.",
        """fun <T : Comparable<T>> findMinItem(items: List<T>): T? {
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
}""",
        "Comparable chegarasi bilan generic taqqoslash algoritmi.",
        """Min son: 3
Min satr: Anor"""
    ),
    (
        579,
        "Star-projection va Kolleksiya elementlarini sanash",
        "Kolleksiya ichidagi null bo'lmagan elementlar sonini sanovchi generik funksiya.",
        """fun countNonNull(items: Iterable<*>): Int {
    var count = 0
    for (item in items) {
        if (item != null) count++
    }
    return count
}

fun main() {
    val list = listOf(1, null, "A", null, 3.14)
    println("Null bo'lmaganlar: ${countNonNull(list)} ta")
}""",
        "Star-projection orqali istalgan turdagi to'plam elementlarini xavfsiz aylanib chiqish.",
        """Null bo'lmaganlar: 3 ta"""
    ),
    (
        580,
        "Generik Pipeline: Ma'lumotlarni o'zgartirish zanjiri",
        "Kirish va chiqish turlari har xil bo'lgan funksional quvur.",
        """class Step<I, O>(val transform: (I) -> O) {
    fun <Next> andThen(nextStep: (O) -> Next): Step<I, Next> {
        return Step { input -> nextStep(this.transform(input)) }
    }
}

fun main() {
    val pipeline = Step<String, Int> { it.length }
        .andThen { it * 10 }
        .andThen { "Natija: $it ball" }

    println(pipeline.transform("Kotlin"))
}""",
        "Zanjirli generik qadamlar (Monad / Pipeline) orqali ma'lumotlarni bosqichma-bosqich o'zgartirish.",
        """Natija: 60 ball"""
    ),
    (
        581,
        "Kovariantlikda metod parametriga 'out' turini berish cheklovi",
        "Nima uchun 'out T' modifikatorli interfeysda 'fun add(item: T)' yozish taqiqlanganligini tushuntiring.",
        """// interface InvalidProducer<out T> {
//     fun add(item: T) // Kompilyatsiya xatosi: Type parameter T is declared as 'out' but occurs in 'in' position
// }

interface ValidProducer<out T> {
    fun get(): T // Qonuniy (out position)
}

fun main() {
    println("Kovariantlik qoidasi: 'out' faqat chiqish joyida bo'ladi.")
}""",
        "Agar 'out T' ga metod parametri (in position) berilsa, subtyping xavfsizligi buziladi. Shu sababli Kotlin kompilyatori 'Type parameter occurs in in-position' xatoligi bilan buni qat'iy to'xtatadi.",
        """Kovariantlik qoidasi: 'out' faqat chiqish joyida bo'ladi."""
    ),
    (
        582,
        "@UnsafeVariance annotatsiyasi: Istisno holatlar",
        "Kovariant sinfda qidiruv metodiga element uzatish uchun '@UnsafeVariance' dan ehtiyotkorlik bilan foydalanish.",
        """interface SafeList<out E> {
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
}""",
        "Ba'zan o'qish uchun mo'ljallangan sinflarda (masalan Set.contains) elementni faqat solishtirish uchun qabul qilish talab etiladi. Bunday xavfsiz holatlarda '@UnsafeVariance' qo'yiladi.",
        """2 mavjudmi: true"""
    ),
    (
        583,
        "Generik xususiyatlar (Generic Extension Properties)",
        "Kolleksiyaning ikkinchi elementini xavfsiz oluvchi kengaytma xususiyati.",
        """val <T> List<T>.secondItem: T?
    get() = if (size >= 2) this[1] else null

fun main() {
    println("Sonlar: ${listOf(10, 20).secondItem}")
    println("Satrlar: ${listOf("Bir").secondItem}")
}""",
        "Kengaytma xususiyatlar ham to'liq generik bo'lishi mumkin.",
        """Sonlar: 20
Satrlar: null"""
    ),
    (
        584,
        "Reified Type bilan Enum qiymatlarini topish",
        "Berilgan satr bo'yicha enum qiymatini topuvchi ixcham reified metod.",
        """inline fun <reified E : Enum<E>> findEnumByName(name: String): E? {
    return enumValues<E>().firstOrNull { it.name.equals(name, ignoreCase = true) }
}

enum class Color { RED, GREEN, BLUE }

fun main() {
    val c = findEnumByName<Color>("green")
    println("Topilgan rang: $c")
}""",
        "'reified' generiklar yordamida enum turlarini tekshirish juda qisqa va qulay yoziladi.",
        """Topilgan rang: GREEN"""
    ),
    (
        585,
        "Generik Kesh xaritasi (Thread-safe Generic Cache)",
        "Ixtiyoriy kalit va qiymatlar uchun keshlovchi generik sinf.",
        """class MemoryCache<K, V> {
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
}""",
        "Generik kesh sinflari loyihada barcha modellar uchun qayta ishlatiladi.",
        """v1: 25, v2 (keshdan): 25"""
    ),
    (
        586,
        "Generik cheklovda Rekursiv Bog'lanish (Recursive Type Bound)",
        "Comparable<T> kabi o'zini o'zi cheklovchi generik parametrlar.",
        """abstract class OrderedItem<T : OrderedItem<T>> : Comparable<T>

class PriorityTask(val priority: Int) : OrderedItem<PriorityTask>() {
    override fun compareTo(other: PriorityTask): Int {
        return this.priority.compareTo(other.priority)
    }
}

fun main() {
    val t1 = PriorityTask(1)
    val t2 = PriorityTask(2)
    println("t1 < t2: ${t1 < t2}")
}""",
        "Rekursiv tur chegarasi ('T : OrderedItem<T>') obyekt faqat o'zi bilan bir xil turdagi obyektlar bilan solishtirilishini kafolatlaydi.",
        """t1 < t2: true"""
    ),
    (
        587,
        "Generik Obyekt Fabrikasi: Provider interfeysi",
        "Obyektlarni yaratib beruvchi generik shartnoma.",
        """interface Provider<T> {
    fun get(): T
}

class StringProvider : Provider<String> {
    override fun get(): String = "Yangi Matn"
}

fun main() {
    val p: Provider<String> = StringProvider()
    println(p.get())
}""",
        "Dependency Injection va Factory andozalarida generik 'Provider<T>' asosiy komponentdir.",
        """Yangi Matn"""
    ),
    (
        588,
        "Reified Type bilan Ro'yxat elementlarini tekshirish",
        "Ro'yxatdagi barcha elementlar ma'lum bir turga tegishli ekanligini tasdiqlash.",
        """inline fun <reified T> allInstancesOf(list: List<Any>): Boolean {
    return list.all { it is T }
}

fun main() {
    println("Barchasi satrmi: ${allInstancesOf<String>(listOf("A", "B", "C"))}")
    println("Barchasi satrmi (aralash): ${allInstancesOf<String>(listOf("A", 1, "C"))}")
}""",
        "'allInstancesOf' yordamida 'list.all { it is T }' amali reified tufayli to'liq ishlaydi.",
        """Barchasi satrmi: true
Barchasi satrmi (aralash): false"""
    ),
    (
        589,
        "Generik Result Wrapper: Data, Error va Loading",
        "Ixtiyoriy ma'lumotni o'rovchi 'Resource<T>' arxitektura sinfi.",
        """sealed class Resource<out T> {
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
}""",
        "'Resource<out T>' kovariantligi 'Nothing' bilan birlashganda Error va Loading holatlarini ixtiyoriy 'Resource<T>' ga xavfsiz biriktirish imkonini beradi.",
        """Muvaffaqiyatli: Ma'lumotlar"""
    ),
    (
        590,
        "Generiklar bilan Ro'yxatni teskarisiga aylantirish",
        "O'zgarmas generik ro'yxatni teskari o'giruvchi shaxsiy metod.",
        """fun <T> List<T>.customReversed(): List<T> {
    val result = ArrayList<T>(size)
    for (i in size - 1 downTo 0) {
        result.add(this[i])
    }
    return result
}

fun main() {
    val list = listOf(1, 2, 3, 4)
    println("Teskari ro'yxat: ${list.customReversed()}")
}""",
        "Generik kengaytma funksiyasi orqali ixtiyoriy ro'yxatni teskarisiga o'girish.",
        """Teskari ro'yxat: [4, 3, 2, 1]"""
    ),
    (
        591,
        "Generik sinfda bir nechta tur parametrlari: Triplet",
        "Uch xil turdagi qiymatlarni bitta generik obyektda birlashtiring.",
        """data class Triplet<A, B, C>(val first: A, val second: B, val third: C)

fun main() {
    val info = Triplet("Foydalanuvchi", 101, true)
    println("Ism: ${info.first}, ID: ${info.second}, Faol: ${info.third}")
}""",
        "Uchta alohida generik parametr orqali ma'lumotlarni turlari bo'yicha bog'lash.",
        """Ism: Foydalanuvchi, ID: 101, Faol: true"""
    ),
    (
        592,
        "Generik Mapper interfeysi",
        "Bitta modelni ikkinchi modelga o'tkazuvchi generik shartnoma.",
        """interface Mapper<in I, out O> {
    fun map(input: I): O
}

class IntToStringMapper : Mapper<Int, String> {
    override fun map(input: Int): String = "Son qiymati: $input"
}

fun main() {
    val mapper: Mapper<Int, String> = IntToStringMapper()
    println(mapper.map(500))
}""",
        "'Mapper<in I, out O>' da kirish 'in', chiqish esa 'out' modifikatorlari bilan to'liq to'g'ri loyihalashtirilgan.",
        """Son qiymati: 500"""
    ),
    (
        593,
        "Reified Type bilan Filtr: findFirstInstance",
        "Kolleksiyadagi ma'lum turdagi birinchi elementni qaytaruvchi inline metod.",
        """inline fun <reified T> findFirstInstance(list: List<Any>): T? {
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
}""",
        "'reified' orqali birinchi mos turdagi elementni topish.",
        """Birinchi satr: Matn
Birinchi double: 3.14"""
    ),
    (
        594,
        "Generik cheklovda Enum klassini talab qilish: <E : Enum<E>>",
        "Faqat Enum turlari bilan ishlaydigan generik metod yozing.",
        """fun <E : Enum<E>> printEnumDetails(enumConstant: E) {
    println("Enum nomi: ${enumConstant.name}, Tartibi: ${enumConstant.ordinal}")
}

enum class Status { ACTIVE, DISABLED }

fun main() {
    printEnumDetails(Status.ACTIVE)
}""",
        "'<E : Enum<E>>' chegarasi parametr faqat Enum turlariga mansub bo'lishini kafolatlaydi.",
        """Enum nomi: ACTIVE, Tartibi: 0"""
    ),
    (
        595,
        "Generik kolleksiyani birlashtirish: customFlatten",
        "Ichma-ich ro'yxatlarni bitta tekis ro'yxatga keltiruvchi generik funksiya.",
        """fun <T> List<List<T>>.customFlatten(): List<T> {
    val result = ArrayList<T>()
    for (sublist in this) {
        result.addAll(sublist)
    }
    return result
}

fun main() {
    val nested = listOf(listOf(1, 2), listOf(3, 4, 5))
    println("Tekislangan ro'yxat: ${nested.customFlatten()}")
}""",
        "Ichma-ich ro'yxatlarni 'flatten' qilish generik kengaytmasi.",
        """Tekislangan ro'yxat: [1, 2, 3, 4, 5]"""
    ),
    (
        596,
        "Generiklar bilan Shartli taqqoslash: areEqual",
        "Ikki generik obyektning tengligini tekshirish.",
        """fun <T> areEqual(a: T, b: T): Boolean = a == b

fun main() {
    println("Tenglik (Int): ${areEqual(10, 10)}")
    println("Tenglik (String): ${areEqual("A", "B")}")
}""",
        "Generik tenglik tekshiruvi Kotlinda xavfsiz 'equals' ga kompilyatsiya bo'ladi.",
        """Tenglik (Int): true
Tenglik (String): false"""
    ),
    (
        597,
        "Generik Predikatlar bilan Kolleksiya bo'lish",
        "Generik ro'yxatni predikatga ko'ra ikkiga ajratish.",
        """fun <T> splitByPredicate(list: List<T>, predicate: (T) -> Boolean): Pair<List<T>, List<T>> {
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
}""",
        "Generik predikatlar bilan ma'lumotlarni saralash.",
        """Musbat: [1, 3] | Manfiy: [-2, -4]"""
    ),
    (
        598,
        "Kovariantlik va Kontravariantlikni birga qo'llash: Data Transformer",
        "Kirish va chiqish kanallari bo'lgan transformator sinfi.",
        """interface DataChannel<in Input, out Output> {
    fun process(item: Input): Output
}

class LengthChannel : DataChannel<String, Int> {
    override fun process(item: String): Int = item.length
}

fun main() {
    val channel: DataChannel<String, Int> = LengthChannel()
    println("Natija: ${channel.process("KotlinGenerics")}")
}""",
        "'in' va 'out' parametrlarini bitta interfeysda to'g'ri joylashtirish.",
        """Natija: 14"""
    ),
    (
        599,
        "Generik xususiyatlar bilan O'zgarmas Singleton to'plami",
        "Bo'sh ro'yxatni generik xususiyat orqali taqdim etish.",
        """val <T> emptyGenericList: List<T>
    get() = emptyList()

fun main() {
    val list1: List<String> = emptyGenericList
    val list2: List<Int> = emptyGenericList
    println("list1 bo'sh: ${list1.isEmpty()}, list2 bo'sh: ${list2.isEmpty()}")
}""",
        "Generik kengaytma xususiyatlari orqali bo'sh xavfsiz to'plamlarni olish.",
        """list1 bo'sh: true, list2 bo'sh: true"""
    ),
    (
        600,
        "Generiklar bo'yicha to'liq amaliy xulosa: Korxona Ma'lumotlar Bazasi va Resurs Repozitoriysi",
        "Generic class, In/Out variance, Reified inline funksiya, Generic constraints va Type projections ni bitta yaxlit tizimda birlashtiring.",
        """interface IdentifiableEntity<ID> {
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
}""",
        "Ushbu yakuniy topshiriqda talab qilingan barcha generik vositalar: Generik klass va interfeys, 'out' kovariantligi ('EntityReader<out T>'), generik cheklovlar ('T : IdentifiableEntity<ID>', 'ID : Comparable<ID>'), hamda 'inline fun <reified T>' reified hisoboti bitta to'laqonli korxona repozitoriysida mukammal birlashtirildi.",
        """[SAQLANDI]: Entity #101
[SAQLANDI]: Entity #102
=== HISOBOT: UserAccount (Jami: 2 ta) ===
 - ID: 101
 - ID: 102"""
    )
]

for item in data_12:
    n, title, condition, sol, exp, res = item
    tasks.append(format_task(n, title, condition, sol, exp, res))

save_file("kotlin_12_generiklar_generics.md", tasks)
