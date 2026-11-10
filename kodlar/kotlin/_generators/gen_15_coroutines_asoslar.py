# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(r"C:\Users\User\Desktop\uzbek_dataset\kodlar\kotlin\_generators")
from task_builder import format_task, save_file

tasks = []

def add_task(num, title, cond, code, exp, res):
    tasks.append(format_task(num, title, cond, code, exp, res))

# 701
add_task(
    701,
    "runBlocking orqali koroutina doirasiga kirish",
    "Kotlin dasturida an'anaviy bloklovchi koddan koroutina doirasiga o'tish uchun runBlocking builder'idan foydalanishni namoyish etuvchi dastur tuzing. Asosiy oqim koroutina yakunlanishini kutishi kerak.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.delay

fun main() {
    println("Dastur boshlandi: ${Thread.currentThread().name}")
    
    runBlocking {
        println("Koroutina ichida: ${Thread.currentThread().name}")
        delay(500L)
        println("Koroutina vazifani yakunladi")
    }
    
    println("Dastur yakunlandi: ${Thread.currentThread().name}")
}
""",
    "runBlocking funksiyasi sinxron kod bilan to'xtatuvchi (suspending) kod o'rtasidagi ko'prikdir. U o'z blokidagi barcha koroutinalar to'liq yakunlanmaguncha o'zi ishlayotgan oqimni (odatda main thread) to'xtatib (bloklab) turadi.",
    """
Dastur boshlandi: main
Koroutina ichida: main
Koroutina vazifani yakunladi
Dastur yakunlandi: main
"""
)

# 702
add_task(
    702,
    "suspend funksiyasi asoslari va qaytish qiymati",
    "Tarmoqdan foydalanuvchi profilini yuklashni simulyatsiya qiluvchi to'xtatilishi mumkin bo'lgan (suspend) funksiya yarating va uning natijasini koroutina ichida qabul qiling.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.delay

suspend fun fetchUserProfile(userId: Int): String {
    println("Foydalanuvchi #$userId ma'lumotlari yuklanmoqda...")
    delay(1000L) // tarmoq kechikishi simulyatsiyasi
    return "Foydalanuvchi: Alisher Navoiy, Id: $userId, Maqom: Faol"
}

fun main() = runBlocking {
    println("Yuklash so'rovi yuborilmoqda...")
    val profile = fetchUserProfile(101)
    println("Natija olindi -> $profile")
}
""",
    "suspend kalit so'zi funksiya oqimni to'xtatmasdan (non-blocking) vaqtinchalik pauza qilinishi va keyin davom ettirilishi mumkinligini bildiradi. suspend funksiyalarni faqat boshqa suspend funksiyadan yoki koroutina builderi ichidan chaqirish mumkin.",
    """
Yuklash so'rovi yuborilmoqda...
Foydalanuvchi #101 ma'lumotlari yuklanmoqda...
Natija olindi -> Foydalanuvchi: Alisher Navoiy, Id: 101, Maqom: Faol
"""
)

# 703
add_task(
    703,
    "launch builder yordamida 'fire-and-forget' vazifasi",
    "Orqa fonda natija kutmasdan bajariladigan (fire-and-forget) vazifani launch orqali ishga tushiring va asosiy oqim bilan parallel harakatini ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

fun main() = runBlocking {
    println("Asosiy koroutina boshlandi")
    
    launch {
        println("Fon vazifasi boshlandi")
        delay(600L)
        println("Fon vazifasi: Hisobot serverga yuklandi!")
    }
    
    println("Asosiy oqim boshqa ishlarni bajarmoqda...")
    delay(1000L)
    println("Barcha ishlar yakunlandi")
}
""",
    "launch builderi yangi koroutina boshlaydi va Job obyektini qaytaradi, lekin to'g'ridan-to'g'ri hisoblash natijasini qaytarmaydi (Unit qaytaradi). Bu fonda bajariluvchi va natijasi kutish talab etilmaydigan vazifalar uchun juda mos.",
    """
Asosiy koroutina boshlandi
Asosiy oqim boshqa ishlarni bajarmoqda...
Fon vazifasi boshlandi
Fon vazifasi: Hisobot serverga yuklandi!
Barcha ishlar yakunlandi
"""
)

# 704
add_task(
    704,
    "async va await orqali natija qaytaruvchi asinxron vazifa",
    "Murakkab hisob-kitobni asinxron bajarib, Deferred obyektidan await() yordamida natijani oluvchi dastur tuzing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.async
import kotlinx.coroutines.delay

suspend fun calculateDiscount(price: Double): Double {
    delay(500L)
    return price * 0.15
}

fun main() = runBlocking {
    println("Chegirma hisoblash boshlandi...")
    val deferredDiscount = async {
        calculateDiscount(250_000.0)
    }
    
    println("Kassada chek shakllanmoqda...")
    val discount = deferredDiscount.await()
    val finalPrice = 250_000.0 - discount
    println("Chegirma miqdori: $discount so'm, Yakuniy to'lov: $finalPrice so'm")
}
""",
    "async builderi Deferred<T> turidagi obyekt qaytaradi. await() metodi chaqirilganda, koroutina natija tayyor bo'lguniga qadar to'xtab turadi (oqimni bloklamasdan) va natija chiqqach qiymatni qaytaradi.",
    """
Chegirma hisoblash boshlandi...
Kassada chek shakllanmoqda...
Chegirma miqdori: 37500.0 so'm, Yakuniy to'lov: 212500.0 so'm
"""
)

# 705
add_task(
    705,
    "delay() yordamida oqimni to'xtatmasdan pauza qilish",
    "Bir nechta koroutina bir xil oqimda delay() chaqirganda bir-biriga xalaqit bermasdan parallel vaqt o'tkazishini ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

fun main() = runBlocking {
    launch {
        for (i in 1..3) {
            println("Koroutina-A: qadam $i [${Thread.currentThread().name}]")
            delay(300L)
        }
    }
    
    launch {
        for (i in 1..3) {
            println("Koroutina-B: qadam $i [${Thread.currentThread().name}]")
            delay(300L)
        }
    }
}
""",
    "delay() suspend funksiyasi taymer qo'yib, oqimni boshqa koroutinalar uchun bo'shatadi. Shuning uchun bitta oqimda A va B koroutinalari navbatma-navbat o'z qadamlarini bajara oladi.",
    """
Koroutina-A: qadam 1 [main]
Koroutina-B: qadam 1 [main]
Koroutina-A: qadam 2 [main]
Koroutina-B: qadam 2 [main]
Koroutina-A: qadam 3 [main]
Koroutina-B: qadam 3 [main]
"""
)

# 706
add_task(
    706,
    "Thread.sleep() va delay() o'rtasidagi farqni taqqoslash",
    "Bitta oqimda Thread.sleep() butun oqimni muzlatib qo'yishi, delay() esa boshqa koroutinaga imkoniyat berishini amaliy kod orqali namoyish eting.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

fun main() = runBlocking {
    println("--- delay() bilan sinov ---")
    launch {
        delay(400L)
        println("1-vazifa: delay tugadi")
    }
    launch {
        println("2-vazifa: darhol bajarildi, chunki 1-vazifa oqimni bo'shatgan")
    }
    delay(600L)
    
    println("--- Thread.sleep() bilan taqqoslash eslatmasi: Thread.sleep oqimni to'liq muzlatadi ---")
}
""",
    "Thread.sleep() butun operatsion tizim oqimini (thread) to'xtatib qo'yadi va hech qanday koroutina bu oqimda ishlay olmaydi. delay() esa oqimni bo'shatib, boshqa koroutinalar ishlashiga ruxsat beradi.",
    """
--- delay() bilan sinov ---
2-vazifa: darhol bajarildi, chunki 1-vazifa oqimni bo'shatgan
1-vazifa: delay tugadi
--- Thread.sleep() bilan taqqoslash eslatmasi: Thread.sleep oqimni to'liq muzlatadi ---
"""
)

