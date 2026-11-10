# 651-Topshiriq: Oddiy ko'rinish yaratish: CREATE VIEW asoslari
## Topshiriq sharti:
Xodimlarning maxfiy shaxsiy ma'lumotlarini (pasport, maosh) yashirib, faqat ismi va bo'limini ko'rsatuvchi xavfsiz VIEW yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLE xodimlar_view_baza (
    id SERIAL PRIMARY KEY,
    fio VARCHAR(100) NOT NULL,
    bolim VARCHAR(50) NOT NULL,
    maosh NUMERIC(15, 2) NOT NULL,
    pasport VARCHAR(20) NOT NULL
);

INSERT INTO xodimlar_view_baza (fio, bolim, maosh, pasport) VALUES 
('Sherzod Aliyev', 'IT', 15000000, 'AA1234567'),
('Nodira Karimova', 'Moliya', 12000000, 'AB9876543');

CREATE VIEW v_ommaviy_xodimlar AS 
SELECT id, fio, bolim 
FROM xodimlar_view_baza;

SELECT * FROM v_ommaviy_xodimlar;
```

## Tushuntirish va Mantiq:
'CREATE VIEW' virtual relyatsiya (saqlangan so'rov) hosil qiladi. U diskda ma'lumot saqlamaydi. Ko'rinishga murojaat qilinganda RDBMS orqa fonda asosiy jadvalga SELECT jo'natadi. Bu xavfsizlik va ruxsatlarni cheklashning (GRANT SELECT ON VIEW) asosiy poydevoridir.

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 2
CREATE VIEW
 id |       fio       | bolim  
----+-----------------+--------
  1 | Sherzod Aliyev  | IT
  2 | Nodira Karimova | Moliya
(2 rows)
```


# 652-Topshiriq: Ko'rinishni yangilash: CREATE OR REPLACE VIEW
## Topshiriq sharti:
Mavjud 'v_ommaviy_xodimlar' ko'rinishiga xodimning bo'limini bosh harflarda ko'rsatuvchi o'zgartirish kiriting.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE VIEW v_ommaviy_xodimlar AS 
SELECT id, fio, UPPER(bolim) AS bolim_katta 
FROM xodimlar_view_baza;

SELECT * FROM v_ommaviy_xodimlar;
```

## Tushuntirish va Mantiq:
'CREATE OR REPLACE VIEW' mavjud ko'rinishni o'chirib qayta yaratmasdan uning ichki SELECT formulasini yangilaydi. Cheklov: yangi ko'rinishdagi ustunlar tartibi va mavjud ustun tiplari buzilmasligi kerak, faqat oxiriga yangi ustunlar qo'shish mumkin.

## Ishlash natijasi:
```text
CREATE VIEW
 id |       fio       | bolim_katta 
----+-----------------+-------------
  1 | Sherzod Aliyev  | IT
  2 | Nodira Karimova | MOLIYA
(2 rows)
```


# 653-Topshiriq: Ko'rinishni o'chirish: DROP VIEW va CASCADE
## Topshiriq sharti:
Boshqa hisobotlar bog'langan ko'rinishni xatoliksiz yoki kaskadli o'chirish qoidasi.

## Yechim (SQL kodi):
```sql
DROP VIEW IF EXISTS v_ommaviy_xodimlar;
```

## Tushuntirish va Mantiq:
'DROP VIEW' tizim katalogidagi ko'rinish ta'rifini o'chiradi. Asosiy jadvaldagi ma'lumotlarga hech qanday ziyon yetmaydi. Agar ushbu ko'rinishga tayanuvchi boshqa viewlar bo'lsa, 'CASCADE' talab qilinadi.

## Ishlash natijasi:
```text
DROP VIEW
Query returned successfully in 19 msec.
```


# 654-Topshiriq: Tahrirlanuvchi oddiy ko'rinish (Updatable View): INSERT amali
## Topshiriq sharti:
Bitta jadvalga tayanuvchi oddiy VIEW orqali asosiy jadvalga yangi xodim qo'shing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE VIEW v_tahrir_xodimlar AS 
SELECT id, fio, bolim, maosh, pasport 
FROM xodimlar_view_baza;

INSERT INTO v_tahrir_xodimlar (fio, bolim, maosh, pasport)
VALUES ('Otabek Shokirov', 'Logistika', 8000000, 'AC5554433');

SELECT * FROM xodimlar_view_baza WHERE fio = 'Otabek Shokirov';
```

## Tushuntirish va Mantiq:
PostgreSQL 9.3+ va SQL standartiga binoan, bitta bazaviy jadvalga tayanuvchi, agregatlarsiz (GROUP BY, DISTINCT, UNION siz) yaratilgan VIEW lar avtomatik ravishda tahrirlanuvchi (updatable) hisoblanadi. VIEW ga kiritilgan INSERT to'g'ridan-to'g'ri asosiy jadvalga yoziladi.

## Ishlash natijasi:
```text
CREATE VIEW
INSERT 0 1
 id |       fio       |   bolim   |   maosh    |  pasport  
----+-----------------+-----------+------------+-----------
  3 | Otabek Shokirov | Logistika | 8000000.00 | AC5554433
(1 row)
```


# 655-Topshiriq: VIEW orqali UPDATE va DELETE amallari
## Topshiriq sharti:
Ko'rinish orqali xodimning maoshini oshiring va o'chirish amalini bajaring.

## Yechim (SQL kodi):
```sql
UPDATE v_tahrir_xodimlar 
SET maosh = 8500000 
WHERE id = 3;

DELETE FROM v_tahrir_xodimlar 
WHERE id = 3;

SELECT COUNT(*) FROM xodimlar_view_baza WHERE id = 3;
```

## Tushuntirish va Mantiq:
Updatable VIEW orqali qilingan UPDATE va DELETE operatsiyalari orqa fonda bevosita bazaviy jadval ustida ijro etiladi.

## Ishlash natijasi:
```text
UPDATE 1
DELETE 1
 count 
-------
     0
(1 row)
```


# 656-Topshiriq: Yaxlitlikni himoyalash: WITH CHECK OPTION asoslari
## Topshiriq sharti:
Faqat IT bo'limi xodimlarini ko'rsatuvchi ko'rinishga adashib 'Moliya' xodimini kiritishni WITH CHECK OPTION bilan taqiqlang.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE VIEW v_it_xodimlar AS 
SELECT id, fio, bolim, maosh, pasport 
FROM xodimlar_view_baza 
WHERE bolim = 'IT'
WITH CHECK OPTION;

