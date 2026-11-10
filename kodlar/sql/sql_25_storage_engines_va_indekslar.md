# Khorazmiy AI: SQL - Modul 25
## Mavzu: Ma'lumotlar bazasi ichki tuzilishi: LSM-Trees, B+Trees, WAL va Indekslash

### Topshiriq #1201: B+Tree indekslarida sahifa (page) to'lish darajasini tahlil qilish
**Tavsif:** Ma'lumotlar bazasi unumdorligini saqlash uchun B+Tree indekslaridagi sahifalarning to'lish darajasini nazorat qilish kerak. Haddan tashqari bo'sh sahifalar xotira isrofiga, juda to'lganlari esa "page split" jarayonlariga olib keladi.
**Talablar:** `sys.dm_db_index_physical_stats` (yoki ekvivalent) yordamida sahifa to'lish darajasi 70% dan past bo'lgan indekslarni aniqlash.
**Yechim (SQL):**
```sql
-- Indeks sahifalarining to'lish darajasini tekshirish
SELECT 
    object_name(object_id) AS TableName,
    index_id,
    avg_page_space_used_in_percent AS FillFactor_Actual
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'DETAILED')
WHERE avg_page_space_used_in_percent < 70.0 -- 70% dan kam to'lgan sahifalar
  AND page_count > 100; -- Faqat katta indekslar uchun
```
**Tushuntirish:** B+Tree tuzilishida sahifalar orasidagi bo'shliqni (fragmentation) kuzatish, indeksni qayta qurish (rebuild) zaruratini aniqlash uchun muhimdir.

### Topshiriq #1202: WAL (Write-Ahead Logging) kechikishini monitoring qilish
**Tavsif:** Tranzaksiyalar xavfsizligini ta'minlashda WAL muhim. Diskdagi yozish tezligi (I/O) WAL loglari tufayli sekinlashsa, butun tizim ishdan chiqadi.
**Talablar:** WAL yozish operatsiyalari uchun o'rtacha kutish vaqtini (latency) aniqlash.
**Yechim (SQL):**
```sql
-- WAL log yozish jarayonidagi kutish vaqtini tahlil qilish
SELECT 
    wait_type, 
    wait_time_ms / 1000.0 AS WaitTimeSeconds,
    waiting_tasks_count
FROM sys.dm_os_wait_stats
WHERE wait_type LIKE 'WRITELOG%'; -- WAL yozish bilan bog'liq kutishlar
```
**Tushuntirish:** `WRITELOG` kutish turi yuqori bo'lsa, bu disk I/O quvvati yetishmasligini anglatadi. Bu ma'lumotlar bazasi yozish unumdorligini optimallashtirish uchun asosiy ko'rsatkichdir.

### Topshiriq #1203: LSM-Tree uchun "Compaction" strategiyasini simulyatsiya qilish
**Tavsif:** LSM-Tree tuzilishida ma'lumotlar avval memtable'ga, so'ngra SSTable'ga yoziladi. Eski va yangi ma'lumotlarni birlashtirish (compaction) jarayonini SQL orqali modellashtirish.
**Talablar:** Dublikat kalitlarni olib tashlab, eng so'nggi versiyadagi yozuvni saqlab qolish.
**Yechim (SQL):**
```sql
-- SSTable'larni birlashtirish va eng so'nggi holatni saqlash
WITH LatestRecords AS (
    SELECT *, ROW_NUMBER() OVER(PARTITION BY key_id ORDER BY timestamp DESC) as rn
    FROM sstable_data
)
DELETE FROM sstable_data 
WHERE key_id IN (SELECT key_id FROM LatestRecords WHERE rn > 1);
```
**Tushuntirish:** LSM-Tree'da "compaction" jarayoni o'chirilgan yoki yangilangan ma'lumotlarni tozalash uchun zarur. `ROW_NUMBER()` funksiyasi eng so'nggi yozuvni aniqlashda samarali.

### Topshiriq #1204: Indeks qamrovini (Index Covering) tekshirish
**Tavsif:** So'rovlar tezligini oshirish uchun "Covering Index" yaratish. Bunda so'rovdagi barcha ustunlar indeks ichida bo'lishi kerak.
**Talablar:** `SELECT` so'rovida ishlatilgan ustunlar indeks tarkibiga to'liq kirishini tekshirish.
**Yechim (SQL):**
```sql
-- Indeks qamrovini tekshirish uchun so'rov
SELECT name AS IndexName, is_included_column
FROM sys.index_columns ic
JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
WHERE ic.object_id = OBJECT_ID('Orders')
  AND c.name IN ('CustomerID', 'OrderDate'); -- So'rovdagi ustunlar
```
**Tushuntirish:** Indeks qamrovi ma'lumotlar bazasiga "Key Lookup" operatsiyasini bajartirmaydi, bu esa diskdan o'qishni keskin kamaytiradi.

### Topshiriq #1205: B+Tree "Page Split" hodisalarini aniqlash
**Tavsif:** Indeks sahifasi to'lganda, yangi ma'lumot qo'shish uchun sahifa ikkiga bo'linadi (split). Bu jarayon qimmatga tushadi.
**Talablar:** `Page Splits/sec` ko'rsatkichini kuzatish orqali noto'g'ri tanlangan `Fill Factor`ni aniqlash.
**Yechim (SQL):**
```sql
-- Indeks sahifalarining bo'linish tezligini kuzatish
SELECT 
    object_name, 
    counter_name, 
    cntr_value 
FROM sys.dm_os_performance_counters
WHERE counter_name = 'Page Splits/sec';
```
**Tushuntirish:** Agar `Page Splits/sec` yuqori bo'lsa, indeksning `Fill Factor` qiymatini kamaytirish orqali sahifada bo'sh joy qoldirish kerak.

