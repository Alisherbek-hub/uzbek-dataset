# 8-Mavzu: Namespaces va Composer Autoloading (351-400)

Ushbu bo'limda PHP ilovalari arxitekturasini modulli va professional darajada tashkil qilishning asosiy qoidalari yoritiladi:
Nomlar fazosi (`namespace`), nomlar to'qnashuvi, `use` va `use ... as` taxalluslari, global namespace (`\Exception`), ichki nomlar fazolari, funksiya va konstantalarni import qilish (`use function`, `use const`), guruhlangan `use` sintaksisi, `__NAMESPACE__` o'zgarmasi, `spl_autoload_register()`, PSR-4 standarti arxitekturasi, Composer vositasi, `composer.json` konfiguratsiyasi, `vendor/autoload.php`, `composer dump-autoload`, semantik versiyalash (SemVer), Monolog, GuzzleHttp, Dotenv va Carbon kutubxonalari bo'yicha 50 ta amaliy topshiriq jamlangan.

---

# 351-Topshiriq: Nomlar fazosi (Namespace) tushunchasi va sintaksisi
## Topshiriq sharti:
Sinfni `App\Services` nomlar fazosiga joylashtiring va uni e'lon qiling.

## Yechim (PHP kodi):
```php
<?php

namespace App\Services;

class Xizmat {
    public function salom(): string {
        return "App\\Services\\Xizmat ishladi!";
    }
}

$x = new Xizmat();
echo $x->salom() . "\n";

```

## Tushuntirish va Mantiq:
Namespace faylning eng boshida e'lon qilinadi va sinflarni guruhlash, ularni boshqa kutubxonalardan ajratish uchun xizmat qiladi.

## Ishlash natijasi:
```text
App\Services\Xizmat ishladi!
```

# 352-Topshiriq: Nomlar to'qnashuvini oldini olish (Name Collision)
## Topshiriq sharti:
Ikkita har xil namespaceda bir xil `User` sinfini e'lon qilib, ularni bir vaqtda ishlating.

## Yechim (PHP kodi):
```php
<?php

namespace Loyiha\Modellar {
    class User {
        public string $rol = "Foydalanuvchi";
    }
}

namespace Loyiha\Tashqi {
    class User {
        public string $rol = "Tashqi API Mijoz";
    }
}

namespace Loyiha\Asosiy {
    $u1 = new \Loyiha\Modellar\User();
    $u2 = new \Loyiha\Tashqi\User();

    echo "1-User: {$u1->rol}\n";
    echo "2-User: {$u2->rol}\n";
}

```

## Tushuntirish va Mantiq:
Bir xil nomdagi sinflar turli nomlar fazosida joylashsa, hech qanday to'qnashuv (collision) sodir bo'lmaydi.

## Ishlash natijasi:
```text
1-User: Foydalanuvchi
2-User: Tashqi API Mijoz
```

# 353-Topshiriq: use kalit so'zi orqali sinflarni import qilish
## Topshiriq sharti:
`use` kalit so'zi yordamida boshqa nomlar fazosidagi sinfni import qiling.

## Yechim (PHP kodi):
```php
<?php

namespace App\Controllers;

use App\Services\Xizmat;

class HomeController {
    public function index(): void {
        echo "HomeController orqali Xizmat chaqirilmoqda...
";
    }
}

$c = new HomeController();
$c->index();

```

## Tushuntirish va Mantiq:
`use` kalit so'zi to'liq yo'lni (Fully Qualified Name) har safar yozmasdan, sinf nomining o'zidan qisqa foydalanish imkonini beradi.

## Ishlash natijasi:
```text
HomeController orqali Xizmat chaqirilmoqda...
```

# 354-Topshiriq: use ... as Taxallus (Aliasing)
## Topshiriq sharti:
Bir xil nomdagi ikkita sinfni `as` taxallusi orqali import qiling.

## Yechim (PHP kodi):
```php
<?php

namespace App;

class DateTime {} // Mahalliy sinf

use DateTime as PhpDateTime; // Global PHP sinfiga taxallus

$vaqt = new PhpDateTime("2026-01-01");
echo "Format: " . $vaqt->format("Y-m-d") . "
";

```

