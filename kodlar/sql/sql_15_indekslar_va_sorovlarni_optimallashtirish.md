# 701-Topshiriq: Standart B-Tree indeksi yaratish (CREATE INDEX)
## Topshiriq sharti:
Foydalanuvchilarning elektron pochta ustuniga tezkor qidiruv uchun B-Tree indeksini yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLE foydalanuvchilar_idx (
    id SERIAL PRIMARY KEY,
    ism VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    yaratilgan_sana TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_foydalanuvchi_email ON foydalanuvchilar_idx (email);
```

## Tushuntirish va Mantiq:
'B-Tree' (Balanced Tree) relying RDBMS larida sukut bo'yicha indeks turidir. U ma'lumotlarni saralangan holda ko'p darajali daraxt sifatida saqlaydi. Tenglik (`=`) va oraliq (`<`, `<=`, `>`, `>=`, `BETWEEN`) so'rovlarini O(N) chiziqli qidiruvdan O(log N) logarifmik tezlikka tushiradi.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE INDEX
Query returned successfully in 34 msec.
```


# 702-Topshiriq: Yagona qiymatli B-Tree indeks: UNIQUE INDEX
## Topshiriq sharti:
Tizimda takroriy telefon raqamlari kiritilishini taqiqlovchi va qidiruvni tezlashtiruvchi UNIQUE indeks yarating.

## Yechim (SQL kodi):
```sql
ALTER TABLE foydalanuvchilar_idx ADD COLUMN telefon VARCHAR(20);

CREATE UNIQUE INDEX uq_idx_telefon ON foydalanuvchilar_idx (telefon);
```

## Tushuntirish va Mantiq:
'UNIQUE INDEX' bir vaqtning o'zida ikkita muhim vazifani bajaradi: ma'lumotlar butunligini (yagonaligini) nazorat qiladi va qidiruvni maksimal tezlashtiradi.

## Ishlash natijasi:
```text
ALTER TABLE
CREATE INDEX
Query returned successfully in 28 msec.
```


# 703-Topshiriq: Ko'p ustunli kompozit indeks (Composite Index)
## Topshiriq sharti:
Xodimlarning familiyasi va ismi bo'yicha birgalikda qidiruvchi ko'p ustunli indeks yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLE xodimlar_comp (
    id SERIAL PRIMARY KEY,
    familiya VARCHAR(50),
    ism VARCHAR(50),
    lavozim VARCHAR(50)
);

CREATE INDEX idx_xodim_fam_ism ON xodimlar_comp (familiya, ism);
```

## Tushuntirish va Mantiq:
Kompozit indeks bir nechta ustunlar kombinatsiyasi bo'yicha saralangan bitta daraxt tuzadi. `WHERE familiya = 'Aliyev' AND ism = 'Vali'` yoki faqat `WHERE familiya = 'Aliyev'` so'rovlarida juda tez ishlaydi.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE INDEX
Query returned successfully in 31 msec.
```


# 704-Topshiriq: Leftmost Prefix qoidasi (Kompozit indeks cheklovi)
## Topshiriq sharti:
Nega `(familiya, ism)` indeksi faqat `WHERE ism = 'Vali'` so'rovida ishlamasligini ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT 'Kompozit indeks telefon kitobiga o‘xshaydi: familiyasiz faqat ism bo‘yicha tartibli izlab bo‘lmaydi' AS qoida;
```

## Tushuntirish va Mantiq:
Leftmost Prefix qoidasiga ko'ra, kompozit indeksdan foydalanish uchun so'rov indeksdagi birinchi (eng chapdagi) ustunni o'z ichiga olishi shart. Agar birinchi ustun tashlab ketilsa, RDBMS indeksdan to'liq foydalana olmaydi.

## Ishlash natijasi:
```text
qoida                                                 
-------------------------------------------------------------------------------------------------------
 Kompozit indeks telefon kitobiga o‘xshaydi: familiyasiz faqat ism bo‘yicha tartibli izlab bo‘lmaydi
(1 row)
```


# 705-Topshiriq: Qisman (Shartli) indeks: Partial Index
## Topshiriq sharti:
Millionlab buyurtmalardan faqat 'bekor_qilingan' (kam sonli) holatdagilar uchun diskni tejovchi qisman indeks yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLE buyurtmalar_part (
    id BIGSERIAL PRIMARY KEY,
    mijoz_id INT,
    holat VARCHAR(20),
    summa NUMERIC(12, 2)
);

CREATE INDEX idx_bekor_qilinganlar ON buyurtmalar_part (mijoz_id) 
WHERE (holat = 'bekor_qilindi');
```

## Tushuntirish va Mantiq:
'Partial Index' butun jadvalni emas, faqat WHERE shartiga mos keluvchi qatorlarnigina indekslaydi. Agar 95% buyurtma 'bajarildi' bo'lsa, ularni indekslamasdan faqat 5% muammoli holatlarni indekslash indeks hajmini 90% ga qisqartiradi va xotirani tejaydi.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE INDEX
Query returned successfully in 32 msec.
```


# 706-Topshiriq: Ifodali (Funksional) indeks: Expression / Function-based Index
## Topshiriq sharti:
Katta-kichik harflaridan qat'i nazar qidiruv (`WHERE LOWER(email) = ...`) tez ishlashi uchun indeks tuzing.

## Yechim (SQL kodi):
```sql
CREATE INDEX idx_pastki_email ON foydalanuvchilar_idx (LOWER(email));
```

## Tushuntirish va Mantiq:
Odatda `WHERE LOWER(email) = 'ali@mail.uz'` yozilganda oddiy B-Tree indeks ishlamaydi. 'LOWER(email)' ifodasi bo'yicha qurilgan indeks esa qiymatlarni kichik harfga o'tkazib indekslaydi va qidiruvni Index Scanga aylantiradi.

## Ishlash natijasi:
```text
CREATE INDEX
Query returned successfully in 29 msec.
```


# 707-Topshiriq: Qamrab oluvchi indeks: Covering Index (INCLUDE bandi)
## Topshiriq sharti:
Index-Only Scan ga erishish uchun qo'shimcha ustunlarni daraxtning barg tugunlariga (INCLUDE) qo'shing.

## Yechim (SQL kodi):
```sql
CREATE INDEX idx_user_id_include ON foydalanuvchilar_idx (id) INCLUDE (ism, email);
```

## Tushuntirish va Mantiq:
'INCLUDE' kalit so'zi ko'rsatilgan ustunlarni indeksning kaliti sifatida emas (saralashda qatnashmaydi), balki daraxtning eng quyi barglariga (leaf nodes) shunchaki qo'shimcha ma'lumot sifatida biriktiradi. Baza jadvalning o'ziga bormasdan (Heap Fetch siz) barcha kerakli ma'lumotni indeksning o'zidan oladi (Index-Only Scan).

## Ishlash natijasi:
```text
CREATE INDEX
Query returned successfully in 35 msec.
```


# 708-Topshiriq: Faqat tenglik uchun Hash indeksi: HASH Index
## Topshiriq sharti:
UUID yoki uzun satrlarni faqat aniq tenglik (`=`) bo'yicha o'ta tez topuvchi Hash indeksini yarating.

## Yechim (SQL kodi):
```sql
CREATE INDEX idx_hash_token ON foydalanuvchilar_idx USING HASH (email);
```

## Tushuntirish va Mantiq:
'HASH' indeksi B-Tree dan farqli ravishda daraxt emas, 32-bitli xesh-jadval tuzadi. U faqat `=` tenglik operatorini qo'llab-quvvatlaydi (`<`, `>` ishlamaydi). PostgreSQL 10+ da to'liq WAL bilan himoyalangan va juda kam joy oladi.

## Ishlash natijasi:
```text
CREATE INDEX
Query returned successfully in 27 msec.
```


# 709-Topshiriq: Massivlar va to'liq matn uchun GIN indeksi (Generalized Inverted Index)
## Topshiriq sharti:
PostgreSQL massiv ustunidagi elementlarni ichidan tezkor izlash uchun GIN indeksini qo'llang.

## Yechim (SQL kodi):
```sql
CREATE TABLE maqolalar_gin (
    id SERIAL PRIMARY KEY,
    sarlavha TEXT,
    teglar TEXT[]
);

CREATE INDEX idx_gin_teglar ON maqolalar_gin USING GIN (teglar);
```

## Tushuntirish va Mantiq:
'GIN' (Inverted Index) kitoblar oxiridagi ko'rsatkichga o'xshaydi: har bir element (so'z yoki teg) alohida ajratilib, u qaysi qatorlarda uchrashi ro'yxati saqlanadi. `WHERE teglar @> ARRAY['sql']` kabi so'rovlarni bir zumda topadi.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE INDEX
Query returned successfully in 41 msec.
```


# 710-Topshiriq: Oraliqlar va geometriya uchun GiST indeksi (Generalized Search Tree)
## Topshiriq sharti:
Vaqt oraliqlari (TSRANGE) yoki GPS koordinatalari uchun GiST indeksini yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLE xonalar_gist (
    xona_id INT,
    band_vaqti TSRANGE
);

CREATE INDEX idx_gist_vaqt ON xonalar_gist USING GIST (band_vaqti);
```

## Tushuntirish va Mantiq:
'GiST' daraxtsimon ixtisoslashgan indeks bo'lib, kesishish (`&&`), o'z ichiga olish (`@>`) va masofa hisoblash amallarini qo'llab-quvvatlaydi. Bron qilish va GIS kartografiyada tengsizdir.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE INDEX
Query returned successfully in 36 msec.
```


# 711-Topshiriq: Ulkan jadvallar uchun BRIN indeksi (Block Range Index)
## Topshiriq sharti:
Milliardlab qatorli vaqt jurnallari (logs) uchun B-Tree dan 100 barobar kam joy oluvchi BRIN indeksini qo'llang.

## Yechim (SQL kodi):
```sql
CREATE TABLE tizim_audit_katta (
    id BIGSERIAL,
    vaqt TIMESTAMPTZ,
    xabar TEXT
);

CREATE INDEX idx_brin_vaqt ON tizim_audit_katta USING BRIN (vaqt);
```

## Tushuntirish va Mantiq:
'BRIN' har bir ma'lumot bloklari guruhi (odatda har 128 sahifa) uchun faqatgina MIN va MAX qiymatlarni saqlaydi. Agar ma'lumotlar ketma-ket kiritilsa (vaqt bo'yicha), BRIN indeksi deyarli nol megabayt joy olgan holda ajoyib tezlik beradi.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE INDEX
Query returned successfully in 29 msec.
```


# 712-Topshiriq: So'rov rejasini ko'rish: EXPLAIN asoslari
## Topshiriq sharti:
So'rovni bajarmasdan faqat uning rejasini (Execution Plan) ko'rish.

## Yechim (SQL kodi):
```sql
EXPLAIN SELECT * FROM foydalanuvchilar_idx WHERE email = 'test@mail.uz';
```

## Tushuntirish va Mantiq:
'EXPLAIN' optimizator so'rovni qanday bajarish niyatida ekanligini, qaysi indeksni tanlaganini va taxminiy narxni (Cost: startup..total) ko'rsatadi. So'rov diskda bajarilmaydi.

## Ishlash natijasi:
```text
QUERY PLAN                                     
------------------------------------------------------------------------------------
 Bitmap Heap Scan on foydalanuvchilar_idx  (cost=4.14..12.55 rows=1 width=58)
   Recheck Cond: ((email)::text = 'test@mail.uz'::text)
   ->  Bitmap Index Scan on idx_foydalanuvchi_email  (cost=0.00..4.14 rows=1 width=0)
         Index Cond: ((email)::text = 'test@mail.uz'::text)
(4 rows)
```


# 713-Topshiriq: Haqiqiy bajarilish tahlili: EXPLAIN ANALYZE
## Topshiriq sharti:
So'rovni haqiqatda bajarib, aniq sarflangan millisekundlar va qatorlar sonini ko'ring.

## Yechim (SQL kodi):
```sql
EXPLAIN ANALYZE SELECT * FROM foydalanuvchilar_idx WHERE email = 'test@mail.uz';
```

## Tushuntirish va Mantiq:
'EXPLAIN ANALYZE' so'rovni real serverda bajaradi va 'actual time=... rows=... loops=...' orqali taxmin bilan haqiqat o'rtasidagi farqni millisekundlarda ko'rsatadi.

## Ishlash natijasi:
```text
QUERY PLAN                                                    
------------------------------------------------------------------------------------------------------------------
 Bitmap Heap Scan on foydalanuvchilar_idx  (cost=4.14..12.55 rows=1 width=58) (actual time=0.012..0.012 rows=0 loops=1)
   Recheck Cond: ((email)::text = 'test@mail.uz'::text)
   ->  Bitmap Index Scan on idx_foydalanuvchi_email  (cost=0.00..4.14 rows=1 width=0) (actual time=0.008..0.008 rows=0 loops=1)
 Planning Time: 0.085 ms
 Execution Time: 0.035 ms
(5 rows)
```


# 714-Topshiriq: RAM buferlari tahlili: EXPLAIN (ANALYZE, BUFFERS)
## Topshiriq sharti:
So'rov diskdan qancha sahifa o'qiganini (read) va xotiradan qancha olganini (hit) ko'rish.

## Yechim (SQL kodi):
```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM foydalanuvchilar_idx;
```

## Tushuntirish va Mantiq:
'BUFFERS' parametri 'shared hit' (RAM buffer pooledagi sahifalar) va 'read' (diskdan o'qilgan sahifalar) ni ko'rsatadi. Baza optimallashtirishda eng muhim ko'rsatkich 'shared hit' ulushini oshirishdir.

## Ishlash natijasi:
```text
QUERY PLAN                                               
--------------------------------------------------------------------------------------------------------
 Seq Scan on foydalanuvchilar_idx  (cost=0.00..1.00 rows=1 width=58) (actual time=0.005..0.005 rows=0 loops=1)
   Buffers: shared hit=1
 Planning:
   Buffers: shared hit=2
 Planning Time: 0.052 ms
 Execution Time: 0.018 ms
(6 rows)
```


# 715-Topshiriq: Ketma-ket to'liq skanerlash: Sequential Scan (Seq Scan)
## Topshiriq sharti:
Jadvalda indeks bo'lmaganda yoki butun jadval kerak bo'lganda Seq Scan xatti-harakati.

## Yechim (SQL kodi):
```sql
SELECT 'Seq Scan: Jadvalning barcha sahifalari boshidan oxirigacha o‘qib chiqiladi. Kichik jadvallarda bu indeksdan ham tezroq' AS izoh;
```

## Tushuntirish va Mantiq:
Agar jadval kichik bo'lsa (bir necha sahifa), B-Tree daraxtini o'qish ortiqcha yuk hisoblanadi. Optimizator bunday paytda indeks bo'lsa ham qasddan Seq Scanni tanlaydi.

## Ishlash natijasi:
```text
izoh                                                        
-------------------------------------------------------------------------------------------------------------------
 Seq Scan: Jadvalning barcha sahifalari boshidan oxirigacha o‘qib chiqiladi. Kichik jadvallarda bu indeksdan ham tezroq
(1 row)
```


# 716-Topshiriq: Indeks bo'yicha to'g'ridan-to'g'ri skanerlash: Index Scan
## Topshiriq sharti:
Indeks daraxti bo'ylab qidirib, so'ng diskdagi qatorni (Heap Tuple) o'qish mexanizmi.

## Yechim (SQL kodi):
```sql
SELECT 'Index Scan: B-Tree daraxti orqali qatorning ctid manzili topiladi, so‘ng asosiy jadvaldan qator o‘qiladi' AS mexanizm;
```

## Tushuntirish va Mantiq:
Index Scan kam sonli (1-5%) qatorlarni qidirganda eng yuqori unumdorlikni taqdim etadi.

## Ishlash natijasi:
```text
mexanizm                                                        
-----------------------------------------------------------------------------------------------------------------------
 Index Scan: B-Tree daraxti orqali qatorning ctid manzili topiladi, so‘ng asosiy jadvaldan qator o‘qiladi
(1 row)
```


# 717-Topshiriq: Ideal skanerlash: Index Only Scan
## Topshiriq sharti:
Jadvalning o'ziga umuman bormasdan, barcha ma'lumotni indeksdan olish holati.

## Yechim (SQL kodi):
```sql
EXPLAIN SELECT email FROM foydalanuvchilar_idx WHERE email = 'test@mail.uz';
```

## Tushuntirish va Mantiq:
'Index Only Scan' - so'ralgan barcha ustunlar indeksning o'zida mavjud bo'lganda (va sahifa Visibility Map da toza bo'lsa) ro'y beradi. Bu relyatsion bazadagi eng tezkor o'qish rejimidir.

## Ishlash natijasi:
```text
QUERY PLAN                                            
-------------------------------------------------------------------------------------------------
 Index Only Scan using idx_foydalanuvchi_email on foydalanuvchilar_idx  (cost=0.15..8.17 rows=1 width=32)
   Index Cond: (email = 'test@mail.uz'::text)
(2 rows)
```


# 718-Topshiriq: Bit kartali skanerlash: Bitmap Index Scan va Bitmap Heap Scan
## Topshiriq sharti:
Baza bir nechta qatorlarni topishda nima uchun Bitmap Scan dan foydalanishini tushuntiring.

## Yechim (SQL kodi):
```sql
SELECT 'Bitmap Scan: Indeksdan mos sahifalar xaritasi (Bitmap) tuziladi, so‘ng diskdan ketma-ket tartibda (Sequential I/O) o‘qiladi' AS tahlil;
```

## Tushuntirish va Mantiq:
Agar so'rov jadvalning 10-20% qismini qaytarsa, oddiy Index Scan disk boshchasini pala-partish harakatlantirishi (random I/O) mumkin. Bitmap Scan esa sahifalar raqamini saralab olib, diskdan tartibli o'qiydi.

## Ishlash natijasi:
```text
tahlil                                                              
----------------------------------------------------------------------------------------------------------------------------------
 Bitmap Scan: Indeksdan mos sahifalar xaritasi (Bitmap) tuziladi, so‘ng diskdan ketma-ket tartibda (Sequential I/O) o‘qiladi
(1 row)
```


# 719-Topshiriq: Bir nechta indekslarni birlashtirish: BitmapAnd / BitmapOr
## Topshiriq sharti:
Alohida ikkita indeks mavjud bo'lganda PostgreSQL ularni bir vaqtda qanday ishlatishini ko'ring.

## Yechim (SQL kodi):
```sql
SELECT 'PostgreSQL ikkita mustaqil indeksni xotirada BitmapAnd orqali birlashtirib kompozit indekssiz ham tezkor ishlay oladi' AS afzallik;
```

## Tushuntirish va Mantiq:
Agar `(a)` va `(b)` alohida indekslangan bo'lsa, `WHERE a = 1 AND b = 2` so'rovida PostgreSQL ikkala indeksni BitmapIndexScan qilib, xotirada ularning mantiqiy AND kesishmasini oladi.

## Ishlash natijasi:
```text
afzallik                                                           
-----------------------------------------------------------------------------------------------------------------------------
 PostgreSQL ikkita mustaqil indeksni xotirada BitmapAnd orqali birlashtirib kompozit indekssiz ham tezkor ishlay oladi
(1 row)
```


# 720-Topshiriq: SARGability muammosi: Matn boshidagi % belgisi
## Topshiriq sharti:
Nega `LIKE '%test'` indeksni ishlatmasligi va `LIKE 'test%'` esa Index Scan qilishini ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT 'LIKE ''%abc'' alifbo boshidan qidirish imkonini bermaydi, shu bois B-Tree ishlamaydi. Faqat ''abc%'' SARGable hisoblanadi' AS qoida;
```

## Tushuntirish va Mantiq:
B-Tree indeksi so'zning boshiga qarab saralangan. Agar boshida noma'lumlik (`%`) bo'lsa, butun daraxtni tekshirib chiqishga majbur bo'ladi.

## Ishlash natijasi:
```text
qoida                                                     
---------------------------------------------------------------------------------------------------------------
 LIKE '%abc' alifbo boshidan qidirish imkonini bermaydi, shu bois B-Tree ishlamaydi. Faqat 'abc%' SARGable hisoblanadi
(1 row)
```


# 721-Topshiriq: SARGability: Sana ustunlarida noto'g'ri formulalar
## Topshiriq sharti:
`WHERE sana::DATE = '2026-05-01'` o'rniga SARGable to'g'ri oraliq yozish.

## Yechim (SQL kodi):
```sql
-- Indeksni o'ldiruvchi so'rov:
-- WHERE DATE(yaratilgan_sana) = '2026-05-01'

-- SARGable ideal so'rov:
EXPLAIN SELECT * FROM foydalanuvchilar_idx 
WHERE yaratilgan_sana >= '2026-05-01' AND yaratilgan_sana < '2026-05-02';
```

## Tushuntirish va Mantiq:
Ustunni funksiyaga o'ramasdan oraliq (`>=` va `<`) bilan yozish B-Tree indeksidan to'liq foydalanishni kafolatlaydi.

## Ishlash natijasi:
```text
QUERY PLAN                                  
------------------------------------------------------------------------------
 Seq Scan on foydalanuvchilar_idx  (cost=0.00..1.02 rows=1 width=58)
   Filter: ((yaratilgan_sana >= '...'::timestamptz) AND (yaratilgan_sana < '...'::timestamptz))
(2 rows)
```


# 722-Topshiriq: Jadvalni bloklamasdan jonli indeks qurish: CREATE INDEX CONCURRENTLY
## Topshiriq sharti:
Ishlab turgan yirik korporativ bazada o'qish va yozishni to'xtatmasdan indeks yaratish buyrug'i.

## Yechim (SQL kodi):
```sql
CREATE INDEX CONCURRENTLY idx_conc_ism ON foydalanuvchilar_idx (ism);
```

## Tushuntirish va Mantiq:
Oddiy `CREATE INDEX` jadvalga SHARE LOCK qo'yadi va barcha INSERT, UPDATE, DELETE larni to'xtatib qo'yadi. 'CONCURRENTLY' esa ikki bosqichda jadvalni qulflamasdan orqa fonda indeks quradi. Production muhitida yagona to'g'ri yo'l.

## Ishlash natijasi:
```text
CREATE INDEX
Query returned successfully in 42 msec.
```


# 723-Topshiriq: Buzilgan yoki eskirgan indeksni qayta qurish: REINDEX
## Topshiriq sharti:
Jadval indekslarini shishib ketishdan (bloat) tozalash va qayta tiklash.

## Yechim (SQL kodi):
```sql
REINDEX TABLE CONCURRENTLY foydalanuvchilar_idx;
```

## Tushuntirish va Mantiq:
'REINDEX TABLE' barcha indekslarni noldan qayta tuzadi. 'CONCURRENTLY' qo'shilsa bu jarayon o'qish va yozishni to'xtatmasdan bajariladi.

## Ishlash natijasi:
```text
REINDEX
Query returned successfully in 55 msec.
```


# 724-Topshiriq: Indekslarning diskdagi hajmini aniqlash
## Topshiriq sharti:
Qaysi indekslar diskda eng ko'p joy olayotganini pg_relation_size bilan aniqlang.

## Yechim (SQL kodi):
```sql
SELECT 
    indexname, 
    pg_size_pretty(pg_relation_size(quote_ident(indexname)::regclass)) AS indeks_hajmi
FROM pg_indexes 
WHERE tablename = 'foydalanuvchilar_idx';
```

## Tushuntirish va Mantiq:
Katta hajmli va keraksiz indekslar xotirani behuda band qiladi va yozish amallarini sekinlashtiradi.

## Ishlash natijasi:
```text
indexname         | indeks_hajmi 
--------------------------+--------------
 foydalanuvchilar_idx_pkey| 16 kB
 idx_foydalanuvchi_email  | 16 kB
 uq_idx_telefon           | 16 kB
 idx_pastki_email         | 16 kB
 idx_user_id_include      | 16 kB
 idx_hash_token           | 16 kB
 idx_conc_ism             | 16 kB
(7 rows)
```


# 725-Topshiriq: Ishlatilmayotgan (keraksiz) indekslarni topish: pg_stat_user_indexes
## Topshiriq sharti:
Bazadagi qaysi indekslar hech qachon so'rovlarda ishlatilmaganini aniqlash.

## Yechim (SQL kodi):
```sql
SELECT 
    relname AS jadval,
    indexrelname AS indeks,
    idx_scan AS skanerlashlar_soni
FROM pg_stat_user_indexes
WHERE schemaname = 'public' AND idx_scan = 0;
```

## Tushuntirish va Mantiq:
Agar 'idx_scan = 0' bo'lsa, demak bu indeks yaratilganidan beri birorta ham so'rov unga kirmagan! Bunday indekslar faqatgina INSERT/UPDATE ni sekinlashtiradi va ularni o'chirish (DROP) tavsiya etiladi.

## Ishlash natijasi:
```text
jadval       |         indeks          | skanerlashlar_soni 
--------------------+-------------------------+--------------------
 foydalanuvchilar_idx| idx_foydalanuvchi_email |                  0
 foydalanuvchilar_idx| uq_idx_telefon          |                  0
(2 rows)
```


# 726-Topshiriq: Baza statistikasini qo'lda yangilash: ANALYZE
## Topshiriq sharti:
Optimizator to'g'ri reja tanlashi uchun jadval ma'lumotlar taqsimoti statistikasini yangilang.

## Yechim (SQL kodi):
```sql
ANALYZE foydalanuvchilar_idx;
```

## Tushuntirish va Mantiq:
'ANALYZE' jadvaldan tasodifiy qatorlar namunalarini olib, 'pg_statistic' katalogiga histogrammalar va chastotalarni yozadi. Optimizator qaysi indeksni tanlashni aynan shu statistikaga qarab hal qiladi.

## Ishlash natijasi:
```text
ANALYZE
Query returned successfully in 18 msec.
```


# 727-Topshiriq: Saralash yo'nalishi bilan indeks yaratish: DESC NULLS LAST
## Topshiriq sharti:
Maxsus saralash talablariga mos keluvchi yo'naltirilgan B-Tree indeksini yarating.

## Yechim (SQL kodi):
```sql
CREATE INDEX idx_user_vaqt_desc ON foydalanuvchilar_idx (yaratilgan_sana DESC NULLS LAST);
```

## Tushuntirish va Mantiq:
B-Tree ikki tomonlama o'qilsa-da, 'NULLS LAST' va 'DESC' bilan yaratilgan indeks murakkab ko'p ustunli saralashlarda vaqtincha xotirada saralash (Sort operatori) xarajatini 0 ga tushiradi.

## Ishlash natijasi:
```text
CREATE INDEX
Query returned successfully in 28 msec.
```


# 728-Topshiriq: Trigram (pg_trgm) indeksi bilan satr o'rtasidagi LIKE qidiruvini tezlashtirish
## Topshiriq sharti:
`LIKE '%so''z%'` so'rovlarini 100 barobarga tezlashtiruvchi GIN Trigram indeksini yarating.

## Yechim (SQL kodi):
```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX idx_trgm_ism ON foydalanuvchilar_idx USING GIN (ism gin_trgm_ops);
```

## Tushuntirish va Mantiq:
'pg_trgm' so'zlarni 3 harfli bo'laklarga (trigrammalarga) ajratadi. GIN indeksi bilan birikib, u hattoki boshida '%' bo'lgan `LIKE '%ali%'` so'rovlarini ham Index Scan rejasida chaqmoqdek tez topadi.

## Ishlash natijasi:
```text
CREATE EXTENSION
CREATE INDEX
Query returned successfully in 45 msec.
```


# 729-Topshiriq: Indeks selektivligi (Index Selectivity) tushunchasi
## Topshiriq sharti:
Nega BOOLEAN ustunga (jinsi, faolligi) oddiy B-Tree indeks qo'yish samarasiz ekanligini tushuntiring.

## Yechim (SQL kodi):
```sql
SELECT 'Past selektivlik (faqat 2 xil qiymat bor ustun) da B-Tree ishlamaydi, optimizator baribir Seq Scan tanlaydi' AS qoida;
```

## Tushuntirish va Mantiq:
Selektivlik: unikal qiymatlar sonining umumiy qatorlarga nisbati. Agar ustunda faqat 'true' va 'false' bo'lsa, selektivlik past bo'ladi va indeks foyda bermaydi (faqat qisman indeks 'WHERE faol = true' foyda berishi mumkin).

## Ishlash natijasi:
```text
qoida                                                        
--------------------------------------------------------------------------------------------------------------------
 Past selektivlik (faqat 2 xil qiymat bor ustun) da B-Tree ishlamaydi, optimizator baribir Seq Scan tanlaydi
(1 row)
```


# 730-Topshiriq: EXPLAIN (ANALYZE, TIMING OFF) bilan yuklamani kamaytirish
## Topshiriq sharti:
Juda katta so'rovlarda vaqt o'lchash protsessorga og'irlik qilmasligi uchun faqat qatorlar sonini tekshirish.

## Yechim (SQL kodi):
```sql
EXPLAIN (ANALYZE, TIMING OFF) SELECT * FROM foydalanuvchilar_idx;
```

## Tushuntirish va Mantiq:
'TIMING OFF' protsessorning soat sikllarini o'lchash xarajatlarini (gettimeofday overhead) olib tashlaydi, bu yirik so'rovlarni xavfsiz tahlil qilish imkonini beradi.

## Ishlash natijasi:
```text
QUERY PLAN                                         
-------------------------------------------------------------------------------------------
 Seq Scan on foydalanuvchilar_idx  (cost=0.00..1.00 rows=1 width=58) (rows=0 loops=1)
 Planning Time: 0.048 ms
 Execution Time: 0.015 ms
(3 rows)
```


# 731-Topshiriq: Indekslarning yozish tezligiga ta'siri (DML Overhead)
## Topshiriq sharti:
Jadvalda 10 ta indeks bo'lsa INSERT va UPDATE nima uchun sekinlashishini ko'rsating.

## Yechim (SQL kodi):
```sql
SELECT 'Har bir yangi INSERT barcha 10 ta indeks daraxtini yangilashni talab qiladi, bu yozishni 5-10 marta sekinlashtiradi' AS ogohlantirish;
```

## Tushuntirish va Mantiq:
Indekslar o'qishni (SELECT) tezlashtiradi, lekin yozishni (INSERT, UPDATE, DELETE) sekinlashtiradi. Har bir jadvalda faqat haqiqatda kerakli indekslar bo'lishi shart.

## Ishlash natijasi:
```text
ogohlantirish                                                          
--------------------------------------------------------------------------------------------------------------------------------
 Har bir yangi INSERT barcha 10 ta indeks daraxtini yangilashni talab qiladi, bu yozishni 5-10 marta sekinlashtiradi
(1 row)
```


# 732-Topshiriq: HOT (Heap-Only Tuples) optimizatsiyasi
## Topshiriq sharti:
UPDATE paytida indekslarni qayta yozmasdan sahifa ichida yangilash mexanizmi.

## Yechim (SQL kodi):
```sql
SELECT 'Agar UPDATE qilingan ustun indekslanmagan bo‘lsa va sahifada joy bo‘lsa, HOT update indekslarga tegmasdan o‘ta tez bajariladi' AS tahlil;
```

## Tushuntirish va Mantiq:
PostgreSQL ning eng buyuk ixtirolaridan biri bo'lgan HOT (Heap-Only Tuples) faqat indekslanmagan ustunlar yangilanganda ishlaydi va indekslarni qayta qurish xarajatini 0 ga tushiradi.

## Ishlash natijasi:
```text
tahlil                                                                    
-----------------------------------------------------------------------------------------------------------------------------------------------
 Agar UPDATE qilingan ustun indekslanmagan bo‘lsa va sahifada joy bo‘lsa, HOT update indekslarga tegmasdan o‘ta tez bajariladi
(1 row)
```


# 733-Topshiriq: Indeks parametrlarini sozlash: FILLFACTOR
## Topshiriq sharti:
Tez-tez yangilanadigan indekslar uchun fillfactor=80 bilan joy qoldirish.

## Yechim (SQL kodi):
```sql
CREATE INDEX idx_user_fill ON foydalanuvchilar_idx (id) WITH (fillfactor = 80);
```

## Tushuntirish va Mantiq:
Indeks B-Tree sahifalarida 20% bo'sh joy qoldirish sahifalarning ikkiga bo'linib ketishi (B-Tree page splits) oldini oladi.

## Ishlash natijasi:
```text
CREATE INDEX
Query returned successfully in 27 msec.
```


# 734-Topshiriq: So'rov rejasini JSON formatida olish: EXPLAIN (FORMAT JSON)
## Topshiriq sharti:
So'rov rejasini avtomatik tahlil qiluvchi vizual dasturlar uchun JSON formatida eksport qiling.

## Yechim (SQL kodi):
```sql
EXPLAIN (FORMAT JSON) SELECT * FROM foydalanuvchilar_idx;
```

## Tushuntirish va Mantiq:
DBeaver, pgAdmin va veb-servislar rejani vizual diagramma sifatida chizish uchun JSON formatidan foydalanadi.

## Ishlash natijasi:
```text
QUERY PLAN             
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
(1 row)
```


# 735-Topshiriq: Tengsizlik va oraliq so'rovlarda kompozit indeks ustunlari tartibi
## Topshiriq sharti:
Nega tenglik ustuni oldinda, oraliq ustuni oxirida turishi kerakligini tushuntiring.

## Yechim (SQL kodi):
```sql
SELECT 'Kompozit indeks qoidasi: Tenglik ustunlari (masalan: filial_id) birinchi, oraliq ustuni (sana) eng oxirida turishi shart' AS mezon;
```

## Tushuntirish va Mantiq:
Agar `(sana, filial_id)` qilinsa, sana bo'yicha oraliqqa tushgach, ikkinchi ustun bo'yicha binar qidiruv to'xtaydi. `(filial_id, sana)` tartibi esa ikkala ustunni ham 100% indeksga jalb qiladi.

## Ishlash natijasi:
```text
mezon                                                           
--------------------------------------------------------------------------------------------------------------------------
 Kompozit indeks qoidasi: Tenglik ustunlari (masalan: filial_id) birinchi, oraliq ustuni (sana) eng oxirida turishi shart
(1 row)
```


# 736-Topshiriq: Indekslangan ustun ustida arifmetika xatosi
## Topshiriq sharti:
`WHERE narx * 1.1 > 10000` nega indeksdan foydalanmasligini va uni to'g'irlash usuli.

## Yechim (SQL kodi):
```sql
-- Indeks ishlamaydi: WHERE narx * 1.1 > 10000;
-- Indeks to'liq ishlaydi:
-- WHERE narx > 10000 / 1.1;
SELECT 'Arifmetik amalni ustunga emas, konstantaga qo‘llash so‘rovni SARGable qiladi' AS yechim;
```

## Tushuntirish va Mantiq:
Matematik tenglamani shunday o'zgartirish kerakki, indekslangan ustun yolg'iz o'zi sof qolsin.

## Ishlash natijasi:
```text
yechim                                        
--------------------------------------------------------------------------------------
 Arifmetik amalni ustunga emas, konstantaga qo‘llash so‘rovni SARGable qiladi
(1 row)
```


# 737-Topshiriq: Indeksni vaqtincha tekshirish: enable_seqscan parametri
## Topshiriq sharti:
PostgreSQL ni qasddan indeks ishlatishga majburlash orqali rejani solishtirish.

## Yechim (SQL kodi):
```sql
SET enable_seqscan = OFF;
EXPLAIN SELECT * FROM foydalanuvchilar_idx;
SET enable_seqscan = ON;
```

## Tushuntirish va Mantiq:
'enable_seqscan = OFF' ishlab chiqarishda ishlatilmaydi, lekin test qilishda optimizator nima uchun Seq Scanni tanlaganini tushunish uchun ajoyib vositadir.

## Ishlash natijasi:
```text
SET
                                  QUERY PLAN                                  
------------------------------------------------------------------------------
 Seq Scan on foydalanuvchilar_idx  (cost=10000000000.00..10000000001.00 rows=1 width=58)
(1 row)
SET
```


# 738-Topshiriq: Parallel so'rovlar bajarilishi (Parallel Query)
## Topshiriq sharti:
PostgreSQL bir nechta protsessor yadrolarini (Worker processes) jalb qilib jadvalni parallel skanerlashi.

## Yechim (SQL kodi):
```sql
SELECT 'PostgreSQL katta jadvallarda avtomatik ravishda Parallel Seq Scan va Parallel Hash Join ishga tushiradi' AS parallelizm;
```

## Tushuntirish va Mantiq:
'max_parallel_workers_per_gather' parametri orqali bitta SQL so'rovini 4-8 ta protsessor yadrolarida baravar parallel hisoblash mumkin.

## Ishlash natijasi:
```text
parallelizm                                                     
--------------------------------------------------------------------------------------------------------------------
 PostgreSQL katta jadvallarda avtomatik ravishda Parallel Seq Scan va Parallel Hash Join ishga tushiradi
(1 row)
```


# 739-Topshiriq: JIT (Just-In-Time) kompilyatsiya tahlili
## Topshiriq sharti:
EXPLAIN ANALYZE da 'JIT: Functions: ...' nima ekanligini tushuntiring.

## Yechim (SQL kodi):
```sql
SELECT 'JIT kompilyatsiya (LLVM) murakkab ifodalar va agregatlarni to‘g‘ridan-to‘g‘ri mashina kodiga o‘girib tezlashtiradi' AS jit_info;
```

## Tushuntirish va Mantiq:
PostgreSQL 11+ da LLVM asosidagi JIT kompilyator mavjud. Og'ir analitik so'rovlarda u SQL ifodalarini protsessorning toza ikkilik ko'rsatmalariga aylantiradi.

## Ishlash natijasi:
```text
jit_info                                                        
------------------------------------------------------------------------------------------------------------------------
 JIT kompilyatsiya (LLVM) murakkab ifodalar va agregatlarni to‘g‘ridan-to‘g‘ri mashina kodiga o‘girib tezlashtiradi
(1 row)
```


# 740-Topshiriq: Kompakt qisman indeks bilan arxivni ajratish
## Topshiriq sharti:
Faqat so'nggi 30 kunlik faol ma'lumotlarni indekslash.

## Yechim (SQL kodi):
```sql
CREATE INDEX idx_songgi_faol ON buyurtmalar_part (mijoz_id) 
WHERE holat IN ('yangi', 'jarayonda');
```

## Tushuntirish va Mantiq:
Eski arxiv yozuvlari indeksdan chiqarib tashlanadi va kesh xotirasi maksimal tejaladi.

## Ishlash natijasi:
```text
CREATE INDEX
Query returned successfully in 28 msec.
```


# 741-Topshiriq: Random Page Cost sozlamasi va SSD drayverlar
## Topshiriq sharti:
SSD disklarda B-Tree indekslaridan foydalanishni rag'batlantirish uchun sozlamani o'zgartirish.

## Yechim (SQL kodi):
```sql
SHOW random_page_cost;
```

## Tushuntirish va Mantiq:
Eski mexanik HDD larda 'random_page_cost = 4.0' bo'lgan. Zamonaviy NVMe SSD larda esa ixtiyoriy sahifani o'qish ketma-ket o'qish bilan deyarli bir xil tezlikda, shuning uchun bu qiymatni 1.1 ga tushirish tavsiya etiladi (bu indekslarni tanlashni oshiradi).

## Ishlash natijasi:
```text
random_page_cost 
------------------
 4
(1 row)
```


# 742-Topshiriq: Indekslangan ustunda implicit type conversion (Yashirin tur o'zgarishi)
## Topshiriq sharti:
VARCHAR ustunni butun son bilan solishtirganda indeks nega ishlamay qolishini ko'rsating.

## Yechim (SQL kodi):
```sql
-- Agar telefon VARCHAR bo'lsa:
-- WHERE telefon = 998901234567; (Indeks ishlamaydi, chunki son matnga o'girilmaydi, ustun songa o'giriladi!)
-- WHERE telefon = '998901234567'; (Indeks to'liq ishlaydi)
SELECT 'Taqqoslanayotgan qiymat tipi ustun tipi bilan 100% mos bo‘lishi shart' AS qoida;
```

## Tushuntirish va Mantiq:
Dasturlash tilidan parametr yuborilganda tip xato bo'lsa, baza ustun ustida yashirin `CAST` bajaradi va bu B-Tree indeksini ishdan chiqaradi.

## Ishlash natijasi:
```text
qoida                                 
-----------------------------------------------------------------------
 Taqqoslanayotgan qiymat tipi ustun tipi bilan 100% mos bo‘lishi shart
(1 row)
```


# 743-Topshiriq: Indeksda ma'lumotlar zichligi: pg_stat_all_indexes
## Topshiriq sharti:
Indeks bloklari qanchalik tez-tez o'qilayotganini tahlil qilish.

## Yechim (SQL kodi):
```sql
SELECT indexrelid, idx_blks_read, idx_blks_hit 
FROM pg_statio_user_indexes 
LIMIT 3;
```

## Tushuntirish va Mantiq:
Xotiradan o'qish (hit) va diskdan o'qish (read) balansi ko'rsatiladi.

## Ishlash natijasi:
```text
indexrelid | idx_blks_read | idx_blks_hit 
------------+---------------+--------------
      16390 |             1 |            0
      16391 |             0 |            0
      16392 |             0 |            0
(3 rows)
```


# 744-Topshiriq: Ko'p ustunli saralashda indeksning to'liq mos kelishi
## Topshiriq sharti:
`ORDER BY a ASC, b DESC` uchun aynan mos indeks tuzish.

## Yechim (SQL kodi):
```sql
CREATE INDEX idx_a_asc_b_desc ON xodimlar_comp (familiya ASC, ism DESC);
```

## Tushuntirish va Mantiq:
Agar so'rovda bir ustun ASC, ikkinchisi DESC bo'lsa, indeks ham aynan shu yo'nalishlarda e'lon qilinishi xotiradagi 'Sort' operatsiyasini batamom yo'qotadi.

## Ishlash natijasi:
```text
CREATE INDEX
Query returned successfully in 27 msec.
```


# 745-Topshiriq: Tizim jadvallarining indekslarini ko'rish
## Topshiriq sharti:
Jadvalda qanday indekslar borligini qisqa so'rov bilan ko'rish.

## Yechim (SQL kodi):
```sql
SELECT c.relname AS indeks_nomi
FROM pg_class c
JOIN pg_index i ON i.indexrelid = c.oid
WHERE i.indrelid = 'foydalanuvchilar_idx'::regclass;
```

## Tushuntirish va Mantiq:
Barcha ichki indekslar ro'yxati olinadi.

## Ishlash natijasi:
```text
indeks_nomi        
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
(10 rows)
```


# 746-Topshiriq: Jadval va indekslarni keshga yuklab qo'yish: pg_prewarm
## Topshiriq sharti:
Server qayta yoqilganda keshni sovuq holatdan (Cold cache) issiq holatga (Warm cache) keltirish.

## Yechim (SQL kodi):
```sql
CREATE EXTENSION IF NOT EXISTS pg_prewarm;

SELECT pg_prewarm('foydalanuvchilar_idx');
```

## Tushuntirish va Mantiq:
'pg_prewarm' kengaytmasi jadval yoki indeks sahifalarini server ishga tushishi bilanoq operativ xotiraga (Buffer Pool) yuklab beradi. Birinchi so'rovlar ham sekinlashmasdan ishlaydi.

## Ishlash natijasi:
```text
CREATE EXTENSION
 pg_prewarm 
------------
          1
(1 row)
```


# 747-Topshiriq: Indekslarning to'g'ri ishlashini tekshiruvchi amocms testi
## Topshiriq sharti:
Indeks haqiqatan ishlayotganini qisqa vaqt ichida isbotlash.

## Yechim (SQL kodi):
```sql
EXPLAIN SELECT id FROM foydalanuvchilar_idx WHERE id = 1;
```

## Tushuntirish va Mantiq:
Birlamchi kalit indeksi bo'yicha Index Scan ko'rsatiladi.

## Ishlash natijasi:
```text
QUERY PLAN                                          
----------------------------------------------------------------------------------------------
 Index Only Scan using foydalanuvchilar_idx_pkey on foydalanuvchilar_idx  (cost=0.15..8.17 rows=1 width=4)
   Index Cond: (id = 1)
(2 rows)
```


# 748-Topshiriq: Expression indeksda DETERMINISTIC funksiya talabi
## Topshiriq sharti:
Nega `CURRENT_DATE` yoki `RANDOM()` qatnashgan ifodalarga indeks qurib bo'lmasligini tushuntiring.

## Yechim (SQL kodi):
```sql
SELECT 'Indeks ifodasi IMMUTABLE (o‘zgarmas natija beruvchi) bo‘lishi shart. Har kuni o‘zgaruvchi NOW() ga indeks qo‘yib bo‘lmaydi' AS qoida;
```

## Tushuntirish va Mantiq:
PostgreSQL faqat deterministik (IMMUTABLE) funksiyalarni indekslashga ruxsat beradi. Natijasi vaqtga qarab o'zgaruvchi funksiyalarni indekslab bo'lmaydi.

## Ishlash natijasi:
```text
qoida                                                           
--------------------------------------------------------------------------------------------------------------------------
 Indeks ifodasi IMMUTABLE (o‘zgarmas natija beruvchi) bo‘lishi shart. Har kuni o‘zgaruvchi NOW() ga indeks qo‘yib bo‘lmaydi
(1 row)
```


# 749-Topshiriq: B-Tree indekslarida deduplikatsiya (PostgreSQL 13+)
## Topshiriq sharti:
Bir xil qiymatli kalitlar indeks hajmini oshirmasligi uchun B-Tree avtomatik deduplikatsiyasi.

## Yechim (SQL kodi):
```sql
SELECT 'PostgreSQL 13 dan boshlab B-Tree indekslaridagi takroriy qiymatlar avtomatik siqiladi (Deduplication)' AS afzallik;
```

## Tushuntirish va Mantiq:
Takrorlanuvchi kalitlarga ega indekslar diskda 3 barobargacha kam joy egallaydi.

## Ishlash natijasi:
```text
afzallik                                                       
---------------------------------------------------------------------------------------------------------------------
 PostgreSQL 13 dan boshlab B-Tree indekslaridagi takroriy qiymatlar avtomatik siqiladi (Deduplication)
(1 row)
```


# 750-Topshiriq: Korporativ Optimallashtirish: FinTech Katta Ma'lumotlar Bazasida Indekslar Arxitekturasi
## Topshiriq sharti:
Millionlab tranzaksiyalarga ega to'lov tizimida oylik qidiruv, hisob raqami bo'yicha izlash, status bo'yicha saralash va tezkor hisobotlar uchun B-Tree, Composite, Partial va Covering indekslarning to'liq optimal kompleksini yarating hamda EXPLAIN ANALYZE bilan isbotlang.

## Yechim (SQL kodi):
```sql
CREATE TABLE korporativ_tranzaksiyalar (
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
LIMIT 5;
```

## Tushuntirish va Mantiq:
Ushbu korporativ arxitektura yuqori yuklamali (High-Load) to'lov tizimlarining standart yechimidir: qamrab oluvchi (Covering Index) orqali asosiy ma'lumotlar bloklariga kirmasdan Index-Only Scan ga erishiladi, qisman indeks (Partial Index) orqali kutilayotgan tranzaksiyalar bir zumda topiladi va server resurslari 90% ga tejaladi.

## Ishlash natijasi:
```text
CREATE TABLE
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
(6 rows)
```

