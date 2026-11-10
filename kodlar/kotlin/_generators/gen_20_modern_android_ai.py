# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(r"C:\Users\User\Desktop\uzbek_dataset\kodlar\kotlin\_generators")
from task_builder import format_task, save_file

tasks = []

def add_task(num, title, cond, code, exp, res):
    tasks.append(format_task(num, title, cond, code, exp, res))

# 951
add_task(
    951,
    "Clean Architecture qatlamlari: Domain Entity modeli",
    "Clean Architecture ning eng markaziy, hech qanday ramka yoki kutubxonaga bog'liq bo'lmagan Domain Entity sinfini yarating.",
    """
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
""",
    "Domain qatlami dasturning yuragi hisoblanadi. Undagi Entity sinflari Android SDK, ma'lumotlar bazasi yoki tarmoq kutubxonalariga mutlaqo bog'liq bo'lmagan sof Kotlin sinflaridir.",
    """
Domain Entity yaratildi: Kotlin K2 kompilyatorini o'rganish (Bajarildi: false)
"""
)

# 952
add_task(
    952,
    "Domain UseCase yaratish (operator fun invoke yordamida)",
    "Bitta aniq biznes vazifasini bajaruvchi GetActiveTasksUseCase ni Kotlin ning `operator fun invoke` sintaksisi bilan yozing.",
    """
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
""",
    "UseCase (yoki Interactor) yagona mas'uliyat tamoyiliga (Single Responsibility Principle) tayanadi. U orqali Presentation qatlami Repository dagi biznes logikani boshqaradi.",
    """
UseCase: Bitta biznes vazifasini bajaruvchi mustaqil domen mantiqi.
operator fun invoke yordamida UseCase funksiya kabi chaqiriladi: getActiveTasks()
"""
)

# 953
add_task(
    953,
    "Repository interfeysi va uning Data qatlamidagi realizatsiyasi",
    "Domain qatlamida e'lon qilingan Repository interfeysini Data qatlamida amalga oshiring.",
    """
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
""",
    "Inversion of Control printsipiga ko'ra, Domain qatlami Repository interfeysini egalik qiladi, Data qatlami esa uni amalga oshiradi. Bu esa ma'lumotlar manbaini oson almashtirish imkonini beradi.",
    """
Repository Pattern: Ma'lumotlar qayerdan kelishini biznes mantiqdan to'liq yashiradi.
"""
)

# 954
add_task(
    954,
    "Result Wrapper (Sealed Class: Success, Error, Loading)",
    "Tarmoq va baza operatsiyalari natijasini xavfsiz ifodalovchi Result umumiy sealed sinfini yarating.",
    """
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
""",
    "Result Wrapper yordamida Presentation qatlami operatsiyaning holatini (yuklanish, natija yoki xato) to'liq va xavfsiz boshqaradi.",
    """
Natija: Muvaffaqiyatli ma'lumot
"""
)

# 955
add_task(
    955,
    "MVVM ViewModel arxitekturasi va UI State boshqaruvi",
    "StateFlow orqali UI State saqlovchi va asinxron biznes operatsiyalarni chaqiruvchi ViewModel namunasini tuzing.",
    """
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
""",
    "MVVM (Model-View-ViewModel) arxitekturasida ViewModel UI holatini saqlaydi va konfiguratsiya o'zgarishlarida (ekran burilishi) o'chib ketmaydi.",
    """
Boshlang'ich holat: isLoading=true
Yuklangach: [Compose o'rganish, Koin ulash]
"""
)

# 956
add_task(
    956,
    "MVI (Model-View-Intent) naqshi: Intent/Action larni qayta ishlash",
    "Foydalanuvchi harakatlarini Intent (harakat signallari) sifatida qabul qilib, holatni bir tomonlama o'zgartiruvchi MVI arxitekturasini yozing.",
    """
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
""",
    "MVI arxitekturasi Unidirectional Data Flow (UDF) tamoyiliga qat'iy asoslangan: View -> Intent -> Reducer/ViewModel -> State -> View sikli aylanadi.",
    """
MVI: Vazifalar yuklanmoqda...
MVI: Vazifa #TK-101 bajarildi deb belgilandi.
"""
)

# 957
add_task(
    957,
    "Dependency Injection (DI) tushunchasi va qo'lda Service Locator yaratish",
    "Kutubxonalarsiz, sof Kotlin da bog'liqliklarni boshqaruvchi Service Locator konteynerini yarating.",
    """
interface ApiService { fun fetch(): String }
class ApiServiceImpl : ApiService { override fun fetch() = "Tarmoq ma'lumoti" }

object AppContainer {
    val apiService: ApiService by lazy { ApiServiceImpl() }
}

fun main() {
    val service = AppContainer.apiService
    println("Olingan servis orqali ma'lumot: ${service.fetch()}")
}
""",
    "Dependency Injection ob'yektlar o'z bog'liqliklarini o'zi yaratmasdan, tashqaridan qabul qilishini ta'minlaydi. Bu kodni modulli va testlashga juda oson qiladi.",
    """
Olingan servis orqali ma'lumot: Tarmoq ma'lumoti
"""
)

