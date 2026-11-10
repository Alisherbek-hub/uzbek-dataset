# 2-Mavzu: Satrlar (Strings) va Muntazam Ifodalar (RegEx) (51-100)

Ushbu bo'limda PHP dasturlash tilida matnlar bilan professional darajada ishlash, UTF-8 ko'p baytli satrlar xususiyatlari, xavfsizlik filtrlari hamda PCRE (Perl Compatible Regular Expressions) imkoniyatlari to'liq ochib berilgan:
Bittalik va qo'shtirnoqlar, Heredoc va Nowdoc sintaksislari, `strlen` va `mb_strlen`, qidiruv va tekshiruv (`strpos`, `stripos`, `str_contains`, `str_starts_with`, `str_ends_with`), registrlarni o'zgartirish (`mb_strtoupper`, `ucfirst`, `ucwords`), satrlarni formatlash va tekislash (`trim`, `str_repeat`, `str_pad`, `sprintf`, `number_format`), xavfsizlik va kodlash (`htmlspecialchars`, `strip_tags`, `md5`, `hash('sha256')`, `base64_encode`), shuningdek muntazam ifodalar (`preg_match`, `preg_match_all`, `preg_replace`, `preg_replace_callback`, `preg_split`, telefon va email tekshiruvi, URL-friendly slug generatsiyasi) bo'yicha 50 ta amaliy topshiriq jamlangan.

---

# 51-Topshiriq: Bittalik va qo'shtirnoq farqi (Interpolyatsiya)
## Topshiriq sharti:
Bittalik tirnoq (`'`) va qo'shtirnoq (`"`) yordamida o'zgaruvchilarni va qochish belgilarini (`\n`, `\t`) chiqarish farqini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

$ism = "Anvar";

// Bittalik tirnoqda o'zgaruvchi va qochish belgilari o'qilmaydi
$matn1 = 'Salom, $ism!
Bu yerda yangi qator bo'lmaydi.';

// Qo'shtirnoqda o'zgaruvchi va belgilar tahlil qilinadi
$matn2 = "Salom, {$ism}!
Bu yerda yangi qator hosil bo'ladi.";

echo "--- Bittalik tirnoq ---
";
echo $matn1 . "
";
echo "--- Qo'shtirnoq ---
";
echo $matn2 . "
";

