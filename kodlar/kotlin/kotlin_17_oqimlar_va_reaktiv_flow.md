# 801-Topshiriq: flow { emit() } yordamida oddiy sovuq oqim (Cold Flow) yaratish
## Topshiriq sharti:
Kotlin Flow yordamida 1 dan 3 gacha bo'lgan sonlarni har 100ms da chiqaruvchi oqim hosil qiling va uni collect() orqali o'qing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
flow { } builderi asinxron qiymatlar ketma-ketligini (Cold Stream) yaratadi. emit() har bir yangi qiymatni oqimga yuboradi, collect() esa ularni qabul qilib oladi.

## Ishlash natijasi:
```text
Oqimga obuna bo'linmoqda...
Qabul qilindi: 1
Qabul qilindi: 2
Qabul qilindi: 3
Oqim yakunlandi.
```


# 802-Topshiriq: flowOf(...) va asFlow() yordamida oqim hosil qilish
## Topshiriq sharti:
Mavjud qiymatlar va ro'yxatni flowOf hamda .asFlow() yordamida Flow ga aylantirishni namoyish eting.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.asFlow

fun main() = runBlocking {
    val fruitFlow = flowOf("Olma", "Anor", "Uzum")
    fruitFlow.collect { println("Meva: $it") }
    
    val listFlow = listOf(10, 20, 30).asFlow()
    listFlow.collect { println("Son: $it") }
}
```

## Tushuntirish va Mantiq:
flowOf berilgan argumentlardan tayyor oqim hosil qiladi, .asFlow() kengaytmasi esa Iterable yoki Sequence kolleksiyalarini to'g'ridan-to'g'ri Flow ga aylantiradi.

## Ishlash natijasi:
```text
Meva: Olma
Meva: Anor
Meva: Uzum
Son: 10
Son: 20
Son: 30
```


# 803-Topshiriq: Cold Stream xususiyati: collect chaqirilmaguncha kod ishlamasligi
## Topshiriq sharti:
Oqim ichidagi loglar faqat collect() chaqirilgandagina ekranga chiqishini, ungacha hech qanday hisoblash bo'lmasligini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Flow - bu sovuq (cold) oqim. U buyurtma asosida ishlaydi: hech kim collect qilmasa, uning ichidagi hech qanday kod ishga tushmaydi va resurs sarflanmaydi.

## Ishlash natijasi:
```text
Oqim yaratildi, lekin hali collect chaqirilmadi.
Endi collect chaqiramiz:
>>> Flow hisoblashni BOSHLADI <<<
Olingan: A
Olingan: B
```


# 804-Topshiriq: Har bir yangi collect() yangi mustaqil oqim boshlashi
## Topshiriq sharti:
Bitta Flow ga ikki marta collect() chaqirilganda har biri o'zining mustaqil hisoblash siklini ishga tushirishini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Har bir collect() chaqiruvi flow { } blokini qaytadan noldan boshlaydi. Shu bois har bir obunachi shaxsiy ma'lumotlar oqimiga ega bo'ladi.

## Ishlash natijasi:
```text
1-kuzatuvchi:
Datchik ishga tushdi
1-qiymat: 25
2-kuzatuvchi:
Datchik ishga tushdi
2-qiymat: 25
```


# 805-Topshiriq: flowOn operatori bilan faqat upstream oqimni IO ga o'tkazish
## Topshiriq sharti:
Ma'lumot chiqarishni (emit) Dispatchers.IO da bajarib, uni asosiy oqimda collect qilishni ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
flowOn faqat o'zidan yuqorida (upstream) turgan operatsiyalar va flow { } blokining oqimini o'zgartiradi. Downstream (collect) esa chaqiruvchining oqimida qoladi.

## Ishlash natijasi:
```text
Collect oqimi: main
Emit oqimi: DefaultDispatcher-worker-1
Qabul qilindi: 100 [main]
```


# 806-Topshiriq: map operatori orqali ma'lumotlarni o'zgartirish
## Topshiriq sharti:
Kelayotgan raqamlarni kvadratiga oshirib yangi formatga o'tkazuvchi oqim yozing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
map operatori oraliq (intermediate) operator bo'lib, har bir elementni berilgan lambda orqali o'zgartirib keyingi bosqichga uzatadi.

## Ishlash natijasi:
```text
Kvadrat natija: 4
Kvadrat natija: 9
Kvadrat natija: 16
```


# 807-Topshiriq: filter operatori orqali saralash
## Topshiriq sharti:
Kelayotgan to'lovlar oqimidan faqat 100 dollardan oshgan muvaffaqiyatli to'lovlarni ajratib oling.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
filter operatori berilgan shartga to'g'ri (true) kelgan elementlarnigina quyi oqimga o'tkazadi, qolganlarini tashlab yuboradi.

## Ishlash natijasi:
```text
Katta to'lov: P2 (250.0 $)
Katta to'lov: P4 (190.0 $)
```


# 808-Topshiriq: transform operatori orqali erkin emit qilish
## Topshiriq sharti:
Har bir kelgan so'rov uchun bir nechta oraliq xabarlar chiqaruvchi transform operatorini qo'llang.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
transform operatori map va filter imkoniyatlarini birlashtiradi: u har bir kiruvchi element uchun 0 ta, 1 ta yoki bir nechta yangi qiymatlarni emit qila oladi.

## Ishlash natijasi:
```text
Yuklash boshlandi: FaylA
Yuklash tugadi: FaylA
Yuklash boshlandi: FaylB
Yuklash tugadi: FaylB
```


# 809-Topshiriq: take operatori orqali dastlabki elementlarni olish va to'xtatish
## Topshiriq sharti:
Cheksiz oqimdan faqat dastlabki 3 ta elementni olib, qolganini avtomatik bekor qiling.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
take(N) operatori N ta element qabul qilingach, oqimga CancellationException yuborib uni xavfsiz to'xtatadi.

## Ishlash natijasi:
```text
Olingan son: 1
Olingan son: 2
Olingan son: 3
Cheksiz oqim xavfsiz to'xtatildi.
```


# 810-Topshiriq: drop operatori orqali dastlabki elementlarni tashlab yuborish
## Topshiriq sharti:
Oqimdagi dastlabki 2 ta boshlang'ich sozlash qiymatini tashlab yuborib, qolganlarini qabul qiling.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.drop

fun main() = runBlocking {
    val configStream = flowOf("Init-1", "Init-2", "HaqiqiyMa'lumot-1", "HaqiqiyMa'lumot-2")
    
    configStream
        .drop(2)
        .collect { println("Amaldagi: $it") }
}
```

