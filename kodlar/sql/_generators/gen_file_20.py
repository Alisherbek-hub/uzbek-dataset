# -*- coding: utf-8 -*-
"""
Generator for File 20: sql_20_amaliy_korporativ_baza_va_ai_vector_db.md
Tasks 951 - 1000
Mavzu: Amaliy korporativ baza arxitekturasi, Partitioning va AI Vector DB (pgvector, HNSW, IVFFlat, RAG)
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

def add_task(num, title, condition, sql, explanation, output):
    tasks.append(format_task(num, title, condition, sql, explanation, output))

# 951
add_task(
    951,
    "Bank hisob-kitob tizimi: Ikki yoqlama yozuv (Double-Entry Bookkeeping) arxitekturasi",
    "Bank to'lov tizimida har qanday moliyaviy o'tkazma uchun Debet va Kredit balansi doimo teng (Zero-Sum) bo'lishini kafolatlovchi ikki yoqlama yozuv arxitekturasini yarating va mablag' o'tkazishni bajaring.",
    """-- 1. Bosh reja va hisoblar
CREATE TABLE bank_hisoblari_core (
    id SERIAL PRIMARY KEY,
    hisob_raqam VARCHAR(20) UNIQUE NOT NULL,
    nomi VARCHAR(100) NOT NULL,
    turi VARCHAR(20) NOT NULL -- 'AKTIV', 'PASSIV'
);

CREATE TABLE jurnal_provodkalar (
    id BIGSERIAL PRIMARY KEY,
    tranzaksiya_id UUID NOT NULL,
    debet_hisob_id INT REFERENCES bank_hisoblari_core(id),
    kredit_hisob_id INT REFERENCES bank_hisoblari_core(id),
    summa NUMERIC(18,2) NOT NULL CHECK (summa > 0),
    valyuta VARCHAR(3) DEFAULT 'UZS',
    sana TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Ikki yoqlama o'tkazma
INSERT INTO jurnal_provodkalar(tranzaksiya_id, debet_hisob_id, kredit_hisob_id, summa)
VALUES ('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d', 101, 202, 1500000.00);

-- 3. Balans tengligini tekshirish
SELECT 
    tranzaksiya_id,
    SUM(summa) AS umumiy_aylanma,
    COUNT(*) AS yozuvlar_soni
FROM jurnal_provodkalar
WHERE tranzaksiya_id = 'a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d'
GROUP BY tranzaksiya_id;""",
    "Professional bank tizimlarida balanslar hech qachon shunchaki `balans = balans + x` qilib yangilanmaydi. Buxgalteriya ikki yoqlama yozuv tamoyiliga (Double-Entry Bookkeeping) ko'ra, har bir pul oqimi qaysidir hisobning Debetiga va boshqa hisobning Kreditiga aynan teng miqdorda yoziladi. Bu tizimda pul 'yo'qdan bor bo'lishi' yoki 'izsiz g'oyib bo'lishi'ning oldini oladi.",
    """            tranzaksiya_id            | umumiy_aylanma | yozuvlar_soni 
--------------------------------------+----------------+---------------
 a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d |     1500000.00 |             1
(1 row)"""
)

# 952
add_task(
    952,
    "E-tijorat arxitekturasi: Buyurtma, inventar rezervatsiyasi va holatlar mashinasi (State Machine)",
    "E-tijorat platformasida buyurtma qabul qilinganda ombordagi tovarlarni 'REZERV_QILINGAN' holatiga o'tkazuvchi va buyurtma holatini yangilovchi tranzaksiyani yozing.",
    """BEGIN;

-- 1. Buyurtma yaratish
INSERT INTO buyurtmalar_ecom (id, mijoz_id, holat, umumiy_summa)
VALUES (5001, 42, 'KUTILMOQDA', 3200000.00);

-- 2. Ombordan tovarlarni qulflab rezerv qilish
UPDATE ombor_inventar
SET mavjud_soni = mavjud_soni - 2,
    rezerv_soni = rezerv_soni + 2
WHERE mahsulot_id = 88 AND mavjud_soni >= 2;

-- 3. Buyurtma tarkibini kiritish
INSERT INTO buyurtma_elementlari (buyurtma_id, mahsulot_id, miqdor, narx)
VALUES (5001, 88, 2, 1600000.00);

-- 4. Holatni o'zgartirish
UPDATE buyurtmalar_ecom
SET holat = 'REZERV_QILINDI'
WHERE id = 5001;

COMMIT;

SELECT id, holat, umumiy_summa FROM buyurtmalar_ecom WHERE id = 5001;""",
    "E-tijorat tizimlarida eng katta xavf over-selling (mavjud bo'lmagan tovarni sotib yuborish) hisoblanadi. Buyurtma yaratilishi bilanoq `mavjud_soni` kamaytirilib `rezerv_soni` oshiriladi. Agar to'lov 15 daqiqada amalga oshmasa cron worker rezervni qaytaradi.",
    """  id  |     holat      | umumiy_summa 
------+----------------+--------------
 5001 | REZERV_QILINDI |   3200000.00
(1 row)"""
)

# 953
add_task(
    953,
    "Ko'p ijarachili tizim (Multi-Tenant): Row-Level Security (RLS) bilan ma'lumotlarni ajratish",
    "Barcha mijozlar (kompaniyalar) ma'lumotlari bitta jadvalda saqlanganda, har bir mijoz faqat o'ziga tegishli (`tenant_id`) qatorlarni ko'ra olishi uchun RLS siyosatini (Policy) joriy eting.",
    """-- 1. Jadval va RLS ni yoqish
CREATE TABLE korxona_hujjatlari (
    id SERIAL PRIMARY KEY,
    tenant_id INT NOT NULL,
    hujjat_nomi VARCHAR(100),
    summa NUMERIC(12,2)
);

ALTER TABLE korxona_hujjatlari ENABLE ROW LEVEL SECURITY;

-- 2. RLS xavfsizlik siyosatini yaratish
CREATE POLICY tenant_ajratish_siyosati ON korxona_hujjatlari
    AS RESTRICTIVE
    USING (tenant_id = NULLIF(current_setting('app.joriy_tenant_id', true), '')::INT);

-- 3. Ijarachi (Tenant) sessiyasini sozlash va o'qish
SET app.joriy_tenant_id = '105';

SELECT * FROM korxona_hujjatlari;""",
    "Row-Level Security (RLS) ma'lumotlar bazasi yadrosi darajasida filtrlashni kafolatlaydi. Backend ilovasi `app.joriy_tenant_id` sessiya o'zgaruvchisini o'rnatishi bilanoq, har qanday `SELECT * FROM jadval` so'rovi avtomatik tarzda `WHERE tenant_id = 105` sharti bilan filtrlanadi. Hech bir ijarachi boshqasining ma'lumotini ko'ra olmaydi.",
    """ id | tenant_id |      hujjat_nomi      |   summa   
----+-----------+-----------------------+-----------
 14 |       105 | Hisob-faktura #882    | 450000.00
 15 |       105 | Akt topshirish #12    | 120000.00
(2 rows)"""
)

# 954
add_task(
    954,
    "RANGE bo'yicha jadvallarni bo'lish (Declarative Partitioning: PARTITION BY RANGE)",
    "Katta hajmdagi to'lovlar jadvalini sanalar bo'yicha (har bir yil uchun alohida) qismlarga bo'ling va bolalar jadvallarini (partitions) oching.",
    """-- Asosiy bo'lingan master jadval
CREATE TABLE tolovlar_partitioned (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    mijoz_id INT NOT NULL,
    summa NUMERIC(15,2) NOT NULL,
    tolov_vaqti TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (id, tolov_vaqti)
) PARTITION BY RANGE (tolov_vaqti);

-- 2023-yil qismi
CREATE TABLE tolovlar_y2023 PARTITION OF tolovlar_partitioned
    FOR VALUES FROM ('2023-01-01 00:00:00+00') TO ('2024-01-01 00:00:00+00');

-- 2024-yil qismi
CREATE TABLE tolovlar_y2024 PARTITION OF tolovlar_partitioned
    FOR VALUES FROM ('2024-01-01 00:00:00+00') TO ('2025-01-01 00:00:00+00');

-- Standart zaxira qism (Default)
CREATE TABLE tolovlar_default PARTITION OF tolovlar_partitioned DEFAULT;

-- Ma'lumot kiritish (avtomatik mos qismga tushadi)
INSERT INTO tolovlar_partitioned(mijoz_id, summa, tolov_vaqti)
VALUES (12, 500000, '2024-05-15 11:20:00+00');

SELECT tableoid::regclass AS qism_jadval, id, summa, tolov_vaqti 
FROM tolovlar_partitioned;""",
    "`PARTITION BY RANGE` vaqtga bog'liq (time-series) yirik jadvallarni qismlarga bo'lishning eng samarali usulidir. Birlamchi kalit tarkibiga bo'linish kaliti (`tolov_vaqti`) kiritilishi shart. `tableoid::regclass` yozuv aynan qaysi fizik qismga (`tolovlar_y2024`) tushganini ko'rsatadi.",
    """   qism_jadval   | id |   summa   |      tolov_vaqti       
-----------------+----+-----------+------------------------
 tolovlar_y2024  |  1 | 500000.00 | 2024-05-15 11:20:00+00
(1 row)"""
)

# 955
add_task(
    955,
    "Partition Pruning: Bo'lingan jadvallarda so'rov rejasini optimallashtirish",
    "PostgreSQL optimallashtiruvchisi so'rov shartiga qarab keraksiz qismlarni butunlay chetlab o'tishini (`Partition Pruning`) `EXPLAIN` orqali isbotlang.",
    """EXPLAIN (COSTS OFF)
SELECT * FROM tolovlar_partitioned
WHERE tolov_vaqti >= '2024-06-01' AND tolov_vaqti < '2024-07-01';""",
    "Partition Pruning mexanizmi tufayli PostgreSQL so'rovdagi `WHERE` shartini tahlil qilib, 2023-yilgi yoki boshqa barcha o'nlab jadvallarni skanerlashdan olib tashlaydi va faqat bitta kerakli qismni (`tolovlar_y2024`) o'qiydi. Bu terabaytlab jadvallarda so'rov tezligini 100 barobargacha oshiradi.",
    """                QUERY PLAN                
------------------------------------------
 Seq Scan on tolovlar_y2024 tolovlar_partitioned
   Filter: ((tolov_vaqti >= '2024-06-01'::timestamptz) AND (tolov_vaqti < '2024-07-01'::timestamptz))
(2 rows)"""
)

# 956
add_task(
    956,
    "LIST bo'yicha jadvallarni bo'lish (PARTITION BY LIST)",
    "Hududlar bo'yicha sotuvlarni 3 ta alohida viloyatlar klasteriga bo'luvchi `PARTITION BY LIST` jadvalini yarating.",
    """CREATE TABLE filial_savdolari (
    id SERIAL,
    hudud VARCHAR(30) NOT NULL,
    tushum NUMERIC(15,2),
    PRIMARY KEY (id, hudud)
) PARTITION BY LIST (hudud);

-- Toshkent va viloyati qismi
CREATE TABLE savdolar_poytaxt PARTITION OF filial_savdolari
    FOR VALUES IN ('Toshkent shahri', 'Toshkent viloyati');

-- Vodiy qismi
CREATE TABLE savdolar_vodiy PARTITION OF filial_savdolari
    FOR VALUES IN ('Andijon', 'Namangan', 'Farg''ona');

-- Voha qismi
CREATE TABLE savdolar_voha PARTITION OF filial_savdolari
    FOR VALUES IN ('Samarqand', 'Buxoro', 'Qashqadaryo');

INSERT INTO filial_savdolari(hudud, tushum) VALUES ('Farg''ona', 45000000);

SELECT tableoid::regclass AS joylashgan_jadval, hudud, tushum FROM filial_savdolari;""",
    "`PARTITION BY LIST` diskret qiymatlar (masalan davlatlar, viloyatlar, valyutalar, biznes statuslar) bo'yicha jadvallarni ajratishda ishlatiladi. Farg'ona qiymati kiritilganda server qatorni avtomatik `savdolar_vodiy` jadvaliga joylashtiradi.",
    """ joylashgan_jadval |  hudud   |   tushum    
------------------+----------+-------------
 savdolar_vodiy   | Farg'ona | 45000000.00
(1 row)"""
)

# 957
add_task(
    957,
    "HASH bo'yicha jadvallarni bo'lish (PARTITION BY HASH)",
    "Foydalanuvchilarning yuklamasini 4 ta teng fizik qismga (shards) taqsimlovchi `PARTITION BY HASH` sxemasini tuzing.",
    """CREATE TABLE foydalanuvchilar_hash (
    user_id UUID NOT NULL,
    login VARCHAR(50) NOT NULL,
    PRIMARY KEY (user_id)
) PARTITION BY HASH (user_id);

CREATE TABLE user_part_0 PARTITION OF foydalanuvchilar_hash FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE user_part_1 PARTITION OF foydalanuvchilar_hash FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE user_part_2 PARTITION OF foydalanuvchilar_hash FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE user_part_3 PARTITION OF foydalanuvchilar_hash FOR VALUES WITH (MODULUS 4, REMAINDER 3);

INSERT INTO foydalanuvchilar_hash(user_id, login) 
VALUES (gen_random_uuid(), 'alisher_01');

SELECT tableoid::regclass AS hash_qism, login FROM foydalanuvchilar_hash;""",
    "`PARTITION BY HASH` kiritilgan kalitning (masalan UUID yoki ID) ichki xesh-kodini hisoblab, qatorlarni `MODULUS N, REMAINDER M` formulasi asosida barcha qismlarga mutlaqo bir tekis taqsimlaydi. Bu I/O yuklamani bir nechta disk drayverlariga teng yoyish uchun juda mos keladi.",
    """  hash_qism  |    login    
-------------+-------------
 user_part_2 | alisher_01
(1 row)"""
)

# 958
add_task(
    958,
    "Tizim to'xtamasdan yangi qismni ulash (ATTACH PARTITION)",
    "Alohida yaratilgan mustaqil jadvalni mavjud bo'lingan master jadvalga `ATTACH PARTITION` buyrug'i orqali uzluksiz integratsiya qiling.",
    """-- 1. Mustaqil yangi jadval yaratish va ma'lumot yuklash
CREATE TABLE tolovlar_y2025 (LIKE tolovlar_partitioned INCLUDING ALL);

-- CHECK cheklovi tekshiruv vaqtini (lock) qisqartiradi
ALTER TABLE tolovlar_y2025 ADD CONSTRAINT chk_2025 
    CHECK (tolov_vaqti >= '2025-01-01 00:00:00+00' AND tolov_vaqti < '2026-01-01 00:00:00+00');

-- 2. Master jadvalga ulash
ALTER TABLE tolovlar_partitioned ATTACH PARTITION tolovlar_y2025
    FOR VALUES FROM ('2025-01-01 00:00:00+00') TO ('2026-01-01 00:00:00+00');""",
    "`ATTACH PARTITION` katta hajmdagi yangi ma'lumotlarni alohida tayyorlab, master jadvalga bir zumda (millisoniyada) ulash imkonini beradi. Oldindan `CHECK` qo'yilishi PostgreSQL butun jadvalni qulflab (Exclusive lock) tekshirib chiqishining oldini oladi.",
    """ALTER TABLE"""
)

# 959
add_task(
    959,
    "Eski ma'lumotlar qismini jonsiz ajratish (DETACH PARTITION CONCURRENTLY)",
    "PostgreSQL 14+ da tizim faoliyatini va o'qish/yozish so'rovlarini to'xtatmagan holda, eskirgan 2023-yilgi arxiv qismini master jadvaldan xavfsiz ajratib oling.",
    """ALTER TABLE tolovlar_partitioned 
    DETACH PARTITION tolovlar_y2023 CONCURRENTLY;""",
    "`DETACH PARTITION CONCURRENTLY` eski arxiv qismlarni master jadvaldan ajratishda qulflanish (locking) yuz bermasligini ta'minlaydi. Ajratilgan jadval o'chirilmaydi, balki mustaqil oddiy jadvalga aylanadi va uni bemalol siqish yoki 'cold storage'ga ko'chirish mumkin.",
    """ALTER TABLE"""
)

# 960
add_task(
    960,
    "AI Vector Database: pgvector kengaytmasini o'rnatish va Vektor turi",
    "PostgreSQL da zamonaviy sun'iy intellekt (AI) modellarining embedding vektorlarini saqlash uchun `pgvector` kengaytmasini yoqing va 1536 o'lchovli (OpenAI text-embedding-3) jadval yarating.",
    """-- 1. Kengaytmani yoqish
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Hujjatlar va vektorlar jadvali
CREATE TABLE ai_hujjatlar_vektor (
    id SERIAL PRIMARY KEY,
    hujjat_matni TEXT NOT NULL,
    kategoriya VARCHAR(50),
    embedding vector(1536), -- 1536 o'lchamli suzuvchi nuqtali sonlar vektori
    yaratilgan_vaqt TIMESTAMPTZ DEFAULT NOW()
);

-- Kengaytma versiyasini tekshirish
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';""",
    "`pgvector` — bu PostgreSQL ni eng ilg'or AI Vektorli Ma'lumotlar Bazalaridan biriga (Pinecone, Weaviate kabi) aylantiruvchi rasmiy kengaytmadir. `vector(1536)` turi LLM (Large Language Models) generatsiya qilgan sonli vektorlarni binar ixcham formatda saqlaydi.",
    """ extname | extversion 
---------+------------
 vector  | 0.7.0
(1 row)"""
)

