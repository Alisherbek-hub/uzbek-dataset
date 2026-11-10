# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(r"C:\Users\User\Desktop\uzbek_dataset\kodlar\kotlin\_generators")
from task_builder import format_task, save_file

tasks = []

def add_task(num, title, cond, code, exp, res):
    tasks.append(format_task(num, title, cond, code, exp, res))

# 751
add_task(
    751,
    "job.cancel() orqali koroutinani bekor qilish",
    "Fonda ishlayotgan koroutinaning Job obyektida cancel() chaqirib, uning ishini to'xtatishni namoyish eting.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val job = launch {
        repeat(100) { i ->
            println("Vazifa bajarilmoqda: qadam $i")
            delay(100L)
        }
    }
    
    delay(250L)
    println("Foydalanuvchi bekor qilish tugmasini bosdi!")
    job.cancel()
    println("Koroutina bekor qilindi.")
}
""",
    "job.cancel() chaqirilganda, koroutinaga CancellationException signali uzatiladi. Koroutina keyingi to'xtatish (suspension) nuqtasida o'z ishini yakunlaydi.",
    """
Vazifa bajarilmoqda: qadam 0
Vazifa bajarilmoqda: qadam 1
Vazifa bajarilmoqda: qadam 2
Foydalanuvchi bekor qilish tugmasini bosdi!
Koroutina bekor qilindi.
"""
)

# 752
add_task(
    752,
    "cancelAndJoin() bilan bekor qilish va to'liq to'xtashini kutish",
    "Koroutinani bekor qilib, uning tozalash ishlari to'liq yakunlanishini kutib turuvchi cancelAndJoin() funksiyasidan foydalaning.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import kotlinx.coroutines.cancelAndJoin

fun main() = runBlocking {
    val job = launch {
        try {
            repeat(10) { i ->
                println("Sensor o'lchovlari: #$i")
                delay(100L)
            }
        } finally {
            println("Sensor to'liq o'chirildi va port yopildi.")
        }
    }
    
    delay(250L)
    println("Tizimni o'chirish boshlandi...")
    job.cancelAndJoin()
    println("Tizim to'liq to'xtadi.")
}
""",
    "cancelAndJoin() bekor qilish so'rovini yuboradi va o'sha koroutina o'zining finally bloklarini to'liq bajarib bo'lguniga qadar kutiladi.",
    """
Sensor o'lchovlari: #0
Sensor o'lchovlari: #1
Sensor o'lchovlari: #2
Tizimni o'chirish boshlandi...
Sensor to'liq o'chirildi va port yopildi.
Tizim to'liq to'xtadi.
"""
)

# 753
add_task(
    753,
    "CancellationException tabiati va catch blokida ushlanishi",
    "CancellationException istisnosi qanday ishlashini va nega uni yutib yubormaslik (rethrow qilish) zarurligini ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import kotlinx.coroutines.cancelAndJoin
import kotlinx.coroutines.CancellationException

fun main() = runBlocking {
    val job = launch {
        try {
            delay(500L)
        } catch (e: CancellationException) {
            println("Bekor qilish signali ushlandi: ${e.message}")
            throw e // bekor qilish to'g'ri ishlashi uchun qayta tashlash shart!
        }
    }
    
    delay(100L)
    job.cancelAndJoin()
    println("Dastur xavfsiz yakunlandi")
}
""",
    "CancellationException Kotlin koroutinalarida normal bekor qilish vositasidir. Agar u try-catch orqali yutib yuborilsa va qayta tashlanmasa, koroutina o'zini to'xtatmasligi mumkin.",
    """
Bekor qilish signali ushlandi: Standart bekor qilish
Dastur xavfsiz yakunlandi
"""
)

# 754
add_task(
    754,
    "Kooperativ bekor qilish: isActive tekshiruvi",
    "Ichida suspend funksiyasi bo'lmagan qattiq CPU hisoblash siklini isActive xususiyati yordamida bekor qilishga sezgir qiling.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.cancelAndJoin
import kotlinx.coroutines.isActive
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val job = launch(Dispatchers.Default) {
        var count = 0
        while (isActive) { // Kooperativ tekshiruv
            count++
        }
        println("Sikl to'xtatildi, hisoblangan qadamlar: $count")
    }
    
    delay(100L)
    job.cancelAndJoin()
    println("Hisoblash koroutinasi muvaffaqiyatli to'xtatildi.")
}
""",
    "Koroutinani bekor qilish kooperativdir. Agar sikl ichida hech qanday suspend chaqiruv bo'lmasa, u bekor qilish signalini sezmaydi. isActive tekshiruvi siklni zudlik bilan to'xtatishga imkon beradi.",
    """
Sikl to'xtatildi, hisoblangan qadamlar: ~
Hisoblash koroutinasi muvaffaqiyatli to'xtatildi.
"""
)

# 755
add_task(
    755,
    "ensureActive() yordamida tezkor bekor qilish tekshiruvi",
    "Katta hajmdagi ma'lumotlarni aylanayotganda ensureActive() chaqiruvi orqali bekor qilinganlikni aniqlashni ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.cancelAndJoin
import kotlinx.coroutines.ensureActive
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val job = launch(Dispatchers.Default) {
        for (i in 1..1_000_000) {
            ensureActive() // Agar bekor qilingan bo'lsa CancellationException tashlaydi
            if (i % 200_000 == 0) println("Qayta ishlangan: $i")
        }
    }
    
    delay(10L)
    job.cancelAndJoin()
    println("Jarayon ensureActive orqali to'xtatildi.")
}
""",
    "ensureActive() metodi agar joriy koroutina Job'i faol bo'lmasa darhol CancellationException tashlaydi. Bu if (!isActive) throw CancellationException() yozishning qisqa va qulay shaklidir.",
    """
Jarayon ensureActive orqali to'xtatildi.
"""
)

# 756
add_task(
    756,
    "finally blokida resurslarni tozalash (cleanup)",
    "Koroutina bekor qilinganda ochilgan tarmoq ulanishi yoki fayl deskriptorini finally blokida yopishni amalga oshiring.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import kotlinx.coroutines.cancelAndJoin

fun main() = runBlocking {
    val job = launch {
        try {
            println("Tarmoq soketi ochildi...")
            delay(1000L)
            println("Ma'lumotlar to'liq o'qildi.")
        } finally {
            println("Resurslarni tozalash: Soket yopildi.")
        }
    }
    
    delay(200L)
    println("Vaqt tugadi, ulanish bekor qilinmoqda...")
    job.cancelAndJoin()
}
""",
    "finally bloki koroutina qanday yakunlanishidan qat'i nazar (muvaffaqiyatli, xato yoki bekor qilish bilan) doimo ishga tushadi va resurslarni yopish uchun eng xavfsiz joydir.",
    """
Tarmoq soketi ochildi...
Vaqt tugadi, ulanish bekor qilinmoqda...
Resurslarni tozalash: Soket yopildi.
"""
)

