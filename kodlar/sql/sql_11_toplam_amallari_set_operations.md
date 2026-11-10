# 501-Topshiriq: To'plamlar birlashmasi: UNION asoslari (Dublikatlarni yo'qotish)
## Topshiriq sharti:
Toshkent va Samarqand filiallari mijozlarining telefon raqamlarini takrorlanishlarsiz birlashtiring.

## Yechim (SQL kodi):
```sql
CREATE TABLE filial_toshkent (id INT, ism TEXT, telefon VARCHAR(20));
CREATE TABLE filial_samarqand (id INT, ism TEXT, telefon VARCHAR(20));

INSERT INTO filial_toshkent VALUES 
(1, 'Ali', '+998901112233'), 
(2, 'Vali', '+998902223344');

INSERT INTO filial_samarqand VALUES 
(10, 'Gani', '+998903334455'), 
(11, 'Ali', '+998901112233'); -- Ikkala filialda ham bor mijoz!

SELECT telefon FROM filial_toshkent
UNION
SELECT telefon FROM filial_samarqand;
```

## Tushuntirish va Mantiq:
'UNION' ikkita SELECT natijasini birlashtiradi va takrorlanuvchi qatorlarni yo'qotish uchun natijani xotirada saralaydi (yoki hash jadval tuzadi). 'Ali' ning telefon raqami ikkala filialda bo'lsa-da, natijada faqat 1 marta chiqadi.

## Ishlash natijasi:
```text
telefon     
----------------
 +998901112233
 +998902223344
 +998903334455
(3 rows)
```


# 502-Topshiriq: Tezkor birlashma: UNION ALL (Dublikatlarni saqlab qolish)
## Topshiriq sharti:
Barcha filiallarning tranzaksiyalarini hech qanday saralashsiz tezkorlik bilan birlashtiring.

## Yechim (SQL kodi):
```sql
SELECT ism, telefon FROM filial_toshkent
UNION ALL
SELECT ism, telefon FROM filial_samarqand;
```

## Tushuntirish va Mantiq:
'UNION ALL' dublikatlarni tekshirmaydi va saralamaydi, shunchaki ikkinchi natijani birinchisining ketiga ulaydi (Append operatori). Bu UNION ga qaraganda ancha tez va tejamkor ishlaydi.

## Ishlash natijasi:
```text
ism  |    telefon    
------+---------------
 Ali  | +998901112233
 Vali | +998902223344
 Gani | +998903334455
 Ali  | +998901112233
(4 rows)
```


# 503-Topshiriq: UNION vs UNION ALL: Unumdorlik va qachon qaysi biri ishlatiladi?
## Topshiriq sharti:
Optimizator darajasida UNION va UNION ALL farqini ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT 'Agar dublikatlar bo‘lmasligi aniq bo‘lsa yoki dublikatlar kerak bo‘lsa, DOIMO UNION ALL ishlatilishi shart' AS qoida;
```

## Tushuntirish va Mantiq:
UNION barcha qatorlarni xotirada tekshirishi (Unique Sort) tufayli millionlab qatorlarda sekinlashuvga olib keladi. UNION ALL esa to'g'ridan-to'g'ri oqim (stream) orqali yuboriladi.

## Ishlash natijasi:
```text
qoida                                                 
-------------------------------------------------------------------------------------------------------
 Agar dublikatlar bo‘lmasligi aniq bo‘lsa yoki dublikatlar kerak bo‘lsa, DOIMO UNION ALL ishlatilishi shart
(1 row)
```


# 504-Topshiriq: To'plamlar kesishmasi: INTERSECT
## Topshiriq sharti:
Bir vaqtning o'zida ham Toshkent, ham Samarqand filialida ro'yxatdan o'tgan umumiy mijozlarni toping.

## Yechim (SQL kodi):
```sql
SELECT telefon FROM filial_toshkent
INTERSECT
SELECT telefon FROM filial_samarqand;
```

## Tushuntirish va Mantiq:
'INTERSECT' ikkala to'plamda ham mavjud bo'lgan umumiy elementlarni (kesishma ∩) qaytaradi va dublikatlarni olib tashlaydi.

## Ishlash natijasi:
```text
telefon     
----------------
 +998901112233
(1 row)
```


# 505-Topshiriq: Dublikatlar sonini inobatga oluvchi kesishma: INTERSECT ALL
## Topshiriq sharti:
Agar qator 1-jadvalda 3 marta, 2-jadvalda 2 marta bo'lsa, INTERSECT ALL nechta qaytarishini ko'ring.

## Yechim (SQL kodi):
```sql
CREATE TABLE t_a (son INT);
CREATE TABLE t_b (son INT);
INSERT INTO t_a VALUES (5), (5), (5);
INSERT INTO t_b VALUES (5), (5);

SELECT son FROM t_a
INTERSECT ALL
SELECT son FROM t_b;
```

## Tushuntirish va Mantiq:
'INTERSECT ALL' har ikkala to'plamdagi takrorlanishlar sonining minimalini (min(3, 2) = 2) qaytaradi. Natijada aynan 2 ta '5' chiqadi.

## Ishlash natijasi:
```text
son 
-----
   5
   5
(2 rows)
```


# 506-Topshiriq: To'plamlar ayirmasi: EXCEPT (MINUS)
## Topshiriq sharti:
Faqat Toshkent filialiga tegishli bo'lgan (Samarqand filialida umuman yo'q) mijozlarni toping.

## Yechim (SQL kodi):
```sql
SELECT telefon FROM filial_toshkent
EXCEPT
SELECT telefon FROM filial_samarqand;
```

## Tushuntirish va Mantiq:
'EXCEPT' (ba'zi tizimlarda MINUS) birinchi to'plamdan ikkinchi to'plamda mavjud barcha elementlarni chiqarib tashlaydi (A \ B).

## Ishlash natijasi:
```text
telefon     
----------------
 +998902223344
