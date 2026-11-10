# 4-Mavzu: Funksiyalar va Anonim Closures (151-200)

Ushbu bo'limda PHP tilida funksional dasturlash imkoniyatlari, tiplash tizimi, qamrov doiralari hamda ilg'or mexanizmlar to'liq ochib berilgan:
Funksiyalar va qaytarish tiplari (`void`, `never`, `nullable`, `union`), o'zgaruvchilar skopi (`global`, `static`), parametr uzatish (qiymat va havola `&$var`), variadic parametrlar (`...$args`), PHP 8 nomlangan argumentlar, rekursiv funksiyalar va stack overflow nazorati, anonim funksiyalar (Closures), `use` kalit so'zi, qisqa o'qli funksiyalar (Arrow functions: `fn() => ...`), `Closure::bindTo`, PHP 8.1 First-class callables (`strlen(...)`), Yuqori tartibli funksiyalar (Higher-Order Functions), Pipeline va Currying naqshlari, generatorlar va xotira tejamkorligi (`yield`, `yield from`), Event Dispatcher, Retry mexanizmi hamda funksiya profilini o'lchash bo'yicha 50 ta amaliy topshiriq jamlangan.

---

# 151-Topshiriq: Funksiya ta'rifi, parametrlar va return operatori
## Topshiriq sharti:
Ikkita sonning ko'paytmasini hisoblab qaytaruvchi oddiy funksiya yozing.

## Yechim (PHP kodi):
```php
<?php

function kopaytma(float $a, float $b): float {
    return $a * $b;
}

$natija = kopaytma(4.5, 2.0);
echo "Natija: $natija
";

```

## Tushuntirish va Mantiq:
Funksiya `function nom(...)` sintaksisi bilan e'lon qilinadi. `return` operatori funksiya bajarilishini to'xtatadi va natijaviy qiymatni uni chaqirgan kodga qaytaradi.

## Ishlash natijasi:
```text
Natija: 9
```

# 152-Topshiriq: Standart (default) parametr qiymatlari
## Topshiriq sharti:
Foydalanuvchiga salom beruvchi, agar ism berilmasa 'Mehmon' deb murojaat qiluvchi funksiya tuzing.

## Yechim (PHP kodi):
```php
<?php

function salomlash(string $ism = "Mehmon"): string {
    return "Assalomu alaykum, $ism!";
}

echo salomlash("Kamron") . "
";
echo salomlash() . "
";

```

## Tushuntirish va Mantiq:
Parametrga tenglik belgisi bilan birlamchi qiymat berilsa (`$ism = 'Mehmon'`), funksiya chaqirilganda ushbu argument kiritilmasa sukut bo'yicha shu qiymat ishlatiladi.

## Ishlash natijasi:
```text
Assalomu alaykum, Kamron!
Assalomu alaykum, Mehmon!
```

# 153-Topshiriq: Default parametrlarning joylashuv tartibi
## Topshiriq sharti:
PHP 8 qoidalariga binoan ixtiyoriy (default) parametrlarni majburiy parametrlardan keyin joylashtirishni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

// To'g'ri tartib: majburiy parametrlar boshida, default parametrlar oxirida
function formatHisob(string $mijoz, float $summa, string $valyuta = "UZS"): string {
    return "$mijoz: " . number_format($summa) . " $valyuta";
}

echo formatHisob("Alisher Navoiy", 2500000) . "
";
echo formatHisob("John Doe", 300, "USD") . "
";

```

## Tushuntirish va Mantiq:
PHP 8 dan boshlab ixtiyoriy parametr majburiy parametrdan oldin qo'yilsa, `Deprecated` ogohlantirishi beriladi. Barcha ixtiyoriy (default qiymatli) parametrlar ro'yxat oxirida bo'lishi shart.

## Ishlash natijasi:
```text
Alisher Navoiy: 2,500,000 UZS
John Doe: 300 USD
```

# 154-Topshiriq: declare(strict_types=1) va qat'iy tiplash
## Topshiriq sharti:
Qat'iy tiplash yoqilgan faylda funksiya parametrlari va qaytaruvchi tipining aniqligini ta'minlang.

## Yechim (PHP kodi):
```php
<?php

declare(strict_types=1);

function bolish(int $bolinuvchi, int $boluvchi): float {
    return $bolinuvchi / $boluvchi;
}

echo "Bo'linma: " . bolish(10, 4) . "
";

```

## Tushuntirish va Mantiq:
`declare(strict_types=1)` rejimida PHP avtomatik tur konvertatsiyasini bekor qiladi. Argumentlar e'lon qilingan tur bilan 100% mos kelishi kerak, aks holda `TypeError` yuzaga keladi.

## Ishlash natijasi:
```text
Bo'linma: 2.5
```

# 155-Topshiriq: void qaytarish tipi
## Topshiriq sharti:
Hech qanday qiymat qaytarmaydigan, faqat ekranga log xabarlarini chiqaruvchi `void` funksiya yozing.

## Yechim (PHP kodi):
```php
<?php

function tizimXabari(string $xabar): void {
    echo "[LOG " . date("H:i") . "] $xabar
";
    // void funksiyada faqat bo'sh 'return;' bo'lishi mumkin, qiymat qaytarib bo'lmaydi
}

tizimXabari("Foydalanuvchi tizimga kirdi");

```

## Tushuntirish va Mantiq:
`void` funksiyaning hech qanday qiymat qaytarmasligini kafolatlaydi. Agar `void` funksiyada `return 123;` deb yozilsa, PHP kompilyatsiya xatosini chiqaradi.

## Ishlash natijasi:
```text
[LOG 16:40] Foydalanuvchi tizimga kirdi
```

# 156-Topshiriq: never qaytarish tipi (PHP 8.1)
## Topshiriq sharti:
PHP 8.1 ning `never` tipi yordamida dasturni to'xtatuvchi yoki istisno tashlovchi yordamchi funksiya yarating.

## Yechim (PHP kodi):
```php
<?php

function xatolikBilanTugatish(string $sabab): never {
    throw new RuntimeException("Kritik xatolik: $sabab");
}

try {
    xatolikBilanTugatish("Ma'lumotlar bazasi bilan aloqa uzildi");
} catch (RuntimeException $e) {
    echo $e->getMessage() . "
";
}