### Topshiriq #1206: WAL checkpoint jarayonini optimallashtirish
**Tavsif:** Checkpoint - bu xotiradagi o'zgarishlarni diskdagi ma'lumotlar fayliga yozish jarayoni. Uning tez-tez sodir bo'lishi tizimni sekinlashtiradi.
**Talablar:** Oxirgi checkpoint vaqtini va uning davomiyligini tahlil qilish.
**Yechim (SQL):**
```sql
-- Checkpoint jarayonining oxirgi bajarilish vaqtini aniqlash
SELECT 
    last_checkpoint_duration_seconds, 
    last_checkpoint_start_time
FROM sys.dm_os_checkpoint_stats;
```
**Tushuntirish:** Checkpoint davomiyligi tizimning yozish yuklamasiga bog'liq. Bu ma'lumotlar bazasi "recovery time objective" (RTO) ni belgilashda muhim.

### Topshiriq #1207: Indeks fragmentatsiyasini tozalash (Defragmentation)
**Tavsif:** B+Tree indekslari vaqt o'tishi bilan fragmentatsiyaga uchraydi. Bu qidiruv tezligini pasaytiradi.
**Talablar:** Fragmentatsiya darajasi 30% dan yuqori bo'lgan indekslarni avtomatik aniqlash va qayta qurish.
**Yechim (SQL):**
```sql
-- 30% dan yuqori fragmentatsiyani aniqlash va qayta qurish
ALTER INDEX ALL ON SalesTable 
REORGANIZE; -- Yoki REBUILD, fragmentatsiya darajasiga qarab
```
**Tushuntirish:** `REORGANIZE` resursni kam sarflaydi, `REBUILD` esa indeksni noldan qurib, sahifalarni to'liq tartiblaydi.

### Topshiriq #1208: LSM-Tree "Bloom Filter" samaradorligini tahlil qilish
**Tavsif:** LSM-Tree'da ma'lumot qaysi SSTable'da ekanligini tez aniqlash uchun Bloom Filter ishlatiladi.
**Talablar:** Bloom Filter noto'g'ri musbat (false positive) natijalarni qanchalik kamaytirayotganini tekshirish.
**Yechim (SQL):**
```sql
-- Bloom Filter samaradorligini tekshirish (Simulyatsiya)
SELECT 
    filter_name, 
    false_positive_count, 
    total_lookups,
    (CAST(false_positive_count AS FLOAT) / total_lookups) * 100 AS ErrorRate
FROM sys.dm_db_bloom_filter_stats;
```
**Tushuntirish:** Bloom Filter xatolik darajasi yuqori bo'lsa, keraksiz SSTable'lar o'qiladi, bu esa unumdorlikni pasaytiradi.

### Topshiriq #1209: Indeks statistikasi yangilanishi
**Tavsif:** Query Optimizer indeks statistikasiga qarab reja tuzadi. Statistika eskirsa, noto'g'ri reja (suboptimal plan) tanlanadi.
**Talablar:** Statistika oxirgi marta qachon yangilangani va qancha qator o'zgarganini aniqlash.
**Yechim (SQL):**
```sql
-- Statistika yangilanishi kerak bo'lgan indekslarni aniqlash
SELECT 
    name AS StatsName, 
    STATS_DATE(object_id, stats_id) AS LastUpdated
FROM sys.stats
WHERE STATS_DATE(object_id, stats_id) < DATEADD(day, -7, GETDATE());
```
**Tushuntirish:** 7 kundan ortiq yangilanmagan statistika tizim uchun xavfli, chunki ma'lumotlar taqsimoti o'zgargan bo'lishi mumkin.

### Topshiriq #1210: Indeks ishlatilishini tahlil qilish (Unused Indexes)
**Tavsif:** Ishlatilmaydigan indekslar yozish operatsiyalarini sekinlashtiradi va disk joyini egallaydi.
**Talablar:** Oxirgi 30 kun ichida hech qanday "seek" yoki "scan" operatsiyasida qatnashmagan indekslarni topish.
**Yechim (SQL):**
```sql
-- Ishlatilmayotgan indekslarni aniqlash
SELECT 
    o.name AS TableName, 
    i.name AS IndexName
FROM sys.indexes i
JOIN sys.objects o ON i.object_id = o.object_id
LEFT JOIN sys.dm_db_index_usage_stats s ON i.index_id = s.index_id AND i.object_id = s.object_id
WHERE s.user_seeks = 0 AND s.user_scans = 0 AND s.user_lookups = 0
  AND i.is_primary_key = 0; -- PK ni o'chirmaslik uchun
```
**Tushuntirish:** Keraksiz indekslarni o'chirish yozish (INSERT/UPDATE/DELETE) tezligini oshiradi, chunki har bir yozishda indekslar ham yangilanishi shart.

---

### Topshiriq #1211: B+Tree indeksining to'liqligini tekshirish
**Tavsif:** Ma'lumotlar bazasida B+Tree indekslari vaqt o'tishi bilan fragmentatsiyaga uchrashi mumkin. Indeks samaradorligini baholash uchun barg tugunlaridagi (leaf nodes) bo'sh joy foizini aniqlash zarur.
**Talablar:** `sys.dm_db_index_physical_stats` funksiyasidan foydalanib, 30% dan ortiq bo'sh joyga ega indekslarni aniqlash.
**Yechim (SQL):**
```sql
SELECT 
    OBJECT_NAME(object_id) AS Jadval_Nomi,
    avg_page_space_used_in_percent AS Band_Joy_Foizi,
    page_count AS Sahifa_Soni
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'DETAILED')
WHERE avg_page_space_used_in_percent < 70 -- 30% dan ortiq bo'sh joy
  AND page_count > 100; -- Kichik indekslarni hisobga olmaslik
```
**Tushuntirish:** B+Tree tuzilishida sahifalarning to'lish darajasi past bo'lsa, qidiruv tezligi pasayadi. Ushbu so'rov indekslarni qayta qurish (rebuild) zarurligini aniqlash uchun ishlatiladi.

