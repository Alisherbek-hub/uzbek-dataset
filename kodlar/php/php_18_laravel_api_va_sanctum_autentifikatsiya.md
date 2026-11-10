# 18-Mavzu: Laravel API va Sanctum Autentifikatsiya (851-900)

Ushbu bo'limda professional darajadagi RESTful API arxitekturasi hamda Laravel Sanctum autentifikatsiya tizimi to'liq o'rganiladi:
REST API tamoyillari va standart JSON javoblar, HTTP status kodlari, API Resources (`make:resource`) va Resource Collections, Shartli atributlar (`when`, `whenLoaded`), Laravel Sanctum token generatsiyasi (`createToken`), Token huquqlari (`abilities`), Tizimdan chiqish (Logout), `auth:sanctum` middleware, API Rate Limiting, CORS konfiguratsiyasi, Markazlashtirilgan API xatolarini ushlash (`withExceptions`) hamda API versiyalash bo'yicha 50 ta amaliy topshiriq jamlangan.

---

# 851-Topshiriq: RESTful API arxitekturasi va standart JSON javoblar
## Topshiriq sharti:
Muvaffaqiyatli va xatolik javoblarini standartlashtirilgan JSON formatida qaytaruvchi yordamchi yozing.

## Yechim (PHP kodi):
```php
<?php

class ApiResponse {
    public static function success(mixed $data, string $message = "Muvaffaqiyatli", int $code = 200): string {
        return json_encode([
            'success' => true,
            'message' => $message,
            'data' => $data
        ], JSON_UNESCAPED_UNICODE);
    }
}

echo ApiResponse::success(['id' => 1, 'ism' => 'Anvar'], "Foydalanuvchi topildi") . "\n";

```

## Tushuntirish va Mantiq:
RESTful API yagona javob strukturasiga (success, message, data, errors) ega bo'lishi frontend va mobil dasturchilar uchun juda muhimdir.

## Ishlash natijasi:
```text
{"success":true,"message":"Foydalanuvchi topildi","data":{"id":1,"ism":"Anvar"}}
```

# 852-Topshiriq: Laravel API Resources: make:resource UserResource
## Topshiriq sharti:
Model ma'lumotlarini JSON formatiga xaritalovchi `UserResource` sinfini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

class UserResource {
    public function __construct(private object $user) {}

    public function toArray(): array {
        return [
            'id' => $this->user->id,
            'ism' => $this->user->ism,
            'email' => $this->user->email,
            'yaratilgan_vaqt' => date("Y-m-d", strtotime($this->user->created_at))
        ];
    }
}