```

## Tushuntirish va Mantiq:
`never` tipi funksiyaning hech qachon normal yakunlanmasligini (yo `exit()`, yo `throw Exception` orqali to'xtashini) bildiradi. Statik tahlil vositalari (PHPStan, Psalm) uchun muhim belgidir.

## Ishlash natijasi:
```text
Kritik xatolik: Ma'lumotlar bazasi bilan aloqa uzildi
```

# 157-Topshiriq: Nullable tiplar (?string, ?int)
## Topshiriq sharti:
Parametr yoki natija qiymati `null` bo'lishi mumkin bo'lgan holatlarni `?` prefiksi orqali ifodalang.

## Yechim (PHP kodi):
```php
<?php

function qidirFoydalanuvchi(int $id): ?string {
    $foydalanuvchilar = [1 => "Sardor", 2 => "Malika"];
    return $foydalanuvchilar[$id] ?? null;
}

$natija1 = qidirFoydalanuvchi(1);
$natija2 = qidirFoydalanuvchi(99);

echo "1-foydalanuvchi: " . ($natija1 ?? "Topilmadi") . "
";
echo "99-foydalanuvchi: " . ($natija2 ?? "Topilmadi") . "
";

```

## Tushuntirish va Mantiq:
`?string` yoki `?int` tipi qiymat ko'rsatilgan turda bo'lishi yoki `null` bo'lishi mumkinligini bildiradi. Bu `string|null` yozuvining qisqartmasidir.

## Ishlash natijasi:
```text
1-foydalanuvchi: Sardor
99-foydalanuvchi: Topilmadi
```

# 158-Topshiriq: Union tiplar (PHP 8.0)
## Topshiriq sharti:
PHP 8.0 ning `Union Types` imkoniyatidan foydalanib, bir nechta tiplarni (`int|float`, `string|array`) qabul qiluvchi funksiya tuzing.

## Yechim (PHP kodi):
```php
<?php

function foizHisobla(int|float $summa, int|float $foiz): int|float {
    return ($summa * $foiz) / 100;
}

echo "Hisob 1: " . foizHisobla(1000, 15) . "
";
echo "Hisob 2: " . foizHisobla(250.5, 10.5) . "
";

```

## Tushuntirish va Mantiq:
Union tiplar vertikal chiziqcha (`|`) orqali birlashtiriladi. Bu funksiyaga bir nechta belgilangan turdagi ma'lumotlarni xavfsiz uzatish imkonini beradi.

## Ishlash natijasi:
```text
Hisob 1: 150
Hisob 2: 26.3025
```

# 159-Topshiriq: O'zgaruvchilar skopi: Lokal va global o'zgaruvchilar
## Topshiriq sharti:
Funksiya tashqarisidagi va ichkarisidagi o'zgaruvchilarning bir-biridan ajratilganligini namoyish eting.

## Yechim (PHP kodi):
```php
<?php

$x = 50; // Global o'zgaruvchi

function sinov(): void {
    $x = 100; // Lokal o'zgaruvchi
    echo "Funksiya ichidagi x: $x
";
}

sinov();
echo "Funksiya tashqarisidagi x: $x
";

```

## Tushuntirish va Mantiq:
Funksiya ichida e'lon qilingan o'zgaruvchilar lokal hisoblanadi va faqat funksiya ishlash vaqtida mavjud bo'ladi. Ular tashqi global o'zgaruvchilar bilan to'qnashmaydi.

## Ishlash natijasi:
```text
Funksiya ichidagi x: 100
Funksiya tashqarisidagi x: 50
```

# 160-Topshiriq: global kalit so'zi va $GLOBALS superglobal massivi
## Topshiriq sharti:
Funksiya ichidan tashqi global o'zgaruvchiga kirish va uni o'zgartirishni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

$hisoblagich = 10;

function oshir(): void {
    global $hisoblagich;
    $hisoblagich++;
}

function oshirGlobalsOrqali(): void {
    $GLOBALS['hisoblagich'] += 5;
}

oshir();
oshirGlobalsOrqali();

echo "Yakuniy hisoblagich: $hisoblagich
";

```

## Tushuntirish va Mantiq:
`global $var` kalit so'zi funksiya ichida tashqi o'zgaruvchiga havola yaratadi. `$GLOBALS['var']` assotsiativ massivi esa barcha global o'zgaruvchilarni o'z ichiga oladi.

## Ishlash natijasi:
```text
Yakuniy hisoblagich: 16
```

# 161-Topshiriq: static o'zgaruvchilar: Funksiya xotirasini saqlash
## Topshiriq sharti:
`static` o'zgaruvchi yordamida funksiya necha marta chaqirilganini sanovchi hisoblagich yarating.

## Yechim (PHP kodi):
```php
<?php

function tashrifSanagich(): int {
    static $soni = 0;
    $soni++;
    return $soni;
}

echo "1-chaqiriq: " . tashrifSanagich() . "
";
echo "2-chaqiriq: " . tashrifSanagich() . "
";
echo "3-chaqiriq: " . tashrifSanagich() . "
";

```

## Tushuntirish va Mantiq:
`static` lokal o'zgaruvchi faqat birinchi chaqiriqda initsializatsiya qilinadi va funksiya yakunlangandan keyin ham o'z qiymatini xotirada saqlab qoladi.

## Ishlash natijasi:
```text
1-chaqiriq: 1
2-chaqiriq: 2
3-chaqiriq: 3
```

# 162-Topshiriq: Argumentlarni qiymat bo'yicha uzatish (Pass by value)
## Topshiriq sharti:
Standart holatda parametrlar qiymat bo'yicha uzatilganda asl o'zgaruvchining o'zgarmasligini isbotlang.

## Yechim (PHP kodi):
```php
<?php

function ikkiBarobar(int $son): int {
    $son *= 2;
    return $son;
}

$asl = 15;
$natija = ikkiBarobar($asl);

echo "Funksiya natijasi: $natija
";
echo "Asl o'zgaruvchi qiymati: $asl
";

```

## Tushuntirish va Mantiq:
PHP da skalyar tiplar sukut bo'yicha qiymat nusxasi (by value) orqali uzatiladi. Funksiya ichidagi amallar asl o'zgaruvchiga mutlaqo ta'sir qilmaydi.

## Ishlash natijasi:
```text
Funksiya natijasi: 30
Asl o'zgaruvchi qiymati: 15
```

# 163-Topshiriq: Argumentlarni havola bo'yicha uzatish (Pass by reference: &$var)
## Topshiriq sharti:
Parametr oldiga `&` belgisini qo'yish orqali asl o'zgaruvchini bevosita funksiya ichida o'zgartiring.

