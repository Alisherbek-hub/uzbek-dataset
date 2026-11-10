# 1-Topshiriq: Foydalanuvchilar jadvalini yaratish (CREATE TABLE asoslari)
## Topshiriq sharti:
Tizim foydalanuvchilarini saqlash uchun 'foydalanuvchilar' (users) jadvalini yarating. Unda id (butun son, birlamchi kalit), to'liq ism (matn, 100 belgidan oshmaydigan), elektron pochta (matn) va ro'yxatdan o'tgan vaqt (sana-vaqt) ustunlari bo'lsin.

## Yechim (SQL kodi):
```sql
CREATE TABLE foydalanuvchilar (
    id INT PRIMARY KEY,
    ism VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    yaratilgan_vaqt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Tushuntirish va Mantiq:
'CREATE TABLE' buyrug'i relyatsion ma'lumotlar bazasida yangi munosabat (jadval) hosil qiladi. 'id' ustuniga 'PRIMARY KEY' cheklovi berilib, u yozuvlarning yagonaligini kafolatlaydi. 'VARCHAR(100)' o'zgaruvchan uzunlikdagi qator bo'lib, xotirani tejaydi. 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP' esa yozuv kiritilgan paytdagi server vaqtini avtomatik biriktiradi.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 45 msec.
```


# 2-Topshiriq: Katta sonlar uchun BIGINT va moliyaviy hisob-kitoblar
## Topshiriq sharti:
Bank tizimida tranzaksiyalar soni milliardlab bo'lishi mumkin. Katta hajmga mo'ljallangan 'bank_tranzaksiyalari' jadvalini yarating. Tranzaksiya id raqami uchun BIGINT turidan foydalaning.

## Yechim (SQL kodi):
```sql
CREATE TABLE bank_tranzaksiyalari (
    tranzaksiya_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    hisob_raqam BIGINT NOT NULL,
    summa NUMERIC(15, 2) NOT NULL,
    tranzaksiya_vaqti TIMESTAMPTZ DEFAULT NOW()
);
```

## Tushuntirish va Mantiq:
'BIGINT' 64-bitli butun son bo'lib, -9,223,372,036,854,775,808 dan +9,223,372,036,854,775,807 gacha bo'lgan qiymatlarni qamrab oladi. Tranzaksiya ID kabi yuqori intensivlikda o'suvchi ustunlar uchun 'INT' (32-bit, maksimal 2.1 milliard) tezda to'lib qolishi xavfi borligi sababli 'BIGINT' tanlanadi.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 38 msec.
```


# 3-Topshiriq: Kichik butun sonlar: SMALLINT bilan xotirani tejash
## Topshiriq sharti:
Talabalarning baholari (1 dan 5 gacha) yoki haftaning kunlari (1 dan 7 gacha) kabi kichik sonlar uchun 'talaba_baholari' jadvalini yarating va SMALLINT turini qo'llang.

## Yechim (SQL kodi):
```sql
CREATE TABLE talaba_baholari (
    id SERIAL PRIMARY KEY,
    talaba_id INT NOT NULL,
    fan_id INT NOT NULL,
    baho SMALLINT NOT NULL,
    semestr SMALLINT NOT NULL
);
```

## Tushuntirish va Mantiq:
'SMALLINT' 16-bit (2 bayt) xotira egallaydi (-32,768 dan 32,767 gacha). 'INT' esa 4 bayt talab qiladi. Millionlab yozuvlarga ega jadvallarda baho, oy raqami yoki status kabi chegaralangan qiymatlar uchun SMALLINT qo'llash disk va operativ xotira (RAM buffer pool) resurslarini 50% gacha tejaydi.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 32 msec.
```


# 4-Topshiriq: Aniq kasr sonlar: NUMERIC va DECIMAL turlari
## Topshiriq sharti:
Valyuta ayirboshlash va buxgalteriya balansi uchun yaxlitlashdagi xatoliklarni mutlaqo istisno qiluvchi 'valyuta_kurslari' jadvalini yarating. Kurs qiymatini aniq kasr sifatida saqlang.

## Yechim (SQL kodi):
```sql
CREATE TABLE valyuta_kurslari (
    valyuta_kodi CHAR(3) PRIMARY KEY,
    kurs NUMERIC(12, 4) NOT NULL,
    oxirgi_yangilanish TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
```

## Tushuntirish va Mantiq:
'NUMERIC(precision, scale)' yoki 'DECIMAL' turlari 'floating-point' (IEEE 754) turlaridan farqli ravishda sonlarni noaniq ikkilik ko'rinishida emas, o'nlik raqamlar shaklida saqlaydi. Bu yerda 'precision=12' umumiy raqamlar soni, 'scale=4' verguldan keyingi xonalar sonini bildiradi. Moliyaviy tizimlarda floating-point (FLOAT/REAL) qat'iyan man etiladi.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 29 msec.
```


# 5-Topshiriq: Suzuvchi vergulli sonlar: REAL va DOUBLE PRECISION
## Topshiriq sharti:
Ilmiy tadqiqotlar, GPS koordinatalari yoki ob-havo datchiklari ma'lumotlarini saqlash uchun 'ob_havo_stansiyasi' jadvalini yarating. Harorat va bosim ko'rsatkichlarini suzuvchi vergulda ifodalang.

## Yechim (SQL kodi):
```sql
CREATE TABLE ob_havo_stansiyasi (
    stansiya_id INT NOT NULL,
    qayd_vaqti TIMESTAMPTZ NOT NULL,
    harorat REAL NOT NULL,
    bosim DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (stansiya_id, qayd_vaqti)
);
```

## Tushuntirish va Mantiq:
'REAL' 4 baytli suzuvchi vergul (aniqligi 6 decimal xona), 'DOUBLE PRECISION' esa 8 baytli (aniqligi 15 decimal xona) hisoblanadi. Ular protsessorda apparat darajasida (FPU) tez hisoblanadi, biroq binary kasr tufayli mayda yaxlitlash xatoliklariga ega bo'lishi mumkin. Ilmiy ma'lumotlar va telemetriya uchun juda mos.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 34 msec.
```


# 6-Topshiriq: O'zgarmas uzunlikdagi matn: CHAR(n)
## Topshiriq sharti:
Mamlakatlar ro'yxatini saqlaydigan 'davlatlar' jadvalini yarating. ISO 3166-1 alpha-2 va alpha-3 kodlari qat'iy 2 va 3 belgidan iborat bo'lgani sababli CHAR turidan foydalaning.

## Yechim (SQL kodi):
```sql
CREATE TABLE davlatlar (
    id SERIAL PRIMARY KEY,
    nomi VARCHAR(100) NOT NULL,
    iso2 CHAR(2) NOT NULL UNIQUE,
    iso3 CHAR(3) NOT NULL UNIQUE
);
```

