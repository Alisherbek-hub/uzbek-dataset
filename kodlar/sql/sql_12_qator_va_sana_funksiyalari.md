# 551-Topshiriq: Satr uzunligi: LENGTH() va OCTET_LENGTH() farqi
## Topshiriq sharti:
O'zbek tilidagi maxsus harflar ('o‘', 'g‘', krill/lotin) nechta belgi va nechta bayt egallashini ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT 
    'O‘zbekiston' AS matn,
    LENGTH('O‘zbekiston') AS belgilar_soni,
    OCTET_LENGTH('O‘zbekiston') AS baytlar_soni;
```

## Tushuntirish va Mantiq:
'LENGTH()' (yoki CHAR_LENGTH) inson ko'zi bilan ko'rinadigan belgilar sonini hisoblaydi. 'OCTET_LENGTH()' esa UTF-8 kodlashida ushbu satr xotirada egallagan fizik baytlar sonini qaytaradi. UTF-8 da '‘' belgisi bir necha bayt joy oladi.

## Ishlash natijasi:
```text
matn     | belgilar_soni | baytlar_soni 
-------------+---------------+--------------
 O‘zbekiston |            11 |           13
(1 row)
```


# 552-Topshiriq: Xavfsiz birlashtirish: CONCAT() va CONCAT_WS()
## Topshiriq sharti:
NULL qiymatlar uchraganda ham so'zlar orasini buzmaydigan ajratuvchili birlashtirish.

## Yechim (SQL kodi):
```sql
SELECT 
    CONCAT('Toshkent', ' - ', 'Samarqand') AS oddiy_ulash,
    CONCAT_WS(', ', 'Toshkent', NULL, 'Buxoro', 'Xiva') AS ws_ulash;
```

## Tushuntirish va Mantiq:
'CONCAT_WS(separator, ...)' birinchi parametrni ajratuvchi qilib oladi va ro'yxatdagi barcha NULL qiymatlarni jimgina o'tkazib yuboradi. Natijada oraliqda keraksiz qo'shaloq vergullar hosil bo'lmaydi.

## Ishlash natijasi:
```text
oddiy_ulash      |        ws_ulash        
----------------------+------------------------
 Toshkent - Samarqand | Toshkent, Buxoro, Xiva
(1 row)
```


# 553-Topshiriq: Satrdan qism kesib olish: SUBSTRING() va SUBSTR()
## Topshiriq sharti:
Pasport seriyasining dastlabki 2 ta harfini va 7 ta raqamini alohida ajrating.

## Yechim (SQL kodi):
```sql
CREATE TABLE pasport_baza (pasport VARCHAR(9));
INSERT INTO pasport_baza VALUES ('AA1234567'), ('AB9876543');

SELECT 
    pasport,
    SUBSTRING(pasport FROM 1 FOR 2) AS seriya,
    SUBSTRING(pasport FROM 3 FOR 7) AS raqam
FROM pasport_baza;
```

## Tushuntirish va Mantiq:
PostgreSQL da `SUBSTRING(satr FROM boshlangich_orin FOR uzunlik)` ANSI SQL standartidagi sintaksisdir. 1-pozitsiyadan boshlanadi.

## Ishlash natijasi:
```text
pasport  | seriya |  raqam  
-----------+--------+---------
 AA1234567 | AA     | 1234567
 AB9876543 | AB     | 9876543
(2 rows)
```


# 554-Topshiriq: Bo'shliqlarni tozalash: TRIM, LTRIM, RTRIM
## Topshiriq sharti:
Foydalanuvchi adashib kiritgan boshidagi va oxiridagi bo'shliqlarni olib tashlang.

## Yechim (SQL kodi):
```sql
SELECT 
    '[' || TRIM('   salom dunyo   ') || ']' AS toza_trim,
    '[' || LTRIM('   chap bo‘shliq') || ']' AS toza_ltrim,
    '[' || RTRIM('o‘ng bo‘shliq   ') || ']' AS toza_rtrim;
```

## Tushuntirish va Mantiq:
TRIM ikki tomondagi bo'shliqlarni, LTRIM faqat chap, RTRIM faqat o'ng tomon bo'shliqlarini tozalaydi.

## Ishlash natijasi:
```text
toza_trim   |   toza_ltrim    |   toza_rtrim   
---------------+-----------------+----------------
 [salom dunyo] | [chap bo‘shliq] | [o‘ng bo‘shliq]
(1 row)
```


# 555-Topshiriq: Maxsus belgilarni TRIM bilan tozalash
## Topshiriq sharti:
Satr boshidagi va oxiridagi nol raqamlarini yoki maxsus belgilarni olib tashlang.

## Yechim (SQL kodi):
```sql
SELECT 
    TRIM(BOTH '0' FROM '00012345000') AS toza_son,
    TRIM(BOTH '#' FROM '###MUHIM_XABAR###') AS toza_matn;
```

## Tushuntirish va Mantiq:
'TRIM(BOTH belgi FROM satr)' parametr sifatida ko'rsatilgan har qanday belgini chetlardan tozalaydi.

## Ishlash natijasi:
```text
toza_son |  toza_matn   
----------+-------------
 12345    | MUHIM_XABAR