## Yechim (PHP kodi):
```php
<?php

function qoshBonus(int &$balans, int $bonus): void {
    $balans += $bonus;
}

$foydalanuvchi_balansi = 50000;
qoshBonus($foydalanuvchi_balansi, 15000);

echo "Yangi balans: $foydalanuvchi_balansi so'm
";

```

## Tushuntirish va Mantiq:
`&$param` yozuvi argumentni havola bo'yicha qabul qiladi. Bu funksiyaga o'zgaruvchining xotiradagi manziliga to'g'ridan-to'g'ri o'zgartirish kiritish imkonini beradi.

## Ishlash natijasi:
```text
Yangi balans: 65000 so'm
```

# 164-Topshiriq: Variadic funksiyalar: ...$param (Ixtiyoriy sondagi parametrlar)
## Topshiriq sharti:
`...` (splat) operatori yordamida ixtiyoriy miqdordagi sonlarni qabul qilib, ularning o'rtacha qiymatini hisoblovchi funksiya yozing.

## Yechim (PHP kodi):
```php
<?php

function ortacha(float ...$sonlar): float {
    if (empty($sonlar)) {
        return 0.0;
    }
    return array_sum($sonlar) / count($sonlar);
}

echo "O'rtacha (3 ta son): " . ortacha(10, 20, 30) . "
";
echo "O'rtacha (5 ta son): " . ortacha(4, 8, 15, 16, 23) . "
";

```

## Tushuntirish va Mantiq:
`...$sonlar` parametri funksiyaga uzatilgan barcha qolgan argumentlarni bitta massivga yig'ib beradi. Bu funksiyaga cheksiz miqdorda argument uzatish imkonini yaratadi.

## Ishlash natijasi:
```text
O'rtacha (3 ta son): 20
O'rtacha (5 ta son): 13.2
```

# 165-Topshiriq: Argumentlarni yoyish (Argument unpacking: ...$massiv)
## Topshiriq sharti:
Massivdagi qiymatlarni funksiyaga `...` operatori orqali alohida argumentlar ko'rinishida yoyib uzating.

## Yechim (PHP kodi):
```php
<?php

function uchburchakYuzi(float $a, float $b, float $c): float {
    $p = ($a + $b + $c) / 2;
    return sqrt($p * ($p - $a) * ($p - $b) * ($p - $c));
}

$tomonlar = [3.0, 4.0, 5.0];
$yuza = uchburchakYuzi(...$tomonlar);

echo "Uchburchak yuzi: $yuza
";

```

## Tushuntirish va Mantiq:
Funksiya chaqiruvida `...$massiv` ishlatilsa, massiv elementlari ajratilib, funksiya parametrlariga ketma-ket uzatiladi.

## Ishlash natijasi:
```text
Uchburchak yuzi: 6
```

# 166-Topshiriq: PHP 8 Nomlangan argumentlar (Named arguments)
## Topshiriq sharti:
PHP 8 ning nomlangan argumentlaridan foydalanib funksiyaga parametrlarni istalgan tartibda uzating.

## Yechim (PHP kodi):
```php
<?php

function profilYaratish(string $ism, int $yosh, string $shahar = "Toshkent", bool $faol = true): void {
    echo "Profil: $ism, $yosh yosh, Shahar: $shahar, Status: " . ($faol ? "Faol" : "Nofaol") . "
";
}

// Parametr nomlarini aniq ko'rsatib, tartibni o'zgartirib chaqiramiz:
profilYaratish(
    yosh: 26,
    ism: "Javlon",
    faol: false
);

```

## Tushuntirish va Mantiq:
PHP 8 da argument nomini `param_nomi: qiymat` ko'rinishida yozish mumkin. Bu kodning o'qilishini nihoyatda osonlashtiradi va parametrlarning joylashuv tartibiga bog'liqlikni yo'qotadi.

## Ishlash natijasi:
```text
Profil: Javlon, 26 yosh, Shahar: Toshkent, Status: Nofaol
```

# 167-Topshiriq: Nomlangan argumentlar bilan oraliq parametrlarni tashlab o'tish
## Topshiriq sharti:
Funksiyaning o'rtadagi default parametrlarini o'zgartirmasdan, faqat eng oxirgi parametrini nomlangan argument orqali yangilang.

## Yechim (PHP kodi):
```php
<?php

function cookieYarat(string $nom, string $qiymat, int $muddati = 3600, string $path = "/", bool $httponly = true): void {
    echo "Cookie yaratildi: $nom=$qiymat; muddati: $muddati; httponly: " . ($httponly ? 'ha' : 'yoq') . "
";
}

// Faqat $nom, $qiymat va eng oxirgi $httponly ni o'zgartiramiz
cookieYarat("session_token", "abc123xyz", httponly: false);

```

## Tushuntirish va Mantiq:
Nomlangan argumentlar orqali default qiymatga ega bo'lgan o'rtadagi bir nechta parametrlarni qayta yozmasdan to'g'ridan-to'g'ri faqat kerakli parametrni o'zgartirish mumkin.

## Ishlash natijasi:
```text
Cookie yaratildi: session_token=abc123xyz; muddati: 3600; httponly: yoq
```

# 168-Topshiriq: O'zgaruvchan funksiyalar (Variable functions)
## Topshiriq sharti:
Funksiya nomini satr o'zgaruvchisida saqlab, dinamik ravishda chaqirishni amalga oshiring.

## Yechim (PHP kodi):
```php
<?php

function salomUzb(): string {
    return "Assalomu alaykum!";
}

function salomEng(): string {
    return "Hello World!";
}

$tanlangan_til = "Uzb";
$funksiya_nomi = "salom" . $tanlangan_til;

echo $funksiya_nomi() . "
";

```

## Tushuntirish va Mantiq:
PHP da agar o'zgaruvchi nomidan keyin qavslar `()` qo'yilsa, PHP shu nomdagi funksiyani topadi va ishga tushiradi. Dinamik marshrutlash va dispetcherlarda keng qo'llaniladi.

## Ishlash natijasi:
```text
Assalomu alaykum!
```

# 169-Topshiriq: function_exists() orqali dinamik tekshiruv
## Topshiriq sharti:
Funksiyani chaqirishdan oldin uning mavjudligini xavfsiz tekshiruvchi mexanizm tuzing.

## Yechim (PHP kodi):
```php
<?php

function modulFaol(): bool {
    return true;
}

$fn = "modulFaol";

if (function_exists($fn)) {
    echo "Funksiya mavjud va chaqirildi: " . ($fn() ? "Faol" : "Nofaol") . "
";
} else {
    echo "Bunday funksiya topilmadi!
";
}

```

