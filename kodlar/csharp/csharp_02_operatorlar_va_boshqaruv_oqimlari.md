# 2-Mavzu: Operatorlar va Boshqaruv Oqimlari (51-100)

Ushbu bo'limda C# tilining operatorlari, shartli tarmoqlanishlari va zamonaviy pattern matching imkoniyatlari: arifmetik/mantiqiy amallar, qisqa tutashuvli hisoblashlar, null xavfsizligi operatorlari (`??`, `??=`, `?.`, `!`), an'anaviy `if-else` va `switch`, C# 8-12 switch ifodalari (Switch Expressions), tiplar, xossalar, kortejlar va ro'yxatlar bo'yicha pattern matching (`is`, `and`, `or`, `not`, List Patterns) bo'yicha 50 ta amaliy topshiriq jamlangan.

# 51-Topshiriq: Arifmetik operatorlar va butun sonli bo'linish
## Topshiriq sharti:
Asosiy arifmetik operatorlarni (`+`, `-`, `*`, `/`, `%`) qo'llang va butun sonli bo'lish bilan haqiqiy sonli bo'lish orasidagi farqni ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int a = 17;
        int b = 5;

        int butunBolinma = a / b;
        int qoldiq = a % b;
        double haqiqiyBolinma = (double)a / b;

        Console.WriteLine($"17 / 5 (butun): {butunBolinma}");
        Console.WriteLine($"17 % 5 (qoldiq): {qoldiq}");
        Console.WriteLine($"17 / 5 (haqiqiy): {haqiqiyBolinma}");
    }
}

```

## Tushuntirish va Mantiq:
C# da ikkita butun son bo'linganda natija har doim butun son bo'ladi va kasr qismi tashlab yuboriladi. Haqiqiy kasr natija olish uchun operantlardan kamida bittasini `double` yoki `float` turiga kasting qilish zarur. `%` operatori esa qoldiqni hisoblaydi.

## Ishlash natijasi:
```text
17 / 5 (butun): 3
17 % 5 (qoldiq): 2
17 / 5 (haqiqiy): 3.4
```

# 52-Topshiriq: Prefiks va postfiks inkrement/dekrement farqi
## Topshiriq sharti:
`++x` (prefiks) va `x++` (postfiks) operatorlarining ifoda ichida bajarilish ketma-ketligini amalda ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int x = 5;
        int y = 5;

        int natijaPostfiks = x++; // Avval qiymat beriladi, keyin x ortadi
        int natijaPrefiks = ++y;  // Avval y ortadi, keyin qiymat beriladi

        Console.WriteLine($"Postfiks natija: {natijaPostfiks}, x ning hozirgi qiymati: {x}");
        Console.WriteLine($"Prefiks natija:  {natijaPrefiks}, y ning hozirgi qiymati: {y}");
    }
}

```

## Tushuntirish va Mantiq:
Postfiks (`x++`) operatorida o'zgaruvchining joriy qiymati ifodada ishlatiladi va shundan so'ng qiymat 1 ga oshiriladi. Prefiks (`++x`) operatorida esa avval o'zgaruvchi 1 ga oshiriladi, so'ng yangilangan qiymat ifodaga uzatiladi.

## Ishlash natijasi:
```text
Postfiks natija: 5, x ning hozirgi qiymati: 6
Prefiks natija:  6, y ning hozirgi qiymati: 6
```

# 53-Topshiriq: Murakkab o'zlashtirish operatorlari (Compound Assignment)
## Topshiriq sharti:
`+=`, `-=`, `*=`, `/=`, `%=` operatorlaridan foydalanib o'zgaruvchi qiymatini qisqa uslubda yangilang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int hisob = 100;
        hisob += 50; // hisob = hisob + 50 (150)
        hisob -= 30; // 120
        hisob *= 2;  // 240
        hisob /= 4;  // 60
        hisob %= 7;  // 60 % 7 = 4

        Console.WriteLine($"Yakuniy hisob: {hisob}");
    }
}

```

## Tushuntirish va Mantiq:
Murakkab o'zlashtirish operatorlari kod hajmini qisqartiradi va chap tomondagi ifodaning faqat bir marta baholanishini ta'minlaydi. Masalan, `massiv[MurakkabHisob()] += 5` da indeks hisoblash funksiyasi faqat bitta marta chaqiriladi.

## Ishlash natijasi:
```text
Yakuniy hisob: 4
```

# 54-Topshiriq: Taqqoslash operatorlari va mantiqiy natija
## Topshiriq sharti:
Sonlarni taqqoslash operatorlari (`==`, `!=`, `<`, `>`, `<=`, `>=`) yordamida mantiqiy (`bool`) natijalar oling.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int yosh = 20;

        Console.WriteLine($"yosh == 18: {yosh == 18}");
        Console.WriteLine($"yosh != 18: {yosh != 18}");
        Console.WriteLine($"yosh >= 18: {yosh >= 18}");
        Console.WriteLine($"yosh < 25:  {yosh < 25}");
    }
}

```

## Tushuntirish va Mantiq:
Taqqoslash operatorlari har doim `bool` qiymat (`true` yoki `false`) qaytaradi. Ular dasturning tarmoqlanish nuqtalarida, `if` va `while` operatorlarida shart sifatida xizmat qiladi.

## Ishlash natijasi:
```text
yosh == 18: False
yosh != 18: True
yosh >= 18: True
yosh < 25:  True
```

# 55-Topshiriq: Qisqa tutashuvli mantiqiy operatorlar: && va ||
## Topshiriq sharti:
`&&` (Short-circuit AND) va `||` (Short-circuit OR) operatorlarining ikkinchi shartni bekor qilish harakatini isbotlang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static bool XavfliMetod()
    {
        Console.WriteLine("--> XavfliMetod chaqirildi!");
        return true;
    }

    static void Main()
    {
        Console.WriteLine("1-Sinov (false && XavfliMetod):");
        bool natija1 = false && XavfliMetod(); // Ikkinchi tomon umuman chaqirilmaydi!

        Console.WriteLine("2-Sinov (true || XavfliMetod):");
        bool natija2 = true || XavfliMetod();  // Ikkinchi tomon umuman chaqirilmaydi!

        Console.WriteLine($"natija1: {natija1}, natija2: {natija2}");
    }
}

```

## Tushuntirish va Mantiq:
Short-circuit (qisqa tutashuv) mexanizmi bo'yicha: `&&` da chap tomon `false` bo'lsa, o'ng tomon natijadan qat'i nazar `false` bo'lgani uchun o'ng tomon hisoblanmaydi. `||` da esa chap tomon `true` bo'lsa, o'ng tomon hisoblanmaydi. Bu orqali `null` tekshiruvlarini xavfsiz qilish mumkin (`obj != null && obj.IsActive`).

## Ishlash natijasi:
```text
1-Sinov (false && XavfliMetod):
2-Sinov (true || XavfliMetod):
natija1: False, natija2: True
```

# 56-Topshiriq: To'liq hisoblanuvchi mantiqiy operatorlar: & va |
## Topshiriq sharti:
`bool` ustida ishlovchi oddiy `&` va `|` operatorlarining har ikkala tomonni majburiy hisoblashini namoyish eting.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static bool LogYozish(string xabar)
    {
        Console.WriteLine($"Log: {xabar}");
        return true;
    }

    static void Main()
    {
        Console.WriteLine("Oddiy & operatori sinovi:");
        bool test = false & LogYozish("Bu xabar baribir chiqadi!");
        Console.WriteLine($"Natija: {test}");
    }
}

```

## Tushuntirish va Mantiq:
Agar `&` yoki `|` operatorlari mantiqiy (`bool`) qiymatlar bilan ishlatilsa, ular qisqa tutashuv qilmaydi, balki ikkala tomonni ham to'liq bajaradi. Odatda yon ta'sirlarni (side-effects) boshqarish yoki aniq hisoblash lozim bo'lganda qo'llaniladi.

## Ishlash natijasi:
```text
Oddiy & operatori sinovi:
Log: Bu xabar baribir chiqadi!
Natija: False
```