# 958
add_task(
    958,
    "Koin DI: module, single va factory e'lon qilish",
    "Koin ning sof Kotlin tilidagi DSL sintaksisi orqali modul tuzilishi va instansiyalar boshqaruvini ko'rsating.",
    """
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
""",
    "Koin reflection ishlatmaydi, kompilyatsiya vaqtida kod generatsiyasi qilmaydi, balki toza Kotlin funksiyalari va DSL orqali juda yengil va tez ishlaydi.",
    """
Koin modul strukturasi sintaksisi:
val appModule = module {
    single { DatabaseDriver() } // Singleton: butun ilovada yagona nusxa
    factory { UserRepository(get()) } // Har chaqirilganda yangi nusxa
}
"""
)

# 959
add_task(
    959,
    "Koin da viewModel {} ta'rifi va in'yeksiyasi",
    "Koin orqali Android ViewModel ni ro'yxatdan o'tkazish qoidasini tushuntiring.",
    """
fun main() {
    println("Koin ViewModel DSL:")
    println("viewModel { HomeViewModel(get()) }")
    println("Composable ichida chaqirish:")
    println("val viewModel: HomeViewModel = koinViewModel()")
}
""",
    "Koin ning Android kutubxonasi `viewModel { }` DSL i orqali Android ViewModelProvider bilan to'liq integratsiya bo'ladi.",
    """
Koin ViewModel DSL:
viewModel { HomeViewModel(get()) }
Composable ichida chaqirish:
val viewModel: HomeViewModel = koinViewModel()
"""
)

# 960
add_task(
    960,
    "Dagger Hilt annotatsiyalari va arxitekturasi",
    "Hilt ning asosiy annotatsiyalari (@HiltAndroidApp, @AndroidEntryPoint, @HiltViewModel, @Inject) vazifalarini tushuntiruvchi kod yozing.",
    """
fun main() {
    println("Dagger Hilt annotatsiyalari:")
    println("- @HiltAndroidApp: Application sinfida DI daraxtini ishga tushiradi")
    println("- @AndroidEntryPoint: Activity va Fragment larni in'yeksiyaga tayyorlaydi")
    println("- @HiltViewModel: ViewModel ga bog'liqliklarni kiritadi")
    println("- @Inject constructor(...): Konstruktorni avtomatik ta'minlash belgisi")
}
""",
    "Dagger Hilt kompilyatsiya vaqtida (compile-time) bog'liqliklarni tekshiradi va hech qanday runtime overhead'siz Java/Kotlin kodlarini generatsiya qiladi.",
    """
Dagger Hilt annotatsiyalari:
- @HiltAndroidApp: Application sinfida DI daraxtini ishga tushiradi
- @AndroidEntryPoint: Activity va Fragment larni in'yeksiyaga tayyorlaydi
- @HiltViewModel: ViewModel ga bog'liqliklarni kiritadi
- @Inject constructor(...): Konstruktorni avtomatik ta'minlash belgisi
"""
)

# 961
add_task(
    961,
    "Ktor HTTP Client bilan asinxron so'rov yuborish asoslari",
    "Kotlin Multiplatform va Android uchun eng ilg'or asinxron tarmoq mijozi bo'lgan Ktor Client arxitekturasini yozing.",
    """
fun main() {
    println("Ktor HTTP Client e'lon qilish:")
    println("val client = HttpClient(CIO) {")
    println("    install(ContentNegotiation) {")
    println("        json()")
    println("    }")
    println("}")
    println("Asinxron so'rov: val response = client.get(\"https://api.example.com/items\")")
}
""",
    "Ktor to'liq koroutinalar ustiga qurilgan va Android, iOS, Desktop va Web (Wasm/JS) platformalarining barchasida bir xil ishlay oladi.",
    """
Ktor HTTP Client e'lon qilish:
val client = HttpClient(CIO) {
    install(ContentNegotiation) {
        json()
    }
}
Asinxron so'rov: val response = client.get("https://api.example.com/items")
"""
)

# 962
add_task(
    962,
    "Ktor Client bilan POST so'rovida JSON uzatish",
    "Ktor yordamida serverga yangi ma'lumot jo'natuvchi POST chaqiruvini loyihalang.",
    """
fun main() {
    println("Ktor POST so'rovi sintaksisi:")
    println("val response: HttpResponse = client.post(\"https://api.example.com/login\") {")
    println("    contentType(ContentType.Application.Json)")
    println("    setBody(LoginRequest(\"alisher\", \"parol123\"))")
    println("}")
}
""",
    "setBody() va ContentType.Application.Json orqali obyekt kotlinx.serialization yordamida avtomatik JSON ga aylanadi va serverga yo'llanadi.",
    """
Ktor POST so'rovi sintaksisi:
val response: HttpResponse = client.post("https://api.example.com/login") {
    contentType(ContentType.Application.Json)
    setBody(LoginRequest("alisher", "parol123"))
}
"""
)

# 963
add_task(
    963,
    "Retrofit API interfeysi va Suspend funksiyalar bilan ishlash",
    "Android dagi an'anaviy Retrofit kutubxonasini Kotlin suspend funksiyalari bilan integratsiyalash.",
    """
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
""",
    "Retrofit 2.6.0+ versiyalaridan boshlab Kotlin Coroutines ni to'liq qo'llab-quvvatlaydi va so'rovlarni avtomatik non-blocking qiladi.",
    """
Retrofit interfeysida `suspend fun` qo'yilsa, qo'shimcha Call<T> talab qilinmaydi.
"""
)

# 964
add_task(
    964,
    "Room Database: @Entity data klassi",
    "Android SQLite bazasi bilan ishlash uchun Room @Entity modelini yarating.",
    """
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
""",
    "Room da har bir jadval @Entity bilan belgilanadi. @PrimaryKey(autoGenerate = true) orqali noyob identifikator avtomatik oshirib boriladi.",
    """
Room Entity yaratildi: Eslatma
"""
)

