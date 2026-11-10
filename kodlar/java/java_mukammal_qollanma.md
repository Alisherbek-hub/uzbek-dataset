# Java Mukammal Qo'llanma: JVM Arxitekturasi, Xotira Modeli, JIT va Enterprise Amaliyotlar

## Kirish va Java Ekotizimi Falsafasi

Java — 1995-yilda Sun Microsystems (hozirda Oracle) tomonidan taqdim etilganidan buyon dunyodagi eng yirik korporativ tizimlar, banklar, telekom va bulutli platformalarning asosi bo'lib xizmat qilib kelmoqda. Uning mashhur shiori: **"Write Once, Run Anywhere" (WORA)** — ya'ni "Bir marta yoz, hamma joyda ishlat".

Ushbu tamoyilning zamirida **Java Virtual Machine (JVM)** yotadi. Java dasturchisi yozgan kod to'g'ridan-to'g'ri operatsion tizimning mashina kodiga emas, balki oraliq **Baytkod (Bytecode - `.class` fayllar)** ga kompilyatsiya qilinadi. Har qanday operatsion tizimda mos JVM mavjud bo'lsa, o'sha baytkod aynan bir xil mantiq bilan bekamu-ko'st ishlayveradi.

Bugungi kunda Java (ayniqsa Java 21 LTS va Java 23 ekotizimi) o'zining Virtual Threads (Project Loom), Generational ZGC, Pattern Matching, Sealed sinflar va GraalVM AOT texnologiyalari bilan dunyoning eng zamonaviy, xavfsiz va yuqori unumdor dasturlash tillari orasida yetakchilik qilmoqda.

---

## 1. JVM Umumiy Arxitekturasi

JVM asosan uchta yirik tizimdan iborat:
1. **Classloader Subsystem** (Sinflarni yuklash quyi tizimi)
2. **Runtime Data Areas** (Bajarilish vaqtidagi xotira hududlari)
3. **Execution Engine** (Bajarilish dvigateli: Interpreter, JIT Compiler, Garbage Collector)

```
+-----------------------------------------------------------------+
|                    Classloader Subsystem                        |
|   Loading (Bootstrap, Platform, App) -> Linking -> Initializing |
+-----------------------------------------------------------------+
                                 |
                                 v
+-----------------------------------------------------------------+
|                      JVM Memory Areas                           |
|  +-----------------------+  +--------------------------------+  |
|  |     Heap Xotira       |  |      Metaspace (Native)        |  |
|  | (Eden, S0, S1, Old)   |  | (Klass metama'lumotlari)       |  |
|  +-----------------------+  +--------------------------------+  |
|  +-----------------------+  +----------------+  +------------+  |
|  | Thread Stacks (Stack) |  | Program Counter|  | Native     |  |
|  | (Har bir oqim uchun)  |  | (PC Registr)   |  | Method     |  |
|  +-----------------------+  +----------------+  +------------+  |
+-----------------------------------------------------------------+
                                 |
                                 v
+-----------------------------------------------------------------+
|                      Execution Engine                           |
|  +-------------+  +-------------------------+  +-------------+  |
|  | Interpreter |  | JIT Compiler (C1, C2)   |  |   Garbage   |  |
|  |             |  | (Inlining, Escape Anal) |  |  Collector  |  |
|  +-------------+  +-------------------------+  +-------------+  |
+-----------------------------------------------------------------+
```

---

## 2. ClassLoader Quyi Tizimi (Class Loading Process)

Sinflarni yuklash jarayoni 3 ta asosiy bosqichda amalga oshiriladi: **Loading**, **Linking** va **Initialization**.

### 2.1. Delegatsiya Ierarxiyasi (Delegation Hierarchy)
ClassLoader har doim "Ota birinchi" (Parent-First) tamoyilida ishlaydi. Sinf yuklanishi kerak bo'lganda, quyi classloader darhol o'zi yuklamay, ota classloaderga delegatsiya qiladi:

