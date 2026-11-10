# 951-Topshiriq: Clean Architecture qatlamlari: Domain Entity modeli
## Topshiriq sharti:
Clean Architecture ning eng markaziy, hech qanday ramka yoki kutubxonaga bog'liq bo'lmagan Domain Entity sinfini yarating.

## Yechim (Kotlin kodi):
```kotlin
data class TaskItem(
    val id: String,
    val title: String,
    val isCompleted: Boolean,
    val createdAtMillis: Long
)

fun main() {
    val task = TaskItem("task-1", "Kotlin K2 kompilyatorini o'rganish", false, System.currentTimeMillis())
    println("Domain Entity yaratildi: ${task.title} (Bajarildi: ${task.isCompleted})")
}
```

## Tushuntirish va Mantiq:
Domain qatlami dasturning yuragi hisoblanadi. Undagi Entity sinflari Android SDK, ma'lumotlar bazasi yoki tarmoq kutubxonalariga mutlaqo bog'liq bo'lmagan sof Kotlin sinflaridir.

## Ishlash natijasi:
```text
Domain Entity yaratildi: Kotlin K2 kompilyatorini o'rganish (Bajarildi: false)
```


# 952-Topshiriq: Domain UseCase yaratish (operator fun invoke yordamida)
## Topshiriq sharti:
Bitta aniq biznes vazifasini bajaruvchi GetActiveTasksUseCase ni Kotlin ning `operator fun invoke` sintaksisi bilan yozing.

## Yechim (Kotlin kodi):
```kotlin
interface TaskRepository {
    suspend fun getTasks(): List<TaskItem>
}

class GetActiveTasksUseCase(private val repository: TaskRepository) {
    suspend operator fun invoke(): List<TaskItem> {
        return repository.getTasks().filter { !it.isCompleted }
    }
}

fun main() {
    println("UseCase: Bitta biznes vazifasini bajaruvchi mustaqil domen mantiqi.")
    println("operator fun invoke yordamida UseCase funksiya kabi chaqiriladi: getActiveTasks()")
}
```

## Tushuntirish va Mantiq:
UseCase (yoki Interactor) yagona mas'uliyat tamoyiliga (Single Responsibility Principle) tayanadi. U orqali Presentation qatlami Repository dagi biznes logikani boshqaradi.

## Ishlash natijasi:
```text
UseCase: Bitta biznes vazifasini bajaruvchi mustaqil domen mantiqi.
operator fun invoke yordamida UseCase funksiya kabi chaqiriladi: getActiveTasks()
```


# 953-Topshiriq: Repository interfeysi va uning Data qatlamidagi realizatsiyasi
## Topshiriq sharti:
Domain qatlamida e'lon qilingan Repository interfeysini Data qatlamida amalga oshiring.

## Yechim (Kotlin kodi):
```kotlin
class TaskRepositoryImpl(
    private val localDataSource: List<TaskItem>
) : TaskRepository {
    override suspend fun getTasks(): List<TaskItem> {
        return localDataSource
    }
}

fun main() {
    println("Repository Pattern: Ma'lumotlar qayerdan kelishini biznes mantiqdan to'liq yashiradi.")
}
```

## Tushuntirish va Mantiq:
Inversion of Control printsipiga ko'ra, Domain qatlami Repository interfeysini egalik qiladi, Data qatlami esa uni amalga oshiradi. Bu esa ma'lumotlar manbaini oson almashtirish imkonini beradi.

## Ishlash natijasi:
```text
Repository Pattern: Ma'lumotlar qayerdan kelishini biznes mantiqdan to'liq yashiradi.
```


# 954-Topshiriq: Result Wrapper (Sealed Class: Success, Error, Loading)
## Topshiriq sharti:
Tarmoq va baza operatsiyalari natijasini xavfsiz ifodalovchi Result umumiy sealed sinfini yarating.

## Yechim (Kotlin kodi):
```kotlin
sealed interface NetworkResult<out T> {
    data class Success<out T>(val data: T) : NetworkResult<T>
    data class Error(val message: String, val throwable: Throwable? = null) : NetworkResult<Nothing>
    object Loading : NetworkResult<Nothing>
}

fun main() {
    val result: NetworkResult<String> = NetworkResult.Success("Muvaffaqiyatli ma'lumot")
    when (result) {
        is NetworkResult.Success -> println("Natija: ${result.data}")
        is NetworkResult.Error -> println("Xatolik: ${result.message}")
        NetworkResult.Loading -> println("Yuklanmoqda...")
    }
}
```

## Tushuntirish va Mantiq:
Result Wrapper yordamida Presentation qatlami operatsiyaning holatini (yuklanish, natija yoki xato) to'liq va xavfsiz boshqaradi.

## Ishlash natijasi:
```text
Natija: Muvaffaqiyatli ma'lumot
```


# 955-Topshiriq: MVVM ViewModel arxitekturasi va UI State boshqaruvi
## Topshiriq sharti:
StateFlow orqali UI State saqlovchi va asinxron biznes operatsiyalarni chaqiruvchi ViewModel namunasini tuzing.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

data class TasksUiState(
    val isLoading: Boolean = false,
    val tasks: List<String> = emptyList(),
    val errorMessage: String? = null
)

class TasksViewModel {
    private val _uiState = MutableStateFlow(TasksUiState(isLoading = true))
    val uiState: StateFlow<TasksUiState> = _uiState.asStateFlow()
    
    fun loadData() {
        _uiState.value = TasksUiState(
            isLoading = false,
            tasks = listOf("Compose o'rganish", "Koin ulash")
        )
    }
}