## Tushuntirish va Mantiq:
'CHAR(n)' qat'iy belgilangan n ta belgi saqlaydi. Agar kiritilgan satr n dan kam bo'lsa, RDBMS uni bo'shliqlar (spaces) bilan oxirigacha to'ldiradi. Qiymat uzunligi har doim bir xil bo'lgan identifikatorlar (valyuta kodi 'USD', davlat kodi 'UZ', pasport seriyasi 'AA') uchun CHAR ishlatiladi.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 31 msec.
```


# 7-Topshiriq: Cheklanmagan matn: TEXT turi
## Topshiriq sharti:
Blog maqolalari, mahsulot tavsiflari yoki yuridik shartnoma matnlarini saqlash uchun 'maqolalar' jadvalini yarating. Maqola matniga uzunlik cheklovisiz TEXT turini bering.

## Yechim (SQL kodi):
```sql
CREATE TABLE maqolalar (
    maqola_id SERIAL PRIMARY KEY,
    sarlavha VARCHAR(255) NOT NULL,
    matn TEXT NOT NULL,
    chop_etilgan BOOLEAN DEFAULT FALSE
);
```

## Tushuntirish va Mantiq:
PostgreSQL da 'TEXT' va 'VARCHAR' (uzunlik ko'rsatilmagan) deyarli bir xil ichki mexanizm (TOAST - The Oversized-Attribute Storage Technique) orqali ishlaydi. Katta hajmli matnlar (odatda 2KB dan oshganda) asosiy sahifadan tashqarida siqilgan holda TOAST jadvalida saqlanadi.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 41 msec.
```


# 8-Topshiriq: Vaqt mintaqasi bilan sana va vaqt: TIMESTAMPTZ
## Topshiriq sharti:
Global miqyosda ishlaydigan xalqaro xizmatda buyurtmalar qabul qilinadi. Har bir buyurtma qaysi vaqt mintaqasida berilganidan qat'i nazar, UTC formatida yagona vaqtni ifodalovchi TIMESTAMPTZ turini qo'llang.

## Yechim (SQL kodi):
```sql
CREATE TABLE xalqaro_buyurtmalar (
    buyurtma_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    mijoz_id INT NOT NULL,
    buyurtma_sanasi TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## Tushuntirish va Mantiq:
'TIMESTAMP WITH TIME ZONE' (TIMESTAMPTZ) ma'lumotlar bazasida UTC vaqtiga o'girilib saqlanadi. Mijoz so'rov berganda esa klientning joriy 'TimeZone' sessiya sozlamasiga moslashtirib ko'rsatiladi. Bu taqsimlangan tizimlarda vaqt chalkashliklarini oldini oladi.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 48 msec.
```


# 9-Topshiriq: Faqat sana (DATE) va faqat vaqt (TIME)
## Topshiriq sharti:
Xodimlarning tug'ilgan sanasi va ish kunining boshlanish/tugash vaqtini saqlaydigan 'ish_grafigi' jadvalini yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLE ish_grafigi (
    jadval_id SERIAL PRIMARY KEY,
    xodim_id INT NOT NULL,
    ish_kuni DATE NOT NULL,
    boshlanish_vaqti TIME NOT NULL,
    tugash_vaqti TIME NOT NULL
);
```

## Tushuntirish va Mantiq:
'DATE' faqat yil, oy va kunni saqlaydi (4 bayt), vaqt qismini o'z ichiga olmaydi. 'TIME' esa soat, daqiqa, soniya va mikrosaniyalarni saqlaydi (8 bayt). Vaqt mintaqasiz kun tartibi yoki dars jadvallari uchun bu eng maqbul yechimdir.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 28 msec.
```


# 10-Topshiriq: Vaqt oraliqlari: INTERVAL turi
## Topshiriq sharti:
Mijozlarning obuna davomiyligi yoki video darslarning davomiyligini (masalan: 1 oy 15 kun, 45 daqiqa) ifodalash uchun INTERVAL turidan foydalanib 'obunalar' jadvalini yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLE obunalar (
    obuna_id SERIAL PRIMARY KEY,
    foydalanuvchi_id INT NOT NULL,
    tarif_nomi VARCHAR(50) NOT NULL,
    davomiylik INTERVAL NOT NULL,
    faollashtirilgan_sana DATE DEFAULT CURRENT_DATE
);
```

## Tushuntirish va Mantiq:
'INTERVAL' ma'lumot turi vaqt oralig'ini (oylar, kunlar, soatlar, soniyalar) saqlaydi. SQL da uning ustida to'g'ridan-to'g'ri sanalar bilan arifmetik amallar bajarish mumkin: `faollashtirilgan_sana + davomiylik AS tugash_sanasi`.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 35 msec.
```


# 11-Topshiriq: Mantiqiy qiymatlar: BOOLEAN turi
## Topshiriq sharti:
Mijoz profilining verifikatsiya qilinganligi, akkaunt bloklanganligi yoki e-mail tasdiqlanganligini ifodalovchi BOOLEAN ustunlariga ega 'akkaunt_xavfsizligi' jadvalini yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLE akkaunt_xavfsizligi (
    foydalanuvchi_id INT PRIMARY KEY,
    email_tasdiqlangan BOOLEAN NOT NULL DEFAULT FALSE,
    ikki_bosqichli_himoya BOOLEAN NOT NULL DEFAULT FALSE,
    bloklangan BOOLEAN NOT NULL DEFAULT FALSE
);
```

## Tushuntirish va Mantiq:
PostgreSQL da 'BOOLEAN' turi uch xil holatni qabul qiladi: TRUE, FALSE va NULL (noma'lum). Xotirada 1 bayt joy oladi. Shartlarda `WHERE email_tasdiqlangan` yoki `WHERE NOT bloklangan` shaklida ixcham yoziladi.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 30 msec.
```


# 12-Topshiriq: Yagona universal identifikator: UUID turi
## Topshiriq sharti:
Mikroxizmatlar (microservices) arxitekturasida ketma-ket raqamlash (1, 2, 3...) xavfsizlik va sinxronizatsiya nuqtai nazaridan xavflidir. gen_random_uuid() yordamida UUID kalitli 'to_lovlar' jadvalini tuzing.

## Yechim (SQL kodi):
```sql
CREATE TABLE to_lovlar (
    to_lov_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    mijoz_id UUID NOT NULL,
    summa NUMERIC(14, 2) NOT NULL,
    holat VARCHAR(20) DEFAULT 'kutilmoqda'
);
```

