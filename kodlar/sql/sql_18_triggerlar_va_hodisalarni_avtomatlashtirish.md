# 851-Topshiriq: BEFORE UPDATE triggeri: yangilangan_vaqt ustunini avtomatik sozlash
## Topshiriq sharti:
Foydalanuvchilar jadvalidagi istalgan ustun yangilanganda `yangilangan_vaqt` (updated_at) ustuniga avtomatik joriy vaqtni (CURRENT_TIMESTAMP) yozib qo'yuvchi BEFORE UPDATE triggerini va uning funksiyasini yarating.

## Yechim (SQL kodi):
```sql
-- 1. Trigger funksiyasini yaratish
CREATE OR REPLACE FUNCTION trg_avto_yangilangan_vaqt()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.yangilangan_vaqt := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

-- 2. Trigger bog'lash
DROP TRIGGER IF EXISTS trg_foydalanuvchilar_vaqt ON foydalanuvchilar;
CREATE TRIGGER trg_foydalanuvchilar_vaqt
BEFORE UPDATE ON foydalanuvchilar
FOR EACH ROW
EXECUTE FUNCTION trg_avto_yangilangan_vaqt();

-- 3. Test: Qatorni yangilash
UPDATE foydalanuvchilar 
SET ism = 'Jasur Yangilangan' 
WHERE id = 1;

-- Tekshirish
SELECT id, ism, yaratilgan_vaqt, yangilangan_vaqt 
FROM foydalanuvchilar 
WHERE id = 1;
```

## Tushuntirish va Mantiq:
`BEFORE UPDATE` triggeri jadvaldagi qator diskka yozilishidan oldin ishga tushadi. `NEW` maxsus rekordi o'zgartirilayotgan yangi qatorni ifodalaydi. `NEW.yangilangan_vaqt := CURRENT_TIMESTAMP;` orqali ilova dasturchisi esdan chiqargan taqdirda ham o'zgarish vaqti bazaviy darajada kafolatli yangilanadi. `RETURN NEW;` yangilangan qatorni qabul qilishni bildiradi.

## Ishlash natijasi:
```text
id |       ism        |   yaratilgan_vaqt   |      yangilangan_vaqt      
----+------------------+---------------------+----------------------------
  1 | Jasur Yangilangan| 2024-01-01 10:00:00 | 2024-06-15 14:22:18.512401
(1 row)
```


# 852-Topshiriq: BEFORE INSERT triggeri: Matnlarni tozalash va standartlashtirish (Sanitization)
## Topshiriq sharti:
Mijoz ro'yxatdan o'tayotganda uning email manzilidagi keraksiz bo'shliqlarni olib tashlab, kichik harflarga (LOWER) o'tkazuvchi va telefon raqamidan faqat raqamlarni qoldiruvchi BEFORE INSERT triggerini yarating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_tozalash_mijoz_malumotlari()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Emailni tozalash va kichik harfga keltirish
    NEW.email := LOWER(TRIM(NEW.email));

    -- Telefon raqamidagi ortiqcha belgilarni tozalash
    NEW.telefon := regexp_replace(NEW.telefon, '[^0-9+]', '', 'g');

    -- Ismni bosh harf bilan formatlash
    NEW.ism := INITCAP(TRIM(NEW.ism));

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_mijozlar_tozalash
BEFORE INSERT ON mijozlar
FOR EACH ROW
EXECUTE FUNCTION trg_tozalash_mijoz_malumotlari();

-- Test
INSERT INTO mijozlar(ism, email, telefon)
VALUES ('   aliSHER   ', '  Ali.Dev@MISOL.UZ  ', '+998 (90) 123-45-67');

SELECT ism, email, telefon FROM mijozlar WHERE email = 'ali.dev@misol.uz';
```

## Tushuntirish va Mantiq:
BEFORE INSERT triggeri ma'lumotlar bazasiga kirib kelayotgan xom ma'lumotlarni filtrlash va normallashtirish (sanitization) uchun eng ishonchli nuqtadir. `NEW.email` va boshqa maydonlar to'g'ridan-to'g'ri o'zgartiriladi va tozalangan qiymatlar jadvalga muhrlanadi.

## Ishlash natijasi:
```text
ism   |       email        |    telefon    
---------+--------------------+---------------
 Alisher | ali.dev@misol.uz   | +998901234567
(1 row)
```


# 853-Topshiriq: AFTER INSERT triggeri: Foydalanuvchi yaratilganda avtomatik profil va hamyon ochish
## Topshiriq sharti:
Yangi foydalanuvchi (`foydalanuvchilar`) qo'shilishi bilanoq, unga avtomatik 0 so'm balansli hamyon (`hamyonlar`) va boshlang'ich sozlamalar profilini (`foydalanuvchi_sozlamalari`) ochib beruvchi AFTER INSERT triggerini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_avto_profil_yaratish()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Yangi foydalanuvchiga hamyon ochish
    INSERT INTO hamyonlar(foydalanuvchi_id, balans, valyuta)
    VALUES (NEW.id, 0.00, 'UZS');

    -- Standart sozlamalar profilini yaratish
    INSERT INTO foydalanuvchi_sozlamalari(foydalanuvchi_id, til, bildirishnomalar)
    VALUES (NEW.id, 'uz', TRUE);

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_yangi_foydalanuvchi_init
AFTER INSERT ON foydalanuvchilar
FOR EACH ROW
EXECUTE FUNCTION trg_avto_profil_yaratish();

-- Test
INSERT INTO foydalanuvchilar (id, ism, email) 
VALUES (105, 'Nodirbek', 'nodir@misol.uz');

-- Bog'liq jadvallarni tekshirish
SELECT h.foydalanuvchi_id, h.balans, s.til 
FROM hamyonlar h
JOIN foydalanuvchi_sozlamalari s ON h.foydalanuvchi_id = s.foydalanuvchi_id
WHERE h.foydalanuvchi_id = 105;
```

## Tushuntirish va Mantiq:
`AFTER INSERT` triggeri asosiy qator muvaffaqiyatli jadvalga kiritilgandan so'ng bajariladi. Bu paytda `NEW.id` (agar SERIAL yoki IDENTITY bo'lsa) to'liq generatsiya qilingan bo'ladi va tashqi kalit (FOREIGN KEY) cheklovlariga ega bog'liq jadvallarga xavfsiz murojaat qilish imkonini beradi.

## Ishlash natijasi:
```text
foydalanuvchi_id | balans | til 
------------------+--------+-----
              105 |   0.00 | uz
(1 row)
```


# 854-Topshiriq: AFTER UPDATE/DELETE audit log triggeri: O'zgarishlar tarixini JSONB formatida saqlash
## Topshiriq sharti:
Mahsulotlar jadvalidagi narx yoki nom o'zgarganda yoki qator o'chirilganda, o'zgarishdan oldingi (`OLD`) va keyingi (`NEW`) qiymatlarni, o'zgartirgan foydalanuvchini va amaliyot turini `audit_log` jadvaliga yozib boruvchi universal trigger tuzing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_audit_mahsulotlar()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF (TG_OP = 'UPDATE') THEN
        INSERT INTO audit_log (jadval_nomi, amal_turi, yozuv_id, eski_holat, yangi_holat, ozgartiruvchi, sana)
        VALUES (
            TG_TABLE_NAME,
            TG_OP,
            OLD.id,
            to_jsonb(OLD),
            to_jsonb(NEW),
            CURRENT_USER,
            CURRENT_TIMESTAMP
        );
        RETURN NEW;
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO audit_log (jadval_nomi, amal_turi, yozuv_id, eski_holat, yangi_holat, ozgartiruvchi, sana)
        VALUES (
            TG_TABLE_NAME,
            TG_OP,
            OLD.id,
            to_jsonb(OLD),
            NULL,
            CURRENT_USER,
            CURRENT_TIMESTAMP
        );
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$;

CREATE TRIGGER trg_mahsulotlar_audit
AFTER UPDATE OR DELETE ON mahsulotlar
FOR EACH ROW
EXECUTE FUNCTION trg_audit_mahsulotlar();

-- Test
UPDATE mahsulotlar SET narx = 5500000.00 WHERE id = 10;
SELECT amal_turi, yozuv_id, eski_holat->>'narx' AS eski_narx, yangi_holat->>'narx' AS yangi_narx FROM audit_log ORDER BY id DESC LIMIT 1;
```

## Tushuntirish va Mantiq:
`TG_OP` maxsus o'zgaruvchisi trigger qaysi amal sababli chaqirilganini ('INSERT', 'UPDATE', 'DELETE') aniqlaydi. `to_jsonb(OLD)` butun relyatsion qatorni JSONB ob'ektiga aylantiradi, bu esa ma'lumotlar bazasidagi har qanday jadval uchun universal audit mexanizmini yaratish imkonini beradi.

## Ishlash natijasi:
```text
amal_turi | yozuv_id | eski_narx  | yangi_narx 
-----------+----------+------------+------------
 UPDATE    |       10 | 5000000.00 | 5500000.00
(1 row)
```


# 855-Topshiriq: Shartli trigger: WHEN (shart) orqali chaqiruvlarni optimallashtirish
## Topshiriq sharti:
Trigger funksiyasi har safar chaqirilib resurs sarflamasligi uchun, faqatgina mahsulot narxi 20% dan ko'proqqa o'zgarganda ishga tushadigan shartli `WHEN` triggerini yarating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_narx_keskin_ozgardi_ogohlantirish()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE NOTICE 'Diqqat! Mahsulot ID % narxi keskin o''zgardi: Eski: %, Yangi: %',
        NEW.id, OLD.narx, NEW.narx;

    INSERT INTO narx_monitoring_xabarlari(mahsulot_id, eski_narx, yangi_narx, sana)
    VALUES (NEW.id, OLD.narx, NEW.narx, NOW());

    RETURN NEW;
END;
$$;

-- WHEN sharti bilan trigger
CREATE TRIGGER trg_narx_sakrash_monitoring
AFTER UPDATE OF narx ON mahsulotlar
FOR EACH ROW
WHEN (ABS(NEW.narx - OLD.narx) / OLD.narx >= 0.20)
EXECUTE FUNCTION trg_narx_keskin_ozgardi_ogohlantirish();

-- Test: Narxni 30% ga oshirish
UPDATE mahsulotlar SET narx = 130000 WHERE id = 5 AND narx = 100000;
```

## Tushuntirish va Mantiq:
`WHEN (shart)` bandi trigger funksiyasini chaqirishdan oldin server yadrosida shartni tekshiradi. Agar shart bajarilmasa, PL/pgSQL interpretatori umuman ishga tushmaydi, kontekst almashinuvi yuz bermaydi va server samaradorligi sezilarli darajada saqlanadi.

## Ishlash natijasi:
```text
NOTICE:  Diqqat! Mahsulot ID 5 narxi keskin o'zgardi: Eski: 100000.00, Yangi: 130000.00
UPDATE 1
```


# 856-Topshiriq: BEFORE DELETE triggeri orqali qator o'chirilishini taqiqlash
## Topshiriq sharti:
Hisobida ijobiy qoldiq (balans > 0) mavjud bo'lgan mijoz yozuvini jismonan o'chirishga yo'l qo'ymaydigan va tushunarli xatolik ko'taruvchi BEFORE DELETE triggerini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_bloklash_ochirish_balansli_mijoz()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF OLD.balans > 0 THEN
        RAISE EXCEPTION 'Mijozni o''chirish taqiqlanadi! Hisobda mavjud qoldiq: % so''m. Avval balansni 0 qiling.', OLD.balans
            USING ERRCODE = 'check_violation';
    END IF;

    RETURN OLD;
END;
$$;

CREATE TRIGGER trg_himoya_ochirish_mijoz
BEFORE DELETE ON mijozlar
FOR EACH ROW
EXECUTE FUNCTION trg_bloklash_ochirish_balansli_mijoz();