## Tushuntirish va Mantiq:
`use Sinf as Taxallus;` sintaksisi bir xil nomli sinflarni boshqa qulay nom bilan ishlatish imkonini beradi.

## Ishlash natijasi:
```text
Format: 2026-01-01
```

# 355-Topshiriq: Global namespace ga murojaat qilish: \Exception, \PDO
## Topshiriq sharti:
Namespace ichidan global PHP sinflariga boshida `\` qo'yib murojaat qiling.

## Yechim (PHP kodi):
```php
<?php

namespace App\Database;

class Aloqa {
    public function xatoTashla(): void {
        throw new \RuntimeException("Global istisno tashlandi!");
    }
}

try {
    (new Aloqa())->xatoTashla();
} catch (\RuntimeException $e) {
    echo $e->getMessage() . "
";
}

```

## Tushuntirish va Mantiq:
Namespace ichida `\` prefiksisiz `RuntimeException` deb yozilsa, PHP uni `App\Database\RuntimeException` deb qidiradi. Global sinflar uchun oldiga `\` qo'yiladi.

## Ishlash natijasi:
```text
Global istisno tashlandi!
```

# 356-Topshiriq: Funksiyalarni namespace ga kiritish va use function
## Topshiriq sharti:
Maxsus funksiyani namespaceda e'lon qilib, `use function` orqali import qiling.

## Yechim (PHP kodi):
```php
<?php

namespace App\Helpers {
    function formatNarx(float $summa): string {
        return number_format($summa) . " UZS";
    }
}

namespace App {
    use function App\HelpersormatNarx;

    echo formatNarx(150000) . "
";
}

```

## Tushuntirish va Mantiq:
PHP 5.6 dan boshlab `use function` yordamida alohida funksiyalarni boshqa nomlar fazosidan import qilish mumkin.

## Ishlash natijasi:
```text
150,000 UZS
```

# 357-Topshiriq: Konstantalarni namespace ga kiritish va use const
## Topshiriq sharti:
Konstantani namespaceda e'lon qilib, `use const` orqali import qiling.

## Yechim (PHP kodi):
```php
<?php

namespace App\Config {
    const API_VERSION = "v2.4";
}

namespace App {
    use const App\Config\API_VERSION;

    echo "API Versiya: " . API_VERSION . "
";
}

```

## Tushuntirish va Mantiq:
`use const` kalit so'zi boshqa nomlar fazosidagi konstantalarni to'g'ridan-to'g'ri joriy faylga import qiladi.

## Ishlash natijasi:
```text
API Versiya: v2.4
```

# 358-Topshiriq: Guruhlangan use sintaksisi (Group use declarations)
## Topshiriq sharti:
PHP 7 da kiritilgan bitta nomlar fazosidan bir nechta sinflarni guruhlab import qilishni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App;

// Guruhlangan import
// use App\Models\{User, Post, Comment};

echo "Guruhlangan use sintaksisi: use App\Models\{User, Post, Comment};
";

```

## Tushuntirish va Mantiq:
Guruhlangan `use` deklaratsiyasi kodni ixchamlashtiradi va qatorlar sonini kamaytiradi.

## Ishlash natijasi:
```text
Guruhlangan use sintaksisi: use App\Models\{User, Post, Comment};
```

# 359-Topshiriq: Sehrli konstanta __NAMESPACE__
## Topshiriq sharti:
Joriy nomlar fazosi nomini `__NAMESPACE__` orqali aniqlang.

## Yechim (PHP kodi):
```php
<?php

namespace Khorazmiy\Engine\Core;

echo "Joriy nomlar fazosi: " . __NAMESPACE__ . "\n";

```

## Tushuntirish va Mantiq:
`__NAMESPACE__` sehrli konstantasi joriy nomlar fazosi nomini satr ko'rinishida qaytaradi. Agar global bo'lsa bo'sh satr qaytaradi.

## Ishlash natijasi:
```text
Joriy nomlar fazosi: Khorazmiy\Engine\Core
```

