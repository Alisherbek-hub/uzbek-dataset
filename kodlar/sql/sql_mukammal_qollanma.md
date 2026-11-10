# Relyatsion Ma'lumotlar Bazasi va SQL Mukammal Ensiklopedik Qo'llanmasi

## Mundarija
1. [Kirish va Relyatsion Modelning Falsafasi](#1-kirish-va-relyatsion-modelning-falsafasi)
2. [Relyatsion Algebra va Matematik Asoslar](#2-relyatsion-algebra-va-matematik-asoslar)
3. [RDBMS Arxitekturasi va So'rovning Bajarilish Zanjiri](#3-rdbms-arxitekturasi-va-sorovning-bajarilish-zanjiri)
4. [Xotira Arxitekturasi: Shared Buffers, WAL va I/O Dvigateli](#4-xotira-arxitekturasi-shared-buffers-wal-va-io-dvigateli)
5. [Fizik Xotira Tuzilishi: Sahifa Anatomiyasi va Indekslar](#5-fizik-xotira-tuzilishi-sahifa-anatomiyasi-va-indekslar)
6. [MVCC (Multi-Version Concurrency Control) va Tranzaksiyalar](#6-mvcc-multi-version-concurrency-control-va-tranzaksiyalar)
7. [Ma'lumotlar Bazasini Normallashtirish (1NF dan BCNF gacha)](#7-malumotlar-bazasini-normallashtirish-1nf-dan-bcnf-gacha)
8. [Zamonaviy Korporativ Baza: Partitioning, AI Vektorlar va Yuqori Yuklama](#8-zamonaviy-korporativ-baza-partitioning-ai-vektorlar-va-yuqori-yuklama)

---

## 1. Kirish va Relyatsion Modelning Falsafasi

### 1.1. E.F. Codd va Relyatsion Inqilob (1970)
1970-yilgacha axborot tizimlarida ma'lumotlar iyerarxik (Iyerarchical, masalan IBM IMS) yoki tarmoq (Network, CODASYL) modellarida saqlangan. Bu tizimlarning eng katta kamchiligi shundaki, ma'lumotlar fizik xotirada qanday saqlansa, dasturchi so'rovni ham xuddi shunday pointerlar (ko'rsatkichlar) orqali qo'lda aylanib chiqishga majbur edi (navigational access). Agar diskdagi fayl tuzilishi biroz o'zgarsa, unga yozilgan barcha biznes dasturlar qulardi.

Edgar Frank Codd (IBM tadqiqotchisi) o'zining mashhur *"A Relational Model of Data for Large Shared Data Banks"* nomli fundamental maqolasida inqilobiy g'oyani ilgari surdi: **Fizik saqlanish mantiqiy modeldan to'liq ajratilishi shart (Physical Data Independence)**.

Codd relyatsion modelni matematik to'plamlar nazariyasi (Set Theory) va birinchi tartibli predikatlar hisobi (First-Order Predicate Logic) asosiga qurdi:
- **Relyatsiya (Relation)** — matematik ma'noda kortejlar (satrlar) to'plami bo'lib, relyatsion jadvalga mos keladi.
- **Kortej (Tuple)** — relyatsiyaning bitta elementi bo'lib, jadvaldagi bitta qatordir.
- **Atribut (Attribute)** — kortejning nomlangan xususiyati bo'lib, jadval ustunidir.
- **Domen (Domain)** — atribut qabul qilishi mumkin bo'lgan cheklangan qiymatlar to'plami (ma'lumotlar turi).

### 1.2. ANSI/ISO SQL Standartlari Evolyutsiyasi
SQL (Structured Query Language) tili deklarativ tildir: siz tizimga **nimani** olish kerakligini aytasiz, lekin uni **qanday** qilib qidirib topishni (algoritmni) RDBMS ning o'zi hal qiladi.
- **SQL-86 / SQL-89**: Ilk rasmiy ANSI/ISO standartlari (boshlang'ich DDL va DML).
- **SQL-92 (SQL2)**: Hozirgi kunda ham relyatsion bazalarning asosi bo'lgan standart: aniq `JOIN` sintaksisi (`INNER JOIN`, `LEFT JOIN`), `CASE` ifodalari, tranzaksiya izolyatsiyasi darajalari.
- **SQL:1999 (SQL3)**: `RECURSIVE CTE` (Common Table Expressions), triggerlar va foydalanuvchi maxsus tiplari kiritildi.
- **SQL:2003**: Oynador funksiyalar (`WINDOW FUNCTIONS: OVER, ROW_NUMBER, RANK`), XML integratsiyasi.
- **SQL:2011**: Temporal jadvallar (vaqt kesimidagi ma'lumotlar auditi).
- **SQL:2016 / SQL:2019**: `JSON` va `JSONB` bilan ishlashning xalqaro standartlari, Polimorfik jadvallar.
- **SQL:2023**: Graf ma'lumotlar bazasi so'rovlari (Property Graph Queries - SQL/PGQ).

---

## 2. Relyatsion Algebra va Matematik Asoslar

Har qanday SQL so'rovi bajarilishidan oldin ma'lumotlar bazasi motori tomonidan **Relyatsion Algebra** ifodasiga o'giriladi. Relyatsion algebra — bu relyatsiyalar ustida bajariladigan va natijada har doim yangi relyatsiya qaytaruvchi yopiq algebraik tizimdir.

### 2.1. Fundamental Operatorlar
1. **Tanlash (Selection — $\sigma$):**
   - Kortejlarni (qatorlarni) mantiqiy predikat asosida filtrlaydi.
   - Matematik: $\sigma_{\text{shart}}(R) = \{ t \in R \mid \text{shart}(t) \}$
   - SQL ekvivalenti: `SELECT * FROM R WHERE shart;`

2. **Proyeksiya (Projection — $\pi$):**
   - Berilgan atributlar (ustunlar) ro'yxatini ajratib oladi va dublikatlarni olib tashlaydi.
   - Matematik: $\pi_{A_1, A_2, ..., A_k}(R)$
   - SQL ekvivalenti: `SELECT DISTINCT A1, A2 FROM R;`

3. **Dekart Ko'paytmasi (Cartesian Product — $\times$):**
   - Ikkita relyatsiyaning barcha mumkin bo'lgan juftliklarini hosil qiladi.
   - Matematik: $R \times S = \{ (r, s) \mid r \in R \land s \in S \}$
   - SQL ekvivalenti: `SELECT * FROM R CROSS JOIN S;`

4. **Birlashma (Union — $\cup$):**
   - Ikki mos relyatsiyaning barcha unikal qatorlarini yig'adi.
   - SQL: `UNION`

5. **Ayirma (Set Difference — $-$):**
   - Birinchi relyatsiyada bor, lekin ikkinchisida yo'q qatorlarni qoldiradi.
   - SQL: `EXCEPT` (yoki Oracle da `MINUS`).

6. **Nomini o'zgartirish (Rename — $\rho$):**
   - Relyatsiya yoki uning atributlari nomini vaqtinchalik o'zgartiradi.
   - SQL: `AS yangi_nom`

### 2.2. Hosilaviy Murakkab Operatorlar
- **Natural Join ($R \bowtie S$):** Dekart ko'paytmasidan so'ng umumiy nomli ustunlar tengligi bo'yicha tanlash va ortiqcha ustunni proyeksiyalash.
- **Theta Join ($R \bowtie_\theta S$):** Ixtiyoriy shart $\theta$ asosida birlashtirish: $\sigma_\theta(R \times S)$.
- **Bo'lish (Division — $R \div S$):** 'Barcha' degan savolga javob beruvchi amal (Masalan: 'Barcha talab qilingan kurslarni tugatgan talabalarni topish').

---

## 3. RDBMS Arxitekturasi va So'rovning Bajarilish Zanjiri

### 3.1. PostgreSQL Process Modeli
PostgreSQL har bir mijoz ulanishi uchun alohida jarayon (Process-per-Connection modeli) ochadi:
- **Postmaster (Daemon):** 5432-portni eshituvchi bosh jarayon. Yangi TCP ulanish kelganda `fork()` orqali yangi `postgres` (backend server process) jarayonini ishga tushiradi.
- **Background Processes:**
  - `Checkpointer`: Xotiradagi iflos sahifalarni (dirty buffers) belgilangan vaqtda diskka yozuvchi jarayon.
  - `Background Writer (bgwriter)`: Shared buffers da doimo toza sahifalar bo'lishini ta'minlovchi fon yozuvchisi.
  - `WAL Writer`: WAL buferidagi ma'lumotlarni doimiy ravishda diskka uzatuvchi jarayon.
  - `Autovacuum Launcher / Workers`: O'lik qatorlarni avtomatik tozalovchi va statistika yig'uvchi fon workerlari.
  - `Archiver`: WAL segmentlarini uzoq muddatli zaxira omboriga (S3/NFS) nusxalovchi jarayon.

### 3.2. So'rovning Hayot Yo'li (Query Lifecycle)
1. **Parser (Sintaktik tahlil):**
   - SQL matnini leksik va grammatik qoidalarga (Bison/Flex) tekshiradi.
   - Natijada **Parse Tree** (so'rov sintaktik daraxti) hosil bo'ladi.
2. **Analyzer / Rewriter (Mantiqiy tahlil va Ko'rinishlar):**
   - Tizim kataloglariga (`pg_class`, `pg_attribute`) qarab jadval va ustunlar mavjudligini, ma'lumot turlari mosligini tekshiradi.
   - Agar so'rov `VIEW` ga yo'naltirilgan bo'lsa, view qoidasini (Query Rewrite Rules) ochib, Parse Tree ni qayta quradi.
   - Natijada **Query Tree** shakllanadi.
3. **Query Optimizer / Planner (Rejalashtiruvchi):**
   - Eng muhim bosqich! Bir xil natijaga erishishning yuzlab mumkin bo'lgan bajarilish rejalarini (Execution Paths) ko'rib chiqadi.
   - Har bir operatsiyaning (Seq Scan, Index Scan, Nested Loop, Hash Join) narxini (Cost) hisoblaydi.
   - Eng minimal umumiy narxga (total cost) ega bo'lgan **Execution Plan** (Bajarilish rejasi) ni tanlaydi.
4. **Executor (Ijrochi):**
   - Tanlangan rejani (Plan Tree) eng yuqori tugundan pastga qarab talab asosida (Volcano Iterator modeli: `InitPlan`, `ExecutePlan`, `FetchTuple`) bajaradi va qatorlarni mijozga uzatadi.

---

## 4. Xotira Arxitekturasi: Shared Buffers, WAL va I/O Dvigateli

### 4.1. Shared Buffers va Kesh Boshqaruvi
Ma'lumotlar bazasi diskdan to'g'ridan-to'g'ri o'qimaydi va yozmaydi! Diskka murojaat operativ xotiraga (RAM) nisbatan 100 000 barobar sekindir.
- **Shared Buffers** — bu PostgreSQL ga ajratilgan umumiy operativ xotira hududidir (standart holda RAM ning 25% qismi tavsiya etiladi).
- Diskdagi jadvallar 8 Kilobaytlik (`8 KB`) sahifalarga (pages) bo'lingan. Xotiradagi sahifalar esa **Buffer Pool** da saqlanadi.
- **Clock Sweep (Clock-Pro) Algoritmi:** Bufer to'lib qolganda qaysi sahifani chiqarib yuborishni (eviction) hal qiluvchi tejamkor soat ko'rsatkichi mexanizmi. Har bir sahifaga kirilganda uning hisoblagichi oshiriladi; soat mili aylanib hisoblagichi 0 bo'lgan foydalanilmayotgan sahifalarni diskka yozib o'rnini bo'shatadi.

### 4.2. WAL (Write-Ahead Logging) va ARIES Protokoli
Tranzaksiyaning **Durability** (chidamlilik) xususiyati WAL orqali kafolatlanadi.
- **Asosiy Qoida:** Ma'lumotlar sahifasi diskka yozilishidan oldin, uning o'zgarish jurnali (WAL record) albatta diskdagi WAL fayliga doimiy saqlangan (`fsync`) bo'lishi shart!
- WAL fayllari standart 16 Megabaytlik segmentlar ko'rinishida `pg_wal` katalogida ketma-ket yoziladi.
- Agar server to'satdan tokdan uzilsa, qayta yoqilganda **Crash Recovery** ishga tushadi:
  1. **Analysis:** Oxirgi Checkpoint nuqtasidan boshlab qaysi tranzaksiyalar qolib ketganini aniqlaydi.
  2. **Redo:** Barcha tasdiqlangan (COMMIT) amallarni xotiradagi sahifalarga qayta qo'llaydi.
  3. **Undo:** Tasdiqlanmagan yarimta tranzaksiyalarni orqaga qaytaradi.

---

## 5. Fizik Xotira Tuzilishi: Sahifa Anatomiyasi va Indekslar

### 5.1. 8KB Relyatsion Sahifa (Page) Anatomiyasi
PostgreSQL da jadval yoki indeks sahifasining ichki tuzilishi quyidagicha:

```text
+----------------------------------------------------------------+
| PageHeaderData (24 bayt: LSN, checksum, pd_lower, pd_upper)   |
+----------------------------------------------------------------+
| ItemIdData (Line Pointers / Qator ko'rsatkichlari: 4 bayt)     |
| [ Item 1 ] [ Item 2 ] [ Item 3 ] ...                          |
|                                     v (pastga qarab o'sadi)   |
| ----------------- Bo'sh Joy (Free Space) ---------------------|
|                                     ^ (yuqoriga qarab o'sadi) |
| [ Tuple 3 ] [ Tuple 2 ] [ Tuple 1 ]                            |
+----------------------------------------------------------------+
| Special Space (Indeksga xos ma'lumotlar, jadvallarda 0 bayt)  |
+----------------------------------------------------------------+
```
- **ItemIdData (Line Pointers):** Sahifa boshidan pastga qarab o'sadi. Har bir qator uchun 4 baytlik manzil ko'rsatkichi.
- **Tuple Data (Qatorlar):** Sahifaning eng tagidan yuqoriga qarab o'sadi.
- Bu struktura qator hajmi o'zgarganda sahifa ichida fragmentatsiyani yo'qotish va qatorni siljitishda uning tashqi manzilini (`ctid = (block_number, item_offset)`) o'zgartirmaslik imkonini beradi.

### 5.2. Indekslar Anatomiyasi
1. **B-Tree Indeks (Lehman & Yao Algoritmi):**
   - O'z-o'zini balanslovchi daraxt.
   - **Root Page:** Qidiruv boshlanadigan ildiz sahifasi.
   - **Internal Pages:** Yo'naltiruvchi oraliq tugunlar.
   - **Leaf Pages:** Eng quyi sahifalar. Ular to'g'ridan-to'g'ri jadval qatorining pointerini (`ItemPointer / ctid`) saqlaydi va bir-biriga ikki tomonlama bog'langan ro'yxat (Doubly Linked List) orqali ulangan. Bu orqali diapazonli (`BETWEEN`, `>`, `<`) qidiruvlar o'ta tez bajariladi.
   - `Lehman-Yao` modifikatsiyasi har bir sahifaga o'ng qo'shnisiga havolani (`High Key` va `Right-link`) kiritadi, bu esa parallel o'qish paytida sahifa bo'linayotganda butun daraxtni qulflamaslik (lock-free read) imkonini beradi.

2. **GIN (Generalized Inverted Index):**
   - Hujjatlar, massivlar va JSONB uchun teskari indeks.
   - Kalitlar B-Tree da saqlanadi, har bir kalitga mos qatorlar ro'yxati esa `Posting List` (kichik bo'lsa) yoki `Posting Tree` (katta bo'lsa) ko'rinishida saqlanadi.

3. **BRIN (Block Range Index):**
   - Ketma-ket o'suvchi (masalan sana yoki avto-inkrement ID) milliardlab qatorli jadvallar uchun.
   - Har 128 ta sahifa uchun faqat minimal va maksimal qiymatni (`Min/Max`) saqlaydi. 100 GB lik jadval uchun BRIN indeksi atigi bir necha Megabayt joy oladi!

---

## 6. MVCC (Multi-Version Concurrency Control) va Tranzaksiyalar

### 6.1. Tuple Header va Versiyalar Boshqaruvi
PostgreSQL da qator yangilanganda (UPDATE), eski qator ustiga yangi qiymat yozilmaydi! Buning o'rniga yangi qator versiyasi (yangi tuple) yaratiladi va eskisi o'lik qilib belgilanadi.
Har bir qator sarlavhasida (HeapTupleHeader) quyidagi muhim maydonlar bo'ladi:
- `xmin`: Ushbu qator versiyasini yaratgan (INSERT/UPDATE qilgan) tranzaksiyaning identifikatori (XID).
- `xmax`: Ushbu qatorni o'chirgan yoki yangilagan tranzaksiya XID si (faol tirik qatorlarda 0 bo'ladi).
- `t_ctid`: Ushbu qatorning fizik joylashuvi yoki yangilangan yangi versiyasiga ko'rsatkich.
- `t_infomask`: Tranzaksiyaning tasdiqlanganligi (COMMITTED) haqidagi bayroqchalar.

### 6.2. Snapshot (Holat Tasviri) Ko'rinuvchanlik Qoidalari
Tranzaksiya so'rov yuborgan paytda xotirada `Snapshot` ochiladi: `xmin:xmax:xip_list`.
- Qator agar uning `xmin` tranzaksiyasi tasdiqlangan (committed) bo'lsa va joriy snapshot yaratilishidan oldin yakunlangan bo'lsa ko'rinadi.
- Agar qatorning `xmax` mavjud bo'lsa va u tasdiqlangan bo'lsa, qator o'chirilgan hisoblanib ko'rinmaydi.
- Natijada: **O'quvchilar yozuvchilarga hech qachon to'sqinlik qilmaydi, yozuvchilar esa o'quvchilarni hech qachon kutib turmaydi!**

### 6.3. VACUUM va Autovacuumning Rol
- `UPDATE` va `DELETE` amallari oqibatida sahifalarda o'lik qatorlar (dead tuples) to'planib boradi. Bu hodisa **Table Bloat** deyiladi.
- `VACUUM` o'lik qatorlar egallagan baytlarni tozalaydi va ushbu joylarni yangi kiritiladigan qatorlar uchun bo'sh (`Free Space Map - FSM`) deb belgilaydi.
- `Visibility Map (VM)`: Sahifadagi barcha qatorlar barcha tranzaksiyalarga ko'rinishi aniq bo'lsa (all-visible), `Index-Only Scan` paytida asosiy jadval disk blokiga kirmasdan to'g'ridan-to'g'ri indeksdan javob berish imkonini yaratadi.

---

## 7. Ma'lumotlar Bazasini Normallashtirish (1NF dan BCNF gacha)

Normallashtirish — ma'lumotlar ortiqchaligini (data redundancy) minimallashtirish va modifikatsiya anomaliyalarini (kiritish, yangilash va o'chirishdagi ziddiyatlar) yo'qotish uchun jadvallarni mantiqiy bo'lish jarayonidir.

### 7.1. Birinchi Normal Shakl (1NF - Atomarlik)
- Jadvalning har bir ustunidagi qiymat **bo'linmas (atomar)** bo'lishi shart.
- Takrorlanuvchi guruhlar yoki massivlar bo'lmasligi lozim.
- Har bir qator yagona unikal kalit (Birlamchi kalit) orqali aniqlanishi kerak.

*Antipattern (1NF buzilishi):* `telefonlar: "+998901234567, +998912345678"`  
*To'g'rilash:* Alohida bog'liq jadval ochiladi: `telefon_raqamlari(mijoz_id, telefon)`.

### 7.2. Ikkinchi Normal Shakl (2NF - To'liq Funksional Bog'liqlik)
- Jadval 1NF talablariga to'liq javob berishi shart.
- Birlamchi kaliti kompozit (bir nechta ustundan iborat) bo'lgan jadvallarda, hech bir no-kalit ustun birlamchi kalitning **qismiga** bog'liq bo'lmasligi lozim (faqat butun kalitga to'liq bog'liq bo'lishi shart).

### 7.3. Uchinchi Normal Shakl (3NF - Tranzitiv Bog'liqliklarni Yo'qotish)
- Jadval 2NF talablariga javob berishi shart.
- Hech bir no-kalit ustun boshqa no-kalit ustunga bog'liq bo'lmasligi kerak ($X \rightarrow Y$, $Y \rightarrow Z$ zanjiri taqiqlanadi).

*Misol:* `xodimlar(id, ism, bolim_id, bolim_nomi)`  
Bu yerda `bolim_nomi` bevosita `id` ga emas, balki `bolim_id` orqali tranzitiv bog'liq. Bo'lim nomi `bolimlar` jadvaliga chiqarilishi shart.

### 7.4. Boys-Kodd Normal Shakli (BCNF)
- 3NF ning kuchaytirilgan varianti.
- Har qanday funksional bog'liqlikda ($X \rightarrow Y$), determinant $X$ albatta **Superkey** (nomzod kalit) bo'lishi shart.

---

## 8. Zamonaviy Korporativ Baza: Partitioning, AI Vektorlar va Yuqori Yuklama

### 8.1. Declarative Partitioning (Jadvallarni Bo'lish)
Milliardlab qatorga ega jadvallarda B-Tree indeksi ham RAM ga sig'may qoladi. Yechim — jadvalni mantiqiy master va fizik qismlarga bo'lish:
- `RANGE`: Vaqt bo'yicha (har oylik yoki har yillik arxivlar).
- `LIST`: Hududlar, davlatlar yoki diskret holatlar bo'yicha.
- `HASH`: Klaster bo'ylab yuklamani teng tarqatish uchun.
- **Partition Pruning:** Rejalashtiruvchi so'rovdagi `WHERE` shartiga qarab, faqat tegishli qismni o'qiydi va qolgan 99% jadvallarni chetlab o'tadi.

### 8.2. Sun'iy Intellekt va pgvector Ekotizimi
Zamonaviy korporativ tizimlarda matnli, audio yoki vizual ma'lumotlar neyron tarmoqlari yordamida N-o'lchamli vektorlarga (Embeddings) aylantiriladi.
- PostgreSQL `pgvector` kengaytmasi orqali alohida ixtisoslashtirilgan NoSQL vektor bazalarisiz, to'g'ridan-to'g'ri relyatsion jadvallar ichida vektorlarni saqlaydi.
- **Masofa Metrikalari:**
  - Kosinus masofasi (`<=>`): Semantik matn o'xshashligi uchun.
  - L2 Evklid masofasi (`<->`): Fazoviy masofalar uchun.
  - Ichki ko'paytma (`<#>`): Normallashgan embeddinglar uchun eng tezyurar hisob.
- **HNSW Graflari:** Ierarxik qatlamli o'tkazgich graflar orqali millionlab vektorlar ichidan eng yaqin qo'shnilarni 2-5 millisoniyada topadi.

### 8.3. Ishlab Chiqarish Barqarorligi (Production Best Practices)
1. **Connection Pooling:** PostgreSQL da har bir ulanish 10 MB gacha xotira olishi mumkin. 1,000 ta parallel so'rov serverni qulatmasligi uchun oldiga doimo **PgBouncer** (Transaction pooling rejimida) qo'yilishi shart.
2. **Kesh Nisbati (Cache Hit Ratio):** `pg_stat_database` dagi keshdan o'qish ko'rsatkichi 99% dan pastga tushmasligi nazorat qilinadi.
3. **Replikatsiya va Failover:** Bitta master serverga tayanib qolmasdan, Patroni + etcd yordamida avtomatik streaming replikatsiya va soniyali Failover klasteri quriladi.

---
*Ushbu qo'llanma relyatsion ma'lumotlar bazalarining ichki mexanizmlari, relyatsion algebra nazariyasi va yuqori yuklamali zamonaviy arxitektura tamoyillarini to'liq qamrab oluvchi professional ensiklopediya hisoblanadi.*