(1 row)
```


# 556-Topshiriq: Matnni almashtirish: REPLACE()
## Topshiriq sharti:
Telefon raqamidagi barcha tire va bo'shliqlarni tozalab toza raqam ko'rinishiga keltiring.

## Yechim (SQL kodi):
```sql
SELECT REPLACE(REPLACE('+998 90-123-45-67', ' ', ''), '-', '') AS toza_telefon;
```

## Tushuntirish va Mantiq:
'REPLACE(matn, eski, yangi)' ko'rsatilgan qismni yangi qism bilan almashtiradi.

## Ishlash natijasi:
```text
toza_telefon  
---------------
 +998901234567
(1 row)
```


# 557-Topshiriq: Registrni o'zgartirish: UPPER, LOWER, INITCAP
## Topshiriq sharti:
Ism-sharifni barcha so'zlari bosh harf bilan boshlanadigan (Capitalized) holatga keltiring.

## Yechim (SQL kodi):
```sql
SELECT 
    UPPER('alisher navoiy') AS katta_harf,
    LOWER('ALISHER NAVOIY') AS kichik_harf,
    INITCAP('alisher navoiy g‘azallari') AS bosh_harflar;
```

## Tushuntirish va Mantiq:
'INITCAP(satr)' har bir so'zning birinchi harfini bosh harfga, qolganlarini kichik harfga aylantiradi.

## Ishlash natijasi:
```text
katta_harf   |   kichik_harf   |        bosh_harflar        
----------------+-----------------+----------------------------
 ALISHER NAVOIY | alisher navoiy | Alisher Navoiy G‘azallari
(1 row)
```


# 558-Topshiriq: Satrlarni to'ldirish: LPAD va RPAD (Maskalash va Formatlash)
## Topshiriq sharti:
Bank kartasining dastlabki 12 ta raqamini '*' bilan yashiring (Masking).

## Yechim (SQL kodi):
```sql
SELECT 
    LPAD(SUBSTRING('8600123456789999' FROM 13 FOR 4), 16, '*') AS maskalangan_karta,
    RPAD('Faktura', 15, '.') AS formatli_qator;
```

## Tushuntirish va Mantiq:
'LPAD(satr, umumiy_uzunlik, toldiruvchi)' chap tomondan kerakli uzunlikka yetguncha belgi qo'shadi. Xavfsiz karta ma'lumotlarini ko'rsatishda juda qulay.

## Ishlash natijasi:
```text
maskalangan_karta | formatli_qator  
------------------+-----------------
 ************9999 | Faktura........
(1 row)
```


# 559-Topshiriq: Ajratuvchi bo'yicha N-qismni olish: SPLIT_PART()
## Topshiriq sharti:
Elektron pochtadan foydalanuvchi nomi va domen qismini alohida oling.

## Yechim (SQL kodi):
```sql
SELECT 
    SPLIT_PART('shoxrux.dev@gmail.com', '@', 1) AS login_qismi,
    SPLIT_PART('shoxrux.dev@gmail.com', '@', 2) AS domen_qismi;
```

## Tushuntirish va Mantiq:
'SPLIT_PART(matn, ajratuvchi, qism_raqami)' satrni massivga ajratib, n-chi bo'lagini to'g'ridan-to'g'ri qaytaradi.

## Ishlash natijasi:
```text
login_qismi | domen_qismi 
-------------+-------------
 shoxrux.dev | gmail.com
(1 row)
```


# 560-Topshiriq: Satrdan qidirish: POSITION() va STRPOS()
## Topshiriq sharti:
Matn ichida '@' belgisi nechanchi o'rinda turganini aniqlang.

## Yechim (SQL kodi):
```sql
SELECT 
    POSITION('@' IN 'user@domain.uz') AS pos_1,
    STRPOS('user@domain.uz', '@') AS pos_2;
```

## Tushuntirish va Mantiq:
Ikkala funksiya ham qidirilayotgan satrchaning 1 dan boshlanuvchi indeksini qaytaradi. Topilmasa 0 beradi.

## Ishlash natijasi:
```text
pos_1 | pos_2 
-------+-------
     5 |     5
(1 row)
```


# 561-Topshiriq: Satrni teskarisiga o'girish: REVERSE()
## Topshiriq sharti:
So'zning palindrom ekanligini (orqasidan o'qiganda ham bir xilligini) REVERSE bilan tekshiring.

## Yechim (SQL kodi):
```sql
SELECT 
    'aziza' AS soz,
    (LOWER('aziza') = REVERSE(LOWER('aziza'))) AS palindrommi;
```

## Tushuntirish va Mantiq:
'REVERSE(satr)' belgilar tartibini teskarisiga o'zgartiradi.

## Ishlash natijasi:
```text
soz  | palindrommi 
-------+-------------
 aziza | t
(1 row)
```


# 562-Topshiriq: Muntazam ifodalar bilan almashtirish: REGEXP_REPLACE()
## Topshiriq sharti:
Matn ichidagi barcha ortiqcha ko'p bo'shliqlarni bitta bo'shliqqa keltiring.

## Yechim (SQL kodi):
```sql
SELECT REGEXP_REPLACE('Toshkent   shahar     Chilonzor', '\s+', ' ', 'g') AS toza_matn;
```

## Tushuntirish va Mantiq:
'REGEXP_REPLACE(matn, pattern, replacement, flags)' dagi 'g' (global) bayrog'i barcha mosliklarni bitta bo'shliq bilan almashtiradi.

## Ishlash natijasi:
```text
toza_matn          
----------------------------
 Toshkent shahar Chilonzor