(1 row)
```


# 507-Topshiriq: Dublikatlar soni bilan ayirma: EXCEPT ALL
## Topshiriq sharti:
1-jadvaldagi takrorlanishlar sonidan 2-jadvaldagi takrorlanishlar sonini ayirib qolganini ko'rsatish.

## Yechim (SQL kodi):
```sql
SELECT son FROM t_a
EXCEPT ALL
SELECT son FROM t_b;
```

## Tushuntirish va Mantiq:
'EXCEPT ALL' birinchi to'plamdagi sonlar miqdoridan ikkinchi to'plamdagi sonlar miqdorini ayiradi: 3 - 2 = 1. Natijada aynan 1 ta '5' qoladi.

## Ishlash natijasi:
```text
son 
-----
   5
(1 row)
```


# 508-Topshiriq: Ustunlar mosligi qoidasi (Number of columns mismatch)
## Topshiriq sharti:
Ikkala SELECT dagi ustunlar soni teng bo'lmasa nima bo'lishini ko'ring.

## Yechim (SQL kodi):
```sql
-- Xato so'rov:
-- SELECT id, ism FROM filial_toshkent UNION SELECT id FROM filial_samarqand;
SELECT 'To‘plam amallarida barcha SELECT larning ustunlar soni bir xil bo‘lishi shart' AS talab;
```

## Tushuntirish va Mantiq:
Relyatsion to'plam amallarida har bir SELECT aynan bir xil miqdordagi ustunlarni qaytarishi shart, aks holda 'each UNION query must have the same number of columns' xatoligi yuzaga keladi.

## Ishlash natijasi:
```text
talab                                  
------------------------------------------------------------------------
 To‘plam amallarida barcha SELECT larning ustunlar soni bir xil bo‘lishi shart
(1 row)
```


# 509-Topshiriq: Ustunlar ma'lumot turlari mosligi (Type compatibility)
## Topshiriq sharti:
Son va matn ustunlarini UNION qilishda tur o'zgartirish (Type Casting).

## Yechim (SQL kodi):
```sql
SELECT id::TEXT AS identifikator FROM filial_toshkent
UNION ALL
SELECT telefon AS identifikator FROM filial_samarqand;
```

## Tushuntirish va Mantiq:
Barcha mos ustunlarning ma'lumot turlari bir-biriga mos kelishi yoki umumiy turga konvertatsiya qilinishi (masalan, ::TEXT) shart.

## Ishlash natijasi:
```text
identifikator  
----------------
 1
 2
 +998903334455
 +998901112233
(4 rows)
```


# 510-Topshiriq: Natijaviy ustun nomlari birinchi SELECT dan olinishi
## Topshiriq sharti:
Ikkinchi SELECT da boshqa nom berilgan bo'lsa ham birinchi SELECT nomi ustun bo'lishini ko'ring.

## Yechim (SQL kodi):
```sql
SELECT ism AS asosiy_nom FROM filial_toshkent
UNION ALL
SELECT ism AS ikkinchi_nom FROM filial_samarqand;
```

## Tushuntirish va Mantiq:
Natijaviy virtual jadval ustunlari har doim eng birinchi SELECT bandidagi sarlavha va taxalluslar (aliases) asosida shakllanadi.

## Ishlash natijasi:
```text
asosiy_nom 
------------
 Ali
 Vali
 Gani
 Ali
(4 rows)
```


# 511-Topshiriq: To'plam amallarida tartiblash qoidasi (ORDER BY joylashuvi)
## Topshiriq sharti:
ORDER BY buyrug'i butun to'plamning eng oxirida yozilishi shartligi.

## Yechim (SQL kodi):
```sql
SELECT ism, telefon FROM filial_toshkent
UNION ALL
SELECT ism, telefon FROM filial_samarqand
ORDER BY ism ASC;
```

## Tushuntirish va Mantiq:
ORDER BY butun birlashgan to'plamga nisbatan qo'llaniladi. Agar alohida ichki SELECT ni tartiblash kerak bo'lsa, u qavs ichiga olinishi va LIMIT bilan birga ishlatilishi lozim.

## Ishlash natijasi:
```text
ism  |    telefon    
------+---------------
 Ali  | +998901112233
 Ali  | +998901112233
 Gani | +998903334455
 Vali | +998902223344
(4 rows)
```


# 512-Topshiriq: Qavslar bilan alohida LIMIT va ORDER BY berish
## Topshiriq sharti:
Toshkent filialidan top-1 va Samarqand filialidan top-1 mijozni olib birlashtiring.

## Yechim (SQL kodi):
```sql
(SELECT ism FROM filial_toshkent ORDER BY id ASC LIMIT 1)
UNION ALL
(SELECT ism FROM filial_samarqand ORDER BY id ASC LIMIT 1);
```

## Tushuntirish va Mantiq:
Qavslar `(SELECT ...)` har bir so'rovning o'ziga xos shaxsiy ORDER BY va LIMIT ini bajarishga imkon beradi, so'ngra hosil bo'lgan ikkita qator birlashtiriladi.

## Ishlash natijasi:
```text
ism  
------
 Ali
 Gani