# 757
add_task(
    757,
    "NonCancellable konteksti bilan finally ichida suspend operatsiyalari",
    "Bekor qilingan koroutinaning finally blokida suspend funksiyani (masalan, serverga log yuborish) withContext(NonCancellable) orqali chaqiring.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import kotlinx.coroutines.cancelAndJoin
import kotlinx.coroutines.withContext
import kotlinx.coroutines.NonCancellable

fun main() = runBlocking {
    val job = launch {
        try {
            delay(1000L)
        } finally {
            withContext(NonCancellable) {
                println("Audit: bekor qilinganlik haqida serverga xabar yuborilmoqda...")
                delay(200L) // Suspend chaqiruv
                println("Audit: xabar muvaffaqiyatli yuborildi.")
            }
        }
    }
    
    delay(100L)
    job.cancelAndJoin()
    println("Barcha jarayon yakunlandi.")
}
""",
    "Bekor qilingan koroutina odatda boshqa suspend funksiyalarni bajara olmaydi, chunki ular darhol bekor bo'ladi. withContext(NonCancellable) esa bu cheklovni chetlab o'tib, tozalash operatsiyalarini oxiriga yetkazishga imkon beradi.",
    """
Audit: bekor qilinganlik haqida serverga xabar yuborilmoqda...
Audit: xabar muvaffaqiyatli yuborildi.
Barcha jarayon yakunlandi.
"""
)

# 758
add_task(
    758,
    "withTimeout yordamida operatsiyaga vaqt chegarasi qo'yish",
    "Serverdan javob kutish vaqtini withTimeout bilan cheklab, belgilangan vaqt oshib ketganda vazifani to'xtating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withTimeout
import kotlinx.coroutines.delay
import kotlinx.coroutines.TimeoutCancellationException

fun main() = runBlocking {
    try {
        withTimeout(300L) {
            println("Serverga so'rov yuborildi...")
            delay(500L) // 300ms dan ko'proq kutadi
            println("Bu satr bajarilmaydi!")
        }
    } catch (e: TimeoutCancellationException) {
        println("Vaqt tugadi: Server o'z vaqtida javob bermadi!")
    }
}
""",
    "withTimeout belgilangan vaqt ichida blok yakunlanmasa TimeoutCancellationException tashlaydi va ichki koroutinani bekor qiladi.",
    """
Serverga so'rov yuborildi...
Vaqt tugadi: Server o'z vaqtida javob bermadi!
"""
)

# 759
add_task(
    759,
    "withTimeoutOrNull bilan xavfsiz null qaytarish",
    "withTimeoutOrNull yordamida istisnosiz (try-catch talab qilmaydigan) xavfsiz timeout tekshiruvini yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withTimeoutOrNull
import kotlinx.coroutines.delay

suspend fun fetchQuickQuote(): String {
    delay(200L)
    return "Bilim - eng katta boylik"
}

suspend fun fetchSlowQuote(): String {
    delay(600L)
    return "Kechikkan hikmat"
}

fun main() = runBlocking {
    val result1 = withTimeoutOrNull(400L) { fetchQuickQuote() }
    println("1-natija: $result1")
    
    val result2 = withTimeoutOrNull(400L) { fetchSlowQuote() }
    println("2-natija: $result2 (vaqt o'tib ketgani sababli null)")
}
""",
    "withTimeoutOrNull belgilangan muddat ichida natija qaytmasa, istisno tashlash o'rniga shunchaki `null` qaytaradi. Bu kodni ixcham va xavfsiz qiladi.",
    """
1-natija: Bilim - eng katta boylik
2-natija: null (vaqt o'tib ketgani sababli null)
"""
)

# 760
add_task(
    760,
    "Standart Job iyerarxiyasida bitta bolaning qulashi ta'siri",
    "Oddiy Job ko'lamida bitta bola koroutina xatolik berganda boshqa qardosh koroutinalar qanday to'xtashini kuzating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

fun main() = runBlocking {
    try {
        launch {
            launch {
                delay(100L)
                println("1-bola: Kutilmagan qulash!")
                throw IllegalStateException("Bazada xatolik")
            }
            
            launch {
                delay(300L)
                println("2-bola: Men bu satrga yetib bormayman!")
            }
        }.join()
    } catch (e: Exception) {
        println("Ota ko'lamda xato ushlandi: ${e.message}")
    }
}
""",
    "Standart koroutina iyerarxiyasida ikki tomonlama xatolik tarqalishi (bidirectional error propagation) mavjud: bitta bola qulasa, ota koroutina va qolgan barcha bolalar bekor qilinadi.",
    """
1-bola: Kutilmagan qulash!
Ota ko'lamda xato ushlandi: Bazada xatolik
"""
)

# 761
add_task(
    761,
    "SupervisorJob bilan bolalarning xatolarini mustaqil qilish",
    "SupervisorJob yordamida bitta bola vazifa qulasa ham boshqa mustaqil bolalar ishlashda davom etishini ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val supervisor = CoroutineScope(Dispatchers.Default + SupervisorJob())
    
    val job1 = supervisor.launch {
        println("1-bola: Xato sodir bo'lmoqda...")
        throw RuntimeException("1-xizmat ishdan chiqdi!")
    }
    
    val job2 = supervisor.launch {
        delay(200L)
        println("2-bola: 1-bola qulagan bo'lsa ham men muvaffaqiyatli ishladim!")
    }
    
    job1.join()
    job2.join()
}
""",
    "SupervisorJob bir tomonlama bekor qilishni (one-way cancellation) amalga oshiradi: ota bekor qilinsa bolalar to'xtaydi, ammo bitta bolaning qulashi otaga va boshqa bolalarga ta'sir qilmaydi.",
    """
1-bola: Xato sodir bo'lmoqda...
2-bola: 1-bola qulagan bo'lsa ham men muvaffaqiyatli ishladim!
"""
)

# 762
add_task(
    762,
    "supervisorScope yordamida lokal xatoliklarni izolyatsiya qilish",
    "Funksiya ichida supervisorScope builder'ini ishlatib, parallel so'rovlarning biridagi xatodan boshqalarini himoya qiling.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.supervisorScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

suspend fun loadMicroservices() = supervisorScope {
    launch {
        delay(100L)
        println("Auth xizmati: OK")
    }
    launch {
        delay(150L)
        println("Tavsiya xizmati: Xatolik yuz berdi (lekin tizim qulamasligi kerak)")
        throw RuntimeException("Tavsiya bazasi mavjud emas")
    }
    launch {
        delay(200L)
        println("To'lov xizmati: OK")
    }
}

fun main() = runBlocking {
    loadMicroservices()
    println("Barcha mikroservislar tekshiruvi yakunlandi.")
}
""",
    "supervisorScope coroutineScope kabi to'xtatuvchi ko'lam yaratadi, biroq uning ichidagi birorta bolaning istisnosi butun ko'lamni va boshqa bolalarni bekor qilmaydi.",
    """
Auth xizmati: OK
Tavsiya xizmati: Xatolik yuz berdi (lekin tizim qulamasligi kerak)
To'lov xizmati: OK
Barcha mikroservislar tekshiruvi yakunlandi.
"""
)

# 763
add_task(
    763,
    "CoroutineExceptionHandler va SupervisorJob hamkorligi",
    "SupervisorJob bilan ishlayotgan koroutinada yuz bergan istisnolarni markazlashgan CoroutineExceptionHandler orqali qayd eting.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.CoroutineExceptionHandler
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val handler = CoroutineExceptionHandler { _, exception ->
        println("Markaziy xato qaydnomasi: ${exception.message}")
    }
    
    val scope = CoroutineScope(Dispatchers.Default + SupervisorJob() + handler)
    
    val job1 = scope.launch {
        throw IllegalStateException("API kaliti muddati tugagan!")
    }
    val job2 = scope.launch {
        delay(100L)
        println("Statistika muvaffaqiyatli yangilandi.")
    }
    
    job1.join()
    job2.join()
}
""",
    "SupervisorJob ostidagi koroutinalarda CoroutineExceptionHandler har bir bolaning ushlanmagan xatolarini mustaqil ravishda ushlab beradi.",
    """