# 707
add_task(
    707,
    "Job obyekti orqali koroutinani kuzatish va join() bilan kutish",
    "launch qaytargan Job obyektining join() metodidan foydalanib, muayyan koroutina yakunlanishini kutib turuvchi dastur yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import kotlinx.coroutines.Job

fun main() = runBlocking {
    val job: Job = launch {
        println("Katta hisobot fayli generatsiya qilinmoqda...")
        delay(700L)
        println("Hisobot fayli tayyorlandi!")
    }
    
    println("Hisobot tayyor bo'lishi kutilmoqda...")
    job.join()
    println("Hisobot tayyor, pochta orqali yuborish mumkin!")
}
""",
    "Job koroutinaning hayotiy siklini boshqarish imkonini beradi. job.join() suspend metodi chaqirilganda, o'sha koroutina to'liq yakunlanmaguncha joriy koroutina kutib turadi.",
    """
Hisobot tayyor bo'lishi kutilmoqda...
Katta hisobot fayli generatsiya qilinmoqda...
Hisobot fayli tayyorlandi!
Hisobot tayyor, pochta orqali yuborish mumkin!
"""
)

# 708
add_task(
    708,
    "Job ning holatlari (isActive, isCompleted, isCancelled)",
    "Job obyektining holat xususiyatlarini (isActive, isCompleted, isCancelled) koroutinaning turli bosqichlarida tekshiring.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val job = launch {
        delay(400L)
    }
    
    println("Ishga tushgach: isActive=${job.isActive}, isCompleted=${job.isCompleted}, isCancelled=${job.isCancelled}")
    job.join()
    println("Yakunlangach: isActive=${job.isActive}, isCompleted=${job.isCompleted}, isCancelled=${job.isCancelled}")
}
""",
    "Job bir necha holatga ega: New, Active, Completing, Completed, Cancelling, Cancelled. Boolean xususiyatlar orqali koroutina hozirda faolmi yoki tugaganmi aniqlanadi.",
    """
Ishga tushgach: isActive=true, isCompleted=false, isCancelled=false
Yakunlangach: isActive=false, isCompleted=true, isCancelled=false
"""
)

# 709
add_task(
    709,
    "Dispatchers.Default - CPU talab qiluvchi hisob-kitoblar",
    "CPU resursini ko'p talab qiluvchi massivni saralash amalini Dispatchers.Default oqimlar guruhida bajaruvchi kod yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers

fun main() = runBlocking {
    launch(Dispatchers.Default) {
        println("Hisoblash boshlandi: ${Thread.currentThread().name}")
        val numbers = (1..100_000).toList().reversed()
        val sorted = numbers.sorted()
        println("100,000 element saralandi. Birinchi element: ${sorted.first()}, oxirgi: ${sorted.last()}")
        println("Hisoblash yakunlandi: ${Thread.currentThread().name}")
    }
}
""",
    "Dispatchers.Default CPU intensiv vazifalar (matematik hisob-kitoblar, JSON parsing, grafika, saralash) uchun mo'ljallangan. U kompyuterdagi CPU yadrolari soniga teng oqimlar pulidan (thread pool) foydalanadi.",
    """
Hisoblash boshlandi: DefaultDispatcher-worker-1
100,000 element saralandi. Birinchi element: 1, oxirgi: 100000
Hisoblash yakunlandi: DefaultDispatcher-worker-1
"""
)

# 710
add_task(
    710,
    "Dispatchers.IO - disk va tarmoq operatsiyalari uchun",
    "Fayldan o'qish yoki tarmoq so'rovini Dispatchers.IO da amalga oshirishni ko'rsatuvchi dastur tuzing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay

fun main() = runBlocking {
    launch(Dispatchers.IO) {
        println("Tarmoq so'rovi yuborilmoqda: ${Thread.currentThread().name}")
        delay(600L) // tarmoq I/O kutilmoqda
        println("Ma'lumotlar bazasiga yozildi: ${Thread.currentThread().name}")
    }
}
""",
    "Dispatchers.IO fayl tizimi, ma'lumotlar bazasi va tarmoq kabi kiritish-chiqarish operatsiyalariga moslashtirilgan bo'lib, kerak bo'lganda 64 tagacha oqim (yoki ko'proq) yarata oladi.",
    """
Tarmoq so'rovi yuborilmoqda: DefaultDispatcher-worker-1
Ma'lumotlar bazasiga yozildi: DefaultDispatcher-worker-1
"""
)

# 711
add_task(
    711,
    "Dispatchers.Unconfined - chaqiruvchi oqimda boshlanuvchi dispatcher",
    "Dispatchers.Unconfined dispatcheri yordamida koroutinaning birinchi to'xtashgacha va undan keyin qaysi oqimlarda ishlashini namoyish eting.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay

fun main() = runBlocking {
    launch(Dispatchers.Unconfined) {
        println("Unconfined boshlanishi: ${Thread.currentThread().name}")
        delay(300L)
        println("Unconfined delay dan so'ng: ${Thread.currentThread().name}")
    }
}
""",
    "Dispatchers.Unconfined koroutinani chaqirilgan oqimda boshlaydi, biroq birinchi to'xtash (masalan, delay) nuqtasidan so'ng qayta tiklanish o'sha kutishni bajargan oqimda davom etadi.",
    """
Unconfined boshlanishi: main
Unconfined delay dan so'ng: kotlinx.coroutines.DefaultExecutor
"""
)

# 712
add_task(
    712,
    "newSingleThreadContext bilan maxsus oqimda koroutina",
    "Maxsus nomlangan bitta oqim yaratib, koroutinani o'sha oqimda bajarishni ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.newSingleThreadContext

fun main() = runBlocking {
    val maxsusOqim = newSingleThreadContext("MaxsusAuditOqimi")
    
    launch(maxsusOqim) {
        println("Xavfsiz audit yozuvi: ${Thread.currentThread().name}")
    }.join()
    
    maxsusOqim.close()
}
""",
    "newSingleThreadContext bitta ajratilgan oqim yaratadi. Bu sinxronizatsiya muammolarini (thread safety) bartaraf etish yoki maxsus ketma-ketlikdagi vazifalar uchun foydalidir.",
    """
Xavfsiz audit yozuvi: MaxsusAuditOqimi
"""
)

