# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(r"C:\Users\User\Desktop\uzbek_dataset\kodlar\kotlin\_generators")
from task_builder import format_task, save_file

tasks = []

def add_task(num, title, cond, code, exp, res):
    tasks.append(format_task(num, title, cond, code, exp, res))

# 901
add_task(
    901,
    "Birinchi @Composable funksiya va Text vidjeti",
    "Jetpack Compose ning deklarativ UI asosini tushuntiruvchi birinchi @Composable funksiyasini yozing va unda ekranga matn chiqaring.",
    """
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun Greeting(name: String) {
    Text(text = "Assalomu alaykum, $name!")
}

fun main() {
    println("Jetpack Compose deklarativ UI funksiyasi e'lon qilindi: Greeting")
    println("Composable funksiyalar UI daraxtini deklarativ kod orqali ifodalaydi.")
}
""",
    "@Composable annotatsiyasi Kotlin kompilyatori plaginiga (Compose Compiler) bu funksiya UI elementlarini chizish uchun mo'ljallanganligini bildiradi. U hech narsa qaytarmaydi (Unit), balki UI grafigini shakllantiradi.",
    """
Jetpack Compose deklarativ UI funksiyasi e'lon qilindi: Greeting
Composable funksiyalar UI daraxtini deklarativ kod orqali ifodalaydi.
"""
)

# 902
add_task(
    902,
    "Column yordamida elementlarni vertikal tartiblash",
    "Bir nechta matn elementini ustma-ust (vertikal) joylashtiruvchi Column tartibini yarating.",
    """
import androidx.compose.foundation.layout.Column
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun UserInfoColumn(name: String, role: String) {
    Column {
        Text(text = "Foydalanuvchi: $name")
        Text(text = "Lavozim: $role")
    }
}

fun main() {
    println("Column: Elementlar yuqoridan pastga qarab vertikal tartiblanadi.")
}
""",
    "Column layout konteyneri ichidagi barcha bolalar Composable elementlarini vertikal o'q bo'ylab ketma-ket joylashtiradi.",
    """
Column: Elementlar yuqoridan pastga qarab vertikal tartiblanadi.
"""
)

# 903
add_task(
    903,
    "Row yordamida elementlarni gorizontal joylashtirish",
    "Belgi va matnni yonma-yon (gorizontal) joylashtirish uchun Row konteyneridan foydalaning.",
    """
import androidx.compose.foundation.layout.Row
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun StatusRow(status: String) {
    Row {
        Text(text = "[*] ")
        Text(text = "Holat: $status")
    }
}

fun main() {
    println("Row: Elementlar chapdan o'ngga gorizontal joylashadi.")
}
""",
    "Row konteyneri barcha elementlarni gorizontal qatorda joylashtiradi va qator ichidagi elementlar oralig'ini sozlash imkonini beradi.",
    """
Row: Elementlar chapdan o'ngga gorizontal joylashadi.
"""
)

# 904
add_task(
    904,
    "Box yordamida elementlarni ustma-ust (overlay) joylashtirish",
    "Elementlarni bir-birining ustiga (masalan orqa fon rasmi ustiga matn) qatlamlab joylashtiruvchi Box konteynerini yozing.",
    """
import androidx.compose.foundation.layout.Box
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun BadgeBox() {
    Box {
        Text(text = "Asosiy Karta")
        Text(text = "Yangi!") // Ustki qatlam
    }
}

fun main() {
    println("Box: Elementlar Z o'qi bo'yicha ustma-ust qatlamlanadi.")
}
""",
    "Box konteyneri FrameLayout kabi ishlaydi, unda elementlar bir-birining ustiga qo'yiladi va alignment orqali burchaklarga taqsimlanadi.",
    """
Box: Elementlar Z o'qi bo'yicha ustma-ust qatlamlanadi.
"""
)

# 905
add_task(
    905,
    "Modifier.fillMaxSize() va Modifier.padding() bilan joylashuvni sozlash",
    "Ekran o'lchamini to'liq egallash va ichki chekinish (padding) berish uchun Modifiyerlardan foydalaning.",
    """
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun ScreenContainer() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(text = "Butun ekranni egallagan va 16dp chekinishga ega blok")
    }
}

fun main() {
    println("Modifier zanjiri elementning ko'rinishi va o'lchamlarini belgilaydi.")
}
""",
    "Modifier - bu Jetpack Compose dagi elementlarning xulq-atvori, hajmi, foni va chekinishlarini tartibga soluvchi asosiy mexanizmdir. Zanjir tartibi juda muhim.",
    """
Modifier zanjiri elementning ko'rinishi va o'lchamlarini belgilaydi.
"""
)

# 906
add_task(
    906,
    "Modifier.background() va clip(RoundedCornerShape) bilan burchaklarni yaxlitlash",
    "Vidjetga rangli fon va yumaloqlangan burchaklar beruvchi Composable tuzing.",
    """
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.runtime.Composable

@Composable
fun RoundedColorCard() {
    Box(
        modifier = Modifier
            .size(100.dp)
            .clip(RoundedCornerShape(12.dp))
            .background(Color.Blue)
    )
}

fun main() {
    println("clip va background kombinatsiyasi burchaklari yumaloq blok hosil qiladi.")
}
""",
    "clip(RoundedCornerShape) shaklni kesib beradi, undan keyin berilgan background esa faqat shu kesilgan hududni bo'yab beradi.",
    """
clip va background kombinatsiyasi burchaklari yumaloq blok hosil qiladi.
"""
)

# 907
add_task(
    907,
    "Modifier.clickable { } yordamida bosish hodisasini qo'shish",
    "Ixtiyoriy matn yoki kartochkani bosiladigan (clickable) qilib, bosilganda xabar chiqaruvchi kod yozing.",
    """
import androidx.compose.foundation.clickable
import androidx.compose.material3.Text
import androidx.compose.ui.Modifier
import androidx.compose.runtime.Composable

@Composable
fun ClickableItem(title: String, onClick: () -> Unit) {
    Text(
        text = title,
        modifier = Modifier.clickable { onClick() }
    )
}

fun main() {
    println("Modifier.clickable har qanday Composable elementga bosish xususiyatini beradi.")
}
""",
    "Modifier.clickable nafaqat bosish hodisasini tinglaydi, balki avtomatik ravishda Material Ripple (to'lqinli bosilish effekti) va accessibility yordamchilarini ham ulaydi.",
    """
Modifier.clickable har qanday Composable elementga bosish xususiyatini beradi.
"""
)