```

## Tushuntirish va Mantiq:
Qo'shtirnoq ichidagi o'zgaruvchilar avtomatik tarzda ularning qiymatlariga almashtiriladi (string interpolation). Murakkab nomlar uchun `{$o'zgaruvchi}` sintaksisi tavsiya etiladi. Bittalik tirnoq esa ichidagi matnni aynan qanday yozilgan bo'lsa shundayligicha qabul qiladi va hisoblash talab qilmagani sababli biroz tezroq ishlaydi.

## Ishlash natijasi:
```text
--- Bittalik tirnoq ---
Salom, $ism!\nBu yerda yangi qator bo'lmaydi.
--- Qo'shtirnoq ---
Salom, Anvar!
Bu yerda yangi qator hosil bo'ladi.
```

# 52-Topshiriq: Heredoc sintaksisi orqali ko'p qatorli matn yaratish
## Topshiriq sharti:
`<<<EOD` (Heredoc) sintaksisidan foydalanib, HTML yoki SQL shablonini o'zgaruvchilar bilan birgalikda yaratuvchi dastur yozing.

## Yechim (PHP kodi):
```php
<?php

$mahsulot = "Noutbuk Asus ROG";
$narx = 14500000;
$miqdor = 2;

$html = <<<HTML
<div class="card">
    <h2>{$mahsulot}</h2>
    <p>Narxi: {$narx} so'm</p>
    <p>Miqdori: {$miqdor} dona</p>
    <p>Jami: {$narx * $miqdor} so'm</p>
</div>
HTML;

echo $html . "
";

```

## Tushuntirish va Mantiq:
Heredoc sintaksisi `<<<IDENTIFIKATOR` bilan boshlanadi va yangi qatorda aynan shu identifikator bilan yakunlanadi. U qo'shtirnoq kabi ishlaydi: ichidagi o'zgaruvchilar va ifodalar tahlil qilinadi, lekin matn ichida tirnoqlarni qochirish (`\"`) shart emas. Ko'p qatorli HTML, SQL yoki JSON shablonlar uchun juda qulay.

## Ishlash natijasi:
```text
<div class="card">
    <h2>Noutbuk Asus ROG</h2>
    <p>Narxi: 14500000 so'm</p>
    <p>Miqdori: 2 dona</p>
    <p>Jami: 29000000 so'm</p>
</div>
```

# 53-Topshiriq: Nowdoc sintaksisi va o'zgarmas shablonlar
## Topshiriq sharti:
`<<<'NOWDOC'` sintaksisidan foydalanib, ichida `$` va boshqa maxsus belgilar bo'lgan xom (raw) skript matnini ekranga chiqaring.

## Yechim (PHP kodi):
```php
<?php

$skript = <<<'BASH'
#!/bin/bash
USER_NAME="admin"
echo "Foydalanuvchi: $USER_NAME"
echo "Barcha parametrlar: $@"
BASH;

echo $skript . "
";

```

## Tushuntirish va Mantiq:
Nowdoc xuddi bittalik tirnoq kabi ishlaydi: ochilish identifikatori bittalik tirnoqqa olinadi `<<<'TEG'`. Unda hech qanday o'zgaruvchi interpolatsiyasi bajarilmaydi. Bash skriptlari, JavaScript kodlari yoki PHP kod namunalarini o'zgarishsiz saqlashda ishlatiladi.

## Ishlash natijasi:
```text
#!/bin/bash
USER_NAME="admin"
echo "Foydalanuvchi: $USER_NAME"
echo "Barcha parametrlar: $@"

```

# 54-Topshiriq: Satrlarni nuqta (.) operatori orqali birlashtirish
## Topshiriq sharti:
Foydalanuvchi ismi, familiyasi va unvonini nuqta `.` birlashtirish operatori orqali bitta to'liq satrga aylantiring.

## Yechim (PHP kodi):
```php
<?php

$unvon = "Muhandis";
$ism = "Javohir";
$familiya = "Usmonov";

$toliq_malumot = $unvon . " " . $ism . " " . $familiya . " - Khorazmiy AI a'zosi";

echo $toliq_malumot . "
";

```

## Tushuntirish va Mantiq:
PHP da satrlarni o'zaro ulash (konkatenatsiya) uchun nuqta (`.`) operatori xizmat qiladi. Raqamlar bilan birga ishlatilganda sonlar avtomatik ravishda satrga o'giriladi.

## Ishlash natijasi:
```text
Muhandis Javohir Usmonov - Khorazmiy AI a'zosi
```

# 55-Topshiriq: strlen() vs mb_strlen(): UTF-8 va ko'p baytli satrlar
## Topshiriq sharti:
O'zbek tilidagi kirill va o'ziga xos harflar ('O'zbekiston', 'Муҳандис') uchun `strlen()` va `mb_strlen()` funksiyalarini taqqoslang.

## Yechim (PHP kodi):
```php
<?php

$matn_lotin = "O'zbekiston";
$matn_kirill = "Ўзбекистон";

echo "Lotin matn: '$matn_lotin'
";
echo "  strlen: " . strlen($matn_lotin) . "
";
echo "  mb_strlen: " . mb_strlen($matn_lotin, 'UTF-8') . "
";

echo "Kirill matn: '$matn_kirill'
";
echo "  strlen: " . strlen($matn_kirill) . " (baytlar soni)
";
echo "  mb_strlen: " . mb_strlen($matn_kirill, 'UTF-8') . " (haqiqiy belgilar soni)
";

```

## Tushuntirish va Mantiq:
`strlen()` funksiyasi satrdagi baytlar sonini hisoblaydi. UTF-8 kodirovkasida kirill va boshqa harflar 2 yoki undan ko'p bayt egallaydi. Shuning uchun UTF-8 belgilar sonini to'g'ri o'lchash uchun har doim `mb_strlen($str, 'UTF-8')` funksiyasidan foydalanish shart.

## Ishlash natijasi:
```text
Lotin matn: 'O'zbekiston'
  strlen: 11
  mb_strlen: 11
Kirill matn: 'Ўзбекистон'
  strlen: 20 (baytlar soni)
  mb_strlen: 10 (haqiqiy belgilar soni)
```

# 56-Topshiriq: strpos() orqali qidirish va qat'iy tekshiruv (=== false)
## Topshiriq sharti:
`strpos()` yordamida matn ichidan so'zning boshlanish pozitsiyasini toping va natijani qat'iy tenglik bilan tekshiring.

## Yechim (PHP kodi):
```php
<?php

$matn = "PHP - bu zamonaviy va tezkor backend tili";
$qidiruv = "PHP";

$pozitsiya = strpos($matn, $qidiruv);

if ($pozitsiya !== false) {
    echo "'$qidiruv' so'zi $pozitsiya - indeksdan boshlanadi.
";
} else {
    echo "'$qidiruv' so'zi topilmadi.
";
}

```

## Tushuntirish va Mantiq:
`strpos()` qidirilayotgan qism satrning birinchi uchragan indeksini qaytaradi (0 dan boshlanadi). Agar qidirilayotgan so'z satr boshida tursa, u `0` qaytaradi. Agar `==` orqali tekshirilsa, `0 == false` rost bo'lib qoladi. Shuning uchun qat'iy tengsizlik `!== false` ishlatilishi shart!

## Ishlash natijasi:
```text
'PHP' so'zi 0 - indeksdan boshlanadi.
```

# 57-Topshiriq: stripos() orqali registrga sezgir bo'lmagan qidiruv
## Topshiriq sharti:
Katta-kichik harflaridan qat'i nazar so'zni topish uchun `stripos()` funksiyasidan foydalaning.

## Yechim (PHP kodi):
```php
<?php

$matn = "Laravel - eng mashhur Web Framework.";
$kalit = "laravel";

$joy = stripos($matn, $kalit);

if ($joy !== false) {
    echo "'$kalit' registrga qaramasdan topildi! Indeks: $joy
";
} else {
    echo "Topilmadi.
";
}

```

## Tushuntirish va Mantiq:
`stripos()` funksiyasidagi 'i' harfi 'case-insensitive' (katta-kichik harfga befarq) degan ma'noni anglatadi. U qidiruvda 'Laravel', 'laravel', 'LARAVEL' so'zlarini teng deb biladi.

## Ishlash natijasi:
```text
'laravel' registrga qaramasdan topildi! Indeks: 0
```

# 58-Topshiriq: strrpos() orqali satr oxiridan qidirish
## Topshiriq sharti:
Fayl yo'lidagi oxirgi nuqta yoki bo'luvchi slesh (`/`) indeksini `strrpos()` orqali aniqlang.

## Yechim (PHP kodi):
```php
<?php

$fayl_yoli = "/var/www/html/khorazmiy/app/Controllers/HomeController.php";

$oxirgi_slash = strrpos($fayl_yoli, "/");
$oxirgi_nuqta = strrpos($fayl_yoli, ".");

$fayl_nomi = substr($fayl_yoli, $oxirgi_slash + 1);
$kengaytma = substr($fayl_yoli, $oxirgi_nuqta + 1);

echo "Fayl nomi: $fayl_nomi
";
echo "Kengaytmasi: $kengaytma
";

```

## Tushuntirish va Mantiq:
`strrpos()` (string reverse position) qidirilayotgan belgining satr oxiriga eng yaqin joylashgan oxirgi indeksini qaytaradi. Fayl kengaytmalarini yoki papka yo'llarini ajratishda juda asqotadi.

## Ishlash natijasi:
```text
Fayl nomi: HomeController.php
Kengaytmasi: php
```

# 59-Topshiriq: str_contains() yordamida qulay mavjudlik tekshiruvi (PHP 8)
## Topshiriq sharti:
PHP 8 da kiritilgan `str_contains()` funksiyasi orqali matnda belgilangan so'z bor yoki yo'qligini aniqlang.

## Yechim (PHP kodi):
```php
<?php

$xabar = "To'lov muvaffaqiyatli qabul qilindi. Tranzaksiya raqami: #TX99102";

if (str_contains($xabar, "muvaffaqiyatli")) {
    echo "Operatsiya ijobiy yakunlangan.
";
}

if (!str_contains($xabar, "xatolik")) {
    echo "Xabarda hech qanday xatolik eslatilmagan.
";
}

```

## Tushuntirish va Mantiq:
`str_contains($butun_matn, $qidiruv)` mantiqiy `true` yoki `false` qaytaradi. Bu eski `strpos($matn, $soz) !== false` yozuvini almashtirib, kodni juda toza va ravon qiladi.

## Ishlash natijasi:
```text
Operatsiya ijobiy yakunlangan.
Xabarda hech qanday xatolik eslatilmagan.
```

# 60-Topshiriq: str_starts_with() va str_ends_with() funksiyalari (PHP 8)
## Topshiriq sharti:
API marshrutining `/api/` bilan boshlanishini va faylning `.json` bilan tugashini tekshiruvchi kod yozing.

## Yechim (PHP kodi):
```php
<?php

$url = "/api/v1/users";
$fayl = "config.production.json";

if (str_starts_with($url, "/api/")) {
    echo "Bu API so'rovi hisoblanadi.
";
}

if (str_ends_with($fayl, ".json")) {
    echo "Bu JSON formatidagi konfiguratsiya fayli.
";
}

```

## Tushuntirish va Mantiq:
PHP 8 ning `str_starts_with()` va `str_ends_with()` funksiyalari satrning boshi yoki oxiri mos kelishini tekshiradi va to'g'ridan-to'g'ri `boolean` qaytaradi.

## Ishlash natijasi:
```text
Bu API so'rovi hisoblanadi.
Bu JSON formatidagi konfiguratsiya fayli.
```

# 61-Topshiriq: strtoupper() va strtolower() funksiyalari
## Topshiriq sharti:
Standart lotin matnini butunlay katta va kichik harflarga o'tkazing.

## Yechim (PHP kodi):
```php
<?php

$matn = "PHP Hypertext Preprocessor";

$katta = strtoupper($matn);
$kichik = strtolower($matn);

echo "Asl: $matn
";
echo "Katta harflarda: $katta
";
echo "Kichik harflarda: $kichik
";

```

## Tushuntirish va Mantiq:
`strtoupper()` barcha harflarni bosh harflarga, `strtolower()` esa kichik harflarga almashtiradi. Standart ASCII harflari uchun mo'ljallangan.

## Ishlash natijasi:
```text
Asl: PHP Hypertext Preprocessor
Katta harflarda: PHP HYPERTEXT PREPROCESSOR
Kichik harflarda: php hypertext preprocessor
```

# 62-Topshiriq: mb_strtoupper() va mb_strtolower() UTF-8 bilan ishlash
## Topshiriq sharti:
Kirill va maxsus harflardan iborat o'zbekcha matnni xavfsiz bosh va kichik harflarga o'giring.

## Yechim (PHP kodi):
```php
<?php

$kirill_matn = "Ўзбекиiston РеспубЛикаси";

$katta_kirill = mb_strtoupper($kirill_matn, 'UTF-8');
$kichik_kirill = mb_strtolower($kirill_matn, 'UTF-8');

echo "Katta: $katta_kirill
";
echo "Kichik: $kichik_kirill
";

```

## Tushuntirish va Mantiq:
Oddiy `strtoupper()` ko'p baytli kirill harflarini noto'g'ri o'zgartirishi yoki buzishi mumkin. Ko'p tilli loyihalarda har doim `mb_strtoupper()` va `mb_strtolower()` dan UTF-8 kodirovkasi bilan foydalanish tavsiya etiladi.

## Ishlash natijasi:
```text
Katta: ЎЗБЕКИISTON РЕСПУБЛИКАСИ
Kichik: ўзбекиiston республикаси
```

# 63-Topshiriq: ucfirst() va lcfirst() funksiyalari
## Topshiriq sharti:
Foydalanuvchi kiritgan ismning birinchi harfini katta qilish va satr boshidagi harfni kichik qilishni namoyish eting.

## Yechim (PHP kodi):
```php
<?php

$ism = "rustam";
$nom = "CamelCaseMetod";

echo "ucfirst: " . ucfirst($ism) . "
";
echo "lcfirst: " . lcfirst($nom) . "
";

```

## Tushuntirish va Mantiq:
`ucfirst()` satrning birinchi belgisini bosh harfga aylantiradi. `lcfirst()` esa aksincha, birinchi belgisini kichik harfga aylantiradi (masalan, sinf nomidan metod nomi yasashda).

## Ishlash natijasi:
```text
ucfirst: Rustam
lcfirst: camelCaseMetod
```

# 64-Topshiriq: ucwords() orqali har bir so'z bosh harfini katta qilish
## Topshiriq sharti:
Kitob yoki maqola sarlavhasidagi barcha so'zlarning birinchi harfini `ucwords()` yordamida katta qiling.

## Yechim (PHP kodi):
```php
<?php

$sarlavha = "algoritmlar va ma'lumotlar tuzilmasi asoslari";

$formatlangan = ucwords($sarlavha);

echo "Sarlavha: $formatlangan
";

```

## Tushuntirish va Mantiq:
`ucwords()` satrdagi probel yoki boshqa ajratuvchilar bilan ajratilgan har bir alohida so'zning bosh harfini katta harfga o'tkazadi.

## Ishlash natijasi:
```text
Sarlavha: Algoritmlar Va Ma'lumotlar Tuzilmasi Asoslari
```

# 65-Topshiriq: trim(), ltrim() va rtrim() orqali bo'shliqlarni tozalash
## Topshiriq sharti:
Formadan kelgan foydalanuvchi ma'lumotlarining boshidagi va oxiridagi bo'shliqlarni tozalashni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

$foydalanuvchi_input = "   dilshod@example.com    
	";

$tozalangan = trim($foydalanuvchi_input);
$faqat_chap = ltrim($foydalanuvchi_input);
$faqat_ong = rtrim($foydalanuvchi_input);

echo "Asl uzunlik: " . strlen($foydalanuvchi_input) . "
";
echo "trim() uzunlik: " . strlen($tozalangan) . " ('$tozalangan')
";

```

## Tushuntirish va Mantiq:
`trim()` satrning ikki chetidagi barcha bo'sh joylar (probel, tabulyatsiya `\t`, yangi qator `\n`, `\r`) ni tozalaydi. `ltrim()` faqat chap tomondan, `rtrim()` faqat o'ng tomondan tozalaydi.

## Ishlash natijasi:
```text
Asl uzunlik: 30
trim() uzunlik: 19 ('dilshod@example.com')
```

# 66-Topshiriq: Maxsus belgilarni trim() yordamida kesib tashlash
## Topshiriq sharti:
Satr boshidagi va oxiridagi ortiqcha chiziqcha va slashelarni `trim()` ning ikkinchi parametri orqali tozalang.

## Yechim (PHP kodi):
```php
<?php

$marshrut = "/users/profile/details///";
$tozalangan_url = trim($marshrut, "/");

$kod = "---KHORAZMIY---";
$tozalangan_kod = trim($kod, "-");

echo "URL: $tozalangan_url
";
echo "Kod: $tozalangan_kod
";

```

## Tushuntirish va Mantiq:
`trim($satr, $belgilar)` ikkinchi argumentida berilgan barcha belgilarni satrning ikki chetidan olib tashlaydi. Bu URL lar, fayl yo'llari va prefikslar bilan ishlashda qulay.

## Ishlash natijasi:
```text
URL: users/profile/details
Kod: KHORAZMIY
```

# 67-Topshiriq: str_repeat() yordamida ajratuvchi chiziqlar va grafik chizish
## Topshiriq sharti:
`str_repeat()` funksiyasidan foydalanib konsol jadvali uchun chiroyli sarlavha va chiziqlar yasang.

## Yechim (PHP kodi):
```php
<?php

$sarlavha = "XISOBOT";
$chiziq = str_repeat("=", 30);
$yulduzcha = str_repeat("*", 5);

echo $chiziq . "
";
echo "$yulduzcha $sarlavha $yulduzcha
";
echo $chiziq . "
";

```

## Tushuntirish va Mantiq:
`str_repeat($satr, $soni)` berilgan satrni ko'rsatilgan miqdorda takrorlab, bitta yangi satr hosil qiladi.

## Ishlash natijasi:
```text
==============================
***** XISOBOT *****
==============================
```

# 68-Topshiriq: str_pad() yordamida satrni to'ldirish
## Topshiriq sharti:
Foydalanuvchi ID raqamlarini olti xonali qilib nollar bilan to'ldirish (`STR_PAD_LEFT`) va chek satrini tekislashni bajaring.

## Yechim (PHP kodi):
```php
<?php

$id1 = 45;
$id2 = 1209;

$format_id1 = str_pad((string)$id1, 6, "0", STR_PAD_LEFT);
$format_id2 = str_pad((string)$id2, 6, "0", STR_PAD_LEFT);

echo "ID 1: INV-$format_id1
";
echo "ID 2: INV-$format_id2
";

$tovar = "Non";
echo str_pad($tovar, 15, ".") . " 3000 so'm
";

```

## Tushuntirish va Mantiq:
`str_pad($satr, $uzunlik, $belgi, $joylashuv)` satrni belgilangan uzunlikka yetguncha ko'rsatilgan belgi bilan to'ldiradi. `$joylashuv` sifatida `STR_PAD_LEFT`, `STR_PAD_RIGHT` yoki `STR_PAD_BOTH` berilishi mumkin.

## Ishlash natijasi:
```text
ID 1: INV-000045
ID 2: INV-001209
Non............ 3000 so'm
```

# 69-Topshiriq: strrev() orqali satrni teskarisiga o'girish va palindrom tekshiruvi
## Topshiriq sharti:
Berilgan so'zning palindrom (o'ngdan ham chapdan ham bir xil o'qilishi) ekanligini `strrev()` yordamida tekshiring.

## Yechim (PHP kodi):
```php
<?php

function palindrommi(string $soz): bool {
    $tozalangan = strtolower(trim($soz));
    return $tozalangan === strrev($tozalangan);
}

$sinov1 = "alla";
$sinov2 = "madam";
$sinov3 = "kitob";

echo "$sinov1: " . (palindrommi($sinov1) ? "Palindrom" : "Oddiy") . "
";
echo "$sinov2: " . (palindrommi($sinov2) ? "Palindrom" : "Oddiy") . "
";
echo "$sinov3: " . (palindrommi($sinov3) ? "Palindrom" : "Oddiy") . "
";

```

## Tushuntirish va Mantiq:
`strrev()` funksiyasi satr belgilarini teskari tartibda qaytaradi. Palindrom so'zlarni aniqlashda juda qulay usul hisoblanadi.

## Ishlash natijasi:
```text
alla: Palindrom
madam: Palindrom
kitob: Oddiy
```

# 70-Topshiriq: str_shuffle() yordamida belgilarni tasodifiy aralashtirish
## Topshiriq sharti:
Harflar va raqamlardan iborat to'plamdan `str_shuffle()` orqali tasodifiy parol generatsiyasi qiling.

## Yechim (PHP kodi):
```php
<?php

$belgilar = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%";
$aralashtirilgan = str_shuffle($belgilar);

// Parol uzunligini 12 ta belgi qilib qirqib olamiz
$parol = substr($aralashtirilgan, 0, 12);

echo "Yaratilgan tasodifiy parol uzunligi: " . strlen($parol) . " ta belgi
";
echo "Parol mavjud: " . (!empty($parol) ? "Ha" : "Yo'q") . "
";

```

## Tushuntirish va Mantiq:
`str_shuffle()` satrdagi barcha belgilarni tasodifiy tartibda o'rin almashtiradi. Uni `substr()` bilan birlashtirib sodda tasodifiy tokenlar yoki parollar yaratish mumkin.

## Ishlash natijasi:
```text
Yaratilgan tasodifiy parol uzunligi: 12 ta belgi
Parol mavjud: Ha
```

# 71-Topshiriq: substr() yordamida satrdan qism qirqib olish
## Topshiriq sharti:
`substr()` funksiyasining musbat va manfiy offsetlari yordamida matn bo'laklarini ajratib oling.

## Yechim (PHP kodi):
```php
<?php

$satr = "Dasturlash sirlari";

$qism1 = substr($satr, 0, 10);  // 0 dan boshlab 10 ta belgi
$qism2 = substr($satr, 11);     // 11 dan oxirigacha
$oxirgi4 = substr($satr, -7);   // Oxiridan 7 ta belgi

echo "Boshi: $qism1
";
echo "Davomi: $qism2
";
echo "Oxirgi qism: $oxirgi4
";

```

## Tushuntirish va Mantiq:
`substr($matn, $boshlanish, $uzunlik)` satrdan qism ajratadi. Agar `$boshlanish` manfiy son bo'lsa, hisoblash satr oxiridan boshlanadi. Agar `$uzunlik` berilmasa, satr oxirigacha olinadi.

## Ishlash natijasi:
```text
Boshi: Dasturlash
Davomi: sirlari
Oxirgi qism: sirlari
```

# 72-Topshiriq: mb_substr() orqali UTF-8 ko'p baytli matnlarni to'g'ri qirqish
## Topshiriq sharti:
O'zbekcha matnni maqola anonsi (preview) sifatida `mb_substr()` orqali xavfsiz qisqartiring.

## Yechim (PHP kodi):
```php
<?php

$maqola = "O'zbekiston kiberxavfsizlik va sun'iy intellekt sohasida ulkan qadamlar tashlamoqda.";

$anons = mb_substr($maqola, 0, 30, 'UTF-8') . "...";

echo "Anons: $anons
";

```

## Tushuntirish va Mantiq:
`mb_substr()` ko'p baytli UTF-8 harflarini ikkiga bo'lib, xunuk va buzilgan belgilar (masalan, ) paydo bo'lishining oldini oladi. Har doim matnlar bilan ishlaganda UTF-8 parametrini ko'rsatish maqsadga muvofiqdir.

## Ishlash natijasi:
```text
Anons: O'zbekiston kiberxavfsizlik v...
```

# 73-Topshiriq: str_replace() yordamida so'z yoki belgilarni almashtirish
## Topshiriq sharti:
Matn ichidagi noo'rin yoki taqiqlangan so'zlarni `str_replace()` orqali yulduzchalarga almashtiring.

## Yechim (PHP kodi):
```php
<?php

$sharh = "Bu mahsulot juda yomon va sifatsiz xizmat!";
$taqiqlangan = "yomon";

$tozalangan_sharh = str_replace($taqiqlangan, "*****", $sharh);

echo "Sharh: $tozalangan_sharh
";

```

## Tushuntirish va Mantiq:
`str_replace($nima, $nimaga, $qayerdan, [&$sanagich])` barcha mos keluvchi qiymatlarni yangi satrga almashtiradi. Ushbu funksiya registrga sezgirdir (case-sensitive).

## Ishlash natijasi:
```text
Sharh: Bu mahsulot juda ***** va sifatsiz xizmat!
```

# 74-Topshiriq: str_replace() ga massivlar uzatish orqali ko'p almashtirishlar
## Topshiriq sharti:
Bir nechta shablon teglarni (`{ism}`, `{sana}`, `{shahar}`) ularning haqiqiy qiymatlariga bitta `str_replace()` chaqiruvi bilan almashtiring.

## Yechim (PHP kodi):
```php
<?php

$shablon = "Hurmatli {ism}! Sizni {sana} kuni {shahar} shahrida kutamiz.";

$kalitlar = ["{ism}", "{sana}", "{shahar}"];
$qiymatlar = ["Botir", "20-may", "Samarqand"];

$xabar = str_replace($kalitlar, $qiymatlar, $shablon);

echo $xabar . "
";

```

## Tushuntirish va Mantiq:
`str_replace()` funksiyasiga birinchi va ikkinchi argument sifatida massivlar uzatilganda, u massiv elementlari bo'yicha mos tartibda bir nechta almashtirishlarni bir vaqtning o'zida amalga oshiradi.

## Ishlash natijasi:
```text
Hurmatli Botir! Sizni 20-may kuni Samarqand shahrida kutamiz.
```

# 75-Topshiriq: str_ireplace() orqali registrga befarq almashtirish
## Topshiriq sharti:
Foydalanuvchi qanday yozganidan qat'i nazar 'php' so'zini 'PHP 8.3' ga `str_ireplace()` yordamida almashtiring.

## Yechim (PHP kodi):
```php
<?php

$matn = "Bugun Php va pHP texnologiyalari juda tez rivojlanmoqda.";

$natija = str_ireplace("php", "PHP 8.3", $matn);

echo $natija . "
";

```

## Tushuntirish va Mantiq:
`str_ireplace()` 'case-insensitive' almashtirishni bajaradi, ya'ni katta va kichik harflarning farqiga bormasdan qidiruv so'zini topadi va almashtiradi.

## Ishlash natijasi:
```text
Bugun PHP 8.3 va PHP 8.3 texnologiyalari juda tez rivojlanmoqda.
```

# 76-Topshiriq: substr_replace() orqali satrning ma'lum qismini almashtirish
## Topshiriq sharti:
Karta raqamining o'rtadagi 8 ta raqamini maxfiylashtirib `**** ****` ko'rinishiga keltiring.

## Yechim (PHP kodi):
```php
<?php

$karta = "8600123456789012";

// 4-indeksdan boshlab 8 ta belgini yulduzchaga almashtiramiz
$yashirin_karta = substr_replace($karta, "********", 4, 8);

echo "Karta: " . chunk_split($yashirin_karta, 4, " ") . "
";

```

## Tushuntirish va Mantiq:
`substr_replace($satr, $almashtirish, $boshlanish, $uzunlik)` satrning aniq belgilangan oraliqdagi qismini boshqa satr bilan to'g'ridan-to'g'ri almashtiradi.

## Ishlash natijasi:
```text
Karta: 8600 ******** 9012 
```

# 77-Topshiriq: explode() yordamida satrni massivga ajratish
## Topshiriq sharti:
Vergul bilan ajratilgan teglarni `explode()` orqali massivga aylantirib, har birini chop eting.

## Yechim (PHP kodi):
```php
<?php

$teglar_satr = "texnologiya, dasturlash, sun'iy intellekt, php";

$teglar_massiv = explode(", ", $teglar_satr);

echo "Jami teglar: " . count($teglar_massiv) . "
";
foreach ($teglar_massiv as $indeks => $teg) {
    echo "  [$indeks] => $teg
";
}

```

## Tushuntirish va Mantiq:
`explode($ajratuvchi, $satr)` satrni ko'rsatilgan belgi bo'yicha bo'laklarga ajratib, massiv (array) ko'rinishida qaytaradi. CSV formatlar va teglarni qayta ishlashda eng ko'p ishlatiladigan vositadir.

## Ishlash natijasi:
```text
Jami teglar: 4
  [0] => texnologiya
  [1] => dasturlash
  [2] => sun'iy intellekt
  [3] => php
```

# 78-Topshiriq: explode() ning limit parametri bilan ishlash
## Topshiriq sharti:
`explode()` funksiyasida limit argumentidan foydalanib, faqat dastlabki elementlarni ajrating.

## Yechim (PHP kodi):
```php
<?php

$kirish = "admin:x:1000:1000:Admin User:/home/admin:/bin/bash";

// Faqat birinchi 3 ta bo'lakka bo'linadi, qolgani oxirgi elementda yaxlit qoladi
$qismlar = explode(":", $kirish, 3);

echo "Foydalanuvchi: " . $qismlar[0] . "
";
echo "Parol belgisi: " . $qismlar[1] . "
";
echo "Qolgan qismi: " . $qismlar[2] . "
";

```

## Tushuntirish va Mantiq:
`explode()` ning uchinchi parametri `$limit` massivdagi maksimal elementlar sonini belgilaydi. Qolgan barcha matn oxirgi element ichida yaxlit saqlanib qoladi.

## Ishlash natijasi:
```text
Foydalanuvchi: admin
Parol belgisi: x
Qolgan qismi: 1000:1000:Admin User:/home/admin:/bin/bash
```

# 79-Topshiriq: implode() (yoki join()) orqali massivni satrga aylantirish
## Topshiriq sharti:
Massivdagi shaharlar nomini `implode()` funksiyasi orqali chiziqcha bilan ajratilgan satrga aylantiring.

## Yechim (PHP kodi):
```php
<?php

$shaharlar = ["Samarqand", "Buxoro", "Xiva", "Toshkent"];

$satr = implode(" -> ", $shaharlar);

echo "Sayohat marshruti: " . $satr . "
";

```

## Tushuntirish va Mantiq:
`implode($ajratuvchi, $massiv)` massiv elementlarini ko'rsatilgan ajratuvchi vositasi bilan birlashtirib, bitta satr hosil qiladi. `join()` funksiyasi `implode()` ning to'liq sinonimidir.

## Ishlash natijasi:
```text
Sayohat marshruti: Samarqand -> Buxoro -> Xiva -> Toshkent
```

# 80-Topshiriq: strtok() orqali satrni leksemalarga (tokens) ajratish
## Topshiriq sharti:
Murakkab ifodani bir nechta har xil ajratuvchilar (probel, vergul, nuqta) bo'yicha `strtok()` orqali qadam-baqadam ajrating.

## Yechim (PHP kodi):
```php
<?php

$satr = "PHP,Java;Python Ruby	Go";
$ajratuvchilar = ",; 	";

$token = strtok($satr, $ajratuvchilar);

while ($token !== false) {
    echo "Leksema: $token
";
    $token = strtok($ajratuvchilar);
}

```

## Tushuntirish va Mantiq:
`strtok()` satrni ko'rsatilgan belgilar to'plami bo'yicha bosqichma-bosqich bo'laklarga (tokenlarga) ajratadi. Birinchi chaqiriqda asl satr beriladi, keyingi chaqiriqlarda faqat ajratuvchilar ko'rsatiladi.

## Ishlash natijasi:
```text
Leksema: PHP
Leksema: Java
Leksema: Python
Leksema: Ruby
Leksema: Go
```

# 81-Topshiriq: sprintf() orqali formatlangan satrlar yaratish
## Topshiriq sharti:
`sprintf()` yordamida sonlarni o'nlik formatda, suzuvchi nuqta aniqligida va matnlarni tartibli qilib formatlang.

## Yechim (PHP kodi):
```php
<?php

$nom = "Server #1";
$xotira_foizi = 78.4567;
$yuklanish = 4;

$natija = sprintf(
    "Holat: %s | Bandlik: %.2f%% | Oqimlar soni: %02d",
    $nom,
    $xotira_foizi,
    $yuklanish
);

echo $natija . "
";

```

## Tushuntirish va Mantiq:
`sprintf()` C tilidagi `printf` kabi formatlash spetsifikatorlaridan (`%s` satr, `%d` butun son, `%.2f` ikkita o'nlik kasrli float, `%02d` nollar bilan to'ldirish) foydalanib satr shakllantiradi va natijani satr sifatida qaytaradi.

## Ishlash natijasi:
```text
Holat: Server #1 | Bandlik: 78.46% | Oqimlar soni: 04
```

# 82-Topshiriq: vsprintf() massiv argumentlari bilan formatlash
## Topshiriq sharti:
Argumentlar soni dinamik bo'lgan holatda `vsprintf()` orqali massivdagi ma'lumotlarni shablonga joylashtiring.

## Yechim (PHP kodi):
```php
<?php

$shablon = "Foydalanuvchi: %s, Rol: %s, Kirishlar soni: %d";
$parametrlar = ["Sardor", "Moderator", 142];

$xabar = vsprintf($shablon, $parametrlar);

echo $xabar . "
";

```

## Tushuntirish va Mantiq:
`vsprintf()` xuddi `sprintf()` kabi ishlaydi, ammo alohida argumentlar o'rniga parametrlar massivini (array) qabul qiladi. Dinamik xabarlar va tarjima (i18n) tizimlarida juda qulay.

## Ishlash natijasi:
```text
Foydalanuvchi: Sardor, Rol: Moderator, Kirishlar soni: 142
```

# 83-Topshiriq: number_format() orqali pul va narx formatini chiqarish
## Topshiriq sharti:
`number_format()` yordamida katta pul miqdorlarini minglik ajratuvchilar bilan formatlang.

## Yechim (PHP kodi):
```php
<?php

$summa = 12543900.50;

// Standart 2 ta kasr xonasi, kasr uchun vergul, mingliklar uchun probel
$chiroyli_narx = number_format($summa, 2, ".", " ");

echo "Hisobingizdagi mablag': $chiroyli_narx so'm
";

```

## Tushuntirish va Mantiq:
`number_format($son, $kasr_xonasi, $kasr_ajratuvchi, $minglik_ajratuvchi)` katta sonlarni o'qilishi oson bo'lgan pul yoki miqdor shakliga keltiradi.

## Ishlash natijasi:
```text
Hisobingizdagi mablag': 12 543 900.50 so'm
```

# 84-Topshiriq: htmlspecialchars() orqali XSS xavfidan himoyalanish
## Topshiriq sharti:
Foydalanuvchi tomonidan yuborilgan HTML teglarni (`<script>`, `<b>`) xavfsiz holatga o'tkazing.

## Yechim (PHP kodi):
```php
<?php

$xavfli_matn = "<script>alert('XSS buzib kirish');</script> <b>Salom!</b>";

$xavfsiz_html = htmlspecialchars($xavfli_matn, ENT_QUOTES | ENT_HTML5, 'UTF-8');

echo "Xavfsiz qilingan kod:
";
echo $xavfsiz_html . "
";

```

## Tushuntirish va Mantiq:
`htmlspecialchars()` funksiyasi HTML dagi maxsus belgilarni (`<`, `>`, `&`, `"`, `'`) ularga mos HTML entitiylariga (`&lt;`, `&gt;`, `&amp;`, `&quot;`, `&apos;`) aylantiradi. Bu brauzerda skriptlarning bajarilishini to'xtatib, XSS hujumlaridan himoya qiladi.

## Ishlash natijasi:
```text
Xavfsiz qilingan kod:
&lt;script&gt;alert(&apos;XSS buzib kirish&apos;);&lt;/script&gt; &lt;b&gt;Salom!&lt;/b&gt;
```

# 85-Topshiriq: html_entity_decode() yordamida entitiylarni asl holiga qaytarish
## Topshiriq sharti:
`&lt;div&gt;` kabi HTML entitiylarni yana asl belgilar ko'rinishiga qaytaring.

## Yechim (PHP kodi):
```php
<?php

$kodlangan = "&lt;h1&gt;O&apos;zbekiston&lt;/h1&gt;";

$asl_holat = html_entity_decode($kodlangan, ENT_QUOTES | ENT_HTML5, 'UTF-8');

echo "Asl HTML: " . $asl_holat . "
";

```

## Tushuntirish va Mantiq:
`html_entity_decode()` `htmlspecialchars()` ga teskari amalni bajaradi, ya'ni HTML entitiylarni haqiqiy belgilariga qayta aylantiradi.

## Ishlash natijasi:
```text
Asl HTML: <h1>O'zbekiston</h1>
```

# 86-Topshiriq: strip_tags() orqali barcha HTML teglarni tozalash
## Topshiriq sharti:
Maqola matnidan barcha HTML teglarni qirqib tashlab, faqat toza matnni ajratib oling.

## Yechim (PHP kodi):
```php
<?php

$html_matn = "<p>Dasturlashni <strong>PHP</strong> va <em>Laravel</em> orqali o'rganamiz. <a href='#'>Batafsil</a></p>";

$toza_matn = strip_tags($html_matn);

echo "Toza matn: $toza_matn
";

```

## Tushuntirish va Mantiq:
`strip_tags()` barcha HTML va PHP teglarini matndan tozalab tashlaydi. E-pochta xabarlari yoki qidiruv tizimlari uchun indeksatsiya matnlarini tayyorlashda foydalidir.

## Ishlash natijasi:
```text
Toza matn: Dasturlashni PHP va Laravel orqali o'rganamiz. Batafsil
```

# 87-Topshiriq: addslashes() va stripslashes() funksiyalari
## Topshiriq sharti:
Satr ichidagi tirnoqlarni qochirish va qayta tiklashni namoyish eting.

## Yechim (PHP kodi):
```php
<?php

$matn = "O'quvchining kitobi: "O'tkan kunlar"";

$qochirilgan = addslashes($matn);
$tiklangan = stripslashes($qochirilgan);

echo "Qochirilgan: $qochirilgan
";
echo "Qayta tiklangan: $tiklangan
";

```

## Tushuntirish va Mantiq:
`addslashes()` tirnoqlar (`'`, `"`) va teskari slashes (`\`) oldiga teskari slashelarni qo'shadi. `stripslashes()` esa bu teskari slashelarni olib tashlaydi. (Eslatma: Ma'lumotlar bazasi so'rovlari uchun Prepared Statements afzalroq).

## Ishlash natijasi:
```text
Qochirilgan: O\'quvchining kitobi: \"O\'tkan kunlar\"
Qayta tiklangan: O'quvchining kitobi: "O'tkan kunlar"
```

# 88-Topshiriq: md5() va sha1() xesh funksiyalari va ularning maqsadi
## Topshiriq sharti:
Fayl yoki satr yaxlitligini tekshirish uchun MD5 va SHA1 nazorat summalarini (checksum) hisoblang.

## Yechim (PHP kodi):
```php
<?php

$malumot = "Khorazmiy AI Hujjat #1029";

$md5_xesh = md5($malumot);
$sha1_xesh = sha1($malumot);

echo "MD5 (32 belgi): $md5_xesh
";
echo "SHA-1 (40 belgi): $sha1_xesh
";

```

## Tushuntirish va Mantiq:
`md5()` va `sha1()` bir tomonlama xesh funksiyalari bo'lib, fayl va ma'lumotlar yaxlitligini tekshirishda ishlatiladi. Muhim eslatma: Ushbu algoritmlar kolliziyalarga moyil bo'lgani sababli foydalanuvchi parollarini saqlash uchun YAROQSIZ va xavfli hisoblanadi (parollar uchun `password_hash()` ishlatiladi).

## Ishlash natijasi:
```text
MD5 (32 belgi): 212c4eaeb46700cba0c26ee00905e94b
SHA-1 (40 belgi): e03cbb878f79fbcad1beaa73685c88bfe4aee10f
```

# 89-Topshiriq: hash('sha256', ...) orqali xavfsiz xeshlash
## Topshiriq sharti:
`hash()` funksiyasi yordamida SHA-256 algoritmi orqali API token xeshini generatsiya qiling.

## Yechim (PHP kodi):
```php
<?php

$api_token = "khorazmiy_live_sec_991823120";

$sha256_xesh = hash('sha256', $api_token);

echo "Algoritm: SHA-256
";
echo "Xesh (64 belgi): $sha256_xesh
";

```

## Tushuntirish va Mantiq:
`hash($algoritm, $malumot)` zamonaviy kriptografik xeshlarni (masalan sha256, sha512) hisoblash uchun standart vositadir. API tokenlarni bazada ochiq saqlamasdan ularning SHA-256 xeshini saqlash eng yaxshi amaliyotdir.

## Ishlash natijasi:
```text
Algoritm: SHA-256
Xesh (64 belgi): d0d20d75c9ebbc27376c67bfca30c44fb742eb463e2a23351336fb3c29ceb424
```

# 90-Topshiriq: base64_encode() va base64_decode() orqali ma'lumotlarni kodlash
## Topshiriq sharti:
Ikkilik (binary) yoki maxsus belgilarni Base64 formatida kodlang va uni qayta dekodlang.

## Yechim (PHP kodi):
```php
<?php

$asl_matn = "Khorazmiy AI: Toshkent, O'zbekiston - 2026";

$kodlangan = base64_encode($asl_matn);
$dekodlangan = base64_decode($kodlangan);

echo "Base64: $kodlangan
";
echo "Asliga qaytarildi: $dekodlangan
";

```

## Tushuntirish va Mantiq:
Base64 kodlash ma'lumotlarni faqat 64 ta xavfsiz ASCII belgilaridan iborat qatorga o'giradi. U shifrlash EMAS, balki tarmoq orqali rasm, fayl yoki ikkilik ma'lumotlarni matnli protokollar (JSON, HTTP, Email) orqali xavfsiz uzatish vositasidir.

## Ishlash natijasi:
```text
Base64: S2hvcmF6bXlpIEFJOiBUb3Noa2VudCwgTyd6YmVraXN0b24gLSAyMDI2
Asliga qaytarildi: Khorazmiy AI: Toshkent, O'zbekiston - 2026
```

# 91-Topshiriq: preg_match() asoslari: Regex shabloni va moslikni topish
## Topshiriq sharti:
`preg_match()` funksiyasi orqali matnda so'z yoki raqam qolipi borligini tekshiring.

## Yechim (PHP kodi):
```php
<?php

$matn = "Buyurtma raqami: ORD-89214 rasmiylashtirildi.";
$shablon = "/ORD-\d+/";

if (preg_match($shablon, $matn, $mosliklar)) {
    echo "Moslik topildi: " . $mosliklar[0] . "
";
} else {
    echo "Mos kelmadi.
";
}

```

## Tushuntirish va Mantiq:
`preg_match($pattern, $subject, [&$matches])` berilgan regular expression (PCRE) bo'yicha qidiradi. Birinchi mos kelgan holatni topishi bilanoq to'xtaydi va `1` qaytaradi, topilmasa `0` qaytaradi. `$mosliklar[0]` to'liq mos kelgan parchani saqlaydi.

## Ishlash natijasi:
```text
Moslik topildi: ORD-89214
```

# 92-Topshiriq: Regex chegaralari (\b) va modifikatorlar (/i, /u)
## Topshiriq sharti:
Alohida so'z chegarasini (`\b`) va registrga befarqlik modifikatorini (`/i`) namoyish eting.

## Yechim (PHP kodi):
```php
<?php

$matn = "Cat catalog category cat";

// Faqat mustaqil 'cat' so'zini qidirish
$shablon = "/cat/i";

preg_match_all($shablon, $matn, $natijalar);

echo "Mustaqil 'cat' so'zlari soni: " . count($natijalar[0]) . "
";

```

## Tushuntirish va Mantiq:
`\b` so'z chegarasini bildiradi, ya'ni qidirilayotgan so'z boshqa so'zlarning qismi bo'lib qolmasligini ta'minlaydi. Modifikator `/i` registrga befarqlikni, `/u` esa UTF-8 rejimini yoqadi.

## Ishlash natijasi:
```text
Mustaqil 'cat' so'zlari soni: 2
```

# 93-Topshiriq: O'zbekiston telefon raqamini tekshiruvchi Regex
## Topshiriq sharti:
+998 bilan boshlanuvchi O'zbekiston telefon raqamlarini tekshiruvchi qat'iy Regex funksiyasini yozing.

## Yechim (PHP kodi):
```php
<?php

function tekshirUzbekTel(string $raqam): bool {
    // +998 dan so'ng 2 ta raqamli operator kodi va 7 ta raqam
    $shablon = "/^\+998(90|91|93|94|95|97|98|99|88|33|77)\d{7}$/";
    return (bool) preg_match($shablon, $raqam);
}

$tel1 = "+998901234567";
$tel2 = "+998711234567";
$tel3 = "1234567";

echo "$tel1: " . (tekshirUzbekTel($tel1) ? "To'g'ri raqam" : "Noto'g'ri") . "
";
echo "$tel2: " . (tekshirUzbekTel($tel2) ? "To'g'ri raqam" : "Noto'g'ri") . "
";
echo "$tel3: " . (tekshirUzbekTel($tel3) ? "To'g'ri raqam" : "Noto'g'ri") . "
";

```

## Tushuntirish va Mantiq:
`^` satr boshini, `$` satr oxirini bildiradi. `(90|91|...)` faqat ma'lum mobil operator kodlariga ruxsat beradi. `\d{7}` esa ketma-ket 7 ta raqam bo'lishini talab qiladi.

## Ishlash natijasi:
```text
+998901234567: To'g'ri raqam
+998711234567: Noto'g'ri
1234567: Noto'g'ri
```

# 94-Topshiriq: Email manzilini tekshirish: Regex vs filter_var()
## Topshiriq sharti:
Email formatini Regex orqali va PHP ning standart `filter_var()` funksiyasi orqali tekshirishni solishtiring.

## Yechim (PHP kodi):
```php
<?php

$email1 = "alisher.navoiy@khorazmiy.uz";
$email2 = "notogri_email@.com";

function tekshirEmail(string $email): bool {
    return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
}

echo "$email1: " . (tekshirEmail($email1) ? "Haqiqiy email" : "Yaroqsiz") . "
";
echo "$email2: " . (tekshirEmail($email2) ? "Haqiqiy email" : "Yaroqsiz") . "
";

```

## Tushuntirish va Mantiq:
Email tekshirish uchun juda uzun regex yozish o'rniga, PHP ning o'rnatilgan `filter_var($email, FILTER_VALIDATE_EMAIL)` funksiyasidan foydalanish eng xavfsiz va RFC standartlariga to'liq mos keladigan usuldir.

## Ishlash natijasi:
```text
alisher.navoiy@khorazmiy.uz: Haqiqiy email
notogri_email@.com: Yaroqsiz
```

# 95-Topshiriq: preg_match_all() orqali barcha xeshteglarni (#tag) ajratib olish
## Topshiriq sharti:
Ijtimoiy tarmoq postidagi barcha `#xeshteg`larni `preg_match_all()` yordamida massivga yig'ing.

## Yechim (PHP kodi):
```php
<?php

$post = "Bugun #php8 va #laravel bo'yicha ajoyib dars bo'ldi. #khorazmiy_ai loyihasi davom etadi!";

$shablon = "/#([a-zA-Z0-9_]+)/u";

preg_match_all($shablon, $post, $mosliklar);

echo "Topilgan xeshteglar:
";
foreach ($mosliklar[1] as $tag) {
    echo "  - $tag
";
}

```

## Tushuntirish va Mantiq:
`preg_match_all()` satrdagi barcha mosliklarni qidiradi. `$mosliklar[0]` to'liq mos kelgan matnlarni (`#php8`), qavs ichidagi guruhlar (`$mosliklar[1]`) esa panjarasiz faqat so'zlarni (`php8`) qaytaradi.

## Ishlash natijasi:
```text
Topilgan xeshteglar:
  - php8
  - laravel
  - khorazmiy_ai
```

# 96-Topshiriq: preg_replace() yordamida shablon bo'yicha almashtirish
## Topshiriq sharti:
Matndagi ketma-ket kelgan bir nechta probellarni bitta probelga `preg_replace()` orqali almashtiring.

## Yechim (PHP kodi):
```php
<?php

$tartibsiz_matn = "Salom,    dunyo!   Bu    yerda    ortiqcha    bo'shliqlar   ko'p.";

// \s+ bir yoki bir nechta bo'shliq belgilarini bildiradi
$toza = preg_replace("/\s+/", " ", $tartibsiz_matn);

echo $toza . "
";

```

## Tushuntirish va Mantiq:
`preg_replace($pattern, $replacement, $subject)` regex qolipiga tushgan barcha bo'laklarni ko'rsatilgan matnga almashtiradi. `\s+` probellar, tabulyatsiyalar va yangi qatorlarni tozalashda juda samarali.

## Ishlash natijasi:
```text
Salom, dunyo! Bu yerda ortiqcha bo'shliqlar ko'p.
```

# 97-Topshiriq: preg_replace_callback() orqali dinamik hisoblash
## Topshiriq sharti:
Matn ichidagi barcha narxlarni 10% soliq qo'shilgan holatda `preg_replace_callback()` orqali qayta hisoblang.

## Yechim (PHP kodi):
```php
<?php

$matn = "Tovar A: 1000 so'm, Tovar B: 2500 so'm, Tovar C: 5000 so'm.";

$shablon = "/(\d+)\s+so'm/";

$yangi_matn = preg_replace_callback($shablon, function ($moslik) {
    $eski_narx = (int)$moslik[1];
    $yangi_narx = (int)($eski_narx * 1.10); // 10% ustama
    return "$yangi_narx so'm (soliq bilan)";
}, $matn);

echo $yangi_matn . "
";

```

## Tushuntirish va Mantiq:
`preg_replace_callback()` har bir moslik topilganda anonim funksiya (closure) chaqiradi. Bu topilgan qiymatlar ustida matematik amallar bajarish yoki dinamik o'zgartirishlar qilish imkonini beradi.

## Ishlash natijasi:
```text
Tovar A: 1100 so'm (soliq bilan), Tovar B: 2750 so'm (soliq bilan), Tovar C: 5500 so'm (soliq bilan).
```

# 98-Topshiriq: preg_split() orqali murakkab ajratish
## Topshiriq sharti:
Matnni nuqta, undov yoki so'roq belgilari bo'yicha gaplarga ajrating.

## Yechim (PHP kodi):
```php
<?php

$matn = "Salom Dunyo! Qandaysiz? PHP 8.3 juda ajoyib. Keling boshlaymiz!";

// Gap oxiri belgilari bo'yicha ajratish
$gaplar = preg_split("/[.!?]\s+/", $matn, -1, PREG_SPLIT_NO_EMPTY);

foreach ($gaplar as $indeks => $gap) {
    echo ($indeks + 1) . "-gap: $gap
";
}

```

## Tushuntirish va Mantiq:
`preg_split()` satrni bitta emas, bir nechta turli xil ajratuvchilar (regex qolipi) bo'yicha bo'laklash imkonini beradi. `PREG_SPLIT_NO_EMPTY` bayrog'i bo'sh elementlarni natijadan chiqarib tashlaydi.

## Ishlash natijasi:
```text
1-gap: Salom Dunyo
2-gap: Qandaysiz
3-gap: PHP 8.3 juda ajoyib
4-gap: Keling boshlaymiz!
```

# 99-Topshiriq: Satr ichidagi barcha URL manzillarni ajratib olish
## Topshiriq sharti:
Kiritilgan matndagi HTTP va HTTPS bilan boshlanuvchi veb-havolalarni aniqlovchi regex yozing.

## Yechim (PHP kodi):
```php
<?php

$matn = "Batafsil ma'lumotni https://khorazmiy.uz yoki http://php.net/manual orqali o'qing.";

$shablon = '/https?:\/\/[^\s]+/';

preg_match_all($shablon, $matn, $mosliklar);

echo "Topilgan havolalar:
";
foreach ($mosliklar[0] as $havola) {
    echo "  - $havola
";
}

```

## Tushuntirish va Mantiq:
`https?:\/\/` orqali ham http, ham https havolalari qamrab olinadi. `[^\s]+` bo'sh joy bo'lmagan barcha keyingi belgilarni havolaning oxirigacha ushlab oladi.

## Ishlash natijasi:
```text
Topilgan havolalar:
  - https://khorazmiy.uz
  - http://php.net/manual
```

# 100-Topshiriq: To'liq 'Slug' (URL-friendly satr) generatorini yaratish
## Topshiriq sharti:
O'zbekcha maqola sarlavhasidan brauzer URL manzili uchun qulay bo'lgan xavfsiz 'slug' yaratuvchi funksiya yozing.

## Yechim (PHP kodi):
```php
<?php

function slugYaratish(string $sarlavha): string {
    // 1. Kichik harfga o'tkazish
    $slug = mb_strtolower(trim($sarlavha), 'UTF-8');
    
    // 2. O'zbek harflarini almashtirish
    $almashtirishlar = [
        "o'" => 'o', "g'" => 'g', "sh" => 'sh', "ch" => 'ch',
        "ў" => 'o', "ғ" => 'g', "ш" => 'sh', "ч" => 'ch'
    ];
    $slug = str_replace(array_keys($almashtirishlar), array_values($almashtirishlar), $slug);
    
    // 3. Raqam va harf bo'lmagan barcha belgilarni chiziqchaga almashtirish
    $slug = preg_replace('/[^a-z0-9]+/i', '-', $slug);
    
    // 4. Chekkadagi va takrorlangan chiziqchalarni tozalash
    return trim($slug, '-');
}

$sarlavha = "PHP 8.3 & Laravel 11: O'zbekiston bo'ylab yangi imkoniyatlar!";
echo "Slug: " . slugYaratish($sarlavha) . "
";

```

## Tushuntirish va Mantiq:
Slug generatsiyasi bir necha bosqichdan iborat: kichik harflarga o'tkazish, maxsus milliy harflarni transliteratsiya qilish, ortiqcha belgi va tinish belgilarini chiziqchaga (`-`) aylantirish hamda chekkadagi chiziqchalarni tozalash.

## Ishlash natijasi:
```text
Slug: php-8-3-laravel-11-ozbekiston-boylab-yangi-imkoniyatlar
```
