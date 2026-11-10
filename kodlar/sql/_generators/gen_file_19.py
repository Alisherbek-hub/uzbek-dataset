# -*- coding: utf-8 -*-
"""
Generator for File 19: sql_19_json_va_zamonaviy_malumotlar_bilan_ishlash.md
Tasks 901 - 950
Mavzu: JSON va zamonaviy ma'lumotlar bilan ishlash (JSON, JSONB, operatorlar, GIN indekslar, json_agg, jsonb_set, JSONPath)
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

def add_task(num, title, condition, sql, explanation, output):
    tasks.append(format_task(num, title, condition, sql, explanation, output))

# 901
add_task(
    901,
    "JSON va JSONB turlarining asosiy farqlari (Format va saqlanish)",
    "`JSON` va `JSONB` ma'lumot turlarini yaratib, ularning bo'shliqlar, kalitlar tartibi va dublikat kalitlarni qanday qayta ishlashini taqqoslovchi SQL so'rovini yozing.",
    """SELECT 
    '{"ism": "Ali",  "yosh":  25, "ism": "Vali"}'::json  AS json_formati,
    '{"ism": "Ali",  "yosh":  25, "ism": "Vali"}'::jsonb AS jsonb_formati;""",
    "PostgreSQL'da `JSON` turi kiruvchi matnni aynan o'z holicha (harfma-harf, bo'shliqlari va dublikat kalitlari bilan birga) saqlaydi va har safar o'qilganda qaytadan parse qilinadi. `JSONB` esa dekonstruktsiyalangan binar formatda saqlanadi: keraksiz bo'shliqlar olib tashlanadi, kalitlar alfavit bo'yicha saralanadi va dublikat kalitlardan eng oxirgisi saqlanadi. Shu sababli JSONB indekslanadi va qidiruvda ancha tez ishlaydi.",
    """                    json_formati                    |        jsonb_formati        
----------------------------------------------------+-----------------------------
 {"ism": "Ali",  "yosh":  25, "ism": "Vali"}        | {"ism": "Vali", "yosh": 25}
(1 row)"""
)

# 902
add_task(
    902,
    "-> va ->> operatorlari yordamida kalit qiymatlarini ajratib olish",
    "Mijoz profili JSONB hujjatidan `ism` maydonini matn (TEXT) sifatida va `yosh` maydonini butun son (INT) sifatida alohida ustunlarga ajrating.",
    """WITH data AS (
    SELECT '{"ism": "Sardor", "yosh": 28, "shahar": "Toshkent"}'::jsonb AS profil
)
SELECT 
    profil -> 'ism'        AS ism_json,
    profil ->> 'ism'       AS ism_text,
    (profil ->> 'yosh')::INT AS yosh_son
FROM data;""",
    "`->` operatori natijani JSON yoki JSONB obyekt/qiymat sifatida qaytaradi (matn qo'shtirnoqlari saqlanadi: `\"Sardor\"`). `->>` operatori esa natijani to'g'ridan-to'g'ri `TEXT` turiga o'girib beradi (`Sardor`). Matematik hisob-kitoblar yoki filtrlashda `->>` orqali olingan matn `::INT` yoki `::NUMERIC` ga o'tkaziladi.",
    """  ism_json  | ism_text | yosh_son 
------------+----------+----------
 "Sardor"   | Sardor   |       28
(1 row)"""
)

# 903
add_task(
    903,
    "Ichma-ich joylashgan JSON ob'ektlarini #> va #>> orqali o'qish",
    "Kompaniya ma'lumotlaridagi manzil iyerarxiyasidan (`manzil -> shahar -> tuman`) qiymatni path (yo'l) massivi orqali to'g'ridan-to'g'ri o'qib oling.",
    """WITH tashkilotlar AS (
    SELECT '{"nomi": "Apex Tech", "manzil": {"mamlakat": "Uzbekistan", "shahar": {"nomi": "Samarqand", "tuman": "Urgut"}}}'::jsonb AS data
)
SELECT 
    data #>  '{manzil, shahar}'         AS shahar_obekt,
    data #>> '{manzil, shahar, tuman}'   AS tuman_nomi
FROM tashkilotlar;""",
    "`#>` operatori massiv ko'rinishidagi yo'l bo'yicha ichki obyektni JSONB sifatida qaytaradi. `#>>` esa ko'rsatilgan iyerarxiya oxiridagi qiymatni toza matn (`TEXT`) sifatida chiqarib beradi. Bu `data->'manzil'->'shahar'->>'tuman'` zanjirini yozishdan ko'ra qisqaroq va qulayroqdir.",
    """        shahar_obekt         | tuman_nomi 
-----------------------------+------------
 {"nomi": "Samarqand", "tuman": "Urgut"} | Urgut
(1 row)"""
)

# 904
add_task(
    904,
    "JSON massiv elementlarini indeks bo'yicha olish",
    "Xodimning ko'nikmalari (`skills`) massividan birinchi (0-indeks) va uchinchi (2-indeks) elementlarni ajratib oling.",
    """WITH xodim AS (
    SELECT '{"ism": "Nodira", "skills": ["PostgreSQL", "Go", "Docker", "Kubernetes"]}'::jsonb AS doc
)
SELECT 
    doc -> 'skills' -> 0   AS birinchi_skill_json,
    doc -> 'skills' ->> 0  AS birinchi_skill_text,
    doc -> 'skills' ->> 2  AS uchinchi_skill_text
FROM xodim;""",
    "PostgreSQL da JSON massivlari nolga asoslangan indekslash (0-indexed) qoidasiga amal qiladi. `-> butun_son` orqali massiv elementi olinadi. `->> 0` birinchi elementni qo'shtirnoqsiz toza matn ko'rinishida beradi.",
    """ birinchi_skill_json | birinchi_skill_text | uchinchi_skill_text 
---------------------+---------------------+---------------------
 "PostgreSQL"        | PostgreSQL          | Docker
(1 row)"""
)

# 905
add_task(
    905,
    "JSONB mavjudlik (Existence) operatorlari: ?, ?| va ?&",
    "Foydalanuvchi sozlamalarida `qorongu_mavzu` kaliti borligini, yoki `email`/`sms` kalitlaridan kamida biri borligini, yoki `til` va `valyuta` har ikkisi ham qatnashganligini tekshiring.",
    """WITH sozlamalar AS (
    SELECT '{"til": "uz", "valyuta": "UZS", "qorongu_mavzu": true, "sms": false}'::jsonb AS config
)
SELECT 
    config ? 'qorongu_mavzu'               AS mavzu_bormi,
    config ?| array['email', 'sms']        AS aloqa_kanali_bormi,
    config ?& array['til', 'valyuta']      AS asosiy_sozlamalar_bormi,
    config ? 'push'                        AS push_bormi
FROM sozlamalar;""",
    "`? 'kalit'` operatori ko'rsatilgan kalit yoki qator JSONB obyektida mavjud bo'lsa `TRUE` qaytaradi. `?| array[...]` ro'yxatdagi kalitlardan kamida bittasi bo'lsa, `?& array[...]` esa ro'yxatdagi barcha kalitlar to'liq mavjud bo'lgandagina `TRUE` beradi.",
    """ mavzu_bormi | aloqa_kanali_bormi | asosiy_sozlamalar_bormi | push_bormi 
-------------+--------------------+-------------------------+-----------
 t           | t                  | t                       | f
(1 row)"""
)

# 906
add_task(
    906,
    "JSONB tarkibida bo'lish (Containment) operatorlari: @> va <@",
    "Ombordagi tovarlar orasidan toifasi 'Noutbuk' va brendi 'Dell' bo'lgan barcha tovarlarni `@>` operatori orqali filtrlang.",
    """SELECT id, nomi, parametrlar