# 961
add_task(
    961,
    "Kosinus masofasi (<=>) orqali semantik o'xshashlikni qidirish (Cosine Distance)",
    "Qidiruv so'rovi vektori berilganda unga eng yaqin (semantik o'xshash) bo'lgan 3 ta hujjatni `<=>` kosinus masofasi operatori orqali toping.",
    """-- Namuna: 3 o'lchamli vektorlar bilan semantik qidiruv
WITH namuna_baza AS (
    SELECT 1 AS id, 'PostgreSQL ma''lumotlar bazasi' AS matn, '[0.95, 0.12, 0.05]'::vector(3) AS v
    UNION ALL
    SELECT 2 AS id, 'MySQL relyatsion tizimi' AS matn, '[0.91, 0.15, 0.08]'::vector(3) AS v
    UNION ALL
    SELECT 3 AS id, 'Toshkentda ob-havo bugun quyoshli' AS matn, '[0.05, 0.85, 0.90]'::vector(3) AS v
)
SELECT 
    id, 
    matn, 
    ROUND((v <=> '[0.93, 0.10, 0.04]'::vector(3))::numeric, 4) AS kosinus_masofa
FROM namuna_baza
ORDER BY v <=> '[0.93, 0.10, 0.04]'::vector(3)
LIMIT 2;""",
    "`<=>` operatori ikkita vektor o'rtasidagi Kosinus masofasini (Cosine Distance = 1 - Cosine Similarity) hisoblaydi. Qiymat 0 ga qancha yaqin bo'lsa, ikki matnning semantik ma'nosi shunchalik bir-biriga o'xshash hisoblanadi. Bazalar haqidagi matnlar ob-havoga qaraganda eng kichik masofaga ega bo'ladi.",
    """ id |             matn             | kosinus_masofa 
----+------------------------------+----------------
  1 | PostgreSQL ma'lumotlar bazasi|         0.0004
  2 | MySQL relyatsion tizimi      |         0.0021
(2 rows)"""
)

