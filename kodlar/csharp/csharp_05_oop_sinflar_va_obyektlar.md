# 5-Mavzu: Obyektga Yo'naltirilgan Dasturlash (OOP) - Sinflar va Obyektlar (201-250)

Ushbu bo'limda C# tilida OOP ning fundamental tamoyillari va sinf arxitekturasi: sinf va obyekt tushunchalari, kirish modifikatorlari (`public`, `private`, `protected`, `internal`), to'liq va avtomatik xossalar, `init`-only setters, C# 11 `required` xossalar, konstruktorlar va konstruktorlar zanjiri (`this`), C# 12 Primary Constructors, statik a'zolar, statik konstruktor va statik sinflar, indeksatorlar (`this[...]`), qisman sinflar (`partial`), destruktorlar, CLR xotira modeli (Type Handle, Sync Block Index) hamda mashhur loyihalash naqshlari bo'yicha 50 ta chuqur amaliy topshiriq keltirilgan.

# 201-Topshiriq: Sinf (class) e'lon qilish va instansiya (obyekt) yaratish
## Topshiriq sharti:
`Avtomobil` sinfini yarating, uning maydonlarini belgilang va `new` orqali yangi obyekt hosil qiling.

## Yechim (C# kodi):
```csharp
using System;

class Avtomobil
{
    public string Model = "";
    public int Yil;
    public double Tezlik;
}

internal class Program
{
    static void Main()
    {
        // Obyekt yaratish (Instansiyalash)
        Avtomobil avto = new Avtomobil();
        avto.Model = "Chevrolet Gentra";
        avto.Yil = 2024;
        avto.Tezlik = 180.5;

        Console.WriteLine($"Model: {avto.Model}, Ishlab chiqarilgan yili: {avto.Yil}, Tezlik: {avto.Tezlik} km/soat");
    }
}

```

## Tushuntirish va Mantiq:
Sinf bu shablon (chizma), obyekt esa ushbu shablon asosida Heap xotirada ajratilgan real nusxadir. `avto` o'zgaruvchisi Stack da saqlanadi va Heap dagi `Avtomobil` obyekti xotira manziliga havola ko'rsatadi.

## Ishlash natijasi:
```text
Model: Chevrolet Gentra, Ishlab chiqarilgan yili: 2024, Tezlik: 180.5 km/soat
```

# 202-Topshiriq: Kirish modifikatorlari: public vs private va ma'lumotlarni himoyalash
## Topshiriq sharti:
`private` maydonlarni yashirish va ularga faqat ochiq (`public`) metodlar orqali xavfsiz murojaat qilishni ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

class BankHisobi
{
    private decimal balans; // Tashqaridan to'g'ridan-to'g'ri o'zgartirib bo'lmaydi

    public void Depozit(decimal summa)
    {
        if (summa > 0)
        {
            balans += summa;
            Console.WriteLine($"{summa:N0} so'm qabul qilindi.");
        }
    }

    public decimal BalansniKorish() => balans;
}

internal class Program
{
    static void Main()
    {
        var hisob = new BankHisobi();
        hisob.Depozit(500000);
        // hisob.balans = 1000000000; // KOMPILYATSIYA XATOSI! private maydon

        Console.WriteLine($"Joriy balans: {hisob.BalansniKorish():N0} so'm");
    }
}

```

## Tushuntirish va Mantiq:
Inkapsulyatsiya (Encapsulation) ma'lumotlarni ruxsatsiz o'zgartirishlardan himoya qiladi. `private` modifikatori maydonni faqat o'sha sinf ichida ko'rinadigan qiladi, tashqi dunyo bilan esa tekshirilgan `public` metodlar orqali muloqot qilinadi.

## Ishlash natijasi:
```text
500,000 so'm qabul qilindi.
Joriy balans: 500,000 so'm
```

# 203-Topshiriq: To'liq xossalar (Full Properties) va Backing Field
## Topshiriq sharti:
Xossaning `get` va `set` bloklarida qiymatni tekshiruvchi (validatsiya) klassik to'liq xossani yozing.

## Yechim (C# kodi):
```csharp
using System;

class Foydalanuvchi
{
    private int yosh; // Backing field

    public int Yosh
    {
        get => yosh;
        set
        {
            if (value < 0 || value > 120)
                throw new ArgumentException("Yosh 0 dan 120 gacha bo'lishi shart!");
            yosh = value;
        }
    }
}

internal class Program
{
    static void Main()
    {
        var f = new Foydalanuvchi();
        f.Yosh = 25; // 'set' bloki ishga tushadi, value = 25
        Console.WriteLine($"Foydalanuvchi yoshi: {f.Yosh}"); // 'get' bloki ishga tushadi

        try
        {
            f.Yosh = -5;
        }
        catch (ArgumentException ex)
        {
            Console.WriteLine($"Validatsiya xatosi: {ex.Message}");
        }
    }
}

```

## Tushuntirish va Mantiq:
Xossalar (Properties) maydon kabi sintaksis taqdim etadi, ammo orqada aslida `get_Yosh()` va `set_Yosh(int value)` metodlari sifatida ishlaydi. Bu orqali maydonga yozilayotgan har qanday qiymat nazoratdan o'tkaziladi.

## Ishlash natijasi:
```text
Foydalanuvchi yoshi: 25
Validatsiya xatosi: Yosh 0 dan 120 gacha bo'lishi shart!
```

# 204-Topshiriq: Avtomatik xossalar (Auto-Implemented Properties)
## Topshiriq sharti:
Qo'shimcha tekshiruv talab qilinmaydigan holatlar uchun qisqa avtomatik xossalardan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

class Kitob
{
    public string Sarlavha { get; set; } = "Noma'lum";
    public string Muallif { get; set; } = "Noma'lum";
    public decimal Narx { get; set; }
}

internal class Program
{
    static void Main()
    {
        var k = new Kitob
        {
            Sarlavha = "O'tkan Kunlar",
            Muallif = "Abdulla Qodiriy",
            Narx = 65000m
        };

        Console.WriteLine($"Kitob: '{k.Sarlavha}', Muallif: {k.Muallif}, Narxi: {k.Narx:N0} so'm");
    }
}

```

## Tushuntirish va Mantiq:
Auto-property e'lon qilinganda C# kompilyatori uning orqasida ko'rinmas shaxsiy maydon (hidden backing field) yaratadi va get/set larni unga ulaydi. Bu kodni ixcham va toza qiladi.

## Ishlash natijasi:
```text
Kitob: 'O'tkan Kunlar', Muallif: Abdulla Qodiriy, Narxi: 65,000 so'm
```

# 205-Topshiriq: C# 9 init-only setterlar: Obyekt yaratilgandan keyin o'zgarmaslik
## Topshiriq sharti:
Obyekt initsializatorida qiymat berishga ruxsat etuvchi, lekin keyinchalik o'zgartirishni taqiqlovchi `init` modifikatorini qo'llang.

## Yechim (C# kodi):
```csharp
using System;

class Tranzaksiya
{
    public Guid Id { get; init; } = Guid.NewGuid();
    public decimal Summa { get; init; }
    public DateTime Vaqt { get; init; } = DateTime.UtcNow;
}

internal class Program
{
    static void Main()
    {
        var t = new Tranzaksiya
        {
            Summa = 150000m // Obyekt yaratilishida qiymat berish mumkin
        };

        Console.WriteLine($"Tranzaksiya ID: {t.Id}");
        Console.WriteLine($"Summa: {t.Summa} so'm");

        // t.Summa = 200000m; // KOMPILYATSIYA XATOSI! init faqat yaratilish vaqtida ishlaydi
    }
}

```

## Tushuntirish va Mantiq:
`init` aktsessori C# 9 da kiritilgan bo'lib, xossani faqat konstruktor yoki obyekt initsializatori (`{ ... }`) orqali to'ldirishga imkon beradi. Shundan so'ng obyekt xossasi o'zgarmas (immutable) bo'lib qoladi.

## Ishlash natijasi:
```text
Tranzaksiya ID: ...
Summa: 150000 so'm
```

# 206-Topshiriq: C# 11 required xossalari: Majburiy initsializatsiya
## Topshiriq sharti:
C# 11 da kiritilgan `required` modifikatori yordamida obyekt yaratilayotganda kiritilishi shart bo'lgan xossalarni belgilang.

## Yechim (C# kodi):
```csharp
using System;

class Xodim
{
    public required string Ism { get; set; }
    public required string Lavozim { get; set; }
    public decimal Maosh { get; set; } = 3000000m;
}

internal class Program
{
    static void Main()
    {
        // To'g'ri initsializatsiya
        var x = new Xodim
        {
            Ism = "Sherzod",
            Lavozim = "Bosh Muhandis"
        };

        Console.WriteLine($"Xodim: {x.Ism}, Lavozim: {x.Lavozim}, Maosh: {x.Maosh:N0}");

        // var xato = new Xodim(); // KOMPILYATSIYA XATOSI! 'Ism' va 'Lavozim' kiritilishi shart!
    }
}

```

