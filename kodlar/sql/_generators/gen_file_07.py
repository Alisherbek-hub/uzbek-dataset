import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

# List of 50 tasks for File 7: 301 - 350
# Ichma-ich so'rovlar (Subqueries: Skalyar, Correlated, EXISTS, NOT EXISTS, IN, ANY, ALL, Derived tables, LATERAL)

subq_data = [
    (
        301,
        "WHERE bandida oddiy skalyar subquery",
        "Oylik maoshi kompaniyadagi o'rtacha maoshdan yuqori bo'lgan xodimlarni toping.",
        """CREATE TABLE xodimlar_sub (
    id SERIAL PRIMARY KEY,
    ism VARCHAR(50),
    bolim VARCHAR(50),
    maosh NUMERIC(12, 2)
);

INSERT INTO xodimlar_sub (ism, bolim, maosh) VALUES 
('Rustam', 'IT', 15000000),
('Sarvar', 'IT', 11000000),
('Dildora', 'Moliya', 8000000),
('Madina', 'Moliya', 12000000),
('Jamshid', 'Marketing', 7000000);

SELECT ism, bolim, maosh 
FROM xodimlar_sub 
WHERE maosh > (SELECT AVG(maosh) FROM xodimlar_sub);""",
        "Skalyar subquery aynan bitta qator va bitta ustun (yagona qiymat) qaytaradi. Bu yerda `(SELECT AVG(maosh) ...)` 10,600,000 qiymatini qaytaradi va WHERE bandida har bir xodim maoshi shu songa solishtiriladi.",
        """   ism   | bolim  |    narx     
---------+--------+-------------
 Rustam  | IT     | 15000000.00
 Sarvar  | IT     | 11000000.00
 Madina  | Moliya | 12000000.00
(3 rows)"""
    ),
    (
        302,
        "SELECT proyeksiyasida skalyar subquery",
        "Har bir xodim yoniga butun kompaniyaning o'rtacha maoshini va xodim maoshining undan farqini chiqaring.",
        """SELECT 
    ism, 
    maosh,
    ROUND((SELECT AVG(maosh) FROM xodimlar_sub), 2) AS kompaniya_ortacha,
    ROUND(maosh - (SELECT AVG(maosh) FROM xodimlar_sub), 2) AS farq
FROM xodimlar_sub;""",
        "SELECT ro'yxatidagi skalyar subquery mustaqil ifoda sifatida ishlaydi. Optimizator uni har safar qayta hisoblamasdan bitta o'zgarmas qiymat (constant) sifatida keshlaydi.",
        """   ism   |    maosh    | kompaniya_ortacha |    farq    
---------+-------------+-------------------+------------
 Rustam  | 15000000.00 |       10600000.00 | 4400000.00
 Sarvar  | 11000000.00 |       10600000.00 |  400000.00
 Dildora |  8000000.00 |       10600000.00 |-2600000.00
 Madina  | 12000000.00 |       10600000.00 | 1400000.00
 Jamshid |  7000000.00 |       10600000.00 |-3600000.00
(5 rows)"""
    ),
    (
        303,
        "Skalyar subquery xatosi: Birdan ortiq qator qaytishi",
        "Agar skalyar o'ringa ko'p qatorli so'rov tushsa nima bo'lishini ko'ring.",
        """-- Xato so'rov:
-- SELECT ism FROM xodimlar_sub WHERE maosh = (SELECT maosh FROM xodimlar_sub WHERE bolim = 'IT');
SELECT 'Skalyar subquery birdan ortiq qiymat qaytarsa: more than one row returned xatosi chiqadi' AS ogohlantirish;""",
        "Taqqoslash operatori (`=`) faqat bitta son kutadi. Agar subquery 2 ta maosh qaytarsa, RDBMS 'more than one row returned by a subquery used as an expression' xatosi bilan to'xtaydi. Bunday joyda 'IN' yoki '= ANY' ishlatilishi lozim.",
        """                                        ogohlantirish                                         
----------------------------------------------------------------------------------------------
 Skalyar subquery birdan ortiq qiymat qaytarsa: more than one row returned xatosi chiqadi
(1 row)"""
    ),
    (
        304,
        "Correlated Subquery (Bog'langan ichki so'rov) asoslari",
        "Har bir xodimni O'Z BO'LIMINING o'rtacha maoshidan ko'p oluvchilarini toping.",
        """SELECT x1.ism, x1.bolim, x1.maosh 
FROM xodimlar_sub x1 
WHERE x1.maosh > (
    SELECT AVG(x2.maosh) 
    FROM xodimlar_sub x2 
    WHERE x2.bolim = x1.bolim
);""",
        "'Correlated Subquery' tashqi so'rovning joriy qatoriga (`x1.bolim`) tayanadi. Ichki so'rov har bir tashqi qator uchun alohida ishlaydi (IT uchun IT o'rtachasi, Moliya uchun Moliya o'rtachasi).",
        """  ism   | bolim  |    maosh    
--------+--------+-------------
 Rustam | IT     | 15000000.00
 Madina | Moliya | 12000000.00
(2 rows)"""
    ),
    (
        305,
        "SELECT bandida Correlated Subquery (Bog'langan soni)",
        "Har bir bo'lim yonida unda jami nechta xodim borligini GROUP BY siz chiqaring.",
        """SELECT 
    DISTINCT x1.bolim,
    (SELECT COUNT(*) FROM xodimlar_sub x2 WHERE x2.bolim = x1.bolim) AS bolim_xodimlar_soni 
FROM xodimlar_sub x1;""",
        "Correlated subquery tashqi jadvalning har bir noyob bo'limi uchun mustaqil COUNT hisoblaydi.",
        """   bolim   | bolim_xodimlar_soni 
-----------+---------------------
 IT        |                   2
 Marketing |                   1
 Moliya    |                   2
(3 rows)"""
    ),
    (
        306,
        "EXISTS operatori (Mavjudlikni tekshirish)",
        "Kamida bitta xaridi bor mijozlarni EXISTS yordamida aniqlang.",
        """CREATE TABLE xaridorlar_s (id INT PRIMARY KEY, ism TEXT);
CREATE TABLE xaridlar_s (id INT, xaridor_id INT, summa NUMERIC);

INSERT INTO xaridorlar_s VALUES (1, 'Farhod'), (2, 'Nilufar'), (3, 'Olim');
INSERT INTO xaridlar_s VALUES (101, 1, 200000), (102, 1, 350000), (103, 2, 90000);

SELECT x.ism 
FROM xaridorlar_s x 
WHERE EXISTS (
    SELECT 1 
    FROM xaridlar_s b 
    WHERE b.xaridor_id = x.id
);""",
        "'EXISTS' ichki so'rovda kamida bitta qator topilsa darhol TRUE qaytaradi va qidiruvni to'xtatadi (short-circuit execution). Bu juda yuqori tezlik beradi.",
        """   ism   
---------
 Farhod
 Nilufar
(2 rows)"""
    ),
    (
        307,
        "EXISTS da 'SELECT 1' va 'SELECT *' farqi",
        "Nega EXISTS ichida 'SELECT 1' yoki 'SELECT *' yozilishining mutlaqo farqi yo'qligini tushuntiring.",
        """SELECT 'EXISTS faqat qator bor-yo‘qligini tekshiradi, ustunlar qiymatini umuman o‘qimaydi' AS xulosa;""",
        "SQL optimizatori EXISTS ichidagi SELECT ro'yxatini to'liq e'tiborsiz qoldiradi. U diskdan ustun ma'lumotlarini yuklamaydi, faqat qator mavjudligi faktini tekshiradi. Shuning uchun 'SELECT 1' yozish qabul qilingan standartdir.",
        """                                                xulosa                                                 
-------------------------------------------------------------------------------------------------------
 EXISTS faqat qator bor-yo‘qligini tekshiradi, ustunlar qiymatini umuman o‘qimaydi
(1 row)"""
    ),
    (
        308,
        "NOT EXISTS operatori (Mavjud emaslikni tekshirish)",
        "Birorta ham xarid qilmagan mijozlarni NOT EXISTS orqali toping.",
        """SELECT x.ism 
FROM xaridorlar_s x 
WHERE NOT EXISTS (
    SELECT 1 
    FROM xaridlar_s b 
    WHERE b.xaridor_id = x.id
);""",
        "'NOT EXISTS' agar ichki so'rov birorta ham qator topa olmasa TRUE qaytaradi. Bu Olim kabi xaridsiz mijozlarni aniqlaydi.",
        """ ism  
------
 Olim
(1 row)"""
    ),
    (
        309,
        "IN va Subquery",
        "Xarid qilgan mijozlar ro'yxatini IN bilan toping.",
        """SELECT ism 
FROM xaridorlar_s 
WHERE id IN (SELECT xaridor_id FROM xaridlar_s);""",
        "'WHERE id IN (subquery)' ichki so'rov natijalari to'plamiga qaraydi. Optimizator bunday so'rovlarni ko'pincha Semi-Join ga aylantiradi.",
        """   ism   
---------
 Farhod
 Nilufar
(2 rows)"""
    ),
    (
        310,
        "NOT IN da subquery va NULL qiymat halokati",
        "Ichki jadvalda bitta NULL bo'lsa NOT IN nega butunlay sinishini ko'rsating.",
        """INSERT INTO xaridlar_s VALUES (104, NULL, 50000);

SELECT ism 
FROM xaridorlar_s 
WHERE id NOT IN (SELECT xaridor_id FROM xaridlar_s);""",
        "Subquery qaytargan to'plamda {1, 2, NULL} bo'lsa, `NOT IN (1, 2, NULL)` har doim FALSE/UNKNOWN beradi. Natijada xaridorlar_s dagi Olim ham chiqmaydi va BO'SH natija qaytadi! Xulosa: NOT IN o'rniga doim NOT EXISTS ishlatilishi shart.",
        """ ism 
-----
(0 rows)"""
    ),
    (
        311,
        "NOT IN tuzog'ini to'g'irlash (WHERE xaridor_id IS NOT NULL)",
        "NOT IN ishlatishga majbur bo'linganda ichki so'rovdan NULL larni olib tashlash usuli.",
        """SELECT ism 
FROM xaridorlar_s 
WHERE id NOT IN (
    SELECT xaridor_id 
    FROM xaridlar_s 
    WHERE xaridor_id IS NOT NULL
);""",
        "Ichki so'rovdan NULL lar filtrlangach, NOT IN yana to'g'ri ishlay boshlaydi va Olimni topadi.",
        """ ism  
------
 Olim
(1 row)"""
    ),
    (
        312,
        "ANY / SOME operatori",
        "Moliya bo'limidagi ixtiyoriy bitta (istalgan kamida bitta) xodimdan ko'p maosh oluvchi boshqa xodimlarni toping.",
        """SELECT ism, bolim, maosh 
FROM xodimlar_sub 
WHERE maosh > ANY (
    SELECT maosh 
    FROM xodimlar_sub 
    WHERE bolim = 'Moliya'
);""",
        "'> ANY (to'plam)' to'plamdagi ENG KICHIK qiymatdan katta bo'lishni anglatadi (Moliya bo'limida eng kam maosh 8M, demak 8M dan katta barcha xodimlar chiqadi). 'SOME' va 'ANY' mutlaqo sinonimdir.",
        """   ism   | bolim  |    maosh    
---------+--------+-------------
 Rustam  | IT     | 15000000.00
 Sarvar  | IT     | 11000000.00
 Madina  | Moliya | 12000000.00
(3 rows)"""
    ),
    (
        313,
        "ALL operatori",
        "Moliya bo'limidagi BARCHA xodimlarning maoshidan ham ko'proq maosh oluvchi xodimlarni toping.",
        """SELECT ism, bolim, maosh 
FROM xodimlar_sub 
WHERE maosh > ALL (
    SELECT maosh 
    FROM xodimlar_sub 
    WHERE bolim = 'Moliya'
);""",
        "'> ALL (to'plam)' to'plamdagi ENG KATTA qiymatdan ham katta bo'lishni talab qiladi (Moliya eng yuqori maoshi 12M bo'lsa, faqat 12M dan ko'p oluvchilar chiqadi).",
        """  ism   | bolim |    maosh    
--------+-------+-------------
 Rustam | IT    | 15000000.00
(1 row)"""
    ),
    (
        314,
        "= ANY va IN ning to'liq tengligi",
        "'= ANY' ifodasi 'IN' bilan aynan bir xilligini ko'rsating.",
        """SELECT ism 
FROM xaridorlar_s 
WHERE id = ANY (SELECT xaridor_id FROM xaridlar_s WHERE xaridor_id IS NOT NULL);""",
        "SQL standartida `id = ANY (subquery)` va `id IN (subquery)` to'liq ekvivalent hisoblanadi.",
        """   ism   
---------
 Farhod
 Nilufar
(2 rows)"""
    ),
    (
        315,
        "<> ALL va NOT IN ning ekvivalentligi",
        "'<> ALL' ifodasi 'NOT IN' kabi ishlashini ko'rsating.",
        """SELECT ism 
FROM xaridorlar_s 
WHERE id <> ALL (SELECT xaridor_id FROM xaridlar_s WHERE xaridor_id IS NOT NULL);""",
        "`id <> ALL (to'plam)` har bir element bilan teng emaslikni tekshiradi, bu NOT IN ning aynan o'zidir.",
        """ ism  
------
 Olim
(1 row)"""
    ),
    (
        316,
        "FROM bandidagi Subquery (Derived Table / Inline View)",
        "Bo'limlarning o'rtacha maoshini hisoblab, so'ngra ushbu o'rtacha maoshlar orasidan eng kattasini toping.",
        """SELECT MAX(bolim_ortacha) AS eng_katta_ortacha_maosh
FROM (
    SELECT bolim, AVG(maosh) AS bolim_ortacha 
    FROM xodimlar_sub 
    GROUP BY bolim
) AS bolim_statistikasi;""",
        "FROM bandidagi ichki so'rov 'Derived Table' (hosil qilingan jadval) deyiladi. U albatta o'z taxallusiga (`AS bolim_statistikasi`) ega bo'lishi shart.",
        """ eng_katta_ortacha_maosh 
--------------------------
    13000000.000000000000
(1 row)"""
    ),
    (
        317,
        "Derived Table larda filtrlash va saralash",
        "Xaridlari yig'indisi 300,000 dan yuqori bo'lgan mijozlar sonini aniqlang.",
        """SELECT COUNT(*) AS katta_xaridorlar_soni 
FROM (
    SELECT xaridor_id, SUM(summa) AS jami 
    FROM xaridlar_s 
    WHERE xaridor_id IS NOT NULL 
    GROUP BY xaridor_id 
    HAVING SUM(summa) > 300000
) AS saralangan;""",
        "Ichki jadval ma'lumotlarni oldindan agregatlab beradi, tashqi so'rov esa oddiy COUNT(*) bilan ularning sonini oladi.",
        """ katta_xaridorlar_soni 
------------------------
                      1
(1 row)"""
    ),
    (
        318,
        "HAVING bandida Subquery",
        "O'rtacha maoshi korxonaning umumiy o'rtacha maoshidan katta bo'lgan bo'limlarni chiqaring.",
        """SELECT bolim, ROUND(AVG(maosh), 2) AS ortacha_maosh 
FROM xodimlar_sub 
GROUP BY bolim 
HAVING AVG(maosh) > (SELECT AVG(maosh) FROM xodimlar_sub);""",
        "HAVING bandida dinamik chegarani aniqlash uchun mustaqil skalyar subquery qo'llaniladi.",
        """ bolim | ortacha_maosh 
-------+---------------
 IT    |   13000000.00
(1 row)"""
    ),
    (
        319,
        "LATERAL Subquery (Tashqi jadvalga murojaat qiluvchi FROM subquery)",
        "Har bir mijoz uchun uning eng yirik 1 ta xaridini LATERAL orqali oling.",
        """SELECT x.ism, eng_katta.summa 
FROM xaridorlar_s x,
LATERAL (
    SELECT summa 
    FROM xaridlar_s b 
    WHERE b.xaridor_id = x.id 
    ORDER BY summa DESC 
    LIMIT 1
) AS eng_katta;""",
        "'LATERAL' kalit so'zi FROM bandidagi subquery ga o'zidan oldin kelgan jadval ustunlariga (`x.id`) murojaat qilish imkonini beradi (oddiy subquery FROM da bunga ruxsat berilmaydi).",
        """   ism   |   summa   
---------+-----------
 Farhod  | 350000.00
 Nilufar |  90000.00
(2 rows)"""
    ),
    (
        320,
        "LEFT JOIN LATERAL (Bo'sh natijali qatorlarni ham saqlash)",
        "Xaridi yo'q mijozlar ham natijadan tushib qolmasligi uchun LEFT JOIN LATERAL qo'llang.",
        """SELECT x.ism, COALESCE(eng_katta.summa, 0) AS eng_katta_xarid 
FROM xaridorlar_s x
LEFT JOIN LATERAL (
    SELECT summa 
    FROM xaridlar_s b 
    WHERE b.xaridor_id = x.id 
    ORDER BY summa DESC 
    LIMIT 1
) AS eng_katta ON TRUE;""",
        "'LEFT JOIN LATERAL ... ON TRUE' xaridi yo'q Olimni ham saqlab qoladi va unga 0 qiymat beradi.",
        """   ism   | eng_katta_xarid 
---------+-----------------
 Farhod  |       350000.00
 Nilufar |        90000.00
 Olim    |            0.00
(3 rows)"""
    ),
    (
        321,
        "Ko'p ustunli (Tuple) Subquery",
        "Har bir bo'limdagi eng yuqori maosh oluvchi xodimlarni tuple subquery yordamida bitta so'rovda toping.",
        """SELECT ism, bolim, maosh 
FROM xodimlar_sub 
WHERE (bolim, maosh) IN (
    SELECT bolim, MAX(maosh) 
    FROM xodimlar_sub 
    GROUP BY bolim
);""",
        "`(bolim, maosh) IN (SELECT bolim, MAX(maosh) ...)` kompozit qatorlar tengligini tekshiradi. Har bir bo'limning eng ko'p maosh oluvchisi aniqlanadi.",
        """   ism   |   bolim   |    maosh    
---------+-----------+-------------
 Rustam  | IT        | 15000000.00
 Madina  | Moliya    | 12000000.00
 Jamshid | Marketing |  7000000.00
(3 rows)"""
    ),
    (
        322,
        "2-o'rindagi eng katta qiymatni topish (Subquery orqali)",
        "Kompaniyadagi ikkinchi eng yuqori maoshni (Second Highest Salary) subquery orqali aniqlang.",
        """SELECT MAX(maosh) AS ikkinchi_eng_katta_maosh 
FROM xodimlar_sub 
WHERE maosh < (SELECT MAX(maosh) FROM xodimlar_sub);""",
        "Eng katta qiymatdan kichik bo'lgan barcha qiymatlarning maksimali aynan 2-o'rindagi qiymat bo'ladi. Texnik intervyularda eng ko'p beriladigan mashhur relyatsion savol.",
        """ ikkinchi_eng_katta_maosh 
----------------------------
                12000000.00
(1 row)"""
    ),
    (
        323,
        "N-o'rindagi qiymatni topish (N-th Highest Salary)",
        "Kompaniyadagi uchinchi eng yuqori maoshni aniqlash so'rovini yozing.",
        """SELECT maosh AS uchinchi_maosh 
FROM xodimlar_sub 
ORDER BY maosh DESC 
LIMIT 1 OFFSET 2;""",
        "OFFSET n-1 yordamida N-o'rindagi qiymat topiladi. Agar dublikatlar bo'lsa, `ORDER BY maosh` oldiga DISTINCT qo'shiladi.",
        """ uchinchi_maosh 
---------------
   11000000.00
(1 row)"""
    ),
    (
        324,
        "Subquery da CASE ifodasi",
        "Xodimning maoshi o'z bo'limi o'rtachasidan yuqori bo'lsa 'Yetakchi', aks holda 'Oddiy' deb baholang.",
        """SELECT 
    ism, 
    bolim, 
    maosh,
    CASE 
        WHEN maosh >= (SELECT AVG(x2.maosh) FROM xodimlar_sub x2 WHERE x2.bolim = x1.bolim) 
        THEN 'Bo''lim yetakchisi' 
        ELSE 'Oddiy xodim' 
    END AS status
FROM xodimlar_sub x1;""",
        "CASE ifodasining 'WHEN' shartida to'liq mustaqil correlated subquery lar ishlay oladi.",
        """   ism   |   bolim   |    maosh    |      status      
---------+-----------+-------------+------------------
 Rustam  | IT        | 15000000.00 | Bo'lim yetakchisi
 Sarvar  | IT        | 11000000.00 | Oddiy xodim
 Dildora | Moliya    |  8000000.00 | Oddiy xodim
 Madina  | Moliya    | 12000000.00 | Bo'lim yetakchisi
 Jamshid | Marketing |  7000000.00 | Bo'lim yetakchisi
(5 rows)"""
    ),
    (
        325,
        "Ichma-ich subquery zanjiri (Nested subqueries)",
        "Eng ko'p xarid qilgan mijozning qaysi shahardan ekanligini toping.",
        """CREATE TABLE mijoz_shahar (id INT PRIMARY KEY, shahar TEXT);
INSERT INTO mijoz_shahar VALUES (1, 'Toshkent'), (2, 'Samarqand');

SELECT shahar 
FROM mijoz_shahar 
WHERE id = (
    SELECT xaridor_id 
    FROM xaridlar_s 
    WHERE xaridor_id IS NOT NULL 
    GROUP BY xaridor_id 
    ORDER BY SUM(summa) DESC 
    LIMIT 1
);""",
        "Ichki so'rov eng ko'p xarid qilgan xaridor ID sini (1) topadi, tashqi so'rov esa ushbu ID bo'yicha shaharni chiqaradi.",
        """  shahar  
----------
 Toshkent
(1 row)"""
    ),
    (
        326,
        "Barcha qatorlari teng bo'lgan guruhlarni topish",
        "Faqat barcha xodimlari bir xil maosh oladigan bo'limlarni subquery orqali toping.",
        """SELECT bolim 
FROM xodimlar_sub 
GROUP BY bolim 
HAVING MIN(maosh) = MAX(maosh);""",
        "Guruhda MIN va MAX teng bo'lsa, demak undagi barcha qiymatlar bir xildir.",
        """   bolim   
-----------
 Marketing
(1 row)"""
    ),
    (
        327,
        "INSERT ichida Subquery",
        "Oyligi 10,000,000 dan yuqori bo'lgan xodimlarni yangi 'yuqori_maoshlilar' jadvaliga ko'chiring.",
        """CREATE TABLE yuqori_xodimlar (ism TEXT, maosh NUMERIC);

INSERT INTO yuqori_xodimlar (ism, maosh)
SELECT ism, maosh 
FROM xodimlar_sub 
WHERE maosh > 10000000;

SELECT * FROM yuqori_xodimlar;""",
        "INSERT INTO ... SELECT mexanizmi subquery orqali ma'lumotlarni filtrlash va boshqa jadvalga yozish imkonini beradi.",
        """CREATE TABLE
INSERT 0 3
  ism   |    maosh    
--------+-------------
 Rustam | 15000000.00
 Sarvar | 11000000.00
 Madina | 12000000.00
(3 rows)"""
    ),
    (
        328,
        "UPDATE ichida Subquery",
        "Moliya bo'limidagi xodimlarning maoshini IT bo'limining eng kam maoshiga tenglashtiring.",
        """UPDATE xodimlar_sub 
SET maosh = (SELECT MIN(maosh) FROM xodimlar_sub WHERE bolim = 'IT')
WHERE bolim = 'Moliya' AND maosh < (SELECT MIN(maosh) FROM xodimlar_sub WHERE bolim = 'IT');

SELECT ism, bolim, maosh FROM xodimlar_sub WHERE bolim = 'Moliya';""",
        "UPDATE ning SET bandida skalyar subquery boshqa bo'lim ko'rsatkichini olib, maqsadli qatorlarga o'zlashtiradi.",
        """UPDATE 1
   ism   | bolim  |    maosh    
---------+--------+-------------
 Madina  | Moliya | 12000000.00
 Dildora | Moliya | 11000000.00
(2 rows)"""
    ),
    (
        329,
        "DELETE ichida Subquery",
        "Hech qanday buyurtmasi bo'lmagan xaridorlarni subquery orqali o'chiring.",
        """DELETE FROM xaridorlar_s 
WHERE id NOT IN (
    SELECT xaridor_id 
    FROM xaridlar_s 
    WHERE xaridor_id IS NOT NULL
);

SELECT * FROM xaridorlar_s;""",
        "DELETE bandida NOT IN subquery si faqat xaridi yo'q Olimni o'chiradi.",
        """DELETE 1
 id |   ism   
----+---------
  1 | Farhod
  2 | Nilufar
(2 rows)"""
    ),
    (
        330,
        "Subquery optimizatsiyasi: Subquery Flattening (Unnesting)",
        "PostgreSQL ichma-ich so'rovlarni qanday qilib oddiy JOIN larga aylantirib yuborishini EXPLAIN orqali ko'ring.",
        """EXPLAIN SELECT * FROM xaridorlar_s WHERE id IN (SELECT xaridor_id FROM xaridlar_s);""",
        "Optimizator ichki so'rovni alohida tsikl qilib aylanmaydi, balki 'Subquery Flattening' usuli orqali uni Semi-Join ga yoki Hash Join ga o'zgartiradi. Bu tezlikni bir necha barobar oshiradi.",
        """                             QUERY PLAN                              
---------------------------------------------------------------------
 Hash Semi Join  (cost=1.09..2.16 rows=2 width=36)
   Hash Cond: (xaridorlar_s.id = xaridlar_s.xaridor_id)
   ->  Seq Scan on xaridorlar_s  (cost=0.00..1.02 rows=2 width=36)
   ->  Hash  (cost=1.04..1.04 rows=4 width=4)
         ->  Seq Scan on xaridlar_s  (cost=0.00..1.04 rows=4 width=4)
(5 rows)"""
    ),
    (
        331,
        "Kompaniya jami maoshining 50 foizini tashkil qiluvchi xodimlarni topish",
        "Kümülyativ taqsimotga tayyorgarlik sifatida korxona jami maosh fondini subquery da olish.",
        """SELECT ism, maosh, (SELECT SUM(maosh) FROM xodimlar_sub) AS jami_fond 
FROM xodimlar_sub;""",
        "Subquery orqali barcha qatorlarga umumiy mezon qo'shib beriladi.",
        """   ism   |    maosh    |  jami_fond  
---------+-------------+-------------
 Rustam  | 15000000.00 | 56000000.00
 Sarvar  | 11000000.00 | 56000000.00
 Madina  | 12000000.00 | 56000000.00
 Jamshid |  7000000.00 | 56000000.00
 Dildora | 11000000.00 | 56000000.00
(5 rows)"""
    ),
    (
        332,
        "O'zaro bog'liq EXISTS: Barcha fandan o'tgan talabalar",
        "Relyatsion bo'lish (Relational Division) amalini ikkita NOT EXISTS subquery orqali yozing.",
        """CREATE TABLE fanlar_r (id INT PRIMARY KEY);
CREATE TABLE talaba_fan_r (talaba_id INT, fan_id INT);

INSERT INTO fanlar_r VALUES (1), (2);
INSERT INTO talaba_fan_r VALUES (10, 1), (10, 2), (20, 1);

-- Barcha mavjud fanlarni topshirgan talaba (10):
SELECT DISTINCT tf1.talaba_id 
FROM talaba_fan_r tf1 
WHERE NOT EXISTS (
    SELECT f.id FROM fanlar_r f 
    WHERE NOT EXISTS (
        SELECT 1 FROM talaba_fan_r tf2 
        WHERE tf2.talaba_id = tf1.talaba_id AND tf2.fan_id = f.id
    )
);""",
        "Ushbu klassik relyatsion so'rov: 'Shunday talaba borki, unga tegishli bo'lmagan birorta ham fan mavjud emas'. Bu to'liq qamrovni (Universal Quantification - \u2200) bildiradi.",
        """ talaba_id 
-----------
        10
(1 row)"""
    ),
    (
        333,
        "Subquery ichida ORDER BY va LIMIT",
        "Kompaniyadagi eng kam maosh oluvchi 2 ta xodimning o'rtacha maoshini hisoblang.",
        """SELECT ROUND(AVG(maosh), 2) AS eng_kam_2ta_ortacha
FROM (
    SELECT maosh 
    FROM xodimlar_sub 
    ORDER BY maosh ASC 
    LIMIT 2
) eng_kamlar;""",
        "Ichki so'rov dastlabki eng kichik 2 ta maoshni oladi, tashqi so'rov esa ularning o'rtachasini chiqaradi.",
        """ eng_kam_2ta_ortacha 
----------------------
           9000000.00
(1 row)"""
    ),
    (
        334,
        "Shartli subquery: Agar jadval bo'sh bo'lsa zaxira qiymat",
        "COALESCE va skalyar subquery orqali xavfsiz qiymat olish.",
        """SELECT COALESCE(
    (SELECT MAX(maosh) FROM xodimlar_sub WHERE bolim = 'MavjudEmas'), 
    0.00
) AS xavfsiz_maosh;""",
        "Agar subquery hech qanday natija qaytarmasa, u NULL bo'ladi. COALESCE uni darhol '0.00' ga aylantiradi.",
        """ xavfsiz_maosh 
---------------
          0.00
(1 row)"""
    ),
    (
        335,
        "Muntazam ifodali subquery",
        "Email domeni faqat korporativ jadvallarda tasdiqlangan domenlar ro'yxatida bor foydalanuvchilar.",
        """CREATE TABLE tasdiq_domen (domen TEXT);
INSERT INTO tasdiq_domen VALUES ('itpark.uz'), ('gov.uz');

CREATE TABLE pochta_foydalanuvchi (ism TEXT, email TEXT);
INSERT INTO pochta_foydalanuvchi VALUES ('Ali', 'ali@itpark.uz'), ('Vali', 'vali@mail.ru');

SELECT ism, email 
FROM pochta_foydalanuvchi 
WHERE SPLIT_PART(email, '@', 2) IN (SELECT domen FROM tasdiq_domen);""",
        "Domen ajratib olinib, ruxsat etilgan domenlar subquery sidan qidiriladi.",
        """ ism |     email     
-----+---------------
 Ali | ali@itpark.uz
(1 row)"""
    ),
    (
        336,
        "Subquery natijasi bilan solishtirish: ALL va NULL qiymat",
        "ALL operatorida subquery natijasida NULL bo'lsa nima bo'ladi?",
        """SELECT ism 
FROM xodimlar_sub 
WHERE maosh > ALL (SELECT NULL::NUMERIC);""",
        "`> ALL (NULL)` ifodasi har doim UNKNOWN/FALSE beradi. Hech bir qator tanlanmaydi.",
        """ ism 
-----
(0 rows)"""
    ),
    (
        337,
        "Bir nechta mustaqil subquery larni SELECT da chiqarish",
        "Bitta so'rovda kompaniya xodimlar soni, jami maosh fondi va eng katta maoshni alohida skalyar subquery lar orqali olish.",
        """SELECT 
    (SELECT COUNT(*) FROM xodimlar_sub) AS jami_xodim,
    (SELECT SUM(maosh) FROM xodimlar_sub) AS jami_maosh,
    (SELECT MAX(maosh) FROM xodimlar_sub) AS eng_katta_maosh;""",
        "FROM siz mustaqil skalyar so'rovlar bitta metrika panelini (dashboard) shakllantirishda qulay.",
        """ jami_xodim | jami_maosh  | eng_katta_maosh 
------------+-------------+-----------------
          5 | 56000000.00 |     15000000.00
(1 row)"""
    ),
    (
        338,
        "WHERE dagi subquery da agregatsiyalangan shart",
        "Xaridlari soni o'rtacha xaridorlarnikidan ko'p bo'lgan faol xaridorlarni topish.",
        """SELECT xaridor_id, COUNT(*) AS buyurtmalar 
FROM xaridlar_s 
WHERE xaridor_id IS NOT NULL 
GROUP BY xaridor_id 
HAVING COUNT(*) > (
    SELECT AVG(b_soni) 
    FROM (
        SELECT COUNT(*) AS b_soni 
        FROM xaridlar_s 
        WHERE xaridor_id IS NOT NULL 
        GROUP BY xaridor_id
    ) s
);""",
        "O'rtacha buyurtmalar sonini topish uchun ichma-ich 2 qavatli subquery dan foydalaniladi.",
        """ xaridor_id | buyurtmalar 
------------+-------------
          1 |           2
(1 row)"""
    ),
    (
        339,
        "Subquery o'rniga CTE ishlatish tavsiyasi",
        "Nega murakkab 3 qavatli subquery larni CTE (WITH) ga o'tkazish kodni ancha toza qilishini tushuntiring.",
        """SELECT 'CTE subquery larga qaraganda ancha o‘qishli va DRY (Don''t Repeat Yourself) tamoyiliga mos keladi' AS maslahat;""",
        "Chuqur qatlamli subquery lar inson ko'zi uchun o'qishga juda og'ir. Keyingi mavzuda ko'rib chiqiladigan CTE barcha oraliq so'rovlarni mantiqiy bloklarga ajratib beradi.",
        """                                               maslahat                                                
-------------------------------------------------------------------------------------------------------
 CTE subquery larga qaraganda ancha o‘qishli va DRY (Don't Repeat Yourself) tamoyiliga mos keladi
(1 row)"""
    ),
    (
        340,
        "NOT EXISTS orqali o'zaro juftlanmagan elementlar",
        "Birorta ham filiali yo'q yangi ochilgan hududlarni aniqlash.",
        """CREATE TABLE hududlar (id INT PRIMARY KEY, nom TEXT);
CREATE TABLE filiallar_h (id INT PRIMARY KEY, hudud_id INT);

INSERT INTO hududlar VALUES (1, 'Farg‘ona'), (2, 'Andijon');
INSERT INTO filiallar_h VALUES (10, 1);

SELECT nom 
FROM hududlar h 
WHERE NOT EXISTS (
    SELECT 1 FROM filiallar_h f WHERE f.hudud_id = h.id
);""",
        "Andijonda filial yo'qligi sababli u NOT EXISTS filtri orqali tezkor topiladi.",
        """   nom   
---------
 Andijon
(1 row)"""
    ),
    (
        341,
        "Correlated Subquery yordamida qatorning o'z guruhidagi o'rnini (Rank) topish",
        "Oynador funksiyalarsiz xodimning o'z bo'limida nechanchi o'rinda turganini sof SQL subquery bilan hisoblang.",
        """SELECT 
    x1.ism, 
    x1.bolim, 
    x1.maosh,
    (
        SELECT COUNT(*) + 1 
        FROM xodimlar_sub x2 
        WHERE x2.bolim = x1.bolim AND x2.maosh > x1.maosh
    ) AS orin
FROM xodimlar_sub x1 
ORDER BY x1.bolim, orin;""",
        "O'zidan yuqori maosh oluvchilar soni + 1 aynan xodimning o'rnini (Dense Rank) beradi. Bu relyatsion mantiqning go'zal namunasidir.",
        """   ism   |   bolim   |    maosh    | orin 
---------+-----------+-------------+------
 Rustam  | IT        | 15000000.00 |    1
 Sarvar  | IT        | 11000000.00 |    2
 Jamshid | Marketing |  7000000.00 |    1
 Madina  | Moliya    | 12000000.00 |    1
 Dildora | Moliya    | 11000000.00 |    2
(5 rows)"""
    ),
    (
        342,
        "Subquery da CASE ifodasi orqali jadval tanlash",
        "Xaridor turiga qarab alohida chegirma jadvalidan koeffitsiyent olish.",
        """SELECT 
    x.ism,
    COALESCE(
        (SELECT SUM(summa) FROM xaridlar_s b WHERE b.xaridor_id = x.id),
        0
    ) AS sarflangan
FROM xaridorlar_s x;""",
        "Mijozning jami sarflagan mablag'ini skalyar correlated subquery bilan bog'lash.",
        """   ism   | sarflangan 
---------+------------
 Farhod  |  550000.00
 Nilufar |   90000.00
(2 rows)"""
    ),
    (
        343,
        "Subquery yordamida massiv yaratish (ARRAY)",
        "Har bir mijozning barcha buyurtma summalarini ARRAY subquery orqali bitta massiv ustuniga joylang.",
        """SELECT 
    x.ism,
    ARRAY(SELECT summa FROM xaridlar_s b WHERE b.xaridor_id = x.id) AS tolovlar_massivi
FROM xaridorlar_s x;""",
        "'ARRAY(SELECT ...)' subquery natijalarini to'g'ridan-to'g'ri massivga aylantirib beradi.",
        """   ism   |    tolovlar_massivi     
---------+-------------------------
 Farhod  | {200000.00,350000.00}
 Nilufar | {90000.00}
(2 rows)"""
    ),
    (
        344,
        "EXISTS da ikkita ustunni tekshirish",
        "Ayni bir vaqtda ham filial, ham lavozim mos kelishini tekshirish.",
        """CREATE TABLE talablar (filial TEXT, rol TEXT);
INSERT INTO talablar VALUES ('IT', 'Admin');

SELECT ism, bolim 
FROM xodimlar_sub x 
WHERE EXISTS (
    SELECT 1 FROM talablar t WHERE t.filial = x.bolim
);""",
        "Ko'p ustunli munosabatlarni tekshirishda EXISTS ning moslashuvchanligi cheksizdir.",
        """  ism   | bolim 
--------+-------
 Rustam | IT
 Sarvar | IT
(2 rows)"""
    ),
    (
        345,
        "Correlated UPDATE (Boshqa jadval bo'yicha yangilash)",
        "Har bir xaridor profiliga uning oxirgi buyurtma sanasini correlated subquery orqali yozish.",
        """ALTER TABLE xaridorlar_s ADD COLUMN oxirgi_xarid_summa NUMERIC;

UPDATE xaridorlar_s x
SET oxirgi_xarid_summa = (
    SELECT summa 
    FROM xaridlar_s b 
    WHERE b.xaridor_id = x.id 
    ORDER BY id DESC 
    LIMIT 1
);

SELECT * FROM xaridorlar_s;""",
        "Har bir qator uchun subquery eng so'nggi summani oladi va asosiy jadvalga saqlaydi.",
        """ALTER TABLE
UPDATE 2
 id |   ism   | oxirgi_xarid_summa 
----+---------+--------------------
  1 | Farhod  |          350000.00
  2 | Nilufar |           90000.00
(2 rows)"""
    ),
    (
        346,
        "Subquery natijasi bilan solishtirish: EXISTS vs IN tezligi",
        "Katta jadvallarda EXISTS va IN unumdorligini tahlil qilish.",
        """SELECT 'Agar tashqi kalit indekslangan bo‘lsa EXISTS va IN bir xil reja oladi, ammo NULL lar bo‘lsa EXISTS ancha xavfsizdir' AS xulosa;""",
        "Zamonaviy PostgreSQL har ikkala operatorni ham Hash Semi-Join ga aylantiradi, lekin NOT EXISTS va NOT IN o'rtasida katta farq bor (NULL sababli).",
        """                                                               xulosa                                                               
------------------------------------------------------------------------------------------------------------------------------------
 Agar tashqi kalit indekslangan bo‘lsa EXISTS va IN bir xil reja oladi, ammo NULL lar bo‘lsa EXISTS ancha xavfsizdir
(1 row)"""
    ),
    (
        347,
        "Subquery orqali kumulyativ o'suvchi yig'indi (Running Total)",
        "Oynador funksiyalarsiz har bir buyurtma sanasigacha bo'lgan o'suvchi jami summani hisoblang.",
        """CREATE TABLE kunlik_daromad (id INT PRIMARY KEY, kun DATE, summa NUMERIC);
INSERT INTO kunlik_daromad VALUES 
(1, '2026-05-01', 100), (2, '2026-05-02', 150), (3, '2026-05-03', 200);

SELECT 
    k1.kun,
    k1.summa,
    (
        SELECT SUM(k2.summa) 
        FROM kunlik_daromad k2 
        WHERE k2.kun <= k1.kun
    ) AS kumulyativ_jami
FROM kunlik_daromad k1 
ORDER BY k1.kun;""",
        "Har bir qator uchun undan oldingi barcha kunlar summasi correlated subquery da yig'iladi. Running total ning sof relyatsion formulasidir.",
        """    kun     | summa  | kumulyativ_jami 
------------+--------+-----------------
 2026-05-01 | 100.00 |          100.00
 2026-05-02 | 150.00 |          250.00
 2026-05-03 | 200.00 |          450.00
(3 rows)"""
    ),
    (
        348,
        "Top-N elementlar bo'yicha Derived table filtrlash",
        "Har bir toifadan faqat eng qimmat 1 ta tovardan iborat ro'yxatni olish.",
        """SELECT toifa, nomi, narx 
FROM tovarlar t1
WHERE narx = (
    SELECT MAX(narx) 
    FROM tovarlar t2 
    WHERE t2.toifa = t1.toifa
);""",
        "Har bir toifa uchun maksimal narx aniqlanadi va unga teng tovarlar tanlab olinadi.",
        """  toifa   |   nomi   |    narx     
----------+----------+-------------
 Noutbuk  | Asus ROG | 14000000.00
 Smartfon | iPhone 15| 12000000.00
(2 rows)"""
    ),
    (
        349,
        "Subquery dagi jadvallarni nomlash qoidasi (Scoping)",
        "Ichki va tashqi so'rovda bir xil jadval qatnashganda taxallus (alias) berish shartligi.",
        """SELECT ism 
FROM xodimlar_sub asosiy 
WHERE maosh > (SELECT AVG(maosh) FROM xodimlar_sub ichki WHERE ichki.bolim = asosiy.bolim);""",
        "Tashqi jadvalga 'asosiy', ichki jadvalga 'ichki' taxallusi berilmasa, RDBMS qaysi ustun qayerdan kelayotganini tushunolmaydi.",
        """  ism   
--------
 Rustam
 Madina
(2 rows)"""
    ),
    (
        350,
        "Korporativ Subquery: Firibgarlikni aniqlash (Fraud Detection)",
        "Bank tizimida oxirgi 1 soat ichida o'zining o'rtacha tranzaksiya summasidan 5 barobar katta pul yechgan shubhali mijozlarni correlated subquery orqali aniqlang.",
        """CREATE TABLE bank_operatsiyalar (
    id BIGSERIAL PRIMARY KEY,
    mijoz_id INT,
    summa NUMERIC(15, 2),
    vaqt TIMESTAMP
);

INSERT INTO bank_operatsiyalar (mijoz_id, summa, vaqt) VALUES 
(1, 100000, '2026-08-01 10:00'),
(1, 150000, '2026-08-01 11:00'),
(1, 120000, '2026-08-01 12:00'),
(1, 10000000, '2026-08-01 12:30'), -- Shubhali sakrash!
(2, 500000, '2026-08-01 10:00'),
(2, 600000, '2026-08-01 12:00');

SELECT 
    bo.id AS shubhali_tranzaksiya_id,
    bo.mijoz_id,
    bo.summa AS yechilgan_summa,
    bo.vaqt,
    ROUND((
        SELECT AVG(tarix.summa) 
        FROM bank_operatsiyalar tarix 
        WHERE tarix.mijoz_id = bo.mijoz_id AND tarix.id <> bo.id
    ), 2) AS odatiy_ortacha_summa
FROM bank_operatsiyalar bo
WHERE bo.summa > 5 * (
    SELECT AVG(tarix.summa) 
    FROM bank_operatsiyalar tarix 
    WHERE tarix.mijoz_id = bo.mijoz_id AND tarix.id <> bo.id
);""",
        "Bu korporativ xavfsizlik tizimlarida (Anti-Fraud Engine) real vaqtda qo'llaniladigan correlated subquery tahlilidir: ayni tranzaksiya o'sha mijozning boshqa barcha oldingi o'rtacha xarajatlari bilan solishtiriladi va agar anomaliya 5 barobardan oshsa, darhol xavfsizlikka signal beriladi.",
        """ shubhali_tranzaksiya_id | mijoz_id | yechilgan_summa |        vaqt         | odatiy_ortacha_summa 
-------------------------+----------+-----------------+---------------------+----------------------
                       4 |        1 |     10000000.00 | 2026-08-01 12:30:00 |            123333.33
(1 row)"""
    )
]

formatted = [format_task(*item) for item in subq_data]
save_file("sql_07_ichma_ich_sorovlar_subqueries.md", formatted)