(1 row)
```


# 563-Topshiriq: Muntazam ifodalar orqali qiymat sug'urib olish: REGEXP_MATCHES()
## Topshiriq sharti:
Matn ichidan telefon raqamlarini regex orqali ajratib oling.

## Yechim (SQL kodi):
```sql
SELECT (REGEXP_MATCHES('Mening raqamim +998901234567, aloqaga chiqing', '(\+998[0-9]{9})'))[1] AS topilgan_raqam;
```

## Tushuntirish va Mantiq:
'REGEXP_MATCHES()' qavs ichidagi guruhlarni massiv sifatida qaytaradi, `[1]` orqali birinchi guruh olinadi.

## Ishlash natijasi:
```text
topilgan_raqam 
---------------
 +998901234567
(1 row)
```


# 564-Topshiriq: Joriy sana va vaqt funksiyalari: NOW() vs CLOCK_TIMESTAMP()
## Topshiriq sharti:
PostgreSQL da NOW() va CLOCK_TIMESTAMP() farqini ko'ring.

## Yechim (SQL kodi):
```sql
SELECT 
    NOW() AS tranzaksiya_vaqti,
    CLOCK_TIMESTAMP() AS soat_vaqti;
```

## Tushuntirish va Mantiq:
'NOW()' yoki 'CURRENT_TIMESTAMP' butun tranzaksiya boshlangan paytdagi o'zgarmas vaqtni saqlaydi. 'CLOCK_TIMESTAMP()' esa haqiqiy joriy vaqtni mikrosaniyasigacha o'qib beradi.

## Ishlash natijasi:
```text
tranzaksiya_vaqti       |          soat_vaqti           
-------------------------------+-------------------------------
 2026-11-08 12:00:00.123456+05 | 2026-11-08 12:00:00.123499+05
(1 row)
```


# 565-Topshiriq: Faqat joriy sana va faqat joriy vaqt
## Topshiriq sharti:
Vaqtsiz sana (CURRENT_DATE) va sanasiz vaqt (CURRENT_TIME).

## Yechim (SQL kodi):
```sql
SELECT 
    CURRENT_DATE AS bugun,
    CURRENT_TIME AS joriy_soat;
```

## Tushuntirish va Mantiq:
Faqat sana bilan ishlaganda CURRENT_DATE xotira va formatlashni soddalashtiradi.

## Ishlash natijasi:
```text
bugun    |    joriy_soat     
------------+-------------------
 2026-11-08 | 12:00:00.12345+05
(1 row)
```


# 566-Topshiriq: Sananing qismlarini ajratish: EXTRACT()
## Topshiriq sharti:
Sanadan yil, oy, kun va haftaning kunini ajratib oling.

## Yechim (SQL kodi):
```sql
SELECT 
    EXTRACT(YEAR FROM NOW()) AS yil,
    EXTRACT(MONTH FROM NOW()) AS oy,
    EXTRACT(DAY FROM NOW()) AS kun,
    EXTRACT(ISODOW FROM NOW()) AS hafta_kuni;
```

## Tushuntirish va Mantiq:
'EXTRACT(field FROM source)' har qanday sana yoki intervaldan butun yoki kasr qismini chiqaradi. ISODOW: 1=Dushanba ... 7=Yakshanba.

## Ishlash natijasi:
```text
yil  | oy | kun | hafta_kuni 
------+----+-----+------------
 2026 | 11 |   8 |          7
(1 row)
```


# 567-Topshiriq: Unix Timestamp (EPOCH soniyalari) ga o'girish
## Topshiriq sharti:
Sanani 1970-yil 1-yanvardan beri o'tgan soniyalar soniga (Unix Epoch) aylantiring.

## Yechim (SQL kodi):
```sql
SELECT 
    EXTRACT(EPOCH FROM NOW())::BIGINT AS unix_epoch_soniyalar,
    TO_TIMESTAMP(1762588800) AS sanaga_qaytish;
```

## Tushuntirish va Mantiq:
'EXTRACT(EPOCH FROM ...)' Unix vaqtini beradi, 'TO_TIMESTAMP(epoch)' esa soniyadan yana PostgreSQL sanasini tiklaydi.

## Ishlash natijasi:
```text
unix_epoch_soniyalar |     sanaga_qaytish     
----------------------+------------------------
           1794121200 | 2025-11-08 13:00:00+05
(1 row)
```


# 568-Topshiriq: Sanalarni yaxlitlash: DATE_TRUNC()
## Topshiriq sharti:
Sanani oyning boshiga, yilning boshiga yoki soatning boshiga to'g'rilang.

## Yechim (SQL kodi):
```sql
SELECT 
    DATE_TRUNC('year', NOW())::DATE AS yil_boshi,
    DATE_TRUNC('month', NOW())::DATE AS oy_boshi,
    DATE_TRUNC('day', NOW()) AS kun_boshi;
```

## Tushuntirish va Mantiq:
'DATE_TRUNC(birlik, sana)' vaqt seriyalarini analitik guruhlashda (Oylar, Yillar, Haftalar bo'yicha) asosiy poydevor hisoblanadi.

## Ishlash natijasi:
```text
yil_boshi  |  oy_boshi  |       kun_boshi        
------------+------------+------------------------
 2026-01-01 | 2026-11-01 | 2026-11-08 00:00:00+05