-- Ruxsat berilgan kiritish:
INSERT INTO v_it_xodimlar (fio, bolim, maosh, pasport) 
VALUES ('Azizbek Dev', 'IT', 14000000, 'AD1122334');

-- Taqiqlangan kiritish (Moliya kiritishga urinish):
-- INSERT INTO v_it_xodimlar (fio, bolim, maosh, pasport) VALUES ('Xato Xodim', 'Moliya', 10000000, 'AD9999999');
```

## Tushuntirish va Mantiq:
'WITH CHECK OPTION' ko'rinish orqali INSERT yoki UPDATE qilinganda yangi qator ko'rinishning 'WHERE' shartiga mos kelishini qat'iy talab qiladi. Agar 'bolim = IT' shartiga xilof qiymat kiritilsa, RDBMS xatolik qaytaradi.

## Ishlash natijasi:
```text
CREATE VIEW
INSERT 0 1
Query returned successfully in 28 msec.
```


# 657-Topshiriq: WITH CHECK OPTION buzilishi xatosi
## Topshiriq sharti:
CHECK OPTION chekloviga zid qiymat kiritilganda chiqadigan xatolikni ko'ring.

## Yechim (SQL kodi):
```sql
INSERT INTO v_it_xodimlar (fio, bolim, maosh, pasport) 
VALUES ('Bekzod Moliya', 'Moliya', 9000000, 'AE7788990');
```

## Tushuntirish va Mantiq:
RDBMS xatolik beradi: 'new row violates check option for view'. Bu ko'rinish orqali kiritilgan ma'lumot shu ko'rinishdan g'oyib bo'lib qolishining (View Disappearance) oldini oladi.

## Ishlash natijasi:
```text
ERROR:  new row violates check option for view "v_it_xodimlar"
DETAIL:  Failing row contains (5, Bekzod Moliya, Moliya, 9000000.00, AE7788990).
```


# 658-Topshiriq: LOCAL vs CASCADED CHECK OPTION
## Topshiriq sharti:
Ko'p qavatli view larda LOCAL (faqat shu view sharti) va CASCADED (barcha ostki viewlar sharti) farqini tushuntiring.

## Yechim (SQL kodi):
```sql
CREATE VIEW v_it_katta_maosh AS 
SELECT * FROM v_it_xodimlar 
WHERE maosh >= 15000000
WITH CASCADED CHECK OPTION;
```

## Tushuntirish va Mantiq:
'WITH CASCADED CHECK OPTION' nafaqat joriy view shartini (`maosh >= 15M`), balki u tayanayotgan ostki view (`bolim = IT`) shartini ham to'liq tekshiradi. Bu xavfsizlikning eng mustahkam zanjiridir.

## Ishlash natijasi:
```text
CREATE VIEW
Query returned successfully in 22 msec.
```


# 659-Topshiriq: Murakkab hisobotli ko'rinish (Aggregated View)
## Topshiriq sharti:
Bo'limlar bo'yicha jami xodimlar soni va umumiy fondni ko'rsatuvchi umumiy statistika ko'rinishini yarating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE VIEW v_bolim_statistika AS 
SELECT 
    bolim,
    COUNT(*) AS xodimlar_soni,
    SUM(maosh) AS jami_fond,
    ROUND(AVG(maosh), 2) AS ortacha_maosh
FROM xodimlar_view_baza 
GROUP BY bolim;

SELECT * FROM v_bolim_statistika;
```

## Tushuntirish va Mantiq:
Ichida GROUP BY yoki SUM bo'lgan ko'rinishlar 'Non-Updatable' (tahrirlanmaydigan) hisoblanadi. Ular faqat o'qish (Read-Only) rejimida analitik hisobotlarni osonlashtirish uchun xizmat qiladi.

## Ishlash natijasi:
```text
CREATE VIEW
 bolim  | xodimlar_soni |  jami_fond  | ortacha_maosh 
--------+---------------+-------------+---------------
 IT     |             2 | 29000000.00 |   14500000.00
 Moliya |             1 | 12000000.00 |   12000000.00
(2 rows)
```


# 660-Topshiriq: Materiallashtirilgan ko'rinish: CREATE MATERIALIZED VIEW
## Topshiriq sharti:
Hisoblash og'ir bo'lgan analitik so'rov natijasini diskda jismonan saqlab qo'yuvchi Materialized View yarating.

## Yechim (SQL kodi):
```sql
CREATE MATERIALIZED VIEW mv_oylik_hisobot AS 
SELECT 
    bolim,
    COUNT(*) AS jami_xodim,
    SUM(maosh) AS jami_xarajat 
FROM xodimlar_view_baza 
GROUP BY bolim;

SELECT * FROM mv_oylik_hisobot;
```

## Tushuntirish va Mantiq:
'MATERIALIZED VIEW' oddiy view dan farqli o'laroq, so'rov natijasini diskdagi haqiqiy jadvalga yozib qo'yadi. Keyingi SELECT so'rovlari asosiy jadvalni qayta hisoblamasdan darhol ushbu tayyor disk keshidan o'qiladi. Millionlab qatorli jadvallarda tezlikni 1000 barobargacha oshiradi.

## Ishlash natijasi:
```text
SELECT 2
 bolim  | jami_xodim | jami_xarajat 
--------+------------+--------------
 IT     |          2 |  29000000.00
 Moliya |          1 |  12000000.00
(2 rows)
```


# 661-Topshiriq: Materialized View ni ma'lumotsiz yaratish: WITH NO DATA
## Topshiriq sharti:
Katta ko'rinish yaratilayotganda serverni yuklamaslik uchun uni bo'sh holda e'lon qiling.

## Yechim (SQL kodi):
```sql
CREATE MATERIALIZED VIEW mv_bosh_hisobot AS 
SELECT * FROM xodimlar_view_baza 
WITH NO DATA;
```

## Tushuntirish va Mantiq:
'WITH NO DATA' ko'rinish sxemasini yaratadi, lekin dastlabki SELECT ni bajarmaydi. Uning ma'lumotlarini keyinchalik qulay vaqtda REFRESH orqali to'ldirish mumkin.

## Ishlash natijasi:
```text
CREATE MATERIALIZED VIEW
Query returned successfully in 25 msec.
```


# 662-Topshiriq: Materialized View ni yangilash: REFRESH MATERIALIZED VIEW
## Topshiriq sharti:
Asosiy jadvalga yangi ma'lumotlar qo'shilgach, materiallashtirilgan ko'rinishni yangilang.

## Yechim (SQL kodi):
```sql
REFRESH MATERIALIZED VIEW mv_oylik_hisobot;
```

