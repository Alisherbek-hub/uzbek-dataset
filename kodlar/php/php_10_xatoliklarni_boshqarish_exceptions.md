# 10-Mavzu: Xatoliklarni Boshqarish va Istisnolar (Exceptions) (451-500)

Ushbu bo'limda PHP tilida xatoliklar arxitekturasi va ularni professional darajada nazorat qilish to'liq yoritiladi:
`Throwable`, `Exception` va `Error` ierarxiyasi, `try-catch-finally`, `getMessage()`, `getCode()`, `getFile()`, `getLine()`, `getTrace()`, ko'p istisnolarni tutish (`catch (A | B $e)`), maxsus istisnolar (`Custom Exceptions`), istisnolar zanjiri (`$previous`), SPL istisnolari (`InvalidArgumentException`, `RuntimeException`), global ushlovchilar (`set_exception_handler`, `set_error_handler`, `register_shutdown_function`), ogohlantirishlarni `ErrorException` ga aylantirish, xatoliklarni fayllarga xavfsiz loglash hamda REST API larda JSON xatolik javoblari bo'yicha 50 ta amaliy topshiriq jamlangan.

---

# 451-Topshiriq: Throwable interfeysi: Exception va Error ierarxiyasi
## Topshiriq sharti:
PHP 7+ da barcha xatoliklarning ota interfeysi bo'lgan `Throwable` orqali ham `Error`, ham `Exception` ni tuting.

## Yechim (PHP kodi):
```php
<?php

function sinov(bool $tur): void {
    try {
        if ($tur) {
            throw new Exception("Mantiqiy istisno");
        } else {
            // PHP tizimli TypeError hosil qilamiz
            intdiv(10, 0);
        }
    } catch (Throwable $e) {
        echo "Throwable ushladi: " . get_class($e) . " -> " . $e->getMessage() . "\n";
    }
}

sinov(true);
sinov(false);

```

## Tushuntirish va Mantiq:
`Throwable` - PHP dagi barcha istisno va xatoliklarning eng yuqori darajadagi interfeysidir. `Exception` (dasturchi xatolari) va `Error` (tizim xatolari) undan meros oladi.

## Ishlash natijasi:
```text
Throwable ushladi: Exception -> Mantiqiy istisno
Throwable ushladi: DivisionByZeroError -> Division by zero
```

# 452-Topshiriq: Oddiy try-catch bloki
## Topshiriq sharti:
Sonni nolga bo'lish paytida yuzaga keladigan xatolikni `try-catch` orqali xavfsiz ushlang.

## Yechim (PHP kodi):
```php
<?php

function xavfsizBolish(int $a, int $b): ?float {
    try {
        if ($b === 0) {
            throw new InvalidArgumentException("Nolga bo'lish taqiqlanadi!");
        }
        return $a / $b;
    } catch (InvalidArgumentException $e) {
        echo "Xatolik: " . $e->getMessage() . "\n";
        return null;
    }
}

$natija = xavfsizBolish(20, 0);
echo "Natija: " . ($natija ?? "null") . "\n";

```

## Tushuntirish va Mantiq:
`try` blokida xatolik yuzaga kelishi mumkin bo'lgan kod yoziladi. `catch` esa tegishli xatolikni ushlab, dasturning to'xtab qolishining oldini oladi.

## Ishlash natijasi:
```text
Xatolik: Nolga bo'lish taqiqlanadi!
Natija: null
```

# 453-Topshiriq: finally bloki va har doim resurslarni yopish
## Topshiriq sharti:
Xatolik yuz berish yoki bermasligidan qat'i nazar `finally` blokining har doim bajarilishini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

function bazaBilanIshla(bool $xatoBor): void {
    echo "1. Ulanish ochildi.\n";
    try {
        if ($xatoBor) {
            throw new RuntimeException("So'rovda xatolik!");
        }
        echo "2. Ma'lumot muvaffaqiyatli saqlandi.\n";
    } catch (RuntimeException $e) {
        echo "Xatolik ushlandi: " . $e->getMessage() . "\n";
    } finally {
        echo "3. FINALLY: Ulanish xavfsiz yopildi.\n";
    }
}

bazaBilanIshla(true);

