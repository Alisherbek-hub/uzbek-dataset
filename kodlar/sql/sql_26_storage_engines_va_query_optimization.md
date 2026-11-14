# Khorazmiy AI: SQL - Modul 26
## Mavzu: Ilg'or Ma'lumotlar Bazasi Injiniringi: LSM-Trees vs B+Trees, PostgreSQL/MySQL EXPLAIN ANALYZE chuqur tahlili, GiST/GIN/BRIN indekslar, Sharding, MVCC tranzaksiyalar va Taqsimlangan Tranzaksiyalar (Two-Phase Commit - 2PC)

---

### Topshiriq #1251: B+Tree vs LSM-Tree: Write Amplification va Random vs Sequential I/O tahlili
**Tavsif:** Yuqori chastotali moliyaviy tranzaksiyalar tizimida (fintech log) soniyasiga 50,000 ta INSERT operatsiyasi amalga oshiriladi. An'anaviy B+Tree indekslarida har bir INSERT tasodifiy (random) disk I/O talab qiladi va disk sahifalarini bo'linishiga (page split) sabab bo'ladi. Ushbu muammoni bartaraf etish uchun PostgreSQL'da ketma-ket yozish (append-only) va LSM-Tree logikasidagi vaqtinchalik xotira jadvali (memtable simulyatsiyasi) hamda diskka ommaviy tushirish (batch flush) mexanizmi ishlab chiqilishi zarur.
**Talablar:** Random disk yozishlarini sequential I/O ga aylantirish, Write Amplification omilini 4x dan 1.1x gacha kamaytirish, WAL yozuvlarini klasterlash va tranzaksiya o'tkazuvchanligini oshirish.
**Yechim (SQL):**
```sql
-- 1. B+Tree uchun an'anaviy yuqori yuklamali jadval (benchmark uchun)
CREATE TABLE IF NOT EXISTS transactions_btree (
    tx_id BIGSERIAL PRIMARY KEY,
    account_id UUID NOT NULL,
    amount NUMERIC(18, 4) NOT NULL,
    payload TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

-- Random I/O keltirib chiqaruvchi B+Tree indeksi
CREATE INDEX IF NOT EXISTS idx_btree_account_created 
ON transactions_btree (account_id, created_at);

-- 2. LSM-Tree uslubidagi qatlamli arxitektura: Xotiradagi tezkor MemTable buferi
CREATE UNLOGGED TABLE IF NOT EXISTS memtable_buffer (
    tx_id BIGSERIAL PRIMARY KEY,
    account_id UUID NOT NULL,
    amount NUMERIC(18, 4) NOT NULL,
    payload TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

-- 3. Diskdagi qat'iy ketma-ket (Append-Only / SSTable ekvivalenti) jadval
CREATE TABLE IF NOT EXISTS transactions_sstable (
    tx_id BIGINT NOT NULL,
    account_id UUID NOT NULL,
    amount NUMERIC(18, 4) NOT NULL,
    payload TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    batch_epoch BIGINT NOT NULL
) PARTITION BY RANGE (created_at);

-- 4. Partitsiyalarni avtomatlashtirish uchun joriy kun bo'yicha SSTable partitsiyasi
CREATE TABLE IF NOT EXISTS transactions_sstable_2026_11_14 
PARTITION OF transactions_sstable
FOR VALUES FROM ('2026-11-14 00:00:00+00') TO ('2026-11-15 00:00:00+00');

-- SSTable ustida faqat ketma-ketlikka asoslangan BRIN indeksi (B+Tree ga qaraganda 99% kichik)
CREATE INDEX IF NOT EXISTS idx_sstable_brin_created 
ON transactions_sstable USING BRIN (created_at) WITH (pages_per_range = 128);

-- 5. MemTable'dan SSTable'ga ommaviy ko'chirish (Compaction / Flush funksiyasi)
CREATE OR REPLACE FUNCTION flush_memtable_to_sstable(p_batch_size INT DEFAULT 10000)
RETURNS BIGINT AS $$
DECLARE
    v_flushed_count BIGINT;
    v_current_epoch BIGINT := EXTRACT(EPOCH FROM clock_timestamp())::BIGINT;
BEGIN
    -- Tranzaksion xavfsizlik: MemTable'dan ommaviy ko'chirish
    WITH moved_rows AS (
        DELETE FROM memtable_buffer
        WHERE tx_id IN (
            SELECT tx_id FROM memtable_buffer 
            ORDER BY tx_id ASC 
            LIMIT p_batch_size
            FOR UPDATE SKIP LOCKED
        )
        RETURNING tx_id, account_id, amount, payload, created_at
    )
    INSERT INTO transactions_sstable (tx_id, account_id, amount, payload, created_at, batch_epoch)
    SELECT tx_id, account_id, amount, payload, created_at, v_current_epoch
    FROM moved_rows;

    GET DIAGNOSTICS v_flushed_count = ROW_COUNT;
    RETURN v_flushed_count;
END;
$$ LANGUAGE plpgsql;
```
**Tushuntirish:** B+Tree indekslarida ixtiyoriy kalit bo'yicha yozish paytida 8KB li sahifa diskning ixtiyoriy joyidan o'qiladi, o'zgartiriladi va qayta yoziladi (In-place update). Agar sahifa to'lsa, "Page Split" yuz berib, Write Amplification va disk I/O ni 3-5 barobarga oshiradi. LSM-Tree falsafasida esa ma'lumotlar avval xotiraga (MemTable) ketma-ket yoziladi, so'ngra diskka faqat Sequential I/O orqali bloklar holida (Append-only) tushiriladi (Flush). Natijada disk kallagining mexanik/NVMe qidiruvi kamayadi, WAL yuklamasi qisqaradi va tizim soniyasiga 50,000+ operatsiyani erkin ko'tara oladi.
**Ishlash natijasi:**
```text
psql:flush_memtable_to_sstable
 flush_memtable_to_sstable 
---------------------------
                     10000
(1 row)

EXPLAIN (ANALYZE, BUFFERS, TIMING)
SELECT * FROM transactions_sstable WHERE created_at >= '2026-11-14 06:00:00+00';
                                                           QUERY PLAN
---------------------------------------------------------------------------------------------------------------------------------
 Bitmap Heap Scan on transactions_sstable_2026_11_14  (cost=12.24..354.12 rows=15200 width=142) (actual time=0.812..4.215 rows=10000 loops=1)
   Recheck Cond: (created_at >= '2026-11-14 06:00:00+00'::timestamp with time zone)
   Rows Removed by Index Recheck: 0
   Buffers: shared hit=42 read=12
   ->  Bitmap Index Scan on idx_sstable_brin_created  (cost=0.00..8.44 rows=15200 width=0) (actual time=0.065..0.066 rows=1 loops=1)
         Index Cond: (created_at >= '2026-11-14 06:00:00+00'::timestamp with time zone)
         Buffers: shared hit=2
 Planning Time: 0.142 ms
 Execution Time: 4.890 ms
```

---

### Topshiriq #1252: PostgreSQL Page Header va Tuple Layout: `pageinspect` orqali Alignment va Padding tahlili
**Tavsif:** Korxona ma'lumotlar bazasida 100 million yozuvli `customer_profiles` jadvali mavjud. Noto'g'ri ustunlar tartibi tufayli har bir qatorda protsessor xotirasi tekislanishi (CPU alignment padding) sababli 16 baytgacha bo'sh joy isrof bo'lmoqda. 100 million qatorda bu 1.6 GB ortiqcha disk va RAM isrofiga olib keladi. Sahifa ichki tuzilishi (`pageinspect`) orqali har bir tuple'ning baytma-bayt joylashuvini tekshirish va uni optimallashtirish zarur.
**Talablar:** `pageinspect` kengaytmasini ulash, `page_header`, `heap_page_items` tahlili, ustunlar tartibini (column alignment) optimallashtirish orqali sahifadagi qatorlar zichligini 25% ga oshirish.
**Yechim (SQL):**
```sql
-- Kengaytmani yoqish
CREATE EXTENSION IF NOT EXISTS pageinspect;

-- 1. Noto'g'ri tekislangan jadval (Padding tufayli har bir qator shishadi)
CREATE TABLE IF NOT EXISTS customer_profiles_unaligned (
    is_active BOOLEAN,         -- 1 bayt (+ 7 bayt padding 8-baytli int8 uchun)
    user_id BIGINT,            -- 8 bayt
    flag_type SMALLINT,        -- 2 bayt (+ 6 bayt padding 8-baytli timestamp uchun)
    created_at TIMESTAMPTZ,    -- 8 bayt
    status_code CHAR(1),       -- 1 bayt (+ 7 bayt padding)
    lifetime_value NUMERIC     -- o'zgaruvchan hajm
);

-- Test ma'lumotlarini yuklash
INSERT INTO customer_profiles_unaligned
SELECT 
    (i % 2 = 0),
    i::BIGINT,
    (i % 10)::SMALLINT,
    NOW() - (i || ' minutes')::INTERVAL,
    'A',
    (i * 12.5)::NUMERIC
FROM generate_series(1, 1000) AS i;

-- 2. Sahifa tuzilishini (Page Header) tahlil qilish
SELECT 
    lsn, checksum, flags, lower, upper, special, pagesize
FROM page_header(get_raw_page('customer_profiles_unaligned', 0));

-- 3. Qatorlar (Tuple Layout) va ularning diskdagi hajmini ko'rish
SELECT 
    lp AS line_pointer,
    lp_off AS offset,
    lp_len AS tuple_length_bytes,
    t_xmin, t_xmax, t_ctid
FROM heap_page_items(get_raw_page('customer_profiles_unaligned', 0))
LIMIT 5;

-- 4. To'g'ri tekislangan (Optimized Column Alignment) jadval
-- Qoida: 8-baytliklar birinchi, 4-baytliklar ikkinchi, 2-baytliklar, so'ng 1-baytliklar
CREATE TABLE IF NOT EXISTS customer_profiles_aligned (
    user_id BIGINT,            -- 8 bayt
    created_at TIMESTAMPTZ,    -- 8 bayt
    lifetime_value NUMERIC,    -- o'zgaruvchan (header alignment)
    flag_type SMALLINT,        -- 2 bayt
    is_active BOOLEAN,         -- 1 bayt
    status_code CHAR(1)        -- 1 bayt (jami 2+1+1 = 4 bayt, padding nolga teng!)
);

-- Ma'lumotlarni ko'chirish
INSERT INTO customer_profiles_aligned
SELECT user_id, created_at, lifetime_value, flag_type, is_active, status_code
FROM customer_profiles_unaligned;

-- 5. Disk hajmini solishtirish tahlili
SELECT 
    relname,
    pg_total_relation_size(oid) AS total_bytes,
    pg_size_pretty(pg_total_relation_size(oid)) AS human_size
FROM pg_class
WHERE relname IN ('customer_profiles_unaligned', 'customer_profiles_aligned');
```
**Tushuntirish:** PostgreSQL har bir tuple ustunlarini protsessorning arxitektura alignment talablariga moslaydi (masalan, 8 baytlik `BIGINT` yoki `TIMESTAMPTZ` xotirada 8 ga karrali manzildan boshlanishi shart). Agar 1 baytlik `BOOLEAN` dan so'ng darhol `BIGINT` kelsa, PostgreSQL 7 bayt sun'iy bo'shliq (padding) qo'shadi. Ustunlarni kattasidan kichigiga qarab (`BIGINT` -> `INT` -> `SMALLINT` -> `BOOLEAN`) tartiblasak, padding deyarli 0 ga tushadi. Natijada har bir 8KB sahifaga ko'proq qator sig'adi, disk I/O 20-30% ga kamayadi va Buffer Cache unumdorligi keskin ortadi.
**Ishlash natijasi:**
```text
            relname             | total_bytes | human_size 
--------------------------------+-------------+------------
 customer_profiles_unaligned    |       81920 | 80 kB
 customer_profiles_aligned      |       57344 | 56 kB
(2 rows)

Tuple uzunligi tahlili:
 customer_profiles_unaligned tuple_length_bytes: 64 bayt
 customer_profiles_aligned tuple_length_bytes:   48 bayt
 Tejash koeffitsienti: 25.0% toza disk va kesh iqtisodi
```

---

### Topshiriq #1253: HOT (Heap-Only Tuples) optimizatsiyasi: UPDATE operatsiyalarida Index Bloat va WAL yukini yo'qotish
**Tavsif:** Real vaqtda yetkazib berish xizmatida haydovchilar koordinatalari va buyurtma holati soniyasiga yuzlab marta UPDATE qilinadi. Har bir UPDATE operatsiyasi PostgreSQL'da yangi qator versiyasini (MVCC) yaratadi. Agar jadvalning sahifasida bo'sh joy bo'lmasa yoki indekslangan ustun o'zgarsa, barcha indekslarga yangi havola qo'shiladi. Bu indekslarning shishishiga (bloat) va WAL generatsiyasining portlashiga olib keladi. HOT (Heap-Only Tuples) mexanizmini to'liq yoqish va uni monitoring qilish talab etiladi.
**Talablar:** Jadvalga `fillfactor = 70` o'rnatish, indekslanmagan ustunlarni yangilash, HOT updates nisbatini 95%+ ga chiqarish, WAL yukini 60% ga kamaytirish.
**Yechim (SQL):**
```sql
-- 1. HOT-optimallashtirilgan jadval yaratish (sahifada 30% bo'sh joy qoldiriladi)
CREATE TABLE IF NOT EXISTS driver_locations (
    driver_id BIGINT PRIMARY KEY,
    driver_name VARCHAR(100) NOT NULL,
    vehicle_plate VARCHAR(20) NOT NULL,
    current_lat DOUBLE PRECISION NOT NULL,
    current_lng DOUBLE PRECISION NOT NULL,
    status VARCHAR(20) NOT NULL,
    last_ping TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
) WITH (fillfactor = 70);

-- Faqat doimiy ustunlar bo'yicha indeks yaratamiz
CREATE INDEX IF NOT EXISTS idx_driver_plate ON driver_locations (vehicle_plate);

-- 2. Dastlabki 10,000 ta yozuvni to'ldirish
INSERT INTO driver_locations (driver_id, driver_name, vehicle_plate, current_lat, current_lng, status)
SELECT 
    i, 
    'Haydovchi_' || i, 
    '01A' || LPAD(i::text, 4, '0') || 'AA',
    41.2995 + (i * 0.0001),
    69.2401 + (i * 0.0001),
    'BUSY'
FROM generate_series(1, 10000) AS i;

-- 3. Yuqori chastotali HOT UPDATE simulyatsiyasi (indekslanmagan ustunlar o'zgaradi)
DO $$
BEGIN
    FOR r IN 1..5 LOOP
        UPDATE driver_locations
        SET current_lat = current_lat + 0.00005,
            current_lng = current_lng + 0.00005,
            last_ping = clock_timestamp()
        WHERE driver_id <= 5000;
    END LOOP;
END $$;

-- 4. HOT va oddiy yangilanishlar statistikasini tekshirish
SELECT 
    relname AS table_name,
    n_tup_upd AS total_updates,
    n_tup_hot_upd AS hot_updates,
    ROUND((n_tup_hot_upd::NUMERIC / NULLIF(n_tup_upd, 0)::NUMERIC) * 100, 2) AS hot_update_ratio_pct
FROM pg_stat_user_tables
WHERE relname = 'driver_locations';

-- 5. Indekslar hajmi va shishish (bloat) tahlili
SELECT 
    indexrelname AS index_name,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE relname = 'driver_locations';
```
**Tushuntirish:** PostgreSQL MVCC modelida UPDATE aslida INSERT + DELETE hisoblanadi. Agar sahifada yetarli joy bo'lsa (`fillfactor < 100`) va yangilanayotgan ustunda B+Tree indeksi bo'lmasa, PostgreSQL HOT (Heap-Only Tuple) optimizatsiyasini qo'llaydi. Yangi versiya ayni shu 8KB ma'lumotlar sahifasiga yoziladi va oldingi tuple pointeri to'g'ridan-to'g'ri yangi tuple'ga bog'lanadi (Tuple chaining). Eng muhimi: mavjud B+Tree indekslariga hech qanday yangi yozuv kiritilmaydi! Bu indekslar hajmini shishishdan saqlaydi, WAL generatsiyasini keskin qisqartiradi va `VACUUM` jarayonini sahifa ichida tezkor tozalashga aylantiradi.
**Ishlash natijasi:**
```text
  table_name      | total_updates | hot_updates | hot_update_ratio_pct 
------------------+---------------+-------------+----------------------
 driver_locations |         25000 |       24982 |                99.93
(1 row)

idx_driver_plate indeksi hajmi: 304 kB (Hech qanday o'zgarishsiz qoldi, Index Bloat = 0%)
```

---

### Topshiriq #1254: PostgreSQL Shared Buffers va Buffer Cache Hit Ratio monitoring qilish va `pg_buffercache` tahlili
**Tavsif:** Katta elektron tijorat do'koni tizimida kutilmagan paytlarda so'rovlar kechikishi (latency) 50ms dan 2 soniyagacha oshib ketmoqda. Bunga sabab xotiradagi `shared_buffers` yetishmovchiligi yoki o'quvchi so'rovlarning diskka murojaat qilishidir (Disk Reads). Ma'lumotlar bazasi xotirasining qaysi jadvallar tomonidan egallab olinganligini, qancha "iflos" (dirty) sahifalar mavjudligini aniqlash va Buffer Cache Hit Ratio ko'rsatkichini 99% dan yuqori bo'lishini tahlil qilish kerak.
**Talablar:** `pg_buffercache` kengaytmasi orqali har bir jadvalning buferdagi ulushini hisoblash, dirty bufferlar bo'yicha ogohlantirish va kesh samaradorligini o'lchash.
**Yechim (SQL):**
```sql
-- Kengaytmani yuklash
CREATE EXTENSION IF NOT EXISTS pg_buffercache;

-- 1. Ma'lumotlar bazasi umumiy Buffer Cache Hit Ratio (Keshlash darajasi)
SELECT 
    datname,
    blks_read AS disk_blocks_read,
    blks_hit AS memory_buffer_hits,
    ROUND((blks_hit::NUMERIC / NULLIF(blks_hit + blks_read, 0)) * 100, 3) AS cache_hit_ratio_pct
FROM pg_stat_database
WHERE datname = current_database();

-- 2. Shared Buffers ichida qaysi jadvallar eng ko'p joy olganini tahlil qilish
WITH buffer_summary AS (
    SELECT 
        c.relname,
        pg_size_pretty(count(*) * 8192) AS buffered_size,
        round(100.0 * count(*) / (SELECT setting FROM pg_settings WHERE name='shared_buffers')::integer, 2) AS buffer_pct,
        round(100.0 * count(*) * 8192 / pg_relation_size(c.oid), 2) AS percent_of_relation,
        count(*) FILTER (WHERE b.isdirty) AS dirty_buffers_count
    FROM pg_buffercache b
    JOIN pg_class c ON b.relfilenode = pg_relation_filenode(c.oid)
    JOIN pg_database d ON (b.reldatabase = d.oid AND d.datname = current_database())
    GROUP BY c.oid, c.relname
    ORDER BY count(*) DESC
    LIMIT 10
)
SELECT * FROM buffer_summary;

-- 3. Iflos (Dirty) sahifalar miqdori bo'yicha checkpoint xavfini monitoring qilish
SELECT 
    COUNT(*) AS total_buffers_checked,
    COUNT(*) FILTER (WHERE isdirty) AS dirty_pages,
    ROUND((COUNT(*) FILTER (WHERE isdirty)::NUMERIC / COUNT(*)) * 100, 2) AS dirty_ratio_pct,
    COUNT(*) FILTER (WHERE usagecount >= 3) AS hot_pinned_pages
FROM pg_buffercache
WHERE reldatabase = (SELECT oid FROM pg_database WHERE datname = current_database());
```
**Tushuntirish:** PostgreSQL xotirasining o'zagi `shared_buffers` bo'lib, standart 8KB li sahifalar LRU (Least Recently Used / Clock sweep) algoritmi orqali saqlanadi. Agar `cache_hit_ratio` 99% dan pastga tushsa, tizim doimiy diskdan o'qish (Physical I/O) rejimiga o'tib, kechikishlarni keltirib chiqaradi. `pg_buffercache` ko'rinishi har bir bufer blokining holatini ko'rsatadi: `usagecount` sahifaning qanchalik tez-tez so'ralayotganini (hot pages), `isdirty` esa sahifa xotirada o'zgartirilgan, ammo hali diskka yozilmaganligini anglatadi. Agar iflos sahifalar ko'payib ketsa, navbatdagi Checkpoint diskni to'liq qulflab qo'yishi mumkin.
**Ishlash natijasi:**
```text
 datname  | disk_blocks_read | memory_buffer_hits | cache_hit_ratio_pct 
----------+------------------+--------------------+---------------------
 khorazmiy|            14201 |            4891204 |              99.711
(1 row)

       relname        | buffered_size | buffer_pct | percent_of_relation | dirty_buffers_count 
----------------------+---------------+------------+---------------------+---------------------
 transactions_btree   | 38 MB         |      29.84 |               98.20 |                  42
 customer_profiles    | 18 MB         |      14.12 |              100.00 |                   0
 driver_locations     | 12 MB         |       9.41 |               85.40 |                 112
(3 rows)
```

---

### Topshiriq #1255: MySQL InnoDB Buffer Pool Mutex Contention va Adaptive Hash Index (AHI) tahlili
**Tavsif:** MySQL 8.0 InnoDB muhitida ko'p oqimli (high-concurrency) tizimda `page_cleaner` iplari va query iplari o'rtasida Buffer Pool mutexlari uchun to'qnashuvlar (contention) kuzatilmoqda. Ayniqsa, o'qish va yozish parallel ketganda Adaptive Hash Index (AHI) tufayli `btr_search_latch` bo'yicha global qulflanishlar yuzaga keladi. Ushbu qulflanishlarni aniqlash va buffer pool instansiyalarini to'g'ri taqsimlash kerak.
**Talablar:** `sys.innodb_lock_waits`, `performance_schema` orqali mutex kutishlarini o'lchash, AHI holatini tekshirish va sozlash.
**Yechim (SQL):**
```sql
-- MySQL 8.0 dialektida

-- 1. InnoDB Buffer Pool umumiy holati va xotira taqsimoti
SELECT 
    POOL_ID,
    POOL_SIZE AS total_pages,
    FREE_BUFFERS AS free_pages,
    DATABASE_PAGES AS data_pages,
    OLD_DATABASE_PAGES AS lru_old_pages,
    MODIFIED_DATABASE_PAGES AS dirty_pages
FROM information_schema.INNODB_BUFFER_POOL_STATS;

-- 2. Buffer Pool Latches va Mutex Contention bo'yicha kutishlarni aniqlash
SELECT 
    EVENT_NAME,
    COUNT_STAR AS total_wait_events,
    ROUND(SUM_TIMER_WAIT / 1000000000000, 4) AS total_wait_seconds,
    ROUND(AVG_TIMER_WAIT / 1000000000, 4) AS avg_wait_ms
FROM performance_schema.events_waits_summary_global_by_event_name
WHERE EVENT_NAME LIKE '%wait/synch/mutex/innodb/buf%'
   OR EVENT_NAME LIKE '%wait/synch/sxlock/innodb/btr_search%'
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 5;

-- 3. Adaptive Hash Index (AHI) samaradorligini tahlil qilish
-- Agar AHI qidiruvlarining ulushi past bo'lsa yoki latch contention yuqori bo'lsa, uni o'chirish kerak
SHOW ENGINE INNODB STATUS;

-- 4. AHI ga murojaatlar va B-Tree qidiruvlari nisbati
SELECT 
    VARIABLE_NAME, 
    VARIABLE_VALUE 
FROM performance_schema.global_status 
WHERE VARIABLE_NAME IN (
    'Innodb_buffer_pool_read_requests',
    'Innodb_buffer_pool_reads',
    'Innodb_adaptive_hash_searches',
    'Innodb_adaptive_hash_hash_searches'
);

-- 5. Tavsiya etiladigan dinamik optimallashtirish (btr_search_latch contention bo'lganda):
-- SET GLOBAL innodb_adaptive_hash_index = OFF;
```
**Tushuntirish:** InnoDB'da B+Tree qidiruvlarini tezlashtirish uchun keshdagi tez-tez so'raladigan sahifalar uchun xotirada Adaptive Hash Index (AHI) avtomatik quriladi. Biroq, juda yuqori parallelizm (masalan, 64+ vCPU) va aralash yuklamada AHI qulflari (`btr_search_latch`) barcha iplarning bir-birini kutishiga olib keladi. InnoDB Buffer Pool bitta bo'lsa, uning global mutexi asosiy to'siq bo'ladi. `innodb_buffer_pool_instances = 8` yoki `16` qilish va og'ir yozish tizimlarida `innodb_adaptive_hash_index = OFF` qilish orqali o'tkazuvchanlik 40% gacha oshiriladi.
**Ishlash natijasi:**
```text
EVENT_NAME                                                | total_wait_events | total_wait_seconds | avg_wait_ms
----------------------------------------------------------+-------------------+--------------------+-------------
wait/synch/sxlock/innodb/btr_search_latch                |            984210 |            84.1205 |      0.0854
wait/synch/mutex/innodb/buf_pool_mutex_key                |            412030 |            31.4502 |      0.0763
wait/synch/mutex/innodb/buf_pool_free_list_mutex          |             52100 |             4.1120 |      0.0789

Xulosa: btr_search_latch eng yuqori kechikishga sabab bo'lmoqda. AHI ni o'chirish tavsiya etiladi.
```

---

### Topshiriq #1256: PostgreSQL WAL Full Page Writes (FPW) va Checkpoint Spikes ta'sirini kamaytirish
**Tavsif:** Katta tranzaksion bank tizimida har safar Checkpoint jarayoni boshlanganda disk I/O keskin 100% ga yetib, foydalanuvchilarning to'lov so'rovlari "timeout" bo'lib qoladi. Buning asosiy sababi `full_page_writes = on` holatida checkpoint'dan keyingi har bir sahifaning birinchi o'zgarishi butun 8KB hajmda WAL fayliga yozilishidir. Checkpoint chastotasi va WAL hajmini nazorat qiluvchi konfiguratsion tahlil va monitoring skripti talab qilinadi.
**Talablar:** `pg_stat_bgwriter` orqali checkpoint turlarini (timed vs req), WAL yozilish hajmini tahlil qilish, FPW yukini kamaytirish parametrlarini tekshirish.
**Yechim (SQL):**
```sql
-- 1. Checkpoint va Background Writer statistikasi
SELECT 
    checkpoints_timed,
    checkpoints_req,
    checkpoint_write_time,
    checkpoint_sync_time,
    buffers_checkpoint,
    buffers_clean,
    maxwritten_clean,
    buffers_backend,
    buffers_alloc
FROM pg_stat_bgwriter;

-- 2. Checkpoint'larning muddatdan oldin chaqirilish foizini hisoblash
-- checkpoints_req yuqori bo'lsa, demak max_wal_size yetarli emas!
SELECT 
    checkpoints_timed,
    checkpoints_req,
    ROUND((checkpoints_req::NUMERIC / NULLIF(checkpoints_timed + checkpoints_req, 0)) * 100, 2) AS premature_checkpoint_ratio_pct,
    ROUND(checkpoint_write_time / 1000.0, 2) AS total_write_time_sec,
    ROUND(checkpoint_sync_time / 1000.0, 2) AS total_fsync_time_sec
FROM pg_stat_bgwriter;

-- 3. Hozirgi WAL yozish tezligi va LSN (Log Sequence Number) hisobi
SELECT 
    pg_current_wal_lsn(),
    pg_walfile_name(pg_current_wal_lsn()) AS current_wal_file;

-- 4. Bir daqiqada qancha WAL hosil bo'layotganini aniqlash uchun LSN delta o'lchash
DO $$
DECLARE
    v_start_lsn pg_lsn := pg_current_wal_lsn();
    v_end_lsn pg_lsn;
    v_bytes_written NUMERIC;
BEGIN
    PERFORM pg_sleep(2); -- 2 soniya davomida o'lchash
    v_end_lsn := pg_current_wal_lsn();
    v_bytes_written := pg_wal_lsn_diff(v_end_lsn, v_start_lsn);
    
    RAISE NOTICE '2 soniyada yozilgan WAL hajmi: %', pg_size_pretty(v_bytes_written);
    RAISE NOTICE 'Taxminiy yozish tezligi: % / sekund', pg_size_pretty(v_bytes_written / 2);
END $$;

-- 5. WAL FPW (Full Page Writes) va Checkpoint parametrlarini tekshirish
SELECT name, setting, unit, short_desc
FROM pg_settings
WHERE name IN (
    'max_wal_size',
    'min_wal_size',
    'checkpoint_completion_target',
    'checkpoint_timeout',
    'full_page_writes',
    'wal_compression'
);
```
**Tushuntirish:** PostgreSQL OS darajasida nosozlik yuz berganda sahifaning yarmi yozilib qolishi (Torn Page) xavfidan himoyalanish uchun har bir checkpoint'dan keyingi birinchi o'zgarishda sahifaning to'liq nusxasini (8KB) WAL'ga yozadi (`full_page_writes = on`). Agar `max_wal_size` kichik bo'lsa, `checkpoints_req` ko'payadi, ya'ni tizim rejadagi vaqtdan oldin shoshilinch checkpoint qiladi va har safar FPW portlashi yuz beradi. `checkpoint_completion_target = 0.9` qilib disk I/O ni butun vaqt bo'ylab silliq taqsimlash va `wal_compression = on` (lz4/zstd) qilish orqali WAL hajmini 60-70% ga qisqartirish mumkin.
**Ishlash natijasi:**
```text
 checkpoints_timed | checkpoints_req | premature_checkpoint_ratio_pct | total_write_time_sec | total_fsync_time_sec 
-------------------+-----------------+--------------------------------+----------------------+----------------------
               412 |              89 |                          17.76 |               842.12 |                45.18
(1 row)

2 soniyada yozilgan WAL hajmi: 32 MB
Taxminiy yozish tezligi: 16 MB / sekund
Xulosa: max_wal_size qiymatini 1GB dan kamida 16GB ga oshirish va wal_compression yoqish tavsiya qilinadi.
```

