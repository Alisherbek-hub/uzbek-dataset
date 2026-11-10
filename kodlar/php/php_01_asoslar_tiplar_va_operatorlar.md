# 1-Mavzu: PHP Asoslari, Ma'lumot Turlari va Operatorlar (1-50)

Ushbu bo'limda zamonaviy PHP 8.3 standartlari asosida dasturlashning fundamental poydevori batafsil yoritiladi:
PHP teglari (`<?php`), `echo` va `print`, qat'iy tiplash (`declare(strict_types=1)`), o'zgaruvchilar va o'zgarmaslar (`define`, `const`), skalyar va maxsus ma'lumot turlari (`int`, `float`, `string`, `bool`, `null`), turni o'zgartirish (type casting va type juggling), o'zgaruvchi holatini tekshiruvchi funksiyalar (`is_int`, `is_string`, `empty`, `is_null`, `var_dump`, `var_export`), arifmetik, tayinlash, taqqoslash, spaceship (`<=>`), mantiqiy operatorlar hamda shart operatorlari (`if-elseif-else`, ternar, elvis `?:`, null coalescing `??` va `??=`, `switch-case`, `goto`) bo'yicha 50 ta to'liq amaliy topshiriq jamlangan.

---

# 1-Topshiriq: PHP 'Salom, Dunyo!' va asosiy teglar
## Topshiriq sharti:
PHP skriptida standart ochilish tegi `<?php` orqali ekranga 'Salom, PHP 8.3 Dunyosi!' matnini chiqaruvchi kod yozing.

## Yechim (PHP kodi):
```php
<?php

echo "Salom, PHP 8.3 Dunyosi!
";

```

## Tushuntirish va Mantiq:
PHP skriptlari odatda `<?php` tegi bilan boshlanadi. Agar fayl faqat toza PHP kodidan iborat bo'lsa, xatoliklar va kutilmagan bo'shliqlarning oldini olish uchun yopiluvchi `?>` tegini qoldirmaslik tavsiya etiladi (PSR-12 standarti). `echo` operatori bir yoki bir nechta satrlarni konsol yoki brauzerga chiqaradi.

## Ishlash natijasi:
```text
Salom, PHP 8.3 Dunyosi!
```

# 2-Topshiriq: echo va print operatorlarining farqi
## Topshiriq sharti:
`echo` va `print` operatorlaridan foydalanib matnlarni chiqaring hamda ularning qiymat qaytarishdagi asosiy farqini amalda namoyish eting.

## Yechim (PHP kodi):
```php
<?php

// echo bir nechta argumentlarni qabul qila oladi va qiymat qaytarmaydi
echo "Birinchi qism", " - ", "Ikkinchi qism
";

// print faqat bitta argument oladi va har doim 1 qiymatini qaytaradi
$natija = print "Print orqali chiqarilgan xabar
";
echo "print qaytargan qiymat: " . $natija . "
";

```

## Tushuntirish va Mantiq:
`echo` til konstruksiyasi bo'lib, hech qanday qiymat qaytarmaydi, shu sababli u `print`ga nisbatan biroz tezroq ishlaydi va vergul bilan ajratilgan bir nechta parametrlarni qabul qilishi mumkin. `print` esa har doim butun son `1` ni qaytaradi, shuning uchun uni ifodalar (expressions) ichida ishlatish mumkin.

## Ishlash natijasi:
```text
Birinchi qism - Ikkinchi qism
Print orqali chiqarilgan xabar
print qaytargan qiymat: 1
```

# 3-Topshiriq: declare(strict_types=1) va qat'iy tiplash rejimi
## Topshiriq sharti:
`declare(strict_types=1);` direktivasini e'lon qilib, ikkita butun sonni qo'shuvchi funksiya yozing va qat'iy tiplash qanday ishlashini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

declare(strict_types=1);

function qoshish(int $a, int $b): int {
    return $a + $b;
}

$x = 15;
$y = 25;
echo "Yig'indi: " . qoshish($x, $y) . "
";

```

## Tushuntirish va Mantiq:
`declare(strict_types=1);` faylning eng boshida e'lon qilinishi shart. Bu rejim PHP ning avtomatik tip o'zgartirishini (coercive typing) o'chiradi va funksiyaga faqat e'lon qilingan turdagi argumentlar uzatilishini talab qiladi. Agar boshqa tip (masalan, string "25") uzatilsa, `TypeError` istisnosi yuzaga keladi.

## Ishlash natijasi:
```text
Yig'indi: 40
```

# 4-Topshiriq: O'zgaruvchilarni e'lon qilish va nomlash qoidalari
## Topshiriq sharti:
PHP da o'zgaruvchilar yaratish, ularning boshida `$` belgisi bo'lishi, katta-kichik harflarga sezgirligi (case-sensitive) va to'g'ri nomlash standartlarini ifodalovchi dastur tuzing.

## Yechim (PHP kodi):
```php
<?php

$ism = "Sardor";
$Ism = "Malika";
$foydalanuvchi_yoshi = 22;
$_identifikator = "USR_9921";

echo "ism: $ism
";
echo "Ism: $Ism
";
echo "Yoshi: $foydalanuvchi_yoshi
";
echo "ID: $_identifikator
";

```

## Tushuntirish va Mantiq:
PHP da o'zgaruvchilar nomi dollar belgisi (`$`) bilan boshlanadi va harf yoki tagchiziq (`_`) bilan davom etishi kerak. Raqam bilan boshlanishi mumkin emas. O'zgaruvchilar nomlari katta-kichik harflarga sezgirdir (case-sensitive), shuning uchun `$ism` va `$Ism` ikki xil o'zgaruvchi hisoblanadi.

## Ishlash natijasi:
```text
ism: Sardor
Ism: Malika
Yoshi: 22
ID: USR_9921
```

# 5-Topshiriq: define() funksiyasi orqali global konstantalar
## Topshiriq sharti:
`define()` funksiyasi yordamida dastur darajasidagi o'zgarmaslarni (konstanta) yarating va ularning qiymatini ekranga chiqaring.

## Yechim (PHP kodi):
```php
<?php

define("ILOVA_NOMI", "Khorazmiy AI Platform");
define("MAX_URINISHLAR", 5);
define("STATUSLAR", ["Yangi", "Jarayonda", "Tugallangan"]);

echo "Ilova: " . ILOVA_NOMI . "
";
echo "Maksimal urinishlar: " . MAX_URINISHLAR . "
";
echo "Birlamchi status: " . STATUSLAR[0] . "
";

```

## Tushuntirish va Mantiq:
`define()` yordamida yaratilgan konstantalar dasturning butun ishlash doirasida (global) mavjud bo'ladi. Ularning oldiga `$` belgisi qo'yilmaydi va ularni qayta o'zgartirib bo'lmaydi. PHP 7 dan boshlab `define()` orqali massivlarni ham konstanta sifatida e'lon qilish mumkin.

## Ishlash natijasi:
```text
Ilova: Khorazmiy AI Platform
Maksimal urinishlar: 5
Birlamchi status: Yangi
```

# 6-Topshiriq: const kalit so'zi orqali o'zgarmaslar yaratish
## Topshiriq sharti:
`const` kalit so'zi yordamida kompilyatsiya vaqtidagi konstantalarni e'lon qiling va `define()` dan farqini tushuntiring.

## Yechim (PHP kodi):
```php
<?php

const ALOQA_PORTI = 8080;
const TIZIM_VERSIYASI = "2.4.1";
const MATEMATIK_PI = 3.1415926535;

echo "Port: " . ALOQA_PORTI . "
";
echo "Versiya: " . TIZIM_VERSIYASI . "
";
echo "PI qiymati: " . MATEMATIK_PI . "
";

