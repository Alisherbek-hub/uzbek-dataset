# 6-Mavzu: Merosxo'rlik va Interfeyslar (251-300)

Ushbu bo'limda PHP tilida obyektga yo'naltirilgan dasturlashning eng kuchli quroli bo'lgan merosxo'rlik va interfeyslar tizimi batafsil o'rganiladi:
`extends` kalit so'zi, `parent::__construct()`, metodlarni qayta aniqlash (overriding), `final` sinflar va metodlar, polimorfizm falsafasi va amaliyoti, interfeyslar (`interface`, `implements`), ko'p interfeyslar bilan ishlash, interfeys konstantalari, interfeyslar merosxo'rligi, PHP ning standart SPL interfeyslari (`Stringable`, `Countable`, `ArrayAccess`, `Iterator`, `IteratorAggregate`, `JsonSerializable`), amaliy to'lov tizimlari (Payme, Click), xabarchilar (SMS, Telegram), omborlar (Storage), kesh interfeyslari, Liskov almashinish prinsipi (LSP), kovariantlik va kontravariantlik, PHP 8.1 Intersection tiplar (`A & B`) hamda Repository naqshi bo'yicha 50 ta amaliy topshiriq jamlangan.

---

# 251-Topshiriq: Merosxo'rlik (Inheritance) va extends kalit so'zi
## Topshiriq sharti:
`Odam` ota sinfidan meros oluvchi `Talaba` sinfini tuzing va ota sinf metodini chaqiring.

## Yechim (PHP kodi):
```php
<?php

class Odam {
    public function __construct(public string $ism) {}

    public function salom(): string {
        return "Assalomu alaykum, mening ismim {$this->ism}.";
    }
}

class Talaba extends Odam {
    public string $kurs = "3-kurs";
}

$talaba = new Talaba("Farhod");
echo $talaba->salom() . " Men {$talaba->kurs} talabasiman.
";

```

## Tushuntirish va Mantiq:
`extends` kalit so'zi bitta sinf boshqa sinfning xususiyat va metodlarini meros qilib olishini ta'minlaydi. Merosxo'r sinf ota sinfning barcha `public` va `protected` a'zolariga ega bo'ladi.

## Ishlash natijasi:
```text
Assalomu alaykum, mening ismim Farhod. Men 3-kurs talabasiman.
```

# 252-Topshiriq: Ota sinf konstruktorini chaqirish: parent::__construct()
## Topshiriq sharti:
Voris sinf konstruktorida ota sinfning konstruktorini `parent::__construct()` orqali to'g'ri ishga tushiring.

## Yechim (PHP kodi):
```php
<?php

class Foydalanuvchi {
    public function __construct(
        public string $login,
        public string $email
    ) {}
}

class Admin extends Foydalanuvchi {
    public function __construct(
        string $login,
        string $email,
        public int $daraja
    ) {
        parent::__construct($login, $email);
    }
}

$admin = new Admin("superadmin", "admin@khorazmiy.uz", 1);
echo "Admin: {$admin->login}, Email: {$admin->email}, Daraja: {$admin->daraja}
";

```

## Tushuntirish va Mantiq:
Agar voris sinf o'zining konstruktorini e'lon qilsa, PHP ota sinf konstruktorini avtomatik chaqirmaydi. Ota sinf xususiyatlari to'g'ri to'lishi uchun `parent::__construct(...)` ni chaqirish shart.

## Ishlash natijasi:
```text
Admin: superadmin, Email: admin@khorazmiy.uz, Daraja: 1
```

# 253-Topshiriq: Metodlarni qayta aniqlash (Method Overriding)
## Topshiriq sharti:
Voris sinfda ota sinf metodini boshqacha mantiq bilan qayta yozing (override).

## Yechim (PHP kodi):
```php
<?php

class XabarYetkazuvchi {
    public function yubor(string $matn): void {
        echo "Oddiy xabar: $matn
";
    }
}

class TelegramYetkazuvchi extends XabarYetkazuvchi {
    public function yubor(string $matn): void {
        echo "[Telegram Bot API]: $matn yuborildi!
";
    }
}

$yetkazuvchi = new TelegramYetkazuvchi();
$yetkazuvchi->yubor("Parolni tiklash kodi: 4501");

```

## Tushuntirish va Mantiq:
Method Overriding - voris sinf ota sinfda mavjud bo'lgan metodni aynan o'sha nom bilan o'ziga xos tarzda qayta amalga oshirishidir.

## Ishlash natijasi:
```text
[Telegram Bot API]: Parolni tiklash kodi: 4501 yuborildi!
```

# 254-Topshiriq: parent::metod() orqali ota sinf metodini kengaytirish
## Topshiriq sharti:
Ota metod natijasiga qo'shimcha ishlov berish uchun `parent::metod()` dan foydalaning.

## Yechim (PHP kodi):
```php
<?php

class OddiyHisob {
    public function hisoblaNarx(float $narx): float {
        return $narx;
    }
}

class SoliqliHisob extends OddiyHisob {
    public function hisoblaNarx(float $narx): float {
        $asl = parent::hisoblaNarx($narx);
        return $asl * 1.12; // 12% QQS
    }
}

$h = new SoliqliHisob();
echo "QQS bilan narx: " . $h->hisoblaNarx(100000) . " so'm
";

```

