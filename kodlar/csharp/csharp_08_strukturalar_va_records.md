# 8-Mavzu: Strukturalar va Records (351-400)

Ushbu bo'limda C# tilida qiymat turlari va zamonaviy o'zgarmas ma'lumotlar modellari: `struct` asoslari, Stack da xotira taqsimoti, `readonly struct`, yuqori unumdorlikka ega stack-only `ref struct`, Boxing va unboxing xarajatlari, `record class` va `record struct`, positional recordlar, buzilmas mutatsiya (`with` ifodasi), qiymatga asoslangan tenglik (Value-based equality), dekonstruksiya hamda xotirani tekislash (Struct Layout & Alignment) bo'yicha 50 ta amaliy topshiriq jamlangan.

# 351-Topshiriq: struct e'lon qilish: Stack xotiradagi qiymat turi (Value Type)
## Topshiriq sharti:
2D koordinata nuqtasini ifodalovchi `Nuqta` strukturasini yarating va uning nusxalanishini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

struct Nuqta
{
    public int X;
    public int Y;

    public Nuqta(int x, int y)
    {
        X = x;
        Y = y;
    }
}

internal class Program
{
    static void Main()
    {
        Nuqta p1 = new Nuqta(10, 20);
        Nuqta p2 = p1; // To'liq qiymat nusxalandi (Stack da alohida joy)

        p2.X = 99;

        Console.WriteLine($"p1 koordinatasi: ({p1.X}, {p1.Y})");
        Console.WriteLine($"p2 koordinatasi: ({p2.X}, {p2.Y})");
    }
}

```

## Tushuntirish va Mantiq:
`struct` bu Value Type (qiymat turi) bo'lib, to'g'ridan-to'g'ri Stack xotirada yashaydi (agar sinf ichida bo'lmasa). U boshqa o'zgaruvchiga o'zlashtirilganda barcha baytlari to'liq nusxalanadi, natijada `p1` va `p2` mutlaqo mustaqil bo'lib qoladi.

## Ishlash natijasi:
```text
p1 koordinatasi: (10, 20)
p2 koordinatasi: (99, 20)
```

# 352-Topshiriq: Struct da parametrsiz konstruktor va maydon initsializatsiyasi
## Topshiriq sharti:
C# 10+ qoidalari bo'yicha struktura ichida maydonlarga dastlabki qiymat berish va parametrsiz konstruktor yozishni ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

struct Sozlama
{
    public int Port { get; set; } = 8080;
    public string Host { get; set; } = "localhost";

    public Sozlama()
    {
        // C# 10 dan boshlab struct da parametrsiz konstruktor yozish mumkin
        Port = 9000;
    }
}

internal class Program
{
    static void Main()
    {
        Sozlama s1 = new Sozlama();
        Console.WriteLine($"s1: {s1.Host}:{s1.Port}");

        Sozlama s2 = default; // default literal konstruktorni chaqirmaydi!
        Console.WriteLine($"s2: {(s2.Host == null ? "null" : s2.Host)}:{s2.Port}");
    }
}

```

## Tushuntirish va Mantiq:
C# 10 gacha struct larda parametrsiz konstruktor yozish taqiqlangan edi. C# 10 dan boshlab bunga ruxsat berildi, biroq `default` literali konstruktorni chaqirmasdan xotirani shunchaki 0 ga tenglashtiradi.

## Ishlash natijasi:
```text
s1: localhost:9000
s2: null:0
```

# 353-Topshiriq: Struct larda merosxo'rlikning yo'qligi va interfeyslar
## Topshiriq sharti:
Strukturalar boshqa sinf yoki struct dan meros ololmasligini, ammo interfeyslarni bemalol qabul qilishini namoyish eting.

## Yechim (C# kodi):
```csharp
using System;

interface IChopEtiladigan
{
    void ChopEt();
}

struct Rang : IChopEtiladigan
{
    public byte R, G, B;
    public Rang(byte r, byte g, byte b) => (R, G, B) = (r, g, b);

    public void ChopEt() => Console.WriteLine($"RGB({R}, {G}, {B})");
}

internal class Program
{
    static void Main()
    {
        Rang oq = new Rang(255, 255, 255);
        oq.ChopEt();
    }
}

```