1. **Bootstrap ClassLoader**: C/C++ da yozilgan bo'lib, eng asosiy JVM sinflarini (`java.lang.*`, `java.util.*` - `java.base` moduli) yuklaydi. Java kodida u `null` ko'rinishida bo'ladi.
2. **Platform (eski nomi Extension) ClassLoader**: Platformaga oid kengaytmalar va modullarni yuklaydi.
3. **Application (System) ClassLoader**: Dasturchining shaxsiy klasslari va `CLASSPATH` dagi barcha uchinchi tomon `.jar` kutubxonalarni yuklaydi.
4. **Custom ClassLoader**: Dasturchi tomonidan `ClassLoader` sinfidan voris olib yozilgan maxsus yuklagichlar (masalan shifrlangan klasslarni o'qish yoki tarmoqdan yuklash uchun).

### 2.2. Uch Bosqichli Jarayon
1. **Loading (Yuklash)**: `.class` faylidan binar baytkod o'qiladi va JVM Metaspace da uning strukturasi shakllantirilib, Heap da `java.lang.Class` obyekti yaratiladi.
2. **Linking (Bog'lash)**:
   - **Verification**: Baytkod xavfsizligi qat'iy tekshiriladi (stack to'lib ketmasligi, tiplar mosligi, xavfsizlik cheklovlari). Bu JVM xavfsizligining eng muhim qalqonidir.
   - **Preparation**: Sinfning statik maydonlari uchun xotira ajratiladi va ularga sukut bo'yicha nol (`0`, `null`, `false`) qiymatlar yoziladi.
   - **Resolution**: Doimiy havzalar (Constant Pool) dagi ramziy ko'rsatkichlar (Symbolic references) to'g'ridan-to'g'ri xotira manzillariga (Direct references) almashtiriladi.
3. **Initialization (Initsializatsiya)**: Sinfning `<clinit>` metodi ishga tushadi: statik bloklar (`static { ... }`) bajariladi va statik o'zgaruvchilarga dasturchi bergan haqiqiy boshlang'ich qiymatlar biriktiriladi.

---

## 3. JVM Xotira Modeli (JVM Memory Areas)

JVM xotirasi mantiqiy jihatdan ikkiga bo'linadi: **Barcha oqimlar uchun umumiy bo'lgan xotira** (Heap, Metaspace, Code Cache) va **Har bir oqim uchun alohida ochiladigan xotira** (Thread Stack, PC Register, Native Method Stack).

### 3.1. Heap Xotira (Heap Memory)
Heap — barcha obyektlar (`new` orqali yaratilgan) va massivlar joylashadigan asosiy xotiradir. U Garbage Collector tomonidan boshqariladi.

Generational farazga (Weak Generational Hypothesis) ko'ra: "Yangi yaratilgan obyektlarning 90% dan ortig'i juda qisqa vaqt ichida o'ladi". Shu sababli Heap ikkiga ajratilgan:

#### A. Young Generation (Yosh avlod)
- **Eden Space**: Barcha yangi obyektlar dastlab shu yerda tug'iladi.
- **Survivor Spaces (S0 / From va S1 / To)**: Eden to'lganda **Minor GC** ishga tushadi. Tirik qolgan obyektlar S0 ga ko'chiriladi. Keyingi Minor GC da tirik qolganlar S0 dan S1 ga ko'chadi (bunda S0 butunlay bo'shatiladi).
- **Age Counter (Yosh hisoblagichi)**: Har safar Survivor dan tirik o'tgan obyektning yoshi 1 ga oshadi. Yosh ma'lum chegaraga (odatda `-XX:MaxTenuringThreshold=15`) yetganda, obyekt qari avlodga o'tkaziladi (**Tenuring / Promotion**).

#### B. Old (Tenured) Generation (Qari avlod)
- Uzoq yashovchi obyektlar (masalan Singleton Bean lar, statik keshlar, DB Connection Pool lar) bu yerda yashaydi.
- Bu hudud to'lganda og'irroq bo'lgan **Major GC / Full GC** ishga tushadi.