FROM tovarlar
WHERE parametrlar @> '{"kategoriya": "Noutbuk", "brend": "Dell"}';""",
    "`chap @> ong` operatori chap tarafdagi JSONB o'ng tarafdagi JSONB tuzilmasini o'z ichiga to'liq qamrab olishini (contains) tekshiradi. Ushbu operator GIN indeksi bilan to'liq quvvatlanadi va millionlab qatorli NoSQL uslubidagi ma'lumotlarni millisoniyalarda topish imkonini beradi.",
    """ id |        nomi        |                       parametrlar                       
----+--------------------+---------------------------------------------------------
  4 | Dell XPS 15        | {"ram": 32, "brend": "Dell", "kategoriya": "Noutbuk"}
  9 | Dell Latitude 5420 | {"ram": 16, "brend": "Dell", "kategoriya": "Noutbuk"}
(2 rows)"""
)

# 907
add_task(
    907,
    "jsonb_set orqali mavjud JSONB hujjatini tahrirlash",
    "Foydalanuvchi profilidagi `shahar` qiymatini 'Buxoro' ga o'zgartiring va mavjud bo'lmagan yangi `bonus` kalitini qo'shing.",
    """WITH data AS (
    SELECT '{"ism": "Anvar", "manzil": {"shahar": "Toshkent"}}'::jsonb AS doc
)
SELECT 
    -- 1. Mavjud ichki maydonni yangilash
    jsonb_set(doc, '{manzil, shahar}', '"Buxoro"') AS manzil_yangilandi,

    -- 2. Yangi maydon yaratish (create_missing = true)
    jsonb_set(doc, '{profil, bonus}', '50000', true) AS yangi_maydon_qoshildi
FROM data;""",
    "`jsonb_set(target, path, new_value, create_missing)` funksiyasi ko'rsatilgan yo'ldagi (path) qiymatni almashtiradi. To'rtinchi argument `create_missing = true` bo'lsa, yo'l mavjud bo'lmagan taqdirda yangi kalit hosil qilinadi.",
    """                     manzil_yangilandi                     |                               yangi_maydon_qoshildi                               
----------------------------------------------------------+-----------------------------------------------------------------------------------
 {"ism": "Anvar", "manzil": {"shahar": "Buxoro"}}         | {"ism": "Anvar", "manzil": {"shahar": "Toshkent"}, "profil": {"bonus": 50000}}
(1 row)"""
)

# 908
add_task(
    908,
    "JSONB massiviga element kiritish (jsonb_insert)",
    "JSONB massivining ma'lum bir pozitsiyasiga (masalan boshiga yoki oxiriga) yangi element qo'shish uchun `jsonb_insert` funksiyasidan foydalaning.",
    """WITH data AS (
    SELECT '{"kurslar": ["HTML", "CSS", "JavaScript"]}'::jsonb AS doc
)
SELECT 
    -- 1-indeks oldiga kiritish
    jsonb_insert(doc, '{kurslar, 1}', '"PostgreSQL"') AS oraga_qoshildi,

    -- Massiv oxiriga qo'shish (insert_after = true)
    jsonb_insert(doc, '{kurslar, -1}', '"Python"', true) AS oxiriga_qoshildi
FROM data;""",
    "`jsonb_insert(target, path, new_value, insert_after)` massiv ichiga maqsadli indeks bo'yicha element kiritadi. `insert_after = true` ko'rsatilgan indeksdan keyin joylashtirishni bildiradi (`-1` esa massivning eng oxirgi elementi).",
    """                  oraga_qoshildi                  |                   oxiriga_qoshildi                   
--------------------------------------------------+------------------------------------------------------
 {"kurslar": ["HTML", "PostgreSQL", "CSS", "JavaScript"]} | {"kurslar": ["HTML", "CSS", "JavaScript", "Python"]}
(1 row)"""
)

# 909
add_task(
    909,
    "- va #- operatorlari orqali JSON kalitlari va massiv indekslarini o'chirish",
    "Foydalanuvchi profilidan maxfiy `parol_hash` kalitini olib tashlang va ichki `manzil.pochta_indeks` kalitini `# -` yo'li orqali o'chiring.",
    """WITH data AS (
    SELECT '{"ism": "Ulugbek", "parol_hash": "secret123", "manzil": {"shahar": "Xiva", "pochta_indeks": "220100"}}'::jsonb AS doc
)
SELECT 
    -- Kalitni nomi bo'yicha o'chirish
    doc - 'parol_hash' AS kalit_ochirildi,

    -- Chuqur yo'l bo'yicha o'chirish
    doc #- '{manzil, pochta_indeks}' AS ichki_ochirildi
FROM data;""",
    "`jsonb - 'kalit'` operatori birinchi darajadagi kalitni o'chiradi (agar butun son berilsa massiv indeksini o'chiradi). `#- '{path}'` esa ixtiyoriy chuqurlikdagi element yoki kalitni o'chirishga xizmat qiladi.",
    """                               kalit_ochirildi                                |                               ichki_ochirildi                                
------------------------------------------------------------------------------+------------------------------------------------------------------------------
 {"ism": "Ulugbek", "manzil": {"shahar": "Xiva", "pochta_indeks": "220100"}} | {"ism": "Ulugbek", "manzil": {"shahar": "Xiva"}, "parol_hash": "secret123"}
(1 row)"""
)

# 910
add_task(
    910,
    "JSONB birlashtirish (Concatenation / Shallow Merge) || operatori",
    "Ikkita JSONB obyektini `||` operatori orqali birlashtiring. Agar bir xil kalitlar mavjud bo'lsa, o'ng tarafdagisi chap tarafdagisini qayta yozishini (override) ko'rsating.",
    """SELECT 
    '{"ism": "Bekzod", "yosh": 22, "shahar": "Toshkent"}'::jsonb 
    || 
    '{"yosh": 23, "kasb": "DevOps", "daraja": "Middle"}'::jsonb AS birlashgan_jsonb;""",
    "`jsonb || jsonb` operatori ikkita obyektni sayoz birlashtiradi (shallow merge). Bir xil nomli kalitlar mavjud bo'lsa, o'ng tarafdagi obyekt qiymati chap tarafdagi qiymat ustiga yoziladi, yangi kalitlar esa qo'shiladi.",
    """                                     birlashgan_jsonb                                     
------------------------------------------------------------------------------------------
 {"ism": "Bekzod", "kasb": "DevOps", "yosh": 23, "daraja": "Middle", "shahar": "Toshkent"}
(1 row)"""
)

# 911
add_task(
    911,
    "jsonb_strip_nulls yordamida NULL qiymatli kalitlarni tozalash",
    "JSONB obyektidagi barcha NULL qiymatli maydonlarni rekursiv ravishda tozalab tashlovchi so'rov yozing.",
    """SELECT jsonb_strip_nulls('{
    "ism": "Dilnoza",
    "email": "dilnoza@misol.uz",
    "telefon": null,
    "profil": {
        "rasm": null,
        "til": "uz"
    }
}'::jsonb) AS tozalangan_jsonb;""",
    "`jsonb_strip_nulls(jsonb)` barcha qiymati JSON `null` bo'lgan kalitlarni chuqur (nested) qidirib, obyektlardan chiqarib tashlaydi. Bu xotirani tejash va JSON payload hajmini optimallashtirishda juda foydalidir (massiv ichidagi null elementlar o'chirilmaydi).",
    """                       tozalangan_jsonb                       
--------------------------------------------------------------
 {"ism": "Dilnoza", "email": "dilnoza@misol.uz", "profil": {"til": "uz"}}
(1 row)"""
)