## Tushuntirish va Mantiq:
'UUID' (Universally Unique Identifier) 128-bit (16 bayt) hajmli global yagona son bo'lib, turli serverlar bir-biri bilan bog'lanmasdan turib mustaqil ravishda yagona kalitlar hosil qilishiga imkon beradi. PostgreSQL 13+ da `gen_random_uuid()` funksiyasi o'rnatilgan holda mavjud.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 43 msec.
```


# 13-Topshiriq: Zamonaviy identifikator: GENERATED ALWAYS AS IDENTITY
## Topshiriq sharti:
Eski SERIAL mexanizmi o'rniga zamonaviy SQL standartiga (SQL:2008) to'liq mos keladigan GENERATED ALWAYS AS IDENTITY yordamida 'kategoriyalar' jadvalini yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLE kategoriyalar (
    kategoriya_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    kategoriya_nomi VARCHAR(100) NOT NULL UNIQUE,
    tavsif TEXT
);
```

## Tushuntirish va Mantiq:
'GENERATED ALWAYS AS IDENTITY' ustuniga foydalanuvchi qo'lda ixtiyoriy son kirita olmaydi (agar OVERRIDING SYSTEM VALUE ko'rsatilmasa). Bu SERIAL dan ustun turadi, chunki SERIAL orqa fonda oddiy SEQUENCE yaratadi va unga to'g'ridan-to'g'ri tashqaridan xato qiymat kiritish mumkin bo'lib qoladi.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 33 msec.
```


# 14-Topshiriq: GENERATED BY DEFAULT AS IDENTITY
## Topshiriq sharti:
Tizimga ma'lumotlarni tashqi manbadan ko'chirib o'tkazish (migration) kerak bo'lganda, avtomatik raqam berish bilan birga qo'lda qiymat kiritishga ham ruxsat beruvchi IDENTITY turini 'tovar_ombori' jadvalida qo'llang.

## Yechim (SQL kodi):
```sql
CREATE TABLE tovar_ombori (
    ombor_id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    nomi VARCHAR(150) NOT NULL,
    manzil TEXT NOT NULL
);
```

## Tushuntirish va Mantiq:
'GENERATED BY DEFAULT AS IDENTITY' agar INSERT so'rovida qiymat ko'rsatilmagan bo'lsa ketma-ketlikdan (sequence) yangi raqam oladi, agar qo'lda aniq ID kiritilsa, shu kiritilgan ID ni qabul qiladi. Bu migratsiya va sinxronizatsiyada qulay.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 31 msec.
```


# 15-Topshiriq: Foydalanuvchi maxsus turlari: CREATE TYPE ... AS ENUM
## Topshiriq sharti:
Buyurtma holatlarini ('yangi', 'qabul_qilindi', 'yetkazilmoqda', 'bajarildi', 'bekor_qilindi') cheklash uchun maxsus ENUM ma'lumot turini yarating va uni 'buyurtmalar' jadvalida ishlating.

## Yechim (SQL kodi):
```sql
CREATE TYPE buyurtma_statusi AS ENUM (
    'yangi',
    'qabul_qilindi',
    'yetkazilmoqda',
    'bajarildi',
    'bekor_qilindi'
);

CREATE TABLE mijoz_buyurtmalari (
    buyurtma_id SERIAL PRIMARY KEY,
    mijoz_fio VARCHAR(150) NOT NULL,
    holat buyurtma_statusi DEFAULT 'yangi'
);
```

## Tushuntirish va Mantiq:
'ENUM' turi ma'lumotlar bazasida satr sifatida emas, ichki 4 baytli butun son sifatida indekslanadi va saqlanadi. Bu xotirani tejaydi va noto'g'ri satriy qiymat (masalan, imloviy xato bilan) kiritilishining oldini to'liq oladi.

## Ishlash natijasi:
```text
CREATE TYPE
CREATE TABLE
Query returned successfully in 55 msec.
```


# 16-Topshiriq: Ikkilik ma'lumotlar (Binary): BYTEA turi
## Topshiriq sharti:
Foydalanuvchilarning profili avatari rasmi yoki hujjatlarning kichik hajmdagi PDF fayllarini bevosita bazada saqlash uchun BYTEA turiga ega 'hujjatlar_ombori' jadvalini yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLE hujjatlar_ombori (
    hujjat_id SERIAL PRIMARY KEY,
    fayl_nomi VARCHAR(255) NOT NULL,
    mime_turi VARCHAR(100) NOT NULL,
    fayl_baytlari BYTEA NOT NULL,
    yuklangan_vaqt TIMESTAMPTZ DEFAULT NOW()
);
```

## Tushuntirish va Mantiq:
'BYTEA' (byte array) xom ikkilik (binary) ma'lumotlarni saqlashga mo'ljallangan. Garchi katta fayllarni tashqi ob'yektlar omborida (S3, MinIO) saqlash tavsiya etilsa-da, kriptografik kalitlar, barmoq izi xeshlari yoki kichik sertifikatlar uchun BYTEA ayni muddaodir.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 40 msec.
```


# 17-Topshiriq: Hisoblanuvchi ustunlar: GENERATED ALWAYS AS (...) STORED
## Topshiriq sharti:
Tovar narxi va soni asosida umumiy summani doimiy hisoblab boruvchi 'sotuv_cheki' jadvalini GENERATED STORED ustuni bilan yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLE sotuv_cheki (
    id SERIAL PRIMARY KEY,
    mahsulot_nomi VARCHAR(200) NOT NULL,
    narx NUMERIC(12, 2) NOT NULL,
    miqdor INT NOT NULL,
    umumiy_summa NUMERIC(14, 2) GENERATED ALWAYS AS (narx * miqdor) STORED
);
```

## Tushuntirish va Mantiq:
'GENERATED ALWAYS AS (ifoda) STORED' ustuni ma'lumotlar bazasi tomonidan avtomatik hisoblanadi va diskda saqlanadi. Narx yoki miqdor o'zgarganda 'umumiy_summa' avtomatik qayta hisoblanadi. Boshqa ustunlar ifodasi asosida indeks tuzishda juda qulay.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 36 msec.
```


# 18-Topshiriq: Jadvalga yangi ustun qo'shish (ALTER TABLE ADD COLUMN)
## Topshiriq sharti:
Mavjud 'foydalanuvchilar' jadvaliga foydalanuvchining telefon raqamini saqlovchi yangi ustun qo'shing.

## Yechim (SQL kodi):
```sql
ALTER TABLE foydalanuvchilar 
ADD COLUMN telefon_raqam VARCHAR(20);
```

## Tushuntirish va Mantiq:
'ALTER TABLE ... ADD COLUMN' mavjud jadval sxemasini kengaytiradi. Agar yangi ustunga 'DEFAULT' berilmagan bo'lsa, mavjud barcha qatorlarda uning qiymati NULL bo'lib qoladi. PostgreSQL 11+ da konstantali DEFAULT berilsa ham jadval bloklanmaydi (metadata update).

## Ishlash natijasi:
```text
ALTER TABLE
Query returned successfully in 22 msec.
```


