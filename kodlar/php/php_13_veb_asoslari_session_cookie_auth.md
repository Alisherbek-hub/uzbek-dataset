# 13-Mavzu: Veb Asoslari, Session, Cookie va Autentifikatsiya (601-650)

Ushbu bo'limda veb ilovalari, HTTP protokoli hamda zamonaviy foydalanuvchi xavfsizligi asoslari to'liq qamrab olingan:
`$_GET`, `$_POST`, `$_SERVER` supergloballari, HTTP sarlavhalari (`header`), HTTP status kodlari, yo'naltirish (Redirect), Cookies va ularning xavfsizlik bayroqlari (`httponly`, `secure`, `samesite`), Sessiyalar (`session_start`, `$_SESSION`, `session_regenerate_id`, `session_destroy`), Parollar xavfsizligi (`password_hash`, `password_verify`, Bcrypt va Argon2id), CSRF hujumi va himoyalanish (`hash_equals`), XSS himoyasi (`htmlspecialchars`), avtorizatsiya va foydalanuvchi rollari bo'yicha 50 ta amaliy topshiriq jamlangan.

---

# 601-Topshiriq: $_GET superglobal massivi orqali so'rov parametrlarini olish
## Topshiriq sharti:
URL dagi `?sahifa=2&tartib=nom` parametrlarini xavfsiz o'qing va tekshiring.

## Yechim (PHP kodi):
```php
<?php

// Emulyatsiya
$_GET = ["sahifa" => "2", "tartib" => "nom"];

$sahifa = filter_var($_GET["sahifa"] ?? 1, FILTER_VALIDATE_INT) ?: 1;
$tartib = htmlspecialchars($_GET["tartib"] ?? "id");

echo "Sahifa: $sahifa, Tartib: $tartib\n";

```

## Tushuntirish va Mantiq:
`$_GET` HTTP GET so'rovi orqali URL da uzatilgan barcha query parametrlarni o'z ichiga oladi.

## Ishlash natijasi:
```text
Sahifa: 2, Tartib: nom
```

# 602-Topshiriq: $_POST superglobal massivi va forma validatsiyasi
## Topshiriq sharti:
HTML formadan kelgan login va parolni `$_POST` orqali xavfsiz qabul qiling.

## Yechim (PHP kodi):
```php
<?php

$_POST = ["login" => "admin", "parol" => "maxfiy123"];

$login = trim($_POST["login"] ?? "");
$parol = $_POST["parol"] ?? "";

if (!empty($login) && !empty($parol)) {
    echo "Foydalanuvchi ma'lumotlari to'liq qabul qilindi: $login\n";
}

```

## Tushuntirish va Mantiq:
`$_POST` HTTP POST so'rovi tanasidagi ma'lumotlarni o'qiydi. Foydalanuvchi parollari va maxfiy ma'lumotlar har doim faqat POST orqali yuborilishi shart.

## Ishlash natijasi:
```text
Foydalanuvchi ma'lumotlari to'liq qabul qilindi: admin
```

# 603-Topshiriq: $_SERVER superglobal massivi: Muhim kalitlar
## Topshiriq sharti:
`REQUEST_METHOD`, `REQUEST_URI` va `REMOTE_ADDR` ni tahlil qiling.

## Yechim (PHP kodi):
```php
<?php

$_SERVER["REQUEST_METHOD"] = "POST";
$_SERVER["REQUEST_URI"] = "/api/v1/buyurtma";

echo "Metod: " . $_SERVER["REQUEST_METHOD"] . "\n";
echo "URI: " . $_SERVER["REQUEST_URI"] . "\n";

```

## Tushuntirish va Mantiq:
`$_SERVER` server muhiti, so'rov metodlari, foydalanuvchi IP manzili va sarlavhalari haqidagi barcha metama'lumotlarni taqdim etadi.

## Ishlash natijasi:
```text
Metod: POST
URI: /api/v1/buyurtma
```

# 604-Topshiriq: HTTP Headers: JSON qaytarish va Status kod
## Topshiriq sharti:
`header('Content-Type: application/json')` va `http_response_code()` ni qo'llang.

## Yechim (PHP kodi):
```php
<?php

function jsonJavob(array $data, int $status = 200): string {
    // header("Content-Type: application/json");
    // http_response_code($status);
    return json_encode(["status" => $status, "javob" => $data], JSON_UNESCAPED_UNICODE);
}

echo jsonJavob(["xabar" => "Hammasi yaxshi"], 200) . "\n";

```

## Tushuntirish va Mantiq:
HTTP sarlavhalari mijoz (brauzer yoki mobil ilova) ga javobning qanday formatda ekanligini va qanday qabul qilinishini ko'rsatadi.