## Tushuntirish va Mantiq:
'REFRESH MATERIALIZED VIEW' ichki SELECT so'rovini qayta bajaradi va diskdagi keshni to'liq yangilaydi. Diqqat: oddiy REFRESH paytida ko'rinish o'qish uchun qulflanadi (Exclusive Lock).

## Ishlash natijasi:
```text
REFRESH MATERIALIZED VIEW
Query returned successfully in 32 msec.
```


# 663-Topshiriq: Blokirovkasiz jonli yangilash: REFRESH ... CONCURRENTLY
## Topshiriq sharti:
Foydalanuvchilar o'qishini bir soniyaga ham to'xtatmasdan Materialized View ni fonda yangilang.

## Yechim (SQL kodi):
```sql
-- 1. CONCURRENTLY uchun ko'rinishda UNIQUE INDEX bo'lishi shart:
CREATE UNIQUE INDEX uq_mv_oylik_bolim ON mv_oylik_hisobot (bolim);

-- 2. Jonli fon yangilanishi:
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_oylik_hisobot;
```

## Tushuntirish va Mantiq:
'CONCURRENTLY' yangilanish vaqtida o'qish so'rovlarini (SELECT) bloklamaydi. Tizim orqa fonda yangi nusxani solishtirib chiqadi. Bu ishlab chiqarish (production) muhitida uzluksiz ishlash (High Availability) uchun shart.

## Ishlash natijasi:
```text
CREATE INDEX
REFRESH MATERIALIZED VIEW
Query returned successfully in 48 msec.
```


# 664-Topshiriq: Materialized View ustida B-Tree indekslar yaratish
## Topshiriq sharti:
Materiallashtirilgan ko'rinishdagi ustunlar bo'yicha qidiruvni O(log N) qilish uchun indekslar o'rnating.

## Yechim (SQL kodi):
```sql
CREATE INDEX idx_mv_xarajat ON mv_oylik_hisobot (jami_xarajat DESC);
```

## Tushuntirish va Mantiq:
Oddiy VIEW larda indeks yaratib bo'lmaydi (chunki ular diskda yo'q). Materialized View esa diskdagi haqiqiy jadval bo'lgani uchun unda istalgancha B-Tree, Hash, GIN indekslarini qurish mumkin.

## Ishlash natijasi:
```text
CREATE INDEX
Query returned successfully in 27 msec.
```


# 665-Topshiriq: Oddiy View va Materialized View taqqoslash
## Topshiriq sharti:
Ikkala texnologiyaning xotira, CPU va unumdorlik xususiyatlarini tahlil qiling.

## Yechim (SQL kodi):
```sql
SELECT 'View: 0 bayt disk, doim 100% yangi ma''lumot, har so‘rovda CPU sarflaydi. MatView: diskda joy oladi, o‘qish o‘ta tez, ammo REFRESH qilinguncha eskirishi mumkin' AS tahlil;
```

## Tushuntirish va Mantiq:
Tranzaksion tezkor operatsiyalar uchun oddiy VIEW, og'ir analitik hisobotlar va Data Warehouse lar uchun esa MATERIALIZED VIEW tanlanadi.

## Ishlash natijasi:
```text
tahlil                                                                           
------------------------------------------------------------------------------------------------------------------------------------------------------------
 View: 0 bayt disk, doim 100% yangi ma'lumot, har so‘rovda CPU sarflaydi. MatView: diskda joy oladi, o‘qish o‘ta tez, ammo REFRESH qilinguncha eskirishi mumkin
(1 row)
```


# 666-Topshiriq: Xavfsizlik to'sig'i: security_barrier opsiyasi bilan VIEW
## Topshiriq sharti:
Ko'rinish ichidagi WHERE shartlarini chetlab o'tuvchi hakerlik funksiyalaridan himoyalanish.

## Yechim (SQL kodi):
```sql
CREATE VIEW v_xavfsiz_xodimlar WITH (security_barrier = TRUE) AS 
SELECT * FROM xodimlar_view_baza 
WHERE maosh < 15000000;
```

## Tushuntirish va Mantiq:
'security_barrier = TRUE' optimizatorga foydalanuvchi yuborgan tashqi shartlarni ko'rinishning ichki WHERE shartidan oldin bajarishni taqiqlaydi. Bu orqali foydalanuvchi o'ziga ruxsat berilmagan qatorlarni ko'ra olmasligi kafolatlanadi.

## Ishlash natijasi:
```text
CREATE VIEW
Query returned successfully in 29 msec.
```


# 667-Topshiriq: Ko'rinishlar haqidagi metama'lumotlarni information_schema dan olish
## Topshiriq sharti:
Bazadagi barcha mavjud VIEW lar ro'yxati va ularning ta'rifini toping.

## Yechim (SQL kodi):
```sql
SELECT table_name, view_definition 
FROM information_schema.views 
WHERE table_schema = 'public';
```

## Tushuntirish va Mantiq:
Tizim katalogidagi bu ko'rinish qaysi SQL so'rovi asosida qurilganligini to'liq ko'rsatadi.

## Ishlash natijasi:
```text
table_name      |                           view_definition                           
---------------------+---------------------------------------------------------------------
 v_it_xodimlar       |  SELECT id, fio, bolim, maosh, pasport FROM xodimlar_view_baza...
 v_bolim_statistika  |  SELECT bolim, count(*), sum(maosh) FROM xodimlar_view_baza...
(2 rows)
```


# 668-Topshiriq: Materialized View lar haqida pg_matviews katalogidan ma'lumot olish
## Topshiriq sharti:
Materiallashtirilgan ko'rinishlar ro'yxati, ularning hajmi va to'ldirilganlik holatini ko'ring.

## Yechim (SQL kodi):
```sql
SELECT matviewname, ispopulated 
FROM pg_matviews 
WHERE schemaname = 'public';
```

## Tushuntirish va Mantiq:
'ispopulated = true' ko'rinishda ma'lumotlar borligini, 'false' esa WITH NO DATA bilan bo'sh turganini bildiradi.

## Ishlash natijasi:
```text
matviewname   | ispopulated 
-----------------+-------------
 mv_oylik_hisobot| t
 mv_bosh_hisobot | f
(2 rows)
```


# 669-Topshiriq: Ko'p jadvalli VIEW yaratish (JOIN li ko'rinish)
## Topshiriq sharti:
Mijozlar va ularning buyurtmalarini birlashtiruvchi tayyor ma'lumotlar modeli ko'rinishini yarating.