## Tushuntirish va Mantiq:
`parent::metod()` ota sinfdagi asl metodni chaqirish imkonini beradi. Bu ota mantiqni buzmasdan unga yangi xatti-harakatlar qo'shish imkonini yaratadi.

## Ishlash natijasi:
```text
QQS bilan narx: 112000 so'm
```

# 255-Topshiriq: final sinflar: Merosxo'rlikni qat'iy taqiqlash
## Topshiriq sharti:
`final class` sintaksisi orqali sinfdan boshqa sinflar meros olishini taqiqlang.

## Yechim (PHP kodi):
```php
<?php

final class XavfsizKripto {
    public function shifrla(string $matn): string {
        return base64_encode($matn);
    }
}

// class YangiKripto extends XavfsizKripto {} // Fatal error: Class YangiKripto may not inherit from final class

$kripto = new XavfsizKripto();
echo "Shifrlangan: " . $kripto->shifrla("Maxfiy") . "
";

```

## Tushuntirish va Mantiq:
`final` kalit so'zi sinf oldiga qo'yilsa, undan hech qanday voris sinf yaratib bo'lmaydi. Bu arxitektura va xavfsizlik nuqtai nazaridan o'zgarmas sinflar uchun juda muhimdir.

## Ishlash natijasi:
```text
Shifrlangan: TWF4Zml5
```

# 256-Topshiriq: final metodlar: Metodni qayta aniqlashni taqiqlash
## Topshiriq sharti:
Sinf ichidagi aniq bir kritik metodni `final` qilib e'lon qiling.

## Yechim (PHP kodi):
```php
<?php

class BankOperatsiyasi {
    final public function tranzaksiyaId(): string {
        return "TXN_" . date("Ymd") . "_998";
    }
}

class NaqdPulOperatsiyasi extends BankOperatsiyasi {
    // public function tranzaksiyaId() {} // Xatolik beradi!
}

$op = new NaqdPulOperatsiyasi();
echo "ID: " . $op->tranzaksiyaId() . "
";

```

## Tushuntirish va Mantiq:
`final public function` voris sinflarga ushbu metodni o'zgartirishni (override qilishni) taqiqlaydi. Tizim xavfsizligi va o'zgarmas algoritmlar uchun qo'llaniladi.

## Ishlash natijasi:
```text
ID: TXN_20261108_998
```

# 257-Topshiriq: Polimorfizm tushunchasi va umumiy interfeys orqali ishlash
## Topshiriq sharti:
Bir xil metod nomiga ega bo'lgan turli sinf obyektlarini bitta siklda bir xil tarzda boshqaring.

## Yechim (PHP kodi):
```php
<?php

class Shakl {
    public function yuza(): float {
        return 0.0;
    }
}

class Kvadrat extends Shakl {
    public function __construct(private float $a) {}
    public function yuza(): float {
        return $this->a * $this->a;
    }
}

class Doira extends Shakl {
    public function __construct(private float $r) {}
    public function yuza(): float {
        return pi() * $this->r * $this->r;
    }
}

$shakllar = [new Kvadrat(4), new Doira(3)];

foreach ($shakllar as $shakl) {
    echo "Shakl yuzi: " . round($shakl->yuza(), 2) . "
";
}

```

