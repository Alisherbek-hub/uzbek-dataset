# 5-Mavzu: OOP Asoslari, Sinflar va Obyektlar (201-250)

Ushbu bo'limda PHP 8.2 va 8.3 versiyalaridagi obyektga yo'naltirilgan dasturlashning (OOP) barcha fundamental poydevori batafsil o'rganiladi:
Sinflar va instansiyalar (`class`, `new`), xususiyatlar va metodlar, `$this` ko'rsatkichi, konstruktor (`__construct`) va destruktor (`__destruct`), ko'rinish darajalari (`public`, `protected`, `private`), getter va setterlar, PHP 8 Constructor Property Promotion, `readonly` xususiyatlar va `readonly class`, statik a'zolar (`static`, `self::`), Late Static Binding (`static::`), sinf konstantalari va `final const`, sehrli metodlar (`__toString`, `__get`, `__set`, `__isset`, `__unset`, `__call`, `__callStatic`, `__invoke`, `__clone`, `__debugInfo`), seriyalashtirish (`__serialize`, `__unserialize`), tiplash va DTO lar, Value Objects, Reflection API, Method Chaining (Fluent Interface), Statik zavod metodlari hamda xotirani boshqarish bo'yicha 50 ta amaliy topshiriq jamlangan.

---

# 201-Topshiriq: Sinf (Class) va Obyekt (Object) yaratish asoslari
## Topshiriq sharti:
`Avtomobil` sinfini yarating va undan yangi instansiya (`new`) hosil qiling.

## Yechim (PHP kodi):
```php
<?php

class Avtomobil {
    public string $model;
    public string $rang;
}

$mashina = new Avtomobil();
$mashina->model = "Chevrolet Gentra";
$mashina->rang = "Oq";

echo "Model: " . $mashina->model . ", Rangi: " . $mashina->rang . "
";

```

## Tushuntirish va Mantiq:
Sinf (class) - bu yangi ma'lumot turining qolipi (blueprint). Obyekt esa ushbu qolip asosida `new` kalit so'zi yordamida xotirada yaratilgan aniq nusxadir.

## Ishlash natijasi:
```text
Model: Chevrolet Gentra, Rangi: Oq
```

# 202-Topshiriq: Metodlar e'lon qilish va ularni chaqirish
## Topshiriq sharti:
Avtomobilni o't oldirish va to'xtatish harakatlarini bajaruvchi metodlar yozing.

## Yechim (PHP kodi):
```php
<?php

class Avtomobil {
    public string $model;
    public bool $yondi = false;

    public function otOldir(): void {
        $this->yondi = true;
        echo "{$this->model} dvigateli o't oldirildi!
";
    }

    public function ochir(): void {
        $this->yondi = false;
        echo "{$this->model} dvigateli o'chirildi.
";
    }
}

$cobalt = new Avtomobil();
$cobalt->model = "Chevrolet Cobalt";
$cobalt->otOldir();
$cobalt->ochir();

```

## Tushuntirish va Mantiq:
Sinf ichida e'lon qilingan funksiyalar 'metodlar' deb ataladi. Ular obyektning xatti-harakatlarini (behavior) ifodalaydi.

## Ishlash natijasi:
```text
Chevrolet Cobalt dvigateli o't oldirildi!
Chevrolet Cobalt dvigateli o'chirildi.
```

# 203-Topshiriq: $this ko'rsatkichi va obyekt holati
## Topshiriq sharti:
Sinf metodlari ichida obyektning o'z xususiyatlariga kirish uchun `$this` dan foydalaning.

## Yechim (PHP kodi):
```php
<?php

class Hamyon {
    public float $balans = 0.0;

    public function tolovQil(float $summa): void {
        if ($this->balans >= $summa) {
            $this->balans -= $summa;
            echo "To'lov amalga oshirildi: $summa so'm. Qoldiq: {$this->balans} so'm
";
        } else {
            echo "Mablag' yetarli emas!
";
        }
    }
}

$hamyon = new Hamyon();
$hamyon->balans = 100000;
$hamyon->tolovQil(35000);

```

## Tushuntirish va Mantiq:
`$this` maxsus psevdo-o'zgaruvchi bo'lib, metod chaqirilayotgan joriy obyekt instansiyasiga ko'rsatib turadi.

## Ishlash natijasi:
```text
To'lov amalga oshirildi: 35000 so'm. Qoldiq: 65000 so'm
```

# 204-Topshiriq: Konstruktor metodi (__construct)
## Topshiriq sharti:
Obyekt yaratilayotgan vaqtda uning xususiyatlarini avtomatik to'ldiruvchi konstruktor yozing.

## Yechim (PHP kodi):
```php
<?php

class Kitob {
    public string $nom;
    public string $muallif;
    public int $sahifalar;

    public function __construct(string $nom, string $muallif, int $sahifalar) {
        $this->nom = $nom;
        $this->muallif = $muallif;
        $this->sahifalar = $sahifalar;
    }

    public function info(): string {
        return "'{$this->nom}' - {$this->muallif} ({$this->sahifalar} bet)";
    }
}

$kitob = new Kitob("O'tkan kunlar", "Abdulla Qodiriy", 380);
echo $kitob->info() . "
";

```

## Tushuntirish va Mantiq:
`__construct()` metodi `new Sinf()` orqali obyekt yaratilgan zahoti avtomatik chaqiriladi va obyektni kerakli boshlang'ich qiymatlar bilan ta'minlaydi.

## Ishlash natijasi:
```text
'O'tkan kunlar' - Abdulla Qodiriy (380 bet)
```

# 205-Topshiriq: Destruktor metodi (__destruct)
## Topshiriq sharti:
Obyekt xotiradan o'chirilayotganda resurslarni yopuvchi destruktor yozing.

## Yechim (PHP kodi):
```php
<?php

class FaylYozuvchi {
    private string $nom;

    public function __construct(string $nom) {
        $this->nom = $nom;
        echo "Fayl ochildi: {$this->nom}
";
    }

    public function __destruct() {
        echo "Fayl xavfsiz yopildi: {$this->nom}
";
    }
}

$fayl = new FaylYozuvchi("hisobot.txt");
unset($fayl); // Destruktor shu yerda darhol ishga tushadi
echo "Dastur yakunlandi.
";

```

## Tushuntirish va Mantiq:
`__destruct()` metodi obyektga boshqa hech qanday havola qolmaganda yoki dastur ishi yakunlanayotganda xotirani tozalash uchun avtomatik ishga tushadi.

## Ishlash natijasi:
```text
Fayl ochildi: hisobot.txt
Fayl xavfsiz yopildi: hisobot.txt
Dastur yakunlandi.
```

# 206-Topshiriq: Ko'rinish darajasi: public
## Topshiriq sharti:
`public` kalit so'zi bilan e'lon qilingan a'zolar tashqaridan bemalol o'qilishi va o'zgartirilishini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

class Mahsulot {
    public string $nom;
    public float $narx;
}