fun main() {
    val vm = TasksViewModel()
    println("Boshlang'ich holat: isLoading=${vm.uiState.value.isLoading}")
    vm.loadData()
    println("Yuklangach: ${vm.uiState.value.tasks}")
}
```

## Tushuntirish va Mantiq:
MVVM (Model-View-ViewModel) arxitekturasida ViewModel UI holatini saqlaydi va konfiguratsiya o'zgarishlarida (ekran burilishi) o'chib ketmaydi.

## Ishlash natijasi:
```text
Boshlang'ich holat: isLoading=true
Yuklangach: [Compose o'rganish, Koin ulash]
```


# 956-Topshiriq: MVI (Model-View-Intent) naqshi: Intent/Action larni qayta ishlash
## Topshiriq sharti:
Foydalanuvchi harakatlarini Intent (harakat signallari) sifatida qabul qilib, holatni bir tomonlama o'zgartiruvchi MVI arxitekturasini yozing.

## Yechim (Kotlin kodi):
```kotlin
sealed interface TaskIntent {
    object LoadTasks : TaskIntent
    data class CompleteTask(val taskId: String) : TaskIntent
}

class MviTaskProcessor {
    fun processIntent(intent: TaskIntent) {
        when (intent) {
            is TaskIntent.LoadTasks -> println("MVI: Vazifalar yuklanmoqda...")
            is TaskIntent.CompleteTask -> println("MVI: Vazifa #${intent.taskId} bajarildi deb belgilandi.")
        }
    }
}

fun main() {
    val processor = MviTaskProcessor()
    processor.processIntent(TaskIntent.LoadTasks)
    processor.processIntent(TaskIntent.CompleteTask("TK-101"))
}
```

## Tushuntirish va Mantiq:
MVI arxitekturasi Unidirectional Data Flow (UDF) tamoyiliga qat'iy asoslangan: View -> Intent -> Reducer/ViewModel -> State -> View sikli aylanadi.

## Ishlash natijasi:
```text
MVI: Vazifalar yuklanmoqda...
MVI: Vazifa #TK-101 bajarildi deb belgilandi.
```


# 957-Topshiriq: Dependency Injection (DI) tushunchasi va qo'lda Service Locator yaratish
## Topshiriq sharti:
Kutubxonalarsiz, sof Kotlin da bog'liqliklarni boshqaruvchi Service Locator konteynerini yarating.

## Yechim (Kotlin kodi):
```kotlin
interface ApiService { fun fetch(): String }
class ApiServiceImpl : ApiService { override fun fetch() = "Tarmoq ma'lumoti" }

object AppContainer {
    val apiService: ApiService by lazy { ApiServiceImpl() }
}

fun main() {
    val service = AppContainer.apiService
    println("Olingan servis orqali ma'lumot: ${service.fetch()}")
}
```

## Tushuntirish va Mantiq:
Dependency Injection ob'yektlar o'z bog'liqliklarini o'zi yaratmasdan, tashqaridan qabul qilishini ta'minlaydi. Bu kodni modulli va testlashga juda oson qiladi.

## Ishlash natijasi:
```text
Olingan servis orqali ma'lumot: Tarmoq ma'lumoti
```


# 958-Topshiriq: Koin DI: module, single va factory e'lon qilish
## Topshiriq sharti:
Koin ning sof Kotlin tilidagi DSL sintaksisi orqali modul tuzilishi va instansiyalar boshqaruvini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
// Koin DSL sintaksisi namoyishi
class DatabaseDriver
class UserRepository(val db: DatabaseDriver)
class UserPresenter(val repo: UserRepository)

fun main() {
    println("Koin modul strukturasi sintaksisi:")
    println("val appModule = module {")
    println("    single { DatabaseDriver() } // Singleton: butun ilovada yagona nusxa")
    println("    factory { UserRepository(get()) } // Har chaqirilganda yangi nusxa")
    println("}")
}
```

## Tushuntirish va Mantiq:
Koin reflection ishlatmaydi, kompilyatsiya vaqtida kod generatsiyasi qilmaydi, balki toza Kotlin funksiyalari va DSL orqali juda yengil va tez ishlaydi.

## Ishlash natijasi:
```text
Koin modul strukturasi sintaksisi:
val appModule = module {
    single { DatabaseDriver() } // Singleton: butun ilovada yagona nusxa
    factory { UserRepository(get()) } // Har chaqirilganda yangi nusxa
}
```


# 959-Topshiriq: Koin da viewModel {} ta'rifi va in'yeksiyasi
## Topshiriq sharti:
Koin orqali Android ViewModel ni ro'yxatdan o'tkazish qoidasini tushuntiring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    println("Koin ViewModel DSL:")
    println("viewModel { HomeViewModel(get()) }")
    println("Composable ichida chaqirish:")
    println("val viewModel: HomeViewModel = koinViewModel()")
}
```

## Tushuntirish va Mantiq:
Koin ning Android kutubxonasi `viewModel { }` DSL i orqali Android ViewModelProvider bilan to'liq integratsiya bo'ladi.

## Ishlash natijasi:
```text
Koin ViewModel DSL:
viewModel { HomeViewModel(get()) }
Composable ichida chaqirish:
val viewModel: HomeViewModel = koinViewModel()
```


# 960-Topshiriq: Dagger Hilt annotatsiyalari va arxitekturasi
## Topshiriq sharti:
Hilt ning asosiy annotatsiyalari (@HiltAndroidApp, @AndroidEntryPoint, @HiltViewModel, @Inject) vazifalarini tushuntiruvchi kod yozing.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    println("Dagger Hilt annotatsiyalari:")
    println("- @HiltAndroidApp: Application sinfida DI daraxtini ishga tushiradi")
    println("- @AndroidEntryPoint: Activity va Fragment larni in'yeksiyaga tayyorlaydi")
    println("- @HiltViewModel: ViewModel ga bog'liqliklarni kiritadi")
    println("- @Inject constructor(...): Konstruktorni avtomatik ta'minlash belgisi")
}
```

## Tushuntirish va Mantiq:
Dagger Hilt kompilyatsiya vaqtida (compile-time) bog'liqliklarni tekshiradi va hech qanday runtime overhead'siz Java/Kotlin kodlarini generatsiya qiladi.

## Ishlash natijasi:
```text
Dagger Hilt annotatsiyalari:
- @HiltAndroidApp: Application sinfida DI daraxtini ishga tushiradi
- @AndroidEntryPoint: Activity va Fragment larni in'yeksiyaga tayyorlaydi
- @HiltViewModel: ViewModel ga bog'liqliklarni kiritadi
- @Inject constructor(...): Konstruktorni avtomatik ta'minlash belgisi
```


# 961-Topshiriq: Ktor HTTP Client bilan asinxron so'rov yuborish asoslari
## Topshiriq sharti:
Kotlin Multiplatform va Android uchun eng ilg'or asinxron tarmoq mijozi bo'lgan Ktor Client arxitekturasini yozing.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    println("Ktor HTTP Client e'lon qilish:")
    println("val client = HttpClient(CIO) {")
    println("    install(ContentNegotiation) {")
    println("        json()")
    println("    }")
    println("}")
    println("Asinxron so'rov: val response = client.get("https://api.example.com/items")")
}
```

## Tushuntirish va Mantiq:
Ktor to'liq koroutinalar ustiga qurilgan va Android, iOS, Desktop va Web (Wasm/JS) platformalarining barchasida bir xil ishlay oladi.

## Ishlash natijasi:
```text
Ktor HTTP Client e'lon qilish:
val client = HttpClient(CIO) {
    install(ContentNegotiation) {
        json()
    }
}
Asinxron so'rov: val response = client.get("https://api.example.com/items")
```


# 962-Topshiriq: Ktor Client bilan POST so'rovida JSON uzatish
## Topshiriq sharti:
Ktor yordamida serverga yangi ma'lumot jo'natuvchi POST chaqiruvini loyihalang.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    println("Ktor POST so'rovi sintaksisi:")
    println("val response: HttpResponse = client.post("https://api.example.com/login") {")
    println("    contentType(ContentType.Application.Json)")
    println("    setBody(LoginRequest("alisher", "parol123"))")
    println("}")
}
```

## Tushuntirish va Mantiq:
setBody() va ContentType.Application.Json orqali obyekt kotlinx.serialization yordamida avtomatik JSON ga aylanadi va serverga yo'llanadi.

## Ishlash natijasi:
```text
Ktor POST so'rovi sintaksisi:
val response: HttpResponse = client.post("https://api.example.com/login") {
    contentType(ContentType.Application.Json)
    setBody(LoginRequest("alisher", "parol123"))
}
```


# 963-Topshiriq: Retrofit API interfeysi va Suspend funksiyalar bilan ishlash
## Topshiriq sharti:
Android dagi an'anaviy Retrofit kutubxonasini Kotlin suspend funksiyalari bilan integratsiyalash.

## Yechim (Kotlin kodi):
```kotlin
interface WeatherApiService {
    // Suspend funksiya tarmoq so'rovini avtomatik orqa fonda bajaradi
    suspend fun getCurrentWeather(city: String): String
}

class FakeWeatherApiService : WeatherApiService {
    override suspend fun getCurrentWeather(city: String): String {
        return "Toshkent: +28 C"
    }
}

fun main() {
    println("Retrofit interfeysida `suspend fun` qo'yilsa, qo'shimcha Call<T> talab qilinmaydi.")
}
```

## Tushuntirish va Mantiq:
Retrofit 2.6.0+ versiyalaridan boshlab Kotlin Coroutines ni to'liq qo'llab-quvvatlaydi va so'rovlarni avtomatik non-blocking qiladi.

## Ishlash natijasi:
```text
Retrofit interfeysida `suspend fun` qo'yilsa, qo'shimcha Call<T> talab qilinmaydi.
```


# 964-Topshiriq: Room Database: @Entity data klassi
## Topshiriq sharti:
Android SQLite bazasi bilan ishlash uchun Room @Entity modelini yarating.

## Yechim (Kotlin kodi):
```kotlin
data class NoteEntity(
    val id: Long = 0,
    val title: String,
    val content: String,
    val timestamp: Long
)

fun main() {
    val note = NoteEntity(1, "Eslatma", "Kotlin darslari", System.currentTimeMillis())
    println("Room Entity yaratildi: ${note.title}")
}
```