# 57-Topshiriq: Ternary shartli operatori: ? :
## Topshiriq sharti:
`shart ? rost : yolgon` ternary operatoridan foydalanib ixcham shartli ifoda yozing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int ball = 85;
        string natija = ball >= 60 ? "Imtihondan o'tdi" : "Yiqildi";
        int chegirma = ball > 80 ? 20 : 5;

        Console.WriteLine($"Talaba holati: {natija}");
        Console.WriteLine($"Chegirma foizi: {chegirma}%");
    }
}

```

## Tushuntirish va Mantiq:
Ternary operatori uchta operand qabul qiladi. U bayonot (statement) emas, balki ifoda (expression) bo'lgani uchun o'zgaruvchiga to'g'ridan-to'g'ri qiymat o'zlashtirish yoki metodga argument sifatida uzatish imkonini beradi.

## Ishlash natijasi:
```text
Talaba holati: Imtihondan o'tdi
Chegirma foizi: 20%
```

# 58-Topshiriq: Null-coalescing operatori: ??
## Topshiriq sharti:
O'zgaruvchi `null` bo'lgan holatda zaxira qiymat berish uchun `??` operatoridan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        string? foydalanuvchiIsmi = null;
        string korsatish = foydalanuvchiIsmi ?? "Mehmon";

        Console.WriteLine($"Xush kelibsiz, {korsatish}!");

        foydalanuvchiIsmi = "Anvar";
        korsatish = foydalanuvchiIsmi ?? "Mehmon";
        Console.WriteLine($"Xush kelibsiz, {korsatish}!");
    }
}

```

## Tushuntirish va Mantiq:
`??` operatori chap tarafdagi operand `null` bo'lmasa, uning qiymatini qaytaradi; agar `null` bo'lsa, o'ng tarafdagi zaxira qiymatni qaytaradi. Bu `if (x == null)` tekshiruvlarini bir qatorga tushiradi.

## Ishlash natijasi:
```text
Xush kelibsiz, Mehmon!
Xush kelibsiz, Anvar!
```

# 59-Topshiriq: Null-coalescing assignment operatori: ??=
## Topshiriq sharti:
C# 8 da kiritilgan `??=` operatori yordamida o'zgaruvchi faqat `null` bo'lgan holdagina unga qiymat biriktiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        string? shahar = null;
        shahar ??= "Toshkent"; // shahar null edi, Toshkent qiymatini oladi
        Console.WriteLine($"1-bosqich: {shahar}");

        shahar ??= "Samarqand"; // shahar endi null emas, qiymat o'zgarmaydi
        Console.WriteLine($"2-bosqich: {shahar}");
    }
}

```

## Tushuntirish va Mantiq:
`o'zgaruvchi ??= qiymat` ifodasi `if (o'zgaruvchi == null) o'zgaruvchi = qiymat;` kodining toza va ixcham ko'rinishidir. Kechiktirilgan initsializatsiya (lazy initialization) uchun juda qulay.

## Ishlash natijasi:
```text
1-bosqich: Toshkent
2-bosqich: Toshkent
```

# 60-Topshiriq: Null-conditional operatori: ?. va ?[]
## Topshiriq sharti:
`NullReferenceException` xatosidan saqlanish uchun obyekt xossalariga va massiv elementlariga `?.` hamda `?[]` orqali xavfsiz kiring.

## Yechim (C# kodi):
```csharp
using System;

class Foydalanuvchi
{
    public string? Ism { get; set; }
}

internal class Program
{
    static void Main()
    {
        Foydalanuvchi? user = null;

        // An'anaviy usulda xato otadi: user.Ism.Length
        // Null-conditional xavfsiz null qaytaradi
        int? uzunlik = user?.Ism?.Length;

        Console.WriteLine($"Ism uzunligi: {(uzunlik == null ? "Mavjud emas (null)" : uzunlik.ToString())}");

        string[]? massiv = null;
        string? birinchi = massiv?[0];
        Console.WriteLine($"Massiv birinchi elementi: {(birinchi == null ? "null" : birinchi)}");
    }
}

```

## Tushuntirish va Mantiq:
`?.` operatori zanjirdagi birinchi `null` uchragan zahoti qolgan amallarni to'xtatadi va butun ifoda natijasi sifatida `null` qaytaradi. Bu dasturni kutilmagan qulashlardan (crash) asraydi.

## Ishlash natijasi:
```text
Ism uzunligi: Mavjud emas (null)
Massiv birinchi elementi: null
```

# 61-Topshiriq: Null-forgiving operatori: !
## Topshiriq sharti:
Nullable ogohlantirishlarini bostirish uchun `!` (null-forgiving) operatoridan foydalanish va uning runtime da ta'sirsizligini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static string? GetMatn() => "Salom .NET";

    static void Main()
    {
        string? matn = GetMatn();

        // Kompilyatorga 'matn null emasligiga kafolat beraman' deb bildirish
        string aniqMatn = matn!;

        Console.WriteLine($"Matn: {aniqMatn}, Uzunligi: {aniqMatn.Length}");
    }
}

```

## Tushuntirish va Mantiq:
`!` operatori faqat kompilyatsiya vaqtidagi statik analizator ogohlantirishini (CS8600, CS8602) bostiradi. U runtime da hech qanday kod generatsiya qilmaydi. Agar qiymat baribir `null` bo'lib chiqsa, runtime da `NullReferenceException` kelib chiqadi.

## Ishlash natijasi:
```text
Matn: Salom .NET, Uzunligi: 10
```

# 62-Topshiriq: if, else if va else shartli tarmoqlanishi
## Topshiriq sharti:
Harorat darajasiga qarab holatni aniqlovchi ko'p tarmoqli `if-else if-else` tuzilmasini yozing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int harorat = 22;

        if (harorat < 0)
        {
            Console.WriteLine("Havo juda sovuq, muzlama.");
        }
        else if (harorat >= 0 && harorat < 15)
        {
            Console.WriteLine("Havo salqin.");
        }
        else if (harorat >= 15 && harorat < 30)
        {
            Console.WriteLine("Havo yoqimli va iliq.");
        }
        else
        {
            Console.WriteLine("Havo juda issiq.");
        }
    }
}

```

## Tushuntirish va Mantiq:
`if` operatori shart rost (`true`) bo'lganda birinchi mos kelgan blokni bajaradi va qolgan shartlarni tekshirmasdan sakrab o'tadi. Barcha shartlar yolg'on bo'lsa, `else` bloki ishga tushadi.

## Ishlash natijasi:
```text
Havo yoqimli va iliq.
```

# 63-Topshiriq: Guard Clause (Himoya bandi) uslubi: Ichma-ich if lardan qutulish
## Topshiriq sharti:
Chuqur ichma-ich joylashgan `if` larni (Arrow Anti-pattern) erta qaytish (`return`) orqali Guard Clause uslubida tozalang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void RoyxatdanOtish(string? ism, int yosh)
    {
        // Guard Clauses - xatoliklarni boshidayoq tekshirib qaytarish
        if (string.IsNullOrWhiteSpace(ism))
        {
            Console.WriteLine("Xato: Ism kiritilishi shart!");
            return;
        }

        if (yosh < 18)
        {
            Console.WriteLine("Xato: Yosh 18 dan kichik bo'lishi mumkin emas!");
            return;
        }

        // Asosiy muvaffaqiyatli mantiq
        Console.WriteLine($"Muvaffaqiyatli: {ism} ro'yxatga olindi.");
    }

    static void Main()
    {
        RoyxatdanOtish("", 20);
        RoyxatdanOtish("Dilshod", 16);
        RoyxatdanOtish("Dilshod", 22);
    }
}

```

## Tushuntirish va Mantiq:
Guard Clause uslubi kodning o'qilishini tubdan yaxshilaydi. Noto'g'ri shartlar boshidayoq `return` bilan kesiladi, natijada asosiy biznes mantiq surilishlarsiz (nesting bo'lmasdan) toza saqlanadi.

## Ishlash natijasi:
```text
Xato: Ism kiritilishi shart!
Xato: Yosh 18 dan kichik bo'lishi mumkin emas!
Muvaffaqiyatli: Dilshod ro'yxatga olindi.
```

# 64-Topshiriq: An'anaviy switch bayonoti va break qoidasi
## Topshiriq sharti:
Hafta kuni raqamiga qarab ish yoki dam olish kuni ekanligini an'anaviy `switch-case` yordamida aniqlang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int kun = 6;

        switch (kun)
        {
            case 1:
            case 2:
            case 3:
            case 4:
            case 5:
                Console.WriteLine("Ish kuni");
                break;
            case 6:
            case 7:
                Console.WriteLine("Dam olish kuni");
                break;
            default:
                Console.WriteLine("Noto'g'ri kun raqami!");
                break;
        }
    }
}

```