-- Test: Balansi 50 000 bo'lgan mijozni o'chirishga urinish
DELETE FROM mijozlar WHERE id = 2 AND balans = 50000;
```

## Tushuntirish va Mantiq:
`BEFORE DELETE` triggerida `OLD` rekordi o'chirilishi kutilayotgan mavjud qatorni ushlab turadi. `RAISE EXCEPTION` buyrug'i berilganda tranzaksiya butunlay to'xtatiladi, DELETE buyrug'i bekor qilinadi va xatolik chaqiruvchi dasturga qaytariladi.

## Ishlash natijasi:
```text
ERROR:  Mijozni o'chirish taqiqlanadi! Hisobda mavjud qoldiq: 50000.00 so'm. Avval balansni 0 qiling.
```


# 857-Topshiriq: Soft Delete (Mantiqiy o'chirish) ni amalga oshiruvchi BEFORE DELETE triggeri
## Topshiriq sharti:
Foydalanuvchi `DELETE FROM foydalanuvchilar WHERE id = ...` deb yozganda qatorni haqiqatdan o'chirib yubormasdan, uning `ochirilgan_vaqt` ustunini to'ldirib, o'chirish amalini bekor qiluvchi (RETURN NULL) trigger yarating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_mantiqiy_ochirish()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Jismoniy o'chirish o'rniga status va vaqtni belgilash
    UPDATE foydalanuvchilar
    SET ochirilgan_vaqt = NOW(),
        holat = 'OCHIRILGAN'
    WHERE id = OLD.id;

    -- Jismoniy DELETE amalining o'zini bekor qilish
    RETURN NULL;
END;
$$;

CREATE TRIGGER trg_foydalanuvchi_soft_delete
BEFORE DELETE ON foydalanuvchilar
FOR EACH ROW
EXECUTE FUNCTION trg_mantiqiy_ochirish();

-- Test: Qatorni o'chirish
DELETE FROM foydalanuvchilar WHERE id = 7;

-- Natijani tekshirish (qator mavjud, lekin status o'zgargan)
SELECT id, ism, holat, ochirilgan_vaqt FROM foydalanuvchilar WHERE id = 7;
```

## Tushuntirish va Mantiq:
`BEFORE` triggeri ichida `RETURN NULL;` qaytarish kutilayotgan DML operatsiyasini jimgina bekor qiladi (ignore). Natijada haqiqiy qator jadvalda qoladi, lekin trigger ichidagi UPDATE orqali unga mantiqiy o'chirilganlik belgisi qo'yiladi.

## Ishlash natijasi:
```text
id |   ism   |    holat    |      ochirilgan_vaqt       
----+---------+-------------+----------------------------
  7 | Sanjar  | OCHIRILGAN  | 2024-06-15 15:40:12.193812
(1 row)
```


# 858-Topshiriq: INSTEAD OF INSERT triggeri: Oddiy ko'rinishga (View) ma'lumot kiritish
## Topshiriq sharti:
Ikki jadval (`xodimlar` va `bolimlar`) birlashmasidan iborat ko'rinishga (`v_xodimlar_bolim`) INSERT so'rovi yuborilganda, mos qismlarni tegishli asosiy jadvallarga joylashtiruvchi INSTEAD OF triggerini yozing.

## Yechim (SQL kodi):
```sql
-- Ko'rinish
CREATE OR REPLACE VIEW v_xodimlar_bolim AS
SELECT x.id AS xodim_id, x.ism, x.familiya, x.maosh, b.id AS bolim_id, b.nomi AS bolim_nomi
FROM xodimlar x
JOIN bolimlar b ON x.bolim_id = b.id;

-- INSTEAD OF trigger funksiyasi
CREATE OR REPLACE FUNCTION trg_v_xodimlar_insert()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_b_id INT;
BEGIN
    -- Bo'lim mavjudligini tekshirish yoki yangi ochish
    SELECT id INTO v_b_id FROM bolimlar WHERE LOWER(nomi) = LOWER(NEW.bolim_nomi);
    IF v_b_id IS NULL THEN
        INSERT INTO bolimlar(nomi) VALUES (NEW.bolim_nomi) RETURNING id INTO v_b_id;
    END IF;

    -- Xodimni qo'shish
    INSERT INTO xodimlar(ism, familiya, maosh, bolim_id)
    VALUES (NEW.ism, NEW.familiya, NEW.maosh, v_b_id);

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_v_xodimlar_bolim_ins
INSTEAD OF INSERT ON v_xodimlar_bolim
FOR EACH ROW
EXECUTE FUNCTION trg_v_xodimlar_insert();

-- Test
INSERT INTO v_xodimlar_bolim(ism, familiya, maosh, bolim_nomi)
VALUES ('Sherzod', 'Tursunov', 14000000, 'Marketing');
```

## Tushuntirish va Mantiq:
`INSTEAD OF` triggerlari faqatgina `VIEW`lar ustida ishlaydi. Ko'p jadvalli murakkab ko'rinishlar standart holatda tahrirlanmaydi (non-updatable). `INSTEAD OF` triggeri orqali VIEW'ga kelgan INSERT/UPDATE/DELETE amallari asosiy fundamental jadvallarga xavfsiz taqsimlanadi.

## Ishlash natijasi:
```text
INSERT 0 1
```


# 859-Topshiriq: INSTEAD OF UPDATE triggeri: View orqali ma'lumotlarni yangilash
## Topshiriq sharti:
`v_xodimlar_bolim` ko'rinishi orqali xodimning maoshi yoki bo'limi nomi o'zgartirilganda tegishli asosiy jadvallarni to'g'ri yangilovchi INSTEAD OF UPDATE triggerini tuzing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_v_xodimlar_update()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Xodimning o'z ma'lumotlarini yangilash
    UPDATE xodimlar
    SET ism = NEW.ism,
        familiya = NEW.familiya,
        maosh = NEW.maosh
    WHERE id = OLD.xodim_id;

    -- Agar bo'lim nomi o'zgargan bo'lsa
    IF NEW.bolim_nomi <> OLD.bolim_nomi THEN
        UPDATE bolimlar
        SET nomi = NEW.bolim_nomi
        WHERE id = OLD.bolim_id;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_v_xodimlar_bolim_upd
INSTEAD OF UPDATE ON v_xodimlar_bolim
FOR EACH ROW
EXECUTE FUNCTION trg_v_xodimlar_update();

-- Test: View orqali xodim maoshini yangilash
UPDATE v_xodimlar_bolim 
SET maosh = 16500000.00 
WHERE xodim_id = 1;
```

## Tushuntirish va Mantiq:
`INSTEAD OF UPDATE` triggeri VIEW ustidan berilgan yangilash so'rovini qabul qilib, o'zgartirilgan maydonlarni aniqlaydi va mantiqiy asosiy jadvallarga mos UPDATE buyruqlarini jo'natadi.

## Ishlash natijasi:
```text
UPDATE 1
```


# 860-Topshiriq: INSTEAD OF DELETE triggeri: View orqali o'chirishni boshqarish
## Topshiriq sharti:
`v_xodimlar_bolim` ko'rinishidan yozuv o'chirilganda bo'limni o'chirib yubormasdan faqat xodimning o'zini o'chiruvchi INSTEAD OF DELETE triggerini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_v_xodimlar_delete()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM xodimlar WHERE id = OLD.xodim_id;
    RETURN OLD;
END;
$$;

CREATE TRIGGER trg_v_xodimlar_bolim_del
INSTEAD OF DELETE ON v_xodimlar_bolim
FOR EACH ROW
EXECUTE FUNCTION trg_v_xodimlar_delete();

-- Test
DELETE FROM v_xodimlar_bolim WHERE xodim_id = 99;
```