# 19-Topshiriq: Jadvaldan ustunni o'chirish (ALTER TABLE DROP COLUMN)
## Topshiriq sharti:
Xavfsizlik talablariga binoan 'foydalanuvchilar' jadvalidan endi kerak bo'lmagan 'telefon_raqam' ustunini butunlay o'chirib tashlang.

## Yechim (SQL kodi):
```sql
ALTER TABLE foydalanuvchilar 
DROP COLUMN IF EXISTS telefon_raqam;
```

## Tushuntirish va Mantiq:
'ALTER TABLE ... DROP COLUMN' ustunni mantiqiy jihatdan o'chiradi. Ko'rsatilgan ustun darhol foydalanuvchilarga ko'rinmaydi. Uning diskdagi joyi esa kelgusida VACUUM jarayoni amalga oshirilganda yoki yangi yozuvlar kiritilganda qayta ishlatiladi.

## Ishlash natijasi:
```text
ALTER TABLE
Query returned successfully in 25 msec.
```


# 20-Topshiriq: Ustun ma'lumot turini o'zgartirish (ALTER COLUMN TYPE)
## Topshiriq sharti:
'kategoriyalar' jadvalidagi 'tavsif' ustunining turini VARCHAR(255) dan kengroq bo'lgan TEXT turiga o'zgartiring.

## Yechim (SQL kodi):
```sql
ALTER TABLE kategoriyalar 
ALTER COLUMN tavsif TYPE TEXT;
```

## Tushuntirish va Mantiq:
PostgreSQL da kichikroq VARCHAR dan TEXT ga yoki kattaroq VARCHAR ga o'tish jadvalni to'liq qayta yozishni (table rewrite) talab qilmaydi, chunki ikkalasining ichki xotira ko'rinishi mos keladi. Bu amaliyot katta jadvallarda soniya ulushlarida bajariladi.

## Ishlash natijasi:
```text
ALTER TABLE
Query returned successfully in 26 msec.
```


# 21-Topshiriq: USING bandi bilan ma'lumot turini konvertatsiya qilish
## Topshiriq sharti:
Matn (VARCHAR) sifatida saqlangan 'yosh' ustunini butun son (INT) turiga o'zgartirish talab etiladi. Buning uchun USING kalit so'zidan foydalaning.

## Yechim (SQL kodi):
```sql
ALTER TABLE foydalanuvchilar 
ADD COLUMN yosh_matn VARCHAR(10) DEFAULT '25';

ALTER TABLE foydalanuvchilar 
ALTER COLUMN yosh_matn TYPE INT 
USING yosh_matn::INT;
```

## Tushuntirish va Mantiq:
Agar mavjud ma'lumotlar yangi turga avtomatik o'tmasa, RDBMS xatolik qaytaradi. 'USING yosh_matn::INT' iborasi ma'lumotlar bazasiga har bir qatordagi qiymatni qaysi qoida bo'yicha yangi turga o'tkazishni buyuradi.

## Ishlash natijasi:
```text
ALTER TABLE
ALTER TABLE
Query returned successfully in 37 msec.
```


# 22-Topshiriq: Ustunga DEFAULT qiymat tayinlash va uni olib tashlash
## Topshiriq sharti:
'foydalanuvchilar' jadvalining 'yaratilgan_vaqt' ustuniga joriy vaqtni sukut bo'yicha berish, so'ngra bu DEFAULT qiymatni bekor qilish amalini bajaring.

## Yechim (SQL kodi):
```sql
ALTER TABLE foydalanuvchilar 
ALTER COLUMN yaratilgan_vaqt SET DEFAULT CURRENT_TIMESTAMP;

-- Sukut bo'yicha qiymatni olib tashlash:
ALTER TABLE foydalanuvchilar 
ALTER COLUMN yaratilgan_vaqt DROP DEFAULT;
```

## Tushuntirish va Mantiq:
'SET DEFAULT' faqat kelajakda qo'shiladigan yozuvlarga ta'sir qiladi, avval kiritilgan ma'lumotlarni o'zgartirmaydi. 'DROP DEFAULT' esa yangi qo'shiladigan yozuvlarda ushbu ustun ko'rsatilmasa, NULL tushishiga olib keladi.

## Ishlash natijasi:
```text
ALTER TABLE
ALTER TABLE
Query returned successfully in 27 msec.
```


# 23-Topshiriq: Ustunga NOT NULL cheklovini qo'shish va olib tashlash
## Topshiriq sharti:
'foydalanuvchilar' jadvalining 'ism' ustunidan NOT NULL cheklovini olib tashlang, so'ngra qayta tiklang.

## Yechim (SQL kodi):
```sql
ALTER TABLE foydalanuvchilar 
ALTER COLUMN ism DROP NOT NULL;

-- Qayta NOT NULL o'rnatish:
ALTER TABLE foydalanuvchilar 
ALTER COLUMN ism SET NOT NULL;
```

## Tushuntirish va Mantiq:
'SET NOT NULL' bajarilganda, PostgreSQL butun jadvalni tekshirib chiqadi. Agar bitta bo'lsa ham qatorda NULL qiymat uchrasa, tranzaksiya xatolik bilan to'xtatiladi. Shuning uchun avval barcha NULL qiymatlarga mos qiymat berilishi lozim.

## Ishlash natijasi:
```text
ALTER TABLE
ALTER TABLE
Query returned successfully in 31 msec.
```


# 24-Topshiriq: Ustun nomini o'zgartirish (RENAME COLUMN)
## Topshiriq sharti:
'foydalanuvchilar' jadvalidagi 'ism' ustuni nomini 'to_liq_ism' ga o'zgartiring.

## Yechim (SQL kodi):
```sql
ALTER TABLE foydalanuvchilar 
RENAME COLUMN ism TO to_liq_ism;
```

## Tushuntirish va Mantiq:
'RENAME COLUMN' faqatgina ma'lumotlar bazasining tizim katalogidagi (system catalog - pg_attribute) metadata yozuvini yangilaydi. Ma'lumotlarning o'ziga tegilmaydi va operatsiya darhol bajariladi.

## Ishlash natijasi:
```text
ALTER TABLE
Query returned successfully in 18 msec.
```


# 25-Topshiriq: Jadval nomini o'zgartirish (RENAME TO)
## Topshiriq sharti:
'foydalanuvchilar' jadvali nomini 'mijozlar' ga o'zgartiring.

## Yechim (SQL kodi):
```sql
ALTER TABLE foydalanuvchilar 
RENAME TO mijozlar;
```

## Tushuntirish va Mantiq:
Jadval nomi o'zgarganda unga tegishli indekslar, ketma-ketliklar (sequences) va cheklovlar avtomatik yangi nomga bog'lanadi. Biroq ushbu jadvalga tayanuvchi tashqi kalitlar yoki ko'rinishlar (views) qayta ko'rib chiqilishi kerak bo'lishi mumkin.