# 965
add_task(
    965,
    "Room Database: @Dao interfeysi va CRUD operatsiyalari",
    "Room Data Access Object (DAO) interfeysida ma'lumot qo'shish, o'chirish va yangilash operatsiyalarini yozing.",
    """
interface NoteDao {
    suspend fun insert(note: NoteEntity)
    suspend fun delete(note: NoteEntity)
    suspend fun getNoteById(id: Long): NoteEntity?
}

fun main() {
    println("Room DAO: Barcha SQL operatsiyalari suspend funksiyalar orqali xavfsiz o'raladi.")
}
""",
    "DAO interfeysidagi suspend funksiyalar Room tomonidan avtomatik ravishda disk I/O oqimida bajariladi va UI ni muzlatmaydi.",
    """
Room DAO: Barcha SQL operatsiyalari suspend funksiyalar orqali xavfsiz o'raladi.
"""
)

# 966
add_task(
    966,
    "Room Database: Flow<List<Entity>> bilan reaktiv ma'lumotlar kuzatuvi",
    "Ma'lumotlar bazasida biror o'zgarish sodir bo'lishi bilan UI ga avtomatik yangi ro'yxatni yetkazib beruvchi Flow so'rovini yozing.",
    """
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
""",
    "Room kutubxonasi Flow qaytaruvchi so'rovlarni avtomatik kuzatuvchi (Observable Query) rejimiga o'tkazadi va SQL tranzaksiyalarini reaktiv boshqaradi.",
    """
Room + Flow: Jadvalga INSERT yoki DELETE bo'lishi bilan Flow avtomatik yangi ma'lumotni emit qiladi.
"""
)

# 967
add_task(
    967,
    "Offline-First arxitekturasi: Kesh va Tarmoq sinxronizatsiyasi",
    "Ilova avval lokal bazadagi ma'lumotni darhol ko'rsatib, so'ngra orqa fonda yangilab boruvchi Repository naqshini loyihalang.",
    """
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
""",
    "Single Source of Truth (SSOT) printsipiga binoan, UI faqat lokal bazani kuzatadi, tarmoqdan kelgan yangi ma'lumotlar esa avval bazaga saqlanadi.",
    """
Offline-First: Internet yo'q bo'lsa ham ilova to'xtamasdan lokal keshdan ishlayveradi.
"""
)

# 968
add_task(
    968,
    "DataStore Preferences orqali kalit-qiymatlarni asinxron saqlash",
    "Eski va xavfli SharedPreferences o'rniga Jetpack DataStore dan foydalanish printsipini tushuntiring.",
    """
fun main() {
    println("Jetpack Preferences DataStore:")
    println("1. To'liq asinxron va Flow asosida ishlaydi")
    println("2. UI thread ni hech qachon bloklamaydi")
    println("3. Tranzaksion xavfsizlikka (consistency) ega")
}
""",
    "DataStore Kotlin koroutinalari va Flow ustiga qurilgan bo'lib, eski SharedPreferences dagi ANR (Application Not Responding) xatolarini butunlay bartaraf etadi.",
    """
Jetpack Preferences DataStore:
1. To'liq asinxron va Flow asosida ishlaydi
2. UI thread ni hech qachon bloklamaydi
3. Tranzaksion xavfsizlikka (consistency) ega
"""
)

# 969
add_task(
    969,
    "WorkManager yordamida kafolatlangan fon vazifalarini rejalashtirish",
    "Ilova yopilganda yoki telefon qayta yoqilganda ham bajarilishini kafolatlovchi CoroutineWorker tuzilishi.",
    """
fun main() {
    println("WorkManager va CoroutineWorker:")
    println("- doWork() suspend funksiyasi orqali koroutina ishga tushadi")
    println("- Constraints: NetworkType.CONNECTED, RequiresCharging")
    println("- PeriodicWorkRequestBuilder<SyncWorker>(24, TimeUnit.HOURS)")
}
""",
    "WorkManager batareyani tejash uchun operatsion tizim Doze rejimiga moslashadi va belgilangan shartlar (masalan Wi-Fi va quvvatlagich ulanganda) bajarilganda fon ishini boshlaydi.",
    """
WorkManager va CoroutineWorker:
- doWork() suspend funksiyasi orqali koroutina ishga tushadi
- Constraints: NetworkType.CONNECTED, RequiresCharging
- PeriodicWorkRequestBuilder<SyncWorker>(24, TimeUnit.HOURS)
"""
)

# 970
add_task(
    970,
    "Kotlin Multiplatform (KMP) `expect` va `actual` deklaratsiyalari",
    "Umumiy (common) kodda platformaga xos operatsiyani e'lon qilib, Android va iOS uchun alohida amalga oshirish mexanizmini ko'rsating.",
    """
// Common modulda:
// expect fun getPlatformName(): String

// Android modulda:
// actual fun getPlatformName(): String = "Android OS"

// iOS modulda:
// actual fun getPlatformName(): String = "Apple iOS"

fun main() {
    println("KMP expect/actual: Umumiy koddan turib platforma imkoniyatlariga to'g'ridan-to'g'ri murojaat.")
}
""",
    "expect/actual Kotlin Multiplatform ning polimorfik kompile-time kaliti bo'lib, umumiy biznes mantiqni platforma drayverlariga bog'laydi.",
    """
KMP expect/actual: Umumiy koddan turib platforma imkoniyatlariga to'g'ridan-to'g'ri murojaat.
"""
)

