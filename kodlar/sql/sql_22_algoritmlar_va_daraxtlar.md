# Khorazmiy AI: SQL - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: Graflarda qisqa yo'lni aniqlash (Dijkstra analogi)
**Tavsif:** Logistika tizimida shaharlararo eng arzon yo'nalishni topish.
**Talablar:** Rekursiv CTE yordamida eng qisqa masofani hisoblash, xavfsizlik uchun sikllarni (cycles) oldini olish.
**Yechim (SQL):**
```sql
WITH RECURSIVE ShortestPath AS (
    -- Boshlang'ich nuqta
    SELECT target_id, cost FROM routes WHERE source_id = 1
    UNION ALL
    -- Rekursiv qadam
    SELECT r.target_id, sp.cost + r.cost
    FROM routes r
    JOIN ShortestPath sp ON r.source_id = sp.target_id
    WHERE sp.cost + r.cost < 1000 -- Maksimal limit
)
SELECT target_id, MIN(cost) as min_cost FROM ShortestPath GROUP BY target_id;
```
**Tushuntirish:** Rekursiv CTE graflarni travers qilish uchun eng samarali SQL vositasidir. `WHERE` bandi orqali cheksiz sikllar va ortiqcha hisoblashlar cheklanadi.

### Topshiriq #1052: Segment Tree yordamida vaqtinchalik agregatsiya
**Tavsif:** Katta hajmdagi moliyaviy tranzaksiyalarni vaqt oralig'i bo'yicha tezkor yig'ish.
**Talablar:** Indekslash strategiyasi va `RANGE` funksiyasidan foydalanish.
**Yechim (SQL):**
```sql
SELECT transaction_date, 
       SUM(amount) OVER (ORDER BY transaction_date RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW) as rolling_sum
FROM transactions;
```
**Tushuntirish:** Segment Tree mantiqini SQL'da `Window Functions` orqali amalga oshirish, ma'lumotlar bazasining ichki indekslaridan foydalangan holda O(log n) tezlikka erishish imkonini beradi.

### Topshiriq #1053: Fenwick Tree (Binary Indexed Tree) mantiqiy yig'indisi
**Tavsif:** Real vaqt rejimida kümülatif statistikalarni yangilash.
**Talablar:** Tranzaksiya jadvalida prefiks yig'indilarni (prefix sums) saqlash.
**Yechim (SQL):**
```sql
-- Fenwick Tree tuzilmasini simulyatsiya qiluvchi yangilash funksiyasi
UPDATE bit_table 
SET val = val + :new_val 
WHERE idx IN (SELECT bit_index FROM bit_mapping WHERE target_idx = :target);
```
**Tushuntirish:** Fenwick Tree yordamida yig'indilarni yangilash va o'qish O(log n) murakkablikda bo'ladi, bu esa katta hajmli ma'lumotlar oqimida yuqori unumdorlik beradi.

### Topshiriq #1054: Trie (Prefix Tree) qidiruv tizimi
**Tavsif:** Foydalanuvchi qidiruv so'rovlarini avtomatik to'ldirish (autocomplete).
**Talablar:** Satrlar bo'yicha ierarxik qidiruv va `LIKE` operatoridan qochish.
**Yechim (SQL):**
```sql
SELECT word FROM trie_nodes 
WHERE prefix = SUBSTRING(:input, 1, length) 
ORDER BY frequency DESC LIMIT 10;
```
**Tushuntirish:** Trie tuzilmasi SQL'da jadval ko'rinishida saqlanadi. Bu `LIKE '%...%'` dan foydalanishdan ko'ra ming barobar tezroq, chunki u indekslangan prefikslarga tayanadi.

### Topshiriq #1055: Graflarda bog'liqlik tahlili (Transitive Closure)
**Tavsif:** Korporativ ierarxiyada bo'ysunuvchilarni aniqlash.
**Talablar:** `CONNECT BY` yoki rekursiv CTE yordamida ierarxik daraxtni qurish.
**Yechim (SQL):**
```sql
WITH RECURSIVE OrgChart AS (
    SELECT id, manager_id, name FROM employees WHERE id = :root_id
    UNION ALL
    SELECT e.id, e.manager_id, e.name 
    FROM employees e 
    JOIN OrgChart o ON e.manager_id = o.id
)
SELECT * FROM OrgChart;
```
**Tushuntirish:** Bu yondashuv graflardagi "reachability" muammosini hal qiladi, bu esa katta tashkilotlar ma'lumotlar bazasida juda muhim.

### Topshiriq #1056: Segment Tree orqali Range Maximum Query (RMQ)
**Tavsif:** Sensor ma'lumotlaridan eng yuqori qiymatni tezkor topish.
**Talablar:** Ma'lumotlarni bloklarga bo'lish va har bir blok uchun `MAX` qiymatini saqlash.
**Yechim (SQL):**
```sql
SELECT MAX(sensor_value) 
FROM sensor_data 
WHERE block_id BETWEEN :start_block AND :end_block;
```
**Tushuntirish:** Ma'lumotlarni bloklarga (Segmentlarga) ajratish orqali qidiruv maydonini keskin qisqartiramiz, bu esa katta jadvallarda skanerlash vaqtini kamaytiradi.