Markaziy xato qaydnomasi: API kaliti muddati tugagan!
Statistika muvaffaqiyatli yangilandi.
"""
)

# 764
add_task(
    764,
    "async va supervisorScope birgalikda: xatoli deferred natijasini ushlash",
    "supervisorScope ichida async chaqirib, uning await() metodida xatoni try-catch bilan xavfsiz qabul qilishni ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.supervisorScope
import kotlinx.coroutines.async
import kotlinx.coroutines.delay

fun main() = runBlocking {
    supervisorScope {
        val def1 = async {
            delay(100L)
            "Server-A ma'lumoti"
        }
        val def2 = async {
            delay(100L)
            throw IllegalArgumentException("Server-B ulanish rad etildi!")
        }
        
        println("1-server: ${def1.await()}")
        try {
            println("2-server: ${def2.await()}")
        } catch (e: Exception) {
            println("2-serverdan muqobil qiymat: Xatolik (${e.message})")
        }
    }
}
""",
    "supervisorScope ichida bo'lgani sababli, def2 dagi istisno def1 ning natijasini yo'qqa chiqarmaydi va await() chaqirilganda lokal catch qilinishi mumkin.",
    """
1-server: Server-A ma'lumoti
2-serverdan muqobil qiymat: Xatolik (Server-B ulanish rad etildi!)
"""
)

# 765
add_task(
    765,
    "withContext(Dispatchers.IO) orqali fayl o'qishni o'tkazish",
    "Asosiy oqimdan IO oqimiga o'tib, matnli fayl yuklash simulyatsiyasini amalga oshiring va asosiy oqimga qayting.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay

suspend fun readConfigAsync(): String = withContext(Dispatchers.IO) {
    println("Konfiguratsiya o'qilmoqda: ${Thread.currentThread().name}")
    delay(200L)
    "database_url=jdbc:postgresql://localhost:5432/main"
}

fun main() = runBlocking {
    println("Boshlang'ich oqim: ${Thread.currentThread().name}")
    val config = readConfigAsync()
    println("Konfig olindi: $config")
    println("Qaytgan oqim: ${Thread.currentThread().name}")
}
""",
    "withContext() oqimni xavfsiz almashtiradi va natija qaytgach, chaqiruvchi oqimga avtomatik qaytaradi. Bu callback'larsiz oqim boshqarishning eng qulay usulidir.",
    """
Boshlang'ich oqim: main
Konfiguratsiya o'qilmoqda: DefaultDispatcher-worker-1
Konfig olindi: database_url=jdbc:postgresql://localhost:5432/main
Qaytgan oqim: main
"""
)

# 766
add_task(
    766,
    "Mutex yordamida poyga holati (race condition) ni bartaraf etish",
    "1000 ta parallel koroutina umumiy o'zgaruvchini oshirganda ma'lumot yo'qolishining oldini oluvchi Mutex yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock

fun main() = runBlocking {
    val mutex = Mutex()
    var hisoblagich = 0
    val total = 1000
    
    val jobs = List(total) {
        launch(Dispatchers.Default) {
            mutex.withLock {
                hisoblagich++
            }
        }
    }
    jobs.forEach { it.join() }
    
    println("Kutilgan: $total, Haqiqiy natija: $hisoblagich")
}
""",
    "Mutex (Mutual Exclusion) koroutinalar uchun mo'ljallangan to'xtatuvchi qulfdir. withLock bloki orqali bir vaqtning o'zida faqat bitta koroutina kritik bo'limga (critical section) kira oladi.",
    """
Kutilgan: 1000, Haqiqiy natija: 1000
"""
)

# 767
add_task(
    767,
    "AtomicInteger yordamida yengil konkurent hisoblagich",
    "Oddiy butun sonlar uchun Mutex o'rniga Lock-free bo'lgan AtomicInteger sinfidan foydalanishni namoyish eting.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers
import java.util.concurrent.atomic.AtomicInteger

fun main() = runBlocking {
    val atomicCounter = AtomicInteger(0)
    val total = 1000
    
    val jobs = List(total) {
        launch(Dispatchers.Default) {
            atomicCounter.incrementAndGet()
        }
    }
    jobs.forEach { it.join() }
    
    println("Atomic hisoblagich natijasi: ${atomicCounter.get()}")
}
""",
    "Atomic turlari protsessor darajasidagi Compare-And-Swap (CAS) operatsiyalaridan foydalanadi va oddiy hisoblashlarda qulflarga (lock) qaraganda ancha tez ishlaydi.",
    """
Atomic hisoblagich natijasi: 1000
"""
)

# 768
add_task(
    768,
    "Thread confinement: bitta oqimga cheklash orqali sinxronizatsiya",
    "newSingleThreadContext orqali barcha amallarni faqat bitta oqimda bajarish hisobiga hech qanday qulfsiz poyga holatidan qutuling.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.newSingleThreadContext

fun main() = runBlocking {
    val singleThread = newSingleThreadContext("HisobchiOqim")
    var oddiyHisoblagich = 0
    val total = 1000
    
    val jobs = List(total) {
        launch(singleThread) {
            oddiyHisoblagich++
        }
    }
    jobs.forEach { it.join() }
    singleThread.close()
    
    println("Bitta oqimga cheklangan natija: $oddiyHisoblagich")
}
""",
    "Oqimga cheklash (Thread Confinement) yondashuvida o'zgaruvchi bilan faqat bitta belgilangan oqim ishlaydi. Natijada hech qanday sinxronizatsiya overhead'i bo'lmaydi.",
    """
Bitta oqimga cheklangan natija: 1000
"""
)

# 769
add_task(
    769,
    "Semaphore orqali ruxsat etilgan parallel operatsiyalar sonini cheklash",
    "Tizimga ortiqcha yuk tushmasligi uchun bir vaqtda maksimal 2 ta operatsiyaga ruxsat beruvchi Semaphore yarating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.sync.Semaphore
import kotlinx.coroutines.sync.withPermit
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val semaphore = Semaphore(2) // bir vaqtda 2 ta koroutina
    
    repeat(5) { id ->
        launch(Dispatchers.Default) {
            semaphore.withPermit {
                println("Vazifa #$id ruxsat oldi va ishlamoqda...")
                delay(200L)
                println("Vazifa #$id yakunlandi va ruxsatni bo'shatdi.")
            }
        }
    }
}
""",
    "Semaphore belgilangan sondagi ruxsatnomalar (permits) taqdim etadi. withPermit mavjud ruxsatlar tugaganda yangi koroutinalarni to'xtatib turadi.",
    """
Vazifa #0 ruxsat oldi va ishlamoqda...
Vazifa #1 ruxsat oldi va ishlamoqda...
Vazifa #0 yakunlandi va ruxsatni bo'shatdi.
Vazifa #2 ruxsat oldi va ishlamoqda...
Vazifa #1 yakunlandi va ruxsatni bo'shatdi.
Vazifa #3 ruxsat oldi va ishlamoqda...
Vazifa #2 yakunlandi va ruxsatni bo'shatdi.
Vazifa #4 ruxsat oldi va ishlamoqda...
Vazifa #3 yakunlandi va ruxsatni bo'shatdi.
Vazifa #4 yakunlandi va ruxsatni bo'shatdi.
"""
)

# 770
add_task(
    770,
    "CompletableJob orqali koroutinani qo'lda complete() qilish",
    "Job() yordamida CompletableJob yaratib, barcha ishlar yakunlanganini qo'lda e'lon qilishni namoyish eting.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val myJob = Job()
    
    launch(myJob) {
        println("1-xizmat ishlamoqda...")
        delay(100L)
    }
    launch(myJob) {
        println("2-xizmat ishlamoqda...")
        delay(150L)
    }
    
    myJob.complete() // Yangi bolalarni qabul qilmaydi, mavjudlari tugashini kutadi
    myJob.join()
    println("CompletableJob to'liq muvaffaqiyatli yakunlandi.")
}
""",
    "Job() orqali olingan CompletableJob da complete() metodi chaqirilsa, u Completing holatiga o'tadi va barcha faol bolalar tugagach Completed bo'ladi.",
    """
1-xizmat ishlamoqda...
2-xizmat ishlamoqda...
CompletableJob to'liq muvaffaqiyatli yakunlandi.
"""
)