# 971
add_task(
    971,
    "Mobil AI arxitekturasi: LLM Request va Response modellari",
    "Mobil qurilmadan sun'iy intellekt (Gemini yoki Claude) modeliga yuboriladigan so'rov va javob ma'lumotlar strukturasini loyihalang.",
    """
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
""",
    "Mobil AI ilovalarda JSON so'rov va javob modellari qat'iy tiplangan bo'lishi lozim, bu esa tarmoq integratsiyasini xavfsiz qiladi.",
    """
AI so'rov modeli tayyorlandi: gemini-1.5-flash, Xabarlar soni: 1
"""
)

# 972
add_task(
    972,
    "Token Streaming: Serverdan tokenlarni Flow da bo'laklab qabul qilish",
    "LLM butun javobni generatsiya qilib bo'lishini kutmasdan, har bir chiqqan so'z/tokenni reaktiv oqim (Flow<String>) orqali uzatuvchi xizmat yozing.",
    """
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
""",
    "Token Streaming mobil ilovada foydalanuvchi tajribasini (UX) keskin oshiradi: foydalanuvchi 5 soniya kutmasdan darhol javob yozilishini jonli ko'radi.",
    """
AI javobi: Kotlin - bu zamonaviy, xavfsiz va kuchli dasturlash tili.
"""
)

# 973
add_task(
    973,
    "Mobil AI Agent: Chat tarixi va xotira boshqaruvi (Context Window)",
    "Foydalanuvchi bilan davom etayotgan suhbat tarixini saqlovchi va xotira to'lib ketmasligi uchun eski xabarlarni ixchamlovchi xotira menejeri yozing.",
    """
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
""",
    "Mobil qurilmalarda xotira va token chegaralari cheklangan. Chat tarixi menejeri kerakli kontekstni saqlab qolgan holda ortiqcha tokenlarni qirqadi.",
    """
Xotirada saqlangan kontekst xabarlari soni: 3
- [assistant]: Salom! Sizga qanday yordam bera olaman?
- [user]: Bugun ob-havo qanday?
- [assistant]: Toshkentda havo iliq.
"""
)

# 974
add_task(
    974,
    "System Prompt ni foydalanuvchi konteksti bilan boyitish",
    "AI Agentga uning vazifasi, joriy sana, foydalanuvchi ismi va tilini tizim ko'rsatmasi (System Instruction) sifatida dinamik shakllantiring.",
    """
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
""",
    "System Prompt AI modelining xulq-atvorini, xavfsizlik chegaralarini va shaxsiyatini belgilab beruvchi eng muhim ko'rsatmadir.",
    """
Siz Android mobil qurilmasidagi shaxsiy AI Agentsiz. Foydalanuvchi: Madina. Javob tili: O'zbek tili. Qisqa, aniq va do'stona javob bering.
"""
)

# 975
add_task(
    975,
    "Function Calling / Tool Use: Mobil harakatlarni chaqirish mexanizmi",
    "AI modeli foydalanuvchi so'roviga javoban JSON shaklida buyruq (Tool Call) berganda, Kotlin kodi orqali tegishli funksiyani ishga tushirish.",
    """
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
""",
    "Tool Use (Function Calling) sun'iy intellektni oddiy chat-botdan haqiqiy Agentga aylantiradi: u real hayotdagi tizimlar va API lar bilan aloqa qila oladi.",
    """
AI Agent harakati bajarildi -> Qurilmada budilnik 07:00 ga o'rnatildi!
"""
)

# 976
add_task(
    976,
    "Local RAG: Room DB dan matn bo'yicha kontekst qidirib LLM ga uzatish",
    "Foydalanuvchi shaxsiy yozuvlari ichidan mos ma'lumotni topib, savolga qo'shib AI ga yuboruvchi RAG (Retrieval-Augmented Generation) moduli.",
    """
data class LocalDocument(val id: Int, val text: String)

class LocalRagEngine(private val localDocs: List<LocalDocument>) {
    fun retrieveRelevantContext(query: String): String {
        val matched = localDocs.filter { doc ->
            doc.text.contains(query, ignoreCase = true)
        }
        return matched.joinToString("\n") { it.text }
    }
}

fun main() {
    val docs = listOf(
        LocalDocument(1, "Uy Wi-Fi paroli: Toshkent2026"),
        LocalDocument(2, "Mashina sug'urtasi muddati: 1-sentyabr")
    )
    val rag = LocalRagEngine(docs)
    val context = rag.retrieveRelevantContext("Wi-Fi")
    
    val augmentedPrompt = "Kontekst: $context\nSavol: Mening uy Wi-Fi parolim nima?"
    println("RAG boyitilgan so'rov:")
    println(augmentedPrompt)
}
""",
    "RAG orqali LLM o'zi bilmaydigan shaxsiy va xususiy ma'lumotlarga ega bo'ladi va o'zbek tilidagi lokal hujjatlar asosida aniq javob beradi.",
    """
RAG boyitilgan so'rov:
Kontekst: Uy Wi-Fi paroli: Toshkent2026
Savol: Mening uy Wi-Fi parolim nima?
"""
)

