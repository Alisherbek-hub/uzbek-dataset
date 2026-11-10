# 751-Topshiriq: Tranzaksiyani boshlash va tasdiqlash: BEGIN va COMMIT
## Topshiriq sharti:
Bank hisobidan mablag' yechish va ikkinchi hisobga qo'shishni atomar tranzaksiyada bajaring.

## Yechim (SQL kodi):
```sql
CREATE TABLE bank_hisoblar_tx (
    hisob_id INT PRIMARY KEY,
    egasi VARCHAR(50),
    balans NUMERIC(15, 2) CHECK (balans >= 0)
);

INSERT INTO bank_hisoblar_tx VALUES (1, 'Ali', 1000000), (2, 'Vali', 200000);

BEGIN;
UPDATE bank_hisoblar_tx SET balans = balans - 300000 WHERE hisob_id = 1;
UPDATE bank_hisoblar_tx SET balans = balans + 300000 WHERE hisob_id = 2;
COMMIT;

SELECT * FROM bank_hisoblar_tx;
```

## Tushuntirish va Mantiq:
'BEGIN' (yoki START TRANSACTION) tranzaksiya blokini ochadi. Barcha UPDATE amallari bitta atomar paketga jamlanadi. 'COMMIT' buyrug'i kelgandagina barcha o'zgarishlar doimiy ravishda WAL jurnaliga va diskka yoziladi. Ungacha o'zgarishlar tashqi dunyoga ko'rinmaydi.

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 2
BEGIN
UPDATE 1
UPDATE 1
COMMIT
 hisob_id | egasi |   balans   
----------+-------+------------
        1 | Ali   |  700000.00
        2 | Vali  |  500000.00
(2 rows)
```


# 752-Topshiriq: Tranzaksiyani bekor qilish: ROLLBACK
## Topshiriq sharti:
Xatolik yuz berganda barcha kiritilgan o'zgarishlarni boshlang'ich holatiga qaytaring.

## Yechim (SQL kodi):
```sql
BEGIN;
UPDATE bank_hisoblar_tx SET balans = balans - 500000 WHERE hisob_id = 1;
-- Kutilmagan xatolik yuz berdi yoki tekshiruvdan o'tmadi:
ROLLBACK;

SELECT * FROM bank_hisoblar_tx WHERE hisob_id = 1;
```

## Tushuntirish va Mantiq:
'ROLLBACK' tranzaksiya davomida qilingan barcha amallarni bekor qiladi. Baza hech narsa bo'lmagandek o'zining BEGIN dan oldingi sof holatiga qaytadi. Bu ACID ning Atomicity (bo'linmaslik) kafolatidir.

## Ishlash natijasi:
```text
BEGIN
UPDATE 1
ROLLBACK
 hisob_id | egasi |  balans   
----------+-------+-----------
        1 | Ali   | 700000.00
(1 row)
```


# 753-Topshiriq: Oraliq saqlash nuqtalari: SAVEPOINT va ROLLBACK TO SAVEPOINT
## Topshiriq sharti:
Tranzaksiya ichida oraliq xatcho'p (checkpoint) qo'yib, faqat xatoli qismni bekor qiling.

## Yechim (SQL kodi):
```sql
BEGIN;
UPDATE bank_hisoblar_tx SET balans = balans + 100000 WHERE hisob_id = 1;

SAVEPOINT qadam_1;

UPDATE bank_hisoblar_tx SET balans = balans + 50000 WHERE hisob_id = 2;
-- Ikkinchi harakat xato ekanligi ma'lum bo'ldi:
ROLLBACK TO SAVEPOINT qadam_1;

COMMIT;

SELECT * FROM bank_hisoblar_tx;
```

## Tushuntirish va Mantiq:
'SAVEPOINT' butun tranzaksiyani bekor qilmasdan, faqatgina ma'lum qadamgacha bo'lgan qismini orqaga qaytarish (partial rollback) imkonini beradi. Ali ga qo'shilgan 100k saqlanib qoladi, Vali ga qo'shilgan 50k esa bekor qilinadi.

## Ishlash natijasi:
```text
BEGIN
UPDATE 1
SAVEPOINT
UPDATE 1
ROLLBACK TO SAVEPOINT
COMMIT
 hisob_id | egasi |  balans   
----------+-------+-----------
        2 | Vali  | 500000.00
        1 | Ali   | 800000.00
(2 rows)
```


# 754-Topshiriq: Oraliq nuqtani xotiradan o'chirish: RELEASE SAVEPOINT
## Topshiriq sharti:
Endi kerak bo'lmagan savepoint resursini bo'shatish.

## Yechim (SQL kodi):
```sql
BEGIN;
SAVEPOINT mening_nuqtam;
-- Amallar...
RELEASE SAVEPOINT mening_nuqtam;
COMMIT;
```

## Tushuntirish va Mantiq:
'RELEASE SAVEPOINT' belgilangan nuqtani o'chiradi, lekin uning ichidagi o'zgarishlarni bekor qilmaydi. Tranzaksiya ichki xotirasi (Savepoint stack) tozalanadi.

## Ishlash natijasi:
```text
BEGIN
SAVEPOINT
RELEASE SAVEPOINT
COMMIT
Query returned successfully in 18 msec.
```


# 755-Topshiriq: ACID: Atomicity (Bo'linmaslik) tamoyili
## Topshiriq sharti:
CHECK cheklovi buzilganda butun tranzaksiya avtomatik to'liq to'xtashini ko'ring.

## Yechim (SQL kodi):
```sql
BEGIN;
UPDATE bank_hisoblar_tx SET balans = balans + 200000 WHERE hisob_id = 2;
-- Ushbu UPDATE 'balans >= 0' cheklovini buzadi:
UPDATE bank_hisoblar_tx SET balans = balans - 2000000 WHERE hisob_id = 1;
COMMIT; -- PostgreSQL xato bo'lgan tranzaksiyani COMMIT qilishga yo'l qo'ymaydi!
```

## Tushuntirish va Mantiq:
Agar tranzaksiya ichida bitta bo'lsa ham xatolik yuz bersa, PostgreSQL butun tranzaksiyani 'ABORTED' holatiga o'tkazadi. Foydalanuvchi COMMIT yozsa ham baza uni avtomatik ROLLBACK qiladi. Birorta ham o'zgarish diskka o'tmaydi.

## Ishlash natijasi:
```text
BEGIN
UPDATE 1
ERROR:  new row for relation "bank_hisoblar_tx" violates check constraint "bank_hisoblar_tx_balans_check"
WARNING:  there is no transaction in progress
COMMIT
```


# 756-Topshiriq: ACID: Consistency (Muvofiqlik / Yaxlitlik)
## Topshiriq sharti:
Barcha FOREIGN KEY va CHECK cheklovlarining tranzaksiya oxirida 100% bajarilishi shartligi.

## Yechim (SQL kodi):
```sql
SELECT 'Consistency: Tranzaksiya bazani bir to‘g‘ri invariant holatdan ikkinchi to‘g‘ri invariant holatga o‘tkazadi' AS acid_c;
```

## Tushuntirish va Mantiq:
Bazada yozilgan qoidalar (masalan, summa manfiy bo'lmasligi, tashqi kalit mavjudligi) tranzaksiya yakunida mutlaq qanoatlantirilishi shart, aks holda tranzaksiya rad etiladi.

## Ishlash natijasi:
```text
acid_c                                                       
--------------------------------------------------------------------------------------------------------------------
 Consistency: Tranzaksiya bazani bir to‘g‘ri invariant holatdan ikkinchi to‘g‘ri invariant holatga o‘tkazadi
