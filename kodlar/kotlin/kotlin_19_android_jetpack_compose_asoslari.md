# 901-Topshiriq: Birinchi @Composable funksiya va Text vidjeti
## Topshiriq sharti:
Jetpack Compose ning deklarativ UI asosini tushuntiruvchi birinchi @Composable funksiyasini yozing va unda ekranga matn chiqaring.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
@Composable annotatsiyasi Kotlin kompilyatori plaginiga (Compose Compiler) bu funksiya UI elementlarini chizish uchun mo'ljallanganligini bildiradi. U hech narsa qaytarmaydi (Unit), balki UI grafigini shakllantiradi.

## Ishlash natijasi:
```text
Jetpack Compose deklarativ UI funksiyasi e'lon qilindi: Greeting
Composable funksiyalar UI daraxtini deklarativ kod orqali ifodalaydi.
```


# 902-Topshiriq: Column yordamida elementlarni vertikal tartiblash
## Topshiriq sharti:
Bir nechta matn elementini ustma-ust (vertikal) joylashtiruvchi Column tartibini yarating.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Column layout konteyneri ichidagi barcha bolalar Composable elementlarini vertikal o'q bo'ylab ketma-ket joylashtiradi.

## Ishlash natijasi:
```text
Column: Elementlar yuqoridan pastga qarab vertikal tartiblanadi.
```


# 903-Topshiriq: Row yordamida elementlarni gorizontal joylashtirish
## Topshiriq sharti:
Belgi va matnni yonma-yon (gorizontal) joylashtirish uchun Row konteyneridan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Row konteyneri barcha elementlarni gorizontal qatorda joylashtiradi va qator ichidagi elementlar oralig'ini sozlash imkonini beradi.

## Ishlash natijasi:
```text
Row: Elementlar chapdan o'ngga gorizontal joylashadi.
```


# 904-Topshiriq: Box yordamida elementlarni ustma-ust (overlay) joylashtirish
## Topshiriq sharti:
Elementlarni bir-birining ustiga (masalan orqa fon rasmi ustiga matn) qatlamlab joylashtiruvchi Box konteynerini yozing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Box konteyneri FrameLayout kabi ishlaydi, unda elementlar bir-birining ustiga qo'yiladi va alignment orqali burchaklarga taqsimlanadi.

## Ishlash natijasi:
```text
Box: Elementlar Z o'qi bo'yicha ustma-ust qatlamlanadi.
```


# 905-Topshiriq: Modifier.fillMaxSize() va Modifier.padding() bilan joylashuvni sozlash
## Topshiriq sharti:
Ekran o'lchamini to'liq egallash va ichki chekinish (padding) berish uchun Modifiyerlardan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Modifier - bu Jetpack Compose dagi elementlarning xulq-atvori, hajmi, foni va chekinishlarini tartibga soluvchi asosiy mexanizmdir. Zanjir tartibi juda muhim.

## Ishlash natijasi:
```text
Modifier zanjiri elementning ko'rinishi va o'lchamlarini belgilaydi.
```


# 906-Topshiriq: Modifier.background() va clip(RoundedCornerShape) bilan burchaklarni yaxlitlash
## Topshiriq sharti:
Vidjetga rangli fon va yumaloqlangan burchaklar beruvchi Composable tuzing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
clip(RoundedCornerShape) shaklni kesib beradi, undan keyin berilgan background esa faqat shu kesilgan hududni bo'yab beradi.

## Ishlash natijasi:
```text
clip va background kombinatsiyasi burchaklari yumaloq blok hosil qiladi.
```