# 977
add_task(
    977,
    "AI Javoblarini yozuv mashinkasi (Typewriter) uslubida ekranda chiqarish",
    "StateFlow va koroutina yordamida matnni harfma-harf ekranga chiqaruvchi UI animatsiyasini tuzing.",
    """
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
""",
    "Typewriter animatsiyasi foydalanuvchiga matn oqib kelayotgan jonli taassurotni beradi.",
    """
Typewriter animatsiyasi boshlandi...
Yakuniy matn: Salom, Antigravity!
"""
)

# 978
add_task(
    978,
    "Mobil qurilmada On-device AI (Gemini Nano AICore) interfeysi",
    "Qurilmaning o'zida internet tarmog'isiz ishlaydigan On-Device kichik model chaqiruvini ifodalovchi abstraksiya.",
    """
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
""",
    "Gemini Nano Android AICore orqali operatsion tizim darajasida taqdim etiladi va ma'lumotlarni serverga yubormasdan to'liq maxfiylikni kafolatlaydi.",
    """
On-device AI qurilmadagi NPU/GPU orqali to'liq maxfiy va offline ishlaydi.
"""
)

# 979
add_task(
    979,
    "AI Agent ning qaror qabul qilish sikli (ReAct: Reason + Act pattern)",
    "Foydalanuvchi buyrug'ini tahlil qilib, 'Fikrlash' (Thought) va 'Harakat' (Action) bosqichlarini bajaruvchi ReAct agenti.",
    """
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
""",
    "ReAct (Reasoning and Acting) - agentik sun'iy intellektning eng samarali metodologiyasi bo'lib, har bir harakatdan oldin fikrlash bosqichini amalga oshiradi.",
    """
Qadam #1:
  Fikr: Foydalanuvchi valyutani bilmoqchi, kurslar datchigini tekshirishim kerak.
  Amal: FetchCurrency(USD)
  Kuzatuv: 1 USD = 12850 UZS
Qadam #2:
  Fikr: Ma'lumot olindi, endi foydalanuvchiga qulay xulosa beraman.
  Amal: ReplyUser
  Kuzatuv: Bugungi kurs: 12,850 so'm
"""
)

# 980
add_task(
    980,
    "Tarmoq uzilganda AI so'rovlarini xavfsiz navbatga qo'yish (Offline Queue)",
    "Internet yo'q paytda berilgan so'rovlarni Room bazasida navbatda saqlab, internet paydo bo'lgach yuborish.",
    """
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
""",
    "Offline Queue mobil tarmoq beqaror bo'lgan sharoitda foydalanuvchi kiritgan so'rovlar yo'qolib ketmasligini ta'minlaydi.",
    """
So'rov offline navbatga olindi: 'Ertangi rejalarimni tuz'
Internet ulandi! Navbatdagi so'rovlar yuborilmoqda...
Yuborildi: Ertangi rejalarimni tuz
"""
)

# 981
add_task(
    981,
    "Koin bilan AI Repository ni in'yeksiya qilish",
    "Sun'iy intellekt repozitoriysini Koin moduli orqali ViewModel ga in'yeksiya qilish arxitekturasi.",
    """
fun main() {
    println("Koin orqali AI modullarini ulash:")
    println("val aiModule = module {")
    println("    single<AiService> { GeminiAiServiceImpl(get()) }")
    println("    single { ChatRepository(get()) }")
    println("    viewModel { AiAssistantViewModel(get()) }")
    println("}")
}
""",
    "Koin yordamida AI servislari (masalan Gemini API yoki lokal model) osongina almashtiriladi va soxtalashtiriladi (mocking).",
    """
Koin orqali AI modullarini ulash:
val aiModule = module {
    single<AiService> { GeminiAiServiceImpl(get()) }
    single { ChatRepository(get()) }
    viewModel { AiAssistantViewModel(get()) }
}
"""
)

# 982
add_task(
    982,
    "AI Agent xatoliklarini (RateLimit, OutOfTokens) ushlab zaxira javob berish",
    "API limiti tugaganda (HTTP 429) yoki internet sekinlashganda xavfsiz va tushunarli xabar chiqaruvchi xatoliklar menejeri.",
    """
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
""",
    "Kutilmagan texnik xatolarni foydalanuvchiga to'g'ridan-to'g'ri ko'rsatmasdan, muloyim va foydali tavsiyalarga aylantirish yuqori sifatli mahsulot belgisidir.",
    """
Xavfsiz xabar: Bugungi so'rovlar limiti tugadi. Iltimos, keyinroq urinib ko'ring.
"""
)

# 983
add_task(
    983,
    "AI yaratgan JSON javoblarini qat'iy tekshirib (Schema Validation) o'girish",
    "Model qaytargan JSON matnini kotlinx.serialization orqali aniq Kotlin sinfiga o'tkazish va xatolikni ushlash.",
    """
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
    val goodJson = "{\\"title\\":\\"Jamoaviy miting\\",\\"date\\":\\"2026-07-01\\",\\"durationMinutes\\":45}"
    val event = parseAiEvent(goodJson)
    println("Tadbir aniqlandi: ${event?.title} (${event?.durationMinutes} daqiqa)")
}
""",
    "LLM lar har doim ham mukammal JSON qaytarmasligi mumkin. Shuning uchun xavfsiz deserializatsiya va sxema tekshiruvi shart.",
    """
Tadbir aniqlandi: Jamoaviy miting (45 daqiqa)
"""
)

