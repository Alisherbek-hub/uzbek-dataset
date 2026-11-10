# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(r"C:\Users\User\Desktop\uzbek_dataset\kodlar\kotlin\_generators")
from task_builder import format_task, save_file

tasks = []

def add_task(num, title, cond, code, exp, res):
    tasks.append(format_task(num, title, cond, code, exp, res))

# 801
add_task(
    801,
    "flow { emit() } yordamida oddiy sovuq oqim (Cold Flow) yaratish",
    "Kotlin Flow yordamida 1 dan 3 gacha bo'lgan sonlarni har 100ms da chiqaruvchi oqim hosil qiling va uni collect() orqali o'qing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.delay

fun simpleNumberFlow(): Flow<Int> = flow {
    for (i in 1..3) {
        delay(100L)
        emit(i)
    }
}

fun main() = runBlocking {
    println("Oqimga obuna bo'linmoqda...")
    simpleNumberFlow().collect { value ->
        println("Qabul qilindi: $value")
    }
    println("Oqim yakunlandi.")
}
""",
    "flow { } builderi asinxron qiymatlar ketma-ketligini (Cold Stream) yaratadi. emit() har bir yangi qiymatni oqimga yuboradi, collect() esa ularni qabul qilib oladi.",
    """
Oqimga obuna bo'linmoqda...
Qabul qilindi: 1
Qabul qilindi: 2
Qabul qilindi: 3
Oqim yakunlandi.
"""
)

# 802
add_task(
    802,
    "flowOf(...) va asFlow() yordamida oqim hosil qilish",
    "Mavjud qiymatlar va ro'yxatni flowOf hamda .asFlow() yordamida Flow ga aylantirishni namoyish eting.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.asFlow

fun main() = runBlocking {
    val fruitFlow = flowOf("Olma", "Anor", "Uzum")
    fruitFlow.collect { println("Meva: $it") }
    
    val listFlow = listOf(10, 20, 30).asFlow()
    listFlow.collect { println("Son: $it") }
}
""",
    "flowOf berilgan argumentlardan tayyor oqim hosil qiladi, .asFlow() kengaytmasi esa Iterable yoki Sequence kolleksiyalarini to'g'ridan-to'g'ri Flow ga aylantiradi.",
    """
Meva: Olma
Meva: Anor
Meva: Uzum
Son: 10
Son: 20
Son: 30
"""
)

# 803
add_task(
    803,
    "Cold Stream xususiyati: collect chaqirilmaguncha kod ishlamasligi",
    "Oqim ichidagi loglar faqat collect() chaqirilgandagina ekranga chiqishini, ungacha hech qanday hisoblash bo'lmasligini ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.delay

fun lazyDataStream() = flow {
    println(">>> Flow hisoblashni BOSHLADI <<<")
    emit("A")
    emit("B")
}

fun main() = runBlocking {
    println("Oqim yaratildi, lekin hali collect chaqirilmadi.")
    val stream = lazyDataStream()
    delay(200L)
    
    println("Endi collect chaqiramiz:")
    stream.collect { println("Olingan: $it") }
}
""",
    "Flow - bu sovuq (cold) oqim. U buyurtma asosida ishlaydi: hech kim collect qilmasa, uning ichidagi hech qanday kod ishga tushmaydi va resurs sarflanmaydi.",
    """
Oqim yaratildi, lekin hali collect chaqirilmadi.
Endi collect chaqiramiz:
>>> Flow hisoblashni BOSHLADI <<<
Olingan: A
Olingan: B
"""
)

# 804
add_task(
    804,
    "Har bir yangi collect() yangi mustaqil oqim boshlashi",
    "Bitta Flow ga ikki marta collect() chaqirilganda har biri o'zining mustaqil hisoblash siklini ishga tushirishini ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flow

fun generateSensorData() = flow {
    println("Datchik ishga tushdi")
    emit(25)
}

fun main() = runBlocking {
    val sensor = generateSensorData()
    
    println("1-kuzatuvchi:")
    sensor.collect { println("1-qiymat: $it") }
    
    println("2-kuzatuvchi:")
    sensor.collect { println("2-qiymat: $it") }
}
""",
    "Har bir collect() chaqiruvi flow { } blokini qaytadan noldan boshlaydi. Shu bois har bir obunachi shaxsiy ma'lumotlar oqimiga ega bo'ladi.",
    """
1-kuzatuvchi:
Datchik ishga tushdi
1-qiymat: 25
2-kuzatuvchi:
Datchik ishga tushdi
2-qiymat: 25
"""
)

# 805
add_task(
    805,
    "flowOn operatori bilan faqat upstream oqimni IO ga o'tkazish",
    "Ma'lumot chiqarishni (emit) Dispatchers.IO da bajarib, uni asosiy oqimda collect qilishni ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.flowOn
import kotlinx.coroutines.Dispatchers

fun cpuIntensiveFlow() = flow {
    println("Emit oqimi: ${Thread.currentThread().name}")
    emit(100)
}.flowOn(Dispatchers.IO)

fun main() = runBlocking {
    println("Collect oqimi: ${Thread.currentThread().name}")
    cpuIntensiveFlow().collect { value ->
        println("Qabul qilindi: $value [${Thread.currentThread().name}]")
    }
}
""",
    "flowOn faqat o'zidan yuqorida (upstream) turgan operatsiyalar va flow { } blokining oqimini o'zgartiradi. Downstream (collect) esa chaqiruvchining oqimida qoladi.",
    """
Collect oqimi: main
Emit oqimi: DefaultDispatcher-worker-1
Qabul qilindi: 100 [main]
"""
)

# 806
add_task(
    806,
    "map operatori orqali ma'lumotlarni o'zgartirish",
    "Kelayotgan raqamlarni kvadratiga oshirib yangi formatga o'tkazuvchi oqim yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.map

fun main() = runBlocking {
    val numbers = flowOf(2, 3, 4)
    
    numbers
        .map { it * it }
        .map { "Kvadrat natija: $it" }
        .collect { println(it) }
}
""",
    "map operatori oraliq (intermediate) operator bo'lib, har bir elementni berilgan lambda orqali o'zgartirib keyingi bosqichga uzatadi.",
    """
Kvadrat natija: 4
Kvadrat natija: 9
Kvadrat natija: 16
"""
)