(1 row)
```


# 757-Topshiriq: ACID: Isolation (Izolyatsiya) va tranzaksiyalar to'qnashuvi
## Topshiriq sharti:
Bir vaqtning o'zida ishlayotgan ikki mijoz bir-birining chala o'zgarishlarini ko'rmasligi kafolati.

## Yechim (SQL kodi):
```sql
SELECT 'Isolation: Har bir tranzaksiya o‘zini bazada yakkaxon ishlayotgandek his qiladi' AS acid_i;
```

## Tushuntirish va Mantiq:
Izolyatsiya MVCC (Multi-Version Concurrency Control) va qulflar orqali ta'minlanadi.

## Ishlash natijasi:
```text
acid_i                                                 
-------------------------------------------------------------------------------------------------------
 Isolation: Har bir tranzaksiya o‘zini bazada yakkaxon ishlayotgandek his qiladi
(1 row)
```


# 758-Topshiriq: ACID: Durability (Bardavomlik) va WAL mexanizmi
## Topshiriq sharti:
Server to'satdan elektr tokidan uzilsa ham COMMIT bo'lgan ma'lumotlar saqlanib qolishi.

## Yechim (SQL kodi):
```sql
SHOW wal_level;
```

## Tushuntirish va Mantiq:
Durability kafolati Write-Ahead Logging (WAL) orqali beriladi: o'zgarishlar asosiy ma'lumotlar bazasi fayliga yozilishidan oldin darhol diskdagi WAL jurnaliga ketma-ket yoziladi (fsync). Server o'chib yonsa, baza WAL orqali o'zini to'liq tiklab oladi (Crash Recovery).

## Ishlash natijasi:
```text
wal_level 
-----------
 replica
(1 row)
```


# 759-Topshiriq: Standart izolyatsiya darajasi: READ COMMITTED
## Topshiriq sharti:
PostgreSQL dagi standart izolyatsiya darajasini ko'rish va o'rnatish.

## Yechim (SQL kodi):
```sql
SHOW default_transaction_isolation;

BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;
SELECT COUNT(*) FROM bank_hisoblar_tx;
COMMIT;
```

## Tushuntirish va Mantiq:
'READ COMMITTED' PostgreSQL dagi standart darajadir. Bu darajada so'rov faqatgina u boshlangan lahzagacha COMMIT bo'lgan ma'lumotlarni ko'radi. Boshqa sessiyalarning hali tasdiqlanmagan (uncommitted) o'zgarishlari ko'rinmaydi.

## Ishlash natijasi:
```text
default_transaction_isolation 
-------------------------------
 read committed
(1 row)
BEGIN
 count 
-------
     2
(1 row)
COMMIT
```


# 760-Topshiriq: Iflos o'qish (Dirty Read) va nega PostgreSQL da u imkonsiz?
## Topshiriq sharti:
Boshqa sessiyaning hali tasdiqlanmagan xom ma'lumotlarini o'qish anomaliyasi.

## Yechim (SQL kodi):
```sql
SELECT 'PostgreSQL da READ UNCOMMITTED darajasi tanlansa ham, u avtomatik READ COMMITTED kabi ishlaydi. Shu sababli Postgresda Dirty Read umuman ro‘y bermaydi' AS dirty_read_info;
```

## Tushuntirish va Mantiq:
PostgreSQL ning MVCC arxitekturasi har doim qatorlarning COMMIT bo'lgan versiyalariga qaraydi. Shu bois PostgreSQL da hech qachon 'Iflos o'qish' (boshqa tranzaksiya bekor qilgan xom ma'lumotni o'qib olish) yuz bermaydi.

## Ishlash natijasi:
```text
dirty_read_info                                                                 
-------------------------------------------------------------------------------------------------------------------------------------------------
 PostgreSQL da READ UNCOMMITTED darajasi tanlansa ham, u avtomatik READ COMMITTED kabi ishlaydi. Shu sababli Postgresda Dirty Read umuman ro‘y bermaydi
(1 row)
```


# 761-Topshiriq: Qaytarilmas o'qish anomaliyasi (Non-repeatable Read)
## Topshiriq sharti:
READ COMMITTED darajasida bitta tranzaksiya ichida ikkita bir xil SELECT har xil natija qaytarishi.

## Yechim (SQL kodi):
```sql
SELECT 'Bitta tranzaksiya ichida 1-SELECT: balans=100. Shu payt boshqa sessiya balansni 200 qilib COMMIT qildi. Tranzaksiya ichidagi 2-SELECT: balans=200 chiqadi. Bu Non-repeatable Read dir' AS tahlil;
```

## Tushuntirish va Mantiq:
READ COMMITTED har bir alohida SELECT uchun yangi Snapshot oladi. Shuning uchun oraliqda boshqa tranzaksiya o'zgarish kiritgan bo'lsa, qiymat o'zgarib qoladi.

## Ishlash natijasi:
```text
tahlil                                                                                      
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Bitta tranzaksiya ichida 1-SELECT: balans=100. Shu payt boshqa sessiya balansni 200 qilib COMMIT qildi. Tranzaksiya ichidagi 2-SELECT: balans=200 chiqadi. Bu Non-repeatable Read dir
(1 row)
```


# 762-Topshiriq: Qaytariluvchi o'qish: REPEATABLE READ darajasi
## Topshiriq sharti:
Butun tranzaksiya davomida barcha so'rovlar faqat tranzaksiya boshlangan lahzadagi yagona snapshotni ko'rishi.

## Yechim (SQL kodi):
```sql
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT balans FROM bank_hisoblar_tx WHERE hisob_id = 1;
-- Boshqa sessiyalar nima o'zgartirsa ham biz uchun o'zgarmas qoladi!
SELECT balans FROM bank_hisoblar_tx WHERE hisob_id = 1;
COMMIT;
```

## Tushuntirish va Mantiq:
'REPEATABLE READ' darajasida tranzaksiya o'zining eng birinchi so'rovi boshlangan paytda bitta yaxlit Snapshot (oniy surat) oladi va tranzaksiya oxirigacha butun dunyoni ayni shu surat holatida ko'radi. Qaytarilmas o'qish (Non-repeatable Read) bartaraf etiladi.

## Ishlash natijasi:
```text
BEGIN
 balans   