(2 rows)
```


# 513-Topshiriq: Jadvallar o'rtasidagi to'liq simmetrik farq (Symmetric Difference)
## Topshiriq sharti:
Ikkala jadvalda bir-biriga mos kelmaydigan barcha farqlarni (A \ B) U (B \ A) toping.

## Yechim (SQL kodi):
```sql
(SELECT telefon FROM filial_toshkent EXCEPT SELECT telefon FROM filial_samarqand)
UNION ALL
(SELECT telefon FROM filial_samarqand EXCEPT SELECT telefon FROM filial_toshkent);
```

## Tushuntirish va Mantiq:
Simmetrik farq jadvallarni taqqoslashda va nomuvofiqliklarni topishda eng ishonchli relyatsion formuladir.

## Ishlash natijasi:
```text
telefon     
----------------
 +998902223344
 +998903334455
(2 rows)
```


# 514-Topshiriq: Jadvallarning 100% aynan bir xilligini tekshirish (Data Reconciliation)
## Topshiriq sharti:
Ikkita jadval o'zaro to'liq mos keladimi yoki yo'qligini tekshiruvchi so'rov yozing.

## Yechim (SQL kodi):
```sql
SELECT CASE 
    WHEN COUNT(*) = 0 THEN '✅ Jadvallar to‘liq bir xil'
    ELSE '❌ Jadvallarda tafovut mavjud'
END AS tekshiruv_natijasi
FROM (
    (SELECT * FROM filial_toshkent EXCEPT SELECT * FROM filial_samarqand)
    UNION ALL
    (SELECT * FROM filial_samarqand EXCEPT SELECT * FROM filial_toshkent)
) farqlar;
```

## Tushuntirish va Mantiq:
Agar simmetrik ayirma bo'sh bo'lsa (COUNT=0), demak ikki jadval ma'lumotlari 100% bir-birini takrorlaydi. Bank tizimlarida kun yakuni (End of Day reconciliation) shunday tekshiriladi.

## Ishlash natijasi:
```text
tekshiruv_natijasi      
-----------------------------
 ❌ Jadvallarda tafovut mavjud
(1 row)
```


# 515-Topshiriq: UNION ALL bilan manba jadvalni ko'rsatish (Provenance tracking)
## Topshiriq sharti:
Qator qaysi filialdan kelganini bilish uchun qo'shimcha statik ustun qo'shing.

## Yechim (SQL kodi):
```sql
SELECT 'Toshkent' AS filial, ism, telefon FROM filial_toshkent
UNION ALL
SELECT 'Samarqand' AS filial, ism, telefon FROM filial_samarqand;
```

## Tushuntirish va Mantiq:
Statik literal (`'Toshkent' AS filial`) qo'shish orqali birlashgan ma'lumotlarning manbasi (data provenance) aniq saqlanadi.

## Ishlash natijasi:
```text
filial   | ism  |    telefon    
-----------+------+---------------
 Toshkent  | Ali  | +998901112233
 Toshkent  | Vali | +998902223344
 Samarqand | Gani | +998903334455
 Samarqand | Ali  | +998901112233
(4 rows)
```


# 516-Topshiriq: To'plam amallarining ustuvorligi (Precedence)
## Topshiriq sharti:
UNION va INTERSECT birga kelganda qaysi biri oldin bajarilishini ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT 1 AS n
UNION
SELECT 2
INTERSECT
SELECT 2;
```

## Tushuntirish va Mantiq:
SQL standartida 'INTERSECT' operatorining ustuvorligi 'UNION' va 'EXCEPT' ga qaraganda YUQORI (ko'paytirish qo'shishdan oldin kelgani kabi). Shu bois avval `2 INTERSECT 2` bajariladi, so'ng `1 UNION 2` bo'ladi.

## Ishlash natijasi:
```text
n 
---
 1
 2
(2 rows)
```


# 517-Topshiriq: Qavslar orqali ustuvorlikni o'zgartirish
## Topshiriq sharti:
Oldin UNION, keyin INTERSECT bajarilishi uchun qavslardan foydalaning.

## Yechim (SQL kodi):
```sql
(SELECT 1 AS n UNION SELECT 2)
INTERSECT
SELECT 2;
```

## Tushuntirish va Mantiq:
Qavslar ustuvorlikni qat'iy belgilaydi. Avval 1 va 2 birlashadi, keyin 2 bilan kesishib faqat 2 qoladi.

## Ishlash natijasi:
```text
n 
---
 2
(1 row)
```


# 518-Topshiriq: NULL qiymatlarning to'plam amallaridagi xulqi
## Topshiriq sharti:
UNION va INTERSECT da NULL qiymatlar bir-biriga teng deb hisoblanadimi?

## Yechim (SQL kodi):
```sql
SELECT NULL AS qiymat
UNION
SELECT NULL;
```

## Tushuntirish va Mantiq:
To'plam amallarida (UNION, INTERSECT, EXCEPT) NULL qiymatlar boshqa barcha taqqoslashlardan farqli ravishda 'teng' (NOT DISTINCT) deb baholanadi. Shu bois ikkita NULL birlashganda faqat 1 ta NULL qoladi.

## Ishlash natijasi:
```text
qiymat 
--------
 NULL
(1 row)
```


# 519-Topshiriq: INTERSECT o'rniga INNER JOIN ishlatish
## Topshiriq sharti:
INTERSECT ning JOIN orqali ekvivalenti va unumdorlik farqi.

## Yechim (SQL kodi):
```sql
SELECT DISTINCT t.telefon 
FROM filial_toshkent t
JOIN filial_samarqand s ON t.telefon = s.telefon;
```

## Tushuntirish va Mantiq:
INTERSECT ikkala tomonni to'liq saralaydi. Agar telefon ustunida B-Tree indeks bo'lsa, INNER JOIN ancha tezroq ishlaydi.

## Ishlash natijasi:
```text
telefon     
----------------
 +998901112233
(1 row)
```


