# 151-Topshiriq: Aniq ustunlarni tanlash (SELECT Projection)
## Topshiriq sharti:
Xodimlar jadvalidan faqat ularning familiyasi, ismi va elektron pochtasini tanlab oling.

## Yechim (SQL kodi):
```sql
CREATE TABLE xodim_royxat (
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
FROM xodim_royxat;
```

## Tushuntirish va Mantiq:
Relyatsion algebrada bu operatsiya 'Proyeksiyalash' (Projection - π) deb ataladi. Keraksiz ustunlarni (masalan, maosh) o'qimaslik tarmoq yukini kamaytiradi va disk I/O ni sezilarli tejaydi. 'SELECT *' amaliyotda faqat tezkor tahlil uchun ishlatilishi lozim.

## Ishlash natijasi:
```text
ism   | familiya |       email        
--------+----------+--------------------
 Anvar  | Soliyev  | anvar@shirkat.uz
 Malika | Karimova | malika@shirkat.uz
(2 rows)
```


# 152-Topshiriq: Ustunlarga taxallus berish (Column Aliasing: AS)
## Topshiriq sharti:
Xodimning ismini 'Xodim Ismi', maoshini esa 'Oylik Maoshi (so'm)' ko'rinishida sarlavha qilib chiqaring.

## Yechim (SQL kodi):
```sql
SELECT 
    ism AS "Xodim Ismi",
    maosh AS "Oylik Maoshi (so'm)"
FROM xodim_royxat;
```

## Tushuntirish va Mantiq:
'AS' kalit so'zi natijadagi ustun sarlavhasini o'zgartiradi. Agar taxallusda bo'shliq yoki maxsus belgilar bo'lsa, u qo'shtirnoqqa ("...") olinishi shart.

## Ishlash natijasi:
```text
Xodim Ismi | Oylik Maoshi (so'm) 
------------+---------------------
 Anvar      |          8500000.00
 Malika     |          9200000.00
(2 rows)
```


# 153-Topshiriq: Hisoblangan ustunlar va arifmetik amallar
## Topshiriq sharti:
Har bir xodimning maoshidan 12% daromad solig'ini hisoblab, qolgan sof maoshini ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    maosh,
    ROUND(maosh * 0.12, 2) AS daromad_soligi,
    ROUND(maosh * 0.88, 2) AS sof_maosh
FROM xodim_royxat;
```

## Tushuntirish va Mantiq:
SELECT bandida ustunlar ustida arifmetik amallar (+, -, *, /) bajarish mumkin. RDBMS har bir qator uchun ushbu formulani hisoblaydi va natijani virtual ustunda ko'rsatadi.

## Ishlash natijasi:
```text
ism   |   maosh    | daromad_soligi | sof_maosh  
--------+------------+----------------+------------
 Anvar  | 8500000.00 |     1020000.00 | 7480000.00
 Malika | 9200000.00 |     1104000.00 | 8096000.00
(2 rows)
```


# 154-Topshiriq: Matnlarni birlashtirish (String Concatenation: || operatori)
## Topshiriq sharti:
Xodimning ismi va familiyasini bitta ustunga 'Ism Familiya' shaklida birlashtirib chiqaring.

## Yechim (SQL kodi):
```sql
SELECT 
    ism || ' ' || familiya AS toliq_ism,
    email
FROM xodim_royxat;
```

## Tushuntirish va Mantiq:
ANSI SQL va PostgreSQL da '||' operatori satrlarni bir-biriga ulaydi (concatenation). Agar qismlardan biri NULL bo'lsa, natija ham NULL bo'ladi (buning oldini olish uchun CONCAT funksiyasi qo'llanadi).

## Ishlash natijasi:
```text
toliq_ism    |       email        
-----------------+--------------------
 Anvar Soliyev   | anvar@shirkat.uz
 Malika Karimova | malika@shirkat.uz
(2 rows)
```


# 155-Topshiriq: Oddiy WHERE filtri: Tenglik (=) sharti
## Topshiriq sharti:
Mahsulotlar orasidan faqat 'Noutbuk' bo'lganlarini tanlab oling.

## Yechim (SQL kodi):
```sql
CREATE TABLE tovarlar (id INT, nomi TEXT, toifa TEXT, narx NUMERIC, mavjud BOOLEAN);
INSERT INTO tovarlar VALUES 
(1, 'Asus ROG', 'Noutbuk', 14000000, TRUE),
(2, 'iPhone 15', 'Smartfon', 12000000, TRUE),
(3, 'Lenovo ThinkPad', 'Noutbuk', 11000000, FALSE);

SELECT nomi, narx 
FROM tovarlar 
WHERE toifa = 'Noutbuk';
```

## Tushuntirish va Mantiq:
Relyatsion algebrada bu operatsiya 'Tanlash' (Selection - σ) deb ataladi. RDBMS jadvaldagi barcha qatorlarni 'toifa = 'Noutbuk'' predikatiga tekshiradi va faqat TRUE bo'lgan qatorlarni qaytaradi.

## Ishlash natijasi:
```text
nomi       |    narx     
-----------------+-------------
 Asus ROG        | 14000000.00
 Lenovo ThinkPad | 11000000.00
(2 rows)
```


# 156-Topshiriq: Teng emaslik operatorlari: <> va !=
## Topshiriq sharti:
'Smartfon' toifasiga kirmaydigan barcha tovarlarni toping.

## Yechim (SQL kodi):
```sql
SELECT nomi, toifa 
FROM tovarlar 
WHERE toifa <> 'Smartfon';
```

## Tushuntirish va Mantiq:
ANSI SQL standartida teng emaslik '<>' ko'rinishida yoziladi, ko'pchilik RDBMS larda '!=' sintaksisi ham qo'llab-quvvatlanadi. Eslatma: Agar toifa qiymati NULL bo'lsa, u ham ushbu natijaga kirmaydi.

## Ishlash natijasi:
```text
nomi       |  toifa  
-----------------+---------
 Asus ROG        | Noutbuk
 Lenovo ThinkPad | Noutbuk
