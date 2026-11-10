# -*- coding: utf-8 -*-
import os

out_path = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\kotlin\kotlin_mukammal_qollanma.md"

content = """# Kotlin Dasturlash Tili: Mukammal Ensiklopediya va Arxitektura Qo'llanmasi (Kotlin 2.0+, K2, KMP, Compose, Mobil AI)

Ushbu fundamental ensiklopediya zamonaviy Kotlin (Kotlin 2.0+, K2 yangi kompilyatori, Jetpack Compose, Kotlin Multiplatform va Mobil AI Agent) dasturlash tilining ichki mexanizmlari, falsafasi, arxitekturasi va eng yuqori darajadagi professional amaliyotlarini o'zida mujassam etgan to'liq o'zbek tilidagi qo'llanmadir.

---

## MUNDARIJA
1. **Kirish va Kotlin Falsafasi**
   - Pragmatik dasturlash tili tamoyili (Developer Ergonomics)
   - Readability vs Writeability
   - Java bilan 100% ikki tomonlama moslik (Interoperability)
   - Null-Safety: "Milliard dollarlik xato"ni til darajasida bartaraf etish
   - O'zgarmaslik (Immutability) birinchi darajali fuqaro sifatida
   - Kotlin evolyutsiyasi: Kotlin 1.0 dan Kotlin 2.0+ gacha
2. **Kotlin K2 Yangi Kompilyator Arxitekturasi**
   - Eski kompilyator (K1) cheklovlari (PSI va BindingContext muammolari)
   - K2 ning yangi Frontend IR (FIR - Frontend Intermediate Representation) arxitekturasi
   - Kompilyatsiya tezligining 2 baravardan ortiq oshishi va xotira samaradorligi
   - Yangi Type Inference algoritmi va aqlli Smart Cast (Smart Cast 2.0)
   - Kompilyator plaginlari arxitekturasi va Compose Compiler birlashuvi
   - Backend IR (JVM, JS, Wasm, Native) kod generatsiyasi
3. **Bayt-kod Dekompilyatsiyasi: Kotlin Kapot Ostida (Under the Hood)**
   - `val` va `var` maydonlarining Java bayt-kodiga o'girilishi
   - Data Class larning dekompilyatsiyasi: `copy()`, `componentN()`, `equals()`, `hashCode()`
   - Extension Functions: statik yordamchi funksiyalar siri
   - Lambdalar va Yuqori Tartibli Funksiyalar (High-Order Functions): `FunctionN` va `invokedynamic`
   - `inline`, `noinline`, `crossinline` ning bayt-kod darajasidagi kuchi
   - Suspend funksiyalar va State Machine: `Continuation<T>`, label va switch-case bayt-kodi
   - Singleton `object` va `companion object` dekompilyatsiyasi
   - Xususiyatlar delegatsiyasi (`by lazy`, `Delegates.observable`) dekompilyatsiyasi
4. **Kotlin Koroutinalari va Reaktiv Dasturlash Arxitekturasi**
   - Koroutinalar falsafasi: Kooperativ ko'p vazifalilik (Cooperative Multitasking)
   - Operatsion tizim oqimlari (OS Threads) vs Koroutinalar
   - Strukturalangan konkurentlik (Structured Concurrency) tamoyillari
   - Bekor qilish (Cancellation) va Istisnolarni boshqarish mexanizmi
   - Kotlin Flow: Sovuq oqimlar (Cold Streams) vs Issiq oqimlar (Hot Streams: StateFlow va SharedFlow)
   - Backpressure va buferlash strategiyalari
5. **Kotlin Multiplatform (KMP) Ensiklopediyasi**
   - KMP strategiyasi: "Share logic, keep native UI"
   - KMP arxitektura qatlamlari: Common, Android, iOS (Kotlin/Native), Desktop, Web (Wasm)
   - `expect` va `actual` deklaratsiyalarining chuqur mexanizmi
   - Kotlin/Native yangi xotira boshqaruvi va Garbage Collector
   - KMP kutubxonalar ekotizimi: Ktor, kotlinx.serialization, Room KMP, Koin
6. **Zamonaviy Android Arxitekturasi va Jetpack Compose**
   - Deklarativ UI inqilobi va Recomposition mexanizmi
   - Clean Architecture va MVI / MVVM qatlamlari
   - Dependency Injection: Koin va Dagger Hilt
   - Offline-First ma'lumotlar oqimi (Room DB + Flow + Ktor)
7. **Mobil Sun'iy Intellekt va AI Agentlar Kelajagi Kotlinda**
   - On-Device AI (Gemini Nano va Android AICore)
   - Token Streaming va real vaqtda reaktiv UI (Flow<String>)
   - Function Calling / Tool Use orqali mobil tizim drayverlarini boshqarish
   - Mobil RAG (Retrieval-Augmented Generation) va lokal semantik qidiruv
   - Mobil AI Agentlarning xavfsizlik filtrlari (Guardrails)
8. **Eng Yaxshi Amaliyotlar, Kod Uslubi va Antipatternlar (Best Practices)**
   - Nimalardan qat'iyan saqlanish lozim (Anti-patterns)
   - Samaradorlik sirlari: Value classes, xotira ajratilishini kamaytirish
   - Xulosa va Professional Kotlin Dasturchisining Yo'l Xaritasi

---

## 1. KIRISH VA KOTLIN FALSAFASI

### 1.1. Pragmatik Til Tamoyili (Developer Ergonomics)
Kotlin - bu sof nazariy yoki akademik laboratoriya tili emas. U JetBrains kompaniyasi tomonidan o'zlarining yirik tijoriy loyihalarida (masalan, IntelliJ IDEA) yuzaga kelgan kundalik og'ir muammolarni amaliy hal qilish uchun yaratilgan. Kotlin ning asosiy tamoyili — dasturchi unumdorligini (developer ergonomics) maksimal darajaga ko'tarishdir.

### 1.2. Readability vs Writeability
Ko'plab dasturlash tillari kodni juda tez yozishga (writeability) urg'u beradi. Biroq dasturiy ta'minot muhandisligida kod yozishdan ko'ra uni o'qish, tushunish va qo'llab-quvvatlashga 10 barobar ko'proq vaqt sarflanadi. Kotlin kodning o'qilishi (readability) birinchi o'ringa qo'yilgan holda loyihalashtirilgan. U qisqa, biroq sirli va chalkash bo'lmagan, har bir iborasi o'z ma'nosini aniq ifoda etuvchi sintaksisga ega.

### 1.3. Java Bilan 100% Ikki Tomonlama Moslik (Interoperability)
Kotlin ning muvaffaqiyatidagi eng katta tayanch — bu mavjud Java ekotizimi bilan mutlaq 100% ikki tomonlama muvofiqlikdir. 
- Kotlin kodidan turib istalgan Java sinfi, kutubxonasi yoki ramkasini hech qanday adapterlarsiz to'g'ridan-to'g'ri chaqirish mumkin.
- Xuddi shunday, Java dasturidan turib ham Kotlin sinflari va kengaytmalarini oddiy statik metodlar kabi chaqirsa bo'ladi.
- Bu xususiyat millionlab qatordan iborat ulkan Java loyihalarini bir zumda emas, balki qadamma-qadam, faylma-fayl Kotlin ga o'tkazish imkoniyatini taqdim etdi.

### 1.4. Null-Safety: "Milliard Dollarlik Xato"ni Bartaraf Etish
Sir Entoni Xoar 1965-yilda `null` ko'rsatkichini ixtiro qilganini "milliard dollarlik xato" deb atagan edi, chunki tarixdagi millionlab dasturlar `NullPointerException` (NPE) tufayli qulagan. 
Kotlin da bu muammo tilning tiplar tizimi (Type System) darajasida yechildi:
- Null bo'la olmaydigan tiplar: `String`, `Int`, `User` (hech qachon null bo'lishi mumkin emas, kompilyator kafolat beradi).
- Null bo'lishi mumkin bo'lgan tiplar: `String?`, `Int?`, `User?` (null saqlashi mumkin, lekin ularga to'g'ridan-to'g'ri murojaat qilish taqiqlanadi).
- Xavfsiz chaqiruv (`?.`), Elvis operatori (`?:`), Smart Cast (`if (x != null)`) orqali kodda kutilmagan qulashlar ehtimoli deyarli nolga tushirildi.

### 1.5. O'zgarmaslik (Immutability) Birinchi Darajali Fuqaro Sifatida
Zamonaviy dasturlashda holatning (state) kutilmagan tarzda o'zgarishi ko'p oqimli tizimlarda eng xatarli xatolarni keltirib chiqaradi. Kotlin dasturchilarni doimo o'zgarmaslikka undaydi:
- `val` (read-only) o'zgaruvchilari `var` (mutable) dan ustun qo'yiladi.
- Kolleksiyalar qat'iy ikkiga bo'lingan: `List` (o'qiluvchi, o'zgarmas) va `MutableList` (o'zgartiriladigan).
- Data class lardagi `copy()` mexanizmi orqali mavjud obyektni o'zgartirmasdan, uning yangi nusxasini yaratish tavsiya etiladi.

---

## 2. KOTLIN K2 YANGI KOMPILYATOR ARXITEKTURASI

Kotlin 2.0 ning chiqarilishi til tarixidagi eng ulkan bosqich bo'ldi. Uning zamirida noldan qayta yozilgan yangi K2 kompilyatori yotadi.

### 2.1. Eski Kompilyator (K1) Cheklovlari
Eski K1 kompilyatori dastlab IntelliJ IDEA plaginining ichki tuzilmasiga (PSI - Program Structure Interface) qattiq bog'langan edi:
- **PSI va BindingContext**: K1 tahlil vaqtida butun kod daraxtini xotiradagi ulkan `BindingContext` xaritasiga bog'lar edi. Bu juda ko'p operativ xotira (RAM) talab qilar va yirik loyihalarda kompilyatsiyani sekinlashtirar edi.
- **Platformalararo farqlar**: Har bir platforma (JVM, JS, Native) o'zining mustaqil frontendiga ega bo'lib, til xususiyatlari ba'zan har xil platformada turlicha xatti-harakat ko'rsatar edi.

### 2.2. K2 Yangi Frontend IR (FIR) Arxitekturasi
K2 kompilyatori ushbu arxitekturani butunlay yangiladi:
- **FIR (Frontend Intermediate Representation)**: Kod avval engil va samarali semantik daraxtga (FIR) o'giriladi. FIR faqat zaruriy sintaksis va semantika ma'lumotlarini saqlaydi, xotirani minimal darajada band qiladi.
- **Yagona Frontend**: Barcha platformalar (Kotlin/JVM, Kotlin/Native, Kotlin/Wasm, Kotlin/JS) uchun yagona umumiy K2 Frontendi xizmat qiladi. Bu barcha platformalarda 100% bir xil xulq-atvor va qat'iy mantiqni ta'minlaydi.

### 2.3. Kompilyatsiya Tezligi va Samaradorligi
Amaliy testlar va yirik korporativ loyihalarda o'tkazilgan o'lchovlarga ko'ra:
- K2 kompilyatsiya tezligini K1 ga nisbatan **2 baravardan ortiq (2x+)** oshiradi.
- Kompilyator sarflaydigan xotira (RAM footprint) sezilarli darajada kamaydi.
- Paralellizatsiya imkoniyatlari kengaytirildi, bu esa ko'p yadroli zamonaviy protsessorlarda loyihalarni yashin tezligida yig'ishga (build) imkon beradi.

### 2.4. Smart Cast 2.0 va Mukammal Type Inference
K2 kompilyatorida ma'lumot turini avtomatik aniqlash (Type Inference) va aqlli turga o'tkazish (Smart Cast) yangi bosqichga ko'tarildi:
- Murakkab mantiqiy ifodalar (`if (a is String || b is String)`) ichida turlar yanada chuqurroq tahlil qilinadi.
- Mahalliy o'zgaruvchilar lambdalar ichida chaqirilganda ham, agar ular o'zgarmasligi kafolatlangan bo'lsa, Smart Cast o'z kuchini saqlab qoladi.
- Sikllar va shartli tarmoqlanishlarda turlarning torayishi (type narrowing) qat'iy matematik aniqlikda ishlaydi.

### 2.5. Kompilyator Plaginlari va Jetpack Compose Integratsiyasi
Kotlin 2.0 bilan birgalikda Android Jetpack Compose Compiler rasman alohida kutubxona bo'lishdan to'xtab, to'g'ridan-to'g'ri Kotlin kompilyatori omboriga birlashtirildi. Endi Kotlin versiyasi yangilanganda Compose versiyasini kutib o'tirish zarurati yo'qoldi; ular doimo sinxron va mukammal integratsiyalashgan holda yetkazib beriladi.

---

## 3. BAYT-KOD DEKOMPILYATSIYASI: KOTLIN KAPOT OSTIDA (UNDER THE HOOD)

Kotlin ning eng buyuk qudrati shundaki, u ishlab chiquvchiga juda chiroyli va yuqori darajali sintaksis beradi, biroq JVM platformasida barcha kodlar eng tejamkor va optimallashtirilgan Java bayt-kodiga kompilyatsiya qilinadi.

### 3.1. `val` va `var` Maydonlarining Dekompilyatsiyasi
Kotlin da e'lon qilingan sinf:
```kotlin
class Person(val id: Int, var name: String)
```
Java bayt-kodidan dekompilyatsiya qilinganda quyidagi shaklga keladi:
```java
public final class Person {
    private final int id;
    private String name;

    public Person(int id, String name) {
        this.id = id;
        this.name = name;
    }

    public final int getId() { return this.id; }
    public final String getName() { return this.name; }
    public final void setName(String name) { this.name = name; }
}
```
Ko'rib turganingizdek:
- `val` faqat xususiy `final` maydon va ommaviy `getId()` getter metodini hosil qiladi.
- `var` esa xususiy maydon, getter va `setName()` setter metodlarini yaratadi.
- Hech qanday sehr yo'q: Kotlin qat'iy enkapsulyatsiya qoidalarini avtomatik bayt-kodga aylantiradi.

### 3.2. Data Class larning Dekompilyatsiyasi
Data class yozganimizda:
```kotlin
data class User(val id: Int, val name: String)
```
Kompilyator orqa fonda biz uchun quyidagi to'liq metodlar to'plamini avtomatik ishlab chiqadi:
1. `equals(Object other)`: barcha konstruktor maydonlarini qat'iy solishtiradi.
2. `hashCode()`: maydonlar asosida hisoblangan noyob butun sonli xesh kod.
3. `toString()`: `"User(id=1, name=Ali)"` ko'rinishidagi o'qishli matn.
4. `component1()` va `component2()`: destrukturizatsiya (`val (id, name) = user`) uchun xizmat qiluvchi metodlar.
5. `copy(id, name)`: mavjud obyektning barcha yoki ba'zi maydonlarini o'zgartirib yangi nusxa oluvchi metod.

### 3.3. Extension Funksiyalarning Ichki Siri
Kotlin dagi kengaytma funksiyalar:
```kotlin
fun String.firstChar(): Char = this[0]
```
Java ga dekompilyatsiya qilinganda quyidagi statik metodga aylanadi:
```java
public final class StringExtensionsKt {
    public static final char firstChar(String $this$firstChar) {
        return $this$firstChar.charAt(0);
    }
}
```
**Xulosa**: Extension funksiyalar mavjud sinfning bayt-kodini o'zgartirmaydi! Ular shunchaki qabul qiluvchi obyektni (receiver) birinchi parametr sifatida oluvchi oddiy statik yordamchi (static utility) funksiyalardir.

### 3.4. `inline`, `noinline`, `crossinline` ning Bayt-kod Darajasidagi Kuchi
Oddiy yuqori tartibli funksiya chaqirilganda har bir lambda uchun JVM da `Function` anonim sinfi va uning yangi obyekti yaratiladi. Bu esa sikllar ichida xotira to'lishiga (Garbage Collection overhead) olib keladi.
`inline` kalit so'zi qo'yilganda:
```kotlin
inline fun measureTime(block: () -> Unit) {
    val start = System.currentTimeMillis()
    block()
    println(System.currentTimeMillis() - start)
}
```
Kompilyator bayt-kod yaratishda chaqiruvchi joyga hech qanday funksiya chaqiruvini qoldirmaydi, balki `block()` ning butun tanasini to'g'ridan-to'g'ri o'sha joyga nusxalab qo'yadi (inlining). Natijada:
- Nol ob'yekt allokatsiyasi (Zero object allocations).
- Hech qanday virtual metod chaqiruvi (No virtual call overhead).
- To'g'ridan-to'g'ri qadam-baqadam mashina kodi tezligida bajarilish.

### 3.5. Suspend Funksiyalar va State Machine Dekompilyatsiyasi
Kotlin koroutinalarining eng ajoyib qismi — ularning to'xtatilishi va qayta tiklanishidir. Bu bayt-kodda qanday ishlaydi?
Har bir `suspend` funksiyaning so'nggi yashirin parametri sifatida `Continuation<T>` obyekti qo'shiladi (CPS - Continuation Passing Style):
```kotlin
suspend fun fetchData(): String {
    delay(100L)
    return "Ma'lumot"
}
```
Kompilyator ushbu funksiyani ichki Holat Mashinasi (State Machine) ga o'giradi:
```java
public Object fetchData(Continuation completion) {
    // Holat mashinasi obyekti yaratiladi yoki qayta ishlatiladi
    int label = ...;
    switch (label) {
        case 0:
            label = 1;
            // delay chaqiriladi va agar u hali tugamagan bo'lsa,
            // COROUTINE_SUSPENDED maxsus belgisi qaytariladi
            if (DelayKt.delay(100L, this) == COROUTINE_SUSPENDED) return COROUTINE_SUSPENDED;
        case 1:
            // Oqim bo'shagan paytda taymer tugagach, shu nuqtaga sakrab kelinadi
            return "Ma'lumot";
    }
}
```
Ushbu dekompilyatsiya ko'rsatadiki, suspend funksiyalar operatsion tizim oqimlarini qotirmaydi. Ular oddiy Java `switch(label)` tarmog'i bo'lib, o'z holatini `Continuation` obyektida saqlab chiqib ketadi va tayyor bo'lgach keyingi `case` ga qaytadi.

---

## 4. KOTLIN KOROUTINALARI VA REAKTIV DASTURLASH ARXITEKTURASI

### 4.1. Threads vs Coroutines
| Ko'rsatkich | Operatsion Tizim Oqimi (OS Thread) | Kotlin Koroutinasi (Coroutine) |
| :--- | :--- | :--- |
| **Boshqaruvchi** | OT Yadrosi (OS Kernel) | Foydalanuvchi doirasida (User-space Runtime) |
| **Xotira sarfi** | Har bir oqim uchun ~1 MB stack | Har bir koroutina uchun bir necha o'n bayt |
| **Kontekst almashish** | Qimmat (Kernel context switch, CPU registrlari) | Arzon (Oddiy Kotlin metod chaqiruvi va label o'zgarishi) |
| **Chegara** | Bir necha mingta (undan keyin OutOfMemoryError) | Millionlab parallel koroutinalar erkin ishlaydi |
| **Bloklanish** | Oqim uxlaganda CPU yadrosi bo'sh turadi | delay() da oqim boshqa koroutinalarga beriladi |

### 4.2. Strukturalangan Konkurentlik (Structured Concurrency)
Kotlin koroutinalari tasodifiy fonda yo'qolib ketuvchi (fire-and-forget) jarayonlar emas. Ular qat'iy iyerarxik ota-bola (parent-child) bog'lanishiga ega:
1. Bola koroutina xatolik bilan qulasa, uning otasi xabardor qilinadi va qolgan barcha birodar bolalar avtomatik bekor qilinadi.
2. Ota koroutina bekor qilinsa, uning barcha avlodlari kaskadli ravishda to'xtatiladi.
3. Ota koroutina o'zining barcha bolalari to'liq yakunlanmaguncha o'zi ham tugallanmaydi.
Bu arxitektura xotirada sarson yurgan oqimlar (leaked threads) muammosiga butunlay barham beradi.

### 4.3. Kotlin Flow: Cold vs Hot Streams
- **Flow (Cold Stream)**: Sovuq oqim buyurtma bo'yicha ishlaydi. Hech kim `collect()` chaqirmasa, uning ichida hech qanday hisoblash bo'lmaydi. Har bir obunachi uchun ma'lumotlar noldan qayta chiqariladi.
- **StateFlow (Hot Stream)**: Doimo bitta joriy qiymatga ega bo'lgan reaktiv holat modeli. U obunachilar bor-yo'qligidan qat'i nazar o'z holatini xotirada saqlaydi va UI bilan ishlashda Android ViewModel larining tayanchidir.
- **SharedFlow (Hot Stream)**: Bir nechta abonentlarga bir martalik hodisalarni (masalan Toast xabarlari, ekran navigatsiyasi) tarqatish (broadcast) uchun eng ideal reaktiv kanaldir.

---

## 5. KOTLIN MULTIPLATFORM (KMP) ENSIKLOPEDIYASI

### 5.1. KMP Falsafasi
Boshqa krossplatforma texnologiyalaridan (Flutter, React Native) farqli o'laroq, Kotlin Multiplatform butun UI ni bitta qolipga solishga majburlamaydi. Uning shiori: **"Biznes mantiqni ulashing, UI ni esa har bir platformaning o'ziga mos, sof va tabiiy holda qoldiring."** (Shu bilan birga Compose Multiplatform orqali xohlaganlar UI ni ham 100% ulashishi mumkin).

### 5.2. Platformalar va Arxitektura
- **commonMain**: Sof Kotlin da yozilgan biznes mantiq, UseCase lar, Repozitoriylar, modellar, tarmoq chaqiruvlari.
- **androidMain**: Android SDK ga to'liq kirish huquqiga ega qatlam.
- **iosMain**: Kotlin/Native orqali to'g'ridan-to'g'ri Apple ning Objective-C / Swift runtime va Framework lari (Foundation, UIKit) bilan bog'lanuvchi qatlam.
- **jvmMain**: Server (Ktor, Spring Boot) va Desktop ilovalari.
- **wasmJsMain**: Veb-brauzerlar uchun yuqori tezlikdagi WebAssembly binar kodi.

### 5.3. `expect` va `actual` Mexanizmi
Umumiy modulda e'lon qilinadi:
```kotlin
// commonMain
expect fun getDeviceIdentifier(): String
```
Platformalarga xos modullarda amalga oshiriladi:
```kotlin
// androidMain
actual fun getDeviceIdentifier(): String = android.os.Build.MODEL

// iosMain
actual fun getDeviceIdentifier(): String = UIDevice.currentDevice.model
```
Kompilyatsiya vaqtida Kotlin K2 kompilyatori `expect` deklaratsiyasini tegishli `actual` realizatsiyasi bilan mustahkam bog'laydi. Hech qanday sekinlashtiruvchi reflection ishlatilmaydi.

### 5.4. Kotlin/Native Yangi Xotira Modeli
Eski Kotlin/Native xotira modeli ob'yektlarni oqimlar orasida muzlatishni (freezing) talab qilar va juda ko'p noqulayliklar keltirib chiqarar edi. Yangi Kotlin/Native arxitekturasida:
- Java JVM kabi to'liq erkin xotira modeli joriy qilindi.
- Yangi avlod Zaxiraviy Chiqindi Yig'uvchisi (Concurrent Garbage Collector) ishga tushirildi.
- Oqimlar o'rtasida ma'lumotlarni almashish hech qanday qiyinchiliksiz va xavfsiz amalga oshiriladi.

---

## 6. ZAMONAVIY ANDROID ARXITEKTURASI VA JETPACK COMPOSE

### 6.1. Deklarativ UI vs Imperativ XML
Eski Android dunyosida UI XML fayllarda e'lon qilinib, Kotlin kodida `findViewById()` orqali imperativ ravishda qo'lda boshqarilar edi (`textView.setText(...)`). Bu juda ko'p xatolarga (holat sinxronizatsiyasi buzilishi) olib kelardi.
Jetpack Compose deklarativ paradigmadir:
- **UI = f(State)**: Foydalanuvchi interfeysi joriy holatning sof matematik funksiyasidir.
- Holat o'zgarganda, Compose aqlli ravishda faqat o'sha o'zgargan vidjetlarnigina qayta chizadi (Smart Recomposition).

### 6.2. Clean Architecture Qatlamlari
Zamonaviy Android loyihasi 3 ta mustaqil qatlamga bo'linadi:
1. **Presentation Layer**: Jetpack Compose ekranlari, StateFlow lar bilan boshqariluvchi ViewModel lar va MVI Intentlari.
2. **Domain Layer**: Sof Kotlin biznes mantiqi, Entity modellar va aniq bitta mas'uliyatga ega UseCase lar.
3. **Data Layer**: Repository realizatsiyalari, Ktor/Retrofit tarmoq manbalari va Room Database lokal ombori.

### 6.3. Dependency Injection: Koin vs Dagger Hilt
- **Dagger Hilt**: Kompilyatsiya vaqtida kod generatsiya qiladi. Qat'iy va tez, biroq loyihani yig'ish (build time) vaqtini oshirishi mumkin.
- **Koin**: Sof Kotlin DSL ga asoslangan, hech qanday kod generatsiyasiz, juda yengil va ayniqsa Kotlin Multiplatform (Android + iOS) loyihalarida yagona universal DI vositasi sifatida porlamoqda.

---

## 7. MOBIL SUN'IY INTELLEKT VA AI AGENTLAR KELAJAGI KOTLINDA

2026-yilga kelib mobil dasturlash oddiy ekran chizishdan to'liq aqlli avtonom Mobil AI Agentlar davriga qadam qo'ydi.

### 7.1. On-Device AI (Gemini Nano)
Serverga so'rov yubormasdan, bevosita qurilmaning o'zidagi NPU (Neural Processing Unit) mikrosxemalarida ishlaydigan kichik modellar:
- To'liq 100% maxfiylik (foydalanuvchi ma'lumotlari qurilmadan tashqariga chiqmaydi).
- Nollik internet talabi (to'liq offline rejimda ishlaydi).
- Android AICore drayverlari orqali Kotlin ilovalariga integratsiya qilinadi.

### 7.2. Token Streaming va Asinxron UX
Foydalanuvchini sekin generatsiya bilan zeriktirmaslik uchun, zamonaviy mobil AI integratsiyasi Ktor HTTP Client ning Server-Sent Events (SSE) imkoniyatlaridan foydalanib, kelayotgan har bir token so'zini Kotlin `Flow<String>` ga aylantiradi va Jetpack Compose ekranda jonli yozuv mashinkasi (Typewriter) effektida render qiladi.

### 7.3. Mobil Function Calling (Tool Use)
AI modeliga qurilma imkoniyatlarini (asboblarini) berish:
- AI foydalanuvchi niyatini tahlil qiladi (Intent recognition).
- Agar kerak bo'lsa, JSON shaklida buyruq generatsiya qiladi (masalan: `{"action": "set_alarm", "time": "07:30"}`).
- Kotlin kodi ushbu buyruqni qabul qilib, Android AlarmManager yoki Room bazasi orqali harakatni bajaradi va natijani yana AI ga qaytaradi.

### 7.4. Mobil Local RAG (Retrieval-Augmented Generation)
Telefon ichidagi shaxsiy yozuvlar, chatlar yoki hujjatlarni Room Database da saqlab, foydalanuvchi savol bergan paytda lokal bazadan eng mos keluvchi kontekstni qidirib topish va so'rovga qo'shib LLM ga uzatish tizimi. Bu orqali mobil AI agent mutlaqo aniq va xolis javoblarni taqdim etadi.

---

## 8. ENG YAXSHI AMALIYOTLAR, KOD USLUBI VA ANTIPATERNLAR (BEST PRACTICES)

### 8.1. Qat'iyan Saqlanish Kerak Bo'lgan Xatolar (Anti-Patterns)
1. **GlobalScope dan foydalanish**: Hech qachon `GlobalScope.launch` qilmang! U ota-bola bog'liqligini uzadi va xotira sizib chiqishiga olib keladi. Har doim `coroutineScope`, `viewModelScope` yoki o'zingizning boshqariladigan `CoroutineScope` ingizdan foydalaning.
2. **Not-null Assertion (`!!`) ni suiiste'mol qilish**: `!!` operatori Kotlin null-safety himoyasini kuch bilan sindiradi. Uning o'rniga Elvis operatori (`?:`), `let`, yoki `checkNotNull()` dan foydalaning.
3. **Recomposition ichida og'ir hisoblashlarni bajarish**: `@Composable` funksiyasi har millisekundda qayta chaqirilishi mumkin. Hech qachon uning to'g'ridan-to'g'ri tanasida ma'lumotlarni saralamang yoki o'qimang; har doim `remember` yoki `derivedStateOf` ga o'rang.
4. **CancellationException ni yutib yuborish**: Koroutinalarda `catch (e: Exception)` qilganda agar `e is CancellationException` bo'lsa, uni albatta qayta tashlang (`throw e`), aks holda koroutinani to'xtatib bo'lmaydi.

### 8.2. Yuqori Samaradorlik Sirlari
- **Value Classes (`@JvmInline value class`)**: Bitta qiymatni o'rab turuvchi turlar uchun qo'shimcha obyekt yaratmasdan, bayt-kod darajasida to'g'ridan-to'g'ri oddiy ibtidoiy (primitive) songa aylantiradi.
- **Kolleksiyalarda Sequences**: 100,000 dan ortiq elementga ega ro'yxatlarni bir nechta zanjirli operatsiyalar bilan (`filter`, `map`) qayta ishlayotganda `asSequence()` dan foydalaning — u oraliq ro'yxatlar yaratmasdan xotirani tejaydi.
- **Strong Skipping Mode Compose da**: Kotlin 2.0 da barcha Composable funksiyalar standart tarzda barqaror bo'lmagan parametrlar uchun ham keraksiz qayta chizilishlarni o'tkazib yubora oladi.

---

## 9. XULOSA VA KOTLIN DASTURCHISINING YO'L XARITASI (ROADMAP)

Ushbu 1,000 ta amaliy topshiriq va ensiklopediya qo'llanmasi orqali siz Kotlin dasturlash tilining barcha qatlamlarini: eng oddiy sintaksisdan tortib, K2 kompilyatori, bayt-kod sirlari, koroutinalar, reaktiv oqimlar, Jetpack Compose, Kotlin Multiplatform va Mobil AI Agent tizimlarigacha to'liq egalladingiz.

### Tavsiya etiladigan amaliy qadamlar:
1. **Nazariyani amaliyotda mustahkamlash**: 1-fayldan 20-faylgacha bo'lgan har bir topshiriq kodini mustaqil tahlil qiling.
2. **K2 imkoniyatlaridan to'liq foydalanish**: Loyihalaringizni eng so'nggi Kotlin 2.0+ versiyasiga o'tkazing va kompilyatsiya tezligi hamda Smart Cast afzalliklaridan bahramand bo'ling.
3. **KMP va Mobil AI yo'nalishida loyihalar qurish**: Faqat bitta platformaga yopishib qolmasdan, umumiy biznes mantiq va aqlli agentik xususiyatlarga ega zamonaviy ilovalarni yarating.

Kotlin — bu nafaqat bugungi kunning eng yetuk tili, balki kelajakning eng ilg'or, moslashuvchan va qudratli dasturlash platformasidir!
"""

with open(out_path, "w", encoding="utf-8") as f:
    f.write(content.strip() + "\n")

print(f"Muvaffaqiyatli saqlandi: {out_path} ({len(content)} belgi)")