## Tushuntirish va Mantiq:
C# da an'anaviy `switch` da har bir blok `break`, `return` yoki `goto` bilan yopilishi shart (bo'sh case lar bundan mustasno bo'lib, ular bitta guruhga birlashadi). Bu C/C++ dagi kutilmagan tushib ketish (fall-through) xatolarini oldini oladi.

## Ishlash natijasi:
```text
Dam olish kuni
```

# 65-Topshiriq: switch ichida goto case va tushib ketishni boshqarish
## Topshiriq sharti:
Bir holatdan ikkinchi holatga o'tish zarur bo'lganda `goto case` dan qanday foydalanishni ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int bosqich = 1;

        switch (bosqich)
        {
            case 1:
                Console.WriteLine("1-Bosqich: Boshlang'ich konfiguratsiya");
                goto case 2; // Qasddan keyingi bosqichga o'tish
            case 2:
                Console.WriteLine("2-Bosqich: Xizmatlarni yuklash");
                break;
            default:
                Console.WriteLine("Noma'lum bosqich");
                break;
        }
    }
}

```

## Tushuntirish va Mantiq:
`goto case X;` C# da `switch` ichida qasddan keyingi case ga o'tishning yagona qonuniy usulidir. Bu murakkab zanjirli holat mashinalarida (pipeline) kodni takrorlamaslik uchun ishlatiladi.

## Ishlash natijasi:
```text
1-Bosqich: Boshlang'ich konfiguratsiya
2-Bosqich: Xizmatlarni yuklash
```

# 66-Topshiriq: Zamonaviy switch ifodasi (Switch Expression)
## Topshiriq sharti:
C# 8 da kiritilgan ixcham `switch` ifodasidan foydalanib rang nomiga qarab uning HEX kodini qaytaring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static string RangHexKodi(string rang) => rang.ToLower() switch
    {
        "qizil"  => "#FF0000",
        "yashil" => "#00FF00",
        "kok"    => "#0000FF",
        _        => "#000000" // Standart diskard
    };

    static void Main()
    {
        Console.WriteLine($"Qizil: {RangHexKodi("qizil")}");
        Console.WriteLine($"Ko'k: {RangHexKodi("kok")}");
        Console.WriteLine($"Boshqa: {RangHexKodi("sariq")}");
    }
}

```

## Tushuntirish va Mantiq:
Switch Expression an'anaviy `switch` ga nisbatan ancha qisqa va qulay. `case` va `break` so'zlari o'rniga `=>` (lambda) qo'llaniladi, `default` o'rniga esa pastki chiziq `_` (discard) ishlatiladi.

## Ishlash natijasi:
```text
Qizil: #FF0000
Ko'k: #0000FF
Boshqa: #000000
```

# 67-Topshiriq: Pattern Matching: Type Pattern (Tur bo'yicha tekshirish)
## Topshiriq sharti:
`is` operatori yordamida obyektning turini tekshirib, bir vaqtning o'zida uni yangi o'zgaruvchiga kasting qiling.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void MalumotniChiqar(object obj)
    {
        if (obj is int raqam)
        {
            Console.WriteLine($"Butun son: {raqam}, kvadrati: {raqam * raqam}");
        }
        else if (obj is string matn)
        {
            Console.WriteLine($"Matn: '{matn}', belgilar soni: {matn.Length}");
        }
        else
        {
            Console.WriteLine($"Boshqa tur: {obj.GetType().Name}");
        }
    }

    static void Main()
    {
        MalumotniChiqar(12);
        MalumotniChiqar("O'zbekiston");
        MalumotniChiqar(3.14);
    }
}

```

## Tushuntirish va Mantiq:
Type Pattern (`obj is Tur nom`) bir amalda ikkita ishni bajaradi: birinchidan, obyektning berilgan turga mansubligini tekshiradi; ikkinchidan, uni xavfsiz o'sha turga o'tkazib yangi o'zgaruvchi yaratadi.

## Ishlash natijasi:
```text
Butun son: 12, kvadrati: 144
Matn: 'O'zbekiston', belgilar soni: 11
Boshqa tur: Double
```

# 68-Topshiriq: Pattern Matching: Constant Pattern
## Topshiriq sharti:
Switch ifodasida o'zgarmas literallar (null, sonlar, satrlar) bo'yicha pattern matching qo'llang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static string HolatMatni(int kod) => kod switch
    {
        0 => "Muvaffaqiyatli",
        1 => "Ogohlantirish",
        2 => "Kritik xatolik",
        _ => "Noma'lum status"
    };

    static void Main()
    {
        Console.WriteLine($"Status 0: {HolatMatni(0)}");
        Console.WriteLine($"Status 2: {HolatMatni(2)}");
        Console.WriteLine($"Status 9: {HolatMatni(9)}");
    }
}

```

## Tushuntirish va Mantiq:
Constant pattern tekshirilayotgan ifodani aniq konstanta qiymat bilan tenglikka solishtiradi. Bu an'anaviy `switch` ning eng yaqin zamonaviy muqobilidir.

## Ishlash natijasi:
```text
Status 0: Muvaffaqiyatli
Status 2: Kritik xatolik
Status 9: Noma'lum status
```

# 69-Topshiriq: Pattern Matching: Relational Pattern (Nisbiy solishtirish)
## Topshiriq sharti:
C# 9 da kiritilgan `<`, `<=`, `>`, `>=` relatsion patternlaridan foydalanib yosh toifasini aniqlang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static string YoshToifasi(int yosh) => yosh switch
    {
        < 0  => "Noto'g'ri yosh",
        < 7  => "Maktabgacha yoshdagi bola",
        < 18 => "Maktab o'quvchisi",
        < 60 => "Mehnatga layoqatli katta yoshli",
        _    => "Faxriy nafaqaxo'r"
    };

    static void Main()
    {
        Console.WriteLine($"5 yosh: {YoshToifasi(5)}");
        Console.WriteLine($"15 yosh: {YoshToifasi(15)}");
        Console.WriteLine($"30 yosh: {YoshToifasi(30)}");
        Console.WriteLine($"65 yosh: {YoshToifasi(65)}");
    }
}

```

## Tushuntirish va Mantiq:
Relational Pattern sonlarni taqqoslash operatorlari bilan bevosita switch ichida solishtirishga imkon beradi. Kod tartib bilan yuqoridan pastga tekshiriladi va birinchi mos kelgan relatsiya bajariladi.

## Ishlash natijasi:
```text
5 yosh: Maktabgacha yoshdagi bola
15 yosh: Maktab o'quvchisi
30 yosh: Mehnatga layoqatli katta yoshli
65 yosh: Faxriy nafaqaxo'r
```

# 70-Topshiriq: Pattern Matching: Mantiqiy kombinatsiyalar (and, or, not)
## Topshiriq sharti:
`and`, `or`, `not` so'zlari yordamida bir nechta shartlarni birlashtiruvchi mantiqiy pattern tuzing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static bool IshVaqtimi(int soat) => soat is >= 9 and <= 18;

    static bool DamOlishKunimi(string kun) => kun.ToLower() is "shanba" or "yakshanba";

    static void Main()
    {
        Console.WriteLine($"Soat 14 ish vaqtimi: {IshVaqtimi(14)}");
        Console.WriteLine($"Soat 20 ish vaqtimi: {IshVaqtimi(20)}");
        Console.WriteLine($"Juma dam olish kunimi: {DamOlishKunimi("Juma")}");
        Console.WriteLine($"Yakshanba dam olish kunimi: {DamOlishKunimi("Yakshanba")}");
    }
}

```

## Tushuntirish va Mantiq:
C# 9 dan boshlab kiritilgan `and`, `or`, `not` kalit so'zlari faqat pattern matching kontekstida ishlaydi. Ular `&&`, `||`, `!` belgilariga qaraganda tabiiy tilga yaqin va o'qish uchun juda qulay.

## Ishlash natijasi:
```text
Soat 14 ish vaqtimi: True
Soat 20 ish vaqtimi: False
Juma dam olish kunimi: False
Yakshanba dam olish kunimi: True
```