(2 rows)
```


# 157-Topshiriq: Katta va kichik operatorlari: >, <, >=, <=
## Topshiriq sharti:
Narxi 12,000,000 so'mdan arzon yoki unga teng bo'lgan tovarlarni aniqlang.

## Yechim (SQL kodi):
```sql
SELECT nomi, narx 
FROM tovarlar 
WHERE narx <= 12000000;
```

## Tushuntirish va Mantiq:
Taqqoslash operatorlari sonlar, sanalar va hatto alifbo tartibida satrlar ustida ham ishlaydi.

## Ishlash natijasi:
```text
nomi       |    narx     
-----------------+-------------
 iPhone 15       | 12000000.00
 Lenovo ThinkPad | 11000000.00
(2 rows)
```


# 158-Topshiriq: Mantiqiy AND operatori (Ikkala shart bir vaqtda bajarilishi)
## Topshiriq sharti:
Noutbuk bo'lgan VA ayni paytda omborda mavjud (mavjud = TRUE) tovarlarni toping.

## Yechim (SQL kodi):
```sql
SELECT nomi, toifa, narx 
FROM tovarlar 
WHERE toifa = 'Noutbuk' AND mavjud = TRUE;
```

## Tushuntirish va Mantiq:
'AND' operatori faqatgina har ikkala mantiqiy ifoda ham TRUE bo'lgandagina natijani qaytaradi.

## Ishlash natijasi:
```text
nomi   |  toifa  |    narx     
----------+---------+-------------
 Asus ROG | Noutbuk | 14000000.00
(1 row)
```


# 159-Topshiriq: Mantiqiy OR operatori (Kamida bitta shart bajarilishi)
## Topshiriq sharti:
Toifasi 'Smartfon' bo'lgan YOKI narxi 13,000,000 so'mdan oshadigan tovarlarni chiqaring.

## Yechim (SQL kodi):
```sql
SELECT nomi, toifa, narx 
FROM tovarlar 
WHERE toifa = 'Smartfon' OR narx > 13000000;
```

## Tushuntirish va Mantiq:
'OR' operatori ifodalardan kamida bittasi qanoatlantirilganda qatorni natijaga qo'shadi.

## Ishlash natijasi:
```text
nomi    |  toifa   |    narx     
-----------+----------+-------------
 Asus ROG  | Noutbuk  | 14000000.00
 iPhone 15 | Smartfon | 12000000.00
(2 rows)
```


# 160-Topshiriq: Operatorlar ustuvorligi va qavslar ahamiyati
## Topshiriq sharti:
AND operatori OR dan oldin bajarilishi sababli qavslardan foydalanish qoidasini ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT nomi, toifa, narx, mavjud 
FROM tovarlar 
WHERE (toifa = 'Noutbuk' OR toifa = 'Smartfon') AND mavjud = TRUE;
```

## Tushuntirish va Mantiq:
SQL da 'AND' ning ustuvorligi (precedence) 'OR' ga qaraganda yuqori. Qavslar qo'yilmasa, so'rov `toifa = 'Noutbuk' OR (toifa = 'Smartfon' AND mavjud = TRUE)` deb noto'g'ri talqin qilinadi.

## Ishlash natijasi:
```text
nomi    |  toifa   |    narx     | mavjud 
-----------+----------+-------------+--------
 Asus ROG  | Noutbuk  | 14000000.00 | t
 iPhone 15 | Smartfon | 12000000.00 | t
(2 rows)
```


# 161-Topshiriq: Oraliqni filtrlash: BETWEEN ... AND ...
## Topshiriq sharti:
Narxi 10,000,000 dan 13,000,000 so'mgacha bo'lgan tovarlarni aniqlang.

## Yechim (SQL kodi):
```sql
SELECT nomi, narx 
FROM tovarlar 
WHERE narx BETWEEN 10000000 AND 13000000;
```

## Tushuntirish va Mantiq:
'BETWEEN a AND b' chegaralarni ham o'z ichiga oladi (`narx >= a AND narx <= b` ifodasi bilan aynan bir xil).

## Ishlash natijasi:
```text
nomi       |    narx     
-----------------+-------------
 iPhone 15       | 12000000.00
 Lenovo ThinkPad | 11000000.00
(2 rows)
```


# 162-Topshiriq: Oraliqdan tashqarini tanlash: NOT BETWEEN
## Topshiriq sharti:
O'rtacha narxlar oralig'iga (11M dan 13M gacha) kirmaydigan arzon yoki qimmat mahsulotlarni toping.

## Yechim (SQL kodi):
```sql
SELECT nomi, narx 
FROM tovarlar 
WHERE narx NOT BETWEEN 11000000 AND 13000000;
```

## Tushuntirish va Mantiq:
'NOT BETWEEN' belgilangan diapazondan tashqaridagi qiymatlarni (`narx < a OR narx > b`) filtrlaydi.

## Ishlash natijasi:
```text
nomi   |    narx     
----------+-------------
 Asus ROG | 14000000.00
(1 row)
```


# 163-Topshiriq: Sanalar oralig'ida BETWEEN filtri
## Topshiriq sharti:
2026-yil 1-yanvardan 2026-yil 31-yanvargacha berilgan buyurtmalarni saralash.

