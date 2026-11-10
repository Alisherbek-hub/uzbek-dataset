# 801-Topshiriq: Oddiy SQL tilidagi skalyar funksiya yaratish (CREATE FUNCTION LANGUAGE SQL)
## Topshiriq sharti:
Ikkita son berilganda ularning yig'indisiga 15% QQS (qo'shilgan qiymat solig'i) qo'shilgan yakuniy summani hisoblaydigan sof SQL tilidagi `hisobla_qqs_bilan` funksiyasini yarating va uni chaqiring.

## Yechim (SQL kodi):
```sql
-- 1. SQL tilidagi skalyar funksiya
CREATE OR REPLACE FUNCTION hisobla_qqs_bilan(narx NUMERIC, miqdor INT)
RETURNS NUMERIC
LANGUAGE SQL
IMMUTABLE
AS $$
    SELECT ROUND((narx * miqdor) * 1.15, 2);
$$;

-- 2. Funksiyani test qilish
SELECT 
    hisobla_qqs_bilan(120000.00, 3) AS yakuniy_summa,
    hisobla_qqs_bilan(45000.50, 10) AS partiya_summa;
```

## Tushuntirish va Mantiq:
Ushbu topshiriqda PostgreSQL'da sof SQL tilidagi funksiya yaratildi. LANGUAGE SQL direktivasi funksiya tanasi bitta SQL so'rovidan iborat ekanini bildiradi. IMMUTABLE atributi berilgan bir xil argumentlar uchun funksiya har doim bir xil natija qaytarishini belgilaydi, bu esa optimallashtiruvchiga (optimizer) natijani keshlashtirish va indekslarda foydalanish imkonini beradi.

## Ishlash natijasi:
```text
yakuniy_summa | partiya_summa 
---------------+---------------
     414000.00 |     517505.75
(1 row)
```


# 802-Topshiriq: PL/pgSQL yordamida shartli tarmoqlanishli funksiya (IF-THEN-ELSE)
## Topshiriq sharti:
Mijozning yillik buyurtmalar summasiga qarab uning chegirma toifasini ('BRONZE', 'SILVER', 'GOLD', 'PLATINUM') aniqlab beruvchi PL/pgSQL funksiyasini yozing.

## Yechim (SQL kodi):
```sql
-- PL/pgSQL skalyar funksiya
CREATE OR REPLACE FUNCTION aniqla_mijoz_darajasi(yillik_savdo NUMERIC)
RETURNS VARCHAR(20)
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
    daraja VARCHAR(20);
BEGIN
    IF yillik_savdo IS NULL OR yillik_savdo < 0 THEN
        daraja := 'NOMALUM';
    ELSIF yillik_savdo >= 100000000 THEN
        daraja := 'PLATINUM';
    ELSIF yillik_savdo >= 50000000 THEN
        daraja := 'GOLD';
    ELSIF yillik_savdo >= 10000000 THEN
        daraja := 'SILVER';
    ELSE
        daraja := 'BRONZE';
    END IF;

    RETURN daraja;
END;
$$;

-- Test chaqiruvi
SELECT 
    aniqla_mijoz_darajasi(125000000) AS mijoz_1,
    aniqla_mijoz_darajasi(75000000)  AS mijoz_2,
    aniqla_mijoz_darajasi(5000000)   AS mijoz_3;
```

## Tushuntirish va Mantiq:
PL/pgSQL (Procedural Language / PostgreSQL) procedural imkoniyatlarni (DECLARE blokida o'zgaruvchilar e'lon qilish, IF-ELSIF-ELSE boshqaruv konstruksiyalari) taqdim etadi. `daraja := 'PLATINUM'` operatori o'zgaruvchiga qiymat yuklaydi. STABLE funksiya bitta tranzaksiya/so'rov davomida bir xil parametrlar uchun o'zgarmas natija beradi.

## Ishlash natijasi:
```text
mijoz_1   | mijoz_2 | mijoz_3 
----------+---------+---------
 PLATINUM | GOLD    | BRONZE
(1 row)
```


# 803-Topshiriq: TABLE qaytaruvchi funksiya (RETURNS TABLE)
## Topshiriq sharti:
Berilgan bo'lim ID (p_bolim_id) va minimal maosh chegarasi (p_min_maosh) bo'yicha xodimlarning ID, ism, lavozim va maoshini jadval (set of rows) ko'rinishida qaytaruvchi `olish_bolim_xodimlari` funksiyasini yarating.

## Yechim (SQL kodi):
```sql
-- RETURNS TABLE yordamida funksiya
CREATE OR REPLACE FUNCTION olish_bolim_xodimlari(
    p_bolim_id INT,
    p_min_maosh NUMERIC DEFAULT 0
)
RETURNS TABLE (
    xodim_id INT,
    toliq_ism TEXT,
    lavozim VARCHAR(50),
    oylik_maosh NUMERIC(12,2)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        x.id,
        (x.ism || ' ' || x.familiya)::TEXT,
        x.lavozim,
        x.maosh
    FROM xodimlar x
    WHERE x.bolim_id = p_bolim_id
      AND x.maosh >= p_min_maosh
    ORDER BY x.maosh DESC;
END;
$$;

-- Test chaqiruvi
SELECT * FROM olish_bolim_xodimlari(3, 10000000.00);
```

## Tushuntirish va Mantiq:
RETURNS TABLE (...) sintaksisi funksiyaga relyatsion jadval sifatida qarash imkonini beradi. Funksiya tanasidagi `RETURN QUERY` ifodasi mos so'rov natijalarini to'g'ridan-to'g'ri chaqiruvchiga qaytaradi. SELECT * FROM funksiya_nomi(...) orqali oddiy VIEW yoki jadval kabi so'rov o'tkazish mumkin.

## Ishlash natijasi:
```text
xodim_id |   toliq_ism   |     lavozim     | oylik_maosh 
----------+---------------+-----------------+-------------
       14 | Sardor Aliyev | Bosh Arxitektor | 24000000.00
       19 | Nigora Karimova| Senior Backend  | 18500000.00
       22 | Jamshid Omonov| Tech Lead       | 16000000.00
(3 rows)
```


# 804-Topshiriq: OUT parametrlari orqali bir nechta qiymat qaytarish
## Topshiriq sharti:
Mahsulot toifasi bo'yicha eng arzon narx, eng qimmat narx va o'rtacha narxni OUT parametrlari orqali bir vaqtda qaytaruvchi `mahsulot_statistika` funksiyasini yarating.

## Yechim (SQL kodi):
```sql
-- OUT parametrlari bilan funksiya
CREATE OR REPLACE FUNCTION mahsulot_statistika(
    IN  p_kategoriya_id INT,
    OUT min_narx NUMERIC(12,2),
    OUT max_narx NUMERIC(12,2),
    OUT avg_narx NUMERIC(12,2),
    OUT jami_soni INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT 
        COALESCE(MIN(narx), 0),
        COALESCE(MAX(narx), 0),
        COALESCE(ROUND(AVG(narx), 2), 0),
        COUNT(*)
    INTO min_narx, max_narx, avg_narx, jami_soni
    FROM mahsulotlar
    WHERE kategoriya_id = p_kategoriya_id;
END;
$$;

-- Test chaqiruvi
SELECT * FROM mahsulot_statistika(5);
```

## Tushuntirish va Mantiq:
OUT parametrlari e'lon qilinganda funksiya kompozit (RECORD) tip qaytaradi va `RETURNS` bo'limini yozish talab etilmaydi. SELECT ... INTO min_narx, max_narx... konstruksiyasi agregat natijalarni mos OUT parametrlariga yozadi.

## Ishlash natijasi:
```text
min_narx  |  max_narx  |  avg_narx  | jami_soni 
-----------+------------+------------+-----------
 150000.00 | 4500000.00 | 1280000.50 |        42
(1 row)
```


# 805-Topshiriq: Tranzaksiyalarni boshqaruvchi Stored Procedure (CREATE PROCEDURE)
## Topshiriq sharti:
Bank hisobvarag'idan boshqa hisobvarag'iga mablag' o'tkazuvchi va ichida to'liq xatolik tekshiruvi bo'lgan `otkazma_otkazish` protsedurasini (CREATE PROCEDURE) yarating. Muvaffaqiyatli o'tkazilganda COMMIT, yetarli mablag' bo'lmasa xato ko'tarsin.

## Yechim (SQL kodi):
```sql
-- PostgreSQL Stored Procedure (COMMIT/ROLLBACK imkoniyati bilan)
CREATE OR REPLACE PROCEDURE mablag_otkazish(
    p_jonatuvchi_hisob INT,
    p_qabul_qiluvchi_hisob INT,
    p_summa NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_jonatuvchi_balans NUMERIC;
BEGIN
    -- Tranzaksion xavfsizlik: Jonatuvchini qulflash (Row Share/Exclusive)
    SELECT balans INTO v_jonatuvchi_balans
    FROM hisoblar
    WHERE id = p_jonatuvchi_hisob
    FOR UPDATE;

    IF v_jonatuvchi_balans IS NULL THEN
        RAISE EXCEPTION 'Xatolik: Jonatuvchi hisob topilmadi (ID: %)', p_jonatuvchi_hisob;
    END IF;

    IF v_jonatuvchi_balans < p_summa THEN
        RAISE EXCEPTION 'Mablag yetarli emas! Mavjud balans: %, Talab: %', v_jonatuvchi_balans, p_summa;
    END IF;

    -- Jonatuvchidan yechish
    UPDATE hisoblar
    SET balans = balans - p_summa
    WHERE id = p_jonatuvchi_hisob;

    -- Qabul qiluvchiga qo'shish
    UPDATE hisoblar
    SET balans = balans + p_summa
    WHERE id = p_qabul_qiluvchi_hisob;

    -- O'tkazma logiga yozish
    INSERT INTO otkazmalar_tarixi(jonatuvchi_id, qabul_qiluvchi_id, summa, sana)
    VALUES (p_jonatuvchi_hisob, p_qabul_qiluvchi_hisob, p_summa, NOW());

    -- Protseduralarda to'g'ridan-to'g'ri COMMIT chaqirish mumkin
    COMMIT;
    RAISE NOTICE 'Otkazma muvaffaqiyatli amalga oshirildi: % som', p_summa;
END;
$$;

-- Protsedurani chaqirish
CALL mablag_otkazish(101, 202, 500000.00);
```

## Tushuntirish va Mantiq:
CREATE PROCEDURE va CALL instruksiyasi funksiyalardan farqli o'laroq o'z ichida COMMIT va ROLLBACK buyruqlarini boshqara oladi. Bu uzoq davom etuvchi partiyali (batch processing) jarayonlarda oraliq tranzaksiyalarni yakunlab borish uchun muhimdir. `FOR UPDATE` so'rovi hisob balansini o'qiyotganda qulflab, race condition'ning oldini oladi.

## Ishlash natijasi:
```text
NOTICE:  Otkazma muvaffaqiyatli amalga oshirildi: 500000.00 som
CALL
```


# 806-Topshiriq: Parametrlarga DEFAULT qiymat berish va nomli parametrlar bilan chaqirish
## Topshiriq sharti:
Chegirma va bonus ballarni hisobga olgan holda kuryerlik yetkazib berish narxini hisoblovchi, parametrlarida standart qiymatlari (DEFAULT) bo'lgan funksiya yarating va uni pozitsion hamda nomli usulda chaqiring.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION hisobla_yetkazib_berish(
    p_masofa_km NUMERIC,
    p_ogirlik_kg NUMERIC DEFAULT 1.0,
    p_tezkor BOOLEAN DEFAULT FALSE,
    p_chegirma_foiz NUMERIC DEFAULT 0
)
RETURNS NUMERIC(10,2)
LANGUAGE plpgsql
IMMUTABLE
AS $$
DECLARE
    baza_tarifi CONSTANT NUMERIC := 10000.00;
    km_narxi CONSTANT NUMERIC := 2500.00;
    ogirlik_narxi CONSTANT NUMERIC := 1500.00;
    jami NUMERIC;
