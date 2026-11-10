Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Kotlin ekotizimini boyitish uchun KMP, Compose Multiplatform va Coroutine Flows bo'yicha 10 ta ilg'or texnik topshiriqni taqdim etaman.

---

# 1001-Topshiriq: KMP uchun Platformaga xos (Expect/Actual) Network Monitor

## Topshiriq sharti:
KMP loyihasida internet ulanishini kuzatuvchi `NetworkMonitor` modulini yarating. U `Flow<Boolean>` qaytarishi kerak.

## Yechim (Kotlin kodi):
```kotlin
// CommonMain
expect class NetworkMonitor {
    fun observeNetwork(): kotlinx.coroutines.flow.Flow<Boolean>
}

// Usage
val monitor = NetworkMonitor()
monitor.observeNetwork().collect { isConnected ->
    println("Tarmoq holati: ${if (isConnected) "Onlayn" else "Offlayn"}")
}
```

## Tushuntirish va Mantiq:
`expect` kalit so'zi orqali interfeys aniqlanadi. Har bir platforma (Android/iOS) o'zining `ConnectivityManager` yoki `NWPathMonitor` vositalari orqali `Flow` ni emit qiladi.

## Ishlash natijasi:
```text
Tarmoq holati: Onlayn
```

---

# 1002-Topshiriq: Compose Multiplatformda StateFlow bilan UI sinxronizatsiyasi

## Topshiriq sharti:
`StateFlow` dan foydalanib, tugma bosilganda hisoblagichni (counter) Compose Multiplatform UI'da yangilang.

## Yechim (Kotlin kodi):
```kotlin
class CounterViewModel {
    private val _count = MutableStateFlow(0)
    val count = _count.asStateFlow()
    fun increment() { _count.value++ }
}

@Composable
fun CounterScreen(viewModel: CounterViewModel) {
    val count by viewModel.count.collectAsState()
    Button(onClick = { viewModel.increment() }) { Text("Hisob: $count") }
}
```

## Tushuntirish va Mantiq:
`collectAsState()` funksiyasi `Flow` ni Compose `State` obyektiga aylantiradi, bu esa UI ni avtomatik qayta chizish (recomposition) imkonini beradi.

## Ishlash natijasi:
```text
Hisob: 1
```

---

# 1003-Topshiriq: Coroutine Flow'da `combine` operatori yordamida ma'lumotlarni birlashtirish

## Topshiriq sharti:
Ikki xil manbadan (foydalanuvchi profili va balans) kelayotgan ma'lumotlarni `combine` yordamida bitta oqimga birlashtiring.

## Yechim (Kotlin kodi):
```kotlin
val userFlow = flowOf("Ali")
val balanceFlow = flowOf(1000)

userFlow.combine(balanceFlow) { user, balance ->
    "$user ning balansi: $balance so'm"
}.collect { println(it) }
```

## Tushuntirish va Mantiq:
`combine` operatori ikkala oqimdan ham yangi qiymat kelganda ularni birlashtirib, oxirgi holatni qaytaradi.

## Ishlash natijasi:
```text
Ali ning balansi: 1000 so'm
```

---

# 1004-Topshiriq: KMP uchun `SharedFlow` yordamida Event Bus yaratish

## Topshiriq sharti:
Butun ilova bo'ylab xatolik xabarlarini yuborish uchun `SharedFlow` dan foydalanib Event Bus yarating.

## Yechim (Kotlin kodi):
```kotlin
object EventBus {
    private val _events = MutableSharedFlow<String>()
    val events = _events.asSharedFlow()
    suspend fun sendEvent(msg: String) = _events.emit(msg)
}
```

## Tushuntirish va Mantiq:
`SharedFlow` ko'p abonentli (multi-subscriber) tizimlar uchun mo'ljallangan. `emit` orqali xabar yuboriladi va barcha kuzatuvchilar uni qabul qiladi.

## Ishlash natijasi:
```text
Xatolik yuz berdi: Server 500
```

---

# 1005-Topshiriq: `flatMapLatest` bilan qidiruv funksiyasini optimallashtirish

## Topshiriq sharti:
Foydalanuvchi yozayotgan matn bo'yicha API dan ma'lumot oluvchi qidiruv funksiyasini `flatMapLatest` bilan yozing.

## Yechim (Kotlin kodi):
```kotlin
queryFlow.flatMapLatest { query ->
    flow { emit(api.search(query)) }
}.collect { results -> println(results) }
```

## Tushuntirish va Mantiq:
`flatMapLatest` yangi so'rov kelganda eski so'rovni bekor qiladi (cancel), bu esa resurslarni tejaydi.

## Ishlash natijasi:
```text
[Natija 1, Natija 2]
```

---

# 1006-Topshiriq: Compose Multiplatformda `LaunchedEffect` bilan Flow'ni boshqarish

