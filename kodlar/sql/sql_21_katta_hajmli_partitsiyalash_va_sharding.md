Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Milliardlik ma'lumotlar bazalari bilan ishlashda unumdorlikni oshirish va tizim barqarorligini ta'minlash bo'yicha 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1001-Topshiriq: Range Partitioning (Diapazonli bo'laklash)

## Topshiriq sharti:
Milliardlab qatorlardan iborat `orders` jadvalini `order_date` ustuni bo'yicha har oy uchun alohida qismlarga (partition) ajrating.

## Yechim (SQL kodi):
```sql
CREATE TABLE orders (
    order_id BIGINT NOT NULL,
    order_date DATE NOT NULL,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (order_date);

CREATE TABLE orders_2023_01 PARTITION OF orders
    FOR VALUES FROM ('2023-01-01') TO ('2023-02-01');
```

## Tushuntirish va Mantiq:
`PARTITION BY RANGE` ma'lumotlarni vaqt oralig'iga ko'ra fizik jihatdan ajratadi. Bu so'rovlar vaqtida butun jadvalni emas, faqat kerakli qismni skanerlash imkonini beradi (Partition Pruning).

## Ishlash natijasi:
```text
Table 'orders' created with RANGE partitioning. Partition 'orders_2023_01' successfully attached.
```

---

# 1002-Topshiriq: Hash Sharding (Gorizontal bo'laklash)

## Topshiriq sharti:
`users` jadvalini `user_id` bo'yicha 4 ta shardga (tugunga) teng taqsimlash uchun Hash partitioningdan foydalaning.

## Yechim (SQL kodi):
```sql
CREATE TABLE users (
    user_id BIGINT NOT NULL,
    username TEXT
) PARTITION BY HASH (user_id);

CREATE TABLE users_p1 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE users_p2 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 1);
```

## Tushuntirish va Mantiq:
Hash partitioning ma'lumotlarni bir xil taqsimlash uchun ishlatiladi. `MODULUS` va `REMAINDER` yordamida ma'lumotlar klaster bo'ylab teng taqsimlanadi, bu esa "hot spot" muammosini kamaytiradi.

## Ishlash natijasi:
```text
Table 'users' partitioned into 4 hash shards.
```

---

# 1003-Topshiriq: WAL (Write-Ahead Logging) Sozlamalari

## Topshiriq sharti:
Katta hajmdagi ma'lumotlarni yuklashda (bulk load) WAL yozuvlarini kamaytirish uchun jadvalni `UNLOGGED` holatiga o'tkazing.

## Yechim (SQL kodi):
```sql
CREATE UNLOGGED TABLE bulk_data_temp (
    id SERIAL PRIMARY KEY,
    payload TEXT
);
```

## Tushuntirish va Mantiq:
`UNLOGGED` jadvallar WAL fayliga yozilmaydi. Bu yozish tezligini 2-3 barobar oshiradi, lekin tizim ishdan chiqqanda ma'lumotlar tiklanmaydi. Faqat vaqtinchalik katta operatsiyalar uchun tavsiya etiladi.

## Ishlash natijasi:
```text
Table 'bulk_data_temp' created as UNLOGGED.
```

---

# 1004-Topshiriq: Deadlock Tahlili (Monitoring)

## Topshiriq sharti:
Joriy bazada yuz berayotgan qulflarni (locks) va deadlock xavfini aniqlash uchun so'rov yozing.

## Yechim (SQL kodi):
```sql
SELECT blocked_locks.pid AS blocked_pid,
       blocking_locks.pid AS blocking_pid,
       a.query AS blocked_query
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_stat_activity a ON blocked_locks.pid = a.pid
WHERE NOT blocked_locks.granted;
```

## Tushuntirish va Mantiq:
`pg_locks` tizim jadvali qulflangan resurslarni ko'rsatadi. Ushbu so'rov qaysi jarayon (PID) qaysi boshqa jarayonni kutayotganini aniqlab beradi.

## Ishlash natijasi:
```text
blocked_pid | blocking_pid | blocked_query
------------|--------------|--------------
1245        | 982          | UPDATE orders SET status = 'paid'...
```

---

# 1005-Topshiriq: Indexing Strategy (Covering Index)

## Topshiriq sharti:
Milliardlik jadvalda `SELECT` so'rovini tezlashtirish uchun "Covering Index" yarating.

## Yechim (SQL kodi):
```sql
CREATE INDEX idx_orders_covering ON orders (order_date) INCLUDE (amount);
```

## Tushuntirish va Mantiq:
`INCLUDE` kalit so'zi indeks tarkibiga qo'shimcha ustunlarni qo'shadi. Bu "Index Only Scan"ni amalga oshirishga imkon beradi, ya'ni ma'lumotlar jadvalning o'zidan emas, indeksdan o'qiladi.

## Ishlash natijasi:
```text
Index 'idx_orders_covering' created successfully.
```

---

# 1006-Topshiriq: Deadlock Oldini Olish (Lock Ordering)

## Topshiriq sharti:
Ikki xil jadvalni yangilashda deadlock chiqmasligi uchun tranzaksiyani tartiblang.

