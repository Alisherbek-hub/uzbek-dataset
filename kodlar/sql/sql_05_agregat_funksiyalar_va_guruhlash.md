# 201-Topshiriq: Qatorlarning umumiy sonini hisoblash: COUNT(*)
## Topshiriq sharti:
Tizimda jami nechta xodim ro'yxatdan o'tganini aniqlash so'rovini yozing.

## Yechim (SQL kodi):
```sql
CREATE TABLE xodimlar_agg (
    id SERIAL PRIMARY KEY,
    ism VARCHAR(50),
    bolim VARCHAR(50),
    maosh NUMERIC(12, 2),
    shahar VARCHAR(50)
);

INSERT INTO xodimlar_agg (ism, bolim, maosh, shahar) VALUES 
('Anvar', 'IT', 12000000, 'Toshkent'),
('Malika', 'IT', 15000000, 'Toshkent'),
('Bobur', 'Moliya', 9000000, 'Samarqand'),
('Dildora', 'Moliya', NULL, 'Toshkent'),
('Jasur', 'Marketing', 7500000, 'Buxoro');

SELECT COUNT(*) AS jami_xodimlar 
FROM xodimlar_agg;
```

## Tushuntirish va Mantiq:
'COUNT(*)' jadvaldagi barcha qatorlar sonini hisoblaydi, qatorlardagi ustunlar NULL yoki NULL emasligiga qaramaydi. Bu to'liq hajm hisobidir.

## Ishlash natijasi:
```text
jami_xodimlar 
----------------
              5
(1 row)
```


# 202-Topshiriq: Ustun bo'yicha COUNT: COUNT(*) va COUNT(ustun) farqi
## Topshiriq sharti:
Maoshi ko'rsatilgan xodimlar sonini 'COUNT(maosh)' orqali hisoblab, COUNT(*) bilan farqini ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT 
    COUNT(*) AS jami_qatorlar,
    COUNT(maosh) AS maoshi_borlar_soni 
FROM xodimlar_agg;
```

## Tushuntirish va Mantiq:
'COUNT(ustun_nomi)' faqat NULL bo'lmagan qiymatlarni hisoblaydi. Dildoraning maoshi NULL bo'lgani uchun 'COUNT(maosh)' 4 natijasini qaytaradi.

## Ishlash natijasi:
```text
jami_qatorlar | maoshi_borlar_soni 
---------------+--------------------
             5 |                  4
(1 row)
```


# 203-Topshiriq: Noyob qiymatlarni hisoblash: COUNT(DISTINCT ustun)
## Topshiriq sharti:
Kompaniyada jami nechta har xil bo'lim mavjudligini aniqlang.

## Yechim (SQL kodi):
```sql
SELECT COUNT(DISTINCT bolim) AS noyob_bolimlar_soni 
FROM xodimlar_agg;
```

## Tushuntirish va Mantiq:
'COUNT(DISTINCT ustun)' takrorlangan qiymatlarni bir marta hisoblaydi. Bo'limlar orasida 'IT' va 'Moliya' bir nechtadan bo'lsa-da, faqat noyob bo'limlar sanaladi.

## Ishlash natijasi:
```text
noyob_bolimlar_soni 
-----------------------
                     3
(1 row)
```


# 204-Topshiriq: Umumiy yig'indini topish: SUM(ustun)
## Topshiriq sharti:
IT bo'limi xodimlariga to'lanadigan jami oylik maosh fondini hisoblang.

## Yechim (SQL kodi):
```sql
SELECT SUM(maosh) AS it_jami_maosh 
FROM xodimlar_agg 
WHERE bolim = 'IT';
```

## Tushuntirish va Mantiq:
'SUM(ustun)' ko'rsatilgan sonli ustunning barcha qatorlardagi yig'indisini hisoblaydi. Agar ustunlar orasida NULL qiymatlar bo'lsa, SUM ularni e'tiborsiz qoldiradi (ignore qiladi).

## Ishlash natijasi:
```text
it_jami_maosh 
--------------
  27000000.00
(1 row)
```


# 205-Topshiriq: O'rtacha qiymatni hisoblash: AVG(ustun)
## Topshiriq sharti:
Barcha xodimlarning o'rtacha oylik maoshini toping.

## Yechim (SQL kodi):
```sql
SELECT ROUND(AVG(maosh), 2) AS ortacha_maosh 
FROM xodimlar_agg;
```

## Tushuntirish va Mantiq:
'AVG(ustun)' o'rtacha arifmetik qiymatni hisoblaydi: `SUM(maosh) / COUNT(maosh)`. Diqqat: Dildoraning maoshi NULL bo'lgani uchun bo'luvchi 5 emas, 4 bo'ladi!

## Ishlash natijasi:
```text
ortacha_maosh 
---------------
   10875000.00
(1 row)
```


# 206-Topshiriq: Minimal va maksimal qiymatlarni topish: MIN va MAX
## Topshiriq sharti:
Kompaniyadagi eng kam va eng ko'p maosh miqdorlarini bitta so'rovda oling.

## Yechim (SQL kodi):
```sql
SELECT 
    MIN(maosh) AS eng_kam_maosh,
    MAX(maosh) AS eng_kop_maosh 
FROM xodimlar_agg;
```

## Tushuntirish va Mantiq:
'MIN()' eng kichik qiymatni, 'MAX()' eng katta qiymatni qaytaradi. Ular nafaqat sonlar, balki matnlar (alifbo bo'yicha) va sanalar (eng eski va eng yangi sana) ustida ham ishlaydi.

## Ishlash natijasi:
```text
eng_kam_maosh | eng_kop_maosh 
---------------+---------------
    7500000.00 |   15000000.00
(1 row)
```


# 207-Topshiriq: Bitta ustun bo'yicha guruhlash: GROUP BY
## Topshiriq sharti:
Har bir bo'limda nechta xodim ishlayotganini aniqlang.

## Yechim (SQL kodi):
```sql
SELECT bolim, COUNT(*) AS xodimlar_soni 
FROM xodimlar_agg 
GROUP BY bolim;
```

## Tushuntirish va Mantiq:
'GROUP BY' jadvaldagi qatorlarni ko'rsatilgan ustun qiymatlari bo'yicha alohida guruhlarga ajratadi. Har bir guruh uchun alohida COUNT, SUM, AVG hisoblanadi.

## Ishlash natijasi:
```text
bolim   | xodimlar_soni 
-----------+---------------
 IT        |             2
 Marketing |             1
 Moliya    |             2