```

## Tushuntirish va Mantiq:
`const` kalit so'zi kompilyatsiya vaqtida aniqlanadi, shuning uchun u `define()` ga qaraganda tezroq bajariladi. `const` ni global darajada yoki sinflar (OOP) ichida ishlatish mumkin, lekin `if` yoki `function` kabi bloklar ichida dinamik chaqirish mumkin emas (`define` esa dinamik bloklarda ham ishlaydi).

## Ishlash natijasi:
```text
Port: 8080
Versiya: 2.4.1
PI qiymati: 3.1415926535
```

# 7-Topshiriq: gettype() yordamida o'zgaruvchi tipini aniqlash
## Topshiriq sharti:
Har xil turdagi o'zgaruvchilar (butun son, satr, massiv, mantiqiy) yaratib, `gettype()` orqali ularning tiplarini konsolga chiqaring.

## Yechim (PHP kodi):
```php
<?php

$a = 100;
$b = 99.95;
$c = "O'zbekiston";
$d = true;
$e = [1, 2, 3];
$f = null;

echo "a tipi: " . gettype($a) . "
";
echo "b tipi: " . gettype($b) . "
";
echo "c tipi: " . gettype($c) . "
";
echo "d tipi: " . gettype($d) . "
";
echo "e tipi: " . gettype($e) . "
";
echo "f tipi: " . gettype($f) . "
";

```

## Tushuntirish va Mantiq:
`gettype()` funksiyasi o'zgaruvchining asosiy tipini satr (string) shaklida qaytaradi: `integer`, `double` (float uchun), `string`, `boolean`, `array`, `NULL`, `object` yoki `resource`. Bu tekshiruv kodni disk raskadrovka qilishda qulay vositadir.

## Ishlash natijasi:
```text
a tipi: integer
b tipi: double
c tipi: string
d tipi: boolean
e tipi: array
f tipi: NULL
```

# 8-Topshiriq: var_dump() orqali o'zgaruvchilarni chuqur tahlil qilish
## Topshiriq sharti:
`var_dump()` funksiyasidan foydalanib bir nechta o'zgaruvchilarning tipi, hajmi va ichki qiymatini to'liq formatda tahlil qiling.

## Yechim (PHP kodi):
```php
<?php

$foydalanuvchi = "Ali";
$baholar = [85, 90, 95];
$faol = false;

var_dump($foydalanuvchi);
var_dump($baholar);
var_dump($faol);

```

## Tushuntirish va Mantiq:
`var_dump()` funksiyasi har qanday o'zgaruvchi yoki ifodaning tipi, uzunligi va ichki tuzilishini batafsil ko'rsatadi. Dasturchilar uchun xatoliklarni topish (debugging) jarayonida eng muhim diagnostika vositasidir.

## Ishlash natijasi:
```text
string(3) "Ali"
array(3) {
  [0]=>
  int(85)
  [1]=>
  int(90)
  [2]=>
  int(95)
}
bool(false)
```

# 9-Topshiriq: Butun sonlar (integer) va har xil sanoq sistemalari
## Topshiriq sharti:
O'nlik (decimal), ikkilik (binary), sakkizlik (octal) va o'n oltilik (hexadecimal) sanoq sistemalarida butun sonlarni e'lon qiling va ularni o'nlik tizimda chiqaring.

## Yechim (PHP kodi):
```php
<?php

$onlik = 120;
$ikkilik = 0b1111000;    // 0b prefiksi ikkilik son
$sakkizlik = 0170;       // 0 yoki 0o prefiksi sakkizlik
$on_oltilik = 0x78;      // 0x prefiksi o'n oltilik

echo "O'nlik: $onlik
";
echo "Ikkilik (0b1111000): $ikkilik
";
echo "Sakkizlik (0170): $sakkizlik
";
echo "O'n oltilik (0x78): $on_oltilik
";

```

## Tushuntirish va Mantiq:
PHP butun sonlarni turli sanoq sistemalarida qabul qiladi: `0b` prefiksi ikkilik (binary), `0` yoki `0o` sakkizlik (octal), `0x` esa o'n oltilik (hexadecimal) sonlarni ifodalaydi. PHP ichki xotirada ularni avtomatik tarzda butun son (int) sifatida saqlaydi.

## Ishlash natijasi:
```text
O'nlik: 120
Ikkilik (0b1111000): 120
Sakkizlik (0170): 120
O'n oltilik (0x78): 120
```

# 10-Topshiriq: Haqiqiy sonlar (float) va ilmiy eksponensial format
## Topshiriq sharti:
Float sonlarni oddiy hamda ilmiy (eksponensial) ko'rinishda e'lon qiling, aniqlik chegarasi va hisoblash amallarini namoyish eting.

## Yechim (PHP kodi):
```php
<?php

$narx = 19.99;
$ilmiy_katta = 1.2e6;  // 1.2 * 10^6 = 1200000
$ilmiy_kichik = 5.5e-3; // 5.5 * 10^-3 = 0.0055

echo "Narx: $narx
";
echo "Katta son: $ilmiy_katta
";
echo "Kichik son: $ilmiy_kichik
";
echo "Qo'shish: " . ($narx + 0.01) . "
";

```

## Tushuntirish va Mantiq:
Haqiqiy sonlar (float yoki double) kasr qismga ega sonlardir. `e` yoki `E` harfi orqali o'nlik darajalarni ifodalash mumkin. Float bilan ishlaganda suzuvchi nuqta (floating-point) yaxlitlash xatoliklari bo'lishi mumkinligini doimo hisobga olish kerak.

## Ishlash natijasi:
```text
Narx: 19.99
Katta son: 1200000
Kichik son: 0.0055
Qo'shish: 20
```

# 11-Topshiriq: Mantiqiy tip (boolean) va uning qiymatlari
## Topshiriq sharti:
Mantiqiy `true` va `false` qiymatlarini o'zgaruvchilarga biriktirib, ularni shartli tekshiruvlarda qo'llashni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

$server_ishlayaptimi = true;
$xatolik_bormi = false;

if ($server_ishlayaptimi && !$xatolik_bormi) {
    echo "Tizim barqaror holatda ishlayapti
";
} else {
    echo "Tizimda nosozlik aniqlandi
";
}

echo "Mantiqiy rost qiymati: " . (int)$server_ishlayaptimi . "
";
echo "Mantiqiy yolg'on qiymati: " . (int)$xatolik_bormi . "
";

```

## Tushuntirish va Mantiq:
Boolean turi faqat ikki qiymatni qabul qiladi: `true` yoki `false`. Ular registrga sezgir emas (`TRUE` yoki `FALSE` deb yozish ham mumkin, ammo kichik harf tavsiya etiladi). Satrga o'girilganda `true` '1' ga, `false` esa bo'sh satrga `""` aylanadi.

## Ishlash natijasi:
```text
Tizim barqaror holatda ishlayapti
Mantiqiy rost qiymati: 1
Mantiqiy yolg'on qiymati: 0
```

# 12-Topshiriq: Null qiymati va unset() orqali xotiradan tozalash
## Topshiriq sharti:
`null` qiymatiga ega o'zgaruvchi e'lon qiling, `unset()` funksiyasi yordamida o'zgaruvchini xotiradan butunlay o'chirishni namoyish eting.

## Yechim (PHP kodi):
```php
<?php

$foydalanuvchi_email = null;

if (is_null($foydalanuvchi_email)) {
    echo "Foydalanuvchi email kiritmagan
";
}

$vaqtinchalik_kods = "SMS_4481";
unset($vaqtinchalik_kods);

echo "O'chirilgandan so'ng mavjudmi: " . (isset($vaqtinchalik_kods) ? "Ha" : "Yo'q") . "
";

```