(1 row)
```


# 569-Topshiriq: Yillik choraklar bo'yicha yaxlitlash (Quarter)
## Topshiriq sharti:
Sana qaysi chorakka (Q1, Q2, Q3, Q4) tegishli ekanligini DATE_TRUNC va EXTRACT orqali toping.

## Yechim (SQL kodi):
```sql
SELECT 
    EXTRACT(QUARTER FROM NOW()) AS chorak_raqami,
    DATE_TRUNC('quarter', NOW())::DATE AS chorak_boshi;
```

## Tushuntirish va Mantiq:
Moliyaviy hisobotlarda choraklik (Quarterly) tahlil shunday quriladi.

## Ishlash natijasi:
```text
chorak_raqami | chorak_boshi 
----------------+--------------
              4 | 2026-10-01
(1 row)
```


# 570-Topshiriq: Oradagi yosh va davrni hisoblash: AGE()
## Topshiriq sharti:
Tug'ilgan sanadan to bugungi kungacha necha yil, necha oy va kun o'tganini aniqlang.

## Yechim (SQL kodi):
```sql
SELECT AGE('1995-04-15'::DATE) AS xodim_yoshi;
```

## Tushuntirish va Mantiq:
'AGE(sana)' yoki 'AGE(sana1, sana2)' ikki sana orasidagi aniq vaqt oralig'ini '31 years 6 mons 24 days' ko'rinishidagi INTERVAL formatida chiqaradi.

## Ishlash natijasi:
```text
xodim_yoshi        
--------------------------
 31 years 6 mons 24 days
(1 row)
```


# 571-Topshiriq: INTERVAL arifmetikasi (Qo'shish va ayirish)
## Topshiriq sharti:
Bugungi kunga 3 oy va 10 kun qo'shish, hamda 2 soat ayirish amali.

## Yechim (SQL kodi):
```sql
SELECT 
    CURRENT_DATE + INTERVAL '3 months 10 days' AS kelajak_sana,
    NOW() - INTERVAL '2 hours 30 minutes' AS otgan_vaqt;
```

## Tushuntirish va Mantiq:
PostgreSQL INTERVAL turlari bilan insoniy tilda matematik arifmetika bajarishga imkon beradi.

## Ishlash natijasi:
```text
kelajak_sana       |          otgan_vaqt           
-------------------------+-------------------------------
 2027-02-18 00:00:00     | 2026-11-08 09:30:00.123456+05
(1 row)
```


# 572-Topshiriq: Ikki sana orasidagi kunlar soni (Oddiy ayirish)
## Topshiriq sharti:
Ikki DATE turini bir-biridan ayirganda INTEGER (kunlar soni) chiqishini ko'ring.

## Yechim (SQL kodi):
```sql
SELECT ('2026-12-31'::DATE - '2026-01-01'::DATE) AS yildagi_kunlar_soni;
```

## Tushuntirish va Mantiq:
PostgreSQL da ikkita DATE ayirilsa, oraliqdagi kunlar soni to'g'ridan-to'g'ri butun son sifatida qaytadi.

## Ishlash natijasi:
```text
yildagi_kunlar_soni 
---------------------
                 364
(1 row)
```


# 573-Topshiriq: Sanalarni chiroyli matnga formatlash: TO_CHAR()
## Topshiriq sharti:
Sanani '08-Noyabr, 2026-yil, 14:30' shaklida formatlab chiqaring.

## Yechim (SQL kodi):
```sql
SELECT TO_CHAR(NOW(), 'DD-TMMonth, YYYY-yil, HH24:MI') AS formatli_sana;
```

## Tushuntirish va Mantiq:
'TO_CHAR(sana, shablon)' sana va vaqtni istalgan ko'rinishda chiroyli matnga o'giradi. 'TM' prefiksi (Translation Mode) mahalliy oylar nomini chiqaradi.

## Ishlash natijasi:
```text
formatli_sana          
---------------------------------
 08-November , 2026-yil, 12:00
(1 row)
```


# 574-Topshiriq: Matnni sanaga o'tkazish: TO_DATE() va TO_TIMESTAMP()
## Topshiriq sharti:
'25/12/2026' shaklidagi nostandart matnni PostgreSQL DATE turiga o'giring.

## Yechim (SQL kodi):
```sql
SELECT 
    TO_DATE('25/12/2026', 'DD/MM/YYYY') AS haqiqiy_sana,
    TO_TIMESTAMP('2026-05-10 14:45:00', 'YYYY-MM-DD HH24:MI:SS') AS haqiqiy_vaqt;
```

## Tushuntirish va Mantiq:
Noto'g'ri formatdagi kiruvchi fayllarni (Excel, CSV) qabul qilishda TO_DATE juda muhim.

## Ishlash natijasi:
```text
haqiqiy_sana |      haqiqiy_vaqt      
-------------+------------------------
 2026-12-25  | 2026-05-10 14:45:00+05
(1 row)
```


# 575-Topshiriq: Vaqt mintaqasi (Time Zone) konvertatsiyasi: AT TIME ZONE
## Topshiriq sharti:
Toshkent vaqtini Nyu-York (EST) va Tokio (JST) vaqtlariga o'tkazing.

## Yechim (SQL kodi):
```sql
SELECT 
    NOW() AT TIME ZONE 'Asia/Tashkent' AS toshkent_vaqti,
    NOW() AT TIME ZONE 'America/New_York' AS new_york_vaqti,
    NOW() AT TIME ZONE 'Asia/Tokyo' AS tokyo_vaqti;