(3 rows)
```


# 208-Topshiriq: Guruhlashda barcha agregatlarni birga qo'llash
## Topshiriq sharti:
Har bir bo'lim bo'yicha xodimlar soni, jami maosh fondi, o'rtacha maosh va eng katta maoshni chiqaring.

## Yechim (SQL kodi):
```sql
SELECT 
    bolim,
    COUNT(*) AS xodimlar_soni,
    COALESCE(SUM(maosh), 0) AS jami_fond,
    ROUND(COALESCE(AVG(maosh), 0), 2) AS ortacha_maosh,
    COALESCE(MAX(maosh), 0) AS eng_yuqori_maosh
FROM xodimlar_agg 
GROUP BY bolim;
```

## Tushuntirish va Mantiq:
Bitta guruhlash so'rovida turli xil agregat funksiyalarini parallel ravishda hisoblash mumkin. COALESCE NULL qiymatlarni 0 ga aylantirish uchun muhim.

## Ishlash natijasi:
```text
bolim   | xodimlar_soni |  jami_fond   | ortacha_maosh | eng_yuqori_maosh 
-----------+---------------+--------------+---------------+------------------
 IT        |             2 |  27000000.00 |   13500000.00 |      15000000.00
 Marketing |             1 |   7500000.00 |    7500000.00 |       7500000.00
 Moliya    |             2 |   9000000.00 |    9000000.00 |       9000000.00
(3 rows)
```


# 209-Topshiriq: Bir nechta ustun bo'yicha guruhlash (Multi-column GROUP BY)
## Topshiriq sharti:
Har bir shahar va bo'lim kesimida xodimlar sonini hisoblang.

## Yechim (SQL kodi):
```sql
SELECT shahar, bolim, COUNT(*) AS soni 
FROM xodimlar_agg 
GROUP BY shahar, bolim;
```

## Tushuntirish va Mantiq:
Ko'p ustunli guruhlashda har bir (shahar, bolim) unikal kombinatsiyasi alohida guruh sifatida qaraladi.

## Ishlash natijasi:
```text
shahar   |   bolim   | soni 
------------+-----------+------
 Buxoro     | Marketing |    1
 Samarqand  | Moliya    |    1
 Toshkent   | IT        |    2
 Toshkent   | Moliya    |    1
(4 rows)
```


# 210-Topshiriq: GROUP BY qoidasi (Mustaqil ustunlar xatosi)
## Topshiriq sharti:
GROUP BY ga kiritilmagan va agregat funksiyaga olinmagan ustun SELECT ga qo'yilsa nima bo'lishini ko'rsating.

## Yechim (SQL kodi):
```sql
-- Xato so'rov:
-- SELECT bolim, ism, COUNT(*) FROM xodimlar_agg GROUP BY bolim;
SELECT 'GROUP BY da qatnashmagan ustun SELECT ga faqat agregat bilan kirishi mumkin' AS qoida;
```

## Tushuntirish va Mantiq:
SQL ning asosiy qoidasi: agar so'rovda GROUP BY bo'lsa, SELECT ro'yxatidagi har bir ustun yo GROUP BY da ko'rsatilgan bo'lishi, yoki agregat funksiya (SUM, COUNT...) ichida bo'lishi shart. Aks holda RDBMS 'must appear in the GROUP BY clause' xatosini beradi.

## Ishlash natijasi:
```text
qoida                                         
--------------------------------------------------------------------------------------
 GROUP BY da qatnashmagan ustun SELECT ga faqat agregat bilan kirishi mumkin
(1 row)
```


# 211-Topshiriq: Guruhlangan natijalarni filtrlash: HAVING bandi
## Topshiriq sharti:
Xodimlari soni 1 tadan ko'p bo'lgan bo'limlarni toping.

## Yechim (SQL kodi):
```sql
SELECT bolim, COUNT(*) AS xodimlar_soni 
FROM xodimlar_agg 
GROUP BY bolim 
HAVING COUNT(*) > 1;
```

## Tushuntirish va Mantiq:
'WHERE' qatorlar guruhlanishidan OLDIN filtrlaydi. 'HAVING' esa guruhlar shakllantirilib, agregat qiymat hisoblab bo'lingandan KEYIN filtrlashni amalga oshiradi.

## Ishlash natijasi:
```text
bolim  | xodimlar_soni 
--------+---------------
 IT     |             2
 Moliya |             2
(2 rows)
```


# 212-Topshiriq: WHERE va HAVING ning birgalikda qo'llanishi
## Topshiriq sharti:
Faqat Toshkent shahrida ishlovchi xodimlar orasidan o'rtacha maoshi 10,000,000 dan yuqori bo'lgan bo'limlarni chiqaring.

## Yechim (SQL kodi):
```sql
SELECT bolim, ROUND(AVG(maosh), 2) AS ortacha_maosh 
FROM xodimlar_agg 
WHERE shahar = 'Toshkent' 
GROUP BY bolim 
HAVING AVG(maosh) > 10000000;
```

## Tushuntirish va Mantiq:
So'rovning bajarilish ketma-ketligi: 1) FROM xodimlar_agg, 2) WHERE shahar = 'Toshkent', 3) GROUP BY bolim, 4) HAVING AVG(maosh) > 10M, 5) SELECT.

## Ishlash natijasi:
```text
bolim | ortacha_maosh 
-------+---------------
 IT    |   13500000.00
(1 row)
```


# 213-Topshiriq: HAVING da SUM bilan shart berish
## Topshiriq sharti:
Jami oylik maosh fondi 10,000,000 so'mdan oshadigan bo'limlarni aniqlang.

## Yechim (SQL kodi):
```sql
SELECT bolim, SUM(maosh) AS jami_maosh 
FROM xodimlar_agg 
GROUP BY bolim 
HAVING SUM(maosh) > 10000000;
```

## Tushuntirish va Mantiq:
HAVING bandida SELECT ga kiritilmagan agregat ifodalari bo'yicha ham shart qo'yish mumkin.

## Ishlash natijasi:
```text
bolim |  jami_maosh  
-------+-------------
 IT    | 27000000.00
(1 row)
```


# 214-Topshiriq: Matnlarni bitta satrga yig'ish: STRING_AGG
## Topshiriq sharti:
Har bir bo'limdagi xodimlarning ismlarini vergul bilan ajratilgan bitta matn qilib chiqaring.

## Yechim (SQL kodi):
```sql
SELECT 
    bolim, 
    STRING_AGG(ism, ', ' ORDER BY ism ASC) AS xodimlar_royxati 