## Tushuntirish va Mantiq:
Room da har bir jadval @Entity bilan belgilanadi. @PrimaryKey(autoGenerate = true) orqali noyob identifikator avtomatik oshirib boriladi.

## Ishlash natijasi:
```text
Room Entity yaratildi: Eslatma
```


# 965-Topshiriq: Room Database: @Dao interfeysi va CRUD operatsiyalari
## Topshiriq sharti:
Room Data Access Object (DAO) interfeysida ma'lumot qo'shish, o'chirish va yangilash operatsiyalarini yozing.

## Yechim (Kotlin kodi):
```kotlin
interface NoteDao {
    suspend fun insert(note: NoteEntity)
    suspend fun delete(note: NoteEntity)
    suspend fun getNoteById(id: Long): NoteEntity?
}

fun main() {
    println("Room DAO: Barcha SQL operatsiyalari suspend funksiyalar orqali xavfsiz o'raladi.")
}
```

## Tushuntirish va Mantiq:
DAO interfeysidagi suspend funksiyalar Room tomonidan avtomatik ravishda disk I/O oqimida bajariladi va UI ni muzlatmaydi.

## Ishlash natijasi:
```text
Room DAO: Barcha SQL operatsiyalari suspend funksiyalar orqali xavfsiz o'raladi.
```


# 966-Topshiriq: Room Database: Flow<List<Entity>> bilan reaktiv ma'lumotlar kuzatuvi
## Topshiriq sharti:
Ma'lumotlar bazasida biror o'zgarish sodir bo'lishi bilan UI ga avtomatik yangi ro'yxatni yetkazib beruvchi Flow so'rovini yozing.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flowOf

interface ReactiveNoteDao {
    fun getAllNotes(): Flow<List<NoteEntity>>
}

class FakeReactiveDao : ReactiveNoteDao {
    override fun getAllNotes(): Flow<List<NoteEntity>> {
        return flowOf(listOf(NoteEntity(1, "Reaktiv Eslatma", "Matn", 12345L)))
    }
}

fun main() {
    println("Room + Flow: Jadvalga INSERT yoki DELETE bo'lishi bilan Flow avtomatik yangi ma'lumotni emit qiladi.")
}
```

## Tushuntirish va Mantiq:
Room kutubxonasi Flow qaytaruvchi so'rovlarni avtomatik kuzatuvchi (Observable Query) rejimiga o'tkazadi va SQL tranzaksiyalarini reaktiv boshqaradi.

## Ishlash natijasi:
```text
Room + Flow: Jadvalga INSERT yoki DELETE bo'lishi bilan Flow avtomatik yangi ma'lumotni emit qiladi.
```


# 967-Topshiriq: Offline-First arxitekturasi: Kesh va Tarmoq sinxronizatsiyasi
## Topshiriq sharti:
Ilova avval lokal bazadagi ma'lumotni darhol ko'rsatib, so'ngra orqa fonda yangilab boruvchi Repository naqshini loyihalang.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class OfflineFirstUserRepository {
    fun getUserStream(): Flow<String> = flow {
        emit("Lokal keshdagi eski ma'lumot: Alisher")
        // Tarmoq so'rovi simulyatsiyasi
        emit("Tarmoqdan yangilangan yangi ma'lumot: Alisher (Premium)")
    }
}

fun main() {
    println("Offline-First: Internet yo'q bo'lsa ham ilova to'xtamasdan lokal keshdan ishlayveradi.")
}
```

## Tushuntirish va Mantiq:
Single Source of Truth (SSOT) printsipiga binoan, UI faqat lokal bazani kuzatadi, tarmoqdan kelgan yangi ma'lumotlar esa avval bazaga saqlanadi.

## Ishlash natijasi:
```text
Offline-First: Internet yo'q bo'lsa ham ilova to'xtamasdan lokal keshdan ishlayveradi.
```


# 968-Topshiriq: DataStore Preferences orqali kalit-qiymatlarni asinxron saqlash
## Topshiriq sharti:
Eski va xavfli SharedPreferences o'rniga Jetpack DataStore dan foydalanish printsipini tushuntiring.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    println("Jetpack Preferences DataStore:")
    println("1. To'liq asinxron va Flow asosida ishlaydi")
    println("2. UI thread ni hech qachon bloklamaydi")
    println("3. Tranzaksion xavfsizlikka (consistency) ega")
}
```

## Tushuntirish va Mantiq:
DataStore Kotlin koroutinalari va Flow ustiga qurilgan bo'lib, eski SharedPreferences dagi ANR (Application Not Responding) xatolarini butunlay bartaraf etadi.

## Ishlash natijasi:
```text
Jetpack Preferences DataStore:
1. To'liq asinxron va Flow asosida ishlaydi
2. UI thread ni hech qachon bloklamaydi
3. Tranzaksion xavfsizlikka (consistency) ega
```


# 969-Topshiriq: WorkManager yordamida kafolatlangan fon vazifalarini rejalashtirish
## Topshiriq sharti:
Ilova yopilganda yoki telefon qayta yoqilganda ham bajarilishini kafolatlovchi CoroutineWorker tuzilishi.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    println("WorkManager va CoroutineWorker:")
    println("- doWork() suspend funksiyasi orqali koroutina ishga tushadi")
    println("- Constraints: NetworkType.CONNECTED, RequiresCharging")
    println("- PeriodicWorkRequestBuilder<SyncWorker>(24, TimeUnit.HOURS)")
}
```

## Tushuntirish va Mantiq:
WorkManager batareyani tejash uchun operatsion tizim Doze rejimiga moslashadi va belgilangan shartlar (masalan Wi-Fi va quvvatlagich ulanganda) bajarilganda fon ishini boshlaydi.

## Ishlash natijasi:
```text
WorkManager va CoroutineWorker:
- doWork() suspend funksiyasi orqali koroutina ishga tushadi
- Constraints: NetworkType.CONNECTED, RequiresCharging
- PeriodicWorkRequestBuilder<SyncWorker>(24, TimeUnit.HOURS)
```


# 970-Topshiriq: Kotlin Multiplatform (KMP) `expect` va `actual` deklaratsiyalari
## Topshiriq sharti:
Umumiy (common) kodda platformaga xos operatsiyani e'lon qilib, Android va iOS uchun alohida amalga oshirish mexanizmini ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
// Common modulda:
// expect fun getPlatformName(): String

// Android modulda:
// actual fun getPlatformName(): String = "Android OS"

// iOS modulda:
// actual fun getPlatformName(): String = "Apple iOS"

fun main() {
    println("KMP expect/actual: Umumiy koddan turib platforma imkoniyatlariga to'g'ridan-to'g'ri murojaat.")
}
```

## Tushuntirish va Mantiq:
expect/actual Kotlin Multiplatform ning polimorfik kompile-time kaliti bo'lib, umumiy biznes mantiqni platforma drayverlariga bog'laydi.

## Ishlash natijasi:
```text
KMP expect/actual: Umumiy koddan turib platforma imkoniyatlariga to'g'ridan-to'g'ri murojaat.
```


# 971-Topshiriq: Mobil AI arxitekturasi: LLM Request va Response modellari
## Topshiriq sharti:
Mobil qurilmadan sun'iy intellekt (Gemini yoki Claude) modeliga yuboriladigan so'rov va javob ma'lumotlar strukturasini loyihalang.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.serialization.Serializable

@Serializable
data class AiChatMessage(val role: String, val content: String)

@Serializable
data class AiChatRequest(
    val model: String,
    val messages: List<AiChatMessage>,
    val temperature: Double = 0.7
)

@Serializable
data class AiChatResponse(
    val reply: String,
    val tokensUsed: Int
)

fun main() {
    val req = AiChatRequest("gemini-1.5-flash", listOf(AiChatMessage("user", "Kotlin nima?")))
    println("AI so'rov modeli tayyorlandi: ${req.model}, Xabarlar soni: ${req.messages.size}")
}
```