```

## Tushuntirish va Mantiq:
'AT TIME ZONE' vaqtni boshqa xalqaro mintaqaga bir zumda konvertatsiya qiladi.

## Ishlash natijasi:
```text
toshkent_vaqti       |       new_york_vaqti       |        tokyo_vaqti         
---------------------------+----------------------------+----------------------------
 2026-11-08 12:00:00.123456| 2026-11-08 02:00:00.123456 | 2026-11-08 16:00:00.123456
(1 row)
```


# 576-Topshiriq: Oyning oxirgi kunini topish
## Topshiriq sharti:
Keyingi oyning 1-kunidan 1 kun ayirish orqali joriy oyning oxirgi kunini aniqlang.

## Yechim (SQL kodi):
```sql
SELECT (DATE_TRUNC('month', NOW()) + INTERVAL '1 month' - INTERVAL '1 day')::DATE AS oyning_oxirgi_kuni;
```

## Tushuntirish va Mantiq:
Fevral 28 yoki 29, 30 yoki 31 kunligini hisobga oluvchi universal formula.

## Ishlash natijasi:
```text
oyning_oxirgi_kuni 
--------------------
 2026-11-30
(1 row)
```


# 577-Topshiriq: Kabisa yilini tekshirish (Leap Year)
## Topshiriq sharti:
Yilda 366 kun bor-yo'qligini tekshiruvchi SQL ifodasini yozing.

## Yechim (SQL kodi):
```sql
SELECT 
    2026 AS yil,
    ('2026-12-31'::DATE - '2026-01-01'::DATE + 1 = 366) AS kabisa_yilimi;
```

## Tushuntirish va Mantiq:
366 kun bo'lsa TRUE, 365 kun bo'lsa FALSE chiqadi.

## Ishlash natijasi:
```text
yil  | kabisa_yilimi 
------+---------------
 2026 | f
(1 row)
```


# 578-Topshiriq: Vaqt oralig'ini soniyalarga aylantirish
## Topshiriq sharti:
2 soat 45 daqiqaning jami necha soniya ekanligini hisoblang.

## Yechim (SQL kodi):
```sql
SELECT EXTRACT(EPOCH FROM INTERVAL '2 hours 45 minutes')::INT AS jami_soniyalar;
```

## Tushuntirish va Mantiq:
INTERVAL ustida EXTRACT(EPOCH) umumiy soniyalar miqdorini qaytaradi.

## Ishlash natijasi:
```text
jami_soniyalar 
-----------------
            9900
(1 row)
```


# 579-Topshiriq: Ikki vaqt oralig'idagi ish soatlarini hisoblash
## Topshiriq sharti:
Boshlanish va tugash vaqti orasidagi sof farqni soatlarda ifodalang.

## Yechim (SQL kodi):
```sql
SELECT ROUND(
    (EXTRACT(EPOCH FROM ('2026-06-01 18:30:00'::TIMESTAMP - '2026-06-01 09:00:00'::TIMESTAMP)) / 3600)::NUMERIC, 
    2
) AS ishlangan_soatlar;
```

## Tushuntirish va Mantiq:
Soniyalarni 3600 ga bo'lish orqali aniq kasr soatlar (9.5 soat) olinadi.

## Ishlash natijasi:
```text
ishlangan_soatlar 
------------------
             9.50
(1 row)
```


# 580-Topshiriq: Haftaning ma'lum kunini topish (Keyingi dushanba)
## Topshiriq sharti:
Ixtiyoriy sanadan keyingi eng yaqin dushanba kunini hisoblash.

## Yechim (SQL kodi):
```sql
SELECT ('2026-11-08'::DATE + ((8 - EXTRACT(ISODOW FROM '2026-11-08'::DATE)::INT) % 7 || ' days')::INTERVAL)::DATE AS keyingi_dushanba;
```

## Tushuntirish va Mantiq:
Modul (%) arifmetikasi bilan eng yaqin ish haftasi boshlanishi aniqlanadi.

## Ishlash natijasi:
```text
keyingi_dushanba 
-------------------
 2026-11-09
(1 row)
```


# 581-Topshiriq: Matndan raqamlarni ajratib olish (REGEXP_REPLACE)
## Topshiriq sharti:
Harflar va belgilardan iborat matndan faqatgina sonlarni qoldiring.

## Yechim (SQL kodi):
```sql
SELECT REGEXP_REPLACE('Buyurtma #A-98745/2026', '[^0-9]', '', 'g') AS toza_raqamlar;
```

## Tushuntirish va Mantiq:
'[^0-9]' raqam bo'lmagan barcha belgilarni topadi va bo'shliqqa almashtiradi.

## Ishlash natijasi:
```text
toza_raqamlar 
---------------
 987452026
(1 row)
```


# 582-Topshiriq: MD5 va SHA256 kriptografik xeshlash
## Topshiriq sharti:
Parol yoki matnning MD5 va SHA256 xesh summasini hisoblang.

## Yechim (SQL kodi):
```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;

SELECT 
    MD5('maxfiy_parol') AS md5_xesh,
    ENCODE(DIGEST('maxfiy_parol', 'sha256'), 'hex') AS sha256_xesh;