# 984
add_task(
    984,
    "Mobil AI Kesh: avval so'ralgan savollarni Room bazasida keshlab trafikni tejash",
    "Bir xil savol qayta berilganda serverga murojaat qilmasdan lokal bazadagi javobni darhol qaytaruvchi kesh mexanizmi.",
    """
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
""",
    "AI kesh tizimi foydalanuvchi trafigini, mobil batareya quvvatini va qimmatli API tokenlarini sezilarli darajada tejaydi.",
    """
[SERVER]: AI serverga so'rov yuborildi
[KESH]: Javob xotiradan berildi
Natija: 3 milliondan ortiq
"""
)

# 985
add_task(
    985,
    "Multimodal AI: Rasm baytlarini (Base64) LLM ga tahlil uchun jo'natish",
    "Kamera yoki galereyadagi rasm baytlarini Base64 matniga o'girib, ko'rish (vision) modeliga yuboruvchi ma'lumotlar modeli.",
    """
data class ImagePart(val mimeType: String, val base64Data: String)
data class MultimodalPrompt(val text: String, val images: List<ImagePart>)

fun main() {
    val prompt = MultimodalPrompt(
        text = "Ushbu chekdagi umumiy summani hisoblab ber",
        images = listOf(ImagePart("image/jpeg", "iVBORw0KGgoAAAANSUhEUg..."))
    )
    println("Multimodal so'rov tayyor: matn='${prompt.text}', rasmlar soni=${prompt.images.size}")
}
""",
    "Multimodal modellar nafaqat matn, balki tasvir, hujjat skaneri va audio fayllarni tahlil qilish imkoniyatini beradi.",
    """
Multimodal so'rov tayyor: matn='Ushbu chekdagi umumiy summani hisoblab ber', rasmlar soni=1
"""
)

# 986
add_task(
    986,
    "MVI arxitekturasida AiChatIntent boshqaruvi",
    "Foydalanuvchining xabar yuborish, suhbatni tozalash va qayta generatsiya qilish amallarini Intent orqali boshqarish.",
    """
sealed interface AiChatIntent {
    data class SendUserMessage(val text: String) : AiChatIntent
    object ClearChatHistory : AiChatIntent
    object RetryLastMessage : AiChatIntent
}

fun main() {
    val intent: AiChatIntent = AiChatIntent.SendUserMessage("Assalomu alaykum!")
    println("Yuborilgan intent turi: ${intent.javaClass.simpleName}")
}
""",
    "MVI Intent lari UI komponentlaridan biznes mantiqqa yuboriladigan aniq buyruqlarni ifodalaydi.",
    """
Yuborilgan intent turi: SendUserMessage
"""
)

# 987
add_task(
    987,
    "Mobil agent xavfsizlik filtri: Xavfli buyruqlarni to'sish (Guardrails)",
    "Foydalanuvchi yoki sun'iy intellekt tomonidan tizimga zarar yetkazuvchi xavfli buyruqlar yuborilishini to'suvchi xavfsizlik tekshiruvini yozing.",
    """
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
""",
    "Mobil AI agentlarga tizim resurslariga kirish huquqi berilganda, xavfsizlik filtri (Guardrails) har qanday zararli operatsiyani zudlik bilan to'xtatishi shart.",
    """
Buyruq 1 xavfsizmi: true
Buyruq 2 xavfsizmi: false
"""
)

# 988
add_task(
    988,
    "Background WorkManager orqali har kuni ertalab kundalik xulosani AI bilan tayyorlash",
    "WorkManager ning davriy vazifasi (PeriodicWorkRequest) orqali tonggi soat 8:00 da AI kunlik rejani generatsiya qilishini loyihalash.",
    """
fun main() {
    println("Davriy AI xulosa xizmati:")
    println("val dailySummaryRequest = PeriodicWorkRequestBuilder<AiSummaryWorker>(24, TimeUnit.HOURS)")
    println("    .setConstraints(Constraints.Builder().setRequiredNetworkType(NetworkType.CONNECTED).build())")
    println("    .build()")
}
""",
    "WorkManager hatto foydalanuvchi ilovani ochmagan bo'lsa ham foni sinxronizatsiya qilib, ertalab bildirishnoma (Push Notification) orqali xulosani taqdim etadi.",
    """
Davriy AI xulosa xizmati:
val dailySummaryRequest = PeriodicWorkRequestBuilder<AiSummaryWorker>(24, TimeUnit.HOURS)
    .setConstraints(Constraints.Builder().setRequiredNetworkType(NetworkType.CONNECTED).build())
    .build()
"""
)

# 989
add_task(
    989,
    "Ktor WebSockets orqali AI Agent bilan ikki tomonlama tezkor muloqot",
    "Oddiy HTTP so'rovlariga qaraganda ancha tezkor va kam kechikishli doimiy WebSocket kanali orqali audio/token almashish.",
    """
fun main() {
    println("Ktor WebSocket mijoz ulanishi:")
    println("client.webSocket(\"wss://ai-agent.live/stream\") {")
    println("    send(Frame.Text(\"Jonli savol\"))")
    println("    for (frame in incoming) {")
    println("        if (frame is Frame.Text) println(frame.readText())")
    println("    }")
    println("}")
}
""",
    "WebSockets orqali jonli ikki tomonlama audio yoki real-time token almashinuvi minimal kechikish (low latency) bilan amalga oshadi.",
    """
Ktor WebSocket mijoz ulanishi:
client.webSocket("wss://ai-agent.live/stream") {
    send(Frame.Text("Jonli savol"))
    for (frame in incoming) {
        if (frame is Frame.Text) println(frame.readText())
    }
}
"""
)