## Tushuntirish va Mantiq:
`null` o'zgaruvchining hech qanday qiymatga ega emasligini bildiradi. O'zgaruvchiga qiymat berilmagan bo'lsa yoki unga `null` o'zlashtirilgan bo'lsa, u NULL hisoblanadi. `unset()` funksiyasi o'zgaruvchini butunlay yo'q qiladi va xotirani bo'shatadi.

## Ishlash natijasi:
```text
Foydalanuvchi email kiritmagan
O'chirilgandan so'ng mavjudmi: Yo'q
```

# 13-Topshiriq: Satrlar va belgilar indeksatsiyasi
## Topshiriq sharti:
Satr o'zgaruvchisi yarating va kvadrat qavslar `[]` yordamida uning alohida belgilarini o'qish hamda o'zgartirishni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

$soz = "Toshkent";

echo "Birinchi belgi: " . $soz[0] . "
";
echo "Oxirgi belgi: " . $soz[strlen($soz) - 1] . "
";

// Belgini o'zgartirish
$soz[0] = "B";
echo "O'zgargan so'z: $soz
";

```

## Tushuntirish va Mantiq:
PHP da satrlarni xuddi belgilar massivi kabi `[indeks]` orqali o'qish va alohida baytlarni almashtirish mumkin. Esda tutingki, bu operatsiya ASCII belgilar uchun to'g'ri ishlaydi, ko'p baytli UTF-8 (masalan, o'zbekcha 'oʻ' yoki 'gʻ') belgilar uchun `mb_*` funksiyalaridan foydalanish zarur.

## Ishlash natijasi:
```text
Birinchi belgi: T
Oxirgi belgi: t
O'zgargan so'z: Boshkent
```

# 14-Topshiriq: Type Casting: Satrni butun songa o'girish
## Topshiriq sharti:
`(int)` va `(integer)` kasting operatorlari yordamida turli ko'rinishdagi satrlarni butun songa xavfsiz o'giring.

## Yechim (PHP kodi):
```php
<?php

$satr1 = "450";
$satr2 = "120 kitob";
$satr3 = "Narxi: 500";

$son1 = (int)$satr1;
$son2 = (int)$satr2;
$son3 = (int)$satr3;

echo "son1: $son1 (tip: " . gettype($son1) . ")
";
echo "son2: $son2 (boshidagi son olindi)
";
echo "son3: $son3 (boshida raqam bo'lmagani uchun 0)
";

```

## Tushuntirish va Mantiq:
`(int)` orqali satr songa aylantirilganda, PHP satr boshidagi raqamlarni oladi. Agar satr raqam bilan boshlanmasa, natija `0` bo'ladi. PHP 8 da satrlarni solishtirish va kasting qilish qoidalari ancha qat'iylashtirilgan.

## Ishlash natijasi:
```text
son1: 450 (tip: integer)
son2: 120 (boshidagi son olindi)
son3: 0 (boshida raqam bo'lmagani uchun 0)
```

# 15-Topshiriq: Type Casting: Sonlarni satrga aylantirish
## Topshiriq sharti:
`(string)` operatori va strval() funksiyasi orqali butun hamda kasr sonlarni satrga o'giring.

## Yechim (PHP kodi):
```php
<?php

$balans = 1500000;
$stavka = 12.5;

$balans_matn = (string)$balans;
$stavka_matn = strval($stavka);

echo "Balans uzunligi: " . strlen($balans_matn) . " ta belgi
";
echo "Stavka matni: " . $stavka_matn . "%
";
echo "Tip: " . gettype($balans_matn) . "
";

```

## Tushuntirish va Mantiq:
Sonlarni satrga aylantirish uchun `(string)$o'zgaruvchi` yoki `strval($o'zgaruvchi)` ishlatiladi. Shuningdek, qo'shtirnoq ichida `"$balans"` deb yozish ham avtomatik satrga interpolyatsiya qiladi.

## Ishlash natijasi:
```text
Balans uzunligi: 7 ta belgi
Stavka matni: 12.5%
Tip: string
```

# 16-Topshiriq: Type Casting: Mantiqiy (boolean) tipga o'girish qoidalari
## Topshiriq sharti:
`(bool)` kasting operatori orqali har xil qiymatlarning (0, 1, bo'sh satr, bo'sh massiv, null) rostlikka tekshirilishini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

$qiymatlar = [
    0,
    1,
    -5,
    "",
    "0",
    "PHP",
    [],
    [10],
    null
];

foreach ($qiymatlar as $q) {
    $bool_qiymat = (bool)$q;
    $matn_reprezentatsiya = var_export($q, true);
    echo "$matn_reprezentatsiya -> " . ($bool_qiymat ? "TRUE" : "FALSE") . "
";
}

```

## Tushuntirish va Mantiq:
PHP da quyidagi qiymatlar `false` deb baholanadi: butun son `0`, suzuvchi nuqtali `0.0`, bo'sh satr `""`, satr `"0"`, bo'sh massiv `[]`, `null`, va atributsiz bo'sh SimpleXML obyekti. Qolgan barcha qiymatlar (jumladan manfiy sonlar `-5`, bo'sh bo'lmagan massivlar) `true` hisoblanadi.

## Ishlash natijasi:
```text
0 -> FALSE
1 -> TRUE
-5 -> TRUE
'' -> FALSE
'0' -> FALSE
'PHP' -> TRUE
array (
) -> FALSE
array (
  0 => 10,
) -> TRUE
NULL -> FALSE
```

# 17-Topshiriq: is_int(), is_float(), is_numeric() tekshiruvlari
## Topshiriq sharti:
Berilgan o'zgaruvchilarni `is_int()`, `is_float()` va `is_numeric()` funksiyalari orqali tekshirib, farqlarini aniqlang.

## Yechim (PHP kodi):
```php
<?php

$qiymat1 = 42;
$qiymat2 = "42";
$qiymat3 = 3.14;

echo "qiymat1 (42):
";
echo "  is_int: " . (is_int($qiymat1) ? "ha" : "yo'q") . "
";
echo "  is_numeric: " . (is_numeric($qiymat1) ? "ha" : "yo'q") . "
";

echo "qiymat2 ('42'):
";
echo "  is_int: " . (is_int($qiymat2) ? "ha" : "yo'q") . "
";
echo "  is_numeric: " . (is_numeric($qiymat2) ? "ha" : "yo'q") . "
";

echo "qiymat3 (3.14):
";
echo "  is_float: " . (is_float($qiymat3) ? "ha" : "yo'q") . "
";
echo "  is_numeric: " . (is_numeric($qiymat3) ? "ha" : "yo'q") . "
";

```

## Tushuntirish va Mantiq:
`is_int()` faqat o'zgaruvchi integer tipida bo'lsa `true` qaytaradi. `is_float()` faqat float bo'lsa ishlaydi. `is_numeric()` esa qiymat raqam bo'lsa yoki raqamlardan iborat satr (masalan `"42"` yoki `"3.14"`) bo'lsa ham `true` qaytaradi, bu tashqi HTTP so'rovlardan kelgan ma'lumotlarni tekshirishda juda qo'l keladi.

## Ishlash natijasi:
```text
qiymat1 (42):
  is_int: ha
  is_numeric: ha
qiymat2 ('42'):
  is_int: yo'q
  is_numeric: ha
qiymat3 (3.14):
  is_float: ha
  is_numeric: ha
```

# 18-Topshiriq: is_string() va is_bool() funksiyalari
## Topshiriq sharti:
Foydalanuvchi profili maydonlarini `is_string()` va `is_bool()` funksiyalari yordamida tekshiruvchi funksiya yozing.