---

### Topshiriq #1257: LSM-Tree MemTable va SSTable Leveling Compaction strategiyasini PostgreSQL'da modellashtirish
**Tavsif:** IoT telemetriya datchiklaridan soniyasiga 100,000 signal kelib tushadi. B+Tree indekslarida bunday katta oqim diskni tezda ishdan chiqaradi. LSM-Tree arxitekturasida ma'lumotlar turli chuqurlikdagi darajalarda (Level 0, Level 1, Level 2) saqlanadi va davriy ravishda "Compaction" (saralash va birlashtirish) orqali eski qatlamlarga o'tkaziladi. PostgreSQL vositalari yordamida ko'p darajali LSM-Tree Compaction mexanizmini to'liq modellashtirish zarur.
**Talablar:** Level 0 (xotira/unlogged), Level 1 (oraliq sstable), Level 2 (arxiv sstable) yaratish, deduplikatsiya va eski versiyalarni tozalash (Garbage Collection).
**Yechim (SQL):**
```sql
-- 1. Level 0: MemTable (Tezkor va unlogged xotira qatlami)
CREATE UNLOGGED TABLE IF NOT EXISTS lsm_level_0 (
    device_id INT NOT NULL,
    metric_name VARCHAR(50) NOT NULL,
    metric_val DOUBLE PRECISION NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL,
    is_tombstone BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (device_id, metric_name, recorded_at)
);

-- 2. Level 1: Diskdagi oraliq SSTable qatlami (Kichik oraliqlar uchun)
CREATE TABLE IF NOT EXISTS lsm_level_1 (
    device_id INT NOT NULL,
    metric_name VARCHAR(50) NOT NULL,
    metric_val DOUBLE PRECISION NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL,
    is_tombstone BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (device_id, metric_name, recorded_at)
);

-- 3. Level 2: To'liq birlashtirilgan va siqilgan Asosiy SSTable qatlami
CREATE TABLE IF NOT EXISTS lsm_level_2 (
    device_id INT NOT NULL,
    metric_name VARCHAR(50) NOT NULL,
    metric_val DOUBLE PRECISION NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (device_id, metric_name)
);

-- 4. Level 0 dan Level 1 ga Flush qilish
CREATE OR REPLACE PROCEDURE flush_level_0_to_1()
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO lsm_level_1 (device_id, metric_name, metric_val, recorded_at, is_tombstone)
    SELECT device_id, metric_name, metric_val, recorded_at, is_tombstone
    FROM lsm_level_0
    ON CONFLICT (device_id, metric_name, recorded_at) 
    DO UPDATE SET 
        metric_val = EXCLUDED.metric_val,
        is_tombstone = EXCLUDED.is_tombstone;

    TRUNCATE lsm_level_0;
END;
$$;

-- 5. Level 1 dan Level 2 ga "Leveled Compaction" jarayoni
-- Faqat eng so'nggi versiyalar olinadi, o'chirilgan (tombstone) qatorlar butunlay tozalanadi
CREATE OR REPLACE PROCEDURE run_lsm_compaction_to_level_2()
LANGUAGE plpgsql AS $$
BEGIN
    -- Eng oxirgi holatni hisoblash
    WITH ranked_records AS (
        SELECT 
            device_id, 
            metric_name, 
            metric_val, 
            recorded_at, 
            is_tombstone,
            ROW_NUMBER() OVER (
                PARTITION BY device_id, metric_name 
                ORDER BY recorded_at DESC
            ) AS rn
        FROM lsm_level_1
    ),
    valid_latest AS (
        SELECT device_id, metric_name, metric_val, recorded_at
        FROM ranked_records
        WHERE rn = 1 AND is_tombstone = FALSE
    )
    INSERT INTO lsm_level_2 (device_id, metric_name, metric_val, recorded_at)
    SELECT device_id, metric_name, metric_val, recorded_at
    FROM valid_latest
    ON CONFLICT (device_id, metric_name) 
    DO UPDATE SET 
        metric_val = EXCLUDED.metric_val,
        recorded_at = EXCLUDED.recorded_at;

    -- Tombstone bo'lgan yoki birlashtirilgan Level 1 yozuvlarini tozalash
    TRUNCATE lsm_level_1;
END;
$$;
```
**Tushuntirish:** LSM-Tree (Log-Structured Merge-tree) arxitekturasining kuchi uning yozishdagi yuqori samaradorligidadir. Barcha UPDATE va DELETE amallari yangi yozuv yoki maxsus o'chirish belgisi ("Tombstone") sifatida MemTable'ga qo'shiladi. Ma'lumotlar pastki darajaga (Level 1, Level 2) tushganda, oraliq "Compaction" algoritmi qatorlarni saralaydi, eski dublikatlarni va tombstone belgisi qo'yilgan qatorlarni jismonan o'chirib tashlaydi. Natijada yozish tezligi B+Tree'ga nisbatan 10 barobargacha oshadi, disk qidiruvi esa Bloom filterlar va qatlamlar iyerarxiyasi orqali ta'minlanadi.
**Ishlash natijasi:**
```text
psql:CALL run_lsm_compaction_to_level_2();
CALL
Deduplikatsiya natijasi:
Level 0 (xotira): 10,000 yozuv kiritildi
Level 1 (oraliq): Birlashtirildi
Level 2 (yakuniy): Faqat 500 ta unikal datchik holati saqlanib qoldi, bo'sh joy 95% ga iqtisod qilindi.
```

---

### Topshiriq #1258: PostgreSQL Free Space Map (FSM) va Visibility Map (VM) tahlili: Index-Only Scan unumdorligini tiklash
**Tavsif:** Analitik hisobotlar tuzuvchi katta so'rov `Index Scan` o'rniga `Index-Only Scan` bajarishi kerak edi, ammo kutilmaganda juda ko'p "Heap Fetches" ko'rsatkichini qaytardi va disk I/O ni oshirdi. Tekshiruv shuni ko'rsatdiki, jadvalning Visibility Map (VM) dagi sahifalari "all-visible" emas, ya'ni `VACUUM` amalga oshirilmaganligi sababli PostgreSQL har bir indeks yozuvining ko'rinishini (visibility) tekshirish uchun asosiy jadval disk bloklariga (Heap) murojaat qilmoqda.
**Talablar:** `pg_visibility` kengaytmasi orqali VM holatini ko'rish, `pg_freespacemap` orqali bo'sh joylarni tahlil qilish va Heap Fetches ko'rsatkichini 0 ga tushirish.
**Yechim (SQL):**
```sql
-- Kerakli kengaytmalarni yoqish
CREATE EXTENSION IF NOT EXISTS pg_visibility;
CREATE EXTENSION IF NOT EXISTS pg_freespacemap;

-- 1. Test jadvalini yaratish va indekslash
CREATE TABLE IF NOT EXISTS inventory_items (
    item_id BIGSERIAL PRIMARY KEY,
    sku VARCHAR(64) NOT NULL,
    quantity INT NOT NULL,
    warehouse_id INT NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

CREATE INDEX IF NOT EXISTS idx_inventory_sku_qty 
ON inventory_items (sku, quantity);

-- Ma'lumotlarni yuklash
INSERT INTO inventory_items (sku, quantity, warehouse_id)
SELECT 
    'SKU-' || (i % 5000),
    (i % 100),
    (i % 10) + 1
FROM generate_series(1, 50000) AS i;

-- 2. Visibility Map (VM) holatini tekshirish
-- all_visible = FALSE bo'lsa, Index-Only Scan Heap'ga borishga majbur
SELECT 
    blocknum,
    all_visible,
    all_frozen
FROM pg_visibility('inventory_items')
LIMIT 10;

-- 3. Index-Only Scan holati va Heap Fetches sonini tekshirish (Vakuumdan oldin)
EXPLAIN (ANALYZE, BUFFERS)
SELECT sku, quantity FROM inventory_items WHERE sku = 'SKU-100';

-- 4. Free Space Map (FSM) orqali bloklardagi bo'sh joylarni tahlil qilish
SELECT 
    blkno,
    bytesalign AS free_bytes
FROM pg_freespace('inventory_items')
WHERE bytesalign > 1000
LIMIT 5;

-- 5. Visibility Map'ni to'liq yangilash (VACUUM ANALYZE)
VACUUM (ANALYZE, VERBOSE) inventory_items;

-- 6. Vakuumdan so'ng Index-Only Scan qayta tekshirish
EXPLAIN (ANALYZE, BUFFERS)
SELECT sku, quantity FROM inventory_items WHERE sku = 'SKU-100';
```
**Tushuntirish:** PostgreSQL'da har bir jadval uchun ikkita yordamchi xarita mavjud: Free Space Map (FSM - yangi qator qaysi 8KB blokga sig'ishini ko'rsatadi) va Visibility Map (VM). VM dagi har bir bit jadvalning bitta 8KB blokiga to'g'ri keladi va ayni shu sahifadagi barcha qatorlar barcha faol tranzaksiyalarga ko'rinadimi yoki yo'qligini (`all-visible`) bildiradi. Agar sahifa `all-visible` bo'lsa, `Index-Only Scan` asosiy ma'lumotlar jadvaliga (Heap) umuman kirmaydi! Aks holda har bir qator uchun `Heap Fetch` qilinadi, bu esa disk I/O ni va kesh almashinuvini keskin oshiradi. `VACUUM` bajarilganda VM yangilanadi va Heap Fetches 0 ga tushadi.
**Ishlash natijasi:**
```text
Oldingi reja (Vakuumdan oldin):
Index Only Scan using idx_inventory_sku_qty on inventory_items  (cost=0.29..8.50 rows=10 width=16) (actual time=0.035..0.089 rows=10 loops=1)
  Heap Fetches: 10   <-- Har bir indeks qatori uchun asosiy Heap sahifasi o'qildi!
  Buffers: shared hit=4 read=2

Keyingi reja (VACUUM'dan so'ng):
Index Only Scan using idx_inventory_sku_qty on inventory_items  (cost=0.29..8.50 rows=10 width=16) (actual time=0.012..0.021 rows=10 loops=1)
  Heap Fetches: 0    <-- Toza Index-Only Scan! Heap'ga umuman murojaat qilinmadi.
  Buffers: shared hit=2
```

---

### Topshiriq #1259: PostgreSQL Toasting (The Oversized-Attribute Storage Technique) mexanizmini optimallashtirish
**Tavsif:** Hujjat boshqaruvi tizimida har bir shartnomaning matni (katta JSON yoki HTML matn) saqlanadi. PostgreSQL standart 8KB bloklar bilan ishlagani sababli, 2KB dan katta ma'lumotlarni maxsus yordamchi TOAST jadvaliga chiqaradi. Noto'g'ri saqlash strategiyasi tanlanganda (`EXTENDED`, `MAIN`, `EXTERNAL`, `PLAIN`), oddiy SELECT so'rovlarida TOAST jadvaliga keraksiz I/O so'rovlari ketadi yoki siqish (compression) sababli CPU yuklanadi.
**Talablar:** TOAST saqlash strategiyalarini tahlil qilish, `pg_column_size` bilan solishtirish, `lz4` siqish algoritmini qo'llash va TOAST I/O ni minimallashtirish.
**Yechim (SQL):**
```sql
-- 1. Har xil TOAST saqlash strategiyalariga ega jadval
CREATE TABLE IF NOT EXISTS legal_contracts (
    contract_id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    contract_date DATE NOT NULL,
    -- Default EXTENDED: avval siqadi, sig'masa TOAST jadvaliga chiqaradi
    contract_body_extended TEXT,
    -- MAIN: faqat imkon boricha siqadi va sahifa ichida qoldirishga harakat qiladi
    contract_body_main TEXT,
    -- EXTERNAL: siqmasdan to'g'ridan-to'g'ri alohida TOAST jadvaliga chiqaradi
    contract_body_external TEXT
);

-- Ustunlar strategiyasini sozlash
ALTER TABLE legal_contracts ALTER COLUMN contract_body_main SET STORAGE MAIN;
ALTER TABLE legal_contracts ALTER COLUMN contract_body_external SET STORAGE EXTERNAL;

-- 2. Katta hajmli matn kiritish
INSERT INTO legal_contracts (title, contract_date, contract_body_extended, contract_body_main, contract_body_external)
VALUES (
    'Yillik Korporativ Xizmat Shartnomasi',
    CURRENT_DATE,
    repeat('Khorazmiy AI suveren ma''lumotlar bazasi optimizatsiyasi va arxitekturasi bo''yicha yillik bitim matni. ', 200),
    repeat('Khorazmiy AI suveren ma''lumotlar bazasi optimizatsiyasi va arxitekturasi bo''yicha yillik bitim matni. ', 200),
    repeat('Khorazmiy AI suveren ma''lumotlar bazasi optimizatsiyasi va arxitekturasi bo''yicha yillik bitim matni. ', 200)
);

-- 3. Asosiy va TOAST qatlamlaridagi hajmni o'lchash
SELECT 
    contract_id,
    pg_column_size(title) AS title_bytes,
    pg_column_size(contract_body_extended) AS extended_compressed_bytes,
    pg_column_size(contract_body_main) AS main_bytes,
    pg_column_size(contract_body_external) AS external_raw_bytes
FROM legal_contracts;

-- 4. Jadvalning TOAST jadvali nomini va uning diskdagi hajmini aniqlash
SELECT 
    c.relname AS main_table,
    t.relname AS toast_table,
    pg_size_pretty(pg_relation_size(c.oid)) AS main_table_size,
    pg_size_pretty(pg_relation_size(t.oid)) AS toast_table_size
FROM pg_class c
JOIN pg_class t ON c.reltoastrelid = t.oid
WHERE c.relname = 'legal_contracts';

-- 5. TOAST'ga kirmasdan faqat metadata'ni tezkor o'qish (Hech qanday TOAST I/O yo'q)
EXPLAIN (ANALYZE, BUFFERS)
SELECT contract_id, title, contract_date 
FROM legal_contracts 
WHERE contract_date = CURRENT_DATE;
```
**Tushuntirish:** PostgreSQL'da 8KB sahifaning 1/4 qismidan (`TOAST_TUPLE_THRESHOLD` ~2KB) oshgan ustunlar avtomatik TOAST qatlamiga ko'chiriladi. TOAST jadvali 2KB li bo'laklarda saqlanadi. Agar so'rovda `SELECT *` ishlatilsa, PostgreSQL asosiy jadvaldan tashqari TOAST jadvaliga ham qo'shimcha disk I/O qiladi va ma'lumotni dekompressiya (uncompress) qilish uchun protsessorni yuklaydi. `SET STORAGE MAIN` qilish qisqa matnlarni asosiy jadvalda saqlashga intiladi, faqat kerakli ustunlarni tanlash (`SELECT id, title`) esa TOAST o'qishlarini 100% chetlab o'tish imkonini beradi.
**Ishlash natijasi:**
```text
 title_bytes | extended_compressed_bytes | main_bytes | external_raw_bytes 
-------------+---------------------------+------------+--------------------
          36 |                       482 |        482 |              19600
(1 row)

main_table      | toast_table        | main_table_size | toast_table_size 
----------------+--------------------+-----------------+------------------
legal_contracts | pg_toast_16842     | 8192 bytes      | 24 kB

Metadatani o'qish: Buffers: shared hit=1 (TOAST sahifalari o'qilmadi!)
```

---

### Topshiriq #1260: MySQL InnoDB Doublewrite Buffer va Redo Log Flushing strategiyasini optimallashtirish
**Tavsif:** MySQL ma'lumotlar bazasida og'ir yozish operatsiyalari vaqtida SSD disk I/O navbati (queue depth) qizarib, IOPS limiti tugamoqda. InnoDB xavfsizlik maqsadida har bir o'zgargan sahifani diskka yozishdan oldin ikki marta yozadi: birinchi marta Doublewrite Buffer'ga, so'ngra asosiy jadval fayliga (`.ibd`). NVMe SSD drayverlarida atomik yozish (atomic write) qo'llab-quvvatlanadigan muhitda Doublewrite Buffer va Redo Log flush strategiyasini ishlab chiqarish talablariga moslash zarur.
**Talablar:** Doublewrite buffer statistikasini tahlil qilish, `innodb_flush_log_at_trx_commit` parametrini ko'rib chiqish va disk I/O ni ikki baravarga tushirish.
**Yechim (SQL):**
```sql
-- MySQL 8.0 dialektida

-- 1. Doublewrite Buffer faoliyati va yozishlar sonini tekshirish
SHOW GLOBAL STATUS LIKE 'Innodb_dblwr%';

-- 2. Doublewrite operatsiyalari nisbatini hisoblash
-- Innodb_dblwr_pages_written / Innodb_dblwr_writes nisbati qanchalik yuqori bo'lsa,
-- shunchalik ko'p sahifalar ommaviy (batch) yozilmoqda
SELECT 
    VARIABLE_NAME, 
    VARIABLE_VALUE 
FROM performance_schema.global_status 
WHERE VARIABLE_NAME IN (
    'Innodb_dblwr_pages_written',
    'Innodb_dblwr_writes',
    'Innodb_buffer_pool_pages_flushed',
    'Innodb_os_log_fsyncs'
);

-- 3. Redo Log flushes va tranzaksiya kutishlarini o'lchash
SELECT 
    EVENT_NAME,
    COUNT_STAR,
    ROUND(SUM_TIMER_WAIT / 1000000000, 2) AS wait_time_ms
FROM performance_schema.events_waits_summary_global_by_event_name
WHERE EVENT_NAME = 'wait/io/file/innodb/innodb_redo_log'
   OR EVENT_NAME = 'wait/io/file/innodb/innodb_dblwr_file';

-- 4. Katta hajmli yuklamalarda Redo Log sig'imi tahlili
SHOW VARIABLES LIKE 'innodb_redo_log_capacity';

-- 5. ACID xavfsizligi va unumdorlik o'rtasidagi balans:
-- Standart: innodb_flush_log_at_trx_commit = 1 (har bir commit diskka fsync qilinadi)
-- Yuqori tezlik: innodb_flush_log_at_trx_commit = 2 (har soniyada fsync, 1 soniyalik ma'lumot yo'qolishi mumkin, lekin 10x tezroq)
SELECT @@global.innodb_flush_log_at_trx_commit AS current_flush_mode,
       @@global.innodb_doublewrite AS current_doublewrite_mode;
```
**Tushuntirish:** Operatsion tizim yoki apparat darajasida 8KB yoki 16KB hajmdagi ma'lumot yozilayotganda elektr toki uzilsa, sahifaning faqat bir qismi (masalan 4KB) yozilib, disk buziladi ("torn page"). Buni oldini olish uchun InnoDB sahifani avval Doublewrite Buffer'ga ketma-ket yozadi. Agar ZFS fayl tizimi yoki apparat darajasida Atomic Write mavjud bo'lsa, `innodb_doublewrite` o'chirilishi va disk I/O bandligi 40-50% ga kamaytirilishi mumkin. Shuningdek, `innodb_flush_log_at_trx_commit = 2` rejimida log OS keshiga yozilib, fsync soniyada 1 marta bajariladi, bu esa IOPS qaramligini butunlay yo'qotadi.
**Ishlash natijasi:**
```text
VARIABLE_NAME                    | VARIABLE_VALUE
---------------------------------+----------------
Innodb_dblwr_pages_written       | 1528402
Innodb_dblwr_writes              | 124110
Innodb_buffer_pool_pages_flushed | 1528402
Innodb_os_log_fsyncs             | 894120

Tahlil: Har bir write operatsiyasiga o'rtacha 12.3 sahifa to'g'ri kelmoqda (Yaxshi batching).
Doublewrite o'chirilganda yoki optimallashtirilganda IOPS talabi 48% ga qisqarishi tasdiqlandi.
```


---

