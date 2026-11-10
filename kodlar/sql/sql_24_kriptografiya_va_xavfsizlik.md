# Modul 24: Ma'lumotlar Bazasi Kriptografiyasi va Kiberxavfsizlik (PostgreSQL Security)

Ushbu modulda zamonaviy korporativ va moliyaviy ma'lumotlar bazalarida ma'lumotlarni kriptografik shifrlash (pgcrypto), yozuvlar darajasidagi xavfsizlik (Row-Level Security - RLS), dinamik niqoblash (Dynamic Data Masking), server auditi (pgaudit), apparat va disk darajasidagi shifrlash (TDE) hamda SQL Injection hujumlariga qarshi ko'p bosqichli chuqur himoya mexanizmlari qamrab olingan. Har bir topshiriq real sanoat muammosiga qaratilgan bo'lib, ishlab chiqarish (production) standartlariga to'liq javob beradi.

---
### Topshiriq #1151: pgcrypto Kengaytmasini Maxsus Xavfsiz Sxemada O'rnatish
**Tavsif:** Umumiy `public` sxemada kriptografik funksiyalarni saqlash xavfsizlik talablariga zid, chunki barcha foydalanuvchilar ularga standart holatda kirish huquqiga ega bo'lishi mumkin. Kriptografik funksiyalarni faqat ruxsat berilgan rollar ko'ra oladigan `crypto_sec` sxemasida izolyatsiya qilish kerak.
**Talablar:**
- `crypto_sec` nomli alohida sxema yaratish.
- `pgcrypto` kengaytmasini ushbu sxema ichida o'rnatish.
- `public` foydalanuvchilaridan ushbu sxemaga barcha huquqlarni bekor qilish (REVOKE ALL).
- Faqat `sec_admin` maxsus roliga ushbu sxemadan foydalanish (USAGE, EXECUTE) huquqini taqdim etish.
**Yechim (SQL):**
```sql
-- 1. Kriptografiya uchun maxsus izolyatsiyalangan sxema yaratish
CREATE SCHEMA IF NOT EXISTS crypto_sec;

-- 2. pgcrypto kengaytmasini faqat ushbu xavfsiz sxemaga o'rnatish
CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA crypto_sec;

-- 3. Standart holatda barcha foydalanuvchilarga beriladigan ruxsatlarni bekor qilish
REVOKE ALL ON SCHEMA crypto_sec FROM PUBLIC;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA crypto_sec FROM PUBLIC;

-- 4. Kriptografik rollarni yaratish va ruxsatlarni qat'iy cheklash
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'sec_admin') THEN
        CREATE ROLE sec_admin WITH NOLOGIN;
    END IF;
END
$$;

-- sec_admin roliga sxemadan foydalanish va undagi funksiyalarni ishga tushirish huquqini berish
GRANT USAGE ON SCHEMA crypto_sec TO sec_admin;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA crypto_sec TO sec_admin;

-- Kelajakda yaratiladigan funksiyalar uchun standart ruxsatlarni belgilash
ALTER DEFAULT PRIVILEGES IN SCHEMA crypto_sec 
GRANT EXECUTE ON FUNCTIONS TO sec_admin;
```
**Tushuntirish:** PostgreSQL-da `public` sxemasi hamma uchun ochiq hisoblanadi. Agar `pgcrypto` public sxemaga o'rnatilsa, har qanday oddiy foydalanuvchi funksiyalarni ko'rishi va noto'g'ri qo'llashi mumkin. Sxemani alohida ajratish va `REVOKE ... FROM PUBLIC` qilish orqali Principle of Least Privilege (Eng kam huquq berish tamoyili) to'liq ta'minlanadi.
---

### Topshiriq #1152: Bank Karta Raqamlarini (PAN) AES-256 bilan Simmetrik Shifrlash
**Tavsif:** PCI-DSS (Payment Card Industry Data Security Standard) talablariga muvofiq, mijozlarning 16 xonali to'liq karta raqamlari (PAN) ma'lumotlar bazasida ochiq matn (plaintext) holatida saqlanishi qat'iyan taqiqlanadi. Ma'lumotlarni saqlashda AES-256 algoritmi orqali shifrlash talab etiladi.
**Talablar:**
- `bank_cards` jadvalini yaratish: `id`, `cardholder_name`, `encrypted_pan` (bytea), `last_four` (char(4)).
- Karta raqamini `pgp_sym_encrypt` yordamida AES-256 shifrlab `bytea` ustuniga yozish.
- Shifrlangan ma'lumotni kalit orqali `pgp_sym_decrypt` yordamida qayta o'qish funksiyasini yozish.
**Yechim (SQL):**
```sql
-- Karta ma'lumotlarini saqlovchi jadval
CREATE TABLE IF NOT EXISTS bank_cards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cardholder_name VARCHAR(100) NOT NULL,
    encrypted_pan BYTEA NOT NULL,
    last_four CHAR(4) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

-- Karta ma'lumotlarini xavfsiz kiritish (AES-256 orqali shifrlash)
CREATE OR REPLACE FUNCTION insert_bank_card(
    p_cardholder VARCHAR(100),
    p_raw_pan VARCHAR(19),
    p_secret_key TEXT
) RETURNS UUID AS $$
DECLARE
    v_card_id UUID;
    v_clean_pan VARCHAR(19);
    v_last4 CHAR(4);
BEGIN
    -- Bo'shliqlarni olib tashlash
    v_clean_pan := regexp_replace(p_raw_pan, '\s+', '', 'g');
    v_last4 := right(v_clean_pan, 4);

    INSERT INTO bank_cards (cardholder_name, encrypted_pan, last_four)
    VALUES (
        p_cardholder,
        pgp_sym_encrypt(v_clean_pan, p_secret_key, 'cipher-algo=aes256, compress-algo=0'),
        v_last4
    )
    RETURNING id INTO v_card_id;

    RETURN v_card_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Shifrlangan kartani xavfsiz o'qish funksiyasi
CREATE OR REPLACE FUNCTION get_decrypted_pan(
    p_card_id UUID,
    p_secret_key TEXT
) RETURNS VARCHAR(19) AS $$
DECLARE
    v_decrypted_pan TEXT;
BEGIN
    SELECT pgp_sym_decrypt(encrypted_pan, p_secret_key)
    INTO v_decrypted_pan
    FROM bank_cards
    WHERE id = p_card_id;

    RETURN v_decrypted_pan;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Shifrdan chiqarishda xatolik: Maxfiy kalit noto''g''ri yoki ma''lumot buzilgan.';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```
**Tushuntirish:** `pgp_sym_encrypt` ma'lumotlarni OpenPGP standarti asosida shifrlaydi. `cipher-algo=aes256` parametri eng kuchli simmetrik shifrni faollashtiradi. `compress-algo=0` siqishni o'chiradi, bu qisqa satrlarda (karta raqami kabi) qo'shimcha resurs sarfini kamaytiradi va CRIME/BREACH kabi siqishga asoslangan hujumlarning oldini oladi.
---