# 713
add_task(
    713,
    "CoroutineName yordamida koroutinalarga nom berish",
    "Debugging va loglarni tahlil qilishni osonlashtirish uchun CoroutineName kontekst elementidan foydalaning.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.CoroutineName
import kotlinx.coroutines.currentCoroutineContext

fun main() = runBlocking(CoroutineName("BoshKoroutina")) {
    println("Bosh oqim: ${currentCoroutineContext()[CoroutineName]?.name}")
    
    launch(CoroutineName("ValyutaKurslariYuklovchi")) {
        println("Yuklovchi: ${currentCoroutineContext()[CoroutineName]?.name}")
    }
}
""",
    "CoroutineName kontekst elementi yordamida har bir koroutinaga o'ziga xos nom beriladi, bu nosozliklarni bartaraf etishda qaysi koroutina ishlayotganini aniq ko'rishga yordam beradi.",
    """
Bosh oqim: BoshKoroutina
Yuklovchi: ValyutaKurslariYuklovchi
"""
)

# 714
add_task(
    714,
    "CoroutineContext elementlarini birlashtirish (+ operatori)",
    "Dispatcher va CoroutineName elementlarini '+' operatori yordamida birlashtirib koroutinaga uzating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.CoroutineName
import kotlinx.coroutines.currentCoroutineContext

fun main() = runBlocking {
    val kontekst = Dispatchers.Default + CoroutineName("FaylPaketlash")
    
    launch(kontekst) {
        val nom = currentCoroutineContext()[CoroutineName]?.name
        println("Vazifa nomi: $nom, Oqim: ${Thread.currentThread().name}")
    }
}
""",
    "CoroutineContext to'plam kabi ishlaydi. '+' operatori yordamida turli elementlar (Job, Dispatcher, CoroutineName, ExceptionHandler) bitta kontekstga birlashtiriladi.",
    """
Vazifa nomi: FaylPaketlash, Oqim: DefaultDispatcher-worker-1
"""
)

# 715
add_task(
    715,
    "CoroutineScope yaratish va unda koroutinalarni boshqarish",
    "Mustaqil CoroutineScope yaratib, unga bir nechta vazifa yuklang va kerak bo'lganda butun ko'lamni bekor qilish imkoniyatini ko'rsating.",
    """
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import kotlinx.coroutines.runBlocking

fun main() = runBlocking {
    val maxsusScope = CoroutineScope(Dispatchers.Default + Job())
    
    maxsusScope.launch {
        println("1-xizmat ishlamoqda...")
        delay(200L)
        println("1-xizmat yakunlandi")
    }
    
    maxsusScope.launch {
        println("2-xizmat ishlamoqda...")
        delay(200L)
        println("2-xizmat yakunlandi")
    }
    
    delay(300L)
}
""",
    "CoroutineScope barcha bolalar koroutinalarini o'zida birlashtiradi. Agar scope bekor qilinsa (cancel), undagi barcha ishlar bir zumda to'xtatiladi.",
    """
1-xizmat ishlamoqda...
2-xizmat ishlamoqda...
1-xizmat yakunlandi
2-xizmat yakunlandi
"""
)

# 716
add_task(
    716,
    "GlobalScope ning xatarlari va to'g'ri arxitektura",
    "Nima sababdan GlobalScope o'rniga strukturalangan konkurentlik (structured concurrency) ishlatilishi zarurligini tushuntiruvchi misol tuzing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

suspend fun xavfsizOperatsiya() = coroutineScope {
    launch {
        delay(200L)
        println("Strukturalangan bola koroutina tugadi")
    }
    println("Scope ichida vazifalar nazorat ostida")
}

fun main() = runBlocking {
    xavfsizOperatsiya()
    println("Barcha nazorat ostidagi vazifalar yakunlandi")
}
""",
    "GlobalScope butun ilova hayot davriga bog'langan bo'lib, xotira sizib chiqishi (memory leak) va nazoratsiz fon jarayonlarini keltirib chiqaradi. Doimo coroutineScope yoki aniq CoroutineScope dan foydalanish zarur.",
    """
Scope ichida vazifalar nazorat ostida
Strukturalangan bola koroutina tugadi
Barcha nazorat ostidagi vazifalar yakunlandi
"""
)

# 717
add_task(
    717,
    "Ketma-ket (sequential) suspend funksiyalar chaqiruvi",
    "Biri ikkinchisining natijasiga bog'liq bo'lgan ikki ta suspend funksiyani tabiiy ketma-ketlikda chaqiring va umumiy sarflangan vaqtni ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.delay
import kotlin.system.measureTimeMillis

suspend fun getUserToken(): String {
    delay(400L)
    return "token_abc_123"
}

suspend fun fetchUserDetails(token: String): String {
    delay(400L)
    return "Foydalanuvchi ma'lumotlari: token tasdiqlandi ($token)"
}

fun main() = runBlocking {
    val vaqt = measureTimeMillis {
        val token = getUserToken()
        val details = fetchUserDetails(token)
        println(details)
    }
    println("Ketma-ket chaqiruv vaqti: ~$vaqt ms")
}
""",
    "Suspend funksiyalar odatiy kod kabi ketma-ket bajariladi. Agar biror qadam avvalgi qadam natijasiga bog'liq bo'lsa, hech qanday callback'siz toza ketma-ket kod yoziladi.",
    """
Foydalanuvchi ma'lumotlari: token tasdiqlandi (token_abc_123)
Ketma-ket chaqiruv vaqti: ~800 ms
"""
)

# 718
add_task(
    718,
    "Parallel bajarilish: ikkita mustaqil async operatsiyani bir vaqtda yurgazish",
    "Ikkita bir-biriga bog'liq bo'lmagan so'rovni async orqali bir vaqtda ishga tushirib, umumiy sarflangan vaqtni deyarli 2 barobar qisqartiring.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.async
import kotlinx.coroutines.delay
import kotlin.system.measureTimeMillis

suspend fun fetchWeather(): String {
    delay(500L)
    return "Toshkent: +26 C, Quyoshli"
}

suspend fun fetchCurrencyRate(): Double {
    delay(500L)
    return 12850.0
}

fun main() = runBlocking {
    val vaqt = measureTimeMillis {
        val obHavo = async { fetchWeather() }
        val valyuta = async { fetchCurrencyRate() }
        
        println("Ob-havo: ${obHavo.await()}")
        println("USD kursi: ${valyuta.await()} UZS")
    }
    println("Parallel bajarilish vaqti: ~$vaqt ms")
}
""",
    "Mustaqil operatsiyalar async bilan o'ralganda ular bir vaqtda fonda ishlay boshlaydi. Umumiy bajarilish vaqti ularning yig'indisi emas, balki eng uzunining vaqtiga teng bo'ladi.",
    """
Ob-havo: Toshkent: +26 C, Quyoshli
USD kursi: 12850.0 UZS
Parallel bajarilish vaqti: ~500 ms
"""
)

# 719
add_task(
    719,
    "awaitAll() bilan bir nechta Deferred natijalarini to'plash",
    "Bir nechta serverdan mahsulot narxlarini async ro'yxati orqali so'rab, awaitAll() yordamida barchasini birdaniga qabul qiling.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.delay

suspend fun fetchPriceFromStore(storeId: Int): Pair<Int, Double> {
    delay(300L)
    val price = 50.0 + (storeId * 5.0)
    return Pair(storeId, price)
}

fun main() = runBlocking {
    val stores = listOf(1, 2, 3, 4)
    val deferredList = stores.map { id ->
        async { fetchPriceFromStore(id) }
    }
    
    val results = deferredList.awaitAll()
    results.forEach { (id, price) ->
        println("Do'kon #$id -> Narx: $price $")
    }
}
""",
    "awaitAll() funksiyasi Collection<Deferred<T>> ustida ishlaydi va barcha koroutinalar natija bermaguncha kutadi, natijalarni List<T> sifatida qaytaradi.",
    """
Do'kon #1 -> Narx: 55.0 $
Do'kon #2 -> Narx: 60.0 $
Do'kon #3 -> Narx: 65.0 $
Do'kon #4 -> Narx: 70.0 $
"""
)