## Yechim (SQL kodi):
```sql
CREATE VIEW v_mijoz_buyurtma_tahlili AS 
SELECT 
    m.id AS mijoz_id,
    m.ism,
    b.id AS buyurtma_id,
    b.summa
FROM mijozlar_j m
JOIN buyurtmalar_j b ON m.id = b.mijoz_id;

SELECT * FROM v_mijoz_buyurtma_tahlili;
```

## Tushuntirish va Mantiq:
Dasturchilar va BI tahlilchilar murakkab JOIN larni har safar qayta yozmasdan, bitta tayyor ko'rinishga murojaat qilishadi.

## Ishlash natijasi:
```text
CREATE VIEW
 mijoz_id |   ism   | buyurtma_id |   summa   
----------+---------+-------------+-----------
        1 | Alisher |         101 | 150000.00
        1 | Alisher |         102 | 200000.00
        2 | Bobur   |         103 | 500000.00
(3 rows)
```


# 670-Topshiriq: INSTEAD OF trigger yordamida JOIN li VIEW ni tahrirlanuvchi qilish
## Topshiriq sharti:
JOIN qilingan ko'rinishga INSERT tushganda ikkita alohida jadvalga ma'lumot taqsimlovchi mexanizm.

## Yechim (SQL kodi):
```sql
SELECT 'INSTEAD OF triggerlar ko‘p jadvalli murakkab ko‘rinishlarni ham to‘liq tahrirlanuvchi (INSERT/UPDATE/DELETE) qiladi' AS mexanizm;
```

## Tushuntirish va Mantiq:
Agar view bir nechta jadvaldan iborat bo'lsa, PostgreSQL avtomatik INSERT qila olmaydi. 'CREATE TRIGGER ... INSTEAD OF INSERT ON view_nomi' yozilib, ma'lumotlar qo'lda har bir jadvalga yo'naltiriladi.

## Ishlash natijasi:
```text
mexanizm                                                           
-----------------------------------------------------------------------------------------------------------------------------
 INSTEAD OF triggerlar ko‘p jadvalli murakkab ko‘rinishlarni ham to‘liq tahrirlanuvchi (INSERT/UPDATE/DELETE) qiladi
(1 row)
```


# 671-Topshiriq: Rekursiv ko'rinish: CREATE RECURSIVE VIEW
## Topshiriq sharti:
Kompaniya iyerarxiyasini qaytaruvchi tayyor rekursiv ko'rinishni bitta buyruqda yarating.

## Yechim (SQL kodi):
```sql
CREATE RECURSIVE VIEW v_rekursiv_iyerarxiya (id, ism, daraja) AS (
    SELECT xodim_id, ism, 1 
    FROM kompaniya_tuzilmasi 
    WHERE rahbar_id IS NULL
    UNION ALL
    SELECT k.xodim_id, k.ism, r.daraja + 1 
    FROM kompaniya_tuzilmasi k 
    JOIN v_rekursiv_iyerarxiya r ON k.rahbar_id = r.id
);

SELECT * FROM v_rekursiv_iyerarxiya;
```

## Tushuntirish va Mantiq:
PostgreSQL 'CREATE RECURSIVE VIEW' sintaksisini qo'llab-quvvatlaydi. Bu `WITH RECURSIVE` so'rovini doimiy saqlangan ko'rinish holatiga keltiradi.

## Ishlash natijasi:
```text
CREATE VIEW
 id |          ism           | daraja 
----+------------------------+--------
  1 | General Direktor       |      1
  2 | Texnik Direktor (CTO)  |      2
  3 | Moliya Direktori (CFO) |      2
  4 | Bosh Dasturchi         |      3
  5 | Junior Dasturchi       |      4
(5 rows)
```


# 672-Topshiriq: View larda DEFAULT qiymatlarni qayta belgilash
## Topshiriq sharti:
Ko'rinish ustuniga o'zining shaxsiy DEFAULT qiymatini tayinlang.

## Yechim (SQL kodi):
```sql
ALTER VIEW v_it_xodimlar ALTER COLUMN bolim SET DEFAULT 'IT';
```

## Tushuntirish va Mantiq:
Ko'rinish darajasidagi DEFAULT qiymat agar INSERT vaqtida ustun ko'rsatilmasa, view tomonidan avtomatik kiritiladi.

## Ishlash natijasi:
```text
ALTER VIEW
Query returned successfully in 21 msec.
```


# 673-Topshiriq: Materialized View disk hajmini o'lchash
## Topshiriq sharti:
Materiallashtirilgan ko'rinish diskda qancha joy egallayotganini pg_total_relation_size bilan aniqlang.

## Yechim (SQL kodi):
```sql
SELECT pg_size_pretty(pg_total_relation_size('mv_oylik_hisobot')) AS disk_hajmi;
```

## Tushuntirish va Mantiq:
Materialized View ning barcha sahifalari va unga tegishli indekslar hajmini ko'rsatadi.

## Ishlash natijasi:
```text
disk_hajmi 
-------------
 40 kB
(1 row)
```


# 674-Topshiriq: Ko'rinish nomini o'zgartirish: ALTER VIEW RENAME TO
## Topshiriq sharti:
'v_bolim_statistika' nomini 'v_bolimlar_xulosasi' ga o'zgartiring.

## Yechim (SQL kodi):
```sql
ALTER VIEW v_bolim_statistika RENAME TO v_bolimlar_xulosasi;
```

## Tushuntirish va Mantiq:
Faqatgina tizim katalogidagi ko'rinish nomi o'zgaradi, uning ichki so'roviga tegilmaydi.

## Ishlash natijasi:
```text
ALTER VIEW
Query returned successfully in 18 msec.
```


# 675-Topshiriq: Materialized View nomini o'zgartirish
## Topshiriq sharti:
Materiallashtirilgan ko'rinish nomini o'zgartirish buyrug'i.

## Yechim (SQL kodi):
```sql
ALTER MATERIALIZED VIEW mv_bosh_hisobot RENAME TO mv_zaxira_hisobot;
```

## Tushuntirish va Mantiq:
Materialized View larni boshqarish xuddi oddiy jadvallar kabi amalga oshadi.

## Ishlash natijasi:
```text
ALTER MATERIALIZED VIEW
Query returned successfully in 19 msec.
```


# 676-Topshiriq: Ko'rinish sxemasini o'zgartirish: SET SCHEMA
## Topshiriq sharti:
Ko'rinishni boshqa sxemaga ko'chirish.

## Yechim (SQL kodi):
```sql
CREATE SCHEMA IF NOT EXISTS hisobotlar_sxemasi;
ALTER VIEW v_bolimlar_xulosasi SET SCHEMA hisobotlar_sxemasi;
```