# 71-Topshiriq: Pattern Matching: is not null tekshiruvi
## Topshiriq sharti:
Eski `!= null` o'rniga zamonaviy va xavfsiz `is not null` patternidan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void SalomBer(string? ism)
    {
        if (ism is not null)
        {
            Console.WriteLine($"Assalomu alaykum, {ism}!");
        }
        else
        {
            Console.WriteLine("Ism ko'rsatilmadi!");
        }
    }

    static void Main()
    {
        SalomBer("Bobur");
        SalomBer(null);
    }
}

```

## Tushuntirish va Mantiq:
`is not null` patternining muhim ustunligi shundaki, agar sinfda `==` yoki `!=` operatorlari qayta yuklangan (overload) bo'lsa ham, `is not null` to'g'ridan-to'g'ri xotiradagi havolani tekshiradi va hech qanday operator buzilishlariga uchramaydi.

## Ishlash natijasi:
```text
Assalomu alaykum, Bobur!
Ism ko'rsatilmadi!
```

# 72-Topshiriq: Property Pattern: Obyekt xossalarini tekshirish
## Topshiriq sharti:
Obyektning xossalari qiymatiga qarab shart bajaruvchi Property Pattern (`{ Xossa: qiymat }`) ni qo'llang.

## Yechim (C# kodi):
```csharp
using System;

class Xodim
{
    public string Ism { get; set; } = "";
    public string Lavozim { get; set; } = "";
    public int TajribaYil { get; set; }
}

internal class Program
{
    static decimal BonusHisobla(Xodim xodim) => xodim switch
    {
        { Lavozim: "Direktor" } => 5000m,
        { Lavozim: "Dasturchi", TajribaYil: >= 3 } => 3000m,
        { Lavozim: "Dasturchi" } => 1500m,
        _ => 500m
    };

    static void Main()
    {
        var x1 = new Xodim { Ism = "Rustam", Lavozim = "Dasturchi", TajribaYil = 5 };
        var x2 = new Xodim { Ism = "Ali", Lavozim = "Direktor", TajribaYil = 2 };

        Console.WriteLine($"{x1.Ism} bonusi: {BonusHisobla(x1)}$");
        Console.WriteLine($"{x2.Ism} bonusi: {BonusHisobla(x2)}$");
    }
}

```

## Tushuntirish va Mantiq:
Property Pattern obyektning ichki xossalarini alohida `if (xodim.Lavozim == ...)` yozmasdan, to'g'ridan-to'g'ri naqsh (pattern) ichida tekshirish imkonini beradi. Bir vaqtning o'zida bir nechta xossalar tekshirilishi mumkin.

## Ishlash natijasi:
```text
Rustam bonusi: 3000$
Ali bonusi: 5000$
```

# 73-Topshiriq: Nested Property Pattern: Ichki obyektlar xossalarini tekshirish
## Topshiriq sharti:
C# 10 da soddalashtirilgan kengaytirilgan xossalar patterni (`{ Manzil.Shahar: "Toshkent" }`) dan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

class Manzil
{
    public string Shahar { get; set; } = "";
}

class Mijoz
{
    public string Ism { get; set; } = "";
    public Manzil? Manzil { get; set; }
}

internal class Program
{
    static decimal YetkazibBerishNarxi(Mijoz mijoz) => mijoz switch
    {
        { Manzil.Shahar: "Toshkent" } => 20000m, // Ichki ob'yekt xossasi
        { Manzil.Shahar: "Samarqand" or "Buxoro" } => 40000m,
        { Manzil: not null } => 60000m,
        _ => 0m
    };

    static void Main()
    {
        var m1 = new Mijoz { Ism = "Nodir", Manzil = new Manzil { Shahar = "Toshkent" } };
        var m2 = new Mijoz { Ism = "Sardor", Manzil = new Manzil { Shahar = "Samarqand" } };

        Console.WriteLine($"{m1.Ism} uchun yetkazish: {YetkazibBerishNarxi(m1)} so'm");
        Console.WriteLine($"{m2.Ism} uchun yetkazish: {YetkazibBerishNarxi(m2)} so'm");
    }
}

```

## Tushuntirish va Mantiq:
C# 10 gacha `{ Manzil: { Shahar: "Toshkent" } }` deb yozish talab qilinar edi. C# 10 dan boshlab nuqta belgisi orqali chuqur joylashgan obyekt xossalarini to'g'ridan-to'g'ri tekshirish mumkin.

## Ishlash natijasi:
```text
Nodir uchun yetkazish: 20000 so'm
Sardor uchun yetkazish: 40000 so'm
```

# 74-Topshiriq: Tuple Pattern: Kortejlarni switch da solishtirish
## Topshiriq sharti:
Ikki yoki undan ortiq qiymatlarni bir vaqtda tekshirish uchun Tuple Pattern (`(a, b) switch`) dan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static string KirishRuxsati(string rol, bool kartaBormi) => (rol, kartaBormi) switch
    {
        ("Admin", _)      => "To'liq ruxsat (Admin)",
        ("Xodim", true)   => "Ruxsat berildi",
        ("Xodim", false)  => "Karta talab qilinadi",
        ("Mehmon", _)     => "Faqat kuzatuvchi",
        _                 => "Kirish taqiqlangan"
    };

    static void Main()
    {
        Console.WriteLine(KirishRuxsati("Admin", false));
        Console.WriteLine(KirishRuxsati("Xodim", true));
        Console.WriteLine(KirishRuxsati("Xodim", false));
    }
}

```

## Tushuntirish va Mantiq:
Tuple Pattern bir vaqtning o'zida bir nechta o'zgaruvchilar holatini tekshirishda juda qo'l keladi. `_` (diskard) operatori qaysidir parametr qiymati bu holatda ahamiyatsiz ekanligini bildiradi.

## Ishlash natijasi:
```text
To'liq ruxsat (Admin)
Ruxsat berildi
Karta talab qilinadi
```

# 75-Topshiriq: Positional Pattern va Deconstruct metodi
## Topshiriq sharti:
Sinf ichida `Deconstruct` metodini e'lon qilib, uni Positional Pattern orqali ochib tekshiring.

## Yechim (C# kodi):
```csharp
using System;

class Nuqta
{
    public int X { get; }
    public int Y { get; }

    public Nuqta(int x, int y) => (X, Y) = (x, y);

    public void Deconstruct(out int x, out int y) => (x, y) = (X, Y);
}

internal class Program
{
    static string NuqtaJoylashuvi(Nuqta n) => n switch
    {
        (0, 0) => "Koordinata boshi (Markaz)",
        (var x, 0) => $"X o'qida: {x}",
        (0, var y) => $"Y o'qida: {y}",
        (var x, var y) when x > 0 && y > 0 => $"1-chorakda ({x}, {y})",
        _ => "Boshqa chorakda"
    };

    static void Main()
    {
        Console.WriteLine(NuqtaJoylashuvi(new Nuqta(0, 0)));
        Console.WriteLine(NuqtaJoylashuvi(new Nuqta(5, 0)));
        Console.WriteLine(NuqtaJoylashuvi(new Nuqta(3, 4)));
    }
}

```

## Tushuntirish va Mantiq:
Positional Pattern sinf ob'yektini uning `Deconstruct` metodi orqali kortejga ajratadi va elementlar tartibi bo'yicha solishtiradi. Bu geometriya, koordinatalar va domen modellarini tahlil qilishda o'ta qulay.

## Ishlash natijasi:
```text
Koordinata boshi (Markaz)
X o'qida: 5
1-chorakda (3, 4)
```

# 76-Topshiriq: C# 11 List Pattern: Massiv elementlari bo'yicha aniq moslik
## Topshiriq sharti:
C# 11 da kiritilgan List Pattern yordamida massiv yoki ro'yxatdagi elementlar ketma-ketligini tekshiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static string MassivniTekshir(int[] sonlar) => sonlar switch
    {
        [] => "Massiv bo'sh",
        [var yagona] => $"Faqat bitta element: {yagona}",
        [1, 2, 3] => "Klassik 1, 2, 3 ketma-ketligi",
        [0, ..] => "Nol bilan boshlanuvchi massiv",
        _ => "Boshqa ixtiyoriy massiv"
    };

    static void Main()
    {
        Console.WriteLine(MassivniTekshir(Array.Empty<int>()));
        Console.WriteLine(MassivniTekshir(new[] { 42 }));
        Console.WriteLine(MassivniTekshir(new[] { 1, 2, 3 }));
        Console.WriteLine(MassivniTekshir(new[] { 0, 99, 100 }));
    }
}

```