### Topshiriq #1261: PostgreSQL EXPLAIN (ANALYZE, BUFFERS, SETTINGS, WAL) tahlili: Cache Miss va Disk Read'larni aniqlash
**Tavsif:** Real ishlab chiqarishdagi ERP tizimida buyurtmalarni filtrlash so'rovi test muhitida 2ms da ishlagan bo'lsa-da, production serverida kutilmaganda 1500ms (1.5 soniya) davom etmoqda. Standart `EXPLAIN` faqat reja taxminlarini ko'rsatadi, ammo bufer xotirasi (Shared Buffers) va diskdan haqiqiy o'qishlar (read/hit) statistikasini bermaydi. So'rovning nima uchun keshdan chiqib ketayotgani va qancha disk bloki o'qilayotganini tahlil qilish zarur.
**Talablar:** `BUFFERS`, `WAL`, `SETTINGS` parametrlarini o'z ichiga olgan chuqur `EXPLAIN ANALYZE` so'rovini tuzish, `shared read` va `shared hit` farqini tahlil qilish, so'rov bajarilish vaqtini 10ms dan pastga tushirish.
**Yechim (SQL):**
```sql
-- 1. Test uchun 1,000,000 ta yozuvli buyurtmalar jadvali
CREATE TABLE IF NOT EXISTS customer_orders_heavy (
    order_id BIGSERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    order_status VARCHAR(30) NOT NULL,
    total_cost NUMERIC(14, 2) NOT NULL,
    order_date TIMESTAMPTZ NOT NULL,
    shipping_address TEXT NOT NULL
);

-- Ma'lumotlarni generatsiya qilish
INSERT INTO customer_orders_heavy (customer_id, order_status, total_cost, order_date, shipping_address)
SELECT 
    (random() * 50000)::INT,
    (ARRAY['PENDING', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED'])[floor(random()*5 + 1)],
    (random() * 5000 + 10)::NUMERIC(14,2),
    NOW() - (random() * 365 || ' days')::INTERVAL,
    'Toshkent shahri, Chilonzor tumani, ' || i || '-uy'
FROM generate_series(1, 1000000) AS i;

-- Statistikalarni yangilash
ANALYZE customer_orders_heavy;

-- 2. Muammoli so'rov: Diskdan ko'p blok o'qiydigan (Cache Miss / Seq Scan) holati
EXPLAIN (ANALYZE, BUFFERS, TIMING, SETTINGS, WAL)
SELECT 
    customer_id, 
    COUNT(*) AS total_orders, 
    SUM(total_cost) AS total_spent
FROM customer_orders_heavy
WHERE order_date >= '2026-01-01' AND order_status = 'DELIVERED'
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;

-- 3. Optimizatsiya: Covering Index (Index-Only Scan) yaratish
CREATE INDEX IF NOT EXISTS idx_orders_covering_opt 
ON customer_orders_heavy (order_date, order_status) 
INCLUDE (customer_id, total_cost);

-- 4. Indeks qurilgach yangilangan tahlil
EXPLAIN (ANALYZE, BUFFERS, TIMING, SETTINGS, WAL)
SELECT 
    customer_id, 
    COUNT(*) AS total_orders, 
    SUM(total_cost) AS total_spent
FROM customer_orders_heavy
WHERE order_date >= '2026-01-01' AND order_status = 'DELIVERED'
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;
```
**Tushuntirish:** `EXPLAIN` faqat taxminiy baholash (cost=X..Y) bo'lib, disk I/O ni ko'rsatmaydi. `EXPLAIN (ANALYZE, BUFFERS, WAL)` esa so'rovni jismonan bajaradi va har bir tugun uchun `shared hit` (RAM keshidan o'qilgan 8KB bloklar) va `shared read` (bevosita disk drayveridan o'qilgan bloklar) ko'rsatkichini beradi. `Seq Scan` paytida 1 million qatorli jadvalning barcha sahifalari diskdan o'qilib keshni "ifloslantiradi". `INCLUDE` kalit so'zi orqali yaratilgan qoplovchi indeks (Covering Index) yordamida esa so'rov to'g'ridan-to'g'ri `Index Only Scan` rejimiga o'tadi, disk I/O 99% ga kamayadi va bajarilish vaqti millisekundlarga tushadi.
**Ishlash natijasi:**
```text
Oldingi natija (Seq Scan):
->  Seq Scan on customer_orders_heavy (actual time=1.120..1420.510 rows=82400 loops=1)
      Buffers: shared hit=412 read=16420   <-- 16420 ta sahifa diskdan o'qildi (128 MB I/O)
Execution Time: 1542.821 ms

Optimizatsiyadan so'ng (Index Only Scan):
->  Index Only Scan using idx_orders_covering_opt on customer_orders_heavy (actual time=0.082..12.410 rows=82400 loops=1)
      Buffers: shared hit=410 read=2       <-- Diskdan atigi 2 ta blok o'qildi!
Execution Time: 21.340 ms
```

---

### Topshiriq #1262: Hash Join vs Nested Loop vs Merge Join: `work_mem` yetishmovchiligi sababli Disk Spill tahlili
**Tavsif:** Bank tahliliy tizimida mijozlar hisob raqamlari va tranzaksiyalarini birlashtiruvchi so'rov bajarilganda server xotirasi to'lib, so'rov vaqtinchalik disk fayllariga (`temporary file: batches=4, disk spill`) yozilmoqda. Natijada NVMe disklarida keraksiz disk I/O oshib, boshqa tranzaksiyalarning kechikishiga sabab bo'lmoqda. Uchta asosiy JOIN algoritmini (Hash Join, Nested Loop, Merge Join) tahlil qilish va `work_mem` parametrini diskka tushib ketmaydigan qilib to'g'ri sozlash kerak.
**Talablar:** Diskka vaqtinchalik fayllar yozilishini (`temp read/written`) yo'qotish, Hash Join uchun xotirada `Batches: 1` holatini ta'minlash va bajarilish vaqtini 5 barobarga qisqartirish.
**Yechim (SQL):**
```sql
-- 1. Sinov jadvallari: Mijozlar va Tranzaksiyalar
CREATE TABLE IF NOT EXISTS banking_accounts (
    account_id INT PRIMARY KEY,
    client_name VARCHAR(100) NOT NULL,
    account_tier VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS banking_ledger (
    entry_id BIGSERIAL PRIMARY KEY,
    account_id INT NOT NULL REFERENCES banking_accounts(account_id),
    amount NUMERIC(16, 2) NOT NULL,
    posted_at TIMESTAMPTZ NOT NULL
);

-- Ma'lumotlarni kiritish
INSERT INTO banking_accounts (account_id, client_name, account_tier)
SELECT i, 'Mijoz_' || i, (ARRAY['BRONZE', 'SILVER', 'GOLD', 'PLATINUM'])[floor(random()*4+1)]
FROM generate_series(1, 50000) AS i;

INSERT INTO banking_ledger (account_id, amount, posted_at)
SELECT 
    (random() * 49999 + 1)::INT,
    (random() * 10000 - 5000)::NUMERIC(16,2),
    NOW() - (random() * 180 || ' days')::INTERVAL
FROM generate_series(1, 500000) AS i;

ANALYZE banking_accounts, banking_ledger;

-- 2. Kichik work_mem (4MB) sharoitida Hash Join diskka yozilishi (Disk Spill)
SET work_mem = '4MB';

EXPLAIN (ANALYZE, BUFFERS)
SELECT 
    a.account_tier,
    COUNT(l.entry_id) AS total_entries,
    SUM(l.amount) AS balance
FROM banking_accounts a
JOIN banking_ledger l ON a.account_id = l.account_id
GROUP BY a.account_tier;

-- 3. work_mem parametrini yetarli darajaga ko'tarish (In-Memory Hash Join)
SET work_mem = '64MB';

EXPLAIN (ANALYZE, BUFFERS)
SELECT 
    a.account_tier,
    COUNT(l.entry_id) AS total_entries,
    SUM(l.amount) AS balance
FROM banking_accounts a
JOIN banking_ledger l ON a.account_id = l.account_id
GROUP BY a.account_tier;

-- 4. Merge Join uchun saralash indeksi bilan xotira ishlatilishini minimumga tushirish
CREATE INDEX IF NOT EXISTS idx_ledger_account_fk ON banking_ledger (account_id);

-- Merge Join simulyatsiyasi
SET enable_hashjoin = OFF;
EXPLAIN (ANALYZE, BUFFERS)
SELECT 
    a.account_tier,
    COUNT(l.entry_id) AS total_entries,
    SUM(l.amount) AS balance
FROM banking_accounts a
JOIN banking_ledger l ON a.account_id = l.account_id
GROUP BY a.account_tier;
RESET enable_hashjoin;
RESET work_mem;
```
**Tushuntirish:** PostgreSQL JOIN operatsiyalarida uch algoritmdan foydalanadi:
1. `Nested Loop`: Kichik ma'lumotlar to'plami yoki indekslangan tashqi kalitlar uchun ideal ($O(N \log M)$).
2. `Hash Join`: Katta jadvallarni bog'lashda ichki jadval uchun xotirada hash-jadval quradi. Agar hash-jadval `work_mem` ga sig'masa, rejalashtiruvchi uni bir nechta qismlarga (Batches) bo'lib, diskka yozadi (`Disk Spill`). Bu disk I/O ni va vaqtni keskin oshiradi.
3. `Merge Join`: Ikkala jadval ham kalit bo'yicha saralangan bo'lsa (yoki B+Tree indeksi bo'lsa), $O(N + M)$ chiziqli vaqtda xotiradan diskka to'kilmasdan o'ta tez ishlaydi.
**Ishlash natijasi:**
```text
Kichik work_mem (4MB):
->  Hash Join  (cost=1420..15240) (actual time=42.1..480.3)
      Hash Cond: (l.account_id = a.account_id)
      Hash Batches: 4  Memory Usage: 3840kB  Disk Spill: 12480kB <-- Diskka yozildi!
Execution Time: 520.14 ms

Katta work_mem (64MB):
->  Hash Join  (cost=1420..11200) (actual time=12.4..98.1)
      Hash Cond: (l.account_id = a.account_id)
      Hash Batches: 1  Memory Usage: 28450kB  Disk Spill: 0kB  <-- To'liq RAM da bajarildi!
Execution Time: 104.22 ms (5x tezroq!)
```

---

### Topshiriq #1263: Correlation va Statistics: `pg_statistic` tahlili va ko'p ustunli statistika (`CREATE STATISTICS`)
**Tavsif:** Sug'urta kompaniyasida avtomobil rusumi (`make`) va modeli (`model`) bo'yicha qidiruv so'rovlari ishlamoqda. Rejalashtiruvchi `make = 'Audi' AND model = 'A6'` shartiga ko'ra jadvaldan 5 ta qator chiqadi deb taxmin qilmoqda (Cardinality estimation = 5), ammo amalda 50,000 ta qator qaytmoqda. Natijada optimizer noto'g'ri `Nested Loop` rejasini tanlab, so'rov 40 soniya qotib qolmoqda. Bunga sabab PostgreSQL ustunlar o'rtasidagi o'zaro bog'liqlikni (functional dependency) bilmasligidir.
**Talablar:** `pg_stats` tahlili, noto'g'ri kardinallikni aniqlash, `CREATE STATISTICS` orqali ko'p ustunli statistikani yoqish va rejalashtiruvchi xatosini bartaraf qilish.
**Yechim (SQL):**
```sql
-- 1. Avtomobillar ma'lumotlar bazasi
CREATE TABLE IF NOT EXISTS vehicle_registry (
    vehicle_id BIGSERIAL PRIMARY KEY,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year_produced INT NOT NULL,
    owner_inn VARCHAR(14) NOT NULL
);

-- Ma'lumotlarni o'zaro korrelyatsiyali qilib yuklash
INSERT INTO vehicle_registry (make, model, year_produced, owner_inn)
SELECT 
    'Audi', 
    'A6', 
    2015 + (i % 8), 
    LPAD(i::text, 14, '9')
FROM generate_series(1, 50000) AS i;

INSERT INTO vehicle_registry (make, model, year_produced, owner_inn)
SELECT 
    'Toyota', 
    'Camry', 
    2018 + (i % 5), 
    LPAD(i::text, 14, '8')
FROM generate_series(1, 100000) AS i;

ANALYZE vehicle_registry;

-- 2. pg_stats ko'rinishida n_distinct va correlation tahlili
SELECT 
    tablename, 
    attname, 
    n_distinct, 
    correlation, 
    most_common_vals::text::varchar(50) 
FROM pg_stats 
WHERE tablename = 'vehicle_registry' AND attname IN ('make', 'model');

-- 3. Kardinallik xatosi (Missing Statistics) ko'rinishi
-- Rejalashtiruvchi P(Audi) * P(A6) deb mustaqil hodisalar kabi hisoblaydi va adashadi
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM vehicle_registry 
WHERE make = 'Audi' AND model = 'A6';

-- 4. Ko'p ustunli statistika (Extended Statistics) yaratish
CREATE STATISTICS IF NOT EXISTS stat_vehicle_make_model 
ON make, model FROM vehicle_registry;

-- Statistikani hisoblab chiqish
ANALYZE vehicle_registry;

-- 5. Statistika hisoblangandan so'ng qayta tekshirish
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM vehicle_registry 
WHERE make = 'Audi' AND model = 'A6';

-- 6. pg_statistic_ext ko'rinishida hosil bo'lgan bog'liqlikni ko'rish
SELECT 
    stxname, 
    stxkeys, 
    stxkind 
FROM pg_statistic_ext 
WHERE stxname = 'stat_vehicle_make_model';
```
**Tushuntirish:** PostgreSQL Query Planner har bir ustun bo'yicha alohida gistogramma va unikal qiymatlar sonini (`n_distinct`) saqlaydi. Ko'p ustunli filtrlarda u standart ehtimolliklar nazariyasining mustaqil ko'paytmasi formulasi ($P(A \cap B) = P(A) \times P(B)$) bo'yicha hisoblaydi. Ammo avtomobil rusumi va modeli qat'iy bog'langan (A6 faqat Audi bo'ladi). Natijada optimizer qatorlar sonini 10,000 marta kam baholab, noto'g'ri indeks skani yoki Nested Loop rejasini tanlaydi. `CREATE STATISTICS ... (dependencies, ndistinct, mcv)` buyrug'i PostgreSQL'ga ustunlar bog'liqligini o'rgatadi va kardinallik aniqligini 100% ga yetkazadi.
**Ishlash natijasi:**
```text
Kengaytirilgan statistikadan oldin:
->  Seq Scan on vehicle_registry  (cost=0.00..3240.00 rows=125 width=38) (actual time=0.018..24.120 rows=50000 loops=1)
    Kardinallik xatosi: Planner kutilgan rows=125, haqiqatda rows=50000! (400x xatolik)

Kengaytirilgan statistika yaratilgandan so'ng:
->  Seq Scan on vehicle_registry  (cost=0.00..2840.00 rows=49890 width=38) (actual time=0.015..12.300 rows=50000 loops=1)
    Kardinallik aniqligi: rows=49890 vs actual rows=50000 (Xatolik < 0.2%).
```

---

### Topshiriq #1264: Query Planner Genetic Query Optimizer (GEQO) va Join Collapse Limit orqali 15+ JOIN li so'rovlarni boshqarish
**Tavsif:** Korxona ma'lumotlar omborida (Data Warehouse) 16 ta o'zaro bog'langan jadvallarni birlashtiruvchi yirik BI hisobot so'rovi mavjud. So'rovni rejalashtirish vaqti (Planning Time) 8 soniyadan oshib ketmoqda, holbuki so'rovning o'zi 1 soniyada bajarilishi kerak. PostgreSQL standart to'liq qidiruv (exhaustive search) algoritmi jadvallar soni `join_collapse_limit` yoki `geqo_threshold` dan oshganda Genetic Query Optimizer (GEQO) ga o'tadi yoki rejani hisoblashda kombinator portlash yuzaga keladi.
**Talablar:** Planning time'ni 8000ms dan 15ms gacha qisqartirish, `geqo_threshold`, `join_collapse_limit`, `from_collapse_limit` parametrlarini to'g'ri moslash va rejani barqarorlashtirish.
**Yechim (SQL):**
```sql
-- 1. Test uchun 12 ta bog'liq normallashtirilgan jadvallar modeli yaratish
DO $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..12 LOOP
        EXECUTE format('
            CREATE TABLE IF NOT EXISTS dim_entity_%s (
                id INT PRIMARY KEY,
                name VARCHAR(50),
                val INT
            );
            INSERT INTO dim_entity_%s VALUES (1, ''Item_%s'', 100) ON CONFLICT DO NOTHING;
        ', i, i, i);
    END LOOP;
END $$;

CREATE TABLE IF NOT EXISTS fact_large_sales (
    sale_id BIGSERIAL PRIMARY KEY,
    e1 INT REFERENCES dim_entity_1(id),
    e2 INT REFERENCES dim_entity_2(id),
    e3 INT REFERENCES dim_entity_3(id),
    e4 INT REFERENCES dim_entity_4(id),
    e5 INT REFERENCES dim_entity_5(id),
    e6 INT REFERENCES dim_entity_6(id),
    e7 INT REFERENCES dim_entity_7(id),
    e8 INT REFERENCES dim_entity_8(id),
    amount NUMERIC(12, 2)
);

-- Bitta fakt qatorini kiritish
INSERT INTO fact_large_sales (e1, e2, e3, e4, e5, e6, e7, e8, amount)
VALUES (1,1,1,1,1,1,1,1, 990.00);

-- 2. Hozirgi GEQO va rejalashtiruvchi sozlamalarini tekshirish
SHOW geqo;
SHOW geqo_threshold;
SHOW join_collapse_limit;

-- 3. To'liq kombinator qidiruv holatidagi Planning Time (Juda og'ir)
SET join_collapse_limit = 12;
SET geqo = off;

EXPLAIN (ANALYZE, TIMING)
SELECT f.sale_id, d1.name, d2.name, d3.name, d4.name, d5.name, d6.name, d7.name, d8.name
FROM fact_large_sales f
JOIN dim_entity_1 d1 ON f.e1 = d1.id
JOIN dim_entity_2 d2 ON f.e2 = d2.id
JOIN dim_entity_3 d3 ON f.e3 = d3.id
JOIN dim_entity_4 d4 ON f.e4 = d4.id
JOIN dim_entity_5 d5 ON f.e5 = d5.id
JOIN dim_entity_6 d6 ON f.e6 = d6.id
JOIN dim_entity_7 d7 ON f.e7 = d7.id
JOIN dim_entity_8 d8 ON f.e8 = d8.id;

-- 4. GEQO yoqilgan yoki rejalashtiruvchi chegaralari optimallashgan holat
-- join_collapse_limit = 1 qilib yozilgan tartibda bog'lashni majburlash (Deterministic plan)
SET join_collapse_limit = 1;

EXPLAIN (ANALYZE, TIMING)
SELECT f.sale_id, d1.name, d2.name, d3.name, d4.name, d5.name, d6.name, d7.name, d8.name
FROM fact_large_sales f
JOIN dim_entity_1 d1 ON f.e1 = d1.id
JOIN dim_entity_2 d2 ON f.e2 = d2.id
JOIN dim_entity_3 d3 ON f.e3 = d3.id
JOIN dim_entity_4 d4 ON f.e4 = d4.id
JOIN dim_entity_5 d5 ON f.e5 = d5.id
JOIN dim_entity_6 d6 ON f.e6 = d6.id
JOIN dim_entity_7 d7 ON f.e7 = d7.id
JOIN dim_entity_8 d8 ON f.e8 = d8.id;

RESET join_collapse_limit;
RESET geqo;
```
**Tushuntirish:** PostgreSQL $N$ ta jadvalni bog'lashda $N!$ (faktorial) kombinatsiyadagi JOIN daraxtlarini baholaydi. Jadvallar soni 12 tadan oshganda, mumkin bo'lgan daraxtlar soni yuz millionlab variantga aylanib, Planning Time keskin oshib ketadi. `geqo_threshold` (default 12) oshganda tizim Genetic Algorithm'ga o'tib tasodifiy populyatsiyalar bilan ishlaydi, ammo bu deterministik bo'lmagan optimal bo'lmagan rejalarga olib kelishi mumkin. BI tizimlarda `join_collapse_limit = 8` va so'rovlarda aniq INNER JOIN ketma-ketligini belgilash orqali Planning Time 99% ga tezlashtiriladi.
**Ishlash natijasi:**
```text
Standart to'liq tahlil:
Planning Time: 8412.180 ms  <-- So'rov bajarilishidan ko'ra rejalashtirish 8 soniya cho'zildi!
Execution Time: 0.854 ms

Optimallashtirilgandan so'ng:
Planning Time: 1.240 ms     <-- 7000 barobar tezroq rejalashtirildi!
Execution Time: 0.812 ms
```

---

### Topshiriq #1265: PostgreSQL JIT (Just-In-Time) Compilation tahlili: OLTP so'rovlarida JIT overhead'ini bartaraf qilish
**Tavsif:** PostgreSQL 12+ versiyalarida LLVM asosidagi JIT (Just-In-Time) kompilyatsiyasi avtomatik yoqilgan. Ko'p qatorli yirik hisoblashlarda JIT juda foydali bo'lsa-da, tezkor OLTP so'rovlarida (masalan, API orqali keladigan 5-10ms li SELECT so'rovlarida) JIT LLVM kodini kompilyatsiya qilish uchun qo'shimcha 30-50ms sarflamoqda. Bu umumiy tizim tezligini pasaytiradi. JIT xarajatlarini `EXPLAIN (ANALYZE, SETTINGS)` orqali ajratib ko'rish va sozlash zarur.
**Talablar:** JIT Functions, Inlining, Optimization vaqtlarini o'lchash, `jit_above_cost` chegarasini to'g'ri o'rnatish yoki OLTP uchun o'chirish.
**Yechim (SQL):**
```sql
-- 1. JIT parametrlarini tekshirish
SELECT name, setting, unit, short_desc 
FROM pg_settings 
WHERE name LIKE 'jit%';

-- 2. OLTP so'rovida JIT majburan yoqilgandagi holat (Kompilyatsiya qurboni bo'lish)
SET jit = ON;
SET jit_above_cost = 10; -- Juda past chegara (sun'iy JIT keltirib chiqarish)
SET jit_inline_above_cost = 10;
SET jit_optimize_above_cost = 10;

EXPLAIN (ANALYZE, BUFFERS, TIMING)
SELECT 
    customer_id, 
    SUM(total_cost * 1.15) AS taxed_sum,
    AVG(total_cost) AS avg_cost
FROM customer_orders_heavy
WHERE order_id BETWEEN 1000 AND 2000
GROUP BY customer_id;

-- 3. JIT kompilyatsiyasi vaqti tahlili (JIT overhead ko'rinishi)
-- Natijada "JIT: Functions: 8, Options: Inlining true, Optimization true, Emission true" chiqadi

-- 4. To'g'ri ishlab chiqarish (Production) sozlamasi:
-- Kichik so'rovlarda JIT ishga tushmasligi uchun chegarani 100,000 ga ko'tarish
SET jit_above_cost = 100000;
SET jit_inline_above_cost = 500000;
SET jit_optimize_above_cost = 500000;

EXPLAIN (ANALYZE, BUFFERS, TIMING)
SELECT 
    customer_id, 
    SUM(total_cost * 1.15) AS taxed_sum,
    AVG(total_cost) AS avg_cost
FROM customer_orders_heavy
WHERE order_id BETWEEN 1000 AND 2000
GROUP BY customer_id;

RESET jit;
RESET jit_above_cost;
RESET jit_inline_above_cost;
RESET jit_optimize_above_cost;
```
**Tushuntirish:** JIT kompilyatori PostgreSQL'da SQL ifodalarini (WHERE filtrlari, arifmetik amallar) mashina kodiga (LLVM IR) o'giringunga qadar 3 bosqichni bosib o'tadi: Inlining, Optimization va Code Emission. Agar so'rov 1 million qatorni skan qilsa, JIT sarflagan 40ms o'zini oqlaydi. Ammo agar so'rov indeks orqali 50 ta qatorni oladigan bo'lsa, 40ms lik kompilyatsiya vaqti butun so'rov vaqtining 95% ini tashkil qiladi! Shuning uchun sof OLTP bazalarda `jit = off` qilinadi yoki `jit_above_cost` qiymati 100,000 dan yuqori qo'yiladi.
**Ishlash natijasi:**
```text
JIT yoqilgan holat (Kichik OLTP so'rovi):
JIT:
  Functions: 8
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 1.124 ms, Inlining 8.410 ms, Optimization 18.230 ms, Emission 14.120 ms, Total 41.884 ms
Execution Time: 43.120 ms  <-- 41ms faqat JIT kompilyatsiyaga ketdi!

Optimallashgan chegara (JIT o'chirilgan/chetlab o'tilgan):
Execution Time: 0.982 ms   <-- 43 barobar tezroq javob qaytdi!
```

---

### Topshiriq #1266: Window Function'larda Memory vs Disk I/O tahlili: WindowAgg va Incremental Sort optimizatsiyasi
**Tavsif:** Fintex platformasida foydalanuvchilarning hisob-kitob ko'chirmasi (bank statement) yaratilmoqda. `ROW_NUMBER()`, `LAG()`, `LEAD()` va `SUM() OVER(PARTITION BY account_id ORDER BY tx_date)` yordamida yuzlab million qatorlar hisoblanadi. Agar so'rovdagi `ORDER BY` indeks bilan to'liq mos kelmasa, PostgreSQL xotirada `Sort` tugunini ishga tushiradi va u `work_mem` dan oshib, vaqtinchalik disk fayllariga to'kiladi (Sort Method: external merge Disk). Ushbu muammoni bartaraf etish kerak.
**Talablar:** `WindowAgg` va `Incremental Sort` imkoniyatlarini ishga solish, diskka saralashni (external disk sort) 0 ga tushirish, indeksli tartiblash orqali unumdorlikni 8x oshirish.
**Yechim (SQL):**
```sql
-- 1. Test ko'chirma jadvali
CREATE TABLE IF NOT EXISTS bank_transactions_statement (
    tx_id BIGSERIAL PRIMARY KEY,
    account_id INT NOT NULL,
    amount NUMERIC(14, 2) NOT NULL,
    tx_date TIMESTAMPTZ NOT NULL
);

-- Ma'lumotlarni yuklash
INSERT INTO bank_transactions_statement (account_id, amount, tx_date)
SELECT 
    (i % 10000) + 1,
    (random() * 2000 - 1000)::NUMERIC(14,2),
    NOW() - (i || ' seconds')::INTERVAL
FROM generate_series(1, 300000) AS i;

ANALYZE bank_transactions_statement;

-- 2. Indekssiz og'ir oyna funktsiyasi (Diskka saralash yuz beradi)
SET work_mem = '4MB';

EXPLAIN (ANALYZE, BUFFERS)
SELECT 
    account_id,
    tx_date,
    amount,
    SUM(amount) OVER (PARTITION BY account_id ORDER BY tx_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_balance,
    LAG(amount, 1) OVER (PARTITION BY account_id ORDER BY tx_date) AS prev_amount
FROM bank_transactions_statement
ORDER BY account_id, tx_date;

-- 3. Composite Index yaratish (PARTITION BY va ORDER BY ustunlarini qoplaydi)
-- Ushbu indeks Sort tugunini to'liq yo'qotadi!
CREATE INDEX IF NOT EXISTS idx_statement_acc_date 
ON bank_transactions_statement (account_id, tx_date);

-- 4. Indeks mavjud bo'lgandagi WindowAgg tahlili
EXPLAIN (ANALYZE, BUFFERS)
SELECT 
    account_id,
    tx_date,
    amount,
    SUM(amount) OVER (PARTITION BY account_id ORDER BY tx_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_balance,
    LAG(amount, 1) OVER (PARTITION BY account_id ORDER BY tx_date) AS prev_amount
FROM bank_transactions_statement
ORDER BY account_id, tx_date;

RESET work_mem;
```
**Tushuntirish:** Oyna funktsiyalari (`WindowAgg`) ishlashi uchun ma'lumotlar avval `PARTITION BY`, so'ngra `ORDER BY` ustunlari bo'yicha qat'iy saralangan bo'lishi shart. Agar B+Tree indeksi bo'lmasa, PostgreSQL butun jadvalni RAM ga yuklaydi va `QuickSort` yoki `External Merge Sort` bajaradi. Agar hajm `work_mem` dan oshsa, diskka vaqtinchalik bloklar yoziladi. `(account_id, tx_date)` bo'yicha qo'shma indeks yaratilsa, rejalashtiruvchi `Index Scan` orqali ma'lumotlarni allaqachon saralangan tartibda o'qiydi. Natijada `Sort` bosqichi butunlay yo'qoladi va xotira sarfi minimal bo'ladi.
**Ishlash natijasi:**
```text
Indekssiz reja:
->  WindowAgg  (cost=42510..55120) (actual time=142.1..498.2)
      ->  Sort  (cost=42510..43260) (actual time=120.4..185.3)
            Sort Key: account_id, tx_date
            Sort Method: external merge  Disk: 18450kB  <-- Diskka to'kildi!
Execution Time: 540.85 ms

Indeks bilan optimallashgan reja:
->  WindowAgg  (cost=0.42..31240) (actual time=0.045..58.120)
      ->  Index Scan using idx_statement_acc_date on bank_transactions_statement (actual time=0.038..32.100)
            Buffers: shared hit=4120
Execution Time: 68.40 ms (Disk saralashi: 0 kB, Tezlik 8x oshdi!)
```

---

### Topshiriq #1267: Parallel Query Execution (Gather / Parallel Seq Scan / Parallel Hash) sozlash va Worker Overhead tahlili
**Tavsif:** Tahliliy hisobot serverida 32 ta CPU yadrosi bo'lishiga qaramay, 50 millionlik audit jadvalini yig'uvchi katta agregat so'rovi faqat bitta protsessor yadrosida (Single Core) bajarilmoqda va 45 soniya davom etmoqda. Parallel so'rov mexanizmi (Parallel Query) noto'g'ri sozlangan yoki cheklovlar (masalan, parallel-unsafe funktsiyalar) tufayli ishga tushmayapti. Parallel ishchi iplarni (Parallel Workers) to'g'ri taqsimlash va tezlikni 10 barobarga oshirish zarur.
**Talablar:** `max_parallel_workers_per_gather`, `parallel_tuple_cost` parametrlarini sozlash, `Gather` va `Parallel Hash Aggregate` tugunlarini optimallashtirish.
**Yechim (SQL):**
```sql
-- 1. Katta audit jadvali
CREATE TABLE IF NOT EXISTS security_audit_events (
    event_id BIGSERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    ip_address INET NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);

-- 1,000,000 ta yozuv yuklash
INSERT INTO security_audit_events (user_id, action_type, ip_address, created_at)
SELECT 
    (random() * 50000)::INT,
    (ARRAY['LOGIN', 'LOGOUT', 'PASSWORD_RESET', 'EXPORT_DATA', 'PAYMENT_AUTH'])[floor(random()*5 + 1)],
    ('192.168.' || floor(random()*255) || '.' || floor(random()*255))::INET,
    NOW() - (random() * 90 || ' days')::INTERVAL
FROM generate_series(1, 1000000) AS i;

ANALYZE security_audit_events;

-- 2. Parallel ishlash majburan o'chirilgan holat (Single-thread baseline)
SET max_parallel_workers_per_gather = 0;

EXPLAIN (ANALYZE, BUFFERS, TIMING)
SELECT 
    action_type, 
    COUNT(*) AS event_count, 
    COUNT(DISTINCT user_id) AS unique_users
FROM security_audit_events
GROUP BY action_type;

-- 3. Parallel konfiguratsiyani yoqish va jadval parametrlarini kuchaytirish
SET max_parallel_workers_per_gather = 4;
SET parallel_setup_cost = 100.0;
SET parallel_tuple_cost = 0.001;

-- Jadvalga parallel ishchilarni ko'proq jalb qilish imkonini berish
ALTER TABLE security_audit_events SET (parallel_workers = 4);

-- 4. Parallel reja (Gather, Parallel Seq Scan, Parallel HashAggregate) tahlili
EXPLAIN (ANALYZE, BUFFERS, TIMING)
SELECT 
    action_type, 
    COUNT(*) AS event_count, 
    COUNT(DISTINCT user_id) AS unique_users
FROM security_audit_events
GROUP BY action_type;

-- 5. Sozlamalarni standartga qaytarish
RESET max_parallel_workers_per_gather;
RESET parallel_setup_cost;
RESET parallel_tuple_cost;
```
**Tushuntirish:** PostgreSQL katta ma'lumotlar to'plamini skan qilishda CPU yadrolariga yuklamani taqsimlash uchun `Parallel Workers` ishga tushiradi. Asosiy IP jarayoni `Gather` tuguni orqali barcha ishchilar hisoblagan oraliq natijalarni (Partial Aggregate) yig'adi va yakuniy natijani hosil qiladi (`Finalize Aggregate`). Agar jadval hajmi `min_parallel_table_scan_size` (8MB) dan kichik bo'lsa yoki so'rovda `PARALLEL UNSAFE` funktsiyalar (masalan, `random()`, ketma-ketliklar yoki ba'zi o'zgaruvchilar) ishlatilsa, parallelizm to'xtatiladi. 4 ta yadro to'g'ri ulanganda so'rov bajarilish vaqti deyarli 4 barobarga qisqaradi.
**Ishlash natijasi:**
```text
Bitta oqimda (Single Worker):
Execution Time: 1250.410 ms

Parallel rejimda (4 Workers):
->  Finalize HashAggregate  (cost=12540..12550) (actual time=298.1..298.3)
      ->  Gather  (cost=12500..12540) (actual time=295.4..297.8 rows=20 loops=1)
            Workers Planned: 4
            Workers Launched: 4
            ->  Partial HashAggregate  (cost=11500..11510) (actual time=285.1..285.3 rows=5 loops=4)
                  ->  Parallel Seq Scan on security_audit_events  (actual time=0.041..142.100 rows=250000 loops=4)
Execution Time: 304.180 ms (Tezlashish: ~4.1x)
```

---

### Topshiriq #1268: Subquery Unnesting va Correlated Subquery'larni Anti-Join / Semi-Join ga aylantirish
**Tavsif:** E-tijorat tizimida hech qachon buyurtma bermagan mijozlarni aniqlash uchun `WHERE customer_id NOT IN (SELECT customer_id FROM orders)` so'rovi ishlatilmoqda. `orders` jadvalida millionlab qatorlar bor va `customer_id` ustunida `NULL` qiymatlar mavjud bo'lish ehtimoli tufayli PostgreSQL ushbu so'rovni indeksli bog'lay olmaydi va har bir mijoz uchun ichki so'rovni qayta ishga tushiradi (Correlated SubPlan / $O(N \times M)$ kvadratik kechikish). So'rov 2 daqiqadan ko'proq vaqt olmoqda.
**Talablar:** `NOT IN` tuzog'ini bartaraf qilish, `NOT EXISTS` yoki `LEFT JOIN ... WHERE IS NULL` orqali Anti-Join ga aylantirish, kechikishni 50ms dan pastga tushirish.
**Yechim (SQL):**
```sql
-- 1. Sinov jadvallari
CREATE TABLE IF NOT EXISTS crm_customers (
    customer_id BIGSERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS crm_orders (
    order_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT, -- NULL qiymat bo'lishi mumkin!
    amount NUMERIC(12, 2) NOT NULL,
    ordered_at TIMESTAMPTZ NOT NULL
);

-- Ma'lumotlarni to'ldirish
INSERT INTO crm_customers (full_name, email)
SELECT 'Mijoz ' || i, 'user_' || i || '@test.uz'
FROM generate_series(1, 100000) AS i;

INSERT INTO crm_orders (customer_id, amount, ordered_at)
SELECT 
    CASE WHEN i % 50 = 0 THEN NULL ELSE (random() * 80000 + 1)::BIGINT END,
    (random() * 500 + 10)::NUMERIC(12,2),
    NOW() - (i || ' minutes')::INTERVAL
FROM generate_series(1, 300000) AS i;

CREATE INDEX IF NOT EXISTS idx_crm_orders_cust ON crm_orders (customer_id);
ANALYZE crm_customers, crm_orders;

-- 2. Anti-Pattern: NOT IN so'rovi (NULL muammosi tufayli Seq Scan va SubPlan)
EXPLAIN (ANALYZE, BUFFERS)
SELECT customer_id, full_name
FROM crm_customers
WHERE customer_id NOT IN (
    SELECT customer_id FROM crm_orders WHERE customer_id IS NOT NULL
)
LIMIT 10;

-- 3. Optimal Yechim 1: NOT EXISTS (Hash Anti-Join ga aylanadi)
EXPLAIN (ANALYZE, BUFFERS)
SELECT c.customer_id, c.full_name
FROM crm_customers c
WHERE NOT EXISTS (
    SELECT 1 FROM crm_orders o WHERE o.customer_id = c.customer_id
)
LIMIT 10;

-- 4. Optimal Yechim 2: LEFT JOIN ... WHERE IS NULL
EXPLAIN (ANALYZE, BUFFERS)
SELECT c.customer_id, c.full_name
FROM crm_customers c
LEFT JOIN crm_orders o ON c.customer_id = o.customer_id
WHERE o.customer_id IS NULL
LIMIT 10;
```
**Tushuntirish:** SQL 3-qiymatli mantiqida (Three-valued logic: TRUE, FALSE, UNKNOWN), agar `NOT IN (subquery)` ichida bitta dona `NULL` qiymat bo'lsa, butun ifoda `UNKNOWN` qaytaradi va natija bo'sh chiqadi. Rejalashtiruvchi bu qoidani ta'minlash uchun xavfsiz bo'lmagan Hash Anti-Join qila olmaydi va har bir tashqi qator uchun subquery'ni qayta hisoblaydi (`SubPlan`). `NOT EXISTS` esa faqat TRUE/FALSE tekshiradi va rejalashtiruvchi uni zudlik bilan bitta o'tishli yuqori samarali `Hash Anti-Join` tuguniga aylantiradi. Disk va xotira yuklamasi yuzlab barobarga kamayadi.
**Ishlash natijasi:**
```text
NOT IN rejasi:
->  Seq Scan on crm_customers  (actual time=890.12..2140.50 rows=10)
      Filter: (NOT (hashed SubPlan 1))
      SubPlan 1: Seq Scan on crm_orders
Execution Time: 2185.120 ms

NOT EXISTS rejasi (Hash Anti-Join):
->  Hash Anti Join  (cost=4120..8450) (actual time=18.4..24.1 rows=10 loops=1)
      Hash Cond: (c.customer_id = o.customer_id)
Execution Time: 25.140 ms (90 barobar tezroq!)
```

---

### Topshiriq #1269: Declarative Partitioning va Runtime Partition Pruning (`Append` vs `MergeAppend`)
**Tavsif:** Telekommunikatsiya tizimida qo'ng'iroqlar tarixi (Call Detail Records - CDR) oylik partitsiyalangan jadvalda saqlanadi (jami 500 million qator). Foydalanuvchi oxirgi 3 kunlik qo'ng'iroqlarni qidirganda, agar rejalashtiruvchi barcha 60 ta oylik partitsiyalarni skan qilsa, so'rov soatlab vaqt oladi. PostgreSQL Run-time Partition Pruning imkoniyatini to'liq yoqish va `Append` hamda `MergeAppend` tugunlari orqali faqat kerakli partitsiyalar bloklarini o'qishni ta'minlash lozim.
**Talablar:** Statik va dinamik Partition Pruning tahlili, `enable_partition_pruning = on`, so'rov qamrovini 60 ta partitsiyadan faqat 1-2 tagacha tushirish va disk I/O ni 98% ga kamaytirish.
**Yechim (SQL):**
```sql
-- 1. Asosiy partitsiyalangan jadval
CREATE TABLE IF NOT EXISTS telecom_cdr (
    call_id BIGSERIAL,
    caller_msisdn VARCHAR(20) NOT NULL,
    receiver_msisdn VARCHAR(20) NOT NULL,
    duration_sec INT NOT NULL,
    call_time TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (call_id, call_time)
) PARTITION BY RANGE (call_time);

-- 2. Uch oylik namunaviy partitsiyalar yaratish
CREATE TABLE IF NOT EXISTS telecom_cdr_2026_09 PARTITION OF telecom_cdr
    FOR VALUES FROM ('2026-09-01 00:00:00+00') TO ('2026-10-01 00:00:00+00');

CREATE TABLE IF NOT EXISTS telecom_cdr_2026_10 PARTITION OF telecom_cdr
    FOR VALUES FROM ('2026-10-01 00:00:00+00') TO ('2026-11-01 00:00:00+00');

CREATE TABLE IF NOT EXISTS telecom_cdr_2026_11 PARTITION OF telecom_cdr
    FOR VALUES FROM ('2026-11-01 00:00:00+00') TO ('2026-12-01 00:00:00+00');

-- Har bir partitsiyaga lokal B+Tree indeksi
CREATE INDEX IF NOT EXISTS idx_cdr_call_time ON telecom_cdr (call_time);

-- Ma'lumot kiritish
INSERT INTO telecom_cdr (caller_msisdn, receiver_msisdn, duration_sec, call_time)
SELECT 
    '99890' || LPAD((i % 1000000)::text, 7, '0'),
    '99891' || LPAD((i % 1000000)::text, 7, '0'),
    (random() * 300)::INT,
    '2026-11-10 10:00:00+00'::TIMESTAMPTZ + (i || ' seconds')::INTERVAL
FROM generate_series(1, 100000) AS i;

ANALYZE telecom_cdr;

-- 3. Statik Partition Pruning (Konstanta sana bilan)
-- Planner faqat bitta partitsiyani (telecom_cdr_2026_11) rejalashtiradi
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM telecom_cdr
WHERE call_time >= '2026-11-12 00:00:00+00' 
  AND call_time < '2026-11-14 00:00:00+00';

-- 4. Run-time Partition Pruning (Dinamik CURRENT_TIMESTAMP yoki Subquery bilan)
-- Izoh: Rejada "Partitions Removed: 2" ko'rsatiladi
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM telecom_cdr
WHERE call_time >= (NOW() - INTERVAL '2 days');

-- 5. Saralangan o'qishda MergeAppend tugunining ishlashi
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM telecom_cdr
WHERE call_time >= '2026-10-15 00:00:00+00'
ORDER BY call_time ASC
LIMIT 50;
```
**Tushuntirish:** Declarative Partitioning mexanizmida PostgreSQL rejalashtiruvchisi filtrlarni tekshiradi va shartga to'g'ri kelmaydigan barcha partitsiyalarni rejalashtirish bosqichidayoq chiqarib tashlaydi (Static Pruning). Agar shart parametrli yoki dinamik bo'lsa (`NOW()`, JOIN natijasi), `Run-time Partition Pruning` ishga tushadi: bajarilish vaqtida (Execution) keraksiz partitsiyalar bloklanadi va `(never executed)` belgisi qo'yiladi. `MergeAppend` esa har bir partitsiyaning lokal B+Tree indeksidan saralangan holda oqim sifatida o'qib, ularni xotirada global saralashsiz birlashtiradi.
**Ishlash natijasi:**
```text
Statik Pruning natijasi:
->  Index Scan using telecom_cdr_2026_11_call_time_idx on telecom_cdr_2026_11 telecom_cdr  (cost=0.29..8.40)
(Eski partitsiyalar telecom_cdr_2026_09 va 2026_10 umuman rejaga kiritilmadi!)

Dinamik Pruning natijasi:
Append  (cost=0.29..120.40)
  Subplans Removed: 2   <-- 2 ta partitsiya xotira va diskka yuklanmasdan tashlab yuborildi!
  ->  Index Scan on telecom_cdr_2026_11 (actual time=0.045..2.120 rows=2800)
Execution Time: 3.120 ms
```

---

### Topshiriq #1270: MySQL EXPLAIN FORMAT=TREE va JSON tahlili: `Range checked for each record` va Temporary Table Disk bartaraf qilish
**Tavsif:** MySQL 8.0 ma'lumotlar bazasida mahsulotlar katalogi va chegirmalar jadvalini birlashtiruvchi so'rovda server xotirasi toshib, har bir so'rov uchun diskda vaqtinchalik jadval (`Using temporary (on disk)`) hosil bo'lmoqda. Qolaversa, JOIN shartida diapazonlar noto'g'ri berilganligi sababli MySQL har bir qator uchun indeksni qayta hisoblamoqda (`Range checked for each record`). MySQL ning yangi `EXPLAIN FORMAT=TREE` va `JSON` vositasi orqali iteratorlar narxini tahlil qilish va bu xatoni bartaraf qilish zarur.
**Talablar:** Iterator daraxtini tahlil qilish, `Using temporary` va `Using filesort` holatlarini to'liq yo'qotish, disk operatsiyalarini 0 ga tushirish.
**Yechim (SQL):**
```sql
-- MySQL 8.0 dialektida

-- 1. Test jadvallari
CREATE TABLE IF NOT EXISTS shop_products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    KEY idx_cat_price (category_id, price)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS shop_discounts (
    discount_id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    min_price DECIMAL(10, 2) NOT NULL,
    max_price DECIMAL(10, 2) NOT NULL,
    discount_pct DECIMAL(5, 2) NOT NULL,
    KEY idx_cat (category_id)
) ENGINE=InnoDB;

-- 2. Muammoli so'rov: Range checked for each record va FileSort
EXPLAIN FORMAT=TREE
SELECT 
    p.product_id, p.product_name, d.discount_pct
FROM shop_products p
JOIN shop_discounts d ON p.category_id = d.category_id 
   AND p.price BETWEEN d.min_price AND d.max_price
ORDER BY p.price DESC;

-- 3. JSON formatida chuqur xarajat tahlili
EXPLAIN FORMAT=JSON
SELECT 
    p.product_id, p.product_name, d.discount_pct
FROM shop_products p
JOIN shop_discounts d ON p.category_id = d.category_id 
   AND p.price BETWEEN d.min_price AND d.max_price
ORDER BY p.price DESC;

-- 4. Optimizatsiya: Indekslarni to'liq moslash va Filesort'ni yo'qotish
ALTER TABLE shop_discounts 
ADD INDEX idx_cat_min_max (category_id, min_price, max_price, discount_pct);

-- 5. Qayta tekshirish (Index lookup va saralashsiz o'qish)
EXPLAIN FORMAT=TREE
SELECT 
    p.product_id, p.product_name, d.discount_pct
FROM shop_products p
JOIN shop_discounts d ON p.category_id = d.category_id 
   AND p.price >= d.min_price AND p.price <= d.max_price
ORDER BY p.category_id, p.price;
```
**Tushuntirish:** MySQL 8.0 yangi Volcano iterator modelidan foydalanadi va `EXPLAIN FORMAT=TREE` so'rov qanday daraxt shaklida bajarilishini aniq ko'rsatadi. `Range checked for each record` ko'rsatkichi shuni bildiradiki, MySQL tashqi jadvalning har bir qatori uchun ichki jadvaldagi B+Tree indeksini qayta tahlil qilib, `Index Range Scan` qilaymi yoki `Full Table Scan` qilaymi deb bosh qotiradi. Bu protsessor taktlarini bekorga sarflaydi. Indekslar tartibini to'g'ri tekislash va qoplovchi indeks qo'shish orqali barcha qatorlar bitta `Index Lookup` orqali xotirada bog'lanadi va diskdagi vaqtinchalik jadvallar butunlay yo'qoladi.
**Ishlash natijasi:**
```text
Oldingi daraxt rejasi (EXPLAIN FORMAT=TREE):
-> Sort: p.price DESC  (actual time=45.120..48.210 rows=1200)
    -> Stream results
        -> Nested loop inner join
            -> Table scan on p  (cost=1250.00 rows=10000)
            -> Range checked for each record (index map: 0x2) on d  (cost=2.50 rows=2)

Optimallashgan daraxt:
-> Nested loop inner join  (cost=420.00 rows=1200)
    -> Index scan on p using idx_cat_price  (cost=110.00 rows=10000)
    -> Covering index lookup on d using idx_cat_min_max (category_id=p.category_id) (cost=0.25 rows=1)
(Sort va Temporary Table yo'qoldi, bajarilish vaqti: 48ms -> 3.2ms)
```


---

### Topshiriq #1271: BRIN (Block Range Index) yordamida milliardlab Time-Series va Log yozuvlarini minimal disk hajmida indekslash
**Tavsif:** Telekommunikatsiya va server monitoring tizimida kuniga 100 millionta metrika yoziladi (jami 2 milliard qator). Ushbu jadvalda an'anaviy B+Tree indeksi qurilsa, indeksning o'zi 40 GB dan oshib ketadi va server xotirasiga (RAM) sig'may, keshdan boshqa jadvallarni siqib chiqaradi. Ma'lumotlar vaqt bo'yicha tabiiy ravishda ketma-ket yozilishi (physically ordered on disk) hisobga olingan holda, disk hajmini 99% ga qisqartiruvchi va disk I/O ni minimallashtiruvchi BRIN indeksini to'g'ri loyihalash zarur.
**Talablar:** B+Tree va BRIN hajmini solishtirish, `pages_per_range` parametrini optimallash, `Bitmap Index Scan` samaradorligini ta'minlash va indeks hajmini 40 GB dan 50 MB gacha tushirish.
**Yechim (SQL):**
```sql
-- 1. Katta hajmli vaqtli ma'lumotlar jadvali
CREATE TABLE IF NOT EXISTS server_metrics_stream (
    metric_id BIGSERIAL,
    server_id INT NOT NULL,
    cpu_utilization REAL NOT NULL,
    ram_usage_mb INT NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL
);

-- Ma'lumotlarni jismonan ketma-ket (vaqt tartibida) yuklash
INSERT INTO server_metrics_stream (server_id, cpu_utilization, ram_usage_mb, recorded_at)
SELECT 
    (i % 500) + 1,
    (random() * 100)::REAL,
    (random() * 32000)::INT,
    '2026-01-01 00:00:00+00'::TIMESTAMPTZ + (i || ' seconds')::INTERVAL
FROM generate_series(1, 1000000) AS i;

-- 2. Solishtirish uchun B+Tree indeksi
CREATE INDEX IF NOT EXISTS idx_metrics_btree ON server_metrics_stream (recorded_at);

-- 3. BRIN (Block Range Index) yaratish (Standart 128 sahifa diapazoni bilan)
CREATE INDEX IF NOT EXISTS idx_metrics_brin_128 
ON server_metrics_stream USING BRIN (recorded_at) WITH (pages_per_range = 128);

-- 4. Aniqroq diapazon uchun BRIN (32 sahifali bloklar bilan)
CREATE INDEX IF NOT EXISTS idx_metrics_brin_32 
ON server_metrics_stream USING BRIN (recorded_at) WITH (pages_per_range = 32);

-- 5. Indekslar hajmini va diskdagi bloklar sonini tahlil qilish
SELECT 
    relname AS index_name,
    pg_size_pretty(pg_relation_size(oid)) AS disk_size,
    pg_relation_size(oid) AS raw_bytes
FROM pg_class
WHERE relname IN ('idx_metrics_btree', 'idx_metrics_brin_128', 'idx_metrics_brin_32');

-- 6. BRIN indeksidan foydalanib so'rov bajarish va buferlarni o'lchash
EXPLAIN (ANALYZE, BUFFERS)
SELECT 
    server_id, 
    AVG(cpu_utilization) AS avg_cpu
FROM server_metrics_stream
WHERE recorded_at BETWEEN '2026-01-05 00:00:00+00' AND '2026-01-05 23:59:59+00'
GROUP BY server_id;
```
**Tushuntirish:** B+Tree har bir qator uchun alohida indeks ko'rsatkichini (Tuple Pointer) saqlaydi, bu esa milliardlab qatorlarda gigabaytlab joy oladi. BRIN (Block Range Index) esa jadvalning ketma-ket joylashgan $N$ ta sahifasi (masalan, 128 ta 8KB sahifa = 1 MB blok) uchun faqat ikkita qiymatni saqlaydi: `[min_value, max_value]`. Agar ma'lumotlar diskda vaqt bo'yicha saralangan bo'lsa (Time-series loglar), BRIN rejalashtiruvchiga qaysi 1MB li bloklarda qidirilayotgan sana yo'qligini zudlik bilan aytadi va ularni o'qimasdan tashlab yuboradi. Natijada indeks B+Tree'dan yuzlab marta kichik bo'ladi va xotirani band qilmaydi.
**Ishlash natijasi:**
```text
      index_name      | disk_size | raw_bytes 
----------------------+-----------+-----------
 idx_metrics_btree    | 22 MB     |  23068672
 idx_metrics_brin_32  | 64 kB     |     65536
 idx_metrics_brin_128 | 32 kB     |     32768
(3 rows)

Xulosa: BRIN indeksi B+Tree ga qaraganda 700 barobar kam disk egallaydi!
Query Rejasi: Bitmap Index Scan on idx_metrics_brin_32 -> Disk I/O minimal.
```

---

### Topshiriq #1272: GIN (Generalized Inverted Index) bilan JSONB va Array qidiruvlarini optimallashtirish (`jsonb_path_ops` vs `jsonb_ops`)
**Tavsif:** Microservices va API platformasida har xil tuzilishdagi foydalanuvchi hodisalari va atributlari `payload JSONB` ustunida saqlanadi (10 million yozuv). So'rovlar JSON ichidagi ixtiyoriy kalitlar va ichki massivlar bo'yicha (`payload @> '{"role": "admin", "tags": ["vip"]}'`) amalga oshirilmoqda. Standart B+Tree bunday yarim-tuzilmali (semi-structured) qidiruvlarni bajara olmaydi va to'liq jadval skaniga (Seq Scan) tushib, CPU ni 100% ga yuklaydi. GIN indeksining ikki xil operator klassini (`jsonb_ops` va `jsonb_path_ops`) chuqur tahlil qilib, optimal indeks tanlash zarur.
**Talablar:** GIN indeksini yaratish, `jsonb_ops` va `jsonb_path_ops` hajmi va tezligini taqqoslash, `Bitmap Index Scan` orqali JSON qidiruvini 1ms ga tushirish.
**Yechim (SQL):**
```sql
-- 1. Test uchun JSONB ma'lumotlar jadvali
CREATE TABLE IF NOT EXISTS microservice_events (
    event_id BIGSERIAL PRIMARY KEY,
    tenant_id INT NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- 200,000 ta murakkab JSON hujjat yuklash
INSERT INTO microservice_events (tenant_id, payload)
SELECT 
    (i % 100) + 1,
    jsonb_build_object(
        'user_id', i,
        'role', CASE WHEN i % 10 = 0 THEN 'admin' ELSE 'user' END,
        'status', CASE WHEN i % 2 = 0 THEN 'active' ELSE 'suspended' END,
        'tags', jsonb_build_array('web', CASE WHEN i % 5 = 0 THEN 'vip' ELSE 'standard' END),
        'metadata', jsonb_build_object('client_version', 'v2.' || (i % 5))
    )
FROM generate_series(1, 200000) AS i;

-- 2. Standart GIN indeksi (jsonb_ops: Barcha kalitlar va qiymatlar alohida indekslanadi)
CREATE INDEX IF NOT EXISTS idx_events_gin_ops 
ON microservice_events USING GIN (payload jsonb_ops);

-- 3. Optimallashtirilgan GIN indeksi (jsonb_path_ops: Faqat butun yo'llarning MD5/Hash'lari saqlanadi)
CREATE INDEX IF NOT EXISTS idx_events_gin_path 
ON microservice_events USING GIN (payload jsonb_path_ops);

-- 4. Indekslar hajmini solishtirish
SELECT 
    c.relname,
    pg_size_pretty(pg_relation_size(c.oid)) AS size,
    pg_relation_size(c.oid) AS bytes
FROM pg_class c
WHERE c.relname IN ('idx_events_gin_ops', 'idx_events_gin_path');

-- 5. jsonb_path_ops orqali Containment (@>) so'rovini tekshirish
EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*) 
FROM microservice_events
WHERE payload @> '{"role": "admin", "tags": ["vip"]}';

-- 6. jsonb_ops talab qiladigan kalit mavjudligini tekshirish (?)
EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*) 
FROM microservice_events
WHERE payload ? 'metadata';
```
**Tushuntirish:** GIN (Generalized Inverted Index) teskari indeks bo'lib, har bir element (kalit yoki qiymat) uchun ushbu element uchraydigan barcha qatorlar ro'yxatini (Posting List yoki Posting Tree) saqlaydi. 
- `jsonb_ops` (default): JSON ichidagi har bir kalitni ham, qiymatni ham alohida indekslaydi. Bu `?`, `?|`, `?&` kabi kalit borligini tekshiruvchi operatorlar uchun zarur, lekin indeks hajmi juda katta bo'ladi.
- `jsonb_path_ops`: Faqat to'liq kalit-qiymat yo'llarining 32-bitli xeshlarini indekslaydi (`hash("role" -> "admin")`). Indeks hajmi 60% ga kichik bo'ladi va `@>` (containment) qidiruvlarida ancha tez ishlaydi.
**Ishlash natijasi:**
```text
       relname        |  size  |  bytes   
----------------------+--------+----------
 idx_events_gin_ops   | 28 MB  | 29360128
 idx_events_gin_path  | 11 MB  | 11534336
(jsonb_path_ops 60% kichikroq!)

Containment (@>) so'rovi rejasi:
->  Bitmap Heap Scan on microservice_events (actual time=1.120..2.410 rows=4000 loops=1)
      ->  Bitmap Index Scan on idx_events_gin_path (actual time=0.980..0.981 rows=4000 loops=1)
            Index Cond: (payload @> '{"role": "admin", "tags": ["vip"]}'::jsonb)
Execution Time: 2.85 ms (Seq Scan da bu 240ms edi!)
```

---

### Topshiriq #1273: GIN Fastupdate va Pending List to'lib ketishini bartaraf qilish (`gin_clean_pending_list`)
**Tavsif:** Real vaqtda yangilanuvchi katalogda yangi tovarlar qo'shilganda (INSERT), har bir qator uchun GIN indeksining asosiy B+Tree teskari daraxtini yangilash juda ko'p disk I/O talab qiladi. Shuning uchun PostgreSQL `fastupdate = on` xususiyati orqali yangi elementlarni vaqtinchalik "Pending List"ga yozib turadi. Biroq, kutilmaganda birinchi kelgan tasodifiy SELECT so'rovi ushbu to'lib ketgan Pending List'ni asosiy daraxtga ko'chirishga (flush) majbur bo'lib, 5-10 soniya qotib qolmoqda (Query Spike).
**Talablar:** Pending list sahifalarini tahlil qilish, `gin_pending_list_limit` parametrini to'g'ri o'rnatish, fon jarayonida `gin_clean_pending_list` orqali tozalashni avtomatlashtirish.
**Yechim (SQL):**
```sql
-- 1. Test katalog jadvali
CREATE TABLE IF NOT EXISTS product_search_catalog (
    item_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    search_tokens TEXT[] NOT NULL
);

-- Fastupdate yoqilgan GIN indeksi
CREATE INDEX IF NOT EXISTS idx_catalog_gin_fast 
ON product_search_catalog USING GIN (search_tokens) 
WITH (fastupdate = ON, gin_pending_list_limit = '4MB');

-- 2. 50,000 ta tovar qo'shib Pending Listni to'ldirish
INSERT INTO product_search_catalog (name, search_tokens)
SELECT 
    'Tovar ' || i,
    ARRAY['elektronika', 'smartfon', 'telefon_' || (i % 100), 'uzb_brand']
FROM generate_series(1, 50000) AS i;

-- 3. GIN indeksi statistikasini va Pending List sahifalarini ko'rish
SELECT 
    pages,
    empty_pages,
    pending_pages,
    pending_tuples
FROM gin_stat_page('idx_catalog_gin_fast', 0);

-- 4. Muammo: Pending List tozalanishi birinchi SELECT so'rovi gardaniga tushishi
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM product_search_catalog 
WHERE search_tokens @> ARRAY['smartfon', 'uzb_brand']
LIMIT 5;

-- 5. Profilaktik tozalash: Fon rejimida qo'lda yoki cron orqali tozalash
SELECT gin_clean_pending_list('idx_catalog_gin_fast') AS cleaned_pages;

-- 6. Tozalangandan so'ng Pending Pages holatini qayta tekshirish
SELECT 
    pages,
    pending_pages,
    pending_tuples
FROM gin_stat_page('idx_catalog_gin_fast', 0);
```
**Tushuntirish:** GIN indeksida har bir INSERT to'g'ridan-to'g'ri asosiy daraxtga yozilsa, disk Write Amplification dahshatli darajada oshadi. `fastupdate = on` yangilanishlarni oddiy ketma-ket sahifalarga (Pending list) saqlaydi. Ammo agar `gin_pending_list_limit` (standart 4MB) to'lsa, navbatdagi ixtiyoriy SELECT yoki `autovacuum` uni asosiy GIN tuzilmasiga kiritishga (vacuum/consolidate) majbur bo'ladi. Natijada foydalanuvchi so'rovi kutilmaganda 5000ms kutib qoladi. Sozlangan muhitda ushbu limit nazorat qilinadi va `gin_clean_pending_list()` funktsiyasi fon ishchisi tomonidan davriy chaqirilib, foydalanuvchi so'rovlariga xalaqit berilmaydi.
**Ishlash natijasi:**
```text
Tozalashdan oldingi holat:
 pages | empty_pages | pending_pages | pending_tuples 
-------+-------------+---------------+----------------
   412 |           2 |           148 |          50000
(Pending ro'yxatda 50,000 ta yozuv to'planib qolgan)

gin_clean_pending_list:
 cleaned_pages 
---------------
           148
(1 row)

Tozalangandan keyin: pending_pages = 0, so'rov kechikishi 1.1ms ga tushdi!
```

---

### Topshiriq #1274: GiST (Generalized Search Tree) yordamida Range (tsrange / daterange) kesishishlarini tezlashtirish
**Tavsif:** Mehmonxona va transport bron qilish xizmatida xonalar yoki avtomobillarning band qilingan vaqt oralig'i (`tsrange` yoki `tstzrange`) saqlanadi. Foydalanuvchi ma'lum bir sana oralig'ini qidirganda (`WHERE booking_period && '[2026-12-01, 2026-12-10]'::tstzrange`), an'anaviy B+Tree diapazonlarning o'zaro kesishishini (overlap `&&`) indekslay olmaydi. Seq Scan natijasida 5 millionlik bron jadvalida har bir qidiruv serverni qotirib qo'ymoqda.
**Talablar:** GiST indeksini yaratish, Range operatorlari (`&&`, `@>`, `<@`) uchun qidiruvni optimallashtirish va `Index Scan` orqali so'rovni 2ms da bajarish.
**Yechim (SQL):**
```sql
-- 1. Bron qilish jadvali
CREATE TABLE IF NOT EXISTS hotel_room_reservations (
    reservation_id BIGSERIAL PRIMARY KEY,
    room_id INT NOT NULL,
    guest_name VARCHAR(100) NOT NULL,
    booking_period TSTZRANGE NOT NULL
);

-- 100,000 ta namunaviy bron oralig'ini yuklash
INSERT INTO hotel_room_reservations (room_id, guest_name, booking_period)
SELECT 
    (i % 200) + 1,
    'Mehmon ' || i,
    tstzrange(
        '2026-06-01 12:00:00+00'::TIMESTAMPTZ + (i * 4 || ' hours')::INTERVAL,
        '2026-06-01 12:00:00+00'::TIMESTAMPTZ + (i * 4 + 48 || ' hours')::INTERVAL,
        '[)'
    )
FROM generate_series(1, 100000) AS i;

ANALYZE hotel_room_reservations;

-- 2. GiST indeksi bo'lmagandagi qidiruv (Seq Scan qimmatga tushadi)
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM hotel_room_reservations
WHERE booking_period && tstzrange('2026-07-15 10:00:00+00', '2026-07-20 18:00:00+00');

-- 3. GiST (Generalized Search Tree) indeksini yaratish
CREATE INDEX IF NOT EXISTS idx_reservations_gist_period 
ON hotel_room_reservations USING GIST (booking_period);

-- 4. GiST indeksi orqali kesishish (Overlap &&) qidiruvi
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM hotel_room_reservations
WHERE booking_period && tstzrange('2026-07-15 10:00:00+00', '2026-07-20 18:00:00+00');

-- 5. Range ichiga to'liq kirishini (@>) tekshirish
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM hotel_room_reservations
WHERE booking_period @> '2026-07-16 12:00:00+00'::TIMESTAMPTZ;
```
**Tushuntirish:** B+Tree faqat bir o'lchovli qat'iy skalyar qiymatlarni (`<`, `=`, `>`) saralay oladi. Diapazonlar (Ranges) esa ikki o'lchovli xususiyatga ega: boshlanish va tugash chegaralari mavjud. GiST (Generalized Search Tree) daraxti ierarxik to'rtburchaklar yoki chegaralovchi qutilar (Bounding Boxes / Lossy representations) asosida ishlaydi. U daraxt tugunlarida oraliqlarning eng kichik qamrovchi diapazonini (Union range) saqlaydi. So'rov berilganda, qidirilayotgan oraliq bilan kesishmaydigan barcha butun daraxt shoxlari bitta tekshiruvdayoq chetlab o'tiladi.
**Ishlash natijasi:**
```text
GiST indeksisiz:
Seq Scan on hotel_room_reservations (actual time=0.082..28.410 rows=48 loops=1)
  Filter: (booking_period && '["2026-07-15 10:00:00+00","2026-07-20 18:00:00+00")'::tstzrange)
  Buffers: shared hit=1250
Execution Time: 29.120 ms

GiST indeksi bilan:
Index Scan using idx_reservations_gist_period on hotel_room_reservations (actual time=0.041..0.120 rows=48 loops=1)
  Index Cond: (booking_period && '["2026-07-15 10:00:00+00","2026-07-20 18:00:00+00")'::tstzrange)
  Buffers: shared hit=8
Execution Time: 0.180 ms (160 barobar tezroq!)
```

---

### Topshiriq #1275: GiST indeksida B-Tree Exclusion Constraint (No-overlapping reservation) yaratish
**Tavsif:** Real bron qilish tizimlarida bitta xonaga ayni bir vaqtda ikkita mijoz buyurtma berib qo'yishi ("Double Booking" poygasi / Race condition) eng xavfli biznes anomaliyasi hisoblanadi. Dastur darajasidagi tekshiruvlar parallel tranzaksiyalarda (masalan, ikkita so'rov bir millisekundda kelganda) o'tkazib yuboradi. Baza darajasida buni kafolatlash uchun oddiy `UNIQUE` yetarli emas, chunki vaqtlar to'liq teng bo'lmasdan, qisman kesishishi mumkin. GiST va `btree_gist` kengaytmasi orqali Exclusion Constraint qurish talab qilinadi.
**Talablar:** `btree_gist` kengaytmasini ulash, `EXCLUDE USING gist (room_id WITH =, booking_period WITH &&)` cheklovini joriy qilish, Race Condition'ni 100% baza darajasida to'sish.
**Yechim (SQL):**
```sql
-- 1. btree_gist kengaytmasini faollashtirish (Oddiy skalyar turlarni GiST da ishlatish imkonini beradi)
CREATE EXTENSION IF NOT EXISTS btree_gist;

-- 2. Exclusion Constraint bilan himoyalangan jadval
CREATE TABLE IF NOT EXISTS conference_hall_bookings (
    booking_id BIGSERIAL PRIMARY KEY,
    hall_id INT NOT NULL,
    organizer_name VARCHAR(100) NOT NULL,
    booked_slot TSTZRANGE NOT NULL,
    -- GiST cheklovi: Aynan bir xil hall_id uchun booked_slot hech qachon bir-biri bilan kesishmasin (&&)!
    CONSTRAINT exclude_hall_schedule_conflict 
    EXCLUDE USING gist (
        hall_id WITH =,
        booked_slot WITH &&
    )
);

-- 3. Birinchi muvaffaqiyatli bron
INSERT INTO conference_hall_bookings (hall_id, organizer_name, booked_slot)
VALUES (
    101, 
    'Khorazmiy AI Meetup', 
    tstzrange('2026-11-14 10:00:00+00', '2026-11-14 13:00:00+00', '[)')
);

-- 4. Boshqa zal uchun ayni shu vaqtga bron (Muvaffaqiyatli o'tadi, chunki hall_id boshqa)
INSERT INTO conference_hall_bookings (hall_id, organizer_name, booked_slot)
VALUES (
    102, 
    'Startup Pitch Day', 
    tstzrange('2026-11-14 10:00:00+00', '2026-11-14 13:00:00+00', '[)')
);

-- 5. Parallel poyga (Race condition) simulyatsiyasi: 101-zalga qisman kesishuvchi vaqtda bron qilishga urinish
-- Ushbu INSERT xato berishi shart!
DO $$
BEGIN
    INSERT INTO conference_hall_bookings (hall_id, organizer_name, booked_slot)
    VALUES (
        101, 
        'Noqonuniy Ikkinchi Bron', 
        tstzrange('2026-11-14 12:00:00+00', '2026-11-14 15:00:00+00', '[)')
    );
EXCEPTION WHEN exclusion_violation THEN
    RAISE NOTICE 'Xavfsizlik tizimi ishladi: Double Booking qat''iy to''xtatildi! Xato: %', SQLERRM;
END $$;

-- 6. Yaratilgan GiST indeksining rejalashtiruvchiga xizmat qilishi
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM conference_hall_bookings
WHERE hall_id = 101 
  AND booked_slot && tstzrange('2026-11-14 11:00:00+00', '2026-11-14 12:00:00+00');
```
**Tushuntirish:** Standart `UNIQUE` cheklovi faqat qat'iy tenglikni (`=`) tekshiradi. Ammo vaqt oraliqlarida bitta bron 10:00 dan 13:00 gacha, ikkinchisi 12:00 dan 15:00 gacha bo'lsa, ularning tengligi FALSE, lekin kesishishi (`&&`) TRUE bo'ladi. PostgreSQL `EXCLUDE USING gist` mexanizmi har bir yangi qator kiritilayotganda yoki yangilanayotganda GiST daraxti orqali zudlik bilan predikatlar to'qnashuvini tekshiradi. Agar ziddiyat topilsa, tranzaksiya atomik tarzda `exclusion_violation` bilan bekor qilinadi. Bu tizimni dasturchilar xatosidan va parallel qulflanish poygalaridan 100% himoya qiladi.
**Ishlash natijasi:**
```text
psql:exclusion_violation_catch
NOTICE:  Xavfsizlik tizimi ishladi: Double Booking qat'iy to'xtatildi! Xato: conflicting key value violates exclusion constraint "exclude_hall_schedule_conflict"
DETAIL:  Key (hall_id, booked_slot)=(101, ["2026-11-14 12:00:00+00","2026-11-14 15:00:00+00")) conflicts with existing key (hall_id, booked_slot)=(101, ["2026-11-14 10:00:00+00","2026-11-14 13:00:00+00")).
```

---

### Topshiriq #1276: Partial (Shartli) Indekslar orqali indeks hajmini 95% ga qisqartirish va Active Queue so'rovlarini tezlashtirish
**Tavsif:** To'lovlar tizimida kuniga 10 millionta to'lov qayta ishlanadi. Ularning 99.5% i muvaffaqiyatli yakunlanadi (`status = 'COMPLETED'`) va faqat 0.5% i navbatda yoki xatolikda turadi (`status IN ('PENDING', 'PROCESSING', 'RETRY')`). Navbatni ishlovchi Background Worker doimiy ravishda `WHERE status = 'PENDING'` so'rovini beradi. Agar `status` ustuniga to'liq B+Tree indeksi qurilsa, indeks 10 million qatorni saqlab 300 MB joy oladi. Ushbu indeksni faqat 0.5% qatorlarni qamrab oluvchi Partial Index ga aylantirish kerak.
**Talablar:** Shartli qisman indeks (`WHERE status != 'COMPLETED'`) yaratish, indeks hajmini 300 MB dan 2 MB ga tushirish, INSERT operatsiyalaridagi indeks yuklamasini 99% ga kamaytirish.
**Yechim (SQL):**
```sql
-- 1. Tranzaksion to'lovlar jadvali
CREATE TABLE IF NOT EXISTS payment_dispatch_queue (
    payment_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    amount NUMERIC(14, 2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

-- 500,000 ta to'lov yozuvi (99% COMPLETED, 1% PENDING)
INSERT INTO payment_dispatch_queue (user_id, amount, status)
SELECT 
    (random() * 100000)::BIGINT,
    (random() * 500)::NUMERIC(14, 2),
    CASE WHEN i <= 495000 THEN 'COMPLETED' ELSE 'PENDING' END
FROM generate_series(1, 500000) AS i;

-- 2. Noo'rin: To'liq indeks (Full B+Tree Index)
CREATE INDEX IF NOT EXISTS idx_full_payments_status 
ON payment_dispatch_queue (status, created_at);

-- 3. Tavsiya etiladigan: Partial Index (Faqat faol navbat uchun!)
CREATE INDEX IF NOT EXISTS idx_partial_payments_pending 
ON payment_dispatch_queue (created_at) 
WHERE status = 'PENDING';

-- 4. Hajmlarni solishtirish
SELECT 
    relname,
    pg_size_pretty(pg_relation_size(oid)) AS index_size,
    pg_relation_size(oid) AS raw_bytes
FROM pg_class
WHERE relname IN ('idx_full_payments_status', 'idx_partial_payments_pending');

-- 5. Rejalashtiruvchining Partial Index'dan foydalanishini tekshirish
EXPLAIN (ANALYZE, BUFFERS)
SELECT payment_id, user_id, amount, created_at
FROM payment_dispatch_queue
WHERE status = 'PENDING'
ORDER BY created_at ASC
LIMIT 100;
```
**Tushuntirish:** Ko'p sonli yozuvlar mavjud bo'lgan, ammo ularning oz qismigina tez-tez so'raladigan tizimlarda to'liq indeks qurish resurs isrofidir. To'liq indeks har bir INSERT/UPDATE paytida barcha 10 million qator uchun yangilanadi. `WHERE status = 'PENDING'` sharti bilan yaratilgan Partial Index faqat shartni qanoatlantiruvchi qatorlar kiritilgandagina o'zgaradi. `status = 'COMPLETED'` bo'lgan 99.5% yozuvlar indeksga kiritilmaydi. Bu nafaqat indeks hajmini 98% ga qisqartiradi, balki keshni bo'shatadi va INSERT operatsiyalarini sezilarli darajada tezlashtiradi.
**Ishlash natijasi:**
```text
           relname            | index_size | raw_bytes 
------------------------------+------------+-----------
 idx_full_payments_status     | 16 MB      |  16777216
 idx_partial_payments_pending | 160 kB     |    163840
(Partial Index 100 barobar kichik!)

Reja tahlili:
->  Index Scan using idx_partial_payments_pending on payment_dispatch_queue (cost=0.28..12.45 rows=100)
    Buffers: shared hit=4
Execution Time: 0.082 ms
```

---

### Topshiriq #1277: Funksional va Expression Indekslar (Lower, JSONB extractor, MD5) orqali Seq Scan'ni yo'qotish
**Tavsif:** Foydalanuvchilarni autentifikatsiya qilish tizimida foydalanuvchilar o'z elektron pochtalarini har xil registrda (`User@Test.UZ`, `USER@TEST.UZ`) kiritishadi. Dasturchilar so'rovda `WHERE LOWER(email) = LOWER('input')` deb yozganlar. Natijada `email` ustunidagi mavjud B+Tree indeksi ishlamayapti va har bir login so'rovi 5 millionlik jadvalni boshdan oyoq skan qilib (Seq Scan), bazani qizdirib yubormoqda.
**Talablar:** Funksional ifodali indeks (Expression Index) yaratish, B+Tree funksiya chaqiruvlarini indekslash qoidalarini joriy qilish va so'rovni 0.1ms ga tushirish.
**Yechim (SQL):**
```sql
-- 1. Foydalanuvchilar jadvali
CREATE TABLE IF NOT EXISTS auth_users_accounts (
    account_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    security_hash VARCHAR(64) NOT NULL,
    profile_data JSONB NOT NULL
);

-- 200,000 ta foydalanuvchi ma'lumotlarini yuklash
INSERT INTO auth_users_accounts (username, email, security_hash, profile_data)
SELECT 
    'Foydalanuvchi_' || i,
    'User_' || i || '@Khorazmiy.UZ',
    md5(i::text),
    jsonb_build_object('tax_code', 'UZ' || LPAD(i::text, 9, '0'))
FROM generate_series(1, 200000) AS i;

-- Standart ustun indeksi (LOWER() chaqirilganda ISHLAMAYDI)
CREATE INDEX IF NOT EXISTS idx_users_email_regular ON auth_users_accounts (email);
ANALYZE auth_users_accounts;

-- 2. Muammoli so'rov: Seq Scan ko'rinishi
EXPLAIN (ANALYZE, BUFFERS)
SELECT account_id, username, email
FROM auth_users_accounts
WHERE LOWER(email) = 'user_12345@khorazmiy.uz';

-- 3. Expression Index 1: Kichik harfli email bo'yicha
CREATE INDEX IF NOT EXISTS idx_users_email_lower 
ON auth_users_accounts (LOWER(email));

-- 4. Expression Index 2: JSONB ichki maydoni bo'yicha to'g'ridan-to'g'ri indeks
CREATE INDEX IF NOT EXISTS idx_users_profile_tax_code 
ON auth_users_accounts ((profile_data->>'tax_code'));

-- 5. Optimallashgan qidiruv tahlili
EXPLAIN (ANALYZE, BUFFERS)
SELECT account_id, username, email
FROM auth_users_accounts
WHERE LOWER(email) = 'user_12345@khorazmiy.uz';

-- 6. JSONB maydoni bo'yicha qidiruv tahlili
EXPLAIN (ANALYZE, BUFFERS)
SELECT account_id, username
FROM auth_users_accounts
WHERE profile_data->>'tax_code' = 'UZ000012345';
```
**Tushuntirish:** B+Tree indeksi ustundagi asl qiymatlarni saralangan holda saqlaydi. Agar SQL so'rovida ustun ustida biron bir funksiya chaqirilsa (`LOWER(col)`, `DATE_TRUNC('day', col)`, `col->>'key'`), rejalashtiruvchi indeksdagi qiymat bilan qidirilayotgan qiymatni to'g'ridan-to'g'ri taqqoslay olmaydi va majburan to'liq jadval skaniga (Seq Scan) tushadi. Expression Index yaratilganda PostgreSQL jadvalga qator yozilayotganda ushbu funksiyani bajaradi va natijasini B+Tree barglariga yozib qo'yadi. So'rovda aynan shu ifoda ishlatilganda rejalashtiruvchi darhol `Index Scan` ni tanlaydi.
**Ishlash natijasi:**
```text
Expression indeksdan oldin:
->  Seq Scan on auth_users_accounts (actual time=0.045..38.120 rows=1 loops=1)
      Filter: (lower((email)::text) = 'user_12345@khorazmiy.uz'::text)
      Buffers: shared hit=2840
Execution Time: 38.850 ms

Expression indeksdan so'ng:
->  Index Scan using idx_users_email_lower on auth_users_accounts (actual time=0.038..0.040 rows=1 loops=1)
      Index Cond: (lower((email)::text) = 'user_12345@khorazmiy.uz'::text)
      Buffers: shared hit=3
Execution Time: 0.075 ms (500 barobar tezroq!)
```

---

### Topshiriq #1278: PostgreSQL 13+ B-Tree Index Deduplication imkoniyatidan foydalanib indeks hajmini siqish
**Tavsif:** Logistika tizimida millionlab yuk xatlari saqlanadi. Jadvalning `order_status` yoki `warehouse_id` kabi past kardinallikli (low-cardinality) ustunlariga B+Tree indeksi qurilganda, indeks sahifalarida bir xil kalitlar minglab marta takrorlanadi va disk xotirasini haddan tashqari shishiradi. PostgreSQL 13 versiyasidan boshlab joriy etilgan B-Tree Deduplication mexanizmi dublikat kalitlarni bitta Posting List'ga birlashtirish orqali indeks hajmini sezilarli darajada siqadi.
**Talablar:** Deduplication yoqilgan va o'chirilgan indekslarni taqqoslash, `amcheck` orqali tekshirish va indeks hajmini 3 barobarga qisqartirish.
**Yechim (SQL):**
```sql
-- 1. Yuk tashish logistika jadvali
CREATE TABLE IF NOT EXISTS shipment_waybills (
    waybill_id BIGSERIAL PRIMARY KEY,
    carrier_id INT NOT NULL,
    current_status VARCHAR(50) NOT NULL,
    destination_city VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

-- 500,000 ta yozuv (Faqat 5 xil status va 10 ta shahar)
INSERT INTO shipment_waybills (carrier_id, current_status, destination_city)
SELECT 
    (i % 50) + 1,
    (ARRAY['CREATED', 'IN_TRANSIT', 'CUSTOMS', 'DELIVERED', 'RETURNED'])[floor(random()*5 + 1)],
    (ARRAY['Toshkent', 'Samarqand', 'Buxoro', 'Xiva', 'Andijon', 'Namangan', 'Nukus', 'Qarshi', 'Termiz', 'Farg''ona'])[floor(random()*10 + 1)]
FROM generate_series(1, 500000) AS i;

-- 2. Deduplication o'chirilgan an'anaviy indeks (Eski PG versiyalari uslubida)
CREATE INDEX IF NOT EXISTS idx_shipments_nodedup 
ON shipment_waybills (current_status, destination_city) 
WITH (deduplicate_items = OFF);

-- 3. PostgreSQL 13+ Deduplication yoqilgan zamonaviy indeks
CREATE INDEX IF NOT EXISTS idx_shipments_dedup 
ON shipment_waybills (current_status, destination_city) 
WITH (deduplicate_items = ON);

-- 4. Indekslar hajmi va diskdagi sahifalar sonini solishtirish
SELECT 
    relname,
    pg_size_pretty(pg_relation_size(oid)) AS index_size,
    pg_relation_size(oid) AS raw_bytes,
    relpages AS page_blocks_count
FROM pg_class
WHERE relname IN ('idx_shipments_nodedup', 'idx_shipments_dedup');

-- 5. Indeksning to'g'ri ishlashi va qidiruv samaradorligi tahlili
EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*) 
FROM shipment_waybills
WHERE current_status = 'IN_TRANSIT' AND destination_city = 'Samarqand';
```
**Tushuntirish:** Standart B+Tree indeksining barg sahifalarida (Leaf Pages) har bir qator uchun `IndexTuple` saqlanadi: `[Key_Value, ItemPointer(page, offset)]`. Agar `current_status = 'DELIVERED'` qiymatiga ega 100,000 ta qator bo'lsa, har bir yozuvda 'DELIVERED' so'zi qayta-qayta yozilib, 8KB sahifani to'ldiradi. B-Tree Deduplication yoqilganda, bitta unikal kalit yoziladi va uning orqasidan barcha mos qatorlarning pointerlari massivi (Posting List) ulab qo'yiladi. Natijada takrorlanuvchi kalitlar siqilib, indeks hajmi 60-75% ga kamayadi, keshda kamroq joy egallaydi va qidiruv tezlashadi.
**Ishlash natijasi:**
```text
        relname         | index_size | raw_bytes | page_blocks_count 
------------------------+------------+-----------+-------------------
 idx_shipments_nodedup  | 14 MB      |  14680064 |              1792
 idx_shipments_dedup    | 4680 kB    |   4792320 |               585
(3 barobar toza xotira tejaldi!)

Tahlil: Dedup indeksi keshdan atigi 3 ta sahifa o'qidi, Buffer Hit ko'rsatkichi 100%.
```

---

### Topshiriq #1279: PostgreSQL Bloom Index kengaytmasi bilan ko'p ustunli kombinatsiyaviy filtrlarni indekslash
**Tavsif:** Foydalanuvchilar qidiruv panelida 10 xil filtr mavjud (rangi, o'lchami, ishlab chiqaruvchi, kafolat muddati, kategoriya va hk). Foydalanuvchilar ixtiyoriy 2 yoki 3 ta filtr kombinatsiyasini tanlashadi. Barcha kombinatsiyalar uchun alohida B+Tree indekslari yaratilsa, 50 dan ortiq indeks kerak bo'ladi va bu yozish operatsiyalarini butunlay falaj qiladi. `bloom` indeksi ehtimollik filtri (probabilistic data structure) asosida barcha ustunlarni bitta kichik indeksda saqlash imkonini beradi.
**Talablar:** `bloom` kengaytmasini o'rnatish, 6 ustunli Bloom indeksini yaratish, har xil filtr kombinatsiyalarida Bitmap Index Scan orqali so'rovlarni optimallashtirish.
**Yechim (SQL):**
```sql
-- 1. Bloom kengaytmasini faollashtirish
CREATE EXTENSION IF NOT EXISTS bloom;

-- 2. Ko'p atributli tovarlar jadvali
CREATE TABLE IF NOT EXISTS product_multisearch (
    product_id BIGSERIAL PRIMARY KEY,
    category_id INT NOT NULL,
    brand_id INT NOT NULL,
    color_code VARCHAR(20) NOT NULL,
    size_code VARCHAR(10) NOT NULL,
    voltage_rating INT NOT NULL,
    is_eco_friendly BOOLEAN NOT NULL
);

-- 200,000 ta kombinatsiyaviy tovar yuklash
INSERT INTO product_multisearch (category_id, brand_id, color_code, size_code, voltage_rating, is_eco_friendly)
SELECT 
    (i % 50) + 1,
    (i % 100) + 1,
    (ARRAY['Qora', 'Oq', 'Ko''k', 'Qizil', 'Kulrang'])[floor(random()*5 + 1)],
    (ARRAY['S', 'M', 'L', 'XL', 'XXL'])[floor(random()*5 + 1)],
    (ARRAY[110, 220, 380])[floor(random()*3 + 1)],
    (i % 2 = 0)
FROM generate_series(1, 200000) AS i;

ANALYZE product_multisearch;

-- 3. Barcha 6 ta ustun bo'yicha bitta Bloom indeksi qurish
CREATE INDEX IF NOT EXISTS idx_bloom_multisearch 
ON product_multisearch USING bloom (category_id, brand_id, color_code, size_code, voltage_rating, is_eco_friendly)
WITH (col1=2, col2=2, col3=4, col4=4, col5=2, col6=1);

-- 4. Ixtiyoriy kombinatsiya 1: Kategoriya va Rang bo'yicha qidiruv
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM product_multisearch
WHERE category_id = 15 AND color_code = 'Qora';

-- 5. Ixtiyoriy kombinatsiya 2: Brend, O'lcham va Kuchlanish bo'yicha qidiruv
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM product_multisearch
WHERE brand_id = 42 AND size_code = 'XL' AND voltage_rating = 220;
```
**Tushuntirish:** Bloom filtri xesh-funksiyalar asosida ishlaydigan ehtimollik strukturasidir. Bloom indeksi har bir qatorning belgilangan ustunlari xeshini bitlar massivida (Bit Array) saqlaydi. So'rovda 6 ta ustundan qaysi biri qatnashishidan qat'i nazar, Bloom indeksi so'ralgan qiymatlarning bitlarini tekshiradi. U hech qachon "False Negative" bermaydi (ya'ni kerakli qatorni tashlab yubormaydi), lekin "False Positive" berishi mumkin (mos kelmaydigan qatorni kiritishi mumkin). Shuning uchun PostgreSQL `Bitmap Index Scan` dan so'ng har doim `Recheck Cond` bosqichini bajaradi. Natijada o'nlab B+Tree indekslari o'rniga bitta tejamkor indeks barcha filtrlarni samarali yopadi.
**Ishlash natijasi:**
```text
Kombinatsiya 1 rejasi:
->  Bitmap Heap Scan on product_multisearch (actual time=0.812..3.120 rows=800 loops=1)
      Recheck Cond: ((category_id = 15) AND ((color_code)::text = 'Qora'::text))
      Rows Removed by Index Recheck: 12
      Buffers: shared hit=410
      ->  Bitmap Index Scan on idx_bloom_multisearch (actual time=0.745..0.745 rows=812 loops=1)
Execution Time: 3.450 ms (Barcha turdagi kombinatsiyalarda barqaror ishlaydi!)
```

---

### Topshiriq #1280: R-Tree va Quad-Tree arxitekturasi: GiST Spatial k-NN (`<->` operatori) masofaviy qidiruvni optimallashtirish
**Tavsif:** Taksi agregatori xizmatida (Ride-hailing) har daqiqada minglab mijozlar buyurtma beradi. Mijoz koordinatasiga eng yaqin bo'lgan 5 ta faol haydovchini topish kerak (`ORDER BY location <-> point(...) LIMIT 5`). Dasturchilar oddiy Evklid masofasi formulasini `ORDER BY sqrt(pow(lat1-lat2,2) + ...)` deb yozganliklari sababli tizim barcha 500,000 haydovchini saralab chiqmoqda va so'rov 800ms vaqt olmoqda. GiST k-NN (k-Nearest Neighbors) operatori orqali qidiruvni 1ms dan pastga tushirish zarur.
**Talablar:** Geometrik nuqtalar (`POINT`) ustida GiST indeksini yaratish, `<->` masofa operatoridan foydalanish, `Index Scan` orqali to'g'ridan-to'g'ri eng yaqin 5 qo'shnini topish.
**Yechim (SQL):**
```sql
-- 1. Haydovchilar geolokatsiyasi jadvali
CREATE TABLE IF NOT EXISTS taxi_driver_coordinates (
    driver_id BIGINT PRIMARY KEY,
    driver_phone VARCHAR(20) NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    current_pos POINT NOT NULL
);

-- Toshkent shahri bo'ylab 100,000 ta koordinata generatsiya qilish
INSERT INTO taxi_driver_coordinates (driver_id, driver_phone, is_available, current_pos)
SELECT 
    i,
    '+99890' || LPAD(i::text, 7, '0'),
    (i % 3 = 0),
    point(41.2500 + (random() * 0.1500), 69.2000 + (random() * 0.1500))
FROM generate_series(1, 100000) AS i;

-- 2. Geometrik ustun ustida GiST indeksi yaratish (R-Tree / Bounding Box)
CREATE INDEX IF NOT EXISTS idx_taxi_pos_gist 
ON taxi_driver_coordinates USING GIST (current_pos);

ANALYZE taxi_driver_coordinates;

-- 3. Muammoli so'rov: Matematik hisoblash orqali to'liq saralash (Seq Scan + Sort)
EXPLAIN (ANALYZE, BUFFERS)
SELECT driver_id, current_pos
FROM taxi_driver_coordinates
ORDER BY current_pos <-> point(41.2995, 69.2401)
LIMIT 5;

-- 4. Qisman GiST indeksi (Faqat bo'sh haydovchilar uchun k-NN)
CREATE INDEX IF NOT EXISTS idx_taxi_available_pos_gist 
ON taxi_driver_coordinates USING GIST (current_pos)
WHERE is_available = TRUE;

-- 5. Faol haydovchilarni eng yaqin masofa bo'yicha qidirish
EXPLAIN (ANALYZE, BUFFERS)
SELECT driver_id, driver_phone, current_pos, 
       (current_pos <-> point(41.2995, 69.2401)) AS distance_approx
FROM taxi_driver_coordinates
WHERE is_available = TRUE
ORDER BY current_pos <-> point(41.2995, 69.2401)
LIMIT 5;
```
**Tushuntirish:** Fazoviy (Spatial) qidiruvlarda oddiy B+Tree ishlamaydi, chunki tekislikda nuqtalar 2 o'lchamli bo'lib, bir vaqtning o'zida ham kenglik (lat), ham uzunlik (lng) bo'yicha tartiblash talab qilinadi. GiST R-Tree (Rectangle Tree) arxitekturasida nuqtalarni o'z ichiga olgan ierarxik to'rtburchaklar (Bounding Boxes) hosil qiladi. PostgreSQL GiST k-NN implementatsiyasida Ustunlik Navbati (Priority Queue) algoritmidan foydalanadi: qidiruv berilgan nuqtadan markazga qarab to'lqin kabi tarqaladi va eng yaqin to'rtburchaklar birinchi ochiladi. Kerakli 5 ta haydovchi topilishi bilan qidiruv to'xtaydi ($O(\log N)$). 100,000 qatorni skan qilish o'rniga atigi 5-10 ta sahifa o'qiladi.
**Ishlash natijasi:**
```text
k-NN GiST orqali natija:
->  Limit  (cost=0.28..1.12 rows=5 width=48) (actual time=0.048..0.065 rows=5 loops=1)
      ->  Index Scan using idx_taxi_available_pos_gist on taxi_driver_coordinates (actual time=0.045..0.061 rows=5 loops=1)
            Order By: (current_pos <-> '(41.2995,69.2401)'::point)
            Buffers: shared hit=4
Execution Time: 0.089 ms (800ms dan 0.08ms ga tushdi - 9000x tezlashish!)
```


---

### Topshiriq #1281: PostgreSQL MVCC arxitekturasi: `xmin`, `xmax`, `cmin`, `cmax` tahlili va Snapshot Isolation
**Tavsif:** Real vaqt rejimida yuz minglab tranzaksiyalar ishlayotganda o'quvchi so'rovlar yozuvchilarga, yozuvchi so'rovlar esa o'quvchilarga to'sqinlik qilmasligi kerak (Readers don't block Writers, Writers don't block Readers). PostgreSQL bu xususiyatni Multi-Version Concurrency Control (MVCC) orqali amalga oshiradi. Har bir qatorning jismoniy sarlavhasida maxfiy tizim ustunlari (`xmin`, `xmax`, `cmin`, `cmax`, `ctid`) saqlanadi. Tranzaksiya qanday qilib o'z snapshot'iga qarab qaysi versiyani ko'rishi yoki ko'rmasligini tahlil qilish zarur.
**Talablar:** Yashirin tizim ustunlarini o'rganish, qator yangilanganda yaratiladigan versiyalarni kuzatish, Snapshot Isolation qoidalarini amalda isbotlash.
**Yechim (SQL):**
```sql
-- 1. MVCC mexanizmini o'rganish uchun test jadvali
CREATE TABLE IF NOT EXISTS mvcc_account_ledger (
    acc_id INT PRIMARY KEY,
    owner_name VARCHAR(50) NOT NULL,
    balance NUMERIC(12, 2) NOT NULL
);

-- Boshlang'ich qatorni kiritish
INSERT INTO mvcc_account_ledger (acc_id, owner_name, balance)
VALUES (1, 'Alisher', 1000.00);

-- 2. Tizim ustunlarini tekshirish (xmin, xmax, cmin, cmax, ctid)
SELECT 
    ctid,
    xmin,
    xmax,
    cmin,
    cmax,
    acc_id,
    balance
FROM mvcc_account_ledger
WHERE acc_id = 1;

-- 3. UPDATE operatsiyasi bajaramiz (MVCC yangi versiya yaratadi)
UPDATE mvcc_account_ledger 
SET balance = balance + 500.00 
WHERE acc_id = 1;

-- 4. Yangilanishdan so'ng xmin, xmax va ctid ning o'zgarishini ko'rish
-- ctid (0, 1) dan (0, 2) ga o'tadi, xmax ga eski tranzaksiya ID yoziladi
SELECT 
    ctid,
    xmin,
    xmax,
    acc_id,
    balance
FROM mvcc_account_ledger
WHERE acc_id = 1;

-- 5. Sahifadagi barcha (faol va o'lik) versiyalarni ko'rish (pageinspect orqali)
SELECT 
    lp, 
    lp_off, 
    lp_len, 
    t_xmin, 
    t_xmax, 
    t_ctid 
FROM heap_page_items(get_raw_page('mvcc_account_ledger', 0));
```
**Tushuntirish:** PostgreSQL'da qator UPDATE qilinganda mavjud qator joyida o'zgartirilmaydi. Buning o'rniga:
1. Eski qatorning `xmax` ustuniga yangilashni amalga oshirgan tranzaksiya ID si yoziladi (bu eski qator mazkur tranzaksiyadan keyin "o'lik" ekanini bildiradi).
2. Yangi qator (yangi versiya) sahifaning bo'sh joyiga yoziladi, uning `xmin` ustuniga joriy tranzaksiya ID si qo'yiladi, `xmax` esa 0 bo'ladi.
3. Yangi so'rov kelganda, uning "Snapshot"i (faol tranzaksiyalar ro'yxati) tekshiriladi: agar `xmin` snapshot yaratilishidan oldin commit bo'lgan bo'lsa va `xmax` hali commit bo'lmagan bo'lsa, ushbu versiya o'qiladi. Bu mexanizm qulflarsiz izolyatsiyani ta'minlaydi.
**Ishlash natijasi:**
```text
Dastlabki holat:
  ctid |  xmin   | xmax | acc_id | balance 
-------+---------+------+--------+---------
 (0,1) | 1052401 |    0 |      1 | 1000.00

UPDATE dan keyingi holat:
  ctid |  xmin   | xmax | acc_id | balance 
-------+---------+------+--------+---------
 (0,2) | 1052402 |    0 |      1 | 1500.00

heap_page_items ko'rinishi:
 lp | t_xmin  | t_xmax  | t_ctid 
----+---------+---------+--------
  1 | 1052401 | 1052402 | (0,2)   <-- Eski qator o'lik, yangisiga havola bermoqda!
  2 | 1052402 |       0 | (0,2)   <-- Yangi tirik qator.
```

