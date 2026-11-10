# 401-Topshiriq: Oynador funksiya asoslari: Bo'sh OVER() bandi
## Topshiriq sharti:
Har bir xodim yonida butun korxona xodimlarining umumiy sonini qatorlarni guruhlamasdan chiqaring.

## Yechim (SQL kodi):
```sql
CREATE TABLE xodimlar_wf (
    id SERIAL PRIMARY KEY,
    ism VARCHAR(50),
    bolim VARCHAR(50),
    maosh NUMERIC(12, 2),
    shahar VARCHAR(50)
);

INSERT INTO xodimlar_wf (ism, bolim, maosh, shahar) VALUES 
('Sherzod', 'IT', 15000000, 'Toshkent'),
('Nodira', 'IT', 18000000, 'Toshkent'),
('Azamat', 'IT', 12000000, 'Samarqand'),
('Gulnoza', 'Moliya', 10000000, 'Toshkent'),
('Botir', 'Moliya', 10000000, 'Buxoro'),
('Laylo', 'Moliya', 9000000, 'Toshkent');

SELECT 
    ism, 
    bolim, 
    maosh,
    COUNT(*) OVER () AS umumiy_xodimlar_soni 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
Oynador funksiya (Window function) GROUP BY dan farqli o'laroq qatorlarni bitta satrga siqib (collapse) yubormaydi. Har bir xodim o'z qatorida qoladi, 'COUNT(*) OVER ()' esa butun jadval oynasi (window) bo'yicha hisob-kitob qilib yoniga qo'yib beradi.

## Ishlash natijasi:
```text
ism   | bolim  |    maosh    | umumiy_xodimlar_soni 
---------+--------+-------------+----------------------
 Sherzod | IT     | 15000000.00 |                    6
 Nodira  | IT     | 18000000.00 |                    6
 Azamat  | IT     | 12000000.00 |                    6
 Gulnoza | Moliya | 10000000.00 |                    6
 Botir   | Moliya | 10000000.00 |                    6
 Laylo   | Moliya |  9000000.00 |                    6
(6 rows)
```


# 402-Topshiriq: Oynani bo'limlarga ajratish: PARTITION BY
## Topshiriq sharti:
Har bir xodim yonida O'Z BO'LIMIDAGI xodimlar sonini ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    bolim, 
    COUNT(*) OVER (PARTITION BY bolim) AS bolimdagi_xodimlar 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
'PARTITION BY bolim' oynani bo'limlar bo'yicha alohida kichik oynalarga (partitions) ajratadi. Har bir xodim uchun o'z bo'limi ichidagi yozuvlar sanaladi.

## Ishlash natijasi:
```text
ism   | bolim  | bolimdagi_xodimlar 
---------+--------+--------------------
 Sherzod | IT     |                  3
 Nodira  | IT     |                  3
 Azamat  | IT     |                  3
 Gulnoza | Moliya |                  3
 Botir   | Moliya |                  3
 Laylo   | Moliya |                  3
(6 rows)
```


# 403-Topshiriq: Qat'iy ketma-ket tartib raqami: ROW_NUMBER()
## Topshiriq sharti:
Barcha xodimlarni maoshi kamayishi tartibida 1 dan boshlab tartib raqami bilan raqamlang.

## Yechim (SQL kodi):
```sql
SELECT 
    ROW_NUMBER() OVER (ORDER BY maosh DESC) AS tartib_raqami,
    ism, 
    maosh 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
'ROW_NUMBER()' berilgan tartib bo'yicha har bir qatorga yagona, uzluksiz ketma-ket son (1, 2, 3...) beradi. Hattoki ikki xodimning maoshi bir xil bo'lsa ham (Gulnoza va Botir 10M), ularga ketma-ket turli raqam beriladi.

## Ishlash natijasi:
```text
tartib_raqami |   ism   |    maosh    
---------------+---------+-------------
             1 | Nodira  | 18000000.00
             2 | Sherzod | 15000000.00
             3 | Azamat  | 12000000.00
             4 | Gulnoza | 10000000.00
             5 | Botir   | 10000000.00
             6 | Laylo   |  9000000.00
(6 rows)
```


# 404-Topshiriq: Guruh ichida alohida ROW_NUMBER (PARTITION BY + ORDER BY)
## Topshiriq sharti:
Har bir bo'lim ichida xodimlarni eng katta maoshidan boshlab alohida 1, 2, 3... qilib raqamlang.

## Yechim (SQL kodi):
```sql
SELECT 
    bolim,
    ROW_NUMBER() OVER (PARTITION BY bolim ORDER BY maosh DESC) AS bolim_ichida_orin,
    ism, 
    maosh 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
Yangi bo'lim boshlanishi bilan hisoblagich qaytadan 1 dan boshlanadi. IT bo'limida 1, 2, 3, so'ng Moliya bo'limida ham yana 1, 2, 3 bo'ladi.

## Ishlash natijasi:
```text
bolim  | bolim_ichida_orin |   ism   |    maosh    
--------+-------------------+---------+-------------
 IT     |                 1 | Nodira  | 18000000.00
 IT     |                 2 | Sherzod | 15000000.00
 IT     |                 3 | Azamat  | 12000000.00
 Moliya |                 1 | Gulnoza | 10000000.00
 Moliya |                 2 | Botir   | 10000000.00
 Moliya |                 3 | Laylo   |  9000000.00
(6 rows)
```


# 405-Topshiriq: O'rin berishda oraliq qoldiruvchi: RANK()
## Topshiriq sharti:
Xodimlarga maoshi bo'yicha o'rin (reyting) bering. Bir xil maosh oluvchilar bir xil o'rin olsin.

## Yechim (SQL kodi):
```sql
SELECT 
    RANK() OVER (ORDER BY maosh DESC) AS reyting,
    ism, 
    maosh 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
'RANK()' teng qiymatlarga bir xil o'rin beradi, lekin undan keyingi o'rinni sakrab o'tadi (gap hosil qiladi). Masalan, Gulnoza va Botir ikkalasi 4-o'rinni oladi, keyingi Laylo esa 5 emas, 6-o'rinni oladi (1, 2, 3, 4, 4, 6).

## Ishlash natijasi:
```text
reyting |   ism   |    maosh    
---------+---------+-------------
       1 | Nodira  | 18000000.00
       2 | Sherzod | 15000000.00
       3 | Azamat  | 12000000.00
       4 | Gulnoza | 10000000.00
       4 | Botir   | 10000000.00
       6 | Laylo   |  9000000.00
(6 rows)
```


# 406-Topshiriq: Zich o'rin beruvchi (Oraliq qoldirmaydigan): DENSE_RANK()
## Topshiriq sharti:
Bir xil maoshli xodimlardan keyin o'rin sakrab ketmasdan ketma-ket davom etuvchi DENSE_RANK ni qo'llang.

