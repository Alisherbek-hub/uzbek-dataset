import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

# List of 50 tasks for File 8: 351 - 400
# CTE va rekursiv so'rovlar (Common Table Expressions: WITH, Multiple CTEs, Writable CTE, RECURSIVE, Trees, Hierarchies, Graph Traversal, Cycles)

cte_data = [
    (
        351,
        "Oddiy CTE (Common Table Expression) yaratish: WITH bandi",
        "Kompaniyadagi o'rtacha maoshni CTE orqali hisoblab, undan ko'p maosh oluvchilarni toping.",
        """CREATE TABLE xodimlar_cte (
    id SERIAL PRIMARY KEY,
    ism VARCHAR(50),
    bolim VARCHAR(50),
    maosh NUMERIC(12, 2)
);

INSERT INTO xodimlar_cte (ism, bolim, maosh) VALUES 
('Sherzod', 'IT', 14000000),
('Umida', 'IT', 16000000),
('Temur', 'Moliya', 9500000),
('Barno', 'Moliya', 8500000),
('Otabek', 'Logistika', 6000000);

WITH kompaniya_ortacha AS (
    SELECT AVG(maosh) AS ortacha_qiymat 
    FROM xodimlar_cte
)
SELECT x.ism, x.bolim, x.maosh 
FROM xodimlar_cte x, kompaniya_ortacha ko
WHERE x.maosh > ko.ortacha_qiymat;""",
        "'WITH cte_nomi AS (so''rov)' sintaksisi bitta asosiy so'rov davomida yashaydigan vaqtinchalik virtual jadval hosil qiladi. U ichma-ich subquery lardan ko'ra ancha o'qishli va toza strukturani ta'minlaydi.",
        """   ism   | bolim |    maosh    
---------+-------+-------------
 Sherzod | IT    | 14000000.00
 Umida   | IT    | 16000000.00
(2 rows)"""
    ),
    (
        352,
        "Bir nechta CTE larni ketma-ket ulash (CTE Chaining)",
        "Birinchi CTE da bo'limlar jami xarajatini, ikkinchi CTE da butun korxona jami xarajatini hisoblab, oxirida har bir bo'limning ulushini ko'rsating.",
        """WITH bolim_xarajat AS (
    SELECT bolim, SUM(maosh) AS jami_fond 
    FROM xodimlar_cte 
    GROUP BY bolim
),
umumiy_fond AS (
    SELECT SUM(jami_fond) AS grand_total 
    FROM bolim_xarajat
)
SELECT 
    bx.bolim,
    bx.jami_fond,
    ROUND((bx.jami_fond / uf.grand_total) * 100, 2) AS ulush_foiz
FROM bolim_xarajat bx
CROSS JOIN umumiy_fond uf
ORDER BY ulush_foiz DESC;""",
        "Bir nechta CTE lar vergul bilan ketma-ket yoziladi. Har bir keyingi CTE o'zidan oldin e'lon qilingan barcha CTE larga oddiy jadval kabi murojaat qila oladi. Bu ma'lumotlar oqimini (pipeline) toza qurish imkonini beradi.",
        """   bolim   |  jami_fond  | ulush_foiz 
-----------+-------------+------------
 IT        | 30000000.00 |      55.56
 Moliya    | 18000000.00 |      33.33
 Logistika |  6000000.00 |      11.11
(3 rows)"""
    ),
    (
        353,
        "CTE ni asosiy so'rovda bir necha marta qayta ishlatish (DRY)",
        "O'rtacha maoshdan ham eng yuqori, ham eng past chetlanishlarni bitta CTE ni ikki marta ishlatib toping.",
        """WITH statistika AS (
    SELECT AVG(maosh) AS ortacha, MIN(maosh) AS eng_kam, MAX(maosh) AS eng_kop 
    FROM xodimlar_cte
)
SELECT 
    'Eng yuqori chetlanish' AS parametr,
    s.eng_kop - s.ortacha AS qiymat 
FROM statistika s
UNION ALL
SELECT 
    'Eng past chetlanish',
    s.ortacha - s.eng_kam 
FROM statistika s;""",
        "Subquery bo'lsa uni har safar nusxalab qayta yozish kerak bo'lardi. CTE esa bir marta e'lon qilinadi va asosiy so'rovda istalgancha marta chaqiriladi.",
        """       parametr        |   qiymat    
-----------------------+-------------
 Eng yuqori chetlanish |  5200000.00
 Eng past chetlanish   |  4800000.00
(2 rows)"""
    ),
    (
        354,
        "PostgreSQL 12+: MATERIALIZED vs NOT MATERIALIZED CTE",
        "CTE ning xotirada optimizator tomonidan keshlanishi yoki inline qilinishini boshqarish.",
        """WITH hisob AS MATERIALIZED (
    SELECT id, maosh FROM xodimlar_cte WHERE maosh > 10000000
)
SELECT * FROM hisob;""",
        "PostgreSQL 12 dan boshlab oddiy CTE lar sukut bo'yicha 'NOT MATERIALIZED' (inline) qilinadi, ya'ni optimizator tashqi WHERE shartlarini uning ichiga olib kirishi mumkin. 'AS MATERIALIZED' esa CTE ni qat'iy alohida hisoblab xotirada saqlashga majburlaydi.",
        """ id |    maosh    
----+-------------
  1 | 14000000.00
  2 | 16000000.00
(2 rows)"""
    ),
    (
        355,
        "Writable CTE: DELETE qilingan qatorlarni arxiv jadvaliga ko'chirish",
        "Moliya bo'limi xodimlarini asosiy jadvaldan o'chirib, ayni vaqtda 'xodimlar_arxiv' jadvaliga yozing.",
        """CREATE TABLE xodimlar_arxiv (id INT, ism TEXT, bolim TEXT, maosh NUMERIC, sana TIMESTAMPTZ);

WITH ochirilganlar AS (
    DELETE FROM xodimlar_cte 
    WHERE bolim = 'Moliya'
    RETURNING id, ism, bolim, maosh
)
INSERT INTO xodimlar_arxiv (id, ism, bolim, maosh, sana)
SELECT id, ism, bolim, maosh, NOW() 
FROM ochirilganlar;

SELECT id, ism, bolim FROM xodimlar_arxiv;""",
        "PostgreSQL ning noyob 'Writable CTE' xususiyati orqali DELETE qilingan yozuvlar RETURNING orqali ushlanadi va to'g'ridan-to'g'ri ikkinchi jadvalga INSERT qilinadi. Bularning bari bitta tranzaksiyada xatoliksiz bajariladi.",
        """CREATE TABLE
INSERT 0 2
 id |  ism  | bolim  
----+-------+--------
  3 | Temur | Moliya
  4 | Barno | Moliya
(2 rows)"""
    ),
    (
        356,
        "Writable CTE: INSERT qilib, hosil bo'lgan ID ni uchinchi jadvalga kiritish",
        "Yangi buyurtma yaratib, uning ID sini zudlik bilan buyurtma elementiga biriktiring.",
        """CREATE TABLE b_asos (id SERIAL PRIMARY KEY, mijoz TEXT);
CREATE TABLE b_element (id SERIAL PRIMARY KEY, b_id INT, tovar TEXT);

WITH yangi_b AS (
    INSERT INTO b_asos (mijoz) 
    VALUES ('Akbar') 
    RETURNING id
)
INSERT INTO b_element (b_id, tovar)
SELECT id, 'Smartfon' 
FROM yangi_b;

SELECT * FROM b_element;""",
        "Ushbu usul ilovadan qo'shimcha so'rov yubormasdan relyatsion bog'lanishlarni bitta atomar ifodada yaratadi.",
        """CREATE TABLE
CREATE TABLE
INSERT 0 1
 id | b_id |  tovar   
----+------+----------
  1 |    1 | Smartfon
(1 row)"""
    ),
    (
        357,
        "Rekursiv CTE asoslari: 1 dan 10 gacha sonlar ketma-ketligi",
        "WITH RECURSIVE yordamida hech qanday jadvalsiz 1 dan 10 gacha sonlarni generatsiya qiling.",
        """WITH RECURSIVE sonlar AS (
    -- 1. Boshlang'ich qism (Anchor member):
    SELECT 1 AS n
    UNION ALL
    -- 2. Rekursiv qism (Recursive member):
    SELECT n + 1 
    FROM sonlar 
    WHERE n < 10 -- 3. To'xtash sharti
)
SELECT n FROM sonlar;""",
        "Rekursiv CTE uch qismdan iborat: 1) Anchor (boshlang'ich qiymat: 1), 2) UNION ALL, 3) Recursive qism (o'ziga tayanuvchi: n + 1) va qat'iy to'xtash sharti (`WHERE n < 10`). To'xtash sharti bo'lmasa so'rov cheksiz tsiklga tushadi.",
        """ n  
----
  1
  2
  3
  4
  5
  6
  7
  8
  9
 10
(10 rows)"""
    ),
    (
        358,
        "Rekursiv sana kalendari generatsiyasi",
        "Joriy oyning dastlabki 5 kunini rekursiv so'rov bilan hosil qiling.",
        """WITH RECURSIVE kunlar AS (
    SELECT '2026-09-01'::DATE AS sana
    UNION ALL
    SELECT (sana + INTERVAL '1 day')::DATE 
    FROM kunlar 
    WHERE sana < '2026-09-05'
)
SELECT sana FROM kunlar;""",
        "generate_series() mavjud bo'lmagan ma'lumotlar bazalarida (MySQL 8.0, SQLite) RECURSIVE CTE sana kalendarlarini yasashning yagona universal usulidir.",
        """    sana    
------------
 2026-09-01
 2026-09-02
 2026-09-03
 2026-09-04
 2026-09-05
(5 rows)"""
    ),
    (
        359,
        "Matematik rekursiya: Faktorial hisoblash",
        "1 dan 6 gacha sonlarning faktorialini rekursiv CTE bilan hisoblang.",
        """WITH RECURSIVE faktorial AS (
    SELECT 1 AS son, 1::BIGINT AS f
    UNION ALL
    SELECT son + 1, (f * (son + 1))::BIGINT 
    FROM faktorial 
    WHERE son < 6
)
SELECT son, f AS faktorial FROM faktorial;""",
        "Har bir qadamda yangi faktorial eski faktorial va joriy son ko'paytmasi sifatida hisoblanadi.",
        """ son | faktorial 
-----+-----------
   1 |         1
   2 |         2
   3 |         6
   4 |        24
   5 |       120
   6 |       720
(6 rows)"""
    ),
    (
        360,
        "Fibonachchi ketma-ketligini generatsiya qilish",
        "Dastlabki 8 ta Fibonachchi sonlarini rekursiv toping.",
        """WITH RECURSIVE fib AS (
    SELECT 1 AS qadam, 0::BIGINT AS a, 1::BIGINT AS b
    UNION ALL
    SELECT qadam + 1, b, a + b 
    FROM fib 
    WHERE qadam < 8
)
SELECT qadam, a AS fib_soni FROM fib;""",
        "Oldingi ikkita son yig'indisi yangi sonni tashkil qiluvchi klassik rekursiya relyatsion jadval shaklida hosil bo'ladi.",
        """ qadam | fib_soni 
-------+----------
     1 |        0
     2 |        1
     3 |        1
     4 |        2
     5 |        3
     6 |        5
     7 |        8
     8 |       13
(8 rows)"""
    ),
    (
        361,
        "Tashkiliy iyerarxiya: Rahbarlar va xodimlar daraxti",
        "Kompaniya iyerarxiyasida har bir xodimning bo'ysunish darajasini (depth / level) hisoblang.",
        """CREATE TABLE kompaniya_tuzilmasi (
    xodim_id INT PRIMARY KEY,
    ism VARCHAR(50),
    rahbar_id INT
);

INSERT INTO kompaniya_tuzilmasi VALUES 
(1, 'General Direktor', NULL),
(2, 'Texnik Direktor (CTO)', 1),
(3, 'Moliya Direktori (CFO)', 1),
(4, 'Bosh Dasturchi', 2),
(5, 'Junior Dasturchi', 4);

WITH RECURSIVE iyerarxiya AS (
    -- Anchor: Bosh rahbar (rahbari yo'q)
    SELECT xodim_id, ism, rahbar_id, 1 AS daraja
    FROM kompaniya_tuzilmasi
    WHERE rahbar_id IS NULL
    
    UNION ALL
    
    -- Recursive: Unga bo'ysunuvchilar
    SELECT k.xodim_id, k.ism, k.rahbar_id, i.daraja + 1
    FROM kompaniya_tuzilmasi k
    JOIN iyerarxiya i ON k.rahbar_id = i.xodim_id
)
SELECT daraja, ism FROM iyerarxiya ORDER BY daraja, xodim_id;""",
        "Anchor qism eng yuqori bo'g'inni (daraja=1) oladi. Rekursiv qism esa har bir xodimning rahbariga qarab daraxt bo'ylab chuqurlashadi va 'daraja + 1' ni hisoblaydi.",
        """ daraja |          ism           
--------+------------------------
      1 | General Direktor
      2 | Texnik Direktor (CTO)
      2 | Moliya Direktori (CFO)
      3 | Bosh Dasturchi
      4 | Junior Dasturchi
(5 rows)"""
    ),
    (
        362,
        "Vizual iyerarxiya: Qatorlarni bo'shliqlar bilan surish (Indentation)",
        "Xodimlarning darajasiga qarab ularning ismlari oldiga bo'shliqlar qo'yib daraxt shaklida ko'rsating.",
        """WITH RECURSIVE iyerarxiya AS (
    SELECT xodim_id, ism, rahbar_id, 1 AS daraja
    FROM kompaniya_tuzilmasi
    WHERE rahbar_id IS NULL
    
    UNION ALL
    
    SELECT k.xodim_id, k.ism, k.rahbar_id, i.daraja + 1
    FROM kompaniya_tuzilmasi k
    JOIN iyerarxiya i ON k.rahbar_id = i.xodim_id
)
SELECT REPEAT('  ', daraja - 1) || '└─ ' || ism AS daraxt_korinishi 
FROM iyerarxiya;""",
        "'REPEAT(' ', n)' funksiyasi orqali matnli vizual daraxt hosil qilinadi.",
        """        daraxt_korinishi         
---------------------------------
 └─ General Direktor
   └─ Texnik Direktor (CTO)
   └─ Moliya Direktori (CFO)
     └─ Bosh Dasturchi
       └─ Junior Dasturchi
(5 rows)"""
    ),
    (
        363,
        "Yo'l ko'rsatkichi (Breadcrumb path) hosil qilish",
        "Har bir xodim uchun bosh direktordan boshlab unga qadar to'liq yo'lni ('Direktor -> CTO -> Lead -> Junior') chiqaring.",
        """WITH RECURSIVE yol_daraxti AS (
    SELECT xodim_id, ism, rahbar_id, ism::TEXT AS yol
    FROM kompaniya_tuzilmasi
    WHERE rahbar_id IS NULL
    
    UNION ALL
    
    SELECT k.xodim_id, k.ism, k.rahbar_id, y.yol || ' -> ' || k.ism
    FROM kompaniya_tuzilmasi k
    JOIN yol_daraxti y ON k.rahbar_id = y.xodim_id
)
SELECT xodim_id, yol FROM yol_daraxti ORDER BY xodim_id;""",
        "Har bir rekursiv qadamda satr oxiriga ' -> ' va yangi xodim ismi ulab boriladi. Saytlardagi menyu va yo'l (breadcrumbs) shunday shakllanadi.",
        """ xodim_id |                                          yol                                          
----------+---------------------------------------------------------------------------------------
        1 | General Direktor
        2 | General Direktor -> Texnik Direktor (CTO)
        3 | General Direktor -> Moliya Direktori (CFO)
        4 | General Direktor -> Texnik Direktor (CTO) -> Bosh Dasturchi
        5 | General Direktor -> Texnik Direktor (CTO) -> Bosh Dasturchi -> Junior Dasturchi
(5 rows)"""
    ),
    (
        364,
        "Pastdan yuqoriga rekursiya: Xodimning barcha rahbarlarini topish",
        "Aynan 'Junior Dasturchi' (ID=5) ning barcha to'g'ridan-to'g'ri va bilvosita rahbarlarini tepaga qarab qidiring.",
        """WITH RECURSIVE rahbarlar AS (
    -- Anchor: Xodimning o'zi
    SELECT xodim_id, ism, rahbar_id 
    FROM kompaniya_tuzilmasi 
    WHERE xodim_id = 5
    
    UNION ALL
    
    -- Tepaga chiqish: rahbariga bog'lanish
    SELECT k.xodim_id, k.ism, k.rahbar_id 
    FROM kompaniya_tuzilmasi k
    JOIN rahbarlar r ON k.xodim_id = r.rahbar_id
)
SELECT xodim_id, ism FROM rahbarlar;""",
        "Bu yerda rekursiya sharti teskari bog'lanadi: `k.xodim_id = r.rahbar_id`. Daraxt ildiziga (root) qadar barcha boshliqlar ketma-ket chiqadi.",
        """ xodim_id |          ism           
----------+------------------------
        5 | Junior Dasturchi
        4 | Bosh Dasturchi
        2 | Texnik Direktor (CTO)
        1 | General Direktor
(4 rows)"""
    ),
    (
        365,
        "Mahsulot katalogi: Ko'p bosqichli kategoriyalar daraxti",
        "E-do'konda istalgan chuqurlikdagi kategoriyalar (Elektronika -> Smartfonlar -> Apple -> iPhone) daraxtini tuzing.",
        """CREATE TABLE katalog (id INT PRIMARY KEY, nom TEXT, ota_id INT);
INSERT INTO katalog VALUES 
(1, 'Elektronika', NULL),
(2, 'Smartfonlar', 1),
(3, 'Apple', 2),
(4, 'iPhone 15 Pro', 3);

WITH RECURSIVE kat_daraxt AS (
    SELECT id, nom, ota_id, nom::TEXT AS toliq_katalog
    FROM katalog 
    WHERE ota_id IS NULL
    
    UNION ALL
    
    SELECT k.id, k.nom, k.ota_id, kd.toliq_katalog || ' / ' || k.nom
    FROM katalog k
    JOIN kat_daraxt kd ON k.ota_id = kd.id
)
SELECT id, toliq_katalog FROM kat_daraxt;""",
        "Har qanday elektron tijorat tizimida cheksiz chuqurlikdagi tovarlar katalogi rekursiv CTE orqali bir zumda tekis (flattened) holatga keltiriladi.",
        """ id |                 toliq_katalog                 
----+-----------------------------------------------
  1 | Elektronika
  2 | Elektronika / Smartfonlar
  3 | Elektronika / Smartfonlar / Apple
  4 | Elektronika / Smartfonlar / Apple / iPhone 15 Pro
(4 rows)"""
    ),
    (
        366,
        "Bo'ysunuvchilarning umumiy sonini rekursiv jamlash",
        "Texnik direktor (CTO) qo'l ostida bilvosita jami nechta xodim ishlashini hisoblang.",
        """WITH RECURSIVE cto_jamoa AS (
    SELECT xodim_id, ism 
    FROM kompaniya_tuzilmasi 
    WHERE xodim_id = 2 -- CTO
    
    UNION ALL
    
    SELECT k.xodim_id, k.ism 
    FROM kompaniya_tuzilmasi k
    JOIN cto_jamoa c ON k.rahbar_id = c.xodim_id
)
SELECT COUNT(*) - 1 AS cto_qol_ostidagilar_soni 
FROM cto_jamoa;""",
        "CTO dan boshlab barcha tarmoqlar rekursiv olinadi. O'zini chiqarib tashlash uchun 'COUNT(*) - 1' qilinadi.",
        """ cto_qol_ostidagilar_soni 
--------------------------
                        2
(1 row)"""
    ),
    (
        367,
        "Graf marshrutlari: A shahardan B shaharga barcha yo'llarni topish",
        "Shaharlar orasidagi parvozlar jadvali bo'yicha Toshkentdan Samarqandga borish yo'llarini qidiring.",
        """CREATE TABLE parvozlar (dan TEXT, ga TEXT, narx NUMERIC);
INSERT INTO parvozlar VALUES 
('Toshkent', 'Buxoro', 400000),
('Buxoro', 'Samarqand', 200000),
('Toshkent', 'Samarqand', 500000);

WITH RECURSIVE marshrut AS (
    SELECT dan, ga, narx, dan || ' -> ' || ga AS yo‘l
    FROM parvozlar 
    WHERE dan = 'Toshkent'
    
    UNION ALL
    
    SELECT m.dan, p.ga, m.narx + p.narx, m.yo‘l || ' -> ' || p.ga
    FROM marshrut m
    JOIN parvozlar p ON m.ga = p.dan
)
SELECT yo‘l, narx FROM marshrut WHERE ga = 'Samarqand';""",
        "Graf nazariyasida yo'l topish (Path Finding): Rekursiv qism bir parvozning tugash nuqtasini (`m.ga`) keyingi parvozning boshlanishiga (`p.dan`) ulaydi va jami narxni jamlab boradi.",
        """              yo‘l              |   narx    
--------------------------------+-----------
 Toshkent -> Samarqand          | 500000.00
 Toshkent -> Buxoro -> Samarqand| 600000.00
(2 rows)"""
    ),
    (
        368,
        "Grafda eng arzon yo'lni (Eng qisqa masofa) topish",
        "Topilgan marshrutlar orasidan eng arzon narxga ega parvozni tanlang.",
        """WITH RECURSIVE marshrut AS (
    SELECT dan, ga, narx, dan || ' -> ' || ga AS yo‘l
    FROM parvozlar 
    WHERE dan = 'Toshkent'
    
    UNION ALL
    
    SELECT m.dan, p.ga, m.narx + p.narx, m.yo‘l || ' -> ' || p.ga
    FROM marshrut m
    JOIN parvozlar p ON m.ga = p.dan
)
SELECT yo‘l, narx 
FROM marshrut 
WHERE ga = 'Samarqand' 
ORDER BY narx ASC 
LIMIT 1;""",
        "ORDER BY narx ASC LIMIT 1 eng optimal yo'lni tanlaydi.",
        """         yo‘l          |   narx    
-----------------------+-----------
 Toshkent -> Samarqand | 500000.00
(1 row)"""
    ),
    (
        369,
        "Sikllarni aniqlash va cheksiz rekursiyadan himoya (CYCLE bandi)",
        "Grafda aylanma yo'l (Toshkent -> Samarqand -> Toshkent) bo'lsa server qotib qolmasligi uchun PostgreSQL 14+ ning CYCLE kalit so'zini ishlating.",
        """INSERT INTO parvozlar VALUES ('Samarqand', 'Toshkent', 300000); -- Sikl hosil qiluvchi yo'l!

WITH RECURSIVE xavfsiz_marshrut AS (
    SELECT dan, ga, ARRAY[dan] AS bosilgan_shaxarlar
    FROM parvozlar 
    WHERE dan = 'Toshkent'
    
    UNION ALL
    
    SELECT p.dan, p.ga, xm.bosilgan_shaxarlar || p.dan
    FROM xavfsiz_marshrut xm
    JOIN parvozlar p ON xm.ga = p.dan
    WHERE NOT (p.ga = ANY(xm.bosilgan_shaxarlar)) -- Siklni to'xtatish
)
SELECT * FROM xavfsiz_marshrut LIMIT 5;""",
        "Agar sikl tekshirilmasa, rekursiya cheksiz davom etib xotirani to'ldiradi. 'bosilgan_shaxarlar' massivi tekshirilib, qayta ayni shaharga tushish taqiqlanadi.",
        """INSERT 0 1
   dan    |    ga     |   bosilgan_shaxarlar    
----------+-----------+-------------------------
 Toshkent | Buxoro    | {Toshkent}
 Toshkent | Samarqand | {Toshkent}
 Buxoro   | Samarqand | {Toshkent,Buxoro}
 Samarqand| Toshkent  | {Toshkent,Samarqand}
 Samarqand| Toshkent  | {Toshkent,Buxoro,Samarqand}
(5 rows)"""
    ),
    (
        370,
        "CTE ichida CTE e'lon qilish (Ichma-ich CTE)",
        "CTE ichida subquery lardan foydalanib murakkab oraliq hisoblar qilish.",
        """WITH xulosa AS (
    SELECT bolim, AVG(maosh) AS o 
    FROM xodimlar_cte 
    GROUP BY bolim
)
SELECT bolim, o 
FROM xulosa 
WHERE o > (SELECT AVG(o) FROM xulosa);""",
        "CTE natijasi oddiy jadval kabi qabul qilinib, uning ustida yana subquery lar bajarilishi mumkin.",
        """ bolim |           o           
-------+-----------------------
 IT    | 15000000.000000000000
(1 row)"""
    ),
    (
        371,
        "Rekursiv CTE bilan satrni belgilarga bo'lish",
        "'DATABASE' so'zining har bir harfini yangi alohida qatorga chiqaruvchi rekursiv so'rov.",
        """WITH RECURSIVE harflar AS (
    SELECT 1 AS orin, SUBSTRING('DATABASE', 1, 1) AS harf
    UNION ALL
    SELECT orin + 1, SUBSTRING('DATABASE', orin + 1, 1)
    FROM harflar 
    WHERE orin < LENGTH('DATABASE')
)
SELECT orin, harf FROM harflar;""",
        "SUBSTRING va rekursiya yordamida satr belgilar bo'yicha iteratsiya qilinadi.",
        """ orin | harf 
------+------
    1 | D
    2 | A
    3 | T
    4 | A
    5 | B
    6 | A
    7 | S
    8 | E
(8 rows)"""
    ),
    (
        372,
        "Bo'sh oraliqlarni to'ldirish (Gap Filling CTE)",
        "Sotuv bo'lmagan sanalarni ham kalendar bilan birlashtirib 0 summa bilan to'ldirish.",
        """WITH RECURSIVE sana_tarmogi AS (
    SELECT '2026-10-01'::DATE AS kun
    UNION ALL
    SELECT (kun + INTERVAL '1 day')::DATE 
    FROM sana_tarmogi 
    WHERE kun < '2026-10-03'
),
haqiqiy_sotuv AS (
    SELECT '2026-10-01'::DATE AS s_kun, 500000::NUMERIC AS s_summa
)
SELECT st.kun, COALESCE(hs.s_summa, 0) AS summa
FROM sana_tarmogi st
LEFT JOIN haqiqiy_sotuv hs ON st.kun = hs.s_kun;""",
        "Bu 'Gap Filling' deb ataladi. Sotuv bo'lmagan 2 va 3 oktyabr kunlari 0 ko'rinishida hisobotda to'liq saqlanadi.",
        """    kun     |   summa   
------------+-----------
 2026-10-01 | 500000.00
 2026-10-02 |      0.00
 2026-10-03 |      0.00
(3 rows)"""
    ),
    (
        373,
        "Daraxtdagi har bir tugunning bolalar sonini hisoblash",
        "Har bir rahbarning bevosita va bilvosita bo'ysunuvchilari sonini bitta so'rovda ko'rsatish.",
        """WITH RECURSIVE barcha_aloqalar AS (
    SELECT rahbar_id AS boshliq_id, xodim_id 
    FROM kompaniya_tuzilmasi 
    WHERE rahbar_id IS NOT NULL
    
    UNION ALL
    
    SELECT ba.boshliq_id, kt.xodim_id 
    FROM barcha_aloqalar ba
    JOIN kompaniya_tuzilmasi kt ON ba.xodim_id = kt.rahbar_id
)
SELECT boshliq_id, COUNT(xodim_id) AS jami_qol_ostidagilar 
FROM barcha_aloqalar 
GROUP BY boshliq_id 
ORDER BY boshliq_id;""",
        "Barcha bo'g'inlar rekursiv kengaytirilgach, oddiy GROUP BY bilan har bir rahbarning jami kadrlar soni olinadi.",
        """ boshliq_id | jami_qol_ostidagilar 
------------+----------------------
          1 |                    4
          2 |                    2
          4 |                    1
(3 rows)"""
    ),
    (
        374,
        "Rekursiv CTE yordamida Bitmask kombinatsiyalarini ochish",
        "0 dan 7 gacha bo'lgan sonlarning ikkilik ko'rinishini hosil qilish.",
        """WITH RECURSIVE bitlar AS (
    SELECT 0 AS son
    UNION ALL
    SELECT son + 1 FROM bitlar WHERE son < 7
)
SELECT son, son::BIT(3) AS ikkilik FROM bitlar;""",
        "Ikkilik registrlar va maskalarni tahlil qilish uchun qulay.",
        """ son | ikkilik 
-----+---------
   0 | 000
   1 | 001
   2 | 010
   3 | 011
   4 | 100
   5 | 101
   6 | 110
   7 | 111
(8 rows)"""
    ),
    (
        375,
        "Kompensatsiya hisoblash: Iyerarxiya bo'yicha maoshlar yig'indisi",
        "Bosh direktor o'z qo'l ostidagi barcha xodimlarning umumiy oylik xarajatini bilsin.",
        """WITH RECURSIVE filial_maosh AS (
    SELECT xodim_id, maosh 
    FROM xodimlar_cte 
    WHERE id = 1
    
    UNION ALL
    
    SELECT x.id, x.maosh 
    FROM xodimlar_cte x 
    JOIN filial_maosh fm ON x.id = fm.xodim_id + 10 -- simulyatsiya
)
SELECT SUM(maosh) FROM filial_maosh;""",
        "Iyerarxik bo'limlar bo'yicha budjet taqsimotini hisoblash rekursiv CTE ning asosiy kuchli jihatlaridan biridir.",
        """     sum     
-------------
 14000000.00
(1 row)"""
    ),
    (
        376,
        "CTE da oynador funksiyalarni ishlatish",
        "CTE ichida ROW_NUMBER hisoblab, tashqi so'rovda faqat 1-o'rindagi yozuvlarni filtrlash.",
        """WITH raqamlangan AS (
    SELECT 
        ism, 
        bolim, 
        maosh,
        ROW_NUMBER() OVER (PARTITION BY bolim ORDER BY maosh DESC) AS rn
    FROM xodimlar_cte
)
SELECT ism, bolim, maosh 
FROM raqamlangan 
WHERE rn = 1;""",
        "WHERE bandida to'g'ridan-to'g'ri oynador funksiya qo'yish mumkin emas. Shuning uchun oynador funksiyalar har doim CTE ichida hisoblanib, tashqarida WHERE rn = 1 qilinadi.",
        """   ism   |   bolim   |    maosh    
---------+-----------+-------------
 Umida   | IT        | 16000000.00
 Otabek  | Logistika |  6000000.00
(2 rows)"""
    ),
    (
        377,
        "CTE yordamida murakkab PIVOT jadval",
        "Har bir bo'limning oylik maoshini qatorlardan ustunlarga o'tkazish.",
        """WITH jamlama AS (
    SELECT bolim, SUM(maosh) AS s FROM xodimlar_cte GROUP BY bolim
)
SELECT 
    MAX(CASE WHEN bolim = 'IT' THEN s END) AS it_fondi,
    MAX(CASE WHEN bolim = 'Logistika' THEN s END) AS logistika_fondi
FROM jamlama;""",
        "CTE va shartli agregatsiya barcha RDBMS larda ishlaydigan eng toza PIVOT mexanizmini beradi.",
        """  it_fondi   | logistika_fondi 
-------------+-----------------
 30000000.00 |      6000000.00
(1 row)"""
    ),
    (
        378,
        "Rekursiv CTE da cheklov: UNION ALL o'rniga UNION xatti-harakati",
        "Rekursiv CTE da UNION (dublikatsiz) va UNION ALL (barcha) farqini ko'ring.",
        """WITH RECURSIVE u_test AS (
    SELECT 1 AS n
    UNION
    SELECT 2 FROM u_test WHERE n = 1
)
SELECT * FROM u_test;""",
        "UNION ALL har doim tezroq ishlaydi, chunki u takrorlanishlarni xotirada tekshirmaydi. Rekursiyada agar dublikat bo'lmasa doimo UNION ALL tanlanadi.",
        """ n 
---
 1
 2
(2 rows)"""
    ),
    (
        379,
        "CTE bilan ma'lumotlarni bosqichma-bosqich tozalash (ETL)",
        "Xom ma'lumotlarni o'qish, bo'sh joylarni tozalash, formatlash va oxirida saralash bosqichlari.",
        """WITH xom_baza AS (
    SELECT '  ali  ' AS ism, '901234567' AS tel
),
tozalangan AS (
    SELECT TRIM(ism) AS toza_ism, '+998' || tel AS toliq_tel 
    FROM xom_baza
)
SELECT * FROM tozalangan;""",
        "Data Engineering (ETL) jarayonlarida CTE har bir transformatsiya qadamini mustaqil mantiqiy blok sifatida saqlaydi.",
        """ toza_ism |   toliq_tel    
----------+----------------
 ali      | +998901234567
(1 row)"""
    ),
    (
        380,
        "Rekursiv yo'l topishda maksimal qadam sonini cheklash",
        "Grafda uzoq aylanib yurmaslik uchun maksimal 3 ta parvozdan iborat yo'llarni cheklash.",
        """WITH RECURSIVE qadamli_parvoz AS (
    SELECT dan, ga, 1 AS sakrashlar_soni
    FROM parvozlar 
    WHERE dan = 'Toshkent'
    
    UNION ALL
    
    SELECT qp.dan, p.ga, qp.sakrashlar_soni + 1
    FROM qadamli_parvoz qp
    JOIN parvozlar p ON qp.ga = p.dan
    WHERE qp.sakrashlar_soni < 3 -- Ko'pi bilan 3 ta transfer
)
SELECT * FROM qadamli_parvoz;""",
        "Bu cheklov algoritm chuqurlashib ketishining va resurslarni haddan tashqari sarflashining oldini oladi.",
        """   dan    |    ga     | sakrashlar_soni 
----------+-----------+-----------------
 Toshkent | Buxoro    |               1
 Toshkent | Samarqand |               1
 Toshkent | Samarqand |               2
 Toshkent | Toshkent  |               2
 Toshkent | Buxoro    |               3
(5 rows)"""
    ),
    (
        381,
        "CTE bilan UPDATE qilish",
        "Top-1 eng ko'p maosh oluvchi xodimga bonus yozish.",
        """WITH eng_yaxshi AS (
    SELECT id FROM xodimlar_cte ORDER BY maosh DESC LIMIT 1
)
UPDATE xodimlar_cte 
SET maosh = maosh + 1000000 
WHERE id IN (SELECT id FROM eng_yaxshi);

SELECT ism, maosh FROM xodimlar_cte WHERE id = 2;""",
        "CTE UPDATE, DELETE va INSERT operatorlari bilan to'liq integratsiyalashgan.",
        """UPDATE 1
  ism  |    maosh    
-------+-------------
 Umida | 17000000.00
(1 row)"""
    ),
    (
        382,
        "Bir nechta jadvallardan olingan ma'lumotlarni CTE da birlashtirib saralash",
        "Mijozlar va ta'minotchilarni bitta umumiy kontaktlar CTE sida yig'ish.",
        """WITH kontaktlar AS (
    SELECT ism, 'Xaridor' AS tur FROM xaridorlar_s
    UNION ALL
    SELECT ism, 'Xodim' AS tur FROM xodimlar_cte
)
SELECT * FROM kontaktlar ORDER BY ism;""",
        "CTE to'plam amallari (UNION) bilan ajoyib tarzda uyg'unlashadi.",
        """   ism   |   tur   
---------+---------
 Farhod  | Xaridor
 Nilufar | Xaridor
 Otabek  | Xodim
 Sherzod | Xodim
 Umida   | Xodim
(5 rows)"""
    ),
    (
        383,
        "Rekursiv CTE yordamida daraxtning barg tugunlarini (Leaf nodes) topish",
        "Qo'l ostida hech qanday xodimi bo'lmagan eng quyi pog'ona xodimlarini aniqlang.",
        """SELECT ism 
FROM kompaniya_tuzilmasi kt 
WHERE NOT EXISTS (
    SELECT 1 FROM kompaniya_tuzilmasi quyi WHERE quyi.rahbar_id = kt.xodim_id
);""",
        "Hech kimga rahbarlik qilmaydigan xodimlar barg tugunlar (leaves) hisoblanadi.",
        """          ism           
------------------------
 Moliya Direktori (CFO)
 Junior Dasturchi
(2 rows)"""
    ),
    (
        384,
        "Rekursiv CTE orqali bo'sh o'rinlarni topish",
        "1 dan 10 gacha raqamlangan xonalardan qaysilari bazada yo'qligini aniqlash.",
        """CREATE TABLE band_xonalar (xona_id INT);
INSERT INTO band_xonalar VALUES (1), (2), (5), (6);

WITH RECURSIVE barcha_10 AS (
    SELECT 1 AS x
    UNION ALL
    SELECT x + 1 FROM barcha_10 WHERE x < 10
)
SELECT x AS bosh_xona 
FROM barcha_10 
WHERE x NOT IN (SELECT xona_id FROM band_xonalar);""",
        "Virtual sonlar hosil qilinib mavjud jadvallar bilan solishtiriladi.",
        """ bosh_xona 
-----------
         3
         4
         7
         8
         9
        10
(6 rows)"""
    ),
    (
        385,
        "CTE da ma'lumotlarni filtrlash va index scan rejalari",
        "PostgreSQL CTE larni optimallashtirishda indekslardan qanday foydalanishini tekshiring.",
        """EXPLAIN WITH m AS (SELECT id, maosh FROM xodimlar_cte WHERE id = 1)
SELECT * FROM m;""",
        "PostgreSQL 12 dan boshlab inline qilingan CTE lar asosiy so'rov kabi B-Tree indekslarini to'liq ishga soladi.",
        """                                QUERY PLAN                                 
-------------------------------------------------------------------------
 Index Scan using xodimlar_cte_pkey on xodimlar_cte  (cost=0.15..8.17 rows=1 width=36)
   Index Cond: (id = 1)
(2 rows)"""
    ),
    (
        386,
        "Ikkita mustaqil rekursiv CTE larni JOIN qilish",
        "Biri oylar, biri haftaning kunlarini hisoblovchi ikki rekursiv CTE ni birlashtirish.",
        """WITH RECURSIVE oylar AS (
    SELECT 1 AS oy
    UNION ALL
    SELECT oy + 1 FROM oylar WHERE oy < 3
),
hafta AS (
    SELECT 1 AS kun
    UNION ALL
    SELECT kun + 1 FROM hafta WHERE kun < 2
)
SELECT oy, kun FROM oylar CROSS JOIN hafta;""",
        "Bir nechta rekursiv jadvallar bitta WITH RECURSIVE ichida vergul orqali yozilishi mumkin.",
        """ oy | kun 
----+-----
  1 |   1
  1 |   2
  2 |   1
  2 |   2
  3 |   1
  3 |   2
(6 rows)"""
    ),
    (
        387,
        "CTE orqali murakkab hisob-kitob natijasini o'zgaruvchi sifatida saqlash",
        "Bir martalik koeffitsiyentni CTE da saqlab, butun hisobot bo'ylab ishlatish.",
        """WITH konversiya AS (
    SELECT 12800.00::NUMERIC AS usd_uzs_kursi
)
SELECT 
    x.ism, 
    x.maosh AS maosh_uzs, 
    ROUND(x.maosh / k.usd_uzs_kursi, 2) AS maosh_usd
FROM xodimlar_cte x, konversiya k;""",
        "So'rovning yuqori qismida barcha biznes koeffitsiyentlari parametr sifatida joylashtiriladi.",
        """   ism   |  maosh_uzs  | maosh_usd 
---------+-------------+-----------
 Sherzod | 14000000.00 |   1093.75
 Umida   | 17000000.00 |   1328.13
 Otabek  |  6000000.00 |    468.75
(3 rows)"""
    ),
    (
        388,
        "Recursive CTE da String agregatsiyasi",
        "Rekursiv yo'l davomida barcha oraliq shaharlarni massivga to'plash.",
        """WITH RECURSIVE yo‘l_massiv AS (
    SELECT dan, ga, ARRAY[dan, ga] AS marshrut
    FROM parvozlar 
    WHERE dan = 'Toshkent' AND ga = 'Buxoro'
    
    UNION ALL
    
    SELECT ym.dan, p.ga, ym.marshrut || p.ga
    FROM yo‘l_massiv ym
    JOIN parvozlar p ON ym.ga = p.dan
    WHERE NOT (p.ga = ANY(ym.marshrut))
)
SELECT * FROM yo‘l_massiv;""",
        "Massivlar rekursiv holatni (state) xotirada saqlab borishning eng qulay vositasidir.",
        """   dan    |    ga     |          marshrut          
----------+-----------+----------------------------
 Toshkent | Buxoro    | {Toshkent,Buxoro}
 Toshkent | Samarqand | {Toshkent,Buxoro,Samarqand}
(2 rows)"""
    ),
    (
        389,
        "CTE bilan ma'lumotlar yaxlitligini tekshirish (Audit qoidalari)",
        "Sxemada qaysi xodimlarning bo'limi yo'qligini CTE orqali audit qilish.",
        """WITH xatolar AS (
    SELECT id, ism FROM xodimlar_cte WHERE bolim IS NULL
)
SELECT 
    CASE WHEN COUNT(*) = 0 THEN 'Ma''lumotlar toza' ELSE 'Xatolar mavjud' END AS audit_holat
FROM xatolar;""",
        "Avtomatik testlar va ma'lumotlar sifatini (Data Quality) tekshirishda CTE juda qulay.",
        """   audit_holat    
------------------
 Ma'lumotlar toza
(1 row)"""
    ),
    (
        390,
        "Rekursiv CTE bilan cheksiz bo'linuvchi struktura (Bill of Materials - BOM)",
        "Murakkab avtomobil detallari (Avto -> Dvigatel -> Porshen -> Bolt) tarkibiy qismlarini yoyish.",
        """CREATE TABLE bom (qism_id INT, ota_qism_id INT, nom TEXT, miqdor INT);
INSERT INTO bom VALUES 
(1, NULL, 'Avtomobil', 1),
(2, 1, 'Dvigatel', 1),
(3, 2, 'Porshen', 4),
(4, 3, 'Halqa', 3);

WITH RECURSIVE bom_daraxt AS (
    SELECT qism_id, nom, miqdor, miqdor AS umumiy_dona
    FROM bom 
    WHERE ota_qism_id IS NULL
    
    UNION ALL
    
    SELECT b.qism_id, b.nom, b.miqdor, bd.umumiy_dona * b.miqdor
    FROM bom b
    JOIN bom_daraxt bd ON b.ota_qism_id = bd.qism_id
)
SELECT nom, umumiy_dona FROM bom_daraxt;""",
        "Ishlab chiqarish korxonalarida 1 ta avtomobil uchun jami nechta halqa kerakligini (1 * 1 * 4 * 3 = 12 dona) rekursiv ko'paytirib hisoblash (BOM Explosion).",
        """    nom    | umumiy_dona 
-----------+-------------
 Avtomobil |           1
 Dvigatel  |           1
 Porshen   |           4
 Halqa     |          12
(4 rows)"""
    ),
    (
        391,
        "CTE va DELETE da LIMIT xulqi",
        "Katta hajmdagi ma'lumotlarni CTE orqali qismlab tozalash.",
        """WITH ochiriladigan AS (
    SELECT id FROM xodimlar_cte LIMIT 1
)
DELETE FROM xodimlar_cte 
WHERE id IN (SELECT id FROM ochiriladigan);""",
        "CTE orqali avval kerakli qatorlar tanlab olinadi va DELETE ga beriladi.",
        """DELETE 1
Query returned successfully in 28 msec."""
    ),
    (
        392,
        "CTE ichida DISTINCT ON qo'llash",
        "Har bir mijozning birinchi xaridini CTE da aniqlab keyin unga chegirma hisoblash.",
        """WITH birinchi_xaridlar AS (
    SELECT DISTINCT ON (xaridor_id) xaridor_id, id AS xarid_id, summa 
    FROM xaridlar_s 
    WHERE xaridor_id IS NOT NULL 
    ORDER BY xaridor_id, id ASC
)
SELECT * FROM birinchi_xaridlar;""",
        "DISTINCT ON va CTE birgalikda eng toza oraliq natijani shakllantiradi.",
        """ xaridor_id | xarid_id |   summa   
------------+----------+-----------
          1 |      101 | 200000.00
          2 |      103 |  90000.00
(2 rows)"""
    ),
    (
        393,
        "Rekursiv CTE bilan geometrik progressiya",
        "Har qadamda 2 ga ko'payib boruvchi 2^0 dan 2^8 gacha sonlarni hisoblang.",
        """WITH RECURSIVE daraja AS (
    SELECT 0 AS n, 1::BIGINT AS qiymat
    UNION ALL
    SELECT n + 1, qiymat * 2 
    FROM daraja 
    WHERE n < 8
)
SELECT n, qiymat FROM daraja;""",
        "Har qadamda eksponensial o'suvchi progressiyalar hosil qilinadi.",
        """ n | qiymat 
---+--------
 0 |      1
 1 |      2
 2 |      4
 3 |      8
 4 |     16
 5 |     32
 6 |     64
 7 |    128
 8 |    256
(9 rows)"""
    ),
    (
        394,
        "CTE orqali jadvallarni taqqoslash (Diff / Comparison)",
        "Ikki jadval o'rtasidagi farqlarni (qaysi qatorlar o'zgarganini) CTE yordamida ko'rish.",
        """WITH t1 AS (SELECT 1 AS id, 'A' AS val),
     t2 AS (SELECT 1 AS id, 'B' AS val)
SELECT 
    COALESCE(t1.id, t2.id) AS id,
    t1.val AS eski_qiymat,
    t2.val AS yangi_qiymat
FROM t1 FULL JOIN t2 ON t1.id = t2.id
WHERE t1.val IS DISTINCT FROM t2.val;""",
        "Ma'lumotlar bazalarini replikatsiyadan keyin yoki migratsiyadan keyin tekshirishda ajoyib vosita.",
        """ id | eski_qiymat | yangi_qiymat 
----+-------------+--------------
  1 | A           | B
(1 row)"""
    ),
    (
        395,
        "Ko'p pog'onali Writable CTE Pipeline",
        "Foydalanuvchini faolsizlantirish, uning tokenini o'chirish va logga yozishni bitta WITH da bajarish.",
        """CREATE TABLE log_table (xabar TEXT);

WITH block_user AS (
    SELECT 10 AS u_id
),
insert_log AS (
    INSERT INTO log_table (xabar)
    SELECT 'User ' || u_id || ' bloklandi' FROM block_user
    RETURNING xabar
)
SELECT * FROM insert_log;""",
        "Bir nechta DML o'zgarishlari bitta zanjirda bog'lanadi.",
        """CREATE TABLE
          xabar          
-------------------------
 User 10 bloklandi
(1 row)"""
    ),
    (
        396,
        "Rekursiv CTE yordamida sanalardan hafta kunlarini ajratish",
        "Haftaning barcha ish kunlarini (dushanba-juma) avtomatik filtrlash.",
        """WITH RECURSIVE kunlar AS (
    SELECT '2026-11-02'::DATE AS d -- Dushanba
    UNION ALL
    SELECT (d + INTERVAL '1 day')::DATE 
    FROM kunlar 
    WHERE d < '2026-11-08'
)
SELECT d, TO_CHAR(d, 'Day') AS hafta_kuni 
FROM kunlar 
WHERE EXTRACT(ISODOW FROM d) <= 5;""",
        "ISODOW (1-dushanba, 7-yakshanba) orqali faqat ish kunlari saralab olinadi.",
        """     d      | hafta_kuni 
------------+------------
 2026-11-02 | Monday   
 2026-11-03 | Tuesday  
 2026-11-04 | Wednesday
 2026-11-05 | Thursday 
 2026-11-06 | Friday   
(5 rows)"""
    ),
    (
        397,
        "CTE da JOIN larni qisqartirish va o'qishlilikni oshirish",
        "Murakkab shartli jadvallarni avval CTE da tozalab olib keyin JOIN qilish.",
        """WITH faol_xodimlar AS (
    SELECT id, ism, maosh FROM xodimlar_cte WHERE maosh >= 10000000
)
SELECT fx.ism, fx.maosh 
FROM faol_xodimlar fx;""",
        "Katta korporativ kod bazalarida har bir mantiqiy blok mustaqil CTE bo'lishi kodni refaktoring qilishni nihoyatda yengillashtiradi.",
        """  ism  |    maosh    
-------+-------------
 Umida | 17000000.00
(1 row)"""
    ),
    (
        398,
        "Rekursiv CTE orqali satrdagi so'zlarni sanash",
        "Bo'shliqlar bilan ajratilgan gapdagi so'zlar sonini rekursiv aniqlash.",
        """WITH RECURSIVE sozlar AS (
    SELECT 1 AS indeks, SPLIT_PART('PostgreSQL juda tez va kuchli baza', ' ', 1) AS soz
    UNION ALL
    SELECT indeks + 1, SPLIT_PART('PostgreSQL juda tez va kuchli baza', ' ', indeks + 1)
    FROM sozlar 
    WHERE SPLIT_PART('PostgreSQL juda tez va kuchli baza', ' ', indeks + 1) <> ''
)
SELECT COUNT(*) AS jami_sozlar FROM sozlar;""",
        "Matnlarni tahlil qilish va tabiiy tilni qayta ishlashga (NLP) tayyorlashda sof SQL usuli.",
        """ jami_sozlar 
-------------
           6
(1 row)"""
    ),
    (
        399,
        "CTE bilan o'rtacha qiymatdan chetlanish koeffitsiyenti",
        "Kompaniya maoshlarining o'rtacha kvadratik chetlanishini CTE lar orqali hisoblash.",
        """WITH stat AS (
    SELECT AVG(maosh) AS o, STDDEV(maosh) AS s FROM xodimlar_cte
)
SELECT 
    x.ism, 
    x.maosh,
    ROUND((x.maosh - s.o) / NULLIF(s.s, 0), 2) AS z_score
FROM xodimlar_cte x, stat s;""",
        "Statistikadagi Z-Score ko'rsatkichi har bir xodim maoshining anomaliyasini aniqlab beradi.",
        """  ism   |    maosh    | z_score 
--------+-------------+---------
 Umida  | 17000000.00 |    0.71
 Otabek |  6000000.00 |   -0.71
(2 rows)"""
    ),
    (
        400,
        "Korporativ Rekursiv CTE: Holding tuzilmasi bo'yicha to'liq konsolidatsiya",
        "Yirik holding kompaniyasining sho'ba korxonalari (Subsidiaries), ularning filiallari va bo'limlari bo'yicha jami xodimlar soni va moliyaviy aylanmasini to'liq daraxt bo'ylab jamlang.",
        """CREATE TABLE holding_tuzilmasi (
    birlik_id INT PRIMARY KEY,
    nomi VARCHAR(100) NOT NULL,
    ota_birlik_id INT,
    oylik_aylanma NUMERIC(15, 2) NOT NULL
);

INSERT INTO holding_tuzilmasi VALUES 
(1, 'Asosiy Holding AJ', NULL, 100000000),
(2, 'FinTech Sho‘ba Korxonasi', 1, 50000000),
(3, 'Tog‘-kon Sho‘ba Korxonasi', 1, 80000000),
(4, 'Toshkent Filiali (FinTech)', 2, 20000000),
(5, 'Samarqand Filiali (FinTech)', 2, 15000000),
(6, 'Navoiy Kon Boshqarmasi', 3, 60000000);

WITH RECURSIVE holding_daraxt AS (
    -- Anchor: Asosiy bosh holding
    SELECT 
        birlik_id, 
        nomi, 
        ota_birlik_id, 
        oylik_aylanma, 
        1 AS iyerarxiya_darajasi,
        nomi::TEXT AS boshqaruv_zanjiri
    FROM holding_tuzilmasi
    WHERE ota_birlik_id IS NULL

    UNION ALL

    -- Rekursiv qism: Barcha sho'balar va filiallar
    SELECT 
        ht.birlik_id, 
        ht.nomi, 
        ht.ota_birlik_id, 
        ht.oylik_aylanma, 
        hd.iyerarxiya_darajasi + 1,
        hd.boshqaruv_zanjiri || ' ==> ' || ht.nomi
    FROM holding_tuzilmasi ht
    JOIN holding_daraxt hd ON ht.ota_birlik_id = hd.birlik_id
)
SELECT 
    iyerarxiya_darajasi,
    nomi AS korxona_birligi,
    oylik_aylanma,
    boshqaruv_zanjiri
FROM holding_daraxt
ORDER BY iyerarxiya_darajasi, birlik_id;""",
        "Ushbu so'rov yirik xalqaro korporatsiyalarda konsolidatsiyalangan moliyaviy hisobotlarni (Consolidated Financial Statements) tuzishda qo'llaniladi: holding boshidan to eng chekka sho'ba korxonasigacha bo'lgan iyerarxiya to'liq ochiladi, darajalar belgilanadi va boshqaruv zanjiri to'liq vizuallashadi.",
        """ iyerarxiya_darajasi |      korxona_birligi       | oylik_aylanma |                              boshqaruv_zanjiri                               
---------------------+----------------------------+---------------+------------------------------------------------------------------------------
                   1 | Asosiy Holding AJ          |  100000000.00 | Asosiy Holding AJ
                   2 | FinTech Sho‘ba Korxonasi   |   50000000.00 | Asosiy Holding AJ ==> FinTech Sho‘ba Korxonasi
                   2 | Tog‘-kon Sho‘ba Korxonasi  |   80000000.00 | Asosiy Holding AJ ==> Tog‘-kon Sho‘ba Korxonasi
                   3 | Toshkent Filiali (FinTech) |   20000000.00 | Asosiy Holding AJ ==> FinTech Sho‘ba Korxonasi ==> Toshkent Filiali (FinTech)
                   3 | Samarqand Filiali (FinTech)|   15000000.00 | Asosiy Holding AJ ==> FinTech Sho‘ba Korxonasi ==> Samarqand Filiali (FinTech)
                   3 | Navoiy Kon Boshqarmasi     |   60000000.00 | Asosiy Holding AJ ==> Tog‘-kon Sho‘ba Korxonasi ==> Navoiy Kon Boshqarmasi
(6 rows)"""
    )
]

formatted = [format_task(*item) for item in cte_data]
save_file("sql_08_cte_va_rekursiv_sorovlar.md", formatted)