### Topshiriq #1212: WAL (Write-Ahead Logging) holatini monitoring qilish
**Tavsif:** Tranzaksiyalar xavfsizligini ta'minlashda WAL muhim. Log fayl hajmining haddan tashqari o'sishi tizim unumdorligiga ta'sir qiladi.
**Talablar:** Log faylning diskdagi hajmi va uning ishlatilish foizini aniqlash.
**Yechim (SQL):**
```sql
SELECT 
    name AS Log_Fayl_Nomi,
    size/128.0 AS Umumiy_Hajm_MB,
    FILEPROPERTY(name, 'SpaceUsed')/128.0 AS Ishlatilgan_Hajm_MB
FROM sys.master_files
WHERE type_desc = 'LOG';
```
**Tushuntirish:** WAL mexanizmi ma'lumotlar bazasi buzilishining oldini oladi. Ushbu so'rov log fayllarining to'lib ketish xavfini oldindan aniqlashga yordam beradi.

### Topshiriq #1213: LSM-Tree asosidagi yozish buferini optimallashtirish
**Tavsif:** LSM-Tree tuzilishida yozish operatsiyalari avval memtable'ga tushadi. Memtable to'lish tezligini tahlil qilish kerak.
**Talablar:** So'nggi 1 soat ichidagi yozish operatsiyalari sonini tahlil qilish.
**Yechim (SQL):**
```sql
SELECT 
    COUNT(*) AS Yozish_Operatsiyalari_Soni,
    DATEPART(HOUR, log_time) AS Soat
FROM transaction_logs
WHERE log_time > DATEADD(HOUR, -1, GETDATE())
GROUP BY DATEPART(HOUR, log_time);
```
**Tushuntirish:** LSM-Tree yozishga yo'naltirilgan (write-optimized) bo'lib, yuqori yuklamalarda memtable'dan diskka ko'chirish (flush) jarayonini kuzatish muhim.

### Topshiriq #1214: Indeks fragmentatsiyasini bartaraf etish
**Tavsif:** B+Tree tuzilmasidagi "page splits" operatsiyalari indeks unumdorligini pasaytiradi.
**Talablar:** Fragmentatsiya darajasi 30% dan yuqori bo'lgan indekslarni avtomatik qayta tashkil etish (reorganize).
**Yechim (SQL):**
```sql
ALTER INDEX ALL ON Mijozlar_Jadvali 
REORGANIZE; -- Indeksni tartibga keltirish va bo'sh joyni optimallashtirish
```
**Tushuntirish:** Reorganize operatsiyasi B+Tree barglarini qayta tartiblaydi, bu esa qidiruv vaqtini kamaytiradi va diskdagi joyni bo'shatadi.

### Topshiriq #1215: Indekslash strategiyasi - Qoplanuvchi indeks (Covering Index)
**Tavsif:** Ko'p so'raladigan so'rovlar uchun jadvalning barcha qismlariga murojaat qilmaslik uchun qoplanuvchi indeks yaratish.
**Talablar:** `Mijoz_ID` va `Buyurtma_Sana` bo'yicha qidiruvni tezlashtirish.
**Yechim (SQL):**
```sql
CREATE NONCLUSTERED INDEX IX_Buyurtmalar_Mijoz_Sana
ON Buyurtmalar (Mijoz_ID, Buyurtma_Sana)
INCLUDE (Umumiy_Summa); -- Qoplanuvchi indeks qismi
```
**Tushuntirish:** `INCLUDE` qismi ma'lumotlarni barg tugunlarida saqlaydi, bu esa "Key Lookup" operatsiyasini bartaraf etib, so'rov tezligini oshiradi.

### Topshiriq #1216: WAL checkpoint jarayonini kuzatish
**Tavsif:** Checkpoint jarayoni memtable'dagi ma'lumotlarni doimiy xotiraga yozadi. Bu jarayonning davomiyligini nazorat qilish.
**Talablar:** Oxirgi checkpoint vaqtini aniqlash.
**Yechim (SQL):**
```sql
SELECT 
    last_user_update,
    last_user_seek,
    last_user_scan
FROM sys.dm_db_index_usage_stats
WHERE database_id = DB_ID();
```
**Tushuntirish:** Checkpoint tez-tez sodir bo'lsa, I/O yuklamasi ortadi. Bu so'rov tizimning yozish intensivligini tushunishga yordam beradi.

### Topshiriq #1217: B+Tree chuqurligini (Depth) tahlil qilish
**Tavsif:** B+Tree chuqurligi qancha ko'p bo'lsa, ma'lumotni topish uchun shuncha ko'p disk operatsiyasi talab qilinadi.
**Talablar:** Indeks darajalarini (index_level) aniqlash.
**Yechim (SQL):**
```sql
SELECT 
    index_level, 
    page_count 
FROM sys.dm_db_index_physical_stats(DB_ID(), OBJECT_ID('Mahsulotlar'), NULL, NULL, 'DETAILED')
ORDER BY index_level DESC;
```
**Tushuntirish:** `index_level` 0 - bu barg tugunlari. Yuqori darajalar qanchalik ko'p bo'lsa, indeks shunchalik "chuqur" va sekinroq bo'ladi.