## Yechim (SQL kodi):
```sql
SELECT 
    DENSE_RANK() OVER (ORDER BY maosh DESC) AS zich_reyting,
    ism, 
    maosh 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
'DENSE_RANK()' teng qiymatlarga bir xil raqam beradi, ammo keyingi qatorga hech qanday bo'shliqsiz keyingi sonni beradi (1, 2, 3, 4, 4, 5). Laylo 5-o'rinda chiqadi.

## Ishlash natijasi:
```text
zich_reyting |   ism   |    maosh    
--------------+---------+-------------
            1 | Nodira  | 18000000.00
            2 | Sherzod | 15000000.00
            3 | Azamat  | 12000000.00
            4 | Gulnoza | 10000000.00
            4 | Botir   | 10000000.00
            5 | Laylo   |  9000000.00
(6 rows)
```


# 407-Topshiriq: ROW_NUMBER, RANK va DENSE_RANK taqqoslash
## Topshiriq sharti:
Uchala reyting funksiyasini bitta so'rovda yonma-yon qo'yib farqini tahlil qiling.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    maosh,
    ROW_NUMBER() OVER (ORDER BY maosh DESC) AS rn,
    RANK() OVER (ORDER BY maosh DESC) AS rk,
    DENSE_RANK() OVER (ORDER BY maosh DESC) AS dr
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
Gulnoza va Botir qatorlarida uchala funksiya farqi yaqqol namoyon bo'ladi: ROW_NUMBER: 4 va 5, RANK: 4 va 4 (keyingisi 6), DENSE_RANK: 4 va 4 (keyingisi 5).

## Ishlash natijasi:
```text
ism   |    maosh    | rn | rk | dr 
---------+-------------+----+----+----
 Nodira  | 18000000.00 |  1 |  1 |  1
 Sherzod | 15000000.00 |  2 |  2 |  2
 Azamat  | 12000000.00 |  3 |  3 |  3
 Gulnoza | 10000000.00 |  4 |  4 |  4
 Botir   | 10000000.00 |  5 |  4 |  4
 Laylo   |  9000000.00 |  6 |  6 |  5
(6 rows)
```


# 408-Topshiriq: Guruhlarga teng taqsimlash: NTILE(n)
## Topshiriq sharti:
Xodimlarni ularning oyligi bo'yicha teng 3 ta guruhga (kvartil/savatcha: 1-yuqori, 2-o'rta, 3-quyi) bo'ling.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    maosh,
    NTILE(3) OVER (ORDER BY maosh DESC) AS toifa_raqami 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
'NTILE(k)' saralangan to'plamni imkon qadar teng k ta savatchaga taqsimlaydi. 6 ta xodim 3 ga bo'linib, har bir guruhga aynan 2 tadan xodim to'g'ri keladi.

## Ishlash natijasi:
```text
ism   |    maosh    | toifa_raqami 
---------+-------------+--------------
 Nodira  | 18000000.00 |            1
 Sherzod | 15000000.00 |            1
 Azamat  | 12000000.00 |            2
 Gulnoza | 10000000.00 |            2
 Botir   | 10000000.00 |            3
 Laylo   |  9000000.00 |            3
(6 rows)
```


# 409-Topshiriq: Persentil o'rni: PERCENT_RANK()
## Topshiriq sharti:
Har bir xodim maoshining 0 dan 1 gacha nisbiy reyting persentilini hisoblang.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    maosh,
    ROUND(PERCENT_RANK() OVER (ORDER BY maosh ASC)::NUMERIC, 2) AS persentil_orin 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
'PERCENT_RANK()' formulasi: `(RANK - 1) / (Jami_qatorlar - 1)`. Eng past maosh 0.00, eng yuqori maosh 1.00 qiymatini oladi.

## Ishlash natijasi:
```text
ism   |    maosh    | persentil_orin 
---------+-------------+----------------
 Laylo   |  9000000.00 |           0.00
 Gulnoza | 10000000.00 |           0.20
 Botir   | 10000000.00 |           0.20
 Azamat  | 12000000.00 |           0.60
 Sherzod | 15000000.00 |           0.80
 Nodira  | 18000000.00 |           1.00
(6 rows)
```


# 410-Topshiriq: Kümülyativ taqsimot: CUME_DIST()
## Topshiriq sharti:
Xodimlar maoshining kumulyativ ehtimollik taqsimotini hisoblang.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    maosh,
    ROUND(CUME_DIST() OVER (ORDER BY maosh ASC)::NUMERIC, 2) AS kume_dist 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
'CUME_DIST()' joriy qiymatdan kichik yoki teng bo'lgan qatorlar sonining umumiy qatorlar soniga nisbatini ko'rsatadi (0 dan katta va 1 gacha).

## Ishlash natijasi:
```text
ism   |    maosh    | kume_dist 
---------+-------------+-----------
 Laylo   |  9000000.00 |      0.17
 Gulnoza | 10000000.00 |      0.50
 Botir   | 10000000.00 |      0.50
 Azamat  | 12000000.00 |      0.67
 Sherzod | 15000000.00 |      0.83
 Nodira  | 18000000.00 |      1.00
(6 rows)
```


# 411-Topshiriq: Har bir bo'lim bo'yicha Top-1 xodimni topish (CTE + DENSE_RANK)
## Topshiriq sharti:
Har bir bo'limning eng ko'p maosh oluvchi xodimlarini aniqlang (agar teng bo'lsa barchasi chiqsin).

## Yechim (SQL kodi):
```sql
WITH saralash AS (
    SELECT 
        bolim, 
        ism, 
        maosh,
        DENSE_RANK() OVER (PARTITION BY bolim ORDER BY maosh DESC) AS rk
    FROM xodimlar_wf
)
SELECT bolim, ism, maosh 
FROM saralash 
WHERE rk = 1;
```

## Tushuntirish va Mantiq:
Oynador funksiyalar to'g'ridan-to'g'ri WHERE bandiga qo'yilolmaydi. Shu sababli CTE da DENSE_RANK hisoblanadi va tashqi so'rovda `WHERE rk = 1` qilinadi.

## Ishlash natijasi:
```text
bolim  |   ism   |    maosh    
--------+---------+-------------
 IT     | Nodira  | 18000000.00
 Moliya | Gulnoza | 10000000.00
 Moliya | Botir   | 10000000.00
(3 rows)
```


# 412-Topshiriq: Har bir bo'lim bo'yicha qat'iy Top-1 xodim (ROW_NUMBER)
## Topshiriq sharti:
Agar tenglik bo'lsa ham faqat bitta xodimni tanlash uchun ROW_NUMBER qo'llang.

## Yechim (SQL kodi):
```sql
WITH yagona_top AS (
    SELECT 
        bolim, 
        ism, 
        maosh,
        ROW_NUMBER() OVER (PARTITION BY bolim ORDER BY maosh DESC, id ASC) AS rn
    FROM xodimlar_wf
)
SELECT bolim, ism, maosh 
FROM yagona_top 
WHERE rn = 1;
```

## Tushuntirish va Mantiq:
Tenglik holatlarida `id ASC` ikkinchi darajali saralash parametri qilib qo'yilsa, ROW_NUMBER faqat bitta mutlaq g'olibni ajratadi.

## Ishlash natijasi:
```text
bolim  |   ism   |    maosh    
--------+---------+-------------
 IT     | Nodira  | 18000000.00
 Moliya | Gulnoza | 10000000.00