## Yechim (SQL kodi):
```sql
CREATE TABLE s_buyurtmalar (id INT, summa NUMERIC, sana DATE);
INSERT INTO s_buyurtmalar VALUES 
(1, 150000, '2026-01-10'), (2, 250000, '2026-01-25'), (3, 80000, '2026-02-05');

SELECT id, summa, sana 
FROM s_buyurtmalar 
WHERE sana BETWEEN '2026-01-01' AND '2026-01-31';
```

## Tushuntirish va Mantiq:
Sana turlari bilan BETWEEN ishlatilganda chegaralar kiritiladi. Eslatma: TIMESTAMPTZ bilan ishlaganda oxirgi kunning '23:59:59' qismiga e'tibor qaratish kerak.

## Ishlash natijasi:
```text
id |   summa   |    sana    
----+-----------+------------
  1 | 150000.00 | 2026-01-10
  2 | 250000.00 | 2026-01-25
(2 rows)
```


# 164-Topshiriq: Ro'yxat bo'yicha filtrlash: IN operatori
## Topshiriq sharti:
ID raqami 1, 3 yoki 7 bo'lgan mahsulotlarni bitta ixcham so'rovda oling.

## Yechim (SQL kodi):
```sql
SELECT id, nomi, narx 
FROM tovarlar 
WHERE id IN (1, 3, 7);
```

## Tushuntirish va Mantiq:
'IN (v1, v2, ...)' operatori `id = 1 OR id = 3 OR id = 7` yozuvining qisqa va qulay shaklidir. RDBMS ichida u ko'pincha B-Tree indeksida tezkor skanerlashga aylanadi.

## Ishlash natijasi:
```text
id |      nomi       |    narx     
----+-----------------+-------------
  1 | Asus ROG        | 14000000.00
  3 | Lenovo ThinkPad | 11000000.00
(2 rows)
```


# 165-Topshiriq: Ro'yxatda mavjud bo'lmaganlarni tanlash: NOT IN
## Topshiriq sharti:
Toifasi 'Smartfon' yoki 'Planshet' bo'lmagan barcha boshqa tovarlarni chiqaring.

## Yechim (SQL kodi):
```sql
SELECT nomi, toifa 
FROM tovarlar 
WHERE toifa NOT IN ('Smartfon', 'Planshet');
```

## Tushuntirish va Mantiq:
'NOT IN' ko'rsatilgan to'plamdagi hech bir elementga teng bo'lmagan qatorlarni qaytaradi.

## Ishlash natijasi:
```text
nomi       |  toifa  
-----------------+---------
 Asus ROG        | Noutbuk
 Lenovo ThinkPad | Noutbuk
(2 rows)
```


# 166-Topshiriq: NOT IN va NULL qiymat tuzog'i
## Topshiriq sharti:
Agar NOT IN ro'yxatida bitta bo'lsa ham NULL qiymat uchrasa nima bo'lishini ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT nomi 
FROM tovarlar 
WHERE toifa NOT IN ('Smartfon', NULL);
```

## Tushuntirish va Mantiq:
SQL ning uch qiymatli mantiqiy modelida (3-valued logic: TRUE, FALSE, UNKNOWN), `x NOT IN ('Smartfon', NULL)` ifodasi `x <> 'Smartfon' AND x <> NULL` ga aylanadi. `x <> NULL` har doim UNKNOWN bo'lgani sababli butun ifoda UNKNOWN bo'lib qoladi va natija BO'SH (0 qator) chiqadi!

## Ishlash natijasi:
```text
nomi 
------
(0 rows)
```


# 167-Topshiriq: Bo'sh qiymatlarni tekshirish: IS NULL
## Topshiriq sharti:
Mijozlar orasidan elektron pochtasi kiritilmagan (NULL bo'lgan) foydalanuvchilarni toping.

## Yechim (SQL kodi):
```sql
CREATE TABLE mijoz_baza (id INT, ism TEXT, email TEXT);
INSERT INTO mijoz_baza VALUES (1, 'Alisher', NULL), (2, 'Bobur', 'bobur@mail.uz');

SELECT ism 
FROM mijoz_baza 
WHERE email IS NULL;
```

## Tushuntirish va Mantiq:
SQL da 'email = NULL' deb yozish xatodir, chunki hech narsa NULL ga teng bo'lolmaydi. NULL bor-yo'qligi faqat 'IS NULL' operatori orqali tekshiriladi.

## Ishlash natijasi:
```text
ism   
---------
 Alisher
(1 row)
```


# 168-Topshiriq: Bo'sh bo'lmagan qiymatlarni aniqlash: IS NOT NULL
## Topshiriq sharti:
Faqat rasmiy e-maili tasdiqlangan va mavjud mijozlarni saralang.

## Yechim (SQL kodi):
```sql
SELECT ism, email 
FROM mijoz_baza 
WHERE email IS NOT NULL;
```

## Tushuntirish va Mantiq:
'IS NOT NULL' ustunda haqiqiy qiymat mavjud bo'lgan qatorlarni ajratib beradi.

## Ishlash natijasi:
```text
ism  |     email     
-------+---------------
 Bobur | bobur@mail.uz
(1 row)
```


# 169-Topshiriq: NULL-safe tenglik: IS NOT DISTINCT FROM
## Topshiriq sharti:
Ikki qiymatni, hattoki ularning ikkalasi ham NULL bo'lgan taqdirda ularni 'teng' deb hisoblovchi operatorni ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT 
    (NULL = NULL) AS oddiy_tenglik,
    (NULL IS NOT DISTINCT FROM NULL) AS xavfsiz_tenglik;
```