## Tushuntirish va Mantiq:
`required` kalit so'zi kompilyatorni obyekt initsializatorida ushbu xossalarga qiymat berilganligini tekshirishga majburlaydi. Bu orqali konstruktorlar ko'payib ketishining oldi olinadi va `null` bo'lish xavfi yo'qotiladi.

## Ishlash natijasi:
```text
Xodim: Sherzod, Lavozim: Bosh Muhandis, Maosh: 3,000,000
```

# 207-Topshiriq: Target-typed new: Zamonaviy qisqa new() sintaksisi
## Topshiriq sharti:
C# 9 ning tur aniq ma'lum bo'lganda sinf nomini takrorlamasdan `new()` yozish imkoniyatidan foydalaning.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

class Mahsulot
{
    public string Nomi { get; set; } = "";
    public Mahsulot(string nomi) => Nomi = nomi;
}

internal class Program
{
    static void Main()
    {
        // Eski usul: Mahsulot m = new Mahsulot("Laptop");
        // Yangi target-typed new:
        Mahsulot m = new("Laptop Pro");

        List<Mahsulot> ombor = new()
        {
            new("Smartfon"),
            new("Planshet")
        };

        Console.WriteLine($"Asosiy mahsulot: {m.Nomi}");
        Console.WriteLine($"Ombordagi mahsulotlar soni: {ombor.Count}");
    }
}

```

## Tushuntirish va Mantiq:
Target-typed `new(...)` o'zgaruvchi turi chap tomonda aniq ko'rsatilgan bo'lsa, o'ng tomonda sinf nomini qayta yozish majburiyatini bekor qiladi. Bu kodni juda qisqa va chiroyli qiladi.

## Ishlash natijasi:
```text
Asosiy mahsulot: Laptop Pro
Ombordagi mahsulotlar soni: 2
```

# 208-Topshiriq: Parametrli konstruktorlar va holatni to'ldirish
## Topshiriq sharti:
Obyekt yaratilish paytidayoq uning barcha kerakli parametrlarini qabul qiluvchi konstruktor yozing.

## Yechim (C# kodi):
```csharp
using System;

class Talaba
{
    public string Ism { get; }
    public int Kurs { get; }

    // Parametrli konstruktor
    public Talaba(string ism, int kurs)
    {
        Ism = ism;
        Kurs = kurs;
    }
}

internal class Program
{
    static void Main()
    {
        Talaba t = new Talaba("Javohir", 3);
        Console.WriteLine($"Talaba: {t.Ism}, Kursi: {t.Kurs}");
    }
}

```

## Tushuntirish va Mantiq:
Agar sinfda birorta parametrli konstruktor yozilsa, C# kompilyatori standart parametrsiz konstruktorni (`new Talaba()`) avtomatik yaratishni to'xtatadi. Bu orqali chala yoki noto'g'ri initsializatsiya qilingan obyektlar paydo bo'lishining oldi olinadi.

## Ishlash natijasi:
```text
Talaba: Javohir, Kursi: 3
```

# 209-Topshiriq: Konstruktorlarni zanjirlash (Constructor Chaining: this(...))
## Topshiriq sharti:
`this(...)` yordamida bitta konstruktordan boshqa konstruktorni chaqirib kod takrorlanishini yo'qoting.

## Yechim (C# kodi):
```csharp
using System;

class ServerKonfig
{
    public string Host { get; }
    public int Port { get; }
    public bool Ssl { get; }

    public ServerKonfig() : this("localhost", 8080, false) { }

    public ServerKonfig(string host, int port) : this(host, port, true) { }

    public ServerKonfig(string host, int port, bool ssl)
    {
        Host = host;
        Port = port;
        Ssl = ssl;
    }
}

internal class Program
{
    static void Main()
    {
        var s1 = new ServerKonfig();
        var s2 = new ServerKonfig("api.uz", 443);

        Console.WriteLine($"s1: {s1.Host}:{s1.Port}, SSL={s1.Ssl}");
        Console.WriteLine($"s2: {s2.Host}:{s2.Port}, SSL={s2.Ssl}");
    }
}

```

## Tushuntirish va Mantiq:
`this(argumentlar)` zanjiri bitta asosiy konstruktorga barcha yukni yuklab, qolgan qisqa konstruktorlarni unga yo'naltirish imkonini beradi. Natijada initsializatsiya mantiqi faqat bitta joyda yoziladi (DRY tamoyili).

## Ishlash natijasi:
```text
s1: localhost:8080, SSL=False
s2: api.uz:443, SSL=True
```

# 210-Topshiriq: C# 12 Primary Constructors sinflarda
## Topshiriq sharti:
C# 12 da sinf sarlavhasida to'g'ridan-to'g'ri Primary Constructor e'lon qiling va uning parametrlaridan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

// C# 12 Primary Constructor
class Dasturchi(string ism, string asosiyTil, int tajriba)
{
    public string Ism => ism;
    public string AsosiyTil => asosiyTil;

    public void Malumot()
    {
        Console.WriteLine($"{ism} ({asosiyTil} dasturchisi), Tajriba: {tajriba} yil");
    }
}

internal class Program
{
    static void Main()
    {
        var dev = new Dasturchi("Mirshod", "C# / .NET", 4);
        dev.Malumot();
    }
}

```

## Tushuntirish va Mantiq:
C# 12 da sinflar uchun kiritilgan Primary Constructors konstruktor yozish zaruratini butunlay yo'qotdi. Qavs ichidagi parametrlar butun sinf tanasida (metodlar va xossalarda) to'g'ridan-to'g'ri o'zgaruvchi sifatida ko'rinadi.

## Ishlash natijasi:
```text
Mirshod (C# / .NET dasturchisi), Tajriba: 4 yil
```

# 211-Topshiriq: Statik maydonlar: Barcha obyektlar uchun yagona umumiy xotira
## Topshiriq sharti:
`static` maydondan foydalanib sinfdan jami nechta obyekt yaratilganini hisoblovchi dastur tuzing.

## Yechim (C# kodi):
```csharp
using System;

class Hisoblagich
{
    public static int YaratilganSoni = 0; // Barcha obyektlar uchun bitta

    public Hisoblagich()
    {
        YaratilganSoni++;
    }
}

internal class Program
{
    static void Main()
    {
        new Hisoblagich();
        new Hisoblagich();
        new Hisoblagich();

        Console.WriteLine($"Jami yaratilgan obyektlar soni: {Hisoblagich.YaratilganSoni}");
    }
}

```

## Tushuntirish va Mantiq:
Statik maydonlar bitta obyektga emas, balki butun sinf turiga (Type object) tegishli bo'ladi. Ular CLR ning High Frequency Heap hududida turadi va har bir yangi obyekt yaratilganda qayta ajratilmaydi.

## Ishlash natijasi:
```text
Jami yaratilgan obyektlar soni: 3
```

# 212-Topshiriq: Statik metodlar va yordamchi funksiyalar
## Topshiriq sharti:
Obyekt instansiyasini talab qilmaydigan statik hisoblash metodlarini yozing.

## Yechim (C# kodi):
```csharp
using System;

class MatematikaYordamchi
{
    public static double GradusdanRadianga(double gradus) => gradus * Math.PI / 180.0;
    public static double RadiandanGradusga(double radian) => radian * 180.0 / Math.PI;
}

internal class Program
{
    static void Main()
    {
        double rad = MatematikaYordamchi.GradusdanRadianga(180.0);
        Console.WriteLine($"180 gradus: {rad:F4} radian (Pi)");
    }
}

```

## Tushuntirish va Mantiq:
Statik metodlar chaqirilganda ularga `this` ko'rsatkichi uzatilmaydi. Ular to'g'ridan-to'g'ri sinf nomi orqali chaqiriladi va instansiyaga bog'liq bo'lmagan mustaqil vazifalarni bajarish uchun juda mos keladi.

## Ishlash natijasi:
```text
180 gradus: 3.1416 radian (Pi)
```

# 213-Topshiriq: Statik konstruktor (static Constructor) va thread-safety
## Topshiriq sharti:
Sinfning birinchi marta ishlatilishida avtomatik ishga tushuvchi `static` konstruktorni namoyish eting.

## Yechim (C# kodi):
```csharp
using System;

class KattaLugat
{
    public static readonly DateTime YuklanganVaqt;

    // Statik konstruktor - parametrlarsiz va modifikatorsiz bo'ladi
    static KattaLugat()
    {
        YuklanganVaqt = DateTime.Now;
        Console.WriteLine(">> KattaLugat statik konstruktori bir marta bajarildi!");
    }

    public static void Salom() => Console.WriteLine("Lug'at tayyor.");
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Dastur boshlandi");
        KattaLugat.Salom(); // Bu yerda statik konstruktor 1 marta ishlaydi
        KattaLugat.Salom(); // 2-marta chaqirilganda qayta ishlamaydi
    }
}

```

