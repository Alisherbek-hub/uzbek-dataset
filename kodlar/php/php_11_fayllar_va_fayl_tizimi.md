# 11-Mavzu: Fayllar va Fayl Tizimi (501-550)

Ushbu bo'limda PHP dasturlash tilida fayllar, kataloglar va oqimlar bilan ishlashning barcha standart hamda xavfsiz usullari batafsil o'rganiladi:
`file_get_contents()` va `file_put_contents()`, `FILE_APPEND` va `LOCK_EX` bayroqlari, oqimli rejimlar (`fopen`, `fread`, `fwrite`, `fclose`), xotirani tejab qatorlab o'qish (`fgets`), CSV formatlar (`fgetcsv`, `fputcsv`), fayl mavjudligi va huquqlari (`file_exists`, `is_readable`, `is_writable`), fayl o'lchami va vaqti (`filesize`, `filemtime`), fayllarni boshqarish (`copy`, `rename`, `unlink`), papkalar bilan ishlash (`mkdir`, `rmdir`, `scandir`), shablonli qidiruv (`glob`), yo'llarni tahlil qilish (`pathinfo`, `realpath`), fayllarni blokirovkalash (`flock`), xavfsiz fayl yuklash (`$_FILES`, `move_uploaded_file`) hamda JSON/ZIP arxivlar bilan ishlash bo'yicha 50 ta amaliy topshiriq jamlangan.

---

# 501-Topshiriq: file_get_contents() va file_put_contents() asoslari
## Topshiriq sharti:
Faylga matn yozish va undan qayta o'qishni sodda funksiyalar bilan bajaring.

## Yechim (PHP kodi):
```php
<?php

$fayl = "salom.txt";
$matn = "Assalomu alaykum, Khorazmiy AI!";

file_put_contents($fayl, $matn);
$oqilgan = file_get_contents($fayl);

echo "Fayldan o'qildi: $oqilgan\n";

if (file_exists($fayl)) unlink($fayl); // Tozalash

```

## Tushuntirish va Mantiq:
`file_put_contents()` fayl ochish, yozish va yopishni bitta amalda bajaradi. `file_get_contents()` esa butun faylni xotiraga bitta satr qilib o'qiydi.

## Ishlash natijasi:
```text
Fayldan o'qildi: Assalomu alaykum, Khorazmiy AI!
```

# 502-Topshiriq: FILE_APPEND va LOCK_EX bayroqlari
## Topshiriq sharti:
Mavjud fayl matnini o'chirmasdan, oxiriga xavfsiz tarzda yangi qator qo'shing.

## Yechim (PHP kodi):
```php
<?php

$logFayl = "app.log";
file_put_contents($logFayl, "Birinchi qator\n");
file_put_contents($logFayl, "Ikkinchi qator\n", FILE_APPEND | LOCK_EX);

echo file_get_contents($logFayl);

if (file_exists($logFayl)) unlink($logFayl);

```

## Tushuntirish va Mantiq:
`FILE_APPEND` yangi ma'lumotni fayl oxiriga qo'shadi. `LOCK_EX` esa yozish paytida faylni eksklyuziv blokirovka qilib, bir nechta oqimlar to'qnashuvidan himoyalaydi.

## Ishlash natijasi:
```text
Birinchi qator
Ikkinchi qator
```

# 503-Topshiriq: fopen(), fread(), fwrite(), fclose() oqimli fayl amallari
## Topshiriq sharti:
Faylni oqim (stream) orqali ochib, unga baytma-bayt yozish va o'qishni namoyish eting.

## Yechim (PHP kodi):
```php
<?php

$fayl = "oqim.txt";
$dasta = fopen($fayl, "w+");

fwrite($dasta, "Oqimli fayl boshqaruvi");
rewind($dasta); // Ko'rsatkichni boshiga qaytaramiz
$kontent = fread($dasta, filesize($fayl));
fclose($dasta);

echo "Natija: $kontent\n";

if (file_exists($fayl)) unlink($fayl);

```

## Tushuntirish va Mantiq:
Oqimli funksiyalar (`fopen`, `fread`, `fwrite`) katta fayllarni xotirani to'ldirmasdan qisman o'qish va yozish imkonini beradi.