## Yechim (PHP kodi):
```php
<?php

function tekshirParametr($nom, $qiymat): void {
    if (is_string($qiymat)) {
        echo "$nom satr turida: '$qiymat'
";
    } elseif (is_bool($qiymat)) {
        echo "$nom mantiqiy turda: " . ($qiymat ? "ROST" : "YOLG'ON") . "
";
    } else {
        echo "$nom boshqa turda
";
    }
}

tekshirParametr("Ism", "Dilshod");
tekshirParametr("Aktiv", true);
tekshirParametr("ID", 101);

```

## Tushuntirish va Mantiq:
`is_string()` berilgan o'zgaruvchining satr ekanligini, `is_bool()` esa uning boolean tipdaligini qat'iy aniqlaydi. Funksiyaga kelayotgan aralash parametrlar validatsiyasida ular samarali vositadir.

## Ishlash natijasi:
```text
Ism satr turida: 'Dilshod'
Aktiv mantiqiy turda: ROST
ID boshqa turda
```

# 19-Topshiriq: is_null() va empty() tekshiruvlari o'rtasidagi farq
## Topshiriq sharti:
`is_null()` va `empty()` funksiyalarining turli qiymatlarga (0, "", null, []) qanday munosabat bildirishini taqqoslang.

## Yechim (PHP kodi):
```php
<?php

$sinovlar = [
    "null" => null,
    "nol soni" => 0,
    "bo'sh satr" => "",
    "bo'sh massiv" => []
];

foreach ($sinovlar as $nom => $qiymat) {
    $nullmi = is_null($qiymat) ? "ha" : "yo'q";
    $boshmi = empty($qiymat) ? "ha" : "yo'q";
    echo "$nom -> is_null: $nullmi, empty: $boshmi
";
}

```

## Tushuntirish va Mantiq:
`is_null()` faqat qiymat aynan `null` bo'lgandagina `true` qaytaradi. `empty()` esa o'zgaruvchi mavjud bo'lmasa, yoki qiymati `null`, `0`, `0.0`, `""`, `"0"`, `[]` bo'lsa ham `true` qaytaradi. Shuning uchun nol yoki bo'sh satrni tekshirishda `empty()` ehtiyotkorlik bilan ishlatilishi lozim.

## Ishlash natijasi:
```text
null -> is_null: ha, empty: ha
nol soni -> is_null: yo'q, empty: ha
bo'sh satr -> is_null: yo'q, empty: ha
bo'sh massiv -> is_null: yo'q, empty: ha
```

# 20-Topshiriq: var_export() orqali to'g'ridan-to'g'ri qayta ishlatiluvchi kod yaratish
## Topshiriq sharti:
`var_export()` funksiyasidan foydalanib murakkab assotsiativ massivni PHP kodi ko'rinishida satrga o'giring va ekranga chiqaring.

## Yechim (PHP kodi):
```php
<?php

$sozlamalar = [
    "db_host" => "localhost",
    "db_port" => 3306,
    "ssl" => true,
    "keshlar" => ["redis", "memcached"]
];

$php_kodi = var_export($sozlamalar, true);

echo "Eksport qilingan kod:
";
echo $php_kodi . ";
";

```

## Tushuntirish va Mantiq:
`var_export()` o'zgaruvchining PHP sintaksisiga mos keluvchi strukturasini qaytaradi. Ikkinchi parametri `true` qilib berilsa, u natijani to'g'ridan-to'g'ri chop etmasdan o'zgaruvchiga qaytaradi. Bu konfiguratsiya fayllarini avtomatik generatsiya qilish va keshga saqlashda ishlatiladi.

## Ishlash natijasi:
```text
Eksport qilingan kod:
array (
  'db_host' => 'localhost',
  'db_port' => 3306,
  'ssl' => true,
  'keshlar' => 
  array (
    0 => 'redis',
    1 => 'memcached',
  ),
);
```

# 21-Topshiriq: Arifmetik operatorlar: Qo'shish, ayirish va ko'paytirish
## Topshiriq sharti:
Mahsulot narxi, miqdori va yetkazib berish haqi berilgan holatda umumiy summani arifmetik operatorlar (+, -, *) yordamida hisoblang.

## Yechim (PHP kodi):
```php
<?php

$birlik_narx = 45000;
$miqdor = 3;
$yetkazish = 15000;
$chegirma = 10000;

$jami_mahsulotlar = $birlik_narx * $miqdor;
$yakuniy_summa = ($jami_mahsulotlar + $yetkazish) - $chegirma;

echo "Mahsulotlar summasi: $jami_mahsulotlar so'm
";
echo "Chegirma va yetkazish bilan yakuniy summa: $yakuniy_summa so'm
";

```

## Tushuntirish va Mantiq:
`*` ko'paytirish, `+` qo'shish va `-` ayirish arifmetik amallaridir. Matematik qonuniyatlarga ko'ra ko'paytirish va bo'lish qo'shish va ayirishdan oldin bajariladi, ustuvorlikni boshqarish uchun qavslar ishlatiladi.

## Ishlash natijasi:
```text
Mahsulotlar summasi: 135000 so'm
Chegirma va yetkazish bilan yakuniy summa: 140000 so'm
```

# 22-Topshiriq: Bo'lish operatori (/) va butun sonli bo'lish (intdiv)
## Topshiriq sharti:
`/` bo'lish operatori va `intdiv()` funksiyasining farqini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

$jami_soniya = 125;

$minutlar_float = $jami_soniya / 60;
$minutlar_butun = intdiv($jami_soniya, 60);
$qolgan_soniya = $jami_soniya % 60;

echo "Oddiy bo'lish (/): $minutlar_float
";
echo "Butun bo'lish (intdiv): $minutlar_butun minut, $qolgan_soniya soniya
";

```

## Tushuntirish va Mantiq:
PHP da `/` bo'lish operatori agar sonlar qoldiqsiz bo'linmasa, avtomatik ravishda `float` natija qaytaradi. `intdiv($a, $b)` funksiyasi esa qoldiqni tashlab yuborib faqat butun qismini (`int`) qaytaradi.

## Ishlash natijasi:
```text
Oddiy bo'lish (/): 2.0833333333333335
Butun bo'lish (intdiv): 2 minut, 5 soniya
```

# 23-Topshiriq: Qoldiqli bo'lish (modulus %) operatori
## Topshiriq sharti:
Berilgan sonning juft yoki toqligini `%` (modulus) operatori yordamida aniqlovchi dastur tuzing.

## Yechim (PHP kodi):
```php
<?php

function juftYokiToq(int $son): string {
    if ($son % 2 === 0) {
        return "$son - juft son";
    }
    return "$son - toq son";
}

echo juftYokiToq(28) . "
";
echo juftYokiToq(37) . "
";
echo juftYokiToq(0) . "
";

```

## Tushuntirish va Mantiq:
`%` operatori birinchi sonni ikkinchi songa bo'lgandagi qoldiqni hisoblaydi. Agar `$son % 2 === 0` bo'lsa, son juft, aks holda toq bo'ladi. Modulus amali sonlarni davriy aylantirishda ham juda qulay.

## Ishlash natijasi:
```text
28 - juft son
37 - toq son
0 - juft son
```

# 24-Topshiriq: Darajaga ko'tarish operatori (**)
## Topshiriq sharti:
`**` operatori yordamida sonlarning kvadrat, kub va ixtiyoriy darajasini hisoblang.

## Yechim (PHP kodi):
```php
<?php

$asos = 4;
$daraja = 3;

$natija = $asos ** $daraja; // 4 * 4 * 4
$kvadrat_ildiz = 16 ** 0.5; // ildiz chiqarish

echo "$asos ning $daraja-darajasi: $natija
";
echo "16 ning kvadrat ildizi: $kvadrat_ildiz
";