## Tushuntirish va Mantiq:
Statik konstruktorni CLR sinfga birinchi marta murojaat qilinganda o'zi avtomatik chaqiradi. CLR uning oqimlararo mutlaqo xavfsiz (thread-safe) va dastur ishlashi davomida faqat bir marta bajarilishini kafolatlaydi.

## Ishlash natijasi:
```text
Dastur boshlandi
>> KattaLugat statik konstruktori bir marta bajarildi!
Lug'at tayyor.
Lug'at tayyor.
```

# 214-Topshiriq: Statik sinflar (static class) xususiyatlari
## Topshiriq sharti:
Instansiyasi olinmaydigan va meros berilmaydigan to'liq `static class` e'lon qiling.

## Yechim (C# kodi):
```csharp
using System;

static class Konverter
{
    public static double KmToMil(double km) => km * 0.621371;
    public static double MilToKm(double mil) => mil / 0.621371;
}

internal class Program
{
    static void Main()
    {
        // new Konverter(); // XATO! Statik sinflardan obyekt olib bo'lmaydi
        Console.WriteLine($"100 km: {Konverter.KmToMil(100):F2} mil");
    }
}

```

## Tushuntirish va Mantiq:
`static class` faqat statik a'zolardan iborat bo'lishi shart. Kompilyator darajasida u avtomatik `abstract sealed` qilib belgilanadi, ya'ni undan obyekt ham yaratib bo'lmaydi, undan meros ham olib bo'lmaydi.

## Ishlash natijasi:
```text
100 km: 62.14 mil
```

# 215-Topshiriq: this kalit so'zi: Disambiguation va o'zini uzatish
## Topshiriq sharti:
`this` yordamida parametr nomi bilan maydon nomi bir xil bo'lganda chalkashlikni yeching va joriy instansiyani tashqi metodga uzating.

## Yechim (C# kodi):
```csharp
using System;

class Xizmat;

class Buyurtma
{
    private string kod;

    public Buyurtma(string kod)
    {
        this.kod = kod; // 'this.kod' sinf maydoni, 'kod' esa parametr
    }

    public void ChopEt()
    {
        ChopEtuvchi.ChopQil(this); // O'zini argument sifatida uzatish
    }

    public string Kod => kod;
}

class ChopEtuvchi
{
    public static void ChopQil(Buyurtma b) => Console.WriteLine($"Buyurtma kodi: {b.Kod}");
}

internal class Program
{
    static void Main()
    {
        var b = new Buyurtma("ORD-999");
        b.ChopEt();
    }
}

```

## Tushuntirish va Mantiq:
`this` joriy sinf obyektining xotiradagi instansiyasiga ishora qiluvchi yashirin ko'rsatkichdir. U nomlar to'qnashuvida qaysi biri maydon ekanligini aniq ajratib beradi.

## Ishlash natijasi:
```text
Buyurtma kodi: ORD-999
```

# 216-Topshiriq: Indeksatorlar (Indexers): Obyektga massiv kabi murojaat qilish
## Topshiriq sharti:
Sinf ichida `this[int index]` indeksatorini e'lon qilib, ob'yektga kvadrat qavslar orqali murojaat qilishni yo'lga qo'ying.

## Yechim (C# kodi):
```csharp
using System;

class Jamoa
{
    private string[] azolar = new string[3];

    public string this[int indeks]
    {
        get => azolar[indeks];
        set => azolar[indeks] = value;
    }
}

internal class Program
{
    static void Main()
    {
        var j = new Jamoa();
        j[0] = "Botir";
        j[1] = "Komil";
        j[2] = "Laziz";

        Console.WriteLine($"Jamoaning 0-a'zosi: {j[0]}");
        Console.WriteLine($"Jamoaning 1-a'zosi: {j[1]}");
    }
}

```

## Tushuntirish va Mantiq:
Indeksatorlar sinf ob'yektlarini xuddi massiv yoki lug'at kabi kvadrat qavslar `obj[i]` bilan ishlatish imkonini beradi. Kompilyator ularni orqada `get_Item(int)` va `set_Item(int, value)` metodlariga aylantiradi.

## Ishlash natijasi:
```text
Jamoaning 0-a'zosi: Botir
Jamoaning 1-a'zosi: Komil
```

# 217-Topshiriq: Satrli indeksator: Lug'at kabi ishlovchi sinf
## Topshiriq sharti:
`this[string key]` indeksatori yordamida kalit so'z orqali qiymatlarni saqlovchi kesh sinfini yozing.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

class Kesh
{
    private Dictionary<string, string> xotira = new();

    public string this[string kalit]
    {
        get => xotira.TryGetValue(kalit, out var qiymat) ? qiymat : "Topilmadi";
        set => xotira[kalit] = value;
    }
}

internal class Program
{
    static void Main()
    {
        var k = new Kesh();
        k["user_1"] = "Farhod";
        k["user_2"] = "Kamola";

        Console.WriteLine($"user_1: {k["user_1"]}");
        Console.WriteLine($"user_99: {k["user_99"]}");
    }
}

```

## Tushuntirish va Mantiq:
Indeksatorlar faqat butun sonli bo'lishi shart emas. Kalit sifatida `string`, `Guid` yoki boshqa ixtiyoriy tur qabul qilinishi va qayta yuklanishi (overloaded) mumkin.

## Ishlash natijasi:
```text
user_1: Farhod
user_99: Topilmadi
```

# 218-Topshiriq: Qisman sinflar (Partial Classes): Kodni bo'laklash
## Topshiriq sharti:
`partial class` kalit so'zi bilan bitta sinfni ikkita alohida mantiqiy blokda yozing.

## Yechim (C# kodi):
```csharp
using System;

// 1-Faylda yoki qismda
partial class FoydalanuvchiXizmati
{
    public void Kirish() => Console.WriteLine("Foydalanuvchi tizimga kirdi.");
}

// 2-Faylda yoki qismda
partial class FoydalanuvchiXizmati
{
    public void Chiqish() => Console.WriteLine("Foydalanuvchi tizimdan chiqdi.");
}

internal class Program
{
    static void Main()
    {
        var xizmat = new FoydalanuvchiXizmati();
        xizmat.Kirish();
        xizmat.Chiqish();
    }
}

```

## Tushuntirish va Mantiq:
`partial class` bitta sinf ta'rifini bir nechta jismoniy fayllarga bo'lib yozishga imkon beradi. Kompilyatsiya vaqtida C# kompilyatori barcha qismlarni birlashtirib, bitta yaxlit sinf hosil qiladi.

## Ishlash natijasi:
```text
Foydalanuvchi tizimga kirdi.
Foydalanuvchi tizimdan chiqdi.
```

# 219-Topshiriq: Qisman metodlar (Partial Methods) va Source Generatorlar
## Topshiriq sharti:
`partial` metod e'lon qiling va uning implementatsiyasini alohida qismda yozing.

## Yechim (C# kodi):
```csharp
using System;

partial class BuyurtmaBoshqaruvchi
{
    // E'lon qilish
    partial void LogYoz(string matn);

    public void Yarat()
    {
        Console.WriteLine("Buyurtma yaratildi.");
        LogYoz("Buyurtma yaratilgani haqida bildirishnoma.");
    }
}

partial class BuyurtmaBoshqaruvchi
{
    // Implementatsiya
    partial void LogYoz(string matn)
    {
        Console.WriteLine($"[LOG]: {matn}");
    }
}

internal class Program
{
    static void Main()
    {
        var b = new BuyurtmaBoshqaruvchi();
        b.Yarat();
    }
}

```

## Tushuntirish va Mantiq:
Qisman metodlar Source Generatorlar va avtomatik kod ishlab chiqaruvchi vositalar uchun juda muhimdir. Agar qisman metod amalga oshirilmasa (tanasi yozilmasa), kompilyator uning chaqiruvlarini kutilmagan xarajatlarsiz olib tashlaydi.

## Ishlash natijasi:
```text
Buyurtma yaratildi.
[LOG]: Buyurtma yaratilgani haqida bildirishnoma.
```

# 220-Topshiriq: Destruktor / Finalizator (~SinfNomi) va CLR tozalash mexanizmi
## Topshiriq sharti:
Obyekt Garbage Collector tomonidan yo'q qilinayotganda chaqiriladigan destruktor yozing.

## Yechim (C# kodi):
```csharp
using System;

class XotiraResursi
{
    public string Nomi;

    public XotiraResursi(string nomi) => Nomi = nomi;

    // Destruktor (Finalizer)
    ~XotiraResursi()
    {
        Console.WriteLine($"Destruktor chaqirildi: {Nomi} xotiradan tozalandi.");
    }
}

internal class Program
{
    static void ResursYarat()
    {
        var r = new XotiraResursi("Vaqtinchalik Fayl");
    }

    static void Main()
    {
        ResursYarat();

        // GC ni majburiy chaqirish (O'quv maqsadida)
        GC.Collect();
        GC.WaitForPendingFinalizers();

        Console.WriteLine("Main yakunlandi.");
    }
}