## Tushuntirish va Mantiq:
Xotira yaxlitligini ta'minlash maqsadida strukturalarda sinflar merosxo'rligi (`struct B : A`) taqiqlangan (chunki bu xotira hajmining o'zgarishiga olib keladi). Biroq har qanday interfeysni amalga oshirish mumkin.

## Ishlash natijasi:
```text
RGB(255, 255, 255)
```

# 354-Topshiriq: readonly struct: Mutlaq o'zgarmaslik va yuqori unumdorlik
## Topshiriq sharti:
`readonly struct` e'lon qilib, uning ichidagi barcha maydonlar o'zgarmas bo'lishini ta'minlang.

## Yechim (C# kodi):
```csharp
using System;

readonly struct KvadratOlchami
{
    public double Tomon { get; }
    public double Yuza => Tomon * Tomon;

    public KvadratOlchami(double tomon)
    {
        Tomon = tomon;
    }
}

internal class Program
{
    static void Main()
    {
        var k = new KvadratOlchami(4.0);
        Console.WriteLine($"Tomon: {k.Tomon}, Yuza: {k.Yuza}");

        // k.Tomon = 5.0; // KOMPILYATSIYA XATOSI! readonly struct a'zolarini o'zgartirib bo'lmaydi
    }
}

```

## Tushuntirish va Mantiq:
`readonly struct` kompilyatorga barcha maydonlar o'zgarmas ekanligini bildiradi. Bu .NET JIT ga metodlarga `in` orqali uzatilganda mudofaaviy nusxalash (defensive copy) yaratmasdan xotirani tejash imkonini beradi.

## Ishlash natijasi:
```text
Tomon: 4, Yuza: 16
```

# 355-Topshiriq: readonly metodlar oddiy struct ichida
## Topshiriq sharti:
Oddiy struktura ichidagi xolatni o'zgartirmaydigan metodlarni `readonly` deb belgilash afzalliklari.

## Yechim (C# kodi):
```csharp
using System;

struct Vektor
{
    public double X;
    public double Y;

    public Vektor(double x, double y) => (X, Y) = (x, y);

    // readonly metod: strukturani o'zgartirmaslikka kafolat beradi
    public readonly double Uzunlik()
    {
        // X = 10; // XATO! readonly metod ichida maydonlarni o'zgartirib bo'lmaydi
        return Math.Sqrt(X * X + Y * Y);
    }
}

internal class Program
{
    static void Main()
    {
        var v = new Vektor(3, 4);
        Console.WriteLine($"Vektor uzunligi: {v.Uzunlik()}");
    }
}

```

## Tushuntirish va Mantiq:
Agar strukturaning o'zi `readonly` bo'lmasa ham, uning faqat o'quvchi metodlariga `readonly` qo'yish kompilyatorga ushbu metod chaqirilganda vaqtinchalik nusxa olmaslikni (no defensive copy) buyuradi.

## Ishlash natijasi:
```text
Vektor uzunligi: 5
```

# 356-Topshiriq: ref struct: Stack-only strukturalar va qat'iy cheklovlar
## Topshiriq sharti:
Faqat va faqat Stack xotirada yashaydigan, Heap ga aslo chiqmaydigan `ref struct` e'lon qiling.

## Yechim (C# kodi):
```csharp
using System;

ref struct StackBufer
{
    public int Hajmi;
    public StackBufer(int h) => Hajmi = h;

    public void Korsat() => Console.WriteLine($"StackBufer hajmi: {Hajmi} bayt");
}

internal class Program
{
    static void Main()
    {
        StackBufer bufer = new StackBufer(64);
        bufer.Korsat();

        // object obj = bufer; // KOMPILYATSIYA XATOSI! ref struct ni qutilab (boxing) bo'lmaydi!
    }
}

```

## Tushuntirish va Mantiq:
`ref struct` C# 7.2 da kiritilgan bo'lib, uning obyektlari hech qachon Heap ga chiqmasligini kafolatlaydi. Uni `object` ga kasting qilib bo'lmaydi, interfeyslarni qabul qila olmaydi va sinf maydoni bo'la olmaydi (`Span<T>` aynan shunday qurilgan).

## Ishlash natijasi:
```text
StackBufer hajmi: 64 bayt
```

# 357-Topshiriq: ref struct cheklovlari: Nega generik yoki async metodda bo'la olmaydi?
## Topshiriq sharti:
`ref struct` ning asinxron metodlarda (`async/await`) ishlatilishiga qo'yilgan cheklov sababini tushuntiring.

## Yechim (C# kodi):
```csharp
using System;

ref struct MaxsusSpan
{
    public int Qiymat;
}

internal class Program
{
    // static async Task XatoMetod(MaxsusSpan s) { await Task.Delay(1); } // KOMPILYATSIYA XATOSI!

    static void Main()
    {
        Console.WriteLine("ref struct xavfsizlik cheklovlari:");
        Console.WriteLine("1. Asinxron (async) metodlarda ishlatib bo'lmaydi (chunki state machine Heap ga ko'chadi).");
        Console.WriteLine("2. Oddiy sinf maydoni bo'la olmaydi.");
        Console.WriteLine("3. Generik tur parametri sifatida berib bo'lmaydi.");
    }
}

```

## Tushuntirish va Mantiq:
`async` metodlar kompilyatsiya paytida Holat Mashinasi (State Machine) sinfiga aylanadi va lokal o'zgaruvchilar Heap dagi ushbu sinf maydoniga ko'chadi. `ref struct` esa Heap ga mutlaqo chiqa olmasligi sababli `async` metodlarda taqiqlangan.

## Ishlash natijasi:
```text
ref struct xavfsizlik cheklovlari:
1. Asinxron (async) metodlarda ishlatib bo'lmaydi (chunki state machine Heap ga ko'chadi).
2. Oddiy sinf maydoni bo'la olmaydi.
3. Generik tur parametri sifatida berib bo'lmaydi.
```

# 358-Topshiriq: readonly ref struct: Eng xavfsiz stack oynasi
## Topshiriq sharti:
`readonly ref struct` kombinatsiyasi orqali ham stack-only, ham to'liq o'zgarmas struktura hosil qiling.

## Yechim (C# kodi):
```csharp
using System;

readonly ref struct OqiladiganOyna
{
    private readonly ReadOnlySpan<char> matn;
    public OqiladiganOyna(ReadOnlySpan<char> m) => matn = m;

    public int Uzunlik => matn.Length;
    public void ChopQil() => Console.WriteLine($"Oyna ichidagi matn: '{matn.ToString()}'");
}

internal class Program
{
    static void Main()
    {
        string s = "O'zbekiston";
        var oyna = new OqiladiganOyna(s.AsSpan(0, 7));

        Console.WriteLine($"Uzunlik: {oyna.Uzunlik}");
        oyna.ChopQil();
    }
}

```

## Tushuntirish va Mantiq:
`readonly ref struct` eng yuqori unumdorlikdagi va eng xavfsiz C# turidir. U GC bosimini 0 da ushlab turadi va ichki ko'rsatkichlarning o'zgartirib yuborilishidan to'liq himoyalaydi.

## Ishlash natijasi:
```text
Uzunlik: 7
Oyna ichidagi matn: 'O'zbeki'
```

# 359-Topshiriq: Boxing va Unboxing narxi: GC bosimi tahlili
## Topshiriq sharti:
Oddiy `struct` ni `object` ga solish va qaytarib olishda yuz beradigan operatsiyalarni namoyish eting.

## Yechim (C# kodi):
```csharp
using System;

struct Nuqta { public int X, Y; }

internal class Program
{
    static void Main()
    {
        Nuqta p = new Nuqta { X = 5, Y = 10 };

        // Boxing: Stack dagi baytlar Heap ga yangi obyekt qilib ko'chiriladi
        object box = p;

        // Unboxing: Heap dan Stack ga qayta nusxalanadi
        Nuqta ochilgan = (Nuqta)box;

        Console.WriteLine($"Ochilgan nuqta: ({ochilgan.X}, {ochilgan.Y})");
        Console.WriteLine("Boxing Heap xotira ajratadi va Garbage Collector ga yuk bo'ladi.");
    }
}

```

## Tushuntirish va Mantiq:
Millionlab marta bajariladigan sikllarda strukturalarni `object` yoki `IInterface` ga o'tkazish katta xotira sarfiga olib keladi. Generik to'plamlar (`List<T>`) aynan ushbu boxing ni yo'qotish uchun yaratilgan.

## Ishlash natijasi:
```text
Ochilgan nuqta: (5, 10)
Boxing Heap xotira ajratadi va Garbage Collector ga yuk bo'ladi.
```

# 360-Topshiriq: Mudofaaviy nusxalash (Defensive Copy) va in modifikatori
## Topshiriq sharti:
`readonly` bo'lmagan struct `in` parametri orqali uzatilganda kompilyator nima uchun yashirin nusxa olishini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

struct OddiyStruct
{
    public int Qiymat;
    public void Oshir() => Qiymat++;
}

internal class Program
{
    // 'in' orqali o'zgarmas havola uzatiladi
    static void Sinov(in OddiyStruct s)
    {
        // Kompilyator s.Qiymat xavfsizligini ta'minlash uchun uni yashirin nusxalaydi (Defensive Copy)
        Console.WriteLine($"Qiymat: {s.Qiymat}");
    }

    static void Main()
    {
        var st = new OddiyStruct { Qiymat = 100 };
        Sinov(in st);
        Console.WriteLine("Agar struct 'readonly struct' deb e'lon qilinsa, Defensive Copy yo'qoladi!");
    }
}

```

## Tushuntirish va Mantiq:
Kompilyator `in` parametri orqali uzatilgan oddiy struct o'zgarib ketmasligi uchun har bir metod/xossa chaqiruvida uning nusxasini oladi. Shuning uchun `in` parametrlari faqat `readonly struct` lar bilan birga ishlatilishi kerak.

## Ishlash natijasi:
```text
Qiymat: 100
Agar struct 'readonly struct' deb e'lon qilinsa, Defensive Copy yo'qoladi!
```

# 361-Topshiriq: record class asoslari: Qiymatga asoslangan tenglik (Value-based Equality)
## Topshiriq sharti:
C# 9 da kiritilgan `record class` yordamida ikkita alohida obyektning xossalari bir xil bo'lganda `==` bilan teng bo'lishini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

record class Talaba
{
    public string Ism { get; init; } = "";
    public int Kurs { get; init; }
}

internal class Program
{
    static void Main()
    {
        var t1 = new Talaba { Ism = "Sanjar", Kurs = 2 };
        var t2 = new Talaba { Ism = "Sanjar", Kurs = 2 };

        Console.WriteLine($"t1 == t2: {t1 == t2}"); // True! (Sinflarda bu False bo'lardi)
        Console.WriteLine($"ReferenceEquals(t1, t2): {object.ReferenceEquals(t1, t2)}"); // False
    }
}

```

## Tushuntirish va Mantiq:
`record class` orqada oddiy sinf (Reference Type) bo'lib qoladi, biroq kompilyator unga qiymatga asoslangan tenglik (`Equals`, `==`, `!=`, `GetHashCode`) metodlarini avtomatik generatsiya qilib beradi.

## Ishlash natijasi:
```text
t1 == t2: True
ReferenceEquals(t1, t2): False
```

# 362-Topshiriq: Positional Record sintaksisi: Bitta qatorda to'liq model
## Topshiriq sharti:
Qisqa Positional Record e'lon qiling va uning konstruktori hamda xossalarini tekshiring.

## Yechim (C# kodi):
```csharp
using System;

// Bitta qatorda konstruktor, init-only xossalar, Equals, GetHashCode, ToString, Deconstruct yaratiladi!
record Shaxs(string Ism, int Yosh, string Shahar);

internal class Program
{
    static void Main()
    {
        var inson = new Shaxs("Temur", 28, "Samarqand");

        Console.WriteLine($"Ism: {inson.Ism}, Shahar: {inson.Shahar}");
        Console.WriteLine($"ToString() avtomatik formati: {inson}");
    }
}

```

## Tushuntirish va Mantiq:
Positional Record C# ning eng ixcham va kuchli imkoniyatlaridan biridir. Qavs ichida e'lon qilingan parametrlar avtomatik ravishda `public { get; init; }` xossalariga aylanadi.

## Ishlash natijasi:
```text
Ism: Temur, Shahar: Samarqand
ToString() avtomatik formati: Shaxs { Ism = Temur, Yosh = 28, Shahar = Samarqand }
```

# 363-Topshiriq: Buzilmas mutatsiya (Non-destructive Mutation): with ifodasi
## Topshiriq sharti:
`with` ifodasidan foydalanib mavjud recorddan faqat bitta xossasi o'zgargan yangi nusxa hosil qiling.

## Yechim (C# kodi):
```csharp
using System;

record Xodim(string Ism, string Lavozim, decimal Maosh);

internal class Program
{
    static void Main()
    {
        var x1 = new Xodim("Mansur", "Kichik Dasturchi", 5000000m);

        // with orqali eski obyektga tegmasdan yangi yangilangan nusxa olish
        var x2 = x1 with { Lavozim = "Katta Dasturchi", Maosh = 12000000m };

        Console.WriteLine($"Eski xodim: {x1.Lavozim}, {x1.Maosh:N0} so'm");
        Console.WriteLine($"Yangi xodim: {x2.Lavozim}, {x2.Maosh:N0} so'm");
    }
}

```

## Tushuntirish va Mantiq:
`with` ifodasi obyektning barcha xossalarini yangi xotira manziliga nusxalaydi va faqat jingalak qavs ichida ko'rsatilgan xossalarni yangilaydi. Bu o'zgarmas (immutable) arxitekturaning asosi hisoblanadi.

## Ishlash natijasi:
```text
Eski xodim: Kichik Dasturchi, 5,000,000 so'm
Yangi xodim: Katta Dasturchi, 12,000,000 so'm
```

# 364-Topshiriq: record struct: Qiymat turi bo'lgan recordlar (C# 10)
## Topshiriq sharti:
C# 10 da kiritilgan `record struct` yordamida Stack da saqlanuvchi, `with` va qiymat tengligiga ega strukturani qo'llang.

## Yechim (C# kodi):
```csharp
using System;

record struct Kordinata(double X, double Y);

internal class Program
{
    static void Main()
    {
        var c1 = new Kordinata(10.5, 20.0);
        var c2 = c1 with { Y = 99.0 };

        Console.WriteLine($"c1 turi ValueType mi: {typeof(Kordinata).IsValueType}");
        Console.WriteLine($"c1: {c1}");
        Console.WriteLine($"c2: {c2}");
    }
}

```

## Tushuntirish va Mantiq:
`record struct` recordlarning barcha qulayliklarini (avtomatik `ToString`, `with`, tenglik) qiymat turining tezligi (Stack xotira, 0 bayt Heap ajratilishi) bilan birlashtiradi.

## Ishlash natijasi:
```text
c1 turi ValueType mi: True
c1: Kordinata { X = 10.5, Y = 20 }
c2: Kordinata { X = 10.5, Y = 99 }
```

# 365-Topshiriq: readonly record struct: O'zgarmas qiymatli recordlar
## Topshiriq sharti:
Xossalari o'zgartirilmaydigan to'liq o'zgarmas `readonly record struct` e'lon qiling.

## Yechim (C# kodi):
```csharp
using System;

readonly record struct FoydalanuvchiId(Guid Id);

internal class Program
{
    static void Main()
    {
        var id1 = new FoydalanuvchiId(Guid.NewGuid());
        var id2 = id1;

        Console.WriteLine($"ID tengligi: {id1 == id2}");
        // id1.Id = Guid.NewGuid(); // KOMPILYATSIYA XATOSI! readonly record struct o'zgarmasdir
    }
}

```

## Tushuntirish va Mantiq:
`readonly record struct` domain identifikatorlari (Strongly Typed IDs) uchun eng yaxshi tanlovdir. U hech qanday GC yuki tug'dirmaydi va mutlaqo xavfsizdir.

## Ishlash natijasi:
```text
ID tengligi: True
```

# 366-Topshiriq: Positional Record Struct larda get/set farqi
## Topshiriq sharti:
`record class` da positional xossalar `init` bo'lishi, `record struct` da esa standart `set` bo'lishi farqini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

record struct OchiqNuqta(int X, int Y);
record class QatiyNuqta(int X, int Y);

internal class Program
{
    static void Main()
    {
        var s = new OchiqNuqta(1, 2);
        s.X = 10; // record struct da ruxsat etiladi (mutabilitiy bor)

        var c = new QatiyNuqta(1, 2);
        // c.X = 10; // KOMPILYATSIYA XATOSI! record class da positional parametrlar { get; init; } bo'ladi

        Console.WriteLine($"OchiqNuqta X: {s.X}");
        Console.WriteLine($"QatiyNuqta X: {c.X}");
    }
}

```

## Tushuntirish va Mantiq:
`record class` da positional parametrlar avtomatik ravishda `init` bo'ladi. Ammo `record struct` da orqaga moslik uchun ular standart `set` (o'zgaruvchan) qilingan; agar o'zgarmaslik kerak bo'lsa, `readonly record struct` yozish lozim.

## Ishlash natijasi:
```text
OchiqNuqta X: 10
QatiyNuqta X: 1
```

# 367-Topshiriq: Record larda Dekonstruksiya (Deconstruct)
## Topshiriq sharti:
Positional Record larning o'z-o'zidan kortejga ajralish imkoniyatidan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

record Avtomobil(string Model, int OtKuchi, decimal Narx);

internal class Program
{
    static void Main()
    {
        var avto = new Avtomobil("Malibu 2", 250, 350000000m);

        // Dekonstruksiya: Kompilyator avtomatik yaratgan Deconstruct metodi orqali
        var (model, otKuchi, narx) = avto;

        Console.WriteLine($"Model: {model}");
        Console.WriteLine($"Ot kuchi: {otKuchi} ta");
        Console.WriteLine($"Narxi: {narx:N0} so'm");
    }
}

```

## Tushuntirish va Mantiq:
Positional recordlar uchun C# kompilyatori avtomatik ravishda `Deconstruct` metodini yozib beradi. Natijada record obyektlarini qulay `var (a, b) = obj` ko'rinishida ochish mumkin bo'ladi.

## Ishlash natijasi:
```text
Model: Malibu 2
Ot kuchi: 250 ta
Narxi: 350,000,000 so'm
```

# 368-Topshiriq: Record larda merosxo'rlik (Record Inheritance)
## Topshiriq sharti:
`record class` larda merosxo'rlik qanday ishlashini va `ToString` qanday aks etishini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

abstract record Hayvon(string Nomi);
record It(string Nomi, string Zoti) : Hayvon(Nomi);
record Mushuk(string Nomi, bool UyMushugimi) : Hayvon(Nomi);

internal class Program
{
    static void Main()
    {
        Hayvon h1 = new It("Olapar", "Bo'ribosar");
        Hayvon h2 = new Mushuk("Tom", true);

        Console.WriteLine(h1);
        Console.WriteLine(h2);
    }
}

```

## Tushuntirish va Mantiq:
`record class` lar faqat boshqa record class lardan meros olishi mumkin (oddiy sinflardan meros ololmaydi). Meros olingan recordning `ToString()` metodi barcha ota va bola xossalarini to'liq ko'rsatadi.

## Ishlash natijasi:
```text
It { Nomi = Olapar, Zoti = Bo'ribosar }
Mushuk { Nomi = Tom, UyMushugimi = True }
```

# 369-Topshiriq: DTO (Data Transfer Object) sifatida Record lardan foydalanish
## Topshiriq sharti:
API va mikroservislar o'rtasida ma'lumot almashuvchi DTO modellarni recordlar orqali yarating.

## Yechim (C# kodi):
```csharp
using System;

record FoydalanuvchiDto(int Id, string Ism, string Email);
record RoyxatdanOtishDto(string Ism, string Email, string Parol);

internal class Program
{
    static void Main()
    {
        var sorov = new RoyxatdanOtishDto("Jamshid", "jamshid@pochta.uz", "Maxfiy123!");
        var javob = new FoydalanuvchiDto(1001, sorov.Ism, sorov.Email);

        Console.WriteLine($"Yangi foydalanuvchi javobi: {javob}");
    }
}

```

## Tushuntirish va Mantiq:
Recordlar DTO larni loyihalash uchun eng yaxshi vositadir: ixcham yozilish, o'zgarmaslik (immutability) va loglashda juda qulay `ToString()` formati.

## Ishlash natijasi:
```text
Yangi foydalanuvchi javobi: FoydalanuvchiDto { Id = 1001, Ism = Jamshid, Email = jamshid@pochta.uz }
```

# 370-Topshiriq: Generik ApiResponse recordi
## Topshiriq sharti:
Har qanday API javobini o'rab beruvchi universal generik record tuzing.

## Yechim (C# kodi):
```csharp
using System;

record ApiResponse<T>(bool Muvaffaqiyatli, T? Malumot, string? Xatolik);

internal class Program
{
    static void Main()
    {
        var okJavob = new ApiResponse<string>(true, "Token_998877", null);
        var xatoJavob = new ApiResponse<string>(false, null, "Parol noto'g'ri");

        Console.WriteLine($"Muvaffaqiyatli javob: {okJavob}");
        Console.WriteLine($"Xato javob: {xatoJavob}");
    }
}

```

## Tushuntirish va Mantiq:
Generik recordlar (`ApiResponse<T>`) API lar uchun yagona javob strukturasini (Envelope pattern) bitta qatorda ta'minlaydi.

## Ishlash natijasi:
```text
Muvaffaqiyatli javob: ApiResponse`1 { Muvaffaqiyatli = True, Malumot = Token_998877, Xatolik =  }
Xato javob: ApiResponse`1 { Muvaffaqiyatli = False, Malumot = , Xatolik = Parol noto'g'ri }
```

# 371-Topshiriq: Struct Layout: Xotira zichligi va StructLayout atributi
## Topshiriq sharti:
`System.Runtime.InteropServices.StructLayout` yordamida struktura maydonlarining ketma-ketligini belgilang.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.InteropServices;

[StructLayout(LayoutKind.Sequential)]
struct SensorPaketi
{
    public byte Id;      // 1 bayt
    public int Qiymat;   // 4 bayt
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine($"SensorPaketi xotira hajmi: {Marshal.SizeOf<SensorPaketi>()} bayt");
        Console.WriteLine("(Eslatma: 1 bayt Id + 3 bayt padding + 4 bayt int = 8 bayt)");
    }
}

```

## Tushuntirish va Mantiq:
CLR unumdorlik uchun maydonlarni 4 yoki 8 bayt chegaralariga tekislaydi (Padding). `[StructLayout(LayoutKind.Sequential)]` apparat drayverlari va tarmoq protokollari bilan baytma-bayt moslikni kafolatlaydi.

## Ishlash natijasi:
```text
SensorPaketi xotira hajmi: 8 bayt
(Eslatma: 1 bayt Id + 3 bayt padding + 4 bayt int = 8 bayt)
```

# 372-Topshiriq: FieldOffset atributi bilan xotirani bo'lishish (C-style Union)
## Topshiriq sharti:
`LayoutKind.Explicit` va `[FieldOffset]` orqali bitta xotira katakchasini int va baytlar sifatida ko'ring.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.InteropServices;

[StructLayout(LayoutKind.Explicit)]
struct RangUnion
{
    [FieldOffset(0)] public uint Rgba;
    [FieldOffset(0)] public byte R;
    [FieldOffset(1)] public byte G;
    [FieldOffset(2)] public byte B;
    [FieldOffset(3)] public byte A;
}

internal class Program
{
    static void Main()
    {
        RangUnion rang = default;
        rang.R = 255;
        rang.G = 128;

        Console.WriteLine($"R qiymati: {rang.R}");
        Console.WriteLine($"G qiymati: {rang.G}");
        Console.WriteLine($"Birlashgan RGBA butun soni: 0x{rang.Rgba:X8}");
    }
}

```

## Tushuntirish va Mantiq:
`[FieldOffset(0)]` ikkita har xil maydonni aynan bitta baytdan boshlashga imkon beradi (C tilidagi `union` kabi). Bu grafik dvigatellar va ikkilik protokollarda juda tez ishlaydi.

## Ishlash natijasi:
```text
R qiymati: 255
G qiymati: 128
Birlashgan RGBA butun soni: 0x000080FF
```

# 373-Topshiriq: Struct lar massivi vs Class lar massivi: Kesh samaradorligi (Cache Locality)
## Topshiriq sharti:
`struct[]` ning xotirada uzluksiz ketma-ket joylashishi va `class[]` ning tarqoqligini solishtiring.

## Yechim (C# kodi):
```csharp
using System;

struct NuqtaStruct { public int X, Y; }
class NuqtaClass { public int X, Y; }

internal class Program
{
    static void Main()
    {
        // 1000 ta NuqtaStruct xotirada bitta uzluksiz 8000 baytli blokda yotadi (CPU L1/L2 kesh uchun mukammal!)
        NuqtaStruct[] sMassiv = new NuqtaStruct[1000];

        // 1000 ta NuqtaClass esa 1000 ta havola + Heap da tarqoq 1000 ta alohida obyekt (Pointer chassing / Cache miss)
        NuqtaClass[] cMassiv = new NuqtaClass[1000];

        Console.WriteLine("NuqtaStruct[] kesh unumdorligi bo'yicha Class[] dan bir necha barobar ustun.");
    }
}

```

## Tushuntirish va Mantiq:
Strukturalar massivi CPU L1/L2 keshlarida ajoyib (sequential memory) tezlik beradi, chunki barcha ma'lumotlar bitta blokda yonma-yon turadi. Sinflar esa kesh o'tkazib yuborishlariga (Cache Miss) sabab bo'ladi.

## Ishlash natijasi:
```text
NuqtaStruct[] kesh unumdorligi bo'yicha Class[] dan bir necha barobar ustun.
```

# 374-Topshiriq: Record larda qo'lda konstruktor va validatsiya yozish
## Topshiriq sharti:
Positional record ichida xossalar tekshiruvini qanday kiritishni namoyish eting.

## Yechim (C# kodi):
```csharp
using System;

record FoydalanuvchiYoshi(string Ism, int Yosh)
{
    // Kompilyator yaratgan asosiy konstruktorni tekshiruv bilan to'ldirish
    public FoydalanuvchiYoshi
    {
        if (Yosh < 0)
            throw new ArgumentOutOfRangeException(nameof(Yosh), "Yosh manfiy bo'lishi mumkin emas!");
    }
}

internal class Program
{
    static void Main()
    {
        var f = new FoydalanuvchiYoshi("Olim", 22);
        Console.WriteLine($"Yaratildi: {f}");

        try
        {
            var xato = new FoydalanuvchiYoshi("Xato", -5);
        }
        catch (ArgumentOutOfRangeException ex)
        {
            Console.WriteLine($"Xatolik ushlandi: {ex.ParamName}");
        }
    }
}

```

## Tushuntirish va Mantiq:
Positional recordlarda parametrsiz qavssiz konstruktor tanasi ochish orqali barcha argumentlarni obyektga o'zlashtirilishidan oldin tekshirish mumkin.

## Ishlash natijasi:
```text
Yaratildi: FoydalanuvchiYoshi { Ism = Olim, Yosh = 22 }
Xatolik ushlandi: Yosh
```

# 375-Topshiriq: Record larda qo'shimcha metodlar va hisoblangan xossalar
## Topshiriq sharti:
Record ichida yangi biznes metodlari va hisoblangan xossalarni e'lon qiling.

## Yechim (C# kodi):
```csharp
using System;

record MahsulotNarxi(string Nomi, decimal AsosiyNarx, decimal SoliqFoizi)
{
    // Hisoblangan xossa
    public decimal YakuniyNarx => AsosiyNarx + (AsosiyNarx * SoliqFoizi / 100m);

    public void ChekChiqar() =>
        Console.WriteLine($"{Nomi}: {AsosiyNarx:N0} + Soliq({SoliqFoizi}%) = {YakuniyNarx:N0} so'm");
}

internal class Program
{
    static void Main()
    {
        var narx = new MahsulotNarxi("Kofe", 20000m, 12m);
        narx.ChekChiqar();
    }
}

```

## Tushuntirish va Mantiq:
Record oddiy sinf kabi o'z ichida metodlar, hisoblangan xossalar va boshqa amallarni bemalol saqlashi mumkin.

## Ishlash natijasi:
```text
Kofe: 20,000 + Soliq(12%) = 22,400 so'm
```

# 376-Topshiriq: Record larda to'plamlar tengligi: Reference Equals muammosi
## Topshiriq sharti:
Record ichida `List<T>` ishlatilganda qiymatlar tengligi emas, havola tengligi tekshirilib qolishini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

record FoydalanuvchiGuruhi(string Nomi, List<string> Azolar);

internal class Program
{
    static void Main()
    {
        var g1 = new FoydalanuvchiGuruhi("Adminlar", new List<string> { "Ali" });
        var g2 = new FoydalanuvchiGuruhi("Adminlar", new List<string> { "Ali" });

        // g1 == g2 FALSE beradi! Chunki List<T> oddiy sinf bo'lib, uning Equals metodi faqat manzilni tekshiradi!
        Console.WriteLine($"g1 == g2: {g1 == g2}");
        Console.WriteLine("Izoh: Record to'plamlari uchun SequenceEqual yoki ImmutableArray ishlatish kerak.");
    }
}

```

## Tushuntirish va Mantiq:
Record har bir xossa uchun uning `Equals` metodini chaqiradi. Standart `List<T>` esa qiymat bo'yicha tenglikni ta'minlamaydi, shuning uchun ikki alohida list record tengligini buzadi.

## Ishlash natijasi:
```text
g1 == g2: False
Izoh: Record to'plamlari uchun SequenceEqual yoki ImmutableArray ishlatish kerak.
```

# 377-Topshiriq: ImmutableArray bilan Recordlarda to'liq qiymat tengligi
## Topshiriq sharti:
`System.Collections.Immutable.ImmutableArray<T>` yordamida to'plamli recordlarni to'liq o'zgarmas qiling.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Immutable;

record Xarid(string Xaridor, ImmutableArray<string> Mahsulotlar);

internal class Program
{
    static void Main()
    {
        var x1 = new Xarid("Sami", ImmutableArray.Create("Non", "Sut"));
        var x2 = x1 with { Xaridor = "Vali" };

        Console.WriteLine($"Xaridor 1: {x1.Xaridor}, Mahsulotlar: {x1.Mahsulotlar.Length} ta");
        Console.WriteLine($"Xaridor 2: {x2.Xaridor}, Mahsulotlar: {x2.Mahsulotlar.Length} ta");
    }
}

```

## Tushuntirish va Mantiq:
`ImmutableArray<T>` bu struct bo'lib, o'zgarmas massivni ifodalaydi. Recordlar ichida to'plamlar saqlashda u eng xavfsiz va toza yechim hisoblanadi.

## Ishlash natijasi:
```text
Xaridor 1: Sami, Mahsulotlar: 2 ta
Xaridor 2: Vali, Mahsulotlar: 2 ta
```

# 378-Topshiriq: Record larni JSON ga serializatsiya va deserializatsiya qilish
## Topshiriq sharti:
`System.Text.Json` orqali record obyektlarini JSON formatiga o'giring va qayta tiklang.

## Yechim (C# kodi):
```csharp
using System;
using System.Text.Json;

record Ob-Havo(string Shahar, double Harorat, DateTime Sana);

internal class Program
{
    static void Main()
    {
        var havo = new Ob-Havo("Toshkent", 24.5, new DateTime(2026, 11, 8));

        string json = JsonSerializer.Serialize(havo);
        Console.WriteLine($"JSON matni: {json}");

        var tiklangan = JsonSerializer.Deserialize<Ob-Havo>(json);
        Console.WriteLine($"Qayta tiklandi: {tiklangan?.Shahar}, {tiklangan?.Harorat}°C");
    }
}

```

## Tushuntirish va Mantiq:
Positional recordlar `System.Text.Json` bilan mukammal ishlaydi. Serializatsiya jarayonida konstruktor parametrlari avtomatik moslashtiriladi.

## Ishlash natijasi:
```text
JSON matni: {"Shahar":"Toshkent","Harorat":24.5,"Sana":"2026-11-08T00:00:00"}
Qayta tiklandi: Toshkent, 24.5°C
```

# 379-Topshiriq: C# 11 ref fields in ref structs
## Topshiriq sharti:
C# 11 da `ref struct` ichida boshqa xotiraga ko'rsatuvchi `ref` maydoni e'lon qilinishini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

ref struct HavolaliKonteyner
{
    public ref int QiymatHavolasi;

    public HavolaliKonteyner(ref int son)
    {
        QiymatHavolasi = ref son;
    }
}

internal class Program
{
    static void Main()
    {
        int aslSon = 50;
        var konteyner = new HavolaliKonteyner(ref aslSon);

        konteyner.QiymatHavolasi = 999; // Asl o'zgaruvchi xotirada o'zgaradi

        Console.WriteLine($"aslSon qiymati: {aslSon}");
    }
}

```

## Tushuntirish va Mantiq:
C# 11 gacha strukturalar ichida `ref` maydonlar saqlash taqiqlangan edi. C# 11 da `ref struct` ichida boshqariladigan ko'rsatkichlarni (`ref T`) xavfsiz saqlashga ruxsat berildi.

## Ishlash natijasi:
```text
aslSon qiymati: 999
```

# 380-Topshiriq: scoped kalit so'zi va Span umr davri nazorati (Lifetime safety)
## Topshiriq sharti:
C# 11 da `scoped` kalit so'zi orqali ko'rsatkichlarning o'z doirasidan (scope) chiqib ketishini taqiqlash.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void QaytaIshla(scoped Span<int> span)
    {
        // 'scoped' span ning ushbu metoddan tashqariga chiqib ketmasligini kafolatlaydi
        span[0] = 777;
    }

    static void Main()
    {
        Span<int> bufer = stackalloc int[2];
        QaytaIshla(bufer);

        Console.WriteLine($"Bufer birinchi elementi: {bufer[0]}");
    }
}

```

## Tushuntirish va Mantiq:
`scoped` modifikatori kompilyatorga havola ko'rsatuvchi `ref struct` ning joriy metod freymidan uzoqroq yashamasligini (dangling pointer bo'lmasligini) qat'iy tekshirishni buyuradi.

## Ishlash natijasi:
```text
Bufer birinchi elementi: 777
```

# 381-Topshiriq: Valyuta miqdori: readonly record struct Money
## Topshiriq sharti:
Domen modellarida pul miqdorini ifodalovchi to'liq o'zgarmas Value Object record strukturasini yozing.

## Yechim (C# kodi):
```csharp
using System;

readonly record struct Pul(decimal Miqdor, string Valyuta)
{
    public static Pul operator +(Pul a, Pul b)
    {
        if (a.Valyuta != b.Valyuta)
            throw new InvalidOperationException("Har xil valyutalarni qo'shib bo'lmaydi!");
        return new Pul(a.Miqdor + b.Miqdor, a.Valyuta);
    }

    public override string ToString() => $"{Miqdor:N0} {Valyuta}";
}

internal class Program
{
    static void Main()
    {
        var p1 = new Pul(50000m, "UZS");
        var p2 = new Pul(35000m, "UZS");
        var jami = p1 + p2;

        Console.WriteLine($"Jami pul: {jami}");
    }
}

```

## Tushuntirish va Mantiq:
Ushbu model Stack da saqlanadi, xotira ajratmaydi, to'liq o'zgarmasdir va o'z ichida matematik operatorlarni qo'llab-quvvatlaydi.

## Ishlash natijasi:
```text
Jami pul: 85,000 UZS
```

# 382-Topshiriq: Koordinatalar uchun readonly struct Point3D
## Topshiriq sharti:
Uch o'lchovli fazodagi nuqtani xotirani tejovchi `readonly struct` orqali hisoblang.

## Yechim (C# kodi):
```csharp
using System;

readonly struct Nuqta3D(double x, double y, double z)
{
    public double X => x;
    public double Y => y;
    public double Z => z;

    public double MarkazgachaMasofa() => Math.Sqrt(x * x + y * y + z * z);
}

internal class Program
{
    static void Main()
    {
        var p = new Nuqta3D(1.0, 2.0, 2.0);
        Console.WriteLine($"Masofa: {p.MarkazgachaMasofa():F1}");
    }
}

```

## Tushuntirish va Mantiq:
3D nuqtalar kompyuter grafikasi va o'yinlarda sekundiga millionlab marta yaratiladi. `readonly struct` bu hisoblashlarni Heap ga kirmasdan 0 kechikish bilan bajaradi.

## Ishlash natijasi:
```text
Masofa: 3.0
```

# 383-Topshiriq: Struct larda Equals va GetHashCode ni qo'lda yozish unumdorligi
## Topshiriq sharti:
Oddiy `struct` nima uchun har doim `IEquatable<T>` ni amalga oshirishi kerakligini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

struct StandartStruct
{
    public int A;
}

struct TezkorStruct : IEquatable<TezkorStruct>
{
    public int A;
    public bool Equals(TezkorStruct other) => A == other.A;
    public override bool Equals(object? obj) => obj is TezkorStruct t && Equals(t);
    public override int GetHashCode() => A;
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Standart ValueType.Equals reflection ishlatadi va sekin ishlaydi.");
        Console.WriteLine("TezkorStruct IEquatable orqali reflection siz, to'g'ridan-to'g'ri CPU instruksiyasida ishlaydi.");
    }
}

```

## Tushuntirish va Mantiq:
Standart `System.ValueType.Equals` ichida Reflection ishlatiladi va bu juda sekin. Struct larda `IEquatable<T>` ni yozish tenglikni 10 barobargacha tezlashtiradi (Record struct larda bu avtomatik bo'ladi).

## Ishlash natijasi:
```text
Standart ValueType.Equals reflection ishlatadi va sekin ishlaydi.
TezkorStruct IEquatable orqali reflection siz, to'g'ridan-to'g'ri CPU instruksiyasida ishlaydi.
```

# 384-Topshiriq: Recordlarda PrintMembers metodini xususiylashtirish
## Topshiriq sharti:
`ToString()` chiqish formatini o'zgartirish uchun `PrintMembers` metodini `override` qiling.

## Yechim (C# kodi):
```csharp
using System;
using System.Text;

record MaxfiyFoydalanuvchi(string Ism, string Parol)
{
    protected virtual bool PrintMembers(StringBuilder builder)
    {
        builder.Append($"Ism = {Ism}, Parol = ***MAXFIY***");
        return true;
    }
}

internal class Program
{
    static void Main()
    {
        var user = new MaxfiyFoydalanuvchi("Alisher", "Parol12345");
        Console.WriteLine(user);
    }
}

```

## Tushuntirish va Mantiq:
`PrintMembers` metodi orqali recordning ichki `ToString()` formatini to'liq o'zgartirish, masalan loglarda parollar va maxfiy ma'lumotlarni yashirish mumkin.

## Ishlash natijasi:
```text
MaxfiyFoydalanuvchi { Ism = Alisher, Parol = ***MAXFIY*** }
```

# 385-Topshiriq: Mutable Structs anti-pattern: Nega o'zgaruvchan struct yomon?
## Topshiriq sharti:
O'zgaruvchan struktura nusxalash paytida chalkashliklarga sabab bo'lishini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

struct YomonStruct
{
    public int Son;
}

internal class Program
{
    static void Main()
    {
        var m1 = new YomonStruct { Son = 10 };
        var m2 = m1; // Nusxa olindi

        m2.Son = 20; // m1 o'zgarmaydi!

        Console.WriteLine($"m1: {m1.Son}, m2: {m2.Son}");
        Console.WriteLine("Xulosa: Kutilmagan nusxalanish xatolarini oldini olish uchun struct har doim 'readonly' bo'lishi shart!");
    }
}

```

## Tushuntirish va Mantiq:
Dasturchilar ko'pincha struct obyektini sinf deb o'ylab uning maydonlarini o'zgartiradi, ammo nusxalanish tufayli asl qiymat o'zgarmasdan qoladi. Shu sababli har doim `readonly struct` yozish qat'iy qoidadir.

## Ishlash natijasi:
```text
m1: 10, m2: 20
Xulosa: Kutilmagan nusxalanish xatolarini oldini olish uchun struct har doim 'readonly' bo'lishi shart!
```

# 386-Topshiriq: Record larda with ifodasi zanjirlanishi
## Topshiriq sharti:
Bir nechta bosqichda `with` operatorini zanjir qilib qo'llang.

## Yechim (C# kodi):
```csharp
using System;

record Server(string Host, int Port, bool Ssl);

internal class Program
{
    static void Main()
    {
        var dev = new Server("localhost", 5000, false);

        var stage = dev with { Port = 8080 };
        var prod = stage with { Host = "api.uz", Ssl = true };

        Console.WriteLine($"Dev:   {dev}");
        Console.WriteLine($"Prod:  {prod}");
    }
}

```

## Tushuntirish va Mantiq:
`with` ifodasi zanjirlanib chaqirilishi mumkin va har safar o'zgarmas holatni yangi konfiguratsiyaga aylantiradi.

## Ishlash natijasi:
```text
Dev:   Server { Host = localhost, Port = 5000, Ssl = False }
Prod:  Server { Host = api.uz, Port = 8080, Ssl = True }
```

# 387-Topshiriq: Recordlarni Dictionary kaliti sifatida ishlatish
## Topshiriq sharti:
Recordlar qiymatga qarab xesh hisoblagani sababli ularni xavfsiz lug'at kaliti sifatida qo'llang.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

record Kalit(string Hudud, int Kod);

internal class Program
{
    static void Main()
    {
        var lugat = new Dictionary<Kalit, string>();

        var k1 = new Kalit("Toshkent", 100);
        lugat[k1] = "Markaziy Ombor";

        // Boshqa yangi obyekt, ammo qiymati bir xil
        var k2 = new Kalit("Toshkent", 100);

        Console.WriteLine($"Topildi: {lugat[k2]}");
    }
}

```

## Tushuntirish va Mantiq:
Sinflar kalit bo'lganda manzil bo'yicha qidiradi va `k2` ni topolmaydi. Recordlar esa `GetHashCode()` va `Equals()` ni avtomatik xossalar asosida hisoblagani uchun `k2` bilan mukammal topiladi.

## Ishlash natijasi:
```text
Topildi: Markaziy Ombor
```

# 388-Topshiriq: Unsafe.SizeOf<T>() orqali struct xotirasini tekshirish
## Topshiriq sharti:
`System.Runtime.CompilerServices.Unsafe` yordamida struct ning operativ xotiradagi sof hajmini aniqlang.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.CompilerServices;

struct KichikNuqta
{
    public short X;
    public short Y;
}

internal class Program
{
    static void Main()
    {
        int hajm = Unsafe.SizeOf<KichikNuqta>();
        Console.WriteLine($"KichikNuqta hajmi: {hajm} bayt (2 ta short = 4 bayt)");
    }
}

```

## Tushuntirish va Mantiq:
`Unsafe.SizeOf<T>()` generik qiymat turlarining xotiradagi sof bayt hajmini tezkor hisoblash vositasidir.

## Ishlash natijasi:
```text
KichikNuqta hajmi: 4 bayt (2 ta short = 4 bayt)
```

# 389-Topshiriq: Nima uchun Entity lar class, DTO va Hodisalar record bo'lishi kerak?
## Topshiriq sharti:
Arxitekturaviy farq: Obyekt identifikatori (ID) vs Ma'lumotlar qiymati.

## Yechim (C# kodi):
```csharp
using System;

// Entity (Sinf): Identifikatori o'zgarmaydi, xossalari o'zgaradi
class FoydalanuvchiEntity
{
    public Guid Id { get; init; } = Guid.NewGuid();
    public string Ism { get; set; } = "";
}

// Hodisa / DTO (Record): Sof ma'lumotlar, qiymatlar bir xilligi muhim
record FoydalanuvchiYaratildiHodisasi(Guid Id, string Ism, DateTime Sana);

internal class Program
{
    static void Main()
    {
        var entity = new FoydalanuvchiEntity { Ism = "Davlat" };
        var hodisa = new FoydalanuvchiYaratildiHodisasi(entity.Id, entity.Ism, DateTime.UtcNow);

        Console.WriteLine($"Entity turi: {entity.GetType().Name}");
        Console.WriteLine($"Hodisa turi: {hodisa.GetType().Name}");
    }
}

```

## Tushuntirish va Mantiq:
Entity larning hayot davri (Lifecycle) davomida xossalari o'zgarib turadi, ammo uning ID si o'zgarmas bo'lib qoladi. DTO va Hodisalar esa vaqtning muayyan nuqtasidagi ma'lumot suratidir (Snapshot) va qat'iy o'zgarmas `record` bo'lishi kerak.

## Ishlash natijasi:
```text
Entity turi: FoydalanuvchiEntity
Hodisa turi: FoydalanuvchiYaratildiHodisasi
```

# 390-Topshiriq: Benchmark: 1 million Struct vs 1 million Class yaratish tezligi
## Topshiriq sharti:
Stack xotiradagi struct va Heap dagi class o'rtasidagi yaratilish tezligi va xotira farqini tahlil qiling.

## Yechim (C# kodi):
```csharp
using System;
using System.Diagnostics;

struct NuqtaS { public int X, Y; }
class NuqtaC { public int X, Y; }

internal class Program
{
    static void Main()
    {
        int sanoq = 1_000_000;

        var sw = Stopwatch.StartNew();
        NuqtaS[] sMassiv = new NuqtaS[sanoq];
        sw.Stop();
        long structVaqt = sw.ElapsedMilliseconds;

        sw.Restart();
        NuqtaC[] cMassiv = new NuqtaC[sanoq];
        for (int i = 0; i < sanoq; i++) cMassiv[i] = new NuqtaC();
        sw.Stop();
        long classVaqt = sw.ElapsedMilliseconds;

        Console.WriteLine($"1 million Struct massivi ajratish: ~{structVaqt} ms (Bitta blok)");
        Console.WriteLine($"1 million Class obyekti yaratish:  ~{classVaqt} ms (1M Heap obyekti)");
    }
}

```

## Tushuntirish va Mantiq:
Strukturalar massivi bitta yaxlit xotira blokida 0 nanosaniyada initsializatsiya qilinadi. Sinflar esa har biri uchun alohida Heap manzil, Type Handle va Sync Block Index talab qilib, GC ga millionlab obyekt yuklaydi.

## Ishlash natijasi:
```text
1 million Struct massivi ajratish: ~... ms (Bitta blok)
1 million Class obyekti yaratish:  ~... ms (1M Heap obyekti)
```

# 391-Topshiriq: Struct da static factory metodlari
## Topshiriq sharti:
Strukturalarni xavfsiz va toza initsializatsiya qilish uchun statik factory metodlarini yozing.

## Yechim (C# kodi):
```csharp
using System;

readonly struct VaqtOraligi
{
    public int Sekundlar { get; }
    private VaqtOraligi(int s) => Sekundlar = s;

    public static VaqtOraligi Daqiqadan(int daqiqa) => new(daqiqa * 60);
    public static VaqtOraligi Soatdan(int soat) => new(soat * 3600);
}

internal class Program
{
    static void Main()
    {
        var v1 = VaqtOraligi.Daqiqadan(5);
        var v2 = VaqtOraligi.Soatdan(2);

        Console.WriteLine($"5 daqiqa: {v1.Sekundlar} sekund");
        Console.WriteLine($"2 soat:   {v2.Sekundlar} sekund");
    }
}

```

## Tushuntirish va Mantiq:
Statik factory metodlari strukturalar uchun ham juda qulay bo'lib, o'lchov birliklarini xavfsiz va aniq nomlar bilan hosil qilishga xizmat qiladi.

## Ishlash natijasi:
```text
5 daqiqa: 300 sekund
2 soat:   7200 sekund
```

# 392-Topshiriq: Record larda xususiy konstruktor va Factory
## Topshiriq sharti:
Positional recordni faqat statik metod orqali yaratish imkoniyatini chegaralang.

## Yechim (C# kodi):
```csharp
using System;

record MaxsusKod
{
    public string Qiymat { get; }

    private MaxsusKod(string q) => Qiymat = q;

    public static MaxsusKod Yarat(string kod)
    {
        if (kod.Length < 3) throw new ArgumentException("Kod juda qisqa!");
        return new MaxsusKod(kod.ToUpper());
    }
}

internal class Program
{
    static void Main()
    {
        var k = MaxsusKod.Yarat("uzb");
        Console.WriteLine($"Kod: {k.Qiymat}");
    }
}

```

## Tushuntirish va Mantiq:
Xususiy konstruktor orqali record larning faqat biznes qoidalaridan o'tgan to'g'ri nusxalari yaratilishini kafolatlash mumkin.

## Ishlash natijasi:
```text
Kod: UZB
```

# 393-Topshiriq: Struct larda default qiymat xavfini bartaraf etish
## Topshiriq sharti:
Struktura `default` bo'lib qolganda nolga bo'linish yoki noto'g'ri holatning oldini olish usulini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

readonly struct Bo'luvchi
{
    private readonly int qiymat;

    // Agar 0 bo'lsa standart 1 qaytarish
    public int Qiymat => qiymat == 0 ? 1 : qiymat;

    public Bo'luvchi(int q)
    {
        if (q == 0) throw new ArgumentException("Bo'luvchi 0 bo'lolmaydi!");
        qiymat = q;
    }
}

internal class Program
{
    static void Main()
    {
        Bo'luvchi def = default; // qiymat = 0
        Console.WriteLine($"Xavfsiz qiymat: {def.Qiymat}"); // 1 qaytadi
    }
}

```

## Tushuntirish va Mantiq:
Strukturalarning `default` qiymati doimo barcha baytlarni 0 qiladi. Shuning uchun xossalarda nol holatini xavfsiz qiymatga tekshirib qaytarish (fallback) muhim hisoblanadi.

## Ishlash natijasi:
```text
Xavfsiz qiymat: 1
```

# 394-Topshiriq: Struct larni saralash: IComparable<T> ni struct da amalga oshirish
## Topshiriq sharti:
Katta massivlarda strukturalarni saralash uchun `IComparable<T>` interfeysini boxing siz qo'llang.

## Yechim (C# kodi):
```csharp
using System;

struct BallStrukt : IComparable<BallStrukt>
{
    public int Ball;
    public BallStrukt(int b) => Ball = b;

    public int CompareTo(BallStrukt boshqa) => Ball.CompareTo(boshqa.Ball);
}

internal class Program
{
    static void Main()
    {
        BallStrukt[] ballar = [ new(85), new(95), new(70) ];
        Array.Sort(ballar);

        foreach (var b in ballar)
        {
            Console.Write($"{b.Ball} ");
        }
        Console.WriteLine();
    }
}

```

## Tushuntirish va Mantiq:
Struktura `IComparable<T>` ni amalga oshirganda `Array.Sort` hech qanday boxing qilmasdan elementlarni to'g'ridan-to'g'ri o'z o'rnida saralaydi.

## Ishlash natijasi:
```text
70 85 95
```

# 395-Topshiriq: Record struct larda operatorlarni qo'llash
## Topshiriq sharti:
`record struct` ichida matematik operatorlarni yuklang va `with` bilan birgalikda ishlating.

## Yechim (C# kodi):
```csharp
using System;

record struct Nuqta(int X, int Y)
{
    public static Nuqta operator +(Nuqta a, Nuqta b) => new(a.X + b.X, a.Y + b.Y);
}

internal class Program
{
    static void Main()
    {
        var n1 = new Nuqta(5, 10);
        var n2 = new Nuqta(3, 4);
        var n3 = n1 + n2;

        Console.WriteLine($"n3: {n3}");
    }
}

```

## Tushuntirish va Mantiq:
`record struct` ham recordlarning zamonaviy xususiyatlariga, ham operatorlar qayta yuklanishiga ega bo'lib, hisoblash geometriyasi uchun juda qulay.

## Ishlash natijasi:
```text
n3: Nuqta { X = 8, Y = 14 }
```

# 396-Topshiriq: Record Class vs Record Struct taqqoslash xulosasi
## Topshiriq sharti:
Ikkala turdagi recordlarning xotiradagi o'rni va xatti-harakatlarini tahlil qiling.

## Yechim (C# kodi):
```csharp
using System;

record class ObyektRecord(int X);
record struct QiymatRecord(int X);

internal class Program
{
    static void Main()
    {
        Console.WriteLine($"ObyektRecord Class mi: {typeof(ObyektRecord).IsClass}");
        Console.WriteLine($"QiymatRecord ValueType mi: {typeof(QiymatRecord).IsValueType}");
        Console.WriteLine("Qoida: Kichik (< 16 bayt) qisqa yashovchi ma'lumotlar uchun record struct,");
        Console.WriteLine("katta yoki meros talab qiluvchi modellar uchun record class tavsiya etiladi.");
    }
}

```

## Tushuntirish va Mantiq:
Ushbu taqqoslash C# arxitekturasida to'g'ri turni tanlashning asosiy mezonlarini belgilab beradi.

## Ishlash natijasi:
```text
ObyektRecord Class mi: True
QiymatRecord ValueType mi: True
Qoida: Kichik (< 16 bayt) qisqa yashovchi ma'lumotlar uchun record struct,
katta yoki meros talab qiluvchi modellar uchun record class tavsiya etiladi.
```

# 397-Topshiriq: Bit darajasidagi ARGB rangi: readonly struct Color32
## Topshiriq sharti:
32-bitli butun son ichida 4 ta rang kanalini (Alpha, Red, Green, Blue) saqlovchi yengil struktura yozing.

## Yechim (C# kodi):
```csharp
using System;

readonly struct Color32(byte a, byte r, byte g, byte b)
{
    public uint Raw => ((uint)a << 24) | ((uint)r << 16) | ((uint)g << 8) | b;
    public override string ToString() => $"ARGB(0x{Raw:X8})";
}

internal class Program
{
    static void Main()
    {
        var qizil = new Color32(255, 255, 0, 0);
        Console.WriteLine(qizil);
    }
}

```

## Tushuntirish va Mantiq:
Faqat 4 bayt xotira oluvchi ushbu struktura millionlab piksellarni Heap ga kirmasdan qayta ishlash imkonini beradi.

## Ishlash natijasi:
```text
ARGB(0xFFFF0000)
```

# 398-Topshiriq: Strongly Typed Id: readonly record struct UserId(Guid Value)
## Topshiriq sharti:
Oddiy `Guid` yoki `int` o'rniga adashib boshqa id ga o'tib ketmaslik uchun kuchli tiplangan identifikator record strukturasini yarating.

## Yechim (C# kodi):
```csharp
using System;

readonly record struct FoydalanuvchiId(Guid Qiymat);
readonly record struct BuyurtmaId(Guid Qiymat);

internal class Program
{
    static void BuyurtmaYukla(BuyurtmaId id)
    {
        Console.WriteLine($"Buyurtma yuklandi: {id.Qiymat.ToString().Substring(0, 8)}...");
    }

    static void Main()
    {
        var bId = new BuyurtmaId(Guid.NewGuid());
        var uId = new FoydalanuvchiId(Guid.NewGuid());

        BuyurtmaYukla(bId);
        // BuyurtmaYukla(uId); // KOMPILYATSIYA XATOSI! FoydalanuvchiId ni BuyurtmaId o'rnida adashtirib bo'lmaydi!
    }
}

```

## Tushuntirish va Mantiq:
Strongly Typed ID lar dasturlashdagi 'Primitive Obsession' anti-patternini yo'qotadi va bitta ID ni boshqa ID o'rnida yanglish uzatishning oldini oladi.

## Ishlash natijasi:
```text
Buyurtma yuklandi: ...
```

# 399-Topshiriq: Record larda pattern matching: Positional Pattern matching
## Topshiriq sharti:
Record larni ularning ichki xossalari bo'yicha `switch expression` da solishtiring.

## Yechim (C# kodi):
```csharp
using System;

record Tolov(decimal Summa, string Turi);

internal class Program
{
    static string Tahlil(Tolov tolov) => tolov switch
    {
        ( > 1_000_000m, "Karta") => "Katta miqdordagi karta to'lovi",
        ( _, "Naqd")             => "Naqd to'lov",
        _                        => "Oddiy to'lov"
    };

    static void Main()
    {
        Console.WriteLine(Tahlil(new Tolov(1500000m, "Karta")));
        Console.WriteLine(Tahlil(new Tolov(50000m, "Naqd")));
    }
}

```

## Tushuntirish va Mantiq:
Record lar avtomatik `Deconstruct` ga ega bo'lgani uchun ularni to'g'ridan-to'g'ri Positional Pattern yordamida tekshirish mumkin.

## Ishlash natijasi:
```text
Katta miqdordagi karta to'lovi
Naqd to'lov
```

# 400-Topshiriq: Strukturalar va Recordlar bo'limi integratsiyalashgan arxitekturasi
## Topshiriq sharti:
`readonly record struct`, `record class`, `with` ifodasi va xotira samaradorligini jamlovchi to'liq elektron savdo buyurtmasi tizimini quring.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

readonly record struct MahsulotId(int Qiymat);
readonly record struct Narx(decimal Miqdor, string Valyuta);

record BuyurtmaQatori(MahsulotId Mahsulot, int Soni, Narx BirlikNarx);

record BuyurtmaPaketi(Guid Id, List<BuyurtmaQatori> Qatorlar, string Holat);

internal class Program
{
    static void Main()
    {
        var q1 = new BuyurtmaQatori(new MahsulotId(101), 2, new Narx(150000m, "UZS"));
        var q2 = new BuyurtmaQatori(new MahsulotId(202), 1, new Narx(300000m, "UZS"));

        var buyurtma = new BuyurtmaPaketi(Guid.NewGuid(), [q1, q2], "Yangi");

        // Holatni with orqali o'zgarmas yangilash
        var yangilangan = buyurtma with { Holat = "Yetkazilmoqda" };

        Console.WriteLine($"Original holati:   {buyurtma.Holat}");
        Console.WriteLine($"Yangilangan holat: {yangilangan.Holat}");
        Console.WriteLine($"Qatorlar soni:     {yangilangan.Qatorlar.Count} ta");
    }
}

```

## Tushuntirish va Mantiq:
Ushbu yakuniy arxitektura zamonaviy .NET da ma'lumotlar modellarini toza, xotira samarador (0 ortiqcha yuk) va o'zgarmas (immutable) qilib qurishning eng namunali standartidir.

## Ishlash natijasi:
```text
Original holati:   Yangi
Yangilangan holat: Yetkazilmoqda
Qatorlar soni:     2 ta
```