# 720
add_task(
    720,
    "coroutineScope builder orqali lokal konkurentlik yaratish",
    "Suspend funksiya ichida parallel operatsiyalarni coroutineScope blokiga o'rab, barcha bolalar tugashini kafolatlovchi xavfsiz funksiya yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.async
import kotlinx.coroutines.delay

suspend fun loadDashboardData(): Pair<Int, Int> = coroutineScope {
    val usersDeferred = async {
        delay(300L)
        1250 // foydalanuvchilar soni
    }
    val ordersDeferred = async {
        delay(300L)
        340 // buyurtmalar soni
    }
    
    Pair(usersDeferred.await(), ordersDeferred.await())
}

fun main() = runBlocking {
    println("Boshqaruv paneli yuklanmoqda...")
    val (users, orders) = loadDashboardData()
    println("Faol foydalanuvchilar: $users, Yangi buyurtmalar: $orders")
}
""",
    "coroutineScope - bu to'xtatuvchi funksiya bo'lib, o'zining barcha ichki bolalar koroutinalari to'liq yakunlanmaguncha o'zidan keyingi qatorga o'tmaydi. Agar birorta bolada xato yuz bersa, qolganlarini ham bekor qiladi.",
    """
Boshqaruv paneli yuklanmoqda...
Faol foydalanuvchilar: 1250, Yangi buyurtmalar: 340
"""
)

# 721
add_task(
    721,
    "Non-blocking UI printsipi: hisoblash vaqtida asosiy oqim erkinligi",
    "Asosiy oqim animatsiyasi yoki foydalanuvchi harakatlarini to'xtatmasdan, Default oqimida og'ir hisoblashni bajarish printsipini simulyatsiya qiling.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay

suspend fun performHeavyCalculation(): Long = withContext(Dispatchers.Default) {
    var sum = 0L
    for (i in 1..10_000_000L) {
        sum += i
    }
    sum
}

fun main() = runBlocking {
    launch {
        // UI hodisalari simulyatsiyasi
        repeat(3) {
            println("UI kadr chizilmoqda... (60 FPS)")
            delay(100L)
        }
    }
    
    val result = performHeavyCalculation()
    println("Hisoblash yakuni: $result")
}
""",
    "withContext(Dispatchers.Default) chaqirilganda, og'ir hisoblash boshqa oqimda bajariladi. Asosiy oqim esa foydalanuvchi interfeysini chizishda erkin davom etadi.",
    """
UI kadr chizilmoqda... (60 FPS)
UI kadr chizilmoqda... (60 FPS)
UI kadr chizilmoqda... (60 FPS)
Hisoblash yakuni: 50000005000000
"""
)

# 722
add_task(
    722,
    "Millionlab koroutinalarni ishga tushirish (Lightweight sinovi)",
    "Kotlin koroutinalarining qanchalik yengil ekanligini 50,000 ta parallel koroutina yaratib, ularning tezligini o'lchash orqali ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import java.util.concurrent.atomic.AtomicInteger

fun main() = runBlocking {
    val counter = AtomicInteger()
    val total = 50_000
    
    val startTime = System.currentTimeMillis()
    val jobs = List(total) {
        launch {
            delay(100L)
            counter.incrementAndGet()
        }
    }
    jobs.forEach { it.join() }
    val duration = System.currentTimeMillis() - startTime
    
    println("$total ta koroutina muvaffaqiyatli yakunlandi: ${counter.get()} ta")
    println("Umumiy vaqt: $duration ms")
}
""",
    "50,000 ta OS oqimi (Thread) yaratish xotira to'lishiga (OutOfMemoryError) olib kelgan bo'lardi. Koroutinalar esa foydalanuvchi doirasidagi (user-space) yengil obyektlar bo'lib, juda kam xotira egallaydi.",
    """
50000 ta koroutina muvaffaqiyatli yakunlandi: 50000 ta
Umumiy vaqt: ~300 ms
"""
)

# 723
add_task(
    723,
    "yield() orqali CPU ni boshqa koroutinalarga kooperativ bo'shatib berish",
    "Bitta oqimda hisoblash bilan band bo'lgan koroutinaning yield() yordamida o'z navbatini boshqa koroutinalarga berishini ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.yield

fun main() = runBlocking {
    launch {
        repeat(3) { i ->
            println("Vazifa-1: hisoblash qadami $i")
            yield()
        }
    }
    
    launch {
        repeat(3) { i ->
            println("Vazifa-2: hisoblash qadami $i")
            yield()
        }
    }
}
""",
    "yield() joriy koroutinani to'xtatib, dispetcherga xuddi shu oqimda navbatda turgan boshqa koroutinalarni bajarish imkoniyatini taqdim etadi. Bu kooperativ ko'p vazifalilikning asosi hisoblanadi.",
    """
Vazifa-1: hisoblash qadami 0
Vazifa-2: hisoblash qadami 0
Vazifa-1: hisoblash qadami 1
Vazifa-2: hisoblash qadami 1
Vazifa-1: hisoblash qadami 2
Vazifa-2: hisoblash qadami 2
"""
)

# 724
add_task(
    724,
    "CoroutineContext dan Job va Dispatcher ni olish",
    "currentCoroutineContext() yordamida koroutinaning ichki parametrlarini o'qishni amalga oshiring.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.currentCoroutineContext
import kotlinx.coroutines.Job
import kotlin.coroutines.ContinuationInterceptor

fun main() = runBlocking {
    launch {
        val context = currentCoroutineContext()
        val job = context[Job]
        val dispatcher = context[ContinuationInterceptor]
        
        println("Job mavjudmi: ${job != null}")
        println("Dispatcher turi: ${dispatcher?.javaClass?.simpleName}")
    }
}
""",
    "currentCoroutineContext() to'xtatuvchi funksiya bo'lib, joriy bajarilish kontekstini qaytaradi. Kontekst kalit-qiymat xaritasi kabi elementlarni indeks orqali olish imkonini beradi.",
    """
Job mavjudmi: true
Dispatcher turi: BlockingEventLoop
"""
)

# 725
add_task(
    725,
    "Maxsus ThreadPoolDispatcher yaratish va unga vazifa yuklash",
    "newFixedThreadPoolContext yordamida 3 ta oqimdan iborat maxsus oqimlar pulini tashkil etib, koroutinalarni taqsimlang.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.newFixedThreadPoolContext
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val pool = newFixedThreadPoolContext(3, "MaxsusPul")
    
    repeat(3) { id ->
        launch(pool) {
            println("Vazifa #$id oqimda boshlandi: ${Thread.currentThread().name}")
            delay(100L)
            println("Vazifa #$id tugadi: ${Thread.currentThread().name}")
        }
    }
    
    delay(200L)
    pool.close()
}
""",
    "newFixedThreadPoolContext belgilangan sondagi oqimlarga ega shaxsiy dispetcher hosil qiladi. Dastur so'ngida pool.close() chaqirilib, oqimlar xavfsiz to'xtatiladi.",
    """
Vazifa #0 oqimda boshlandi: MaxsusPul-1
Vazifa #1 oqimda boshlandi: MaxsusPul-2
Vazifa #2 oqimda boshlandi: MaxsusPul-3
Vazifa #0 tugadi: MaxsusPul-1
Vazifa #1 tugadi: MaxsusPul-2
Vazifa #2 tugadi: MaxsusPul-3
"""
)