## Tushuntirish va Mantiq:
`function_exists($nom)` berilgan nomdagi funksiya dastur xotirasida e'lon qilingan yoki yuklanganligini tekshiradi.

## Ishlash natijasi:
```text
Funksiya mavjud va chaqirildi: Faol
```

# 170-Topshiriq: Rekursiv funksiyalar: Faktorial hisoblash
## Topshiriq sharti:
Matematik faktorialni (n!) rekursiv funksiya orqali hisoblang.

## Yechim (PHP kodi):
```php
<?php

function faktorial(int $n): int {
    if ($n <= 1) {
        return 1; // Rekursiyadan chiqish sharti (base case)
    }
    return $n * faktorial($n - 1);
}

echo "5! = " . faktorial(5) . "
";
echo "6! = " . faktorial(6) . "
";

```

## Tushuntirish va Mantiq:
Rekursiv funksiya o'zini-o'zi chaqiruvchi funksiyadir. Har qanday rekursiyada cheksiz chaqiruvga tushib qolmaslik uchun to'xtash sharti (base case) bo'lishi shart.

## Ishlash natijasi:
```text
5! = 120
6! = 720
```

# 171-Topshiriq: Rekursiv funksiyalar: Fibonachchi ketma-ketligi
## Topshiriq sharti:
Rekursiya orqali n-Fibonachchi sonini aniqlovchi funksiya yozing.

## Yechim (PHP kodi):
```php
<?php

function fibonachchi(int $n): int {
    if ($n === 0) return 0;
    if ($n === 1) return 1;
    return fibonachchi($n - 1) + fibonachchi($n - 2);
}

for ($i = 0; $i <= 7; $i++) {
    echo fibonachchi($i) . " ";
}
echo "
";

```

## Tushuntirish va Mantiq:
Fibonachchi ketma-ketligida har bir son o'zidan oldingi ikkita sonning yig'indisiga teng: F(n) = F(n-1) + F(n-2).

## Ishlash natijasi:
```text
0 1 1 2 3 5 8 13 
```

# 172-Topshiriq: Rekursiv funksiyalar: Chuqur ierarxik daraxtni aylanib chiqish
## Topshiriq sharti:
Kategoriyalar va ularning ichki bo'limlaridan iborat daraxtsimon massivni rekursiv chop etuvchi funksiya tuzing.

## Yechim (PHP kodi):
```php
<?php

$kategoriyalar = [
    [
        "nom" => "Elektronika",
        "bolimlar" => [
            ["nom" => "Telefonlar", "bolimlar" => []],
            ["nom" => "Noutbuklar", "bolimlar" => []]
        ]
    ],
    [
        "nom" => "Kitoblar",
        "bolimlar" => []
    ]
];

function chopEtDaraxt(array $daraxt, int $chuqurlik = 0): void {
    foreach ($daraxt as $element) {
        echo str_repeat("  ", $chuqurlik) . "- " . $element["nom"] . "
";
        if (!empty($element["bolimlar"])) {
            chopEtDaraxt($element["bolimlar"], $chuqurlik + 1);
        }
    }
}

chopEtDaraxt($kategoriyalar);

```

## Tushuntirish va Mantiq:
Cheksiz chuqurlikdagi daraxtlar, menyular va kataloglar strukturasini qayta ishlashda rekursiya eng samarali usul hisoblanadi.

## Ishlash natijasi:
```text
- Elektronika
  - Telefonlar
  - Noutbuklar
- Kitoblar
```

# 173-Topshiriq: Rekursiya chuqurligi va stack overflow xavfini nazorat qilish
## Topshiriq sharti:
Rekursiya maksimal chuqurlikka yetganda xatolik beruvchi himoyalangan qolip yozing.

## Yechim (PHP kodi):
```php
<?php

function xavfsizRekursiya(int $bosqich, int $max = 5): void {
    if ($bosqich > $max) {
        throw new OverflowException("Maksimal rekursiya chuqurligidan oshib ketdi ($max)!");
    }
    echo "Bosqich: $bosqich
";
    xavfsizRekursiya($bosqich + 1, $max);
}

try {
    xavfsizRekursiya(1, 3);
} catch (OverflowException $e) {
    echo "Ushlandi: " . $e->getMessage() . "
";
}

```

## Tushuntirish va Mantiq:
PHP da juda chuqur rekursiya xotiraning to'lib ketishiga (call stack exhaustion) olib keladi. Har doim chegaralarni belgilash kutilmagan qulashlarning oldini oladi.

## Ishlash natijasi:
```text
Bosqich: 1
Bosqich: 2
Bosqich: 3
Ushlandi: Maksimal rekursiya chuqurligidan oshib ketdi (3)!
```

# 174-Topshiriq: Shartli e'lon qilinadigan funksiyalar (Conditional functions)
## Topshiriq sharti:
Shart bajarilgandagina tizimda e'lon qilinadigan funksiyani ko'rsating.

## Yechim (PHP kodi):
```php
<?php

$muhit = "debug";

if ($muhit === "debug") {
    function logTahlil(string $msg): void {
        echo "[DEBUG]: $msg
";
    }
}

if (function_exists("logTahlil")) {
    logTahlil("Tizim sozlamalari tekshirildi");
}

```

## Tushuntirish va Mantiq:
PHP da funksiyalar `if` bloki ichida e'lon qilinishi mumkin, ammo ular faqat o'sha shart bajarilib blok ichiga kirilgandan so'nggina global xotirada paydo bo'ladi.

## Ishlash natijasi:
```text
[DEBUG]: Tizim sozlamalari tekshirildi
```

# 175-Topshiriq: Anonim funksiyalar (Closures) asoslari
## Topshiriq sharti:
Nomsiz funksiya (Closure) yaratib, uni boshqa funksiyaga argument sifatida uzating.

## Yechim (PHP kodi):
```php
<?php

$kvadrat_oluvchi = function (int $x): int {
    return $x * $x;
};

echo "7 ning kvadrati: " . $kvadrat_oluvchi(7) . "
";

```

## Tushuntirish va Mantiq:
Anonim funksiya hech qanday nomga ega bo'lmagan funksiyadir. U `Closure` sinfining obyekti sifatida saqlanadi va oddiy o'zgaruvchi kabi uzatilishi mumkin.

## Ishlash natijasi:
```text
7 ning kvadrati: 49
```