### Topshiriq #1057: Fenwick Tree yordamida chastotali tahlil
**Tavsif:** Foydalanuvchi faolligini vaqt bo'yicha hisoblash.
**Talablar:** `BIT` jadvalida chastotalarni saqlash va yangilash.
**Yechim (SQL):**
```sql
-- Chastotani yangilash
UPDATE frequency_bit SET count = count + 1 WHERE bit_pos = :current_time_slot;
-- Yig'indini olish
SELECT SUM(count) FROM frequency_bit WHERE bit_pos <= :query_time;
```
**Tushuntirish:** Fenwick Tree yordamida vaqtinchalik qatorlarni (time-series) samarali boshqarish, xotira sarfini optimallashtiradi.

### Topshiriq #1058: Trie asosida domen nomlarini filtrlash
**Tavsif:** Qora ro'yxatdagi (blacklist) domenlarni tezkor aniqlash.
**Talablar:** Domen qismlarini ierarxik saqlash va qidirish.
**Yechim (SQL):**
```sql
SELECT domain_name FROM blacklist 
WHERE domain_path @> ARRAY['com', 'example', 'malware'];
```
**Tushuntirish:** PostgreSQL'ning `ltree` yoki `array` turlaridan foydalanish Trie tuzilmasini SQL'da implementatsiya qilishning eng zamonaviy va tezkor usulidir.

### Topshiriq #1059: Graflarda eng uzun yo'lni topish (DAG)
**Tavsif:** Ish jarayonlari (workflow) ketma-ketligini optimallashtirish.
**Talablar:** `DAG` (Directed Acyclic Graph) xususiyatidan foydalanish.
**Yechim (SQL):**
```sql
WITH RECURSIVE PathFinder AS (
    SELECT id, duration, CAST(id AS TEXT) as path FROM tasks WHERE parent_id IS NULL
    UNION ALL
    SELECT t.id, pf.duration + t.duration, pf.path || '->' || t.id
    FROM tasks t
    JOIN PathFinder pf ON t.parent_id = pf.id
)
SELECT MAX(duration) FROM PathFinder;
```
**Tushuntirish:** Rekursiv CTE orqali barcha yo'llarni hisoblab, eng uzunini (kritik yo'lni) topish loyiha boshqaruvida juda muhimdir.

### Topshiriq #1060: Segment Tree yordamida dinamik yangilanish
**Tavsif:** Inventar qoldiqlarini real vaqtda kuzatish.
**Talablar:** `UPSERT` operatsiyalari va segmentlangan indekslar.
**Yechim (SQL):**
```sql
INSERT INTO inventory_tree (node_id, total_stock)
VALUES (:node, :stock)
ON CONFLICT (node_id) DO UPDATE SET total_stock = inventory_tree.total_stock + EXCLUDED.total_stock;
```
**Tushuntirish:** `ON CONFLICT` (Upsert) funksiyasi Segment Tree tugunlarini yangilashda ma'lumotlar yaxlitligini ta'minlaydi va raqobatbardosh yozish (concurrent writes) holatlarida xatolarni oldini oladi.

---

### Topshiriq #1061: Graflarda Qisqa Yo'lni Aniqlash (Dijkstra SQL implementatsiyasi)
**Tavsif:** Logistika tizimida shaharlararo eng arzon yo'nalishni topish.
**Talablar:** `edges` jadvalidan foydalanib, rekursiv CTE orqali eng qisqa masofani hisoblash.
**Yechim (SQL):**
```sql
WITH RECURSIVE Dijkstra AS (
    -- Boshlang'ich tugun
    SELECT target_node, weight AS total_cost FROM edges WHERE source_node = 1
    UNION ALL
    SELECT e.target_node, d.total_cost + e.weight
    FROM edges e
    JOIN Dijkstra d ON e.source_node = d.target_node
    WHERE d.total_cost < 1000 -- Xavfsizlik chegarasi
)
SELECT target_node, MIN(total_cost) FROM Dijkstra GROUP BY target_node;
```
**Tushuntirish:** Rekursiv CTE yordamida graf bo'ylab yurish amalga oshirildi. `total_cost` chegarasi cheksiz sikllarni oldini olish uchun qo'yildi.

### Topshiriq #1062: Segment Tree yordamida Oraliq Summani Hisoblash
**Tavsif:** Moliya tizimida vaqt oralig'idagi tranzaksiyalar yig'indisini tezkor olish.
**Talablar:** O(log n) murakkablikda so'rovlarni qayta ishlash.
**Yechim (SQL):**
```sql
-- Segment Tree jadvalini yaratish va so'rov
SELECT SUM(val) FROM segment_tree 
WHERE node_range_start >= 10 AND node_range_end <= 50;
-- Indekslash: node_range_start va node_range_end ustunlariga B-Tree indeksi qo'shilgan
```
**Tushuntirish:** Segment Tree tuzilmasi ma'lumotlarni ierarxik saqlash orqali katta hajmdagi ma'lumotlar orasidan oraliq yig'indini tezkor aniqlash imkonini beradi.