# 807
add_task(
    807,
    "filter operatori orqali saralash",
    "Kelayotgan to'lovlar oqimidan faqat 100 dollardan oshgan muvaffaqiyatli to'lovlarni ajratib oling.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.asFlow
import kotlinx.coroutines.flow.filter

data class Payment(val id: String, val amount: Double)

fun main() = runBlocking {
    val payments = listOf(
        Payment("P1", 50.0),
        Payment("P2", 250.0),
        Payment("P3", 80.0),
        Payment("P4", 190.0)
    ).asFlow()
    
    payments
        .filter { it.amount > 100.0 }
        .collect { println("Katta to'lov: ${it.id} (${it.amount} $)") }
}
""",
    "filter operatori berilgan shartga to'g'ri (true) kelgan elementlarnigina quyi oqimga o'tkazadi, qolganlarini tashlab yuboradi.",
    """
Katta to'lov: P2 (250.0 $)
Katta to'lov: P4 (190.0 $)
"""
)

# 808
add_task(
    808,
    "transform operatori orqali erkin emit qilish",
    "Har bir kelgan so'rov uchun bir nechta oraliq xabarlar chiqaruvchi transform operatorini qo'llang.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.transform

fun main() = runBlocking {
    flowOf("FaylA", "FaylB")
        .transform { file ->
            emit("Yuklash boshlandi: $file")
            emit("Yuklash tugadi: $file")
        }
        .collect { println(it) }
}
""",
    "transform operatori map va filter imkoniyatlarini birlashtiradi: u har bir kiruvchi element uchun 0 ta, 1 ta yoki bir nechta yangi qiymatlarni emit qila oladi.",
    """
Yuklash boshlandi: FaylA
Yuklash tugadi: FaylA
Yuklash boshlandi: FaylB
Yuklash tugadi: FaylB
"""
)

# 809
add_task(
    809,
    "take operatori orqali dastlabki elementlarni olish va to'xtatish",
    "Cheksiz oqimdan faqat dastlabki 3 ta elementni olib, qolganini avtomatik bekor qiling.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.take

fun infiniteSequence() = flow {
    var count = 1
    while (true) {
        emit(count++)
    }
}

fun main() = runBlocking {
    infiniteSequence()
        .take(3)
        .collect { println("Olingan son: $it") }
    println("Cheksiz oqim xavfsiz to'xtatildi.")
}
""",
    "take(N) operatori N ta element qabul qilingach, oqimga CancellationException yuborib uni xavfsiz to'xtatadi.",
    """
Olingan son: 1
Olingan son: 2
Olingan son: 3
Cheksiz oqim xavfsiz to'xtatildi.
"""
)

# 810
add_task(
    810,
    "drop operatori orqali dastlabki elementlarni tashlab yuborish",
    "Oqimdagi dastlabki 2 ta boshlang'ich sozlash qiymatini tashlab yuborib, qolganlarini qabul qiling.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.drop

fun main() = runBlocking {
    val configStream = flowOf("Init-1", "Init-2", "HaqiqiyMa'lumot-1", "HaqiqiyMa'lumot-2")
    
    configStream
        .drop(2)
        .collect { println("Amaldagi: $it") }
}
""",
    "drop(N) operatori boshlang'ich N ta elementni o'tkazib yuboradi va faqat undan keyingi kelgan barcha elementlarni quyi oqimga uzatadi.",
    """
Amaldagi: HaqiqiyMa'lumot-1
Amaldagi: HaqiqiyMa'lumot-2
"""
)

# 811
add_task(
    811,
    "first() terminal operatori bilan birinchi elementni olish",
    "Shartga mos keluvchi eng birinchi elementni topib, oqimni to'xtatuvchi dastur yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.asFlow
import kotlinx.coroutines.flow.first

fun main() = runBlocking {
    val numbers = listOf(5, 12, 17, 24, 30).asFlow()
    
    val firstEven = numbers.first { it % 2 == 0 }
    println("Birinchi juft son: $firstEven")
}
""",
    "first() terminal operatori shartni qanoatlantiruvchi eng birinchi qiymatni qaytaradi va oqimni darhol to'xtatadi.",
    """
Birinchi juft son: 12
"""
)

# 812
add_task(
    812,
    "toList() va toSet() orqali butun oqimni xotiradagi to'plamga yig'ish",
    "Oqim elementlarini to'liq kutib, ularni Kotlin List va Set to'plamlariga o'tkazing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.toList
import kotlinx.coroutines.flow.toSet

fun main() = runBlocking {
    val stream = flowOf("A", "B", "A", "C")
    
    val list = stream.toList()
    val set = stream.toSet()
    
    println("List: $list")
    println("Set: $set")
}
""",
    "toList() va toSet() oqim tugaguniga qadar barcha qiymatlarni to'playdi va tayyor kolleksiya sifatida qaytaradi.",
    """
List: [A, B, A, C]
Set: [A, B, C]
"""
)

# 813
add_task(
    813,
    "reduce va fold orqali oqim elementlarini yagona qiymatga yig'ish",
    "Oqimdan kelgan raqamlarni fold yordamida boshlang'ich qoldiq bilan birgalikda jamlang.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.fold
import kotlinx.coroutines.flow.reduce

fun main() = runBlocking {
    val numbers = flowOf(10, 20, 30)
    
    val sumWithInitial = numbers.fold(100) { acc, value -> acc + value }
    val product = numbers.reduce { acc, value -> acc * value }
    
    println("Boshlang'ich 100 bilan yig'indi: $sumWithInitial")
    println("Ko'paytma: $product")
}
""",
    "fold boshlang'ich qiymat qabul qiladi va barcha elementlarni akkumulyatorga jamlaydi. reduce esa birinchi elementni boshlang'ich qiymat sifatida oladi.",
    """
Boshlang'ich 100 bilan yig'indi: 160
Ko'paytma: 6000
"""
)

# 814
add_task(
    814,
    "onEach operatori bilan oraliq log yozish",
    "Elementlarning oqim bo'ylab harakatlanishini o'zgartirmasdan kuzatish uchun onEach dan foydalaning.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.asFlow
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.flow.map

fun main() = runBlocking {
    listOf("toshkent", "samarqand")
        .asFlow()
        .onEach { println("Xom qiymat: $it") }
        .map { it.uppercase() }
        .onEach { println("Katta harf: $it") }
        .collect { println("Ekranga chiqdi: $it") }
}
""",
    "onEach har bir element o'tganda ko'rsatilgan amalni (odatda log yozish yoki keshga qo'yish) bajaradi, lekin elementning o'zini o'zgartirmasdan quyi bosqichga o'tkazadi.",
    """
Xom qiymat: toshkent
Katta harf: TOSHKENT
Ekranga chiqdi: TOSHKENT
Xom qiymat: samarqand
Katta harf: SAMARQAND
Ekranga chiqdi: SAMARQAND
"""
)