# 912
add_task(
    912,
    "Relyatsion ma'lumotlarni JSON obyektga aylantirish (to_json va to_jsonb)",
    "Xodimlar jadvalidagi har bir qatorni to'liq JSONB obyektiga aylantirib chiquvchi so'rov yozing.",
    """SELECT 
    id, 
    to_jsonb(x) AS xodim_jsonb 
FROM xodimlar x 
WHERE x.id <= 2;""",
    "`to_json(record)` va `to_jsonb(record)` relyatsion jadval qatorini yoki kompozit turni bittalik JSON/JSONB obyektiga aylantiradi. Ustun nomlari kalitlar, ustun qiymatlari esa mos JSON qiymatlari bo'ladi.",
    """ id |                                         xodim_jsonb                                         
----+---------------------------------------------------------------------------------------------
  1 | {"id": 1, "ism": "Alisher", "maosh": 25000000.00, "bolim_id": 1, "familiya": "Usmonov"}
  2 | {"id": 2, "ism": "Bobur", "maosh": 18000000.00, "bolim_id": 1, "familiya": "Rahimov"}
(2 rows)"""
)

# 913
add_task(
    913,
    "jsonb_build_object yordamida maxsus shakldagi JSON qurish",
    "Xodimlar jadvalidan foydalanib, faqat kerakli maydonlarni o'z ichiga olgan maxsus formatdagi JSON hujjatini quring.",
    """SELECT jsonb_build_object(
    'xodim_kodi', id,
    'shaxsiy_malumot', jsonb_build_object('ism', ism, 'familiya', familiya),
    'daromad', maosh,
    'holat', 'FAOL'
) AS maxsus_profil
FROM xodimlar
WHERE id = 1;""",
    "`jsonb_build_object(key1, val1, key2, val2, ...)` juftlik parametrlarini qabul qilib, xohlagan iyerarxik shakldagi yangi JSONB obyektini generatsiya qiladi. Bu REST API yoki GraphQL javoblarini to'g'ridan-to'g'ri SQL darajasida shakllantirishda tengsizdir.",
    """                                                              maxsus_profil                                                              
----------------------------------------------------------------------------------------------------------------------------------------
 {"holat": "FAOL", "daromad": 25000000.00, "xodim_kodi": 1, "shaxsiy_malumot": {"ism": "Alisher", "familiya": "Usmonov"}}
(1 row)"""
)

# 914
add_task(
    914,
    "jsonb_build_array yordamida aralash turlardan iborat massiv yaratish",
    "Turli xil turlardagi (son, matn, boolean va ichki JSON) qiymatlardan iborat JSON massivini yarating.",
    """SELECT jsonb_build_array(
    101,
    'Muvaffaqiyatli',
    TRUE,
    CURRENT_DATE,
    jsonb_build_object('kod', 'OK')
) AS aralash_massiv;""",
    "`jsonb_build_array(...)` berilgan barcha argumentlarni tartibi bo'yicha yagona JSON massiviga birlashtiradi va har bir parametr turini mos JSON turiga konvertatsiya qiladi.",
    """                           aralash_massiv                           
--------------------------------------------------------------------
 [101, "Muvaffaqiyatli", true, "2024-06-15", {"kod": "OK"}]
(1 row)"""
)

# 915
add_task(
    915,
    "json_agg va jsonb_agg yordamida qatorlarni bitta JSON massiviga agregatlash",
    "Har bir bo'lim bo'yicha bo'lim nomini va unga tegishli barcha xodimlarning ro'yxatini yagona JSONB massivi ko'rinishida guruhlang.",
    """SELECT 
    b.nomi AS bolim_nomi,
    jsonb_agg(
        jsonb_build_object('id', x.id, 'ism', x.ism, 'maosh', x.maosh) 
        ORDER BY x.maosh DESC
    ) AS xodimlar_royxati
FROM bolimlar b
JOIN xodimlar x ON b.id = x.bolim_id
GROUP BY b.id, b.nomi;""",
    "`jsonb_agg(ifoda)` relyatsion qatorlarni bitta JSON massiviga to'playdi. Ichida `ORDER BY` qo'llash orqali massiv elementlarining joylashuv tartibini kafolatlash mumkin. Natijada 1:N relyatsiyasi bitta so'rovda JSON ko'rinishida qaytadi.",
    """ bolim_nomi |                                      xodimlar_royxati                                       
------------+---------------------------------------------------------------------------------------------
 IT Bolimi  | [{"id": 1, "ism": "Alisher", "maosh": 25000000.00}, {"id": 2, "ism": "Bobur", "maosh": 18000000.00}]
(1 row)"""
)

# 916
add_task(
    916,
    "json_object_agg va jsonb_object_agg yordamida kalit-qiymat xaritasi (Map) tuzish",
    "Valyutalar jadvalidan foydalanib, valyuta kodini kalit, uning kursini qiymat qilib yagona JSON ob'ekti (dictionary / hash map) hosil qiling.",
    """SELECT jsonb_object_agg(kod, kurs) AS kurslar_xaritasi
FROM valyutalar;""",
    "`jsonb_object_agg(key_col, val_col)` ikki ustunni mos ravishda kalit va qiymat qilib oladi va ulardan bitta yagona JSONB lug'atini (dict) quradi. Bu frontend ilovalariga lookup jadvalini yuborishda juda qulay.",
    """                      kurslar_xaritasi                      
------------------------------------------------------------
 {"EUR": 13950.00, "RUB": 142.50, "USD": 12850.00}
(1 row)"""
)

# 917
add_task(
    917,
    "jsonb_array_elements yordamida massivni alohida qatorlarga yoyish",
    "Buyurtmadagi mahsulotlar massivini alohida relyatsion qatorlarga yoyib, har bir mahsulotning narxi va miqdorini alohida ustunlarga ajrating.",
    """WITH buyurtma AS (
    SELECT 101 AS buyurtma_id, '[
        {"nomi": "Klaviatura", "narx": 350000, "miqdor": 1},
        {"nomi": "Sichqoncha", "narx": 150000, "miqdor": 2}
    ]'::jsonb AS tovarlar
)
SELECT 
    buyurtma_id,
    elem ->> 'nomi'                AS tovar_nomi,
    (elem ->> 'narx')::NUMERIC     AS narx,
    (elem ->> 'miqdor')::INT       AS miqdor,
    ((elem ->> 'narx')::NUMERIC * (elem ->> 'miqdor')::INT) AS summa
FROM buyurtma,
jsonb_array_elements(buyurtma.tovarlar) AS elem;""",
    "`jsonb_array_elements(jsonb_array)` JSON massividagi har bir elementni alohida relyatsion qatorga yoyadi (unnest qiladi). Vergul bilan bog'langan cross join orqali har bir yoyilgan elementdan ustunlar ajratib olinadi.",
    """ buyurtma_id | tovar_nomi |   narx    | miqdor |   summa   
------------+------------+-----------+--------+-----------
        101 | Klaviatura | 350000.00 |      1 | 350000.00
        101 | Sichqoncha | 150000.00 |      2 | 300000.00
(2 rows)"""
)

# 918
add_task(
    918,
    "jsonb_each va jsonb_each_text yordamida obyekt kalit-qiymatlarini yoyish",
    "Dinamik foydalanuvchi atributlari obyektining barcha kalit va qiymatlarini alohida satrlarga ajratib oling.",
    """WITH data AS (
    SELECT '{"rang": "qora", "olcham": "XL", "material": "paxta"}'::jsonb AS xususiyatlar
)
SELECT 
    kalit, 
    qiymat 
FROM data,
jsonb_each_text(data.xususiyatlar) AS qator(kalit, qiymat);""",
    "`jsonb_each_text(jsonb)` JSON obyektini aylanib chiqib, har bir kalit-qiymat juftligini `(key TEXT, value TEXT)` formatidagi relyatsion satrlarga aylantiradi. Bu sxemasiz (schemaless) atributlar ustida agregatsiya va qidiruv o'tkazish imkonini beradi.",
    """  kalit   | qiymat 
----------+--------
 material | paxta
 olcham   | XL
 rang     | qora
(3 rows)"""
)