# 771
add_task(
    771,
    "Bekor qilingan koroutinada isActive va isCancelled xususiyatlari",
    "Bekor qilish amalga oshirilgandan so'ng Job xususiyatlarining holatini konsolda ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val job = launch {
        delay(1000L)
    }
    
    println("Bekor qilishdan avval: isActive=${job.isActive}, isCancelled=${job.isCancelled}")
    job.cancel()
    println("Bekor qilingach: isActive=${job.isActive}, isCancelled=${job.isCancelled}")
}
""",
    "cancel() chaqirilishi bilan isActive zudlik bilan `false`, isCancelled esa `true` bo'ladi.",
    """
Bekor qilishdan avval: isActive=true, isCancelled=false
Bekor qilingach: isActive=false, isCancelled=true
"""
)

# 772
add_task(
    772,
    "Ota koroutina bekor qilinganda barcha bolalar avtomatik bekor bo'lishi",
    "Ota koroutina cancel qilinganda uning barcha avlodlari bir zumda to'xtatilishini isbotlang.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val ota = launch {
        launch {
            try {
                repeat(10) { i ->
                    println("1-bola: ishlayapti ($i)")
                    delay(100L)
                }
            } finally {
                println("1-bola to'xtatildi!")
            }
        }
        launch {
            try {
                repeat(10) { i ->
                    println("2-bola: ishlayapti ($i)")
                    delay(100L)
                }
            } finally {
                println("2-bola to'xtatildi!")
            }
        }
    }
    
    delay(250L)
    println("Ota koroutina bekor qilinmoqda...")
    ota.cancel()
    ota.join()
}
""",
    "Strukturalangan konkurentlikning asosiy qoidasi: ota koroutina bekor qilinsa, uning barcha ichki bolalari zudlik bilan kaskadli ravishda bekor qilinadi.",
    """
1-bola: ishlayapti (0)
2-bola: ishlayapti (0)
1-bola: ishlayapti (1)
2-bola: ishlayapti (1)
1-bola: ishlayapti (2)
2-bola: ishlayapti (2)
Ota koroutina bekor qilinmoqda...
1-bola to'xtatildi!
2-bola to'xtatildi!
"""
)

# 773
add_task(
    773,
    "suspendCancellableCoroutine bilan callback asosidagi kutubxonani koroutinaga moslash",
    "Eski uslubdagi listener/callback arxitekturasini zamonaviy suspendCancellableCoroutine yordamida to'xtatuvchi funksiyaga aylantiring.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlin.concurrent.thread
import kotlin.coroutines.resume

interface LegacyCallback {
    fun onSuccess(data: String)
}

fun legacyApiCall(callback: LegacyCallback) {
    thread {
        Thread.sleep(200L)
        callback.onSuccess("Eski API dan ma'lumot")
    }
}

suspend fun fetchFromLegacyApi(): String = suspendCancellableCoroutine { continuation ->
    legacyApiCall(object : LegacyCallback {
        override fun onSuccess(data: String) {
            continuation.resume(data)
        }
    })
}

fun main() = runBlocking {
    println("Callback chaqiruvi boshlandi...")
    val natija = fetchFromLegacyApi()
    println("Natija olindi: $natija")
}
""",
    "suspendCancellableCoroutine callback chaqiruvlarini zamonaviy koroutina uslubiga (suspend funksiya) o'girish uchun asosiy ko'prik vositasidir.",
    """
Callback chaqiruvi boshlandi...
Natija olindi: Eski API dan ma'lumot
"""
)

# 774
add_task(
    774,
    "invokeOnCancellation bilan tinglovchini tozalash",
    "suspendCancellableCoroutine ichida bekor qilish sodir bo'lganda tashqi manbadagi ulanishni uzuvchi callback ro'yxatdan o'tkazing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlinx.coroutines.delay
import kotlinx.coroutines.cancelAndJoin

suspend fun cancellableSensorStream(): String = suspendCancellableCoroutine { cont ->
    println("Sensor tinglovchisi ulandi")
    
    cont.invokeOnCancellation {
        println("Tozalash: Sensor tinglovchisi uzildi!")
    }
}

fun main() = runBlocking {
    val job = launch {
        cancellableSensorStream()
    }
    
    delay(100L)
    println("Ilova yopilmoqda, sensor bekor qilinadi:")
    job.cancelAndJoin()
}
""",
    "invokeOnCancellation agar koroutina kutish vaqtida bekor qilinsa, resurslarni tozalash, soketlarni yopish yoki listenerlarni bekor qilish uchun juda muhimdir.",
    """
Sensor tinglovchisi ulandi
Ilova yopilmoqda, sensor bekor qilinadi:
Tozalash: Sensor tinglovchisi uzildi!
"""
)

# 775
add_task(
    775,
    "Asinxron fayl yuklash jarayonini foydalanuvchi tugmasi bilan bekor qilish simulyatsiyasi",
    "Foydalanuvchi katta faylni yuklashni istalgan paytda to'xtata olishi uchun cancellation mexanizmini to'liq loyihalashtiring.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import kotlinx.coroutines.cancelAndJoin

fun main() = runBlocking {
    val downloadJob = launch {
        try {
            for (progress in 10..100 step 10) {
                println("Yuklanmoqda: $progress%")
                delay(150L)
            }
            println("Fayl to'liq yuklandi!")
        } finally {
            println("Vaqtinchalik yuklangan (.part) fayllar diskdan tozalandi.")
        }
    }
    
    delay(350L)
    println("[Foydalanuvchi: Bekor qilish tugmasini bosdi]")
    downloadJob.cancelAndJoin()
    println("Yuklash to'liq to'xtatildi.")
}
""",
    "Yuklash jarayoni bekor qilinganda finally bloki xomaki fayllarni tozalab, foydalanuvchi xotirasini tejaydi.",
    """
Yuklanmoqda: 10%
Yuklanmoqda: 20%
Yuklanmoqda: 30%
[Foydalanuvchi: Bekor qilish tugmasini bosdi]
Vaqtinchalik yuklangan (.part) fayllar diskdan tozalandi.
Yuklash to'liq to'xtatildi.
"""
)

# 776
add_task(
    776,
    "Web-sahifani yuklashda timeout o'rnatish va zaxira keshga o'tish",
    "Tarmoqdan yangiliklar lentasini olishda 300ms cheklov qo'ying, agar kechiksa keshdagi yangiliklarni qaytaring.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withTimeoutOrNull
import kotlinx.coroutines.delay

suspend fun fetchLiveNews(): String {
    delay(500L) // tarmoq sekin
    return "Jonli yangiliklar: Toshkentda IT sammit"
}

fun getCachedNews(): String = "Keshdagi yangiliklar: Dasturlash bo'yicha yangi kurslar"

fun main() = runBlocking {
    println("Yangiliklar qidirilmoqda...")
    val live = withTimeoutOrNull(300L) { fetchLiveNews() }
    val result = live ?: getCachedNews()
    println("Ekranga chiqarildi -> $result")
}
""",
    "withTimeoutOrNull va Elvis operatori (`?:`) kombinatsiyasi tarmoq sekinlashganda ilova muzlab qolmasdan darhol offline keshga o'tishini ta'minlaydi.",
    """
Yangiliklar qidirilmoqda...
Ekranga chiqarildi -> Keshdagi yangiliklar: Dasturlash bo'yicha yangi kurslar
"""
)