$m = new Mahsulot();
$m->nom = "Monitor";
$m->narx = 2200000;

echo "Mahsulot: {$m->nom}, Narxi: {$m->narx} so'm
";

```

## Tushuntirish va Mantiq:
`public` xususiyatlar va metodlar sinf ichida ham, undan meros olgan sinflarda ham, hamda sinfdan tashqaridagi ixtiyoriy kodda ham ochiq va mavjuddir.

## Ishlash natijasi:
```text
Mahsulot: Monitor, Narxi: 2200000 so'm
```

# 207-Topshiriq: Ko'rinish darajasi: protected
## Topshiriq sharti:
`protected` xususiyatlar faqat sinfning o'zi va uning vorislarida (merosxorda) ishlashini namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class Xodim {
    protected float $maosh;

    public function __construct(float $maosh) {
        $this->maosh = $maosh;
    }
}

class Menejer extends Xodim {
    public function maoshKorsat(): string {
        return "Menejer maoshi: " . number_format($this->maosh) . " so'm";
    }
}

$m = new Menejer(15000000);
echo $m->maoshKorsat() . "
";
// $m->maosh tashqaridan to'g'ridan-to'g'ri o'qilsa xatolik beradi

```

## Tushuntirish va Mantiq:
`protected` a'zolar tashqi dunyodan yashirilgan bo'ladi, lekin bolalar (merosxo'r sinflar) ularga erkin murojaat qila oladi.

## Ishlash natijasi:
```text
Menejer maoshi: 15,000,000 so'm
```

# 208-Topshiriq: Ko'rinish darajasi: private
## Topshiriq sharti:
`private` xususiyatlar faqat e'lon qilingan sinf tanasi ichida yopiq bo'lishini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

class BankKarta {
    private string $pinKod;

    public function __construct(string $pin) {
        $this->pinKod = $pin;
    }

    public function pinTogrimi(string $kiritilgan): bool {
        return $this->pinKod === $kiritilgan;
    }
}

$karta = new BankKarta("4491");
echo "PIN 4491 to'g'rimi: " . ($karta->pinTogrimi("4491") ? "Ha" : "Yo'q") . "
";
echo "PIN 0000 to'g'rimi: " . ($karta->pinTogrimi("0000") ? "Ha" : "Yo'q") . "
";

```

## Tushuntirish va Mantiq:
`private` a'zolar faqat shu sinfning ichida ko'rinadi. Hatto voris sinflar ham `private` a'zolarga bevosita kira olmaydi. Bu to'liq inkapsulyatsiyani ta'minlaydi.

## Ishlash natijasi:
```text
PIN 4491 to'g'rimi: Ha
PIN 0000 to'g'rimi: Yo'q
```

# 209-Topshiriq: Getter va Setter metodlari orqali inkapsulyatsiya
## Topshiriq sharti:
Yosh xususiyatini faqat musbat va mantiqiy son bo'lishini nazorat qiluvchi getter va setter yozing.

## Yechim (PHP kodi):
```php
<?php

class Foydalanuvchi {
    private int $yosh;

    public function setYosh(int $yosh): void {
        if ($yosh < 0 || $yosh > 150) {
            throw new InvalidArgumentException("Yaroqsiz yosh: $yosh");
        }
        $this->yosh = $yosh;
    }

    public function getYosh(): int {
        return $this->yosh;
    }
}

$f = new Foydalanuvchi();
$f->setYosh(25);
echo "Foydalanuvchi yoshi: " . $f->getYosh() . "
";

```

## Tushuntirish va Mantiq:
Getter va Setter metodlari obyekt ichki holatini tashqi noto'g'ri o'zgarishlardan himoya qiladi va ma'lumotlar yaxlitligini (validation) kafolatlaydi.

## Ishlash natijasi:
```text
Foydalanuvchi yoshi: 25
```

# 210-Topshiriq: PHP 8 Constructor Property Promotion
## Topshiriq sharti:
PHP 8 ning yangi sintaksisi yordamida konstruktor argumentida xususiyatlarni bir vaqtning o'zida e'lon qiling va initsializatsiya qiling.

## Yechim (PHP kodi):
```php
<?php

class Mijoz {
    public function __construct(
        public string $ism,
        public string $telefon,
        private float $balans = 0.0
    ) {}

    public function getBalans(): float {
        return $this->balans;
    }
}

$mijoz = new Mijoz("Bekzod", "+998901234567", 500000);
echo "Mijoz: {$mijoz->ism}, Balans: {$mijoz->getBalans()} so'm
";

```

## Tushuntirish va Mantiq:
PHP 8 Constructor Property Promotion sintaksisi xususiyatlarni alohida e'lon qilish va konstruktorda `$this->x = $x` deb yozish majburiyatini yo'qotib, kod hajmini 3 barobarga qisqartiradi.

## Ishlash natijasi:
```text
Mijoz: Bekzod, Balans: 500000 so'm
```

# 211-Topshiriq: PHP 8.1 Readonly xususiyatlar
## Topshiriq sharti:
PHP 8.1 ning `readonly` kalit so'zi yordamida faqat bir marta initsializatsiya qilinadigan o'zgarmas xususiyat yarating.

## Yechim (PHP kodi):
```php
<?php

class FoydalanuvchiID {
    public function __construct(
        public readonly string $uuid,
        public readonly int $tizimID
    ) {}
}

$uid = new FoydalanuvchiID("usr-8891-abx", 42);
echo "UUID: {$uid->uuid}
";
// $uid->uuid = "yangi"; // Bu qator Error tashlaydi!

```

## Tushuntirish va Mantiq:
`readonly` xususiyatlar faqat konstruktorda bir marta qiymat oladi va keyinchalik ularning qiymatini o'zgartirish qat'iyan taqiqlanadi (immutability).

## Ishlash natijasi:
```text
UUID: usr-8891-abx
```

# 212-Topshiriq: PHP 8.2 Readonly sinflar
## Topshiriq sharti:
PHP 8.2 ning `readonly class` imkoniyatidan foydalanib butun sinf xususiyatlarini avtomatik o'zgarmas qiling.

## Yechim (PHP kodi):
```php
<?php

readonly class ManzilDTO {
    public function __construct(
        public string $shahar,
        public string $kocha,
        public string $uyRaqami
    ) {}
}

$manzil = new ManzilDTO("Toshkent", "Amir Temur", "14A");
echo "Manzil: {$manzil->shahar}, {$manzil->kocha} ko'chasi, {$manzil->uyRaqami}-uy
";

```

## Tushuntirish va Mantiq:
`readonly class` e'lon qilinganda, uning barcha xususiyatlari avtomatik ravishda `readonly` bo'ladi va dinamik xususiyatlar qo'shish taqiqlanadi. DTO lar uchun mukammal yechim.

## Ishlash natijasi:
```text
Manzil: Toshkent, Amir Temur ko'chasi, 14A-uy
```

# 213-Topshiriq: Statik xususiyatlar va self::$xususiyat
## Topshiriq sharti:
Sinfdan nechtadan obyekt yaratilganini hisoblab boruvchi statik hisoblagich tuzing.

## Yechim (PHP kodi):
```php
<?php

class Foydalanuvchi {
    public static int $umumiySoni = 0;

    public function __construct(public string $ism) {
        self::$umumiySoni++;
    }
}

new Foydalanuvchi("Ali");
new Foydalanuvchi("Vali");
new Foydalanuvchi("Gani");

echo "Jami yaratilgan foydalanuvchilar: " . Foydalanuvchi::$umumiySoni . "
";

```

## Tushuntirish va Mantiq:
Statik xususiyatlar alohida obyektga emas, balki butun sinfga tegishli bo'ladi. Ular barcha obyektlar uchun umumiy bitta xotira maydonida saqlanadi va `self::$nomi` orqali murojaat qilinadi.

## Ishlash natijasi:
```text
Jami yaratilgan foydalanuvchilar: 3
```

# 214-Topshiriq: Statik metodlar va yordamchi utility sinflar
## Topshiriq sharti:
Instansiya yaratmasdan to'g'ridan-to'g'ri chaqiriluvchi statik yordamchi metodlar to'plamini tuzing.

## Yechim (PHP kodi):
```php
<?php

class PulFormati {
    public static function format(float $summa, string $valyuta = "so'm"): string {
        return number_format($summa, 0, '.', ' ') . " " . $valyuta;
    }
}

echo PulFormati::format(15000000) . "
";
echo PulFormati::format(250, "USD") . "
";

```

## Tushuntirish va Mantiq:
Statik metodlar `Sinf::metod()` sintaksisi bilan `new` siz chaqiriladi. Ular `$this` ga ega emas, shuning uchun faqat argumentlar va statik xususiyatlar bilan ishlaydi.

## Ishlash natijasi:
```text
15 000 000 so'm
250 USD
```

# 215-Topshiriq: Late Static Binding (LSB): static:: vs self:: farqi
## Topshiriq sharti:
Merosxo'rlikda `self::` o'rniga `static::` dan foydalanish polimorfik statik chaqiruvlarni qanday ta'minlashini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

class Model {
    protected static string $jadval = "models";

    public static function getJadvalSelf(): string {
        return self::$jadval;
    }

    public static function getJadvalStatic(): string {
        return static::$jadval; // Late Static Binding
    }
}

class User extends Model {
    protected static string $jadval = "users";
}

echo "self orqali: " . User::getJadvalSelf() . "
";
echo "static orqali: " . User::getJadvalStatic() . "
";

```

## Tushuntirish va Mantiq:
`self::` har doim metod e'lon qilingan sinfga murojaat qiladi. `static::` esa dastur bajarilish vaqtida metodni aynan kim chaqirgan bo'lsa (Late Static Binding), o'sha sinfga murojaat qiladi. Eloquent ORM aynan shunga tayanadi.

## Ishlash natijasi:
```text
self orqali: models
static orqali: users
```

# 216-Topshiriq: Sinf konstantalari va ko'rinish darajalari
## Topshiriq sharti:
Sinf ichida `public const` va `private const` konstantalarini e'lon qiling.

## Yechim (PHP kodi):
```php
<?php

class Buyurtma {
    public const STATUS_YANGI = "yangi";
    public const STATUS_YETKAZILDI = "yetkazildi";
    private const KOMISSIYA = 0.05;

    public function hisoblaKomissiya(float $summa): float {
        return $summa * self::KOMISSIYA;
    }
}

echo "Birlamchi status: " . Buyurtma::STATUS_YANGI . "
";

$b = new Buyurtma();
echo "Komissiya: " . $b->hisoblaKomissiya(100000) . " so'm
";

```

## Tushuntirish va Mantiq:
Sinf konstantalari sinfga biriktirilgan o'zgarmas qiymatlardir. PHP 7.1 dan boshlab konstantalarga ham `public`, `protected`, `private` ko'rinish darajalarini berish mumkin.

## Ishlash natijasi:
```text
Birlamchi status: yangi
Komissiya: 5000 so'm
```

# 217-Topshiriq: Final sinf konstantalari (PHP 8.1)
## Topshiriq sharti:
PHP 8.1 ning `final const` sintaksisi yordamida voris sinflarda o'zgarmasni qayta e'lon qilishni taqiqlang.

## Yechim (PHP kodi):
```php
<?php

class AsosiyKonfig {
    final public const PROTOKOL = "HTTPS";
}

class KengaytirilganKonfig extends AsosiyKonfig {
    // public const PROTOKOL = "HTTP"; // Fatal error beradi!
}

echo "Protokol: " . KengaytirilganKonfig::PROTOKOL . "
";

```

## Tushuntirish va Mantiq:
`final const` voris sinflar tomonidan konstantaning qayta aniqlanishini (override) bloklaydi.

## Ishlash natijasi:
```text
Protokol: HTTPS
```

# 218-Topshiriq: Sehrli metod: __toString()
## Topshiriq sharti:
Obyekt satr sifatida (`echo $obj`) ishlatilganda avtomatik formatlangan matn qaytaruvchi `__toString()` metodini yozing.

## Yechim (PHP kodi):
```php
<?php

class Talaba {
    public function __construct(
        private string $ism,
        private float $gpa
    ) {}

    public function __toString(): string {
        return "Talaba: {$this->ism} (GPA: {$this->gpa})";
    }
}

$talaba = new Talaba("Akmal", 3.85);
echo $talaba . "
";

```

## Tushuntirish va Mantiq:
`__toString()` obyekti satr sifatida chaqirilganda (masalan `echo` qilinganda yoki satrga ulanayotganda) avtomatik ishga tushadi.

## Ishlash natijasi:
```text
Talaba: Akmal (GPA: 3.85)
```

# 219-Topshiriq: Sehrli metodlar: __get() va __set()
## Topshiriq sharti:
Mavjud bo'lmagan xususiyatlarga murojaatni boshqaruvchi dinamik xususiyatlar omborini (property container) tuzing.

## Yechim (PHP kodi):
```php
<?php

class Sozlamalar {
    private array $malumotlar = [];

    public function __set(string $nom, mixed $qiymat): void {
        $this->malumotlar[$nom] = $qiymat;
    }

    public function __get(string $nom): mixed {
        return $this->malumotlar[$nom] ?? null;
    }
}

$s = new Sozlamalar();
$s->til = "uz";
$s->keshVaqti = 3600;

echo "Til: " . $s->til . "
";
echo "Kesh vaqti: " . $s->keshVaqti . " soniya
";

```

## Tushuntirish va Mantiq:
`__set($name, $value)` sinfda e'lon qilinmagan yoki yopiq xususiyatga qiymat yozilayotganda, `__get($name)` esa undan qiymat o'qilayotganda ishlaydi.

## Ishlash natijasi:
```text
Til: uz
Kesh vaqti: 3600 soniya
```

# 220-Topshiriq: Sehrli metodlar: __isset() va __unset()
## Topshiriq sharti:
Dinamik xususiyatlar mavjudligini `isset()` va ularni `unset()` qilishni ta'minlang.

## Yechim (PHP kodi):
```php
<?php

class DinamikModel {
    private array $maydonlar = ["status" => "faol"];

    public function __isset(string $nom): bool {
        return isset($this->maydonlar[$nom]);
    }

    public function __unset(string $nom): void {
        unset($this->maydonlar[$nom]);
    }
}

$m = new DinamikModel();
echo "status bormi: " . (isset($m->status) ? "Ha" : "Yo'q") . "
";
unset($m->status);
echo "unset dan so'ng bormi: " . (isset($m->status) ? "Ha" : "Yo'q") . "
";

```

## Tushuntirish va Mantiq:
`__isset()` yopiq yoki mavjud bo'lmagan xususiyatga `isset()` yoki `empty()` chaqirilganda, `__unset()` esa `unset()` qilinganda ishlaydi.

## Ishlash natijasi:
```text
status bormi: Ha
unset dan so'ng bormi: Yo'q
```

# 221-Topshiriq: Sehrli metod: __call() dinamik metod chaqiruvlari
## Topshiriq sharti:
Mavjud bo'lmagan metod chaqirilganda uni avtomatik ushlab olib tegishli xabarni ko'rsatuvchi sinf tuzing.

## Yechim (PHP kodi):
```php
<?php

class Qidiruvchi {
    public function __call(string $metodNomi, array $argumentlar): void {
        if (str_starts_with($metodNomi, "findBy")) {
            $maydon = substr($metodNomi, 6);
            echo "Bazada qidirilmoqda: {$maydon} = '{$argumentlar[0]}'
";
            return;
        }
        echo "Bunday metod mavjud emas: $metodNomi
";
    }
}

$qidiruv = new Qidiruvchi();
$qidiruv->findByEmail("admin@uz.uz");
$qidiruv->findByTelefon("+998901234567");

```

## Tushuntirish va Mantiq:
`__call($method, $args)` obyektdan topilmagan yoki yopiq metod chaqirilganda chaqiriladi. Laravel Eloquent dagi `whereName(...)` kabi sehrli metodlar aynan shu tamoyil asosida ishlaydi.

## Ishlash natijasi:
```text
Bazada qidirilmoqda: Email = 'admin@uz.uz'
Bazada qidirilmoqda: Telefon = '+998901234567'
```

# 222-Topshiriq: Sehrli metod: __callStatic() dinamik statik chaqiruvlar
## Topshiriq sharti:
Sinfga statik tarzda mavjud bo'lmagan metod orqali murojaat qilinganda uni `__callStatic()` orqali ushlang.

## Yechim (PHP kodi):
```php
<?php

class Logger {
    public static function __callStatic(string $daraja, array $argumentlar): void {
        $xabar = $argumentlar[0] ?? "";
        echo "[" . strtoupper($daraja) . "]: $xabar
";
    }
}

Logger::info("Tizim muvaffaqiyatli yuklandi");
Logger::error("Ulanish rad etildi");

```

## Tushuntirish va Mantiq:
`__callStatic()` statik metod topilmaganda ishga tushadi. Facade lar va statik kirish interfeyslarida juda ko'p ishlatiladi.

## Ishlash natijasi:
```text
[INFO]: Tizim muvaffaqiyatli yuklandi
[ERROR]: Ulanish rad etildi
```

# 223-Topshiriq: Sehrli metod: __invoke() orqali obyektni funksiya kabi chaqirish
## Topshiriq sharti:
`Invokable` sinf yaratib, obyektni xuddi oddiy funksiya kabi `$obyekt()` tarzida ishlatishni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

class NarxChegirma {
    public function __construct(private float $foiz) {}

    public function __invoke(float $narx): float {
        return $narx - ($narx * ($this->foiz / 100));
    }
}

$chegirma20 = new NarxChegirma(20);

// Obyekt to'g'ridan-to'g'ri chaqiriladi
echo "100 000 so'm chegirma bilan: " . $chegirma20(100000) . " so'm
";

```

## Tushuntirish va Mantiq:
`__invoke()` metodi obyekt funksiya kabi chaqirilganda bajariladi. Laravel Single Action Controllers (`__invoke`) aynan shu metodga tayanadi.

## Ishlash natijasi:
```text
100 000 so'm chegirma bilan: 80000 so'm
```

# 224-Topshiriq: Obyektlarni klonlash va __clone() metodi
## Topshiriq sharti:
`clone` operatori va `__clone()` orqali obyekt nusxasini yaratishda ichki qiymatlarni yangilang.

## Yechim (PHP kodi):
```php
<?php

class Hisobot {
    public string $sana;
    public string $id;

    public function __construct(string $sana) {
        $this->sana = $sana;
        $this->id = uniqid("rep_");
    }

    public function __clone() {
        // Yangi klon uchun yangi ID beramiz
        $this->id = uniqid("rep_");
    }
}

$asl = new Hisobot("2026-05-01");
$nusxa = clone $asl;

echo "Asl hisobot ID: " . (!empty($asl->id) ? "Mavjud" : "Yo'q") . "
";
echo "Klon hisobot ID aslidan farq qiladi: " . ($asl->id !== $nusxa->id ? "Ha" : "Yo'q") . "
";

```

## Tushuntirish va Mantiq:
`clone $obj` operatori obyektning sayoz nusxasini (shallow copy) oladi va avtomatik ravishda `__clone()` sehrli metodini ishga tushiradi.

## Ishlash natijasi:
```text
Asl hisobot ID: Mavjud
Klon hisobot ID aslidan farq qiladi: Ha
```

# 225-Topshiriq: Chuqur nusxalash (Deep Copy) __clone() orqali
## Topshiriq sharti:
Obyekt ichida boshqa obyekt mavjud bo'lganda, `__clone()` da uning ham alohida nusxasini olishni ta'minlang.

## Yechim (PHP kodi):
```php
<?php

class Manzil {
    public function __construct(public string $shahar) {}
}

class Shaxs {
    public function __construct(
        public string $ism,
        public Manzil $manzil
    ) {}

    public function __clone() {
        // Ichki obyektni ham alohida klon qilamiz (Deep Copy)
        $this->manzil = clone $this->manzil;
    }
}

$a = new Shaxs("Akmal", new Manzil("Toshkent"));
$b = clone $a;

$b->manzil->shahar = "Samarqand";

echo "Asl shaxs shahri: {$a->manzil->shahar}
";
echo "Klon shaxs shahri: {$b->manzil->shahar}
";

```

## Tushuntirish va Mantiq:
Sayoz nusxalashda ichki obyektlar havola sifatida qoladi. Chuqur nusxalashda (Deep Copy) esa `__clone()` ichida barcha ichki obyektlar ham qayta `clone` qilinadi.

## Ishlash natijasi:
```text
Asl shaxs shahri: Toshkent
Klon shaxs shahri: Samarqand
```

# 226-Topshiriq: Sehrli metod: __debugInfo() orqali maxfiy ma'lumotlarni yashirish
## Topshiriq sharti:
`var_dump()` qilinganda parollar va xavfsizlik kalitlari konsolga chiqmasligi uchun `__debugInfo()` ni qo'llang.

## Yechim (PHP kodi):
```php
<?php

class FoydalanuvchiAkkaunt {
    public function __construct(
        public string $login,
        private string $parolXesh
    ) {}

    public function __debugInfo(): array {
        return [
            "login" => $this->login,
            "parolXesh" => "****** [MAXFIY HIMOYA] ******"
        ];
    }
}

$user = new FoydalanuvchiAkkaunt("admin", "argon2id$v=19$m=65536...");
var_dump($user);

```

## Tushuntirish va Mantiq:
`__debugInfo()` `var_dump()` chaqirilganda ko'rsatiladigan massivni qaytaradi. Bu maxfiy API kalitlar yoki parollarning loglarga tushib qolishini oldini oladi.

## Ishlash natijasi:
```text
object(FoydalanuvchiAkkaunt)#1 (2) {
  ["login"]=>
  string(5) "admin"
  ["parolXesh"]=>
  string(31) "****** [MAXFIY HIMOYA] ******"
}
```

# 227-Topshiriq: Obyektlarni seriyalashtirish: serialize() va unserialize()
## Topshiriq sharti:
Obyekt holatini satrga aylantirib, so'ngra asl obyekt ko'rinishida qayta tiklang.

## Yechim (PHP kodi):
```php
<?php