# 919
add_task(
    919,
    "jsonb_object_keys yordamida barcha kalitlar ro'yxatini olish",
    "JSONB hujjatida qaysi kalitlar mavjudligini ro'yxat qilib oling va kalitlar sonini hisoblang.",
    """WITH data AS (
    SELECT '{"cpu": "M3 Pro", "ram": "36GB", "ssd": "1TB", "gpu": "18 Core"}'::jsonb AS spec
)
SELECT 
    jsonb_object_keys(spec) AS kalit_nomi
FROM data;""",
    "`jsonb_object_keys(jsonb)` ob'ektning eng yuqori darajasidagi (top-level) barcha kalit nomlarini qatorlar to'plami (`SETOF TEXT`) sifatida qaytaradi.",
    """ kalit_nomi 
------------
 cpu
 gpu
 ram
 ssd
(4 rows)"""
)

# 920
add_task(
    920,
    "jsonb_to_recordset yordamida JSON massivini to'liq jadvallashtirish",
    "JSON ko'rinishidagi foydalanuvchilar massivini `jsonb_to_recordset` orqali to'g'ridan-to'g'ri SQL jadvaliga o'giring va tiplarga keltiring.",
    """SELECT *
FROM jsonb_to_recordset('[
    {"id": 1, "ism": "Akmal", "balans": 450000.50},
    {"id": 2, "ism": "Nargiza", "balans": 1200000.00}
]'::jsonb) AS (id INT, ism TEXT, balans NUMERIC);""",
    "`jsonb_to_recordset(jsonb_array) AS (...)` konstruksiyasi JSON massivini bir zumda kuchli tiplangan (strongly typed) relyatsion jadvalga aylantiradi. `AS (id INT, ...)` qismida har bir kalit qaysi SQL turiga o'tishi belgilanadi.",
    """ id |   ism   |   balans   
----+---------+------------
  1 | Akmal   |  450000.50
  2 | Nargiza | 1200000.00
(2 rows)"""
)

# 921
add_task(
    921,
    "GIN (Generalized Inverted Index) indeksi yaratish (Standart jsonb_ops)",
    "Millionlab qatorli `mijoz_anketa` jadvalidagi `malumotlar` JSONB ustuniga `@>`, `?`, `?|` operatorlarini tezlashtiruvchi standart GIN indeksini quring.",
    """-- Standart jsonb_ops GIN indeksi
CREATE INDEX idx_mijoz_anketa_gin 
ON mijoz_anketa USING gin (malumotlar);

-- Indeksdan foydalanuvchi so'rov
EXPLAIN (COSTS OFF)
SELECT * FROM mijoz_anketa
WHERE malumotlar @> '{"status": "VIP", "shahar": "Samarqand"}';""",
    "Standart `GIN` indeksi (`jsonb_ops`) har bir kalit va qiymatni alohida indekslaydi. U `@>`, `?`, `?|`, `?&` operatorlarining barchasini to'liq qo'llab-quvvatlaydi va juda moslashuvchan (general-purpose) hisoblanadi.",
    """                     QUERY PLAN                     
----------------------------------------------------
 Bitmap Heap Scan on mijoz_anketa
   Recheck Cond: (malumotlar @> '{"shahar": "Samarqand", "status": "VIP"}'::jsonb)
   ->  Bitmap Index Scan on idx_mijoz_anketa_gin
(3 rows)"""
)

# 922
add_task(
    922,
    "Tezkor va tejamkor GIN indeksi: jsonb_path_ops",
    "Faqatgina `@>` (containment) operatori bo'yicha maksimal qidiruv tezligi va kichikroq indeks hajmini ta'minlovchi `jsonb_path_ops` indeksini yarating.",
    """-- jsonb_path_ops operatorlar sinfi bilan GIN indeks
CREATE INDEX idx_tovarlar_path_ops 
ON tovarlar USING gin (parametrlar jsonb_path_ops);

-- Indeks qidiruvi
EXPLAIN (COSTS OFF)
SELECT id, nomi FROM tovarlar
WHERE parametrlar @> '{"brend": "Apple"}';""",
    "`jsonb_path_ops` har bir to'liq yo'l (path + value) ning xeshini indekslaydi. Natijada indeks hajmi standart GIN ga nisbatan 2-3 barobar kichikroq bo'ladi va `@>` operatori bo'yicha qidiruv sezilarli darajada tezroq bajariladi (lekin `?` kalit tekshiruvini quvvatlamaydi).",
    """                     QUERY PLAN                     
----------------------------------------------------
 Bitmap Heap Scan on tovarlar
   Recheck Cond: (parametrlar @> '{"brend": "Apple"}'::jsonb)
   ->  Bitmap Index Scan on idx_tovarlar_path_ops
(3 rows)"""
)

# 923
add_task(
    923,
    "JSON ichidagi aniq skalyar maydonga B-Tree indeksi qurish",
    "Faqat `profil->>'telefon'` maydoni bo'yicha qat'iy qidiruv va unikal tartiblash amalga oshirilishi uchun ifodali (Expression) B-Tree indeksini yarating.",
    """-- Aniq bitta maydonga B-Tree indeksi
CREATE UNIQUE INDEX idx_foydalanuvchi_json_telefon 
ON foydalanuvchilar (((profil ->> 'telefon')::TEXT));

-- Indeks orqali to'g'ridan-to'g'ri Index Scan
EXPLAIN (COSTS OFF)
SELECT id, profil FROM foydalanuvchilar
WHERE (profil ->> 'telefon') = '+998901234567';""",
    "Agar JSONB ichidagi ma'lum bir maydon bo'yicha tez-tez `=` yoki `ORDER BY` amallari bajarilsa, butun hujjatga GIN qurish o'rniga aynan o'sha skalyar maydonga `((doc ->> 'maydon'))` B-Tree indeksi qurish xotira va tezlik bo'yicha eng samarali yo'ldir.",
    """                           QUERY PLAN                           
----------------------------------------------------------------
 Index Scan using idx_foydalanuvchi_json_telefon on foydalanuvchilar
   Index Cond: ((profil ->> 'telefon'::text) = '+998901234567'::text)
(2 rows)"""
)

# 924
add_task(
    924,
    "JSONPath: jsonb_path_exists orqali shartli qidiruv (SQL/JSON)",
    "PostgreSQL ning SQL/JSON standarti (`jsonb_path_exists`) yordamida narxi 500 dan katta bo'lgan buyurtmalarni JSONPath ifodasi orqali toping.",
    """SELECT id, buyurtma_data
FROM buyurtmalar
WHERE jsonb_path_exists(
    buyurtma_data, 
    '$.elementlar[*] ? (@.narx > 500)'
);""",
    "`jsonb_path_exists(target, path)` SQL/JSON standarti bo'lib, murakkab filtrlarni JSON ichida bajarish imkonini beradi. `$.elementlar[*] ? (@.narx > 500)` ifodasi massiv ichidagi har bir elementning `narx` kalitini 500 dan kattaligini bevosita tekshiradi.",
    """ id |                         buyurtma_data                          
----+----------------------------------------------------------------
  3 | {"elementlar": [{"nomi": "Monitor", "narx": 1200}, {"nomi": "Kabel", "narx": 20}]}
(1 row)"""
)

# 925
add_task(
    925,
    "JSONPath: jsonb_path_query orqali filtrlangan massiv elementlarini chiqarish",
    "JSONB hujjatidan ma'lum shartga mos keluvchi barcha elementlarni `jsonb_path_query` orqali to'g'ridan-to'g'ri oqim qilib oling.",
    """WITH do`kon AS (
    SELECT '{
        "ombor": [
            {"nomi": "Telefon", "qoldiq": 15},
            {"nomi": "Quloqchin", "qoldiq": 3},
            {"nomi": "G'ilof", "qoldiq": 0}
        ]
    }'::jsonb AS data
)
SELECT jsonb_path_query(
    data, 
    '$.ombor[*] ? (@.qoldiq > 0).nomi'
) AS mavjud_tovarlar
FROM do`kon;""",
    "`jsonb_path_query(target, path)` berilgan yo'lga mos keladigan barcha JSON fragmentlarini alohida qatorlar ko'rinishida qaytaradi. Bu yerda faqat qoldig'i 0 dan katta tovarlarning nomlari ajratib olinmoqda.",
    """ mavjud_tovarlar 
------------------
 "Telefon"
 "Quloqchin"
(2 rows)"""
)

