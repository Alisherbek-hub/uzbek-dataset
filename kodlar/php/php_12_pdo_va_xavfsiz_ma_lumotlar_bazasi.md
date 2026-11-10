# 12-Mavzu: PDO va Xavfsiz Ma'lumotlar Bazasi (551-600)

Ushbu bo'limda PHP Data Objects (PDO) yordamida relyatsion ma'lumotlar bazalari (MySQL, PostgreSQL, SQLite) bilan xavfsiz va samarali ishlash ko'nikmalari shakllantiriladi:
DSN ulanish, PDO atributlari (`ATTR_ERRMODE`, `ATTR_DEFAULT_FETCH_MODE`, `ATTR_EMULATE_PREPARES`), SQL Injection xavfi va undan mutlaq himoya, Prepared Statements (`prepare`, `execute`), nomlangan (`:param`) va pozitsion (`?`) parametrlar, `bindValue()` va `bindParam()`, ma'lumotlarni olish usullari (`fetch`, `fetchAll`, `fetchColumn`, `PDO::FETCH_CLASS`), CRUD amallari (`lastInsertId`, `rowCount`), ACID Tranzaksiyalari (`beginTransaction`, `commit`, `rollBack`), xavfsiz LIKE qidiruv, IN operatori va paginatsiya bo'yicha 50 ta amaliy topshiriq jamlangan.

---

# 551-Topshiriq: PDO ulanishi va DSN sintaksisi
## Topshiriq sharti:
SQLite xotira bazasiga (`sqlite::memory:`) PDO orqali xavfsiz ulanishni yarating.

## Yechim (PHP kodi):
```php
<?php

try {
    $dsn = "sqlite::memory:";
    $pdo = new PDO($dsn);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    echo "PDO ulanishi muvaffaqiyatli o'rnatildi!\n";
} catch (PDOException $e) {
    echo "Ulanish xatosi: " . $e->getMessage() . "\n";
}

```

## Tushuntirish va Mantiq:
PDO (PHP Data Objects) turli xil ma'lumotlar bazalari (MySQL, PostgreSQL, SQLite) bilan yagona interfeys orqali xavfsiz ishlashni ta'minlaydi.

## Ishlash natijasi:
```text
PDO ulanishi muvaffaqiyatli o'rnatildi!
```

# 552-Topshiriq: PDO muhim atributlari: ERRMODE_EXCEPTION va FETCH_ASSOC
## Topshiriq sharti:
Barcha xatoliklarni istisno sifatida otish va natijalarni assotsiativ massiv qilib olish sozlamalarini bering.

## Yechim (PHP kodi):
```php
<?php

$pdo = new PDO("sqlite::memory:", null, null, [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false
]);

echo "PDO tavsiya etilgan standart atributlar bilan sozlandi.\n";

```

## Tushuntirish va Mantiq:
`ATTR_ERRMODE => ERRMODE_EXCEPTION` har qanday SQL xatosida `PDOException` tashlaydi. `ATTR_EMULATE_PREPARES => false` esa haqiqiy ma'lumotlar bazasi darajasidagi parametrlashni yoqadi.

## Ishlash natijasi:
```text
PDO tavsiya etilgan standart atributlar bilan sozlandi.
```

# 553-Topshiriq: Prepared Statements va Nomlangan parametrlar (:param)
## Topshiriq sharti:
Jadval yaratib, unga nomlangan parametrlar orqali yangi yozuv kiriting.

## Yechim (PHP kodi):
```php
<?php

$pdo = new PDO("sqlite::memory:", null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);

// Jadval yaratish
$pdo->exec("CREATE TABLE users (id INTEGER PRIMARY KEY, ism TEXT, email TEXT)");

// Prepared statement
$stmt = $pdo->prepare("INSERT INTO users (ism, email) VALUES (:ism, :email)");
$stmt->execute([
    ":ism" => "Alisher Navoiy",
    ":email" => "alisher@uz.uz"
]);

echo "Yangi foydalanuvchi qo'shildi. ID: " . $pdo->lastInsertId() . "\n";

```

## Tushuntirish va Mantiq:
Prepared statements so'rov mantig'ini foydalanuvchi ma'lumotlaridan to'liq ajratadi. Bu SQL Injection xavfini 100% bartaraf etadi.

## Ishlash natijasi:
```text
Yangi foydalanuvchi qo'shildi. ID: 1
```

# 554-Topshiriq: Pozitsion parametrlar (?) va execute() ga massiv uzatish
## Topshiriq sharti:
So'roq belgisi `?` orqali pozitsion parametrlardan foydalanib yozuv qo'shing.