FROM xodimlar_agg 
GROUP BY bolim;
```

## Tushuntirish va Mantiq:
'STRING_AGG(ustun, ajratuvchi)' PostgreSQL ning kuchli funksiyasi bo'lib, guruh ichidagi matnlarni bitta satrga birlashtiradi. Ichida alohida ORDER BY berish mumkin.

## Ishlash natijasi:
```text
bolim   | xodimlar_royxati 
-----------+------------------
 IT        | Anvar, Malika
 Marketing | Jasur
 Moliya    | Bobur, Dildora
(3 rows)
```


# 215-Topshiriq: MySQL ekvivalenti: GROUP_CONCAT
## Topshiriq sharti:
MySQL da matnlarni agregatlash sintaksisini ko'rsating.

## Yechim (SQL kodi):
```sql
-- MySQL 8.0+ sintaksisi:
-- SELECT bolim, GROUP_CONCAT(ism ORDER BY ism SEPARATOR ', ') AS royxat
-- FROM xodimlar_agg GROUP BY bolim;
SELECT 'MySQL da STRING_AGG o''rniga GROUP_CONCAT ishlatiladi' AS izoh;
```

## Tushuntirish va Mantiq:
MySQL da xuddi shu vazifani 'GROUP_CONCAT()' funksiyasi bajaradi, ajratuvchi belgi 'SEPARATOR' so'zi orqali beriladi.

## Ishlash natijasi:
```text
izoh                         
------------------------------------------------------
 MySQL da STRING_AGG o'rniga GROUP_CONCAT ishlatiladi
(1 row)
```


# 216-Topshiriq: Elementlarni massivga yig'ish: ARRAY_AGG
## Topshiriq sharti:
Har bir bo'limdagi xodimlarning ID raqamlarini PostgreSQL massivi (ARRAY) ko'rinishida yig'ing.

## Yechim (SQL kodi):
```sql
SELECT 
    bolim, 
    ARRAY_AGG(id ORDER BY id) AS id_massivi 
FROM xodimlar_agg 
GROUP BY bolim;
```

## Tushuntirish va Mantiq:
'ARRAY_AGG()' guruh ichidagi elementlarni bitta massivga (array[]) to'playdi. Bu JSON yaratishda va backend ilovalariga ixcham ma'lumot jo'natishda juda qulay.

## Ishlash natijasi:
```text
bolim   | id_massivi 
-----------+------------
 IT        | {1,2}
 Marketing | {5}
 Moliya    | {3,4}
(3 rows)
```


# 217-Topshiriq: Shartli agregatsiya: FILTER (WHERE ...)
## Topshiriq sharti:
Har bir bo'limda jami nechta xodim borligi va ulardan nechtasi 10,000,000 dan ko'p maosh olishini hisoblang.

## Yechim (SQL kodi):
```sql
SELECT 
    bolim,
    COUNT(*) AS jami_xodimlar,
    COUNT(*) FILTER (WHERE maosh > 10000000) AS yuqori_maoshlilar 
FROM xodimlar_agg 
GROUP BY bolim;
```

## Tushuntirish va Mantiq:
PostgreSQL va SQL:2003 standartidagi 'FILTER (WHERE shart)' agregat funksiya ichida faqat ma'lum shartga mos keluvchi qatorlarni sanash/yig'ish imkonini beradi. Bu eski usuldagi murakkab CASE iboralarining o'rnini bosadi.

## Ishlash natijasi:
```text
bolim   | jami_xodimlar | yuqori_maoshlilar 
-----------+---------------+-------------------
 IT        |             2 |                 2
 Marketing |             1 |                 0
 Moliya    |             2 |                 0
(3 rows)
```


# 218-Topshiriq: FILTER bilan bir nechta turli agregatlarni bir satrda hisoblash
## Topshiriq sharti:
Bitta so'rovda Toshkentdagi va viloyatlardagi xodimlar sonini bo'limlar bo'yicha alohida ustunlarda ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT 
    bolim,
    COUNT(*) FILTER (WHERE shahar = 'Toshkent') AS toshkentliklar,
    COUNT(*) FILTER (WHERE shahar <> 'Toshkent') AS viloyatliklar 
FROM xodimlar_agg 
GROUP BY bolim;
```

## Tushuntirish va Mantiq:
Bu vosita pivot jadvallarni (satrlarni ustunlarga aylantirish) hech qanday murakkab plaginlarsiz o'ta tez va o'qishli amalga oshirishga yordam beradi.

## Ishlash natijasi:
```text
bolim   | toshkentliklar | viloyatliklar 
-----------+----------------+---------------
 IT        |              2 |             0
 Marketing |              0 |             1
 Moliya    |              1 |             1
(3 rows)
```


# 219-Topshiriq: Sana bo'yicha guruhlash (DATE_TRUNC)
## Topshiriq sharti:
Sotuvlarni oylar bo'yicha guruhlab, har bir oyda jami qancha daromad bo'lganini hisoblang.

## Yechim (SQL kodi):
```sql
CREATE TABLE sotuvlar_oy (id SERIAL PRIMARY KEY, summa NUMERIC, sana DATE);
INSERT INTO sotuvlar_oy (summa, sana) VALUES 
(500000, '2026-01-15'), (700000, '2026-01-20'), 
(1200000, '2026-02-10'), (400000, '2026-02-25');

SELECT 
    DATE_TRUNC('month', sana)::DATE AS oy,
    SUM(summa) AS oylik_tushum 
FROM sotuvlar_oy 
GROUP BY DATE_TRUNC('month', sana) 
ORDER BY oy ASC;
```

## Tushuntirish va Mantiq:
'DATE_TRUNC('month', sana)' barcha sanalarni shu oyning birinchi kuniga yaxlitlaydi (masalan: 2026-01-01). Bu vaqt seriyalari bo'yicha oylik hisobot tuzishning eng to'g'ri usulidir.

## Ishlash natijasi:
```text
oy     | oylik_tushum 
------------+--------------
 2026-01-01 |   1200000.00
 2026-02-01 |   1600000.00
(2 rows)
```


# 220-Topshiriq: Agregat natijalari bo'yicha saralash (ORDER BY Aggregate)
## Topshiriq sharti:
Bo'limlarni eng ko'p umumiy maosh fondiga ega bo'lganidan boshlab saralang.

## Yechim (SQL kodi):
```sql
SELECT bolim, SUM(maosh) AS jami_maosh 
FROM xodimlar_agg 
GROUP BY bolim 
ORDER BY SUM(maosh) DESC NULLS LAST;
```

## Tushuntirish va Mantiq:
ORDER BY bandida to'g'ridan-to'g'ri 'SUM(maosh)' agregat ifodasini yoki uning 'jami_maosh' taxallusini ko'rsatish mumkin.

