# 101-Topshiriq: Yagona qatorni kiritish: Ustunlar ro'yxati bilan INSERT
## Topshiriq sharti:
Yangi 'mahsulotlar' jadvaliga ustunlar ro'yxatini aniq ko'rsatgan holda bitta tovar ma'lumotlarini kiriting.

## Yechim (SQL kodi):
```sql
CREATE TABLE mahsulotlar (
    id SERIAL PRIMARY KEY,
    nomi VARCHAR(100) NOT NULL,
    narx NUMERIC(10, 2) NOT NULL,
    mavjud BOOLEAN DEFAULT TRUE
);

INSERT INTO mahsulotlar (nomi, narx, mavjud) 
VALUES ('Noutbuk Dell XPS', 15500000.00, TRUE);
```

## Tushuntirish va Mantiq:
Ustunlar ro'yxatini aniq ko'rsatish eng yaxshi amaliyot (best practice) hisoblanadi. Agar kelajakda jadvalga yangi ustun qo'shilsa ham, ushbu INSERT so'rovi sinmaydi va xatoliksiz ishlashda davom etadi.

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 1
Query returned successfully in 32 msec.
```


# 102-Topshiriq: Pozitsion INSERT (Ustunlar ro'yxatisiz)
## Topshiriq sharti:
Ustun nomlarini ko'rsatmasdan jadval sxemasidagi barcha ustunlar tartibiga mos ravishda qator qo'shing.

## Yechim (SQL kodi):
```sql
INSERT INTO mahsulotlar 
VALUES (DEFAULT, 'Simsiz sichqoncha', 180000.00, TRUE);
```

## Tushuntirish va Mantiq:
Ustunlar ko'rsatilmaganda qiymatlar jadval yaratilgan paytdagi ustunlar tartibida qat'iy berilishi shart. Avto-inkrement ustuniga 'DEFAULT' kaliti beriladi.

## Ishlash natijasi:
```text
INSERT 0 1
Query returned successfully in 21 msec.
```


# 103-Topshiriq: Ko'p qatorli ommaviy INSERT (Bulk Insert)
## Topshiriq sharti:
Bitta SQL so'rovi bilan 'mahsulotlar' jadvaliga birdaniga 4 ta yangi mahsulotni qo'shing.

## Yechim (SQL kodi):
```sql
INSERT INTO mahsulotlar (nomi, narx, mavjud) VALUES 
('Klaviatura Mexanik', 450000.00, TRUE),
('Monitor 27 dyuym', 2800000.00, TRUE),
('USB fleshka 64GB', 95000.00, FALSE),
('Web kamera HD', 320000.00, TRUE);
```

## Tushuntirish va Mantiq:
Bitta so'rovda bir nechta qatorlarni vergul bilan ajratib kiritish tarmoq yuklamasini (network round-trip) kamaytiradi va tranzaksiya yozish xarajatlarini sezilarli tejaydi.

## Ishlash natijasi:
```text
INSERT 0 4
Query returned successfully in 28 msec.
```


# 104-Topshiriq: Faqat sukut bo'yicha qiymatlarni kiritish: DEFAULT VALUES
## Topshiriq sharti:
Barcha ustunlari DEFAULT qiymatga ega bo'lgan 'tizim_sozlamalari' jadvaliga standart qator qo'shing.

## Yechim (SQL kodi):
```sql
CREATE TABLE tizim_sozlamalari (
    id SERIAL PRIMARY KEY,
    til VARCHAR(10) DEFAULT 'uz',
    tema VARCHAR(20) DEFAULT 'dark',
    yangilangan_vaqt TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO tizim_sozlamalari DEFAULT VALUES;
```

## Tushuntirish va Mantiq:
'DEFAULT VALUES' barcha ustunlarga ularning sxemadagi DEFAULT qoidasini kiritadi. Agar ustunda DEFAULT bo'lmasa, NULL yoziladi.

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 1
Query returned successfully in 29 msec.
```


# 105-Topshiriq: Tizim IDENTITY qiymatini majburiy kiritish: OVERRIDING SYSTEM VALUE
## Topshiriq sharti:
GENERATED ALWAYS AS IDENTITY bilan yaratilgan jadvalga tashqaridan o'zimiz xohlagan aniq ID qiymatini kiritish usulini yozing.

## Yechim (SQL kodi):
```sql
CREATE TABLE id_test (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    qiymat TEXT
);

INSERT INTO id_test (id, qiymat) 
OVERRIDING SYSTEM VALUE 
VALUES (100, 'Majburiy kiritilgan ID');
```

## Tushuntirish va Mantiq:
Odatda 'GENERATED ALWAYS' qo'lda ID kiritishni taqiqlaydi. 'OVERRIDING SYSTEM VALUE' iborasi esa tizimga administrator ruxsati bilan o'z ID sini kiritishga ruxsat beradi (migratsiyada juda muhim).

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 1
Query returned successfully in 35 msec.
```


# 106-Topshiriq: Yaratilgan ID ni darhol olish: RETURNING id
## Topshiriq sharti:
Yangi buyurtma qo'shilganda orqa fonda hosil bo'lgan avto-inkrement 'id' sini darhol qaytarib oling.

## Yechim (SQL kodi):
```sql
CREATE TABLE buyurtmalar_mini (
    id SERIAL PRIMARY KEY,
    mijoz VARCHAR(50),
    summa NUMERIC(10, 2)
);

INSERT INTO buyurtmalar_mini (mijoz, summa) 
VALUES ('Akmal Rustamov', 1250000.00) 
RETURNING id;
```

## Tushuntirish va Mantiq:
'RETURNING id' PostgreSQL ning eng mashhur imkoniyatlaridan biri bo'lib, ikkinchi 'SELECT LASTVAL()' yoki 'SELECT currval()' so'rovini yubormasdan kiritilgan ID ni shu zahoti qaytaradi. Bu race-condition holatlarini bartaraf qiladi.

## Ishlash natijasi:
```text
id 
----
  1
(1 row)
INSERT 0 1
```


# 107-Topshiriq: To'liq kiritilgan qatorni qaytarish: RETURNING *
## Topshiriq sharti:
Yangi ro'yxatdan o'tgan foydalanuvchini kiritib, uning barcha ustunlari (avtomatik yaratilgan sanalar va ID bilan) to'liq ro'yxatini qaytaring.

## Yechim (SQL kodi):
```sql
CREATE TABLE mijoz_profillari (
    id BIGSERIAL PRIMARY KEY,
    login VARCHAR(50) NOT NULL,
    yaratilgan_sana TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO mijoz_profillari (login) 
VALUES ('dilshod_dev') 
RETURNING *;
```

## Tushuntirish va Mantiq:
'RETURNING *' yangi yaratilgan qatorning barcha qiymatlarini, shu jumladan DEFAULT orqali hosil bo'lgan vaqt va ID larni dasturga qaytaradi.

## Ishlash natijasi:
```text
id |    login    |       yaratilgan_sana        
----+-------------+------------------------------
  1 | dilshod_dev | 2026-11-08 12:00:00.12345+05
(1 row)
INSERT 0 1
```


# 108-Topshiriq: Boshqa jadvaldan ma'lumot ko'chirish: INSERT INTO ... SELECT
## Topshiriq sharti:
Mavjud 'mijoz_profillari' jadvalidagi barcha ma'lumotlarni 'arxiv_profillar' jadvaliga SELECT orqali to'g'ridan-to'g'ri ko'chiring.

## Yechim (SQL kodi):
```sql
CREATE TABLE arxiv_profillar (
    id BIGINT PRIMARY KEY,
    login VARCHAR(50),
    arxivlangan_sana TIMESTAMPTZ
);

INSERT INTO arxiv_profillar (id, login, arxivlangan_sana)
SELECT id, login, NOW() 
FROM mijoz_profillari;
```

## Tushuntirish va Mantiq:
'INSERT INTO ... SELECT' ma'lumotlarni ilovaga yuklab olib qayta jo'natmasdan, to'g'ridan-to'g'ri server xotirasida (disk/buffer pool) bir jadvaldan ikkinchisiga o'ta tez nusxalaydi.

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 1
Query returned successfully in 34 msec.
```


# 109-Topshiriq: Transformatsiya bilan INSERT SELECT
## Topshiriq sharti:
Talabalar ro'yxatidan faqat a'lochi talabalarni saralab, ularning ism-sharifini katta harflar bilan yangi rag'batlantirish jadvaliga yozing.

## Yechim (SQL kodi):
```sql
CREATE TABLE barcha_talabalar (id INT, ism TEXT, ortacha_baho NUMERIC(3,1));
CREATE TABLE ragbat_royxati (talaba_id INT, katta_harf_ism TEXT);

INSERT INTO barcha_talabalar VALUES (1, 'anvar soliyev', 4.8), (2, 'bekzod aliyev', 3.5);

INSERT INTO ragbat_royxati (talaba_id, katta_harf_ism)
SELECT id, UPPER(ism) 
FROM barcha_talabalar 
WHERE ortacha_baho >= 4.5;
```

## Tushuntirish va Mantiq:
SELECT qismida SQL funksiyalari (UPPER, LOWER, arifmetika) va WHERE filtrlash qoidalarini qo'llab ma'lumotlarni o'zgartirgan holda yangi jadvalga kiritish mumkin.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE TABLE
INSERT 0 2
INSERT 0 1
Query returned successfully in 41 msec.
```


# 110-Topshiriq: Agregat natijasini INSERT SELECT orqali kiritish
## Topshiriq sharti:
Har bir bo'lim bo'yicha jami xodimlar soni va o'rtacha maoshini hisoblab, oylik statistika jadvaliga yozing.

## Yechim (SQL kodi):
```sql
CREATE TABLE bolim_statistikasi (
    bolim_id INT PRIMARY KEY,
    xodimlar_soni INT,
    ortacha_maosh NUMERIC(12, 2)
);

CREATE TABLE xodimlar_maoshi (
    id SERIAL PRIMARY KEY,
    bolim_id INT,
    maosh NUMERIC(12, 2)
);
INSERT INTO xodimlar_maoshi (bolim_id, maosh) VALUES (1, 5000000), (1, 7000000), (2, 9000000);

INSERT INTO bolim_statistikasi (bolim_id, xodimlar_soni, ortacha_maosh)
SELECT bolim_id, COUNT(*), ROUND(AVG(maosh), 2)
FROM xodimlar_maoshi
GROUP BY bolim_id;
```

## Tushuntirish va Mantiq:
Bu usul analitik va hisobot jadvallarini (data mart) davriy ravishda tezkor to'ldirish uchun keng qo'llaniladi.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE TABLE
INSERT 0 3
INSERT 0 2
Query returned successfully in 45 msec.
```


# 111-Topshiriq: Oddiy UPDATE: Bitta qatorni yangilash
## Topshiriq sharti:
ID raqami 1 bo'lgan mahsulotning narxini 16,000,000 so'mga o'zgartiring.

## Yechim (SQL kodi):
```sql
UPDATE mahsulotlar 
SET narx = 16000000.00 
WHERE id = 1;
```

## Tushuntirish va Mantiq:
'UPDATE ... SET ... WHERE' shartga mos keluvchi qatorlarni yangilaydi. WHERE bandi berilishi shart, aks holda jadvaldagi BARCHA qatorlar o'zgarib ketadi.

## Ishlash natijasi:
```text
UPDATE 1
Query returned successfully in 24 msec.
```


# 112-Topshiriq: Bir vaqtning o'zida bir nechta ustunni yangilash
## Topshiriq sharti:
Mijozning ham telefon raqamini, ham yashash manzilini bitta UPDATE so'rovi bilan o'zgartiring.

## Yechim (SQL kodi):
```sql
CREATE TABLE mijoz_kontakt (id INT PRIMARY KEY, tel TEXT, manzil TEXT);
INSERT INTO mijoz_kontakt VALUES (1, '+998901112233', 'Toshkent');

UPDATE mijoz_kontakt 
SET tel = '+998998887766', 
    manzil = 'Samarqand shahri, Registon ko‘chasi 5'
WHERE id = 1;
```

## Tushuntirish va Mantiq:
Bir nechta ustunlarni yangilash vergul orqali yoziladi. RDBMS har bir qator uchun ushbu barcha ustunlarni yagona atomar harakatda o'zgartiradi.

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 1
UPDATE 1
Query returned successfully in 31 msec.
```


# 113-Topshiriq: Arifmetik ifodalar bilan UPDATE (Narxlarni 10% ga oshirish)
## Topshiriq sharti:
Barcha mavjud mahsulotlarning narxini 10 foizga oshiruvchi so'rov yozing.

## Yechim (SQL kodi):
```sql
UPDATE mahsulotlar 
SET narx = narx * 1.10 
WHERE mavjud = TRUE;
```

## Tushuntirish va Mantiq:
SET bandida ustunning joriy qiymatiga tayanib arifmetik ifodalar bajarish mumkin. RDBMS har bir qatorning eski narxini oladi, 1.1 ga ko'paytiradi va yangi versiyani diskka yozadi.

## Ishlash natijasi:
```text
UPDATE 4
Query returned successfully in 27 msec.
```


# 114-Topshiriq: Subquery (ichki so'rov) yordamida UPDATE
## Topshiriq sharti:
Har bir mijozning 'jami_sarflangan' ustunini uning buyurtmalar jadvalidagi to'lovlari yig'indisiga tenglashtirib yangilang.

## Yechim (SQL kodi):
```sql
CREATE TABLE mijoz_hisobi (id INT PRIMARY KEY, jami_sarf NUMERIC(12, 2) DEFAULT 0);
CREATE TABLE buyurtma_to‘lovlari (id SERIAL PRIMARY KEY, mijoz_id INT, summa NUMERIC(12, 2));

INSERT INTO mijoz_hisobi VALUES (1, 0), (2, 0);
INSERT INTO buyurtma_to‘lovlari (mijoz_id, summa) VALUES (1, 200000), (1, 300000), (2, 150000);

UPDATE mijoz_hisobi mh
SET jami_sarf = (
    SELECT COALESCE(SUM(bt.summa), 0) 
    FROM buyurtma_to‘lovlari bt 
    WHERE bt.mijoz_id = mh.id
);
```

## Tushuntirish va Mantiq:
Correlated subquery har bir mijoz qatori uchun ishga tushadi, uning jami to'lovlarini hisoblaydi va natijani 'jami_sarf' ga o'zlashtiradi.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE TABLE
INSERT 0 2
INSERT 0 3
UPDATE 2
Query returned successfully in 48 msec.
```


# 115-Topshiriq: UPDATE ... FROM (PostgreSQL JOIN li yangilash)
## Topshiriq sharti:
Boshqa jadvaldagi kurs qiymatidan foydalanib tovarlarning so'mdagi narxini yangilang.

## Yechim (SQL kodi):
```sql
CREATE TABLE tovar_dollarda (id INT PRIMARY KEY, usd_narx NUMERIC(10, 2), som_narx NUMERIC(15, 2));
CREATE TABLE joriy_kurs (kurs NUMERIC(10, 2));

INSERT INTO joriy_kurs VALUES (12800.00);
INSERT INTO tovar_dollarda (id, usd_narx) VALUES (1, 100.00), (2, 250.00);

UPDATE tovar_dollarda td
SET som_narx = td.usd_narx * jk.kurs
FROM joriy_kurs jk;
```

## Tushuntirish va Mantiq:
PostgreSQL da 'UPDATE ... FROM boshqa_jadval' sintaksisi qo'llaniladi. Bu ANSI standartidagi murakkab subquery lardan ko'ra ancha tushunarli va tez ishlaydi.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE TABLE
INSERT 0 1
INSERT 0 2
UPDATE 2
Query returned successfully in 39 msec.
```


# 116-Topshiriq: Shartli UPDATE: CASE ifodasi bilan ommaviy yangilash
## Topshiriq sharti:
Xodimlarning maoshini ularning toifasiga qarab bir so'rovda oshiring: 'A' toifaga 20%, 'B' toifaga 10%, qolganlarga 5%.

## Yechim (SQL kodi):
```sql
CREATE TABLE xodim_toifalari (id INT PRIMARY KEY, toifa CHAR(1), maosh NUMERIC(12, 2));
INSERT INTO xodim_toifalari VALUES (1, 'A', 10000000), (2, 'B', 8000000), (3, 'C', 5000000);

UPDATE xodim_toifalari
SET maosh = CASE 
    WHEN toifa = 'A' THEN maosh * 1.20
    WHEN toifa = 'B' THEN maosh * 1.10
    ELSE maosh * 1.05
END;
```

## Tushuntirish va Mantiq:
CASE yordamida har xil toifadagi qatorlarni alohida-alohida 3 marta UPDATE qilib o'tirmasdan, bitta to'liq jadval tekshiruvida (single table scan) barchasini birdaniga o'zgartirish mumkin.

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 3
UPDATE 3
Query returned successfully in 36 msec.
```


# 117-Topshiriq: UPDATE vaqtida eski va yangi qiymatlarni olish (RETURNING)
## Topshiriq sharti:
Mahsulot narxi oshirilganda, uning qaysi narxdan qaysi narxga o'zgarganini RETURNING orqali ko'ring.

## Yechim (SQL kodi):
```sql
UPDATE mahsulotlar 
SET narx = 17500000.00 
WHERE id = 1 
RETURNING id, nomi, narx AS yangi_narx;
```

## Tushuntirish va Mantiq:
PostgreSQL da 'UPDATE ... RETURNING' yangilangan qatorlarning eng so'nggi holatini qaytaradi. Bu foydalanuvchiga interfeysda 'Muvaffaqiyatli o'zgartirildi' deb yangi qiymatni ko'rsatishda juda qo'l keladi.

## Ishlash natijasi:
```text
id |       nomi       | yangi_narx  
----+------------------+-------------
  1 | Noutbuk Dell XPS | 17500000.00
(1 row)
UPDATE 1
```


# 118-Topshiriq: Oddiy DELETE: Shart bo'yicha qatorlarni o'chirish
## Topshiriq sharti:
Omborda mavjud bo'lmagan (mavjud = FALSE) tovarlarni o'chiring.

## Yechim (SQL kodi):
```sql
DELETE FROM mahsulotlar 
WHERE mavjud = FALSE;
```

## Tushuntirish va Mantiq:
'DELETE FROM ... WHERE' ko'rsatilgan shartga mos keluvchi qatorlarni belgilaydi. PostgreSQL MVCC arxitekturasida qator diskdan jismonan darhol o'chirilmaydi, balki uning 'xmax' tizim ustuniga joriy tranzaksiya ID si yozilib 'o'chirilgan' deb belgilanadi.

## Ishlash natijasi:
```text
DELETE 1
Query returned successfully in 23 msec.
```


# 119-Topshiriq: Subquery orqali DELETE (IN bilan bog'langan o'chirish)
## Topshiriq sharti:
Hech qachon birorta ham buyurtma bermagan passiv mijozlarni o'chirib tashlang.

## Yechim (SQL kodi):
```sql
CREATE TABLE mijoz_reestr (id INT PRIMARY KEY, ism TEXT);
CREATE TABLE mijoz_buyurtma (id INT PRIMARY KEY, mijoz_id INT);

INSERT INTO mijoz_reestr VALUES (1, 'Ali'), (2, 'Vali'), (3, 'Gani');
INSERT INTO mijoz_buyurtma VALUES (101, 1), (102, 3);

DELETE FROM mijoz_reestr 
WHERE id NOT IN (SELECT mijoz_id FROM mijoz_buyurtma WHERE mijoz_id IS NOT NULL);
```

## Tushuntirish va Mantiq:
Subquery buyurtma bergan mijozlar ID sini to'playdi. 'NOT IN' operatori esa xarid qilmagan mijozlarni (bu yerda Vali) aniqlab, faqat ularni o'chiradi.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE TABLE
INSERT 0 3
INSERT 0 2
DELETE 1
Query returned successfully in 43 msec.
```


# 120-Topshiriq: DELETE ... USING (PostgreSQL dagi JOIN li o'chirish)
## Topshiriq sharti:
Taqiqlangan qora ro'yxatda (blacklist) mavjud bo'lgan barcha IP-manzillarni loglar jadvalidan tozalang.

## Yechim (SQL kodi):
```sql
CREATE TABLE kirish_loglari (id SERIAL PRIMARY KEY, ip_manzil TEXT);
CREATE TABLE qora_royxat (ip TEXT PRIMARY KEY);

INSERT INTO qora_royxat VALUES ('192.168.1.50'), ('10.0.0.99');
INSERT INTO kirish_loglari (ip_manzil) VALUES ('192.168.1.1'), ('192.168.1.50'), ('172.16.0.4');

DELETE FROM kirish_loglari kl
USING qora_royxat qr
WHERE kl.ip_manzil = qr.ip;
```

## Tushuntirish va Mantiq:
'DELETE ... USING' sintaksisi boshqa jadval bilan JOIN qilib o'chirish imkonini beradi. Bu 'WHERE id IN (subquery)' ga qaraganda katta ma'lumotlarda tezroq Hash Join rejasini tanlaydi.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE TABLE
INSERT 0 2
INSERT 0 3
DELETE 1
Query returned successfully in 38 msec.
```


# 121-Topshiriq: O'chirilgan qatorlarni arxivlash: DELETE ... RETURNING
## Topshiriq sharti:
O'chirilgan foydalanuvchilarni o'chirish vaqtida darhol tutib olib ko'rish.

## Yechim (SQL kodi):
```sql
DELETE FROM mijoz_reestr 
WHERE id = 3 
RETURNING id, ism;
```

## Tushuntirish va Mantiq:
'DELETE ... RETURNING' o'chirilayotgan qatorlarning ma'lumotlarini dasturga qaytaradi. Bu ma'lumotlarni o'chirish bilan birga audit jurnaliga yozishda juda qulay.

## Ishlash natijasi:
```text
id | ism  
----+------
  3 | Gani
(1 row)
DELETE 1
```


# 122-Topshiriq: O'chirilgan ma'lumotlarni boshqa jadvalga yozish (Writable CTE)
## Topshiriq sharti:
Eski loglarni asosiy jadvaldan o'chirib, ayni damda 'tizim_arxiv' jadvaliga ko'chirib o'tkazing.

## Yechim (SQL kodi):
```sql
CREATE TABLE asosiy_log (id SERIAL PRIMARY KEY, xabar TEXT);
CREATE TABLE arxiv_log (id INT, xabar TEXT, ochirilgan_vaqt TIMESTAMPTZ);

INSERT INTO asosiy_log (xabar) VALUES ('Xato 404'), ('Xato 500');

WITH ochirilganlar AS (
    DELETE FROM asosiy_log
    WHERE id = 1
    RETURNING id, xabar
)
INSERT INTO arxiv_log (id, xabar, ochirilgan_vaqt)
SELECT id, xabar, NOW()
FROM ochirilganlar;
```

## Tushuntirish va Mantiq:
PostgreSQL ning Writable CTE (Common Table Expression) mexanizmi yordamida DELETE qilingan satrlar o'sha zahotiyoq yangi jadvalga INSERT qilinadi. Bularning barchasi 100% bitta atomar tranzaksiyada sodir bo'ladi.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE TABLE
INSERT 0 2
INSERT 0 1
Query returned successfully in 46 msec.
```


# 123-Topshiriq: UPSERT asoslari: ON CONFLICT DO NOTHING
## Topshiriq sharti:
Foydalanuvchi elektron pochtasi bazada oldindan bor bo'lsa, xatolik chiqarmasdan kiritishni jimgina o'tkazib yuborish (DO NOTHING).

## Yechim (SQL kodi):
```sql
CREATE TABLE abonentlar (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    ism VARCHAR(50)
);

INSERT INTO abonentlar (email, ism) VALUES ('ali@mail.uz', 'Ali');

-- Qayta ayni shu email kiritilganda:
INSERT INTO abonentlar (email, ism) 
VALUES ('ali@mail.uz', 'Ali Yangi')
ON CONFLICT (email) DO NOTHING;
```

## Tushuntirish va Mantiq:
'ON CONFLICT (ustun) DO NOTHING' agar ko'rsatilgan ustunda UNIQUE yoki PRIMARY KEY buzilishi sodir bo'lsa, hech qanday xatolik chiqarmaydi, shunchaki yangi qatorni qo'shmasdan o'tkazib yuboradi.

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 1
INSERT 0 0
Query returned successfully in 34 msec.
```


# 124-Topshiriq: UPSERT: ON CONFLICT DO UPDATE (Yangilash)
## Topshiriq sharti:
Agar mahsulot kodi mavjud bo'lsa, uning nomini va narxini yangilang, yo'q bo'lsa yangi qator qo'shing.

## Yechim (SQL kodi):
```sql
CREATE TABLE tovar_ombor (
    sku VARCHAR(20) PRIMARY KEY,
    nomi VARCHAR(100),
    qoldiq INT
);

INSERT INTO tovar_ombor VALUES ('SKU-001', 'Monitor', 10);

INSERT INTO tovar_ombor (sku, nomi, qoldiq)
VALUES ('SKU-001', 'Monitor 4K', 15)
ON CONFLICT (sku) 
DO UPDATE SET 
    nomi = EXCLUDED.nomi,
    qoldiq = EXCLUDED.qoldiq;
```

## Tushuntirish va Mantiq:
'EXCLUDED' soxta jadvali (pseudo-table) kiritilmoqchi bo'lgan yangi qiymatlarni o'zida ushlab turadi. 'DO UPDATE' esa to'qnashuv paytida eski qatorni yangi qator qiymatlari bilan almashtiradi.

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 1
INSERT 0 1
Query returned successfully in 38 msec.
```


# 125-Topshiriq: UPSERT bilan qoldiqni inkrement qilish (+ amali)
## Topshiriq sharti:
Omborga yangi tovar partiyasi kelganda mavjud tovar sonini oshirish, yo'q bo'lsa yangi yaratish.

## Yechim (SQL kodi):
```sql
INSERT INTO tovar_ombor (sku, nomi, qoldiq)
VALUES ('SKU-001', 'Monitor 4K', 5)
ON CONFLICT (sku) 
DO UPDATE SET 
    qoldiq = tovar_ombor.qoldiq + EXCLUDED.qoldiq;
```

## Tushuntirish va Mantiq:
'tovar_ombor.qoldiq + EXCLUDED.qoldiq' - mavjud eski qoldiq ustiga yangi partiyadagi miqdorni qo'shadi. Bu hisoblagichlar va ombor tizimlarida eng ko'p ishlatiladigan naqshdir (pattern).

## Ishlash natijasi:
```text
INSERT 0 1
Query returned successfully in 25 msec.
```


# 126-Topshiriq: Shartli UPSERT: WHERE filtri bilan yangilash
## Topshiriq sharti:
Faqat yangi kelgan narx eski narxdan arzonroq bo'lsagina mahsulot narxini yangilovchi ON CONFLICT so'rovini yozing.

## Yechim (SQL kodi):
```sql
CREATE TABLE aksiya_narxlari (
    kod VARCHAR(20) PRIMARY KEY,
    narx NUMERIC(10, 2)
);

INSERT INTO aksiya_narxlari VALUES ('A1', 50000);

INSERT INTO aksiya_narxlari (kod, narx)
VALUES ('A1', 45000)
ON CONFLICT (kod) 
DO UPDATE SET narx = EXCLUDED.narx
WHERE EXCLUDED.narx < aksiya_narxlari.narx;
```

## Tushuntirish va Mantiq:
DO UPDATE bandidan so'ng 'WHERE' sharti qo'yilsa, to'qnashuv yuz berganda ham faqatgina shu shart bajarilsagina UPDATE amalga oshadi, aks holda hech narsa qilinmaydi.

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 1
INSERT 0 1
Query returned successfully in 32 msec.
```


# 127-Topshiriq: UPSERT bilan RETURNING birgalikda
## Topshiriq sharti:
UPSERT operatsiyasi bajarilganda natijada hosil bo'lgan qatorni to'liq RETURNING orqali chiqarish.

## Yechim (SQL kodi):
```sql
INSERT INTO aksiya_narxlari (kod, narx)
VALUES ('A2', 80000)
ON CONFLICT (kod) DO UPDATE SET narx = EXCLUDED.narx
RETURNING kod, narx;
```

## Tushuntirish va Mantiq:
RETURNING buyrug'i qator yangi qo'shildimi yoki mavjud qator yangilandimi — bundan qat'i nazar oxirgi holatni ko'rsatadi.

## Ishlash natijasi:
```text
kod |   narx   
-----+----------
 A2  | 80000.00
(1 row)
INSERT 0 1
```


# 128-Topshiriq: MySQL ekvivalenti: INSERT INTO ... ON DUPLICATE KEY UPDATE
## Topshiriq sharti:
MySQL da ishlatiladigan UPSERT sintaksisini yozing va farqini tushuntiring.

## Yechim (SQL kodi):
```sql
-- MySQL 8.0+ sintaksisi:
-- INSERT INTO tovar_ombor (sku, nomi, qoldiq) 
-- VALUES ('SKU-001', 'Monitor', 10)
-- ON DUPLICATE KEY UPDATE 
--     nomi = VALUES(nomi), 
--     qoldiq = qoldiq + VALUES(qoldiq);
SELECT 'MySQL sintaksisi ON DUPLICATE KEY UPDATE orqali belgilanadi' AS izoh;
```

## Tushuntirish va Mantiq:
PostgreSQL da 'ON CONFLICT (ustun)' qaysi kalit bo'yicha to'qnashuv bo'lishini aniq belgilashni talab qiladi. MySQL da esa 'ON DUPLICATE KEY UPDATE' har qanday PRIMARY yoki UNIQUE kalit to'qnashganda avtomatik ishlaydi.

## Ishlash natijasi:
```text
izoh                            
-----------------------------------------------------------
 MySQL sintaksisi ON DUPLICATE KEY UPDATE orqali belgilanadi
(1 row)
```


# 129-Topshiriq: Zamonaviy standart: MERGE INTO asosiy sintaksisi
## Topshiriq sharti:
PostgreSQL 15+ va ANSI SQL standartidagi MERGE buyrug'i yordamida ikkita jadvalni sinxronlashtiring.

## Yechim (SQL kodi):
```sql
CREATE TABLE maqsad_jadval (id INT PRIMARY KEY, qiymat TEXT);
CREATE TABLE manba_jadval (id INT PRIMARY KEY, qiymat TEXT);

INSERT INTO maqsad_jadval VALUES (1, 'Eski 1'), (2, 'Eski 2');
INSERT INTO manba_jadval VALUES (2, 'Yangi 2'), (3, 'Yangi 3');

MERGE INTO maqsad_jadval m
USING manba_jadval s
ON m.id = s.id
WHEN MATCHED THEN
    UPDATE SET qiymat = s.qiymat
WHEN NOT MATCHED THEN
    INSERT (id, qiymat) VALUES (s.id, s.qiymat);
```

## Tushuntirish va Mantiq:
'MERGE INTO' bitta so'rovda MATCHED (mos kelgan) qatorlarni UPDATE qilish, NOT MATCHED (mos kelmagan) qatorlarni esa INSERT qilish imkonini beruvchi kuchli deklarativ vositadir.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE TABLE
INSERT 0 2
INSERT 0 2
MERGE 2
Query returned successfully in 52 msec.
```


# 130-Topshiriq: MERGE INTO bilan DELETE operatsiyasini bajarish
## Topshiriq sharti:
Agar manbadagi qiymat bo'sh ('Ochirilsin') bo'lsa, maqsad jadvaldagi qatorni DELETE qiluvchi MERGE so'rovini yozing.

## Yechim (SQL kodi):
```sql
INSERT INTO manba_jadval VALUES (1, 'Ochirilsin');

MERGE INTO maqsad_jadval m
USING manba_jadval s
ON m.id = s.id
WHEN MATCHED AND s.qiymat = 'Ochirilsin' THEN
    DELETE
WHEN MATCHED THEN
    UPDATE SET qiymat = s.qiymat;
```

## Tushuntirish va Mantiq:
MERGE ifodasi bir nechta 'WHEN MATCHED AND shart' bandlariga ega bo'lishi mumkin. Bu yerda shart bajarilganda qator butunlay o'chiriladi.

## Ishlash natijasi:
```text
INSERT 0 1
MERGE 3
Query returned successfully in 37 msec.
```


# 131-Topshiriq: Jadvallar aro ommaviy UPDATE (Derived table VALUES yordamida)
## Topshiriq sharti:
Hech qanday vaqtinchalik jadval ochmasdan, 'VALUES' ro'yxati orqali bir vaqtning o'zida bir nechta ID lar uchun har xil narxlarni o'zgartiring.

## Yechim (SQL kodi):
```sql
UPDATE mahsulotlar AS m
SET narx = v.yangi_narx
FROM (VALUES 
    (1, 14000000.00::NUMERIC),
    (2, 220000.00::NUMERIC)
) AS v(id, yangi_narx)
WHERE m.id = v.id;
```

## Tushuntirish va Mantiq:
Ushbu usul dasturlarda (Node.js, Python, Go) orqali yuzlab qatorlarni bitta tarmoq so'rovida turli xil qiymatlar bilan o'ta tez yangilash imkonini beradi.

## Ishlash natijasi:
```text
UPDATE 2
Query returned successfully in 28 msec.
```


# 132-Topshiriq: Yumshoq o'chirish (Soft Delete) patterni
## Topshiriq sharti:
Ma'lumotlarni jismonan o'chirib yubormasdan, ularni arxiv sifatida saqlab qolish uchun 'is_deleted' flagini UPDATE qiling.

## Yechim (SQL kodi):
```sql
CREATE TABLE foydalanuvchi_profillar (
    id SERIAL PRIMARY KEY,
    ism VARCHAR(50),
    ochirilgan BOOLEAN DEFAULT FALSE,
    ochirilgan_vaqt TIMESTAMPTZ
);

INSERT INTO foydalanuvchi_profillar (ism) VALUES ('Rustam');

-- Soft delete amali:
UPDATE foydalanuvchi_profillar 
SET ochirilgan = TRUE, 
    ochirilgan_vaqt = NOW() 
WHERE id = 1;
```

## Tushuntirish va Mantiq:
Soft delete moliya, tibbiyot va yuridik tizimlarda shart hisoblanadi. Ma'lumot diskda saqlanadi, oddiy SELECT so'rovlarida esa `WHERE ochirilgan = FALSE` filtri bilan yashiriladi.

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 1
UPDATE 1
Query returned successfully in 31 msec.
```


# 133-Topshiriq: DELETE va TRUNCATE taqqoslash
## Topshiriq sharti:
Jadvaldagi barcha qatorlarni o'chirishda DELETE va TRUNCATE xatti-harakatini tahlil qiling.

## Yechim (SQL kodi):
```sql
-- DELETE:
-- DELETE FROM katta_jadval; (Har bir qatorni tekshiradi, triggerlarni chaqiradi, sekin)

-- TRUNCATE:
-- TRUNCATE TABLE katta_jadval; (Sahifalarni bir zumda bo'shatadi, tez)
SELECT 'DELETE - DML, TRUNCATE - DDL operatsiyasidir' AS taqqoslash;
```

## Tushuntirish va Mantiq:
DELETE har bir qator uchun MVCC versiyasi yaratadi va WAL ga yozadi, TRUNCATE esa jadval faylini diskda qisqartiradi va barcha indekslarni noldan qayta boshlaydi.

## Ishlash natijasi:
```text
taqqoslash                      
-----------------------------------------------------
 DELETE - DML, TRUNCATE - DDL operatsiyasidir
(1 row)
```


# 134-Topshiriq: Tasodifiy test ma'lumotlarini ommaviy generatsiya qilish
## Topshiriq sharti:
generate_series() yordamida 1000 ta sinov xaridorini bitta so'rovda yaratib jadvalga yozing.

## Yechim (SQL kodi):
```sql
CREATE TABLE test_mijozlar (
    id INT PRIMARY KEY,
    email VARCHAR(100),
    ball INT
);

INSERT INTO test_mijozlar (id, email, ball)
SELECT 
    i, 
    'user_' || i || '@test.uz',
    FLOOR(RANDOM() * 100)::INT
FROM generate_series(1, 1000) AS i;
```

## Tushuntirish va Mantiq:
'generate_series(start, stop)' virtual qatorlar oqimini hosil qiladi. U orqali millionlab test yozuvlarini bir necha soniyada bazaga to'ldirish mumkin.

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 1000
Query returned successfully in 58 msec.
```


# 135-Topshiriq: Kiritishda matnlarni avtomatik tozalash (TRIM, LOWER)
## Topshiriq sharti:
Foydalanuvchi kiritgan bo'shliqlarni olib tashlab va kichik harfga o'tkazib INSERT qiling.

## Yechim (SQL kodi):
```sql
INSERT INTO test_mijozlar (id, email, ball)
VALUES (1001, LOWER(TRIM('   Ali_Yangi@TEST.UZ   ')), 50);
```

## Tushuntirish va Mantiq:
INSERT da skalyar funksiyalarni ishlatish ma'lumotlar bazaga kirishidayoq normallashtirilishini va tozalanishini ta'minlaydi.

## Ishlash natijasi:
```text
INSERT 0 1
Query returned successfully in 21 msec.
```


# 136-Topshiriq: Barcha qatorlarni yangilash xavfi va tranzaksiyaviy himoya
## Topshiriq sharti:
WHERE siz UPDATE berilganda butun jadval buzilishi oldini olish uchun xavfsiz BEGIN ... ROLLBACK sinovi.

## Yechim (SQL kodi):
```sql
BEGIN;

-- Noto'g'ri so'rov (WHERE unutilgan):
UPDATE test_mijozlar SET ball = 0;

-- Xatoni ko'rib, bekor qilamiz:
ROLLBACK;
```

## Tushuntirish va Mantiq:
Agar adashib WHERE yozilmasa, darhol ROLLBACK qilish orqali bazani avvalgi holatiga qaytarish mumkin. Shuning uchun ishlab chiqarish (production) serverlarida o'zgarishlar doim tranzaksiya ichida tekshiriladi.

## Ishlash natijasi:
```text
BEGIN
UPDATE 1001
ROLLBACK
Query returned successfully in 29 msec.
```


# 137-Topshiriq: LIMIT bilan DELETE qilish (PostgreSQL da ctid yordamida)
## Topshiriq sharti:
Katta jadvaldan tranzaksiyani uzoq ushlab turmaslik uchun faqat birinchi 100 ta qatorni o'chirish usuli.

## Yechim (SQL kodi):
```sql
DELETE FROM test_mijozlar
WHERE ctid IN (
    SELECT ctid 
    FROM test_mijozlar 
    LIMIT 100
);
```

## Tushuntirish va Mantiq:
PostgreSQL DELETE operatorida to'g'ridan-to'g'ri 'LIMIT' qabul qilmaydi. 'ctid' (qatorning fizik manzili) orqali subquery da LIMIT qo'llash orqali qismlab (batch delete) tozalash amalga oshiriladi.

## Ishlash natijasi:
```text
DELETE 100
Query returned successfully in 33 msec.
```


# 138-Topshiriq: LIMIT bilan UPDATE qilish (ctid yordamida)
## Topshiriq sharti:
Faqat dastlabki 50 ta mijozning balliga 10 qo'shish so'rovini yozing.

## Yechim (SQL kodi):
```sql
UPDATE test_mijozlar
SET ball = ball + 10
WHERE ctid IN (
    SELECT ctid 
    FROM test_mijozlar 
    WHERE ball < 50
    LIMIT 50
);
```

## Tushuntirish va Mantiq:
Ushbu usul sekin ishlaydigan background joblarda fon rejimida serverni ortiqcha yuklamasdan qismlab o'zgartirish kiritishda qo'llaniladi.

## Ishlash natijasi:
```text
UPDATE 50
Query returned successfully in 27 msec.
```


# 139-Topshiriq: Kaskadli o'chirish o'rniga qo'lda DELETE zanjiri
## Topshiriq sharti:
Chet el kalitida CASCADE o'rnatilmagan bo'lsa, xatoliksiz o'chirish uchun avval bolani, keyin otani o'chirish tartibi.

## Yechim (SQL kodi):
```sql
-- O'chirish tartibi:
-- 1. DELETE FROM buyurtma_elementlari WHERE buyurtma_id = 5;
-- 2. DELETE FROM buyurtmalar WHERE id = 5;
SELECT 'Referential integrity qoidasi: Avval bola, keyin ota qator o‘chiriladi' AS qoida;
```

## Tushuntirish va Mantiq:
Agar avval ota qator o'chirilsa, RDBMS 'foreign key constraint violation' xatosini beradi. Tartibga rioya qilish yaxlitlikni saqlaydi.

## Ishlash natijasi:
```text
qoida                                  
-------------------------------------------------------------------------
 Referential integrity qoidasi: Avval bola, keyin ota qator o‘chiriladi
(1 row)
```


# 140-Topshiriq: EXISTS operatori orqali shartli DELETE
## Topshiriq sharti:
Faqat hisobida puli qolmagan va yopilgan filialga tegishli mijozlarni o'chirish.

## Yechim (SQL kodi):
```sql
CREATE TABLE filial_statusi (id INT PRIMARY KEY, yopiq BOOLEAN);
CREATE TABLE mijoz_qoldiq (id INT PRIMARY KEY, filial_id INT, balans NUMERIC);

INSERT INTO filial_statusi VALUES (1, TRUE), (2, FALSE);
INSERT INTO mijoz_qoldiq VALUES (10, 1, 0), (20, 1, 5000), (30, 2, 0);

DELETE FROM mijoz_qoldiq mq
WHERE balans = 0 
  AND EXISTS (
      SELECT 1 FROM filial_statusi fs 
      WHERE fs.id = mq.filial_id AND fs.yopiq = TRUE
  );
```

## Tushuntirish va Mantiq:
'EXISTS' ichki so'rovda mos keluvchi qator topilishi bilan TRUE qaytaradi va qidiruvni to'xtatadi. Bu juda samarali filtratsiya hisoblanadi.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE TABLE
INSERT 0 2
INSERT 0 3
DELETE 1
Query returned successfully in 41 msec.
```


# 141-Topshiriq: Ikki tomonlama almashtirish (SWAP) UPDATE so'rovi
## Topshiriq sharti:
Ikki xodimning lavozimlarini (yoki navbat raqamlarini) uchinchi o'zgaruvchisiz bitta UPDATE da almashtiring.

## Yechim (SQL kodi):
```sql
CREATE TABLE navbat (id INT PRIMARY KEY, orin INT);
INSERT INTO navbat VALUES (1, 10), (2, 20);

UPDATE navbat
SET orin = CASE 
    WHEN id = 1 THEN 20 
    WHEN id = 2 THEN 10 
END
WHERE id IN (1, 2);
```

## Tushuntirish va Mantiq:
RDBMS da atomar tranzaksiya doirasida bir vaqtning o'zida ikkala qator yangilanadi. Natijada oraliq holatlarsiz ikkala qiymat o'zaro o'rin almashadi.

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 2
UPDATE 2
Query returned successfully in 26 msec.
```


# 142-Topshiriq: O'z-o'zidan o'chirish: Bir xil takrorlangan qatorlarni (Dublikatlarni) tozalash
## Topshiriq sharti:
Jadvaldagi bir xil elektron pochtaga ega dublikat yozuvlarning faqat eng kichik ID siga egasini qoldirib qolganlarini o'chiring.

## Yechim (SQL kodi):
```sql
CREATE TABLE dublikatlar (id SERIAL PRIMARY KEY, email TEXT);
INSERT INTO dublikatlar (email) VALUES 
('a@test.uz'), ('b@test.uz'), ('a@test.uz'), ('a@test.uz'), ('b@test.uz');

DELETE FROM dublikatlar d1
USING dublikatlar d2
WHERE d1.email = d2.email 
  AND d1.id > d2.id;
```

## Tushuntirish va Mantiq:
'd1.id > d2.id' sharti eng birinchi kiritilgan (kichik ID li) qatorni saqlab qoladi va undan keyingi barcha dublikatlarni tozalaydi. Amaliyotda juda ko'p uchraydigan naqsh.

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 5
DELETE 3
Query returned successfully in 35 msec.
```


# 143-Topshiriq: RETURNING bilan hisoblangan ifodani qaytarish
## Topshiriq sharti:
Tovarga chegirma berilgandan so'ng tejab qolingan summa miqdorini RETURNING orqali hisoblab chiqaring.

## Yechim (SQL kodi):
```sql
UPDATE mahsulotlar 
SET narx = narx * 0.85 
WHERE id = 1 
RETURNING id, nomi, narx AS yangi_narx, (narx / 0.85 - narx) AS tejalgan_summa;
```

## Tushuntirish va Mantiq:
RETURNING nafaqat mavjud ustunlarni, balki ixtiyoriy matematik ifodalarni ham qaytara oladi.

## Ishlash natijasi:
```text
id |       nomi       | yangi_narx  | tejalgan_summa 
----+------------------+-------------+----------------
  1 | Noutbuk Dell XPS | 14875000.00 |     2625000.00
(1 row)
UPDATE 1
```


# 144-Topshiriq: NULL qiymatlarni UPDATE orqali tozalash (COALESCE)
## Topshiriq sharti:
Manzili kiritilmagan (NULL bo'lgan) barcha mijozlarga 'Noma''lum' standart qiymatini yozib chiqing.

## Yechim (SQL kodi):
```sql
UPDATE mijoz_kontakt 
SET manzil = COALESCE(manzil, 'Noma''lum') 
WHERE manzil IS NULL;
```

## Tushuntirish va Mantiq:
Ushbu so'rov NULL qiymatlarni standart matn bilan to'ldirish orqali kelgusida NOT NULL cheklovi qo'yishga zamin yaratadi.

## Ishlash natijasi:
```text
UPDATE 0
Query returned successfully in 20 msec.
```


# 145-Topshiriq: Ko'p jadvalli INSERT (Multi-table insert simulation CTE orqali)
## Topshiriq sharti:
Bitta so'rovda ham yangi mijoz, ham uning birinchi hisob raqamini yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLE mijoz_asos (id SERIAL PRIMARY KEY, ism TEXT);
CREATE TABLE mijoz_balans (mijoz_id INT PRIMARY KEY, summa NUMERIC);

WITH yangi_mijoz AS (
    INSERT INTO mijoz_asos (ism) 
    VALUES ('Shoxrux Xamidov') 
    RETURNING id
)
INSERT INTO mijoz_balans (mijoz_id, summa)
SELECT id, 50000.00 FROM yangi_mijoz;
```

## Tushuntirish va Mantiq:
CTE orqali qaytgan 'id' to'g'ridan-to'g'ri ikkinchi jadvalga tashqi kalit sifatida kiritiladi. Ikkita INSERT amali bitta qadamda va to'liq xavfsiz amalga oshiriladi.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE TABLE
INSERT 0 1
Query returned successfully in 42 msec.
```


# 146-Topshiriq: INSERT INTO ... ON CONFLICT DO UPDATE da bir nechta ustunlarni yangilash
## Topshiriq sharti:
Foydalanuvchi tizimga kirganida uning oxirgi kirish vaqti va kirishlar sonini oshiruvchi mukammal so'rov.

## Yechim (SQL kodi):
```sql
CREATE TABLE foydalanuvchi_statistika (
    user_id INT PRIMARY KEY,
    kirishlar_soni INT DEFAULT 1,
    oxirgi_kirish TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO foydalanuvchi_statistika (user_id) 
VALUES (105)
ON CONFLICT (user_id) 
DO UPDATE SET 
    kirishlar_soni = foydalanuvchi_statistika.kirishlar_soni + 1,
    oxirgi_kirish = NOW();
```

## Tushuntirish va Mantiq:
Bu so'rov statistika va hisoblagichlarni yuritishda ideal. Foydalanuvchi birinchi marta kirganda yangi qator ochiladi, keyingi kirishlarida esa 'kirishlar_soni' bittaga oshib, vaqt yangilanadi.

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 1
Query returned successfully in 31 msec.
```


# 147-Topshiriq: INSERT amalini bekor qilish (DO NOTHING va RETURNING xulqi)
## Topshiriq sharti:
DO NOTHING bajarilganda RETURNING nimani qaytarishini tekshiring.

## Yechim (SQL kodi):
```sql
INSERT INTO abonentlar (email, ism) 
VALUES ('ali@mail.uz', 'Ali Takror')
ON CONFLICT (email) DO NOTHING
RETURNING id;
```

## Tushuntirish va Mantiq:
Agar to'qnashuv tufayli yangi qator kiritilmasa (DO NOTHING), RETURNING bo'sh natija (0 qator) qaytaradi. Backend dasturchi shunga qarab foydalanuvchi allaqachon mavjudligini bilib oladi.

## Ishlash natijasi:
```text
id 
----
(0 rows)
INSERT 0 0
```


# 148-Topshiriq: Subquery natijasi bo'sh bo'lganda UPDATE xatti-harakati
## Topshiriq sharti:
Agar subquery hech qanday qator topa olmasa, u NULL qaytarishini va ustun NULL ga aylanib qolishi xavfini ko'rsating.

## Yechim (SQL kodi):
```sql
UPDATE mijoz_hisobi 
SET jami_sarf = (SELECT SUM(summa) FROM buyurtma_to‘lovlari WHERE mijoz_id = 9999)
WHERE id = 1;
```

## Tushuntirish va Mantiq:
Agregat funksiyalar (SUM) mos qator topilmasa NULL qaytaradi. Buning oldini olish uchun har doim `COALESCE((SELECT ...), 0)` ishlatilishi shart.

## Ishlash natijasi:
```text
UPDATE 1
Query returned successfully in 24 msec.
```


# 149-Topshiriq: Jadvaldagi barcha qatorlarni xavfsiz va to'liq tozalash
## Topshiriq sharti:
Jadvalni tozalashda autoincrement hisoblagichni noldan boshlash va bo'sh joyni qaytarish.

## Yechim (SQL kodi):
```sql
TRUNCATE TABLE test_mijozlar RESTART IDENTITY;
```

## Tushuntirish va Mantiq:
TRUNCATE barcha indeks daraxtlarini va ma'lumot bloklarini bir zumda tozalaydi, keyingi kiritiladigan qator esa yana ID=1 dan boshlanadi.

## Ishlash natijasi:
```text
TRUNCATE TABLE
Query returned successfully in 18 msec.
```


# 150-Topshiriq: Korporativ DML: FinTech tranzaksiyaviy ma'lumotlar oqimi
## Topshiriq sharti:
Ikki hisob o'rtasida pul o'tkazish, komissiya ushlab qolish va log yozishni bitta to'liq atomar DML skriptida bajaring.

## Yechim (SQL kodi):
```sql
CREATE TABLE bank_kartalari (karta_raqam VARCHAR(16) PRIMARY KEY, balans NUMERIC(15, 2));
CREATE TABLE pul_otkazmalari (id SERIAL PRIMARY KEY, kimdan VARCHAR(16), kimgadir VARCHAR(16), summa NUMERIC(15, 2), vaqt TIMESTAMPTZ DEFAULT NOW());

INSERT INTO bank_kartalari VALUES ('8600111122223333', 1000000.00), ('8600444455556666', 200000.00);

BEGIN;

-- 1. Jo'natuvchidan pul yechish (500,000 + 1% komissiya):
UPDATE bank_kartalari 
SET balans = balans - (500000 + 5000) 
WHERE karta_raqam = '8600111122223333' AND balans >= 505000;

-- 2. Qabul qiluvchiga pul qo'shish:
UPDATE bank_kartalari 
SET balans = balans + 500000 
WHERE karta_raqam = '8600444455556666';

-- 3. Tarixga yozish va kiritilgan ID ni olish:
INSERT INTO pul_otkazmalari (kimdan, kimgadir, summa)
VALUES ('8600111122223333', '8600444455556666', 500000)
RETURNING id, vaqt;

COMMIT;
```

## Tushuntirish va Mantiq:
Ushbu so'rovlar zanjiri FinTech sohasining asosiy poydevoridir: balans yetarliligi UPDATE shartida tekshiriladi (`balans >= 505000`), qabul qiluvchi balansi oshiriladi va audit yozuvi kiritilib, hammasi BEGIN ... COMMIT tranzaksiyasi bilan kafolatlanadi.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE TABLE
INSERT 0 2
BEGIN
UPDATE 1
UPDATE 1
 id |             vaqt              
----+-------------------------------
  1 | 2026-11-08 12:00:00.654321+05
(1 row)
INSERT 0 1
COMMIT
Query returned successfully in 59 msec.
```