# 926
add_task(
    926,
    "Ko'p tilli (Multilingual/i18n) ma'lumotlarni JSONB da saqlash va qidirish",
    "Mahsulot nomi bir nechta tilda (`uz`, `ru`, `en`) saqlangan jadvaldan foydalanuvchi tanlagan til bo'yicha nomni chiqaruvchi va tanlangan til bo'lmasa standart `uz` ga tushuvchi (fallback) so'rov yozing.",
    """WITH tovarlar_i18n AS (
    SELECT 1 AS id, '{"uz": "Olma", "ru": "Яблоко", "en": "Apple"}'::jsonb AS nomlar
    UNION ALL
    SELECT 2 AS id, '{"uz": "Uzum", "ru": "Виноград"}'::jsonb AS nomlar
)
SELECT 
    id,
    COALESCE(nomlar ->> 'en', nomlar ->> 'uz') AS korsatish_nomi
FROM tovarlar_i18n;""",
    "Ko'p tilli tizimlarda har bir til uchun alohida ustun ochmasdan, bitta `nomlar jsonb` ustunida barcha tillarni saqlash keng tarqalgan zamonaviy pattern hisoblanadi. `COALESCE(nomlar->>'til', nomlar->>'standart_til')` orqali til mavjud bo'lmaganda zaxira tilga qaytish juda oson amalga oshiriladi.",
    """ id | korsatish_nomi 
----+----------------
  1 | Apple
  2 | Uzum
(2 rows)"""
)

# 927
add_task(
    927,
    "JSONB massividagi elementlarni guruhlab agregatsiya qilish",
    "Barcha buyurtmalarning JSON ichidagi mahsulotlarini bitta umumiy ro'yxatga yoyib, har bir mahsulot bo'yicha umumiy sotilgan sonini hisoblang.",
    """SELECT 
    elem ->> 'nomi' AS mahsulot_nomi,
    SUM((elem ->> 'miqdor')::INT) AS jami_sotilgan
FROM buyurtmalar b,
jsonb_array_elements(b.buyurtma_data -> 'elementlar') AS elem
GROUP BY elem ->> 'nomi'
ORDER BY jami_sotilgan DESC;""",
    "Relyatsion bo'lmagan JSONB massivlari `jsonb_array_elements` orqali SQL dunyosiga yoyilgach, an'anaviy `GROUP BY`, `SUM()`, `AVG()` kabi barcha qudratli SQL agregatlari ularga to'liq tatbiq etiladi.",
    """ mahsulot_nomi | jami_sotilgan 
---------------+---------------
 Sichqoncha    |            14
 Klaviatura    |             8
 Monitor       |             3
(3 rows)"""
)

# 928
add_task(
    928,
    "JSONB ichidagi sonlar bo'yicha matematik shartli filtrlash",
    "Mijozning hisob kitoblaridan 1 000 000 dan katta to'lovlarni JSONB ichidan aniqlab, 15% chegirma hisoblovchi so'rov yozing.",
    """WITH tolovlar AS (
    SELECT '{"summa": 1500000, "valyuta": "UZS"}'::jsonb AS tx
    UNION ALL
    SELECT '{"summa": 450000, "valyuta": "UZS"}'::jsonb AS tx
)
SELECT 
    (tx ->> 'summa')::NUMERIC AS asl_summa,
    CASE 
        WHEN (tx ->> 'summa')::NUMERIC >= 1000000 
        THEN ROUND((tx ->> 'summa')::NUMERIC * 0.85, 2)
        ELSE (tx ->> 'summa')::NUMERIC
    END AS chegirmali_summa
FROM tolovlar;""",
    "`(tx ->> 'summa')::NUMERIC` orqali JSON matnli qiymati haqiqiy raqamga aylantiriladi va `CASE` shartli logikasida solishtirish amallari uchun qo'llaniladi.",
    """ asl_summa  | chegirmali_summa 
------------+------------------
 1500000.00 |       1275000.00
  450000.00 |        450000.00
(2 rows)"""
)

# 929
add_task(
    929,
    "E-tijorat dinamik atributlari: Har xil toifadagi tovarlarni bitta jadvalda boshqarish",
    "Kiyimlar (o'lcham, mato), noutbuklar (ram, ssd) va kitoblar (sahifalar, muallif) ning har xil atributlarini bitta `xususiyatlar jsonb` ustunida saqlab, toifa bo'yicha qidirishni ko'rsating.",
    """SELECT id, nomi, kategoriya, xususiyatlar
FROM mahsulotlar
WHERE kategoriya = 'Elektronika' 
  AND (xususiyatlar ->> 'ram')::INT >= 16;""",
    "E-tijoratda har bir yangi toifa uchun alohida jadvallar ochish (EAV antipattern) o'rniga `JSONB` ustuni ideal arxitekturaviy yechimdir. Kerakli paytda kiyim atributlari, kerakli paytda texnika parametrlari bir xil jadvalda erkin saqlanadi.",
    """ id |    nomi     |  kategoriya  |               xususiyatlar                
----+-------------+--------------+-------------------------------------------
  5 | MacBook Air | Elektronika  | {"ram": 16, "ssd": "512GB", "protsessor": "M2"}
(1 row)"""
)

# 930
add_task(
    930,
    "jsonb_pretty yordamida JSON ni chiroyli formatlash (Indentation)",
    "Siqilgan ixcham JSONB hujjatini inson o'qishiga qulay (indentatsiyalangan) ko'rinishga keltirib chiquvchi so'rov yozing.",
    """SELECT jsonb_pretty('{"ism": "Komil", "manzil": {"shahar": "Toshkent", "uy": 12}, "faol": true}'::jsonb) AS chiroyli_json;""",
    "`jsonb_pretty(jsonb)` barcha qavs va ichki obyektlarni qator tashlab, 4 bo'shliqli chiroyli matn shaklida formatlab beradi. Bu audit va konsol tahlillarida juda qo'l keladi.",
    """         chiroyli_json         
-------------------------------
 {                            +
     "ism": "Komil",          +
     "faol": true,            +
     "manzil": {              +
         "uy": 12,            +
         "shahar": "Toshkent" +
     }                        +
 }
(1 row)"""
)

# 931
add_task(
    931,
    "CHECK cheklovi orqali JSONB sxemasini qisman tekshirish (Schema validation)",
    "Jadvaldagi JSONB ustunida `email` kaliti bo'lishi shartligini va `yosh` musbat son bo'lishini jadval yaratish paytida CHECK cheklovi orqali ta'minlang.",
    """CREATE TABLE mijoz_hujjatlari (
    id SERIAL PRIMARY KEY,
    profil JSONB NOT NULL,
    CONSTRAINT chk_json_sxema CHECK (
        profil ? 'email' AND 
        (profil ->> 'email') LIKE '%@%' AND
        ((profil ->> 'yosh')::INT > 0)
    )
);

-- Test kiritish
INSERT INTO mijoz_hujjatlari(profil)
VALUES ('{"email": "sanjar@misol.uz", "yosh": 29}');""",
    "PostgreSQL'da `CHECK` cheklovlari JSONB operatorlari bilan mukammal ishlaydi. Bu orqali NoSQL moslashuvchanligini saqlagan holda kerakli muhim maydonlarning majburiyligi va qiymat diapazonlarini ma'lumotlar bazasi darajasida kafolatlash mumkin.",
    """INSERT 0 1"""
)