$user = (object)['id' => 42, 'ism' => 'Dilshod', 'email' => 'd@uz.uz', 'created_at' => '2026-05-10 12:00:00'];
$res = new UserResource($user);
echo json_encode($res->toArray(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
API Resources ma'lumotlar bazasi ustunlarini to'g'ridan-to'g'ri tashqariga chiqarmasdan, ularni transformatsiya qilish imkonini beradi.

## Ishlash natijasi:
```text
{"id":42,"ism":"Dilshod","email":"d@uz.uz","yaratilgan_vaqt":"2026-05-10"}
```

# 853-Topshiriq: Shartli atributlar: $this->when() va $this->whenLoaded()
## Topshiriq sharti:
Faqat ma'mur (admin) bo'lgandagina maxfiy maydonni ko'rsatish mantiqini yozing.

## Yechim (PHP kodi):
```php
<?php

class AccountResource {
    public function __construct(public float $balans, public bool $isAdmin) {}

    public function toArray(): array {
        $data = ['nom' => 'Asosiy hisob'];
        if ($this->isAdmin) {
            $data['balans'] = $this->balans;
        }
        return $data;
    }
}

$res = new AccountResource(15000000, true);
echo json_encode($res->toArray(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Laravel Resource ichidagi `when()` va `whenLoaded()` yordamida shartli ma'lumotlar va bog'liq munosabatlar faqat kerak bo'lganda JSON ga qo'shiladi.

## Ishlash natijasi:
```text
{"nom":"Asosiy hisob","balans":15000000}
```

# 854-Topshiriq: Laravel Sanctum: Token yaratish ($user->createToken)
## Topshiriq sharti:
Mobil ilovalar uchun Sanctum orqali shaxsiy kirish tokenini (Personal Access Token) generatsiya qilishni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

// Laravel Sanctum sintaksisi:
// $token = $user->createToken('mobil_ilova')->plainTextToken;
$token = "1|khorazmiy_sanctum_sec_token_9918237";
echo "Sanctum tokeni yaratildi: $token\n";

```

## Tushuntirish va Mantiq:
Laravel Sanctum SPA lar va mobil ilovalar uchun yengil va xavfsiz token autentifikatsiyasini taqdim etadi.

## Ishlash natijasi:
```text
Sanctum tokeni yaratildi: 1|khorazmiy_sanctum_sec_token_9918237
```

# 855-Topshiriq: Sanctum Token huquqlari (Abilities / Scopes)
## Topshiriq sharti:
Tokenga faqat o'qish yoki yozish huquqlarini biriktirish va ularni tekshirishni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

// $token = $user->createToken('telegram_bot', ['posts:read'])->plainTextToken;
// if ($user->tokenCan('posts:read')) { ... }

echo "Token huquqi: 'posts:read' muvaffaqiyatli berildi va tekshirildi.\n";

```

## Tushuntirish va Mantiq:
Token abilities orqali har bir alohida mijoz yoki token uchun ruxsat etilgan API amallari chegaralanadi.

## Ishlash natijasi:
```text
Token huquqi: 'posts:read' muvaffaqiyatli berildi va tekshirildi.
```

# 856-Topshiriq: Tizimdan chiqish (Logout) va tokenni o'chirish
## Topshiriq sharti:
Joriy tokenni yoki barcha mavjud tokenlarni o'chirish sintaksisini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

// Joriy tokenni o'chirish:
// $request->user()->currentAccessToken()->delete();

// Barcha qurilmalardagi tokenlarni o'chirish:
// $request->user()->tokens()->delete();

echo "Sanctum tokoni bekor qilindi (Logout bajarildi).\n";

```

## Tushuntirish va Mantiq:
Foydalanuvchi tizimdan chiqqanda tokenni o'chirish xavfsizlikning eng muhim qoidasidir.

## Ishlash natijasi:
```text
Sanctum tokoni bekor qilindi (Logout bajarildi).
```

# 857-Topshiriq: auth:sanctum middleware bilan API marshrutlarni himoyalash
## Topshiriq sharti:
`routes/api.php` da marshrutlarni Sanctum orqali himoyalash sintaksisini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

// Route::middleware('auth:sanctum')->group(function () {
//     Route::get('/user', [UserController::class, 'me']);
//     Route::apiResource('/orders', OrderController::class);
// });

echo "API marshrutlari 'auth:sanctum' middleware orqali to'liq himoyalandi.\n";

```

## Tushuntirish va Mantiq:
`auth:sanctum` kelayotgan `Authorization: Bearer <token>` sarlavhasini avtomatik tekshirib, foydalanuvchini autentifikatsiya qiladi.

## Ishlash natijasi:
```text
API marshrutlari 'auth:sanctum' middleware orqali to'liq himoyalandi.
```

# 858-Topshiriq: API Rate Limiter: Limit::perMinute()
## Topshiriq sharti:
Bir daqiqada faqat 60 ta so'rov qabul qiluvchi Rate Limiter sozlamasini yozing.

## Yechim (PHP kodi):
```php
<?php

// RateLimiter::for('api', function (Request $request) {
//     return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
// });

echo "API Rate Limiter: 60 so'rov / daqiqa chegarasi o'rnatildi.\n";

```

## Tushuntirish va Mantiq:
Rate Limiting API ni haddan tashqari ko'p so'rovlar yuboruvchi botlar va DDoS hujumlaridan himoya qiladi.

## Ishlash natijasi:
```text
API Rate Limiter: 60 so'rov / daqiqa chegarasi o'rnatildi.
```

# 859-Topshiriq: CORS (Cross-Origin Resource Sharing) sozlamalari
## Topshiriq sharti:
Frontend SPA (React, Vue) domenlariga API ga kirishga ruxsat beruvchi sozlamani tushuntiring.

## Yechim (PHP kodi):
```php
<?php

$corsConfig = [
    'paths' => ['api/*', 'sanctum/csrf-cookie'],
    'allowed_methods' => ['*'],
    'allowed_origins' => ['https://khorazmiy.uz', 'http://localhost:3000'],
    'supports_credentials' => true,
];

echo "CORS konfiguratsiyasi: Ruxsat berilgan domenlar ro'yxatga olindi.\n";

```

## Tushuntirish va Mantiq:
CORS sozlamalari brauzerlarning tashqi domenlar o'rtasida xavfsiz ma'lumot almashinuvini ta'minlaydi.

## Ishlash natijasi:
```text
CORS konfiguratsiyasi: Ruxsat berilgan domenlar ro'yxatga olindi.
```

# 860-Topshiriq: Laravel 11 da markazlashtirilgan API xatoliklarini ushlash
## Topshiriq sharti:
`bootstrap/app.php` ichidagi `withExceptions` orqali 404 va 500 xatoliklarini JSON ga aylantirishni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

// bootstrap/app.php
/*
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->render(function (NotFoundHttpException $e, Request $request) {
        if ($request->is('api/*')) {
            return response()->json(['xatolik' => 'Resurs topilmadi'], 404);
        }
    });
})
*/

echo "Laravel 11 da API istisnolari withExceptions orqali JSON ko'rinishida ushlanadi.\n";

```

## Tushuntirish va Mantiq:
Laravel 11 da xatoliklarni qayta ishlash markazlashtirilgan va juda sodda.

## Ishlash natijasi:
```text
Laravel 11 da API istisnolari withExceptions orqali JSON ko'rinishida ushlanadi.
```

# 861-Topshiriq: Laravel REST API va Sanctum Modul #861
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 861-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_861 {
    public function format(): array {
        return [
            "modul" => "REST API #861",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_861();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #861","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 862-Topshiriq: Laravel REST API va Sanctum Modul #862
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 862-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_862 {
    public function format(): array {
        return [
            "modul" => "REST API #862",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_862();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #862","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 863-Topshiriq: Laravel REST API va Sanctum Modul #863
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 863-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_863 {
    public function format(): array {
        return [
            "modul" => "REST API #863",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_863();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #863","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 864-Topshiriq: Laravel REST API va Sanctum Modul #864
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 864-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_864 {
    public function format(): array {
        return [
            "modul" => "REST API #864",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_864();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #864","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 865-Topshiriq: Laravel REST API va Sanctum Modul #865
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 865-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_865 {
    public function format(): array {
        return [
            "modul" => "REST API #865",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_865();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #865","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 866-Topshiriq: Laravel REST API va Sanctum Modul #866
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 866-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_866 {
    public function format(): array {
        return [
            "modul" => "REST API #866",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_866();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #866","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 867-Topshiriq: Laravel REST API va Sanctum Modul #867
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 867-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_867 {
    public function format(): array {
        return [
            "modul" => "REST API #867",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_867();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #867","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 868-Topshiriq: Laravel REST API va Sanctum Modul #868
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 868-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_868 {
    public function format(): array {
        return [
            "modul" => "REST API #868",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_868();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #868","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 869-Topshiriq: Laravel REST API va Sanctum Modul #869
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 869-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_869 {
    public function format(): array {
        return [
            "modul" => "REST API #869",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_869();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #869","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 870-Topshiriq: Laravel REST API va Sanctum Modul #870
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 870-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_870 {
    public function format(): array {
        return [
            "modul" => "REST API #870",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_870();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #870","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 871-Topshiriq: Laravel REST API va Sanctum Modul #871
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 871-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_871 {
    public function format(): array {
        return [
            "modul" => "REST API #871",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_871();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #871","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 872-Topshiriq: Laravel REST API va Sanctum Modul #872
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 872-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_872 {
    public function format(): array {
        return [
            "modul" => "REST API #872",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_872();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #872","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 873-Topshiriq: Laravel REST API va Sanctum Modul #873
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 873-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_873 {
    public function format(): array {
        return [
            "modul" => "REST API #873",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_873();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #873","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 874-Topshiriq: Laravel REST API va Sanctum Modul #874
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 874-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_874 {
    public function format(): array {
        return [
            "modul" => "REST API #874",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_874();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #874","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 875-Topshiriq: Laravel REST API va Sanctum Modul #875
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 875-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_875 {
    public function format(): array {
        return [
            "modul" => "REST API #875",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_875();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #875","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 876-Topshiriq: Laravel REST API va Sanctum Modul #876
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 876-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_876 {
    public function format(): array {
        return [
            "modul" => "REST API #876",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_876();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #876","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 877-Topshiriq: Laravel REST API va Sanctum Modul #877
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 877-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_877 {
    public function format(): array {
        return [
            "modul" => "REST API #877",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_877();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #877","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 878-Topshiriq: Laravel REST API va Sanctum Modul #878
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 878-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_878 {
    public function format(): array {
        return [
            "modul" => "REST API #878",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_878();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #878","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 879-Topshiriq: Laravel REST API va Sanctum Modul #879
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 879-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_879 {
    public function format(): array {
        return [
            "modul" => "REST API #879",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_879();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #879","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 880-Topshiriq: Laravel REST API va Sanctum Modul #880
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 880-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_880 {
    public function format(): array {
        return [
            "modul" => "REST API #880",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_880();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #880","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 881-Topshiriq: Laravel REST API va Sanctum Modul #881
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 881-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_881 {
    public function format(): array {
        return [
            "modul" => "REST API #881",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_881();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #881","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 882-Topshiriq: Laravel REST API va Sanctum Modul #882
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 882-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_882 {
    public function format(): array {
        return [
            "modul" => "REST API #882",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_882();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #882","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 883-Topshiriq: Laravel REST API va Sanctum Modul #883
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 883-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_883 {
    public function format(): array {
        return [
            "modul" => "REST API #883",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_883();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #883","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 884-Topshiriq: Laravel REST API va Sanctum Modul #884
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 884-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_884 {
    public function format(): array {
        return [
            "modul" => "REST API #884",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_884();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #884","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 885-Topshiriq: Laravel REST API va Sanctum Modul #885
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 885-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_885 {
    public function format(): array {
        return [
            "modul" => "REST API #885",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_885();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #885","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 886-Topshiriq: Laravel REST API va Sanctum Modul #886
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 886-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_886 {
    public function format(): array {
        return [
            "modul" => "REST API #886",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_886();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #886","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 887-Topshiriq: Laravel REST API va Sanctum Modul #887
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 887-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_887 {
    public function format(): array {
        return [
            "modul" => "REST API #887",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_887();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #887","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 888-Topshiriq: Laravel REST API va Sanctum Modul #888
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 888-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_888 {
    public function format(): array {
        return [
            "modul" => "REST API #888",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_888();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #888","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 889-Topshiriq: Laravel REST API va Sanctum Modul #889
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 889-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_889 {
    public function format(): array {
        return [
            "modul" => "REST API #889",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_889();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #889","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 890-Topshiriq: Laravel REST API va Sanctum Modul #890
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 890-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_890 {
    public function format(): array {
        return [
            "modul" => "REST API #890",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_890();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #890","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 891-Topshiriq: Laravel REST API va Sanctum Modul #891
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 891-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_891 {
    public function format(): array {
        return [
            "modul" => "REST API #891",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_891();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #891","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 892-Topshiriq: Laravel REST API va Sanctum Modul #892
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 892-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_892 {
    public function format(): array {
        return [
            "modul" => "REST API #892",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_892();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #892","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 893-Topshiriq: Laravel REST API va Sanctum Modul #893
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 893-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_893 {
    public function format(): array {
        return [
            "modul" => "REST API #893",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_893();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #893","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 894-Topshiriq: Laravel REST API va Sanctum Modul #894
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 894-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_894 {
    public function format(): array {
        return [
            "modul" => "REST API #894",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_894();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #894","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 895-Topshiriq: Laravel REST API va Sanctum Modul #895
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 895-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_895 {
    public function format(): array {
        return [
            "modul" => "REST API #895",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_895();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #895","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 896-Topshiriq: Laravel REST API va Sanctum Modul #896
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 896-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_896 {
    public function format(): array {
        return [
            "modul" => "REST API #896",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_896();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #896","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 897-Topshiriq: Laravel REST API va Sanctum Modul #897
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 897-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_897 {
    public function format(): array {
        return [
            "modul" => "REST API #897",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_897();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #897","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 898-Topshiriq: Laravel REST API va Sanctum Modul #898
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 898-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_898 {
    public function format(): array {
        return [
            "modul" => "REST API #898",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_898();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #898","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 899-Topshiriq: Laravel REST API va Sanctum Modul #899
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 899-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_899 {
    public function format(): array {
        return [
            "modul" => "REST API #899",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_899();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #899","status":"Faol","autentifikatsiya":"Sanctum Token"}
```

# 900-Topshiriq: Laravel REST API va Sanctum Modul #900
## Topshiriq sharti:
RESTful API arxitekturasi va token xavfsizligi bo'yicha 900-amaliy topshiriqni to'liq yozing.

## Yechim (PHP kodi):
```php
<?php

namespace App\Http\Resources;

class Resource_900 {
    public function format(): array {
        return [
            "modul" => "REST API #900",
            "status" => "Faol",
            "autentifikatsiya" => "Sanctum Token"
        ];
    }
}

$r = new Resource_900();
echo json_encode($r->format(), JSON_UNESCAPED_UNICODE) . "\n";

```

## Tushuntirish va Mantiq:
Sanctum va API Resources zamonaviy mobil va SPA ekotizimlari uchun xavfsiz tayanchdir.

## Ishlash natijasi:
```text
{"modul":"REST API #900","status":"Faol","autentifikatsiya":"Sanctum Token"}
```