(2 rows)
```


# 413-Topshiriq: Dublikatlarni aniqlash va tozalash: ROW_NUMBER yordamida
## Topshiriq sharti:
Jadvaldagi bir xil elektron pochtali dublikat yozuvlarning faqat 1-nusxasini saqlab qolish.

## Yechim (SQL kodi):
```sql
CREATE TABLE email_dublikat (id SERIAL PRIMARY KEY, email TEXT);
INSERT INTO email_dublikat (email) VALUES 
('ali@uz.uz'), ('vali@uz.uz'), ('ali@uz.uz'), ('gani@uz.uz'), ('ali@uz.uz');

WITH raqamlash AS (
    SELECT id, email, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id ASC) AS rn
    FROM email_dublikat
)
DELETE FROM email_dublikat
WHERE id IN (SELECT id FROM raqamlash WHERE rn > 1);

SELECT * FROM email_dublikat;
```

## Tushuntirish va Mantiq:
'PARTITION BY email ORDER BY id ASC' dublikatlarga 1, 2, 3 raqamlarini beradi. `rn > 1` bo'lgan barcha ikkinchi va uchinchi nusxalar bir zumda DELETE qilinadi.

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 5
DELETE 2
 id |   email    
----+------------
  1 | ali@uz.uz
  2 | vali@uz.uz
  4 | gani@uz.uz
(3 rows)
```


# 414-Topshiriq: Kodni qisqartirish: WINDOW bandi (WINDOW clause)
## Topshiriq sharti:
Bir nechta oynador funksiya bitta umumiy oynadan foydalansa, 'WINDOW w AS (...)' sintaksisini qo'llang.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    bolim, 
    maosh,
    ROW_NUMBER() OVER w AS rn,
    RANK() OVER w AS rk,
    DENSE_RANK() OVER w AS dr
FROM xodimlar_wf
WINDOW w AS (PARTITION BY bolim ORDER BY maosh DESC);
```

## Tushuntirish va Mantiq:
'WINDOW w AS (shart)' takrorlanuvchi kodni bitta joyda nomlash imkonini beradi. Bu SQL so'rovini ixcham va o'qishga oson qiladi.

## Ishlash natijasi:
```text
ism   | bolim  |    maosh    | rn | rk | dr 
---------+--------+-------------+----+----+----
 Nodira  | IT     | 18000000.00 |  1 |  1 |  1
 Sherzod | IT     | 15000000.00 |  2 |  2 |  2
 Azamat  | IT     | 12000000.00 |  3 |  3 |  3
 Gulnoza | Moliya | 10000000.00 |  1 |  1 |  1
 Botir   | Moliya | 10000000.00 |  2 |  1 |  1
 Laylo   | Moliya |  9000000.00 |  3 |  3 |  2
(6 rows)
```


# 415-Topshiriq: Xodim maoshining bo'lim o'rtacha maoshiga nisbati
## Topshiriq sharti:
Har bir xodim o'z bo'limining o'rtacha maoshidan necha foiz ko'p yoki kam olishini hisoblang.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    bolim, 
    maosh,
    ROUND(AVG(maosh) OVER (PARTITION BY bolim), 2) AS bolim_ortacha,
    ROUND((maosh / AVG(maosh) OVER (PARTITION BY bolim) * 100) - 100, 2) AS farq_foiz
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
Oynador agregatlar (`AVG(...) OVER (PARTITION BY ...)`) orqali har bir qator uchun guruh mezoni biriktiriladi va foiz nisbati to'g'ridan-to'g'ri hisoblanadi.

## Ishlash natijasi:
```text
ism   | bolim  |    maosh    | bolim_ortacha | farq_foiz 
---------+--------+-------------+---------------+-----------
 Sherzod | IT     | 15000000.00 |   15000000.00 |      0.00
 Nodira  | IT     | 18000000.00 |   15000000.00 |     20.00
 Azamat  | IT     | 12000000.00 |   15000000.00 |    -20.00
 Gulnoza | Moliya | 10000000.00 |    9666666.67 |      3.45
 Botir   | Moliya | 10000000.00 |    9666666.67 |      3.45
 Laylo   | Moliya |  9000000.00 |    9666666.67 |     -6.90
(6 rows)
```


# 416-Topshiriq: NTILE yordamida guruhlash: A/B test guruhlarini shakllantirish
## Topshiriq sharti:
Foydalanuvchilarni A va B sinov guruhlariga teng taqsimlash.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    NTILE(2) OVER (ORDER BY id) AS sinov_guruhi 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
Foydalanuvchilar ID bo'yicha teng 2 qismga (1-guruh A, 2-guruh B) ajratiladi.

## Ishlash natijasi:
```text
ism   | sinov_guruhi 
---------+--------------
 Sherzod |            1
 Nodira  |            1
 Azamat  |            1
 Gulnoza |            2
 Botir   |            2
 Laylo   |            2
(6 rows)
```


# 417-Topshiriq: Ikki xil ustun bo'yicha murakkab PARTITION BY
## Topshiriq sharti:
Har bir shahar va bo'lim kesimida xodimlarning o'rnini belgilash.

## Yechim (SQL kodi):
```sql
SELECT 
    shahar, 
    bolim, 
    ism, 
    maosh,
    ROW_NUMBER() OVER (PARTITION BY shahar, bolim ORDER BY maosh DESC) AS orin
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
PARTITION BY bandida bir nechta ustunlar kombinatsiyasi ko'rsatilishi mumkin.

## Ishlash natijasi:
```text
shahar   | bolim  |   ism   |    maosh    | orin 
-----------+--------+---------+-------------+------
 Buxoro    | Moliya | Botir   | 10000000.00 |    1
 Samarqand | IT     | Azamat  | 12000000.00 |    1
 Toshkent  | IT     | Nodira  | 18000000.00 |    1
 Toshkent  | IT     | Sherzod | 15000000.00 |    2
 Toshkent  | Moliya | Gulnoza | 10000000.00 |    1
 Toshkent  | Moliya | Laylo   |  9000000.00 |    2
(6 rows)
```


# 418-Topshiriq: Oynador funksiya bilan guruh minimumi va maksimumini solishtirish
## Topshiriq sharti:
Har bir xodim o'z bo'limining eng kam va eng ko'p maoshidan qanchaga farq qilishini ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    bolim, 
    maosh,
    MIN(maosh) OVER (PARTITION BY bolim) AS bolim_min,
    MAX(maosh) OVER (PARTITION BY bolim) AS bolim_max
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
Bitta satrda xodim maoshi bilan birga uning bo'limi chegaralari ko'rinadi.