## Ishlash natijasi:
```text
ALTER TABLE
Query returned successfully in 20 msec.
```


# 26-Topshiriq: Jadvalni to'liq o'chirish: DROP TABLE va IF EXISTS
## Topshiriq sharti:
Keraksiz bo'lgan 'eski_arxiv' jadvalini agar u mavjud bo'lsa xatoliksiz o'chirish buyrug'ini yozing.

## Yechim (SQL kodi):
```sql
DROP TABLE IF EXISTS eski_arxiv;
```

## Tushuntirish va Mantiq:
'DROP TABLE' jadvalni, uning ma'lumotlarini, indekslarini va triggerlarini katalogdan butunlay yo'q qiladi. 'IF EXISTS' qo'shimchasi agar jadval oldindan mavjud bo'lmasa, dastur xatolik berib to'xtab qolishining oldini oladi (NOTICE ogohlantirish qaytaradi).

## Ishlash natijasi:
```text
NOTICE:  table "eski_arxiv" does not exist, skipping
DROP TABLE
Query returned successfully in 14 msec.
```


# 27-Topshiriq: Kaskadli o'chirish: DROP TABLE ... CASCADE
## Topshiriq sharti:
Boshqa jadvallar FOREIGN KEY orqali bog'langan 'asosiy_kategoriya' jadvalini barcha unga bog'liq cheklovlar bilan birga o'chirish kodini yozing.

## Yechim (SQL kodi):
```sql
CREATE TABLE asosiy_kategoriya (
    id INT PRIMARY KEY,
    nomi TEXT
);

CREATE TABLE ostki_kategoriya (
    id INT PRIMARY KEY,
    asosiy_id INT REFERENCES asosiy_kategoriya(id)
);

DROP TABLE asosiy_kategoriya CASCADE;
```

## Tushuntirish va Mantiq:
'CASCADE' opsiyasi berilganda, RDBMS ushbu jadvalga bog'langan tashqi kalitlarni (FOREIGN KEY constraints) yoki ushbu jadvalga tayanuvchi VIEW larni avtomatik tarzda o'chirib tashlaydi. Ehtiyotkorlik bilan qo'llanishi shart.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE TABLE
NOTICE:  drop cascades to constraint ostki_kategoriya_asosiy_id_fkey on table ostki_kategoriya
DROP TABLE
Query returned successfully in 44 msec.
```


# 28-Topshiriq: Jadvalni tezkor tozalash: TRUNCATE TABLE
## Topshiriq sharti:
Katta hajmdagi log yozuvlarini saqlovchi 'tizim_loglari' jadvalidagi barcha ma'lumotlarni soniyaning ulushlarida tozalash so'rovini yozing.

## Yechim (SQL kodi):
```sql
CREATE TABLE tizim_loglari (
    id BIGSERIAL PRIMARY KEY,
    xabar TEXT,
    sana TIMESTAMPTZ DEFAULT NOW()
);

TRUNCATE TABLE tizim_loglari;
```

## Tushuntirish va Mantiq:
'TRUNCATE' DDL operatsiyasi hisoblanadi. U 'DELETE FROM table' dan farqli o'laroq har bir qatorni alohida o'chirib chiqmaydi, balki jadval egallagan sahifalarni (data pages) operatsion tizim darajasida bo'shatadi va WAL jurnaliga minimal yozuv tushiradi. Millionlab qatorlar bir zumda tozalanadi.

## Ishlash natijasi:
```text
CREATE TABLE
TRUNCATE TABLE
Query returned successfully in 21 msec.
```


# 29-Topshiriq: TRUNCATE bilan hisoblagichni qayta ishga tushirish (RESTART IDENTITY)
## Topshiriq sharti:
'sinov_natijalari' jadvalini tozalash bilan birga uning avto-inkrement (SERIAL/IDENTITY) hisoblagichini yana 1 dan boshlanadigan holatga keltiring.

## Yechim (SQL kodi):
```sql
CREATE TABLE sinov_natijalari (
    id SERIAL PRIMARY KEY,
    qiymat VARCHAR(50)
);

TRUNCATE TABLE sinov_natijalari RESTART IDENTITY;
```

## Tushuntirish va Mantiq:
Odatda TRUNCATE qilinganda ketma-ketlik (sequence) o'z qiymatini saqlab qoladi (CONTINUE IDENTITY). 'RESTART IDENTITY' qo'shilsa, id hisoblagichi o'zining boshlang'ich qiymatiga (odatda 1 ga) qaytariladi.

## Ishlash natijasi:
```text
CREATE TABLE
TRUNCATE TABLE
Query returned successfully in 24 msec.
```


# 30-Topshiriq: Bir nechta jadvallarni bitta buyruqda tozalash
## Topshiriq sharti:
O'zaro bog'langan 'buyurtma_bosh' va 'buyurtma_tarkib' jadvallarini bir vaqtning o'zida tozalang.

## Yechim (SQL kodi):
```sql
CREATE TABLE b_bosh (id INT PRIMARY KEY);
CREATE TABLE b_tarkib (id INT PRIMARY KEY, bosh_id INT REFERENCES b_bosh(id));

TRUNCATE TABLE b_bosh, b_tarkib RESTART IDENTITY CASCADE;
```

## Tushuntirish va Mantiq:
Tashqi kalit bilan bog'langan jadvallarni oddiy TRUNCATE qilib bo'lmaydi. Bir vaqtning o'zida barcha bog'liq jadvallarni vergul bilan ko'rsatish yoki 'CASCADE' opsiyasini kiritish orqali barcha bog'liq jadvallar xatoliksiz tozalanadi.

## Ishlash natijasi:
```text
CREATE TABLE
CREATE TABLE
TRUNCATE TABLE
Query returned successfully in 32 msec.
```


# 31-Topshiriq: Boshqa jadval asosida yangi jadval yaratish (CTAS)
## Topshiriq sharti:
Barcha faol mijozlarni yangi 'faol_mijozlar' jadvaliga ko'chirib, bir vaqtning o'zida yangi jadval hosil qiling (CREATE TABLE AS SELECT).

## Yechim (SQL kodi):
```sql
CREATE TABLE barcha_mijozlar (
    id INT,
    ism VARCHAR(50),
    faol BOOLEAN
);
INSERT INTO barcha_mijozlar VALUES (1, 'Ali', TRUE), (2, 'Vali', FALSE);

CREATE TABLE faol_mijozlar AS 
SELECT id, ism 
FROM barcha_mijozlar 
WHERE faol = TRUE;
```

## Tushuntirish va Mantiq:
'CREATE TABLE AS SELECT' (CTAS) so'rovi SELECT natijasi ustunlari va ularning turlari asosida yangi jadval yaratadi va ma'lumotlarni darhol nusxalaydi. Eslatma: CTAS birlamchi kalitlar, indekslar va cheklovlarni nusxalamaydi.

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 2
SELECT 1
Query returned successfully in 42 msec.
```