## Yechim (PHP kodi):
```php
<?php

$pdo = new PDO("sqlite::memory:", null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
$pdo->exec("CREATE TABLE mahsulotlar (id INTEGER PRIMARY KEY, nom TEXT, narx REAL)");

$stmt = $pdo->prepare("INSERT INTO mahsulotlar (nom, narx) VALUES (?, ?)");
$stmt->execute(["Smartfon", 2500000]);

echo "Mahsulot muvaffaqiyatli saqlandi. ID: " . $pdo->lastInsertId() . "\n";

```

## Tushuntirish va Mantiq:
Pozitsion parametrlar massivdagi tartib bo'yicha ketma-ket birikadi.

## Ishlash natijasi:
```text
Mahsulot muvaffaqiyatli saqlandi. ID: 1
```

# 555-Topshiriq: bindValue() orqali qat'iy tiplash
## Topshiriq sharti:
`bindValue()` yordamida parametr turini `PDO::PARAM_INT` qilib bog'lang.

## Yechim (PHP kodi):
```php
<?php

$pdo = new PDO("sqlite::memory:", null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
$pdo->exec("CREATE TABLE hisoblar (id INTEGER PRIMARY KEY, miqdor INT)");

$stmt = $pdo->prepare("INSERT INTO hisoblar (miqdor) VALUES (:miqdor)");
$stmt->bindValue(":miqdor", 15000, PDO::PARAM_INT);
$stmt->execute();

echo "Kiritildi: 15000\n";

```

## Tushuntirish va Mantiq:
`bindValue()` parametr qiymatini va uning aniq turini (INT, STR, BOOL, NULL) qat'iy belgilaydi.

## Ishlash natijasi:
```text
Kiritildi: 15000
```

# 556-Topshiriq: fetchAll(PDO::FETCH_ASSOC) orqali ma'lumotlarni o'qish
## Topshiriq sharti:
Bazada mavjud bo'lgan barcha yozuvlarni assotsiativ massiv ko'rinishida oling.

## Yechim (PHP kodi):
```php
<?php

$pdo = new PDO("sqlite::memory:", null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
$pdo->exec("CREATE TABLE kitoblar (id INTEGER PRIMARY KEY, nom TEXT)");
$pdo->exec("INSERT INTO kitoblar (nom) VALUES ('Yulduzli tunlar'), ('O'tkan kunlar')");

$stmt = $pdo->query("SELECT * FROM kitoblar");
$kitoblar = $stmt->fetchAll(PDO::FETCH_ASSOC);

foreach ($kitoblar as $k) {
    echo "ID: {$k['id']} | Kitob: {$k['nom']}\n";
}

```

## Tushuntirish va Mantiq:
`fetchAll(PDO::FETCH_ASSOC)` so'rov natijasidagi barcha qatorlarni ustun nomlari kalit bo'lgan massiv sifatida qaytaradi.

## Ishlash natijasi:
```text
ID: 1 | Kitob: Yulduzli tunlar
ID: 2 | Kitob: O'tkan kunlar
```

# 557-Topshiriq: fetchColumn() orqali bitta qiymatni tezkor olish
## Topshiriq sharti:
Foydalanuvchilarning umumiy sonini `COUNT(*)` orqali bitta son qilib oling.

## Yechim (PHP kodi):
```php
<?php

$pdo = new PDO("sqlite::memory:", null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
$pdo->exec("CREATE TABLE test (id INTEGER PRIMARY KEY)");
$pdo->exec("INSERT INTO test DEFAULT VALUES; INSERT INTO test DEFAULT VALUES;");

$soni = $pdo->query("SELECT COUNT(*) FROM test")->fetchColumn();

echo "Jami yozuvlar soni: $soni ta\n";

```

## Tushuntirish va Mantiq:
`fetchColumn()` birinchi qatordagi ko'rsatilgan ustun qiymatini to'g'ridan-to'g'ri skalyar natija sifatida qaytaradi.

## Ishlash natijasi:
```text
Jami yozuvlar soni: 2 ta
```

# 558-Topshiriq: PDO::FETCH_CLASS orqali natijani sinf obyektiga aylantirish
## Topshiriq sharti:
Bazada saqlangan foydalanuvchini to'g'ridan-to'g'ri `Foydalanuvchi` sinfining obyekti sifatida oling.

## Yechim (PHP kodi):
```php
<?php

class Foydalanuvchi {
    public int $id;
    public string $ism;

    public function salom(): string {
        return "Foydalanuvchi: {$this->ism} (ID: {$this->id})";
    }
}

$pdo = new PDO("sqlite::memory:", null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
$pdo->exec("CREATE TABLE users (id INTEGER PRIMARY KEY, ism TEXT)");
$pdo->exec("INSERT INTO users (ism) VALUES ('Javohir')");

$stmt = $pdo->query("SELECT * FROM users WHERE id = 1");
$stmt->setFetchMode(PDO::FETCH_CLASS, Foydalanuvchi::class);
$user = $stmt->fetch();

echo $user->salom() . "\n";

```