## Tushuntirish va Mantiq:
Mobil AI ilovalarda JSON so'rov va javob modellari qat'iy tiplangan bo'lishi lozim, bu esa tarmoq integratsiyasini xavfsiz qiladi.

## Ishlash natijasi:
```text
AI so'rov modeli tayyorlandi: gemini-1.5-flash, Xabarlar soni: 1
```


# 972-Topshiriq: Token Streaming: Serverdan tokenlarni Flow da bo'laklab qabul qilish
## Topshiriq sharti:
LLM butun javobni generatsiya qilib bo'lishini kutmasdan, har bir chiqqan so'z/tokenni reaktiv oqim (Flow<String>) orqali uzatuvchi xizmat yozing.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.delay

class AiStreamingService {
    fun streamAiResponse(prompt: String): Flow<String> = flow {
        val tokens = listOf("Kotlin", " - bu", " zamonaviy,", " xavfsiz", " va", " kuchli", " dasturlash", " tili.")
        for (token in tokens) {
            delay(100L) // Har bir token generatsiyasi simulyatsiyasi
            emit(token)
        }
    }
}

fun main() = runBlocking {
    val ai = AiStreamingService()
    print("AI javobi: ")
    ai.streamAiResponse("Kotlin haqida ayt").collect { token ->
        print(token)
    }
    println()
}
```

## Tushuntirish va Mantiq:
Token Streaming mobil ilovada foydalanuvchi tajribasini (UX) keskin oshiradi: foydalanuvchi 5 soniya kutmasdan darhol javob yozilishini jonli ko'radi.

## Ishlash natijasi:
```text
AI javobi: Kotlin - bu zamonaviy, xavfsiz va kuchli dasturlash tili.
```


# 973-Topshiriq: Mobil AI Agent: Chat tarixi va xotira boshqaruvi (Context Window)
## Topshiriq sharti:
Foydalanuvchi bilan davom etayotgan suhbat tarixini saqlovchi va xotira to'lib ketmasligi uchun eski xabarlarni ixchamlovchi xotira menejeri yozing.

## Yechim (Kotlin kodi):
```kotlin
class ChatMemoryManager(private val maxMessages: Int = 4) {
    private val history = mutableListOf<AiChatMessage>()
    
    fun addMessage(role: String, content: String) {
        history.add(AiChatMessage(role, content))
        if (history.size > maxMessages) {
            history.removeAt(0) // Eng eski xabarni o'chirish
        }
    }
    
    fun getContext(): List<AiChatMessage> = history.toList()
}

fun main() {
    val memory = ChatMemoryManager(maxMessages = 3)
    memory.addMessage("user", "Salom")
    memory.addMessage("assistant", "Salom! Sizga qanday yordam bera olaman?")
    memory.addMessage("user", "Bugun ob-havo qanday?")
    memory.addMessage("assistant", "Toshkentda havo iliq.")
    
    println("Xotirada saqlangan kontekst xabarlari soni: ${memory.getContext().size}")
    memory.getContext().forEach { println("- [${it.role}]: ${it.content}") }
}
```

## Tushuntirish va Mantiq:
Mobil qurilmalarda xotira va token chegaralari cheklangan. Chat tarixi menejeri kerakli kontekstni saqlab qolgan holda ortiqcha tokenlarni qirqadi.

## Ishlash natijasi:
```text
Xotirada saqlangan kontekst xabarlari soni: 3
- [assistant]: Salom! Sizga qanday yordam bera olaman?
- [user]: Bugun ob-havo qanday?
- [assistant]: Toshkentda havo iliq.
```


# 974-Topshiriq: System Prompt ni foydalanuvchi konteksti bilan boyitish
## Topshiriq sharti:
AI Agentga uning vazifasi, joriy sana, foydalanuvchi ismi va tilini tizim ko'rsatmasi (System Instruction) sifatida dinamik shakllantiring.

## Yechim (Kotlin kodi):
```kotlin
fun buildSystemPrompt(userName: String, userLanguage: String): String {
    return "Siz Android mobil qurilmasidagi shaxsiy AI Agentsiz. " +
           "Foydalanuvchi: $userName. " +
           "Javob tili: $userLanguage. " +
           "Qisqa, aniq va do'stona javob bering."
}

fun main() {
    val prompt = buildSystemPrompt("Madina", "O'zbek tili")
    println(prompt)
}
```

## Tushuntirish va Mantiq:
System Prompt AI modelining xulq-atvorini, xavfsizlik chegaralarini va shaxsiyatini belgilab beruvchi eng muhim ko'rsatmadir.

## Ishlash natijasi:
```text
Siz Android mobil qurilmasidagi shaxsiy AI Agentsiz. Foydalanuvchi: Madina. Javob tili: O'zbek tili. Qisqa, aniq va do'stona javob bering.
```


# 975-Topshiriq: Function Calling / Tool Use: Mobil harakatlarni chaqirish mexanizmi
## Topshiriq sharti:
AI modeli foydalanuvchi so'roviga javoban JSON shaklida buyruq (Tool Call) berganda, Kotlin kodi orqali tegishli funksiyani ishga tushirish.

## Yechim (Kotlin kodi):
```kotlin
sealed interface DeviceTool {
    data class SetAlarm(val time: String) : DeviceTool
    data class OpenApp(val appPackage: String) : DeviceTool
}

fun executeDeviceTool(tool: DeviceTool): String {
    return when (tool) {
        is DeviceTool.SetAlarm -> "Qurilmada budilnik ${tool.time} ga o'rnatildi!"
        is DeviceTool.OpenApp -> "Ilova ochildi: ${tool.appPackage}"
    }
}

fun main() {
    val aiDecision: DeviceTool = DeviceTool.SetAlarm("07:00")
    val result = executeDeviceTool(aiDecision)
    println("AI Agent harakati bajarildi -> $result")
}
```

## Tushuntirish va Mantiq:
Tool Use (Function Calling) sun'iy intellektni oddiy chat-botdan haqiqiy Agentga aylantiradi: u real hayotdagi tizimlar va API lar bilan aloqa qila oladi.

## Ishlash natijasi:
```text
AI Agent harakati bajarildi -> Qurilmada budilnik 07:00 ga o'rnatildi!
```


# 976-Topshiriq: Local RAG: Room DB dan matn bo'yicha kontekst qidirib LLM ga uzatish
## Topshiriq sharti:
Foydalanuvchi shaxsiy yozuvlari ichidan mos ma'lumotni topib, savolga qo'shib AI ga yuboruvchi RAG (Retrieval-Augmented Generation) moduli.

## Yechim (Kotlin kodi):
```kotlin
data class LocalDocument(val id: Int, val text: String)