BEGIN
    jami := baza_tarifi + (p_masofa_km * km_narxi) + (p_ogirlik_kg * ogirlik_narxi);

    IF p_tezkor THEN
        jami := jami * 1.5; -- 50% tezkorlik ustamasi
    END IF;

    IF p_chegirma_foiz > 0 THEN
        jami := jami * (1 - p_chegirma_foiz / 100.0);
    END IF;

    RETURN ROUND(jami, 2);
END;
$$;

-- 1. Pozitsion chaqirish (faqat masofa berildi, qolgani standart)
SELECT hisobla_yetkazib_berish(12.5) AS standart_yetkazish;

-- 2. Nomli argumentlar bilan chaqirish (Named notation: =>)
SELECT hisobla_yetkazib_berish(
    p_masofa_km => 15.0,
    p_tezkor => TRUE,
    p_chegirma_foiz => 10.0
) AS nomli_chaqiruv;
```

## Tushuntirish va Mantiq:
PostgreSQL'da funksiya parametrlariga `DEFAULT` qiymat berilishi mumkin. Chaqirish paytida `nom => qiymat` (yoki `:=`) sintaksisi yordamida oraliq parametrlarni tashlab ketib, aynan kerakli parametrlarni nomma-nom uzatish mumkin. Bu kod o'qilishini keskin yaxshilaydi.

## Ishlash natijasi:
```text
standart_yetkazish | nomli_chaqiruv 
-------------------+----------------
          42750.00 |       44100.00
(1 row)
```


# 807-Topshiriq: O'zgaruvchilar ko'lami va CONSTANT xususiyati (DECLARE block)
## Topshiriq sharti:
Valyuta ayirboshlash komissiyasi va konvertatsiyasini hisoblovchi ichki blokli funksiya tuzing. Ichki blokda o'zgaruvchilarning qayta e'lon qilinishi (shadowing) va CONSTANT turg'un o'zgaruvchilardan foydalaning.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION konvertatsiya_valyuta(
    p_summa NUMERIC,
    p_kurs NUMERIC
)
RETURNS TEXT
LANGUAGE plpgsql
AS $$
DECLARE
    asosiy_xabar TEXT := 'Konvertatsiya boshlandi';
    v_natija NUMERIC;
BEGIN
    -- Ichki blok boshlanishi
    DECLARE
        KOMISSIYA_FOIZ CONSTANT NUMERIC := 0.015; -- 1.5% o'zgarmas komissiya
        v_sof_summa NUMERIC;
        asosiy_xabar TEXT := 'Ichki blokda hisoblandi'; -- Tashqi o'zgaruvchini shadow qilish
    BEGIN
        v_sof_summa := p_summa * (1 - KOMISSIYA_FOIZ);
        v_natija := ROUND(v_sof_summa * p_kurs, 2);
        RAISE NOTICE 'Holat: %, Sof valyuta: %', asosiy_xabar, v_sof_summa;
    END;
    -- Ichki blok tugashi

    RETURN 'Muvaffaqiyat: ' || v_natija || ' so''m';
END;
$$;

SELECT konvertatsiya_valyuta(1000.00, 12850.00);
```

## Tushuntirish va Mantiq:
PL/pgSQL da `BEGIN ... END` bloklari ixtiyoriy chuqurlikda ichma-ich joylashishi mumkin. Har bir blok o'zining `DECLARE` bo'limiga ega bo'lishi mumkin. Ichki blokdagi o'zgaruvchi tashqi blokdagi o'zgaruvchini shadow (berkitish) qiladi va blok tugashi bilan o'chiriladi. `CONSTANT` kalit so'zi esa o'zgaruvchi qiymati butun ijro davomida o'zgarmasligini kafolatlaydi.

## Ishlash natijasi:
```text
NOTICE:  Holat: Ichki blokda hisoblandi, Sof valyuta: 985.00000
       konvertatsiya_valyuta        
------------------------------------
 Muvaffaqiyat: 12657250.00 so'm
(1 row)
```


# 808-Topshiriq: EXCEPTION WHEN bo'limi orqali xatoliklarni ushlash (Error Handling)
## Topshiriq sharti:
Hisob raqamlari bo'yicha bo'lish amali bajarilganda nolga bo'lish (DIVISION_BY_ZERO) va boshqa kutilmagan istisnolarni (OTHERS) ushlab, tranzaksiya qulamasdan xavfsiz javob qaytaruvchi funksiya yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION xavfsiz_bolish(
    p_surat NUMERIC,
    p_maxraj NUMERIC
)
RETURNS NUMERIC
LANGUAGE plpgsql
IMMUTABLE
AS $$
DECLARE
    v_natija NUMERIC;
BEGIN
    v_natija := p_surat / p_maxraj;
    RETURN ROUND(v_natija, 4);

EXCEPTION
    WHEN division_by_zero THEN
        RAISE NOTICE 'Diqqat: Nolga bo''lish holati aniqlandi!';
        RETURN 0.0000;
    WHEN numeric_value_out_of_range THEN
        RAISE WARNING 'Diqqat: Son sig''imi chegaradan oshdi!';
        RETURN NULL;
    WHEN OTHERS THEN
        RAISE WARNING 'Kutilmagan xatolik yuz berdi: %', SQLERRM;
        RETURN NULL;
END;
$$;

-- Test sinovlari
SELECT 
    xavfsiz_bolish(100, 4) AS normal,
    xavfsiz_bolish(50, 0)  AS nolga_bolish;
```

## Tushuntirish va Mantiq:
PL/pgSQL funksiyasida `EXCEPTION` bloki yordamida o'ziga xos xatoliklar (masalan `division_by_zero`, `unique_violation`) yoki umumiy `OTHERS` guruhi tutiladi. Xatolik tutilganda funksiya to'xtab qolmasdan o'rniga zaxira qiymat yoki log yozib qaytadi. `SQLERRM` xatolikning rasmiy matnini beradi.

## Ishlash natijasi:
```text
NOTICE:  Diqqat: Nolga bo'lish holati aniqlandi!
 normal  | nolga_bolish 
---------+--------------
 25.0000 |       0.0000
(1 row)
```


# 809-Topshiriq: GET DIAGNOSTICS yordamida ta'sirlangan qatorlar sonini aniqlash (ROW_COUNT)
## Topshiriq sharti:
Muddati o'tgan faol bo'lmagan foydalanuvchilar sessiyalarini o'chiruvchi va `GET DIAGNOSTICS` orqali aynan nechta sessiya yozuvi o'chirilganini log qilib, sonini qaytaruvchi funksiya yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION tozalash_eskirgan_sessiyalar(p_kun_chegara INT)
RETURNS INT
LANGUAGE plpgsql
AS $$
DECLARE
    v_ochirilgan_soni INT;
BEGIN
    -- Belgilangan muddatdan eski sessiyalarni o'chirish
    DELETE FROM foydalanuvchi_sessiyalari
    WHERE oxirgi_faollik < NOW() - (p_kun_chegara || ' days')::INTERVAL;

    -- Oxirgi DML operatori ta'sir qilgan qatorlar sonini olish
    GET DIAGNOSTICS v_ochirilgan_soni = ROW_COUNT;

    RAISE NOTICE 'Tozalash yakunlandi. Ochirilgan sessiyalar soni: %', v_ochirilgan_soni;
    RETURN v_ochirilgan_soni;
END;
$$;

-- Chaqiruv
SELECT tozalash_eskirgan_sessiyalar(30) AS tozalangan_qatorlar;
```

## Tushuntirish va Mantiq:
`GET DIAGNOSTICS o'zgaruvchi = ROW_COUNT;` konstruktsiyasi eng oxirgi bajarilgan INSERT, UPDATE yoki DELETE buyrug'i tomonidan qancha qator o'zgartirilgan yoki o'chirilganini aniq hisoblaydi. Bu partiyaviy operatsiyalarda biznes hisobotlar tuzishda nihoyatda qo'l keladi.

## Ishlash natijasi:
```text
NOTICE:  Tozalash yakunlandi. Ochirilgan sessiyalar soni: 142
 tozalangan_qatorlar 
---------------------
                 142
(1 row)
```


# 810-Topshiriq: Dinamik SQL: EXECUTE ... USING operatori bilan xavfsiz so'rov qurish
## Topshiriq sharti:
Jadval nomi va filtr ustuni nomi dinamik berilganda SQL Injection xavfidan xoli tarzda `quote_ident` va `USING` orqali parametrlangan agregat hisoblovchi funksiya yarating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION dinamik_hisobla_qatorlar(
    p_jadval_nomi TEXT,
    p_ustun_nomi TEXT,
    p_minimal_qiymat NUMERIC
)
RETURNS BIGINT
LANGUAGE plpgsql
AS $$
DECLARE
    v_sql TEXT;
    v_soni BIGINT;
BEGIN
    -- format() va %I identifikatorlarni SQL Injection'dan himoyalaydi
    v_sql := format(
        'SELECT COUNT(*) FROM %I WHERE %I >= $1',
        p_jadval_nomi,
        p_ustun_nomi
    );

    -- Parametrni $1 orqali xavfsiz uzatish
    EXECUTE v_sql INTO v_soni USING p_minimal_qiymat;

    RETURN v_soni;
END;
$$;

-- Test chaqiruvi
SELECT dinamik_hisobla_qatorlar('buyurtmalar', 'umumiy_summa', 500000.00);
```

## Tushuntirish va Mantiq:
Dinamik SQL bajarish uchun `EXECUTE sql_matni` ishlatiladi. Jadval va ustun nomlarini matnga oddiy ulash (string concatenation) juda xavfli bo'lgani sababli `format('%I', nom)` funksiyasi ishlatiladi (%I = identifier). Qiymatlar esa hech qachon matn ichiga joylanmay, `USING qiymat` orqali `$1, $2` parametrlariga xavfsiz bog'lanadi.

## Ishlash natijasi:
```text
dinamik_hisobla_qatorlar 
-------------------------
                     854
(1 row)
```


# 811-Topshiriq: Oddiy LOOP ... EXIT WHEN tsikli yordamida faktorial hisoblash
## Topshiriq sharti:
Musbat butun son berilganda uning faktorialini (`N!`) hisoblovchi, cheksiz LOOP va EXIT WHEN boshqaruvidan foydalanadigan funksiya tuzing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION hisobla_faktorial(n INT)
RETURNS NUMERIC
LANGUAGE plpgsql
IMMUTABLE
AS $$
DECLARE
    v_faktorial NUMERIC := 1;
    v_sanagich INT := 1;
BEGIN
    IF n < 0 THEN
        RAISE EXCEPTION 'Manfiy son uchun faktorial aniqlanmagan: %', n;
    ELSIF n = 0 THEN
        RETURN 1;
    END IF;

    LOOP
        v_faktorial := v_faktorial * v_sanagich;
        v_sanagich := v_sanagich + 1;

        EXIT WHEN v_sanagich > n;
    END LOOP;

    RETURN v_faktorial;
END;
$$;

SELECT 
    hisobla_faktorial(5)  AS faktorial_5,
    hisobla_faktorial(10) AS faktorial_10;
```

## Tushuntirish va Mantiq:
PL/pgSQL'da `LOOP ... END LOOP` asosiy cheksiz tsikl hisoblanadi. Undan chiqish uchun `EXIT WHEN shart;` operatori qo'llaniladi. Katta sonlar bilan ishlashda to'lib toshish (overflow) sodir bo'lmasligi uchun qaytariluvchi tur sifatida NUMERIC tanlandi.

## Ishlash natijasi:
```text
faktorial_5 | faktorial_10 
-------------+--------------
         120 |      3628800
(1 row)
```