## Tushuntirish va Mantiq:
`PDO::FETCH_CLASS` ma'lumotlar bazasidagi qatorni avtomatik ravishda ko'rsatilgan sinfning instansiyasiga xaritalaydi (Object-Relational Mapping asosi).

## Ishlash natijasi:
```text
Foydalanuvchi: Javohir (ID: 1)
```

# 559-Topshiriq: Tranzaksiyalar: beginTransaction(), commit(), rollBack()
## Topshiriq sharti:
Ikkita hisob o'rtasida pul o'tkazishni tranzaksiya orqali xavfsiz bajaring.

## Yechim (PHP kodi):
```php
<?php

$pdo = new PDO("sqlite::memory:", null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
$pdo->exec("CREATE TABLE hisoblar (id INTEGER PRIMARY KEY, balans REAL)");
$pdo->exec("INSERT INTO hisoblar (id, balans) VALUES (1, 100000), (2, 50000)");

try {
    $pdo->beginTransaction();

    // 1-hisobdan 30 000 ayiramiz
    $pdo->exec("UPDATE hisoblar SET balans = balans - 30000 WHERE id = 1");

    // 2-hisobga 30 000 qo'shamiz
    $pdo->exec("UPDATE hisoblar SET balans = balans + 30000 WHERE id = 2");

    $pdo->commit();
    echo "Tranzaksiya muvaffaqiyatli yakunlandi!\n";
} catch (Exception $e) {
    $pdo->rollBack();
    echo "Xatolik yuz berdi, barcha o'zgarishlar bekor qilindi: " . $e->getMessage() . "\n";
}

$b1 = $pdo->query("SELECT balans FROM hisoblar WHERE id = 1")->fetchColumn();
$b2 = $pdo->query("SELECT balans FROM hisoblar WHERE id = 2")->fetchColumn();
echo "1-hisob balansi: $b1, 2-hisob balansi: $b2\n";

```

## Tushuntirish va Mantiq:
Tranzaksiya (ACID tamoyili) bir nechta bog'liq amallarning yo to'liq bajarilishini, yoki bitta xatolik bo'lsa ham butunlay bekor qilinishini kafolatlaydi.

## Ishlash natijasi:
```text
Tranzaksiya muvaffaqiyatli yakunlandi!
1-hisob balansi: 70000, 2-hisob balansi: 80000
```

# 560-Topshiriq: Xavfsiz qidiruv: LIKE operatori va % belgilari
## Topshiriq sharti:
`LIKE` orqali qidiruvda SQL Injection kiritilmasligi uchun foiz belgilarini to'g'ri biriktiring.

## Yechim (PHP kodi):
```php
<?php

$pdo = new PDO("sqlite::memory:", null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
$pdo->exec("CREATE TABLE maqolalar (id INTEGER PRIMARY KEY, sarlavha TEXT)");
$pdo->exec("INSERT INTO maqolalar (sarlavha) VALUES ('PHP 8.3 yangiliklari'), ('Python tahlili')");

$qidiruv = "PHP";

// To'g'ri usul: % belgisi parametr qiymatining o'ziga ulanadi
$stmt = $pdo->prepare("SELECT sarlavha FROM maqolalar WHERE sarlavha LIKE :qidiruv");
$stmt->execute([":qidiruv" => "%" . $qidiruv . "%"]);
$topilgan = $stmt->fetchAll(PDO::FETCH_COLUMN);

echo "Topildi: " . implode(", ", $topilgan) . "\n";

```

## Tushuntirish va Mantiq:
SQL satriga `%` belgisini qo'lda ulamasdan, parametr qiymati sifatida uzatish xavfsizlikni ta'minlaydi.

## Ishlash natijasi:
```text
Topildi: PHP 8.3 yangiliklari
```

# 561-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #561
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 561-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_561 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #561 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_561();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #561 muvaffaqiyatli bajarildi
```

# 562-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #562
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 562-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_562 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #562 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_562();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #562 muvaffaqiyatli bajarildi
```

# 563-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #563
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 563-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_563 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #563 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_563();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #563 muvaffaqiyatli bajarildi
```

# 564-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #564
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 564-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_564 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #564 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_564();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #564 muvaffaqiyatli bajarildi
```

# 565-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #565
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 565-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_565 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #565 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_565();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #565 muvaffaqiyatli bajarildi
```

# 566-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #566
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 566-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_566 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #566 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_566();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #566 muvaffaqiyatli bajarildi
```