class Sessiya {
    public function __construct(
        public int $userId,
        public string $ip
    ) {}
}

$sessiya = new Sessiya(105, "127.0.0.1");
$satr = serialize($sessiya);

echo "Seriyalangan satr: $satr
";

$tiklangan = unserialize($satr);
echo "Qayta tiklangan UserID: {$tiklangan->userId}
";

```

## Tushuntirish va Mantiq:
`serialize()` obyektning xotiradagi holatini baytlar ketma-ketligiga (satrga) aylantiradi. `unserialize()` esa uni asl obyekt ko'rinishida tiklaydi.

## Ishlash natijasi:
```text
Seriyalangan satr: O:7:"Sessiya":2:{s:6:"userId";i:105;s:2:"ip";s:9:"127.0.0.1";}
Qayta tiklangan UserID: 105
```

# 228-Topshiriq: __serialize() va __unserialize() zamonaviy metodlari (PHP 7.4+)
## Topshiriq sharti:
PHP 7.4 da kiritilgan `__serialize` va `__unserialize` orqali faqat kerakli xususiyatlarni saqlashni nazorat qiling.

## Yechim (PHP kodi):
```php
<?php

class KeshOb'ekt {
    public function __construct(
        public string $kalit,
        public mixed $qiymat,
        public int $vaqt
    ) {}

    public function __serialize(): array {
        // Faqat kalit va qiymat saqlansin
        return ["k" => $this->kalit, "q" => $this->qiymat];
    }

    public function __unserialize(array $data): void {
        $this->kalit = $data["k"];
        $this->qiymat = $data["q"];
        $this->vaqt = time(); // Tiklangan vaqt yangilanadi
    }
}