## Tushuntirish va Mantiq:
'IS NOT DISTINCT FROM' NULL qiymatlarni ham bir-biriga teng deb biladi. Bu tashqi so'rovlarda va murakkab JOIN shartlarida NULL larni xatosiz taqqoslashda juda zarur.

## Ishlash natijasi:
```text
oddiy_tenglik | xavfsiz_tenglik 
---------------+-----------------
 NULL          | t
(1 row)
```


# 170-Topshiriq: Shablon bo'yicha qidirish: LIKE va % belgisi
## Topshiriq sharti:
Nomi 'Asus' so'zi bilan boshlanadigan barcha tovarlarni toping.

## Yechim (SQL kodi):
```sql
SELECT nomi, narx 
FROM tovarlar 
WHERE nomi LIKE 'Asus%';
```

## Tushuntirish va Mantiq:
'%' belgisi ixtiyoriy sondagi (0 yoki undan ortiq) belgilarni ifodalaydi. 'Asus%' - 'Asus' bilan boshlanuvchi barcha satrlarni topadi.

## Ishlash natijasi:
```text
nomi   |    narx     
----------+-------------
 Asus ROG | 14000000.00
(1 row)
```


# 171-Topshiriq: Satrning istalgan joyida so'zni qidirish (%so'z%)
## Topshiriq sharti:
Nomi tarkibida 'Pad' so'zi uchraydigan mahsulotlarni aniqlang.

## Yechim (SQL kodi):
```sql
SELECT nomi 
FROM tovarlar 
WHERE nomi LIKE '%Pad%';
```

## Tushuntirish va Mantiq:
'%so'z%' shabloni qidirilayotgan satr qatorning boshi, o'rtasi yoki oxirida uchrashidan qat'i nazar topadi.

## Ishlash natijasi:
```text
nomi       
-----------------
 Lenovo ThinkPad
(1 row)
```


# 172-Topshiriq: Yagona belgini almashtiruvchi pastki chiziq: LIKE va _
## Topshiriq sharti:
Telefon modeli aynan 4 ta belgidan iborat va oxiri '0' bilan tugaydigan mahsulotlarni toping.

## Yechim (SQL kodi):
```sql
CREATE TABLE modellar (kod VARCHAR(10));
INSERT INTO modellar VALUES ('A100'), ('B20'), ('X500'), ('M10');

SELECT kod 
FROM modellar 
WHERE kod LIKE '__00';
```

## Tushuntirish va Mantiq:
'_' (underscore) belgisi aynan 1 ta ixtiyoriy belgini ifodalaydi. '__00' aynan 4 ta belgidan iborat va oxiri '00' bilan tugagan kodlarni filtrlaydi.

## Ishlash natijasi:
```text
kod  
------
 A100
 X500
(2 rows)
```


# 173-Topshiriq: Katta-kichik harfni inobatga olmaydigan qidiruv: ILIKE
## Topshiriq sharti:
Foydalanuvchi qidiruv maydoniga 'asus', 'ASUS' yoki 'AsUs' deb yozganidan qat'i nazar to'g'ri topuvchi ILIKE so'rovini yozing.

## Yechim (SQL kodi):
```sql
SELECT nomi 
FROM tovarlar 
WHERE nomi ILIKE 'asus%';
```

## Tushuntirish va Mantiq:
'ILIKE' PostgreSQL ning xususiy kengaytmasi bo'lib, registrga sezgir bo'lmagan (case-insensitive) LIKE amalini bajaradi. Standart SQL da buning uchun `WHERE LOWER(nomi) LIKE LOWER('asus%')` yoziladi.

## Ishlash natijasi:
```text
nomi   
----------
 Asus ROG
(1 row)
```


# 174-Topshiriq: Shablondan tashqarini topish: NOT LIKE va NOT ILIKE
## Topshiriq sharti:
Elektron pochta domeni '@gmail.com' bilan tugamaydigan korporativ foydalanuvchilarni aniqlang.

## Yechim (SQL kodi):
```sql
SELECT ism, email 
FROM xodim_royxat 
WHERE email NOT LIKE '%@gmail.com';
```

## Tushuntirish va Mantiq:
'NOT LIKE' shablonga mos kelmagan barcha satrlarni qaytaradi.

## Ishlash natijasi:
```text
ism   |       email        
--------+--------------------
 Anvar  | anvar@shirkat.uz
 Malika | malika@shirkat.uz
(2 rows)
```


# 175-Topshiriq: Maxsus belgilarni ekranlash (ESCAPE bandi)
## Topshiriq sharti:
Matn ichidagi haqiqiy '%' belgisini qidirish (masalan: '10%' chegirma).

## Yechim (SQL kodi):
```sql
CREATE TABLE aksiyalar (matn TEXT);
INSERT INTO aksiyalar VALUES ('Chegirma 10% gacha'), ('Oddiy xabar');

SELECT matn 
FROM aksiyalar 
WHERE matn LIKE '%10\%%' ESCAPE '';
```

## Tushuntirish va Mantiq:
'ESCAPE' bandi qidiruv shablonidagi maxsus belgini (masalan '%') o'zining asl ma'nosida qabul qilinishini ta'minlaydi.

## Ishlash natijasi:
```text
matn        
--------------------
 Chegirma 10% gacha
(1 row)
```


# 176-Topshiriq: Muntazam ifodalar (RegEx) bilan filtrlash: ~ operatori
## Topshiriq sharti:
Nomida faqat raqamlar bilan boshlanadigan modellarni POSIX RegEx (~) orqali saralang.

## Yechim (SQL kodi):
```sql
SELECT kod 
FROM modellar 
WHERE kod ~ '^[A-Z][0-9]+';
```

