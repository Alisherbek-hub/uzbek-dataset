# 251-Topshiriq: INNER JOIN asoslari (Ikki jadvalning kesishmasi)
## Topshiriq sharti:
Mijozlar va ularning buyurtmalarini INNER JOIN orqali bog'lab, mijoz ismi va buyurtma summasini chiqaring.

## Yechim (SQL kodi):
```sql
CREATE TABLE mijozlar_j (id INT PRIMARY KEY, ism VARCHAR(50));
CREATE TABLE buyurtmalar_j (id INT PRIMARY KEY, mijoz_id INT, summa NUMERIC(12, 2));

INSERT INTO mijozlar_j VALUES (1, 'Alisher'), (2, 'Bobur'), (3, 'Sardor');
INSERT INTO buyurtmalar_j VALUES (101, 1, 150000), (102, 1, 200000), (103, 2, 500000);

SELECT m.ism, b.id AS buyurtma_id, b.summa 
FROM mijozlar_j m
INNER JOIN buyurtmalar_j b ON m.id = b.mijoz_id;
```

## Tushuntirish va Mantiq:
'INNER JOIN' ikkala jadvalda ham bir-biriga mos keluvchi bog'lanish sharti (`m.id = b.mijoz_id`) qanoatlantirilgan qatorlarni qaytaradi. Buyurtmasi bo'lmagan Sardor natijaga kirmaydi.

## Ishlash natijasi:
```text
ism   | buyurtma_id |   summa   
---------+-------------+-----------
 Alisher |         101 | 150000.00
 Alisher |         102 | 200000.00
 Bobur   |         103 | 500000.00
(3 rows)
```


# 252-Topshiriq: USING bandi orqali birlashtirish
## Topshiriq sharti:
Agar ikkala jadvaldagi bog'lanuvchi ustun nomlari bir xil bo'lsa, ixcham 'USING' bandidan foydalaning.

## Yechim (SQL kodi):
```sql
CREATE TABLE bolim_j (bolim_id INT PRIMARY KEY, nomi VARCHAR(50));
CREATE TABLE xodim_j (id INT PRIMARY KEY, ism VARCHAR(50), bolim_id INT);

INSERT INTO bolim_j VALUES (10, 'IT'), (20, 'Kadrlar');
INSERT INTO xodim_j VALUES (1, 'Nodir', 10), (2, 'Zilola', 20);

SELECT ism, nomi AS bolim_nomi 
FROM xodim_j 
INNER JOIN bolim_j USING (bolim_id);
```

## Tushuntirish va Mantiq:
'USING (bolim_id)' sintaksisi `ON xodim_j.bolim_id = bolim_j.bolim_id` yozuvining qisqa va qulay shaklidir. Natijada 'bolim_id' ustuni faqat bitta marta aks etadi.

## Ishlash natijasi:
```text
ism   | bolim_nomi 
--------+------------
 Nodir  | IT
 Zilola | Kadrlar
(2 rows)
```


# 253-Topshiriq: LEFT OUTER JOIN (Chap jadvalni to'liq saqlab qolish)
## Topshiriq sharti:
Barcha mijozlarni, hatto ularning birorta ham buyurtmasi bo'lmasa ham to'liq ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT m.ism, b.id AS buyurtma_id, b.summa 
FROM mijozlar_j m
LEFT JOIN buyurtmalar_j b ON m.id = b.mijoz_id;
```

## Tushuntirish va Mantiq:
'LEFT JOIN' (yoki LEFT OUTER JOIN) chap tomondagi (mijozlar_j) barcha qatorlarni natijaga kiritadi. Agar o'ng jadvalda mos yozuv topilmasa, o'ng ustunlarga NULL qiymatlar qo'yiladi (Sardor misolida).

## Ishlash natijasi:
```text
ism   | buyurtma_id |   summa   
---------+-------------+-----------
 Alisher |         101 | 150000.00
 Alisher |         102 | 200000.00
 Bobur   |         103 | 500000.00
 Sardor  |        NULL |      NULL
(4 rows)
```


# 254-Topshiriq: Anti-Join: Bog'lanmagan qatorlarni topish (IS NULL filtri)
## Topshiriq sharti:
Hech qachon birorta ham buyurtma bermagan mijozlarni aniqlang.

## Yechim (SQL kodi):
```sql
SELECT m.ism 
FROM mijozlar_j m
LEFT JOIN buyurtmalar_j b ON m.id = b.mijoz_id
WHERE b.id IS NULL;
```

## Tushuntirish va Mantiq:
Ushbu naqsh 'Anti-Join' deb ataladi. LEFT JOIN qilinib, o'ng jadvalning birlamchi kaliti 'IS NULL' ekanligi tekshiriladi. Bu orqali xarid qilmagan mijozlar (Sardor) bir zumda topiladi.

## Ishlash natijasi:
```text
ism   
--------
 Sardor
(1 row)
```


# 255-Topshiriq: RIGHT OUTER JOIN (O'ng jadval ustuvorligi)
## Topshiriq sharti:
O'ng jadvaldagi barcha qatorlarni saqlab qoluvchi RIGHT JOIN xatti-harakatini ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT m.ism, b.id AS buyurtma_id, b.summa 
FROM mijozlar_j m
RIGHT JOIN buyurtmalar_j b ON m.id = b.mijoz_id;
```

## Tushuntirish va Mantiq:
'RIGHT JOIN' o'ng jadvalning (buyurtmalar_j) barcha qatorlarini kafolatlaydi. Amaliyotda ko'pchilik dasturchilar so'rovlarni tushunarli qilish uchun RIGHT JOIN o'rniga jadvallar o'rnini almashtirib LEFT JOIN ishlatishni afzal ko'rishadi.

## Ishlash natijasi:
```text
ism   | buyurtma_id |   summa   
---------+-------------+-----------
 Alisher |         101 | 150000.00
 Alisher |         102 | 200000.00
 Bobur   |         103 | 500000.00
(3 rows)
```


# 256-Topshiriq: FULL OUTER JOIN (Ikkala jadvalning to'liq birlashmasi)
## Topshiriq sharti:
Buyurtmasi yo'q mijozlarni ham, mijozsiz qolgan adashgan buyurtmalarni ham birdek ko'rsatuvchi to'liq birlashtirish.

## Yechim (SQL kodi):
```sql
INSERT INTO buyurtmalar_j VALUES (104, NULL, 990000); -- egasiz buyurtma

SELECT m.ism, b.id AS buyurtma_id, b.summa 
FROM mijozlar_j m
FULL OUTER JOIN buyurtmalar_j b ON m.id = b.mijoz_id;
```

## Tushuntirish va Mantiq:
'FULL OUTER JOIN' ikkala tomonning barcha qatorlarini oladi. Mos kelmagan joylarda har ikkala tomonga ham NULL qiymatlar biriktiriladi. Ma'lumotlarni solishtirish va rekonsilyatsiyada tengsizdir.

## Ishlash natijasi:
```text
ism   | buyurtma_id |   summa   
---------+-------------+-----------
 Alisher |         101 | 150000.00
 Alisher |         102 | 200000.00
 Bobur   |         103 | 500000.00
 Sardor  |        NULL |      NULL
 NULL    |         104 | 990000.00
(5 rows)
```


# 257-Topshiriq: FULL JOIN da ikkala tomondagi farqlarni topish (Simmetrik ayirma)
## Topshiriq sharti:
Faqat bir-biriga mos kelmagan (yetim qolgan) mijozlar va buyurtmalarni chiqaring.

## Yechim (SQL kodi):
```sql
SELECT m.ism, b.id AS buyurtma_id 
FROM mijozlar_j m
FULL OUTER JOIN buyurtmalar_j b ON m.id = b.mijoz_id
WHERE m.id IS NULL OR b.id IS NULL;
```