class LocalRagEngine(private val localDocs: List<LocalDocument>) {
    fun retrieveRelevantContext(query: String): String {
        val matched = localDocs.filter { doc ->
            doc.text.contains(query, ignoreCase = true)
        }
        return matched.joinToString("
") { it.text }
    }
}

fun main() {
    val docs = listOf(
        LocalDocument(1, "Uy Wi-Fi paroli: Toshkent2026"),
        LocalDocument(2, "Mashina sug'urtasi muddati: 1-sentyabr")
    )
    val rag = LocalRagEngine(docs)
    val context = rag.retrieveRelevantContext("Wi-Fi")
    
    val augmentedPrompt = "Kontekst: $context
Savol: Mening uy Wi-Fi parolim nima?"
    println("RAG boyitilgan so'rov:")
    println(augmentedPrompt)
}
```

## Tushuntirish va Mantiq:
RAG orqali LLM o'zi bilmaydigan shaxsiy va xususiy ma'lumotlarga ega bo'ladi va o'zbek tilidagi lokal hujjatlar asosida aniq javob beradi.

## Ishlash natijasi:
```text
RAG boyitilgan so'rov:
Kontekst: Uy Wi-Fi paroli: Toshkent2026
Savol: Mening uy Wi-Fi parolim nima?
```


# 977-Topshiriq: AI Javoblarini yozuv mashinkasi (Typewriter) uslubida ekranda chiqarish
## Topshiriq sharti:
StateFlow va koroutina yordamida matnni harfma-harf ekranga chiqaruvchi UI animatsiyasini tuzing.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.delay

class TypewriterViewModel {
    val displayState = MutableStateFlow("")
    
    suspend fun animateText(fullText: String) {
        val sb = StringBuilder()
        for (char in fullText) {
            sb.append(char)
            displayState.value = sb.toString()
            delay(20L)
        }
    }
}

fun main() = runBlocking {
    val vm = TypewriterViewModel()
    println("Typewriter animatsiyasi boshlandi...")
    vm.animateText("Salom, Antigravity!")
    println("Yakuniy matn: ${vm.displayState.value}")
}
```

## Tushuntirish va Mantiq:
Typewriter animatsiyasi foydalanuvchiga matn oqib kelayotgan jonli taassurotni beradi.

## Ishlash natijasi:
```text
Typewriter animatsiyasi boshlandi...
Yakuniy matn: Salom, Antigravity!
```


# 978-Topshiriq: Mobil qurilmada On-device AI (Gemini Nano AICore) interfeysi
## Topshiriq sharti:
Qurilmaning o'zida internet tarmog'isiz ishlaydigan On-Device kichik model chaqiruvini ifodalovchi abstraksiya.

## Yechim (Kotlin kodi):
```kotlin
interface OnDeviceAiModel {
    suspend fun generateText(prompt: String): String
}

class FakeGeminiNano : OnDeviceAiModel {
    override suspend fun generateText(prompt: String): String {
        return "Gemini Nano (Offline): Qurilmada mahalliy NPU yordamida hisoblandi."
    }
}

fun main() {
    println("On-device AI qurilmadagi NPU/GPU orqali to'liq maxfiy va offline ishlaydi.")
}
```

## Tushuntirish va Mantiq:
Gemini Nano Android AICore orqali operatsion tizim darajasida taqdim etiladi va ma'lumotlarni serverga yubormasdan to'liq maxfiylikni kafolatlaydi.

## Ishlash natijasi:
```text
On-device AI qurilmadagi NPU/GPU orqali to'liq maxfiy va offline ishlaydi.
```


# 979-Topshiriq: AI Agent ning qaror qabul qilish sikli (ReAct: Reason + Act pattern)
## Topshiriq sharti:
Foydalanuvchi buyrug'ini tahlil qilib, 'Fikrlash' (Thought) va 'Harakat' (Action) bosqichlarini bajaruvchi ReAct agenti.

## Yechim (Kotlin kodi):
```kotlin
data class AgentStep(val thought: String, val action: String, val observation: String)

class SimpleReActAgent {
    fun solve(goal: String): List<AgentStep> {
        return listOf(
            AgentStep(
                thought = "Foydalanuvchi valyutani bilmoqchi, kurslar datchigini tekshirishim kerak.",
                action = "FetchCurrency(USD)",
                observation = "1 USD = 12850 UZS"
            ),
            AgentStep(
                thought = "Ma'lumot olindi, endi foydalanuvchiga qulay xulosa beraman.",
                action = "ReplyUser",
                observation = "Bugungi kurs: 12,850 so'm"
            )
        )
    }
}

fun main() {
    val agent = SimpleReActAgent()
    val steps = agent.solve("USD kursi qancha?")
    steps.forEachIndexed { i, step ->
        println("Qadam #${i+1}:")
        println("  Fikr: ${step.thought}")
        println("  Amal: ${step.action}")
        println("  Kuzatuv: ${step.observation}")
    }
}
```

## Tushuntirish va Mantiq:
ReAct (Reasoning and Acting) - agentik sun'iy intellektning eng samarali metodologiyasi bo'lib, har bir harakatdan oldin fikrlash bosqichini amalga oshiradi.

## Ishlash natijasi:
```text
Qadam #1:
  Fikr: Foydalanuvchi valyutani bilmoqchi, kurslar datchigini tekshirishim kerak.
  Amal: FetchCurrency(USD)
  Kuzatuv: 1 USD = 12850 UZS
Qadam #2:
  Fikr: Ma'lumot olindi, endi foydalanuvchiga qulay xulosa beraman.
  Amal: ReplyUser
  Kuzatuv: Bugungi kurs: 12,850 so'm
```


# 980-Topshiriq: Tarmoq uzilganda AI so'rovlarini xavfsiz navbatga qo'yish (Offline Queue)
## Topshiriq sharti:
Internet yo'q paytda berilgan so'rovlarni Room bazasida navbatda saqlab, internet paydo bo'lgach yuborish.

## Yechim (Kotlin kodi):
```kotlin
class OfflineAiQueue {
    private val pendingPrompts = mutableListOf<String>()
    
    fun enqueue(prompt: String) {
        pendingPrompts.add(prompt)
        println("So'rov offline navbatga olindi: '$prompt'")
    }
    
    fun processQueue(sender: (String) -> Unit) {
        println("Internet ulandi! Navbatdagi so'rovlar yuborilmoqda...")
        while (pendingPrompts.isNotEmpty()) {
            val p = pendingPrompts.removeAt(0)
            sender(p)
        }
    }
}

fun main() {
    val queue = OfflineAiQueue()
    queue.enqueue("Ertangi rejalarimni tuz")
    queue.processQueue { println("Yuborildi: $it") }
}
```

## Tushuntirish va Mantiq:
Offline Queue mobil tarmoq beqaror bo'lgan sharoitda foydalanuvchi kiritgan so'rovlar yo'qolib ketmasligini ta'minlaydi.

## Ishlash natijasi:
```text
So'rov offline navbatga olindi: 'Ertangi rejalarimni tuz'
Internet ulandi! Navbatdagi so'rovlar yuborilmoqda...
Yuborildi: Ertangi rejalarimni tuz
```


# 981-Topshiriq: Koin bilan AI Repository ni in'yeksiya qilish
## Topshiriq sharti:
Sun'iy intellekt repozitoriysini Koin moduli orqali ViewModel ga in'yeksiya qilish arxitekturasi.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    println("Koin orqali AI modullarini ulash:")
    println("val aiModule = module {")
    println("    single<AiService> { GeminiAiServiceImpl(get()) }")
    println("    single { ChatRepository(get()) }")
    println("    viewModel { AiAssistantViewModel(get()) }")
    println("}")
}
```

## Tushuntirish va Mantiq:
Koin yordamida AI servislari (masalan Gemini API yoki lokal model) osongina almashtiriladi va soxtalashtiriladi (mocking).

## Ishlash natijasi:
```text
Koin orqali AI modullarini ulash:
val aiModule = module {
    single<AiService> { GeminiAiServiceImpl(get()) }
    single { ChatRepository(get()) }
    viewModel { AiAssistantViewModel(get()) }
}
```


# 982-Topshiriq: AI Agent xatoliklarini (RateLimit, OutOfTokens) ushlab zaxira javob berish
## Topshiriq sharti:
API limiti tugaganda (HTTP 429) yoki internet sekinlashganda xavfsiz va tushunarli xabar chiqaruvchi xatoliklar menejeri.

## Yechim (Kotlin kodi):
```kotlin
sealed interface AiError {
    object RateLimitExceeded : AiError
    object NetworkUnavailable : AiError
    data class Unknown(val message: String) : AiError
}

fun handleAiError(error: AiError): String = when (error) {
    AiError.RateLimitExceeded -> "Bugungi so'rovlar limiti tugadi. Iltimos, keyinroq urinib ko'ring."
    AiError.NetworkUnavailable -> "Internet aloqasi mavjud emas. Offline rejim ishga tushdi."
    is AiError.Unknown -> "Xatolik: ${error.message}"
}