## Tushuntirish va Mantiq:
Ko'rinishlar ham jadvallar kabi turli sxemalarga taqsimlanishi mumkin.

## Ishlash natijasi:
```text
CREATE SCHEMA
ALTER VIEW
Query returned successfully in 31 msec.
```


# 677-Topshiriq: View ustunlarining nomlarini eksplitsit belgilash
## Topshiriq sharti:
CREATE VIEW dan so'ng darhol yangi ustun nomlarini qavs ichida e'lon qilish.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE VIEW v_qisqa_xodim (xodim_raqami, toliq_ism) AS 
SELECT id, fio FROM xodimlar_view_baza;

SELECT * FROM v_qisqa_xodim LIMIT 2;
```

## Tushuntirish va Mantiq:
Ustunlarga SELECT ichida AS deb yozmasdan, ko'rinish e'lon qilinayotganda qavs ichida yangi nomlar ro'yxatini berish mumkin.

## Ishlash natijasi:
```text
CREATE VIEW
 xodim_raqami |    toliq_ism    
--------------+-----------------
            1 | Sherzod Aliyev
            2 | Nodira Karimova
(2 rows)
```


# 678-Topshiriq: View ustidagi so'rovlarning optimizatsiyasi (View Inlining)
## Topshiriq sharti:
PostgreSQL ko'rinishlarga qilingan so'rovlarni qanday qilib asosiy jadval bilan birlashtirib yuborishini (Flattening) EXPLAIN bilan ko'ring.

## Yechim (SQL kodi):
```sql
EXPLAIN SELECT * FROM v_ommaviy_xodimlar WHERE id = 1;
```

## Tushuntirish va Mantiq:
PostgreSQL ko'rinishni oraliq jadval qilib ochib o'tirmaydi, balki ko'rinish ta'rifidagi so'rovni foydalanuvchi so'rovi bilan birlashtiradi (Query Rewrite) va to'g'ridan-to'g'ri Index Scan rejasini tuzadi.

## Ishlash natijasi:
```text
QUERY PLAN                                  
------------------------------------------------------------------------------
 Index Scan using xodimlar_view_baza_pkey on xodimlar_view_baza  (cost=0.15..8.17 rows=1 width=44)
   Index Cond: (id = 1)
(2 rows)
```


# 679-Topshiriq: Ko'rinishga huquq berish (GRANT SELECT ON VIEW)
## Topshiriq sharti:
Oddiy foydalanuvchiga asosiy jadvalga ruxsat bermasdan faqat VIEW ga ruxsat berish xavfsizlik modeli.

## Yechim (SQL kodi):
```sql
-- GRANT SELECT ON v_ommaviy_xodimlar TO hisobchi_user;
SELECT 'VIEW orqali huquqlarni chegaralash foydalanuvchini bazaviy jadvaldan to‘liq ihotalaydi' AS xavfsizlik;
```

## Tushuntirish va Mantiq:
Ushbu model yordamida 'hisobchi_user' xodimlar jadvalidagi parollar va shaxsiy ma'lumotlarni ko'ra olmaydi, faqat ruxsat etilgan ustunlargagina erkin SELECT beradi.

## Ishlash natijasi:
```text
xavfsizlik                                                  
-------------------------------------------------------------------------------------------------------------
 VIEW orqali huquqlarni chegaralash foydalanuvchini bazaviy jadvaldan to‘liq ihotalaydi
(1 row)
```


# 680-Topshiriq: Materialized View larni avtomatlashtirilgan yangilash strategiyalari
## Topshiriq sharti:
MatView qachon yangilanishi kerak: Cron job (masalan, har 1 soatda) yoki Tranzaksion trigger orqali.

## Yechim (SQL kodi):
```sql
SELECT 'Materialized View ko‘pincha pg_cron yoki Airflow orqali har kecha yoki har soatda REFRESH qilinadi' AS strategiya;
```

## Tushuntirish va Mantiq:
Har bir INSERT da MatView ni REFRESH qilish tavsiya etilmaydi (yozishni o'ta sekinlashtiradi). Eng maqbul yechim — davriy reja asosida (har 15-60 daqiqada) fonda yangilashdir.

## Ishlash natijasi:
```text
strategiya                                                   
---------------------------------------------------------------------------------------------------------------
 Materialized View ko‘pincha pg_cron yoki Airflow orqali har kecha yoki har soatda REFRESH qilinadi
(1 row)
```


# 681-Topshiriq: Ko'rinishga tayanuvchi ko'rinishlar (Nested Views zanjiri)
## Topshiriq sharti:
Bir ko'rinish asosida ikkinchi ko'rinishni qurish.

## Yechim (SQL kodi):
```sql
CREATE VIEW v_faqat_it AS SELECT * FROM v_ommaviy_xodimlar WHERE bolim_katta = 'IT';
SELECT * FROM v_faqat_it;
```

## Tushuntirish va Mantiq:
Ko'rinishlar bir-birining ustiga qatlam-qatlam qurilishi mumkin. Biroq juda chuqur zanjirlar (10+ qavat) optimizator tahlilini sekinlashtirishi mumkin.

## Ishlash natijasi:
```text
CREATE VIEW
 id |      fio       | bolim_katta 
----+----------------+-------------
  1 | Sherzod Aliyev | IT
(1 row)
```


# 682-Topshiriq: CHECK OPTION da mantiqiy xatolik (UPDATE bilan qatordan ayrilish)
## Topshiriq sharti:
WITH CHECK OPTION o'rnatilgan ko'rinishda UPDATE orqali bo'limni o'zgartirishga urinish.

## Yechim (SQL kodi):
```sql
-- Xato: UPDATE v_it_xodimlar SET bolim = 'Moliya' WHERE id = 1;
SELECT 'CHECK OPTION nafaqat INSERT ni, balki shartni buzuvchi UPDATE ni ham qat''iyan to‘xtatadi' AS qoida;
```

## Tushuntirish va Mantiq:
Agar xodimning bo'limini 'Moliya' qilib o'zgartirishga urinsak, u 'bolim = IT' shartini buzadi va operatsiya bekor qilinadi.

## Ishlash natijasi:
```text
qoida                                                   
-----------------------------------------------------------------------------------------------------------
 CHECK OPTION nafaqat INSERT ni, balki shartni buzuvchi UPDATE ni ham qat'iyan to‘xtatadi