```

## Tushuntirish va Mantiq:
PostgreSQL o'rnatilgan MD5 hamda pgcrypto moduli orqali sanoat standartidagi SHA256 xeshlarini generatsiya qiladi.

## Ishlash natijasi:
```text
CREATE EXTENSION
             md5_xesh             |                           sha256_xesh                            
----------------------------------+------------------------------------------------------------------
 ebc35fef6d27ca5e45447fb50d3e0988 | e20e0657960ea9b027b4b1a41db86f55462ee67d32c5aa8c05e1975e1823eb97
(1 row)
```


# 583-Topshiriq: Tasodifiy belgilar satri generatsiyasi (Tasodifiy parol)
## Topshiriq sharti:
Tasodifiy 8 belgili xavfsiz kod hosil qiling.

## Yechim (SQL kodi):
```sql
SELECT SUBSTRING(MD5(RANDOM()::TEXT) FROM 1 FOR 8) AS tasodifiy_kod;
```

## Tushuntirish va Mantiq:
RANDOM va MD5 birikmasi tezkor vaqtinchalik parol va tokenlar yasaydi.

## Ishlash natijasi:
```text
tasodifiy_kod 
----------------
 4f8b2c1a
(1 row)
```


# 584-Topshiriq: Sana qatorlarini ketma-ket generatsiya qilish: generate_series()
## Topshiriq sharti:
Bir sanadan ikkinchi sanagacha bo'lgan barcha kunlarni qatorlar qilib chiqaring.

## Yechim (SQL kodi):
```sql
SELECT kun::DATE 
FROM generate_series('2026-12-01'::DATE, '2026-12-03'::DATE, '1 day'::INTERVAL) AS kun;
```

## Tushuntirish va Mantiq:
Hisobotlarda ma'lumotlar uzluksizligini ta'minlovchi asosiy funksiya.

## Ishlash natijasi:
```text
kun     
------------
 2026-12-01
 2026-12-02
 2026-12-03
(3 rows)
```


# 585-Topshiriq: Harflar o'rnini almashtirish: TRANSLATE()
## Topshiriq sharti:
Matndagi kirill 'a, b, c' harflarini lotin muqobiliga birdaniga almashtirish.

## Yechim (SQL kodi):
```sql
SELECT TRANSLATE('abc', 'abc', '123') AS almashtirilgan;
```

## Tushuntirish va Mantiq:
'TRANSLATE(satr, qidiriluvchi, almashtiriluvchi)' har bir belgini o'z o'rnidagi belgiga bittalab moslaydi.

## Ishlash natijasi:
```text
almashtirilgan 
----------------
 123
(1 row)
```


# 586-Topshiriq: Qatorni massivga ajratish: STRING_TO_ARRAY()
## Topshiriq sharti:
Vergulli matnni PostgreSQL massiviga o'giring.

## Yechim (SQL kodi):
```sql
SELECT STRING_TO_ARRAY('olma,anor,uzum,shaftoli', ',') AS mevalar_massivi;
```

## Tushuntirish va Mantiq:
CSV ko'rinishidagi satrlarni massivga aylantiradi.

## Ishlash natijasi:
```text
mevalar_massivi      
--------------------------
 {olma,anor,uzum,shaftoli}
(1 row)
```


# 587-Topshiriq: Massivni yana matnga birlashtirish: ARRAY_TO_STRING()
## Topshiriq sharti:
Massiv elementlarini chiziqcha (-) bilan ajratilgan bitta matn qiling.

## Yechim (SQL kodi):
```sql
SELECT ARRAY_TO_STRING(ARRAY['Toshkent', 'Samarqand', 'Buxoro'], ' - ') AS marshrut_matni;
```

## Tushuntirish va Mantiq:
Massivlarni chiroyli formatda ko'rsatishda qo'llanadi.

## Ishlash natijasi:
```text
marshrut_matni         
------------------------------
 Toshkent - Samarqand - Buxoro
(1 row)
```


# 588-Topshiriq: Sana formatlashda hafta raqamini olish (ISO Week)
## Topshiriq sharti:
Yilning nechanchi haftasi ekanligini hisoblang.

## Yechim (SQL kodi):
```sql
SELECT 
    EXTRACT(WEEK FROM NOW()) AS hafta_raqami,
    TO_CHAR(NOW(), 'IYYY-IW') AS iso_yil_va_hafta;
```

## Tushuntirish va Mantiq:
Ishlab chiqarish va yetkazib berish grafiklari ISO haftalar (W01 ... W52) bo'yicha tuziladi.

## Ishlash natijasi:
```text
hafta_raqami | iso_yil_va_hafta 
--------------+------------------
           45 | 2026-45
(1 row)
```


# 589-Topshiriq: Bo'sh satr yoki bo'shliqlarni aniqlash funksiyasi
## Topshiriq sharti:
Satr haqiqiy ma'noli belgiga egami yoki faqat bo'shliqlarmi?

## Yechim (SQL kodi):
```sql
SELECT 
    ism,
    (NULLIF(TRIM(ism), '') IS NULL) AS yaroqsizmi
FROM (VALUES ('   '), ('Ali'), ('')) AS t(ism);
```

## Tushuntirish va Mantiq:
'NULLIF(TRIM(matn), '')' barcha bo'sh qatorlarni yagona NULL ga aylantiradi.

## Ishlash natijasi:
```text
ism | yaroqsizmi 
-----+------------
     | t
 Ali | f
     | t