# 908
add_task(
    908,
    "mutableStateOf va remember yordamida hisoblagich holatini saqlash",
    "Tugma har gal bosilganda oshib boruvchi va UI ni yangilovchi Reaktiv hisoblagich (Counter) yarating.",
    """
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue

@Composable
fun SimpleCounter() {
    var count by remember { mutableStateOf(0) }
    
    Button(onClick = { count++ }) {
        Text(text = "Bosildi: $count marta")
    }
}

fun main() {
    println("remember qayta chizilishda (recomposition) qiymatni xotirada saqlab qoladi.")
}
""",
    "mutableStateOf Compose kuzatuv tizimiga yangilanish signallarini beradi. remember esa funksiya qayta chaqirilganda holat nollanib ketmasligini ta'minlaydi.",
    """
remember qayta chizilishda (recomposition) qiymatni xotirada saqlab qoladi.
"""
)

# 909
add_task(
    909,
    "Recomposition mexanizmi va uning aqlli filtri (Smart Recomposition)",
    "Faqat o'zgargan qiymatga bog'liq bo'lgan Composable qismlarigina qayta chizilishini tushuntiruvchi misol keltiring.",
    """
import androidx.compose.foundation.layout.Column
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember

@Composable
fun SmartRecompositionDemo() {
    val count = remember { mutableStateOf(0) }
    
    Column {
        println("Doimiy qism: faqat dastlab chiziladi")
        Text(text = "Statik sarlavha")
        
        Button(onClick = { count.value++ }) {
            Text(text = "Qiymat: ${count.value}") // Faqat shu qism recomposition bo'ladi
        }
    }
}

fun main() {
    println("Compose aqlli: butun ekranni emas, faqat o'zgargan vidjetni qayta chizadi.")
}
""",
    "Recomposition (qayta chizilish) holat (State) o'zgarganda sodir bo'ladi. Compose faqat qiymati o'zgargan Composable tugunlarini yangilaydi (Smart Recomposition).",
    """
Compose aqlli: butun ekranni emas, faqat o'zgargan vidjetni qayta chizadi.
"""
)

# 910
add_task(
    910,
    "rememberSaveable yordamida ekran burilganda holatni yo'qotmaslik",
    "Oddiy remember bilan rememberSaveable o'rtasidagi farqni va ekran holatini (Configuration change) saqlashni namoyish eting.",
    """
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue

@Composable
fun PersistentSearchInput() {
    var query by rememberSaveable { mutableStateOf("") }
    
    TextField(
        value = query,
        onValueChange = { query = it }
    )
}

fun main() {
    println("rememberSaveable: Ekran burilganda (rotate) yoki jarayon o'ldirilganda ham holatni saqlab qoladi.")
}
""",
    "remember faqat recomposition vaqtida xotirani saqlaydi, Activity qayta yaratilsa (masalan til yoki ekran burilishi) ma'lumot o'chib ketadi. rememberSaveable esa Bundle ga saqlab, to'liq tiklaydi.",
    """
rememberSaveable: Ekran burilganda (rotate) yoki jarayon o'ldirilganda ham holatni saqlab qoladi.
"""
)

# 911
add_task(
    911,
    "TextField va OutlinedTextField orqali matn kiritish",
    "Foydalanuvchi kiritgan matnni o'zida aks ettiruvchi va boshqaruvchi (controlled component) TextField yarating.",
    """
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue

@Composable
fun UserInputField() {
    var text by remember { mutableStateOf("") }
    
    OutlinedTextField(
        value = text,
        onValueChange = { newText -> text = newText },
        label = { Text("Ismingizni kiriting") }
    )
}

fun main() {
    println("Controlled TextField: qiymat doimo Kotlin State o'zgaruvchisidan olinadi.")
}
""",
    "Compose dagi TextField odatda 'boshqariladigan' (controlled) komponent hisoblanadi: kiritilgan belgi onValueChange orqali State ga yoziladi va qayta value ga beriladi.",
    """
Controlled TextField: qiymat doimo Kotlin State o'zgaruvchisidan olinadi.
"""
)

# 912
add_task(
    912,
    "State Hoisting (holatni ajratish): Stateless vs Stateful",
    "Komponentni qayta ishlatiluvchi (reusable) va test qilish oson bo'lishi uchun State Hoisting qoidasiga ko'ra holatni tashqariga chiqaring.",
    """
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

// 1. Stateless (Holatsiz) - faqat parametr oladi, qayta ishlatish oson
@Composable
fun CounterButton(count: Int, onIncrement: () -> Unit) {
    Button(onClick = onIncrement) {
        Text("Hisob: $count")
    }
}

fun main() {
    println("State Hoisting: Holatni yuqoriga (caller ga) ko'tarish, UI ni esa sof render qiluvchi qilish.")
}
""",
    "State Hoisting arxitekturasida komponent ichida state saqlanmaydi, balki `value` va `onValueChange` parametrlari orqali tashqaridan boshqariladi. Bu testlashni osonlashtiradi.",
    """
State Hoisting: Holatni yuqoriga (caller ga) ko'tarish, UI ni esa sof render qiluvchi qilish.
"""
)

# 913
add_task(
    913,
    "Shartli UI: if (isLoggedIn) orqali ekran ko'rinishini almashtirish",
    "Foydalanuvchi tizimga kirgan yoki kirmaganligiga qarab boshqa-boshqa UI qismlarini chizuvchi shartli Composable yozing.",
    """
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun ConditionalScreen(isLoggedIn: Boolean, userName: String) {
    if (isLoggedIn) {
        Text("Xush kelibsiz, $userName!")
    } else {
        Text("Iltimos, avval tizimga kiring.")
    }
}

fun main() {
    println("Compose da shartli render oddiy Kotlin `if-else` yoki `when` orqali ifodalanadi.")
}
""",
    "XML da visibility = GONE/VISIBLE o'rniga Compose da oddiy Kotlin `if-else` shartlari ishlatiladi. Shart bajarilmasa, o'sha Composable umuman UI daraxtiga qo'shilmaydi.",
    """
Compose da shartli render oddiy Kotlin `if-else` yoki `when` orqali ifodalanadi.
"""
)