```

## Tushuntirish va Mantiq:
PHP 5.6 versiyasidan boshlab `**` operatori darajaga ko'tarish uchun joriy qilingan. Bu `pow($asos, $daraja)` funksiyasi bilan bir xil ishlaydi, ammo sintaktik jihatdan ixchamroq va o'qilishi osonroq.

## Ishlash natijasi:
```text
4 ning 3-darajasi: 64
16 ning kvadrat ildizi: 4
```

# 25-Topshiriq: Unar plyus va minus operatorlari
## Topshiriq sharti:
Unar `+` va `-` operatorlari son qiymatlariga va raqamli satrlarga qanday ta'sir qilishini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

$satr_raqam = "50";
$musbat = +$satr_raqam;  // int ga o'giradi
$manfiy = -$satr_raqam;  // int ga o'girib manfiy qiladi

echo "Musbat: $musbat, tipi: " . gettype($musbat) . "
";
echo "Manfiy: $manfiy, tipi: " . gettype($manfiy) . "
";
echo "Manfiyning inkori: " . (-$manfiy) . "
";

```

## Tushuntirish va Mantiq:
Unar `+` operatori operandni raqamga (int yoki float) o'giradi. Unar `-` operatori esa qiymatning ishorasini teskarisiga o'zgartiradi va bir vaqtning o'zida uni raqam tipiga aylantiradi.

## Ishlash natijasi:
```text
Musbat: 50, tipi: integer
Manfiy: -50, tipi: integer
Manfiyning inkori: 50
```

# 26-Topshiriq: Prefiks va postfiks inkrement (++$x vs $x++)
## Topshiriq sharti:
Prefiks (`++$a`) va postfiks (`$a++`) inkrement operatorlari o'rtasidagi farqni ifoda ichida namoyish eting.

## Yechim (PHP kodi):
```php
<?php

$a = 5;
echo "Boshlang'ich a: $a
";
echo "Postfiks a++ natijasi: " . ($a++) . " (lekin amaldan so'ng a = $a)
";

$b = 5;
echo "Boshlang'ich b: $b
";
echo "Prefiks ++b natijasi: " . (++$b) . " (amaldan so'ng b = $b)
";

```

## Tushuntirish va Mantiq:
`$a++` (postfiks) avval o'zgaruvchining joriy qiymatini ifodaga qaytaradi, so'ngra uning qiymatini 1 ga oshiradi. `++$b` (prefiks) esa avval o'zgaruvchini 1 ga oshiradi, so'ngra yangi oshirilgan qiymatni ifodaga qaytaradi.

## Ishlash natijasi:
```text
Boshlang'ich a: 5
Postfiks a++ natijasi: 5 (lekin amaldan so'ng a = 6)
Boshlang'ich b: 5
Prefiks ++b natijasi: 6 (amaldan so'ng b = 6)
```

# 27-Topshiriq: Prefiks va postfiks dekrement (--$x vs $x--)
## Topshiriq sharti:
Prefiks (`--$x`) va postfiks (`$x--`) dekrement operatorlarini taqqoslang.

## Yechim (PHP kodi):
```php
<?php

$x = 10;
$y = $x--; // y ga 10 o'tadi, x esa 9 bo'ladi

echo "Postfiks: x = $x, y = $y
";

$m = 10;
$n = --$m; // m 9 bo'ladi va n ga 9 o'tadi

echo "Prefiks: m = $m, n = $n
";

```

## Tushuntirish va Mantiq:
Dekrement operatori o'zgaruvchi qiymatini 1 ga kamaytiradi. Postfiks (`$x--`) eski qiymatni qaytarib keyin kamaytirsa, prefiks (`--$m`) darhol kamaytirib yangi qiymatni qaytaradi.

## Ishlash natijasi:
```text
Postfiks: x = 9, y = 10
Prefiks: m = 9, n = 9
```

# 28-Topshiriq: Qisqartirilgan tayinlash operatorlari (+=, -=, *=, /=)
## Topshiriq sharti:
O'zgaruvchi qiymatini `+=`, `-=`, `*=` va `/=` operatorlari yordamida yangilovchi hisoblagich tuzing.

## Yechim (PHP kodi):
```php
<?php

$jami = 100;
echo "Boshlang'ich: $jami
";

$jami += 50;  // 150
echo "+= 50 dan keyin: $jami
";

$jami -= 30;  // 120
echo "-= 30 dan keyin: $jami
";

$jami *= 2;   // 240
echo "*= 2 dan keyin: $jami
";

$jami /= 4;   // 60
echo "/= 4 dan keyin: $jami
";

```

## Tushuntirish va Mantiq:
Qisqartirilgan tayinlash operatorlari `$a = $a + $b` amalini `$a += $b` ko'rinishida yozish imkonini beradi. Bu kodni ixcham va tez o'qiladigan qiladi.

## Ishlash natijasi:
```text
Boshlang'ich: 100
+= 50 dan keyin: 150
-= 30 dan keyin: 120
*= 2 dan keyin: 240
/= 4 dan keyin: 60
```

# 29-Topshiriq: Satr ulab tayinlash operatori (.=)
## Topshiriq sharti:
Satrlarni ketma-ket ulash (konkatenatsiya) uchun `.=` operatoridan foydalanib HTML ro'yxat generatorini yozing.

## Yechim (PHP kodi):
```php
<?php

$matn = "Mavzular:";
$matn .= " 1. PHP Asoslari;";
$matn .= " 2. OOP Dasturlash;";
$matn .= " 3. Laravel Framework.";

echo $matn . "
";

```

## Tushuntirish va Mantiq:
`.=` operatori o'ng tomondagi satrni chap tomondagi satr oxiriga ulaydi (konkatenatsiya qiladi). Bu `$matn = $matn . "qo'shimcha"` ifodasining qisqa va qulay shaklidir.

## Ishlash natijasi:
```text
Mavzular: 1. PHP Asoslari; 2. OOP Dasturlash; 3. Laravel Framework.
```

# 30-Topshiriq: Null Coalescing tayinlash operatori (??=)
## Topshiriq sharti:
PHP 7.4 da kiritilgan `??=` (Null Coalescing Assignment) operatori orqali sukut bo'yicha parametrlar berishni amalga oshiring.

## Yechim (PHP kodi):
```php
<?php

$foydalanuvchi = [
    "ism" => "Zokir",
    "til" => null
];

// Agar 'til' null bo'lsa yoki mavjud bo'lmasa, 'uz' qiymati berilsin
$foydalanuvchi["til"] ??= "uz";
$foydalanuvchi["mavzu"] ??= "qorong'i";

echo "Til: " . $foydalanuvchi["til"] . "
";
echo "Mavzu: " . $foydalanuvchi["mavzu"] . "
";

```

## Tushuntirish va Mantiq:
`$a ??= $b` ifodasi `$a = $a ?? $b` ning qisqartmasidir. Agar chap tomondagi o'zgaruvchi e'lon qilinmagan yoki `null` bo'lsa, unga o'ng tarafdagi qiymat tayinlanadi. Agar qiymati mavjud bo'lsa, o'zgarishsiz qoladi.

## Ishlash natijasi:
```text
Til: uz
Mavzu: qorong'i
```

# 31-Topshiriq: Tenglik operatorlari: Bo'sh tenglik (==) va Qat'iy tenglik (===)
## Topshiriq sharti:
`==` (type juggling) va `===` (strict equality) operatorlarining farqini aniq misollar orqali ko'rsating.

## Yechim (PHP kodi):
```php
<?php

$son = 100;
$satr = "100";

echo "== taqqoslash: ";
if ($son == $satr) {
    echo "Teng (tiplar avtomatik moslashtirildi)
";
} else {
    echo "Teng emas
";
}

echo "=== taqqoslash: ";
if ($son === $satr) {
    echo "Teng
";
} else {
    echo "Teng emas (chunki int !== string)
";
}

```