## Ishlash natijasi:
```text
bolim   |  jami_maosh  
-----------+-------------
 IT        | 27000000.00
 Moliya    |  9000000.00
 Marketing |  7500000.00
(3 rows)
```


# 221-Topshiriq: Eng katta qiymatli guruhni topish (GROUP BY + LIMIT)
## Topshiriq sharti:
Kompaniyadagi eng ko'p xodimga ega bo'lgan top-1 bo'limni aniqlang.

## Yechim (SQL kodi):
```sql
SELECT bolim, COUNT(*) AS soni 
FROM xodimlar_agg 
GROUP BY bolim 
ORDER BY soni DESC 
LIMIT 1;
```

## Tushuntirish va Mantiq:
Guruhlash, saralash va LIMIT birgalikda biznes savollariga (eng ko'p sotilgan mahsulot, eng faol mijoz) darhol javob beradi.

## Ishlash natijasi:
```text
bolim | soni 
-------+------
 IT    |    2
(1 row)
```


# 222-Topshiriq: NULL qiymatlarning GROUP BY dagi xulqi
## Topshiriq sharti:
Agar ustunda NULL qiymatlar bo'lsa, GROUP BY ularni alohida guruh qiladimi?

## Yechim (SQL kodi):
```sql
CREATE TABLE test_null_group (toifa TEXT, qiymat INT);
INSERT INTO test_null_group VALUES ('A', 10), (NULL, 20), ('A', 30), (NULL, 40);

SELECT toifa, SUM(qiymat) AS jami 
FROM test_null_group 
GROUP BY toifa;
```

## Tushuntirish va Mantiq:
SQL standartiga binoan GROUP BY barcha NULL qiymatlarni bitta alohida guruhga jamlaydi. Natijada 'NULL' nomli guruh chiqadi.

## Ishlash natijasi:
```text
toifa | jami 
-------+------
 A     |   40
 NULL  |   60
(2 rows)
```


# 223-Topshiriq: Jadval bo'sh bo'lganda COUNT va SUM xatti-harakati
## Topshiriq sharti:
Bo'sh jadvalga COUNT va SUM so'rovi berilganda qanday natija chiqadi?

## Yechim (SQL kodi):
```sql
CREATE TABLE bosh_jadval (son INT);

SELECT 
    COUNT(*) AS count_natija,
    SUM(son) AS sum_natija,
    COALESCE(SUM(son), 0) AS xavfsiz_sum 
FROM bosh_jadval;
```

## Tushuntirish va Mantiq:
Qatorlar bo'lmaganda 'COUNT(*)' 0 qaytaradi, biroq 'SUM(son)' NULL qaytaradi! Chunki hech qanday son yo'q. Shu sababli dasturlarda SUM har doim COALESCE bilan o'ralishi tavsiya etiladi.

## Ishlash natijasi:
```text
count_natija | sum_natija | xavfsiz_sum 
--------------+------------+-------------
            0 | NULL       |           0
(1 row)
```


# 224-Topshiriq: Iyerarxik jami hisoblar: ROLLUP
## Topshiriq sharti:
Shahar va bo'limlar kesimida, shuningdek har bir shahar bo'yicha oraliq jami (subtotal) va butun korxona bo'yicha umumiy jami (grand total) maoshni hisoblang.

## Yechim (SQL kodi):
```sql
SELECT 
    shahar, 
    bolim, 
    SUM(maosh) AS jami_maosh 
FROM xodimlar_agg 
GROUP BY ROLLUP (shahar, bolim);
```

## Tushuntirish va Mantiq:
'ROLLUP (A, B)' daraxtsimon iyerarxiyani hisoblaydi: 1) (A, B) guruhlari, 2) A bo'yicha oraliq jamilar, 3) Umumiy jami (grand total). NULL chiqqan joylar oraliq jamini bildiradi.

## Ishlash natijasi:
```text
shahar   |   bolim   |  jami_maosh  
------------+-----------+-------------
 Buxoro     | Marketing |  7500000.00
 Buxoro     | NULL      |  7500000.00
 Samarqand  | Moliya    |  9000000.00
 Samarqand  | NULL      |  9000000.00
 Toshkent   | IT        | 27000000.00
 Toshkent   | Moliya    |        NULL
 Toshkent   | NULL      | 27000000.00
 NULL       | NULL      | 43500000.00
(8 rows)
```


# 225-Topshiriq: Barcha o'lchamlar kombinatsiyasi: CUBE
## Topshiriq sharti:
Shahar va bo'limning barcha mumkin bo'lgan kombinatsiyalari bo'yicha ko'p o'lchovli kub hisobotini tuzing.

## Yechim (SQL kodi):
```sql
SELECT 
    shahar, 
    bolim, 
    COUNT(*) AS soni 
FROM xodimlar_agg 
GROUP BY CUBE (shahar, bolim);
```

## Tushuntirish va Mantiq:
'CUBE (A, B)' barcha mumkin bo'lgan 2^N ta kombinatsiyalarni hisoblaydi: (A, B), (A), (B) va (). OLAP (Online Analytical Processing) hisobotlarida keng qo'llaniladi.

## Ishlash natijasi:
```text
shahar   |   bolim   | soni 
------------+-----------+------
 Buxoro     | Marketing |    1
 Samarqand  | Moliya    |    1
 Toshkent   | IT        |    2
 Toshkent   | Moliya    |    1
 NULL       | IT        |    2
 NULL       | Marketing |    1
 NULL       | Moliya    |    2
 Buxoro     | NULL      |    1
 Samarqand  | NULL      |    1
 Toshkent   | NULL      |    3
 NULL       | NULL      |    5
(11 rows)
```


# 226-Topshiriq: Maxsus guruhlash to'plamlari: GROUPING SETS
## Topshiriq sharti:
Ortiqcha kombinatsiyalarsiz faqat 1) (shahar), 2) (bolim) bo'yicha alohida-alohida hisobotlarni bitta so'rovda oling.

## Yechim (SQL kodi):
```sql
SELECT 
    shahar, 
    bolim, 
    COUNT(*) AS xodimlar 
FROM xodimlar_agg 
GROUP BY GROUPING SETS (
    (shahar),
    (bolim),
    ()
);
```

## Tushuntirish va Mantiq:
'GROUPING SETS' dasturchiga qaysi aniq o'lchamlar bo'yicha jamlash kerakligini qo'lda belgilash imkonini beradi. Bu bir nechta UNION ALL so'rovlarini bitta samarali so'rovga birlashtiradi.