# 914
add_task(
    914,
    "LazyColumn yordamida minglab elementlarni samarali ro'yxatda ko'rsatish",
    "Android dagi RecyclerView o'rnini bosuvchi, faqat ekranda ko'rinib turgan elementlarnigina xotiraga oluvchi LazyColumn ni loyihalang.",
    """
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun SimpleLazyList(names: List<String>) {
    LazyColumn {
        items(names) { name ->
            Text(text = "Ism: $name")
        }
    }
}

fun main() {
    println("LazyColumn faqat ekrandagi ko'rinib turgan elementlarni chizadi (Recycling).")
}
""",
    "LazyColumn an'anaviy RecyclerView ning barcha afzalliklarini bitta qulay deklarativ blokda taqdim etadi: adapter yoki viewHolder yaratish talab etilmaydi.",
    """
LazyColumn faqat ekrandagi ko'rinib turgan elementlarni chizadi (Recycling).
"""
)

# 915
add_task(
    915,
    "LazyColumn da items(key = { it.id }) parametrining o'rni",
    "Ro'yxat elementlari qo'shilganda yoki saralanganda keraksiz qayta chizilishlarni oldini olish uchun barqaror kalit (key) bering.",
    """
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

data class Contact(val id: Int, val name: String)

@Composable
fun OptimizedContactList(contacts: List<Contact>) {
    LazyColumn {
        items(
            items = contacts,
            key = { contact -> contact.id } // Noyob kalit
        ) { contact ->
            Text(text = "${contact.id}: ${contact.name}")
        }
    }
}

fun main() {
    println("key parametri elementlar almashganda holatni va animatsiyalarni to'g'ri saqlaydi.")
}
""",
    "key berilganda Compose elementlarni pozitsiyasi (indeksi) bo'yicha emas, aynan shu noyob kalit bo'yicha taniydi, bu esa ro'yxat tartibi o'zgarganda yuqori samaradorlik beradi.",
    """
key parametri elementlar almashganda holatni va animatsiyalarni to'g'ri saqlaydi.
"""
)

# 916
add_task(
    916,
    "LazyRow yordamida gorizontal suriluvchi kartochkalar ro'yxatini yaratish",
    "Gorizontal o'q bo'ylab suriluvchi (horizontal scrolling) toifalar yoki fotogalereya ro'yxatini yozing.",
    """
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun CategoryRow(categories: List<String>) {
    LazyRow {
        items(categories) { category ->
            Card {
                Text(text = category)
            }
        }
    }
}

fun main() {
    println("LazyRow: Gorizontal o'qda dangasa yuklanuvchi ro'yxat.")
}
""",
    "LazyRow gorizontal yo'nalishdagi elementlarni xuddi LazyColumn kabi resurslarni tejagan holda render qiladi.",
    """
LazyRow: Gorizontal o'qda dangasa yuklanuvchi ro'yxat.
"""
)

# 917
add_task(
    917,
    "Card va ElevatedCard vidjetlari bilan soya va qavariq ko'rinish",
    "Material 3 uslubidagi Card vidjetiga soya (elevation) va burchaklar berib chiroyli mahsulot kartasi yasang.",
    """
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ElevatedCard
import androidx.compose.material3.Text
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.runtime.Composable

@Composable
fun ProductCard(title: String, price: String) {
    ElevatedCard(
        elevation = CardDefaults.cardElevation(defaultElevation = 6.dp),
        modifier = Modifier.padding(8.dp)
    ) {
        Text(text = title, modifier = Modifier.padding(8.dp))
        Text(text = price, modifier = Modifier.padding(8.dp))
    }
}

fun main() {
    println("ElevatedCard: Zamonaviy Material Design 3 kartochka komponenti.")
}
""",
    "ElevatedCard chiroyli yorug'lik va soya effekti bilan vizual iyerarxiyani ajratib ko'rsatishga yordam beradi.",
    """
ElevatedCard: Zamonaviy Material Design 3 kartochka komponenti.
"""
)

# 918
add_task(
    918,
    "CircularProgressIndicator va LinearProgressIndicator",
    "Yuklanish jarayonini ko'rsatuvchi aylanma va chiziqli ko'rsatkichlarni Composable da chiqarish.",
    """
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.runtime.Composable

@Composable
fun LoadingStateView(isLoading: Boolean) {
    if (isLoading) {
        CircularProgressIndicator()
        LinearProgressIndicator()
    }
}

fun main() {
    println("Progress indikatorlar foydalanuvchiga jarayon davom etayotganini bildiradi.")
}
""",
    "Progress indikatorlari indeterminate (cheksiz aylanuvchi) yoki progress parametri orqali aniq foiz ko'rsatuvchi holatda ishlatiladi.",
    """
Progress indikatorlar foydalanuvchiga jarayon davom etayotganini bildiradi.
"""
)

# 919
add_task(
    919,
    "Checkbox va Switch komponentlari bilan holatni boshqarish",
    "Sozlamalar ekranidagi bayroqcha (Checkbox) va yoqish/o'chirish tugmachasini (Switch) boshqaring.",
    """
import androidx.compose.material3.Checkbox
import androidx.compose.material3.Switch
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue

@Composable
fun SettingsControls() {
    var isChecked by remember { mutableStateOf(true) }
    var isEnabled by remember { mutableStateOf(false) }
    
    Checkbox(checked = isChecked, onCheckedChange = { isChecked = it })
    Switch(checked = isEnabled, onCheckedChange = { isEnabled = it })
}

fun main() {
    println("Checkbox va Switch: Boolean qiymatlarni interaktiv o'zgartirish.")
}
""",
    "Checkbox va Switch komponentlari o'zlarining checked va onCheckedChange xususiyatlari orqali deklarativ boshqariladi.",
    """
Checkbox va Switch: Boolean qiymatlarni interaktiv o'zgartirish.
"""
)

# 920
add_task(
    920,
    "Slider komponenti bilan qiymatni silliq tanlash",
    "Ovoz balandligi yoki yorug'lik darajasini 0 dan 100 gacha silliq o'zgartiruvchi Slider ni yozing.",
    """
import androidx.compose.material3.Slider
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue

@Composable
fun VolumeSlider() {
    var volume by remember { mutableStateOf(50f) }
    
    Text(text = "Ovoz balandligi: ${volume.toInt()}%")
    Slider(
        value = volume,
        onValueChange = { volume = it },
        valueRange = 0f..100f
    )
}

fun main() {
    println("Slider uzluksiz raqamli diapazonlardan qiymat tanlash imkonini beradi.")
}
""",
    "Slider komponenti berilgan valueRange chegarasida qiymatni silliq Float ko'rinishida yetkazib beradi.",
    """
Slider uzluksiz raqamli diapazonlardan qiymat tanlash imkonini beradi.
"""
)

