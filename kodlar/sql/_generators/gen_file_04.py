import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

# List of 50 tasks for File 4: 151 - 200
# DQL: Oddiy tanlash (SELECT) va filtrlash (WHERE, DISTINCT, ORDER BY, LIMIT, OFFSET, BETWEEN, IN, LIKE, ILIKE, IS NULL)

dql_data = [
    (
        151,
        "Aniq ustunlarni tanlash (SELECT Projection)",
        "Xodimlar jadvalidan faqat ularning familiyasi, ismi va elektron pochtasini tanlab oling.",
        """CREATE TABLE xodim_royxat (
    id SERIAL PRIMARY KEY,
    ism VARCHAR(50),
    familiya VARCHAR(50),
    email VARCHAR(100),
    maosh NUMERIC(12, 2)
);
INSERT INTO xodim_royxat (ism, familiya, email, maosh) VALUES 
('Anvar', 'Soliyev', 'anvar@shirkat.uz', 8500000),
('Malika', 'Karimova', 'malika@shirkat.uz', 9200000);

SELECT ism, familiya, email 
FROM xodim_royxat;""",
        "Relyatsion algebrada bu operatsiya 'Proyeksiyalash' (Projection - \u03c0) deb ataladi. Keraksiz ustunlarni (masalan, maosh) o'qimaslik tarmoq yukini kamaytiradi va disk I/O ni sezilarli tejaydi. 'SELECT *' amaliyotda faqat tezkor tahlil uchun ishlatilishi lozim.",
        """  ism   | familiya |       email        
--------+----------+--------------------
 Anvar  | Soliyev  | anvar@shirkat.uz
 Malika | Karimova | malika@shirkat.uz
(2 rows)"""
    ),
    (
        152,
        "Ustunlarga taxallus berish (Column Aliasing: AS)",
        "Xodimning ismini 'Xodim Ismi', maoshini esa 'Oylik Maoshi (so'm)' ko'rinishida sarlavha qilib chiqaring.",
        """SELECT 
    ism AS "Xodim Ismi",
    maosh AS "Oylik Maoshi (so'm)"
FROM xodim_royxat;""",
        "'AS' kalit so'zi natijadagi ustun sarlavhasini o'zgartiradi. Agar taxallusda bo'shliq yoki maxsus belgilar bo'lsa, u qo'shtirnoqqa (\"...\") olinishi shart.",
        """ Xodim Ismi | Oylik Maoshi (so'm) 
------------+---------------------
 Anvar      |          8500000.00
 Malika     |          9200000.00
(2 rows)"""
    ),
    (
        153,
        "Hisoblangan ustunlar va arifmetik amallar",
        "Har bir xodimning maoshidan 12% daromad solig'ini hisoblab, qolgan sof maoshini ko'rsating.",
        """SELECT 
    ism, 
    maosh,
    ROUND(maosh * 0.12, 2) AS daromad_soligi,
    ROUND(maosh * 0.88, 2) AS sof_maosh
FROM xodim_royxat;""",
        "SELECT bandida ustunlar ustida arifmetik amallar (+, -, *, /) bajarish mumkin. RDBMS har bir qator uchun ushbu formulani hisoblaydi va natijani virtual ustunda ko'rsatadi.",
        """  ism   |   maosh    | daromad_soligi | sof_maosh  
--------+------------+----------------+------------
 Anvar  | 8500000.00 |     1020000.00 | 7480000.00
 Malika | 9200000.00 |     1104000.00 | 8096000.00
(2 rows)"""
    ),
    (
        154,
        "Matnlarni birlashtirish (String Concatenation: || operatori)",
        "Xodimning ismi va familiyasini bitta ustunga 'Ism Familiya' shaklida birlashtirib chiqaring.",
        """SELECT 
    ism || ' ' || familiya AS toliq_ism,
    email
FROM xodim_royxat;""",
        "ANSI SQL va PostgreSQL da '||' operatori satrlarni bir-biriga ulaydi (concatenation). Agar qismlardan biri NULL bo'lsa, natija ham NULL bo'ladi (buning oldini olish uchun CONCAT funksiyasi qo'llanadi).",
        """    toliq_ism    |       email        
-----------------+--------------------
 Anvar Soliyev   | anvar@shirkat.uz
 Malika Karimova | malika@shirkat.uz
(2 rows)"""
    ),
    (
        155,
        "Oddiy WHERE filtri: Tenglik (=) sharti",
        "Mahsulotlar orasidan faqat 'Noutbuk' bo'lganlarini tanlab oling.",
        """CREATE TABLE tovarlar (id INT, nomi TEXT, toifa TEXT, narx NUMERIC, mavjud BOOLEAN);
INSERT INTO tovarlar VALUES 
(1, 'Asus ROG', 'Noutbuk', 14000000, TRUE),
(2, 'iPhone 15', 'Smartfon', 12000000, TRUE),
(3, 'Lenovo ThinkPad', 'Noutbuk', 11000000, FALSE);

SELECT nomi, narx 
FROM tovarlar 
WHERE toifa = 'Noutbuk';""",
        "Relyatsion algebrada bu operatsiya 'Tanlash' (Selection - \u03c3) deb ataladi. RDBMS jadvaldagi barcha qatorlarni 'toifa = 'Noutbuk'' predikatiga tekshiradi va faqat TRUE bo'lgan qatorlarni qaytaradi.",
        """      nomi       |    narx     
-----------------+-------------
 Asus ROG        | 14000000.00
 Lenovo ThinkPad | 11000000.00
(2 rows)"""
    ),
    (
        156,
        "Teng emaslik operatorlari: <> va !=",
        "'Smartfon' toifasiga kirmaydigan barcha tovarlarni toping.",
        """SELECT nomi, toifa 
FROM tovarlar 
WHERE toifa <> 'Smartfon';""",
        "ANSI SQL standartida teng emaslik '<>' ko'rinishida yoziladi, ko'pchilik RDBMS larda '!=' sintaksisi ham qo'llab-quvvatlanadi. Eslatma: Agar toifa qiymati NULL bo'lsa, u ham ushbu natijaga kirmaydi.",
        """      nomi       |  toifa  
-----------------+---------
 Asus ROG        | Noutbuk
 Lenovo ThinkPad | Noutbuk
(2 rows)"""
    ),
    (
        157,
        "Katta va kichik operatorlari: >, <, >=, <=",
        "Narxi 12,000,000 so'mdan arzon yoki unga teng bo'lgan tovarlarni aniqlang.",
        """SELECT nomi, narx 
FROM tovarlar 
WHERE narx <= 12000000;""",
        "Taqqoslash operatorlari sonlar, sanalar va hatto alifbo tartibida satrlar ustida ham ishlaydi.",
        """      nomi       |    narx     
-----------------+-------------
 iPhone 15       | 12000000.00
 Lenovo ThinkPad | 11000000.00
(2 rows)"""
    ),
    (
        158,
        "Mantiqiy AND operatori (Ikkala shart bir vaqtda bajarilishi)",
        "Noutbuk bo'lgan VA ayni paytda omborda mavjud (mavjud = TRUE) tovarlarni toping.",
        """SELECT nomi, toifa, narx 
FROM tovarlar 
WHERE toifa = 'Noutbuk' AND mavjud = TRUE;""",
        "'AND' operatori faqatgina har ikkala mantiqiy ifoda ham TRUE bo'lgandagina natijani qaytaradi.",
        """   nomi   |  toifa  |    narx     
----------+---------+-------------
 Asus ROG | Noutbuk | 14000000.00
(1 row)"""
    ),
    (
        159,
        "Mantiqiy OR operatori (Kamida bitta shart bajarilishi)",
        "Toifasi 'Smartfon' bo'lgan YOKI narxi 13,000,000 so'mdan oshadigan tovarlarni chiqaring.",
        """SELECT nomi, toifa, narx 
FROM tovarlar 
WHERE toifa = 'Smartfon' OR narx > 13000000;""",
        "'OR' operatori ifodalardan kamida bittasi qanoatlantirilganda qatorni natijaga qo'shadi.",
        """   nomi    |  toifa   |    narx     
-----------+----------+-------------
 Asus ROG  | Noutbuk  | 14000000.00
 iPhone 15 | Smartfon | 12000000.00
(2 rows)"""
    ),
    (
        160,
        "Operatorlar ustuvorligi va qavslar ahamiyati",
        "AND operatori OR dan oldin bajarilishi sababli qavslardan foydalanish qoidasini ko'rsating.",
        """SELECT nomi, toifa, narx, mavjud 
FROM tovarlar 
WHERE (toifa = 'Noutbuk' OR toifa = 'Smartfon') AND mavjud = TRUE;""",
        "SQL da 'AND' ning ustuvorligi (precedence) 'OR' ga qaraganda yuqori. Qavslar qo'yilmasa, so'rov `toifa = 'Noutbuk' OR (toifa = 'Smartfon' AND mavjud = TRUE)` deb noto'g'ri talqin qilinadi.",
        """   nomi    |  toifa   |    narx     | mavjud 
-----------+----------+-------------+--------
 Asus ROG  | Noutbuk  | 14000000.00 | t
 iPhone 15 | Smartfon | 12000000.00 | t
(2 rows)"""
    ),
    (
        161,
        "Oraliqni filtrlash: BETWEEN ... AND ...",
        "Narxi 10,000,000 dan 13,000,000 so'mgacha bo'lgan tovarlarni aniqlang.",
        """SELECT nomi, narx 
FROM tovarlar 
WHERE narx BETWEEN 10000000 AND 13000000;""",
        "'BETWEEN a AND b' chegaralarni ham o'z ichiga oladi (`narx >= a AND narx <= b` ifodasi bilan aynan bir xil).",
        """      nomi       |    narx     
-----------------+-------------
 iPhone 15       | 12000000.00
 Lenovo ThinkPad | 11000000.00
(2 rows)"""
    ),
    (
        162,
        "Oraliqdan tashqarini tanlash: NOT BETWEEN",
        "O'rtacha narxlar oralig'iga (11M dan 13M gacha) kirmaydigan arzon yoki qimmat mahsulotlarni toping.",
        """SELECT nomi, narx 
FROM tovarlar 
WHERE narx NOT BETWEEN 11000000 AND 13000000;""",
        "'NOT BETWEEN' belgilangan diapazondan tashqaridagi qiymatlarni (`narx < a OR narx > b`) filtrlaydi.",
        """   nomi   |    narx     
----------+-------------
 Asus ROG | 14000000.00
(1 row)"""
    ),
    (
        163,
        "Sanalar oralig'ida BETWEEN filtri",
        "2026-yil 1-yanvardan 2026-yil 31-yanvargacha berilgan buyurtmalarni saralash.",
        """CREATE TABLE s_buyurtmalar (id INT, summa NUMERIC, sana DATE);
INSERT INTO s_buyurtmalar VALUES 
(1, 150000, '2026-01-10'), (2, 250000, '2026-01-25'), (3, 80000, '2026-02-05');

SELECT id, summa, sana 
FROM s_buyurtmalar 
WHERE sana BETWEEN '2026-01-01' AND '2026-01-31';""",
        "Sana turlari bilan BETWEEN ishlatilganda chegaralar kiritiladi. Eslatma: TIMESTAMPTZ bilan ishlaganda oxirgi kunning '23:59:59' qismiga e'tibor qaratish kerak.",
        """ id |   summa   |    sana    
----+-----------+------------
  1 | 150000.00 | 2026-01-10
  2 | 250000.00 | 2026-01-25
(2 rows)"""
    ),
    (
        164,
        "Ro'yxat bo'yicha filtrlash: IN operatori",
        "ID raqami 1, 3 yoki 7 bo'lgan mahsulotlarni bitta ixcham so'rovda oling.",
        """SELECT id, nomi, narx 
FROM tovarlar 
WHERE id IN (1, 3, 7);""",
        "'IN (v1, v2, ...)' operatori `id = 1 OR id = 3 OR id = 7` yozuvining qisqa va qulay shaklidir. RDBMS ichida u ko'pincha B-Tree indeksida tezkor skanerlashga aylanadi.",
        """ id |      nomi       |    narx     
----+-----------------+-------------
  1 | Asus ROG        | 14000000.00
  3 | Lenovo ThinkPad | 11000000.00
(2 rows)"""
    ),
    (
        165,
        "Ro'yxatda mavjud bo'lmaganlarni tanlash: NOT IN",
        "Toifasi 'Smartfon' yoki 'Planshet' bo'lmagan barcha boshqa tovarlarni chiqaring.",
        """SELECT nomi, toifa 
FROM tovarlar 
WHERE toifa NOT IN ('Smartfon', 'Planshet');""",
        "'NOT IN' ko'rsatilgan to'plamdagi hech bir elementga teng bo'lmagan qatorlarni qaytaradi.",
        """      nomi       |  toifa  
-----------------+---------
 Asus ROG        | Noutbuk
 Lenovo ThinkPad | Noutbuk
(2 rows)"""
    ),
    (
        166,
        "NOT IN va NULL qiymat tuzog'i",
        "Agar NOT IN ro'yxatida bitta bo'lsa ham NULL qiymat uchrasa nima bo'lishini ko'rsating.",
        """SELECT nomi 
FROM tovarlar 
WHERE toifa NOT IN ('Smartfon', NULL);""",
        "SQL ning uch qiymatli mantiqiy modelida (3-valued logic: TRUE, FALSE, UNKNOWN), `x NOT IN ('Smartfon', NULL)` ifodasi `x <> 'Smartfon' AND x <> NULL` ga aylanadi. `x <> NULL` har doim UNKNOWN bo'lgani sababli butun ifoda UNKNOWN bo'lib qoladi va natija BO'SH (0 qator) chiqadi!",
        """ nomi 
------
(0 rows)"""
    ),
    (
        167,
        "Bo'sh qiymatlarni tekshirish: IS NULL",
        "Mijozlar orasidan elektron pochtasi kiritilmagan (NULL bo'lgan) foydalanuvchilarni toping.",
        """CREATE TABLE mijoz_baza (id INT, ism TEXT, email TEXT);
INSERT INTO mijoz_baza VALUES (1, 'Alisher', NULL), (2, 'Bobur', 'bobur@mail.uz');

SELECT ism 
FROM mijoz_baza 
WHERE email IS NULL;""",
        "SQL da 'email = NULL' deb yozish xatodir, chunki hech narsa NULL ga teng bo'lolmaydi. NULL bor-yo'qligi faqat 'IS NULL' operatori orqali tekshiriladi.",
        """   ism   
---------
 Alisher
(1 row)"""
    ),
    (
        168,
        "Bo'sh bo'lmagan qiymatlarni aniqlash: IS NOT NULL",
        "Faqat rasmiy e-maili tasdiqlangan va mavjud mijozlarni saralang.",
        """SELECT ism, email 
FROM mijoz_baza 
WHERE email IS NOT NULL;""",
        "'IS NOT NULL' ustunda haqiqiy qiymat mavjud bo'lgan qatorlarni ajratib beradi.",
        """  ism  |     email     
-------+---------------
 Bobur | bobur@mail.uz
(1 row)"""
    ),
    (
        169,
        "NULL-safe tenglik: IS NOT DISTINCT FROM",
        "Ikki qiymatni, hattoki ularning ikkalasi ham NULL bo'lgan taqdirda ularni 'teng' deb hisoblovchi operatorni ko'rsating.",
        """SELECT 
    (NULL = NULL) AS oddiy_tenglik,
    (NULL IS NOT DISTINCT FROM NULL) AS xavfsiz_tenglik;""",
        "'IS NOT DISTINCT FROM' NULL qiymatlarni ham bir-biriga teng deb biladi. Bu tashqi so'rovlarda va murakkab JOIN shartlarida NULL larni xatosiz taqqoslashda juda zarur.",
        """ oddiy_tenglik | xavfsiz_tenglik 
---------------+-----------------
 NULL          | t
(1 row)"""
    ),
    (
        170,
        "Shablon bo'yicha qidirish: LIKE va % belgisi",
        "Nomi 'Asus' so'zi bilan boshlanadigan barcha tovarlarni toping.",
        """SELECT nomi, narx 
FROM tovarlar 
WHERE nomi LIKE 'Asus%';""",
        "'%' belgisi ixtiyoriy sondagi (0 yoki undan ortiq) belgilarni ifodalaydi. 'Asus%' - 'Asus' bilan boshlanuvchi barcha satrlarni topadi.",
        """   nomi   |    narx     
----------+-------------
 Asus ROG | 14000000.00
(1 row)"""
    ),
    (
        171,
        "Satrning istalgan joyida so'zni qidirish (%so'z%)",
        "Nomi tarkibida 'Pad' so'zi uchraydigan mahsulotlarni aniqlang.",
        """SELECT nomi 
FROM tovarlar 
WHERE nomi LIKE '%Pad%';""",
        "'%so'z%' shabloni qidirilayotgan satr qatorning boshi, o'rtasi yoki oxirida uchrashidan qat'i nazar topadi.",
        """      nomi       
-----------------
 Lenovo ThinkPad
(1 row)"""
    ),
    (
        172,
        "Yagona belgini almashtiruvchi pastki chiziq: LIKE va _",
        "Telefon modeli aynan 4 ta belgidan iborat va oxiri '0' bilan tugaydigan mahsulotlarni toping.",
        """CREATE TABLE modellar (kod VARCHAR(10));
INSERT INTO modellar VALUES ('A100'), ('B20'), ('X500'), ('M10');

SELECT kod 
FROM modellar 
WHERE kod LIKE '__00';""",
        "'_' (underscore) belgisi aynan 1 ta ixtiyoriy belgini ifodalaydi. '__00' aynan 4 ta belgidan iborat va oxiri '00' bilan tugagan kodlarni filtrlaydi.",
        """ kod  
------
 A100
 X500
(2 rows)"""
    ),
    (
        173,
        "Katta-kichik harfni inobatga olmaydigan qidiruv: ILIKE",
        "Foydalanuvchi qidiruv maydoniga 'asus', 'ASUS' yoki 'AsUs' deb yozganidan qat'i nazar to'g'ri topuvchi ILIKE so'rovini yozing.",
        """SELECT nomi 
FROM tovarlar 
WHERE nomi ILIKE 'asus%';""",
        "'ILIKE' PostgreSQL ning xususiy kengaytmasi bo'lib, registrga sezgir bo'lmagan (case-insensitive) LIKE amalini bajaradi. Standart SQL da buning uchun `WHERE LOWER(nomi) LIKE LOWER('asus%')` yoziladi.",
        """   nomi   
----------
 Asus ROG
(1 row)"""
    ),
    (
        174,
        "Shablondan tashqarini topish: NOT LIKE va NOT ILIKE",
        "Elektron pochta domeni '@gmail.com' bilan tugamaydigan korporativ foydalanuvchilarni aniqlang.",
        """SELECT ism, email 
FROM xodim_royxat 
WHERE email NOT LIKE '%@gmail.com';""",
        "'NOT LIKE' shablonga mos kelmagan barcha satrlarni qaytaradi.",
        """  ism   |       email        
--------+--------------------
 Anvar  | anvar@shirkat.uz
 Malika | malika@shirkat.uz
(2 rows)"""
    ),
    (
        175,
        "Maxsus belgilarni ekranlash (ESCAPE bandi)",
        "Matn ichidagi haqiqiy '%' belgisini qidirish (masalan: '10%' chegirma).",
        """CREATE TABLE aksiyalar (matn TEXT);
INSERT INTO aksiyalar VALUES ('Chegirma 10% gacha'), ('Oddiy xabar');

SELECT matn 
FROM aksiyalar 
WHERE matn LIKE '%10\%%' ESCAPE '\';""",
        "'ESCAPE' bandi qidiruv shablonidagi maxsus belgini (masalan '%') o'zining asl ma'nosida qabul qilinishini ta'minlaydi.",
        """        matn        
--------------------
 Chegirma 10% gacha
(1 row)"""
    ),
    (
        176,
        "Muntazam ifodalar (RegEx) bilan filtrlash: ~ operatori",
        "Nomida faqat raqamlar bilan boshlanadigan modellarni POSIX RegEx (~) orqali saralang.",
        """SELECT kod 
FROM modellar 
WHERE kod ~ '^[A-Z][0-9]+';""",
        "PostgreSQL da '~' operatori to'liq POSIX muntazam ifodalarini qo'llab-quvvatlaydi. Bu yerda bosh harf bilan boshlanib, ketidan raqam keluvchi qatorlar filtrlanadi.",
        """ kod  
------
 A100
 B20
 X500
 M10
(4 rows)"""
    ),
    (
        177,
        "Registrga sezgir bo'lmagan RegEx: ~* operatori",
        "Matnda 'pro' yoki 'max' so'zlari katta-kichikligidan qat'i nazar borligini tekshirish.",
        """CREATE TABLE gadjetlar (nomi TEXT);
INSERT INTO gadjetlar VALUES ('iPhone 15 Pro'), ('MacBook MAX'), ('Redmi Note');

SELECT nomi 
FROM gadjetlar 
WHERE nomi ~* '(pro|max)';""",
        "'~*' operatori case-insensitive RegEx tekshiruvini amalga oshiradi. '|' esa 'yoki' amalini bajaradi.",
        """     nomi      
---------------
 iPhone 15 Pro
 MacBook MAX
(2 rows)"""
    ),
    (
        178,
        "Takrorlanishlarni yo'qotish: DISTINCT",
        "Jadvalda qanday toifalar mavjudligini takrorlanishlarsiz yagona ro'yxat sifatida chiqaring.",
        """SELECT DISTINCT toifa 
FROM tovarlar;""",
        "'DISTINCT' so'rovi barcha takrorlanuvchi qatorlarni filtrlash uchun natijani vaqtincha xotirada (WorkMem) saralaydi yoki hash-jadval (HashAggregate) tuzadi.",
        """  toifa   
----------
 Noutbuk
 Smartfon
(2 rows)"""
    ),
    (
        179,
        "Bir nechta ustun bo'yicha DISTINCT",
        "Mijoz va to'lov usuli kombinatsiyasining noyob juftliklarini oling.",
        """CREATE TABLE tolov_log (mijoz TEXT, usul TEXT);
INSERT INTO tolov_log VALUES ('Ali', 'karta'), ('Ali', 'karta'), ('Ali', 'naqd'), ('Vali', 'karta');

SELECT DISTINCT mijoz, usul 
FROM tolov_log;""",
        "Ko'p ustunli DISTINCT da har ikkala ustun bir vaqtda bir xil bo'lgan qatorlar olib tashlanadi.",
        """ mijoz | usul  
-------+-------
 Ali   | karta
 Ali   | naqd
 Vali  | karta
(3 rows)"""
    ),
    (
        180,
        "PostgreSQL maxsus imkoniyati: DISTINCT ON (ustun)",
        "Har bir mijozning eng oxirgi amalga oshirgan to'lovini bitta so'rovda oling.",
        """CREATE TABLE tranzaksiyalar_vaqt (id INT, mijoz TEXT, summa NUMERIC, vaqt TIMESTAMP);
INSERT INTO tranzaksiyalar_vaqt VALUES 
(1, 'Ali', 10000, '2026-03-01 10:00'),
(2, 'Ali', 50000, '2026-03-01 12:00'),
(3, 'Vali', 30000, '2026-03-01 11:00');

SELECT DISTINCT ON (mijoz) mijoz, summa, vaqt 
FROM tranzaksiyalar_vaqt 
ORDER BY mijoz, vaqt DESC;""",
        "'DISTINCT ON (ustun)' berilgan ustun bo'yicha guruhlaydi va ORDER BY tartibiga ko'ra birinchi uchragan qatorni saqlab qoladi. Guruh bo'yicha eng oxirgi yoki eng katta qiymatni olishda eng tezkor usuldir.",
        """ mijoz |  summa   |        vaqt         
-------+----------+---------------------
 Ali   | 50000.00 | 2026-03-01 12:00:00
 Vali  | 30000.00 | 2026-03-01 11:00:00
(2 rows)"""
    ),
    (
        181,
        "Natijalarni o'sish tartibida saralash: ORDER BY ASC",
        "Mahsulotlarni ularning narxi bo'yicha eng arzonidan eng qimmatiga qarab saralab ko'rsating.",
        """SELECT nomi, narx 
FROM tovarlar 
ORDER BY narx ASC;""",
        "'ORDER BY narx ASC' natijani kichikdan kattaga qarab saralaydi. 'ASC' ko'rsatilmasa ham sukut bo'yicha qabul qilinadi.",
        """      nomi       |    narx     
-----------------+-------------
 Lenovo ThinkPad | 11000000.00
 iPhone 15       | 12000000.00
 Asus ROG        | 14000000.00
(3 rows)"""
    ),
    (
        182,
        "Natijalarni kamayish tartibida saralash: ORDER BY DESC",
        "Xodimlarni eng yuqori maosh oluvchidan boshlab saralash.",
        """SELECT ism, maosh 
FROM xodim_royxat 
ORDER BY maosh DESC;""",
        "'DESC' (descending) eng katta qiymatdan eng kichigiga qarab saralaydi.",
        """  ism   |   maosh    
--------+------------
 Malika | 9200000.00
 Anvar  | 8500000.00
(2 rows)"""
    ),
    (
        183,
        "Bir nechta ustun bo'yicha tartiblash",
        "Avval toifa bo'yicha alifbo tartibida, so'ngra bir xil toifa ichida narx bo'yicha qimmatidan arzoniga qarab saralang.",
        """SELECT toifa, nomi, narx 
FROM tovarlar 
ORDER BY toifa ASC, narx DESC;""",
        "RDBMS avval 1-ustun bo'yicha saralaydi. Agar 1-ustun qiymatlari teng bo'lsa, 2-ustun bo'yicha taqqoslashga o'tadi.",
        """  toifa   |      nomi       |    narx     
----------+-----------------+-------------
 Noutbuk  | Asus ROG        | 14000000.00
 Noutbuk  | Lenovo ThinkPad | 11000000.00
 Smartfon | iPhone 15       | 12000000.00
(3 rows)"""
    ),
    (
        184,
        "Ustun o'rni raqami bilan saralash (ORDER BY 1, 2)",
        "Ustun nomlarini qayta yozmasdan ularning SELECT dagi tartib raqami orqali saralash.",
        """SELECT toifa, nomi, narx 
FROM tovarlar 
ORDER BY 1, 3 DESC;""",
        "'ORDER BY 1, 3 DESC' birinchi ustun (toifa) va uchinchi ustun (narx) bo'yicha saralashni bildiradi.",
        """  toifa   |      nomi       |    narx     
----------+-----------------+-------------
 Noutbuk  | Asus ROG        | 14000000.00
 Noutbuk  | Lenovo ThinkPad | 11000000.00
 Smartfon | iPhone 15       | 12000000.00
(3 rows)"""
    ),
    (
        185,
        "NULL qiymatlarni saralashda boshqarish: NULLS FIRST",
        "Saralashda qiymati bo'sh (NULL) bo'lgan qatorlar eng boshida chiqishini ta'minlang.",
        """CREATE TABLE reyting (ism TEXT, ball INT);
INSERT INTO reyting VALUES ('Ali', 85), ('Vali', NULL), ('Gani', 95);

SELECT ism, ball 
FROM reyting 
ORDER BY ball ASC NULLS FIRST;""",
        "'NULLS FIRST' bandi bo'sh qiymatlarni barcha sonlardan kichik deb baholab, ro'yxatning eng boshiga joylashtiradi.",
        """ ism  | ball 
------+------
 Vali | NULL
 Ali  |   85
 Gani |   95
(3 rows)"""
    ),
    (
        186,
        "NULL qiymatlarni eng oxiriga surish: NULLS LAST",
        "Kamayish tartibida saralaganda NULL lar birinchi chiqib qolmasligi uchun NULLS LAST dan foydalaning.",
        """SELECT ism, ball 
FROM reyting 
ORDER BY ball DESC NULLS LAST;""",
        "PostgreSQL da odatda DESC tartibida NULL qiymatlar boshida keladi. 'NULLS LAST' ularni jadvalning eng quyi qismiga surib beradi.",
        """ ism  | ball 
------+------
 Gani |   95
 Ali  |   85
 Vali | NULL
(3 rows)"""
    ),
    (
        187,
        "Ifodalar bo'yicha saralash (ORDER BY Expression)",
        "Talabalarni ularning ism uzunligi (LENGTH) bo'yicha saralash.",
        """SELECT ism 
FROM xodim_royxat 
ORDER BY LENGTH(ism) ASC;""",
        "ORDER BY bandiga ustun nomidan tashqari ixtiyoriy SQL funksiyalari va formulalarini qo'yish mumkin.",
        """  ism   
--------
 Anvar
 Malika
(2 rows)"""
    ),
    (
        188,
        "Natijalar sonini cheklash: LIMIT",
        "Tizimdagi eng qimmat bitta tovar ma'lumotini oling.",
        """SELECT nomi, narx 
FROM tovarlar 
ORDER BY narx DESC 
LIMIT 1;""",
        "'LIMIT n' qidiruv natijalarining faqat dastlabki n tasini qaytaradi. LIMIT doimo ORDER BY bilan birga ishlatilishi shart, aks holda natija tasodifiy bo'lib qoladi.",
        """   nomi   |    narx     
----------+-------------
 Asus ROG | 14000000.00
(1 row)"""
    ),
    (
        189,
        "Sahifalash (Pagination): LIMIT va OFFSET",
        "Har bir sahifada 2 tadan tovar ko'rsatilganda, 2-sahifadagi tovarlarni chiqarish so'rovini yozing.",
        """SELECT nomi, narx 
FROM tovarlar 
ORDER BY id 
LIMIT 2 OFFSET 2;""",
        "'OFFSET m' dastlabki m ta qatorni tashlab yuboradi, 'LIMIT n' esa undan keyingi n ta qatorni oladi. 2-sahifa formulasi: `OFFSET (sahifa_raqami - 1) * sahifa_hajmi`.",
        """      nomi       |    narx     
-----------------+-------------
 Lenovo ThinkPad | 11000000.00
(1 row)"""
    ),
    (
        190,
        "Standart SQL sahifalash: FETCH FIRST ... ROWS ONLY",
        "LIMIT o'rniga zamonaviy ANSI SQL:2008 standartidagi FETCH kalit so'zini qo'llang.",
        """SELECT nomi, narx 
FROM tovarlar 
ORDER BY narx DESC 
OFFSET 0 ROWS 
FETCH FIRST 2 ROWS ONLY;""",
        "'OFFSET ... FETCH FIRST ...' barcha asosiy ma'lumotlar bazalarida (PostgreSQL, Oracle, MS SQL Server, DB2) birdek ishlaydigan standartlashtirilgan sintaksisdir.",
        """   nomi    |    narx     
-----------+-------------
 Asus ROG  | 14000000.00
 iPhone 15 | 12000000.00
(2 rows)"""
    ),
    (
        191,
        "Teng qiymatlarni ham qamrab oluvchi FETCH WITH TIES",
        "Top-2 talabani tanlaganda, 2-o'rindagi talaba bilan bir xil ball to'plagan boshqa talabalarni ham qoldirmasdan olish.",
        """CREATE TABLE imtihon (ism TEXT, ball INT);
INSERT INTO imtihon VALUES ('A', 100), ('B', 90), ('C', 90), ('D', 80);

SELECT ism, ball 
FROM imtihon 
ORDER BY ball DESC 
FETCH FIRST 2 ROWS WITH TIES;""",
        "'WITH TIES' - agar chegaradagi oxirgi qator bilan ayni bir xil ORDER BY qiymatiga ega boshqa qatorlar ham bo'lsa, ularni ham natijaga qo'shadi.",
        """ ism | ball 
-----+------
 A   |  100
 B   |   90
 C   |   90
(3 rows)"""
    ),
    (
        192,
        "Katta OFFSET muammosi va Keyset (Seek) Pagination",
        "OFFSET 1000000 juda sekin ishlashi sababli, oxirgi ko'rilgan ID orqali tezkor sahifalash so'rovini yozing.",
        """-- Sekin: SELECT * FROM tovarlar ORDER BY id LIMIT 10 OFFSET 1000000;
-- Tez (Keyset pagination):
SELECT id, nomi, narx 
FROM tovarlar 
WHERE id > 2 
ORDER BY id ASC 
LIMIT 10;""",
        "OFFSET m butun m ta qatorni xotirada o'qib chiqib tashlab yuboradi. Keyset pagination esa B-Tree indeksidan bevosita `WHERE id > oxirgi_id` orqali kerakli joyga sakraydi va doimiy O(1) tezlikda ishlaydi.",
        """ id |      nomi       |    narx     
----+-----------------+-------------
  3 | Lenovo ThinkPad | 11000000.00
(1 row)"""
    ),
    (
        193,
        "Tasodifiy qatorni tanlash: ORDER BY RANDOM()",
        "Foydalanuvchilar orasidan yutuqli o'yin uchun tasodifiy 1 ta g'olibni aniqlang.",
        """SELECT ism 
FROM xodim_royxat 
ORDER BY RANDOM() 
LIMIT 1;""",
        "'ORDER BY RANDOM()' har bir qator uchun tasodifiy son hisoblaydi va ularni saralaydi. Kichik jadvallarda juda qulay, lekin millionlab qatorli jadvallarda og'ir bo'lishi mumkin.",
        """  ism  
-------
 Anvar
(1 row)"""
    ),
    (
        194,
        "Mantiqiy ifodani to'g'ridan-to'g'ri SELECT da ko'rish",
        "Xodimning oyligi 9,000,000 dan kattaligini mantiqiy (true/false) ustun sifatida chiqaring.",
        """SELECT 
    ism, 
    maosh, 
    (maosh > 9000000) AS yuqori_maoshmi 
FROM xodim_royxat;""",
        "SQL da har qanday solishtirish ifodasi mustaqil BOOLEAN natija beradi va uni SELECT proyeksiyasida bevosita ko'rish mumkin.",
        """  ism   |   maosh    | yuqori_maoshmi 
--------+------------+----------------
 Anvar  | 8500000.00 | f
 Malika | 9200000.00 | t
(2 rows)"""
    ),
    (
        195,
        "WHERE da mantiqiy ustunni qisqa yozish",
        "'WHERE mavjud = TRUE' o'rniga toza qisqa relyatsion yozuvni qo'llang.",
        """SELECT nomi 
FROM tovarlar 
WHERE mavjud;""",
        "BOOLEAN ustunlar o'z-o'zidan TRUE yoki FALSE bo'lgani uchun ularni '= TRUE' deb taqqoslash ortiqcha hisoblanadi. Shunchaki 'WHERE mavjud' yoki inkor uchun 'WHERE NOT mavjud' yozish to'g'ri odatdir.",
        """   nomi    
-----------
 Asus ROG
 iPhone 15
(2 rows)"""
    ),
    (
        196,
        "Murakkab saralash: Shartli ORDER BY (CASE WHEN bilan)",
        "Buyurtmalarni saralashda 'shoshilinch' buyurtmalar eng birinchi, qolganlari esa sana bo'yicha chiqsin.",
        """CREATE TABLE navbatlar (id INT, turi TEXT, sana DATE);
INSERT INTO navbatlar VALUES (1, 'oddiy', '2026-03-01'), (2, 'shoshilinch', '2026-03-05'), (3, 'oddiy', '2026-02-20');

SELECT id, turi, sana 
FROM navbatlar 
ORDER BY 
    CASE WHEN turi = 'shoshilinch' THEN 0 ELSE 1 END,
    sana ASC;""",
        "ORDER BY ichida CASE ifodasidan foydalanib o'zimiz istagan biznes ustuvorligi bo'yicha maxsus saralash qoidalarini yaratish mumkin.",
        """ id |    turi     |    sana    
----+-------------+------------
  2 | shoshilinch | 2026-03-05
  3 | oddiy       | 2026-02-20
  1 | oddiy       | 2026-03-01
(3 rows)"""
    ),
    (
        197,
        "WHERE da bir nechta ustunlarni tuple (qator) shaklida solishtirish",
        "Talabaning kursi va guruhi aynan (3, 101) juftligiga mos kelishini tuple sintaksisi bilan tekshiring.",
        """CREATE TABLE talaba_kurs (ism TEXT, kurs INT, guruh INT);
INSERT INTO talaba_kurs VALUES ('Ali', 3, 101), ('Vali', 2, 101), ('Hasan', 3, 102);

SELECT ism 
FROM talaba_kurs 
WHERE (kurs, guruh) = (3, 101);""",
        "Row Constructor (v1, v2) = (c1, c2) ko'p ustunli tekshiruvlarni qisqa va o'qishli qiladi va kompozit indekslar bilan juda samarali ishlaydi.",
        """ ism 
-----
 Ali
(1 row)"""
    ),
    (
        198,
        "WHERE da Tuple IN ro'yxati",
        "Bir nechta juftliklar ro'yxatiga (kurs, guruh) mos talabalarni bitta so'rovda filtrlash.",
        """SELECT ism, kurs, guruh 
FROM talaba_kurs 
WHERE (kurs, guruh) IN ((3, 101), (2, 101));""",
        "Row constructor bilan 'IN ((a,b), (c,d))' murakkab kompozit identifikatorlar bo'yicha ommaviy filtrlashda nihoyatda qulay vositadir.",
        """ ism  | kurs | guruh 
------+------+-------
 Ali  |    3 |   101
 Vali |    2 |   101
(2 rows)"""
    ),
    (
        199,
        "Filtrlashda qat'iy matn mosligi va bo'shliqlar farqi",
        "CHAR(10) va VARCHAR(10) ustunlarida oxiridagi bo'shliqlarni (trailing spaces) solishtirish xulqini ko'ring.",
        """SELECT 
    ('test'::CHAR(10) = 'test'::CHAR(10)) AS char_teng,
    ('test '::VARCHAR = 'test'::VARCHAR) AS varchar_teng;""",
        "CHAR turlari bo'shliqlar bilan to'ldiriladi va solishtirganda oxirgi bo'shliqlar inobatga olinmasligi mumkin. VARCHAR da esa har bir belgi va bo'shliq qat'iy inobatga olinadi.",
        """ char_teng | varchar_teng 
-----------+--------------
 t         | f
(1 row)"""
    ),
    (
        200,
        "Korporativ DQL: E-tijorat qidiruv va filtrlash mexanizmi",
        "Elektron do'konda foydalanuvchi narxlar oralig'ini, mavjudligini, nom qidiruvini kiritganda saralash va sahifalash bilan ishlovchi to'liq qidiruv so'rovini yozing.",
        """SELECT 
    id,
    nomi,
    toifa,
    narx,
    ROUND(narx * 1.12, 2) AS narx_nds_bilan,
    mavjud
FROM tovarlar
WHERE 
    mavjud = TRUE
    AND narx BETWEEN 5000000 AND 20000000
    AND (nomi ILIKE '%asus%' OR nomi ILIKE '%phone%')
ORDER BY narx DESC, nomi ASC
OFFSET 0 ROWS 
FETCH FIRST 10 ROWS ONLY;""",
        "Ushbu so'rov zamonaviy internet-do'konlarning filtrlash dvigatelining yuragidir: aniq ustunlar proyeksiyasi, soliqlar virtual hisobi, bir nechta shartlar birikmasi (AND, BETWEEN, ILIKE), aniq ikki bosqichli tartiblash (ORDER BY) va standart xavfsiz sahifalash (FETCH FIRST).",
        """ id |   nomi   |  toifa   |    narx     | narx_nds_bilan | mavjud 
----+----------+----------+-------------+----------------+--------
  1 | Asus ROG | Noutbuk  | 14000000.00 |    15680000.00 | t
  2 | iPhone 15| Smartfon | 12000000.00 |    13440000.00 | t
(2 rows)"""
    )
]

formatted = [format_task(*item) for item in dql_data]
save_file("sql_04_dql_oddiy_tanlash_select_va_filtrlash.md", formatted)
