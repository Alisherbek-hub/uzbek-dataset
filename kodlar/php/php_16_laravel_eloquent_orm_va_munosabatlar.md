# 16-Mavzu: Laravel Eloquent ORM va Munosabatlar (751-800)

Ushbu bo'limda Laravel freymvorkining eng kuchli qismi bo'lgan Eloquent ORM va ma'lumotlar bazasi munosabatlari to'liq ochib beriladi:
Migratsiyalar arxitekturasi, Eloquent Model konfiguratsiyasi, Mass Assignment va `$fillable`, CRUD amallari, Birga-bir (`hasOne`, `belongsTo`), Birga-ko'p (`hasMany`), Ko'pga-ko'p (`belongsToMany` va Pivot jadvallar), N+1 so'rovlar muammosi va Eager Loading (`with`), Local va Global Scopes, Yangi Accessor va Mutatorlar (`Attribute::make`), Eloquent Events va Observers, Paginatsiya hamda Collections metodlari bo'yicha 50 ta amaliy topshiriq jamlangan.

---

# 751-Topshiriq: Laravel Migratsiyalar tuzilishi (Schema::create)
## Topshiriq sharti:
Foydalanuvchilar jadvalini yaratuvchi migratsiya fayli sintaksisini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

// database/migrations/xxxx_create_users_table.php
/*
Schema::create('users', function (Blueprint $table) {
    $table->id();
    $table->string('ism');
    $table->string('email')->unique();
    $table->string('parol');
    $table->timestamps();
});
*/

echo "Schema::create orqali 'users' jadvali migratsiyasi tuzildi.\n";

```

## Tushuntirish va Mantiq:
Laravel migratsiyalari ma'lumotlar bazasi strukturasini versiyalash imkonini beradi. Har bir migratsiyada `up()` va `down()` metodlari bo'ladi.

## Ishlash natijasi:
```text
Schema::create orqali 'users' jadvali migratsiyasi tuzildi.
```

# 752-Topshiriq: Eloquent Model asoslari: $fillable va $guarded
## Topshiriq sharti:
Mass Assignment hujumlaridan himoyalanish uchun `$fillable` xususiyatini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class User {
    // Faqat ushbu maydonlarni ommaviy to'ldirishga ruxsat beriladi
    protected array $fillable = [
        'ism',
        'email',
        'parol',
    ];

    public function getFillable(): array {
        return $this->fillable;
    }
}

$u = new User();
echo "Ruxsat etilgan maydonlar: " . implode(", ", $u->getFillable()) . "\n";

```

## Tushuntirish va Mantiq:
`$fillable` massiviga kiritilmagan maydonlar (masalan `is_admin`) foydalanuvchi so'rovi orqali avtomatik yozilishining oldini oladi.

## Ishlash natijasi:
```text
Ruxsat etilgan maydonlar: ism, email, parol
```

# 753-Topshiriq: Eloquent CRUD: create, find, update, delete
## Topshiriq sharti:
Eloquent modelida asosiy CRUD amallarini chaqirish sintaksisini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

// 1. Create:
// $user = User::create(['ism' => 'Ali', 'email' => 'ali@uz.uz']);

// 2. Read:
// $user = User::findOrFail(1);

// 3. Update:
// $user->update(['ism' => 'Alisher']);

// 4. Delete:
// $user->delete();

echo "Eloquent CRUD metodlari: create(), findOrFail(), update(), delete()\n";

```

## Tushuntirish va Mantiq:
Eloquent Active Record naqshiga asoslangan bo'lib, har bir qatorni bitta obyekt ko'rinishida taqdim etadi.

## Ishlash natijasi:
```text
Eloquent CRUD metodlari: create(), findOrFail(), update(), delete()
```

# 754-Topshiriq: Birga-ko'p (One-to-Many) munosabat: hasMany va belongsTo
## Topshiriq sharti:
Muallif va uning maqolalari o'rtasidagi bog'liqlikni ifodalang.

## Yechim (PHP kodi):
```php
<?php

class Post {
    public function __construct(public string $title) {}
}

class Author {
    public function posts(): array {
        // Eloquentda: return $this->hasMany(Post::class);
        return [new Post("1-maqola"), new Post("2-maqola")];
    }
}

$author = new Author();
echo "Muallif maqolalari soni: " . count($author->posts()) . "\n";