# 921
add_task(
    921,
    "Scaffold yordamida standart ekran skeletini qurish",
    "Material ekranning sarlavhasi (TopBar), harakat tugmasi (FAB) va asosiy kontentini Scaffold yordamida tartibga soling.",
    """
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier

@Composable
fun MainScreenScaffold() {
    Scaffold(
        topBar = { Text("Mening Ilovam") }
    ) { innerPadding ->
        Text(
            text = "Asosiy ekran kontenti",
            modifier = Modifier.padding(innerPadding)
        )
    }
}

fun main() {
    println("Scaffold Material Design ekranlarining asosiy karkasini tashkil etadi.")
}
""",
    "Scaffold avtomatik ravishda tizim panellari, sarlavha va pastki navigatsiya uchun joy (innerPadding) hisoblab beradi.",
    """
Scaffold Material Design ekranlarining asosiy karkasini tashkil etadi.
"""
)

# 922
add_task(
    922,
    "SnackbarHost orqali pastki xabarnoma chiqarish",
    "rememberSnackbarHostState va coroutineScope orqali foydalanuvchiga vaqtinchalik Snackbar xabarini ko'rsatish.",
    """
import androidx.compose.material3.Button
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import kotlinx.coroutines.launch

@Composable
fun SnackbarExample() {
    val snackbarHostState = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()
    
    Scaffold(
        snackbarHost = { SnackbarHost(snackbarHostState) }
    ) {
        Button(onClick = {
            scope.launch {
                snackbarHostState.showSnackbar("Amal muvaffaqiyatli bajarildi!")
            }
        }) {
            Text("Xabarni ko'rsatish")
        }
    }
}

fun main() {
    println("SnackbarHost zamonaviy asinxron xabarnomalarni chiqarish markazidir.")
}
""",
    "showSnackbar() suspend funksiya bo'lgani uchun uni chaqirishda rememberCoroutineScope() orqali olingan koroutina ko'lami ishlatiladi.",
    """
SnackbarHost zamonaviy asinxron xabarnomalarni chiqarish markazidir.
"""
)

# 923
add_task(
    923,
    "LaunchedEffect yordamida ekran ochilganda bir martalik tarmoq so'rovini boshlash",
    "Composable ekranga birinchi marta kirganda (mount) asinxron ma'lumot yuklashni LaunchedEffect orqali boshlang.",
    """
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.material3.Text
import kotlinx.coroutines.delay

@Composable
fun DataLoaderScreen(userId: Int) {
    LaunchedEffect(userId) {
        println("LaunchedEffect: Foydalanuvchi #$userId ma'lumotlari yuklanmoqda...")
        delay(200L)
        println("LaunchedEffect: Ma'lumot yuklandi!")
    }
    Text("Foydalanuvchi ekrani")
}

fun main() {
    println("LaunchedEffect hayot sikliga bog'liq asinxron Side-Effect larni boshqaradi.")
}
""",
    "LaunchedEffect Composable render bo'lganda yangi koroutina boshlaydi. Agar key (userId) o'zgarsa, eski koroutina bekor qilinib yangisi boshlanadi.",
    """
LaunchedEffect hayot sikliga bog'liq asinxron Side-Effect larni boshqaradi.
"""
)

# 924
add_task(
    924,
    "DisposableEffect yordamida ekrandan chiqib ketilganda resurslarni tozalash",
    "Composable hayot sikli tugaganda (onDispose) sensor yoki tinglovchini o'chiruvchi DisposableEffect ni qo'llang.",
    """
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect

@Composable
fun SensorObserver() {
    DisposableEffect(Unit) {
        println("Sensor tinglovchisi ulandi")
        
        onDispose {
            println("Sensor tinglovchisi to'xtatildi va resurs tozalandi!")
        }
    }
}

fun main() {
    println("DisposableEffect: Resurslarni ulash va onDispose da xavfsiz tozalash.")
}
""",
    "DisposableEffect uning bloki tugaganda yoki Composable ekrandan yo'qolganda `onDispose { }` chaqiruvini bajaradi, bu memory leak larni oldini oladi.",
    """
DisposableEffect: Resurslarni ulash va onDispose da xavfsiz tozalash.
"""
)

# 925
add_task(
    925,
    "derivedStateOf yordamida ortiqcha recomposition larning oldini olish",
    "Tez-tez o'zgaruvchi qiymatdan (masalan skroll pozitsiyasi) faqat natijaviy shart o'zgargandagina qayta chizilishni ta'minlang.",
    """
import androidx.compose.runtime.Composable
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.material3.Text

@Composable
fun ScrollTopButtonDemo() {
    val scrollOffset = remember { mutableStateOf(0) }
    
    // Faqat offset > 100 boolean o'zgargandagina recomposition bo'ladi
    val showButton by remember {
        derivedStateOf { scrollOffset.value > 100 }
    }
    
    Text("Tugma ko'rinadimi: $showButton")
}

fun main() {
    println("derivedStateOf: O'zgarishlar ko'p bo'lganda faqat yakuniy hisoblangan shartni kuzatish.")
}
""",
    "Agar har bir piksel skrollida oddiy state ishlatilsa, butun UI har millisekundda qayta chizilar edi. derivedStateOf faqat natijaviy holat o'zgargandagina recomposition chaqiradi.",
    """
derivedStateOf: O'zgarishlar ko'p bo'lganda faqat yakuniy hisoblangan shartni kuzatish.
"""
)

# 926
add_task(
    926,
    "AnimatedVisibility yordamida elementning paydo bo'lishini animatsiya qilish",
    "Tugma bosilganda matnning silliq kengayib (expand) va qisqarib (shrink) paydo bo'lishini ta'minlang.",
    """
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue

@Composable
fun CollapsibleSection() {
    var visible by remember { mutableStateOf(false) }
    
    Button(onClick = { visible = !visible }) {
        Text("Ko'rsatish/Yashirish")
    }
    
    AnimatedVisibility(visible = visible) {
        Text("Bu matn silliq animatsiya bilan paydo bo'ladi!")
    }
}

fun main() {
    println("AnimatedVisibility deklarativ tarzda UI elementlarini animatsiyalaydi.")
}
""",
    "AnimatedVisibility elementi avtomatik ravishda kirish (fadeIn/expand) va chiqish (fadeOut/shrink) animatsiyalarini ulaydi.",
    """
AnimatedVisibility deklarativ tarzda UI elementlarini animatsiyalaydi.
"""
)