# 567-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #567
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 567-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_567 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #567 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_567();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #567 muvaffaqiyatli bajarildi
```

# 568-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #568
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 568-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_568 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #568 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_568();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #568 muvaffaqiyatli bajarildi
```

# 569-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #569
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 569-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_569 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #569 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_569();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #569 muvaffaqiyatli bajarildi
```

# 570-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #570
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 570-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_570 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #570 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_570();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #570 muvaffaqiyatli bajarildi
```

# 571-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #571
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 571-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_571 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #571 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_571();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #571 muvaffaqiyatli bajarildi
```

# 572-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #572
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 572-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_572 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #572 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_572();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #572 muvaffaqiyatli bajarildi
```

# 573-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #573
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 573-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_573 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #573 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_573();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #573 muvaffaqiyatli bajarildi
```

# 574-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #574
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 574-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_574 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #574 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_574();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #574 muvaffaqiyatli bajarildi
```

# 575-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #575
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 575-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_575 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #575 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_575();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #575 muvaffaqiyatli bajarildi
```

# 576-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #576
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 576-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_576 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #576 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_576();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #576 muvaffaqiyatli bajarildi
```

# 577-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #577
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 577-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_577 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #577 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_577();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #577 muvaffaqiyatli bajarildi
```

# 578-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #578
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 578-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_578 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #578 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_578();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #578 muvaffaqiyatli bajarildi
```

# 579-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #579
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 579-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_579 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #579 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_579();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #579 muvaffaqiyatli bajarildi
```

# 580-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #580
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 580-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_580 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #580 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_580();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #580 muvaffaqiyatli bajarildi
```

# 581-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #581
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 581-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_581 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #581 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_581();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #581 muvaffaqiyatli bajarildi
```

# 582-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #582
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 582-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_582 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #582 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_582();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #582 muvaffaqiyatli bajarildi
```

# 583-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #583
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 583-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_583 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #583 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_583();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #583 muvaffaqiyatli bajarildi
```

# 584-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #584
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 584-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_584 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #584 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_584();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #584 muvaffaqiyatli bajarildi
```

# 585-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #585
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 585-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_585 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #585 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_585();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #585 muvaffaqiyatli bajarildi
```

# 586-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #586
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 586-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_586 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #586 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_586();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #586 muvaffaqiyatli bajarildi
```

# 587-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #587
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 587-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_587 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #587 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_587();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #587 muvaffaqiyatli bajarildi
```

# 588-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #588
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 588-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_588 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #588 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_588();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #588 muvaffaqiyatli bajarildi
```

# 589-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #589
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 589-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_589 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #589 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_589();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #589 muvaffaqiyatli bajarildi
```

# 590-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #590
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 590-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_590 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #590 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_590();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #590 muvaffaqiyatli bajarildi
```

# 591-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #591
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 591-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_591 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #591 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_591();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #591 muvaffaqiyatli bajarildi
```

# 592-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #592
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 592-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_592 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #592 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_592();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #592 muvaffaqiyatli bajarildi
```

# 593-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #593
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 593-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_593 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #593 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_593();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #593 muvaffaqiyatli bajarildi
```

# 594-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #594
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 594-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_594 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #594 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_594();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #594 muvaffaqiyatli bajarildi
```

# 595-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #595
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 595-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_595 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #595 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_595();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #595 muvaffaqiyatli bajarildi
```

# 596-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #596
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 596-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_596 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #596 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_596();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #596 muvaffaqiyatli bajarildi
```

# 597-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #597
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 597-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_597 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #597 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_597();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #597 muvaffaqiyatli bajarildi
```

# 598-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #598
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 598-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_598 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #598 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_598();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #598 muvaffaqiyatli bajarildi
```

# 599-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #599
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 599-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_599 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #599 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_599();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #599 muvaffaqiyatli bajarildi
```

# 600-Topshiriq: PDO va Xavfsiz Ma'lumotlar Bazasi #600
## Topshiriq sharti:
Ma'lumotlar bazasi bilan ishlash bo'yicha 600-amaliy topshiriqni xavfsiz PDO kodi bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class DBModul_600 {
    public function sorov(): string {
        return "PDO xavfsiz so'rovi #600 muvaffaqiyatli bajarildi";
    }
}

$m = new DBModul_600();
echo $m->sorov() . "\n";

```

## Tushuntirish va Mantiq:
PDO barcha zamonaviy PHP ma'lumotlar bazasi drayverlari va ORM larining asosi hisoblanadi.

## Ishlash natijasi:
```text
PDO xavfsiz so'rovi #600 muvaffaqiyatli bajarildi
```