### Topshiriq #1063: Fenwick Tree (Binary Indexed Tree) bilan Kümülatif Summa
**Tavsif:** Real vaqt rejimida yangilanib turuvchi reyting tizimi.
**Talablar:** Yangilanish va o'qish operatsiyalarini O(log n) tezlikda bajarish.
**Yechim (SQL):**
```sql
-- Fenwick Tree yordamida qiymatni yangilash
UPDATE fenwick_tree SET val = val + 50 
WHERE idx IN (1, 2, 4, 8); -- Bitwise operatsiyalar natijasida olingan indekslar
```
**Tushuntirish:** Fenwick Tree massivni yangilash va yig'indini hisoblashda Segment Tree'ga qaraganda kamroq xotira talab qiladi.

### Topshiriq #1064: Trie (Prefix Tree) yordamida Avtomatik To'ldirish
**Tavsif:** Foydalanuvchi qidiruv so'rovlarini tezkor taklif qilish.
**Talablar:** Prefiks bo'yicha qidiruvni O(m) vaqtda bajarish (m - so'z uzunligi).
**Yechim (SQL):**
```sql
SELECT word FROM trie_nodes 
WHERE prefix_path LIKE 'uzb%' 
ORDER BY frequency DESC LIMIT 10;
```
**Tushuntirish:** Trie tuzilmasi prefikslarni ierarxik saqlaydi, bu esa `LIKE` operatori bilan birgalikda juda tez qidiruvni ta'minlaydi.

### Topshiriq #1065: Graflarda Transitive Closure (Bog'liqliklar)
**Tavsif:** Mikroservislar arxitekturasida bog'liqliklar zanjirini aniqlash.
**Talablar:** Barcha bog'liq tugunlarni aniqlash.
**Yechim (SQL):**
```sql
WITH RECURSIVE DependencyGraph AS (
    SELECT parent_id, child_id FROM dependencies
    UNION
    SELECT dg.parent_id, d.child_id
    FROM DependencyGraph dg
    JOIN dependencies d ON dg.child_id = d.parent_id
)
SELECT * FROM DependencyGraph;
```
**Tushuntirish:** Rekursiv bog'liqliklar orqali tizimning to'liq ierarxik tuzilishini (transitive closure) ochib beradi.

### Topshiriq #1066: Segment Tree yordamida Range Minimum Query (RMQ)
**Tavsif:** Sensor ma'lumotlarida minimal qiymatni aniqlash.
**Talablar:** O(log n) vaqtda minimal qiymatni topish.
**Yechim (SQL):**
```sql
SELECT MIN(min_val) FROM segment_tree_nodes 
WHERE range_start >= 100 AND range_end <= 200;
```
**Tushuntirish:** Segment Tree tugunlarida oraliqning minimal qiymati saqlanadi, bu esa butun jadvalni skanerlashdan ko'ra samaraliroq.

### Topshiriq #1067: Fenwick Tree yordamida Chastotani Hisoblash
**Tavsif:** Saytga tashrif buyuruvchilarning kunlik statistikasini yuritish.
**Talablar:** Ma'lumotlarni samarali jamlash.
**Yechim (SQL):**
```sql
-- Fenwick Tree tuzilmasida qiymatni qo'shish
UPDATE bit_table SET bit_value = bit_value + 1 
WHERE bit_index = (SELECT MAX(bit_index) FROM bit_table WHERE bit_index <= 1024);
```
**Tushuntirish:** Bitwise indekslash yordamida ma'lumotlar qatorini tezkor yangilash va yig'indini olish imkonini beradi.

### Topshiriq #1068: Trie yordamida IP-manzillar Prefiksini Qidirish
**Tavsif:** Tarmoq xavfsizligi (Firewall) qoidalarini tekshirish.
**Talablar:** IP prefiksiga mos keladigan qoidalarni topish.
**Yechim (SQL):**
```sql
SELECT rule_id FROM firewall_trie 
WHERE ip_prefix = SUBSTRING('192.168.1.1', 1, 7);
```
**Tushuntirish:** Trie tuzilmasi IP manzillarni bitli ierarxiyada saqlash uchun eng maqbul yechimdir.

### Topshiriq #1069: Graflarda Sikllarni Aniqlash
**Tavsif:** Ma'lumotlar bazasidagi o'zaro bog'liq jadvallarda sikllarni (deadlock) topish.
**Talablar:** Sikl mavjudligini aniqlash va xabar berish.
**Yechim (SQL):**
```sql
SELECT source_node, target_node FROM edges 
WHERE source_node = target_node OR EXISTS (
    SELECT 1 FROM edges e2 WHERE e2.source_node = edges.target_node 
    AND e2.target_node = edges.source_node
);
```
**Tushuntirish:** To'g'ridan-to'g'ri bog'liqliklar va teskari bog'liqliklarni tekshirish orqali oddiy sikllarni aniqlaydi.