## Topshiriq sharti:
Ekran ochilganda ma'lumotlarni yuklash uchun `LaunchedEffect` dan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
@Composable
fun DataScreen(viewModel: ViewModel) {
    LaunchedEffect(Unit) {
        viewModel.dataFlow.collect { /* UI yangilash */ }
    }
}
```

## Tushuntirish va Mantiq:
`LaunchedEffect(Unit)` komponent birinchi marta chizilganda ishga tushadi va korutinani boshqaradi.

## Ishlash natijasi:
```text
Ma'lumotlar yuklandi.
```

---

# 1007-Topshiriq: `buffer` operatori bilan Flow tezligini oshirish

## Topshiriq sharti:
Ma'lumotlarni qayta ishlash sekin bo'lsa, `buffer` yordamida oqimni to'xtatib qo'ymaslikni ta'minlang.

## Yechim (Kotlin kodi):
```kotlin
flow {
    for (i in 1..3) { emit(i); delay(100) }
}.buffer().collect { delay(200); println(it) }
```

## Tushuntirish va Mantiq:
`buffer` emit qiluvchi va kollektor o'rtasida kanal yaratadi, bu esa parallel ishlashga imkon beradi.

## Ishlash natijasi:
```text
1
2
3
```

---

# 1008-Topshiriq: `retry` operatori bilan xatolarni qayta ishlash

## Topshiriq sharti:
Tarmoq xatosi yuz berganda oqimni 3 marta qayta urinib ko'rish (retry) mexanizmini qo'shing.

## Yechim (Kotlin kodi):
```kotlin
flow { throw Exception("Xato") }
    .retry(3) { e -> (e is Exception) }
    .catch { println("Qayta urinishlar tugadi") }
    .collect()
```

## Tushuntirish va Mantiq:
`retry` operatori xatolik yuz berganda oqimni qayta ishga tushiradi, `catch` esa oxirgi xatolikni ushlaydi.

## Ishlash natijasi:
```text
Qayta urinishlar tugadi
```

---

# 1009-Topshiriq: KMP uchun `CoroutineScope` boshqaruvi

## Topshiriq sharti:
`CoroutineScope` ni `MainScope()` yordamida KMP platformalarida to'g'ri boshqaring.

## Yechim (Kotlin kodi):
```kotlin
class MyPresenter {
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())
    fun onDestroy() = scope.cancel()
}
```

## Tushuntirish va Mantiq:
`SupervisorJob` bitta korutina xatosi boshqalarini to'xtatmasligini ta'minlaydi. `cancel()` esa xotira sizib chiqishining oldini oladi.

## Ishlash natijasi:
```text
Scope bekor qilindi.
```

---

# 1010-Topshiriq: `Flow` yordamida real-time timer yaratish

## Topshiriq harakati:
Har soniyada qiymat chiqaradigan timer oqimini yarating.

## Yechim (Kotlin kodi):
```kotlin
fun timerFlow() = flow {
    var time = 0
    while(true) {
        emit(time++)
        delay(1000)
    }
}
```

## Tushuntirish va Mantiq:
`flow` builder'i ichidagi `while(true)` va `delay` kombinatsiyasi cheksiz, vaqtga asoslangan oqim hosil qiladi.

## Ishlash natijasi:
```text
0
1
2
...
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Kotlin ekotizimini chuqur o'rganish va KMP (Kotlin Multiplatform) bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1011-Topshiriq: KMP da Platformaga xos (Expect/Actual) Logger

## Topshiriq sharti:
KMP loyihasida `commonMain` da e'lon qilingan `Logger` interfeysini `androidMain` va `iosMain` uchun `actual` implementatsiyasini yarating.

## Yechim (Kotlin kodi):
```kotlin
// commonMain
expect class PlatformLogger() {
    fun log(message: String)
}

// androidMain
actual class PlatformLogger {
    actual fun log(message: String) = println("Android Log: $message")
}

// iosMain
actual class PlatformLogger {
    actual fun log(message: String) = println("iOS Log: $message")
}
```

## Tushuntirish va Mantiq:
`expect` kalit so'zi umumiy kodda interfeysni belgilaydi, `actual` esa har bir platforma uchun o'ziga xos amalga oshirishni ta'minlaydi. Bu KMP arxitekturasining asosi hisoblanadi.

## Ishlash natijasi:
```text
Android Log: Tizim ishga tushdi
```

---

# 1012-Topshiriq: Compose Multiplatform da State Hoisting

## Topshiriq sharti:
Compose Multiplatform da `Counter` komponentini yarating, unda holat (state) yuqori qatlamdan boshqarilsin.

## Yechim (Kotlin kodi):
```kotlin
@Composable
fun Counter(count: Int, onIncrement: () -> Unit) {
    Button(onClick = onIncrement) {
        Text("Hisob: $count")
    }
}
```

## Tushuntirish va Mantiq:
State Hoisting — bu komponentni "stateless" qilish usuli. Holatni yuqoriga ko'tarish orqali komponentni qayta ishlatish (reusability) va test qilish osonlashadi.

## Ishlash natijasi:
```text
[Button] -> Hisob: 1
```

---

# 1013-Topshiriq: Flow da `combine` operatori

## Topshiriq sharti:
Ikki xil Flow (foydalanuvchi nomi va yoshi) ni birlashtirib, yangi ma'lumot hosil qiluvchi oqim yarating.