## Tushuntirish va Mantiq:
PostgreSQL da '~' operatori to'liq POSIX muntazam ifodalarini qo'llab-quvvatlaydi. Bu yerda bosh harf bilan boshlanib, ketidan raqam keluvchi qatorlar filtrlanadi.

## Ishlash natijasi:
```text
kod  
------
 A100
 B20
 X500
 M10
(4 rows)
```


# 177-Topshiriq: Registrga sezgir bo'lmagan RegEx: ~* operatori
## Topshiriq sharti:
Matnda 'pro' yoki 'max' so'zlari katta-kichikligidan qat'i nazar borligini tekshirish.

## Yechim (SQL kodi):
```sql
CREATE TABLE gadjetlar (nomi TEXT);
INSERT INTO gadjetlar VALUES ('iPhone 15 Pro'), ('MacBook MAX'), ('Redmi Note');

SELECT nomi 
FROM gadjetlar 
WHERE nomi ~* '(pro|max)';
```

## Tushuntirish va Mantiq:
'~*' operatori case-insensitive RegEx tekshiruvini amalga oshiradi. '|' esa 'yoki' amalini bajaradi.

## Ishlash natijasi:
```text
nomi      
---------------
 iPhone 15 Pro
 MacBook MAX
(2 rows)
```


# 178-Topshiriq: Takrorlanishlarni yo'qotish: DISTINCT
## Topshiriq sharti:
Jadvalda qanday toifalar mavjudligini takrorlanishlarsiz yagona ro'yxat sifatida chiqaring.

## Yechim (SQL kodi):
```sql
SELECT DISTINCT toifa 
FROM tovarlar;
```

## Tushuntirish va Mantiq:
'DISTINCT' so'rovi barcha takrorlanuvchi qatorlarni filtrlash uchun natijani vaqtincha xotirada (WorkMem) saralaydi yoki hash-jadval (HashAggregate) tuzadi.

## Ishlash natijasi:
```text
toifa   
----------
 Noutbuk
 Smartfon
(2 rows)
```


# 179-Topshiriq: Bir nechta ustun bo'yicha DISTINCT
## Topshiriq sharti:
Mijoz va to'lov usuli kombinatsiyasining noyob juftliklarini oling.

## Yechim (SQL kodi):
```sql
CREATE TABLE tolov_log (mijoz TEXT, usul TEXT);
INSERT INTO tolov_log VALUES ('Ali', 'karta'), ('Ali', 'karta'), ('Ali', 'naqd'), ('Vali', 'karta');

SELECT DISTINCT mijoz, usul 
FROM tolov_log;
```

## Tushuntirish va Mantiq:
Ko'p ustunli DISTINCT da har ikkala ustun bir vaqtda bir xil bo'lgan qatorlar olib tashlanadi.

## Ishlash natijasi:
```text
mijoz | usul  
-------+-------
 Ali   | karta
 Ali   | naqd
 Vali  | karta
(3 rows)
```


# 180-Topshiriq: PostgreSQL maxsus imkoniyati: DISTINCT ON (ustun)
## Topshiriq sharti:
Har bir mijozning eng oxirgi amalga oshirgan to'lovini bitta so'rovda oling.

## Yechim (SQL kodi):
```sql
CREATE TABLE tranzaksiyalar_vaqt (id INT, mijoz TEXT, summa NUMERIC, vaqt TIMESTAMP);
INSERT INTO tranzaksiyalar_vaqt VALUES 
(1, 'Ali', 10000, '2026-03-01 10:00'),
(2, 'Ali', 50000, '2026-03-01 12:00'),
(3, 'Vali', 30000, '2026-03-01 11:00');

SELECT DISTINCT ON (mijoz) mijoz, summa, vaqt 
FROM tranzaksiyalar_vaqt 
ORDER BY mijoz, vaqt DESC;
```

## Tushuntirish va Mantiq:
'DISTINCT ON (ustun)' berilgan ustun bo'yicha guruhlaydi va ORDER BY tartibiga ko'ra birinchi uchragan qatorni saqlab qoladi. Guruh bo'yicha eng oxirgi yoki eng katta qiymatni olishda eng tezkor usuldir.

## Ishlash natijasi:
```text
mijoz |  summa   |        vaqt         
-------+----------+---------------------
 Ali   | 50000.00 | 2026-03-01 12:00:00
 Vali  | 30000.00 | 2026-03-01 11:00:00
(2 rows)
```


# 181-Topshiriq: Natijalarni o'sish tartibida saralash: ORDER BY ASC
## Topshiriq sharti:
Mahsulotlarni ularning narxi bo'yicha eng arzonidan eng qimmatiga qarab saralab ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT nomi, narx 
FROM tovarlar 
ORDER BY narx ASC;
```

## Tushuntirish va Mantiq:
'ORDER BY narx ASC' natijani kichikdan kattaga qarab saralaydi. 'ASC' ko'rsatilmasa ham sukut bo'yicha qabul qilinadi.

## Ishlash natijasi:
```text
nomi       |    narx     
-----------------+-------------
 Lenovo ThinkPad | 11000000.00
 iPhone 15       | 12000000.00
 Asus ROG        | 14000000.00
(3 rows)
```


# 182-Topshiriq: Natijalarni kamayish tartibida saralash: ORDER BY DESC
## Topshiriq sharti:
Xodimlarni eng yuqori maosh oluvchidan boshlab saralash.

## Yechim (SQL kodi):
```sql
SELECT ism, maosh 
FROM xodim_royxat 
ORDER BY maosh DESC;
```

## Tushuntirish va Mantiq:
'DESC' (descending) eng katta qiymatdan eng kichigiga qarab saralaydi.

## Ishlash natijasi:
```text
ism   |   maosh    
--------+------------
 Malika | 9200000.00
 Anvar  | 8500000.00