### Topshiriq #1070: Segment Tree yordamida Dinamik Yangilanish
**Tavsif:** Narxlar o'zgarishini real vaqtda kuzatish.
**Talablar:** Yangilanishdan so'ng oraliq yig'indini qayta hisoblash.
**Yechim (SQL):**
```sql
-- Yangilanish operatsiyasi
UPDATE segment_tree SET val = 500 WHERE node_id = 45;
-- Yig'indini qayta hisoblash (Trigger orqali avtomatlashtirilishi mumkin)
SELECT SUM(val) FROM segment_tree WHERE parent_id = 10;
```
**Tushuntirish:** Segment Tree'da bitta barg tugunining o'zgarishi faqat uning ota tugunlariga ta'sir qiladi, bu esa butun jadvalni qayta hisoblashdan saqlaydi.

---

### Topshiriq #1071: Graflarda Qisqa Yo'lni Topish (Dijkstra SQL implementatsiyasi)
**Tavsif:** Logistika tizimida shaharlararo eng arzon yo'nalishni aniqlash.
**Talablar:** `edges` jadvalidan foydalanib, rekursiv CTE orqali eng qisqa masofani hisoblash.
**Yechim (SQL):**
```sql
WITH RECURSIVE Dijkstra AS (
    -- Boshlang'ich nuqta
    SELECT target_node, cost FROM edges WHERE source_node = 1
    UNION ALL
    SELECT e.target_node, d.cost + e.cost
    FROM edges e
    JOIN Dijkstra d ON e.source_node = d.target_node
    WHERE d.cost + e.cost < 1000 -- Maksimal limit
)
SELECT target_node, MIN(cost) as min_cost FROM Dijkstra GROUP BY target_node;
```
**Tushuntirish:** Rekursiv CTE graflarni o'tishda samarali, `MIN` funksiyasi esa eng optimal yo'lni tanlashni ta'minlaydi.

### Topshiriq #1072: Segment Tree yordamida diapazon yig'indisi
**Tavsif:** Moliya tizimida vaqt oralig'idagi tranzaksiyalar yig'indisini tezkor hisoblash.
**Talablar:** `O(log n)` murakkablikdagi so'rovlar uchun indekslangan jadval tuzilmasi.
**Yechim (SQL):**
```sql
-- Segment Tree tugunlarini saqlash jadvali
CREATE TABLE segment_tree (node_id INT PRIMARY KEY, val DECIMAL(18,2));

-- Diapazon yig'indisini olish funksiyasi
CREATE FUNCTION get_sum(l INT, r INT) RETURNS DECIMAL AS $$
BEGIN
    RETURN (SELECT SUM(val) FROM segment_tree WHERE node_id BETWEEN l AND r);
END;
$$ LANGUAGE plpgsql;
```
**Tushuntirish:** Segment Tree katta hajmdagi ma'lumotlar ustida agregatsiyani tezlashtiradi.

### Topshiriq #1073: Fenwick Tree (Binary Indexed Tree) yordamida yangilanish
**Tavsif:** Real vaqt rejimida hisob balanslarini yangilash va prefiks yig'indisini olish.
**Talablar:** `UPDATE` operatsiyasini `O(log n)` vaqtda bajarish.
**Yechim (SQL):**
```sql
-- Fenwick Tree yangilash protsedurasi
CREATE PROCEDURE update_fenwick(idx INT, delta DECIMAL)
LANGUAGE plpgsql AS $$
BEGIN
    WHILE idx <= 100000 LOOP
        UPDATE fenwick_table SET val = val + delta WHERE id = idx;
        idx := idx + (idx & -idx); -- BIT operatsiyasi
    END LOOP;
END;
$$;
```
**Tushuntirish:** Fenwick Tree xotira tejamkorligi va tezkor yangilanishi bilan ajralib turadi.

### Topshiriq #1074: Trie (Prefix Tree) yordamida qidiruv
**Tavsif:** Foydalanuvchi qidiruv so'rovlarini avtomatik to'ldirish (Autocomplete).
**Talablar:** Satr prefiksi bo'yicha eng yaqin mosliklarni topish.
**Yechim (SQL):**
```sql
-- Trie tugunlari jadvali
CREATE TABLE trie (id INT, char_val CHAR(1), parent_id INT, is_end BOOLEAN);

-- Prefiks bo'yicha qidiruv
SELECT * FROM trie 
WHERE char_val LIKE 'A%' -- 'A' bilan boshlanuvchi so'zlar
AND parent_id IS NULL;
```
**Tushuntirish:** Trie tuzilmasi matnli ma'lumotlarni ierarxik saqlash orqali qidiruvni optimallashtiradi.