$kesh = new KeshOb'ekt("foydalanuvchi_1", ["ism" => "Ali"], 100);
$str = serialize($kesh);
$qayta = unserialize($str);

echo "Tiklandi: kalit = {$qayta->kalit}
";

```

## Tushuntirish va Mantiq:
`__serialize()` va `__unserialize()` eski `Serializable` interfeysini almashtirdi va seriyalashtirish jarayonini xavfsiz va to'liq nazorat qilish imkonini beradi.

## Ishlash natijasi:
```text
Tiklandi: kalit = foydalanuvchi_1
```

# 229-Topshiriq: instanceof operatori orqali obyekt tipini tekshirish
## Topshiriq sharti:
Berilgan obyektning ma'lum sinfga yoki interfeysga tegishli ekanligini `instanceof` orqali tekshiring.

## Yechim (PHP kodi):
```php
<?php

class Hayvon {}
class Mushuk extends Hayvon {}
class Mashina {}

$mushuk = new Mushuk();

echo "mushuk Hayvon sinfiga tegishlimi: " . ($mushuk instanceof Hayvon ? "Ha" : "Yo'q") . "
";
echo "mushuk Mashina sinfiga tegishlimi: " . ($mushuk instanceof Mashina ? "Ha" : "Yo'q") . "
";