# 927
add_task(
    927,
    "animateColorAsState yordamida ranglar almashinuvini silliq qilish",
    "Tanlangan yoki tanlanmagan holatga qarab fon rangi silliq o'zgaruvchi Composable yozing.",
    """
import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

@Composable
fun AnimatedColorBox() {
    var isSelected by remember { mutableStateOf(false) }
    val animatedBgColor by animateColorAsState(
        targetValue = if (isSelected) Color.Green else Color.Gray
    )
    
    Box(
        modifier = Modifier
            .size(80.dp)
            .background(animatedBgColor)
            .clickable { isSelected = !isSelected }
    )
}

fun main() {
    println("animateColorAsState: Ranglarning keskin emas, silliq o'tishini ta'minlaydi.")
}
""",
    "animate*AsState funksiyalari (color, float, dp, int) berilgan maqsadli qiymatga (targetValue) silliq interpolyatsiya bilan o'tishni amalga oshiradi.",
    """
animateColorAsState: Ranglarning keskin emas, silliq o'tishini ta'minlaydi.
"""
)

# 928
add_task(
    928,
    "Canvas vidjeti yordamida maxsus shakllar va chiziqlar chizish",
    "DrawScope orqali ekranga qizil doira va to'g'ri chiziq chizuvchi maxsus Canvas Composable yozing.",
    """
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

@Composable
fun CustomDrawing() {
    Canvas(modifier = Modifier.size(100.dp)) {
        drawCircle(
            color = Color.Red,
            radius = size.minDimension / 4,
            center = center
        )
        drawLine(
            color = Color.Black,
            start = Offset(0f, 0f),
            end = Offset(size.width, size.height),
            strokeWidth = 4f
        )
    }
}

fun main() {
    println("Canvas DrawScope orqali 2D grafik shakllarni to'g'ridan-to'g'ri chizish imkonini beradi.")
}
""",
    "Canvas Composable vidjeti ichida drawCircle, drawRect, drawLine, drawPath kabi past darajadagi 2D chizish vositalari mavjud.",
    """
Canvas DrawScope orqali 2D grafik shakllarni to'g'ridan-to'g'ri chizish imkonini beradi.
"""
)

# 929
add_task(
    929,
    "AlertDialog yordamida tasdiqlash oynasini ko'rsatish",
    "Foydalanuvchi ma'lumotni o'chirishdan avval 'Ishonchingiz komilmi?' deb so'rovchi AlertDialog tuzing.",
    """
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue

@Composable
fun ConfirmDeleteDialog() {
    var showDialog by remember { mutableStateOf(true) }
    
    if (showDialog) {
        AlertDialog(
            onDismissRequest = { showDialog = false },
            title = { Text("O'chirishni tasdiqlash") },
            text = { Text("Ushbu faylni haqiqatan ham o'chirmoqchimisiz?") },
            confirmButton = {
                TextButton(onClick = { showDialog = false }) { Text("Ha") }
            },
            dismissButton = {
                TextButton(onClick = { showDialog = false }) { Text("Bekor qilish") }
            }
        )
    }
}

fun main() {
    println("AlertDialog: Ekranning markazida tasdiqlovchi modal oyna chiqarish.")
}
""",
    "AlertDialog deklarativdir: agar `showDialog` rost bo'lsa u chiziladi, yolg'on bo'lsa butunlay yo'qoladi.",
    """
AlertDialog: Ekranning markazida tasdiqlovchi modal oyna chiqarish.
"""
)

# 930
add_task(
    930,
    "Slot API yondashuvi bilan moslashuvchan konteyner yaratish",
    "O'z ichiga ixtiyoriy boshqa Composable elementni qabul qila oluvchi (trailing lambda) maxsus sarlavhali panel yarating.",
    """
import androidx.compose.foundation.layout.Column
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun CustomCardSlot(
    title: String,
    content: @Composable () -> Unit // Slot parametri
) {
    Column {
        Text(text = "=== $title ===")
        content() // Ichki kontentni chizish
    }
}

fun main() {
    println("Slot API: Komponentlarga bolalar vidjetlarini erkin joylashtirish imkonini beradi.")
}
""",
    "Slot API Jetpack Compose ning eng kuchli arxitektura qoidalaridan biri bo'lib, uning yordamida Scaffold, TopAppBar kabi moslashuvchan konteynerlar quriladi.",
    """
Slot API: Komponentlarga bolalar vidjetlarini erkin joylashtirish imkonini beradi.
"""
)

# 931
add_task(
    931,
    "MaterialTheme orqali ranglar palitrasi va tipografiyani qo'llash",
    "MaterialTheme.colorScheme va MaterialTheme.typography orqali umumiy dizayn tizimiga rioya qilishni ko'rsating.",
    """
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun ThemedText() {
    Text(
        text = "Mavzuga mos matn",
        color = MaterialTheme.colorScheme.primary,
        style = MaterialTheme.typography.titleLarge
    )
}

fun main() {
    println("MaterialTheme butun ilova bo'ylab yagona rang, shrift va shakllar uslubini ta'minlaydi.")
}
""",
    "MaterialTheme markazlashgan tokenlar tizimidir. Ilova qorong'u rejimga o'tganda `primary` ranglar avtomatik moslashadi.",
    """
MaterialTheme butun ilova bo'ylab yagona rang, shrift va shakllar uslubini ta'minlaydi.
"""
)

# 932
add_task(
    932,
    "Custom Modifier kengaytma funksiyasi yaratish",
    "Kodni qayta-qayta takrorlamaslik uchun bir nechta modifiyerlarni birlashtiruvchi shaxsiy kengaytma yozing.",
    """
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

fun Modifier.standardCardStyle(): Modifier = this
    .clip(RoundedCornerShape(8.dp))
    .background(Color.LightGray)
    .padding(12.dp)

fun main() {
    println("Custom Modifier: Takrorlanuvchi dizayn parametrlarini ixcham kengaytma funksiyaga yig'ish.")
}
""",
    "Modifier ga kengaytma funksiya yozish orqali loyihaning UI kodini toza va o'qilishi oson holatga keltirish mumkin.",
    """
Custom Modifier: Takrorlanuvchi dizayn parametrlarini ixcham kengaytma funksiyaga yig'ish.
"""
)