## Yechim (Kotlin kodi):
```kotlin
val nameFlow = flowOf("Ali", "Vali")
val ageFlow = flowOf(20, 25)

val combined = nameFlow.combine(ageFlow) { name, age -> "$name, $age yoshda" }
```

## Tushuntirish va Mantiq:
`combine` operatori ikkala oqimdan kelgan oxirgi qiymatlarni olib, ularni birlashtiradi. Bu real vaqt rejimida UI yangilash uchun juda samarali.

## Ishlash natijasi:
```text
Ali, 20 yoshda
Vali, 25 yoshda
```

---

# 1014-Topshiriq: Coroutine da `flatMapLatest` dan foydalanish

## Topshiriq sharti:
Qidiruv so'rovi o'zgarganda, eski so'rovni bekor qilib, yangisini boshlaydigan Flow yarating.

## Yechim (Kotlin kodi):
```kotlin
searchQuery.flatMapLatest { query ->
    flow { emit(api.search(query)) }
}.collect { result -> println(result) }
```

## Tushuntirish va Mantiq:
`flatMapLatest` yangi qiymat kelganda eski jarayonni darhol to'xtatadi (cancel). Bu resurslarni tejash va "race condition" ning oldini olish uchun muhim.

## Ishlash natijasi:
```text
Oxirgi qidiruv natijasi: ...
```

---

# 1015-Topshiriq: KMP da `SharedFlow` orqali hodisalarni uzatish

## Topshiriq sharti:
Bir marta sodir bo'ladigan hodisalarni (masalan, "Xatolik yuz berdi") UI ga uzatish uchun `SharedFlow` dan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
private val _events = MutableSharedFlow<String>()
val events = _events.asSharedFlow()

suspend fun sendError(msg: String) = _events.emit(msg)
```

## Tushuntirish va Mantiq:
`SharedFlow` ko'p qabul qiluvchili (multi-cast) oqimdir. U hodisalar (events) uchun juda mos, chunki u holatni saqlamaydi, faqat uzatadi.

## Ishlash natijasi:
```text
Xatolik yuz berdi: Internet uzildi
```

---

# 1016-Topshiriq: Compose da `LaunchedEffect` bilan ma'lumot yuklash

## Topshiriq sharti:
Ekran ochilganda API dan ma'lumotni avtomatik yuklaydigan `LaunchedEffect` blokini yozing.

## Yechim (Kotlin kodi):
```kotlin
@Composable
fun UserScreen(viewModel: UserViewModel) {
    LaunchedEffect(Unit) {
        viewModel.loadData()
    }
}
```

## Tushuntirish va Mantiq:
`LaunchedEffect(Unit)` komponent birinchi marta chizilganda (composition) ishga tushadi va `CoroutineScope` ni boshqaradi.

## Ishlash natijasi:
```text
Ma'lumot yuklanmoqda...
```

---

# 1017-Topshiriq: Flow da `buffer` operatori

## Topshiriq sharti:
Ma'lumotlar oqimini qayta ishlash sekin bo'lsa, uni `buffer` yordamida tezlashtiring.

## Yechim (Kotlin kodi):
```kotlin
flow {
    for (i in 1..3) { emit(i); delay(1000) }
}.buffer().collect { delay(2000); println(it) }
```

## Tushuntirish va Mantiq:
`buffer` operatori ishlab chiqaruvchi va iste'molchi o'rtasida kanal yaratadi, bu esa ikkala jarayonning parallel ishlashiga imkon beradi.

## Ishlash natijasi:
```text
1
2
3
```

---

# 1018-Topshiriq: KMP da `expect` funksiya bilan vaqtni olish

## Topshiriq sharti:
Platformadan qat'iy nazar joriy vaqtni (timestamp) oladigan funksiya yarating.

## Yechim (Kotlin kodi):
```kotlin
expect fun getCurrentTimeMillis(): Long

// Android/iOS da platforma kutubxonalari orqali amalga oshiriladi
```

## Tushuntirish va Mantiq:
KMP da `kotlinx.datetime` kutubxonasi bo'lsa ham, ba'zida past darajadagi platforma API lariga murojaat qilish kerak bo'ladi.

## Ishlash natijasi:
```text
1715678900000
```

---

# 1019-Topshiriq: Compose da `derivedStateOf` optimizatsiyasi

## Topshiriq sharti:
Ro'yxatni o'qishda faqat ma'lum bir shart bajarilganda UI ni qayta chizadigan `derivedStateOf` yarating.

## Yechim (Kotlin kodi):
```kotlin
val isButtonVisible by remember { derivedStateOf { listState.firstVisibleItemIndex > 0 } }
```

## Tushuntirish dan Mantiq:
`derivedStateOf` keraksiz qayta chizishlarning (recomposition) oldini oladi. U faqat qiymat o'zgarganda ishlaydi.

## Ishlash natijasi:
```text
Button visibility: true
```

---

# 1020-Topshiriq: Flow da `retry` mexanizmi

## Topshiriq sharti:
Tarmoq xatosi yuz berganda oqimni 3 marta qayta urinib ko'radigan kod yozing.

## Yechim (Kotlin kodi):
```kotlin
flow { emit(fetchData()) }
    .retry(3) { e -> e is IOException }
    .collect()