### Topshiriq #1075: Graflarda bog'liqlik komponentlarini aniqlash
**Tavsif:** Ijtimoiy tarmoqlarda o'zaro bog'liq foydalanuvchilar guruhini ajratish.
**Talablar:** `Union-Find` algoritmini SQLda simulyatsiya qilish.
**Yechim (SQL):**
```sql
WITH RECURSIVE Components AS (
    SELECT user_id, friend_id as root FROM connections
    UNION
    SELECT c.user_id, f.friend_id 
    FROM Components c
    JOIN connections f ON c.root = f.user_id
)
SELECT user_id, MIN(root) as group_id FROM Components GROUP BY user_id;
```
**Tushuntirish:** Rekursiya orqali graflardagi "orol" (island) komponentlarni topish imkonini beradi.

### Topshiriq #1076: Segment Tree yordamida Range Maximum Query (RMQ)
**Tavsif:** Sensor ma'lumotlarida eng yuqori qiymatni aniqlash.
**Talablar:** `O(log n)` vaqtda maksimal qiymatni qaytarish.
**Yechim (SQL):**
```sql
-- Maksimal qiymatni saqlovchi segment tugunlari
SELECT MAX(val) FROM segment_tree 
WHERE node_id IN (SELECT id FROM tree_map WHERE range_start >= 10 AND range_end <= 50);
```
**Tushuntirish:** Segment Tree tuzilmasi katta diapazonlardagi ekstremal qiymatlarni tez topishga imkon beradi.

### Topshiriq #1077: Trie yordamida IP manzillarni filtrlash
**Tavsif:** Tarmoq xavfsizligi uchun IP prefikslarini tezkor tekshirish.
**Talablar:** Trie daraxti orqali IP maskalarini moslashtirish.
**Yechim (SQL):**
```sql
-- IP prefiks qidiruvi
SELECT network_id FROM ip_trie 
WHERE path_sequence @> ARRAY['192', '168'];
```
**Tushuntirish:** `ARRAY` va `Trie` kombinatsiyasi tarmoq marshrutlarini tasniflashda juda samarali.

### Topshiriq #1078: Fenwick Tree orqali chastotali tahlil
**Tavsif:** Saytga tashrif buyuruvchilar sonini vaqt bo'yicha yig'ish.
**Talablar:** `O(log n)` murakkablikda statistikani yangilash.
**Yechim (SQL):**
```sql
-- Tashriflar sonini yangilash
UPDATE fenwick_stats 
SET val = val + 1 
WHERE id = (SELECT id FROM fenwick_stats WHERE time_slot = CURRENT_DATE);
```
**Tushuntirish:** Fenwick daraxti vaqt seriyali ma'lumotlarni yig'ishda eng kam yuklama beruvchi yechimdir.

### Topshiriq #1079: Graflarda sikllarni aniqlash
**Tavsif:** Moliyaviy firibgarlik (pul oqimi sikllari) ni aniqlash.
**Talablar:** `Cycle Detection` algoritmi orqali yopiq graflarni topish.
**Yechim (SQL):**
```sql
SELECT source_node, target_node FROM transactions
WHERE source_node = target_node 
OR EXISTS (SELECT 1 FROM transactions t2 WHERE t2.source_node = transactions.target_node 
           AND t2.target_node = transactions.source_node);
```
**Tushuntirish:** Tranzaksiyalar zanjiridagi teskari bog'lanishlarni tekshirish firibgarlikni oldini oladi.

### Topshiriq #1080: Segment Tree yordamida ma'lumotlarni siqish
**Tavsif:** Katta hajmli log fayllarni samarali saqlash va so'rov berish.
**Talablar:** Ma'lumotlarni ierarxik guruhlash.
**Yechim (SQL):**
```sql
-- Ierarxik guruhlash
SELECT level, SUM(val) 
FROM segment_tree 
GROUP BY level ORDER BY level DESC;
```
**Tushuntirish:** Segment Tree darajalari (level) bo'yicha guruhlash ma'lumotlarni tahlil qilishni osonlashtiradi.

---

### Topshiriq #1081: Graflarda Qisqa Yo'lni Topish (Dijkstra)
**Tavsif:** Logistika tizimida omborlar orasidagi eng arzon yetkazib berish yo'nalishini aniqlash.
**Talablar:** Rekursiv CTE yordamida eng kam vaznli yo'lni topish, `Dijkstra` algoritmi mantig'ini SQLda simulyatsiya qilish.
**Yechim (SQL):**
```sql
WITH RECURSIVE ShortestPath AS (
    -- Boshlang'ich tugun
    SELECT target_id, cost FROM routes WHERE source_id = 1
    UNION ALL
    SELECT r.target_id, sp.cost + r.cost
    FROM routes r
    JOIN ShortestPath sp ON r.source_id = sp.target_id
    WHERE sp.cost + r.cost < 1000 -- Maksimal limit
)
SELECT target_id, MIN(cost) as min_cost 
FROM ShortestPath GROUP BY target_id;
```
**Tushuntirish:** Rekursiv CTE graflarni bosib o'tish uchun ishlatildi. `MIN` funksiyasi va `GROUP BY` orqali har bir tugun uchun eng optimal qiymat saqlab qolindi.