# 520-Topshiriq: EXCEPT o'rniga NOT EXISTS ishlatish
## Topshiriq sharti:
EXCEPT operatsiyasini NOT EXISTS orqali tezlashtirish.

## Yechim (SQL kodi):
```sql
SELECT DISTINCT t.telefon 
FROM filial_toshkent t
WHERE NOT EXISTS (
    SELECT 1 FROM filial_samarqand s WHERE s.telefon = t.telefon
);
```

## Tushuntirish va Mantiq:
NOT EXISTS qidiruvni indeks orqali Anti-Join bilan amalga oshiradi va EXCEPT ga qaraganda katta jadvallarda kamroq xotira sarflaydi.

## Ishlash natijasi:
```text
telefon     
----------------
 +998902223344
(1 row)
```


# 521-Topshiriq: To'plam natijasini CTE ichiga o'rash
## Topshiriq sharti:
Birlashgan mijozlar ro'yxati ustida keyingi filtrlash va saralashni bajarish.

## Yechim (SQL kodi):
```sql
WITH barcha_mijozlar AS (
    SELECT ism, telefon FROM filial_toshkent
    UNION
    SELECT ism, telefon FROM filial_samarqand
)
SELECT ism, telefon 
FROM barcha_mijozlar 
WHERE ism LIKE 'A%'
ORDER BY telefon DESC;
```

## Tushuntirish va Mantiq:
To'plam amallari natijasi CTE ichiga olinib, uning ustida oddiy jadvallardagi kabi WHERE va ORDER BY qo'llanadi.

## Ishlash natijasi:
```text
ism |    telefon    
-----+---------------
 Ali | +998901112233
(1 row)
```


# 522-Topshiriq: To'plam amallarida umumiy agregatsiya (COUNT)
## Topshiriq sharti:
Barcha filiallarning takrorlanmas noyob mijozlari sonini hisoblang.

## Yechim (SQL kodi):
```sql
SELECT COUNT(*) AS jami_noyob_mijozlar 
FROM (
    SELECT telefon FROM filial_toshkent
    UNION
    SELECT telefon FROM filial_samarqand
) umumiy;
```

## Tushuntirish va Mantiq:
UNION qilgandan so'ng tashqi COUNT(*) aniq noyob mijozlar sonini chiqaradi.

## Ishlash natijasi:
```text
jami_noyob_mijozlar 
----------------------
                    3
(1 row)
```