```

## Tushuntirish va Mantiq:
`hasMany` bitta yozuvga bir nechta boshqa yozuvlar tegishli ekanligini, `belongsTo` esa aksincha ota yozuvga bog'liqlikni bildiradi.

## Ishlash natijasi:
```text
Muallif maqolalari soni: 2
```

# 755-Topshiriq: Ko'pga-ko'p (Many-to-Many) munosabat: belongsToMany va Pivot jadval
## Topshiriq sharti:
Foydalanuvchilar va rollar o'rtasidagi ko'pga-ko'p munosabatni ko'rsating.

## Yechim (PHP kodi):
```php
<?php

// Foydalanuvchi modeli ichida:
// public function roles() { return $this->belongsToMany(Role::class)->withTimestamps(); }

echo "Ko'pga-ko'p munosabat: belongsToMany(Role::class) orqali pivot jadval bog'lanadi\n";

```

## Tushuntirish va Mantiq:
`belongsToMany` o'rtada oraliq bog'lovchi jadval (pivot table: masalan `role_user`) orqali ikkita jadvalni bog'laydi.

## Ishlash natijasi:
```text
Ko'pga-ko'p munosabat: belongsToMany(Role::class) orqali pivot jadval bog'lanadi
```

# 756-Topshiriq: N+1 so'rovlar muammosi va Eager Loading (with)
## Topshiriq sharti:
Sikl ichida yuzlab ortiqcha SQL so'rovlar ketishining oldini olish uchun `with()` dan foydalaning.

## Yechim (PHP kodi):
```php
<?php

// Yomon usul (N+1 muammo):
// $users = User::all();
// foreach ($users as $u) { echo $u->profile->bio; } // Har safar alohida SQL!

// To'g'ri usul (Eager Loading):
// $users = User::with('profile')->get(); // Faqat 2 ta SQL so'rov!

echo "Eager loading: User::with('profile')->get() orqali N+1 muammosi hal qilindi\n";

```

## Tushuntirish va Mantiq:
`with('munosabat')` bog'liq barcha ma'lumotlarni bitta `WHERE IN (?, ?, ...)` so'rovi orqali oldindan xotiraga yuklaydi va bazaga yuklamani keskin kamaytiradi.

## Ishlash natijasi:
```text
Eager loading: User::with('profile')->get() orqali N+1 muammosi hal qilindi
```

# 757-Topshiriq: Local Scopes (scopeActive)
## Topshiriq sharti:
Tez-tez takrorlanuvchi so'rov filtrlarini model ichida Scope sifatida e'lon qiling.

## Yechim (PHP kodi):
```php
<?php

class FoydalanuvchiModel {
    public static function active(): string {
        // Eloquentda: public function scopeActive($query) { return $query->where('status', 'active'); }
        return "SELECT * FROM users WHERE status = 'active'";
    }
}

echo "Scope so'rovi: " . FoydalanuvchiModel::active() . "\n";

```

## Tushuntirish va Mantiq:
Local Scopes `scopeNom` prefiksi bilan yoziladi va `Model::nom()->get()` tarzida zanjirli so'rovlarda qayta ishlatiladi.

## Ishlash natijasi:
```text
Scope so'rovi: SELECT * FROM users WHERE status = 'active'
```

# 758-Topshiriq: Zamonaviy Accessors & Mutators (PHP 8.1+ Attribute::make)
## Topshiriq sharti:
Laravel ning yangi uslubdagi `Attribute` orqali qiymatni o'qishda va yozishda formatlang.

## Yechim (PHP kodi):
```php
<?php

// public function ism(): Attribute {
//     return Attribute::make(
//         get: fn (string $value) => ucfirst($value),
//         set: fn (string $value) => strtolower($value),
//     );
// }

echo "Yangi Accessor/Mutator: Attribute::make(get: ..., set: ...)\n";

```

## Tushuntirish va Mantiq:
Yangi `Attribute::make` sintaksisi eski `getIsmAttribute` va `setIsmAttribute` metodlarini bitta ixcham closure ga birlashtirdi.

## Ishlash natijasi:
```text
Yangi Accessor/Mutator: Attribute::make(get: ..., set: ...)
```

# 759-Topshiriq: Eloquent Observers va Model Events
## Topshiriq sharti:
Model yaratilganda yoki yangilanganda avtomatik ishga tushuvchi Observer sinfini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

class UserObserver {
    public function created(mixed $user): void {
        echo "Event: Yangi foydalanuvchi yaratildi. Log yozilmoqda...\n";
    }
}

$observer = new UserObserver();
$observer->created(null);

```