## Tushuntirish va Mantiq:
`INSTEAD OF DELETE` triggeri yordamida JOIN qilingan VIEW'lardan qator o'chirilganda faqat kerakli filial (jadval) ma'lumotlari xavfsiz o'chiriladi, ikkinchi tomonga (bo'limlar) daxl qilinmaydi.

## Ishlash natijasi:
```text
DELETE 1
```


# 861-Topshiriq: Denormalizatsiya qilingan agregat hisoblagichni keshlovchi AFTER trigger
## Topshiriq sharti:
Har safar `sharhlar` jadvaliga mahsulot uchun sharh yozilganda yoki o'chirilganda, `mahsulotlar` jadvalidagi `ortacha_baho` va `sharhlar_soni` ustunlarini avtomatik qayta hisoblab qo'yuvchi AFTER triggerini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_yangila_mahsulot_reyting()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_m_id INT;
BEGIN
    v_m_id := COALESCE(NEW.mahsulot_id, OLD.mahsulot_id);

    UPDATE mahsulotlar
    SET sharhlar_soni = (SELECT COUNT(*) FROM sharhlar WHERE mahsulot_id = v_m_id),
        ortacha_baho  = (SELECT COALESCE(ROUND(AVG(baho), 2), 0) FROM sharhlar WHERE mahsulot_id = v_m_id)
    WHERE id = v_m_id;

    RETURN NULL;
END;
$$;

CREATE TRIGGER trg_sharh_reyting_avto
AFTER INSERT OR UPDATE OR DELETE ON sharhlar
FOR EACH ROW
EXECUTE FUNCTION trg_yangila_mahsulot_reyting();

-- Test: Yangi 5 baholi sharh kiritish
INSERT INTO sharhlar(mahsulot_id, foydalanuvchi_id, baho, matn)
VALUES (15, 2, 5, 'Ajoyib sifat!');

SELECT id, sharhlar_soni, ortacha_baho FROM mahsulotlar WHERE id = 15;
```

## Tushuntirish va Mantiq:
High-load tizimlarda har bir sahifa ochilganda `AVG()` va `COUNT()` hisoblash bazaga og'irlik qiladi. Denormalizatsiya usuli bilan ustunlar asosiy jadvalga joylashtiriladi va `AFTER INSERT OR UPDATE OR DELETE` triggeri orqali doimo to'g'ri holatda sinxronlashtirib turiladi.

## Ishlash natijasi:
```text
id | sharhlar_soni | ortacha_baho 
----+---------------+--------------
 15 |             6 |         4.83
(1 row)
```


# 862-Topshiriq: Ombor qoldiqlarini boshqarish: AFTER INSERT triggeri orqali tovar kamaytirish
## Topshiriq sharti:
Yangi buyurtma qatori (`buyurtma_tarkibi`) qo'shilganda ombordagi tovar miqdorini kamaytiruvchi va yetarli qoldiq bo'lmasa xatolik beruvchi tranzaksion trigger yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_kamaytir_ombor_qoldiq()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_mavjud_soni INT;
BEGIN
    SELECT mavjud_soni INTO v_mavjud_soni
    FROM ombor_tovarlar
    WHERE mahsulot_id = NEW.mahsulot_id
    FOR UPDATE;

    IF v_mavjud_soni IS NULL OR v_mavjud_soni < NEW.miqdor THEN
        RAISE EXCEPTION 'Omborda yetarli mahsulot yo''q! Mavjud: %, So''ralgan: %', 
            COALESCE(v_mavjud_soni, 0), NEW.miqdor;
    END IF;

    UPDATE ombor_tovarlar
    SET mavjud_soni = mavjud_soni - NEW.miqdor
    WHERE mahsulot_id = NEW.mahsulot_id;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_buyurtma_ombor_kamaytirish
BEFORE INSERT ON buyurtma_tarkibi
FOR EACH ROW
EXECUTE FUNCTION trg_kamaytir_ombor_qoldiq();

-- Test
INSERT INTO buyurtma_tarkibi(buyurtma_id, mahsulot_id, miqdor, narx)
VALUES (101, 4, 3, 450000);
```

## Tushuntirish va Mantiq:
`BEFORE INSERT` triggerida ombor qatori `FOR UPDATE` bilan qulflanadi va yetarli miqdor tekshiriladi. Agar tovar yetarli bo'lsa ombor kamaytiriladi va so'ng buyurtma qatori kiritiladi. Kam bo'lsa xato berilib butun tranzaksiya to'xtatiladi.

## Ishlash natijasi:
```text
INSERT 0 1
```


# 863-Topshiriq: Statement-level trigger (FOR EACH STATEMENT): Partiyaviy o'zgarishlarni bitta log qilish
## Topshiriq sharti:
1000 ta qator bir vaqtda UPDATE qilinganda 1000 marta emas, balki butun SQL so'rovi uchun faqat bitta marta bajariladigan `FOR EACH STATEMENT` triggerini yarating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_baza_ommaviy_yangilash_log()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO ma_muriy_audit(amal, jadval, vaqt)
    VALUES (TG_OP, TG_TABLE_NAME, NOW());

    RAISE NOTICE 'Ommaviy operatsiya muvaffaqiyatli qayd etildi: % jadvalida % amali', TG_TABLE_NAME, TG_OP;
    RETURN NULL;
END;
$$;

CREATE TRIGGER trg_statment_darajasi_log
AFTER UPDATE ON xodimlar
FOR EACH STATEMENT
EXECUTE FUNCTION trg_baza_ommaviy_yangilash_log();

-- Test: Bir vaqtda 50 ta xodimning maoshini oshirish
UPDATE xodimlar SET maosh = maosh * 1.05 WHERE bolim_id = 2;
```

## Tushuntirish va Mantiq:
`FOR EACH STATEMENT` triggeri so'rov nechta qatorga ta'sir qilishidan qat'i nazar (hatto 0 ta qator bo'lsa ham) butun SQL buyrug'i uchun faqat 1 marta ishga tushadi. Bu tizimli monitoring va statistikani hisoblashda katta unumdorlik beradi.

## Ishlash natijasi:
```text
NOTICE:  Ommaviy operatsiya muvaffaqiyatli qayd etildi: xodimlar jadvalida UPDATE amali
UPDATE 50
```


# 864-Topshiriq: PostgreSQL 10+ O'tish jadvallari (REFERENCING NEW TABLE AS new_rows)
## Topshiriq sharti:
`FOR EACH STATEMENT` triggeri ichida yangilangan barcha qatorlarni virtual jadval (transition table) orqali o'qib, o'rtacha maosh oshishini bitta amalda hisoblovchi zamonaviy trigger yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_tahlil_yangilangan_partiya()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_ortacha_oshish NUMERIC;
    v_jami_xodimlar INT;
BEGIN
    SELECT 
        COUNT(*),
        ROUND(AVG(n.maosh - o.maosh), 2)
    INTO v_jami_xodimlar, v_ortacha_oshish
    FROM yangi_qatorlar n
    JOIN eski_qatorlar o ON n.id = o.id;

    RAISE NOTICE 'Ommaviy yangilash tahlili: % ta xodim, O''rtacha o''sish: % so''m',
        v_jami_xodimlar, v_ortacha_oshish;

    RETURN NULL;
END;
$$;

CREATE TRIGGER trg_kuzatuv_otish_jadvallari
AFTER UPDATE OF maosh ON xodimlar
REFERENCING OLD TABLE AS eski_qatorlar NEW TABLE AS yangi_qatorlar
FOR EACH STATEMENT
EXECUTE FUNCTION trg_tahlil_yangilangan_partiya();

-- Test
UPDATE xodimlar SET maosh = maosh + 500000 WHERE bolim_id = 1;
```

## Tushuntirish va Mantiq:
PostgreSQL 10 versiyasidan boshlab joriy qilingan `REFERENCING OLD/NEW TABLE AS` mexanizmi statement-level triggerlarga butun o'zgargan qatorlar to'plamini (Transition Tables) relyatsion ko'rinishda taqdim etadi. Bu qatorma-qator aylanib chiqish (row-by-row iteration) o'rniga bitta set-based operatsiya bajarish imkonini beradi.

## Ishlash natijasi:
```text
NOTICE:  Ommaviy yangilash tahlili: 12 ta xodim, O'rtacha o'sish: 500000.00 so'm
UPDATE 12
```


# 865-Topshiriq: Cheklovlarni dinamik tekshirish: Ish vaqtidan tashqarida o'chirishni taqiqlash
## Topshiriq sharti:
Dam olish kunlari (shanba va yakshanba) yoki ish vaqtidan tashqarida (18:00 dan 09:00 gacha) moliyaviy tranzaksiyalarni o'chirish yoki o'zgartirishni bloklovchi korporativ xavfsizlik triggerini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_ish_vaqti_nazorati()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_hafta_kuni INT;
    v_soat INT;
BEGIN
    v_hafta_kuni := EXTRACT(ISODOW FROM CURRENT_TIMESTAMP); -- 1=Dushanba .. 7=Yakshanba
    v_soat := EXTRACT(HOUR FROM CURRENT_TIMESTAMP);

    -- Shanba (6) yoki Yakshanba (7)
    IF v_hafta_kuni IN (6, 7) THEN
        RAISE EXCEPTION 'Dam olish kunlarida moliyaviy yozuvlarni o''zgartirish taqiqlanadi!';
    END IF;

    -- Soat 09:00 dan 18:00 gacha ruxsat
    IF v_soat < 9 OR v_soat >= 18 THEN
        RAISE EXCEPTION 'Ish vaqtidan (09:00-18:00) tashqarida ma''lumotlarni o''zgartirish cheklangan!';
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_moliyaviy_xavfsizlik_vaqti
BEFORE UPDATE OR DELETE ON tolov_operatsiyalari
FOR EACH ROW
EXECUTE FUNCTION trg_ish_vaqti_nazorati();

-- Test (Ish vaqtidan tashqarida chaqirilganda xato beradi)
UPDATE tolov_operatsiyalari SET summa = 1000 WHERE id = 1;
```

## Tushuntirish va Mantiq:
Ushbu trigger dinamik biznes cheklovlarini joriy etadi. ANSI SQL `CHECK` cheklovlari vaqtga (`CURRENT_TIMESTAMP`) bog'liq ifodalarni qabul qilmaydi (chunki ular deterministik bo'lishi shart). Triggerlar esa bunday vaqtinchalik va dinamik xavfsizlik qoidalarini mukammal bajaradi.

## Ishlash natijasi:
```text
ERROR:  Ish vaqtidan (09:00-18:00) tashqarida ma'lumotlarni o'zgartirish cheklangan!
```


# 866-Topshiriq: Triggerlarning bajarilish tartibini boshqarish (Alphabetical order)
## Topshiriq sharti:
Bitta jadval va bitta hodisada ikkita BEFORE trigger mavjud bo'lganda, ularning qaysi biri birinchi bajarilishini qat'iy nazorat qilish usulini ko'rsating.

## Yechim (SQL kodi):
```sql
-- PostgreSQL triggerlarni ularning nomining alfavit tartibi bo'yicha bajaradi!
-- 1. Birinchi bajariluvchi trigger: 01_tozalash
CREATE OR REPLACE FUNCTION trg_qadam_1_tozalash()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.nomi := TRIM(NEW.nomi);
    RETURN NEW;
END; $$;

CREATE TRIGGER a01_trg_tozalash
BEFORE INSERT ON toifalar
FOR EACH ROW EXECUTE FUNCTION trg_qadam_1_tozalash();

-- 2. Ikkinchi bajariluvchi trigger: 02_tekshirish
CREATE OR REPLACE FUNCTION trg_qadam_2_tekshirish()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF LENGTH(NEW.nomi) < 3 THEN
        RAISE EXCEPTION 'Toifa nomi kamida 3 belgidan iborat bolishi shart!';
    END IF;
    RETURN NEW;
END; $$;

CREATE TRIGGER a02_trg_tekshirish
BEFORE INSERT ON toifalar
FOR EACH ROW EXECUTE FUNCTION trg_qadam_2_tekshirish();

-- Test
INSERT INTO toifalar(nomi) VALUES ('  IT  ');
SELECT * FROM toifalar WHERE nomi = 'IT';
```

## Tushuntirish va Mantiq:
PostgreSQL bir xil voqeaga bog'langan bir nechta triggerlarni ularning nomlarining alfavit (ASCII) tartibida ketma-ket bajaradi (`a01_...`, `a02_...`). Shuning uchun oldin tozalash, so'ngra validatsiya qilish ketma-ketligini trigger nomlarini to'g'ri nomlash orqali ta'minlash mumkin.

## Ishlash natijasi:
```text
id | nomi 
----+------
  8 | IT
(1 row)
```


# 867-Topshiriq: Rekursiv triggerlarning oldini olish (Infinite Loop Protection)
## Topshiriq sharti:
Trigger ichida xuddi shu jadval yangilanganda cheksiz aylanma (infinite recursion) yuzaga kelmasligi uchun `pg_trigger_depth()` orqali himoya mexanizmini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_xavfsiz_rekursiya()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Agar trigger o'z-o'zini ichma-ich chaqirayotgan bo'lsa, to'xtatish
    IF pg_trigger_depth() > 1 THEN
        RETURN NEW;
    END IF;

    -- Xuddi shu jadval ustida qo'shimcha amaliyot
    UPDATE hisoblar
    SET keshbek_ball = keshbek_ball + (NEW.balans * 0.01)
    WHERE id = NEW.id;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_hisob_yangilanishi
AFTER UPDATE OF balans ON hisoblar
FOR EACH ROW
EXECUTE FUNCTION trg_xavfsiz_rekursiya();

-- Test
UPDATE hisoblar SET balans = 2000000 WHERE id = 3;
```

## Tushuntirish va Mantiq:
`pg_trigger_depth()` joriy triggerlar chaqiruv steki chuqurligini qaytaradi. Boshlang'ich chaqiruvda u 1 ga teng bo'ladi. Agar trigger o'zi UPDATE qilib, o'zini qayta qo'zg'atsa, chuqurlik 2 bo'ladi va `pg_trigger_depth() > 1` sharti orqali rekursiya darhol uziladi.

## Ishlash natijasi:
```text
UPDATE 1
```


# 868-Topshiriq: Faqat ma'lum ustunlar o'zgarganda ishlovchi trigger (UPDATE OF column)
## Topshiriq sharti:
Foydalanuvchining boshqa ma'lumotlari (ism, telefon) o'zgarganda ishlamay, faqat va faqat `parol_hash` ustuni yangilangandagina xavfsizlik bildirishnomasi jo'natuvchi trigger yarating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_parol_almashdi_bildirish()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO xavfsizlik_bildirishnomalari(foydalanuvchi_id, xabar, vaqt)
    VALUES (NEW.id, 'Sizning hisob parolingiz muvaffaqiyatli o''zgartirildi!', NOW());

    RAISE NOTICE 'Foydalanuvchi ID % uchun parolni almashtirish xabari yaratildi.', NEW.id;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_parol_kuzatuv
AFTER UPDATE OF parol_hash ON foydalanuvchilar
FOR EACH ROW
EXECUTE FUNCTION trg_parol_almashdi_bildirish();

-- Test 1: Ism o'zgardi (trigger ishlamaydi)
UPDATE foydalanuvchilar SET ism = 'Dilshodbek' WHERE id = 4;

-- Test 2: Parol o'zgardi (trigger ishga tushadi)
UPDATE foydalanuvchilar SET parol_hash = 'd8578edf8458ce06fbc5bb76a58c5ca4' WHERE id = 4;
```

## Tushuntirish va Mantiq:
`AFTER UPDATE OF ustun_nomi` sintaksisi PostgreSQL ga so'rovda aynan shu ustun o'zgargandagina trigger chaqiruvini rejalashtirishni buyuradi. Bu keraksiz trigger chaqiruvlarini 90% gacha kamaytiradi.

## Ishlash natijasi:
```text
NOTICE:  Foydalanuvchi ID 4 uchun parolni almashtirish xabari yaratildi.
UPDATE 1
```


# 869-Topshiriq: Trigger yordamida jadval qatorlari soni chegarasini (Quota/Limit) nazorat qilish
## Topshiriq sharti:
Har bir foydalanuvchi tizimda ko'pi bilan 5 tagacha faol bank kartasi bog'lashi mumkinligini qat'iy kafolatlovchi BEFORE INSERT triggerini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_tekshir_karta_limiti()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_karta_soni INT;
BEGIN
    SELECT COUNT(*) INTO v_karta_soni
    FROM foydalanuvchi_kartalari
    WHERE foydalanuvchi_id = NEW.foydalanuvchi_id
      AND holat = 'FAOL';

    IF v_karta_soni >= 5 THEN
        RAISE EXCEPTION 'Limit tugadi! Bitta foydalanuvchiga 5 tadan ortiq faol karta ulanishi mumkin emas!'
            USING ERRCODE = 'check_violation';
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_karta_limit_nazorat
BEFORE INSERT ON foydalanuvchi_kartalari
FOR EACH ROW
EXECUTE FUNCTION trg_tekshir_karta_limiti();

-- Test
INSERT INTO foydalanuvchi_kartalari(foydalanuvchi_id, karta_raqam, holat)
VALUES (10, '8600123412345678', 'FAOL');
```

## Tushuntirish va Mantiq:
Jadvallararo cheklovlarni (masalan, bitta parent uchun child qatorlar soni) oddiy `CHECK` bilan tekshirib bo'lmaydi. `BEFORE INSERT` triggeri orqali hisoblangan agregat yordamida qat'iy biznes kvotalari va limitlarini qo'llash mumkin.

## Ishlash natijasi:
```text
INSERT 0 1
```


# 870-Topshiriq: Event Trigger: DDL buyruqlari tugaganda audit qilish (ddl_command_end)
## Topshiriq sharti:
Ma'lumotlar bazasida kimdir `CREATE TABLE`, `ALTER TABLE` yoki `DROP TABLE` bajarganda uni avtomatik tarzda maxsus `ddl_audit_jurnali` jadvaliga yozib boruvchi Event Triggerni yarating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION evt_ddl_audit_log()
RETURNS EVENT_TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    obj RECORD;
BEGIN
    FOR obj IN SELECT * FROM pg_event_trigger_ddl_commands() LOOP
        INSERT INTO ddl_audit_jurnali(amal, obekt_turi, obekt_nomi, foydalanuvchi, vaqt)
        VALUES (
            obj.command_tag,
            obj.object_type,
            obj.object_identity,
            CURRENT_USER,
            NOW()
        );
        RAISE NOTICE 'DDL Hodisasi: % bajarildi -> % (%)', 
            obj.command_tag, obj.object_identity, obj.object_type;
    END LOOP;
END;
$$;

CREATE EVENT TRIGGER trg_kuzatuv_ddl
ON ddl_command_end
EXECUTE FUNCTION evt_ddl_audit_log();

-- Test: Yangi sinov jadvali ochish
CREATE TABLE test_ddl_jadval (id INT);
```

## Tushuntirish va Mantiq:
Event Triggerlar oddiy triggerlardan tubdan farq qiladi: ular jadvalga emas, balki butun ma'lumotlar bazasiga biriktiriladi va DDL (Data Definition Language) hodisalarida (`ddl_command_end`, `sql_drop`, `table_rewrite`) ishga tushadi. `pg_event_trigger_ddl_commands()` tizim funksiyasi bajarilgan barcha DDL ob'ektlarini ko'rsatadi.

## Ishlash natijasi:
```text
NOTICE:  DDL Hodisasi: CREATE TABLE bajarildi -> public.test_ddl_jadval (table)
CREATE TABLE
```


# 871-Topshiriq: Event Trigger: Muhim ishlab chiqarish jadvallarini o'chirishni taqiqlash (sql_drop)
## Topshiriq sharti:
Dasturchi yoki DBA adashib `DROP TABLE` orqali tizimning muhim asosiy jadvallarini o'chirib yuborishiga yo'l qo'ymaydigan `sql_drop` Event Triggerini yarating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION evt_bloklash_muhim_ochirish()
RETURNS EVENT_TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    obj RECORD;
BEGIN
    FOR obj IN SELECT * FROM pg_event_trigger_dropped_objects() LOOP
        IF obj.object_type = 'table' AND obj.object_identity IN ('public.mijozlar', 'public.hisoblar', 'public.tolovlar') THEN
            RAISE EXCEPTION 'Kritik xatolik: Muhim jadvalni (%) o''chirish bazaviy qoidalar bo''yicha qat''iyan man etiladi!',
                obj.object_identity;
        END IF;
    END LOOP;
END;
$$;

CREATE EVENT TRIGGER trg_himoya_muhim_jadvallar
ON sql_drop
EXECUTE FUNCTION evt_bloklash_muhim_ochirish();

-- Test: Asosiy mijozlar jadvalini o'chirishga urinish
DROP TABLE mijozlar;
```

## Tushuntirish va Mantiq:
`ON sql_drop` hodisasi ob'ektlar o'chirilayotganda ishga tushadi. `pg_event_trigger_dropped_objects()` orqali o'chirilishi mo'ljallangan ob'ektlar ro'yxati tekshiriladi va agar ular orasida muhim jadvallar bo'lsa darhol EXCEPTION chiqarilib, butun DROP bekor qilinadi.

## Ishlash natijasi:
```text
ERROR:  Kritik xatolik: Muhim jadvalni (public.mijozlar) o'chirish bazaviy qoidalar bo'yicha qat'iyan man etiladi!
```


# 872-Topshiriq: Triggerlarni vaqtincha o'chirish va qayta yoqish (DISABLE / ENABLE TRIGGER)
## Topshiriq sharti:
Katta hajmdagi ma'lumotlarni ommaviy yuklash (bulk load) paytida triggerlarni o'chirib turish va yuklash tugagach qayta yoqish buyruqlarini yozing.

## Yechim (SQL kodi):
```sql
-- 1. Bitta aniq triggerni vaqtincha to'xtatish
ALTER TABLE xodimlar DISABLE TRIGGER trg_xodimlar_audit;

-- 2. Jadvaldagi barcha triggerlarni to'xtatish
ALTER TABLE xodimlar DISABLE TRIGGER ALL;

-- 3. Ommaviy yuklashni amalga oshirish
-- (Bu vaqtda triggerlar ishlamaydi, tezlik keskin oshadi)
INSERT INTO xodimlar (ism, familiya, maosh, bolim_id)
SELECT 'Xodim_' || i, 'Familiya_' || i, 5000000, 1
FROM generate_series(1, 1000) AS i;

-- 4. Barcha triggerlarni qayta yoqish
ALTER TABLE xodimlar ENABLE TRIGGER ALL;

-- Trigger holatini pg_trigger tizim katalogidan tekshirish
SELECT tgname, tgenabled FROM pg_trigger WHERE tgrelid = 'xodimlar'::regclass;
```

## Tushuntirish va Mantiq:
`ALTER TABLE ... DISABLE TRIGGER ALL` buyrug'i jadvaldagi foydalanuvchi triggerlarini vaqtincha to'xtatadi (`tgenabled = 'd'`). `ENABLE TRIGGER ALL` esa ularni qayta normal holatga (`'O'`) keltiradi. Bu millionlab qatorlarni migratsiya qilishda sarflanadigan vaqtni bir necha barobar qisqartiradi.

## Ishlash natijasi:
```text
tgname            | tgenabled 
-----------------------------+-----------
 trg_xodimlar_audit          | O
 trg_avto_yangilangan_vaqt   | O
(2 rows)
```


# 873-Topshiriq: ENABLE ALWAYS TRIGGER: Replikatsiya va tizim rejimlarida ham doimiy ishlovchi trigger
## Topshiriq sharti:
Baza replikatsiyasi (Logical Replication) paytida ham, replika serverida audit jurnallari uzilib qolmasligi uchun doimiy ishlovchi `ENABLE ALWAYS` triggerini yarating.

## Yechim (SQL kodi):
```sql
-- Triggerni doimiy faol rejimga o'tkazish
ALTER TABLE xavfsizlik_auditi ENABLE ALWAYS TRIGGER trg_xavfsizlik_yozuv;

-- Katalogdan tekshirish
SELECT tgname, tgenabled 
FROM pg_trigger 
WHERE tgname = 'trg_xavfsizlik_yozuv';
```

## Tushuntirish va Mantiq:
Oddiy holatda replikatsiya workerlari ishlayotganda (`session_replication_role = 'replica'`) odatiy triggerlar e'tiborga olinmaydi. `ENABLE ALWAYS` rejimi (`tgenabled = 'A'`) esa server qaysi rejimda bo'lishidan qat'i nazar triggerni har qanday holatda chaqirilishini kafolatlaydi.

## Ishlash natijasi:
```text
tgname         | tgenabled 
-----------------------+-----------
 trg_xavfsizlik_yozuv  | A
(1 row)
```


# 874-Topshiriq: TG_ARGV parametrlaridan foydalanuvchi qayta ishlatiluvchi (Generic) trigger
## Topshiriq sharti:
Trigger yaratishda berilgan matnli parametrlarni (`TG_ARGV`) o'qib, bir nechta turli jadvallar uchun yagona trigger funksiyasidan foydalanish amaliyotini ko'rsating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_umumiy_chegara_tekshiruvchi()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_ustun_nomi TEXT := TG_ARGV[0];
    v_min_qiymat NUMERIC := TG_ARGV[1]::NUMERIC;
    v_joriy_qiymat NUMERIC;
BEGIN
    -- NEW rekordidagi dinamik ustun qiymatini olish
    EXECUTE format('SELECT ($1).%I', v_ustun_nomi) INTO v_joriy_qiymat USING NEW;

    IF v_joriy_qiymat < v_min_qiymat THEN
        RAISE EXCEPTION '% jadvalida % ustuni kamida % bolishi kerak! Berildi: %',
            TG_TABLE_NAME, v_ustun_nomi, v_min_qiymat, v_joriy_qiymat;
    END IF;

    RETURN NEW;
END;
$$;

-- Funksiyaga parametrlar berib turli jadvallarga bog'lash
CREATE TRIGGER trg_maosh_chegara
BEFORE INSERT OR UPDATE ON xodimlar
FOR EACH ROW
EXECUTE FUNCTION trg_umumiy_chegara_tekshiruvchi('maosh', '1000000');

CREATE TRIGGER trg_narx_chegara
BEFORE INSERT OR UPDATE ON mahsulotlar
FOR EACH ROW
EXECUTE FUNCTION trg_umumiy_chegara_tekshiruvchi('narx', '500');

-- Test
INSERT INTO mahsulotlar (nomi, narx) VALUES ('Ruchka', 200);
```

## Tushuntirish va Mantiq:
`TG_ARGV[]` massivi `CREATE TRIGGER ... EXECUTE FUNCTION funksiya('param1', 'param2')` chaqiruvidagi argumentlarni ushlab oladi. Bu bitta universal trigger logikasini kodni takrorlamasdan (DRY prinsipi) o'nlab jadvallarga xizmat ko'rsatishiga imkon beradi.

## Ishlash natijasi:
```text
ERROR:  mahsulotlar jadvalida narx ustuni kamida 500 bolishi kerak! Berildi: 200
```


# 875-Topshiriq: Bank hisoblarida overdraft (manfiy balans) oldini oluvchi BEFORE UPDATE triggeri
## Topshiriq sharti:
Hisobdan pul yechilganda hisob balansi manfiy bo'lib ketmasligini tranzaksiya darajasida bloklovchi qat'iy tekshiruvchi trigger yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_tekshir_overdraft()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.balans < 0 THEN
        RAISE EXCEPTION 'Operatsiya rad etildi! Hisob balansi manfiy bo''lishi mumkin emas. Joriy balans: %, Olinmoqda: %',
            OLD.balans, (OLD.balans - NEW.balans);
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_himoya_hisob_balans
BEFORE UPDATE OF balans ON bank_hisoblari
FOR EACH ROW
EXECUTE FUNCTION trg_tekshir_overdraft();

-- Test: Balansi 100 000 bo'lgan hisobdan 150 000 yechishga urinish
UPDATE bank_hisoblari SET balans = balans - 150000 WHERE id = 12 AND balans = 100000;
```

## Tushuntirish va Mantiq:
`BEFORE UPDATE OF balans` triggeri balans o'zgarayotganda kiritilayotgan `NEW.balans` qiymatini tekshiradi. Agar balans 0 dan kichik bo'lsa, xatolik berib pul yechilishini to'xtatadi.

## Ishlash natijasi:
```text
ERROR:  Operatsiya rad etildi! Hisob balansi manfiy bo'lishi mumkin emas. Joriy balans: 100000.00, Olinmoqda: 150000.00
```


# 876-Topshiriq: Kaskadli yangilanishni (Cascade Update) qo'lda boshqaruvchi trigger
## Topshiriq sharti:
Mijozning telefon raqami yangilanganda, unga tegishli barcha buyurtmalar, kuryer topshiriqlari va xabarlar jadvallaridagi eski telefon raqamini avtomatik sinxronlashtiruvchi trigger yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_kaskad_telefon_yangilash()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.telefon <> OLD.telefon THEN
        -- Buyurtmalar jadvalidagi kontaktni yangilash
        UPDATE buyurtmalar
        SET mijoz_telefon = NEW.telefon
        WHERE mijoz_id = NEW.id;

        -- Yetkazib berish kuryer topshiriqlarini yangilash
        UPDATE yetkazib_berish
        SET aloqa_telefon = NEW.telefon
        WHERE mijoz_id = NEW.id AND holat IN ('KUTILMOQDA', 'YOLDA');

        RAISE NOTICE 'Mijoz ID % ning yangi telefoni barcha faol xizmatlarga sinxronlandi.', NEW.id;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_mijoz_telefon_kaskad
AFTER UPDATE OF telefon ON mijozlar
FOR EACH ROW
EXECUTE FUNCTION trg_kaskad_telefon_yangilash();

-- Test
UPDATE mijozlar SET telefon = '+998991112233' WHERE id = 8;
```

## Tushuntirish va Mantiq:
`AFTER UPDATE OF telefon` triggeri mijozning telefon raqami haqiqatdan o'zgarganini aniqlaydi (`NEW.telefon <> OLD.telefon`) va tizimdagi barcha faol hujjatlardagi aloqa ma'lumotlarini kaskad tarzida avtomatik yangilaydi.

## Ishlash natijasi:
```text
NOTICE:  Mijoz ID 8 ning yangi telefoni barcha faol xizmatlarga sinxronlandi.
UPDATE 1
```


# 877-Topshiriq: Sotuv savati (Shopping Cart) umumiy summasini avtomatik qayta hisoblash
## Topshiriq sharti:
Savat tarkibiga yangi tovar qo'shilganda, miqdori o'zgarganda yoki o'chirilganda asosiy savat jadvalidagi `umumiy_summa`ni yangilovchi trigger yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_yangila_savat_summa()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_savat_id INT;
BEGIN
    v_savat_id := COALESCE(NEW.savat_id, OLD.savat_id);

    UPDATE savatlar
    SET umumiy_summa = (
        SELECT COALESCE(SUM(miqdor * narx), 0)
        FROM savat_elementlari
        WHERE savat_id = v_savat_id
    ),
    yangilangan_vaqt = NOW()
    WHERE id = v_savat_id;

    RETURN NULL;
END;
$$;

CREATE TRIGGER trg_savat_summa_avto
AFTER INSERT OR UPDATE OR DELETE ON savat_elementlari
FOR EACH ROW
EXECUTE FUNCTION trg_yangila_savat_summa();

-- Test: Savatga tovar qo'shish
INSERT INTO savat_elementlari(savat_id, mahsulot_id, miqdor, narx)
VALUES (55, 12, 2, 85000);

SELECT id, umumiy_summa FROM savatlar WHERE id = 55;
```

## Tushuntirish va Mantiq:
`AFTER INSERT OR UPDATE OR DELETE` barcha DML amallarini bitta triggerda qamrab oladi. `COALESCE(NEW.savat_id, OLD.savat_id)` INSERT/UPDATE paytida NEW'dan, DELETE paytida esa OLD'dan savat ID sini to'g'ri oladi va doimo to'g'ri umumiy summani ushlab turadi.

## Ishlash natijasi:
```text
id | umumiy_summa 
----+--------------
 55 |    170000.00
(1 row)
```


# 878-Topshiriq: O'zgartirilmas (Immutable / Append-Only) jadval yaratish
## Topshiriq sharti:
Tranzaksiyalar ledger (buxgalteriya daftari) jadvaliga yangi yozuv qo'shishga ruxsat beruvchi, lekin mavjud yozuvlarni UPDATE yoki DELETE qilishni mutlaqo taqiqlovchi trigger yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_bloklash_ozgarish_ledger()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE EXCEPTION 'Buxgalteriya ledger jadvalida yozuvlarni tahrirlash yoki o''chirish qat''iyan man etiladi!'
        USING ERRCODE = 'restrict_violation';
END;
$$;

CREATE TRIGGER trg_ledger_faqat_qoshish
BEFORE UPDATE OR DELETE ON buxgalteriya_ledger
FOR EACH ROW
EXECUTE FUNCTION trg_bloklash_ozgarish_ledger();

-- Test: Tahrirlashga urinish
UPDATE buxgalteriya_ledger SET summa = 999999 WHERE id = 1;
```

## Tushuntirish va Mantiq:
Fintex va moliyaviy audit tizimlarida jadvallar 'Append-Only' (faqat qo'shiladigan) bo'lishi shart. Ushbu trigger UPDATE va DELETE buyruqlarini boshlang'ich bosqichidayoq to'xtatib, ma'lumotlar soxtalashtirilishining (tampering) oldini oladi.

## Ishlash natijasi:
```text
ERROR:  Buxgalteriya ledger jadvalida yozuvlarni tahrirlash yoki o'chirish qat'iyan man etiladi!
```


# 879-Topshiriq: Trigger orqali bildirishnomalar yuborish (NOTIFY / LISTEN)
## Topshiriq sharti:
Yangi shoshilinch xabar (`ogohlantirishlar`) kiritilganda tashqi backend serverlariga (Node.js, Python, Go) PostgreSQL ning `NOTIFY` kanali orqali zudlik bilan signal jo'natuvchi trigger yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_yubor_jonli_bildirishnoma()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_yuklama TEXT;
BEGIN
    -- JSON ko'rinishida xabar tayyorlash
    v_yuklama := json_build_object(
        'hodisa', 'YANGI_XABAR',
        'xabar_id', NEW.id,
        'sarlavha', NEW.sarlavha,
        'daraja', NEW.daraja,
        'vaqt', NOW()
    )::TEXT;

    -- 'jonli_kanal' ga xabar jo'natish
    PERFORM pg_notify('jonli_kanal', v_yuklama);

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_ogohlantirish_notify
AFTER INSERT ON ogohlantirishlar
FOR EACH ROW
EXECUTE FUNCTION trg_yubor_jonli_bildirishnoma();

-- Test
INSERT INTO ogohlantirishlar(sarlavha, daraja) 
VALUES ('Server harorati 85C dan oshdi', 'KRITIK');
```

## Tushuntirish va Mantiq:
`pg_notify('kanal_nomi', yuklama)` funksiyasi PostgreSQL pub/sub mexanizmini ishga tushiradi. Ulanib turgan tashqi mikroservislar ma'lumotlar bazasini har soniyada so'rab turmasdan (polling o'rniga), trigger yuborgan hodisalarni reaktiv usulda ushlab oladi.

## Ishlash natijasi:
```text
INSERT 0 1
```


# 880-Topshiriq: Yagona faol holatni (Unique Active State) ta'minlovchi BEFORE UPDATE/INSERT triggeri
## Topshiriq sharti:
Foydalanuvchining faqat bitta asosiy to'lov kartasi (`asosiy = TRUE`) bo'lishi mumkinligini, yangi karta asosiy qilib belgilanganda boshqa kartalarning asosiy belgisini avtomatik olib tashlovchi trigger yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_yagona_asosiy_karta()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.asosiy = TRUE THEN
        -- Shu foydalanuvchining boshqa kartalaridan asosiy belgisini yechish
        UPDATE foydalanuvchi_kartalari
        SET asosiy = FALSE
        WHERE foydalanuvchi_id = NEW.foydalanuvchi_id
          AND id <> COALESCE(NEW.id, -1)
          AND asosiy = TRUE;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_karta_asosiy_boshqaruv
BEFORE INSERT OR UPDATE OF asosiy ON foydalanuvchi_kartalari
FOR EACH ROW
EXECUTE FUNCTION trg_yagona_asosiy_karta();

-- Test
UPDATE foydalanuvchi_kartalari SET asosiy = TRUE WHERE id = 3 AND foydalanuvchi_id = 1;
SELECT id, karta_raqam, asosiy FROM foydalanuvchi_kartalari WHERE foydalanuvchi_id = 1;
```

## Tushuntirish va Mantiq:
Ushbu trigger biznes mantig'idagi 'faqat bitta element asosiy bo'lishi mumkin' qoidasini to'liq avtomatlashtiradi. Yangi karta asosiy bo'lganda, avvalgi barcha faol asosiy kartalar avtomatik ikkinchi darajali qilinadi.

## Ishlash natijasi:
```text
id |   karta_raqam    | asosiy 
----+------------------+--------
  1 | 8600************ | f
  2 | 9860************ | f
  3 | 4000************ | t
(3 rows)
```


# 881-Topshiriq: Parolning murakkabligini tekshiruvchi BEFORE INSERT/UPDATE triggeri
## Topshiriq sharti:
Parol matni kiritilganda uning kamida 8 ta belgidan iboratligi, kamida bitta katta harf, bitta kichik harf va bitta son qatnashganligini regex orqali tekshiruvchi trigger yarating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_tekshir_parol_talablari()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Parol uzunligi
    IF LENGTH(NEW.parol_ochiq) < 8 THEN
        RAISE EXCEPTION 'Parol kamida 8 ta belgidan iborat bo''lishi kerak!';
    END IF;

    -- Katta harf tekshiruvi
    IF NEW.parol_ochiq !~ '[A-Z]' THEN
        RAISE EXCEPTION 'Parolda kamida bitta bosh (katta) harf qatnashishi shart!';
    END IF;

    -- Kichik harf tekshiruvi
    IF NEW.parol_ochiq !~ '[a-z]' THEN
        RAISE EXCEPTION 'Parolda kamida bitta kichik harf qatnashishi shart!';
    END IF;

    -- Raqam tekshiruvi
    IF NEW.parol_ochiq !~ '[0-9]' THEN
        RAISE EXCEPTION 'Parolda kamida bitta son bo''lishi shart!';
    END IF;

    -- Parolni xeshlab saqlash va ochiq matnni tozalash
    NEW.parol_hash := MD5(NEW.parol_ochiq || '_tuz');
    NEW.parol_ochiq := NULL;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_foydalanuvchi_parol_xavfsizlik
BEFORE INSERT OR UPDATE OF parol_ochiq ON foydalanuvchi_akkountlari
FOR EACH ROW
WHEN (NEW.parol_ochiq IS NOT NULL)
EXECUTE FUNCTION trg_tekshir_parol_talablari();

-- Test
INSERT INTO foydalanuvchi_akkountlari(login, parol_ochiq) 
VALUES ('bekzod', 'Maxfiy123');
```

## Tushuntirish va Mantiq:
Muntazam ifodalar (`!~` regex mos kelmaslik) yordamida parollarning xavfsizlik talablariga mosligi bazaga kiritilishidan oldin tekshiriladi. Shundan so'ng parol ochiq holatda qoldirilmasdan xeshlangan ustunga o'tkaziladi.

## Ishlash natijasi:
```text
INSERT 0 1
```


# 882-Topshiriq: Trigger orqali qatorning UUID identifikatorini avtomatik hosil qilish
## Topshiriq sharti:
Agar yangi qator kiritilayotganda `uuid` ustuni bo'sh (NULL) bo'lsa, unga `gen_random_uuid()` orqali avtomatik 4-versiyali UUID biriktiruvchi BEFORE INSERT triggerini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_avto_uuid_generatsiya()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.unikal_id IS NULL THEN
        NEW.unikal_id := gen_random_uuid();
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_hujjatlar_uuid
BEFORE INSERT ON hujjatlar
FOR EACH ROW
EXECUTE FUNCTION trg_avto_uuid_generatsiya();

-- Test
INSERT INTO hujjatlar(nomi) VALUES ('Shartnoma #104');
SELECT id, nomi, unikal_id FROM hujjatlar WHERE nomi = 'Shartnoma #104';
```

## Tushuntirish va Mantiq:
`BEFORE INSERT` triggeri orqali birlamchi yoki tashqi identifikatorlar bo'sh qolmasligi ta'minlanadi. Agar chaqiruvchi tizim UUID uzatmagan bo'lsa, trigger uni xavfsiz tasodifiy kriptografik algoritm orqali to'ldiradi.

## Ishlash natijasi:
```text
id |      nomi       |              unikal_id               
----+-----------------+--------------------------------------
  1 | Shartnoma #104  | a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11
(1 row)
```


# 883-Topshiriq: Trigger orqali avtomatik qator arxivlash (Data Archiving)
## Topshiriq sharti:
Mijoz shartnomasi 'BEKOR_QILINDI' yoki 'MUDDATI_OTGAN' holatiga o'tkazilganda, ushbu qatorni avtomatik tarzda `arxiv_shartnomalar` jadvaliga ko'chirib, asosiy jadvaldan o'chiruvchi AFTER UPDATE triggerini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_arxivla_shartnoma()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.holat IN ('BEKOR_QILINDI', 'MUDDATI_OTGAN') THEN
        -- Arxiv jadvaliga nusxalash
        INSERT INTO arxiv_shartnomalar(shartnoma_id, mijoz_id, sana, arxivlangan_vaqt)
        VALUES (NEW.id, NEW.mijoz_id, NEW.sana, NOW());

        -- Asosiy jadvaldan o'chirish
        DELETE FROM shartnomalar WHERE id = NEW.id;

        RAISE NOTICE 'Shartnoma ID % muvaffaqiyatli arxivlandi va asosiy jadvaldan tozalandi.', NEW.id;
    END IF;

    RETURN NULL;
END;
$$;

CREATE TRIGGER trg_shartnoma_avto_arxiv
AFTER UPDATE OF holat ON shartnomalar
FOR EACH ROW
EXECUTE FUNCTION trg_arxivla_shartnoma();

-- Test
UPDATE shartnomalar SET holat = 'BEKOR_QILINDI' WHERE id = 77;
```

## Tushuntirish va Mantiq:
`AFTER UPDATE OF holat` triggeri shartnoma statusi o'zgarganda qatorni arxiv jadvaliga ko'chiradi va asosiy ishchi jadvalni yengillashtirish maqsadida undan qatorni tozalaydi.

## Ishlash natijasi:
```text
NOTICE:  Shartnoma ID 77 muvaffaqiyatli arxivlandi va asosiy jadvaldan tozalandi.
UPDATE 1
```


# 884-Topshiriq: Trigger orqali elektron imzo va ma'lumotlar butunligi xeshini yangilash
## Topshiriq sharti:
Hujjat jadvalidagi har qanday ustun o'zgarganda, hujjatning yangi ma'lumotlari asosida SHA-256 xeshini qayta hisoblab `imzo_xesh` ustuniga joylovchi BEFORE UPDATE triggerini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_yangila_hujjat_xesh()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_birlashgan_matn TEXT;
BEGIN
    v_birlashgan_matn := NEW.id || '|' || NEW.nomi || '|' || NEW.matn || '|' || NEW.muallif_id;
    NEW.imzo_xesh := encode(digest(v_birlashgan_matn, 'sha256'), 'hex');

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_hujjat_tamper_proof
BEFORE INSERT OR UPDATE ON elektron_hujjatlar
FOR EACH ROW
EXECUTE FUNCTION trg_yangila_hujjat_xesh();

-- Test
INSERT INTO elektron_hujjatlar(id, nomi, matn, muallif_id) 
VALUES (1, 'Buyruq #1', 'Barcha xodimlar rag''batlantirilsin', 10);

SELECT id, nomi, SUBSTRING(imzo_xesh FROM 1 FOR 16) || '...' AS qisqa_xesh 
FROM elektron_hujjatlar WHERE id = 1;
```

## Tushuntirish va Mantiq:
Kriptografik SHA-256 funksiyasi `digest()` orqali amalga oshiriladi. Trigger hujjat maydonlari o'zgargan zahoti yangi xeshni hisoblaydi, bu esa ma'lumotlar tashqaridan noqonuniy o'zgartirilganda soxtalikni darhol fosh qilishga imkon beradi.

## Ishlash natijasi:
```text
id |    nomi    |      qisqa_xesh      
----+------------+----------------------
  1 | Buyruq #1  | 8f4b23c91d4e0a7b...
(1 row)
```


# 885-Topshiriq: Foydalanuvchi oxirgi faollik vaqtini aqlli kechiktirib yangilash
## Topshiriq sharti:
Saytga har bir bosishda DB ga og'irlik tushmasligi uchun, faqatgina oxirgi yangilanishdan 5 daqiqadan ko'proq vaqt o'tgandagina `oxirgi_faollik` ustunini yangilovchi shartli trigger tuzing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_aqlli_faollik_vaqti()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF OLD.oxirgi_faollik IS NULL OR NEW.oxirgi_faollik > OLD.oxirgi_faollik + INTERVAL '5 minutes' THEN
        RETURN NEW;
    ELSE
        -- 5 daqiqa o'tmagan bo'lsa yangilanishni e'tiborsiz qoldirish
        NEW.oxirgi_faollik := OLD.oxirgi_faollik;
        RETURN NEW;
    END IF;
END;
$$;

CREATE TRIGGER trg_faollik_monitoring
BEFORE UPDATE OF oxirgi_faollik ON foydalanuvchilar
FOR EACH ROW
EXECUTE FUNCTION trg_aqlli_faollik_vaqti();

-- Test
UPDATE foydalanuvchilar SET oxirgi_faollik = NOW() WHERE id = 5;
```

## Tushuntirish va Mantiq:
Yuqori yuklamali veb-ilovalarda har bir HTTP so'rovida `users` jadvalini yangilash WAL va disk I/O ni haddan tashqari to'ldirib yuboradi. Ushbu trigger oraliq vaqtni tekshiradi va kichik farqlardagi yangilanishlarni bostirib (throttle) beradi.

## Ishlash natijasi:
```text
UPDATE 1
```


# 886-Topshiriq: Oldingi qiymat bilan yangi qiymat bir xil bo'lsa yangilanishni bekor qilish (No-op Update)
## Topshiriq sharti:
Agar ilova yuborgan UPDATE so'rovidagi yangi qiymatlar eski qiymatlar bilan mutlaqo bir xil bo'lsa, keraksiz disk yozilishining oldini olish uchun amalni to'xtatuvchi trigger yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_bekor_qilish_ozgarmagan_update()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Agar barcha maydonlar aynan bir xil bo'lsa
    IF NEW IS NOT DISTINCT FROM OLD THEN
        RETURN NULL; -- Hech qanday yangilanish sodir bo'lmaydi, qator saqlanadi
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_tejamkor_update
BEFORE UPDATE ON mahsulotlar
FOR EACH ROW
EXECUTE FUNCTION trg_bekor_qilish_ozgarmagan_update();

-- Test: Aynan bir xil qiymat bilan UPDATE yuborish
UPDATE mahsulotlar SET narx = narx WHERE id = 10;
```

## Tushuntirish va Mantiq:
`NEW IS NOT DISTINCT FROM OLD` operatori qatorning har bir ustuni, jumladan `NULL` qiymatlari ham o'zgarmasdan qolganligini tekshiradi. `RETURN NULL;` qaytarilganda PostgreSQL ushbu qator uchun yangi tuple yaratmaydi va MVCC table bloat'ning oldi olinadi.

## Ishlash natijasi:
```text
UPDATE 0
```


# 887-Topshiriq: Barcha triggerlarni o'chirish va tozalash (DROP TRIGGER)
## Topshiriq sharti:
Jadvaldan mavjud triggerlarni xavfsiz tarzda o'chirish (`IF EXISTS`) va unga bog'liq trigger funksiyalarini bartaraf etish buyruqlarini bajaring.

## Yechim (SQL kodi):
```sql
-- 1. Triggerni jadvaldan uzish
DROP TRIGGER IF EXISTS trg_tejamkor_update ON mahsulotlar;

-- 2. Bir nechta triggerlarni ketma-ket o'chirish
DROP TRIGGER IF EXISTS trg_narx_sakrash_monitoring ON mahsulotlar;

-- 3. Trigger funksiyasini o'chirish
DROP FUNCTION IF EXISTS trg_bekor_qilish_ozgarmagan_update();

-- Tekshirish: mahsulotlar jadvalida trigger qolmaganligini ko'rish
SELECT tgname FROM pg_trigger WHERE tgrelid = 'mahsulotlar'::regclass AND NOT tgisinternal;
```

## Tushuntirish va Mantiq:
`DROP TRIGGER trigger_nomi ON jadval_nomi;` sintaksisi triggerni o'chiradi. Trigger funksiyasi alohida ob'ekt bo'lgani sababli, `DROP FUNCTION` yordamida mustaqil ravishda o'chirilishi talab etiladi.

## Ishlash natijasi:
```text
tgname 
--------
(0 rows)
```


# 888-Topshiriq: Trigger orqali qatorlar o'rtasida mantiqiy zanjir (Sessiya davomiyligi) hosil qilish
## Topshiriq sharti:
Foydalanuvchi yangi harakat bajarganda, uning oldingi harakatining `tugash_vaqti` ustuniga yangi harakatning boshlanish vaqtini avtomatik yozib qo'yuvchi trigger tuzing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_yopish_oldingi_harakat()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE foydalanuvchi_sessiya_harakatlari
    SET tugash_vaqti = NEW.boshlanish_vaqti
    WHERE foydalanuvchi_id = NEW.foydalanuvchi_id
      AND tugash_vaqti IS NULL
      AND id <> COALESCE(NEW.id, -1);

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_harakat_zanjiri
BEFORE INSERT ON foydalanuvchi_sessiya_harakatlari
FOR EACH ROW
EXECUTE FUNCTION trg_yopish_oldingi_harakat();

-- Test
INSERT INTO foydalanuvchi_sessiya_harakatlari(foydalanuvchi_id, sahifa, boshlanish_vaqti)
VALUES (14, '/bosh-sahifa', '2024-06-15 10:00:00');

INSERT INTO foydalanuvchi_sessiya_harakatlari(foydalanuvchi_id, sahifa, boshlanish_vaqti)
VALUES (14, '/katalog', '2024-06-15 10:04:30');

SELECT id, sahifa, boshlanish_vaqti, tugash_vaqti 
FROM foydalanuvchi_sessiya_harakatlari WHERE foydalanuvchi_id = 14;
```

## Tushuntirish va Mantiq:
Vaqt ketma-ketliklari (Time-series) tahlilida har bir harakat davomiyligini aniqlash uchun oldingi qatorning tugash vaqtini yopish talab etiladi. Ushbu trigger avtomatik tarzda ochiq qolgan avvalgi yozuvni topib, uning tugash vaqtini muhrlaydi.

## Ishlash natijasi:
```text
id |    sahifa    |   boshlanish_vaqti  |    tugash_vaqti     
----+--------------+---------------------+---------------------
  1 | /bosh-sahifa | 2024-06-15 10:00:00 | 2024-06-15 10:04:30
  2 | /katalog     | 2024-06-15 10:04:30 | 
(2 rows)
```


# 889-Topshiriq: Valyutalar kursi o'zgarganda narxlarni qayta hisoblovchi trigger
## Topshiriq sharti:
AQSH dollari kursi yangilanganda, narxi dollar bilan bog'langan barcha tovarlarning so'mdagi narxini zudlik bilan qayta hisoblovchi AFTER UPDATE triggerini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_avto_kurs_qayta_hisob()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.kurs <> OLD.kurs AND NEW.kod = 'USD' THEN
        UPDATE tovarlar
        SET narx_som = ROUND(narx_usd * NEW.kurs, 2)
        WHERE valyuta_kod = 'USD';

        RAISE NOTICE 'Barcha tovarlar narxi yangi kurs (%) bo''yicha qayta hisoblandi.', NEW.kurs;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_kurs_yangilanish
AFTER UPDATE OF kurs ON valyutalar
FOR EACH ROW
EXECUTE FUNCTION trg_avto_kurs_qayta_hisob();

-- Test
UPDATE valyutalar SET kurs = 12900.00 WHERE kod = 'USD';
```

## Tushuntirish va Mantiq:
Markaziy ma'lumotlar (kurslar, soliq stavkalari) o'zgarganda `AFTER UPDATE` triggeri orqali unga bog'liq millionlab qatorlardagi hisob-kitoblarni sinxronlashtirish relyatsion bazalarning kuchli jihatlaridan biridir.

## Ishlash natijasi:
```text
NOTICE:  Barcha tovarlar narxi yangi kurs (12900.00) bo'yicha qayta hisoblandi.
UPDATE 1
```


# 890-Topshiriq: Trigger orqali qatorlar o'rtasida ustun qiymatini cheklash (Parent/Child integrity)
## Topshiriq sharti:
Faqat 'FAOL' holatdagi yetkazib beruvchilardan tovar qabul qilinishini kafolatlovchi, agar yetkazib beruvchi bloklangan bo'lsa xatolik chiqaruvchi BEFORE INSERT triggerini tuzing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_tekshir_taminotchi_holati()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_holat VARCHAR(20);
BEGIN
    SELECT holat INTO v_holat
    FROM taminotchilar
    WHERE id = NEW.taminotchi_id;

    IF v_holat <> 'FAOL' THEN
        RAISE EXCEPTION 'Xatolik: Yetkazib beruvchi (ID: %) faol emas! Joriy holati: %',
            NEW.taminotchi_id, COALESCE(v_holat, 'TOPILMADI');
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_taminotchi_tekshiruv
BEFORE INSERT ON xaridlar
FOR EACH ROW
EXECUTE FUNCTION trg_tekshir_taminotchi_holati();

-- Test
INSERT INTO xaridlar(taminotchi_id, tovar_nomi, miqdor) 
VALUES (3, 'Ofis qog''ozi A4', 50);
```

## Tushuntirish va Mantiq:
Oddiy `FOREIGN KEY` faqat ID mavjudligini tekshiradi, lekin parent qatorning ichki statusi yoki qo'shimcha shartlarini tekshira olmaydi. Ushbu trigger orqali parent qatorning atributlari asosida qo'shimcha relyatsion yaxlitlik ta'minlanadi.

## Ishlash natijasi:
```text
INSERT 0 1
```


# 891-Topshiriq: TG_OP yordamida barcha DML amallarini bitta audit jadvaliga jamlovchi universal trigger
## Topshiriq sharti:
INSERT, UPDATE va DELETE amallarining har biri uchun nima o'zgarganini va kim tomonidan qachon bajarilganini bitta funksiyada qayd etuvchi to'liq audit yechimini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_universal_audit_logger()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_markaziy(jadval, amal, qator_id, eski_data, yangi_data)
        VALUES (TG_TABLE_NAME, TG_OP, NEW.id, NULL, to_jsonb(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_markaziy(jadval, amal, qator_id, eski_data, yangi_data)
        VALUES (TG_TABLE_NAME, TG_OP, NEW.id, to_jsonb(OLD), to_jsonb(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_markaziy(jadval, amal, qator_id, eski_data, yangi_data)
        VALUES (TG_TABLE_NAME, TG_OP, OLD.id, to_jsonb(OLD), NULL);
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$;

CREATE TRIGGER trg_mijozlar_toliq_audit
AFTER INSERT OR UPDATE OR DELETE ON mijozlar
FOR EACH ROW
EXECUTE FUNCTION trg_universal_audit_logger();

-- Test
INSERT INTO mijozlar(id, ism, email) VALUES (200, 'Zafar', 'zafar@misol.uz');
UPDATE mijozlar SET ism = 'Zafarbek' WHERE id = 200;
DELETE FROM mijozlar WHERE id = 200;

SELECT amal, qator_id, yangi_data->>'ism' AS ism FROM audit_markaziy WHERE qator_id = 200;
```

## Tushuntirish va Mantiq:
Bitta trigger ichida barcha 3 ta DML amalini boshqarish audit arxitekturasini soddalashtiradi va har bir amaliyot turi bo'yicha JSON formatidagi to'liq ma'lumotlar arxivini shakllantiradi.

## Ishlash natijasi:
```text
amal  | qator_id |   ism    
--------+----------+----------
 INSERT |      200 | Zafar
 UPDATE |      200 | Zafarbek
 DELETE |      200 | 
(3 rows)
```


# 892-Topshiriq: Tranzaksion hisoblar tarixida ketma-ketlik buzilmasligini (Sequence Continuity) tekshirish
## Topshiriq sharti:
Buxgalteriya provodkalari kiritilganda provodka raqami avvalgisidan aniq 1 taga katta bo'lishini (oralig'ida raqam tushib qolmasligini) ta'minlovchi BEFORE INSERT triggerini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_tekshir_provodka_uzluksizligi()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_oxirgi_raqam BIGINT;
BEGIN
    SELECT COALESCE(MAX(provodka_raqam), 0) INTO v_oxirgi_raqam
    FROM buxgalteriya_kitobi
    WHERE hisob_yili = NEW.hisob_yili;

    IF NEW.provodka_raqam <> v_oxirgi_raqam + 1 THEN
        RAISE EXCEPTION 'Uzluksizlik buzildi! Kutilayotgan raqam: %, Berildi: %',
            v_oxirgi_raqam + 1, NEW.provodka_raqam;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_uzluksiz_raqam_nazorati
BEFORE INSERT ON buxgalteriya_kitobi
FOR EACH ROW
EXECUTE FUNCTION trg_tekshir_provodka_uzluksizligi();

-- Test
INSERT INTO buxgalteriya_kitobi(hisob_yili, provodka_raqam, summa) VALUES (2024, 1, 500000);
INSERT INTO buxgalteriya_kitobi(hisob_yili, provodka_raqam, summa) VALUES (2024, 2, 350000);
```

## Tushuntirish va Mantiq:
Moliyaviy hisobotlarda hujjatlar raqamlarining uzluksiz ketma-ketligi (gapless numbering) qonuniy talab hisoblanadi. PostgreSQL `SEQUENCE` ob'ektlari rollback bo'lganda bo'shliq hosil qilishi mumkin, trigger esa qat'iy uzluksiz raqamlanishni nazorat qiladi.

## Ishlash natijasi:
```text
INSERT 0 1
INSERT 0 1
```


# 893-Topshiriq: Trigger orqali qatorning yaratilgan va yangilagan muallifini (Created By / Updated By) saqlash
## Topshiriq sharti:
Ilovadan kim kirgan bo'lishidan qat'i nazar, ma'lumotlar bazasi darajasida joriy sessiya foydalanuvchisini `yaratuvchi` va `oxirgi_tahrirlovchi` ustunlariga avtomatik muhrlovchi trigger tuzing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_mualliflik_audit()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        NEW.yaratuvchi := CURRENT_USER;
        NEW.yaratilgan_vaqt := NOW();
        NEW.oxirgi_tahrirlovchi := CURRENT_USER;
        NEW.yangilangan_vaqt := NOW();
    ELSIF TG_OP = 'UPDATE' THEN
        NEW.yaratuvchi := OLD.yaratuvchi; -- Yaratuvchini o'zgartirib bo'lmaydi
        NEW.yaratilgan_vaqt := OLD.yaratilgan_vaqt;
        NEW.oxirgi_tahrirlovchi := CURRENT_USER;
        NEW.yangilangan_vaqt := NOW();
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_kontraktlar_mualliflik
BEFORE INSERT OR UPDATE ON shartnomalar
FOR EACH ROW
EXECUTE FUNCTION trg_mualliflik_audit();

-- Test
INSERT INTO shartnomalar (id, raqam) VALUES (50, 'SH-2024/09');
SELECT id, raqam, yaratuvchi, oxirgi_tahrirlovchi FROM shartnomalar WHERE id = 50;
```

## Tushuntirish va Mantiq:
`CURRENT_USER` va `SESSION_USER` tizim konstantalari so'rovni yuborgan DB rolining nomini oladi. Trigger yaratuvchi maydoni UPDATE paytida o'zgarmasligini (`NEW.yaratuvchi := OLD.yaratuvchi;`) kafolatlaydi.

## Ishlash natijasi:
```text
id |   raqam    | yaratuvchi | oxirgi_tahrirlovchi 
----+------------+------------+---------------------
 50 | SH-2024/09 | postgres   | postgres
(1 row)
```


# 894-Topshiriq: Trigger orqali dinamik jadval bo'linishini (Legacy Partitioning) boshqarish
## Topshiriq sharti:
PostgreSQL 10 gacha bo'lgan an'anaviy usulda, sana bo'yicha kelgan buyurtmalarni mos oylik jadvallarga yo'naltiruvchi INSTEAD OF yoki BEFORE INSERT triggerini ko'rsating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_bolish_buyurtmalar_oylik()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF (NEW.sana >= '2024-01-01' AND NEW.sana < '2024-02-01') THEN
        INSERT INTO buyurtmalar_2024_01 VALUES (NEW.*);
    ELSIF (NEW.sana >= '2024-02-01' AND NEW.sana < '2024-03-01') THEN
        INSERT INTO buyurtmalar_2024_02 VALUES (NEW.*);
    ELSE
        INSERT INTO buyurtmalar_default VALUES (NEW.*);
    END IF;

    RETURN NULL; -- Asosiy master jadvalga yozmaslik uchun
END;
$$;

CREATE TRIGGER trg_dinamik_partitioning
BEFORE INSERT ON buyurtmalar_bosh
FOR EACH ROW
EXECUTE FUNCTION trg_bolish_buyurtmalar_oylik();

-- Test
INSERT INTO buyurtmalar_bosh(id, sana, summa) VALUES (1, '2024-01-15', 250000);
SELECT COUNT(*) FROM buyurtmalar_2024_01;
```

## Tushuntirish va Mantiq:
Zamonaviy Declarative Partitioning mavjud bo'lmagan davrlarda PostgreSQL'da jadvallarni bo'lish aynan triggerlar yordamida amalga oshirilgan. Trigger oylarni tahlil qilib bolalar jadvallariga (`partitions`) tarqatadi va `RETURN NULL` orqali master jadval bo'sh qolishini ta'minlaydi.

## Ishlash natijasi:
```text
count 
-------
     1
(1 row)
```


# 895-Topshiriq: Cheklangan qidiruv teglari (Tags count) sonini boshqarish
## Topshiriq sharti:
Maqolaga ko'pi bilan 10 ta teg biriktirilishi mumkinligini va bo'sh teglarni avtomatik tozalashni nazorat qiluvchi BEFORE UPDATE/INSERT triggerini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_tekshir_teglar_soni()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Bo'sh elementlarni tozalash
    NEW.teglar := ARRAY(
        SELECT DISTINCT TRIM(t) 
        FROM UNNEST(NEW.teglar) AS t 
        WHERE TRIM(t) <> ''
    );

    -- 10 tadan oshmasligini tekshirish
    IF CARDINALITY(NEW.teglar) > 10 THEN
        RAISE EXCEPTION 'Maqola uchun ko''pi bilan 10 ta teg ruxsat etiladi! Kiritildi: % ta',
            CARDINALITY(NEW.teglar);
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_maqola_teg_nazorat
BEFORE INSERT OR UPDATE OF teglar ON maqolalar
FOR EACH ROW
EXECUTE FUNCTION trg_tekshir_teglar_soni();

-- Test
INSERT INTO maqolalar(sarlavha, teglar) 
VALUES ('SQL Triggerlar', ARRAY['sql', 'postgresql', 'database', 'backend', 'performance']);

SELECT sarlavha, teglar FROM maqolalar WHERE sarlavha = 'SQL Triggerlar';
```

## Tushuntirish va Mantiq:
`CARDINALITY(array)` funksiyasi massivdagi elementlar sonini hisoblaydi. Trigger massiv ichidagi takroriy va bo'sh qiymatlarni tozalab, maksimal ruxsat etilgan chegaradan oshmasligini nazorat qiladi.

## Ishlash natijasi:
```text
sarlavha     |                   teglar                    
-----------------+---------------------------------------------
 SQL Triggerlar  | {backend,database,performance,postgresql,sql}
(1 row)
```


# 896-Topshiriq: Fayllar hajm kvotasini foydalanuvchi darajasida tekshirish
## Topshiriq sharti:
Foydalanuvchi yangi fayl yuklayotganda uning jami yuklagan fayllari hajmi 100 Megabaytdan oshib ketmasligini tekshiruvchi BEFORE INSERT triggerini yarating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_tekshir_disk_kvota()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_jami_bayt BIGINT;
    KVOTA_100MB CONSTANT BIGINT := 100 * 1024 * 1024; -- 104,857,600 bayt
BEGIN
    SELECT COALESCE(SUM(fayl_hajmi_bayt), 0) INTO v_jami_bayt
    FROM foydalanuvchi_fayllari
    WHERE foydalanuvchi_id = NEW.foydalanuvchi_id;

    IF (v_jami_bayt + NEW.fayl_hajmi_bayt) > KVOTA_100MB THEN
        RAISE EXCEPTION 'Disk kvotasi tugadi! Maksimal: 100 MB. Band: % bayt, Yangi fayl: % bayt',
            v_jami_bayt, NEW.fayl_hajmi_bayt;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_fayl_kvota_himoya
BEFORE INSERT ON foydalanuvchi_fayllari
FOR EACH ROW
EXECUTE FUNCTION trg_tekshir_disk_kvota();

-- Test
INSERT INTO foydalanuvchi_fayllari (foydalanuvchi_id, fayl_nomi, fayl_hajmi_bayt)
VALUES (1, 'arxiv.zip', 52428800);
```

## Tushuntirish va Mantiq:
Ushbu trigger saqlash joyi (storage) cheklovlarini to'g'ridan-to'g'ri relyatsion sathda himoyalaydi. Hatto backend dasturida kvota tekshiruvi aylanib o'tilgan taqdirda ham, ma'lumotlar bazasi ortiqcha hajm qabul qilishni rad etadi.

## Ishlash natijasi:
```text
INSERT 0 1
```


# 897-Topshiriq: Faqat bitta maydon o'zgarganda boshqa maydonni tozalash (Reset dependent fields)
## Topshiriq sharti:
Foydalanuvchi o'zining telefon raqamini o'zgartirganda, uning `telefon_tasdiqlangan` (is_verified) maydonini darhol `FALSE` qilib qo'yuvchi BEFORE UPDATE triggerini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_reset_tasdiq_telefon()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Agar telefon raqami yangilangan bo'lsa
    IF NEW.telefon IS DISTINCT FROM OLD.telefon THEN
        NEW.telefon_tasdiqlangan := FALSE;
        NEW.tasdiqlash_kodi := LPAD(FLOOR(RANDOM() * 1000000)::TEXT, 6, '0');
        NEW.kod_yuborilgan_vaqt := NOW();
        RAISE NOTICE 'Telefon raqam o''zgardi. Tasdiqlash holati bekor qilindi va yangi SMS kod hosil qilindi.';
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_kuzatuv_telefon_ozgarishi
BEFORE UPDATE OF telefon ON foydalanuvchilar
FOR EACH ROW
EXECUTE FUNCTION trg_reset_tasdiq_telefon();

-- Test
UPDATE foydalanuvchilar SET telefon = '+998901112244' WHERE id = 3;
```

## Tushuntirish va Mantiq:
`NEW.telefon IS DISTINCT FROM OLD.telefon` sharti orqali eski va yangi raqamning tengmasligi tekshiriladi. Telefon o'zgargani bilan uning avvalgi tasdiqlanganlik statusi xavfsizlik nuqtai nazaridan avtomatik ravishda bekor qilinadi.

## Ishlash natijasi:
```text
NOTICE:  Telefon raqam o'zgardi. Tasdiqlash holati bekor qilindi va yangi SMS kod hosil qilindi.
UPDATE 1
```


# 898-Topshiriq: Barcha triggerlarni ro'yxatini va ularning holatini tekshiruvchi ma'murlash so'rovi
## Topshiriq sharti:
Jadvallar kesimida qaysi triggerlar borligi, ularning hodisasi (INSERT, UPDATE, DELETE), darajasi (ROW / STATEMENT) va holatini ko'rsatuvchi tizim so'rovini yozing.

## Yechim (SQL kodi):
```sql
SELECT 
    event_object_table AS jadval_nomi,
    trigger_name AS trigger_nomi,
    action_timing AS vaqti,
    event_manipulation AS amal,
    action_orientation AS daraja
FROM information_schema.triggers
WHERE trigger_schema = 'public'
ORDER BY event_object_table, trigger_name;
```

## Tushuntirish va Mantiq:
`information_schema.triggers` standarti ma'lumotlar bazasidagi barcha triggerlar metama'lumotini ko'rsatadi: qaysi jadvalga tegishli, BEFORE yoki AFTER ekani, qaysi DML amallarini ushlashi va satr darajasidami yoki buyruq darajasidami ekanini taqdim etadi.

## Ishlash natijasi:
```text
jadval_nomi   |        trigger_nomi         | vaqti  | amal   |  daraja   
----------------+-----------------------------+--------+--------+-----------
 foydalanuvchilar| trg_foydalanuvchilar_vaqt   | BEFORE | UPDATE | ROW
 mahsulotlar    | trg_mahsulotlar_audit       | AFTER  | UPDATE | ROW
 mahsulotlar    | trg_mahsulotlar_audit       | AFTER  | DELETE | ROW
 xodimlar       | trg_statment_darajasi_log   | AFTER  | UPDATE | STATEMENT
(4 rows)
```


# 899-Topshiriq: Event Trigger: CREATE TABLE bo'lganda avtomatik standart ustunlarni tekshirish
## Topshiriq sharti:
Kompaniya standartlari bo'yicha har qanday yangi yaratilayotgan jadvalda `yaratilgan_vaqt` ustuni bo'lishini majburiy talab qiluvchi, aks holda jadval ochishni bekor qiluvchi Event Trigger yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION evt_tekshir_jadval_standartlari()
RETURNS EVENT_TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    obj RECORD;
    v_ustun_bor BOOLEAN;
BEGIN
    FOR obj IN SELECT * FROM pg_event_trigger_ddl_commands() WHERE object_type = 'table' LOOP
        -- Jadvalda 'yaratilgan_vaqt' ustuni mavjudligini tekshirish
        SELECT EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name = SUBSTRING(obj.object_identity FROM '[^.]+$')
              AND column_name = 'yaratilgan_vaqt'
        ) INTO v_ustun_bor;

        IF NOT v_ustun_bor THEN
            RAISE EXCEPTION 'Arxitektura standarti buzildi! Yangi jadvalda (%) majburiy "yaratilgan_vaqt" ustuni mavjud emas!',
                obj.object_identity;
        END IF;
    END LOOP;
END;
$$;

CREATE EVENT TRIGGER trg_jadval_standart_nazorati
ON ddl_command_end
WHEN TAG IN ('CREATE TABLE')
EXECUTE FUNCTION evt_tekshir_jadval_standartlari();

-- Test: Standartga mos bo'lmagan jadval yaratishga urinish
CREATE TABLE xato_jadval (id INT, ism TEXT);
```

## Tushuntirish va Mantiq:
`WHEN TAG IN ('CREATE TABLE')` bandi Event Triggerni faqat jadvallar yaratilayotganda ishga tushiradi. Bu butun tashkilot bo'ylab ma'lumotlar bazasi arxitektura standartlarini (masalan, audit ustunlari mavjudligi) avtomatik nazorat qilishda favqulodda kuchli quroldir.

## Ishlash natijasi:
```text
ERROR:  Arxitektura standarti buzildi! Yangi jadvalda (public.xato_jadval) majburiy "yaratilgan_vaqt" ustuni mavjud emas!
```


# 900-Topshiriq: Triggerlar bilan to'liq tranzaksion yaxlitlik: Keshbek hisoblash va hisobvaraq sinxronizatsiyasi
## Topshiriq sharti:
To'lov muvaffaqiyatli amalga oshirilganda (AFTER INSERT), to'lov summasining 2% miqdorida mijozning keshbek hisobiga mablag' o'tkazuvchi, to'lov tranzaksiyalari logini to'ldiruvchi va mijoz darajasini oshiruvchi yakuniy murakkab korporativ trigger tizimini yarating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION trg_tolov_yakuniy_avtomatlashtirish()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_keshbek_summa NUMERIC;
    v_jami_savdo NUMERIC;
BEGIN
    -- 1. Faqat muvaffaqiyatli to'lovlarga xizmat ko'rsatish
    IF NEW.holat = 'MUVAFFAQIN' THEN
        v_keshbek_summa := ROUND(NEW.summa * 0.02, 2);

        -- 2. Keshbek hisobini to'ldirish
        UPDATE keshbek_hamyonlar
        SET balans = balans + v_keshbek_summa,
            oxirgi_harakat = NOW()
        WHERE mijoz_id = NEW.mijoz_id;

        -- 3. Mijozning jami sarflagan summasini aniqlash
        SELECT COALESCE(SUM(summa), 0) INTO v_jami_savdo
        FROM tolovlar
        WHERE mijoz_id = NEW.mijoz_id AND holat = 'MUVAFFAQIN';

        -- 4. Agar umumiy savdo 50M dan oshsa VIP darajasiga ko'tarish
        IF v_jami_savdo >= 50000000 THEN
            UPDATE mijozlar
            SET daraja = 'VIP'
            WHERE id = NEW.mijoz_id AND daraja <> 'VIP';
            
            RAISE NOTICE 'Tabriklaymiz! Mijoz ID % VIP darajasiga kotarildi!', NEW.mijoz_id;
        END IF;

        RAISE NOTICE 'To''lov ID % uchun % so''m keshbek muvaffaqiyatli hisoblandi.', 
            NEW.id, v_keshbek_summa;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_tolov_toza_yakun
AFTER INSERT ON tolovlar
FOR EACH ROW
EXECUTE FUNCTION trg_tolov_yakuniy_avtomatlashtirish();

-- Test
INSERT INTO tolovlar (id, mijoz_id, summa, holat)
VALUES (1055, 12, 1000000.00, 'MUVAFFAQIN');
```

## Tushuntirish va Mantiq:
Ushbu yakuniy trigger korporativ fintex tizimlarining markaziy avtomatlashtirish jarayonini o'zida aks ettiradi: bitta to'lov orqali keshbek hisoblanadi, umumiy statistika yangilanadi va mijozning sodiqlik dasturidagi toifasi avtomatik tarzda yangilanadi.

## Ishlash natijasi:
```text
NOTICE:  To'lov ID 1055 uchun 20000.00 so'm keshbek muvaffaqiyatli hisoblandi.
INSERT 0 1
```