# 815
add_task(
    815,
    "catch operatori orqali yuqoridagi xatoni ushlash va zaxira emit qilish",
    "Oqim ichida xato sodir bo'lganda dastur qulamasdan zaxira xabarni emit qiluvchi xavfsiz oqim tuzing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.catch

fun unstableStream() = flow {
    emit("Xabar-1")
    throw RuntimeException("Tarmoq kabeli uzildi!")
}

fun main() = runBlocking {
    unstableStream()
        .catch { e ->
            println("Xatolik ushlandi: ${e.message}")
            emit("Zaxira: Offline rejimdagi xabar")
        }
        .collect { println("Olingan: $it") }
}
""",
    "catch operatori faqat o'zidan yuqorida (upstream) yuz bergan istisnolarni ushlaydi va xohlasa oqimga yangi xavfsiz zaxira elementlarni emit qila oladi.",
    """
Olingan: Xabar-1
Xatolik ushlandi: Tarmoq kabeli uzildi!
Olingan: Zaxira: Offline rejimdagi xabar
"""
)

# 816
add_task(
    816,
    "onStart va onCompletion orqali oqim hayot siklini kuzatish",
    "Yuklanish boshlanganda 'Yuklanmoqda...', tugaganda esa 'Yuklandi' holatlarini beruvchi oqim yarating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.onStart
import kotlinx.coroutines.flow.onCompletion

fun main() = runBlocking {
    flowOf("Foydalanuvchi ma'lumotlari")
        .onStart { println("Hayot sikli: Oqim boshlandi") }
        .onCompletion { println("Hayot sikli: Oqim tugadi") }
        .collect { println("Kontent: $it") }
}
""",
    "onStart oqim obunachisi birinchi elementni olishdan avval chaqiriladi, onCompletion esa oqim normal yoki xatolik bilan tugaganda chaqiriladi.",
    """
Hayot sikli: Oqim boshlandi
Kontent: Foydalanuvchi ma'lumotlari
Hayot sikli: Oqim tugadi
"""
)

# 817
add_task(
    817,
    "onCompletion da xatolik sababini tahlil qilish",
    "onCompletion parametrida keluvchi Throwable orqali oqim qanday sabab bilan tugaganini aniqlang.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.onCompletion

fun riskyFlow() = flow<String> {
    emit("Boshlandi")
    throw IllegalStateException("Baza javob bermadi")
}

fun main() = runBlocking {
    riskyFlow()
        .onCompletion { cause ->
            if (cause != null) {
                println("Oqim xatolik bilan yakunlandi: ${cause.message}")
            } else {
                println("Oqim muvaffaqiyatli tugadi")
            }
        }
        .catch { /* xatoni so'ndirish */ }
        .collect { println("Ma'lumot: $it") }
}
""",
    "onCompletion blokining `cause` parametri oqim tinch yakunlansa `null`, agar istisno tashlansa o'sha istisno obyektini saqlaydi.",
    """
Ma'lumot: Boshlandi
Oqim xatolik bilan yakunlandi: Baza javob bermadi
"""
)

# 818
add_task(
    818,
    "buffer() operatori yordamida tezkor ishlab chiqaruvchi va sekin iste'molchini muvozanatlash",
    "Tez element ishlab chiqaruvchi oqim va har bir elementni uzoq qayta ishlovchi collect o'rtasida buffer() qo'yib umumiy vaqtni tejang.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.buffer
import kotlinx.coroutines.delay
import kotlin.system.measureTimeMillis

fun fastEmitter() = flow {
    for (i in 1..3) {
        delay(100L) // tez chiqaradi
        emit(i)
    }
}

fun main() = runBlocking {
    val vaqt = measureTimeMillis {
        fastEmitter()
            .buffer() // Emitter collect ni kutib turmaydi
            .collect { value ->
                delay(300L) // sekin iste'mol
                println("Iste'mol qilindi: $value")
            }
    }
    println("Umumiy vaqt: ~$vaqt ms")
}
""",
    "buffer() operatori emit qilish va collect qilish amallarini alohida koroutinalarga ajratib, o'rtaga bufer qo'yadi. Natijada emitter iste'molchini kutmasdan o'z ishini davom ettiradi.",
    """
Iste'mol qilindi: 1
Iste'mol qilindi: 2
Iste'mol qilindi: 3
Umumiy vaqt: ~1000 ms
"""
)

# 819
add_task(
    819,
    "conflate() yordamida oraliq eskirgan elementlarni tashlab yuborish",
    "Iste'molchi sekin ishlayotgan paytda oradagi yangi elementlar to'planib qolmasdan, faqat eng so'nggisini uzatishni ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.conflate
import kotlinx.coroutines.delay

fun rapidUpdates() = flow {
    for (i in 1..5) {
        delay(50L)
        emit(i)
    }
}

fun main() = runBlocking {
    rapidUpdates()
        .conflate()
        .collect { value ->
            println("Qabul qilindi: $value")
            delay(120L) // sekin iste'molchi
        }
}
""",
    "conflate() operatori iste'molchi band bo'lgan paytda kelgan oraliq qiymatlarni tashlab yuboradi va iste'molchi bo'shashi bilan unga eng so'nggi yangilangan qiymatni beradi.",
    """
Qabul qilindi: 1
Qabul qilindi: 3
Qabul qilindi: 5
"""
)

# 820
add_task(
    820,
    "collectLatest() yordamida eskirgan hisob-kitobni bekor qilish",
    "Yangi qiymat kelishi bilan hali tugab ulgurmagan avvalgi collect blokini to'xtatuvchi collectLatest ni qo'llang.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.delay

fun valueGenerator() = flow {
    emit(1)
    delay(100L)
    emit(2)
    delay(100L)
    emit(3)
}

fun main() = runBlocking {
    valueGenerator().collectLatest { value ->
        println("Boshlandi: $value")
        delay(200L) // 200ms kutolmaydi, chunki 100ms da yangi qiymat keladi!
        println("Yakunlandi: $value")
    }
}
""",
    "collectLatest yangi qiymat emit qilinganda, avvalgi qiymat ustida ishlayotgan koroutina blokini CancellationException orqali bekor qiladi va yangi qiymatni qayta ishlashga kirishadi.",
    """
Boshlandi: 1
Boshlandi: 2
Boshlandi: 3
Yakunlandi: 3
"""
)