(3 rows)
```


# 590-Topshiriq: Takrorlanuvchi matn generatsiyasi: REPEAT()
## Topshiriq sharti:
Reyting balliga qarab yulduzchalar (⭐⭐⭐⭐⭐) chiqarish.

## Yechim (SQL kodi):
```sql
SELECT 
    ism, ball,
    REPEAT('★', ball) || REPEAT('☆', 5 - ball) AS yulduzlar
FROM (VALUES ('Ali', 4), ('Vali', 5), ('Gani', 3)) AS r(ism, ball);
```

## Tushuntirish va Mantiq:
REPEAT vizual progress-bar va yulduzchalarni konsolda chizishda juda qo'l keladi.

## Ishlash natijasi:
```text
ism  | ball | yulduzlar 
------+------+-----------
 Ali  |    4 | ★★★★☆
 Vali |    5 | ★★★★★
 Gani |    3 | ★★★☆☆
(3 rows)
```


# 591-Topshiriq: Soat, daqiqa, soniyani alohida yasash: MAKE_TIME()
## Topshiriq sharti:
Raqamlardan TIME turini hosil qiling.

## Yechim (SQL kodi):
```sql
SELECT MAKE_TIME(14, 30, 00) AS dars_vaqti;
```

## Tushuntirish va Mantiq:
Raqamli o'zgaruvchilarni toza TIME ga aylantiradi.

## Ishlash natijasi:
```text
dars_vaqti 
------------
 14:30:00
(1 row)
```


# 592-Topshiriq: Sanani alohida raqamlardan yasash: MAKE_DATE()
## Topshiriq sharti:
Yil, oy va kundan DATE hosil qilish.

## Yechim (SQL kodi):
```sql
SELECT MAKE_DATE(2026, 9, 1) AS mustaqillik_kuni;
```

## Tushuntirish va Mantiq:
Yil, oy, kun parametrlaridan to'g'ridan-to'g'ri kalendar sanasi hosil qilinadi.

## Ishlash natijasi:
```text
mustaqillik_kuni 
-------------------
 2026-09-01
(1 row)
```


# 593-Topshiriq: Sana vaqt zonasini o'rnatish: SET TIME ZONE
## Topshiriq sharti:
Joriy sessiyaning vaqt mintaqasini vaqtincha UTC ga o'zgartirish.

## Yechim (SQL kodi):
```sql
SET TIME ZONE 'UTC';
SELECT NOW() AS utc_vaqti;
SET TIME ZONE 'Asia/Tashkent';
```

## Tushuntirish va Mantiq:
Sessiyaning vaqt zonasi sozlamasi barcha TIMESTAMPTZ ko'rinishlariga ta'sir qiladi.

## Ishlash natijasi:
```text
SET
          utc_vaqti           
------------------------------
 2026-11-08 07:00:00.12345+00
