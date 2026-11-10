import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

# List of 50 tasks for File 15: 701 - 750
# Indekslar va so'rovlarni optimallashtirish (B-Tree, Hash, GIN, GiST, BRIN, Partial, Expression, Covering/INCLUDE, EXPLAIN ANALYZE, BUFFERS, SARGability, CONCURRENTLY)

index_data = [
    (
        701,
        "Standart B-Tree indeksi yaratish (CREATE INDEX)",
        "Foydalanuvchilarning elektron pochta ustuniga tezkor qidiruv uchun B-Tree indeksini yarating.",
        """CREATE TABLE foydalanuvchilar_idx (
    id SERIAL PRIMARY KEY,
    ism VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    yaratilgan_sana TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_foydalanuvchi_email ON foydalanuvchilar_idx (email);""",
        "'B-Tree' (Balanced Tree) relying RDBMS larida sukut bo'yicha indeks turidir. U ma'lumotlarni saralangan holda ko'p darajali daraxt sifatida saqlaydi. Tenglik (`=`) va oraliq (`<`, `<=`, `>`, `>=`, `BETWEEN`) so'rovlarini O(N) chiziqli qidiruvdan O(log N) logarifmik tezlikka tushiradi.",
        """CREATE TABLE
CREATE INDEX
Query returned successfully in 34 msec."""
    ),
    (
        702,
        "Yagona qiymatli B-Tree indeks: UNIQUE INDEX",
        "Tizimda takroriy telefon raqamlari kiritilishini taqiqlovchi va qidiruvni tezlashtiruvchi UNIQUE indeks yarating.",
        """ALTER TABLE foydalanuvchilar_idx ADD COLUMN telefon VARCHAR(20);

CREATE UNIQUE INDEX uq_idx_telefon ON foydalanuvchilar_idx (telefon);""",
        "'UNIQUE INDEX' bir vaqtning o'zida ikkita muhim vazifani bajaradi: ma'lumotlar butunligini (yagonaligini) nazorat qiladi va qidiruvni maksimal tezlashtiradi.",
        """ALTER TABLE
CREATE INDEX
Query returned successfully in 28 msec."""
    ),
    (
        703,
        "Ko'p ustunli kompozit indeks (Composite Index)",
        "Xodimlarning familiyasi va ismi bo'yicha birgalikda qidiruvchi ko'p ustunli indeks yarating.",
        """CREATE TABLE xodimlar_comp (
    id SERIAL PRIMARY KEY,
    familiya VARCHAR(50),
    ism VARCHAR(50),
    lavozim VARCHAR(50)
);

CREATE INDEX idx_xodim_fam_ism ON xodimlar_comp (familiya, ism);""",
        "Kompozit indeks bir nechta ustunlar kombinatsiyasi bo'yicha saralangan bitta daraxt tuzadi. `WHERE familiya = 'Aliyev' AND ism = 'Vali'` yoki faqat `WHERE familiya = 'Aliyev'` so'rovlarida juda tez ishlaydi.",
        """CREATE TABLE
CREATE INDEX
Query returned successfully in 31 msec."""
    ),
    (
        704,
        "Leftmost Prefix qoidasi (Kompozit indeks cheklovi)",
        "Nega `(familiya, ism)` indeksi faqat `WHERE ism = 'Vali'` so'rovida ishlamasligini ko'rsating.",
        """SELECT 'Kompozit indeks telefon kitobiga o‘xshaydi: familiyasiz faqat ism bo‘yicha tartibli izlab bo‘lmaydi' AS qoida;""",
        "Leftmost Prefix qoidasiga ko'ra, kompozit indeksdan foydalanish uchun so'rov indeksdagi birinchi (eng chapdagi) ustunni o'z ichiga olishi shart. Agar birinchi ustun tashlab ketilsa, RDBMS indeksdan to'liq foydalana olmaydi.",
        """                                                 qoida                                                 
-------------------------------------------------------------------------------------------------------
 Kompozit indeks telefon kitobiga o‘xshaydi: familiyasiz faqat ism bo‘yicha tartibli izlab bo‘lmaydi
(1 row)"""
    ),
    (
        705,
        "Qisman (Shartli) indeks: Partial Index",
        "Millionlab buyurtmalardan faqat 'bekor_qilingan' (kam sonli) holatdagilar uchun diskni tejovchi qisman indeks yarating.",
        """CREATE TABLE buyurtmalar_part (
    id BIGSERIAL PRIMARY KEY,
    mijoz_id INT,
    holat VARCHAR(20),
    summa NUMERIC(12, 2)
);

CREATE INDEX idx_bekor_qilinganlar ON buyurtmalar_part (mijoz_id) 
WHERE (holat = 'bekor_qilindi');""",
        "'Partial Index' butun jadvalni emas, faqat WHERE shartiga mos keluvchi qatorlarnigina indekslaydi. Agar 95% buyurtma 'bajarildi' bo'lsa, ularni indekslamasdan faqat 5% muammoli holatlarni indekslash indeks hajmini 90% ga qisqartiradi va xotirani tejaydi.",
        """CREATE TABLE
CREATE INDEX
Query returned successfully in 32 msec."""
    ),
    (
        706,
        "Ifodali (Funksional) indeks: Expression / Function-based Index",
        "Katta-kichik harflaridan qat'i nazar qidiruv (`WHERE LOWER(email) = ...`) tez ishlashi uchun indeks tuzing.",
        """CREATE INDEX idx_pastki_email ON foydalanuvchilar_idx (LOWER(email));""",
        "Odatda `WHERE LOWER(email) = 'ali@mail.uz'` yozilganda oddiy B-Tree indeks ishlamaydi. 'LOWER(email)' ifodasi bo'yicha qurilgan indeks esa qiymatlarni kichik harfga o'tkazib indekslaydi va qidiruvni Index Scanga aylantiradi.",
        """CREATE INDEX
Query returned successfully in 29 msec."""
    ),
    (
        707,
        "Qamrab oluvchi indeks: Covering Index (INCLUDE bandi)",
        "Index-Only Scan ga erishish uchun qo'shimcha ustunlarni daraxtning barg tugunlariga (INCLUDE) qo'shing.",
        """CREATE INDEX idx_user_id_include ON foydalanuvchilar_idx (id) INCLUDE (ism, email);""",
        "'INCLUDE' kalit so'zi ko'rsatilgan ustunlarni indeksning kaliti sifatida emas (saralashda qatnashmaydi), balki daraxtning eng quyi barglariga (leaf nodes) shunchaki qo'shimcha ma'lumot sifatida biriktiradi. Baza jadvalning o'ziga bormasdan (Heap Fetch siz) barcha kerakli ma'lumotni indeksning o'zidan oladi (Index-Only Scan).",
        """CREATE INDEX
Query returned successfully in 35 msec."""
    ),
    (
        708,
        "Faqat tenglik uchun Hash indeksi: HASH Index",
        "UUID yoki uzun satrlarni faqat aniq tenglik (`=`) bo'yicha o'ta tez topuvchi Hash indeksini yarating.",
        """CREATE INDEX idx_hash_token ON foydalanuvchilar_idx USING HASH (email);""",
        "'HASH' indeksi B-Tree dan farqli ravishda daraxt emas, 32-bitli xesh-jadval tuzadi. U faqat `=` tenglik operatorini qo'llab-quvvatlaydi (`<`, `>` ishlamaydi). PostgreSQL 10+ da to'liq WAL bilan himoyalangan va juda kam joy oladi.",
        """CREATE INDEX
Query returned successfully in 27 msec."""
    ),
    (
        709,
        "Massivlar va to'liq matn uchun GIN indeksi (Generalized Inverted Index)",
        "PostgreSQL massiv ustunidagi elementlarni ichidan tezkor izlash uchun GIN indeksini qo'llang.",
        """CREATE TABLE maqolalar_gin (
    id SERIAL PRIMARY KEY,
    sarlavha TEXT,
    teglar TEXT[]
);

CREATE INDEX idx_gin_teglar ON maqolalar_gin USING GIN (teglar);""",
        "'GIN' (Inverted Index) kitoblar oxiridagi ko'rsatkichga o'xshaydi: har bir element (so'z yoki teg) alohida ajratilib, u qaysi qatorlarda uchrashi ro'yxati saqlanadi. `WHERE teglar @> ARRAY['sql']` kabi so'rovlarni bir zumda topadi.",
        """CREATE TABLE
CREATE INDEX
Query returned successfully in 41 msec."""
    ),
    (
        710,
        "Oraliqlar va geometriya uchun GiST indeksi (Generalized Search Tree)",
        "Vaqt oraliqlari (TSRANGE) yoki GPS koordinatalari uchun GiST indeksini yarating.",
        """CREATE TABLE xonalar_gist (
    xona_id INT,
    band_vaqti TSRANGE
);

CREATE INDEX idx_gist_vaqt ON xonalar_gist USING GIST (band_vaqti);""",
        "'GiST' daraxtsimon ixtisoslashgan indeks bo'lib, kesishish (`&&`), o'z ichiga olish (`@>`) va masofa hisoblash amallarini qo'llab-quvvatlaydi. Bron qilish va GIS kartografiyada tengsizdir.",
        """CREATE TABLE
CREATE INDEX
Query returned successfully in 36 msec."""
    ),
    (
        711,
        "Ulkan jadvallar uchun BRIN indeksi (Block Range Index)",
        "Milliardlab qatorli vaqt jurnallari (logs) uchun B-Tree dan 100 barobar kam joy oluvchi BRIN indeksini qo'llang.",
        """CREATE TABLE tizim_audit_katta (
    id BIGSERIAL,
    vaqt TIMESTAMPTZ,
    xabar TEXT
);

CREATE INDEX idx_brin_vaqt ON tizim_audit_katta USING BRIN (vaqt);""",
        "'BRIN' har bir ma'lumot bloklari guruhi (odatda har 128 sahifa) uchun faqatgina MIN va MAX qiymatlarni saqlaydi. Agar ma'lumotlar ketma-ket kiritilsa (vaqt bo'yicha), BRIN indeksi deyarli nol megabayt joy olgan holda ajoyib tezlik beradi.",
        """CREATE TABLE
CREATE INDEX
Query returned successfully in 29 msec."""
    ),
    (
        712,
        "So'rov rejasini ko'rish: EXPLAIN asoslari",
        "So'rovni bajarmasdan faqat uning rejasini (Execution Plan) ko'rish.",
        """EXPLAIN SELECT * FROM foydalanuvchilar_idx WHERE email = 'test@mail.uz';""",
        "'EXPLAIN' optimizator so'rovni qanday bajarish niyatida ekanligini, qaysi indeksni tanlaganini va taxminiy narxni (Cost: startup..total) ko'rsatadi. So'rov diskda bajarilmaydi.",
        """                                     QUERY PLAN                                     
------------------------------------------------------------------------------------
 Bitmap Heap Scan on foydalanuvchilar_idx  (cost=4.14..12.55 rows=1 width=58)
   Recheck Cond: ((email)::text = 'test@mail.uz'::text)
   ->  Bitmap Index Scan on idx_foydalanuvchi_email  (cost=0.00..4.14 rows=1 width=0)
         Index Cond: ((email)::text = 'test@mail.uz'::text)
(4 rows)"""
    ),
    (
        713,
        "Haqiqiy bajarilish tahlili: EXPLAIN ANALYZE",
        "So'rovni haqiqatda bajarib, aniq sarflangan millisekundlar va qatorlar sonini ko'ring.",
        """EXPLAIN ANALYZE SELECT * FROM foydalanuvchilar_idx WHERE email = 'test@mail.uz';""",
        "'EXPLAIN ANALYZE' so'rovni real serverda bajaradi va 'actual time=... rows=... loops=...' orqali taxmin bilan haqiqat o'rtasidagi farqni millisekundlarda ko'rsatadi.",
        """                                                    QUERY PLAN                                                    
------------------------------------------------------------------------------------------------------------------
 Bitmap Heap Scan on foydalanuvchilar_idx  (cost=4.14..12.55 rows=1 width=58) (actual time=0.012..0.012 rows=0 loops=1)
   Recheck Cond: ((email)::text = 'test@mail.uz'::text)
   ->  Bitmap Index Scan on idx_foydalanuvchi_email  (cost=0.00..4.14 rows=1 width=0) (actual time=0.008..0.008 rows=0 loops=1)
 Planning Time: 0.085 ms
 Execution Time: 0.035 ms
(5 rows)"""
    ),
    (
        714,
        "RAM buferlari tahlili: EXPLAIN (ANALYZE, BUFFERS)",
        "So'rov diskdan qancha sahifa o'qiganini (read) va xotiradan qancha olganini (hit) ko'rish.",
        """EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM foydalanuvchilar_idx;""",
        "'BUFFERS' parametri 'shared hit' (RAM buffer pooledagi sahifalar) va 'read' (diskdan o'qilgan sahifalar) ni ko'rsatadi. Baza optimallashtirishda eng muhim ko'rsatkich 'shared hit' ulushini oshirishdir.",
        """                                               QUERY PLAN                                               
--------------------------------------------------------------------------------------------------------
 Seq Scan on foydalanuvchilar_idx  (cost=0.00..1.00 rows=1 width=58) (actual time=0.005..0.005 rows=0 loops=1)
   Buffers: shared hit=1
 Planning:
   Buffers: shared hit=2
 Planning Time: 0.052 ms
 Execution Time: 0.018 ms
(6 rows)"""
    ),
    (
        715,
        "Ketma-ket to'liq skanerlash: Sequential Scan (Seq Scan)",
        "Jadvalda indeks bo'lmaganda yoki butun jadval kerak bo'lganda Seq Scan xatti-harakati.",
        """SELECT 'Seq Scan: Jadvalning barcha sahifalari boshidan oxirigacha o‘qib chiqiladi. Kichik jadvallarda bu indeksdan ham tezroq' AS izoh;""",
        "Agar jadval kichik bo'lsa (bir necha sahifa), B-Tree daraxtini o'qish ortiqcha yuk hisoblanadi. Optimizator bunday paytda indeks bo'lsa ham qasddan Seq Scanni tanlaydi.",
        """                                                       izoh                                                        
-------------------------------------------------------------------------------------------------------------------
 Seq Scan: Jadvalning barcha sahifalari boshidan oxirigacha o‘qib chiqiladi. Kichik jadvallarda bu indeksdan ham tezroq
(1 row)"""
    ),
    (
        716,
        "Indeks bo'yicha to'g'ridan-to'g'ri skanerlash: Index Scan",
        "Indeks daraxti bo'ylab qidirib, so'ng diskdagi qatorni (Heap Tuple) o'qish mexanizmi.",
        """SELECT 'Index Scan: B-Tree daraxti orqali qatorning ctid manzili topiladi, so‘ng asosiy jadvaldan qator o‘qiladi' AS mexanizm;""",
        "Index Scan kam sonli (1-5%) qatorlarni qidirganda eng yuqori unumdorlikni taqdim etadi.",
        """                                                       mexanizm                                                        
-----------------------------------------------------------------------------------------------------------------------
 Index Scan: B-Tree daraxti orqali qatorning ctid manzili topiladi, so‘ng asosiy jadvaldan qator o‘qiladi
(1 row)"""
    ),
    (
        717,
        "Ideal skanerlash: Index Only Scan",
        "Jadvalning o'ziga umuman bormasdan, barcha ma'lumotni indeksdan olish holati.",
        """EXPLAIN SELECT email FROM foydalanuvchilar_idx WHERE email = 'test@mail.uz';""",
        "'Index Only Scan' - so'ralgan barcha ustunlar indeksning o'zida mavjud bo'lganda (va sahifa Visibility Map da toza bo'lsa) ro'y beradi. Bu relyatsion bazadagi eng tezkor o'qish rejimidir.",
        """                                           QUERY PLAN                                            
-------------------------------------------------------------------------------------------------
 Index Only Scan using idx_foydalanuvchi_email on foydalanuvchilar_idx  (cost=0.15..8.17 rows=1 width=32)
   Index Cond: (email = 'test@mail.uz'::text)
(2 rows)"""
    ),
    (
        718,
        "Bit kartali skanerlash: Bitmap Index Scan va Bitmap Heap Scan",
        "Baza bir nechta qatorlarni topishda nima uchun Bitmap Scan dan foydalanishini tushuntiring.",
        """SELECT 'Bitmap Scan: Indeksdan mos sahifalar xaritasi (Bitmap) tuziladi, so‘ng diskdan ketma-ket tartibda (Sequential I/O) o‘qiladi' AS tahlil;""",
        "Agar so'rov jadvalning 10-20% qismini qaytarsa, oddiy Index Scan disk boshchasini pala-partish harakatlantirishi (random I/O) mumkin. Bitmap Scan esa sahifalar raqamini saralab olib, diskdan tartibli o'qiydi.",
        """                                                              tahlil                                                              
----------------------------------------------------------------------------------------------------------------------------------
 Bitmap Scan: Indeksdan mos sahifalar xaritasi (Bitmap) tuziladi, so‘ng diskdan ketma-ket tartibda (Sequential I/O) o‘qiladi
(1 row)"""
    ),
    (
        719,
        "Bir nechta indekslarni birlashtirish: BitmapAnd / BitmapOr",
        "Alohida ikkita indeks mavjud bo'lganda PostgreSQL ularni bir vaqtda qanday ishlatishini ko'ring.",
        """SELECT 'PostgreSQL ikkita mustaqil indeksni xotirada BitmapAnd orqali birlashtirib kompozit indekssiz ham tezkor ishlay oladi' AS afzallik;""",
        "Agar `(a)` va `(b)` alohida indekslangan bo'lsa, `WHERE a = 1 AND b = 2` so'rovida PostgreSQL ikkala indeksni BitmapIndexScan qilib, xotirada ularning mantiqiy AND kesishmasini oladi.",
        """                                                          afzallik                                                           
-----------------------------------------------------------------------------------------------------------------------------
 PostgreSQL ikkita mustaqil indeksni xotirada BitmapAnd orqali birlashtirib kompozit indekssiz ham tezkor ishlay oladi
(1 row)"""
    ),
    (
        720,
        "SARGability muammosi: Matn boshidagi % belgisi",
        "Nega `LIKE '%test'` indeksni ishlatmasligi va `LIKE 'test%'` esa Index Scan qilishini ko'rsating.",
        """SELECT 'LIKE ''%abc'' alifbo boshidan qidirish imkonini bermaydi, shu bois B-Tree ishlamaydi. Faqat ''abc%'' SARGable hisoblanadi' AS qoida;""",
        "B-Tree indeksi so'zning boshiga qarab saralangan. Agar boshida noma'lumlik (`%`) bo'lsa, butun daraxtni tekshirib chiqishga majbur bo'ladi.",
        """                                                     qoida                                                     
---------------------------------------------------------------------------------------------------------------
 LIKE '%abc' alifbo boshidan qidirish imkonini bermaydi, shu bois B-Tree ishlamaydi. Faqat 'abc%' SARGable hisoblanadi
(1 row)"""
    ),
    (
        721,
        "SARGability: Sana ustunlarida noto'g'ri formulalar",
        "`WHERE sana::DATE = '2026-05-01'` o'rniga SARGable to'g'ri oraliq yozish.",
        """-- Indeksni o'ldiruvchi so'rov:
-- WHERE DATE(yaratilgan_sana) = '2026-05-01'

-- SARGable ideal so'rov:
EXPLAIN SELECT * FROM foydalanuvchilar_idx 
WHERE yaratilgan_sana >= '2026-05-01' AND yaratilgan_sana < '2026-05-02';""",
        "Ustunni funksiyaga o'ramasdan oraliq (`>=` va `<`) bilan yozish B-Tree indeksidan to'liq foydalanishni kafolatlaydi.",
        """                                  QUERY PLAN                                  
------------------------------------------------------------------------------
 Seq Scan on foydalanuvchilar_idx  (cost=0.00..1.02 rows=1 width=58)
   Filter: ((yaratilgan_sana >= '...'::timestamptz) AND (yaratilgan_sana < '...'::timestamptz))
(2 rows)"""
    ),
    (
        722,
        "Jadvalni bloklamasdan jonli indeks qurish: CREATE INDEX CONCURRENTLY",
        "Ishlab turgan yirik korporativ bazada o'qish va yozishni to'xtatmasdan indeks yaratish buyrug'i.",
        """CREATE INDEX CONCURRENTLY idx_conc_ism ON foydalanuvchilar_idx (ism);""",
        "Oddiy `CREATE INDEX` jadvalga SHARE LOCK qo'yadi va barcha INSERT, UPDATE, DELETE larni to'xtatib qo'yadi. 'CONCURRENTLY' esa ikki bosqichda jadvalni qulflamasdan orqa fonda indeks quradi. Production muhitida yagona to'g'ri yo'l.",
        """CREATE INDEX
Query returned successfully in 42 msec."""
    ),
    (
        723,
        "Buzilgan yoki eskirgan indeksni qayta qurish: REINDEX",
        "Jadval indekslarini shishib ketishdan (bloat) tozalash va qayta tiklash.",
        """REINDEX TABLE CONCURRENTLY foydalanuvchilar_idx;""",
        "'REINDEX TABLE' barcha indekslarni noldan qayta tuzadi. 'CONCURRENTLY' qo'shilsa bu jarayon o'qish va yozishni to'xtatmasdan bajariladi.",
        """REINDEX
Query returned successfully in 55 msec."""
    ),
    (
        724,
        "Indekslarning diskdagi hajmini aniqlash",
        "Qaysi indekslar diskda eng ko'p joy olayotganini pg_relation_size bilan aniqlang.",
        """SELECT 
    indexname, 
    pg_size_pretty(pg_relation_size(quote_ident(indexname)::regclass)) AS indeks_hajmi
FROM pg_indexes 
WHERE tablename = 'foydalanuvchilar_idx';""",
        "Katta hajmli va keraksiz indekslar xotirani behuda band qiladi va yozish amallarini sekinlashtiradi.",
        """       indexname         | indeks_hajmi 
--------------------------+--------------
 foydalanuvchilar_idx_pkey| 16 kB
 idx_foydalanuvchi_email  | 16 kB
 uq_idx_telefon           | 16 kB
 idx_pastki_email         | 16 kB
 idx_user_id_include      | 16 kB
 idx_hash_token           | 16 kB
 idx_conc_ism             | 16 kB
(7 rows)"""
    ),
    (
        725,
        "Ishlatilmayotgan (keraksiz) indekslarni topish: pg_stat_user_indexes",
        "Bazadagi qaysi indekslar hech qachon so'rovlarda ishlatilmaganini aniqlash.",
        """SELECT 
    relname AS jadval,
    indexrelname AS indeks,
    idx_scan AS skanerlashlar_soni
FROM pg_stat_user_indexes
WHERE schemaname = 'public' AND idx_scan = 0;""",
        "Agar 'idx_scan = 0' bo'lsa, demak bu indeks yaratilganidan beri birorta ham so'rov unga kirmagan! Bunday indekslar faqatgina INSERT/UPDATE ni sekinlashtiradi va ularni o'chirish (DROP) tavsiya etiladi.",
        """       jadval       |         indeks          | skanerlashlar_soni 
--------------------+-------------------------+--------------------
 foydalanuvchilar_idx| idx_foydalanuvchi_email |                  0
 foydalanuvchilar_idx| uq_idx_telefon          |                  0
(2 rows)"""
    ),
    (
        726,
        "Baza statistikasini qo'lda yangilash: ANALYZE",
        "Optimizator to'g'ri reja tanlashi uchun jadval ma'lumotlar taqsimoti statistikasini yangilang.",
        """ANALYZE foydalanuvchilar_idx;""",
        "'ANALYZE' jadvaldan tasodifiy qatorlar namunalarini olib, 'pg_statistic' katalogiga histogrammalar va chastotalarni yozadi. Optimizator qaysi indeksni tanlashni aynan shu statistikaga qarab hal qiladi.",
        """ANALYZE
Query returned successfully in 18 msec."""
    ),
    (
        727,
        "Saralash yo'nalishi bilan indeks yaratish: DESC NULLS LAST",
        "Maxsus saralash talablariga mos keluvchi yo'naltirilgan B-Tree indeksini yarating.",
        """CREATE INDEX idx_user_vaqt_desc ON foydalanuvchilar_idx (yaratilgan_sana DESC NULLS LAST);""",
        "B-Tree ikki tomonlama o'qilsa-da, 'NULLS LAST' va 'DESC' bilan yaratilgan indeks murakkab ko'p ustunli saralashlarda vaqtincha xotirada saralash (Sort operatori) xarajatini 0 ga tushiradi.",
        """CREATE INDEX
Query returned successfully in 28 msec."""
    ),
    (
        728,
        "Trigram (pg_trgm) indeksi bilan satr o'rtasidagi LIKE qidiruvini tezlashtirish",
        "`LIKE '%so''z%'` so'rovlarini 100 barobarga tezlashtiruvchi GIN Trigram indeksini yarating.",
        """CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX idx_trgm_ism ON foydalanuvchilar_idx USING GIN (ism gin_trgm_ops);""",
        "'pg_trgm' so'zlarni 3 harfli bo'laklarga (trigrammalarga) ajratadi. GIN indeksi bilan birikib, u hattoki boshida '%' bo'lgan `LIKE '%ali%'` so'rovlarini ham Index Scan rejasida chaqmoqdek tez topadi.",
        """CREATE EXTENSION
CREATE INDEX
Query returned successfully in 45 msec."""
    ),
    (
        729,
        "Indeks selektivligi (Index Selectivity) tushunchasi",
        "Nega BOOLEAN ustunga (jinsi, faolligi) oddiy B-Tree indeks qo'yish samarasiz ekanligini tushuntiring.",
        """SELECT 'Past selektivlik (faqat 2 xil qiymat bor ustun) da B-Tree ishlamaydi, optimizator baribir Seq Scan tanlaydi' AS qoida;""",
        "Selektivlik: unikal qiymatlar sonining umumiy qatorlarga nisbati. Agar ustunda faqat 'true' va 'false' bo'lsa, selektivlik past bo'ladi va indeks foyda bermaydi (faqat qisman indeks 'WHERE faol = true' foyda berishi mumkin).",
        """                                                       qoida                                                        
--------------------------------------------------------------------------------------------------------------------
 Past selektivlik (faqat 2 xil qiymat bor ustun) da B-Tree ishlamaydi, optimizator baribir Seq Scan tanlaydi
(1 row)"""
    ),
    (
        730,
        "EXPLAIN (ANALYZE, TIMING OFF) bilan yuklamani kamaytirish",
        "Juda katta so'rovlarda vaqt o'lchash protsessorga og'irlik qilmasligi uchun faqat qatorlar sonini tekshirish.",
        """EXPLAIN (ANALYZE, TIMING OFF) SELECT * FROM foydalanuvchilar_idx;""",
        "'TIMING OFF' protsessorning soat sikllarini o'lchash xarajatlarini (gettimeofday overhead) olib tashlaydi, bu yirik so'rovlarni xavfsiz tahlil qilish imkonini beradi.",
        """                                        QUERY PLAN                                         
-------------------------------------------------------------------------------------------
 Seq Scan on foydalanuvchilar_idx  (cost=0.00..1.00 rows=1 width=58) (rows=0 loops=1)
 Planning Time: 0.048 ms
 Execution Time: 0.015 ms
(3 rows)"""
    ),
    (
        731,
        "Indekslarning yozish tezligiga ta'siri (DML Overhead)",
        "Jadvalda 10 ta indeks bo'lsa INSERT va UPDATE nima uchun sekinlashishini ko'rsating.",
        """SELECT 'Har bir yangi INSERT barcha 10 ta indeks daraxtini yangilashni talab qiladi, bu yozishni 5-10 marta sekinlashtiradi' AS ogohlantirish;""",
        "Indekslar o'qishni (SELECT) tezlashtiradi, lekin yozishni (INSERT, UPDATE, DELETE) sekinlashtiradi. Har bir jadvalda faqat haqiqatda kerakli indekslar bo'lishi shart.",
        """                                                         ogohlantirish                                                          
--------------------------------------------------------------------------------------------------------------------------------
 Har bir yangi INSERT barcha 10 ta indeks daraxtini yangilashni talab qiladi, bu yozishni 5-10 marta sekinlashtiradi
(1 row)"""
    ),
    (
        732,
        "HOT (Heap-Only Tuples) optimizatsiyasi",
        "UPDATE paytida indekslarni qayta yozmasdan sahifa ichida yangilash mexanizmi.",
        """SELECT 'Agar UPDATE qilingan ustun indekslanmagan bo‘lsa va sahifada joy bo‘lsa, HOT update indekslarga tegmasdan o‘ta tez bajariladi' AS tahlil;""",
        "PostgreSQL ning eng buyuk ixtirolaridan biri bo'lgan HOT (Heap-Only Tuples) faqat indekslanmagan ustunlar yangilanganda ishlaydi va indekslarni qayta qurish xarajatini 0 ga tushiradi.",
        """                                                                    tahlil                                                                    
-----------------------------------------------------------------------------------------------------------------------------------------------
 Agar UPDATE qilingan ustun indekslanmagan bo‘lsa va sahifada joy bo‘lsa, HOT update indekslarga tegmasdan o‘ta tez bajariladi
(1 row)"""
    ),
    (
        733,
        "Indeks parametrlarini sozlash: FILLFACTOR",
        "Tez-tez yangilanadigan indekslar uchun fillfactor=80 bilan joy qoldirish.",
        """CREATE INDEX idx_user_fill ON foydalanuvchilar_idx (id) WITH (fillfactor = 80);""",
        "Indeks B-Tree sahifalarida 20% bo'sh joy qoldirish sahifalarning ikkiga bo'linib ketishi (B-Tree page splits) oldini oladi.",
        """CREATE INDEX
Query returned successfully in 27 msec."""
    ),
    (
        734,
        "So'rov rejasini JSON formatida olish: EXPLAIN (FORMAT JSON)",
        "So'rov rejasini avtomatik tahlil qiluvchi vizual dasturlar uchun JSON formatida eksport qiling.",
        """EXPLAIN (FORMAT JSON) SELECT * FROM foydalanuvchilar_idx;""",
        "DBeaver, pgAdmin va veb-servislar rejani vizual diagramma sifatida chizish uchun JSON formatidan foydalanadi.",
        """             QUERY PLAN             
------------------------------------
 [                                 +
   {                               +
     "Plan": {                     +
       "Node Type": "Seq Scan",    +
       "Parallel Aware": false,    +
       "Async Aware": false,       +
       "Relation Name": "foydalanuvchilar_idx",+
       "Alias": "foydalanuvchilar_idx",+
       "Startup Cost": 0.00,       +
       "Total Cost": 1.00,         +
       "Plan Rows": 1,             +
       "Plan Width": 58            +
     }                             +
   }                               +
 ]
(1 row)"""
    ),
    (
        735,
        "Tengsizlik va oraliq so'rovlarda kompozit indeks ustunlari tartibi",
        "Nega tenglik ustuni oldinda, oraliq ustuni oxirida turishi kerakligini tushuntiring.",
        """SELECT 'Kompozit indeks qoidasi: Tenglik ustunlari (masalan: filial_id) birinchi, oraliq ustuni (sana) eng oxirida turishi shart' AS mezon;""",
        "Agar `(sana, filial_id)` qilinsa, sana bo'yicha oraliqqa tushgach, ikkinchi ustun bo'yicha binar qidiruv to'xtaydi. `(filial_id, sana)` tartibi esa ikkala ustunni ham 100% indeksga jalb qiladi.",
        """                                                          mezon                                                           
--------------------------------------------------------------------------------------------------------------------------
 Kompozit indeks qoidasi: Tenglik ustunlari (masalan: filial_id) birinchi, oraliq ustuni (sana) eng oxirida turishi shart
(1 row)"""
    ),
    (
        736,
        "Indekslangan ustun ustida arifmetika xatosi",
        "`WHERE narx * 1.1 > 10000` nega indeksdan foydalanmasligini va uni to'g'irlash usuli.",
        """-- Indeks ishlamaydi: WHERE narx * 1.1 > 10000;
-- Indeks to'liq ishlaydi:
-- WHERE narx > 10000 / 1.1;
SELECT 'Arifmetik amalni ustunga emas, konstantaga qo‘llash so‘rovni SARGable qiladi' AS yechim;""",
        "Matematik tenglamani shunday o'zgartirish kerakki, indekslangan ustun yolg'iz o'zi sof qolsin.",
        """                                        yechim                                        
--------------------------------------------------------------------------------------
 Arifmetik amalni ustunga emas, konstantaga qo‘llash so‘rovni SARGable qiladi
(1 row)"""
    ),
    (
        737,
        "Indeksni vaqtincha tekshirish: enable_seqscan parametri",
        "PostgreSQL ni qasddan indeks ishlatishga majburlash orqali rejani solishtirish.",
        """SET enable_seqscan = OFF;
EXPLAIN SELECT * FROM foydalanuvchilar_idx;
SET enable_seqscan = ON;""",
        "'enable_seqscan = OFF' ishlab chiqarishda ishlatilmaydi, lekin test qilishda optimizator nima uchun Seq Scanni tanlaganini tushunish uchun ajoyib vositadir.",
        """SET
                                  QUERY PLAN                                  
------------------------------------------------------------------------------
 Seq Scan on foydalanuvchilar_idx  (cost=10000000000.00..10000000001.00 rows=1 width=58)
(1 row)
SET"""
    ),
    (
        738,
        "Parallel so'rovlar bajarilishi (Parallel Query)",
        "PostgreSQL bir nechta protsessor yadrolarini (Worker processes) jalb qilib jadvalni parallel skanerlashi.",
        """SELECT 'PostgreSQL katta jadvallarda avtomatik ravishda Parallel Seq Scan va Parallel Hash Join ishga tushiradi' AS parallelizm;""",
        "'max_parallel_workers_per_gather' parametri orqali bitta SQL so'rovini 4-8 ta protsessor yadrolarida baravar parallel hisoblash mumkin.",
        """                                                    parallelizm                                                     
--------------------------------------------------------------------------------------------------------------------
 PostgreSQL katta jadvallarda avtomatik ravishda Parallel Seq Scan va Parallel Hash Join ishga tushiradi
(1 row)"""
    ),
    (
        739,
        "JIT (Just-In-Time) kompilyatsiya tahlili",
        "EXPLAIN ANALYZE da 'JIT: Functions: ...' nima ekanligini tushuntiring.",
        """SELECT 'JIT kompilyatsiya (LLVM) murakkab ifodalar va agregatlarni to‘g‘ridan-to‘g‘ri mashina kodiga o‘girib tezlashtiradi' AS jit_info;""",
        "PostgreSQL 11+ da LLVM asosidagi JIT kompilyator mavjud. Og'ir analitik so'rovlarda u SQL ifodalarini protsessorning toza ikkilik ko'rsatmalariga aylantiradi.",
        """                                                        jit_info                                                        
------------------------------------------------------------------------------------------------------------------------
 JIT kompilyatsiya (LLVM) murakkab ifodalar va agregatlarni to‘g‘ridan-to‘g‘ri mashina kodiga o‘girib tezlashtiradi
(1 row)"""
    ),
    (
        740,
        "Kompakt qisman indeks bilan arxivni ajratish",
        "Faqat so'nggi 30 kunlik faol ma'lumotlarni indekslash.",
        """CREATE INDEX idx_songgi_faol ON buyurtmalar_part (mijoz_id) 
WHERE holat IN ('yangi', 'jarayonda');""",
        "Eski arxiv yozuvlari indeksdan chiqarib tashlanadi va kesh xotirasi maksimal tejaladi.",
        """CREATE INDEX
Query returned successfully in 28 msec."""
    ),
    (
        741,
        "Random Page Cost sozlamasi va SSD drayverlar",
        "SSD disklarda B-Tree indekslaridan foydalanishni rag'batlantirish uchun sozlamani o'zgartirish.",
        """SHOW random_page_cost;""",
        "Eski mexanik HDD larda 'random_page_cost = 4.0' bo'lgan. Zamonaviy NVMe SSD larda esa ixtiyoriy sahifani o'qish ketma-ket o'qish bilan deyarli bir xil tezlikda, shuning uchun bu qiymatni 1.1 ga tushirish tavsiya etiladi (bu indekslarni tanlashni oshiradi).",
        """ random_page_cost 
------------------
 4
(1 row)"""
    ),
    (
        742,
        "Indekslangan ustunda implicit type conversion (Yashirin tur o'zgarishi)",
        "VARCHAR ustunni butun son bilan solishtirganda indeks nega ishlamay qolishini ko'rsating.",
        """-- Agar telefon VARCHAR bo'lsa:
-- WHERE telefon = 998901234567; (Indeks ishlamaydi, chunki son matnga o'girilmaydi, ustun songa o'giriladi!)
-- WHERE telefon = '998901234567'; (Indeks to'liq ishlaydi)
SELECT 'Taqqoslanayotgan qiymat tipi ustun tipi bilan 100% mos bo‘lishi shart' AS qoida;""",
        "Dasturlash tilidan parametr yuborilganda tip xato bo'lsa, baza ustun ustida yashirin `CAST` bajaradi va bu B-Tree indeksini ishdan chiqaradi.",
        """                                 qoida                                 
-----------------------------------------------------------------------
 Taqqoslanayotgan qiymat tipi ustun tipi bilan 100% mos bo‘lishi shart
(1 row)"""
    ),
    (
        743,
        "Indeksda ma'lumotlar zichligi: pg_stat_all_indexes",
        "Indeks bloklari qanchalik tez-tez o'qilayotganini tahlil qilish.",
        """SELECT indexrelid, idx_blks_read, idx_blks_hit 
FROM pg_statio_user_indexes 
LIMIT 3;""",
        "Xotiradan o'qish (hit) va diskdan o'qish (read) balansi ko'rsatiladi.",
        """ indexrelid | idx_blks_read | idx_blks_hit 
------------+---------------+--------------
      16390 |             1 |            0
      16391 |             0 |            0
      16392 |             0 |            0
(3 rows)"""
    ),
    (
        744,
        "Ko'p ustunli saralashda indeksning to'liq mos kelishi",
        "`ORDER BY a ASC, b DESC` uchun aynan mos indeks tuzish.",
        """CREATE INDEX idx_a_asc_b_desc ON xodimlar_comp (familiya ASC, ism DESC);""",
        "Agar so'rovda bir ustun ASC, ikkinchisi DESC bo'lsa, indeks ham aynan shu yo'nalishlarda e'lon qilinishi xotiradagi 'Sort' operatsiyasini batamom yo'qotadi.",
        """CREATE INDEX
Query returned successfully in 27 msec."""
    ),
    (
        745,
        "Tizim jadvallarining indekslarini ko'rish",
        "Jadvalda qanday indekslar borligini qisqa so'rov bilan ko'rish.",
        """SELECT c.relname AS indeks_nomi
FROM pg_class c
JOIN pg_index i ON i.indexrelid = c.oid
WHERE i.indrelid = 'foydalanuvchilar_idx'::regclass;""",
        "Barcha ichki indekslar ro'yxati olinadi.",
        """        indeks_nomi        
---------------------------
 foydalanuvchilar_idx_pkey
 idx_foydalanuvchi_email
 uq_idx_telefon
 idx_pastki_email
 idx_user_id_include
 idx_hash_token
 idx_conc_ism
 idx_trgm_ism
 idx_user_fill
 idx_user_vaqt_desc
(10 rows)"""
    ),
    (
        746,
        "Jadval va indekslarni keshga yuklab qo'yish: pg_prewarm",
        "Server qayta yoqilganda keshni sovuq holatdan (Cold cache) issiq holatga (Warm cache) keltirish.",
        """CREATE EXTENSION IF NOT EXISTS pg_prewarm;

SELECT pg_prewarm('foydalanuvchilar_idx');""",
        "'pg_prewarm' kengaytmasi jadval yoki indeks sahifalarini server ishga tushishi bilanoq operativ xotiraga (Buffer Pool) yuklab beradi. Birinchi so'rovlar ham sekinlashmasdan ishlaydi.",
        """CREATE EXTENSION
 pg_prewarm 
------------
          1
(1 row)"""
    ),
    (
        747,
        "Indekslarning to'g'ri ishlashini tekshiruvchi amocms testi",
        "Indeks haqiqatan ishlayotganini qisqa vaqt ichida isbotlash.",
        """EXPLAIN SELECT id FROM foydalanuvchilar_idx WHERE id = 1;""",
        "Birlamchi kalit indeksi bo'yicha Index Scan ko'rsatiladi.",
        """                                          QUERY PLAN                                          
----------------------------------------------------------------------------------------------
 Index Only Scan using foydalanuvchilar_idx_pkey on foydalanuvchilar_idx  (cost=0.15..8.17 rows=1 width=4)
   Index Cond: (id = 1)
(2 rows)"""
    ),
    (
        748,
        "Expression indeksda DETERMINISTIC funksiya talabi",
        "Nega `CURRENT_DATE` yoki `RANDOM()` qatnashgan ifodalarga indeks qurib bo'lmasligini tushuntiring.",
        """SELECT 'Indeks ifodasi IMMUTABLE (o‘zgarmas natija beruvchi) bo‘lishi shart. Har kuni o‘zgaruvchi NOW() ga indeks qo‘yib bo‘lmaydi' AS qoida;""",
        "PostgreSQL faqat deterministik (IMMUTABLE) funksiyalarni indekslashga ruxsat beradi. Natijasi vaqtga qarab o'zgaruvchi funksiyalarni indekslab bo'lmaydi.",
        """                                                          qoida                                                           
--------------------------------------------------------------------------------------------------------------------------
 Indeks ifodasi IMMUTABLE (o‘zgarmas natija beruvchi) bo‘lishi shart. Har kuni o‘zgaruvchi NOW() ga indeks qo‘yib bo‘lmaydi
(1 row)"""
    ),
    (
        749,
        "B-Tree indekslarida deduplikatsiya (PostgreSQL 13+)",
        "Bir xil qiymatli kalitlar indeks hajmini oshirmasligi uchun B-Tree avtomatik deduplikatsiyasi.",
        """SELECT 'PostgreSQL 13 dan boshlab B-Tree indekslaridagi takroriy qiymatlar avtomatik siqiladi (Deduplication)' AS afzallik;""",
        "Takrorlanuvchi kalitlarga ega indekslar diskda 3 barobargacha kam joy egallaydi.",
        """                                                      afzallik                                                       
---------------------------------------------------------------------------------------------------------------------
 PostgreSQL 13 dan boshlab B-Tree indekslaridagi takroriy qiymatlar avtomatik siqiladi (Deduplication)
(1 row)"""
    ),
    (
        750,
        "Korporativ Optimallashtirish: FinTech Katta Ma'lumotlar Bazasida Indekslar Arxitekturasi",
        "Millionlab tranzaksiyalarga ega to'lov tizimida oylik qidiruv, hisob raqami bo'yicha izlash, status bo'yicha saralash va tezkor hisobotlar uchun B-Tree, Composite, Partial va Covering indekslarning to'liq optimal kompleksini yarating hamda EXPLAIN ANALYZE bilan isbotlang.",
        """CREATE TABLE korporativ_tranzaksiyalar (
    tr_id BIGSERIAL PRIMARY KEY,
    hisob_raqam VARCHAR(20) NOT NULL,
    valyuta CHAR(3) NOT NULL,
    summa NUMERIC(15, 2) NOT NULL,
    holat VARCHAR(20) NOT NULL,
    yaratilgan_vaqt TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 1. Qamrab oluvchi kompozit indeks (Hisob bo'yicha oxirgi amallarni Heap Fetch siz Index-Only Scan qilish):
CREATE INDEX idx_tr_hisob_vaqt ON korporativ_tranzaksiyalar (hisob_raqam, yaratilgan_vaqt DESC) 
INCLUDE (summa, valyuta);

-- 2. Qisman indeks: Faqatgina 'muammoli / kutilayotgan' tranzaksiyalarni nazorat qilish uchun (hajmi o'ta kichik):
CREATE INDEX idx_tr_muammoli ON korporativ_tranzaksiyalar (yaratilgan_vaqt ASC) 
WHERE (holat IN ('xato', 'tekshirilmoqda'));

-- 3. Valyuta bo'yicha tahliliy B-Tree indeksi:
CREATE INDEX idx_tr_valyuta ON korporativ_tranzaksiyalar (valyuta, summa);

-- Sinov ma'lumotlarini kiritish:
INSERT INTO korporativ_tranzaksiyalar (hisob_raqam, valyuta, summa, holat) VALUES 
('202080001001', 'UZS', 5000000, 'bajarildi'),
('202080001001', 'UZS', 1200000, 'bajarildi'),
('202080001002', 'USD', 500,     'tekshirilmoqda');

-- Statistikani yangilash:
ANALYZE korporativ_tranzaksiyalar;

-- Optimal so'rovni tahlil qilish (Index Only Scan isboti):
EXPLAIN ANALYZE 
SELECT hisob_raqam, summa, valyuta 
FROM korporativ_tranzaksiyalar 
WHERE hisob_raqam = '202080001001' 
ORDER BY yaratilgan_vaqt DESC 
LIMIT 5;""",
        "Ushbu korporativ arxitektura yuqori yuklamali (High-Load) to'lov tizimlarining standart yechimidir: qamrab oluvchi (Covering Index) orqali asosiy ma'lumotlar bloklariga kirmasdan Index-Only Scan ga erishiladi, qisman indeks (Partial Index) orqali kutilayotgan tranzaksiyalar bir zumda topiladi va server resurslari 90% ga tejaladi.",
        """CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE INDEX
INSERT 0 3
ANALYZE
                                                               QUERY PLAN                                                                
-----------------------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=0.15..8.17 rows=2 width=29) (actual time=0.015..0.016 rows=2 loops=1)
   ->  Index Only Scan using idx_tr_hisob_vaqt on korporativ_tranzaksiyalar  (cost=0.15..8.17 rows=2 width=29) (actual time=0.014..0.014 rows=2 loops=1)
         Index Cond: (hisob_raqam = '202080001001'::text)
         Heap Fetches: 0
 Planning Time: 0.120 ms
 Execution Time: 0.038 ms
(6 rows)"""
    )
]

formatted = [format_task(*item) for item in index_data]
save_file("sql_15_indekslar_va_sorovlarni_optimallashtirish.md", formatted)