(2 rows)
```


# 183-Topshiriq: Bir nechta ustun bo'yicha tartiblash
## Topshiriq sharti:
Avval toifa bo'yicha alifbo tartibida, so'ngra bir xil toifa ichida narx bo'yicha qimmatidan arzoniga qarab saralang.

## Yechim (SQL kodi):
```sql
SELECT toifa, nomi, narx 
FROM tovarlar 
ORDER BY toifa ASC, narx DESC;
```

## Tushuntirish va Mantiq:
RDBMS avval 1-ustun bo'yicha saralaydi. Agar 1-ustun qiymatlari teng bo'lsa, 2-ustun bo'yicha taqqoslashga o'tadi.

## Ishlash natijasi:
```text
toifa   |      nomi       |    narx     
----------+-----------------+-------------
 Noutbuk  | Asus ROG        | 14000000.00
 Noutbuk  | Lenovo ThinkPad | 11000000.00
 Smartfon | iPhone 15       | 12000000.00
(3 rows)
```


# 184-Topshiriq: Ustun o'rni raqami bilan saralash (ORDER BY 1, 2)
## Topshiriq sharti:
Ustun nomlarini qayta yozmasdan ularning SELECT dagi tartib raqami orqali saralash.

## Yechim (SQL kodi):
```sql
SELECT toifa, nomi, narx 
FROM tovarlar 
ORDER BY 1, 3 DESC;
```

## Tushuntirish va Mantiq:
'ORDER BY 1, 3 DESC' birinchi ustun (toifa) va uchinchi ustun (narx) bo'yicha saralashni bildiradi.

## Ishlash natijasi:
```text
toifa   |      nomi       |    narx     
----------+-----------------+-------------
 Noutbuk  | Asus ROG        | 14000000.00
 Noutbuk  | Lenovo ThinkPad | 11000000.00
 Smartfon | iPhone 15       | 12000000.00
(3 rows)
```


# 185-Topshiriq: NULL qiymatlarni saralashda boshqarish: NULLS FIRST
## Topshiriq sharti:
Saralashda qiymati bo'sh (NULL) bo'lgan qatorlar eng boshida chiqishini ta'minlang.

## Yechim (SQL kodi):
```sql
CREATE TABLE reyting (ism TEXT, ball INT);
INSERT INTO reyting VALUES ('Ali', 85), ('Vali', NULL), ('Gani', 95);

SELECT ism, ball 
FROM reyting 
ORDER BY ball ASC NULLS FIRST;
```

## Tushuntirish va Mantiq:
'NULLS FIRST' bandi bo'sh qiymatlarni barcha sonlardan kichik deb baholab, ro'yxatning eng boshiga joylashtiradi.

## Ishlash natijasi:
```text
ism  | ball 
------+------
 Vali | NULL
 Ali  |   85
 Gani |   95
(3 rows)
```


# 186-Topshiriq: NULL qiymatlarni eng oxiriga surish: NULLS LAST
## Topshiriq sharti:
Kamayish tartibida saralaganda NULL lar birinchi chiqib qolmasligi uchun NULLS LAST dan foydalaning.

## Yechim (SQL kodi):
```sql
SELECT ism, ball 
FROM reyting 
ORDER BY ball DESC NULLS LAST;
```

## Tushuntirish va Mantiq:
PostgreSQL da odatda DESC tartibida NULL qiymatlar boshida keladi. 'NULLS LAST' ularni jadvalning eng quyi qismiga surib beradi.

## Ishlash natijasi:
```text
ism  | ball 
------+------
 Gani |   95
 Ali  |   85
 Vali | NULL
(3 rows)
```


# 187-Topshiriq: Ifodalar bo'yicha saralash (ORDER BY Expression)
## Topshiriq sharti:
Talabalarni ularning ism uzunligi (LENGTH) bo'yicha saralash.

## Yechim (SQL kodi):
```sql
SELECT ism 
FROM xodim_royxat 
ORDER BY LENGTH(ism) ASC;
```

## Tushuntirish va Mantiq:
ORDER BY bandiga ustun nomidan tashqari ixtiyoriy SQL funksiyalari va formulalarini qo'yish mumkin.

## Ishlash natijasi:
```text
ism   
--------
 Anvar
 Malika
(2 rows)
```


# 188-Topshiriq: Natijalar sonini cheklash: LIMIT
## Topshiriq sharti:
Tizimdagi eng qimmat bitta tovar ma'lumotini oling.

## Yechim (SQL kodi):
```sql
SELECT nomi, narx 
FROM tovarlar 
ORDER BY narx DESC 
LIMIT 1;
```

## Tushuntirish va Mantiq:
'LIMIT n' qidiruv natijalarining faqat dastlabki n tasini qaytaradi. LIMIT doimo ORDER BY bilan birga ishlatilishi shart, aks holda natija tasodifiy bo'lib qoladi.

## Ishlash natijasi:
```text
nomi   |    narx     
----------+-------------
 Asus ROG | 14000000.00