# 777
add_task(
    777,
    "Ma'lumotlar bazasiga tranzaksiyani NonCancellable orqali yozish",
    "Foydalanuvchi jarayonni bekor qilgan taqdirda ham, audit jurnaliga (audit log) ma'lumot yozilishini kafolatlang.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import kotlinx.coroutines.cancelAndJoin
import kotlinx.coroutines.withContext
import kotlinx.coroutines.NonCancellable

fun main() = runBlocking {
    val transactionJob = launch {
        try {
            println("To'lov boshlandi...")
            delay(500L)
        } finally {
            withContext(NonCancellable) {
                println("Audit: Bekor qilingan tranzaksiya bazaga yozilmoqda...")
                delay(100L)
                println("Audit: Muvaffaqiyatli qayd etildi.")
            }
        }
    }
    
    delay(100L)
    transactionJob.cancelAndJoin()
    println("Tranzaksiya bekor qilindi.")
}
""",
    "Moliyaviy va xavfsizlik dasturlarida bekor qilingan urinishlarni ham bazaga yozish shart. NonCancellable bu vazifani xavfsiz bajaradi.",
    """
To'lov boshlandi...
Audit: Bekor qilingan tranzaksiya bazaga yozilmoqda...
Audit: Muvaffaqiyatli qayd etildi.
Tranzaksiya bekor qilindi.
"""
)

# 778
add_task(
    778,
    "Parallel rasmlarni qayta ishlashda bitta rasm xatosi boshqalariga ta'sir qilmasligi",
    "SupervisorJob va async yordamida bir nechta rasmdan biri buzilgan bo'lsa ham qolganlarini muvaffaqiyatli saqlovchi konvertor yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.supervisorScope
import kotlinx.coroutines.async
import kotlinx.coroutines.delay

data class ImageResult(val filename: String, val success: Boolean)

suspend fun convertImage(name: String): ImageResult {
    delay(100L)
    if (name.contains("corrupt")) {
        throw IllegalArgumentException("Buzilgan rasm: $name")
    }
    return ImageResult(name, true)
}

fun main() = runBlocking {
    val files = listOf("foto1.png", "corrupt_foto.png", "foto2.png")
    
    supervisorScope {
        val jobs = files.map { file ->
            async {
                try {
                    convertImage(file)
                } catch (e: Exception) {
                    ImageResult(file, false)
                }
            }
        }
        
        jobs.forEach {
            val res = it.await()
            println("Fayl: ${res.filename}, Holat: ${if (res.success) "Tayyor" else "Xato"}")
        }
    }
}
""",
    "supervisorScope va individual try-catch yordamida har bir rasm mustaqil qayta ishlanadi va bitta nosoz rasm butun partiyani to'xtatmaydi.",
    """
Fayl: foto1.png, Holat: Tayyor
Fayl: corrupt_foto.png, Holat: Xato
Fayl: foto2.png, Holat: Tayyor
"""
)

# 779
add_task(
    779,
    "To'lov tizimida Mutex orqali bitta hisobdan bir vaqtda pul yechilishini to'sish",
    "Bank hisobidan 5 ta parallel so'rov bir vaqtda pul yechmoqchi bo'lganda poyga holatini bartaraf qiluvchi bank hisob sinfini tuzing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock

class BankAccount(private var balance: Double) {
    private val mutex = Mutex()
    
    suspend fun withdraw(amount: Double): Boolean = mutex.withLock {
        if (balance >= amount) {
            balance -= amount
            println("-$amount $ yechildi, qoldiq: $balance $")
            true
        } else {
            println("Yetarli mablag' yo'q: so'raldi: $amount $, qoldiq: $balance $")
            false
        }
    }
}

fun main() = runBlocking {
    val account = BankAccount(100.0)
    
    val jobs = List(3) {
        launch(Dispatchers.Default) {
            account.withdraw(40.0)
        }
    }
    jobs.forEach { it.join() }
}
""",
    "Mutex.withLock balanso'zgarishini qulflab bergani sababli hisob manfiyga tushib ketmaydi va pul xavfsiz yechiladi.",
    """
-40.0 $ yechildi, qoldiq: 60.0 $
-40.0 $ yechildi, qoldiq: 20.0 $
Yetarli mablag' yo'q: so'raldi: 40.0 $, qoldiq: 20.0 $
"""
)

# 780
add_task(
    780,
    "Online test tizimida javob berish vaqtini cheklash",
    "Har bir test savoliga 200ms vaqt berilib, vaqt tugasa test bekor qilinishini simulyatsiya qiling.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withTimeoutOrNull
import kotlinx.coroutines.delay

suspend fun answerQuestion(answerTimeMs: Long): String {
    delay(answerTimeMs)
    return "A varianti"
}

fun main() = runBlocking {
    val savol1 = withTimeoutOrNull(200L) { answerQuestion(100L) }
    println("1-savol javobi: ${savol1 ?: "Vaqt tugadi!"}")
    
    val savol2 = withTimeoutOrNull(200L) { answerQuestion(300L) }
    println("2-savol javobi: ${savol2 ?: "Vaqt tugadi!"}")
}
""",
    "withTimeoutOrNull savolga berilgan vaqt tugaganda javob qabul qilinmasligini juda toza va sodda tarzda ta'minlaydi.",
    """
1-savol javobi: A varianti
2-savol javobi: Vaqt tugadi!
"""
)

# 781
add_task(
    781,
    "Tarmoq uzilganda yuklashni bekor qilish va xabardor qilish",
    "Tarmoq yo'qolganda koroutina bekor qilinishi va tinglovchi orqali foydalanuvchiga bildirishnoma chiqishini ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import kotlinx.coroutines.cancelAndJoin
import kotlinx.coroutines.CancellationException

fun main() = runBlocking {
    val networkJob = launch {
        try {
            while (true) {
                delay(100L)
            }
        } catch (e: CancellationException) {
            println("Xabarnoma: Tarmoq uzildi! (${e.message})")
            throw e
        }
    }
    
    delay(250L)
    networkJob.cancel(CancellationException("Wi-Fi tarmog'i o'chirildi"))
    networkJob.join()
}
""",
    "cancel(CancellationException(\"sabab\")) metodi bekor qilish sababini xabarda ifodalash imkonini beradi.",
    """
Xabarnoma: Tarmoq uzildi! (Wi-Fi tarmog'i o'chirildi)
"""
)

# 782
add_task(
    782,
    "Katta hisobot eksportini to'xtatganda ensureActive orqali chiqish",
    "Million satrli faylni eksport qilish jarayonida har 100 ming satrda bekor qilinganlikni tekshiring.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.cancelAndJoin
import kotlinx.coroutines.ensureActive
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val exportJob = launch(Dispatchers.Default) {
        try {
            for (row in 1..500_000) {
                if (row % 100_000 == 0) {
                    ensureActive()
                    println("$row satr eksport qilindi...")
                }
            }
        } finally {
            println("Eksport to'xtatildi, xotira tozalandi.")
        }
    }
    
    delay(5L)
    exportJob.cancelAndJoin()
    println("Eksport to'liq bekor qilindi.")
}
""",
    "ensureActive() sikl ichida har doim Cancellation holatini tekshirib, bekor qilish chaqirilgan bo'lsa darhol chiqib ketishni ta'minlaydi.",
    """
Eksport to'xtatildi, xotira tozalandi.
Eksport to'liq bekor qilindi.
"""
)