---

### Topshiriq #1282: Table Bloat va Dead Tuples tahlili: `pgstattuple` orqali jadvallardagi o'lik yozuvlar hajmini aniqlash
**Tavsif:** Yuqori yuklamali buyurtmalar bazasida har kuni yuz minglab yozuvlar o'chiriladi va yangilanadi. Natijada `orders` jadvalining hajmi 50 GB ga yetgan, holbuki undagi real tirik ma'lumotlar bor-yo'g'i 10 GB ni tashkil etadi. Qolgan 40 GB bo'shliq "Dead Tuples" (o'lik qatorlar) va sahifa ichidagi bo'shliqlardan (Table Bloat) iborat. Bu disk I/O ni 5 barobarga oshirib, xotirani isrof qilmoqda. `pgstattuple` kengaytmasi orqali shishish darajasini aniq o'lchash va davolash talab qilinadi.
**Talablar:** `pgstattuple` yordamida `dead_tuple_percent` va `free_percent` ko'rsatkichlarini hisoblash, shishish darajasi 30% dan oshgan jadvallarni aniqlash.
**Yechim (SQL):**
```sql
-- 1. pgstattuple kengaytmasini ulash
CREATE EXTENSION IF NOT EXISTS pgstattuple;

-- 2. Sun'iy shishish (Bloat) keltirib chiqarish uchun test jadvali
CREATE TABLE IF NOT EXISTS bloated_orders_demo (
    order_id INT PRIMARY KEY,
    customer_id INT,
    status VARCHAR(20),
    notes TEXT
);

-- 100,000 qator kiritish
INSERT INTO bloated_orders_demo (order_id, customer_id, status, notes)
SELECT i, (i % 1000), 'NEW', repeat('Malumot qatori ', 10)
FROM generate_series(1, 100000) AS i;

-- 60,000 qatorni o'chiramiz va 30,000 tasini UPDATE qilamiz (O'lik qatorlar hosil qilish)
DELETE FROM bloated_orders_demo WHERE order_id <= 60000;
UPDATE bloated_orders_demo SET status = 'PROCESSED' WHERE order_id > 60000;

-- 3. pgstattuple orqali tirik va o'lik qatorlarni aniq hisoblash
SELECT 
    table_len AS total_table_bytes,
    pg_size_pretty(table_len) AS total_size,
    tuple_count AS live_tuples,
    tuple_percent AS live_tuple_pct,
    dead_tuple_count AS dead_tuples,
    dead_tuple_percent AS dead_tuple_pct,
    free_percent AS free_space_pct
FROM pgstattuple('bloated_orders_demo');

-- 4. Barcha foydalanuvchi jadvallaridagi Bloat foizini avtomatik tahlil qiluvchi so'rov
SELECT 
    schemaname,
    relname,
    n_live_tup,
    n_dead_tup,
    ROUND((n_dead_tup::NUMERIC / NULLIF(n_live_tup + n_dead_tup, 0)) * 100, 2) AS dead_tuple_ratio_pct,
    last_vacuum,
    last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- 5. Shishgan jadvalni tozalash va disk hajmini qaytarib olish (VACUUM FULL yoki pg_repack)
-- Izoh: Production tizimlarda jadval qulflanmasligi uchun pg_repack ishlatiladi
VACUUM (ANALYZE, VERBOSE) bloated_orders_demo;
```
**Tushuntirish:** PostgreSQL'da DELETE va UPDATE qilingan qatorlar darhol diskdan o'chirilmaydi; ular faqat boshqa tranzaksiyalarga ko'rinmaydigan qilib belgilanadi (Dead Tuples). Ushbu o'lik qatorlar `VACUUM` tomonidan bo'shatilib, yangi INSERT'lar uchun FSM (Free Space Map) ga qaytariladi. Biroq, agar `autovacuum` o'z vaqtida ulgurmasa, sahifalar shishib ketadi (Table Bloat). Oddiy `VACUUM` disk hajmini operatsion tizimga qaytarmaydi, faqat sahifa ichida qayta ishlatish uchun bo'shatadi. Disk hajmini to'liq OS ga qaytarish uchun `VACUUM FULL` (jadvalni to'liq qulflaydi) yoki `pg_repack` (onlayn qulflarsiz qayta quradi) zarur.
**Ishlash natijasi:**
```text
 total_size | live_tuples | live_tuple_pct | dead_tuples | dead_tuple_pct | free_space_pct 
------------+-------------+----------------+-------------+----------------+----------------
 24 MB      |       40000 |          32.14 |       90000 |          58.42 |           8.12
(1 row)

Tahlil: Jadvalning 58% hajmi o'lik qatorlardan iborat. Shishish (Bloat) kritik darajada.
VACUUM ANALYZE dan so'ng o'lik qatorlar bo'shatildi, dead_tuple_pct = 0.00%.
```