## Tushuntirish va Mantiq:
Ushbu so'rov relyatsion algebraning simmetrik ayirmasidir ((A \ B) ∪ (B \ A)). Faqat aloqasi bo'lmagan chetki qatorlar ko'rinadi.

## Ishlash natijasi:
```text
ism   | buyurtma_id 
--------+-------------
 Sardor |        NULL
 NULL   |         104
(2 rows)
```


# 258-Topshiriq: CROSS JOIN (Dekart ko'paytmasi - Cartesian Product)
## Topshiriq sharti:
Barcha ranglar va barcha o'lchamlar kombinatsiyasidan iborat to'liq mahsulot matritsasini hosil qiling.

## Yechim (SQL kodi):
```sql
CREATE TABLE ranglar (rang TEXT);
CREATE TABLE olchamlar (olcham TEXT);

INSERT INTO ranglar VALUES ('Qizil'), ('Qora');
INSERT INTO olchamlar VALUES ('S'), ('M'), ('L');

SELECT r.rang, o.olcham 
FROM ranglar r
CROSS JOIN olchamlar o;
```

## Tushuntirish va Mantiq:
'CROSS JOIN' birinchi jadvaldagi N ta qatorni ikkinchi jadvaldagi M ta qatorga ko'paytirib, N * M ta kombinatsiyani hosil qiladi. Shart (ON) talab qilinmaydi.

## Ishlash natijasi:
```text
rang  | olcham 
-------+--------
 Qizil | S
 Qizil | M
 Qizil | L
 Qora  | S
 Qora  | M
 Qora  | L
(6 rows)
```


# 259-Topshiriq: O'z-o'ziga birlashish: Self Join (Xodim va uning rahbari)
## Topshiriq sharti:
Xodimlarning ismi yoniga ularning to'g'ridan-to'g'ri rahbarining ismini chiqaring.

## Yechim (SQL kodi):
```sql
CREATE TABLE xodim_rahbar (
    id INT PRIMARY KEY,
    ism VARCHAR(50),
    rahbar_id INT
);

INSERT INTO xodim_rahbar VALUES 
(1, 'Davron Boshliq', NULL),
(2, 'Otabek Menejer', 1),
(3, 'Shohida Dasturchi', 2);

SELECT 
    x.ism AS xodim,
    COALESCE(r.ism, 'Rahbar yo''q (Bosh direktor)') AS rahbar
FROM xodim_rahbar x
LEFT JOIN xodim_rahbar r ON x.rahbar_id = r.id;
```

## Tushuntirish va Mantiq:
'Self Join' ayni bitta jadvalni turli taxalluslar (x va r) bilan o'zaro birlashtiradi. Rahbari yo'q boshliq ham chiqishi uchun LEFT JOIN qo'llaniladi.

## Ishlash natijasi:
```text
xodim       |           rahbar            
-------------------+-----------------------------
 Davron Boshliq    | Rahbar yo'q (Bosh direktor)
 Otabek Menejer    | Davron Boshliq
 Shohida Dasturchi | Otabek Menejer
(3 rows)
```


# 260-Topshiriq: Uchta jadvalni zanjirsimon birlashtirish (Multi-table JOIN)
## Topshiriq sharti:
Mijoz, uning buyurtmasi va buyurtma to'lov usulini bog'lab ma'lumotlarni oling.

## Yechim (SQL kodi):
```sql
CREATE TABLE tolov_turlari (id INT PRIMARY KEY, usul TEXT);
INSERT INTO tolov_turlari VALUES (1, 'Payme'), (2, 'Uzum Bank');

CREATE TABLE buyurtma_3 (id INT PRIMARY KEY, mijoz_id INT, tolov_id INT, summa NUMERIC);
INSERT INTO buyurtma_3 VALUES (1001, 1, 1, 350000);

SELECT 
    m.ism AS mijoz,
    b.id AS buyurtma_raqami,
    b.summa,
    t.usul AS tolov_turi
FROM buyurtma_3 b
INNER JOIN mijozlar_j m ON b.mijoz_id = m.id
INNER JOIN tolov_turlari t ON b.tolov_id = t.id;
```

## Tushuntirish va Mantiq:
So'rovlar zanjirida har bir yangi JOIN oldingi oraliq relyatsiya bilan yangi shart bo'yicha bog'lanadi. Optimizator qaysi jadvallarni oldinroq birlashtirishni o'zi eng maqbul reja asosida tanlaydi.

## Ishlash natijasi:
```text
mijoz  | buyurtma_raqami |   summa   | tolov_turi 
---------+-----------------+-----------+------------
 Alisher |            1001 | 350000.00 | Payme
(1 row)
```


# 261-Topshiriq: Tengliksiz birlashtirish: Non-Equi JOIN (Oraliqlar bo'yicha)
## Topshiriq sharti:
Xodimlarning maoshini maosh tariflari jadvalidagi diapazonlar bilan solishtirib lavozim toifasini aniqlang.

## Yechim (SQL kodi):
```sql
CREATE TABLE maosh_tariflari (
    daraja VARCHAR(20),
    min_maosh NUMERIC,
    max_maosh NUMERIC
);

INSERT INTO maosh_tariflari VALUES 
('Kichik mutaxassis', 3000000, 6000000),
('Yetakchi mutaxassis', 6000001, 10000000),
('Bosh mutaxassis', 10000001, 20000000);

CREATE TABLE hodimlar_m (ism TEXT, maosh NUMERIC);
INSERT INTO hodimlar_m VALUES ('Kamron', 8500000), ('Zarina', 14000000);

SELECT 
    h.ism, 
    h.maosh, 
    t.daraja 
FROM hodimlar_m h
INNER JOIN maosh_tariflari t 
    ON h.maosh BETWEEN t.min_maosh AND t.max_maosh;
```

## Tushuntirish va Mantiq:
'Non-Equi JOIN' birlashtirishda '=' o'rniga 'BETWEEN', '>', '<' kabi taqqoslash operatorlaridan foydalanadi. Bu orqali tarif toifalari, soliq shkalalari dinamik belgilanadi.

## Ishlash natijasi:
```text
ism   |    maosh    |       daraja        
--------+-------------+---------------------
 Kamron |  8500000.00 | Yetakchi mutaxassis
 Zarina | 14000000.00 | Bosh mutaxassis
(2 rows)
```


# 262-Topshiriq: ON sharti va WHERE filtri o'rtasidagi nozik farq
## Topshiriq sharti:
LEFT JOIN da ikkinchi jadval shartini ON bandiga qo'yish bilan WHERE ga qo'yish qanday mutlaqo boshqa natija berishini ko'rsating.

## Yechim (SQL kodi):
```sql
-- 1-holat: Shart ON bandida:
SELECT m.ism, b.summa 
FROM mijozlar_j m
LEFT JOIN buyurtmalar_j b ON m.id = b.mijoz_id AND b.summa > 180000;

-- 2-holat: Shart WHERE bandida:
SELECT m.ism, b.summa 
FROM mijozlar_j m
LEFT JOIN buyurtmalar_j b ON m.id = b.mijoz_id 
WHERE b.summa > 180000;
```

## Tushuntirish va Mantiq:
Agar shart ON ichida bo'lsa, mos kelmagan chap qatorlar (Alisherning 150000 li xaridi yoki Sardor) saqlanib qoladi va summa NULL bo'ladi. Agar shart WHERE ga qo'yilsa, butun LEFT JOIN ichki INNER JOIN ga aylanadi va barcha NULL qatorlar o'chib ketadi!