## Tushuntirish va Mantiq:
List Pattern (`[...]`) to'plam uzunligini va uning ichidagi aniq elementlarni bitta ifodada tekshirish imkonini beradi. `[]` bo'sh ro'yxatni, `[0, ..]` esa 0 bilan boshlanib, qolgan elementlari har qanday bo'lgan massivni bildiradi.

## Ishlash natijasi:
```text
Massiv bo'sh
Faqat bitta element: 42
Klassik 1, 2, 3 ketma-ketligi
Nol bilan boshlanuvchi massiv
```

# 77-Topshiriq: List Pattern: Slice Pattern (..) bilan bosh va oxirgi elementlarni olish
## Topshiriq sharti:
`..` (slice) patterni yordamida massivning boshi va oxiridagi elementlarni ushlab, o'rtadagi elementlarni o'tkazib yuboring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static string ChegaralarniAniqlash(string[] sozlar) => sozlar switch
    {
        [var bosh, .., var oxiri] => $"Boshi: '{bosh}', Oxiri: '{oxiri}'",
        [var yagona] => $"Bitta so'z: '{yagona}'",
        [] => "Ro'yxat bo'sh"
    };

    static void Main()
    {
        string[] matnlar = { "Boshlanish", "O'rta-1", "O'rta-2", "Yakun" };
        Console.WriteLine(ChegaralarniAniqlash(matnlar));
    }
}

```

## Tushuntirish va Mantiq:
Slice patterni (`..`) massivning o'rtasidagi ixtiyoriy miqdordagi (nol yoki undan ko'p) elementlarni qamrab oladi. Bu orqali ro'yxatning birinchi va oxirgi elementlarini o'ta qisqa va qulay sintaksisda ajratib olish mumkin.

## Ishlash natijasi:
```text
Boshi: 'Boshlanish', Oxiri: 'Yakun'
```

# 78-Topshiriq: List Pattern: Diskard (_) bilan aniq pozitsiyalarni tekshirish
## Topshiriq sharti:
Uchta elementdan iborat massivning aynan o'rtadagi elementini diskard (`_`) yordamida oling.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static string OrtadaginiOlish(int[] uchlik) => uchlik switch
    {
        [_, var orta, _] => $"O'rtadagi qiymat: {orta}",
        _ => "Uchta elementdan iborat emas"
    };

    static void Main()
    {
        Console.WriteLine(OrtadaginiOlish(new[] { 10, 20, 30 }));
        Console.WriteLine(OrtadaginiOlish(new[] { 1, 2 }));
    }
}

```

## Tushuntirish va Mantiq:
`[_, var orta, _]` naqshi massivda aniq 3 ta element bo'lishini talab qiladi. Birinchi va uchinchi elementlar qiymatidan qat'i nazar e'tiborsiz qoldiriladi (`_`), o'rtadagi esa `orta` o'zgaruvchisiga o'zlashtiriladi.

## Ishlash natijasi:
```text
O'rtadagi qiymat: 20
Uchta elementdan iborat emas
```

# 79-Topshiriq: Type Pattern bilan polimorfik switch
## Topshiriq sharti:
Har xil geometrik shakllar yuzini bitta switch ifodasida Type Pattern orqali hisoblang.

## Yechim (C# kodi):
```csharp
using System;

abstract class Shakl { }
class Doira : Shakl { public double Radius { get; set; } }
class Tortburchak : Shakl { public double Asos { get; set; } public double Balandlik { get; set; } }

internal class Program
{
    static double YuzaHisobla(Shakl shakl) => shakl switch
    {
        Doira d       => Math.PI * d.Radius * d.Radius,
        Tortburchak t => t.Asos * t.Balandlik,
        _             => 0.0
    };

    static void Main()
    {
        Shakl s1 = new Doira { Radius = 10 };
        Shakl s2 = new Tortburchak { Asos = 5, Balandlik = 8 };

        Console.WriteLine($"Doira yuzi: {YuzaHisobla(s1):F2}");
        Console.WriteLine($"To'rtburchak yuzi: {YuzaHisobla(s2):F2}");
    }
}

```

## Tushuntirish va Mantiq:
Type Pattern yordamida switch ifodasi klassik polimorfizmdan ko'ra moslashuvchan bo'lishi mumkin. Sinf ichiga kirmasdan, tashqaridan turib har xil sinf turlari bo'yicha algoritmlarni ajratishga imkon beradi.

## Ishlash natijasi:
```text
Doira yuzi: 314.16
To'rtburchak yuzi: 40.00
```

# 80-Topshiriq: when shartli filtri bilan switch ifodasi
## Topshiriq sharti:
Case ichida qo'shimcha mantiqiy shartlarni tekshirish uchun `when` filtridan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static string SonniTahlilQil(int son) => son switch
    {
        var n when n < 0 => $"Manfiy son: {n}",
        var n when n % 2 == 0 => $"Musbat juft son: {n}",
        var n when n % 2 != 0 => $"Musbat toq son: {n}",
        _ => "Noma'lum"
    };

    static void Main()
    {
        Console.WriteLine(SonniTahlilQil(-7));
        Console.WriteLine(SonniTahlilQil(12));
        Console.WriteLine(SonniTahlilQil(15));
    }
}

```

## Tushuntirish va Mantiq:
`when` so'zi pattern matching bilan birgalikda qo'shimcha dinamik shartlarni belgilaydi. Pattern mos kelgandan so'ng, faqat `when` ifodasi `true` bo'lsagina ushbu blok ishga tushadi.

## Ishlash natijasi:
```text
Manfiy son: -7
Musbat juft son: 12
Musbat toq son: 15
```

# 81-Topshiriq: Ko'p qiymatli birlashma: or pattern
## Topshiriq sharti:
Bir nechta mumkin bo'lgan qiymatlarni `or` operatori bilan bitta holatda birlashtiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static bool UnliHarfmi(char belgi) => char.ToLower(belgi) switch
    {
        'a' or 'e' or 'i' or 'o' or 'u' => true,
        _ => false
    };

    static void Main()
    {
        Console.WriteLine($"'a' unlimi: {UnliHarfmi('a')}");
        Console.WriteLine($"'B' unlimi: {UnliHarfmi('B')}");
        Console.WriteLine($"'O' unlimi: {UnliHarfmi('O')}");
    }
}

```

## Tushuntirish va Mantiq:
C# 9 da kiritilgan `or` patterni bir nechta konstantalarni tekshirishni bir qatorga jamlaydi. An'anaviy `switch` dagi ko'p sonli `case 'a': case 'e':` yozuvlariga ehtiyoj qolmaydi.

## Ishlash natijasi:
```text
'a' unlimi: True
'B' unlimi: False
'O' unlimi: True
```

# 82-Topshiriq: Var Pattern: Ifoda ichida vaqtinchalik o'zgaruvchi yaratish
## Topshiriq sharti:
Hisoblangan natijani qayta hisoblamasdan oraliq o'zgaruvchiga olish uchun `var pattern` dan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static string HaroratXabari(double selsiy) => (selsiy * 9 / 5 + 32) switch
    {
        var farengeyt when farengeyt > 100 => $"Juda issiq! ({farengeyt:F1}°F)",
        var farengeyt when farengeyt < 32  => $"Muzlama! ({farengeyt:F1}°F)",
        var farengeyt                      => $"Mo'tadil ob-havo ({farengeyt:F1}°F)"
    };

    static void Main()
    {
        Console.WriteLine(HaroratXabari(40));
        Console.WriteLine(HaroratXabari(-5));
        Console.WriteLine(HaroratXabari(20));
    }
}