#### C. TLAB (Thread Local Allocation Buffer)
Ko'p oqimli muhitda bir nechta oqim Heap ga bir vaqtda obyekt yozishga uringanda sinxronizatsiya qulflari (contention) sekinlashuvga olib kelmasligi uchun, har bir oqimga Eden ichidan kichik xususiy TLAB buferi ajratiladi. Oqim o'z TLAB ichiga obyektni hech qanday qulfsiz, o'ta yuqori tezlikda joylashtiradi.

### 3.2. Thread Stack va Stack Frame tuzilishi
Har bir Java oqimi (Thread) ochilganda, unga operatsion tizimdan alohida Stack xotira ajratiladi (sukut bo'yicha `-Xss1m` = 1MB).
Oqim ichida har safar yangi metod chaqirilganda, Stack da yangi **Stack Frame (freym)** ochiladi. Metod `return` qilganda freym Stack dan yo'qotiladi.

Stack Frame quyidagi qismlardan iborat:
1. **Local Variables Table (Lokal o'zgaruvchilar jadvali)**: Metod parametrlari va lokal o'zgaruvchilar saqlanadi. `this` ko'rsatkichi 0-indeksda turadi. `int`, `float`, reference lar 1 slot, `long` va `double` esa 2 slot egallaydi.
2. **Operand Stack**: Arifmetik hisob-kitoblar bajariluvchi "LIFO" operatsion xotira. Masalan `iload_1`, `iload_2`, `iadd`, `istore_3` instruksiyalari aynan shu operand stack ustida amallarni bajaradi.
3. **Frame Data**: Metod qayerga qaytishi kerakligi (Return address), dinamik havolalar (Constant pool resolution) va istisnolarni boshqaruvchi jadval (Exception table).

### 3.3. Metaspace (Native Xotira)
Java 8 da eskirgan va chegaralangan `PermGen` (Permanent Generation) butunlay olib tashlandi va uning o'rniga operatsion tizimning bevosita RAM xotirasidan joy oluvchi **Metaspace** joriy etildi.
Metaspace da:
- Yuklangan barcha klasslarning tuzilishi (Class Metadata);
- Metodlar baytkodi, parametrlar turlari;
- Annotatsiyalar;
- Metod jadvallari (vtable / itable) saqlanadi.

Sukut bo'yicha Metaspace operatsion tizimning bo'sh xotirasi yetguncha kengaya oladi. Xotira sizib chiqishini (Memory Leak) cheklash uchun `-XX:MaxMetaspaceSize=512m` kabi parametr bilan cheklash tavsiya etiladi.

---

## 4. JIT (Just-In-Time) Kompilyator va Bajarilish Dvigateli

Java kodi dastlab **Interpreter (Interpretator)** tomonidan baytkod qatorma-qator o'qilib bajariladi. Bu ilovaning zudlik bilan ishga tushishini ta'minlaydi, ammo sekin ishlaydi.
Biroq dastur ishlab turgan vaqtda JVM eng ko'p chaqirilayotgan metodlar va issiq nuqtalarni (**Hotspots**) hisoblab boradi. Bular maxsus **JIT Compiler** ga uzatiladi va to'g'ridan-to'g'ri protsessorning mahalliy (native) mashina kodiga kompilyatsiya qilinadi.

### 4.1. Tiered Compilation (Pog'onali Kompilyatsiya)
Zamonaviy HotSpot JVM 5 ta bosqichdan iborat pog'onali kompilyatsiyadan foydalanadi:
- **Tier 0 (Interpreter)**: Sof interpretatsiya rejimi, dastur start oladi.
- **Tier 1 (Simple C1)**: C1 Client kompilyatori. Profil yig'masdan tezkor mashina kodiga o'tkazadi.
- **Tier 2-3 (Limited/Full Profiling C1)**: C1 kompilyatori kod qanday shoxlanayotganini (branch statistics) va metod turlarini profil qilib boradi.
- **Tier 4 (C2 Server Compiler / Graal)**: Eng chuqur, eng murakkab va maksimal optimallashtirilgan mashina kodini ishlab chiqadi. C++ tezligiga aynan shu bosqichda erishiladi.

### 4.2. JIT Optimizatsiyalarining Shoh Asarlari
1. **Method Inlining (Metodlarni ichiga joylash)**: Kichik metod chaqiruvlari (masalan getter/setter yoki `Math.max()`) chaqiruv xarajatlarini (call overhead) yo'qotish uchun to'g'ridan-to'g'ri chaqirgan joyga ko'chirib qo'yiladi.
2. **Escape Analysis va Scalar Replacement**: JIT metod ichida yaratilgan obyekt metod tashqarisiga "qochib ketadimi" (tashqariga uzatiladimi yoki yo'q) deb tekshiradi. Agar obyekt metod ichida qolib ketsa, u Heap da yaratilmaydi! Uning maydonlari to'g'ridan-to'g'ri protsessor registrlariga yoki Stack ga ajratiladi (**Scalar Replacement**). Bu Garbage Collector yuklamasini 70-80% ga kamaytiradi.
3. **Loop Unrolling (Sikllarni ochish)**: Sikl hisoblagichini tekshirish sonini kamaytirish uchun sikl tanasi 4-8 marta takrorlanib yoziladi va SIMD (vektorli protsessor instruksiyalari) ga moslanadi.
4. **Dead Code Elimination**: Natijasi hech qayerda ishlatilmaydigan hisob-kitoblar mashina kodidan butunlay olib tashlanadi.
5. **On-Stack Replacement (OSR)**: Agar biror sikl juda ko'p iteratsiya qilsa, JVM o'sha siklning o'rtasidayoq interpretatsiyadan to'g'ridan-to'g'ri mashina kodiga o'tib ketadi.

---

## 5. Garbage Collection (GC) Mexanizmlari

Garbage Collection — Heap xotirada yetib bo'lmas (unreachable) holga kelgan obyektlarni aniqlab, xotirani ozod qilish jarayonidir.

### 5.1. GC Asosiy Bosqichlari
- **Mark (Belgilash)**: GC Roots (Stack freymlardagi o'zgaruvchilar, statik maydonlar, JNI ko'rsatkichlari) dan boshlab barcha tirik obyektlar grafigi bo'ylab yuriladi va tiriklar belgilanadi.
- **Sweep (Tozalash)**: Belgilanmagan (o'lik) obyektlar egallab turgan xotira bo'shatiladi.
- **Compact (Zichlashtirish)**: Xotirada teshiklar (fragmentatsiya) hosil bo'lmasligi uchun tirik obyektlar xotiraning boshiga bir-biriga yopishtirib ko'chiriladi.

### 5.2. Garbage Collectorlar Qiyosiy Tahlili

| GC Nomi | Algoritm | Pauza Vaqti (STW) | Qo'llanish Sohasi |
| :--- | :--- | :--- | :--- |
| **Serial GC** | Mark-Sweep-Compact | Yuqori (bitta oqimda) | Kichik CLI utilitalar, 512MB dan kam RAM |
| **Parallel GC** | Ko'p oqimli Throughput | O'rtacha (soniyalar) | Katta hisob-kitoblar, Batch qayta ishlash |
| **G1 GC** | Regionlar, SATB, Incremental | Past (10-200 ms) | Standart korporativ ilovalar (4GB - 64GB) |
| **ZGC (Java 21+)** | Colored Pointers, Load Barriers | Ultra-past (< 1 ms!) | Real-time, Bank to'lovlari, 16GB dan Terabaytgacha |
| **Shenandoah GC** | Brooks Pointers, Concurrent Compact | Ultra-past (< 10 ms) | Red Hat/Fedora bulutli serverlari |

### 5.3. G1 GC (Garbage-First)
Java 9 dan boshlab sukut bo'yicha faol:
- Heap xotirasini 2048 tagacha teng o'lchamli (1MB dan 32MB gacha) **Region** larga bo'ladi.
- Regionlar qat'iy emas: ixtiyoriy region istalgan paytda Eden, Survivor yoki Old bo'lishi mumkin.
- **Garbage-First tamoyili**: G1 eng ko'p chiqindi yig'ilib qolgan regionlarni birinchi navbatda tozalaydi.
- Dasturchi `-XX:MaxGCPauseMillis=200` orqali kutiladigan maksimal pauza vaqtini belgilashi mumkin va G1 o'z ishini shu vaqtga sig'dirishga intiladi.

### 5.4. ZGC (Z Garbage Collector) va Generational ZGC (Java 21 LTS)
ZGC — zamonaviy Java tarixidagi eng ulkan yutuqlardan biridir:
- **Kafolat**: Heap hajmi 16GB bo'ladimi yoki 16 Terabayt bo'ladimi, Stop-the-World pauzasi **1 millisekunddan kam** bo'lishi kafolatlanadi!
- **Colored Pointers**: ZGC 64-bitli xotira ko'rsatkichining (reference) yuqori bitlaridan metadata sifatida foydalanadi (Marked0, Marked1, Remapped).
- **Load Barriers**: Dastur o'qiyotgan paytda obyekt agar boshqa joyga ko'chirilgan bo'lsa, yuklash to'sig'i uni parvozda yangi manzilga yangilab yuboradi.
- **Java 21 Generational ZGC**: `-XX:+UseZGC -XX:+ZGenerational` bayrog'i orqali yosh va qari avlodlarni alohida tozalash imkoni qo'shildi, bu CPU sarfini 40% ga kamaytirdi.

---

## 6. Java Xotira Modeli (JMM) va Virtual Threads

### 6.1. Happens-Before Shartnomasi
Ko'p yadroli protsessorlarda keshlar mosligi (Cache Coherence) va buyruqlarni o'rin almashtirish (Instruction Reordering) tufayli bitta oqim yozgan ma'lumot ikkinchi oqimga ko'rinmasligi mumkin.
JMM quyidagi holatlarda **Happens-Before** kafolatini beradi:
1. **Volatile qoidasi**: `volatile` maydonga yozish amali undan keyingi har qanday o'qish amalidan oldin bajariladi (Hardware Memory Barrier qo'yiladi).
2. **Monitor Lock qoidasi**: `synchronized` blokidan chiqish (unlock) keyingi kiruvchi oqimning blokga kirishi (lock) bilan sinxronlashadi.
3. **Thread Start qoidasi**: `thread.start()` chaqiruvi o'sha oqim ichidagi har qanday buyruqdan oldin sodir bo'ladi.
4. **Thread Termination qoidasi**: Oqim ichidagi barcha amallar `thread.join()` tugashidan oldin yakunlanadi.

### 6.2. Virtual Threads (Project Loom) Chuqur Tahlili
An'anaviy 1:1 modeli (Platform Thread = OS Thread) serverlarda C10K (o'n mingta mijoz) muammosiga sabab bo'lgan.
Virtual Threads bu M:N modelidir:
- **1,000,000 ta Virtual Thread** atigi **16 ta OS Carrier Thread** ustida bemalol aylanadi.
- Virtual thread I/O so'rovida qotganda (masalan Socket o'qish, JDBC so'rovi, HTTP call), JVM ning `Continuation` mexanizmi uning chaqiruv stackini Heap xotiraga yozib, OS oqimini zudlik bilan boshqa virtual threadga bo'shatib beradi.
- I/O javobi kelishi bilan OS hodisasi (epoll/kqueue) orqali virtual thread qayta Heap dan yuklanib (mount) ishini davom ettiradi.

> [!WARNING] Virtual Threads bilan ishlashda eng muhim qoidalar:
> 1. Hech qachon Virtual Thread larni havzada (Pool) saqlamang! Ularni doim yangi yaratib ishlating (`Executors.newVirtualThreadPerTaskExecutor()`).
> 2. `ThreadLocal` dan ehtiyotkorlik bilan foydalaning (chunki 1 million virtual thread ko'p xotira yeb qo'yishi mumkin). Buning o'rniga Java 21 `ScopedValue` qo'llang.
> 3. `synchronized` bloklarida uzoq I/O amallarini bajarmang (Thread Pinning bo'lmasligi uchun). O'rniga `ReentrantLock` ishlating.

---

## 7. Enterprise Profiling va JVM Sozlash (Best Practices)

### 7.1. Ishlab Chiqarish (Production) uchun Muhim JVM Bayroqlari
```bash
# Xotirani sozlash (Min va Max bir xil qo'yilishi OS qayta ajratish xarajatlarini yo'qotadi)
-Xms8g -Xmx8g

# Metaspace limitini qo'yish
-XX:MaxMetaspaceSize=512m

# Java 21 da Generational ZGC ni yoqish (Real-time va to'lov tizimlari uchun)
-XX:+UseZGC -XX:+ZGenerational

# Agar G1 GC ishlatilsa, pauza maqsadini qo'yish
-XX:+UseG1GC -XX:MaxGCPauseMillis=150

# OOM (OutOfMemoryError) yuz berganda avtomatik xotira fotosuratini (Heap Dump) olish
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/var/log/app/heap_dump.hprof

# GC loglarini batafsil yozish
-Xlog:gc*,gc+phases=debug:file=/var/log/app/gc.log:time,uptime,pid:filecount=5,filesize=50m
```

### 7.2. Diagnostika Asboblari
1. **jcmd**: JVM ga jonli buyruqlar berish (`jcmd <PID> GC.heap_dump /tmp/dump.hprof`, `jcmd <PID> Thread.print`).
2. **jstack**: Oqimlarning holati (Thread Dump) va Deadlock larni aniqlash.
3. **Java Flight Recorder (JFR)**: JVM ichiga o'rnatilgan, atigi 1% dan kam CPU sarflovchi doimiy monitoring vositasi (`-XX:StartFlightRecording=disk=true,dumponexit=true`).
4. **async-profiler**: FlameGraph (Olovli grafiklar) orqali qaysi metod eng ko'p CPU yoki Heap xotirani sarflayotganini aniqlovchi eng mashhur vosita.

### 7.3. GraalVM Native Image va Spring Boot 3 AOT
Zamonaviy bulutli (Kubernetes) muhitlarda ilovalarning tez start olishi (Cold start) va minimal RAM iste'mol qilishi juda muhimdir.
- **GraalVM Native Image** an'anaviy JVM o'rniga dasturni oldindan (**Ahead-of-Time - AOT**) to'liq tahlil qilib, faqat ishlatiladigan baytkodlarni bitta mustaqil binar mashina fayliga kompilyatsiya qiladi.
- Natijada:
  - Start vaqti: **10-30 millisekund**!
  - RAM iste'moli: **30-50 Megabayt** (JVM dagi 500MB o'rniga).
  - Serverless va AWS Lambda uchun ideal yechim.

---

## Xulosa

Java dasturlash tili bugungi kunda shunchaki dasturlash tili emas, balki 30 yillik tajriba va eng ilg'or muhandislik yutuqlarini o'zida jamlagan qudratli ekotizimdir.
Ushbu ensiklopedik qo'llanmada tahlil qilingan JVM arxitekturasi, xotira tuzilishi, JIT dvigateli va zamonaviy Java 21 xususiyatlarini chuqur anglash — yuqori malakali, millionlab so'rovlarni xatosiz ko'tara oladigan haqiqiy Senior Java muhandisi bo'lishning poydevoridir.