# 932
add_task(
    932,
    "Tashqi API javoblarini (Webhook Payloads) saqlash va xatoliklarni tahlil qilish",
    "To'lov shlyuzidan (masalan, Click yoki Payme) kelgan xom webhook JSON javobini saqlab, xatolik bergan (`status <> 'OK'`) to'lovlarni filtrlash.",
    """SELECT 
    id,
    webhook_body ->> 'transaction_id' AS transaktsiya_id,
    webhook_body -> 'error' ->> 'message' AS xato_matni,
    yaratilgan_vaqt
FROM tolov_webhooklar
WHERE webhook_body ->> 'status' = 'ERROR';""",
    "Zamonaviy arxitekturalarda tashqi tizimlar yuboradigan webhook JSON ma'lumotlarini qat'iy jadvallarga bo'lib o'tirmasdan, xom holida JSONB ustuniga yozish eng to'g'ri amaliyotdir. So'ngra barcha nosozliklar bevosita JSON operatorlari orqali tahlil qilinadi.",
    """ id | transaktsiya_id |     xato_matni      |      yaratilgan_vaqt       
----+-----------------+---------------------+----------------------------
 42 | TX-8891024      | Balans yetarli emas | 2024-06-15 16:30:10.124501
(1 row)"""
)

# 933
add_task(
    933,
    "Qatorli ma'lumotlar va JSON massivlarini kesishuvini (Intersection) topish",
    "Foydalanuvchining ko'nikmalari (`skills`) massivi vakansiya talab qilgan ko'nikmalar bilan kesishishini tekshiruvchi so'rov yozing.",
    """WITH foydalanuvchilar AS (
    SELECT 1 AS id, 'Ali' AS ism, '["Java", "Spring", "Docker"]'::jsonb AS skills
    UNION ALL
    SELECT 2 AS id, 'Vali' AS ism, '["Python", "Django", "PostgreSQL"]'::jsonb AS skills
)
SELECT id, ism, skills
FROM foydalanuvchilar
WHERE skills ?| array['PostgreSQL', 'Docker'];""",
    "`?| array['val1', 'val2']` operatori JSONB massivida berilgan qatorlardan kamida bittasi qatnashganligini tekshiradi va tezkor moslikni (matching) aniqlaydi.",
    """ id | ism  |                skills                
----+------+--------------------------------------
  1 | Ali  | ["Java", "Spring", "Docker"]
  2 | Vali | ["Python", "Django", "PostgreSQL"]
(2 rows)"""
)

# 934
add_task(
    934,
    "JSONB massividan dublikat elementlarni olib tashlash",
    "Tarkibida takrorlanuvchi sonlar yoki matnlar bo'lgan JSONB massividan faqat unikal elementlarni qoldiruvchi so'rov yozing.",
    """WITH data AS (
    SELECT '["olma", "anor", "olma", "uzum", "anor"]'::jsonb AS mevalar
)
SELECT jsonb_agg(DISTINCT elem) AS unikal_mevalar
FROM data,
jsonb_array_elements_text(data.mevalar) AS elem;""",
    "`jsonb_array_elements_text` massivni matnli qatorlarga yoyadi, so'ngra `jsonb_agg(DISTINCT elem)` takrorlanuvchi elementlarni filtrlab, yana toza unikal JSONB massiviga jamlaydi.",
    """    unikal_mevalar     
-----------------------
 ["anor", "olma", "uzum"]
(1 row)"""
)

# 935
add_task(
    935,
    "JSONB obyektidagi barcha kalitlar va ularning turlarini aniqlash",
    "JSONB hujjati ichidagi har bir kalitning ma'lumot turini (`string`, `number`, `boolean`, `object`, `array`, `null`) aniqlovchi so'rov yozing.",
    """WITH doc AS (
    SELECT '{
        "nomi": "Kitob",
        "sahifa": 320,
        "mavjud": true,
        "teglar": ["badiiy", "tarixiy"],
        "muallif": {"ism": "Otkir Hoshimov"}
    }'::jsonb AS data
)
SELECT 
    key AS kalit,
    jsonb_typeof(value) AS malumot_turi
FROM doc,
jsonb_each(doc.data);""",
    "`jsonb_typeof(jsonb_val)` funksiyasi berilgan JSON qiymatining aniq JSON turini matn sifatida qaytaradi (`string`, `number`, `boolean`, `null`, `object`, `array`). Bu dinamik ma'lumotlarni tahlil qilishda zaruriy yordamchidir.",
    """  kalit  | malumot_turi 
---------+--------------
 mavjud  | boolean
 muallif | object
 nomi    | string
 sahifa  | number
 teglar  | array
(5 rows)"""
)

# 936
add_task(
    936,
    "JSONB ustunidagi sonlarni jamlash (Agregatsiya)",
    "Barcha filiallarning JSON formatidagi ko'rsatkichlaridan foydalanib umumiy daromadni jamlang.",
    """WITH filiallar AS (
    SELECT '{"shahar": "Toshkent", "moliyaviy": {"daromad": 540000000}}'::jsonb AS hisobot
    UNION ALL
    SELECT '{"shahar": "Samarqand", "moliyaviy": {"daromad": 320000000}}'::jsonb AS hisobot
)
SELECT SUM((hisobot #>> '{moliyaviy, daromad}')::NUMERIC) AS umumiy_daromad
FROM filiallar;""",
    "`#>> '{moliyaviy, daromad}'` yo'li orqali ichki daromad raqami olinadi va `SUM()` yordamida barcha filiallarning daromadlari bitta yig'indiga birlashtiriladi.",
    """ umumiy_daromad 
----------------
   860000000.00
(1 row)"""
)

# 937
add_task(
    937,
    "JSONB massivida qidiruv: Ichki massiv obyektlarining ma'lum bir maydoni bo'yicha filtrlash",
    "Foydalanuvchilar orasidan kamida bitta 'ADMIN' roliga ega bo'lgan foydalanuvchilarni toping (`rollar: [{\"nom\": \"ADMIN\"}]`).",
    """SELECT id, ism, xavfsizlik
FROM foydalanuvchilar
WHERE xavfsizlik @> '{"rollar": [{"nom": "ADMIN"}]}';""",
    "Tarkibida obyektlar bo'lgan massivlar ustida `@>` operatori juda qulay ishlaydi: u massiv elementlaridan kamida bittasi ko'rsatilgan qolipga (pattern) mos kelishini to'liq tekshiradi va GIN indeksi orqali bir zumda natija beradi.",
    """ id |   ism   |               xavfsizlik                
----+---------+-----------------------------------------
  1 | Alisher | {"rollar": [{"nom": "USER"}, {"nom": "ADMIN"}]}
(1 row)"""
)

# 938
add_task(
    938,
    "JSONPath: jsonb_path_query_array orqali faqat mos kelgan elementlardan iborat yangi massiv hosil qilish",
    "Xaridlar ro'yxatidan faqat narxi 100 000 dan oshgan tovarlarni yangi filtratsiyalangan JSON massiv qilib oling.",
    """WITH savat AS (
    SELECT '[
        {"nom": "Non", "narx": 4000},
        {"nom": "Gosh", "narx": 110000},
        {"nom": "Moy", "narx": 125000}
    ]'::jsonb AS xaridlar
)
SELECT jsonb_path_query_array(
    xaridlar, 
    '$[*] ? (@.narx >= 100000)'
) AS qimmat_xaridlar
FROM savat;""",
    "`jsonb_path_query_array(target, path)` filtrlash shartiga mos kelgan barcha elementlarni yangi yagona JSONB massiviga joylab qaytaradi. Bu massivni yoyib, qayta yig'ish (unnest -> agg) bosqichlarini bitta operatsiyaga tushiradi.",
    """                     qimmat_xaridlar                      
----------------------------------------------------------
 [{"nom": "Gosh", "narx": 110000}, {"nom": "Moy", "narx": 125000}]
(1 row)"""
)

