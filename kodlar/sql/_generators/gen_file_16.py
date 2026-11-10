import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

# List of 50 tasks for File 16: 751 - 800
# Tranzaksiyalar va ACID xususiyatlari (BEGIN, COMMIT, ROLLBACK, SAVEPOINT, Isolation Levels, Anomalies, SELECT FOR UPDATE, SKIP LOCKED, Deadlocks, Advisory Locks)

tx_data = [
    (
        751,
        "Tranzaksiyani boshlash va tasdiqlash: BEGIN va COMMIT",
        "Bank hisobidan mablag' yechish va ikkinchi hisobga qo'shishni atomar tranzaksiyada bajaring.",
        """CREATE TABLE bank_hisoblar_tx (
    hisob_id INT PRIMARY KEY,
    egasi VARCHAR(50),
    balans NUMERIC(15, 2) CHECK (balans >= 0)
);

INSERT INTO bank_hisoblar_tx VALUES (1, 'Ali', 1000000), (2, 'Vali', 200000);

BEGIN;
UPDATE bank_hisoblar_tx SET balans = balans - 300000 WHERE hisob_id = 1;
UPDATE bank_hisoblar_tx SET balans = balans + 300000 WHERE hisob_id = 2;
COMMIT;

SELECT * FROM bank_hisoblar_tx;""",
        "'BEGIN' (yoki START TRANSACTION) tranzaksiya blokini ochadi. Barcha UPDATE amallari bitta atomar paketga jamlanadi. 'COMMIT' buyrug'i kelgandagina barcha o'zgarishlar doimiy ravishda WAL jurnaliga va diskka yoziladi. Ungacha o'zgarishlar tashqi dunyoga ko'rinmaydi.",
        """CREATE TABLE
INSERT 0 2
BEGIN
UPDATE 1
UPDATE 1
COMMIT
 hisob_id | egasi |   balans   
----------+-------+------------
        1 | Ali   |  700000.00
        2 | Vali  |  500000.00
(2 rows)"""
    ),
    (
        752,
        "Tranzaksiyani bekor qilish: ROLLBACK",
        "Xatolik yuz berganda barcha kiritilgan o'zgarishlarni boshlang'ich holatiga qaytaring.",
        """BEGIN;
UPDATE bank_hisoblar_tx SET balans = balans - 500000 WHERE hisob_id = 1;
-- Kutilmagan xatolik yuz berdi yoki tekshiruvdan o'tmadi:
ROLLBACK;

SELECT * FROM bank_hisoblar_tx WHERE hisob_id = 1;""",
        "'ROLLBACK' tranzaksiya davomida qilingan barcha amallarni bekor qiladi. Baza hech narsa bo'lmagandek o'zining BEGIN dan oldingi sof holatiga qaytadi. Bu ACID ning Atomicity (bo'linmaslik) kafolatidir.",
        """BEGIN
UPDATE 1
ROLLBACK
 hisob_id | egasi |  balans   
----------+-------+-----------
        1 | Ali   | 700000.00
(1 row)"""
    ),
    (
        753,
        "Oraliq saqlash nuqtalari: SAVEPOINT va ROLLBACK TO SAVEPOINT",
        "Tranzaksiya ichida oraliq xatcho'p (checkpoint) qo'yib, faqat xatoli qismni bekor qiling.",
        """BEGIN;
UPDATE bank_hisoblar_tx SET balans = balans + 100000 WHERE hisob_id = 1;

SAVEPOINT qadam_1;

UPDATE bank_hisoblar_tx SET balans = balans + 50000 WHERE hisob_id = 2;
-- Ikkinchi harakat xato ekanligi ma'lum bo'ldi:
ROLLBACK TO SAVEPOINT qadam_1;

COMMIT;

SELECT * FROM bank_hisoblar_tx;""",
        "'SAVEPOINT' butun tranzaksiyani bekor qilmasdan, faqatgina ma'lum qadamgacha bo'lgan qismini orqaga qaytarish (partial rollback) imkonini beradi. Ali ga qo'shilgan 100k saqlanib qoladi, Vali ga qo'shilgan 50k esa bekor qilinadi.",
        """BEGIN
UPDATE 1
SAVEPOINT
UPDATE 1
ROLLBACK TO SAVEPOINT
COMMIT
 hisob_id | egasi |  balans   
----------+-------+-----------
        2 | Vali  | 500000.00
        1 | Ali   | 800000.00
(2 rows)"""
    ),
    (
        754,
        "Oraliq nuqtani xotiradan o'chirish: RELEASE SAVEPOINT",
        "Endi kerak bo'lmagan savepoint resursini bo'shatish.",
        """BEGIN;
SAVEPOINT mening_nuqtam;
-- Amallar...
RELEASE SAVEPOINT mening_nuqtam;
COMMIT;""",
        "'RELEASE SAVEPOINT' belgilangan nuqtani o'chiradi, lekin uning ichidagi o'zgarishlarni bekor qilmaydi. Tranzaksiya ichki xotirasi (Savepoint stack) tozalanadi.",
        """BEGIN
SAVEPOINT
RELEASE SAVEPOINT
COMMIT
Query returned successfully in 18 msec."""
    ),
    (
        755,
        "ACID: Atomicity (Bo'linmaslik) tamoyili",
        "CHECK cheklovi buzilganda butun tranzaksiya avtomatik to'liq to'xtashini ko'ring.",
        """BEGIN;
UPDATE bank_hisoblar_tx SET balans = balans + 200000 WHERE hisob_id = 2;
-- Ushbu UPDATE 'balans >= 0' cheklovini buzadi:
UPDATE bank_hisoblar_tx SET balans = balans - 2000000 WHERE hisob_id = 1;
COMMIT; -- PostgreSQL xato bo'lgan tranzaksiyani COMMIT qilishga yo'l qo'ymaydi!""",
        "Agar tranzaksiya ichida bitta bo'lsa ham xatolik yuz bersa, PostgreSQL butun tranzaksiyani 'ABORTED' holatiga o'tkazadi. Foydalanuvchi COMMIT yozsa ham baza uni avtomatik ROLLBACK qiladi. Birorta ham o'zgarish diskka o'tmaydi.",
        """BEGIN
UPDATE 1
ERROR:  new row for relation "bank_hisoblar_tx" violates check constraint "bank_hisoblar_tx_balans_check"
WARNING:  there is no transaction in progress
COMMIT"""
    ),
    (
        756,
        "ACID: Consistency (Muvofiqlik / Yaxlitlik)",
        "Barcha FOREIGN KEY va CHECK cheklovlarining tranzaksiya oxirida 100% bajarilishi shartligi.",
        """SELECT 'Consistency: Tranzaksiya bazani bir to‘g‘ri invariant holatdan ikkinchi to‘g‘ri invariant holatga o‘tkazadi' AS acid_c;""",
        "Bazada yozilgan qoidalar (masalan, summa manfiy bo'lmasligi, tashqi kalit mavjudligi) tranzaksiya yakunida mutlaq qanoatlantirilishi shart, aks holda tranzaksiya rad etiladi.",
        """                                                       acid_c                                                       
--------------------------------------------------------------------------------------------------------------------
 Consistency: Tranzaksiya bazani bir to‘g‘ri invariant holatdan ikkinchi to‘g‘ri invariant holatga o‘tkazadi
(1 row)"""
    ),
    (
        757,
        "ACID: Isolation (Izolyatsiya) va tranzaksiyalar to'qnashuvi",
        "Bir vaqtning o'zida ishlayotgan ikki mijoz bir-birining chala o'zgarishlarini ko'rmasligi kafolati.",
        """SELECT 'Isolation: Har bir tranzaksiya o‘zini bazada yakkaxon ishlayotgandek his qiladi' AS acid_i;""",
        "Izolyatsiya MVCC (Multi-Version Concurrency Control) va qulflar orqali ta'minlanadi.",
        """                                                acid_i                                                 
-------------------------------------------------------------------------------------------------------
 Isolation: Har bir tranzaksiya o‘zini bazada yakkaxon ishlayotgandek his qiladi
(1 row)"""
    ),
    (
        758,
        "ACID: Durability (Bardavomlik) va WAL mexanizmi",
        "Server to'satdan elektr tokidan uzilsa ham COMMIT bo'lgan ma'lumotlar saqlanib qolishi.",
        """SHOW wal_level;""",
        "Durability kafolati Write-Ahead Logging (WAL) orqali beriladi: o'zgarishlar asosiy ma'lumotlar bazasi fayliga yozilishidan oldin darhol diskdagi WAL jurnaliga ketma-ket yoziladi (fsync). Server o'chib yonsa, baza WAL orqali o'zini to'liq tiklab oladi (Crash Recovery).",
        """ wal_level 
-----------
 replica
(1 row)"""
    ),
    (
        759,
        "Standart izolyatsiya darajasi: READ COMMITTED",
        "PostgreSQL dagi standart izolyatsiya darajasini ko'rish va o'rnatish.",
        """SHOW default_transaction_isolation;

BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;
SELECT COUNT(*) FROM bank_hisoblar_tx;
COMMIT;""",
        "'READ COMMITTED' PostgreSQL dagi standart darajadir. Bu darajada so'rov faqatgina u boshlangan lahzagacha COMMIT bo'lgan ma'lumotlarni ko'radi. Boshqa sessiyalarning hali tasdiqlanmagan (uncommitted) o'zgarishlari ko'rinmaydi.",
        """ default_transaction_isolation 
-------------------------------
 read committed
(1 row)
BEGIN
 count 
-------
     2
(1 row)
COMMIT"""
    ),
    (
        760,
        "Iflos o'qish (Dirty Read) va nega PostgreSQL da u imkonsiz?",
        "Boshqa sessiyaning hali tasdiqlanmagan xom ma'lumotlarini o'qish anomaliyasi.",
        """SELECT 'PostgreSQL da READ UNCOMMITTED darajasi tanlansa ham, u avtomatik READ COMMITTED kabi ishlaydi. Shu sababli Postgresda Dirty Read umuman ro‘y bermaydi' AS dirty_read_info;""",
        "PostgreSQL ning MVCC arxitekturasi har doim qatorlarning COMMIT bo'lgan versiyalariga qaraydi. Shu bois PostgreSQL da hech qachon 'Iflos o'qish' (boshqa tranzaksiya bekor qilgan xom ma'lumotni o'qib olish) yuz bermaydi.",
        """                                                                 dirty_read_info                                                                 
-------------------------------------------------------------------------------------------------------------------------------------------------
 PostgreSQL da READ UNCOMMITTED darajasi tanlansa ham, u avtomatik READ COMMITTED kabi ishlaydi. Shu sababli Postgresda Dirty Read umuman ro‘y bermaydi
(1 row)"""
    ),
    (
        761,
        "Qaytarilmas o'qish anomaliyasi (Non-repeatable Read)",
        "READ COMMITTED darajasida bitta tranzaksiya ichida ikkita bir xil SELECT har xil natija qaytarishi.",
        """SELECT 'Bitta tranzaksiya ichida 1-SELECT: balans=100. Shu payt boshqa sessiya balansni 200 qilib COMMIT qildi. Tranzaksiya ichidagi 2-SELECT: balans=200 chiqadi. Bu Non-repeatable Read dir' AS tahlil;""",
        "READ COMMITTED har bir alohida SELECT uchun yangi Snapshot oladi. Shuning uchun oraliqda boshqa tranzaksiya o'zgarish kiritgan bo'lsa, qiymat o'zgarib qoladi.",
        """                                                                                     tahlil                                                                                      
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Bitta tranzaksiya ichida 1-SELECT: balans=100. Shu payt boshqa sessiya balansni 200 qilib COMMIT qildi. Tranzaksiya ichidagi 2-SELECT: balans=200 chiqadi. Bu Non-repeatable Read dir
(1 row)"""
    ),
    (
        762,
        "Qaytariluvchi o'qish: REPEATABLE READ darajasi",
        "Butun tranzaksiya davomida barcha so'rovlar faqat tranzaksiya boshlangan lahzadagi yagona snapshotni ko'rishi.",
        """BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT balans FROM bank_hisoblar_tx WHERE hisob_id = 1;
-- Boshqa sessiyalar nima o'zgartirsa ham biz uchun o'zgarmas qoladi!
SELECT balans FROM bank_hisoblar_tx WHERE hisob_id = 1;
COMMIT;""",
        "'REPEATABLE READ' darajasida tranzaksiya o'zining eng birinchi so'rovi boshlangan paytda bitta yaxlit Snapshot (oniy surat) oladi va tranzaksiya oxirigacha butun dunyoni ayni shu surat holatida ko'radi. Qaytarilmas o'qish (Non-repeatable Read) bartaraf etiladi.",
        """BEGIN
 balans   
----------
 800000.00
(1 row)
 balans   
----------
 800000.00
(1 row)
COMMIT"""
    ),
    (
        763,
        "Sharpasimon o'qish anomaliyasi (Phantom Read)",
        "Oraliqda boshqa sessiya yangi qator kiritganda qatorlar sonining o'zgarib qolishi.",
        """SELECT 'PostgreSQL da REPEATABLE READ darajasi nafaqat mavjud qatorlar o‘zgarishidan, balki Phantom Read (yangi qatorlar paydo bo‘lishi) dan ham to‘liq himoyalaydi' AS phantom_info;""",
        "SQL standartida REPEATABLE READ faqat mavjud qatorlarni himoyalaydi deyilgan, biroq PostgreSQL da MVCC snapshot butun jadvalni qamragani bois u sharpasimon qatorlarni (Phantom Reads) ham o'tkazmaydi.",
        """                                                                   phantom_info                                                                    
--------------------------------------------------------------------------------------------------------------------------------------------------
 PostgreSQL da REPEATABLE READ darajasi nafaqat mavjud qatorlar o‘zgarishidan, balki Phantom Read (yangi qatorlar paydo bo‘lishi) dan ham to‘liq himoyalaydi
(1 row)"""
    ),
    (
        764,
        "Eng yuqori izolyatsiya: SERIALIZABLE darajasi",
        "Tranzaksiyalarning parallel bajarilishi ularning ketma-ket (bittalab) bajarilishi bilan 100% teng natija berishi kafolati.",
        """BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT SUM(balans) FROM bank_hisoblar_tx;
COMMIT;""",
        "'SERIALIZABLE' darajasi SSI (Serializable Snapshot Isolation) texnologiyasidan foydalanadi. U qulflar qo'ymasdan xotirada tranzaksiyalar orasidagi bog'liqlik grafigini (rw-antidependencies) tekshiradi. Agar anomaliya xavfi sezilsa, tranzaksiyalardan birini 'could not serialize access' xatosi bilan to'xtatadi.",
        """BEGIN
     sum     
-------------
 1300000.00
(1 row)
COMMIT"""
    ),
    (
        765,
        "Serializatsiya buzilishi xatosini dasturda qayta urinish (Retry Pattern)",
        "SERIALIZABLE xatosi chiqqanda backend dasturining standart xatti-harakati.",
        """SELECT 'SERIALIZABLE ishlatilganda dastur doimo 40001 (serialization_failure) xatosini kutishi va avtomatik qayta urinishi (retry loop) shart' AS retry_qoida;""",
        "SERIALIZABLE optimistik xarakterga ega. To'qnashuv bo'lsa xato beradi, dasturchi uni tutib olib tranzaksiyani boshidan qayta ishga tushirishi lozim.",
        """                                                          retry_qoida                                                          
------------------------------------------------------------------------------------------------------------------------------
 SERIALIZABLE ishlatilganda dastur doimo 40001 (serialization_failure) xatosini kutishi va avtomatik qayta urinishi (retry loop) shart
(1 row)"""
    ),
    (
        766,
        "Pessimistik qulflash: SELECT FOR UPDATE",
        "Chipta yoki tovar sotib olinayotganda, boshqa hech kim unga teginmasligi uchun qatorni eksklyuziv qulflang.",
        """BEGIN;
SELECT * FROM bank_hisoblar_tx 
WHERE hisob_id = 1 
FOR UPDATE;

-- Boshqa sessiyalar ushbu hisob_id = 1 ni UPDATE qila olmay navbatda kutib turadi!
UPDATE bank_hisoblar_tx SET balans = balans - 50000 WHERE hisob_id = 1;
COMMIT;""",
        "'SELECT ... FOR UPDATE' tanlangan qatorlarga qat'iy qulf qo'yadi. Boshqa tranzaksiyalar ushbu qatorlarni UPDATE yoki DELETE qilmoqchi bo'lsa, joriy tranzaksiya COMMIT yoki ROLLBACK bo'lmaguncha kutishga majbur bo'ladi. Race condition (poyga holati) ning oldini oladi.",
        """BEGIN
 hisob_id | egasi |  balans   
----------+-------+-----------
        1 | Ali   | 800000.00
(1 row)
UPDATE 1
COMMIT"""
    ),
    (
        767,
        "Kutmasdan darhol xato berish: SELECT FOR UPDATE NOWAIT",
        "Agar qator boshqa birov tomonidan band qilingan bo'lsa, kutib o'tirmasdan darhol xabar bering.",
        """BEGIN;
SELECT * FROM bank_hisoblar_tx 
WHERE hisob_id = 1 
FOR UPDATE NOWAIT;
COMMIT;""",
        "'NOWAIT' qo'shilsa, agar qator boshqa tranzaksiya tomonidan qulflangan bo'lsa, server mijozni kuttirib o'tirmaydi, o'sha zahotiyoq 'could not obtain lock on row' xatoligini qaytaradi.",
        """BEGIN
 hisob_id | egasi |  balans   
----------+-------+-----------
        1 | Ali   | 750000.00
(1 row)
COMMIT"""
    ),
    (
        768,
        "Navbat tizimlari uchun mo'jiza: SKIP LOCKED",
        "Ko'p oqimli xabarlar navbatida (Task Queue) bir vaqtda ishlovchi workerlar bir-birini kutmasdan bo'sh vazifani olishi.",
        """CREATE TABLE vazifalar_navbati (
    id SERIAL PRIMARY KEY,
    vazifa_nomi TEXT,
    holat VARCHAR(20) DEFAULT 'kutilmoqda'
);

INSERT INTO vazifalar_navbati (vazifa_nomi) VALUES ('SMS jo‘natish'), ('Email jo‘natish');

BEGIN;
-- Birinchi bo'sh vazifani band qilamiz:
SELECT * FROM vazifalar_navbati 
WHERE holat = 'kutilmoqda' 
ORDER BY id ASC 
LIMIT 1 
FOR UPDATE SKIP LOCKED;

UPDATE vazifalar_navbati SET holat = 'bajarilmoqda' WHERE id = 1;
COMMIT;""",
        "'SKIP LOCKED' boshqa workerlar tomonidan qulflangan qatorlarni jimgina tashlab o'tib, navbatdagi bo'sh qatorni oladi. Bu PostgreSQL ni RabbitMQ yoki Kafka kabi o'ta tezkor xabarlar navbati (Message Broker) sifatida ishlatish imkonini beradi.",
        """CREATE TABLE
INSERT 0 2
BEGIN
 id | vazifa_nomi  |    holat    
----+--------------+------------
  1 | SMS jo‘natish| kutilmoqda
(1 row)
UPDATE 1
COMMIT"""
    ),
    (
        769,
        "O'qish uchun birgalikda qulflash: SELECT FOR SHARE",
        "Qatorni boshqalar o'qishi mumkin bo'lgan, lekin hech kim o'zgartira olmaydigan qulflash darajasi.",
        """BEGIN;
SELECT * FROM bank_hisoblar_tx 
WHERE hisob_id = 1 
FOR SHARE;
COMMIT;""",
        "'FOR SHARE' bir nechta sessiyalarning parallel qulflashiga ruxsat beradi, biroq hech biriga UPDATE yoki DELETE qilishga yo'l qo'ymaydi.",
        """BEGIN
 hisob_id | egasi |  balans   
----------+-------+-----------
        1 | Ali   | 750000.00
(1 row)
COMMIT"""
    ),
    (
        770,
        "Faqat kalit bo'lmagan ustunlarni qulflash: FOR NO KEY UPDATE",
        "Birlamchi kalitga tegmasdan faqat oddiy ustunlarni yangilashda FOREIGN KEY larni bloklamaslik.",
        """BEGIN;
SELECT * FROM bank_hisoblar_tx 
WHERE hisob_id = 1 
FOR NO KEY UPDATE;
COMMIT;""",
        "PostgreSQL 9.3+ da kiritilgan bu daraja boshqa jadvallardagi ushbu qatorga havola qiluvchi INSERT amallarini bloklamaydi.",
        """BEGIN
 hisob_id | egasi |  balans   
----------+-------+-----------
        1 | Ali   | 750000.00
(1 row)
COMMIT"""
    ),
    (
        771,
        "O'lik qulflanish (Deadlock) qanday sodir bo'ladi?",
        "Ikki tranzaksiyaning bir-birining resurslarini kutib qotib qolishi ssenariysi.",
        """SELECT 'Deadlock: 1-sessiya A ni qulflab B ni kutadi. 2-sessiya B ni qulflab A ni kutadi. Hech biri davom etolmaydi' AS deadlock_sababi;""",
        "Deadlock sodir bo'lganda PostgreSQL ichki 'deadlock_timeout' taymeridan so'ng (odatda 1 soniya) vaziyatni aniqlaydi va birinchi tranzaksiyani bekor qilib (abort) ikkinchisiga yo'l ochadi.",
        """                                                deadlock_sababi                                                 
----------------------------------------------------------------------------------------------------------------
 Deadlock: 1-sessiya A ni qulflab B ni kutadi. 2-sessiya B ni qulflab A ni kutadi. Hech biri davom etolmaydi
(1 row)"""
    ),
    (
        772,
        "Deadlockning oldini olish: Qat'iy tartibda qulflash (Lock Ordering)",
        "Barcha tranzaksiyalarda hisob raqamlarini doimo ID o'sish tartibida qulflash qoidasi.",
        """-- Doimo kichik ID dan katta ID ga qarab qulflanadi:
BEGIN;
SELECT * FROM bank_hisoblar_tx 
WHERE hisob_id IN (1, 2) 
ORDER BY hisob_id ASC 
FOR UPDATE;

-- Pul o'tkazish amali...
COMMIT;""",
        "Agar barcha dasturchilar resurslarni bir xil qat'iy tartibda (masalan, `WHERE id IN (1, 2) ORDER BY id`) qulflasa, deadlock 100% matematik jihatdan imkonsiz bo'lib qoladi!",
        """BEGIN
 hisob_id | egasi |  balans   
----------+-------+-----------
        1 | Ali   | 750000.00
        2 | Vali  | 500000.00
(2 rows)
COMMIT"""
    ),
    (
        773,
        "Dasturiy qulflar: Advisory Locks (Maslahat qulflari)",
        "Jadvallarga tegmasdan xotirada 64-bitli butun son bo'yicha global qulf olish.",
        """-- 12345 sonli biznes jarayonni qulflash:
SELECT pg_advisory_lock(12345);

-- Muhim bir martalik ish bajariladi...

-- Qulfni bo'shatish:
SELECT pg_advisory_unlock(12345);""",
        "'Advisory Lock' Relyatsion jadval qatorlariga bog'liq bo'lmagan, faqatgina dasturchi ixtiyoriga berilgan xotira qulfidir. Crontab skriptlari bir vaqtda ikki marta ishga tushib ketmasligini ta'minlashda juda qulay.",
        """ pg_advisory_lock 
------------------
 
(1 row)
 pg_advisory_unlock 
--------------------
 t
(1 row)"""
    ),
    (
        774,
        "Tranzaksiyaga bog'liq maslahat qulfi: pg_advisory_xact_lock",
        "COMMIT yoki ROLLBACK bo'lganda o'z-o'zidan avtomatik yechiladigan qulf.",
        """BEGIN;
SELECT pg_advisory_xact_lock(99999);
-- Qulf COMMIT paytida avtomatik ochiladi, unlock qilish shart emas!
COMMIT;""",
        "'pg_advisory_xact_lock' tranzaksiya tugashi bilan o'z-o'zidan yechiladi, dasturchi unlock qilishni unutib qo'ysa ham xavf tug'dirmaydi.",
        """BEGIN
 pg_advisory_xact_lock 
-----------------------
 
(1 row)
COMMIT"""
    ),
    (
        775,
        "Jadval darajasidagi qulflar: LOCK TABLE",
        "Jadval sxemasi o'zgarayotganda yoki ommaviy yuklashda butun jadvalni qulflash.",
        """BEGIN;
LOCK TABLE bank_hisoblar_tx IN SHARE ROW EXCLUSIVE MODE;
-- Ma'lumotlar bilan xavfsiz ishlash...
COMMIT;""",
        "Jadval darajasidagi qulflar DDL amallarida va ommaviy sinxronizatsiyada parallel o'zgarishlarni to'xtatib turish uchun xizmat qiladi.",
        """BEGIN
LOCK TABLE
COMMIT
Query returned successfully in 21 msec."""
    ),
    (
        776,
        "Faol qulflarni tizim katalogidan ko'rish: pg_locks",
        "Ayni damda qaysi tranzaksiyalar qaysi resurslarni qulflab turganini aniqlash.",
        """SELECT 
    pid, 
    locktype, 
    mode, 
    granted 
FROM pg_locks 
WHERE pid = pg_backend_pid();""",
        "'pg_locks' serverdagi barcha olingan va kutilayotgan qulflarni real vaqt rejimida ko'rsatadi.",
        """  pid  | locktype |      mode       | granted 
-------+----------+-----------------+---------
 12345 | relation | AccessShareLock | t
 12345 | virtualxid| ExclusiveLock   | t
(2 rows)"""
    ),
    (
        777,
        "Kutayotgan (Bloklangan) so'rovlarni aniqlash",
        "Kim kimni kutayotganligini ko'rsatuvchi diagnostic so'rov.",
        """SELECT 
    blocked_locks.pid AS bloklangan_pid,
    blocking_locks.pid AS bloklayotgan_pid
FROM pg_catalog.pg_locks blocked_locks
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
WHERE NOT blocked_locks.granted;""",
        "Ushbu so'rov orqali tizim administratori qaysi foydalanuvchi butun tizimni to'xtatib qo'yganini darhol aniqlaydi.",
        """ bloklangan_pid | bloklayotgan_pid 
----------------+------------------
(0 rows)"""
    ),
    (
        778,
        "Bloklagan sessiyani majburiy to'xtatish: pg_terminate_backend",
        "Baza qulflanib qolishiga sababchi bo'lgan sessiyani uzib tashlash.",
        """-- SELECT pg_terminate_backend(bloklayotgan_pid);
SELECT 'pg_terminate_backend(pid) qotib qolgan sessiyani favqulodda to‘xtatib qulflarni bo‘shatadi' AS maslahat;""",
        "DBA ning favqulodda quroli: zombi yoki uzoq qolib ketgan tranzaksiyani serverdan uzadi.",
        """                                                   maslahat                                                   
--------------------------------------------------------------------------------------------------------------
 pg_terminate_backend(pid) qotib qolgan sessiyani favqulodda to‘xtatib qulflarni bo‘shatadi
(1 row)"""
    ),
    (
        779,
        "Tranzaksiya taymerlari: statement_timeout",
        "So'rov 5 soniyadan ko'p vaqt olsa tranzaksiyani avtomatik to'xtatish.",
        """SET statement_timeout = 5000; -- 5000 ms (5 soniya)""",
        "So'rovlar uzoq vaqt resurslarni band qilib turmasligi uchun chegaralar belgilash.",
        """SET
Query returned successfully in 16 msec."""
    ),
    (
        780,
        "Bo'sh turgan tranzaksiya taymeri: idle_in_transaction_session_timeout",
        "BEGIN qilib qo'yib unutib qoldirilgan xavfli sessiyalarni avtomatik o'chirish.",
        """SET idle_in_transaction_session_timeout = 10000; -- 10 soniya""",
        "Dastur tranzaksiya ochib qo'yib qulflarni ushlab tursa, ushbu taymer uni 10 soniyadan so'ng avtomatik uzadi va qulflar bo'shatiladi.",
        """SET
Query returned successfully in 15 msec."""
    ),
    (
        781,
        "Faqat o'qish uchun tranzaksiya: READ ONLY",
        "Bazada hech narsani o'zgartira olmaydigan xavfsiz tranzaksiya ochish.",
        """BEGIN READ ONLY;
SELECT * FROM bank_hisoblar_tx;
-- INSERT INTO bank_hisoblar_tx VALUES (9, 'Xato', 0); -- Bu xatolik beradi!
COMMIT;""",
        "'READ ONLY' tranzaksiyasi ichida har qanday yozish amali taqiqlanadi. Bu zaxira nusxa olishda (Backup) va hisobotlarda ma'lumotlarning tasodifiy o'zgarishidan asraydi.",
        """BEGIN
 hisob_id | egasi |  balans   
----------+-------+-----------
        2 | Vali  | 500000.00
        1 | Ali   | 750000.00
(2 rows)
COMMIT"""
    ),
    (
        782,
        "Qator versiyalari (MVCC Tuple versions) va xmin/xmax",
        "Tranzaksiya o'zgarganda qatorning qanday yangi versiyasi hosil bo'lishini ko'ring.",
        """SELECT ctid, xmin, xmax, hisob_id, balans 
FROM bank_hisoblar_tx;""",
        "PostgreSQL MVCC tizimida UPDATE eski qatorni o'chirmaydi, balki uning xmax ustuniga tranzaksiya ID sini yozib, yangi xmin bilan yangi qator yaratadi.",
        """ ctid  | xmin | xmax | hisob_id |  balans   
-------+------+------+----------+-----------
 (0,4) | 1250 |    0 |        2 | 500000.00
 (0,7) | 1255 |    0 |        1 | 750000.00
(2 rows)"""
    ),
    (
        783,
        "Optimistik qulflash (Optimistic Locking) va Versiya ustuni",
        "Baza qulflarisiz qator versiyasi (version int) orqali to'qnashuvni dasturda aniqlash.",
        """ALTER TABLE bank_hisoblar_tx ADD COLUMN versiya INT DEFAULT 1;

-- Optimistik yangilash:
UPDATE bank_hisoblar_tx 
SET balans = balans - 10000, versiya = versiya + 1 
WHERE hisob_id = 1 AND versiya = 1;""",
        "Agar ikki foydalanuvchi bir vaqtda kelsa, birinchisi versiyani 2 ga oshiradi, ikkinchisining WHERE versiya=1 sharti bajarilmaydi (UPDATE 0 bo'ladi). Hech qanday qulflarsiz xavfsizlik ta'minlanadi.",
        """ALTER TABLE
UPDATE 1
Query returned successfully in 34 msec."""
    ),
    (
        784,
        "Tranzaksiya snapshotini eksport qilish: pg_export_snapshot()",
        "Bir nechta parallel sessiyalarga aynan bir xil ma'lumotlar holatini ulashish.",
        """BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT pg_export_snapshot() AS snapshot_id;
COMMIT;""",
        "'pg_export_snapshot()' pg_dump vositasiga parallel bir nechta ishchilar orqali aynan bir xil vaqt kesimidagi zaxira nusxasini olishga imkon beradi.",
        """BEGIN
 snapshot_id 
-------------
 00000003-00000010-1
(1 row)
COMMIT"""
    ),
    (
        785,
        "Ikki bosqichli tasdiqlash: Two-Phase Commit (PREPARE TRANSACTION)",
        "Taqsimlangan tizimlarda (Distributed Transactions) bir nechta serverlar aro tranzaksiyani tayyorlash.",
        """BEGIN;
UPDATE bank_hisoblar_tx SET balans = balans + 500 WHERE hisob_id = 1;
PREPARE TRANSACTION 'tranzaksiya_kod_99';

-- Boshqa serverlar ham tayyor bo'lgach:
COMMIT PREPARED 'tranzaksiya_kod_99';""",
        "'PREPARE TRANSACTION' tarmoq uzilib qolishi mumkin bo'lgan taqsimlangan bazalarda 2PC (Two-Phase Commit) protokolini ta'minlaydi. O'zgarishlar sessiya yopilsa ham diskda tayyor holatda saqlanadi.",
        """BEGIN
UPDATE 1
PREPARE TRANSACTION
COMMIT PREPARED
Query returned successfully in 41 msec."""
    ),
    (
        786,
        "Tayyorlangan tranzaksiyani bekor qilish: ROLLBACK PREPARED",
        "Tayyorlab qo'yilgan taqsimlangan tranzaksiyani bekor qilish.",
        """BEGIN;
UPDATE bank_hisoblar_tx SET balans = balans + 10 WHERE hisob_id = 1;
PREPARE TRANSACTION 'bekor_boluvchi_tx';

ROLLBACK PREPARED 'bekor_boluvchi_tx';""",
        "Agar boshqa mikroxizmatlardan biri xato qaytarsa, barcha tugunlardagi tayyorlangan tranzaksiyalar 'ROLLBACK PREPARED' orqali bekor qilinadi.",
        """BEGIN
UPDATE 1
PREPARE TRANSACTION
ROLLBACK PREPARED
Query returned successfully in 35 msec."""
    ),
    (
        787,
        "Auto-commit xususiyati va dasturlash tillari",
        "Dasturlash drayverlarida har bir so'rov avtomatik tranzaksiya ichida bo'lishi.",
        """SELECT 'Dasturchilar ko‘pincha drayverlarda Auto-Commit yoqilganini unutishadi, bu millionlab mayda tranzaksiyalar hosil qilib serverni charchatadi' AS tahlil;""",
        "Ommaviy kiritishda doimo eksplitsit `BEGIN ... COMMIT` qo'yish kerak, aks holda har bir INSERT alohida tranzaksiya bo'lib diskka fsync talab qiladi.",
        """                                                          tahlil                                                           
---------------------------------------------------------------------------------------------------------------------------
 Dasturchilar ko‘pincha drayverlarda Auto-Commit yoqilganini unutishadi, bu millionlab mayda tranzaksiyalar hosil qilib serverni charchatadi
(1 row)"""
    ),
    (
        788,
        "Tranzaksiyada DDL buyruqlarining xavfsizligi (Transactional DDL)",
        "PostgreSQL da CREATE TABLE yoki ALTER TABLE amallarini ROLLBACK qilish imkoniyati.",
        """BEGIN;
CREATE TABLE sinov_ochadigan_jadval (id INT);
ALTER TABLE bank_hisoblar_tx ADD COLUMN sinov_ustun INT;
-- Fikrimizdan qaytdik:
ROLLBACK;

SELECT 'PostgreSQL da hattoki jadvallar yaratish va o‘chirish ham ROLLBACK bo‘ladi (MySQL va Oracle da bu yo‘q!)' AS postgres_ustunligi;""",
        "PostgreSQL ning eng mashhur ustunliklaridan biri: barcha DDL (CREATE, ALTER, DROP) operatsiyalari tranzaksiyaviydir. Migratsiya sinib qolsa, butun sxema o'zgarishlari to'liq orqaga qaytadi.",
        """BEGIN
CREATE TABLE
ALTER TABLE
ROLLBACK
                                                 postgres_ustunligi                                                  
---------------------------------------------------------------------------------------------------------------------
 PostgreSQL da hattoki jadvallar yaratish va o‘chirish ham ROLLBACK bo‘ladi (MySQL va Oracle da bu yo‘q!)
(1 row)"""
    ),
    (
        789,
        "Tranzaksiyada ketma-ketliklarning (Sequence) izolyatsiyalanmasligi",
        "Nega ROLLBACK bo'lsa ham avto-inkrement ID lar orqaga qaytmasligini ko'ring.",
        """CREATE TABLE seq_test (id SERIAL PRIMARY KEY, n TEXT);

BEGIN;
INSERT INTO seq_test (n) VALUES ('Test 1');
ROLLBACK;

INSERT INTO seq_test (n) VALUES ('Test 2');
SELECT * FROM seq_test;""",
        "Sequence (ketma-ketlik) lar boshqa tranzaksiyalarni bloklamaslik uchun asosiy tranzaksiya doirasidan tashqarida ishlaydi. Shu bois ROLLBACK bo'lsa ID yo'qotiladi (gap hosil bo'ladi, 1 o'rniga 2 chiqadi).",
        """CREATE TABLE
BEGIN
INSERT 0 1
ROLLBACK
INSERT 0 1
 id |   n    
----+--------
  2 | Test 2
(1 row)"""
    ),
    (
        790,
        "PostgreSQL da Synchronous Commit sozlamasi",
        "Maksimal tezlik uchun xavfsizlikni ozgina qurbon qilish (Asinxron commit).",
        """SHOW synchronous_commit;""",
        "'synchronous_commit = off' qilinsa, COMMIT buyrug'i WAL diskka jismonan yozilishini kutmasdan darhol javob beradi. Bu yozish tezligini 10 barobarga oshiradi, lekin server tokdan uzilsa so'nggi 200 ms ma'lumot yo'qolishi mumkin.",
        """ synchronous_commit 
--------------------
 on
(1 row)"""
    ),
    (
        791,
        "Write Skew anomaliyasi (SERIALIZABLE darajasi talab qilinishi)",
        "Ikki shifokordan kamida biri navbatchilikda qolishi kerak bo'lganda bir vaqtda ikkalasi ham ta'tilga chiqib ketishi holati.",
        """SELECT 'Write Skew: REPEATABLE READ da ikki tranzaksiya o‘zaro bir-birining qatorlarini o‘zgartirmasdan umumiy qoidani buzishi mumkin. Buni faqat SERIALIZABLE to‘xtatadi' AS write_skew;""",
        "SERIALIZABLE darajasi SSI grafigi orqali bunday mantiqiy chalkashliklarni darhol ushlaydi.",
        """                                                                      write_skew                                                                      
------------------------------------------------------------------------------------------------------------------------------------------------------
 Write Skew: REPEATABLE READ da ikki tranzaksiya o‘zaro bir-birining qatorlarini o‘zgartirmasdan umumiy qoidani buzishi mumkin. Buni faqat SERIALIZABLE to‘xtatadi
(1 row)"""
    ),
    (
        792,
        "Tranzaksiyada vaqtning muzlab turishi (Transaction Timestamp)",
        "Tranzaksiya ichida NOW() necha marta chaqirilsa ham aynan bir xil vaqtni berishi.",
        """BEGIN;
SELECT NOW() AS t1;
-- 1 soniya kutgandan so'ng ham:
SELECT NOW() AS t2;
COMMIT;""",
        "'NOW()' tranzaksiya boshlangan lahzada bir marta o'rnatiladi va tranzaksiya tugaguncha muzlab turadi.",
        """BEGIN
              t1               
-------------------------------
 2026-11-08 12:00:00.123456+05
(1 row)
              t2               
-------------------------------
 2026-11-08 12:00:00.123456+05
(1 row)
COMMIT"""
    ),
    (
        793,
        "Uzoq yashovchi tranzaksiyalar (Long-running transactions) xavfi",
        "Nega uzoq ochiq qolgan tranzaksiya butun bazada Autovacuum ishini to'xtatib qo'yishini ko'rsating.",
        """SELECT 'Uzoq yashovchi ochiq tranzaksiya o‘zidan keyingi eski qatorlarning tozalanishini (VACUUM) bloklaydi va butun baza shishib (bloat) ketadi' AS xavf;""",
        "Baza xmin chegarasi eng eski ochiq tranzaksiya bilan bog'lanib qoladi va undan keyingi o'chirilgan qatorlarni hech kim tozalay olmaydi.",
        """                                                               xavf                                                                
-----------------------------------------------------------------------------------------------------------------------------------
 Uzoq yashovchi ochiq tranzaksiya o‘zidan keyingi eski qatorlarning tozalanishini (VACUUM) bloklaydi va butun baza shishib (bloat) ketadi
(1 row)"""
    ),
    (
        794,
        "Tranzaksiya identifikatori: txid_current()",
        "Joriy tranzaksiya 64-bitli ID raqamini aniqlash.",
        """BEGIN;
SELECT pg_current_xact_id() AS joriy_tranzaksiya_id;
COMMIT;""",
        "'pg_current_xact_id()' PostgreSQL dagi unikal tranzaksiya hisoblagichini ko'rsatadi.",
        """BEGIN
 joriy_tranzaksiya_id 
----------------------
                 1260
(1 row)
COMMIT"""
    ),
    (
        795,
        "Faqat o'qish rejimida tranzaksiya izolyatsiyasini sozlash",
        "SET TRANSACTION buyrug'i bilan tranzaksiya boshida xususiyatlarni belgilash.",
        """BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY;
SELECT COUNT(*) FROM bank_hisoblar_tx;
COMMIT;""",
        "Sozlamalar BEGIN dan so'ng darhol 'SET TRANSACTION' orqali kiritilishi mumkin.",
        """BEGIN
SET TRANSACTION
 count 
-------
     2
(1 row)
COMMIT"""
    ),
    (
        796,
        "Shartli FOR UPDATE: Faqat ma'lum jadvallarni qulflash",
        "JOIN qilingan so'rovda faqat bitta jadval qatorlarini qulflash.",
        """BEGIN;
SELECT * FROM bank_hisoblar_tx h
JOIN vazifalar_navbati v ON h.hisob_id = v.id
FOR UPDATE OF h; -- Faqat bank_hisoblar_tx qulflanadi, vazifalar_navbati qulflanmaydi!
COMMIT;""",
        "'FOR UPDATE OF jadval_taxallusi' qulflashni faqat kerakli jadval bilan cheklaydi.",
        """BEGIN
 hisob_id | egasi |  balans   | versiya | id | vazifa_nomi  |    holat     
----------+-------+-----------+---------+----+--------------+--------------
        1 | Ali   | 740000.00 |       2 |  1 | SMS jo‘natish| bajarilmoqda
(1 row)
COMMIT"""
    ),
    (
        797,
        "Eksklyuziv bo'lmagan tranzaksiya jurnali tekshiruvi: pg_stat_activity",
        "Ayni damda bazada nechta ochiq tranzaksiya borligini monitoring qilish.",
        """SELECT pid, usename, state, query_start, query 
FROM pg_stat_activity 
WHERE state = 'idle in transaction';""",
        "Ochiq qolib ketgan tranzaksiyalarni aniqlashning eng tezkor ma'muriy so'rovi.",
        """ pid | usename | state | query_start | query 
-----+---------+-------+-------------+-------
(0 rows)"""
    ),
    (
        798,
        "Dastur darajasidagi Idempotentlik (Idempotency Key)",
        "Tarmoq uzilib qayta so'rov kelganda pul ikki marta yechilmasligi uchun tranzaksiyada idempotent kalit tekshirish.",
        """CREATE TABLE tolov_idempotent (
    kalit UUID PRIMARY KEY,
    summa NUMERIC,
    bajarilgan_vaqt TIMESTAMPTZ DEFAULT NOW()
);

BEGIN;
INSERT INTO tolov_idempotent (kalit, summa)
VALUES ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 150000)
ON CONFLICT (kalit) DO NOTHING;
COMMIT;""",
        "Idempotentlik kafolati: agar so'rov qayta jo'natilsa ham, PRIMARY KEY to'qnashuvi tufayli ikkinchi to'lov amalga oshmaydi.",
        """CREATE TABLE
BEGIN
INSERT 0 1
COMMIT
Query returned successfully in 31 msec."""
    ),
    (
        799,
        "Deadlock xavfini kamaytiruvchi SELECT FOR UPDATE SKIP LOCKED unumdorligi",
        "Bir vaqtda 100 ta oqim ishlasa ham to'qnashuvsiz vazifa taqsimoti.",
        """SELECT 'SKIP LOCKED resurslar ustida hech qachon navbat yoki deadlock hosil qilmaydi, har bir ishchi darhol o‘z ishini oladi' AS afzallik;""",
        "Yuqori yuklamali FinTech mikroservislarida backend navbatlari uchun eng mukammal yechim.",
        """                                                        afzallik                                                         
-------------------------------------------------------------------------------------------------------------------------
 SKIP LOCKED resurslar ustida hech qachon navbat yoki deadlock hosil qilmaydi, har bir ishchi darhol o‘z ishini oladi
(1 row)"""
    ),
    (
        800,
        "Korporativ Tranzaksiya: FinTech To'lov Tizimi va Ikki Bosqichli Buxgalteriya Balansi",
        "Bank hisoblari o'rtasida pul o'tkazish, jo'natuvchi va qabul qiluvchi qatorlarini qat'iy tartibda qulflash (Pessimistic Locking / Deadlock Prevention), balans yetarliligini tekshirish, komissiya hisoblash, audit jurnalini yuritish va bularning barchasini to'liq ACID xususiyatlari bilan kafolatlovchi korporativ tranzaksiya skriptini yozing.",
        """CREATE TABLE fin_hisoblar (
    hisob_raqam VARCHAR(20) PRIMARY KEY,
    egasi VARCHAR(100) NOT NULL,
    balans NUMERIC(15, 2) NOT NULL CHECK (balans >= 0)
);

CREATE TABLE fin_audit_jurnal (
    operatsiya_id BIGSERIAL PRIMARY KEY,
    kimdan VARCHAR(20) NOT NULL,
    kimgadir VARCHAR(20) NOT NULL,
    otkazma_summasi NUMERIC(15, 2) NOT NULL,
    komissiya NUMERIC(15, 2) NOT NULL,
    sana TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO fin_hisoblar VALUES 
('ACC_001', 'Sherzod Toshmatov', 5000000.00),
('ACC_002', 'Nodira Salimova',   1000000.00);

BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- 1. Deadlock ning oldini olish uchun hisoblar qat'iy alifbo tartibida qulflanadi:
SELECT hisob_raqam, balans 
FROM fin_hisoblar 
WHERE hisob_raqam IN ('ACC_001', 'ACC_002') 
ORDER BY hisob_raqam ASC 
FOR UPDATE;

-- 2. Oraliq nuqta (Savepoint):
SAVEPOINT otkazma_boshi;

-- 3. Jo'natuvchidan pul va 1% komissiya yechish (Jami: 1,000,000 + 10,000 = 1,010,000):
UPDATE fin_hisoblar 
SET balans = balans - (1000000.00 + 10000.00)
WHERE hisob_raqam = 'ACC_001' AND balans >= (1000000.00 + 10000.00);

-- 4. Qabul qiluvchiga to'liq summani qo'shish:
UPDATE fin_hisoblar 
SET balans = balans + 1000000.00 
WHERE hisob_raqam = 'ACC_002';

-- 5. Audit jurnaliga o'chmas iz qoldirish:
INSERT INTO fin_audit_jurnal (kimdan, kimgadir, otkazma_summasi, komissiya)
VALUES ('ACC_001', 'ACC_002', 1000000.00, 10000.00);

-- 6. Butun operatsiyani yaxlit tasdiqlash:
COMMIT;

-- Natijalarni ko'rish:
SELECT * FROM fin_hisoblar;
SELECT * FROM fin_audit_jurnal;""",
        "Ushbu korporativ skript xalqaro FinTech standartlariga (PCI-DSS, Core Banking System) to'liq mos keladi: hisoblar alifbo bo'yicha saralanib qulflangani uchun Deadlock xavfi nolga teng, CHECK cheklovi balansning manfiyga tushishidan asraydi, SAVEPOINT xatolik yuz berganda xavfsiz chekinishni beradi va audit yozuvi bilan barcha o'zgarishlar bitta atomar COMMIT da diskdagi WAL ga abadiy muhrlanadi.",
        """CREATE TABLE
CREATE TABLE
INSERT 0 2
BEGIN
 hisob_raqam |   balans   
-------------+------------
 ACC_001     | 5000000.00
 ACC_002     | 1000000.00
(2 rows)
SAVEPOINT
UPDATE 1
UPDATE 1
INSERT 0 1
COMMIT
 hisob_raqam |       egasi       |   balans   
-------------+-------------------+------------
 ACC_001     | Sherzod Toshmatov | 3990000.00
 ACC_002     | Nodira Salimova   | 2000000.00
(2 rows)
 operatsiya_id | kimdan  | kimgadir | otkazma_summasi | komissiya |             sana              
---------------+---------+----------+-----------------+-----------+-------------------------------
             1 | ACC_001 | ACC_002  |      1000000.00 |  10000.00 | 2026-11-08 12:00:00.654321+05
(1 row)"""
    )
]

formatted = [format_task(*item) for item in tx_data]
save_file("sql_16_tranzaksiyalar_va_acid_xususiyatlari.md", formatted)