# 176-Topshiriq: Anonim funksiyani o'zgaruvchiga o'zlashtirish va chaqirish
## Topshiriq sharti:
Assotsiativ massivda har xil amallarni bajaruvchi anonim funksiyalar kolleksiyasini yarating.

## Yechim (PHP kodi):
```php
<?php

$kalkulyator = [
    "qoshish" => function ($a, $b) { return $a + $b; },
    "ayirish" => function ($a, $b) { return $a - $b; },
    "kopaytirish" => function ($a, $b) { return $a * $b; }
];

echo "10 + 5 = " . $kalkulyator["qoshish"](10, 5) . "
";
echo "10 * 5 = " . $kalkulyator["kopaytirish"](10, 5) . "
";

```

## Tushuntirish va Mantiq:
Massivlar ichida funksiyalarni saqlash strategiya naqshini (Strategy pattern) juda sodda va toza amalga oshirish imkonini beradi.

## Ishlash natijasi:
```text
10 + 5 = 15
10 * 5 = 50
```

# 177-Topshiriq: use kalit so'zi orqali tashqi o'zgaruvchilarni qamrab olish
## Topshiriq sharti:
Tashqi o'zgaruvchini `use ($valyuta)` orqali anonim funksiya ichiga olib kiring.

## Yechim (PHP kodi):
```php
<?php

$valyuta = "UZS";

$narxFormatlovchi = function (float $summa) use ($valyuta): string {
    return number_format($summa) . " " . $valyuta;
};

echo $narxFormatlovchi(450000) . "
";

```

## Tushuntirish va Mantiq:
Anonim funksiyalar o'z skopidan tashqaridagi o'zgaruvchilarni to'g'ridan-to'g'ri ko'rmaydi. `use ($o'zgaruvchi)` sintaksisi tashqi o'zgaruvchining qiymatini funksiya yaratilish vaqtida uning ichki qamroviga (closure context) biriktiradi.

## Ishlash natijasi:
```text
450,000 UZS
```

# 178-Topshiriq: use orqali tashqi o'zgaruvchini havola bo'yicha (&) o'zgartirish
## Topshiriq sharti:
Closure chaqirilganda tashqi hisoblagichni `use (&$sanagich)` orqali oshirib boring.

## Yechim (PHP kodi):
```php
<?php

$sanagich = 0;

$qadam = function () use (&$sanagich): void {
    $sanagich++;
};

$qadam();
$qadam();
$qadam();

echo "Yakuniy hisob: $sanagich
";

```

## Tushuntirish va Mantiq:
`use (&$var)` yordamida tashqi o'zgaruvchi havola sifatida qamrab olinadi va funksiya ichidagi barcha o'zgarishlar bevosita tashqi o'zgaruvchida aks etadi.

## Ishlash natijasi:
```text
Yakuniy hisob: 3
```

# 179-Topshiriq: Closure va callable tiplarini aniq belgilash
## Topshiriq sharti:
`callable` va `Closure` tiplarini qabul qiluvchi o'ram (wrapper) funksiya yozing.

## Yechim (PHP kodi):
```php
<?php

function amaliyotniBajar(callable $amal, mixed ...$argumentlar): mixed {
    echo "Operatsiya boshlandi...
";
    $natija = $amal(...$argumentlar);
    echo "Operatsiya tugadi.
";
    return $natija;
}

$hisob = amaliyotniBajar(fn($x, $y) => $x ** $y, 2, 8);
echo "Natija: $hisob
";

```

## Tushuntirish va Mantiq:
`callable` tipi har qanday chaqirilishi mumkin bo'lgan vositani (anonim funksiya, satr funksiya nomi, `[$obj, 'metod']`) qabul qiladi. `Closure` esa faqat toza anonim funksiyalarni talab qiladi.

## Ishlash natijasi:
```text
Operatsiya boshlandi...
Operatsiya tugadi.
Natija: 256
```

# 180-Topshiriq: Arrow functions (Qisqa o'qli funksiyalar: fn() => ...)
## Topshiriq sharti:
PHP 7.4 da kiritilgan `fn($param) => ifoda` sintaksisi orqali bir qatorli funksiyalar yozing.

## Yechim (PHP kodi):
```php
<?php

$ustama = 1.2;

// Qisqa arrow function
$hisoblaUstama = fn(float $narx) => $narx * $ustama;

echo "Asl narx: 100, Ustama bilan: " . $hisoblaUstama(100) . "
";

```

## Tushuntirish va Mantiq:
Arrow funksiyalari `fn(...) => ...` bir qatorda yoziladi va faqat bitta ifoda qaytaradi. Ular avtomatik ravishda `return` qiladi va tashqi o'zgaruvchilarni `use` so'zisiz avtomatik qamrab oladi.

## Ishlash natijasi:
```text
Asl narx: 100, Ustama bilan: 120
```

# 181-Topshiriq: Arrow functions da qiymat bo'yicha avtomatik qamrab olish (by-value capture)
## Topshiriq sharti:
Arrow funksiyalarda tashqi o'zgaruvchi o'zgarsa ham funksiya uning nusxasi bilan ishlashini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

$koytargich = 10;

$funksiya = fn($x) => $x * $koytargich;

$koytargich = 20; // O'zgartirdik

// Arrow function yaratilgan vaqtdagi nusxasini saqlaydi (10)
echo "Natija: " . $funksiya(5) . "
";

```

## Tushuntirish va Mantiq:
Arrow functions tashqi o'zgaruvchilarni faqat qiymat bo'yicha (by-value) avtomatik ushlaydi. Ular tashqi o'zgaruvchini havola bo'yicha o'zgartira olmaydi.

## Ishlash natijasi:
```text
Natija: 50
```

# 182-Topshiriq: Closure::bindTo() yordamida $this kontekstini o'zgartirish
## Topshiriq sharti:
Sinfning private xususiyatini `bindTo()` orqali tashqaridan o'qishni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

class MaxfiyHisob {
    private int $balans = 1500000;
}

$hisob = new MaxfiyHisob();

$oqish = function () {
    return $this->balans;
};

// Kontekstni MaxfiyHisob obyektiga va uning skopiga bog'laymiz
$bogланган = $oqish->bindTo($hisob, MaxfiyHisob::class);

echo "Maxfiy balans: " . number_format($bogланган()) . " so'm
";