# 962
add_task(
    962,
    "Evklid masofasi (<->) va Ichki ko'paytma (<#>) masofa operatorlari",
    "L2 (Evklid) masofasi `<->` va manfiy ichki ko'paytma (Negative Inner Product) `<#>` operatorlari yordamida vektorlar yaqinligini hisoblang.",
    """SELECT 
    ('[1, 2, 3]'::vector(3) <-> '[4, 5, 6]'::vector(3)) AS evklid_masofa,
    ('[1, 2, 3]'::vector(3) <#> '[4, 5, 6]'::vector(3)) AS manfiy_ichki_kopaytma,
    -1 * ('[1, 2, 3]'::vector(3) <#> '[4, 5, 6]'::vector(3)) AS toza_dot_product;""",
    "`<->` — L2 masofasini (to'g'ri chiziqli Evklid masofasi) hisoblaydi. `<#>` — manfiy ichki ko'paytmani (Negative Dot Product) beradi (PostgreSQL eng kichik qiymat bo'yicha ORDER BY qilgani sababli ichki ko'paytma manfiy qilinadi; uni -1 ga ko'paytirsak haqiqiy Dot Product hosil bo'ladi).",
    """ evklid_masofa | manfiy_ichki_kopaytma | toza_dot_product 
---------------+-----------------------+------------------
      5.196152 |                   -32 |               32
(1 row)"""
)

# 963
add_task(
    963,
    "HNSW (Hierarchical Navigable Small World) Vektor indeksi yaratish",
    "Millionlab vektorlar ustida millisoniyalarda eng yuqori aniqlikdagi ANN (Approximate Nearest Neighbor) qidiruvini ta'minlovchi zamonaviy `HNSW` indeksini yarating.",
    """-- HNSW indeksi yaratish (Kosinus masofasi uchun vector_cosine_ops)
CREATE INDEX idx_hujjatlar_hnsw_cosine 
ON ai_hujjatlar_vektor USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Indeksdan foydalangan qidiruv
EXPLAIN (COSTS OFF)
SELECT id, hujjat_matni
FROM ai_hujjatlar_vektor
ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector(1536)
LIMIT 5;""",
    "`HNSW` — hozirgi kunda dunyodagi eng tez va aniq vektorli indekslash grafigi algoritmidir. `m = 16` har bir tugunning qo'shnilari soni, `ef_construction = 64` esa indeks qurishdagi qidiruv chuqurligidir. U xotirani ko'proq oladi, ammo qidiruv tezligi bo'yicha IVFFlat'dan bir necha barobar ustundir.",
    """                       QUERY PLAN                       
--------------------------------------------------------
 Limit
   ->  Index Scan using idx_hujjatlar_hnsw_cosine on ai_hujjatlar_vektor
         Order By: (embedding <=> '[...]'::vector)
(3 rows)"""
)

# 964
add_task(
    964,
    "IVFFlat (Inverted File Flat) Vektor indeksi yaratish",
    "Xotirasi cheklangan serverlarda vektorlarni klasterlarga (Voronoi hujayralari) bo'lib indekslovchi `IVFFlat` indeksini yarating.",
    """-- IVFFlat indeksi (100 ta klaster markazi bilan)
CREATE INDEX idx_hujjatlar_ivfflat_l2 
ON ai_hujjatlar_vektor USING ivfflat (embedding vector_l2_ops)
WITH (lists = 100);

-- Qidiruv paytida tekshiriladigan klasterlar sonini sozlash
SET ivfflat.probes = 10;""",
    "`IVFFlat` barcha vektorlarni `lists` sonicha klasterlarga (centroid) taqsimlaydi. Indeks qurish HNSW ga qaraganda ancha tez va xotirani juda kam talab qiladi. Qidiruvda `probes` soni qancha katta qo'yilsa, aniqlik (recall) shuncha oshadi, lekin tezlik biroz pasayadi.",
    """SET"""
)

# 965
add_task(
    965,
    "Gibrid qidiruv (Hybrid Search): To'liq matnli (Full-Text) va Vektorli qidiruvni birlashtirish",
    "Aniq kalit so'zlar bo'yicha PostgreSQL ning `tsvector` imkoniyatini va semantik ma'no bo'yicha `pgvector`ni yagona ball (Reciprocal Rank Fusion - RRF) bilan birlashtiruvchi gibrid qidiruv so'rovini yozing.",
    """WITH matn_qidiruv AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY ts_rank(matn_tsvector, to_tsquery('uzbek', 'kredit & foiz')) DESC) AS rank_matn
    FROM korxona_bilimlar_bazasi
    WHERE matn_tsvector @@ to_tsquery('uzbek', 'kredit & foiz')
    LIMIT 20
),
vektor_qidiruv AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY embedding <=> '[0.12, 0.45, 0.88]'::vector(3)) AS rank_vektor
    FROM korxona_bilimlar_bazasi
    LIMIT 20
)
SELECT 
    COALESCE(m.id, v.id) AS hujjat_id,
    -- RRF (Reciprocal Rank Fusion) formulasi: 1 / (60 + rank)
    COALESCE(1.0 / (60 + m.rank_matn), 0.0) + COALESCE(1.0 / (60 + v.rank_vektor), 0.0) AS rrf_ball
FROM matn_qidiruv m
FULL OUTER JOIN vektor_qidiruv v ON m.id = v.id
ORDER BY rrf_ball DESC
LIMIT 5;""",
    "Gibrid qidiruv (Hybrid Search) AI tizimlarining 'oltin standarti'dir. Aniq kodlar, modellar, familiyalar (BM25/tsvector) orqali qidirilganda vektor adashishi mumkin; gibrid usul esa leksik qidiruv va neyron tarmoq vektorini RRF orqali birlashtirib, eng mukammal aniqlikni beradi.",
    """ hujjat_id |      rrf_ball       
-----------+--------------------
        14 | 0.0327868852459016
        88 | 0.0163934426229508
        22 | 0.0161290322580645
(3 rows)"""
)

# 966
add_task(
    966,
    "RAG (Retrieval-Augmented Generation) konveyeri: Matn bo'laklari (Chunks) va Metadata filtri",
    "Katta kitob yoki qonunchilik hujjatining bo'laklangan qismlarini (chunk_index) saqlab, bir vaqtda ham metadata (bo'lim, sana), ham vektor bo'yicha AI uchun kontekst yig'uvchi RAG so'rovini yozing.",
    """SELECT 
    hujjat_nomi,
    chunk_index,
    chunk_matni,
    ROUND((embedding <=> '[0.02, 0.77, 0.15]'::vector(3))::numeric, 4) AS masofa
FROM rag_bilimlar_ombori
WHERE tashkilot_id = 5 
  AND til = 'uz'
  AND nashr_yili >= 2023
ORDER BY embedding <=> '[0.02, 0.77, 0.15]'::vector(3)
LIMIT 3;""",
    "RAG arxitekturasida LLM (masalan, Claude yoki GPT) ga berish uchun hujjatlar 500-1000 belgilik bo'laklarga (chunks) ajratiladi. SQL ning eng katta ustunligi shundaki, u bitta so'rovda qat'iy relyatsion metama'lumotlarni (`tashkilot_id = 5`, `nashr_yili >= 2023`) vektorli semantik qidiruv bilan birga filtrlay oladi.",
    """     hujjat_nomi      | chunk_index |                  chunk_matni                  | masofa 
----------------------+-------------+-----------------------------------------------+--------
 Mehnat Kodeksi       |          12 | Xodimga yillik asosiy ta'til 21 kalendar kuni | 0.0112
 Soliq Imtiyozlari    |           4 | IT Park rezidentlari daromad solig'i 7.5%     | 0.0345
 Ichki Tartib Qoidasi |           1 | Ish vaqti soat 09:00 dan boshlanadi           | 0.0892
(3 rows)"""
)

# 967
add_task(
    967,
    "Vektorlarni normallashtirish (L2 Normalize) va Inner Product orqali maksimal tezlikka erishish",
    "Barcha vektorlarni birlik uzunlikka (norm = 1.0) keltirib saqlash va kosinus masofasi o'rniga eng tez hisoblanuvchi Inner Product `<#>` operatoridan foydalanish usulini ko'rsating.",
    """-- Vektorni uzunligiga bo'lib normallashtirish (Unit vector)
WITH vektorlar AS (
    SELECT '[3, 4]'::vector(2) AS v
)
SELECT 
    v,
    -- l2_norm funksiyasi vektor uzunligini (normasini) hisoblaydi: sqrt(3^2 + 4^2) = 5
    l2_norm(v) AS norma,
    -- Normallashgan vektor: [3/5, 4/5] = [0.6, 0.8]
    (v / l2_norm(v)) AS normallashtirilgan_vektor
FROM vektorlar;""",
    "Matematik jihatdan, agar ikki vektor birlik uzunlikka ega bo'lsa (`norm = 1`), ularning Kosinus o'xshashligi to'g'ridan-to'g'ri ularning Skalyar ko'paytmasiga (Dot Product) teng bo'ladi. Skalyar ko'paytma esa protsessorda ildiz olish amalisiz ishlaydi va SIMD (AVX-512) instruksiyalari bilan apparat darajasida 3-5 barobar tezroq hisoblanadi.",
    """    v    | norma | normallashtirilgan_vektor 
---------+-------+---------------------------
 [3,4]   |     5 | [0.6,0.8]
(1 row)"""
)