# 821
add_task(
    821,
    "zip operatori orqali ikkita oqim elementlarini juftlab birlashtirish",
    "Ikkita turli tezlikdagi oqimni zip yordamida 1-ga-1 tartibida birlashtiruvchi kod yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.asFlow
import kotlinx.coroutines.flow.zip

fun main() = runBlocking {
    val english = listOf("One", "Two", "Three").asFlow()
    val uzbek = listOf("Bir", "Ikki", "Uch").asFlow()
    
    english.zip(uzbek) { en, uz -> "$en = $uz" }
        .collect { println(it) }
}
""",
    "zip operatori ikkala oqimdan kelgan elementlarni juft-juft qilib birlashtiradi. Oqimlarning biri tugasa, umumiy birlashgan oqim ham tugaydi.",
    """
One = Bir
Two = Ikki
Three = Uch
"""
)

# 822
add_task(
    822,
    "combine operatori orqali ikkita oqimning eng so'nggi qiymatlarini birlashtirish",
    "Foydalanuvchi ismi va uning onlayn holati o'zgarganda eng oxirgi holatni ko'rsatuvchi combine dasturini yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.flow

fun main() = runBlocking {
    val userFlow = flow {
        emit("Ali")
        delay(150L)
        emit("Vali")
    }
    
    val statusFlow = flow {
        emit("Offline")
        delay(50L)
        emit("Online")
    }
    
    userFlow.combine(statusFlow) { user, status ->
        "$user hozirda: $status"
    }.collect { println(it) }
}
""",
    "combine operatori oqimlarning birortasida yangi element paydo bo'lishi bilan, boshqa oqimning eng so'nggi (oxirgi) elementi bilan yangi natija hosil qiladi.",
    """
Ali hozirda: Offline
Ali hozirda: Online
Vali hozirda: Online
"""
)

# 823
add_task(
    823,
    "flatMapConcat orqali ketma-ket ichki Flow larni ochish",
    "Har bir kelgan buyurtma identifikatori uchun uning detallarini chiqaruvchi ichki oqimni ketma-ket ulab oching.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.flatMapConcat
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.delay

fun fetchDetails(orderId: String) = flow {
    emit("$orderId detal 1")
    delay(50L)
    emit("$orderId detal 2")
}

fun main() = runBlocking {
    flowOf("ORD-1", "ORD-2")
        .flatMapConcat { id -> fetchDetails(id) }
        .collect { println(it) }
}
""",
    "flatMapConcat bitta oqim elementini yangi ichki oqimga o'giradi va ularni qat'iy ketma-ket (avvalgi ichki oqim to'liq tugagach keyingisi) tartibda birlashtiradi.",
    """
ORD-1 detal 1
ORD-1 detal 2
ORD-2 detal 1
ORD-2 detal 2
"""
)

# 824
add_task(
    824,
    "flatMapMerge orqali ichki Flow larni parallel birlashtirish",
    "Bir nechta foydalanuvchi ma'lumotlarini parallel so'rovchi ichki Flow larni birlashtiring.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.flatMapMerge
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.delay

fun getUserLogs(user: String) = flow {
    delay(100L)
    emit("$user: Tizimga kirdi")
}

fun main() = runBlocking {
    flowOf("User1", "User2")
        .flatMapMerge { user -> getUserLogs(user) }
        .collect { println(it) }
}
""",
    "flatMapMerge ichki oqimlarni bir vaqtda parallel ishga tushiradi va ularning natijalarini qaysi biri tezroq kelsa o'sha tartibda birlashtirib beradi.",
    """
User1: Tizimga kirdi
User2: Tizimga kirdi
"""
)

# 825
add_task(
    825,
    "flatMapLatest orqali yangi kalit kelganda avvalgisini to'xtatish",
    "Qidiruv maydonida foydalanuvchi yangi harf yozganda avvalgi server so'rovi Flow ini to'xtatib yangisini boshlashni simulyatsiya qiling.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.delay

fun searchApi(query: String) = flow {
    println("Qidiruv boshlandi: $query")
    delay(150L)
    emit("Natija: $query uchun javob")
}

fun main() = runBlocking {
    flow {
        emit("Ko")
        delay(50L)
        emit("Kot")
        delay(50L)
        emit("Kotlin")
    }.flatMapLatest { query ->
        searchApi(query)
    }.collect { println(it) }
}
""",
    "flatMapLatest yangi so'rov paydo bo'lishi bilan avvalgi ichki oqimni CancellationException orqali to'xtatadi va yangi so'rov oqimini ochadi.",
    """
Qidiruv boshlandi: Ko
Qidiruv boshlandi: Kot
Qidiruv boshlandi: Kotlin
Natija: Kotlin uchun javob
"""
)

# 826
add_task(
    826,
    "distinctUntilChanged() bilan bir xil ketma-ket qiymatlarni filtrlash",
    "Ketma-ket bir xil takrorlangan qiymatlarni tashlab yuboruvchi filtrni qo'llang.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.distinctUntilChanged

fun main() = runBlocking {
    flowOf(1, 1, 2, 2, 2, 3, 1, 1)
        .distinctUntilChanged()
        .collect { println("Yangi qiymat: $it") }
}
""",
    "distinctUntilChanged() faqat avvalgi qiymatdan farq qiluvchi yangi elementlarnigina o'tkazadi. Ketma-ket kelgan nusxalar tashlab yuboriladi.",
    """
Yangi qiymat: 1
Yangi qiymat: 2
Yangi qiymat: 3
Yangi qiymat: 1
"""
)

# 827
add_task(
    827,
    "debounce() operatori orqali qidiruv maydonini sokinlashtirish",
    "Foydalanuvchi klaviaturada to'xtamasdan yozayotgan paytda ortiqcha so'rov yubormasdan, faqat 100ms pauza bo'lganda so'rov jo'nating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.debounce
import kotlinx.coroutines.delay

fun userInputFlow() = flow {
    emit("A")
    delay(40L)
    emit("An")
    delay(40L)
    emit("Ant")
    delay(150L) // foydalanuvchi to'xtadi!
    emit("Anti")
}

fun main() = runBlocking {
    userInputFlow()
        .debounce(100L)
        .collect { println("Serverga so'rov yuborildi: $it") }
}
""",
    "debounce(vaqt) yangi element kelgandan keyin ko'rsatilgan vaqt ichida boshqa yangi element kelmasa, o'sha elementni uzatadi.",
    """
Serverga so'rov yuborildi: Ant
Serverga so'rov yuborildi: Anti
"""
)

# 828
add_task(
    828,
    "retry va retryWhen operatorlari orqali xatolikda qayta ulanish",
    "Tarmoq uzilishi sodir bo'lganda 2 martagacha oqimni qayta boshlovchi retry operatorini yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.retry
import kotlinx.coroutines.flow.catch

var attempts = 0
fun unstableNetworkFlow() = flow {
    attempts++
    println("Ulanish urinishi: #$attempts")
    if (attempts < 3) {
        throw RuntimeException("Ulanish rad etildi!")
    }
    emit("Muvaffaqiyatli tarmoq oqimi")
}

fun main() = runBlocking {
    unstableNetworkFlow()
        .retry(2) { cause ->
            println("Qayta urinish uchun sabab: ${cause.message}")
            true
        }
        .catch { e -> println("Barcha urinishlar tugadi: ${e.message}") }
        .collect { println("Natija: $it") }
}
""",
    "retry operatori upstream da xatolik sodir bo'lganda oqimni boshidan qayta obuna qiladi (qayta ishga tushiradi).",
    """
Ulanish urinishi: #1
Qayta urinish uchun sabab: Ulanish rad etildi!
Ulanish urinishi: #2
Qayta urinish uchun sabab: Ulanish rad etildi!
Ulanish urinishi: #3
Natija: Muvaffaqiyatli tarmoq oqimi
"""
)