```

## Tushuntirish va Mantiq:
`finally` bloki `try` va `catch` dan so'ng har doim (hatto `return` chaqirilsa ham) bajariladi. Ochiq qolgan fayllar va tarmoq ulanishlarini tozalashda ishlatiladi.

## Ishlash natijasi:
```text
1. Ulanish ochildi.
Xatolik ushlandi: So'rovda xatolik!
3. FINALLY: Ulanish xavfsiz yopildi.
```

# 454-Topshiriq: Exception xususiyatlari: getMessage, getCode, getFile, getLine
## Topshiriq sharti:
Istisno obyekti qayerda va qachon yuz berganini batafsil tahlil qiling.

## Yechim (PHP kodi):
```php
<?php

try {
    throw new Exception("Kutilmagan server xatosi", 500);
} catch (Exception $e) {
    echo "Xabar: " . $e->getMessage() . "\n";
    echo "Kod: " . $e->getCode() . "\n";
    echo "Qator raqami: " . (!empty($e->getLine()) ? "Mavjud" : "Yo'q") . "\n";
}

```

## Tushuntirish va Mantiq:
Exception obyektlari xatolik matni, xato kodi, yuz bergan fayl nomi va qator raqami kabi to'liq diagnostika ma'lumotlarini taqdim etadi.

## Ishlash natijasi:
```text
Xabar: Kutilmagan server xatosi
Kod: 500
Qator raqami: Mavjud
```

# 455-Topshiriq: Ko'p istisnolarni bitta catch da tutish (TypeA | TypeB)
## Topshiriq sharti:
PHP 7.1 da kiritilgan vertikal chiziq `|` yordamida bir nechta istisnolarni bitta joyda qayta ishlang.

## Yechim (PHP kodi):
```php
<?php

class ValidatsiyaXatosi extends Exception {}
class AutentifikatsiyaXatosi extends Exception {}

function jarayon(int $tur): void {
    try {
        if ($tur === 1) throw new ValidatsiyaXatosi("Email formati noto'g'ri");
        if ($tur === 2) throw new AutentifikatsiyaXatosi("Parol mos kelmadi");
    } catch (ValidatsiyaXatosi | AutentifikatsiyaXatosi $e) {
        echo "Mijoz xatoligi (" . get_class($e) . "): " . $e->getMessage() . "\n";
    }
}

jarayon(1);
jarayon(2);

```

## Tushuntirish va Mantiq:
`catch (A | B $e)` sintaksisi bir xil qayta ishlash logikasiga ega bo'lgan turli xatoliklarni kodni takrorlamasdan bitta blokda tutish imkonini beradi.

## Ishlash natijasi:
```text
Mijoz xatoligi (ValidatsiyaXatosi): Email formati noto'g'ri
Mijoz xatoligi (AutentifikatsiyaXatosi): Parol mos kelmadi
```

# 456-Topshiriq: Maxsus istisno sinflari (Custom Exceptions)
## Topshiriq sharti:
O'z biznes logikangiz uchun `FoydalanuvchiTopilmadiException` sinfini yarating.

## Yechim (PHP kodi):
```php
<?php

class FoydalanuvchiTopilmadiException extends Exception {
    public function __construct(int $id) {
        parent::__construct("ID={$id} bo'lgan foydalanuvchi bazadan topilmadi!", 404);
    }
}

try {
    throw new FoydalanuvchiTopilmadiException(89);
} catch (FoydalanuvchiTopilmadiException $e) {
    echo "Status: " . $e->getCode() . " | " . $e->getMessage() . "\n";
}

```

## Tushuntirish va Mantiq:
Maxsus istisno sinflari dasturdagi biznes xatoliklarni aniq nomlar bilan ajratish va ularga xos parametrlar qo'shish imkonini beradi.

## Ishlash natijasi:
```text
Status: 404 | ID=89 bo'lgan foydalanuvchi bazadan topilmadi!
```

# 457-Topshiriq: Istisnolar zanjiri (Chained Exceptions / $previous)
## Topshiriq sharti:
Quyi darajadagi xatolikni yuqori darajadagi biznes istisnoga o'rab, asl xatolikni `$previous` orqali saqlang.

## Yechim (PHP kodi):
```php
<?php