### Topshiriq #1218: Indeks ishlatilishini tekshirish (Unused Indexes)
**Tavsif:** Ishlatilmaydigan indekslar yozish operatsiyalarini sekinlashtiradi va disk joyini egallaydi.
**Talablar:** 30 kun davomida ishlatilmagan indekslarni topish.
**Yechim (SQL):**
```sql
SELECT name AS Indeks_Nomi
FROM sys.indexes
WHERE object_id = OBJECT_ID('Buyurtmalar')
AND index_id NOT IN (SELECT index_id FROM sys.dm_db_index_usage_stats WHERE database_id = DB_ID());
```
**Tushuntirish:** Keraksiz indekslarni o'chirish LSM-Tree yoki B+Tree tuzilmalarida yozish unumdorligini sezilarli darajada oshiradi.

### Topshiriq #1219: WAL log faylini qisqartirish (Shrink)
**Tavsif:** Tranzaksiya logi juda katta bo'lib ketganda, uni xavfsiz qisqartirish.
**Talablar:** Log faylini 100MB gacha qisqartirish.
**Yechim (SQL):**
```sql
BACKUP LOG [KhorazmiyDB] WITH TRUNCATE_ONLY; -- Logni tozalash
DBCC SHRINKFILE (KhorazmiyDB_Log, 100); -- 100MB gacha qisqartirish
```
**Tushuntirish:** WAL fayllari doimiy ravishda o'sib boradi. Uni vaqti-vaqti bilan tozalash bazaning barqaror ishlashini ta'minlaydi.