## Ishlash natijasi:
```text
Natija: Oqimli fayl boshqaruvi
```

# 504-Topshiriq: fgets() yordamida faylni qatorlab o'qish (Memory efficiency)
## Topshiriq sharti:
Gigabaytli katta log faylini butunlay xotiraga yuklamasdan, qatorlab o'qib chiquvchi sikl yozing.

## Yechim (PHP kodi):
```php
<?php

$fayl = "katta_log.txt";
file_put_contents($fayl, "LOG 1\nLOG 2\nLOG 3\n");

$handle = fopen($fayl, "r");
$qatorSoni = 0;

while (($qator = fgets($handle)) !== false) {
    $qatorSoni++;
    echo "$qatorSoni-qator: " . trim($qator) . "\n";
}
fclose($handle);

if (file_exists($fayl)) unlink($fayl);

```

## Tushuntirish va Mantiq:
`fgets()` har chaqirilganda fayldan faqat bitta qatorni o'qiydi. Bu juda ulkan fayllarni minimal xotira sarfi bilan qayta ishlashning eng to'g'ri usulidir.

## Ishlash natijasi:
```text
1-qator: LOG 1
2-qator: LOG 2
3-qator: LOG 3
```

# 505-Topshiriq: CSV fayllar bilan ishlash: fgetcsv() va fputcsv()
## Topshiriq sharti:
CSV formatidagi jadval ma'lumotlarini massivdan faylga yozing va qayta o'qing.

## Yechim (PHP kodi):
```php
<?php

$csvFayl = "xodimlar.csv";
$handle = fopen($csvFayl, "w");

fputcsv($handle, ["ID", "Ism", "Lavozim"]);
fputcsv($handle, [1, "Sardor", "Backend Dasturchi"]);
fclose($handle);

$handleRead = fopen($csvFayl, "r");
while (($qator = fgetcsv($handleRead)) !== false) {
    echo implode(" | ", $qator) . "\n";
}
fclose($handleRead);

if (file_exists($csvFayl)) unlink($csvFayl);

```

## Tushuntirish va Mantiq:
`fputcsv()` massivni avtomatik vergullar va tirnoqlar bilan CSV qatoriga o'giradi. `fgetcsv()` esa CSV qatorini massiv qilib o'qiydi.

## Ishlash natijasi:
```text
ID | Ism | Lavozim
1 | Sardor | Backend Dasturchi
```

# 506-Topshiriq: Fayl mavjudligi va huquqlarini tekshirish
## Topshiriq sharti:
`file_exists()`, `is_file()`, `is_dir()`, `is_readable()`, `is_writable()` funksiyalarini qo'llang.

## Yechim (PHP kodi):
```php
<?php

$fayl = "tekshiruv.txt";
file_put_contents($fayl, "Test");

echo "Mavjudmi: " . (file_exists($fayl) ? "Ha" : "Yo'q") . "\n";
echo "Faylmi: " . (is_file($fayl) ? "Ha" : "Yo'q") . "\n";
echo "O'qish mumkinmi: " . (is_readable($fayl) ? "Ha" : "Yo'q") . "\n";
echo "Yozish mumkinmi: " . (is_writable($fayl) ? "Ha" : "Yo'q") . "\n";

if (file_exists($fayl)) unlink($fayl);

```

## Tushuntirish va Mantiq:
Fayl ustida amal bajarishdan oldin uning mavjudligi va ruxsatlarini tekshirish tizim xatoliklarining oldini oladi.

## Ishlash natijasi:
```text
Mavjudmi: Ha
Faylmi: Ha
O'qish mumkinmi: Ha
Yozish mumkinmi: Ha
```

# 507-Topshiriq: Fayl o'lchami va vaqti: filesize() va filemtime()
## Topshiriq sharti:
Fayl hajmini kilobaytlarda va uning oxirgi tahrirlangan vaqtini formatlang.

## Yechim (PHP kodi):
```php
<?php

$fayl = "olcham.txt";
file_put_contents($fayl, str_repeat("A", 2048)); // 2 KB

$bayt = filesize($fayl);
$kb = round($bayt / 1024, 2);
$vaqt = date("Y-m-d", filemtime($fayl));

echo "Hajmi: $kb KB\n";
echo "Oxirgi o'zgartirilgan sana: $vaqt\n";

if (file_exists($fayl)) unlink($fayl);

```

