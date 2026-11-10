import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

# List of 50 tasks for File 10: 451 - 500
# Oynador funksiyalar 2 (LEAD, LAG, FIRST_VALUE, LAST_VALUE, NTH_VALUE, Window Frames: ROWS/RANGE BETWEEN, Running Totals, Moving Averages, MoM, YoY, Islands & Gaps)

wf2_data = [
    (
        451,
        "Oldingi qator qiymatini olish: LAG() asoslari",
        "Har bir oyning savdo hajmi yoniga o'tgan oydagi savdo hajmini chiqaring.",
        """CREATE TABLE oylik_savdo_wf (
    oy DATE PRIMARY KEY,
    summa NUMERIC(15, 2)
);

INSERT INTO oylik_savdo_wf VALUES 
('2026-01-01', 100000000),
('2026-02-01', 120000000),
('2026-03-01', 115000000),
('2026-04-01', 140000000);

SELECT 
    oy, 
    summa,
    LAG(summa) OVER (ORDER BY oy ASC) AS otgan_oy_summasi 
FROM oylik_savdo_wf;""",
        "'LAG(ustun)' funksiyasi joriy qatordan 1 qadam oldingi qator qiymatini oladi. Eng birinchi oy uchun oldingi oy yo'qligi sababli natija NULL bo'ladi.",
        """     oy     |    summa     | otgan_oy_summasi 
------------+--------------+------------------
 2026-01-01 | 100000000.00 |             NULL
 2026-02-01 | 120000000.00 |     100000000.00
 2026-03-01 | 115000000.00 |     120000000.00
 2026-04-01 | 140000000.00 |     115000000.00
(4 rows)"""
    ),
    (
        452,
        "LAG() da qadamlar soni va sukut bo'yicha qiymat (Offset va Default)",
        "O'tgan oydan oldingi 2-oyni olish va agar qiymat bo'lmasa NULL o'rniga 0 chiqarish.",
        """SELECT 
    oy, 
    summa,
    LAG(summa, 2, 0) OVER (ORDER BY oy ASC) AS ikki_oy_oldingi_summa 
FROM oylik_savdo_wf;""",
        "'LAG(ustun, offset, default_qiymat)' sintaksisi: 'offset=2' ikkita qator orqaga sakraydi, 'default=0' esa mavjud bo'lmagan qatorlar o'rniga 0 qo'yadi.",
        """     oy     |    summa     | ikki_oy_oldingi_summa 
------------+--------------+-----------------------
 2026-01-01 | 100000000.00 |                  0.00
 2026-02-01 | 120000000.00 |                  0.00
 2026-03-01 | 115000000.00 |          100000000.00
 2026-04-01 | 140000000.00 |          120000000.00
(4 rows)"""
    ),
    (
        453,
        "Oylik o'sish sur'atini hisoblash (Month-over-Month - MoM)",
        "Har bir oyda savdo o'tgan oyga nisbatan necha foizga o'sganini yoki kamayganini hisoblang.",
        """SELECT 
    oy, 
    summa,
    LAG(summa) OVER (ORDER BY oy ASC) AS oldingi_oy,
    ROUND(((summa - LAG(summa) OVER (ORDER BY oy ASC)) / LAG(summa) OVER (ORDER BY oy ASC) * 100), 2) AS o_sish_foiz
FROM oylik_savdo_wf;""",
        "MoM formulasi: `(Joriy - Oldingi) / Oldingi * 100`. LAG funksiyasi tufayli hech qanday Self Joinlarsiz bitta qatorda o'sish foizi hisoblanadi.",
        """     oy     |    summa     |  oldingi_oy  | o_sish_foiz 
------------+--------------+--------------+-------------
 2026-01-01 | 100000000.00 |         NULL |        NULL
 2026-02-01 | 120000000.00 | 100000000.00 |       20.00
 2026-03-01 | 115000000.00 | 120000000.00 |       -4.17
 2026-04-01 | 140000000.00 | 115000000.00 |       21.74
(4 rows)"""
    ),
    (
        454,
        "Keyingi qator qiymatini olish: LEAD() asoslari",
        "Har bir oy yonida keyingi oyda qancha savdo kutilayotganini (keyingi qator qiymatini) chiqaring.",
        """SELECT 
    oy, 
    summa,
    LEAD(summa) OVER (ORDER BY oy ASC) AS keyingi_oy_summasi 
FROM oylik_savdo_wf;""",
        "'LEAD(ustun)' joriy qatordan 1 qadam oldinga (keyingi qatorga) qaraydi. Eng oxirgi oy uchun keyingi oy bo'lmagani sababli NULL chiqadi.",
        """     oy     |    summa     | keyingi_oy_summasi 
------------+--------------+--------------------
 2026-01-01 | 100000000.00 |       120000000.00
 2026-02-01 | 120000000.00 |       115000000.00
 2026-03-01 | 115000000.00 |       140000000.00
 2026-04-01 | 140000000.00 |               NULL
(4 rows)"""
    ),
    (
        455,
        "LEAD yordamida oraliq vaqtni (Davomiylikni) hisoblash",
        "Foydalanuvchining har bir sahifada necha daqiqa qolganini (keyingi sahifani ochgan vaqtidan ayirib) aniqlang.",
        """CREATE TABLE foydalanuvchi_sessiya (
    id SERIAL PRIMARY KEY,
    sahifa VARCHAR(50),
    ochilgan_vaqt TIMESTAMP
);

INSERT INTO foydalanuvchi_sessiya (sahifa, ochilgan_vaqt) VALUES 
('Bosh sahifa', '2026-05-01 10:00:00'),
('Katalog', '2026-05-01 10:03:30'),
('Mahsulot tafsiloti', '2026-05-01 10:07:00'),
('Savatcha', '2026-05-01 10:15:00');

SELECT 
    sahifa, 
    ochilgan_vaqt,
    LEAD(ochilgan_vaqt) OVER (ORDER BY ochilgan_vaqt ASC) AS keyingi_sahifa_vaqti,
    LEAD(ochilgan_vaqt) OVER (ORDER BY ochilgan_vaqt ASC) - ochilgan_vaqt AS sarflangan_vaqt
FROM foydalanuvchi_sessiya;""",
        "Web-analitikada seanslar uzunligini hisoblash uchun 'LEAD(vaqt) - joriy_vaqt' eng qulay standart formuladir.",
        """       sahifa       |    ochilgan_vaqt    | keyingi_sahifa_vaqti| sarflangan_vaqt 
--------------------+---------------------+---------------------+-----------------
 Bosh sahifa        | 2026-05-01 10:00:00 | 2026-05-01 10:03:30 | 00:03:30
 Katalog            | 2026-05-01 10:03:30 | 2026-05-01 10:07:00 | 00:03:30
 Mahsulot tafsiloti | 2026-05-01 10:07:00 | 2026-05-01 10:15:00 | 00:08:00
 Savatcha           | 2026-05-01 10:15:00 | NULL                | NULL
(4 rows)"""
    ),
    (
        456,
        "Eng birinchi qiymatni olish: FIRST_VALUE()",
        "Har bir xodim yonida uning bo'limidagi eng birinchi (eng yuqori) maosh oluvchi shaxsning ismini ko'rsating.",
        """SELECT 
    bolim,
    ism,
    maosh,
    FIRST_VALUE(ism) OVER (
        PARTITION BY bolim 
        ORDER BY maosh DESC
    ) AS bolimdagi_eng_katta_xodim
FROM xodimlar_wf;""",
        "'FIRST_VALUE(ustun)' saralangan oyna doirasidagi eng birinchi element qiymatini barcha qatorlarga qaytaradi.",
        """ bolim  |   ism   |    maosh    | bolimdagi_eng_katta_xodim 
--------+---------+-------------+---------------------------
 IT     | Nodira  | 18000000.00 | Nodira
 IT     | Sherzod | 15000000.00 | Nodira
 IT     | Azamat  | 12000000.00 | Nodira
 Moliya | Gulnoza | 10000000.00 | Gulnoza
 Moliya | Botir   | 10000000.00 | Gulnoza
 Moliya | Laylo   |  9000000.00 | Gulnoza
(6 rows)"""
    ),
    (
        457,
        "Eng oxirgi qiymat: LAST_VALUE() va Default Frame tuzog'i",
        "Nega oddiy LAST_VALUE() kutilganidek eng oxirgi qatorni emas, joriy qatorning o'zini qaytarishini ko'ring.",
        """SELECT 
    bolim,
    ism,
    maosh,
    LAST_VALUE(ism) OVER (
        PARTITION BY bolim 
        ORDER BY maosh DESC
    ) AS xato_oxirgi_xodim
FROM xodimlar_wf;""",
        "SQL standartida ORDER BY berilganda sukut bo'yicha freym chegarasi `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` bo'ladi. Ya'ni oyna joriy qatorda TUGAYDI! Shu sababli joriy qatorning o'zi oynaning oxirgi qiymati bo'lib qoladi.",
        """ bolim  |   ism   |    maosh    | xato_oxirgi_xodim 
--------+---------+-------------+-------------------
 IT     | Nodira  | 18000000.00 | Nodira
 IT     | Sherzod | 15000000.00 | Sherzod
 IT     | Azamat  | 12000000.00 | Azamat
 Moliya | Gulnoza | 10000000.00 | Botir
 Moliya | Botir   | 10000000.00 | Botir
 Moliya | Laylo   |  9000000.00 | Laylo
(6 rows)"""
    ),
    (
        458,
        "To'g'ri LAST_VALUE() (Freymni oxirigacha kengaytirish)",
        "Oyna chegarasini oxirigacha surib (UNBOUNDED FOLLOWING) haqiqiy oxirgi xodimni toping.",
        """SELECT 
    bolim,
    ism,
    maosh,
    LAST_VALUE(ism) OVER (
        PARTITION BY bolim 
        ORDER BY maosh DESC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS haqiqiy_oxirgi_xodim
FROM xodimlar_wf;""",
        "'ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING' butun bo'lim qatorlarini to'liq qamrab oladi. Endi LAST_VALUE haqiqatan eng quyi xodimni (IT uchun Azamat, Moliya uchun Laylo) barcha qatorlarda to'g'ri ko'rsatadi.",
        """ bolim  |   ism   |    maosh    | haqiqiy_oxirgi_xodim 
--------+---------+-------------+----------------------
 IT     | Nodira  | 18000000.00 | Azamat
 IT     | Sherzod | 15000000.00 | Azamat
 IT     | Azamat  | 12000000.00 | Azamat
 Moliya | Gulnoza | 10000000.00 | Laylo
 Moliya | Botir   | 10000000.00 | Laylo
 Moliya | Laylo   |  9000000.00 | Laylo
(6 rows)"""
    ),
    (
        459,
        "N-chi qiymatni olish: NTH_VALUE()",
        "Har bir bo'limdagi ikkinchi eng yuqori maosh oluvchining ismini NTH_VALUE bilan chiqaring.",
        """SELECT 
    bolim,
    ism,
    maosh,
    NTH_VALUE(ism, 2) OVER (
        PARTITION BY bolim 
        ORDER BY maosh DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS ikkinchi_xodim
FROM xodimlar_wf;""",
        "'NTH_VALUE(ustun, n)' oyna ichidagi n-chi qatordagi qiymatni qaytaradi. Bu yerda har bir bo'limning aynan 2-xodimi (Sherzod va Botir) tanlanadi.",
        """ bolim  |   ism   |    maosh    | ikkinchi_xodim 
--------+---------+-------------+----------------
 IT     | Nodira  | 18000000.00 | Sherzod
 IT     | Sherzod | 15000000.00 | Sherzod
 IT     | Azamat  | 12000000.00 | Sherzod
 Moliya | Gulnoza | 10000000.00 | Botir
 Moliya | Botir   | 10000000.00 | Botir
 Moliya | Laylo   |  9000000.00 | Botir
(6 rows)"""
    ),
    (
        460,
        "O'suvchi jami (Running Total / Cumulative Sum)",
        "Oylar bo'yicha yil boshidan to shu oygacha bo'lgan to'plangan umumiy savdo hajmini hisoblang.",
        """SELECT 
    oy, 
    summa,
    SUM(summa) OVER (
        ORDER BY oy ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS kumulyativ_jami
FROM oylik_savdo_wf;""",
        "Kümülyativ jamlashda har bir yangi qator oldingi barcha oylarning summasini o'ziga qo'shib boradi (100M, 220M, 335M, 475M). Buxgalteriya va moliyaviy oqimlar hisobida eng asosiy ko'rsatkich.",
        """     oy     |    summa     | kumulyativ_jami 
------------+--------------+-----------------
 2026-01-01 | 100000000.00 |    100000000.00
 2026-02-01 | 120000000.00 |    220000000.00
 2026-03-01 | 115000000.00 |    335000000.00
 2026-04-01 | 140000000.00 |    475000000.00
(4 rows)"""
    ),
    (
        461,
        "ROWS va RANGE o'rtasidagi farq",
        "Bir xil qiymatlar bo'lganda ROWS (aniq fizik qator) va RANGE (mantiqiy qiymat diapazoni) qanday natija berishini ko'rsating.",
        """CREATE TABLE test_range (id INT, sana INT, summa NUMERIC);
INSERT INTO test_range VALUES (1, 1, 100), (2, 2, 200), (3, 2, 300);

SELECT 
    sana, summa,
    SUM(summa) OVER (ORDER BY sana ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS rows_summa,
    SUM(summa) OVER (ORDER BY sana RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS range_summa
FROM test_range;""",
        "Agar ayni bir sana (2) bo'yicha bir nechta yozuv bo'lsa: 'ROWS' ularni bittalab qo'shadi (100 -> 300 -> 600). 'RANGE' esa bir xil qiymatlarni teng deb baholab, ikkala qatorga ham to'liq guruh jamini (600 va 600) beradi! Shu sababli ko'pincha 'ROWS' afzal ko'riladi.",
        """ sana | summa  | rows_summa | range_summa 
------+--------+------------+-------------
    1 | 100.00 |     100.00 |      100.00
    2 | 200.00 |     300.00 |      600.00
    2 | 300.00 |     600.00 |      600.00
(3 rows)"""
    ),
    (
        462,
        "Harakatlanuvchi o'rtacha (3 oylik Moving Average - MA3)",
        "Mavsumiy tebranishlarni silliqlash uchun joriy oy va undan oldingi 2 oyning (jami 3 oy) o'rtacha savdo ko'rsatkichini hisoblang.",
        """SELECT 
    oy, 
    summa,
    ROUND(AVG(summa) OVER (
        ORDER BY oy ASC 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS ma_3_oylik
FROM oylik_savdo_wf;""",
        "'ROWS BETWEEN 2 PRECEDING AND CURRENT ROW' har bir satr uchun joriy oy va oldingi 2 oyni (3 ta nuqta) qamrab oladi. Texnik tahlil (Trading) va savdo prognozlashda asosiy vosita hisoblanadi.",
        """     oy     |    summa     |  ma_3_oylik  
------------+--------------+--------------
 2026-01-01 | 100000000.00 | 100000000.00
 2026-02-01 | 120000000.00 | 110000000.00
 2026-03-01 | 115000000.00 | 11166666.67
 2026-04-01 | 140000000.00 | 125000000.00
(4 rows)"""
    ),
    (
        463,
        "Markazlashtirilgan o'rtacha (Centered Moving Average)",
        "Oldingi 1 ta qator, joriy qator va keyingi 1 ta qatorning (1 preceding and 1 following) o'rtachasini hisoblang.",
        """SELECT 
    oy, 
    summa,
    ROUND(AVG(summa) OVER (
        ORDER BY oy ASC 
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
    ), 2) AS markaziy_ortacha
FROM oylik_savdo_wf;""",
        "Freym chegaralari ham oldinga, ham orqaga teng kengaytiriladi.",
        """     oy     |    summa     | markaziy_ortacha 
------------+--------------+------------------
 2026-01-01 | 100000000.00 |     110000000.00
 2026-02-01 | 120000000.00 |     11166666.67
 2026-03-01 | 115000000.00 |     125000000.00
 2026-04-01 | 140000000.00 |     127500000.00
(4 rows)"""
    ),
    (
        464,
        "O'suvchi maksimum (Running Maximum)",
        "Yil boshidan to joriy oygacha erishilgan eng yuqori rekord savdo summasini ko'rsatib boring.",
        """SELECT 
    oy, 
    summa,
    MAX(summa) OVER (
        ORDER BY oy ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS erishilgan_rekord
FROM oylik_savdo_wf;""",
        "O'suvchi maksimum har bir oydagi yangi 'All-Time High' rekordlarni qayd etib boradi.",
        """     oy     |    summa     | erishilgan_rekord 
------------+--------------+-------------------
 2026-01-01 | 100000000.00 |      100000000.00
 2026-02-01 | 120000000.00 |      120000000.00
 2026-03-01 | 115000000.00 |      120000000.00
 2026-04-01 | 140000000.00 |      140000000.00
(4 rows)"""
    ),
    (
        465,
        "Kümülyativ qatorlar soni (Running Count)",
        "Har bir tranzaksiya o'sha paytgacha bo'lgan jami nechanchi tranzaksiya ekanligini hisoblang.",
        """SELECT 
    oy, 
    COUNT(*) OVER (
        ORDER BY oy ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS to‘plangan_tranzaksiyalar
FROM oylik_savdo_wf;""",
        "Har qadamda oyna kengayib boradi va 1, 2, 3, 4 ko'rinishida yozuvlar jamlanadi.",
        """     oy     | to‘plangan_tranzaksiyalar 
------------+---------------------------
 2026-01-01 |                         1
 2026-02-01 |                         2
 2026-03-01 |                         3
 2026-04-01 |                         4
(4 rows)"""
    ),
    (
        466,
        "Keyingi oylardagi qoldiq jami (Reverse Running Total)",
        "Joriy oydan boshlab to yil oxirigacha qolgan oylardagi jami kutilayotgan summani hisoblang.",
        """SELECT 
    oy, 
    summa,
    SUM(summa) OVER (
        ORDER BY oy ASC 
        ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
    ) AS kelajakdagi_qoldiq_summa
FROM oylik_savdo_wf;""",
        "'ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING' joriy qatordan oxirgi qatorgacha bo'lgan masofani jamlaydi.",
        """     oy     |    summa     | kelajakdagi_qoldiq_summa 
------------+--------------+--------------------------
 2026-01-01 | 100000000.00 |             475000000.00
 2026-02-01 | 120000000.00 |             375000000.00
 2026-03-01 | 115000000.00 |             255000000.00
 2026-04-01 | 140000000.00 |             140000000.00
(4 rows)"""
    ),
    (
        467,
        "Orollar va Bo'shliqlar (Islands and Gaps): Ketma-ket kunlar orolini topish",
        "Foydalanuvchining ketma-ket (uzluksiz) tizimga kirgan kunlarini guruhlarga (orollarga) ajrating.",
        """CREATE TABLE kirish_kunlari (user_id INT, sana DATE);
INSERT INTO kirish_kunlari VALUES 
(1, '2026-06-01'), (1, '2026-06-02'), (1, '2026-06-03'), -- 1-orol
(1, '2026-06-06'), (1, '2026-06-07');                     -- 2-orol

WITH farq_guruhi AS (
    SELECT 
        user_id, 
        sana,
        sana - (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY sana))::INT AS orol_id
    FROM kirish_kunlari
)
SELECT 
    user_id,
    MIN(sana) AS orol_boshi,
    MAX(sana) AS orol_oxiri,
    COUNT(*) AS ketma_ket_kunlar_soni
FROM farq_guruhi
GROUP BY user_id, orol_id
ORDER BY orol_boshi;""",
        "Klassik 'sana - ROW_NUMBER()' naqshi: agar kunlar uzluksiz ketma-ket kelsa, sana va row_number bir xil tezlikda o'sadi va ularning ayirmasi doimiy o'zgarmas son (orol_id) bo'lib qoladi. Shu orqali ketma-ketliklar bir zumda guruhlanadi.",
        """ user_id | orol_boshi | orol_oxiri | ketma_ket_kunlar_soni 
---------+------------+------------+-----------------------
       1 | 2026-06-01 | 2026-06-03 |                     3
       1 | 2026-06-06 | 2026-06-07 |                     2
(2 rows)"""
    ),
    (
        468,
        "Bo'shliqlarni aniqlash (Gaps Detection)",
        "Ketma-ket raqamlangan hisob-fakturalar orasida tushib qolgan (yo'qolgan) raqamlar oraliqlarini LAG yordamida toping.",
        """CREATE TABLE faktura (f_raqam INT);
INSERT INTO faktura VALUES (1), (2), (3), (7), (8), (12);

SELECT 
    oldingi_raqam + 1 AS boshliq_boshi,
    f_raqam - 1 AS boshliq_oxiri 
FROM (
    SELECT 
        f_raqam, 
        LAG(f_raqam) OVER (ORDER BY f_raqam) AS oldingi_raqam
    FROM faktura
) t
WHERE f_raqam - oldingi_raqam > 1;""",
        "Agar joriy raqam va oldingi raqam farqi 1 dan katta bo'lsa, demak ular orasida uzilish (gap) mavjud.",
        """ boshliq_boshi | boshliq_oxiri 
---------------+---------------
             4 |             6
             9 |            11
(2 rows)"""
    ),
    (
        469,
        "Seanslashtirish (Sessionization): 30 daqiqalik tanaffus bo'yicha",
        "Foydalanuvchi faoliyatida agar 30 daqiqadan ko'p sukut saqlansa, yangi sessiya ID sini hisoblang.",
        """CREATE TABLE harakatlar (id INT, vaqt TIMESTAMP);
INSERT INTO harakatlar VALUES 
(1, '2026-07-01 10:00:00'),
(2, '2026-07-01 10:15:00'),
(3, '2026-07-01 11:00:00'), -- 45 daqiqa tanaffus! Yangi sessiya
(4, '2026-07-01 11:10:00');

WITH farq AS (
    SELECT 
        id, vaqt,
        CASE 
            WHEN vaqt - LAG(vaqt) OVER (ORDER BY vaqt) > INTERVAL '30 minutes' 
                 OR LAG(vaqt) OVER (ORDER BY vaqt) IS NULL 
            THEN 1 ELSE 0 
        END AS yangi_sessiyami
    FROM harakatlar
)
SELECT 
    id, 
    vaqt,
    SUM(yangi_sessiyami) OVER (ORDER BY vaqt) AS sessiya_raqami
FROM farq;""",
        "Tanaffus 30 daqiqadan oshganda flag=1 bo'ladi. 'SUM(flag) OVER (...)' esa kumulyativ hisoblab sessiya raqamini 1, 1, 2, 2 qilib avtomatik oshirib boradi.",
        """ id |        vaqt         | sessiya_raqami 
----+---------------------+----------------
  1 | 2026-07-01 10:00:00 |              1
  2 | 2026-07-01 10:15:00 |              1
  3 | 2026-07-01 11:00:00 |              2
  4 | 2026-07-01 11:10:00 |              2
(4 rows)"""
    ),
    (
        470,
        "Yillik o'sish sur'ati (Year-over-Year - YoY)",
        "Har bir oyning savdosini o'tgan yilning ayni shu oyi (LAG 12) bilan solishtiring.",
        """CREATE TABLE yillik_savdo (sana DATE, summa NUMERIC);
INSERT INTO yillik_savdo VALUES 
('2025-01-01', 80000000), ('2026-01-01', 100000000);

SELECT 
    sana, 
    summa,
    LAG(summa, 1) OVER (ORDER BY sana) AS otgan_yilgi_summa,
    ROUND(((summa - LAG(summa, 1) OVER (ORDER BY sana)) / LAG(summa, 1) OVER (ORDER BY sana) * 100), 2) AS yoy_osish_foiz
FROM yillik_savdo;""",
        "YoY tahlili mavsumiylik ta'sirini istisno qiluvchi eng ishonchli biznes metrikadir.",
        """    sana    |    summa     | otgan_yilgi_summa | yoy_osish_foiz 
------------+--------------+-------------------+----------------
 2025-01-01 |  80000000.00 |              NULL |           NULL
 2026-01-01 | 100000000.00 |       80000000.00 |          25.00
(2 rows)"""
    ),
    (
        471,
        "Oldingi qiymat bilan teng bo'lsa filtrlash",
        "Sensor harorat ko'rsatkichi faqat o'zgargandagina qayd etish (o'zgarmagan takrorlarni o'chirish).",
        """CREATE TABLE sensor (vaqt INT, harorat INT);
INSERT INTO sensor VALUES (1, 25), (2, 25), (3, 26), (4, 26), (5, 27);

SELECT vaqt, harorat 
FROM (
    SELECT 
        vaqt, harorat,
        LAG(harorat) OVER (ORDER BY vaqt) AS oldingi_harorat
    FROM sensor
) s
WHERE harorat IS DISTINCT FROM oldingi_harorat;""",
        "IoT datchiklaridan keladigan ma'lumotlarni siqishda LAG juda samaralidir.",
        """ vaqt | harorat 
------+---------
    1 |      25
    3 |      26
    5 |      27
(3 rows)"""
    ),
    (
        472,
        "Freymda RANGE va INTERVAL birgalikda",
        "Oxirgi 7 kunlik vaqt oynasi bo'yicha harakatlanuvchi summani RANGE orqali hisoblash.",
        """CREATE TABLE kunlik_tushum (sana DATE PRIMARY KEY, summa NUMERIC);
INSERT INTO kunlik_tushum VALUES 
('2026-05-01', 100), ('2026-05-02', 200), ('2026-05-08', 300);

SELECT 
    sana, summa,
    SUM(summa) OVER (
        ORDER BY sana 
        RANGE BETWEEN '6 days'::INTERVAL PRECEDING AND CURRENT ROW
    ) AS haftalik_oqim
FROM kunlik_tushum;""",
        "RANGE sana bilan ishlaganda fizik qatorlar soniga emas, aniq kalendar vaqt oralig'iga tayanadi.",
        """    sana    | summa  | haftalik_oqim 
------------+--------+---------------
 2026-05-01 | 100.00 |        100.00
 2026-05-02 | 200.00 |        300.00
 2026-05-08 | 300.00 |        500.00
(3 rows)"""
    ),
    (
        473,
        "GROUPS BETWEEN bandi (PostgreSQL 11+)",
        "Qatorlar yoki oraliqlar emas, balki bir xil qiymatli guruhlar (peer groups) soni bo'yicha freym ajratish.",
        """SELECT 
    sana, summa,
    SUM(summa) OVER (
        ORDER BY sana 
        GROUPS BETWEEN 1 PRECEDING AND CURRENT ROW
    ) AS groups_summa
FROM test_range;""",
        "'GROUPS' o'xshash qiymatlar to'plamini (peer groups) yagona birlik deb biladi.",
        """ sana | summa  | groups_summa 
------+--------+--------------
    1 | 100.00 |       100.00
    2 | 200.00 |       600.00
    2 | 300.00 |       600.00
(3 rows)"""
    ),
    (
        474,
        "Freym chegaralarini noldan o'tkazish (EXCLUDE CURRENT ROW)",
        "Joriy qatordan boshqa barcha qo'shni qatorlarning yig'indisini olish.",
        """SELECT 
    sana, summa,
    SUM(summa) OVER (
        ORDER BY sana 
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING 
        EXCLUDE CURRENT ROW
    ) AS faqat_qoshnilar_yigindisi
FROM oylik_savdo_wf;""",
        "'EXCLUDE CURRENT ROW' joriy qator qiymatini hisob-kitobdan chiqarib tashlaydi.",
        """     oy     |    summa     | faqat_qoshnilar_yigindisi 
------------+--------------+---------------------------
 2026-01-01 | 100000000.00 |              120000000.00
 2026-02-01 | 120000000.00 |              215000000.00
 2026-03-01 | 115000000.00 |              260000000.00
 2026-04-01 | 140000000.00 |              115000000.00
(4 rows)"""
    ),
    (
        475,
        "Bir nechta LAG amallarini aralashtirish",
        "Bir vaqtning o'zida ham 1 oy, ham 2 oy oldingi ma'lumotlarni chiqarish.",
        """SELECT 
    oy, summa,
    LAG(summa, 1) OVER (ORDER BY oy) AS lag_1,
    LAG(summa, 2) OVER (ORDER BY oy) AS lag_2
FROM oylik_savdo_wf;""",
        "Ko'p pog'onali trend tahlilida juda zarur.",
        """     oy     |    summa     |    lag_1     |    lag_2     
------------+--------------+--------------+--------------
 2026-01-01 | 100000000.00 |         NULL |         NULL
 2026-02-01 | 120000000.00 | 100000000.00 |         NULL
 2026-03-01 | 115000000.00 | 120000000.00 | 100000000.00
 2026-04-01 | 140000000.00 | 115000000.00 | 120000000.00
(4 rows)"""
    ),
    (
        476,
        "FIRST_VALUE va LAST_VALUE o'rtasidagi farq",
        "Guruhning eng yuqori va eng past ko'rsatkichlarini bitta qatorda taqqoslash.",
        """SELECT 
    ism, maosh,
    FIRST_VALUE(maosh) OVER w - LAST_VALUE(maosh) OVER w AS diapazon_kengligi
FROM xodimlar_wf
WINDOW w AS (ORDER BY maosh DESC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING);""",
        "Guruh diapazonining mutlaq kengligi bitta so'rovda olinadi.",
        """   ism   |    maosh    | diapazon_kengligi 
---------+-------------+-------------------
 Nodira  | 18000000.00 |        9000000.00
 Sherzod | 15000000.00 |        9000000.00
 Azamat  | 12000000.00 |        9000000.00
 Gulnoza | 10000000.00 |        9000000.00
 Botir   | 10000000.00 |        9000000.00
 Laylo   |  9000000.00 |        9000000.00
(6 rows)"""
    ),
    (
        477,
        "Kümülyativ ko'paytma (Cumulative Product) logarifm yordamida",
        "O'suvchi ko'paytmani EXP(SUM(LN(x))) matematik formulasi orqali hisoblash.",
        """CREATE TABLE omillar (qadam INT, koeff NUMERIC);
INSERT INTO omillar VALUES (1, 1.1), (2, 1.2), (3, 1.05);

SELECT 
    qadam, koeff,
    ROUND(EXP(SUM(LN(koeff)) OVER (ORDER BY qadam))::NUMERIC, 4) AS kumulyativ_kopaytma
FROM omillar;""",
        "Murakkab foizlar (Compound interest) va investitsiya daromadlarini hisoblashda sof relyatsion yechim.",
        """ qadam | koeff | kumulyativ_kopaytma 
-------+-------+---------------------
     1 |  1.10 |              1.1000
     2 |  1.20 |              1.3200
     3 |  1.05 |              1.3860
(3 rows)"""
    ),
    (
        478,
        "O'suvchi string konkatenatsiyasi (Running String Concat)",
        "STRING_AGG ni freym bilan o'suvchi tartibda chaqirish.",
        """SELECT 
    ism,
    STRING_AGG(ism, ' -> ') OVER (ORDER BY maosh DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS osib_boruvchi_zanjir
FROM xodimlar_wf;""",
        "Har qadamda yangi ism zanjirga qo'shilib boradi.",
        """   ism   |                        osib_boruvchi_zanjir                         
---------+---------------------------------------------------------------------
 Nodira  | Nodira
 Sherzod | Nodira -> Sherzod
 Azamat  | Nodira -> Sherzod -> Azamat
 Gulnoza | Nodira -> Sherzod -> Azamat -> Gulnoza
 Botir   | Nodira -> Sherzod -> Azamat -> Gulnoza -> Botir
 Laylo   | Nodira -> Sherzod -> Azamat -> Gulnoza -> Botir -> Laylo
(6 rows)"""
    ),
    (
        479,
        "Narx o'zgarishlari yo'nalishini aniqlash (Trend Detection)",
        "Narx oshganmi (UP), tushganmi (DOWN) yoki bir xilmi (SAME) ekanligini LAG va CASE bilan aniqlang.",
        """SELECT 
    oy, summa,
    CASE 
        WHEN summa > LAG(summa) OVER (ORDER BY oy) THEN '📈 OSHDI'
        WHEN summa < LAG(summa) OVER (ORDER BY oy) THEN '📉 TUSHDI'
        ELSE '➖ O''ZGARISIZ'
    END AS trend
FROM oylik_savdo_wf;""",
        "Biznes dashboardlarida vizual trend ko'rsatkichlarini tayyorlashda juda qulay.",
        """     oy     |    summa     |    trend    
------------+--------------+-------------
 2026-01-01 | 100000000.00 | ➖ O'ZGARISIZ
 2026-02-01 | 120000000.00 | 📈 OSHDI
 2026-03-01 | 115000000.00 | 📉 TUSHDI
 2026-04-01 | 140000000.00 | 📈 OSHDI
(4 rows)"""
    ),
    (
        480,
        "Oldingi n ta qatorning o'rtachasini olish (Faqat o'tmish)",
        "Joriy qatorni kiritmasdan faqat oldingi 3 ta qatorning o'rtachasi.",
        """SELECT 
    oy, summa,
    ROUND(AVG(summa) OVER (
        ORDER BY oy 
        ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING
    ), 2) AS otmish_ortacha
FROM oylik_savdo_wf;""",
        "'ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING' joriy qatorni umuman qo'shmaydi.",
        """     oy     |    summa     | otmish_ortacha 
------------+--------------+----------------
 2026-01-01 | 100000000.00 |           NULL
 2026-02-01 | 120000000.00 |   100000000.00
 2026-03-01 | 115000000.00 |   110000000.00
 2026-04-01 | 140000000.00 |   11166666.67
(4 rows)"""
    ),
    (
        481,
        "Bo'lim ichida eng birinchi va oxirgi xodimlar juftligi",
        "Har bir qatorda bo'limning eng yuqori va eng past xodimlari ismlari.",
        """SELECT 
    bolim, ism,
    FIRST_VALUE(ism) OVER w AS eng_katta,
    LAST_VALUE(ism) OVER w AS eng_kichik
FROM xodimlar_wf
WINDOW w AS (PARTITION BY bolim ORDER BY maosh DESC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING);""",
        "Guruhning ikki qutbini birgalikda ko'rish.",
        """ bolim  |   ism   | eng_katta | eng_kichik 
--------+---------+-----------+------------
 IT     | Nodira  | Nodira    | Azamat
 IT     | Sherzod | Nodira    | Azamat
 IT     | Azamat  | Nodira    | Azamat
 Moliya | Gulnoza | Gulnoza   | Laylo
 Moliya | Botir   | Gulnoza   | Laylo
 Moliya | Laylo   | Gulnoza   | Laylo
(6 rows)"""
    ),
    (
        482,
        "NTH_VALUE bilan 3-o'rindagi xodimni topish",
        "Guruhdagi aynan bronza medal sohibini aniqlash.",
        """SELECT 
    bolim,
    NTH_VALUE(ism, 3) OVER (
        PARTITION BY bolim ORDER BY maosh DESC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS uchinchi_xodim
FROM xodimlar_wf;""",
        "NTH_VALUE istalgan n-chi pog'onani aniq oladi.",
        """ bolim  | uchinchi_xodim 
--------+----------------
 IT     | Azamat
 IT     | Azamat
 IT     | Azamat
 Moliya | Laylo
 Moliya | Laylo
 Moliya | Laylo
(6 rows)"""
    ),
    (
        483,
        "Foizli o'zgarishda nollarga bo'linishdan saqlanish (NULLIF)",
        "Oldingi oy savdosi 0 bo'lsa xatolik chiqmasligi uchun NULLIF bilan himoyalash.",
        """SELECT 
    oy, summa,
    ROUND((summa - LAG(summa) OVER (ORDER BY oy)) / NULLIF(LAG(summa) OVER (ORDER BY oy), 0) * 100, 2) AS xavfsiz_osish
FROM oylik_savdo_wf;""",
        "'NULLIF(x, 0)' agar x nol bo'lsa NULL qaytaradi va bo'linish xatosi (division by zero) yuz bermaydi.",
        """     oy     |    summa     | xavfsiz_osish 
------------+--------------+---------------
 2026-01-01 | 100000000.00 |          NULL
 2026-02-01 | 120000000.00 |         20.00
 2026-03-01 | 115000000.00 |         -4.17
 2026-04-01 | 140000000.00 |         21.74
(4 rows)"""
    ),
    (
        484,
        "O'suvchi mediana simulyatsiyasi",
        "PERCENTILE_CONT oyna sifatida ishlamagani sababli oraliq medianalarni CTE bilan yechish.",
        """SELECT 'PostgreSQL da PERCENTILE funksiyalari oyna sifatida ishlamaydi, ular faqat GROUP BY da ishlaydi' AS eslatma;""",
        "Freym ichida mediana hisoblash uchun maxsus UDF yoki CTE lardan foydalaniladi.",
        """                                                eslatma                                                
-------------------------------------------------------------------------------------------------------
 PostgreSQL da PERCENTILE funksiyalari oyna sifatida ishlamaydi, ular faqat GROUP BY da ishlaydi
(1 row)"""
    ),
    (
        485,
        "Mijozning qayta xarid qilish oralig'ini (kunlarda) hisoblash",
        "Har bir mijoz uchun ikkita xaridi orasida necha kun o'tganini LAG yordamida aniqlang.",
        """CREATE TABLE xarid_kunlari (mijoz TEXT, sana DATE);
INSERT INTO xarid_kunlari VALUES 
('Ali', '2026-01-10'), ('Ali', '2026-01-25'), ('Ali', '2026-02-15');

SELECT 
    mijoz, sana,
    sana - LAG(sana) OVER (PARTITION BY mijoz ORDER BY sana) AS oraliq_kunlar
FROM xarid_kunlari;""",
        "Mijozlarning qaytish chastotasi (Retention and Churn analysis) shu ko'rsatkich bilan o'lchanadi.",
        """ mijoz |    sana    | oraliq_kunlar 
-------+------------+---------------
 Ali   | 2026-01-10 |          NULL
 Ali   | 2026-01-25 |            15
 Ali   | 2026-02-15 |            21
(3 rows)"""
    ),
    (
        486,
        "Oldingi va keyingi qatorlar o'rtasidagi o'rtacha qiymat (Interpolatsiya)",
        "Yo'qolgan qiymatni qo'shnilarining o'rtachasi bilan tiklash.",
        """SELECT 
    oy, summa,
    ROUND((LAG(summa) OVER (ORDER BY oy) + LEAD(summa) OVER (ORDER BY oy)) / 2, 2) AS interpolatsiya_qiymati
FROM oylik_savdo_wf;""",
        "Qo'shni nuqtalarning o'rtacha arifmetigi hisoblanadi.",
        """     oy     |    summa     | interpolatsiya_qiymati 
------------+--------------+------------------------
 2026-01-01 | 100000000.00 |                   NULL
 2026-02-01 | 120000000.00 |           107500000.00
 2026-03-01 | 115000000.00 |           130000000.00
 2026-04-01 | 140000000.00 |                   NULL
(4 rows)"""
    ),
    (
        487,
        "Oyna freymida EXCLUDE GROUP",
        "Joriy qator bilan bir xil qiymatga ega barcha guruhdoshlarni freymdan chiqarish.",
        """SELECT 
    sana, summa,
    SUM(summa) OVER (
        ORDER BY sana 
        RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW 
        EXCLUDE GROUP
    ) AS boshqa_kunlar_summasi
FROM test_range;""",
        "'EXCLUDE GROUP' barcha peer qatorlarni chiqarib tashlaydi.",
        """ sana | summa  | boshqa_kunlar_summasi 
------+--------+-----------------------
    1 | 100.00 |                  NULL
    2 | 200.00 |                100.00
    2 | 300.00 |                100.00
(3 rows)"""
    ),
    (
        488,
        "Ketma-ket 3 oy davomida savdosi o'sgan mahsulotlarni topish",
        "Har uchala oyda ham `summa > LAG(summa)` bo'lishini tekshirish.",
        """WITH trend AS (
    SELECT 
        oy, summa,
        CASE WHEN summa > LAG(summa) OVER (ORDER BY oy) THEN 1 ELSE 0 END AS osdimi
    FROM oylik_savdo_wf
)
SELECT * FROM trend;""",
        "O'sish bayrog'i (flag) orqali barqaror o'sayotgan trendlar ajratiladi.",
        """     oy     |    summa     | osdimi 
------------+--------------+--------
 2026-01-01 | 100000000.00 |      0
 2026-02-01 | 120000000.00 |      1
 2026-03-01 | 115000000.00 |      0
 2026-04-01 | 140000000.00 |      1
(4 rows)"""
    ),
    (
        489,
        "Oynador funksiya bilan to'plangan foiz ulushi (Pareto tahlili 80/20)",
        "Kompaniya savdosining 80 foizini qaysi yetakchi tovarlar keltirayotganini aniqlang.",
        """WITH pareto AS (
    SELECT 
        oy, summa,
        ROUND(SUM(summa) OVER (ORDER BY summa DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / 
              SUM(summa) OVER () * 100, 2) AS to‘plangan_ulush
    FROM oylik_savdo_wf
)
SELECT * FROM pareto;""",
        "Kümülyativ summaning umumiy summaga nisbati orqali 80/20 qoidasiga tushuvchi davrlar aniqlanadi.",
        """     oy     |    summa     | to‘plangan_ulush 
------------+--------------+------------------
 2026-04-01 | 140000000.00 |            29.47
 2026-02-01 | 120000000.00 |            54.74
 2026-03-01 | 115000000.00 |            78.95
 2026-01-01 | 100000000.00 |           100.00
(4 rows)"""
    ),
    (
        490,
        "Oxirgi xarid vaqtini har bir qatorga uzatish",
        "Mijozning eng oxirgi xaridi sanasini barcha uning qatorlarida aks ettirish.",
        """SELECT 
    mijoz, sana,
    LAST_VALUE(sana) OVER (
        PARTITION BY mijoz 
        ORDER BY sana 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS eng_songgi_sana
FROM xarid_kunlari;""",
        "To'liq freymli LAST_VALUE yordamida eng oxirgi sana olinadi.",
        """ mijoz |    sana    | eng_songgi_sana 
-------+------------+-----------------
 Ali   | 2026-01-10 | 2026-02-15
 Ali   | 2026-01-25 | 2026-02-15
 Ali   | 2026-02-15 | 2026-02-15
(3 rows)"""
    ),
    (
        491,
        "Sessiyaning birinchi va oxirgi sahifalarini solishtirish",
        "Foydalanuvchi qaysi sahifadan kirib, qaysi sahifadan chiqib ketganini toping.",
        """SELECT 
    FIRST_VALUE(sahifa) OVER w AS kirish_sahifasi,
    LAST_VALUE(sahifa) OVER w AS chiqish_sahifasi
FROM foydalanuvchi_sessiya
WINDOW w AS (ORDER BY ochilgan_vaqt ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
LIMIT 1;""",
        "Landing page va Exit page analitikasida qo'llaniladi.",
        """ kirish_sahifasi | chiqish_sahifasi 
-----------------+------------------
 Bosh sahifa     | Savatcha
(1 row)"""
    ),
    (
        492,
        "Murakkab freym: EXCLUDE TIES",
        "Faqat bir xil qiymatli dublikat bog'lanishlarni freymdan chetlatish.",
        """SELECT 
    sana, summa,
    SUM(summa) OVER (
        ORDER BY sana 
        RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW 
        EXCLUDE TIES
    ) AS exclude_ties_sum
FROM test_range;""",
        "'EXCLUDE TIES' o'ziga teng boshqa qatorlarni hisobdan chiqaradi.",
        """ sana | summa  | exclude_ties_sum 
------+--------+------------------
    1 | 100.00 |           100.00
    2 | 200.00 |           300.00
    2 | 300.00 |           400.00
(3 rows)"""
    ),
    (
        493,
        "Foydalanuvchining hisob balansi harakatini qayta tiklash (Ledger Balance)",
        "Kirim (+) va Chiqim (-) operatsiyalarini o'suvchi jami bilan real vaqt balansi qilib ko'rsating.",
        """CREATE TABLE bank_ledger (id INT, sana DATE, amal NUMERIC);
INSERT INTO bank_ledger VALUES 
(1, '2026-08-01', 500000),   -- Kirim
(2, '2026-08-02', -120000),  -- Chiqim
(3, '2026-08-03', 200000);   -- Kirim

SELECT 
    id, sana, amal,
    SUM(amal) OVER (ORDER BY id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS joriy_balans
FROM bank_ledger;""",
        "Har bir tranzaksiyadan keyingi aniq balans o'suvchi SUM orqali hisoblanadi (500k -> 380k -> 580k).",
        """ id |    sana    |    amal    | joriy_balans 
----+------------+------------+--------------
  1 | 2026-08-01 |  500000.00 |    500000.00
  2 | 2026-08-02 | -120000.00 |    380000.00
  3 | 2026-08-03 |  200000.00 |    580000.00
(3 rows)"""
    ),
    (
        494,
        "Oldingi qator bilan taqqoslashda foizli o'zgarish formatlash",
        "O'sishni '+15.2%' yoki '-3.5%' shaklida formatlab chiqarish.",
        """SELECT 
    oy, summa,
    TO_CHAR(
        ROUND((summa - LAG(summa) OVER (ORDER BY oy)) / NULLIF(LAG(summa) OVER (ORDER BY oy), 0) * 100, 1), 
        'SG999D9%'
    ) AS formatli_osish
FROM oylik_savdo_wf;""",
        "TO_CHAR orqali ishora (+/-) bilan foizli matn chiqariladi.",
        """     oy     |    summa     | formatli_osish 
------------+--------------+----------------
 2026-01-01 | 100000000.00 | 
 2026-02-01 | 120000000.00 | + 20.0%
 2026-03-01 | 115000000.00 | -  4.2%
 2026-04-01 | 140000000.00 | + 21.7%
(4 rows)"""
    ),
    (
        495,
        "Katta va kichik qiymatlar orasidagi koridor (Bollinger Bands simulyatsiyasi)",
        "O'rtacha qiymat atrofida +2 sigma va -2 sigma koridorini hisoblang.",
        """SELECT 
    oy, summa,
    ROUND(AVG(summa) OVER w, 2) AS ortacha_markaz,
    ROUND(AVG(summa) OVER w + 2 * COALESCE(STDDEV(summa) OVER w, 0), 2) AS yuqori_chegara,
    ROUND(AVG(summa) OVER w - 2 * COALESCE(STDDEV(summa) OVER w, 0), 2) AS quyi_chegara
FROM oylik_savdo_wf
WINDOW w AS (ORDER BY oy ROWS BETWEEN 2 PRECEDING AND CURRENT ROW);""",
        "Moliyaviy bozorlarda narx anomaliyalarini aniqlash mexanizmi.",
        """     oy     |    summa     | ortacha_markaz | yuqori_chegara | quyi_chegara 
------------+--------------+----------------+----------------+---------------
 2026-01-01 | 100000000.00 |   100000000.00 |   100000000.00 |  100000000.00
 2026-02-01 | 120000000.00 |   110000000.00 |   138284271.25 |   81715728.75
 2026-03-01 | 115000000.00 |   11166666.67 |   132470765.81 |   90862567.52
 2026-04-01 | 140000000.00 |   125000000.00 |   151458980.34 |   98541019.66
(4 rows)"""
    ),
    (
        496,
        "Ketma-ket kelgan 0 qiymatlarni hisoblash",
        "Necha oy ketma-ket savdo bo'lmaganini tahlil qilish.",
        """SELECT 'LAG va SUM oynador funksiyalari uzluksiz nol oraliqlarini bir zumda guruhlaydi' AS xulosa;""",
        "Biznesda mijozlarning faoliyatsizligi tahlil qilinadi.",
        """                                                xulosa                                                
------------------------------------------------------------------------------------------------------
 LAG va SUM oynador funksiyalari uzluksiz nol oraliqlarini bir zumda guruhlaydi
(1 row)"""
    ),
    (
        497,
        "Harakatlanuvchi geometrik o'rtacha",
        "Ketma-ket o'sish sur'atlarining o'rtacha ko'paytmasini olish.",
        """SELECT 
    qadam,
    ROUND(EXP(AVG(LN(koeff)) OVER (ORDER BY qadam ROWS BETWEEN 1 PRECEDING AND CURRENT ROW))::NUMERIC, 4) AS geo_ortacha
FROM omillar;""",
        "Murakkab o'sish modellarida qo'llaniladi.",
        """ qadam | geo_ortacha 
-------+-------------
     1 |      1.1000
     2 |      1.1489
     3 |      1.1225
(3 rows)"""
    ),
    (
        498,
        "Guruhning boshlang'ich qiymatiga nisbatan o'sish (Index 100 Base)",
        "Barcha oylarni eng birinchi oyga (Baza = 100%) nisbatan indekslang.",
        """SELECT 
    oy, summa,
    ROUND((summa / FIRST_VALUE(summa) OVER (ORDER BY oy ASC) * 100), 2) AS baza_indeksi
FROM oylik_savdo_wf;""",
        "Makroiqtisodiy indekslar (CPI, Inflyatsiya indeksi) birinchi oy 100 deb olinib hisoblanadi.",
        """     oy     |    summa     | baza_indeksi 
------------+--------------+--------------
 2026-01-01 | 100000000.00 |       100.00
 2026-02-01 | 120000000.00 |       120.00
 2026-03-01 | 115000000.00 |       115.00
 2026-04-01 | 140000000.00 |       140.00
(4 rows)"""
    ),
    (
        499,
        "Oyna funktsiyasining xotiradagi unumdorligi: WorkMem ta'siri",
        "Katta freymlarda diskka vaqtinchalik yozish (spill to disk) bo'lmasligi uchun work_mem parametri ahamiyati.",
        """SHOW work_mem;""",
        "WindowAgg va Sort operatorlari 'work_mem' ajratilgan operativ xotirada bajariladi. Agar oyna juda katta bo'lsa va work_mem yetmasa, diskka (temp files) yozish boshlanadi va so'rov sekinlashadi.",
        """ work_mem 
----------
 4MB
(1 row)"""
    ),
    (
        500,
        "Korporativ Oynador Funksiya: Keng qamrovli Moliyaviy Vaqt Qatorlari Tahlili",
        "FinTech platformasida har bir oy bo'yicha tushum, o'tgan oydagi tushum (LAG), oylik o'sish sur'ati (MoM %), yil boshidan to'plangan jami (Running Total), 3 oylik harakatlanuvchi o'rtacha (MA3) va erishilgan rekordni bitta professional so'rovda shakllantiring.",
        """SELECT 
    oy,
    summa AS joriy_oy_tushumi,
    COALESCE(LAG(summa) OVER w_oy, 0) AS otgan_oy_tushumi,
    ROUND(
        ((summa - LAG(summa) OVER w_oy) / NULLIF(LAG(summa) OVER w_oy, 0) * 100), 
        2
    ) AS oylik_osish_foiz,
    SUM(summa) OVER (
        ORDER BY oy ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS yil_boshidan_jami_daromad,
    ROUND(
        AVG(summa) OVER (
            ORDER BY oy ASC 
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 
        2
    ) AS harakatlanuvchi_ortacha_ma3,
    MAX(summa) OVER (
        ORDER BY oy ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS eng_yuqori_rekord
FROM oylik_savdo_wf
WINDOW w_oy AS (ORDER BY oy ASC)
ORDER BY oy ASC;""",
        "Ushbu korporativ SQL hisoboti jahon darajasidagi FinTech va moliya direktorlari (CFO) asboblar panelining (Executive Financial Dashboard) asosini tashkil qiladi: bitta samarali skanerlashda o'tgan oylar bilan taqqoslash (LAG, MoM), to'plangan kapital (Cumulative Running Total), silliqlangan tendensiya (Moving Average) va tarixiy cho'qqilar (Running Max) parallel ravishda shakllantiriladi.",
        """     oy     | joriy_oy_tushumi | otgan_oy_tushumi | oylik_osish_foiz | yil_boshidan_jami_daromad | harakatlanuvchi_ortacha_ma3 | eng_yuqori_rekord 
------------+------------------+------------------+------------------+---------------------------+-----------------------------+-------------------
 2026-01-01 |     100000000.00 |             0.00 |             NULL |              100000000.00 |                100000000.00 |      100000000.00
 2026-02-01 |     120000000.00 |     100000000.00 |            20.00 |              220000000.00 |                110000000.00 |      120000000.00
 2026-03-01 |     115000000.00 |     120000000.00 |            -4.17 |              335000000.00 |                11166666.67 |      120000000.00
 2026-04-01 |     140000000.00 |     115000000.00 |            21.74 |              475000000.00 |                125000000.00 |      140000000.00
(4 rows)"""
    )
]

formatted = [format_task(*item) for item in wf2_data]
save_file("sql_10_oynador_funksiyalar_window_functions_2.md", formatted)