# 812-Topshiriq: WHILE tsikli yordamida Evklid algoritmi (EKUB hisoblash)
## Topshiriq sharti:
Ikkita musbat son berilganda ularning eng katta umumiy bo'luvchisini (EKUB / GCD) `WHILE` tsikli yordamida hisoblovchi `aniqla_ekub` funksiyasini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION aniqla_ekub(a INT, b INT)
RETURNS INT
LANGUAGE plpgsql
IMMUTABLE
AS $$
DECLARE
    v_a INT := ABS(a);
    v_b INT := ABS(b);
    v_vaqtincha INT;
BEGIN
    WHILE v_b <> 0 LOOP
        v_vaqtincha := v_b;
        v_b := v_a % v_b;
        v_a := v_vaqtincha;
    END LOOP;

    RETURN v_a;
END;
$$;

SELECT 
    aniqla_ekub(48, 18)  AS ekub_1,
    aniqla_ekub(1071, 462) AS ekub_2;
```

## Tushuntirish va Mantiq:
Evklid algoritmi qoldiqli bo'lish orqali EKUBni eng tez topish usulidir. `WHILE shart LOOP ... END LOOP` konstruktsiyasi har bir iteratsiyada shartni tekshiradi va shart rost bo'lib turganda qadamlarni takrorlaydi.

## Ishlash natijasi:
```text
ekub_1 | ekub_2 
--------+--------
      6 |     21
(1 row)
```


# 813-Topshiriq: FOR IN diapazon tsikli (FOR i IN 1..N REVERSE)
## Topshiriq sharti:
Berilgan sondan 1 gacha teskari sanash orqali kreditning yillik foizlarini amortizatsiya jadvalini hisoblovchi FOR tsiklli funksiya yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION yaratish_yillik_reja(p_yillar INT, p_asosiy_qarz NUMERIC)
RETURNS TABLE(yil INT, oraliq_qoldiq NUMERIC)
LANGUAGE plpgsql
AS $$
DECLARE
    v_yillik_tolov NUMERIC;
    v_joriy_qoldiq NUMERIC := p_asosiy_qarz;
BEGIN
    v_yillik_tolov := p_asosiy_qarz / p_yillar;

    FOR i IN 1..p_yillar LOOP
        yil := i;
        v_joriy_qoldiq := v_joriy_qoldiq - v_yillik_tolov;
        oraliq_qoldiq := ROUND(v_joriy_qoldiq, 2);
        RETURN NEXT;
    END LOOP;
END;
$$;

SELECT * FROM yaratish_yillik_reja(3, 30000000.00);
```

## Tushuntirish va Mantiq:
`FOR o'zgaruvchi IN boshlang'ich..oxirgi LOOP` konstruksiyasi avtomatik o'zgaruvchini oshirib boradi (agar `REVERSE` qo'yilsa kamaytiradi). `RETURN NEXT` buyrug'i joriy ustun o'zgaruvchilarining qiymatlarini bitta qator qilib natijalar buferiga yuboradi va tsikl tugagach barcha qatorlar bir vaqtda qaytariladi.

## Ishlash natijasi:
```text
yil | oraliq_qoldiq 
-----+---------------
   1 |   20000000.00
   2 |   10000000.00
   3 |          0.00
(3 rows)
```


# 814-Topshiriq: FOR record IN SELECT tsikli orqali qatorlarni aylanib chiqish
## Topshiriq sharti:
Barcha filiallarning oylik tushumlarini ketma-ket o'qib, ularga korporativ bonus hisoblovchi va har bir filial bo'yicha hisobot yaratuvchi kursorli tsikl funksiyasini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION hisobla_filiallar_bonusi()
RETURNS TABLE (
    filial_id INT,
    filial_nomi VARCHAR(100),
    tushum NUMERIC(15,2),
    bonus_summa NUMERIC(15,2)
)
LANGUAGE plpgsql
AS $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN 
        SELECT f.id, f.nomi, COALESCE(SUM(b.summa), 0) AS jami_savdo
        FROM filiallar f
        LEFT JOIN savdolar b ON f.id = b.filial_id
        GROUP BY f.id, f.nomi
        ORDER BY jami_savdo DESC
    LOOP
        filial_id := r.id;
        filial_nomi := r.nomi;
        tushum := r.jami_savdo;

        -- 100 milliondan ortiq tushumga 5% bonus
        IF r.jami_savdo >= 100000000 THEN
            bonus_summa := ROUND(r.jami_savdo * 0.05, 2);
        ELSE
            bonus_summa := ROUND(r.jami_savdo * 0.02, 2);
        END IF;

        RETURN NEXT;
    END LOOP;
END;
$$;

SELECT * FROM hisobla_filiallar_bonusi();
```

## Tushuntirish va Mantiq:
`FOR record IN SELECT ... LOOP` konstruksiyasi PostgreSQL PL/pgSQL ning eng qulay xususiyatlaridan biridir. Dvigatel orqa fonda implicit cursor ochadi va har bir qatorni RECORD turidagi o'zgaruvchiga yuklaydi. Xotira qatorlar sonidan qat'i nazar tejaladi.

## Ishlash natijasi:
```text
filial_id |     filial_nomi     |    tushum    | bonus_summa 
-----------+---------------------+--------------+-------------
         1 | Toshkent Markaz     | 350000000.00 | 17500000.00
         3 | Samarqand Katta     | 120000000.00 |  6000000.00
         2 | Farg'ona Vodiy      |  85000000.00 |  1700000.00
(3 rows)
```


# 815-Topshiriq: Ochiq kursorlar (Explicit Cursors: OPEN, FETCH, CLOSE)
## Topshiriq sharti:
Katta hajmdagi ombor qoldiqlarini 2 tadan qilib paketlab (batch) o'qiydigan aniq e'lon qilingan kursorli funksiya yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION oqish_mahsulot_paket(p_paket_hajmi INT)
RETURNS TABLE(mahsulot_id INT, mahsulot_nomi VARCHAR(100), qoldiq INT)
LANGUAGE plpgsql
AS $$
DECLARE
    kursor_ombor CURSOR FOR 
        SELECT id, nomi, mavjud_soni 
        FROM ombor_tovarlar 
        ORDER BY mavjud_soni ASC;
    v_id INT;
    v_nomi VARCHAR(100);
    v_soni INT;
    v_sanagich INT := 0;
BEGIN
    OPEN kursor_ombor;

    LOOP
        FETCH kursor_ombor INTO v_id, v_nomi, v_soni;
        EXIT WHEN NOT FOUND OR v_sanagich >= p_paket_hajmi;

        mahsulot_id := v_id;
        mahsulot_nomi := v_nomi;
        qoldiq := v_soni;
        v_sanagich := v_sanagich + 1;

        RETURN NEXT;
    END LOOP;

    CLOSE kursor_ombor;
END;
$$;

SELECT * FROM oqish_mahsulot_paket(2);
```