(1 row)
```


# 189-Topshiriq: Sahifalash (Pagination): LIMIT va OFFSET
## Topshiriq sharti:
Har bir sahifada 2 tadan tovar ko'rsatilganda, 2-sahifadagi tovarlarni chiqarish so'rovini yozing.

## Yechim (SQL kodi):
```sql
SELECT nomi, narx 
FROM tovarlar 
ORDER BY id 
LIMIT 2 OFFSET 2;
```

## Tushuntirish va Mantiq:
'OFFSET m' dastlabki m ta qatorni tashlab yuboradi, 'LIMIT n' esa undan keyingi n ta qatorni oladi. 2-sahifa formulasi: `OFFSET (sahifa_raqami - 1) * sahifa_hajmi`.

## Ishlash natijasi:
```text
nomi       |    narx     
-----------------+-------------
 Lenovo ThinkPad | 11000000.00
(1 row)
```


# 190-Topshiriq: Standart SQL sahifalash: FETCH FIRST ... ROWS ONLY
## Topshiriq sharti:
LIMIT o'rniga zamonaviy ANSI SQL:2008 standartidagi FETCH kalit so'zini qo'llang.

## Yechim (SQL kodi):
```sql
SELECT nomi, narx 
FROM tovarlar 
ORDER BY narx DESC 
OFFSET 0 ROWS 
FETCH FIRST 2 ROWS ONLY;
```

## Tushuntirish va Mantiq:
'OFFSET ... FETCH FIRST ...' barcha asosiy ma'lumotlar bazalarida (PostgreSQL, Oracle, MS SQL Server, DB2) birdek ishlaydigan standartlashtirilgan sintaksisdir.

## Ishlash natijasi:
```text
nomi    |    narx     
-----------+-------------
 Asus ROG  | 14000000.00
 iPhone 15 | 12000000.00
(2 rows)
```


# 191-Topshiriq: Teng qiymatlarni ham qamrab oluvchi FETCH WITH TIES
## Topshiriq sharti:
Top-2 talabani tanlaganda, 2-o'rindagi talaba bilan bir xil ball to'plagan boshqa talabalarni ham qoldirmasdan olish.

## Yechim (SQL kodi):
```sql
CREATE TABLE imtihon (ism TEXT, ball INT);
INSERT INTO imtihon VALUES ('A', 100), ('B', 90), ('C', 90), ('D', 80);

SELECT ism, ball 
FROM imtihon 
ORDER BY ball DESC 
FETCH FIRST 2 ROWS WITH TIES;
```

## Tushuntirish va Mantiq:
'WITH TIES' - agar chegaradagi oxirgi qator bilan ayni bir xil ORDER BY qiymatiga ega boshqa qatorlar ham bo'lsa, ularni ham natijaga qo'shadi.

## Ishlash natijasi:
```text
ism | ball 
-----+------
 A   |  100
 B   |   90
 C   |   90
(3 rows)
```


# 192-Topshiriq: Katta OFFSET muammosi va Keyset (Seek) Pagination
## Topshiriq sharti:
OFFSET 1000000 juda sekin ishlashi sababli, oxirgi ko'rilgan ID orqali tezkor sahifalash so'rovini yozing.

## Yechim (SQL kodi):
```sql
-- Sekin: SELECT * FROM tovarlar ORDER BY id LIMIT 10 OFFSET 1000000;
-- Tez (Keyset pagination):
SELECT id, nomi, narx 
FROM tovarlar 
WHERE id > 2 
ORDER BY id ASC 
LIMIT 10;
```

## Tushuntirish va Mantiq:
OFFSET m butun m ta qatorni xotirada o'qib chiqib tashlab yuboradi. Keyset pagination esa B-Tree indeksidan bevosita `WHERE id > oxirgi_id` orqali kerakli joyga sakraydi va doimiy O(1) tezlikda ishlaydi.

## Ishlash natijasi:
```text
id |      nomi       |    narx     
----+-----------------+-------------
  3 | Lenovo ThinkPad | 11000000.00
(1 row)
```


# 193-Topshiriq: Tasodifiy qatorni tanlash: ORDER BY RANDOM()
## Topshiriq sharti:
Foydalanuvchilar orasidan yutuqli o'yin uchun tasodifiy 1 ta g'olibni aniqlang.

## Yechim (SQL kodi):
```sql
SELECT ism 
FROM xodim_royxat 
ORDER BY RANDOM() 
LIMIT 1;
```

## Tushuntirish va Mantiq:
'ORDER BY RANDOM()' har bir qator uchun tasodifiy son hisoblaydi va ularni saralaydi. Kichik jadvallarda juda qulay, lekin millionlab qatorli jadvallarda og'ir bo'lishi mumkin.

## Ishlash natijasi:
```text
ism  
-------
 Anvar
(1 row)
```


# 194-Topshiriq: Mantiqiy ifodani to'g'ridan-to'g'ri SELECT da ko'rish
## Topshiriq sharti:
Xodimning oyligi 9,000,000 dan kattaligini mantiqiy (true/false) ustun sifatida chiqaring.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, 
    maosh, 
    (maosh > 9000000) AS yuqori_maoshmi 
FROM xodim_royxat;
```

## Tushuntirish va Mantiq:
SQL da har qanday solishtirish ifodasi mustaqil BOOLEAN natija beradi va uni SELECT proyeksiyasida bevosita ko'rish mumkin.

## Ishlash natijasi:
```text
ism   |   maosh    | yuqori_maoshmi 
--------+------------+----------------
 Anvar  | 8500000.00 | f
 Malika | 9200000.00 | t
(2 rows)
```


# 195-Topshiriq: WHERE da mantiqiy ustunni qisqa yozish
## Topshiriq sharti:
'WHERE mavjud = TRUE' o'rniga toza qisqa relyatsion yozuvni qo'llang.

## Yechim (SQL kodi):
```sql
SELECT nomi 
FROM tovarlar 
WHERE mavjud;
```