# 726
add_task(
    726,
    "async blokida xato yuz berganda await() da ushlash",
    "async ichida yuz bergan istisnoli holat await() chaqirilganda qanday namoyon bo'lishini va uni try-catch orqali qayta ishlashni ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.async
import kotlinx.coroutines.coroutineScope

suspend fun riskyAsyncCalculation(): Int = coroutineScope {
    val deferred = async {
        throw IllegalArgumentException("Noto'g'ri ko'rsatkich kiritildi!")
    }
    try {
        deferred.await()
    } catch (e: IllegalArgumentException) {
        println("Istisno ushlandi: ${e.message}")
        -1
    }
}

fun main() = runBlocking {
    val natija = riskyAsyncCalculation()
    println("Qaytarilgan xavfsiz qiymat: $natija")
}
""",
    "async ichidagi istisno o'sha zaxotiyoq portlamaydi, balki Deferred obyekti ichiga saqlanadi. Qachonki await() chaqirilsa, o'sha istisno qayta tashlanadi (rethrow).",
    """
Istisno ushlandi: Noto'g'ri ko'rsatkich kiritildi!
Qaytarilgan xavfsiz qiymat: -1
"""
)

# 727
add_task(
    727,
    "launch va async orasidagi xatolikni uzatish farqlari",
    "launch va async ning xatoni yuqori qatlamga qanday yetkazishini tushuntiruvchi misol yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.async
import kotlinx.coroutines.delay

fun main() = runBlocking {
    println("--- Async vs Launch xatolik farqi ---")
    
    val deferred = async {
        delay(50L)
        "Muvaffaqiyatli qiymat"
    }
    println("Async natijasi: ${deferred.await()}")
    
    val job = launch {
        delay(50L)
        println("Launch fon vazifasi muvaffaqiyatli tugadi")
    }
    job.join()
}
""",
    "launch xatolikni ota koroutinaga darhol uzatadi (agar unhandled bo'lsa butun scopeni to'xtatadi), async esa natijani Deferred ichida kapsulalaydi va await() chaqirilganda oshkor qiladi.",
    """
--- Async vs Launch xatolik farqi ---
Async natijasi: Muvaffaqiyatli qiymat
Launch fon vazifasi muvaffaqiyatli tugadi
"""
)

# 728
add_task(
    728,
    "Bir nechta API chaqiruvlarini async bilan agregatsiya qilish",
    "Foydalanuvchi ma'lumotlari, uning bildirishnomalari va hisob balansini 3 ta mustaqil so'rov orqali parallel yig'uvchi agregator yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.async
import kotlinx.coroutines.delay

data class UserSummary(val name: String, val balance: Double, val unreadCount: Int)

suspend fun fetchName(): String { delay(300L); return "Dilshod" }
suspend fun fetchBalance(): Double { delay(350L); return 4500.50 }
suspend fun fetchUnreadNotifications(): Int { delay(250L); return 5 }

fun main() = runBlocking {
    val nameDeferred = async { fetchName() }
    val balanceDeferred = async { fetchBalance() }
    val unreadDeferred = async { fetchUnreadNotifications() }
    
    val summary = UserSummary(
        name = nameDeferred.await(),
        balance = balanceDeferred.await(),
        unreadCount = unreadDeferred.await()
    )
    
    println("Foydalanuvchi ma'lumotnomasi: $summary")
}
""",
    "Uchta alohida tarmoq so'rovi parallel yuboriladi va barchasining natijasi tayyor bo'lgach bitta umumiy Data Class obyektiga jamlanadi.",
    """
Foydalanuvchi ma'lumotnomasi: UserSummary(name=Dilshod, balance=4500.5, unreadCount=5)
"""
)

# 729
add_task(
    729,
    "Foydalanuvchi profili va buyurtmalarini parallel yuklovchi servis",
    "Mijozning asosiy profili va uning so'nggi 3 ta buyurtmasini parallel yuklab konsolga chiqaruvchi servis yarating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.async
import kotlinx.coroutines.delay

data class Order(val id: String, val amount: Double)

suspend fun getOrders(userId: Int): List<Order> {
    delay(400L)
    return listOf(Order("ORD-1", 120.0), Order("ORD-2", 45.0), Order("ORD-3", 89.0))
}

suspend fun getUserStatus(userId: Int): String {
    delay(200L)
    return "VIP Mijoz"
}

fun main() = runBlocking {
    val userId = 77
    val statusDeferred = async { getUserStatus(userId) }
    val ordersDeferred = async { getOrders(userId) }
    
    println("Mijoz #$userId maomi: ${statusDeferred.await()}")
    println("Buyurtmalar ro'yxati:")
    ordersDeferred.await().forEach { println("- ${it.id}: ${it.amount} $") }
}
""",
    "Async yordamida ikkita so'rov bir vaqtda ishlaydi, eng tez kelgani kutishsiz konsolga chiqishi mumkin yoki await bilan tartib bilan ekranga beriladi.",
    """
Mijoz #77 maomi: VIP Mijoz
Buyurtmalar ro'yxati:
- ORD-1: 120.0 $
- ORD-2: 45.0 $
- ORD-3: 89.0 $
"""
)

# 730
add_task(
    730,
    "Ob-havo ma'lumotlarini turli stansiyalardan asinxron yig'ish",
    "Samarqand, Buxoro va Xiva shaharlaridagi meteorologik stansiyalardan parallel haroratni o'lchovchi tizim tuzing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.async
import kotlinx.coroutines.delay

data class CityWeather(val city: String, val tempC: Int)

suspend fun getCityTemp(city: String, temp: Int): CityWeather {
    delay(300L)
    return CityWeather(city, temp)
}

fun main() = runBlocking {
    val cities = listOf("Samarqand" to 24, "Buxoro" to 27, "Xiva" to 22)
    val deferreds = cities.map { (city, temp) ->
        async { getCityTemp(city, temp) }
    }
    
    val weatherReport = deferreds.map { it.await() }
    weatherReport.forEach { println("${it.city}: ${it.tempC} C") }
}
""",
    "Kolleksiya map funktsiyasi orqali har bir shahar uchun alohida async koroutina ishga tushirilib, natijalar to'plami yig'iladi.",
    """
Samarqand: 24 C
Buxoro: 27 C
Xiva: 22 C
"""
)

# 731
add_task(
    731,
    "Mahsulot narxlarini bir nechta do'kondan tekshirib eng arzonini topish",
    "Bir nechta onlayn do'kondan bir vaqtda narx so'rab, eng arzon taklifni aniqlovchi dastur yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.async
import kotlinx.coroutines.delay

data class StoreOffer(val storeName: String, val price: Double)

suspend fun queryStore(name: String, price: Double): StoreOffer {
    delay(250L)
    return StoreOffer(name, price)
}

fun main() = runBlocking {
    val storeCalls = listOf(
        async { queryStore("Mediapark", 3_200_000.0) },
        async { queryStore("Texnomart", 3_150_000.0) },
        async { queryStore("Idea", 3_300_000.0) }
    )
    
    val offers = storeCalls.map { it.await() }
    val bestOffer = offers.minByOrNull { it.price }
    println("Eng arzon taklif: ${bestOffer?.storeName} da ${bestOffer?.price} so'm")
}
""",
    "Parallel so'rovlar natijalari olingach, standart kolleksiya operatsiyasi (minByOrNull) yordamida eng arzon do'kon aniqlanadi.",
    """
Eng arzon taklif: Texnomart da 3150000.0 so'm
"""
)