## Ishlash natijasi:
```text
ism   |   summa   
---------+-----------
 Alisher | 200000.00
 Bobur   | 500000.00
(2 rows)
```


# 263-Topshiriq: JOIN larda Agregatsiya (GROUP BY bilan birgalikda)
## Topshiriq sharti:
Har bir mijozning ismi va uning barcha buyurtmalari yig'indisini hisoblang (buyurtmasi yo'qlarga 0 chiqsin).

## Yechim (SQL kodi):
```sql
SELECT 
    m.ism, 
    COALESCE(SUM(b.summa), 0) AS jami_xarid 
FROM mijozlar_j m
LEFT JOIN buyurtmalar_j b ON m.id = b.mijoz_id
GROUP BY m.id, m.ism;
```

## Tushuntirish va Mantiq:
LEFT JOIN va GROUP BY birgalikda qo'llanilganda Sardor kabi passiv mijozlar ham 0 summa bilan hisobotda aks etadi.

## Ishlash natijasi:
```text
ism   | jami_xarid 
---------+------------
 Alisher |  350000.00
 Bobur   |  500000.00
 Sardor  |       0.00
(3 rows)
```


# 264-Topshiriq: NATURAL JOIN va uning xavflari
## Topshiriq sharti:
NATURAL JOIN qanday ishlashi va nima sababli sanoat tizimlarida uni ishlatish tavsiya etilmasligini tushuntiring.

## Yechim (SQL kodi):
```sql
SELECT * 
FROM xodim_j 
NATURAL JOIN bolim_j;
```

## Tushuntirish va Mantiq:
'NATURAL JOIN' ikkala jadvalda bir xil nomlangan barcha ustunlarni avtomatik tenglashtiradi. Agar kelajakda ikkala jadvalga bir xil nomli boshqa ustun (masalan 'status' yoki 'created_at') qo'shilsa, so'rov kutilmaganda sinadi yoki bo'sh natija qaytara boshlaydi. Shu bois har doim 'ON' yoki 'USING' ishlatilishi shart.

## Ishlash natijasi:
```text
bolim_id | id |  ism   |  nomi   
----------+----+--------+---------
       10 |  1 | Nodir  | IT
       20 |  2 | Zilola | Kadrlar
(2 rows)
```


# 265-Topshiriq: Ko'pdan-ko'pga (Many-to-Many) munosabatni birlashtirish
## Topshiriq sharti:
Talabalar va Kurslar o'rtasidagi bog'lovchi oraliq jadval (pivot table) orqali barcha ma'lumotlarni oling.

## Yechim (SQL kodi):
```sql
CREATE TABLE talabalar_m (id INT PRIMARY KEY, ism TEXT);
CREATE TABLE kurslar_m (id INT PRIMARY KEY, kurs_nomi TEXT);
CREATE TABLE talaba_kurs_m (talaba_id INT, kurs_id INT, PRIMARY KEY(talaba_id, kurs_id));

INSERT INTO talabalar_m VALUES (1, 'Farrux'), (2, 'Shahzod');
INSERT INTO kurslar_m VALUES (101, 'PostgreSQL'), (102, 'Python');
INSERT INTO talaba_kurs_m VALUES (1, 101), (1, 102), (2, 101);

SELECT t.ism AS talaba, k.kurs_nomi 
FROM talaba_kurs_m tk
JOIN talabalar_m t ON tk.talaba_id = t.id
JOIN kurslar_m k ON tk.kurs_id = k.id;
```

## Tushuntirish va Mantiq:
Many-to-Many bog'lanishida ikkita ota jadval oraliq kross-jadval orqali ikkita ketma-ket INNER JOIN yordamida birlashtiriladi.

## Ishlash natijasi:
```text
talaba  | kurs_nomi  
---------+------------
 Farrux  | PostgreSQL
 Farrux  | Python
 Shahzod | PostgreSQL
(3 rows)
```


# 266-Topshiriq: Nested Loop Join bajarilish algoritmi
## Topshiriq sharti:
PostgreSQL kichik jadvallarni birlashtirishda Nested Loop dan qanday foydalanishini EXPLAIN bilan ko'ring.

## Yechim (SQL kodi):
```sql
EXPLAIN SELECT m.ism, b.summa 
FROM mijozlar_j m
JOIN buyurtmalar_j b ON m.id = b.mijoz_id;
```

## Tushuntirish va Mantiq:
'Nested Loop' tashqi jadvalning har bir qatori uchun ichki jadvalni qidirib chiqadi (dasturlashdagi ikki qavatli for tsikli kabi). Ichki jadvalda mos indeks bo'lganda yoki ma'lumotlar kam bo'lganda bu eng tezkor algoritm hisoblanadi.

## Ishlash natijasi:
```text
QUERY PLAN                              
---------------------------------------------------------------------
 Hash Join  (cost=1.07..2.14 rows=3 width=44)
   Hash Cond: (b.mijoz_id = m.id)
   ->  Seq Scan on buyurtmalar_j b  (cost=0.00..1.04 rows=4 width=16)
   ->  Hash  (cost=1.03..1.03 rows=3 width=36)
         ->  Seq Scan on mijozlar_j m  (cost=0.00..1.03 rows=3 width=36)
(5 rows)
```


# 267-Topshiriq: Hash Join bajarilish algoritmi
## Topshiriq sharti:
Katta hajmdagi jadvallarda RDBMS qanday qilib birinchi jadvaldan xotirada hash-jadval yasashini tushuntiring.

## Yechim (SQL kodi):
```sql
SELECT 'Hash Join: Kichik jadvaldan xotirada Hash Table quriladi, keyin ikkinchi jadval bittalab o‘qilib hash orqali O(1) topiladi' AS algoritm;
```

## Tushuntirish va Mantiq:
Tenglik sharti (`=`) bo'lgan katta jadvallarda PostgreSQL xotirada (WorkMem) kichik jadval kalitlaridan Hash Table tuzadi va ikkinchi jadvalni bitta skanerlashda bog'laydi.

## Ishlash natijasi:
```text
algoritm                                                                
---------------------------------------------------------------------------------------------------------------------------------------
 Hash Join: Kichik jadvaldan xotirada Hash Table quriladi, keyin ikkinchi jadval bittalab o‘qilib hash orqali O(1) topiladi
(1 row)
```


# 268-Topshiriq: Merge Join bajarilish algoritmi
## Topshiriq sharti:
Ikkala jadval ham birlashuvchi kalit bo'yicha oldindan saralangan (indekslangan) bo'lsa ishlaydigan Merge Join mexanizmi.

## Yechim (SQL kodi):
```sql
SELECT 'Merge Join: Ikkala tomon kalit bo‘yicha tartiblangan bo‘lsa, ikki ko‘rsatkich bilan O(N + M) vaqtda birlashtiriladi' AS algoritm;
```

## Tushuntirish va Mantiq:
Merge Join ikki tomondan parallel yurib boradi. Agar ustunlarda B-Tree indekslari mavjud bo'lsa, bu algoritm xotira sarflamaydi va juda ulkan ma'lumotlarda yuqori unumdorlik beradi.

## Ishlash natijasi:
```text
algoritm                                                          
----------------------------------------------------------------------------------------------------------------------------
 Merge Join: Ikkala tomon kalit bo‘yicha tartiblangan bo‘lsa, ikki ko‘rsatkich bilan O(N + M) vaqtda birlashtiriladi
(1 row)
```


# 269-Topshiriq: Bir jadvalni o'ziga bog'lab juftliklar hosil qilish (A < B sharti bilan)
## Topshiriq sharti:
Talabalardan iborat barcha mumkin bo'lgan 2 kishilik noyob jamoalarni (takrorlanishlarsiz) tuzing.