```

## Tushuntirish va Mantiq:
`var nom` patterni har doim muvaffaqiyatli mos keladi (hech qachon fail bo'lmaydi) va baholangan qiymatni o'zgaruvchiga biriktiradi. Bu formulani bir marta hisoblab, keyingi `when` shartlarida qayta-qayta ishlatishda juda qo'l keladi.

## Ishlash natijasi:
```text
Juda issiq! (104.0°F)
Muzlama! (23.0°F)
Mo'tadil ob-havo (68.0°F)
```

# 83-Topshiriq: Qavsli patternlar (Parenthesized Patterns)
## Topshiriq sharti:
Mantiqiy ustunlikni (operator precedence) qat'iy belgilash uchun qavslar bilan murakkab pattern hosil qiling.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static bool MaxsusOraliqdami(int n) => n is (> 0 and < 10) or (> 90 and < 100);

    static void Main()
    {
        Console.WriteLine($"5 maxsus oraliqdami: {MaxsusOraliqdami(5)}");
        Console.WriteLine($"50 maxsus oraliqdami: {MaxsusOraliqdami(50)}");
        Console.WriteLine($"95 maxsus oraliqdami: {MaxsusOraliqdami(95)}");
    }
}

```

## Tushuntirish va Mantiq:
Pattern matching da qavslardan foydalanish shartlar tartibini aniq boshqarishga imkon beradi (`and` odatda `or` ga nisbatan yuqori ustunlikka ega). Bu chalkashliklarni bartaraf etadi.

## Ishlash natijasi:
```text
5 maxsus oraliqdami: True
50 maxsus oraliqdami: False
95 maxsus oraliqdami: True
```

# 84-Topshiriq: Mantiqiy XOR (^) amali va yagona haqiqiylik sharti
## Topshiriq sharti:
Faqat bitta shart rost bo'lishini talab qiluvchi vaziyatda `^` (mantiqiy XOR) operatorini qo'llang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        bool foydalanuvchiParolKiritdi = true;
        bool foydalanuvchiGoogleBilanKirdi = false;

        // Faqat bitta autentifikatsiya usuli tanlangan bo'lishi shart
        bool yagonaUsul = foydalanuvchiParolKiritdi ^ foydalanuvchiGoogleBilanKirdi;

        Console.WriteLine($"Kirish usuli to'g'rimi: {yagonaUsul}");

        // Agar ikkalasi ham true bo'lsa xato bo'ladi
        bool ikkalasiHam = true ^ true;
        Console.WriteLine($"Ikkala usul ham tanlansa: {ikkalasiHam}");
    }
}

```

## Tushuntirish va Mantiq:
`bool` ustida ishlovchi `^` (XOR) amali ikkala operand qiymati har xil bo'lganda `true`, bir xil bo'lganda (ikkisi ham `true` yoki ikkisi ham `false`) `false` qaytaradi. Bu 'Yoki bu, yoki u, lekin ikkalasi emas' mantiqini ifodalaydi.

## Ishlash natijasi:
```text
Kirish usuli to'g'rimi: True
Ikkala usul ham tanlansa: False
```

# 85-Topshiriq: Null-coalescing zanjiri (Chaining ??)
## Topshiriq sharti:
Bir nechta o'zgaruvchilardan birinchi `null` bo'lmaganini olish uchun `??` zanjirini tuzing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        string? manba1 = null;
        string? manba2 = null;
        string? manba3 = "Zaxira Server";
        string? standart = "Mahalliy Fayl";

        string faolManba = manba1 ?? manba2 ?? manba3 ?? standart;
        Console.WriteLine($"Tanlangan manba: {faolManba}");
    }
}

```

## Tushuntirish va Mantiq:
`??` operatorlari ketma-ket zanjirlanishi mumkin. Ular chapdan o'ngga qarab birinchi `null` bo'lmagan qiymatni topadi va keyingi ifodalarni hisoblamasdan darhol qaytaradi.

## Ishlash natijasi:
```text
Tanlangan manba: Zaxira Server
```

# 86-Topshiriq: Null-conditional zanjiri va xavfsiz chaqiruvlar
## Topshiriq sharti:
Chuqur iyerarxiyadagi obyektlar xossalarini xavfsiz o'qish uchun `?.` zanjiridan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

class Kompaniya { public Bolim? AsosiyBolim { get; set; } }
class Bolim { public Menejer? Boshliq { get; set; } }
class Menejer { public string? Ism { get; set; } }

internal class Program
{
    static void Main()
    {
        Kompaniya? k = new Kompaniya();

        string? ism = k?.AsosiyBolim?.Boshliq?.Ism;
        Console.WriteLine($"Boshliq ismi: {(ism ?? "Tayinlanmagan")}");

        k.AsosiyBolim = new Bolim { Boshliq = new Menejer { Ism = "Sobir" } };
        ism = k?.AsosiyBolim?.Boshliq?.Ism;
        Console.WriteLine($"Boshliq ismi: {(ism ?? "Tayinlanmagan")}");
    }
}

```

## Tushuntirish va Mantiq:
Har qanday pog'onada `null` uchrasa, butun zanjir to'xtatilib `null` qaytariladi. Bu klassik 'NullReferenceException: Object reference not set to an instance of an object' xatosini butunlay yo'q qiladi.

## Ishlash natijasi:
```text
Boshliq ismi: Tayinlanmagan
Boshliq ismi: Sobir
```

# 87-Topshiriq: Null-coalescing bilan istisno otish: ?? throw
## Topshiriq sharti:
C# 7 da kiritilgan `throw` ifodasidan `??` bilan birgalikda argumentlarni tekshirishda foydalaning.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void TizimgaKirit(string? token)
    {
        string aniqToken = token ?? throw new ArgumentNullException(nameof(token), "Token bo'sh bo'lishi mumkin emas!");
        Console.WriteLine($"Token qabul qilindi: {aniqToken.Substring(0, 5)}...");
    }

    static void Main()
    {
        TizimgaKirit("SECRET_TOKEN_12345");

        try
        {
            TizimgaKirit(null);
        }
        catch (ArgumentNullException ex)
        {
            Console.WriteLine($"Istisno ushlandi: {ex.Message}");
        }
    }
}

```

## Tushuntirish va Mantiq:
C# 7 da `throw` faqat bayonot emas, balki ifoda (expression) sifatida ham tan olingan. Bu konstruktorlar va metodlarda `this.token = token ?? throw new ...` shaklida bitta qatorda himoya qilishga imkon beradi.

## Ishlash natijasi:
```text
Token qabul qilindi: SECRE...
Istisno ushlandi: Token bo'sh bo'lishi mumkin emas! (Parameter 'token')
```

# 88-Topshiriq: Shartli ifodalarda pattern matching va xossa filtri
## Topshiriq sharti:
`if` ichida ob'yekt xossasini tekshirib, uni darhol filtrlang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Tekshir(object obj)
    {
        if (obj is string { Length: > 5 } s)
        {
            Console.WriteLine($"5 dan uzun satr: '{s}'");
        }
        else
        {
            Console.WriteLine("Talabga javob bermaydi");
        }
    }

    static void Main()
    {
        Tekshir("Salom");
        Tekshir("O'zbekiston");
        Tekshir(1234567);
    }
}

```

## Tushuntirish va Mantiq:
`if (obj is string { Length: > 5 } s)` sintaksisi uchta amalni birlashtiradi: ob'yekt satr ekanligini, `null` emasligini va uning `Length` xossasi 5 dan kattaligini tekshirib, yangi `s` o'zgaruvchisiga o'zlashtiradi.

## Ishlash natijasi:
```text
Talabga javob bermaydi
5 dan uzun satr: 'O'zbekiston'
Talabga javob bermaydi
```

# 89-Topshiriq: Switch Expression orqali Enum xaritalash (Mapping)
## Topshiriq sharti:
Enum qiymatlarini foydalanuvchiga ko'rsatiladigan o'zbekcha matnga switch expression orqali xaritalang.

## Yechim (C# kodi):
```csharp
using System;

enum BuyurtmaHolati { Kutilmoqda, Tolandi, Yetkazilmoqda, Yakunlandi, BekorQilindi }

internal class Program
{
    static string HolatNomi(BuyurtmaHolati holat) => holat switch
    {
        BuyurtmaHolati.Kutilmoqda     => "To'lov kutilmoqda",
        BuyurtmaHolati.Tolandi        => "To'lov qabul qilindi",
        BuyurtmaHolati.Yetkazilmoqda  => "Yetkazib berilmoqda",
        BuyurtmaHolati.Yakunlandi     => "Buyurtma yetkazildi",
        BuyurtmaHolati.BekorQilindi   => "Buyurtma bekor qilindi",
        _ => throw new ArgumentOutOfRangeException(nameof(holat), "Bunday holat mavjud emas")
    };