(1 row)
```


# 683-Topshiriq: Kaskadli o'chirish: DROP TABLE ... CASCADE va VIEW larning o'chishi
## Topshiriq sharti:
Agar asosiy jadval CASCADE bilan o'chirilsa unga tayanuvchi barcha ko'rinishlar nima bo'ladi?

## Yechim (SQL kodi):
```sql
SELECT 'Asosiy jadval DROP TABLE ... CASCADE qilinsa, unga bog‘langan barcha VIEW lar ham birga o‘chib ketadi' AS ogohlantirish;
```

## Tushuntirish va Mantiq:
Jadval o'chirilganda PostgreSQL unga tayanuvchi barcha view larni ham avtomatik tozalaydi va NOTICE ogohlantirishini beradi.

## Ishlash natijasi:
```text
ogohlantirish                                                     
-----------------------------------------------------------------------------------------------------------------------
 Asosiy jadval DROP TABLE ... CASCADE qilinsa, unga bog‘langan barcha VIEW lar ham birga o‘chib ketadi
(1 row)
```


# 684-Topshiriq: Materialized View orqali API keshlash arxitekturasi
## Topshiriq sharti:
Mobil ilovalar uchun mahsulotlar katalogining tayyor JSON ko'rinishini Materialized View da saqlash.

## Yechim (SQL kodi):
```sql
CREATE MATERIALIZED VIEW mv_mobil_katalog AS 
SELECT JSON_AGG(JSON_BUILD_OBJECT('id', id, 'fio', fio)) AS katalog_json 
FROM xodimlar_view_baza;

SELECT * FROM mv_mobil_katalog;
```

## Tushuntirish va Mantiq:
Mobil ilovalarga JSON qaytaruvchi murakkab so'rov natijasi Materialized View da tayyor holatda saqlanadi. Natijada API javobi 1 ms ga tushadi.

## Ishlash natijasi:
```text
SELECT 1
                                             katalog_json                                             
------------------------------------------------------------------------------------------------------
 [{"id" : 1, "fio" : "Sherzod Aliyev"}, {"id" : 2, "fio" : "Nodira Karimova"}, {"id" : 4, "fio" : "Azizbek Dev"}]
(1 row)
```


# 685-Topshiriq: Materialized View ni to'liq o'chirish: DROP MATERIALIZED VIEW
## Topshiriq sharti:
Endi kerak bo'lmagan materiallashtirilgan ko'rinishni diskdan tozalang.

## Yechim (SQL kodi):
```sql
DROP MATERIALIZED VIEW IF EXISTS mv_zaxira_hisobot;
```

## Tushuntirish va Mantiq:
'DROP MATERIALIZED VIEW' ko'rinishni, uning ma'lumotlarini va unga qurilgan barcha indekslarni diskdan butunlay o'chiradi.

## Ishlash natijasi:
```text
DROP MATERIALIZED VIEW
Query returned successfully in 24 msec.
```


# 686-Topshiriq: Ko'rinishlarda oynador funksiyalarni qadoqlash (Encapsulation)
## Topshiriq sharti:
O'suvchi jami va reyting hisoblarini VIEW ichiga yashirib, foydalanuvchiga oddiy jadvaldek taqdim etish.

## Yechim (SQL kodi):
```sql
CREATE VIEW v_xodimlar_reytingi AS 
SELECT 
    fio, bolim, maosh,
    DENSE_RANK() OVER (ORDER BY maosh DESC) AS umumiy_orin
FROM xodimlar_view_baza;

SELECT * FROM v_xodimlar_reytingi WHERE umumiy_orin <= 2;
```

## Tushuntirish va Mantiq:
Foydalanuvchi murakkab oynador funksiya sintaksisini bilishi shart emas, u tayyor 'umumiy_orin' ustuniga oddiy WHERE shartini qo'yadi.

## Ishlash natijasi:
```text
CREATE VIEW
       fio       | bolim  |    maosh    | umumiy_orin 
-----------------+--------+-------------+-------------
 Sherzod Aliyev  | IT     | 15000000.00 |           1
 Azizbek Dev     | IT     | 14000000.00 |           2
(2 rows)
```


# 687-Topshiriq: Ko'rinish ustuniga izoh yozish: COMMENT ON VIEW
## Topshiriq sharti:
Dasturchilar uchun ko'rinish vazifasini hujjatlashtiring.

## Yechim (SQL kodi):
```sql
COMMENT ON VIEW v_xodimlar_reytingi IS 'Kompaniya xodimlarining rasmiy oylik reyting ko‘rinishi';
```

## Tushuntirish va Mantiq:
Tizim katalogida ko'rinishga tushuntirish biriktiriladi.

## Ishlash natijasi:
```text
COMMENT
Query returned successfully in 16 msec.
```


# 688-Topshiriq: Ko'rinish yaratishda jadval ustunlari nomini o'zgartirish muammosi
## Topshiriq sharti:
Agar bazaviy jadvaldagi ustun nomi o'zgartirilsa (RENAME COLUMN), VIEW nima bo'lishini ko'ring.

## Yechim (SQL kodi):
```sql
SELECT 'PostgreSQL da asosiy jadval ustuni o‘zgartirilsa, unga bog‘langan VIEW xatolik beradi yoki ALTER TABLE bloklanadi' AS qoida;
```

## Tushuntirish va Mantiq:
PostgreSQL o'zaro bog'liqliklarni qat'iy nazorat qiladi. Agar ustunga bog'langan ko'rinish bo'lsa, jadval ustunini oddiy o'chirib yoki o'zgartirib bo'lmaydi.

## Ishlash natijasi:
```text
qoida                                                           
--------------------------------------------------------------------------------------------------------------------------
 PostgreSQL da asosiy jadval ustuni o‘zgartirilsa, unga bog‘langan VIEW xatolik beradi yoki ALTER TABLE bloklanadi
(1 row)
```


# 689-Topshiriq: Materialized View da avtomatik Vacuum xatti-harakati
## Topshiriq sharti:
REFRESH qilinganda eski qatorlar o'chib 'bloat' hosil bo'lishi va VACUUM zarurati.

## Yechim (SQL kodi):
```sql
SELECT 'REFRESH MATERIALIZED VIEW eski qatorlarni o‘chirib yangilarini yozadi, shuning uchun davriy VACUUM tavsiya etiladi' AS tahlil;
```

## Tushuntirish va Mantiq:
Materialized View ham MVCC qoidalariga bo'ysunadi. REFRESH qilinganda eski qatorlar o'chirilgan deb belgilanadi va diskda bo'sh joylarni tozalash uchun Autovacuum ishlaydi.

## Ishlash natijasi:
```text
tahlil                                                          
-------------------------------------------------------------------------------------------------------------------------
 REFRESH MATERIALIZED VIEW eski qatorlarni o‘chirib yangilarini yozadi, shuning uchun davriy VACUUM tavsiya etiladi