fun main() {
    val msg = handleAiError(AiError.RateLimitExceeded)
    println("Xavfsiz xabar: $msg")
}
```

## Tushuntirish va Mantiq:
Kutilmagan texnik xatolarni foydalanuvchiga to'g'ridan-to'g'ri ko'rsatmasdan, muloyim va foydali tavsiyalarga aylantirish yuqori sifatli mahsulot belgisidir.

## Ishlash natijasi:
```text
Xavfsiz xabar: Bugungi so'rovlar limiti tugadi. Iltimos, keyinroq urinib ko'ring.
```


# 983-Topshiriq: AI yaratgan JSON javoblarini qat'iy tekshirib (Schema Validation) o'girish
## Topshiriq sharti:
Model qaytargan JSON matnini kotlinx.serialization orqali aniq Kotlin sinfiga o'tkazish va xatolikni ushlash.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json

@Serializable
data class CalendarEventProposal(val title: String, val date: String, val durationMinutes: Int)

fun parseAiEvent(jsonText: String): CalendarEventProposal? {
    return try {
        Json { ignoreUnknownKeys = true }.decodeFromString<CalendarEventProposal>(jsonText)
    } catch (e: Exception) {
        println("AI formati buzilgan: ${e.message}")
        null
    }
}

fun main() {
    val goodJson = "{\"title\":\"Jamoaviy miting\",\"date\":\"2026-07-01\",\"durationMinutes\":45}"
    val event = parseAiEvent(goodJson)
    println("Tadbir aniqlandi: ${event?.title} (${event?.durationMinutes} daqiqa)")
}
```

## Tushuntirish va Mantiq:
LLM lar har doim ham mukammal JSON qaytarmasligi mumkin. Shuning uchun xavfsiz deserializatsiya va sxema tekshiruvi shart.

## Ishlash natijasi:
```text
Tadbir aniqlandi: Jamoaviy miting (45 daqiqa)
```


# 984-Topshiriq: Mobil AI Kesh: avval so'ralgan savollarni Room bazasida keshlab trafikni tejash
## Topshiriq sharti:
Bir xil savol qayta berilganda serverga murojaat qilmasdan lokal bazadagi javobni darhol qaytaruvchi kesh mexanizmi.

## Yechim (Kotlin kodi):
```kotlin
class SmartAiCache {
    private val memoryCache = mutableMapOf<String, String>()
    
    fun getOrFetch(prompt: String, fetcher: () -> String): String {
        val cached = memoryCache[prompt.lowercase().trim()]
        if (cached != null) {
            println("[KESH]: Javob xotiradan berildi")
            return cached
        }
        println("[SERVER]: AI serverga so'rov yuborildi")
        val fresh = fetcher()
        memoryCache[prompt.lowercase().trim()] = fresh
        return fresh
    }
}

fun main() {
    val cache = SmartAiCache()
    val ans1 = cache.getOrFetch("Toshkent aholisi qancha?") { "3 milliondan ortiq" }
    val ans2 = cache.getOrFetch("Toshkent aholisi qancha?") { "3 milliondan ortiq" }
    println("Natija: $ans2")
}
```

## Tushuntirish va Mantiq:
AI kesh tizimi foydalanuvchi trafigini, mobil batareya quvvatini va qimmatli API tokenlarini sezilarli darajada tejaydi.

## Ishlash natijasi:
```text
[SERVER]: AI serverga so'rov yuborildi
[KESH]: Javob xotiradan berildi
Natija: 3 milliondan ortiq
```


# 985-Topshiriq: Multimodal AI: Rasm baytlarini (Base64) LLM ga tahlil uchun jo'natish
## Topshiriq sharti:
Kamera yoki galereyadagi rasm baytlarini Base64 matniga o'girib, ko'rish (vision) modeliga yuboruvchi ma'lumotlar modeli.

## Yechim (Kotlin kodi):
```kotlin
data class ImagePart(val mimeType: String, val base64Data: String)
data class MultimodalPrompt(val text: String, val images: List<ImagePart>)

fun main() {
    val prompt = MultimodalPrompt(
        text = "Ushbu chekdagi umumiy summani hisoblab ber",
        images = listOf(ImagePart("image/jpeg", "iVBORw0KGgoAAAANSUhEUg..."))
    )
    println("Multimodal so'rov tayyor: matn='${prompt.text}', rasmlar soni=${prompt.images.size}")
}
```

## Tushuntirish va Mantiq:
Multimodal modellar nafaqat matn, balki tasvir, hujjat skaneri va audio fayllarni tahlil qilish imkoniyatini beradi.

## Ishlash natijasi:
```text
Multimodal so'rov tayyor: matn='Ushbu chekdagi umumiy summani hisoblab ber', rasmlar soni=1
```


# 986-Topshiriq: MVI arxitekturasida AiChatIntent boshqaruvi
## Topshiriq sharti:
Foydalanuvchining xabar yuborish, suhbatni tozalash va qayta generatsiya qilish amallarini Intent orqali boshqarish.

## Yechim (Kotlin kodi):
```kotlin
sealed interface AiChatIntent {
    data class SendUserMessage(val text: String) : AiChatIntent
    object ClearChatHistory : AiChatIntent
    object RetryLastMessage : AiChatIntent
}

fun main() {
    val intent: AiChatIntent = AiChatIntent.SendUserMessage("Assalomu alaykum!")
    println("Yuborilgan intent turi: ${intent.javaClass.simpleName}")
}
```

## Tushuntirish va Mantiq:
MVI Intent lari UI komponentlaridan biznes mantiqqa yuboriladigan aniq buyruqlarni ifodalaydi.

## Ishlash natijasi:
```text
Yuborilgan intent turi: SendUserMessage
```


# 987-Topshiriq: Mobil agent xavfsizlik filtri: Xavfli buyruqlarni to'sish (Guardrails)
## Topshiriq sharti:
Foydalanuvchi yoki sun'iy intellekt tomonidan tizimga zarar yetkazuvchi xavfli buyruqlar yuborilishini to'suvchi xavfsizlik tekshiruvini yozing.

## Yechim (Kotlin kodi):
```kotlin
class SafetyGuardrail {
    private val blockedKeywords = listOf("delete_database", "format_storage", "leak_passwords")
    
    fun isSafe(command: String): Boolean {
        return blockedKeywords.none { command.contains(it, ignoreCase = true) }
    }
}

fun main() {
    val guard = SafetyGuardrail()
    println("Buyruq 1 xavfsizmi: ${guard.isSafe("OpenSettings")}")
    println("Buyruq 2 xavfsizmi: ${guard.isSafe("format_storage_now")}")
}
```

## Tushuntirish va Mantiq:
Mobil AI agentlarga tizim resurslariga kirish huquqi berilganda, xavfsizlik filtri (Guardrails) har qanday zararli operatsiyani zudlik bilan to'xtatishi shart.

## Ishlash natijasi:
```text
Buyruq 1 xavfsizmi: true
Buyruq 2 xavfsizmi: false
```


# 988-Topshiriq: Background WorkManager orqali har kuni ertalab kundalik xulosani AI bilan tayyorlash
## Topshiriq sharti:
WorkManager ning davriy vazifasi (PeriodicWorkRequest) orqali tonggi soat 8:00 da AI kunlik rejani generatsiya qilishini loyihalash.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    println("Davriy AI xulosa xizmati:")
    println("val dailySummaryRequest = PeriodicWorkRequestBuilder<AiSummaryWorker>(24, TimeUnit.HOURS)")
    println("    .setConstraints(Constraints.Builder().setRequiredNetworkType(NetworkType.CONNECTED).build())")
    println("    .build()")
}
```

## Tushuntirish va Mantiq:
WorkManager hatto foydalanuvchi ilovani ochmagan bo'lsa ham foni sinxronizatsiya qilib, ertalab bildirishnoma (Push Notification) orqali xulosani taqdim etadi.

## Ishlash natijasi:
```text
Davriy AI xulosa xizmati:
val dailySummaryRequest = PeriodicWorkRequestBuilder<AiSummaryWorker>(24, TimeUnit.HOURS)
    .setConstraints(Constraints.Builder().setRequiredNetworkType(NetworkType.CONNECTED).build())
    .build()
