# Swift: Mukammal Ensiklopediya va Fundamental Qo'llanma
**Loyiha:** Khorazmiy AI — O'zbek Tilidagi Katta Dasturlash Dataseti  
**Muallif:** Khorazmiy AI Swift Dataset Specialist  
**Versiya:** Swift 5.9 / Swift 6 (2026-yil holatiga)  
**Qamrovi:** Swift tili falsafasi, Kompilyatsiya tizimi (SIL), Xotira boshqaruvi (ARC), Protokolga yo'naltirilgan dasturlash (POP), Swift Concurrency va Data-Race Safety, Reaktiv SwiftUI, CoreML va On-Device AI Agentlar arxitekturasi.

---

## Mundarija
1. [Kirish va Swift Evolyutsiyasi](#1-kirish-va-swift-evolyutsiyasi)
2. [Kompilyator Arxitekturasi: Parser, SIL va LLVM](#2-kompilyator-arxitekturasi-parser-sil-va-llvm)
3. [Tiplar Tizimi va Semantika: Value vs Reference Types](#3-tiplar-tizimi-va-semantika-value-vs-reference-types)
4. [Xotira Boshqaruvi va ARC (Automatic Reference Counting)](#4-xotira-boshqaruvi-va-arc-automatic-reference-counting)
5. [Protokolga Yo'naltirilgan Dasturlash (POP) va Generiklar](#5-protokolga-yonaltirilgan-dasturlash-pop-va-generiklar)
6. [Swift 6 Structured Concurrency va Data-Race Safety](#6-swift-6-structured-concurrency-va-data-race-safety)
7. [SwiftUI: Deklarativ UI va Reaktiv Holat Arxitekturasi](#7-swiftui-deklarativ-ui-va-reaktiv-holat-arxitekturasi)
8. [Apple Silicon, CoreML va On-Device Sun'iy Intellekt](#8-apple-silicon-coreml-va-on-device-suniy-intellekt)
9. [Mobil Dasturiy Ta'minot Arxitekturalari (MVVM, Clean Architecture)](#9-mobil-dasturiy-taminot-arxitekturalari-mvvm-clean-architecture)
10. [Professional Xulosa va Best Practices](#10-professional-xulosa-va-best-practices)

---

## 1. Kirish va Swift Evolyutsiyasi

Swift tili 2014-yilda Apple kompaniyasi (Kris Lattner boshchiligidagi jamoa) tomonidan Objective-C tilining o'rnini bosuvchi zamonaviy, xavfsiz va yuqori unumdor tizimli til sifatida taqdim etildi. 2015-yilda til ochiq kodli (open-source) deb e'lon qilindi va bugungi kunda nafaqat iOS, iPadOS, macOS, watchOS, tvOS va visionOS platformalarida, balki Linux va Windows server dasturlashida ham keng qo'llanilmoqda.

### Swift Falsafasining Uch Ustuni:
1. **Xavfsiz (Safe):** Swift dasturlash xatolarining oldini kompilyatsiya bosqichidayoq olishga intiladi. Null pointer muammosini yo'q qiluvchi `Optionals`, tiplar xavfsizligi (Type Safety), xotirani nazoratsiz o'zgartirishdan asrovchi o'zgarmaslik (`let` vs `var`) va Swift 6 bilan to'liq tatbiq etilgan xotira poygalaridan (Data-Race Safety) himoya.
2. **Tezkor (Fast):** Swift C va C++ tillari bilan raqobatlasha oladigan tezlikka ega. Unda dinamik runtime dispatch o'rniga statik metod chaqiruvlari (Static / VTable Dispatch), aggressively inlining va LLVM optimizatsiyalari qo'llaniladi.
3. **Ifodali (Expressive):** Python va Ruby kabi skript tillarining qulay sintaksisi, pattern matching, closures, operator overloading, shuningdek Swift 5.9-da taqdim etilgan qudratli Makroslar (Swift Macros) tizimi kodni qisqa va tushunarli qilishga xizmat qiladi.

---

## 2. Kompilyator Arxitekturasi: Parser, SIL va LLVM

Swift kompilyatori (`swiftc`) oddiy matnli kodni mashina binariga aylantirishda murakkab va yuqori darajada optimallashgan ko'p bosqichli konveyerdan (pipeline) foydalanadi:

```
[Swift Manba Kodi (.swift)]
           │
           ▼
     [Parsing & AST]
           │
           ▼
 [Semantik Tahlil & Type Check]
           │
           ▼
[SIL Generation (Xom SIL)]
           │
           ▼
[SIL Optimizatsiyalari (Definite Init, ARC, Inlining)]
           │
           ▼
     [LLVM IR Generatsiyasi]
           │
           ▼
  [LLVM Backend Optimizatsiyalari]
           │
           ▼
[Mashina Kodi: ARM64 / x86_64 Binar]
```

### Swift Intermediate Language (SIL) nima?
Ko'plab tillar to'g'ridan-to'g'ri AST-dan LLVM IR generatsiya qilsa, Swift o'rtada **SIL (Swift Intermediate Language)** deb nomlangan maxsus oraliq tilni kiritgan. SIL Swift-ga quyidagi tahlillarni amalga oshirishga imkon beradi:
- **Definite Initialization:** Barcha o'zgaruvchilar va maydonlar ishlatilishidan oldin 100% initsializatsiya qilinganligini isbotlash.
- **ARC Optimizatsiyasi:** Ortiqcha `retain` va `release` chaqiruvlarini yo'qotish va xotira harakatlarini minimallashtirish.
- **Generic Specialization:** Umumiy generik funksiyalarni aniq tiplar (masalan `Array<Int>`) uchun maxsus tezkor funksiyalarga nusxalash (monomorphization).
- **Dead-Code Elimination:** Ishlatilmaydigan kod bloklarini xotira va binar hajmidan o'chirish.

---

## 3. Tiplar Tizimi va Semantika: Value vs Reference Types

Swift-dagi barcha tiplar ikkita katta toifaga bo'linadi: **Qiymat tiplari (Value Types)** va **Havola tiplari (Reference Types)**.

### Qiymat Tiplari (`struct`, `enum`, `tuple`):
- O'zgaruvchiga berilganda yoki funksiyaga uzatilganda uning mustaqil nusxasi olinadi.
- Stack xotirasida juda yengil va tezkor saqlanadi (agar katta hajmda bo'lmasa).
- Ko'p oqimli muhitda tabiiy ravishda thread-safe hisoblanadi, chunki har bir oqim o'z nusxasi ustida ishlaydi.
- Swift-dagi asosiy tiplar: `Int`, `Double`, `String`, `Array`, `Dictionary`, `Set` barchasi `struct` hisoblanadi.

### Copy-on-Write (COW) Mexanizmi:
`String` va `Array` kabi katta tuzilmalar nusxalanganda, xotira sarfini tejash uchun ular darhol nusxa ko'chirilmaydi. Ular xotiradagi bitta buferga qarab turadi. Faqat nusxalardan biri o'zgartirilgan lahzada (mutation) Swift `isKnownUniquelyReferenced` orqali yangi chuqur nusxani ajratadi.

### Havola Tiplari (`class`, `actor`, `closure`):
- Xotiraning Heap sohasida joylashadi.
- O'zgaruvchilar obyektning o'zini emas, uning xotiradagi manzilini (pointer) ushlaydi.
- Bir nechta o'zgaruvchilar bitta umumiy holatni bo'lishadi (Shared Mutable State).

| Mezon | Value Type (Struct) | Reference Type (Class) | Actor |
|---|---|---|---|
| **Xotira maydoni** | Asosan Stack | Heap | Heap |
| **Nusxalash usuli** | To'liq qiymat nusxasi | Manzil nusxasi (Reference) | Manzil nusxasi |
| **Merosxo'rlik** | Yo'q (faqat protokollar) | Bor (Single inheritance) | Yo'q (faqat protokollar) |
| **Xotira boshqaruvi**| Avtomatik (Scope-based) | ARC (Retain count) | ARC (Retain count) |
| **Thread Safety** | Yuqori | Xavfli (Lock talab qiladi) | Avtomatik (Data isolation) |

---

## 4. Xotira Boshqaruvi va ARC (Automatic Reference Counting)

Swift avtomatik axlat yig'uvchi (Garbage Collector) ishlatmaydi. Buning o'rniga deterministik **ARC (Automatic Reference Counting)** mexanizmidan foydalanadi. Obyektning reference count hisoblagichi 0 ga tushgan onda uning `deinit` metodi chaqiriladi va xotira zudlik bilan operatsion tizimga qaytariladi.

### Retain Cycle (Xotira Sizishi - Memory Leak):
Agar ikkita obyekt bir-biriga `strong` havola qilsa, ularning reference counti hech qachon 0 ga tushmaydi. Natijada ilova RAM xotirasini behuda band qilib, vaqt o'tishi bilan tizim tomonidan yopib yuboriladi (OOM Crash).

### Yechimlar:
1. **`weak` havolasi:** Reference countni oshirmaydi. Obyekt yo'q qilinganda avtomatik `nil`ga aylanadi. Shuning uchun `weak` har doim ixtiyoriy (`weak var delegate: SomeDelegate?`) bo'lishi shart.
2. **`unowned` havolasi:** Reference countni oshirmaydi, lekin obyekt mavjud bo'lishiga kafolat beradi (non-optional). Agar obyekt o'chirilgandan so'ng `unowned` ga murojaat qilinsa, runtime crash beradi.
3. **Closure Capture List:** Closurlar ichida `self` kuchli saqlanib qolmasligi uchun `[weak self]` sintaksisidan foydalaniladi:
   ```swift
   tarmoqSo'rovi { [weak self] in
       guard let self else { return }
       self.ekranniYangilash()
   }
   ```

---

## 5. Protokolga Yo'naltirilgan Dasturlash (POP) va Generiklar

Swift dunyoda birinchi **Protocol-Oriented Programming (POP)** tili sifatida e'tirof etiladi. Obyektga yo'naltirilgan dasturlashdagi (OOP) sinflar iyerarxiyasining qattiqligi va ko'p tomonlama merosxo'rlik muammolari Swift-da protokollar va ularning kengaytmalari (Protocol Extensions) orqali yengiladi.

### POP Afzalliklari:
- Har qanday tip (`struct`, `enum`, `class`) protokollarni qabul qilishi mumkin.
- Protokol kengaytmasi orqali interfeysga standart amalga oshirish (Default Implementation) berish mumkin.
- Gorizontal kompozitsiya: Obyekt bir vaqtning o'zida `Identifiable`, `Codable`, `Equatable`, `Hashable` bo'la oladi.

### Generiklar va Cheklovlar (Type Constraints):
Swift-dagi generiklar kodni bitta yozib, har qanday tip uchun xavfsiz ishlatish imkonini beradi:
```swift
func ikkitaElementniAlmashtir<T>(_ a: inout T, _ b: inout T) {
    let vaqtincha = a
    a = b
    b = vaqtincha
}
```
`some` va `any` kalit so'zlari (Opaque Types vs Existentials) orqali xotira allokatsiyasini optimallashtirish zamonaviy Swift-ning eng ilg'or yo'nalishidir.

---

## 6. Swift 6 Structured Concurrency va Data-Race Safety

Swift 6 versiyasining eng ulug'vor inqilobi — bu **Data-Race Safety by Default** (birlamchi xotira poygasi xavfsizligi) hisoblanadi.

### Asosiy Elementlar:
- **`async/await`:** Callback Hell va delegatsiya zanjirlarini yo'qotib, asinxron kodni xuddi sinxron kod kabi toza, chiziqli o'qish imkonini beradi.
- **`Task` va `TaskGroup`:** Tuzilmali ko'p oqimlilik (Structured Concurrency). Bola vazifalar ota vazifa tugashidan oldin tugashi yoki bekor qilinishi kafolatlanadi.
- **`actor`:** O'z ichki holatini tashqi dunyodan himoya qiluvchi, barcha metod va maydonlariga kirishni bitta oqim bo'yicha ketma-ketlashtiruvchi (serialization) xavfsiz reference tipi.
- **`@MainActor`:** UI bilan bog'liq barcha harakatlarni avtomatik tarzda asosiy oqimda (Main Thread) bajarilishini kafolatlovchi global aktor.
- **`Sendable` Protokoli:** Oqimlar aro (threads / tasks) xavfsiz uzatish mumkin bo'lgan qiymat tiplarini belgilovchi kontrakt.

---

## 7. SwiftUI: Deklarativ UI va Reaktiv Holat Arxitekturasi

SwiftUI — Apple platformalari uchun yaratilgan deklarativ foydalanuvchi interfeysi freymvorkidir. Unda foydalanuvchi interfeysi holat funksiyasi (`UI = f(State)`) sifatida tavsiflanadi.

### Reaktivlik Zanjiri:
- `@State`: Ko'rinishning lokal ichki holati.
- `@Binding`: Ota ko'rinish va bola ko'rinish o'rtasida ikki tomonlama bog'lanish.
- `@Observable` (Swift 5.9+): Zamonaviy kuzatuv mexanizmi. Klass property-lari o'zgarganda faqat o'sha property ishlatilgan ko'rinishlargina qayta chiziladi (fine-grained rendering).
- `NavigationStack`: Qiymatga asoslangan tiplangan navigatsiya (`navigationDestination(for:)`).
- `ViewModifier`: Komponentlarni toza va modulli uslubda bezatish.

---

## 8. Apple Silicon, CoreML va On-Device Sun'iy Intellekt

Apple M-seriyasi va A-seriyasi chiplari (Apple Silicon) On-Device AI vazifalarini bajarishda jahon yetakchisi hisoblanadi. Uning siri — **Unified Memory Architecture (UMA)** va **Apple Neural Engine (ANE)** apparat blokidadir.

### Nega On-Device AI?
1. **100% Maxfiylik (Privacy):** Foydalanuvchining shaxsiy ma'lumotlari, fotosuratlari va suhbatlari hech qachon serverlarga jo'natilmaydi.
2. **Kechikishsizlik (Zero Latency):** Tarmoqqa murojaat qilinmagani sababli javoblar darhol olinadi.
3. **Oflayn Ishlash:** Internet ulanishi mavjud bo'lmagan sharoitda ham to'liq funksionallik saqlanadi.

### AI Freymvorklari:
- **CoreML:** Neyron to'rlarni ANE, GPU va CPU-da apparat darajasida ishga tushirish.
- **Vision:** Rasmlarni tahlil qilish, yuzlarni, matnlarni (OCR) va shtrix-kodlarni aniqlash.
- **NaturalLanguage:** Tilni aniqlash, so'zlarni leksik tahlil qilish, his-tuyg'ularni (sentiment) baholash va matn embeddinglari.
- **Autonomous AI Agents:** Kichik til modellari (SLM) yordamida ReAct (Reasoning + Acting) sikli bo'yicha mustaqil vazifalarni bajaruvchi, Tool / Function Calling mexanizmlari orqali qurilma imkoniyatlarini boshqaruvchi agentlar.

---

## 9. Mobil Dasturiy Ta'minot Arxitekturalari

Katta hajmdagi professional iOS loyihalari qat'iy arxitektura tamoyillariga asoslanadi.

### 1. MVVM (Model-View-ViewModel)
SwiftUI uchun eng tabiiy arxitektura:
- **Model:** Domen ma'lumotlari va biznes qoidalari.
- **ViewModel (`@Observable`):** Ko'rinish holatini saqlaydi, tarmoq va ma'lumotlar bazasi bilan ishlaydi, UI uchun ma'lumotlarni formatlaydi.
- **View:** Faqat vizual qiyofani aks ettiradi va foydalanuvchi harakatlarini ViewModelga uzatadi.

### 2. Clean Architecture va Repository Pattern
Loyihani uchta asosiy qatlamga ajratish:
- **Domain Layer:** Entities, Use Cases (Interactors) — hech qanday tashqi kutubxonaga bog'liq bo'lmagan sof Swift kodi.
- **Data Layer:** Repositories, Data Sources (API, CoreData/SwiftData, NetworkClient).
- **Presentation Layer:** SwiftUI Views, ViewModels, UI Modifiers.

---

## 10. Professional Xulosa va Best Practices

1. **Strukturalarga ustuvorlik bering:** Agar merosxo'rlik yoki umumiy o'zgaruvchan holat talab etilmasa, doimo `struct` tanlang.
2. **Optionals bilan ehtiyot bo'ling:** Majburiy unwrap (`!`) o'rniga doimo `guard let`, `if let` yoki `??` (nil-coalescing) ishlating.
3. **Retain Cyclelarni kuzating:** Closure capture listlarida `[weak self]` ni unutmang, delegatlarni `weak` qiling.
4. **Swift 6 qoidalariga o'ting:** Global o'zgaruvchilardan saqlaning, parallel jarayonlarni `actor` va `TaskGroup` bilan himoyalang.
5. **On-Device AI imkoniyatlarini qo'llang:** Ilovalaringizga CoreML, Vision va NaturalLanguage orqali zamonaviy intellektual xususiyatlarni qo'shing.

---
*Khorazmiy AI — O'zbekistonning milliy ta'limiy va texnologik intellektual kelajagi uchun maxsus tayyorlandi.*