### Topshiriq #1220: Indeksni "Fill Factor" orqali optimallashtirish
**Tavsif:** B+Tree sahifalarida yangi ma'lumotlar uchun bo'sh joy qoldirish (page split'ni kamaytirish).
**Talablar:** Indeksni 80% to'ldirish darajasi bilan qayta yaratish.
**Yechim (SQL):**
```sql
CREATE INDEX IX_Mijozlar_Ism 
ON Mijozlar (Ism)
WITH (FILLFACTOR = 80, PAD_INDEX = ON);
```
**Tushuntirish:** `FILLFACTOR = 80` sahifalarda 20% bo'sh joy qoldiradi. Bu yangi ma'lumotlar qo'shilganda sahifani bo'lish (page split) operatsiyasini kamaytiradi, bu esa yozish tezligini oshiradi.

---

### Topshiriq #1221: B+Tree indeksining samaradorligini tahlil qilish
**Tavsif:** Katta hajmli jadvallarda `SELECT` so‘rovlari sekinlashganda, B+Tree indeksining chuqurligini (height) aniqlash va qidiruv samaradorligini baholash zarur.
**Talablar:** Indeks sahifalari soni va darajasini aniqlash, o‘qish operatsiyalari sonini minimallashtirish.
**Yechim (SQL):**
```sql
-- PostgreSQL tizim katalogidan indeks chuqurligini tekshirish
SELECT 
    i.relname AS index_name,
    s.index_depth AS depth
FROM pg_stat_index_info s
JOIN pg_class i ON s.indexrelid = i.oid
WHERE i.relname = 'idx_transactions_user_id'; -- Muayyan indeks uchun
```
**Tushuntirish:** B+Tree chuqurligi qancha kam bo‘lsa, diskdan ma’lumot o‘qish shunchalik kamayadi. Bu so‘rov indeks tuzilishini monitoring qilish uchun ishlatiladi.

### Topshiriq #1222: WAL (Write-Ahead Logging) holatini monitoring qilish
**Tavsif:** Tranzaksiyalar xavfsizligini ta’minlash uchun WAL fayllarining hajmi va yozilish tezligini nazorat qilish.
**Talablar:** WAL segmentlari sonini va oxirgi yozilish vaqtini aniqlash.
**Yechim (SQL):**
```sql
-- Joriy WAL holatini va o'tgan tranzaksiya loglarini ko'rish
SELECT 
    pg_current_wal_lsn() AS current_lsn,
    pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), '0/0')) AS total_wal_size;
```
**Tushuntirish:** WAL yozuvlari ma’lumotlar bazasi "crash" bo‘lganda ma’lumotlarni tiklash uchun muhim. Ushbu so‘rov tizimning yozish yuklamasini baholashga yordam beradi.

### Topshiriq #1223: LSM-Tree asosidagi "Compaction" jarayonini simulyatsiya qilish
**Tavsif:** LSM-Tree (Log-Structured Merge-Tree) da eskirgan ma’lumotlarni tozalash (compaction) jarayonini optimallashtirish.
**Talablar:** `deleted` bayrog‘i qo‘yilgan qatorlarni jismoniy o‘chirish va indeksni qayta qurish.
**Yechim (SQL):**
```sql
-- Eskirgan (tombstone) yozuvlarni tozalash va jadvalni optimallashtirish
DELETE FROM logs_table 
WHERE is_deleted = TRUE 
AND created_at < NOW() - INTERVAL '30 days';
VACUUM ANALYZE logs_table; -- Indeks va statistikani yangilash
```
**Tushuntirish:** LSM-Tree tuzilishida o‘chirish operatsiyasi darhol amalga oshmaydi. `VACUUM` orqali bo‘sh joyni qaytarish va indeksni qayta tartiblash ishlash tezligini oshiradi.

### Topshiriq #1224: Indeks fragmentatsiyasini aniqlash
**Tavsif:** Uzoq vaqt davomida `UPDATE` va `DELETE` operatsiyalari natijasida indekslarda bo‘sh joylar (fragmentatsiya) paydo bo‘ladi.
**Talablar:** Indeksning to‘liqlik darajasini (fill factor) tekshirish.
**Yechim (SQL):**
```sql
-- Indeksning samaradorligini (bloat) tahlil qilish
SELECT 
    relname AS table_name,
    index_relname AS index_name,
    (avg_leaf_fill_factor) AS fill_factor
FROM pgstatindex('idx_user_activity_date');
```
**Tushuntirish:** Agar `fill_factor` juda past bo‘lsa, indeks hajmi keraksiz darajada katta bo‘ladi va bu `I/O` operatsiyalarini sekinlashtiradi.

### Topshiriq #1225: Indekssiz qidiruvlarni (Full Table Scan) aniqlash
**Tavsif:** Ishlab chiqarish muhitida indekslanmagan ustunlar bo‘yicha qidiruvlar tizimni qulatishi mumkin.
**Talablar:** `seq_scan` (ketma-ket qidiruv) amalga oshirilgan jadvallarni aniqlash.
**Yechim (SQL):**
```sql
-- Eng ko'p to'liq jadval skanerlash (Full Table Scan) qilingan jadvallar
SELECT relname, seq_scan, seq_tup_read 
FROM pg_stat_user_tables 
ORDER BY seq_tup_read DESC 
LIMIT 10;
```
**Tushuntirish:** Ushbu so‘rov qaysi jadvallarga indeks qo‘shish kerakligini ko‘rsatib beradi. `seq_tup_read` yuqori bo‘lsa, indeks yetishmayapti.

### Topshiriq #1226: B+Tree "Covering Index" yaratish
**Tavsif:** Qidiruv tezligini maksimal darajaga chiqarish uchun faqat indeksning o‘zidan ma’lumot olish (Index Only Scan).
**Talablar:** `INCLUDE` kalit so‘zidan foydalanib, qo‘shimcha ustunlarni indeksga kiritish.
**Yechim (SQL):**
```sql
-- So'rovni tezlashtirish uchun qamrab oluvchi indeks
CREATE INDEX idx_orders_customer_total 
ON orders (customer_id) 
INCLUDE (total_amount); -- Asosiy jadvalga murojaat qilmasdan ma'lumot olish
```
**Tushuntirish:** `INCLUDE` yordamida indeks barglarida qo‘shimcha ma’lumot saqlanadi, bu esa "Heap Fetch" (asosiy jadvalga murojaat) jarayonini bartaraf etadi.

### Topshiriq #1227: WAL yozish kechikishini (Latency) o‘lchash
**Tavsif:** Tranzaksiyalar yozilishida WAL disklari bottleneck (to‘siq) bo‘lib qolmasligini ta’minlash.
**Talablar:** WAL yozish operatsiyalari uchun ketgan vaqtni tahlil qilish.
**Yechim (SQL):**
```sql
-- WAL yozish vaqti statistikasi
SELECT 
    wait_event_type, 
    count(*) 
FROM pg_stat_activity 
WHERE wait_event_type = 'WALWrite' 
GROUP BY wait_event_type;
```
**Tushuntirish:** Agar `WALWrite` hodisalari ko‘p bo‘lsa, disk tezligi (IOPS) yetarli emasligini anglatadi.

### Topshiriq #1228: Indeksni "Hot" (Heap Only Tuple) optimizatsiyasi
**Tavsif:** `UPDATE` operatsiyalari vaqtida indeksni yangilash xarajatini kamaytirish.
**Talablar:** `FILLFACTOR` parametrini sozlash orqali sahifa ichida yangilanishlarni amalga oshirish.
**Yechim (SQL):**
```sql
-- Indeks sahifalarida bo'sh joy qoldirish (HOT uchun)
ALTER TABLE users SET (fillfactor = 80);
-- Jadvalni qayta qurish
VACUUM FULL users;
```
**Tushuntirish:** `FILLFACTOR` 80 ga tushirilsa, sahifalarda yangi versiyalar uchun joy qoladi va indeks ko‘rsatkichlarini yangilash shart bo‘lmaydi.

### Topshiriq #1229: Indeks ishlatilishi monitoringi
**Tavsif:** Keraksiz indekslarni aniqlash va ularni o‘chirish orqali yozish tezligini oshirish.
**Talablar:** Hech qachon ishlatilmagan indekslarni topish.
**Yechim (SQL):**
```sql
-- Ishlatilmagan indekslarni aniqlash
SELECT indexrelname 
FROM pg_stat_user_indexes 
WHERE idx_scan = 0 
AND indexrelname NOT LIKE '%pkey';
```
**Tushuntirish:** Har bir indeks `INSERT/UPDATE` operatsiyalarini sekinlashtiradi. Ishlatilmaydigan indekslarni o‘chirish yozish unumdorligini oshiradi.

### Topshiriq #1230: LSM-Tree "Bloom Filter" samaradorligini tekshirish
**Tavsif:** LSM-Tree tuzilishida ma’lumot qaysi faylda ekanligini tez aniqlash uchun Bloom Filterdan foydalanish.
**Talablar:** Bloom filter indeksini yaratish va uning hajmini boshqarish.
**Yechim (SQL):**
```sql
-- Bloom filter kengaytmasini ishlatish
CREATE EXTENSION IF NOT EXISTS bloom;
CREATE INDEX idx_bloom_search 
ON large_data_table USING bloom (category_id, status);
```
**Tushuntirish:** Bloom filter qidiruv vaqtida qaysi ma’lumotlar bloki (SSTable) ichida kerakli ma’lumot yo‘qligini darhol aniqlab beradi, bu esa diskdan o‘qishni keskin kamaytiradi.

---

### Topshiriq #1231: B+Tree indeks samaradorligini tahlil qilish
**Tavsif:** Katta hajmli jadvallarda `SELECT` so‘rovlari sekinlashganda, B+Tree indeksining chuqurligi (height) va sahifa (page) to‘liqligini aniqlash zarur.
**Talablar:** Indeksning samaradorligini baholash uchun `sys.dm_db_index_physical_stats` funksiyasidan foydalaning.
**Yechim (SQL):**
```sql
-- Indeksning parchalanish darajasi va sahifa to'liqligini tekshirish
SELECT 
    OBJECT_NAME(object_id) AS Jadval,
    index_id,
    avg_page_space_used_in_percent AS Sahifa_Bandligi,
    avg_fragmentation_in_percent AS Parchalanish_Foizi
FROM sys.dm_db_index_physical_stats(DB_ID(), OBJECT_ID('Foydalanuvchilar'), NULL, NULL, 'DETAILED')
WHERE avg_fragmentation_in_percent > 10; -- 10% dan yuqori parchalanishni aniqlash
```
**Tushuntirish:** B+Tree indekslarida parchalanish (fragmentation) oshishi I/O operatsiyalarini ko‘paytiradi. Ushbu so‘rov indeksni qayta qurish (rebuild) kerakligini aniqlashga yordam beradi.

---

### Topshiriq #1232: WAL (Write-Ahead Logging) holatini monitoring qilish
**Tavsif:** Tranzaksiyalar xavfsizligini ta'minlash uchun WAL log fayllari hajmini nazorat qilish va tizim xatolarini oldini olish.
**Talablar:** Log faylining to‘lib ketish xavfini aniqlash va tranzaksiya logi hajmini kuzatish.
**Yechim (SQL):**
```sql
-- Tranzaksiya logi ishlatilish foizini ko'rish
SELECT 
    name AS Log_Fayl_Nomi,
    size/128.0 AS Hajmi_MB,
    FILEPROPERTY(name, 'SpaceUsed')/128.0 AS Ishlatilgan_MB
FROM sys.master_files 
WHERE type_desc = 'LOG';
```
**Tushuntirish:** WAL tizimida log fayli to‘lib qolsa, ma'lumotlar bazasi yozishni to‘xtatadi. Bu so‘rov log hajmini real vaqtda kuzatib, tizim barqarorligini ta'minlaydi.

---

### Topshiriq #1233: LSM-Tree asosidagi yozish buferini optimallashtirish
**Tavsif:** LSM-Tree tuzilmasida yozish operatsiyalari uchun MemTable (xotira buferi) hajmini sozlash.
**Talablar:** Yozish tezligini oshirish uchun `buffer_pool` samaradorligini tahlil qilish.
**Yechim (SQL):**
```sql
-- Buffer pool'dagi sahifalar taqsimotini tahlil qilish
SELECT 
    COUNT(*) AS Sahifalar_Soni,
    CASE WHEN is_modified = 1 THEN 'O\'zgartirilgan (Dirty)' ELSE 'Toza' END AS Holat
FROM sys.dm_os_buffer_descriptors
WHERE database_id = DB_ID()
GROUP BY is_modified;
```
**Tushuntirish:** LSM-Tree yozishni avval xotiraga (MemTable) amalga oshiradi. "Dirty" sahifalar ko‘pligi yozish yuklamasi yuqoriligini bildiradi, bu esa flush jarayonini tezlashtirish kerakligini anglatadi.

---

### Topshiriq #1234: Indeks qamrovini (Covering Index) optimallashtirish
**Tavsif:** `INCLUDE` kalit so‘zi yordamida so‘rovlarni diskdan o‘qimasdan, faqat indeks orqali bajarish.
**Talablar:** `SELECT` so‘rovida ishlatiladigan barcha ustunlarni indeksga kiritish.
**Yechim (SQL):**
```sql
-- Qamrovchi indeks yaratish (Index Seek uchun)
CREATE NONCLUSTERED INDEX IX_Foydalanuvchi_Email 
ON Foydalanuvchilar (Email) 
INCLUDE (Ism, Familiya); -- Asosiy jadvalga murojaatni kamaytiradi
```
**Tushuntirish:** `INCLUDE` qismi ma'lumotlarni "leaf node" darajasida saqlaydi, bu esa "Key Lookup" operatsiyasini bartaraf etib, tezlikni keskin oshiradi.

---

### Topshiriq #1235: Indeks tanlash strategiyasi (Clustered vs Non-Clustered)
**Tavsif:** Jadval uchun to‘g‘ri klasterlangan indeksni tanlash (Primary Key tanlovi).
**Talablar:** Indeks kaliti sifatida ketma-ket (sequential) qiymatlarni tanlash.
**Yechim (SQL):**
```sql
-- Klasterlangan indeksni qayta aniqlash
ALTER TABLE Buyurtmalar 
ADD CONSTRAINT PK_Buyurtmalar PRIMARY KEY CLUSTERED (BuyurtmaID); -- Identity (1,1) bo'lishi shart
```
**Tavsif:** B+Tree tuzilmasida klasterlangan indeks ketma-ket bo‘lmasa, "page split" hodisasi yuz beradi. Bu esa yozish unumdorligini pasaytiradi.

---

### Topshiriq #1236: Indekslashda "Fill Factor" ni sozlash
**Tavsif:** Sahifalarda bo‘sh joy qoldirib, yozish paytida sahifa bo‘linishini (page split) kamaytirish.
**Talablar:** `FILLFACTOR` parametrini 80-90% oralig‘ida belgilash.
**Yechim (SQL):**
```sql
-- Indeksni 80% to'ldirish bilan qayta qurish
ALTER INDEX IX_Mahsulotlar_Narx ON Mahsulotlar
REBUILD WITH (FILLFACTOR = 80);
```
**Tushuntirish:** Agar jadvalga tez-tez yangi ma'lumotlar qo‘shilsa, sahifalarni 100% to‘ldirmaslik "page split" xarajatlarini kamaytiradi.

---

### Topshiriq #1237: Keraksiz indekslarni aniqlash
**Tavsif:** Tizimda ishlatilmaydigan indekslar yozish operatsiyalarini sekinlashtiradi.
**Talablar:** `user_seeks`, `user_scans` qiymatlari 0 bo‘lgan indekslarni topish.
**Yechim (SQL):**
```sql
SELECT name AS Indeks_Nomi 
FROM sys.indexes 
WHERE object_id = OBJECT_ID('Tranzaksiyalar') 
AND index_id NOT IN (SELECT index_id FROM sys.dm_db_index_usage_stats WHERE user_seeks > 0);
```
**Tushuntirish:** Har bir indeks yozish paytida yangilanishi kerak. Ishlatilmaydigan indekslarni o‘chirish yozish tezligini oshiradi.

---

### Topshiriq #1238: WAL Checkpoint jarayonini kuzatish
**Tavsif:** WAL logidagi o‘zgarishlarni ma'lumotlar fayliga yozish (Checkpoint) vaqtini optimallashtirish.
**Talablar:** Checkpointlar orasidagi vaqtni tahlil qilish.
**Yechim (SQL):**
```sql
-- Oxirgi checkpoint vaqtini tekshirish
SELECT last_recovery_fork_guid, last_checkpoint_lsn 
FROM sys.database_recovery_status;
```
**Tushuntirish:** Checkpoint tez-tez amalga oshirilsa, I/O yuklamasi ortadi. Kam amalga oshirilsa, tizim tiklanishi (recovery) uzoq davom etadi.

---

### Topshiriq #1239: Indeks statistikasi yangilanishi
**Tavsif:** Query Optimizer to‘g‘ri qaror qabul qilishi uchun indeks statistikasini dolzarb saqlash.
**Talablar:** Statistikani avtomatik yangilashni yoqish va qo‘lda yangilash.
**Yechim (SQL):**
```sql
-- Statistikani yangilash
UPDATE STATISTICS Foydalanuvchilar WITH FULLSCAN;
```
**Tushuntirish:** B+Tree qidiruv yo‘lini tanlashda statistika muhim rol o‘ynaydi. `FULLSCAN` eng aniq ma'lumotni beradi.

---

### Topshiriq #1240: Xotira ichidagi (In-Memory) indekslar
**Tavsif:** Juda tezkor qidiruv talab qilinadigan jadvallar uchun xotira indekslaridan foydalanish.
**Talablar:** `MEMORY_OPTIMIZED` jadval uchun `NONCLUSTERED HASH` indeksini yaratish.
**Yechim (SQL):**
```sql
-- Hash indeks yaratish (O(1) murakkablik)
CREATE TABLE Tezkor_Kesh (
    ID INT PRIMARY KEY NONCLUSTERED HASH WITH (BUCKET_COUNT = 10000),
    Qiymat NVARCHAR(100)
) WITH (MEMORY_OPTIMIZED = ON, DURABILITY = SCHEMA_ONLY);
```
**Tushuntirish:** Hash indekslar B+Tree'dan farqli o‘laroq, aniq moslik qidiruvlarida O(1) vaqt murakkabligini ta'minlaydi, bu esa eng yuqori unumdorlikdir.

---

### Topshiriq #1241: B+Tree indeksining to‘liqligini tekshirish
**Tavsif:** Ma'lumotlar bazasida indekslarning parchalanishi (fragmentation) va barg tugunlarining to‘lish darajasini aniqlash.
**Talablar:** Indeks sahifalarining 70% dan kam to‘lganligini aniqlash va samaradorlikni baholash.
**Yechim (SQL):**
```sql
-- Indeks sahifalarining to‘lish darajasini tahlil qilish
SELECT 
    index_name, 
    avg_page_space_used_in_percent,
    avg_fragmentation_in_percent
FROM sys.dm_db_index_physical_stats(DB_ID(), OBJECT_ID('Khorazmiy_Data'), NULL, NULL, 'DETAILED')
WHERE avg_page_space_used_in_percent < 70; -- 70% dan kam to‘lgan sahifalarni topish
```
**Tushuntirish:** B+Tree tuzilishida sahifalar bo‘sh qolganda I/O operatsiyalari ortadi. Ushbu so‘rov indeksni qayta qurish (rebuild) zarurligini aniqlash uchun ishlatiladi.

### Topshiriq #1242: WAL (Write-Ahead Logging) holatini monitoring qilish
**Tavsif:** Tranzaksiyalar jurnalining (WAL) hajmi va yozish tezligini nazorat qilish.
**Talablar:** Jurnal fayli hajmi 2GB dan oshganda ogohlantirish berish.
**Yechim (SQL):**
```sql
-- WAL log fayli hajmini tekshirish
SELECT 
    name AS LogFileName, 
    size/128 AS SizeInMB 
FROM sys.master_files 
WHERE type_desc = 'LOG' 
AND size/128 > 2048; -- 2GB dan oshgan log fayllar
```
**Tushuntirish:** WAL ma'lumotlar bazasi yaxlitligini ta'minlaydi. Log faylning haddan tashqari o‘sishi disk to‘lishiga va tizim sekinlashishiga olib keladi.

### Topshiriq #1243: LSM-Tree uchun "Compaction" strategiyasi
**Tavsif:** LSM-Tree tuzilishida eski (stale) ma'lumotlarni tozalash va "SSTables"ni birlashtirish.
**Talablar:** O‘chirilgan (tombstone) yozuvlarni aniqlash va ularni bazadan jismonan o‘chirish.
**Yechim (SQL):**
```sql
-- O‘chirilgan yozuvlar (tombstones) mavjud bo‘lgan qatorlarni tozalash
DELETE FROM SSTable_Storage 
WHERE is_deleted = 1 
AND timestamp < DATEADD(day, -30, GETDATE()); -- 30 kundan eski o‘chirilgan ma'lumotlar
```
**Tavsif:** LSM-Tree'da ma'lumotlar darhol o‘chirilmaydi, balki "tombstone" belgisi qo‘yiladi. Bu so‘rov xotirani bo‘shatish uchun "Compaction" jarayonini simulyatsiya qiladi.

### Topshiriq #1244: Indeks tanlashda "Covering Index" yaratish
**Tavsif:** Murakkab so‘rovlar uchun faqat indeksning o‘zidan ma'lumot olib, jadvalga murojaat qilmaslik (Index Seek).
**Talablar:** `User_ID` va `Access_Date` bo‘yicha qidiruvni optimallashtirish.
**Yechim (SQL):**
```sql
-- Covering Index yaratish
CREATE NONCLUSTERED INDEX IX_UserAccess_Covering
ON User_Logs (User_ID, Access_Date)
INCLUDE (Action_Type); -- Kerakli qo‘shimcha ustunlar
```
**Tushuntirish:** `INCLUDE` kalit so‘zi yordamida ma'lumotlar barg tugunlariga qo‘shiladi, bu esa "Key Lookup" operatsiyasini bartaraf etib, tezlikni oshiradi.

### Topshiriq #1245: B+Tree "Deadlock" monitoringi
**Tavsif:** Indeks sahifalarini yangilashda yuzaga keladigan qulflar (locks) to‘qnashuvini aniqlash.
**Talablar:** Qulflangan resurslarni aniqlash va tranzaksiya identifikatorini qaytarish.
**Yechim (SQL):**
```sql
-- Qulflangan resurslarni aniqlash
SELECT 
    request_session_id, 
    resource_type, 
    request_mode 
FROM sys.dm_tran_locks 
WHERE resource_database_id = DB_ID();
```
**Tushuntirish:** B+Tree tuzilishida yuqori darajadagi tugunlarga bo‘lgan raqobat (contention) tizimni to‘xtatib qo‘yishi mumkin. Ushbu so‘rov qulf ziddiyatlarini tahlil qiladi.

### Topshiriq #1246: WAL checkpoint vaqtini optimallashtirish
**Tavsif:** WAL ma'lumotlarini diskka yozish (checkpoint) chastotasini boshqarish.
**Talablar:** Oxirgi checkpoint vaqtini aniqlash va tizim yuklamasini baholash.
**Yechim (SQL):**
```sql
-- Oxirgi checkpoint vaqtini tekshirish
SELECT 
    last_checkpoint_database, 
    last_checkpoint_time 
FROM sys.dm_os_sys_info;
```
**Tushuntirish:** Checkpoint jarayoni tez-tez amalga oshirilsa, disk yuklamasi ortadi; kam amalga oshirilsa, tizim tiklanish vaqti (Recovery Time) uzayadi.

### Topshiriq #1247: Indeks samaradorligini tahlil qilish (Unused Indexes)
**Tavsif:** Ishlatilmayotgan indekslarni aniqlab, yozish operatsiyalarini tezlashtirish.
**Talablar:** So‘nggi 30 kunda foydalanilmagan indekslarni topish.
**Yechim (SQL):**
```sql
-- Ishlatilmayotgan indekslarni topish
SELECT o.name AS TableName, i.name AS IndexName
FROM sys.indexes i
JOIN sys.objects o ON i.object_id = o.object_id
WHERE i.is_primary_key = 0 
AND i.index_id NOT IN (SELECT index_id FROM sys.dm_db_index_usage_stats);
```
**Tushuntirish:** Har bir indeks yozish (INSERT/UPDATE) operatsiyasini sekinlashtiradi. Keraksiz indekslarni o‘chirish yozish unumdorligini oshiradi.

### Topshiriq #1248: B+Tree chuqurligini (Depth) o‘lchash
**Tavsif:** Indeksning qidiruv chuqurligini aniqlash orqali qidiruv tezligini prognoz qilish.
**Talablar:** Indeks darajasi 4 dan yuqori bo‘lganlarni aniqlash.
**Yechim (SQL):**
```sql
-- Indeks darajasini tekshirish
SELECT 
    name, 
    index_level, 
    page_count 
FROM sys.dm_db_index_physical_stats(DB_ID(), OBJECT_ID('Khorazmiy_Data'), NULL, NULL, 'DETAILED')
WHERE index_level > 4;
```
**Tushuntirish:** B+Tree darajasi (height) qancha yuqori bo‘lsa, ma'lumotni topish uchun shuncha ko‘p disk o‘qish operatsiyasi kerak bo‘ladi.

### Topshiriq #1249: WAL yozish kechikishini (Latency) o‘lchash
**Tavsif:** WAL yozish jarayonidagi kechikishlarni aniqlash.
**Talablar:** Diskdagi log yozish tezligini millisekundlarda o‘lchash.
**Yechim (SQL):**
```sql
-- Log yozish kechikishini tahlil qilish
SELECT 
    io_stall_write_ms / num_of_writes AS AvgWriteLatency
FROM sys.dm_io_virtual_file_stats(DB_ID(), 2); -- 2 - odatda log fayl ID si
```
**Tavsif:** WAL yozish tezligi tranzaksiya unumdorligining asosiy omilidir. Yuqori kechikish diskdagi muammolarni ko‘rsatadi.

### Topshiriq #1250: Indeksni "Fill Factor" orqali optimallashtirish
**Tavsif:** Indeks sahifalaridagi bo‘sh joyni boshqarish orqali "Page Splits" (sahifa bo‘linishi) ni kamaytirish.
**Talablar:** Indeks uchun 80% Fill Factor belgilash.
**Yechim (SQL):**
```sql
-- Indeksni 80% Fill Factor bilan qayta qurish
ALTER INDEX IX_Khorazmiy_Main 
ON Khorazmiy_Data 
REBUILD WITH (FILLFACTOR = 80);
```
**Tushuntirish:** Fill Factor 80% bo‘lganda, har bir sahifada 20% bo‘sh joy qoladi. Bu yangi ma'lumotlar qo‘shilganda sahifa bo‘linishining oldini oladi va ishlash tezligini barqarorlashtiradi.