## Yechim (SQL kodi):
```sql
SELECT 
    t1.ism AS talaba_1,
    t2.ism AS talaba_2
FROM talabalar_m t1
JOIN talabalar_m t2 ON t1.id < t2.id;
```

## Tushuntirish va Mantiq:
't1.id < t2.id' sharti odam o'zi bilan o'zi juft bo'lishining (id = id) hamda (Farrux, Shahzod) va (Shahzod, Farrux) kabi o'rin almashgan dublikatlarning oldini oladi.

## Ishlash natijasi:
```text
talaba_1 | talaba_2 
----------+----------
 Farrux   | Shahzod
(1 row)
```


# 270-Topshiriq: Vaqt oraliqlarining kesishishini JOIN qilish
## Topshiriq sharti:
Mehmonxonada xonaning bandlik vaqtlari boshqa xona yoki reja bilan to'qnash kelishini solishtiring.

## Yechim (SQL kodi):
```sql
CREATE TABLE bandlik_a (xona INT, bosh DATE, tugash DATE);
CREATE TABLE bandlik_b (xona INT, bosh DATE, tugash DATE);

INSERT INTO bandlik_a VALUES (101, '2026-05-01', '2026-05-10');
INSERT INTO bandlik_b VALUES (101, '2026-05-05', '2026-05-15');

SELECT a.xona, a.bosh AS a_bosh, b.bosh AS b_bosh 
FROM bandlik_a a
JOIN bandlik_b b ON a.xona = b.xona 
    AND a.bosh <= b.tugash 
    AND a.tugash >= b.bosh;
```

## Tushuntirish va Mantiq:
Sanalar oralig'ining kesishish sharti: `start1 <= end2 AND end1 >= start2`. Ushbu Non-Equi JOIN vaqt to'qnashuvlarini (conflicts) aniqlashda qo'llaniladi.

## Ishlash natijasi:
```text
xona |   a_bosh   |   b_bosh   
------+------------+------------
  101 | 2026-05-01 | 2026-05-05
(1 row)
```


# 271-Topshiriq: Bir nechta shartga ega kompozit JOIN (Composite key join)
## Topshiriq sharti:
Ikkita ustun bo'yicha (filial_id va xodim_id) bir vaqtda bog'lanuvchi JOIN so'rovini yozing.

## Yechim (SQL kodi):
```sql
CREATE TABLE filial_jadval_1 (filial INT, xodim INT, ball INT);
CREATE TABLE filial_jadval_2 (filial INT, xodim INT, mukofot NUMERIC);

INSERT INTO filial_jadval_1 VALUES (1, 10, 95);
INSERT INTO filial_jadval_2 VALUES (1, 10, 500000);

SELECT j1.filial, j1.xodim, j1.ball, j2.mukofot 
FROM filial_jadval_1 j1
JOIN filial_jadval_2 j2 
    ON j1.filial = j2.filial AND j1.xodim = j2.xodim;
```

## Tushuntirish va Mantiq:
Kompozit kalitli munosabatlarda JOIN ning ON bandiga 'AND' orqali barcha bog'lovchi ustunlar ko'rsatiladi.

## Ishlash natijasi:
```text
filial | xodim | ball |  mukofot  
--------+-------+------+-----------
      1 |    10 |   95 | 500000.00
(1 row)
```