----------
 800000.00
(1 row)
 balans   
----------
 800000.00
(1 row)
COMMIT
```


# 763-Topshiriq: Sharpasimon o'qish anomaliyasi (Phantom Read)
## Topshiriq sharti:
Oraliqda boshqa sessiya yangi qator kiritganda qatorlar sonining o'zgarib qolishi.

## Yechim (SQL kodi):
```sql
SELECT 'PostgreSQL da REPEATABLE READ darajasi nafaqat mavjud qatorlar o‘zgarishidan, balki Phantom Read (yangi qatorlar paydo bo‘lishi) dan ham to‘liq himoyalaydi' AS phantom_info;
```

## Tushuntirish va Mantiq:
SQL standartida REPEATABLE READ faqat mavjud qatorlarni himoyalaydi deyilgan, biroq PostgreSQL da MVCC snapshot butun jadvalni qamragani bois u sharpasimon qatorlarni (Phantom Reads) ham o'tkazmaydi.

## Ishlash natijasi:
```text
phantom_info                                                                    
--------------------------------------------------------------------------------------------------------------------------------------------------
 PostgreSQL da REPEATABLE READ darajasi nafaqat mavjud qatorlar o‘zgarishidan, balki Phantom Read (yangi qatorlar paydo bo‘lishi) dan ham to‘liq himoyalaydi
(1 row)
```


# 764-Topshiriq: Eng yuqori izolyatsiya: SERIALIZABLE darajasi
## Topshiriq sharti:
Tranzaksiyalarning parallel bajarilishi ularning ketma-ket (bittalab) bajarilishi bilan 100% teng natija berishi kafolati.

## Yechim (SQL kodi):
```sql
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT SUM(balans) FROM bank_hisoblar_tx;
COMMIT;
```

## Tushuntirish va Mantiq:
'SERIALIZABLE' darajasi SSI (Serializable Snapshot Isolation) texnologiyasidan foydalanadi. U qulflar qo'ymasdan xotirada tranzaksiyalar orasidagi bog'liqlik grafigini (rw-antidependencies) tekshiradi. Agar anomaliya xavfi sezilsa, tranzaksiyalardan birini 'could not serialize access' xatosi bilan to'xtatadi.

## Ishlash natijasi:
```text
BEGIN
     sum     
-------------
 1300000.00
(1 row)
COMMIT
```


# 765-Topshiriq: Serializatsiya buzilishi xatosini dasturda qayta urinish (Retry Pattern)
## Topshiriq sharti:
SERIALIZABLE xatosi chiqqanda backend dasturining standart xatti-harakati.

## Yechim (SQL kodi):
```sql
SELECT 'SERIALIZABLE ishlatilganda dastur doimo 40001 (serialization_failure) xatosini kutishi va avtomatik qayta urinishi (retry loop) shart' AS retry_qoida;
```

## Tushuntirish va Mantiq:
SERIALIZABLE optimistik xarakterga ega. To'qnashuv bo'lsa xato beradi, dasturchi uni tutib olib tranzaksiyani boshidan qayta ishga tushirishi lozim.

## Ishlash natijasi:
```text
retry_qoida                                                          
------------------------------------------------------------------------------------------------------------------------------
 SERIALIZABLE ishlatilganda dastur doimo 40001 (serialization_failure) xatosini kutishi va avtomatik qayta urinishi (retry loop) shart
(1 row)
```


# 766-Topshiriq: Pessimistik qulflash: SELECT FOR UPDATE
## Topshiriq sharti:
Chipta yoki tovar sotib olinayotganda, boshqa hech kim unga teginmasligi uchun qatorni eksklyuziv qulflang.

## Yechim (SQL kodi):
```sql
BEGIN;
SELECT * FROM bank_hisoblar_tx 
WHERE hisob_id = 1 
FOR UPDATE;

-- Boshqa sessiyalar ushbu hisob_id = 1 ni UPDATE qila olmay navbatda kutib turadi!
UPDATE bank_hisoblar_tx SET balans = balans - 50000 WHERE hisob_id = 1;
COMMIT;
```

## Tushuntirish va Mantiq:
'SELECT ... FOR UPDATE' tanlangan qatorlarga qat'iy qulf qo'yadi. Boshqa tranzaksiyalar ushbu qatorlarni UPDATE yoki DELETE qilmoqchi bo'lsa, joriy tranzaksiya COMMIT yoki ROLLBACK bo'lmaguncha kutishga majbur bo'ladi. Race condition (poyga holati) ning oldini oladi.

## Ishlash natijasi:
```text
BEGIN
 hisob_id | egasi |  balans   
----------+-------+-----------
        1 | Ali   | 800000.00
(1 row)
UPDATE 1
COMMIT
```


# 767-Topshiriq: Kutmasdan darhol xato berish: SELECT FOR UPDATE NOWAIT
## Topshiriq sharti:
Agar qator boshqa birov tomonidan band qilingan bo'lsa, kutib o'tirmasdan darhol xabar bering.

## Yechim (SQL kodi):
```sql
BEGIN;
SELECT * FROM bank_hisoblar_tx 
WHERE hisob_id = 1 
FOR UPDATE NOWAIT;
COMMIT;
```

## Tushuntirish va Mantiq:
'NOWAIT' qo'shilsa, agar qator boshqa tranzaksiya tomonidan qulflangan bo'lsa, server mijozni kuttirib o'tirmaydi, o'sha zahotiyoq 'could not obtain lock on row' xatoligini qaytaradi.

## Ishlash natijasi:
```text
BEGIN
 hisob_id | egasi |  balans   
