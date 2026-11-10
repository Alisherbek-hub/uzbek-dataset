import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

# List of 50 tasks for File 11: 501 - 550
# To'plam amallari (Set Operations: UNION, UNION ALL, INTERSECT, INTERSECT ALL, EXCEPT, EXCEPT ALL, Data Reconciliation, Set Theory)

set_data = [
    (
        501,
        "To'plamlar birlashmasi: UNION asoslari (Dublikatlarni yo'qotish)",
        "Toshkent va Samarqand filiallari mijozlarining telefon raqamlarini takrorlanishlarsiz birlashtiring.",
        """CREATE TABLE filial_toshkent (id INT, ism TEXT, telefon VARCHAR(20));
CREATE TABLE filial_samarqand (id INT, ism TEXT, telefon VARCHAR(20));

INSERT INTO filial_toshkent VALUES 
(1, 'Ali', '+998901112233'), 
(2, 'Vali', '+998902223344');

INSERT INTO filial_samarqand VALUES 
(10, 'Gani', '+998903334455'), 
(11, 'Ali', '+998901112233'); -- Ikkala filialda ham bor mijoz!

SELECT telefon FROM filial_toshkent
UNION
SELECT telefon FROM filial_samarqand;""",
        "'UNION' ikkita SELECT natijasini birlashtiradi va takrorlanuvchi qatorlarni yo'qotish uchun natijani xotirada saralaydi (yoki hash jadval tuzadi). 'Ali' ning telefon raqami ikkala filialda bo'lsa-da, natijada faqat 1 marta chiqadi.",
        """    telefon     
----------------
 +998901112233
 +998902223344
 +998903334455
(3 rows)"""
    ),
    (
        502,
        "Tezkor birlashma: UNION ALL (Dublikatlarni saqlab qolish)",
        "Barcha filiallarning tranzaksiyalarini hech qanday saralashsiz tezkorlik bilan birlashtiring.",
        """SELECT ism, telefon FROM filial_toshkent
UNION ALL
SELECT ism, telefon FROM filial_samarqand;""",
        "'UNION ALL' dublikatlarni tekshirmaydi va saralamaydi, shunchaki ikkinchi natijani birinchisining ketiga ulaydi (Append operatori). Bu UNION ga qaraganda ancha tez va tejamkor ishlaydi.",
        """ ism  |    telefon    
------+---------------
 Ali  | +998901112233
 Vali | +998902223344
 Gani | +998903334455
 Ali  | +998901112233
(4 rows)"""
    ),
    (
        503,
        "UNION vs UNION ALL: Unumdorlik va qachon qaysi biri ishlatiladi?",
        "Optimizator darajasida UNION va UNION ALL farqini ko'rsating.",
        """SELECT 'Agar dublikatlar bo‘lmasligi aniq bo‘lsa yoki dublikatlar kerak bo‘lsa, DOIMO UNION ALL ishlatilishi shart' AS qoida;""",
        "UNION barcha qatorlarni xotirada tekshirishi (Unique Sort) tufayli millionlab qatorlarda sekinlashuvga olib keladi. UNION ALL esa to'g'ridan-to'g'ri oqim (stream) orqali yuboriladi.",
        """                                                 qoida                                                 
-------------------------------------------------------------------------------------------------------
 Agar dublikatlar bo‘lmasligi aniq bo‘lsa yoki dublikatlar kerak bo‘lsa, DOIMO UNION ALL ishlatilishi shart
(1 row)"""
    ),
    (
        504,
        "To'plamlar kesishmasi: INTERSECT",
        "Bir vaqtning o'zida ham Toshkent, ham Samarqand filialida ro'yxatdan o'tgan umumiy mijozlarni toping.",
        """SELECT telefon FROM filial_toshkent
INTERSECT
SELECT telefon FROM filial_samarqand;""",
        "'INTERSECT' ikkala to'plamda ham mavjud bo'lgan umumiy elementlarni (kesishma \u2229) qaytaradi va dublikatlarni olib tashlaydi.",
        """    telefon     
----------------
 +998901112233
(1 row)"""
    ),
    (
        505,
        "Dublikatlar sonini inobatga oluvchi kesishma: INTERSECT ALL",
        "Agar qator 1-jadvalda 3 marta, 2-jadvalda 2 marta bo'lsa, INTERSECT ALL nechta qaytarishini ko'ring.",
        """CREATE TABLE t_a (son INT);
CREATE TABLE t_b (son INT);
INSERT INTO t_a VALUES (5), (5), (5);
INSERT INTO t_b VALUES (5), (5);

SELECT son FROM t_a
INTERSECT ALL
SELECT son FROM t_b;""",
        "'INTERSECT ALL' har ikkala to'plamdagi takrorlanishlar sonining minimalini (min(3, 2) = 2) qaytaradi. Natijada aynan 2 ta '5' chiqadi.",
        """ son 
-----
   5
   5
(2 rows)"""
    ),
    (
        506,
        "To'plamlar ayirmasi: EXCEPT (MINUS)",
        "Faqat Toshkent filialiga tegishli bo'lgan (Samarqand filialida umuman yo'q) mijozlarni toping.",
        """SELECT telefon FROM filial_toshkent
EXCEPT
SELECT telefon FROM filial_samarqand;""",
        "'EXCEPT' (ba'zi tizimlarda MINUS) birinchi to'plamdan ikkinchi to'plamda mavjud barcha elementlarni chiqarib tashlaydi (A \ B).",
        """    telefon     
----------------
 +998902223344
(1 row)"""
    ),
    (
        507,
        "Dublikatlar soni bilan ayirma: EXCEPT ALL",
        "1-jadvaldagi takrorlanishlar sonidan 2-jadvaldagi takrorlanishlar sonini ayirib qolganini ko'rsatish.",
        """SELECT son FROM t_a
EXCEPT ALL
SELECT son FROM t_b;""",
        "'EXCEPT ALL' birinchi to'plamdagi sonlar miqdoridan ikkinchi to'plamdagi sonlar miqdorini ayiradi: 3 - 2 = 1. Natijada aynan 1 ta '5' qoladi.",
        """ son 
-----
   5
(1 row)"""
    ),
    (
        508,
        "Ustunlar mosligi qoidasi (Number of columns mismatch)",
        "Ikkala SELECT dagi ustunlar soni teng bo'lmasa nima bo'lishini ko'ring.",
        """-- Xato so'rov:
-- SELECT id, ism FROM filial_toshkent UNION SELECT id FROM filial_samarqand;
SELECT 'To‘plam amallarida barcha SELECT larning ustunlar soni bir xil bo‘lishi shart' AS talab;""",
        "Relyatsion to'plam amallarida har bir SELECT aynan bir xil miqdordagi ustunlarni qaytarishi shart, aks holda 'each UNION query must have the same number of columns' xatoligi yuzaga keladi.",
        """                                 talab                                  
------------------------------------------------------------------------
 To‘plam amallarida barcha SELECT larning ustunlar soni bir xil bo‘lishi shart
(1 row)"""
    ),
    (
        509,
        "Ustunlar ma'lumot turlari mosligi (Type compatibility)",
        "Son va matn ustunlarini UNION qilishda tur o'zgartirish (Type Casting).",
        """SELECT id::TEXT AS identifikator FROM filial_toshkent
UNION ALL
SELECT telefon AS identifikator FROM filial_samarqand;""",
        "Barcha mos ustunlarning ma'lumot turlari bir-biriga mos kelishi yoki umumiy turga konvertatsiya qilinishi (masalan, ::TEXT) shart.",
        """ identifikator  
----------------
 1
 2
 +998903334455
 +998901112233
(4 rows)"""
    ),
    (
        510,
        "Natijaviy ustun nomlari birinchi SELECT dan olinishi",
        "Ikkinchi SELECT da boshqa nom berilgan bo'lsa ham birinchi SELECT nomi ustun bo'lishini ko'ring.",
        """SELECT ism AS asosiy_nom FROM filial_toshkent
UNION ALL
SELECT ism AS ikkinchi_nom FROM filial_samarqand;""",
        "Natijaviy virtual jadval ustunlari har doim eng birinchi SELECT bandidagi sarlavha va taxalluslar (aliases) asosida shakllanadi.",
        """ asosiy_nom 
------------
 Ali
 Vali
 Gani
 Ali
(4 rows)"""
    ),
    (
        511,
        "To'plam amallarida tartiblash qoidasi (ORDER BY joylashuvi)",
        "ORDER BY buyrug'i butun to'plamning eng oxirida yozilishi shartligi.",
        """SELECT ism, telefon FROM filial_toshkent
UNION ALL
SELECT ism, telefon FROM filial_samarqand
ORDER BY ism ASC;""",
        "ORDER BY butun birlashgan to'plamga nisbatan qo'llaniladi. Agar alohida ichki SELECT ni tartiblash kerak bo'lsa, u qavs ichiga olinishi va LIMIT bilan birga ishlatilishi lozim.",
        """ ism  |    telefon    
------+---------------
 Ali  | +998901112233
 Ali  | +998901112233
 Gani | +998903334455
 Vali | +998902223344
(4 rows)"""
    ),
    (
        512,
        "Qavslar bilan alohida LIMIT va ORDER BY berish",
        "Toshkent filialidan top-1 va Samarqand filialidan top-1 mijozni olib birlashtiring.",
        """(SELECT ism FROM filial_toshkent ORDER BY id ASC LIMIT 1)
UNION ALL
(SELECT ism FROM filial_samarqand ORDER BY id ASC LIMIT 1);""",
        "Qavslar `(SELECT ...)` har bir so'rovning o'ziga xos shaxsiy ORDER BY va LIMIT ini bajarishga imkon beradi, so'ngra hosil bo'lgan ikkita qator birlashtiriladi.",
        """ ism  
------
 Ali
 Gani
(2 rows)"""
    ),
    (
        513,
        "Jadvallar o'rtasidagi to'liq simmetrik farq (Symmetric Difference)",
        "Ikkala jadvalda bir-biriga mos kelmaydigan barcha farqlarni (A \\ B) U (B \\ A) toping.",
        """(SELECT telefon FROM filial_toshkent EXCEPT SELECT telefon FROM filial_samarqand)
UNION ALL
(SELECT telefon FROM filial_samarqand EXCEPT SELECT telefon FROM filial_toshkent);""",
        "Simmetrik farq jadvallarni taqqoslashda va nomuvofiqliklarni topishda eng ishonchli relyatsion formuladir.",
        """    telefon     
----------------
 +998902223344
 +998903334455
(2 rows)"""
    ),
    (
        514,
        "Jadvallarning 100% aynan bir xilligini tekshirish (Data Reconciliation)",
        "Ikkita jadval o'zaro to'liq mos keladimi yoki yo'qligini tekshiruvchi so'rov yozing.",
        """SELECT CASE 
    WHEN COUNT(*) = 0 THEN '✅ Jadvallar to‘liq bir xil'
    ELSE '❌ Jadvallarda tafovut mavjud'
END AS tekshiruv_natijasi
FROM (
    (SELECT * FROM filial_toshkent EXCEPT SELECT * FROM filial_samarqand)
    UNION ALL
    (SELECT * FROM filial_samarqand EXCEPT SELECT * FROM filial_toshkent)
) farqlar;""",
        "Agar simmetrik ayirma bo'sh bo'lsa (COUNT=0), demak ikki jadval ma'lumotlari 100% bir-birini takrorlaydi. Bank tizimlarida kun yakuni (End of Day reconciliation) shunday tekshiriladi.",
        """     tekshiruv_natijasi      
-----------------------------
 ❌ Jadvallarda tafovut mavjud
(1 row)"""
    ),
    (
        515,
        "UNION ALL bilan manba jadvalni ko'rsatish (Provenance tracking)",
        "Qator qaysi filialdan kelganini bilish uchun qo'shimcha statik ustun qo'shing.",
        """SELECT 'Toshkent' AS filial, ism, telefon FROM filial_toshkent
UNION ALL
SELECT 'Samarqand' AS filial, ism, telefon FROM filial_samarqand;""",
        "Statik literal (`'Toshkent' AS filial`) qo'shish orqali birlashgan ma'lumotlarning manbasi (data provenance) aniq saqlanadi.",
        """  filial   | ism  |    telefon    
-----------+------+---------------
 Toshkent  | Ali  | +998901112233
 Toshkent  | Vali | +998902223344
 Samarqand | Gani | +998903334455
 Samarqand | Ali  | +998901112233
(4 rows)"""
    ),
    (
        516,
        "To'plam amallarining ustuvorligi (Precedence)",
        "UNION va INTERSECT birga kelganda qaysi biri oldin bajarilishini ko'rsating.",
        """SELECT 1 AS n
UNION
SELECT 2
INTERSECT
SELECT 2;""",
        "SQL standartida 'INTERSECT' operatorining ustuvorligi 'UNION' va 'EXCEPT' ga qaraganda YUQORI (ko'paytirish qo'shishdan oldin kelgani kabi). Shu bois avval `2 INTERSECT 2` bajariladi, so'ng `1 UNION 2` bo'ladi.",
        """ n 
---
 1
 2
(2 rows)"""
    ),
    (
        517,
        "Qavslar orqali ustuvorlikni o'zgartirish",
        "Oldin UNION, keyin INTERSECT bajarilishi uchun qavslardan foydalaning.",
        """(SELECT 1 AS n UNION SELECT 2)
INTERSECT
SELECT 2;""",
        "Qavslar ustuvorlikni qat'iy belgilaydi. Avval 1 va 2 birlashadi, keyin 2 bilan kesishib faqat 2 qoladi.",
        """ n 
---
 2
(1 row)"""
    ),
    (
        518,
        "NULL qiymatlarning to'plam amallaridagi xulqi",
        "UNION va INTERSECT da NULL qiymatlar bir-biriga teng deb hisoblanadimi?",
        """SELECT NULL AS qiymat
UNION
SELECT NULL;""",
        "To'plam amallarida (UNION, INTERSECT, EXCEPT) NULL qiymatlar boshqa barcha taqqoslashlardan farqli ravishda 'teng' (NOT DISTINCT) deb baholanadi. Shu bois ikkita NULL birlashganda faqat 1 ta NULL qoladi.",
        """ qiymat 
--------
 NULL
(1 row)"""
    ),
    (
        519,
        "INTERSECT o'rniga INNER JOIN ishlatish",
        "INTERSECT ning JOIN orqali ekvivalenti va unumdorlik farqi.",
        """SELECT DISTINCT t.telefon 
FROM filial_toshkent t
JOIN filial_samarqand s ON t.telefon = s.telefon;""",
        "INTERSECT ikkala tomonni to'liq saralaydi. Agar telefon ustunida B-Tree indeks bo'lsa, INNER JOIN ancha tezroq ishlaydi.",
        """    telefon     
----------------
 +998901112233
(1 row)"""
    ),
    (
        520,
        "EXCEPT o'rniga NOT EXISTS ishlatish",
        "EXCEPT operatsiyasini NOT EXISTS orqali tezlashtirish.",
        """SELECT DISTINCT t.telefon 
FROM filial_toshkent t
WHERE NOT EXISTS (
    SELECT 1 FROM filial_samarqand s WHERE s.telefon = t.telefon
);""",
        "NOT EXISTS qidiruvni indeks orqali Anti-Join bilan amalga oshiradi va EXCEPT ga qaraganda katta jadvallarda kamroq xotira sarflaydi.",
        """    telefon     
----------------
 +998902223344
(1 row)"""
    ),
    (
        521,
        "To'plam natijasini CTE ichiga o'rash",
        "Birlashgan mijozlar ro'yxati ustida keyingi filtrlash va saralashni bajarish.",
        """WITH barcha_mijozlar AS (
    SELECT ism, telefon FROM filial_toshkent
    UNION
    SELECT ism, telefon FROM filial_samarqand
)
SELECT ism, telefon 
FROM barcha_mijozlar 
WHERE ism LIKE 'A%'
ORDER BY telefon DESC;""",
        "To'plam amallari natijasi CTE ichiga olinib, uning ustida oddiy jadvallardagi kabi WHERE va ORDER BY qo'llanadi.",
        """ ism |    telefon    
-----+---------------
 Ali | +998901112233
(1 row)"""
    ),
    (
        522,
        "To'plam amallarida umumiy agregatsiya (COUNT)",
        "Barcha filiallarning takrorlanmas noyob mijozlari sonini hisoblang.",
        """SELECT COUNT(*) AS jami_noyob_mijozlar 
FROM (
    SELECT telefon FROM filial_toshkent
    UNION
    SELECT telefon FROM filial_samarqand
) umumiy;""",
        "UNION qilgandan so'ng tashqi COUNT(*) aniq noyob mijozlar sonini chiqaradi.",
        """ jami_noyob_mijozlar 
----------------------
                    3
(1 row)"""
    ),
    (
        523,
        "Bir nechta SELECT larni ketma-ket UNION qilish",
        "Uchta turli hudud (Toshkent, Samarqand, Farg'ona) ma'lumotlarini birlashtirish.",
        """SELECT 'Toshkent' AS shahar UNION ALL
SELECT 'Samarqand' UNION ALL
SELECT 'Farg‘ona';""",
        "Zanjirda istalgancha ko'p SELECT operatorlari ketma-ket birlashishi mumkin.",
        """   shahar   
------------
 Toshkent
 Samarqand
 Farg‘ona
(3 rows)"""
    ),
    (
        524,
        "Statik ro'yxat (Mock data) hosil qilish: UNION ALL yordamida",
        "Jadval ochmasdan xotirada virtual ma'lumotlar to'plamini hosil qiling.",
        """SELECT 1 AS kod, 'Yangi' AS holat UNION ALL
SELECT 2, 'Jarayonda' UNION ALL
SELECT 3, 'Bajarildi';""",
        "Testlar va kichik ma'lumotnomalarni tezkor ifodalashda juda qulay.",
        """ kod |   holat   
-----+-----------
   1 | Yangi
   2 | Jarayonda
   3 | Bajarildi
(3 rows)"""
    ),
    (
        525,
        "To'plamlar bilan qidiruv: Google Search uslubidagi natijalarni birlashtirish",
        "Bir vaqtning o'zida ham maqolalar sarlavhasi, ham mualliflar ismi bo'yicha qidirib natijalarni bitta ro'yxatda chiqarish.",
        """CREATE TABLE blog_m (id INT, sarlavha TEXT);
CREATE TABLE user_m (id INT, ism TEXT);
INSERT INTO blog_m VALUES (1, 'SQL optimallashtirish');
INSERT INTO user_m VALUES (10, 'Ali Dasturchi');

SELECT 'Maqola' AS tur, sarlavha AS matn FROM blog_m WHERE sarlavha ILIKE '%sql%'
UNION ALL
SELECT 'Muallif' AS tur, ism AS matn FROM user_m WHERE ism ILIKE '%ali%';""",
        "Universal global qidiruv tizimlarining arxitekturasi turli xil jadvallardagi mosliklarni UNION ALL orqali yagona qidiruv ro'yxatiga yig'adi.",
        """   tur   |         matn          
---------+-----------------------
 Maqola  | SQL optimallashtirish
 Muallif | Ali Dasturchi
(2 rows)"""
    ),
    (
        526,
        "To'plam amallarida turli ustun tiplari xatosi",
        "VARCHAR va INTEGER ustunlari to'g'ridan-to'g'ri UNION bo'lmasligini ko'ring.",
        """-- Xato: SELECT 123 UNION SELECT 'matn';
SELECT 'PostgreSQL tiplar mos bo‘lmasa avtomatik o‘tkazmaydi, aniq CAST talab qiladi' AS xulosa;""",
        "MySQL ba'zan tiplarni yashirin o'girishi mumkin, ammo qat'iy standartlarga ega PostgreSQL 'UNION types integer and text cannot be matched' xatosini qaytaradi.",
        """                                                xulosa                                                
------------------------------------------------------------------------------------------------------
 PostgreSQL tiplar mos bo‘lmasa avtomatik o‘tkazmaydi, aniq CAST talab qiladi
(1 row)"""
    ),
    (
        527,
        "EXCEPT yordamida ruxsat berilmagan xatti-harakatlarni aniqlash",
        "Xavfsizlik tizimida: qilingan amallar ichidan ruxsat etilgan amallar ro'yxatida bo'lmaganlarini toping.",
        """CREATE TABLE bajarilgan_amallar (amal TEXT);
CREATE TABLE ruxsatlar (amal TEXT);

INSERT INTO bajarilgan_amallar VALUES ('LOGIN'), ('VIEW_REPORT'), ('DELETE_DATABASE');
INSERT INTO ruxsatlar VALUES ('LOGIN'), ('VIEW_REPORT');

SELECT amal AS qonunbuzarlik 
FROM bajarilgan_amallar
EXCEPT
SELECT amal 
FROM ruxsatlar;""",
        "Audit va xavfsizlik nazoratida noqonuniy amallarni topishning eng ishonchli usuli.",
        """  qonunbuzarlik  
-----------------
 DELETE_DATABASE
(1 row)"""
    ),
    (
        528,
        "Venn diagrammasi: Faqat A, Faqat B va Ikkalasida ham bor qismlar",
        "Ikki to'plamning barcha mantiqiy sohalarini alohida belgilab chiqaring.",
        """SELECT telefon, 'Faqat Toshkent' AS holat FROM filial_toshkent
EXCEPT
SELECT telefon, 'Faqat Toshkent' FROM filial_samarqand
UNION ALL
SELECT telefon, 'Faqat Samarqand' FROM filial_samarqand
EXCEPT
SELECT telefon, 'Faqat Samarqand' FROM filial_toshkent
UNION ALL
SELECT telefon, 'Umumiy Ikkalasida' FROM (
    SELECT telefon FROM filial_toshkent INTERSECT SELECT telefon FROM filial_samarqand
) s;""",
        "To'liq relyatsion tahlil: mijozlarning hududiy taqsimoti Venn diagrammasi qismlariga ajratiladi.",
        """    telefon     |      holat      
----------------+-----------------
 +998902223344  | Faqat Toshkent
 +998903334455  | Faqat Samarqand
 +998901112233  | Umumiy Ikkalasida
(3 rows)"""
    ),
    (
        529,
        "UNION natijasiga GROUP BY qo'llash",
        "Barcha manbalardan tushgan daromadlarni manbalar kesimida umumlashtirish.",
        """SELECT manba, SUM(summa) AS jami_tushum
FROM (
    SELECT 'Do''kon' AS manba, 500000 AS summa
    UNION ALL
    SELECT 'Sayt' AS manba, 700000 AS summa
    UNION ALL
    SELECT 'Do''kon' AS manba, 300000 AS summa
) s
GROUP BY manba;""",
        "Birlashgan to'plam ustida guruhlash to'liq qo'llab-quvvatlanadi.",
        """ manba  | jami_tushum 
--------+-------------
 Do'kon |      800000
 Sayt   |      700000
(2 rows)"""
    ),
    (
        530,
        "To'plam amallari ijro rejasi: HashSetOp vs Append",
        "EXPLAIN orqali UNION ALL (Append) va UNION (Unique Hash) rejalarini taqqoslang.",
        """EXPLAIN SELECT telefon FROM filial_toshkent UNION ALL SELECT telefon FROM filial_samarqand;""",
        "UNION ALL rejasida shunchaki 'Append' operatori ko'rinadi (hech qanday xotira sarflamaydi). Oddiy UNION bo'lsa 'HashAggregate' yoki 'Unique' operatori qo'shiladi.",
        """                                  QUERY PLAN                                  
------------------------------------------------------------------------------
 Append  (cost=0.00..2.10 rows=4 width=32)
   ->  Seq Scan on filial_toshkent  (cost=0.00..1.02 rows=2 width=32)
   ->  Seq Scan on filial_samarqand  (cost=0.00..1.04 rows=2 width=32)
(3 rows)"""
    ),
    (
        531,
        "UNION da doimiy ustunlar bilan shakl tenglashtirish",
        "Agar ikkinchi jadvalda ba'zi ustunlar bo'lmasa, ularning o'rniga NULL qo'yib shaklni tenglashtirish.",
        """CREATE TABLE arxiv_xaridor (id INT, ism TEXT);

SELECT id, ism, telefon FROM filial_toshkent
UNION ALL
SELECT id, ism, NULL AS telefon FROM arxiv_xaridor;""",
        "Jadvallar strukturasi turlicha bo'lganda, etishmayotgan ustunlar o'rniga `NULL AS ustun` qo'yilib relyatsion ustunlar soni tenglashtiriladi.",
        """ id | ism  |    telefon    
----+------+---------------
  1 | Ali  | +998901112233
  2 | Vali | +998902223344
(2 rows)"""
    ),
    (
        532,
        "Takrorlanishlar soni bo'yicha to'liq taqqoslash (INTERSECT ALL va EXCEPT ALL)",
        "Ombordagi tovarlar partiyasi soni qat'iy mos kelishini tekshirish.",
        """SELECT son FROM t_a INTERSECT ALL SELECT son FROM t_b;""",
        "To'plamdagi elementlar soni qat'iy inobatga olinadi.",
        """ son 
-----
   5
   5
(2 rows)"""
    ),
    (
        533,
        "INTERSECT natijasining bo'shligini tekshirish (Disjoint Sets)",
        "Ikki to'plamning umuman kesishmasligi (o'zaro mutlaqo begona ekanligi)ni aniqlash.",
        """SELECT CASE 
    WHEN COUNT(*) = 0 THEN 'To‘plamlar umuman kesishmaydi' 
    ELSE 'Kesishma mavjud' 
END AS xulosa
FROM (
    SELECT 1 AS x INTERSECT SELECT 2 AS x
) s;""",
        "Kesishma natijasi 0 bo'lsa, to'plamlar kesishtirilmaydigan (Disjoint) hisoblanadi.",
        """            xulosa             
-------------------------------
 To‘plamlar umuman kesishmaydi
(1 row)"""
    ),
    (
        534,
        "UNION da murakkab mantiqiy saralash",
        "Birlashgan ro'yxatda Toshkent mijozlari doim yuqorida, Samarqand mijozlari pastda chiqsin.",
        """SELECT 'Toshkent' AS filial, ism FROM filial_toshkent
UNION ALL
SELECT 'Samarqand', ism FROM filial_samarqand
ORDER BY CASE WHEN filial = 'Toshkent' THEN 1 ELSE 2 END, ism ASC;""",
        "ORDER BY dagi CASE ifodasi manbalar bo'yicha sun'iy ustuvorlik yaratadi.",
        """  filial   | ism  
-----------+------
 Toshkent  | Ali
 Toshkent  | Vali
 Samarqand | Ali
 Samarqand | Gani
(4 rows)"""
    ),
    (
        535,
        "INTERSECT bilan bir nechta shartlarni bir vaqtda qondirish",
        "Ham 'PostgreSQL' kursiga, ham 'Python' kursiga yozilgan talabalarni INTERSECT orqali toping.",
        """CREATE TABLE yozilishlar (talaba TEXT, kurs TEXT);
INSERT INTO yozilishlar VALUES 
('Sherzod', 'PostgreSQL'), ('Sherzod', 'Python'), ('Aziz', 'PostgreSQL');

SELECT talaba FROM yozilishlar WHERE kurs = 'PostgreSQL'
INTERSECT
SELECT talaba FROM yozilishlar WHERE kurs = 'Python';""",
        "Turli shartlarni bajargan yozuvlar kesishmasi talabaning ikkala fanda ham borligini tasdiqlaydi.",
        """ talaba  
---------
 Sherzod
(1 row)"""
    ),
    (
        536,
        "EXCEPT bilan talabaning kirmagan darslarini topish",
        "Talaba qatnashmagan fanlar ro'yxatini aniqlang.",
        """CREATE TABLE barcha_fanlar (nomi TEXT);
INSERT INTO barcha_fanlar VALUES ('PostgreSQL'), ('Python'), ('Docker');

SELECT nomi FROM barcha_fanlar
EXCEPT
SELECT kurs FROM yozilishlar WHERE talaba = 'Sherzod';""",
        "Barcha fanlar to'plamidan talaba o'qigan fanlar ayirib tashlanadi va kutilayotgan qoldiq fan (Docker) topiladi.",
        """  nomi  
--------
 Docker
(1 row)"""
    ),
    (
        537,
        "To'plam natijasida LIMIT va OFFSET",
        "Birlashgan ro'yxatning dastlabki 3 ta qatorini olish.",
        """SELECT ism FROM filial_toshkent
UNION ALL
SELECT ism FROM filial_samarqand
LIMIT 3;""",
        "LIMIT butun birlashgan oqim ustida ishlaydi.",
        """ ism  
------
 Ali
 Vali
 Gani
(3 rows)"""
    ),
    (
        538,
        "UNION ALL bilan sonlar jadvali yasash",
        "Dasturlash tilidan 1, 2, 3 sonlarini virtual jadval qilib kiritish.",
        """SELECT * FROM (VALUES (1), (2), (3)) AS sonlar(qiymat);""",
        "VALUES (...) sintaksisi bir nechta UNION ALL so'rovlarining eng ixcham va zamonaviy alternatividir.",
        """ qiymat 
--------
      1
      2
      3
(3 rows)"""
    ),
    (
        539,
        "Ko'p bosqichli EXCEPT zanjiri",
        "A to'plamdan B ni, so'ngra hosil bo'lgan natijadan C ni ayirish.",
        """SELECT 1 AS n UNION SELECT 2 UNION SELECT 3
EXCEPT
SELECT 2
EXCEPT
SELECT 3;""",
        "Ketma-ket EXCEPT amallari chapdan o'ngga qarab bajariladi va yakunda faqat 1 qoladi.",
        """ n 
---
 1
(1 row)"""
    ),
    (
        540,
        "To'plam amallari bilan ko'rinish (VIEW) yaratish",
        "Barcha filiallarning yagona birlashgan ko'rinishini VIEW orqali saqlab qo'yish.",
        """CREATE OR REPLACE VIEW v_barcha_filiallar AS
SELECT 'Toshkent' AS shahar, ism, telefon FROM filial_toshkent
UNION ALL
SELECT 'Samarqand' AS shahar, ism, telefon FROM filial_samarqand;

SELECT * FROM v_barcha_filiallar WHERE ism = 'Ali';""",
        "VIEW orqali taqsimlangan jadvallar tashqi dunyoga yagona monolit jadval kabi ko'rsatiladi.",
        """ shahar   | ism |    telefon    
-----------+-----+---------------
 Toshkent  | Ali | +998901112233
 Samarqand | Ali | +998901112233
(2 rows)"""
    ),
    (
        541,
        "To'plam amallarida avtomatik ma'lumot turlarini kengaytirish (Coercion)",
        "SMALLINT va BIGINT birlashganda natija qaysi turga aylanishini ko'rsating.",
        """SELECT 10::SMALLINT AS son
UNION ALL
SELECT 10000000000::BIGINT;""",
        "RDBMS avtomatik ravishda ma'lumot yo'qolmasligi uchun eng sig'imli turga (bu yerda BIGINT) o'tkazadi.",
        """     son     
-------------
          10
 10000000000
(2 rows)"""
    ),
    (
        542,
        "INTERSECT bilan o'zaro do'stlik (Mutual Friends) munosabatini topish",
        "Ikki foydalanuvchining umumiy do'stlarini INTERSECT orqali toping.",
        """CREATE TABLE dostlar (u_id INT, dost_id INT);
INSERT INTO dostlar VALUES (1, 10), (1, 20), (1, 30), (2, 20), (2, 30), (2, 40);

SELECT dost_id AS umumiy_dost 
FROM dostlar WHERE u_id = 1
INTERSECT
SELECT dost_id 
FROM dostlar WHERE u_id = 2;""",
        "Ijtimoiy tarmoqlarda ikki profilning umumiy do'stlari (Mutual Connections) INTERSECT bilan aniqlanadi.",
        """ umumiy_dost 
-------------
          20
          30
(2 rows)"""
    ),
    (
        543,
        "UNION ALL va GROUP BY yordamida Full Outer Join simulyatsiyasi",
        "FULL OUTER JOIN mavjud bo'lmagan ba'zi sodda ma'lumotlar bazalarida UNION ALL orqali to'liq birlashishni hosil qilish.",
        """SELECT COALESCE(t.ism, s.ism) AS ism
FROM filial_toshkent t
FULL JOIN filial_samarqand s ON t.telefon = s.telefon;""",
        "Relyatsion algebrada FULL JOIN va UNION o'zaro chambarchas bog'liqdir.",
        """ ism  
------
 Ali
 Vali
 Gani
(3 rows)"""
    ),
    (
        544,
        "EXCEPT orqali ruxsat berilgan IP manzillardan begonalarni tozalash",
        "Tizimga kirgan barcha IP lardan oq ro'yxatdagi (whitelist) IP larni ayirib shubhali manzillarni topish.",
        """CREATE TABLE kirgan_iplar (ip TEXT);
CREATE TABLE oq_royxat (ip TEXT);

INSERT INTO kirgan_iplar VALUES ('192.168.1.1'), ('10.0.0.5'), ('172.16.0.99');
INSERT INTO oq_royxat VALUES ('192.168.1.1'), ('10.0.0.5');

SELECT ip AS notanish_ip FROM kirgan_iplar
EXCEPT
SELECT ip FROM oq_royxat;""",
        "Notanish va xavfli IP manzillar bir zumda aniqlanadi.",
        """ notanish_ip  
--------------
 172.16.0.99
(1 row)"""
    ),
    (
        545,
        "Barcha to'plam amallarini bitta murakkab so'rovda qo'llash",
        "(A UNION B) EXCEPT (C INTERSECT D) kombinatsiyasi.",
        """((SELECT 1 AS n UNION SELECT 2) 
EXCEPT 
(SELECT 2 INTERSECT SELECT 2));""",
        "Murakkab diskret matematika munosabatlari to'liq ifodalanadi.",
        """ n 
---
 1
(1 row)"""
    ),
    (
        546,
        "To'plamlar birlashmasida o'rtacha qiymat hisoblash xatosi",
        "Nega o'rtacha qiymatlar alohida hisoblanib keyin o'rtachasi olinmasligini (Simpson Paradoksi) tushuntiring.",
        """-- Xato: (AVG(A) + AVG(B)) / 2
-- To'g'ri: Barcha xom qatorlar UNION ALL qilinib, keyin bitta AVG hisoblanadi:
SELECT ROUND(AVG(summa), 2) AS haqiqiy_ortacha
FROM (
    SELECT 100::NUMERIC AS summa UNION ALL
    SELECT 100 UNION ALL
    SELECT 100 UNION ALL
    SELECT 200
) umumiy;""",
        "Guruhlar hajmi har xil bo'lgani sababli, o'rtachalarning o'rtachasi xato beradi. Har doim barcha qatorlar bitta to'plamga UNION ALL qilinib umumiy AVG olinadi.",
        """ haqiqiy_ortacha 
-----------------
          125.00
(1 row)"""
    ),
    (
        547,
        "UNION orqali ma'lumotlar bazasi lug'atini (Dictionary) shakllantirish",
        "Tizimdagi barcha mavjud unikal so'zlar va toifalarni bitta ro'yxatga jamlash.",
        """SELECT ism AS kalit_soz FROM filial_toshkent
UNION
SELECT ism FROM filial_samarqand
UNION
SELECT holat FROM (SELECT 'Yangi' AS holat) h;""",
        "Turli jadvallardagi matnlar unikal lug'atga yig'iladi.",
        """ kalit_soz 
-----------
 Ali
 Gani
 Vali
 Yangi
(4 rows)"""
    ),
    (
        548,
        "EXCEPT ALL va qoldiq zaxirani hisoblash",
        "Ishlab chiqarishga kerakli xomashyo sonidan omborda borini ayirib yetishmayotgan qismlarni topish.",
        """CREATE TABLE kerak (detal TEXT);
CREATE TABLE omborda_bor (detal TEXT);

INSERT INTO kerak VALUES ('Bolt'), ('Bolt'), ('Bolt'), ('Gayka');
INSERT INTO omborda_bor VALUES ('Bolt');

SELECT detal AS yetishmayotgan_detal 
FROM kerak 
EXCEPT ALL 
SELECT detal 
FROM omborda_bor;""",
        "3 ta bolt kerak, 1 ta bor. 'EXCEPT ALL' aynan yetishmayotgan 2 ta bolt va 1 ta gaykani aniq chiqaradi.",
        """ yetishmayotgan_detal 
---------------------
 Bolt
 Bolt
 Gayka
(3 rows)"""
    ),
    (
        549,
        "To'plam amallarida xotira cheklovlari va Hash vs Sort",
        "UNION operatsiyasi xotirada katta hajm talab qilganda diskka tushishi.",
        """SELECT 'UNION orqali millionlab qatorlarni tekshirish temp_file yaratishi mumkin, UNION ALL esa deyarli xotira yemaydi' AS tahlil;""",
        "Yirik ma'lumotlar bazalarida UNION o'rniga faqat zarurat bo'lgandagina foydalanish tavsiya etiladi.",
        """                                                 tahlil                                                 
--------------------------------------------------------------------------------------------------------
 UNION orqali millionlab qatorlarni tekshirish temp_file yaratishi mumkin, UNION ALL esa deyarli xotira yemaydi
(1 row)"""
    ),
    (
        550,
        "Korporativ To'plam: Bank Replikatsiya Audit Tizimi (Data Reconciliation Engine)",
        "Asosiy tranzaksion baza (OLTP) va Zaxira hisobot bazasi (DWH) o'rtasidagi ma'lumotlarni solishtirib, qaysi tranzaksiyalar yo'qolgan yoki tafovutga uchraganini UNION, EXCEPT va INTERSECT yordamida to'liq hisobot qilib bering.",
        """CREATE TABLE oltp_tranzaksiyalar (
    tr_id BIGINT PRIMARY KEY,
    hisob_raqam VARCHAR(20),
    summa NUMERIC(15, 2),
    holat VARCHAR(20)
);

CREATE TABLE dwh_tranzaksiyalar (
    tr_id BIGINT PRIMARY KEY,
    hisob_raqam VARCHAR(20),
    summa NUMERIC(15, 2),
    holat VARCHAR(20)
);

INSERT INTO oltp_tranzaksiyalar VALUES 
(1001, '202080001', 5000000.00, 'BAJARILDI'),
(1002, '202080002', 1200000.00, 'BAJARILDI'),
(1003, '202080003', 750000.00,  'KUTILMOQDA');

INSERT INTO dwh_tranzaksiyalar VALUES 
(1001, '202080001', 5000000.00, 'BAJARILDI'), -- To'liq mos!
(1002, '202080002', 1100000.00, 'BAJARILDI'), -- Summa tafovuti!
(1004, '202080004', 3000000.00, 'BAJARILDI'); -- DWH ga adashib tushgan yetim yozuv!

WITH faqat_oltp AS (
    SELECT tr_id, hisob_raqam, summa, holat, 'Faqat OLTP da bor (DWH ga yetib bormagan)' AS tafovut_turi
    FROM (SELECT * FROM oltp_tranzaksiyalar EXCEPT SELECT * FROM dwh_tranzaksiyalar) s
),
faqat_dwh AS (
    SELECT tr_id, hisob_raqam, summa, holat, 'Faqat DWH da bor (OLTP da mavjud emas)' AS tafovut_turi
    FROM (SELECT * FROM dwh_tranzaksiyalar EXCEPT SELECT * FROM oltp_tranzaksiyalar) s
)
SELECT * FROM faqat_oltp
UNION ALL
SELECT * FROM faqat_dwh
ORDER BY tr_id, tafovut_turi;""",
        "Ushbu korporativ so'rov bank va to'lov tashkilotlarida har tun ishga tushiriluvchi Avtomatik Rekonsilyatsiya Dvigatelidir (Automated Reconciliation Engine): relyatsion to'plam ayirmasi (EXCEPT) orqali asosiy baza va replika bazadagi barcha xatoliklar, yetib bormagan tranzaksiyalar va tafovutli summalar bir millisekundda aniqlanib xavfsizlik jurnaliga yoziladi.",
        """ tr_id | hisob_raqam |   summa    |   holat    |                 tafovut_turi                 
-------+-------------+------------+------------+----------------------------------------------
  1002 | 202080002   | 1100000.00 | BAJARILDI  | Faqat DWH da bor (OLTP da mavjud emas)
  1002 | 202080002   | 1200000.00 | BAJARILDI  | Faqat OLTP da bor (DWH ga yetib bormagan)
  1003 | 202080003   |  750000.00 | KUTILMOQDA | Faqat OLTP da bor (DWH ga yetib bormagan)
  1004 | 202080004   | 3000000.00 | BAJARILDI  | Faqat DWH da bor (OLTP da mavjud emas)
(4 rows)"""
    )
]

formatted = [format_task(*item) for item in set_data]
save_file("sql_11_toplam_amallari_set_operations.md", formatted)