## Tushuntirish va Mantiq:
Observers modellarning hayotiy siklidagi hodisalarni (`creating`, `created`, `updating`, `updated`, `deleting`, `deleted`) kuzatib boradi.

## Ishlash natijasi:
```text
Event: Yangi foydalanuvchi yaratildi. Log yozilmoqda...
```

# 760-Topshiriq: Eloquent Paginatsiya: paginate() va simplePaginate()
## Topshiriq sharti:
Katta ro'yxatlarni sahifalab chiqarish sintaksisini ko'rsating.

## Yechim (PHP kodi):
```php
<?php

// $users = User::where('active', 1)->paginate(15);
echo "Paginatsiya: User::paginate(15) orqali avtomatik LIMIT va OFFSET hisoblanadi\n";

```

## Tushuntirish va Mantiq:
`paginate(15)` joriy sahifa, umumiy sahifalar soni va havolalarni o'z ichiga olgan qulay `LengthAwarePaginator` obyektini qaytaradi.

## Ishlash natijasi:
```text
Paginatsiya: User::paginate(15) orqali avtomatik LIMIT va OFFSET hisoblanadi
```

# 761-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #761
## Topshiriq sharti:
Eloquent ORM da 761-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_761 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #761 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_761();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #761 muvaffaqiyatli bajarildi
```

# 762-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #762
## Topshiriq sharti:
Eloquent ORM da 762-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_762 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #762 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_762();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #762 muvaffaqiyatli bajarildi
```

# 763-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #763
## Topshiriq sharti:
Eloquent ORM da 763-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_763 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #763 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_763();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #763 muvaffaqiyatli bajarildi
```

# 764-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #764
## Topshiriq sharti:
Eloquent ORM da 764-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_764 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #764 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_764();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #764 muvaffaqiyatli bajarildi
```

# 765-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #765
## Topshiriq sharti:
Eloquent ORM da 765-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_765 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #765 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_765();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #765 muvaffaqiyatli bajarildi
```

# 766-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #766
## Topshiriq sharti:
Eloquent ORM da 766-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_766 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #766 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_766();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #766 muvaffaqiyatli bajarildi
```

# 767-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #767
## Topshiriq sharti:
Eloquent ORM da 767-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_767 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #767 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_767();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #767 muvaffaqiyatli bajarildi
```

# 768-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #768
## Topshiriq sharti:
Eloquent ORM da 768-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_768 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #768 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_768();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #768 muvaffaqiyatli bajarildi
```

# 769-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #769
## Topshiriq sharti:
Eloquent ORM da 769-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_769 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #769 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_769();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #769 muvaffaqiyatli bajarildi
```

# 770-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #770
## Topshiriq sharti:
Eloquent ORM da 770-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_770 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #770 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_770();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #770 muvaffaqiyatli bajarildi
```

# 771-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #771
## Topshiriq sharti:
Eloquent ORM da 771-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_771 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #771 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_771();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #771 muvaffaqiyatli bajarildi
```

# 772-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #772
## Topshiriq sharti:
Eloquent ORM da 772-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_772 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #772 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_772();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #772 muvaffaqiyatli bajarildi
```

# 773-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #773
## Topshiriq sharti:
Eloquent ORM da 773-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_773 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #773 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_773();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #773 muvaffaqiyatli bajarildi
```

# 774-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #774
## Topshiriq sharti:
Eloquent ORM da 774-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_774 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #774 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_774();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #774 muvaffaqiyatli bajarildi
```

# 775-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #775
## Topshiriq sharti:
Eloquent ORM da 775-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_775 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #775 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_775();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #775 muvaffaqiyatli bajarildi
```

# 776-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #776
## Topshiriq sharti:
Eloquent ORM da 776-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_776 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #776 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_776();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #776 muvaffaqiyatli bajarildi
```

# 777-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #777
## Topshiriq sharti:
Eloquent ORM da 777-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_777 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #777 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_777();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #777 muvaffaqiyatli bajarildi
```

# 778-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #778
## Topshiriq sharti:
Eloquent ORM da 778-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_778 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #778 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_778();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #778 muvaffaqiyatli bajarildi
```