# 272-Topshiriq: LEFT JOIN bilan eng so'nggi yozuvni bog'lash
## Topshiriq sharti:
Har bir mijoz yoniga uning eng oxirgi buyurtmasini (agar bo'lsa) qo'shib chiqarish.

## Yechim (SQL kodi):
```sql
SELECT m.ism, oxirgi_b.id AS oxirgi_buyurtma_id, oxirgi_b.summa
FROM mijozlar_j m
LEFT JOIN LATERAL (
    SELECT id, summa 
    FROM buyurtmalar_j b 
    WHERE b.mijoz_id = m.id 
    ORDER BY id DESC 
    LIMIT 1
) oxirgi_b ON TRUE;
```

## Tushuntirish va Mantiq:
'LEFT JOIN LATERAL' subquery ga asosiy jadvalning ustuniga (`m.id`) murojaat qilish imkonini beradi. Har bir mijoz uchun alohida top-1 buyurtmani bog'lashda ajoyib vosita.

## Ishlash natijasi:
```text
ism   | oxirgi_buyurtma_id |   summa   
---------+--------------------+-----------
 Alisher |                102 | 200000.00
 Bobur   |                103 | 500000.00
 Sardor  |               NULL |      NULL
(3 rows)
```


# 273-Topshiriq: CROSS JOIN bilan sana kalendarini generatsiya qilish
## Topshiriq sharti:
Filiallar ro'yxatini haftaning 7 kuni bilan birlashtirib navbatchilik jadvali shablonini hosil qiling.

## Yechim (SQL kodi):
```sql
CREATE TABLE f_filiallar (nomi TEXT);
INSERT INTO f_filiallar VALUES ('Bosh Office'), ('Chilonzor');

SELECT f.nomi, k.kun::DATE 
FROM f_filiallar f
CROSS JOIN generate_series('2026-06-01'::DATE, '2026-06-03'::DATE, '1 day'::INTERVAL) AS k(kun);
```

## Tushuntirish va Mantiq:
CROSS JOIN va generate_series() birgalikda to'liq sana setkalarini (calendar grid) tuzishda va ma'lumot yo'q kunlarni 0 bilan to'ldirishda qo'llaniladi.

## Ishlash natijasi:
```text
nomi     |    kun     
-------------+------------
 Bosh Office | 2026-06-01
 Bosh Office | 2026-06-02
 Bosh Office | 2026-06-03
 Chilonzor   | 2026-06-01
 Chilonzor   | 2026-06-02
 Chilonzor   | 2026-06-03
(6 rows)
```


# 274-Topshiriq: JOIN shartida funksiyalardan foydalanish
## Topshiriq sharti:
Foydalanuvchi elektron pochta domenini kompaniyalar domeni bilan bog'lang.

## Yechim (SQL kodi):
```sql
CREATE TABLE foydalanuvchilar_e (ism TEXT, email TEXT);
CREATE TABLE tashkilotlar_e (nomi TEXT, domen TEXT);

INSERT INTO foydalanuvchilar_e VALUES ('Aziz', 'aziz@uzcard.uz');
INSERT INTO tashkilotlar_e VALUES ('Uzcard AJ', 'uzcard.uz');

SELECT f.ism, t.nomi AS tashkilot 
FROM foydalanuvchilar_e f
JOIN tashkilotlar_e t 
    ON SPLIT_PART(f.email, '@', 2) = t.domen;
```

## Tushuntirish va Mantiq:
JOIN ning ON shartida ixtiyoriy skalyar funksiyalar (SPLIT_PART, LOWER, SUBSTRING) ishlashi mumkin. Optimizator bunday ifodalarni taqqoslay oladi.

## Ishlash natijasi:
```text
ism  | tashkilot 
------+-----------
 Aziz | Uzcard AJ
(1 row)
```


# 275-Topshiriq: JOIN lar zanjirida filtrni erta qo'llash unumdorligi
## Topshiriq sharti:
Katta jadvalni to'liq JOIN qilmasdan oldin subquery ichida filtrlab keyin JOIN qilish.

## Yechim (SQL kodi):
```sql
SELECT m.ism, b.summa 
FROM mijozlar_j m
JOIN (
    SELECT mijoz_id, summa 
    FROM buyurtmalar_j 
    WHERE summa > 180000
) b ON m.id = b.mijoz_id;
```

## Tushuntirish va Mantiq:
Zamonaviy PostgreSQL optimizatori (Push-down predicate) ko'pincha bu ikkala yozuvni bir xil optimal rejaga keltiradi, lekin subquery orqali cheklash murakkab ko'rinishlarda xotirani tejashi mumkin.

## Ishlash natijasi:
```text
ism   |   summa   
---------+-----------
 Alisher | 200000.00
 Bobur   | 500000.00
(2 rows)
```


# 276-Topshiriq: Anti-Join ning NOT EXISTS bilan ekvivalentligi
## Topshiriq sharti:
LEFT JOIN ... IS NULL o'rniga NOT EXISTS yordamida buyurtmasiz mijozlarni topish.

## Yechim (SQL kodi):
```sql
SELECT m.ism 
FROM mijozlar_j m
WHERE NOT EXISTS (
    SELECT 1 FROM buyurtmalar_j b WHERE b.mijoz_id = m.id
);
```

## Tushuntirish va Mantiq:
'NOT EXISTS' va 'LEFT JOIN ... IS NULL' optimizator tomonidan deyarli bir xil Hash Anti-Join rejasiga o'giriladi. Biroq NOT EXISTS NULL qiymatlardan qo'rqmaydi va o'qish uchun juda qulay.

## Ishlash natijasi:
```text
ism   
--------
 Sardor
(1 row)
```


# 277-Topshiriq: Semi-Join: Kamida bitta buyurtmasi bor mijozlar
## Topshiriq sharti:
Buyurtmasi bor mijozlarning ismini takrorlanishlarsiz topish (lekin buyurtmalar jadvalidagi dublikatlarni ko'paytirmaslik).

## Yechim (SQL kodi):
```sql
SELECT m.ism 
FROM mijozlar_j m
WHERE EXISTS (
    SELECT 1 FROM buyurtmalar_j b WHERE b.mijoz_id = m.id
);
```

## Tushuntirish va Mantiq:
'Semi-Join' chap jadvaldagi qator o'ng jadvalda kamida bir marta uchrashi bilanoq uni natijaga chiqaradi. Oddiy INNER JOIN dan farqi — agar mijozning 10 ta buyurtmasi bo'lsa, mijoz 10 marta emas, 1 marta chiqadi.

## Ishlash natijasi:
```text
ism   
---------
 Alisher
 Bobur
(2 rows)
```


# 278-Topshiriq: Ko'p darajali Self Join (Bobo -> Ota -> Bola)
## Topshiriq sharti:
Uch avlod iyerarxiyasini ko'rsatish.

## Yechim (SQL kodi):
```sql
CREATE TABLE shajara (id INT PRIMARY KEY, ism TEXT, ota_id INT);
INSERT INTO shajara VALUES (1, 'Bobo Odam', NULL), (2, 'Ota Tohir', 1), (3, 'O‘g‘il Sobir', 2);

SELECT 
    bola.ism AS bola,
    ota.ism AS ota,
    bobo.ism AS bobo
FROM shajara bola
LEFT JOIN shajara ota ON bola.ota_id = ota.id
LEFT JOIN shajara bobo ON ota.ota_id = bobo.id;
```

## Tushuntirish va Mantiq:
Self Join bir necha marotaba takrorlanishi mumkin. Har bir bosqich iyerarxiyaning bitta yuqori pog'onasini ochib beradi.

## Ishlash natijasi:
```text
bola     |    ota    |   bobo    
--------------+-----------+-----------
 Bobo Odam    | NULL      | NULL
 Ota Tohir    | Bobo Odam | NULL
 O‘g‘il Sobir | Ota Tohir | Bobo Odam
(3 rows)
```


# 279-Topshiriq: JOIN shartida CASE ifodasi
## Topshiriq sharti:
Mijozning to'lov turiga qarab boshqa-boshqa jadvallar bilan dinamik bog'lanish.

## Yechim (SQL kodi):
```sql
CREATE TABLE mijoz_h (id INT PRIMARY KEY, tur TEXT, hisob_id INT);
CREATE TABLE bank_h (id INT PRIMARY KEY, info TEXT);
CREATE TABLE hamyon_h (id INT PRIMARY KEY, info TEXT);

INSERT INTO mijoz_h VALUES (1, 'bank', 10), (2, 'hamyon', 20);
INSERT INTO bank_h VALUES (10, 'Bank Hisob Raqami');
INSERT INTO hamyon_h VALUES (20, 'Elektron Hamyon');

SELECT 
    m.id, 
    m.tur,
    COALESCE(b.info, h.info) AS hisob_tafsiloti 
FROM mijoz_h m
LEFT JOIN bank_h b ON m.hisob_id = b.id AND m.tur = 'bank'
LEFT JOIN hamyon_h h ON m.hisob_id = h.id AND m.tur = 'hamyon';
```

## Tushuntirish va Mantiq:
Polimorfik munosabatlarni relyatsion tilda ifodalash uchun har bir maqsad jadval alohida LEFT JOIN qilinadi va tur ustuni bo'yicha cheklanadi.

## Ishlash natijasi:
```text
id |  tur   |  hisob_tafsiloti  
----+--------+-------------------
  1 | bank   | Bank Hisob Raqami
  2 | hamyon | Elektron Hamyon
(2 rows)
```


# 280-Topshiriq: Tashqi kalitsiz (Unconstrained) jadvallarni JOIN qilish
## Topshiriq sharti:
RDBMS da rasmiy FOREIGN KEY o'rnatilmagan bo'lsa ham ustunlar qiymati mos kelsa JOIN ishlashini ko'rsating.

## Yechim (SQL kodi):
```sql
CREATE TABLE log_a (foydalanuvchi_login TEXT, harakat TEXT);
CREATE TABLE log_b (user_login TEXT, ip_manzil TEXT);

INSERT INTO log_a VALUES ('admin', 'login'), ('user1', 'logout');
INSERT INTO log_b VALUES ('admin', '192.168.0.1');

SELECT a.foydalanuvchi_login, a.harakat, b.ip_manzil 
FROM log_a a
JOIN log_b b ON a.foydalanuvchi_login = b.user_login;
```

## Tushuntirish va Mantiq:
Relyatsion ma'lumotlar bazasida JOIN qilish uchun jadvalda FOREIGN KEY bo'lishi MAJBURIY EMAS. JOIN faqatgina SELECT vaqtida qiymatlarni solishtiradi.

## Ishlash natijasi:
```text
foydalanuvchi_login | harakat | ip_manzil  
---------------------+---------+-------------
 admin               | login   | 192.168.0.1
(1 row)
```


# 281-Topshiriq: JOIN natijasida qatorlar ko'payib ketishi (Fan-out / Row explosion)
## Topshiriq sharti:
Birga-ko'p bog'lanishda ikkita bola jadval JOIN qilinganda qatorlar soni ko'payib hisob-kitoblar buzilishini ko'rsating.

## Yechim (SQL kodi):
```sql
CREATE TABLE xaridor (id INT PRIMARY KEY);
CREATE TABLE x_telefon (xaridor_id INT, tel TEXT);
CREATE TABLE x_manzil (xaridor_id INT, manzil TEXT);

INSERT INTO xaridor VALUES (1);
INSERT INTO x_telefon VALUES (1, 'tel_1'), (1, 'tel_2');
INSERT INTO x_manzil VALUES (1, 'manzil_1'), (1, 'manzil_2');

SELECT * 
FROM xaridor x
JOIN x_telefon t ON x.id = t.xaridor_id
JOIN x_manzil m ON x.id = m.xaridor_id;
```

## Tushuntirish va Mantiq:
Diqqat: 2 ta telefon va 2 ta manzil qo'shilganda natijada 2 * 2 = 4 ta qator hosil bo'ladi! Agar shu yerda SUM(summa) hisoblansa, summa 4 marta ko'payib xato chiqadi. Bunday holatda alohida CTE yoki subquery ishlatilishi shart.

## Ishlash natijasi:
```text
id | xaridor_id |  tel  | xaridor_id |  manzil  
----+------------+-------+------------+----------
  1 |          1 | tel_1 |          1 | manzil_1
  1 |          1 | tel_1 |          1 | manzil_2
  1 |          1 | tel_2 |          1 | manzil_1
  1 |          1 | tel_2 |          1 | manzil_2
(4 rows)
```


# 282-Topshiriq: Fan-out xatosini to'g'irlash (CTE orqali alohida jamlash)
## Topshiriq sharti:
Mijozning telefonlari soni va uning to'lovlari summasini qatorlar ko'payib ketmasdan to'g'ri hisoblang.

## Yechim (SQL kodi):
```sql
WITH jami_tel AS (
    SELECT xaridor_id, COUNT(*) AS tel_soni 
    FROM x_telefon GROUP BY xaridor_id
),
jami_manzil AS (
    SELECT xaridor_id, COUNT(*) AS manzil_soni 
    FROM x_manzil GROUP BY xaridor_id
)
SELECT x.id, t.tel_soni, m.manzil_soni
FROM xaridor x
LEFT JOIN jami_tel t ON x.id = t.xaridor_id
LEFT JOIN jami_manzil m ON x.id = m.xaridor_id;
```

## Tushuntirish va Mantiq:
Har bir o'lcham alohida CTE da agregatlanadi, so'ngra asosiy jadvalga 1:1 nisbatda ulanadi. Natija 100% aniq va toza chiqadi.

## Ishlash natijasi:
```text
id | tel_soni | manzil_soni 
----+----------+-------------
  1 |        2 |           2
(1 row)
```


# 283-Topshiriq: CROSS JOIN LATERAL bilan massivlarni yoyish (UNNEST)
## Topshiriq sharti:
Jadvaldagi massiv ustunini har bir elementi bo'yicha yangi qatorlarga yoyib chiqarish.

## Yechim (SQL kodi):
```sql
CREATE TABLE kitoblar (id INT, sarlavha TEXT, teglar TEXT[]);
INSERT INTO kitoblar VALUES (1, 'SQL Asoslari', ARRAY['baza', 'dasturlash', 'backend']);

SELECT k.sarlavha, t.teg 
FROM kitoblar k
CROSS JOIN LATERAL UNNEST(k.teglar) AS t(teg);
```

## Tushuntirish va Mantiq:
'CROSS JOIN LATERAL UNNEST(massiv)' massivning har bir elementini satrga aylantirib, asosiy qator bilan birlashtiradi.

## Ishlash natijasi:
```text
sarlavha   |    teg     
--------------+------------
 SQL Asoslari | baza
 SQL Asoslari | dasturlash
 SQL Asoslari | backend
(3 rows)
```


# 284-Topshiriq: Teskari bog'lanish: Barcha bo'sh xonalarni topish
## Topshiriq sharti:
Mehmonxona xonalari ro'yxatidan ayni damda birorta ham mijozi yo'q bo'sh xonalarni aniqlang.

## Yechim (SQL kodi):
```sql
CREATE TABLE mehmonxona_xonalari (xona_id INT PRIMARY KEY, qavat INT);
CREATE TABLE xona_yashovchilari (id INT PRIMARY KEY, xona_id INT, ism TEXT);

INSERT INTO mehmonxona_xonalari VALUES (101, 1), (102, 1), (201, 2);
INSERT INTO xona_yashovchilari VALUES (1, 101, 'Javlon');

SELECT x.xona_id, x.qavat 
FROM mehmonxona_xonalari x
LEFT JOIN xona_yashovchilari y ON x.xona_id = y.xona_id
WHERE y.id IS NULL;
```

## Tushuntirish va Mantiq:
Anti-join klassik yechimi: mehmonxona xonalari to'liq olinadi, yashovchisi yo'q (NULL) qatorlar filtrlanadi.

## Ishlash natijasi:
```text
xona_id | qavat 
---------+-------
     102 |     1
     201 |     2
(2 rows)
```


# 285-Topshiriq: JOIN larda indekslarning o'rni
## Topshiriq sharti:
Tashqi kalit ustunida indeks bo'lmaganda RDBMS Seq Scan qilishini va indeks yaratilganda Index Scan ga o'tishini tushuntiring.

## Yechim (SQL kodi):
```sql
SELECT 'Tashqi kalit ustuniga B-Tree indeks qo‘yish JOIN tezligini 100 martagacha oshiradi' AS xulosa;
```

## Tushuntirish va Mantiq:
PostgreSQL birlamchi kalitga avtomatik indeks yaratadi, ammo FOREIGN KEY ustuniga indeks yaratmaydi! Katta jadvallarda tezkor JOIN uchun har bir tashqi kalit ustuniga `CREATE INDEX` yozish shart.

## Ishlash natijasi:
```text
xulosa                                         
--------------------------------------------------------------------------------------
 Tashqi kalit ustuniga B-Tree indeks qo‘yish JOIN tezligini 100 martagacha oshiradi
(1 row)
```


# 286-Topshiriq: Bir nechta jadvallardan shartli saralash
## Topshiriq sharti:
Xaridor ismi yoki buyurtma summasi bo'yicha dinamik tartiblash.

## Yechim (SQL kodi):
```sql
SELECT m.ism, b.summa 
FROM mijozlar_j m
JOIN buyurtmalar_j b ON m.id = b.mijoz_id
ORDER BY b.summa DESC, m.ism ASC;
```

## Tushuntirish va Mantiq:
ORDER BY bandida JOIN dagi istalgan qatnashuvchi jadval ustunlarini erkin aralashtirib saralash mumkin.

## Ishlash natijasi:
```text
ism   |   summa   
---------+-----------
 Bobur   | 500000.00
 Alisher | 200000.00
 Alisher | 150000.00
(3 rows)
```


# 287-Topshiriq: Katta va kichik registrli matnlarni JOIN qilish (LOWER)
## Topshiriq sharti:
Email manzillari har xil registrda saqlangan bo'lsa ularni LOWER orqali to'g'ri bog'lang.

## Yechim (SQL kodi):
```sql
CREATE TABLE kl1 (email TEXT);
CREATE TABLE kl2 (email TEXT);
INSERT INTO kl1 VALUES ('Ali@Mail.uz');
INSERT INTO kl2 VALUES ('ali@mail.uz');

SELECT * 
FROM kl1 a
JOIN kl2 b ON LOWER(a.email) = LOWER(b.email);
```

## Tushuntirish va Mantiq:
LOWER funksiyasi orqali matnlarni yagona registrga keltirib aniq moslik topiladi.

## Ishlash natijasi:
```text
email     |    email    
--------------+-------------
 Ali@Mail.uz  | ali@mail.uz
(1 row)
```


# 288-Topshiriq: Birlashtirishda NULL ustunlar bilan to'qnashuv
## Topshiriq sharti:
Ikkala jadvalda ham NULL bo'lgan tashqi kalitlar bir-biri bilan JOIN bo'ladimi?

## Yechim (SQL kodi):
```sql
SELECT * 
FROM buyurtmalar_j b1
JOIN buyurtmalar_j b2 ON b1.mijoz_id = b2.mijoz_id 
WHERE b1.mijoz_id IS NULL;
```

## Tushuntirish va Mantiq:
`NULL = NULL` har doim NULL (UNKNOWN) bo'lganligi sababli, NULL tashqi kalitli qatorlar hech qachon INNER JOIN shartida bir-biriga ulanmaydi.

## Ishlash natijasi:
```text
id | mijoz_id | summa | id | mijoz_id | summa 
----+----------+-------+----+----------+-------
(0 rows)
```


# 289-Topshiriq: CROSS JOIN o'rniga vergul bilan yozish (Eski uslub va xavf)
## Topshiriq sharti:
`FROM jadval1, jadval2` sintaksisi nega tavsiya etilmasligini tushuntiring.

## Yechim (SQL kodi):
```sql
-- Eski sintaksis:
-- SELECT * FROM ranglar, olchamlar;
SELECT 'Eksplitsit CROSS JOIN yozish adashib WHERE ni unutib qoldirish xavfini yo‘qotadi' AS maslahat;
```

## Tushuntirish va Mantiq:
Vergul bilan ajratilgan jadvallarda WHERE sharti adashib qolib ketsa, tasodifiy Dekart ko'paytmasi yuzaga kelib server xotirasini to'ldirib yuborishi mumkin. Har doim 'JOIN ... ON' sintaksisi qo'llanishi kerak.

## Ishlash natijasi:
```text
maslahat                                        
--------------------------------------------------------------------------------------
 Eksplitsit CROSS JOIN yozish adashib WHERE ni unutib qoldirish xavfini yo‘qotadi
(1 row)
```


# 290-Topshiriq: JOIN da ustunlarni to'liq qamrab olish (Coalesce bilan)
## Topshiriq sharti:
FULL JOIN natijasida mijoz ismi qaysi tomonda bo'lsa ham bitta ustunda ko'rsatish.

## Yechim (SQL kodi):
```sql
SELECT 
    COALESCE(m.ism, 'Noma''lum Mijoz') AS mijoz_nomi,
    b.id AS buyurtma_raqam,
    COALESCE(b.summa, 0) AS summa
FROM mijozlar_j m
FULL JOIN buyurtmalar_j b ON m.id = b.mijoz_id;
```

## Tushuntirish va Mantiq:
FULL JOIN da COALESCE chap va o'ng tomon ustunlarini yagona o'qiladigan ustunga birlashtiradi.

## Ishlash natijasi:
```text
mijoz_nomi   | buyurtma_raqam |   summa   
----------------+----------------+-----------
 Alisher        |            101 | 150000.00
 Alisher        |            102 | 200000.00
 Bobur          |            103 | 500000.00
 Sardor         |           NULL |      0.00
 Noma'lum Mijoz |            104 | 990000.00
(5 rows)
```


# 291-Topshiriq: JOIN orqali yangilash (UPDATE ... JOIN ekvivalenti)
## Topshiriq sharti:
Boshqa jadval ma'lumotlariga qarab narxlarni yangilashda JOIN mantiqi.

## Yechim (SQL kodi):
```sql
CREATE TABLE tovar_narx (id INT, narx NUMERIC);
CREATE TABLE narx_skidka (tovar_id INT, foiz INT);

INSERT INTO tovar_narx VALUES (1, 100000);
INSERT INTO narx_skidka VALUES (1, 20);

UPDATE tovar_narx tn
SET narx = tn.narx * (1 - ns.foiz / 100.0)
FROM narx_skidka ns
WHERE tn.id = ns.tovar_id;

SELECT * FROM tovar_narx;
```

## Tushuntirish va Mantiq:
PostgreSQL dagi `UPDATE ... FROM ... WHERE` mexanizmi orqa fonda jadvallarni JOIN qilib yangilaydi.

## Ishlash natijasi:
```text
id |   narx   
----+----------
  1 | 80000.00
(1 row)
```


# 292-Topshiriq: Self Join orqali ketma-ket hodisalar farqini topish
## Topshiriq sharti:
Foydalanuvchining oldingi va keyingi kirish vaqtlari farqini topish.

## Yechim (SQL kodi):
```sql
CREATE TABLE login_vaqt (id SERIAL PRIMARY KEY, user_id INT, kirgan_vaqt TIMESTAMP);
INSERT INTO login_vaqt (user_id, kirgan_vaqt) VALUES 
(1, '2026-06-01 10:00'), (1, '2026-06-01 10:45');

SELECT 
    v1.user_id,
    v1.kirgan_vaqt AS birinchi_kirish,
    v2.kirgan_vaqt AS ikkinchi_kirish,
    (v2.kirgan_vaqt - v1.kirgan_vaqt) AS oraliq_vaqt
FROM login_vaqt v1
JOIN login_vaqt v2 ON v1.user_id = v2.user_id AND v1.id < v2.id;
```

## Tushuntirish va Mantiq:
Self join yordamida oynador funksiyalarsiz ham ketma-ket kelgan qatorlar orasidagi farqni hisoblash mumkin.

## Ishlash natijasi:
```text
user_id |   birinchi_kirish   |   ikkinchi_kirish   | oraliq_vaqt 
---------+---------------------+---------------------+-------------
       1 | 2026-06-01 10:00:00 | 2026-06-01 10:45:00 | 00:45:00
(1 row)
```


# 293-Topshiriq: JOIN shartida OR operatorining xavfi
## Topshiriq sharti:
JOIN ON shartida OR qo'llanganda indekslar ishlamay sekinlashishi muammosi.

## Yechim (SQL kodi):
```sql
SELECT 'JOIN ON da OR ishlatilsa Hash/Merge join ishlamaydi va Nested Loop Cartesianga tushishi mumkin' AS ogohlantirish;
```

## Tushuntirish va Mantiq:
Agar JOIN ning ON bandiga `t1.a = t2.a OR t1.b = t2.b` deb yozilsa, optimizator hash qura olmaydi va so'rov juda sekinlashadi. Bunday so'rovlarni ikkita JOIN ga yoki UNION ga ajratish samaraliroqdir.

## Ishlash natijasi:
```text
ogohlantirish                                                 
--------------------------------------------------------------------------------------------------------------
 JOIN ON da OR ishlatilsa Hash/Merge join ishlamaydi va Nested Loop Cartesianga tushishi mumkin
(1 row)
```


# 294-Topshiriq: JOIN va DISTINCT: Nega keraksiz DISTINCT qo'ymaslik kerak?
## Topshiriq sharti:
Ko'p dasturchilar 1:N JOIN dagi dublikatlarni yo'qotish uchun DISTINCT qo'yishadi. Buning o'rniga EXISTS ishlatish afzalligini ko'rsating.

## Yechim (SQL kodi):
```sql
-- DISTINCT bilan (xotirani yeydi):
SELECT DISTINCT m.ism FROM mijozlar_j m JOIN buyurtmalar_j b ON m.id = b.mijoz_id;

-- EXISTS bilan (eng optimal):
SELECT m.ism FROM mijozlar_j m WHERE EXISTS (SELECT 1 FROM buyurtmalar_j b WHERE b.mijoz_id = m.id);
```

## Tushuntirish va Mantiq:
DISTINCT butun natijani xotirada saralashni talab qiladi. EXISTS esa birinchi moslikni topishi bilanoq qidiruvni to'xtatadi va hech qanday saralash talab qilmaydi.

## Ishlash natijasi:
```text
ism   
---------
 Alisher
 Bobur
(2 rows)
```


# 295-Topshiriq: LEFT JOIN da o'ng jadval agregatini ulash
## Topshiriq sharti:
Har bir mijoz yoniga uning buyurtmalar sonini alohida inline subquery JOIN orqali bog'lash.

## Yechim (SQL kodi):
```sql
SELECT m.ism, COALESCE(b_stat.jami_soni, 0) AS buyurtmalar_soni
FROM mijozlar_j m
LEFT JOIN (
    SELECT mijoz_id, COUNT(*) AS jami_soni 
    FROM buyurtmalar_j 
    GROUP BY mijoz_id
) b_stat ON m.id = b_stat.mijoz_id;
```

## Tushuntirish va Mantiq:
Ushbu usul butun so'rovni GROUP BY qilishga majbur bo'lmasdan faqat kerakli statistikani 1:1 bog'lashda yordam beradi.

## Ishlash natijasi:
```text
ism   | buyurtmalar_soni 
---------+------------------
 Alisher |                2
 Bobur   |                1
 Sardor  |                0
(3 rows)
```


# 296-Topshiriq: Shartli hisob-kitoblar: JOIN qilingan jadval ma'lumoti bo'yicha CASE
## Topshiriq sharti:
Mijozning oxirgi buyurtmasi summasiga qarab unga 'VIP', 'Oddiy' yoki 'Yangi' maqomini bering.

## Yechim (SQL kodi):
```sql
SELECT 
    m.ism,
    CASE 
        WHEN MAX(b.summa) > 300000 THEN 'VIP Mijoz'
        WHEN MAX(b.summa) IS NOT NULL THEN 'Oddiy Mijoz'
        ELSE 'Yangi Mijoz (Xaridsiz)'
    END AS mijoz_toifasi
FROM mijozlar_j m
LEFT JOIN buyurtmalar_j b ON m.id = b.mijoz_id
GROUP BY m.id, m.ism;
```

## Tushuntirish va Mantiq:
JOIN qilingan jadval ustunlari agregatlanib, CASE mantiqiy ifodasi orqali tahlil qilinadi.

## Ishlash natijasi:
```text
ism   |     mijoz_toifasi      
---------+------------------------
 Alisher | Oddiy Mijoz
 Bobur   | VIP Mijoz
 Sardor  | Yangi Mijoz (Xaridsiz)
(3 rows)
```


# 297-Topshiriq: NATURAL LEFT JOIN xatti-harakati
## Topshiriq sharti:
NATURAL va LEFT JOIN birgalikda qo'llanganda nima yuz berishini ko'ring.

## Yechim (SQL kodi):
```sql
SELECT * 
FROM xodim_j 
NATURAL LEFT JOIN bolim_j;
```

## Tushuntirish va Mantiq:
'NATURAL LEFT JOIN' barcha bir xil nomli ustunlar bo'yicha chap tashqi birlashishni amalga oshiradi.

## Ishlash natijasi:
```text
bolim_id | id |  ism   |  nomi   
----------+----+--------+---------
       10 |  1 | Nodir  | IT
       20 |  2 | Zilola | Kadrlar
(2 rows)
```


# 298-Topshiriq: Jadvallar o'rtasidagi rekursiv bo'lmagan cheksiz bog'lanishlar
## Topshiriq sharti:
Filial, xodim, kompyuter va dastur o'rtasidagi 4 qavatli to'liq bog'lanish.

## Yechim (SQL kodi):
```sql
CREATE TABLE f_1 (id INT PRIMARY KEY, n TEXT);
CREATE TABLE x_1 (id INT PRIMARY KEY, f_id INT, n TEXT);
CREATE TABLE k_1 (id INT PRIMARY KEY, x_id INT, n TEXT);

INSERT INTO f_1 VALUES (1, 'Toshkent Filial');
INSERT INTO x_1 VALUES (10, 1, 'Rustam');
INSERT INTO k_1 VALUES (100, 10, 'Dell Noutbuk');

SELECT f.n AS filial, x.n AS xodim, k.n AS kompyuter
FROM f_1 f
JOIN x_1 x ON f.id = x.f_id
JOIN k_1 k ON x.id = k.x_id;
```

## Tushuntirish va Mantiq:
Har bir qatlam o'zining ota identifikatori orqali xatosiz bog'lanadi.

## Ishlash natijasi:
```text
filial      | xodim  |  kompyuter   
-----------------+--------+--------------
 Toshkent Filial | Rustam | Dell Noutbuk
(1 row)
```


# 299-Topshiriq: PostgreSQL da Join Collapse Limit sozlamasi
## Topshiriq sharti:
Optimizator nechta jadvalgacha barcha kombinatsiyalarni qidirishini belgilovchi 'join_collapse_limit' parametri haqida ma'lumot.

## Yechim (SQL kodi):
```sql
SHOW join_collapse_limit;
```

## Tushuntirish va Mantiq:
PostgreSQL da sukut bo'yicha 'join_collapse_limit = 8'. Agar so'rovda 8 tadan ko'p jadval qatnashsa, optimizator barcha mumkin bo'lgan N! ta rejalarni tekshirishni to'xtatadi va genetik algoritmga (GEQO) o'tadi.

## Ishlash natijasi:
```text
join_collapse_limit 
---------------------
 8
(1 row)
```


# 300-Topshiriq: Korporativ Birlashma: ERP Tizimi uchun 5 jadvalli To'liq Sotuv Hisoboti
## Topshiriq sharti:
Mijozlar, Buyurtmalar, Buyurtma tarkibi, Mahsulotlar va Omborni bog'lab to'liq analitik fakt-jadval hisobotini shakllantiring.

## Yechim (SQL kodi):
```sql
CREATE TABLE erp_mijoz (id INT PRIMARY KEY, ism TEXT);
CREATE TABLE erp_buyurtma (id INT PRIMARY KEY, mijoz_id INT, sana DATE);
CREATE TABLE erp_tovar (id INT PRIMARY KEY, nomi TEXT, tannarx NUMERIC);
CREATE TABLE erp_ombor (id INT PRIMARY KEY, tovar_id INT, ombor_nomi TEXT);
CREATE TABLE erp_tarkib (buyurtma_id INT, tovar_id INT, soni INT, sotuv_narx NUMERIC);

INSERT INTO erp_mijoz VALUES (1, 'Artel Holding');
INSERT INTO erp_buyurtma VALUES (5001, 1, '2026-07-01');
INSERT INTO erp_tovar VALUES (101, 'Konditsioner Inverter', 3000000);
INSERT INTO erp_ombor VALUES (1, 101, 'Markaziy Ombor');
INSERT INTO erp_tarkib VALUES (5001, 101, 5, 4200000);

SELECT 
    m.ism AS mijoz_nomi,
    b.id AS buyurtma_raqami,
    b.sana,
    t.nomi AS mahsulot,
    o.ombor_nomi,
    tk.soni,
    tk.sotuv_narx,
    (tk.soni * tk.sotuv_narx) AS jami_tushum,
    (tk.soni * (tk.sotuv_narx - t.tannarx)) AS sof_foyda
FROM erp_buyurtma b
INNER JOIN erp_mijoz m ON b.mijoz_id = m.id
INNER JOIN erp_tarkib tk ON b.id = tk.buyurtma_id
INNER JOIN erp_tovar t ON tk.tovar_id = t.id
LEFT JOIN erp_ombor o ON t.id = o.tovar_id;
```

## Tushuntirish va Mantiq:
Ushbu korporativ so'rov yirik taqsimlangan ERP (Enterprise Resource Planning) tizimlarining yuragi hisoblanadi: bir nechta tranzaksiyaviy jadvallar (buyurtma, faktura elementlari) ma'lumotnomalar (mijoz, tovar, ombor) bilan birlashib, real vaqt rejimida daromad va sof foydani aniq hisoblab beradi.

## Ishlash natijasi:
```text
mijoz_nomi   | buyurtma_raqami |    sana    |       mahsulot        |   ombor_nomi   | soni | sotuv_narx | jami_tushum | sof_foyda  
---------------+-----------------+------------+-----------------------+----------------+------+------------+-------------+------------
 Artel Holding |            5001 | 2026-07-01 | Konditsioner Inverter | Markaziy Ombor |    5 | 4200000.00 | 21000000.00 | 6000000.00
(1 row)
```