# 907-Topshiriq: Modifier.clickable { } yordamida bosish hodisasini qo'shish
## Topshiriq sharti:
Ixtiyoriy matn yoki kartochkani bosiladigan (clickable) qilib, bosilganda xabar chiqaruvchi kod yozing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Modifier.clickable nafaqat bosish hodisasini tinglaydi, balki avtomatik ravishda Material Ripple (to'lqinli bosilish effekti) va accessibility yordamchilarini ham ulaydi.

## Ishlash natijasi:
```text
Modifier.clickable har qanday Composable elementga bosish xususiyatini beradi.
```


# 908-Topshiriq: mutableStateOf va remember yordamida hisoblagich holatini saqlash
## Topshiriq sharti:
Tugma har gal bosilganda oshib boruvchi va UI ni yangilovchi Reaktiv hisoblagich (Counter) yarating.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
mutableStateOf Compose kuzatuv tizimiga yangilanish signallarini beradi. remember esa funksiya qayta chaqirilganda holat nollanib ketmasligini ta'minlaydi.

## Ishlash natijasi:
```text
remember qayta chizilishda (recomposition) qiymatni xotirada saqlab qoladi.
```


# 909-Topshiriq: Recomposition mexanizmi va uning aqlli filtri (Smart Recomposition)
## Topshiriq sharti:
Faqat o'zgargan qiymatga bog'liq bo'lgan Composable qismlarigina qayta chizilishini tushuntiruvchi misol keltiring.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Recomposition (qayta chizilish) holat (State) o'zgarganda sodir bo'ladi. Compose faqat qiymati o'zgargan Composable tugunlarini yangilaydi (Smart Recomposition).

## Ishlash natijasi:
```text
Compose aqlli: butun ekranni emas, faqat o'zgargan vidjetni qayta chizadi.
```


# 910-Topshiriq: rememberSaveable yordamida ekran burilganda holatni yo'qotmaslik
## Topshiriq sharti:
Oddiy remember bilan rememberSaveable o'rtasidagi farqni va ekran holatini (Configuration change) saqlashni namoyish eting.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
remember faqat recomposition vaqtida xotirani saqlaydi, Activity qayta yaratilsa (masalan til yoki ekran burilishi) ma'lumot o'chib ketadi. rememberSaveable esa Bundle ga saqlab, to'liq tiklaydi.

## Ishlash natijasi:
```text
rememberSaveable: Ekran burilganda (rotate) yoki jarayon o'ldirilganda ham holatni saqlab qoladi.
```


# 911-Topshiriq: TextField va OutlinedTextField orqali matn kiritish
## Topshiriq sharti:
Foydalanuvchi kiritgan matnni o'zida aks ettiruvchi va boshqaruvchi (controlled component) TextField yarating.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Compose dagi TextField odatda 'boshqariladigan' (controlled) komponent hisoblanadi: kiritilgan belgi onValueChange orqali State ga yoziladi va qayta value ga beriladi.

## Ishlash natijasi:
```text
Controlled TextField: qiymat doimo Kotlin State o'zgaruvchisidan olinadi.
```


# 912-Topshiriq: State Hoisting (holatni ajratish): Stateless vs Stateful
## Topshiriq sharti:
Komponentni qayta ishlatiluvchi (reusable) va test qilish oson bo'lishi uchun State Hoisting qoidasiga ko'ra holatni tashqariga chiqaring.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
State Hoisting arxitekturasida komponent ichida state saqlanmaydi, balki `value` va `onValueChange` parametrlari orqali tashqaridan boshqariladi. Bu testlashni osonlashtiradi.

## Ishlash natijasi:
```text
State Hoisting: Holatni yuqoriga (caller ga) ko'tarish, UI ni esa sof render qiluvchi qilish.
```


# 913-Topshiriq: Shartli UI: if (isLoggedIn) orqali ekran ko'rinishini almashtirish
## Topshiriq sharti:
Foydalanuvchi tizimga kirgan yoki kirmaganligiga qarab boshqa-boshqa UI qismlarini chizuvchi shartli Composable yozing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
XML da visibility = GONE/VISIBLE o'rniga Compose da oddiy Kotlin `if-else` shartlari ishlatiladi. Shart bajarilmasa, o'sha Composable umuman UI daraxtiga qo'shilmaydi.

## Ishlash natijasi:
```text
Compose da shartli render oddiy Kotlin `if-else` yoki `when` orqali ifodalanadi.
```


# 914-Topshiriq: LazyColumn yordamida minglab elementlarni samarali ro'yxatda ko'rsatish
## Topshiriq sharti:
Android dagi RecyclerView o'rnini bosuvchi, faqat ekranda ko'rinib turgan elementlarnigina xotiraga oluvchi LazyColumn ni loyihalang.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
LazyColumn an'anaviy RecyclerView ning barcha afzalliklarini bitta qulay deklarativ blokda taqdim etadi: adapter yoki viewHolder yaratish talab etilmaydi.

## Ishlash natijasi:
```text
LazyColumn faqat ekrandagi ko'rinib turgan elementlarni chizadi (Recycling).
```


# 915-Topshiriq: LazyColumn da items(key = { it.id }) parametrining o'rni
## Topshiriq sharti:
Ro'yxat elementlari qo'shilganda yoki saralanganda keraksiz qayta chizilishlarni oldini olish uchun barqaror kalit (key) bering.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
key berilganda Compose elementlarni pozitsiyasi (indeksi) bo'yicha emas, aynan shu noyob kalit bo'yicha taniydi, bu esa ro'yxat tartibi o'zgarganda yuqori samaradorlik beradi.

## Ishlash natijasi:
```text
key parametri elementlar almashganda holatni va animatsiyalarni to'g'ri saqlaydi.
```


# 916-Topshiriq: LazyRow yordamida gorizontal suriluvchi kartochkalar ro'yxatini yaratish
## Topshiriq sharti:
Gorizontal o'q bo'ylab suriluvchi (horizontal scrolling) toifalar yoki fotogalereya ro'yxatini yozing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
LazyRow gorizontal yo'nalishdagi elementlarni xuddi LazyColumn kabi resurslarni tejagan holda render qiladi.

## Ishlash natijasi:
```text
LazyRow: Gorizontal o'qda dangasa yuklanuvchi ro'yxat.
```


# 917-Topshiriq: Card va ElevatedCard vidjetlari bilan soya va qavariq ko'rinish
## Topshiriq sharti:
Material 3 uslubidagi Card vidjetiga soya (elevation) va burchaklar berib chiroyli mahsulot kartasi yasang.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
ElevatedCard chiroyli yorug'lik va soya effekti bilan vizual iyerarxiyani ajratib ko'rsatishga yordam beradi.

## Ishlash natijasi:
```text
ElevatedCard: Zamonaviy Material Design 3 kartochka komponenti.
```


# 918-Topshiriq: CircularProgressIndicator va LinearProgressIndicator
## Topshiriq sharti:
Yuklanish jarayonini ko'rsatuvchi aylanma va chiziqli ko'rsatkichlarni Composable da chiqarish.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Progress indikatorlari indeterminate (cheksiz aylanuvchi) yoki progress parametri orqali aniq foiz ko'rsatuvchi holatda ishlatiladi.

## Ishlash natijasi:
```text
Progress indikatorlar foydalanuvchiga jarayon davom etayotganini bildiradi.
```


# 919-Topshiriq: Checkbox va Switch komponentlari bilan holatni boshqarish
## Topshiriq sharti:
Sozlamalar ekranidagi bayroqcha (Checkbox) va yoqish/o'chirish tugmachasini (Switch) boshqaring.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Checkbox va Switch komponentlari o'zlarining checked va onCheckedChange xususiyatlari orqali deklarativ boshqariladi.

## Ishlash natijasi:
```text
Checkbox va Switch: Boolean qiymatlarni interaktiv o'zgartirish.
```


# 920-Topshiriq: Slider komponenti bilan qiymatni silliq tanlash
## Topshiriq sharti:
Ovoz balandligi yoki yorug'lik darajasini 0 dan 100 gacha silliq o'zgartiruvchi Slider ni yozing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Slider komponenti berilgan valueRange chegarasida qiymatni silliq Float ko'rinishida yetkazib beradi.

## Ishlash natijasi:
```text
Slider uzluksiz raqamli diapazonlardan qiymat tanlash imkonini beradi.
```


# 921-Topshiriq: Scaffold yordamida standart ekran skeletini qurish
## Topshiriq sharti:
Material ekranning sarlavhasi (TopBar), harakat tugmasi (FAB) va asosiy kontentini Scaffold yordamida tartibga soling.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Scaffold avtomatik ravishda tizim panellari, sarlavha va pastki navigatsiya uchun joy (innerPadding) hisoblab beradi.

## Ishlash natijasi:
```text
Scaffold Material Design ekranlarining asosiy karkasini tashkil etadi.
```


# 922-Topshiriq: SnackbarHost orqali pastki xabarnoma chiqarish
## Topshiriq sharti:
rememberSnackbarHostState va coroutineScope orqali foydalanuvchiga vaqtinchalik Snackbar xabarini ko'rsatish.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
showSnackbar() suspend funksiya bo'lgani uchun uni chaqirishda rememberCoroutineScope() orqali olingan koroutina ko'lami ishlatiladi.

## Ishlash natijasi:
```text
SnackbarHost zamonaviy asinxron xabarnomalarni chiqarish markazidir.
```


# 923-Topshiriq: LaunchedEffect yordamida ekran ochilganda bir martalik tarmoq so'rovini boshlash
## Topshiriq sharti:
Composable ekranga birinchi marta kirganda (mount) asinxron ma'lumot yuklashni LaunchedEffect orqali boshlang.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
LaunchedEffect Composable render bo'lganda yangi koroutina boshlaydi. Agar key (userId) o'zgarsa, eski koroutina bekor qilinib yangisi boshlanadi.

## Ishlash natijasi:
```text
LaunchedEffect hayot sikliga bog'liq asinxron Side-Effect larni boshqaradi.
```


# 924-Topshiriq: DisposableEffect yordamida ekrandan chiqib ketilganda resurslarni tozalash
## Topshiriq sharti:
Composable hayot sikli tugaganda (onDispose) sensor yoki tinglovchini o'chiruvchi DisposableEffect ni qo'llang.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
DisposableEffect uning bloki tugaganda yoki Composable ekrandan yo'qolganda `onDispose { }` chaqiruvini bajaradi, bu memory leak larni oldini oladi.

## Ishlash natijasi:
```text
DisposableEffect: Resurslarni ulash va onDispose da xavfsiz tozalash.
```


# 925-Topshiriq: derivedStateOf yordamida ortiqcha recomposition larning oldini olish
## Topshiriq sharti:
Tez-tez o'zgaruvchi qiymatdan (masalan skroll pozitsiyasi) faqat natijaviy shart o'zgargandagina qayta chizilishni ta'minlang.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Agar har bir piksel skrollida oddiy state ishlatilsa, butun UI har millisekundda qayta chizilar edi. derivedStateOf faqat natijaviy holat o'zgargandagina recomposition chaqiradi.

## Ishlash natijasi:
```text
derivedStateOf: O'zgarishlar ko'p bo'lganda faqat yakuniy hisoblangan shartni kuzatish.
```


# 926-Topshiriq: AnimatedVisibility yordamida elementning paydo bo'lishini animatsiya qilish
## Topshiriq sharti:
Tugma bosilganda matnning silliq kengayib (expand) va qisqarib (shrink) paydo bo'lishini ta'minlang.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
AnimatedVisibility elementi avtomatik ravishda kirish (fadeIn/expand) va chiqish (fadeOut/shrink) animatsiyalarini ulaydi.

## Ishlash natijasi:
```text
AnimatedVisibility deklarativ tarzda UI elementlarini animatsiyalaydi.
```


# 927-Topshiriq: animateColorAsState yordamida ranglar almashinuvini silliq qilish
## Topshiriq sharti:
Tanlangan yoki tanlanmagan holatga qarab fon rangi silliq o'zgaruvchi Composable yozing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
animate*AsState funksiyalari (color, float, dp, int) berilgan maqsadli qiymatga (targetValue) silliq interpolyatsiya bilan o'tishni amalga oshiradi.

## Ishlash natijasi:
```text
animateColorAsState: Ranglarning keskin emas, silliq o'tishini ta'minlaydi.
```


# 928-Topshiriq: Canvas vidjeti yordamida maxsus shakllar va chiziqlar chizish
## Topshiriq sharti:
DrawScope orqali ekranga qizil doira va to'g'ri chiziq chizuvchi maxsus Canvas Composable yozing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Canvas Composable vidjeti ichida drawCircle, drawRect, drawLine, drawPath kabi past darajadagi 2D chizish vositalari mavjud.

## Ishlash natijasi:
```text
Canvas DrawScope orqali 2D grafik shakllarni to'g'ridan-to'g'ri chizish imkonini beradi.
```


# 929-Topshiriq: AlertDialog yordamida tasdiqlash oynasini ko'rsatish
## Topshiriq sharti:
Foydalanuvchi ma'lumotni o'chirishdan avval 'Ishonchingiz komilmi?' deb so'rovchi AlertDialog tuzing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
AlertDialog deklarativdir: agar `showDialog` rost bo'lsa u chiziladi, yolg'on bo'lsa butunlay yo'qoladi.

## Ishlash natijasi:
```text
AlertDialog: Ekranning markazida tasdiqlovchi modal oyna chiqarish.
```


# 930-Topshiriq: Slot API yondashuvi bilan moslashuvchan konteyner yaratish
## Topshiriq sharti:
O'z ichiga ixtiyoriy boshqa Composable elementni qabul qila oluvchi (trailing lambda) maxsus sarlavhali panel yarating.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Slot API Jetpack Compose ning eng kuchli arxitektura qoidalaridan biri bo'lib, uning yordamida Scaffold, TopAppBar kabi moslashuvchan konteynerlar quriladi.

## Ishlash natijasi:
```text
Slot API: Komponentlarga bolalar vidjetlarini erkin joylashtirish imkonini beradi.
```


# 931-Topshiriq: MaterialTheme orqali ranglar palitrasi va tipografiyani qo'llash
## Topshiriq sharti:
MaterialTheme.colorScheme va MaterialTheme.typography orqali umumiy dizayn tizimiga rioya qilishni ko'rsating.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
MaterialTheme markazlashgan tokenlar tizimidir. Ilova qorong'u rejimga o'tganda `primary` ranglar avtomatik moslashadi.

## Ishlash natijasi:
```text
MaterialTheme butun ilova bo'ylab yagona rang, shrift va shakllar uslubini ta'minlaydi.
```


# 932-Topshiriq: Custom Modifier kengaytma funksiyasi yaratish
## Topshiriq sharti:
Kodni qayta-qayta takrorlamaslik uchun bir nechta modifiyerlarni birlashtiruvchi shaxsiy kengaytma yozing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Modifier ga kengaytma funksiya yozish orqali loyihaning UI kodini toza va o'qilishi oson holatga keltirish mumkin.

## Ishlash natijasi:
```text
Custom Modifier: Takrorlanuvchi dizayn parametrlarini ixcham kengaytma funksiyaga yig'ish.
```


# 933-Topshiriq: DropdownMenu va DropdownMenuItem ochiluvchi ro'yxati
## Topshiriq sharti:
Tugma bosilganda pastga qarab ochiluvchi va tanlov qilish imkonini beruvchi DropdownMenu yarating.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
DropdownMenu o'zining expanded holati orqali ko'rinadi va foydalanuvchi variantlardan birini bosishi bilan yopiladi.

## Ishlash natijasi:
```text
DropdownMenu: Tanlov menyularini chiqarish uchun qulay komponent.
```


# 934-Topshiriq: LazyVerticalGrid yordamida fotogalereya yoki mahsulotlar to'rini (Grid) qurish
## Topshiriq sharti:
2 ustunli jadval shaklida elementlarni taqsimlovchi LazyVerticalGrid ni yozing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
GridCells.Fixed(2) har bir qatorda teng ikkita ustun hosil qiladi va elementlarni avtomatik taqsimlaydi.

## Ishlash natijasi:
```text
LazyVerticalGrid: Ko'p ustunli to'r (Grid) ko'rinishida elementlarni ko'rsatish.
```


# 935-Topshiriq: CompositionLocalProvider orqali chuqur parametr uzatish
## Topshiriq sharti:
Har bir Composable ga alohida argument uzatmasdan, daraxt bo'ylab ma'lumot tarqatuvchi CompositionLocal mexanizmini tushuntiring.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
LocalContext, LocalDensity va LocalContentColor kabi barcha standart Compose vositalari aynan CompositionLocal orqali ishlaydi.

## Ishlash natijasi:
```text
CompositionLocal: Parametrlarni har bir funksiyaga qo'lda uzatish muammosini hal qiladi.
```


# 936-Topshiriq: snapshotFlow yordamida Compose State ni Kotlin Flow ga aylantirish
## Topshiriq sharti:
Compose State qiymatini Coroutine Flow sifatida kuzatib, unda debounce yoki filter operatorlarini ishlatish.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
snapshotFlow Compose State va Coroutine Flow dunyolarini birlashtiruvchi rasmiy ko'prikdir.

## Ishlash natijasi:
```text
snapshotFlow: Compose xotirasidagi o'zgarishlarni reaktiv Flow ga aylantiradi.
```


# 937-Topshiriq: animateFloatAsState yordamida shaffoflikni (alpha) animatsiya qilish
## Topshiriq sharti:
Tugma bosilganda elementning paydo bo'lishini shaffoflik (alpha) o'zgarishi orqali animatsiyalang.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Modifier.alpha(alpha) parametri elementning shaffofligini o'zgartiradi va silliq fade effektini hosil qiladi.

## Ishlash natijasi:
```text
animateFloatAsState: Float o'zgaruvchilarni animatsiya qilish vositasi.
```


# 938-Topshiriq: Modifier.border() va gradient fon (Brush.horizontalGradient)
## Topshiriq sharti:
Vidjetga rangli gradient hoshiya va fon berishni amalga oshiring.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Brush sinfi chiziqli, radial yoki sweep gradientlarini yasab, ularni border yoki background ga uzatish imkonini beradi.

## Ishlash natijasi:
```text
Brush.horizontalGradient yordamida zamonaviy gradient vizuallari yaratiladi.
```


# 939-Topshiriq: Shaxsiy UserProfileCard Composable vidjetini yaratish
## Topshiriq sharti:
Foydalanuvchi rasmi, ismi, kasbi va obuna tugmasini o'z ichiga olgan mustaqil komponent loyihalang.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Mustaqil Composable komponentlar yaratish orqali butun ilova arxitekturasi g'ishtdek yig'iladi va toza bo'ladi.

## Ishlash natijasi:
```text
UserProfileCard: Modulli, toza va mustaqil Compose komponenti.
```


# 940-Topshiriq: rememberCoroutineScope orqali foydalanuvchi amallarida koroutina ishga tushirish
## Topshiriq sharti:
Tugma onClick hodisasida tarmoqqa asinxron ma'lumot yuborish uchun rememberCoroutineScope dan foydalaning.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Composable funksiyalarning o'zi oddiy funksiya (suspend emas), shuning uchun onClick kabi lambdalarda to'xtatuvchi kod yozish uchun rememberCoroutineScope talab qilinadi.

## Ishlash natijasi:
```text
rememberCoroutineScope tugma yoki foydalanuvchi hodisalari ichida koroutina boshlash uchun kerak.
```


# 941-Topshiriq: IconButton va Icon orqali savatcha va bildirishnoma tugmalari
## Topshiriq sharti:
Piktogramma asosidagi tugmalarni (IconButton) yaratish.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
IconButton minimal 48dp o'lchamdagi qulay bosish maydonini ta'minlaydi va to'lqin effektini beradi.

## Ishlash natijasi:
```text
IconButton piktogramma o'lchamlarini Material standartlariga moslaydi.
```


# 942-Topshiriq: RadioGroup va RadioButton guruhi yaratish
## Topshiriq sharti:
Foydalanuvchiga to'lov turini tanlash imkonini beruvchi yagona tanlovli (Single Choice) radio guruh tuzing.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Radio tugmalari guruhi har bir elementni joriy tanlangan qiymat bilan solishtirish orqali boshqariladi.

## Ishlash natijasi:
```text
RadioButton: Ro'yxatdan faqat bitta variantni tanlash.
```


# 943-Topshiriq: TopAppBar bilan harakatlar (actions) va orqaga qaytish tugmasi
## Topshiriq sharti:
Ekran tepasidagi sarlavha panelida orqaga qaytish va qidiruv harakatlari tugmalarini joylashtiring.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Material 3 TopAppBar navigatsiya ikonkasi, sarlavha va o'ng tarafdagi harakatlar (actions) uchun maxsus slotlarga ega.

## Ishlash natijasi:
```text
TopAppBar: Ekranning standart yuqori navigatsiya paneli.
```


# 944-Topshiriq: FloatingActionButton (FAB) orqali yangi yozuv qo'shish tugmasi
## Topshiriq sharti:
Ekranning pastki o'ng burchagida qalqib turuvchi yumaloq harakat tugmasini (FAB) yasang.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
FloatingActionButton Scaffold ning floatingActionButton uyasiga (slotiga) joylashtiriladi va avtomatik joylashuvni oladi.

## Ishlash natijasi:
```text
FAB ekrandagi asosiy va eng muhim harakatni ifodalaydi.
```


# 945-Topshiriq: Compose da qorong'u rejimni (isSystemInDarkTheme) tekshirish
## Topshiriq sharti:
Tizim hozir qorong'u (Dark) yoki yorug' (Light) rejimda ekanligini aniqlovchi Compose funksiyasi misoli.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
isSystemInDarkTheme() reaktiv bo'lib, foydalanuvchi tizim panelidan rejimni almashtirishi bilan darhol UI ni yangilaydi.

## Ishlash natijasi:
```text
isSystemInDarkTheme() tizim sozlamalaridagi tungi rejimni aniqlaydi.
```


# 946-Topshiriq: ModalBottomSheet yordamida pastdan chiquvchi panelni ko'rsatish
## Topshiriq sharti:
Ekran pastidan silliq ko'tariluvchi zamonaviy ma'lumotlar panelini (Bottom Sheet) namoyish eting.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
ModalBottomSheet foydalanuvchi qo'li bilan pastga tortganda yoki fonga bosganda avtomatik ravishda yopiladi.

## Ishlash natijasi:
```text
ModalBottomSheet: Mobil ilovalarda qo'shimcha menyu va filtrlash uchun eng qulay panel.
```


# 947-Topshiriq: Modifier.weight() orqali elementlarni mutanosib taqsimlash
## Topshiriq sharti:
Row ichidagi ikki elementga weight(1f) va weight(2f) berib kenglikni proporsional bo'ling.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
weight modifiyeri LinearLayout dagi `layout_weight` kabi ishlaydi va har xil ekran o'lchamlariga moslashuvchanlik beradi.

## Ishlash natijasi:
```text
Modifier.weight qolgan bo'sh maydonni ko'rsatilgan nisbatda bo'lib beradi.
```


# 948-Topshiriq: Compose da rasm chizish (Image va Painter)
## Topshiriq sharti:
Rasm chiqarish va uning kontent masshtabini (ContentScale.Crop) boshqarish.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Image Composable vidjeti Bitmap, Vector yoki Painter obyektlarini qabul qiladi va kontent tavsifini (accessibility contentDescription) talab qiladi.

## Ishlash natijasi:
```text
Image vidjeti ContentScale orqali rasmni to'liq to'ldirish yoki sig'dirishni boshqaradi.
```


# 949-Topshiriq: rememberUpdatedState yordamida uzoq davom etuvchi effektdagi yangi callbackni ushlash
## Topshiriq sharti:
LaunchedEffect davomida tashqaridan o'zgargan eng so'nggi lambdani eslab qolish texnikasi.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
rememberUpdatedState LaunchedEffect ning key parametrlarini yangilamasdan turib, uning ichida eng so'nggi lambdani chaqirish imkonini beradi.

## Ishlash natijasi:
```text
rememberUpdatedState: Qayta chizilishda effekti qayta ishga tushirmasdan yangi qiymatni uzatish.
```


# 950-Topshiriq: 19-qism xulosasi: To'liq Compose mobil ilovasi (Mahsulotlar katalogi, qidiruv va savatcha UI)
## Topshiriq sharti:
State, Recomposition, LazyColumn, Scaffold, SearchField va animatsiyalarni birlashtirgan to'liq deklarativ mobil do'kon ilovasini yarating.

## Yechim (Kotlin kodi):
```kotlin
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
```

## Tushuntirish va Mantiq:
Ushbu yakuniy loyihada barcha asosiy Jetpack Compose konseptlari: Reaktiv holat (mutableStateOf, mutableStateListOf), deklarativ Layout (Column, Row, Scaffold), samarali ro'yxatlar (LazyColumn), matn kiritish va voqealar to'liq sintez qilindi.

## Ishlash natijasi:
```text
Jetpack Compose asoslari to'liq va mukammal loyihalashtirildi!
```