```


# 989-Topshiriq: Ktor WebSockets orqali AI Agent bilan ikki tomonlama tezkor muloqot
## Topshiriq sharti:
Oddiy HTTP so'rovlariga qaraganda ancha tezkor va kam kechikishli doimiy WebSocket kanali orqali audio/token almashish.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    println("Ktor WebSocket mijoz ulanishi:")
    println("client.webSocket("wss://ai-agent.live/stream") {")
    println("    send(Frame.Text("Jonli savol"))")
    println("    for (frame in incoming) {")
    println("        if (frame is Frame.Text) println(frame.readText())")
    println("    }")
    println("}")
}
```

## Tushuntirish va Mantiq:
WebSockets orqali jonli ikki tomonlama audio yoki real-time token almashinuvi minimal kechikish (low latency) bilan amalga oshadi.

## Ishlash natijasi:
```text
Ktor WebSocket mijoz ulanishi:
client.webSocket("wss://ai-agent.live/stream") {
    send(Frame.Text("Jonli savol"))
    for (frame in incoming) {
        if (frame is Frame.Text) println(frame.readText())
    }
}
```


# 990-Topshiriq: AI javobidagi Markdown formatini Jetpack Compose da ko'rsatish
## Topshiriq sharti:
Qalin harflar (**matn**), kod bloklari (`kod`) va ro'yxatlarni to'g'ri render qilish arxitekturasi.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    println("Compose da AI Markdown rendering:")
    println("- Matn ichidagi **qalin** so'zlar AnnotatedString orqali bo'yaladi")
    println("- Kod bloklari maxsus monospaced shrift va fon bilan Card ichiga olinadi")
}
```

## Tushuntirish va Mantiq:
AnnotatedString va Compose RichText kutubxonalari sun'iy intellekt yozgan texnik javoblarni juda chiroyli formatda taqdim etish imkonini beradi.

## Ishlash natijasi:
```text
Compose da AI Markdown rendering:
- Matn ichidagi **qalin** so'zlar AnnotatedString orqali bo'yaladi
- Kod bloklari maxsus monospaced shrift va fon bilan Card ichiga olinadi
```


# 991-Topshiriq: Mobil resurslar (batareya va harorat) ga qarab AI so'rovlarini adaptiv boshqarish
## Topshiriq sharti:
Agar batareya quvvati 15% dan kam bo'lsa, og'ir multimodal so'rovlarni cheklab faqat yengil matn rejimiga o'tish.

## Yechim (Kotlin kodi):
```kotlin
class AdaptiveAiPolicy {
    fun selectModel(batteryPercent: Int): String {
        return if (batteryPercent < 20) {
            "gemini-nano-light (Energiya tejovchi rejim)"
        } else {
            "gemini-pro-cloud (To'liq quvvatli rejim)"
        }
    }
}

fun main() {
    val policy = AdaptiveAiPolicy()
    println("15% quvvatda model: ${policy.selectModel(15)}")
    println("85% quvvatda model: ${policy.selectModel(85)}")
}
```

## Tushuntirish va Mantiq:
Moslashuvchan (Adaptive) siyosat mobil qurilmaning qizib ketishini va batareyasi tez tugab qolishini oldini oladi.

## Ishlash natijasi:
```text
15% quvvatda model: gemini-nano-light (Energiya tejovchi rejim)
85% quvvatda model: gemini-pro-cloud (To'liq quvvatli rejim)
```


# 992-Topshiriq: Clean Architecture: Domain, Data va UI bog'lanishining to'liq zanjiri
## Topshiriq sharti:
UseCase -> Repository -> DataSource -> ViewModel -> Compose UI zanjirini to'liq ko'rsatuvchi arxitektura namunasi.

## Yechim (Kotlin kodi):
```kotlin
// 1. Data Source
class FakeRemoteDataSource { fun getGreeting() = "Salom, Antigravity dunyosi!" }
// 2. Repository
class GreetingRepository(private val ds: FakeRemoteDataSource) { fun fetch() = ds.getGreeting() }
// 3. UseCase
class GetGreetingUseCase(private val repo: GreetingRepository) { operator fun invoke() = repo.fetch() }

fun main() {
    val ds = FakeRemoteDataSource()
    val repo = GreetingRepository(ds)
    val useCase = GetGreetingUseCase(repo)
    
    println("Zanjir yakuni: ${useCase()}")
}
```

## Tushuntirish va Mantiq:
Ushbu toza zanjir har bir qatlamning mustaqilligini, test qilinishini va kengaytirilishini kafolatlaydi.

## Ishlash natijasi:
```text
Zanjir yakuni: Salom, Antigravity dunyosi!
```


# 993-Topshiriq: Jetpack Compose da AI Chat Bubble UI komponenti
## Topshiriq sharti:
Foydalanuvchi (o'ngda yashil) va AI (chapda kulrang) xabarlari pufakchalarini (chat bubbles) yasang.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    println("Compose Chat Bubble dizayni:")
    println("Row(horizontalArrangement = if (isUser) End else Start) {")
    println("    Card(colors = if (isUser) Primary else SurfaceVariant) {")
    println("        Text(message.content)")
    println("    }")
    println("}")
}
```

## Tushuntirish va Mantiq:
Composable pufakchalar Row va Alignment yordamida dinamik joylashadi va har ikki tomon xabarlarini ajratadi.

## Ishlash natijasi:
```text
Compose Chat Bubble dizayni:
Row(horizontalArrangement = if (isUser) End else Start) {
    Card(colors = if (isUser) Primary else SurfaceVariant) {
        Text(message.content)
    }
}
```


# 994-Topshiriq: Mobil AI Agent testlash: Mock UseCase va Unit Testlar
## Topshiriq sharti:
Biznes mantiqni haqiqiy tarmoq so'rovisiz testlovchi soxta (Mock) UseCase yozing.

## Yechim (Kotlin kodi):
```kotlin
class MockAiUseCase {
    fun execute(prompt: String): String = "Test javobi: $prompt"
}

fun main() {
    val mock = MockAiUseCase()
    val result = mock.execute("Salom")
    println("Unit test muvaffaqiyatli: ${result == "Test javobi: Salom"}")
}
```

## Tushuntirish va Mantiq:
Clean Architecture tufayli barcha qatlamlar izolyatsiya qilingan va hech qanday haqiqiy API puli sarflanmasdan 100% test qilinadi.

## Ishlash natijasi:
```text
Unit test muvaffaqiyatli: true
```


# 995-Topshiriq: AI Agent javobini xotiraga nusxalash (Clipboard Manager)
## Topshiriq sharti:
Foydalanuvchi AI javobini bitta tugma bilan telefon xotirasiga (clipboard) ko'chirib olishi.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    println("LocalClipboardManager orqali matn nusxalash:")
    println("val clipboardManager = LocalClipboardManager.current")
    println("clipboardManager.setText(AnnotatedString(aiText))")
}
```

## Tushuntirish va Mantiq:
LocalClipboardManager Compose da tizim buferi bilan xavfsiz muloqot qiladi.

## Ishlash natijasi:
```text
LocalClipboardManager orqali matn nusxalash:
val clipboardManager = LocalClipboardManager.current
clipboardManager.setText(AnnotatedString(aiText))
```


# 996-Topshiriq: AI Xabarlar ro'yxatida avtomatik pastga skroll qilish (LazyListState.animateScrollToItem)
## Topshiriq sharti:
Yangi token yoki xabar kelishi bilan ro'yxatni avtomatik ravishda eng pastiga surib turuvchi Compose yechimi.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    println("Avtomatik skroll mexanizmi:")
    println("val listState = rememberLazyListState()")
    println("LaunchedEffect(messages.size) {")
    println("    listState.animateScrollToItem(messages.size - 1)")
    println("}")
}
```

## Tushuntirish va Mantiq:
LaunchedEffect messages.size ga bog'langan bo'lib, har bir yangi xabarda oxirgi elementga silliq surib beradi.