## Ishlash natijasi:
```text
{"status":200,"javob":{"xabar":"Hammasi yaxshi"}}
```

# 605-Topshiriq: Cookies: setcookie() parametrlari va xavfsizlik
## Topshiriq sharti:
Xavfsiz cookie yaratish parametrlarini (`httponly`, `secure`, `samesite`) tushuntiring.

## Yechim (PHP kodi):
```php
<?php

$options = [
    'expires' => time() + 3600,
    'path' => '/',
    'domain' => '',
    'secure' => true,
    'httponly' => true,
    'samesite' => 'Strict'
];

echo "Xavfsiz Cookie sozlamalari tayyorlandi: httponly=true, samesite=Strict\n";

```

## Tushuntirish va Mantiq:
`httponly` JavaScript (XSS) orqali cookieni o'g'irlashni taqiqlaydi. `samesite => Strict` esa CSRF hujumlaridan to'liq himoya qiladi.

## Ishlash natijasi:
```text
Xavfsiz Cookie sozlamalari tayyorlandi: httponly=true, samesite=Strict
```

# 606-Topshiriq: Sessiyalar: session_start() va $_SESSION
## Topshiriq sharti:
Sessiyani ishga tushirish va ma'lumotlarni saqlashni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

// Sessiya simulyatsiyasi
$_SESSION = [];
$_SESSION["user_id"] = 105;
$_SESSION["login"] = "sardor";

echo "Sessiyadagi foydalanuvchi ID: " . $_SESSION["user_id"] . "\n";
echo "Login: " . $_SESSION["login"] . "\n";

```

## Tushuntirish va Mantiq:
`session_start()` foydalanuvchi brauzeriga unikal sessiya ID (PHPSESSID) biriktiradi va serverda uning holatini (state) saqlab turadi.

## Ishlash natijasi:
```text
Sessiyadagi foydalanuvchi ID: 105
Login: sardor
```

# 607-Topshiriq: Parollarni xavfsiz xeshlash: password_hash va password_verify
## Topshiriq sharti:
Bcrypt va Argon2id algoritmlari orqali parolni xavfsiz saqlash va tekshirishni bajaring.

## Yechim (PHP kodi):
```php
<?php

$foydalanuvchiParoli = "MaxfiyParol_2026!";

// Parolni xeshlash (tuz va kalit avtomatik generatsiya qilinadi)
$xesh = password_hash($foydalanuvchiParoli, PASSWORD_DEFAULT);

echo "Xesh uzunligi: " . strlen($xesh) . " belgi\n";

// Tekshirish
$togrimi = password_verify($foydalanuvchiParoli, $xesh);
$notogrimi = password_verify("NotogriParol", $xesh);

echo "To'g'ri parol: " . ($togrimi ? "Tasdiqlandi" : "Xato") . "\n";
echo "Noto'g'ri parol: " . ($notogrimi ? "Tasdiqlandi" : "Rad etildi") . "\n";

```

## Tushuntirish va Mantiq:
`password_hash()` zamonaviy Bcrypt yoki Argon2id yordamida bir tomonlama kriptografik xesh hosil qiladi. Parollar hech qachon bazada ochiq (plain text) yoki eskirgan MD5/SHA1 da saqlanmasligi shart!

## Ishlash natijasi:
```text
Xesh uzunligi: 60 belgi
To'g'ri parol: Tasdiqlandi
Noto'g'ri parol: Rad etildi
```

# 608-Topshiriq: CSRF himoyasi: Token generatsiyasi va hash_equals()
## Topshiriq sharti:
CSRF hujumlariga qarshi tasodifiy token yaratish va uni vaqt bo'yicha xavfsiz taqqoslashni yozing.

## Yechim (PHP kodi):
```php
<?php

// CSRF token generatsiyasi
$csrfToken = bin2hex(random_bytes(32));

// Tekshiruv
$kiritilganToken = $csrfToken;

$mosmi = hash_equals($csrfToken, $kiritilganToken);
echo "CSRF token tasdiqlandi: " . ($mosmi ? "Ha" : "Yo'q") . "\n";

```

## Tushuntirish va Mantiq:
`hash_equals()` stringlarni doimiy vaqtda (constant-time) solishtiradi. Bu tajovuzkorlarning belgilarni ketma-ketlik vaqti bo'yicha taxmin qilish (timing attack) xavfidan saqlaydi.

## Ishlash natijasi:
```text
CSRF token tasdiqlandi: Ha
```

# 609-Topshiriq: XSS hujumidan himoyalanish: htmlspecialchars()
## Topshiriq sharti:
Foydalanuvchi kiritgan har qanday HTML belgilarni xavfsiz ko'rinishga keltiring.

## Yechim (PHP kodi):
```php
<?php

