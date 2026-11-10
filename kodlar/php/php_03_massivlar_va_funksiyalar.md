# 3-Mavzu: Massivlar (Arrays) va Massiv Funksiyalari (101-150)

Ushbu bo'limda PHP tilining eng muhim va universal ma'lumotlar tuzilmasi bo'lgan massivlar hamda ular ustida amallar to'liq qamrab olingan:
Indekslangan va assotsiativ massivlar, ko'p o'lchamli tuzilmalar, staklar va navbatlar (`array_push`, `array_pop`, `array_shift`, `array_unshift`), aylanish sikllari (`foreach`, `for`, ko'rsatkichlar `current`/`next`/`reset`), havolalar bilan ishlash (`&$ref`), destructuring (`[$a, $b]`), spread operatori (`...$arr`), massivlarni qidirish va saralash (`in_array`, `array_search`, `array_key_exists`, `array_filter`, `array_column`), transformatsiyalar (`array_map`, `array_reduce`, `array_merge`, `array_replace`, `array_slice`, `array_splice`, `array_chunk`, `array_unique`), saralash turlari (`sort`, `asort`, `ksort`, `usort`, `uasort`) hamda to'plamlar ustida amallar (`array_diff`, `array_intersect`, `array_flip`, `array_reverse`, `count`) bo'yicha 50 ta amaliy topshiriq jamlangan.

---

# 101-Topshiriq: Indekslangan massivlar yaratish: array() va []
## Topshiriq sharti:
Eski `array()` konstruksiyasi va zamonaviy qisqa kvadrat qavs `[]` yordamida raqamli indekslangan massivlar yarating.

## Yechim (PHP kodi):
```php
<?php

// Eski sintaksis
$tillar_eski = array("PHP", "JavaScript", "Python");

// Zamonaviy sintaksis (tavsiya etiladi)
$tillar_yangi = ["PHP", "JavaScript", "Python"];

echo "Birinchi element: " . $tillar_yangi[0] . "
";
echo "Ikkinchi element: " . $tillar_yangi[1] . "
";
echo "Uchinchi element: " . $tillar_yangi[2] . "
";

```

## Tushuntirish va Mantiq:
PHP 5.4 versiyasidan boshlab kiritilgan qisqa massiv sintaksisi `[]` bugungi kunda barcha zamonaviy loyihalarda standart hisoblanadi. Indekslar sukut bo'yicha `0` dan boshlanadi.

## Ishlash natijasi:
```text
Birinchi element: PHP
Ikkinchi element: JavaScript
Uchinchi element: Python
```

# 102-Topshiriq: Massiv elementlariga murojaat va ularni indeks bo'yicha yangilash
## Topshiriq sharti:
Massiv elementining qiymatini indeks orqali qayta tayinlang va natijani ekranga chiqaring.

## Yechim (PHP kodi):
```php
<?php

$shaharlar = ["Samarqand", "Buxoro", "Toshkent"];

echo "Yangilashdan oldin: " . $shaharlar[1] . "
";

// Buxoroni Xivaga almashtiramiz
$shaharlar[1] = "Xiva";

echo "Yangilashdan so'ng: " . $shaharlar[1] . "
";

```

## Tushuntirish va Mantiq:
Massiv elementining qiymatini o'zgartirish uchun uning indeksi kvadrat qavs ichida ko'rsatiladi: `$massiv[$indeks] = $yangi_qiymat`.

## Ishlash natijasi:
```text
Yangilashdan oldin: Buxoro
Yangilashdan so'ng: Xiva
```

# 103-Topshiriq: Massiv oxiriga element qo'shish: $massiv[] = qiymat
## Topshiriq sharti:
Kvadrat qavs `[]` operatori orqali yangi elementlarni massiv oxiriga dinamik qo'shing.

## Yechim (PHP kodi):
```php
<?php

$xaridlar = ["Non", "Sut"];

$xaridlar[] = "Tuxum";
$xaridlar[] = "Choy";

foreach ($xaridlar as $indeks => $mahsulot) {
    echo "[$indeks] => $mahsulot
";
}

```

## Tushuntirish va Mantiq:
`$massiv[] = $qiymat` ifodasi massivdagi eng katta butun son indeksidan keyingi keyingi bo'sh indeksga yangi elementni biriktiradi. Bu PHP da bitta element qo'shishning eng tezkor usulidir.

## Ishlash natijasi:
```text
[0] => Non
[1] => Sut
[2] => Tuxum
[3] => Choy
```

# 104-Topshiriq: array_push() yordamida bir vaqtda bir nechta element qo'shish
## Topshiriq sharti:
`array_push()` funksiyasidan foydalanib massiv oxiriga bir nechta ma'lumotlarni birdaniga joylashtiring.

## Yechim (PHP kodi):
```php
<?php

$serverlar = ["srv-01", "srv-02"];

$yangi_hajm = array_push($serverlar, "srv-03", "srv-04", "srv-05");

echo "Yangi hajm: $yangi_hajm dona element
";
echo "Oxirgi server: " . $serverlar[count($serverlar) - 1] . "
";

```

## Tushuntirish va Mantiq:
`array_push(&$massiv, ...$qiymatlar)` bir nechta qiymatlarni bitta chaqiriqda massiv oxiriga qo'shadi va yangilangan massivdagi umumiy elementlar sonini qaytaradi.

## Ishlash natijasi:
```text
Yangi hajm: 5 dona element
Oxirgi server: srv-05
```

# 105-Topshiriq: array_pop() orqali oxirgi elementni sug'urib olish
## Topshiriq sharti:
Navbat yoki stek (LIFO - Last In First Out) prinsipi bo'yicha oxirgi kiritilgan elementni o'chirib oling.

## Yechim (PHP kodi):
```php
<?php

$tarix = ["sahifa_1", "sahifa_2", "sahifa_3"];

$oxirgi_sahifa = array_pop($tarix);

echo "Ko'rilgan oxirgi sahifa: $oxirgi_sahifa
";
echo "Qolgan sahifalar soni: " . count($tarix) . "
";

```

## Tushuntirish va Mantiq:
`array_pop(&$massiv)` massivning eng oxirgi elementini qirqib oladi va uni qaytaradi. Massiv uzunligi 1 taga qisqaradi.

## Ishlash natijasi:
```text
Ko'rilgan oxirgi sahifa: sahifa_3
Qolgan sahifalar soni: 2
```

# 106-Topshiriq: array_unshift() orqali massiv boshiga element qo'shish
## Topshiriq sharti:
VIP mijozni navbatning eng boshiga `array_unshift()` orqali kiritishni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

$navbat = ["Mijoz A", "Mijoz B"];

array_unshift($navbat, "VIP Mijoz X");

foreach ($navbat as $orrin => $mijoz) {
    echo "$orrin: $mijoz
";
}

```

## Tushuntirish va Mantiq:
`array_unshift(&$massiv, ...$qiymatlar)` yangi elementlarni massiv boshiga qo'shadi va mavjud raqamli indekslarni avtomatik ravishda 0 dan boshlab qayta tartiblaydi.

## Ishlash natijasi:
```text
0: VIP Mijoz X
1: Mijoz A
2: Mijoz B
```

# 107-Topshiriq: array_shift() orqali massiv boshidagi elementni sug'urib olish
## Topshiriq sharti:
FIFO (First In First Out) navbat tizimini `array_shift()` orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

$buyurtmalar = ["ORD-001", "ORD-002", "ORD-003"];

$bajariladigan = array_shift($buyurtmalar);

echo "Hozir bajarilayotgan: $bajariladigan
";
echo "Keyingi navbatdagi: " . $buyurtmalar[0] . "
";

```

## Tushuntirish va Mantiq:
`array_shift(&$massiv)` massiv boshidagi birinchi elementni olib tashlaydi va uni qaytaradi. Qolgan raqamli indekslar oldinga bir pog'ona suriladi.

## Ishlash natijasi:
```text
Hozir bajarilayotgan: ORD-001
Keyingi navbatdagi: ORD-002
```

# 108-Topshiriq: Assotsiativ massivlar (kalit => qiymat)
## Topshiriq sharti:
Foydalanuvchi ma'lumotlarini (ism, email, lavozim) saqlaydigan assotsiativ massiv tuzing.

## Yechim (PHP kodi):
```php
<?php

$xodim = [
    "ism" => "Otabek",
    "email" => "otabek@khorazmiy.uz",
    "lavozim" => "Lead Backend Muhandis",
    "staj_yil" => 5
];

echo "Xodim ismi: " . $xodim["ism"] . "
";
echo "Lavozimi: " . $xodim["lavozim"] . "
";
echo "Tajribasi: " . $xodim["staj_yil"] . " yil
";

```

## Tushuntirish va Mantiq:
Assotsiativ massivlarda indekslar o'rniga nomli satr kalitlar (`key => value`) ishlatiladi. Bu ma'lumotlar strukturasini aniq va tushunarli ifodalash imkonini beradi.

## Ishlash natijasi:
```text
Xodim ismi: Otabek
Lavozimi: Lead Backend Muhandis
Tajribasi: 5 yil
```

# 109-Topshiriq: Ko'p o'lchamli massivlar (Multi-dimensional arrays)
## Topshiriq sharti:
Bir nechta talabalarning baholari va fanlarini ko'p o'lchamli massivda ifodalang.

## Yechim (PHP kodi):
```php
<?php

$talabalar = [
    [
        "ism" => "Jamshid",
        "fanlar" => ["Matematika" => 90, "Fizika" => 85]
    ],
    [
        "ism" => "Shahnoza",
        "fanlar" => ["Matematika" => 98, "Fizika" => 92]
    ]
];

echo $talabalar[0]["ism"] . "ning Matematika bali: " . $talabalar[0]["fanlar"]["Matematika"] . "
";
echo $talabalar[1]["ism"] . "ning Matematika bali: " . $talabalar[1]["fanlar"]["Matematika"] . "
";

```

## Tushuntirish va Mantiq:
Ko'p o'lchamli massiv - bu boshqa massivlarni o'z ichiga olgan massivdir. Chuqur elementlarga ketma-ket qavslar orqali murojaat qilinadi: `$massiv[0]['fanlar']['Matematika']`.

## Ishlash natijasi:
```text
Jamshidning Matematika bali: 90
Shahnozaning Matematika bali: 98
```

# 110-Topshiriq: unset() orqali elementni o'chirish va array_values() bilan qayta indekslash
## Topshiriq sharti:
Massivdan elementni `unset()` orqali o'chiring va indekslar uzilishini `array_values()` orqali to'g'irlang.

## Yechim (PHP kodi):
```php
<?php

$raqamlar = ["A", "B", "C", "D"];

unset($raqamlar[1]); // "B" o'chirildi. Indekslar: 0, 2, 3 bo'lib qoladi!

echo "unset dan so'ng indekslar:
";
foreach ($raqamlar as $k => $v) {
    echo "  $k => $v
";
}

$qayta_indekslangan = array_values($raqamlar);

echo "array_values dan so'ng:
";
foreach ($qayta_indekslangan as $k => $v) {
    echo "  $k => $v
";
}

```

## Tushuntirish va Mantiq:
`unset($massiv[$indeks])` elementni massivdan olib tashlaydi, biroq qolgan indekslar siljimaydi. Qolgan elementlarni 0 dan boshlab uzluksiz raqamlab chiqish uchun `array_values()` funksiyasi ishlatiladi.

## Ishlash natijasi:
```text
unset dan so'ng indekslar:
  0 => A
  2 => C
  3 => D
array_values dan so'ng:
  0 => A
  1 => C
  2 => D
```

# 111-Topshiriq: foreach orqali massiv qiymatlarini aylanish
## Topshiriq sharti:
`foreach ($massiv as $qiymat)` sintaksisi yordamida shahar nomlarini konsolga chiqaring.

## Yechim (PHP kodi):
```php
<?php

$shaharlar = ["Samarqand", "Buxoro", "Xiva", "Andijon"];

foreach ($shaharlar as $shahar) {
    echo "Shahar: $shahar
";
}

```

## Tushuntirish va Mantiq:
`foreach` sikli massivlar bilan ishlash uchun eng qulay va xavfsiz konstruksiya hisoblanadi. U massiv boshidan oxirigacha har bir elementni o'zgaruvchiga olib sikl tanasini bajaradi.

## Ishlash natijasi:
```text
Shahar: Samarqand
Shahar: Buxoro
Shahar: Xiva
Shahar: Andijon
```

# 112-Topshiriq: foreach orqali kalit va qiymatlarni birgalikda o'qish
## Topshiriq sharti:
`foreach ($massiv as $kalit => $qiymat)` orqali konfiguratsiya sozlamalarini chop eting.

## Yechim (PHP kodi):
```php
<?php

$konfig = [
    "app_env" => "production",
    "app_debug" => "false",
    "db_connection" => "pgsql"
];

foreach ($konfig as $kalit => $qiymat) {
    echo "$kalit = $qiymat
";
}

```

## Tushuntirish va Mantiq:
`$kalit => $qiymat` sintaksisi joriy elementning indeksini (yoki satr kalitini) `$kalit` o'zgaruvchisiga, uning qiymatini esa `$qiymat` o'zgaruvchisiga o'zlashtiradi.

## Ishlash natijasi:
```text
app_env = production
app_debug = false
db_connection = pgsql
```

# 113-Topshiriq: foreach da havola (&) orqali qiymatlarni joyida o'zgartirish va unset
## Topshiriq sharti:
Massivdagi barcha narxlarni `&$narx` havolasi orqali 15% ga oshiring va xavfsiz `unset` qiling.

## Yechim (PHP kodi):
```php
<?php

$narxlar = [10000, 20000, 30000];

foreach ($narxlar as &$narx) {
    $narx = (int)($narx * 1.15);
}
unset($narx); // Muhim: havolani uzish shart!

print_r($narxlar);

```

## Tushuntirish va Mantiq:
`&$narx` belgisidagi ampersand (`&`) parametrni havola (reference) bo'yicha oladi, ya'ni sikl ichidagi o'zgarish bevosita massivning o'ziga ta'sir qiladi. Sikldan so'ng `unset($narx)` chaqirish juda muhim, aks holda oxirgi element keyingi kodlarda tasodifan buzilishi mumkin.

## Ishlash natijasi:
```text
Array
(
    [0] => 11500
    [1] => 23000
    [2] => 34500
)
```

# 114-Topshiriq: for sikli orqali indekslangan massivlarni aylanish
## Topshiriq sharti:
`for ($i = 0; $i < $count; $i++)` sikli orqali massiv elementlarini indekslari bilan chiqaring.

## Yechim (PHP kodi):
```php
<?php

$hafta_kunlari = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma"];
$soni = count($hafta_kunlari);

for ($i = 0; $i < $soni; $i++) {
    echo ($i + 1) . "-kun: " . $hafta_kunlari[$i] . "
";
}

```

## Tushuntirish va Mantiq:
`for` sikli raqamli indekslari 0 dan boshlanib uzluksiz ketgan massivlarni indekslari bo'yicha to'liq nazorat qilish imkonini beradi. Har bir qadamda `count()` ni qayta chaqirmaslik uchun uning qiymatini oldindan o'zgaruvchiga olib qo'yish yaxshi amaliyotdir.

## Ishlash natijasi:
```text
1-kun: Dushanba
2-kun: Seshanba
3-kun: Chorshanba
4-kun: Payshanba
5-kun: Juma
```

# 115-Topshiriq: current(), next(), prev(), reset(), end() ko'rsatkichlari
## Topshiriq sharti:
Massivning ichki ko'rsatkichlarini boshqaruvchi standart funksiyalardan foydalaning.

## Yechim (PHP kodi):
```php
<?php

$kurslar = ["Frontend", "Backend", "Mobile", "DevOps"];

echo "Hozirgi: " . current($kurslar) . "
"; // Frontend
echo "Keyingi: " . next($kurslar) . "
";    // Backend
echo "Eng oxirgi: " . end($kurslar) . "
";  // DevOps
echo "Oldingi: " . prev($kurslar) . "
";    // Mobile
echo "Boshiga qaytish: " . reset($kurslar) . "
"; // Frontend

```

## Tushuntirish va Mantiq:
PHP massivlari ichki ko'rsatkichga (internal pointer) ega. `current()` joriy elementni, `next()` ko'rsatkichni bir qadam oldinga surib qiymatini, `prev()` bir qadam orqaga, `end()` oxiriga, `reset()` esa boshiga ko'chiradi.

## Ishlash natijasi:
```text
Hozirgi: Frontend
Keyingi: Backend
Eng oxirgi: DevOps
Oldingi: Mobile
Boshiga qaytish: Frontend
```

# 116-Topshiriq: array_walk() orqali elementlarni joyida qayta ishlash
## Topshiriq sharti:
`array_walk()` yordamida massivdagi barcha satrlarni katta harflarga aylantiring.

## Yechim (PHP kodi):
```php
<?php

$xodimlar = ["alisher", "bobur", "nodira"];

array_walk($xodimlar, function (&$ism, $indeks) {
    $ism = ucfirst($ism);
});

print_r($xodimlar);

```

## Tushuntirish va Mantiq:
`array_walk(&$massiv, $callback)` massivning har bir elementiga berilgan funksiyani qo'llaydi. Callback funksiyasida birinchi argument havola (`&$ism`) qilib olinsa, o'zgarishlar asl massivda saqlanadi.

## Ishlash natijasi:
```text
Array
(
    [0] => Alisher
    [1] => Bobur
    [2] => Nodira
)
```

# 117-Topshiriq: array_walk_recursive() orqali chuqur massivlarni qayta ishlash
## Topshiriq sharti:
Chuqur kiritilgan bo'limlar va toifalar massividagi barcha qiymatlarni `array_walk_recursive()` orqali tozalang.

## Yechim (PHP kodi):
```php
<?php

$katalog = [
    "Elektronika" => [
        "Smartfonlar" => "  Apple iPhone ",
        "Noutbuklar" => "  Dell XPS  "
    ],
    "Kiyim" => " Kurtka "
];

array_walk_recursive($katalog, function (&$qiymat) {
    $qiymat = trim($qiymat);
});

print_r($katalog);

```

## Tushuntirish va Mantiq:
`array_walk_recursive()` ko'p o'lchamli massivlarning barcha ichki tarmoqlariga kirib, faqatgina haqiqiy barg elementlariga (skalyar qiymatlarga) funksiyani qo'llaydi.

## Ishlash natijasi:
```text
Array
(
    [Elektronika] => Array
        (
            [Smartfonlar] => Apple iPhone
            [Noutbuklar] => Dell XPS
        )

    [Kiyim] => Kurtka
)
```

# 118-Topshiriq: Massiv destructuring: [$a, $b] = $massiv
## Topshiriq sharti:
Massiv elementlarini alohida o'zgaruvchilarga qisqa destrukturizatsiya sintaksisi orqali ajrating.

## Yechim (PHP kodi):
```php
<?php

$nuqta = [10, 25];

[$x, $y] = $nuqta;

echo "X koordinatasi: $x
";
echo "Y koordinatasi: $y
";

// Ikki o'zgaruvchining o'rnini almashtirish (swap)
[$x, $y] = [$y, $x];
echo "Almashgandan so'ng: X = $x, Y = $y
";

```

## Tushuntirish va Mantiq:
PHP 7.1 dan boshlab `[$a, $b] = $massiv` sintaksisi kiritilgan (eski `list($a, $b)` o'rniga). Bu orqali massiv elementlarini juda qisqa va qulay tarzda o'zgaruvchilarga ochib olish mumkin.

## Ishlash natijasi:
```text
X koordinatasi: 10
Y koordinatasi: 25
Almashgandan so'ng: X = 25, Y = 10
```

# 119-Topshiriq: Assotsiativ massiv destructuring
## Topshiriq sharti:
Assotsiativ massivdan aniq kalitlarni ularning nomi bo'yicha destrukturizatsiya qiling.

## Yechim (PHP kodi):
```php
<?php

$foydalanuvchi = [
    "id" => 402,
    "ism" => "Mansur",
    "rol" => "Admin"
];

["ism" => $ism, "rol" => $rol] = $foydalanuvchi;

echo "Foydalanuvchi: $ism, Roli: $rol
";

```

## Tushuntirish va Mantiq:
Assotsiativ massivlarda `['kalit' => $o'zgaruvchi]` shaklida destrukturizatsiya qilib, faqat kerakli maydonlarni ajratib olish mumkin.

## Ishlash natijasi:
```text
Foydalanuvchi: Mansur, Roli: Admin
```

# 120-Topshiriq: Massivlar uchun splat operatori (...$massiv unpacking)
## Topshiriq sharti:
PHP 7.4 da kiritilgan `...` (spread operator) yordamida massivlarni birlashtirish va nusxalashni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

$sonlar1 = [1, 2, 3];
$sonlar2 = [4, 5, 6];

$birlashtirilgan = [...$sonlar1, 99, ...$sonlar2];

print_r($birlashtirilgan);

```

## Tushuntirish va Mantiq:
`...$massiv` (array unpacking) massiv elementlarini alohida ochib beradi. U `array_merge()` ga nisbatan tezroq ishlaydi va sintaktik jihatdan juda ixchamdir. PHP 8.1 dan boshlab assotsiativ massivlarni ham unpacking qilish qo'llab-quvvatlanadi.

## Ishlash natijasi:
```text
Array
(
    [0] => 1
    [1] => 2
    [2] => 3
    [3] => 99
    [4] => 4
    [5] => 5
    [6] => 6
)
```

# 121-Topshiriq: in_array() orqali qiymat mavjudligini qat'iy tekshirish
## Topshiriq sharti:
`in_array()` funksiyasida uchinchi `$strict` parametrining o'rni va xavfsizligini isbotlang.

## Yechim (PHP kodi):
```php
<?php

$ruxsatlar = ["1", "2", "3"];

// Qat'iy bo'lmagan tekshiruv (xavfli):
echo "Qat'iysiz tekshiruv (0 == 'ruxsat'): " . (in_array(0, ["ruxsat_yoq"], false) ? "Mavjud deb topdi!" : "Topilmadi") . "
";

// Qat'iy tekshiruv (strict: true):
if (in_array(2, [1, 2, 3], true)) {
    echo "Raqam qat'iy mos keldi.
";
}

```

## Tushuntirish va Mantiq:
`in_array($qidiruv, $massiv, $strict)` uchinchi parametri `true` qilib berilmasa, u `==` kabi tiplarni avtomatik o'zgartiradi va jiddiy mantiqiy xatolar keltirib chiqarishi mumkin. Shuning uchun har doim `true` (strict) berish tavsiya etiladi.

## Ishlash natijasi:
```text
Qat'iysiz tekshiruv (0 == 'ruxsat'): Mavjud deb topdi!
Raqam qat'iy mos keldi.
```

# 122-Topshiriq: array_search() yordamida qiymatning kalitini topish
## Topshiriq sharti:
Foydalanuvchi roli massiv ichida nechanchi o'rinda yoki qaysi kalit ostida ekanligini `array_search()` bilan aniqlang.

## Yechim (PHP kodi):
```php
<?php

$rollar = [
    "user" => "Oddiy foydalanuvchi",
    "editor" => "Muharrir",
    "admin" => "Administrator"
];

$topilgan_kalit = array_search("Muharrir", $rollar, true);

if ($topilgan_kalit !== false) {
    echo "'Muharrir' roli kaliti: $topilgan_kalit
";
} else {
    echo "Topilmadi.
";
}

```

## Tushuntirish va Mantiq:
`array_search()` qidirilayotgan qiymat birinchi uchragan kalitni (indeksni) qaytaradi. Agar topilmasa `false` qaytaradi. Indeks `0` bo'lishi mumkinligi sababli tekshirishda `!== false` ishlatiladi.

## Ishlash natijasi:
```text
'Muharrir' roli kaliti: editor
```

# 123-Topshiriq: array_key_exists() vs isset(): null qiymatlardagi farqi
## Topshiriq sharti:
Massivda kalit mavjud, lekin qiymati `null` bo'lgan holatda `array_key_exists()` va `isset()` funksiyalarining natijalarini solishtiring.

## Yechim (PHP kodi):
```php
<?php

$sozlamalar = [
    "kripto_kalit" => null,
    "port" => 8080
];

echo "isset('kripto_kalit'): " . (isset($sozlamalar["kripto_kalit"]) ? "Mavjud" : "Mavjud emas (null bo'lgani uchun)") . "
";
echo "array_key_exists('kripto_kalit'): " . (array_key_exists("kripto_kalit", $sozlamalar) ? "Kalit mavjud!" : "Kalit yo'q") . "
";

```

## Tushuntirish va Mantiq:
`isset()` agar kalit mavjud bo'lsa ham uning qiymati `null` bo'lsa `false` qaytaradi. `array_key_exists()` esa qiymat nima bo'lishidan qat'i nazar (hatto `null` bo'lsa ham) kalitning mavjudligini aniqlaydi.

## Ishlash natijasi:
```text
isset('kripto_kalit'): Mavjud emas (null bo'lgani uchun)
array_key_exists('kripto_kalit'): Kalit mavjud!
```

# 124-Topshiriq: array_keys() orqali barcha kalitlarni ajratib olish
## Topshiriq sharti:
Assotsiativ massivdagi barcha maydon nomlarini `array_keys()` orqali ajratib oling.

## Yechim (PHP kodi):
```php
<?php

$foydalanuvchi = [
    "ism" => "Farrux",
    "familiya" => "Aliyev",
    "yosh" => 29,
    "mamlakat" => "O'zbekiston"
];

$maydonlar = array_keys($foydalanuvchi);

echo "Maydonlar: " . implode(", ", $maydonlar) . "
";

```

## Tushuntirish va Mantiq:
`array_keys($massiv)` barcha kalitlarni raqamli indekslangan yangi massiv sifatida qaytaradi. Shuningdek, ma'lum bir qiymatga ega bo'lgan kalitlarni filtrlash uchun ikkinchi parametrni ham qabul qiladi.

## Ishlash natijasi:
```text
Maydonlar: ism, familiya, yosh, mamlakat
```

# 125-Topshiriq: array_values() orqali faqat qiymatlarni raqamli indekslarga yig'ish
## Topshiriq sharti:
Assotsiativ massiv kalitlarini tashlab yuborib, faqat uning qiymatlarini `array_values()` orqali oling.

## Yechim (PHP kodi):
```php
<?php

$narxlar = [
    "olma" => 12000,
    "anor" => 25000,
    "uzum" => 18000
];

$faqat_narxlar = array_values($narxlar);

print_r($faqat_narxlar);

```

## Tushuntirish va Mantiq:
`array_values()` massivning barcha qiymatlarini ajratib olib, ularni 0 dan boshlab qayta tartiblangan yangi massivga joylaydi.

## Ishlash natijasi:
```text
Array
(
    [0] => 12000
    [1] => 25000
    [2] => 18000
)
```

# 126-Topshiriq: array_filter() yordamida massivni shart bo'yicha saralash
## Topshiriq sharti:
Talabalar baholari orasidan faqat 80 dan yuqori bo'lganlarini `array_filter()` orqali ajrating.

## Yechim (PHP kodi):
```php
<?php

$baholar = [65, 82, 90, 45, 78, 95];

$a_baholar = array_filter($baholar, fn(int $ball) => $ball >= 80);

print_r(array_values($a_baholar));

```

## Tushuntirish va Mantiq:
`array_filter($massiv, $callback)` callback funksiyasi `true` qaytargan elementlarni saqlab qoladi, `false` qaytarganlarini esa o'chiradi. Kalitlarni saqlab qoladi, shuning uchun uzluksiz indekslar uchun `array_values()` bilan birga ishlatiladi.

## Ishlash natijasi:
```text
Array
(
    [0] => 82
    [1] => 90
    [2] => 95
)
```

# 127-Topshiriq: array_filter() bo'sh qiymatlarni avtomatik tozalashi
## Topshiriq sharti:
`array_filter()` ga hech qanday callback bermasdan massivdagi barcha soxta (falsy: null, 0, false, '') qiymatlarni tozalang.

## Yechim (PHP kodi):
```php
<?php

$kiruvchi_malumotlar = ["Ali", "", null, false, 0, "Vali", " "];

$tozalangan = array_filter($kiruvchi_malumotlar);

print_r(array_values($tozalangan));

```

## Tushuntirish va Mantiq:
Agar `array_filter()` ga ikkinchi argument uzatilmasa, u sukut bo'yicha `(bool)$element == false` bo'lgan barcha qiymatlarni (null, 0, '', false, []) avtomatik ravishda tozalab tashlaydi.

## Ishlash natijasi:
```text
Array
(
    [0] => Ali
    [1] => Vali
    [2] =>  
)
```

# 128-Topshiriq: array_column() orqali ko'p o'lchamli massivdan bitta ustunni ajratish
## Topshiriq sharti:
Ma'lumotlar bazasidan kelgan foydalanuvchilar ro'yxatidan faqat ularning email manzillarini `array_column()` orqali bitta massivga oling.

## Yechim (PHP kodi):
```php
<?php

$foydalanuvchilar = [
    ["id" => 1, "ism" => "Sanjar", "email" => "sanjar@uz.uz"],
    ["id" => 2, "ism" => "Kamola", "email" => "kamola@uz.uz"],
    ["id" => 3, "ism" => "Timur", "email" => "timur@uz.uz"]
];

$emaillar = array_column($foydalanuvchilar, "email");

print_r($emaillar);

```

## Tushuntirish va Mantiq:
`array_column($massiv, $ustun_nomi)` massivdagi har bir qator ichidan ko'rsatilgan ustun qiymatlarini sug'urib olib, bir o'lchamli qulay massiv yaratadi.

## Ishlash natijasi:
```text
Array
(
    [0] => sanjar@uz.uz
    [1] => kamola@uz.uz
    [2] => timur@uz.uz
)
```

# 129-Topshiriq: array_column() da uchinchi parametr: indeks kalitini belgilash
## Topshiriq sharti:
`array_column()` ning uchinchi parametri orqali yangi massivning indekslari sifatida `id` ustunini belgilang.

## Yechim (PHP kodi):
```php
<?php

$mahsulotlar = [
    ["id" => 101, "nom" => "Smartfon", "narx" => 300],
    ["id" => 205, "nom" => "Planshet", "narx" => 450]
];

$id_boyicha_nomlar = array_column($mahsulotlar, "nom", "id");

print_r($id_boyicha_nomlar);

```

## Tushuntirish va Mantiq:
`array_column($massiv, $ustun, $indeks_ustuni)` uchinchi parametri orqali hosil bo'ladigan yangi massiv kalitlarini boshqa bir ustun (masalan birlamchi kalit `id`) qiymatiga bog'lash mumkin.

## Ishlash natijasi:
```text
Array
(
    [101] => Smartfon
    [205] => Planshet
)
```

# 130-Topshiriq: array_key_first() va array_key_last() funksiyalari
## Topshiriq sharti:
PHP 7.3 da kiritilgan `array_key_first()` va `array_key_last()` yordamida massivning birinchi va oxirgi kalitlarini aniqlang.

## Yechim (PHP kodi):
```php
<?php

$jadval = [
    "birinchi_bob" => "Kirish",
    "ikkinchi_bob" => "Asosiy qism",
    "oxirgi_bob" => "Xulosa"
];

echo "Birinchi kalit: " . array_key_first($jadval) . "
";
echo "Oxirgi kalit: " . array_key_last($jadval) . "
";

```

## Tushuntirish va Mantiq:
`array_key_first()` va `array_key_last()` funksiyalari massivning ichki ko'rsatkichini buzmasdan to'g'ridan-to'g'ri birinchi va oxirgi kalitlarini qaytaradi.

## Ishlash natijasi:
```text
Birinchi kalit: birinchi_bob
Oxirgi kalit: oxirgi_bob
```

# 131-Topshiriq: array_map() orqali massiv elementlariga funksiya qo'llash
## Topshiriq sharti:
Massivdagi har bir sonning kvadratini `array_map()` orqali hisoblang.

## Yechim (PHP kodi):
```php
<?php

$sonlar = [1, 2, 3, 4, 5];

$kvadratlar = array_map(fn(int $n) => $n * $n, $sonlar);

print_r($kvadratlar);

```

## Tushuntirish va Mantiq:
`array_map($callback, $massiv)` berilgan funksiyani massivning har bir elementiga qo'llaydi va yangi o'zgargan massivni qaytaradi. Asl massiv o'zgarmaydi.

## Ishlash natijasi:
```text
Array
(
    [0] => 1
    [1] => 4
    [2] => 9
    [3] => 16
    [4] => 25
)
```

# 132-Topshiriq: Bir nechta massivlarni parallel array_map() qilish
## Topshiriq sharti:
Ikkita alohida massivdagi ismlar va familiyalarni `array_map()` yordamida juftlab bitta massivga aylantiring.

## Yechim (PHP kodi):
```php
<?php

$ismlar = ["Anvar", "Zuhra"];
$familiyalar = ["Qodirov", "Ergasheva"];

$toliq = array_map(fn($ism, $fam) => "$ism $fam", $ismlar, $familiyalar);

print_r($toliq);

```

## Tushuntirish va Mantiq:
`array_map()` bir vaqtning o'zida bir nechta massivlarni qabul qila oladi. Funksiya har bir massivdan mos indeksdagi elementlarni parallel ravishda qabul qiladi.

## Ishlash natijasi:
```text
Array
(
    [0] => Anvar Qodirov
    [1] => Zuhra Ergasheva
)
```

# 133-Topshiriq: array_reduce() yordamida massivni bitta qiymatga keltirish
## Topshiriq sharti:
Xarid qilingan mahsulotlarning umumiy narxini `array_reduce()` yordamida bitta umumiy summaga yig'ing.

## Yechim (PHP kodi):
```php
<?php

$savatcha = [
    ["nom" => "Kitob", "narx" => 40000],
    ["nom" => "Daftar", "narx" => 10000],
    ["nom" => "Ruchka", "narx" => 5000]
];

$jami = array_reduce($savatcha, function ($yigindi, $mahsulot) {
    return $yigindi + $mahsulot["narx"];
}, 0);

echo "Savatchaning umumiy summasi: $jami so'm
";

```

## Tushuntirish va Mantiq:
`array_reduce($massiv, $callback, $boshlangich_qiymat)` massiv elementlarini qadam-baqadam yagona qiymatga (akkumulyator) yig'adi. Boshlang'ich qiymat (masalan, 0) uchinchi argumentda beriladi.

## Ishlash natijasi:
```text
Savatchaning umumiy summasi: 55000 so'm
```

# 134-Topshiriq: array_merge() va massiv qo'shish (+) operatori farqi
## Topshiriq sharti:
`array_merge()` va `+` (union) operatorlarining raqamli hamda satrli kalitlarni qanday birlashtirishini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

$m1 = ["a" => 1, "b" => 2, 0 => "PHP"];
$m2 = ["b" => 99, "c" => 4, 0 => "Go"];

// array_merge: satr kalitlarni ustidan yozadi, raqamli kalitlarni esa qayta indekslaydi
$birlashma = array_merge($m1, $m2);

// + operatori: chap tomondagi mavjud kalitlarni saqlaydi, o'ngdagilarni qabul qilmaydi
$union = $m1 + $m2;

echo "--- array_merge ---
";
print_r($birlashma);

echo "--- + operatori ---
";
print_r($union);

```

## Tushuntirish va Mantiq:
`array_merge()` bir xil satr kalitlar bo'lsa oxirgisini yozadi, raqamli kalitlarni esa qayta nomerlaydi. `+` operatori esa chapdagi kalitlarni qat'iy saqlab qoladi va o'ng tomondagi mavjud kalitlarni inkor qiladi.

## Ishlash natijasi:
```text
--- array_merge ---
Array
(
    [a] => 1
    [b] => 99
    [0] => PHP
    [c] => 4
    [1] => Go
)
--- + operatori ---
Array
(
    [a] => 1
    [b] => 2
    [0] => PHP
    [c] => 4
)
```

# 135-Topshiriq: array_merge_recursive() orqali chuqur birlashtirish
## Topshiriq sharti:
Ikkita konfiguratsiya massividagi ichki parametrlarni `array_merge_recursive()` orqali birlashtiring.

## Yechim (PHP kodi):
```php
<?php

$birlamchi = ["db" => ["host" => "localhost", "port" => 3306]];
$qoshimcha = ["db" => ["user" => "root", "port" => 3307]];

$natija = array_merge_recursive($birlamchi, $qoshimcha);

print_r($natija);

```

## Tushuntirish va Mantiq:
`array_merge_recursive()` agar ikkala massivda bir xil kalitlar bo'lsa, ularni ustidan yozmasdan, o'sha kalit ichida yangi kichik massiv hosil qilib ikkala qiymatni ham saqlaydi.

## Ishlash natijasi:
```text
Array
(
    [db] => Array
        (
            [host] => localhost
            [port] => Array
                (
                    [0] => 3306
                    [1] => 3307
                )

            [user] => root
        )

)
```

# 136-Topshiriq: array_replace() orqali sukut bo'yicha qiymatlarni almashtirish
## Topshiriq sharti:
Birlamchi parametrlar ustiga foydalanuvchi tanlagan parametrlarni `array_replace()` orqali yozing.

## Yechim (PHP kodi):
```php
<?php

$default_sozlamalar = [
    "mavzu" => "oq",
    "shrift" => "Roboto",
    "bildirishnomalar" => true
];

$foydalanuvchi_sozlamalari = [
    "mavzu" => "qorong'i",
    "bildirishnomalar" => false
];

$yakuniy = array_replace($default_sozlamalar, $foydalanuvchi_sozlamalari);

print_r($yakuniy);

```

## Tushuntirish va Mantiq:
`array_replace()` keyingi massivdagi elementlar bilan oldingi massiv elementlarining ustidan yozadi. Bu dastur parametrlarini (options) birlashtirishda eng ideal vositadir.

## Ishlash natijasi:
```text
Array
(
    [mavzu] => qorong'i
    [shrift] => Roboto
    [bildirishnomalar] => 
)
```

# 137-Topshiriq: array_slice() orqali massivdan qism ajratish
## Topshiriq sharti:
Massivdan 2-indeksdan boshlab 3 ta elementni `array_slice()` orqali qirqib oling.

## Yechim (PHP kodi):
```php
<?php

$alifbo = ["A", "B", "C", "D", "E", "F", "G"];

$qism = array_slice($alifbo, 2, 3);

print_r($qism);

```

## Tushuntirish va Mantiq:
`array_slice($massiv, $boshlanish, $uzunlik, $preserve_keys)` massivdan ko'rsatilgan oraliqdagi elementlarni ajratib oladi va yangi massiv sifatida qaytaradi. Asl massivga tegilmaydi.

## Ishlash natijasi:
```text
Array
(
    [0] => C
    [1] => D
    [2] => E
)
```

# 138-Topshiriq: array_splice() orqali massivni joyida o'zgartirish va almashtirish
## Topshiriq sharti:
Massivdagi ma'lum elementlarni o'chirib, o'rniga yangi elementlar kiritishni `array_splice()` orqali bajaring.

## Yechim (PHP kodi):
```php
<?php

$ranglar = ["qizil", "yashil", "ko'k", "sariq"];

// 1-indeksdan boshlab 2 ta elementni o'chirib, o'rniga "binafsha" ni qo'yamiz
$ochirilganlar = array_splice($ranglar, 1, 2, ["binafsha"]);

echo "Qolgan massiv:
";
print_r($ranglar);

echo "O'chirilganlar:
";
print_r($ochirilganlar);

```

## Tushuntirish va Mantiq:
`array_splice(&$massiv, $offset, $length, $replacement)` asl massivning o'zini joyida o'zgartiradi. U elementlarni o'chiradi va ixtiyoriy ravishda yangilarini joylashtiradi.

## Ishlash natijasi:
```text
Qolgan massiv:
Array
(
    [0] => qizil
    [1] => binafsha
    [2] => sariq
)
O'chirilganlar:
Array
(
    [0] => yashil
    [1] => ko'k
)
```

# 139-Topshiriq: array_chunk() yordamida massivni sahifalarga (bo'laklarga) bo'lish
## Topshiriq sharti:
10 ta elementdan iborat ro'yxatni `array_chunk()` yordamida 3 tadan elementli guruhlarga bo'ling.

## Yechim (PHP kodi):
```php
<?php

$mahsulotlar = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

$sahifalar = array_chunk($mahsulotlar, 3);

echo "Jami sahifalar soni: " . count($sahifalar) . "
";
foreach ($sahifalar as $sahifa_raqami => $guruh) {
    echo ($sahifa_raqami + 1) . "-sahifa: " . implode(", ", $guruh) . "
";
}

```

## Tushuntirish va Mantiq:
`array_chunk($massiv, $olcham)` katta massivni kichik bloklarga ajratadi. Web-loyihalarda paginatsiya yoki ma'lumotlar bazasiga batch (to'p) ko'rinishida yozishda juda ko'p qo'llaniladi.

## Ishlash natijasi:
```text
Jami sahifalar soni: 4
1-sahifa: 1, 2, 3
2-sahifa: 4, 5, 6
3-sahifa: 7, 8, 9
4-sahifa: 10
```

# 140-Topshiriq: array_unique() orqali takrorlangan elementlarni tozalash
## Topshiriq sharti:
Massivdagi takrorlangan ID raqamlarni `array_unique()` yordamida olib tashlang.

## Yechim (PHP kodi):
```php
<?php

$kirgan_idlar = [101, 102, 101, 105, 102, 108, 105];

$unikal_idlar = array_values(array_unique($kirgan_idlar));

print_r($unikal_idlar);

```

## Tushuntirish va Mantiq:
`array_unique($massiv)` barcha takrorlangan elementlarni o'chirib, har bir qiymatdan faqat bittadan qoldiradi. Dastlabki kalitlar saqlanib qoladi.

## Ishlash natijasi:
```text
Array
(
    [0] => 101
    [1] => 102
    [2] => 105
    [3] => 108
)
```

# 141-Topshiriq: sort() va rsort() orqali o'sish va kamayish tartibida saralash
## Topshiriq sharti:
Sonli massivni `sort()` (o'sish) va `rsort()` (kamayish) bo'yicha tartiblang.

## Yechim (PHP kodi):
```php
<?php

$raqamlar = [45, 12, 89, 3, 27];

sort($raqamlar);
echo "O'sish tartibida: " . implode(", ", $raqamlar) . "
";

rsort($raqamlar);
echo "Kamayish tartibida: " . implode(", ", $raqamlar) . "
";

```

## Tushuntirish va Mantiq:
`sort(&$massiv)` massivni o'sish tartibida saralaydi va kalitlarni 0 dan qayta raqamlaydi. `rsort(&$massiv)` esa kamayish tartibida saralaydi.

## Ishlash natijasi:
```text
O'sish tartibida: 3, 12, 27, 45, 89
Kamayish tartibida: 89, 45, 27, 12, 3
```

# 142-Topshiriq: asort() va arsort() orqali kalitlarni saqlab saralash
## Topshiriq sharti:
Assotsiativ massivdagi talabalar ballarini ularning ism-kalitlarini yo'qotmasdan `asort()` va `arsort()` orqali saralang.

## Yechim (PHP kodi):
```php
<?php

$natijalar = [
    "Aziz" => 75,
    "Malika" => 95,
    "Sardor" => 88
];

arsort($natijalar);

echo "Reyting (yuqoridan pastga):
";
foreach ($natijalar as $ism => $ball) {
    echo "  $ism: $ball ball
";
}

```

## Tushuntirish va Mantiq:
`asort()` va `arsort()` qiymat bo'yicha saralaydi, ammo mavjud kalit-qiymat assotsiatsiyasini saqlab qoladi. Reyting jadvallari uchun juda qulay.

## Ishlash natijasi:
```text
Reyting (yuqoridan pastga):
  Malika: 95 ball
  Sardor: 88 ball
  Aziz: 75 ball
```

# 143-Topshiriq: ksort() va krsort() orqali massiv kalitlari bo'yicha saralash
## Topshiriq sharti:
Lug'at yoki sana bo'yicha indekslangan massivni kalitlari asosida `ksort()` yordamida alifbo tartibiga keltiring.

## Yechim (PHP kodi):
```php
<?php

$lugat = [
    "nok" => "Pear",
    "olma" => "Apple",
    "anor" => "Pomegranate",
    "shaftoli" => "Peach"
];

ksort($lugat);

foreach ($lugat as $uzb => $eng) {
    echo "$uzb -> $eng
";
}

```

## Tushuntirish va Mantiq:
`ksort()` massivni kalitlari (keys) bo'yicha o'sish tartibida, `krsort()` esa kamayish tartibida saralaydi.

## Ishlash natijasi:
```text
anor -> Pomegranate
nok -> Pear
olma -> Apple
shaftoli -> Peach
```

# 144-Topshiriq: usort() yordamida maxsus qoida bo'yicha saralash
## Topshiriq sharti:
Foydalanuvchilarni ularning yoshi bo'yicha `<=>` operatoridan foydalanib `usort()` orqali saralang.

## Yechim (PHP kodi):
```php
<?php

$odamlar = [
    ["ism" => "Rustam", "yosh" => 34],
    ["ism" => "Diyor", "yosh" => 21],
    ["ism" => "Kamron", "yosh" => 28]
];

usort($odamlar, fn($a, $b) => $a["yosh"] <=> $b["yosh"]);

foreach ($odamlar as $odam) {
    echo $odam["ism"] . " (" . $odam["yosh"] . " yosh)
";
}

```

## Tushuntirish va Mantiq:
`usort(&$massiv, $callback)` foydalanuvchi tomonidan taqdim etilgan solishtirish funksiyasiga asosan saralaydi. Callback `-1, 0, 1` qaytarishi kerak (Spaceship `<=>` operatori bu uchun ideal).

## Ishlash natijasi:
```text
Diyor (21 yosh)
Kamron (28 yosh)
Rustam (34 yosh)
```

# 145-Topshiriq: uasort() va uksort() funksiyalari
## Topshiriq sharti:
Kalitlarni saqlagan holda maxsus algoritm bo'yicha `uasort()` bilan saralashni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

$shaharlar_aholi = [
    "Samarqand" => 550000,
    "Toshkent" => 2900000,
    "Namangan" => 670000
];

// Aholisi eng ko'p bo'yicha kamayish tartibida saralash
uasort($shaharlar_aholi, fn($a, $b) => $b <=> $a);

foreach ($shaharlar_aholi as $shahar => $aholi) {
    echo "$shahar: " . number_format($aholi) . " kishi
";
}

```

## Tushuntirish va Mantiq:
`uasort()` assotsiativ massiv kalitlarini saqlagan holda foydalanuvchi funksiyasi orqali saralaydi. `uksort()` esa kalitlarni foydalanuvchi funksiyasi bilan tartiblaydi.

## Ishlash natijasi:
```text
Toshkent: 2,900,000 kishi
Namangan: 670,000 kishi
Samarqand: 550,000 kishi
```

# 146-Topshiriq: array_diff() va array_diff_assoc() orqali massivlar farqini topish
## Topshiriq sharti:
Ikki massiv o'rtasidagi farqlarni (faqat birinchisida bor, ikkinchisida yo'q elementlarni) toping.

## Yechim (PHP kodi):
```php
<?php

$eski_rollar = ["ko'rish", "tahrirlash", "o'chirish"];
$yangi_rollar = ["ko'rish", "eksport"];

$ochirilishi_kerak = array_diff($eski_rollar, $yangi_rollar);

echo "O'chirilishi kerak bo'lgan huquqlar:
";
print_r(array_values($ochirilishi_kerak));

```

## Tushuntirish va Mantiq:
`array_diff($m1, $m2)` birinchi massivda mavjud bo'lib, keyingi massivlarda uchramaydigan qiymatlarni qaytaradi. `array_diff_assoc()` esa bir vaqtning o'zida kalitlarni ham tekshiradi.

## Ishlash natijasi:
```text
O'chirilishi kerak bo'lgan huquqlar:
Array
(
    [0] => tahrirlash
    [1] => o'chirish
)
```

# 147-Topshiriq: array_intersect() orqali umumiy kesishmani topish
## Topshiriq sharti:
Ikkita foydalanuvchining umumiy qiziqishlarini `array_intersect()` orqali aniqlang.

## Yechim (PHP kodi):
```php
<?php

$qiziqish1 = ["futbol", "kino", "dasturlash", "shaxmat"];
$qiziqish2 = ["musiqa", "shaxmat", "dasturlash"];

$umumiy = array_intersect($qiziqish1, $qiziqish2);

echo "Umumiy qiziqishlar:
";
print_r(array_values($umumiy));

```

## Tushuntirish va Mantiq:
`array_intersect($m1, $m2)` barcha berilgan massivlarda bir vaqtda mavjud bo'lgan umumiy elementlarni qaytaradi.

## Ishlash natijasi:
```text
Umumiy qiziqishlar:
Array
(
    [0] => dasturlash
    [1] => shaxmat
)
```

# 148-Topshiriq: array_flip() yordamida kalit va qiymatlar o'rnini almashtirish
## Topshiriq sharti:
Tezkor qidiruv (O(1) murakkablik) qilish uchun massivning kalit va qiymatlarini `array_flip()` orqali almashtiring.

## Yechim (PHP kodi):
```php
<?php

$statuslar = [
    1 => "faol",
    2 => "bloklangan",
    3 => "kutishda"
];

$qidiruv_jadvali = array_flip($statuslar);

echo "'bloklangan' status kodi: " . $qidiruv_jadvali["bloklangan"] . "
";

```

## Tushuntirish va Mantiq:
`array_flip($massiv)` massivdagi har bir elementning kalitini qiymatga, qiymatini esa kalitga aylantiradi. Agar qiymatlar takrorlangan bo'lsa, oxirgi kalit saqlanib qoladi.

## Ishlash natijasi:
```text
'bloklangan' status kodi: 2
```

# 149-Topshiriq: array_reverse() orqali massivni teskari tartibda o'girish
## Topshiriq sharti:
Xabarlar lentasini teskari tartibda chiqarish uchun `array_reverse()` funksiyasidan foydalaning.

## Yechim (PHP kodi):
```php
<?php

$xabarlar = ["Xabar #1", "Xabar #2", "Xabar #3"];

$teskari = array_reverse($xabarlar);

print_r($teskari);

```

## Tushuntirish va Mantiq:
`array_reverse($massiv, $preserve_keys)` massiv elementlarini oxiridan boshlab teskari tartibda yangi massiv qilib qaytaradi. Ikkinchi parametri `true` bo'lsa, raqamli kalitlar saqlanadi.

## Ishlash natijasi:
```text
Array
(
    [0] => Xabar #3
    [1] => Xabar #2
    [2] => Xabar #1
)
```

# 150-Topshiriq: count() va COUNT_RECURSIVE parametri
## Topshiriq sharti:
Ko'p o'lchamli massivdagi barcha ichki elementlar sonini `COUNT_RECURSIVE` orqali to'liq hisoblang.

## Yechim (PHP kodi):
```php
<?php

$menyu = [
    "Bosh sahifa" => [],
    "Xizmatlar" => ["Veb dizayn", "Mobil ilova", "SEO"],
    "Aloqa" => ["Manzil", "Telefon"]
];

$oddiy_soni = count($menyu);
$rekursiv_soni = count($menyu, COUNT_RECURSIVE);

echo "Asosiy bo'limlar soni: $oddiy_soni
";
echo "Barcha ichki elementlar bilan jami soni: $rekursiv_soni
";

```

## Tushuntirish va Mantiq:
`count($massiv, $mode)` massiv hajmini qaytaradi. Agar ikkinchi parametr `COUNT_RECURSIVE` (yoki 1) berilsa, u barcha ichma-ich massiv elementlarini ham qo'shib hisoblaydi.

## Ishlash natijasi:
```text
Asosiy bo'limlar soni: 3
Barcha ichki elementlar bilan jami soni: 8
```