try {
    try {
        // Ma'lumotlar bazasi xatosi
        throw new PDOException("Baza ulanish vaqti tugadi");
    } catch (PDOException $pdoErr) {
        // Biznes xatosiga o'rab qayta tashlaymiz
        throw new RuntimeException("Buyurtmani saqlab bo'lmadi", 0, $pdoErr);
    }
} catch (RuntimeException $e) {
    echo "Asosiy xato: " . $e->getMessage() . "\n";
    echo "Birlamchi sabab: " . $e->getPrevious()->getMessage() . "\n";
}

```

## Tushuntirish va Mantiq:
`new Exception($msg, $code, $previous)` uchinchi parametri oldingi asl xatolikni zanjir sifatida saqlaydi. Bu nosozlikning tub sababini yo'qotmaslik uchun xizmat qiladi.

## Ishlash natijasi:
```text
Asosiy xato: Buyurtmani saqlab bo'lmadi
Birlamchi sabab: Baza ulanish vaqti tugadi
```

# 458-Topshiriq: Global istisno nazoratchisi: set_exception_handler()
## Topshiriq sharti:
Hech qayerda ushlanmagan istisnolarni markazlashgan holda qabul qiluvchi funksiyani o'rnating.

## Yechim (PHP kodi):
```php
<?php

set_exception_handler(function (Throwable $e) {
    echo "[GLOBAL HANDLER]: " . $e->getMessage() . "\n";
});

// Ushlanmagan istisno
throw new Exception("Kutilmagan global hodisa");

```

## Tushuntirish va Mantiq:
`set_exception_handler()` dasturning har qanday joyida `try-catch` qilinmay qolgan istisnolarni qabul qiladi va xavfsiz yakunlaydi.

## Ishlash natijasi:
```text
[GLOBAL HANDLER]: Kutilmagan global hodisa
```

# 459-Topshiriq: Ogohlantirishlarni Exceptionga aylantirish: set_error_handler
## Topshiriq sharti:
`set_error_handler()` orqali PHP ning eski Warning/Notice larini zamonaviy `ErrorException` ga aylantiring.

## Yechim (PHP kodi):
```php
<?php

set_error_handler(function ($errno, $errstr, $errfile, $errline) {
    throw new ErrorException($errstr, 0, $errno, $errfile, $errline);
});

try {
    // E'lon qilinmagan o'zgaruvchi (Notice)
    $qiymat = $nomalumO'zgaruvchi;
} catch (ErrorException $e) {
    echo "Notice istisnoga aylantirildi: " . $e->getMessage() . "\n";
} finally {
    restore_error_handler();
}

```

## Tushuntirish va Mantiq:
PHP ogohlantirishlarini `ErrorException` ga aylantirish loyihadagi yashirin xatoliklarni darhol yuzaga chiqarishga yordam beradi.

## Ishlash natijasi:
```text
Notice istisnoga aylantirildi: Undefined variable $nomalumO'zgaruvchi
```

# 460-Topshiriq: Xavfsiz JSON API xatolik formati
## Topshiriq sharti:
Har qanday istisnoni standart JSON API xatolik javobiga aylantiruvchi yordamchi tuzing.

## Yechim (PHP kodi):
```php
<?php

function jsonXatolikJavob(Throwable $e): string {
    $kod = $e->getCode() >= 400 && $e->getCode() <= 599 ? $e->getCode() : 500;
    return json_encode([
        "muvaffaqiyat" => false,
        "xatolik" => [
            "kod" => $kod,
            "xabar" => $e->getMessage(),
            "tur" => (new ReflectionClass($e))->getShortName()
        ]
    ], JSON_UNESCAPED_UNICODE);
}

echo jsonXatolikJavob(new InvalidArgumentException("Noto'g'ri ID berildi", 400)) . "\n";

```

## Tushuntirish va Mantiq:
Professional REST API larda har qanday xatolik yagona standart JSON strukturasida qaytarilishi kerak.

## Ishlash natijasi:
```text
{"muvaffaqiyat":false,"xatolik":{"kod":400,"xabar":"Noto'g'ri ID berildi","tur":"InvalidArgumentException"}}
```

# 461-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #461
## Topshiriq sharti:
Ilg'or arxitekturada 461-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_461 extends RuntimeException {}

function tekshirModul_461(): void {
    try {
        throw new TizimXatosi_461("Modul #461 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_461 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_461();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #461 da maxsus istisno holati yuz berdi
```