# 933
add_task(
    933,
    "DropdownMenu va DropdownMenuItem ochiluvchi ro'yxati",
    "Tugma bosilganda pastga qarab ochiluvchi va tanlov qilish imkonini beruvchi DropdownMenu yarating.",
    """
import androidx.compose.foundation.layout.Box
import androidx.compose.material3.Button
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue

@Composable
fun LanguageSelector() {
    var expanded by remember { mutableStateOf(false) }
    var selectedLanguage by remember { mutableStateOf("O'zbek") }
    
    Box {
        Button(onClick = { expanded = true }) {
            Text(selectedLanguage)
        }
        DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
            DropdownMenuItem(text = { Text("O'zbek") }, onClick = { selectedLanguage = "O'zbek"; expanded = false })
            DropdownMenuItem(text = { Text("English") }, onClick = { selectedLanguage = "English"; expanded = false })
        }
    }
}

fun main() {
    println("DropdownMenu: Tanlov menyularini chiqarish uchun qulay komponent.")
}
""",
    "DropdownMenu o'zining expanded holati orqali ko'rinadi va foydalanuvchi variantlardan birini bosishi bilan yopiladi.",
    """
DropdownMenu: Tanlov menyularini chiqarish uchun qulay komponent.
"""
)

# 934
add_task(
    934,
    "LazyVerticalGrid yordamida fotogalereya yoki mahsulotlar to'rini (Grid) qurish",
    "2 ustunli jadval shaklida elementlarni taqsimlovchi LazyVerticalGrid ni yozing.",
    """
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun PhotoGrid(photos: List<String>) {
    LazyVerticalGrid(
        columns = GridCells.Fixed(2)
    ) {
        items(photos) { photo ->
            Text(text = "Rasm: $photo")
        }
    }
}

fun main() {
    println("LazyVerticalGrid: Ko'p ustunli to'r (Grid) ko'rinishida elementlarni ko'rsatish.")
}
""",
    "GridCells.Fixed(2) har bir qatorda teng ikkita ustun hosil qiladi va elementlarni avtomatik taqsimlaydi.",
    """
LazyVerticalGrid: Ko'p ustunli to'r (Grid) ko'rinishida elementlarni ko'rsatish.
"""
)

# 935
add_task(
    935,
    "CompositionLocalProvider orqali chuqur parametr uzatish",
    "Har bir Composable ga alohida argument uzatmasdan, daraxt bo'ylab ma'lumot tarqatuvchi CompositionLocal mexanizmini tushuntiring.",
    """
import androidx.compose.runtime.Composable
import androidx.compose.runtime.compositionLocalOf
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.material3.Text

val LocalAppRole = compositionLocalOf { "Guest" }

@Composable
fun DeepChildComponent() {
    val role = LocalAppRole.current
    Text("Joriy rol: $role")
}

@Composable
fun RootContainer() {
    CompositionLocalProvider(LocalAppRole provides "Admin") {
        DeepChildComponent()
    }
}

fun main() {
    println("CompositionLocal: Parametrlarni har bir funksiyaga qo'lda uzatish muammosini hal qiladi.")
}
""",
    "LocalContext, LocalDensity va LocalContentColor kabi barcha standart Compose vositalari aynan CompositionLocal orqali ishlaydi.",
    """
CompositionLocal: Parametrlarni har bir funksiyaga qo'lda uzatish muammosini hal qiladi.
"""
)

# 936
add_task(
    936,
    "snapshotFlow yordamida Compose State ni Kotlin Flow ga aylantirish",
    "Compose State qiymatini Coroutine Flow sifatida kuzatib, unda debounce yoki filter operatorlarini ishlatish.",
    """
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.snapshotFlow
import kotlinx.coroutines.flow.filter

@Composable
fun StateToFlowObserver() {
    val searchState = remember { mutableStateOf("") }
    
    LaunchedEffect(Unit) {
        snapshotFlow { searchState.value }
            .filter { it.length > 3 }
            .collect { query ->
                println("Qidiruv so'rovi yuborildi: $query")
            }
    }
}

fun main() {
    println("snapshotFlow: Compose xotirasidagi o'zgarishlarni reaktiv Flow ga aylantiradi.")
}
""",
    "snapshotFlow Compose State va Coroutine Flow dunyolarini birlashtiruvchi rasmiy ko'prikdir.",
    """
snapshotFlow: Compose xotirasidagi o'zgarishlarni reaktiv Flow ga aylantiradi.
"""
)

# 937
add_task(
    937,
    "animateFloatAsState yordamida shaffoflikni (alpha) animatsiya qilish",
    "Tugma bosilganda elementning paydo bo'lishini shaffoflik (alpha) o'zgarishi orqali animatsiyalang.",
    """
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha

@Composable
fun FadingText(isVisible: Boolean) {
    val alpha by animateFloatAsState(targetValue = if (isVisible) 1f else 0.2f)
    
    Text(
        text = "Yumshoq o'zgaruvchi matn",
        modifier = Modifier.alpha(alpha)
    )
}

fun main() {
    println("animateFloatAsState: Float o'zgaruvchilarni animatsiya qilish vositasi.")
}
""",
    "Modifier.alpha(alpha) parametri elementning shaffofligini o'zgartiradi va silliq fade effektini hosil qiladi.",
    """
animateFloatAsState: Float o'zgaruvchilarni animatsiya qilish vositasi.
"""
)

# 938
add_task(
    938,
    "Modifier.border() va gradient fon (Brush.horizontalGradient)",
    "Vidjetga rangli gradient hoshiya va fon berishni amalga oshiring.",
    """
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

@Composable
fun GradientCircle() {
    val gradient = Brush.horizontalGradient(listOf(Color.Magenta, Color.Cyan))
    
    Box(
        modifier = Modifier
            .size(60.dp)
            .border(2.dp, gradient, CircleShape)
            .background(Color.White, CircleShape)
    )
}

fun main() {
    println("Brush.horizontalGradient yordamida zamonaviy gradient vizuallari yaratiladi.")
}
""",
    "Brush sinfi chiziqli, radial yoki sweep gradientlarini yasab, ularni border yoki background ga uzatish imkonini beradi.",
    """
Brush.horizontalGradient yordamida zamonaviy gradient vizuallari yaratiladi.
"""
)