# 32-Topshiriq: Jadval nusxasini faqat tuzilmasini yaratish (WITH NO DATA)
## Topshiriq sharti:
'faol_mijozlar' jadvalining tuzilmasini aynan takrorlovchi, lekin ichida hech qanday ma'lumot bo'lmagan 'mijozlar_shabloni' jadvalini yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLE mijozlar_shabloni AS 
SELECT * FROM faol_mijozlar 
WITH NO DATA;
```

## Tushuntirish va Mantiq:
'WITH NO DATA' qo'shimchasi jadval tuzilmasini (schema) SELECT natijasiga qarab yaratadi, lekin qatorlarni nusxalamaydi. Bu test jadvallari yoki oraliq bosqichlar uchun juda qulay.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 19 msec.
```


# 33-Topshiriq: Jadval sxemasini to'liq meros qilib nusxalash: LIKE ... INCLUDING ALL
## Topshiriq sharti:
Mavjud 'mijozlar' jadvalining barcha ustunlari, DEFAULT qiymatlari, cheklovlari va indekslari bilan birgalikda 'mijozlar_arxiv' jadvalini yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLE mijozlar_arxiv (
    LIKE mijozlar INCLUDING ALL
);
```

## Tushuntirish va Mantiq:
'LIKE jadval_nomi INCLUDING ALL' barcha ustunlar turlarini, DEFAULT qiymatlarini, NOT NULL va CHECK cheklovlarini hamda indekslarni to'liq yangi jadvalga ko'chiradi. Bu CTAS dan ko'ra mukammalroq nusxalash usulidir.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 27 msec.
```


# 34-Topshiriq: Vaqtinchalik jadvallar: CREATE TEMP TABLE
## Topshiriq sharti:
Faqat joriy sessiya davomida yashaydigan va sessiya yopilishi bilan o'z-o'zidan o'chib ketadigan 'vaqtinchalik_hisobot' jadvalini yarating.

## Yechim (SQL kodi):
```sql
CREATE TEMP TABLE vaqtinchalik_hisobot (
    hisobot_id INT,
    jami_foyda NUMERIC(15, 2),
    hisoblangan_vaqt TIMESTAMP DEFAULT NOW()
);
```

## Tushuntirish va Mantiq:
'CREATE TEMP TABLE' (yoki TEMPORARY) foydalanuvchining alohida ajratilgan vaqtinchalik sxemasida (pg_temp_nn) yaratiladi. Boshqa ulanishlar (connections) bu jadvalni ko'ra olmaydi va mijoz serverdan uzilganda jadval avtomatik o'chiriladi.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 16 msec.
```


# 35-Topshiriq: ON COMMIT DROP bilan tranzaksiyaviy vaqtinchalik jadval
## Topshiriq sharti:
Faqat joriy tranzaksiya (BEGIN ... COMMIT) doirasida yashaydigan va COMMIT bo'lishi bilanoq yo'qoladigan jadval yarating.

## Yechim (SQL kodi):
```sql
BEGIN;

CREATE TEMP TABLE tranzaksiya_keshi (
    kalit VARCHAR(50),
    qiymat TEXT
) ON COMMIT DROP;

INSERT INTO tranzaksiya_keshi VALUES ('token', 'xyz123abc');

COMMIT;
```

## Tushuntirish va Mantiq:
'ON COMMIT DROP' bilan yaratilgan vaqtinchalik jadval faqatgina shu tranzaksiya davomida mavjud bo'ladi. Tranzaksiya muvaffaqiyatli yakunlanishi yoki bekor qilinishi bilanoq tizim uni xotiradan tozalaydi.

## Ishlash natijasi:
```text
BEGIN
CREATE TABLE
INSERT 0 1
COMMIT
Query returned successfully in 28 msec.
```


# 36-Topshiriq: Jurnallanmaydigan jadvallar: CREATE UNLOGGED TABLE
## Topshiriq sharti:
Kesh ma'lumotlari yoki vaqtinchalik sessiya tokenlari uchun Write-Ahead Logging (WAL) yozmaydigan, o'ta tez ishlaydigan UNLOGGED jadval yarating.

## Yechim (SQL kodi):
```sql
CREATE UNLOGGED TABLE sessiya_keshi (
    sessiya_id UUID PRIMARY KEY,
    foydalanuvchi_id INT NOT NULL,
    oxirgi_faollik TIMESTAMPTZ DEFAULT NOW()
);
```

## Tushuntirish va Mantiq:
'UNLOGGED TABLE' ma'lumotlar kiritilganda diskdagi WAL jurnaliga yozilmaydi. Bu yozish tezligini 2-3 barobarga oshiradi. Biroq, agar server favqulodda o'chib qolsa (crash), qayta yuklanganda UNLOGGED jadvallar avtomatik bo'shatiladi (truncated). Keshlar uchun ideal.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 22 msec.
```


# 37-Topshiriq: Jadval va ustunlarga izoh (dokumentatsiya) yozish: COMMENT ON
## Topshiriq sharti:
Dasturchilar va ma'lumotlar tahlilchilari uchun jadval va uning ustunlariga tushuntirish izohlarini biriktiring.

## Yechim (SQL kodi):
```sql
COMMENT ON TABLE mijozlar IS 'Tizimda ro‘yxatdan o‘tgan barcha mijozlarning asosiy profillari';
COMMENT ON COLUMN mijozlar.email IS 'Mijozning asosiy tasdiqlangan elektron pochtasi';
```

## Tushuntirish va Mantiq:
'COMMENT ON' buyrug'i ma'lumotlar bazasining tizim katalogiga (pg_description) hujjatlashtirish izohlarini kiritadi. Ushbu izohlar DBeaver, pgAdmin va turli ORM larda jadvallarning vazifasini tushunishda yordam beradi.

## Ishlash natijasi:
```text
COMMENT
COMMENT
Query returned successfully in 15 msec.
```


# 38-Topshiriq: Sxemalar bilan ishlash: CREATE SCHEMA
## Topshiriq sharti:
Katta korporativ tizimda moliya modulini boshqa modullardan ajratish uchun 'moliya' nomli alohida sxema yarating va uning ichida jadval oching.

## Yechim (SQL kodi):
```sql
CREATE SCHEMA IF NOT EXISTS moliya;

CREATE TABLE moliya.hisoblar (
    hisob_id SERIAL PRIMARY KEY,
    balans NUMERIC(15, 2) DEFAULT 0.00
);
```

## Tushuntirish va Mantiq:
'SCHEMA' mantiqiy nomlar maydoni (namespace) vazifasini bajaradi. U jadvallarni guruhlash, huquqlarni chegaralash (GRANT) va bir xil nomdagi jadvallarni to'qnashuvsiz bir bazada saqlash imkonini beradi.