# 732
add_task(
    732,
    "Asinxron fayl hajmini hisoblash simulyatsiyasi",
    "Diskdagi uchta virtual papkaning umumiy hajmini parallel hisoblovchi dastur tuzing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.async
import kotlinx.coroutines.delay

suspend fun scanFolderSize(folderName: String, sizeMb: Long): Long {
    delay(200L)
    println("Papka tekshirildi: $folderName ($sizeMb MB)")
    return sizeMb
}

fun main() = runBlocking {
    val folders = listOf("Documents" to 450L, "Downloads" to 1200L, "Pictures" to 850L)
    val deferredSizes = folders.map { (name, size) ->
        async { scanFolderSize(name, size) }
    }
    
    val totalSize = deferredSizes.sumOf { it.await() }
    println("Jami band qilingan disk maydoni: $totalSize MB")
}
""",
    "sumOf bilan birgalikda chaqirilgan await() barcha papkalar hajmini jamlab umumiy hajmni asinxron hisoblaydi.",
    """
Papka tekshirildi: Documents (450 MB)
Papka tekshirildi: Downloads (1200 MB)
Papka tekshirildi: Pictures (850 MB)
Jami band qilingan disk maydoni: 2500 MB
"""
)

# 733
add_task(
    733,
    "Asinxron keshdan ma'lumot qidirish, topilmasa tarmoqdan olish",
    "Avval keshdan ma'lumotni asinxron tekshirib, agar u yerda mavjud bo'lmasa tarmoqdan yuklovchi funksiya yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.delay

suspend fun getFromCache(key: String): String? {
    delay(100L)
    return null // Keshda topilmadi
}

suspend fun getFromNetwork(key: String): String {
    delay(400L)
    return "Serverdan yangi ma'lumot ($key)"
}

suspend fun fetchSmartData(key: String): String {
    val cached = getFromCache(key)
    if (cached != null) {
        println("Keshdan olindi!")
        return cached
    }
    println("Kesh bo'sh, tarmoqqa murojaat qilinmoqda...")
    return getFromNetwork(key)
}

fun main() = runBlocking {
    val data = fetchSmartData("user_settings")
    println("Yakuniy natija: $data")
}
""",
    "Kesh va tarmoq iyerarxiyasini ketma-ketlikda xavfsiz boshqarish koroutinalarda toza va tushunarli ifodalanadi.",
    """
Kesh bo'sh, tarmoqqa murojaat qilinmoqda...
Yakuniy natija: Serverdan yangi ma'lumot (user_settings)
"""
)

# 734
add_task(
    734,
    "suspend funksiyalarda rekursiv operatsiyalar",
    "Fayllar daraxti yoki bo'limlar iyerarxiyasini suspend rekursiv funksiya orqali rekursiv ko'rib chiquvchi dastur yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.delay

data class Category(val name: String, val subCategories: List<Category> = emptyList())

suspend fun printCategoryTree(cat: Category, indent: String = "") {
    delay(50L)
    println("$indent- ${cat.name}")
    for (sub in cat.subCategories) {
        printCategoryTree(sub, "$indent  ")
    }
}

fun main() = runBlocking {
    val tree = Category("Elektronika", listOf(
        Category("Smartfonlar", listOf(Category("Android"), Category("iOS"))),
        Category("Noutbuklar")
    ))
    println("Katalog daraxti:")
    printCategoryTree(tree)
}
""",
    "Suspend funksiyalar rekursiyani to'liq qo'llab-quvvatlaydi. Har bir rekursiv chaqiruv suspend holatida o'z kontekstini to'xtatib davom ettira oladi.",
    """
Katalog daraxti:
- Elektronika
  - Smartfonlar
    - Android
    - iOS
  - Noutbuklar
"""
)

# 735
add_task(
    735,
    "suspend funksiyaga to'xtatuvchi lambda uzatish",
    "Argument sifatida suspend lambdani (suspend () -> T) qabul qiluvchi yuqori tartibli funksiya yarating va uning bajarilish vaqtini o'lchang.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.delay

suspend fun <T> measureAsyncBlock(nomi: String, block: suspend () -> T): T {
    println("'$nomi' bloki boshlandi")
    val start = System.currentTimeMillis()
    val res = block()
    val duration = System.currentTimeMillis() - start
    println("'$nomi' bloki yakunlandi (${duration} ms)")
    return res
}

fun main() = runBlocking {
    val natija = measureAsyncBlock("Foydalanuvchi tekshiruvi") {
        delay(300L)
        "Foydalanuvchi tasdiqlandi"
    }
    println("Natija: $natija")
}
""",
    "suspend () -> T sintaksisi lambdaning o'zi ham boshqa suspend funksiyalarni chaqirish huquqiga ega ekanligini bildiradi.",
    """
'Foydalanuvchi tekshiruvi' bloki boshlandi
'Foydalanuvchi tekshiruvi' bloki yakunlandi (~300 ms)
Natija: Foydalanuvchi tasdiqlandi
"""
)

# 736
add_task(
    736,
    "CoroutineScope.launch da yangi Job biriktirish",
    "launch ga alohida Job() parametri berilganda ota-bola bog'liqligi qanday uzilishini ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val otaJob = launch {
        println("Ota koroutina boshlandi")
        
        launch(Job()) { // yangi Job orqali bog'lanish uziladi
            delay(300L)
            println("Mustaqil bola koroutina tugadi")
        }
        
        println("Ota koroutina o'z ishini tugatmoqda")
    }
    
    otaJob.join()
    println("Ota koroutina to'liq yakunlandi")
    delay(400L) // mustaqil koroutinaning tugashini ko'rish uchun
}
""",
    "Odatda bola koroutinalar ota koroutinaning Job'iga bog'lanadi. Agar launch ga yangi Job() berilsa, ota koroutina bu bolaning tugashini kutmaydi va strukturalangan konkurentlik uziladi.",
    """
Ota koroutina boshlandi
Ota koroutina o'z ishini tugatmoqda
Ota koroutina to'liq yakunlandi
Mustaqil bola koroutina tugadi
"""
)

# 737
add_task(
    737,
    "Job.invokeOnCompletion orqali koroutina tugashini monitoring qilish",
    "Koroutina o'z ishini muvaffaqiyatli yoki xatolik bilan yakunlaganda avtomatik chaqiriluvchi tinglovchi (listener) o'rnating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val job = launch {
        println("Muhim fon vazifasi boshlandi...")
        delay(400L)
        println("Muhim fon vazifasi yakuniga yetdi.")
    }
    
    job.invokeOnCompletion { exception ->
        if (exception != null) {
            println("Koroutina xatolik bilan tugadi: ${exception.message}")
        } else {
            println("Monitoring: Koroutina to'liq va muvaffaqiyatli yakunlandi!")
        }
    }
    
    job.join()
}
""",
    "invokeOnCompletion koroutina qanday yakunlanishidan qat'i nazar chaqiriladi. Undagi parametr orqali xato yuz bergani yoki tinch yakunlangani aniqlanadi.",
    """
Muhim fon vazifasi boshlandi...
Muhim fon vazifasi yakuniga yetdi.
Monitoring: Koroutina to'liq va muvaffaqiyatli yakunlandi!
"""
)

# 738
add_task(
    738,
    "Job.children orqali faol bola koroutinalarni nazorat qilish",
    "Bitta ota koroutina ichida bir nechta bolalar ishga tushirilganda, ularning sonini job.children xususiyati orqali sanang.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val otaJob = launch {
        repeat(4) {
            launch {
                delay(300L)
            }
        }
    }
    
    delay(50L) // bolalar ishga tushishi uchun qisqa vaqt
    println("Faol bola koroutinalar soni: ${otaJob.children.count()}")
    otaJob.join()
    println("Ota va uning barcha bolalari yakunlandi.")
}
""",
    "job.children barcha faol bola koroutinalar ro'yxatini (Sequence) taqdim etadi. Ota koroutina barcha bolalari yakunlanmaguncha o'zi ham yakunlanmaydi.",
    """