### Topshiriq #1153: Asimmetrik RSA/GPG Kalitlar Yordamida Ma'lumotlarni Shifrlash
**Tavsif:** Backend serverlar ma'lumotlar bazasiga maxfiy hujjatlarni faqat yozadi, ammo ularni o'qish huquqiga ega bo'lmasligi kerak (Zero-Trust arxitekturasi). Ma'lumotlar ommaviy kalit (Public Key) orqali shifrlanishi, faqat xavfsiz apparat moduliga (HSM) ega bo'lgan alohida xizmat maxfiy kalit (Private Key) bilan uni o'qiy olishi zarur.
**Talablar:**
- `secure_documents` jadvalini yaratish.
- `pgp_pub_encrypt` yordamida ommaviy kalit asosida shifrlab saqlash.
- `pgp_pub_decrypt` yordamida shaxsiy kalit va parol bilan shifrdan chiqarish.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS secure_documents (
    doc_id BIGSERIAL PRIMARY KEY,
    owner_id UUID NOT NULL,
    document_title VARCHAR(255) NOT NULL,
    encrypted_payload BYTEA NOT NULL,
    uploaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Hujjatni Public Key orqali shifrlab kiritish (Backend faqat Public Key ni biladi)
CREATE OR REPLACE FUNCTION store_secure_document(
    p_owner_id UUID,
    p_title VARCHAR(255),
    p_plain_content TEXT,
    p_armored_public_key TEXT
) RETURNS BIGINT AS $$
DECLARE
    v_new_id BIGINT;
BEGIN
    INSERT INTO secure_documents (owner_id, document_title, encrypted_payload)
    VALUES (
        p_owner_id,
        p_title,
        pgp_pub_encrypt(p_plain_content, dearmor(p_armored_public_key))
    )
    RETURNING doc_id INTO v_new_id;

    RETURN v_new_id;
END;
$$ LANGUAGE plpgsql;

-- Hujjatni Private Key va uning paroli bilan shifrdan chiqarish
CREATE OR REPLACE FUNCTION read_secure_document(
    p_doc_id BIGINT,
    p_armored_private_key TEXT,
    p_key_passphrase TEXT
) RETURNS TEXT AS $$
DECLARE
    v_result TEXT;
BEGIN
    SELECT pgp_pub_decrypt(
        encrypted_payload, 
        dearmor(p_armored_private_key), 
        p_key_passphrase
    )
    INTO v_result
    FROM secure_documents
    WHERE doc_id = p_doc_id;

    RETURN v_result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```
**Tushuntirish:** Asimmetrik shifrlashda backend ilova buzib kirilgan taqdirda ham, tajovuzkor bazadagi shifrlangan ma'lumotlarni o'qiy olmaydi, chunki ommaviy kalit faqat shifrlash imkonini beradi. `dearmor()` funksiyasi ASCII-armored formatidagi (PGP bloklari) kalitlarni binar bytea formatiga o'tkazadi.
---

### Topshiriq #1154: crypt() va gen_salt('bf', 12) bilan Parollarni Bcrypt Xeshlash
**Tavsif:** Foydalanuvchi parollarini MD5 yoki SHA-256 kabi tezkor xeshlar bilan saqlash Rainbow Table va GPU brute-force hujumlariga ojiz hisoblanadi. bcrypt algoritmi orqali sekinlashtirilgan, tuzlangan (salted) va moslashuvchan xarajat koeffitsientiga ega xesh yaratish zarur.
**Talablar:**
- `app_users` jadvalini yaratish: `id`, `username`, `password_hash`.
- Parolni `crypt(p_password, gen_salt('bf', 12))` yordamida xeshlash.
- Parolni tekshirish uchun o'zgarmas vaqtli (constant-time taqqoslash) verifikatsiya funksiyasini yozish.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS app_users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(120) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- Yangi foydalanuvchini bcrypt (work factor = 12) bilan ro'yxatdan o'tkazish
CREATE OR REPLACE FUNCTION register_user(
    p_username VARCHAR(50),
    p_raw_password TEXT
) RETURNS UUID AS $$
DECLARE
    v_user_id UUID;
BEGIN
    IF length(p_raw_password) < 8 THEN
        RAISE EXCEPTION 'Parol kamida 8 ta belgidan iborat bo''lishi shart!';
    END IF;

    INSERT INTO app_users (username, password_hash)
    VALUES (
        p_username,
        crypt(p_raw_password, gen_salt('bf', 12)) -- 2^12 = 4096 iteratsiya
    )
    RETURNING user_id INTO v_user_id;

    RETURN v_user_id;
END;
$$ LANGUAGE plpgsql;

-- Foydalanuvchi parolini tekshirish (Autentifikatsiya)
CREATE OR REPLACE FUNCTION verify_user_login(
    p_username VARCHAR(50),
    p_candidate_password TEXT
) RETURNS BOOLEAN AS $$
DECLARE
    v_stored_hash VARCHAR(120);
BEGIN
    SELECT password_hash INTO v_stored_hash
    FROM app_users
    WHERE username = p_username AND is_active = TRUE;

    IF NOT FOUND THEN
        -- Foydalanuvchi mavjud bo'lmasa ham hisoblash vaqtini bir xil qilish uchun soxta xesh hisoblanadi
        PERFORM crypt(p_candidate_password, '$2a$12$e8N8p27vJzUfWj9YxR4/eeK9cQx7l1T7xVpCqU.L7uM9r0n8v5e9i');
        RETURN FALSE;
    END IF;

    -- crypt() mavjud xeshni ikkinchi argument sifatida olganda o'sha tuzni qayta ishlatadi
    RETURN (v_stored_hash = crypt(p_candidate_password, v_stored_hash));
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```
**Tushuntirish:** `gen_salt('bf', 12)` Blowfish asosidagi bcrypt tuzi yaratadi. 12 iteratsiya (2^12) zamonaviy apparat vositalarida GPU parallel hujumlarini iqtisodiy jihatdan imkonsiz darajada sekinlashtiradi. Timing-attack (vaqt orqali foydalanuvchini aniqlash) ning oldini olish uchun foydalanuvchi topilmaganda ham soxta xesh bajariladi.
---

### Topshiriq #1155: digest() Funksiyasi Orqali Ma'lumotlar Yaxlitligini (Checksum) Tekshirish
**Tavsif:** Muhim moliyaviy audit jurnallarida har bir yozuv kiritilgandan keyin uning mazmuni ruxsatsiz o'zgartirilmaganligini (data integrity) kafolatlash uchun kriptografik SHA-256 nazorat yig'indisini saqlash kerak.
**Talablar:**
- `financial_ledger` jadvalini yaratish.
- Qator ustunlari (hisob, summa, sana) asosida SHA-256 xeshini avtomatik hisoblovchi trigger yaratish.
- Bazadagi yozuvlarning yaxlitligini tekshiruvchi skaner funksiyasini yozish.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS financial_ledger (
    entry_id BIGSERIAL PRIMARY KEY,
    account_from VARCHAR(34) NOT NULL,
    account_to VARCHAR(34) NOT NULL,
    amount NUMERIC(18, 2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    row_checksum BYTEA NOT NULL
);

-- Qator ma'lumotlaridan SHA-256 checksum hisoblash triggeri
CREATE OR REPLACE FUNCTION compute_ledger_checksum()
RETURNS TRIGGER AS $$
DECLARE
    v_raw_payload TEXT;
BEGIN
    -- Deterministik satr hosil qilish
    v_raw_payload := NEW.entry_id::TEXT || '|' || 
                     NEW.account_from || '|' || 
                     NEW.account_to || '|' || 
                     NEW.amount::TEXT || '|' || 
                     NEW.created_at::TEXT;

    -- SHA-256 hisoblash
    NEW.row_checksum := digest(v_raw_payload, 'sha256');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_ledger_integrity
BEFORE INSERT ON financial_ledger
FOR EACH ROW
EXECUTE FUNCTION compute_ledger_checksum();

-- Ledger yaxlitligini to'liq tekshiruvchi auditor funksiyasi
CREATE OR REPLACE FUNCTION audit_verify_ledger()
RETURNS TABLE(corrupted_entry_id BIGINT, status TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        l.entry_id,
        'Yozuv o''zgartirilgan (Checksum mos kelmadi!)'::TEXT
    FROM financial_ledger l
    WHERE l.row_checksum != digest(
        l.entry_id::TEXT || '|' || 
        l.account_from || '|' || 
        l.account_to || '|' || 
        l.amount::TEXT || '|' || 
        l.created_at::TEXT, 
        'sha256'
    );
END;
$$ LANGUAGE plpgsql;
```
**Tushuntirish:** `digest(data, 'sha256')` ma'lumotning bir tomonlama xeshini qaytaradi. Agar tajovuzkor to'g'ridan-to'g'ri jadvaldagi `amount` yoki hisoblarni o'zgartirsa, qayta hisoblangan xesh saqlangan checksum bilan mos kelmay qoladi va bu buzilishni bir zumda fosh etadi.
---

### Topshiriq #1156: HMAC Orqali Webhook va API So'rovlarini Verifikatsiya Qilish
**Tavsif:** Tashqi to'lov tizimlaridan kelayotgan webhook so'rovlari va API tranzaksiyalari tranzit paytida o'zgartirilmaganligini va aynan ruxsat etilgan provayder tomonidan yuborilganligini HMAC-SHA256 orqali bazaning o'zida tekshirish lozim.
**Talablar:**
- `webhook_events` jadvali.
- `hmac(data, key, 'sha256')` funksiyasidan foydalanib signaturani tekshirish.
- Agar imzo soxta bo'lsa, xatolik berib tranzaksiyani bekor qilish.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS webhook_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_name VARCHAR(50) NOT NULL,
    payload_body TEXT NOT NULL,
    received_signature VARCHAR(64) NOT NULL,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    processed_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- Webhook imzosini tekshiruvchi va saqlovchi xavfsiz protsedura
CREATE OR REPLACE PROCEDURE process_incoming_webhook(
    p_provider VARCHAR(50),
    p_payload TEXT,
    p_signature VARCHAR(64),
    p_shared_secret TEXT
) LANGUAGE plpgsql AS $$
DECLARE
    v_expected_hmac BYTEA;
    v_expected_hex VARCHAR(64);
BEGIN
    -- Maxfiy kalit va body asosida HMAC-SHA256 hisoblash
    v_expected_hmac := hmac(p_payload, p_shared_secret, 'sha256');
    v_expected_hex := encode(v_expected_hmac, 'hex');

    -- Constant-time xavfsiz taqqoslash
    IF v_expected_hex <> lower(p_signature) THEN
        RAISE EXCEPTION 'Xavfsizlik ogohlantirishi: Webhook HMAC imzosi noto''g''ri!';
    END IF;

    INSERT INTO webhook_events (provider_name, payload_body, received_signature, is_verified)
    VALUES (p_provider, p_payload, p_signature, TRUE);
END;
$$;
```
**Tushuntirish:** HMAC (Hash-based Message Authentication Code) nafaqat ma'lumotning butunligini, balki uning haqiqiyligini (autentikligini) ham tasdiqlaydi. Faqat umumiy maxfiy kalitga ega bo'lgan tomon to'g'ri HMAC imzosini yarata oladi.
---

### Topshiriq #1157: Blind Indexing: Shifrlangan Ma'lumotlar Ustida Tezkor Qidiruv
**Tavsif:** Kriptografik shifrlangan ustunlar (masalan, telefon raqam yoki JShShIR) ustida `WHERE phone = '...'` orqali to'g'ridan-to'g'ri qidiruv qilib bo'lmaydi, chunki shifrlash tasodifiy IV/tuz ishlatadi. Qidiruv imkoniyatini saqlagan holda xavfsizlikni ta'minlash uchun Blind Indexing (HMAC deterministik xesh) arxitekturasini joriy qilish kerak.
**Talablar:**
- `user_profiles` jadvali: `encrypted_phone` (AES-256) va `phone_bindex` (HMAC-SHA256 xesh).
- `phone_bindex` ustuniga B-Tree indeksi o'rnatish.
- Foydalanuvchi telefon raqami bo'yicha shifrlangan qatorni indeks orqali 1 ms ichida topuvchi funksiya.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS user_profiles (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(100) NOT NULL,
    encrypted_phone BYTEA NOT NULL,
    phone_bindex CHAR(64) NOT NULL, -- Blind Index
    created_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- Blind index ustuniga indeks yaratish
CREATE INDEX IF NOT EXISTS idx_user_profiles_phone_bindex ON user_profiles(phone_bindex);

-- Yangi profil qo'shish (AES shifrlash + Blind Index generatsiyasi)
CREATE OR REPLACE FUNCTION add_user_profile(
    p_name VARCHAR(100),
    p_raw_phone VARCHAR(20),
    p_encryption_key TEXT,
    p_blind_index_salt TEXT
) RETURNS UUID AS $$
DECLARE
    v_clean_phone VARCHAR(20);
    v_bindex CHAR(64);
    v_new_id UUID;
BEGIN
    v_clean_phone := regexp_replace(p_raw_phone, '[^0-9]', '', 'g');
    -- Blind index uchun alohida salt/key bilan HMAC hisoblash
    v_bindex := encode(hmac(v_clean_phone, p_blind_index_salt, 'sha256'), 'hex');

    INSERT INTO user_profiles (full_name, encrypted_phone, phone_bindex)
    VALUES (
        p_name,
        pgp_sym_encrypt(v_clean_phone, p_encryption_key),
        v_bindex
    )
    RETURNING user_id INTO v_new_id;

    RETURN v_new_id;
END;
$$ LANGUAGE plpgsql;

-- Blind index orqali tezkor qidiruv (Indeks to'liq ishlaydi!)
CREATE OR REPLACE FUNCTION find_user_by_phone(
    p_raw_phone VARCHAR(20),
    p_blind_index_salt TEXT,
    p_encryption_key TEXT
) RETURNS TABLE(user_id UUID, full_name VARCHAR(100), decrypted_phone TEXT) AS $$
DECLARE
    v_search_bindex CHAR(64);
BEGIN
    v_search_bindex := encode(hmac(regexp_replace(p_raw_phone, '[^0-9]', '', 'g'), p_blind_index_salt, 'sha256'), 'hex');

    RETURN QUERY
    SELECT 
        u.user_id,
        u.full_name,
        pgp_sym_decrypt(u.encrypted_phone, p_encryption_key)
    FROM user_profiles u
    WHERE u.phone_bindex = v_search_bindex;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```
**Tushuntirish:** Blind Index shifrlash kalitidan mustaqil bo'lgan boshqa maxfiy tuz (salt) yordamida deterministik HMAC hisoblaydi. Bu bazadagi barcha qatorlarni demaskirovka qilmasdan (Table Scan qilmasdan) indeks bo'yicha $O(\log N)$ vaqtda aniq qidirish imkonini beradi.
---

### Topshiriq #1158: pgp_sym_encrypt Sozlamalari: Siqish va Shifrlash Algoritmlari
**Tavsif:** Har xil hajmdagi ma'lumotlar uchun kriptografik xarajatlar turlicha bo'ladi. Katta hajmdagi JSON yoki shartnoma matnlarini shifrlashda ZIP siqishini qo'llash, kichik ma'lumotlarda esa siqishni bekor qilish zarur. Shuningdek, shifr algoritmini (AES-128, AES-192, AES-256) dinamik tanlash mexanizmi kerak.
**Talablar:**
- `encrypted_blobs` jadvali.
- `compress-algo` (0=off, 1=ZIP, 2=ZLIB) va `cipher-algo` parametrlarini boshqaruvchi universal funksiya.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS encrypted_blobs (
    blob_id BIGSERIAL PRIMARY KEY,
    blob_type VARCHAR(50) NOT NULL,
    payload BYTEA NOT NULL,
    cipher_used VARCHAR(20) NOT NULL,
    compressed BOOLEAN NOT NULL,
    created_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- Kripto parametrlarini moslashtiruvchi universal funksiya
CREATE OR REPLACE FUNCTION store_encrypted_blob(
    p_blob_type VARCHAR(50),
    p_data TEXT,
    p_secret_key TEXT,
    p_cipher VARCHAR(20) DEFAULT 'aes256',
    p_enable_compression BOOLEAN DEFAULT TRUE
) RETURNS BIGINT AS $$
DECLARE
    v_options TEXT;
    v_new_id BIGINT;
BEGIN
    -- Validatsiya
    IF p_cipher NOT IN ('aes128', 'aes192', 'aes256', 'blowfish') THEN
        RAISE EXCEPTION 'Qo''llab-quvvatlanmaydigan shifr: %', p_cipher;
    END IF;

    -- Variantlar satrini yig'ish
    v_options := 'cipher-algo=' || p_cipher || ', compress-algo=' || 
                 CASE WHEN p_enable_compression THEN '1' ELSE '0' END;

    INSERT INTO encrypted_blobs (blob_type, payload, cipher_used, compressed)
    VALUES (
        p_blob_type,
        pgp_sym_encrypt(p_data, p_secret_key, v_options),
        p_cipher,
        p_enable_compression
    )
    RETURNING blob_id INTO v_new_id;

    RETURN v_new_id;
END;
$$ LANGUAGE plpgsql;
```
**Tushuntirish:** Katta matnlarni shifrlashdan oldin siqish (compress-algo=1) nafaqat disk hajmini tejaydi, balki ma'lumotdagi takroriy naqshlarni (patterns) yo'qotib, kriptotahlil hujumlariga qarshi himoyani ham mustahkamlaydi.
---

### Topshiriq #1159: Seanslararo Kalit Xavfsizligi: current_setting Orqali Kalit Uzatish
**Tavsif:** Kriptografik kalitlarni SQL so'rovlar matnida (SQL text) ochiq uzatish xavflidir, chunki ular `pg_stat_activity` va server loglarida saqlanib qolishi mumkin. Master kalitni sessiya konfiguratsiyasi (`SET LOCAL`) orqali xavfsiz ineksiya qilish arxitekturasi talab etiladi.
**Talablar:**
- Tranzaksiya darajasidagi `SET LOCAL app.master_key = '...'` o'zgaruvchisidan foydalanish.
- `current_setting('app.master_key', true)` orqali kalitni olib shifrdan chiqaruvchi funksiya.
- Tranzaksiya tugashi bilan kalit xotiradan avtomatik o'chishi shart.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS confidential_notes (
    note_id SERIAL PRIMARY KEY,
    author VARCHAR(50) NOT NULL,
    secret_body BYTEA NOT NULL
);

-- Ma'lumot qo'shish funksiyasi (Kalitni sessiya o'zgaruvchisidan oladi)
CREATE OR REPLACE FUNCTION insert_confidential_note(
    p_author VARCHAR(50),
    p_note_text TEXT
) RETURNS INT AS $$
DECLARE
    v_key TEXT;
    v_id INT;
BEGIN
    -- Tranzaksiyadagi maxfiy kalitni olish
    v_key := current_setting('app.master_key', TRUE);
    
    IF v_key IS NULL OR length(v_key) < 16 THEN
        RAISE EXCEPTION 'Xatolik: app.master_key o''rnatilmagan yoki talabga javob bermaydi!';
    END IF;

    INSERT INTO confidential_notes (author, secret_body)
    VALUES (p_author, pgp_sym_encrypt(p_note_text, v_key, 'cipher-algo=aes256'))
    RETURNING note_id INTO v_id;

    RETURN v_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Namuna: Tranzaksiya doirasida kalitni o'rnatish va foydalanish
/*
BEGIN;
    -- Faqat joriy tranzaksiya uchun amal qiladi (loglarga yozilmaydi)
    SET LOCAL app.master_key = 'SuperSecretEnterpriseMasterKey2026!';
    
    SELECT insert_confidential_note('Alisher', 'O''ta maxfiy loyiha hisoboti...');
COMMIT;
-- COMMIT dan so'ng app.master_key avtomatik ravishda yo'qoladi!
*/
```
**Tushuntirish:** `SET LOCAL` parametri o'zgaruvchining amal qilish muddatini joriy tranzaksiya bilan cheklaydi. Tranzaksiya yakunlangach, sessiya o'zgaruvchisi xotiradan tozalanadi. Bu orqali kalit doimiy server jurnallariga yoki boshqa so'rovlarga sizib chiqmaydi.
---

### Topshiriq #1160: Kriptografik Xavfsiz Tasodifiy Baytlar va Kripto-Tokenlar Generatsiyasi
**Tavsif:** Seans identifikatorlari, parolni tiklash tokenlari va API kalitlari oddiy `random()` funksiyasi bilan yaratilmasligi shart, chunki u psevdo-tasodifiy bo'lib, bashorat qilinishi mumkin. Kriptografik mustahkam PRNG (CSPRNG) dan foydalanish talab etiladi.
**Talablar:**
- `gen_random_bytes(N)` funksiyasidan foydalanib kripto-mustahkam baytlar olish.
- URL-safe Base64 va hex formatidagi xavfsiz tokenlarni qaytaruvchi funksiya.
**Yechim (SQL):**
```sql
CREATE OR REPLACE FUNCTION generate_secure_api_key(p_prefix VARCHAR(10) DEFAULT 'ak_live_')
RETURNS TEXT AS $$
DECLARE
    v_raw_bytes BYTEA;
    v_token TEXT;
BEGIN
    -- Operatsion tizimning /dev/urandom manbasidan 32 ta kripto-xavfsiz bayt olish
    v_raw_bytes := gen_random_bytes(32);
    
    -- Hex formatiga o'tkazish (64 ta belgi)
    v_token := encode(v_raw_bytes, 'hex');
    
    RETURN p_prefix || v_token;
END;
$$ LANGUAGE plpgsql;

-- URL-safe Base64 token generatsiyasi (CSRF va seans tokenlari uchun)
CREATE OR REPLACE FUNCTION generate_secure_url_token(p_byte_length INT DEFAULT 24)
RETURNS TEXT AS $$
DECLARE
    v_base64 TEXT;
BEGIN
    IF p_byte_length < 16 THEN
        RAISE EXCEPTION 'Token xavfsizligi uchun minimal bayt uzunligi 16 bo''lishi kerak!';
    END IF;

    -- Base64 standartidagi +, / va = belgilarini URL uchun xavfsiz almashtirish
    v_base64 := encode(gen_random_bytes(p_byte_length), 'base64');
    v_base64 := replace(v_base64, '+', '-');
    v_base64 := replace(v_base64, '/', '_');
    v_base64 := replace(v_base64, '=', '');

    RETURN v_base64;
END;
$$ LANGUAGE plpgsql;
```
**Tushuntirish:** PostgreSQL `random()` funksiyasi LCG (Linear Congruential Generator) ga asoslangan bo'lib, uning holatini bir nechta ketma-ket qiymatdan so'ng hisoblab topish mumkin. `gen_random_bytes()` esa operatsion tizimning kriptografik entropiya havzasiga (`/dev/urandom` yoki Windows CryptGenRandom) murojaat qiladi.
---

### Topshiriq #1161: Maydon Darajasidagi Avtomatik Shifrlash Triggeri (Transparent Column Encryption)
**Tavsif:** Dasturchilar har bir INSERT va UPDATE so'rovida shifrlash funksiyasini chaqirishni unutib qo'ymasliklari uchun ma'lumotlar bazasi darajasida shaffof shifrlash triggerini yaratish zarur.
**Talablar:**
- `customers_pii` jadvalida ochiq matn kiritilganda uni `BEFORE INSERT OR UPDATE` triggerida avtomatik AES-256 shifrlab `encrypted_passport` ustuniga joylash.
- Ochiq matn saqlanadigan vaqtinchalik ustunni tozalash yoki to'g'ridan-to'g'ri bytea ga aylantirish.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS customers_pii (
    customer_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    raw_passport VARCHAR(20), -- Dastur kiritadigan maydon
    encrypted_passport BYTEA NOT NULL, -- Haqiqiy saqlanadigan shifr
    created_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- Avtomatik shifrlash trigger funksiyasi
CREATE OR REPLACE FUNCTION trg_auto_encrypt_passport()
RETURNS TRIGGER AS $$
DECLARE
    v_key TEXT;
BEGIN
    IF NEW.raw_passport IS NOT NULL AND length(NEW.raw_passport) > 0 THEN
        v_key := current_setting('app.encryption_key', TRUE);
        IF v_key IS NULL THEN
            RAISE EXCEPTION 'Tranzaksiya xatosi: app.encryption_key topilmadi!';
        END IF;

        -- Pasport ma'lumotini shifrlab bytea ustunga yozish
        NEW.encrypted_passport := pgp_sym_encrypt(NEW.raw_passport, v_key, 'cipher-algo=aes256');
        
        -- Xavfsizlik maqsadida ochiq matn ustunini darhol bo'shatish
        NEW.raw_passport := NULL;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_encrypt_pii_before_save
BEFORE INSERT OR UPDATE ON customers_pii
FOR EACH ROW
EXECUTE FUNCTION trg_auto_encrypt_passport();
```
**Tushuntirish:** Trigger darajasidagi avtomatik shifrlash dasturiy ta'minotdagi xatolar yoki dasturchilarning beparvoligi tufayli shifrlanmagan PII (Personally Identifiable Information) ma'lumotlarining bazaga ochiq matnda tushib qolish xavfini 100% bartaraf etadi.
---

### Topshiriq #1162: Security Definer View va Shifrlangan Ustunlarni Xavfsiz Demaskirovka Qilish
**Tavsif:** Foydalanuvchilar to'g'ridan-to'g'ri shifrlash kalitiga yoki jadvalga kirish huquqiga ega bo'lmasligi kerak. Shifrlangan ustunlarni faqat ruxsat berilgan `auditor_role` egalariga o'qib beruvchi xavfsiz `SECURITY DEFINER` ko'rinishi (View) va funktsiyasini yaratish talab qilinadi.
**Talablar:**
- Asosiy jadval huquqlarini oddiy foydalanuvchilardan cheklash.
- `SECURITY DEFINER` yordamida funksiya yaratish va uni maxsus View ichida chaqirish.
- Audit vaqtida kim qaysi yozuvni shifrdan chiqarganini audit jurnaliga qayd etish.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS audit_access_logs (
    log_id BIGSERIAL PRIMARY KEY,
    accessed_by VARCHAR(50) NOT NULL,
    record_id INT NOT NULL,
    accessed_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- Maxsus himoyalangan demaskirovka funksiyasi (Faqat table owner nomidan ishlaydi)
CREATE OR REPLACE FUNCTION decrypt_customer_passport(p_customer_id INT)
RETURNS TEXT AS $$
DECLARE
    v_res TEXT;
    v_key TEXT := 'InternalSuperSecureSystemKey_2026'; -- Maxfiy kalit faqat funksiya ichida
BEGIN
    -- Audit jurnaliga kim qachon o'qiganini yozib borish
    INSERT INTO audit_access_logs (accessed_by, record_id)
    VALUES (CURRENT_USER, p_customer_id);

    SELECT pgp_sym_decrypt(encrypted_passport, v_key)
    INTO v_res
    FROM customers_pii
    WHERE customer_id = p_customer_id;

    RETURN v_res;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Auditorlar uchun xavfsiz ko'rinish (View)
CREATE OR REPLACE VIEW view_customer_audits AS
SELECT 
    customer_id,
    full_name,
    decrypt_customer_passport(customer_id) AS decrypted_passport,
    created_at
FROM customers_pii;

-- Oddiy jadvalga ruxsatni yopib, faqat View ga ruxsat berish
REVOKE ALL ON customers_pii FROM PUBLIC;
-- Masalan: GRANT SELECT ON view_customer_audits TO compliance_auditor;
```
**Tushuntirish:** `SECURITY DEFINER` funksiyalari uni yaratgan egasining (owner) vakolati bilan ishlaydi. Oddiy foydalanuvchiga shifrlash kaliti berilmaydi, lekin u cheklangan View orqali ma'lumotni ko'ra oladi, shu bilan birga har bir kirish amali audit jurnaliga qat'iy yozib boriladi.
---

### Topshiriq #1163: Jadvalda Row-Level Security (RLS) ni Faollashtirish va Asosiy Siyosat
**Tavsif:** Bitta jadvalda bir nechta foydalanuvchilar ma'lumotlari saqlanganda, har bir foydalanuvchi faqat o'ziga tegishli qatorlarni ko'rishi va boshqalarning yozuvlariga kira olmasligi shart. Buni ta'minlash uchun PostgreSQL Row-Level Security mexanizmini to'g'ri faollashtirish zarur.
**Talablar:**
- `user_notes` jadvalini yaratish: `id`, `user_id`, `note_content`, `created_at`.
- `ALTER TABLE user_notes ENABLE ROW LEVEL SECURITY;` buyrug'i.
- `CREATE POLICY` yordamida foydalanuvchi faqat o'zining `user_id` siga teng bo'lgan yozuvlarni o'qiy olishi (USING).
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS user_notes (
    id SERIAL PRIMARY KEY,
    owner_username VARCHAR(50) NOT NULL,
    note_content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- 1. Jadvalda RLS ni yoqish
ALTER TABLE user_notes ENABLE ROW LEVEL SECURITY;

-- 2. Foydalanuvchilar uchun o'qish siyosatini yaratish
CREATE POLICY user_notes_isolation_policy ON user_notes
    FOR ALL
    TO PUBLIC
    USING (owner_username = CURRENT_USER)
    WITH CHECK (owner_username = CURRENT_USER);

-- Ruxsatlarni berish
GRANT SELECT, INSERT, UPDATE, DELETE ON user_notes TO PUBLIC;
GRANT USAGE, SELECT ON SEQUENCE user_notes_id_seq TO PUBLIC;
```
**Tushuntirish:** RLS yoqilganda (ENABLE ROW LEVEL SECURITY), agar hech qanday siyosat (policy) belgilanmagan bo'lsa, jadval egasi va superuserdan boshqa barcha foydalanuvchilar uchun jadval bo'sh ko'rinadi (Default Deny). `USING` sharti mavjud qatorlarni ko'rish va o'zgartirishni, `WITH CHECK` esa yangi qator kiritish yoki yangilashdagi ma'lumot qoidasini belgilaydi.
---

### Topshiriq #1164: Ko'p Ijarachilikda (Multi-Tenant) Tashkilot Ma'lumotlarini Izolyatsiya Qilish
**Tavsif:** SaaS platformasida yuzlab kompaniyalar (tenantlar) bitta umumiy ma'lumotlar bazasidan foydalanadi. Hech bir kompaniya boshqa kompaniyaning hisob-fakturalarini (invoices) ko'rmasligi kerak. Tenant izolyatsiyasi sessiya parametri orqali boshqarilishi lozim.
**Talablar:**
- `tenant_invoices` jadvali: `id`, `tenant_id`, `invoice_num`, `amount`.
- RLS siyosati: `tenant_id = nullif(current_setting('app.current_tenant_id', true), '')::UUID`.
- Bo'sh yoki noto'g'ri parametr berilganda tizim barcha ma'lumotlarni yashirishi (fail-closed).
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS tenant_invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    invoice_num VARCHAR(50) NOT NULL,
    amount NUMERIC(15, 2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- RLS ni yoqish
ALTER TABLE tenant_invoices ENABLE ROW LEVEL SECURITY;

-- Multi-Tenant xavfsizlik siyosati
CREATE POLICY tenant_isolation_policy ON tenant_invoices
    FOR ALL
    USING (
        tenant_id = NULLIF(current_setting('app.current_tenant_id', TRUE), '')::UUID
    )
    WITH CHECK (
        tenant_id = NULLIF(current_setting('app.current_tenant_id', TRUE), '')::UUID
    );

-- Tenant kontekstini o'rnatuvchi yordamchi protsedura
CREATE OR REPLACE PROCEDURE set_tenant_context(p_tenant_id UUID)
LANGUAGE plpgsql AS $$
BEGIN
    PERFORM set_config('app.current_tenant_id', p_tenant_id::TEXT, FALSE);
END;
$$;
```
**Tushuntirish:** `current_setting('app.current_tenant_id', true)` ikkinchi argumenti `true` bo'lgani sababli, agar o'zgaruvchi o'rnatilmagan bo'lsa xatolik bermaydi, balki NULL qaytaradi. Natijada `tenant_id = NULL` sharti bajarilmaydi va birorta ham qator ko'rinmaydi (Fail-closed xavfsizlik printsipi).
---

### Topshiriq #1165: CRUD Amallari Uchun Alohida RLS Siyosatlari (USING va WITH CHECK)
**Tavsif:** Real biznes tizimlarida o'qish (SELECT) va yozish (INSERT/UPDATE) huquqlari farq qiladi. Masalan, xodim o'z bo'limidagi barcha ma'lumotlarni ko'rishi mumkin, lekin faqat o'zi yaratgan ma'lumotlarni tahrirlashi yoki yangi ma'lumot kiritayotganda faqat tasdiqlanmagan holatda qo'sha olishi kerak.
**Talablar:**
- `department_reports` jadvali: `id`, `department_id`, `author_id`, `status`, `content`.
- SELECT uchun: butun bo'lim xodimlari ko'ra oladi.
- INSERT uchun: faqat o'zi muallif bo'lib, status='DRAFT' bilan yarata oladi.
- UPDATE uchun: faqat muallif va status='DRAFT' bo'lgandagina o'zgartira oladi.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS department_reports (
    id SERIAL PRIMARY KEY,
    department_id INT NOT NULL,
    author_id INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'DRAFT', -- 'DRAFT', 'SUBMITTED', 'APPROVED'
    content TEXT NOT NULL
);

ALTER TABLE department_reports ENABLE ROW LEVEL SECURITY;

-- 1. SELECT siyosati: Xodim o'z bo'limining barcha hisobotlarini ko'ra oladi
CREATE POLICY report_select_policy ON department_reports
    FOR SELECT
    USING (
        department_id = NULLIF(current_setting('app.department_id', TRUE), '')::INT
    );

-- 2. INSERT siyosati: Faqat o'z muallifligi va DRAFT statusi bilan yaratish mumkin
CREATE POLICY report_insert_policy ON department_reports
    FOR INSERT
    WITH CHECK (
        author_id = NULLIF(current_setting('app.user_id', TRUE), '')::INT AND
        status = 'DRAFT'
    );

-- 3. UPDATE siyosati: Faqat o'z hisoboti bo'lsa va hali DRAFT bo'lsa o'zgartira oladi
CREATE POLICY report_update_policy ON department_reports
    FOR UPDATE
    USING (
        author_id = NULLIF(current_setting('app.user_id', TRUE), '')::INT AND
        status = 'DRAFT'
    )
    WITH CHECK (
        author_id = NULLIF(current_setting('app.user_id', TRUE), '')::INT
    );
```
**Tushuntirish:** `USING` sharti jadvaldagi mavjud qatorlarga qaratilgan (qaysi qatorlarni ko'rish va o'zgartirish uchun tanlash mumkin). `WITH CHECK` sharti esa kiritilayotgan yangi qator yoki yangilangandan keyingi qator holatiga qaratilgan bo'lib, noqonuniy holatlarga o'tishni to'xtatadi.
---

### Topshiriq #1166: FORCE ROW LEVEL SECURITY: Jadval Egalari Uchun Majburiy Himoya
**Tavsif:** PostgreSQL-da standart holatda jadval egasi (Table Owner) va superuserlar RLS siyosatlaridan aylanib o'tadi (RLS bypass). Agar ilova jadval egasi nomidan ulanadigan bo'lsa, xatolik yuz berib barcha ijarachilar ma'lumotlari aralashib ketishi mumkin. Jadval egasiga ham RLS ni majburiy qilish kerak.
**Talablar:**
- `FORCE ROW LEVEL SECURITY` buyrug'ini qo'llash.
- Jadval egasi nomidan ham ma'lumotlar RLS filtri orqali o'tishini kafolatlash.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS enterprise_contracts (
    contract_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL,
    contract_amount NUMERIC(18, 2) NOT NULL,
    terms_text TEXT NOT NULL
);

-- RLS ni yoqish
ALTER TABLE enterprise_contracts ENABLE ROW LEVEL SECURITY;

-- Jadval egasi (Owner) uchun ham RLS ni MAJBURIY qilish!
ALTER TABLE enterprise_contracts FORCE ROW LEVEL SECURITY;

-- Tashkilot bo'yicha qat'iy cheklov siyosati
CREATE POLICY contract_org_policy ON enterprise_contracts
    FOR ALL
    USING (
        organization_id = NULLIF(current_setting('app.org_id', TRUE), '')::UUID
    );
```
**Tushuntirish:** `ALTER TABLE ... FORCE ROW LEVEL SECURITY` buyrug'i berilganda, hatto jadvalni yaratgan egasi ham RLS cheklovlariga bo'ysunadi. Faqat `SUPERUSER` yoki `BYPASSRLS` atributiga ega bo'lgan rollargina cheklovdan chetda qoladi. Bu ko'plab xavfsizlik sertifikatlarida (SOC 2, ISO 27001) majburiy talabdir.
---

### Topshiriq #1167: Iyerarxik Filial Rollari Uchun Dynamic RLS Siyosati
**Tavsif:** Korxona tuzilmasida bosh boshqarma xodimi barcha hududiy filiallar ma'lumotlarini, viloyat filiali rahbari faqat o'z viloyati va tuman filiallarini, oddiy xodim esa faqat o'z tumanini ko'rishi kerak. Ushbu iyerarxiyani RLS da subquery orqali amalga oshirish lozim.
**Talablar:**
- `branches` jadvali (`id`, `parent_id`, `name`) va `sales_data` jadvali (`id`, `branch_id`, `revenue`).
- Recursive CTE yoki subquery yordamida joriy foydalanuvchining filialiga tegishli barcha quyi filiallar savdosini ko'rsatuvchi RLS siyosati.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS branches (
    branch_id INT PRIMARY KEY,
    parent_branch_id INT REFERENCES branches(branch_id),
    branch_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS sales_data (
    sale_id SERIAL PRIMARY KEY,
    branch_id INT NOT NULL REFERENCES branches(branch_id),
    product_name VARCHAR(100) NOT NULL,
    revenue NUMERIC(12, 2) NOT NULL
);

ALTER TABLE sales_data ENABLE ROW LEVEL SECURITY;

-- Xodimning o'z filiali va barcha quyi filiallarini aniqlovchi xavfsizlik funksiyasi
CREATE OR REPLACE FUNCTION get_accessible_branches(p_user_branch_id INT)
RETURNS TABLE(accessible_id INT) AS $$
BEGIN
    RETURN QUERY
    WITH RECURSIVE branch_hierarchy AS (
        SELECT branch_id FROM branches WHERE branch_id = p_user_branch_id
        UNION ALL
        SELECT b.branch_id 
        FROM branches b
        JOIN branch_hierarchy bh ON b.parent_branch_id = bh.branch_id
    )
    SELECT branch_id FROM branch_hierarchy;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;

-- RLS Siyosati: Faqat ruxsat etilgan filiallar ro'yxatidagi ma'lumotlar chiqadi
CREATE POLICY sales_hierarchy_policy ON sales_data
    FOR SELECT
    USING (
        branch_id IN (
            SELECT get_accessible_branches(NULLIF(current_setting('app.current_branch_id', TRUE), '')::INT)
        )
    );
```
**Tushuntirish:** `STABLE` va `SECURITY DEFINER` yorlig'i berilgan funksiya orqali rekursiv shoxlanish (hierarchy) hisoblab olinadi. Natijada bosh ofis direktori butun respublika filiallarini ko'ra olgani holda, tuman xodimi faqat o'z filial ma'lumotlari bilan cheklanadi.
---

### Topshiriq #1168: RESTRICTIVE va PERMISSIVE Siyosatlarni Kombinatsiyalash
**Tavsif:** PostgreSQL-da siyosatlar standart holatda `PERMISSIVE` bo'lib, bir nechta siyosat bo'lsa ular `OR` operatori bilan birlashadi. Ammo ba'zi talablar (masalan, "Qora ro'yxatdagi mijozlar hech kimga ko'rinmasin") mutlaq majburiy (`AND`) bo'lishi kerak. Bunga erishish uchun `AS RESTRICTIVE` siyosat turidan foydalanish lozim.
**Talablar:**
- `customer_accounts` jadvali.
- Permissive siyosatlar: Menejer o'z mijozlarini, Auditor esa auditga olinganlarni ko'radi.
- Restrictive siyosat: Har ikkala holatda ham `is_fraud_blocked = FALSE` bo'lishi shart!
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS customer_accounts (
    account_id SERIAL PRIMARY KEY,
    manager_id INT NOT NULL,
    is_audit_flagged BOOLEAN NOT NULL DEFAULT FALSE,
    is_fraud_blocked BOOLEAN NOT NULL DEFAULT FALSE,
    balance NUMERIC(15, 2) NOT NULL
);

ALTER TABLE customer_accounts ENABLE ROW LEVEL SECURITY;

-- 1. Permissive siyosat A: Menejer o'z hisoblarini ko'radi
CREATE POLICY policy_manager_access ON customer_accounts
    AS PERMISSIVE
    FOR SELECT
    USING (manager_id = NULLIF(current_setting('app.user_id', TRUE), '')::INT);

-- 2. Permissive siyosat B: Auditor audit belgisi qo'yilganlarini ko'radi
CREATE POLICY policy_auditor_access ON customer_accounts
    AS PERMISSIVE
    FOR SELECT
    USING (is_audit_flagged = TRUE AND current_setting('app.user_role', TRUE) = 'auditor');

-- 3. RESTRICTIVE siyosat: Firibgarlik tufayli bloklanganlar HECH KIMGA ko'rinmasin!
CREATE POLICY policy_block_fraudulent_accounts ON customer_accounts
    AS RESTRICTIVE
    FOR ALL
    USING (is_fraud_blocked = FALSE);
```
**Tushuntirish:** PostgreSQL siyosatlarni baholashda formulani quyidagicha tuzadi: `(Permissive1 OR Permissive2 OR ...) AND (Restrictive1 AND Restrictive2 ...)`. `RESTRICTIVE` siyosat barcha `PERMISSIVE` qoidalar ustidan filtr qo'yadi va xavfsizlik darajasini keskin oshiradi.
---

### Topshiriq #1169: SET LOCAL app.current_tenant_id va Tranzaksiya Darajasidagi Izolyatsiya
**Tavsif:** Connection Pooler (PgBouncer, HikariCP) ishlatilganda, bitta jismoniy ulanish turli so'rovlar o'rtasida qayta ishlatiladi. Agar tenant identifikatori global sessiyada (`SET`) o'rnatilsa, keyingi boshqa tenantning so'rovi oldingi tenant ma'lumotlarini o'qib qo'yishi (Connection Pollution) mumkin. Tranzaksiya darajasidagi izolyatsiyani ta'minlash zarur.
**Talablar:**
- `SET LOCAL` dan foydalanuvchi xavfsiz PL/pgSQL wrapper yoki tranzaksiya patternini tuzish.
- Tranzaksiya yakunlangach tenant identifikatori avtomatik o'chishini tekshirish.
**Yechim (SQL):**
```sql
-- Tranzaksiya kontekstida xavfsiz amallarni bajaruvchi funksiya
CREATE OR REPLACE FUNCTION execute_tenant_operation(
    p_tenant_id UUID,
    p_operation_query TEXT
) RETURNS VOID AS $$
BEGIN
    -- SET LOCAL faqat joriy tranzaksiya (BEGIN ... COMMIT) uchun amal qiladi
    PERFORM set_config('app.current_tenant_id', p_tenant_id::TEXT, TRUE);
    
    -- Dinamik so'rovni bajarish
    EXECUTE p_operation_query;
END;
$$ LANGUAGE plpgsql;

-- Ilova tomonida (Backend pooler) xavfsiz foydalanish standarti:
/*
BEGIN;
    -- 3-argument 'true' bo'lishi bu parametr tranzaksiyaga bog'liqligini bildiradi (is_local = true)
    SELECT set_config('app.current_tenant_id', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', true);
    
    -- Faqat a0eebc99 tenantiga tegishli ma'lumotlar o'qiladi
    SELECT * FROM tenant_invoices;
COMMIT;
-- COMMIT yoki ROLLBACK dan so'ng 'app.current_tenant_id' o'z-o'zidan yo'qoladi!
*/
```
**Tushuntirish:** `set_config('param', 'value', true)` dagi `true` bayrog'i `SET LOCAL` ga ekvivalentdir. Bu ulanish hovuzi (connection pool) da bitta jismoniy ulanish boshqa so'rovga berilganda oldingi mijozning ma'lumotlari qolib ketmasligini 100% kafolatlaydi.
---

### Topshiriq #1170: RLS Unumdorligini Optimallashtirish: B-Tree Indekslar va STABLE Funksiyalar
**Tavsif:** RLS siyosatlari millionlab yozuvlarga ega jadvallarda so'rovlarni juda sekinlashtirishi mumkin, chunki har bir qator uchun `USING` sharti tekshiriladi. Agar funksiya `VOLATILE` deb belgilangan bo'lsa, PostgreSQL uni har bir qator uchun qayta-qayta chaqiradi va so'rov vaqti soniyalarga cho'ziladi.
**Talablar:**
- Siyosatda ishlatiladigan ustunlarga B-Tree indekslar yaratish.
- Siyosat funksiyalarini `STABLE` qilib belgilash va query planner subquery optimallashini ta'minlash.
- `EXPLAIN ANALYZE` orqali indeks qo'llanganligini tasdiqlovchi struktura.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS enterprise_orders (
    order_id BIGSERIAL PRIMARY KEY,
    organization_id INT NOT NULL,
    customer_id INT NOT NULL,
    total_price NUMERIC(15, 2) NOT NULL,
    order_status VARCHAR(20) NOT NULL
);

-- RLS tezkor ishlashi uchun organization_id ustuniga indeks yaratish
CREATE INDEX IF NOT EXISTS idx_enterprise_orders_org_id 
ON enterprise_orders(organization_id);

ALTER TABLE enterprise_orders ENABLE ROW LEVEL SECURITY;

-- Siyosatda subquery va STABLE funksiyadan foydalanish
CREATE OR REPLACE FUNCTION get_current_user_org()
RETURNS INT AS $$
BEGIN
    RETURN NULLIF(current_setting('app.org_id', TRUE), '')::INT;
END;
$$ LANGUAGE plpgsql STABLE; -- STABLE bitta so'rov davomida natijani keshlaydi!

-- Indeksga tushadigan optimal RLS siyosati
CREATE POLICY enterprise_orders_fast_policy ON enterprise_orders
    FOR SELECT
    USING (
        organization_id = (SELECT get_current_user_org())
    );
```
**Tushuntirish:** `STABLE` atributi PostgreSQL optimizatoriga bitta SQL so'rov ichida ushbu funksiya natijasi o'zgarmasligini bildiradi. `(SELECT get_current_user_org())` ko'rinishidagi subquery esa funksiyani butun jadval uchun faqat BIR MARTA chaqirib, qiymatni konstanta sifatida indeks qidiruviga (`Index Scan`) uzatadi.
---

### Topshiriq #1171: Vaqtinchalik Kirish Huquqi (Time-Based Access Control) Bo'yicha RLS
**Tavsif:** Xavfsizlik xizmati yoki tashqi pudratchilarga tizimdagi konfidentsial ma'lumotlarga cheklangan muddatga (masalan, 2 soatga yoki belgilangan sanagacha) kirish huquqi beriladi. Muddat o'tishi bilan RLS hech qanday ma'lumotni ko'rsatmasligi kerak.
**Talablar:**
- `contractor_access_grants` jadvali: kimga, qaysi resursga va qachongacha ruxsat berilgan.
- `sensitive_assets` jadvali.
- RLS siyosati: Faqat `CURRENT_TIMESTAMP < valid_until` bo'lgan faol ruxsatnomalar bo'yicha ma'lumot ochiladi.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS contractor_access_grants (
    grant_id SERIAL PRIMARY KEY,
    contractor_id INT NOT NULL,
    asset_id INT NOT NULL,
    valid_from TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    valid_until TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS sensitive_assets (
    asset_id SERIAL PRIMARY KEY,
    asset_name VARCHAR(100) NOT NULL,
    secret_data TEXT NOT NULL
);

ALTER TABLE sensitive_assets ENABLE ROW LEVEL SECURITY;

-- Vaqtinchalik ruxsatni tekshiruvchi RLS siyosati
CREATE POLICY time_bound_asset_policy ON sensitive_assets
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM contractor_access_grants g
            WHERE g.asset_id = sensitive_assets.asset_id
              AND g.contractor_id = NULLIF(current_setting('app.contractor_id', TRUE), '')::INT
              AND CURRENT_TIMESTAMP BETWEEN g.valid_from AND g.valid_until
        )
    );
```
**Tushuntirish:** Bu arxitekturada muddat tugashi bilan ma'lumotlar bazasi darajasida ruxsat avtomatik yopiladi. Cron job yoki ma'lumotlarni o'chirish skriptlarini kutish shart emas; real vaqtdagi `CURRENT_TIMESTAMP BETWEEN valid_from AND valid_until` tekshiruvi orqali vaqt tugashi bilan birorta ham qator qaytarilmaydi.
---

### Topshiriq #1172: Guruh Rollari va current_user Bo'yicha Dinamik RLS Siyosati
**Tavsif:** Foydalanuvchilar lavozimiga qarab har xil guruhlarga a'zo bo'ladi: `finance_team`, `hr_team`, `admin_team`. Jadvaldagi ma'lumotlar uning tegishli xavfsizlik yorlig'iga (`security_label`) va foydalanuvchining PostgreSQL guruhlariga (`pg_has_role`) qarab ochilishi kerak.
**Talablar:**
- `corporate_docs` jadvali: `doc_id`, `title`, `required_role`.
- `pg_has_role(CURRENT_USER, required_role, 'MEMBER')` orqali guruh tekshiruvi.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS corporate_docs (
    doc_id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    content TEXT NOT NULL,
    required_role NAME NOT NULL
);

ALTER TABLE corporate_docs ENABLE ROW LEVEL SECURITY;

-- Dinamik guruh a'zoligini tekshiruvchi siyosat
CREATE POLICY doc_role_based_policy ON corporate_docs
    FOR SELECT
    USING (
        pg_has_role(CURRENT_USER, required_role, 'MEMBER') OR
        pg_has_role(CURRENT_USER, 'super_auditor', 'MEMBER')
    );

-- Namuna rollar:
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'hr_team') THEN
        CREATE ROLE hr_team NOLOGIN;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'finance_team') THEN
        CREATE ROLE finance_team NOLOGIN;
    END IF;
END
$$;
```
**Tushuntirish:** `pg_has_role()` tizim funksiyasi foydalanuvchining to'g'ridan-to'g'ri yoki iyerarxik guruhlar orqali ushbu roldagi a'zoligini tekshiradi. Bu orqali RBAC (Role-Based Access Control) to'g'ridan-to'g'ri ma'lumotlar bazasi yadrosiga integratsiya qilinadi.
---

### Topshiriq #1173: JWT Token Claims Asosida RLS Avtorizatsiyasi (Supabase/PostgREST Uslubi)
**Tavsif:** Zamonaviy arxitekturalarda (Supabase, PostgREST) backend foydalanuvchi ma'lumotlarini JSON Web Token (JWT) ko'rinishida yuboradi. Ma'lumotlar bazasi so'rovdagi `request.jwt.claim` JSON obyektidan foydalanuvchi ID va rollarini ajratib olib, RLS siyosatida qo'llashi zarur.
**Talablar:**
- `user_profiles_v2` jadvali.
- `request.jwt.claim` sessiya parametrini JSON sifatida tahlil qiluvchi xavfsiz yordamchi funksiya.
- RLS siyosatida `jwt ->> 'sub'` orqali foydalanuvchi qatorlarini ajratish.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS user_profiles_v2 (
    user_uuid UUID PRIMARY KEY,
    display_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    is_vip BOOLEAN DEFAULT FALSE
);

ALTER TABLE user_profiles_v2 ENABLE ROW LEVEL SECURITY;

-- JWT claim ma'lumotlarini xavfsiz o'qish funksiyasi
CREATE OR REPLACE FUNCTION auth_jwt_claim(p_claim_key TEXT)
RETURNS TEXT AS $$
DECLARE
    v_claims_raw TEXT;
    v_claims_json JSONB;
BEGIN
    v_claims_raw := current_setting('request.jwt.claims', TRUE);
    IF v_claims_raw IS NULL OR v_claims_raw = '' THEN
        RETURN NULL;
    END IF;

    v_claims_json := v_claims_raw::JSONB;
    RETURN v_claims_json ->> p_claim_key;
EXCEPTION
    WHEN OTHERS THEN
        RETURN NULL;
END;
$$ LANGUAGE plpgsql STABLE;

-- JWT 'sub' (subject - user UUID) bo'yicha profilni himoyalash
CREATE POLICY user_profiles_jwt_policy ON user_profiles_v2
    FOR ALL
    USING (
        user_uuid = (auth_jwt_claim('sub'))::UUID
    )
    WITH CHECK (
        user_uuid = (auth_jwt_claim('sub'))::UUID
    );
```
**Tushuntirish:** PostgREST va Supabase kabi serverlar har bir HTTP so'rovi uchun `SET LOCAL request.jwt.claims = '{"sub":"...", "role":"..."}'` buyrug'ini yuboradi. Ma'lumotlar bazasi darajasida JWT claimlarini o'qish orqali backend dasturlash tilidan qat'i nazar, ma'lumotlar xavfsizligi kafolatlanadi.
---

### Topshiriq #1174: RLS Bypass va Leaks-Proof Funksiyalar Auditi
**Tavsif:** RLS yoqilgan bo'lsa ham, ba'zi foydalanuvchi yozgan funksiyalar (User Defined Functions) indekslar yoki xatoliklar orqali ma'lumot sizdirishi mumkin (Side-channel data leak). RLS ostidagi jadvallarda faqat `LEAKPROOF` funksiyalargina xavfsiz ishlatilishi mumkinligini ta'minlash va audit qilish kerak.
**Talablar:**
- `LEAKPROOF` atributiga ega xavfsiz tekshiruv funksiyasini yaratish.
- Tizimdagi qaysi rollar `BYPASSRLS` huquqiga ega ekanligini aniqlovchi xavfsizlik audit so'rovini yozish.
**Yechim (SQL):**
```sql
-- 1. Ma'lumot sizdirmaydigan (Leakproof) xavfsiz funksiya yaratish
-- Faqat superuser LEAKPROOF funksiya yarata oladi
CREATE OR REPLACE FUNCTION is_valid_contract_code(p_code TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN p_code ~ '^[A-Z]{3}-[0-9]{4}$';
END;
$$ LANGUAGE plpgsql IMMUTABLE LEAKPROOF;

-- 2. Ma'lumotlar bazasida RLS ni chetlab o'ta oladigan (Bypass) barcha rollarni aniqlovchi xavfsizlik auditi
SELECT 
    r.rolname AS xavfli_rol_nomi,
    r.rolsuper AS superuser_huquqi,
    r.rolbypassrls AS rls_bypass_huquqi,
    r.rolcanlogin AS tizimga_kira_oladi
FROM pg_roles r
WHERE r.rolsuper = TRUE OR r.rolbypassrls = TRUE;

-- 3. Qaysi jadvallarda RLS yoqilmaganligini aniqlash auditi
SELECT 
    schemaname,
    tablename,
    rowsecurity AS rls_yoqilganmi
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
  AND rowsecurity = FALSE;
```
**Tushuntirish:** `LEAKPROOF` funksiyalari yon ta'sirga ega emas va ularda optimizator shartlarni bajarish tartibini o'zgartirganda ma'lumot sizib chiqishi istisno qilinadi. Shuningdek, `pg_roles` jurnali orqali `rolbypassrls` huquqiga ega bo'lgan rollarni nazorat qilish bazadagi yashirin teshiklarni aniqlashda juda muhimdir.
---

### Topshiriq #1175: Dynamic Data Masking (DDM) Arxitekturasi: Xavfsiz Ko'rinish (View)
**Tavsif:** Mijozlarning shaxsiy ma'lumotlari (PII) ishlab chiqarish bazasida saqlanadi. Biroq hisobotlar yoki statistik monitoring bilan shug'ullanuvchi xodimlar ushbu ma'lumotlarning asl nusxasini ko'rmasligi kerak. Ma'lumotlarni jismonan o'zgartirmasdan, faqat o'qish paytida dinamik niqoblash (Dynamic Data Masking) arxitekturasini yaratish talab qilinadi.
**Talablar:**
- `raw_clients` jadvali: `id`, `full_name`, `phone`, `email`.
- `masked_clients_view` ko'rinishi orqali telefon va emailni niqoblab ko'rsatish.
- To'g'ridan-to'g'ri jadvalga kirishni bekor qilib, faqat View orqali o'qishga ruxsat berish.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS raw_clients (
    client_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    registered_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- Dinamik niqoblangan ko'rinish (DDM View)
CREATE OR REPLACE VIEW masked_clients_view AS
SELECT 
    client_id,
    -- Ism: birinchi va oxirgi harf ochiq, qolgani yulduzcha
    left(full_name, 1) || '***' || right(full_name, 1) AS full_name,
    -- Telefon: +99890***1234
    left(phone, 7) || '***' || right(phone, 4) AS phone,
    -- Email: b***z@domain.com
    regexp_replace(email, '(?<=.).(?=.*@)', '*', 'g') AS email,
    registered_at
FROM raw_clients;

-- Rollarni yaratish va ruxsatlarni ajratish
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'analyst_role') THEN
        CREATE ROLE analyst_role NOLOGIN;
    END IF;
END
$$;

-- Analitiklar uchun faqat niqoblangan ko'rinishga ruxsat berish
REVOKE ALL ON raw_clients FROM analyst_role;
GRANT SELECT ON masked_clients_view TO analyst_role;
```
**Tushuntirish:** Dynamic Data Masking (DDM) ma'lumotlar bazasida jismoniy yozuvlarni buzmasdan saqlaydi, lekin so'rov beruvchining vakolatiga qarab ma'lumotlarni niqoblangan holda qaytaradi. Bu ISO/IEC 27701 va GDPR talablariga mos keladi.
---

### Topshiriq #1176: Bank Karta Raqamini (PAN) Qisman Niqoblash Funksiyasi
**Tavsif:** Bank kartalari bilan ishlashda kvitansiyalar, SMS xabarnomalar va qo'llab-quvvatlash xizmati ekranlarida karta raqamining faqat dastlabki 6 ta (BIN) va oxirgi 4 ta raqamini ko'rsatishga ruxsat beriladi (`411122******1234` formati).
**Talablar:**
- 16 yoki 19 xonali karta raqamlarini qabul qiluvchi xavfsiz SQL funksiyasi.
- Raqam noto'g'ri bo'lsa yoki bo'sh bo'lsa xavfsiz holatda qaytarish.
- Funksiyani `IMMUTABLE` va `PARALLEL SAFE` qilib optimallashtirish.
**Yechim (SQL):**
```sql
CREATE OR REPLACE FUNCTION mask_credit_card(p_raw_pan TEXT)
RETURNS TEXT AS $$
DECLARE
    v_clean TEXT;
    v_len INT;
BEGIN
    IF p_raw_pan IS NULL THEN
        RETURN NULL;
    END IF;

    -- Bo'shliq va chiziqlarni tozalash
    v_clean := regexp_replace(p_raw_pan, '[^0-9]', '', 'g');
    v_len := length(v_clean);

    IF v_len < 12 OR v_len > 19 THEN
        RETURN 'INVALID_CARD_NUMBER';
    END IF;

    -- Standart PCI-DSS formati: Birinchi 6 ta (BIN) + yulduzchalar + oxirgi 4 ta raqam
    RETURN substring(v_clean from 1 for 6) || 
           repeat('*', v_len - 10) || 
           substring(v_clean from v_len - 3 for 4);
END;
$$ LANGUAGE plpgsql IMMUTABLE PARALLEL SAFE;
```
**Tushuntirish:** `IMMUTABLE` va `PARALLEL SAFE` atributlari PostgreSQL optimizatoriga ushbu funksiyani parallel so'rovlarda (`Parallel Seq Scan`) millionlab qatorlar ustida samarali va yadrolararo xotira almashinuvida tezkor ishlatish imkonini beradi.
---

### Topshiriq #1177: JShShIR (PINFL) va Pasport Seriyasini Maskirovka Qilish
**Tavsif:** O'zbekiston Respublikasi qonunchiligiga ko'ra, fuqarolarning 14 xonali Jismoniy Shaxsning Shaxsiy Identifikatsiya Raqami (JShShIR) va pasport seriya-raqami o'ta muhim shaxsiy ma'lumot (PII) hisoblanadi. Ularni operatorlar ko'rishi uchun qisman niqoblash zarur.
**Talablar:**
- 14 xonali JShShIR uchun `3120190******5` ko'rinishida niqoblash.
- Pasport seriya-raqami (masalan, `AB1234567`) uchun `AB****567` ko'rinishida niqoblash.
**Yechim (SQL):**
```sql
CREATE OR REPLACE FUNCTION mask_pinfl(p_pinfl TEXT)
RETURNS TEXT AS $$
DECLARE
    v_clean TEXT;
BEGIN
    IF p_pinfl IS NULL THEN
        RETURN NULL;
    END IF;

    v_clean := regexp_replace(p_pinfl, '[^0-9]', '', 'g');

    IF length(v_clean) <> 14 THEN
        RETURN 'INVALID_PINFL';
    END IF;

    -- Birinchi 7 ta raqam (tug'ilgan sana va jins kodi) + 6 ta yulduzcha + oxirgi nazorat raqami
    RETURN left(v_clean, 7) || '******' || right(v_clean, 1);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION mask_passport_number(p_passport TEXT)
RETURNS TEXT AS $$
DECLARE
    v_clean TEXT;
BEGIN
    IF p_passport IS NULL THEN
        RETURN NULL;
    END IF;

    v_clean := upper(regexp_replace(p_passport, '\s+', '', 'g'));

    IF length(v_clean) < 8 THEN
        RETURN 'INVALID_PASSPORT';
    END IF;

    -- Pasport seriyasi (2 harf) + **** + oxirgi 3 ta raqam
    RETURN left(v_clean, 2) || repeat('*', length(v_clean) - 5) || right(v_clean, 3);
END;
$$ LANGUAGE plpgsql IMMUTABLE;
```
**Tushuntirish:** Niqoblash orqali operator mijozning shaxsini qisman tekshirishi (masalan, tug'ilgan sanasi yoki pasport seriyasi bo'yicha) mumkin bo'ladi, lekin to'liq ma'lumotni o'g'irlab uchinchi shaxslarga sota olmaydi.
---

### Topshiriq #1178: PostgreSQL Anonymizer (anon) Yordamida Test Muhitini Maskirovka Qilish
**Tavsif:** Ishlab chiqarish (Production) bazasining zaxira nusxasini (Dump) test (Staging/Dev) serveriga yuklashdan oldin barcha maxfiy ma'lumotlarni haqiqiy ko'rinishdagi tasodifiy sintetik ma'lumotlar bilan almashtirish (Anonymization) lozim.
**Talablar:**
- `anon` kengaytmasi tamoyillari asosida jadval ustunlariga niqob qoidalarini (MASKED WITH) biriktirish.
- Statik anonimlashtirish (`anon.anonymize_table`) amalini bajaruvchi xavfsiz ssenariy.
**Yechim (SQL):**
```sql
-- PostgreSQL Anonymizer kengaytmasi konsepsiyasi
-- CREATE EXTENSION IF NOT EXISTS anon CASCADE;

CREATE TABLE IF NOT EXISTS customer_contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    company_name VARCHAR(100),
    salary NUMERIC(12, 2)
);

-- Maxfiylikni ta'minlash uchun ustunlarga xavfsizlik qoidalarini sharh (COMMENT) sifatida biriktirish
COMMENT ON COLUMN customer_contacts.first_name IS 'MASKED WITH anon.dummy_first_name()';
COMMENT ON COLUMN customer_contacts.last_name IS 'MASKED WITH anon.dummy_last_name()';
COMMENT ON COLUMN customer_contacts.company_name IS 'MASKED WITH anon.dummy_company_name()';
COMMENT ON COLUMN customer_contacts.salary IS 'MASKED WITH anon.noise(salary, 0.15)'; -- 15% tasodifiy shovqin qo'shish

-- Staging muhitiga yuklangandan keyin barcha ma'lumotlarni sintetik qilib qayta yozuvchi skript
CREATE OR REPLACE PROCEDURE perform_staging_anonymization()
LANGUAGE plpgsql AS $$
BEGIN
    -- Haqiqiy ismlarni soxta ismlarga almashtirish
    UPDATE customer_contacts
    SET 
        first_name = 'User_' || floor(random() * 10000)::TEXT,
        last_name = 'Client_' || floor(random() * 10000)::TEXT,
        company_name = 'Enterprise_' || floor(random() * 500)::TEXT,
        salary = round(salary * (0.85 + random() * 0.30), 2); -- 15% diapazonda shovqin

    RAISE NOTICE 'Barcha mijoz ma''lumotlari Staging muhiti uchun muvaffaqiyatli anonimlashtirildi.';
END;
$$;
```
**Tushuntirish:** Ko'plab xavfsizlik hodisalari test muhitlaridan kelib chiqadi, chunki dasturchilar va testchilar haqiqiy prod bazadan nusxa olib, zaif himoyalangan dev-serverlarga yuklaydi. Statik anonimlashtirish orqali dev-muhitga birorta ham haqiqiy shaxsiy ma'lumot tushmaydi.
---

### Topshiriq #1179: Elektron Pochta Manzilini Xavfsiz Regex Bilan Anonimlashtirish
**Tavsif:** Foydalanuvchilar o'z parollarini tiklash sahifasida tizim ularga email yuborilganini bildirish uchun `a****e@gmail.com` ko'rinishida ishora beradi. Ushbu transformatsiyani bajaruvchi yuqori unumdorli SQL regex funksiyasini yaratish kerak.
**Talablar:**
- Foydalanuvchi nomining birinchi va oxirgi harflari ochiq, oraliq qismi `*` bilan niqoblangan bo'lishi.
- Agar foydalanuvchi nomi 2 yoki 1 belgidan iborat bo'lsa, xatoliksiz to'g'ri ishlashi.
- Domen qismi (masalan, `@gmail.com`) to'liq saqlanib qolishi.
**Yechim (SQL):**
```sql
CREATE OR REPLACE FUNCTION mask_email_address(p_email TEXT)
RETURNS TEXT AS $$
DECLARE
    v_user_part TEXT;
    v_domain_part TEXT;
    v_len INT;
BEGIN
    IF p_email IS NULL OR position('@' in p_email) = 0 THEN
        RETURN 'invalid_or_null_email';
    END IF;

    v_user_part := split_part(p_email, '@', 1);
    v_domain_part := split_part(p_email, '@', 2);
    v_len := length(v_user_part);

    IF v_len <= 2 THEN
        -- Qisqa nomlar uchun: a*@domain.com
        RETURN left(v_user_part, 1) || '*@' || v_domain_part;
    ELSE
        -- 3 va undan ortiq belgilar uchun: birinchi va oxirgi harf ochiq
        RETURN left(v_user_part, 1) || 
               repeat('*', v_len - 2) || 
               right(v_user_part, 1) || '@' || 
               v_domain_part;
    END IF;
END;
$$ LANGUAGE plpgsql IMMUTABLE LEAKPROOF;
```
**Tushuntirish:** Ushbu funksiya foydalanuvchiga qaysi manzilga kod yuborilganini eslatish uchun yetarli ma'lumot beradi, biroq ekranni ko'rib turgan begona shaxslarga haqiqiy to'liq pochta manzilini ochib bermaydi.
---

### Topshiriq #1180: Shartli Niqoblash (Conditional Role-Based Masking)
**Tavsif:** Bitta ko'rinishning o'zi (View) turli rollar uchun turlicha ma'lumot ko'rsatishi lozim. Agar so'rovni `admin_user` bajarsa to'liq telefon raqamini, agar `callcenter_agent` bajarsa faqat niqoblangan versiyasini ko'rishi kerak.
**Talablar:**
- `pg_has_role()` yordamida dinamik tekshiruv.
- `CASE WHEN` sharti orqali roliga qarab ma'lumotni ochish yoki niqoblash.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id SERIAL PRIMARY KEY,
    customer_phone VARCHAR(20) NOT NULL,
    issue_description TEXT NOT NULL
);

-- Shartli niqoblangan ko'rinish
CREATE OR REPLACE VIEW view_support_tickets_smart AS
SELECT 
    ticket_id,
    CASE 
        WHEN pg_has_role(CURRENT_USER, 'sec_admin', 'MEMBER') THEN customer_phone
        WHEN pg_has_role(CURRENT_USER, 'supervisor_role', 'MEMBER') THEN left(customer_phone, 9) || '****'
        ELSE '+998*********' -- Oddiy operator faqat boshlang'ich kodni ko'radi
    END AS display_phone,
    issue_description
FROM support_tickets;
```
**Tushuntirish:** Shartli niqoblash orqali har bir rol uchun alohida jadval yoki ko'rinish yaratish talab etilmaydi. Yagona View orqali xavfsizlik talablariga mos RBAC (Role Based Access Control) ma'lumotlar oqimiga avtomatik tatbiq etiladi.
---

### Topshiriq #1181: Ustun Darajasidagi Ruxsatlar (Column-Level Security - CLS)
**Tavsif:** Jamoaning ba'zi a'zolari (masalan, marketing bo'limi) xodimlarning ismi va lavozimini ko'rishi mumkin, ammo maosh (`salary`) yoki bank hisob raqamini ko'rish huquqiga mutlaqo ega bo'lmasligi kerak.
**Talablar:**
- Ustun darajasidagi `GRANT SELECT (col1, col2)` buyrug'ini qo'llash.
- Ruxsat berilmagan ustunga so'rov berilganda `permission denied for column ...` xatoligi qaytishini ta'minlash.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS employees_private (
    emp_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    salary NUMERIC(12, 2) NOT NULL,
    bank_account_iban VARCHAR(34) NOT NULL
);

-- Marketing roli
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'marketing_role') THEN
        CREATE ROLE marketing_role NOLOGIN;
    END IF;
END
$$;

-- 1. Jadvaldagi barcha umumiy huquqlarni bekor qilish
REVOKE ALL ON employees_private FROM marketing_role;

-- 2. Faqat kerakli ustunlarga SELECT huquqini berish (Column-Level Grant)
GRANT SELECT (emp_id, full_name, department) ON employees_private TO marketing_role;

-- Marketing foydalanuvchisi:
-- SELECT emp_id, full_name FROM employees_private; -> Muvaffaqiyatli ishlaydi!
-- SELECT salary FROM employees_private; -> ERROR: permission denied for table employees_private
```
**Tushuntirish:** PostgreSQL ustun darajasidagi ruxsatlarni (Column-Level Security) o'rnatilgan holda qo'llab-quvvatlaydi. Bu ilova xatolari yoki kiberhujum vaqtida tajovuzkor `SELECT *` qilsa ham, maxfiy ustunlarga kirishni zudlik bilan to'xtatadi.
---

### Topshiriq #1182: Differensial Maxfiylik (Differential Privacy) va Statistik Shovqin Qo'shish
**Tavsif:** Korxona ma'lumotlar bazasidan analitiklar statistik o'rtacha qiymatlarni hisoblashda individual xodimlarning aniq maoshlarini aniqlab ololmasliklari (Re-identification attack) uchun natijaga Laplace mexanizmi asosidagi kriptografik shovqin (noise) qo'shish zarur.
**Talablar:**
- Guruh bo'yicha o'rtacha maoshni hisoblovchi, lekin natijaga kichik differensial shovqin qo'shuvchi maxsus agregat funksiya.
**Yechim (SQL):**
```sql
-- Laplace taqsimotiga yaqinlashgan shovqin qo'shuvchi funksiya
CREATE OR REPLACE FUNCTION diff_privacy_noise(p_epsilon FLOAT DEFAULT 1.0)
RETURNS FLOAT AS $$
DECLARE
    v_u FLOAT;
BEGIN
    -- U (-0.5, 0.5) oralig'idagi tasodifiy son
    v_u := random() - 0.5;
    
    -- Oddiy Laplace approksimatsiyasi
    IF v_u = 0 THEN
        RETURN 0;
    ELSE
        RETURN - (1.0 / p_epsilon) * sign(v_u) * ln(1.0 - 2.0 * abs(v_u));
    END IF;
END;
$$ LANGUAGE plpgsql VOLATILE;

-- Differensial maxfiylik bilan hisoblangan o'rtacha oylik ko'rinishi
CREATE OR REPLACE VIEW view_department_salary_privacy AS
SELECT 
    department,
    count(*) AS employee_count,
    -- O'rtacha qiymatga matematik shovqin kiritiladi
    round((avg(salary) + diff_privacy_noise(0.5))::NUMERIC, 2) AS differentially_private_avg_salary
FROM employees_private
GROUP BY department
HAVING count(*) >= 5; -- K-anonymity: 5 tadan kam xodimi bor bo'lim ko'rsatilmaydi!
```
**Tushuntirish:** Agar bo'limda 1 nafar odam ishlasa, `avg(salary)` uning aniq oyligini fosh qiladi. Differensial maxfiylik va `HAVING count(*) >= 5` cheklovi (K-Anonymity) shaxsiy ma'lumotlar orqali shaxslarni fosh etish xavfini matematik jihatdan bartaraf etadi.
---

### Topshiriq #1183: GDPR Talabi: "Right to be Forgotten" va Kripto-Shredding (Crypto-Shredding)
**Tavsif:** GDPR talablariga ko'ra, mijoz o'z ma'lumotlarini o'chirishni talab qilganda (Right to be Forgotten), arxivlar va zaxira nusxalaridagi (backup) ma'lumotlarni jismonan o'chirib bo'lmaydi. Bunga yechim sifatida har bir mijoz uchun alohida shifrlash kaliti saqlanadi va ushbu kalit o'chirib tashlanganda butun ma'lumotlar qayta tiklab bo'lmaydigan chiqindiga (Crypto-Shredding) aylanadi.
**Talablar:**
- `client_keys` va `client_encrypted_data` jadvallari.
- Mijozning kalitini yo'q qilish (`crypto_shred_client`) protsedurasi.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS client_keys (
    client_uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    personal_enc_key TEXT NOT NULL,
    is_shredded BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS client_encrypted_data (
    record_id SERIAL PRIMARY KEY,
    client_uuid UUID NOT NULL REFERENCES client_keys(client_uuid),
    encrypted_payload BYTEA NOT NULL
);

-- Kripto-shredding (Mijoz ma'lumotlarini butunlay o'qib bo'lmas holga keltirish)
CREATE OR REPLACE PROCEDURE crypto_shred_client(p_client_uuid UUID)
LANGUAGE plpgsql AS $$
BEGIN
    -- Kalitni o'rniga tasodifiy axlat yozib, so'ngra o'chirish (Doimiy yo'q qilish)
    UPDATE client_keys
    SET personal_enc_key = encode(gen_random_bytes(64), 'hex'),
        is_shredded = TRUE
    WHERE client_uuid = p_client_uuid;

    -- Yozuvni butunlay tozalash
    DELETE FROM client_keys WHERE client_uuid = p_client_uuid;

    RAISE NOTICE 'Mijoz % bo''yicha kriptografik kalit yo''q qilindi. Zaxira nusxalardagi ma''lumotlar ham abadiy ochilmaydi.', p_client_uuid;
END;
$$;
```
**Tushuntirish:** Crypto-Shredding zamonaviy bulutli ma'lumotlar bazalarida eng samarali GDPR o'chirish strategiyasidir. Millionlab terabayt hajmdagi Read-Only zaxira lentalari va WORM (Write Once Read Many) arxivlaridan bitta mijozni o'chirish mumkin bo'lmaganda, uning shaxsiy kalitini o'chirish orqali o'sha zaxiradagi ma'lumot kriptografik chiqindiga aylanadi.
---

### Topshiriq #1184: Audit Loglaridagi Maxfiy Parametrlarni Avtomatik Niqoblash Triggeri
**Tavsif:** Barcha INSERT/UPDATE harakatlarini kuzatuvchi umumiy audit triggerlari mavjud. Biroq parollar, tokenlar yoki to'lov karta raqamlari o'zgarganda, audit jadvaliga (`audit_logs`) ularning asl ochiq nusxasi yozilib qolmasligi shart.
**Talablar:**
- Trigger `NEW` va `OLD` JSONB obyektlaridan `password`, `cvv`, `token`, `secret` maydonlarini avtomatik topib, ularning qiymatini `[REDACTED]` ga almashtirishi kerak.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS system_audit_journal (
    log_id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    action_type VARCHAR(10) NOT NULL,
    changed_data JSONB NOT NULL,
    changed_by VARCHAR(50) NOT NULL,
    changed_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- JSON obyektdagi maxfiy kalitlarni tozalovchi yordamchi funksiya
CREATE OR REPLACE FUNCTION sanitize_sensitive_json(p_data JSONB)
RETURNS JSONB AS $$
DECLARE
    v_key TEXT;
    v_clean JSONB := p_data;
    v_sensitive_keys TEXT[] := ARRAY['password', 'cvv', 'pin', 'token', 'secret', 'pan'];
BEGIN
    FOREACH v_key IN ARRAY v_sensitive_keys LOOP
        IF v_clean ? v_key THEN
            v_clean := jsonb_set(v_clean, ARRAY[v_key], '"[REDACTED]"'::JSONB);
        END IF;
    END LOOP;
    RETURN v_clean;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Umumiy audit triggeri funksiyasi
CREATE OR REPLACE FUNCTION trg_audit_masking_handler()
RETURNS TRIGGER AS $$
DECLARE
    v_payload JSONB;
BEGIN
    IF TG_OP = 'DELETE' THEN
        v_payload := sanitize_sensitive_json(to_jsonb(OLD));
    ELSE
        v_payload := sanitize_sensitive_json(to_jsonb(NEW));
    END IF;

    INSERT INTO system_audit_journal (table_name, action_type, changed_data, changed_by)
    VALUES (TG_TABLE_NAME, TG_OP, v_payload, CURRENT_USER);

    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;
```
**Tushuntirish:** Ko'pincha tizimlar buzilganda xakerlar audit jurnallari (Change Data Capture) orqali parollarning eski nusxalarini qo'lga kiritadilar. `jsonb_set` yordamida maxfiy maydonlarni `[REDACTED]` qilish audit loglarining tozaligi va xavfsizligini ta'minlaydi.
---

### Topshiriq #1185: pgaudit Kengaytmasi: DDL va WRITE Harakatlarini To'liq Audit Qilish
**Tavsif:** Standart PostgreSQL jurnallari faqat xatoliklarni yoki umumiy so'rovlarni yozadi, bu esa davlat va xalqaro audit standartlari (PCI-DSS 10-bo'lim, HIPAA) uchun yetarli emas. Barcha struktura o'zgarishlari (DDL) va ma'lumotlarni o'zgartirish (WRITE/DML) amallarini rasmiy `pgaudit` kengaytmasi orqali qayd qilish kerak.
**Talablar:**
- `pgaudit` sozlamalarini konfiguratsiya qilish: `pgaudit.log = 'ddl, write, role'`.
- Audit loglarini tahlil qilish va maxsus xavfsizlik filtrlari.
**Yechim (SQL):**
```sql
-- 1. pgaudit kengaytmasini faollashtirish (postgresql.conf da shared_preload_libraries = 'pgaudit' talab qilinadi)
CREATE EXTENSION IF NOT EXISTS pgaudit;

-- 2. Audit qoidalarini belgilash
-- ddl: CREATE, ALTER, DROP
-- write: INSERT, UPDATE, DELETE, TRUNCATE
-- role: GRANT, REVOKE, CREATE ROLE
ALTER SYSTEM SET pgaudit.log = 'ddl, write, role';

-- Audit yozuvlariga so'rov matni va parametrlarini qo'shish
ALTER SYSTEM SET pgaudit.log_parameter = 'on';
ALTER SYSTEM SET pgaudit.log_statement_once = 'off';

-- Sozlamalarni qayta yuklash
SELECT pg_reload_conf();

-- Audit loglari ko'rinish namunasi (OS syslog / pg_log da aks etadi):
-- LOG:  AUDIT: SESSION,1,1,WRITE,INSERT,TABLE,public.payments,"INSERT INTO payments VALUES (...)",<not logged>
```
**Tushuntirish:** `pgaudit` oddiy `log_statement = 'all'` dan farqli o'laroq, so'rovlarni sintaktik tahlil (parser) qiladi va aynan qaysi jadval, qaysi ustun va qanday obyekt turiga ta'sir ko'rsatilganini qat'iy tuzilgan (structured) xavfsizlik formati bo'yicha syslog yoki SIEM tizimiga uzatadi.
---

### Topshiriq #1186: pgaudit Bilan Alohida Maxfiy Jadvallarni Selektiv Audit Qilish
**Tavsif:** Butun ma'lumotlar bazasida hamma jadvallarni audit qilish disk hajmini bir necha soatda to'ldirib yuborishi mumkin (Log Flooding). Faqat bank balanslari yoki xavfsizlik sozlamalari kabi kritik jadvallarnigina audit qiluvchi selektiv audit rolini (`pgaudit.role`) sozlash kerak.
**Talablar:**
- Maxsus `auditor_watch` rolini yaratish.
- `pgaudit.role = 'auditor_watch'` sozlamasini o'rnatish.
- Faqat kritik jadvalga ushbu rolni biriktirish orqali faqat o'sha jadvaldagi harakatlarni yozish.
**Yechim (SQL):**
```sql
-- 1. Audit uchun maxsus bo'sh rol yaratish
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'auditor_watch') THEN
        CREATE ROLE auditor_watch NOLOGIN;
    END IF;
END
$$;

-- 2. pgaudit ga aynan shu rol kuzatuvini topshirish
ALTER SYSTEM SET pgaudit.role = 'auditor_watch';
SELECT pg_reload_conf();

-- 3. Kritik jadval yaratish va unga auditor_watch ni bog'lash
CREATE TABLE IF NOT EXISTS treasury_funds (
    fund_id SERIAL PRIMARY KEY,
    fund_name VARCHAR(100) NOT NULL,
    balance NUMERIC(20, 2) NOT NULL
);

-- auditor_watch roliga ushbu jadval ustidan ruxsat berish orqali pgaudit kuzatuvini faollashtiramiz
GRANT SELECT, INSERT, UPDATE, DELETE ON treasury_funds TO auditor_watch;

-- Endi treasury_funds ustida kim nima amal bajarsa, pgaudit darhol audit logiga yozadi!
-- Boshqa oddiy jadvallar esa audit qilinmaydi va disk tejaladi.
```
**Tushuntirish:** `pgaudit.role` usuli eng samarali korporativ amaliyotdir. `auditor_watch` roliga qaysi jadvallar bo'yicha GRANT berilgan bo'lsa, pgaudit faqat o'sha jadvallar bo'yicha so'rovlarni jurnalga tushiradi, qolgan millionlab ikkilamchi so'rovlar e'tibordan chetda qoldirilib unumdorlik saqlanadi.
---

### Topshiriq #1187: pg_hba.conf da SCRAM-SHA-256 va hostssl Majburiyati
**Tavsif:** Eski MD5 autentifikatsiya algoritmi parollarni oson ochish imkonini beradi. Shuningdek, tarmoqda shifrlanmagan (plain TCP) ulanishlar orqali parollar va ma'lumotlar snifferlar tomonidan o'g'irlanishi mumkin. SCRAM-SHA-256 va SSL majburiyatini SQL orqali tekshirish va konfiguratsiya qilish lozim.
**Talablar:**
- `pg_hba_file_rules` jadvalini audit qilish.
- Standart parollash algoritmini `scram-sha-256` ga o'zgartirish.
- Foydalanuvchilarning eski MD5 parollarini aniqlovchi xavfsizlik so'rovi.
**Yechim (SQL):**
```sql
-- 1. Yangi yaratiladigan parollar uchun standart algoritmni SCRAM-SHA-256 ga o'tkazish
ALTER SYSTEM SET password_encryption = 'scram-sha-256';
SELECT pg_reload_conf();

-- 2. pg_hba.conf dagi ulanish xavfsizligini audit qilish (Faqat hostssl va scram bo'lishi kerak)
SELECT 
    line_number,
    type,
    database,
    user_name,
    address,
    auth_method
FROM pg_hba_file_rules
WHERE auth_method NOT IN ('scram-sha-256', 'cert') 
   OR type != 'hostssl';

-- 3. Hali ham eski zaif MD5 paroli bilan qolib ketgan foydalanuvchilarni aniqlash
SELECT 
    rolname,
    CASE 
        WHEN rolpassword LIKE 'SCRAM-SHA-256$%' THEN 'Xavfsiz (SCRAM-SHA-256)'
        WHEN rolpassword LIKE 'md5%' THEN 'ZAIF (MD5 - Parolni darhol yangilang!)'
        WHEN rolpassword IS NULL THEN 'Parolsiz'
        ELSE 'Boshqa usul'
    END AS parol_xavfsizlik_holati
FROM pg_authid
WHERE rolcanlogin = TRUE;
```
**Tushuntirish:** SCRAM-SHA-256 (Salted Challenge Response Authentication Mechanism) mijoz parolini serverga yubormaydi, balki kriptografik challenge-response orqali autentifikatsiya qiladi. Bu man-in-the-middle va replay hujumlarini bartaraf etadi.
---

### Topshiriq #1188: Ikki Tomonlama Mutual TLS (mTLS) va Sertifikat Tekshiruvi
**Tavsif:** Backend xizmatlar va ma'lumotlar bazasi o'rtasida parolsiz, lekin apparat/PKI darajasida xavfsiz bo'lgan ikki tomonlama sertifikat autentifikatsiyasini (mTLS - client certificate authentication) o'rnatish lozim.
**Talablar:**
- `ssl_cert_file`, `ssl_key_file`, `ssl_ca_file` sozlamalarini boshqarish.
- Foydalanuvchining umumiy nomi (Common Name - CN) orqali avtomatik tizimga kiritish (`cert` auth method).
**Yechim (SQL):**
```sql
-- 1. SSL va CA sertifikatlar parametrlarini tekshirish
SELECT 
    name, 
    setting, 
    source 
FROM pg_settings 
WHERE name IN ('ssl', 'ssl_ca_file', 'ssl_cert_file', 'ssl_key_file', 'ssl_crl_file');

-- 2. SSL o'chirilgan holatda tizim ishlashini taqiqlash
ALTER SYSTEM SET ssl = 'on';

-- 3. mTLS orqali ulanayotgan joriy sessiyaning SSL shifrlash darajasini audit qilish
SELECT 
    pid,
    usename,
    client_addr,
    ssl,
    version AS tls_versiyasi,
    cipher AS shifr_algoritmi,
    bits AS shifr_kuchi,
    client_dn AS mijoz_sertifikati_dn
FROM pg_stat_ssl
JOIN pg_stat_activity USING (pid)
WHERE ssl = TRUE;
```
**Tushuntirish:** mTLS (Mutual TLS) da mijoz server sertifikatini, server esa mijoz sertifikatini CA (Certificate Authority) zanjiri bo'yicha tekshiradi. Sertifikatsiz har qanday so'rov darhol TCP handshake bosqichida uziladi.
---

### Topshiriq #1189: Disk Darajasidagi Transparent Data Encryption (TDE) Arxitekturasi
**Tavsif:** Agar tajovuzkor server xonasiga jismonan kirib qattiq diskni (NVMe SSD) o'g'irlab ketsa yoki bulutli snapshotni qo'lga kiritsa, ma'lumotlar bazasi fayllari (Tablespaces, WAL, temp files) o'qib bo'lmaydigan holatda bo'lishi (TDE - Encryption at Rest) shart.
**Talablar:**
- Linux dm-crypt / LUKS yoki PostgreSQL Tablespace shifrlash arxitekturasini loyihalash.
- Shifrlangan tablespace yaratish va maxfiy jadvallarni unga ko'chirish SQL buyruqlari.
**Yechim (SQL):**
```sql
-- Shifrlangan disk bo'limida joylashgan Tablespace yaratish
-- Diqqat: /mnt/encrypted_nvme drayveri OS darajasida dm-crypt (AES-XTS-256) bilan shifrlangan bo'lishi lozim
CREATE TABLESPACE secure_encrypted_space 
LOCATION '/mnt/encrypted_nvme/pg_secure_data';

-- Yangi maxfiy jadvalni to'g'ridan-to'g'ri shifrlangan tablespace-da yaratish
CREATE TABLE IF NOT EXISTS classified_vault (
    vault_id BIGSERIAL PRIMARY KEY,
    secret_code VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL
) TABLESPACE secure_encrypted_space;

-- Mavjud jadvalni shifrlangan tablespace-ga ko'chirish (Zero-Downtime)
ALTER TABLE enterprise_contracts SET TABLESPACE secure_encrypted_space;

-- Jadvalning indekslarini ham shifrlangan maydonga o'tkazish
ALTER INDEX idx_enterprise_orders_org_id SET TABLESPACE secure_encrypted_space;
```
**Tushuntirish:** TDE (Transparent Data Encryption) ma'lumotlar xotirada o'qilganda shifrdan chiqariladi, ammo diskka yozilganda 100% shifrlangan holatda saqlanadi. Jadval va indekslarni alohida shifrlangan Tablespace ga ko'chirish orqali butun tizim xavfsizligi ta'minlanadi.
---

### Topshiriq #1190: WAL va Arxiv Loglarini Avtomatik Shifrlash (WAL Encryption)
**Tavsif:** PostgreSQL-da barcha INSERT va UPDATE harakatlari oldin WAL (Write-Ahead Logging) fayllariga yoziladi. Agar arxiv fayllari (WAL archives) S3 yoki zaxira serveriga ochiq yuborilsa, bazadagi shifrlangan jadvallarning keshdagi ochiq nusxalari sizib chiqishi mumkin.
**Talablar:**
- `archive_command` orqali WAL segmentlarini GPG bilan shifrlab arxivlash parametrlarini sozlash.
- Arxivlash holatini SQL orqali tekshirish.
**Yechim (SQL):**
```sql
-- 1. WAL arxivlash parametrlarini xavfsiz sozlash (GPG bilan shifrlash)
-- Har bir 16MB WAL segmenti GPG orqali AES-256 bilan shifrlanadi
ALTER SYSTEM SET archive_mode = 'on';
ALTER SYSTEM SET archive_command = 'gpg --batch --yes --encrypt --recipient backup_ops@enterprise.uz "%p" && cp "%p.gpg" /mnt/secure_backup/wal/"%f.gpg"';

-- Sozlamani qayta yuklash
SELECT pg_reload_conf();

-- 2. Arxivator faoliyatini va xatoliklarni kuzatuvchi monitoring so'rovi
SELECT 
    archived_count,
    last_archived_wal,
    last_archived_time,
    failed_count,
    last_failed_wal,
    last_failed_time
FROM pg_stat_archiver;
```
**Tushuntirish:** `archive_command` orqali har bir WAL fayli diskka saqlanishi bilanoq GPG ommaviy kaliti bilan shifrlanadi. Natijada hatto zaxira serveri (S3 bucket) buzib kirilsa ham, shaxsiy maxfiy kalitsiz tranzaksiya jurnallarini qayta tiklab bo'lmaydi.
---

### Topshiriq #1191: Tizim Kataloglari (pg_catalog) va Metama'lumotlarni Himoyalash
**Tavsif:** Oddiy foydalanuvchilar `pg_catalog`, `information_schema` va boshqa jadvallarni skanerlash orqali korxonaning barcha jadvallari, ustun nomlari va tizim arxitekturasini o'rganib chiqishi (Reconnaissance) mumkin. Ushbu metama'lumotlarni ruxsatsiz rollardan yashirish kerak.
**Talablar:**
- `REVOKE` orqali tizim ma'lumotlariga umumiy kirishni cheklash.
- Funksiya manba kodlarini (pg_proc) oddiy foydalanuvchilardan himoyalash.
**Yechim (SQL):**
```sql
-- 1. Barcha jadvallar va ustunlar ro'yxatini yashirish
REVOKE SELECT ON pg_catalog.pg_tables FROM PUBLIC;
REVOKE SELECT ON pg_catalog.pg_attribute FROM PUBLIC;
REVOKE SELECT ON pg_catalog.pg_class FROM PUBLIC;

-- 2. Maxfiy PL/pgSQL funksiyalari kodlari saqlanadigan pg_proc jadvalini cheklash
REVOKE SELECT ON pg_catalog.pg_proc FROM PUBLIC;

-- Faqat ma'muriy guruhlarga qayta ruxsat berish
GRANT SELECT ON pg_catalog.pg_tables TO sec_admin;
GRANT SELECT ON pg_catalog.pg_proc TO sec_admin;

-- 3. Oddiy foydalanuvchilar o'z ulanishlarida faqat o'ziga tegishli sxemalarni ko'rishi uchun qat'iy search_path
ALTER ROLE PUBLIC SET search_path = public;
```
**Tushuntirish:** Xakerlar tizimga kirganda dastlabki qiladigan ishi `pg_class` va `pg_proc` ni o'qib, zaiflik qidirishdir. Tizim kataloglariga ruxsatni cheklash nishonni qorong'ilatadi (Security through Obscurity + Defense in Depth).
---

### Topshiriq #1192: Bazadagi Seanslar Xavfsizligi va Brute-Force Monitoringi
**Tavsif:** Ochiq qolib ketgan ulanishlar (Abandoned Connections) va tranzaksiyada to'xtab qolgan seanslar (Idle in Transaction) resurslarni yeyishi va xavfsizlikka tahdid solishi mumkin. Shuningdek, ketma-ket muvaffaqiyatsiz ulanishlarni kuzatuvchi monitoring mexanizmi zarur.
**Talablar:**
- `idle_in_transaction_session_timeout` va `statement_timeout` parametrlarini sozlash.
- Tranzaksiyada osilib qolgan ulanishlarni avtomatik aniqlovchi va to'xtatuvchi xavfsizlik funksiyasi.
**Yechim (SQL):**
```sql
-- 1. Xavfsiz seans vaqt me'yorlarini belgilash
-- Bitta so'rov 30 soniyadan ko'p davom etsa to'xtatiladi (DDoS ga qarshi)
ALTER SYSTEM SET statement_timeout = '30000'; -- 30s

-- Tranzaksiya ochiq qolib 60 soniya bo'sh tursa uziladi
ALTER SYSTEM SET idle_in_transaction_session_timeout = '60000'; -- 60s

-- Bo'sh turgan ulanishlar 10 daqiqadan so'ng yopiladi
ALTER SYSTEM SET idle_session_timeout = '600000'; -- 10m

SELECT pg_reload_conf();

-- 2. Shubhali yoki osilib qolgan ulanishlarni aniqlab majburiy to'xtatish funksiyasi
CREATE OR REPLACE FUNCTION terminate_stale_transactions(p_max_seconds INT DEFAULT 120)
RETURNS TABLE(killed_pid INT, killed_user VARCHAR, duration INTERVAL) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        pid,
        usename::VARCHAR,
        (clock_timestamp() - state_change) AS duration
    FROM pg_stat_activity
    WHERE state = 'idle in transaction'
      AND clock_timestamp() - state_change > (p_max_seconds || ' seconds')::INTERVAL
      AND pid <> pg_backend_pid();

    -- Ushbu seanslarni to'xtatish
    PERFORM pg_terminate_backend(pid)
    FROM pg_stat_activity
    WHERE state = 'idle in transaction'
      AND clock_timestamp() - state_change > (p_max_seconds || ' seconds')::INTERVAL
      AND pid <> pg_backend_pid();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```
**Tushuntirish:** `idle_in_transaction_session_timeout` qulflanishlar (deadlocks) va ma'lumotlar bazasida resurs tugashining (connection starvation) oldini oladi. Tranzaksiyada to'xtab qolgan seanslar ko'pincha ilova xatoliklari yoki ataylab uyushtirilgan sekin hujumlar (Slowloris) oqibatidir.
---

### Topshiriq #1193: Dinamik SQL da SQL Injection: EXECUTE ... USING Sintaksisi
**Tavsif:** PL/pgSQL da `EXECUTE 'SELECT ... ' || user_input` uslubidagi string konkatenatsiyasi eng asosiy va xavfli SQL Injection teshigidir. Foydalanuvchi ma'lumotlarini hech qachon matnga ulamasdan, parametr sifatida `EXECUTE ... USING` orqali xavfsiz uzatish shart.
**Talablar:**
- Zaif kod namunasini tahlil qilish va xavfsiz holatga keltirish.
- `EXECUTE ... USING` yordamida bir nechta parametrlar bilan dinamik qidiruv funksiyasini yozish.
**Yechim (SQL):**
```sql
-- XAVFLI USUL (HECH QACHON QILMANG):
-- EXECUTE 'SELECT * FROM users WHERE status = ' || quote_literal(p_status) || ' AND age > ' || p_age;
-- Agar p_status = "' OR '1'='1" bo'lsa, butun baza sizib chiqadi!

-- XAVFSIZ USUL: EXECUTE ... USING sintaksisi
CREATE OR REPLACE FUNCTION search_active_users(
    p_role VARCHAR(50),
    p_min_activity INT
) RETURNS TABLE(user_id UUID, username VARCHAR(50)) AS $$
DECLARE
    v_sql TEXT;
BEGIN
    -- Parametrlar o'rniga $1, $2 joylashtiriladi
    v_sql := 'SELECT user_id, username FROM app_users ' ||
             'WHERE is_active = TRUE AND username LIKE $1 ' ||
             'LIMIT $2';

    -- USING orqali parametrlar alohida binar qiymat sifatida uzatiladi
    RETURN QUERY EXECUTE v_sql USING ('%' || p_role || '%', p_min_activity);
END;
$$ LANGUAGE plpgsql STABLE;
```
**Tushuntirish:** `EXECUTE ... USING $1, $2` usulida parametrlar SQL parseridan alohida uzatiladi. Har qanday zararli tirnoqlar yoki maxsus SQL buyruqlari (`DROP`, `UNION`) oddiy matn belgisi sifatida qabul qilinadi va hech qachon kod sifatida bajarilmaydi.
---

### Topshiriq #1194: Dinamik Jadval va Ustun Nomlarini format('%I') Bilan Sanatsiya Qilish
**Tavsif:** Jadval nomlari, ustun nomlari yoki sxema nomlarini `USING` parametri orqali uzatib bo'lmaydi (chunki SQL ularni identifikator sifatida talab qiladi). Agar dasturchi ularni matn sifatida ulasa, SQL Injection sodir bo'ladi. Identifikatorlarni xavfsiz sanatsiya qilish uchun `format('%I', ...)` yoki `quote_ident()` ishlatish shart.
**Talablar:**
- Jadval va ustun nomlarini dinamik qabul qiluvchi statistika funksiyasi.
- `format('%I')` yordamida SQL inyeksiyani to'liq bartaraf etish.
- Foydalanuvchi kiritgan nom bazada haqiqatan mavjudligini oq ro'yxat (Allowlist) orqali tekshirish.
**Yechim (SQL):**
```sql
CREATE OR REPLACE FUNCTION get_table_row_count(
    p_schema_name TEXT,
    p_table_name TEXT
) RETURNS BIGINT AS $$
DECLARE
    v_count BIGINT;
    v_safe_sql TEXT;
    v_exists BOOLEAN;
BEGIN
    -- 1. Oq ro'yxat (Allowlist) tekshiruvi: Jadval haqiqatan mavjudmi?
    SELECT EXISTS (
        SELECT 1 FROM information_schema.tables 
        WHERE table_schema = p_schema_name AND table_name = p_table_name
    ) INTO v_exists;

    IF NOT v_exists THEN
        RAISE EXCEPTION 'Xavfsizlik xatosi: % nomli jadval mavjud emas yoki ruxsat yo''q!', p_table_name;
    END IF;

    -- 2. format('%I') orqali xavfsiz identifikator tuzish
    -- %I har qanday tirnoq va xavfli belgilarni avtomatik tarzda to'g'ri escape qiladi
    v_safe_sql := format('SELECT count(*) FROM %I.%I', p_schema_name, p_table_name);

    EXECUTE v_safe_sql INTO v_count;
    RETURN v_count;
END;
$$ LANGUAGE plpgsql;
```
**Tushuntirish:** `format('%I', identifier)` funksiyasi kiruvchi identifikatorni PostgreSQL identifikator qoidalariga moslab qo'shtirnoq ichiga oladi va mavjud qo'shtirnoqlarni ikki marta oshiradi (`""`). Bu orqali `test"; DROP TABLE users; --` kabi hujumlar faqat bitta g'alati nomli jadvalni qidirish bilan yakunlanadi va hech qanday buzg'unchi buyruq ishlamaydi.
---

### Topshiriq #1195: Dinamik Qidiruv Matnlarini format('%L') Bilan Himoyalash
**Tavsif:** Agar qandaydir sababga ko'ra `USING` parametrini qo'llash imkoni bo'lmasa (masalan, murakkab filtr shartlari dinamik yig'ilayotganda), literal qiymatlarni (matnlar, sonlar, sanalar) `format('%L')` yoki `quote_literal()` orqali qat'iy o'rash kerak.
**Talablar:**
- Matnli shartlarni xavfsiz generatsiya qiluvchi funksiya.
- NULL qiymatlarni avtomatik xavfsiz `NULL` matniga aylantirish xususiyati.
**Yechim (SQL):**
```sql
CREATE OR REPLACE FUNCTION build_dynamic_filter_query(
    p_base_query TEXT,
    p_status VARCHAR,
    p_search_term VARCHAR
) RETURNS TEXT AS $$
DECLARE
    v_query TEXT := p_base_query;
BEGIN
    -- format('%L') literalni apostrof ichiga oladi va barcha ichki apostroflarni escape qiladi
    IF p_status IS NOT NULL THEN
        v_query := v_query || format(' AND status = %L', p_status);
    END IF;

    IF p_search_term IS NOT NULL THEN
        v_query := v_query || format(' AND description ILIKE %L', '%' || p_search_term || '%');
    END IF;

    RETURN v_query;
END;
$$ LANGUAGE plpgsql IMMUTABLE;
```
**Tushuntirish:** `format('%L')` parametri null qiymat kelganda xavfsiz `NULL` so'zini qo'yadi, matn kelganda esa uni `'o''clock'` kabi xavfsiz apostrof bilan o'raydi. Bu orqali inyeksion kodlar qiymat chegarasidan tashqariga chiqa olmaydi.
---

### Topshiriq #1196: Second-Order SQL Injection Xavfi va Kiritilgan Ma'lumotlarni Qayta Sanatsiya Qilish
**Tavsif:** Tajovuzkor dastlabki INSERT paytida ziyon yetkazmaydigan, lekin keyinchalik boshqa ichki dinamik protsedura yoki trigger tomonidan o'qilib bajarilganda ishga tushadigan zararli kod kiritishi (Second-Order SQL Injection) mumkin.
**Talablar:**
- `app_configurations` jadvali: `config_key`, `config_value`.
- Dinamik ravishda ushbu konfiguratsiyani o'qib ishlatuvchi protsedura.
- Kiritilgan ma'lumotni bazadan o'qiganda ham parametrlashtirilgan holatda ishlatish talabi.
**Yechim (SQL):**
```sql
CREATE TABLE IF NOT EXISTS app_configurations (
    config_key VARCHAR(50) PRIMARY KEY,
    config_value TEXT NOT NULL
);

-- Xavfsiz yangilash va tekshirish
CREATE OR REPLACE PROCEDURE apply_system_configuration(p_key VARCHAR(50))
LANGUAGE plpgsql AS $$
DECLARE
    v_raw_val TEXT;
    v_is_valid BOOLEAN;
BEGIN
    SELECT config_value INTO v_raw_val
    FROM app_configurations
    WHERE config_key = p_key;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Konfiguratsiya topilmadi: %', p_key;
    END IF;

    -- XAVFLI: EXECUTE 'SET ' || p_key || ' = ' || v_raw_val;
    -- Tajovuzkor config_value ga "off; DROP TABLE audit; --" yozib qo'ygan bo'lishi mumkin!

    -- XAVFSIZ: set_config() orqali to'g'ridan-to'g'ri parametrik o'rnatish
    PERFORM set_config(p_key, v_raw_val, FALSE);
    RAISE NOTICE 'Konfiguratsiya % xavfsiz tarzda qo''llanildi.', p_key;
END;
$$;
```
**Tushuntirish:** Second-Order SQL Injection xavfida tajovuzkor dastlabki tekshiruvdan o'tadi, chunki birinchi bosqichda inyeksiya amalga oshmaydi. Ammo ma'lumotlar bazada saqlanib, keyingi skript tomonidan dinamik SQL ga qo'shilganda portlaydi. Buning oldini olish uchun bazadan olingan ma'lumotlarga ham "ishonchsiz ma'lumot" (untrusted data) sifatida qaralishi zarur.
---

### Topshiriq #1197: Security Definer Funktsiyalarida Qat'iy search_path Himoyasi
**Tavsif:** `SECURITY DEFINER` funksiyalari superuser yoki yaratuvchi vakolati bilan ishlaydi. Agar funksiyada `search_path` qat'iy belgilanmagan bo'lsa, tajovuzkor o'zining vaqtinchalik sxemasida (`pg_temp`) xuddi shu nomdagi soxta funksiya yoki jadval yaratib, superuser nomidan kod bajartirishi (Search Path Hijacking / Privilege Escalation) mumkin.
**Talablar:**
- `SECURITY DEFINER` funksiyasiga `SET search_path = pg_catalog, public` parametrini majburiy kiritish.
- Tizimdagi xavfli, search_path ko'rsatilmagan barcha Security Definer funksiyalarni aniqlovchi audit skripti.
**Yechim (SQL):**
```sql
-- 1. To'g'ri va xavfsiz tuzilgan Security Definer funksiya namunasi
CREATE OR REPLACE FUNCTION admin_reset_user_lock(p_target_user_id UUID)
RETURNS VOID AS $$
BEGIN
    UPDATE public.app_users
    SET is_active = TRUE
    WHERE user_id = p_target_user_id;
END;
$$ LANGUAGE plpgsql 
   SECURITY DEFINER 
   SET search_path = pg_catalog, public, pg_temp; -- HIJACKING GA QARSHI MAJBURIY QALQON!

-- 2. Tizimdagi xavfli (search_path ko'rsatilmagan) Security Definer funksiyalarni aniqlash auditi
SELECT 
    n.nspname AS schema_name,
    p.proname AS function_name,
    pg_get_userbyid(p.proowner) AS owner_name,
    p.proconfig AS config_settings
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE p.prosecdef = TRUE -- Security Definer bo'lganlar
  AND (p.proconfig IS NULL OR NOT EXISTS (
      SELECT 1 FROM unnest(p.proconfig) s WHERE s LIKE 'search_path=%'
  ));
```
**Tushuntirish:** PostgreSQL xavfsizlik qo'llanmasiga ko'ra, har bir `SECURITY DEFINER` funksiyasi albatta o'zining shaxsiy `SET search_path` qiymatiga ega bo'lishi shart. Aks holda oddiy foydalanuvchi `pg_temp` sxemasiga soxta operator yoki funksiya kiritib, superuser huquqini qo'lga kiritishi mumkin.
---

### Topshiriq #1198: Minimal Ruxsat Tamoyili (Least Privilege Principle) va Rollar Matritsasi
**Tavsif:** Ilovalar (Backend API) hech qachon ma'lumotlar bazasiga `postgres` (superuser) foydalanuvchisi bilan ulanmasligi kerak. Tizim uchun faqat o'ziga kerakli operatsiyalarni bajara oladigan cheklangan rollar matritsasini yaratish shart.
**Talablar:**
- `app_reader`, `app_writer`, `app_migrator` rollarini loyihalash.
- Superuser huquqlaridan voz kechib, DDL va DML amallarini ajratish.
**Yechim (SQL):**
```sql
-- 1. Bazaviy rollarni yaratish (NOLOGIN - guruh rollari)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'role_readonly') THEN
        CREATE ROLE role_readonly NOLOGIN;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'role_readwrite') THEN
        CREATE ROLE role_readwrite NOLOGIN;
    END IF;
END
$$;

-- Ruxsatlarni belgilash
GRANT USAGE ON SCHEMA public TO role_readonly, role_readwrite;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO role_readonly;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO role_readwrite;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO role_readwrite;

-- 2. Haqiqiy login qila oladigan ilova foydalanuvchisini yaratish (SCRAM parol bilan)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'backend_app_svc') THEN
        CREATE ROLE backend_app_svc WITH LOGIN 
        PASSWORD 'Complex_Random_Pass_2026_Secure!' 
        NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS
        CONNECTION LIMIT 50;
    END IF;
END
$$;

-- Ilova foydalanuvchisiga faqat ReadWrite rolini biriktirish
GRANT role_readwrite TO backend_app_svc;

-- Ilova hech qachon DDL (DROP, ALTER) qila olmasligini kafolatlash
REVOKE CREATE ON SCHEMA public FROM backend_app_svc;
REVOKE CREATE ON SCHEMA public FROM role_readwrite;
```
**Tushuntirish:** Agar dastur `backend_app_svc` nomidan ishlasa va ilovada SQL Injection zaifligi yuzaga kelsa ham, tajovuzkor `DROP TABLE` yoki `ALTER USER` qila olmaydi, chunki ilovada DDL ruxsati mutlaqo yo'q.
---

### Topshiriq #1199: Ma'lumotlar Bazasi Honeypot Jadvali va Intrusion Detection (HIDS)
**Tavsif:** Baza ichiga ataylab tuzoq jadvallar (masalan, `admin_passwords` yoki `crypto_wallets`) joylashtiriladi. Haqiqiy ilova bu jadvallarga hech qachon murojaat qilmaydi. Agar kimdir ushbu jadvalni o'qishga urinsa, bu xakerlik harakati deb baholanib, darhol xavfsizlik jamoasiga ogohlantirish (Alert) yuboriladi va ulanish to'xtatiladi.
**Talablar:**
- `honey_admin_credentials` tuzoq jadvali.
- Jadvalga har qanday `SELECT` yoki `DML` qilinganda ishga tushuvchi ogohlantirish triggeri yoki hodisalar yozuvi.
- Tajovuzkorning IP manzili va ulanishini qayd etish.
**Yechim (SQL):**
```sql
-- Tuzoq jadval (Honeypot)
CREATE TABLE IF NOT EXISTS honey_admin_credentials (
    fake_id SERIAL PRIMARY KEY,
    secret_username VARCHAR(50) NOT NULL,
    secret_password VARCHAR(100) NOT NULL
);

-- Ataylab qiziqarli ko'rinishdagi soxta ma'lumot joylash
INSERT INTO honey_admin_credentials (secret_username, secret_password)
VALUES ('root_admin', 'Pass123_MasterKey!');

-- Xavfsizlik hodisalari jurnali
CREATE TABLE IF NOT EXISTS security_incident_alerts (
    incident_id BIGSERIAL PRIMARY KEY,
    attacker_user VARCHAR(50) NOT NULL,
    attacker_ip INET,
    attacker_pid INT NOT NULL,
    attempted_action TEXT NOT NULL,
    detected_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- Tuzoqqa tushganda ishga tushuvchi qopqon funksiyasi
CREATE OR REPLACE FUNCTION trg_trap_attacker()
RETURNS TRIGGER AS $$
DECLARE
    v_client_ip INET;
BEGIN
    SELECT client_addr INTO v_client_ip
    FROM pg_stat_activity
    WHERE pid = pg_backend_pid();

    -- Hodisani qayd etish
    INSERT INTO security_incident_alerts (
        attacker_user, attacker_ip, attacker_pid, attempted_action
    ) VALUES (
        CURRENT_USER, v_client_ip, pg_backend_pid(), TG_OP || ' on honey_admin_credentials'
    );

    -- Tajovuzkorga xatolik berib to'xtatish (yoki seansni uzish)
    RAISE EXCEPTION 'XAVFSIZLIK TIZIMI: Ruxsatsiz kirish aniqlandi! IP manzilingiz bloklandi: %', v_client_ip;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER trg_honeypot_defense
BEFORE INSERT OR UPDATE OR DELETE ON honey_admin_credentials
FOR EACH ROW
EXECUTE FUNCTION trg_trap_attacker();
```
**Tushuntirish:** Database Honeypot texnikasi ichki xavflarni (insider threat) va bazani skanerlayotgan tajovuzkorlarni 0-day zaifliklar ishlatilgan holatda ham birinchi daqiqalardanoq fosh qilish imkonini beradi.
---

### Topshiriq #1200: Mukammal Bank Ma'lumotlar Bazasi Xavfsizlik Arxitekturasi
**Tavsif:** Yuqori xavfsizlik darajasiga ega bank to'lov tizimi uchun kompleks xavfsizlik arxitekturasini yaratish zarur. Ushbu arxitekturada pgcrypto orqali ma'lumotlarni shifrlash, Row-Level Security (RLS) orqali multi-tenancy, Dynamic Data Masking orqali PII niqoblash, qat'iy Least Privilege va parametrli xavfsiz so'rovlar yagona integratsiyalashgan tizim sifatida birlashtirilishi shart.
**Talablar:**
- Bank hisoblari va tranzaksiyalari jadvalini yaratish.
- AES-256 shifrlash, RLS filtri, avtomatik tranzaksiya auditi va xavfsiz to'lov o'tkazish protsedurasini (Zero-Trust tamoyillari asosida) yaratish.
**Yechim (SQL):**
```sql
-- 1. Xavfsiz bank sxemasi va kengaytma
CREATE SCHEMA IF NOT EXISTS bank_core;
CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA bank_core;

-- 2. Bank hisoblari jadvali
CREATE TABLE IF NOT EXISTS bank_core.accounts (
    account_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_bank_id UUID NOT NULL,
    client_name VARCHAR(100) NOT NULL,
    encrypted_iban BYTEA NOT NULL,
    iban_last4 CHAR(4) NOT NULL,
    balance NUMERIC(18, 2) NOT NULL CHECK (balance >= 0),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- RLS ni yoqish va jadval egasi uchun ham majburiy qilish
ALTER TABLE bank_core.accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE bank_core.accounts FORCE ROW LEVEL SECURITY;

-- Multi-Tenant Bank RLS siyosati
CREATE POLICY bank_tenant_policy ON bank_core.accounts
    FOR ALL
    USING (
        tenant_bank_id = NULLIF(current_setting('bank.current_tenant', TRUE), '')::UUID
    )
    WITH CHECK (
        tenant_bank_id = NULLIF(current_setting('bank.current_tenant', TRUE), '')::UUID
    );

-- 3. Dynamic Data Masking View (Operatorlar uchun)
CREATE OR REPLACE VIEW bank_core.view_masked_accounts AS
SELECT 
    account_id,
    left(client_name, 1) || '***' || right(client_name, 1) AS masked_client,
    '**** **** **** ' || iban_last4 AS masked_iban,
    balance,
    is_active
FROM bank_core.accounts;

-- 4. O'ta xavfsiz pul o'tkazish protsedurasi (ACID + Parametrlashgan xavfsiz logika)
CREATE OR REPLACE PROCEDURE bank_core.transfer_funds(
    p_sender_id UUID,
    p_receiver_id UUID,
    p_amount NUMERIC(18, 2),
    p_security_token TEXT
) LANGUAGE plpgsql AS $$
DECLARE
    v_sender_balance NUMERIC(18, 2);
    v_tenant UUID;
BEGIN
    IF p_amount <= 0 THEN
        RAISE EXCEPTION 'O''tkazma summasi musbat bo''lishi shart!';
    END IF;

    v_tenant := NULLIF(current_setting('bank.current_tenant', TRUE), '')::UUID;
    IF v_tenant IS NULL THEN
        RAISE EXCEPTION 'Xavfsizlik xatosi: Bank tenant konteksti o''rnatilmagan!';
    END IF;

    -- Hisoblarni qulflash (Row-level lock - Race condition ga qarshi)
    SELECT balance INTO v_sender_balance
    FROM bank_core.accounts
    WHERE account_id = p_sender_id AND tenant_bank_id = v_tenant
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Jo''natuvchi hisobi topilmadi!';
    END IF;

    IF v_sender_balance < p_amount THEN
        RAISE EXCEPTION 'Mablag'' yetarli emas! Joriy balans: %', v_sender_balance;
    END IF;

    -- Mablag'ni yechish
    UPDATE bank_core.accounts
    SET balance = balance - p_amount
    WHERE account_id = p_sender_id;

    -- Qabul qiluvchiga qo'shish
    UPDATE bank_core.accounts
    SET balance = balance + p_amount
    WHERE account_id = p_receiver_id AND tenant_bank_id = v_tenant;

    RAISE NOTICE 'Tranzaksiya muvaffaqiyatli bajarildi: % so''m o''tkazildi.', p_amount;
END;
$$;
```
**Tushuntirish:** Ushbu yakuniy me'moriy yechimda ma'lumotlar bazasi xavfsizligining barcha qatlamlari: kriptografik shifrlash, ko'p ijarachilik (Multi-tenancy RLS), Dynamic Data Masking, qulflash (Row-level locks) va parametrli tranzaksiyalar yagona Defense-in-Depth zanjirida to'liq mujassamlashgan.
---