# 968
add_task(
    968,
    "pg_stat_statements yordamida sekin ishlayotgan korporativ so'rovlarni aniqlash",
    "Ma'lumotlar bazasida eng ko'p umumiy vaqt sarflayotgan (total_exec_time) va serverga eng katta yuklama berayotgan top-3 ta SQL so'rovini aniqlovchi monitoring tahlilini yozing.",
    """SELECT 
    queryid,
    SUBSTRING(query, 1, 50) AS qisqa_sorov,
    calls AS chaqiruvlar_soni,
    ROUND(total_exec_time::numeric, 2) AS jami_vaqt_ms,
    ROUND(mean_exec_time::numeric, 2) AS ortacha_vaqt_ms,
    ROUND((100.0 * total_exec_time / SUM(total_exec_time) OVER())::numeric, 2) AS umumiy_yuklama_foiz
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 3;""",
    "`pg_stat_statements` har bir korporativ DBA va arxitektorning birinchi raqamli diagnostika qurolidir. U barcha bajarilgan so'rovlarning parametrlarini umumlashtirib, qaysi SQL eng ko'p protsessor va xotira vaqtini olayotganini foizlarda aniq ko'rsatib beradi.",
    """       queryid        |                    qisqa_sorov                    | chaqiruvlar_soni | jami_vaqt_ms | ortacha_vaqt_ms | umumiy_yuklama_foiz 
---------------------+---------------------------------------------------+------------------+--------------+-----------------+---------------------
 -489218491204812491 | SELECT * FROM buyurtmalar WHERE mijoz_id = $1     |           250000 |    452100.50 |            1.81 |               42.15
  192048124910294102 | UPDATE hisoblar SET balans = balans + $1 WHERE id |           180000 |    210400.12 |            1.17 |               19.60
  881924019240129401 | SELECT count(*) FROM loglar WHERE vaqt < $1       |             1200 |    140500.80 |          117.08 |               13.09
(3 rows)"""
)

# 969
add_task(
    969,
    "Xotira keshini tahlil qilish (Buffer Cache Hit Ratio)",
    "Server diskdan o'qiyaptimi yoki RAM xotirasidanmi (Shared Buffers)? Ma'lumotlar bazasining keshdan o'qish samaradorligi (Cache Hit Ratio) 99% dan yuqoriligini tekshiruvchi so'rov yozing.",
    """SELECT 
    datname AS baza_nomi,
    blks_hit AS ramdan_oqilgan_bloklar,
    blks_read AS diskdan_oqilgan_bloklar,
    ROUND((blks_hit::numeric / NULLIF(blks_hit + blks_read, 0) * 100), 2) AS kesh_samaradorligi_foiz
FROM pg_stat_database
WHERE datname = current_database();""",
    "Yuqori samarali OLTP tizimlarida `kesh_samaradorligi_foiz` (Buffer Cache Hit Ratio) kamida 99.0% bo'lishi kerak. Agar ushbu ko'rsatkich 95% dan pastga tushsa, bu serverga `shared_buffers` yetishmayotganini va baza juda ko'p sekin disk I/O operatsiyalarini bajarayotganini bildiradi.",
    """ baza_nomi | ramdan_oqilgan_bloklar | diskdan_oqilgan_bloklar | kesh_samaradorligi_foiz 
-----------+------------------------+-------------------------+-------------------------
 postgres  |              145289100 |                  210450 |                   99.86
(1 row)"""
)

# 970
add_task(
    970,
    "Jadvallardagi o'lik qatorlar (Dead Tuples) va Bloat darajasini aniqlash",
    "Jadvalda `UPDATE` va `DELETE` amallaridan keyin qolib ketgan, xotirani band qilib so'rovlarni sekinlashtirayotgan o'lik qatorlarni (dead tuples) aniqlovchi DBA so'rovini yozing.",
    """SELECT 
    relname AS jadval_nomi,
    n_live_tup AS tirik_qatorlar,
    n_dead_tup AS olik_qatorlar,
    ROUND((n_dead_tup::numeric / NULLIF(n_live_tup + n_dead_tup, 0) * 100), 2) AS olik_qatorlar_ulushi_foiz,
    last_autovacuum AS oxirgi_autovacuum_vaqti
FROM pg_stat_user_tables
WHERE n_dead_tup > 0
ORDER BY n_dead_tup DESC
LIMIT 5;""",
    "PostgreSQL MVCC arxitekturasida o'chirilgan yoki yangilangan qatorlar darhol diskdan o'chirilmaydi, balki o'lik qator (`dead tuple`) sifatida qoladi. Ularni tozalash `VACUUM` jarayoni orqali amalga oshiriladi. Agar o'lik qatorlar ulushi 20% dan oshib ketsa, autovacuum parametrlarini agressivroq sozlash lozim.",
    """   jadval_nomi   | tirik_qatorlar | olik_qatorlar | olik_qatorlar_ulushi_foiz |    oxirgi_autovacuum_vaqti    
-----------------+----------------+---------------+---------------------------+-------------------------------
 tolov_sessiyalar|         120000 |         45000 |                     27.27 | 2024-06-15 04:12:00.124581+00
 buyurtma_status |          85000 |         12000 |                     12.37 | 2024-06-15 06:30:15.891201+00
(2 rows)"""
)

# 971
add_task(
    971,
    "Ulanishlar hovuzi (Connection Pooling): pg_stat_activity orqali ulanishlarni boshqarish",
    "Barcha faol (active) va bo'sh turgan (idle in transaction) ulanishlarni, ularning IP manzili va qancha vaqtdan beri qulflanib turganini aniqlovchi so'rov yozing.",
    """SELECT 
    pid,
    usename AS foydalanuvchi,
    client_addr AS mijoz_ip,
    state AS holat,
    NOW() - state_change AS holatda_turgan_vaqt,
    SUBSTRING(query, 1, 40) AS bajarilayotgan_sql
FROM pg_stat_activity
WHERE state <> 'idle'
ORDER BY state_change ASC;""",
    "Ayniqsa `idle in transaction` holatidagi ulanishlar juda xavflidir, chunki ular o'z ortidan jadval qulflarini (locks) ushlab turadi va boshqa tranzaksiyalarni muzlatib qo'yadi. PgBouncer kabi ulanishlar hovuzidan (connection pooler) foydalanish va bunday sessiyalarni tezkor bartaraf etish talab etiladi.",
    """  pid  | foydalanuvchi |  mijoz_ip   |        holat        | holatda_turgan_vaqt |          bajarilayotgan_sql           
-------+---------------+-------------+---------------------+---------------------+---------------------------------------
 15421 | app_user      | 192.168.1.5 | active              | 00:00:02.140501     | SELECT * FROM katta_hisobot_view...
 15488 | app_user      | 192.168.1.8 | idle in transaction | 00:02:15.890124     | UPDATE bank_hisob SET balans = ...
(2 rows)"""
)

# 972
add_task(
    972,
    "Sessiyani majburiy to'xtatish: pg_cancel_backend vs pg_terminate_backend",
    "Tizimni muzlatib qo'ygan 15488-raqamli jarayonni xavfsiz to'xtatish (cancel) va agar to'xtamasa majburan uzib tashlash (terminate) buyruqlarini yozing.",
    """-- 1. Avval faqat joriy so'rovni yumshoq bekor qilishga urinish (Cancel)
SELECT pg_cancel_backend(15488);

-- 2. Agar so'rov javob bermasa, TCP ulanishni majburan o'ldirish (Terminate)
SELECT pg_terminate_backend(15488);""",
    "`pg_cancel_backend(pid)` faqatgina shu sessiyada bajarilayotgan so'rovga SIGINT signali yuboradi va ulanish ochiq qoladi. `pg_terminate_backend(pid)` esa butun backend jarayonini (SIGTERM) zudlik bilan yo'q qiladi va operatsion tizim resurslarini ozod qiladi.",
    """ pg_terminate_backend 
----------------------
 t
(1 row)"""
)

# 973
add_task(
    973,
    "Jadval va indekslarning diskdagi fizik hajmini aniq tahlil qilish",
    "Barcha jadvallarning faqat jadval qismi hajmini, indekslari hajmini va umumiy diskdan egallagan o'rnini chiroyli formatda (`pg_size_pretty`) hisoblang.",
    """SELECT 
    relname AS obekt_nomi,
    pg_size_pretty(pg_table_size(c.oid)) AS sof_jadval_hajmi,
    pg_size_pretty(pg_indexes_size(c.oid)) AS indekslar_hajmi,
    pg_size_pretty(pg_total_relation_size(c.oid)) AS jami_fizik_hajm
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND c.relkind = 'r'
ORDER BY pg_total_relation_size(c.oid) DESC
LIMIT 3;""",
    "`pg_table_size` faqat qatorlar hajmini, `pg_indexes_size` unga tegishli barcha B-Tree/GIN indekslar hajmini, `pg_total_relation_size` esa TOAST va barcha qo'shimcha komponentlar bilan umumiy xotirani ko'rsatadi. Ko'pincha noto'g'ri loyihalangan indekslar jadvalning o'zidan 3 barobar ko'proq joy egallashi aniqlanadi.",
    """   obekt_nomi    | sof_jadval_hajmi | indekslar_hajmi | jami_fizik_hajm 
-----------------+------------------+-----------------+-----------------
 tolov_jurnali   | 14 GB            | 8192 MB         | 22 GB
 foydalanuvchilar| 850 MB           | 1200 MB         | 2050 MB
 tovarlar        | 120 MB           | 45 MB           | 165 MB
(3 rows)"""
)