## Ishlash natijasi:
```text
shahar   |   bolim   | xodimlar 
------------+-----------+----------
 Buxoro     | NULL      |        1
 Samarqand  | NULL      |        1
 Toshkent   | NULL      |        3
 NULL       | IT        |        2
 NULL       | Marketing |        1
 NULL       | Moliya    |        2
 NULL       | NULL      |        5
(7 rows)
```


# 227-Topshiriq: Oraliq jamini aniqlash: GROUPING() funksiyasi
## Topshiriq sharti:
Chiqarilayotgan satr haqiqiy ma'lumotmi yoki ROLLUP tomonidan hosil qilingan umumiy jamimi ekanligini ajratib bering.

## Yechim (SQL kodi):
```sql
SELECT 
    CASE WHEN GROUPING(bolim) = 1 THEN 'Barcha Bo''limlar' ELSE bolim END AS bolim_nomi,
    SUM(maosh) AS jami_maosh 
FROM xodimlar_agg 
GROUP BY ROLLUP (bolim);
```

## Tushuntirish va Mantiq:
'GROUPING(ustun)' funksiyasi agar ushbu ustun agregatlangan umumiy oraliq jami bo'lsa 1, haqiqiy ma'lumot qatori bo'lsa 0 qaytaradi. Bu hisobotlarda 'Jami' so'zini chiroyli chiqarishda ishlatiladi.

## Ishlash natijasi:
```text
bolim_nomi     |  jami_maosh  
-------------------+-------------
 IT                | 27000000.00
 Marketing         |  7500000.00
 Moliya            |  9000000.00
 Barcha Bo'limlar  | 43500000.00
(4 rows)
```


# 228-Topshiriq: Guruh ichida foiz ulushini hisoblash
## Topshiriq sharti:
Har bir bo'limning kompaniya umumiy maosh fondidagi foiz ulushini aniqlang.

## Yechim (SQL kodi):
```sql
SELECT 
    bolim,
    SUM(maosh) AS bolim_fondi,
    ROUND((SUM(maosh) / (SELECT SUM(maosh) FROM xodimlar_agg WHERE maosh IS NOT NULL) * 100), 2) AS ulush_foiz 
FROM xodimlar_agg 
WHERE maosh IS NOT NULL 
GROUP BY bolim;
```

## Tushuntirish va Mantiq:
Subquery yordamida korxonaning to'liq fondi olinadi va har bir guruhning summasi umumiy summaga bo'linadi.

## Ishlash natijasi:
```text
bolim   | bolim_fondi | ulush_foiz 
-----------+-------------+------------
 IT        | 27000000.00 |      62.07
 Marketing |  7500000.00 |      17.24
 Moliya    |  9000000.00 |      20.69
(3 rows)
```


# 229-Topshiriq: Statistik funksiyalar: Standart og'ish (STDDEV) va Dispersiya (VARIANCE)
## Topshiriq sharti:
Xodimlarning maoshlari bo'yicha tanlanma dispersiyasi va standart og'ishini hisoblang.

## Yechim (SQL kodi):
```sql
SELECT 
    ROUND(STDDEV(maosh), 2) AS standart_ogish,
    ROUND(VARIANCE(maosh), 2) AS dispersiya 
FROM xodimlar_agg;
```

## Tushuntirish va Mantiq:
'STDDEV' va 'VARIANCE' ma'lumotlar to'plamidagi sonlarning o'rtacha qiymat atrofida qanchalik tarqalganligini ko'rsatuvchi matematik statistik funksiyalardir.

## Ishlash natijasi:
```text
standart_ogish |       dispersiya       
----------------+------------------------
     3250000.00 | 10562500000000.00
(1 row)
```


# 230-Topshiriq: Guruhlashda ifodalardan foydalanish (Expression grouping)
## Topshiriq sharti:
Xodimlarni ularning maosh darajasi ('Yuqori' >= 10M, 'O''rta' < 10M) bo'yicha guruhlab sonini hisoblang.

## Yechim (SQL kodi):
```sql
SELECT 
    CASE WHEN maosh >= 10000000 THEN 'Yuqori' ELSE 'O''rta' END AS maosh_darajasi,
    COUNT(*) AS soni 
FROM xodimlar_agg 
WHERE maosh IS NOT NULL 
GROUP BY (CASE WHEN maosh >= 10000000 THEN 'Yuqori' ELSE 'O''rta' END);
```

## Tushuntirish va Mantiq:
GROUP BY bandiga ixtiyoriy CASE mantiqiy ifodasini kiritish orqali ma'lumotlarni virtual toifalarga ajratib guruhlash mumkin.

## Ishlash natijasi:
```text
maosh_darajasi | soni 
----------------+------
 O'rta          |    2
 Yuqori         |    2
(2 rows)
```


# 231-Topshiriq: SELECT dagi taxallus (alias) bo'yicha GROUP BY
## Topshiriq sharti:
PostgreSQL da SELECT da berilgan taxallus nomini bevosita GROUP BY ga qo'yish imkoniyati.

## Yechim (SQL kodi):
```sql
SELECT 
    CASE WHEN maosh >= 10000000 THEN 'Yuqori' ELSE 'O''rta' END AS daraja,
    COUNT(*) AS soni 
FROM xodimlar_agg 
WHERE maosh IS NOT NULL 
GROUP BY daraja;
```

## Tushuntirish va Mantiq:
PostgreSQL sintaksisi GROUP BY da SELECT dagi taxalluslar (aliases) dan to'g'ridan-to'g'ri foydalanishga ruxsat beradi (ANSI SQL da bu taqiqlangan, lekin dasturchilar uchun juda qulay).

## Ishlash natijasi:
```text
daraja | soni 
--------+------
 O'rta  |    2
 Yuqori |    2
(2 rows)
```


# 232-Topshiriq: HAVING da bir nechta mantiqiy shartlar (AND, OR)
## Topshiriq sharti:
Xodimlar soni 1 tadan ko'p bo'lgan VA o'rtacha maoshi 8,000,000 dan oshadigan bo'limlarni filtrlash.

## Yechim (SQL kodi):
```sql
SELECT bolim, COUNT(*) AS soni, AVG(maosh) AS ortacha 
FROM xodimlar_agg 
GROUP BY bolim 
HAVING COUNT(*) > 1 AND AVG(maosh) > 8000000;
```

## Tushuntirish va Mantiq:
HAVING bandida ham WHERE kabi AND, OR, NOT operatorlari orqali bir nechta murakkab agregat mezonlarni birlashtirish mumkin.