```

## Tushuntirish va Mantiq:
`instanceof` operatori obyektning ma'lum sinfdan yoki uning avlodlaridan yaratilganligini tekshiradi va `boolean` qaytaradi.

## Ishlash natijasi:
```text
mushuk Hayvon sinfiga tegishlimi: Ha
mushuk Mashina sinfiga tegishlimi: Yo'q
```

# 230-Topshiriq: Anonim sinflar (Anonymous classes: new class { ... })
## Topshiriq sharti:
Alohida fayl ochmasdan bitta o'rinda bir martalik anonim sinf yaratib, uning metodini chaqiring.

## Yechim (PHP kodi):
```php
<?php

$logger = new class {
    public function log(string $xabar): void {
        echo "[LOG]: $xabar
";
    }
};

$logger->log("Bir martalik anonim sinf muvaffaqiyatli ishladi");

```

## Tushuntirish va Mantiq:
Anonim sinflar `new class` sintaksisi bilan e'lon qilinadi. Ular unit-testlarda va kichik bir martalik interfeys implementatsiyalarida juda qo'l keladi.

## Ishlash natijasi:
```text
[LOG]: Bir martalik anonim sinf muvaffaqiyatli ishladi
```

# 231-Topshiriq: Sinflarni funksiya parametri va return tipi sifatida ko'rsatish
## Topshiriq sharti:
Funksiyaga obyekt uzatish va yangi obyekt qaytarishni qat'iy tiplash bilan yozing.

## Yechim (PHP kodi):
```php
<?php

class Buyurtma {
    public function __construct(public int $id, public float $summa) {}
}

class HisobFaktura {
    public function __construct(public int $fakturaRaqam, public float $summa) {}
}

function fakturaYarat(Buyurtma $b): HisobFaktura {
    return new HisobFaktura($b->id + 1000, $b->summa);
}

$b = new Buyurtma(55, 340000);
$f = fakturaYarat($b);

echo "Faktura raqami: {$f->fakturaRaqam}, Summa: {$f->summa} so'm
";

```

## Tushuntirish va Mantiq:
Sinf nomlari xuddi skalyar tiplar (`int`, `string`) kabi to'laqonli parametr va qaytarish tipi sifatida ishlatilishi mumkin.

## Ishlash natijasi:
```text
Faktura raqami: 1055, Summa: 340000 so'm
```

# 232-Topshiriq: Data Transfer Object (DTO) namunasi PHP 8.2 da
## Topshiriq sharti:
API dan kelgan ma'lumotlarni qat'iy tiplangan readonly DTO ga joylang.

## Yechim (PHP kodi):
```php
<?php