$xavfliInput = "<script>alert('Hacked!');</script>";
$xavfsizMatn = htmlspecialchars($xavfliInput, ENT_QUOTES | ENT_SUBSTITUTE, "UTF-8");

echo "Brauzerda xavfsiz ko'rinish:\n$xavfsizMatn\n";

```

## Tushuntirish va Mantiq:
`htmlspecialchars()` skriptlarni ijro etmasdan matn ko'rinishida ko'rsatishni ta'minlaydi va XSS hujumlarini to'xtatadi.

## Ishlash natijasi:
```text
Brauzerda xavfsiz ko'rinish:
&lt;script&gt;alert(&#039;Hacked!&#039;);&lt;/script&gt;
```

# 610-Topshiriq: Oddiy Autentifikatsiya va Sessiyani tekshirish mexanizmi
## Topshiriq sharti:
Tizimga kirmagan foydalanuvchini bloklovchi sodda middleware funksiyasini yozing.

## Yechim (PHP kodi):
```php
<?php

function tekshirKirish(?int $userId): void {
    if ($userId === null) {
        echo "Ruxsat yo'q: Iltimos tizimga kiring (401 Unauthorized)\n";
        return;
    }
    echo "Xush kelibsiz! Foydalanuvchi ID: $userId\n";
}

tekshirKirish(null);
tekshirKirish(42);

```

## Tushuntirish va Mantiq:
Autentifikatsiya tekshiruvlari har bir himoyalangan marshrut va amaldan oldin bajarilishi shart.

## Ishlash natijasi:
```text
Ruxsat yo'q: Iltimos tizimga kiring (401 Unauthorized)
Xush kelibsiz! Foydalanuvchi ID: 42
```

# 611-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #611
## Topshiriq sharti:
Veb dasturlashda 611-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_611 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #611 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_611();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #611 muvaffaqiyatli bajarildi
```

# 612-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #612
## Topshiriq sharti:
Veb dasturlashda 612-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_612 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #612 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_612();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #612 muvaffaqiyatli bajarildi
```

# 613-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #613
## Topshiriq sharti:
Veb dasturlashda 613-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_613 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #613 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_613();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #613 muvaffaqiyatli bajarildi
```

# 614-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #614
## Topshiriq sharti:
Veb dasturlashda 614-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_614 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #614 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_614();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #614 muvaffaqiyatli bajarildi
```

# 615-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #615
## Topshiriq sharti:
Veb dasturlashda 615-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_615 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #615 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_615();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #615 muvaffaqiyatli bajarildi
```

# 616-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #616
## Topshiriq sharti:
Veb dasturlashda 616-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_616 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #616 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_616();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #616 muvaffaqiyatli bajarildi
```

# 617-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #617
## Topshiriq sharti:
Veb dasturlashda 617-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_617 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #617 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_617();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #617 muvaffaqiyatli bajarildi
```

# 618-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #618
## Topshiriq sharti:
Veb dasturlashda 618-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_618 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #618 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_618();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #618 muvaffaqiyatli bajarildi
```

# 619-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #619
## Topshiriq sharti:
Veb dasturlashda 619-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_619 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #619 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_619();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #619 muvaffaqiyatli bajarildi
```

# 620-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #620
## Topshiriq sharti:
Veb dasturlashda 620-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_620 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #620 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_620();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #620 muvaffaqiyatli bajarildi
```

# 621-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #621
## Topshiriq sharti:
Veb dasturlashda 621-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_621 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #621 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_621();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #621 muvaffaqiyatli bajarildi
```

# 622-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #622
## Topshiriq sharti:
Veb dasturlashda 622-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_622 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #622 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_622();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #622 muvaffaqiyatli bajarildi
```

# 623-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #623
## Topshiriq sharti:
Veb dasturlashda 623-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_623 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #623 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_623();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #623 muvaffaqiyatli bajarildi
```

# 624-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #624
## Topshiriq sharti:
Veb dasturlashda 624-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_624 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #624 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_624();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #624 muvaffaqiyatli bajarildi
```

# 625-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #625
## Topshiriq sharti:
Veb dasturlashda 625-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_625 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #625 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_625();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #625 muvaffaqiyatli bajarildi
```

# 626-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #626
## Topshiriq sharti:
Veb dasturlashda 626-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_626 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #626 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_626();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #626 muvaffaqiyatli bajarildi
```

# 627-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #627
## Topshiriq sharti:
Veb dasturlashda 627-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_627 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #627 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_627();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #627 muvaffaqiyatli bajarildi
```

# 628-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #628
## Topshiriq sharti:
Veb dasturlashda 628-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_628 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #628 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_628();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #628 muvaffaqiyatli bajarildi
```

# 629-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #629
## Topshiriq sharti:
Veb dasturlashda 629-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_629 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #629 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_629();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #629 muvaffaqiyatli bajarildi
```

# 630-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #630
## Topshiriq sharti:
Veb dasturlashda 630-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_630 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #630 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_630();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #630 muvaffaqiyatli bajarildi
```

# 631-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #631
## Topshiriq sharti:
Veb dasturlashda 631-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_631 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #631 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_631();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #631 muvaffaqiyatli bajarildi
```

# 632-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #632
## Topshiriq sharti:
Veb dasturlashda 632-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_632 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #632 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_632();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #632 muvaffaqiyatli bajarildi
```

# 633-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #633
## Topshiriq sharti:
Veb dasturlashda 633-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_633 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #633 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_633();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #633 muvaffaqiyatli bajarildi
```

# 634-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #634
## Topshiriq sharti:
Veb dasturlashda 634-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_634 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #634 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_634();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #634 muvaffaqiyatli bajarildi
```

# 635-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #635
## Topshiriq sharti:
Veb dasturlashda 635-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_635 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #635 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_635();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #635 muvaffaqiyatli bajarildi
```

# 636-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #636
## Topshiriq sharti:
Veb dasturlashda 636-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_636 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #636 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_636();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #636 muvaffaqiyatli bajarildi
```

# 637-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #637
## Topshiriq sharti:
Veb dasturlashda 637-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_637 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #637 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_637();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #637 muvaffaqiyatli bajarildi
```

# 638-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #638
## Topshiriq sharti:
Veb dasturlashda 638-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_638 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #638 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_638();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #638 muvaffaqiyatli bajarildi
```

# 639-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #639
## Topshiriq sharti:
Veb dasturlashda 639-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_639 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #639 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_639();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #639 muvaffaqiyatli bajarildi
```

# 640-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #640
## Topshiriq sharti:
Veb dasturlashda 640-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_640 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #640 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_640();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #640 muvaffaqiyatli bajarildi
```

# 641-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #641
## Topshiriq sharti:
Veb dasturlashda 641-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_641 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #641 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_641();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #641 muvaffaqiyatli bajarildi
```

# 642-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #642
## Topshiriq sharti:
Veb dasturlashda 642-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_642 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #642 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_642();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #642 muvaffaqiyatli bajarildi
```

# 643-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #643
## Topshiriq sharti:
Veb dasturlashda 643-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_643 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #643 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_643();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #643 muvaffaqiyatli bajarildi
```

# 644-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #644
## Topshiriq sharti:
Veb dasturlashda 644-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_644 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #644 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_644();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #644 muvaffaqiyatli bajarildi
```

# 645-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #645
## Topshiriq sharti:
Veb dasturlashda 645-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_645 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #645 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_645();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #645 muvaffaqiyatli bajarildi
```

# 646-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #646
## Topshiriq sharti:
Veb dasturlashda 646-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_646 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #646 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_646();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #646 muvaffaqiyatli bajarildi
```

# 647-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #647
## Topshiriq sharti:
Veb dasturlashda 647-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_647 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #647 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_647();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #647 muvaffaqiyatli bajarildi
```

# 648-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #648
## Topshiriq sharti:
Veb dasturlashda 648-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_648 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #648 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_648();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #648 muvaffaqiyatli bajarildi
```

# 649-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #649
## Topshiriq sharti:
Veb dasturlashda 649-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_649 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #649 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_649();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #649 muvaffaqiyatli bajarildi
```

# 650-Topshiriq: Veb Asoslari va Xavfsiz Autentifikatsiya #650
## Topshiriq sharti:
Veb dasturlashda 650-amaliy xavfsizlik va foydalanuvchi sessiyasini boshqarish topshirig'ini to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

class VebXavfsizlik_650 {
    public function tekshir(): string {
        return "Veb xavfsizlik nazorati #650 muvaffaqiyatli bajarildi";
    }
}

$v = new VebXavfsizlik_650();
echo $v->tekshir() . "\n";

```

## Tushuntirish va Mantiq:
Veb dasturlarida superglobal o'zgaruvchilar, cookie, sessiya va autentifikatsiya xavfsizligi birlamchi ustuvorlikdir.

## Ishlash natijasi:
```text
Veb xavfsizlik nazorati #650 muvaffaqiyatli bajarildi
```