# 523-Topshiriq: Bir nechta SELECT larni ketma-ket UNION qilish
## Topshiriq sharti:
Uchta turli hudud (Toshkent, Samarqand, Farg'ona) ma'lumotlarini birlashtirish.

## Yechim (SQL kodi):
```sql
SELECT 'Toshkent' AS shahar UNION ALL
SELECT 'Samarqand' UNION ALL
SELECT 'Farg‘ona';
```

## Tushuntirish va Mantiq:
Zanjirda istalgancha ko'p SELECT operatorlari ketma-ket birlashishi mumkin.

## Ishlash natijasi:
```text
shahar   
------------
 Toshkent
 Samarqand
 Farg‘ona
(3 rows)
```


# 524-Topshiriq: Statik ro'yxat (Mock data) hosil qilish: UNION ALL yordamida
## Topshiriq sharti:
Jadval ochmasdan xotirada virtual ma'lumotlar to'plamini hosil qiling.

## Yechim (SQL kodi):
```sql
SELECT 1 AS kod, 'Yangi' AS holat UNION ALL
SELECT 2, 'Jarayonda' UNION ALL
SELECT 3, 'Bajarildi';
```

## Tushuntirish va Mantiq:
Testlar va kichik ma'lumotnomalarni tezkor ifodalashda juda qulay.

## Ishlash natijasi:
```text
kod |   holat   
-----+-----------
   1 | Yangi
   2 | Jarayonda
   3 | Bajarildi
(3 rows)
```


# 525-Topshiriq: To'plamlar bilan qidiruv: Google Search uslubidagi natijalarni birlashtirish
## Topshiriq sharti:
Bir vaqtning o'zida ham maqolalar sarlavhasi, ham mualliflar ismi bo'yicha qidirib natijalarni bitta ro'yxatda chiqarish.

## Yechim (SQL kodi):
```sql
CREATE TABLE blog_m (id INT, sarlavha TEXT);
CREATE TABLE user_m (id INT, ism TEXT);
INSERT INTO blog_m VALUES (1, 'SQL optimallashtirish');
INSERT INTO user_m VALUES (10, 'Ali Dasturchi');

SELECT 'Maqola' AS tur, sarlavha AS matn FROM blog_m WHERE sarlavha ILIKE '%sql%'
UNION ALL
SELECT 'Muallif' AS tur, ism AS matn FROM user_m WHERE ism ILIKE '%ali%';
```

## Tushuntirish va Mantiq:
Universal global qidiruv tizimlarining arxitekturasi turli xil jadvallardagi mosliklarni UNION ALL orqali yagona qidiruv ro'yxatiga yig'adi.

## Ishlash natijasi:
```text
tur   |         matn          
---------+-----------------------
 Maqola  | SQL optimallashtirish
 Muallif | Ali Dasturchi
(2 rows)
```


# 526-Topshiriq: To'plam amallarida turli ustun tiplari xatosi
## Topshiriq sharti:
VARCHAR va INTEGER ustunlari to'g'ridan-to'g'ri UNION bo'lmasligini ko'ring.

## Yechim (SQL kodi):
```sql
-- Xato: SELECT 123 UNION SELECT 'matn';
SELECT 'PostgreSQL tiplar mos bo‘lmasa avtomatik o‘tkazmaydi, aniq CAST talab qiladi' AS xulosa;
```

## Tushuntirish va Mantiq:
MySQL ba'zan tiplarni yashirin o'girishi mumkin, ammo qat'iy standartlarga ega PostgreSQL 'UNION types integer and text cannot be matched' xatosini qaytaradi.

## Ishlash natijasi:
```text
xulosa                                                
------------------------------------------------------------------------------------------------------
 PostgreSQL tiplar mos bo‘lmasa avtomatik o‘tkazmaydi, aniq CAST talab qiladi
(1 row)
```


# 527-Topshiriq: EXCEPT yordamida ruxsat berilmagan xatti-harakatlarni aniqlash
## Topshiriq sharti:
Xavfsizlik tizimida: qilingan amallar ichidan ruxsat etilgan amallar ro'yxatida bo'lmaganlarini toping.

## Yechim (SQL kodi):
```sql
CREATE TABLE bajarilgan_amallar (amal TEXT);
CREATE TABLE ruxsatlar (amal TEXT);

INSERT INTO bajarilgan_amallar VALUES ('LOGIN'), ('VIEW_REPORT'), ('DELETE_DATABASE');
INSERT INTO ruxsatlar VALUES ('LOGIN'), ('VIEW_REPORT');

SELECT amal AS qonunbuzarlik 
FROM bajarilgan_amallar
EXCEPT
SELECT amal 
FROM ruxsatlar;
```

## Tushuntirish va Mantiq:
Audit va xavfsizlik nazoratida noqonuniy amallarni topishning eng ishonchli usuli.

## Ishlash natijasi:
```text
qonunbuzarlik  
-----------------
 DELETE_DATABASE
(1 row)
```


# 528-Topshiriq: Venn diagrammasi: Faqat A, Faqat B va Ikkalasida ham bor qismlar
## Topshiriq sharti:
Ikki to'plamning barcha mantiqiy sohalarini alohida belgilab chiqaring.

## Yechim (SQL kodi):
```sql
SELECT telefon, 'Faqat Toshkent' AS holat FROM filial_toshkent
EXCEPT
SELECT telefon, 'Faqat Toshkent' FROM filial_samarqand
UNION ALL
SELECT telefon, 'Faqat Samarqand' FROM filial_samarqand
EXCEPT
SELECT telefon, 'Faqat Samarqand' FROM filial_toshkent
UNION ALL
SELECT telefon, 'Umumiy Ikkalasida' FROM (
    SELECT telefon FROM filial_toshkent INTERSECT SELECT telefon FROM filial_samarqand
) s;
```

## Tushuntirish va Mantiq:
To'liq relyatsion tahlil: mijozlarning hududiy taqsimoti Venn diagrammasi qismlariga ajratiladi.

## Ishlash natijasi:
```text
telefon     |      holat      
----------------+-----------------
 +998902223344  | Faqat Toshkent
 +998903334455  | Faqat Samarqand
 +998901112233  | Umumiy Ikkalasida
(3 rows)
```


# 529-Topshiriq: UNION natijasiga GROUP BY qo'llash
## Topshiriq sharti:
Barcha manbalardan tushgan daromadlarni manbalar kesimida umumlashtirish.

## Yechim (SQL kodi):
```sql
SELECT manba, SUM(summa) AS jami_tushum
FROM (
    SELECT 'Do''kon' AS manba, 500000 AS summa
    UNION ALL
    SELECT 'Sayt' AS manba, 700000 AS summa
    UNION ALL
    SELECT 'Do''kon' AS manba, 300000 AS summa
) s
GROUP BY manba;
```

## Tushuntirish va Mantiq:
Birlashgan to'plam ustida guruhlash to'liq qo'llab-quvvatlanadi.

## Ishlash natijasi:
```text
manba  | jami_tushum 
--------+-------------
 Do'kon |      800000
 Sayt   |      700000
(2 rows)
```


# 530-Topshiriq: To'plam amallari ijro rejasi: HashSetOp vs Append
## Topshiriq sharti:
EXPLAIN orqali UNION ALL (Append) va UNION (Unique Hash) rejalarini taqqoslang.

## Yechim (SQL kodi):
```sql
EXPLAIN SELECT telefon FROM filial_toshkent UNION ALL SELECT telefon FROM filial_samarqand;
```

## Tushuntirish va Mantiq:
UNION ALL rejasida shunchaki 'Append' operatori ko'rinadi (hech qanday xotira sarflamaydi). Oddiy UNION bo'lsa 'HashAggregate' yoki 'Unique' operatori qo'shiladi.

## Ishlash natijasi:
```text
QUERY PLAN                                  
------------------------------------------------------------------------------
 Append  (cost=0.00..2.10 rows=4 width=32)
   ->  Seq Scan on filial_toshkent  (cost=0.00..1.02 rows=2 width=32)
   ->  Seq Scan on filial_samarqand  (cost=0.00..1.04 rows=2 width=32)
(3 rows)
```


# 531-Topshiriq: UNION da doimiy ustunlar bilan shakl tenglashtirish
## Topshiriq sharti:
Agar ikkinchi jadvalda ba'zi ustunlar bo'lmasa, ularning o'rniga NULL qo'yib shaklni tenglashtirish.

## Yechim (SQL kodi):
```sql
CREATE TABLE arxiv_xaridor (id INT, ism TEXT);

SELECT id, ism, telefon FROM filial_toshkent
UNION ALL
SELECT id, ism, NULL AS telefon FROM arxiv_xaridor;
```

## Tushuntirish va Mantiq:
Jadvallar strukturasi turlicha bo'lganda, etishmayotgan ustunlar o'rniga `NULL AS ustun` qo'yilib relyatsion ustunlar soni tenglashtiriladi.

## Ishlash natijasi:
```text
id | ism  |    telefon    
----+------+---------------
  1 | Ali  | +998901112233
  2 | Vali | +998902223344
(2 rows)
```


# 532-Topshiriq: Takrorlanishlar soni bo'yicha to'liq taqqoslash (INTERSECT ALL va EXCEPT ALL)
## Topshiriq sharti:
Ombordagi tovarlar partiyasi soni qat'iy mos kelishini tekshirish.

## Yechim (SQL kodi):
```sql
SELECT son FROM t_a INTERSECT ALL SELECT son FROM t_b;
```

## Tushuntirish va Mantiq:
To'plamdagi elementlar soni qat'iy inobatga olinadi.

## Ishlash natijasi:
```text
son 
-----
   5
   5
(2 rows)
```


# 533-Topshiriq: INTERSECT natijasining bo'shligini tekshirish (Disjoint Sets)
## Topshiriq sharti:
Ikki to'plamning umuman kesishmasligi (o'zaro mutlaqo begona ekanligi)ni aniqlash.