# 939
add_task(
    939,
    "Shaxsiy UserProfileCard Composable vidjetini yaratish",
    "Foydalanuvchi rasmi, ismi, kasbi va obuna tugmasini o'z ichiga olgan mustaqil komponent loyihalang.",
    """
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun UserProfileCard(name: String, job: String, onFollow: () -> Unit) {
    Card(modifier = Modifier.padding(8.dp)) {
        Row(modifier = Modifier.padding(16.dp)) {
            Column(modifier = Modifier.weight(1f)) {
                Text(text = name)
                Text(text = job)
            }
            Button(onClick = onFollow) {
                Text("Obuna")
            }
        }
    }
}

fun main() {
    println("UserProfileCard: Modulli, toza va mustaqil Compose komponenti.")
}
""",
    "Mustaqil Composable komponentlar yaratish orqali butun ilova arxitekturasi g'ishtdek yig'iladi va toza bo'ladi.",
    """
UserProfileCard: Modulli, toza va mustaqil Compose komponenti.
"""
)

# 940
add_task(
    940,
    "rememberCoroutineScope orqali foydalanuvchi amallarida koroutina ishga tushirish",
    "Tugma onClick hodisasida tarmoqqa asinxron ma'lumot yuborish uchun rememberCoroutineScope dan foydalaning.",
    """
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.rememberCoroutineScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

@Composable
fun AsyncSubmitButton() {
    val scope = rememberCoroutineScope()
    
    Button(onClick = {
        scope.launch {
            println("So'rov yuborilmoqda...")
            delay(300L)
            println("Serverdan javob olindi!")
        }
    }) {
        Text("Yuborish")
    }
}

fun main() {
    println("rememberCoroutineScope tugma yoki foydalanuvchi hodisalari ichida koroutina boshlash uchun kerak.")
}
""",
    "Composable funksiyalarning o'zi oddiy funksiya (suspend emas), shuning uchun onClick kabi lambdalarda to'xtatuvchi kod yozish uchun rememberCoroutineScope talab qilinadi.",
    """
rememberCoroutineScope tugma yoki foydalanuvchi hodisalari ichida koroutina boshlash uchun kerak.
"""
)

# 941
add_task(
    941,
    "IconButton va Icon orqali savatcha va bildirishnoma tugmalari",
    "Piktogramma asosidagi tugmalarni (IconButton) yaratish.",
    """
import androidx.compose.material3.IconButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun CartIconButton(onClick: () -> Unit) {
    IconButton(onClick = onClick) {
        Text("[Xarid]")
    }
}

fun main() {
    println("IconButton piktogramma o'lchamlarini Material standartlariga moslaydi.")
}
""",
    "IconButton minimal 48dp o'lchamdagi qulay bosish maydonini ta'minlaydi va to'lqin effektini beradi.",
    """
IconButton piktogramma o'lchamlarini Material standartlariga moslaydi.
"""
)

# 942
add_task(
    942,
    "RadioGroup va RadioButton guruhi yaratish",
    "Foydalanuvchiga to'lov turini tanlash imkonini beruvchi yagona tanlovli (Single Choice) radio guruh tuzing.",
    """
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.material3.RadioButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue

@Composable
fun PaymentMethodSelector() {
    val methods = listOf("UzCard", "Humo", "Naqd")
    var selectedMethod by remember { mutableStateOf(methods[0]) }
    
    Column {
        methods.forEach { method ->
            Row {
                RadioButton(
                    selected = (method == selectedMethod),
                    onClick = { selectedMethod = method }
                )
                Text(text = method)
            }
        }
    }
}

fun main() {
    println("RadioButton: Ro'yxatdan faqat bitta variantni tanlash.")
}
""",
    "Radio tugmalari guruhi har bir elementni joriy tanlangan qiymat bilan solishtirish orqali boshqariladi.",
    """
RadioButton: Ro'yxatdan faqat bitta variantni tanlash.
"""
)

# 943
add_task(
    943,
    "TopAppBar bilan harakatlar (actions) va orqaga qaytish tugmasi",
    "Ekran tepasidagi sarlavha panelida orqaga qaytish va qidiruv harakatlari tugmalarini joylashtiring.",
    """
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AppHeader(title: String) {
    TopAppBar(
        title = { Text(title) }
    )
}

fun main() {
    println("TopAppBar: Ekranning standart yuqori navigatsiya paneli.")
}
""",
    "Material 3 TopAppBar navigatsiya ikonkasi, sarlavha va o'ng tarafdagi harakatlar (actions) uchun maxsus slotlarga ega.",
    """
TopAppBar: Ekranning standart yuqori navigatsiya paneli.
"""
)

# 944
add_task(
    944,
    "FloatingActionButton (FAB) orqali yangi yozuv qo'shish tugmasi",
    "Ekranning pastki o'ng burchagida qalqib turuvchi yumaloq harakat tugmasini (FAB) yasang.",
    """
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun AddItemFab(onAdd: () -> Unit) {
    FloatingActionButton(onClick = onAdd) {
        Text("+")
    }
}

fun main() {
    println("FAB ekrandagi asosiy va eng muhim harakatni ifodalaydi.")
}
""",
    "FloatingActionButton Scaffold ning floatingActionButton uyasiga (slotiga) joylashtiriladi va avtomatik joylashuvni oladi.",
    """
FAB ekrandagi asosiy va eng muhim harakatni ifodalaydi.
"""
)

# 945
add_task(
    945,
    "Compose da qorong'u rejimni (isSystemInDarkTheme) tekshirish",
    "Tizim hozir qorong'u (Dark) yoki yorug' (Light) rejimda ekanligini aniqlovchi Compose funksiyasi misoli.",
    """
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun ThemeStatusView() {
    val isDark = isSystemInDarkTheme()
    Text(text = if (isDark) "Qorong'u rejim faol" else "Yorug' rejim faol")
}

fun main() {
    println("isSystemInDarkTheme() tizim sozlamalaridagi tungi rejimni aniqlaydi.")
}
""",
    "isSystemInDarkTheme() reaktiv bo'lib, foydalanuvchi tizim panelidan rejimni almashtirishi bilan darhol UI ni yangilaydi.",
    """
isSystemInDarkTheme() tizim sozlamalaridagi tungi rejimni aniqlaydi.
"""
)