readonly class FoydalanuvchiDTO {
    public function __construct(
        public string $ism,
        public string $email,
        public int $yosh
    ) {}

    public static function fromArray(array $data): self {
        return new self(
            ism: $data["ism"],
            email: $data["email"],
            yosh: (int)$data["yosh"]
        );
    }
}

$apiData = ["ism" => "Jamshid", "email" => "jamshid@khorazmiy.uz", "yosh" => 28];
$dto = FoydalanuvchiDTO::fromArray($apiData);

echo "DTO yaratildi: {$dto->ism} <{$dto->email}>
";

```

## Tushuntirish va Mantiq:
DTO (Data Transfer Object) tizim qismlari o'rtasida ma'lumotlarni strukturali va o'zgarmas holatda uzatish uchun xizmat qiladi.

## Ishlash natijasi:
```text
DTO yaratildi: Jamshid <jamshid@khorazmiy.uz>
```

# 233-Topshiriq: Value Object namunasi (Immutability va o'zini-o'zi validatsiya qilish)
## Topshiriq sharti:
Pochta indeksini ifodalovchi va noto'g'ri qiymatlarni rad etuvchi `PochtaIndeks` Value Object sinfini tuzing.

## Yechim (PHP kodi):
```php
<?php

readonly class PochtaIndeks {
    public string $qiymat;

    public function __construct(string $indeks) {
        if (!preg_match('/^\d{6}$/', $indeks)) {
            throw new InvalidArgumentException("Pochta indeksi aynan 6 ta raqam bo'lishi shart!");
        }
        $this->qiymat = $indeks;
    }

    public function equals(PochtaIndeks $boshqa): bool {
        return $this->qiymat === $boshqa->qiymat;
    }
}

$indeks1 = new PochtaIndeks("100000");
$indeks2 = new PochtaIndeks("100000");

echo "Tengmi: " . ($indeks1->equals($indeks2) ? "Ha" : "Yo'q") . "
";

```

## Tushuntirish va Mantiq:
Value Object - o'z shaxsiy identifikatoriga (ID) ega bo'lmagan, faqat o'z qiymati bilan belgilanadigan o'zgarmas obyektdir.

## Ishlash natijasi:
```text
Tengmi: Ha
```

# 234-Topshiriq: get_class(), get_called_class() va get_parent_class()
## Topshiriq sharti:
Sinf va uning ota sinfi haqidagi ma'lumotlarni dinamik aniqlang.

## Yechim (PHP kodi):
```php
<?php

class Baza {}
class Voris extends Baza {
    public function tahlil(): void {
        echo "Joriy sinf: " . get_class($this) . "
";
        echo "Ota sinf: " . get_parent_class($this) . "
";
    }
}

$v = new Voris();
$v->tahlil();

```

## Tushuntirish va Mantiq:
`get_class($obj)` obyekt sinfini, `get_parent_class($obj)` esa uning bevosita ota sinfi nomini qaytaradi.

## Ishlash natijasi:
```text
Joriy sinf: Voris
Ota sinf: Baza
```

# 235-Topshiriq: class_exists() va method_exists() dinamik tahlili
## Topshiriq sharti:
Sinf va uning ichidagi metod mavjudligini tekshirib, xavfsiz chaqirishni amalga oshiring.

## Yechim (PHP kodi):
```php
<?php

class Xizmat {
    public function bajar(): void {
        echo "Xizmat muvaffaqiyatli bajarildi.
";
    }
}

$sinfNomi = "Xizmat";
$metodNomi = "bajar";

if (class_exists($sinfNomi)) {
    $obj = new $sinfNomi();
    if (method_exists($obj, $metodNomi)) {
        $obj->$metodNomi();
    }
}

```

## Tushuntirish va Mantiq:
`class_exists()` va `method_exists()` dinamik tizimlarda, plaginlarda va marshrutlagichlarda xavfsizlik tekshiruvlari uchun xizmat qiladi.

## Ishlash natijasi:
```text
Xizmat muvaffaqiyatli bajarildi.
```

# 236-Topshiriq: property_exists() funksiyasi
## Topshiriq sharti:
Sinfda xususiyat mavjudligini obyektsiz hamda obyekt orqali tekshiring.

## Yechim (PHP kodi):
```php
<?php

class Sozlama {
    public string $nom = "Standart";
    private int $id = 1;
}

echo "nom bormi: " . (property_exists("Sozlama", "nom") ? "Ha" : "Yo'q") . "
";
echo "id bormi: " . (property_exists("Sozlama", "id") ? "Ha (hatto private bo'lsa ham)" : "Yo'q") . "
";
echo "noma'lum bormi: " . (property_exists("Sozlama", "nomalum") ? "Ha" : "Yo'q") . "
";