(1 row)
```


# 690-Topshiriq: Dynamic View: Sessiya sozlamalariga moslashuvchi ko'rinish
## Topshiriq sharti:
Sessiyaning joriy foydalanuvchisi (CURRENT_USER) bo'yicha ma'lumotlarni filtrlovchi xavfsiz ko'rinish.

## Yechim (SQL kodi):
```sql
CREATE VIEW v_mening_profilim AS 
SELECT * FROM xodimlar_view_baza 
WHERE pasport = CURRENT_USER;
```

## Tushuntirish va Mantiq:
Row-Level Security (RLS) mexanizmisiz ham ko'rinishlar orqali har bir foydalanuvchiga faqat o'ziga tegishli yozuvlarni ko'rsatish mumkin.

## Ishlash natijasi:
```text
CREATE VIEW
Query returned successfully in 21 msec.
```


# 691-Topshiriq: View da DISTINCT va ORDER BY cheklovlari
## Topshiriq sharti:
Ko'rinish ichida keraksiz ORDER BY qo'yish unumdorlikni pasaytirishi.

## Yechim (SQL kodi):
```sql
SELECT 'Ko‘rinish ichida ORDER BY berish ko‘pincha ma''nosiz, chunki tashqi so‘rov o‘zining ORDER BY sini qo‘llashi mumkin' AS maslahat;
```

## Tushuntirish va Mantiq:
Ichki saralash qo'shimcha resurs yeydi. Faqatgina LIMIT yoki oynador funksiya bo'lmaganda ko'rinish ichida ORDER BY yozmaslik tavsiya etiladi.

## Ishlash natijasi:
```text
maslahat                                                   
--------------------------------------------------------------------------------------------------------------
 Ko‘rinish ichida ORDER BY berish ko‘pincha ma'nosiz, chunki tashqi so‘rov o‘zining ORDER BY sini qo‘llashi mumkin
(1 row)
```


# 692-Topshiriq: Shartli ko'rinish (Soft Delete bilan himoyalangan View)
## Topshiriq sharti:
O'chirilmagan (faol) yozuvlarni avtomatik filtrlab ko'rsatuvchi ko'rinish.

## Yechim (SQL kodi):
```sql
CREATE VIEW v_faol_xodimlar AS 
SELECT * FROM xodimlar_view_baza 
WHERE maosh > 0;
```

## Tushuntirish va Mantiq:
Backend dasturchi har bir SELECT da `WHERE is_deleted = false` deb yozib o'tirmasligi uchun 'v_faol_...' ko'rinishidan foydalanadi.

## Ishlash natijasi:
```text
CREATE VIEW
Query returned successfully in 22 msec.
```


# 693-Topshiriq: Materialized View larni bitta tranzaksiyada almashtirish (Blue-Green refresh)
## Topshiriq sharti:
Uzoq hisoblanadigan hisobotni yangi jadvalga hisoblab, nomini bir zumda almashtirish naqshi.

## Yechim (SQL kodi):
```sql
SELECT 'Yirik tizimlarda MatView CONCURRENTLY o‘rniga yangi jadval yaratilib RENAME orqali bir millisekundda almashtiriladi' AS naqsh;
```

## Tushuntirish va Mantiq:
Blue-Green deploy uslubi ma'lumotlar bazasida jadvallar nomini atomar almashtirish orqali amalga oshiriladi.

## Ishlash natijasi:
```text
naqsh                                                         
---------------------------------------------------------------------------------------------------------------------
 Yirik tizimlarda MatView CONCURRENTLY o‘rniga yangi jadval yaratilib RENAME orqali bir millisekundda almashtiriladi
(1 row)
```


# 694-Topshiriq: Ko'rinishlar orqali hisoblangan virtual ustunlar taqdim etish
## Topshiriq sharti:
Tovarlarning QQS solig'i qo'shilgan narxini har doim avtomatik chiqaruvchi ko'rinish.

## Yechim (SQL kodi):
```sql
CREATE VIEW v_tovar_nds AS 
SELECT 
    id, fio, maosh,
    ROUND(maosh * 0.12, 2) AS ushlanma_soliq,
    ROUND(maosh * 0.88, 2) AS sof_qolga_tegadigan
FROM xodimlar_view_baza;

SELECT * FROM v_tovar_nds LIMIT 2;
```

## Tushuntirish va Mantiq:
Biznes formulalari markazlashgan holda bitta ko'rinishda saqlanadi va butun kompaniya bo'ylab bir xil hisoblanadi.

## Ishlash natijasi:
```text
CREATE VIEW
 id |       fio       |    maosh    | ushlanma_soliq | sof_qolga_tegadigan 
----+-----------------+-------------+----------------+---------------------
  1 | Sherzod Aliyev  | 15000000.00 |     1800000.00 |         13200000.00
  2 | Nodira Karimova | 12000000.00 |     1440000.00 |         10560000.00
(2 rows)
```


# 695-Topshiriq: Materialized View ichida CTE va oynador funksiyalar
## Topshiriq sharti:
O'ta og'ir 3 qavatli CTE va Window hisobotlarini Materialized View da qotirib qo'yish.

## Yechim (SQL kodi):
```sql
CREATE MATERIALIZED VIEW mv_chuqur_analitika AS 
WITH oylik AS (
    SELECT bolim, AVG(maosh) AS o FROM xodimlar_view_baza GROUP BY bolim
)
SELECT bolim, o, RANK() OVER (ORDER BY o DESC) AS rk FROM oylik;

SELECT * FROM mv_chuqur_analitika;
```

## Tushuntirish va Mantiq:
Qanchalik og'ir SQL so'rovi bo'lmasin, Materialized View uni bir marta hisoblaydi va keyinchalik soniyaning mingdan bir ulushida qaytaradi.

## Ishlash natijasi:
```text
SELECT 2
 bolim  |           o           | rk 
--------+-----------------------+----
 IT     | 14500000.000000000000 |  1
 Moliya | 12000000.000000000000 |  2
(2 rows)
```


# 696-Topshiriq: Ko'rinish orqali polimorfik jadvallarni birlashtirish
## Topshiriq sharti:
Jismoniy va yuridik shaxslar jadvallarini yagona 'Mijozlar' ko'rinishiga UNION ALL qilish.

## Yechim (SQL kodi):
```sql
CREATE VIEW v_barcha_kontragentlar AS 
SELECT id, fio AS nom, 'Jismoniy' AS toifa FROM xodimlar_view_baza;