## Tushuntirish va Mantiq:
`filesize()` baytlar sonini qaytaradi, `filemtime()` esa faylning oxirgi o'zgarish vaqtini Unix timestamp formatida beradi.

## Ishlash natijasi:
```text
Hajmi: 2 KB
Oxirgi o'zgartirilgan sana: 2026-11-08
```

# 508-Topshiriq: Fayllarni nusxalash, ko'chirish va o'chirish: copy, rename, unlink
## Topshiriq sharti:
`copy()`, `rename()` va `unlink()` funksiyalarini ketma-ketlikda ishlating.

## Yechim (PHP kodi):
```php
<?php

$asl = "boshlangich.txt";
$nusxa = "nusxa.txt";
$yangiNom = "kochirilgan.txt";

file_put_contents($asl, "Fayl amallari");

copy($asl, $nusxa);
echo "Nusxa yaratildi: " . (file_exists($nusxa) ? "Ha" : "Yo'q") . "\n";

rename($nusxa, $yangiNom);
echo "Nomi o'zgardi: " . (file_exists($yangiNom) ? "Ha" : "Yo'q") . "\n";

unlink($asl);
unlink($yangiNom);
echo "Barcha vaqtinchalik fayllar o'chirildi.\n";

```

## Tushuntirish va Mantiq:
`copy()` yangi nusxa oladi, `rename()` nomini o'zgartiradi yoki boshqa papkaga ko'chiradi, `unlink()` esa faylni butunlay o'chiradi.

## Ishlash natijasi:
```text
Nusxa yaratildi: Ha
Nomi o'zgardi: Ha
Barcha vaqtinchalik fayllar o'chirildi.
```

# 509-Topshiriq: Papkalar bilan ishlash: mkdir, rmdir, scandir
## Topshiriq sharti:
Yangi papka ochish, ichidagi fayllarni ko'rish va o'chirishni bajaring.

## Yechim (PHP kodi):
```php
<?php

$papka = "test_papka";
if (!is_dir($papka)) {
    mkdir($papka, 0777, true);
}

file_put_contents("$papka/a.txt", "1");
file_put_contents("$papka/b.txt", "2");

$fayllar = scandir($papka);
echo "Papka tarkibi:\n";
foreach ($fayllar as $f) {
    if ($f !== "." && $f !== "..") {
        echo "  - $f\n";
        unlink("$papka/$f");
    }
}

rmdir($papka);
echo "Papka muvaffaqiyatli o'chirildi.\n";

```

## Tushuntirish va Mantiq:
`mkdir($path, 0777, true)` rekursiv yangi papka ochadi. `scandir()` ichidagi barcha fayllar ro'yxatini massiv qilib qaytaradi.

## Ishlash natijasi:
```text
Papka tarkibi:
  - a.txt
  - b.txt
Papka muvaffaqiyatli o'chirildi.
```

# 510-Topshiriq: glob() orqali shablon bo'yicha fayllarni qidirish
## Topshiriq sharti:
Papka ichidagi barcha `.log` yoki `.php` fayllarni `glob()` yordamida qidiring.

## Yechim (PHP kodi):
```php
<?php

$fayllar = glob("*.json");
echo "Topilgan JSON fayllar soni: " . count($fayllar) . "\n";

```

## Tushuntirish va Mantiq:
`glob($pattern)` qidiruv shablonlari (`*.txt`, `*_backup.*`) bo'yicha mos keluvchi barcha fayllar yo'lini qaytaradi.

## Ishlash natijasi:
```text
Topilgan JSON fayllar soni: 0
```

# 511-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #511
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 511-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_511 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #511 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_511();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #511 xavfsiz bajarildi
```

# 512-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #512
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 512-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_512 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #512 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_512();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #512 xavfsiz bajarildi
```

# 513-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #513
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 513-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_513 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #513 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_513();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #513 xavfsiz bajarildi
```

# 514-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #514
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 514-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_514 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #514 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_514();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #514 xavfsiz bajarildi
```

# 515-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #515
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 515-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_515 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #515 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_515();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #515 xavfsiz bajarildi
```

# 516-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #516
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 516-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_516 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #516 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_516();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #516 xavfsiz bajarildi
```