# 990
add_task(
    990,
    "AI javobidagi Markdown formatini Jetpack Compose da ko'rsatish",
    "Qalin harflar (**matn**), kod bloklari (`kod`) va ro'yxatlarni to'g'ri render qilish arxitekturasi.",
    """
fun main() {
    println("Compose da AI Markdown rendering:")
    println("- Matn ichidagi **qalin** so'zlar AnnotatedString orqali bo'yaladi")
    println("- Kod bloklari maxsus monospaced shrift va fon bilan Card ichiga olinadi")
}
""",
    "AnnotatedString va Compose RichText kutubxonalari sun'iy intellekt yozgan texnik javoblarni juda chiroyli formatda taqdim etish imkonini beradi.",
    """
Compose da AI Markdown rendering:
- Matn ichidagi **qalin** so'zlar AnnotatedString orqali bo'yaladi
- Kod bloklari maxsus monospaced shrift va fon bilan Card ichiga olinadi
"""
)

# 991
add_task(
    991,
    "Mobil resurslar (batareya va harorat) ga qarab AI so'rovlarini adaptiv boshqarish",
    "Agar batareya quvvati 15% dan kam bo'lsa, og'ir multimodal so'rovlarni cheklab faqat yengil matn rejimiga o'tish.",
    """
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
""",
    "Moslashuvchan (Adaptive) siyosat mobil qurilmaning qizib ketishini va batareyasi tez tugab qolishini oldini oladi.",
    """
15% quvvatda model: gemini-nano-light (Energiya tejovchi rejim)
85% quvvatda model: gemini-pro-cloud (To'liq quvvatli rejim)
"""
)

# 992
add_task(
    992,
    "Clean Architecture: Domain, Data va UI bog'lanishining to'liq zanjiri",
    "UseCase -> Repository -> DataSource -> ViewModel -> Compose UI zanjirini to'liq ko'rsatuvchi arxitektura namunasi.",
    """
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
""",
    "Ushbu toza zanjir har bir qatlamning mustaqilligini, test qilinishini va kengaytirilishini kafolatlaydi.",
    """
Zanjir yakuni: Salom, Antigravity dunyosi!
"""
)

# 993
add_task(
    993,
    "Jetpack Compose da AI Chat Bubble UI komponenti",
    "Foydalanuvchi (o'ngda yashil) va AI (chapda kulrang) xabarlari pufakchalarini (chat bubbles) yasang.",
    """
fun main() {
    println("Compose Chat Bubble dizayni:")
    println("Row(horizontalArrangement = if (isUser) End else Start) {")
    println("    Card(colors = if (isUser) Primary else SurfaceVariant) {")
    println("        Text(message.content)")
    println("    }")
    println("}")
}
""",
    "Composable pufakchalar Row va Alignment yordamida dinamik joylashadi va har ikki tomon xabarlarini ajratadi.",
    """
Compose Chat Bubble dizayni:
Row(horizontalArrangement = if (isUser) End else Start) {
    Card(colors = if (isUser) Primary else SurfaceVariant) {
        Text(message.content)
    }
}
"""
)

# 994
add_task(
    994,
    "Mobil AI Agent testlash: Mock UseCase va Unit Testlar",
    "Biznes mantiqni haqiqiy tarmoq so'rovisiz testlovchi soxta (Mock) UseCase yozing.",
    """
class MockAiUseCase {
    fun execute(prompt: String): String = "Test javobi: $prompt"
}

fun main() {
    val mock = MockAiUseCase()
    val result = mock.execute("Salom")
    println("Unit test muvaffaqiyatli: ${result == "Test javobi: Salom"}")
}
""",
    "Clean Architecture tufayli barcha qatlamlar izolyatsiya qilingan va hech qanday haqiqiy API puli sarflanmasdan 100% test qilinadi.",
    """
Unit test muvaffaqiyatli: true
"""
)

# 995
add_task(
    995,
    "AI Agent javobini xotiraga nusxalash (Clipboard Manager)",
    "Foydalanuvchi AI javobini bitta tugma bilan telefon xotirasiga (clipboard) ko'chirib olishi.",
    """
fun main() {
    println("LocalClipboardManager orqali matn nusxalash:")
    println("val clipboardManager = LocalClipboardManager.current")
    println("clipboardManager.setText(AnnotatedString(aiText))")
}
""",
    "LocalClipboardManager Compose da tizim buferi bilan xavfsiz muloqot qiladi.",
    """
LocalClipboardManager orqali matn nusxalash:
val clipboardManager = LocalClipboardManager.current
clipboardManager.setText(AnnotatedString(aiText))
"""
)

# 996
add_task(
    996,
    "AI Xabarlar ro'yxatida avtomatik pastga skroll qilish (LazyListState.animateScrollToItem)",
    "Yangi token yoki xabar kelishi bilan ro'yxatni avtomatik ravishda eng pastiga surib turuvchi Compose yechimi.",
    """
fun main() {
    println("Avtomatik skroll mexanizmi:")
    println("val listState = rememberLazyListState()")
    println("LaunchedEffect(messages.size) {")
    println("    listState.animateScrollToItem(messages.size - 1)")
    println("}")
}
""",
    "LaunchedEffect messages.size ga bog'langan bo'lib, har bir yangi xabarda oxirgi elementga silliq surib beradi.",
    """
Avtomatik skroll mexanizmi:
val listState = rememberLazyListState()
LaunchedEffect(messages.size) {
    listState.animateScrollToItem(messages.size - 1)
}
"""
)