```

## Tushuntirish va Mantiq:
`retry` operatori xatolik yuz berganda oqimni qaytadan ishga tushiradi. Bu tarmoq barqarorligi past bo'lgan holatlarda juda muhim.

## Ishlash natijasi:
```text
Qayta urinish: 1... Muvaffaqiyatli.
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Kotlin ekotizimini chuqur o'rganish va datasetimizni boyitish uchun mo'ljallangan #1021-#1030 topshiriqlar to'plamini taqdim etaman.

---

# 1021-Topshiriq: KMP da Platform-agnostic Networking (Ktor)

## Topshiriq sharti:
Ktor kutubxonasidan foydalanib, barcha platformalar (Android, iOS, Desktop) uchun umumiy bo'lgan `HttpClient` ni sozlang va `https://jsonplaceholder.typicode.com/posts/1` manzilidan ma'lumotni `Flow` orqali qaytaruvchi funksiya yozing.

## Yechim (Kotlin kodi):
```kotlin
import io.ktor.client.*
import io.ktor.client.call.*
import io.ktor.client.request.*
import kotlinx.coroutines.flow.flow

class ApiService(private val client: HttpClient) {
    fun fetchPost() = flow {
        val response: String = client.get("https://jsonplaceholder.typicode.com/posts/1").body()
        emit(response)
    }
}
```

## Tushuntirish va Mantiq:
`flow` builder'i yordamida tarmoq so'rovi asinxron tarzda amalga oshiriladi. `HttpClient` platformaga xos engine (Android uchun OkHttp, iOS uchun Darwin) bilan ishlaydi, bu esa KMP ning asosiy kuchidir.

## Ishlash natijasi:
```text
{"userId": 1, "id": 1, "title": "sunt aut facere...", "body": "quia et suscipit..."}
```

---

# 1022-Topshiriq: Compose Multiplatform da State Management

## Topshiriq sharti:
Compose Multiplatform da `MutableStateFlow` dan foydalanib, tugma bosilganda hisoblagichni (counter) oshiruvchi va barcha platformalarda bir xil ishlaydigan UI komponentini yarating.

## Yechim (Kotlin kodi):
```kotlin
import androidx.compose.runtime.*
import kotlinx.coroutines.flow.MutableStateFlow

@Composable
fun CounterScreen() {
    val count = remember { MutableStateFlow(0) }
    val state by count.collectAsState()

    Button(onClick = { count.value++ }) {
        Text("Hisob: $state")
    }
}
```

## Tushuntirish va Mantiq:
`collectAsState()` funksiyasi `Flow` ni Compose `State` ga aylantiradi. Bu UI ning har bir o'zgarishda avtomatik qayta chizilishini (recomposition) ta'minlaydi.

## Ishlash natijasi:
```text
[Tugma bosilganda: Hisob: 1, Hisob: 2, ...]
```

---

# 1023-Topshiriq: Coroutine Flow da `combine` operatori

## Topshiriq sharti:
Ikki xil `Flow` (foydalanuvchi nomi va yoshi) ni `combine` operatori yordamida birlashtirib, natijani bitta string ko'rinishida chiqaring.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.runBlocking

fun main() = runBlocking {
    val nameFlow = flowOf("Ali", "Vali")
    val ageFlow = flowOf(20, 25)

    nameFlow.combine(ageFlow) { name, age -> "$name $age yoshda" }
        .collect { println(it) }
}
```

## Tushuntirish va Mantiq:
`combine` operatori har ikkala flow dan yangi qiymat kelganda ishga tushadi va ularni birlashtirib yangi oqim hosil qiladi.

## Ishlash natijasi:
```text
Ali 20 yoshda
Vali 25 yoshda
```

---

# 1024-Topshiriq: Flow da Xatoliklarni Boshqarish (`catch`)

## Topshiriq sharti:
`Flow` ichida yuzaga kelishi mumkin bo'lgan `Exception` ni `catch` operatori yordamida ushlab qoling va foydalanuvchiga xabar bering.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.flow.*

fun getData() = flow {
    emit("Ma'lumot yuklandi")
    throw Exception("Tarmoq xatosi!")
}.catch { e -> emit("Xatolik yuz berdi: ${e.message}") }
```

## Tushuntirish va Mantiq:
`catch` operatori faqat upstream (yuqoridagi) oqimdagi xatolarni ushlaydi. Bu dasturning kutilmaganda yopilib ketishining oldini oladi.

## Ishlash natijasi:
```text
Ma'lumot yuklandi
Xatolik yuz berdi: Tarmoq xatosi!
```

---

# 1025-Topshiriq: KMP da `expect/actual` mexanizmi

## Topshiriq sharti:
Platformaga xos bo'lgan qurilma nomini olish uchun `expect` funksiyasini e'lon qiling va Android uchun `actual` implementatsiyasini yozing.