# 939
add_task(
    939,
    "Bir nechta JSON ustunlarini bitta umumiy obyektga birlashtirish",
    "Foydalanuvchining `asosiy_profil`, `aloqa_malumotlari` va `tizim_sozlamalari` nomli alohida JSONB ustunlarini bitta to'liq JSON hujjatiga birlashtirib ko'rsating.",
    """SELECT 
    id,
    asosiy_profil || aloqa_malumotlari || tizim_sozlamalari AS toliq_profil
FROM foydalanuvchi_baza
WHERE id = 10;""",
    "`||` operatori zanjirsimon qo'llanilganda (`col1 || col2 || col3`) barcha jadvallar ustunidagi atributlar yagona keng qamrovli JSON ob'ektiga aylanadi.",
    """ id |                                               toliq_profil                                                
----+-----------------------------------------------------------------------------------------------------------
 10 | {"ism": "Temur", "til": "uz", "email": "temur@misol.uz", "shahar": "Toshkent", "qorongu_mavzu": true}
(1 row)"""
)

# 940
add_task(
    940,
    "JSONB da saralash: Ichki maydon bo'yicha tartiblash (ORDER BY JSON value)",
    "Xodimlarni ularning JSON profilidagi ish boshlagan sanasi (`profil ->> 'ishga_kirgan_sana'`) bo'yicha kamayish tartibida saralang.",
    """SELECT 
    id, 
    profil ->> 'ism' AS ism, 
    (profil ->> 'ishga_kirgan_sana')::DATE AS sana
FROM xodim_profillari
ORDER BY (profil ->> 'ishga_kirgan_sana')::DATE DESC;""",
    "JSONB qiymatlarini saralashda ularni to'g'ri relyatsion turga (`::DATE`, `::NUMERIC`) keltirish lozim, aks holda matnli saralash (lexicographical sorting) amalga oshib, natija xato chiqishi mumkin.",
    """ id |   ism   |    sana    
----+---------+------------
  4 | Jahongir| 2024-02-01
  2 | Malika  | 2023-11-15
  1 | Sardor  | 2022-05-10
(3 rows)"""
)

# 941
add_task(
    941,
    "JSON kalitlari nomini o'zgartirish (Rename key in JSONB)",
    "JSONB obyektidagi eski kalit nomini (`tel`) yangi nomga (`telefon`) o'zgartiruvchi va eski kalitni o'chiruvchi so'rov yozing.",
    """WITH data AS (
    SELECT '{"ism": "Farrux", "tel": "+998901234567"}'::jsonb AS doc
)
SELECT 
    (doc - 'tel') || jsonb_build_object('telefon', doc ->> 'tel') AS yangilangan_doc
FROM data;""",
    "JSONB da kalit nomini almashtirish uchun avval eski kalit `doc - 'eski_nom'` orqali o'chiriladi, so'ngra yangi kalit bilan `|| jsonb_build_object('yangi_nom', qiymat)` orqali birlashtiriladi.",
    """                yangilangan_doc                 
-----------------------------------------------
 {"ism": "Farrux", "telefon": "+998901234567"}
(1 row)"""
)

# 942
add_task(
    942,
    "Bo'sh massivlar va bo'sh obyektlarni aniqlash",
    "JSON ustuni bo'sh massiv (`[]`), bo'sh obyekt (`{}`) yoki NULL bo'lgan yozuvlarni topuvchi so'rov yozing.",
    """SELECT id, metadata
FROM tizim_loglari
WHERE metadata IS NULL 
   OR metadata = '{}'::jsonb 
   OR metadata = '[]'::jsonb 
   OR jsonb_array_length(CASE WHEN jsonb_typeof(metadata) = 'array' THEN metadata ELSE '[]'::jsonb END) = 0;""",
    "`metadata = '{}'::jsonb` to'g'ridan-to'g'ri bo'sh JSONB obyektini tekshiradi. `jsonb_array_length()` esa massivdagi elementlar sonini beradi (faqat massiv turlariga qo'llash sharti bilan).",
    """ id | metadata 
----+----------
  7 | {}
 12 | []
(2 rows)"""
)

# 943
add_task(
    943,
    "JSON massivini vergul bilan ajratilgan oddiy matnga (CSV/String) aylantirish",
    "Foydalanuvchining ko'nikmalari JSON massividan bitta chiroyli vergulli matn (`Java, Kotlin, Android`) hosil qiling.",
    """WITH user_data AS (
    SELECT '{"skills": ["Java", "Kotlin", "Android", "Git"]}'::jsonb AS profil
)
SELECT string_agg(skill, ', ') AS ko'nikmalar_matni
FROM user_data,
jsonb_array_elements_text(user_data.profil -> 'skills') AS skill;""",
    "`jsonb_array_elements_text` orqali matnga aylantirilgan qatorlar relyatsion `string_agg(skill, ', ')` agregati orqali yagona matnga ulanadi.",
    """     ko'nikmalar_matni     
---------------------------
 Java, Kotlin, Android, Git
(1 row)"""
)

# 944
add_task(
    944,
    "JSON ma'lumotlarini to'g'ridan-to'g'ri UPDATE buyrug'ida qisman yangilash",
    "Mahsulotning narxi oshganda, uning `xususiyatlar` JSONB ustunidagi `narx_tarixi` massiviga yangi sana va narxni append qilib boruvchi UPDATE so'rovi yozing.",
    """UPDATE tovarlar
SET xususiyatlar = jsonb_set(
    xususiyatlar,
    '{narx_tarixi}',
    COALESCE(xususiyatlar -> 'narx_tarixi', '[]'::jsonb) || jsonb_build_array(
        jsonb_build_object('sana', CURRENT_DATE, 'narx', 450000)
    )
)
WHERE id = 5;

SELECT id, xususiyatlar -> 'narx_tarixi' AS tarix FROM tovarlar WHERE id = 5;""",
    "Ushbu UPDATE amali mavjud massivga yangi obyektni `||` orqali qo'shadi va `jsonb_set` yordamida o'rniga yozadi. Bu audit va narx o'zgarishi tarixini alohida jadvallarsiz to'g'ridan-to'g'ri hujjat ichida saqlash imkonini beradi.",
    """ id |                                  tarix                                   
----+--------------------------------------------------------------------------
  5 | [{"narx": 420000, "sana": "2024-01-10"}, {"narx": 450000, "sana": "2024-06-15"}]
(1 row)"""
)

# 945
add_task(
    945,
    "JSONB dagi kalitlarni tekshiruvchi funksiya yaratish",
    "Berilgan JSONB hujjatida talab qilingan barcha kalitlar bor-yo'qligini tekshirib `BOOLEAN` natija beruvchi maxsus PL/pgSQL funksiyasini yozing.",
    """CREATE OR REPLACE FUNCTION tekshir_jsonb_kalitlar(
    doc JSONB, 
    VARIADIC talab_qilingan_kalitlar TEXT[]
)
RETURNS BOOLEAN
LANGUAGE SQL
IMMUTABLE
AS $$
    SELECT doc ?& talab_qilingan_kalitlar;
$$;

SELECT 
    tekshir_jsonb_kalitlar('{"id": 1, "ism": "Ali", "email": "ali@misol.uz"}'::jsonb, 'id', 'ism') AS natija_1,
    tekshir_jsonb_kalitlar('{"id": 1, "ism": "Ali"}'::jsonb, 'id', 'email') AS natija_2;""",
    "`VARIADIC` matn massivi qabul qilinib, to'g'ridan-to'g'ri `doc ?& massiv` operatoriga uzatiladi. Funksiya barcha talab qilingan kalitlar mavjudligini bir zumda tekshirib beradi.",
    """ natija_1 | natija_2 
----------+----------
 t        | f
(1 row)"""
)