```

## Tushuntirish va Mantiq:
`bindTo()` yoki `Closure::bind()` metodlari anonim funksiyaga `$this` kontekstini va uning kirish ruxsatlarini (hatto private xususiyatlarga kirish huquqini) dinamik o'zgartirish imkonini beradi.

## Ishlash natijasi:
```text
Maxfiy balans: 1,500,000 so'm
```

# 183-Topshiriq: First-class callable sintaksisi (PHP 8.1)
## Topshiriq sharti:
PHP 8.1 ning `funksiya(...)` sintaksisi yordamida standart PHP funksiyalarini to'g'ridan-to'g'ri Closure obyektiga aylantiring.

## Yechim (PHP kodi):
```php
<?php

$matn_uzunligi = strlen(...);

echo "Tipi: " . get_class($matn_uzunligi) . "
";
echo "Uzunlik: " . $matn_uzunligi("Khorazmiy AI") . "
";

$massiv = ["PHP", "JavaScript", "Rust"];
$uzunliklar = array_map(strlen(...), $massiv);
print_r($uzunliklar);

```

## Tushuntirish va Mantiq:
PHP 8.1 da `strlen(...)` sintaksisi istalgan funksiyadan to'laqonli `Closure` obyekti yasab beradi. Bu eski `Closure::fromCallable('strlen')` yozuvini almashtirib, kodni juda toza va xatosiz qiladi.

## Ishlash natijasi:
```text
Tipi: Closure
Uzunlik: 12
Array
(
    [0] => 3
    [1] => 10
    [2] => 4
)
```

# 184-Topshiriq: Obyekt metodlari uchun First-class callable sintaksisi
## Topshiriq sharti:
Obyekt instansiyasi metodini `$obyekt->metod(...)` orqali callable ga aylantiring.

## Yechim (PHP kodi):
```php
<?php

class ValyutaKonvertor {
    public function __construct(private float $kurs) {}

    public function konvert(float $usd): float {
        return $usd * $this->kurs;
    }
}

$konvertor = new ValyutaKonvertor(12800);
$funksiya = $konvertor->konvert(...);

echo "100 USD = " . number_format($funksiya(100)) . " UZS
";

```

## Tushuntirish va Mantiq:
`$obyekt->metod(...)` sintaksisi obyekt va uning metodini bitta ixcham `Closure` ga bog'lab beradi.

## Ishlash natijasi:
```text
100 USD = 1,280,000 UZS
```

# 185-Topshiriq: Statik metodlar uchun First-class callable sintaksisi
## Topshiriq sharti:
`Sinf::metod(...)` orqali statik metodni callable qilib uzating.

## Yechim (PHP kodi):
```php
<?php

class Matematika {
    public static function kub(int $x): int {
        return $x * $x * $x;
    }
}

$kubMetod = Matematika::kub(...);

echo "4 ning kubi: " . $kubMetod(4) . "
";

```

## Tushuntirish va Mantiq:
`Sinf::statikMetod(...)` sintaksisi statik metodlarga birinchi toifali chaqiruvchi sifatida havola yaratadi.

## Ishlash natijasi:
```text
4 ning kubi: 64
```

# 186-Topshiriq: Higher-Order Functions: Funksiyani argument sifatida qabul qilish
## Topshiriq sharti:
Filtr shartini tashqaridan funksiya ko'rinishida qabul qiluvchi maxsus massiv filtri tuzing.

## Yechim (PHP kodi):
```php
<?php

function maxsusFiltr(array $massiv, callable $shart): array {
    $natija = [];
    foreach ($massiv as $element) {
        if ($shart($element)) {
            $natija[] = $element;
        }
    }
    return $natija;
}

$sonlar = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
$juftlar = maxsusFiltr($sonlar, fn(int $n) => $n % 2 === 0);

echo "Juft sonlar: " . implode(", ", $juftlar) . "
";

```

## Tushuntirish va Mantiq:
Boshqa funksiyalarni parametr sifatida qabul qiluvchi yoki natija sifatida funksiya qaytaruvchi funksiyalar 'Yuqori tartibli funksiyalar' (Higher-Order Functions) deb ataladi.

## Ishlash natijasi:
```text
Juft sonlar: 2, 4, 6, 8, 10
```

# 187-Topshiriq: Higher-Order Functions: Funksiya generatori (Currying / Closure Factory)
## Topshiriq sharti:
Berilgan songa ko'paytiruvchi yangi maxsus funksiyalar yasab beruvchi funksiya yozing.

## Yechim (PHP kodi):
```php
<?php

function kopaytiruvchiYarat(float $koeffitsiyent): Closure {
    return function (float $son) use ($koeffitsiyent): float {
        return $son * $koeffitsiyent;
    };
}

$uchgaKopaytir = kopaytiruvchiYarat(3);
$ongaKopaytir = kopaytiruvchiYarat(10);

echo "5 * 3 = " . $uchgaKopaytir(5) . "
";
echo "5 * 10 = " . $ongaKopaytir(5) . "
";

```

## Tushuntirish va Mantiq:
Funksiyadan yangi funksiya qaytarish orqali sozlanuvchi xatti-harakatlarni yaratish mumkin (Factory Closure).

## Ishlash natijasi:
```text
5 * 3 = 15
5 * 10 = 50
```

# 188-Topshiriq: Funksiyalarni kompozitsiya qilish (Function Composition)
## Topshiriq sharti:
Ikkita funksiyani bitta ketma-ketlikda birlashtiruvchi `kompozitsiya(f, g)` mexanizmini yarating.

## Yechim (PHP kodi):
```php
<?php

function kompozitsiya(callable $f, callable $g): Closure {
    return fn($x) => $f($g($x));
}

$ikkiBarobar = fn(int $x) => $x * 2;
$uchQosh = fn(int $x) => $x + 3;

// avval 3 qo'shadi, so'ng natijani 2 ga ko'paytiradi: (5 + 3) * 2 = 16
$yangiAmal = kompozitsiya($ikkiBarobar, $uchQosh);

echo "Natija: " . $yangiAmal(5) . "
";

```

## Tushuntirish va Mantiq:
Funksiyalar kompozitsiyasi matematik `f(g(x))` qoidasiga asoslanadi. Bu murakkab biznes mantiqlarni kichik sof funksiyalardan yig'ishga yordam beradi.

## Ishlash natijasi:
```text
Natija: 16
```

# 189-Topshiriq: Funksional Pipeline (Konveyer) patterni
## Topshiriq sharti:
Berilgan matnni bir nechta funksiyalar zanjiri orqali bosqichma-bosqich o'tkazuvchi `pipeline` yarating.

## Yechim (PHP kodi):
```php
<?php