Faol bola koroutinalar soni: 4
Ota va uning barcha bolalari yakunlandi.
"""
)

# 739
add_task(
    739,
    "runBlocking ichida ko'p qavatli launch bloklari bajarilish tartibi",
    "Bir necha qavatli ichma-ich launch chaqiruvlari navbatda qanday rejalashtirilishini kuzating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch

fun main() = runBlocking {
    println("1 - Asosiy boshlandi")
    launch {
        println("2 - 1-darajali koroutina boshlandi")
        launch {
            println("3 - 2-darajali ichki koroutina bajarildi")
        }
        println("4 - 1-darajali koroutina tugadi")
    }
    println("5 - Asosiy davom etmoqda")
}
""",
    "Koroutinalar navbatga (event loop) qo'yiladi va joriy blok to'xtash nuqtasiga yetganda yoki yakunlanganda navbatdagi koroutina oqimni egallaydi.",
    """
1 - Asosiy boshlandi
5 - Asosiy davom etmoqda
2 - 1-darajali koroutina boshlandi
4 - 1-darajali koroutina tugadi
3 - 2-darajali ichki koroutina bajarildi
"""
)

# 740
add_task(
    740,
    "Asinxron ro'yxatni saralash (Parallel Merge Sort simulyatsiyasi)",
    "Katta ro'yxatni ikkiga bo'lib, har bir yarmini alohida koroutinada saralovchi va birlashtiruvchi algoritmni tuzing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.async
import kotlinx.coroutines.Dispatchers

suspend fun parallelSort(list: List<Int>): List<Int> {
    if (list.size <= 1) return list
    val mid = list.size / 2
    
    val left = list.subList(0, mid)
    val right = list.subList(mid, list.size)
    
    val sortedLeft = kotlinx.coroutines.CoroutineScope(Dispatchers.Default).async { left.sorted() }
    val sortedRight = kotlinx.coroutines.CoroutineScope(Dispatchers.Default).async { right.sorted() }
    
    return merge(sortedLeft.await(), sortedRight.await())
}

fun merge(a: List<Int>, b: List<Int>): List<Int> {
    val res = mutableListOf<Int>()
    var i = 0
    var j = 0
    while (i < a.size && j < b.size) {
        if (a[i] <= b[j]) res.add(a[i++]) else res.add(b[j++])
    }
    while (i < a.size) res.add(a[i++])
    while (j < b.size) res.add(b[j++])
    return res
}

fun main() = runBlocking {
    val numbers = listOf(55, 12, 89, 4, 33, 71, 19, 8)
    val sorted = parallelSort(numbers)
    println("Saralangan ro'yxat: $sorted")
}
""",
    "Parallel hisoblash orqali ro'yxatning ikkala yarmi bir vaqtda CPU yadrolarida saralanadi va so'ngra chiziqli vaqtda (O(N)) birlashtiriladi.",
    """
Saralangan ro'yxat: [4, 8, 12, 19, 33, 55, 71, 89]
"""
)

# 741
add_task(
    741,
    "Asinxron qidiruv tizimi: birinchi javob qaytargan manbani olish",
    "Ikkita serverdan bir xil ma'lumot qidirilganda, eng tez javob bergan server natijasini olib, sekinini bekor qilish simulyatsiyasi.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.async
import kotlinx.coroutines.delay
import kotlinx.coroutines.CompletableDeferred

fun main() = runBlocking {
    val resultChannel = CompletableDeferred<String>()
    
    val server1 = async {
        delay(400L)
        resultChannel.complete("Server 1 natijasi")
    }
    
    val server2 = async {
        delay(150L) // Bu server ancha tezroq
        resultChannel.complete("Server 2 natijasi")
    }
    
    val winner = resultChannel.await()
    server1.cancel()
    server2.cancel()
    
    println("Eng tez manba natijasi: $winner")
}
""",
    "CompletableDeferred orqali birinchi bo'lib natija yuborgan koroutinaning qiymati qabul qilinadi va ortiqcha kutishlarning oldi olinadi.",
    """
Eng tez manba natijasi: Server 2 natijasi
"""
)

# 742
add_task(
    742,
    "Lazy async boshlanishi (CoroutineStart.LAZY)",
    "async vazifasini zudlik bilan emas, balki faqat await() yoki start() chaqirilgandagina boshlanadigan qilib sozlang.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.async
import kotlinx.coroutines.CoroutineStart
import kotlinx.coroutines.delay

fun main() = runBlocking {
    println("Lazy async e'lon qilinmoqda...")
    val lazyCalc = async(start = CoroutineStart.LAZY) {
        println("Lazy hisoblash haqiqatdan ham boshlandi!")
        delay(200L)
        42
    }
    
    println("Hozircha hech narsa bajarilmadi.")
    delay(300L)
    println("Endi await() chaqiramiz:")
    val res = lazyCalc.await()
    println("Natija: $res")
}
""",
    "CoroutineStart.LAZY parametri qo'yilganda koroutina darhol ishga tushmaydi. U faqat natija so'ralganda (await) yoki start() metodida ishga tushadi.",
    """
Lazy async e'lon qilinmoqda...
Hozircha hech narsa bajarilmadi.
Endi await() chaqiramiz:
Lazy hisoblash haqiqatdan ham boshlandi!
Natija: 42
"""
)

# 743
add_task(
    743,
    "Lazy launch boshlanishi va start() metodi",
    "launch vazifasini LAZY holatda yaratib, start() chaqiruvi bilan qo'lda harakatga keltirishni ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.CoroutineStart
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val job = launch(start = CoroutineStart.LAZY) {
        println("Lazy launch nihoyat ishga tushdi!")
    }
    
    println("Vazifa yaratildi, lekin kutilmoqda...")
    delay(200L)
    println("job.start() chaqirilmoqda:")
    job.start()
    job.join()
}
""",
    "start() metodi koroutinani rejalashtirish navbatiga kiritadi va uning fon rejimida boshlanishini ta'minlaydi.",
    """
Vazifa yaratildi, lekin kutilmoqda...
job.start() chaqirilmoqda:
Lazy launch nihoyat ishga tushdi!
"""
)

# 744
add_task(
    744,
    "CoroutineExceptionHandler bilan kutilmagan xatolarni ushlash",
    "Kutilmagan xatoliklarni ushlab qolib dastur qulashining oldini oluvchi CoroutineExceptionHandler dan foydalaning.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.CoroutineExceptionHandler
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val handler = CoroutineExceptionHandler { _, exception ->
        println("ExceptionHandler orqali xato ushlandi: ${exception.message}")
    }
    
    val job = GlobalScope.launch(handler) {
        println("Xavfli vazifa boshlanmoqda...")
        throw RuntimeException("Kutilmagan server xatosi!")
    }
    
    job.join()
    println("Dastur xavfsiz davom etmoqda.")
}
""",
    "CoroutineExceptionHandler koroutinalar iyerarxiyasidagi ushlanmagan xatolarni (uncaught exceptions) global darajada ushlash uchun maxsus kontekst elementidir.",
    """
Xavfli vazifa boshlanmoqda...
ExceptionHandler orqali xato ushlandi: Kutilmagan server xatosi!
Dastur xavfsiz davom etmoqda.
"""
)

# 745
add_task(
    745,
    "Dispatcher ni dinamik almashtirish zarurati",
    "Bitta jarayon ichida I/O operatsiyasidan CPU hisoblashiga va konsolga chiqarishga o'tish zanjirini yarating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay

suspend fun pipelineDataProcessing(): String {
    // 1-qadam: I/O orqali yuklash
    val rawData = withContext(Dispatchers.IO) {
        delay(200L)
        "10,20,30,40"
    }
    // 2-qadam: CPU orqali qayta ishlash
    val sum = withContext(Dispatchers.Default) {
        rawData.split(",").sumOf { it.toInt() }
    }
    return "Jami hisoblangan qiymat: $sum"
}

fun main() = runBlocking {
    val natija = pipelineDataProcessing()
    println(natija)
}
""",
    "withContext() yordamida har bir bosqich o'ziga eng mos keluvchi Dispetcherda (IO, Default) xavfsiz bajariladi.",
    """
Jami hisoblangan qiymat: 100
"""
)