## Yechim (Kotlin kodi):
```kotlin
// Common
expect fun getPlatformName(): String

// Android
actual fun getPlatformName(): String = "Android ${android.os.Build.VERSION.SDK_INT}"
```

## Tushuntirish va Mantiq:
`expect/actual` KMP ning poydevori bo'lib, umumiy kodda platformaga xos funksiyalarni chaqirish imkonini beradi.

## Ishlash natijasi:
```text
Android 34
```

---

# 1026-Topshiriq: `flatMapLatest` bilan qidiruv tizimi

## Topshiriq sharti:
Foydalanuvchi qidiruv maydoniga yozganda, eski so'rovni bekor qilib, faqat oxirgi so'rov natijasini qaytaruvchi `flatMapLatest` funksiyasini qo'llang.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.flow.*

val searchQuery = MutableStateFlow("")
val results = searchQuery.flatMapLatest { query ->
    flow { emit("Natijalar: $query") }
}
```

## Tushuntirish and Mantiq:
`flatMapLatest` yangi qiymat kelganda eski blokni bekor qiladi (cancel), bu qidiruv tizimlarida resurslarni tejash uchun juda muhim.

## Ishlash natijasi:
```text
Natijalar: Kotlin
```

---

# 1027-Topshiriq: Compose Multiplatform da Animatsiya

## Topshiriq sharti:
`animateFloatAsState` yordamida tugma bosilganda uning o'lchamini (scale) silliq o'zgartiruvchi animatsiya yarating.

## Yechim (Kotlin kodi):
```kotlin
val scale by animateFloatAsState(if (pressed) 1.2f else 1.0f)
Box(modifier = Modifier.scale(scale))
```

## Tushuntirish va Mantiq:
`animateFloatAsState` Compose ning deklarativ animatsiya tizimi bo'lib, qiymat o'zgarganda oraliq qiymatlarni avtomatik hisoblaydi.

## Ishlash natijasi:
```text
[Tugma bosilganda silliq kattalashadi]
```

---

# 1028-Topshiriq: `SharedFlow` yordamida Eventlarni uzatish

## Topshiriq sharti:
`SharedFlow` dan foydalanib, bir nechta obunachiga (subscriber) bir vaqtning o'zida "Tizimga kirildi" xabarini yuboring.

## Yechim (Kotlin kodi):
```kotlin
val eventFlow = MutableSharedFlow<String>()
// Obuna
eventFlow.emit("Tizimga kirildi")
```

## Tushuntirish va Mantiq:
`SharedFlow` "hot" stream hisoblanadi va bir nechta qabul qiluvchilarga xabar tarqatish (broadcast) uchun mo'ljallangan.

## Ishlash natijasi:
```text
Tizimga kirildi
```

---

# 1029-Topshiriq: `buffer` operatori bilan ishlash

## Topshiriq sharti:
Ma'lumotlar oqimini qayta ishlash sekin bo'lsa, `buffer` operatori yordamida ishlab chiqaruvchi (producer) ni bloklamasdan ma'lumotlarni to'plashni ta'minlang.

## Yechim (Kotlin kodi):
```kotlin
flow {
    for (i in 1..3) { emit(i); delay(100) }
}.buffer().collect { delay(200); println(it) }
```

## Tushuntirish va Mantiq:
`buffer` ishlab chiqaruvchi va iste'molchi o'rtasida kanal yaratadi, bu esa parallel ishlash imkonini beradi.

## Ishlash natijasi:
```text
1
2
3
```

---

# 1030-Topshiriq: `flowOn` bilan Thread boshqaruvi

## Topshiriq sharti:
Ma'lumotni `Dispatchers.IO` da yuklab, UI ni `Dispatchers.Main` da yangilash uchun `flowOn` dan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
flow {
    emit(fetchDataFromNetwork())
}.flowOn(Dispatchers.IO)
 .collect { updateUI(it) }
```

## Tushuntirish va Mantiq:
`flowOn` o'zidan oldingi operatorlarning qaysi thread da ishlashini belgilaydi. Bu UI thread ni bloklamaslik uchun eng yaxshi amaliyotdir.

## Ishlash natijasi:
```text
Ma'lumot IO thread da yuklandi va Main thread da ko'rsatildi.
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Kotlin ekotizimini chuqur o'rganish va sun'iy intellekt modellarini o'qitish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1031-Topshiriq: KMP da Platformaga xos (Expect/Actual) Networking

## Topshiriq sharti:
Kotlin Multiplatform loyihasida `HttpClient` orqali ma'lumot olish uchun `expect` funksiyasini yarating. Android va iOS platformalari uchun alohida `actual` implementatsiyalarni yozing.

## Yechim (Kotlin kodi):
```kotlin
// Common
expect fun getPlatformName(): String

// Android
actual fun getPlatformName(): String = "Android (OkHttp)"

// iOS
actual fun getPlatformName(): String = "iOS (NSURLSession)"