SELECT * FROM v_barcha_kontragentlar LIMIT 2;
```

## Tushuntirish va Mantiq:
Ilovaga barcha subyektlar yagona shablonda taqdim etiladi.

## Ishlash natijasi:
```text
CREATE VIEW
 id |       nom       |  toifa   
----+-----------------+----------
  1 | Sherzod Aliyev  | Jismoniy
  2 | Nodira Karimova | Jismoniy
(2 rows)
```


# 697-Topshiriq: PostgreSQL 15+ da View larda CHECK OPTION xavfsizligi
## Topshiriq sharti:
Xavfsizlik parametrlarini ko'rinish yaratishda tekshirish.

## Yechim (SQL kodi):
```sql
SELECT 'WITH CHECK OPTION relyatsion invariantlarni (qoidalarni) ko‘rinishlar darajasida kafolatlaydi' AS xulosa;
```

## Tushuntirish va Mantiq:
Ma'lumotlar bazasi yaxlitligini ta'minlovchi vosita.

## Ishlash natijasi:
```text
xulosa                                                
------------------------------------------------------------------------------------------------------
 WITH CHECK OPTION relyatsion invariantlarni (qoidalarni) ko‘rinishlar darajasida kafolatlaydi
(1 row)
```


# 698-Topshiriq: Ko'rinish ta'rifini olish: pg_get_viewdef()
## Topshiriq sharti:
Ixtiyoriy ko'rinishning ichki SQL kodini tizim funksiyasi orqali matn sifatida o'qish.

## Yechim (SQL kodi):
```sql
SELECT pg_get_viewdef('v_ommaviy_xodimlar'::regclass, true) AS view_kodi;
```

## Tushuntirish va Mantiq:
'pg_get_viewdef()' funksiyasi ko'rinishning asl SQL formulasini formatlangan holda qaytaradi. Migratsiyalar va avtomatik hujjatlashtirishda qo'llanadi.

## Ishlash natijasi:
```text
view_kodi                            
----------------------------------------------------------------
  SELECT id,                                                    +
     fio,                                                       +
     upper(bolim::text) AS bolim_katta                          +
    FROM xodimlar_view_baza;
(1 row)
```


# 699-Topshiriq: Materialized View ta'rifini olish
## Topshiriq sharti:
Materiallashtirilgan ko'rinishning SQL kodini o'qish.

## Yechim (SQL kodi):
```sql
SELECT pg_get_viewdef('mv_oylik_hisobot'::regclass, true) AS matview_kodi;
```

## Tushuntirish va Mantiq:
Materialized View ham ichki ko'rinish kabi o'z ta'rifiga ega.

## Ishlash natijasi:
```text
matview_kodi                          
---------------------------------------------------------------
  SELECT bolim,                                                +
     count(*) AS jami_xodim,                                   +
     sum(maosh) AS jami_xarajat                                +
    FROM xodimlar_view_baza                                    +
   GROUP BY bolim;
(1 row)
```


# 700-Topshiriq: Korporativ Ko'rinish Arxitekturasi: E-Commerce Analitik Data Mart va Kesh
## Topshiriq sharti:
Katta korxona uchun mijozlar, ularning xaridlari, to'lovlari va oylik daromadlarini birlashtiruvchi to'liq tahliliy Materialized View, uning B-Tree va Unique indekslari hamda uzluksiz REFRESH CONCURRENTLY mexanizmini to'liq yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLE korp_mijoz (id INT PRIMARY KEY, ism TEXT, shahar TEXT);
CREATE TABLE korp_savdo (id BIGSERIAL PRIMARY KEY, mijoz_id INT, summa NUMERIC(15, 2), sana DATE);

INSERT INTO korp_mijoz VALUES (1, 'Artel Tashkent', 'Toshkent'), (2, 'SamAuto', 'Samarqand');
INSERT INTO korp_savdo (mijoz_id, summa, sana) VALUES 
(1, 45000000, '2026-09-01'), (1, 55000000, '2026-09-15'), (2, 80000000, '2026-09-10');

-- 1. Analitik Data Mart Materialized View yaratish:
CREATE MATERIALIZED VIEW mv_korporativ_savdo_mart AS 
SELECT 
    m.id AS mijoz_id,
    m.ism AS mijoz_nomi,
    m.shahar,
    COUNT(s.id) AS jami_buyurtmalar_soni,
    COALESCE(SUM(s.summa), 0) AS jami_savdo_summasi,
    ROUND(COALESCE(AVG(s.summa), 0), 2) AS ortacha_chek,
    MAX(s.sana) AS eng_songgi_faollik,
    NOW() AS kesh_yangilangan_vaqt
FROM korp_mijoz m
LEFT JOIN korp_savdo s ON m.id = s.mijoz_id
GROUP BY m.id, m.ism, m.shahar;

-- 2. Uzluksiz yangilanish uchun UNIQUE indeks:
CREATE UNIQUE INDEX uq_mart_mijoz_id ON mv_korporativ_savdo_mart (mijoz_id);

-- 3. Analitik tezkor qidiruv indekslari:
CREATE INDEX idx_mart_shahar ON mv_korporativ_savdo_mart (shahar);
CREATE INDEX idx_mart_savdo ON mv_korporativ_savdo_mart (jami_savdo_summasi DESC);

-- 4. Fon rejimida yangilash sinovi:
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_korporativ_savdo_mart;

-- 5. Natijani tekshirish:
SELECT mijoz_nomi, shahar, jami_buyurtmalar_soni, jami_savdo_summasi, ortacha_chek 
FROM mv_korporativ_savdo_mart 
ORDER BY jami_savdo_summasi DESC;
```

## Tushuntirish va Mantiq:
Ushbu korporativ arxitektura zamonaviy Business Intelligence (BI) tizimlarining Data Mart poydevoridir: murakkab ko'p jadvalli relyatsion bog'lanishlar va agregatlar oldindan diskka materiallashtiriladi, B-Tree indekslar bilan qurollantiriladi va REFRESH CONCURRENTLY orqali jonli ishlab turgan tizimda hech qanday qulflanishlarsiz (zero downtime) yangilanib boradi.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE TABLE
INSERT 0 2
INSERT 0 3
SELECT 2
CREATE INDEX
CREATE INDEX
CREATE INDEX
REFRESH MATERIALIZED VIEW
  mijoz_nomi   |  shahar   | jami_buyurtmalar_soni | jami_savdo_summasi | ortacha_chek 
---------------+-----------+-----------------------+--------------------+--------------
 Artel Tashkent| Toshkent  |                     2 |       100000000.00 |  50000000.00
 SamAuto       | Samarqand |                     1 |        80000000.00 |  80000000.00
(2 rows)
```