## Yechim (SQL kodi):
```sql
SELECT CASE 
    WHEN COUNT(*) = 0 THEN 'To‘plamlar umuman kesishmaydi' 
    ELSE 'Kesishma mavjud' 
END AS xulosa
FROM (
    SELECT 1 AS x INTERSECT SELECT 2 AS x
) s;
```

## Tushuntirish va Mantiq:
Kesishma natijasi 0 bo'lsa, to'plamlar kesishtirilmaydigan (Disjoint) hisoblanadi.

## Ishlash natijasi:
```text
xulosa             
-------------------------------
 To‘plamlar umuman kesishmaydi
(1 row)
```


# 534-Topshiriq: UNION da murakkab mantiqiy saralash
## Topshiriq sharti:
Birlashgan ro'yxatda Toshkent mijozlari doim yuqorida, Samarqand mijozlari pastda chiqsin.

## Yechim (SQL kodi):
```sql
SELECT 'Toshkent' AS filial, ism FROM filial_toshkent
UNION ALL
SELECT 'Samarqand', ism FROM filial_samarqand
ORDER BY CASE WHEN filial = 'Toshkent' THEN 1 ELSE 2 END, ism ASC;
```

## Tushuntirish va Mantiq:
ORDER BY dagi CASE ifodasi manbalar bo'yicha sun'iy ustuvorlik yaratadi.

## Ishlash natijasi:
```text
filial   | ism  
-----------+------
 Toshkent  | Ali
 Toshkent  | Vali
 Samarqand | Ali
 Samarqand | Gani
(4 rows)
```


# 535-Topshiriq: INTERSECT bilan bir nechta shartlarni bir vaqtda qondirish
## Topshiriq sharti:
Ham 'PostgreSQL' kursiga, ham 'Python' kursiga yozilgan talabalarni INTERSECT orqali toping.

## Yechim (SQL kodi):
```sql
CREATE TABLE yozilishlar (talaba TEXT, kurs TEXT);
INSERT INTO yozilishlar VALUES 
('Sherzod', 'PostgreSQL'), ('Sherzod', 'Python'), ('Aziz', 'PostgreSQL');

SELECT talaba FROM yozilishlar WHERE kurs = 'PostgreSQL'
INTERSECT
SELECT talaba FROM yozilishlar WHERE kurs = 'Python';
```

## Tushuntirish va Mantiq:
Turli shartlarni bajargan yozuvlar kesishmasi talabaning ikkala fanda ham borligini tasdiqlaydi.

## Ishlash natijasi:
```text
talaba  
---------
 Sherzod
(1 row)
```


# 536-Topshiriq: EXCEPT bilan talabaning kirmagan darslarini topish
## Topshiriq sharti:
Talaba qatnashmagan fanlar ro'yxatini aniqlang.

## Yechim (SQL kodi):
```sql
CREATE TABLE barcha_fanlar (nomi TEXT);
INSERT INTO barcha_fanlar VALUES ('PostgreSQL'), ('Python'), ('Docker');

SELECT nomi FROM barcha_fanlar
EXCEPT
SELECT kurs FROM yozilishlar WHERE talaba = 'Sherzod';
```

## Tushuntirish va Mantiq:
Barcha fanlar to'plamidan talaba o'qigan fanlar ayirib tashlanadi va kutilayotgan qoldiq fan (Docker) topiladi.

## Ishlash natijasi:
```text
nomi  
--------
 Docker
(1 row)
```


# 537-Topshiriq: To'plam natijasida LIMIT va OFFSET
## Topshiriq sharti:
Birlashgan ro'yxatning dastlabki 3 ta qatorini olish.

## Yechim (SQL kodi):
```sql
SELECT ism FROM filial_toshkent
UNION ALL
SELECT ism FROM filial_samarqand
LIMIT 3;
```

## Tushuntirish va Mantiq:
LIMIT butun birlashgan oqim ustida ishlaydi.

## Ishlash natijasi:
```text
ism  
------
 Ali
 Vali
 Gani
(3 rows)
```


# 538-Topshiriq: UNION ALL bilan sonlar jadvali yasash
## Topshiriq sharti:
Dasturlash tilidan 1, 2, 3 sonlarini virtual jadval qilib kiritish.

## Yechim (SQL kodi):
```sql
SELECT * FROM (VALUES (1), (2), (3)) AS sonlar(qiymat);
```

## Tushuntirish va Mantiq:
VALUES (...) sintaksisi bir nechta UNION ALL so'rovlarining eng ixcham va zamonaviy alternatividir.

## Ishlash natijasi:
```text
qiymat 
--------
      1
      2
      3
(3 rows)
```