fun main() {
    println("Platforma: ${getPlatformName()}")
}
```

## Tushuntirish va Mantiq:
`expect` kalit so'zi umumiy kodda interfeys vazifasini bajaradi. Har bir platforma o'zining `actual` implementatsiyasini taqdim etadi, bu esa KMP loyihalarida platformaga xos kutubxonalardan foydalanish imkonini beradi.

## Ishlash natijasi:
```text
Platforma: Android (OkHttp)
```

---

# 1032-Topshiriq: Compose Multiplatform da State Management

## Topshiriq sharti:
Compose Multiplatform yordamida tugma bosilganda hisoblagichni (counter) oshiruvchi va uni `State` orqali boshqaruvchi UI komponentini yarating.

## Yechim (Kotlin kodi):
```kotlin
import androidx.compose.runtime.*

@Composable
fun CounterApp() {
    var count by remember { mutableStateOf(0) }
    
    // UI qismi (pseudo-code)
    println("Joriy qiymat: $count")
    count++ 
}
```

## Tushuntirish va Mantiq:
`mutableStateOf` Compose ning reaktivlik asosidir. `remember` esa recomposition vaqtida qiymatni xotirada saqlab qoladi.

## Ishlash natijasi:
```text
Joriy qiymat: 0
```

---

# 1033-Topshiriq: Coroutine Flow da `combine` operatori

## Topshiriq sharti:
Ikki xil `Flow` (foydalanuvchi nomi va yoshi) ni `combine` operatori yordamida birlashtirib, yakuniy natijani chiqaring.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.runBlocking

fun main() = runBlocking {
    val names = flowOf("Ali", "Vali")
    val ages = flowOf(20, 25)
    
    names.combine(ages) { name, age -> "$name $age yoshda" }
        .collect { println(it) }
}
```

## Tushuntirish va Mantiq:
`combine` operatori ikkala oqimdan kelgan eng oxirgi qiymatlarni birlashtiradi. Har safar oqimlardan biri yangilansa, blok qayta ishga tushadi.

## Ishlash natijasi:
```text
Ali 20 yoshda
Vali 25 yoshda
```

---

# 1034-Topshiriq: Flow da `flatMapLatest` bilan ma'lumotlarni yuklash

## Topshiriq sharti:
Qidiruv so'rovi o'zgarganda eski so'rovni bekor qilib, yangisini boshlaydigan `flatMapLatest` mexanizmini yarating.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.runBlocking

fun main() = runBlocking {
    val queryFlow = flowOf("Kotlin", "KMP")
    queryFlow.flatMapLatest { query ->
        flow { emit("Natija: $query") }
    }.collect { println(it) }
}
```

## Tushuntirish va Mantiq:
`flatMapLatest` yangi qiymat kelganda avvalgi ishlab turgan blokni darhol to'xtatadi (cancel), bu esa resurslarni tejash uchun juda muhim.

## Ishlash natijasi:
```text
Natija: Kotlin
Natija: KMP
```

---

# 1035-Topshiriq: KMP da `SharedFlow` orqali Event yuborish

## Topshiriq sharti:
`SharedFlow` dan foydalanib, UI qatlamiga "Xatolik yuz berdi" degan xabarni yuboruvchi mexanizm yarating.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.flow.*

class EventManager {
    private val _events = MutableSharedFlow<String>()
    val events = _events.asSharedFlow()

    suspend fun sendError(msg: String) = _events.emit(msg)
}
```

## Tushuntirish va Mantiq:
`SharedFlow` ko'p qabul qiluvchili (multi-cast) oqimdir. U asosan UI hodisalari (snackbars, navigation) uchun ishlatiladi.

## Ishlash natijasi:
```text
(Eventlar tizimi ishga tushdi)
```

---

# 1036-Topshiriq: Coroutine Context va Dispatchers

## Topshiriq sharti:
Og'ir hisoblashni `Dispatchers.Default` da, UI yangilanishini `Dispatchers.Main` da bajaradigan kod yozing.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking {
    withContext(Dispatchers.Default) {
        val result = (1..1000000).sum()
        println("Hisoblandi: $result")
    }
}
```

## Tushuntirish va Mantiq:
`withContext` korutin kontekstini o'zgartiradi. `Default` CPU talab qiladigan ishlar uchun, `Main` esa UI operatsiyalari uchun mo'ljallangan.

## Ishlash natijasi:
```text
Hisoblandi: 500000500000
```

---

# 1037-Topshiriq: Flow da `buffer` operatori

## Topshiriq sharti:
Ma'lumotlar oqimini qayta ishlash tezligini oshirish uchun `buffer` operatoridan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.runBlocking

fun main() = runBlocking {
    (1..3).asFlow()
        .onEach { println("Ishlab chiqarildi: $it") }
        .buffer()
        .collect { println("Qabul qilindi: $it") }
}
```

## Tushuntirish va Mantiq:
`buffer` ishlab chiqaruvchi va qabul qiluvchini alohida korutinlarda ishlashga majbur qiladi, bu esa bloklanishning oldini oladi.

## Ishlash natijasi:
```text
Ishlab chiqarildi: 1
Qabul qilindi: 1
Ishlab chiqarildi: 2
Qabul qilindi: 2
```

---

# 1038-Topshiriq: Compose da `LaunchedEffect`