# 829
add_task(
    829,
    "MutableStateFlow yaratish va uning boshlang'ich qiymatini o'qish",
    "Android da UI State saqlashning asosi bo'lgan MutableStateFlow ni boshlang'ich qiymat bilan e'lon qiling va qiymatini o'zgartiring.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.MutableStateFlow

fun main() = runBlocking {
    val counterState = MutableStateFlow(0)
    
    println("Boshlang'ich holat: ${counterState.value}")
    
    counterState.value = 5
    println("Yangilangan holat: ${counterState.value}")
}
""",
    "StateFlow - bu doimo bitta joriy qiymatni o'zida saqlovchi issiq (hot) oqimdir. Uning joriy holatini .value orqali istalgan paytda sinxron o'qish mumkin.",
    """
Boshlang'ich holat: 0
Yangilangan holat: 5
"""
)

# 830
add_task(
    830,
    "StateFlow ga faqat o'qiladigan interfeys (asStateFlow) berish",
    "Enkapsulyatsiya qoidasiga binoan, ViewModel ichida MutableStateFlow ni tashqariga faqat o'qiluvchi StateFlow sifatida taqdim eting.",
    """
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class ProfileViewModel {
    private val _userName = MutableStateFlow("Mehmon")
    val userName: StateFlow<String> = _userName.asStateFlow()
    
    fun updateName(newName: String) {
        _userName.value = newName
    }
}

fun main() {
    val vm = ProfileViewModel()
    println("Dastlabki ism: ${vm.userName.value}")
    vm.updateName("Jasur")
    println("O'zgargan ism: ${vm.userName.value}")
}
""",
    "_userName xususiy (private) bo'lib, tashqaridagi kod faqat o'qiluvchi StateFlow orqali unga ulanadi va qiymatni to'g'ridan-to'g'ri o'zboshimchalik bilan o'zgartira olmaydi.",
    """
Dastlabki ism: Mehmon
O'zgargan ism: Jasur
"""
)

# 831
add_task(
    831,
    "MutableStateFlow.update { } atomik yangilash amali",
    "Konkurent sharoitda StateFlow qiymatini .update { } orqali poyga holatisiz xavfsiz yangilang.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers

fun main() = runBlocking {
    val totalCount = MutableStateFlow(0)
    
    val jobs = List(100) {
        launch(Dispatchers.Default) {
            totalCount.update { current -> current + 1 }
        }
    }
    jobs.forEach { it.join() }
    
    println("Atomik yangilash natijasi: ${totalCount.value}")
}
""",
    ".update { } funksiyasi ichki Compare-And-Set (CAS) siklidan foydalanib, hatto bir nechta oqim bir vaqtda chaqirsa ham qiymatning xavfsiz va aniq yangilanishini ta'minlaydi.",
    """
Atomik yangilash natijasi: 100
"""
)

# 832
add_task(
    832,
    "Bir nechta abonentlarning StateFlow qiymatini collect qilishi",
    "Bitta StateFlow ga 2 ta alohida koroutina obuna bo'lganda, ularning ikkalasi ham yangilanishlarni qabul qilishini ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val state = MutableStateFlow("Yuklanmoqda")
    
    val job1 = launch {
        state.collect { println("1-UI Ekran: $it") }
    }
    val job2 = launch {
        state.collect { println("2-Log tizimi: $it") }
    }
    
    delay(50L)
    state.value = "Muvaffaqiyatli yuklandi"
    delay(50L)
    
    job1.cancel()
    job2.cancel()
}
""",
    "StateFlow issiq (hot) oqim bo'lgani sababli, uning barcha abonentlari (subscribers) yangilanishlarni parallel va bir xil qabul qiladi.",
    """
1-UI Ekran: Yuklanmoqda
2-Log tizimi: Yuklanmoqda
1-UI Ekran: Muvaffaqiyatli yuklandi
2-Log tizimi: Muvaffaqiyatli yuklandi
"""
)

# 833
add_task(
    833,
    "MutableSharedFlow yaratish va bir martalik hodisani yuborish",
    "Toast xabarnomasi yoki ekran navigatsiyasi kabi bir martalik hodisalar uchun SharedFlow dan foydalaning.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val eventFlow = MutableSharedFlow<String>()
    
    val subscriber = launch {
        eventFlow.collect { event ->
            println("Hodisa qabul qilindi: $event")
        }
    }
    
    delay(50L) // obunachi ulanishini kutish
    eventFlow.emit("Xabar: Foydalanuvchi ro'yxatdan o'tdi")
    
    delay(50L)
    subscriber.cancel()
}
""",
    "SharedFlow o'zida holat (current value) saqlamaydi, balki kelgan xabarlarni barcha faol abonentlarga tarqatadi (broadcast event).",
    """
Hodisa qabul qilindi: Xabar: Foydalanuvchi ro'yxatdan o'tdi
"""
)