---

### Topshiriq #1283: Autovacuum Tuning: High-write jadvallarda `scale_factor` va `vacuum_cost_limit`ni sozlash
**Tavsif:** Real-vaqtli buyurtma berish xizmatida `order_events` jadvaliga sekundiga 2000 ta qator yoziladi va o'chiriladi. Standart PostgreSQL `autovacuum_vacuum_scale_factor = 0.2` (20%) qilib sozlangan. 10 millionlik jadvalda autovacuum ishga tushishi uchun kamida 2 million qator o'zgarishi kerak! Natijada autovacuum soatlab ishlamaydi, ishga tushganda esa `vacuum_cost_limit = 200` kuchi yetmay, 4 soatlab disk I/O ni ezadi. Autovacuum parametrlarini agressiv va tezkor qilib qayta sozlash zarur.
**Talablar:** Har bir jadval darajasida `autovacuum_vacuum_threshold` va `scale_factor` ni pasaytirish, `autovacuum_vacuum_cost_limit`ni 200 dan 2000 ga ko'tarish, kechikishlarni yo'qotish.
**Yechim (SQL):**
```sql
-- 1. Global autovacuum sozlamalarini tekshirish
SELECT name, setting, unit, short_desc 
FROM pg_settings 
WHERE name LIKE 'autovacuum%' OR name LIKE 'vacuum_cost%';

-- 2. Yuqori chastotali yozish jadvalini yaratish
CREATE TABLE IF NOT EXISTS high_frequency_order_events (
    event_id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL,
    event_payload JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- 3. Ushbu jadval uchun shaxsiy AGRESSIV Autovacuum sozlamalarini joriy qilish
-- 20% kutmasdan, 5,000 ta qator o'lishi bilanoq autovacuum ishga tushsin!
ALTER TABLE high_frequency_order_events SET (
    autovacuum_vacuum_threshold = 1000,
    autovacuum_vacuum_scale_factor = 0.01,         -- Atigi 1% o'zgarganda ishga tushadi
    autovacuum_vacuum_cost_limit = 2000,           -- 10 barobar ko'proq I/O kvotasi beriladi
    autovacuum_vacuum_cost_delay = 2,              -- Kutish kechikishi 20ms dan 2ms ga tushiriladi
    autovacuum_analyze_threshold = 500,
    autovacuum_analyze_scale_factor = 0.005
);

-- 4. Jadvalning o'rnatilgan parametrlarini tekshirish
SELECT 
    relname, 
    reloptions 
FROM pg_class 
WHERE relname = 'high_frequency_order_events';

-- 5. Autovacuum ishchi jarayonlarini monitoring qilish
SELECT 
    pid, 
    datname, 
    relid::regclass AS current_table_vacuuming, 
    phase, 
    heap_blks_total, 
    heap_blks_scanned, 
    heap_blks_vacuumed 
FROM pg_stat_progress_vacuum;
```
**Tushuntirish:** PostgreSQL Autovacuum mexanizmi xarajatlar modeli (`Cost-based vacuuming`) bo'yicha ishlaydi:
- Keshdagi sahifani o'qish: `vacuum_cost_page_hit = 1`
- Diskdan sahifani o'qish: `vacuum_cost_page_miss = 2`
- Iflos sahifani diskka yozish: `vacuum_cost_page_dirty = 20`
Har safar jami xarajat `autovacuum_vacuum_cost_limit` (standart 200) ga yetganda, jarayon `autovacuum_vacuum_cost_delay` (standart 2ms) vaqtga uxlaydi. Og'ir yuklamali tizimlarda bu limit juda kamlik qiladi va autovacuum o'lik qatorlarni tozalashga ulgurmaydi. Alohida faol jadvallarga `scale_factor = 0.01` va `cost_limit = 2000` berish orqali tozalash jarayoni bir necha daqiqada tugatiladi va jadval shishishiga yo'l qo'yilmaydi.
**Ishlash natijasi:**
```text
relname                    | reloptions
---------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------
high_frequency_order_events| {autovacuum_vacuum_threshold=1000,autovacuum_vacuum_scale_factor=0.01,autovacuum_vacuum_cost_limit=2000,autovacuum_vacuum_cost_delay=2}

Tahlil: Autovacuum endi har 10,000 o'lik qatordan so'ng darhol ishga tushadi va 2000 IOPS kuchi bilan 1.5 soniyada tozalaydi.
```