```

## Tushuntirish va Mantiq:
Destruktor (`~ClassName`) C# da `Finalize()` metodiga aylanadi. Obyekt xotiradan o'chirilishidan oldin GC uni Finalization Queue navbatiga qo'yadi va alohida finalizer oqimida destruktorni chaqiradi.

## Ishlash natijasi:
```text
Destruktor chaqirildi: Vaqtinchalik Fayl xotiradan tozalandi.
Main yakunlandi.
```

# 221-Topshiriq: Ichki sinflar (Nested Classes)
## Topshiriq sharti:
Tashqi sinf ichida joylashgan va faqat unga xizmat qiluvchi ichki sinf e'lon qiling.

## Yechim (C# kodi):
```csharp
using System;

class TarmoqXabari
{
    // Ichki sinf
    public class Bosh qism
    {
        public int Id { get; set; }
        public string Protokol { get; set; } = "TCP";
    }

    public Boshqism Header { get; set; } = new();
    public string Tana { get; set; } = "";
}

internal class Program
{
    static void Main()
    {
        var xabar = new TarmoqXabari();
        xabar.Header.Id = 101;
        xabar.Tana = "Salom, Tarmoq!";

        Console.WriteLine($"Xabar ID: {xabar.Header.Id}, Protokol: {xabar.Header.Protokol}, Tana: {xabar.Tana}");
    }
}

```

## Tushuntirish va Mantiq:
Ichki sinflar (Nested Classes) faqat tashqi sinf kontekstida ma'noga ega bo'lgan ma'lumot tuzilmalarini guruhlashda qo'llaniladi. Ular tashqi sinfning `private` a'zolariga to'liq kira oladi.

## Ishlash natijasi:
```text
Xabar ID: 101, Protokol: TCP, Tana: Salom, Tarmoq!
```

# 222-Topshiriq: Sinf ichidagi const vs static readonly maydonlar
## Topshiriq sharti:
`const` bilan `static readonly` ning xotirada joylashishi va initsializatsiya paytini solishtiring.

## Yechim (C# kodi):
```csharp
using System;

class DasturSozlamalari
{
    // const: Kompilyatsiya vaqtida qiymat oladi va inlining qilinadi
    public const string StandartValyuta = "UZS";

    // static readonly: Runtime da yuklanadi (masalan muhit o'zgaruvchisidan)
    public static readonly DateTime BoshlanganSana = DateTime.Now;
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine($"Valyuta: {DasturSozlamalari.StandartValyuta}");
        Console.WriteLine($"Boshlangan sana yili: {DasturSozlamalari.BoshlanganSana.Year}");
    }
}

```

## Tushuntirish va Mantiq:
`const` primitiv turlar uchun juda tez ishlaydi, ammo uning qiymati kompilyatsiya paytida aniq bo'lishi shart. `static readonly` esa dastur ishlashi paytida murakkab hisob-kitoblar yoki konfiguratsiya fayllaridan yuklanishi mumkin.

## Ishlash natijasi:
```text
Valyuta: UZS
Boshlangan sana yili: 2026
```

# 223-Topshiriq: CLR xotira tuzilishi: Type Handle va Sync Block Index
## Topshiriq sharti:
Heap da joylashgan har bir C# obyekti xotirasida maydonlardan tashqari qanday xizmat ma'lumotlari bo'lishini tushuntiring.

## Yechim (C# kodi):
```csharp
using System;

class OddiyObyekt
{
    public int Son; // 4 bayt
}

internal class Program
{
    static void Main()
    {
        var obj = new OddiyObyekt { Son = 42 };

        Console.WriteLine("Obyekt xotiradagi tuzilishi (64-bit CLR da):");
        Console.WriteLine("1. Sync Block Index: 8 bayt (lock va hashcode uchun)");
        Console.WriteLine("2. Type Handle (Method Table Pointer): 8 bayt (turi haqida ma'lumot)");
        Console.WriteLine("3. Maydonlar: Son = 4 bayt (+ 4 bayt alignment to'ldirish)");
        Console.WriteLine("Jami bitta bo'sh obyekt kamida 24 bayt xotira oladi!");
    }
}