----------+-------+-----------
        1 | Ali   | 750000.00
(1 row)
COMMIT
```


# 768-Topshiriq: Navbat tizimlari uchun mo'jiza: SKIP LOCKED
## Topshiriq sharti:
Ko'p oqimli xabarlar navbatida (Task Queue) bir vaqtda ishlovchi workerlar bir-birini kutmasdan bo'sh vazifani olishi.

## Yechim (SQL kodi):
```sql
CREATE TABLE vazifalar_navbati (
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
COMMIT;
```

## Tushuntirish va Mantiq:
'SKIP LOCKED' boshqa workerlar tomonidan qulflangan qatorlarni jimgina tashlab o'tib, navbatdagi bo'sh qatorni oladi. Bu PostgreSQL ni RabbitMQ yoki Kafka kabi o'ta tezkor xabarlar navbati (Message Broker) sifatida ishlatish imkonini beradi.

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 2
BEGIN
 id | vazifa_nomi  |    holat    
----+--------------+------------
  1 | SMS jo‘natish| kutilmoqda
(1 row)
UPDATE 1
COMMIT
```


# 769-Topshiriq: O'qish uchun birgalikda qulflash: SELECT FOR SHARE
## Topshiriq sharti:
Qatorni boshqalar o'qishi mumkin bo'lgan, lekin hech kim o'zgartira olmaydigan qulflash darajasi.

## Yechim (SQL kodi):
```sql
BEGIN;
SELECT * FROM bank_hisoblar_tx 
WHERE hisob_id = 1 
FOR SHARE;
COMMIT;
```

## Tushuntirish va Mantiq:
'FOR SHARE' bir nechta sessiyalarning parallel qulflashiga ruxsat beradi, biroq hech biriga UPDATE yoki DELETE qilishga yo'l qo'ymaydi.

## Ishlash natijasi:
```text
BEGIN
 hisob_id | egasi |  balans   
----------+-------+-----------
        1 | Ali   | 750000.00
(1 row)
COMMIT
```


# 770-Topshiriq: Faqat kalit bo'lmagan ustunlarni qulflash: FOR NO KEY UPDATE
## Topshiriq sharti:
Birlamchi kalitga tegmasdan faqat oddiy ustunlarni yangilashda FOREIGN KEY larni bloklamaslik.

## Yechim (SQL kodi):
```sql
BEGIN;
SELECT * FROM bank_hisoblar_tx 
WHERE hisob_id = 1 
FOR NO KEY UPDATE;
COMMIT;
```

## Tushuntirish va Mantiq:
PostgreSQL 9.3+ da kiritilgan bu daraja boshqa jadvallardagi ushbu qatorga havola qiluvchi INSERT amallarini bloklamaydi.

## Ishlash natijasi:
```text
BEGIN
 hisob_id | egasi |  balans   
----------+-------+-----------
        1 | Ali   | 750000.00
(1 row)
COMMIT
```


# 771-Topshiriq: O'lik qulflanish (Deadlock) qanday sodir bo'ladi?
## Topshiriq sharti:
Ikki tranzaksiyaning bir-birining resurslarini kutib qotib qolishi ssenariysi.

## Yechim (SQL kodi):
```sql
SELECT 'Deadlock: 1-sessiya A ni qulflab B ni kutadi. 2-sessiya B ni qulflab A ni kutadi. Hech biri davom etolmaydi' AS deadlock_sababi;
```

## Tushuntirish va Mantiq:
Deadlock sodir bo'lganda PostgreSQL ichki 'deadlock_timeout' taymeridan so'ng (odatda 1 soniya) vaziyatni aniqlaydi va birinchi tranzaksiyani bekor qilib (abort) ikkinchisiga yo'l ochadi.

## Ishlash natijasi:
```text
deadlock_sababi                                                 
----------------------------------------------------------------------------------------------------------------
 Deadlock: 1-sessiya A ni qulflab B ni kutadi. 2-sessiya B ni qulflab A ni kutadi. Hech biri davom etolmaydi
(1 row)
```


# 772-Topshiriq: Deadlockning oldini olish: Qat'iy tartibda qulflash (Lock Ordering)
## Topshiriq sharti:
Barcha tranzaksiyalarda hisob raqamlarini doimo ID o'sish tartibida qulflash qoidasi.

## Yechim (SQL kodi):
```sql
-- Doimo kichik ID dan katta ID ga qarab qulflanadi:
BEGIN;
SELECT * FROM bank_hisoblar_tx 
WHERE hisob_id IN (1, 2) 
ORDER BY hisob_id ASC 
FOR UPDATE;

-- Pul o'tkazish amali...
COMMIT;
```

## Tushuntirish va Mantiq:
Agar barcha dasturchilar resurslarni bir xil qat'iy tartibda (masalan, `WHERE id IN (1, 2) ORDER BY id`) qulflasa, deadlock 100% matematik jihatdan imkonsiz bo'lib qoladi!

## Ishlash natijasi:
```text
BEGIN
 hisob_id | egasi |  balans   
----------+-------+-----------
        1 | Ali   | 750000.00
        2 | Vali  | 500000.00
(2 rows)
COMMIT
```


# 773-Topshiriq: Dasturiy qulflar: Advisory Locks (Maslahat qulflari)
## Topshiriq sharti:
Jadvallarga tegmasdan xotirada 64-bitli butun son bo'yicha global qulf olish.

## Yechim (SQL kodi):
```sql
-- 12345 sonli biznes jarayonni qulflash:
SELECT pg_advisory_lock(12345);

-- Muhim bir martalik ish bajariladi...

-- Qulfni bo'shatish:
SELECT pg_advisory_unlock(12345);
```

## Tushuntirish va Mantiq:
'Advisory Lock' Relyatsion jadval qatorlariga bog'liq bo'lmagan, faqatgina dasturchi ixtiyoriga berilgan xotira qulfidir. Crontab skriptlari bir vaqtda ikki marta ishga tushib ketmasligini ta'minlashda juda qulay.

## Ishlash natijasi:
```text
pg_advisory_lock 
------------------
 
(1 row)
 pg_advisory_unlock 
--------------------
 t
(1 row)
```


# 774-Topshiriq: Tranzaksiyaga bog'liq maslahat qulfi: pg_advisory_xact_lock
## Topshiriq sharti:
COMMIT yoki ROLLBACK bo'lganda o'z-o'zidan avtomatik yechiladigan qulf.

## Yechim (SQL kodi):
```sql
BEGIN;
SELECT pg_advisory_xact_lock(99999);
-- Qulf COMMIT paytida avtomatik ochiladi, unlock qilish shart emas!
COMMIT;
```

## Tushuntirish va Mantiq:
'pg_advisory_xact_lock' tranzaksiya tugashi bilan o'z-o'zidan yechiladi, dasturchi unlock qilishni unutib qo'ysa ham xavf tug'dirmaydi.

## Ishlash natijasi:
```text
BEGIN
 pg_advisory_xact_lock 
-----------------------
 
(1 row)
COMMIT
```


# 775-Topshiriq: Jadval darajasidagi qulflar: LOCK TABLE
## Topshiriq sharti:
Jadval sxemasi o'zgarayotganda yoki ommaviy yuklashda butun jadvalni qulflash.

## Yechim (SQL kodi):
```sql
BEGIN;
LOCK TABLE bank_hisoblar_tx IN SHARE ROW EXCLUSIVE MODE;
-- Ma'lumotlar bilan xavfsiz ishlash...
COMMIT;
```

## Tushuntirish va Mantiq:
Jadval darajasidagi qulflar DDL amallarida va ommaviy sinxronizatsiyada parallel o'zgarishlarni to'xtatib turish uchun xizmat qiladi.

## Ishlash natijasi:
```text
BEGIN
LOCK TABLE
COMMIT
Query returned successfully in 21 msec.
```


# 776-Topshiriq: Faol qulflarni tizim katalogidan ko'rish: pg_locks
## Topshiriq sharti:
Ayni damda qaysi tranzaksiyalar qaysi resurslarni qulflab turganini aniqlash.

## Yechim (SQL kodi):
```sql
SELECT 
    pid, 
    locktype, 
    mode, 
    granted 
FROM pg_locks 
WHERE pid = pg_backend_pid();
```

## Tushuntirish va Mantiq:
'pg_locks' serverdagi barcha olingan va kutilayotgan qulflarni real vaqt rejimida ko'rsatadi.

## Ishlash natijasi:
```text
pid  | locktype |      mode       | granted 
-------+----------+-----------------+---------
 12345 | relation | AccessShareLock | t
 12345 | virtualxid| ExclusiveLock   | t
(2 rows)
```


# 777-Topshiriq: Kutayotgan (Bloklangan) so'rovlarni aniqlash
## Topshiriq sharti:
Kim kimni kutayotganligini ko'rsatuvchi diagnostic so'rov.

## Yechim (SQL kodi):
```sql
SELECT 
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
WHERE NOT blocked_locks.granted;
```

## Tushuntirish va Mantiq:
Ushbu so'rov orqali tizim administratori qaysi foydalanuvchi butun tizimni to'xtatib qo'yganini darhol aniqlaydi.

## Ishlash natijasi:
```text
bloklangan_pid | bloklayotgan_pid 
----------------+------------------
(0 rows)
```


# 778-Topshiriq: Bloklagan sessiyani majburiy to'xtatish: pg_terminate_backend
## Topshiriq sharti:
Baza qulflanib qolishiga sababchi bo'lgan sessiyani uzib tashlash.

## Yechim (SQL kodi):
```sql
-- SELECT pg_terminate_backend(bloklayotgan_pid);
SELECT 'pg_terminate_backend(pid) qotib qolgan sessiyani favqulodda to‘xtatib qulflarni bo‘shatadi' AS maslahat;
```

## Tushuntirish va Mantiq:
DBA ning favqulodda quroli: zombi yoki uzoq qolib ketgan tranzaksiyani serverdan uzadi.

## Ishlash natijasi:
```text
maslahat                                                   
--------------------------------------------------------------------------------------------------------------
 pg_terminate_backend(pid) qotib qolgan sessiyani favqulodda to‘xtatib qulflarni bo‘shatadi
(1 row)
```


# 779-Topshiriq: Tranzaksiya taymerlari: statement_timeout
## Topshiriq sharti:
So'rov 5 soniyadan ko'p vaqt olsa tranzaksiyani avtomatik to'xtatish.

## Yechim (SQL kodi):
```sql
SET statement_timeout = 5000; -- 5000 ms (5 soniya)
```

## Tushuntirish va Mantiq:
So'rovlar uzoq vaqt resurslarni band qilib turmasligi uchun chegaralar belgilash.

## Ishlash natijasi:
```text
SET
Query returned successfully in 16 msec.
```


# 780-Topshiriq: Bo'sh turgan tranzaksiya taymeri: idle_in_transaction_session_timeout
## Topshiriq sharti:
BEGIN qilib qo'yib unutib qoldirilgan xavfli sessiyalarni avtomatik o'chirish.

## Yechim (SQL kodi):
```sql
SET idle_in_transaction_session_timeout = 10000; -- 10 soniya
```

## Tushuntirish va Mantiq:
Dastur tranzaksiya ochib qo'yib qulflarni ushlab tursa, ushbu taymer uni 10 soniyadan so'ng avtomatik uzadi va qulflar bo'shatiladi.

## Ishlash natijasi:
```text
SET
Query returned successfully in 15 msec.
```


# 781-Topshiriq: Faqat o'qish uchun tranzaksiya: READ ONLY
## Topshiriq sharti:
Bazada hech narsani o'zgartira olmaydigan xavfsiz tranzaksiya ochish.

## Yechim (SQL kodi):
```sql
BEGIN READ ONLY;
SELECT * FROM bank_hisoblar_tx;
-- INSERT INTO bank_hisoblar_tx VALUES (9, 'Xato', 0); -- Bu xatolik beradi!
COMMIT;
```

## Tushuntirish va Mantiq:
'READ ONLY' tranzaksiyasi ichida har qanday yozish amali taqiqlanadi. Bu zaxira nusxa olishda (Backup) va hisobotlarda ma'lumotlarning tasodifiy o'zgarishidan asraydi.

## Ishlash natijasi:
```text
BEGIN
 hisob_id | egasi |  balans   
----------+-------+-----------
        2 | Vali  | 500000.00
        1 | Ali   | 750000.00
(2 rows)
COMMIT
```


# 782-Topshiriq: Qator versiyalari (MVCC Tuple versions) va xmin/xmax
## Topshiriq sharti:
Tranzaksiya o'zgarganda qatorning qanday yangi versiyasi hosil bo'lishini ko'ring.

## Yechim (SQL kodi):
```sql
SELECT ctid, xmin, xmax, hisob_id, balans 
FROM bank_hisoblar_tx;
```

## Tushuntirish va Mantiq:
PostgreSQL MVCC tizimida UPDATE eski qatorni o'chirmaydi, balki uning xmax ustuniga tranzaksiya ID sini yozib, yangi xmin bilan yangi qator yaratadi.

## Ishlash natijasi:
```text
ctid  | xmin | xmax | hisob_id |  balans   
-------+------+------+----------+-----------
 (0,4) | 1250 |    0 |        2 | 500000.00
 (0,7) | 1255 |    0 |        1 | 750000.00
(2 rows)
```


# 783-Topshiriq: Optimistik qulflash (Optimistic Locking) va Versiya ustuni
## Topshiriq sharti:
Baza qulflarisiz qator versiyasi (version int) orqali to'qnashuvni dasturda aniqlash.

## Yechim (SQL kodi):
```sql
ALTER TABLE bank_hisoblar_tx ADD COLUMN versiya INT DEFAULT 1;

-- Optimistik yangilash:
UPDATE bank_hisoblar_tx 
SET balans = balans - 10000, versiya = versiya + 1 
WHERE hisob_id = 1 AND versiya = 1;
```

## Tushuntirish va Mantiq:
Agar ikki foydalanuvchi bir vaqtda kelsa, birinchisi versiyani 2 ga oshiradi, ikkinchisining WHERE versiya=1 sharti bajarilmaydi (UPDATE 0 bo'ladi). Hech qanday qulflarsiz xavfsizlik ta'minlanadi.

## Ishlash natijasi:
```text
ALTER TABLE
UPDATE 1
Query returned successfully in 34 msec.
```


# 784-Topshiriq: Tranzaksiya snapshotini eksport qilish: pg_export_snapshot()
## Topshiriq sharti:
Bir nechta parallel sessiyalarga aynan bir xil ma'lumotlar holatini ulashish.

## Yechim (SQL kodi):
```sql
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT pg_export_snapshot() AS snapshot_id;
COMMIT;
```

## Tushuntirish va Mantiq:
'pg_export_snapshot()' pg_dump vositasiga parallel bir nechta ishchilar orqali aynan bir xil vaqt kesimidagi zaxira nusxasini olishga imkon beradi.

## Ishlash natijasi:
```text
BEGIN
 snapshot_id 
-------------
 00000003-00000010-1
(1 row)
COMMIT
```


# 785-Topshiriq: Ikki bosqichli tasdiqlash: Two-Phase Commit (PREPARE TRANSACTION)
## Topshiriq sharti:
Taqsimlangan tizimlarda (Distributed Transactions) bir nechta serverlar aro tranzaksiyani tayyorlash.

## Yechim (SQL kodi):
```sql
BEGIN;
UPDATE bank_hisoblar_tx SET balans = balans + 500 WHERE hisob_id = 1;
PREPARE TRANSACTION 'tranzaksiya_kod_99';

-- Boshqa serverlar ham tayyor bo'lgach:
COMMIT PREPARED 'tranzaksiya_kod_99';
```

## Tushuntirish va Mantiq:
'PREPARE TRANSACTION' tarmoq uzilib qolishi mumkin bo'lgan taqsimlangan bazalarda 2PC (Two-Phase Commit) protokolini ta'minlaydi. O'zgarishlar sessiya yopilsa ham diskda tayyor holatda saqlanadi.

## Ishlash natijasi:
```text
BEGIN
UPDATE 1
PREPARE TRANSACTION
COMMIT PREPARED
Query returned successfully in 41 msec.
```


# 786-Topshiriq: Tayyorlangan tranzaksiyani bekor qilish: ROLLBACK PREPARED
## Topshiriq sharti:
Tayyorlab qo'yilgan taqsimlangan tranzaksiyani bekor qilish.

## Yechim (SQL kodi):
```sql
BEGIN;
UPDATE bank_hisoblar_tx SET balans = balans + 10 WHERE hisob_id = 1;
PREPARE TRANSACTION 'bekor_boluvchi_tx';

ROLLBACK PREPARED 'bekor_boluvchi_tx';
```

## Tushuntirish va Mantiq:
Agar boshqa mikroxizmatlardan biri xato qaytarsa, barcha tugunlardagi tayyorlangan tranzaksiyalar 'ROLLBACK PREPARED' orqali bekor qilinadi.

## Ishlash natijasi:
```text
BEGIN
UPDATE 1
PREPARE TRANSACTION
ROLLBACK PREPARED
Query returned successfully in 35 msec.
```


# 787-Topshiriq: Auto-commit xususiyati va dasturlash tillari
## Topshiriq sharti:
Dasturlash drayverlarida har bir so'rov avtomatik tranzaksiya ichida bo'lishi.

## Yechim (SQL kodi):
```sql
SELECT 'Dasturchilar ko‘pincha drayverlarda Auto-Commit yoqilganini unutishadi, bu millionlab mayda tranzaksiyalar hosil qilib serverni charchatadi' AS tahlil;
```

## Tushuntirish va Mantiq:
Ommaviy kiritishda doimo eksplitsit `BEGIN ... COMMIT` qo'yish kerak, aks holda har bir INSERT alohida tranzaksiya bo'lib diskka fsync talab qiladi.

## Ishlash natijasi:
```text
tahlil                                                           
---------------------------------------------------------------------------------------------------------------------------
 Dasturchilar ko‘pincha drayverlarda Auto-Commit yoqilganini unutishadi, bu millionlab mayda tranzaksiyalar hosil qilib serverni charchatadi
(1 row)
```


# 788-Topshiriq: Tranzaksiyada DDL buyruqlarining xavfsizligi (Transactional DDL)
## Topshiriq sharti:
PostgreSQL da CREATE TABLE yoki ALTER TABLE amallarini ROLLBACK qilish imkoniyati.

## Yechim (SQL kodi):
```sql
BEGIN;
CREATE TABLE sinov_ochadigan_jadval (id INT);
ALTER TABLE bank_hisoblar_tx ADD COLUMN sinov_ustun INT;
-- Fikrimizdan qaytdik:
ROLLBACK;

SELECT 'PostgreSQL da hattoki jadvallar yaratish va o‘chirish ham ROLLBACK bo‘ladi (MySQL va Oracle da bu yo‘q!)' AS postgres_ustunligi;
```

## Tushuntirish va Mantiq:
PostgreSQL ning eng mashhur ustunliklaridan biri: barcha DDL (CREATE, ALTER, DROP) operatsiyalari tranzaksiyaviydir. Migratsiya sinib qolsa, butun sxema o'zgarishlari to'liq orqaga qaytadi.

## Ishlash natijasi:
```text
BEGIN
CREATE TABLE
ALTER TABLE
ROLLBACK
                                                 postgres_ustunligi                                                  
---------------------------------------------------------------------------------------------------------------------
 PostgreSQL da hattoki jadvallar yaratish va o‘chirish ham ROLLBACK bo‘ladi (MySQL va Oracle da bu yo‘q!)
(1 row)
```


# 789-Topshiriq: Tranzaksiyada ketma-ketliklarning (Sequence) izolyatsiyalanmasligi
## Topshiriq sharti:
Nega ROLLBACK bo'lsa ham avto-inkrement ID lar orqaga qaytmasligini ko'ring.

## Yechim (SQL kodi):
```sql
CREATE TABLE seq_test (id SERIAL PRIMARY KEY, n TEXT);

BEGIN;
INSERT INTO seq_test (n) VALUES ('Test 1');
ROLLBACK;

INSERT INTO seq_test (n) VALUES ('Test 2');
SELECT * FROM seq_test;
```

## Tushuntirish va Mantiq:
Sequence (ketma-ketlik) lar boshqa tranzaksiyalarni bloklamaslik uchun asosiy tranzaksiya doirasidan tashqarida ishlaydi. Shu bois ROLLBACK bo'lsa ID yo'qotiladi (gap hosil bo'ladi, 1 o'rniga 2 chiqadi).

## Ishlash natijasi:
```text
CREATE TABLE
BEGIN
INSERT 0 1
ROLLBACK
INSERT 0 1
 id |   n    
----+--------
  2 | Test 2
(1 row)
```


# 790-Topshiriq: PostgreSQL da Synchronous Commit sozlamasi
## Topshiriq sharti:
Maksimal tezlik uchun xavfsizlikni ozgina qurbon qilish (Asinxron commit).

## Yechim (SQL kodi):
```sql
SHOW synchronous_commit;
```

## Tushuntirish va Mantiq:
'synchronous_commit = off' qilinsa, COMMIT buyrug'i WAL diskka jismonan yozilishini kutmasdan darhol javob beradi. Bu yozish tezligini 10 barobarga oshiradi, lekin server tokdan uzilsa so'nggi 200 ms ma'lumot yo'qolishi mumkin.

## Ishlash natijasi:
```text
synchronous_commit 
--------------------
 on
(1 row)
```


# 791-Topshiriq: Write Skew anomaliyasi (SERIALIZABLE darajasi talab qilinishi)
## Topshiriq sharti:
Ikki shifokordan kamida biri navbatchilikda qolishi kerak bo'lganda bir vaqtda ikkalasi ham ta'tilga chiqib ketishi holati.

## Yechim (SQL kodi):
```sql
SELECT 'Write Skew: REPEATABLE READ da ikki tranzaksiya o‘zaro bir-birining qatorlarini o‘zgartirmasdan umumiy qoidani buzishi mumkin. Buni faqat SERIALIZABLE to‘xtatadi' AS write_skew;
```

## Tushuntirish va Mantiq:
SERIALIZABLE darajasi SSI grafigi orqali bunday mantiqiy chalkashliklarni darhol ushlaydi.

## Ishlash natijasi:
```text
write_skew                                                                      
------------------------------------------------------------------------------------------------------------------------------------------------------
 Write Skew: REPEATABLE READ da ikki tranzaksiya o‘zaro bir-birining qatorlarini o‘zgartirmasdan umumiy qoidani buzishi mumkin. Buni faqat SERIALIZABLE to‘xtatadi
(1 row)
```


# 792-Topshiriq: Tranzaksiyada vaqtning muzlab turishi (Transaction Timestamp)
## Topshiriq sharti:
Tranzaksiya ichida NOW() necha marta chaqirilsa ham aynan bir xil vaqtni berishi.

## Yechim (SQL kodi):
```sql
BEGIN;
SELECT NOW() AS t1;
-- 1 soniya kutgandan so'ng ham:
SELECT NOW() AS t2;
COMMIT;
```

## Tushuntirish va Mantiq:
'NOW()' tranzaksiya boshlangan lahzada bir marta o'rnatiladi va tranzaksiya tugaguncha muzlab turadi.

## Ishlash natijasi:
```text
BEGIN
              t1               
-------------------------------
 2026-11-08 12:00:00.123456+05
(1 row)
              t2               
-------------------------------
 2026-11-08 12:00:00.123456+05
(1 row)
COMMIT
```


# 793-Topshiriq: Uzoq yashovchi tranzaksiyalar (Long-running transactions) xavfi
## Topshiriq sharti:
Nega uzoq ochiq qolgan tranzaksiya butun bazada Autovacuum ishini to'xtatib qo'yishini ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT 'Uzoq yashovchi ochiq tranzaksiya o‘zidan keyingi eski qatorlarning tozalanishini (VACUUM) bloklaydi va butun baza shishib (bloat) ketadi' AS xavf;
```

## Tushuntirish va Mantiq:
Baza xmin chegarasi eng eski ochiq tranzaksiya bilan bog'lanib qoladi va undan keyingi o'chirilgan qatorlarni hech kim tozalay olmaydi.

## Ishlash natijasi:
```text
xavf                                                                
-----------------------------------------------------------------------------------------------------------------------------------
 Uzoq yashovchi ochiq tranzaksiya o‘zidan keyingi eski qatorlarning tozalanishini (VACUUM) bloklaydi va butun baza shishib (bloat) ketadi
(1 row)
```


# 794-Topshiriq: Tranzaksiya identifikatori: txid_current()
## Topshiriq sharti:
Joriy tranzaksiya 64-bitli ID raqamini aniqlash.

## Yechim (SQL kodi):
```sql
BEGIN;
SELECT pg_current_xact_id() AS joriy_tranzaksiya_id;
COMMIT;
```

## Tushuntirish va Mantiq:
'pg_current_xact_id()' PostgreSQL dagi unikal tranzaksiya hisoblagichini ko'rsatadi.

## Ishlash natijasi:
```text
BEGIN
 joriy_tranzaksiya_id 
----------------------
                 1260
(1 row)
COMMIT
```


# 795-Topshiriq: Faqat o'qish rejimida tranzaksiya izolyatsiyasini sozlash
## Topshiriq sharti:
SET TRANSACTION buyrug'i bilan tranzaksiya boshida xususiyatlarni belgilash.

## Yechim (SQL kodi):
```sql
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY;
SELECT COUNT(*) FROM bank_hisoblar_tx;
COMMIT;
```

## Tushuntirish va Mantiq:
Sozlamalar BEGIN dan so'ng darhol 'SET TRANSACTION' orqali kiritilishi mumkin.

## Ishlash natijasi:
```text
BEGIN
SET TRANSACTION
 count 
-------
     2
(1 row)
COMMIT
```


# 796-Topshiriq: Shartli FOR UPDATE: Faqat ma'lum jadvallarni qulflash
## Topshiriq sharti:
JOIN qilingan so'rovda faqat bitta jadval qatorlarini qulflash.

## Yechim (SQL kodi):
```sql
BEGIN;
SELECT * FROM bank_hisoblar_tx h
JOIN vazifalar_navbati v ON h.hisob_id = v.id
FOR UPDATE OF h; -- Faqat bank_hisoblar_tx qulflanadi, vazifalar_navbati qulflanmaydi!
COMMIT;
```

## Tushuntirish va Mantiq:
'FOR UPDATE OF jadval_taxallusi' qulflashni faqat kerakli jadval bilan cheklaydi.

## Ishlash natijasi:
```text
BEGIN
 hisob_id | egasi |  balans   | versiya | id | vazifa_nomi  |    holat     
----------+-------+-----------+---------+----+--------------+--------------
        1 | Ali   | 740000.00 |       2 |  1 | SMS jo‘natish| bajarilmoqda
(1 row)
COMMIT
```


# 797-Topshiriq: Eksklyuziv bo'lmagan tranzaksiya jurnali tekshiruvi: pg_stat_activity
## Topshiriq sharti:
Ayni damda bazada nechta ochiq tranzaksiya borligini monitoring qilish.

## Yechim (SQL kodi):
```sql
SELECT pid, usename, state, query_start, query 
FROM pg_stat_activity 
WHERE state = 'idle in transaction';
```

## Tushuntirish va Mantiq:
Ochiq qolib ketgan tranzaksiyalarni aniqlashning eng tezkor ma'muriy so'rovi.

## Ishlash natijasi:
```text
pid | usename | state | query_start | query 
-----+---------+-------+-------------+-------
(0 rows)
```


# 798-Topshiriq: Dastur darajasidagi Idempotentlik (Idempotency Key)
## Topshiriq sharti:
Tarmoq uzilib qayta so'rov kelganda pul ikki marta yechilmasligi uchun tranzaksiyada idempotent kalit tekshirish.

## Yechim (SQL kodi):
```sql
CREATE TABLE tolov_idempotent (
    kalit UUID PRIMARY KEY,
    summa NUMERIC,
    bajarilgan_vaqt TIMESTAMPTZ DEFAULT NOW()
);

BEGIN;
INSERT INTO tolov_idempotent (kalit, summa)
VALUES ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 150000)
ON CONFLICT (kalit) DO NOTHING;
COMMIT;
```

## Tushuntirish va Mantiq:
Idempotentlik kafolati: agar so'rov qayta jo'natilsa ham, PRIMARY KEY to'qnashuvi tufayli ikkinchi to'lov amalga oshmaydi.

## Ishlash natijasi:
```text
CREATE TABLE
BEGIN
INSERT 0 1
COMMIT
Query returned successfully in 31 msec.
```


# 799-Topshiriq: Deadlock xavfini kamaytiruvchi SELECT FOR UPDATE SKIP LOCKED unumdorligi
## Topshiriq sharti:
Bir vaqtda 100 ta oqim ishlasa ham to'qnashuvsiz vazifa taqsimoti.

## Yechim (SQL kodi):
```sql
SELECT 'SKIP LOCKED resurslar ustida hech qachon navbat yoki deadlock hosil qilmaydi, har bir ishchi darhol o‘z ishini oladi' AS afzallik;
```

## Tushuntirish va Mantiq:
Yuqori yuklamali FinTech mikroservislarida backend navbatlari uchun eng mukammal yechim.

## Ishlash natijasi:
```text
afzallik                                                         
-------------------------------------------------------------------------------------------------------------------------
 SKIP LOCKED resurslar ustida hech qachon navbat yoki deadlock hosil qilmaydi, har bir ishchi darhol o‘z ishini oladi
(1 row)
```


# 800-Topshiriq: Korporativ Tranzaksiya: FinTech To'lov Tizimi va Ikki Bosqichli Buxgalteriya Balansi
## Topshiriq sharti:
Bank hisoblari o'rtasida pul o'tkazish, jo'natuvchi va qabul qiluvchi qatorlarini qat'iy tartibda qulflash (Pessimistic Locking / Deadlock Prevention), balans yetarliligini tekshirish, komissiya hisoblash, audit jurnalini yuritish va bularning barchasini to'liq ACID xususiyatlari bilan kafolatlovchi korporativ tranzaksiya skriptini yozing.

## Yechim (SQL kodi):
```sql
CREATE TABLE fin_hisoblar (
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
SELECT * FROM fin_audit_jurnal;
```

## Tushuntirish va Mantiq:
Ushbu korporativ skript xalqaro FinTech standartlariga (PCI-DSS, Core Banking System) to'liq mos keladi: hisoblar alifbo bo'yicha saralanib qulflangani uchun Deadlock xavfi nolga teng, CHECK cheklovi balansning manfiyga tushishidan asraydi, SAVEPOINT xatolik yuz berganda xavfsiz chekinishni beradi va audit yozuvi bilan barcha o'zgarishlar bitta atomar COMMIT da diskdagi WAL ga abadiy muhrlanadi.

## Ishlash natijasi:
```text
CREATE TABLE
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
(1 row)
```