## Ishlash natijasi:
```text
CREATE SCHEMA
CREATE TABLE
Query returned successfully in 34 msec.
```


# 39-Topshiriq: Qidiruv yo'lini sozlash: SET search_path
## Topshiriq sharti:
Jadvallarga har doim 'moliya.jadval' deb murojaat qilmaslik uchun sessiyaning 'search_path' sozlamasini o'zgartiring.

## Yechim (SQL kodi):
```sql
SET search_path TO moliya, public;

-- Endi 'moliya.hisoblar' ga shunchaki 'hisoblar' deb so'rov berish mumkin:
SELECT * FROM hisoblar;
```

## Tushuntirish va Mantiq:
'search_path' qaysi sxemalar birinchi navbatda tekshirilishini belgilaydi (operatsion tizimdagi PATH kabi). Foydalanuvchi jadvallarni sxemasiz yozganda, PostgreSQL ularni qidiruv yo'lidagi birinchi sxemadan izlaydi.

## Ishlash natijasi:
```text
SET
 hisob_id | balans 
----------+--------
(0 rows)
```


# 40-Topshiriq: Jadvalni boshqa sxemaga ko'chirish: ALTER TABLE ... SET SCHEMA
## Topshiriq sharti:
'public' sxemasida turgan 'tizim_loglari' jadvalini 'audit' nomli yangi sxemaga ko'chiring.

## Yechim (SQL kodi):
```sql
CREATE SCHEMA IF NOT EXISTS audit;

ALTER TABLE tizim_loglari 
SET SCHEMA audit;
```

## Tushuntirish va Mantiq:
'SET SCHEMA' amali jadval ma'lumotlarini nusxalamasdan, faqatgina uning sxema bog'liqligini o'zgartiradi. Natijada jadval fizik qayta yozilmasdan bir zumda yangi sxemaga o'tkaziladi.

## Ishlash natijasi:
```text
CREATE SCHEMA
ALTER TABLE
Query returned successfully in 29 msec.
```


# 41-Topshiriq: Murakkab kompozit turlar: CREATE TYPE ... AS (...)
## Topshiriq sharti:
Ko'cha, shahar, pochta indeksidan iborat manzilni yagona strukturaviy tur sifatida saqlash uchun kompozit tur (composite type) yarating.

## Yechim (SQL kodi):
```sql
CREATE TYPE manzil_turi AS (
    shahar VARCHAR(50),
    kocha VARCHAR(100),
    uy_raqami VARCHAR(20),
    pochta_indeksi VARCHAR(10)
);

CREATE TABLE filiallar (
    filial_id SERIAL PRIMARY KEY,
    filial_nomi VARCHAR(100) NOT NULL,
    manzil manzil_turi
);
```

## Tushuntirish va Mantiq:
Kompozit tur bir nechta maydonlarni birlashtirgan obyektga o'xshaydi. Ustunga qiymat kiritishda `ROW('Toshkent', 'Amir Temur', '12-uy', '100000')` sintaksisidan foydalaniladi.

## Ishlash natijasi:
```text
CREATE TYPE
CREATE TABLE
Query returned successfully in 45 msec.
```


# 42-Topshiriq: Sana oraliqlari (Range types): DATERANGE
## Topshiriq sharti:
Mehmonxona xonalarining band qilingan kunlar oralig'ini yagona ustunda saqlash uchun DATERANGE turidan foydalanib jadval tuzing.

## Yechim (SQL kodi):
```sql
CREATE TABLE xona_bandligi (
    bandlik_id SERIAL PRIMARY KEY,
    xona_raqami INT NOT NULL,
    band_kunlar DATERANGE NOT NULL
);

INSERT INTO xona_bandligi (xona_raqami, band_kunlar)
VALUES (101, '[2026-06-01, 2026-06-10)');
```

## Tushuntirish va Mantiq:
'DATERANGE' boshlang'ich va tugash sanasini yaxlit holda saqlaydi. '[' va ']' chegaraning kirishini, '(' va ')' esa kirmasligini bildiradi. Range turlari ustida kesishish (&&), o'z ichiga olish (@>) amallarini bajarish juda oson.

## Ishlash natijasi:
```text
CREATE TABLE
INSERT 0 1
Query returned successfully in 38 msec.
```


# 43-Topshiriq: Tarmoq manzillari ma'lumot turlari: INET va CIDR
## Topshiriq sharti:
Serverga kirgan foydalanuvchilarning IPv4 va IPv6 IP-manzillarini hamda quyi tarmoq maskalarini saqlovchi 'xavfsizlik_jurnali' jadvalini yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLE xavfsizlik_jurnali (
    qayd_id BIGSERIAL PRIMARY KEY,
    foydalanuvchi_id INT,
    mijoz_ip INET NOT NULL,
    tarmoq_diapazoni CIDR
);
```

## Tushuntirish va Mantiq:
'INET' IP manzil va uning subnet maskasini saqlaydi, 'CIDR' esa tarmoq manzilining o'zini qat'iy saqlaydi. Ular manzil formatini avtomatik tekshiradi (noto'g'ri IP kiritilishidan saqlaydi) va tarmoqqa tegishlilikni (`mijoz_ip << tarmoq_diapazoni`) tekshirish imkonini beradi.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 33 msec.
```


# 44-Topshiriq: Qurilma MAC-manzillari: MACADDR turi
## Topshiriq sharti:
Ofis lokal tarmog'iga ulangan tarmoq qurilmalari (kompyuter, printer, router) jismoniy manzillarini saqlash uchun MACADDR turini ishlating.

## Yechim (SQL kodi):
```sql
CREATE TABLE tarmoq_qurilmalari (
    qurilma_id SERIAL PRIMARY KEY,
    qurilma_nomi VARCHAR(100) NOT NULL,
    mac_manzil MACADDR NOT NULL UNIQUE
);
```

## Tushuntirish va Mantiq:
'MACADDR' 6 baytli apparat manzilini saqlaydi ('08:00:2b:01:02:03' yoki '08-00-2b-01-02-03'). PostgreSQL uni to'g'ri formatda ekanligini avtomatik tekshiradi va saralashda qulaylik yaratadi.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 27 msec.
```


# 45-Topshiriq: Bit satrlari: BIT va BIT VARYING
## Topshiriq sharti:
Haftaning qaysi kunlarida xizmat ko'rsatilishini (7 ta bit: 1-ishlaydi, 0-ishlamaydi) saqlash uchun qat'iy 7 bitli ustun bilan 'grafiklar' jadvalini yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLE ishchi_kunlar_jadvali (
    id SERIAL PRIMARY KEY,
    filial_id INT NOT NULL,
    ish_kunlari BIT(7) NOT NULL -- Masalan: B'1111100' (dush-juma)
);
```