# 783
add_task(
    783,
    "Bir vaqtning o'zida maksimal 3 ta yuklashga ruxsat beruvchi Semaphore nazoratchisi",
    "Tarmoq o'tkazuvchanligini oshirib yubormaslik uchun bir vaqtda faqat 3 ta yuklashga ruxsat bering.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.sync.Semaphore
import kotlinx.coroutines.sync.withPermit
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val downloadGate = Semaphore(3)
    val files = listOf("audio1.mp3", "video.mp4", "doc.pdf", "image.png", "archive.zip")
    
    val jobs = files.map { file ->
        launch(Dispatchers.Default) {
            downloadGate.withPermit {
                println("Yuklanmoqda: $file")
                delay(150L)
                println("Yakunlandi: $file")
            }
        }
    }
    jobs.forEach { it.join() }
}
""",
    "Semaphore(3) faqat 3 ta oqimga parallel ishlashga ruxsat beradi, boshqalari esa navbatda xavfsiz kutib turadi.",
    """
Yuklanmoqda: audio1.mp3
Yuklanmoqda: video.mp4
Yuklanmoqda: doc.pdf
Yakunlandi: audio1.mp3
Yuklanmoqda: image.png
Yakunlandi: video.mp4
Yuklanmoqda: archive.zip
Yakunlandi: doc.pdf
Yakunlandi: image.png
Yakunlandi: archive.zip
"""
)

# 784
add_task(
    784,
    "Xavfsiz qayta urinish (Retry with exponential backoff) mexanizmi",
    "Vaqtinchalik xatolik yuz berganda operatsiyani ortib boruvchi kechikish bilan qayta urinuvchi yordamchi funksiya yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.delay

suspend fun <T> retryWithBackoff(
    times: Int = 3,
    initialDelay: Long = 100L,
    factor: Double = 2.0,
    block: suspend () -> T
): T {
    var currentDelay = initialDelay
    repeat(times - 1) { attempt ->
        try {
            return block()
        } catch (e: Exception) {
            println("Urinish #${attempt + 1} muvaffaqiyatsiz: ${e.message}. Qayta urinish: ${currentDelay}ms dan keyin")
            delay(currentDelay)
            currentDelay = (currentDelay * factor).toLong()
        }
    }
    return block() // Oxirgi urinish
}

fun main() = runBlocking {
    var attempts = 0
    val result = retryWithBackoff(times = 3) {
        attempts++
        if (attempts < 3) throw RuntimeException("Ulanish xatosi")
        "Muvaffaqiyatli server javobi"
    }
    println("Yakuniy natija: $result")
}
""",
    "Eksponentsial orqaga chekinish (Exponential Backoff) tarmoq beqaror bo'lganda serverni so'rovlar bilan ko'mib tashlamasdan xavfsiz qayta urinish imkonini beradi.",
    """
Urinish #1 muvaffaqiyatsiz: Ulanish xatosi. Qayta urinish: 100ms dan keyin
Urinish #2 muvaffaqiyatsiz: Ulanish xatosi. Qayta urinish: 200ms dan keyin
Yakuniy natija: Muvaffaqiyatli server javobi
"""
)

# 785
add_task(
    785,
    "Timeout bilan birgalikda qayta urinish mexanizmi",
    "Har bir urinishga aniq timeout o'rnatilgan va timeout sodir bo'lganda qayta urinuvchi xizmat tuzing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withTimeoutOrNull
import kotlinx.coroutines.delay

suspend fun unreliableService(attempt: Int): String {
    if (attempt == 1) {
        delay(400L) // kechikadi
    } else {
        delay(100L) // tez ishlaydi
    }
    return "Ma'lumotlar to'plami #$attempt"
}

fun main() = runBlocking {
    var result: String? = null
    for (i in 1..2) {
        println("Urinish $i: 200ms timeout bilan...")
        result = withTimeoutOrNull(200L) {
            unreliableService(i)
        }
        if (result != null) break
        println("Vaqt yetmadi, qayta uriniladi...")
    }
    println("Olingan natija: $result")
}
""",
    "withTimeoutOrNull orqali har bir urinishga vaqt cheklovi qo'yilib, javob bermagan sekin so'rovlar to'xtatiladi va qayta yangi so'rov yuboriladi.",
    """
Urinish 1: 200ms timeout bilan...
Vaqt yetmadi, qayta uriniladi...
Urinish 2: 200ms timeout bilan...
Olingan natija: Ma'lumotlar to'plami #2
"""
)

# 786
add_task(
    786,
    "Bloklovchi Java kodi va koroutinalar integratsiyasi: runInterruptible",
    "Bloklovchi Java I/O funksiyasini koroutina bekor qilinganda Thread.interrupt() chaqiradigan runInterruptible bilan o'rang.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.runInterruptible
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.cancelAndJoin
import kotlinx.coroutines.delay

fun blockingJavaOperation() {
    Thread.sleep(500L)
}

fun main() = runBlocking {
    val job = launch(Dispatchers.IO) {
        try {
            runInterruptible {
                println("Bloklovchi Java kodi boshlandi...")
                blockingJavaOperation()
                println("Bloklovchi Java kodi tugadi.")
            }
        } catch (e: Exception) {
            println("Java oqimi uzildi (interrupted): ${e.javaClass.simpleName}")
        }
    }
    
    delay(100L)
    println("Koroutina bekor qilinmoqda...")
    job.cancelAndJoin()
    println("Dastur yakunlandi.")
}
""",
    "runInterruptible bloklovchi kodni o'raydi va koroutina bekor qilinganda tegishli oqimga `Thread.interrupt()` yuborib, blokdan tezkor chiqishni ta'minlaydi.",
    """
Bloklovchi Java kodi boshlandi...
Koroutina bekor qilinmoqda...
Java oqimi uzildi (interrupted): InterruptedException
Dastur yakunlandi.
"""
)

# 787
add_task(
    787,
    "Koroutina bekor bo'lganda resurslarni avtomatik yopish: use funktsiyasi",
    "AutoCloseable obyektini koroutinada use bilan o'rab, bekor qilinganda ham xavfsiz yopilishini ko'rsating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import kotlinx.coroutines.cancelAndJoin

class SafeResource : AutoCloseable {
    init { println("Xavfsiz resurs ochildi.") }
    override fun close() { println("Xavfsiz resurs avtomatik yopildi!") }
}

fun main() = runBlocking {
    val job = launch {
        SafeResource().use {
            println("Resurs bilan ish olib borilmoqda...")
            delay(1000L)
        }
    }
    
    delay(150L)
    println("Bekor qilish chaqirildi:")
    job.cancelAndJoin()
}
""",
    "Kotlin ning standart .use { } kengaytmasi koroutina bekor qilinganda ham Closeable resursni yopib, xotira sizib ketishining oldini oladi.",
    """
Xavfsiz resurs ochildi.
Resurs bilan ish olib borilmoqda...
Bekor qilish chaqirildi:
Xavfsiz resurs avtomatik yopildi!
"""
)

# 788
add_task(
    788,
    "Mutaxassis darajasi: Deadlock dan saqlanish qoidalari",
    "Ikkita Mutex ishlatilganda navbatlar teskari bo'lib qolishi natijasida kelib chiqadigan qotib qolish (deadlock) va undan saqlanish tartibini tushuntiring.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val mutexA = Mutex()
    val mutexB = Mutex()
    
    // Qat'iy tartib: Avval A, keyin B olinadi
    val job1 = launch {
        mutexA.withLock {
            delay(50L)
            mutexB.withLock {
                println("Vazifa-1 ikkala qulfni xavfsiz oldi.")
            }
        }
    }
    
    val job2 = launch {
        mutexA.withLock {
            delay(50L)
            mutexB.withLock {
                println("Vazifa-2 ikkala qulfni xavfsiz oldi.")
            }
        }
    }
    
    job1.join()
    job2.join()
}
""",
    "Bir nechta Mutex ishlatilganda doimo bir xil iyerarxik ketma-ketlikda qulflash lozim. Aks holda bir koroutina A ni olib B ni kutadi, ikkinchisi B ni olib A ni kutadi va deadlock yuzaga keladi.",
    """
Vazifa-1 ikkala qulfni xavfsiz oldi.
Vazifa-2 ikkala qulfni xavfsiz oldi.
"""
)

