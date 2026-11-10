import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

# List of 50 tasks for File 3: 101 - 150
# DML: Ma'lumotlarni boshqarish (INSERT, UPDATE, DELETE, RETURNING, UPSERT, MERGE)

dml_data = [
    (
        101,
        "Yagona qatorni kiritish: Ustunlar ro'yxati bilan INSERT",
        "Yangi 'mahsulotlar' jadvaliga ustunlar ro'yxatini aniq ko'rsatgan holda bitta tovar ma'lumotlarini kiriting.",
        """CREATE TABLE mahsulotlar (
    id SERIAL PRIMARY KEY,
    nomi VARCHAR(100) NOT NULL,
    narx NUMERIC(10, 2) NOT NULL,
    mavjud BOOLEAN DEFAULT TRUE
);

INSERT INTO mahsulotlar (nomi, narx, mavjud) 
VALUES ('Noutbuk Dell XPS', 15500000.00, TRUE);""",
        "Ustunlar ro'yxatini aniq ko'rsatish eng yaxshi amaliyot (best practice) hisoblanadi. Agar kelajakda jadvalga yangi ustun qo'shilsa ham, ushbu INSERT so'rovi sinmaydi va xatoliksiz ishlashda davom etadi.",
        """CREATE TABLE
INSERT 0 1
Query returned successfully in 32 msec."""
    ),
    (
        102,
        "Pozitsion INSERT (Ustunlar ro'yxatisiz)",
        "Ustun nomlarini ko'rsatmasdan jadval sxemasidagi barcha ustunlar tartibiga mos ravishda qator qo'shing.",
        """INSERT INTO mahsulotlar 
VALUES (DEFAULT, 'Simsiz sichqoncha', 180000.00, TRUE);""",
        "Ustunlar ko'rsatilmaganda qiymatlar jadval yaratilgan paytdagi ustunlar tartibida qat'iy berilishi shart. Avto-inkrement ustuniga 'DEFAULT' kaliti beriladi.",
        """INSERT 0 1
Query returned successfully in 21 msec."""
    ),
    (
        103,
        "Ko'p qatorli ommaviy INSERT (Bulk Insert)",
        "Bitta SQL so'rovi bilan 'mahsulotlar' jadvaliga birdaniga 4 ta yangi mahsulotni qo'shing.",
        """INSERT INTO mahsulotlar (nomi, narx, mavjud) VALUES 
('Klaviatura Mexanik', 450000.00, TRUE),
('Monitor 27 dyuym', 2800000.00, TRUE),
('USB fleshka 64GB', 95000.00, FALSE),
('Web kamera HD', 320000.00, TRUE);""",
        "Bitta so'rovda bir nechta qatorlarni vergul bilan ajratib kiritish tarmoq yuklamasini (network round-trip) kamaytiradi va tranzaksiya yozish xarajatlarini sezilarli tejaydi.",
        """INSERT 0 4
Query returned successfully in 28 msec."""
    ),
    (
        104,
        "Faqat sukut bo'yicha qiymatlarni kiritish: DEFAULT VALUES",
        "Barcha ustunlari DEFAULT qiymatga ega bo'lgan 'tizim_sozlamalari' jadvaliga standart qator qo'shing.",
        """CREATE TABLE tizim_sozlamalari (
    id SERIAL PRIMARY KEY,
    til VARCHAR(10) DEFAULT 'uz',
    tema VARCHAR(20) DEFAULT 'dark',
    yangilangan_vaqt TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO tizim_sozlamalari DEFAULT VALUES;""",
        "'DEFAULT VALUES' barcha ustunlarga ularning sxemadagi DEFAULT qoidasini kiritadi. Agar ustunda DEFAULT bo'lmasa, NULL yoziladi.",
        """CREATE TABLE
INSERT 0 1
Query returned successfully in 29 msec."""
    ),
    (
        105,
        "Tizim IDENTITY qiymatini majburiy kiritish: OVERRIDING SYSTEM VALUE",
        "GENERATED ALWAYS AS IDENTITY bilan yaratilgan jadvalga tashqaridan o'zimiz xohlagan aniq ID qiymatini kiritish usulini yozing.",
        """CREATE TABLE id_test (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    qiymat TEXT
);

INSERT INTO id_test (id, qiymat) 
OVERRIDING SYSTEM VALUE 
VALUES (100, 'Majburiy kiritilgan ID');""",
        "Odatda 'GENERATED ALWAYS' qo'lda ID kiritishni taqiqlaydi. 'OVERRIDING SYSTEM VALUE' iborasi esa tizimga administrator ruxsati bilan o'z ID sini kiritishga ruxsat beradi (migratsiyada juda muhim).",
        """CREATE TABLE
INSERT 0 1
Query returned successfully in 35 msec."""
    ),
    (
        106,
        "Yaratilgan ID ni darhol olish: RETURNING id",
        "Yangi buyurtma qo'shilganda orqa fonda hosil bo'lgan avto-inkrement 'id' sini darhol qaytarib oling.",
        """CREATE TABLE buyurtmalar_mini (
    id SERIAL PRIMARY KEY,
    mijoz VARCHAR(50),
    summa NUMERIC(10, 2)
);

INSERT INTO buyurtmalar_mini (mijoz, summa) 
VALUES ('Akmal Rustamov', 1250000.00) 
RETURNING id;""",
        "'RETURNING id' PostgreSQL ning eng mashhur imkoniyatlaridan biri bo'lib, ikkinchi 'SELECT LASTVAL()' yoki 'SELECT currval()' so'rovini yubormasdan kiritilgan ID ni shu zahoti qaytaradi. Bu race-condition holatlarini bartaraf qiladi.",
        """ id 
----
  1
(1 row)
INSERT 0 1"""
    ),
    (
        107,
        "To'liq kiritilgan qatorni qaytarish: RETURNING *",
        "Yangi ro'yxatdan o'tgan foydalanuvchini kiritib, uning barcha ustunlari (avtomatik yaratilgan sanalar va ID bilan) to'liq ro'yxatini qaytaring.",
        """CREATE TABLE mijoz_profillari (
    id BIGSERIAL PRIMARY KEY,
    login VARCHAR(50) NOT NULL,
    yaratilgan_sana TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO mijoz_profillari (login) 
VALUES ('dilshod_dev') 
RETURNING *;""",
        "'RETURNING *' yangi yaratilgan qatorning barcha qiymatlarini, shu jumladan DEFAULT orqali hosil bo'lgan vaqt va ID larni dasturga qaytaradi.",
        """ id |    login    |       yaratilgan_sana        
----+-------------+------------------------------
  1 | dilshod_dev | 2026-11-08 12:00:00.12345+05
(1 row)
INSERT 0 1"""
    ),
    (
        108,
        "Boshqa jadvaldan ma'lumot ko'chirish: INSERT INTO ... SELECT",
        "Mavjud 'mijoz_profillari' jadvalidagi barcha ma'lumotlarni 'arxiv_profillar' jadvaliga SELECT orqali to'g'ridan-to'g'ri ko'chiring.",
        """CREATE TABLE arxiv_profillar (
    id BIGINT PRIMARY KEY,
    login VARCHAR(50),
    arxivlangan_sana TIMESTAMPTZ
);

INSERT INTO arxiv_profillar (id, login, arxivlangan_sana)
SELECT id, login, NOW() 
FROM mijoz_profillari;""",
        "'INSERT INTO ... SELECT' ma'lumotlarni ilovaga yuklab olib qayta jo'natmasdan, to'g'ridan-to'g'ri server xotirasida (disk/buffer pool) bir jadvaldan ikkinchisiga o'ta tez nusxalaydi.",
        """CREATE TABLE
INSERT 0 1
Query returned successfully in 34 msec."""
    ),
    (
        109,
        "Transformatsiya bilan INSERT SELECT",
        "Talabalar ro'yxatidan faqat a'lochi talabalarni saralab, ularning ism-sharifini katta harflar bilan yangi rag'batlantirish jadvaliga yozing.",
        """CREATE TABLE barcha_talabalar (id INT, ism TEXT, ortacha_baho NUMERIC(3,1));
CREATE TABLE ragbat_royxati (talaba_id INT, katta_harf_ism TEXT);

INSERT INTO barcha_talabalar VALUES (1, 'anvar soliyev', 4.8), (2, 'bekzod aliyev', 3.5);

INSERT INTO ragbat_royxati (talaba_id, katta_harf_ism)
SELECT id, UPPER(ism) 
FROM barcha_talabalar 
WHERE ortacha_baho >= 4.5;""",
        "SELECT qismida SQL funksiyalari (UPPER, LOWER, arifmetika) va WHERE filtrlash qoidalarini qo'llab ma'lumotlarni o'zgartirgan holda yangi jadvalga kiritish mumkin.",
        """CREATE TABLE
CREATE TABLE
INSERT 0 2
INSERT 0 1
Query returned successfully in 41 msec."""
    ),
    (
        110,
        "Agregat natijasini INSERT SELECT orqali kiritish",
        "Har bir bo'lim bo'yicha jami xodimlar soni va o'rtacha maoshini hisoblab, oylik statistika jadvaliga yozing.",
        """CREATE TABLE bolim_statistikasi (
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
GROUP BY bolim_id;""",
        "Bu usul analitik va hisobot jadvallarini (data mart) davriy ravishda tezkor to'ldirish uchun keng qo'llaniladi.",
        """CREATE TABLE
CREATE TABLE
INSERT 0 3
INSERT 0 2
Query returned successfully in 45 msec."""
    ),
    (
        111,
        "Oddiy UPDATE: Bitta qatorni yangilash",
        "ID raqami 1 bo'lgan mahsulotning narxini 16,000,000 so'mga o'zgartiring.",
        """UPDATE mahsulotlar 
SET narx = 16000000.00 
WHERE id = 1;""",
        "'UPDATE ... SET ... WHERE' shartga mos keluvchi qatorlarni yangilaydi. WHERE bandi berilishi shart, aks holda jadvaldagi BARCHA qatorlar o'zgarib ketadi.",
        """UPDATE 1
Query returned successfully in 24 msec."""
    ),
    (
        112,
        "Bir vaqtning o'zida bir nechta ustunni yangilash",
        "Mijozning ham telefon raqamini, ham yashash manzilini bitta UPDATE so'rovi bilan o'zgartiring.",
        """CREATE TABLE mijoz_kontakt (id INT PRIMARY KEY, tel TEXT, manzil TEXT);
INSERT INTO mijoz_kontakt VALUES (1, '+998901112233', 'Toshkent');

UPDATE mijoz_kontakt 
SET tel = '+998998887766', 
    manzil = 'Samarqand shahri, Registon ko‘chasi 5'
WHERE id = 1;""",
        "Bir nechta ustunlarni yangilash vergul orqali yoziladi. RDBMS har bir qator uchun ushbu barcha ustunlarni yagona atomar harakatda o'zgartiradi.",
        """CREATE TABLE
INSERT 0 1
UPDATE 1
Query returned successfully in 31 msec."""
    ),
    (
        113,
        "Arifmetik ifodalar bilan UPDATE (Narxlarni 10% ga oshirish)",
        "Barcha mavjud mahsulotlarning narxini 10 foizga oshiruvchi so'rov yozing.",
        """UPDATE mahsulotlar 
SET narx = narx * 1.10 
WHERE mavjud = TRUE;""",
        "SET bandida ustunning joriy qiymatiga tayanib arifmetik ifodalar bajarish mumkin. RDBMS har bir qatorning eski narxini oladi, 1.1 ga ko'paytiradi va yangi versiyani diskka yozadi.",
        """UPDATE 4
Query returned successfully in 27 msec."""
    ),
    (
        114,
        "Subquery (ichki so'rov) yordamida UPDATE",
        "Har bir mijozning 'jami_sarflangan' ustunini uning buyurtmalar jadvalidagi to'lovlari yig'indisiga tenglashtirib yangilang.",
        """CREATE TABLE mijoz_hisobi (id INT PRIMARY KEY, jami_sarf NUMERIC(12, 2) DEFAULT 0);
CREATE TABLE buyurtma_to‘lovlari (id SERIAL PRIMARY KEY, mijoz_id INT, summa NUMERIC(12, 2));

INSERT INTO mijoz_hisobi VALUES (1, 0), (2, 0);
INSERT INTO buyurtma_to‘lovlari (mijoz_id, summa) VALUES (1, 200000), (1, 300000), (2, 150000);

UPDATE mijoz_hisobi mh
SET jami_sarf = (
    SELECT COALESCE(SUM(bt.summa), 0) 
    FROM buyurtma_to‘lovlari bt 
    WHERE bt.mijoz_id = mh.id
);""",
        "Correlated subquery har bir mijoz qatori uchun ishga tushadi, uning jami to'lovlarini hisoblaydi va natijani 'jami_sarf' ga o'zlashtiradi.",
        """CREATE TABLE
CREATE TABLE
INSERT 0 2
INSERT 0 3
UPDATE 2
Query returned successfully in 48 msec."""
    ),
    (
        115,
        "UPDATE ... FROM (PostgreSQL JOIN li yangilash)",
        "Boshqa jadvaldagi kurs qiymatidan foydalanib tovarlarning so'mdagi narxini yangilang.",
        """CREATE TABLE tovar_dollarda (id INT PRIMARY KEY, usd_narx NUMERIC(10, 2), som_narx NUMERIC(15, 2));
CREATE TABLE joriy_kurs (kurs NUMERIC(10, 2));

INSERT INTO joriy_kurs VALUES (12800.00);
INSERT INTO tovar_dollarda (id, usd_narx) VALUES (1, 100.00), (2, 250.00);

UPDATE tovar_dollarda td
SET som_narx = td.usd_narx * jk.kurs
FROM joriy_kurs jk;""",
        "PostgreSQL da 'UPDATE ... FROM boshqa_jadval' sintaksisi qo'llaniladi. Bu ANSI standartidagi murakkab subquery lardan ko'ra ancha tushunarli va tez ishlaydi.",
        """CREATE TABLE
CREATE TABLE
INSERT 0 1
INSERT 0 2
UPDATE 2
Query returned successfully in 39 msec."""
    ),
    (
        116,
        "Shartli UPDATE: CASE ifodasi bilan ommaviy yangilash",
        "Xodimlarning maoshini ularning toifasiga qarab bir so'rovda oshiring: 'A' toifaga 20%, 'B' toifaga 10%, qolganlarga 5%.",
        """CREATE TABLE xodim_toifalari (id INT PRIMARY KEY, toifa CHAR(1), maosh NUMERIC(12, 2));
INSERT INTO xodim_toifalari VALUES (1, 'A', 10000000), (2, 'B', 8000000), (3, 'C', 5000000);

UPDATE xodim_toifalari
SET maosh = CASE 
    WHEN toifa = 'A' THEN maosh * 1.20
    WHEN toifa = 'B' THEN maosh * 1.10
    ELSE maosh * 1.05
END;""",
        "CASE yordamida har xil toifadagi qatorlarni alohida-alohida 3 marta UPDATE qilib o'tirmasdan, bitta to'liq jadval tekshiruvida (single table scan) barchasini birdaniga o'zgartirish mumkin.",
        """CREATE TABLE
INSERT 0 3
UPDATE 3
Query returned successfully in 36 msec."""
    ),
    (
        117,
        "UPDATE vaqtida eski va yangi qiymatlarni olish (RETURNING)",
        "Mahsulot narxi oshirilganda, uning qaysi narxdan qaysi narxga o'zgarganini RETURNING orqali ko'ring.",
        """UPDATE mahsulotlar 
SET narx = 17500000.00 
WHERE id = 1 
RETURNING id, nomi, narx AS yangi_narx;""",
        "PostgreSQL da 'UPDATE ... RETURNING' yangilangan qatorlarning eng so'nggi holatini qaytaradi. Bu foydalanuvchiga interfeysda 'Muvaffaqiyatli o'zgartirildi' deb yangi qiymatni ko'rsatishda juda qo'l keladi.",
        """ id |       nomi       | yangi_narx  
----+------------------+-------------
  1 | Noutbuk Dell XPS | 17500000.00
(1 row)
UPDATE 1"""
    ),
    (
        118,
        "Oddiy DELETE: Shart bo'yicha qatorlarni o'chirish",
        "Omborda mavjud bo'lmagan (mavjud = FALSE) tovarlarni o'chiring.",
        """DELETE FROM mahsulotlar 
WHERE mavjud = FALSE;""",
        "'DELETE FROM ... WHERE' ko'rsatilgan shartga mos keluvchi qatorlarni belgilaydi. PostgreSQL MVCC arxitekturasida qator diskdan jismonan darhol o'chirilmaydi, balki uning 'xmax' tizim ustuniga joriy tranzaksiya ID si yozilib 'o'chirilgan' deb belgilanadi.",
        """DELETE 1
Query returned successfully in 23 msec."""
    ),
    (
        119,
        "Subquery orqali DELETE (IN bilan bog'langan o'chirish)",
        "Hech qachon birorta ham buyurtma bermagan passiv mijozlarni o'chirib tashlang.",
        """CREATE TABLE mijoz_reestr (id INT PRIMARY KEY, ism TEXT);
CREATE TABLE mijoz_buyurtma (id INT PRIMARY KEY, mijoz_id INT);

INSERT INTO mijoz_reestr VALUES (1, 'Ali'), (2, 'Vali'), (3, 'Gani');
INSERT INTO mijoz_buyurtma VALUES (101, 1), (102, 3);

DELETE FROM mijoz_reestr 
WHERE id NOT IN (SELECT mijoz_id FROM mijoz_buyurtma WHERE mijoz_id IS NOT NULL);""",
        "Subquery buyurtma bergan mijozlar ID sini to'playdi. 'NOT IN' operatori esa xarid qilmagan mijozlarni (bu yerda Vali) aniqlab, faqat ularni o'chiradi.",
        """CREATE TABLE
CREATE TABLE
INSERT 0 3
INSERT 0 2
DELETE 1
Query returned successfully in 43 msec."""
    ),
    (
        120,
        "DELETE ... USING (PostgreSQL dagi JOIN li o'chirish)",
        "Taqiqlangan qora ro'yxatda (blacklist) mavjud bo'lgan barcha IP-manzillarni loglar jadvalidan tozalang.",
        """CREATE TABLE kirish_loglari (id SERIAL PRIMARY KEY, ip_manzil TEXT);
CREATE TABLE qora_royxat (ip TEXT PRIMARY KEY);

INSERT INTO qora_royxat VALUES ('192.168.1.50'), ('10.0.0.99');
INSERT INTO kirish_loglari (ip_manzil) VALUES ('192.168.1.1'), ('192.168.1.50'), ('172.16.0.4');

DELETE FROM kirish_loglari kl
USING qora_royxat qr
WHERE kl.ip_manzil = qr.ip;""",
        "'DELETE ... USING' sintaksisi boshqa jadval bilan JOIN qilib o'chirish imkonini beradi. Bu 'WHERE id IN (subquery)' ga qaraganda katta ma'lumotlarda tezroq Hash Join rejasini tanlaydi.",
        """CREATE TABLE
CREATE TABLE
INSERT 0 2
INSERT 0 3
DELETE 1
Query returned successfully in 38 msec."""
    ),
    (
        121,
        "O'chirilgan qatorlarni arxivlash: DELETE ... RETURNING",
        "O'chirilgan foydalanuvchilarni o'chirish vaqtida darhol tutib olib ko'rish.",
        """DELETE FROM mijoz_reestr 
WHERE id = 3 
RETURNING id, ism;""",
        "'DELETE ... RETURNING' o'chirilayotgan qatorlarning ma'lumotlarini dasturga qaytaradi. Bu ma'lumotlarni o'chirish bilan birga audit jurnaliga yozishda juda qulay.",
        """ id | ism  
----+------
  3 | Gani
(1 row)
DELETE 1"""
    ),
    (
        122,
        "O'chirilgan ma'lumotlarni boshqa jadvalga yozish (Writable CTE)",
        "Eski loglarni asosiy jadvaldan o'chirib, ayni damda 'tizim_arxiv' jadvaliga ko'chirib o'tkazing.",
        """CREATE TABLE asosiy_log (id SERIAL PRIMARY KEY, xabar TEXT);
CREATE TABLE arxiv_log (id INT, xabar TEXT, ochirilgan_vaqt TIMESTAMPTZ);

INSERT INTO asosiy_log (xabar) VALUES ('Xato 404'), ('Xato 500');

WITH ochirilganlar AS (
    DELETE FROM asosiy_log
    WHERE id = 1
    RETURNING id, xabar
)
INSERT INTO arxiv_log (id, xabar, ochirilgan_vaqt)
SELECT id, xabar, NOW()
FROM ochirilganlar;""",
        "PostgreSQL ning Writable CTE (Common Table Expression) mexanizmi yordamida DELETE qilingan satrlar o'sha zahotiyoq yangi jadvalga INSERT qilinadi. Bularning barchasi 100% bitta atomar tranzaksiyada sodir bo'ladi.",
        """CREATE TABLE
CREATE TABLE
INSERT 0 2
INSERT 0 1
Query returned successfully in 46 msec."""
    ),
    (
        123,
        "UPSERT asoslari: ON CONFLICT DO NOTHING",
        "Foydalanuvchi elektron pochtasi bazada oldindan bor bo'lsa, xatolik chiqarmasdan kiritishni jimgina o'tkazib yuborish (DO NOTHING).",
        """CREATE TABLE abonentlar (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    ism VARCHAR(50)
);

INSERT INTO abonentlar (email, ism) VALUES ('ali@mail.uz', 'Ali');

-- Qayta ayni shu email kiritilganda:
INSERT INTO abonentlar (email, ism) 
VALUES ('ali@mail.uz', 'Ali Yangi')
ON CONFLICT (email) DO NOTHING;""",
        "'ON CONFLICT (ustun) DO NOTHING' agar ko'rsatilgan ustunda UNIQUE yoki PRIMARY KEY buzilishi sodir bo'lsa, hech qanday xatolik chiqarmaydi, shunchaki yangi qatorni qo'shmasdan o'tkazib yuboradi.",
        """CREATE TABLE
INSERT 0 1
INSERT 0 0
Query returned successfully in 34 msec."""
    ),
    (
        124,
        "UPSERT: ON CONFLICT DO UPDATE (Yangilash)",
        "Agar mahsulot kodi mavjud bo'lsa, uning nomini va narxini yangilang, yo'q bo'lsa yangi qator qo'shing.",
        """CREATE TABLE tovar_ombor (
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
    qoldiq = EXCLUDED.qoldiq;""",
        "'EXCLUDED' soxta jadvali (pseudo-table) kiritilmoqchi bo'lgan yangi qiymatlarni o'zida ushlab turadi. 'DO UPDATE' esa to'qnashuv paytida eski qatorni yangi qator qiymatlari bilan almashtiradi.",
        """CREATE TABLE
INSERT 0 1
INSERT 0 1
Query returned successfully in 38 msec."""
    ),
    (
        125,
        "UPSERT bilan qoldiqni inkrement qilish (+ amali)",
        "Omborga yangi tovar partiyasi kelganda mavjud tovar sonini oshirish, yo'q bo'lsa yangi yaratish.",
        """INSERT INTO tovar_ombor (sku, nomi, qoldiq)
VALUES ('SKU-001', 'Monitor 4K', 5)
ON CONFLICT (sku) 
DO UPDATE SET 
    qoldiq = tovar_ombor.qoldiq + EXCLUDED.qoldiq;""",
        "'tovar_ombor.qoldiq + EXCLUDED.qoldiq' - mavjud eski qoldiq ustiga yangi partiyadagi miqdorni qo'shadi. Bu hisoblagichlar va ombor tizimlarida eng ko'p ishlatiladigan naqshdir (pattern).",
        """INSERT 0 1
Query returned successfully in 25 msec."""
    ),
    (
        126,
        "Shartli UPSERT: WHERE filtri bilan yangilash",
        "Faqat yangi kelgan narx eski narxdan arzonroq bo'lsagina mahsulot narxini yangilovchi ON CONFLICT so'rovini yozing.",
        """CREATE TABLE aksiya_narxlari (
    kod VARCHAR(20) PRIMARY KEY,
    narx NUMERIC(10, 2)
);

INSERT INTO aksiya_narxlari VALUES ('A1', 50000);

INSERT INTO aksiya_narxlari (kod, narx)
VALUES ('A1', 45000)
ON CONFLICT (kod) 
DO UPDATE SET narx = EXCLUDED.narx
WHERE EXCLUDED.narx < aksiya_narxlari.narx;""",
        "DO UPDATE bandidan so'ng 'WHERE' sharti qo'yilsa, to'qnashuv yuz berganda ham faqatgina shu shart bajarilsagina UPDATE amalga oshadi, aks holda hech narsa qilinmaydi.",
        """CREATE TABLE
INSERT 0 1
INSERT 0 1
Query returned successfully in 32 msec."""
    ),
    (
        127,
        "UPSERT bilan RETURNING birgalikda",
        "UPSERT operatsiyasi bajarilganda natijada hosil bo'lgan qatorni to'liq RETURNING orqali chiqarish.",
        """INSERT INTO aksiya_narxlari (kod, narx)
VALUES ('A2', 80000)
ON CONFLICT (kod) DO UPDATE SET narx = EXCLUDED.narx
RETURNING kod, narx;""",
        "RETURNING buyrug'i qator yangi qo'shildimi yoki mavjud qator yangilandimi — bundan qat'i nazar oxirgi holatni ko'rsatadi.",
        """ kod |   narx   
-----+----------
 A2  | 80000.00
(1 row)
INSERT 0 1"""
    ),
    (
        128,
        "MySQL ekvivalenti: INSERT INTO ... ON DUPLICATE KEY UPDATE",
        "MySQL da ishlatiladigan UPSERT sintaksisini yozing va farqini tushuntiring.",
        """-- MySQL 8.0+ sintaksisi:
-- INSERT INTO tovar_ombor (sku, nomi, qoldiq) 
-- VALUES ('SKU-001', 'Monitor', 10)
-- ON DUPLICATE KEY UPDATE 
--     nomi = VALUES(nomi), 
--     qoldiq = qoldiq + VALUES(qoldiq);
SELECT 'MySQL sintaksisi ON DUPLICATE KEY UPDATE orqali belgilanadi' AS izoh;""",
        "PostgreSQL da 'ON CONFLICT (ustun)' qaysi kalit bo'yicha to'qnashuv bo'lishini aniq belgilashni talab qiladi. MySQL da esa 'ON DUPLICATE KEY UPDATE' har qanday PRIMARY yoki UNIQUE kalit to'qnashganda avtomatik ishlaydi.",
        """                           izoh                            
-----------------------------------------------------------
 MySQL sintaksisi ON DUPLICATE KEY UPDATE orqali belgilanadi
(1 row)"""
    ),
    (
        129,
        "Zamonaviy standart: MERGE INTO asosiy sintaksisi",
        "PostgreSQL 15+ va ANSI SQL standartidagi MERGE buyrug'i yordamida ikkita jadvalni sinxronlashtiring.",
        """CREATE TABLE maqsad_jadval (id INT PRIMARY KEY, qiymat TEXT);
CREATE TABLE manba_jadval (id INT PRIMARY KEY, qiymat TEXT);

INSERT INTO maqsad_jadval VALUES (1, 'Eski 1'), (2, 'Eski 2');
INSERT INTO manba_jadval VALUES (2, 'Yangi 2'), (3, 'Yangi 3');

MERGE INTO maqsad_jadval m
USING manba_jadval s
ON m.id = s.id
WHEN MATCHED THEN
    UPDATE SET qiymat = s.qiymat
WHEN NOT MATCHED THEN
    INSERT (id, qiymat) VALUES (s.id, s.qiymat);""",
        "'MERGE INTO' bitta so'rovda MATCHED (mos kelgan) qatorlarni UPDATE qilish, NOT MATCHED (mos kelmagan) qatorlarni esa INSERT qilish imkonini beruvchi kuchli deklarativ vositadir.",
        """CREATE TABLE
CREATE TABLE
INSERT 0 2
INSERT 0 2
MERGE 2
Query returned successfully in 52 msec."""
    ),
    (
        130,
        "MERGE INTO bilan DELETE operatsiyasini bajarish",
        "Agar manbadagi qiymat bo'sh ('Ochirilsin') bo'lsa, maqsad jadvaldagi qatorni DELETE qiluvchi MERGE so'rovini yozing.",
        """INSERT INTO manba_jadval VALUES (1, 'Ochirilsin');

MERGE INTO maqsad_jadval m
USING manba_jadval s
ON m.id = s.id
WHEN MATCHED AND s.qiymat = 'Ochirilsin' THEN
    DELETE
WHEN MATCHED THEN
    UPDATE SET qiymat = s.qiymat;""",
        "MERGE ifodasi bir nechta 'WHEN MATCHED AND shart' bandlariga ega bo'lishi mumkin. Bu yerda shart bajarilganda qator butunlay o'chiriladi.",
        """INSERT 0 1
MERGE 3
Query returned successfully in 37 msec."""
    ),
    (
        131,
        "Jadvallar aro ommaviy UPDATE (Derived table VALUES yordamida)",
        "Hech qanday vaqtinchalik jadval ochmasdan, 'VALUES' ro'yxati orqali bir vaqtning o'zida bir nechta ID lar uchun har xil narxlarni o'zgartiring.",
        """UPDATE mahsulotlar AS m
SET narx = v.yangi_narx
FROM (VALUES 
    (1, 14000000.00::NUMERIC),
    (2, 220000.00::NUMERIC)
) AS v(id, yangi_narx)
WHERE m.id = v.id;""",
        "Ushbu usul dasturlarda (Node.js, Python, Go) orqali yuzlab qatorlarni bitta tarmoq so'rovida turli xil qiymatlar bilan o'ta tez yangilash imkonini beradi.",
        """UPDATE 2
Query returned successfully in 28 msec."""
    ),
    (
        132,
        "Yumshoq o'chirish (Soft Delete) patterni",
        "Ma'lumotlarni jismonan o'chirib yubormasdan, ularni arxiv sifatida saqlab qolish uchun 'is_deleted' flagini UPDATE qiling.",
        """CREATE TABLE foydalanuvchi_profillar (
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
WHERE id = 1;""",
        "Soft delete moliya, tibbiyot va yuridik tizimlarda shart hisoblanadi. Ma'lumot diskda saqlanadi, oddiy SELECT so'rovlarida esa `WHERE ochirilgan = FALSE` filtri bilan yashiriladi.",
        """CREATE TABLE
INSERT 0 1
UPDATE 1
Query returned successfully in 31 msec."""
    ),
    (
        133,
        "DELETE va TRUNCATE taqqoslash",
        "Jadvaldagi barcha qatorlarni o'chirishda DELETE va TRUNCATE xatti-harakatini tahlil qiling.",
        """-- DELETE:
-- DELETE FROM katta_jadval; (Har bir qatorni tekshiradi, triggerlarni chaqiradi, sekin)

-- TRUNCATE:
-- TRUNCATE TABLE katta_jadval; (Sahifalarni bir zumda bo'shatadi, tez)
SELECT 'DELETE - DML, TRUNCATE - DDL operatsiyasidir' AS taqqoslash;""",
        "DELETE har bir qator uchun MVCC versiyasi yaratadi va WAL ga yozadi, TRUNCATE esa jadval faylini diskda qisqartiradi va barcha indekslarni noldan qayta boshlaydi.",
        """                     taqqoslash                      
-----------------------------------------------------
 DELETE - DML, TRUNCATE - DDL operatsiyasidir
(1 row)"""
    ),
    (
        134,
        "Tasodifiy test ma'lumotlarini ommaviy generatsiya qilish",
        "generate_series() yordamida 1000 ta sinov xaridorini bitta so'rovda yaratib jadvalga yozing.",
        """CREATE TABLE test_mijozlar (
    id INT PRIMARY KEY,
    email VARCHAR(100),
    ball INT
);

INSERT INTO test_mijozlar (id, email, ball)
SELECT 
    i, 
    'user_' || i || '@test.uz',
    FLOOR(RANDOM() * 100)::INT
FROM generate_series(1, 1000) AS i;""",
        "'generate_series(start, stop)' virtual qatorlar oqimini hosil qiladi. U orqali millionlab test yozuvlarini bir necha soniyada bazaga to'ldirish mumkin.",
        """CREATE TABLE
INSERT 0 1000
Query returned successfully in 58 msec."""
    ),
    (
        135,
        "Kiritishda matnlarni avtomatik tozalash (TRIM, LOWER)",
        "Foydalanuvchi kiritgan bo'shliqlarni olib tashlab va kichik harfga o'tkazib INSERT qiling.",
        """INSERT INTO test_mijozlar (id, email, ball)
VALUES (1001, LOWER(TRIM('   Ali_Yangi@TEST.UZ   ')), 50);""",
        "INSERT da skalyar funksiyalarni ishlatish ma'lumotlar bazaga kirishidayoq normallashtirilishini va tozalanishini ta'minlaydi.",
        """INSERT 0 1
Query returned successfully in 21 msec."""
    ),
    (
        136,
        "Barcha qatorlarni yangilash xavfi va tranzaksiyaviy himoya",
        "WHERE siz UPDATE berilganda butun jadval buzilishi oldini olish uchun xavfsiz BEGIN ... ROLLBACK sinovi.",
        """BEGIN;

-- Noto'g'ri so'rov (WHERE unutilgan):
UPDATE test_mijozlar SET ball = 0;

-- Xatoni ko'rib, bekor qilamiz:
ROLLBACK;""",
        "Agar adashib WHERE yozilmasa, darhol ROLLBACK qilish orqali bazani avvalgi holatiga qaytarish mumkin. Shuning uchun ishlab chiqarish (production) serverlarida o'zgarishlar doim tranzaksiya ichida tekshiriladi.",
        """BEGIN
UPDATE 1001
ROLLBACK
Query returned successfully in 29 msec."""
    ),
    (
        137,
        "LIMIT bilan DELETE qilish (PostgreSQL da ctid yordamida)",
        "Katta jadvaldan tranzaksiyani uzoq ushlab turmaslik uchun faqat birinchi 100 ta qatorni o'chirish usuli.",
        """DELETE FROM test_mijozlar
WHERE ctid IN (
    SELECT ctid 
    FROM test_mijozlar 
    LIMIT 100
);""",
        "PostgreSQL DELETE operatorida to'g'ridan-to'g'ri 'LIMIT' qabul qilmaydi. 'ctid' (qatorning fizik manzili) orqali subquery da LIMIT qo'llash orqali qismlab (batch delete) tozalash amalga oshiriladi.",
        """DELETE 100
Query returned successfully in 33 msec."""
    ),
    (
        138,
        "LIMIT bilan UPDATE qilish (ctid yordamida)",
        "Faqat dastlabki 50 ta mijozning balliga 10 qo'shish so'rovini yozing.",
        """UPDATE test_mijozlar
SET ball = ball + 10
WHERE ctid IN (
    SELECT ctid 
    FROM test_mijozlar 
    WHERE ball < 50
    LIMIT 50
);""",
        "Ushbu usul sekin ishlaydigan background joblarda fon rejimida serverni ortiqcha yuklamasdan qismlab o'zgartirish kiritishda qo'llaniladi.",
        """UPDATE 50
Query returned successfully in 27 msec."""
    ),
    (
        139,
        "Kaskadli o'chirish o'rniga qo'lda DELETE zanjiri",
        "Chet el kalitida CASCADE o'rnatilmagan bo'lsa, xatoliksiz o'chirish uchun avval bolani, keyin otani o'chirish tartibi.",
        """-- O'chirish tartibi:
-- 1. DELETE FROM buyurtma_elementlari WHERE buyurtma_id = 5;
-- 2. DELETE FROM buyurtmalar WHERE id = 5;
SELECT 'Referential integrity qoidasi: Avval bola, keyin ota qator o‘chiriladi' AS qoida;""",
        "Agar avval ota qator o'chirilsa, RDBMS 'foreign key constraint violation' xatosini beradi. Tartibga rioya qilish yaxlitlikni saqlaydi.",
        """                                  qoida                                  
-------------------------------------------------------------------------
 Referential integrity qoidasi: Avval bola, keyin ota qator o‘chiriladi
(1 row)"""
    ),
    (
        140,
        "EXISTS operatori orqali shartli DELETE",
        "Faqat hisobida puli qolmagan va yopilgan filialga tegishli mijozlarni o'chirish.",
        """CREATE TABLE filial_statusi (id INT PRIMARY KEY, yopiq BOOLEAN);
CREATE TABLE mijoz_qoldiq (id INT PRIMARY KEY, filial_id INT, balans NUMERIC);

INSERT INTO filial_statusi VALUES (1, TRUE), (2, FALSE);
INSERT INTO mijoz_qoldiq VALUES (10, 1, 0), (20, 1, 5000), (30, 2, 0);

DELETE FROM mijoz_qoldiq mq
WHERE balans = 0 
  AND EXISTS (
      SELECT 1 FROM filial_statusi fs 
      WHERE fs.id = mq.filial_id AND fs.yopiq = TRUE
  );""",
        "'EXISTS' ichki so'rovda mos keluvchi qator topilishi bilan TRUE qaytaradi va qidiruvni to'xtatadi. Bu juda samarali filtratsiya hisoblanadi.",
        """CREATE TABLE
CREATE TABLE
INSERT 0 2
INSERT 0 3
DELETE 1
Query returned successfully in 41 msec."""
    ),
    (
        141,
        "Ikki tomonlama almashtirish (SWAP) UPDATE so'rovi",
        "Ikki xodimning lavozimlarini (yoki navbat raqamlarini) uchinchi o'zgaruvchisiz bitta UPDATE da almashtiring.",
        """CREATE TABLE navbat (id INT PRIMARY KEY, orin INT);
INSERT INTO navbat VALUES (1, 10), (2, 20);

UPDATE navbat
SET orin = CASE 
    WHEN id = 1 THEN 20 
    WHEN id = 2 THEN 10 
END
WHERE id IN (1, 2);""",
        "RDBMS da atomar tranzaksiya doirasida bir vaqtning o'zida ikkala qator yangilanadi. Natijada oraliq holatlarsiz ikkala qiymat o'zaro o'rin almashadi.",
        """CREATE TABLE
INSERT 0 2
UPDATE 2
Query returned successfully in 26 msec."""
    ),
    (
        142,
        "O'z-o'zidan o'chirish: Bir xil takrorlangan qatorlarni (Dublikatlarni) tozalash",
        "Jadvaldagi bir xil elektron pochtaga ega dublikat yozuvlarning faqat eng kichik ID siga egasini qoldirib qolganlarini o'chiring.",
        """CREATE TABLE dublikatlar (id SERIAL PRIMARY KEY, email TEXT);
INSERT INTO dublikatlar (email) VALUES 
('a@test.uz'), ('b@test.uz'), ('a@test.uz'), ('a@test.uz'), ('b@test.uz');

DELETE FROM dublikatlar d1
USING dublikatlar d2
WHERE d1.email = d2.email 
  AND d1.id > d2.id;""",
        "'d1.id > d2.id' sharti eng birinchi kiritilgan (kichik ID li) qatorni saqlab qoladi va undan keyingi barcha dublikatlarni tozalaydi. Amaliyotda juda ko'p uchraydigan naqsh.",
        """CREATE TABLE
INSERT 0 5
DELETE 3
Query returned successfully in 35 msec."""
    ),
    (
        143,
        "RETURNING bilan hisoblangan ifodani qaytarish",
        "Tovarga chegirma berilgandan so'ng tejab qolingan summa miqdorini RETURNING orqali hisoblab chiqaring.",
        """UPDATE mahsulotlar 
SET narx = narx * 0.85 
WHERE id = 1 
RETURNING id, nomi, narx AS yangi_narx, (narx / 0.85 - narx) AS tejalgan_summa;""",
        "RETURNING nafaqat mavjud ustunlarni, balki ixtiyoriy matematik ifodalarni ham qaytara oladi.",
        """ id |       nomi       | yangi_narx  | tejalgan_summa 
----+------------------+-------------+----------------
  1 | Noutbuk Dell XPS | 14875000.00 |     2625000.00
(1 row)
UPDATE 1"""
    ),
    (
        144,
        "NULL qiymatlarni UPDATE orqali tozalash (COALESCE)",
        "Manzili kiritilmagan (NULL bo'lgan) barcha mijozlarga 'Noma''lum' standart qiymatini yozib chiqing.",
        """UPDATE mijoz_kontakt 
SET manzil = COALESCE(manzil, 'Noma''lum') 
WHERE manzil IS NULL;""",
        "Ushbu so'rov NULL qiymatlarni standart matn bilan to'ldirish orqali kelgusida NOT NULL cheklovi qo'yishga zamin yaratadi.",
        """UPDATE 0
Query returned successfully in 20 msec."""
    ),
    (
        145,
        "Ko'p jadvalli INSERT (Multi-table insert simulation CTE orqali)",
        "Bitta so'rovda ham yangi mijoz, ham uning birinchi hisob raqamini yarating.",
        """CREATE TABLE mijoz_asos (id SERIAL PRIMARY KEY, ism TEXT);
CREATE TABLE mijoz_balans (mijoz_id INT PRIMARY KEY, summa NUMERIC);

WITH yangi_mijoz AS (
    INSERT INTO mijoz_asos (ism) 
    VALUES ('Shoxrux Xamidov') 
    RETURNING id
)
INSERT INTO mijoz_balans (mijoz_id, summa)
SELECT id, 50000.00 FROM yangi_mijoz;""",
        "CTE orqali qaytgan 'id' to'g'ridan-to'g'ri ikkinchi jadvalga tashqi kalit sifatida kiritiladi. Ikkita INSERT amali bitta qadamda va to'liq xavfsiz amalga oshiriladi.",
        """CREATE TABLE
CREATE TABLE
INSERT 0 1
Query returned successfully in 42 msec."""
    ),
    (
        146,
        "INSERT INTO ... ON CONFLICT DO UPDATE da bir nechta ustunlarni yangilash",
        "Foydalanuvchi tizimga kirganida uning oxirgi kirish vaqti va kirishlar sonini oshiruvchi mukammal so'rov.",
        """CREATE TABLE foydalanuvchi_statistika (
    user_id INT PRIMARY KEY,
    kirishlar_soni INT DEFAULT 1,
    oxirgi_kirish TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO foydalanuvchi_statistika (user_id) 
VALUES (105)
ON CONFLICT (user_id) 
DO UPDATE SET 
    kirishlar_soni = foydalanuvchi_statistika.kirishlar_soni + 1,
    oxirgi_kirish = NOW();""",
        "Bu so'rov statistika va hisoblagichlarni yuritishda ideal. Foydalanuvchi birinchi marta kirganda yangi qator ochiladi, keyingi kirishlarida esa 'kirishlar_soni' bittaga oshib, vaqt yangilanadi.",
        """CREATE TABLE
INSERT 0 1
Query returned successfully in 31 msec."""
    ),
    (
        147,
        "INSERT amalini bekor qilish (DO NOTHING va RETURNING xulqi)",
        "DO NOTHING bajarilganda RETURNING nimani qaytarishini tekshiring.",
        """INSERT INTO abonentlar (email, ism) 
VALUES ('ali@mail.uz', 'Ali Takror')
ON CONFLICT (email) DO NOTHING
RETURNING id;""",
        "Agar to'qnashuv tufayli yangi qator kiritilmasa (DO NOTHING), RETURNING bo'sh natija (0 qator) qaytaradi. Backend dasturchi shunga qarab foydalanuvchi allaqachon mavjudligini bilib oladi.",
        """ id 
----
(0 rows)
INSERT 0 0"""
    ),
    (
        148,
        "Subquery natijasi bo'sh bo'lganda UPDATE xatti-harakati",
        "Agar subquery hech qanday qator topa olmasa, u NULL qaytarishini va ustun NULL ga aylanib qolishi xavfini ko'rsating.",
        """UPDATE mijoz_hisobi 
SET jami_sarf = (SELECT SUM(summa) FROM buyurtma_to‘lovlari WHERE mijoz_id = 9999)
WHERE id = 1;""",
        "Agregat funksiyalar (SUM) mos qator topilmasa NULL qaytaradi. Buning oldini olish uchun har doim `COALESCE((SELECT ...), 0)` ishlatilishi shart.",
        """UPDATE 1
Query returned successfully in 24 msec."""
    ),
    (
        149,
        "Jadvaldagi barcha qatorlarni xavfsiz va to'liq tozalash",
        "Jadvalni tozalashda autoincrement hisoblagichni noldan boshlash va bo'sh joyni qaytarish.",
        """TRUNCATE TABLE test_mijozlar RESTART IDENTITY;""",
        "TRUNCATE barcha indeks daraxtlarini va ma'lumot bloklarini bir zumda tozalaydi, keyingi kiritiladigan qator esa yana ID=1 dan boshlanadi.",
        """TRUNCATE TABLE
Query returned successfully in 18 msec."""
    ),
    (
        150,
        "Korporativ DML: FinTech tranzaksiyaviy ma'lumotlar oqimi",
        "Ikki hisob o'rtasida pul o'tkazish, komissiya ushlab qolish va log yozishni bitta to'liq atomar DML skriptida bajaring.",
        """CREATE TABLE bank_kartalari (karta_raqam VARCHAR(16) PRIMARY KEY, balans NUMERIC(15, 2));
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

COMMIT;""",
        "Ushbu so'rovlar zanjiri FinTech sohasining asosiy poydevoridir: balans yetarliligi UPDATE shartida tekshiriladi (`balans >= 505000`), qabul qiluvchi balansi oshiriladi va audit yozuvi kiritilib, hammasi BEGIN ... COMMIT tranzaksiyasi bilan kafolatlanadi.",
        """CREATE TABLE
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
Query returned successfully in 59 msec."""
    )
]

formatted = [format_task(*item) for item in dml_data]
save_file("sql_03_dml_malumotlarni_boshqarish.md", formatted)