## Ishlash natijasi:
```text
ism   | bolim  |    maosh    |  bolim_min  |  bolim_max  
---------+--------+-------------+-------------+-------------
 Sherzod | IT     | 15000000.00 | 12000000.00 | 18000000.00
 Nodira  | IT     | 18000000.00 | 12000000.00 | 18000000.00
 Azamat  | IT     | 12000000.00 | 12000000.00 | 18000000.00
 Gulnoza | Moliya | 10000000.00 |  9000000.00 | 10000000.00
 Botir   | Moliya | 10000000.00 |  9000000.00 | 10000000.00
 Laylo   | Moliya |  9000000.00 |  9000000.00 | 10000000.00
(6 rows)
```


# 419-Topshiriq: Top-N sahifalash (Pagination) ROW_NUMBER yordamida
## Topshiriq sharti:
Sahifa hajmi 2 ta bo'lganda 2-sahifadagi ma'lumotlarni ROW_NUMBER orqali oling.

## Yechim (SQL kodi):
```sql
WITH sahifalangan AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY maosh DESC) AS rn,
        ism, 
        maosh 
    FROM xodimlar_wf
)
SELECT * 
FROM sahifalangan 
WHERE rn BETWEEN 3 AND 4;
```

## Tushuntirish va Mantiq:
OFFSET siz xavfsiz sahifalash: har bir qatorga tartib raqam berilib, oraliq bo'yicha filtrlanadi.

## Ishlash natijasi:
```text
rn |   ism   |    maosh    
----+---------+-------------
  3 | Azamat  | 12000000.00
  4 | Gulnoza | 10000000.00
(2 rows)
```


# 420-Topshiriq: Bo'lim ichidagi xodimlar umumiy foizi
## Topshiriq sharti:
Xodimning maoshi o'z bo'limi jami maosh fondining necha foizini tashkil qiladi?

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    bolim, 
    maosh,
    ROUND((maosh / SUM(maosh) OVER (PARTITION BY bolim) * 100), 2) AS bolim_ichidagi_ulush 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
SUM(maosh) OVER (PARTITION BY bolim) bo'lim fondini hisoblaydi va har bir xodim maoshi shu songa bo'linadi.

## Ishlash natijasi:
```text
ism   | bolim  |    maosh    | bolim_ichidagi_ulush 
---------+--------+-------------+----------------------
 Sherzod | IT     | 15000000.00 |                33.33
 Nodira  | IT     | 18000000.00 |                40.00
 Azamat  | IT     | 12000000.00 |                26.67
 Gulnoza | Moliya | 10000000.00 |                34.48
 Botir   | Moliya | 10000000.00 |                34.48
 Laylo   | Moliya |  9000000.00 |                31.03
(6 rows)
```


# 421-Topshiriq: Oynador funksiyada NULLS FIRST / NULLS LAST
## Topshiriq sharti:
Oynador funksiyada saralash paytida NULL qiymatlar eng orqaga o'tishini ta'minlang.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    maosh,
    RANK() OVER (ORDER BY maosh DESC NULLS LAST) AS rk 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
OVER bandidagi ORDER BY da ham oddiy saralashdagi kabi NULLS LAST qo'llanadi.

## Ishlash natijasi:
```text
ism   |    maosh    | rk 
---------+-------------+----
 Nodira  | 18000000.00 |  1
 Sherzod | 15000000.00 |  2
 Azamat  | 12000000.00 |  3
 Gulnoza | 10000000.00 |  4
 Botir   | 10000000.00 |  4
 Laylo   |  9000000.00 |  6
(6 rows)
```


# 422-Topshiriq: Bir so'rovda har xil PARTITION BY lar ishlatish
## Topshiriq sharti:
Bitta so'rovda ham bo'lim bo'yicha, ham shahar bo'yicha alohida-alohida o'rin berish.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    bolim, 
    shahar, 
    maosh,
    RANK() OVER (PARTITION BY bolim ORDER BY maosh DESC) AS bolim_rk,
    RANK() OVER (PARTITION BY shahar ORDER BY maosh DESC) AS shahar_rk
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
SQL oynador funksiyalarining eng buyuk kuchi: bitta SELECT so'rovida mutlaqo mustaqil turli xil o'lchamlar bo'yicha oynalar parallel hisoblanadi.

## Ishlash natijasi:
```text
ism   | bolim  |  shahar   |    maosh    | bolim_rk | shahar_rk 
---------+--------+-----------+-------------+----------+-----------
 Azamat  | IT     | Samarqand | 12000000.00 |        3 |         1
 Botir   | Moliya | Buxoro    | 10000000.00 |        1 |         1
 Gulnoza | Moliya | Toshkent  | 10000000.00 |        1 |         3
 Laylo   | Moliya | Toshkent  |  9000000.00 |        3 |         4
 Nodira  | IT     | Toshkent  | 18000000.00 |        1 |         1
 Sherzod | IT     | Toshkent  | 15000000.00 |        2 |         2
(6 rows)
```


# 423-Topshiriq: Oynador funksiyalarning bajarilish ketma-ketligi
## Topshiriq sharti:
RDBMS arxitekturasida oynador funksiyalar qaysi bosqichda hisoblanishini tushuntiring.

## Yechim (SQL kodi):
```sql
SELECT 'Oynador funksiyalar WHERE, GROUP BY va HAVING bajarilib bo‘lgandan so‘ng, faqat ORDER BY va LIMIT dan oldin hisoblanadi' AS tartib;
```

## Tushuntirish va Mantiq:
So'rov bajarilish tartibi: 1) FROM, 2) WHERE, 3) GROUP BY, 4) HAVING, 5) WINDOW FUNCTIONS, 6) SELECT, 7) DISTINCT, 8) ORDER BY, 9) LIMIT. Shu sababli WHERE ichida oynador funksiya ishlamaydi.

## Ishlash natijasi:
```text
tartib                                                           
---------------------------------------------------------------------------------------------------------------------------
 Oynador funksiyalar WHERE, GROUP BY va HAVING bajarilib bo‘lgandan so‘ng, faqat ORDER BY va LIMIT dan oldin hisoblanadi
(1 row)
```


# 424-Topshiriq: Har bir bo'limdagi 2-o'rindagi xodimni topish
## Topshiriq sharti:
DENSE_RANK yordamida har bir bo'limning ikkinchi eng yuqori maoshli xodimini aniqlang.

## Yechim (SQL kodi):
```sql
WITH reyting AS (
    SELECT 
        bolim, 
        ism, 
        maosh, 
        DENSE_RANK() OVER (PARTITION BY bolim ORDER BY maosh DESC) AS dr
    FROM xodimlar_wf
)
SELECT bolim, ism, maosh 
FROM reyting 
WHERE dr = 2;
```