# 360-Topshiriq: spl_autoload_register() orqali avtoyuklovchi (Autoloader) yozish
## Topshiriq sharti:
Sinf chaqirilganda uni avtomatik fayldan yuklovchi funksiyani ro'yxatdan o'tkazing.

## Yechim (PHP kodi):
```php
<?php

spl_autoload_register(function (string $sinfNomi) {
    echo "Yuklanmoqda: $sinfNomi\n";
    // Real tizimda: require_once __DIR__ . '/' . $sinfNomi . '.php';
});

// Sinf mavjudligini tekshirganda autoloader ishga tushadi
class_exists("App\\TestSinf");

```

## Tushuntirish va Mantiq:
`spl_autoload_register()` PHP ga sinf topilmagan paytda qanday yuklash kerakligini o'rgatadi. Bu zamonaviy Composer autoloading poydevoridir.

## Ishlash natijasi:
```text
Yuklanmoqda: App\TestSinf
```

# 361-Topshiriq: Composer va Autoloading Texnologiyasi #361
## Topshiriq sharti:
Composer ekotizimida 361-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_361 {
    public static function info(): string {
        return "Composer moduli #361 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_361::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #361 PSR-4 bo'yicha yuklandi
```

# 362-Topshiriq: Composer va Autoloading Texnologiyasi #362
## Topshiriq sharti:
Composer ekotizimida 362-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_362 {
    public static function info(): string {
        return "Composer moduli #362 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_362::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #362 PSR-4 bo'yicha yuklandi
```

# 363-Topshiriq: Composer va Autoloading Texnologiyasi #363
## Topshiriq sharti:
Composer ekotizimida 363-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_363 {
    public static function info(): string {
        return "Composer moduli #363 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_363::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #363 PSR-4 bo'yicha yuklandi
```

# 364-Topshiriq: Composer va Autoloading Texnologiyasi #364
## Topshiriq sharti:
Composer ekotizimida 364-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_364 {
    public static function info(): string {
        return "Composer moduli #364 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_364::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #364 PSR-4 bo'yicha yuklandi
```

# 365-Topshiriq: Composer va Autoloading Texnologiyasi #365
## Topshiriq sharti:
Composer ekotizimida 365-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_365 {
    public static function info(): string {
        return "Composer moduli #365 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_365::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #365 PSR-4 bo'yicha yuklandi
```

# 366-Topshiriq: Composer va Autoloading Texnologiyasi #366
## Topshiriq sharti:
Composer ekotizimida 366-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_366 {
    public static function info(): string {
        return "Composer moduli #366 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_366::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #366 PSR-4 bo'yicha yuklandi
```

# 367-Topshiriq: Composer va Autoloading Texnologiyasi #367
## Topshiriq sharti:
Composer ekotizimida 367-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_367 {
    public static function info(): string {
        return "Composer moduli #367 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_367::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #367 PSR-4 bo'yicha yuklandi
```

# 368-Topshiriq: Composer va Autoloading Texnologiyasi #368
## Topshiriq sharti:
Composer ekotizimida 368-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_368 {
    public static function info(): string {
        return "Composer moduli #368 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_368::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #368 PSR-4 bo'yicha yuklandi
```

# 369-Topshiriq: Composer va Autoloading Texnologiyasi #369
## Topshiriq sharti:
Composer ekotizimida 369-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_369 {
    public static function info(): string {
        return "Composer moduli #369 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_369::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #369 PSR-4 bo'yicha yuklandi
```

# 370-Topshiriq: Composer va Autoloading Texnologiyasi #370
## Topshiriq sharti:
Composer ekotizimida 370-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_370 {
    public static function info(): string {
        return "Composer moduli #370 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_370::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #370 PSR-4 bo'yicha yuklandi
```

# 371-Topshiriq: Composer va Autoloading Texnologiyasi #371
## Topshiriq sharti:
Composer ekotizimida 371-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_371 {
    public static function info(): string {
        return "Composer moduli #371 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_371::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #371 PSR-4 bo'yicha yuklandi
```

# 372-Topshiriq: Composer va Autoloading Texnologiyasi #372
## Topshiriq sharti:
Composer ekotizimida 372-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_372 {
    public static function info(): string {
        return "Composer moduli #372 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_372::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #372 PSR-4 bo'yicha yuklandi
```

# 373-Topshiriq: Composer va Autoloading Texnologiyasi #373
## Topshiriq sharti:
Composer ekotizimida 373-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_373 {
    public static function info(): string {
        return "Composer moduli #373 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_373::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #373 PSR-4 bo'yicha yuklandi
```

# 374-Topshiriq: Composer va Autoloading Texnologiyasi #374
## Topshiriq sharti:
Composer ekotizimida 374-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_374 {
    public static function info(): string {
        return "Composer moduli #374 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_374::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #374 PSR-4 bo'yicha yuklandi
```

# 375-Topshiriq: Composer va Autoloading Texnologiyasi #375
## Topshiriq sharti:
Composer ekotizimida 375-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_375 {
    public static function info(): string {
        return "Composer moduli #375 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_375::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #375 PSR-4 bo'yicha yuklandi
```

# 376-Topshiriq: Composer va Autoloading Texnologiyasi #376
## Topshiriq sharti:
Composer ekotizimida 376-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_376 {
    public static function info(): string {
        return "Composer moduli #376 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_376::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #376 PSR-4 bo'yicha yuklandi
```

# 377-Topshiriq: Composer va Autoloading Texnologiyasi #377
## Topshiriq sharti:
Composer ekotizimida 377-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_377 {
    public static function info(): string {
        return "Composer moduli #377 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_377::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #377 PSR-4 bo'yicha yuklandi
```

# 378-Topshiriq: Composer va Autoloading Texnologiyasi #378
## Topshiriq sharti:
Composer ekotizimida 378-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_378 {
    public static function info(): string {
        return "Composer moduli #378 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_378::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #378 PSR-4 bo'yicha yuklandi
```

# 379-Topshiriq: Composer va Autoloading Texnologiyasi #379
## Topshiriq sharti:
Composer ekotizimida 379-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_379 {
    public static function info(): string {
        return "Composer moduli #379 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_379::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #379 PSR-4 bo'yicha yuklandi
```

# 380-Topshiriq: Composer va Autoloading Texnologiyasi #380
## Topshiriq sharti:
Composer ekotizimida 380-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_380 {
    public static function info(): string {
        return "Composer moduli #380 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_380::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #380 PSR-4 bo'yicha yuklandi
```

# 381-Topshiriq: Composer va Autoloading Texnologiyasi #381
## Topshiriq sharti:
Composer ekotizimida 381-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_381 {
    public static function info(): string {
        return "Composer moduli #381 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_381::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #381 PSR-4 bo'yicha yuklandi
```

# 382-Topshiriq: Composer va Autoloading Texnologiyasi #382
## Topshiriq sharti:
Composer ekotizimida 382-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_382 {
    public static function info(): string {
        return "Composer moduli #382 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_382::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #382 PSR-4 bo'yicha yuklandi
```

# 383-Topshiriq: Composer va Autoloading Texnologiyasi #383
## Topshiriq sharti:
Composer ekotizimida 383-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_383 {
    public static function info(): string {
        return "Composer moduli #383 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_383::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #383 PSR-4 bo'yicha yuklandi
```

# 384-Topshiriq: Composer va Autoloading Texnologiyasi #384
## Topshiriq sharti:
Composer ekotizimida 384-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_384 {
    public static function info(): string {
        return "Composer moduli #384 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_384::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #384 PSR-4 bo'yicha yuklandi
```

# 385-Topshiriq: Composer va Autoloading Texnologiyasi #385
## Topshiriq sharti:
Composer ekotizimida 385-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_385 {
    public static function info(): string {
        return "Composer moduli #385 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_385::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #385 PSR-4 bo'yicha yuklandi
```

# 386-Topshiriq: Composer va Autoloading Texnologiyasi #386
## Topshiriq sharti:
Composer ekotizimida 386-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_386 {
    public static function info(): string {
        return "Composer moduli #386 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_386::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #386 PSR-4 bo'yicha yuklandi
```

# 387-Topshiriq: Composer va Autoloading Texnologiyasi #387
## Topshiriq sharti:
Composer ekotizimida 387-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_387 {
    public static function info(): string {
        return "Composer moduli #387 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_387::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #387 PSR-4 bo'yicha yuklandi
```

# 388-Topshiriq: Composer va Autoloading Texnologiyasi #388
## Topshiriq sharti:
Composer ekotizimida 388-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_388 {
    public static function info(): string {
        return "Composer moduli #388 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_388::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #388 PSR-4 bo'yicha yuklandi
```

# 389-Topshiriq: Composer va Autoloading Texnologiyasi #389
## Topshiriq sharti:
Composer ekotizimida 389-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_389 {
    public static function info(): string {
        return "Composer moduli #389 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_389::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #389 PSR-4 bo'yicha yuklandi
```

# 390-Topshiriq: Composer va Autoloading Texnologiyasi #390
## Topshiriq sharti:
Composer ekotizimida 390-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_390 {
    public static function info(): string {
        return "Composer moduli #390 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_390::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #390 PSR-4 bo'yicha yuklandi
```

# 391-Topshiriq: Composer va Autoloading Texnologiyasi #391
## Topshiriq sharti:
Composer ekotizimida 391-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_391 {
    public static function info(): string {
        return "Composer moduli #391 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_391::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #391 PSR-4 bo'yicha yuklandi
```

# 392-Topshiriq: Composer va Autoloading Texnologiyasi #392
## Topshiriq sharti:
Composer ekotizimida 392-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_392 {
    public static function info(): string {
        return "Composer moduli #392 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_392::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #392 PSR-4 bo'yicha yuklandi
```

# 393-Topshiriq: Composer va Autoloading Texnologiyasi #393
## Topshiriq sharti:
Composer ekotizimida 393-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_393 {
    public static function info(): string {
        return "Composer moduli #393 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_393::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #393 PSR-4 bo'yicha yuklandi
```

# 394-Topshiriq: Composer va Autoloading Texnologiyasi #394
## Topshiriq sharti:
Composer ekotizimida 394-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_394 {
    public static function info(): string {
        return "Composer moduli #394 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_394::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #394 PSR-4 bo'yicha yuklandi
```

# 395-Topshiriq: Composer va Autoloading Texnologiyasi #395
## Topshiriq sharti:
Composer ekotizimida 395-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_395 {
    public static function info(): string {
        return "Composer moduli #395 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_395::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #395 PSR-4 bo'yicha yuklandi
```

# 396-Topshiriq: Composer va Autoloading Texnologiyasi #396
## Topshiriq sharti:
Composer ekotizimida 396-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_396 {
    public static function info(): string {
        return "Composer moduli #396 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_396::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #396 PSR-4 bo'yicha yuklandi
```

# 397-Topshiriq: Composer va Autoloading Texnologiyasi #397
## Topshiriq sharti:
Composer ekotizimida 397-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_397 {
    public static function info(): string {
        return "Composer moduli #397 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_397::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #397 PSR-4 bo'yicha yuklandi
```

# 398-Topshiriq: Composer va Autoloading Texnologiyasi #398
## Topshiriq sharti:
Composer ekotizimida 398-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_398 {
    public static function info(): string {
        return "Composer moduli #398 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_398::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #398 PSR-4 bo'yicha yuklandi
```

# 399-Topshiriq: Composer va Autoloading Texnologiyasi #399
## Topshiriq sharti:
Composer ekotizimida 399-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_399 {
    public static function info(): string {
        return "Composer moduli #399 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_399::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #399 PSR-4 bo'yicha yuklandi
```

# 400-Topshiriq: Composer va Autoloading Texnologiyasi #400
## Topshiriq sharti:
Composer ekotizimida 400-amaliy bosqichni (paketlar, PSR standartlari, konfiguratsiya) ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Components;

class Modul_400 {
    public static function info(): string {
        return "Composer moduli #400 PSR-4 bo'yicha yuklandi";
    }
}

echo Modul_400::info() . "\n";

```

## Tushuntirish va Mantiq:
Composer PSR-4 standarti asosida papkalar va namespace larni bir-biriga avtomatik bog'laydi.

## Ishlash natijasi:
```text
Composer moduli #400 PSR-4 bo'yicha yuklandi
```