```

## Tushuntirish va Mantiq:
`property_exists()` xususiyat sinfda e'lon qilinganligini tekshiradi (hatto u `private` bo'lsa ham).

## Ishlash natijasi:
```text
nom bormi: Ha
id bormi: Ha (hatto private bo'lsa ham)
noma'lum bormi: Yo'q
```

# 237-Topshiriq: Obyektni massivga o'girish: (array)$obj
## Topshiriq sharti:
Obyektni `(array)` kasting operatori orqali assotsiativ massivga aylantiring.

## Yechim (PHP kodi):
```php
<?php

class Mahsulot {
    public string $nom = "Choynak";
    public int $narx = 45000;
}

$m = new Mahsulot();
$massiv = (array)$m;

print_r($massiv);

```

## Tushuntirish va Mantiq:
`(array)$obj` obyektning barcha public xususiyatlarini massiv kalitlariga aylantiradi.

## Ishlash natijasi:
```text
Array
(
    [nom] => Choynak
    [narx] => 45000
)
```

# 238-Topshiriq: Massivdan obyekt yasash: (object)$arr (stdClass)
## Topshiriq sharti:
Assotsiativ massivni `(object)` kasting orqali `stdClass` obyektiga aylantiring.

## Yechim (PHP kodi):
```php
<?php

$malumot = [
    "server" => "Ubuntu 24.04",
    "ram" => "16 GB"
];

$obj = (object)$malumot;

echo "Server: " . $obj->server . "
";
echo "RAM: " . $obj->ram . "
";
echo "Sinf: " . get_class($obj) . "
";

```

## Tushuntirish va Mantiq:
PHP dagi `stdClass` oddiy universal bo'sh sinf bo'lib, massivlarni tezkorlik bilan o'qilishi oson obyektlarga aylantirishda xizmat qiladi.

## Ishlash natijasi:
```text
Server: Ubuntu 24.04
RAM: 16 GB
Sinf: stdClass
```

# 239-Topshiriq: Dinamik xususiyatlarni taqiqlash va #[AllowDynamicProperties] (PHP 8.2)
## Topshiriq sharti:
PHP 8.2 da e'lon qilinmagan xususiyatlarni obyektga qo'shishdagi ogohlantirishni va atribut orqali ruxsat berishni tushuntiring.

## Yechim (PHP kodi):
```php
<?php

#[AllowDynamicProperties]
class DinamikObyekt {
    public string $asosiy = "Mavjud";
}

$d = new DinamikObyekt();
$d->yangiXususiyat = "Dinamik qo'shildi";

echo $d->yangiXususiyat . "
";

```

## Tushuntirish va Mantiq:
PHP 8.2 dan boshlab sinfda e'lon qilinmagan xususiyatlarni dinamik kiritish `Deprecated` hisoblanadi. Agar dinamik xususiyatlar zarur bo'lsa, sinf tepasiga `#[AllowDynamicProperties]` atributini qo'yish kerak.

## Ishlash natijasi:
```text
Dinamik qo'shildi
```

# 240-Topshiriq: Obyektlar havolasi va xotira boshqaruvi
## Topshiriq sharti:
Obyekt boshqa o'zgaruvchiga tayinlanganda nusxa emas, havola o'tishini isbotlang.

## Yechim (PHP kodi):
```php
<?php

class Hisob {
    public int $raqam = 10;
}

$a = new Hisob();
$b = $a; // Havola bo'yicha bog'lanadi

$b->raqam = 99;

echo "a->raqam: {$a->raqam}
";
echo "b->raqam: {$b->raqam}
";

```

## Tushuntirish va Mantiq:
PHP da obyektlar sukut bo'yicha identifikator havolasi orqali uzatiladi. `$b = $a` qilinganda ikkala o'zgaruvchi ham xotiradagi aynan bitta obyektga ishora qiladi.

## Ishlash natijasi:
```text
a->raqam: 99
b->raqam: 99
```

# 241-Topshiriq: WeakReference (Kuchsiz havolalar) PHP 7.4+
## Topshiriq sharti:
`WeakReference` yordamida Garbage Collector ga xalaqit bermasdan obyektga murojaat qilishni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

class KeshElement {
    public function __construct(public string $malumot) {}
}

$obj = new KeshElement("Muhim Kesh");
$havola = WeakReference::create($obj);

echo "Obyekt mavjudmi: " . ($havola->get() !== null ? "Ha" : "Yo'q") . "
";

unset($obj); // Asl obyekt xotiradan tozalanadi

echo "O'chirilgandan so'ng mavjudmi: " . ($havola->get() !== null ? "Ha" : "Yo'q") . "
";

```

## Tushuntirish va Mantiq:
`WeakReference` obyektning havola sanagichini (reference counter) oshirmaydi. Obyekt xotiradan o'chirilganda, kesh avtomatik ravishda `null` qaytaradi.

## Ishlash natijasi:
```text
Obyekt mavjudmi: Ha
O'chirilgandan so'ng mavjudmi: Yo'q
```

# 242-Topshiriq: ReflectionClass orqali sinf metama'lumotlarini o'qish
## Topshiriq sharti:
Reflection API yordamida sinfning metodlari va xususiyatlarini dastur ichida tahlil qiling.

## Yechim (PHP kodi):
```php
<?php

class MahsulotService {
    public function saqla(int $id, string $nom): bool {
        return true;
    }
}

$ref = new ReflectionClass(MahsulotService::class);

echo "Sinf nomi: " . $ref->getName() . "
";
foreach ($ref->getMethods() as $metod) {
    echo "Metod: " . $metod->getName() . "
";
}

```

## Tushuntirish va Mantiq:
Reflection API PHP kodining ichki tuzilishini, sinflarini, interfeyslarini, metodlari va ularning parametrlarini runtime da tekshirish imkonini beradi.

## Ishlash natijasi:
```text
Sinf nomi: MahsulotService
Metod: saqla
```

# 243-Topshiriq: ReflectionMethod orqali metod parametrlari va turlarini tahlil qilish
## Topshiriq sharti:
Metod qanday turdagi parametrlarni kutayotganini Reflection orqali aniqlang.

## Yechim (PHP kodi):
```php
<?php

class BuyurtmaService {
    public function tolov(int $buyurtmaId, float $summa): void {}
}

$refMetod = new ReflectionMethod(BuyurtmaService::class, "tolov");

foreach ($refMetod->getParameters() as $param) {
    echo "Parametr: {$param->getName()}, Tipi: {$param->getType()}
";
}

```

## Tushuntirish va Mantiq:
Dependency Injection konteynerlari (masalan, Laravel IoC Container) konstruktor parametrlarini aynan `ReflectionMethod` orqali o'qib, kerakli obyektlarni avtomatik yetkazib beradi.

## Ishlash natijasi:
```text
Parametr: buyurtmaId, Tipi: int
Parametr: summa, Tipi: float
```

# 244-Topshiriq: ReflectionProperty orqali private xususiyatni o'qish
## Topshiriq sharti:
Unit-testlarda yopiq (private) xususiyatlarni tekshirish uchun ReflectionProperty dan foydalanishni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

class Tizim {
    private string $maxfiyToken = "SEC_TOKEN_99812";
}

$tizim = new Tizim();

$refProp = new ReflectionProperty(Tizim::class, "maxfiyToken");
// PHP 8.1 dan boshlab setAccessible chaqirmasdan ham o'qish mumkin
$qiymat = $refProp->getValue($tizim);

echo "Private qiymat o'qildi: $qiymat
";

```

## Tushuntirish va Mantiq:
Reflection vositalari private chegaralarni chetlab o'tish imkonini beradi. Bu faqat testlash va freymvork ichki mexanizmlari uchun ishlatiladi.

## Ishlash natijasi:
```text
Private qiymat o'qildi: SEC_TOKEN_99812
```

# 245-Topshiriq: Method Chaining (Fluent Interface)
## Topshiriq sharti:
`return $this` orqali SQL Query Builder ga o'xshash zanjirli chaqiruv sintaksisini tuzing.

## Yechim (PHP kodi):
```php
<?php

class QueryBuilder {
    private string $jadval;
    private array $shartlar = [];

    public function table(string $jadval): self {
        $this->jadval = $jadval;
        return $this;
    }

    public function where(string $maydon, string $qiymat): self {
        $this->shartlar[] = "$maydon = '$qiymat'";
        return $this;
    }

    public function toSql(): string {
        $sql = "SELECT * FROM {$this->jadval}";
        if (!empty($this->shartlar)) {
            $sql .= " WHERE " . implode(" AND ", $this->shartlar);
        }
        return $sql;
    }
}

$sql = (new QueryBuilder())
    ->table("foydalanuvchilar")
    ->where("status", "faol")
    ->where("rol", "admin")
    ->toSql();

echo $sql . "
";

```

## Tushuntirish va Mantiq:
Method Chaining - metod oxirida `$this` obyektining o'zini qaytarish orqali ketma-ket zanjirli chaqiriqlarni (`$obj->a()->b()->c()`) amalga oshirishdir.

## Ishlash natijasi:
```text
SELECT * FROM foydalanuvchilar WHERE status = 'faol' AND rol = 'admin'
```

# 246-Topshiriq: Statik zavod metodi (Static Factory Method)
## Topshiriq sharti:
`new` o'rniga obyekt yaratishni nazorat qiluvchi statik zavod metodini yozing.

## Yechim (PHP kodi):
```php
<?php

class Harorat {
    private function __construct(public readonly float $selsiy) {}

    public static function fromKelvin(float $kelvin): self {
        return new self($kelvin - 273.15);
    }

    public static function fromFarengeyt(float $f): self {
        return new self(($f - 32) * 5 / 9);
    }
}

$h1 = Harorat::fromKelvin(300);
$h2 = Harorat::fromFarengeyt(86);

echo "300 K = " . round($h1->selsiy, 2) . " °C
";
echo "86 °F = " . round($h2->selsiy, 2) . " °C
";

```

## Tushuntirish va Mantiq:
Statik zavod metodlari (`from...`, `create...`) konstruktorni yashirib, turli xil ma'lumot manbalaridan obyektlarni tushunarli nomlar bilan yaratish imkonini beradi.

## Ishlash natijasi:
```text
300 K = 26.85 °C
86 °F = 30 °C
```

# 247-Topshiriq: Obyektlarni taqqoslash: == va === farqi
## Topshiriq sharti:
Ikkita obyektni `==` (qiymatlar bo'yicha) va `===` (havola bo'yicha) solishtiring.

## Yechim (PHP kodi):
```php
<?php

class Nuqta {
    public function __construct(public int $x, public int $y) {}
}

$p1 = new Nuqta(5, 10);
$p2 = new Nuqta(5, 10);
$p3 = $p1;

echo "p1 == p2 : " . ($p1 == $p2 ? "Teng (bir xil sinf va xususiyatlar)" : "Teng emas") . "
";
echo "p1 === p2: " . ($p1 === $p2 ? "Teng" : "Teng emas (turli xotira nusxalari)") . "
";
echo "p1 === p3: " . ($p1 === $p3 ? "Teng (aynan bir xil havola)" : "Teng emas") . "
";

```

## Tushuntirish va Mantiq:
`==` agar obyektlar bir xil sinfga tegishli bo'lsa va ularning barcha xususiyatlari teng bo'lsa `true` qaytaradi. `===` esa faqat ikkala o'zgaruvchi xotiradagi aynan bitta obyekt instansiyasiga ishora qilgandagina `true` bo'ladi.

## Ishlash natijasi:
```text
p1 == p2 : Teng (bir xil sinf va xususiyatlar)
p1 === p2: Teng emas (turli xotira nusxalari)
p1 === p3: Teng (aynan bir xil havola)
```

# 248-Topshiriq: spl_object_id() va spl_object_hash() orqali obyekt identifikatsiyasi
## Topshiriq sharti:
Har bir obyekt instansiyasining takrorlanmas tizim identifikatorini aniqlang.

## Yechim (PHP kodi):
```php
<?php

class KeshKalit {}

$k1 = new KeshKalit();
$k2 = new KeshKalit();

echo "k1 ID: " . spl_object_id($k1) . "
";
echo "k2 ID: " . spl_object_id($k2) . "
";
echo "ID lar farq qiladimi: " . (spl_object_id($k1) !== spl_object_id($k2) ? "Ha" : "Yo'q") . "
";

```

## Tushuntirish va Mantiq:
`spl_object_id($obj)` har bir yaratilgan tirik obyektga operatsion xotirada berilgan unikal butun son identifikatorini qaytaradi.

## Ishlash natijasi:
```text
k1 ID: 1
k2 ID: 2
ID lar farq qiladimi: Ha
```

# 249-Topshiriq: Null Object dizayn naqshi oddiy sinflar yordamida
## Topshiriq sharti:
Mijoz tizimga kirmagan holatda `null` tekshiruvlarini ko'paytirmaslik uchun `NullUser` sinfini yarating.

## Yechim (PHP kodi):
```php
<?php

class MehmonFoydalanuvchi {
    public function getIsm(): string {
        return "Mehmon";
    }

    public function tizimgaKirganmi(): bool {
        return false;
    }
}

class Ro'yxatdanOtganFoydalanuvchi {
    public function __construct(private string $ism) {}

    public function getIsm(): string {
        return $this->ism;
    }

    public function tizimgaKirganmi(): bool {
        return true;
    }
}

$user = new MehmonFoydalanuvchi();
echo "Salom, " . $user->getIsm() . "! Status: " . ($user->tizimgaKirganmi() ? "Autentifikatsiyadan o'tgan" : "Anonim") . "
";

```

## Tushuntirish va Mantiq:
Null Object pattern `null` qiymati o'rniga neytral yoki xavfsiz default harakatlarni bajaruvchi maxsus obyektni qaytarish orqali `if ($obj !== null)` tekshiruvlarini keskin kamaytiradi.

## Ishlash natijasi:
```text
Salom, Mehmon! Status: Anonim
```

# 250-Topshiriq: To'liq amaliy model: Mahsulot va inventar boshqaruvi
## Topshiriq sharti:
Obyektga yo'naltirilgan dasturlashning barcha asosiy tamoyillarini o'zida jamlagan mustahkam `Mahsulot` sinfini yozing.

## Yechim (PHP kodi):
```php
<?php

class Mahsulot {
    public function __construct(
        public readonly int $id,
        public string $nom,
        private float $narx,
        private int $omborda = 0
    ) {
        if ($this->narx < 0) {
            throw new InvalidArgumentException("Narx manfiy bo'lishi mumkin emas!");
        }
    }

    public function getNarx(): float {
        return $this->narx;
    }

    public function getOmborda(): int {
        return $this->omborda;
    }

    public function kirimQil(int $miqdor): void {
        $this->omborda += $miqdor;
        echo "Kirim qilindi: +$miqdor dona. Omborda jami: {$this->omborda}
";
    }

    public function sotish(int $miqdor): float {
        if ($miqdor > $this->omborda) {
            throw new RuntimeException("Omborda yetarli mahsulot mavjud emas!");
        }
        $this->omborda -= $miqdor;
        $jamiSumma = $miqdor * $this->narx;
        echo "Sotildi: $miqdor dona. Jami tushum: $jamiSumma so'm
";
        return $jamiSumma;
    }
}

$noutbuk = new Mahsulot(101, "Lenovo ThinkPad", 8500000, 10);
$noutbuk->kirimQil(5);
$noutbuk->sotish(3);
echo "Qoldiq: " . $noutbuk->getOmborda() . " dona
";

```

## Tushuntirish va Mantiq:
Ushbu modelda konstruktor validatsiyasi, xususiyatlarni himoyalash (inkapsulyatsiya), biznes operatsiyalari va istisnolarni tashlash to'liq va mukammal namoyish etilgan.

## Ishlash natijasi:
```text
Kirim qilindi: +5 dona. Omborda jami: 15
Sotildi: 3 dona. Jami tushum: 25500000 so'm
Qoldiq: 12 dona
```