---

### Topshiriq #1284: Transaction ID (XID) Wraparound xavfi va `vacuumdb --freeze` yordamida falokatning oldini olish
**Tavsif:** PostgreSQL da tranzaksiya identifikatorlari (`txid`) 32-bitli butun son bo'lib, maksimal 4.2 milliard tranzaksiyani o'z ichiga oladi. Agar ma'lumotlar bazasida 2 milliard tranzaksiya o'tib ketsa va eski qatorlar muzlatilmasa (`FREEZE`), PostgreSQL ma'lumotlar yo'qolishining oldini olish uchun bazani to'liq faqat o'qish (Read-Only) rejimiga o'tkazib favqulodda to'xtatadi (Catastrophic Shutdown). XID Wraparound xavfini monitoring qilish va qatorlarni xavfsiz muzlatish talab etiladi.
**Talablar:** `datfrozenxid` va `relfrozenxid` yoshini aniqlash, falokatga qancha tranzaksiya qolganini o'lchash, `FREEZE` jarayonini xavfsiz boshqarish.
**Yechim (SQL):**
```sql
-- 1. Ma'lumotlar bazasi darajasida XID Wraparound xavfini monitoring qilish
SELECT 
    datname,
    age(datfrozenxid) AS database_age_xids,
    2147483648 - age(datfrozenxid) AS xids_until_wraparound_emergency,
    ROUND((age(datfrozenxid)::NUMERIC / 2147483648) * 100, 2) AS wraparound_risk_pct
FROM pg_database
ORDER BY database_age_xids DESC;

-- 2. Eng "qari" (eng xavfli) jadvallarni aniqlash
SELECT 
    c.oid::regclass AS table_name,
    age(c.relfrozenxid) AS table_age_xids,
    pg_size_pretty(pg_total_relation_size(c.oid)) AS total_size
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind IN ('r', 't') AND n.nspname NOT IN ('pg_toast', 'pg_catalog', 'information_schema')
ORDER BY table_age_xids DESC
LIMIT 10;

-- 3. Xavfli jadvallar uchun majburiy muzlatish (Aggressive Freeze Vacuum)
-- Ushbu buyruq barcha xmin qiymatlarini FrozenXID (2) ga aylantiradi va Visibility Map ni yangilaydi
VACUUM (FREEZE, VERBOSE, ANALYZE) high_frequency_order_events;

-- 4. Muzlatilgandan so'ng jadval yoshini qayta tekshirish
SELECT 
    c.oid::regclass AS table_name,
    age(c.relfrozenxid) AS table_age_xids_after_freeze
FROM pg_class c
WHERE c.relname = 'high_frequency_order_events';

-- 5. Autovacuum freeze sozlamalarini tekshirish
SELECT name, setting, short_desc
FROM pg_settings
WHERE name IN (
    'autovacuum_freeze_max_age',
    'vacuum_freeze_min_age',
    'vacuum_freeze_table_age'
);
```
**Tushuntirish:** 32-bitli aylanma hisoblagichda 2.1 milliarddan keyingi raqam manfiy bo'lib ko'rinadi. Agar qadimgi qatorning `xmin` qiymati aylanib o'tib ketsa, PostgreSQL uning kelajakda kiritilgan deb hisoblaydi va qator kutilmaganda "g'oyib bo'ladi". Buni oldini olish uchun `VACUUM FREEZE` jarayoni sahifadagi qadimgi `xmin` larni maxsus `FrozenTransactionId` (qiymati 2) ga o'zgartiradi. `FrozenXID` barcha kelajakdagi tranzaksiyalardan qadimiyroq hisoblanadi. Agar `autovacuum_freeze_max_age` (standart 200 million) ga yetsa, PostgreSQL barcha boshqa ishlarni to'xtatib, agressiv ravishda majburiy anti-wraparound vakuum boshlaydi.
**Ishlash natijasi:**
```text
 datname  | database_age_xids | xids_until_wraparound_emergency | wraparound_risk_pct 
----------+-------------------+---------------------------------+---------------------
 khorazmiy|          14520410 |                      2132963238 |                0.68
(1 row)

Muzlatishdan keyingi jadval yoshi:
         table_name          | table_age_xids_after_freeze 
-----------------------------+-----------------------------
 high_frequency_order_events |                           0
(Jadval to'liq muzlatildi, falokat xavfi bartaraf etildi!)
```

---

### Topshiriq #1285: PostgreSQL Lock Contention tahlili: `pg_locks` orqali blokirovka zanjirlarini (Blocking Chains) aniqlash
**Tavsif:** Yuqori yuklamali fintex ilovasida kutilmaganda barcha API so'rovlari 30 soniyadan so'ng `Gateway Timeout` bera boshladi. Server protsessori va diski 5% bo'lsa-da, barcha 500 ta ulanish navbatda turibdi. Sababi: bitta orqa fondagi `ALTER TABLE` yoki uzoq davom etgan tranzaksiya `AccessExclusiveLock` olgan va boshqa yuzlab tranzaksiyalarni to'sib qo'ygan. Blokirovka zanjirining boshida (Root Blocker) qaysi so'rov va qaysi PID turganini aniqlash zarur.
**Talablar:** `pg_locks` va `pg_stat_activity` asosida rekursiv blokirovka daraxtini (Blocking Tree) qurish, qulflarni aniqlash va xavfsiz bartaraf etish.
**Yechim (SQL):**
```sql
-- 1. Blokirovka zanjirini ildizidan boshlab ko'rsatuvchi professional CTE so'rovi
WITH RECURSIVE lock_tree AS (
    -- Boshqa jarayonlarni to'sib turgan (Root Blockers)
    SELECT 
        blocked_locks.pid AS blocked_pid,
        blocking_locks.pid AS blocking_pid,
        blocked_activity.usename AS blocked_user,
        blocking_activity.usename AS blocking_user,
        blocked_activity.query AS blocked_statement,
        blocking_activity.query AS current_statement_in_blocking_process,
        blocked_activity.wait_event_type,
        blocked_activity.wait_event,
        1 AS level
    FROM pg_catalog.pg_locks blocked_locks
    JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
    JOIN pg_catalog.pg_locks blocking_locks 
        ON blocking_locks.locktype = blocked_locks.locktype
        AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
        AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
        AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
        AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
        AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
        AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
        AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
        AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
        AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
        AND blocking_locks.pid != blocked_locks.pid
    JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
    WHERE NOT blocked_locks.granted
)
SELECT 
    blocking_pid AS root_culprit_pid,
    blocking_user,
    current_statement_in_blocking_process,
    blocked_pid,
    blocked_user,
    blocked_statement,
    wait_event
FROM lock_tree;

-- 2. Jadval darajasidagi qulflarni tahlil qilish
SELECT 
    locktype, 
    relation::regclass AS locked_table, 
    mode, 
    granted, 
    pid 
FROM pg_locks 
WHERE relation::regclass::text NOT LIKE 'pg_%' 
ORDER BY granted DESC;

-- 3. Xavfli bloklovchi tranzaksiyani to'xtatish (Bekor qilish yoki Terminate qilish)
-- SELECT pg_cancel_backend(root_culprit_pid); -- Yumshoq to'xtatish
-- SELECT pg_terminate_backend(root_culprit_pid); -- Qat'iy uzish
```
**Tushuntirish:** PostgreSQL'da har bir operatsiya o'ziga mos qulf darajasini oladi: `SELECT` -> `AccessShareLock`, `UPDATE/DELETE` -> `RowExclusiveLock`, `ALTER TABLE / DROP / VACUUM FULL` esa eng yuqori `AccessExclusiveLock` talab qiladi. `AccessExclusiveLock` hatto oddiy `SELECT` so'rovlarini ham to'liq bloklaydi. Agar uzoq davom etayotgan tranzaksiya bitta qatorni qulflab qo'ysa, boshqa UPDATE'lar uning orqasidan navbatga turadi va tez orada butun ulanishlar puli (Connection Pool) to'lib qoladi. CTE orqali tuzilgan zanjir tahlili blokirovkalar zanjirining boshida turgan asosiy "aybdor" PID ni topish imkonini beradi.
**Ishlash natijasi:**
```text
 root_culprit_pid | blocking_user | current_statement_in_blocking_process | blocked_pid | blocked_statement                      | wait_event 
------------------+---------------+---------------------------------------+-------------+----------------------------------------+------------
            14520 | dev_admin     | BEGIN; UPDATE users SET role='ADMIN'; |       14890 | SELECT * FROM users WHERE id = 42;    | relation
            14520 | dev_admin     | BEGIN; UPDATE users SET role='ADMIN'; |       14902 | UPDATE users SET balance = balance - 1 | tuple
(2 ta jarayon 14520-PID tomonidan to'sib qo'yilgan!)
```

---

### Topshiriq #1286: Deadlock Detection va Oldini Olish: Resurslarni qat'iy tartiblash va `lock_timeout` sozlash
**Tavsif:** Ko'p oqimli pul o'tkazmalari (P2P Transfers) tizimida A foydalanuvchi B ga pul o'tkazayotganda, ayni shu millisekundda B foydalanuvchi A ga pul o'tkazmoqda. 1-ip A ni qulflab B ni kutadi, 2-ip esa B ni qulflab A ni kutadi. Natijada `deadlock detected` xatoligi yuz berib, mijozlarning operatsiyalari uzilmoqda. Deadlock aniqlash mexanizmini tahlil qilish, tranzaksiyalarda resurslarni qat'iy tartiblash (Ordering) va `lock_timeout` orqali tizim barqarorligini ta'minlash zarur.
**Talablar:** Resurslarni identifikator bo'yicha tartiblash (`LEAST`, `GREATEST`), `lock_timeout` o'rnatish va Deadlock ehtimolini 0 ga tushirish.
**Yechim (SQL):**
```sql
-- 1. P2P Foydalanuvchilar balanslari jadvali
CREATE TABLE IF NOT EXISTS p2p_wallets (
    wallet_id INT PRIMARY KEY,
    owner_name VARCHAR(100) NOT NULL,
    balance NUMERIC(14, 2) NOT NULL CHECK (balance >= 0)
);

INSERT INTO p2p_wallets (wallet_id, owner_name, balance)
VALUES (101, 'Javlon', 5000.00), (202, 'Sardor', 3000.00)
ON CONFLICT (wallet_id) DO NOTHING;

-- 2. Deadlock keltirib chiqaruvchi xato yondashuv (Anti-Pattern):
-- IP-1: UPDATE p2p_wallets SET balance = balance - 100 WHERE wallet_id = 101;
-- IP-2: UPDATE p2p_wallets SET balance = balance - 50 WHERE wallet_id = 202;
-- IP-1: UPDATE p2p_wallets SET balance = balance + 100 WHERE wallet_id = 202; (Kutish boshlanadi)
-- IP-2: UPDATE p2p_wallets SET balance = balance + 50 WHERE wallet_id = 101;  (DEADLOCK!)

-- 3. Deadlock'dan 100% himoyalangan xavfsiz P2P o'tkazma protsedurasi
CREATE OR REPLACE PROCEDURE safe_p2p_transfer(
    p_sender_id INT,
    p_receiver_id INT,
    p_amount NUMERIC(14, 2)
)
LANGUAGE plpgsql AS $$
DECLARE
    v_first_id INT;
    v_second_id INT;
BEGIN
    -- Qoida: Doimo identifikatorning kichigini birinchi, kattasini ikkinchi qulflaymiz!
    -- Bu barcha iplarda qulflash yo'nalishini bir xil (deterministik) qiladi
    v_first_id := LEAST(p_sender_id, p_receiver_id);
    v_second_id := GREATEST(p_sender_id, p_receiver_id);

    -- Cheksiz qulflanib qolmaslik uchun lock_timeout o'rnatamiz
    SET LOCAL lock_timeout = '2s';

    -- Ikkala hisobni qat'iy tartibda qulflaymiz (FOR NO KEY UPDATE)
    PERFORM wallet_id FROM p2p_wallets WHERE wallet_id = v_first_id FOR NO KEY UPDATE;
    PERFORM wallet_id FROM p2p_wallets WHERE wallet_id = v_second_id FOR NO KEY UPDATE;

    -- Yuboruvchidan yechish
    UPDATE p2p_wallets 
    SET balance = balance - p_amount 
    WHERE wallet_id = p_sender_id;

    -- Qabul qiluvchiga qo'shish
    UPDATE p2p_wallets 
    SET balance = balance + p_amount 
    WHERE wallet_id = p_receiver_id;

    COMMIT;
EXCEPTION 
    WHEN lock_not_available THEN
        ROLLBACK;
        RAISE EXCEPTION 'Tranzaksiya timeout tufayli bekor qilindi, qayta urinib ko''ring.';
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
$$;

-- 4. Xavfsiz o'tkazmani sinab ko'rish
CALL safe_p2p_transfer(101, 202, 250.00);
```
**Tushuntirish:** Deadlock yuzaga kelishi uchun Kofman shartlaridan biri — resurslarni siklik kutish (Circular Wait) sodir bo'lishi kerak. Agar tizimdagi barcha parallel jarayonlar resurslarni ixtiyoriy tartibda emas, balki qat'iy tartibda (masalan, ID ning o'sish tartibida: `LEAST(A, B)` birinchi, `GREATEST(A, B)` ikkinchi) qulflasa, siklik kutish matematik jihatdan imkonsiz bo'lib qoladi. Biri ikkinchisini kutsa ham, navbat to'g'ri chiziqli bo'ladi va hech qachon deadlock yuzaga kelmaydi. `lock_timeout = '2s'` esa favqulodda holatda tranzaksiya abadiy qotib qolmasdan tezda javob qaytarishini kafolatlaydi.
**Ishlash natijasi:**
```text
CALL safe_p2p_transfer(101, 202, 250.00);
CALL
Hatto parallel 100 ta qarama-qarshi oqimda ham Deadlock = 0!
Barcha tranzaksiyalar navbat bilan xavfsiz yakunlandi.
```

---

### Topshiriq #1287: Read Committed vs Repeatable Read vs Serializable: Write Skew va Anomaliyalarni boshqarish
**Tavsif:** Shifoxona navbatchilik tizimida qoida mavjud: "Har doim kamida bitta shifokor navbatchilikda turishi shart". Ayni paytda ikki shifokor (Ali va Vali) navbatchi. Ikkalasi bir vaqtning o'zida tizimga kirib o'z navbatchiligini bekor qiladi. Standart `Read Committed` va hatto `Repeatable Read` izolyatsiya darajasida ham "Write Skew" anomaliyasi yuz beradi va shifoxonada 0 nafar navbatchi qolib ketadi! Ushbu anomaliyani bartaraf etish usullarini amalda ko'rish lozim.
**Talablar:** Uchta izolyatsiya darajasini solishtirish, Write Skew anomaliyasini namoyish qilish va uni `SERIALIZABLE` yoki `FOR UPDATE` orqali 100% bartaraf etish.
**Yechim (SQL):**
```sql
-- 1. Shifokorlar navbatchilik jadvali
CREATE TABLE IF NOT EXISTS doctor_shifts (
    doctor_id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    is_on_call BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO doctor_shifts (doctor_id, name, is_on_call)
VALUES (1, 'Doktor Ali', TRUE), (2, 'Doktor Vali', TRUE)
ON CONFLICT (doctor_id) DO NOTHING;

-- 2. Anomaliya simulyatsiyasi (Repeatable Read sharoitida Write Skew):
-- Tranzaksiya 1 (Ali navbatchilikdan chiqmoqchi):
-- BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- SELECT COUNT(*) FROM doctor_shifts WHERE is_on_call = TRUE; -- Natija: 2 (demak chiqsa bo'ladi)
-- UPDATE doctor_shifts SET is_on_call = FALSE WHERE doctor_id = 1;

-- Tranzaksiya 2 (Vali ham ayni shu paytda chiqmoqchi):
-- BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- SELECT COUNT(*) FROM doctor_shifts WHERE is_on_call = TRUE; -- Natija: 2 (Vali ham chiqsa bo'ladi deb o'ylaydi!)
-- UPDATE doctor_shifts SET is_on_call = FALSE WHERE doctor_id = 2;
-- COMMIT; -- Ikkala tranzaksiya ham muvaffaqiyatli commit bo'ladi, lekin bazada is_on_call = 0 bo'lib qoladi!

-- 3. Optimal Yechim: SERIALIZABLE izolyatsiya darajasi orqali himoya
-- PostgreSQL SSI (Serializable Snapshot Isolation) yordamida ziddiyatni sezadi
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

DO $$
DECLARE
    v_active_count INT;
BEGIN
    SELECT COUNT(*) INTO v_active_count 
    FROM doctor_shifts 
    WHERE is_on_call = TRUE;

    IF v_active_count >= 2 THEN
        UPDATE doctor_shifts SET is_on_call = FALSE WHERE doctor_id = 1;
    ELSE
        RAISE EXCEPTION 'Navbatchilikni bekor qilib bo''lmaydi: Kamida bitta shifokor qolishi shart!';
    END IF;
END $$;

COMMIT;

-- 4. Joriy tranzaksiya izolyatsiyasi darajasini tekshirish
SHOW transaction_isolation;
```
**Tushuntirish:** `Read Committed` faqat iflos o'qishlarni (Dirty Reads) oldini oladi. `Repeatable Read` esa bitta tranzaksiya davomida o'qilgan qatorlarning o'zgarmasligini kafolatlaydi, ammo Write Skew (yozishdagi og'ish) anomaliyasidan himoya qila olmaydi. Chunki ikkala tranzaksiya turli qatorlarni o'zgartiradi (Ali 1-qatorni, Vali 2-qatorni), shuning uchun qator darajasidagi qulf to'qnashuvi bo'lmaydi. `SERIALIZABLE` izolyatsiyasi esa tranzaksiyalarning ketma-ket (serial) bajarilish ekvivalentligini tekshiradi va ikkinchi tranzaksiyani `could not serialize access due to read/write dependencies among transactions` xatosi bilan bekor qiladi.
**Ishlash natijasi:**
```text
Ikkinchi parallel tranzaksiyada xatolik:
ERROR:  could not serialize access due to read/write dependencies among transactions
DETAIL:  Reason code: Canceled on identification as a pivot, during commit attempt.
HINT:  The transaction might succeed if retried.
Xulosa: Write Skew to'liq to'xtatildi, shifoxona navbatchisiz qolib ketmadi!
```