### Topshiriq #1082: Segment Tree yordamida Range Sum Query
**Tavsif:** Moliya tizimida vaqt oralig'idagi tranzaksiyalar yig'indisini tezkor hisoblash.
**Talablar:** `O(log n)` murakkablikda ma'lumotlarni olish, indekslangan jadvaldan foydalanish.
**Yechim (SQL):**
```sql
-- Segment Tree tuzilmasini jadval ko'rinishida ifodalash
SELECT SUM(amount) 
FROM transactions 
WHERE transaction_date BETWEEN '2023-01-01' AND '2023-03-31'
-- Indeks yordamida qidiruvni tezlashtirish
CREATE INDEX idx_trans_date ON transactions(transaction_date);
```
**Tushuntirish:** SQLda Segment Tree mantiqiy indekslar orqali amalga oshiriladi. B-Tree indekslari `O(log n)` qidiruv tezligini ta'minlaydi.

### Topshiriq #1083: Fenwick Tree (Binary Indexed Tree)
**Tavsif:** Katta hajmdagi ma'lumotlar oqimida kümülatif yig'indilarni (prefix sums) yangilash.
**Talablar:** `Update` va `Query` operatsiyalari uchun samaradorlik.
**Yechim (SQL):**
```sql
-- Fenwick Tree uchun yordamchi jadval
UPDATE fenwick_tree 
SET val = val + :delta 
WHERE idx IN (SELECT id FROM bit_indices WHERE bit_mask = :mask);
```
**Tushuntirish:** Fenwick Tree bitli operatsiyalar yordamida yig'indilarni saqlaydi. SQLda bu `bit_mask` jadvali orqali samarali amalga oshiriladi.

### Topshiriq #1084: Trie (Prefix Tree) yordamida avtomatik to'ldirish
**Tavsif:** Foydalanuvchi qidiruv so'rovlarini tezkor bashorat qilish.
**Talablar:** Prefiks bo'yicha qidiruv, `LIKE` operatoridan tezroq ishlash.
**Yechim (SQL):**
```sql
-- Trie tuzilmasi: har bir tugun o'z ota-tuguniga bog'liq
SELECT word 
FROM trie_nodes 
WHERE path LIKE 'uzb%' -- Prefiks qidiruvi
ORDER BY frequency DESC LIMIT 10;
```
**Tushuntirish:** Trie tuzilmasi ma'lumotlar bazasida "path" (yo'l) ustuni orqali iyerarxik saqlanadi, bu esa qidiruvni keskin tezlashtiradi.

### Topshiriq #1085: Graflarda Topologik Saralash
**Tavsif:** Loyiha vazifalarining bajarilish ketma-ketligini (Dependency) aniqlash.
**Talablar:** Sikllarni aniqlash va vazifalarni tartiblash.
**Yechim (SQL):**
```sql
WITH RECURSIVE TaskOrder AS (
    SELECT id, task_name, 0 as level FROM tasks WHERE parent_id IS NULL
    UNION ALL
    SELECT t.id, t.task_name, to.level + 1
    FROM tasks t JOIN TaskOrder to ON t.parent_id = to.id
)
SELECT * FROM TaskOrder ORDER BY level;
```
**Tushuntirish:** Rekursiv CTE iyerarxik bog'liqliklarni (DAG - Directed Acyclic Graph) tartiblab beradi.

### Topshiriq #1086: Segment Tree: Range Maximum Query
**Tavsif:** Sensor ma'lumotlaridan eng yuqori qiymatni aniqlash.
**Talablar:** `MAX` funksiyasini indekslangan qatlamlar bilan birlashtirish.
**Yechim (SQL):**
```sql
-- Oldindan hisoblangan oraliqlar (Precomputed ranges)
SELECT MAX(val) 
FROM sensor_data_segments 
WHERE segment_id IN (1, 2, 3);
```
**Tushuntirish:** Segment Tree g'oyasiga ko'ra, ma'lumotlar oldindan kichik bo'laklarga bo'linib, har birining `MAX` qiymati saqlanadi.

### Topshiriq #1087: Fenwick Tree: Dinamik yangilanish
**Tavsif:** Real vaqt rejimida hisob balansini yangilash.
**Talablar:** `ACID` tranzaksiyalari bilan moslik.
**Yechim (SQL):**
```sql
BEGIN;
UPDATE bit_tree SET val = val + 500 WHERE idx = 10;
-- Fenwick tuzilmasi bo'yicha yuqori tugunlarni yangilash
UPDATE bit_tree SET val = val + 500 WHERE idx IN (12, 16, 32);
COMMIT;
```
**Tushuntirish:** Fenwick Tree'da bitta qiymat o'zgarganda, unga bog'liq bo'lgan barcha "ota" tugunlar yangilanishi kerak.