```

## Tushuntirish va Mantiq:
Har qanday Reference Type obyekti Heap da 2 ta qo'shimcha so'z (header) saqlaydi: `Sync Block Index` (oqimlararo qulflash va `GetHashCode` uchun) hamda `Type MethodTable Pointer` (virtual metodlar jadvaliga havola).

## Ishlash natijasi:
```text
Obyekt xotiradagi tuzilishi (64-bit CLR da):
1. Sync Block Index: 8 bayt (lock va hashcode uchun)
2. Type Handle (Method Table Pointer): 8 bayt (turi haqida ma'lumot)
3. Maydonlar: Son = 4 bayt (+ 4 bayt alignment to'ldirish)
Jami bitta bo'sh obyekt kamida 24 bayt xotira oladi!
```

# 224-Topshiriq: ToString() metodini qayta yuklash (Overriding)
## Topshiriq sharti:
Obyekt konsolga chiqarilganda tushunarli matn paydo bo'lishi uchun `ToString` ni `override` qiling.

## Yechim (C# kodi):
```csharp
using System;

class Nuqta2D
{
    public int X { get; }
    public int Y { get; }

    public Nuqta2D(int x, int y) => (X, Y) = (x, y);

    public override string ToString() => $"Nuqta({X}, {Y})";
}

internal class Program
{
    static void Main()
    {
        var n = new Nuqta2D(15, 30);
        Console.WriteLine($"Obyekt chop etildi: {n}");
    }
}

```

## Tushuntirish va Mantiq:
Standart holatda `object.ToString()` sinfning to'liq nomini (`Namespace.SinfNomi`) qaytaradi. Uni `override` qilish orqali obyektning ichki holatini formatlangan matn sifatida ko'rsatish mumkin.

## Ishlash natijasi:
```text
Obyekt chop etildi: Nuqta(15, 30)
```

# 225-Topshiriq: Static Factory Method naqshi bilan obyekt yaratish
## Topshiriq sharti:
Konstruktor o'rniga aniq ma'noli statik metodlar orqali obyekt yaratishni joriy qiling.

## Yechim (C# kodi):
```csharp
using System;

class Harorat
{
    public double Selsiy { get; }

    private Harorat(double selsiy) => Selsiy = selsiy;

    // Factory metodlar
    public static Harorat FromSelsiy(double s) => new(s);
    public static Harorat FromKelvin(double k) => new(k - 273.15);
}

internal class Program
{
    static void Main()
    {
        var h1 = Harorat.FromSelsiy(25);
        var h2 = Harorat.FromKelvin(300);

        Console.WriteLine($"h1 Selsiy: {h1.Selsiy:F1}°C");
        Console.WriteLine($"h2 Selsiy: {h2.Selsiy:F1}°C");
    }
}

```

## Tushuntirish va Mantiq:
Static Factory Method konstruktordan farqli ravishda ma'noli nomga ega bo'ladi (`FromKelvin`, `FromSelsiy`), keshdagi obyektlarni qaytarishi yoki turli mantiqiy tekshiruvlarni qulay bajarishi mumkin.

## Ishlash natijasi:
```text
h1 Selsiy: 25.0°C
h2 Selsiy: 26.9°C
```

# 226-Topshiriq: GC.SuppressFinalize va IDisposable bilan resurslarni tozalash
## Topshiriq sharti:
Resurs qo'lda tozalanganda destruktor qayta chaqirilmasligi uchun `GC.SuppressFinalize` dan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

class XavfsizFayl : IDisposable
{
    private bool tozalandi = false;

    public void Dispose()
    {
        Tozala(true);
        GC.SuppressFinalize(this); // GC ga destruktorni chaqirmaslikni buyurish
    }

    protected virtual void Tozala(bool qoldanTozalandi)
    {
        if (!tozalandi)
        {
            if (qoldanTozalandi)
            {
                Console.WriteLine("Boshqariladigan (managed) resurslar qo'lda tozalandi.");
            }
            Console.WriteLine("Operatsion tizim resurslari tozalandi.");
            tozalandi = true;
        }
    }

    ~XavfsizFayl()
    {
        Tozala(false); // Dasturchi Dispose ni chaqirishni unutganda GC tozalaydi
    }
}

internal class Program
{
    static void Main()
    {
        using (var fayl = new XavfsizFayl())
        {
            Console.WriteLine("Fayl bilan ishlanmoqda...");
        } // using tugaganda Dispose() chaqiriladi va SuppressFinalize ishlaydi
    }
}

```

## Tushuntirish va Mantiq:
`GC.SuppressFinalize(this)` ob'yektni Finalization Queue ro'yxatidan o'chiradi. Bu GC ga obyektni darhol (Gen 0/1 da) tozalash imkonini beradi va tizim unumdorligini oshiradi.

## Ishlash natijasi:
```text
Fayl bilan ishlanmoqda...
Boshqariladigan (managed) resurslar qo'lda tozalandi.
Operatsion tizim resurslari tozalandi.
```

# 227-Topshiriq: Singleton naqshi: Thread-safe Singleton with Lazy<T>
## Topshiriq sharti:
`Lazy<T>` yordamida butun dastur davomida faqat bitta instansiyaga ega bo'lgan oqimlararo xavfsiz Singleton sinfini quring.

## Yechim (C# kodi):
```csharp
using System;

class TizimSozlamasi
{
    private static readonly Lazy<TizimSozlamasi> nusxa =
        new(() => new TizimSozlamasi());

    public static TizimSozlamasi Instance => nusxa.Value;

    public string Muhit { get; set; } = "Production";

    private TizimSozlamasi()
    {
        Console.WriteLine(">> TizimSozlamasi bir martagina instansiyalandi!");
    }
}

internal class Program
{
    static void Main()
    {
        var s1 = TizimSozlamasi.Instance;
        var s2 = TizimSozlamasi.Instance;

        Console.WriteLine($"Muhit: {s1.Muhit}");
        Console.WriteLine($"s1 va s2 bitta obyektdami: {object.ReferenceEquals(s1, s2)}");
    }
}

```

## Tushuntirish va Mantiq:
`Lazy<T>` C# da kechiktirilgan initsializatsiyani (lazy loading) va bir nechta oqimlar bir vaqtda kirganda ham faqat bitta obyekt yaratilishini (thread-safety) to'liq kafolatlaydi.

## Ishlash natijasi:
```text
>> TizimSozlamasi bir martagina instansiyalandi!
Muhit: Production
s1 va s2 bitta obyektdami: True
```

# 228-Topshiriq: Builder naqshi: Murakkab obyektlarni bosqichma-bosqich yig'ish
## Topshiriq sharti:
Ko'p parametrlarga ega kompyuter konfiguratsiyasini yaratish uchun Builder naqshini joriy qiling.

## Yechim (C# kodi):
```csharp
using System;

class Kompyuter
{
    public string CPU { get; set; } = "";
    public int RAM { get; set; }
    public int SSD { get; set; }
    public string GPU { get; set; } = "";

    public override string ToString() => $"Kompyuter: CPU={CPU}, RAM={RAM}GB, SSD={SSD}GB, GPU={GPU}";
}

class KompyuterBuilder
{
    private readonly Kompyuter pc = new();

    public KompyuterBuilder SetCPU(string cpu) { pc.CPU = cpu; return this; }
    public KompyuterBuilder SetRAM(int ram) { pc.RAM = ram; return this; }
    public KompyuterBuilder SetSSD(int ssd) { pc.SSD = ssd; return this; }
    public KompyuterBuilder SetGPU(string gpu) { pc.GPU = gpu; return this; }

    public Kompyuter Build() => pc;
}

internal class Program
{
    static void Main()
    {
        var gamingPC = new KompyuterBuilder()
            .SetCPU("Intel Core i9")
            .SetRAM(32)
            .SetSSD(1000)
            .SetGPU("RTX 4080")
            .Build();

        Console.WriteLine(gamingPC);
    }
}

```

## Tushuntirish va Mantiq:
Builder naqshi juda ko'p argumentli konstruktorlar (Telescoping Constructor anti-pattern) o'rniga obyektni bosqichma-bosqich, o'qilishi oson metodlar zanjiri orqali qurishga xizmat qiladi.

## Ishlash natijasi:
```text
Kompyuter: CPU=Intel Core i9, RAM=32GB, SSD=1000GB, GPU=RTX 4080
```

# 229-Topshiriq: Value Object tamoyili: Qiymat tengligi (Equals va GetHashCode)
## Topshiriq sharti:
Obyektlar havolasiga emas, balki ichidagi qiymatlariga qarab teng deb hisoblanishi uchun `Equals` va `GetHashCode` ni qayta yozing.

## Yechim (C# kodi):
```csharp
using System;

class Pul
{
    public decimal Miqdor { get; }
    public string Valyuta { get; }

    public Pul(decimal miqdor, string valyuta)
    {
        Miqdor = miqdor;
        Valyuta = valyuta;
    }

    public override bool Equals(object? obj)
    {
        return obj is Pul boshqa && Miqdor == boshqa.Miqdor && Valyuta == boshqa.Valyuta;
    }

    public override int GetHashCode() => HashCode.Combine(Miqdor, Valyuta);
}

internal class Program
{
    static void Main()
    {
        var p1 = new Pul(50000, "UZS");
        var p2 = new Pul(50000, "UZS");

        Console.WriteLine($"p1 va p2 ReferenceEquals: {object.ReferenceEquals(p1, p2)}");
        Console.WriteLine($"p1 va p2 Equals: {p1.Equals(p2)}");
    }
}

```

## Tushuntirish va Mantiq:
Domen modellashtirishda (DDD) Value Object lar o'z identifikatoriga ega bo'lmaydi, faqat qiymatlari orqali aniqlanadi. `Equals` va `GetHashCode` ni moslashtirish ularni `Dictionary` va `HashSet` larda to'g'ri ishlashini ta'minlaydi.

## Ishlash natijasi:
```text
p1 va p2 ReferenceEquals: False
p1 va p2 Equals: True
```

# 230-Topshiriq: Immutability (O'zgarmaslik) sinflarda
## Topshiriq sharti:
Yaratilgandan so'ng holati hech qachon o'zgarmaydigan to'liq o'zgarmas (immutable) sinf yarating.

## Yechim (C# kodi):
```csharp
using System;

public sealed class ValyutaKursi
{
    public string Kod { get; }
    public decimal Kurs { get; }
    public DateTime Sana { get; }

    public ValyutaKursi(string kod, decimal kurs, DateTime sana)
    {
        Kod = kod;
        Kurs = kurs;
        Sana = sana;
    }
}

internal class Program
{
    static void Main()
    {
        var kurs = new ValyutaKursi("USD", 12800m, DateTime.Today);
        Console.WriteLine($"{kurs.Kod}: {kurs.Kurs} so'm ({kurs.Sana:yyyy-MM-dd})");
        // kurs.Kurs = 13000m; // XATO! O'zgartirib bo'lmaydi
    }
}

```

## Tushuntirish va Mantiq:
O'zgarmas sinflar ko'p oqimli dasturlashda 100% xavfsiz (thread-safe), kutilmagan yon ta'sirlardan xoli va keshlashtirish uchun ideal vositadir.

## Ishlash natijasi:
```text
USD: 12800 so'm (2026-11-08)
```

# 231-Topshiriq: Copy Constructor: Obyekt nusxasini yaratish
## Topshiriq sharti:
Mavjud obyektdan nusxa oluvchi va ayrim xossalarini yangilovchi nusxa ko'chirish konstruktorini yozing.

## Yechim (C# kodi):
```csharp
using System;

class Xat
{
    public string QabulQiluvchi { get; set; }
    public string Mavzu { get; set; }
    public string Matn { get; set; }

    public Xat(string qabul, string mavzu, string matn)
    {
        QabulQiluvchi = qabul;
        Mavzu = mavzu;
        Matn = matn;
    }

    // Copy Constructor
    public Xat(Xat nusxa)
    {
        QabulQiluvchi = nusxa.QabulQiluvchi;
        Mavzu = nusxa.Mavzu;
        Matn = nusxa.Matn;
    }
}

internal class Program
{
    static void Main()
    {
        var x1 = new Xat("ali@uz", "Hisobot", "Oylik hisobot ilova qilindi.");
        var x2 = new Xat(x1) { QabulQiluvchi = "vali@uz" };

        Console.WriteLine($"1-xat kimga: {x1.QabulQiluvchi}");
        Console.WriteLine($"2-xat kimga: {x2.QabulQiluvchi}, Mavzusi: {x2.Mavzu}");
    }
}

```

## Tushuntirish va Mantiq:
Copy Constructor mavjud obyektning barcha maydonlarini yangi yaratilayotgan ob'yektga ko'chirib beradi. Bu yangi ob'yekt ustidagi amallar asl nusxaga ta'sir qilmasligini kafolatlaydi.

## Ishlash natijasi:
```text
1-xat kimga: ali@uz
2-xat kimga: vali@uz, Mavzusi: Hisobot
```

# 232-Topshiriq: Nullable Reference Types (NRT) sinflarda
## Topshiriq sharti:
C# 8+ da kiritilgan Nullable Reference Types qoidalariga rioya qiluvchi va `CS8618` ogohlantirishini to'g'ri bartaraf etuvchi sinf tuzing.

## Yechim (C# kodi):
```csharp
using System;

class Profil
{
    // null bo'lishi mumkin bo'lmagan maydon
    public string Login { get; set; }

    // null bo'lishi mumkin bo'lgan maydon
    public string? Bio { get; set; }

    public Profil(string login)
    {
        Login = login; // Konstruktorda to'ldirilishi shart
    }
}

internal class Program
{
    static void Main()
    {
        var p = new Profil("super_coder");
        Console.WriteLine($"Login: {p.Login}, Bio: {(p.Bio ?? "Mavjud emas")}");
    }
}

```

## Tushuntirish va Mantiq:
NRT yoqilganda `string` hech qachon `null` bo'la olmaydi. Agar xususiyat `null` bo'lishi mumkin bo'lsa, u aniq `string?` qilib e'lon qilinishi shart. Bu dasturdagi potensial `NullReferenceException` xatolarining 90% ini kompilyatsiya bosqichidayoq bartaraf etadi.

## Ishlash natijasi:
```text
Login: super_coder, Bio: Mavjud emas
```

# 233-Topshiriq: Domen modeli: Bank hisob raqami (Invariants va biznes qoidalar)
## Topshiriq sharti:
Balans noldan kam bo'lmasligi va pul yechish chegaralarini qat'iy tekshiruvchi boy domen modelini yozing.

## Yechim (C# kodi):
```csharp
using System;

class HisobRaqam
{
    public string Raqam { get; }
    public decimal Balans { get; private set; }

    public HisobRaqam(string raqam, decimal dastlabkiBalans)
    {
        if (dastlabkiBalans < 0) throw new ArgumentException("Boshlang'ich balans manfiy bo'lolmaydi");
        Raqam = raqam;
        Balans = dastlabkiBalans;
    }

    public void MablagKirit(decimal summa)
    {
        if (summa <= 0) throw new ArgumentException("Summa musbat bo'lishi shart");
        Balans += summa;
    }

    public bool MablagYech(decimal summa)
    {
        if (summa <= 0 || summa > Balans) return false;
        Balans -= summa;
        return true;
    }
}

internal class Program
{
    static void Main()
    {
        var hisob = new HisobRaqam("2020800099", 100000);
        hisob.MablagKirit(50000);
        bool yechildi = hisob.MablagYech(120000);

        Console.WriteLine($"Yechish muvaffaqiyati: {yechildi}, Qolgan balans: {hisob.Balans} so'm");
    }
}

```

## Tushuntirish va Mantiq:
Boy domen modeli (Rich Domain Model) Anemic Domain Model dan farqli o'laroq, barcha biznes qoidalari va invariantlarni sinf ichida saqlaydi va noto'g'ri holatga tushishni imkonsiz qiladi.

## Ishlash natijasi:
```text
Yechish muvaffaqiyati: True, Qolgan balans: 30000 so'm
```

# 234-Topshiriq: Domen modeli: Savatcha (ShoppingCart) va mahsulotlar yig'indisi
## Topshiriq sharti:
Ichida to'plam saqlovchi va jami summani hisoblovchi sinf arxitekturasini quring.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

record SavatElementi(string MahsulotNomi, decimal Narx, int Soni)
{
    public decimal Jami => Narx * Soni;
}

class Savat
{
    private readonly List<SavatElementi> elementlar = new();

    public IReadOnlyList<SavatElementi> Elementlar => elementlar.AsReadOnly();

    public void Qoshish(string nom, decimal narx, int soni)
    {
        elementlar.Add(new SavatElementi(nom, narx, soni));
    }

    public decimal JamiSumma()
    {
        decimal jami = 0;
        foreach (var e in elementlar) jami += e.Jami;
        return jami;
    }
}

internal class Program
{
    static void Main()
    {
        var savat = new Savat();
        savat.Qoshish("Klaviatura", 250000, 1);
        savat.Qoshish("Sichqoncha", 120000, 2);

        Console.WriteLine($"Savatchadagi mahsulotlar soni: {savat.Elementlar.Count}");
        Console.WriteLine($"Jami summa: {savat.JamiSumma():N0} so'm");
    }
}

```

## Tushuntirish va Mantiq:
Ichki ro'yxatni `IReadOnlyList<T>` orqali ochish inkapsulyatsiyani saqlaydi: tashqi kod savatchani aylanib ko'rishi mumkin, ammo to'g'ridan-to'g'ri element qo'sha yoki o'chira olmaydi.

## Ishlash natijasi:
```text
Savatchadagi mahsulotlar soni: 2
Jami summa: 490,000 so'm
```

# 235-Topshiriq: Domen hodisalarini (Domain Events) qayd etish
## Topshiriq sharti:
Sinf ichida muhim biznes amali yuz berganda hodisa obyektini ro'yxatga oluvchi mexanizm tuzing.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

record BuyurtmaTolandiHodisasi(Guid BuyurtmaId, decimal Summa, DateTime Vaqt);

class BuyurtmaModeli
{
    public Guid Id { get; } = Guid.NewGuid();
    private readonly List<object> hodisalar = new();

    public IReadOnlyCollection<object> Hodisalar => hodisalar.AsReadOnly();

    public void TolovQabulQil(decimal summa)
    {
        Console.WriteLine($"To'lov amalga oshirildi: {summa:N0} so'm");
        hodisalar.Add(new BuyurtmaTolandiHodisasi(Id, summa, DateTime.UtcNow));
    }
}

internal class Program
{
    static void Main()
    {
        var b = new BuyurtmaModeli();
        b.TolovQabulQil(750000);

        Console.WriteLine($"Qayd etilgan hodisalar soni: {b.Hodisalar.Count}");
    }
}

```

## Tushuntirish va Mantiq:
Domain Events dasturiy ta'minot arxitekturasida (masalan Clean Architecture va Microservices) modullar orasida bog'lanishni kamaytirish va kesh, log hamda email jo'natish kabi amallarni xabardor qilish uchun ishlatiladi.

## Ishlash natijasi:
```text
To'lov amalga oshirildi: 750,000 so'm
Qayd etilgan hodisalar soni: 1
```

# 236-Topshiriq: WeakReference<T>: Katta obyektlarni xotirani band qilmasdan ushlab turish
## Topshiriq sharti:
`WeakReference` yordamida Garbage Collector zarur bo'lganda tozalab yuborishi mumkin bo'lgan kuchsiz havolani boshqaring.

## Yechim (C# kodi):
```csharp
using System;

class KattaRasm
{
    public byte[] Bufer = new byte[1024]; // Simulyatsiya
}

internal class Program
{
    static void Main()
    {
        var rasm = new KattaRasm();
        var kuchsizHavola = new WeakReference<KattaRasm>(rasm);

        Console.WriteLine($"Obyekt xotirada mavjudmi: {kuchsizHavola.TryGetTarget(out _)}");

        rasm = null; // Kuchli havola uzildi
        GC.Collect(); // Xotira tozalanadi

        bool tirikmi = kuchsizHavola.TryGetTarget(out var qutqarilgan);
        Console.WriteLine($"GC dan keyin obyekt yashab qoldimi: {tirikmi}");
    }
}

```

## Tushuntirish va Mantiq:
`WeakReference<T>` ob'yektni GC ning tozalashidan to'sib qo'ymaydi. Katta hajmdagi keshlar uchun juda qulay: xotira yetarli bo'lsa keshdan olinadi, xotira tugaganda GC ularni bemalol tozalaydi.

## Ishlash natijasi:
```text
Obyekt xotirada mavjudmi: True
GC dan keyin obyekt yashab qoldimi: False
```

# 237-Topshiriq: GC generatsiyalarini aniqlash: GC.GetGeneration(obj)
## Topshiriq sharti:
Obyekt qaysi GC generatsiyasida (Gen 0, Gen 1, Gen 2) yashayotganini aniqlang.

## Yechim (C# kodi):
```csharp
using System;

class SinovObyekti { }

internal class Program
{
    static void Main()
    {
        var obj = new SinovObyekti();
        Console.WriteLine($"Yangi yaratilgan obyekt generatsiyasi: Gen {GC.GetGeneration(obj)}");

        GC.Collect(0); // Gen 0 tozalandi, tirik qolgan obyekt Gen 1 ga o'tadi
        Console.WriteLine($"1-tozalashdan keyin: Gen {GC.GetGeneration(obj)}");

        GC.Collect(1); // Gen 1 tozalandi, obyekt Gen 2 ga o'tadi
        Console.WriteLine($"2-tozalashdan keyin: Gen {GC.GetGeneration(obj)}");
    }
}

```

## Tushuntirish va Mantiq:
.NET Garbage Collector 3 ta generatsiyadan foydalanadi: Gen 0 (yangi kichik obyektlar), Gen 1 (o'tish bosqichi) va Gen 2 (uzoq yashovchi obyektlar). Har bir tozalashdan omon qolgan obyekt yuqori generatsiyaga ko'tariladi.

## Ishlash natijasi:
```text
Yangi yaratilgan obyekt generatsiyasi: Gen 0
1-tozalashdan keyin: Gen 1
2-tozalashdan keyin: Gen 2
```

# 238-Topshiriq: Aggregation vs Composition: Obyektlar o'rtasidagi munosabat
## Topshiriq sharti:
Kompozitsiya (qat'iy bog'liqlik) va Agregatsiya (erkin bog'liqlik) munosabatlarini C# kodida ifodalang.

## Yechim (C# kodi):
```csharp
using System;

// Agregatsiya: O'qituvchi maktabsiz ham mustaqil yashay oladi
class Oqituvchi
{
    public string Ism { get; set; } = "";
}

// Kompozitsiya: Xona maktab mavjud bo'lsagina ma'noga ega
class Xona
{
    public int Raqam { get; set; }
}

class Maktab
{
    public Oqituvchi? TayinlanganOqituvchi { get; set; } // Agregatsiya (tashqaridan beriladi)
    public Xona AsosiyXona { get; } = new() { Raqam = 101 }; // Kompozitsiya (maktab bilan birga tug'iladi)
}

internal class Program
{
    static void Main()
    {
        var ustoz = new Oqituvchi { Ism = "Olim aka" };
        var maktab = new Maktab { TayinlanganOqituvchi = ustoz };

        Console.WriteLine($"Maktab xonasi: {maktab.AsosiyXona.Raqam}");
        Console.WriteLine($"Maktab o'qituvchisi: {maktab.TayinlanganOqituvchi.Ism}");
    }
}

```

## Tushuntirish va Mantiq:
Kompozitsiyada butun yo'qolsa, uning qismlari ham birga yo'qoladi (`Xona`). Agregatsiyada esa qism mustaqil ob'yekt bo'lib, uning hayot davri butunga bog'liq bo'lmaydi (`Oqituvchi`).

## Ishlash natijasi:
```text
Maktab xonasi: 101
Maktab o'qituvchisi: Olim aka
```

# 239-Topshiriq: Computed (Hisoblangan) xossalar
## Topshiriq sharti:
Xotirada maydon saqlamasdan, boshqa xossalarga tayanib har chaqirilganda hisoblanuvchi xossani yozing.

## Yechim (C# kodi):
```csharp
using System;

class Tortburchak
{
    public double Eni { get; set; }
    public double Boyi { get; set; }

    // Computed property
    public double Yuza => Eni * Boyi;
    public double Perimetr => 2 * (Eni + Boyi);
}

internal class Program
{
    static void Main()
    {
        var t = new Tortburchak { Eni = 5, Boyi = 10 };
        Console.WriteLine($"Eni: {t.Eni}, Bo'yi: {t.Boyi}");
        Console.WriteLine($"Yuza: {t.Yuza}, Perimetr: {t.Perimetr}");
    }
}

```

## Tushuntirish va Mantiq:
Hisoblangan xossalar uchun backing field kerak emas. Ular har doim obyektning joriy holatiga mos eng yangi ma'lumotni hisoblab beradi va sinxronizatsiya buzilishining oldini oladi.

## Ishlash natijasi:
```text
Eni: 5, Bo'yi: 10
Yuza: 50, Perimetr: 30
```

# 240-Topshiriq: Generic metod oddiy sinf ichida
## Topshiriq sharti:
Oddiy (nogenerik) sinf ichida o'z tur parametriga (`<T>`) ega bo'lgan generik metod e'lon qiling.

## Yechim (C# kodi):
```csharp
using System;

class ChopQiluvchi
{
    public void EkrangaChiqar<T>(T element, string belgi = "=")
    {
        Console.WriteLine($"{belgi} [{typeof(T).Name}]: {element}");
    }
}

internal class Program
{
    static void Main()
    {
        var printer = new ChopQiluvchi();
        printer.EkrangaChiqar(123);
        printer.EkrangaChiqar("Salom C#");
        printer.EkrangaChiqar(true, "*");
    }
}

```

## Tushuntirish va Mantiq:
Sinfning o'zi umumiy (generic) bo'lmasa ham, uning ayrim metodlari o'zlarining shaxsiy `<T>` parametriga ega bo'lishi mumkin. Bu yordamchi sinflarda universal yechimlar yaratishga imkon beradi.

## Ishlash natijasi:
```text
= [Int32]: 123
= [String]: Salom C#
* [Boolean]: True
```

# 241-Topshiriq: ReferenceEquals vs Equals taqqoslash
## Topshiriq sharti:
Xotira manzillari bo'yicha tenglik (`ReferenceEquals`) va qiymat tengligi (`Equals`) orasidagi amaliy farqni ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

class Inson
{
    public string Ism { get; set; } = "";
}

internal class Program
{
    static void Main()
    {
        var i1 = new Inson { Ism = "Ali" };
        var i2 = new Inson { Ism = "Ali" };
        var i3 = i1;

        Console.WriteLine($"i1 == i2 (ReferenceEquals): {object.ReferenceEquals(i1, i2)}");
        Console.WriteLine($"i1 == i3 (ReferenceEquals): {object.ReferenceEquals(i1, i3)}");
    }
}

```

## Tushuntirish va Mantiq:
`ReferenceEquals` faqat Stack dagi ko'rsatkichlarning bir xil Heap manziliga qarayotganini tekshiradi. Ikkala obyektning barcha maydonlari bir xil bo'lsa ham, ular alohida `new` qilingan bo'lsa, `ReferenceEquals` har doim `false` beradi.

## Ishlash natijasi:
```text
i1 == i2 (ReferenceEquals): False
i1 == i3 (ReferenceEquals): True
```

# 242-Topshiriq: Strategy naqshi: Obyekt xulq-atvorini dinamik o'zgartirish
## Topshiriq sharti:
Sinfning to'lovni hisoblash algoritmini konstruktor orqali dinamik almashtiring.

## Yechim (C# kodi):
```csharp
using System;

class TolovStrategiyasi
{
    public Func<decimal, decimal> KomissiyaHisobla { get; set; }

    public TolovStrategiyasi(Func<decimal, decimal> komissiya)
    {
        KomissiyaHisobla = komissiya;
    }
}

internal class Program
{
    static void Main()
    {
        var humo = new TolovStrategiyasi(summa => summa * 0.005m); // 0.5%
        var visa = new TolovStrategiyasi(summa => summa * 0.02m);  // 2%

        decimal xarid = 1000000m;
        Console.WriteLine($"Humo komissiyasi: {humo.KomissiyaHisobla(xarid)} so'm");
        Console.WriteLine($"Visa komissiyasi: {visa.KomissiyaHisobla(xarid)} so'm");
    }
}

```

## Tushuntirish va Mantiq:
Strategy naqshi sinfning harakatlarini algoritmlar oilasiga ajratib, ularni bir-birining o'rnida erkin almashtirish imkonini beradi.

## Ishlash natijasi:
```text
Humo komissiyasi: 5000.000m so'm
Visa komissiyasi: 20000.00m so'm
```

# 243-Topshiriq: Obyektlar hovuzi (Object Pool pattern) asoslari
## Topshiriq sharti:
Tez-tez yaratilib yo'q qilinadigan og'ir sinf instansiyalarini ro'yxatda saqlab qayta ishlatish mexanizmini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

class TarmoqKlienti
{
    public int Id { get; set; }
}

class KlientHovuzi
{
    private readonly Queue<TarmoqKlienti> hovuz = new();
    private int counter = 0;

    public TarmoqKlienti Olish()
    {
        if (hovuz.Count > 0) return hovuz.Dequeue();
        return new TarmoqKlienti { Id = ++counter };
    }

    public void Qaytarish(TarmoqKlienti klient)
    {
        hovuz.Enqueue(klient);
    }
}

internal class Program
{
    static void Main()
    {
        var pool = new KlientHovuzi();
        var k1 = pool.Olish();
        Console.WriteLine($"Olingan klient ID: {k1.Id}");

        pool.Qaytarish(k1);
        var k2 = pool.Olish();
        Console.WriteLine($"Qayta olingan klient ID: {k2.Id} (Aynan o'sha instansiya)");
    }
}

```

## Tushuntirish va Mantiq:
Object Pool pattern ma'lumotlar bazasi ulanishlari (Connection Pool) va o'yinlardagi zarralar (bullets/particles) uchun juda muhim bo'lib, xotira ajratish va tozalash xarajatlarini yo'qotadi.

## Ishlash natijasi:
```text
Olingan klient ID: 1
Qayta olingan klient ID: 1 (Aynan o'sha instansiya)
```

# 244-Topshiriq: Obyektda xatolik yuz berganda Transactional Rollback qilish
## Topshiriq sharti:
Obyektning o'zgarishlarini saqlashdan oldin tekshiruvdan o'tkazuvchi mantiq yozing.

## Yechim (C# kodi):
```csharp
using System;

class TizimHolati
{
    public string Konfig { get; private set; } = "Standart";

    public bool Yangilash(string yangiKonfig)
    {
        string eski = Konfig;
        Konfig = yangiKonfig;

        if (yangiKonfig.Contains("XATO"))
        {
            Console.WriteLine("Xatolik aniqlandi, holat avvalgiga qaytarildi (Rollback)!");
            Konfig = eski;
            return false;
        }

        return true;
    }
}

internal class Program
{
    static void Main()
    {
        var h = new TizimHolati();
        h.Yangilash("YangiKonfig_1");
        Console.WriteLine($"Joriy holat: {h.Konfig}");

        h.Yangilash("XATO_Konfig");
        Console.WriteLine($"Joriy holat: {h.Konfig}");
    }
}

```

## Tushuntirish va Mantiq:
Obyektlar o'zlarining yaxlitligini (integrity) har doim saqlashi shart. Agar biror qadamda xatolik yuz bersa, obyekt yarimta o'zgargan holatda qolib ketmasligi kerak.

## Ishlash natijasi:
```text
Joriy holat: YangiKonfig_1
Xatolik aniqlandi, holat avvalgiga qaytarildi (Rollback)!
Joriy holat: YangiKonfig_1
```

# 245-Topshiriq: Deconstruct metodi sinflarda
## Topshiriq sharti:
Oddiy sinf ichida `Deconstruct` metodini yozib, obyektni kortejga ajratish imkoniyatini bering.

## Yechim (C# kodi):
```csharp
using System;

class MahsulotKartasi
{
    public string Nomi { get; }
    public decimal Narxi { get; }

    public MahsulotKartasi(string nomi, decimal narxi)
    {
        Nomi = nomi;
        Narxi = narxi;
    }

    public void Deconstruct(out string nomi, out decimal narxi)
    {
        nomi = Nomi;
        narxi = Narxi;
    }
}

internal class Program
{
    static void Main()
    {
        var mahsulot = new MahsulotKartasi("Monitor 4K", 3200000m);

        // Obyektni dekonstruksiya qilish
        var (nom, narx) = mahsulot;

        Console.WriteLine($"Mahsulot: {nom}, Narxi: {narx:N0} so'm");
    }
}

```

## Tushuntirish va Mantiq:
Sinfga `Deconstruct` metodi qo'shilganda, C# kompilyatori uni bir zumda `var (a, b) = obyekt` ko'rinishida ochishga ruxsat beradi.

## Ishlash natijasi:
```text
Mahsulot: Monitor 4K, Narxi: 3,200,000 so'm
```

# 246-Topshiriq: Operatorlarni qayta yuklash (Operator Overloading)
## Topshiriq sharti:
`+` operatorini qayta yuklab, ikkita 2D vektor koordinatalarini qo'shuvchi sinf yarating.

## Yechim (C# kodi):
```csharp
using System;

class Vektor2D
{
    public int X { get; }
    public int Y { get; }

    public Vektor2D(int x, int y) => (X, Y) = (x, y);

    // '+' operatorini overload qilish
    public static Vektor2D operator +(Vektor2D v1, Vektor2D v2)
    {
        return new Vektor2D(v1.X + v2.X, v1.Y + v2.Y);
    }

    public override string ToString() => $"({X}, {Y})";
}

internal class Program
{
    static void Main()
    {
        var v1 = new Vektor2D(3, 4);
        var v2 = new Vektor2D(1, 2);
        var v3 = v1 + v2;

        Console.WriteLine($"{v1} + {v2} = {v3}");
    }
}

```

## Tushuntirish va Mantiq:
Operator Overloading matematik va grafik domen modellarida kodni tabiiy algebraik ifodalar shaklida yozish imkonini beradi. `operator +` har doim `public static` bo'lishi shart.

## Ishlash natijasi:
```text
(3, 4) + (1, 2) = (4, 6)
```

# 247-Topshiriq: Taqqoslash operatorlarini qayta yuklash (== va !=)
## Topshiriq sharti:
`==` va `!=` operatorlarini qayta yuklashda `Equals` bilan sinxronlikni ta'minlang.

## Yechim (C# kodi):
```csharp
using System;

class IDKarta
{
    public string SeriyaRaqam { get; }

    public IDKarta(string seriya) => SeriyaRaqam = seriya;

    public static bool operator ==(IDKarta? a, IDKarta? b)
    {
        if (ReferenceEquals(a, b)) return true;
        if (a is null || b is null) return false;
        return a.SeriyaRaqam == b.SeriyaRaqam;
    }

    public static bool operator !=(IDKarta? a, IDKarta? b) => !(a == b);

    public override bool Equals(object? obj) => obj is IDKarta k && this == k;
    public override int GetHashCode() => SeriyaRaqam.GetHashCode();
}

internal class Program
{
    static void Main()
    {
        var k1 = new IDKarta("AA1234567");
        var k2 = new IDKarta("AA1234567");

        Console.WriteLine($"k1 == k2: {k1 == k2}");
        Console.WriteLine($"k1 != k2: {k1 != k2}");
    }
}

```

## Tushuntirish va Mantiq:
C# qoidalariga ko'ra, agar `==` qayta yuklansa, albatta `!=` ham qayta yuklanishi, shuningdek `Equals` va `GetHashCode` metodlari ham to'g'ri moslashtirilishi shart.

## Ishlash natijasi:
```text
k1 == k2: True
k1 != k2: False
```

# 248-Topshiriq: Axborotni berkitish (Information Hiding) va Getter-only xossalar
## Topshiriq sharti:
Sinfning ichki holatini tashqaridan to'liq yopib, faqat xavfsiz hisoblangan natijalarni ochiq saqlang.

## Yechim (C# kodi):
```csharp
using System;

class XavfsizHisoblagich
{
    private int qiymat = 0;

    public void Qadam() => qiymat++;

    public int JoriyQiymat => qiymat; // Faqat o'qish mumkin
}

internal class Program
{
    static void Main()
    {
        var h = new XavfsizHisoblagich();
        h.Qadam();
        h.Qadam();

        Console.WriteLine($"Joriy hisob: {h.JoriyQiymat}");
        // h.JoriyQiymat = 50; // XATO! Faqat o'qish mumkin
    }
}

```

## Tushuntirish va Mantiq:
Tashqi kod ob'yektning qanday ishlashini bilishi shart emas, faqat nima bera olishini ko'rishi kifoya. Bu dastur tuzilmasini o'zgarishlarga juda chidamli qiladi.

## Ishlash natijasi:
```text
Joriy hisob: 2
```

# 249-Topshiriq: Dastur xotirasi diagnostikasi: GC Memory Info
## Topshiriq sharti:
Joriy jarayonning Heap xotira sarfini `GC.GetTotalMemory` orqali tekshiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        long xotiraOldin = GC.GetTotalMemory(false);

        // 10,000 ta sinf instansiyasi yaratish
        object[] massiv = new object[10000];
        for (int i = 0; i < massiv.Length; i++)
        {
            massiv[i] = new object();
        }

        long xotiraKeyin = GC.GetTotalMemory(false);
        long sarf = xotiraKeyin - xotiraOldin;

        Console.WriteLine($"10,000 obyekt yaratilgandan keyin sarflangan Heap xotira: ~{sarf / 1024} KB");
    }
}

```

## Tushuntirish va Mantiq:
`GC.GetTotalMemory(false)` joriy .NET boshqariladigan (managed) xotirasining taxminiy bayt hajmini qaytaradi. Bu xotira sizishini (memory leak) kuzatishda eng dastlabki vositadir.

## Ishlash natijasi:
```text
10,000 obyekt yaratilgandan keyin sarflangan Heap xotira: ~234 KB
```

# 250-Topshiriq: OOP Sinflar va Obyektlar bo'limi integratsiyalashgan loyihasi
## Topshiriq sharti:
Primary Constructor, required xossalar, to'liq inkapsulyatsiya va biznes mantiqni o'z ichiga olgan to'liq `FoydalanuvchiAkkaunti` sinfini yarating.

## Yechim (C# kodi):
```csharp
using System;

class FoydalanuvchiAkkaunti(string email, string boshlangichRol)
{
    public required string Ism { get; init; }
    public string Email { get; } = email;
    public string Rol { get; private set; } = boshlangichRol;
    public bool Faolmi { get; private set; } = true;

    public void RolniYangila(string yangiRol)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(yangiRol);
        Rol = yangiRol;
        Console.WriteLine($"[LOG]: {Email} roli '{yangiRol}' ga yangilandi.");
    }

    public void Bloklash()
    {
        Faolmi = false;
        Console.WriteLine($"[OGOHLANTIRISH]: {Email} akkaunti bloklandi!");
    }

    public override string ToString() => $"Akkaunt({Ism}, {Email}, {Rol}, Faol={Faolmi})";
}

internal class Program
{
    static void Main()
    {
        var akkaunt = new FoydalanuvchiAkkaunti("kamol@tizim.uz", "Operator")
        {
            Ism = "Kamoliddin"
        };

        Console.WriteLine(akkaunt);
        akkaunt.RolniYangila("Administrator");
        akkaunt.Bloklash();
        Console.WriteLine(akkaunt);
    }
}

```

## Tushuntirish va Mantiq:
Ushbu yechim zamonaviy C# OOP ning barcha ilg'or xususiyatlarini o'zida birlashtiradi: Primary Constructor orqali toza initsializatsiya, `required init` orqali xavfsizlik, shaxsiy holat modifikatorlari orqali qat'iy inkapsulyatsiya va chiroyli `ToString()` ifodasi.

## Ishlash natijasi:
```text
Akkaunt(Kamoliddin, kamol@tizim.uz, Operator, Faol=True)
[LOG]: kamol@tizim.uz roli 'Administrator' ga yangilandi.
[OGOHLANTIRISH]: kamol@tizim.uz akkaunti bloklandi!
Akkaunt(Kamoliddin, kamol@tizim.uz, Administrator, Faol=False)
```