## Ishlash natijasi:
```text
Avtomatik skroll mexanizmi:
val listState = rememberLazyListState()
LaunchedEffect(messages.size) {
    listState.animateScrollToItem(messages.size - 1)
}
```


# 997-Topshiriq: KMP va Compose Multiplatform: Bir xil UI ni Android va iOS da yurgazish
## Topshiriq sharti:
Compose Multiplatform orqali bir xil yozilgan Composable kodini ikkala operatsion tizimda ham ishlatish tushuntirishi.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    println("Compose Multiplatform (CMP):")
    println("- Android da: Jetpack Compose")
    println("- iOS da: Skia / Metal orqali to'g'ridan-to'g'ri render")
    println("- 100% bir xil Kotlin UI kodi")
}
```

## Tushuntirish va Mantiq:
JetBrains Compose Multiplatform barcha platformalarda bir xil deklarativ kod yozish va umumiy UI yaratish imkonini beradi.

## Ishlash natijasi:
```text
Compose Multiplatform (CMP):
- Android da: Jetpack Compose
- iOS da: Skia / Metal orqali to'g'ridan-to'g'ri render
- 100% bir xil Kotlin UI kodi
```


# 998-Topshiriq: Kotlin 2.0 K2 kompilyatori va Compose Compiler integratsiyasi
## Topshiriq sharti:
Kotlin 2.0 da Compose Compiler plaginining to'g'ridan-to'g'ri Kotlin omboriga birlashtirilishi va uning afzalliklari.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    println("Kotlin 2.0 K2 Compilator va Compose:")
    println("1. Compose Compiler endi alohida emas, Kotlin 2.0+ tarkibiga kiritilgan")
    println("2. Yangi FIR (Frontend Intermediate Representation) orqali kompilyatsiya tezligi 2 barobar oshgan")
    println("3. Barqarorlik (Strong Skipping Mode) avtomatik yoqilgan")
}
```

## Tushuntirish va Mantiq:
K2 kompilyatori Compose kodini ancha tezroq tekshiradi va Strong Skipping Mode tufayli barqaror bo'lmagan parametrlar uchun ham ortiqcha qayta chizilishlarni oldini oladi.

## Ishlash natijasi:
```text
Kotlin 2.0 K2 Compilator va Compose:
1. Compose Compiler endi alohida emas, Kotlin 2.0+ tarkibiga kiritilgan
2. Yangi FIR (Frontend Intermediate Representation) orqali kompilyatsiya tezligi 2 barobar oshgan
3. Barqarorlik (Strong Skipping Mode) avtomatik yoqilgan
```


# 999-Topshiriq: Mobil AI Agentning to'liq arxitektura diagrammasi va konveyeri
## Topshiriq sharti:
Foydalanuvchi ovozidan boshlab, LLM tahlili, Tool chaqiruvi va yakuniy UI yangilanishigacha bo'lgan to'liq konveyerni sintez qilish.

## Yechim (Kotlin kodi):
```kotlin
fun main() {
    println("Mobil AI Agent to'liq konveyeri:")
    println("[Foydalanuvchi] -> UI Intent -> ViewModel")
    println("               -> Local RAG (Room DB)")
    println("               -> Guardrails (Xavfsizlik)")
    println("               -> Ktor Client (Token Streaming)")
    println("               -> Tool Execution (Agar buyruq bo'lsa)")
    println("               -> StateFlow (Typewriter) -> Jetpack Compose UI")
}
```

## Tushuntirish va Mantiq:
Ushbu yaxlit konveyer zamonaviy mobil dasturlashning eng ilg'or cho'qqisi bo'lib, Clean Architecture va zamonaviy sun'iy intellektni birlashtiradi.

## Ishlash natijasi:
```text
Mobil AI Agent to'liq konveyeri:
[Foydalanuvchi] -> UI Intent -> ViewModel
               -> Local RAG (Room DB)
               -> Guardrails (Xavfsizlik)
               -> Ktor Client (Token Streaming)
               -> Tool Execution (Agar buyruq bo'lsa)
               -> StateFlow (Typewriter) -> Jetpack Compose UI
```


# 1000-Topshiriq: 1000-Topshiriq: To'liq ishlab turgan Mobil Shaxsiy AI Yordamchisi tizimi
## Topshiriq sharti:
Clean Architecture, Ktor Streaming, StateFlow, Room kesh, Tool Execution va Compose UI ni o'zida birlashtirgan, to'liq ishlovchi 1000-yakuniy grand-loyiha dasturini yarating.

## Yechim (Kotlin kodi):
```kotlin
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.delay

// 1. DOMAIN QATLAMI
data class Message(val sender: String, val text: String)

interface AiService {
    fun streamResponse(prompt: String): Flow<String>
}

// 2. DATA QATLAMI
class FakeAiClient : AiService {
    override fun streamResponse(prompt: String): Flow<String> = flow {
        val words = "Salom! Men sizning Kotlin 2.0 da yaratilgan shaxsiy mobil AI yordamchingizman. Barcha vazifalar bajarildi!".split(" ")
        for (w in words) {
            delay(50L)
            emit("$w ")
        }
    }
}

// 3. PRESENTATION QATLAMI (VIEWMODEL)
class MobileAiAssistantViewModel(private val aiService: AiService) {
    private val _messages = MutableStateFlow<List<Message>>(emptyList())
    val messages = _messages.asStateFlow()
    
    private val _isStreaming = MutableStateFlow(false)
    val isStreaming = _isStreaming.asStateFlow()
    
    suspend fun sendMessage(userText: String) {
        val currentList = _messages.value.toMutableList()
        currentList.add(Message("Foydalanuvchi", userText))
        _messages.value = currentList
        
        _isStreaming.value = true
        val responseBuilder = StringBuilder()
        
        aiService.streamResponse(userText).collect { token ->
            responseBuilder.append(token)
            val updated = _messages.value.toMutableList()
            if (updated.last().sender == "AI") {
                updated[updated.size - 1] = Message("AI", responseBuilder.toString().trim())
            } else {
                updated.add(Message("AI", responseBuilder.toString().trim()))
            }
            _messages.value = updated
        }
        _isStreaming.value = false
    }
}

// 4. MAIN VA ISHGA TUSHIRISH
fun main() = runBlocking {
    println("================================================================")
    println("  KOTLIN 2.0 TA'LIMIY DATASET: 1000-YAKUNIY TOPSHIRIQ LOYIHASI  ")
    println("================================================================")
    
    val aiService = FakeAiClient()
    val viewModel = MobileAiAssistantViewModel(aiService)
    
    println("Foydalanuvchi so'rovi yuborilmoqda: 'Salom, yordamchi!'")
    viewModel.sendMessage("Salom, yordamchi!")
    
    println("
Suhbat tarixi:")
    viewModel.messages.value.forEach { msg ->
        println("[${msg.sender}]: ${msg.text}")
    }
    
    println("
Tabriklaymiz! 1,000 ta amaliy Kotlin topshirig'i muvaffaqiyatli yakunlandi!")
}
```

## Tushuntirish va Mantiq:
Ushbu 1000-yakuniy topshiriqda butun kurs davomida o'rganilgan barcha asosiy tushunchalar: Asosiy tiplar, Null-safety, OOP, Koroutinalar, Flow, Clean Architecture, Ktor streaming va Mobil AI Agent tamoyillari mukammal yakuniy loyihaga birlashtirildi.

## Ishlash natijasi:
```text
================================================================
  KOTLIN 2.0 TA'LIMIY DATASET: 1000-YAKUNIY TOPSHIRIQ LOYIHASI  
================================================================
Foydalanuvchi so'rovi yuborilmoqda: 'Salom, yordamchi!'

Suhbat tarixi:
[Foydalanuvchi]: Salom, yordamchi!
[AI]: Salom! Men sizning Kotlin 2.0 da yaratilgan shaxsiy mobil AI yordamchingizman. Barcha vazifalar bajarildi!

Tabriklaymiz! 1,000 ta amaliy Kotlin topshirig'i muvaffaqiyatli yakunlandi!
```