### Topshiriq #1088: Trie: So'zlarni o'chirish va optimallashtirish
**Tavsif:** Qidiruv indeksidan eskirgan so'rovlarni olib tashlash.
**Talablar:** Trie shoxlarini tozalash.
**Yechim (SQL):**
```sql
DELETE FROM trie_nodes 
WHERE path LIKE 'eski_soz%' 
AND NOT EXISTS (SELECT 1 FROM trie_nodes WHERE path LIKE 'eski_soz%/%');
```
**Tushuntirish:** Trie tuzilmasida barg tugunlarini o'chirish orqali xotira bo'shatiladi.

### Topshiriq #1089: Graflarda bog'liqlik tahlili (Transitive Closure)
**Tavsif:** Foydalanuvchilar o'rtasidagi "do'stlik" zanjirini aniqlash.
**Talablar:** 3-darajali bog'liqlikni topish.
**Yechim (SQL):**
```sql
SELECT DISTINCT f1.user_id, f3.friend_id
FROM friends f1
JOIN friends f2 ON f1.friend_id = f2.user_id
JOIN friends f3 ON f2.friend_id = f3.user_id;
```
**Tushuntirish:** Join operatsiyalari orqali graflardagi yo'llar kengaytiriladi, bu "do'stning do'sti" kabi munosabatlarni aniqlashda samarali.

### Topshiriq #1090: Segment Tree: Range Update
**Tavsif:** Narxlarni ommaviy yangilash (Range Update).
**Talablar:** `Lazy Propagation` texnikasini SQLda simulyatsiya qilish.
**Yechim (SQL):**
```sql
-- Lazy flag yordamida narxlarni yangilash
UPDATE products 
SET price = price * 1.1, lazy_update = 0 
WHERE category_id BETWEEN 100 AND 200;
```
**Tushuntirish:** `Lazy Propagation` yordamida har bir elementni alohida yangilash o'rniga, oraliq belgisi (flag) orqali ommaviy yangilash amalga oshiriladi.

---

### Topshiriq #1091: Graflarda Qisqa Yo'lni Topish (Dijkstra SQL implementatsiyasi)
**Tavsif:** Logistika tizimida shaharlararo eng arzon yo'nalishni aniqlash.
**Talablar:** `Recursive CTE` yordamida eng qisqa yo'lni topish, `O(V+E)` murakkablik.
**Yechim (SQL):**
```sql
WITH RECURSIVE Dijkstra AS (
    -- Boshlang'ich tugun
    SELECT target_node, cost FROM edges WHERE source_node = 1
    UNION ALL
    SELECT e.target_node, d.cost + e.cost
    FROM edges e
    JOIN Dijkstra d ON e.source_node = d.target_node
    WHERE d.cost + e.cost < 1000 -- Cheklov: maksimal xarajat
)
SELECT target_node, MIN(cost) as min_cost FROM Dijkstra GROUP BY target_node;
```
**Tushuntirish:** Rekursiv CTE orqali barcha mumkin bo'lgan yo'llar tekshiriladi va `MIN` funksiyasi bilan eng maqbul yo'l ajratib olinadi.

### Topshiriq #1092: Segment Tree yordamida Interval Sum Query
**Tavsif:** Moliya tizimida vaqt oralig'idagi tranzaksiyalar yig'indisini tezkor hisoblash.
**Talablar:** Indeksli jadvaldan foydalangan holda `O(log N)` tezlikda so'rov.
**Yechim (SQL):**
```sql
-- Segment Tree strukturasini simulyatsiya qilish
SELECT SUM(amount) 
FROM transactions 
WHERE transaction_date BETWEEN '2023-01-01' AND '2023-03-31'
-- Indeks: CREATE INDEX idx_date_amount ON transactions(transaction_date, amount);
```
**Tushuntirish:** B-Tree indekslari SQL'da Segment Tree vazifasini bajaradi, bu esa katta hajmli ma'lumotlarda qidiruvni logarifmik tezlikka olib chiqadi.

### Topshiriq #1093: Fenwick Tree (Binary Indexed Tree) yordamida Prefix Sum
**Tavsif:** Real vaqt rejimida kümülatif hisobotlarni yangilash.
**Talablar:** `Bitwise` operatsiyalar bilan indeksni boshqarish.
**Yechim (SQL):**
```sql
-- Fenwick Tree'ning SQL'dagi mantiqiy ko'rinishi
CREATE FUNCTION get_prefix_sum(idx INT) RETURNS INT AS $$
BEGIN
    -- Indeksni bitwise operatsiyalar bilan kamaytirish
    RETURN (SELECT SUM(val) FROM bit_table WHERE id <= idx);
END;
$$ LANGUAGE plpgsql;
```
**Tushuntirish:** Fenwick Tree ma'lumotlar o'zgarib turadigan holatlarda yig'indini hisoblash uchun eng samarali tuzilmadir.

