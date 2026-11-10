# Khorazmiy AI: SQL - Modul 23
## Mavzu: Ma'lumotlar bazasi replikatsiyasi, Logical Decoding, CDC (Debezium), Distributed Queries va Connection Pooling

Salom, men **Khorazmiy AI** loyihasining SQL va taqsimlangan ma'lumotlar bazalari bo'yicha bosh dataset mutaxassisisiz. Ushbu modulda zamonaviy korporativ tizimlarda ma'lumotlar yaxlitligi, yuqori barqarorlik (HA), oqimli o'zgarishlarni tutib olish (CDC), federativ taqsimlangan so'rovlar (FDW) va ulanishlar havuzini (Connection Pooling) chuqur o'rganish uchun ishlab chiqilgan 50 ta (#1101 - #1150) sanoat darajasidagi amaliy topshiriq va yechimlar jamlangan.

---

### Topshiriq #1101: PostgreSQL Physical Streaming Replication va Sinxron Rejimlarini Sozlash
**Tavsif:** Yuqori yuklamali bank tranzaksion tizimida ma'lumotlar yo'qolishiga mutlaqo yo'l qo'ymaslik (RPO=0) va replikatsiya kechikishini nazorat qilish uchun Primary va Standby o'rtasida sinxron va asinxron replikatsiya rejimlarini sozlash talab etiladi.
**Talablar:** wal_level=replica, synchronous_commit parametrlarining turli darajalarini (on, remote_write, remote_apply, off) tahlil qilish va sync_standby_names sozlamalarini o'rnatish.
**Yechim (SQL):**
```sql
-- 1. Primary serverda postgresql.conf asosiy sozlamalari
-- Ushbu parametrlarni qo'llash uchun serverni qayta ishga tushirish (restart) talab etiladi
ALTER SYSTEM SET wal_level = 'replica';
ALTER SYSTEM SET max_wal_senders = 10;
ALTER SYSTEM SET max_replication_slots = 10;
ALTER SYSTEM SET wal_keep_size = '4GB';
ALTER SYSTEM SET archive_mode = 'on';
ALTER SYSTEM SET archive_command = 'test ! -f /mnt/wal_archive/%f && cp %p /mnt/wal_archive/%f';

-- 2. Sinxron replikatsiyani faollashtirish (standby1 va standby2 nomli replikalar uchun)
-- FIRST 1: standby1 birinchi navbatda sinxron bo'ladi, agar u to'xtasa standby2 sinxronlikni oladi
ALTER SYSTEM SET synchronous_standby_names = 'FIRST 1 (standby1, standby2)';

-- 3. Tranzaksiya darajasida xavfsizlik darajasini tanlash:
-- 'remote_apply' -> RPO=0, Standby xotirasiga va diskiga to'liq apply bo'lmaguncha commit tugamaydi
-- 'remote_write' -> Standby disk buferiga yetganda javob qaytaradi (OS keshida bo'lishi mumkin)
-- 'on'           -> Standby diskiga WAL to'liq yozilganda javob beradi (odatdagi qat'iy rejim)
ALTER SYSTEM SET synchronous_commit = 'remote_apply';

-- Sozlamalarni qayta yuklash
SELECT pg_reload_conf();

-- 4. Replikatsiya foydalanuvchisini yaratish (pg_hba.conf da replication ruxsati bo'lishi lozim)
CREATE ROLE repl_user WITH REPLICATION LOGIN PASSWORD 'KhorazmiySecure2026!';

-- 5. Standby serverda primaryga ulanish sozlamasi (postgresql.auto.conf yoki connection string)
-- primary_conninfo = 'host=192.168.1.10 port=5432 user=repl_user password=KhorazmiySecure2026! application_name=standby1'
-- primary_slot_name = 'standby1_slot'
```
**Tushuntirish:** Streaming replication WAL (Write-Ahead Log) bloklarini tarmoq orqali oqimli uzatishga asoslanadi. `synchronous_commit = 'remote_apply'` tranzaksiyani nafaqat Standby diskiga yozilishini, balki uning Standby xotirasida o'quvchi so'rovlar uchun ko'rinadigan bo'lishini kutadi. Bu 'Read-Your-Writes' kafolatini beradi, lekin Primary-dagi kommit kechikishini (latency) oshiradi.

---

### Topshiriq #1102: Replication Lag va LSN Masofasini Monitoring Qilish
**Tavsif:** Analitika so'rovlari o'qiladigan Standby serverida ma'lumotlar eskirib qolmasligini ta'minlash uchun replikatsiya kechikishini (Replication Lag) vaqt va baytlar (LSN diff) miqdorida doimiy kuzatib borish zarur.
**Talablar:** pg_stat_replication va pg_stat_wal_receiver jadvallaridan foydalanib, Primary va Standby tomondan kechikishni hisoblovchi professional SQL monitoring skriptini yozish.
**Yechim (SQL):**
```sql
-- Primary serverda barcha ulangan replikalarning LSN va vaqt kechikishini monitoring qilish
SELECT 
    client_addr AS replica_ip,
    application_name,
    state,
    sync_state,
    sync_priority,
    -- WAL joylashuv nuqtalari
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    -- Bayt hisobida orqada qolish masofasi (Lag in Bytes)
    pg_wal_lsn_diff(sent_lsn, write_lsn) AS write_lag_bytes,
    pg_wal_lsn_diff(sent_lsn, flush_lsn) AS flush_lag_bytes,
    pg_wal_lsn_diff(sent_lsn, replay_lsn) AS replay_lag_bytes,
    -- Vaqt bo'yicha orqada qolish
    write_lag,
    flush_lag,
    replay_lag,
    -- O'qish uchun MB formatida
    round(pg_wal_lsn_diff(sent_lsn, replay_lsn) / (1024.0 * 1024.0), 2) AS replay_lag_mb
FROM pg_stat_replication;

-- Standby serverning o'zida oxirgi qabul qilingan va replay qilingan vaqtni tekshirish
SELECT 
    now() - pg_last_xact_replay_timestamp() AS replication_time_delay,
    pg_last_wal_receive_lsn() AS last_received_lsn,
    pg_last_wal_replay_lsn() AS last_replayed_lsn,
    pg_wal_lsn_diff(pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn()) AS standby_pending_bytes,
    pg_is_wal_replay_paused() AS is_replay_paused;
```
**Tushuntirish:** `pg_wal_lsn_diff()` ikkita Log Sequence Number (LSN) orasidagi baytlar farqini hisoblaydi. `write_lag` - tarmoq kechikishini, `flush_lag` - Standby diski tezligini, `replay_lag` esa Standby CPU/disk resurslarining WAL tranzaksiyalarini bazaga qayta qo'llash tezligini bildiradi. Replay lag oshib ketsa, standby serverda og'ir o'qish so'rovlari yoki resurs yetishmovchiligi yuzaga kelgan bo'ladi.

---

### Topshiriq #1103: Hot Standby Feedback va Replikatsiya Mojarolarini (Replication Conflict) Bartaraf Etish
**Tavsif:** Standby replikasida uzoq davom etuvchi analitik so'rovlar bajarilayotganda Primary serverdagi VACUUM eski qatorlarni tozalab tashlasa, Standbyda 'canceling statement due to conflict with recovery' xatosi yuzaga keladi.
**Talablar:** hot_standby_feedback, max_standby_streaming_delay va max_standby_archive_delay parametrlarini optimal sozlash hamda nizolarni pg_stat_database_conflicts jadvali orqali kuzatish.
**Yechim (SQL):**
```sql
-- 1. Standby serverida Hot Standby ziddiyatlarini boshqarish parametrlari
-- (postgresql.conf yoki ALTER SYSTEM orqali)

-- Standby Primary-ga o'zida hozirda qaysi tranzaksiya o'qilayotgani haqida xabar beradi,
-- natijada Primary VACUUM jarayoni o'sha qatorlarni o'chirmay turadi
ALTER SYSTEM SET hot_standby_feedback = 'on';

-- Agar nizo yuz bersa, Standby so'rovni bekor qilishdan oldin kutadigan maksimal vaqt (masalan, 30 soniya)
ALTER SYSTEM SET max_standby_streaming_delay = '30000ms';
ALTER SYSTEM SET max_standby_archive_delay = '60000ms';

-- Sozlamalarni yangilash
SELECT pg_reload_conf();

-- 2. Replikatsiya sababli bekor qilingan so'rovlar statistikasini kuzatish
SELECT 
    datname,
    confl_tablespace AS tablespace_conflicts,
    confl_lock AS lock_conflicts,
    confl_snapshot AS snapshot_conflicts,
    confl_bufferpin AS bufferpin_conflicts,
    confl_deadlock AS deadlock_conflicts
FROM pg_stat_database_conflicts
WHERE datname = current_database();

-- 3. Standbyda uzoq davom etayotgan qulflarni va to'sqinlik qiluvchi sessiyalarni aniqlash
SELECT 
    pid, 
    usename, 
    now() - xact_start AS transaction_age, 
    now() - query_start AS query_age, 
    state, 
    query 
FROM pg_stat_activity 
WHERE backend_type = 'client backend' 
  AND state != 'idle' 
ORDER BY query_age DESC 
LIMIT 5;
```
**Tushuntirish:** `hot_standby_feedback=on` Standby'dagi uzoq so'rovlarni bekor qilinishidan himoya qiladi. Biroq, bu Primary serverda 'table bloat' (jadval shishishi) xavfini keltirib chiqarishi mumkin, chunki VACUUM Standby bitmaguncha 'dead tuples'larni o'chira olmaydi. Shuning uchun `max_standby_streaming_delay` orqali muvozanat saqlanadi.

---

### Topshiriq #1104: Physical Replication Slot Yaratish va Monitoring Qilish
**Tavsif:** Tarmoqdagi nosozlik tufayli Standby uzoq vaqt Primarydan uzilib qolganda, Primary o'z WAL fayllarini o'chirib yubormasligi va replikatsiya buzilmasligi uchun Physical Replication Slot mexanizmini joriy qilish kerak.
**Talablar:** pg_create_physical_replication_slot orqali slot yaratish, pg_replication_slots jadvalini monitoring qilish va zaxira WAL hajmini nazorat qilish.
**Yechim (SQL):**
```sql
-- 1. Primary serverda jismoniy replikatsiya slotini yaratish
-- immediately_reserve = true bo'lsa, slot shu zahotiyoq WAL saqlashni boshlaydi
SELECT pg_create_physical_replication_slot(
    slot_name => 'standby_dr_slot',
    immediately_reserve => true,
    temporary => false
);

-- 2. Mavjud replikatsiya slotlarining holatini va ushlab turilgan WAL hajmini tekshirish
SELECT 
    slot_name,
    plugin,
    slot_type,
    active,
    active_pid,
    restart_lsn,
    confirmed_flush_lsn,
    wal_status,
    -- Slot qancha WAL hajmini diskda ushlab turibdi
    round(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) / (1024.0 * 1024.0 * 1024.0), 2) AS retained_wal_gb
FROM pg_replication_slots
WHERE slot_type = 'physical';

-- 3. Xavfli (nofaol va diskni to'ldirayotgan) slotlarni aniqlash va xavfsiz o'chirish
DO $$
DECLARE
    r RECORD;
    v_diff_gb NUMERIC;
BEGIN
    FOR r IN SELECT slot_name, restart_lsn, active FROM pg_replication_slots WHERE slot_type = 'physical' LOOP
        IF NOT r.active THEN
            v_diff_gb := round(pg_wal_lsn_diff(pg_current_wal_lsn(), r.restart_lsn) / (1024.0 * 1024.0 * 1024.0), 2);
            -- Agar faol bo'lmagan slot 50 GB dan ko'p WAL ushlab turgan bo'lsa, ogohlantirish berish
            IF v_diff_gb > 50 THEN
                RAISE WARNING 'Slot % faol emas va % GB WAL ushlab turibdi! Disk to`lib ketish xavfi mavjud.', r.slot_name, v_diff_gb;
            END IF;
        END IF;
    END LOOP;
END $$;

-- 4. Keraksiz replikatsiya slotini o'chirish
-- SELECT pg_drop_replication_slot('standby_dr_slot');
```
**Tushuntirish:** Replication Slot Primary serverga Standby oxirgi marta qaysi LSN gacha WAL o'qiganini bildiradi. Primary bu nuqtadan keyingi WAL fayllarni diskdan o'chirmaydi. Agar Standby butunlay o'chib qolsa va slot faol qolaversa, Primary diski WAL fayllar bilan to'lib, butun ma'lumotlar bazasi to'xtab qolishi mumkin. Shuning uchun slot monitoringi o'ta muhim.

---

### Topshiriq #1105: Standby Serverni Primary Qilib Ko'tarish (Failover/Promote) va pg_promote()
**Tavsif:** Asosiy Primary server jiddiy apparat nosozligiga uchraganda, xizmat ko'rsatish uzilishini minimallashtirish uchun eng yangi LSN ga ega bo'lgan Standby serverini darhol yangi Primary qilib ko'tarish kerak.
**Talablar:** PostgreSQL 12+ dagi pg_promote() funksiyasidan foydalanish, kutish vaqtini (wait_seconds) belgilash va tugun yangi Primary holatiga o'tganligini tekshirish.
**Yechim (SQL):**
```sql
-- Standby serverda bajariladigan amallar:

-- 1. Server haqiqatdan ham Standby (qabul qiluvchi) rejimida ekanligini tasdiqlash
SELECT pg_is_in_recovery() AS is_standby;

-- 2. Standby qabul qilgan barcha WAL yozuvlarini bazaga to'liq yozib tugatishini (replay) kutish
-- Agar replay to'xtatilgan bo'lsa, qayta yoqish
SELECT CASE WHEN pg_is_wal_replay_paused() THEN pg_wal_replay_resume() ELSE true END AS resume_status;

-- 3. pg_promote funksiyasi orqali Standby'ni Primary qilib ko'tarish
-- wait = true va wait_seconds = 60: yangi Timeline yaratilib, bazaga yozish ochilguncha kutadi
SELECT pg_promote(wait => true, wait_seconds => 60);

-- 4. Serverning yangi holatini tekshirish (false qaytishi kerak, ya'ni u endi Primary)
SELECT 
    pg_is_in_recovery() AS is_standby,
    CASE 
        WHEN NOT pg_is_in_recovery() THEN 'Muvaffaqiyatli: Server yangi PRIMARY holatiga o`tdi!'
        ELSE 'Xatolik: Server hali ham kutish rejimida!'
    END AS status;

-- 5. Yangi Timeline (TLI) o'zgarganligini WAL fayl nomidan tekshirish
SELECT 
    timeline_id,
    redo_lsn
FROM pg_control_checkpoint();
```
**Tushuntirish:** `pg_promote()` funksiyasi klaster fayl tizimidagi `standby.signal` faylini o'chiradi va Standby-ni yangi Timeline ID (TLI) bilan ochadi. Yangi Timeline eski Primary qayta tiklangan taqdirda ularning WAL yozuvlari bir-biri bilan chalkashib ketmasligini ta'minlaydi.

---

### Topshiriq #1106: Kaskadli Replikatsiya (Cascading Replication) Arxitekturasini Tashkil Qilish
**Tavsif:** Bosh ofisdagi Primary serverga o'nlab hududiy filiallar to'g'ridan-to'g'ri ulansa, markaziy tarmoq o'tkazuvchanligi va CPU zo'riqadi. Shu sababli, oraliq Standby orqali kaskadli replikatsiya zanjirini qurish talab etiladi.
**Talablar:** Primary -> Intermediate Standby (Relay) -> Leaf Standby zanjirini sozlash, max_wal_senders parametrlarini to'g'ri taqsimlash.
**Yechim (SQL):**
```sql
-- 1. Intermediate Standby (Relay tugun) postgresql.conf sozlamalari
-- Bu tugun ham boshqalar uchun WAL tarqatuvchi (wal_sender) bo'lib xizmat qiladi
ALTER SYSTEM SET hot_standby = 'on';
ALTER SYSTEM SET max_wal_senders = 5;
ALTER SYSTEM SET max_replication_slots = 5;
ALTER SYSTEM SET wal_level = 'replica';
-- WAL qabul qilinganda uni darhol kaskad replikalarga yuborish
ALTER SYSTEM SET wal_sender_timeout = '60s';

-- 2. Leaf Standby (oxirgi filial tugun) sozlamasi
-- U Primary-ga emas, Intermediate Standby IP manziliga ulanadi
-- primary_conninfo = 'host=192.168.2.20 port=5432 user=repl_user application_name=leaf_standby_samarkand'

-- 3. Intermediate Standby serverida o'ziga ulangan quyi replikalarni tekshirish
SELECT 
    client_addr AS leaf_replica_ip,
    application_name,
    state,
    pg_wal_lsn_diff(pg_last_wal_receive_lsn(), replay_lsn) AS cascade_delay_bytes,
    replay_lag
FROM pg_stat_replication;

-- 4. Kaskad zanjiridagi umumiy kechikishni nazorat qiluvchi SQL ko'rinishi
CREATE OR REPLACE VIEW v_cascading_health AS
SELECT 
    pg_is_in_recovery() AS is_in_recovery,
    pg_last_wal_receive_lsn() AS upstream_received_lsn,
    pg_last_wal_replay_lsn() AS local_replayed_lsn,
    (SELECT count(*) FROM pg_stat_replication) AS downstream_leaves_connected;

SELECT * FROM v_cascading_health;
```
**Tushuntirish:** Kaskadli replikatsiya arxitekturasi Primary serverdagi tarmoq I/O yuklamasini keskin kamaytiradi. Intermediate tugun Primarydan bir marotaba WAL blokini qabul qiladi va uni o'z navbatida barcha quyi filial Standby'lariga tarqatadi. Bunda faqat asinxron replikatsiya qo'llaniladi.

---

### Topshiriq #1107: Kechiktirilgan Replikatsiya (Delayed Standby) bilan Falokatdan Qutqarish
**Tavsif:** Ishlab chiqarish (Production) bazasida inson omili sababli tasodifan xato `DROP TABLE` yoki `DELETE` bajarilsa, sinxron replika ham bir zumda o'zgaradi. Shu sababli ma'lumotlarni 4 soat kechikish bilan o'qiydigan Delayed Standby serverini sozlash zarur.
**Talablar:** recovery_min_apply_delay parametri yordamida replikatsiyani kechiktirish va kutilmagan falokat paytida to'xtash nuqtasini boshqarish.
**Yechim (SQL):**
```sql
-- Standby serverda postgresql.conf (yoki ALTER SYSTEM) sozlamasi
-- WAL qabul qilinadi, lekin uni bazaga qo'llash (replay) belgilangan vaqtga kechiktiriladi
ALTER SYSTEM SET recovery_min_apply_delay = '4h'; -- 4 soat kechikish

-- Sozlamalarni yangilash
SELECT pg_reload_conf();

-- Holatni monitoring qilish: Standby qancha kechikayotgani va hozirgi replay holati
SELECT 
    now() AS current_system_time,
    pg_last_xact_replay_timestamp() AS last_replayed_xact_time,
    now() - pg_last_xact_replay_timestamp() AS effective_delay,
    pg_last_wal_receive_lsn() AS received_lsn,
    pg_last_wal_replay_lsn() AS replayed_lsn;

-- Agar Production bazasida soat 14:15 da tasodifan xato sodir bo'lsa:
-- Darhol Delayed Standby-da replay jarayonini to'xtatish lozim!
SELECT pg_wal_replay_pause();

-- Replay to'xtatilganligini tasdiqlash
SELECT pg_is_wal_replay_paused();

-- Endi ma'lumotlar bazasini 14:14 holatiga qadar o'tkazib (PITR recovery_target_time), 
-- kerakli jadvallarni pg_dump orqali qutqarib olish mumkin!
```
**Tushuntirish:** `recovery_min_apply_delay` WAL fayllarini tarmoq orqali qabul qilishni to'xtatmaydi (shuning uchun LSN farqi minimal bo'lishi mumkin), faqat ularni Standby diskiga qayta o'qish (replay) vaqtini sun'iy kechiktiradi. Bu PITR (Point-in-Time Recovery) qilishdan ko'ra 10 barobar tezroq falokatdan chiqish imkonini beradi.

---

### Topshiriq #1108: pg_rewind Mexanizmi Bilan Split-Brain Tugunini Qayta Sinxronlash
**Tavsif:** Failover sodir bo'lgandan so'ng, sobiq Primary server qayta ishga tushsa, uning xotirasida yangi Primaryga kirmagan 'yetim' tranzaksiyalar (diverged history) bo'lishi mumkin. Butun bazani qayta yuklamasdan faqat o'zgargan bloklarni orqaga qaytarish talab etiladi.
**Talablar:** pg_rewind ishlashi uchun zarur bo'lgan wal_log_hints parametrini yoqish, ajralgan bloklarni aniqlash va Standby sifatida qayta ulash.
**Yechim (SQL):**
```sql
-- 1. Barcha serverlarda pg_rewind ishlashi uchun oldindan wal_log_hints yoqilgan bo'lishi shart
ALTER SYSTEM SET wal_log_hints = 'on';
SELECT pg_reload_conf();

-- 2. Serverda oxirgi checkpoint va Timeline holatini tekshirish
SELECT 
    checkpoint_lsn,
    redo_lsn,
    timeline_id
FROM pg_control_checkpoint();

-- 3. Shell orqali sobiq Primary serverda pg_rewind ishga tushirish (Konseptual buyruq):
-- pg_rewind --target-pgdata=/var/lib/postgresql/data \
--           --source-server='host=192.168.1.20 port=5432 user=postgres dbname=postgres' \
--           --progress

-- 4. pg_rewind ishlaganidan so'ng sobiq Primary tugunini yangi Standby sifatida belgilash:
-- Fayl yaratiladi: touch /var/lib/postgresql/data/standby.signal
-- postgresql.auto.conf fayliga yangi primary conninfo yoziladi:
-- primary_conninfo = 'host=192.168.1.20 port=5432 user=repl_user password=Secret'

-- 5. Qayta ulanganidan so'ng yangi Standby sifatida muvaffaqiyatli ulanganini tekshirish
SELECT 
    pg_is_in_recovery() AS is_standby,
    pg_last_wal_receive_lsn(),
    pg_last_wal_replay_lsn();
```
**Tushuntirish:** `pg_rewind` ikki serverning WAL ajralgan (fork bo'lgan) nuqtasini topadi va sobiq Primary-dagi faqat o'zgargan disk bloklarini yangi Primary'dan nusxalab oladi. Bu yuzlab gigabaytli bazani tarmoq orqali qayta yuklash (pg_basebackup) o'rniga bir necha soniyada tugunni klasterga qaytarish imkonini beradi.

---

### Topshiriq #1109: Standby Replikatsiyada wal_keep_size va WAL Arxivlash Strategiyasi
**Tavsif:** Tarmoqdagi uzilish paytida Primary serverdagi WAL aylanmasi tezlashib ketsa, Standby kerakli WAL segmentlarini topa olmay replikatsiya to'xtab qolishi mumkin. Buni bartaraf qilish uchun xotira va arxiv aralash strategiyasini ishlab chiqish kerak.
**Talablar:** wal_keep_size parametrini hisoblash, pg_stat_archiver orqali arxiv holatini tekshirish va xavfsiz tozalash chegaralarini belgilash.
**Yechim (SQL):**
```sql
-- 1. Primary serverda WAL saqlash parametrlarini belgilash
-- Har bir WAL segmenti 16MB. 8GB = 512 ta fayl kafolatlangan saqlanadi
ALTER SYSTEM SET wal_keep_size = '8192MB';
ALTER SYSTEM SET max_slot_wal_keep_size = '32768MB'; -- Slotlar xatoga uchrasa disk to'lmasligi uchun cheklov
SELECT pg_reload_conf();

-- 2. WAL arxivlash muvaffaqiyati va xatoliklarini monitoring qilish
SELECT 
    archived_count,
    last_archived_wal,
    last_archived_time,
    failed_count,
    last_failed_wal,
    last_failed_time,
    now() - last_archived_time AS time_since_last_archive
FROM pg_stat_archiver;

-- 3. Hozirda server diskida jami qancha WAL fayl borligini hisoblash
SELECT 
    count(*) AS wal_file_count,
    pg_size_pretty(count(*) * 16 * 1024 * 1024) AS total_wal_disk_size
FROM pg_ls_waldir();

-- 4. Arxivlashda xatolik yuz bersa, ogohlantiruvchi tekshiruv
DO $$
DECLARE
    v_failed_count BIGINT;
BEGIN
    SELECT failed_count INTO v_failed_count FROM pg_stat_archiver;
    IF v_failed_count > 0 THEN
        RAISE WARNING 'Diqqat: WAL arxivlashda % ta xatolik qayd etilgan! Arxiv diskini tekshiring.', v_failed_count;
    END IF;
END $$;
```
**Tushuntirish:** `wal_keep_size` Standby uzilib qolganda Primary diskida minimal saqlanadigan WAL hajmini kafolatlaydi. Biroq eng ishonchli usul - replication slot va doimiy `archive_command` (masalan, pgBackRest yoki WAL-G) birgalikda ishlatilishidir. `max_slot_wal_keep_size` esa nosoz Standby butun Primary diskini to'ldirib yuborishidan himoya qiladi.

---

### Topshiriq #1110: Sinxron Replikatsiyada Kvorum (Quorum-based Replication) Sozlash
**Tavsif:** Uchta turli Data-Markazda joylashgan replikalar mavjud bo'lganda, tranzaksiya tasdiqlanishi uchun istalgan ikkita replika javob berishi kifoya qiladigan Kvorum tizimini o'rnatish lozim.
**Talablar:** synchronous_standby_names = 'ANY 2 (dc1_node, dc2_node, dc3_node)' konfiguratsiyasini joriy qilish va kvorum holatini tekshirish.
**Yechim (SQL):**
```sql
-- 1. Kvorum asosidagi sinxron replikatsiyani yoqish
-- ANY 2 (...) -> ko'rsatilgan replikalardan ixtiyoriy 2 tasi tranzaksiyani qabul qilsa commit muvaffaqiyatli hisoblanadi
ALTER SYSTEM SET synchronous_standby_names = 'ANY 2 (node_dc1, node_dc2, node_dc3)';
SELECT pg_reload_conf();

-- 2. Hozirda qaysi replikalar kvorumda ishtirok etayotganini tahlil qilish
SELECT 
    application_name,
    client_addr,
    state,
    sync_state, -- 'quorum' qiymatini ko'rsatishi lozim
    sync_priority,
    pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS lag_bytes
FROM pg_stat_replication;

-- 3. Sinxron kutish vaqtini cheklash uchun sessiya darajasidagi sozlama
-- Agar replikalar javob bermasa, butun ilova qotib qolmasligi uchun timeout
SET statement_timeout = '5000ms';

-- Tranzaksiya testi
BEGIN;
INSERT INTO audit_log (event, created_at) VALUES ('QUORUM_TEST_TX', now());
COMMIT; -- Ushbu nuqtada 3 ta replikadan kamida 2 tasi WAL'ni tasdiqlashi shart
```
**Tushuntirish:** Kvorum replikatsiyasi (`ANY N`) bitta replika to'xtab qolganda Primary serverning qotib qolishining (lockup) oldini oladi. `FIRST N` dan farqli ravishda, tarmoq bo'yicha eng tezkor javob bergan replikalar tanlanadi, bu esa geo-taqsimlangan yuqori barqarorlikdagi klasterlar uchun eng yaxshi yechimdir.

---

### Topshiriq #1111: Mantiqiy Replikatsiya: CREATE PUBLICATION Bilan Ma'lum Jadvallarni Ommaga Chiqarish
**Tavsif:** Jismoniy replikatsiyada butun klaster nusxalanadi, biroq mikroxizmatlar arxitekturasida faqat ma'lum bir domen jadvallari (masalan, `users` va `accounts`) boshqa xizmatga uzatilishi kerak.
**Talablar:** wal_level=logical sozlamasini talab qilish, alohida jadvallar uchun PUBLICATION yaratish va DML amallarini (INSERT, UPDATE, DELETE, TRUNCATE) filtrlab ommaga chiqarish.
**Yechim (SQL):**
```sql
-- 1. Nashriyotchi (Publisher) serverda tayyorgarlik
ALTER SYSTEM SET wal_level = 'logical';
-- Server qayta ishga tushirilishi kerak

-- 2. Sinov jadvallarini yaratish
CREATE TABLE billing_customers (
    customer_id BIGSERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    balance NUMERIC(15,2) DEFAULT 0.00,
    created_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

CREATE TABLE billing_invoices (
    invoice_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT REFERENCES billing_customers(customer_id),
    amount NUMERIC(15,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'DRAFT',
    issued_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- 3. Jadvallarni o'z ichiga olgan Publication yaratish
-- WITH (publish = 'insert, update, delete') orqali TRUNCATE amallarini replikatsiyadan chiqarib tashlash
CREATE PUBLICATION pub_billing_core 
FOR TABLE billing_customers, billing_invoices
WITH (publish = 'insert, update, delete');

-- 4. Publication holatini va unga biriktirilgan jadvallarni tekshirish
SELECT 
    pubname,
    puballtables,
    pubinsert,
    pubupdate,
    pubdelete,
    pubtruncate
FROM pg_publication
WHERE pubname = 'pub_billing_core';

SELECT 
    schemaname,
    tablename
FROM pg_publication_tables
WHERE pubname = 'pub_billing_core';
```
**Tushuntirish:** `CREATE PUBLICATION` PostgreSQL mantiqiy replikatsiyasining boshlang'ich nuqtasidir. Jismoniy replikatsiyadan farqli o'laroq, u qator darajasidagi o'zgarishlarni abstrakt mantiqiy formatda uzatadi. Bu turli versiyadagi va turli arxitekturadagi PostgreSQL instansiyalari o'rtasida selektiv ma'lumot uzatish imkonini beradi.

---

### Topshiriq #1112: CREATE SUBSCRIPTION Orqali Obunani Sozlash va Mantiqiy Slot Integratsiyasi
**Tavsif:** Boshqa serverda joylashgan tahliliy ma'lumotlar ombori (DWH) asosiy bazadagi `pub_billing_core` nashriga ulanib, ma'lumotlarni real vaqtda qabul qilishi va dastlabki ma'lumotlarni avtomatik nusxalashi kerak.
**Talablar:** Subscriber serverida CREATE SUBSCRIPTION yaratish, copy_data parametrini boshqarish va obunachi xizmatining holatini tekshirish.
**Yechim (SQL):**
```sql
-- Obunachi (Subscriber) serverda bajariladi:

-- 1. Qabul qiluvchi tomonda xuddi shu nom va ustunlarga ega jadvallar yaratiladi
CREATE TABLE billing_customers (
    customer_id BIGSERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    balance NUMERIC(15,2) DEFAULT 0.00,
    created_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

CREATE TABLE billing_invoices (
    invoice_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT REFERENCES billing_customers(customer_id),
    amount NUMERIC(15,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'DRAFT',
    issued_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- 2. Asosiy serverga ulanish obunasini yaratish
-- copy_data = true: jadvallardagi mavjud ma'lumotlarni avtomatik dastlabki nusxalaydi
-- create_slot = true: Publisher serverda avtomatik logical replication slot ochadi
CREATE SUBSCRIPTION sub_billing_analytics
CONNECTION 'host=192.168.1.10 port=5432 dbname=production user=repl_user password=SecurePass2026!'
PUBLICATION pub_billing_core
WITH (
    copy_data = true,
    create_slot = true,
    enabled = true,
    slot_name = 'sub_billing_analytics_slot'
);

-- 3. Obunaning holatini va jadval sinxronizatsiya bosqichini tekshirish
SELECT 
    subid,
    subname,
    subenabled,
    subslotname,
    subconninfo
FROM pg_subscription
WHERE subname = 'sub_billing_analytics';

-- Har bir jadvalning dastlabki ko'chish (copy) holati (r=ready, d=copying, s=synchronized)
SELECT 
    srsubid::regnamespace AS sub_schema,
    srrelid::regclass AS table_name,
    srsubstate AS sync_state,
    srsublsn AS sync_lsn
FROM pg_subscription_rel;
```
**Tushuntirish:** `CREATE SUBSCRIPTION` jarayoni orqa fonda `logical replication worker` jarayonini ishga tushiradi. Agar `copy_data=true` bo'lsa, avval mavjud qatorlar oqim orqali jadvalga nusxalanadi (`srsubstate='s'`), so'ngra streaming rejimiga o'tib, doimiy o'zgarishlarni qabul qila boshlaydi (`srsubstate='r'`).

---

### Topshiriq #1113: Mantiqiy Replikatsiyada Qator Darajasidagi Filtrlash (Row Filters WHERE Clause)
**Tavsif:** Ko'p ijarachili (Multi-tenant) bulutli tizimda har bir hududiy filial faqat o'ziga tegishli (`region_id = 'TOSHKENT'`) mijozlar ma'lumotlarini qabul qilishi, boshqa hududlar ma'lumotlari esa tarmoq orqali o'tmasligi lozim.
**Talablar:** PostgreSQL 15+ dagi qator filtri (Row Filter WHERE clause) yordamida PUBLICATION yaratish va xavfsiz ma'lumot segmentatsiyasini o'rnatish.
**Yechim (SQL):**
```sql
-- Publisher serverda:

-- 1. Ko'p hududli mijozlar jadvali
CREATE TABLE regional_orders (
    order_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    region_code VARCHAR(20) NOT NULL,
    order_amount NUMERIC(12,2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- 2. Faqat Toshkent hududiga oid va bekor qilinmagan buyurtmalarni replikatsiya qilish
CREATE PUBLICATION pub_orders_toshkent
FOR TABLE regional_orders WHERE (region_code = 'UZ-TK' AND status != 'CANCELLED');

-- 3. Faqat Samarqand hududiga oid buyurtmalar uchun alohida publication
CREATE PUBLICATION pub_orders_samarkand
FOR TABLE regional_orders WHERE (region_code = 'UZ-SM' AND status != 'CANCELLED');

-- 4. Publication filtr qoidasini tekshirish
SELECT 
    p.pubname,
    t.schemaname,
    t.tablename,
    t.rowfilter
FROM pg_publication p
JOIN pg_publication_tables t ON p.pubname = t.pubname
WHERE p.pubname IN ('pub_orders_toshkent', 'pub_orders_samarkand');

-- 5. Shartni keyinchalik o'zgartirish (masalan, status tekshiruvini olib tashlash)
ALTER PUBLICATION pub_orders_toshkent 
ALTER TABLE regional_orders SET WHERE (region_code = 'UZ-TK');
```
**Tushuntirish:** Row Filtering replikatsiya oqimidan keraksiz qatorlarni server yadrosida (WAL reader darajasida) filtrlab tashlaydi. Bu orqali tarmoq trafiki, Subscriber diski va CPU resurslari tejaladi, shuningdek maxfiy ma'lumotlar ruxsat etilmagan quyi tugunlarga yetib bormaydi.

---

### Topshiriq #1114: Ustunlar Ro'yxatini Cheklash (Column Lists in Logical Publications)
**Tavsif:** Mijozlar jadvalida shaxsiy identifikatsiya ma'lumotlari (PINFL, pasport seriyasi) va moliyaviy ma'lumotlar mavjud. Ommaviy tahliliy bazaga faqat mijozning ID raqami, faoliyat sohasi va ro'yxatdan o'tgan sanasi replikatsiya qilinishi shart.
**Talablar:** PostgreSQL 15+ dagi Column List imkoniyatidan foydalanib ma'lum ustunlarni ommaga chiqarish va birlamchi kalit talablarini bajarish.
**Yechim (SQL):**
```sql
-- Publisher serverda:

-- 1. Nozik ma'lumotlarga ega jadval
CREATE TABLE employee_profiles (
    emp_id BIGSERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    ssn_pinfl VARCHAR(14) NOT NULL, -- Maxfiy ma'lumot (replikatsiya qilinmasligi kerak)
    salary_amount NUMERIC(12,2) NOT NULL, -- Maxfiy
    department_code VARCHAR(30) NOT NULL,
    hire_date DATE NOT NULL
);

-- 2. Faqat emp_id, full_name, department_code va hire_date ustunlarini replikatsiya qilish
-- DIQQAT: REPLICA IDENTITY (Primary Key) ustuni ro'yxatda bo'lishi shart!
CREATE PUBLICATION pub_employee_public
FOR TABLE employee_profiles (emp_id, full_name, department_code, hire_date);

-- 3. Ustunlar ro'yxatini tekshirish
SELECT 
    prpubid::regnamespace AS pub_schema,
    prrelid::regclass AS table_name,
    prattrs AS column_attributes_bitmap
FROM pg_publication_rel;

-- 4. Subscriber serverda faqat o'sha ochiq ustunlar bilan jadval yaratiladi:
-- CREATE TABLE employee_profiles (
--     emp_id BIGSERIAL PRIMARY KEY,
--     full_name VARCHAR(150) NOT NULL,
--     department_code VARCHAR(30) NOT NULL,
--     hire_date DATE NOT NULL
-- );
```
**Tushuntirish:** Column List funksiyasi ma'lumotlar xavfsizligini (Data Masking & Privacy) ma'lumotlar bazasi yadrosi darajasida hal qiladi. WAL logidan faqat ko'rsatilgan ustunlar dekodlanadi va tarmoq orqali uzatiladi. Bu maxfiy ustunlarning tashqi tizimlarga chiqib ketishining 100% oldini oladi.

---

### Topshiriq #1115: Partitsiyalangan Jadvallarni Mantiqiy Replikatsiya Qilish (publish_via_partition_root)
**Tavsif:** Publisher serverida `sales` jadvali oylar bo'yicha o'nlab partitsiyalarga bo'lingan, ammo Subscriber serverida u partitsiyasiz bitta umumiy jadval yoki boshqacha partitsiya sxemasiga ega bo'lishi lozim.
**Talablar:** publish_via_partition_root = true parametri orqali partitsiyalar o'zgarishini ildiz (Root) jadval nomidan uzatishni sozlash.
**Yechim (SQL):**
```sql
-- Publisher serverda:

-- 1. Ildiz (Root) partitsiyalangan jadval
CREATE TABLE sales_master (
    sale_id BIGINT NOT NULL,
    sale_date DATE NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    CONSTRAINT pk_sales PRIMARY KEY (sale_id, sale_date)
) PARTITION BY RANGE (sale_date);

-- Quyi partitsiyalar
CREATE TABLE sales_2026_q1 PARTITION OF sales_master
    FOR VALUES FROM ('2026-01-01') TO ('2026-04-01');

CREATE TABLE sales_2026_q2 PARTITION OF sales_master
    FOR VALUES FROM ('2026-04-01') TO ('2026-07-01');

-- 2. Publication yaratish va publish_via_partition_root parametrini yoqish
-- Bu qoida orqali har bir alohida partitsiya emas, sales_master sifatida uzatiladi
CREATE PUBLICATION pub_sales_partitioned
FOR TABLE sales_master
WITH (publish_via_partition_root = true);

-- 3. Parametr to'g'ri o'rnatilganini tekshirish
SELECT 
    pubname,
    pubvia_root
FROM pg_publication
WHERE pubname = 'pub_sales_partitioned';

-- 4. Yangi partitsiya qo'shilganda:
CREATE TABLE sales_2026_q3 PARTITION OF sales_master
    FOR VALUES FROM ('2026-07-01') TO ('2026-10-01');
-- publish_via_partition_root=true bo'lgani uchun, yangi partitsiya avtomatik replikatsiya oqimiga kiradi!
```
**Tushuntirish:** `publish_via_partition_root = true` bo'lmaganda, PostgreSQL har bir quyi jadvalni alohida nom bilan uzatadi, bu esa Subscriber tomonida aynan o'sha jadvallar bo'lishini talab qiladi. Root orqali uzatilganda, Subscriber tomoni partitsiyalar tuzilishidan bexabar holda barcha yozuvlarni qabul qilib oladi.

---

### Topshiriq #1116: Ikki Tomonlama (Bi-directional) Mantiqiy Replikatsiyada Cheksiz Sikllarni Oldini Olish
**Tavsif:** Ikki xil geografik lokatsiyadagi PostgreSQL tugunlari (Toshkent va Samarqand) bir-biriga o'zaro replikatsiya qilinganda, A dan B ga o'tgan ma'lumot yana B dan A ga qaytib abadiy halqa (Infinite Loop) hosil qilishi mumkin.
**Talablar:** PostgreSQL 16+ dagi origin = none parametrini CREATE SUBSCRIPTION da qo'llash orqali faqat mahalliy yaratilgan o'zgarishlarni replikatsiya qilish.
**Yechim (SQL):**
```sql
-- Tugun A (Toshkent): 192.168.1.10
-- Tugun B (Samarqand): 192.168.2.20

-- 1. Ikkala tugunda ham jadval yaratiladi
CREATE TABLE shared_inventory (
    item_sku VARCHAR(50) PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    stock_qty INT NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- 2. Ikkala tugunda ham o'z Publication'ini yaratish
CREATE PUBLICATION pub_local_inventory FOR TABLE shared_inventory;

-- 3. Tugun A dagi Obuna (Tugun B dan ma'lumot oladi):
-- origin = 'none': Tugun B dan faqat Tugun B ning o'zida yaratilgan o'zgarishlarni ol,
-- boshqa manbalardan (shu jumladan A ning o'zidan) borgan o'zgarishlarni takrorlama!
CREATE SUBSCRIPTION sub_from_samarkand
CONNECTION 'host=192.168.2.20 port=5432 dbname=corp user=repl_user password=Secret'
PUBLICATION pub_local_inventory
WITH (
    origin = 'none',
    copy_data = false,
    create_slot = true
);

-- 4. Tugun B dagi Obuna (Tugun A dan ma'lumot oladi):
-- CREATE SUBSCRIPTION sub_from_toshkent
-- CONNECTION 'host=192.168.1.10 port=5432 dbname=corp user=repl_user password=Secret'
-- PUBLICATION pub_local_inventory
-- WITH (
--     origin = 'none',
--     copy_data = false,
--     create_slot = true
-- );

-- 5. Replikatsiya kelib chiqishi (origin) holatini monitoring qilish
SELECT 
    subname,
    suborigin
FROM pg_subscription;
```
**Tushuntirish:** PostgreSQL 16 versiyasida qo'shilgan `origin = 'none'` parametri obunachiga faqat dastlabki tugunning o'zida yuz bergan o'zgarishlarni filtrlab olishni buyuradi. Bu replikatsiya 'ping-pong' yoki 'infinite loop' muammosini plaginlarsiz (masalan, pglogical yoki BDR siz) toza hal etadi.

---

### Topshiriq #1117: Mantiqiy Replikatsiyada Birlamchi Kalit Mojarolarini (Conflict Handling) Boshqarish
**Tavsif:** Subscriber bazasiga allaqachon mavjud bo'lgan ID ga ega yozuv replikatsiya oqimidan kelib tushsa, 'duplicate key value violates unique constraint' xatosi chiqadi va butun obuna to'xtab qoladi.
**Talablar:** disable_on_error parametri va pg_subscription_error_callback hamda PostgreSQL 15+ dagi ALTER SUBSCRIPTION ... SKIP (LSN) orqali tiqilib qolgan tranzaksiyani xavfsiz o'tkazib yuborish.
**Yechim (SQL):**
```sql
-- Subscriber serverda:

-- 1. Agar xatolik tufayli obuna qotib qolmasin desak, avval obuna xatosini aniqlaymiz:
SELECT 
    subname,
    last_error_relid::regclass AS conflicting_table,
    last_error_code,
    last_error_message,
    last_error_lsn
FROM pg_stat_subscription;

-- Misol uchun, last_error_lsn = '0/16D3A48' nuqtasida nizo yuz berdi va worker to'xtadi

-- 2. Nizoli tranzaksiyani o'tkazib yuborish (Skip conflicting LSN)
-- PostgreSQL 15+ imkoniyati:
ALTER SUBSCRIPTION sub_billing_analytics SKIP (lsn = '0/16D3A48');

-- 3. Obunani qayta faollashtirish
ALTER SUBSCRIPTION sub_billing_analytics ENABLE;

-- 4. Kelgusida nizo yuz berganda butun log faylni to'ldirib yubormaslik uchun
-- avtomatik to'xtash parametrini o'rnatish
ALTER SUBSCRIPTION sub_billing_analytics SET (disable_on_error = true);

-- 5. Obuna muammosiz davom etayotganini tekshirish
SELECT 
    subid,
    subname,
    pid,
    received_lsn,
    last_msg_send_time,
    last_msg_receipt_time
FROM pg_stat_subscription
WHERE subname = 'sub_billing_analytics';
```
**Tushuntirish:** `ALTER SUBSCRIPTION ... SKIP (lsn = ...)` xususiyati replikatsiya oqimidagi ma'lum bir ziddiyatli LSN tranzaksiyasini xotiradan tashlab o'tish imkonini beradi. Bu obuna butunlay muzlab qolmasligini ta'minlaydi. Biroq, tashlab o'tilgan qatorni loglardan tekshirib, qo'lda yarashtirish (reconciliation) zarur.

---

### Topshiriq #1118: Mantiqiy Obunani Xavfsiz To'xtatish, Qayta Yoqish va Slotni Boshqarish
**Tavsif:** Subscriber bazasida yirik indekslarni qayta qurish (REINDEX) yoki texnik ta'mirlash o'tkazilayotganda replikatsiya oqimini vaqtinchalik to'xtatib turish, so'ngra qolgan joyidan xavfsiz davom ettirish talab etiladi.
**Talablar:** ALTER SUBSCRIPTION ... DISABLE va ENABLE amallarini to'g'ri ketma-ketlikda bajarish, replikatsiya slotida WAL yig'ilib qolishini nazorat qilish.
**Yechim (SQL):**
```sql
-- Subscriber serverda:

-- 1. Obunani vaqtinchalik to'xtatish (Worker jarayoni yopiladi, lekin slot Publisherda saqlanadi)
ALTER SUBSCRIPTION sub_billing_analytics DISABLE;

-- 2. To'xtatilganligini tasdiqlash
SELECT 
    subname,
    subenabled,
    subslotname
FROM pg_subscription
WHERE subname = 'sub_billing_analytics';

-- DIQQAT: Obuna to'xtatilgan vaqtda Publisher tomonidagi slotda WAL to'plana boshlaydi.
-- Publisher serverda slot holatini tekshirib turish zarur:
-- SELECT slot_name, active, round(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)/(1024*1024), 2) AS lag_mb
-- FROM pg_replication_slots WHERE slot_name = 'sub_billing_analytics_slot';

-- 3. Texnik ishlar (masalan indekslarni qayta qurish) tugagach, obunani qayta yoqish
ALTER SUBSCRIPTION sub_billing_analytics ENABLE;

-- 4. Worker qayta ulangach, streaming jarayonini tekshirish
SELECT 
    subname,
    received_lsn,
    latest_end_lsn,
    last_msg_receipt_time
FROM pg_stat_subscription
WHERE subname = 'sub_billing_analytics';
```
**Tushuntirish:** Obunani `DISABLE` qilganda Publisherdagi replikatsiya sloti yo'qolmaydi, bu esa ma'lumotlar yo'qolmasligini kafolatlaydi. Ammo uzoq muddat `DISABLE` holatida qoldirish Publisher diskini WAL bilan to'ldirishi mumkin, shu sababli texnik amallar tezkor yakunlanishi lozim.

---

### Topshiriq #1119: DDL Sxema O'zgarishlarida Mantiqiy Replikatsiyani Yangilash (REFRESH PUBLICATION)
**Tavsif:** Publisher bazasidagi mavjud Publication'ga yangi jadval qo'shildi (`ALTER PUBLICATION ... ADD TABLE`), ammo Subscriber bazasida ushbu jadval avtomatik paydo bo'lmadi va replikatsiyalanmadi.
**Talablar:** Subscriber tomonida tegishli sxemani yaratish va ALTER SUBSCRIPTION ... REFRESH PUBLICATION buyrug'i orqali yangi jadvallarni sinxronlashtirish.
**Yechim (SQL):**
```sql
-- 1. Publisher serverda yangi jadval yaratish va mavjud publicationga qo'shish
CREATE TABLE billing_discounts (
    discount_id BIGSERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    percentage NUMERIC(5,2) NOT NULL,
    is_active BOOLEAN DEFAULT true
);

ALTER PUBLICATION pub_billing_core ADD TABLE billing_discounts;

-- 2. Subscriber serverda avval jadval sxemasini yaratib olish shart
-- (PostgreSQL logical replication DDL buyruqlarini avtomatik ko'chirmaydi)
CREATE TABLE billing_discounts (
    discount_id BIGSERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    percentage NUMERIC(5,2) NOT NULL,
    is_active BOOLEAN DEFAULT true
);

-- 3. Subscriber tomonida Publication metadata'sini yangilash
-- copy_data = true yangi qo'shilgan billing_discounts jadvalining mavjud qatorlarini ham nusxalab oladi
ALTER SUBSCRIPTION sub_billing_analytics REFRESH PUBLICATION WITH (copy_data = true);

-- 4. Yangi jadval replikatsiya holatiga qo'shilganini tekshirish
SELECT 
    srrelid::regclass AS table_name,
    srsubstate AS state_code,
    CASE srsubstate
        WHEN 'i' THEN 'Boshlang`ich holat (initialize)'
        WHEN 'd' THEN 'Ma`lumot nusxalanmoqda (copying)'
        WHEN 's' THEN 'Sinxronlangan (synchronized)'
        WHEN 'r' THEN 'Faol replikatsiya (ready)'
    END AS status_desc
FROM pg_subscription_rel
JOIN pg_subscription ON srsubid = pg_subscription.oid
WHERE subname = 'sub_billing_analytics';
```
**Tushuntirish:** PostgreSQL mantiqiy replikatsiyasi faqat DML amallarini uzatadi, DDL (`CREATE`, `ALTER`) amallari replikatsiya qilinmaydi. Shuning uchun Subscriberda jadval qo'lda ochilishi va `REFRESH PUBLICATION` chaqirilishi kerak. `copy_data = true` opsiyasi yangi qo'shilgan jadvaldagi mavjud ma'lumotlarni tortib olishni ta'minlaydi.

---

### Topshiriq #1120: PostgreSQL Katta Versiyalarini (Masalan PG14 -> PG16) Nol To'xtalish Bilan Migratsiya Qilish
**Tavsif:** Kompaniya PostgreSQL 14 klasteridan PostgreSQL 16 klasteriga xizmatni to'xtatmasdan (Zero-Downtime) o'tishi kerak. `pg_upgrade` xizmatni bir necha daqiqaga to'xtatishni talab qiladi, shuning uchun mantiqiy replikatsiya asosidagi ko'chirish rejasi lozim.
**Talablar:** Eski bazada barcha jadvallar uchun Publication yaratish, yangi bazada DDL sxemani tiklash, obuna ochish va oxirgi switchover paytini ketma-ketlikda boshqarish.
**Yechim (SQL):**
```sql
-- QADAM 1: Eski serverda (PG 14 - Source):
-- Barcha jadvallar uchun publication yaratish
CREATE PUBLICATION pub_full_migration FOR ALL TABLES;

-- QADAM 2: Yangi serverda (PG 16 - Target):
-- Avval eski serverdan faqat sxema (DDL) eksport qilinadi:
-- pg_dump -h 192.168.1.14 -s -d prod_db | psql -h 192.168.1.16 -d prod_db

-- QADAM 3: Yangi serverda obunani yoqish:
CREATE SUBSCRIPTION sub_full_migration
CONNECTION 'host=192.168.1.14 port=5432 dbname=prod_db user=migrator password=TopSecret'
PUBLICATION pub_full_migration
WITH (copy_data = true, create_slot = true);

-- QADAM 4: Yangi serverda barcha jadvallar 'ready' holatiga yetganini tekshirish
SELECT count(*) AS total_tables,
       count(*) FILTER (WHERE srsubstate = 'r') AS synced_tables
FROM pg_subscription_rel;

-- QADAM 5: SWITCHOVER (O'tish soniyalari):
-- 1. Ilova tomonida yozishni to'xtatish (Maintenance mode 1-2 soniya)
-- 2. Eski serverda ketma-ketliklarni (Sequences) eng oxirgi qiymatga sinxronlash:
-- SELECT sequence_name, last_value FROM information_schema.sequences ...
-- 3. Obunani o'chirish:
DROP SUBSCRIPTION sub_full_migration;
-- 4. Traffic DNS yoki PgBouncer orqali yangi PG16 serveriga yo'naltiriladi!
```
**Tushuntirish:** Mantiqiy replikatsiya yordamida versiya yangilash mutlaqo uzilishlarsiz (zero downtime) amalga oshadi, chunki PG14 va PG16 o'rtasidagi WAL strukturasi farq qilsa ham, mantiqiy protokol o'zaro moslashuvchan. Dastlabki sinxronlash fonda ishlaydi, switchover esa bir necha soniyada tugaydi.

---

### Topshiriq #1121: Mantiqiy Dekodlash (Logical Decoding) va test_decoding Plagini Bilan Ishlash
**Tavsif:** Tashqi ilovalar uchun PostgreSQL tranzaksiyalari oqimini to'g'ridan-to'g'ri WAL fayllaridan o'qib beruvchi plaginlar bilan ishlash va dekodlash mexanizmining ishlash prinsipini o'rganish lozim.
**Talablar:** pg_create_logical_replication_slot funksiyasi orqali test_decoding plaginida slot ochish va tranzaksiya xabarlarini tahlil qilish.
**Yechim (SQL):**
```sql
-- 1. test_decoding plagini yordamida mantiqiy slot yaratish
SELECT pg_create_logical_replication_slot('slot_test_decoding', 'test_decoding');

-- 2. Ma'lumotlar bazasida sinov jadvali va tranzaksiyasi
CREATE TABLE demo_accounts (
    acc_id INT PRIMARY KEY,
    owner_name TEXT,
    balance NUMERIC
);

BEGIN;
INSERT INTO demo_accounts VALUES (101, 'Alisher Navoiy', 500000.00);
UPDATE demo_accounts SET balance = 550000.00 WHERE acc_id = 101;
COMMIT;

-- 3. Slotedagi WAL o'zgarishlarini SQL orqali matn ko'rinishida o'qib olish
-- pg_logical_slot_peek_changes: slotdagi ko'rsatgichni siljitmasdan o'qiydi (faqat ko'rish)
SELECT lsn, xid, data 
FROM pg_logical_slot_peek_changes('slot_test_decoding', NULL, NULL);

-- 4. Slotedagi o'zgarishlarni o'qish va slot pozitsiyasini siljitish (Consume)
SELECT lsn, xid, data 
FROM pg_logical_slot_get_changes('slot_test_decoding', NULL, NULL);

-- 5. Slotni xavfsiz tozalash
SELECT pg_drop_replication_slot('slot_test_decoding');
```
**Tushuntirish:** Logical Decoding WAL dagi past darajali binar amallarni (Write-Ahead Log) tushunarli mantiqiy amallarga (INSERT, UPDATE, DELETE) o'giradi. `test_decoding` PostgreSQL bilan birga keladigan standart namoyish plaginidir. U har bir tranzaksiyaning `BEGIN`, `table ...: INSERT:` va `COMMIT` bosqichlarini matn shaklida ko'rsatadi.

---

### Topshiriq #1122: pg_logical_slot_peek_changes va get_changes Yordamida SQL Orqali Hodisalarni Ajratish
**Tavsif:** Maxsus ETL dasturi tashqi xabar navbatiga (RabbitMQ/Kafka) uzatishdan oldin, tranzaksiyalar oqimidan faqat ma'lum bir schema va jadval o'zgarishlarini o'qib, xatolik yuz berganda qayta o'qish imkoniyatiga ega bo'lishi kerak.
**Talablar:** peek_changes yordamida xabarlarni ko'rish, muvaffaqiyatli jo'natilgach get_changes orqali tasdiqlash (Acknowledge) parametrlarini sozlash.
**Yechim (SQL):**
```sql
-- 1. Mantiqiy slot yaratish
SELECT * FROM pg_create_logical_replication_slot('etl_cdc_slot', 'test_decoding');

-- 2. Sinov amallari
INSERT INTO demo_accounts VALUES (202, 'Mirzo Ulugbek', 1200000.00);

-- 3. Xabarlarni o'qish (Peek rejimi - LSN surilmaydi, xavfsiz ko'rib chiqish)
-- Parametrlar: slot_name, upto_lsn, upto_nchanges, 'include-xids', '0'
SELECT 
    lsn, 
    xid, 
    data 
FROM pg_logical_slot_peek_changes(
    'etl_cdc_slot', 
    NULL, 
    100, 
    'include-xids', 'true', 
    'skip-empty-xacts', 'true'
);

-- 4. Tashqi xizmat (ETL) o'zgarishlarni qabul qilganini tasdiqlaganidan keyin
-- get_changes orqali xuddi shu o'zgarishlar iste'mol qilinadi va slot LSN oldinga suriladi
SELECT 
    lsn, 
    xid, 
    data 
FROM pg_logical_slot_get_changes(
    'etl_cdc_slot', 
    NULL, 
    100, 
    'include-xids', 'true'
);

-- 5. Slot oxirgi iste'mol qilingan LSN nuqtasini tekshirish
SELECT 
    slot_name, 
    confirmed_flush_lsn 
FROM pg_replication_slots 
WHERE slot_name = 'etl_cdc_slot';

-- Slotni tozalash
SELECT pg_drop_replication_slot('etl_cdc_slot');
```
**Tushuntirish:** `peek_changes` va `get_changes` orasidagi asosiy farq LSN ning oldinga siljishidadir. Agar tashqi ETL tizimi o'qish paytida to'xtab qolsa yoki tarmoq uzilsa, `peek` qilingan ma'lumotlar yo'qolmaydi. Faqat `get_changes` chaqirilgandagina PostgreSQL `confirmed_flush_lsn` ni yangilaydi va WAL tozalanadi.

---

### Topshiriq #1123: wal2json Plagini Bilan WAL O'zgarishlarini Strukturaviy JSON Formatida O'qish
**Tavsif:** Zamonaviy veb-xizmatlar va hodisalarga asoslangan (Event-Driven) arxitekturalar ma'lumotlar bazasi o'zgarishlarini qulay JSON formatida qabul qilishni talab qiladi.
**Talablar:** wal2json chiqish formatini sozlash (include-types, include-lsn, pretty-print) va JSONB sifatida indekslash hamda parse qilish.
**Yechim (SQL):**
```sql
-- 1. wal2json plaginida mantiqiy slot yaratish (serverda wal2json kutubxonasi o'rnatilgan bo'lishi lozim)
-- SELECT pg_create_logical_replication_slot('json_cdc_slot', 'wal2json');

-- 2. Sinov jadvali
CREATE TABLE store_products (
    product_id INT PRIMARY KEY,
    name VARCHAR(100),
    price NUMERIC(10,2),
    tags TEXT[]
);

-- 3. wal2json parametrlarini sozlagan holda o'zgarishlarni JSON formatida olish
-- Namuna: format-version=2, add-tables='public.store_products', include-lsn=true
/*
SELECT data::jsonb
FROM pg_logical_slot_peek_changes(
    'json_cdc_slot', 
    NULL, 
    NULL,
    'format-version', '2',
    'include-lsn', 'true',
    'add-tables', 'public.store_products'
);
*/

-- 4. Qabul qilingan JSON strukturani simulyatsiya qilish va SQL orqali tahlil qilish
WITH simulated_wal2json AS (
    SELECT '{"action":"I","schema":"public","table":"store_products","columns":[{"name":"product_id","type":"integer","value":55},{"name":"name","type":"character varying(100)","value":"Smartfon Ultra"},{"name":"price","type":"numeric","value":3500000.00}]}'::jsonb AS change_doc
)
SELECT 
    change_doc->>'action' AS action_type,
    change_doc->>'table' AS table_name,
    col->>'name' AS column_name,
    col->>'value' AS column_value
FROM simulated_wal2json,
LATERAL jsonb_array_elements(change_doc->'columns') AS col;
```
**Tushuntirish:** `wal2json` tranzaksiyalarni bitta JSON obyektiga jamlab beradi. `format-version=2` da har bir o'zgarish alohida JSON qatori sifatida uzatiladi, bu esa xotirani tejaydi va katta hajmdagi tranzaksiyalarni streaming qilish imkonini beradi.

---

### Topshiriq #1124: Nofaol Mantiqiy Replikatsiya Slotlarini Aniqlash va Disk To'lishining Oldini Olish
**Tavsif:** Ulanishi uzilib qolgan yoki unutilgan mantiqiy replikatsiya sloti PostgreSQL serveridagi WAL fayllarni doimiy ushlab turadi, natijada bir necha kunda butun disk 100% to'lib, server avariya holatida o'chadi.
**Talablar:** pg_replication_slots, pg_stat_activity va disk hajmini solishtirish orqali nofaol slotlarni avtomatik aniqlash va xavfsiz tozalash SQL protsedurasini yaratish.
**Yechim (SQL):**
```sql
-- 1. Nofaol va xavfli darajada WAL to'plagan mantiqiy slotlarni aniqlash so'rovi
SELECT 
    slot_name,
    plugin,
    active,
    active_pid,
    wal_status, -- 'normal', 'reserved', 'lost'
    round(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) / (1024.0 * 1024.0 * 1024.0), 3) AS retained_wal_gb,
    round(pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn) / (1024.0 * 1024.0 * 1024.0), 3) AS unconfirmed_lag_gb
FROM pg_replication_slots
WHERE slot_type = 'logical'
ORDER BY retained_wal_gb DESC;

-- 2. Xavfli slotlarni avtomatik tozalash uchun ma'muriy protsedura
CREATE OR REPLACE PROCEDURE pr_cleanup_stale_logical_slots(IN max_allowed_lag_gb NUMERIC)
LANGUAGE plpgsql
AS $$
DECLARE
    r RECORD;
    v_lag_gb NUMERIC;
BEGIN
    FOR r IN 
        SELECT slot_name, restart_lsn, active 
        FROM pg_replication_slots 
        WHERE slot_type = 'logical' 
    LOOP
        -- Agar slot nofaol bo'lsa
        IF NOT r.active THEN
            v_lag_gb := round(pg_wal_lsn_diff(pg_current_wal_lsn(), r.restart_lsn) / (1024.0 * 1024.0 * 1024.0), 3);
            
            IF v_lag_gb > max_allowed_lag_gb THEN
                RAISE WARNING 'O`chirilmoqda: Slot % faol emas va % GB WAL to`plagan!', r.slot_name, v_lag_gb;
                PERFORM pg_drop_replication_slot(r.slot_name);
            END IF;
        END IF;
    END LOOP;
END;
$$;

-- 3. 20 GB dan ortiq kechikkan nofaol slotlarni tozalashni chaqirish
CALL pr_cleanup_stale_logical_slots(20.0);
```
**Tushuntirish:** Mantiqiy slotlar Primary serverga WAL yozuvlarini qat'iy saqlab turish majburiyatini yuklaydi. `max_slot_wal_keep_size` parametri slot ushlab turishi mumkin bo'lgan maksimal WAL hajmini cheklab beradi; cheklovdan oshganda slot 'lost' holatiga o'tadi va Primary diskining to'lib ketishini oldini oladi.

---

### Topshiriq #1125: Mantiqiy Replikatsiya Slotida LSN Pozitsiyasini Qo'lda Oldinga Siljitish
**Tavsif:** Tashqi tizim (masalan Debezium yoki custom CDC iste'molchisi) xatoga uchrab qayta tiklanganda, eski o'zgarishlarni qayta o'qish shart bo'lmasa, slot pozitsiyasini joriy LSN ga majburiy oldinga siljitish lozim.
**Talablar:** pg_replication_origin_advance funksiyasi va pg_replication_slots metadata yangilanishi orqali LSN sakrashini amalga oshirish.
**Yechim (SQL):**
```sql
-- 1. Mavjud replikatsiya kelib chiqishi (Origin) larni ko'rish
SELECT roident, roname FROM pg_replication_origin;

-- 2. Yangi origin yaratish (agar mavjud bo'lmasa)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_replication_origin WHERE roname = 'debezium_cdc_origin') THEN
        PERFORM pg_replication_origin_create('debezium_cdc_origin');
    END IF;
END $$;

-- 3. Origin holati va uning oxirgi tasdiqlangan LSN nuqtasi
SELECT 
    roname,
    remote_lsn,
    local_lsn
FROM pg_replication_origin_status;

-- 4. LSN pozitsiyasini joriy WAL nuqtasiga oldinga siljitish (Fast-Forward)
-- Bu orqali eski barcha o'zgarishlar e'tiborsiz qoldiriladi va slot eng so'nggi holatga o'tadi
SELECT pg_replication_origin_advance('debezium_cdc_origin', pg_current_wal_lsn());

-- 5. Keraksiz bo'lganda origin identifikatorini o'chirish
-- SELECT pg_replication_origin_drop('debezium_cdc_origin');
```
**Tushuntirish:** `pg_replication_origin_advance()` mantiqiy replikatsiyada oqim ko'rsatgichini to'g'ridan-to'g'ri yangi LSN ga ko'chiradi. Bu falokatdan so'ng millionlab eski tranzaksiyalarni o'qib vaqt sarflamasdan, tizimni darhol joriy onlayn rejimga ulash uchun kerak bo'ladi.

---

### Topshiriq #1126: CDC uchun Jadval REPLICA IDENTITY (DEFAULT, FULL, NOTHING, INDEX) Strategiyasini Sozlash
**Tavsif:** Debezium orqali `UPDATE` va `DELETE` amallarini kuzatishda, o'zgarishdan oldingi qator holatini (`before` bloki) olish zarur bo'ladi. PostgreSQL odatda faqat Primary Keyni yuboradi.
**Talablar:** ALTER TABLE ... REPLICA IDENTITY FULL va REPLICA IDENTITY USING INDEX imkoniyatlarini tahlil qilish, WAL hajmiga ta'sirini baholash.
**Yechim (SQL):**
```sql
-- 1. Sinov jadvali
CREATE TABLE users_credentials (
    user_id BIGINT NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    password_hash TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    updated_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- DEFAULT holati: Faqat PRIMARY KEY ustunlari 'before' sifatida yuboriladi
ALTER TABLE users_credentials ADD CONSTRAINT pk_users PRIMARY KEY (user_id);
ALTER TABLE users_credentials REPLICA IDENTITY DEFAULT;

-- 2. REPLICA IDENTITY FULL: UPDATE va DELETE paytida qatorning BARCHA eski qiymatlari WAL'ga yoziladi
-- Debezium bu rejimda to'liq 'before' obyektini hosil qila oladi
ALTER TABLE users_credentials REPLICA IDENTITY FULL;

-- 3. Maxsus Unikal Indeks orqali REPLICA IDENTITY o'rnatish
-- FULL rejimiga nisbatan kamroq WAL yozadi, faqat ko'rsatilgan unikal indeks ustunlarini oladi
CREATE UNIQUE INDEX idx_users_email_uniq ON users_credentials(email);
ALTER TABLE users_credentials REPLICA IDENTITY USING INDEX idx_users_email_uniq;

-- 4. Jadvallarning joriy Replica Identity holatini monitoring qilish
-- d = default, f = full, n = nothing, i = index
SELECT 
    c.relname AS table_name,
    c.relreplident AS replica_identity_type,
    CASE c.relreplident
        WHEN 'd' THEN 'DEFAULT (Birlamchi kalit)'
        WHEN 'n' THEN 'NOTHING (Hech narsa)'
        WHEN 'f' THEN 'FULL (Barcha ustunlar - To`liq oldingi holat)'
        WHEN 'i' THEN 'USING INDEX (Unikal indeks)'
    END AS replica_identity_desc
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND c.relkind = 'r' AND c.relname = 'users_credentials';
```
**Tushuntirish:** `REPLICA IDENTITY FULL` har bir yangilanishda (`UPDATE`) butun qatorning eski nusxasini WAL ga kiritadi. Bu Debeziumga to'liq solishtirma (diff) berish imkonini taqdim etsa-da, katta jadvallarda WAL hajmini va disk I/O yuklamasini sezilarli oshiradi. Shuning uchun faqat zarur jadvallarga qo'llash tavsiya etiladi.

---

### Topshiriq #1127: Debezium PostgreSQL Connector Uchun Publication va Mantiqiy Slotni Tayyorlash
**Tavsif:** Apache Kafka ekotizimiga ulangan Debezium konnektori PostgreSQL dan ma'lumotlarni oqimli (CDC) o'qishi uchun maxsus ruxsatlar, publication va pgoutput plaginiga mos slot talab etiladi.
**Talablar:** Debezium uchun xavfsiz foydalanuvchi yaratish, pgoutput plaginiga mos slot ochish va publication biriktirish.
**Yechim (SQL):**
```sql
-- 1. Debezium uchun xavfsiz CDC foydalanuvchisini yaratish
CREATE ROLE debezium_user WITH REPLICATION LOGIN PASSWORD 'DebeziumKafkaSecret2026!';

-- Jadvallarni o'qish ruxsatlarini berish
GRANT USAGE ON SCHEMA public TO debezium_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO debezium_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO debezium_user;

-- 2. Debezium konnektori uchun alohida publication yaratish
-- Faqat kerakli biznes jadvallarini qo'shamiz
CREATE PUBLICATION debezium_publication FOR TABLE 
    billing_customers, 
    billing_invoices, 
    users_credentials;

-- 3. Debezium avtomatik slot yaratishi mumkin, lekin uni oldindan xavfsiz ochish:
-- pgoutput - PostgreSQL 10+ dagi o'rnatilgan yuqori tezlikdagi ikkilik protokol plagini
SELECT pg_create_logical_replication_slot('debezium_slot', 'pgoutput');

-- 4. Konnektor holatini tekshirish uchun ko'rinish
CREATE OR REPLACE VIEW v_debezium_connector_status AS
SELECT 
    slot_name,
    plugin,
    active,
    active_pid,
    confirmed_flush_lsn,
    pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn) AS pending_wal_bytes
FROM pg_replication_slots
WHERE slot_name = 'debezium_slot';

SELECT * FROM v_debezium_connector_status;
```
**Tushuntirish:** Debezium standart `pgoutput` plaginidan foydalanadi, bu esa serverga uchinchi tomon C-plaginlarini (masalan `decoderbufs` yoki `wal2json`) o'rnatmasdan ishlash imkonini beradi. `pgoutput` ikkilik formatda ishlagani uchun CPU va tarmoq yuklamasi minimal bo'ladi.

---

### Topshiriq #1128: Tranzaksion Outbox Pattern: CDC Orqali Kafolatlangan Hodisalarni Yetkazish
**Tavsif:** Asosiy biznes operatsiyasi (masalan, buyurtma yaratish) va tashqi xabar tizimiga (Kafka) hodisa yuborish 'Dual Write' muammosini keltirib chiqaradi. Buni bartaraf qilish uchun Transactional Outbox jadvali va CDC oqimi talab etiladi.
**Talablar:** outbox jadvalini loyihalash, biznes tranzaksiyasi ichida atomar yozish va Debezium orqali buni Kafka mavzusiga yo'naltirish.
**Yechim (SQL):**
```sql
-- 1. Outbox jadvalini loyihalash
CREATE TABLE transactional_outbox (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(100) NOT NULL, -- masalan 'ORDER', 'PAYMENT'
    aggregate_id VARCHAR(100) NOT NULL,   -- 'ORD-98765'
    event_type VARCHAR(100) NOT NULL,     -- 'ORDER_CREATED'
    payload JSONB NOT NULL,               -- Hodisa ma'lumotlari
    tracing_headers JSONB,                -- OpenTelemetry / Zipkin konteksti
    created_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- Jadvalni CDC publication'ga qo'shish
ALTER PUBLICATION debezium_publication ADD TABLE transactional_outbox;

-- 2. Atomar Biznes Tranzaksiyasi: Buyurtma saqlanadi va Outbox'ga yoziladi
BEGIN;

-- Asosiy biznes harakati
INSERT INTO billing_invoices (customer_id, amount, status) 
VALUES (1, 1500000.00, 'PAID')
RETURNING invoice_id;

-- Bir vaqtda Outbox jadvaliga hodisa qayd etiladi (bitta DB tranzaksiyasida!)
INSERT INTO transactional_outbox (aggregate_type, aggregate_id, event_type, payload)
VALUES (
    'INVOICE',
    'INV-1001',
    'INVOICE_PAID',
    jsonb_build_object(
        'invoice_id', 1001,
        'customer_id', 1,
        'amount', 1500000.00,
        'currency', 'UZS',
        'paid_at', now()
    )
);

COMMIT; -- Agar kommit bo'lsa, ikkala ma'lumot ham WAL ga tushadi va Debezium uni Kafkaga kafolatli uzatadi!
```
**Tushuntirish:** Transactional Outbox patterni mikroxizmatlar orasidagi eng mashhur ishonchli xabar almashish usulidir. Ilova bevosita Kafka kutubxonasiga bog'lanmaydi; biznes jadval va `transactional_outbox` bitta ACID tranzaksiyada yoziladi. CDC esa outbox jadvalidan o'zgarishni o'qib, Kafkaga uzatadi. Bu orqali 'kamida bir marta yetkazish' (at-least-once delivery) kafolatlanadi.

---

### Topshiriq #1129: WAL To'lib Ketishining Oldini Olish Uchun Heartbeat Jadvali va Mexanizmi
**Tavsif:** Agar kuzatilayotgan jadvallarda kamdan-kam o'zgarish sodir bo'lsa, Debezium PostgreSQL ga tasdiqlangan LSN ni yubora olmaydi. Natijada boshqa jadvallardagi o'zgarishlar tufayli WAL to'planib, disk to'lib ketadi.
**Talablar:** debezium_heartbeat jadvalini yaratish, davriy yangilab turish va Debezium konfiguratsiyasiga moslash.
**Yechim (SQL):**
```sql
-- 1. Heartbeat jadvalini yaratish
CREATE TABLE debezium_heartbeat (
    id VARCHAR(50) PRIMARY KEY,
    last_heartbeat_ts TIMESTAMPTZ NOT NULL
);

-- Boshlang'ich yozuv
INSERT INTO debezium_heartbeat (id, last_heartbeat_ts) VALUES ('debezium_hb', now());

-- Heartbeat jadvalini Debezium publication'ga qo'shish
ALTER PUBLICATION debezium_publication ADD TABLE debezium_heartbeat;

-- 2. Heartbeat'ni davriy yangilovchi funksiya (pg_cron yoki tashqi scheduler orqali chaqiriladi)
CREATE OR REPLACE FUNCTION fn_trigger_debezium_heartbeat()
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE debezium_heartbeat
    SET last_heartbeat_ts = clock_timestamp()
    WHERE id = 'debezium_hb';
END;
$$;

-- 3. Debezium konnektor parametrlarida quyidagilar yoqiladi:
-- heartbeat.interval.ms = 5000
-- heartbeat.action.query = UPDATE debezium_heartbeat SET last_heartbeat_ts = clock_timestamp() WHERE id = 'debezium_hb';

-- 4. Heartbeat ishlayotganini va LSN oldinga siljiyotganini tekshirish
SELECT 
    slot_name,
    confirmed_flush_lsn,
    pg_current_wal_lsn(),
    pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn) AS lag_bytes
FROM pg_replication_slots 
WHERE slot_name = 'debezium_slot';
```
**Tushuntirish:** Heartbeat mexanizmi passiv jadvallarni kuzatayotgan CDC tizimlarida disk xavfsizligini ta'minlovchi eng muhim instrumentdir. Har 5 soniyada `debezium_heartbeat` jadvaliga yangi timestamp yozilishi orqali Debezium WAL LSN pozitsiyasini doimiy oldinga siljitadi va PostgreSQL eski WAL bloklarini xavfsiz o'chirib tashlaydi.

---

### Topshiriq #1130: Debezium CDC Payload Strukturasini Tahlil Qilish va SQL JSONB Bilan Qayta Ishlash
**Tavsif:** Kafkadan kelgan yoki CDC orqali tutilgan murakkab Debezium voqea paketlari (schema, payload: before, after, source, op, ts_ms) bazaga kelganda, ularni SQL orqali ochib tegishli analitika jadvaliga yo'naltirish zarur.
**Talablar:** op amallarini ('c' - create, 'u' - update, 'd' - delete, 'r' - read) tahlil qiluvchi va ma'lumotlar farqini ajratuvchi saqlanadigan protsedura yozish.
**Yechim (SQL):**
```sql
-- 1. Xom CDC voqealarini qabul qiluvchi bufer jadvali
CREATE TABLE raw_cdc_events (
    event_id BIGSERIAL PRIMARY KEY,
    topic_name VARCHAR(150),
    kafka_offset BIGINT,
    payload JSONB NOT NULL,
    received_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- 2. CDC payload strukturasini parse qiluvchi ko'rinish
CREATE OR REPLACE VIEW v_parsed_cdc_events AS
SELECT 
    event_id,
    payload->'source'->>'db' AS db_name,
    payload->'source'->>'table' AS table_name,
    payload->'source'->>'lsn' AS wal_lsn,
    to_timestamp((payload->'source'->>'ts_ms')::bigint / 1000.0) AS source_commit_time,
    payload->>'op' AS operation_type, -- c=insert, u=update, d=delete, r=snapshot
    payload->'before' AS row_before,
    payload->'after' AS row_after
FROM raw_cdc_events;

-- 3. UPDATE paytida qaysi ustunlar o'zgarganini (Diff) aniqlash funksiyasi
CREATE OR REPLACE FUNCTION fn_extract_cdc_diff(before_json JSONB, after_json JSONB)
RETURNS JSONB
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT jsonb_object_agg(a.key, jsonb_build_object('old', b.value, 'new', a.value))
    FROM jsonb_each(after_json) a
    JOIN jsonb_each(before_json) b ON a.key = b.key
    WHERE a.value IS DISTINCT FROM b.value;
$$;

-- 4. Sinov uchun Debezium CDC namunaviy voqeasini kiritish va diff olish
INSERT INTO raw_cdc_events (topic_name, payload)
VALUES ('pg.public.billing_invoices', '{
    "op": "u",
    "source": {"db": "prod", "table": "billing_invoices", "lsn": 12345678, "ts_ms": 1773050400000},
    "before": {"invoice_id": 1001, "amount": 100.00, "status": "DRAFT"},
    "after":  {"invoice_id": 1001, "amount": 100.00, "status": "PAID"}
}');

SELECT 
    event_id, 
    operation_type, 
    fn_extract_cdc_diff(row_before, row_after) AS changed_fields
FROM v_parsed_cdc_events;
```
**Tushuntirish:** Debezium har bir operatsiyani `op` kodi bilan belgilaydi. `before` va `after` bloklarini JSONB solishtirish orqali aynan qaysi ustunlar o'zgarganini aniqlash mumkin. Bu esa to'liq audit jurnallarini va o'zgarishlar tarixini minimal xotira sarflab yaratish imkonini beradi.

---

### Topshiriq #1131: CDC Signallari Orqali Bosqichma-bosqich (Incremental Snapshot) Olish Jadvalini Tashkil Qilish
**Tavsif:** Ishlab turgan milliardlik jadvalni birdaniga to'liq snapshot qilish ma'lumotlar bazasini qotirib qo'yishi mumkin. Debezium Signallash mexanizmi orqali jadvalni bloklab qo'ymasdan qismlarga bo'lib (Incremental Snapshot) surish talab etiladi.
**Talablar:** debezium_signal jadvalini loyihalash va maxsus 'execute-snapshot' buyruqlarini JSON shaklida uzatish.
**Yechim (SQL):**
```sql
-- 1. Debezium signallar jadvalini yaratish
CREATE TABLE debezium_signal (
    id VARCHAR(64) PRIMARY KEY,
    type VARCHAR(32) NOT NULL,
    data VARCHAR(2048) NULL
);

-- Jadvalni CDC publication'ga qo'shish
ALTER PUBLICATION debezium_publication ADD TABLE debezium_signal;

-- 2. Bosqichma-bosqich (Incremental Snapshot) buyrug'ini yuborish
-- Debezium konnektor sozlamalarida signal.data.collection = 'public.debezium_signal' ko'rsatiladi
INSERT INTO debezium_signal (id, type, data)
VALUES (
    'snapshot-signal-001',
    'execute-snapshot',
    '{
        "data-collections": ["public.billing_invoices"],
        "type": "incremental",
        "additional-condition": "issued_at >= ''2026-01-01''"
    }'
);

-- 3. Snapshot jarayonini to'xtatish yoki bekor qilish signali
-- INSERT INTO debezium_signal (id, type, data)
-- VALUES ('stop-signal-002', 'stop-snapshot', '{"data-collections": ["public.billing_invoices"]}');

-- 4. Yuborilgan signallar tarixini ko'rish
SELECT * FROM debezium_signal ORDER BY id DESC;
```
**Tushuntirish:** Incremental Snapshot Debeziumning eng kuchli xususiyatlaridan biridir. Oddiy snapshot butun jadvalni bir marta qulflab (shared lock) o'qisa, bosqichma-bosqich snapshot jadvalni Primary Key bo'yicha 'chunk'larga (masalan 1024 tadan qatorga) bo'lib, oqim (streaming) orasida navbatma-navbat yuklaydi. Bu ishlab chiqarish bazasiga nol ta'sir ko'rsatadi.

---

### Topshiriq #1132: MySQL CDC Uchun Binlog Parametrlari va GTID Sozlamalarini O'rnatish
**Tavsif:** Heterogen infratuzilmada MySQL ma'lumotlar bazasidan Debezium orqali ma'lumotlarni tutib olish uchun binar loglar (Binary Log) va global tranzaksiya identifikatorlari (GTID) sozlanishi lozim.
**Talablar:** binlog_format=ROW, binlog_row_image=FULL, gtid_mode=ON sozlamalarini SQL orqali tekshirish va CDC foydalanuvchisi huquqlarini berish.
**Yechim (SQL):**
```sql
-- MySQL serverda (yoki MySQL muvofiq SQL konsolida):

-- 1. Binlog va GTID tizim o'zgaruvchilarini tekshirish
SHOW VARIABLES LIKE 'binlog_format';      -- 'ROW' bo'lishi shart
SHOW VARIABLES LIKE 'binlog_row_image';  -- 'FULL' bo'lishi lozim
SHOW VARIABLES LIKE 'gtid_mode';         -- 'ON' bo'lishi shart
SHOW VARIABLES LIKE 'enforce_gtid_consistency'; -- 'ON'

-- 2. CDC Debezium foydalanuvchisini yaratish va replikatsiya huquqlarini berish
-- CREATE USER 'debezium_mysql'@'%' IDENTIFIED BY 'KhorazmiyMysqlCDC2026!';
-- GRANT SELECT, RELOAD, SHOW DATABASES, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'debezium_mysql'@'%';
-- FLUSH PRIVILEGES;

-- 3. Joriy Binlog pozitsiyasi va GTID holatini monitoring qilish
SHOW MASTER STATUS;

-- 4. Binlog hajmini va saqlanish muddatini tekshirish
SHOW VARIABLES LIKE 'binlog_expire_logs_seconds';

-- 5. Binlogdagi hodisalar ro'yxatini SQL orqali ko'rib chiqish
SHOW BINLOG EVENTS IN 'binlog.000001' LIMIT 10;
```
**Tushuntirish:** MySQL da CDC to'g'ri ishlashi uchun `binlog_format = ROW` va `binlog_row_image = FULL` bo'lishi qat'iy talabdir. Aks holda `STATEMENT` rejimida faqat SQL matni yoziladi va o'zgargan aniq qator ma'lumotlarini ajratib bo'lmaydi. GTID (Global Transaction Identifier) esa serverlar almashganda Debeziumning aniq qolgan joyidan davom etishini kafolatlaydi.

---

### Topshiriq #1133: CDC Oqimidan SCD Type 2 (Sekin O'zgaruvchi O'lchamlar) Tarixiy Jadvalini Shakllantirish
**Tavsif:** Mijozning manzili yoki tarif rejasi o'zgarganda, eski qiymatni o'chirib tashlamasdan, har bir o'zgarishning amal qilish muddatini (`valid_from` va `valid_to`) ko'rsatuvchi Slowly Changing Dimension (SCD Type 2) audit jadvali yuritilishi kerak.
**Talablar:** CDC INSERT va UPDATE hodisalari asosida avvalgi yozuvning valid_to ustunini yopuvchi va yangi versiyani ochuvchi idempotent SQL mantiqini yozish.
**Yechim (SQL):**
```sql
-- 1. Asosiy mijozlar SCD Type 2 jadvali
CREATE TABLE dim_customers_scd2 (
    scd_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    full_name TEXT NOT NULL,
    tier_plan TEXT NOT NULL,
    valid_from TIMESTAMPTZ NOT NULL,
    valid_to TIMESTAMPTZ DEFAULT '9999-12-31 23:59:59+00'::timestamptz,
    is_current BOOLEAN DEFAULT true
);

CREATE INDEX idx_dim_cust_current ON dim_customers_scd2(customer_id) WHERE is_current = true;

-- 2. CDC o'zgarishini SCD Type 2 ga o'tkazuvchi protsedura
CREATE OR REPLACE PROCEDURE pr_apply_cdc_to_scd2(
    p_customer_id BIGINT,
    p_full_name TEXT,
    p_tier_plan TEXT,
    p_change_timestamp TIMESTAMPTZ
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- 1-QADAM: Hozirgi faol yozuv mavjud bo'lsa, uni yopish
    UPDATE dim_customers_scd2
    SET valid_to = p_change_timestamp,
        is_current = false
    WHERE customer_id = p_customer_id 
      AND is_current = true;

    -- 2-QADAM: Yangi versiyani kiritish
    INSERT INTO dim_customers_scd2 (
        customer_id, 
        full_name, 
        tier_plan, 
        valid_from, 
        valid_to, 
        is_current
    )
    VALUES (
        p_customer_id, 
        p_full_name, 
        p_tier_plan, 
        p_change_timestamp, 
        '9999-12-31 23:59:59+00'::timestamptz, 
        true
    );
END;
$$;

-- 3. Sinov: Dastlabki ro'yxatdan o'tish va 1 kundan keyin tarifning o'zgarishi
CALL pr_apply_cdc_to_scd2(5001, 'Jaloliddin Manguberdi', 'STANDARD', '2026-03-01 10:00:00+00');
CALL pr_apply_cdc_to_scd2(5001, 'Jaloliddin Manguberdi', 'PREMIUM',  '2026-03-02 15:30:00+00');

-- 4. Natijani tekshirish
SELECT customer_id, tier_plan, valid_from, valid_to, is_current 
FROM dim_customers_scd2 
WHERE customer_id = 5001 
ORDER BY valid_from;
```
**Tushuntirish:** SCD Type 2 ma'lumotlar omborida (DWH) tarixiy holatni aniq qayta tiklash imkonini beradi. CDC oqimidagi `source.ts_ms` yoki LSN commit vaqti `valid_from` va `valid_to` uchun ideal manba bo'lib xizmat qiladi, natijada har qanday o'tgan sanadagi holatni `WHERE valid_from <= $date AND valid_to > $date` orqali topish mumkin.

---

### Topshiriq #1134: Idempotent CDC Ingest: Tranzaksiya LSN va Ketma-ketlikni Boshqarish
**Tavsif:** Tarmoqdagi nosozlik sababli Kafka yoki Debezium bir xil o'zgarish xabarini takroran (duplicate delivery) yuborishi yoki xabarlar tartibi buzilishi mumkin. Ma'lumotlar buzilmasligi uchun oxirgi LSN asosida idempotent INSERT/UPDATE qilish zarur.
**Talablar:** Har bir satr uchun last_modified_lsn ustunini saqlash va faqat kattaroq LSN kelgandagina ma'lumotni yangilash mantig'ini SQL da tuzish.
**Yechim (SQL):**
```sql
-- 1. Maqsadli replika jadvali
CREATE TABLE replica_products (
    product_id BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(12,2) NOT NULL,
    last_applied_lsn PG_LSN NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- 2. Idempotent CDC Upsert funksiyasi
CREATE OR REPLACE FUNCTION fn_upsert_cdc_product(
    p_id BIGINT,
    p_name VARCHAR(100),
    p_price NUMERIC(12,2),
    p_lsn PG_LSN
)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO replica_products (product_id, name, price, last_applied_lsn)
    VALUES (p_id, p_name, p_price, p_lsn)
    ON CONFLICT (product_id) DO UPDATE
    SET 
        name = EXCLUDED.name,
        price = EXCLUDED.price,
        last_applied_lsn = EXCLUDED.last_applied_lsn,
        updated_at = clock_timestamp()
    -- MUHIM SHART: Faqat yangi kelgan LSN oldingisidan qat'iy katta bo'lsagina yangilansin!
    WHERE replica_products.last_applied_lsn < EXCLUDED.last_applied_lsn;
END;
$$;

-- 3. Sinov: Yangi yozuv (LSN = '0/1600000')
SELECT fn_upsert_cdc_product(1, 'Gaming Monitor', 400.00, '0/1600000'::pg_lsn);

-- Takroriy eski xabar kelganda (LSN = '0/1500000') - O'zgarish inkor qilinadi!
SELECT fn_upsert_cdc_product(1, 'Gaming Monitor (Eski)', 350.00, '0/1500000'::pg_lsn);

-- Yangiroq xabar kelganda (LSN = '0/1700000') - Muvaffaqiyatli yangilanadi
SELECT fn_upsert_cdc_product(1, 'Gaming Monitor Pro', 450.00, '0/1700000'::pg_lsn);

-- 4. Yakuniy holat
SELECT * FROM replica_products WHERE product_id = 1;
```
**Tushuntirish:** `PG_LSN` ma'lumotlar turi PostgreSQL da log sequence number'larni to'g'ridan-to'g'ri solishtirish imkonini beradi (`<`, `>`). `ON CONFLICT DO UPDATE WHERE ... < EXCLUDED.last_applied_lsn` sharti xabarlarning navbatdan tashqari kelishi (Out-of-Order delivery) muammosini arxitektura darajasida bartaraf qiladi.

---

### Topshiriq #1135: Soft-Delete va Hard-Delete Operatsiyalarini CDC Oqimida Differensiatsiya Qilish
**Tavsif:** Biznes tizimida qator `deleted_at = now()` orqali yumshoq o'chirilishi (Soft-Delete) yoki ma'lumotlar bazasidan butunlay yo'q qilinishi (Hard-Delete `DELETE FROM`) mumkin. Qabul qiluvchi analitika ombori bu ikki holatni to'g'ri qayta ishlashi shart.
**Talablar:** Debezium 'd' operatsiyasi (Tombstone) va Soft-delete UPDATE amallarini ajratib oluvchi trigger yoki qabul qiluvchi protsedura yozish.
**Yechim (SQL):**
```sql
-- 1. Analitika markazidagi sinxronlashtiriluvchi jadval
CREATE TABLE target_audit_customers (
    customer_id BIGINT PRIMARY KEY,
    full_name TEXT NOT NULL,
    is_soft_deleted BOOLEAN DEFAULT false,
    is_hard_deleted BOOLEAN DEFAULT false,
    soft_deleted_at TIMESTAMPTZ,
    hard_deleted_at TIMESTAMPTZ,
    last_event_op CHAR(1)
);

-- 2. CDC oqimidan kelgan har qanday o'chirishni qayta ishlovchi protsedura
CREATE OR REPLACE PROCEDURE pr_process_cdc_deletion(
    p_customer_id BIGINT,
    p_op CHAR(1), -- 'u' (update) yoki 'd' (delete)
    p_before_data JSONB,
    p_after_data JSONB,
    p_event_time TIMESTAMPTZ
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_op = 'u' AND (p_after_data->>'deleted_at') IS NOT NULL AND (p_before_data->>'deleted_at') IS NULL THEN
        -- SOFT DELETE holati aniqlandi
        UPDATE target_audit_customers
        SET is_soft_deleted = true,
            soft_deleted_at = p_event_time,
            last_event_op = 'S'
        WHERE customer_id = p_customer_id;
        
    ELSIF p_op = 'd' THEN
        -- HARD DELETE holati: qatorni o'chirmaymiz, aksincha arxiv holatiga belgilaymiz
        UPDATE target_audit_customers
        SET is_hard_deleted = true,
            hard_deleted_at = p_event_time,
            last_event_op = 'H'
        WHERE customer_id = p_customer_id;
    END IF;
END;
$$;
```
**Tushuntirish:** Ko'pincha CDC tizimlarida Hard-Delete amalga oshirilganda Kafka `tombstone` (null payload) hodisasini yuboradi. Agar analitika ombori ushbu qatorni to'g'ridan-to'g'ri o'chirib yuborsa, tarixiy hisobotlar va moliyaviy audit ma'lumotlari uzilib qoladi. Shuning uchun CDC iste'molchisida Hard Delete holatini 'Logical Flag' orqali saqlab qolish eng to'g'ri amaliyotdir.

---

### Topshiriq #1136: postgres_fdw: Tashqi Server va Foydalanuvchi Xaritalarini (User Mapping) Xavfsiz Sozlash
**Tavsif:** Markaziy PostgreSQL ma'lumotlar bazasi orqali boshqa masofaviy PostgreSQL serveridagi jadvallarni xuddi mahalliy jadvallardek so'rov qilish (Federated Query) talab etiladi.
**Talablar:** postgres_fdw kengaytmasini o'rnatish, FOREIGN SERVER, USER MAPPING va FOREIGN TABLE larni to'g'ri xavfsizlik cheklovlari bilan e'lon qilish.
**Yechim (SQL):**
```sql
-- 1. FDW kengaytmasini o'rnatish
CREATE EXTENSION IF NOT EXISTS postgres_fdw;

-- 2. Masofaviy server obyektini ro'yxatdan o'tkazish
CREATE SERVER remote_billing_srv
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (
    host '192.168.10.50',
    port '5432',
    dbname 'billing_db',
    keepalives '1',
    keepalives_idle '30',
    connect_timeout '10'
);

-- 3. Mahalliy foydalanuvchini masofaviy server foydalanuvchisiga xaritalash (User Mapping)
CREATE USER MAPPING FOR current_user
SERVER remote_billing_srv
OPTIONS (
    user 'fdw_reader_user',
    password 'SuperSecurePassword2026!'
);

-- 4. Masofaviy serverdagi bitta jadvalni mahalliy nom bilan e'lon qilish
CREATE FOREIGN TABLE foreign_payments (
    payment_id BIGINT,
    account_id BIGINT,
    amount NUMERIC(14,2),
    status TEXT,
    created_at TIMESTAMPTZ
)
SERVER remote_billing_srv
OPTIONS (
    schema_name 'public',
    table_name 'payments'
);

-- 5. Tashqi jadvaldan oddiy SELECT so'rovi bajarish
SELECT payment_id, amount, status FROM foreign_payments WHERE status = 'SUCCESS' LIMIT 5;
```
**Tushuntirish:** `postgres_fdw` PostgreSQL ning SQL/MED (Management of External Data) standartini amalga oshiradi. U masofaviy server bilan alohida ulanish ochadi va so'rovlarni optimallashtirilgan holda yuboradi. Foydalanuvchi paroli bazada shifrlanmagan holda saqlanmasligi uchun faqat vakolatli rollarga `USAGE` huquqi berilishi shart.

---

### Topshiriq #1137: IMPORT FOREIGN SCHEMA Bilan Masofaviy Sxemani Avtomatik Import Qilish
**Tavsif:** Masofaviy serverda o'nlab jadvallar mavjud bo'lganda, ularning har birini qo'lda `CREATE FOREIGN TABLE` qilib chiqish ko'p vaqt oladi va insoniy xatolarga sabab bo'ladi.
**Talablar:** IMPORT FOREIGN SCHEMA buyrug'idan foydalanib, faqat kerakli jadvallarni (LIMIT TO) mahalliy maxsus sxemaga avtomatik yuklash.
**Yechim (SQL):**
```sql
-- 1. Tashqi jadvallar uchun alohida mahalliy sxema yaratish
CREATE SCHEMA IF NOT EXISTS remote_crm;

-- 2. Masofaviy serverdagi 'public' sxemasidan faqat tanlangan jadvallarni import qilish
IMPORT FOREIGN SCHEMA public
    LIMIT TO (customers, deals, contacts, pipeline_stages)
    FROM SERVER remote_billing_srv
    INTO remote_crm;

-- Yoki aksincha, maxfiy jadvallardan tashqari barchasini import qilish (EXCEPT):
-- IMPORT FOREIGN SCHEMA public
--     EXCEPT (passwords, api_keys, audit_secrets)
--     FROM SERVER remote_billing_srv
--     INTO remote_crm;

-- 3. Import qilingan tashqi jadvallar ro'yxatini ko'rish
SELECT 
    foreign_table_schema,
    foreign_table_name,
    foreign_server_name
FROM information_schema.foreign_tables
WHERE foreign_server_name = 'remote_billing_srv';

-- 4. Import qilingan jadvalga to'g'ridan-to'g'ri so'rov yuborish
SELECT count(*) AS total_remote_customers FROM remote_crm.customers;
```
**Tushuntirish:** `IMPORT FOREIGN SCHEMA` masofaviy serverdagi jadvallarning ustun nomlari, tiplari va `NOT NULL` cheklovlarini avtomatik o'qib, mahalliy tizimda mos tashqi jadvallarni hosil qiladi. Bu ma'lumotlar bazalari orasidagi federatsiya integratsiyasini sekundlar ichida sozlash imkonini beradi.

---

### Topshiriq #1138: postgres_fdw da Filtr va Agregatlarni Masofaga Surish (Pushdown Optimization)
**Tavsif:** Agar 100 million qatorlik masofaviy jadvaldan `SUM()` yoki `WHERE year = 2026` qidirilsa, barcha 100 million qator tarmoq orqali tortib olinsa, tizim qotib qoladi. So'rovni to'g'ridan-to'g'ri masofaviy serverda bajarilishini ta'minlash lozim.
**Talablar:** pushdown parametrlarini (use_remote_estimate, pushdown) yoqish va EXPLAIN ANALYZE orqali pushdown ishlashini isbotlash.
**Yechim (SQL):**
```sql
-- 1. Tashqi serverda agregatlar va funksiyalarni masofaga surishni faollashtirish
ALTER SERVER remote_billing_srv OPTIONS (
    ADD fdw_startup_cost '100.0',
    ADD fdw_tuple_cost '0.2',
    ADD use_remote_estimate 'true' -- Masofaviy server statistikasini (ANALYZE) inobatga olish
);

-- 2. Alohida jadval darajasida pushdown sozlamalari
ALTER FOREIGN TABLE foreign_payments OPTIONS (
    ADD fetch_size '5000' -- Bitta tarmoq so'rovida qancha qator tortilishi
);

-- 3. So'rov bajarilish rejasini (EXPLAIN) tahlil qilish
-- Agar pushdown to'g'ri ishlasa, 'Foreign Scan' blokida masofaviy so'rov ko'rinadi:
-- Remote SQL: SELECT sum(amount), count(*) FROM public.payments WHERE (created_at >= '2026-01-01')
EXPLAIN (VERBOSE, COSTS)
SELECT 
    count(*),
    sum(amount) AS total_revenue
FROM foreign_payments
WHERE created_at >= '2026-01-01 00:00:00+00';

-- 4. Masofaviy serverda qo'llab-quvvatlanmaydigan no-shaffof funksiyalar pushdown'ni to'xtatadi.
-- Shu sababli faqat IMMUTABLE va standart funksiyalardan foydalanish tavsiya etiladi.
```
**Tushuntirish:** `Aggregate Pushdown` va `WHERE Pushdown` postgres_fdw ning eng muhim optimizatsiyasidir. Agar `use_remote_estimate = true` bo'lsa, rejalashtiruvchi masofaviy serverdan statistika oladi va `SUM()`, `COUNT()` kabi agregatlarni masofaviy serverning o'zida hisoblab, tarmoq orqali faqat bitta yakuniy qatorni qaytaradi. Bu tarmoq I/O yuklamasini 99.9% ga kamaytiradi.

---

### Topshiriq #1139: Masofaviy Serverlar O'rtasida Birlashtirish (Remote Join Pushdown) va fetch_size Boshqaruvi
**Tavsif:** Bitta masofaviy serverda joylashgan ikkita katta jadval (`customers` va `orders`) o'zaro `JOIN` qilinganda, ikkala jadval ham mahalliy serverga tortilmasdan, masofaviy serverning o'zida birlashtirilishi kerak.
**Talablar:** postgres_fdw da join_pushdown parametrlarini boshqarish va fetch_size ni katta hajmli skanlar uchun optimallashtirish.
**Yechim (SQL):**
```sql
-- 1. Tashqi server parametrlarida join pushdown yoqilganligini tekshirish
-- PostgreSQL 9.6+ dan boshlab sukut bo'yicha yoqilgan
-- ALTER SERVER remote_billing_srv OPTIONS (SET async_capable 'true');

-- 2. Ikki tashqi jadvalni birlashtiruvchi so'rov rejasini tekshirish
EXPLAIN (VERBOSE, COSTS)
SELECT 
    c.foreign_table_name,
    p.amount
FROM remote_crm.customers c
JOIN foreign_payments p ON c.customer_id = p.account_id
WHERE p.status = 'PAID';

-- Bajarilish rejasida:
-- Foreign Scan on (join tree)
-- Remote SQL: SELECT r1.name, r2.amount FROM (public.customers r1 JOIN public.payments r2 ON (r1.id = r2.account_id)) ...

-- 3. Tarmoq buferini (fetch_size) sozlash
-- Katta hajmli hisobotlar uchun sukut bo'yicha 100 qator o'rniga 10 000 qator qilib belgilash
ALTER SERVER remote_billing_srv OPTIONS (ADD fetch_size '10000');
SELECT pg_reload_conf();
```
**Tushuntirish:** Agar ikkala jadval aynan bitta masofaviy serverda va bitta user mapping orqali ochilgan bo'lsa, PostgreSQL `Join Pushdown` ni amalga oshiradi. Bu butun birlashtirish jarayonini masofadagi server CPU va xotirasida bajarib, mahalliy tugunga faqat birlashgan natijani jo'natadi.

---

### Topshiriq #1140: Taqsimlangan Tranzaksiyalar va Ikki Fazali Kommit (Two-Phase Commit - 2PC)
**Tavsif:** Ilova bitta biznes harakati davomida ham mahalliy bazadagi balansni kamaytirishi, ham masofaviy serverdagi xizmatni faollashtirishi kerak. Tarmoq uzilsa ham pul yo'qolmasligi uchun 2PC (PREPARE TRANSACTION) talab etiladi.
**Talablar:** max_prepared_transactions parametrini yoqish, PREPARE TRANSACTION, COMMIT PREPARED va nosozlikda ROLLBACK PREPARED amallarini SQL da bajarish.
**Yechim (SQL):**
```sql
-- 1. Serverda 2PC tranzaksiyalarni qo'llab-quvvatlash uchun postgresql.conf sozlamasi
-- max_prepared_transactions kamida max_connections ga teng bo'lishi lozim
ALTER SYSTEM SET max_prepared_transactions = 100;
-- Serverni qayta ishga tushirish lozim

-- 2. Ikki fazali tranzaksiyani boshlash va tayyorlash (1-FAZA: PREPARE)
BEGIN;
UPDATE billing_customers SET balance = balance - 250000.00 WHERE customer_id = 1;
-- Tranzaksiyani global unikal identifikator bilan zaxiralash
PREPARE TRANSACTION 'global_tx_order_2026_0987';

-- 3. Qotib qolgan yoki tayyorlangan tranzaksiyalarni monitoring qilish
SELECT 
    gid,
    prepared,
    owner,
    database
FROM pg_prepared_xacts;

-- 4. Agar masofaviy tugun ham o'z ishini muvaffaqiyatli tayyorlagan bo'lsa (2-FAZA: COMMIT):
COMMIT PREPARED 'global_tx_order_2026_0987';

-- Agar masofaviy tizim xato bersa, birinchi serverdagi o'zgarishni bekor qilish:
-- ROLLBACK PREPARED 'global_tx_order_2026_0987';
```
**Tushuntirish:** Ikki Fazali Kommit (2PC) taqsimlangan tizimlarda atomarlikni (Atomicity) ta'minlovchi klassik protokoldir. `PREPARE TRANSACTION` paytida barcha o'zgarishlar diskka yoziladi va qulflar saqlanadi. Klient uzilib ketsa ham tranzaksiya yopilmaydi va tranzaksiya koordinatori qaroriga ko'ra keyinchalik kommit yoki rollback qilinadi.

---

### Topshiriq #1141: Taqsimlangan Partitsiyalash: Mahalliy Master Jadval Ostiga Masofaviy FDW Bo'laklarni Joylashtirish
**Tavsif:** Markaziy ombor jadvallari shunchalik kattaki, ularning har bir yillik bo'lagi alohida serverlarda (Shard-1, Shard-2) jismoniy joylashishi kerak. Mijoz esa bitta umumiy jadvalga so'rov yuborishi lozim.
**Talablar:** Mahalliy Declarative Partition jadvali yaratish va uning partitsiyalari sifatida FOREIGN TABLE larni biriktirish (ATTACH PARTITION).
**Yechim (SQL):**
```sql
-- 1. Asosiy bo'lim boshqaruvchi master jadvali (Mahalliy serverda)
CREATE TABLE enterprise_logs_distributed (
    log_id BIGINT NOT NULL,
    log_date DATE NOT NULL,
    service_name VARCHAR(50) NOT NULL,
    message TEXT
) PARTITION BY RANGE (log_date);

-- 2. 2025-yilgi ma'lumotlar uchun 1-masofaviy serverdagi tashqi jadvalni yaratish
CREATE FOREIGN TABLE foreign_logs_2025 (
    log_id BIGINT NOT NULL,
    log_date DATE NOT NULL,
    service_name VARCHAR(50) NOT NULL,
    message TEXT
) SERVER remote_billing_srv
OPTIONS (table_name 'logs_2025');

-- 3. 2026-yilgi ma'lumotlar uchun 2-masofaviy serverdagi tashqi jadvalni yaratish
-- CREATE FOREIGN TABLE foreign_logs_2026 (...) SERVER remote_shard2_srv OPTIONS (table_name 'logs_2026');

-- 4. Tashqi jadvallarni master jadvalga partitsiya sifatida ulash (ATTACH)
ALTER TABLE enterprise_logs_distributed 
ATTACH PARTITION foreign_logs_2025 
FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

-- 5. Partitsiya qirqish (Partition Pruning) tekshiruvi:
-- So'rov faqat 2025 yilga tegishli bo'lsa, boshqa shard serverlariga so'rov bormaydi
EXPLAIN (COSTS OFF)
SELECT * FROM enterprise_logs_distributed
WHERE log_date = '2025-06-15';
```
**Tushuntirish:** Bu arxitektura PostgreSQL yordamida to'liq taqsimlangan ma'lumotlar bazasini (Distributed Database Sharding) tashkil qiladi. So'rov rejalashtiruvchisi `Partition Pruning` mexanizmi orqali `WHERE` shartiga qarab aynan qaysi masofaviy shard serveriga murojaat qilishni aniqlaydi va qolgan shardlarni butunlay chetlab o'tadi.

---

### Topshiriq #1142: Asinxron Parallel Tashqi So'rovlar (enable_async_append = on) Bilan Shardlarni O'qish
**Tavsif:** Agar master jadval ostida 4 ta turli xil masofaviy serverdagi FDW jadvallari bo'lsa, standart ketma-ket o'qish 4 barobar ko'p vaqt oladi. Ulardan bir vaqtda parallel ravishda ma'lumot tortish talab etiladi.
**Talablar:** PostgreSQL 14+ dagi enable_async_append parametrini yoqish, serverlarda async_capable = true sozlash va parallel bajarilish tezligini taqqoslash.
**Yechim (SQL):**
```sql
-- 1. Masofaviy serverlarda asinxron so'rov qobiliyatini yoqish
ALTER SERVER remote_billing_srv OPTIONS (ADD async_capable 'true');

-- 2. Sessiya darajasida asinxron Append mexanizmini faollashtirish
SET enable_async_append = on;

-- 3. Bir nechta masofaviy partitsiyalarni qamrab oluvchi so'rovni bajarish
EXPLAIN (ANALYZE, VERBOSE)
SELECT 
    service_name,
    count(*) AS error_count
FROM enterprise_logs_distributed
WHERE log_date BETWEEN '2024-01-01' AND '2026-12-31'
GROUP BY service_name;

-- Rejada 'Async Foreign Scan' tugunlari paydo bo'ladi.
-- Bu shuni anglatadiki, PostgreSQL bir vaqtning o'zida barcha shard serverlariga tarmoq so'rovini yuboradi
-- va javoblarni ular kelishi bilanoq asinxron ravishda qabul qilib oladi!
```
**Tushuntirish:** `enable_async_append = on` yordamida PostgreSQL taqsimlangan so'rovlar bajarilish vaqtini dramatik ravishda pasaytiradi. Ketma-ket rejimda har bir masofaviy tarmoq javobi kutilgan bo'lsa, asinxron rejimda eng sekin server qancha vaqt olsa, umumiy so'rov vaqti ham shunga teng bo'ladi ($T_{jami} pprox \max(T_1, T_2, ...)$).

---

### Topshiriq #1143: file_fdw Yordamida Tashqi CSV va Log Fayllarini To'g'ridan-to'g'ri SQL Bilan So'rov Qilish
**Tavsif:** Server operatsion tizimidagi xom Nginx kirish jurnallari (access.log) yoki tashqi tizimlardan kelgan CSV fayllarini bazaga yuklab o'tirmasdan, bevosita SQL yordamida tezkor tahlil qilish kerak.
**Talablar:** file_fdw kengaytmasini ulash, tashqi fayl serverini yaratish va format parametrlarini (CSV, HEADER, DELIMITER) sozlash.
**Yechim (SQL):**
```sql
-- 1. file_fdw kengaytmasini o'rnatish (superuser talab qilinadi)
CREATE EXTENSION IF NOT EXISTS file_fdw;

-- 2. Tashqi fayl serverini yaratish
CREATE SERVER file_server FOREIGN DATA WRAPPER file_fdw;

-- 3. CSV faylga bog'langan tashqi jadval yaratish
CREATE FOREIGN TABLE fdw_nginx_logs (
    client_ip INET,
    log_time TEXT,
    http_method VARCHAR(10),
    request_url TEXT,
    status_code INT,
    response_bytes BIGINT
)
SERVER file_server
OPTIONS (
    filename '/var/log/nginx/api_access.csv',
    format 'csv',
    header 'true',
    delimiter ','
);

-- 4. Tashqi log fayl ustida murakkab SQL tahlillarini yurgizish
SELECT 
    status_code,
    count(*) AS hit_count,
    round(avg(response_bytes), 2) AS avg_bytes
FROM fdw_nginx_logs
GROUP BY status_code
ORDER BY hit_count DESC;
```
**Tushuntirish:** `file_fdw` operatsion tizimdagi fayllarni diskdan xotiraga nusxalamasdan, to'g'ridan-to'g'ri streaming rejimida o'qish imkonini beradi. Bu Gigabaytlab hajmdagi loglarni ma'lumotlar bazasi diskiga qo'shimcha yuklamasdan turib SQL analitika kuchi bilan tadqiq qilish uchun nihoyatda qulay vositadir.

---

### Topshiriq #1144: Taqsimlangan So'rovlarni EXPLAIN (ANALYZE, VERBOSE) Bilan Tahlil Qilish va Tarmoq I/O Optimizatsiyasi
**Tavsif:** Taqsimlangan FDW so'rovlari sekin ishlayotganda qaysi qism tarmoq orqali o'tayotgani va qaysi qism mahalliy diskda bajarilayotganini chuqur tahlil qilish zarur.
**Talablar:** Tashqi so'rovlar rejasidagi Remote SQL, Foreign Scan parametrlarini o'rganish va parametrlar moslashuvini amalga oshirish.
**Yechim (SQL):**
```sql
-- Masofaviy so'rov rejasini batafsil tahlil qilish
EXPLAIN (ANALYZE, VERBOSE, BUFFERS, SETTINGS)
SELECT 
    p.status,
    count(*) AS total_count,
    sum(p.amount) AS total_amount
FROM foreign_payments p
WHERE p.created_at >= '2026-01-01 00:00:00+00'
GROUP BY p.status;

-- Tahlil qilinishi kerak bo'lgan asosiy metrikalar:
-- 1. 'Remote SQL': Masofaviy serverga aynan qanday so'rov ketganini ko'rsatadi.
--    Agar u yerda GROUP BY bo'lmasa, demak agregat pushdown ishlamagan!
-- 2. 'Planning Time' va 'Execution Time'
-- 3. 'Rows Removed by Filter': Filtrlash masofada emas, mahalliy serverda bo'lganini fosh qiladi.
-- 4. Tarmoq orqali o'tgan satrlar soni.

-- Agar so'rov yomon rejalashtirilayotgan bo'lsa, tashqi jadval statistikasini yangilash:
ANALYZE foreign_payments;
```
**Tushuntirish:** Tashqi jadvallar ustida statistik ma'lumotlar (n_distinct, most_common_vals) mahalliy `pg_statistic` jadvalida avtomatik yangilanmaydi. Shuning uchun vaqti-vaqti bilan tashqi jadvalga `ANALYZE` berib turish rejalashtiruvchiga tarmoq xarajatlarini to'g'ri baholashga yordam beradi.

---

### Topshiriq #1145: Heterogen Federatsiya: Mahalliy va Masofaviy Ma'lumotlarni Birlashtiruvchi Dinamik Tahliliy Ko'rinishlar
**Tavsif:** Mahalliy operatsion foydalanuvchilar ma'lumotlari (`users`) bilan masofaviy to'lovlar serveridagi tranzaksiyalarni (`payments`) birlashtirib, bitta konsolidatsiyalangan mijoz profili ko'rinishini (Federated View) barpo etish talab etiladi.
**Talablar:** Mahalliy jadval va FDW tashqi jadvalini optimal indekslash va keshlovchi materiallashtirilgan ko'rinish (Materialized View) bilan bog'lash.
**Yechim (SQL):**
```sql
-- 1. Mahalliy foydalanuvchilar jadvali
CREATE TABLE local_crm_users (
    user_id BIGINT PRIMARY KEY,
    full_name TEXT NOT NULL,
    segment VARCHAR(50) DEFAULT 'RETAIL'
);

-- 2. Federativ tahliliy ko'rinishni barpo etish
CREATE OR REPLACE VIEW v_customer_complete_profile AS
SELECT 
    u.user_id,
    u.full_name,
    u.segment,
    coalesce(stats.total_paid, 0) AS total_lifetime_spent,
    coalesce(stats.payment_count, 0) AS lifetime_orders,
    stats.last_payment_date
FROM local_crm_users u
LEFT JOIN (
    -- Tashqi jadvaldan agregat olingan subquery (Pushdown bo'lishi uchun)
    SELECT 
        account_id,
        sum(amount) AS total_paid,
        count(*) AS payment_count,
        max(created_at) AS last_payment_date
    FROM foreign_payments
    WHERE status = 'SUCCESS'
    GROUP BY account_id
) stats ON u.user_id = stats.account_id;

-- 3. Tezkor hisobotlar uchun davriy yangilanuvchi Materialized View
CREATE MATERIALIZED VIEW mv_customer_summary AS
SELECT * FROM v_customer_complete_profile;

CREATE UNIQUE INDEX idx_mv_cust_id ON mv_customer_summary(user_id);

-- 4. Ko'rinishni har soatda yangilash (Zero-locking CONCURRENTLY bilan)
-- REFRESH MATERIALIZED VIEW CONCURRENTLY mv_customer_summary;
```
**Tushuntirish:** Federated View orqali turli ma'lumotlar bazalaridagi ma'lumotlar fizik jihatdan bitta joyga yig'ilmasdan turib yagona relyatsion mantiq ostida birlashadi. Tez-tez murojaat qilinadigan federativ so'rovlar uchun `MATERIALIZED VIEW` va `REFRESH CONCURRENTLY` orqali tarmoq kechikishini keshlab olish tavsiya etiladi.

---

### Topshiriq #1146: PgBouncer Havuz Rejimlari (Session, Transaction, Statement Pooling) Tahlili va Konfiguratsiyasi
**Tavsif:** PostgreSQL da har bir yangi klient ulanishi alohida operatsion tizim jarayonini (OS process) ochadi va 10-20 MB operativ xotira band qiladi. 10 000 ta parallel klient ulanishiga bardosh berish uchun PgBouncer ulanishlar havuzini (Connection Pooler) sozlash zarur.
**Talablar:** Session, Transaction va Statement pooling farqlarini tahlil qilish, pgbouncer.ini asosiy parametrlarini (pool_mode, default_pool_size, max_client_conn) loyihalash.
**Yechim (SQL):**
```sql
-- PgBouncer konfiguratsiyasi (pgbouncer.ini fayli mantiqi):
/*
[databases]
production_db = host=127.0.0.1 port=5432 dbname=production_db auth_user=pgbouncer_auth

[pgbouncer]
logfile = /var/log/postgresql/pgbouncer.log
pidfile = /var/run/postgresql/pgbouncer.pid
listen_addr = *
listen_port = 6432
auth_type = scram-sha-256
auth_file = /etc/pgbouncer/userlist.txt

-- Havuz rejimi: 'transaction' eng yuqori masshtablashni ta'minlaydi
-- Server ulanishi faqat tranzaksiya tugaguncha mijozga beriladi, 
-- tranzaksiya tugashi bilan boshqa klientga qayta taqsimlanadi!
pool_mode = transaction

-- Ulanish chegaralari
max_client_conn = 10000      -- Tashqi klientlarning maksimal soni
default_pool_size = 25       -- PostgreSQL backend'iga ochiladigan real ulanishlar soni
min_pool_size = 5            -- Doimiy ochiq turadigan minimal ulanishlar
reserve_pool_size = 5        -- Favqulodda yuklama paytida qo'shiladigan ulanishlar
reserve_pool_timeout = 5.0   -- Kutish vaqti (soniya)

-- Xavfsiz tozalash: Har bir tranzaksiya o'rtasida sessiya holatini tozalash
server_reset_query = DISCARD ALL
*/

-- PostgreSQL tomonida PgBouncer uchun maxsus autentifikatsiya foydalanuvchisi
CREATE ROLE pgbouncer_auth WITH LOGIN PASSWORD 'PoolerAuthPassword2026!';
GRANT CONNECT ON DATABASE production TO pgbouncer_auth;
```
**Tushuntirish:** `pool_mode = transaction` PgBouncer'ning eng samarali rejimidir. U 10 000 ta mijoz so'rovini PostgreSQL-dagi atigi 25-50 ta real jarayonga multiplexing qilib beradi. Bunda e'tibor berish lozim: `SET LOCAL`, `LISTEN/NOTIFY` va sessiyaga bog'liq vaqtinchalik jadvallar tranzaksiyadan tashqarida saqlanmaydi.

---

### Topshiriq #1147: PgBouncer Tranzaksion Pooling Rejimida Prepared Statements Bilan Xavfsiz Ishlash
**Tavsif:** Tranzaksion pooling rejimida `PREPARE stmt AS ...` buyrug'i bitta backend server jarayonida saqlanadi, keyingi so'rov esa boshqa backendga tushsa 'prepared statement does not exist' xatosi chiqadi.
**Talablar:** pgbouncer.ini dagi max_prepared_statements (PgBouncer 1.21+) imkoniyati yoki klient drayveridagi unnamed prepared statements sozlamalarini SQL darajasida moslash.
**Yechim (SQL):**
```sql
-- 1. PgBouncer 1.21+ versiyasida o'rnatilgan Prepared Statement qo'llab-quvvatlovi:
/*
-- pgbouncer.ini sozlamasi:
max_prepared_statements = 100
*/

-- 2. Agar eski PgBouncer ishlatilsa, mijoz kutubxonalarida (masalan, JDBC, pgx, node-postgres)
-- 'unnamed prepared statements' yoki 'binary simple query protocol' yoqilishi shart.

-- 3. Tranzaksiya ichida lokal parametrlar va xavfsiz tozalash:
BEGIN;
-- Faqat joriy tranzaksiya uchun amal qiladigan lokal parametr
SET LOCAL work_mem = '64MB';

-- Tranzaksiya tugashi bilan PgBouncer serverni yangi mijozga berishdan oldin tozalaydi:
-- server_reset_query = DISCARD ALL (yoki DISCARD TEMP)
COMMIT;

-- 4. DISCARD ALL qanday ishlashini tekshirish
-- U barcha vaqtinchalik jadvallar, keshlar va tayyorlangan bayonotlarni tozalaydi:
DISCARD ALL;
```
**Tushuntirish:** PgBouncer 1.21 versiyasiga qadar tranzaksion pooling va Prepared Statement'lar bir-biriga mos kelmas edi va dasturchilar ularni o'chirib qo'yishga majbur bo'lar edilar. Yangi versiyalarda PgBouncer o'zida prepared statements keshini boshqaradi va backend almashganda bayonotni yangi serverda shaffof qayta ro'yxatdan o'tkazadi.

---

### Topshiriq #1148: PgBouncer Ma'muriy Konsoli: SHOW POOLS, SHOW CLIENTS va PAUSE/RESUME Boshqaruvi
**Tavsif:** Ishlab chiqarish bazasida yuklama keskin oshganda yoki yangilanish (patch) o'tkazilayotganda havuz holatini kuzatish va ulanishlarni vaqtinchalik to'xtatib turish (PAUSE) talab etiladi.
**Talablar:** PgBouncer maxsus ma'muriy portiga (6432) ulanib SHOW POOLS, SHOW CLIENTS, SHOW SERVERS, PAUSE va RESUME buyruqlarini boshqarish.
**Yechim (SQL):**
```sql
-- PgBouncer ma'muriy bazasiga ulanish:
-- psql -h 127.0.0.1 -p 6432 -U pgbouncer_admin pgbouncer

-- 1. Barcha ma'lumotlar bazalari bo'yicha havuzlar holatini tekshirish
SHOW POOLS;
-- Qaytariladigan asosiy ustunlar:
-- database, user, cl_active (faol mijozlar), cl_waiting (navbatda kutayotgan mijozlar),
-- sv_active (serverda ishlayotgan), sv_idle (bo'sh turgan ulanishlar), maxwait (navbatdagi maksimal kutish vaqti)

-- 2. Navbatda tiqilib qolgan (cl_waiting) mijozlarni ko'rish
SHOW CLIENTS;

-- 3. PostgreSQL serveriga ulangan real backend ulanishlarni ko'rish
SHOW SERVERS;

-- 4. Bazada operativ yangilanish o'tkazish uchun yangi so'rovlarni vaqtinchalik to'xtatish (PAUSE)
-- Klientlar uzilmaydi, ularning so'rovlari navbatda kutib turadi!
PAUSE production_db;

-- 5. Texnik amallar tugagach, so'rovlar oqimini qayta davom ettirish
RESUME production_db;

-- 6. Konfiguratsiya fayli o'zgarganda xizmatni to'xtatmasdan qayta yuklash
RELOAD;
```
**Tushuntirish:** `PAUSE` buyrug'i klasterga nol to'xtalish bilan texnik xizmat ko'rsatishning yuragi hisoblanadi. U PostgreSQL-dagi barcha joriy tranzaksiyalar tugashini kutadi va yangi so'rovlarni PgBouncer buferida ushlab turadi. Ma'murlar bazani qayta ishga tushirishi yoki failover qilishi bilanoq `RESUME` beriladi va hech qaysi mijoz 'Connection Refused' xatosini olmaydi.

---

### Topshiriq #1149: HAProxy Orqali Read-Write va Read-Only Replikatsiyani Portlar Bo'yicha Marshrutlash
**Tavsif:** Ilovalar yozish so'rovlarini asosiy Primary serverga, og'ir analitik o'qish so'rovlarini esa Standby replikalariga yo'naltirishi kerak. Buni avtomatlashtirish uchun HAProxy orqali Read-Write va Read-Only marshrutlash talab etiladi.
**Talablar:** PostgreSQL sog'lig'ini tekshiruvchi HTTP/SQL health-check va HAProxy frontend/backend qoidalarini tuzish.
**Yechim (SQL):**
```sql
-- PostgreSQL tomonida sog'liqni tekshirish uchun ko'rinish va foydalanuvchi:
-- Primary server 'is_standby = false', Standby server esa 'is_standby = true' qaytaradi
CREATE OR REPLACE VIEW v_cluster_node_role AS
SELECT 
    CASE 
        WHEN pg_is_in_recovery() THEN 'READ_ONLY_STANDBY'
        ELSE 'READ_WRITE_PRIMARY'
    END AS node_role,
    inet_server_addr() AS server_ip;

-- HAProxy konfiguratsiyasi (haproxy.cfg mantiqi):
/*
-- 1. WRITE PORT: 5432 (Faqat Primary serverga yo'naltiradi)
frontend postgres_write_front
    bind *:5432
    mode tcp
    default_backend postgres_write_back

backend postgres_write_back
    mode tcp
    option tcp-check
    -- PostgreSQL health check orqali pg_is_in_recovery() ni tekshiradi
    -- faqat Master (recovery=false) bo'lgan server trafigi ochiladi
    tcp-check send-binary 000000100003000075736572007067636865636b0000
    server pg_node1 192.168.1.10:6432 check
    server pg_node2 192.168.1.20:6432 check backup

-- 2. READ PORT: 5433 (Barcha Standby replikalari bo'yicha Round-Robin muvozanatlash)
frontend postgres_read_front
    bind *:5433
    mode tcp
    default_backend postgres_read_back

backend postgres_read_back
    mode tcp
    balance roundrobin
    server pg_replica1 192.168.1.20:6432 check
    server pg_replica2 192.168.1.30:6432 check
*/
```
**Tushuntirish:** HAProxy ma'lumotlar bazasi klasteri oldida yuklamani taqsimlovchi (Load Balancer) sifatida xizmat qiladi. Port 5432 orqali tushgan yozish so'rovlari faqatgina aktiv Primary'ga boradi, port 5433 orqali esa yuzlab o'qish so'rovlari Standby replikalari bo'ylab `roundrobin` orqali taqsimlanadi, bu esa Primary serverni og'ir o'qish yuklamasidan ozod qiladi.

---

### Topshiriq #1150: Ulanish Bo'ronini (Connection Storm) Monitoring Qilish va Kutish Hodisalarini (Wait Events) Tahlil Qilish
**Tavsif:** Ilova to'satdan qayta yuklanganda minglab yangi ulanishlar PostgreSQL serveriga birdaniga yopirilib keladi (Thundering Herd / Connection Storm). Havuzning to'lib qolganligini va qotib qolgan sessiyalarni aniqlash zarur.
**Talablar:** pg_stat_activity jadvalidan wait_event_type, wait_event va connection states tahlili orqali havuz tiqilinchini aniqlovchi SQL skriptini yozish.
**Yechim (SQL):**
```sql
-- Ulanishlar bo'roni va havuz tiqilinchini aniqlovchi kompleks diagnostika so'rovi
SELECT 
    coalesce(wait_event_type, 'CPU / Running') AS wait_type,
    coalesce(wait_event, 'Processing') AS wait_event,
    state,
    count(*) AS session_count,
    round(100.0 * count(*) / sum(count(*)) OVER (), 2) AS percentage_of_total
FROM pg_stat_activity
WHERE backend_type = 'client backend'
GROUP BY wait_event_type, wait_event, state
ORDER BY session_count DESC;

-- Havuzda juda uzoq vaqt navbatda turgan yoki qotib qolgan tranzaksiyalarni aniqlash
SELECT 
    pid,
    usename,
    client_addr,
    application_name,
    state,
    wait_event_type,
    wait_event,
    clock_timestamp() - xact_start AS transaction_duration,
    clock_timestamp() - query_start AS query_duration,
    query
FROM pg_stat_activity
WHERE state IN ('active', 'idle in transaction')
  AND (clock_timestamp() - xact_start) > interval '10 seconds'
ORDER BY transaction_duration DESC
LIMIT 10;

-- Xavfli 'idle in transaction' sessiyalarini majburiy to'xtatuvchi xavfsizlik parametri
-- (postgresql.conf da o'rnatiladi):
-- idle_in_transaction_session_timeout = '30000ms'; -- 30 soniyada avtomatik terminate qilinadi
```
**Tushuntirish:** `wait_event_type = 'ClientRead'` mijoz so'rov jo'natishini server kutib turganini bildiradi. Agar serverda yuzlab `idle in transaction` sessiyalari paydo bo'lsa, ular qulflarni ushlab turib boshqa ulanishlarning navbatda to'planishiga (Connection Storm) sabab bo'ladi. `idle_in_transaction_session_timeout` parametri orqali ushbu muammo ildizi bilan hal etiladi.

---