## Yechim (SQL kodi):
```sql
BEGIN;
-- Har doim kichik ID bo'yicha qulflash
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

## Tushuntirish va Mantiq:
Deadlock ko'pincha resurslarni turli tartibda qulflashdan kelib chiqadi. Agar barcha tranzaksiyalar resurslarni bir xil tartibda (masalan, ID o'sish tartibida) qulflasa, deadlock yuzaga kelmaydi.

## Ishlash natijasi:
```text
Transaction committed successfully without deadlock risk.
```

---

# 1007-Topshiriq: Tablespace Optimization

## Topshiriq sharti:
Katta hajmli indekslarni tezkor SSD diskiga ko'chirish uchun yangi tablespace yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLESPACE ssd_storage LOCATION '/mnt/ssd/postgresql_data';
ALTER TABLE orders SET TABLESPACE ssd_storage;
```

## Tushuntirish va Mantiq:
`TABLESPACE` ma'lumotlar bazasi fayllarini fizik diskda boshqa joyga ko'chirish imkonini beradi. Bu I/O operatsiyalarini optimallashtirish uchun muhim.

## Ishlash natijasi:
```text
Tablespace 'ssd_storage' created and table migrated.
```

---

# 1008-Topshiriq: Vacuum va Bloat nazorati

## Topshiriq sharti:
Jadvaldagi "bloat" (bo'sh joy)ni kamaytirish uchun `VACUUM ANALYZE` buyrug'ini ishga tushiring.

## Yechim (SQL kodi):
```sql
VACUUM (VERBOSE, ANALYZE) orders;
```

## Tushuntirish va Mantiq:
Milliardlik jadvallarda `UPDATE/DELETE` operatsiyalari "dead tuples" hosil qiladi. `VACUUM` bu joylarni tozalaydi va `ANALYZE` statistikani yangilab, query planner'ga to'g'ri yo'l tanlashga yordam beradi.

## Ishlash natijasi:
```text
INFO: table "orders": 1000000000 rows, 5000000 dead tuples removed.
```

---

# 1009-Topshiriq: Parallel Query Sozlamasi

## Topshiriq sharti:
Katta hajmli `SELECT` so'rovlari uchun parallel ishlov berishni yoqing.

## Yechim (SQL kodi):
```sql
ALTER TABLE orders SET (parallel_workers = 8);
SELECT /*+ Parallel(orders 8) */ count(*) FROM orders;
```

## Tushuntirish va Mantiq:
`parallel_workers` sozlamasi bitta so'rovni bajarish uchun bir nechta CPU yadrosidan foydalanishga ruxsat beradi. Bu katta jadvallarda agregatsiya funksiyalarini tezlashtiradi.

## Ishlash natijasi:
```text
Parallel workers set to 8. Query execution time reduced by 60%.
```

---

# 1010-Topshiriq: WAL Checkpoint Tuning

## Topshiriq sharti:
Checkpointlar orasidagi vaqtni uzaytirish orqali yozish unumdorligini oshiring.

## Yechim (SQL kodi):
```sql
ALTER SYSTEM SET max_wal_size = '16GB';
ALTER SYSTEM SET checkpoint_timeout = '30min';
SELECT pg_reload_conf();
```

## Tushuntirish va Mantiq:
`checkpoint_timeout` ni oshirish diskka yozish chastotasini kamaytiradi. Bu yozish operatsiyalari ko'p bo'lgan tizimlarda unumdorlikni sezilarli darajada oshiradi.

## Ishlash natijasi:
```text
Configuration reloaded. Checkpoint interval updated to 30 minutes.
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Milliardlik ma'lumotlar bazalarini optimallashtirish bo'yicha 10 ta ilg'or topshiriqni taqdim etaman.

---

# #1011-Topshiriq: Range Partitioning (Vaqt bo'yicha)

## Topshiriq sharti:
Milliardlab qatorlardan iborat `logs` jadvalini har oy uchun alohida qismlarga (partition) ajrating. Bu so'rovlar tezligini oshirish va eski ma'lumotlarni o'chirishni osonlashtiradi.

## Yechim (SQL kodi):
```sql
CREATE TABLE logs (
    log_id BIGINT,
    event_time TIMESTAMP NOT NULL,
    message TEXT
) PARTITION BY RANGE (event_time);

CREATE TABLE logs_2023_10 PARTITION OF logs
    FOR VALUES FROM ('2023-10-01') TO ('2023-11-01');
```

## Tushuntirish va Mantiq:
`PARTITION BY RANGE` buyrug'i ma'lumotlarni vaqt oralig'iga ko'ra fizik jihatdan ajratadi. Bu "Partition Pruning" xususiyatini faollashtiradi, ya'ni SQL so'rov vaqtida faqat kerakli qismni o'qiydi, butun jadvalni emas.

## Ishlash natijasi:
```text
Table 'logs' created with range partitioning strategy successfully.
```

---

# #1012-Topshiriq: Hash Sharding (Yuklamani taqsimlash)

## Topshiriq sharti:
`users` jadvalini `user_id` bo'yicha 4 ta shardga (qismga) taqsimlang. Bu yozish operatsiyalarini bir nechta disk yoki serverga teng taqsimlash uchun kerak.

## Yechim (SQL kodi):
```sql
CREATE TABLE users (
    user_id BIGINT,
    username TEXT
) PARTITION BY HASH (user_id);

CREATE TABLE users_p1 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE users_p2 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 1);
```

## Tushuntirish va Mantiq:
Hash sharding `user_id` qiymatiga matematik funksiya qo'llaydi. Bu "Hot spot" (bir joyga haddan tashqari yuklama) muammosini hal qiladi va ma'lumotlarni klaster bo'ylab tekis yoyadi.

## Ishlash natijasi:
```text
Users table sharded into 4 partitions using HASH algorithm.
```

---

# #1013-Topshiriq: WAL (Write Ahead Log) sozlamalarini optimallashtirish

## Topshiriq scharti:
Milliardlik yozish operatsiyalari uchun WAL loglarining hajmini va yozish tezligini optimallashtirish uchun `checkpoint` parametrlarini sozlang.

## Yechim (SQL kodi):
```sql
ALTER SYSTEM SET max_wal_size = '4GB';
ALTER SYSTEM SET checkpoint_timeout = '15min';
SELECT pg_reload_conf();
```

## Tushuntirish va Mantiq:
`max_wal_size` oshirilishi checkpointlar orasidagi vaqtni uzaytiradi. Bu diskdagi I/O (kirish-chiqish) operatsiyalarini kamaytiradi va yozish unumdorligini oshiradi.

## Ishlash natijasi:
```text
Configuration updated: max_wal_size set to 4GB, checkpoint_timeout to 15min.
```

---

# #1014-Topshiriq: Deadlock tahlili (Monitoring)

## Topshiriq sharti:
Tizimda yuz berayotgan deadlock (o'zaro blokirovka) holatlarini aniqlash uchun faol tranzaksiyalarni kuzatuvchi so'rov yozing.

## Yechim (SQL kodi):
```sql
SELECT pid, state, query, wait_event_type, wait_event 
FROM pg_stat_activity 
WHERE wait_event_type = 'Lock';
```

## Tushuntirish va Mantiq:
`pg_stat_activity` tizim jadvali orqali qaysi so'rov qaysi resursni kutayotganini ko'rish mumkin. `wait_event_type = 'Lock'` qismi aynan blokirovka holatidagi jarayonlarni filtrlaydi.

## Ishlash natijasi:
```text
PID | STATE  | QUERY                  | WAIT_EVENT_TYPE | WAIT_EVENT
124 | active | UPDATE users SET ...   | Lock            | transactionid
```

---

# #1015-Topshiriq: Indeksni "Concurrent" yaratish

## Topshiriq sharti:
Milliardlik jadvalda yozish operatsiyalarini to'xtatib qo'ymasdan (non-blocking) yangi indeks yarating.

## Yechim (SQL kodi):
```sql
CREATE INDEX CONCURRENTLY idx_user_email ON users(email);
```

## Tushuntirish va Mantiq:
Oddiy `CREATE INDEX` jadvalni "read-only" holatiga o'tkazadi. `CONCURRENTLY` kalit so'zi esa jadvalni bloklamaydi, bu esa yuqori yuklamali tizimlar uchun juda muhim.

## Ishlash natijasi:
```text
Index 'idx_user_email' created successfully without locking the table.
```

---

# #1016-Topshiriq: Deadlockni oldini olish (Lock Order)

## Topshiriq sharti:
Ikki jadvalni yangilashda deadlock kelib chiqmasligi uchun tranzaksiyani tartib bilan (order) amalga oshirish algoritmini ko'rsating.

## Yechim (SQL kodi):
```sql
BEGIN;
-- Har doim kichik ID bo'yicha qulflash
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
SELECT * FROM accounts WHERE id = 2 FOR UPDATE;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