    static void Main()
    {
        Console.WriteLine(HolatNomi(BuyurtmaHolati.Tolandi));
        Console.WriteLine(HolatNomi(BuyurtmaHolati.Yetkazilmoqda));
    }
}

```

## Tushuntirish va Mantiq:
Switch expression enumlarni DTO yoki View modellarga xaritalashda (mapping) eng toza va xatosiz usul hisoblanadi. Agar yangi enum qiymati qo'shilsa va u bu yerda qamrab olinmasa, kompilyator ogohlantirish (CS8509) beradi.

## Ishlash natijasi:
```text
To'lov qabul qilindi
Yetkazib berilmoqda
```

# 90-Topshiriq: Relational Pattern bilan baholash (Grade Calculator)
## Topshiriq sharti:
Talabaning 0 dan 100 gacha bo'lgan ballini an'anaviy 'A', 'B', 'C', 'F' baholariga relational pattern orqali aylantiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static char BallniBahola(int ball) => ball switch
    {
        >= 90 and <= 100 => 'A',
        >= 80 and < 90   => 'B',
        >= 70 and < 80   => 'C',
        >= 60 and < 70   => 'D',
        >= 0 and < 60    => 'F',
        _ => throw new ArgumentException("Ball 0 dan 100 gacha bo'lishi shart!")
    };

    static void Main()
    {
        Console.WriteLine($"95 ball: {BallniBahola(95)}");
        Console.WriteLine($"82 ball: {BallniBahola(82)}");
        Console.WriteLine($"58 ball: {BallniBahola(58)}");
    }
}

```

## Tushuntirish va Mantiq:
Relational va mantiqiy patternlar yordamida baholash chegaralari juda tushunarli va xatosiz yoziladi. Har bir oraliq aniq qamrab olingan.

## Ishlash natijasi:
```text
95 ball: A
82 ball: B
58 ball: F
```

# 91-Topshiriq: Property Pattern bilan chegirma hisoblash
## Topshiriq sharti:
Mijozning statusi, xarid summasi va a'zolik muddatiga qarab chegirma beruvchi biznes mantiqni tuzing.

## Yechim (C# kodi):
```csharp
using System;

class Buyurtma
{
    public decimal Summa { get; set; }
    public bool PremiumAzo { get; set; }
    public int XaridlarSoni { get; set; }
}

internal class Program
{
    static decimal ChegirmaFoizi(Buyurtma b) => b switch
    {
        { PremiumAzo: true, Summa: > 1_000_000m } => 0.20m, // 20%
        { PremiumAzo: true }                      => 0.10m, // 10%
        { XaridlarSoni: > 10, Summa: > 500_000m } => 0.08m, // 8%
        { Summa: > 500_000m }                     => 0.05m, // 5%
        _ => 0.0m
    };

    static void Main()
    {
        var b1 = new Buyurtma { PremiumAzo = true, Summa = 1_500_000m, XaridlarSoni = 5 };
        var b2 = new Buyurtma { PremiumAzo = false, Summa = 600_000m, XaridlarSoni = 12 };

        Console.WriteLine($"1-Buyurtma chegirmasi: {ChegirmaFoizi(b1):P0}");
        Console.WriteLine($"2-Buyurtma chegirmasi: {ChegirmaFoizi(b2):P0}");
    }
}

```

## Tushuntirish va Mantiq:
Property Pattern bir nechta xossalar kombinatsiyasini tekshirishni juda osonlashtiradi. Obyektning murakkab holatlari yuqoridan pastga qarab mos kelgan birinchi qoidada ushlanadi.

## Ishlash natijasi:
```text
1-Buyurtma chegirmasi: 20%
2-Buyurtma chegirmasi: 8%
```

# 92-Topshiriq: Tuple Pattern bilan Tosh-Qaychi-Qog'oz o'yini
## Topshiriq sharti:
Ikki o'yinchi harakatini Tuple Pattern yordamida solishtirib g'olibni aniqlang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static string Oyna(string p1, string p2) => (p1.ToLower(), p2.ToLower()) switch
    {
        ("tosh", "qaychi")  => "1-o'yinchi yutdi (Tosh qaychini sindiradi)",
        ("qaychi", "qogoz") => "1-o'yinchi yutdi (Qaychi qog'ozni kesadi)",
        ("qogoz", "tosh")   => "1-o'yinchi yutdi (Qog'oz toshni o'raydi)",
        (var a, var b) when a == b => "Durrang!",
        _ => "2-o'yinchi yutdi!"
    };

    static void Main()
    {
        Console.WriteLine(Oyna("Tosh", "Qaychi"));
        Console.WriteLine(Oyna("Qogoz", "Qogoz"));
        Console.WriteLine(Oyna("Tosh", "Qogoz"));
    }
}

```

## Tushuntirish va Mantiq:
Kortejlar yordamida ikkita parametr birlashtirilib, kombinatorik barcha variantlar qulay jadval ko'rinishida modellashtiriladi. Durrang holati `when a == b` orqali ushlanadi.

## Ishlash natijasi:
```text
1-o'yinchi yutdi (Tosh qaychini sindiradi)
Durrang!
2-o'yinchi yutdi!
```

# 93-Topshiriq: List Pattern bilan CLI buyruqlarini tahlil qilish (Parsing)
## Topshiriq sharti:
Terminaldan kiritilgan argumentlar massivini List Pattern yordamida tahlil qiling.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void BuyruqniBajar(string[] args)
    {
        string natija = args switch
        {
            ["start"] => "Tizim ishga tushirilmoqda...",
            ["stop", "--force"] => "Tizim majburiy to'xtatildi!",
            ["stop"] => "Tizim yumshoq to'xtatildi.",
            ["config", "set", var kalit, var qiymat] => $"Sozlama o'rnatildi: {kalit} = {qiymat}",
            _ => "Noma'lum buyruq! Yordam uchun 'help' deb yozing."
        };

        Console.WriteLine(natija);
    }

    static void Main()
    {
        BuyruqniBajar(new[] { "start" });
        BuyruqniBajar(new[] { "stop", "--force" });
        BuyruqniBajar(new[] { "config", "set", "port", "8080" });
    }
}

```

## Tushuntirish va Mantiq:
List Pattern yordamida buyruqlar satri argumentlarini (CLI parser) yozish juda osonlashdi. Har xil uzunlikdagi argumentlar va ularning ichki qiymatlari bir zumda o'zgaruvchilarga ajratiladi.

## Ishlash natijasi:
```text
Tizim ishga tushirilmoqda...
Tizim majburiy to'xtatildi!
Sozlama o'rnatildi: port = 8080
```

# 94-Topshiriq: Nullable qiymat turlarida mantiqiy taqqoslashlar (Lifting)
## Topshiriq sharti:
`int?` kabi nullable turlar taqqoslanganda C# ning maxsus qoidalarini (Lifted operators) ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int? a = null;
        int? b = 10;
        int? c = null;

        Console.WriteLine($"null == null: {a == c}"); // True
        Console.WriteLine($"null == 10:   {a == b}"); // False
        Console.WriteLine($"null > 10:    {a > b}");  // Har doim False
        Console.WriteLine($"null < 10:    {a < b}");  // Har doim False
    }
}

```

## Tushuntirish va Mantiq:
C# da solishtirish operatorlari nullable turlar uchun avtomatik 'ko'tariladi' (lifted). Tenglikda ikkita `null` o'zaro teng. Ammo `<, >, <=, >=` amallarida agar operandlardan biri `null` bo'lsa, natija har doim `false` bo'ladi.

## Ishlash natijasi:
```text
null == null: True
null == 10:   False
null > 10:    False
null < 10:    False
```

# 95-Topshiriq: is operatori vs as operatori farqlari
## Topshiriq sharti:
Tipni xavfsiz o'zgartirishda `is` (Pattern Matching) va `as` (kasting) operatorlari o'rtasidagi farqni solishtiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        object obj = "O'zbekiston";

        // 'as' operatori faqat Reference yoki Nullable turlarda ishlaydi
        string? strAs = obj as string;
        Console.WriteLine($"'as' natijasi: {strAs}");

        // 'is' pattern matching Value Type larda ham bemalol ishlaydi
        object sonObj = 42;
        if (sonObj is int son)
        {
            Console.WriteLine($"'is' orqali olingan son: {son}");
        }

        // sonObj as int; // KOMPILYATSIYA XATOSI! int nullable emas
    }
}

```