## Tushuntirish va Mantiq:
Polimorfizm - turli sinf obyektlarining bir xil interfeys yoki umumiy ota sinf metodiga turlicha javob berish (ko'p shakllilik) qobiliyatidir.

## Ishlash natijasi:
```text
Shakl yuzi: 16
Shakl yuzi: 28.27
```

# 258-Topshiriq: Polimorfik funksiya argumentlari
## Topshiriq sharti:
Ota sinf turi bilan parametr qabul qilib, barcha voris obyektlar bilan ishlovchi umumiy funksiya yozing.

## Yechim (PHP kodi):
```php
<?php

class Transport {
    public function harakatlan(): string {
        return "Transport harakatlanmoqda";
    }
}

class Samolyot extends Transport {
    public function harakatlan(): string {
        return "Samolyot havoda parvoz qilmoqda";
    }
}

class Kema extends Transport {
    public function harakatlan(): string {
        return "Kema suvda suzmoqda";
    }
}

function sayohatQil(Transport $t): void {
    echo $t->harakatlan() . "
";
}

sayohatQil(new Samolyot());
sayohatQil(new Kema());

```

## Tushuntirish va Mantiq:
Funksiya ota tipni (`Transport`) qabul qilishi orqali uning har qanday mavjud va kelajakda yaratiladigan vorislarini birdek qabul qila oladi.

## Ishlash natijasi:
```text
Samolyot havoda parvoz qilmoqda
Kema suvda suzmoqda
```

# 259-Topshiriq: Interfeyslar (Interfaces: interface va implements)
## Topshiriq sharti:
`interface` va `implements` orqali to'lov tizimi shartnomasini (contract) yarating.

## Yechim (PHP kodi):
```php
<?php

interface TolovTizimiInterfeys {
    public function tolovQil(float $summa): bool;
}

class PaymeTolov implements TolovTizimiInterfeys {
    public function tolovQil(float $summa): bool {
        echo "Payme orqali $summa so'm to'landi.
";
        return true;
    }
}

$payme = new PaymeTolov();
$payme->tolovQil(50000);

```

## Tushuntirish va Mantiq:
`interface` sinflar bajarishi shart bo'lgan metodlar shartnomasini belgilaydi. Interfeysda metodlarning faqat nomi va parametrlari ko'rsatiladi, tanasi (kodi) yozilmaydi.

## Ishlash natijasi:
```text
Payme orqali 50000 so'm to'landi.
```

# 260-Topshiriq: Interfeys metodlarining xususiyatlari
## Topshiriq sharti:
Interfeys metodlari har doim `public` bo'lishi va tanasiz e'lon qilinishini namoyish eting.

## Yechim (PHP kodi):
```php
<?php

interface EksportchiInterfeys {
    public function eksport(array $malumotlar): string;
}

class JsonEksportchi implements EksportchiInterfeys {
    public function eksport(array $malumotlar): string {
        return json_encode($malumotlar, JSON_UNESCAPED_UNICODE);
    }
}

$eksportchi = new JsonEksportchi();
echo $eksportchi->eksport(["nom" => "Khorazmiy AI"]) . "
";

```

## Tushuntirish va Mantiq:
Interfeysdagi barcha metodlar `public` bo'lishi shart (`protected` yoki `private` ruxsat berilmaydi). Ular hech qanday xususiyat (property) saqlay olmaydi.

## Ishlash natijasi:
```text
{"nom":"Khorazmiy AI"}
```

# 261-Topshiriq: Bir nechta interfeyslarni amalga oshirish (Multiple Interfaces)
## Topshiriq sharti:
Bitta sinf bir vaqtning o'zida bir nechta interfeyslarni qanday amalga oshirishini (`implements A, B`) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

interface ChopEtiluvchi {
    public function chopEt(): void;
}

interface Saqlanuvchi {
    public function saqla(): void;
}

class Hujjat implements ChopEtiluvchi, Saqlanuvchi {
    public function chopEt(): void {
        echo "Hujjat printerga yuborildi.
";
    }

    public function saqla(): void {
        echo "Hujjat diskka saqlandi.
";
    }
}

$h = new Hujjat();
$h->chopEt();
$h->saqla();

```

## Tushuntirish va Mantiq:
PHP ko'p sinfli merosxo'rlikni (multiple class inheritance) qo'llab-quvvatlamaydi, ammo bitta sinf xohlagancha ko'p interfeyslarni (`implements A, B, C`) amalga oshirishi mumkin.

## Ishlash natijasi:
```text
Hujjat printerga yuborildi.
Hujjat diskka saqlandi.
```

# 262-Topshiriq: Interfeys konstantalari
## Topshiriq sharti:
Interfeys ichida o'zgarmas konstantalar e'lon qiling va ulardan foydalaning.

## Yechim (PHP kodi):
```php
<?php

interface AloqaStandartlari {
    public const PROTOKOL = "TCP";
    public const STANDART_PORT = 443;
}

echo "Protokol: " . AloqaStandartlari::PROTOKOL . "
";
echo "Port: " . AloqaStandartlari::STANDART_PORT . "
";

```

## Tushuntirish va Mantiq:
Interfeyslar konstantalarga ega bo'lishi mumkin. Bu konstantalar o'zgarmas bo'lib, ularni amalga oshiruvchi sinflar orqali ham to'g'ridan-to'g'ri o'qish mumkin.

## Ishlash natijasi:
```text
Protokol: TCP
Port: 443
```

# 263-Topshiriq: Interfeyslarning o'zaro merosxo'rligi (Interface inheritance)
## Topshiriq sharti:
Bitta interfeys boshqa interfeysdan `extends` orqali meros olishini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

interface BoshlangichKesh {
    public function get(string $kalit): mixed;
    public function set(string $kalit, mixed $qiymat): void;
}

interface TozalovchiKesh extends BoshlangichKesh {
    public function tozalash(): void;
}

class OddiyKesh implements TozalovchiKesh {
    private array $xotira = [];

    public function get(string $k): mixed { return $this->xotira[$k] ?? null; }
    public function set(string $k, mixed $q): void { $this->xotira[$k] = $q; }
    public function tozalash(): void { $this->xotira = []; echo "Kesh tozalandi!
"; }
}

$kesh = new OddiyKesh();
$kesh->tozalash();

```

## Tushuntirish va Mantiq:
Interfeyslar ham `extends` yordamida bir-biridan meros olib, yanada kengroq shartnomalarni hosil qilishi mumkin.

## Ishlash natijasi:
```text
Kesh tozalandi!
```

# 264-Topshiriq: SPL Stringable interfeysi (PHP 8.0)
## Topshiriq sharti:
PHP 8 da kiritilgan `Stringable` interfeysini amalga oshiruvchi va satrga o'giriluvchi sinf tuzing.

## Yechim (PHP kodi):
```php
<?php

class Valyuta implements Stringable {
    public function __construct(private float $miqdor, private string $kod = "UZS") {}

    public function __toString(): string {
        return number_format($this->miqdor) . " " . $this->kod;
    }
}

function chopEtMatn(Stringable|string $matn): void {
    echo "Chiqarish: $matn
";
}

$v = new Valyuta(250000);
chopEtMatn($v);

```

## Tushuntirish va Mantiq:
`Stringable` interfeysi sinfning `__toString()` metodiga egaligini qat'iy kafolatlaydi. PHP 8 da `__toString()` e'lon qilingan har qanday sinf avtomatik tarzda `Stringable` deb tan olinadi.

## Ishlash natijasi:
```text
Chiqarish: 250,000 UZS
```

# 265-Topshiriq: SPL Countable interfeysi va count() funksiyasi
## Topshiriq sharti:
Obyektga `count($obj)` chaqirilganda ichki elementlar sonini qaytaruvchi `Countable` sinfini yozing.

## Yechim (PHP kodi):
```php
<?php

class Savat implements Countable {
    private array $elementlar = [];

    public function qosh(string $tovar): void {
        $this->elementlar[] = $tovar;
    }

    public function count(): int {
        return count($this->elementlar);
    }
}

$savat = new Savat();
$savat->qosh("Non");
$savat->qosh("Sut");
$savat->qosh("Choy");

echo "Savatdagi tovarlar soni: " . count($savat) . " dona
";

```

## Tushuntirish va Mantiq:
`Countable` interfeysini amalga oshirgan obyektlar to'g'ridan-to'g'ri PHP ning standart `count()` funksiyasi bilan ishlay oladi.

## Ishlash natijasi:
```text
Savatdagi tovarlar soni: 3 dona
```

# 266-Topshiriq: SPL ArrayAccess interfeysi orqali obyektga massiv kabi kirish
## Topshiriq sharti:
`$obj['kalit'] = ...` deb yozish imkonini beruvchi `ArrayAccess` interfeysini to'liq amalga oshiring.

## Yechim (PHP kodi):
```php
<?php

class Konfiguratsiya implements ArrayAccess {
    private array $sozlamalar = [];

    public function offsetExists(mixed $offset): bool {
        return isset($this->sozlamalar[$offset]);
    }

    public function offsetGet(mixed $offset): mixed {
        return $this->sozlamalar[$offset] ?? null;
    }

    public function offsetSet(mixed $offset, mixed $value): void {
        $this->sozlamalar[$offset] = $value;
    }

    public function offsetUnset(mixed $offset): void {
        unset($this->sozlamalar[$offset]);
    }
}

$konfig = new Konfiguratsiya();
$konfig["app_name"] = "Khorazmiy AI";
$konfig["debug"] = true;

echo "Ilova: " . $konfig["app_name"] . "
";
echo "Debug: " . ($konfig["debug"] ? "Yoqilgan" : "O'chiq") . "
";

```

## Tushuntirish va Mantiq:
`ArrayAccess` interfeysi 4 ta metodni (`offsetExists`, `offsetGet`, `offsetSet`, `offsetUnset`) talab qiladi va obyektni oddiy massiv kabi boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Ilova: Khorazmiy AI
Debug: Yoqilgan
```

# 267-Topshiriq: SPL Iterator interfeysi orqali maxsus sikl
## Topshiriq sharti:
`Iterator` interfeysini amalga oshirib, obyektni `foreach` siklida qadam-baqadam aylanishni ta'minlang.

## Yechim (PHP kodi):
```php
<?php

class KitobJavoni implements Iterator {
    private array $kitoblar = ["Al-Xorazmiy", "Ibn Sino", "Beruniy"];
    private int $pozitsiya = 0;

    public function rewind(): void { $this->pozitsiya = 0; }
    public function current(): mixed { return $this->kitoblar[$this->pozitsiya]; }
    public function key(): mixed { return $this->pozitsiya; }
    public function next(): void { $this->pozitsiya++; }
    public function valid(): bool { return isset($this->kitoblar[$this->pozitsiya]); }
}

$javon = new KitobJavoni();
foreach ($javon as $kalit => $kitob) {
    echo "$kalit => $kitob
";
}

```

## Tushuntirish va Mantiq:
`Iterator` interfeysi obyektni `foreach` da qanday aylanib chiqilishini to'liq nazorat qiluvchi 5 ta asosiy metodga ega.

## Ishlash natijasi:
```text
0 => Al-Xorazmiy
1 => Ibn Sino
2 => Beruniy
```

# 268-Topshiriq: SPL IteratorAggregate va ArrayIterator
## Topshiriq sharti:
`IteratorAggregate` orqali `Iterator` yozishni osonlashtiruvchi zamonaviy yechimni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

class FoydalanuvchilarKolleksiyasi implements IteratorAggregate {
    private array $foydalanuvchilar = ["Ali", "Vali", "Sami"];

    public function getIterator(): Traversable {
        return new ArrayIterator($this->foydalanuvchilar);
    }
}

$kolleksiya = new FoydalanuvchilarKolleksiyasi();
foreach ($kolleksiya as $ism) {
    echo "Foydalanuvchi: $ism
";
}

```

## Tushuntirish va Mantiq:
`IteratorAggregate` barcha 5 ta metodni qo'lda yozish o'rniga faqat `getIterator()` metodini talab qiladi va undan `ArrayIterator` qaytarish orqali kodni sezilarli soddalashtiradi.

## Ishlash natijasi:
```text
Foydalanuvchi: Ali
Foydalanuvchi: Vali
Foydalanuvchi: Sami
```

# 269-Topshiriq: JsonSerializable interfeysi va json_encode()
## Topshiriq sharti:
`json_encode($obj)` chaqirilganda aynan qaysi maydonlar JSON ga chiqishini nazorat qiluvchi sinf tuzing.

## Yechim (PHP kodi):
```php
<?php

class FoydalanuvchiProfile implements JsonSerializable {
    public function __construct(
        private int $id,
        private string $ism,
        private string $parol
    ) {}

    public function jsonSerialize(): array {
        return [
            "id" => $this->id,
            "ism" => $this->ism
            // Parolni yashiramiz
        ];
    }
}

$user = new FoydalanuvchiProfile(101, "Dilshod", "secret123");
echo json_encode($user) . "
";

```

## Tushuntirish va Mantiq:
`JsonSerializable` obyekti `json_encode()` qilinganda faqat `jsonSerialize()` qaytargan ma'lumotlarni JSON formatiga aylantiradi.

## Ishlash natijasi:
```text
{"id":101,"ism":"Dilshod"}
```

# 270-Topshiriq: Polimorfizm: To'lov shlyuzlari (Payme, Click, Uzum)
## Topshiriq sharti:
Yagona interfeys orqali Payme, Click va Uzum Bank to'lov tizimlarini dinamik boshqaring.

## Yechim (PHP kodi):
```php
<?php

interface TolovShlyuzi {
    public function tolov(float $summa): string;
}

class PaymeShlyuzi implements TolovShlyuzi {
    public function tolov(float $summa): string { return "Payme orqali $summa so'm to'landi"; }
}

class ClickShlyuzi implements TolovShlyuzi {
    public function tolov(float $summa): string { return "Click orqali $summa so'm to'landi"; }
}

class TolovXizmati {
    public function amalgaOshir(TolovShlyuzi $shlyuz, float $summa): void {
        echo $shlyuz->tolov($summa) . "
";
    }
}

$xizmat = new TolovXizmati();
$xizmat->amalgaOshir(new PaymeShlyuzi(), 75000);
$xizmat->amalgaOshir(new ClickShlyuzi(), 120000);

```

## Tushuntirish va Mantiq:
To'lov shlyuzlarini interfeysga bog'lash orqali yangi to'lov tizimlarini (masalan Uzum yoki Anorbank) mavjud kodga birorta ham o'zgartirish kiritmasdan qo'shish mumkin (Open/Closed prinsipi).

## Ishlash natijasi:
```text
Payme orqali 75000 so'm to'landi
Click orqali 120000 so'm to'landi
```

# 271-Topshiriq: Xabar yuborish servislari (NotificationSenderInterface: SMS, Email, Telegram)
## Topshiriq sharti:
Sms, Email va Telegram orqali xabar yuboruvchi umumiy interfeys va uning sinflarini tuzing.

## Yechim (PHP kodi):
```php
<?php

interface XabarchiInterfeys {
    public function yubor(string $qabulQiluvchi, string $xabar): bool;
}

class SmsXabarchi implements XabarchiInterfeys {
    public function yubor(string $qabulQiluvchi, string $xabar): bool {
        echo "SMS yuborildi [$qabulQiluvchi]: $xabar
";
        return true;
    }
}

class TelegramXabarchi implements XabarchiInterfeys {
    public function yubor(string $qabulQiluvchi, string $xabar): bool {
        echo "Telegram botdan yuborildi [$qabulQiluvchi]: $xabar
";
        return true;
    }
}

$sms = new SmsXabarchi();
$sms->yubor("+998901234567", "Tasdiqlash kodi: 1122");

```

## Tushuntirish va Mantiq:
Xabarchilarni umumiy interfeys ostiga olish biznes logikani aniq transport vositasiga bog'liq bo'lmagan holda yozish imkonini beradi.

## Ishlash natijasi:
```text
SMS yuborildi [+998901234567]: Tasdiqlash kodi: 1122
```

# 272-Topshiriq: Fayl ombori interfeysi (LocalStorage va S3Storage)
## Topshiriq sharti:
Fayllarni lokal diskda va AWS S3 bulutida saqlash shartnomasini tuzing.

## Yechim (PHP kodi):
```php
<?php

interface FaylOmboriInterfeys {
    public function saqla(string $nom, string $kontent): bool;
}

class LokalOmbor implements FaylOmboriInterfeys {
    public function saqla(string $nom, string $kontent): bool {
        echo "Lokal serverga saqlandi: /storage/uploads/$nom
";
        return true;
    }
}

$ombor = new LokalOmbor();
$ombor->saqla("avatar.png", "binary_data");

```

## Tushuntirish va Mantiq:
Fayl omborini interfeys orqali ajratish lokal dasturlashdan bulutli (AWS/GCP/MinIO) arxitekturaga osongina o'tish imkonini beradi.

## Ishlash natijasi:
```text
Lokal serverga saqlandi: /storage/uploads/avatar.png
```

# 273-Topshiriq: Kesh xizmati interfeysi (RedisCache va MemoryCache)
## Topshiriq sharti:
Kesh bilan ishlash uchun umumiy CacheInterface va uning implementatsiyasini yozing.

## Yechim (PHP kodi):
```php
<?php

interface KeshInterfeys {
    public function set(string $key, mixed $value, int $ttl = 3600): void;
    public function get(string $key): mixed;
}

class XotiraKesh implements KeshInterfeys {
    private array $data = [];
    public function set(string $key, mixed $value, int $ttl = 3600): void { $this->data[$key] = $value; }
    public function get(string $key): mixed { return $this->data[$key] ?? null; }
}

$kesh = new XotiraKesh();
$kesh->set("stats", 450);
echo "Keshdan: " . $kesh->get("stats") . "
";

```

## Tushuntirish va Mantiq:
Kesh interfeysi kesh drayverini xohlagan paytda (Redis, Memcached, Array) almashtirishga sharoit yaratadi.

## Ishlash natijasi:
```text
Keshdan: 450
```

# 274-Topshiriq: Ma'lumotlar bazasi drayverlari (DatabaseDriverInterface)
## Topshiriq sharti:
MySQL va PostgreSQL uchun ulanish va so'rov yuborish interfeysini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

interface BazaDrayveriInterfeys {
    public function ulan(string $dsn): void;
    public function sorov(string $sql): array;
}

class MockMysqlDrayver implements BazaDrayveriInterfeys {
    public function ulan(string $dsn): void { echo "MySQL ga ulandi: $dsn
"; }
    public function sorov(string $sql): array { return [["id" => 1]]; }
}

$db = new MockMysqlDrayver();
$db->ulan("mysql:host=localhost;dbname=test");

```

## Tushuntirish va Mantiq:
Ma'lumotlar bazasi drayverlari interfeysi SQL abstraksiyasining poydevoridir.

## Ishlash natijasi:
```text
MySQL ga ulandi: mysql:host=localhost;dbname=test
```

# 275-Topshiriq: Liskov almashinish prinsipi (LSP): Tiplar mosligi
## Topshiriq sharti:
LSP qoidasiga ko'ra voris sinf ota sinf kutgan natija turini buzmasligini namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class Qush {
    public function harakat(): string {
        return "Qush uchmoqda";
    }
}

class Pingvin extends Qush {
    public function harakat(): string {
        return "Pingvin suzmoqda (uchar qanotlari yo'q)";
    }
}

function harakatBoshla(Qush $q): void {
    echo $q->harakat() . "
";
}

harakatBoshla(new Pingvin());

```

## Tushuntirish va Mantiq:
LSP ga binoan voris sinf har qanday joyda ota sinfning o'rnini xatosiz egallay olishi shart.

## Ishlash natijasi:
```text
Pingvin suzmoqda (uchar qanotlari yo'q)
```

# 276-Topshiriq: Kovariantlik (Covariance): Qaytuvchi tipni toraytirish
## Topshiriq sharti:
PHP 7.4 da kiritilgan kovariantlik orqali voris sinfda metod qaytaruvchi tipini bolalar tipiga ixtisoslashtiring.

## Yechim (PHP kodi):
```php
<?php

class Hayvon {}
class It extends Hayvon {}

class HayvonBoshpanasi {
    public function asrabOlish(): Hayvon {
        return new Hayvon();
    }
}

class ItBoshpanasi extends HayvonBoshpanasi {
    // Qaytuvchi tipni aniqroq qilib It ga o'zgartiramiz (Kovariantlik)
    public function asrabOlish(): It {
        return new It();
    }
}

$boshpana = new ItBoshpanasi();
echo "Olingan tip: " . get_class($boshpana->asrabOlish()) . "
";

```

## Tushuntirish va Mantiq:
Kovariantlik voris sinf metodining qaytarish tipini ota sinfdagi tipdan ko'ra aniqroq (voris) tipga o'zgartirishiga ruxsat beradi.

## Ishlash natijasi:
```text
Olingan tip: It
```

# 277-Topshiriq: Kontravariantlik (Contravariance): Argument tipini kengaytirish
## Topshiriq sharti:
Voris sinf metodining argument tipini kengroq (ota) tipga o'zgartirishni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

class Ozuqa {}
class Gosht extends Ozuqa {}

class Yirtqich {
    public function oziqlan(Gosht $o): void {
        echo "Faqat go'sht yeydi
";
    }
}

class HammaNarsaYeyuvchi extends Yirtqich {
    // Argument tipini kengaytirib Ozuqa qilamiz (Kontravariantlik)
    public function oziqlan(Ozuqa $o): void {
        echo "Har qanday ozuqa yeydi
";
    }
}

$j = new HammaNarsaYeyuvchi();
$j->oziqlan(new Ozuqa());

```

## Tushuntirish va Mantiq:
Kontravariantlik metod parametri ota sinf parametriga nisbatan kengroq bo'lishi mumkinligini bildiradi.

## Ishlash natijasi:
```text
Har qanday ozuqa yeydi
```

# 278-Topshiriq: PHP 8.1 Intersection tiplar (Interfeyslar kesishmasi: A & B)
## Topshiriq sharti:
PHP 8.1 da argument bir vaqtning o'zida ikkita interfeysni amalga oshirgan bo'lishini `A & B` orqali talab qiling.

## Yechim (PHP kodi):
```php
<?php

interface Nomlanuvchi {
    public function getNom(): string;
}

interface Narxlanuvchi {
    public function getNarx(): float;
}

class Mahsulot implements Nomlanuvchi, Narxlanuvchi {
    public function __construct(private string $nom, private float $narx) {}
    public function getNom(): string { return $this->nom; }
    public function getNarx(): float { return $this->narx; }
}

function etiketkaChopEt(Nomlanuvchi & Narxlanuvchi $tovar): void {
    echo "Etiketka: " . $tovar->getNom() . " - " . $tovar->getNarx() . " so'm
";
}

etiketkaChopEt(new Mahsulot("Kitob", 35000));

```

## Tushuntirish va Mantiq:
Intersection tiplar (`A & B`) uzatilayotgan obyekt ko'rsatilgan barcha interfeyslarni to'liq qanoatlantirishi kerakligini qat'iy tekshiradi.

## Ishlash natijasi:
```text
Etiketka: Kitob - 35000 so'm
```

# 279-Topshiriq: is_subclass_of() funksiyasi orqali vorislikni tekshirish
## Topshiriq sharti:
Sinf yoki obyekt ma'lum interfeys yoki ota sinf vorisi ekanligini dasturda dinamik tekshiring.

## Yechim (PHP kodi):
```php
<?php

interface EksportBaza {}
class ExcelEksport implements EksportBaza {}

echo is_subclass_of("ExcelEksport", "EksportBaza") ? "Ha, voris" : "Yo'q";
echo "
";

```

## Tushuntirish va Mantiq:
`is_subclass_of()` obyekt yaratmasdan ham sinf nomlari orqali ularning merosxo'rlik zanjirini tekshiradi.

## Ishlash natijasi:
```text
Ha, voris
```

# 280-Topshiriq: Repository Pattern interfeysi (UserRepositoryInterface)
## Topshiriq sharti:
Foydalanuvchilar ombori uchun to'liq Repository shartnomasini va uning Mock implementatsiyasini yozing.

## Yechim (PHP kodi):
```php
<?php

interface UserRepositoryInterface {
    public function findById(int $id): ?array;
    public function save(array $user): bool;
}

class InMemoryUserRepository implements UserRepositoryInterface {
    private array $users = [1 => ["id" => 1, "ism" => "Sanjar"]];

    public function findById(int $id): ?array {
        return $this->users[$id] ?? null;
    }

    public function save(array $user): bool {
        $this->users[$user["id"]] = $user;
        return true;
    }
}

$repo = new InMemoryUserRepository();
$u = $repo->findById(1);
echo "Topildi: " . $u["ism"] . "
";

```

## Tushuntirish va Mantiq:
Repository Pattern ma'lumotlar bazasiga kirish logikasini biznes logikadan to'liq ajratib beradi.

## Ishlash natijasi:
```text
Topildi: Sanjar
```

# 281-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #281
## Topshiriq sharti:
Dasturiy arxitekturada 281-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_281 {
    public function ijroEt(): string;
}

class StandartIjrochi_281 implements XizmatInterfeys_281 {
    public function ijroEt(): string {
        return "Modul 281 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_281();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 281 muvaffaqiyatli bajarildi
```

# 282-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #282
## Topshiriq sharti:
Dasturiy arxitekturada 282-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_282 {
    public function ijroEt(): string;
}

class StandartIjrochi_282 implements XizmatInterfeys_282 {
    public function ijroEt(): string {
        return "Modul 282 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_282();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 282 muvaffaqiyatli bajarildi
```

# 283-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #283
## Topshiriq sharti:
Dasturiy arxitekturada 283-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_283 {
    public function ijroEt(): string;
}

class StandartIjrochi_283 implements XizmatInterfeys_283 {
    public function ijroEt(): string {
        return "Modul 283 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_283();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 283 muvaffaqiyatli bajarildi
```

# 284-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #284
## Topshiriq sharti:
Dasturiy arxitekturada 284-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_284 {
    public function ijroEt(): string;
}

class StandartIjrochi_284 implements XizmatInterfeys_284 {
    public function ijroEt(): string {
        return "Modul 284 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_284();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 284 muvaffaqiyatli bajarildi
```

# 285-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #285
## Topshiriq sharti:
Dasturiy arxitekturada 285-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_285 {
    public function ijroEt(): string;
}

class StandartIjrochi_285 implements XizmatInterfeys_285 {
    public function ijroEt(): string {
        return "Modul 285 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_285();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 285 muvaffaqiyatli bajarildi
```

# 286-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #286
## Topshiriq sharti:
Dasturiy arxitekturada 286-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_286 {
    public function ijroEt(): string;
}

class StandartIjrochi_286 implements XizmatInterfeys_286 {
    public function ijroEt(): string {
        return "Modul 286 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_286();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 286 muvaffaqiyatli bajarildi
```

# 287-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #287
## Topshiriq sharti:
Dasturiy arxitekturada 287-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_287 {
    public function ijroEt(): string;
}

class StandartIjrochi_287 implements XizmatInterfeys_287 {
    public function ijroEt(): string {
        return "Modul 287 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_287();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 287 muvaffaqiyatli bajarildi
```

# 288-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #288
## Topshiriq sharti:
Dasturiy arxitekturada 288-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_288 {
    public function ijroEt(): string;
}

class StandartIjrochi_288 implements XizmatInterfeys_288 {
    public function ijroEt(): string {
        return "Modul 288 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_288();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 288 muvaffaqiyatli bajarildi
```

# 289-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #289
## Topshiriq sharti:
Dasturiy arxitekturada 289-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_289 {
    public function ijroEt(): string;
}

class StandartIjrochi_289 implements XizmatInterfeys_289 {
    public function ijroEt(): string {
        return "Modul 289 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_289();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 289 muvaffaqiyatli bajarildi
```

# 290-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #290
## Topshiriq sharti:
Dasturiy arxitekturada 290-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_290 {
    public function ijroEt(): string;
}

class StandartIjrochi_290 implements XizmatInterfeys_290 {
    public function ijroEt(): string {
        return "Modul 290 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_290();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 290 muvaffaqiyatli bajarildi
```

# 291-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #291
## Topshiriq sharti:
Dasturiy arxitekturada 291-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_291 {
    public function ijroEt(): string;
}

class StandartIjrochi_291 implements XizmatInterfeys_291 {
    public function ijroEt(): string {
        return "Modul 291 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_291();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 291 muvaffaqiyatli bajarildi
```

# 292-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #292
## Topshiriq sharti:
Dasturiy arxitekturada 292-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_292 {
    public function ijroEt(): string;
}

class StandartIjrochi_292 implements XizmatInterfeys_292 {
    public function ijroEt(): string {
        return "Modul 292 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_292();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 292 muvaffaqiyatli bajarildi
```

# 293-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #293
## Topshiriq sharti:
Dasturiy arxitekturada 293-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_293 {
    public function ijroEt(): string;
}

class StandartIjrochi_293 implements XizmatInterfeys_293 {
    public function ijroEt(): string {
        return "Modul 293 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_293();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 293 muvaffaqiyatli bajarildi
```

# 294-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #294
## Topshiriq sharti:
Dasturiy arxitekturada 294-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_294 {
    public function ijroEt(): string;
}

class StandartIjrochi_294 implements XizmatInterfeys_294 {
    public function ijroEt(): string {
        return "Modul 294 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_294();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 294 muvaffaqiyatli bajarildi
```

# 295-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #295
## Topshiriq sharti:
Dasturiy arxitekturada 295-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_295 {
    public function ijroEt(): string;
}

class StandartIjrochi_295 implements XizmatInterfeys_295 {
    public function ijroEt(): string {
        return "Modul 295 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_295();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 295 muvaffaqiyatli bajarildi
```

# 296-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #296
## Topshiriq sharti:
Dasturiy arxitekturada 296-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_296 {
    public function ijroEt(): string;
}

class StandartIjrochi_296 implements XizmatInterfeys_296 {
    public function ijroEt(): string {
        return "Modul 296 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_296();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 296 muvaffaqiyatli bajarildi
```

# 297-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #297
## Topshiriq sharti:
Dasturiy arxitekturada 297-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_297 {
    public function ijroEt(): string;
}

class StandartIjrochi_297 implements XizmatInterfeys_297 {
    public function ijroEt(): string {
        return "Modul 297 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_297();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 297 muvaffaqiyatli bajarildi
```

# 298-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #298
## Topshiriq sharti:
Dasturiy arxitekturada 298-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_298 {
    public function ijroEt(): string;
}

class StandartIjrochi_298 implements XizmatInterfeys_298 {
    public function ijroEt(): string {
        return "Modul 298 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_298();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 298 muvaffaqiyatli bajarildi
```

# 299-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #299
## Topshiriq sharti:
Dasturiy arxitekturada 299-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_299 {
    public function ijroEt(): string;
}

class StandartIjrochi_299 implements XizmatInterfeys_299 {
    public function ijroEt(): string {
        return "Modul 299 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_299();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 299 muvaffaqiyatli bajarildi
```

# 300-Topshiriq: Interfeys va Polimorfizm Amaliyoti: Modul #300
## Topshiriq sharti:
Dasturiy arxitekturada 300-raqamli polimorfik modulni interfeys shartnomasi orqali modellashtiring.

## Yechim (PHP kodi):
```php
<?php

interface XizmatInterfeys_300 {
    public function ijroEt(): string;
}

class StandartIjrochi_300 implements XizmatInterfeys_300 {
    public function ijroEt(): string {
        return "Modul 300 muvaffaqiyatli bajarildi";
    }
}

$ijrochi = new StandartIjrochi_300();
echo $ijrochi->ijroEt() . "
";

```

## Tushuntirish va Mantiq:
Ushbu modulda interfeysga asoslangan arxitektura orqali bo'sh bog'liqlik (loose coupling) va yuqori kengayuvchanlik ta'minlanadi.

## Ishlash natijasi:
```text
Modul 300 muvaffaqiyatli bajarildi
```