# 974
add_task(
    974,
    "Foydalanilmayotgan keraksiz indekslarni (Unused Indexes) topish",
    "Serverda saqlanib, INSERT va UPDATE amallarini sekinlashtirayotgan, lekin biror marta ham qidiruvda ishlatilmagan (`idx_scan = 0`) indekslarni aniqlang.",
    """SELECT 
    schemaname AS sxema,
    relname AS jadval_nomi,
    indexrelname AS indeks_nomi,
    idx_scan AS ishlatilgan_soni,
    pg_size_pretty(pg_relation_size(indexrelid)) AS indeks_hajmi
FROM pg_stat_user_indexes
WHERE idx_scan = 0 
  AND indexrelname NOT LIKE '%_pkey' -- Birlamchi kalit indekslarini chetlab o'tish
ORDER BY pg_relation_size(indexrelid) DESC;""",
    "Har bir yaratilgan indeks har qanday INSERT va UPDATE operatsiyasida qayta yozilishi shart. Agar indeksdan hech kim foydalanmayotgan bo'lsa (`idx_scan = 0`), u faqat tizimni sekinlashtiradi va diskni behuda band qiladi. Bunday indekslar darhol o'chirilishi kerak.",
    """ sxema  |   jadval_nomi    |         indeks_nomi          | ishlatilgan_soni | indeks_hajmi 
--------+------------------+------------------------------+------------------+--------------
 public | buyurtmalar      | idx_buyurtma_eski_izoh       |                0 | 450 MB
 public | foydalanuvchilar | idx_foydalanuvchi_vaqtincha  |                0 | 120 MB
(2 rows)"""
)

# 975
add_task(
    975,
    "Replitsiya kechikishini (Replication Lag) o'lchash",
    "Asosiy (Master/Primary) serverda replikatsiyaga ulangan replika serverlarining holatini va qancha bayt yoki soniya orqada qolayotganini tahlil qiluvchi so'rov yozing.",
    """SELECT 
    application_name AS replika_nomi,
    client_addr AS replika_ip,
    state AS oqim_holati,
    sync_state AS sinxronlik_turi,
    pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS kechikish_baytlarda
FROM pg_stat_replication;""",
    "`pg_stat_replication` ko'rinishi streaming replication holatini nazorat qiladi. `pg_wal_lsn_diff` orqali masterdagi oxirgi WAL pozitsiyasi bilan replikada qayta ijro etilgan pozitsiya o'rtasidagi farq o'lchanadi. Agar kechikish ortib ketsa, replikadan o'qiyotgan foydalanuvchilar eskirgan ma'lumotlarni ko'radi.",
    """ replika_nomi |  replika_ip   | oqim_holati | sinxronlik_turi | kechikish_baytlarda 
--------------+---------------+-------------+-----------------+---------------------
 standby_replica_1 | 192.168.1.100 | streaming   | async           |                   0
 standby_replica_2 | 192.168.1.101 | streaming   | async           |                4096
(2 rows)"""
)

# 976
add_task(
    976,
    "WAL (Write-Ahead Logging) hosil bo'lish tezligini va arxivlanishini kuzatish",
    "Serverda so'nggi vaqtda qancha WAL loglari yozilayotganini va arxivlash holatini ko'rsatuvchi ma'muriy so'rov yozing.",
    """SELECT 
    archived_count AS arxivlangan_fayllar,
    failed_count AS xatolik_berganlar,
    last_archived_wal AS oxirgi_arxiv_wal,
    last_archived_time AS oxirgi_arxiv_vaqti
FROM pg_stat_archiver;""",
    "`pg_stat_archiver` doimiy zaxira nusxalash (Point-in-Time Recovery - PITR) jarayonining sog'lomligini ko'rsatadi. Agar `failed_count > 0` bo'lsa, demak arxiv saqlash drayverida (masalan S3 yoki NFS) muammo bor va zudlik bilan bartaraf etilishi shart, aks holda master disk to'lib qulashi mumkin.",
    """ arxivlangan_fayllar | xatolik_berganlar |    oxirgi_arxiv_wal     |      oxirgi_arxiv_vaqti       
--------------------+-------------------+-------------------------+-------------------------------
               4512 |                 0 | 0000000100000A1B0000002F | 2024-06-15 17:00:02.124501+00
(1 row)"""
)

# 977
add_task(
    977,
    "Muzlagan XID (Transaction ID Wraparound) xavfini monitoring qilish",
    "PostgreSQL ning eng xavfli falokatlaridan biri bo'lgan 2 milliardlik tranzaksiyalar hisoblagichining to'lib qolishiga qancha qolganini tahlil qiluvchi so'rov yozing.",
    """SELECT 
    datname AS baza_nomi,
    age(datfrozenxid) AS joriy_tranzaksiya_yoshi,
    2147483648 - age(datfrozenxid) AS tolib_toshishgacha_qolgan_xid
FROM pg_database
WHERE datallowconn
ORDER BY age(datfrozenxid) DESC;""",
    "PostgreSQL 32-bitli Tranzaksiya ID (XID) dan foydalanadi. Agar baza 2 milliard tranzaksiyadan oshib ketsa va `VACUUM FREEZE` qilinmagan bo'lsa, tizim o'zini ma'lumotlar yo'qolishidan himoya qilish uchun avtomatik ravishda to'liq to'xtaydi (Read-Only rejimiga o'tadi). Shuning uchun XID yoshi doimiy monitoring qilinishi shart.",
    """ baza_nomi | joriy_tranzaksiya_yoshi | tolib_toshishgacha_qolgan_xid 
-----------+-------------------------+-------------------------------
 korxona_db|                45100200 |                    2102383448
 postgres  |                 1200450 |                    2146283198
(2 rows)"""
)

# 978
add_task(
    978,
    "Avtomatik statistikani yangilash: ANALYZE va Auto-Analyze koeffitsientlari",
    "PostgreSQL so'rov rejalashtiruvchisi (Query Planner) to'g'ri reja tuza olishi uchun statistikani qo'lda yangilang va jadval statistikasining yangilangan vaqtini tekshiring.",
    """-- 1. Jadval statistikalarini qayta tahlil qilish
ANALYZE VERBOSE buyurtmalar;

-- 2. Statistika qachon yangilanganini tekshirish
SELECT 
    relname,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
WHERE relname = 'buyurtmalar';""",
    "`ANALYZE` jadvaldagi ma'lumotlarning taqsimlanish chastotasini (MCV - Most Common Values va Histogram) o'lchab `pg_statistic` ga yozadi. Barcha Index Scan va Seq Scan qarorlari aynan shu statistikaga asoslanadi. Yangilanmagan statistika noto'g'ri reja tuzilishiga va so'rovlarning 1000 barobar sekinlashishiga olib keladi.",
    """INFO:  analyzing "public.buyurtmalar"
INFO:  "buyurtmalar": scanned 3000 of 3000 pages, containing 250000 live rows and 0 dead rows; 30000 rows in sample
   relname   |         last_analyze          |       last_autoanalyze        
-------------+-------------------------------+-------------------------------
 buyurtmalar | 2024-06-15 17:15:22.189201+00 | 2024-06-14 22:00:10.512401+00
(1 row)"""
)

# 979
add_task(
    979,
    "Vektorli ma'lumotlar bazasida klasterlash: K-Means orqali mijozlarni segmentatsiya qilish",
    "Mijozlarning xarid harakatlari vektorlarini (3 o'lchamli) tahlil qilib, ularning markazini (centroid) o'rtacha qiymatlar orqali hisoblang.",
    """WITH mijoz_vektorlari AS (
    SELECT 1 AS mijoz_id, 'A' AS guruh, '[100, 2, 5]'::vector(3) AS xulq
    UNION ALL
    SELECT 2 AS mijoz_id, 'A' AS guruh, '[120, 3, 6]'::vector(3) AS xulq
    UNION ALL
    SELECT 3 AS mijoz_id, 'B' AS guruh, '[10, 50, 2]'::vector(3) AS xulq
)
SELECT 
    guruh,
    COUNT(*) AS mijozlar_soni,
    -- Vektorlarning o'rtacha markazini (Centroid) hisoblash
    avg(xulq)::vector(3) AS klaster_markazi
FROM mijoz_vektorlari
GROUP BY guruh;""",
    "`pgvector` kengaytmasi vektorlar ustida maxsus `avg(vector)` agregat funksiyasini taqdim etadi. Bu mashinaviy o'rganishdagi K-Means klasterlash algoritmini bevosita SQL ichida amalga oshirish va har bir mijoz segmentining markaziy vektorini aniqlash imkonini beradi.",
    """ guruh | mijozlar_soni | klaster_markazi 
-------+---------------+-----------------
 A     |             2 | [110,2.5,5.5]
 B     |             1 | [10,50,2]
(2 rows)"""
)

# 980
add_task(
    980,
    "Jadval qulflanishini (Lock Contention) diagnostika qilish va to'siqlarni bartaraf etish",
    "Qaysi sessiya boshqa qaysi sessiyani qulflab, kutishga (Lock Wait) majbur qilayotganini ko'rsatuvchi to'liq qulflar daraxti (Lock Tree) so'rovini yozing.",
    """SELECT 
    blocked_locks.pid AS kutilayotgan_pid,
    blocked_activity.usename AS kutilayotgan_user,
    blocking_locks.pid AS tosqinlik_qilayotgan_pid,
    blocking_activity.usename AS tosqinlik_qilayotgan_user,
    blocked_activity.query AS toxtab_qolgan_sorov,
    blocking_activity.query AS bloklagan_sorov
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks 
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
    AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
    AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
    AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
    AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
    AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
    AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;""",
    "Ushbu mashhur diagnostik SQL so'rovi kim kimni ushlab turganini ko'rsatadi: qaysi PID qulflangan, qaysi PID qulfni bermayapti va ular qaysi so'rovlarni bajarmoqda. Bu orqali bloklangan jarayon darhol topilib hal qilinadi.",
    """ kutilayotgan_pid | kutilayotgan_user | tosqinlik_qilayotgan_pid | tosqinlik_qilayotgan_user |         toxtab_qolgan_sorov          |          bloklagan_sorov          
-----------------+-------------------+--------------------------+---------------------------+--------------------------------------+-----------------------------------
           19820 | web_app           |                    19800 | cron_worker               | UPDATE mahsulotlar SET qoldiq = ...  | ALTER TABLE mahsulotlar ADD CO...
(1 row)"""
)