function pipeline(mixed $boshlangich, callable ...$bosqichlar): mixed {
    return array_reduce(
        $bosqichlar,
        fn($qiymat, $bosqich) => $bosqich($qiymat),
        $boshlangich
    );
}

$matn = "  Khorazmiy AI Dasturlash   ";

$tozalangan = pipeline(
    $matn,
    trim(...),
    strtolower(...),
    fn($str) => str_replace(" ", "-", $str)
);

echo "Pipeline natijasi: $tozalangan
";

```

## Tushuntirish va Mantiq:
Pipeline pattern ma'lumotlarni ketma-ket qadamlar orqali o'tkazib, har bir qadam natijasini keyingi qadamga uzatadi.

## Ishlash natijasi:
```text
Pipeline natijasi: khorazmiy-ai-dasturlash
```

# 190-Topshiriq: Memoization: Funksiya natijalarini keshlab tezlashtirish
## Topshiriq sharti:
Og'ir hisob-kitoblarni qayta bajarmaslik uchun ularni statik keshda eslab qoluvchi memoizatsiya mexanizmini yozing.

## Yechim (PHP kodi):
```php
<?php

function memoFaktorial(int $n): int {
    static $kesh = [];

    if (isset($kesh[$n])) {
        return $kesh[$n];
    }

    if ($n <= 1) {
        return 1;
    }

    $kesh[$n] = $n * memoFaktorial($n - 1);
    return $kesh[$n];
}

echo "Hisoblash 1 (6!): " . memoFaktorial(6) . "
";
echo "Hisoblash 2 (keshdan tezkor olinadi): " . memoFaktorial(6) . "
";

```

## Tushuntirish va Mantiq:
Memoization - bir xil argumentlar uchun funksiya natijasini xotirada saqlab, keyingi chaqiriqlarda qayta hisoblamasdan darhol qaytarish optimizatsiyasidir.

## Ishlash natijasi:
```text
Hisoblash 1 (6!): 720
Hisoblash 2 (keshdan tezkor olinadi): 720
```

# 191-Topshiriq: call_user_func() va call_user_func_array() funksiyalari
## Topshiriq sharti:
Dinamik argumentlar bilan funksiyani `call_user_func_array()` orqali chaqiring.

## Yechim (PHP kodi):
```php
<?php

function xabarFormatla(string $kimdan, string $matn): string {
    return "[$kimdan]: $matn";
}

$parametrlar = ["Admin", "Server qayta yuklanmoqda"];

$natija = call_user_func_array("xabarFormatla", $parametrlar);

echo $natija . "
";

```

## Tushuntirish va Mantiq:
`call_user_func_array($callback, $params)` massivdagi argumentlar to'plami bilan ixtiyoriy callback funksiyani ishga tushirish imkonini beradi.

## Ishlash natijasi:
```text
[Admin]: Server qayta yuklanmoqda
```

# 192-Topshiriq: Callback filtrlari yordamida dinamik qoidalar
## Topshiriq sharti:
Bir nechta tekshiruv qoidalarini (validatsiya) callbacklar orqali amalga oshiring.

## Yechim (PHP kodi):
```php
<?php

$qoidalar = [
    "Uzunlik kamida 5 ta" => fn(string $s) => strlen($s) >= 5,
    "Katta harf bor" => fn(string $s) => preg_match('/[A-Z]/', $s) === 1,
    "Raqam bor" => fn(string $s) => preg_match('/[0-9]/', $s) === 1,
];

$parol = "MaxfiyParol99";
$xatolar = [];

foreach ($qoidalar as $qoida_nomi => $tekshiruv) {
    if (!$tekshiruv($parol)) {
        $xatolar[] = $qoida_nomi;
    }
}

echo empty($xatolar) ? "Parol barcha talablarga javob beradi!
" : "Xatolar mavjud
";

```

## Tushuntirish va Mantiq:
Callbacklar yordamida qoidalarni dinamik ro'yxat sifatida saqlash va ularni alohida mustaqil ravishda sinab ko'rish juda osonlashadi.

## Ishlash natijasi:
```text
Parol barcha talablarga javob beradi!
```

# 193-Topshiriq: Generator funksiyalar va yield operatori asoslari
## Topshiriq sharti:
`yield` yordamida sonlar ketma-ketligini generatsiya qiluvchi oddiy generator yarating.

## Yechim (PHP kodi):
```php
<?php

function oddiySanagich(int $bosh, int $oxir): Generator {
    for ($i = $bosh; $i <= $oxir; $i++) {
        yield $i;
    }
}

foreach (oddiySanagich(1, 4) as $son) {
    echo "Son: $son
";
}

```

## Tushuntirish va Mantiq:
Generator funksiya `return` o'rniga `yield` operatoridan foydalanadi. U butun massivni xotirada birdaniga yaratmasdan, talab bo'lganda (on-demand) har bir qiymatni bittalab yetkazib beradi.

## Ishlash natijasi:
```text
Son: 1
Son: 2
Son: 3
Son: 4
```

# 194-Topshiriq: yield yordamida xotirani tejash (Memory efficiency)
## Topshiriq sharti:
1 millionta sonni massivda saqlash va generator orqali hosil qilishdagi xotira sarfini taqqoslang.

## Yechim (PHP kodi):
```php
<?php

function millionSonlar(): Generator {
    for ($i = 1; $i <= 100000; $i++) {
        yield $i;
    }
}

$boshlangich_xotira = memory_get_usage();
$generator = millionSonlar();
$generator_xotira = memory_get_usage() - $boshlangich_xotira;

echo "Generator egallagan xotira: " . round($generator_xotira / 1024, 2) . " KB
";

```

## Tushuntirish va Mantiq:
Oddiy massiv 100,000 ta butun son uchun bir necha megabayt xotira talab qilsa, `yield` generatori bitta obyekt sifatida bir necha kilobayt xotira egallaydi. Katta fayllarni o'qishda generatorlar tengsizdir.

## Ishlash natijasi:
```text
Generator egallagan xotira: 0 KB
```

# 195-Topshiriq: yield from sintaksisi orqali generatorlarni delegatsiya qilish
## Topshiriq sharti:
PHP 7 da kiritilgan `yield from` orqali bir nechta ichki generatorlarni bitta oqimga birlashtiring.

## Yechim (PHP kodi):
```php
<?php

function harflar(): Generator {
    yield "A";
    yield "B";
}

function raqamlar(): Generator {
    yield 1;
    yield 2;
}

function umumiyOqim(): Generator {
    yield from harflar();
    yield from raqamlar();
}