# 834
add_task(
    834,
    "SharedFlow da replay parametri yordamida kesh hosil qilish",
    "Yangi ulangan obunachiga oxirgi 2 ta xabarni qayta uzatuvchi (replay = 2) SharedFlow sozlang.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.launch

fun main() = runBlocking {
    val chatFlow = MutableSharedFlow<String>(replay = 2)
    
    chatFlow.emit("Xabar 1")
    chatFlow.emit("Xabar 2")
    chatFlow.emit("Xabar 3")
    
    println("Kechikkan foydalanuvchi ulandi:")
    val sub = launch {
        chatFlow.collect { println("O'qildi: $it") }
    }
    
    sub.cancel()
}
""",
    "replay = 2 parametri SharedFlow ga eng so'nggi 2 ta xabarni xotirada saqlab turishni va yangi obunachilarga darhol yetkazishni buyuradi.",
    """
Kechikkan foydalanuvchi ulandi:
O'qildi: Xabar 2
O'qildi: Xabar 3
"""
)

# 835
add_task(
    835,
    "StateFlow va SharedFlow o'rtasidagi farqlar",
    "StateFlow va SharedFlow xatti-harakatlarini solishtiruvchi tushuntirish va taqqoslash kodini yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.MutableSharedFlow

fun main() = runBlocking {
    // StateFlow doimo boshlang'ich qiymatga ega va distinctUntilChanged xususiyatiga ega
    val state = MutableStateFlow("Holat A")
    println("StateFlow qiymati: ${state.value}")
    
    // SharedFlow boshlang'ich qiymatga ega emas, hodisalar uchun ishlatiladi
    val shared = MutableSharedFlow<String>()
    println("SharedFlow replayCache hajmi: ${shared.replayCache.size}")
}
""",
    "StateFlow holat (State) uchun ishlatiladi: u har doim qiymatga ega, takroriy qiymatni emit qilmaydi. SharedFlow esa hodisalar (Events) uchun: har bir emit abonentlarga yetib boradi.",
    """
StateFlow qiymati: Holat A
SharedFlow replayCache hajmi: 0
"""
)

# 836
add_task(
    836,
    "stateIn operatori orqali oddiy Flow ni StateFlow ga aylantirish",
    "Muntazam ma'lumot beruvchi sovuq oqimni CoroutineScope ichida issiq StateFlow ga aylantiring.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.delay

fun ticker() = flow {
    var count = 1
    while (true) {
        delay(100L)
        emit(count++)
    }
}

fun main() = runBlocking {
    val stateFlow = ticker().stateIn(
        scope = this,
        started = SharingStarted.Eagerly,
        initialValue = 0
    )
    
    println("Boshlang'ich: ${stateFlow.value}")
    delay(250L)
    println("250ms dan keyin: ${stateFlow.value}")
}
""",
    "stateIn sovuq oqimni berilgan ko'lamda (scope) ishga tushirib, uni UI uchun qulay StateFlow ga aylantiradi.",
    """
Boshlang'ich: 0
250ms dan keyin: 2
"""
)

# 837
add_task(
    837,
    "SharingStarted.WhileSubscribed(5000L) strategiyasi",
    "Faqat kamida bitta faol UI obunachi bo'lganda oqimni saqlab turuvchi va 5 soniya ekran burilganda kutuvchi strategiyani namoyish eting.",
    """
import kotlinx.coroutines.flow.SharingStarted

fun main() {
    val strategy = SharingStarted.WhileSubscribed(5000L)
    println("Strategiya nomi: ${strategy.javaClass.simpleName}")
    println("Android tavsiyasi: Ekran aylanganda bekor bo'lishining oldini olish uchun 5000ms delay")
}
""",
    "WhileSubscribed(5000L) Android arxitekturasida standart bo'lib, oxirgi obunachi chiqib ketganidan so'ng 5 soniya kutadi va shundan keyingina resursni to'xtatadi.",
    """
Strategiya nomi: StartedWhileSubscribed
Android tavsiyasi: Ekran aylanganda bekor bo'lishining oldini olish uchun 5000ms delay
"""
)

# 838
add_task(
    838,
    "shareIn operatori orqali Flow ni SharedFlow ga aylantirish",
    "Tarmoqdan olingan oqimni barcha abonentlarga qayta so'rov yubormasdan tarqatish uchun shareIn dan foydalaning.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.shareIn
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

fun apiDataFlow() = flow {
    println(">>> Og'ir API so'rovi amalga oshirildi! <<<")
    emit("JSON ma'lumot")
}

fun main() = runBlocking {
    val shared = apiDataFlow().shareIn(this, SharingStarted.Lazily, replay = 1)
    
    launch { shared.collect { println("1-abonent: $it") } }
    delay(50L)
    launch { shared.collect { println("2-abonent: $it") } }
    
    delay(100L)
}
""",
    "shareIn sovuq oqimni faqat bitta marta bajaradi va uning natijasini bir nechta mustaqil obunachilarga ulashadi (multicast).",
    """
>>> Og'ir API so'rovi amalga oshirildi! <<<
1-abonent: JSON ma'lumot
2-abonent: JSON ma'lumot
"""
)

# 839
add_task(
    839,
    "callbackFlow orqali hodisalar tinglovchisini Flow ga aylantirish",
    "Tashqi hodisalar manbaini (masalan GPS yoki sensor tinglovchisi) callbackFlow yordamida oqimga aylantiring.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.callbackFlow
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

interface LocationListener {
    fun onLocationChanged(loc: String)
}

fun getLocationUpdates() = callbackFlow {
    val listener = object : LocationListener {
        override fun onLocationChanged(loc: String) {
            trySend(loc)
        }
    }
    
    println("GPS tinglovchisi ro'yxatdan o'tdi")
    listener.onLocationChanged("41.2995 N, 69.2401 E")
    
    awaitClose {
        println("GPS tinglovchisi to'xtatildi va xotiradan o'chirildi.")
    }
}

fun main() = runBlocking {
    val job = launch {
        getLocationUpdates().collect { loc ->
            println("Yangi manzil: $loc")
        }
    }
    
    delay(100L)
    job.cancel()
}
""",
    "callbackFlow ichida trySend() bilan hodisalar oqimga uzatiladi, awaitClose esa obunachi oqimni to'xtatganda listenerni tozalashni kafolatlaydi.",
    """
GPS tinglovchisi ro'yxatdan o'tdi
Yangi manzil: 41.2995 N, 69.2401 E
GPS tinglovchisi to'xtatildi va xotiradan o'chirildi.
"""
)

# 840
add_task(
    840,
    "channelFlow orqali parallel koroutinalardan turli oqimlarda emit qilish",
    "Bir vaqtda bir nechta parallel ishchilardan bitta umumiy oqimga send() orqali ma'lumot jo'natuvchi channelFlow tuzing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.channelFlow
import kotlinx.coroutines.launch

fun parallelNumbers() = channelFlow {
    launch {
        send("1-ishchi: ma'lumot")
    }
    launch {
        send("2-ishchi: ma'lumot")
    }
}

fun main() = runBlocking {
    parallelNumbers().collect { println(it) }
}
""",
    "Oddiy flow { } ichida boshqa koroutinadan emit() chaqirish qat'iyan taqiqlangan (Flow invariant). channelFlow esa ko'p oqimli parallel muhitda send() orqali element yuborishga ruxsat beradi.",
    """
1-ishchi: ma'lumot
2-ishchi: ma'lumot
"""
)