## Tushuntirish va Mantiq:
`==` faqat qiymatlarni solishtiradi va kerak bo'lsa ularning turlarini avtomatik o'zgartiradi (type juggling). `===` esa ham qiymatni, ham o'zgaruvchi turini (type) qat'iy tekshiradi. Zamonaviy PHP da har doim `===` dan foydalanish xavfsizlik va barqarorlik garovidir.

## Ishlash natijasi:
```text
== taqqoslash: Teng (tiplar avtomatik moslashtirildi)
=== taqqoslash: Teng emas (chunki int !== string)
```

# 32-Topshiriq: Tengsizlik operatorlari: != va !== farqi
## Topshiriq sharti:
`!=` va `!==` operatorlari yordamida o'zgaruvchilarni solishtiring va qat'iy tengsizlik qanday ishlashini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

$foydalanuvchi_turi = 0;
$admin_emas = false;

echo "!= natijasi: " . ($foydalanuvchi_turi != $admin_emas ? "Farqli" : "Bir xil deb topildi") . "
";
echo "!== natijasi: " . ($foydalanuvchi_turi !== $admin_emas ? "Farqli (to'g'ri tekshiruv)" : "Bir xil") . "
";

```

## Tushuntirish va Mantiq:
`!=` solishtirishida `0` va `false` bir xil deb hisoblanishi mumkin, chunki bo'sh taqqoslashda tiplar konvertatsiya qilinadi. Ammo `!==` operatori ularning tipi har xilligini (int va bool) ko'radi va to'g'ri qaror qabul qiladi.

## Ishlash natijasi:
```text
!= natijasi: Bir xil deb topildi
!== natijasi: Farqli (to'g'ri tekshiruv)
```

# 33-Topshiriq: Katta va kichik taqqoslash operatorlari (<, >, <=, >=)
## Topshiriq sharti:
Foydalanuvchi yoshiga qarab uning toifasini (bola, o'smir, katta) taqqoslash operatorlari orqali aniqlang.

## Yechim (PHP kodi):
```php
<?php

$yosh = 18;

if ($yosh < 7) {
    echo "Maktabgacha yosh
";
} elseif ($yosh >= 7 && $yosh < 18) {
    echo "Maktab o'quvchisi
";
} elseif ($yosh >= 18 && $yosh <= 60) {
    echo "Mehnatga layoqatli katta yosh
";
} else {
    echo "Nafaqaxo'r
";
}

```

## Tushuntirish va Mantiq:
`<` (kichik), `>` (katta), `<=` (kichik yoki teng), `>=` (katta yoki teng) operatorlari sonli va leksikografik solishtirishlarda shartlarni tekshirish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Mehnatga layoqatli katta yosh
```

# 34-Topshiriq: Spaceship operatori (<=>) va uning natijalari
## Topshiriq sharti:
PHP 7 da qo'shilgan `<=>` (Spaceship) operatorining -1, 0, 1 qiymat qaytarish qoidasini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

echo "5 <=> 10 : " . (5 <=> 10) . " (birinchi son kichik)
";
echo "10 <=> 10 : " . (10 <=> 10) . " (ikkala son teng)
";
echo "15 <=> 10 : " . (15 <=> 10) . " (birinchi son katta)
";

// usort() da qulay ishlatilishi
$massiv = [42, 10, 88, 5, 23];
usort($massiv, fn($a, $b) => $a <=> $b);
echo "Saralangan: " . implode(", ", $massiv) . "
";

```

## Tushuntirish va Mantiq:
`$a <=> $b` operatori: agar `$a < $b` bo'lsa `-1`, `$a == $b` bo'lsa `0`, `$a > $b` bo'lsa `1` qaytaradi. U ayniqsa `usort()` funksiyasida maxsus saralash qoidalarini yozishda nihoyatda qulay vositadir.

## Ishlash natijasi:
```text
5 <=> 10 : -1 (birinchi son kichik)
10 <=> 10 : 0 (ikkala son teng)
15 <=> 10 : 1 (birinchi son katta)
Saralangan: 5, 10, 23, 42, 88
```

# 35-Topshiriq: Mantiqiy VA operatori: && va and farqi
## Topshiriq sharti:
`&&` va `and` operatorlari o'rtasidagi ustuvorlik (precedence) farqini amaliy kod orqali isbotlang.

## Yechim (PHP kodi):
```php
<?php

// && operatori tayinlash (=) ga nisbatan yuqori ustuvorlikka ega
$natija1 = true && false;
echo "true && false natijasi: " . ($natija1 ? "true" : "false") . "
";

// and operatori tayinlash (=) ga nisbatan PAST ustuvorlikka ega!
$natija2 = true and false;
// Bu aslida: ($natija2 = true) and false; deb bajariladi!
echo "true and false natijasi: " . ($natija2 ? "true (tayinlash oldin yuz berdi!)" : "false") . "
";

```

## Tushuntirish va Mantiq:
`&&` operatori tayinlash (`=`) operatoridan kuchliroq ustuvorlikka ega, shuning uchun ifoda to'liq hisoblanib keyin natija o'zgaruvchiga yoziladi. `and` operatori esa `=` dan ham kuchsizroq, shuning uchun avval chap qism o'zlashtiriladi. Shu sababli doimo `&&` dan foydalanish xavfsiz.

## Ishlash natijasi:
```text
true && false natijasi: false
true and false natijasi: true (tayinlash oldin yuz berdi!)
```

# 36-Topshiriq: Mantiqiy YOKI operatori: || va or farqi
## Topshiriq sharti:
`||` va `or` mantiqiy operatorlarini ifodalarda qo'llab, ularning xususiyatlarini tushuntiring.

## Yechim (PHP kodi):
```php
<?php

$login_email = "test@example.com";
$login_telefon = "";

// Foydalanuvchi email YOKI telefon orqali kirishi mumkin
if (!empty($login_email) || !empty($login_telefon)) {
    echo "Identifikatsiya vositasi kiritildi
";
} else {
    echo "Hech qanday ma'lumot kiritilmadi
";
}

```

## Tushuntirish va Mantiq:
`||` operatori agar kamida bitta shart rost bo'lsa `true` qaytaradi. Ikkala shart yolg'on bo'lgandagina `false` bo'ladi. Xuddi `and` kabi, `or` operatori ham juda past ustuvorlikka ega, shuning uchun shart bloklarida odatda `||` ishlatiladi.

## Ishlash natijasi:
```text
Identifikatsiya vositasi kiritildi
```

# 37-Topshiriq: Mantiqiy EMAS operatori (!) va juft inkor (!!)
## Topshiriq sharti:
`!` (not) operatori va har qanday qiymatni tezkor boolean ga o'girish uchun `!!` (double not) usulini namoyish eting.

## Yechim (PHP kodi):
```php
<?php

$avtorizatsiyadan_otgan = false;

echo "Avtorizatsiya yo'qmi: " . (!$avtorizatsiyadan_otgan ? "Ha" : "Yo'q") . "
";

$matn = "Salom";
$massiv = [];

// !! orqali tezkor bool ga o'girish
$matn_bormi = !!$matn;
$massiv_bormi = !!$massiv;

echo "Matn mavjudmi: " . ($matn_bormi ? "Ha" : "Yo'q") . "
";
echo "Massiv elementlarga egami: " . ($massiv_bormi ? "Ha" : "Yo'q") . "
";

