import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

# List of 50 tasks for File 13: 601 - 650
# Shartli mantiq: CASE, COALESCE, NULLIF, GREATEST, LEAST, 3-Valued Logic, Conditional Aggregation, Pivot

case_data = [
    (
        601,
        "Oddiy CASE ifodasi (Simple CASE)",
        "Buyurtma holati kodini (1, 2, 3) inson tushunadigan so'zlarga almashtiring.",
        """CREATE TABLE buyurtmalar_case (
    id SERIAL PRIMARY KEY,
    mijoz VARCHAR(50),
    status_kod SMALLINT,
    summa NUMERIC(12, 2)
);

INSERT INTO buyurtmalar_case (mijoz, status_kod, summa) VALUES 
('Sherzod', 1, 150000),
('Dildora', 2, 250000),
('Akmal', 3, 500000),
('Zilola', 99, 100000);

SELECT 
    mijoz,
    status_kod,
    CASE status_kod
        WHEN 1 THEN 'Yangi qabul qilingan'
        WHEN 2 THEN 'Yetkazib berilmoqda'
        WHEN 3 THEN 'Muvaffaqiyatli topshirildi'
        ELSE 'Noma''lum holat'
    END AS holat_matni
FROM buyurtmalar_case;""",
        "'Simple CASE' ustun nomini 'CASE' dan so'ng darhol qabul qiladi va uning qiymatini 'WHEN qiymat' bilan aynan tenglikka (`=`) tekshiradi. Mos kelmaganlar ELSE ga o'tadi.",
        """  mijoz  | status_kod |        holat_matni         
---------+------------+----------------------------
 Sherzod |          1 | Yangi qabul qilingan
 Dildora |          2 | Yetkazib berilmoqda
 Akmal   |          3 | Muvaffaqiyatli topshirildi
 Zilola  |         99 | Noma'lum holat
(4 rows)"""
    ),
    (
        602,
        "Qidiruvli CASE ifodasi (Searched CASE)",
        "Xarid summasiga qarab xaridorga chegirma darajasini (VIP >= 400k, Standart >= 200k, Boshlang'ich) belgilang.",
        """SELECT 
    mijoz,
    summa,
    CASE 
        WHEN summa >= 400000 THEN 'Platinum (VIP)'
        WHEN summa >= 200000 THEN 'Gold (Standart)'
        ELSE 'Silver (Boshlang''ich)'
    END AS mijoz_darajasi
FROM buyurtmalar_case;""",
        "'Searched CASE' har bir WHEN dan so'ng mustaqil mantiqiy ifodani (`summa >= 400000`) qabul qiladi. Bu taqqoslashlar, oraliqlar va murakkab shartlar uchun eng ko'p ishlatiladigan variantdir.",
        """  mijoz  |   summa   |    mijoz_darajasi     
---------+-----------+-----------------------
 Sherzod | 150000.00 | Silver (Boshlang'ich)
 Dildora | 250000.00 | Gold (Standart)
 Akmal   | 500000.00 | Platinum (VIP)
 Zilola  | 100000.00 | Silver (Boshlang'ich)
(4 rows)"""
    ),
    (
        603,
        "CASE da ELSE bandini unutish xavfi",
        "Agar ELSE yozilmasa va shartlarning birortasi ham mos kelmasa natija nima bo'lishini ko'ring.",
        """SELECT 
    mijoz,
    status_kod,
    CASE status_kod
        WHEN 1 THEN 'Yangi'
        WHEN 2 THEN 'Yetkazilmoqda'
    END AS holat_elsiz
FROM buyurtmalar_case;""",
        "SQL qoidasiga ko'ra, agar CASE da ELSE berilmagan bo'lsa, mos kelmagan barcha qatorlar uchun sukut bo'yicha NULL qaytariladi (Akmal va Zilola misolida). Kutilmagan NULL lardan saqlanish uchun har doim ELSE yozish tavsiya etiladi.",
        """  mijoz  | status_kod |  holat_elsiz  
---------+------------+---------------
 Sherzod |          1 | Yangi
 Dildora |          2 | Yetkazilmoqda
 Akmal   |          3 | NULL
 Zilola  |         99 | NULL
(4 rows)"""
    ),
    (
        604,
        "Birinchi uchragan qiymatni tanlash: COALESCE asoslari",
        "Mijozning telefon raqami, agar u bo'lmasa uy telefoni, u ham bo'lmasa elektron pochtasini bitta kontakt ustuniga oling.",
        """CREATE TABLE kontaktlar_case (
    id SERIAL PRIMARY KEY,
    ism VARCHAR(50),
    mobil_tel VARCHAR(20),
    uy_tel VARCHAR(20),
    email VARCHAR(100)
);

INSERT INTO kontaktlar_case (ism, mobil_tel, uy_tel, email) VALUES 
('Ali', '+998901112233', '+998712001122', 'ali@mail.uz'),
('Vali', NULL, '+998712003344', 'vali@mail.uz'),
('Gani', NULL, NULL, 'gani@mail.uz'),
('Botir', NULL, NULL, NULL);

SELECT 
    ism,
    COALESCE(mobil_tel, uy_tel, email, 'Aloqa vositasi yo''q') AS asosiy_aloqa
FROM kontaktlar_case;""",
        "'COALESCE(a, b, c, ...)' berilgan ro'yxatdan birinchi uchragan NOT NULL qiymatni qaytaradi. Agar barchasi NULL bo'lsa, oxirgi zaxira matn chiqadi.",
        """  ism  |     asosiy_aloqa     
-------+----------------------
 Ali   | +998901112233
 Vali  | +998712003344
 Gani  | gani@mail.uz
 Botir | Aloqa vositasi yo'q
(4 rows)"""
    ),
    (
        605,
        "COALESCE bilan nolga aylantirish (Zero fallback)",
        "NULL bo'lgan narx yoki miqdorlarni hisob-kitoblarda 0 deb qabul qiling.",
        """CREATE TABLE hisoblar_null (balans NUMERIC, bonus NUMERIC);
INSERT INTO hisoblar_null VALUES (100000, 20000), (50000, NULL), (NULL, NULL);

SELECT 
    balans, bonus,
    COALESCE(balans, 0) + COALESCE(bonus, 0) AS jami_kapital
FROM hisoblar_null;""",
        "SQL da `NULL + 20000 = NULL` bo'ladi! Moliyaviy arifmetikada bitta NULL butun yig'indini yo'q qilmasligi uchun har doim COALESCE(ustun, 0) ishlatiladi.",
        """  balans   |  bonus   | jami_kapital 
-----------+----------+--------------
 100000.00 | 20000.00 |    120000.00
  50000.00 |     NULL |     50000.00
      NULL |     NULL |         0.00
(3 rows)"""
    ),
    (
        606,
        "Teng bo'lsa NULL ga aylantirish: NULLIF() asoslari",
        "Nolga bo'lish (Division by zero) xatosini NULLIF bilan to'liq bartaraf qiling.",
        """CREATE TABLE bolinma_test (daromad NUMERIC, xodimlar_soni INT);
INSERT INTO bolinma_test VALUES (10000000, 5), (5000000, 0);

SELECT 
    daromad, 
    xodimlar_soni,
    ROUND(daromad / NULLIF(xodimlar_soni, 0), 2) AS xodim_boshiga_daromad
FROM bolinma_test;""",
        "'NULLIF(a, b)' agar a = b bo'lsa NULL qaytaradi, aks holda a ning o'zini qaytaradi. 'NULLIF(xodimlar_soni, 0)' 0 ni NULL ga aylantiradi, `daromad / NULL` esa xato bermay xavfsiz NULL chiqaradi.",
        """  daromad   | xodimlar_soni | xodim_boshiga_daromad 
------------+---------------+-----------------------
 10000000.00|             5 |            2000000.00
  5000000.00|             0 |                  NULL
(2 rows)"""
    ),
    (
        607,
        "Bir nechta ustunlardan eng kattasini olish: GREATEST()",
        "Mahsulotning do'kondagi narxi, onlayn narxi va aksiyadagi narxlaridan eng balandini tanlang.",
        """CREATE TABLE narxlar_solishtirish (dokon NUMERIC, onlayn NUMERIC, aksiya NUMERIC);
INSERT INTO narxlar_solishtirish VALUES (15000, 14000, 18000), (22000, 25000, NULL);

SELECT 
    dokon, onlayn, aksiya,
    GREATEST(dokon, onlayn, aksiya) AS eng_yuqori_narx
FROM narxlar_solishtirish;""",
        "'GREATEST(a, b, c, ...)' bir xil qatordagi bir nechta ustunlar orasidan eng katta qiymatni oladi (MAX esa qatorlar bo'ylab olinadi). Agar ba'zi qiymatlar NULL bo'lsa, GREATEST ularni e'tiborsiz qoldiradi.",
        """  dokon   |  onlayn  |  aksiya  | eng_yuqori_narx 
----------+----------+----------+-----------------
 15000.00 | 14000.00 | 18000.00 |        18000.00
 22000.00 | 25000.00 |     NULL |        25000.00
(2 rows)"""
    ),
    (
        608,
        "Bir nechta ustunlardan eng kichigini olish: LEAST()",
        "Tovarga qo'llanishi mumkin bo'lgan eng arzon narxni aniqlang.",
        """SELECT 
    dokon, onlayn, aksiya,
    LEAST(dokon, onlayn, aksiya) AS eng_arzon_narx
FROM narxlar_solishtirish;""",
        "'LEAST(a, b, c, ...)' satr ichidagi eng minimal ustun qiymatini tanlab beradi.",
        """  dokon   |  onlayn  |  aksiya  | eng_arzon_narx 
----------+----------+----------+----------------
 15000.00 | 14000.00 | 18000.00 |       14000.00
 22000.00 | 25000.00 |     NULL |       22000.00
(2 rows)"""
    ),
    (
        609,
        "Uch qiymatli mantiq (Three-Valued Logic - 3VL): UNKNOWN",
        "NULL bilan mantiqiy AND va OR amallarining haqiqat jadvalini (Truth table) sinang.",
        """SELECT 
    (TRUE AND NULL) AS "TRUE and NULL",
    (FALSE AND NULL) AS "FALSE and NULL",
    (TRUE OR NULL) AS "TRUE or NULL",
    (FALSE OR NULL) AS "FALSE or NULL",
    (NOT NULL) AS "NOT NULL";""",
        "Relyatsion algebrada NULL = UNKNOWN. `FALSE AND NULL` har doim FALSE (chunki bir tomoni yolg'on), lekin `TRUE AND NULL` noma'lum (NULL) bo'lib qoladi. `TRUE OR NULL` esa doimo TRUE!",
        """ TRUE and NULL | FALSE and NULL | TRUE or NULL | FALSE or NULL | NOT NULL 
---------------+----------------+--------------+---------------+----------
 NULL          | f              | t            | NULL          | NULL
(1 row)"""
    ),
    (
        610,
        "Mantiqiy predikatlar: IS TRUE, IS FALSE, IS UNKNOWN",
        "Mantiqiy ifodani xavfsiz tekshiruvchi maxsus SQL predikatlarini qo'llang.",
        """SELECT 
    (1 = 1) IS TRUE AS tekshiruv_1,
    (1 = 2) IS FALSE AS tekshiruv_2,
    (NULL = NULL) IS UNKNOWN AS tekshiruv_3;""",
        "'IS TRUE', 'IS FALSE', 'IS UNKNOWN' predikatlari o'zlari HECH QACHON NULL qaytarmaydi, ular faqat qat'iy TRUE yoki FALSE qaytaradi.",
        """ tekshiruv_1 | tekshiruv_2 | tekshiruv_3 
-------------+-------------+-------------
 t           | t           | t
(1 row)"""
    ),
    (
        611,
        "Shartli agregatsiya: COUNT(CASE WHEN ...)",
        "Bitta so'rovda jami buyurtmalar soni, yangi buyurtmalar soni va yetkazilganlar sonini alohida ustunlarda sanang.",
        """SELECT 
    COUNT(*) AS jami_buyurtmalar,
    COUNT(CASE WHEN status_kod = 1 THEN 1 END) AS yangilar_soni,
    COUNT(CASE WHEN status_kod = 3 THEN 1 END) AS bajarilganlar_soni
FROM buyurtmalar_case;""",
        "COUNT faqat NOT NULL larni sanaydi. CASE da ELSE yozilmaganligi sababli, mos kelmagan qatorlar NULL bo'ladi va COUNT ularni hisobga olmaydi. Shartli sanashning eng tezkor usuli.",
        """ jami_buyurtmalar | yangilar_soni | bajarilganlar_soni 
-------------------+---------------+--------------------
                 4 |             1 |                  1
(1 row)"""
    ),
    (
        612,
        "Shartli jamlash: SUM(CASE WHEN ...)",
        "Faqat topshirilgan buyurtmalarning umumiy pul summasini bitta SELECT da jamlang.",
        """SELECT 
    SUM(summa) AS umumiy_aylanma,
    SUM(CASE WHEN status_kod = 3 THEN summa ELSE 0 END) AS tasdiqlangan_tushum
FROM buyurtmalar_case;""",
        "SUM(CASE WHEN ...) faqat kerakli statusdagi qatorlar summasini oladi, qolganlariga 0 qo'shadi.",
        """ umumiy_aylanma | tasdiqlangan_tushum 
-----------------+---------------------
      1000000.00 |           500000.00
(1 row)"""
    ),
    (
        613,
        "Dinamik PIVOT: CASE yordamida qatorlarni ustunlarga aylantirish",
        "Har bir mijozning har xil statusdagi xarajatlarini satrlardan alohida ustunlarga yoying.",
        """SELECT 
    mijoz,
    COALESCE(SUM(CASE WHEN status_kod = 1 THEN summa END), 0) AS yangi_summa,
    COALESCE(SUM(CASE WHEN status_kod = 2 THEN summa END), 0) AS yol_ustida_summa,
    COALESCE(SUM(CASE WHEN status_kod = 3 THEN summa END), 0) AS yetkazilgan_summa
FROM buyurtmalar_case
GROUP BY mijoz;""",
        "Ushbu naqsh relyatsion jadvallarni Excel pivot-jadvallari kabi ustunlarga yoyishning (Cross-tabulation) universal ANSI SQL usulidir.",
        """  mijoz  | yangi_summa | yol_ustida_summa | yetkazilgan_summa 
---------+-------------+------------------+-------------------
 Akmal   |        0.00 |             0.00 |         500000.00
 Dildora |        0.00 |        250000.00 |              0.00
 Sherzod |   150000.00 |             0.00 |              0.00
 Zilola  |        0.00 |             0.00 |              0.00
(4 rows)"""
    ),
    (
        614,
        "WHERE bandida dinamik filtrlash uchun CASE",
        "Agar qidiruv parametri 'BARCHASI' bo'lsa hamma tovarlarni, aks holda faqat ko'rsatilgan toifani filtrlash.",
        """SELECT * 
FROM buyurtmalar_case 
WHERE 
    CASE 
        WHEN 'HAMMASI' = 'HAMMASI' THEN TRUE 
        ELSE status_kod = 1 
    END;""",
        "WHERE bandida CASE yordamida backenddan kelgan filtr parametrlariga qarab dinamik mantiq qurish mumkin.",
        """ id |  mijoz  | status_kod |   summa   
----+---------+------------+-----------
  1 | Sherzod |          1 | 150000.00
  2 | Dildora |          2 | 250000.00
  3 | Akmal   |          3 | 500000.00
  4 | Zilola  |         99 | 100000.00
(4 rows)"""
    ),
    (
        615,
        "ORDER BY da shartli saralash: CASE WHEN bilan",
        "VIP mijozlarni birinchi navbatda, qolgan mijozlarni esa summa bo'yicha saralash.",
        """SELECT mijoz, summa 
FROM buyurtmalar_case 
ORDER BY 
    CASE WHEN summa >= 400000 THEN 0 ELSE 1 END,
    summa DESC;""",
        "CASE orqali saralashda biznes ustuvorligi (VIP flag) 0 va 1 qilib beriladi.",
        """  mijoz  |   summa   
---------+-----------
 Akmal   | 500000.00
 Dildora | 250000.00
 Sherzod | 150000.00
 Zilola  | 100000.00
(4 rows)"""
    ),
    (
        616,
        "GROUP BY da shartli guruhlash: CASE ifodasi",
        "Xaridlarni narx toifalari bo'yicha guruhlab sonini hisoblang.",
        """SELECT 
    CASE 
        WHEN summa < 200000 THEN 'Kichik xarid (< 200k)'
        ELSE 'Yirik xarid (>= 200k)'
    END AS toifa,
    COUNT(*) AS buyurtmalar_soni
FROM buyurtmalar_case 
GROUP BY 
    CASE 
        WHEN summa < 200000 THEN 'Kichik xarid (< 200k)'
        ELSE 'Yirik xarid (>= 200k)'
    END;""",
        "CASE ifodasi qatorlarni virtual toifalarga guruhlash imkonini beradi.",
        """         toifa         | buyurtmalar_soni 
-----------------------+------------------
 Kichik xarid (< 200k) |                2
 Yirik xarid (>= 200k) |                2
(2 rows)"""
    ),
    (
        617,
        "UPDATE da shartli ma'lumotlarni o'zgartirish",
        "Status kodi 1 bo'lganlarga 5% bonus, status kodi 2 bo'lganlarga 10% bonus yozish.",
        """UPDATE buyurtmalar_case 
SET summa = CASE 
    WHEN status_kod = 1 THEN summa * 1.05
    WHEN status_kod = 2 THEN summa * 1.10
    ELSE summa
END;

SELECT mijoz, status_kod, summa FROM buyurtmalar_case;""",
        "Alohida-alohida UPDATE so'rovlari o'rniga bitta atomar UPDATE da har bir toifa o'z qoidasiga ko'ra o'zgaradi.",
        """UPDATE 4
  mijoz  | status_kod |   summa   
---------+------------+-----------
 Akmal   |          3 | 500000.00
 Zilola  |         99 | 100000.00
 Sherzod |          1 | 157500.00
 Dildora |          2 | 275000.00
(4 rows)"""
    ),
    (
        618,
        "Ichma-ich CASE ifodalari (Nested CASE)",
        "Hududga qarab, so'ngra toifaga qarab ko'p qavatli chegirma belgilash.",
        """SELECT 
    mijoz,
    CASE 
        WHEN summa > 200000 THEN 
            CASE WHEN status_kod = 3 THEN 'Katta yetkazilgan' ELSE 'Katta kutilayotgan' END
        ELSE 'Kichik xarid'
    END AS tafsilot
FROM buyurtmalar_case;""",
        "CASE ichida ikkinchi CASE ifodasini yozish mumkin, biroq kod toza bo'lishi uchun ko'pincha 'AND' orqali bitta qavatda yozish tavsiya etiladi.",
        """  mijoz  |     tafsilot      
---------+-------------------
 Akmal   | Katta yetkazilgan
 Zilola  | Kichik xarid
 Sherzod | Kichik xarid
 Dildora | Katta kutilayotgan
(4 rows)"""
    ),
    (
        619,
        "NULL bilan matematik taqqoslashning tuzoqlari",
        "Nega `WHERE maosh > NULL` yoki `WHERE maosh < NULL` hech qachon qator qaytarmasligini ko'ring.",
        """SELECT * FROM buyurtmalar_case WHERE summa > NULL;""",
        "Har qanday qiymatning NULL bilan solishtirilishi UNKNOWN bo'ladi. WHERE faqat TRUE larni o'tkazgani sababli bo'sh natija qaytadi.",
        """ id | mijoz | status_kod | summa 
----+-------+------------+-------
(0 rows)"""
    ),
    (
        620,
        "COALESCE o'rnida CASE ekvivalenti",
        "COALESCE(a, b) orqa fonda aynan qanday CASE ifodasi ekanligini ko'ring.",
        """SELECT 
    COALESCE(mobil_tel, 'Yo''q') AS coalesced,
    CASE WHEN mobil_tel IS NOT NULL THEN mobil_tel ELSE 'Yo''q' END AS case_ekvivalenti
FROM kontaktlar_case
LIMIT 2;""",
        "SQL spetsifikatsiyasiga ko'ra, `COALESCE(e1, e2)` aynan `CASE WHEN e1 IS NOT NULL THEN e1 ELSE e2 END` ga teng qisqartmadir.",
        """   coalesced   | case_ekvivalenti 
---------------+------------------
 +998901112233 | +998901112233
 Yo'q          | Yo'q
(2 rows)"""
    ),
    (
        621,
        "NULLIF o'rnida CASE ekvivalenti",
        "NULLIF(a, b) ning CASE orqali ichki mexanizmi.",
        """SELECT 
    NULLIF(status_kod, 99) AS nullifed,
    CASE WHEN status_kod = 99 THEN NULL ELSE status_kod END AS case_ekvivalenti
FROM buyurtmalar_case;""",
        "`NULLIF(a, b)` sintaktik shakar (syntactic sugar) bo'lib, `CASE WHEN a = b THEN NULL ELSE a END` ifodasini bajaradi.",
        """ nullifed | case_ekvivalenti 
----------+------------------
        3 |                3
     NULL |             NULL
        1 |                1
        2 |                2
(4 rows)"""
    ),
    (
        622,
        "Bo'sh joylarni (Bo'sh satrlarni) NULL ga o'tkazish: NULLIF(TRIM(x), '')",
        "Faqat bo'shliq kiritilgan iflos satrlarni toza NULL ga aylantirish.",
        """SELECT NULLIF(TRIM('   '), '') AS toza_null;""",
        "Ushbu kombinatsiya ma'lumotlar omborida bo'sh qatorlar bilan NULL larning aralashib ketishini to'xtatadi.",
        """ toza_null 
-----------
 NULL
(1 row)"""
    ),
    (
        623,
        "CASE yordamida foizli ustama (Markup) hisoblash",
        "Mijoz shartnoma toifasiga qarab yakuniy to'lov miqdorini aniqlash.",
        """SELECT 
    mijoz,
    summa,
    summa * (1 + CASE 
        WHEN status_kod = 1 THEN 0.02 -- 2% xizmat haqi
        WHEN status_kod = 2 THEN 0.05 -- 5% yetkazish
        ELSE 0.00
    END) AS jami_tolov
FROM buyurtmalar_case;""",
        "CASE matematik ko'paytuvchi sifatida to'g'ridan-to'g'ri formulalarga kiritiladi.",
        """  mijoz  |   summa   | jami_tolov  
---------+-----------+-------------
 Akmal   | 500000.00 | 500000.0000
 Zilola  | 100000.00 | 100000.0000
 Sherzod | 157500.00 | 160650.0000
 Dildora | 275000.00 | 302500.0000
(4 rows)"""
    ),
    (
        624,
        "Ikki sananing eng kattasini olish: GREATEST(sana1, sana2)",
        "Shartnoma tuzilgan sana va to'lov sanasidan eng so'nggisini aniqlang.",
        """SELECT GREATEST('2026-05-01'::DATE, '2026-06-15'::DATE) AS oxirgi_harakat;""",
        "GREATEST nafaqat sonlar, balki barcha taqqoslanuvchi turlar (sanalar, matnlar) ustida ham ishlaydi.",
        """ oxirgi_harakat 
----------------
 2026-06-15
(1 row)"""
    ),
    (
        625,
        "O'rtacha qiymat hisoblashda NULL va Nol (0) farqi",
        "NULL larni 0 ga aylantirish o'rtacha arifmetikani (AVG) qanday o'zgartirib yuborishini ko'ring.",
        """CREATE TABLE avg_null_farq (baho INT);
INSERT INTO avg_null_farq VALUES (5), (NULL), (5);

SELECT 
    AVG(baho) AS tabiiy_ortacha,
    AVG(COALESCE(baho, 0)) AS nollashtirilgan_ortacha
FROM avg_null_farq;""",
        "Tabiiy AVG NULL ni e'tiborsiz qoldirib (5+5)/2 = 5.00 beradi. Agar COALESCE qilib 0 qo'yilsa, (5+0+5)/3 = 3.33 chiqadi! Shuning uchun AVG ichida COALESCE qo'llashda o'ta ehtiyot bo'lish lozim.",
        """   tabiiy_ortacha   | nollashtirilgan_ortacha 
--------------------+-------------------------
 5.0000000000000000 |      3.3333333333333333
(1 row)"""
    ),
    (
        626,
        "Ko'p ustunli tekshiruvda birorta ham NULL yo'qligini tekshirish",
        "Profilning 100% to'ldirilganligini aniqlash.",
        """SELECT 
    ism,
    (mobil_tel IS NOT NULL AND uy_tel IS NOT NULL AND email IS NOT NULL) AS toliq_toldirilganmi
FROM kontaktlar_case;""",
        "Barcha maydonlar NOT NULL bo'lsagina TRUE chiqadi.",
        """  ism  | toliq_toldirilganmi 
-------+---------------------
 Ali   | t
 Vali  | f
 Gani  | f
 Botir | f
(4 rows)"""
    ),
    (
        627,
        "Oracle dagi NVL va NVL2 ekvivalentlari",
        "Oracle dan PostgreSQL ga o'tuvchilar uchun NVL va NVL2 vazifasini bajaruvchi standart SQL.",
        """SELECT 
    COALESCE(mobil_tel, 'Bo''sh') AS nvl_ekvivalenti,
    CASE WHEN mobil_tel IS NOT NULL THEN 'Mavjud' ELSE 'Mavjud emas' END AS nvl2_ekvivalenti
FROM kontaktlar_case
LIMIT 2;""",
        "PostgreSQL da 'NVL' o'rniga 'COALESCE', 'NVL2' o'rniga esa 'CASE WHEN x IS NOT NULL THEN a ELSE b END' ishlatiladi.",
        """ nvl_ekvivalenti | nvl2_ekvivalenti 
-----------------+------------------
 +998901112233   | Mavjud
 Bo'sh           | Mavjud emas
(2 rows)"""
    ),
    (
        628,
        "Shartli saralash: Muayyan ID larni eng tepaga chiqarish",
        "ID raqami 3 bo'lgan mahsulot har doim eng tepada chiqsin, qolganlari narx bo'yicha saralansin.",
        """SELECT id, mijoz, summa 
FROM buyurtmalar_case 
ORDER BY (id = 3) DESC, summa DESC;""",
        "Mantiqiy ifoda `id = 3` TRUE (1) yoki FALSE (0) beradi. 'DESC' bo'yicha tartiblanganda TRUE (ID=3) birinchi chiqadi.",
        """ id |  mijoz  |   summa   
----+---------+-----------
  3 | Akmal   | 500000.00
  2 | Dildora | 275000.00
  1 | Sherzod | 157500.00
  4 | Zilola  | 100000.00
(4 rows)"""
    ),
    (
        629,
        "CASE da barcha natijalar bir xil ma'lumot turida bo'lishi sharti",
        "THEN bandida son, ELSE bandida matn yozilsa nima bo'ladi?",
        """-- Xato: CASE WHEN x THEN 100 ELSE 'Tugadi' END;
SELECT 'CASE ning barcha THEN va ELSE qiymatlari bitta ma''lumot turiga mos kelishi shart' AS qoida;""",
        "RDBMS har bir ustunning yagona qat'iy ma'lumot turiga ega bo'lishini talab qiladi. Agar bir joyda son, bir joyda satr berilsa, 'incompatible types' xatosi chiqadi.",
        """                                                 qoida                                                 
-------------------------------------------------------------------------------------------------------
 CASE ning barcha THEN va ELSE qiymatlari bitta ma'lumot turiga mos kelishi shart
(1 row)"""
    ),
    (
        630,
        "NULL qiymat ustida IS DISTINCT FROM",
        "Ikki ustun qiymati teng emasligini (biri NULL, biri matn bo'lsa ham) xavfsiz solishtirish.",
        """SELECT 
    ism,
    (mobil_tel IS DISTINCT FROM uy_tel) AS farq_bormi 
FROM kontaktlar_case;""",
        "'IS DISTINCT FROM' NULL qiymatlarni hisobga olib xavfsiz taqqoslaydi.",
        """  ism  | farq_bormi 
-------+------------
 Ali   | t
 Vali  | t
 Gani  | f
 Botir | f
(4 rows)"""
    ),
    (
        631,
        "CASE yordamida shartli bo'linish (Ratio calculation)",
        "Yetkazilgan buyurtmalar summasining umumiy summaga nisbatini hisoblash.",
        """SELECT 
    ROUND(
        SUM(CASE WHEN status_kod = 3 THEN summa ELSE 0 END) / 
        NULLIF(SUM(summa), 0) * 100, 
        2
    ) AS muvaffaqiyat_foizi
FROM buyurtmalar_case;""",
        "Konversiya foizlarini (Success Rate) hisoblashda eng ko'p ishlatiladigan formula.",
        """ muvaffaqiyat_foizi 
---------------------
               48.43
(1 row)"""
    ),
    (
        632,
        "Avtomatik test: Kutilgan qiymat bilan solishtirish (Assert CASE)",
        "Hisoblangan balans kutilgan natijaga tengligini tekshirish.",
        """SELECT 
    CASE WHEN SUM(summa) > 0 THEN 'PASS' ELSE 'FAIL' END AS test_natijasi
FROM buyurtmalar_case;""",
        "Baza darajasidagi regression testlarni yozishda CASE tekshiruvlari.",
        """ test_natijasi 
---------------
 PASS
(1 row)"""
    ),
    (
        633,
        "Telefon raqami yo'q foydalanuvchilar foizini hisoblash",
        "NULL qiymatlar butun jadvalning necha foizini tashkil qilishini toping.",
        """SELECT 
    ROUND(
        COUNT(CASE WHEN mobil_tel IS NULL THEN 1 END)::NUMERIC / 
        COUNT(*) * 100, 
        2
    ) AS telefonsizlar_foizi
FROM kontaktlar_case;""",
        "Ma'lumotlar to'liqligi (Data Completeness) sifat ko'rsatkichini aniqlash.",
        """ telefonsizlar_foizi 
---------------------
               75.00
(1 row)"""
    ),
    (
        634,
        "Shartli saralash: Yo'nalishni dinamik o'zgartirish (ASC/DESC)",
        "Parametrga qarab natijani o'sish yoki kamayish tartibida saralash.",
        """SELECT ism, summa 
FROM buyurtmalar_case 
ORDER BY 
    CASE WHEN 'OSISH' = 'OSISH' THEN summa END ASC,
    CASE WHEN 'OSISH' = 'KAMAYISH' THEN summa END DESC;""",
        "Dinamik ORDER BY yo'nalishini CASE orqali boshqarish usuli.",
        """  ism  |   summa   
-------+-----------
 Zilola| 100000.00
Sherzod| 157500.00
Dildora| 275000.00
 Akmal | 500000.00
(4 rows)"""
    ),
    (
        635,
        "Birinchi mavjud qiymatning ustun nomini aniqlash",
        "Mijoz bilan qaysi kanal orqali bog'lanish mumkinligini (Telefon, Uy, Email) aniqlang.",
        """SELECT 
    ism,
    CASE 
        WHEN mobil_tel IS NOT NULL THEN 'Mobil Telefon'
        WHEN uy_tel IS NOT NULL THEN 'Uy Telefoni'
        WHEN email IS NOT NULL THEN 'Elektron Pochta'
        ELSE 'Hech narsa yo''q'
    END AS eng_afzal_aloqa_turi
FROM kontaktlar_case;""",
        "Ustunlarning prioriteti bo'yicha kanal nomini qaytaradi.",
        """  ism  | eng_afzal_aloqa_turi 
-------+----------------------
 Ali   | Mobil Telefon
 Vali  | Uy Telefoni
 Gani  | Elektron Pochta
 Botir | Hech narsa yo'q
(4 rows)"""
    ),
    (
        636,
        "GREATEST da barcha parametrlar NULL bo'lsa",
        "Agar barcha parametrlar NULL bo'lsa nima natija chiqishini tekshiring.",
        """SELECT GREATEST(NULL::INT, NULL::INT) AS barcha_null_greatest;""",
        "Agar ro'yxatdagi barcha qiymatlar NULL bo'lsa, GREATEST ham NULL qaytaradi.",
        """ barcha_null_greatest 
----------------------
                 NULL
(1 row)"""
    ),
    (
        637,
        "LEAST va cheklangan maksimal qiymat (Cap limit)",
        "Mijoz hisobiga yoziladigan keshbek miqdori maksimum 50,000 so'mdan oshib ketmasligini ta'minlang.",
        """SELECT 
    summa,
    LEAST(summa * 0.05, 50000.00) AS cheklangan_keshbek
FROM buyurtmalar_case;""",
        "'LEAST(hisoblangan_qiymat, maksimal_chegara)' biznesda bonuslar yoki komissiyalarning yuqori chegarasini (Ceiling/Cap) cheklashda juda qulay.",
        """   summa   | cheklangan_keshbek 
-----------+--------------------
 500000.00 |           25000.00
 100000.00 |            5000.00
 157500.00 |            7875.00
 275000.00 |           13750.00
(4 rows)"""
    ),
    (
        638,
        "GREATEST va minimal to'lov chegarasi (Floor limit)",
        "Bank tranzaksiyasi komissiyasi kamida 5,000 so'm bo'lishini ta'minlang.",
        """SELECT 
    summa,
    GREATEST(summa * 0.01, 5000.00) AS komissiya
FROM buyurtmalar_case;""",
        "'GREATEST(hisob, minimal_chegara)' to'lovning quyi chegarasini (Floor) kafolatlaydi.",
        """   summa   | komissiya 
-----------+-----------
 500000.00 |   5000.00
 100000.00 |   5000.00
 157500.00 |   5000.00
 275000.00 |   5000.00
(4 rows)"""
    ),
    (
        639,
        "COALESCE ichida Subquery chaqirish",
        "Agar mijozning shaxsiy chegirmasi bo'lmasa, umumiy tizim chegirmasini subquery dan oling.",
        """SELECT 
    mijoz,
    COALESCE(
        NULL, -- Shaxsiy chegirma NULL deb hisoblaymiz
        (SELECT 5.0) -- Tizim umumiy chegirmasi
    ) AS qollanilgan_chegirma;""",
        "COALESCE o'ng tomonidagi ifodalarni faqat chap tomoni NULL bo'lgandagina hisoblaydi (Lazy evaluation).",
        """ qollanilgan_chegirma 
----------------------
                  5.0
(1 row)"""
    ),
    (
        640,
        "CASE yordamida statuslarni guruhlash",
        "Ko'plab mayda holatlarni 2 ta asosiy toifaga ('Faol' va 'Nofaol') birlashtiring.",
        """SELECT 
    mijoz,
    CASE status_kod 
        WHEN 1 THEN 'Faol jarayonda'
        WHEN 2 THEN 'Faol jarayonda'
        ELSE 'Yakunlangan yoki bekor'
    END AS makro_holat
FROM buyurtmalar_case;""",
        "Biznesda operatsion statuslarni boshqaruv statuslariga birlashtirish.",
        """  mijoz  |       makro_holat       
---------+-------------------------
 Akmal   | Yakunlangan yoki bekor
 Zilola  | Yakunlangan yoki bekor
 Sherzod | Faol jarayonda
 Dildora | Faol jarayonda
(4 rows)"""
    ),
    (
        641,
        "3VL: UNKNOWN mantiqiy ifodasi va WHERE filtri",
        "Agar WHERE sharti UNKNOWN bersa, nima uchun qator o'tkazib yuborilishini ko'rsating.",
        """SELECT 'WHERE filtri faqat qat''iy TRUE bo‘lgan qatorlarni o‘tkazadi, FALSE va UNKNOWN ni esa tashlab yuboradi' AS tushuntirish;""",
        "SQL ning asosiy qoidasi: qator faqatgina WHERE shartining natijasi aniq TRUE bo'lsagina tanlanadi. UNKNOWN qiymatlar rad etiladi.",
        """                                                 tushuntirish                                                  
---------------------------------------------------------------------------------------------------------------
 WHERE filtri faqat qat'iy TRUE bo‘lgan qatorlarni o‘tkazadi, FALSE va UNKNOWN ni esa tashlab yuboradi
(1 row)"""
    ),
    (
        642,
        "NULL bo'lmagan birinchi 2 ta qiymatni topish",
        "COALESCE faqat bittasini beradi, ikkitasini massiv orqali ajratish.",
        """SELECT (ARRAY_REMOVE(ARRAY[mobil_tel, uy_tel, email], NULL))[1:2] AS birinchi_ikkita_kontakt 
FROM kontaktlar_case 
WHERE id = 1;""",
        "ARRAY_REMOVE orqali NULL lar tozalangach, massivdan birinchi ikkita mavjud aloqa vositasi olinadi.",
        """      birinchi_ikkita_kontakt      
-----------------------------------
 {+998901112233,+998712001122}
(1 row)"""
    ),
    (
        643,
        "Qatorning to'liq bo'shligini tekshirish (All NULLs check)",
        "Barcha kontakt ustunlari NULL bo'lgan tashlandiq profillarni toping.",
        """SELECT ism 
FROM kontaktlar_case 
WHERE COALESCE(mobil_tel, uy_tel, email) IS NULL;""",
        "COALESCE barcha ustunlar NULL bo'lgandagina NULL qaytaradi. Bu barcha ustunlarning bo'shligini bitta qisqa ifodada tekshirish usulidir.",
        """  ism  
-------
 Botir
(1 row)"""
    ),
    (
        644,
        "CASE orqali har xil shartlar bo'yicha soliq stavkasi",
        "Yillik daromad miqdoriga qarab progressiv daromad solig'i hisoblash.",
        """SELECT 
    mijoz, summa,
    CASE 
        WHEN summa > 300000 THEN summa * 0.15
        WHEN summa > 150000 THEN summa * 0.12
        ELSE summa * 0.08
    END AS soliq_summasi
FROM buyurtmalar_case;""",
        "Progressiv soliq tizimlari CASE ifodalariga tayanadi.",
        """  mijoz  |   summa   | soliq_summasi 
---------+-----------+---------------
 Akmal   | 500000.00 |    75000.0000
 Zilola  | 100000.00 |     8000.0000
 Sherzod | 157500.00 |    18900.0000
 Dildora | 275000.00 |    33000.0000
(4 rows)"""
    ),
    (
        645,
        "COALESCE bilan formatlangan xabar yasash",
        "Mijozga jo'natiladigan xabarda uning ismi bo'lmasa 'Hurmatli mijoz' deb murojaat qilish.",
        """SELECT 'Salom, ' || COALESCE(ism, 'hurmatli mijoz') || '!' AS xabar 
FROM kontaktlar_case;""",
        "Shaxsiy xabarnomalar (Notification generator) da NULL larni muqobil murojaat bilan almashtirish.",
        """            xabar            
-----------------------------
 Salom, Ali!
 Salom, Vali!
 Salom, Gani!
 Salom, Botir!
(4 rows)"""
    ),
    (
        646,
        "CASE yordamida ikkita ustun qiymatini solishtirib ustun tanlash",
        "Rejadagi va amaldagi xarajatlardan kattasini tanlash.",
        """SELECT 
    CASE WHEN 150 > 100 THEN 'Haqiqiy xarajat katta' ELSE 'Reja katta' END AS natija;""",
        "Kattalik mezoni bo'yicha toifalar aniqlanadi.",
        """        natija         
-----------------------
 Haqiqiy xarajat katta
(1 row)"""
    ),
    (
        647,
        "NULLIF yordamida cheksiz o'sish anomaliyasini to'xtatish",
        "O'tgan oy 0 bo'lsa o'sishni hisoblamasdan 'Yangi tushum' deb belgilash.",
        """SELECT 
    CASE 
        WHEN NULLIF(0, 0) IS NULL THEN 'Oldingi ko‘rsatkich mavjud emas' 
        ELSE 'O‘sish hisoblandi' 
    END AS tahlil;""",
        "Nolga bo'lishdan himoyalanishda CASE va NULLIF tandemda ishlaydi.",
        """             tahlil              
---------------------------------
 Oldingi ko‘rsatkich mavjud emas
(1 row)"""
    ),
    (
        648,
        "Shartli COUNT va FILTER (WHERE ...) taqqoslash",
        "Nega PostgreSQL da FILTER bandi CASE ga qaraganda 10-15% tezroq ishlashini ko'rsating.",
        """SELECT 
    COUNT(*) FILTER (WHERE status_kod = 1) AS filter_usuli,
    COUNT(CASE WHEN status_kod = 1 THEN 1 END) AS case_usuli
FROM buyurtmalar_case;""",
        "PostgreSQL ichki C-kodida 'FILTER' oynador/agregat ifodasi qatorni bevosita o'tkazib yuboradi, 'CASE' esa virtual qiymat hisoblab keyin COUNT ga uzatadi.",
        """ filter_usuli | case_usuli 
--------------+------------
            1 |          1
(1 row)"""
    ),
    (
        649,
        "CASE natijasida bir xil ma'lumot turini kafolatlash (Explicit Cast)",
        "Turli shartlarda turli uzunlikdagi sonlar qaytganda ularni aniq NUMERIC(10,2) ga o'tkazish.",
        """SELECT 
    mijoz,
    (CASE 
        WHEN status_kod = 1 THEN 100
        WHEN status_kod = 2 THEN 200.50
        ELSE 0
    END)::NUMERIC(10, 2) AS bir_xil_tip
FROM buyurtmalar_case;""",
        "Eksplitsit kasting (::NUMERIC) orqali kutilmagan yaxlitlashlar oldi olinadi.",
        """  mijoz  | bir_xil_tip 
---------+-------------
 Akmal   |        0.00
 Zilola  |        0.00
 Sherzod |      100.00
 Dildora |      200.50
(4 rows)"""
    ),
    (
        650,
        "Korporativ Shartli Mantiq: Mijozlarning Kredit Skoringi va Risklarni Baholash",
        "Bank mijozining oylik daromadi, kechiktirilgan kunlari, kredit yuki va ish stajiga tayanib unga kredit berish qarorini (Skoring: Tasdiqlandi, Qo'shimcha tekshiruv, Rad etildi) to'liq avtomatik qabul qiluvchi CASE mexanizmini yarating.",
        """CREATE TABLE kredit_arizalari (
    ariza_id BIGSERIAL PRIMARY KEY,
    mijoz_fio VARCHAR(100),
    oylik_daromad NUMERIC(15, 2),
    soralgan_summa NUMERIC(15, 2),
    kechiktirilgan_kunlar INT,
    ish_staji_oy INT
);

INSERT INTO kredit_arizalari (mijoz_fio, oylik_daromad, soralgan_summa, kechiktirilgan_kunlar, ish_staji_oy) VALUES 
('Javohir Toshmatov', 15000000, 50000000, 0, 24),  -- Ideal mijoz
('Sarvinoz Rahimova', 8000000, 40000000, 5, 12),    -- Kichik kechikish, o'rtacha yuk
('Umid Normatov',     4000000, 60000000, 45, 3);    -- Katta xavf, past daromad

SELECT 
    ariza_id,
    mijoz_fio,
    oylik_daromad,
    soralgan_summa,
    ROUND(soralgan_summa / NULLIF(oylik_daromad, 0), 1) AS qarz_daromad_nisbati,
    CASE 
        WHEN kechiktirilgan_kunlar > 30 OR ish_staji_oy < 6 THEN '❌ RAD ETILDI (Yuqori risk)'
        WHEN (soralgan_summa / NULLIF(oylik_daromad, 0)) <= 4.0 AND kechiktirilgan_kunlar = 0 THEN '✅ AVTOMATIK TASDIQLANDI'
        WHEN (soralgan_summa / NULLIF(oylik_daromad, 0)) <= 6.0 AND kechiktirilgan_kunlar <= 10 THEN '⚠️ QO‘SHIMCHA TAHLIL TALAB ETILADI'
        ELSE '❌ RAD ETILDI (Daromad yetarsiz)'
    END AS skoring_qarori,
    CASE 
        WHEN kechiktirilgan_kunlar = 0 AND ish_staji_oy >= 12 THEN 0.22 -- 22% yillik
        ELSE 0.28 -- 28% yillik
    END * 100 || '%' AS tavsiya_etilgan_foiz
FROM kredit_arizalari;""",
        "Ushbu korporativ so'rov bank va mikromoliya tashkilotlarining Avtomatlashtirilgan Kredit Skoringi (Underwriting & Credit Scoring Engine) asosini aks ettiradi: NULLIF yordamida qarz-daromad nisbati (DTI ratio) xavfsiz hisoblanadi, ko'p parametrli CASE mantiqi bir zumda xavf darajasini baholaydi va individual foiz stavkasini tayinlaydi.",
        """ ariza_id |     mijoz_fio     | oylik_daromad | soralgan_summa | qarz_daromad_nisbati |           skoring_qarori           | tavsiya_etilgan_foiz 
----------+-------------------+---------------+----------------+----------------------+------------------------------------+----------------------
        1 | Javohir Toshmatov |   15000000.00 |    50000000.00 |                  3.3 | ✅ AVTOMATIK TASDIQLANDI           | 22.0%
        2 | Sarvinoz Rahimova |    8000000.00 |    40000000.00 |                  5.0 | ⚠️ QO‘SHIMCHA TAHLIL TALAB ETILADI | 28.0%
        3 | Umid Normatov     |    4000000.00 |    60000000.00 |                 15.0 | ❌ RAD ETILDI (Yuqori risk)        | 28.0%
(3 rows)"""
    )
]

formatted = [format_task(*item) for item in case_data]
save_file("sql_13_shartli_mantiq_case_va_null_boshqaruvi.md", formatted)