# 841
add_task(
    841,
    "Jonli valyuta kurslari generatori (Real-time Currency Ticker)",
    "Har 100ms da tasodifiy o'zgaruvchi valyuta narxini chiqaruvchi va 3 ta qiymatdan so'ng to'xtovchi jonli ticker yarating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.take
import kotlinx.coroutines.delay

data class Rate(val currency: String, val price: Double)

fun currencyRateFlow() = flow {
    val prices = listOf(12820.0, 12835.5, 12810.0)
    for (p in prices) {
        delay(100L)
        emit(Rate("USD/UZS", p))
    }
}

fun main() = runBlocking {
    currencyRateFlow()
        .take(3)
        .collect { println("Valyuta kursi: ${it.currency} -> ${it.price} so'm") }
}
""",
    "Real-time tizimlarda birja yoki valyuta monitoringi uchun Flow eng qulay va kam xotira sarflaydigan reaktiv vositadir.",
    """
Valyuta kursi: USD/UZS -> 12820.0 so'm
Valyuta kursi: USD/UZS -> 12835.5 so'm
Valyuta kursi: USD/UZS -> 12810.0 so'm
"""
)

# 842
add_task(
    842,
    "Sensor ma'lumotlarini silliqlash (Moving Average Flow)",
    "Harorat datchigidan kelayotgan ketma-ket har 3 ta qiymatning o'rtacha arifmetik qiymatini hisoblab beruvchi oqim yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.asFlow
import kotlinx.coroutines.flow.transform

fun main() = runBlocking {
    val rawTemps = listOf(20.0, 22.0, 24.0, 26.0, 28.0).asFlow()
    val window = mutableListOf<Double>()
    
    rawTemps.transform { temp ->
        window.add(temp)
        if (window.size > 3) window.removeAt(0)
        if (window.size == 3) {
            val avg = window.average()
            emit(avg)
        }
    }.collect { println("O'rtacha silliqlangan harorat: $it C") }
}
""",
    "transform operatori va oraliq bufer yordamida tebranishlarni silliqlovchi Moving Average filtri oson yaratiladi.",
    """
O'rtacha silliqlangan harorat: 22.0 C
O'rtacha silliqlangan harorat: 24.0 C
O'rtacha silliqlangan harorat: 26.0 C
"""
)

# 843
add_task(
    843,
    "Avtomatik to'ldirish (Autocomplete) qidiruv xizmati",
    "debounce, distinctUntilChanged va flatMapLatest operatorlarini birlashtirib professional qidiruv oqimini loyihalang.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.debounce
import kotlinx.coroutines.flow.distinctUntilChanged
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.delay

fun simulateSearchQuery(query: String) = flow {
    delay(50L)
    emit(listOf("$query natija 1", "$query natija 2"))
}

fun main() = runBlocking {
    val userTyping = flow {
        emit("K")
        delay(20L)
        emit("Ko")
        delay(20L)
        emit("Kot")
        delay(120L) // to'xtadi
    }
    
    userTyping
        .debounce(100L)
        .distinctUntilChanged()
        .flatMapLatest { q -> simulateSearchQuery(q) }
        .collect { results ->
            println("Serverdan kelgan qidiruv natijalari: $results")
        }
}
""",
    "Bu kombinatsiya mobil va veb ilovalardagi qidiruv maydonchalarining eng yuqori standartidir: ortiqcha harflar uchun so'rov ketmaydi va eski javoblar yangisini bosib ketmaydi.",
    """
Serverdan kelgan qidiruv natijalari: [Kot natija 1, Kot natija 2]
"""
)

# 844
add_task(
    844,
    "Fayl yuklash jarayonini (Progress Flow) kuzatish",
    "Fayl baytlarini uzatishda har 25% da foizni emit qiluvchi yuklash ko'rsatkichi oqimini yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.delay

fun downloadFileWithProgress() = flow {
    emit(0)
    for (p in 25..100 step 25) {
        delay(100L)
        emit(p)
    }
}

fun main() = runBlocking {
    downloadFileWithProgress().collect { progress ->
        println("Yuklanish ko'rsatkichi: [$progress%]")
    }
    println("Yuklash yakunlandi!")
}
""",
    "UI progressBar yoki loading indikatorlarini yangilab turish uchun Flow eng qulay usul hisoblanadi.",
    """
Yuklanish ko'rsatkichi: [0%]
Yuklanish ko'rsatkichi: [25%]
Yuklanish ko'rsatkichi: [50%]
Yuklanish ko'rsatkichi: [75%]
Yuklanish ko'rsatkichi: [100%]
Yuklash yakunlandi!
"""
)

# 845
add_task(
    845,
    "Tarmoq aloqasi holatini kuzatuvchi Flow (Connectivity Monitor)",
    "Tarmoq online/offline bo'lganini kuzatuvchi reaktiv StateFlow tizimini simulyatsiya qiling.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

enum class NetworkStatus { AVAILABLE, LOST }

class NetworkMonitor {
    private val _status = MutableStateFlow(NetworkStatus.AVAILABLE)
    val status = _status.asStateFlow()
    
    fun setStatus(newStatus: NetworkStatus) {
        _status.value = newStatus
    }
}

fun main() = runBlocking {
    val monitor = NetworkMonitor()
    
    val job = launch {
        monitor.status.collect { println("Tarmoq holati: $it") }
    }
    
    delay(50L)
    monitor.setStatus(NetworkStatus.LOST)
    delay(50L)
    monitor.setStatus(NetworkStatus.AVAILABLE)
    delay(50L)
    
    job.cancel()
}
""",
    "Ilova bo'ylab tarmoq bor-yo'qligini kuzatib turuvchi reaktiv boshqaruvchi StateFlow orqali barcha qismlarga darhol signal uzatadi.",
    """
Tarmoq holati: AVAILABLE
Tarmoq holati: LOST
Tarmoq holati: AVAILABLE
"""
)

# 846
add_task(
    846,
    "Foydalanuvchi qadamlarini hisoblovchi pedometr oqimi (StateFlow)",
    "Har bir bosilgan qadamni sanab, umumiy masofani hisoblovchi StateFlow modeli tuzing.",
    """
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.update

data class PedometerState(val steps: Int, val distanceMeters: Double)

class PedometerService {
    val state = MutableStateFlow(PedometerState(0, 0.0))
    
    fun stepTaken() {
        state.update { current ->
            val nextSteps = current.steps + 1
            PedometerState(nextSteps, nextSteps * 0.75) // har bir qadam 0.75 metr
        }
    }
}

fun main() {
    val service = PedometerService()
    repeat(3) { service.stepTaken() }
    
    val res = service.state.value
    println("Qadamlar soni: ${res.steps}, Bosib o'tilgan masofa: ${res.distanceMeters} metr")
}
""",
    "update orqali holatni xavfsiz o'zgartirib borish UI qatlamiga yangilangan hisobotlarni yetkazib turadi.",
    """
Qadamlar soni: 3, Bosib o'tilgan masofa: 2.25 metr
"""
)

# 847
add_task(
    847,
    "Bir nechta datchikdan ma'lumotlarni combine orqali yig'ish",
    "Harorat va namlik datchiklarining eng oxirgi qiymatlarini birlashtirib ob-havo indeksi chiqaring.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.combine

fun main() = runBlocking {
    val tempFlow = flowOf(28.0) // Harorat
    val humidityFlow = flowOf(45.0) // Namlik
    
    tempFlow.combine(humidityFlow) { temp, humidity ->
        "Iqlim: Harorat $temp C, Namlik: $humidity%"
    }.collect { println(it) }
}
""",
    "combine operatori bir nechta mustaqil datchiklarning eng yangi qiymatlarini bitta ma'lumotlar modeliga bog'lab beradi.",
    """
Iqlim: Harorat 28.0 C, Namlik: 45.0%
"""
)