## Tushuntirish va Mantiq:
drop(N) operatori boshlang'ich N ta elementni o'tkazib yuboradi va faqat undan keyingi kelgan barcha elementlarni quyi oqimga uzatadi.

## Ishlash natijasi:
```text
Amaldagi: HaqiqiyMa'lumot-1
Amaldagi: HaqiqiyMa'lumot-2
```


# 811-Topshiriq: first() terminal operatori bilan birinchi elementni olish
## Topshiriq sharti:
Shartga mos keluvchi eng birinchi elementni topib, oqimni to'xtatuvchi dastur yozing.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.asFlow
import kotlinx.coroutines.flow.first

fun main() = runBlocking {
    val numbers = listOf(5, 12, 17, 24, 30).asFlow()
    
    val firstEven = numbers.first { it % 2 == 0 }
    println("Birinchi juft son: $firstEven")
}
```

## Tushuntirish va Mantiq:
first() terminal operatori shartni qanoatlantiruvchi eng birinchi qiymatni qaytaradi va oqimni darhol to'xtatadi.

## Ishlash natijasi:
```text
Birinchi juft son: 12
```


# 812-Topshiriq: toList() va toSet() orqali butun oqimni xotiradagi to'plamga yig'ish
## Topshiriq sharti:
Oqim elementlarini to'liq kutib, ularni Kotlin List va Set to'plamlariga o'tkazing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
toList() va toSet() oqim tugaguniga qadar barcha qiymatlarni to'playdi va tayyor kolleksiya sifatida qaytaradi.

## Ishlash natijasi:
```text
List: [A, B, A, C]
Set: [A, B, C]
```


# 813-Topshiriq: reduce va fold orqali oqim elementlarini yagona qiymatga yig'ish
## Topshiriq sharti:
Oqimdan kelgan raqamlarni fold yordamida boshlang'ich qoldiq bilan birgalikda jamlang.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
fold boshlang'ich qiymat qabul qiladi va barcha elementlarni akkumulyatorga jamlaydi. reduce esa birinchi elementni boshlang'ich qiymat sifatida oladi.

## Ishlash natijasi:
```text
Boshlang'ich 100 bilan yig'indi: 160
Ko'paytma: 6000
```


# 814-Topshiriq: onEach operatori bilan oraliq log yozish
## Topshiriq sharti:
Elementlarning oqim bo'ylab harakatlanishini o'zgartirmasdan kuzatish uchun onEach dan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
onEach har bir element o'tganda ko'rsatilgan amalni (odatda log yozish yoki keshga qo'yish) bajaradi, lekin elementning o'zini o'zgartirmasdan quyi bosqichga o'tkazadi.

## Ishlash natijasi:
```text
Xom qiymat: toshkent
Katta harf: TOSHKENT
Ekranga chiqdi: TOSHKENT
Xom qiymat: samarqand
Katta harf: SAMARQAND
Ekranga chiqdi: SAMARQAND
```


# 815-Topshiriq: catch operatori orqali yuqoridagi xatoni ushlash va zaxira emit qilish
## Topshiriq sharti:
Oqim ichida xato sodir bo'lganda dastur qulamasdan zaxira xabarni emit qiluvchi xavfsiz oqim tuzing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
catch operatori faqat o'zidan yuqorida (upstream) yuz bergan istisnolarni ushlaydi va xohlasa oqimga yangi xavfsiz zaxira elementlarni emit qila oladi.

## Ishlash natijasi:
```text
Olingan: Xabar-1
Xatolik ushlandi: Tarmoq kabeli uzildi!
Olingan: Zaxira: Offline rejimdagi xabar
```


# 816-Topshiriq: onStart va onCompletion orqali oqim hayot siklini kuzatish
## Topshiriq sharti:
Yuklanish boshlanganda 'Yuklanmoqda...', tugaganda esa 'Yuklandi' holatlarini beruvchi oqim yarating.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
onStart oqim obunachisi birinchi elementni olishdan avval chaqiriladi, onCompletion esa oqim normal yoki xatolik bilan tugaganda chaqiriladi.

## Ishlash natijasi:
```text
Hayot sikli: Oqim boshlandi
Kontent: Foydalanuvchi ma'lumotlari
Hayot sikli: Oqim tugadi
```


# 817-Topshiriq: onCompletion da xatolik sababini tahlil qilish
## Topshiriq sharti:
onCompletion parametrida keluvchi Throwable orqali oqim qanday sabab bilan tugaganini aniqlang.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
onCompletion blokining `cause` parametri oqim tinch yakunlansa `null`, agar istisno tashlansa o'sha istisno obyektini saqlaydi.

## Ishlash natijasi:
```text
Ma'lumot: Boshlandi
Oqim xatolik bilan yakunlandi: Baza javob bermadi
```


# 818-Topshiriq: buffer() operatori yordamida tezkor ishlab chiqaruvchi va sekin iste'molchini muvozanatlash
## Topshiriq sharti:
Tez element ishlab chiqaruvchi oqim va har bir elementni uzoq qayta ishlovchi collect o'rtasida buffer() qo'yib umumiy vaqtni tejang.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
buffer() operatori emit qilish va collect qilish amallarini alohida koroutinalarga ajratib, o'rtaga bufer qo'yadi. Natijada emitter iste'molchini kutmasdan o'z ishini davom ettiradi.

## Ishlash natijasi:
```text
Iste'mol qilindi: 1
Iste'mol qilindi: 2
Iste'mol qilindi: 3
Umumiy vaqt: ~1000 ms
```


# 819-Topshiriq: conflate() yordamida oraliq eskirgan elementlarni tashlab yuborish
## Topshiriq sharti:
Iste'molchi sekin ishlayotgan paytda oradagi yangi elementlar to'planib qolmasdan, faqat eng so'nggisini uzatishni ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
conflate() operatori iste'molchi band bo'lgan paytda kelgan oraliq qiymatlarni tashlab yuboradi va iste'molchi bo'shashi bilan unga eng so'nggi yangilangan qiymatni beradi.

## Ishlash natijasi:
```text
Qabul qilindi: 1
Qabul qilindi: 3
Qabul qilindi: 5
```


# 820-Topshiriq: collectLatest() yordamida eskirgan hisob-kitobni bekor qilish
## Topshiriq sharti:
Yangi qiymat kelishi bilan hali tugab ulgurmagan avvalgi collect blokini to'xtatuvchi collectLatest ni qo'llang.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
collectLatest yangi qiymat emit qilinganda, avvalgi qiymat ustida ishlayotgan koroutina blokini CancellationException orqali bekor qiladi va yangi qiymatni qayta ishlashga kirishadi.

## Ishlash natijasi:
```text
Boshlandi: 1
Boshlandi: 2
Boshlandi: 3
Yakunlandi: 3
```


# 821-Topshiriq: zip operatori orqali ikkita oqim elementlarini juftlab birlashtirish
## Topshiriq sharti:
Ikkita turli tezlikdagi oqimni zip yordamida 1-ga-1 tartibida birlashtiruvchi kod yozing.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.asFlow
import kotlinx.coroutines.flow.zip

fun main() = runBlocking {
    val english = listOf("One", "Two", "Three").asFlow()
    val uzbek = listOf("Bir", "Ikki", "Uch").asFlow()
    
    english.zip(uzbek) { en, uz -> "$en = $uz" }
        .collect { println(it) }
}
```