# 981
add_task(
    981,
    "Korporativ zaxira nusxalash strategiyasi: pg_dump va pg_restore parametrlari",
    "Ishlab chiqarish bazasining to'liq siqilgan, ko'p oqimli parallel (Directory format) zaxira nusxasini olish va uni tiklash bo'yicha terminal buyruqlarini bajaring.",
    """-- 1. 4 ta yadroda parallel zaxira olish (Directory formati)
-- pg_dump -h localhost -U postgres -d korxona_db -F d -j 4 -f /backup/korxona_2024_06_15

-- 2. Ma'lumotlar bazasiga parallel qayta tiklash (Restore)
-- pg_restore -h localhost -U postgres -d yangi_korxona_db -j 4 /backup/korxona_2024_06_15

SELECT 'Zaxiralash strategiyasi muvaffaqiyatli rejalashtirildi' AS status;""",
    "`pg_dump` ning `-F d` (directory) formati eng kuchli usul bo'lib, har bir jadvalni alohida faylga siqib yozadi va `-j 4` orqali 4 ta CPU yadrosida parallel ishlaydi. Bu terabaytlik bazalarni tiklash vaqtini 10 soatdan 1 soatga qisqartiradi.",
    """                        status                        
------------------------------------------------------
 Zaxiralash strategiyasi muvaffaqiyatli rejalashtirildi
(1 row)"""
)

# 982
add_task(
    982,
    "Logical Replication (Mantiqiy replikatsiya): PUBLICATION va SUBSCRIPTION yaratish",
    "Boshqa serverga faqat aniq ikkita jadvalning ma'lumotlarini real vaqtda uzluksiz oqim (streaming) qilib uzatuvchi `PUBLICATION` va `SUBSCRIPTION` buyruqlarini yozing.",
    """-- 1. Bosh serverda (Publisher) nashr yaratish
CREATE PUBLICATION pub_savdo_mahsulot 
FOR TABLE tovarlar, filial_savdolari;

-- Nashr holatini tekshirish
SELECT pubname, puballtables FROM pg_publication;

-- 2. Qabul qiluvchi serverda (Subscriber) obuna ochish (Izohda berilgan)
-- CREATE SUBSCRIPTION sub_savdo_mahsulot 
-- CONNECTION 'host=192.168.1.10 dbname=korxona_db user=repl_user password=maxfiy' 
-- PUBLICATION pub_savdo_mahsulot;""",
    "Mantiqiy replikatsiya (Logical Replication) turli xil versiyalardagi (masalan PG 15 dan PG 16 ga) yoki turli operatsion tizimlardagi serverlar o'rtasida aniq jadvallarni real vaqtda nusxalash imkonini beradi.",
    """      pubname       | puballtables 
--------------------+--------------
 pub_savdo_mahsulot | f
(1 row)"""
)

# 983
add_task(
    983,
    "pg_trgm va pgvector ni birlashtirgan universal qidiruv mexanizmi",
    "Foydalanuvchi so'rovida imlo xatolari (typos) bo'lsa trigramma (`pg_trgm`) orqali tuzatuvchi, so'ngra vektor orqali uning chuqur ma'nosini topuvchi integratsion yechim tuzing.",
    """CREATE EXTENSION IF NOT EXISTS pg_trgm;

WITH xom_qidiruv AS (
    -- Imlo xatosini trigramma o'xshashligi orqali tuzatish (masalan 'kredt' -> 'kredit')
    SELECT soz 
    FROM lugat 
    ORDER BY similarity(soz, 'kredt') DESC 
    LIMIT 1
)
SELECT h.id, h.hujjat_matni, (h.embedding <=> '[0.11, 0.44, 0.89]'::vector(3)) AS masofa
FROM ai_hujjatlar_vektor h, xom_qidiruv x
WHERE h.hujjat_matni ILIKE '%' || x.soz || '%'
ORDER BY h.embedding <=> '[0.11, 0.44, 0.89]'::vector(3)
LIMIT 2;""",
    "Ushbu yechim zamonaviy AI qidiruv tizimlarining muammosini hal qiladi: foydalanuvchilar qidiruvda ko'pincha so'zlarni xato yozadi (`pg_trgm` xatoni to'g'rilaydi), so'ngra `pgvector` orqali semantik kontekst chiqariladi.",
    """ id |                    hujjat_matni                    | masofa 
----+----------------------------------------------------+--------
  4 | Imtiyozli ta'lim krediti shartlari va foizlari    | 0.0125
  8 | Iste'mol krediti bo'yicha to'lovlar jadvali        | 0.0450
(2 rows)"""
)

# 984
add_task(
    984,
    "SQL Injection dan 100% himoyalangan dinamik xavfsiz protsedura",
    "Istalgan filtr parametri berilganda SQL Injection xavfini `quote_ident`, `quote_literal` va `format()` orqali butunlay bartaraf etuvchi korporativ protsedura yarating.",
    """CREATE OR REPLACE FUNCTION xavfsiz_qidiruv_korxona(
    p_jadval TEXT,
    p_maydon TEXT,
    p_qiymat TEXT
)
RETURNS TABLE(id INT, natija TEXT)
LANGUAGE plpgsql
AS $$
DECLARE
    v_sql TEXT;
BEGIN
    -- Identifikatorlarni %I va parametrlarni $1 bilan bog'lash
    v_sql := format(
        'SELECT id, %I::TEXT FROM %I WHERE %I = $1 LIMIT 5',
        p_maydon, p_jadval, p_maydon
    );

    RETURN QUERY EXECUTE v_sql USING p_qiymat;
END;
$$;

SELECT * FROM xavfsiz_qidiruv_korxona('xodimlar', 'ism', 'Alisher');""",
    "Hech qachon SQL so'roviga foydalanuvchi matni `+` yoki `||` orqali ulanmasligi kerak! `format('%I', col)` identifikatorlarni qo'shtirnoqqa oladi, qiymatlar esa qat'iy ravishda `USING` va `$1` parametrlari orqali uzatiladi.",
    """ id | natija  
----+---------
  1 | Alisher
(1 row)"""
)

# 985
add_task(
    985,
    "pg_upgrade orqali yangi PostgreSQL versiyasiga 'Zero Downtime' yaqin rejimda o'tish",
    "PostgreSQL 15 dan PostgreSQL 16 ga ma'lumotlarni ko'chirishda diskdagi fayllarni qayta nusxalamasdan, qattiq havolalar (`--link`) orqali soniyalar ichida yangilash buyrug'ini ko'rsating.",
    """-- pg_upgrade --link buyrug'i:
-- /usr/lib/postgresql/16/bin/pg_upgrade \\
--   --old-datadir=/var/lib/postgresql/15/main \\
--   --new-datadir=/var/lib/postgresql/16/main \\
--   --old-bindir=/usr/lib/postgresql/15/bin \\
--   --new-bindir=/usr/lib/postgresql/16/bin \\
--   --link

SELECT 'Hard links orqali terabaytlab baza 2 daqiqada yangilandi' AS yangilanish_xabari;""",
    "`pg_upgrade --link` drayver darajasida yangi versiya katalogiga OS qattiq havolalarini (hard links) bog'laydi. 10 Terabaytlik bazani ko'chirish an'anaviy `pg_dump` da bir necha kun talab qilsa, `--link` rejimi bilan atigi 2-3 daqiqada bajariladi.",
    """                     yangilanish_xabari                      
-------------------------------------------------------------
 Hard links orqali terabaytlab baza 2 daqiqada yangilandi
(1 row)"""
)

# 986
add_task(
    986,
    "Vektorlarni siqish: Half-Precision (vector 16-bit / fp16) va HNSW",
    "RAM xotirani 50% ga tejash uchun embedding vektorlarini 16-bitli suzuvchi nuqta (halfvec) formatida saqlash va indekslash amaliyotini bajaring.",
    """-- pgvector ning yangi halfvec (16-bit float) turi
CREATE TABLE ai_hujjatlar_halfvec (
    id SERIAL PRIMARY KEY,
    matn TEXT,
    embedding halfvec(1536) -- 32-bit o'rniga 16-bit (xotira 2 barobar tejaladi!)
);

-- Indeks yaratish
CREATE INDEX idx_halfvec_hnsw 
ON ai_hujjatlar_halfvec USING hnsw (embedding halfvec_l2_ops);

SELECT 'Halfvec orqali 50% RAM tejaldi' AS xotira_natija;""",
    "1536 o'lchamli 1 millionta standart vektor (`vector`) taxminan 6.2 GB RAM talab qiladi. `halfvec` (FP16) orqali ushbu hajm 3.1 GB ga tushadi, qidiruv aniqligi (recall) esa 99.5% darajasida deyarli o'zgarishsiz saqlanib qoladi.",
    """         xotira_natija         
-------------------------------
 Halfvec orqali 50% RAM tejaldi
(1 row)"""
)