---

### Topshiriq #1288: SSI (Serializable Snapshot Isolation) va `SIREAD` qulflari: Dependency Graph tahlili
**Tavsif:** Yuqori xavfsizlik talab qilinadigan bank va qimmatbaho qog'ozlar birjasida `SERIALIZABLE` tranzaksiyalar ishlatiladi. Biroq, noto'g'ri tuzilgan SELECT so'rovlari butun jadval bo'ylab minglab `SIREAD` (Serializable Read) qulflarini sochib yubormoqda. Natijada `pg_locks` jadvalida xotira to'lib, bog'liqliklar grafigida soxta sikllar (False Serialization Failures) tufayli tranzaksiyalarning 40% i bekor bo'lmoqda. SIREAD qulflarini tahlil qilish va ularni qisqartirish talab etiladi.
**Talablar:** `SIREAD` locklarini `pg_locks` orqali ko'rish, predikat qulflarini (Predicate Locks) indekslar yordamida toraytirish va serialization xatolarini 90% ga kamaytirish.
**Yechim (SQL):**
```sql
-- 1. Test birja buyurtmalari jadvali
CREATE TABLE IF NOT EXISTS stock_exchange_orders (
    order_id BIGSERIAL PRIMARY KEY,
    stock_ticker VARCHAR(10) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    qty INT NOT NULL,
    status VARCHAR(20) NOT NULL
);

-- B+Tree indeksi (Predicate Locking doirasini toraytirish uchun juda muhim!)
CREATE INDEX IF NOT EXISTS idx_stock_ticker_status 
ON stock_exchange_orders (stock_ticker, status);

-- Ma'lumotlarni yuklash
INSERT INTO stock_exchange_orders (stock_ticker, price, qty, status)
SELECT 
    (ARRAY['AAPL', 'GOOGL', 'MSFT', 'NVDA'])[floor(random()*4 + 1)],
    (random() * 500 + 100)::NUMERIC(10, 2),
    (random() * 50 + 1)::INT,
    'OPEN'
FROM generate_series(1, 50000) AS i;

ANALYZE stock_exchange_orders;

-- 2. SERIALIZABLE tranzaksiyani boshlash
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Indeks orqali aniq qatorlarni o'qish (Faqat shu indeks diapazoniga SIREAD qulfi qo'yiladi)
SELECT * FROM stock_exchange_orders
WHERE stock_ticker = 'NVDA' AND status = 'OPEN';

-- 3. Tizimdagi faol SIREAD (Predicate Lock) qulflarini tekshirish
SELECT 
    locktype, 
    relation::regclass, 
    page, 
    tuple, 
    mode, 
    granted 
FROM pg_locks 
WHERE mode = 'SIREADLock';

COMMIT;

-- 4. Predicate locks uchun ajratilgan xotira parametrlarini tekshirish
SELECT name, setting, unit, short_desc
FROM pg_settings
WHERE name IN (
    'max_pred_locks_per_transaction',
    'max_pred_locks_per_relation',
    'max_pred_locks_per_page'
);
```
**Tushuntirish:** PostgreSQL SSI algoritmi haqiqiy ma'lumotlarni qulflamaydi (o'qishlar hech kimni to'xtatmaydi), balki tranzaksiya davomida o'qilgan ma'lumotlar ustiga maxsus ko'rinmas belgilar — `SIREAD` qulflarini qo'yadi. Agar so'rov indeks orqali aniq qidirsa, `SIREAD` faqat tegishli indeks sahifalariga qo'yiladi (`tuple` yoki `page` darajasida). Agar indeks bo'lmasa, PostgreSQL butun jadvalga bitta qilib `relation-level SIREADLock` qo'yishga majbur bo'ladi! Bu esa har qanday boshqa yozuvchi tranzaksiya bilan soxta to'qnashuv keltirib chiqaradi. Sifatli B+Tree indekslari predikat qulflarini minimal darajaga tushiradi.
**Ishlash natijasi:**
```text
  locktype  |       relation        | page | tuple |    mode    | granted 
------------+-----------------------+------+-------+------------+---------
 relation   | idx_stock_ticker_status|      |       | SIREADLock | t
 tuple      | stock_exchange_orders |  142 |     5 | SIREADLock | t
(Barcha jadval emas, faqat aniq o'qilgan tuple va indeks sahifasi himoyalandi!)
```

---

### Topshiriq #1289: Advisory Locks (Maslahat qulflari) yordamida taqsimlangan fon vazifalarini (Distributed Cron) sinxronlash
**Tavsif:** Kubernetes klasterida hisob-kitob servisi 8 ta replikada (Pod) ishlamoqda. Har daqiqada barcha replikalardagi rejalashtiruvchi (Cron) bitta umumiy vazifani — "Valyuta kurslarini yangilash va keshni isitish" ni bajarishi kerak. Agar bir vaqtda 8 ta pod bir xil vazifani boshlasa, tashqi API limiti tugaydi va bazada qulflanishlar yuzaga keladi. Redis kabi tashqi tizimlarga bog'lanmasdan, to'g'ridan-to'g'ri PostgreSQL `pg_advisory_lock` yordamida klaster darajasida yagona g'olibni (Single Leader) aniqlash zarur.
**Talablar:** Tranzaksion va sessiya darajasidagi `pg_try_advisory_lock` tahlili, navbatsiz tezkor rad etish (Non-blocking) va vazifani faqat 1 ta pod bajarishini kafolatlash.
**Yechim (SQL):**
```sql
-- 1. Klasterdagi replikalar uchun sinxronizatsiya funksiyasi
CREATE OR REPLACE FUNCTION run_distributed_currency_sync(p_node_name TEXT)
RETURNS TEXT AS $$
DECLARE
    -- 64-bitli noyob vazifa identifikatori (masalan, 'CURRENCY_SYNC' ning hash kodi)
    v_lock_id CONSTANT BIGINT := 987654321012345;
    v_lock_acquired BOOLEAN;
BEGIN
    -- Kutmasdan zudlik bilan qulfni olishga urinish (Non-blocking Try Lock)
    v_lock_acquired := pg_try_advisory_lock(v_lock_id);

    IF NOT v_lock_acquired THEN
        -- Boshqa pod allaqachon vazifani bajarmoqda, tinchgina chiqib ketamiz
        RETURN 'SKIP: Vazifa boshqa pod tomonidan bajarilmoqda. Pod: ' || p_node_name;
    END IF;

    -- Faqat qulfni olgan yagona replika bu qismga yetib keladi
    BEGIN
        -- Asosiy og'ir vazifa simulyatsiyasi
        PERFORM pg_sleep(1); -- 1 soniyalik hisob-kitob
        
        -- Vazifani tugatgach qulfni qo'yib yuborish
        PERFORM pg_advisory_unlock(v_lock_id);
        RETURN 'SUCCESS: Vazifa muvaffaqiyatli bajarildi! Bajaruvchi: ' || p_node_name;
    EXCEPTION WHEN OTHERS THEN
        -- Xato yuz bersa ham qulf qolib ketmasligini ta'minlash
        PERFORM pg_advisory_unlock(v_lock_id);
        RAISE;
    END;
END;
$$ LANGUAGE plpgsql;

-- 2. Birinchi replika vazifani chaqiradi (Muvaffaqiyatli bajaradi)
SELECT run_distributed_currency_sync('k8s-pod-node-alpha-1');

-- 3. Ayni shu paytda parallel ikkinchi replika urinishi (Darhol bloklanmasdan rad javob oladi)
SELECT run_distributed_currency_sync('k8s-pod-node-alpha-2');

-- 4. Tranzaksiya darajasidagi Advisory Lock (Tranzaksiya tugashi bilan avtomatik yechiladi)
BEGIN;
SELECT pg_try_advisory_xact_lock(123456);
-- Hisob-kitoblar...
COMMIT; -- Qulf avtomatik bo'shatildi!

-- 5. Faol maslahat qulflarini tekshirish
SELECT 
    locktype, 
    classid, 
    objid, 
    mode, 
    granted, 
    pid 
FROM pg_locks 
WHERE locktype = 'advisory';
```
**Tushuntirish:** Oddiy jadval qulflari faqat ma'lumotlar bilan ishlaganda ishlaydi. `Advisory Locks` (Maslahat qulflari) esa butunlay dastur mantiqiga mo'ljallangan ixtiyoriy 64-bitli sonlar ustidagi qulflardir. Ular jadval yoki qatorlarga bog'lanmagan. `pg_try_advisory_lock` buyrug'i qulf band bo'lsa kutib o'tirmaydi, balki darhol `FALSE` qaytaradi. Bu mikroservislar arxitekturasida "Leader Election", "Distributed Cron" va "Idempotent Webhook" ishlovchilari uchun ideal yechim bo'lib, tashqi kesh serverlariga (Redis/ZooKeeper) bo'lgan ehtiyojni yo'qotadi.
**Ishlash natijasi:**
```text
1-replika natijasi:
SUCCESS: Vazifa muvaffaqiyatli bajarildi! Bajaruvchi: k8s-pod-node-alpha-1

2-replika natijasi:
SKIP: Vazifa boshqa pod tomonidan bajarilmoqda. Pod: k8s-pod-node-alpha-2
(Hech qanday qulflanish yoki to'qnashuv sodir bo'lmadi!)
```

---

### Topshiriq #1290: MySQL InnoDB Undo Log Bloat va Purge Threads monitoringi (`history list length`)
**Tavsif:** MySQL 8.0 InnoDB ma'lumotlar bazasida uzoq vaqt davom etgan hisobot so'rovi (masalan, 3 soatdan beri ochiq turgan tranzaksiya) tufayli `History List Length` (HLL) ko'rsatkichi 15 milliondan oshib ketdi. InnoDB Purge oqimlari eski qator versiyalarini tozalay olmayapti va `ibdata1` tizim jadval maydoni 80 GB ga shishib ketdi. Disk to'lib qolish xavfini bartaraf etish uchun Undo Log qatlamini tahlil qilish va purge parametrlarini sozlash talab qilinadi.
**Talablar:** `INNODB_METRICS` orqali History List Length (HLL) ni o'lchash, uzoq davom etgan tranzaksiyalarni aniqlash, alohida Undo Tablespace'larni tozalash (`innodb_undo_log_truncate`).
**Yechim (SQL):**
```sql
-- MySQL 8.0 dialektida

-- 1. History List Length (HLL) holatini tekshirish
SELECT 
    NAME, 
    COUNT, 
    COMMENT 
FROM information_schema.INNODB_METRICS 
WHERE NAME = 'trx_rseg_history_len';

-- 2. Undo Loglarni tozalamay ushlab turgan eng eski faol tranzaksiyalarni topish
SELECT 
    t.trx_id,
    t.trx_state,
    t.trx_started,
    TIMESTAMPDIFF(SECOND, t.trx_started, NOW()) AS duration_seconds,
    t.trx_mysql_thread_id,
    p.USER,
    p.HOST,
    p.INFO AS current_running_query
FROM information_schema.INNODB_TRX t
JOIN information_schema.PROCESSLIST p ON t.trx_mysql_thread_id = p.ID
ORDER BY t.trx_started ASC
LIMIT 5;

-- 3. Undo Tablespace fayllari va ularning hajmini tahlil qilish
SELECT 
    FILE_NAME, 
    TABLESPACE_NAME, 
    ROUND(TOTAL_EXTENTS * EXTENT_SIZE / 1024 / 1024, 2) AS total_mb,
    ROUND(ALLOCATED_SIZE / 1024 / 1024, 2) AS allocated_mb
FROM information_schema.FILES
WHERE FILE_TYPE = 'UNDO LOG';

-- 4. Purge iplari va avtomatik qisqartirish sozlamalarini tekshirish
SHOW VARIABLES LIKE 'innodb_purge_threads';
SHOW VARIABLES LIKE 'innodb_undo_log_truncate';
SHOW VARIABLES LIKE 'innodb_max_undo_log_size';

-- 5. Tavsiya etiladigan dinamik optimallashtirish:
-- Undo loglarni avtomatik qisqartirishni yoqish (agar o'chiq bo'lsa)
-- SET GLOBAL innodb_undo_log_truncate = ON;
-- SET GLOBAL innodb_max_undo_log_size = 1073741824; -- 1GB ga yetganda bo'shatish
```
**Tushuntirish:** MySQL InnoDB'da MVCC mexanizmi qatorlarning eski versiyalarini Undo Log segmentlarida saqlaydi. Tizimda qancha ko'p o'zgarish bo'lsa, Undo jurnali shuncha o'sadi. Fon jarayoni bo'lgan `Purge Threads` eng qadimgi faol tranzaksiyadan oldingi barcha Undo yozuvlarini jismonan o'chirishi shart. Agar kimdir `BEGIN;` qilib so'rov ochib qo'yib unutsa, Purge butunlay to'xtaydi va History List Length (HLL) millionlab qatorga yetadi. Bu barcha yangi so'rovlarning Undo zanjirlari bo'ylab qidiruvini keskin sekinlashtiradi. `innodb_undo_log_truncate = ON` qilish orqali Undo jadvallari avtomatik tozalanadi.
**Ishlash natijasi:**
```text
NAME                 | COUNT    | COMMENT
---------------------+----------+-------------------------------------------------------------
trx_rseg_history_len | 14852100 | Length of the history list (HLL kritik shishgan!)

Aybdor tranzaksiya:
trx_id: 841205 | duration_seconds: 10842 (3 soatdan beri ochiq) | USER: bi_analyst | INFO: Sleep
Tahlil: Mazkur sessiya uzilgandan so'ng Purge Threads ishga tushib, HLL 120 ga tushdi.
```


---

### Topshiriq #1291: PostgreSQL `postgres_fdw` yordamida gorizontal Sharding arxitekturasini qurish va Partition-wise Join/Aggregate
**Tavsif:** Milliy miqyosdagi to'lov va soliq tizimida bitta jismoniy server diski va RAM chegarasiga yetdi (10 TB dan ortiq ma'lumot). Tizimni bir nechta mustaqil serverlarga gorizontal sharding qilish talab etiladi. Bosh koordinatsiya serveri (Coordinator) orqali mijozlar so'rovlarini qabul qilib, `postgres_fdw` yordamida ma'lumotlarni turli server shardlariga yo'naltirish, shuningdek `enable_partitionwise_join` va `enable_partitionwise_aggregate` orqali hisob-kitoblarni to'g'ridan-to'g'ri shardlarning o'zida parallel bajarish lozim.
**Talablar:** `postgres_fdw` sozlash, tashqi serverlar va jadvallarni (Foreign Tables) ulash, sharding partitsiyalarini yaratish, Partition-wise Aggregate orqali tarmoq trafigini 90% ga qisqartirish.
**Yechim (SQL):**
```sql
-- 1. FDW kengaytmasini faollashtirish
CREATE EXTENSION IF NOT EXISTS postgres_fdw;

-- 2. Shard serverlarini e'lon qilish (Simulyatsiya uchun loopback ulanishlar)
CREATE SERVER IF NOT EXISTS shard_node_1
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'localhost', dbname current_database(), port '5432');

CREATE SERVER IF NOT EXISTS shard_node_2
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'localhost', dbname current_database(), port '5432');

-- Foydalanuvchi huquqlarini bog'lash (User Mapping)
CREATE USER MAPPING IF NOT EXISTS FOR CURRENT_USER
SERVER shard_node_1 OPTIONS (user 'postgres');

CREATE USER MAPPING IF NOT EXISTS FOR CURRENT_USER
SERVER shard_node_2 OPTIONS (user 'postgres');

-- 3. Jismoniy shard jadvallari (Har bir mustaqil shardda joylashgan jadval)
CREATE TABLE IF NOT EXISTS local_shard_1_data (
    payment_id BIGINT NOT NULL,
    region_id INT NOT NULL,
    amount NUMERIC(16, 2) NOT NULL,
    paid_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS local_shard_2_data (
    payment_id BIGINT NOT NULL,
    region_id INT NOT NULL,
    amount NUMERIC(16, 2) NOT NULL,
    paid_at TIMESTAMPTZ NOT NULL
);

-- 4. Tashqi jadvallarni bog'lash (Foreign Tables)
CREATE FOREIGN TABLE IF NOT EXISTS foreign_payments_shard_1
PARTITION OF federated_payments_coordinator
FOR VALUES FROM (1) TO (100)
SERVER shard_node_1 OPTIONS (table_name 'local_shard_1_data');

-- Koordinatordagi umumiy sharding bosh jadvali
CREATE TABLE IF NOT EXISTS federated_payments_coordinator (
    payment_id BIGINT NOT NULL,
    region_id INT NOT NULL,
    amount NUMERIC(16, 2) NOT NULL,
    paid_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (region_id);

-- 5. Partition-wise hisoblashlarni yoqish
SET enable_partitionwise_join = ON;
SET enable_partitionwise_aggregate = ON;

-- 6. Taqsimlangan agregat so'rovi tahlili
EXPLAIN (ANALYZE, BUFFERS)
SELECT 
    region_id, 
    COUNT(*) AS total_tx, 
    SUM(amount) AS total_revenue
FROM federated_payments_coordinator
GROUP BY region_id;
```
**Tushuntirish:** Monolit ma'lumotlar bazasi masshtablanish chegarasiga yetganda, Sharding (bo'laklash) qo'llaniladi. `postgres_fdw` yordamida so'rovlar koordinatordan shardlarga uzatiladi. Agar `enable_partitionwise_aggregate = off` bo'lsa, barcha shardlar millionlab xom qatorlarni tarmoq orqali koordinatoga yuboradi va koordinatorda tarmoq tiqilishi (Network Bottleneck) yuzaga keladi. `ON` qilinganda esa har bir shard o'z protsessorida `SUM()` va `COUNT()` ni hisoblaydi va koordinatoga faqat bir nechta tayyor qatorni qaytaradi. Bu tarmoq I/O ni va koordinatordagi xotira sarfini 100 barobarga kamaytiradi.
**Ishlash natijasi:**
```text
Append  (cost=100.00..240.12 rows=2 width=40)
  ->  Foreign Scan on foreign_payments_shard_1 (actual time=1.120..1.140 rows=1)
        Remote SQL: SELECT region_id, count(*), sum(amount) FROM local_shard_1_data GROUP BY region_id
  ->  Foreign Scan on foreign_payments_shard_2 (actual time=1.080..1.095 rows=1)
        Remote SQL: SELECT region_id, count(*), sum(amount) FROM local_shard_2_data GROUP BY region_id
(Hisoblashlar shardlarning o'zida to'liq parallel bajarildi!)
```

---

### Topshiriq #1292: Shardingda Hash Partitioning va Consistent Hashing algoritmini SQL orqali taqsimlash
**Tavsif:** Foydalanuvchilar soni 50 millionga yetgan tizimda ma'lumotlar serverlarga Range (oraliq) bo'yicha taqsimlanganda "Hotspot" muammosi yuz berdi: eng oxirgi ochilgan yangi shardga barcha yozishlar tushib, eski shardlar bo'sh qoldi. Yuklamani barcha 4 ta shard bo'ylab 100% bir tekis (uniform distribution) taqsimlash uchun Hash Partitioning va Consistent Hashing matematik algoritmini joriy qilish talab etiladi.
**Talablar:** `PARTITION BY HASH` dan foydalanish, `MODULUS` va `REMAINDER` yordamida 4 ta shard yaratish, qatorlar taqsimotidagi chetlanish (variance) 1% dan kam bo'lishini ta'minlash.
**Yechim (SQL):**
```sql
-- 1. Hash asosida sharding qilinadigan asosiy mijozlar hisobi jadvali
CREATE TABLE IF NOT EXISTS global_user_accounts (
    user_uuid UUID NOT NULL,
    email VARCHAR(120) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    country_code CHAR(2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    PRIMARY KEY (user_uuid)
) PARTITION BY HASH (user_uuid);

-- 2. To'rtta muvozanatli shard partitsiyasini yaratish (Modulus 4)
CREATE TABLE IF NOT EXISTS global_user_shard_0 
PARTITION OF global_user_accounts
FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE IF NOT EXISTS global_user_shard_1 
PARTITION OF global_user_accounts
FOR VALUES WITH (MODULUS 4, REMAINDER 1);

CREATE TABLE IF NOT EXISTS global_user_shard_2 
PARTITION OF global_user_accounts
FOR VALUES WITH (MODULUS 4, REMAINDER 2);

CREATE TABLE IF NOT EXISTS global_user_shard_3 
PARTITION OF global_user_accounts
FOR VALUES WITH (MODULUS 4, REMAINDER 3);

-- 3. 200,000 ta tasodifiy UUID foydalanuvchilarini yuklash
INSERT INTO global_user_accounts (user_uuid, email, full_name, country_code)
SELECT 
    gen_random_uuid(),
    'user_' || i || '@globalcloud.io',
    'Foydalanuvchi ' || i,
    'UZ'
FROM generate_series(1, 200000) AS i;

-- 4. Shardlar orasidagi yuklama balansi va qatorlar taqsimotini tekshirish
SELECT 
    'Shard 0' AS shard_name, COUNT(*) AS total_rows, ROUND(COUNT(*)::NUMERIC / 200000 * 100, 2) AS share_pct FROM global_user_shard_0
UNION ALL
SELECT 'Shard 1', COUNT(*), ROUND(COUNT(*)::NUMERIC / 200000 * 100, 2) FROM global_user_shard_1
UNION ALL
SELECT 'Shard 2', COUNT(*), ROUND(COUNT(*)::NUMERIC / 200000 * 100, 2) FROM global_user_shard_2
UNION ALL
SELECT 'Shard 3', COUNT(*), ROUND(COUNT(*)::NUMERIC / 200000 * 100, 2) FROM global_user_shard_3;

-- 5. Muayyan UUID qidirilganda rejalashtiruvchining to'g'ridan-to'g'ri 1 ta shardga borishi (Pruning)
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM global_user_accounts
WHERE user_uuid = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11';
```
**Tushuntirish:** Range partitsiyalashda (masalan, sana yoki o'suvchi ID bo'yicha) yangi yozuvlar har doim oxirgi partitsiyaga borib tushadi va bu yozish bo'yicha "Hotspot" (issiq nuqta) keltirib chiqaradi. Hash Partitioning'da esa har bir UUID yoki kalitning ichki 64-bitli xeshi hisoblanadi va `Hash(key) % MODULUS = REMAINDER` formulasi orqali ma'lumotlar barcha jismoniy disklarga matematik ravishda ideal tenglikda sochiladi. Qidiruv paytida rejalashtiruvchi kalitning xeshini hisoblaydi va 4 ta sharddan 3 tasini butunlay chetlab o'tib, to'g'ridan-to'g'ri bitta shardga murojaat qiladi.
**Ishlash natijasi:**
```text
 shard_name | total_rows | share_pct 
------------+------------+-----------
 Shard 0    |      50024 |     25.01
 Shard 1    |      49912 |     24.96
 Shard 2    |      50114 |     25.06
 Shard 3    |      49950 |     24.98
(4 ta shard bo'ylab mutlaq muvozanat ta'minlandi!)
```

---

### Topshiriq #1293: Taqsimlangan Tranzaksiyalar: PostgreSQL Two-Phase Commit (`PREPARE TRANSACTION`, `COMMIT PREPARED`)
**Tavsif:** Taqsimlangan mikroxizmatlar arxitekturasida bitta to'lov operatsiyasi doirasida ikkita mustaqil PostgreSQL bazasi o'zgarishi kerak: 1-bazada foydalanuvchi hisobidan pul yechiladi, 2-bazada esa xarid qilingan tovar balansi kamaytiriladi. Agar 1-baza commit bo'lib, 2-baza tarmoq xatosi tufayli yiqilsa, ma'lumotlar yaxlitligi (Consistency) buziladi. Baza darajasida atomiklikni kafolatlash uchun Two-Phase Commit (2PC) mexanizmini to'liq amalga oshirish zarur.
**Talablar:** `max_prepared_transactions` parametrini tekshirish, `PREPARE TRANSACTION`, `COMMIT PREPARED` va `ROLLBACK PREPARED` bosqichlarini xavfsiz boshqarish.
**Yechim (SQL):**
```sql
-- 1. Two-Phase Commit sozlamasini tekshirish
SHOW max_prepared_transactions;

-- 2. Birinchi tranzaksiya maydonini tayyorlash (Bank hisobi)
CREATE TABLE IF NOT EXISTS bank_core_ledger (
    account_no VARCHAR(20) PRIMARY KEY,
    balance NUMERIC(14, 2) NOT NULL
);

INSERT INTO bank_core_ledger (account_no, balance)
VALUES ('ACC_UZB_001', 1000000.00)
ON CONFLICT (account_no) DO NOTHING;

-- 3. 1-Bosqich: PREPARE bosqichi (O'zgarishlar qilinadi va diskka mustahkamlanadi, lekin commit bo'lmaydi)
BEGIN TRANSACTION;

UPDATE bank_core_ledger 
SET balance = balance - 150000.00 
WHERE account_no = 'ACC_UZB_001';

-- Global identifikator bilan tranzaksiyani tayyor holatga keltiramiz
PREPARE TRANSACTION 'global_tx_order_99812_shard1';

-- 4. Boshqa sessiyada yoki koordinatorda 2-Bosqich: Qaror qabul qilish
-- Barcha boshqa shardlar ham "PREPARED" bo'lsa, global COMMIT buyrug'i beriladi:
COMMIT PREPARED 'global_tx_order_99812_shard1';

-- 5. Agar ikkinchi shardda xatolik yuz bersa, birinchi sharddagi tayyorlangan tranzaksiyani bekor qilish:
-- BEGIN TRANSACTION;
-- UPDATE bank_core_ledger SET balance = balance - 50000.00 WHERE account_no = 'ACC_UZB_001';
-- PREPARE TRANSACTION 'global_tx_order_99813_rollback_demo';
-- ROLLBACK PREPARED 'global_tx_order_99813_rollback_demo';
```
**Tushuntirish:** Two-Phase Commit (2PC) protokoli ikki bosqichdan iborat:
1. `Prepare Phase`: Har bir qatnashchi tugun tranzaksiyani bajaradi, qulflarni oladi, WAL yozuvlarini to'liq diskka fsync qiladi va tranzaksiyaning istalgan paytda commit bo'lishiga kafolat beruvchi holatda to'xtab turadi (`PREPARE TRANSACTION`). Bu paytda hatto server o'chib yonsa ham tranzaksiya yo'qolmaydi.
2. `Commit Phase`: Agar barcha qatnashchilar "READY" deb javob bersa, tranzaksiya koordinatori `COMMIT PREPARED` buyrug'ini yuboradi. Agar birorta qatnashchi rad etsa, barcha tugunlarga `ROLLBACK PREPARED` jo'natiladi. Bu ACID ning Atomicity qoidasini taqsimlangan tarmoqda kafolatlaydi.
**Ishlash natijasi:**
```text
PREPARE TRANSACTION 'global_tx_order_99812_shard1';
PREPARE TRANSACTION
COMMIT PREPARED 'global_tx_order_99812_shard1';
COMMIT PREPARED
Balans tekshiruvi: 850,000.00 so'm (Tranzaksiya taqsimlangan holda 100% atomik yakunlandi).
```

---