## Tushuntirish va Mantiq:
zip operatori ikkala oqimdan kelgan elementlarni juft-juft qilib birlashtiradi. Oqimlarning biri tugasa, umumiy birlashgan oqim ham tugaydi.

## Ishlash natijasi:
```text
One = Bir
Two = Ikki
Three = Uch
```


# 822-Topshiriq: combine operatori orqali ikkita oqimning eng so'nggi qiymatlarini birlashtirish
## Topshiriq sharti:
Foydalanuvchi ismi va uning onlayn holati o'zgarganda eng oxirgi holatni ko'rsatuvchi combine dasturini yozing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
combine operatori oqimlarning birortasida yangi element paydo bo'lishi bilan, boshqa oqimning eng so'nggi (oxirgi) elementi bilan yangi natija hosil qiladi.

## Ishlash natijasi:
```text
Ali hozirda: Offline
Ali hozirda: Online
Vali hozirda: Online
```


# 823-Topshiriq: flatMapConcat orqali ketma-ket ichki Flow larni ochish
## Topshiriq sharti:
Har bir kelgan buyurtma identifikatori uchun uning detallarini chiqaruvchi ichki oqimni ketma-ket ulab oching.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
flatMapConcat bitta oqim elementini yangi ichki oqimga o'giradi va ularni qat'iy ketma-ket (avvalgi ichki oqim to'liq tugagach keyingisi) tartibda birlashtiradi.

## Ishlash natijasi:
```text
ORD-1 detal 1
ORD-1 detal 2
ORD-2 detal 1
ORD-2 detal 2
```


# 824-Topshiriq: flatMapMerge orqali ichki Flow larni parallel birlashtirish
## Topshiriq sharti:
Bir nechta foydalanuvchi ma'lumotlarini parallel so'rovchi ichki Flow larni birlashtiring.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
flatMapMerge ichki oqimlarni bir vaqtda parallel ishga tushiradi va ularning natijalarini qaysi biri tezroq kelsa o'sha tartibda birlashtirib beradi.

## Ishlash natijasi:
```text
User1: Tizimga kirdi
User2: Tizimga kirdi
```


# 825-Topshiriq: flatMapLatest orqali yangi kalit kelganda avvalgisini to'xtatish
## Topshiriq sharti:
Qidiruv maydonida foydalanuvchi yangi harf yozganda avvalgi server so'rovi Flow ini to'xtatib yangisini boshlashni simulyatsiya qiling.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
flatMapLatest yangi so'rov paydo bo'lishi bilan avvalgi ichki oqimni CancellationException orqali to'xtatadi va yangi so'rov oqimini ochadi.

## Ishlash natijasi:
```text
Qidiruv boshlandi: Ko
Qidiruv boshlandi: Kot
Qidiruv boshlandi: Kotlin
Natija: Kotlin uchun javob
```


# 826-Topshiriq: distinctUntilChanged() bilan bir xil ketma-ket qiymatlarni filtrlash
## Topshiriq sharti:
Ketma-ket bir xil takrorlangan qiymatlarni tashlab yuboruvchi filtrni qo'llang.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.distinctUntilChanged

fun main() = runBlocking {
    flowOf(1, 1, 2, 2, 2, 3, 1, 1)
        .distinctUntilChanged()
        .collect { println("Yangi qiymat: $it") }
}
```

## Tushuntirish va Mantiq:
distinctUntilChanged() faqat avvalgi qiymatdan farq qiluvchi yangi elementlarnigina o'tkazadi. Ketma-ket kelgan nusxalar tashlab yuboriladi.

## Ishlash natijasi:
```text
Yangi qiymat: 1
Yangi qiymat: 2
Yangi qiymat: 3
Yangi qiymat: 1
```


# 827-Topshiriq: debounce() operatori orqali qidiruv maydonini sokinlashtirish
## Topshiriq sharti:
Foydalanuvchi klaviaturada to'xtamasdan yozayotgan paytda ortiqcha so'rov yubormasdan, faqat 100ms pauza bo'lganda so'rov jo'nating.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
debounce(vaqt) yangi element kelgandan keyin ko'rsatilgan vaqt ichida boshqa yangi element kelmasa, o'sha elementni uzatadi.

## Ishlash natijasi:
```text
Serverga so'rov yuborildi: Ant
Serverga so'rov yuborildi: Anti
```


# 828-Topshiriq: retry va retryWhen operatorlari orqali xatolikda qayta ulanish
## Topshiriq sharti:
Tarmoq uzilishi sodir bo'lganda 2 martagacha oqimni qayta boshlovchi retry operatorini yozing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
retry operatori upstream da xatolik sodir bo'lganda oqimni boshidan qayta obuna qiladi (qayta ishga tushiradi).

## Ishlash natijasi:
```text
Ulanish urinishi: #1
Qayta urinish uchun sabab: Ulanish rad etildi!
Ulanish urinishi: #2
Qayta urinish uchun sabab: Ulanish rad etildi!
Ulanish urinishi: #3
Natija: Muvaffaqiyatli tarmoq oqimi
```


# 829-Topshiriq: MutableStateFlow yaratish va uning boshlang'ich qiymatini o'qish
## Topshiriq sharti:
Android da UI State saqlashning asosi bo'lgan MutableStateFlow ni boshlang'ich qiymat bilan e'lon qiling va qiymatini o'zgartiring.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.MutableStateFlow

fun main() = runBlocking {
    val counterState = MutableStateFlow(0)
    
    println("Boshlang'ich holat: ${counterState.value}")
    
    counterState.value = 5
    println("Yangilangan holat: ${counterState.value}")
}
```

## Tushuntirish va Mantiq:
StateFlow - bu doimo bitta joriy qiymatni o'zida saqlovchi issiq (hot) oqimdir. Uning joriy holatini .value orqali istalgan paytda sinxron o'qish mumkin.

## Ishlash natijasi:
```text
Boshlang'ich holat: 0
Yangilangan holat: 5
```


# 830-Topshiriq: StateFlow ga faqat o'qiladigan interfeys (asStateFlow) berish
## Topshiriq sharti:
Enkapsulyatsiya qoidasiga binoan, ViewModel ichida MutableStateFlow ni tashqariga faqat o'qiluvchi StateFlow sifatida taqdim eting.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
_userName xususiy (private) bo'lib, tashqaridagi kod faqat o'qiluvchi StateFlow orqali unga ulanadi va qiymatni to'g'ridan-to'g'ri o'zboshimchalik bilan o'zgartira olmaydi.

## Ishlash natijasi:
```text
Dastlabki ism: Mehmon
O'zgargan ism: Jasur
```


# 831-Topshiriq: MutableStateFlow.update { } atomik yangilash amali
## Topshiriq sharti:
Konkurent sharoitda StateFlow qiymatini .update { } orqali poyga holatisiz xavfsiz yangilang.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
.update { } funksiyasi ichki Compare-And-Set (CAS) siklidan foydalanib, hatto bir nechta oqim bir vaqtda chaqirsa ham qiymatning xavfsiz va aniq yangilanishini ta'minlaydi.

## Ishlash natijasi:
```text
Atomik yangilash natijasi: 100
```


# 832-Topshiriq: Bir nechta abonentlarning StateFlow qiymatini collect qilishi
## Topshiriq sharti:
Bitta StateFlow ga 2 ta alohida koroutina obuna bo'lganda, ularning ikkalasi ham yangilanishlarni qabul qilishini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
StateFlow issiq (hot) oqim bo'lgani sababli, uning barcha abonentlari (subscribers) yangilanishlarni parallel va bir xil qabul qiladi.

## Ishlash natijasi:
```text
1-UI Ekran: Yuklanmoqda
2-Log tizimi: Yuklanmoqda
1-UI Ekran: Muvaffaqiyatli yuklandi
2-Log tizimi: Muvaffaqiyatli yuklandi
```


# 833-Topshiriq: MutableSharedFlow yaratish va bir martalik hodisani yuborish
## Topshiriq sharti:
Toast xabarnomasi yoki ekran navigatsiyasi kabi bir martalik hodisalar uchun SharedFlow dan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
SharedFlow o'zida holat (current value) saqlamaydi, balki kelgan xabarlarni barcha faol abonentlarga tarqatadi (broadcast event).

## Ishlash natijasi:
```text
Hodisa qabul qilindi: Xabar: Foydalanuvchi ro'yxatdan o'tdi
```


# 834-Topshiriq: SharedFlow da replay parametri yordamida kesh hosil qilish
## Topshiriq sharti:
Yangi ulangan obunachiga oxirgi 2 ta xabarni qayta uzatuvchi (replay = 2) SharedFlow sozlang.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
replay = 2 parametri SharedFlow ga eng so'nggi 2 ta xabarni xotirada saqlab turishni va yangi obunachilarga darhol yetkazishni buyuradi.

## Ishlash natijasi:
```text
Kechikkan foydalanuvchi ulandi:
O'qildi: Xabar 2
O'qildi: Xabar 3
```


# 835-Topshiriq: StateFlow va SharedFlow o'rtasidagi farqlar
## Topshiriq sharti:
StateFlow va SharedFlow xatti-harakatlarini solishtiruvchi tushuntirish va taqqoslash kodini yozing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
StateFlow holat (State) uchun ishlatiladi: u har doim qiymatga ega, takroriy qiymatni emit qilmaydi. SharedFlow esa hodisalar (Events) uchun: har bir emit abonentlarga yetib boradi.

## Ishlash natijasi:
```text
StateFlow qiymati: Holat A
SharedFlow replayCache hajmi: 0
```


# 836-Topshiriq: stateIn operatori orqali oddiy Flow ni StateFlow ga aylantirish
## Topshiriq sharti:
Muntazam ma'lumot beruvchi sovuq oqimni CoroutineScope ichida issiq StateFlow ga aylantiring.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
stateIn sovuq oqimni berilgan ko'lamda (scope) ishga tushirib, uni UI uchun qulay StateFlow ga aylantiradi.

## Ishlash natijasi:
```text
Boshlang'ich: 0
250ms dan keyin: 2
```


# 837-Topshiriq: SharingStarted.WhileSubscribed(5000L) strategiyasi
## Topshiriq sharti:
Faqat kamida bitta faol UI obunachi bo'lganda oqimni saqlab turuvchi va 5 soniya ekran burilganda kutuvchi strategiyani namoyish eting.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.flow.SharingStarted

fun main() {
    val strategy = SharingStarted.WhileSubscribed(5000L)
    println("Strategiya nomi: ${strategy.javaClass.simpleName}")
    println("Android tavsiyasi: Ekran aylanganda bekor bo'lishining oldini olish uchun 5000ms delay")
}
```

## Tushuntirish va Mantiq:
WhileSubscribed(5000L) Android arxitekturasida standart bo'lib, oxirgi obunachi chiqib ketganidan so'ng 5 soniya kutadi va shundan keyingina resursni to'xtatadi.

## Ishlash natijasi:
```text
Strategiya nomi: StartedWhileSubscribed
Android tavsiyasi: Ekran aylanganda bekor bo'lishining oldini olish uchun 5000ms delay
```


# 838-Topshiriq: shareIn operatori orqali Flow ni SharedFlow ga aylantirish
## Topshiriq sharti:
Tarmoqdan olingan oqimni barcha abonentlarga qayta so'rov yubormasdan tarqatish uchun shareIn dan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
shareIn sovuq oqimni faqat bitta marta bajaradi va uning natijasini bir nechta mustaqil obunachilarga ulashadi (multicast).

## Ishlash natijasi:
```text
>>> Og'ir API so'rovi amalga oshirildi! <<<
1-abonent: JSON ma'lumot
2-abonent: JSON ma'lumot
```


# 839-Topshiriq: callbackFlow orqali hodisalar tinglovchisini Flow ga aylantirish
## Topshiriq sharti:
Tashqi hodisalar manbaini (masalan GPS yoki sensor tinglovchisi) callbackFlow yordamida oqimga aylantiring.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
callbackFlow ichida trySend() bilan hodisalar oqimga uzatiladi, awaitClose esa obunachi oqimni to'xtatganda listenerni tozalashni kafolatlaydi.

## Ishlash natijasi:
```text
GPS tinglovchisi ro'yxatdan o'tdi
Yangi manzil: 41.2995 N, 69.2401 E
GPS tinglovchisi to'xtatildi va xotiradan o'chirildi.
```


# 840-Topshiriq: channelFlow orqali parallel koroutinalardan turli oqimlarda emit qilish
## Topshiriq sharti:
Bir vaqtda bir nechta parallel ishchilardan bitta umumiy oqimga send() orqali ma'lumot jo'natuvchi channelFlow tuzing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Oddiy flow { } ichida boshqa koroutinadan emit() chaqirish qat'iyan taqiqlangan (Flow invariant). channelFlow esa ko'p oqimli parallel muhitda send() orqali element yuborishga ruxsat beradi.

## Ishlash natijasi:
```text
1-ishchi: ma'lumot
2-ishchi: ma'lumot
```


# 841-Topshiriq: Jonli valyuta kurslari generatori (Real-time Currency Ticker)
## Topshiriq sharti:
Har 100ms da tasodifiy o'zgaruvchi valyuta narxini chiqaruvchi va 3 ta qiymatdan so'ng to'xtovchi jonli ticker yarating.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Real-time tizimlarda birja yoki valyuta monitoringi uchun Flow eng qulay va kam xotira sarflaydigan reaktiv vositadir.

## Ishlash natijasi:
```text
Valyuta kursi: USD/UZS -> 12820.0 so'm
Valyuta kursi: USD/UZS -> 12835.5 so'm
Valyuta kursi: USD/UZS -> 12810.0 so'm
```


# 842-Topshiriq: Sensor ma'lumotlarini silliqlash (Moving Average Flow)
## Topshiriq sharti:
Harorat datchigidan kelayotgan ketma-ket har 3 ta qiymatning o'rtacha arifmetik qiymatini hisoblab beruvchi oqim yozing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
transform operatori va oraliq bufer yordamida tebranishlarni silliqlovchi Moving Average filtri oson yaratiladi.

## Ishlash natijasi:
```text
O'rtacha silliqlangan harorat: 22.0 C
O'rtacha silliqlangan harorat: 24.0 C
O'rtacha silliqlangan harorat: 26.0 C
```


# 843-Topshiriq: Avtomatik to'ldirish (Autocomplete) qidiruv xizmati
## Topshiriq sharti:
debounce, distinctUntilChanged va flatMapLatest operatorlarini birlashtirib professional qidiruv oqimini loyihalang.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Bu kombinatsiya mobil va veb ilovalardagi qidiruv maydonchalarining eng yuqori standartidir: ortiqcha harflar uchun so'rov ketmaydi va eski javoblar yangisini bosib ketmaydi.

## Ishlash natijasi:
```text
Serverdan kelgan qidiruv natijalari: [Kot natija 1, Kot natija 2]
```


# 844-Topshiriq: Fayl yuklash jarayonini (Progress Flow) kuzatish
## Topshiriq sharti:
Fayl baytlarini uzatishda har 25% da foizni emit qiluvchi yuklash ko'rsatkichi oqimini yozing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
UI progressBar yoki loading indikatorlarini yangilab turish uchun Flow eng qulay usul hisoblanadi.

## Ishlash natijasi:
```text
Yuklanish ko'rsatkichi: [0%]
Yuklanish ko'rsatkichi: [25%]
Yuklanish ko'rsatkichi: [50%]
Yuklanish ko'rsatkichi: [75%]
Yuklanish ko'rsatkichi: [100%]
Yuklash yakunlandi!
```


# 845-Topshiriq: Tarmoq aloqasi holatini kuzatuvchi Flow (Connectivity Monitor)
## Topshiriq sharti:
Tarmoq online/offline bo'lganini kuzatuvchi reaktiv StateFlow tizimini simulyatsiya qiling.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Ilova bo'ylab tarmoq bor-yo'qligini kuzatib turuvchi reaktiv boshqaruvchi StateFlow orqali barcha qismlarga darhol signal uzatadi.

## Ishlash natijasi:
```text
Tarmoq holati: AVAILABLE
Tarmoq holati: LOST
Tarmoq holati: AVAILABLE
```


# 846-Topshiriq: Foydalanuvchi qadamlarini hisoblovchi pedometr oqimi (StateFlow)
## Topshiriq sharti:
Har bir bosilgan qadamni sanab, umumiy masofani hisoblovchi StateFlow modeli tuzing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
update orqali holatni xavfsiz o'zgartirib borish UI qatlamiga yangilangan hisobotlarni yetkazib turadi.

## Ishlash natijasi:
```text
Qadamlar soni: 3, Bosib o'tilgan masofa: 2.25 metr
```


# 847-Topshiriq: Bir nechta datchikdan ma'lumotlarni combine orqali yig'ish
## Topshiriq sharti:
Harorat va namlik datchiklarining eng oxirgi qiymatlarini birlashtirib ob-havo indeksi chiqaring.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
combine operatori bir nechta mustaqil datchiklarning eng yangi qiymatlarini bitta ma'lumotlar modeliga bog'lab beradi.

## Ishlash natijasi:
```text
Iqlim: Harorat 28.0 C, Namlik: 45.0%
```


# 848-Topshiriq: Xatoliklarni cheksiz qayta ulovchi xavfsiz oqim (retryWhen)
## Topshiriq sharti:
retryWhen operatoridan foydalanib, har bir xatolikdan so'ng 100ms kutib qayta ulanuvchi chidamli oqim tuzing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
retryWhen to'xtatuvchi (suspend) tekshiruvlarni qo'llab-quvvatlaydi, bu orqali qayta urinishdan oldin delay qo'yish mumkin.

## Ishlash natijasi:
```text
Xato (Datchik vaqtinchalik javob bermadi), urinish #0. 100ms kutib qayta ulanamiz...
Xato (Datchik vaqtinchalik javob bermadi), urinish #1. 100ms kutib qayta ulanamiz...
Barqaror sensor qiymati: 100
```


# 849-Topshiriq: Oqim elementlarini sanash va tekshirish (count, any, all)
## Topshiriq sharti:
Oqimdagi barcha elementlar musbat ekanligini va juft sonlar sonini Flow terminal operatorlari bilan aniqlang.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.asFlow
import kotlinx.coroutines.flow.count

fun main() = runBlocking {
    val numbers = listOf(2, 4, 6, 8, 10).asFlow()
    
    val totalCount = numbers.count()
    println("Jami elementlar soni: $totalCount")
}
```

## Tushuntirish va Mantiq:
Flow da count() terminal operatori oqim bo'ylab kelgan barcha elementlarni sanaydi va yakuniy natijani qaytaradi.

## Ishlash natijasi:
```text
Jami elementlar soni: 5
```


# 850-Topshiriq: 17-qism xulosasi: To'liq MVI / UDF arxitekturasidagi State va Event oqimi
## Topshiriq sharti:
StateFlow orqali UI State va SharedFlow orqali bir martalik hodisalarni (Toast, navigatsiya) boshqaruvchi zamonaviy MVI ViewModel tizimini loyihalang.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Bu yakuniy amaliyot StateFlow va SharedFlow ning zamonaviy Android (Jetpack Compose va MVI) arxitekturasidagi o'rnini to'liq ifodalaydi: barqaror holat StateFlow da, vaqtinchalik effektlar esa SharedFlow da uzatiladi.

## Ishlash natijasi:
```text
UI Holati: isLoading=false, isSuccess=false
UI Holati: isLoading=true, isSuccess=false
UI Holati: isLoading=false, isSuccess=true
Toast ekranga chiqdi: Xush kelibsiz!
Ekran almashdi: Asosiy oynaga o'tildi
```