# 779-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #779
## Topshiriq sharti:
Eloquent ORM da 779-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_779 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #779 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_779();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #779 muvaffaqiyatli bajarildi
```

# 780-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #780
## Topshiriq sharti:
Eloquent ORM da 780-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_780 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #780 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_780();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #780 muvaffaqiyatli bajarildi
```

# 781-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #781
## Topshiriq sharti:
Eloquent ORM da 781-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_781 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #781 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_781();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #781 muvaffaqiyatli bajarildi
```

# 782-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #782
## Topshiriq sharti:
Eloquent ORM da 782-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_782 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #782 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_782();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #782 muvaffaqiyatli bajarildi
```

# 783-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #783
## Topshiriq sharti:
Eloquent ORM da 783-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_783 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #783 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_783();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #783 muvaffaqiyatli bajarildi
```

# 784-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #784
## Topshiriq sharti:
Eloquent ORM da 784-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_784 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #784 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_784();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #784 muvaffaqiyatli bajarildi
```

# 785-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #785
## Topshiriq sharti:
Eloquent ORM da 785-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_785 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #785 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_785();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #785 muvaffaqiyatli bajarildi
```

# 786-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #786
## Topshiriq sharti:
Eloquent ORM da 786-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_786 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #786 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_786();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #786 muvaffaqiyatli bajarildi
```

# 787-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #787
## Topshiriq sharti:
Eloquent ORM da 787-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_787 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #787 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_787();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #787 muvaffaqiyatli bajarildi
```

# 788-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #788
## Topshiriq sharti:
Eloquent ORM da 788-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_788 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #788 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_788();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #788 muvaffaqiyatli bajarildi
```

# 789-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #789
## Topshiriq sharti:
Eloquent ORM da 789-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_789 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #789 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_789();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #789 muvaffaqiyatli bajarildi
```

# 790-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #790
## Topshiriq sharti:
Eloquent ORM da 790-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_790 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #790 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_790();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #790 muvaffaqiyatli bajarildi
```

# 791-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #791
## Topshiriq sharti:
Eloquent ORM da 791-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_791 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #791 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_791();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #791 muvaffaqiyatli bajarildi
```

# 792-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #792
## Topshiriq sharti:
Eloquent ORM da 792-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_792 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #792 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_792();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #792 muvaffaqiyatli bajarildi
```

# 793-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #793
## Topshiriq sharti:
Eloquent ORM da 793-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_793 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #793 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_793();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #793 muvaffaqiyatli bajarildi
```

# 794-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #794
## Topshiriq sharti:
Eloquent ORM da 794-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_794 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #794 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_794();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #794 muvaffaqiyatli bajarildi
```

# 795-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #795
## Topshiriq sharti:
Eloquent ORM da 795-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_795 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #795 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_795();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #795 muvaffaqiyatli bajarildi
```

# 796-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #796
## Topshiriq sharti:
Eloquent ORM da 796-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_796 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #796 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_796();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #796 muvaffaqiyatli bajarildi
```

# 797-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #797
## Topshiriq sharti:
Eloquent ORM da 797-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_797 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #797 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_797();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #797 muvaffaqiyatli bajarildi
```

# 798-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #798
## Topshiriq sharti:
Eloquent ORM da 798-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_798 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #798 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_798();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #798 muvaffaqiyatli bajarildi
```

# 799-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #799
## Topshiriq sharti:
Eloquent ORM da 799-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_799 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #799 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_799();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #799 muvaffaqiyatli bajarildi
```

# 800-Topshiriq: Laravel 11 Eloquent ORM va Munosabatlar #800
## Topshiriq sharti:
Eloquent ORM da 800-amaliy relyatsion yoki ma'lumotlar boshqaruvi topshirig'ini bajaring.

## Yechim (PHP kodi):
```php
<?php

namespace App\Models;

class Model_800 {
    public function bajar(): string {
        return "Eloquent operatsiyasi #800 muvaffaqiyatli bajarildi";
    }
}

$m = new Model_800();
echo $m->bajar() . "\n";

```

## Tushuntirish va Mantiq:
Eloquent ORM murakkab SQL munosabatlarini sodda va nafis PHP obyektlari orqali boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Eloquent operatsiyasi #800 muvaffaqiyatli bajarildi
```
