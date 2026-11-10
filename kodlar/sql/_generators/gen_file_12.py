import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

# List of 50 tasks for File 12: 551 - 600
# Qator va sana funksiyalari (String Functions: CONCAT, SUBSTRING, LENGTH, TRIM, REPLACE, LPAD, RPAD, REGEXP; Date Functions: NOW, EXTRACT, DATE_TRUNC, INTERVAL, AGE, TO_CHAR, Timezones)

str_date_data = [
    (
        551,
        "Satr uzunligi: LENGTH() va OCTET_LENGTH() farqi",
        "O'zbek tilidagi maxsus harflar ('o‘', 'g‘', krill/lotin) nechta belgi va nechta bayt egallashini ko'rsating.",
        """SELECT 
    'O‘zbekiston' AS matn,
    LENGTH('O‘zbekiston') AS belgilar_soni,
    OCTET_LENGTH('O‘zbekiston') AS baytlar_soni;""",
        "'LENGTH()' (yoki CHAR_LENGTH) inson ko'zi bilan ko'rinadigan belgilar sonini hisoblaydi. 'OCTET_LENGTH()' esa UTF-8 kodlashida ushbu satr xotirada egallagan fizik baytlar sonini qaytaradi. UTF-8 da '‘' belgisi bir necha bayt joy oladi.",
        """    matn     | belgilar_soni | baytlar_soni 
-------------+---------------+--------------
 O‘zbekiston |            11 |           13
(1 row)"""
    ),
    (
        552,
        "Xavfsiz birlashtirish: CONCAT() va CONCAT_WS()",
        "NULL qiymatlar uchraganda ham so'zlar orasini buzmaydigan ajratuvchili birlashtirish.",
        """SELECT 
    CONCAT('Toshkent', ' - ', 'Samarqand') AS oddiy_ulash,
    CONCAT_WS(', ', 'Toshkent', NULL, 'Buxoro', 'Xiva') AS ws_ulash;""",
        "'CONCAT_WS(separator, ...)' birinchi parametrni ajratuvchi qilib oladi va ro'yxatdagi barcha NULL qiymatlarni jimgina o'tkazib yuboradi. Natijada oraliqda keraksiz qo'shaloq vergullar hosil bo'lmaydi.",
        """      oddiy_ulash      |        ws_ulash        
----------------------+------------------------
 Toshkent - Samarqand | Toshkent, Buxoro, Xiva
(1 row)"""
    ),
    (
        553,
        "Satrdan qism kesib olish: SUBSTRING() va SUBSTR()",
        "Pasport seriyasining dastlabki 2 ta harfini va 7 ta raqamini alohida ajrating.",
        """CREATE TABLE pasport_baza (pasport VARCHAR(9));
INSERT INTO pasport_baza VALUES ('AA1234567'), ('AB9876543');

SELECT 
    pasport,
    SUBSTRING(pasport FROM 1 FOR 2) AS seriya,
    SUBSTRING(pasport FROM 3 FOR 7) AS raqam
FROM pasport_baza;""",
        "PostgreSQL da `SUBSTRING(satr FROM boshlangich_orin FOR uzunlik)` ANSI SQL standartidagi sintaksisdir. 1-pozitsiyadan boshlanadi.",
        """  pasport  | seriya |  raqam  
-----------+--------+---------
 AA1234567 | AA     | 1234567
 AB9876543 | AB     | 9876543
(2 rows)"""
    ),
    (
        554,
        "Bo'shliqlarni tozalash: TRIM, LTRIM, RTRIM",
        "Foydalanuvchi adashib kiritgan boshidagi va oxiridagi bo'shliqlarni olib tashlang.",
        """SELECT 
    '[' || TRIM('   salom dunyo   ') || ']' AS toza_trim,
    '[' || LTRIM('   chap bo‘shliq') || ']' AS toza_ltrim,
    '[' || RTRIM('o‘ng bo‘shliq   ') || ']' AS toza_rtrim;""",
        "TRIM ikki tomondagi bo'shliqlarni, LTRIM faqat chap, RTRIM faqat o'ng tomon bo'shliqlarini tozalaydi.",
        """   toza_trim   |   toza_ltrim    |   toza_rtrim   
---------------+-----------------+----------------
 [salom dunyo] | [chap bo‘shliq] | [o‘ng bo‘shliq]
(1 row)"""
    ),
    (
        555,
        "Maxsus belgilarni TRIM bilan tozalash",
        "Satr boshidagi va oxiridagi nol raqamlarini yoki maxsus belgilarni olib tashlang.",
        """SELECT 
    TRIM(BOTH '0' FROM '00012345000') AS toza_son,
    TRIM(BOTH '#' FROM '###MUHIM_XABAR###') AS toza_matn;""",
        "'TRIM(BOTH belgi FROM satr)' parametr sifatida ko'rsatilgan har qanday belgini chetlardan tozalaydi.",
        """ toza_son |  toza_matn   
----------+-------------
 12345    | MUHIM_XABAR
(1 row)"""
    ),
    (
        556,
        "Matnni almashtirish: REPLACE()",
        "Telefon raqamidagi barcha tire va bo'shliqlarni tozalab toza raqam ko'rinishiga keltiring.",
        """SELECT REPLACE(REPLACE('+998 90-123-45-67', ' ', ''), '-', '') AS toza_telefon;""",
        "'REPLACE(matn, eski, yangi)' ko'rsatilgan qismni yangi qism bilan almashtiradi.",
        """ toza_telefon  
---------------
 +998901234567
(1 row)"""
    ),
    (
        557,
        "Registrni o'zgartirish: UPPER, LOWER, INITCAP",
        "Ism-sharifni barcha so'zlari bosh harf bilan boshlanadigan (Capitalized) holatga keltiring.",
        """SELECT 
    UPPER('alisher navoiy') AS katta_harf,
    LOWER('ALISHER NAVOIY') AS kichik_harf,
    INITCAP('alisher navoiy g‘azallari') AS bosh_harflar;""",
        "'INITCAP(satr)' har bir so'zning birinchi harfini bosh harfga, qolganlarini kichik harfga aylantiradi.",
        """   katta_harf   |   kichik_harf   |        bosh_harflar        
----------------+-----------------+----------------------------
 ALISHER NAVOIY | alisher navoiy | Alisher Navoiy G‘azallari
(1 row)"""
    ),
    (
        558,
        "Satrlarni to'ldirish: LPAD va RPAD (Maskalash va Formatlash)",
        "Bank kartasining dastlabki 12 ta raqamini '*' bilan yashiring (Masking).",
        """SELECT 
    LPAD(SUBSTRING('8600123456789999' FROM 13 FOR 4), 16, '*') AS maskalangan_karta,
    RPAD('Faktura', 15, '.') AS formatli_qator;""",
        "'LPAD(satr, umumiy_uzunlik, toldiruvchi)' chap tomondan kerakli uzunlikka yetguncha belgi qo'shadi. Xavfsiz karta ma'lumotlarini ko'rsatishda juda qulay.",
        """ maskalangan_karta | formatli_qator  
------------------+-----------------
 ************9999 | Faktura........
(1 row)"""
    ),
    (
        559,
        "Ajratuvchi bo'yicha N-qismni olish: SPLIT_PART()",
        "Elektron pochtadan foydalanuvchi nomi va domen qismini alohida oling.",
        """SELECT 
    SPLIT_PART('shoxrux.dev@gmail.com', '@', 1) AS login_qismi,
    SPLIT_PART('shoxrux.dev@gmail.com', '@', 2) AS domen_qismi;""",
        "'SPLIT_PART(matn, ajratuvchi, qism_raqami)' satrni massivga ajratib, n-chi bo'lagini to'g'ridan-to'g'ri qaytaradi.",
        """ login_qismi | domen_qismi 
-------------+-------------
 shoxrux.dev | gmail.com
(1 row)"""
    ),
    (
        560,
        "Satrdan qidirish: POSITION() va STRPOS()",
        "Matn ichida '@' belgisi nechanchi o'rinda turganini aniqlang.",
        """SELECT 
    POSITION('@' IN 'user@domain.uz') AS pos_1,
    STRPOS('user@domain.uz', '@') AS pos_2;""",
        "Ikkala funksiya ham qidirilayotgan satrchaning 1 dan boshlanuvchi indeksini qaytaradi. Topilmasa 0 beradi.",
        """ pos_1 | pos_2 
-------+-------
     5 |     5
(1 row)"""
    ),
    (
        561,
        "Satrni teskarisiga o'girish: REVERSE()",
        "So'zning palindrom ekanligini (orqasidan o'qiganda ham bir xilligini) REVERSE bilan tekshiring.",
        """SELECT 
    'aziza' AS soz,
    (LOWER('aziza') = REVERSE(LOWER('aziza'))) AS palindrommi;""",
        "'REVERSE(satr)' belgilar tartibini teskarisiga o'zgartiradi.",
        """ soz  | palindrommi 
-------+-------------
 aziza | t
(1 row)"""
    ),
    (
        562,
        "Muntazam ifodalar bilan almashtirish: REGEXP_REPLACE()",
        "Matn ichidagi barcha ortiqcha ko'p bo'shliqlarni bitta bo'shliqqa keltiring.",
        """SELECT REGEXP_REPLACE('Toshkent   shahar     Chilonzor', '\\s+', ' ', 'g') AS toza_matn;""",
        "'REGEXP_REPLACE(matn, pattern, replacement, flags)' dagi 'g' (global) bayrog'i barcha mosliklarni bitta bo'shliq bilan almashtiradi.",
        """         toza_matn          
----------------------------
 Toshkent shahar Chilonzor
(1 row)"""
    ),
    (
        563,
        "Muntazam ifodalar orqali qiymat sug'urib olish: REGEXP_MATCHES()",
        "Matn ichidan telefon raqamlarini regex orqali ajratib oling.",
        """SELECT (REGEXP_MATCHES('Mening raqamim +998901234567, aloqaga chiqing', '(\\+998[0-9]{9})'))[1] AS topilgan_raqam;""",
        "'REGEXP_MATCHES()' qavs ichidagi guruhlarni massiv sifatida qaytaradi, `[1]` orqali birinchi guruh olinadi.",
        """ topilgan_raqam 
---------------
 +998901234567
(1 row)"""
    ),
    (
        564,
        "Joriy sana va vaqt funksiyalari: NOW() vs CLOCK_TIMESTAMP()",
        "PostgreSQL da NOW() va CLOCK_TIMESTAMP() farqini ko'ring.",
        """SELECT 
    NOW() AS tranzaksiya_vaqti,
    CLOCK_TIMESTAMP() AS soat_vaqti;""",
        "'NOW()' yoki 'CURRENT_TIMESTAMP' butun tranzaksiya boshlangan paytdagi o'zgarmas vaqtni saqlaydi. 'CLOCK_TIMESTAMP()' esa haqiqiy joriy vaqtni mikrosaniyasigacha o'qib beradi.",
        """       tranzaksiya_vaqti       |          soat_vaqti           
-------------------------------+-------------------------------
 2026-11-08 12:00:00.123456+05 | 2026-11-08 12:00:00.123499+05
(1 row)"""
    ),
    (
        565,
        "Faqat joriy sana va faqat joriy vaqt",
        "Vaqtsiz sana (CURRENT_DATE) va sanasiz vaqt (CURRENT_TIME).",
        """SELECT 
    CURRENT_DATE AS bugun,
    CURRENT_TIME AS joriy_soat;""",
        "Faqat sana bilan ishlaganda CURRENT_DATE xotira va formatlashni soddalashtiradi.",
        """   bugun    |    joriy_soat     
------------+-------------------
 2026-11-08 | 12:00:00.12345+05
(1 row)"""
    ),
    (
        566,
        "Sananing qismlarini ajratish: EXTRACT()",
        "Sanadan yil, oy, kun va haftaning kunini ajratib oling.",
        """SELECT 
    EXTRACT(YEAR FROM NOW()) AS yil,
    EXTRACT(MONTH FROM NOW()) AS oy,
    EXTRACT(DAY FROM NOW()) AS kun,
    EXTRACT(ISODOW FROM NOW()) AS hafta_kuni;""",
        "'EXTRACT(field FROM source)' har qanday sana yoki intervaldan butun yoki kasr qismini chiqaradi. ISODOW: 1=Dushanba ... 7=Yakshanba.",
        """ yil  | oy | kun | hafta_kuni 
------+----+-----+------------
 2026 | 11 |   8 |          7
(1 row)"""
    ),
    (
        567,
        "Unix Timestamp (EPOCH soniyalari) ga o'girish",
        "Sanani 1970-yil 1-yanvardan beri o'tgan soniyalar soniga (Unix Epoch) aylantiring.",
        """SELECT 
    EXTRACT(EPOCH FROM NOW())::BIGINT AS unix_epoch_soniyalar,
    TO_TIMESTAMP(1762588800) AS sanaga_qaytish;""",
        "'EXTRACT(EPOCH FROM ...)' Unix vaqtini beradi, 'TO_TIMESTAMP(epoch)' esa soniyadan yana PostgreSQL sanasini tiklaydi.",
        """ unix_epoch_soniyalar |     sanaga_qaytish     
----------------------+------------------------
           1794121200 | 2025-11-08 13:00:00+05
(1 row)"""
    ),
    (
        568,
        "Sanalarni yaxlitlash: DATE_TRUNC()",
        "Sanani oyning boshiga, yilning boshiga yoki soatning boshiga to'g'rilang.",
        """SELECT 
    DATE_TRUNC('year', NOW())::DATE AS yil_boshi,
    DATE_TRUNC('month', NOW())::DATE AS oy_boshi,
    DATE_TRUNC('day', NOW()) AS kun_boshi;""",
        "'DATE_TRUNC(birlik, sana)' vaqt seriyalarini analitik guruhlashda (Oylar, Yillar, Haftalar bo'yicha) asosiy poydevor hisoblanadi.",
        """ yil_boshi  |  oy_boshi  |       kun_boshi        
------------+------------+------------------------
 2026-01-01 | 2026-11-01 | 2026-11-08 00:00:00+05
(1 row)"""
    ),
    (
        569,
        "Yillik choraklar bo'yicha yaxlitlash (Quarter)",
        "Sana qaysi chorakka (Q1, Q2, Q3, Q4) tegishli ekanligini DATE_TRUNC va EXTRACT orqali toping.",
        """SELECT 
    EXTRACT(QUARTER FROM NOW()) AS chorak_raqami,
    DATE_TRUNC('quarter', NOW())::DATE AS chorak_boshi;""",
        "Moliyaviy hisobotlarda choraklik (Quarterly) tahlil shunday quriladi.",
        """ chorak_raqami | chorak_boshi 
----------------+--------------
              4 | 2026-10-01
(1 row)"""
    ),
    (
        570,
        "Oradagi yosh va davrni hisoblash: AGE()",
        "Tug'ilgan sanadan to bugungi kungacha necha yil, necha oy va kun o'tganini aniqlang.",
        """SELECT AGE('1995-04-15'::DATE) AS xodim_yoshi;""",
        "'AGE(sana)' yoki 'AGE(sana1, sana2)' ikki sana orasidagi aniq vaqt oralig'ini '31 years 6 mons 24 days' ko'rinishidagi INTERVAL formatida chiqaradi.",
        """       xodim_yoshi        
--------------------------
 31 years 6 mons 24 days
(1 row)"""
    ),
    (
        571,
        "INTERVAL arifmetikasi (Qo'shish va ayirish)",
        "Bugungi kunga 3 oy va 10 kun qo'shish, hamda 2 soat ayirish amali.",
        """SELECT 
    CURRENT_DATE + INTERVAL '3 months 10 days' AS kelajak_sana,
    NOW() - INTERVAL '2 hours 30 minutes' AS otgan_vaqt;""",
        "PostgreSQL INTERVAL turlari bilan insoniy tilda matematik arifmetika bajarishga imkon beradi.",
        """      kelajak_sana       |          otgan_vaqt           
-------------------------+-------------------------------
 2027-02-18 00:00:00     | 2026-11-08 09:30:00.123456+05
(1 row)"""
    ),
    (
        572,
        "Ikki sana orasidagi kunlar soni (Oddiy ayirish)",
        "Ikki DATE turini bir-biridan ayirganda INTEGER (kunlar soni) chiqishini ko'ring.",
        """SELECT ('2026-12-31'::DATE - '2026-01-01'::DATE) AS yildagi_kunlar_soni;""",
        "PostgreSQL da ikkita DATE ayirilsa, oraliqdagi kunlar soni to'g'ridan-to'g'ri butun son sifatida qaytadi.",
        """ yildagi_kunlar_soni 
---------------------
                 364
(1 row)"""
    ),
    (
        573,
        "Sanalarni chiroyli matnga formatlash: TO_CHAR()",
        "Sanani '08-Noyabr, 2026-yil, 14:30' shaklida formatlab chiqaring.",
        """SELECT TO_CHAR(NOW(), 'DD-TMMonth, YYYY-yil, HH24:MI') AS formatli_sana;""",
        "'TO_CHAR(sana, shablon)' sana va vaqtni istalgan ko'rinishda chiroyli matnga o'giradi. 'TM' prefiksi (Translation Mode) mahalliy oylar nomini chiqaradi.",
        """          formatli_sana          
---------------------------------
 08-November , 2026-yil, 12:00
(1 row)"""
    ),
    (
        574,
        "Matnni sanaga o'tkazish: TO_DATE() va TO_TIMESTAMP()",
        "'25/12/2026' shaklidagi nostandart matnni PostgreSQL DATE turiga o'giring.",
        """SELECT 
    TO_DATE('25/12/2026', 'DD/MM/YYYY') AS haqiqiy_sana,
    TO_TIMESTAMP('2026-05-10 14:45:00', 'YYYY-MM-DD HH24:MI:SS') AS haqiqiy_vaqt;""",
        "Noto'g'ri formatdagi kiruvchi fayllarni (Excel, CSV) qabul qilishda TO_DATE juda muhim.",
        """ haqiqiy_sana |      haqiqiy_vaqt      
-------------+------------------------
 2026-12-25  | 2026-05-10 14:45:00+05
(1 row)"""
    ),
    (
        575,
        "Vaqt mintaqasi (Time Zone) konvertatsiyasi: AT TIME ZONE",
        "Toshkent vaqtini Nyu-York (EST) va Tokio (JST) vaqtlariga o'tkazing.",
        """SELECT 
    NOW() AT TIME ZONE 'Asia/Tashkent' AS toshkent_vaqti,
    NOW() AT TIME ZONE 'America/New_York' AS new_york_vaqti,
    NOW() AT TIME ZONE 'Asia/Tokyo' AS tokyo_vaqti;""",
        "'AT TIME ZONE' vaqtni boshqa xalqaro mintaqaga bir zumda konvertatsiya qiladi.",
        """      toshkent_vaqti       |       new_york_vaqti       |        tokyo_vaqti         
---------------------------+----------------------------+----------------------------
 2026-11-08 12:00:00.123456| 2026-11-08 02:00:00.123456 | 2026-11-08 16:00:00.123456
(1 row)"""
    ),
    (
        576,
        "Oyning oxirgi kunini topish",
        "Keyingi oyning 1-kunidan 1 kun ayirish orqali joriy oyning oxirgi kunini aniqlang.",
        """SELECT (DATE_TRUNC('month', NOW()) + INTERVAL '1 month' - INTERVAL '1 day')::DATE AS oyning_oxirgi_kuni;""",
        "Fevral 28 yoki 29, 30 yoki 31 kunligini hisobga oluvchi universal formula.",
        """ oyning_oxirgi_kuni 
--------------------
 2026-11-30
(1 row)"""
    ),
    (
        577,
        "Kabisa yilini tekshirish (Leap Year)",
        "Yilda 366 kun bor-yo'qligini tekshiruvchi SQL ifodasini yozing.",
        """SELECT 
    2026 AS yil,
    ('2026-12-31'::DATE - '2026-01-01'::DATE + 1 = 366) AS kabisa_yilimi;""",
        "366 kun bo'lsa TRUE, 365 kun bo'lsa FALSE chiqadi.",
        """ yil  | kabisa_yilimi 
------+---------------
 2026 | f
(1 row)"""
    ),
    (
        578,
        "Vaqt oralig'ini soniyalarga aylantirish",
        "2 soat 45 daqiqaning jami necha soniya ekanligini hisoblang.",
        """SELECT EXTRACT(EPOCH FROM INTERVAL '2 hours 45 minutes')::INT AS jami_soniyalar;""",
        "INTERVAL ustida EXTRACT(EPOCH) umumiy soniyalar miqdorini qaytaradi.",
        """ jami_soniyalar 
-----------------
            9900
(1 row)"""
    ),
    (
        579,
        "Ikki vaqt oralig'idagi ish soatlarini hisoblash",
        "Boshlanish va tugash vaqti orasidagi sof farqni soatlarda ifodalang.",
        """SELECT ROUND(
    (EXTRACT(EPOCH FROM ('2026-06-01 18:30:00'::TIMESTAMP - '2026-06-01 09:00:00'::TIMESTAMP)) / 3600)::NUMERIC, 
    2
) AS ishlangan_soatlar;""",
        "Soniyalarni 3600 ga bo'lish orqali aniq kasr soatlar (9.5 soat) olinadi.",
        """ ishlangan_soatlar 
------------------
             9.50
(1 row)"""
    ),
    (
        580,
        "Haftaning ma'lum kunini topish (Keyingi dushanba)",
        "Ixtiyoriy sanadan keyingi eng yaqin dushanba kunini hisoblash.",
        """SELECT ('2026-11-08'::DATE + ((8 - EXTRACT(ISODOW FROM '2026-11-08'::DATE)::INT) % 7 || ' days')::INTERVAL)::DATE AS keyingi_dushanba;""",
        "Modul (%) arifmetikasi bilan eng yaqin ish haftasi boshlanishi aniqlanadi.",
        """ keyingi_dushanba 
-------------------
 2026-11-09
(1 row)"""
    ),
    (
        581,
        "Matndan raqamlarni ajratib olish (REGEXP_REPLACE)",
        "Harflar va belgilardan iborat matndan faqatgina sonlarni qoldiring.",
        """SELECT REGEXP_REPLACE('Buyurtma #A-98745/2026', '[^0-9]', '', 'g') AS toza_raqamlar;""",
        "'[^0-9]' raqam bo'lmagan barcha belgilarni topadi va bo'shliqqa almashtiradi.",
        """ toza_raqamlar 
---------------
 987452026
(1 row)"""
    ),
    (
        582,
        "MD5 va SHA256 kriptografik xeshlash",
        "Parol yoki matnning MD5 va SHA256 xesh summasini hisoblang.",
        """CREATE EXTENSION IF NOT EXISTS pgcrypto;

SELECT 
    MD5('maxfiy_parol') AS md5_xesh,
    ENCODE(DIGEST('maxfiy_parol', 'sha256'), 'hex') AS sha256_xesh;""",
        "PostgreSQL o'rnatilgan MD5 hamda pgcrypto moduli orqali sanoat standartidagi SHA256 xeshlarini generatsiya qiladi.",
        """CREATE EXTENSION
             md5_xesh             |                           sha256_xesh                            
----------------------------------+------------------------------------------------------------------
 ebc35fef6d27ca5e45447fb50d3e0988 | e20e0657960ea9b027b4b1a41db86f55462ee67d32c5aa8c05e1975e1823eb97
(1 row)"""
    ),
    (
        583,
        "Tasodifiy belgilar satri generatsiyasi (Tasodifiy parol)",
        "Tasodifiy 8 belgili xavfsiz kod hosil qiling.",
        """SELECT SUBSTRING(MD5(RANDOM()::TEXT) FROM 1 FOR 8) AS tasodifiy_kod;""",
        "RANDOM va MD5 birikmasi tezkor vaqtinchalik parol va tokenlar yasaydi.",
        """ tasodifiy_kod 
----------------
 4f8b2c1a
(1 row)"""
    ),
    (
        584,
        "Sana qatorlarini ketma-ket generatsiya qilish: generate_series()",
        "Bir sanadan ikkinchi sanagacha bo'lgan barcha kunlarni qatorlar qilib chiqaring.",
        """SELECT kun::DATE 
FROM generate_series('2026-12-01'::DATE, '2026-12-03'::DATE, '1 day'::INTERVAL) AS kun;""",
        "Hisobotlarda ma'lumotlar uzluksizligini ta'minlovchi asosiy funksiya.",
        """    kun     
------------
 2026-12-01
 2026-12-02
 2026-12-03
(3 rows)"""
    ),
    (
        585,
        "Harflar o'rnini almashtirish: TRANSLATE()",
        "Matndagi kirill 'a, b, c' harflarini lotin muqobiliga birdaniga almashtirish.",
        """SELECT TRANSLATE('abc', 'abc', '123') AS almashtirilgan;""",
        "'TRANSLATE(satr, qidiriluvchi, almashtiriluvchi)' har bir belgini o'z o'rnidagi belgiga bittalab moslaydi.",
        """ almashtirilgan 
----------------
 123
(1 row)"""
    ),
    (
        586,
        "Qatorni massivga ajratish: STRING_TO_ARRAY()",
        "Vergulli matnni PostgreSQL massiviga o'giring.",
        """SELECT STRING_TO_ARRAY('olma,anor,uzum,shaftoli', ',') AS mevalar_massivi;""",
        "CSV ko'rinishidagi satrlarni massivga aylantiradi.",
        """     mevalar_massivi      
--------------------------
 {olma,anor,uzum,shaftoli}
(1 row)"""
    ),
    (
        587,
        "Massivni yana matnga birlashtirish: ARRAY_TO_STRING()",
        "Massiv elementlarini chiziqcha (-) bilan ajratilgan bitta matn qiling.",
        """SELECT ARRAY_TO_STRING(ARRAY['Toshkent', 'Samarqand', 'Buxoro'], ' - ') AS marshrut_matni;""",
        "Massivlarni chiroyli formatda ko'rsatishda qo'llanadi.",
        """        marshrut_matni         
------------------------------
 Toshkent - Samarqand - Buxoro
(1 row)"""
    ),
    (
        588,
        "Sana formatlashda hafta raqamini olish (ISO Week)",
        "Yilning nechanchi haftasi ekanligini hisoblang.",
        """SELECT 
    EXTRACT(WEEK FROM NOW()) AS hafta_raqami,
    TO_CHAR(NOW(), 'IYYY-IW') AS iso_yil_va_hafta;""",
        "Ishlab chiqarish va yetkazib berish grafiklari ISO haftalar (W01 ... W52) bo'yicha tuziladi.",
        """ hafta_raqami | iso_yil_va_hafta 
--------------+------------------
           45 | 2026-45
(1 row)"""
    ),
    (
        589,
        "Bo'sh satr yoki bo'shliqlarni aniqlash funksiyasi",
        "Satr haqiqiy ma'noli belgiga egami yoki faqat bo'shliqlarmi?",
        """SELECT 
    ism,
    (NULLIF(TRIM(ism), '') IS NULL) AS yaroqsizmi
FROM (VALUES ('   '), ('Ali'), ('')) AS t(ism);""",
        "'NULLIF(TRIM(matn), '')' barcha bo'sh qatorlarni yagona NULL ga aylantiradi.",
        """ ism | yaroqsizmi 
-----+------------
     | t
 Ali | f
     | t
(3 rows)"""
    ),
    (
        590,
        "Takrorlanuvchi matn generatsiyasi: REPEAT()",
        "Reyting balliga qarab yulduzchalar (⭐⭐⭐⭐⭐) chiqarish.",
        """SELECT 
    ism, ball,
    REPEAT('★', ball) || REPEAT('☆', 5 - ball) AS yulduzlar
FROM (VALUES ('Ali', 4), ('Vali', 5), ('Gani', 3)) AS r(ism, ball);""",
        "REPEAT vizual progress-bar va yulduzchalarni konsolda chizishda juda qo'l keladi.",
        """ ism  | ball | yulduzlar 
------+------+-----------
 Ali  |    4 | ★★★★☆
 Vali |    5 | ★★★★★
 Gani |    3 | ★★★☆☆
(3 rows)"""
    ),
    (
        591,
        "Soat, daqiqa, soniyani alohida yasash: MAKE_TIME()",
        "Raqamlardan TIME turini hosil qiling.",
        """SELECT MAKE_TIME(14, 30, 00) AS dars_vaqti;""",
        "Raqamli o'zgaruvchilarni toza TIME ga aylantiradi.",
        """ dars_vaqti 
------------
 14:30:00
(1 row)"""
    ),
    (
        592,
        "Sanani alohida raqamlardan yasash: MAKE_DATE()",
        "Yil, oy va kundan DATE hosil qilish.",
        """SELECT MAKE_DATE(2026, 9, 1) AS mustaqillik_kuni;""",
        "Yil, oy, kun parametrlaridan to'g'ridan-to'g'ri kalendar sanasi hosil qilinadi.",
        """ mustaqillik_kuni 
-------------------
 2026-09-01
(1 row)"""
    ),
    (
        593,
        "Sana vaqt zonasini o'rnatish: SET TIME ZONE",
        "Joriy sessiyaning vaqt mintaqasini vaqtincha UTC ga o'zgartirish.",
        """SET TIME ZONE 'UTC';
SELECT NOW() AS utc_vaqti;
SET TIME ZONE 'Asia/Tashkent';""",
        "Sessiyaning vaqt zonasi sozlamasi barcha TIMESTAMPTZ ko'rinishlariga ta'sir qiladi.",
        """SET
          utc_vaqti           
------------------------------
 2026-11-08 07:00:00.12345+00
(1 row)
SET"""
    ),
    (
        594,
        "Matn ichidagi qatorlar sonini aniqlash",
        "Ko'p qatorli TEXT matnida nechta qator (Enter) borligini sanang.",
        """SELECT CARDINALITY(STRING_TO_ARRAY('Birinchi qator\nIkkinchi qator\nUchinchi', '\n')) AS qatorlar_soni;""",
        "STRING_TO_ARRAY va CARDINALITY matndagi qatorlar sonini bir zumda aytadi.",
        """ qatorlar_soni 
---------------
             3
(1 row)"""
    ),
    (
        595,
        "LEFT va RIGHT qator funksiyalari",
        "Satrning eng chap yoki eng o'ng tomonidagi N ta belgini olish.",
        """SELECT 
    LEFT('TOSHKENT', 4) AS chap_4,
    RIGHT('TOSHKENT', 4) AS ong_4;""",
        "SUBSTRING ga qaraganda soddaroq va ixchamroq sintaksis.",
        """ chap_4 | ong_4 
--------+-------
 TOSH   | KENT
(1 row)"""
    ),
    (
        596,
        "Vaqt oralig'i (Interval) ustida ko'paytirish va bo'lish",
        "15 daqiqalik dars tanaffusini 4 barobarga oshirish.",
        """SELECT INTERVAL '15 minutes' * 4 AS jami_tanaffus;""",
        "INTERVAL turlari butun yoki kasr sonlarga to'g'ridan-to'g'ri ko'paytiriladi.",
        """ jami_tanaffus 
---------------
 01:00:00
(1 row)"""
    ),
    (
        597,
        "Vaqtlar kesishuvini OVERLAPS bilan tekshirish",
        "Ikki sana oralig'ining bir-biriga tushib qolishini SQL standartidagi OVERLAPS bilan aniqlang.",
        """SELECT (DATE '2026-05-01', DATE '2026-05-10') OVERLAPS 
       (DATE '2026-05-08', DATE '2026-05-15') AS kesishadimi;""",
        "'OVERLAPS' ANSI SQL ning o'rnatilgan operatori bo'lib, ikkita vaqt oralig'ining kesishuvini tekshiradi.",
        """ kesishadimi 
-------------
 t
(1 row)"""
    ),
    (
        598,
        "Sana ustuniga B-Tree indeks qo'yilganda funksiya xavfi (SARGability)",
        "Nega `WHERE EXTRACT(YEAR FROM sana) = 2026` indeksni o'ldirishi va uning to'g'ri yozilishini ko'rsating.",
        """-- Sekin (Indeks ishlamaydi):
-- WHERE EXTRACT(YEAR FROM sana) = 2026;

-- Tez va SARGable (Indeks to'liq ishlaydi):
-- WHERE sana >= '2026-01-01' AND sana < '2027-01-01';
SELECT 'Indekslangan ustunni funksiya ichiga o‘rash Index Scanni yo‘qotadi!' AS ogohlantirish;""",
        "SARGable (Search Argument Able): ustun hech qanday funksiya ichiga olinmasdan sof holda taqqoslanishi shart, aks holda optimizator Seq Scanga tushadi.",
        """                                    ogohlantirish                                     
--------------------------------------------------------------------------------------
 Indekslangan ustunni funksiya ichiga o‘rash Index Scanni yo‘qotadi!
(1 row)"""
    ),
    (
        599,
        "Matn o'xshashligini tekshirish (Levenshtein masofasi)",
        "Imloviy xatolarni qidirish uchun ikkita so'z orasidagi Levenshtein masofasini hisoblang.",
        """CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;

SELECT LEVENSHTEIN('Toshkent', 'Tashkent') AS tahrir_masofasi;""",
        "Levenshtein masofasi bitta so'zni ikkinchisiga aylantirish uchun nechta harfni o'zgartirish kerakligini bildiradi (bu yerda 'o' -> 'a', masofa 1). Qidiruvdagi imlo tuzatishlarida ishlatiladi.",
        """CREATE EXTENSION
 tahrir_masofasi 
-----------------
               1
(1 row)"""
    ),
    (
        600,
        "Korporativ Vaqt va Matn Mexanizmi: Xalqaro SLA va Ish Vaqti Tahlili",
        "Texnik qo'llab-quvvatlash xizmatiga (HelpDesk) kelgan murojaatning dam olish kunlari va kechki soatlarni chiqarib tashlagan holda haqiqiy ish vaqtini (SLA) daqiqalarda hisoblang va hisobot qiling.",
        """CREATE TABLE mijoz_murojaatlari (
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
FROM mijoz_murojaatlari;""",
        "Ushbu korporativ so'rov IT-Service Management (ITSM, Jira, Zendesk) tizimlarining Service Level Agreement (SLA) nazorati markazidir: sana va vaqt arifmetikasi, AGE(), TO_CHAR() formatlashlari va daqiqalar hisobi orqali mijozlar shikoyatlarining o'z vaqtida hal etilishi shaffof nazorat qilinadi.",
        """ ticket_id |      mijoz      |     ochilgan     |     yopilgan     |  toliq_kalendar_farqi  | jami_daqiqalar |          sla_holati          
-----------+-----------------+------------------+------------------+------------------------+----------------+------------------------------
         1 | Anvar Qodirov   | 2026-10-01 09:15 | 2026-10-01 11:45 | 02:30:00               |            150 | ✅ SLA Bajarildi
         2 | Dilnoza Alimova | 2026-10-02 17:30 | 2026-10-05 10:00 | 2 days 16:30:00        |           3870 | ⚠️ SLA Buzildi (Kechikish)
(2 rows)"""
    )
]

formatted = [format_task(*item) for item in str_date_data]
save_file("sql_12_qator_va_sana_funksiyalari.md", formatted)