```

## Tushuntirish va Mantiq:
`!` operatori mantiqiy qiymatni teskarisiga aylantiradi (`true` ni `false` ga, `false` ni `true` ga). Juft inkor `!!` esa birinchi inkor orqali teskari bool qilib, ikkinchisi orqali asl haqiqiy boolean qiymatga aylantirib beradi.

## Ishlash natijasi:
```text
Avtorizatsiya yo'qmi: Ha
Matn mavjudmi: Ha
Massiv elementlarga egami: Yo'q
```

# 38-Topshiriq: Mantiqiy XOR (istisno qiluvchi yoki) operatori
## Topshiriq sharti:
`xor` operatoridan foydalanib, faqat va faqat bitta shart bajarilganda ishlaydigan mantiqni yozing.

## Yechim (PHP kodi):
```php
<?php

function tekshirBonus(bool $yangiMijoz, bool $promokodBor): void {
    if ($yangiMijoz xor $promokodBor) {
        echo "Aksiya qo'llaniladi (faqat bittasi bajarildi)
";
    } else {
        echo "Aksiya qo'llanilmaydi (yoki ikkalasi ham bor, yoki ikkalasi ham yo'q)
";
    }
}

tekshirBonus(true, false);
tekshirBonus(true, true);
tekshirBonus(false, false);

```

## Tushuntirish va Mantiq:
`xor` (exclusive OR) agar operandlardan faqat bittasi `true` bo'lsa `true` qaytaradi. Agar ikkalasi ham `true` bo'lsa yoki ikkalasi ham `false` bo'lsa, natija `false` bo'ladi.

## Ishlash natijasi:
```text
Aksiya qo'llaniladi (faqat bittasi bajarildi)
Aksiya qo'llanilmaydi (yoki ikkalasi ham bor, yoki ikkalasi ham yo'q)
Aksiya qo'llanilmaydi (yoki ikkalasi ham bor, yoki ikkalasi ham yo'q)
```

# 39-Topshiriq: Qisqa tutashuv (Short-circuit evaluation) mantiqiy ifodalarda
## Topshiriq sharti:
Funksiya chaqiruvlari orqali `&&` va `||` da ikkinchi tomon qachon bajarilmasligini (short-circuit) isbotlang.

## Yechim (PHP kodi):
```php
<?php

function birinchi(): bool {
    echo "1-funksiya chaqirildi
";
    return false;
}

function ikkinchi(): bool {
    echo "2-funksiya chaqirildi
";
    return true;
}

echo "--- VA (&&) sinovi ---
";
// Agar birinchi false bo'lsa, ikkinchi funksiya umuman ishga tushirilmaydi!
$natija = birinchi() && ikkinchi();

echo "--- YOKI (||) sinovi ---
";
// Agar ikkinchi true bo'lsa...
$natija2 = ikkinchi() || birinchi();

```

## Tushuntirish va Mantiq:
Short-circuit evaluation - mantiqiy ifodaning yakuniy natijasi aniq bo'lishi bilanoq keyingi ifodalar hisoblanmasligidir. `false && ...` bo'lsa ikkinchi tomon chaqirilmaydi. `true || ...` bo'lsa ham ikkinchi tomon chaqirilmaydi. Bu xatoliklarni oldini olish va samaradorlik uchun juda muhim.

## Ishlash natijasi:
```text
--- VA (&&) sinovi ---
1-funksiya chaqirildi
--- YOKI (||) sinovi ---
2-funksiya chaqirildi
```

# 40-Topshiriq: Operatorlar prioriteti (precedence) va qavslardan to'g'ri foydalanish
## Topshiriq sharti:
Murakkab arifmetik va mantiqiy ifodada qavslarning ta'sirini ko'rsatuvchi dastur yozing.

## Yechim (PHP kodi):
```php
<?php

$a = 5;
$b = 10;
$c = 2;

$natija1 = $a + $b * $c;       // 5 + (10 * 2) = 25
$natija2 = ($a + $b) * $c;     // (5 + 10) * 2 = 30

echo "Qavssiz: $natija1
";
echo "Qavs bilan: $natija2
";

```

## Tushuntirish va Mantiq:
Operatorlar ma'lum bir ustuvorlik tartibiga (precedence) ega. Masalan, ko'paytirish qo'shishdan oldin bajariladi. Kodning o'qilishi oson bo'lishi va kutilmagan mantiqiy xatoliklar yuz bermasligi uchun har doim qavslardan foydalanish tavsiya etiladi.

## Ishlash natijasi:
```text
Qavssiz: 25
Qavs bilan: 30
```

# 41-Topshiriq: Oddiy if shart operatori
## Topshiriq sharti:
Foydalanuvchi hisobidagi mablag' to'lov uchun yetarli ekanligini `if` operatori yordamida tekshiring.

## Yechim (PHP kodi):
```php
<?php

$hisob = 50000;
$narx = 35000;

if ($hisob >= $narx) {
    echo "To'lov muvaffaqiyatli amalga oshirildi
";
    $hisob -= $narx;
}

echo "Qoldiq hisob: $hisob so'm
";

```

## Tushuntirish va Mantiq:
`if` operatori qavs ichidagi shart rost (`true`) bo'lgandagina uning jingalak qavslari ichidagi kod blokini ishga tushiradi. Agar shart yolg'on bo'lsa, kod bloki tashlab o'tiladi.

## Ishlash natijasi:
```text
To'lov muvaffaqiyatli amalga oshirildi
Qoldiq hisob: 15000 so'm
```

# 42-Topshiriq: if-else shart operatori
## Topshiriq sharti:
Talabaning imtihon bali 60 yoki undan yuqori bo'lsa 'O'tdi', aks holda 'Yiqildi' xabarini chiqaruvchi `if-else` dasturini yozing.

## Yechim (PHP kodi):
```php
<?php

$ball = 74;

if ($ball >= 60) {
    echo "Tabriklaymiz, siz imtihondan o'tdingiz!
";
} else {
    echo "Afsuski, imtihondan o'ta olmadingiz.
";
}

```

## Tushuntirish va Mantiq:
`if-else` konstruksiyasida shart `true` bo'lsa `if` bloki, shart `false` bo'lganda esa `else` bloki bajarilishi kafolatlanadi.

## Ishlash natijasi:
```text
Tabriklaymiz, siz imtihondan o'tdingiz!
```

# 43-Topshiriq: if-elseif-else shart zanjiri
## Topshiriq sharti:
Ob-havo haroratiga qarab tavsiyalar beruvchi ko'p tarmoqli `if-elseif-else` zanjirini tuzing.

## Yechim (PHP kodi):
```php
<?php

$harorat = 24;

if ($harorat < 0) {
    echo "Havo juda sovuq, qalin kiyining.
";
} elseif ($harorat < 15) {
    echo "Havo salqin, kurtka kiyish tavsiya etiladi.
";
} elseif ($harorat <= 28) {
    echo "Ob-havo juda yoqimli va iliq.
";
} else {
    echo "Havo juda issiq, ko'proq suv iching.
";
}

```

## Tushuntirish va Mantiq:
`if-elseif-else` ketma-ket bir nechta shartlarni tekshirish imkonini beradi. Qaysi shart birinchi bo'lib `true` bo'lsa, faqat o'sha blok ishlaydi va qolgan tekshiruvlar to'xtatiladi. Hech biri to'g'ri kelmasa `else` qismi ishlaydi.

## Ishlash natijasi:
```text
Ob-havo juda yoqimli va iliq.
```

# 44-Topshiriq: Ichma-ich joylashgan if (nested if) shartlari
## Topshiriq sharti:
Foydalanuvchining login va parolini, so'ngra ikki bosqichli tasdiqlash (2FA) kodini ichma-ich `if` orqali tekshiring.

## Yechim (PHP kodi):
```php
<?php

$parol_togri = true;
$ikki_bosqichli_kod_togri = true;

if ($parol_togri) {
    echo "Parol tasdiqlandi. 2FA tekshirilmoqda...
";
    if ($ikki_bosqichli_kod_togri) {
        echo "Tizimga muvaffaqiyatli kirdingiz!
";
    } else {
        echo "Xatolik: 2FA kod noto'g'ri!
";
    }
} else {
    echo "Xatolik: Parol noto'g'ri!
";
}