(1 row)
SET
```


# 594-Topshiriq: Matn ichidagi qatorlar sonini aniqlash
## Topshiriq sharti:
Ko'p qatorli TEXT matnida nechta qator (Enter) borligini sanang.

## Yechim (SQL kodi):
```sql
SELECT CARDINALITY(STRING_TO_ARRAY('Birinchi qator
Ikkinchi qator
Uchinchi', '
')) AS qatorlar_soni;
```

## Tushuntirish va Mantiq:
STRING_TO_ARRAY va CARDINALITY matndagi qatorlar sonini bir zumda aytadi.

## Ishlash natijasi:
```text
qatorlar_soni 
---------------
             3
(1 row)
```


# 595-Topshiriq: LEFT va RIGHT qator funksiyalari
## Topshiriq sharti:
Satrning eng chap yoki eng o'ng tomonidagi N ta belgini olish.

## Yechim (SQL kodi):
```sql
SELECT 
    LEFT('TOSHKENT', 4) AS chap_4,
    RIGHT('TOSHKENT', 4) AS ong_4;
```

## Tushuntirish va Mantiq:
SUBSTRING ga qaraganda soddaroq va ixchamroq sintaksis.

## Ishlash natijasi:
```text
chap_4 | ong_4 
--------+-------
 TOSH   | KENT
(1 row)
```


# 596-Topshiriq: Vaqt oralig'i (Interval) ustida ko'paytirish va bo'lish
## Topshiriq sharti:
15 daqiqalik dars tanaffusini 4 barobarga oshirish.

## Yechim (SQL kodi):
```sql
SELECT INTERVAL '15 minutes' * 4 AS jami_tanaffus;
```

## Tushuntirish va Mantiq:
INTERVAL turlari butun yoki kasr sonlarga to'g'ridan-to'g'ri ko'paytiriladi.

## Ishlash natijasi:
```text
jami_tanaffus 
---------------
 01:00:00
(1 row)
```


# 597-Topshiriq: Vaqtlar kesishuvini OVERLAPS bilan tekshirish
## Topshiriq sharti:
Ikki sana oralig'ining bir-biriga tushib qolishini SQL standartidagi OVERLAPS bilan aniqlang.

## Yechim (SQL kodi):
```sql
SELECT (DATE '2026-05-01', DATE '2026-05-10') OVERLAPS 
       (DATE '2026-05-08', DATE '2026-05-15') AS kesishadimi;
```

## Tushuntirish va Mantiq:
'OVERLAPS' ANSI SQL ning o'rnatilgan operatori bo'lib, ikkita vaqt oralig'ining kesishuvini tekshiradi.

## Ishlash natijasi:
```text
kesishadimi 
-------------
 t
(1 row)
```


# 598-Topshiriq: Sana ustuniga B-Tree indeks qo'yilganda funksiya xavfi (SARGability)
## Topshiriq sharti:
Nega `WHERE EXTRACT(YEAR FROM sana) = 2026` indeksni o'ldirishi va uning to'g'ri yozilishini ko'rsating.

## Yechim (SQL kodi):
```sql
-- Sekin (Indeks ishlamaydi):
-- WHERE EXTRACT(YEAR FROM sana) = 2026;

-- Tez va SARGable (Indeks to'liq ishlaydi):
-- WHERE sana >= '2026-01-01' AND sana < '2027-01-01';
SELECT 'Indekslangan ustunni funksiya ichiga o‘rash Index Scanni yo‘qotadi!' AS ogohlantirish;
```

## Tushuntirish va Mantiq:
SARGable (Search Argument Able): ustun hech qanday funksiya ichiga olinmasdan sof holda taqqoslanishi shart, aks holda optimizator Seq Scanga tushadi.

## Ishlash natijasi:
```text
ogohlantirish                                     
--------------------------------------------------------------------------------------
 Indekslangan ustunni funksiya ichiga o‘rash Index Scanni yo‘qotadi!
(1 row)
```


# 599-Topshiriq: Matn o'xshashligini tekshirish (Levenshtein masofasi)
## Topshiriq sharti:
Imloviy xatolarni qidirish uchun ikkita so'z orasidagi Levenshtein masofasini hisoblang.

## Yechim (SQL kodi):
```sql
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;

SELECT LEVENSHTEIN('Toshkent', 'Tashkent') AS tahrir_masofasi;
```

## Tushuntirish va Mantiq:
Levenshtein masofasi bitta so'zni ikkinchisiga aylantirish uchun nechta harfni o'zgartirish kerakligini bildiradi (bu yerda 'o' -> 'a', masofa 1). Qidiruvdagi imlo tuzatishlarida ishlatiladi.

## Ishlash natijasi:
```text
CREATE EXTENSION
 tahrir_masofasi 
-----------------
               1
(1 row)
```


# 600-Topshiriq: Korporativ Vaqt va Matn Mexanizmi: Xalqaro SLA va Ish Vaqti Tahlili
## Topshiriq sharti:
Texnik qo'llab-quvvatlash xizmatiga (HelpDesk) kelgan murojaatning dam olish kunlari va kechki soatlarni chiqarib tashlagan holda haqiqiy ish vaqtini (SLA) daqiqalarda hisoblang va hisobot qiling.

## Yechim (SQL kodi):
```sql
CREATE TABLE mijoz_murojaatlari (
    ticket_id BIGSERIAL PRIMARY KEY,
    mijoz_fio VARCHAR(100),
    ochilgan_vaqt TIMESTAMPTZ,
    yopilgan_vaqt TIMESTAMPTZ
);

INSERT INTO mijoz_murojaatlari (mijoz_fio, ochilgan_vaqt, yopilgan_vaqt) VALUES 
('Anvar Qodirov', '2026-10-01 09:15:00+05', '2026-10-01 11:45:00+05'),
('Dilnoza Alimova', '2026-10-02 17:30:00+05', '2026-10-05 10:00:00+05'); -- Dam olish kunlari (shanba-yakshanba) oraliqda!

SELECT 
    ticket_id,
    INITCAP(mijoz_fio) AS mijoz,
    TO_CHAR(ochilgan_vaqt, 'YYYY-MM-DD HH24:MI') AS ochilgan,
    TO_CHAR(yopilgan_vaqt, 'YYYY-MM-DD HH24:MI') AS yopilgan,
    AGE(yopilgan_vaqt, ochilgan_vaqt) AS toliq_kalendar_farqi,
    ROUND((EXTRACT(EPOCH FROM (yopilgan_vaqt - ochilgan_vaqt)) / 60)::NUMERIC, 0) AS jami_daqiqalar,
    CASE 
        WHEN EXTRACT(EPOCH FROM (yopilgan_vaqt - ochilgan_vaqt)) / 60 <= 180 THEN '✅ SLA Bajarildi'
        ELSE '⚠️ SLA Buzildi (Kechikish)'
    END AS sla_holati
FROM mijoz_murojaatlari;
```

## Tushuntirish va Mantiq:
Ushbu korporativ so'rov IT-Service Management (ITSM, Jira, Zendesk) tizimlarining Service Level Agreement (SLA) nazorati markazidir: sana va vaqt arifmetikasi, AGE(), TO_CHAR() formatlashlari va daqiqalar hisobi orqali mijozlar shikoyatlarining o'z vaqtida hal etilishi shaffof nazorat qilinadi.

## Ishlash natijasi:
```text
ticket_id |      mijoz      |     ochilgan     |     yopilgan     |  toliq_kalendar_farqi  | jami_daqiqalar |          sla_holati          
-----------+-----------------+------------------+------------------+------------------------+----------------+------------------------------
         1 | Anvar Qodirov   | 2026-10-01 09:15 | 2026-10-01 11:45 | 02:30:00               |            150 | ✅ SLA Bajarildi
         2 | Dilnoza Alimova | 2026-10-02 17:30 | 2026-10-05 10:00 | 2 days 16:30:00        |           3870 | ⚠️ SLA Buzildi (Kechikish)
(2 rows)
```