# 946
add_task(
    946,
    "ModalBottomSheet yordamida pastdan chiquvchi panelni ko'rsatish",
    "Ekran pastidan silliq ko'tariluvchi zamonaviy ma'lumotlar panelini (Bottom Sheet) namoyish eting.",
    """
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DetailsBottomSheet() {
    var showSheet by remember { mutableStateOf(true) }
    
    if (showSheet) {
        ModalBottomSheet(onDismissRequest = { showSheet = false }) {
            Text("Pastdan chiquvchi qo'shimcha ma'lumotlar")
        }
    }
}

fun main() {
    println("ModalBottomSheet: Mobil ilovalarda qo'shimcha menyu va filtrlash uchun eng qulay panel.")
}
""",
    "ModalBottomSheet foydalanuvchi qo'li bilan pastga tortganda yoki fonga bosganda avtomatik ravishda yopiladi.",
    """
ModalBottomSheet: Mobil ilovalarda qo'shimcha menyu va filtrlash uchun eng qulay panel.
"""
)

# 947
add_task(
    947,
    "Modifier.weight() orqali elementlarni mutanosib taqsimlash",
    "Row ichidagi ikki elementga weight(1f) va weight(2f) berib kenglikni proporsional bo'ling.",
    """
import androidx.compose.foundation.layout.Row
import androidx.compose.material3.Text
import androidx.compose.ui.Modifier
import androidx.compose.runtime.Composable

@Composable
fun ProportionalRow() {
    Row {
        Text("1-qism (33%)", modifier = Modifier.weight(1f))
        Text("2-qism (66%)", modifier = Modifier.weight(2f))
    }
}

fun main() {
    println("Modifier.weight qolgan bo'sh maydonni ko'rsatilgan nisbatda bo'lib beradi.")
}
""",
    "weight modifiyeri LinearLayout dagi `layout_weight` kabi ishlaydi va har xil ekran o'lchamlariga moslashuvchanlik beradi.",
    """
Modifier.weight qolgan bo'sh maydonni ko'rsatilgan nisbatda bo'lib beradi.
"""
)

# 948
add_task(
    948,
    "Compose da rasm chizish (Image va Painter)",
    "Rasm chiqarish va uning kontent masshtabini (ContentScale.Crop) boshqarish.",
    """
import androidx.compose.foundation.layout.size
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun AvatarImage(imageUrl: String) {
    Text(
        text = "[Avatar Rasmi: $imageUrl]",
        modifier = Modifier.size(50.dp)
    )
}

fun main() {
    println("Image vidjeti ContentScale orqali rasmni to'liq to'ldirish yoki sig'dirishni boshqaradi.")
}
""",
    "Image Composable vidjeti Bitmap, Vector yoki Painter obyektlarini qabul qiladi va kontent tavsifini (accessibility contentDescription) talab qiladi.",
    """
Image vidjeti ContentScale orqali rasmni to'liq to'ldirish yoki sig'dirishni boshqaradi.
"""
)

# 949
add_task(
    949,
    "rememberUpdatedState yordamida uzoq davom etuvchi effektdagi yangi callbackni ushlash",
    "LaunchedEffect davomida tashqaridan o'zgargan eng so'nggi lambdani eslab qolish texnikasi.",
    """
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.getValue
import kotlinx.coroutines.delay

@Composable
fun TimerWatcher(onTimeout: () -> Unit) {
    val currentOnTimeout by rememberUpdatedState(onTimeout)
    
    LaunchedEffect(Unit) {
        delay(1000L)
        currentOnTimeout() // Har doim eng oxirgi berilgan funksiyani chaqiradi
    }
}

fun main() {
    println("rememberUpdatedState: Qayta chizilishda effekti qayta ishga tushirmasdan yangi qiymatni uzatish.")
}
""",
    "rememberUpdatedState LaunchedEffect ning key parametrlarini yangilamasdan turib, uning ichida eng so'nggi lambdani chaqirish imkonini beradi.",
    """
rememberUpdatedState: Qayta chizilishda effekti qayta ishga tushirmasdan yangi qiymatni uzatish.
"""
)

# 950
add_task(
    950,
    "19-qism xulosasi: To'liq Compose mobil ilovasi (Mahsulotlar katalogi, qidiruv va savatcha UI)",
    "State, Recomposition, LazyColumn, Scaffold, SearchField va animatsiyalarni birlashtirgan to'liq deklarativ mobil do'kon ilovasini yarating.",
    """
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

data class ShopProduct(val id: Int, val title: String, val price: Double)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FullShopApp() {
    var searchQuery by remember { mutableStateOf("") }
    val cart = remember { mutableStateListOf<ShopProduct>() }
    
    val allProducts = listOf(
        ShopProduct(1, "Noutbuk Ultra", 899.0),
        ShopProduct(2, "Simsiz Quloqchin", 49.0),
        ShopProduct(3, "Mexanik Klaviatura", 85.0)
    )
    
    val filtered = allProducts.filter { it.title.contains(searchQuery, ignoreCase = true) }
    
    Scaffold(
        topBar = { TopAppBar(title = { Text("Mobil Do'kon (Savatchada: ${cart.size} ta)") }) }
    ) { padding ->
        Column(modifier = Modifier.fillMaxSize().padding(padding).padding(16.dp)) {
            OutlinedTextField(
                value = searchQuery,
                onValueChange = { searchQuery = it },
                label = { Text("Qidiruv...") },
                modifier = Modifier.padding(bottom = 12.dp)
            )
            
            LazyColumn {
                items(filtered, key = { it.id }) { product ->
                    Card(modifier = Modifier.padding(vertical = 4.dp)) {
                        Row(modifier = Modifier.padding(12.dp)) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text(product.title)
                                Text("${product.price} $")
                            }
                            Button(onClick = { cart.add(product) }) {
                                Text("Sotib olish")
                            }
                        }
                    }
                }
            }
        }
    }
}

fun main() {
    println("Jetpack Compose asoslari to'liq va mukammal loyihalashtirildi!")
}
""",
    "Ushbu yakuniy loyihada barcha asosiy Jetpack Compose konseptlari: Reaktiv holat (mutableStateOf, mutableStateListOf), deklarativ Layout (Column, Row, Scaffold), samarali ro'yxatlar (LazyColumn), matn kiritish va voqealar to'liq sintez qilindi.",
    """
Jetpack Compose asoslari to'liq va mukammal loyihalashtirildi!
"""
)

save_file("kotlin_19_android_jetpack_compose_asoslari.md", tasks)
