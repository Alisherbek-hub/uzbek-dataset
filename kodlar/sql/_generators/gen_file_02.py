import sys
import os
sys.path.append(os.path.dirname(__file__))
from task_builder import format_task, save_file

tasks = []

# List of 50 tasks for File 2: 51 - 100
# Cheklovlar (Constraints) va Yaxlitlik (Referential Integrity)

constraints_data = [
    (
        51,
        "Yagona ustunli PRIMARY KEY cheklovi",
        "Mijozlarning shaxsiy kabinet tizimi uchun 'mijoz_akkounti' jadvalini tuzing. 'mijoz_id' ustuniga inline PRIMARY KEY cheklovini bering.",
        """CREATE TABLE mijoz_akkounti (
    mijoz_id INT PRIMARY KEY,
    fio VARCHAR(100) NOT NULL,
    telefon VARCHAR(20) NOT NULL
);""",
        "'PRIMARY KEY' relyatsion bazadagi eng muhim cheklov bo'lib, har bir qatorning yagonaligini ta'minlaydi. U avtomatik ravishda 'UNIQUE' va 'NOT NULL' talablarini qondiradi va orqa fonda tezkor qidiruv uchun B-Tree indeksini yaratadi.",
        """CREATE TABLE
Query returned successfully in 28 msec."""
    ),
    (
        52,
        "Alohida nomlangan PRIMARY KEY cheklovi (CONSTRAINT bilan)",
        "PRIMARY KEY chekloviga o'zimiz xohlagan aniq nom (pk_talabalar) berib 'talabalar' jadvalini e'lon qiling.",
        """CREATE TABLE talabalar (
    talaba_id BIGINT,
    ism VARCHAR(50) NOT NULL,
    familiya VARCHAR(50) NOT NULL,
    CONSTRAINT pk_talabalar PRIMARY KEY (talaba_id)
);""",
        "Cheklovni nomlash (masalan 'pk_talabalar') ma'lumotlar bazasi administratsiyasida juda qulay. Agar cheklov buzilsa, xatolik xabarida aniq 'pk_talabalar' ko'rinadi va keyinchalik uni DROP qilish oson bo'ladi.",
        """CREATE TABLE
Query returned successfully in 31 msec."""
    ),
    (
        53,
        "Kompozit (ko'p ustunli) PRIMARY KEY",
        "Universitetda talaba ma'lum bir fanga bitta semestrda faqat bir marta yozilishi mumkin. 'kurs_yozilishlari' jadvalida (talaba_id, kurs_id, semestr) ustunlaridan iborat kompozit kalit yarating.",
        """CREATE TABLE kurs_yozilishlari (
    talaba_id INT NOT NULL,
    kurs_id INT NOT NULL,
    semestr VARCHAR(10) NOT NULL,
    yozilgan_sana DATE DEFAULT CURRENT_DATE,
    CONSTRAINT pk_kurs_yozilishlari PRIMARY KEY (talaba_id, kurs_id, semestr)
);""",
        "Kompozit birlamchi kalit bir nechta ustunlar kombinatsiyasining yagonaligini ta'minlaydi. Talaba alohida o'zi takrorlanishi mumkin, kurs ham, lekin ularning bitta semestrdagi juftligi yagona bo'lishi shart.",
        """CREATE TABLE
Query returned successfully in 35 msec."""
    ),
    (
        54,
        "Mavjud jadvalga PRIMARY KEY qo'shish (ALTER TABLE)",
        "Boshida kalitsiz yaratilgan 'tovarlar_katalogi' jadvaliga 'ALTER TABLE' orqali birlamchi kalit biriktiring.",
        """CREATE TABLE tovarlar_katalogi (
    tovar_kodi VARCHAR(20) NOT NULL,
    nomi VARCHAR(150) NOT NULL
);

ALTER TABLE tovarlar_katalogi 
ADD CONSTRAINT pk_tovarlar_katalogi PRIMARY KEY (tovar_kodi);""",
        "Mavjud jadvalga PRIMARY KEY qo'shilganda RDBMS jadvaldagi barcha qatorlarni tekshiradi: unda NULL yoki takroriy qiymatlar bo'lmasligi shart. Agar tekshiruv muvaffaqiyatli o'tsa, B-tree indeks yaratiladi.",
        """CREATE TABLE
ALTER TABLE
Query returned successfully in 41 msec."""
    ),
    (
        55,
        "PRIMARY KEY cheklovini bekor qilish (DROP CONSTRAINT)",
        "'tovarlar_katalogi' jadvalidan mavjud birlamchi kalitni o'chiring.",
        """ALTER TABLE tovarlar_katalogi 
DROP CONSTRAINT pk_tovarlar_katalogi;""",
        "'DROP CONSTRAINT' birlamchi kalit qoidasini va unga bog'liq avtomatik yaratilgan B-Tree indeksini diskdan o'chiradi. Shundan so'ng jadvalga takroriy identifikatorlar kiritish imkoni ochiladi.",
        """ALTER TABLE
Query returned successfully in 23 msec."""
    ),
    (
        56,
        "Oddiy FOREIGN KEY (Tashqi kalit)",
        "Kompaniyaning bo'limlari va xodimlarini ifodalovchi ikkita jadval yarating. Xodim qaysi bo'limga tegishli ekanligini FOREIGN KEY bilan bog'lang.",
        """CREATE TABLE bolimlar (
    bolim_id SERIAL PRIMARY KEY,
    bolim_nomi VARCHAR(100) NOT NULL
);

CREATE TABLE xodimlar (
    xodim_id SERIAL PRIMARY KEY,
    ism VARCHAR(100) NOT NULL,
    bolim_id INT REFERENCES bolimlar(bolim_id)
);""",
        "'REFERENCES bolimlar(bolim_id)' xodimlar jadvalidagi 'bolim_id' ustuniga kiritiladigan har bir son 'bolimlar' jadvalining mavjud 'bolim_id' iga mos kelishini talab qiladi. Baza mavjud bo'lmagan bo'limga xodim biriktirilishiga yo'l qo'ymaydi.",
        """CREATE TABLE
CREATE TABLE
Query returned successfully in 46 msec."""
    ),
    (
        57,
        "Nomlangan FOREIGN KEY cheklovi",
        "Tashqi kalitga tizim tomonidan beriladigan tasodifiy nom o'rniga aniq 'fk_xodim_bolim' nomini bering.",
        """CREATE TABLE xodimlar_v2 (
    xodim_id SERIAL PRIMARY KEY,
    ism VARCHAR(100) NOT NULL,
    bolim_id INT,
    CONSTRAINT fk_xodim_bolim FOREIGN KEY (bolim_id) 
        REFERENCES bolimlar(bolim_id)
);""",
        "Tashqi kalitlarga eksplitsit (ochiq) nom berish ma'lumotlar yaxlitligi buzilganda aniq xato nomini ko'rish va kelajakda ALTER TABLE orqali o'zgartirish yoki o'chirishni osonlashtiradi.",
        """CREATE TABLE
Query returned successfully in 32 msec."""
    ),
    (
        58,
        "Kaskadli o'chirish: ON DELETE CASCADE",
        "Foydalanuvchi akkaunti o'chirilganda unga tegishli barcha postlar, izohlar ham avtomatik o'chib ketishi kerak. Buni 'ON DELETE CASCADE' yordamida amalga oshiring.",
        """CREATE TABLE mualliflar (
    muallif_id SERIAL PRIMARY KEY,
    ism VARCHAR(100) NOT NULL
);

CREATE TABLE blog_postlar (
    post_id SERIAL PRIMARY KEY,
    sarlavha VARCHAR(200) NOT NULL,
    muallif_id INT REFERENCES mualliflar(muallif_id) ON DELETE CASCADE
);""",
        "'ON DELETE CASCADE' - ota jadvaldagi (mualliflar) yozuv o'chirilganda, unga havola qilgan bola jadvaldagi (blog_postlar) barcha yozuvlarni bir tranzaksiyada avtomatik tozalaydi. Bolim yetim qolishining (orphan records) oldini oladi.",
        """CREATE TABLE
CREATE TABLE
Query returned successfully in 40 msec."""
    ),
    (
        59,
        "Qiymatni NULL ga o'rnatish: ON DELETE SET NULL",
        "Bo'lim boshlig'i ishdan bo'shatilsa yoki o'chirilsa, xodimlarning bo'lim ustuni bo'sh (NULL) bo'lib qolishi lozim. ON DELETE SET NULL bilan jadval tuzing.",
        """CREATE TABLE loyihalar (
    loyiha_id SERIAL PRIMARY KEY,
    loyiha_nomi VARCHAR(100) NOT NULL,
    yetakchi_id INT REFERENCES xodimlar(xodim_id) ON DELETE SET NULL
);""",
        "'ON DELETE SET NULL' - ota qator o'chirilganda, unga bog'langan tashqi kalit qiymatini avtomatik ravishda NULL ga o'zgartiradi. Muhim shart: tashqi kalit ustuni 'NOT NULL' bo'lmasligi kerak.",
        """CREATE TABLE
Query returned successfully in 36 msec."""
    ),
    (
        60,
        "O'chirishni qat'iy taqiqlash: ON DELETE RESTRICT",
        "Agar omborda mahsulot qoldiqlari bo'lsa, mahsulot kategoriyasini o'chirishni darhol to'xtatuvchi ON DELETE RESTRICT cheklovini yozing.",
        """CREATE TABLE tovar_turkumlari (
    turkum_id SERIAL PRIMARY KEY,
    turkum_nomi VARCHAR(100) NOT NULL
);

CREATE TABLE ombor_mahsulotlari (
    mahsulot_id SERIAL PRIMARY KEY,
    turkum_id INT REFERENCES tovar_turkumlari(turkum_id) ON DELETE RESTRICT,
    nomi VARCHAR(150) NOT NULL
);""",
        "'ON DELETE RESTRICT' ota yozuv o'chirilmoqchi bo'lganda tekshiradi: agar bitta bo'lsa ham unga bog'langan bola yozuv mavjud bo'lsa, xatolik berib o'chirishni taqiqlaydi. Bu moliyaviy va ombor tizimlarida eng xavfsiz strategiyadir.",
        """CREATE TABLE
CREATE TABLE
Query returned successfully in 38 msec."""
    ),
    (
        61,
        "Kechiktirilgan tekshiruv: ON DELETE NO ACTION",
        "PostgreSQL da standart tashqi kalit xulqi bo'lgan ON DELETE NO ACTION bilan jadval yarating va uning RESTRICT dan farqini ko'rsating.",
        """CREATE TABLE buyurtma_statuslari (
    status_id INT PRIMARY KEY,
    nomi VARCHAR(50) NOT NULL
);

CREATE TABLE sotuvlar (
    sotuv_id SERIAL PRIMARY KEY,
    status_id INT REFERENCES buyurtma_statuslari(status_id) ON DELETE NO ACTION
);""",
        "'NO ACTION' va 'RESTRICT' odatda bir xil natija beradi, biroq 'NO ACTION' kechiktiriladigan (DEFERRABLE) cheklovlar bilan ishlaganda tekshiruvni tranzaksiya oxirigacha (COMMIT paytigacha) kechiktirish imkonini beradi.",
        """CREATE TABLE
CREATE TABLE
Query returned successfully in 35 msec."""
    ),
    (
        62,
        "Sukut bo'yicha qiymatga qaytarish: ON DELETE SET DEFAULT",
        "Menejer ishdan ketsa, uning mijozlarini umumiy navbatchi menejerga (ID=1) avtomatik o'tkazish uchun ON DELETE SET DEFAULT qo'llang.",
        """CREATE TABLE menejerlar (
    id INT PRIMARY KEY,
    ism VARCHAR(50)
);

CREATE TABLE korporativ_mijozlar (
    mijoz_id SERIAL PRIMARY KEY,
    nomi VARCHAR(100),
    menejer_id INT DEFAULT 1 REFERENCES menejerlar(id) ON DELETE SET DEFAULT
);""",
        "'ON DELETE SET DEFAULT' - ota yozuv o'chirilganda bola jadval ustunini uning 'DEFAULT' qoidasida ko'rsatilgan qiymatiga o'tkazadi. Bu yerda '1' raqami tizim administratori yoki umumiy navbatchi hisobiga mos keladi.",
        """CREATE TABLE
CREATE TABLE
Query returned successfully in 39 msec."""
    ),
    (
        63,
        "O'zgarishlarni kaskadlash: ON UPDATE CASCADE",
        "Ota jadvaldagi birlamchi kalit (masalan, foydalanuvchi pasport seriyasi yoki login) o'zgarganda, unga bog'liq barcha jadvallarda ham yangi qiymat avtomatik yangilansin.",
        """CREATE TABLE filial_kodlari (
    filial_kodi VARCHAR(10) PRIMARY KEY,
    shahar VARCHAR(50) NOT NULL
);

CREATE TABLE kassa_apparatlari (
    kassa_id SERIAL PRIMARY KEY,
    filial_kodi VARCHAR(10) REFERENCES filial_kodlari(filial_kodi) 
        ON UPDATE CASCADE ON DELETE RESTRICT
);""",
        "'ON UPDATE CASCADE' - birlamchi kalit qiymati o'zgarganda (UPDATE), barcha bola jadvallardagi mos tashqi kalitlarni yangi qiymatga kaskadli tarzda sinxronlashtiradi. Bu relyatsion yaxlitlikni buzmasdan saqlaydi.",
        """CREATE TABLE
CREATE TABLE
Query returned successfully in 43 msec."""
    ),
    (
        64,
        "O'z-o'ziga havola qiluvchi tashqi kalit (Self-referencing FK)",
        "Kompaniya iyerarxiyasida har bir xodimning o'z rahbari (menejeri) mavjud. Rahbarning o'zi ham xodim hisoblanadi. Buni self-referencing tashqi kalit bilan bajaring.",
        """CREATE TABLE xodimlar_daraxti (
    xodim_id INT PRIMARY KEY,
    ism VARCHAR(100) NOT NULL,
    rahbar_id INT REFERENCES xodimlar_daraxti(xodim_id) ON DELETE SET NULL
);""",
        "Self-referencing (o'ziga murojaat qiluvchi) tashqi kalit daraxtsimon (rekursiv) tuzilmalarni — tashkiliy iyerarxiya, katalog ostidagi kataloglar va cheksiz darajali menyularni ifodalashda qo'llaniladi. Bosh rahbar uchun 'rahbar_id' NULL bo'ladi.",
        """CREATE TABLE
Query returned successfully in 29 msec."""
    ),
    (
        65,
        "Bir jadvalda bir nechta FOREIGN KEY",
        "Elektron tijoratda buyurtma bir vaqtning o'zida 'mijozlar', 'kuryerlar' va 'tolov_usullari' jadvallariga bog'langan bo'ladi. Ushbu ko'p bog'lanishli jadvalni yarating.",
        """CREATE TABLE mijozlar_base (id INT PRIMARY KEY);
CREATE TABLE kuryerlar_base (id INT PRIMARY KEY);
CREATE TABLE tolov_usullari_base (id INT PRIMARY KEY);

CREATE TABLE dostavka_buyurtmalari (
    buyurtma_id BIGSERIAL PRIMARY KEY,
    mijoz_id INT NOT NULL REFERENCES mijozlar_base(id),
    kuryer_id INT REFERENCES kuryerlar_base(id),
    tolov_usuli_id INT NOT NULL REFERENCES tolov_usullari_base(id),
    buyurtma_vaqti TIMESTAMPTZ DEFAULT NOW()
);""",
        "Bitta relyatsion jadvalda bir nechta ota jadvallarga havola qiluvchi o'nlab tashqi kalitlar bo'lishi mumkin. Har bir FOREIGN KEY alohida relyatsion tekshiruvdan o'tadi va ma'lumotlar butunligini ta'minlaydi.",
        """CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
Query returned successfully in 58 msec."""
    ),
    (
        66,
        "Yagona ustunli UNIQUE cheklovi",
        "Foydalanuvchilar ro'yxatga olinganda ularning pasport raqami (JSHSHIR / PINFL) takrorlanmasligini kafolatlovchi UNIQUE cheklovini yozing.",
        """CREATE TABLE shaxslar (
    shaxs_id SERIAL PRIMARY KEY,
    jshshir CHAR(14) UNIQUE NOT NULL,
    fio VARCHAR(150) NOT NULL
);""",
        "'UNIQUE' cheklovi jadvaldagi ustun bo'yicha hech qachon bir xil ikkita qiymat bo'lmasligini talab qiladi. U avtomatik tarzda UNIQUE B-Tree indeksini yaratadi, bu esa shu ustun bo'yicha qidiruvni O(log N) tezlikka keltiradi.",
        """CREATE TABLE
Query returned successfully in 30 msec."""
    ),
    (
        67,
        "Ko'p ustunli (kompozit) UNIQUE cheklovi",
        "Kompaniyada bitta xodimga bitta loyihada faqat bitta rol biriktirilishi mumkin (masalan, 'Ali' 'CRM' loyihasida bir vaqtning o'zida ikki marta 'Dasturchi' bo'la olmaydi).",
        """CREATE TABLE loyiha_ishtirokchilari (
    id SERIAL PRIMARY KEY,
    loyiha_id INT NOT NULL,
    xodim_id INT NOT NULL,
    rol VARCHAR(50) NOT NULL,
    CONSTRAINT uq_loyiha_xodim_rol UNIQUE (loyiha_id, xodim_id, rol)
);""",
        "Kompozit UNIQUE cheklovi ko'rsatilgan barcha ustunlar birlashmasi yagona bo'lishini ta'minlaydi. Alohida xodim bir nechta loyihada, yoki loyihada bir nechta xodim bo'lishi mumkin, ammo uchtalik yagona bo'ladi.",
        """CREATE TABLE
Query returned successfully in 34 msec."""
    ),
    (
        68,
        "UNIQUE cheklovida NULL qiymatlarning o'ziga xosligi",
        "UNIQUE ustunga bir nechta NULL qiymat kiritib, SQL standartidagi NULL xulqini tushuntiring.",
        """CREATE TABLE test_unique_null (
    id INT PRIMARY KEY,
    soliq_raqami VARCHAR(20) UNIQUE
);

INSERT INTO test_unique_null VALUES (1, NULL);
INSERT INTO test_unique_null VALUES (2, NULL); -- Bu xato beradimi?

SELECT * FROM test_unique_null;""",
        "SQL:2008 standartiga ko'ra 'NULL <> NULL' hisoblanadi (noma'lumlik). Shu bois standart UNIQUE ustuniga istalgancha NULL kiritish mumkin, ular bir-birini takrorlamaydi. Agar faqat bitta NULL ruxsat etilishi kerak bo'lsa, PostgreSQL 15+ da 'UNIQUE NULLS NOT DISTINCT' qo'llanadi.",
        """ id | soliq_raqami 
----+--------------
  1 | NULL
  2 | NULL
(2 rows)"""
    ),
    (
        69,
        "PostgreSQL 15+ yangiligi: UNIQUE NULLS NOT DISTINCT",
        "Jadvalda NULL qiymat ham faqat bir marta kiritilishini ta'minlovchi yangi standart cheklovni qo'llang.",
        """CREATE TABLE shartnoma_reestr (
    reestr_id SERIAL PRIMARY KEY,
    ichki_raqam VARCHAR(50) UNIQUE NULLS NOT DISTINCT
);

INSERT INTO shartnoma_reestr (ichki_raqam) VALUES (NULL);
-- Keyingi so'rov xatolik beradi:
-- INSERT INTO shartnoma_reestr (ichki_raqam) VALUES (NULL);""",
        "PostgreSQL 15 dan boshlab kiritilgan 'NULLS NOT DISTINCT' cheklovi NULL qiymatlarni teng deb baholaydi va ustunda birdan ortiq NULL bo'lishiga yo'l qo'ymaydi. Bu biznes qoidalarini kod darajasisiz bazada toza hal qiladi.",
        """CREATE TABLE
INSERT 0 1
Query returned successfully in 31 msec."""
    ),
    (
        70,
        "Shartli (qisman) UNIQUE indeks: WHERE filtri bilan",
        "Foydalanuvchi bir vaqtning o'zida faqat bitta FAOL (is_active = true) sessiyaga ega bo'lishi mumkin. Eski yopilgan sessiyalari esa istalgancha bo'lishi mumkin.",
        """CREATE TABLE foydalanuvchi_sessiyalari (
    id BIGSERIAL PRIMARY KEY,
    foydalanuvchi_id INT NOT NULL,
    token TEXT NOT NULL,
    faol BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE UNIQUE INDEX uq_faol_sessiya 
ON foydalanuvchi_sessiyalari (foydalanuvchi_id) 
WHERE (faol = TRUE);""",
        "Qisman (partial) UNIQUE indeks faqat 'WHERE' shartini qanoatlantiruvchi qatorlar uchun yagonalikni talab qiladi. 'faol = FALSE' bo'lgan yuzlab eski yozuvlar bo'lsa ham xato bermaydi, lekin ayni bir foydalanuvchi uchun ikkinchi 'faol = TRUE' yozuv kirishini to'xtatadi.",
        """CREATE TABLE
CREATE INDEX
Query returned successfully in 42 msec."""
    ),
    (
        71,
        "Oddiy CHECK cheklovi: Musbat qiymatni talab qilish",
        "Ombor mahsulotlari narxi yoki qoldiq soni hech qachon manfiy bo'lishi mumkin emas. Narx 0 dan qat'iy katta, miqdor esa 0 yoki undan katta bo'lishini CHECK orqali ta'minlang.",
        """CREATE TABLE do‘kon_mahsulotlari (
    mahsulot_id SERIAL PRIMARY KEY,
    nomi VARCHAR(100) NOT NULL,
    narx NUMERIC(10, 2) NOT NULL CHECK (narx > 0),
    qoldiq_miqdori INT NOT NULL CHECK (qoldiq_miqdori >= 0)
);""",
        "'CHECK (shart)' berilgan ustun qiymati mantiqiy TRUE bo'lishini talab qiladi. Agar INSERT yoki UPDATE paytida manfiy son kiritilsa, 'check constraint violation' xatoligi yuzaga keladi va tranzaksiya bekor qilinadi.",
        """CREATE TABLE
Query returned successfully in 32 msec."""
    ),
    (
        72,
        "Oraliqni tekshiruvchi CHECK cheklovi (BETWEEN)",
        "Talabalarning yakuniy reyting balli 0 dan 100 gacha bo'lishini CHECK va BETWEEN yordamida cheklang.",
        """CREATE TABLE reyting_jurnali (
    id SERIAL PRIMARY KEY,
    talaba_id INT NOT NULL,
    umumiy_ball NUMERIC(5, 2) NOT NULL 
        CHECK (umumiy_ball BETWEEN 0 AND 100)
);""",
        "'CHECK (umumiy_ball BETWEEN 0 AND 100)' ballning 0 dan kichik yoki 100 dan katta bo'lib ketishini bazaning o'zida to'xtatadi. Bu backend ilovalarida tekshirish unutilgan taqdirda ham ma'lumotlar ifloslanishidan asraydi.",
        """CREATE TABLE
Query returned successfully in 28 msec."""
    ),
    (
        73,
        "Sanalar mantiqiy ketma-ketligini tekshirish",
        "Mehmonxona yoki avtomobil ijarasida bron qilishning boshlanish vaqti tugash vaqtidan oldin bo'lishi shart. Ko'p ustunli CHECK cheklovini yozing.",
        """CREATE TABLE transport_ijarasi (
    ijara_id SERIAL PRIMARY KEY,
    mijoz_fio VARCHAR(100) NOT NULL,
    boshlanish_sanasi DATE NOT NULL,
    qaytarish_sanasi DATE NOT NULL,
    CONSTRAINT chk_ijara_muddati CHECK (qaytarish_sanasi >= boshlanish_sanasi)
);""",
        "CHECK cheklovi bir xil qatordagi bir nechta ustunlarni taqqoslay oladi. Bu yerda 'qaytarish_sanasi' 'boshlanish_sanasi'dan avval bo'lgan noo'rin ma'lumotlar kiritilishining oldi olinadi.",
        """CREATE TABLE
Query returned successfully in 30 msec."""
    ),
    (
        74,
        "Matn formatini tekshiruvchi CHECK: RegEx (Muntazam ifoda)",
        "Elektron pochta manzili haqiqiy e-mail formatiga (kamida @ va nuqta belgisiga) ega bo'lishini RegEx (~) orqali tekshiruvchi jadval tuzing.",
        """CREATE TABLE aloqa_kontaktlari (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    CONSTRAINT chk_email_formati CHECK (
        email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'
    )
);""",
        "PostgreSQL da '~*' operatori registrga sezgir bo'lmagan (case-insensitive) RegEx tekshiruvini amalga oshiradi. Noto'g'ri shakldagi elektron pochta (masalan, 'test@' yoki 'not-an-email') kiritilsa, baza uni rad etadi.",
        """CREATE TABLE
Query returned successfully in 37 msec."""
    ),
    (
        75,
        "O'zbekiston telefon raqamlari formatini CHECK bilan cheklash",
        "Telefon raqami faqat O'zbekiston formatida (+998 bilan boshlanuvchi va jami 12 ta raqam) bo'lishini ta'minlang.",
        """CREATE TABLE mijoz_telefonlari (
    id SERIAL PRIMARY KEY,
    telefon VARCHAR(13) NOT NULL,
    CONSTRAINT chk_uz_telefon CHECK (
        telefon ~ '^\\+998[0-9]{9}$'
    )
);""",
        "'^\\+998[0-9]{9}$' qat'iy format talab qiladi: boshida '+998', undan so'ng aynan 9 ta raqam. Bu operator kodi va abonent raqami to'g'ri kiritilishini kafolatlaydi.",
        """CREATE TABLE
Query returned successfully in 33 msec."""
    ),
    (
        76,
        "Qat'iy ro'yxat bo'yicha CHECK (IN operatori bilan)",
        "ENUM turini yaratmasdan turib, 'tolov_usuli' ustuni faqat 'naqd', 'karta', 'otkazma' qiymatlaridan birini qabul qilishini CHECK orqali belgilang.",
        """CREATE TABLE kassadagi_tolovlar (
    tolov_id SERIAL PRIMARY KEY,
    summa NUMERIC(15, 2) NOT NULL,
    tolov_usuli VARCHAR(20) NOT NULL 
        CHECK (tolov_usuli IN ('naqd', 'karta', 'otkazma'))
);""",
        "'CHECK (ustun IN ('a', 'b', 'c'))' cheklovi kiritilayotgan qiymatni ruxsat berilgan to'plamga tekshiradi. ENUM dan farqi shundaki, ro'yxatga yangi element qo'shish yoki o'chirish ALTER TABLE DROP/ADD CONSTRAINT orqali oson kechadi.",
        """CREATE TABLE
Query returned successfully in 29 msec."""
    ),
    (
        77,
        "Matn uzunligini CHECK bilan chegaralash (LENGTH)",
        "Foydalanuvchining paroli xeshlangan matn emas, balki kiritilayotgan PIN kodi qat'iy 4 tadan 6 tagacha raqamdan iborat bo'lishini tekshiring.",
        """CREATE TABLE pin_kodlar (
    foydalanuvchi_id INT PRIMARY KEY,
    pin_kod VARCHAR(6) NOT NULL,
    CONSTRAINT chk_pin_uzunligi CHECK (
        LENGTH(pin_kod) BETWEEN 4 AND 6 AND pin_kod ~ '^[0-9]+$'
    )
);""",
        "CHECK cheklovida SQL ning istalgan skalyar funksiyalaridan (LENGTH, LOWER, TRIM) foydalanish mumkin. Bu yerda bir vaqtning o'zida satr uzunligi hamda unda faqat raqamlar bo'lishi qat'iy tekshiriladi.",
        """CREATE TABLE
Query returned successfully in 32 msec."""
    ),
    (
        78,
        "Bo'sh satr kiritilishini taqiqlovchi CHECK",
        "Foydalanuvchi ismiga shunchaki bo'shliqlar ('   ') yoki bo'sh qator ('') kiritishini taqiqlovchi cheklov yozing.",
        """CREATE TABLE mualliflar_royxati (
    id SERIAL PRIMARY KEY,
    ism VARCHAR(100) NOT NULL,
    CONSTRAINT chk_ism_bosh_emas CHECK (LENGTH(TRIM(ism)) > 0)
);""",
        "'NOT NULL' cheklovi NULL ni to'xtatadi, biroq bo'sh satrni ('') o'tkazib yuboradi. 'CHECK (LENGTH(TRIM(ism)) > 0)' esa bo'shliqlar olib tashlanganidan keyin haqiqiy belgilar borligini tekshiradi.",
        """CREATE TABLE
Query returned successfully in 27 msec."""
    ),
    (
        79,
        "Mavjud katta jadvalga tezkor CHECK qo'shish: NOT VALID va VALIDATE",
        "Millionlab yozuvlari bor 'tranzaksiyalar' jadvalini uzoq vaqt qulflab qo'ymaslik uchun avval CHECK ni 'NOT VALID' bilan qo'shing, so'ngra alohida tasdiqlang.",
        """CREATE TABLE yirik_tranzaksiyalar (
    id BIGSERIAL PRIMARY KEY,
    summa NUMERIC(12, 2)
);

-- 1-qadam: Jadvalni bloklamasdan tezkor qo'shish:
ALTER TABLE yirik_tranzaksiyalar 
ADD CONSTRAINT chk_summa_musbat CHECK (summa >= 0) NOT VALID;

-- 2-qadam: Fon rejimida tekshirib tasdiqlash:
ALTER TABLE yirik_tranzaksiyalar 
VALIDATE CONSTRAINT chk_summa_musbat;""",
        "'NOT VALID' opsiyasi bilan yangi qatorlar darhol tekshirila boshlaydi, lekin mavjud eski qatorlar tekshirilmagani sababli jadval ACCESS EXCLUSIVE qulfini faqat millisekund ushlab turadi. 'VALIDATE CONSTRAINT' esa o'qish/yozishni to'xtatmasdan orqa fonda eski ma'lumotlarni tekshirib chiqadi.",
        """CREATE TABLE
ALTER TABLE
ALTER TABLE
Query returned successfully in 48 msec."""
    ),
    (
        80,
        "CHECK cheklovini bekor qilish (DROP CONSTRAINT)",
        "'yirik_tranzaksiyalar' jadvalidan 'chk_summa_musbat' cheklovini o'chirib tashlang.",
        """ALTER TABLE yirik_tranzaksiyalar 
DROP CONSTRAINT chk_summa_musbat;""",
        "Nomlangan cheklovlarni 'ALTER TABLE ... DROP CONSTRAINT cheklov_nomi' orqali istalgan vaqtda olib tashlash mumkin. Operatsiya bir zumda metadata darajasida amalga oshiriladi.",
        """ALTER TABLE
Query returned successfully in 19 msec."""
    ),
    (
        81,
        "Kechiktiriladigan cheklovlar: DEFERRABLE INITIALLY DEFERRED",
        "O'zaro bir-biriga bog'langan ikki jadvalga ma'lumot kiritishda siklik xatolik chiqmasligi uchun FOREIGN KEY ni tranzaksiya oxirigacha kechiktiring.",
        """CREATE TABLE a_jadval (
    id INT PRIMARY KEY,
    b_id INT
);

CREATE TABLE b_jadval (
    id INT PRIMARY KEY,
    a_id INT REFERENCES a_jadval(id) DEFERRABLE INITIALLY DEFERRED
);

ALTER TABLE a_jadval 
ADD CONSTRAINT fk_a_to_b FOREIGN KEY (b_id) 
REFERENCES b_jadval(id) DEFERRABLE INITIALLY DEFERRED;""",
        "'DEFERRABLE INITIALLY DEFERRED' - cheklov qator kiritilayotgan paytda emas, balki butun tranzaksiya yakunida (COMMIT vaqtida) tekshiriladi. Bu siklik bog'lanishlarni (circular dependency) bir tranzaksiyada xatoliksiz kiritishga imkon beradi.",
        """CREATE TABLE
CREATE TABLE
ALTER TABLE
Query returned successfully in 52 msec."""
    ),
    (
        82,
        "Sessiya davomida cheklovni kechiktirish: SET CONSTRAINTS",
        "Tranzaksiya ichida barcha kechiktiriluvchi cheklovlarni vaqtincha kechiktirish rejimiga o'tkazish kodini yozing.",
        """BEGIN;

SET CONSTRAINTS ALL DEFERRED;

-- Endi INSERT amallari cheklovlarga xilof bo'lsa ham COMMIT gacha ruxsat etiladi:
-- INSERT INTO ...

COMMIT;""",
        "'SET CONSTRAINTS ALL DEFERRED' tranzaksiya davomida barcha deferrable cheklovlar nazoratini tranzaksiya oxirigacha to'xtatib turadi. Agar COMMIT da mantiq buzilgan bo'lsa, tranzaksiya to'liq ROLLBACK bo'ladi.",
        """BEGIN
SET CONSTRAINTS
COMMIT
Query returned successfully in 24 msec."""
    ),
    (
        83,
        "Mustisno cheklovlari: EXCLUDE USING gist (Vaqt kesishuvlarini taqiqlash)",
        "Konferens-zalni bir vaqtning o'zida ikkita mijoz band qilib qo'yishini (bron vaqtlari kesishishini) bazaviy darajada EXCLUDE cheklovi bilan taqiqlang.",
        """CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TABLE zal_bandligi (
    bandlik_id SERIAL PRIMARY KEY,
    zal_raqami INT NOT NULL,
    band_vaqti TSRANGE NOT NULL,
    EXCLUDE USING gist (zal_raqami WITH =, band_vaqti WITH &&)
);""",
        "'EXCLUDE USING gist' ustunlar kombinatsiyasida maxsus operatorlar (tenglik '=', kesishish '&&') bo'yicha taqiq o'rnatadi. Agar ayni bir 'zal_raqami' uchun yangi kiritilayotgan 'band_vaqti' mavjud vaqt bilan kesishsa (&&), baza 'conflicting key' xatoligini beradi. Bandlik tizimlaridagi eng qudratli relyatsion cheklovdir.",
        """CREATE EXTENSION
CREATE TABLE
Query returned successfully in 68 msec."""
    ),
    (
        84,
        "DEFAULT: Matematik va tasodifiy qiymatlar",
        "Yangi ro'yxatdan o'tgan foydalanuvchiga tasodifiy 6 xonali tasdiqlash kodi beruvchi DEFAULT ifodasini yozing.",
        """CREATE TABLE telefon_tasdiqlash (
    id SERIAL PRIMARY KEY,
    telefon VARCHAR(20) NOT NULL,
    sms_kod INT DEFAULT FLOOR(100000 + RANDOM() * 900000),
    jonatilgan_vaqt TIMESTAMPTZ DEFAULT NOW()
);""",
        "DEFAULT faqat statik konstantalar bilan emas, deterministik bo'lmagan SQL ifodalari (RANDOM, CURRENT_TIMESTAMP, gen_random_uuid) bilan ham ishlashi mumkin. Qiymat ko'rsatilmaganda ifoda avtomatik hisoblanadi.",
        """CREATE TABLE
Query returned successfully in 31 msec."""
    ),
    (
        85,
        "DEFAULT: Foydalanuvchi yoki sessiya parametrini o'rnatish",
        "Har bir qatorga uni qaysi ma'lumotlar bazasi foydalanuvchisi yaratganini avtomatik yozib boruvchi 'DEFAULT CURRENT_USER' ustunini qo'shing.",
        """CREATE TABLE xavfsiz_hujjatlar (
    hujjat_id SERIAL PRIMARY KEY,
    fayl_nomi VARCHAR(200) NOT NULL,
    yaratuvchi_user VARCHAR(100) DEFAULT CURRENT_USER,
    yaratilgan_sana TIMESTAMPTZ DEFAULT CLOCK_TIMESTAMP()
);""",
        "'CURRENT_USER' joriy sessiyada ulangan Postgres foydalanuvchisi nomini qaytaradi. 'CLOCK_TIMESTAMP()' esa NOW() dan farqli o'laroq, tranzaksiya boshini emas, ayni shu qator diskka yozilgan aniq mikrosaniyani qayd etadi.",
        """CREATE TABLE
Query returned successfully in 34 msec."""
    ),
    (
        86,
        "Barcha cheklovlarni tizim katalogidan ko'rish",
        "Berilgan jadvalda (masalan 'do‘kon_mahsulotlari') qanday cheklovlar (PK, FK, UNIQUE, CHECK) mavjudligini information_schema orqali topuvchi so'rov yozing.",
        """SELECT 
    constraint_name, 
    constraint_type, 
    is_deferrable, 
    initially_deferred
FROM information_schema.table_constraints
WHERE table_name = 'do‘kon_mahsulotlari';""",
        "'information_schema.table_constraints' ANSI SQL standartidagi ko'rinish bo'lib, jadvallarga biriktirilgan barcha cheklovlar haqidagi to'liq metama'lumotlarni ko'rsatadi.",
        """    constraint_name     | constraint_type | is_deferrable | initially_deferred 
------------------------+-----------------+---------------+--------------------
 do‘kon_mahsulotlari_pkey| PRIMARY KEY     | NO            | NO
 2200_xxxx_narx_check   | CHECK           | NO            | NO
 2200_xxxx_qoldiq_check | CHECK           | NO            | NO
(3 rows)"""
    ),
    (
        87,
        "CHECK cheklovi formulasini pg_constraint dan o'qish",
        "PostgreSQL ning ichki tizim katalogi (pg_constraint) orqali barcha CHECK cheklovlarining qat'iy formulasini bilish so'rovini yozing.",
        """SELECT 
    conname AS cheklov_nomi,
    pg_get_constraintdef(c.oid) AS cheklov_ifodasi
FROM pg_constraint c
JOIN pg_namespace n ON n.oid = c.connamespace
WHERE conrelid = 'transport_ijarasi'::regclass;""",
        "'pg_get_constraintdef(oid)' funksiyasi cheklovning ichki binar ifodasini inson o'qiy oladigan SQL sintaksisiga aylantirib beradi.",
        """    cheklov_nomi     |                 cheklov_ifodasi                  
---------------------+--------------------------------------------------
 transport_ijarasi_pkey | PRIMARY KEY (ijara_id)
 chk_ijara_muddati   | CHECK ((qaytarish_sanasi >= boshlanish_sanasi))
(2 rows)"""
    ),
    (
        88,
        "Shartli CHECK: Agar status 'bekor_qilindi' bo'lsa izoh majburiy",
        "E-tijorat tizimida buyurtma bekor qilinganda bekor qilish sababi (izoh) yozilishi shart, boshqa holatlarda esa ixtiyoriy bo'lishini ta'minlovchi CHECK yozing.",
        """CREATE TABLE mijoz_buyurtma_tarixi (
    id SERIAL PRIMARY KEY,
    status VARCHAR(20) NOT NULL,
    bekor_qilish_sababi TEXT,
    CONSTRAINT chk_sabab_talabi CHECK (
        (status = 'bekor_qilindi' AND bekor_qilish_sababi IS NOT NULL) OR
        (status <> 'bekor_qilindi')
    )
);""",
        "Mantiqiy shartlar yordamida (IMPLICATION: `status = 'bekor_qilindi' => sabab IS NOT NULL`) biznes qoidalarini bazaning o'zida qat'iy tekshirish mumkin. Bu ilova dasturchilarining xatolarini to'liq istisno qiladi.",
        """CREATE TABLE
Query returned successfully in 32 msec."""
    ),
    (
        89,
        "Bir nechta ustundan iborat kompozit FOREIGN KEY",
        "Boshqa jadvalning kompozit birlamchi kalitiga havola qiluvchi kompozit tashqi kalitli jadval tuzing.",
        """CREATE TABLE kompozit_ota (
    tashkilot_id INT NOT NULL,
    filial_id INT NOT NULL,
    nomi VARCHAR(100),
    PRIMARY KEY (tashkilot_id, filial_id)
);

CREATE TABLE kompozit_bola (
    yozuv_id SERIAL PRIMARY KEY,
    t_id INT NOT NULL,
    f_id INT NOT NULL,
    FOREIGN KEY (t_id, f_id) REFERENCES kompozit_ota(tashkilot_id, filial_id)
        ON DELETE CASCADE
);""",
        "Kompozit tashqi kalit bola jadvaldagi bir nechta ustunlarni ota jadvaldagi aynan mos kompozit birlamchi (yoki unique) kalit ustunlari bilan bog'laydi.",
        """CREATE TABLE
CREATE TABLE
Query returned successfully in 44 msec."""
    ),
    (
        90,
        "Cheklovni vaqtincha o'chirib turish (DISABLE TRIGGER)",
        "PostgreSQL da FOREIGN KEY tekshiruvi tizim triggerlari orqali boshqariladi. Ommaviy import paytida tashqi kalitlarni vaqtincha to'xtatish usulini ko'rsating.",
        """-- Diqqat: superuser huquqi talab etiladi:
ALTER TABLE kompozit_bola DISABLE TRIGGER ALL;

-- Ma'lumotlarni ommaviy yuklash amalga oshiriladi...

ALTER TABLE kompozit_bola ENABLE TRIGGER ALL;""",
        "PostgreSQL da FOREIGN KEY cheklovlari orqa fonda 'RI_ConstraintTrigger' triggerlari orqali amalga oshadi. Barcha triggerlarni o'chirish orqali import tezligini oshirish mumkin, lekin keyin ma'lumotlar yaxlitligi qo'lda tekshirilishi lozim.",
        """ALTER TABLE
ALTER TABLE
Query returned successfully in 28 msec."""
    ),
    (
        91,
        "Avtomatik UUID generatori bilan DEFAULT cheklovi",
        "gen_random_uuid() yordamida yangi qator kiritilganda unikal UUID4 ni avtomatik hosil qiluvchi DEFAULT kalitini qo'llang.",
        """CREATE TABLE xavfsiz_foydalanuvchilar (
    user_guid UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    login VARCHAR(50) NOT NULL UNIQUE
);""",
        "UUID (v4) tasodifiy 122 bitli kriptografik entropiyaga tayanadi. Baza darajasidagi 'gen_random_uuid()' orqali mijoz dasturlari alohida ID generatsiya qilishi shart emas.",
        """CREATE TABLE
Query returned successfully in 29 msec."""
    ),
    (
        92,
        "Narx va chegirma mantiqiy nisbati bo'yicha CHECK",
        "Mahsulotning chegirmali narxi hech qachon uning asl narxidan qimmat bo'lmasligini ta'minlovchi cheklov yozing.",
        """CREATE TABLE aksiya_mahsulotlari (
    id SERIAL PRIMARY KEY,
    asl_narx NUMERIC(12, 2) NOT NULL CHECK (asl_narx > 0),
    chegirma_narxi NUMERIC(12, 2) CHECK (chegirma_narxi > 0),
    CONSTRAINT chk_chegirma_asldan_kichik CHECK (
        chegirma_narxi IS NULL OR chegirma_narxi < asl_narx
    )
);""",
        "Ushbu qoidada 'chegirma_narxi' mavjud bo'lgandagina uning 'asl_narx'dan kamligi tekshiriladi. NULL qiymatlar mantiqiy ifodani buzmaydi.",
        """CREATE TABLE
Query returned successfully in 31 msec."""
    ),
    (
        93,
        "Yaxlitlik qoidalarining buzilishini tutib olish (INSERT xatosi)",
        "CHECK cheklovi o'rnatilgan jadvalga ataylab noto'g'ri qiymat kiritib, RDBMS qaytargan xatolikni ko'ring.",
        """-- chk_uz_telefon faqat +998 talab qiladi:
INSERT INTO mijoz_telefonlari (telefon) 
VALUES ('+12345678901');""",
        "RDBMS tranzaksiyani bekor qiladi va ma'lumotlar bazasiga noto'g'ri qiymat yozilishiga yo'l qo'ymaydi. Bu xavfsizlikning fundamental kafolatidir.",
        """ERROR:  new row for relation "mijoz_telefonlari" violates check constraint "chk_uz_telefon"
DETAIL:  Failing row contains (1, +12345678901)."""
    ),
    (
        94,
        "FOREIGN KEY buzilishi xatosi (Referential integrity error)",
        "Mavjud bo'lmagan xodim ID raqami bilan loyihaga yetakchi biriktirishga urinib, tashqi kalit xatosini sinang.",
        """INSERT INTO loyihalar (loyiha_nomi, yetakchi_id) 
VALUES ('Suniy Intellekt Modeli', 99999);""",
        "Codd relyatsion modeliga asosan, tashqi kalitdagi har bir qiymat ota jadvalda mavjud bo'lishi shart. Agar 99999 id dagi xodim bo'lmasa, RDBMS xatolik qaytaradi.",
        """ERROR:  insert or update on table "loyihalar" violates foreign key constraint "loyihalar_yetakchi_id_fkey"
DETAIL:  Key (yetakchi_id)=(99999) is not present in table "xodimlar"."""
    ),
    (
        95,
        "UNIQUE buzilishi xatosi (Duplicate key violation)",
        "Bir xil JSHSHIR (PINFL) raqamiga ega ikkita shaxsni kiritishga urinishdagi tizim xatti-harakatini tahlil qiling.",
        """INSERT INTO shaxslar (jshshir, fio) VALUES ('12345678901234', 'Aliyev Ali');
-- Ikkinchi marta ayni shu JSHSHIR kiritiladi:
INSERT INTO shaxslar (jshshir, fio) VALUES ('12345678901234', 'Valiyev Vali');""",
        "B-Tree unique indeksi ikkinchi yozuvni qo'shish paytida kalitlar to'qnashuvini aniqlaydi va 'duplicate key' xatoligini chiqaradi.",
        """INSERT 0 1
ERROR:  duplicate key value violates unique constraint "shaxslar_jshshir_key"
DETAIL:  Key (jshshir)=(12345678901234) already exists."""
    ),
    (
        96,
        "ON UPDATE RESTRICT bilan asosiy kalit o'zgarishini bloklash",
        "Bo'lim ID si o'zgartirilmoqchi bo'lganda, unga biriktirilgan xodimlar bor bo'lsa o'zgartirishni to'xtatuvchi cheklov qo'llang.",
        """CREATE TABLE idora_bolimlari (
    id INT PRIMARY KEY,
    nomi VARCHAR(100)
);

CREATE TABLE idora_xodimlari (
    id SERIAL PRIMARY KEY,
    bolim_id INT REFERENCES idora_bolimlari(id) ON UPDATE RESTRICT
);""",
        "'ON UPDATE RESTRICT' ota jadvalning birlamchi kaliti UPDATE qilinayotganda ushbu kalitga tayanuvchi xodimlar mavjud bo'lsa, operatsiyani qat'iyan man etadi.",
        """CREATE TABLE
CREATE TABLE
Query returned successfully in 41 msec."""
    ),
    (
        97,
        "Cheklov nomini o'zgartirish: RENAME CONSTRAINT",
        "'shaxslar' jadvalidagi 'shaxslar_jshshir_key' nomli cheklovni 'uq_shaxs_pinfl' ga o'zgartiring.",
        """ALTER TABLE shaxslar 
RENAME CONSTRAINT shaxslar_jshshir_key TO uq_shaxs_pinfl;""",
        "'RENAME CONSTRAINT' ma'lumotlar bazasidagi cheklov nomini o'zgartiradi. Ushbu o'zgarish tegishli indeks nomiga ham ta'sir qiladi.",
        """ALTER TABLE
Query returned successfully in 21 msec."""
    ),
    (
        98,
        "Ko'p shartli murakkab CHECK (Ish haqi darajalari)",
        "Lavozimga qarab ish haqi chegaralarini (Junior: 5M-10M, Middle: 10M-20M, Senior: 20M+) tekshiruvchi cheklov yozing.",
        """CREATE TABLE lavozim_maoshlari (
    xodim_id SERIAL PRIMARY KEY,
    daraja VARCHAR(20) NOT NULL,
    maosh NUMERIC(15, 2) NOT NULL,
    CONSTRAINT chk_daraja_maosh CHECK (
        (daraja = 'Junior' AND maosh BETWEEN 5000000 AND 10000000) OR
        (daraja = 'Middle' AND maosh BETWEEN 10000001 AND 20000000) OR
        (daraja = 'Senior' AND maosh >= 20000001)
    )
);""",
        "Ushbu CHECK cheklovi lavozim va unga to'lanadigan maosh mutanosibligini qat'iy kafolatlaydi va insoniy xatolik tufayli Juniorga noto'g'ri katta maosh yozilishini to'xtatadi.",
        """CREATE TABLE
Query returned successfully in 35 msec."""
    ),
    (
        99,
        "Kaskadli o'chirish chuqurligi (Ko'p bosqichli CASCADE)",
        "3 bosqichli bog'lanish: Universitet -> Fakultet -> Guruh. Universitet o'chirilganda butun zanjir avtomatik tozalansin.",
        """CREATE TABLE universlar (id INT PRIMARY KEY, nomi TEXT);
CREATE TABLE fakultetlar (id INT PRIMARY KEY, u_id INT REFERENCES universlar(id) ON DELETE CASCADE);
CREATE TABLE guruhlar (id INT PRIMARY KEY, f_id INT REFERENCES fakultetlar(id) ON DELETE CASCADE);

INSERT INTO universlar VALUES (1, 'Milliy Universitet');
INSERT INTO fakultetlar VALUES (10, 1);
INSERT INTO guruhlar VALUES (100, 10);

DELETE FROM universlar WHERE id = 1;

SELECT COUNT(*) AS qolgan_guruhlar FROM guruhlar;""",
        "PostgreSQL 'ON DELETE CASCADE' ni rekursiv tarzda barcha chuqurlikdagi bog'liq jadvallar bo'ylab ijro etadi. Universitet o'chirilishi bilan uning barcha fakultetlari va barcha guruhlari avtomatik o'chadi.",
        """ qolgan_guruhlar 
------------------
                0
(1 row)"""
    ),
    (
        100,
        "Korporativ Baza: Yaxlitlik cheklovlarining to'liq me'morchiligi",
        "Bank kredit tizimi uchun mijozlar, kredit shartnomalari va to'lov grafigi jadvallarini PK, FK, UNIQUE, CHECK, NOT NULL va DEFAULT cheklovlari bilan to'liq yaratuvchi mustahkam skript yozing.",
        """CREATE TABLE bank_mijozlari (
    mijoz_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pinfl CHAR(14) NOT NULL,
    fio VARCHAR(150) NOT NULL,
    tugilgan_sana DATE NOT NULL,
    telefon VARCHAR(13) NOT NULL,
    CONSTRAINT uq_mijoz_pinfl UNIQUE (pinfl),
    CONSTRAINT chk_voyaga_yetgan CHECK (AGE(CURRENT_DATE, tugilgan_sana) >= '18 years'::INTERVAL),
    CONSTRAINT chk_uzb_tel CHECK (telefon ~ '^\\+998[0-9]{9}$')
);

CREATE TABLE kredit_shartnomalari (
    shartnoma_id BIGSERIAL PRIMARY KEY,
    shartnoma_raqami VARCHAR(50) NOT NULL UNIQUE,
    mijoz_id UUID NOT NULL REFERENCES bank_mijozlari(mijoz_id) ON DELETE RESTRICT,
    ajratilgan_summa NUMERIC(15, 2) NOT NULL CHECK (ajratilgan_summa > 0),
    yillik_foiz NUMERIC(5, 2) NOT NULL CHECK (yillik_foiz BETWEEN 1 AND 100),
    boshlanish_sanasi DATE NOT NULL DEFAULT CURRENT_DATE,
    tugash_sanasi DATE NOT NULL,
    holat VARCHAR(20) NOT NULL DEFAULT 'faol' CHECK (holat IN ('faol', 'yopilgan', 'sudda')),
    CONSTRAINT chk_shartnoma_muddati CHECK (tugash_sanasi > boshlanish_sanasi)
);

CREATE TABLE tolov_grafigi (
    grafik_id BIGSERIAL PRIMARY KEY,
    shartnoma_id BIGINT NOT NULL REFERENCES kredit_shartnomalari(shartnoma_id) ON DELETE CASCADE,
    oy_raqami SMALLINT NOT NULL CHECK (oy_raqami >= 1),
    tolash_sanasi DATE NOT NULL,
    asosiy_qarz NUMERIC(15, 2) NOT NULL CHECK (asosiy_qarz >= 0),
    foiz_qarzi NUMERIC(15, 2) NOT NULL CHECK (foiz_qarzi >= 0),
    tolangan BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT uq_shartnoma_oy UNIQUE (shartnoma_id, oy_raqami)
);""",
        "Ushbu relyatsion arxitektura korporativ standartlarga to'liq javob beradi: yoshni tekshirish (18 yoshdan kattalarga kredit), xalqaro telefon formatlari, foiz va summalar diapazoni, qarz jadvali unikal oylari va kaskadli yaxlitlik qat'iy himoyalangan.",
        """CREATE TABLE
CREATE TABLE
CREATE TABLE
Query returned successfully in 84 msec."""
    )
]

formatted = [format_task(*item) for item in constraints_data]
save_file("sql_02_cheklovlar_constraints_va_yaxlitlik.md", formatted)