## Tushuntirish va Mantiq:
'BIT(n)' aynan n ta bitdan iborat ikkilik satrni saqlaydi. Baytlar darajasidagi mantiqiy amallar (&, |, #, ~) orqali ruxsatnomalar (permissions mask) yoki haftalik jadvallarni bir bayt ichida saqlash va tekshirish mumkin.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 29 msec.
```


# 46-Topshiriq: Valyuta turi: MONEY ma'lumot turi
## Topshiriq sharti:
Baza sozlamalaridagi milliy valyuta formatini inobatga oluvchi MONEY turidan foydalanib 'xizmat_narxlari' jadvalini tuzing.

## Yechim (SQL kodi):
```sql
CREATE TABLE xizmat_narxlari (
    xizmat_id SERIAL PRIMARY KEY,
    nomi VARCHAR(100) NOT NULL,
    narx MONEY NOT NULL
);
```

## Tushuntirish va Mantiq:
'MONEY' ma'lumot turi qiymatni qat'iy valyuta formatida saqlaydi va 'lc_monetary' sozlamasiga qarab valyuta belgisi bilan chiqaradi. Biroq xalqaro konvertatsiyalar uchun NUMERIC turi ko'proq tavsiya etiladi.

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 26 msec.
```


# 47-Topshiriq: Jadvalning tizim ustunlari bilan tanishish: ctid, xmin, xmax
## Topshiriq sharti:
PostgreSQL jadvallarida har bir qatorda ko'rinmas tizim ustunlari (ctid, xmin) mavjudligini ko'rsatuvchi so'rov yozing.

## Yechim (SQL kodi):
```sql
CREATE TABLE sinov_qatorlar (
    id INT,
    nomi TEXT
);
INSERT INTO sinov_qatorlar VALUES (1, 'Birinchi yozuv');

SELECT ctid, xmin, xmax, id, nomi 
FROM sinov_qatorlar;
```

## Tushuntirish va Mantiq:
'ctid' qatorning diskdagi fizik joylashuvini ko'rsatadi (sahifa raqami, sahifa ichidagi indeks). 'xmin' esa ushbu qatorni kiritgan tranzaksiya identifikatori bo'lib, MVCC (Multi-Version Concurrency Control) mexanizmining asosiy ustunidir.

## Ishlash natijasi:
```text
ctid  | xmin | xmax | id |      nomi      
-------+------+------+----+----------------
 (0,1) | 1205 |    0 |  1 | Birinchi yozuv
(1 row)
```


# 48-Topshiriq: Jadvalning xotiradagi to'ldirish omili: FILLFACTOR sozlamasi
## Topshiriq sharti:
Juda ko'p UPDATE bo'ladigan jadvalda sahifalar bo'sh joyini saqlab qolish (HOT - Heap-Only Tuple optimallashtirish) uchun fillfactor=70 bilan jadval yarating.

## Yechim (SQL kodi):
```sql
CREATE TABLE faol_sessiyalar (
    sessiya_id UUID PRIMARY KEY,
    oxirgi_ping TIMESTAMPTZ
) WITH (fillfactor = 70);
```

## Tushuntirish va Mantiq:
'FILLFACTOR' ma'lumot sahifasining (page) necha foizi yangi INSERT yozuvlariga ajratilishini bildiradi (standart 100%). 70% ga qo'yilsa, har bir sahifada 30% bo'sh joy qoladi. Keyinchalik qator UPDATE qilinganda, yangi versiya boshqa sahifaga ko'chmasdan shu sahifaning o'ziga sig'adi (HOT updates).

## Ishlash natijasi:
```text
CREATE TABLE
Query returned successfully in 31 msec.
```


# 49-Topshiriq: Foydalanuvchi ma'lumot turlarini o'chirish: DROP TYPE
## Topshiriq sharti:
Endi foydalanilmayotgan 'manzil_turi' kompozit turini tizimdan xatoliksiz o'chirish buyrug'ini yozing.

## Yechim (SQL kodi):
```sql
DROP TABLE IF EXISTS filiallar;
DROP TYPE IF EXISTS manzil_turi;
```

## Tushuntirish va Mantiq:
Maxsus ma'lumot turini o'chirishdan oldin, ushbu turdan foydalanayotgan barcha jadvallar va ustunlar o'chirilishi yoki ularning turlari boshqasiga o'zgartirilishi shart. Aks holda bog'liqlik xatoligi yuzaga keladi.

## Ishlash natijasi:
```text
DROP TABLE
DROP TYPE
Query returned successfully in 23 msec.
```


# 50-Topshiriq: Katta korporativ DDL: Hamkorlikdagi to'liq sxema
## Topshiriq sharti:
Logistika tizimi uchun haydovchilar, transport vositalari va marshrutlar jadvallarini to'g'ri ma'lumot turlari (UUID, VARCHAR, NUMERIC, TIMESTAMPTZ, ENUM) bilan birgalikda yaratuvchi to'liq DDL skriptini yozing.

## Yechim (SQL kodi):
```sql
CREATE TYPE haydovchi_toifasi AS ENUM ('B', 'C', 'D', 'E');

CREATE TABLE haydovchilar (
    haydovchi_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fio VARCHAR(150) NOT NULL,
    telefon VARCHAR(20) UNIQUE NOT NULL,
    guvohnoma_toifasi haydovchi_toifasi NOT NULL,
    ishga_olingan_sana DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE transport_vositalari (
    transport_id SERIAL PRIMARY KEY,
    davlat_raqami VARCHAR(15) UNIQUE NOT NULL,
    model VARCHAR(100) NOT NULL,
    yuk_kotarish_tonna NUMERIC(5, 2) NOT NULL,
    faol BOOLEAN DEFAULT TRUE
);

CREATE TABLE reyslar (
    reys_id BIGSERIAL PRIMARY KEY,
    haydovchi_id UUID NOT NULL REFERENCES haydovchilar(haydovchi_id),
    transport_id INT NOT NULL REFERENCES transport_vositalari(transport_id),
    jonash_vaqti TIMESTAMPTZ NOT NULL,
    yetib_kelish_vaqti TIMESTAMPTZ,
    masofa_km NUMERIC(8, 2) NOT NULL
);
```

## Tushuntirish va Mantiq:
Ushbu skript zamonaviy relyatsion DDL ning barcha amaliyotlarini o'zida jamlagan: xavfsiz UUID birlamchi kalitlar, qat'iy cheklovchi ENUM toifalar, aniq hisob-kitob uchun NUMERIC va xalqaro vaqt uchun TIMESTAMPTZ turlari to'g'ri va o'z o'rnida ishlatilgan.

## Ishlash natijasi:
```text
CREATE TYPE
CREATE TABLE
CREATE TABLE
CREATE TABLE
Query returned successfully in 76 msec.
```