## Tushuntirish va Mantiq:
`as` operatori faqat havola turlarida ishlaydi va o'xshamasa `null` qaytaradi (istisno otmaydi). `is` esa ancha qudratli bo'lib, ham havola, ham qiymat (ValueType) turlarida ishlaydi va `null` tekshiruvini ham o'z ichiga oladi.

## Ishlash natijasi:
```text
'as' natijasi: O'zbekiston
'is' orqali olingan son: 42
```

# 96-Topshiriq: Switch Expression da to'liq qamrab olish (Exhaustiveness)
## Topshiriq sharti:
Barcha mumkin bo'lgan holatlar qamrab olinishi shartligi va diskard (`_`) ning roli.

## Yechim (C# kodi):
```csharp
using System;

enum Chiroq { Qizil, Sariq, Yashil }

internal class Program
{
    static string ChiroqHarakati(Chiroq rang) => rang switch
    {
        Chiroq.Qizil  => "To'xtang!",
        Chiroq.Sariq  => "Tayyorlaning!",
        Chiroq.Yashil => "Harakatlaning!"
        // Agar birorta rang qolib ketsa yoki _ bo'lmasa, kompilyator ogohlantirish beradi
    };

    static void Main()
    {
        Console.WriteLine(ChiroqHarakati(Chiroq.Qizil));
        Console.WriteLine(ChiroqHarakati(Chiroq.Yashil));
    }
}

```

## Tushuntirish va Mantiq:
Switch Expression to'liq qamrovli (exhaustive) bo'lishi shart. Agar tekshirilmagan holat yuzaga kelsa va u qamrab olinmagan bo'lsa, runtime da `SwitchExpressionException` tashlanadi.

## Ishlash natijasi:
```text
To'xtang!
Harakatlaning!
```

# 97-Topshiriq: Murakkab Holat Mashinasi (State Machine) switch yordamida
## Topshiriq sharti:
E-tijorat buyurtmasining holatlarini boshqaruvchi State Machine o'tishlarini Tuple Pattern orqali yarating.

## Yechim (C# kodi):
```csharp
using System;

enum Holat { Yangi, Tolangan, Jonatilgan, Yetkazilgan, BekorQilingan }
enum Amal { Tolash, Jonatish, Topshirish, BekorQilish }

internal class Program
{
    static Holat KeyingiHolat(Holat joriy, Amal amal) => (joriy, amal) switch
    {
        (Holat.Yangi, Amal.Tolash)           => Holat.Tolangan,
        (Holat.Yangi, Amal.BekorQilish)      => Holat.BekorQilingan,
        (Holat.Tolangan, Amal.Jonatish)      => Holat.Jonatilgan,
        (Holat.Tolangan, Amal.BekorQilish)   => Holat.BekorQilingan,
        (Holat.Jonatilgan, Amal.Topshirish)  => Holat.Yetkazilgan,
        _ => throw new InvalidOperationException($"{joriy} holatida {amal} amalini bajarib bo'lmaydi!")
    };

    static void Main()
    {
        Holat holat = Holat.Yangi;
        Console.WriteLine($"Boshlang'ich holat: {holat}");

        holat = KeyingiHolat(holat, Amal.Tolash);
        Console.WriteLine($"To'lovdan keyin: {holat}");

        holat = KeyingiHolat(holat, Amal.Jonatish);
        Console.WriteLine($"Jo'natilgandan keyin: {holat}");
    }
}

```

## Tushuntirish va Mantiq:
Holat mashinalari dasturiy ta'minot arxitekturasida juda muhim. `(joriyHolat, amal) switch` konstruktsiyasi o'tishlar jadvalini nihoyatda qisqa va qat'iy nazorat ostida ifodalash imkonini beradi.

## Ishlash natijasi:
```text
Boshlang'ich holat: Yangi
To'lovdan keyin: Tolangan
Jo'natilgandan keyin: Jonatilgan
```

# 98-Topshiriq: Qisqa tutashuv va xotira samaradorligi
## Topshiriq sharti:
Katta hisoblash xarajatlariga ega funksiyalarni `&&` orqali faqat zarur bo'lganda chaqirish amaliyoti.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static bool KattaBazadanQidir(int id)
    {
        Console.WriteLine($"Bazaga og'ir so'rov ketdi: ID={id}");
        return id == 100;
    }

    static void Main()
    {
        bool keshdaBor = true;
        int id = 100;

        // keshdaBor rost bo'lgani uchun o'ng tarafdagi og'ir funksiya chaqirilmaydi
        if (keshdaBor || KattaBazadanQidir(id))
        {
            Console.WriteLine("Ma'lumot topildi (Bazaga kirmasdan)!");
        }
    }
}

```

## Tushuntirish va Mantiq:
Mantiqiy ifodalarni to'g'ri tartibda joylashtirish (masalan arzon amallarni chapga, qimmat I/O yoki baza amallarini o'ngga qo'yish) qisqa tutashuv tufayli tizim unumdorligini bir necha barobar oshiradi.

## Ishlash natijasi:
```text
Ma'lumot topildi (Bazaga kirmasdan)!
```

# 99-Topshiriq: Pattern Matching da o'zgaruvchilar ko'rinish sohasi (Scope)
## Topshiriq sharti:
`if (obj is Tur x)` orqali yaratilgan o'zgaruvchining qayerda amal qilishini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        object obj = "O'zbekiston yoshlari";

        if (obj is string matn && matn.Length > 0)
        {
            // 'matn' o'zgaruvchisi if bloki ichida mavjud
            Console.WriteLine($"Matn mavjud: {matn}");
        }

        // if dan tashqarida ham 'matn' o'zgaruvchisi ko'rinishi mumkin (definite assignment qoidasi)
    }
}

```

## Tushuntirish va Mantiq:
Pattern matching da yaratilgan o'zgaruvchi uni o'rab turgan blok doirasiga kiradi. Biroq C# kompilyatori unga qiymat aniq biriktirilgan (definitely assigned) bo'lsagina undan foydalanishga ruxsat beradi.

## Ishlash natijasi:
```text
Matn mavjud: O'zbekiston yoshlari
```

# 100-Topshiriq: Ko'p pog'onali Pattern Matching bilan to'liq avtorizatsiya filtri
## Topshiriq sharti:
Foydalanuvchi obyekti, roli va huquqlarini bitta kompleks pattern orqali tekshirish.

## Yechim (C# kodi):
```csharp
using System;

record Foydalanuvchi(string Ism, string Rol, bool Bloklangan, int RuxsatDarajasi);

internal class Program
{
    static string KirishniTekshir(Foydalanuvchi? user) => user switch
    {
        null => "Foydalanuvchi aniqlanmadi (null)",
        { Bloklangan: true } => "Foydalanuvchi bloklangan!",
        { Rol: "Admin" } => "To'liq admin paneli ochildi",
        { Rol: "Moderator", RuxsatDarajasi: >= 5 } => "Moderator amallari ruxsat etildi",
        { Rol: "Foydalanuvchi", RuxsatDarajasi: > 0 } => "Oddiy foydalanuvchi kabineti",
        _ => "Kirish cheklandi"
    };

    static void Main()
    {
        var u1 = new Foydalanuvchi("Ali", "Admin", false, 10);
        var u2 = new Foydalanuvchi("Vali", "Foydalanuvchi", true, 2);
        var u3 = new Foydalanuvchi("Sami", "Moderator", false, 7);

        Console.WriteLine($"{u1.Ism}: {KirishniTekshir(u1)}");
        Console.WriteLine($"{u2.Ism}: {KirishniTekshir(u2)}");
        Console.WriteLine($"{u3.Ism}: {KirishniTekshir(u3)}");
    }
}

```

## Tushuntirish va Mantiq:
Zamonaviy C# da bunday murakkab biznes tekshiruvlarini ko'p qatorli `if-else` larsiz, yagona va o'qilishi juda oson bo'lgan Switch Expression orqali modellashtirish eng to'g'ri amaliyot (best practice) hisoblanadi.

## Ishlash natijasi:
```text
Ali: To'liq admin paneli ochildi
Vali: Foydalanuvchi bloklangan!
Sami: Moderator amallari ruxsat etildi
```