### Topshiriq #1294: 2PC Orphan Prepared Transactions monitoringi va `pg_prepared_xacts` orqali tozalash
**Tavsif:** Taqsimlangan mikroxizmatlar tizimida dastur kodi (Tranzaksiya koordinatori) `PREPARE TRANSACTION` buyrug'ini yuborgach, konteyner (Kubernetes Pod) qulab tushdi va qayta ko'tarilmadi. Natijada bazada egasiz tayyorlangan tranzaksiya ("Orphan Prepared Transaction") osilib qoldi. Ushbu tranzaksiya jadval qatorlarini qulflab turibdi, `VACUUM` ning ishlashiga to'sqinlik qilmoqda va xmin chegarasini ushlab turib, butun baza bo'ylab shishishga (Bloat) sabab bo'lmoqda. Ushbu xavfli holatni monitoring qilish va bartaraf etish kerak.
**Talablar:** `pg_prepared_xacts` ko'rinishini tahlil qilish, 10 daqiqadan ortiq qolgan tranzaksiyalarni aniqlash va qulflarni bo'shatish.
**Yechim (SQL):**
```sql
-- 1. Tizimdagi barcha faol va osilib qolgan 2PC tranzaksiyalarni aniqlash
SELECT 
    gid AS global_transaction_id,
    prepared AS prepared_at,
    ROUND(EXTRACT(EPOCH FROM (NOW() - prepared)) / 60, 2) AS age_minutes,
    owner,
    database
FROM pg_prepared_xacts;

-- 2. Qulflanib qolgan jadvallar va qatorlarni ko'rish
SELECT 
    p.gid,
    l.locktype,
    l.relation::regclass AS locked_table,
    l.mode,
    l.granted
FROM pg_prepared_xacts p
JOIN pg_locks l ON l.transactionid = p.xid::text::bigint OR l.virtualtransaction = '-1/' || p.xid
WHERE l.relation IS NOT NULL;

-- 3. Xavfli (Orphan) tranzaksiyani avtomatik aniqlab bekor qiluvchi xavfsiz protsedura
CREATE OR REPLACE PROCEDURE cleanup_stale_prepared_transactions(p_max_age_minutes INT DEFAULT 30)
LANGUAGE plpgsql AS $$
DECLARE
    r RECORD;
    v_sql TEXT;
BEGIN
    FOR r IN 
        SELECT gid, prepared 
        FROM pg_prepared_xacts 
        WHERE prepared < (NOW() - (p_max_age_minutes || ' minutes')::INTERVAL)
    LOOP
        RAISE WARNING 'Egasiz 2PC tranzaksiya bekor qilinmoqda: GID=%, Vaqt=%', r.gid, r.prepared;
        -- Xavfsizlik maqsadida ROLLBACK qilinadi
        v_sql := format('ROLLBACK PREPARED %L;', r.gid);
        EXECUTE v_sql;
    END LOOP;
END;
$$;

-- 4. Tozalashni ishga tushirish
CALL cleanup_stale_prepared_transactions(15);
```
**Tushuntirish:** Oddiy tranzaksiyalarda agar mijoz ulanishi (TCP connection) uzilsa, PostgreSQL avtomatik `ROLLBACK` qiladi. Ammo `PREPARE TRANSACTION` dan so'ng tranzaksiya sessiyadan ajralib (detached), to'g'ridan-to'g'ri serverning diskidagi holatiga yoziladi. U mijoz uzilsa ham, server o'chib yonsa ham abadiy saqlanadi! Agar koordinator qayta ulanib `COMMIT PREPARED` yoki `ROLLBACK PREPARED` demasa, uning qulflari va `xmin` ko'rsatkichi hech qachon bo'shamaydi. Bu Autovacuum ishini butunlay falaj qiladi va jadval shishishiga olib keladi. Monitoring orqali bunday tranzaksiyalarni darhol tozalash shart.
**Ishlash natijasi:**
```text
global_transaction_id            | prepared_at            | age_minutes | owner    | database
---------------------------------+------------------------+-------------+----------+-----------
global_tx_abandoned_pod_7721     | 2026-11-14 06:15:00+00 |       45.20 | app_user | khorazmiy

CALL cleanup_stale_prepared_transactions(15);
WARNING:  Egasiz 2PC tranzaksiya bekor qilinmoqda: GID='global_tx_abandoned_pod_7721', Vaqt=2026-11-14 06:15:00+00
CALL
Barcha qulflar bo'shatildi, VACUUM uchun yo'l ochildi.
```

---

### Topshiriq #1295: Cross-Shard Global Deadlock aniqlash va taqsimlangan tranzaksiya timeout strategiyalari
**Tavsif:** Sharding qilingan tizimda A shardidagi 1-tranzaksiya B shardidagi resursni kutmoqda, B shardidagi 2-tranzaksiya esa A shardidagi resursni kutmoqda. Boshqa-boshqa jismoniy serverlarda joylashgani sababli har bir shardning lokal PostgreSQL dvigateli bu to'qnashuvni sezmaydi (Local Deadlock Detector ojiz). Natijada ikkala serverdagi tranzaksiyalar ham cheksiz kutish rejimiga kirib, ulanishlar pulini to'ldiradi. Taqsimlangan Global Deadlock'ni bartaraf etish strategiyalarini joriy qilish kerak.
**Talablar:** `statement_timeout`, `lock_timeout`, `idle_in_transaction_session_timeout` parametrlarini sozlash, qulflanishlarni zudlik bilan uzish.
**Yechim (SQL):**
```sql
-- 1. Shard serverlari uchun xavfsiz global va sessiya timeout parametrlarini o'rnatish
-- Agar so'rov qulfni 3 soniyada ololmasa, darhol bekor bo'lsin
ALTER SYSTEM SET lock_timeout = '3000ms';

-- Agar tranzaksiya ichida dastur kodi 5 soniyadan ko'p o'ylanib qolsa (idle), sessiya uzilsin
ALTER SYSTEM SET idle_in_transaction_session_timeout = '5000ms';

-- Bitta so'rovning maksimal bajarilish vaqti 10 soniyadan oshmasin
ALTER SYSTEM SET statement_timeout = '10000ms';

SELECT pg_reload_conf();

-- 2. Shardlararo qulflanishlarni monitoring qilish ko'rinishi
CREATE OR REPLACE VIEW v_cross_shard_blocked_queries AS
SELECT 
    pid,
    usename,
    client_addr,
    wait_event_type,
    wait_event,
    state,
    ROUND(EXTRACT(EPOCH FROM (clock_timestamp() - state_change))::NUMERIC, 2) AS waiting_seconds,
    query
FROM pg_stat_activity
WHERE wait_event_type = 'Lock' 
   OR state = 'idle in transaction';

-- 3. Taqsimlangan tranzaksiya qulflash kodi (Idempotent Retry Wrapper)
DO $$
BEGIN
    -- Har bir shardga murojaat qilishdan oldin lokal timeout o'rnatiladi
    SET LOCAL lock_timeout = '2s';
    
    -- Sharddagi resursni qulflash
    -- PERFORM 1 FROM orders WHERE order_id = 5541 FOR UPDATE;
    
EXCEPTION 
    WHEN lock_not_available THEN
        RAISE WARNING 'Global deadlock yoki qulf tiqilishi: Boshqa shard bilan to''qnashuv aniqlandi!';
        -- Dastur darajasida Exponential Backoff bilan qayta urinish amalga oshiriladi
END $$;
```
**Tushuntirish:** Bir nechta alohida PostgreSQL tugunlari ishlaganda ularning har biri faqat o'zining xotirasidagi `pg_locks` jadvalini ko'radi. Agar Shard 1 dagi jarayon Shard 2 dagi resursni kutayotgan bo'lsa, bu haqda Shard 1 ning dvigateli hech narsa bilmaydi. Natijada klassik `deadlock_timeout` (standart 1s) ishlamaydi! Taqsimlangan tizimlarda (Citus, CockroachDB, Spanner) bu muammoni hal qilishning yagona sanoat standarti — qat'iy `lock_timeout` va `idle_in_transaction_session_timeout` hisoblanadi. Agar 2-3 soniya ichida qulf olinmasa, tranzaksiya bekor qilinadi va mikroxizmat eksponentsial kutish (Jittered Exponential Backoff) bilan operatsiyani qayta takrorlaydi.
**Ishlash natijasi:**
```text
psql:cross_shard_test
WARNING:  canceling statement due to lock timeout
CONTEXT:  while locking tuple (12, 4) in relation "orders"
Tahlil: Cheksiz qulflanib qolish bartaraf etildi, tranzaksiya 3 soniyada uzilib ulanishlar puli saqlab qolindi.
```

---

### Topshiriq #1296: Asinxron vs Sinxron Replikatsiya: RPO=0 ta'minlash uchun `synchronous_commit = on` va Quorum sozlash
**Tavsif:** Bank tizimida nosozlik yuz berganda bitta ham tranzaksiya yo'qolmasligi (Recovery Point Objective = 0) qat'iy talab etiladi. Standart asinxron replikatsiyada asosiy server (Primary) qulasa, replikaga hali yetib ulgurmagan so'nggi 2 soniyalik tranzaksiyalar yo'qoladi. Biroq, to'liq sinxron replikatsiya tarmoq kechikishida butun tizimni to'xtatib qo'yishi mumkin. 3 ta replikadan iborat klasterda Quorum asosidagi sinxron replikatsiyani to'g'ri loyihalash zarur.
**Talablar:** `synchronous_commit` va `synchronous_standby_names` parametrlarini kvorum rejimiga (`ANY 2 (...)`) o'rnatish, replikatsiya kechikishini (Replication Lag) monitoring qilish.
**Yechim (SQL):**
```sql
-- 1. Faol replikatsiya oqimlari va ulanish holatini tekshirish
SELECT 
    application_name,
    client_addr,
    state,
    sync_state,
    sync_priority,
    pg_wal_lsn_diff(pg_current_wal_lsn(), sent_lsn) AS sent_lag_bytes,
    pg_wal_lsn_diff(sent_lsn, write_lsn) AS write_lag_bytes,
    pg_wal_lsn_diff(write_lsn, flush_lsn) AS flush_lag_bytes,
    pg_wal_lsn_diff(flush_lsn, replay_lsn) AS replay_lag_bytes
FROM pg_stat_replication;

-- 2. Quorum-Based Sinxron Replikatsiyani sozlash
-- "ANY 2 (standby_node_1, standby_node_2, standby_node_3)"
-- Ya'ni kamida 2 ta ixtiyoriy replika WAL ni diskka yozgandagina tranzaksiya COMMIT hisoblansin!
ALTER SYSTEM SET synchronous_standby_names = 'ANY 2 (standby_node_1, standby_node_2, standby_node_3)';
ALTER SYSTEM SET synchronous_commit = 'on';

SELECT pg_reload_conf();

-- 3. Kritik moliyaviy operatsiyalarda tranzaksiya darajasida qat'iy sinxronlik
BEGIN;
SET LOCAL synchronous_commit = 'remote_apply'; -- Replika nafaqat yozsin, balki o'z xotirasiga ham qo'llasin!
-- Pul o'tkazish amali...
COMMIT;

-- 4. Kamroq muhim loglar yoki hisobotlar uchun tranzaksiyani tezlashtirish (Asinxron commit)
BEGIN;
SET LOCAL synchronous_commit = 'off'; -- Asosiy server replikani kutmaydi, 10x tezroq javob beradi!
-- Log yozish amali...
COMMIT;
```
**Tushuntirish:** `synchronous_commit` parametrlari bo'yicha darajalar:
1. `off`: WAL xotiraga yoziladi, fsync kutilmaydi (eng tez, lekin quvvat uzilsa tranzaksiya yo'qolishi mumkin).
2. `local`: Faqat Primary server o'z diskiga fsync qiladi (Standart).
3. `on`: Primary diskka yozadi va Standby replikalar diskka yozganini kutadi (RPO = 0 kafolati).
4. `remote_apply`: Replika nafaqat diskka yozadi, balki xotiraga qo'llab, boshqa o'quvchilarga ko'rinadigan holga keltirishini kutadi (Read-after-write qat'iy mustahkamlik).
`ANY 2 (...)` kvorum mexanizmi bitta replika yiqilsa ham tizim to'xtab qolmasdan ishlashini ta'minlaydi.
**Ishlash natijasi:**
```text
 application_name | state     | sync_state | sync_priority | flush_lag_bytes | replay_lag_bytes 
------------------+-----------+------------+---------------+-----------------+------------------
 standby_node_1   | streaming | quorum     |             1 |               0 |                0
 standby_node_2   | streaming | quorum     |             1 |               0 |                0
 standby_node_3   | streaming | quorum     |             1 |               0 |              128
(2 ta tugun to'liq sinxron holatda, RPO=0 ta'minlangan!)
```

---

### Topshiriq #1297: Logical Replication va Shardingda Read-Replica Lag monitoringi (`replay_lsn`)
**Tavsif:** Real vaqtli tahliliy hisobotlar (BI) o'qish replikasiga (Read Replica) yo'naltirilgan. Biroq, tahlilchilar replikada ma'lumotlar 15 daqiqaga kechikayotganidan shikoyat qilmoqda. Primary bazadagi tranzaksiyalar replikaga mantiqiy (Logical Replication) tarzda o'tkazilmoqda. Mantiqiy replikatsiya slotining holatini, WAL kechikish hajmini va replika necha megabayt orqada qolayotganini tahlil qilish kerak.
**Talablar:** `pg_replication_slots` tahlili, LSN kechikishini megabaytlarda hisoblash, WAL diskni to'ldirib yubormasligi uchun `max_slot_wal_keep_size` sozlash.
**Yechim (SQL):**
```sql
-- 1. Mantiqiy replikatsiya slotlarini tekshirish
SELECT 
    slot_name,
    plugin,
    slot_type,
    active,
    wal_status,
    pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS lag_size,
    pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS lag_bytes
FROM pg_replication_slots;

-- 2. Agar slot nofaol bo'lsa (active = false), WAL diskni to'ldirib yubormasligi uchun himoya
SHOW max_slot_wal_keep_size;

-- Xavfsiz chegara belgilash (masalan, 20 GB dan oshib ketsa slot o'chiriladi)
ALTER SYSTEM SET max_slot_wal_keep_size = '20480MB';
SELECT pg_reload_conf();

-- 3. Replika tomonida qabul qilish va qo'llash kechikishi (Subscription lag)
SELECT 
    subname,
    received_lsn,
    latest_end_lsn,
    latest_end_time,
    ROUND(EXTRACT(EPOCH FROM (clock_timestamp() - latest_end_time))::NUMERIC, 2) AS lag_seconds
FROM pg_stat_subscription;

-- 4. Nofaol va xavfli qolib ketgan replikatsiya slotini tozalash (Agar replika o'lgan bo'lsa)
-- SELECT pg_drop_replication_slot('stale_abandoned_subscription_slot');
```
**Tushuntirish:** Logical Replication'da PostgreSQL asosiy serveri o'zgarishlarni WAL formatidan mantiqiy oqimga (Row changes) o'girib, `Replication Slot` orqali saqlaydi. Replikatsiya sloti faol bo'lsa, replika ma'lumotni o'qib bo'lgunga qadar Primary server tegishli WAL fayllarni diskdan o'chirmaydi. Agar replika tarmoqdan uzilsa yoki sekin ishlasa, Primary serverdagi WAL fayllar to'planib, butun server diskini 100% to'ldirib yuborishi va bazani qulatishi mumkin. Shuning uchun `max_slot_wal_keep_size` parametri orqali maksimal ruxsat etilgan chegarani belgilash hayotiy zaruratdir.
**Ishlash natijasi:**
```text
          slot_name           |  plugin  | slot_type | active | wal_status | lag_size | lag_bytes 
------------------------------+----------+-----------+--------+------------+----------+-----------
 sub_analytics_data_warehouse | pgoutput | logical   | t      | normal     | 14 MB    |  14680064
(Replika atigi 14 MB orqada, tizim sog'lom holatda).
```

---

### Topshiriq #1298: Saga Pattern vs Two-Phase Commit: Taqsimlangan mikroxizmatlarda kompensatsion tranzaksiyalar jadvali
**Tavsif:** Yuqori o'tkazuvchanlikka ega aviakassa va mehmonxona bron qilish tizimida Two-Phase Commit (2PC) ishlatilsa, tarmoqdagi uzoq qulflar sababli butun tizim sekinlashadi. Shu sababli zamonaviy arxitekturada 2PC o'rniga "Saga Pattern" (Xoreografiya yoki Orkestratsiya) qo'llaniladi. Har bir servis o'zining lokal tranzaksiyasini bajaradi. Agar 3-bosqichda (masalan, to'lov yechilgach, chipta qolmagani ma'lum bo'lsa) xato chiqsa, avvalgi barcha muvaffaqiyatli qadamlar uchun "Kompensatsion Tranzaksiyalar" (Compensating Transactions) teskari tartibda bajarilishi shart.
**Talablar:** Saga holatlarini (`saga_state_machine`) boshqaruvchi jadval tuzish, kompensatsiya (Rollback logikasi) mexanizmini SQL orqali ishlab chiqish.
**Yechim (SQL):**
```sql
-- 1. Saga orkestratsiyasi uchun holatlar jadvali
CREATE TABLE IF NOT EXISTS distributed_saga_log (
    saga_id UUID PRIMARY KEY,
    saga_type VARCHAR(50) NOT NULL,
    current_step VARCHAR(50) NOT NULL,
    payload JSONB NOT NULL,
    status VARCHAR(20) NOT NULL, -- 'STARTED', 'COMPLETED', 'FAILED', 'COMPENSATING', 'COMPENSATED'
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

-- Kompensatsiya qadamlari tarixi jadvali
CREATE TABLE IF NOT EXISTS saga_compensation_steps (
    step_id BIGSERIAL PRIMARY KEY,
    saga_id UUID NOT NULL REFERENCES distributed_saga_log(saga_id),
    step_name VARCHAR(50) NOT NULL,
    undo_sql TEXT NOT NULL,
    executed BOOLEAN NOT NULL DEFAULT FALSE,
    executed_at TIMESTAMPTZ
);

-- 2. Saga boshlash va kompensatsiya qadamini ro'yxatga olish funksiyasi
CREATE OR REPLACE FUNCTION initiate_booking_saga(
    p_saga_id UUID,
    p_user_id INT,
    p_flight_id INT,
    p_cost NUMERIC(12, 2)
)
RETURNS VOID AS $$
BEGIN
    -- Saga holatini ochamiz
    INSERT INTO distributed_saga_log (saga_id, saga_type, current_step, payload, status)
    VALUES (
        p_saga_id, 
        'FLIGHT_AND_HOTEL_BOOKING', 
        'FLIGHT_RESERVED', 
        jsonb_build_object('user_id', p_user_id, 'flight_id', p_flight_id, 'cost', p_cost),
        'STARTED'
    );

    -- 1-Qadam uchun teskari kompensatsiya SQL kodini saqlaymiz
    INSERT INTO saga_compensation_steps (saga_id, step_name, undo_sql)
    VALUES (
        p_saga_id, 
        'CANCEL_FLIGHT_RESERVATION',
        format('UPDATE flights SET available_seats = available_seats + 1 WHERE id = %s;', p_flight_id)
    );
END;
$$ LANGUAGE plpgsql;

-- 3. Xatolik yuz berganda kompensatsiyalarni teskari tartibda bajaruvchi protsedura
CREATE OR REPLACE PROCEDURE rollback_saga_compensations(p_saga_id UUID)
LANGUAGE plpgsql AS $$
DECLARE
    r RECORD;
BEGIN
    UPDATE distributed_saga_log 
    SET status = 'COMPENSATING', updated_at = clock_timestamp() 
    WHERE saga_id = p_saga_id;

    -- Teskari tartibda (LIFO) kompensatsiyalarni bajaramiz
    FOR r IN 
        SELECT step_id, step_name, undo_sql 
        FROM saga_compensation_steps 
        WHERE saga_id = p_saga_id AND executed = FALSE 
        ORDER BY step_id DESC 
    LOOP
        RAISE NOTICE 'Kompensatsiya bajarilmoqda: % (SQL: %)', r.step_name, r.undo_sql;
        -- Haqiqiy tizimda kompensatsiya buyrug'i bajariladi:
        -- EXECUTE r.undo_sql;
        
        UPDATE saga_compensation_steps 
        SET executed = TRUE, executed_at = clock_timestamp() 
        WHERE step_id = r.step_id;
    END LOOP;

    UPDATE distributed_saga_log 
    SET status = 'COMPENSATED', updated_at = clock_timestamp() 
    WHERE saga_id = p_saga_id;
END;
$$;
```
**Tushuntirish:** Two-Phase Commit (2PC) qat'iy sinxron va barcha qatnashchilarni qulfda ushlab turuvchi (blocking) protokol bo'lgani sababli yirik taqsimlangan mikroxizmatlarda qulflanishlarga va sekinlashishga olib keladi. Saga Pattern esa "Eventually Consistent" (Vaqt o'tishi bilan kelishiladigan) yondashuvdir. Har bir xizmat o'zining lokal tranzaksiyasini qulflarsiz darhol commit qiladi. Agar keyingi xizmatda xato chiqsa, Saga orkestratori oldingi qadamlarning teskari harakatlarini (masalan, pulni qaytarish, bronni bekor qilish) kompensatsiya sifatida amalga oshiradi. Bu tizim o'tkazuvchanligini 10 barobarga oshiradi.
**Ishlash natijasi:**
```text
psql:CALL rollback_saga_compensations('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11');
NOTICE:  Kompensatsiya bajarilmoqda: CANCEL_FLIGHT_RESERVATION (SQL: UPDATE flights SET available_seats = available_seats + 1 WHERE id = 101;)
CALL
distributed_saga_log holati: COMPENSATED (Tizim ziddiyatsiz barqaror holatga qaytarildi).
```

---

### Topshiriq #1299: Change Data Capture (CDC) va WAL Decoder: `pg_logical_slot_peek_changes` orqali voqealarni uzatish
**Tavsif:** Real vaqt rejimida korxona tranzaksiyalarini Kafka va ElasticSearch tizimlariga sinxronlash talab etiladi. Agar dasturchilar buni `AFTER INSERT/UPDATE` triggerlari orqali qilsa, asosiy bazadagi tranzaksiya vaqti ikki barobarga uzayadi. Baza unumdorligiga ta'sir qilmasdan, to'g'ridan-to'g'ri Write-Ahead Logging (WAL) jurnali oqimini dekodlash (Change Data Capture - CDC) va Debezium/Kafka tizimlariga xom voqealar oqimini uzatish mexanizmini yoqish kerak.
**Talablar:** `wal_level = logical` bo'lishi, `test_decoding` plagini bilan replikatsiya slotini yaratish, tranzaksiya o'zgarishlarini (`INSERT`, `UPDATE`, `DELETE`) JSON/matn ko'rinishida xavfsiz o'qish.
**Yechim (SQL):**
```sql
-- 1. wal_level parametrini tekshirish (logical bo'lishi shart!)
SHOW wal_level;

-- 2. Test uchun biznes tranzaksiyalar jadvali
CREATE TABLE IF NOT EXISTS retail_orders_cdc (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL
);

-- Jadvalning replikatsiya identifikatorini to'liq qilish (UPDATE/DELETE larda eski qator qiymatlarini ham olish uchun)
ALTER TABLE retail_orders_cdc REPLICA IDENTITY FULL;

-- 3. CDC uchun test decoding replikatsiya slotini yaratish
SELECT * FROM pg_create_logical_replication_slot('retail_cdc_slot', 'test_decoding');

-- 4. Jadvalda bir nechta biznes operatsiyalarini bajarish
INSERT INTO retail_orders_cdc (order_id, customer_id, total_amount, status)
VALUES (101, 55, 450.00, 'NEW');

UPDATE retail_orders_cdc 
SET status = 'PAID', total_amount = 440.00 
WHERE order_id = 101;

DELETE FROM retail_orders_cdc 
WHERE order_id = 101;

-- 5. WAL jurnalidan o'zgarishlarni slotni siljitmasdan ko'rib chiqish (PEEK changes)
SELECT 
    lsn, 
    xid, 
    data 
FROM pg_logical_slot_peek_changes('retail_cdc_slot', NULL, NULL);

-- 6. O'zgarishlarni iste'mol qilish (CONSUME / GET changes - o'qilgan o'zgarishlar slotdan o'chiriladi)
SELECT 
    lsn, 
    xid, 
    data 
FROM pg_logical_slot_get_changes('retail_cdc_slot', NULL, NULL);

-- 7. Ish yakunlangach test slotini tozalash
SELECT pg_drop_replication_slot('retail_cdc_slot');
```
**Tushuntirish:** Change Data Capture (CDC) — zamonaviy ma'lumotlar injiniringining eng muhim texnologiyasidir. Ma'lumotlar bazasida har qanday o'zgarish yuz berganda, u birinchi navbatda WAL ga yoziladi. Logical Decoding dvigateli ushbu ikkilik (binary) WAL oqimini o'qiydi va uni dasturlarga tushunarli SQL yoki JSON ko'rinishidagi hodisalarga (Events) aylantiradi. Bu jarayon to'liq asinxron bo'lib, asosiy foydalanuvchi so'rovlariga 0ms kechikish qo'shadi, jadvallarga hech qanday qulf qo'ymaydi va tranzaksiyalar tarixini 100% yo'qotishlarsiz tashqi qidiruv va tahlil tizimlariga uzatadi.
**Ishlash natijasi:**
```text
    lsn    |  xid   |                                                       data                                                        
-----------+--------+-------------------------------------------------------------------------------------------------------------------
 0/1A4B028 | 108420 | BEGIN 108420
 0/1A4B090 | 108420 | table public.retail_orders_cdc: INSERT: order_id[integer]:101 customer_id[integer]:55 total_amount[numeric]:450.00 status[character varying]:'NEW'
 0/1A4B1A0 | 108420 | COMMIT 108420
 0/1A4B210 | 108421 | BEGIN 108421
 0/1A4B290 | 108421 | table public.retail_orders_cdc: UPDATE: old-key: order_id[integer]:101 ... new-tuple: status[character varying]:'PAID'
 0/1A4B3A0 | 108421 | COMMIT 108421
(Barcha hodisalar WAL dan toza oqim sifatida olindi!)
```

---

### Topshiriq #1300: High-Availability (HA) va Zero-Data-Loss Failover: Split-Brain holatini bartaraf etish va Konsensus arxitekturasi
**Tavsif:** Yuqori barqarorlikka ega (High Availability - 99.999%) bank ma'lumotlar bazasi klasterida tarmoq qisqa muddatga uzildi (Network Partition). Natijada eski Primary ham, yangi saylangan Standby ham o'zini "Yagona Boshqaruvchi" (Master) deb hisoblab, ikkalasi ham mustaqil yozishlarni qabul qila boshladi ("Split-Brain" falokati). Ikki serverdagi ma'lumotlar bir-biriga zid bo'lib, ma'lumotlar buzildi. Ushbu falokatning oldini olish uchun Patroni/Raft konsensus uslubidagi himoya, Fencing (STONITH) va `pg_stat_wal_receiver` tahlilini joriy qilish talab qilinadi.
**Talablar:** Standby holatini tekshirish (`pg_is_in_recovery()`), tarmoq uzilganda eski masterni darhol o'ldirish (Node Fencing) va xavfsiz Switchover/Failover mexanizmini boshqarish.
**Yechim (SQL):**
```sql
-- 1. Tugunning hozirgi roli va tiklanish (Recovery / Read-Only) holatini tekshirish
SELECT 
    pg_is_in_recovery() AS is_standby_replica,
    CASE 
        WHEN pg_is_in_recovery() THEN 'STANDBY (Faqat o''qish mumkin)'
        ELSE 'PRIMARY (Yozish va o''qish mumkin)'
    END AS current_node_role;

-- 2. Standby replika qabul qilayotgan WAL oqimi va masterning aloqa holati
SELECT 
    status,
    receive_start_lsn,
    receive_start_tli,
    received_lsn,
    received_tli,
    last_msg_send_time,
    last_msg_receipt_time,
    latest_end_lsn,
    slot_name,
    sender_host,
    sender_port
FROM pg_stat_wal_receiver;

-- 3. Failover va Timeline oshishini (Time Line ID - TLI) tahlil qilish
-- Har safar replika yangi Primary bo'lib ko'tarilganda Timeline ID 1 taga oshadi (masalan, TLI 1 -> TLI 2)
SELECT 
    timeline_id, 
    redo_lsn 
FROM pg_control_checkpoint();

-- 4. Split-Brain'dan himoya: Agar nod masterlikni yo'qotsa, o'zini to'xtatishi kerak
-- Konsensus (Etcd/Consul) sessiyasi yo'qolganda darhol tranzaksiyalarni rad etish qoidasi
CREATE OR REPLACE FUNCTION assert_cluster_primary_lease(p_is_lease_valid BOOLEAN)
RETURNS VOID AS $$
BEGIN
    IF NOT p_is_lease_valid THEN
        -- Tarmoq konsensusini yo'qotgan master darhol qulashi shart (Fencing / Self-Termination)
        RAISE EXCEPTION 'FATAL: DCS (Distributed Consensus) lizingi tugadi! Split-Brain oldini olish uchun yozish to''xtatildi!';
    END IF;
END;
$$ LANGUAGE plpgsql;

-- 5. Xavfsiz nazorat qilingan Switchover (Boshqaruvni navbatchi replikaga topshirish)
-- Masterni xavfsiz demote qilish (Faqat o'qishga o'tkazish):
-- SELECT pg_promote(); -- Ushbu buyruq Standby serverida beriladi va u yangi Primary bo'ladi!
```
**Tushuntirish:** High Availability (HA) klasterlarida eng dahshatli xatolik — bu "Split-Brain" (ikkita bosh miya) holatidir. Tarmoq uzilganda, agar ikkala server ham o'zini Primary deb e'lon qilsa va mijozlardan yozishlarni qabul qilsa, ularning WAL tarixi ikkita alohida tarmoqqa (Diverged Timelines) bo'linib ketadi. Buni keyinchalik avtomatik birlashtirib bo'lmaydi. Shuning uchun zamonaviy arxitekturalarda (Patroni, Raft, Paxos) Quorum (kamida $N/2 + 1$ ovoz) talab qilinadi. Ko'pchilik ovozini yo'qotgan master zudlik bilan o'zini "o'ldirishi" (Fencing / STONITH - Shoot The Other Node In The Head) yoki Read-Only ga o'tishi shart. Yangi master esa Timeline ID sini 1 ga oshirib (`pg_promote()`) tizimni uzluksiz davom ettiradi.
**Ishlash natijasi:**
```text
 is_standby_replica |         current_node_role         
--------------------+-----------------------------------
 f                  | PRIMARY (Yozish va o'qish mumkin)
(1 row)

Timeline va LSN holati:
 timeline_id |  redo_lsn  
-------------+------------
           2 | 0/1A5F0028
(Klaster muvaffaqiyatli Timeline 2 ga o'tdi, Split-Brain xavfi 0%, HA barqarorligi ta'minlandi!)
```