## Ishlash natijasi:
```text
bolim | soni |       ortacha        
-------+------+----------------------
 IT    |    2 | 13500000.000000000000
(1 row)
```


# 233-Topshiriq: COUNT(1) va COUNT(*) o'rtasidagi farq bormi?
## Topshiriq sharti:
Ko'p muhokama qilinadigan COUNT(1), COUNT(*), COUNT('x') farqini RDBMS darajasida tahlil qiling.

## Yechim (SQL kodi):
```sql
SELECT 
    COUNT(*) AS c_yulduz,
    COUNT(1) AS c_bir,
    COUNT('ixtiyoriy') AS c_matn 
FROM xodimlar_agg;
```

## Tushuntirish va Mantiq:
Zamonaviy SQL optimizatorlari (PostgreSQL, MySQL, Oracle) uchun COUNT(*) va COUNT(1) o'rtasida HECH QANDAY ishlash tezligi farqi yo'q. Ular ichki reja tuzishda (execution plan) aynan bitta Aggregate operatoriga aylanadi. Standart bo'yicha COUNT(*) yozish eng to'g'ri hisoblanadi.

## Ishlash natijasi:
```text
c_yulduz | c_bir | c_matn 
----------+-------+--------
        5 |     5 |      5
(1 row)
```


# 234-Topshiriq: Mantiqiy qiymatlarni agregatlash: BOOL_AND va BOOL_OR
## Topshiriq sharti:
Bo'limdagi barcha xodimlarning sinov muddati tugaganligini (BOOL_AND) yoki kamida bittasining tugaganligini (BOOL_OR) tekshiring.

## Yechim (SQL kodi):
```sql
CREATE TABLE xodim_sinov (bolim TEXT, otganmi BOOLEAN);
INSERT INTO xodim_sinov VALUES ('IT', TRUE), ('IT', TRUE), ('Moliya', TRUE), ('Moliya', FALSE);

SELECT 
    bolim, 
    BOOL_AND(otganmi) AS barchasi_otganmi,
    BOOL_OR(otganmi) AS kamida_biri_otganmi 
FROM xodim_sinov 
GROUP BY bolim;
```

## Tushuntirish va Mantiq:
'BOOL_AND()' barcha qatorlar TRUE bo'lsagina TRUE qaytaradi (mantiqiy AND). 'BOOL_OR()' esa kamida bitta TRUE bo'lsa TRUE qaytaradi.

## Ishlash natijasi:
```text
bolim  | barchasi_otganmi | kamida_biri_otganmi 
--------+------------------+---------------------
 IT     | t                | t
 Moliya | f                | t
(2 rows)
```


# 235-Topshiriq: Guruhlashda B-Tree vs HashAggregate ijro rejalari
## Topshiriq sharti:
EXPLAIN orqali RDBMS qachon HashAggregate va qachon GroupAggregate tanlashini ko'ring.

## Yechim (SQL kodi):
```sql
EXPLAIN SELECT bolim, COUNT(*) 
FROM xodimlar_agg 
GROUP BY bolim;
```

## Tushuntirish va Mantiq:
RDBMS xotira (work_mem) yetarli bo'lsa guruhlash uchun HashAggregate (hash jadval) ishlatadi, bu O(N) vaqt oladi. Agar xotira yetmasa yoki ma'lumotlar indeks orqali saralangan bo'lsa, GroupAggregate (Sort + Group) rejasini tanlaydi.

## Ishlash natijasi:
```text
QUERY PLAN                              
---------------------------------------------------------------------
 HashAggregate  (cost=1.07..1.10 rows=3 width=40)
   Group Key: bolim
   ->  Seq Scan on xodimlar_agg  (cost=0.00..1.05 rows=5 width=32)
(3 rows)
```


# 236-Topshiriq: Ortiqcha ustunlarni GROUP BY ga qo'shmaslik: PK mavjudligi
## Topshiriq sharti:
Agar birlamchi kalit (PK) GROUP BY ga kiritilgan bo'lsa, jadvalning boshqa ustunlarini GROUP BY ga kiritish shart emasligini (Functional Dependency) ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT id, ism, bolim, COUNT(*) 
FROM xodimlar_agg 
GROUP BY id;
```

## Tushuntirish va Mantiq:
SQL:2003 standartiga ko'ra, agar birlamchi kalit 'id' GROUP BY da bo'lsa, qolgan 'ism' va 'bolim' ustunlari id ga to'liq funktsional bog'liq bo'lgani uchun ularni GROUP BY da takrorlash shart emas.

## Ishlash natijasi:
```text
id |   ism   |   bolim   | count 
----+---------+-----------+-------
  1 | Anvar   | IT        |     1
  2 | Malika  | IT        |     1
  3 | Bobur   | Moliya    |     1
  4 | Dildora | Moliya    |     1
  5 | Jasur   | Marketing |     1
(5 rows)
```


# 237-Topshiriq: Shartli o'rtachani hisoblash (Faqat musbat summalar o'rtachasi)
## Topshiriq sharti:
Hisobdagi faqat musbat tushumlarning o'rtacha miqdorini aniqlang.

## Yechim (SQL kodi):
```sql
CREATE TABLE tr_hisob (summa NUMERIC);
INSERT INTO tr_hisob VALUES (100000), (-50000), (300000), (-20000);

SELECT 
    AVG(summa) FILTER (WHERE summa > 0) AS ortacha_tushum,
    AVG(summa) AS umumiy_balans_harakati 
FROM tr_hisob;
```

## Tushuntirish va Mantiq:
FILTER yordamida statistik ko'rsatkichlarni bir nechta so'rovsiz bitta qatorda taqqoslash mumkin.

## Ishlash natijasi:
```text
ortacha_tushum | umumiy_balans_harakati 
----------------+------------------------
    200000.0000 |             82500.0000
(1 row)
```


# 238-Topshiriq: Guruh ichida eng ko'p takrorlangan qiymatni topish: MODE()
## Topshiriq sharti:
Talabalar eng ko'p olgan modal bahoni (eng keng tarqalgan qiymat) aniqlang.

## Yechim (SQL kodi):
```sql
CREATE TABLE baholar (baho INT);
INSERT INTO baholar VALUES (4), (5), (4), (3), (5), (4);

SELECT MODE() WITHIN GROUP (ORDER BY baho) AS modal_baho 
FROM baholar;
```

## Tushuntirish va Mantiq:
'MODE() WITHIN GROUP (ORDER BY ustun)' guruh ichida eng ko'p uchragan qiymatni qaytaruvchi buyurtmali to'plam (ordered-set) agregat funksiyasidir.

## Ishlash natijasi:
```text
modal_baho 
------------
          4