## Tushuntirish va Mantiq:
BOOLEAN ustunlar o'z-o'zidan TRUE yoki FALSE bo'lgani uchun ularni '= TRUE' deb taqqoslash ortiqcha hisoblanadi. Shunchaki 'WHERE mavjud' yoki inkor uchun 'WHERE NOT mavjud' yozish to'g'ri odatdir.

## Ishlash natijasi:
```text
nomi    
-----------
 Asus ROG
 iPhone 15
(2 rows)
```


# 196-Topshiriq: Murakkab saralash: Shartli ORDER BY (CASE WHEN bilan)
## Topshiriq sharti:
Buyurtmalarni saralashda 'shoshilinch' buyurtmalar eng birinchi, qolganlari esa sana bo'yicha chiqsin.

## Yechim (SQL kodi):
```sql
CREATE TABLE navbatlar (id INT, turi TEXT, sana DATE);
INSERT INTO navbatlar VALUES (1, 'oddiy', '2026-03-01'), (2, 'shoshilinch', '2026-03-05'), (3, 'oddiy', '2026-02-20');

SELECT id, turi, sana 
FROM navbatlar 
ORDER BY 
    CASE WHEN turi = 'shoshilinch' THEN 0 ELSE 1 END,
    sana ASC;
```

## Tushuntirish va Mantiq:
ORDER BY ichida CASE ifodasidan foydalanib o'zimiz istagan biznes ustuvorligi bo'yicha maxsus saralash qoidalarini yaratish mumkin.

## Ishlash natijasi:
```text
id |    turi     |    sana    
----+-------------+------------
  2 | shoshilinch | 2026-03-05
  3 | oddiy       | 2026-02-20
  1 | oddiy       | 2026-03-01
(3 rows)
```


# 197-Topshiriq: WHERE da bir nechta ustunlarni tuple (qator) shaklida solishtirish
## Topshiriq sharti:
Talabaning kursi va guruhi aynan (3, 101) juftligiga mos kelishini tuple sintaksisi bilan tekshiring.

## Yechim (SQL kodi):
```sql
CREATE TABLE talaba_kurs (ism TEXT, kurs INT, guruh INT);
INSERT INTO talaba_kurs VALUES ('Ali', 3, 101), ('Vali', 2, 101), ('Hasan', 3, 102);

SELECT ism 
FROM talaba_kurs 
WHERE (kurs, guruh) = (3, 101);
```

## Tushuntirish va Mantiq:
Row Constructor (v1, v2) = (c1, c2) ko'p ustunli tekshiruvlarni qisqa va o'qishli qiladi va kompozit indekslar bilan juda samarali ishlaydi.

## Ishlash natijasi:
```text
ism 
-----
 Ali
(1 row)
```


# 198-Topshiriq: WHERE da Tuple IN ro'yxati
## Topshiriq sharti:
Bir nechta juftliklar ro'yxatiga (kurs, guruh) mos talabalarni bitta so'rovda filtrlash.

## Yechim (SQL kodi):
```sql
SELECT ism, kurs, guruh 
FROM talaba_kurs 
WHERE (kurs, guruh) IN ((3, 101), (2, 101));
```

## Tushuntirish va Mantiq:
Row constructor bilan 'IN ((a,b), (c,d))' murakkab kompozit identifikatorlar bo'yicha ommaviy filtrlashda nihoyatda qulay vositadir.

## Ishlash natijasi:
```text
ism  | kurs | guruh 
------+------+-------
 Ali  |    3 |   101
 Vali |    2 |   101
(2 rows)
```


# 199-Topshiriq: Filtrlashda qat'iy matn mosligi va bo'shliqlar farqi
## Topshiriq sharti:
CHAR(10) va VARCHAR(10) ustunlarida oxiridagi bo'shliqlarni (trailing spaces) solishtirish xulqini ko'ring.

## Yechim (SQL kodi):
```sql
SELECT 
    ('test'::CHAR(10) = 'test'::CHAR(10)) AS char_teng,
    ('test '::VARCHAR = 'test'::VARCHAR) AS varchar_teng;
```

## Tushuntirish va Mantiq:
CHAR turlari bo'shliqlar bilan to'ldiriladi va solishtirganda oxirgi bo'shliqlar inobatga olinmasligi mumkin. VARCHAR da esa har bir belgi va bo'shliq qat'iy inobatga olinadi.

## Ishlash natijasi:
```text
char_teng | varchar_teng 
-----------+--------------
 t         | f
(1 row)
```


# 200-Topshiriq: Korporativ DQL: E-tijorat qidiruv va filtrlash mexanizmi
## Topshiriq sharti:
Elektron do'konda foydalanuvchi narxlar oralig'ini, mavjudligini, nom qidiruvini kiritganda saralash va sahifalash bilan ishlovchi to'liq qidiruv so'rovini yozing.

## Yechim (SQL kodi):
```sql
SELECT 
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
FETCH FIRST 10 ROWS ONLY;
```

## Tushuntirish va Mantiq:
Ushbu so'rov zamonaviy internet-do'konlarning filtrlash dvigatelining yuragidir: aniq ustunlar proyeksiyasi, soliqlar virtual hisobi, bir nechta shartlar birikmasi (AND, BETWEEN, ILIKE), aniq ikki bosqichli tartiblash (ORDER BY) va standart xavfsiz sahifalash (FETCH FIRST).

## Ishlash natijasi:
```text
id |   nomi   |  toifa   |    narx     | narx_nds_bilan | mavjud 
----+----------+----------+-------------+----------------+--------
  1 | Asus ROG | Noutbuk  | 14000000.00 |    15680000.00 | t
  2 | iPhone 15| Smartfon | 12000000.00 |    13440000.00 | t
(2 rows)
```