# 789
add_task(
    789,
    "Kesh tozalash va fon xizmati monitoringi",
    "Har 200ms da ishlaydigan fon tozalash vazifasini tuzing va asosiy ish tugagach uni to'xtating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import kotlinx.coroutines.cancelAndJoin

fun main() = runBlocking {
    val janitorJob = launch {
        try {
            while (true) {
                delay(200L)
                println("Janitor: Chiqindilar va eski keshlar tozalandi.")
            }
        } finally {
            println("Janitor xizmati to'xtatildi.")
        }
    }
    
    println("Asosiy ilova 550ms davomida ishlamoqda...")
    delay(550L)
    println("Ilova yopilmoqda...")
    janitorJob.cancelAndJoin()
}
""",
    "Cheksiz sikldagi fon koroutinalari (Daemon vazifalar) delay() orqali to'xtatilishi mumkin bo'lib, ilova yakunlanganda cancelAndJoin orqali tartibli yopiladi.",
    """
Asosiy ilova 550ms davomida ishlamoqda...
Janitor: Chiqindilar va eski keshlar tozalandi.
Janitor: Chiqindilar va eski keshlar tozalandi.
Ilova yopilmoqda...
Janitor xizmati to'xtatildi.
"""
)

# 790
add_task(
    790,
    "Job.attachChild orqali koroutina aloqalarini tushunish",
    "Ota va bola Job larning bog'liqlik mexanizmini Job() hayot sikli orqali tahlil qiling.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val parentJob = Job()
    
    launch(parentJob) {
        delay(100L)
        println("1-ichki koroutina bajarildi")
    }
    launch(parentJob) {
        delay(150L)
        println("2-ichki koroutina bajarildi")
    }
    
    parentJob.complete()
    parentJob.join()
    println("Barcha biriktirilgan vazifalar to'liq yakunlandi.")
}
""",
    "Ota Job ga bog'langan barcha koroutinalar yakunlanmaguncha ota Job Completed holatiga o'tmaydi.",
    """
1-ichki koroutina bajarildi
2-ichki koroutina bajarildi
Barcha biriktirilgan vazifalar to'liq yakunlandi.
"""
)

# 791
add_task(
    791,
    "Asinxron yuklama balansi (Load balancing simulyatsiyasi)",
    "Kelayotgan 6 ta so'rovni Semaphore orqali 2 ta parallel ishchi oqimiga muvozanatlashtirib bering.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.sync.Semaphore
import kotlinx.coroutines.sync.withPermit
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val balanceGate = Semaphore(2)
    
    val jobs = (1..4).map { id ->
        launch {
            balanceGate.withPermit {
                println("So'rov #$id qabul qilindi")
                delay(100L)
                println("So'rov #$id javob berildi")
            }
        }
    }
    jobs.forEach { it.join() }
}
""",
    "Semaphore yordamida backend servislariga bir vaqtning o'zida tushadigan so'rovlar chegaralanadi, bu esa ortiqcha yuklanishdan asraydi.",
    """
So'rov #1 qabul qilindi
So'rov #2 qabul qilindi
So'rov #1 javob berildi
So'rov #2 javob berildi
So'rov #3 qabul qilindi
So'rov #4 qabul qilindi
So'rov #3 javob berildi
So'rov #4 javob berildi
"""
)

# 792
add_task(
    792,
    "CoroutineContext da ExceptionHandler ni dinamik qo'shish",
    "Har bir koroutinaga o'zining shaxsiy istisno qayta ishlovchisini dinamik tarzda biriktiring.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.CoroutineExceptionHandler
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch

fun main() = runBlocking {
    val handler1 = CoroutineExceptionHandler { _, ex ->
        println("1-vazifa xatosi ushlandi: ${ex.message}")
    }
    
    val job = GlobalScope.launch(handler1) {
        throw ArithmeticException("Nolga bo'lish yuz berdi")
    }
    job.join()
}
""",
    "CoroutineExceptionHandler har bir koroutinaning kontekstiga alohida berilishi mumkin bo'lib, uning xatolarini markaziy qayta ishlashga uzatadi.",
    """
1-vazifa xatosi ushlandi: Nolga bo'lish yuz berdi
"""
)

# 793
add_task(
    793,
    "Bekor qilish vaqtida ulanishni xavfsiz uzish (Safe Disconnect)",
    "IoT qurilmasi bilan bog'langan Bluetooth yoki MQTT ulanishini bekor qilishda xavfsiz tozalash.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import kotlinx.coroutines.cancelAndJoin

class DeviceConnection {
    fun connect() = println("Qurilma ulandi: BLE")
    fun disconnect() = println("Qurilma uzildi: BLE port yopildi.")
}

fun main() = runBlocking {
    val conn = DeviceConnection()
    val job = launch {
        conn.connect()
        try {
            while (true) {
                delay(100L)
            }
        } finally {
            conn.disconnect()
        }
    }
    
    delay(250L)
    job.cancelAndJoin()
}
""",
    "finally blokida qurilma bilan ulanish uziladi va Bluetooth drayveri ochiq qolib ketishining oldi olinadi.",
    """
Qurilma ulandi: BLE
Qurilma uzildi: BLE port yopildi.
"""
)

# 794
add_task(
    794,
    "withTimeout ichida resurs yaratish xavfi va to'g'ri yechim",
    "withTimeout ichida resurs yaratilganda timeout istisnosi tufayli resurs yopilmay qolish xavfini to'g'ri bartaraf etish usuli.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withTimeout
import kotlinx.coroutines.delay

class MyFileResource : AutoCloseable {
    init { println("Resurs ochildi") }
    override fun close() { println("Resurs yopildi") }
}

fun main() = runBlocking {
    var res: MyFileResource? = null
    try {
        withTimeout(200L) {
            res = MyFileResource()
            delay(500L) // timeout yuz beradi
        }
    } catch (e: Exception) {
        println("Timeout yuz berdi!")
    } finally {
        res?.close()
    }
}
""",
    "withTimeout chaqiruvidan tashqarida o'zgaruvchi e'lon qilib, finally blokida tozalash resurs ochiq qolib ketishidan asraydi.",
    """
Resurs ochildi
Timeout yuz berdi!
Resurs yopildi
"""
)