foreach (umumiyOqim() as $belgi) {
    echo "$belgi ";
}
echo "
";

```

## Tushuntirish va Mantiq:
`yield from <generator | array>` boshqa bir generator yoki massivdagi barcha qiymatlarni avtomatik tarzda joriy generatordan tashqariga uzatadi.

## Ishlash natijasi:
```text
A B 1 2 
```

# 196-Topshiriq: Generatorlarda kalit va qiymat qaytarish: yield $kalit => $qiymat
## Topshiriq sharti:
Satrlarni o'qib, ularning qator raqamini kalit sifatida `yield` orqali uzating.

## Yechim (PHP kodi):
```php
<?php

function qatorlarGeneratori(array $matnlar): Generator {
    $qator = 1;
    foreach ($matnlar as $matn) {
        yield "qator_$qator" => $matn;
        $qator++;
    }
}

$mahsulotlar = ["Olma", "Nok", "Shaftoli"];

foreach (qatorlarGeneratori($mahsulotlar) as $kalit => $qiymat) {
    echo "$kalit: $qiymat
";
}

```

## Tushuntirish va Mantiq:
`yield $kalit => $qiymat` yordamida generator orqali assotsiativ juftliklarni qaytarish mumkin.

## Ishlash natijasi:
```text
qator_1: Olma
qator_2: Nok
qator_3: Shaftoli
```

# 197-Topshiriq: Generatorga tashqaridan qiymat yuborish: $generator->send()
## Topshiriq sharti:
Generatorni ikki tomonlama aloqa vositasi (koroutina) sifatida ishlatib, unga `send()` orqali ma'lumot uzating.

## Yechim (PHP kodi):
```php
<?php

function logQabulQiluvchi(): Generator {
    while (true) {
        $xabar = yield; // Tashqaridan xabar kelishini kutadi
        echo "Qabul qilindi: $xabar
";
    }
}

$logger = logQabulQiluvchi();
$logger->send("Birinchi xabar");
$logger->send("Ikkinchi xabar");

```

## Tushuntirish va Mantiq:
`$generator->send($qiymat)` generator ichidagi `yield` ifodasining qiymati sifatida ma'lumot yetkazadi va ijroni keyingi `yield` gacha davom ettiradi.

## Ishlash natijasi:
```text
Qabul qilindi: Birinchi xabar
Qabul qilindi: Ikkinchi xabar
```

# 198-Topshiriq: Closures asosida oddiy Event Dispatcher (Hodisalar boshqaruvchisi)
## Topshiriq sharti:
Hodisalarni tinglovchi (listener) va chaqiruvchi tizimni anonim funksiyalar bilan tuzing.

## Yechim (PHP kodi):
```php
<?php

class HodisalarBoshqaruvchi {
    private array $tinglovchilar = [];

    public function tingla(string $hodisa, callable $callback): void {
        $this->tinglovchilar[$hodisa][] = $callback;
    }

    public function tarqat(string $hodisa, mixed $malumot): void {
        if (!empty($this->tinglovchilar[$hodisa])) {
            foreach ($this->tinglovchilar[$hodisa] as $callback) {
                $callback($malumot);
            }
        }
    }
}

$dispetcher = new HodisalarBoshqaruvchi();
$dispetcher->tingla("foydalanuvchi.royxat", function ($ism) {
    echo "Xush kelibsiz xati yuborildi: $ism
";
});

$dispetcher->tarqat("foydalanuvchi.royxat", "Farrux");

```

## Tushuntirish va Mantiq:
Anonim funksiyalar hodisalarni (Events & Listeners) erkin va o'zaro bog'lanmagan (decoupled) arxitekturada boshqarish uchun eng qulay vositadir.

## Ishlash natijasi:
```text
Xush kelibsiz xati yuborildi: Farrux
```

# 199-Topshiriq: Xatolik yuz berganda qayta urinuvchi (Retry mechanism) closure
## Topshiriq sharti:
Amal muvaffaqiyatsiz bo'lganda uni bir necha bor qayta sinab ko'ruvchi universal retry yordamchisini yozing.

## Yechim (PHP kodi):
```php
<?php

function qaytaUrin(callable $amal, int $maksimalUrinish = 3): mixed {
    $urinish = 0;
    while ($urinish < $maksimalUrinish) {
        try {
            $urinish++;
            return $amal($urinish);
        } catch (Exception $e) {
            echo "{$urinish}-urinish muvaffaqiyatsiz: " . $e->getMessage() . "
";
            if ($urinish >= $maksimalUrinish) {
                throw $e;
            }
        }
    }
    return null;
}

$natija = qaytaUrin(function ($urinish) {
    if ($urinish < 2) {
        throw new Exception("Ulanish xatosi");
    }
    return "Muvaffaqiyatli ma'lumot olindi!";
});

echo "Yakun: $natija
";

```

## Tushuntirish va Mantiq:
Retry naqshi tashqi tarmoq yoki API so'rovlarida yuzaga keladigan vaqtinchalik xatoliklarni bartaraf etishda eng muhim barqarorlik mexanizmidir.

## Ishlash natijasi:
```text
1-urinish muvaffaqiyatsiz: Ulanish xatosi
Yakun: Muvaffaqiyatli ma'lumot olindi!
```

# 200-Topshiriq: Benchmarking: Funksiyaning ishlash tezligini o'lchovchi profilchi
## Topshiriq sharti:
Ixtiyoriy funksiya kodining qancha millisekundda bajarilganini va xotira sarfini aniqlovchi o'lchov vositasini tuzing.

## Yechim (PHP kodi):
```php
<?php

function profilchi(callable $funksiya): void {
    $vaqt_boshlandi = microtime(true);
    $xotira_boshlandi = memory_get_usage();

    $funksiya();

    $vaqt_farqi = (microtime(true) - $vaqt_boshlandi) * 1000;
    $xotira_farqi = memory_get_usage() - $xotira_boshlandi;

    echo sprintf("Bajarilish vaqti: %.4f ms | Xotira sarfi: %d bayt
", $vaqt_farqi, $xotira_farqi);
}

profilchi(function () {
    $summa = 0;
    for ($i = 0; $i < 100000; $i++) {
        $summa += $i;
    }
});

```

## Tushuntirish va Mantiq:
`microtime(true)` va `memory_get_usage()` funksiyalari dasturchiga kodning unumdorligi va resurs sarfini aniq tahlil qilish imkonini beradi.

## Ishlash natijasi:
```text
Bajarilish vaqti: 2.1500 ms | Xotira sarfi: 0 bayt
```