# 848
add_task(
    848,
    "Xatoliklarni cheksiz qayta ulovchi xavfsiz oqim (retryWhen)",
    "retryWhen operatoridan foydalanib, har bir xatolikdan so'ng 100ms kutib qayta ulanuvchi chidamli oqim tuzing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.retryWhen
import kotlinx.coroutines.flow.take
import kotlinx.coroutines.delay

var failCount = 0
fun resilientSensor() = flow {
    failCount++
    if (failCount <= 2) {
        throw RuntimeException("Datchik vaqtinchalik javob bermadi")
    }
    emit("Barqaror sensor qiymati: 100")
}

fun main() = runBlocking {
    resilientSensor()
        .retryWhen { cause, attempt ->
            println("Xato (${cause.message}), urinish #$attempt. 100ms kutib qayta ulanamiz...")
            delay(100L)
            attempt < 3
        }
        .take(1)
        .collect { println(it) }
}
""",
    "retryWhen to'xtatuvchi (suspend) tekshiruvlarni qo'llab-quvvatlaydi, bu orqali qayta urinishdan oldin delay qo'yish mumkin.",
    """
Xato (Datchik vaqtinchalik javob bermadi), urinish #0. 100ms kutib qayta ulanamiz...
Xato (Datchik vaqtinchalik javob bermadi), urinish #1. 100ms kutib qayta ulanamiz...
Barqaror sensor qiymati: 100
"""
)

# 849
add_task(
    849,
    "Oqim elementlarini sanash va tekshirish (count, any, all)",
    "Oqimdagi barcha elementlar musbat ekanligini va juft sonlar sonini Flow terminal operatorlari bilan aniqlang.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.asFlow
import kotlinx.coroutines.flow.count

fun main() = runBlocking {
    val numbers = listOf(2, 4, 6, 8, 10).asFlow()
    
    val totalCount = numbers.count()
    println("Jami elementlar soni: $totalCount")
}
""",
    "Flow da count() terminal operatori oqim bo'ylab kelgan barcha elementlarni sanaydi va yakuniy natijani qaytaradi.",
    """
Jami elementlar soni: 5
"""
)

# 850
add_task(
    850,
    "17-qism xulosasi: To'liq MVI / UDF arxitekturasidagi State va Event oqimi",
    "StateFlow orqali UI State va SharedFlow orqali bir martalik hodisalarni (Toast, navigatsiya) boshqaruvchi zamonaviy MVI ViewModel tizimini loyihalang.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

// 1. UI State
data class LoginUiState(val isLoading: Boolean = false, val isSuccess: Boolean = false)

// 2. Bir martalik hodisalar (One-time UI Events)
sealed interface LoginUiEvent {
    data class ShowToast(val message: String) : LoginUiEvent
    object NavigateToHome : LoginUiEvent
}

// 3. ViewModel
class LoginViewModel {
    private val _uiState = MutableStateFlow(LoginUiState())
    val uiState = _uiState.asStateFlow()
    
    private val _eventFlow = MutableSharedFlow<LoginUiEvent>()
    val eventFlow = _eventFlow.asSharedFlow()
    
    suspend fun login(login: String, pass: String) {
        _uiState.value = LoginUiState(isLoading = true)
        delay(100L) // tarmoq so'rovi
        
        if (pass == "12345") {
            _uiState.value = LoginUiState(isSuccess = true)
            _eventFlow.emit(LoginUiEvent.ShowToast("Xush kelibsiz!"))
            _eventFlow.emit(LoginUiEvent.NavigateToHome)
        } else {
            _uiState.value = LoginUiState(isSuccess = false)
            _eventFlow.emit(LoginUiEvent.ShowToast("Parol noto'g'ri!"))
        }
    }
}

fun main() = runBlocking {
    val vm = LoginViewModel()
    
    val stateJob = launch {
        vm.uiState.collect { println("UI Holati: isLoading=${it.isLoading}, isSuccess=${it.isSuccess}") }
    }
    val eventJob = launch {
        vm.eventFlow.collect { event ->
            when (event) {
                is LoginUiEvent.ShowToast -> println("Toast ekranga chiqdi: ${event.message}")
                is LoginUiEvent.NavigateToHome -> println("Ekran almashdi: Asosiy oynaga o'tildi")
            }
        }
    }
    
    delay(50L)
    vm.login("admin", "12345")
    delay(150L)
    
    stateJob.cancel()
    eventJob.cancel()
}
""",
    "Bu yakuniy amaliyot StateFlow va SharedFlow ning zamonaviy Android (Jetpack Compose va MVI) arxitekturasidagi o'rnini to'liq ifodalaydi: barqaror holat StateFlow da, vaqtinchalik effektlar esa SharedFlow da uzatiladi.",
    """
UI Holati: isLoading=false, isSuccess=false
UI Holati: isLoading=true, isSuccess=false
UI Holati: isLoading=false, isSuccess=true
Toast ekranga chiqdi: Xush kelibsiz!
Ekran almashdi: Asosiy oynaga o'tildi
"""
)

save_file("kotlin_17_oqimlar_va_reaktiv_flow.md", tasks)