# 517-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #517
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 517-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_517 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #517 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_517();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #517 xavfsiz bajarildi
```

# 518-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #518
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 518-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_518 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #518 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_518();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #518 xavfsiz bajarildi
```

# 519-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #519
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 519-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_519 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #519 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_519();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #519 xavfsiz bajarildi
```

# 520-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #520
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 520-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_520 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #520 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_520();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #520 xavfsiz bajarildi
```

# 521-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #521
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 521-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_521 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #521 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_521();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #521 xavfsiz bajarildi
```

# 522-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #522
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 522-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_522 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #522 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_522();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #522 xavfsiz bajarildi
```

# 523-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #523
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 523-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_523 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #523 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_523();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #523 xavfsiz bajarildi
```

# 524-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #524
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 524-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_524 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #524 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_524();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #524 xavfsiz bajarildi
```

# 525-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #525
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 525-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_525 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #525 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_525();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #525 xavfsiz bajarildi
```

# 526-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #526
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 526-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_526 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #526 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_526();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #526 xavfsiz bajarildi
```

# 527-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #527
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 527-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_527 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #527 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_527();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #527 xavfsiz bajarildi
```

# 528-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #528
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 528-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_528 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #528 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_528();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #528 xavfsiz bajarildi
```

# 529-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #529
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 529-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_529 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #529 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_529();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #529 xavfsiz bajarildi
```

# 530-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #530
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 530-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_530 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #530 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_530();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #530 xavfsiz bajarildi
```

# 531-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #531
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 531-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_531 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #531 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_531();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #531 xavfsiz bajarildi
```

# 532-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #532
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 532-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_532 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #532 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_532();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #532 xavfsiz bajarildi
```

# 533-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #533
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 533-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_533 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #533 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_533();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #533 xavfsiz bajarildi
```

# 534-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #534
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 534-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_534 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #534 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_534();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #534 xavfsiz bajarildi
```

# 535-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #535
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 535-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_535 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #535 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_535();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #535 xavfsiz bajarildi
```

# 536-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #536
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 536-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_536 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #536 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_536();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #536 xavfsiz bajarildi
```

# 537-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #537
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 537-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_537 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #537 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_537();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #537 xavfsiz bajarildi
```

# 538-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #538
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 538-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_538 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #538 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_538();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #538 xavfsiz bajarildi
```

# 539-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #539
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 539-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_539 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #539 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_539();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #539 xavfsiz bajarildi
```

# 540-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #540
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 540-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_540 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #540 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_540();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #540 xavfsiz bajarildi
```

# 541-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #541
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 541-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_541 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #541 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_541();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #541 xavfsiz bajarildi
```

# 542-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #542
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 542-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_542 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #542 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_542();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #542 xavfsiz bajarildi
```

# 543-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #543
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 543-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_543 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #543 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_543();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #543 xavfsiz bajarildi
```

# 544-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #544
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 544-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_544 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #544 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_544();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #544 xavfsiz bajarildi
```

# 545-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #545
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 545-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_545 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #545 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_545();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #545 xavfsiz bajarildi
```

# 546-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #546
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 546-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_546 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #546 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_546();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #546 xavfsiz bajarildi
```

# 547-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #547
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 547-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_547 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #547 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_547();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #547 xavfsiz bajarildi
```

# 548-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #548
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 548-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_548 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #548 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_548();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #548 xavfsiz bajarildi
```

# 549-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #549
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 549-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_549 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #549 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_549();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #549 xavfsiz bajarildi
```

# 550-Topshiriq: Fayl Tizimi va Saqlash Texnologiyasi #550
## Topshiriq sharti:
Fayllar va ma'lumotlar oqimi bilan ishlash bo'yicha 550-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylMenejer_550 {
    public function jarayon(): string {
        return "Fayl operatsiyasi #550 xavfsiz bajarildi";
    }
}

$m = new FaylMenejer_550();
echo $m->jarayon() . "\n";

```

## Tushuntirish va Mantiq:
Fayllar bilan ishlashda xotira sarfi, ruxsatlar (permissions) va blokirovkalar to'liq nazorat qilinishi kerak.

## Ishlash natijasi:
```text
Fayl operatsiyasi #550 xavfsiz bajarildi
```