(1 row)
```


# 239-Topshiriq: Persentillarni hisoblash: PERCENTILE_CONT
## Topshiriq sharti:
Xodimlarning median maoshini (50-persentil) hisoblang.

## Yechim (SQL kodi):
```sql
SELECT 
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY maosh) AS mediana_maosh 
FROM xodimlar_agg 
WHERE maosh IS NOT NULL;
```

## Tushuntirish va Mantiq:
Mediana o'rtacha qiymatdan farqli o'laroq haddan tashqari katta anomaliyalarga (outliers) berilmaydi va real o'rtahol xodimning daromadini aniq ko'rsatadi.

## Ishlash natijasi:
```text
mediana_maosh 
---------------
      10500000
(1 row)
```


# 240-Topshiriq: Oraliq summalarni taqqoslash: Guruh o'rtachasidan yuqori bo'lganlar
## Topshiriq sharti:
O'z bo'limining o'rtacha maoshidan ko'p oluvchi xodimlarni topishga tayyorgarlik.

## Yechim (SQL kodi):
```sql
SELECT bolim, ROUND(AVG(maosh), 2) AS bolim_ortacha 
FROM xodimlar_agg 
GROUP BY bolim;
```

## Tushuntirish va Mantiq:
Guruhlangan agregat qiymatlar keyingi bosqichda subquery yoki JOIN lar yordamida alohida xodimlar bilan solishtiriladi.

## Ishlash natijasi:
```text
bolim   | bolim_ortacha 
-----------+---------------
 IT        |   13500000.00
 Marketing |    7500000.00
 Moliya    |    9000000.00
(3 rows)
```


# 241-Topshiriq: JSON obyektiga agregatlash: JSON_OBJECT_AGG
## Topshiriq sharti:
Bo'lim nomi kalit, undagi xodimlar soni qiymat bo'lgan yagona JSON obyektini hosil qiling.

## Yechim (SQL kodi):
```sql
SELECT JSON_OBJECT_AGG(bolim, xodimlar_soni) AS statistika_json
FROM (
    SELECT bolim, COUNT(*) AS xodimlar_soni 
    FROM xodimlar_agg 
    GROUP BY bolim
) s;
```

## Tushuntirish va Mantiq:
'JSON_OBJECT_AGG(key, value)' relyatsion ma'lumotlarni to'g'ridan-to'g'ri JSON lug'atiga (key-value) aylantirib beradi.

## Ishlash natijasi:
```text
statistika_json                   
-----------------------------------------------------
 { "IT" : 2, "Marketing" : 1, "Moliya" : 2 }
(1 row)
```


# 242-Topshiriq: Murakkab HAVING: Faqat barcha shartlarni bajargan guruhlar
## Topshiriq sharti:
Bo'limdagi barcha xodimlarning maoshi 8,000,000 dan yuqori bo'lgan (eng kami ham 8M dan katta) bo'limlarni toping.

## Yechim (SQL kodi):
```sql
SELECT bolim, MIN(maosh) AS minimal_maosh 
FROM xodimlar_agg 
GROUP BY bolim 
HAVING MIN(maosh) >= 8000000;
```

## Tushuntirish va Mantiq:
'HAVING MIN(maosh) >= 8000000' sharti bo'limda birorta ham kam maosh oluvchi yo'qligini kafolatlaydi.

## Ishlash natijasi:
```text
bolim  | minimal_maosh 
--------+---------------
 IT     |   12000000.00
 Moliya |    9000000.00
(2 rows)
```


# 243-Topshiriq: Takrorlanuvchi qatorlarni topish (Dublikatlar tahlili)
## Topshiriq sharti:
Jadvalda ayni bir xil ism nechta marta takrorlanganini HAVING yordamida aniqlang.

## Yechim (SQL kodi):
```sql
CREATE TABLE ismlar_royxati (ism TEXT);
INSERT INTO ismlar_royxati VALUES ('Ali'), ('Vali'), ('Ali'), ('Gani'), ('Ali');

SELECT ism, COUNT(*) AS takrorlanishlar_soni 
FROM ismlar_royxati 
GROUP BY ism 
HAVING COUNT(*) > 1;
```

## Tushuntirish va Mantiq:
'GROUP BY ustun HAVING COUNT(*) > 1' relyatsion bazalarda dublikat yozuvlarni topishning klassik va eng universal usulidir.

## Ishlash natijasi:
```text
ism | takrorlanishlar_soni 
-----+---------------------
 Ali |                   3
(1 row)
```


# 244-Topshiriq: Yil va fasllar bo'yicha guruhlash
## Topshiriq sharti:
Sotuv sanasining oyi bo'yicha fasllarga ajratib daromadni jamlang.

## Yechim (SQL kodi):
```sql
SELECT 
    CASE 
        WHEN EXTRACT(MONTH FROM sana) IN (12, 1, 2) THEN 'Qish'
        WHEN EXTRACT(MONTH FROM sana) IN (3, 4, 5) THEN 'Bahor'
        WHEN EXTRACT(MONTH FROM sana) IN (6, 7, 8) THEN 'Yoz'
        ELSE 'Kuz'
    END AS fasl,
    SUM(summa) AS fasliy_daromad 
FROM sotuvlar_oy 
GROUP BY 1;
```

## Tushuntirish va Mantiq:
SELECT bandining 1-ustuniga tayanuvchi fasl formulasi bo'yicha daromadlar to'liq guruhlanadi.

## Ishlash natijasi:
```text
fasl | fasliy_daromad 
------+----------------
 Qish |     2800000.00
(1 row)
```


# 245-Topshiriq: Bitwise agregatlar: BIT_AND va BIT_OR
## Topshiriq sharti:
Foydalanuvchilarning ruxsatnomalar bit maskasini birlashtirish.

## Yechim (SQL kodi):
```sql
CREATE TABLE huquqlar (maska BIT(4));
INSERT INTO huquqlar VALUES (B'1010'), (B'1100');

SELECT 
    BIT_AND(maska) AS umumiy_kesishma,
    BIT_OR(maska) AS umumiy_birlashma 
FROM huquqlar;
```

## Tushuntirish va Mantiq:
Bit darajasidagi agregatlar xavfsizlik va ruxsatlar boshqaruvida (access control list) barcha qatorlarning umumiy huquqlarini hisoblashda ishlatiladi.

## Ishlash natijasi:
```text
umumiy_kesishma | umumiy_birlashma 
-----------------+------------------
 1000            | 1110