# 795
add_task(
    795,
    "Asinxron navbat (Queue) simulyatsiyasi",
    "Bitta yozuvchi va bitta o'quvchi o'rtasida ma'lumotlarni tartibli almashish simulyatsiyasini yozing.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.delay

class SimpleAsyncQueue<T> {
    private val list = mutableListOf<T>()
    private val mutex = Mutex()
    
    suspend fun enqueue(item: T) = mutex.withLock {
        list.add(item)
    }
    
    suspend fun dequeue(): T? = mutex.withLock {
        if (list.isNotEmpty()) list.removeAt(0) else null
    }
}

fun main() = runBlocking {
    val queue = SimpleAsyncQueue<String>()
    
    launch {
        queue.enqueue("Xabar-1")
        queue.enqueue("Xabar-2")
    }.join()
    
    println("Navbatdan olindi: ${queue.dequeue()}")
    println("Navbatdan olindi: ${queue.dequeue()}")
}
""",
    "Mutex orqali himoyalangan sodda navbat ma'lumotlarning yo'qolishisiz va xavfsiz tartibda o'qilishini ta'minlaydi.",
    """
Navbatdan olindi: Xabar-1
Navbatdan olindi: Xabar-2
"""
)

# 796
add_task(
    796,
    "Koroutina bekor qilinganda sababni o'qish (Cancellation reason)",
    "cancel(reason) chaqirilganda, Job.getCancellationException() orqali aniq sababni aniqlash.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import kotlinx.coroutines.CancellationException

fun main() = runBlocking {
    val job = launch {
        delay(1000L)
    }
    
    delay(100L)
    job.cancel(CancellationException("Foydalanuvchi sahifani yopdi"))
    job.join()
    
    val reason = job.getCancellationException().message
    println("Bekor qilish sababi: $reason")
}
""",
    "getCancellationException() metodi orqali koroutina aynan qaysi sababga ko'ra to'xtatilganini bilish va tahlil qilish mumkin.",
    """
Bekor qilish sababi: Foydalanuvchi sahifani yopdi
"""
)

# 797
add_task(
    797,
    "Ko'p bosqichli autentifikatsiyani timeout bilan himoyalash",
    "SMS kodni kiritish jarayoniga 300ms muddat belgilab, o'z vaqtida kiritilmasa sessiyani bekor qiling.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withTimeoutOrNull
import kotlinx.coroutines.delay

suspend fun enterSmsCode(userInputDelay: Long): String {
    delay(userInputDelay)
    return "774921"
}

fun main() = runBlocking {
    println("SMS kod yuborildi. Kodni kiriting (300ms berildi):")
    val code = withTimeoutOrNull(300L) {
        enterSmsCode(150L) // o'z vaqtida kiritdi
    }
    
    if (code != null) {
        println("Kod tasdiqlandi: $code. Tizimga muvaffaqiyatli kirildi!")
    } else {
        println("Kod kiritish vaqti tugadi. Qayta urinib ko'ring.")
    }
}
""",
    "Xavfsizlik tizimlarida SMS yoki 2FA kod kiritish vaqtini cheklash uchun withTimeoutOrNull eng ixcham yechim hisoblanadi.",
    """
SMS kod yuborildi. Kodni kiriting (300ms berildi):
Kod tasdiqlandi: 774921. Tizimga muvaffaqiyatli kirildi!
"""
)

# 798
add_task(
    798,
    "SupervisorJob ostida xatolik yuz berganda qayta ishga tushirish (Restart pattern)",
    "Nosozlik yuz berganda fon xizmatini avtomatik qayta boshlovchi nazoratchi (supervisor watchdog) loyihalang.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

fun main() = runBlocking {
    val scope = CoroutineScope(Dispatchers.Default + SupervisorJob())
    var attempts = 0
    
    fun startWorker() {
        scope.launch {
            attempts++
            println("Ishchi xizmat boshlandi (Urinish #$attempts)")
            if (attempts == 1) {
                delay(50L)
                throw RuntimeException("Kutilmagan nosozlik!")
            } else {
                delay(50L)
                println("Ishchi xizmat barqaror ishlamoqda.")
            }
        }.invokeOnCompletion { ex ->
            if (ex != null && attempts < 3) {
                println("Qayta yuklanmoqda...")
                startWorker()
            }
        }
    }
    
    startWorker()
    delay(200L)
}
""",
    "SupervisorJob va invokeOnCompletion yordamida qulagan koroutinani aniqlab, xizmatni avtomatik ravishda qayta oyoqqa turgazish mumkin.",
    """
Ishchi xizmat boshlandi (Urinish #1)
Qayta yuklanmoqda...
Ishchi xizmat boshlandi (Urinish #2)
Ishchi xizmat barqaror ishlamoqda.
"""
)

# 799
add_task(
    799,
    "Asinxron audit va tozalash zanjiri (Clean-up Pipeline)",
    "Ilova to'xtatilganda keshni tozalash, ochiq fayllarni yopish va serverga yakuniy xabarni jo'natish zanjirini NonCancellable da bajaring.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import kotlinx.coroutines.cancelAndJoin
import kotlinx.coroutines.withContext
import kotlinx.coroutines.NonCancellable

fun main() = runBlocking {
    val appJob = launch {
        try {
            delay(1000L)
        } finally {
            withContext(NonCancellable) {
                println("1. Kesh tozalandi.")
                delay(50L)
                println("2. Fayl deskriptorlari yopildi.")
                delay(50L)
                println("3. Serverga 'Offline' holati bildirildi.")
            }
        }
    }
    
    delay(100L)
    println("Ilova to'xtatish buyrug'i berildi...")
    appJob.cancelAndJoin()
    println("Tizim toza holatda o'chirildi.")
}
""",
    "NonCancellable kontekstida bir nechta tozalash bosqichlari to'liq va uzluksiz bajariladi.",
    """
Ilova to'xtatish buyrug'i berildi...
1. Kesh tozalandi.
2. Fayl deskriptorlari yopildi.
3. Serverga 'Offline' holati bildirildi.
Tizim toza holatda o'chirildi.
"""
)

# 800
add_task(
    800,
    "16-qism xulosasi: Chidamli va xavfsiz parallel ma'lumot yig'ish va tranzaksiya agregatori",
    "SupervisorJob, Mutex, Timeout va NonCancellable vositalarini birlashtirgan mustahkam ko'p oqimli moliyaviy agregator tizimini yarating.",
    """
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.supervisorScope
import kotlinx.coroutines.async
import kotlinx.coroutines.withTimeoutOrNull
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.withContext
import kotlinx.coroutines.NonCancellable
import kotlinx.coroutines.delay

data class TransactionReport(val totalProcessed: Double, val successfulCount: Int)

class ResilientProcessor {
    private val mutex = Mutex()
    private var totalSum = 0.0
    private var count = 0
    
    suspend fun processPayment(id: Int, amount: Double): Boolean {
        // Har bir to'lovga 250ms vaqt beriladi
        val success = withTimeoutOrNull(250L) {
            delay(100L)
            true
        } ?: false
        
        if (success) {
            mutex.withLock {
                totalSum += amount
                count++
            }
        }
        return success
    }
    
    suspend fun getReport(): TransactionReport = mutex.withLock {
        TransactionReport(totalSum, count)
    }
}

fun main() = runBlocking {
    val processor = ResilientProcessor()
    
    supervisorScope {
        val tasks = listOf(
            async { processor.processPayment(1, 150.0) },
            async { processor.processPayment(2, 300.0) },
            async { processor.processPayment(3, 50.0) }
        )
        tasks.forEach { it.await() }
    }
    
    // Natijalarni yopish va audit
    withContext(NonCancellable) {
        val report = processor.getReport()
        println("Moliyaviy hisobot: Jami pul: ${report.totalProcessed} $, O'tgan to'lovlar soni: ${report.successfulCount}")
    }
}
""",
    "Bu murakkab tizimda: 1) supervisorScope orqali xatoliklar izolyatsiyasi ta'minlandi, 2) withTimeoutOrNull orqali har bir to'lov vaqti cheklandi, 3) Mutex orqali parallel tranzaksiyalar xavfsiz hisoblandi, 4) NonCancellable orqali yakuniy audit kafolatlandi.",
    """
Moliyaviy hisobot: Jami pul: 500.0 $, O'tgan to'lovlar soni: 3
"""
)

save_file("kotlin_16_koroutinalar_chuqur_va_bekor_qilish.md", tasks)