# 987
add_task(
    987,
    "pg_repack yordamida jadvalni bloklamasdan Bloatni yo'qotish (Zero Downtime Repack)",
    "`VACUUM FULL` butun jadvalni qulflab qo'yishi sababli, ishlab chiqarish tizimida o'qish va yozishni to'xtatmasdan jadvalni nolga teng ixcham holatga keltiruvchi `pg_repack` arxitekturasini tushuntiring.",
    """-- pg_repack kengaytmasi
-- pg_repack -h localhost -U postgres -d korxona_db -t buyurtmalar

SELECT 'pg_repack jadvalni qulflamasdan toliq ixchamlashtirdi' AS repack_status;""",
    "`pg_repack` fonda yangi nusxa jadval yaratadi, trigger orqali yangi o'zgarishlarni yozib boradi, indekslarni qayta quradi va eng oxirida millisoniyalik qulf bilan jadvallar nomini almashtirib qo'yadi. Foydalanuvchilar uzilishni mutlaqo sezmaydi.",
    """                    repack_status                    
-----------------------------------------------------
 pg_repack jadvalni qulflamasdan toliq ixchamlashtirdi
(1 row)"""
)

# 988
add_task(
    988,
    "Tizim parametrlarini apparat resurslariga moslash (Hardware-based PGTune)",
    "64 GB operativ xotiraga (RAM) va 16 yadroli CPU ga ega korporativ PostgreSQL serveri uchun optimal konfiguratsiya sozlamalarini hisoblang.",
    """SELECT 
    '64GB RAM / 16 Core' AS server_profil,
    '16GB' AS shared_buffers,         -- RAM ning 25% qismi
    '48GB' AS effective_cache_size,    -- RAM ning 75% qismi
    '64MB' AS work_mem,                -- Murakkab saralashlar uchun
    '2GB'  AS maintenance_work_mem,    -- Indeks va VACUUM tezligi
    '1.1'  AS random_page_cost;        -- NVMe SSD uchun optimal ko'rsatkich""",
    "PostgreSQL ning standart sozlamalari (standart shared_buffers = 128MB) qadimiy kompyuterlar uchun mo'ljallangan. Zamonaviy NVMe SSD drayverlarda `random_page_cost = 1.1` qo'yilsa, rejalashtiruvchi indekslarni to'g'ri tanlaydi va tezlik keskin oshadi.",
    """   server_profil    | shared_buffers | effective_cache_size | work_mem | maintenance_work_mem | random_page_cost 
--------------------+----------------+----------------------+----------+----------------------+------------------
 64GB RAM / 16 Core | 16GB           | 48GB                 | 64MB     | 2GB                  | 1.1
(1 row)"""
)

# 989
add_task(
    989,
    "Binar vektorlar va Hamming masofasi (<~>) orqali ultra-tezkor qidiruv",
    "Embedding vektorlarini binarlashtirib (0 va 1 lar to'plami), xotirani 32 barobar tejash va Hamming masofasi `<~>` orqali bitli amallar bilan soniyasiga millionlab qidiruv o'tkazing.",
    """-- Binar vektor (bit turi)
WITH binar_vektorlar AS (
    SELECT 1 AS id, B'11010011'::bit(8) AS b_vec
    UNION ALL
    SELECT 2 AS id, B'11110000'::bit(8) AS b_vec
)
SELECT 
    id,
    -- Hamming masofasi: farqli bitlar soni (<~>)
    (b_vec <~> B'11010000'::bit(8)) AS hamming_farq
FROM binar_vektorlar;""",
    "Binary Quantization — sun'iy intellekt vektorlarini binar bitlarga (1 bit per dimension) aylantiradi. Hamming masofasi zamonaviy protsessorlarning `POPCNT` (population count) bitta mikrokodi bilan hisoblanadi va an'anaviy float32 ga qaraganda 50 barobar kamroq xotira sarflaydi.",
    """ id | hamming_farq 
----+--------------
  1 |            2
  2 |            1
(2 rows)"""
)

# 990
add_task(
    990,
    "Audit compliance: DDL o'zgarishlarini bloklash va Production Freeze",
    "Ishlab chiqarish bazasida ish vaqtida yoki hisobot yopilishi davrida hech kim jadvallar tuzilmasini o'zgartira olmasligi uchun 'Production Freeze' rejimini yoqishni Event Trigger orqali ta'minlang.",
    """CREATE OR REPLACE FUNCTION evt_bloklash_production_freeze()
RETURNS EVENT_TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE EXCEPTION 'Diqqat! Tizimda "Production Freeze" rejimi faol! Barcha DDL operatsiyalari taqiqlangan.'
        USING HINT = 'O''zgarish kiritish uchun release oynasini kuting.';
END;
$$;

CREATE EVENT TRIGGER trg_muhim_freeze
ON ddl_command_start
EXECUTE FUNCTION evt_bloklash_production_freeze();

-- Test
ALTER TABLE xodimlar ADD COLUMN sinov INT;""",
    "`ON ddl_command_start` hodisasi har qanday DDL boshlanishidayoq ishga tushadi va tranzaksiyaga yo'l bermaydi. Bu moliyaviy davr yopilishi paytida (masalan chorak oxiri yoki Qora Juma sotuvlarida) noxush kutilmagan o'zgarishlar oldini oladi.",
    """ERROR:  Diqqat! Tizimda "Production Freeze" rejimi faol! Barcha DDL operatsiyalari taqiqlangan.
HINT:  O'zgarish kiritish uchun release oynasini kuting."""
)

# 991
add_task(
    991,
    "SQL orqali korporativ kiberxavfsizlik: Parollar xavfsizligi va pgcrypto bilan ma'lumotlarni shifrlash",
    "`pgcrypto` kengaytmasidan foydalanib, foydalanuvchining shaxsiy sirli ma'lumotlarini (PIN kod, pasport) AES-256 algoritmi bilan shifrlab saqlash va parolni ochishni bajaring.",
    """CREATE EXTENSION IF NOT EXISTS pgcrypto;

WITH maxfiy AS (
    SELECT 
        -- AES-256 bilan shifrlash (pgp_sym_encrypt)
        pgp_sym_encrypt('Passport: AA1234567, PIN: 9988', 'SuperMaxfiyKalit_2024') AS shifrlangan_matn
)
SELECT 
    shifrlangan_matn,
    -- Shifrni kalit orqali qayta o'qish (pgp_sym_decrypt)
    pgp_sym_decrypt(shifrlangan_matn, 'SuperMaxfiyKalit_2024') AS ochilgan_matn
FROM maxfiy;""",
    "`pgcrypto` orqali saqlangan ma'lumotlar bazadan xakerlar tomonidan to'liq ko'chirib ketilgan (dump o'g'irlangan) taqdirda ham, shifrlash kalitisiz ularni o'qib bo'lmaydi. Bu xalqaro GDPR va PCI-DSS xavfsizlik standartlarining majburiy talabidir.",
    """                   shifrlangan_matn                   |          ochilgan_matn          
------------------------------------------------------+---------------------------------
 \xc30d04070302bf71d3...                             | Passport: AA1234567, PIN: 9988
(1 row)"""
)

# 992
add_task(
    992,
    "Avtomatik ma'lumotlarni tozalash (Retention Policy): Bo'lingan jadvallarda DROP PARTITION",
    "Eskirgan ma'lumotlarni o'chirish uchun milliardlab qatorga `DELETE` so'rovi yozmasdan, bitta buyruq orqali 3 yildan eski oylik qismni nolga teng disk yuklamasi bilan o'chirib tashlang.",
    """-- DELETE FROM logs WHERE vaqt < ... O'RNIGA:
DROP TABLE IF EXISTS tolovlar_y2020;

SELECT 'Eski arxiv qismi 0.01 soniyada jismonan tozalandi' AS status;""",
    "Katta jadvallardan `DELETE` qilish WAL jurnalini to'ldiradi, CPU ni yuklaydi va bo'sh joyni operatsion tizimga qaytarmaydi (bloat hosil qiladi). Bo'lingan (partitioned) jadvallarda esa bitta `DROP TABLE partition_name` buyrug'i terabaytlik ma'lumotni soniyaning ulushida diskdan ozod qiladi.",
    """                     status                      
-------------------------------------------------
 Eski arxiv qismi 0.01 soniyada jismonan tozalandi
(1 row)"""
)

# 993
add_task(
    993,
    "pg_stat_kcache orqali CPU va Disk I/O apparat yuklamasini o'lchash",
    "Qaysi SQL so'rovlari haqiqiy tizim operatsion tizimi (OS Kernel) darajasida eng ko'p CPU User Time va Read Bytes sarflayotganini tushuntiring.",
    """SELECT 
    queryid,
    ROUND(user_time::numeric, 2) AS cpu_foydalanuvchi_vaqti,
    ROUND(system_time::numeric, 2) AS cpu_yadro_vaqti,
    reads AS diskdan_oqilgan_baytlar
FROM pg_stat_kcache()
ORDER BY user_time DESC
LIMIT 1;""",
    "`pg_stat_kcache` kengaytmasi `getrusage` operatsion tizim qo'ng'iroqlari orqali so'rovning nafaqat PostgreSQL ichidagi vaqtini, balki Linux yadrosi sarflagan haqiqiy CPU va Disk I/O baytlarini aniq ko'rsatadi.",
    """       queryid        | cpu_foydalanuvchi_vaqti | cpu_yadro_vaqti | diskdan_oqilgan_baytlar 
---------------------+-------------------------+-----------------+-------------------------
 -819248102941029410 |                  145.20 |           12.40 |             14529100000
(1 row)"""
)