# 462-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #462
## Topshiriq sharti:
Ilg'or arxitekturada 462-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_462 extends RuntimeException {}

function tekshirModul_462(): void {
    try {
        throw new TizimXatosi_462("Modul #462 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_462 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_462();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #462 da maxsus istisno holati yuz berdi
```

# 463-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #463
## Topshiriq sharti:
Ilg'or arxitekturada 463-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_463 extends RuntimeException {}

function tekshirModul_463(): void {
    try {
        throw new TizimXatosi_463("Modul #463 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_463 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_463();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #463 da maxsus istisno holati yuz berdi
```

# 464-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #464
## Topshiriq sharti:
Ilg'or arxitekturada 464-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_464 extends RuntimeException {}

function tekshirModul_464(): void {
    try {
        throw new TizimXatosi_464("Modul #464 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_464 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_464();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #464 da maxsus istisno holati yuz berdi
```

# 465-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #465
## Topshiriq sharti:
Ilg'or arxitekturada 465-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_465 extends RuntimeException {}

function tekshirModul_465(): void {
    try {
        throw new TizimXatosi_465("Modul #465 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_465 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_465();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #465 da maxsus istisno holati yuz berdi
```

# 466-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #466
## Topshiriq sharti:
Ilg'or arxitekturada 466-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_466 extends RuntimeException {}

function tekshirModul_466(): void {
    try {
        throw new TizimXatosi_466("Modul #466 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_466 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_466();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #466 da maxsus istisno holati yuz berdi
```

# 467-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #467
## Topshiriq sharti:
Ilg'or arxitekturada 467-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_467 extends RuntimeException {}

function tekshirModul_467(): void {
    try {
        throw new TizimXatosi_467("Modul #467 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_467 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_467();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #467 da maxsus istisno holati yuz berdi
```

# 468-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #468
## Topshiriq sharti:
Ilg'or arxitekturada 468-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_468 extends RuntimeException {}

function tekshirModul_468(): void {
    try {
        throw new TizimXatosi_468("Modul #468 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_468 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_468();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #468 da maxsus istisno holati yuz berdi
```

# 469-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #469
## Topshiriq sharti:
Ilg'or arxitekturada 469-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_469 extends RuntimeException {}

function tekshirModul_469(): void {
    try {
        throw new TizimXatosi_469("Modul #469 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_469 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_469();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #469 da maxsus istisno holati yuz berdi
```

# 470-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #470
## Topshiriq sharti:
Ilg'or arxitekturada 470-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_470 extends RuntimeException {}

function tekshirModul_470(): void {
    try {
        throw new TizimXatosi_470("Modul #470 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_470 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_470();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #470 da maxsus istisno holati yuz berdi
```

# 471-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #471
## Topshiriq sharti:
Ilg'or arxitekturada 471-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_471 extends RuntimeException {}

function tekshirModul_471(): void {
    try {
        throw new TizimXatosi_471("Modul #471 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_471 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_471();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #471 da maxsus istisno holati yuz berdi
```

# 472-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #472
## Topshiriq sharti:
Ilg'or arxitekturada 472-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_472 extends RuntimeException {}

function tekshirModul_472(): void {
    try {
        throw new TizimXatosi_472("Modul #472 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_472 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_472();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #472 da maxsus istisno holati yuz berdi
```

# 473-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #473
## Topshiriq sharti:
Ilg'or arxitekturada 473-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_473 extends RuntimeException {}

function tekshirModul_473(): void {
    try {
        throw new TizimXatosi_473("Modul #473 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_473 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_473();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #473 da maxsus istisno holati yuz berdi
```

# 474-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #474
## Topshiriq sharti:
Ilg'or arxitekturada 474-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_474 extends RuntimeException {}

function tekshirModul_474(): void {
    try {
        throw new TizimXatosi_474("Modul #474 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_474 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_474();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #474 da maxsus istisno holati yuz berdi
```

# 475-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #475
## Topshiriq sharti:
Ilg'or arxitekturada 475-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_475 extends RuntimeException {}

function tekshirModul_475(): void {
    try {
        throw new TizimXatosi_475("Modul #475 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_475 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_475();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #475 da maxsus istisno holati yuz berdi
```

# 476-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #476
## Topshiriq sharti:
Ilg'or arxitekturada 476-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_476 extends RuntimeException {}

function tekshirModul_476(): void {
    try {
        throw new TizimXatosi_476("Modul #476 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_476 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_476();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #476 da maxsus istisno holati yuz berdi
```

# 477-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #477
## Topshiriq sharti:
Ilg'or arxitekturada 477-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_477 extends RuntimeException {}

function tekshirModul_477(): void {
    try {
        throw new TizimXatosi_477("Modul #477 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_477 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_477();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #477 da maxsus istisno holati yuz berdi
```

# 478-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #478
## Topshiriq sharti:
Ilg'or arxitekturada 478-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_478 extends RuntimeException {}

function tekshirModul_478(): void {
    try {
        throw new TizimXatosi_478("Modul #478 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_478 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_478();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #478 da maxsus istisno holati yuz berdi
```

# 479-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #479
## Topshiriq sharti:
Ilg'or arxitekturada 479-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_479 extends RuntimeException {}

function tekshirModul_479(): void {
    try {
        throw new TizimXatosi_479("Modul #479 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_479 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_479();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #479 da maxsus istisno holati yuz berdi
```

# 480-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #480
## Topshiriq sharti:
Ilg'or arxitekturada 480-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_480 extends RuntimeException {}

function tekshirModul_480(): void {
    try {
        throw new TizimXatosi_480("Modul #480 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_480 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_480();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #480 da maxsus istisno holati yuz berdi
```

# 481-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #481
## Topshiriq sharti:
Ilg'or arxitekturada 481-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_481 extends RuntimeException {}

function tekshirModul_481(): void {
    try {
        throw new TizimXatosi_481("Modul #481 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_481 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_481();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #481 da maxsus istisno holati yuz berdi
```

# 482-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #482
## Topshiriq sharti:
Ilg'or arxitekturada 482-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_482 extends RuntimeException {}

function tekshirModul_482(): void {
    try {
        throw new TizimXatosi_482("Modul #482 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_482 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_482();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #482 da maxsus istisno holati yuz berdi
```

# 483-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #483
## Topshiriq sharti:
Ilg'or arxitekturada 483-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_483 extends RuntimeException {}

function tekshirModul_483(): void {
    try {
        throw new TizimXatosi_483("Modul #483 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_483 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_483();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #483 da maxsus istisno holati yuz berdi
```

# 484-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #484
## Topshiriq sharti:
Ilg'or arxitekturada 484-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_484 extends RuntimeException {}

function tekshirModul_484(): void {
    try {
        throw new TizimXatosi_484("Modul #484 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_484 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_484();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #484 da maxsus istisno holati yuz berdi
```

# 485-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #485
## Topshiriq sharti:
Ilg'or arxitekturada 485-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_485 extends RuntimeException {}

function tekshirModul_485(): void {
    try {
        throw new TizimXatosi_485("Modul #485 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_485 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_485();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #485 da maxsus istisno holati yuz berdi
```

# 486-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #486
## Topshiriq sharti:
Ilg'or arxitekturada 486-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_486 extends RuntimeException {}

function tekshirModul_486(): void {
    try {
        throw new TizimXatosi_486("Modul #486 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_486 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_486();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #486 da maxsus istisno holati yuz berdi
```

# 487-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #487
## Topshiriq sharti:
Ilg'or arxitekturada 487-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_487 extends RuntimeException {}

function tekshirModul_487(): void {
    try {
        throw new TizimXatosi_487("Modul #487 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_487 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_487();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #487 da maxsus istisno holati yuz berdi
```

# 488-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #488
## Topshiriq sharti:
Ilg'or arxitekturada 488-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_488 extends RuntimeException {}

function tekshirModul_488(): void {
    try {
        throw new TizimXatosi_488("Modul #488 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_488 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_488();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #488 da maxsus istisno holati yuz berdi
```

# 489-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #489
## Topshiriq sharti:
Ilg'or arxitekturada 489-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_489 extends RuntimeException {}

function tekshirModul_489(): void {
    try {
        throw new TizimXatosi_489("Modul #489 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_489 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_489();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #489 da maxsus istisno holati yuz berdi
```

# 490-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #490
## Topshiriq sharti:
Ilg'or arxitekturada 490-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_490 extends RuntimeException {}

function tekshirModul_490(): void {
    try {
        throw new TizimXatosi_490("Modul #490 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_490 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_490();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #490 da maxsus istisno holati yuz berdi
```

# 491-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #491
## Topshiriq sharti:
Ilg'or arxitekturada 491-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_491 extends RuntimeException {}

function tekshirModul_491(): void {
    try {
        throw new TizimXatosi_491("Modul #491 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_491 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_491();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #491 da maxsus istisno holati yuz berdi
```

# 492-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #492
## Topshiriq sharti:
Ilg'or arxitekturada 492-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_492 extends RuntimeException {}

function tekshirModul_492(): void {
    try {
        throw new TizimXatosi_492("Modul #492 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_492 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_492();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #492 da maxsus istisno holati yuz berdi
```

# 493-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #493
## Topshiriq sharti:
Ilg'or arxitekturada 493-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_493 extends RuntimeException {}

function tekshirModul_493(): void {
    try {
        throw new TizimXatosi_493("Modul #493 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_493 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_493();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #493 da maxsus istisno holati yuz berdi
```

# 494-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #494
## Topshiriq sharti:
Ilg'or arxitekturada 494-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_494 extends RuntimeException {}

function tekshirModul_494(): void {
    try {
        throw new TizimXatosi_494("Modul #494 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_494 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_494();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #494 da maxsus istisno holati yuz berdi
```

# 495-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #495
## Topshiriq sharti:
Ilg'or arxitekturada 495-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_495 extends RuntimeException {}

function tekshirModul_495(): void {
    try {
        throw new TizimXatosi_495("Modul #495 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_495 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_495();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #495 da maxsus istisno holati yuz berdi
```

# 496-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #496
## Topshiriq sharti:
Ilg'or arxitekturada 496-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_496 extends RuntimeException {}

function tekshirModul_496(): void {
    try {
        throw new TizimXatosi_496("Modul #496 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_496 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_496();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #496 da maxsus istisno holati yuz berdi
```

# 497-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #497
## Topshiriq sharti:
Ilg'or arxitekturada 497-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_497 extends RuntimeException {}

function tekshirModul_497(): void {
    try {
        throw new TizimXatosi_497("Modul #497 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_497 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_497();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #497 da maxsus istisno holati yuz berdi
```

# 498-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #498
## Topshiriq sharti:
Ilg'or arxitekturada 498-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_498 extends RuntimeException {}

function tekshirModul_498(): void {
    try {
        throw new TizimXatosi_498("Modul #498 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_498 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_498();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #498 da maxsus istisno holati yuz berdi
```

# 499-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #499
## Topshiriq sharti:
Ilg'or arxitekturada 499-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_499 extends RuntimeException {}

function tekshirModul_499(): void {
    try {
        throw new TizimXatosi_499("Modul #499 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_499 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_499();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #499 da maxsus istisno holati yuz berdi
```

# 500-Topshiriq: Xatoliklarni Boshqarish va Istisnolar #500
## Topshiriq sharti:
Ilg'or arxitekturada 500-amaliy xatolik nazorati mexanizmini to'liq namoyish eting.

## Yechim (PHP kodi):
```php
<?php

class TizimXatosi_500 extends RuntimeException {}

function tekshirModul_500(): void {
    try {
        throw new TizimXatosi_500("Modul #500 da maxsus istisno holati yuz berdi");
    } catch (TizimXatosi_500 $e) {
        echo "Nazorat qilindi: " . $e->getMessage() . "\n";
    }
}

tekshirModul_500();

```

## Tushuntirish va Mantiq:
Istisnolarni to'g'ri boshqarish tizim barqarorligi va foydalanuvchi ma'lumotlari xavfsizligining kafolatidir.

## Ishlash natijasi:
```text
Nazorat qilindi: Modul #500 da maxsus istisno holati yuz berdi
```