# 997
add_task(
    997,
    "KMP va Compose Multiplatform: Bir xil UI ni Android va iOS da yurgazish",
    "Compose Multiplatform orqali bir xil yozilgan Composable kodini ikkala operatsion tizimda ham ishlatish tushuntirishi.",
    """
fun main() {
    println("Compose Multiplatform (CMP):")
    println("- Android da: Jetpack Compose")
    println("- iOS da: Skia / Metal orqali to'g'ridan-to'g'ri render")
    println("- 100% bir xil Kotlin UI kodi")
}
""",
    "JetBrains Compose Multiplatform barcha platformalarda bir xil deklarativ kod yozish va umumiy UI yaratish imkonini beradi.",
    """
Compose Multiplatform (CMP):
- Android da: Jetpack Compose
- iOS da: Skia / Metal orqali to'g'ridan-to'g'ri render
- 100% bir xil Kotlin UI kodi
"""
)

# 998
add_task(
    998,
    "Kotlin 2.0 K2 kompilyatori va Compose Compiler integratsiyasi",
    "Kotlin 2.0 da Compose Compiler plaginining to'g'ridan-to'g'ri Kotlin omboriga birlashtirilishi va uning afzalliklari.",
    """
fun main() {
    println("Kotlin 2.0 K2 Compilator va Compose:")
    println("1. Compose Compiler endi alohida emas, Kotlin 2.0+ tarkibiga kiritilgan")
    println("2. Yangi FIR (Frontend Intermediate Representation) orqali kompilyatsiya tezligi 2 barobar oshgan")
    println("3. Barqarorlik (Strong Skipping Mode) avtomatik yoqilgan")
}
""",
    "K2 kompilyatori Compose kodini ancha tezroq tekshiradi va Strong Skipping Mode tufayli barqaror bo'lmagan parametrlar uchun ham ortiqcha qayta chizilishlarni oldini oladi.",
    """
Kotlin 2.0 K2 Compilator va Compose:
1. Compose Compiler endi alohida emas, Kotlin 2.0+ tarkibiga kiritilgan
2. Yangi FIR (Frontend Intermediate Representation) orqali kompilyatsiya tezligi 2 barobar oshgan
3. Barqarorlik (Strong Skipping Mode) avtomatik yoqilgan
"""
)

# 999
add_task(
    999,
    "Mobil AI Agentning to'liq arxitektura diagrammasi va konveyeri",
    "Foydalanuvchi ovozidan boshlab, LLM tahlili, Tool chaqiruvi va yakuniy UI yangilanishigacha bo'lgan to'liq konveyerni sintez qilish.",
    """
fun main() {
    println("Mobil AI Agent to'liq konveyeri:")
    println("[Foydalanuvchi] -> UI Intent -> ViewModel")
    println("               -> Local RAG (Room DB)")
    println("               -> Guardrails (Xavfsizlik)")
    println("               -> Ktor Client (Token Streaming)")
    println("               -> Tool Execution (Agar buyruq bo'lsa)")
    println("               -> StateFlow (Typewriter) -> Jetpack Compose UI")
}
""",
    "Ushbu yaxlit konveyer zamonaviy mobil dasturlashning eng ilg'or cho'qqisi bo'lib, Clean Architecture va zamonaviy sun'iy intellektni birlashtiradi.",
    """
Mobil AI Agent to'liq konveyeri:
[Foydalanuvchi] -> UI Intent -> ViewModel
               -> Local RAG (Room DB)
               -> Guardrails (Xavfsizlik)
               -> Ktor Client (Token Streaming)
               -> Tool Execution (Agar buyruq bo'lsa)
               -> StateFlow (Typewriter) -> Jetpack Compose UI
"""
)

# 1000
add_task(
    1000,
    "1000-Topshiriq: To'liq ishlab turgan Mobil Shaxsiy AI Yordamchisi tizimi",
    "Clean Architecture, Ktor Streaming, StateFlow, Room kesh, Tool Execution va Compose UI ni o'zida birlashtirgan, to'liq ishlovchi 1000-yakuniy grand-loyiha dasturini yarating.",
    """
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
    
    println("\nSuhbat tarixi:")
    viewModel.messages.value.forEach { msg ->
        println("[${msg.sender}]: ${msg.text}")
    }
    
    println("\nTabriklaymiz! 1,000 ta amaliy Kotlin topshirig'i muvaffaqiyatli yakunlandi!")
}
""",
    "Ushbu 1000-yakuniy topshiriqda butun kurs davomida o'rganilgan barcha asosiy tushunchalar: Asosiy tiplar, Null-safety, OOP, Koroutinalar, Flow, Clean Architecture, Ktor streaming va Mobil AI Agent tamoyillari mukammal yakuniy loyihaga birlashtirildi.",
    """
================================================================
  KOTLIN 2.0 TA'LIMIY DATASET: 1000-YAKUNIY TOPSHIRIQ LOYIHASI  
================================================================
Foydalanuvchi so'rovi yuborilmoqda: 'Salom, yordamchi!'

Suhbat tarixi:
[Foydalanuvchi]: Salom, yordamchi!
[AI]: Salom! Men sizning Kotlin 2.0 da yaratilgan shaxsiy mobil AI yordamchingizman. Barcha vazifalar bajarildi!

Tabriklaymiz! 1,000 ta amaliy Kotlin topshirig'i muvaffaqiyatli yakunlandi!
"""
)

save_file("kotlin_20_zamonaviy_android_va_ai_agent_mobile.md", tasks)