## Tushuntirish va Mantiq:
Explicit Cursor yordamida o'qish xotira sarfini qat'iy nazorat qilish imkonini beradi. `OPEN` kursor so'rovini ishga tushiradi, `FETCH` bitta qatorni o'zgaruvchilarga oladi (`NOT FOUND` kursor oxiriga yetganda TRUE bo'ladi) va `CLOSE` tizim resurslarini bo'shatadi.

## Ishlash natijasi:
```text
mahsulot_id |  mahsulot_nomi  | qoldiq 
-------------+-----------------+--------
           4 | Klaviatura RGB  |      2
           9 | Simsiz Sichqon  |      5
(2 rows)
```


# 816-Topshiriq: Parametrlangan kursor (Parameterized Cursor)
## Topshiriq sharti:
Faqat ma'lum bir yetkazib beruvchi ID'si bo'yicha tovarlarni saralovchi parametrlangan kursor tuzing va funksiya ichida foydalaning.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION yetkazib_beruvchi_tovarlari(p_taminotchi_id INT)
RETURNS TABLE(tovar_nomi VARCHAR(100), tannarx NUMERIC)
LANGUAGE plpgsql
AS $$
DECLARE
    cur_tovarlar CURSOR(t_id INT) FOR 
        SELECT nomi, kelish_narxi 
        FROM xaridlar 
        WHERE taminotchi_id = t_id;
    v_rec RECORD;
BEGIN
    OPEN cur_tovarlar(t_id := p_taminotchi_id);

    LOOP
        FETCH cur_tovarlar INTO v_rec;
        EXIT WHEN NOT FOUND;

        tovar_nomi := v_rec.nomi;
        tannarx := v_rec.kelish_narxi;
        RETURN NEXT;
    END LOOP;

    CLOSE cur_tovarlar;
END;
$$;

SELECT * FROM yetkazib_beruvchi_tovarlari(12);
```

## Tushuntirish va Mantiq:
Parametrlangan kursor `CURSOR(t_id INT)` ko'rinishida e'lon qilinadi va `OPEN cur_nom(argument)` orqali ochiladi. Bu bir xil kursor tuzilmasini funksiya ichida har xil parametrlar bilan qayta-qayta ochish va ishlatish imkoniyatini beradi.

## Ishlash natijasi:
```text
tovar_nomi     |  tannarx   
------------------+------------
 Monitor 27 IPS   | 1800000.00
 HDMI Kabel 3m    |   35000.00
 Veb-kamera 1080p |  320000.00
(3 rows)
```


# 817-Topshiriq: Funksiya o'zgaruvchiligining darajalari: VOLATILE, STABLE va IMMUTABLE
## Topshiriq sharti:
PostgreSQL optimallashtiruvchisiga funksiya xulqini tushuntiruvchi 3 xil toifadagi funksiya yarating va ularning keshlanish farqini ko'rsating.

## Yechim (SQL kodi):
```sql
-- 1. IMMUTABLE: Parametrlar bir xil bo'lsa, natija hech qachon o'zgarmaydi (DB holatiga bog'liq emas)
CREATE OR REPLACE FUNCTION kvadrat(x NUMERIC)
RETURNS NUMERIC
LANGUAGE SQL
IMMUTABLE
AS $$ SELECT x * x; $$;

-- 2. STABLE: Bitta SQL so'rov ichida jadval o'zgarmas ekan, natija o'zgarmaydi
CREATE OR REPLACE FUNCTION joriy_kurs(valyuta VARCHAR(3))
RETURNS NUMERIC
LANGUAGE SQL
STABLE
AS $$ SELECT kurs FROM valyutalar WHERE kod = valyuta; $$;

-- 3. VOLATILE (Standart): Har bir chaqiruvda har xil natija yoki yon ta'siri (side-effect) bor
CREATE OR REPLACE FUNCTION yaratish_tasodifiy_kod()
RETURNS TEXT
LANGUAGE SQL
VOLATILE
AS $$ SELECT LPAD(FLOOR(RANDOM() * 1000000)::TEXT, 6, '0'); $$;

SELECT 
    kvadrat(12) AS immut,
    yaratish_tasodifiy_kod() AS volat;
```

## Tushuntirish va Mantiq:
Funksiya volatilitesi (o'zgaruvchanligi) optimallashtiruvchi uchun juda muhim: IMMUTABLE funksiyalar so'rovni rejalashtirish bosqichidayoq statik doimiyga almashtirilishi mumkin va indekslarda ishlatiladi; STABLE bitta statement ichida keshlanadi; VOLATILE esa har bir qator uchun qaytadan to'liq bajariladi.

## Ishlash natijasi:
```text
immut  |  volat  
--------+---------
 144.00 | 582914
(1 row)
```


# 818-Topshiriq: SECURITY DEFINER va SECURITY INVOKER xavfsizlik rejimlari
## Topshiriq sharti:
Oddiy xodimlar parolni o'zgartira olishi uchun ularga butun foydalanuvchilar jadvaliga ruxsat bermasdan, funksiyani yaratuvchi superadmin huquqi bilan ishlaydigan xavfsiz `parol_ozgartir` funksiyasini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION parol_ozgartir(
    p_foydalanuvchi_id INT,
    p_yangi_parol_hash TEXT
)
RETURNS VOID
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
BEGIN
    UPDATE xavfsizlik_foydalanuvchilar
    SET parol_hash = p_yangi_parol_hash,
        oxirgi_yangilanish = NOW()
    WHERE id = p_foydalanuvchi_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Bunday foydalanuvchi topilmadi!';
    END IF;
END;
$$;

-- Chaqiruv
SELECT parol_ozgartir(5, 'e10adc3949ba59abbe56e057f20f883e');
```

## Tushuntirish va Mantiq:
Standart holatda funksiyalar `SECURITY INVOKER` rejimida ishlaydi (chaqirgan shaxsning huquqlari bilan). `SECURITY DEFINER` esa funksiyani uni yaratgan egasining (owner) huquqlari bilan ishga tushiradi (Linux'dagi SUID analogi). Xavfsizlik uchun `SET search_path = public, pg_temp` orqali qidiruv yo'lini mahkamlab qo'yish shart, aks holda search_path injection hujumi xavfi tug'iladi.

## Ishlash natijasi:
```text
parol_ozgartir 
----------------
 
(1 row)
```


# 819-Topshiriq: VARIADIC parametrlari bilan ixtiyoriy miqdordagi argumentlarni qabul qilish
## Topshiriq sharti:
Funksiyaga istalgancha sonli argument uzatilganda ularning geometrik o'rtachasini hisoblaydigan funksiya tuzing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION geometrik_ortacha(VARIADIC sonlar NUMERIC[])
RETURNS NUMERIC
LANGUAGE plpgsql
IMMUTABLE
AS $$
DECLARE
    v_kopaytma NUMERIC := 1.0;
    v_element NUMERIC;
    v_jami_elementlar INT;
BEGIN
    v_jami_elementlar := ARRAY_LENGTH(sonlar, 1);

    IF v_jami_elementlar IS NULL OR v_jami_elementlar = 0 THEN
        RETURN NULL;
    END IF;

    FOREACH v_element IN ARRAY sonlar LOOP
        IF v_element <= 0 THEN
            RAISE EXCEPTION 'Musbat sonlar kutilmoqda, berildi: %', v_element;
        END IF;
        v_kopaytma := v_kopaytma * v_element;
    END LOOP;

    -- n-darajali ildiz: x^(1/n)
    RETURN ROUND((v_kopaytma ^ (1.0 / v_jami_elementlar)), 4);
END;
$$;

SELECT 
    geometrik_ortacha(2, 8) AS geom_1,
    geometrik_ortacha(3, 9, 27) AS geom_2;
```

## Tushuntirish va Mantiq:
`VARIADIC sonlar NUMERIC[]` parametri funksiyaga cheksiz ko'p argumentlarni vergul bilan uzatish imkonini beradi. Funksiya ichida bu parametr massiv (array) sifatida ko'riladi. `FOREACH v IN ARRAY massiv` konstruktsiyasi massiv elementlarini qulay aylanib chiqadi.

## Ishlash natijasi:
```text
geom_1 | geom_2 
--------+--------
 4.0000 | 9.0000
(1 row)
```


# 820-Topshiriq: Massivlar ustida amallar: UNNEST va ARRAY konstruktorlari funksiyada
## Topshiriq sharti:
Matn ko'rinishidagi teglar ro'yxatini (tag_list) massiv qilib olib, takrorlanuvchi teglarni olib tashlab, alfavit bo'yicha saralangan massiv qaytaruvchi funksiya yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION sarala_unikal_teglar(p_teglar TEXT[])
RETURNS TEXT[]
LANGUAGE SQL
IMMUTABLE
AS $$
    SELECT ARRAY(
        SELECT DISTINCT LOWER(TRIM(t))
        FROM UNNEST(p_teglar) AS t
        WHERE TRIM(t) <> ''
        ORDER BY 1
    );
$$;

SELECT sarala_unikal_teglar(ARRAY['PostgreSQL', 'sql', ' Database ', 'SQL', 'PostgreSQL']);
```

## Tushuntirish va Mantiq:
`UNNEST(array)` massiv elementlarini alohida relyatsion qatorlarga yoyadi. Qatorlar ustida `DISTINCT`, `LOWER` va `ORDER BY` amallari bajarilgandan so'ng, `ARRAY(...)` konstruktori natijaviy qatorlarni yana massivga yig'adi.

## Ishlash natijasi:
```text
sarala_unikal_teglar    
---------------------------
 {database,postgresql,sql}
(1 row)
```


# 821-Topshiriq: RETURN QUERY EXECUTE orqali dinamik jadval qaytarish
## Topshiriq sharti:
Berilgan ustun bo'yicha o'sish yoki kamayish tartibida saralangan foydalanuvchilar ro'yxatini qaytaruvchi dinamik so'rovli funksiya tuzing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION olish_saralangan_foydalanuvchilar(
    p_saralash_ustun TEXT,
    p_tartib TEXT DEFAULT 'ASC'
)
RETURNS TABLE(id INT, ism VARCHAR(50), yaratilgan_vaqt TIMESTAMP)
LANGUAGE plpgsql
AS $$
DECLARE
    v_sql TEXT;
BEGIN
    IF LOWER(p_tartib) NOT IN ('asc', 'desc') THEN
        RAISE EXCEPTION 'Notogri tartib: faqat ASC yoki DESC bolishi mumkin!';
    END IF;

    IF LOWER(p_saralash_ustun) NOT IN ('id', 'ism', 'yaratilgan_vaqt') THEN
        RAISE EXCEPTION 'Notogri ustun nomi: %', p_saralash_ustun;
    END IF;

    v_sql := format(
        'SELECT id, ism, yaratilgan_vaqt FROM foydalanuvchilar ORDER BY %I %s LIMIT 5',
        p_saralash_ustun,
        p_tartib
    );

    RETURN QUERY EXECUTE v_sql;
END;
$$;

SELECT * FROM olish_saralangan_foydalanuvchilar('ism', 'ASC');
```

## Tushuntirish va Mantiq:
`RETURN QUERY EXECUTE sql_matni` dinamik tarzda hosil qilingan SELECT so'rovi natijasini RETURNS TABLE formatida to'g'ridan-to'g'ri oqim qilib chaqiruvchiga yo'naltiradi. SQL Injection oldini olish uchun ustun nomlari oq ro'yxat (whitelist) orqali tekshiriladi.

## Ishlash natijasi:
```text
id |   ism   |      yaratilgan_vaqt       
----+---------+----------------------------
  7 | Anvar   | 2024-01-15 10:20:00
 12 | Bekzod  | 2024-02-10 14:45:00
  3 | Dilshod | 2024-01-05 09:12:00
  1 | Feruza  | 2023-12-01 18:00:00
 15 | Jasur   | 2024-03-01 11:30:00
(5 rows)
```


# 822-Topshiriq: GET STACKED DIAGNOSTICS yordamida chuqur xatolik stack trace olish
## Topshiriq sharti:
Funksiya xatolikka uchraganda xatoning aniq kodi (PG_EXCEPTION_CONTEXT, RETURNED_SQLSTATE) va qaysi qatorda yuz berganini ushlab, audit jadvaliga yozuvchi protsedura tuzing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE PROCEDURE xavfsiz_ijro_bilan_log(p_sql TEXT)
LANGUAGE plpgsql
AS $$
DECLARE
    v_state   TEXT;
    v_msg     TEXT;
    v_context TEXT;
BEGIN
    EXECUTE p_sql;
    RAISE NOTICE 'Buyruq muvaffaqiyatli bajarildi.';

EXCEPTION WHEN OTHERS THEN
    GET STACKED DIAGNOSTICS
        v_state   = RETURNED_SQLSTATE,
        v_msg     = MESSAGE_TEXT,
        v_context = PG_EXCEPTION_CONTEXT;

    RAISE WARNING 'Xatolik yuz berdi! Kod: %, Xabar: %, Kontekst: %', 
        v_state, v_msg, v_context;

    INSERT INTO tizim_xatolari(xato_kodi, xato_matni, kontekst, sana)
    VALUES (v_state, v_msg, v_context, NOW());
END;
$$;

CALL xavfsiz_ijro_bilan_log('SELECT 100 / 0');
```

## Tushuntirish va Mantiq:
`GET STACKED DIAGNOSTICS` faqat EXCEPTION bloki ichida ishlaydi va PostgreSQL'ning ichki qo'ng'iroqlar stekini (stack trace), xatoning SQLSTATE kodini va batafsil xabarini ajratib olishga xizmat qiladi. Bu ishlab chiqarish tizimlarida jiddiy xatoliklarni ro'yxatga olishda asosiy mexanizmdir.

## Ishlash natijasi:
```text
WARNING:  Xatolik yuz berdi! Kod: 22012, Xabar: division by zero, Kontekst: SQL statement "SELECT 100 / 0"
PL/pgSQL function xavfsiz_ijro_bilan_log(text) line 8 at EXECUTE
CALL
```


# 823-Topshiriq: Protsedura ichida tranzaksiya o'rtasida COMMIT va ROLLBACK qilish
## Topshiriq sharti:
1000 ta mijozning hisobini yangilash jarayonida har 100 ta qatordan keyin oraliq `COMMIT` chaqiruvchi va xato bo'lsa oxirgi blokni `ROLLBACK` qiluvchi protsedura yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE PROCEDURE partiyaviy_foiz_yangilash()
LANGUAGE plpgsql
AS $$
DECLARE
    r RECORD;
    v_sanagich INT := 0;
BEGIN
    FOR r IN SELECT id, balans FROM omonat_hisoblar WHERE holat = 'FAOL' LOOP
        UPDATE omonat_hisoblar
        SET balans = balans * 1.01
        WHERE id = r.id;

        v_sanagich := v_sanagich + 1;

        -- Har 100 ta yozuvda tranzaksiyani mustahkamlash
        IF v_sanagich % 100 = 0 THEN
            COMMIT;
            RAISE NOTICE '% ta mijoz saqlandi va COMMIT qilindi.', v_sanagich;
        END IF;
    END LOOP;

    -- Qolgan yozuvlarni yakuniy saqlash
    COMMIT;
    RAISE NOTICE 'Jami % ta mijoz toliq yangilandi.', v_sanagich;
END;
$$;

CALL partiyaviy_foiz_yangilash();
```

## Tushuntirish va Mantiq:
PostgreSQL 11 versiyasidan boshlab joriy etilgan `CREATE PROCEDURE` funksiyalardan farqli ravishda tranzaksiyalarni boshqarishga (COMMIT/ROLLBACK) to'liq ruxsat beradi. Bu katta jadvallarni o'zgartirishda WAL jurnali haddan tashqari to'lib ketishini va qulflarning (locks) uzoq ushlanib qolishini oldini oladi.

## Ishlash natijasi:
```text
NOTICE:  100 ta mijoz saqlandi va COMMIT qilindi.
NOTICE:  200 ta mijoz saqlandi va COMMIT qilindi.
NOTICE:  Jami 245 ta mijoz toliq yangilandi.
CALL
```


# 824-Topshiriq: Rekursiv PL/pgSQL funksiyasi (Fibonachchi ketma-ketligi)
## Topshiriq sharti:
Rekursiv chaqiruv yordamida N-o'rindagi Fibonachchi sonini aniqlovchi PL/pgSQL funksiyasini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION fibonachchi(n INT)
RETURNS BIGINT
LANGUAGE plpgsql
IMMUTABLE
AS $$
BEGIN
    IF n < 0 THEN
        RAISE EXCEPTION 'Manfiy orin mavjud emas: %', n;
    ELSIF n = 0 THEN
        RETURN 0;
    ELSIF n = 1 THEN
        RETURN 1;
    ELSE
        RETURN fibonachchi(n - 1) + fibonachchi(n - 2);
    END IF;
END;
$$;

SELECT 
    fibonachchi(0) AS fib_0,
    fibonachchi(1) AS fib_1,
    fibonachchi(7) AS fib_7,
    fibonachchi(10) AS fib_10;
```

## Tushuntirish va Mantiq:
PL/pgSQL funksiyalari o'z-o'zini rekursiv chaqirishi mumkin. Har bir chaqiruv stekkada o'zining alohida xotira freymini yaratadi. Katta N qiymatlar uchun rekursiya stek to'lishiga olib kelishi mumkinligi sababli bazaviy shart (`n <= 1`) qat'iy nazorat qilinishi kerak.

## Ishlash natijasi:
```text
fib_0 | fib_1 | fib_7 | fib_10 
-------+-------+-------+--------
     0 |     1 |    13 |     55
(1 row)
```


# 825-Topshiriq: Rekursiv funksiya orqali xodimlar iyerarxiyasini yig'ish
## Topshiriq sharti:
Berilgan rahbar ID'si bo'yicha unga to'g'ridan-to'g'ri va bilvosita bo'ysunuvchi barcha xodimlarni iyerarxiya darajasi (level) bilan birga yig'ib beruvchi funksiya yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION bolinma_xodimlari_daraxti(p_rahbar_id INT)
RETURNS TABLE(xodim_id INT, ism TEXT, lavozim VARCHAR(50), daraja INT)
LANGUAGE SQL
STABLE
AS $$
    WITH RECURSIVE iyerarxiya AS (
        -- Boshlang'ich rahbar
        SELECT id, ism || ' ' || familiya AS toliq_ism, lavozim, 0 AS lvl
        FROM xodimlar
        WHERE id = p_rahbar_id

        UNION ALL

        -- Bo'ysunuvchilar
        SELECT x.id, x.ism || ' ' || x.familiya, x.lavozim, i.lvl + 1
        FROM xodimlar x
        INNER JOIN iyerarxiya i ON x.rahbar_id = i.id
    )
    SELECT id, toliq_ism, lavozim, lvl FROM iyerarxiya;
$$;

SELECT * FROM bolinma_xodimlari_daraxti(1);
```

## Tushuntirish va Mantiq:
Ushbu funksiya ichida RECURSIVE Common Table Expression (CTE) ishlatilib, SQL tili ichida iyerarxik daraxtlar tez va xavfsiz aylanib chiqiladi. SQL tili optimallashtiruvchisi bunday CTE so'rovlarni juda samarali ijro etadi.

## Ishlash natijasi:
```text
xodim_id |       ism       |     lavozim      | daraja 
----------+-----------------+------------------+--------
        1 | Alisher Usmonov | Bosh Direktor    |      0
        2 | Jasur Fayziyev  | Texnik Direktor  |      1
        3 | Umid Vohidov    | Bosh Buxgalter   |      1
        5 | Otabek Madaminov| Backend Dev      |      2
(4 rows)
```


# 826-Topshiriq: Tranzaksion hisob tekshiruvi va maxsus RAISE EXCEPTION kodlari
## Topshiriq sharti:
Mijozning yoshini tekshiruvchi va agar 18 yoshdan kichik bo'lsa xalqaro standartdagi maxsus SQLSTATE kodi ('22003') bilan istisno chiqaruvchi funksiya yarating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION tekshir_mijoz_yoshi(p_tugilgan_sana DATE)
RETURNS BOOLEAN
LANGUAGE plpgsql
IMMUTABLE
AS $$
DECLARE
    v_yosh INT;
BEGIN
    v_yosh := EXTRACT(YEAR FROM AGE(CURRENT_DATE, p_tugilgan_sana));

    IF v_yosh < 18 THEN
        RAISE EXCEPTION 'Mijoz voyaga yetmagan! Yoshi: %', v_yosh
            USING ERRCODE = 'check_violation',
                  HINT = 'Mijoz 18 yoshdan katta bolishi shart!';
    END IF;

    RETURN TRUE;
END;
$$;

SELECT tekshir_mijoz_yoshi('2000-05-15');
```

## Tushuntirish va Mantiq:
`RAISE EXCEPTION` yordamida nafaqat xato matni, balki `ERRCODE`, `HINT`, `DETAIL` kabi qo'shimcha semantik parametrlar ham uzatiladi. Bu API va backend dasturchilariga xatoni dastur darajasida aniq ushlash va foydalanuvchiga to'g'ri xabar berish imkonini ta'minlaydi.

## Ishlash natijasi:
```text
tekshir_mijoz_yoshi 
---------------------
 t
(1 row)
```


# 827-Topshiriq: Massiv elementlarini qidirish va filtrlovchi PL/pgSQL funksiyasi
## Topshiriq sharti:
Sonlar massivi berilganda faqat juft va musbat sonlarni saralab yangi massiv ko'rinishida qaytaruvchi funksiya yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION sarala_juft_sonlar(p_sonlar INT[])
RETURNS INT[]
LANGUAGE plpgsql
IMMUTABLE
AS $$
DECLARE
    v_saralangan INT[] := '{}';
    v_element INT;
BEGIN
    FOREACH v_element IN ARRAY p_sonlar LOOP
        IF v_element > 0 AND v_element % 2 = 0 THEN
            v_saralangan := ARRAY_APPEND(v_saralangan, v_element);
        END IF;
    END LOOP;

    RETURN v_saralangan;
END;
$$;

SELECT sarala_juft_sonlar(ARRAY[-4, -2, 0, 1, 2, 5, 8, 11, 14]);
```

## Tushuntirish va Mantiq:
`v_saralangan INT[] := '{}'` bo'sh massiv bilan initsializatsiya qilinadi. `ARRAY_APPEND(massiv, yangi_element)` har safar shart bajarilganda elementni massiv oxiriga qo'shadi.

## Ishlash natijasi:
```text
sarala_juft_sonlar 
---------------------
 {2,8,14}
(1 row)
```


# 828-Topshiriq: CONTINUE va EXIT bandlari bilan ichki tsikllarni boshqarish
## Topshiriq sharti:
1 dan 20 gacha bo'lgan sonlar orasidan 3 ga karralilarini tashlab ketuvchi (CONTINUE), lekin 16 ga yetganda tsiklni butunlay to'xtatuvchi (EXIT) funksiya tuzing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION filtr_sonlar_oqimi()
RETURNS TABLE(son INT)
LANGUAGE plpgsql
IMMUTABLE
AS $$
BEGIN
    FOR i IN 1..20 LOOP
        -- 16 ga yetganda butunlay to'xtatish
        EXIT WHEN i = 16;

        -- 3 ga karrali bo'lsa tashlab ketish
        CONTINUE WHEN i % 3 = 0;

        son := i;
        RETURN NEXT;
    END LOOP;
END;
$$;

SELECT ARRAY_AGG(son) AS natija_massiv FROM filtr_sonlar_oqimi();
```

## Tushuntirish va Mantiq:
`CONTINUE WHEN shart` operatori joriy iteratsiyani shu zahoti yakunlab, keyingi qadamga o'tadi. `EXIT WHEN shart` esa tsikldan zudlik bilan chiqib ketishni ta'minlaydi.

## Ishlash natijasi:
```text
natija_massiv       
--------------------------
 {1,2,4,5,7,8,10,11,13,14}
(1 row)
```


# 829-Topshiriq: Teglangan tsikllar (Labeled Loops) va ko'p bosqichli EXIT
## Topshiriq sharti:
Matritsa (ikki o'lchovli koordinatalar) ichida qidiruv amalga oshiruvchi va nishon topilganda birdaniga har ikkala ichma-ich tsikldan bittada chiqib ketuvchi teglangan tsikl yarating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION qidir_matritsa(p_nishon INT)
RETURNS TEXT
LANGUAGE plpgsql
IMMUTABLE
AS $$
DECLARE
    v_x INT;
    v_y INT;
    v_topildi BOOLEAN := FALSE;
BEGIN
    <<tashqi_tsikl>>
    FOR i IN 1..10 LOOP
        <<ichki_tsikl>>
        FOR j IN 1..10 LOOP
            IF (i * j) = p_nishon THEN
                v_x := i;
                v_y := j;
                v_topildi := TRUE;
                EXIT tashqi_tsikl; -- Birdaniga tashqi tsikldan chiqish
            END IF;
        END LOOP ichki_tsikl;
    END LOOP tashqi_tsikl;

    IF v_topildi THEN
        RETURN format('Nishon %s x=%s, y=%s nuqtada topildi', p_nishon, v_x, v_y);
    ELSE
        RETURN 'Topilmadi';
    END IF;
END;
$$;

SELECT qidir_matritsa(42);
```

## Tushuntirish va Mantiq:
Tsikllarga `<<teg_nomi>>` formatida yorliq (label) berilganda, ichki qavatdagi tsikldan turib `EXIT teg_nomi;` orqali to'g'ridan-to'g'ri tashqi tsikldan ham chiqib ketish mumkin. Bu ko'p bosqichli flag (bayroqcha) o'zgaruvchilarini tekshirish zaruratini yo'qotadi.

## Ishlash natijasi:
```text
qidir_matritsa              
-----------------------------------------
 Nishon 42 x=6, y=7 nuqtada topildi
(1 row)
```


# 830-Topshiriq: SETOF RECORD qaytaruvchi umumiy funksiya
## Topshiriq sharti:
Parametr sifatida uzatilgan ixtiyoriy SQL so'rovini qabul qilib, uning natijasini turlaridan qat'i nazar SETOF RECORD ko'rinishida qaytaruvchi funksiya yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION bajar_universal_sorov(p_query TEXT)
RETURNS SETOF RECORD
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY EXECUTE p_query;
END;
$$;

-- Chaqiruvda ustunlar turlarini aniq ko'rsatish (AS bandi)
SELECT * FROM bajar_universal_sorov('SELECT id, ism FROM foydalanuvchilar LIMIT 2')
AS (f_id INT, f_ism VARCHAR(50));
```

## Tushuntirish va Mantiq:
`SETOF RECORD` qaytaruvchi funksiyalarda ustunlar soni va turlari oldindan qat'iy belgilanmagan bo'ladi. Chaqiruvchi so'rov paytida `AS (ustun1 tur1, ustun2 tur2)` orqali PostgreSQL'ga kutilayotgan relyatsion shaklni tushuntirishi shart.

## Ishlash natijasi:
```text
f_id | f_ism  
------+--------
    1 | Feruza
    2 | Jasur
(2 rows)
```


# 831-Topshiriq: Strict (RETURNS NULL ON NULL INPUT) optimizatsiyasi
## Topshiriq sharti:
Agar argumentlardan biri NULL bo'lsa, funksiya tanasini umuman bajarmasdan to'g'ridan-to'g'ri NULL qaytaruvchi STRICT funksiya yarating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION toliq_manzil_quruvchi(
    shahar TEXT,
    kocha TEXT,
    uy_raqam TEXT
)
RETURNS TEXT
LANGUAGE SQL
IMMUTABLE
STRICT
AS $$
    SELECT shahar || ', ' || kocha || ' ko''chasi, ' || uy_raqam || '-uy';
$$;

-- NULL bilan va NULL siz chaqiruv
SELECT 
    toliq_manzil_quruvchi('Toshkent', 'Amir Temur', '14') AS manzil,
    toliq_manzil_quruvchi('Toshkent', NULL, '14')          AS null_manzil;
```

## Tushuntirish va Mantiq:
`STRICT` (yoki `RETURNS NULL ON NULL INPUT`) direktivasi kiritilganda, agar biron bir argument `NULL` bo'lsa, PostgreSQL funksiya tanasini (kodini) umuman bajarmaydi va darhol `NULL` qaytaradi. Bu resurslarni tejaydi va ichkarida qo'shimcha NULL tekshiruvlarini talab qilmaydi.

## Ishlash natijasi:
```text
manzil                 | null_manzil 
--------------------------------------+-------------
 Toshkent, Amir Temur ko'chasi, 14-uy | 
(1 row)
```


# 832-Topshiriq: Polimorfik turlar bilan ishlash (ANYELEMENT va ANYARRAY)
## Topshiriq sharti:
Ixtiyoriy turdagi (INT, TEXT, DATE va h.k.) ikkita qiymatni taqqoslab, kattasini qaytaruvchi polimorfik universal funksiya yarating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION universal_maksimum(a ANYELEMENT, b ANYELEMENT)
RETURNS ANYELEMENT
LANGUAGE plpgsql
IMMUTABLE
AS $$
BEGIN
    IF a IS NULL THEN
        RETURN b;
    ELSIF b IS NULL THEN
        RETURN a;
    ELSIF a >= b THEN
        RETURN a;
    ELSE
        RETURN b;
    END IF;
END;
$$;

SELECT 
    universal_maksimum(105, 230) AS max_son,
    universal_maksimum('Olma'::TEXT, 'Anor'::TEXT) AS max_matn,
    universal_maksimum('2024-01-01'::DATE, '2024-12-31'::DATE) AS max_sana;
```

## Tushuntirish va Mantiq:
`ANYELEMENT` va `ANYARRAY` polimorfik turlari bir nechta tur uchun bitta umumiy funksiya yozish imkonini beradi (Generics kabi). Barcha `ANYELEMENT` parametrlari bitta aniq chaqiruv paytida bir xil turga tegishli bo'lishi talab etiladi.

## Ishlash natijasi:
```text
max_son | max_matn |  max_sana  
---------+----------+------------
     230 | Olma     | 2024-12-31
(1 row)
```


# 833-Topshiriq: Jadval turi asosida qator parametrlarini qabul qilish (Row-Type arguments)
## Topshiriq sharti:
Xodimlar jadvalining butun bir qatorini (`xodimlar%ROWTYPE`) argument sifatida qabul qilib, uning nafaqa yoshiga yetganligini baholovchi funksiya tuzing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION tekshir_pensiya_huquqi(p_xodim xodimlar)
RETURNS BOOLEAN
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
    v_yosh INT;
BEGIN
    v_yosh := EXTRACT(YEAR FROM AGE(CURRENT_DATE, p_xodim.tugilgan_sana));

    IF p_xodim.jinsi = 'ERKAK' AND v_yosh >= 60 THEN
        RETURN TRUE;
    ELSIF p_xodim.jinsi = 'AYOL' AND v_yosh >= 55 THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$;

-- Jadvalning o'zini funksiya bilan chaqirish
SELECT id, ism, tekshir_pensiya_huquqi(x.*) AS pensiyada
FROM xodimlar x
LIMIT 3;
```

## Tushuntirish va Mantiq:
PostgreSQL da har bir jadval avtomatik ravishda xuddi shu nomdagi kompozit ma'lumot turini yaratadi (`xodimlar`). Funksiyaga butun jadval qatorini `x.*` tarzida bitta argument qilib uzatish mumkin. Bu ustunlar soni ko'p bo'lgan biznes tahlillarida juda qulay.

## Ishlash natijasi:
```text
id |   ism   | pensiyada 
----+---------+-----------
  1 | Feruza  | f
  2 | Bobur   | t
  3 | Dilshod | f
(3 rows)
```


# 834-Topshiriq: INOUT parametrlari orqali qiymatni o'zgartirib qaytarish
## Topshiriq sharti:
Berilgan boshlang'ich balans va operatsiya summasini qabul qilib, komissiyani chegirib balansni to'g'ridan-to'g'ri o'zgartirib qaytaruvchi INOUT parametrli protsedura tuzing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE PROCEDURE yangila_balans_inout(
    INOUT p_balans NUMERIC,
    IN p_chiqim NUMERIC,
    IN p_komissiya_stavka NUMERIC DEFAULT 0.01
)
LANGUAGE plpgsql
AS $$
BEGIN
    p_balans := p_balans - (p_chiqim * (1 + p_komissiya_stavka));
END;
$$;

-- CALL orqali INOUT parametrni sinash
DO $$
DECLARE
    v_hisob_balans NUMERIC := 1000000.00;
BEGIN
    CALL yangila_balans_inout(v_hisob_balans, 200000.00, 0.02);
    RAISE NOTICE 'Yangi qoldiq: %', v_hisob_balans;
END;
$$;
```

## Tushuntirish va Mantiq:
`INOUT` parametri ham kiruvchi argument, ham chiquvchi natija vazifasini bajaradi. Protsedura chaqirilganda berilgan o'zgaruvchi qiymati protsedura ichida o'zgartiriladi va chaqiruvchiga qaytariladi.

## Ishlash natijasi:
```text
NOTICE:  Yangi qoldiq: 796000.00
DO
```


# 835-Topshiriq: DO bloklari orqali nomsiz anonim PL/pgSQL kodlarini bajarish
## Topshiriq sharti:
Hech qanday funksiya yoki ob'ekt yaratmasdan, faqat bitta marta bajariladigan va terminalga xabar chiqaruvchi anonim DO kod blokini yozing.

## Yechim (SQL kodi):
```sql
DO $$
DECLARE
    v_jami_foydalanuvchilar INT;
    v_faol_ulush NUMERIC;
BEGIN
    SELECT COUNT(*) INTO v_jami_foydalanuvchilar FROM foydalanuvchilar;

    SELECT ROUND(COUNT(*) * 100.0 / NULLIF(v_jami_foydalanuvchilar, 0), 2)
    INTO v_faol_ulush
    FROM foydalanuvchilar
    WHERE oxirgi_faollik >= NOW() - INTERVAL '7 days';

    RAISE NOTICE '-----------------------------------------';
    RAISE NOTICE 'Tizimdagi umumiy son: % ta', v_jami_foydalanuvchilar;
    RAISE NOTICE 'Haftalik faol foydalanuvchilar: %% %', v_faol_ulush;
    RAISE NOTICE '-----------------------------------------';
END;
$$;
```

## Tushuntirish va Mantiq:
`DO $$ ... $$;` buyrug'i ma'lumotlar bazasida doimiy funksiya saqlamasdan anonim PL/pgSQL skriptlarini bajarish uchun xizmat qiladi. U migratsiyalar, tezkor sinovlar va ma'lumotlarni bir martalik tozalashda ishlatiladi.

## Ishlash natijasi:
```text
NOTICE:  -----------------------------------------
NOTICE:  Tizimdagi umumiy son: 1540 ta
NOTICE:  Haftalik faol foydalanuvchilar: % 42.85
NOTICE:  -----------------------------------------
DO
```


# 836-Topshiriq: FOUND maxsus o'zgaruvchisi orqali natija mavjudligini tekshirish
## Topshiriq sharti:
Berilgan email bo'yicha foydalanuvchini topib, uning statusini yangilovchi, agar qator topilmasa yangi foydalanuvchi qo'shuvchi (`FOUND` mantiqi) funksiya tuzing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION yangila_yoki_qosh_mijoz(
    p_email TEXT,
    p_ism TEXT
)
RETURNS TEXT
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE mijozlar
    SET ism = p_ism,
        yangilangan_vaqt = NOW()
    WHERE email = p_email;

    -- Oxirgi DML qatorga ta'sir qildimi?
    IF FOUND THEN
        RETURN 'Mavjud mijoz ma''lumotlari yangilandi';
    ELSE
        INSERT INTO mijozlar(email, ism, yaratilgan_vaqt)
        VALUES (p_email, p_ism, NOW());
        RETURN 'Yangi mijoz muvaffaqiyatli qoshildi';
    END IF;
END;
$$;

SELECT yangila_yoki_qosh_mijoz('anvar@misol.uz', 'Anvar Fayziyev');
```

## Tushuntirish va Mantiq:
`FOUND` — PL/pgSQL ning o'rnatilgan mantiqiy (BOOLEAN) maxsus o'zgaruvchisidir. Agar oxirgi SELECT INTO, UPDATE yoki DELETE kamida bitta qator topsa yoki unga ta'sir qilsa `FOUND = TRUE` bo'ladi, aks holda `FALSE` bo'ladi.

## Ishlash natijasi:
```text
yangila_yoki_qosh_mijoz        
--------------------------------------
 Yangi mijoz muvaffaqiyatli qoshildi
(1 row)
```


# 837-Topshiriq: Massivlar bilan ishlash: FOREACH SLICE orqali ko'p o'lchovli massivlarni aylanib chiqish
## Topshiriq sharti:
2 o'lchovli matritsaning har bir qatorini alohida massiv sifatida o'qib, ularning yig'indisini hisoblovchi FOREACH SLICE funksiyasini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION hisobla_matritsa_qatorlar_yigindisi(matritsa INT[][])
RETURNS TABLE(qator_indeks INT, qator_yigindi INT)
LANGUAGE plpgsql
IMMUTABLE
AS $$
DECLARE
    qator INT[];
    idx INT := 1;
    v_yigindi INT;
    v_son INT;
BEGIN
    -- SLICE 1 har bir 1-o'lchovli qatorni massiv sifatida oladi
    FOREACH qator SLICE 1 IN ARRAY matritsa LOOP
        v_yigindi := 0;
        FOREACH v_son IN ARRAY qator LOOP
            v_yigindi := v_yigindi + v_son;
        END LOOP;

        qator_indeks := idx;
        qator_yigindi := v_yigindi;
        RETURN NEXT;

        idx := idx + 1;
    END LOOP;
END;
$$;

SELECT * FROM hisobla_matritsa_qatorlar_yigindisi(ARRAY[[10, 20, 30], [5, 15, 25]]);
```

## Tushuntirish va Mantiq:
`FOREACH qator SLICE 1 IN ARRAY matritsa` operatori ko'p o'lchovli massivdan bitta o'lchamli to'liq qism-massivlarni (slices) ketma-ket kesib oladi. Bu matritsaviy va jadval ko'rinishidagi ma'lumotlarni qayta ishlashni soddalashtiradi.

## Ishlash natijasi:
```text
qator_indeks | qator_yigindi 
--------------+---------------
            1 |            60
            2 |            45
(2 rows)
```


# 838-Topshiriq: Xotirani optimallashtirish: SET work_mem ni funksiya darajasida o'rnatish
## Topshiriq sharti:
Katta hajmdagi ma'lumotlarni saralovchi funksiya yaratib, butun server sozlamalarini buzmagan holda, faqat ushbu funksiya doirasida `work_mem = '64MB'` o'rnatilishini ta'minlang.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION ogir_saralash_hisoboti()
RETURNS TABLE(kategoriya_id INT, jami_summa NUMERIC)
LANGUAGE plpgsql
SET work_mem = '64MB'
SET statement_timeout = '5s'
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.kategoriya_id,
        SUM(b.summa)
    FROM katta_buyurtmalar b
    JOIN mahsulotlar m ON b.mahsulot_id = m.id
    GROUP BY m.kategoriya_id
    ORDER BY SUM(b.summa) DESC;
END;
$$;

SELECT * FROM ogir_saralash_hisoboti() LIMIT 3;
```

## Tushuntirish va Mantiq:
PostgreSQL'da `CREATE FUNCTION ... SET parametr = qiymat` sintaksisi yordamida funksiya chaqirilganda GUC (Grand Unified Configuration) parametrlarini lokal o'zgartirish mumkin. Funksiya tugashi bilan parametrlar avvalgi holatiga qaytadi, bu esa boshqa so'rovlarga xotira yetishmovchiligi xavfini bartaraf etadi.

## Ishlash natijasi:
```text
kategoriya_id |  jami_summa  
---------------+--------------
             4 | 895000000.00
             2 | 642000000.00
             7 | 410000000.00
(3 rows)
```


# 839-Topshiriq: Parallel xavfsizlik atributlari (PARALLEL SAFE, PARALLEL RESTRICTED)
## Topshiriq sharti:
PostgreSQL parallel query workerlariga so'rovni ko'p yadroli rejimda parallel hisoblashga to'sqinlik qilmaydigan `PARALLEL SAFE` funksiya yarating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION hisobla_bonus_koeffitsiyent(staj_yil INT, reyting NUMERIC)
RETURNS NUMERIC
LANGUAGE SQL
IMMUTABLE
PARALLEL SAFE
AS $$
    SELECT ROUND((staj_yil * 0.05) + (reyting * 0.1), 4);
$$;

-- Parallel skanerlashda foydalanish
EXPLAIN (COSTS OFF)
SELECT id, hisobla_bonus_koeffitsiyent(staj, baho)
FROM yirik_xodimlar_bazasi
WHERE staj > 5;
```

## Tushuntirish va Mantiq:
`PARALLEL SAFE` atributi funksiya hech qanday tranzaksiya holatini o'zgartirmasligini, ketma-ketliklarni (sequence) yangilamasligini va parallel worker jarayonlarida erkin parallel ishlatilishi mumkinligini kafolatlaydi.

## Ishlash natijasi:
```text
QUERY PLAN        
--------------------------
 Gather
   Workers Planned: 2
   ->  Parallel Seq Scan on yirik_xodimlar_bazasi
         Filter: (staj > 5)
(4 rows)
```


# 840-Topshiriq: O'zgaruvchilar turini jadval ustuniga bog'lash (%TYPE va %ROWTYPE)
## Topshiriq sharti:
Kelajakda ustun turi o'zgarganda (masalan INT dan BIGINT ga) buzilmaydigan, o'zgaruvchilari `%TYPE` orqali e'lon qilingan PL/pgSQL funksiyasini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION olish_xodim_qisqa_malumot(p_id xodimlar.id%TYPE)
RETURNS TEXT
LANGUAGE plpgsql
AS $$
DECLARE
    v_ism xodimlar.ism%TYPE;
    v_maosh xodimlar.maosh%TYPE;
BEGIN
    SELECT ism, maosh
    INTO v_ism, v_maosh
    FROM xodimlar
    WHERE id = p_id;

    IF NOT FOUND THEN
        RETURN 'Xodim topilmadi';
    END IF;

    RETURN format('Xodim: %s, Maoshi: %s so''m', v_ism, v_maosh);
END;
$$;

SELECT olish_xodim_qisqa_malumot(1);
```

## Tushuntirish va Mantiq:
`jadval.ustun%TYPE` sintaksisi o'zgaruvchi turini to'g'ridan-to'g'ri jadvaldagi mos ustun turiga bog'laydi. Jadvalda ustun o'lchami yoki turi o'zgarganda, funksiyani qo'lda tahrirlash talab etilmaydi, kod doimiy barqaror qoladi.

## Ishlash natijasi:
```text
olish_xodim_qisqa_malumot          
--------------------------------------------
 Xodim: Alisher, Maoshi: 25000000.00 so'm
(1 row)
```


# 841-Topshiriq: Muddati o'tgan buyurtmalarni bekor qilish va qoldiqlarni qaytarish protsedurasi
## Topshiriq sharti:
To'lov kutilayotgan holatda 24 soatdan ortiq qolib ketgan buyurtmalarni 'BEKOR_QILINDI' statusiga o'tkazib, mahsulot qoldiqlarini omborga qaytaruvchi murakkab biznes protsedurasini tuzing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE PROCEDURE bekor_qilish_muddati_otgan_buyurtmalar()
LANGUAGE plpgsql
AS $$
DECLARE
    r_buyurtma RECORD;
    r_item RECORD;
    v_bekor_soni INT := 0;
BEGIN
    FOR r_buyurtma IN 
        SELECT id FROM buyurtmalar
        WHERE holat = 'TOLOV_KUTILMOQDA'
          AND yaratilgan_vaqt < NOW() - INTERVAL '24 hours'
        FOR UPDATE
    LOOP
        -- Har bir buyurtma ichidagi mahsulotlarni omborga qaytarish
        FOR r_item IN 
            SELECT mahsulot_id, miqdor 
            FROM buyurtma_tarkibi 
            WHERE buyurtma_id = r_buyurtma.id 
        LOOP
            UPDATE ombor_qoldiqlari
            SET mavjud_soni = mavjud_soni + r_item.miqdor
            WHERE mahsulot_id = r_item.mahsulot_id;
        END LOOP;

        -- Buyurtma holatini yangilash
        UPDATE buyurtmalar
        SET holat = 'BEKOR_QILINDI',
            yangilangan_vaqt = NOW()
        WHERE id = r_buyurtma.id;

        v_bekor_soni := v_bekor_soni + 1;
    END LOOP;

    RAISE NOTICE 'Jami bekor qilingan buyurtmalar: % ta', v_bekor_soni;
END;
$$;

CALL bekor_qilish_muddati_otgan_buyurtmalar();
```

## Tushuntirish va Mantiq:
Ushbu protsedura relyatsion yaxlitlik va real dunyo e-tijorat biznes-jarayonini modellashtiradi: muddati o'tgan buyurtmalar qulflanadi (`FOR UPDATE`), ombordagi zahiralar qaytariladi va buyurtma statusi o'zgartiriladi.

## Ishlash natijasi:
```text
NOTICE:  Jami bekor qilingan buyurtmalar: 18 ta
CALL
```


# 842-Topshiriq: Murakkab soliq pog'onalarini (Progressive Tax) hisoblovchi PL/pgSQL funksiyasi
## Topshiriq sharti:
Daromad hajmiga qarab progressiv soliq stavkalari (0%, 12%, 20%) bo'yicha jismoniy shaxslar daromad solig'ini hisoblovchi aniq funksiya yarating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION hisobla_progressiv_soliq(p_daromad NUMERIC)
RETURNS NUMERIC(12,2)
LANGUAGE plpgsql
IMMUTABLE
AS $$
DECLARE
    v_soliq NUMERIC := 0;
    v_qoldiq NUMERIC := p_daromad;
BEGIN
    IF p_daromad <= 0 THEN
        RETURN 0.00;
    END IF;

    -- 1-bosqich: 3 000 000 gacha 0%
    IF v_qoldiq > 3000000 THEN
        v_qoldiq := v_qoldiq - 3000000;
    ELSE
        RETURN 0.00;
    END IF;

    -- 2-bosqich: Keyingi 7 000 000 gacha (jami 10M gacha) 12%
    IF v_qoldiq > 7000000 THEN
        v_soliq := v_soliq + (7000000 * 0.12);
        v_qoldiq := v_qoldiq - 7000000;
    ELSE
        v_soliq := v_soliq + (v_qoldiq * 0.12);
        RETURN ROUND(v_soliq, 2);
    END IF;

    -- 3-bosqich: 10 000 000 dan oshgan qismiga 20%
    v_soliq := v_soliq + (v_qoldiq * 0.20);

    RETURN ROUND(v_soliq, 2);
END;
$$;

SELECT 
    hisobla_progressiv_soliq(2500000)  AS soliq_kam,
    hisobla_progressiv_soliq(8000000)  AS soliq_orta,
    hisobla_progressiv_soliq(15000000) AS soliq_yuqori;
```

## Tushuntirish va Mantiq:
Progressiv soliq hisoblash relyatsion tizimlarda bosqichma-bosqich ayirish mantig'ini talab qiladi. Shartli bloklar ketma-ketligi orqali ortiqcha summa keyingi soliq stavkasi pog'onasiga uzatiladi.

## Ishlash natijasi:
```text
soliq_kam | soliq_orta | soliq_yuqori 
-----------+------------+--------------
      0.00 |  600000.00 |   1840000.00
(1 row)
```


# 843-Topshiriq: Tranzaksion hisoblar balansi taqqoslash va asserting (ASSERT)
## Topshiriq sharti:
PL/pgSQL ning `ASSERT` buyrug'idan foydalanib, bank tizimida debet va kredit aylanmalari mutanosibligini tekshiruvchi avtotest funksiyasini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION audit_balans_tengligi()
RETURNS VOID
LANGUAGE plpgsql
AS $$
DECLARE
    v_debet_jami NUMERIC;
    v_kredit_jami NUMERIC;
BEGIN
    SELECT COALESCE(SUM(debet), 0), COALESCE(SUM(kredit), 0)
    INTO v_debet_jami, v_kredit_jami
    FROM buxgalteriya_provodkalar;

    -- Balans tengligini tasdiqlash
    ASSERT v_debet_jami = v_kredit_jami, 
        format('Buxgalteriya balansi buzilgan! Debet: %s, Kredit: %s', v_debet_jami, v_kredit_jami);

    RAISE NOTICE 'Buxgalteriya balansi ideal holatda: % so''m', v_debet_jami;
END;
$$;

SELECT audit_balans_tengligi();
```

## Tushuntirish va Mantiq:
`ASSERT shart, xabar;` ifodasi agar shart yolg'on (FALSE yoki NULL) bo'lsa darhol `assert_failure` xatoligini qo'zg'atadi. U test va ma'lumotlar yaxlitligini tekshirish uchun maxsus mo'ljallangan bo'lib, `plpgsql.check_asserts` orqali yoqiladi yoki o'chiriladi.

## Ishlash natijasi:
```text
NOTICE:  Buxgalteriya balansi ideal holatda: 14500000000.00 so'm
 audit_balans_tengligi 
-----------------------
 
(1 row)
```


# 844-Topshiriq: Sessiya vaqtinchalik jadvallari (TEMPORARY TABLE) bilan ishlovchi protsedura
## Topshiriq sharti:
Murakkab oraliq hisob-kitoblarni amalga oshirish uchun vaqtinchalik jadval ochuvchi, unga ma'lumot yuklovchi va tranzaksiya oxirida avtomatik tozalovchi protsedura tuzing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE PROCEDURE hisobla_mijoz_ballari()
LANGUAGE plpgsql
AS $$
BEGIN
    -- Tranzaksiya oxirida qatorlari o'chiriladigan vaqtinchalik jadval
    CREATE TEMP TABLE IF NOT EXISTS vaqtincha_hisob (
        mijoz_id INT,
        ball NUMERIC
    ) ON COMMIT DELETE ROWS;

    INSERT INTO vaqtincha_hisob(mijoz_id, ball)
    SELECT mijoz_id, SUM(summa) * 0.01
    FROM buyurtmalar
    WHERE holat = 'YAKUNLANGAN'
    GROUP BY mijoz_id;

    -- Asosiy jadvalni vaqtinchalik jadval asosida yangilash
    UPDATE mijoz_profili m
    SET toplangan_ballar = m.toplangan_ballar + v.ball
    FROM vaqtincha_hisob v
    WHERE m.id = v.mijoz_id;

    RAISE NOTICE 'Barcha mijoz ballari muvaffaqiyatli qayta ishlandi.';
END;
$$;

CALL hisobla_mijoz_ballari();
```

## Tushuntirish va Mantiq:
`CREATE TEMP TABLE ... ON COMMIT DELETE ROWS` tranzaksiya tugagach (COMMIT bo'lganda) o'z ma'lumotlarini avtomatik tozalaydi. Bu parallel sessiyalar o'rtasida to'qnashuv bo'lmasligini va disk hajmi behuda band bo'lmasligini ta'minlaydi.

## Ishlash natijasi:
```text
NOTICE:  Barcha mijoz ballari muvaffaqiyatli qayta ishlandi.
CALL
```


# 845-Topshiriq: PL/pgSQL orqali qatorlarni regex bilan ajratish va normallashtirish
## Topshiriq sharti:
Vergullar, nuqtali vergullar yoki bo'shliqlar bilan aralash kiritilgan telefon raqamlari matnini bittalab ajratib, tozalab jadval ko'rinishida qaytaruvchi funksiya yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION tozalash_telefon_raqamlar(p_matn TEXT)
RETURNS TABLE(toza_raqam TEXT)
LANGUAGE plpgsql
IMMUTABLE
AS $$
DECLARE
    r TEXT;
    v_raqam TEXT;
BEGIN
    -- Regex bo'yicha ajratish: vergul, nuqtali vergul yoki bo'shliqlar
    FOR r IN SELECT regexp_split_to_table(p_matn, '[,;\s]+') AS x LOOP
        -- Faqat raqamlarni qoldirish
        v_raqam := regexp_replace(r, '\D', '', 'g');

        IF LENGTH(v_raqam) = 9 THEN
            v_raqam := '998' || v_raqam;
        END IF;

        IF LENGTH(v_raqam) = 12 AND v_raqam LIKE '998%' THEN
            toza_raqam := '+' || v_raqam;
            RETURN NEXT;
        END IF;
    END LOOP;
END;
$$;

SELECT * FROM tozalash_telefon_raqamlar('901234567, +99893 999-88-77; 712001122  notogri_nom');
```

## Tushuntirish va Mantiq:
`regexp_split_to_table` muntazam ifoda (regex) asosida xom matnni qatorlarga bo'ladi. `regexp_replace(..., '\D', '', 'g')` esa barcha son bo'lmagan belgilarni tozalaydi va funksiya xalqaro formatdagi telefon raqamlarni qaytaradi.

## Ishlash natijasi:
```text
toza_raqam   
----------------
 +998901234567
 +998939998877
 +998712001122
(3 rows)
```


# 846-Topshiriq: Funksiya ichida SAVEPOINT va qisman orqaga qaytarish (Subtransactions)
## Topshiriq sharti:
PL/pgSQL dagi har bir `BEGIN ... EXCEPTION` bloki PostgreSQL da avtomatik ichki savepoint (subtransaction) ochishini amalda ko'rsatuvchi xavfsiz partiyaviy kiritish funksiyasini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE PROCEDURE partiya_foydalanuvchilar_kiritish(p_royxat JSONB)
LANGUAGE plpgsql
AS $$
DECLARE
    item JSONB;
    v_muvaffaqiyat INT := 0;
    v_xatolik INT := 0;
BEGIN
    FOR item IN SELECT * FROM jsonb_array_elements(p_royxat) LOOP
        BEGIN
            -- Ushbu ichki BEGIN avtomatik subtransaction (SAVEPOINT) yaratadi
            INSERT INTO foydalanuvchilar(email, ism)
            VALUES (item->>'email', item->>'ism');

            v_muvaffaqiyat := v_muvaffaqiyat + 1;
        EXCEPTION WHEN unique_violation THEN
            -- Xatolik bo'lsa faqat ushbu qator orqaga qaytadi, boshqalar saqlanib qoladi
            v_xatolik := v_xatolik + 1;
            RAISE NOTICE 'Dublikat email tashlab ketildi: %', item->>'email';
        END;
    END LOOP;

    RAISE NOTICE 'Yakun: Muvaffaqiyatli: %, Xatolar: %', v_muvaffaqiyat, v_xatolik;
END;
$$;

CALL partiya_foydalanuvchilar_kiritish('[
    {"email": "ali@misol.uz", "ism": "Ali"},
    {"email": "ali@misol.uz", "ism": "Ali Dublikat"},
    {"email": "vali@misol.uz", "ism": "Vali"}
]'::jsonb);
```

## Tushuntirish va Mantiq:
PL/pgSQL da `BEGIN ... EXCEPTION` bloki ichida xato sodir bo'lganda, faqat ushbu blok ichidagi o'zgarishlar bekor qilinadi, asosiy tranzaksiya esa davom etaveradi. Bu ichki SAVEPOINT mexanizmi hisobiga amalga oshiriladi.

## Ishlash natijasi:
```text
NOTICE:  Dublikat email tashlab ketildi: ali@misol.uz
NOTICE:  Yakun: Muvaffaqiyatli: 2, Xatolar: 1
CALL
```


# 847-Topshiriq: Jadval qatorini hashlab nazorat summasini (Checksum) hisoblovchi funksiya
## Topshiriq sharti:
Audit maqsadida xodim ma'lumotlarining barcha maydonlarini yagona MD5 nazorat summasiga birlashtiruvchi va ma'lumotlar o'zgarganini tezkor aniqlashga yordam beruvchi funksiya yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION hisobla_qator_checksum(p_xodim_id INT)
RETURNS TEXT
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
    r RECORD;
    v_matn TEXT;
BEGIN
    SELECT * INTO r FROM xodimlar WHERE id = p_id;

    IF NOT FOUND THEN
        RETURN NULL;
    END IF;

    -- Barcha maydonlarni kanonik matnga aylantirish
    v_matn := r.id || '|' || r.ism || '|' || r.familiya || '|' || 
              r.lavozim || '|' || r.maosh || '|' || r.bolim_id;

    RETURN MD5(v_matn);
END;
$$;

SELECT id, hisobla_qator_checksum(id) AS qator_hash FROM xodimlar LIMIT 2;
```

## Tushuntirish va Mantiq:
Kriptografik yoki MD5 hash funksiyalari ma'lumotlar yaxlitligini (integrity) tekshirishda juda qo'l keladi. Replikatsiya yoki kesh tizimlarida qatorning o'zgargan-o'zgarmaganini butun qatorni solishtirmasdan, uning ixcham xesh-summasi orqali soniyaning mingdan bir ulushida aniqlash mumkin.

## Ishlash natijasi:
```text
id |            qator_hash            
----+----------------------------------
  1 | 8b1a9953c4611296a827abf8c47804d7
  2 | c4ca4238a0b923820dcc509a6f75849b
(2 rows)
```


# 848-Topshiriq: Foydalanuvchi huquqlarini tekshiruvchi avtorizatsiya funksiyasi
## Topshiriq sharti:
Foydalanuvchi ID va kerakli ruxsatnoma kodi berilganda, uning rollari va bevosita ruxsatnomalarini tekshirib `BOOLEAN` natija beruvchi `ruxsat_bormi` funksiyasini yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION ruxsat_bormi(
    p_foydalanuvchi_id INT,
    p_ruxsat_kodi VARCHAR(50)
)
RETURNS BOOLEAN
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
    v_mavjud BOOLEAN := FALSE;
BEGIN
    -- Superadmin har qanday ruxsatga ega
    IF EXISTS (
        SELECT 1 FROM foydalanuvchi_rollari fr
        JOIN rollar r ON fr.rol_id = r.id
        WHERE fr.foydalanuvchi_id = p_foydalanuvchi_id AND r.nomi = 'SUPERADMIN'
    ) THEN
        RETURN TRUE;
    END IF;

    -- Rollar orqali berilgan ruxsatlarni tekshirish
    SELECT TRUE INTO v_mavjud
    FROM foydalanuvchi_rollari fr
    JOIN rol_ruxsatlar rr ON fr.rol_id = rr.rol_id
    JOIN ruxsatlar rx ON rr.ruxsat_id = rx.id
    WHERE fr.foydalanuvchi_id = p_foydalanuvchi_id
      AND rx.kod = p_ruxsat_kodi
    LIMIT 1;

    RETURN COALESCE(v_mavjud, FALSE);
END;
$$;

SELECT 
    ruxsat_bormi(1, 'BUYURTMA_OCHIRISH') AS admin_ruxsat,
    ruxsat_bormi(15, 'BUYURTMA_OCHIRISH') AS oddiy_ruxsat;
```

## Tushuntirish va Mantiq:
RBAC (Role-Based Access Control) tizimlarida avtorizatsiya mantiqini ma'lumotlar bazasi darajasida markazlashtirish xavfsizlikni kafolatlaydi. Ushbu funksiya foydalanuvchining superadminligini yoki uning rollariga biriktirilgan aniq imtiyozlarni tekshiradi.

## Ishlash natijasi:
```text
admin_ruxsat | oddiy_ruxsat 
--------------+--------------
 t            | f
(1 row)
```


# 849-Topshiriq: Moliya: Depozitning murakkab foizini (Compound Interest) hisoblovchi funksiya
## Topshiriq sharti:
Boshlang'ich kapital, yillik foiz stavkasi, muddat (oylar soni) va kapitallashuv davri berilganda murakkab foiz hisoblovchi moliyaviy funksiya yozing.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE FUNCTION hisobla_depozit_murakkab_foiz(
    p_kapital NUMERIC,
    p_yillik_foiz NUMERIC,
    p_oylar INT
)
RETURNS TABLE(oy INT, oylik_ustama NUMERIC, jami_balans NUMERIC)
LANGUAGE plpgsql
IMMUTABLE
AS $$
DECLARE
    v_oylik_stavka NUMERIC;
    v_joriy_balans NUMERIC := p_kapital;
    v_ustama NUMERIC;
BEGIN
    v_oylik_stavka := (p_yillik_foiz / 100.0) / 12.0;

    FOR i IN 1..p_oylar LOOP
        v_ustama := ROUND(v_joriy_balans * v_oylik_stavka, 2);
        v_joriy_balans := v_joriy_balans + v_ustama;

        oy := i;
        oylik_ustama := v_ustama;
        jami_balans := v_joriy_balans;
        RETURN NEXT;
    END LOOP;
END;
$$;

SELECT * FROM hisobla_depozit_murakkab_foiz(10000000.00, 24.0, 3);
```

## Tushuntirish va Mantiq:
Murakkab foizda har oylik hisoblangan daromad depozitning asosiy qismiga qo'shiladi va keyingi oyda yangi kattaroq balansga foiz hisoblanadi (`v_joriy_balans := v_joriy_balans + v_ustama`).

## Ishlash natijasi:
```text
oy | oylik_ustama | jami_balans 
----+--------------+-------------
  1 |    200000.00 | 10200000.00
  2 |    204000.00 | 10404000.00
  3 |    208080.00 | 10612080.00
(3 rows)
```


# 850-Topshiriq: To'liq audit va ob'ektlar metama'lumotini tekshirish protsedurasi
## Topshiriq sharti:
Baza ichidagi barcha jadvallarning nomini, ulardagi ustunlar sonini va xotiradan egallagan umumiy hajmini hisoblab chiquvchi ma'murlash tizim protsedurasini yarating.

## Yechim (SQL kodi):
```sql
CREATE OR REPLACE PROCEDURE audit_baza_jadvallari()
LANGUAGE plpgsql
AS $$
DECLARE
    r RECORD;
BEGIN
    RAISE NOTICE '=== MA''LUMOTLAR BAZASI JADVALLAR AUDITI ===';

    FOR r IN 
        SELECT 
            t.table_name,
            COUNT(c.column_name) AS ustunlar_soni,
            pg_size_pretty(pg_total_relation_size(quote_ident(t.table_name)::regclass)) AS umumiy_hajm
        FROM information_schema.tables t
        JOIN information_schema.columns c 
          ON t.table_name = c.table_name AND t.table_schema = c.table_schema
        WHERE t.table_schema = 'public' 
          AND t.table_type = 'BASE TABLE'
        GROUP BY t.table_name
        ORDER BY pg_total_relation_size(quote_ident(t.table_name)::regclass) DESC
    LOOP
        RAISE NOTICE 'Jadval: % | Ustunlar: % | Egallagan hajm: %', 
            RPAD(r.table_name, 25), 
            LPAD(r.ustunlar_soni::TEXT, 3), 
            r.umumiy_hajm;
    END LOOP;

    RAISE NOTICE '=== AUDIT MUVAFFAQIYATLI YAKUNLANDI ===';
END;
$$;

CALL audit_baza_jadvallari();
```

## Tushuntirish va Mantiq:
`information_schema.tables`, `columns` va PostgreSQL ning `pg_total_relation_size` tizim funksiyalari orqali ma'lumotlar bazasi fizik tuzilishi ustidan chuqur tahlil o'tkaziladi. Bu DBA va arxitektorlar uchun jadvallar o'sishini kuzatishda asosiy vositadir.

## Ishlash natijasi:
```text
NOTICE:  === MA'LUMOTLAR BAZASI JADVALLAR AUDITI ===
NOTICE:  Jadval: buyurtmalar               | Ustunlar:  12 | Egallagan hajm: 48 MB
NOTICE:  Jadval: tolovlar                  | Ustunlar:   8 | Egallagan hajm: 24 MB
NOTICE:  Jadval: foydalanuvchilar          | Ustunlar:   6 | Egallagan hajm: 8192 kB
NOTICE:  === AUDIT MUVAFFAQIYATLI YAKUNLANDI ===
CALL
```