# 539-Topshiriq: Ko'p bosqichli EXCEPT zanjiri
## Topshiriq sharti:
A to'plamdan B ni, so'ngra hosil bo'lgan natijadan C ni ayirish.

## Yechim (SQL kodi):
```sql
SELECT 1 AS n UNION SELECT 2 UNION SELECT 3
EXCEPT
SELECT 2
EXCEPT
SELECT 3;
```

## Tushuntirish va Mantiq:
Ketma-ket EXCEPT amallari chapdan o'ngga qarab bajariladi va yakunda faqat 1 qoladi.

## Ishlash natijasi:
```text
n 
---
 1
(1 row)
```


# 540-Topshiriq: To'plam amallari bilan ko'rinish (VIEW) yaratish
## Topshiriq sharti:
Barcha filiallarning yagona birlashgan ko'rinishini VIEW orqali saqlab qo'yish.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE VIEW v_barcha_filiallar AS
SELECT 'Toshkent' AS shahar, ism, telefon FROM filial_toshkent
UNION ALL
SELECT 'Samarqand' AS shahar, ism, telefon FROM filial_samarqand;

SELECT * FROM v_barcha_filiallar WHERE ism = 'Ali';
```

## Tushuntirish va Mantiq:
VIEW orqali taqsimlangan jadvallar tashqi dunyoga yagona monolit jadval kabi ko'rsatiladi.

## Ishlash natijasi:
```text
shahar   | ism |    telefon    
-----------+-----+---------------
 Toshkent  | Ali | +998901112233
 Samarqand | Ali | +998901112233
(2 rows)
```


# 541-Topshiriq: To'plam amallarida avtomatik ma'lumot turlarini kengaytirish (Coercion)
## Topshiriq sharti:
SMALLINT va BIGINT birlashganda natija qaysi turga aylanishini ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT 10::SMALLINT AS son
UNION ALL
SELECT 10000000000::BIGINT;
```

## Tushuntirish va Mantiq:
RDBMS avtomatik ravishda ma'lumot yo'qolmasligi uchun eng sig'imli turga (bu yerda BIGINT) o'tkazadi.

## Ishlash natijasi:
```text
son     
-------------
          10
 10000000000
(2 rows)
```


# 542-Topshiriq: INTERSECT bilan o'zaro do'stlik (Mutual Friends) munosabatini topish
## Topshiriq sharti:
Ikki foydalanuvchining umumiy do'stlarini INTERSECT orqali toping.

## Yechim (SQL kodi):
```sql
CREATE TABLE dostlar (u_id INT, dost_id INT);
INSERT INTO dostlar VALUES (1, 10), (1, 20), (1, 30), (2, 20), (2, 30), (2, 40);

SELECT dost_id AS umumiy_dost 
FROM dostlar WHERE u_id = 1
INTERSECT
SELECT dost_id 
FROM dostlar WHERE u_id = 2;
```

## Tushuntirish va Mantiq:
Ijtimoiy tarmoqlarda ikki profilning umumiy do'stlari (Mutual Connections) INTERSECT bilan aniqlanadi.

## Ishlash natijasi:
```text
umumiy_dost 
-------------
          20
          30
(2 rows)
```


# 543-Topshiriq: UNION ALL va GROUP BY yordamida Full Outer Join simulyatsiyasi
## Topshiriq sharti:
FULL OUTER JOIN mavjud bo'lmagan ba'zi sodda ma'lumotlar bazalarida UNION ALL orqali to'liq birlashishni hosil qilish.

## Yechim (SQL kodi):
```sql
SELECT COALESCE(t.ism, s.ism) AS ism
FROM filial_toshkent t
FULL JOIN filial_samarqand s ON t.telefon = s.telefon;
```

## Tushuntirish va Mantiq:
Relyatsion algebrada FULL JOIN va UNION o'zaro chambarchas bog'liqdir.

## Ishlash natijasi:
```text
ism  
------
 Ali
 Vali
 Gani
(3 rows)
```


# 544-Topshiriq: EXCEPT orqali ruxsat berilgan IP manzillardan begonalarni tozalash
## Topshiriq sharti:
Tizimga kirgan barcha IP lardan oq ro'yxatdagi (whitelist) IP larni ayirib shubhali manzillarni topish.

## Yechim (SQL kodi):
```sql
CREATE TABLE kirgan_iplar (ip TEXT);
CREATE TABLE oq_royxat (ip TEXT);

INSERT INTO kirgan_iplar VALUES ('192.168.1.1'), ('10.0.0.5'), ('172.16.0.99');
INSERT INTO oq_royxat VALUES ('192.168.1.1'), ('10.0.0.5');

SELECT ip AS notanish_ip FROM kirgan_iplar
EXCEPT
SELECT ip FROM oq_royxat;
```

## Tushuntirish va Mantiq:
Notanish va xavfli IP manzillar bir zumda aniqlanadi.

## Ishlash natijasi:
```text
notanish_ip  
--------------
 172.16.0.99
(1 row)
```


# 545-Topshiriq: Barcha to'plam amallarini bitta murakkab so'rovda qo'llash
## Topshiriq sharti:
(A UNION B) EXCEPT (C INTERSECT D) kombinatsiyasi.

## Yechim (SQL kodi):
```sql
((SELECT 1 AS n UNION SELECT 2) 
EXCEPT 
(SELECT 2 INTERSECT SELECT 2));
```

## Tushuntirish va Mantiq:
Murakkab diskret matematika munosabatlari to'liq ifodalanadi.

## Ishlash natijasi:
```text
n 
---
 1
(1 row)
```


# 546-Topshiriq: To'plamlar birlashmasida o'rtacha qiymat hisoblash xatosi
## Topshiriq sharti:
Nega o'rtacha qiymatlar alohida hisoblanib keyin o'rtachasi olinmasligini (Simpson Paradoksi) tushuntiring.