# 994
add_task(
    994,
    "AI Agent xotirasi: Suhbatlar tarixi (Chat History) va qisqa/uzoq muddatli xotira arxitekturasi",
    "Sun'iy intellekt agenti foydalanuvchi bilan olib borgan muloqotlari tarixini saqlaydigan va oxirgi 5 ta xabarni tezkor olib, eskilari bo'yicha semantik qidiruv qiluvchi arxitekturani quring.",
    """CREATE TABLE ai_suhbat_xotirasi (
    id BIGSERIAL PRIMARY KEY,
    sessiya_id UUID NOT NULL,
    rol VARCHAR(20) NOT NULL, -- 'user', 'assistant', 'system'
    xabar TEXT NOT NULL,
    embedding vector(3),
    yaratilgan_vaqt TIMESTAMPTZ DEFAULT NOW()
);

-- Oxirgi 3 ta xabarni olish (Qisqa muddatli xotira)
SELECT rol, xabar 
FROM ai_suhbat_xotirasi
WHERE sessiya_id = 'e7b1a2c3-4d5e-6f7a-8b9c-0d1e2f3a4b5c'
ORDER BY yaratilgan_vaqt DESC
LIMIT 3;""",
    "AI agentlar ikki xil xotiradan foydalanadi: Short-term memory (oxirgi N ta xabar relyatsion `ORDER BY vaqt DESC` orqali olinadi) va Long-term memory (avvalgi mavzular bo'yicha `embedding <=> query` orqali kerakli esdaliklar topiladi).",
    """    rol    |                 xabar                  
-----------+----------------------------------------
 assistant | Albatta, SQL optimallashtirish bo'yicha
 user      | PostgreSQL indekslari haqida aytib bering
 system    | Siz yordamchi AI assistentsiz
(3 rows)"""
)

# 995
add_task(
    995,
    "Auto-Failover va Yuqori Mavjudlik (High Availability: Patroni + etcd arxitekturasi)",
    "Master server qulagan taqdirda 10 soniya ichida yangi Masterni aniqlab, so'rovlarni uzluksiz davom ettiruvchi Patroni arxitekturasining boshqaruv so'rovini ko'rsating.",
    """-- Patroni holatini tekshirish (REST API orqali va SQL dan):
SELECT pg_is_in_recovery() AS server_replikami;""",
    "`pg_is_in_recovery()` funksiyasi agar server Master (bosh) bo'lsa `FALSE`, agar Replica (zaxira) bo'lsa `TRUE` qaytaradi. Patroni va DCS (etcd/Consul) klasteri orqali Master qulaganda avtomatik failover amalga oshirilib, eng ilg'or replika yangi masterga aylantiriladi.",
    """ server_replikami 
------------------
 f
(1 row)"""
)

# 996
add_task(
    996,
    "pg_dumpall yordamida butun klaster, rollar va global huquqlarni to'liq eksport qilish",
    "Barcha ma'lumotlar bazalari, global foydalanuvchilar (rollar) va ularning parollarini bitta yaxlit skriptda zaxiralash buyrug'ini bajaring.",
    """-- Faqat global rollar va huquqlarni olish
-- pg_dumpall -U postgres --globals-only -f /backup/globals.sql

SELECT 'Barcha global rollar va huquqlar saqlandi' AS natija;""",
    "`pg_dumpall --globals-only` barcha foydalanuvchilar, ularning rollari, tizim huquqlari va parollarini xavfsiz eksport qiladi. Bu yangi serverni noldan o'rnatishda foydalanuvchilarni qaytadan qo'lda kiritib o'tirish zaruratini yo'qotadi.",
    """                  natija                  
------------------------------------------
 Barcha global rollar va huquqlar saqlandi
(1 row)"""
)

# 997
add_task(
    997,
    "Katta jadvallarda Indekslarni uzluksiz qayta qurish (REINDEX CONCURRENTLY)",
    "Ishlab chiqarish jarayonida jadvallarni o'qish va yangilash operatsiyalarini bloklamasdan, eskirgan va bo'shliqlar hosil bo'lgan indeksni qayta quruvchi `CONCURRENTLY` buyrug'ini yozing.",
    """REINDEX TABLE CONCURRENTLY buyurtmalar;""",
    "Oddiy `REINDEX` butun jadvalga `AccessExclusiveLock` qo'yadi va hech kim jadvaldan o'qiy olmaydi. `REINDEX TABLE CONCURRENTLY` esa fonda parallel yangi indeks quradi va eski indeksni uning o'rniga jimgina almashtiradi. Hech qanday downtime yuz bermaydi.",
    """REINDEX"""
)

# 998
add_task(
    998,
    "Sun'iy intellekt embedding vektorlarining o'lchamlarini tekshiruvchi CHECK cheklovi",
    "Dasturchi adashib boshqa modelning (masalan 768 o'lchamli) vektorini kiritib qo'ymasligi uchun vektor o'lchamini tekshiruvchi cheklov qo'ying.",
    """CREATE TABLE model_vektorlar (
    id SERIAL PRIMARY KEY,
    v vector(1536),
    CONSTRAINT chk_vektor_olcham CHECK (vector_dims(v) = 1536)
);

SELECT 'Vektor o''lchami kafolatlangan jadval yaratildi' AS xabar;""",
    "`vector_dims(v)` funksiyasi vektorning o'lchamlar sonini qaytaradi. Ushbu `CHECK` cheklovi noto'g'ri o'lchamdagi vektorlar bazaga kirishining oldini oladi va AI pipeline'ning barqarorligini ta'minlaydi.",
    """                     xabar                     
-----------------------------------------------
 Vektor o'lchami kafolatlangan jadval yaratildi
(1 row)"""
)

# 999
add_task(
    999,
    "Korporativ SLA va Downtime audit monitoring ko'rinishi (System Uptime & Health View)",
    "Server oxirgi marta qachon ishga tushirilgani, umumiy ishlash vaqti (uptime) va kesh ko'rsatkichlarini bitta monitoring view'ga birlashtiring.",
    """CREATE OR REPLACE VIEW v_tizim_salomatligi AS
SELECT 
    pg_postmaster_start_time() AS server_ishga_tushgan_vaqt,
    NOW() - pg_postmaster_start_time() AS uzluksiz_ishlash_vaqti,
    (SELECT count(*) FROM pg_stat_activity WHERE state = 'active') AS faol_so'rovlar_soni,
    (SELECT count(*) FROM pg_stat_activity) AS jami_ulanishlar,
    current_setting('server_version') AS server_versiyasi;

SELECT * FROM v_tizim_salomatligi;""",
    "Ushbu monitoring ko'rinishi DevOps va monitoring (Prometheus, Grafana) tizimlari uchun server holatini bir zumda skanerlash imkonini beradi: uptime, versiya va joriy faol yuklama darajasi ko'rinib turadi.",
    """   server_ishga_tushgan_vaqt   | uzluksiz_ishlash_vaqti | faol_so'rovlar_soni | jami_ulanishlar | server_versiyasi 
-------------------------------+------------------------+---------------------+-----------------+------------------
 2024-06-01 00:00:00.000000+00 | 14 days 17:35:10       |                   3 |              42 | 16.3
(1 row)"""
)

# 1000
add_task(
    1000,
    "1,000-Topshiriq: To'liq korporativ Bank, E-Commerce va AI RAG ekotizimini birlashtiruvchi yakuniy master arxitektura",
    "Bank hisoblari, e-tijorat savdolari va sun'iy intellekt semantik tavsiyalarini bitta tranzaksiyada xavfsiz boshqaruvchi, RLS, audit va vektor qidiruvi bilan qurollangan yakuniy master yechimni yozing.",
    """BEGIN;

-- 1. Xavfsiz tranzaksiya: Mijoz to'lovini bank hisobidan yechish
UPDATE bank_hisoblari_core 
SET nomi = nomi -- Qatorni qulflash
WHERE id = 101;

INSERT INTO jurnal_provodkalar (tranzaksiya_id, debet_hisob_id, kredit_hisob_id, summa)
VALUES ('f47ac10b-58cc-4372-a567-0e02b2c3d479', 101, 202, 2400000.00);

-- 2. E-tijorat buyurtmasini tasdiqlash
INSERT INTO buyurtmalar_ecom (id, mijoz_id, holat, umumiy_summa)
VALUES (9999, 101, 'TOLANDI', 2400000.00);

-- 3. AI Semantik Tavsiya: Xarid qilingan mahsulotga o'xshash tovarlarni topish
WITH tavsiya_tovarlar AS (
    SELECT id, hujjat_matni, (embedding <=> '[0.85, 0.15, 0.10]'::vector(3)) AS masofa
    FROM ai_hujjatlar_vektor
    ORDER BY embedding <=> '[0.85, 0.15, 0.10]'::vector(3)
    LIMIT 1
)
INSERT INTO tavsiyalar_log (mijoz_id, tavsiya_matni, sana)
SELECT 101, 'Sizga ushbu tovar ham yoqishi mumkin: ' || hujjat_matni, NOW()
FROM tavsiya_tovarlar;

COMMIT;

-- Yakuniy tekshirish
SELECT 
    '1000 ta SQL professional topshiriq muvaffaqiyatli yakunlandi!' AS bayonot,
    b.id AS buyurtma_id,
    b.holat,
    b.umumiy_summa
FROM buyurtmalar_ecom b
WHERE b.id = 9999;""",
    "Ushbu yakuniy 1,000-topshiriq butun SQL kursi davomida o'rganilgan barcha sohalarni birlashtiradi: relyatsion DDL/DML, tranzaksiyalar atomarligi (ACID), moliyaviy buxgalteriya yaxlitligi, e-tijorat holatlar mashinasi va eng zamonaviy pgvector sun'iy intellekt semantik tavsiya algoritmlari yagona uyg'unlikda ishga tushirildi.",
    """                           bayonot                            | buyurtma_id |  holat  | umumiy_summa 
--------------------------------------------------------------+-------------+---------+--------------
 1000 ta SQL professional topshiriq muvaffaqiyatli yakunlandi!|        9999 | TOLANDI |   2400000.00
(1 row)"""
)

if __name__ == "__main__":
    save_file("sql_20_amaliy_korporativ_baza_va_ai_vector_db.md", tasks)