# 946
add_task(
    946,
    "JSONPath: jsonb_path_match yordamida mantiqiy predikatni baholash",
    "Foydalanuvchining hisobi faolligini va yoshi 18 dan kattaligini SQL/JSON predikati orqali tekshiring.",
    """WITH profillar AS (
    SELECT '{"yosh": 25, "faol": true}'::jsonb AS data
    UNION ALL
    SELECT '{"yosh": 16, "faol": true}'::jsonb AS data
)
SELECT 
    data,
    jsonb_path_match(data, '$.yosh >= 18 && $.faol == true') AS ruxsat
FROM profillar;""",
    "`jsonb_path_match(target, path)` SQL/JSON standart mantiqiy ifodasini baholab, `TRUE`, `FALSE` yoki `NULL` natija beradi (`&&` = AND, `||` = OR, `==` = tenglik).",
    """               data               | ruxsat 
----------------------------------+--------
 {"faol": true, "yosh": 25}       | t
 {"faol": true, "yosh": 16}       | f
(2 rows)"""
)

# 947
add_task(
    947,
    "JSONB hujjatlarini chuqur rekursiv birlashtirish (Deep Merge)",
    "PostgreSQL ning standart `||` operatori sayoz (faqat 1-darajali) birlashtirgani sababli, ichki obyektlarni ham buzmasdan birlashtiruvchi rekursiv deep-merge funksiyasini yozing.",
    """CREATE OR REPLACE FUNCTION jsonb_deep_merge(asos JSONB, yangi JSONB)
RETURNS JSONB
LANGUAGE SQL
IMMUTABLE
AS $$
    SELECT 
        jsonb_object_agg(
            kalit,
            CASE 
                WHEN asos ? kalit AND yangi ? kalit AND 
                     jsonb_typeof(asos -> kalit) = 'object' AND 
                     jsonb_typeof(yangi -> kalit) = 'object'
                THEN jsonb_deep_merge(asos -> kalit, yangi -> kalit)
                WHEN yangi ? kalit THEN yangi -> kalit
                ELSE asos -> kalit
            END
        )
    FROM (
        SELECT jsonb_object_keys(asos) AS kalit
        UNION
        SELECT jsonb_object_keys(yangi) AS kalit
    ) kalitlar;
$$;

SELECT jsonb_deep_merge(
    '{"profil": {"ism": "Ali", "til": "uz"}, "status": "FAOL"}'::jsonb,
    '{"profil": {"shahar": "Toshkent"}}'::jsonb
) AS chuqur_birlashgan;""",
    "Standart `||` butun `profil` obyektini yangisiga almashtirib yuborgan bo'lardi. Rekursiv `jsonb_deep_merge` funksiyasi ichki obyektlarni ham o'zaro birlashtirib, `ism` va `til` yo'qolmasdan `shahar` qo'shilishini kafolatlaydi.",
    """                               chuqur_birlashgan                               
-------------------------------------------------------------------------------
 {"status": "FAOL", "profil": {"ism": "Ali", "til": "uz", "shahar": "Toshkent"}}
(1 row)"""
)

# 948
add_task(
    948,
    "Hujjatlar bazasi (NoSQL Document Store) patterni: Yagona jadvalda to'liq NoSQL tizimi",
    "PostgreSQL da MongoDB kabi ixtiyoriy tuzilishdagi hujjatlarni saqlaydigan, avtomatik ID, yaratilgan vaqt va GIN indeksi bilan to'liq jihozlangan hujjatlar jadvalini quring.",
    """CREATE TABLE nosql_hujjatlar (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    kolleksiya VARCHAR(50) NOT NULL,
    hujjat JSONB NOT NULL,
    yaratilgan_vaqt TIMESTAMPTZ DEFAULT NOW()
);

-- GIN indeksi
CREATE INDEX idx_nosql_hujjatlar_gin ON nosql_hujjatlar USING gin (hujjat);

-- Ma'lumot kiritish
INSERT INTO nosql_hujjatlar (kolleksiya, hujjat)
VALUES ('orders', '{"customer": "Akbar", "total": 850000, "items_count": 3}');

-- Qidiruv
SELECT id, kolleksiya, hujjat ->> 'customer' AS mijoz 
FROM nosql_hujjatlar 
WHERE kolleksiya = 'orders' AND hujjat @> '{"total": 850000}';""",
    "PostgreSQL ko'plab loyihalarda MongoDB yoki CouchDB o'rnini to'liq bosa oladi: ACID kafolatlari, JSONB binar saqlash va GIN indekslari bilan qurollangan holda yuqori tezlikdagi NoSQL Document Store sifatida xizmat qiladi.",
    """                  id                  | kolleksiya | mijoz 
--------------------------------------+------------+-------
 4f3e2b1a-8c9d-4e5f-0a1b-2c3d4e5f6a7b | orders     | Akbar
(1 row)"""
)

# 949
add_task(
    949,
    "Fayllar metama'lumoti va EXIF ma'lumotlarini JSONB da tahlil qilish",
    "Yuklangan rasmlarning EXIF ma'lumotlaridan (kamera modeli, ISO, ekspozitsiya) ISO sezgirligi 800 dan yuqori bo'lgan rasmlarni filtrlovchi so'rov yozing.",
    """WITH media AS (
    SELECT 1 AS rasm_id, '{"kamera": "Sony A7IV", "exif": {"iso": 1600, "f_stop": 2.8}}'::jsonb AS meta
    UNION ALL
    SELECT 2 AS rasm_id, '{"kamera": "Canon R6", "exif": {"iso": 400, "f_stop": 4.0}}'::jsonb AS meta
)
SELECT 
    rasm_id,
    meta ->> 'kamera' AS kamera_modeli,
    (meta #>> '{exif, iso}')::INT AS iso_qiymati
FROM media
WHERE (meta #>> '{exif, iso}')::INT >= 800;""",
    "Media fayllarning EXIF va texnik metama'lumotlari juda xilma-xil bo'ladi. JSONB ularni hech qanday cheklovlarsiz qabul qiladi va ichki parametrlar bo'yicha tezkor statistik tahlil o'tkazish imkoniyatini yaratadi.",
    """ rasm_id | kamera_modeli | iso_qiymati 
---------+---------------+-------------
       1 | Sony A7IV     |        1600
(1 row)"""
)

# 950
add_task(
    950,
    "Katta hajmdagi JSONB ustunini siqish va xotira tahlili (pg_column_size)",
    "JSON va JSONB ma'lumot turlarining diskdagi xotira hajmini `pg_column_size` orqali o'lchab, TOAST mexanizmining ta'sirini ko'rsatuvchi tahlil so'rovini yozing.",
    """WITH namuna AS (
    SELECT 
        '{"id": 101, "ism": "Shavkat", "status": "FAOL", "ball": 98.5}' AS xom_matn
)
SELECT 
    pg_column_size(xom_matn::text)  AS text_bayt_hajmi,
    pg_column_size(xom_matn::json)  AS json_bayt_hajmi,
    pg_column_size(xom_matn::jsonb) AS jsonb_bayt_hajmi;""",
    "`pg_column_size()` ustun qiymatining xotiradagi haqiqiy hajmini baytlarda ko'rsatadi. `JSONB` formatida kalitlar va yo'llar binar ko'rinishda sarlavha (header) bilan saqlanganligi sababli, kichik hujjatlarda u `text` va `json` ga qaraganda bir oz ko'proq bayt band qilishi mumkin, biroq qidiruv vaqtida parse xarajatlari nolga teng bo'ladi.",
    """ text_bayt_hajmi | json_bayt_hajmi | jsonb_bayt_hajmi 
-----------------+-----------------+------------------
              61 |              61 |               74
(1 row)"""
)

if __name__ == "__main__":
    save_file("sql_19_json_va_zamonaviy_malumotlar_bilan_ishlash.md", tasks)