## Yechim (SQL kodi):
```sql
-- Xato: (AVG(A) + AVG(B)) / 2
-- To'g'ri: Barcha xom qatorlar UNION ALL qilinib, keyin bitta AVG hisoblanadi:
SELECT ROUND(AVG(summa), 2) AS haqiqiy_ortacha
FROM (
    SELECT 100::NUMERIC AS summa UNION ALL
    SELECT 100 UNION ALL
    SELECT 100 UNION ALL
    SELECT 200
) umumiy;
```

## Tushuntirish va Mantiq:
Guruhlar hajmi har xil bo'lgani sababli, o'rtachalarning o'rtachasi xato beradi. Har doim barcha qatorlar bitta to'plamga UNION ALL qilinib umumiy AVG olinadi.

## Ishlash natijasi:
```text
haqiqiy_ortacha 
-----------------
          125.00
(1 row)
```


# 547-Topshiriq: UNION orqali ma'lumotlar bazasi lug'atini (Dictionary) shakllantirish
## Topshiriq sharti:
Tizimdagi barcha mavjud unikal so'zlar va toifalarni bitta ro'yxatga jamlash.

## Yechim (SQL kodi):
```sql
SELECT ism AS kalit_soz FROM filial_toshkent
UNION
SELECT ism FROM filial_samarqand
UNION
SELECT holat FROM (SELECT 'Yangi' AS holat) h;
```

## Tushuntirish va Mantiq:
Turli jadvallardagi matnlar unikal lug'atga yig'iladi.

## Ishlash natijasi:
```text
kalit_soz 
-----------
 Ali
 Gani
 Vali
 Yangi
(4 rows)
```


# 548-Topshiriq: EXCEPT ALL va qoldiq zaxirani hisoblash
## Topshiriq sharti:
Ishlab chiqarishga kerakli xomashyo sonidan omborda borini ayirib yetishmayotgan qismlarni topish.

## Yechim (SQL kodi):
```sql
CREATE TABLE kerak (detal TEXT);
CREATE TABLE omborda_bor (detal TEXT);

INSERT INTO kerak VALUES ('Bolt'), ('Bolt'), ('Bolt'), ('Gayka');
INSERT INTO omborda_bor VALUES ('Bolt');

SELECT detal AS yetishmayotgan_detal 
FROM kerak 
EXCEPT ALL 
SELECT detal 
FROM omborda_bor;
```

## Tushuntirish va Mantiq:
3 ta bolt kerak, 1 ta bor. 'EXCEPT ALL' aynan yetishmayotgan 2 ta bolt va 1 ta gaykani aniq chiqaradi.

## Ishlash natijasi:
```text
yetishmayotgan_detal 
---------------------
 Bolt
 Bolt
 Gayka
(3 rows)
```


# 549-Topshiriq: To'plam amallarida xotira cheklovlari va Hash vs Sort
## Topshiriq sharti:
UNION operatsiyasi xotirada katta hajm talab qilganda diskka tushishi.

## Yechim (SQL kodi):
```sql
SELECT 'UNION orqali millionlab qatorlarni tekshirish temp_file yaratishi mumkin, UNION ALL esa deyarli xotira yemaydi' AS tahlil;
```

## Tushuntirish va Mantiq:
Yirik ma'lumotlar bazalarida UNION o'rniga faqat zarurat bo'lgandagina foydalanish tavsiya etiladi.

## Ishlash natijasi:
```text
tahlil                                                 
--------------------------------------------------------------------------------------------------------
 UNION orqali millionlab qatorlarni tekshirish temp_file yaratishi mumkin, UNION ALL esa deyarli xotira yemaydi
(1 row)
```


# 550-Topshiriq: Korporativ To'plam: Bank Replikatsiya Audit Tizimi (Data Reconciliation Engine)
## Topshiriq sharti:
Asosiy tranzaksion baza (OLTP) va Zaxira hisobot bazasi (DWH) o'rtasidagi ma'lumotlarni solishtirib, qaysi tranzaksiyalar yo'qolgan yoki tafovutga uchraganini UNION, EXCEPT va INTERSECT yordamida to'liq hisobot qilib bering.

## Yechim (SQL kodi):
```sql
CREATE TABLE oltp_tranzaksiyalar (
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
ORDER BY tr_id, tafovut_turi;
```

## Tushuntirish va Mantiq:
Ushbu korporativ so'rov bank va to'lov tashkilotlarida har tun ishga tushiriluvchi Avtomatik Rekonsilyatsiya Dvigatelidir (Automated Reconciliation Engine): relyatsion to'plam ayirmasi (EXCEPT) orqali asosiy baza va replika bazadagi barcha xatoliklar, yetib bormagan tranzaksiyalar va tafovutli summalar bir millisekundda aniqlanib xavfsizlik jurnaliga yoziladi.

## Ishlash natijasi:
```text
tr_id | hisob_raqam |   summa    |   holat    |                 tafovut_turi                 
-------+-------------+------------+------------+----------------------------------------------
  1002 | 202080002   | 1100000.00 | BAJARILDI  | Faqat DWH da bor (OLTP da mavjud emas)
  1002 | 202080002   | 1200000.00 | BAJARILDI  | Faqat OLTP da bor (DWH ga yetib bormagan)
  1003 | 202080003   |  750000.00 | KUTILMOQDA | Faqat OLTP da bor (DWH ga yetib bormagan)
  1004 | 202080004   | 3000000.00 | BAJARILDI  | Faqat DWH da bor (OLTP da mavjud emas)
(4 rows)
```