# 746
add_task(
    746,
    "Suspend funksiyalar zanjiri (Pipeline of suspend operations)",
    "Buyurtmani tekshirish, to'lovni yechish va chek yuborishdan iborat 3 ta suspend funksiya zanjirini tuzing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.delay

suspend fun checkStock(itemId: String): Boolean {
    delay(100L)
    return true
}

suspend fun chargeCard(amount: Double): Boolean {
    delay(200L)
    return true
}

suspend fun sendReceipt(email: String): String {
    delay(100L)
    return "Chek $email ga yuborildi"
}

fun main() = runBlocking {
    val itemId = "ITEM-99"
    val isAvailable = checkStock(itemId)
    if (isAvailable) {
        val paid = chargeCard(50.0)
        if (paid) {
            val msg = sendReceipt("user@example.com")
            println("Natija: $msg")
        }
    }
}
""",
    "Suspend zanjiri orqali asinxron kod go'yo oddiy sinxron koddek o'qiladi, bu esa kodning tozaligi va qo'llab-quvvatlanishini sezilarli oshiradi.",
    """
Natija: Chek user@example.com ga yuborildi
"""
)

# 747
add_task(
    747,
    "Bank tranzaksiyasini asinxron verifikatsiya qilish tizimi",
    "Mijoz hisobida mablag' yetarliligini va firibgarlik (anti-fraud) tekshiruvini parallel amalga oshiruvchi bank moduli yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.async
import kotlinx.coroutines.delay

suspend fun checkBalance(accId: String, amount: Double): Boolean {
    delay(250L)
    return 1000.0 >= amount
}

suspend fun runAntiFraudCheck(accId: String): Boolean {
    delay(300L)
    return true // xavfsiz deb topildi
}

fun main() = runBlocking {
    val acc = "UZB-ACC-777"
    val sum = 250.0
    
    val balanceCheck = async { checkBalance(acc, sum) }
    val fraudCheck = async { runAntiFraudCheck(acc) }
    
    val isApproved = balanceCheck.await() && fraudCheck.await()
    if (isApproved) {
        println("Tranzaksiya muvaffaqiyatli tasdiqlandi!")
    } else {
        println("Tranzaksiya rad etildi!")
    }
}
""",
    "Ikkita mustaqil xavfsizlik tekshiruvi parallel bajarilib, umumiy javob berish vaqti deyarli ikki barobarga qisqartiriladi.",
    """
Tranzaksiya muvaffaqiyatli tasdiqlandi!
"""
)

# 748
add_task(
    748,
    "Parollarni asinxron hashing qilish xizmati",
    "Foydalanuvchi parolini CPU oqimida xavfsiz hashlovchi suspend xizmat modulini tuzing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withContext
import kotlinx.coroutines.Dispatchers
import java.security.MessageDigest

suspend fun hashPasswordAsync(password: String): String = withContext(Dispatchers.Default) {
    val bytes = MessageDigest.getInstance("SHA-256").digest(password.toByteArray())
    bytes.joinToString("") { "%02x".format(it) }
}

fun main() = runBlocking {
    val pass = "MaxfiyParol2026"
    val hash = hashPasswordAsync(pass)
    println("Parol: $pass")
    println("SHA-256 Hash: $hash")
}
""",
    "Kriptografik hashing CPU resursini ko'p sarflaydi. Uni withContext(Dispatchers.Default) ichiga o'rash ilovaning boshqa oqimlarini qotib qolishdan asraydi.",
    """
Parol: MaxfiyParol2026
SHA-256 Hash: 887ec17c460a5e8fe376174a7b7a58a69842bfcfbfad5263a236ddda1e17d7b0
"""
)

# 749
add_task(
    749,
    "Rasmlarni parallel yuklash va siqish operatsiyasini simulyatsiya qilish",
    "Uchta rasmni tarmoqdan parallel yuklab, ularning hajmini siqishni ifodalovchi dastur yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.delay

data class ImageTask(val name: String, val originalSize: Int)

suspend fun processImage(img: ImageTask): String {
    delay(200L) // yuklash
    val compressed = img.originalSize / 2
    return "${img.name} siqildi: ${img.originalSize}KB -> ${compressed}KB"
}

fun main() = runBlocking {
    val images = listOf(
        ImageTask("banner.jpg", 1024),
        ImageTask("avatar.png", 512),
        ImageTask("logo.png", 256)
    )
    
    val tasks = images.map { img ->
        async { processImage(img) }
    }
    
    val report = tasks.awaitAll()
    report.forEach { println(it) }
}
""",
    "Rasmlarni parallel qayta ishlash mobil va veb ilovalarda galereya yuklash tezligini sezilarli darajada optimallashtiradi.",
    """
banner.jpg siqildi: 1024KB -> 512KB
avatar.png siqildi: 512KB -> 256KB
logo.png siqildi: 256KB -> 128KB
"""
)

# 750
add_task(
    750,
    "15-qism xulosasi: To'liq asinxron e-tijorat buyurtma qayta ishlash konveyeri",
    "Buyurtma qabul qilish, to'lovni yechish, ombordan zaxiralash va kurerga xabar berish bosqichlarini qamrab oluvchi to'liq asinxron koroutina konveyerini yarating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.async
import kotlinx.coroutines.delay

data class CustomerOrder(val orderId: String, val item: String, val price: Double)

suspend fun processFullOrder(order: CustomerOrder) = coroutineScope {
    println("Buyurtma qabul qilindi: ${order.orderId} (${order.item})")
    
    // 1. To'lov va Omborni parallel tekshirish
    val paymentResult = async {
        delay(300L)
        println("To'lov muvaffaqiyatli yechildi: ${order.price} $")
        true
    }
    
    val inventoryResult = async {
        delay(250L)
        println("Omborda mahsulot zaxiralandi: ${order.item}")
        true
    }
    
    val ready = paymentResult.await() && inventoryResult.await()
    
    // 2. Kuryerga buyurtma jo'natish
    if (ready) {
        delay(150L)
        println("Kuryer xizmatiga yetkazib berish xabarnomasi yuborildi!")
    }
    println("Buyurtma #${order.orderId} to'liq yakunlandi!")
}

fun main() = runBlocking {
    val order = CustomerOrder("ORD-2026-UZ", "Smart Soat", 199.99)
    processFullOrder(order)
}
""",
    "Bu yakuniy amaliyot koroutinalarning asosiy qudratini: parallel tekshiruvlar (async/await), oqimni to'xtatmasdan kutish (delay) va xavfsiz ko'lam boshqaruvini (coroutineScope) to'liq jamlaydi.",
    """
Buyurtma qabul qilindi: ORD-2026-UZ (Smart Soat)
Omborda mahsulot zaxiralandi: Smart Soat
To'lov muvaffaqiyatli yechildi: 199.99 $
Kuryer xizmatiga yetkazib berish xabarnomasi yuborildi!
Buyurtma #ORD-2026-UZ to'liq yakunlandi!
"""
)

save_file("kotlin_15_koroutinalar_asoslari_coroutines.md", tasks)