```

## Tushuntirish va Mantiq:
Bitta `if` blokining ichiga yana boshqa `if` larni joylashtirish 'ichma-ich' (nested) shart deb ataladi. U qadam-baqadam tekshirishlar va chuqur shartlar uchun qo'llaniladi.

## Ishlash natijasi:
```text
Parol tasdiqlandi. 2FA tekshirilmoqda...
Tizimga muvaffaqiyatli kirdingiz!
```

# 45-Topshiriq: Ternar operatori (? :) orqali qisqa shart
## Topshiriq sharti:
Foydalanuvchi yoshiga qarab 'Kattalar' yoki 'Bolalar' toifasini ternar operator yordamida o'zgaruvchiga o'zlashtiring.

## Yechim (PHP kodi):
```php
<?php

$yosh = 20;
$toifa = ($yosh >= 18) ? "Kattalar" : "Bolalar";

echo "Toifa: $toifa
";

```

## Tushuntirish va Mantiq:
Ternar operatori uchta qismdan iborat bo'lib, `(shart) ? qiymat1 : qiymat2` ko'rinishida yoziladi. Agar shart rost bo'lsa `qiymat1`, yolg'on bo'lsa `qiymat2` qaytariladi. Bu oddiy `if-else` ning bir qatorli muqobilidir.

## Ishlash natijasi:
```text
Toifa: Kattalar
```

# 46-Topshiriq: Elvis operatori (?: qisqartmasi)
## Topshiriq sharti:
`?:` (Elvis) operatoridan foydalanib, foydalanuvchi nikini tekshiring va agar bo'sh bo'lsa sukut bo'yicha 'Mehmon' qiymatini qaytaring.

## Yechim (PHP kodi):
```php
<?php

$foydalanuvchi_nik = "";
$amaldagi_nik = $foydalanuvchi_nik ?: "Mehmon";

echo "Xush kelibsiz, $amaldagi_nik!
";

$kiritilgan_nik = "Bobur";
echo "Xush kelibsiz, " . ($kiritilgan_nik ?: "Mehmon") . "!
";

```

## Tushuntirish va Mantiq:
Elvis operatori `$a ?: $b` ifodasi `$a ? $a : $b` ning qisqartmasidir. Agar `$a` rost (truthy) bo'lsa uning o'zi, aks holda `$b` qaytariladi. Eslatma: agar `$a` umuman e'lon qilinmagan bo'lsa, bu operator Notice chiqarishi mumkin, shuning uchun o'zgaruvchi yo'qligini tekshirishda `??` afzalroq.

## Ishlash natijasi:
```text
Xush kelibsiz, Mehmon!
Xush kelibsiz, Bobur!
```

# 47-Topshiriq: Null Coalescing operatori (??)
## Topshiriq sharti:
Massivda kalit mavjud emasligi yoki `null` bo'lishi mumkin bo'lgan holatda `??` operatori orqali xavfsiz qiymat olishni namoyish eting.

## Yechim (PHP kodi):
```php
<?php

$sorov = [
    "sahifa" => 2
    // 'tartib' kaliti yo'q
];

$joriy_sahifa = $sorov["sahifa"] ?? 1;
$tartib = $sorov["tartib"] ?? "id_kamayish";

echo "Sahifa: $joriy_sahifa
";
echo "Tartib: $tartib
";

```

## Tushuntirish va Mantiq:
`??` (Null Coalescing) operatori o'zgaruvchi mavjudligini va `null` emasligini tekshiradi (`isset()` ga teng). Agar chap tomondagi qiymat mavjud va null bo'lmasa, uning o'zini, aks holda o'ng tomondagi qiymatni qaytaradi. Hech qanday Warning yoki Notice chiqarmaydi.

## Ishlash natijasi:
```text
Sahifa: 2
Tartib: id_kamayish
```

# 48-Topshiriq: switch-case operatori va break kalit so'zi
## Topshiriq sharti:
Hafta kuni raqamiga (1 dan 7 gacha) qarab kun nomini o'zbek tilida chiqaruvchi `switch-case` dasturini yozing.

## Yechim (PHP kodi):
```php
<?php

$kun_raqami = 3;
$kun_nomi = "";

switch ($kun_raqami) {
    case 1:
        $kun_nomi = "Dushanba";
        break;
    case 2:
        $kun_nomi = "Seshanba";
        break;
    case 3:
        $kun_nomi = "Chorshanba";
        break;
    case 4:
        $kun_nomi = "Payshanba";
        break;
    case 5:
        $kun_nomi = "Juma";
        break;
    case 6:
        $kun_nomi = "Shanba";
        break;
    case 7:
        $kun_nomi = "Yakshanba";
        break;
    default:
        $kun_nomi = "Noma'lum kun";
        break;
}

echo "Hafta kuni: $kun_nomi
";

```

## Tushuntirish va Mantiq:
`switch` operatori ifodani bir nechta `case` qiymatlari bilan solishtiradi. Har bir `case` oxirida `break` qo'yilishi shart, aks holda dastur keyingi `case` larga ham o'tib ketadi (fall-through). Agar birorta `case` to'g'ri kelmasa `default` bloki bajariladi.

## Ishlash natijasi:
```text
Hafta kuni: Chorshanba
```

# 49-Topshiriq: switch operatorida bir nechta case larni guruhlash
## Topshiriq sharti:
Hafta kuniga qarab ish kuni yoki dam olish kuni ekanligini bir nechta `case` larni bitta joyga guruhlab aniqlang.

## Yechim (PHP kodi):
```php
<?php

$kun = "Shanba";

switch ($kun) {
    case "Dushanba":
    case "Seshanba":
    case "Chorshanba":
    case "Payshanba":
    case "Juma":
        echo "$kun - Ish kuni.
";
        break;
    case "Shanba":
    case "Yakshanba":
        echo "$kun - Dam olish kuni!
";
        break;
    default:
        echo "Bunday hafta kuni mavjud emas.
";
        break;
}

```

## Tushuntirish va Mantiq:
Agar bir nechta qiymatlar uchun bir xil harakat bajarilishi kerak bo'lsa, `case` larni ketma-ket yozib, ularning orasiga `break` qo'ymasdan guruhlash mumkin. Bu kod takrorlanishining oldini oladi.

## Ishlash natijasi:
```text
Shanba - Dam olish kuni!
```

# 50-Topshiriq: goto operatori va uning maxsus chegaralangan qo'llanilishi
## Topshiriq sharti:
`goto` operatori orqali chuqur kiritilgan shartdan bevosita belgilangan nishonga (label) sakrashni ko'rsating va uning xavflarini tushuntiring.

## Yechim (PHP kodi):
```php
<?php

$xatolik_aniqlandi = true;

if ($xatolik_aniqlandi) {
    goto xatolikni_tozalash;
}

echo "Bu qator hech qachon bajarilmaydi.
";

xatolikni_tozalash:
echo "Tozalash jarayoni boshlandi: Resurslar yopildi va log yozildi.
";

```

## Tushuntirish va Mantiq:
`goto` operatori dastur oqimini ko'rsatilgan `label:` ga o'tkazadi. Funksiya yoki metoddan tashqariga sakrashga ruxsat berilmaydi. `goto` kodning o'qilishini qiyinlashtirishi (spaghetti code) sababli kamdan-kam holatlarda (masalan, chuqur sikllardan darhol chiqish yoki xatolik tozalash) qo'llanilishi mumkin, lekin umumiy amaliyotda undan tiyilish ma'qul.

## Ishlash natijasi:
```text
Tozalash jarayoni boshlandi: Resurslar yopildi va log yozildi.
```