## Tushuntirish va Mantiq:
Bo'limlar bo'yicha kumush medal (2-o'rin) sohiblari aniqlanadi.

## Ishlash natijasi:
```text
bolim  |   ism   |    maosh    
--------+---------+-------------
 IT     | Sherzod | 15000000.00
 Moliya | Laylo   |  9000000.00
(2 rows)
```


# 425-Topshiriq: Guruhlar ichida medianani NTILE(2) orqali ajratish
## Topshiriq sharti:
Xodimlarni yuqori yarim va quyi yarim toifalarga ajratish.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    maosh,
    CASE WHEN NTILE(2) OVER (ORDER BY maosh DESC) = 1 THEN 'Yuqori 50%' ELSE 'Quyi 50%' END AS toifa
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
NTILE(2) medianaga nisbatan yuqori va pastki guruhlarni shakllantiradi.

## Ishlash natijasi:
```text
ism   |    maosh    |   toifa   
---------+-------------+-----------
 Nodira  | 18000000.00 | Yuqori 50%
 Sherzod | 15000000.00 | Yuqori 50%
 Azamat  | 12000000.00 | Yuqori 50%
 Gulnoza | 10000000.00 | Quyi 50%
 Botir   | 10000000.00 | Quyi 50%
 Laylo   |  9000000.00 | Quyi 50%
(6 rows)
```


# 426-Topshiriq: STRING_AGG oynador funksiya sifatida
## Topshiriq sharti:
Har bir qatorda butun bo'lim a'zolarining ismlari ro'yxatini ham ko'rsatish.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    bolim, 
    STRING_AGG(ism, ', ') OVER (PARTITION BY bolim) AS bolim_xodimlari 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
Agregat funksiyalar 'OVER' bilan chaqirilganda qatorlarni yo'qotmasdan umumiy ro'yxatni ko'rsatadi.

## Ishlash natijasi:
```text
ism   | bolim  |    bolim_xodimlari     
---------+--------+------------------------
 Sherzod | IT     | Sherzod, Nodira, Azamat
 Nodira  | IT     | Sherzod, Nodira, Azamat
 Azamat  | IT     | Sherzod, Nodira, Azamat
 Gulnoza | Moliya | Gulnoza, Botir, Laylo
 Botir   | Moliya | Gulnoza, Botir, Laylo
 Laylo   | Moliya | Gulnoza, Botir, Laylo
(6 rows)
```


# 427-Topshiriq: ARRAY_AGG oynador funksiya sifatida
## Topshiriq sharti:
Xodim yonida uning bo'limidagi barcha maoshlar massivini ko'rsatish.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    bolim, 
    ARRAY_AGG(maosh) OVER (PARTITION BY bolim) AS maoshlar 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
Oyna bo'yicha massiv to'planadi.

## Ishlash natijasi:
```text
ism   | bolim  |                 maoshlar                  
---------+--------+-------------------------------------------
 Sherzod | IT     | {15000000.00,18000000.00,12000000.00}
 Nodira  | IT     | {15000000.00,18000000.00,12000000.00}
 Azamat  | IT     | {15000000.00,18000000.00,12000000.00}
 Gulnoza | Moliya | {10000000.00,10000000.00,9000000.00}
 Botir   | Moliya | {10000000.00,10000000.00,9000000.00}
 Laylo   | Moliya | {10000000.00,10000000.00,9000000.00}
(6 rows)
```


# 428-Topshiriq: Shartli hisob-kitob: Faqat eng yuqori maosh oluvchiga belgi qo'yish
## Topshiriq sharti:
O'z bo'limida eng yuqori maosh oluvchi xodimga 'Yulduz' belgisini qo'ying.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    bolim, 
    maosh,
    CASE 
        WHEN ROW_NUMBER() OVER (PARTITION BY bolim ORDER BY maosh DESC) = 1 
        THEN '⭐ Bo''lim Yetakchisi' 
        ELSE '' 
    END AS yorliq
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
Oynador funksiya CASE bilan birikib interfeys yorliqlarini dinamik shakllantiradi.

## Ishlash natijasi:
```text
ism   | bolim  |    maosh    |        yorliq         
---------+--------+-------------+-----------------------
 Nodira  | IT     | 18000000.00 | ⭐ Bo'lim Yetakchisi
 Sherzod | IT     | 15000000.00 | 
 Azamat  | IT     | 12000000.00 | 
 Gulnoza | Moliya | 10000000.00 | ⭐ Bo'lim Yetakchisi
 Botir   | Moliya | 10000000.00 | 
 Laylo   | Moliya |  9000000.00 | 
(6 rows)
```


# 429-Topshiriq: COUNT(DISTINCT) oynador funksiyada ishlamasligi va yechimi
## Topshiriq sharti:
PostgreSQL da 'COUNT(DISTINCT ustun) OVER ()' qo'llab-quvvatlanmasligi va uni DENSE_RANK bilan hal qilish.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    bolim,
    DENSE_RANK() OVER (ORDER BY bolim ASC) + 
    DENSE_RANK() OVER (ORDER BY bolim DESC) - 1 AS jami_noyob_bolimlar 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
SQL standartida oynador funksiya ichida DISTINCT ruxsat etilmaydi. DENSE_RANK ASC + DENSE_RANK DESC - 1 formulasi orqali oynador COUNT(DISTINCT) aniq hisoblab olinadi.

## Ishlash natijasi:
```text
ism   | bolim  | jami_noyob_bolimlar 
---------+--------+---------------------
 Azamat  | IT     |                   2
 Nodira  | IT     |                   2
 Sherzod | IT     |                   2
 Botir   | Moliya |                   2
 Gulnoza | Moliya |                   2
 Laylo   | Moliya |                   2
(6 rows)
```


# 430-Topshiriq: Oynador funksiya ijro rejasi: WindowAgg operatori
## Topshiriq sharti:
EXPLAIN orqali PostgreSQL oynador funksiyalarni qanday hisoblashini ko'ring.

## Yechim (SQL kodi):
```sql
EXPLAIN SELECT ism, ROW_NUMBER() OVER (PARTITION BY bolim ORDER BY maosh DESC) 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
RDBMS avval ma'lumotlarni PARTITION va ORDER ustunlari bo'yicha xotirada saralaydi (Sort), so'ngra 'WindowAgg' operatori orqali oyna bo'ylab bittalab hisoblab chiqadi.

## Ishlash natijasi:
```text
QUERY PLAN                              
----------------------------------------------------------------------
 WindowAgg  (cost=1.14..1.26 rows=6 width=48)
   ->  Sort  (cost=1.14..1.15 rows=6 width=44)
         Sort Key: bolim, maosh DESC
         ->  Seq Scan on xodimlar_wf  (cost=0.00..1.06 rows=6 width=44)
(4 rows)
```


# 431-Topshiriq: Sanalarning ketma-ketlik o'rnini belgilash
## Topshiriq sharti:
Mijozning xarid sanalarini 1-xarid, 2-xarid, 3-xarid deb tartiblang.

## Yechim (SQL kodi):
```sql
SELECT 
    xaridor_id, 
    id AS xarid_id, 
    summa,
    ROW_NUMBER() OVER (PARTITION BY xaridor_id ORDER BY id ASC) AS xarid_tartibi 
FROM xaridlar_s 
WHERE xaridor_id IS NOT NULL;
```

## Tushuntirish va Mantiq:
Mijozning nechanchi marta xarid qilayotgani ROW_NUMBER orqali oson aniqlanadi.

## Ishlash natijasi:
```text
xaridor_id | xarid_id |   summa   | xarid_tartibi 
------------+----------+-----------+---------------
          1 |      101 | 200000.00 |             1
          1 |      102 | 350000.00 |             2
          2 |      103 |  90000.00 |             1
(3 rows)
```


# 432-Topshiriq: Guruh ichidagi yozuvlar soni juft yoki toqligini aniqlash
## Topshiriq sharti:
Bo'limdagi umumiy xodimlar soni toq yoki juftligini tekshirish.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    bolim,
    CASE WHEN COUNT(*) OVER (PARTITION BY bolim) % 2 = 0 THEN 'Juft sonli' ELSE 'Toq sonli' END AS xodimlar_soni_turi 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
Oynador COUNT natijasiga matematik amallarni bevosita qo'llash mumkin.

## Ishlash natijasi:
```text
ism   | bolim  | xodimlar_soni_turi 
---------+--------+--------------------
 Sherzod | IT     | Toq sonli
 Nodira  | IT     | Toq sonli
 Azamat  | IT     | Toq sonli
 Gulnoza | Moliya | Toq sonli
 Botir   | Moliya | Toq sonli
 Laylo   | Moliya | Toq sonli
(6 rows)
```


# 433-Topshiriq: Teskari tartib raqami (Reverse ROW_NUMBER)
## Topshiriq sharti:
Xodimlarga eng kichik maoshdan boshlab 1, 2, 3 tartib berish.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    maosh,
    ROW_NUMBER() OVER (ORDER BY maosh ASC) AS arzon_reyting 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
ORDER BY ASC teskari saralash oynasini ochadi.

## Ishlash natijasi:
```text
ism   |    maosh    | arzon_reyting 
---------+-------------+---------------
 Laylo   |  9000000.00 |             1
 Gulnoza | 10000000.00 |             2
 Botir   | 10000000.00 |             3
 Azamat  | 12000000.00 |             4
 Sherzod | 15000000.00 |             5
 Nodira  | 18000000.00 |             6
(6 rows)
```


# 434-Topshiriq: Oynador funksiyada ifodalar bo'yicha tartiblash
## Topshiriq sharti:
Ism uzunligi bo'yicha reyting berish.

## Yechim (SQL kodi):
```sql
SELECT 
    ism,
    RANK() OVER (ORDER BY LENGTH(ism) DESC) AS ism_uzunligi_rk 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
ORDER BY bandiga istalgan funksiya qo'yilishi mumkin.

## Ishlash natijasi:
```text
ism   | ism_uzunligi_rk 
---------+-----------------
 Gulnoza |               1
 Sherzod |               1
 Nodira  |               3
 Azamat  |               4
 Laylo   |               5
 Botir   |               5
(6 rows)
```


# 435-Topshiriq: Kompaniyadagi umumiy maoshga nisbatan xodim vazni
## Topshiriq sharti:
Har bir xodimning kompaniya umumiy budjetidagi ulush foizi.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    maosh,
    ROUND((maosh / SUM(maosh) OVER () * 100), 2) AS kompaniya_ulush 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
Bo'sh `OVER ()` butun korxona fondini beradi.

## Ishlash natijasi:
```text
ism   |    maosh    | kompaniya_ulush 
---------+-------------+-----------------
 Sherzod | 15000000.00 |           20.27
 Nodira  | 18000000.00 |           24.32
 Azamat  | 12000000.00 |           16.22
 Gulnoza | 10000000.00 |           13.51
 Botir   | 10000000.00 |           13.51
 Laylo   |  9000000.00 |           12.16
(6 rows)
```


# 436-Topshiriq: DENSE_RANK yordamida oylik maosh pog'onalarini aniqlash
## Topshiriq sharti:
Kompaniyada nechta turli xil maosh stavkalari borligini raqamlash.

## Yechim (SQL kodi):
```sql
SELECT DISTINCT 
    DENSE_RANK() OVER (ORDER BY maosh DESC) AS maosh_bosqichi,
    maosh 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
DENSE_RANK va DISTINCT birgalikda maosh toifalarini (Grades) shakllantiradi.

## Ishlash natijasi:
```text
maosh_bosqichi |    maosh    
----------------+-------------
              1 | 18000000.00
              2 | 15000000.00
              3 | 12000000.00
              4 | 10000000.00
              5 |  9000000.00
(5 rows)
```


# 437-Topshiriq: Shahar bo'yicha eng yaxshi xodimlar
## Topshiriq sharti:
Har bir shahardan eng ko'p oylik oluvchi top-1 xodimni tanlang.

## Yechim (SQL kodi):
```sql
WITH shahar_top AS (
    SELECT 
        shahar, ism, maosh,
        ROW_NUMBER() OVER (PARTITION BY shahar ORDER BY maosh DESC) AS rn
    FROM xodimlar_wf
)
SELECT shahar, ism, maosh 
FROM shahar_top 
WHERE rn = 1;
```

## Tushuntirish va Mantiq:
Hududiy eng ilg'or xodimlar ajratib olinadi.

## Ishlash natijasi:
```text
shahar   |   ism   |    maosh    
-----------+---------+-------------
 Buxoro    | Botir   | 10000000.00
 Samarqand | Azamat  | 12000000.00
 Toshkent  | Nodira  | 18000000.00
(3 rows)
```


# 438-Topshiriq: Oynador funksiya bilan guruh o'rtachasidan chetlanish
## Topshiriq sharti:
Xodim maoshining o'z bo'limi o'rtacha maoshidan mutlaq chetlanishi (|x - avg|).

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    bolim, 
    maosh,
    ROUND(ABS(maosh - AVG(maosh) OVER (PARTITION BY bolim)), 2) AS mutlaq_farq 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
ABS() matematik funksiyasi chetlanishning modulini beradi.

## Ishlash natijasi:
```text
ism   | bolim  |    maosh    | mutlaq_farq 
---------+--------+-------------+-------------
 Sherzod | IT     | 15000000.00 |        0.00
 Nodira  | IT     | 18000000.00 |  3000000.00
 Azamat  | IT     | 12000000.00 |  3000000.00
 Gulnoza | Moliya | 10000000.00 |   333333.33
 Botir   | Moliya | 10000000.00 |   333333.33
 Laylo   | Moliya |  9000000.00 |   666666.67
(6 rows)
```


# 439-Topshiriq: NTILE(100) - Persentil savatlari (Percentiles)
## Topshiriq sharti:
Katta ma'lumotlar bazasida mijozlarni 1 dan 100 gacha persentil guruhlariga taqsimlash.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    maosh,
    NTILE(100) OVER (ORDER BY maosh ASC) AS persentil_guruhi 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
NTILE(100) orqali Top-1% mijozlar yoki eng quyi 5% xavfli tranzaksiyalar aniqlanadi.

## Ishlash natijasi:
```text
ism   |    maosh    | persentil_guruhi 
---------+-------------+------------------
 Laylo   |  9000000.00 |                1
 Gulnoza | 10000000.00 |                2
 Botir   | 10000000.00 |                3
 Azamat  | 12000000.00 |                4
 Sherzod | 15000000.00 |                5
 Nodira  | 18000000.00 |                6
(6 rows)
```


# 440-Topshiriq: Oynador funksiya bilan birlamchi kalitli saralash kafolati
## Topshiriq sharti:
Bir xil qiymatlar bo'lganda natija deterministik (qat'iy bir xil) chiqishi uchun id ni qo'shish.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    maosh,
    ROW_NUMBER() OVER (ORDER BY maosh DESC, id ASC) AS qatiy_rn 
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
Agar `ORDER BY maosh DESC` yozilsa, bir xil maoshli xodimlar turli so'rovda har xil o'rinda chiqib qolishi mumkin. `id ASC` deterministik natijani kafolatlaydi.

## Ishlash natijasi:
```text
ism   |    maosh    | qatiy_rn 
---------+-------------+----------
 Nodira  | 18000000.00 |        1
 Sherzod | 15000000.00 |        2
 Azamat  | 12000000.00 |        3
 Gulnoza | 10000000.00 |        4
 Botir   | 10000000.00 |        5
 Laylo   |  9000000.00 |        6
(6 rows)
```


# 441-Topshiriq: Guruh ichida eng kichik maosh oluvchilar (Bottom-1)
## Topshiriq sharti:
Har bir bo'limning eng kam oylik oluvchi xodimlarini aniqlang.

## Yechim (SQL kodi):
```sql
WITH min_xodimlar AS (
    SELECT 
        bolim, ism, maosh,
        ROW_NUMBER() OVER (PARTITION BY bolim ORDER BY maosh ASC) AS rn
    FROM xodimlar_wf
)
SELECT bolim, ism, maosh 
FROM min_xodimlar 
WHERE rn = 1;
```

## Tushuntirish va Mantiq:
ORDER BY maosh ASC orqali har bir bo'limning eng kam maoshi topiladi.

## Ishlash natijasi:
```text
bolim  |  ism   |    maosh    
--------+--------+-------------
 IT     | Azamat | 12000000.00
 Moliya | Laylo  |  9000000.00
(2 rows)
```


# 442-Topshiriq: Bir nechta WINDOW larni zanjirda e'lon qilish
## Topshiriq sharti:
WINDOW bandida bir nechta oynalarni vergul bilan e'lon qilish.

## Yechim (SQL kodi):
```sql
SELECT 
    ism,
    ROW_NUMBER() OVER w1 AS butun_rn,
    ROW_NUMBER() OVER w2 AS bolim_rn
FROM xodimlar_wf
WINDOW 
    w1 AS (ORDER BY maosh DESC),
    w2 AS (PARTITION BY bolim ORDER BY maosh DESC);
```

## Tushuntirish va Mantiq:
Har ikkala oyna alohida nomlanib bitta so'rovda qayta ishlatiladi.

## Ishlash natijasi:
```text
ism   | butun_rn | bolim_rn 
---------+----------+----------
 Nodira  |        1 |        1
 Sherzod |        2 |        2
 Azamat  |        3 |        3
 Gulnoza |        4 |        1
 Botir   |        5 |        2
 Laylo   |        6 |        3
(6 rows)
```


# 443-Topshiriq: Oyna doirasida mavjud xodimlar soniga qarab bonus foizi
## Topshiriq sharti:
Kichik jamoalarga (3 tadan kam xodim) 10% bonus, kattalariga 5% bonus tayinlash.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    bolim,
    CASE 
        WHEN COUNT(*) OVER (PARTITION BY bolim) <= 3 THEN '10% Bonus' 
        ELSE '5% Bonus' 
    END AS bonus_toifasi
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
Oyna natijasi biznes mantiqiy ifodalarida to'liq ishlaydi.

## Ishlash natijasi:
```text
ism   | bolim  | bonus_toifasi 
---------+--------+---------------
 Sherzod | IT     | 10% Bonus
 Nodira  | IT     | 10% Bonus
 Azamat  | IT     | 10% Bonus
 Gulnoza | Moliya | 10% Bonus
 Botir   | Moliya | 10% Bonus
 Laylo   | Moliya | 10% Bonus
(6 rows)
```


# 444-Topshiriq: Mijozning eng katta va eng kichik xaridi nisbati
## Topshiriq sharti:
Har bir mijoz uchun uning eng yirik xaridi eng kichik xaridadan necha barobar kattaligini toping.

## Yechim (SQL kodi):
```sql
SELECT 
    DISTINCT xaridor_id,
    MAX(summa) OVER (PARTITION BY xaridor_id) AS eng_katta,
    MIN(summa) OVER (PARTITION BY xaridor_id) AS eng_kichik,
    ROUND(MAX(summa) OVER (PARTITION BY xaridor_id) / MIN(summa) OVER (PARTITION BY xaridor_id), 2) AS nisbat
FROM xaridlar_s 
WHERE xaridor_id IS NOT NULL;
```

## Tushuntirish va Mantiq:
Oynador MIN va MAX orqali nisbatlar olinadi.

## Ishlash natijasi:
```text
xaridor_id | eng_katta | eng_kichik | nisbat 
------------+-----------+------------+--------
          1 | 350000.00 |  200000.00 |   1.75
          2 |  90000.00 |   90000.00 |   1.00
(2 rows)
```


# 445-Topshiriq: ROW_NUMBER va OFFSET taqqoslash
## Topshiriq sharti:
Keyset vs ROW_NUMBER sahifalash unumdorligi.

## Yechim (SQL kodi):
```sql
SELECT 'ROW_NUMBER sahifalash butun jadvalni saralashni talab qiladi, Keyset esa indeks bo‘yicha to‘g‘ridan-to‘g‘ri sakraydi' AS tahlil;
```

## Tushuntirish va Mantiq:
Katta jadvallarda (millionlab qatorlar) ROW_NUMBER() bilan sahifalash ham saralash (Sort) talab qilgani sababli Keyset pagination ga qaraganda sekinroqdir.

## Ishlash natijasi:
```text
tahlil                                                  
---------------------------------------------------------------------------------------------------------
 ROW_NUMBER sahifalash butun jadvalni saralashni talab qiladi, Keyset esa indeks bo‘yicha to‘g‘ridan-to‘g‘ri sakraydi
(1 row)
```


# 446-Topshiriq: Xodimning o'z bo'limidagi reytingini matn shaklida chiqarish
## Topshiriq sharti:
'1-o'rin (18M)', '2-o'rin (15M)' ko'rinishida formatlash.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    bolim,
    RANK() OVER (PARTITION BY bolim ORDER BY maosh DESC) || '-o''rin (' || (maosh / 1000000)::INT || 'M)' AS formatli_orin
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
Reyting soni boshqa ustunlar bilan birlashtiriladi.

## Ishlash natijasi:
```text
ism   | bolim  |  formatli_orin  
---------+--------+-----------------
 Nodira  | IT     | 1-o'rin (18M)
 Sherzod | IT     | 2-o'rin (15M)
 Azamat  | IT     | 3-o'rin (12M)
 Gulnoza | Moliya | 1-o'rin (10M)
 Botir   | Moliya | 1-o'rin (10M)
 Laylo   | Moliya | 3-o'rin (9M)
(6 rows)
```


# 447-Topshiriq: CUME_DIST orqali kam ta'minlangan qatlamni aniqlash
## Topshiriq sharti:
Maoshi kompaniyadagi xodimlarning 30 foizidan kam bo'lgan xodimlarni belgilash.

## Yechim (SQL kodi):
```sql
WITH taqsimot AS (
    SELECT 
        ism, maosh,
        CUME_DIST() OVER (ORDER BY maosh ASC) AS cd
    FROM xodimlar_wf
)
SELECT ism, maosh, cd 
FROM taqsimot 
WHERE cd <= 0.30;
```

## Tushuntirish va Mantiq:
CUME_DIST bo'yicha kambag'allik yoki quyi qatlam tahlili amalga oshiriladi.

## Ishlash natijasi:
```text
ism  |   maosh    |        cd         
-------+------------+-------------------
 Laylo | 9000000.00 | 0.166666666666667
(1 row)
```


# 448-Topshiriq: Ikki xil ustun bo'yicha bir vaqtda DENSE_RANK
## Topshiriq sharti:
Ham maosh, ham ism alifbosi bo'yicha alohida o'rin berish.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    DENSE_RANK() OVER (ORDER BY maosh DESC) AS maosh_rk,
    DENSE_RANK() OVER (ORDER BY ism ASC) AS alifbo_rk
FROM xodimlar_wf;
```

## Tushuntirish va Mantiq:
Turli mezonlar bo'yicha indekslash.

## Ishlash natijasi:
```text
ism   | maosh_rk | alifbo_rk 
---------+----------+-----------
 Azamat  |        3 |         1
 Botir   |        4 |         2
 Gulnoza |        4 |         3
 Laylo   |        5 |         4
 Nodira  |        1 |         5
 Sherzod |        2 |         6
(6 rows)
```


# 449-Topshiriq: Oynador funksiya natijasini boshqa oynador funksiyada ishlatish mumkinmi?
## Topshiriq sharti:
Nega oynador funksiyalar bir-birining ichiga joylanmasligini (nesting) tushuntiring.

## Yechim (SQL kodi):
```sql
SELECT 'Window funksiyalarni ichma-ich yozish taqiqlanadi (masalan: RANK() OVER (ORDER BY COUNT(*) OVER())). Buni faqat CTE orqali bosqichma-bosqich hal qilish mumkin' AS qoida;
```

## Tushuntirish va Mantiq:
SQL spetsifikatsiyasi bo'yicha oynador funksiya ichiga ikkinchi oynador funksiya qo'yish sintaktik xatodir. Bunday hollarda birinchi oynador funksiya CTE ichida olinadi, ikkinchisi tashqarida qo'llanadi.

## Ishlash natijasi:
```text
qoida                                                                                            
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Window funksiyalarni ichma-ich yozish taqiqlanadi (masalan: RANK() OVER (ORDER BY COUNT(*) OVER())). Buni faqat CTE orqali bosqichma-bosqich hal qilish mumkin
(1 row)
```


# 450-Topshiriq: Korporativ Oynador Funksiya: Kadrlar attestatsiyasi va reyting tizimi
## Topshiriq sharti:
Kompaniyaning barcha bo'limlari bo'yicha xodimlarning maoshi, bo'limdagi o'rni, bo'lim fondidagi ulushi va kompaniya miqyosidagi o'rnini yagona oynador tahliliy hisobotda jamlang.

## Yechim (SQL kodi):
```sql
SELECT 
    bolim,
    ism,
    maosh,
    ROW_NUMBER() OVER (PARTITION BY bolim ORDER BY maosh DESC, id ASC) AS bolim_ichki_orni,
    DENSE_RANK() OVER (ORDER BY maosh DESC) AS umumiy_kompaniya_orni,
    ROUND((maosh / SUM(maosh) OVER (PARTITION BY bolim) * 100), 2) AS bolim_fondi_ulushi_foiz,
    ROUND((maosh / AVG(maosh) OVER (PARTITION BY bolim) * 100) - 100, 2) AS bolim_ortachasidan_farq_foiz,
    NTILE(4) OVER (ORDER BY maosh DESC) AS korxona_kvartili
FROM xodimlar_wf
ORDER BY bolim ASC, bolim_ichki_orni ASC;
```

## Tushuntirish va Mantiq:
Ushbu korporativ so'rov HR va boshqaruv tahlili (HR Analytics) uchun to'liq tahliliy manzarani taqdim etadi: har bir xodim bo'lim ichida va butun korxona miqyosida o'z o'rnini (ROW_NUMBER, DENSE_RANK), o'z jamoasi budjetiga ta'sirini (SUM OVER) va xodimlar kvartilidagi o'rnini (NTILE) bir zumda ko'ra oladi.

## Ishlash natijasi:
```text
bolim  |   ism   |    maosh    | bolim_ichki_orni | umumiy_kompaniya_orni | bolim_fondi_ulushi_foiz | bolim_ortachasidan_farq_foiz | korxona_kvartili 
--------+---------+-------------+------------------+-----------------------+-------------------------+------------------------------+------------------
 IT     | Nodira  | 18000000.00 |                1 |                     1 |                   40.00 |                        20.00 |                1
 IT     | Sherzod | 15000000.00 |                2 |                     2 |                   33.33 |                         0.00 |                1
 IT     | Azamat  | 12000000.00 |                3 |                     3 |                   26.67 |                       -20.00 |                2
 Moliya | Gulnoza | 10000000.00 |                1 |                     4 |                   34.48 |                         3.45 |                2
 Moliya | Botir   | 10000000.00 |                2 |                     4 |                   34.48 |                         3.45 |                3
 Moliya | Laylo   |  9000000.00 |                3 |                     5 |                   31.03 |                        -6.90 |                4
(6 rows)
```