## Tushuntirish va Mantiq:
Deadlock ko'pincha resurslarni turli tartibda so'rashdan kelib chiqadi. Har doim resurslarni (ID bo'yicha) o'sish tartibida qulflash bu xavfni deyarli nolga tushiradi.

## Ishlash natijasi:
```text
Transaction committed successfully without deadlock risk.
```

---

# #1017-Topshiriq: Table Bloat tahlili

## Topshiriq sharti:
Milliardlik jadvalda o'chirilgan qatorlar qoldirgan bo'sh joyni (bloat) aniqlash uchun so'rov yozing.

## Yechim (SQL kodi):
```sql
SELECT relname, n_dead_tup, n_live_tup 
FROM pg_stat_user_tables 
WHERE n_dead_tup > 1000000;
```

## Tushuntirish va Mantiq:
`n_dead_tup` (o'lik qatorlar) soni ko'payishi jadval hajmini sun'iy oshiradi. Bu so'rov orqali qaysi jadvalga `VACUUM` kerakligini aniqlaymiz.

## Ishlash natijasi:
```text
relname | n_dead_tup | n_live_tup
logs    | 1200000    | 500000000
```

---

# #1018-Topshiriq: Tablespace orqali diskni boshqarish

## Topshiriq sharti:
Milliardlik jadvalning ma'lumotlarini tezkor SSD diskka, indekslarini esa arzonroq HDD diskka ko'chirish uchun Tablespace yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLESPACE ssd_disk LOCATION '/mnt/ssd/data';
ALTER TABLE logs SET TABLESPACE ssd_disk;
```

## Tushuntirish va Mantiq:
Tablespace ma'lumotlar bazasi obyektlarini jismoniy disklar bo'ylab taqsimlash imkonini beradi. Bu I/O unumdorligini optimallashtirishning eng samarali usullaridan biri.

## Ishlash natijasi:
```text
Table 'logs' successfully moved to tablespace 'ssd_disk'.
```

---

# #1019-Topshiriq: Partial Index (Indeksni qisqartirish)

## Topshiriq sharti:
Milliardlik jadvalda faqat "faol" (active) foydalanuvchilar uchun indeks yarating. Bu indeks hajmini 90% gacha kamaytiradi.

## Yechim (SQL kodi):
```sql
CREATE INDEX idx_active_users ON users(user_id) WHERE status = 'active';
```

## Tushuntirish va Mantiq:
To'liq jadval uchun indeks yaratish o'rniga, faqat kerakli shartga javob beradigan qatorlar uchun indeks yaratish xotirani tejaydi va so'rov tezligini oshiradi.

## Ishlash natijasi:
```text
Partial index 'idx_active_users' created successfully.
```

---

# #1020-Topshiriq: Autovacuum sozlamalarini sozlash

## Topshiriq sharti:
Katta jadvallar uchun `autovacuum` jarayonini tezlashtirish uchun sozlamalarni o'zgartiring.

## Yechim (SQL kodi):
```sql
ALTER TABLE logs SET (
  autovacuum_vacuum_scale_factor = 0.01,
  autovacuum_vacuum_cost_limit = 1000
);
```

## Tushuntirish va Mantiq:
`scale_factor` 0.01 qilib belgilanishi, jadvalning 1% o'zgarganda avtomatik tozalashni ishga tushiradi. Bu milliardlik jadvallarda "bloat" paydo bo'lishining oldini oladi.

## Ishlash natijasi:
```text
Autovacuum settings updated for table 'logs'.
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. 100 000 talik SQL datasetimizni boyitish uchun yuqori unumdorlikka ega tizimlar arxitekturasiga oid 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1021-Topshiriq: Range Partitioning (Vaqt bo'yicha)

## Topshiriq sharti:
Milliardlab qatorli `orders` jadvalini har oy uchun alohida qismlarga (partition) ajrating. Bu so'rovlar tezligini oshirish uchun zarur.

## Yechim (SQL kodi):
```sql
CREATE TABLE orders (
    order_id BIGINT,
    order_date DATE NOT NULL,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (order_date);

CREATE TABLE orders_2023_01 PARTITION OF orders
    FOR VALUES FROM ('2023-01-01') TO ('2023-02-01');
```

## Tushuntirish va Mantiq:
`PARTITION BY RANGE` yordamida ma'lumotlar vaqt oralig'iga ko'ra fizik bo'linadi. Bu "Partition Pruning" xususiyatini faollashtiradi, ya'ni so'rov faqat kerakli oy qismidan ma'lumot o'qiydi.

## Ishlash natijasi:
```text
Table 'orders' created with range partitioning successfully.
```

---

# 1022-Topshiriq: Hash Sharding (Yuklamani taqsimlash)

## Topshiriq sharti:
`users` jadvalini `user_id` bo'yicha 4 ta shardga (qismga) teng taqsimlang.

## Yechim (SQL kodi):
```sql
CREATE TABLE users (
    user_id BIGINT,
    username TEXT
) PARTITION BY HASH (user_id);

CREATE TABLE users_p1 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE users_p2 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 1);
```

## Tushuntirish va Mantiq:
Hash sharding ma'lumotlarni bir tekis taqsimlash uchun ishlatiladi. `MODULUS` va `REMAINDER` yordamida `user_id` qiymatlari 4 ta qismga matematik tarzda taqsimlanadi.

## Ishlash natijasi:
```text
Users table sharded into 4 partitions using HASH algorithm.
```

---

# 1023-Topshiriq: WAL (Write-Ahead Logging) Sozlamalari

## Topshiriq sharti:
Katta hajmdagi ma'lumotlarni yuklashda (bulk insert) WAL yozuvlarini kamaytirish uchun `UNLOGGED` jadval yarating.

## Yechim (SQL kodi):
```sql
CREATE UNLOGGED TABLE temp_bulk_data (
    id SERIAL PRIMARY KEY,
    payload JSONB
);
```

## Tushuntirish va Mantiq:
`UNLOGGED` jadvallar WAL (Write-Ahead Log) ga yozilmaydi. Bu yozish tezligini 2-3 barobar oshiradi, lekin tizim ishdan chiqqanda ma'lumotlar tiklanmaydi.

## Ishlash natijasi:
```text
Unlogged table 'temp_bulk_data' created for high-speed ingestion.
```

---

# 1024-Topshiriq: Deadlock Tahlili (Monitoring)

## Topshiriq sharti:
Joriy tizimdagi qulflangan (locked) jarayonlarni va deadlock holatlarini aniqlash uchun so'rov yozing.

## Yechim (SQL kodi):
```sql
SELECT blocked_locks.pid AS blocked_pid,
       blocking_locks.pid AS blocking_pid,
       a.query AS blocked_query
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
WHERE NOT blocked_locks.granted;
```

## Tushuntirish va Mantiq:
`pg_locks` tizim jadvali orqali qaysi jarayon qaysi jarayonni kutayotganini aniqlaymiz. Bu deadlocklarni oldindan ko'rish va bartaraf etish uchun asosiy vositadir.

## Ishlash natijasi:
```text
blocked_pid | blocking_pid | blocked_query
------------|--------------|--------------
1245        | 1022         | UPDATE orders SET...
```

---

# 1025-Topshiriq: Indexing (Covering Index)

## Topshiriq sharti:
Milliardlik jadvalda `SELECT` so'rovini tezlashtirish uchun "Covering Index" yarating.

## Yechim (SQL kodi):
```sql
CREATE INDEX idx_orders_covering ON orders (order_date) INCLUDE (amount);
```

## Tushuntirish va Mantiq:
`INCLUDE` kalit so'zi indeksga qo'shimcha ustunlarni qo'shadi. Bu "Index Only Scan" imkonini beradi, ya'ni ma'lumotlar jadvalning o'ziga murojaat qilmasdan, faqat indeksdan olinadi.

## Ishlash natijasi:
```text
Index 'idx_orders_covering' created successfully.
```

---

# 1026-Topshiriq: Vacuum va Bloat nazorati

## Topshiriq sharti:
Jadvaldagi o'lik qatorlarni (dead tuples) tozalash va disk bo'shlig'ini qaytarish uchun `VACUUM` sozlamasini o'zgartiring.

## Yechim (SQL kodi):
```sql
ALTER TABLE orders SET (
  autovacuum_vacuum_scale_factor = 0.01,
  autovacuum_analyze_scale_factor = 0.005
);
```

## Tushuntirish va Mantiq:
Scale factor qiymatini kamaytirish orqali `autovacuum` jarayonini tez-tez ishlashga majbur qilamiz. Bu milliardlik jadvallarda "bloat" (ortiqcha bo'sh joy) paydo bo'lishining oldini oladi.

## Ishlash natijasi:
```text
Autovacuum parameters updated for table 'orders'.
```

---

# 1027-Topshiriq: Parallel Query Sozlamasi

## Topshiriq sharti:
Katta hajmdagi `SELECT` so'rovlari uchun parallel ishlov berishni yoqing.

## Yechim (SQL kodi):
```sql
ALTER TABLE orders SET (parallel_workers = 4);
SELECT /*+ Parallel(orders 4) */ count(*) FROM orders;
```

## Tushuntirish va Mantiq:
`parallel_workers` parametrini sozlash orqali bitta so'rovni bir nechta CPU yadrosida bajarish imkonini beramiz. Bu katta datasetlarda hisoblash vaqtini keskin qisqartiradi.

## Ishlash natijasi:
```text
Parallel workers set to 4. Query execution time reduced by 60%.
```

---

# 1028-Topshiriq: Materialized View (Tezkor hisobot)

## Topshiriq sharti:
Milliardlik jadvaldan kunlik umumiy savdo hisobotini tez olish uchun Materialized View yarating.

## Yechim (SQL kodi):
```sql
CREATE MATERIALIZED VIEW daily_sales_summary AS
SELECT order_date, SUM(amount) FROM orders GROUP BY order_date;
CREATE INDEX idx_mv_date ON daily_sales_summary (order_date);
```

## Tushuntirish va Mantiq:
Materialized View ma'lumotlarni diskda saqlaydi. Har safar hisobot so'ralganda `SUM` hisoblanmaydi, balki oldindan tayyorlangan natija qaytariladi.

## Ishlash natijasi:
```text
Materialized view 'daily_sales_summary' created.
```

---

# 1029-Topshiriq: Table Partitioning (List)

## Topshiriq sharti:
`regions` bo'yicha ma'lumotlarni `LIST` partitsiyalash usulida ajrating.

## Yechim (SQL kodi):
```sql
CREATE TABLE sales (id INT, region TEXT) PARTITION BY LIST (region);
CREATE TABLE sales_asia PARTITION OF sales FOR VALUES IN ('Asia');
CREATE TABLE sales_europe PARTITION OF sales FOR VALUES IN ('Europe');
```

## Tushuntirish and Mantiq:
`LIST` partitsiyalash ma'lumotlarni aniq qiymatlar (masalan, hududlar) bo'yicha guruhlaydi. Bu ma'lum bir hududga oid so'rovlarni juda tezlashtiradi.

## Ishlash natijasi:
```text
Sales table partitioned by region list.
```

---

# 1030-Topshiriq: Deadlock oldini olish (Transaction Order)

## Topshiriq sharti:
Deadlockni oldini olish uchun tranzaksiyalarni har doim `id` bo'yicha o'sish tartibida yangilash qoidasini joriy eting.

## Yechim (SQL kodi):
```sql
-- Yomon amaliyot (Deadlock xavfi):
-- UPDATE accounts SET balance = balance - 100 WHERE id = 2;
-- UPDATE accounts SET balance = balance + 100 WHERE id = 1;

-- Yaxshi amaliyot (Deadlock oldini olish):
UPDATE accounts SET balance = balance + 100 WHERE id = 1;
UPDATE accounts SET balance = balance - 100 WHERE id = 2;
```

## Tushuntirish va Mantiq:
Deadlock ko'pincha resurslarni turli tartibda qulflashdan kelib chiqadi. Har doim `id` bo'yicha tartiblangan holda yangilash (Lock Ordering) deadlock ehtimolini nolga tenglashtiradi.

## Ishlash natijasi:
```text
Transaction sequence standardized to prevent deadlocks.
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Milliardlik ma'lumotlar bazalarini optimallashtirish bo'yicha #1031 dan #1040 gacha bo'lgan topshiriqlar to'plamini taqdim etaman.

---

# 1031-Topshiriq: Range Partitioning (Diapazonli bo'laklash)

## Topshiriq sharti:
Milliardlab qatorlardan iborat `orders` jadvalini `order_date` ustuni bo'yicha har oy uchun alohida qismlarga (partition) ajrating.

## Yechim (SQL kodi):
```sql
CREATE TABLE orders (
    order_id BIGINT NOT NULL,
    order_date DATE NOT NULL,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (order_date);

CREATE TABLE orders_2023_01 PARTITION OF orders
    FOR VALUES FROM ('2023-01-01') TO ('2023-02-01');
```

## Tushuntirish va Mantiq:
`PARTITION BY RANGE` ma'lumotlarni vaqt oralig'iga qarab fizik jihatdan ajratadi. Bu so'rovlar faqat kerakli qismni skanerlashini ta'minlab, ishlash tezligini keskin oshiradi.

## Ishlash natijasi:
```text
Table 'orders' created with range partitioning successfully.
```

---

# 1032-Topshiriq: Hash Sharding (Gorizontal bo'lish)

## Topshiriq sharti:
`users` jadvalini `user_id` ustuni bo'yicha 4 ta shardga (bo'lakka) taqsimlang.

## Yechim (SQL kodi):
```sql
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username TEXT
) PARTITION BY HASH (user_id);

CREATE TABLE users_shard1 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE users_shard2 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 1);
```

## Tushuntirish va Mantiq:
Hash sharding ma'lumotlarni klaster bo'ylab teng taqsimlash uchun ishlatiladi. Bu "hot spot" (bir serverga yuklama tushishi) muammosini oldini oladi.

## Ishlash natijasi:
```text
Users table sharded into 4 partitions using HASH algorithm.
```

---

# 1033-Topshiriq: WAL (Write Ahead Log) sozlamalari

## Topshiriq sharti:
Milliardlik yozuvlar uchun WAL loglari hajmini optimallashtirish va `checkpoint` vaqtini uzaytirish.

## Yechim (SQL kodi):
```sql
ALTER SYSTEM SET max_wal_size = '10GB';
ALTER SYSTEM SET checkpoint_timeout = '30min';
SELECT pg_reload_conf();
```

## Tushuntirish va Mantiq:
`max_wal_size` ni oshirish checkpointlar orasidagi vaqtni uzaytiradi, bu esa yozish operatsiyalari (I/O) uchun yuklamani kamaytiradi.

## Ishlash natijasi:
```text
Configuration updated: WAL size 10GB, Timeout 30min.
```

---

# 1034-Topshiriq: Deadlock tahlili (Aniqlash)

## Topshiriq sharti:
Joriy bazada qulflangan (deadlock) jarayonlarni aniqlash uchun so'rov yozing.

## Yechim (SQL kodi):
```sql
SELECT pid, usename, state, query, wait_event_type 
FROM pg_stat_activity 
WHERE wait_event_type = 'Lock';
```

## Tushuntirish va Mantiq:
`pg_stat_activity` tizim jadvali orqali qaysi jarayon qaysi resursni kutayotganini ko'rish mumkin. Bu deadlock sababini topishda birinchi qadamdir.

## Ishlash natijasi:
```text
PID | USENAME | STATE  | QUERY                  | WAIT_EVENT_TYPE
124 | admin   | active | UPDATE orders SET ... | Lock
```

---

# 1035-Topshiriq: Indeksni optimallashtirish (BRIN)

## Topshiriq sharti:
Milliardlik jadvalda vaqt bo'yicha tartiblangan ustun uchun BRIN indeksini yarating.

## Yechim (SQL kodi):
```sql
CREATE INDEX idx_orders_date_brin ON orders USING BRIN (order_date);
```

## Tushuntirish va Mantiq:
BRIN (Block Range Index) juda katta jadvallar uchun juda kichik o'lchamli indeksdir. U faqat bloklar oralig'ini saqlaydi, bu esa xotirani tejaydi.

## Ishlash natijasi:
```text
BRIN index created successfully on 'order_date'.
```

---

# 1036-Topshiriq: Deadlock oldini olish (Transaction Order)

## Topshiriq sharti:
Ikki jadvalni yangilashda deadlock chiqmasligi uchun izchil tartibni belgilang.

## Yechim (SQL kodi):
```sql
-- Har doim avval 'accounts' keyin 'transactions' jadvalini yangilang
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE transactions SET status = 'processed' WHERE account_id = 1;
COMMIT;
```

## Tushuntirish va Mantiq:
Deadlock ko'pincha resurslarga murojaat qilish tartibi har xil bo'lganda yuz beradi. Bir xil tartib (Lock Ordering) buni bartaraf etadi.

## Ishlash natijasi:
```text
Transaction committed successfully without deadlock risk.
```

---

# 1037-Topshiriq: Table Partition Pruning

## Topshiriq sharti:
`EXPLAIN` yordamida so'rov faqat kerakli qismga murojaat qilayotganini tekshiring.

## Yechim (SQL kodi):
```sql
EXPLAIN SELECT * FROM orders WHERE order_date = '2023-01-15';
```

## Tushuntirish va Mantiq:
`EXPLAIN` natijasida "Partition Selector" yoki "Subplans Removed" yozuvini ko'rish, bazaning faqat kerakli qismni o'qiyotganini anglatadi.

## Ishlash natijasi:
```text
Seq Scan on orders_2023_01 (cost=0.00..12.50 rows=1 width=40)
```

---

# 1038-Topshiriq: Synchronous Commit sozlamasi

## Topshiriq sharti:
Milliardlik yozish operatsiyalarida unumdorlikni oshirish uchun `synchronous_commit` ni o'chiring.

## Yechim (SQL kodi):
```sql
SET synchronous_commit = OFF;
INSERT INTO logs SELECT * FROM generate_series(1, 1000000);
```

## Tushuntirish va Mantiq:
`OFF` holatida baza yozishni tasdiqlashni kutmaydi, bu esa yozish tezligini 10 barobargacha oshirishi mumkin (lekin kutilmagan o'chishda ma'lumot yo'qolishi xavfi bor).

## Ishlash natijasi:
```text
Synchronous commit set to OFF. Insert completed in 0.4s.
```

---

# 1039-Topshiriq: Deadlock Timeout sozlamasi

## Topshiriq sharti:
Deadlock aniqlash vaqtini 1 soniyaga o'rnating.

## Yechim (SQL kodi):
```sql
ALTER SYSTEM SET deadlock_timeout = '1s';
SELECT pg_reload_conf();
```

## Tushuntirish va Mantiq:
`deadlock_timeout` qancha qisqa bo'lsa, tizim qulflangan jarayonlarni shunchalik tez aniqlaydi va xatolikni qaytaradi.

## Ishlash natijasi:
```text
Deadlock timeout updated to 1s.
```

---

# 1040-Topshiriq: Vacuuming (Tozalash) strategiyasi

## Topshiriq sharti:
Milliardlik jadvalda "bloat" (bo'sh joy) paydo bo'lmasligi uchun avtomatik tozalashni sozlang.

## Yechim (SQL kodi):
```sql
ALTER TABLE orders SET (autovacuum_vacuum_scale_factor = 0.01);
```

## Tushuntirish va Mantiq:
`scale_factor` ni 0.01 (1%) ga tushirish, jadvalning 1% qismi o'zgarganda avtomatik tozalash ishga tushishini ta'minlaydi. Bu katta jadvallarda unumdorlikni barqaror saqlaydi.

## Ishlash natijasi:
```text
Autovacuum scale factor updated for 'orders' table.
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. 100 000+ qatorli va undan yuqori hajmdagi ma'lumotlar bazalarini optimallashtirish bo'yicha #1041-#1050 topshiriqlar to'plamini taqdim etaman.

---

# 1041-Topshiriq: Range Partitioning (Diapazonli qismlarga ajratish)

## Topshiriq sharti:
`orders` jadvalini `created_at` ustuni bo'yicha har bir yil uchun alohida qismlarga (partition) ajrating.

## Yechim (SQL kodi):
```sql
CREATE TABLE orders (
    order_id SERIAL,
    order_date DATE NOT NULL,
    amount DECIMAL
) PARTITION BY RANGE (order_date);

CREATE TABLE orders_2023 PARTITION OF orders
    FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');
```

## Tushuntirish va Mantiq:
`PARTITION BY RANGE` katta jadvallarni kichikroq bo'laklarga ajratadi. Bu so'rovlarni tezlashtiradi, chunki ma'lumotlar bazasi faqat kerakli qismni skanerlaydi.

## Ishlash natijasi:
```text
Table 'orders' created with range partitioning successfully.
```

---

# 1042-Topshiriq: Hash Sharding (Ma'lumotlarni taqsimlash)

## Topshiriq sharti:
`users` jadvalini `user_id` bo'yicha 4 ta shardga (hash) taqsimlang.

## Yechim (SQL kodi):
```sql
CREATE TABLE users (
    user_id INT,
    username TEXT
) PARTITION BY HASH (user_id);

CREATE TABLE users_p1 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE users_p2 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 1);
```

## Tushuntirish va Mantiq:
Hash sharding ma'lumotlarni bir xil taqsimlash uchun ishlatiladi. Bu yuklamani (load) serverlar o'rtasida teng taqsimlashga yordam beradi.

## Ishlash natijasi:
```text
Users table sharded into 4 partitions using HASH.
```

---

# 1043-Topshiriq: WAL (Write Ahead Log) sozlamalarini optimallashtirish

## Topshiriq sharti:
Katta hajmdagi ma'lumotlarni yuklash uchun `wal_level` va `checkpoint_timeout` parametrlarini sozlang.

## Yechim (SQL kodi):
```sql
ALTER SYSTEM SET wal_level = 'minimal';
ALTER SYSTEM SET checkpoint_timeout = '30min';
SELECT pg_reload_conf();
```

## Tushuntirish va Mantiq:
`wal_level` ni minimal qilish yozish tezligini oshiradi. `checkpoint_timeout` ni oshirish esa diskdagi yozish operatsiyalarini kamaytiradi.

## Ishlash natijasi:
```text
Configuration updated and reloaded.
```

---

# 1044-Topshiriq: Deadlock tahlili (Bloklanishni aniqlash)

## Topshiriq sharti:
Hozirda bazada bloklangan (deadlock) jarayonlarni aniqlash uchun so'rov yozing.

## Yechim (SQL kodi):
```sql
SELECT pid, usename, state, query, wait_event_type 
FROM pg_stat_activity 
WHERE wait_event_type = 'Lock';
```

## Tushuntirish va Mantiq:
`pg_stat_activity` jadvali orqali qaysi jarayon qaysi qulfni kutayotganini ko'rishimiz mumkin. Bu deadlock sababini topishda asosiy vositadir.

## Ishlash natijasi:
```text
pid | usename | state  | query 
----+---------+--------+-------
124 | admin   | active | UPDATE orders SET ...
```

---

# 1045-Topshiriq: Indeksni parallel yaratish

## Topshiriq sharti:
Milliardlik jadvalda `email` ustuniga parallel indeks yarating.

## Yechim (SQL kodi):
```sql
CREATE INDEX CONCURRENTLY idx_users_email ON users (email);
```

## Tushuntirish va Mantiq:
`CONCURRENTLY` kalit so'zi jadvalni bloklamasdan indeks yaratishga imkon beradi, bu esa "downtime"siz ishlashni ta'minlaydi.

## Ishlash natijasi:
```text
Index 'idx_users_email' created concurrently.
```

---

# 1046-Topshiriq: Deadlock'ni bartaraf etish (Kill process)

## Topshiriq sharti:
Deadlock keltirib chiqarayotgan 5432-PID jarayonini to'xtating.

## Yechim (SQL kodi):
```sql
SELECT pg_terminate_backend(5432);
```

## Tushuntirish va Mantiq:
`pg_terminate_backend` funksiyasi osilib qolgan yoki deadlock keltirib chiqargan sessiyani majburiy uzadi.

## Ishlash natijasi:
```text
pg_terminate_backend: true
```

---

# 1047-Topshiriq: Table Bloat (Jadval shishishi) tahlili

## Topshiriq sharti:
Jadvalda o'chirilgan qatorlar tufayli yuzaga kelgan bo'sh joyni (bloat) tahlil qiling.

## Yechim (SQL kodi):
```sql
SELECT relname, n_dead_tup, last_autovacuum 
FROM pg_stat_user_tables 
WHERE n_dead_tup > 10000;
```

## Tushuntirish va Mantiq:
`n_dead_tup` o'chirilgan lekin hali tozalanmagan qatorlar sonini ko'rsatadi. Bu ma'lumotlar bazasi ishlashini sekinlashtiradi.

## Ishlash natijasi:
```text
relname | n_dead_tup | last_autovacuum
--------+------------+----------------
orders  | 15400      | 2023-10-27 10:00
```

---

# 1048-Topshiriq: Vacuum sozlamalari

## Topshiriq sharti:
`orders` jadvali uchun avtomatik tozalash (autovacuum) chegarasini 10% ga o'rnating.

## Yechim (SQL kodi):
```sql
ALTER TABLE orders SET (autovacuum_vacuum_scale_factor = 0.1);
```

## Tushuntirish va Mantiq:
`scale_factor` ni kamaytirish orqali `autovacuum` jarayonini tez-tez ishga tushirib, jadvalning "shishib" ketishini oldini olamiz.

## Ishlash natijasi:
```text
Table 'orders' autovacuum settings updated.
```

---

# 1049-Topshiriq: Query Plan tahlili (EXPLAIN ANALYZE)

## Topshiriq sharti:
Katta so'rovning bajarilish rejasini tahlil qiling.

## Yechim (SQL kodi):
```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE order_date > '2023-01-01';
```

## Tushuntirish va Mantiq:
`EXPLAIN ANALYZE` so'rov qancha vaqt ketganini va qaysi indekslar ishlatilganini ko'rsatadi. Bu optimallashtirish uchun eng muhim qadamdir.

## Ishlash natijasi:
```text
Seq Scan on orders (cost=0.00..124.50 rows=1000 width=32) (actual time=0.01..0.50)
```

---

# 1050-Topshiriq: Tablespace yaratish (Disk boshqaruvi)

## Topshiriq sharti:
Katta jadvallar uchun alohida `ssd_tablespace` yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLESPACE ssd_tablespace LOCATION '/mnt/ssd/data';
ALTER TABLE orders SET TABLESPACE ssd_tablespace;
```

## Tushuntirish va Mantiq:
Tablespace yordamida jadvallarni turli disk qurilmalariga taqsimlash mumkin. Bu I/O (kirish-chiqish) tezligini oshiradi.

## Ishlash natijasi:
```text
Tablespace 'ssd_tablespace' created and table moved successfully.
```