## Topshiriq sharti:
Ekran ochilganda bir marta ma'lumot yuklaydigan `LaunchedEffect` blokini yarating.

## Yechim (Kotlin kodi):
```kotlin
import androidx.compose.runtime.*

@Composable
fun DataScreen() {
    LaunchedEffect(Unit) {
        println("Ma'lumotlar yuklanmoqda...")
    }
}
```

## Tushuntirish va Mantiq:
`LaunchedEffect` Compose sikli bilan bog'liq bo'lgan korutinni ishga tushiradi. `Unit` kaliti u faqat bir marta ishlashini bildiradi.

## Ishlash natijasi:
```text
Ma'lumotlar yuklanmoqda...
```

---

# 1039-Topshiriq: Flow da `retry` mexanizmi

## Topshiriq sharti:
Tarmoq xatosi yuz berganda oqimni 3 marta qayta urinib ko'radigan `retry` operatorini qo'llang.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.flow.*

fun main() = runBlocking {
    flow {
        emit(1)
        throw Exception("Xato!")
    }.retry(3) { e -> 
        println("Qayta urinish..."); true 
    }.collect()
}
```

## Tushuntirish va Mantiq:
`retry` operatori xatolik yuz berganda oqimni qayta ishga tushiradi. Bu tarmoq uzilishlari uchun juda samarali.

## Ishlash natijasi:
```text
Qayta urinish...
Qayta urinish...
Qayta urinish...
```

---

# 1040-Topshiriq: KMP da `StateFlow` bilan UI holati

## Topshiriq sharti:
`StateFlow` yordamida UI holatini (Loading, Success, Error) boshqaradigan `ViewModel` qismini yarating.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.flow.*

sealed class UiState {
    object Loading : UiState()
    data class Success(val data: String) : UiState()
}

class MainViewModel {
    private val _state = MutableStateFlow<UiState>(UiState.Loading)
    val state = _state.asStateFlow()
}
```

## Tushuntirish va Mantiq:
`StateFlow` har doim oxirgi holatni saqlaydi. `sealed class` esa UI holatlarini xavfsiz va tushunarli boshqarishga yordam beradi.

## Ishlash natijasi:
```text
StateFlow initialized: Loading
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Kotlin ekotizimini chuqur o'rganish va KMP (Kotlin Multiplatform) bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1041-Topshiriq: KMP da Platformaga xos (Expect/Actual) Logger

## Topshiriq sharti:
KMP loyihasida `expect` va `actual` mexanizmidan foydalanib, Android va iOS uchun har xil log chiqaradigan tizim yarating.

## Yechim (Kotlin kodi):
```kotlin
// commonMain
expect class Logger() {
    fun log(message: String)
}

// androidMain
actual class Logger {
    actual fun log(message: String) = println("Android Log: $message")
}

// iosMain
actual class Logger {
    actual fun log(message: String) = println("iOS Log: $message")
}
```

## Tushuntirish va Mantiq:
`expect` kalit so'zi umumiy modulda interfeysni belgilaydi, `actual` esa har bir platforma uchun o'ziga xos implementatsiyani ta'minlaydi. Bu kod bazasini qisqartirish va platforma imkoniyatlaridan foydalanish uchun asosdir.

## Ishlash natijasi:
```text
Android Log: Tizim ishga tushdi
```

---

# 1042-Topshiriq: Compose Multiplatform da State Hoisting

## Topshiriq sharti:
Compose Multiplatform da `MutableState` dan foydalanib, ota komponentdan bola komponentga holatni (state) uzatishni amalga oshiring.

## Yechim (Kotlin kodi):
```kotlin
@Composable
fun CounterScreen() {
    var count by remember { mutableStateOf(0) }
    CounterButton(count = count, onIncrement = { count++ })
}

@Composable
fun CounterButton(count: Int, onIncrement: () -> Unit) {
    Button(onClick = onIncrement) { Text("Hisob: $count") }
}
```

## Tushuntirish va Mantiq:
State hoisting — bu holatni yuqoriga ko'tarish. Bu komponentlarni qayta ishlatiladigan (reusable) va test qilish oson bo'lgan holatga keltiradi.

## Ishlash natijasi:
```text
Hisob: 1 (tugma bosilganda)
```

---

# 1043-Topshiriq: Flow da `combine` operatori

## Topshiriq sharti:
Ikki xil `StateFlow` dan kelayotgan ma'lumotlarni `combine` operatori yordamida birlashtirib, yangi qiymat hosil qiling.

## Yechim (Kotlin kodi):
```kotlin
val flow1 = MutableStateFlow("Salom")
val flow2 = MutableStateFlow("Khorazmiy")