(1 row)
```


# 246-Topshiriq: Agregat funksiyada arifmetik ifodalarni jamlash
## Topshiriq sharti:
Mahsulot narxi va sotilgan sonini ko'paytmasini bitta SUM ichida hisoblang.

## Yechim (SQL kodi):
```sql
CREATE TABLE savdo_detal (narx NUMERIC, miqdor INT);
INSERT INTO savdo_detal VALUES (10000, 5), (20000, 3);

SELECT SUM(narx * miqdor) AS jami_tushum 
FROM savdo_detal;
```

## Tushuntirish va Mantiq:
SUM(a * b) amali har bir qator uchun oldin ko'paytirishni bajaradi va hosil bo'lgan natijalarni yig'adi.

## Ishlash natijasi:
```text
jami_tushum 
-------------
   110000.00
(1 row)
```


# 247-Topshiriq: Guruhlash ustunida bo'shliqlarni tozalash (TRIM bilan GROUP BY)
## Topshiriq sharti:
Imloviy bo'shliqlar (' IT', 'IT ') tufayli sun'iy alohida guruhlar hosil bo'lishining oldini oling.

## Yechim (SQL kodi):
```sql
CREATE TABLE iflos_bolim (b TEXT);
INSERT INTO iflos_bolim VALUES ('IT'), (' IT '), ('IT');

SELECT TRIM(b) AS toza_bolim, COUNT(*) 
FROM iflos_bolim 
GROUP BY TRIM(b);
```

## Tushuntirish va Mantiq:
GROUP BY ga TRIM qo'llash orqali kiruvchi ma'lumotlardagi xatolar tufayli bir xil ma'noli qatorlar turli guruhlarga bo'linib ketishi bartaraf etiladi.

## Ishlash natijasi:
```text
toza_bolim | count 
------------+-------
 IT         |     3
(1 row)
```


# 248-Topshiriq: COUNT(DISTINCT a, b) simulyatsiyasi
## Topshiriq sharti:
PostgreSQL da ikkita ustun juftligining noyob kombinatsiyalarini sanash.

## Yechim (SQL kodi):
```sql
SELECT COUNT(DISTINCT (shahar, bolim)) AS noyob_juftliklar 
FROM xodimlar_agg;
```

## Tushuntirish va Mantiq:
Tuple konstruktori `(shahar, bolim)` yordamida ikkita ustunning birgalikdagi noyob juftliklari soni aniq hisoblanadi.

## Ishlash natijasi:
```text
noyob_juftliklar 
-------------------
                 4
(1 row)
```


# 249-Topshiriq: HAVING da Subquery ishlatish
## Topshiriq sharti:
O'rtacha maoshi butun kompaniyaning o'rtacha maoshidan yuqori bo'lgan bo'limlarni filtrlash.

## Yechim (SQL kodi):
```sql
SELECT bolim, AVG(maosh) AS b_ortacha 
FROM xodimlar_agg 
WHERE maosh IS NOT NULL 
GROUP BY bolim 
HAVING AVG(maosh) > (SELECT AVG(maosh) FROM xodimlar_agg);
```

## Tushuntirish va Mantiq:
HAVING bandida global korxona ko'rsatkichini qaytaruvchi mustaqil subquery qo'llash mumkin.

## Ishlash natijasi:
```text
bolim |        b_ortacha        
-------+-------------------------
 IT    | 13500000.00000000000000
(1 row)
```


# 250-Topshiriq: Korporativ Agregat: Savdo tahlili va ko'p bosqichli hisobot
## Topshiriq sharti:
E-tijorat tizimida har bir toifa va oy bo'yicha jami savdo hajmi, buyurtmalar soni, o'rtacha chek miqdori va umumiy jami ko'rsatkichlarni ROLLUP yordamida tuzing.

## Yechim (SQL kodi):
```sql
CREATE TABLE korporativ_savdo (
    buyurtma_id BIGSERIAL PRIMARY KEY,
    toifa VARCHAR(50),
    summa NUMERIC(15, 2),
    sana DATE
);

INSERT INTO korporativ_savdo (toifa, summa, sana) VALUES 
('Elektronika', 15000000, '2026-01-10'),
('Elektronika', 25000000, '2026-01-15'),
('Kiyim-kechak', 4000000, '2026-01-18'),
('Elektronika', 30000000, '2026-02-05'),
('Kiyim-kechak', 6000000, '2026-02-14');

SELECT 
    COALESCE(toifa, '=== BARCHA TOIFALAR ===') AS mahsulot_toifasi,
    CASE 
        WHEN GROUPING(toifa) = 0 AND GROUPING(DATE_TRUNC('month', sana)) = 1 THEN '--- Oylik Jami ---'
        WHEN GROUPING(toifa) = 1 THEN '*** YAKUNIY JAMI ***'
        ELSE TO_CHAR(DATE_TRUNC('month', sana), 'YYYY-MM')
    END AS hisobot_davri,
    COUNT(*) AS buyurtmalar_soni,
    SUM(summa) AS jami_tushum,
    ROUND(AVG(summa), 2) AS ortacha_chek
FROM korporativ_savdo 
GROUP BY ROLLUP (toifa, DATE_TRUNC('month', sana))
ORDER BY toifa NULLS LAST, hisobot_davri ASC;
```

## Tushuntirish va Mantiq:
Bu so'rov yirik analitik tizimlarda (PowerBI, Tableau, Superset kabi) qo'llaniladigan to'liq iyerarxik guruhlash modelidir: ROLLUP yordamida toifalar va oylar bo'yicha oraliq hamda yakuniy jami balanslar bir vaqtda shakllantiriladi.

## Ishlash natijasi:
```text
mahsulot_toifasi     |    hisobot_davri    | buyurtmalar_soni |  jami_tushum  | ortacha_chek 
-------------------------+---------------------+------------------+--------------+--------------
 Elektronika             | 2026-01             |                2 |  40000000.00 |  20000000.00
 Elektronika             | 2026-02             |                1 |  30000000.00 |  30000000.00
 Elektronika             | --- Oylik Jami ---  |                3 |  70000000.00 |  23333333.33
 Kiyim-kechak            | 2026-01             |                1 |   4000000.00 |   4000000.00
 Kiyim-kechak            | 2026-02             |                1 |   6000000.00 |   6000000.00
 Kiyim-kechak            | --- Oylik Jami ---  |                2 |  10000000.00 |   5000000.00
 === BARCHA TOIFALAR === | *** YAKUNIY JAMI ***|                5 |  80000000.00 |  16000000.00
(7 rows)
```