### Topshiriq #1094: Trie (Prefix Tree) yordamida Avtomatik To'ldirish
**Tavsif:** Foydalanuvchi qidiruv so'rovlarini tezkor taklif qilish tizimi.
**Talablar:** `LIKE` operatoridan qochish, `Prefix` bo'yicha qidiruv.
**Yechim (SQL):**
```sql
-- Trie tugunlari jadvali
SELECT word FROM trie_nodes 
WHERE path_prefix = 'khor' 
ORDER BY frequency DESC LIMIT 10;
```
**Tushuntirish:** `LIKE '%text%'` o'rniga `path_prefix` ustunidan foydalanish indeksdan foydalanish imkonini beradi va qidiruvni 100x tezlashtiradi.

### Topshiriq #1095: Graflarda Topologik Saralash
**Tavsif:** Loyiha vazifalari (Task dependencies) ketma-ketligini aniqlash.
**Talablar:** `DAG` (Directed Acyclic Graph) tekshiruvi.
**Yechim (SQL):**
```sql
WITH RECURSIVE TaskOrder AS (
    SELECT task_id, 1 as level FROM tasks WHERE parent_id IS NULL
    UNION ALL
    SELECT t.task_id, to_o.level + 1
    FROM tasks t
    JOIN TaskOrder to_o ON t.parent_id = to_o.task_id
)
SELECT * FROM TaskOrder ORDER BY level;
```
**Tushuntirish:** Rekursiv CTE vazifalar o'rtasidagi bog'liqlikni ierarxik tartibda saralab beradi.

### Topshiriq #1096: Segment Tree: Range Maximum Query (RMQ)
**Tavsif:** Sensor ma'lumotlaridan eng yuqori qiymatni aniqlash.
**Talablar:** `Window Functions` yordamida optimallashtirish.
**Yechim (SQL):**
```sql
SELECT sensor_id, MAX(value) OVER (PARTITION BY sensor_id ORDER BY timestamp 
       ROWS BETWEEN 10 PRECEDING AND CURRENT ROW) as moving_max
FROM sensor_data;
```
**Tushuntirish:** `Window Functions` segment tree mantig'ini SQL darajasida abstraktlashtiradi, bu esa kodni qisqa va tezkor qiladi.

### Topshiriq #1097: Trie yordamida IP Manzillarni Qidirish
**Tavsif:** Tarmoq xavfsizligi uchun IP prefikslarini moslashtirish.
**Talablar:** Bit-maskalash va Trie qidiruvi.
**Yechim (SQL):**
```sql
SELECT network_id FROM ip_trie 
WHERE ip_address_bits LIKE '192.168.0.%'; -- Trie yo'li bo'yicha
```
**Tushuntirish:** IP manzillarni bitlar ketma-ketligi sifatida saqlash Trie tuzilmasida eng tezkor qidiruvni ta'minlaydi.

### Topshiriq #1098: Fenwick Tree: Update va Query
**Tavsif:** Inventarizatsiya tizimida zaxiralarni dinamik yangilash.
**Talablar:** `Atomic` operatsiyalar bilan ma'lumotlar yaxlitligini saqlash.
**Yechim (SQL):**
```sql
UPDATE fenwick_tree SET val = val + 5 WHERE id IN (1, 2, 4, 8); -- Indeks yangilanishi
```
**Tushuntirish:** Fenwick Tree'da bitta elementni yangilash uchun faqat `log N` ta tugunni yangilash kifoya qiladi.

### Topshiriq #1099: Graflarda Birlashgan Komponentlarni Topish
**Tavsif:** Ijtimoiy tarmoqlarda "Do'stlar doirasi"ni aniqlash.
**Talablar:** `Disjoint Set Union (DSU)` mantig'i.
**Yechim (SQL):**
```sql
WITH RECURSIVE Friends AS (
    SELECT user_id, friend_id FROM connections
    UNION
    SELECT f.user_id, c.friend_id
    FROM Friends f JOIN connections c ON f.friend_id = c.user_id
)
SELECT user_id, COUNT(DISTINCT friend_id) FROM Friends GROUP BY user_id;
```
**Tushuntirish:** Rekursiya orqali barcha bilvosita aloqador foydalanuvchilar bitta komponentga birlashtiriladi.

### Topshiriq #1100: Trie yordamida Katta hajmli Lug'atni Saralash
**Tavsif:** Milliy til korpusi uchun so'zlarni tezkor qidirish.
**Talablar:** Xotira samaradorligi va `Index-Only Scan`.
**Yechim (SQL):**
```sql
-- Trie strukturasini indekslash
CREATE INDEX idx_trie_path ON dictionary_trie (path_vector);
SELECT word FROM dictionary_trie WHERE path_vector @> ARRAY[1, 5, 2];
```
**Tushuntirish:** `PostgreSQL`'ning `GIN` indekslari va `Array` turlari Trie tuzilmasini SQL'da mukammal implementatsiya qilish imkonini beradi.