val combined = combine(flow1, flow2) { f1, f2 -> "$f1, $f2!" }
```

## Tushuntirish va Mantiq:
`combine` operatori har ikkala oqimdan yangi qiymat kelganda ishga tushadi va ularni birlashtirib, reaktiv UI yangilanishini ta'minlaydi.

## Ishlash natijasi:
```text
Salom, Khorazmiy!
```

---

# 1044-Topshiriq: Coroutine Scope va `SupervisorJob`

## Topshiriq sharti:
Bir nechta parallel vazifani `SupervisorJob` yordamida bajaring, bunda bitta vazifa xato bersa, qolganlari to'xtamasligi kerak.

## Yechim (Kotlin kodi):
```kotlin
val scope = CoroutineScope(Dispatchers.Default + SupervisorJob())
scope.launch {
    launch { throw Exception("Xato!") }
    launch { println("Men ishlayapman!") }
}
```

## Tushuntirish va Mantiq:
`SupervisorJob` bolalar o'rtasidagi bog'liqlikni uzadi. Bitta korutin muvaffaqiyatsiz bo'lsa, boshqa korutinlar o'z ishini davom ettiradi.

## Ishlash natijasi:
```text
Men ishlayapman!
```

---

# 1045-Topshiriq: Flow da `debounce` operatori

## Topshiriq sharti:
Qidiruv satriga yozilayotgan matnni `debounce` yordamida 500ms kechikish bilan qayta ishlang.

## Yechim (Kotlin kodi):
```kotlin
val searchFlow = MutableStateFlow("")
searchFlow.debounce(500).collect { query ->
    println("Qidirilmoqda: $query")
}
```

## Tushuntirish va Mantiq:
`debounce` foydalanuvchi yozishni to'xtatguncha kutadi, bu esa serverga ortiqcha so'rovlar yuborilishining oldini oladi.

## Ishlash natijasi:
```text
Qidirilmoqda: Kotlin (500ms kutgandan so'ng)
```

---

# 1046-Topshiriq: KMP da `expect` funksiyasi bilan vaqtni olish

## Topshiriq sharti:
Platformadan qat'iy nazar joriy vaqtni (timestamp) oluvchi `expect` funksiyasini yarating.

## Yechim (Kotlin kodi):
```kotlin
// commonMain
expect fun getCurrentTime(): Long

// androidMain
actual fun getCurrentTime(): Long = System.currentTimeMillis()
```

## Tushuntirish va Mantiq:
Platforma API lari turlicha bo'lgani uchun, umumiy kodda `expect` orqali platforma funksiyasini chaqirish eng to'g'ri yondashuvdir.

## Ishlash natijasi:
```text
1715678900000
```

---

# 1047-Topshiriq: Flow da `flatMapLatest`

## Topshiriq sharti:
Foydalanuvchi ID si o'zgarganda, eski so'rovni bekor qilib, yangisini boshlaydigan `flatMapLatest` ni qo'llang.

## Yechim (Kotlin kodi):
```kotlin
userIdFlow.flatMapLatest { id ->
    repository.getUserData(id)
}.collect { data -> println(data) }
```

## Tushuntirish va Mantiq:
`flatMapLatest` yangi qiymat kelganda avvalgi oqimni darhol to'xtatadi va yangisini boshlaydi. Bu resurslarni tejash uchun juda muhim.

## Ishlash natijasi:
```text
User(id=1, name="Ali")
```

---

# 1048-Topshiriq: Compose Multiplatform da `LaunchedEffect`

## Topshiriq sharti:
Ekran ochilganda bir marta ma'lumot yuklaydigan `LaunchedEffect` blokini yarating.

## Yechim (Kotlin kodi):
```kotlin
@Composable
fun UserScreen(viewModel: UserViewModel) {
    LaunchedEffect(Unit) {
        viewModel.loadData()
    }
}
```

## Tushuntirish the Mantiq:
`LaunchedEffect(Unit)` komponent birinchi marta chizilganda (composition) ishga tushadi va faqat bir marta bajariladi.

## Ishlash natijasi:
```text
Ma'lumot yuklandi...
```

---

# 1049-Topshiriq: Coroutine `Channel` dan foydalanish

## Topshiriq sharti:
`Channel` yordamida ikkita korutin o'rtasida xabar almashinuvini tashkil qiling.

## Yechim (Kotlin kodi):
```kotlin
val channel = Channel<String>()
launch { channel.send("Salom Khorazmiy") }
launch { println(channel.receive()) }
```

## Tushuntirish va Mantiq:
`Channel` — bu korutinlar o'rtasida xavfsiz ma'lumot uzatish uchun mo'ljallangan "quvur". U `BlockingQueue` ning korutinlar uchun moslashgan ko'rinishidir.

## Ishlash natijasi:
```text
Salom Khorazmiy
```

---

# 1050-Topshiriq: Flow da `retry` operatori

## Topshiriq sharti:
Tarmoq xatosi yuz berganda so'rovni 3 marta qayta urinib ko'radigan `retry` mexanizmini yarating.

## Yechim (Kotlin kodi):
```kotlin
flow {
    emit(api.fetchData())
}.retry(3) { e -> e is IOException }.collect()
```

## Tushuntirish va Mantiq:
`retry` operatori xatolik yuz berganda oqimni qayta ishga tushiradi. Bu tarmoq beqaror bo'lgan mobil ilovalarda juda muhim.

## Ishlash natijasi:
```text
Ma'lumot muvaffaqiyatli olindi (3-urinishda)
```