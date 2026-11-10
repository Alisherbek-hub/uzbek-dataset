# 7-Mavzu: Interfeyslar va Abstraksiya (301-350)

Ushbu bo'limda C# tilida abstraksiya va shartnomaga asoslangan dasturlash: interfeyslar (`interface`), ko'p interfeysli implementatsiya, oshkora (explicit) interfeys realizatsiyasi, C# 8 Default Interface Methods, C# 11 Static Abstract a'zolar va Generic Math (`INumber<T>`), standart .NET interfeyslari (`IComparable<T>`, `IEquatable<T>`, `IDisposable`, `IAsyncDisposable`), Interface Segregation Principle (ISP), Dependency Injection tayyorgarligi hamda mashhur arxitektura naqshlari (Repository, Adapter, Decorator) bo'yicha 50 ta amaliy topshiriq keltirilgan.

# 301-Topshiriq: Interfeys e'lon qilish va shartnoma (Contract) tushunchasi
## Topshiriq sharti:
Xabar yetkazish shartnomasini ifodalovchi `IXabarYetkazuvchi` interfeysini e'lon qiling va uni sinfda bajaring.

## Yechim (C# kodi):
```csharp
using System;

interface IXabarYetkazuvchi
{
    void Yubor(string qabulQiluvchi, string matn);
}

class EmailXizmati : IXabarYetkazuvchi
{
    public void Yubor(string email, string matn)
    {
        Console.WriteLine($"Email yuborildi: [{email}] -> {matn}");
    }
}

internal class Program
{
    static void Main()
    {
        IXabarYetkazuvchi xizmat = new EmailXizmati();
        xizmat.Yubor("mijoz@domen.uz", "Buyurtmangiz yo'lga chiqdi.");
    }
}

```

## Tushuntirish va Mantiq:
Interfeys shartnomadir (Contract). U sinf nima qilishi kerakligini belgilaydi, ammo uni qanday bajarishni sinfning o'ziga qoldiradi. Interfeys a'zolari standart holatda `public abstract` hisoblanadi va nomlari an'anaga ko'ra `I` harfi bilan boshlanadi.

## Ishlash natijasi:
```text
Email yuborildi: [mijoz@domen.uz] -> Buyurtmangiz yo'lga chiqdi.
```

# 302-Topshiriq: Bir nechta interfeysni amalga oshirish (Multiple Interfaces)
## Topshiriq sharti:
Bitta sinfda ikkita mustaqil interfeysni (`IOqiladigan` va `IYoziladigan`) bir vaqtda amalga oshiring.

## Yechim (C# kodi):
```csharp
using System;

interface IOqiladigan
{
    string Oqi();
}

interface IYoziladigan
{
    void Yoz(string malumot);
}

class XotiraHujjati : IOqiladigan, IYoziladigan
{
    private string matn = "";

    public string Oqi() => matn;
    public void Yoz(string malumot) => matn = malumot;
}

internal class Program
{
    static void Main()
    {
        var hujjat = new XotiraHujjati();
        hujjat.Yoz("Muhim ma'lumot");

        Console.WriteLine($"O'qilgan matn: {hujjat.Oqi()}");
    }
}

```

## Tushuntirish va Mantiq:
C# da sinflardan faqat bitta meros olish mumkin bo'lsa-da, interfeyslarni cheksiz miqdorda amalga oshirish mumkin. Bu xavfsiz ko'p merosxo'rlikning yagona rasmiy mexanizmidir.

## Ishlash natijasi:
```text
O'qilgan matn: Muhim ma'lumot
```

# 303-Topshiriq: Oshkora interfeys implementatsiyasi (Explicit Interface Implementation)
## Topshiriq sharti:
Ikkita interfeysda bir xil nomli metod bo'lganda to'qnashuvni Explicit usulda yeching.

## Yechim (C# kodi):
```csharp
using System;

interface IAdminPanel
{
    void Kirish();
}

interface IFoydalanuvchiPanel
{
    void Kirish();
}

class TizimXizmati : IAdminPanel, IFoydalanuvchiPanel
{
    // Explicit implementatsiya: public yozilmaydi, interfeys nomi bilan ko'rsatiladi
    void IAdminPanel.Kirish() => Console.WriteLine("Admin paneliga kirildi (To'liq huquq).");
    void IFoydalanuvchiPanel.Kirish() => Console.WriteLine("Foydalanuvchi paneliga kirildi (Cheklangan).");
}

internal class Program
{
    static void Main()
    {
        var xizmat = new TizimXizmati();

        // xizmat.Kirish(); // XATO! Bevosita sinf orqali chaqirib bo'lmaydi

        IAdminPanel admin = xizmat;
        admin.Kirish();

        IFoydalanuvchiPanel user = xizmat;
        user.Kirish();
    }
}

```

## Tushuntirish va Mantiq:
Explicit interfeys implementatsiyasida metodlar faqat tegishli interfeys havolasi orqali ko'rinadi (`IAdminPanel admin = ...`). Bu nomlar to'qnashuvini (Name Collision) bartaraf etadi va sinfning ochiq API sini toza saqlaydi.

## Ishlash natijasi:
```text
Admin paneliga kirildi (To'liq huquq).
Foydalanuvchi paneliga kirildi (Cheklangan).
```

# 304-Topshiriq: C# 8 Standart interfeys metodlari (Default Interface Methods)
## Topshiriq sharti:
Interfeys ichida standart metod tanasini (Default implementation) yozing.

## Yechim (C# kodi):
```csharp
using System;

interface ILogger
{
    void Log(string xabar);

    // C# 8 Default Interface Method: Agar sinf yozmasa, ushbu standart kod ishlaydi
    void LogXato(string xato) => Log($"[XATOLIK]: {xato}");
}

class KonsolLogger : ILogger
{
    public void Log(string xabar) => Console.WriteLine(xabar);
    // LogXato ni yozish majburiy emas, standart tanasi bor
}

internal class Program
{
    static void Main()
    {
        ILogger logger = new KonsolLogger();
        logger.Log("Oddiy operatsiya");
        logger.LogXato("Ulanish uzildi");
    }
}

```

## Tushuntirish va Mantiq:
Default Interface Methods C# 8 da kiritilgan bo'lib, mavjud interfeyslarga yangi metod qo'shilganda uning barcha voris sinflarini sindirib yubormaslik (Binary backward compatibility) uchun xizmat qiladi.

## Ishlash natijasi:
```text
Oddiy operatsiya
[XATOLIK]: Ulanish uzildi
```

# 305-Topshiriq: C# 11 Static Abstract a'zolar interfeyslarda
## Topshiriq sharti:
Interfeysda `static abstract` metodi e'lon qilib, uni amalga oshiruvchi sinflarda statik metod mavjudligini majburlang.

## Yechim (C# kodi):
```csharp
using System;

interface IIdentifikatorli<TSelf>
{
    static abstract TSelf Yarat(int id);
}

class Mahsulot : IIdentifikatorli<Mahsulot>
{
    public int Id { get; }
    private Mahsulot(int id) => Id = id;

    // Interfeys talab qilgan statik metod
    public static Mahsulot Yarat(int id) => new Mahsulot(id);
}

internal class Program
{
    static T Ob'yektYarat<T>(int id) where T : IIdentifikatorli<T>
    {
        return T.Yarat(id); // Generik parametr orqali statik metodni chaqirish!
    }

    static void Main()
    {
        Mahsulot m = Ob'yektYarat<Mahsulot>(101);
        Console.WriteLine($"Mahsulot Id: {m.Id}");
    }
}

```

## Tushuntirish va Mantiq:
C# 11 ning inqilobiy yangiliklaridan biri bu `static abstract` metodlardir. Ular generik turlar ustida bevosita statik metodlarni (masalan `T.Yarat()`, `T.Parse()`) chaqirishga ruxsat beradi.

## Ishlash natijasi:
```text
Mahsulot Id: 101
```

# 306-Topshiriq: C# 11 Generic Math va INumber<T> interfeysi
## Topshiriq sharti:
Barcha sonli turlar (`int`, `double`, `decimal`) bilan bir xil ishlovchi umumiy arifmetik metod yozing.

## Yechim (C# kodi):
```csharp
using System;
using System.Numerics;

internal class Program
{
    // T har qanday sonli tur bo'lishi mumkin (int, double, float, decimal)
    static T YigindiHisobla<T>(T a, T b) where T : INumber<T>
    {
        return a + b; // '+' operatori INumber orqali kafolatlangan!
    }

    static void Main()
    {
        Console.WriteLine($"int yig'indisi: {YigindiHisobla(10, 20)}");
        Console.WriteLine($"double yig'indisi: {YigindiHisobla(3.5, 2.1)}");
        Console.WriteLine($"decimal yig'indisi: {YigindiHisobla(100.50m, 200.25m)}");
    }
}

```

## Tushuntirish va Mantiq:
`INumber<T>` .NET 7/8 da kiritilgan bo'lib, statik abstrakt operatorlar (`+`, `-`, `*`, `/`) orqali har xil son turlari uchun bitta universal generik kod yozish imkonini yaratdi.

## Ishlash natijasi:
```text
int yig'indisi: 30
double yig'indisi: 5.6
decimal yig'indisi: 300.75
```

# 307-Topshiriq: IComparable<T>: Obyektlarni tabiiy saralash shartnomasi
## Topshiriq sharti:
`IComparable<Talaba>` interfeysini amalga oshirib, talabalarni ballari bo'yicha avtomatik saralanadigan qiling.

## Yechim (C# kodi):
```csharp
using System;

class Talaba : IComparable<Talaba>
{
    public string Ism { get; }
    public double Ball { get; }

    public Talaba(string ism, double ball) => (Ism, Ball) = (ism, ball);

    public int CompareTo(Talaba? boshqa)
    {
        if (boshqa == null) return 1;
        return Ball.CompareTo(boshqa.Ball); // Ball bo'yicha o'sish tartibida
    }
}

internal class Program
{
    static void Main()
    {
        Talaba[] guruh = [
            new Talaba("Zohid", 75.5),
            new Talaba("Anvar", 92.0),
            new Talaba("Malika", 84.0)
        ];

        Array.Sort(guruh); // IComparable<Talaba> orqali avtomatik saralanadi

        Console.WriteLine("Saralangan talabalar:");
        foreach (var t in guruh)
        {
            Console.WriteLine($"- {t.Ism}: {t.Ball}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`IComparable<T>.CompareTo(T other)` metodi: joriy obyekt kichik bo'lsa manfiy, teng bo'lsa 0, katta bo'lsa musbat son qaytarishi kerak. `Array.Sort` va `List.Sort` ushbu metodga tayanadi.

## Ishlash natijasi:
```text
Saralangan talabalar:
- Zohid: 75.5
- Malika: 84
- Anvar: 92
```

# 308-Topshiriq: IComparer<T>: Maxsus saralash qoidalari (Custom Comparer)
## Topshiriq sharti:
Obyekt sinfini o'zgartirmasdan, tashqaridan ism bo'yicha teskari saralovchi alohida komparator sinfini yozing.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

class Xodim
{
    public string Ism { get; set; } = "";
    public int Yosh { get; set; }
}

class IsmBoyichaTeskari : IComparer<Xodim>
{
    public int Compare(Xodim? x, Xodim? y)
    {
        if (x == null || y == null) return 0;
        return string.Compare(y.Ism, x.Ism, StringComparison.Ordinal); // Teskari tartib
    }
}

internal class Program
{
    static void Main()
    {
        Xodim[] xodimlar = [
            new Xodim { Ism = "Bobur", Yosh = 30 },
            new Xodim { Ism = "Zafar", Yosh = 25 },
            new Xodim { Ism = "Dilshod", Yosh = 28 }
        ];

        Array.Sort(xodimlar, new IsmBoyichaTeskari());

        foreach (var x in xodimlar)
        {
            Console.WriteLine($"{x.Ism} ({x.Yosh} yosh)");
        }
    }
}

```

## Tushuntirish va Mantiq:
`IComparer<T>` alohida saralash strategiyalarini belgilash uchun xizmat qiladi. Bitta sinf uchun xohlagancha turli komparatorlar (Ism bo'yicha, Yosh bo'yicha, Maosh bo'yicha) yaratish mumkin.

## Ishlash natijasi:
```text
Zafar (25 yosh)
Dilshod (28 yosh)
Bobur (30 yosh)
```

# 309-Topshiriq: IEquatable<T>: Boxing siz yuqori tezlikdagi tenglik
## Topshiriq sharti:
`IEquatable<T>` orqali struct va class larda boxing bo'lmasdan `Equals(T)` chaqirilishini ta'minlang.

## Yechim (C# kodi):
```csharp
using System;

class MahsulotKodi : IEquatable<MahsulotKodi>
{
    public string Kod { get; }
    public MahsulotKodi(string kod) => Kod = kod;

    // IEquatable<T> ning kuchli tiplangan metodi
    public bool Equals(MahsulotKodi? boshqa)
    {
        if (boshqa is null) return false;
        return Kod == boshqa.Kod;
    }

    public override bool Equals(object? obj) => Equals(obj as MahsulotKodi);
    public override int GetHashCode() => Kod.GetHashCode();
}

internal class Program
{
    static void Main()
    {
        var k1 = new MahsulotKodi("PRD-100");
        var k2 = new MahsulotKodi("PRD-100");

        Console.WriteLine($"k1.Equals(k2): {k1.Equals(k2)}");
    }
}

```

## Tushuntirish va Mantiq:
Standart `object.Equals(object)` qiymat turlarida Boxing (Stack dan Heap ga ko'chirish) keltirib chiqaradi. `IEquatable<T>` esa to'g'ridan-to'g'ri `T` turini qabul qilib, boxing overhead ni butunlay yo'qotadi.

## Ishlash natijasi:
```text
k1.Equals(k2): True
```

# 310-Topshiriq: IEqualityComparer<T>: Dictionary va HashSet uchun maxsus xesh qoidalari
## Topshiriq sharti:
Katta-kichik harflarni inkor qiluvchi maxsus `IEqualityComparer<string>` bilan `HashSet` yarating.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

class HarfSezmasTaqqoslagich : IEqualityComparer<string>
{
    public bool Equals(string? x, string? y) =>
        string.Equals(x, y, StringComparison.OrdinalIgnoreCase);

    public int GetHashCode(string obj) =>
        obj.ToLowerInvariant().GetHashCode();
}

internal class Program
{
    static void Main()
    {
        var royxat = new HashSet<string>(new HarfSezmasTaqqoslagich());
        royxat.Add("TOSHKENT");
        royxat.Add("toshkent"); // Qaytadan qo'shilmaydi!

        Console.WriteLine($"HashSet dagi elementlar soni: {royxat.Count}");
    }
}

```

## Tushuntirish va Mantiq:
`IEqualityComparer<T>` to'plamlarga elementlarni qanday qilib unikal deb hisoblash kerakligini o'rgatadi. U orqali dublikatlarni aniqlash logikasini erkin o'zgartirish mumkin.

## Ishlash natijasi:
```text
HashSet dagi elementlar soni: 1
```

# 311-Topshiriq: IDisposable va using bayonoti: Resurslarni kafolatli tozalash
## Topshiriq sharti:
`IDisposable` interfeysini amalga oshirib, fayl yoki tarmoq resursini `using` bloki orqali tozalashni ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

class BoshqarilmaydiganResurs : IDisposable
{
    public void Amaliyot() => Console.WriteLine("Resurs bilan xavfsiz ish bajarildi.");

    public void Dispose()
    {
        Console.WriteLine("Dispose chaqirildi: Resurs to'liq yopildi va xotiradan bo'shatildi.");
    }
}

internal class Program
{
    static void Main()
    {
        using (var res = new BoshqarilmaydiganResurs())
        {
            res.Amaliyot();
        } // Chiqish paytida avtomatik res.Dispose() chaqiriladi

        Console.WriteLine("Dastur davom etmoqda.");
    }
}

```

## Tushuntirish va Mantiq:
`IDisposable` CLR tomonidan boshqarilmaydigan (fayl deskriptorlari, soketlar, baza ulanishlari) operatsion tizim resurslarini zudlik bilan yopish uchun yagona standart interfeysdir.

## Ishlash natijasi:
```text
Resurs bilan xavfsiz ish bajarildi.
Dispose chaqirildi: Resurs to'liq yopildi va xotiradan bo'shatildi.
Dastur davom etmoqda.
```

# 312-Topshiriq: IAsyncDisposable va await using: Asinxron resurslarni tozalash
## Topshiriq sharti:
C# 8 da kiritilgan `IAsyncDisposable` interfeysidan foydalanib asinxron ulanishlarni tozalang.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

class AsinxronUlanish : IAsyncDisposable
{
    public async ValueTask DisposeAsync()
    {
        await Task.Delay(50); // Tarmoq ulanishini asinxron yopish simulyatsiyasi
        Console.WriteLine("DisposeAsync: Asinxron ulanish toza yopildi.");
    }
}

internal class Program
{
    static async Task Main()
    {
        await using (var conn = new AsinxronUlanish())
        {
            Console.WriteLine("Asinxron ulanish ochiq.");
        }
    }
}

```

## Tushuntirish va Mantiq:
`IAsyncDisposable` asinxron operatsiyalar (masalan tarmoq soketiga ma'lumotlarni yuvib tashlash / flush qilish) davomida oqimni to'xtatib qo'ymasdan (non-blocking) resurslarni tozalash imkonini beradi.

## Ishlash natijasi:
```text
Asinxron ulanish ochiq.
DisposeAsync: Asinxron ulanish toza yopildi.
```

# 313-Topshiriq: IEnumerable<T> va IEnumerator<T>: Maxsus to'plam uchun iterator yaratish
## Topshiriq sharti:
`IEnumerable<int>` interfeysini amalga oshiruvchi sodda oraliq to'plamini yarating.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections;
using System.Collections.Generic;

class Oraliq : IEnumerable<int>
{
    private readonly int boshlanish;
    private readonly int tugash;

    public Oraliq(int b, int t) => (boshlanish, tugash) = (b, t);

    public IEnumerator<int> GetEnumerator()
    {
        for (int i = boshlanish; i <= tugash; i++)
        {
            yield return i;
        }
    }

    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}

internal class Program
{
    static void Main()
    {
        var oraliq = new Oraliq(10, 13);

        Console.Write("Oraliq elementlari: ");
        foreach (int x in oraliq)
        {
            Console.Write($"{x} ");
        }
        Console.WriteLine();
    }
}

```

## Tushuntirish va Mantiq:
`IEnumerable<T>` interfeysini amalga oshirgan har qanday sinf `foreach` siklida, shuningdek barcha LINQ metodlarida (`.Where()`, `.Select()`) to'g'ridan-to'g'ri ishtirok eta oladi.

## Ishlash natijasi:
```text
Oraliq elementlari: 10 11 12 13
```

# 314-Topshiriq: Interfeyslar merosxo'rligi (Interface Inheritance)
## Topshiriq sharti:
Interfeys boshqa interfeyslardan meros olib kengayishi mumkinligini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

interface IEntitiy
{
    int Id { get; }
}

interface IAuditableEntity : IEntitiy
{
    DateTime YaratilganSana { get; }
}

class Foydalanuvchi : IAuditableEntity
{
    public int Id { get; set; } = 1;
    public DateTime YaratilganSana { get; set; } = DateTime.UtcNow;
}

internal class Program
{
    static void Main()
    {
        IAuditableEntity f = new Foydalanuvchi();
        Console.WriteLine($"ID: {f.Id}, Sana yili: {f.YaratilganSana.Year}");
    }
}

```

## Tushuntirish va Mantiq:
Interfeyslar iyerarxiyasida bola interfeys ota interfeysning barcha a'zolarini o'ziga qo'shib oladi. Voris sinf ikkala interfeysning barcha talablarini bajarishi shart.

## Ishlash natijasi:
```text
ID: 1, Sana yili: 2026
```

# 315-Topshiriq: Interface Segregation Principle (ISP): Interfeyslarni maydalash
## Topshiriq sharti:
Bitta ulkan interfeys (Fat Interface) o'rniga kichik va maqsadli interfeyslar tuzish tamoyilini namoyish eting.

## Yechim (C# kodi):
```csharp
using System;

// Yomon: interface IMashina { void ChopEt(); void Skanerla(); void FaksYubor(); }
// Yaxshi (ISP):
interface IChopEtuvchi { void ChopEt(); }
interface ISkaner { void Skanerla(); }

class OddiyPrinter : IChopEtuvchi
{
    public void ChopEt() => Console.WriteLine("Oddiy printer hujjatni bosib chiqardi.");
}

class SuperKombayn : IChopEtuvchi, ISkaner
{
    public void ChopEt() => Console.WriteLine("Super qurilma chop etdi.");
    public void Skanerla() => Console.WriteLine("Super qurilma skaner qildi.");
}

internal class Program
{
    static void Main()
    {
        IChopEtuvchi p = new OddiyPrinter();
        p.ChopEt();

        SuperKombayn sk = new SuperKombayn();
        sk.ChopEt();
        sk.Skanerla();
    }
}

```

## Tushuntirish va Mantiq:
Interface Segregation Principle (ISP) ga ko'ra, mijozlar o'zlari ishlatmaydigan metodlarga qaram bo'lib qolmasligi kerak. Kichik interfeyslar dasturni ancha moslashuvchan qiladi.

## Ishlash natijasi:
```text
Oddiy printer hujjatni bosib chiqardi.
Super qurilma chop etdi.
Super qurilma skaner qildi.
```

# 316-Topshiriq: Dependency Injection (DI) poydevori: Interfeyslarga tayanish
## Topshiriq sharti:
Xizmat sinfini aniq sinflarga emas, interfeysga bog'lab Erkin Bog'lanish (Loose Coupling) yarating.

## Yechim (C# kodi):
```csharp
using System;

interface INotifier
{
    void Bildir(string xabar);
}

class TelegramNotifier : INotifier
{
    public void Bildir(string xabar) => Console.WriteLine($"[Telegram Bot]: {xabar}");
}

class BuyurtmaServisi
{
    private readonly INotifier notifier;

    // Dependency Injection konstruktor orqali
    public BuyurtmaServisi(INotifier n) => notifier = n;

    public void Yakunla()
    {
        Console.WriteLine("Buyurtma yakunlandi.");
        notifier.Bildir("Sizning buyurtmangiz muvaffaqiyatli qabul qilindi!");
    }
}

internal class Program
{
    static void Main()
    {
        var bot = new TelegramNotifier();
        var servis = new BuyurtmaServisi(bot);

        servis.Yakunla();
    }
}

```

## Tushuntirish va Mantiq:
Dependency Injection interfeyslar orqali sinfning tashqi bog'liqliklarini tashqaridan qabul qilishiga imkon beradi. Ertaga Telegram o'rniga SMS qo'shilsa ham, `BuyurtmaServisi` ning birorta qatori o'zgarmaydi.

## Ishlash natijasi:
```text
Buyurtma yakunlandi.
[Telegram Bot]: Sizning buyurtmangiz muvaffaqiyatli qabul qilindi!
```

# 317-Topshiriq: Interfeys xossalari va indeksatorlari
## Topshiriq sharti:
Interfeysda faqat o'qiladigan xossa va indeksator shartnomasini belgilang.

## Yechim (C# kodi):
```csharp
using System;

interface ILugat
{
    int Hajmi { get; }
    string this[string kalit] { get; set; }
}

class SoddaLugat : ILugat
{
    private readonly System.Collections.Generic.Dictionary<string, string> dict = new();

    public int Hajmi => dict.Count;

    public string this[string kalit]
    {
        get => dict.TryGetValue(kalit, out var v) ? v : "";
        set => dict[kalit] = value;
    }
}

internal class Program
{
    static void Main()
    {
        ILugat l = new SoddaLugat();
        l["salom"] = "hello";
        l["dunyo"] = "world";

        Console.WriteLine($"Lug'at hajmi: {l.Hajmi}");
        Console.WriteLine($"'salom' tarjimasi: {l["salom"]}");
    }
}

```

## Tushuntirish va Mantiq:
Interfeyslar metodlardan tashqari xossalar (`{ get; set; }`), indeksatorlar (`this[...]`) va hatto hodisalarni (`event`) ham o'z ichiga olishi mumkin.

## Ishlash natijasi:
```text
Lug'at hajmi: 2
'salom' tarjimasi: hello
```

# 318-Topshiriq: Interfeys hodisalari (Interface Events)
## Topshiriq sharti:
Interfeys orqali hodisa (event) shartnomasini taqdim eting va unga obuna bo'ling.

## Yechim (C# kodi):
```csharp
using System;

interface ISensor
{
    event Action<double> HaroratOzgardi;
    void Tekshir(double yangiHarorat);
}

class Termostat : ISensor
{
    public event Action<double>? HaroratOzgardi;

    public void Tekshir(double yangiHarorat)
    {
        HaroratOzgardi?.Invoke(yangiHarorat);
    }
}

internal class Program
{
    static void Main()
    {
        ISensor s = new Termostat();
        s.HaroratOzgardi += h => Console.WriteLine($"[SIGNAL]: Harorat o'zgardi -> {h}°C");

        s.Tekshir(28.5);
    }
}

```

## Tushuntirish va Mantiq:
Interfeys hodisalari kuzatuvchi (Observer) tizimlarni standartlashtirish va hodisalarni obuna bo'luvchilarga yetkazish uchun qo'llaniladi.

## Ishlash natijasi:
```text
[SIGNAL]: Harorat o'zgardi -> 28.5°C
```

# 319-Topshiriq: is va as operatorlari orqali ixtiyoriy interfeysni tekshirish
## Topshiriq sharti:
Obyekt ma'lum bir interfeysni qo'llab-quvvatlashini dastur ishlashi paytida (runtime) tekshirib harakat qiling.

## Yechim (C# kodi):
```csharp
using System;

interface IFaylgaSaqlanadigan
{
    void Saqla();
}

class Rasm : IFaylgaSaqlanadigan
{
    public void Saqla() => Console.WriteLine("Rasm faylga saqlandi.");
}

class Audio { }

internal class Program
{
    static void Jarayon(object obj)
    {
        if (obj is IFaylgaSaqlanadigan saqlagich)
        {
            saqlagich.Saqla();
        }
        else
        {
            Console.WriteLine($"{obj.GetType().Name} interfeysni qo'llamaydi.");
        }
    }

    static void Main()
    {
        Jarayon(new Rasm());
        Jarayon(new Audio());
    }
}

```

## Tushuntirish va Mantiq:
Runtime da obyektning interfeysga mosligini tekshirish plaginlar (Plugins) va modulli kengaytmalarni dinamik kashf qilishda asosiy vositadir.

## Ishlash natijasi:
```text
Rasm faylga saqlandi.
Audio interfeysni qo'llamaydi.
```

# 320-Topshiriq: Interfeys chaqiruvlari (Interface Dispatch) va unumdorlik
## Topshiriq sharti:
Sinf metodini bevosita chaqirish bilan interfeys orqali chaqirish o'rtasidagi farqni tushuntiring.

## Yechim (C# kodi):
```csharp
using System;

interface IHisobchi
{
    int Hisobla(int a, int b);
}

class OddiyHisobchi : IHisobchi
{
    public int Hisobla(int a, int b) => a + b;
}

internal class Program
{
    static void Main()
    {
        OddiyHisobchi direct = new OddiyHisobchi();
        IHisobchi inter = direct;

        int r1 = direct.Hisobla(5, 5); // To'g'ridan-to'g'ri chaqiruv (Direct call)
        int r2 = inter.Hisobla(5, 5);  // Interfeys chaqiruvi (Interface table dispatch)

        Console.WriteLine($"Natijalar: {r1}, {r2}");
        Console.WriteLine("Interfeys chaqiruvi ITable orqali amalga oshadi va xavfsiz polimorfizmni ta'minlaydi.");
    }
}

```

## Tushuntirish va Mantiq:
Interfeys chaqiruvlari CLR da Interface Dispatch jadvali (ITable) orqali bajariladi. JIT kompilyatori monomorfik chaqiruvlarni (agar faqat bitta sinf bo'lsa) tezkor to'g'ridan-to'g'ri chaqiruvga optimallashtiradi.

## Ishlash natijasi:
```text
Natijalar: 10, 10
Interfeys chaqiruvi ITable orqali amalga oshadi va xavfsiz polimorfizmni ta'minlaydi.
```

# 321-Topshiriq: Interfeys orqali Repository Pattern (IRepository<T>)
## Topshiriq sharti:
Ma'lumotlar bazasi amallari uchun standart CRUD interfeysini e'lon qiling.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

interface IRepository<T>
{
    void Add(T entity);
    T? GetById(int id);
    IEnumerable<T> GetAll();
}

record Foydalanuvchi(int Id, string Ism);

class XotiraFoydalanuvchiRepo : IRepository<Foydalanuvchi>
{
    private readonly Dictionary<int, Foydalanuvchi> baza = new();

    public void Add(Foydalanuvchi entity) => baza[entity.Id] = entity;
    public Foydalanuvchi? GetById(int id) => baza.GetValueOrDefault(id);
    public IEnumerable<Foydalanuvchi> GetAll() => baza.Values;
}

internal class Program
{
    static void Main()
    {
        IRepository<Foydalanuvchi> repo = new XotiraFoydalanuvchiRepo();
        repo.Add(new Foydalanuvchi(1, "Sardor"));
        repo.Add(new Foydalanuvchi(2, "Lola"));

        Console.WriteLine($"Topildi: {repo.GetById(1)?.Ism}");
    }
}

```

## Tushuntirish va Mantiq:
Repository Pattern dastur biznes mantig'ini ma'lumotlar saqlanadigan joydan (SQL, NoSQL, Memory) butunlay ajratib qo'yadi.

## Ishlash natijasi:
```text
Topildi: Sardor
```

# 322-Topshiriq: Interfeys orqali Adapter Pattern
## Topshiriq sharti:
Eski uchinchi tomon sinfini yangi tizim interfeysiga moslashtiruvchi Adapter yozing.

## Yechim (C# kodi):
```csharp
using System;

// Yangi tizim kutayotgan interfeys
interface ITolovTizimi
{
    void PulOtkaz(decimal summa);
}

// Eski kutubxona sinfi (Mos kelmaydigan metod)
class EskiBankApi
{
    public void MakePaymentInTiyin(long tiyin) =>
        Console.WriteLine($"Eski Bank orqali {tiyin / 100} so'm to'landi.");
}

// Adapter
class BankAdapter : ITolovTizimi
{
    private readonly EskiBankApi eski = new();

    public void PulOtkaz(decimal summa)
    {
        long tiyin = (long)(summa * 100);
        eski.MakePaymentInTiyin(tiyin);
    }
}

internal class Program
{
    static void Main()
    {
        ITolovTizimi tolov = new BankAdapter();
        tolov.PulOtkaz(50000m);
    }
}

```

## Tushuntirish va Mantiq:
Adapter Pattern bir-biriga mos kelmaydigan interfeyslarni o'zaro bog'lash uchun xizmat qiladi. Mavjud kodni o'zgartirmasdan tizimga kiritish imkonini beradi.

## Ishlash natijasi:
```text
Eski Bank orqali 50000 so'm to'landi.
```

# 323-Topshiriq: Interfeys orqali Decorator Pattern: Funksionallikni o'rash
## Topshiriq sharti:
Asosiy xizmat kodini o'zgartirmasdan, uning atrofida log yozuvchi Dekorator yarating.

## Yechim (C# kodi):
```csharp
using System;

interface IXizmat
{
    void Bajar();
}

class HaqiqiyXizmat : IXizmat
{
    public void Bajar() => Console.WriteLine("Asosiy muhim vazifa bajarildi.");
}

class LogDekorator : IXizmat
{
    private readonly IXizmat ichki;
    public LogDekorator(IXizmat x) => ichki = x;

    public void Bajar()
    {
        Console.WriteLine("[LOG]: Amaliyot boshlanmoqda...");
        ichki.Bajar();
        Console.WriteLine("[LOG]: Amaliyot muvaffaqiyatli yakunlandi.");
    }
}

internal class Program
{
    static void Main()
    {
        IXizmat xizmat = new LogDekorator(new HaqiqiyXizmat());
        xizmat.Bajar();
    }
}

```

## Tushuntirish va Mantiq:
Decorator Pattern obyektga dinamik ravishda qo'shimcha xatti-harakatlar (keshlash, loglash, xavfsizlik tekshiruvi) qo'shish imkonini beradi.

## Ishlash natijasi:
```text
[LOG]: Amaliyot boshlanmoqda...
Asosiy muhim vazifa bajarildi.
[LOG]: Amaliyot muvaffaqiyatli yakunlandi.
```

# 324-Topshiriq: Interfeyslar va Value Types: Boxing xavfi
## Topshiriq sharti:
`struct` interfeys o'zgaruvchisiga berilganda Heap ga ko'chishi (Boxing) xavfini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

interface ISanagich
{
    void Oshir();
}

struct Sanagich : ISanagich
{
    public int Son;
    public void Oshir() => Son++;
}

internal class Program
{
    static void Main()
    {
        Sanagich s = new Sanagich();
        s.Oshir();
        Console.WriteLine($"Struct da to'g'ridan-to'g'ri: {s.Son}");

        // Diqqat: Struct interfeysga o'tganda BOXING yuz beradi!
        ISanagich i = s; // Heap da yangi quti ochiladi!
        i.Oshir();       // Quti ichidagi son oshadi

        Console.WriteLine($"Original struct soni: {s.Son} (O'zgarmadi, chunki i quti edi!)");
    }
}

```

## Tushuntirish va Mantiq:
Qiymat turlari (struct) interfeys o'zgaruvchisiga o'zlashtirilganda CLR uni majburan Heap da qutilaydi (Boxing). Bu xotira ajratishiga va kutilmagan nusxalanish muammolariga olib kelishi mumkin.

## Ishlash natijasi:
```text
Struct da to'g'ridan-to'g'ri: 1
Original struct soni: 1 (O'zgarmadi, chunki i quti edi!)
```

# 325-Topshiriq: Generik cheklov bilan Boxing siz Struct interfeys chaqiruvi
## Topshiriq sharti:
`where T : ISanagich` orqali struct larni hech qanday boxing siz tezkor ishlatishni ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

interface ISanagich
{
    void Oshir();
}

struct TezkorSanagich : ISanagich
{
    public int Son;
    public void Oshir() => Son++;
}

internal class Program
{
    // Generik cheklov orqali chaqirilganda CLR boxing QILMAYDI!
    static void Ishlat<T>(ref T obj) where T : struct, ISanagich
    {
        obj.Oshir();
    }

    static void Main()
    {
        TezkorSanagich s = new TezkorSanagich();
        Ishlat(ref s);

        Console.WriteLine($"Boxing siz oshirildi: {s.Son}");
    }
}

```

## Tushuntirish va Mantiq:
Generik cheklov (`where T : IInterface`) JIT ga parametr turini to'g'ridan-to'g'ri bilish imkonini beradi. Natijada `struct` uchun ixtisoslashgan (specialized) mashina kodi generatsiya qilinadi va 0 boxing bo'ladi.

## Ishlash natijasi:
```text
Boxing siz oshirildi: 1
```

# 326-Topshiriq: Default Interface Methodlarda ota interfeys metodini chaqirish
## Topshiriq sharti:
Interfeys merosxo'rligida `base(IInterface).Metod()` orqali ota interfeysning standart kodini chaqiring.

## Yechim (C# kodi):
```csharp
using System;

interface IBazaXizmat
{
    void Ishla() => Console.WriteLine("Baza interfeysi kodi");
}

interface IKengayganXizmat : IBazaXizmat
{
    void IBazaXizmat.Ishla()
    {
        Console.WriteLine("Kengaygan interfeys boshlanishi");
        base(IBazaXizmat).Ishla(); // Ota interfeysning standart implementatsiyasi
    }
}

class MeningXizmatim : IKengayganXizmat { }

internal class Program
{
    static void Main()
    {
        IBazaXizmat x = new MeningXizmatim();
        x.Ishla();
    }
}

```

## Tushuntirish va Mantiq:
C# 8 dan boshlab interfeyslar zanjirida `base(IInterfeys).Metod()` sintaksisi yordamida ota interfeysning standart metod tanasini chaqirish mumkin.

## Ishlash natijasi:
```text
Kengaygan interfeys boshlanishi
Baza interfeysi kodi
```

# 327-Topshiriq: Interfeys orqali Factory Pattern
## Topshiriq sharti:
Turli ma'lumotlar bazasi ulanishlarini interfeys orqali ishlab chiqaruvchi Factory yozing.

## Yechim (C# kodi):
```csharp
using System;

interface IDbConnection
{
    void Ulanish();
}

class SqlServerConnection : IDbConnection
{
    public void Ulanish() => Console.WriteLine("SQL Server ga ulandi.");
}

class PostgreSqlConnection : IDbConnection
{
    public void Ulanish() => Console.WriteLine("PostgreSQL ga ulandi.");
}

class DbFactory
{
    public static IDbConnection Yarat(string tur) => tur.ToLower() switch
    {
        "sql" => new SqlServerConnection(),
        "postgres" => new PostgreSqlConnection(),
        _ => throw new ArgumentException("Noma'lum baza turi")
    };
}

internal class Program
{
    static void Main()
    {
        IDbConnection conn = DbFactory.Yarat("postgres");
        conn.Ulanish();
    }
}

```

## Tushuntirish va Mantiq:
Factory Pattern aniq sinflarni yashirib, mijoz kodiga faqat umumiy `IDbConnection` interfeysini taqdim etadi.

## Ishlash natijasi:
```text
PostgreSQL ga ulandi.
```

# 328-Topshiriq: Interfeys orqali Facade Pattern: Murakkab tizimni soddalashtirish
## Topshiriq sharti:
Ko'p bosqichli buyurtma tizimini bitta oddiy `IBuyurtmaFasad` interfeysi ortiga yashiring.

## Yechim (C# kodi):
```csharp
using System;

interface IBuyurtmaFasad
{
    void XaridniRasmiylashtir(string mahsulot, decimal narx);
}

class Ombor { public void MahsulotniBronQil(string nom) => Console.WriteLine($"Ombor: {nom} bron qilindi."); }
class Bank { public void PulYech(decimal summa) => Console.WriteLine($"Bank: {summa:N0} so'm yechildi."); }
class Yetkazish { public void KuryergaBer() => Console.WriteLine("Yetkazish: Kuryer yo'lga chiqdi."); }

class BuyurtmaFasad : IBuyurtmaFasad
{
    private readonly Ombor ombor = new();
    private readonly Bank bank = new();
    private readonly Yetkazish kuryer = new();

    public void XaridniRasmiylashtir(string mahsulot, decimal narx)
    {
        ombor.MahsulotniBronQil(mahsulot);
        bank.PulYech(narx);
        kuryer.KuryergaBer();
        Console.WriteLine("Xarid muvaffaqiyatli yakunlandi!");
    }
}

internal class Program
{
    static void Main()
    {
        IBuyurtmaFasad fasad = new BuyurtmaFasad();
        fasad.XaridniRasmiylashtir("Smartfon", 2500000m);
    }
}

```

## Tushuntirish va Mantiq:
Facade Pattern bir nechta murakkab quyi tizimlarni (subsystems) bitta sodda interfeys ortiga jamlaydi va mijoz uchun dasturdan foydalanishni nihoyatda yengillashtiradi.

## Ishlash natijasi:
```text
Ombor: Smartfon bron qilindi.
Bank: 2,500,000 so'm yechildi.
Yetkazish: Kuryer yo'lga chiqdi.
Xarid muvaffaqiyatli yakunlandi!
```

# 329-Topshiriq: IProgress<T>: Asinxron jarayon foizini ko'rsatuvchi interfeys
## Topshiriq sharti:
Uzoq davom etuvchi operatsiya jarayonini `IProgress<int>` orqali kuzatib boring.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    static void OgirYuklash(IProgress<int>? progress)
    {
        for (int i = 1; i <= 3; i++)
        {
            Thread.Sleep(50); // Simulyatsiya
            progress?.Report(i * 33);
        }
    }

    static void Main()
    {
        var progress = new Progress<int>(foiz =>
        {
            Console.WriteLine($"Yuklanish jarayoni: {foiz}%");
        });

        OgirYuklash(progress);
        Console.WriteLine("Jarayon yakunlandi.");
    }
}

```

## Tushuntirish va Mantiq:
`IProgress<T>` .NET ning asinxron jarayonlar rivojini xavfsiz kuzatib boruvchi standart interfeysidir. U UI oqimlarida grafik progress-barlarni yangilash uchun keng qo'llaniladi.

## Ishlash natijasi:
```text
Yuklanish jarayoni: 33%
Yuklanish jarayoni: 66%
Yuklanish jarayoni: 99%
Jarayon yakunlandi.
```

# 330-Topshiriq: IAsyncEnumerable<T>: Asinxron oqimlar shartnomasi
## Topshiriq sharti:
`IAsyncEnumerable<int>` orqali ma'lumotlarni asinxron oqim sifatida uzatuvchi metod yozing.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

internal class Program
{
    static async IAsyncEnumerable<int> OqimniOlishAsync()
    {
        for (int i = 1; i <= 3; i++)
        {
            await Task.Delay(20); // Asinxron kutish
            yield return i * 10;
        }
    }

    static async Task Main()
    {
        await foreach (int son in OqimniOlishAsync())
        {
            Console.WriteLine($"Oqimdan keldi: {son}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`IAsyncEnumerable<T>` C# 8 da kiritilgan bo'lib, veb-soketlar, IoT datchiklari yoki sun'iy intellekt (LLM token streaming) natijalarini real vaqt rejimida qabul qilish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Oqimdan keldi: 10
Oqimdan keldi: 20
Oqimdan keldi: 30
```

# 331-Topshiriq: Static Abstract a'zolar bilan Factory shartnomasi
## Topshiriq sharti:
Interfeysda yangi obyekt yaratuvchi `static abstract` factory metodini e'lon qiling.

## Yechim (C# kodi):
```csharp
using System;

interface IYaratiladigan<T>
{
    static abstract T StandartQiymat();
}

class Konfiguratsiya : IYaratiladigan<Konfiguratsiya>
{
    public string Muhit { get; set; } = "Dev";

    public static Konfiguratsiya StandartQiymat() => new Konfiguratsiya { Muhit = "Production" };
}

internal class Program
{
    static void Tekshir<T>() where T : IYaratiladigan<T>
    {
        T def = T.StandartQiymat();
        Console.WriteLine($"Standart instansiya turi: {def.GetType().Name}");
    }

    static void Main()
    {
        Tekshir<Konfiguratsiya>();
    }
}

```

## Tushuntirish va Mantiq:
Statik abstrakt a'zolar C# 11 da Static Polymorphism (kompilyatsiya vaqtidagi polimorfizm) imkonini taqdim etdi. Bu instansiya yaratmasdan interfeys orqali metodlarni chaqirishga yo'l ochadi.

## Ishlash natijasi:
```text
Standart instansiya turi: Konfiguratsiya
```

# 332-Topshiriq: Marker Interface vs Custom Attributes
## Topshiriq sharti:
Tarixiy bo'sh interfeys (Marker) va zamonaviy atributlar o'rtasidagi farqni namoyish eting.

## Yechim (C# kodi):
```csharp
using System;

// Tarixiy: Marker Interface (Ichida hech narsa yo'q)
interface IArxivlanadigan { }

// Zamonaviy: Custom Attribute
[AttributeUsage(AttributeTargets.Class)]
class ArxivlanadiganAttribute : Attribute { }

[Arxivlanadigan]
class FoydalanuvchiHujjati : IArxivlanadigan { }

internal class Program
{
    static void Main()
    {
        var doc = new FoydalanuvchiHujjati();

        // Marker tekshiruvi:
        bool marker = doc is IArxivlanadigan;

        // Atribut tekshiruvi:
        bool attr = Attribute.IsDefined(typeof(FoydalanuvchiHujjati), typeof(ArxivlanadiganAttribute));

        Console.WriteLine($"Marker bilan tekshirildi: {marker}");
        Console.WriteLine($"Atribut bilan tekshirildi: {attr}");
    }
}

```

## Tushuntirish va Mantiq:
Ilgari obyektlarni belgilash uchun Marker interfeyslar ishlatilgan. Zamonaviy .NET da esa atributlar (Attributes) afzal ko'riladi, chunki atributlar qo'shimcha parametrlar va metama'lumotlarni o'zida saqlay oladi.

## Ishlash natijasi:
```text
Marker bilan tekshirildi: True
Atribut bilan tekshirildi: True
```

# 333-Topshiriq: Domen arxitekturasi: IEntity va IAggregateRoot
## Topshiriq sharti:
Domain-Driven Design (DDD) da yagona identifikatorga ega Entity va Aggregate Root interfeyslarini belgilang.

## Yechim (C# kodi):
```csharp
using System;

interface IEntity<TId>
{
    TId Id { get; }
}

interface IAggregateRoot { }

class Buyurtma : IEntity<Guid>, IAggregateRoot
{
    public Guid Id { get; } = Guid.NewGuid();
    public decimal Summa { get; set; } = 150000m;
}

internal class Program
{
    static void Main()
    {
        var b = new Buyurtma();
        Console.WriteLine($"Buyurtma ID uzunligi: {b.Id.ToString().Length}");
        Console.WriteLine($"Aggregate Root mi: {b is IAggregateRoot}");
    }
}

```

## Tushuntirish va Mantiq:
DDD arxitekturasida `IAggregateRoot` faqat tranzaksiyalarning markaziy nuqtasi bo'lgan bosh obyektlarga beriladi (masalan `Buyurtma`, lekin uning ichidagi alohida qatorlar emas).

## Ishlash natijasi:
```text
Buyurtma ID uzunligi: 36
Aggregate Root mi: True
```

# 334-Topshiriq: Domen servislari: IPaymentService va ITokenService
## Topshiriq sharti:
Autentifikatsiya va to'lov shartnomalarini toza interfeyslar orqali modellashtiring.

## Yechim (C# kodi):
```csharp
using System;

interface ITokenService
{
    string TokenYarat(string foydalanuvchi);
}

class JwtTokenService : ITokenService
{
    public string TokenYarat(string user) => $"eyJhbGciOiJIUzI1NiIsIn...[{user}]";
}

internal class Program
{
    static void Main()
    {
        ITokenService tokenXizmati = new JwtTokenService();
        string token = tokenXizmati.TokenYarat("admin_anvar");
        Console.WriteLine($"Token yaratildi: {token}");
    }
}

```

## Tushuntirish va Mantiq:
Domen servislari interfeyslari infratuzilma qatlamidan (Infrastructure) mustaqil bo'lishi kerak. Bu kelajakda JWT o'rniga boshqa standartga o'tishni juda osonlashtiradi.

## Ishlash natijasi:
```text
Token yaratildi: eyJhbGciOiJIUzI1NiIsIn...[admin_anvar]
```

# 335-Topshiriq: Multi-Tenancy arxitekturasi: ITenantAware interfeysi
## Topshiriq sharti:
Har bir mijoz kompaniyasining (Tenant) ma'lumotlarini ajratib turuvchi interfeysni qo'llang.

## Yechim (C# kodi):
```csharp
using System;

interface ITenantAware
{
    string TenantId { get; set; }
}

class MahsulotYozuvi : ITenantAware
{
    public string TenantId { get; set; } = "";
    public string Nomi { get; set; } = "";
}

internal class Program
{
    static void Filtrlash(ITenantAware entity, string joriyKompaniya)
    {
        if (entity.TenantId == joriyKompaniya)
            Console.WriteLine($"Ruxsat berildi: {entity.GetType().Name} joriy kompaniyaga tegishli.");
        else
            Console.WriteLine("Kirish taqiqlandi: Boshqa kompaniya ma'lumoti!");
    }

    static void Main()
    {
        var p1 = new MahsulotYozuvi { TenantId = "COMPANY_A", Nomi = "Kofe" };
        Filtrlash(p1, "COMPANY_A");
        Filtrlash(p1, "COMPANY_B");
    }
}

```

## Tushuntirish va Mantiq:
SaaS (Software as a Service) bulutli tizimlarida barcha domen modellari `ITenantAware` interfeysini qabul qiladi va ma'lumotlar bazasidan o'qishda avtomatik kompaniya bo'yicha filtrlanadi.

## Ishlash natijasi:
```text
Ruxsat berildi: MahsulotYozuvi joriy kompaniyaga tegishli.
Kirish taqiqlandi: Boshqa kompaniya ma'lumoti!
```

# 336-Topshiriq: Audit interfeysi: IAuditableEntity
## Topshiriq sharti:
Obyektning kim tomonidan va qachon yaratilgani/yangilangani haqidagi shartnomani bajaring.

## Yechim (C# kodi):
```csharp
using System;

interface IAuditableEntity
{
    DateTime YaratilganVaqt { get; set; }
    string Yaratuvchi { get; set; }
}

class Hujjat : IAuditableEntity
{
    public int Id { get; set; }
    public DateTime YaratilganVaqt { get; set; }
    public string Yaratuvchi { get; set; } = "";
}

internal class Program
{
    static void AuditQaydEt(IAuditableEntity entity, string kim)
    {
        entity.YaratilganVaqt = DateTime.UtcNow;
        entity.Yaratuvchi = kim;
    }

    static void Main()
    {
        var h = new Hujjat { Id = 100 };
        AuditQaydEt(h, "Admin_Shokir");

        Console.WriteLine($"Hujjat ID: {h.Id}, Yaratuvchi: {h.Yaratuvchi}, Sana yili: {h.YaratilganVaqt.Year}");
    }
}

```

## Tushuntirish va Mantiq:
Entity Framework Core va korporativ tizimlarda `SaveChanges` chaqirilganda barcha `IAuditableEntity` obyektlari avtomatik ushlanib, joriy sana va foydalanuvchi ma'lumotlari to'ldiriladi.

## Ishlash natijasi:
```text
Hujjat ID: 100, Yaratuvchi: Admin_Shokir, Sana yili: 2026
```

# 337-Topshiriq: Soft Delete interfeysi: ISoftDeletable
## Topshiriq sharti:
Ma'lumotlar bazasidan jismonan o'chirmasdan, bayroq orqali yashiruvchi Soft Delete shartnomasini yarating.

## Yechim (C# kodi):
```csharp
using System;

interface ISoftDeletable
{
    bool Ochirilganmi { get; set; }
    DateTime? OchirilganVaqt { get; set; }
}

class Mijoz : ISoftDeletable
{
    public string Ism { get; set; } = "";
    public bool Ochirilganmi { get; set; }
    public DateTime? OchirilganVaqt { get; set; }
}

internal class Program
{
    static void XavfsizOchirish(ISoftDeletable obj)
    {
        obj.Ochirilganmi = true;
        obj.OchirilganVaqt = DateTime.UtcNow;
        Console.WriteLine("Obyekt jismonan o'chirilmadi, arxivlandi.");
    }

    static void Main()
    {
        var m = new Mijoz { Ism = "Rustam" };
        XavfsizOchirish(m);

        Console.WriteLine($"Mijoz o'chirilganmi: {m.Ochirilganmi}, Vaqt yili: {m.OchirilganVaqt?.Year}");
    }
}

```

## Tushuntirish va Mantiq:
Soft Delete bank va hisob-kitob dasturlarida ma'lumotlar yo'qolishining oldini oladi. Barcha so'rovlar avtomatik `WHERE Ochirilganmi = false` filtri bilan ishlaydi.

## Ishlash natijasi:
```text
Obyekt jismonan o'chirilmadi, arxivlandi.
Mijoz o'chirilganmi: True, Vaqt yili: 2026
```

# 338-Topshiriq: C# da Duck Typing yo'qligi va qat'iy interfeys majburiyati
## Topshiriq sharti:
Python yoki JavaScript dan farqli ravishda C# da metodlar nomi bir xil bo'lsa ham interfeys aniq e'lon qilinishi shartligini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

interface IUchar
{
    void Uch();
}

class Qush : IUchar
{
    public void Uch() => Console.WriteLine("Qush osmonda uchmoqda.");
}

class Dron
{
    public void Uch() => Console.WriteLine("Dron havoga ko'tarildi.");
}

internal class Program
{
    static void ParvozQildir(IUchar ob) => ob.Uch();

    static void Main()
    {
        ParvozQildir(new Qush());
        // ParvozQildir(new Dron()); // KOMPILYATSIYA XATOSI! Dron Uch() ga ega bo'lsa ham, IUchar ni aniq e'lon qilmagan!

        Console.WriteLine("C# qat'iy statik tiplangan til bo'lib, Duck Typing ga yo'l qo'ymaydi.");
    }
}

```

## Tushuntirish va Mantiq:
C# da nominal tiplash (Nominal Typing) amalda bo'lib, sinf qaysi interfeysni bajarganini aniq o'z sarlavhasida yozishi shart. Bu kutilmagan nom o'xshashliklari sababli xatoliklar kelib chiqishini 100% bartaraf etadi.

## Ishlash natijasi:
```text
Qush osmonda uchmoqda.
C# qat'iy statik tiplangan til bo'lib, Duck Typing ga yo'l qo'ymaydi.
```

# 339-Topshiriq: Abstrakt sinf va Interfeysning gibrid qo'llanilishi
## Topshiriq sharti:
Interfeys shartnomasi va uning asosiy standart implementatsiyasini beruvchi Abstrakt sinf juftligini (Base Class + Interface) quring.

## Yechim (C# kodi):
```csharp
using System;

interface ISoluvchi
{
    void IchishgaQuy();
}

abstract class BazaIchimlik : ISoluvchi
{
    public string Nomi { get; }
    protected BazaIchimlik(string nomi) => Nomi = nomi;

    public virtual void IchishgaQuy() => Console.WriteLine($"{Nomi} stakanga quyildi.");
}

class Choy : BazaIchimlik
{
    public Choy() : base("Ko'k Choy") { }
}

internal class Program
{
    static void Main()
    {
        ISoluvchi choy = new Choy();
        choy.IchishgaQuy();
    }
}

```

## Tushuntirish va Mantiq:
Ushbu naqsh .NET freymvorkida juda keng tarqalgan (masalan `IDisposable` va `SafeHandle`, `IList<T>` va `Collection<T>`). Interfeys eng yuqori darajadagi moslashuvchanlikni beradi, abstrakt ota sinf esa tayyor kodni ulashadi.

## Ishlash natijasi:
```text
Ko'k Choy stakanga quyildi.
```

# 340-Topshiriq: Mocking va Unit Testlar uchun interfeyslarning o'rni
## Topshiriq sharti:
Test paytida haqiqiy SMS xizmati o'rniga soxta (Mock) sinfdan foydalanishni ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

interface ISmsXizmati
{
    bool Yubor(string telefon, string matn);
}

// Testlar uchun soxta (Mock) obyekt
class MockSmsXizmati : ISmsXizmati
{
    public int YuborilganlarSoni = 0;

    public bool Yubor(string telefon, string matn)
    {
        YuborilganlarSoni++;
        return true; // Har doim muvaffaqiyatli deb qaytarish
    }
}

internal class Program
{
    static void Main()
    {
        var mock = new MockSmsXizmati();
        mock.Yubor("+998901112233", "Test kod");

        Console.WriteLine($"Test muvaffaqiyati: {mock.YuborilganlarSoni == 1}");
    }
}

```

## Tushuntirish va Mantiq:
Interfeyslar bo'lmaganda Unit Testlarni yozish deyarli imkonsiz bo'lib qoladi. Interfeyslar yordamida tashqi tizimlarga (SMS, To'lov, Ma'lumotlar bazasi) ulanmasdan biznes mantiqni alohida ajratib testlash mumkin.

## Ishlash natijasi:
```text
Test muvaffaqiyati: True
```

# 341-Topshiriq: IReadOnlyList<T> va IReadOnlyDictionary<TKey, TValue>
## Topshiriq sharti:
To'plamlarni tashqi modifikatsiyalardan himoyalovchi faqat o'qiladigan interfeyslarni qo'llang.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

class KursBoshqaruvi
{
    private readonly List<string> mavzular = [ "C# Asoslari", "OOP", "LINQ" ];

    // Faqat o'qish mumkin bo'lgan interfeys orqali tashqariga berish
    public IReadOnlyList<string> Mavzular => mavzular;
}

internal class Program
{
    static void Main()
    {
        var kurs = new KursBoshqaruvi();
        Console.WriteLine($"Mavzular soni: {kurs.Mavzular.Count}");
        Console.WriteLine($"1-mavzu: {kurs.Mavzular[0]}");

        // kurs.Mavzular.Add("Yangi"); // XATO! IReadOnlyList da Add metodi yo'q
    }
}

```

## Tushuntirish va Mantiq:
`IReadOnlyList<T>` tashqi kodga elementlarni o'qish va indekslash (`[i]`) imkonini beradi, lekin element qo'shish yoki o'chirishni cheklaydi.

## Ishlash natijasi:
```text
Mavzular soni: 3
1-mavzu: C# Asoslari
```

# 342-Topshiriq: Interfeys a'zolarida kirish modifikatorlari (internal, protected)
## Topshiriq sharti:
C# 8 dan boshlab interfeys ichida `internal` yoki `protected` a'zolarni e'lon qilishni ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

interface IAuditXizmati
{
    // Faqat shu yig'ma (assembly) ichida ko'rinuvchi metod
    internal void IchkiAudit();
}

class MahalliAudit : IAuditXizmati
{
    void IAuditXizmati.IchkiAudit() => Console.WriteLine("Ichki audit bajarildi.");
}

internal class Program
{
    static void Main()
    {
        IAuditXizmati x = new MahalliAudit();
        x.IchkiAudit();
    }
}

```

## Tushuntirish va Mantiq:
C# 8 dan boshlab interfeyslar a'zolari nafaqat `public`, balki `internal`, `protected`, `private` bo'lishi ham mumkin. Bu murakkab kutubxona arxitekturalarini loyihalashda juda qo'l keladi.

## Ishlash natijasi:
```text
Ichki audit bajarildi.
```

# 343-Topshiriq: Inversion of Control (IoC) Servis Deskriptori simulyatsiyasi
## Topshiriq sharti:
Interfeys va uning amalga oshiruvchi sinfini ro'yxatga oluvchi mini-IoC mexanizmini yozing.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

interface ILog { void Print(string s); }
class MyLog : ILog { public void Print(string s) => Console.WriteLine($"LOG: {s}"); }

class MiniKonteyner
{
    private readonly Dictionary<Type, Type> xarita = new();

    public void Register<TInterface, TImplementation>()
    {
        xarita[typeof(TInterface)] = typeof(TImplementation);
    }

    public TInterface Resolve<TInterface>()
    {
        Type implType = xarita[typeof(TInterface)];
        return (TInterface)Activator.CreateInstance(implType)!;
    }
}

internal class Program
{
    static void Main()
    {
        var container = new MiniKonteyner();
        container.Register<ILog, MyLog>();

        ILog logger = container.Resolve<ILog>();
        logger.Print("Mini IoC muvaffaqiyatli ishladi!");
    }
}

```

## Tushuntirish va Mantiq:
Dependency Injection konteynerlari (masalan ASP.NET Core dagi `IServiceProvider`) aynan shu tamoyil asosida ishlaydi: interfeys turi ro'yxatga olinadi va talab qilinganda uning aniq sinfi yaratib beriladi.

## Ishlash natijasi:
```text
LOG: Mini IoC muvaffaqiyatli ishladi!
```

# 344-Topshiriq: Interfeys orqali Command Pattern (ICommand)
## Topshiriq sharti:
Buyruqlarni obyektlarga aylantirib, ularni navbat bilan bajaruvchi Command naqshini yozing.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

interface IBuyruq
{
    void Execute();
}

class ChiroqniYoq : IBuyruq
{
    public void Execute() => Console.WriteLine("Chiroq yoqildi.");
}

class ChiroqniOchir : IBuyruq
{
    public void Execute() => Console.WriteLine("Chiroq o'chirildi.");
}

internal class Program
{
    static void Main()
    {
        Queue<IBuyruq> navbat = new();
        navbat.Enqueue(new ChiroqniYoq());
        navbat.Enqueue(new ChiroqniOchir());

        while (navbat.Count > 0)
        {
            IBuyruq cmd = navbat.Dequeue();
            cmd.Execute();
        }
    }
}

```

## Tushuntirish va Mantiq:
Command Pattern harakatlarni parametrlash, ularni navbatga qo'yish (Task queue) va bekor qilish (Undo/Redo) imkoniyatlarini taqdim etadi.

## Ishlash natijasi:
```text
Chiroq yoqildi.
Chiroq o'chirildi.
```

# 345-Topshiriq: Interfeys orqali Middleware / Pipeline Pattern
## Topshiriq sharti:
So'rovlarni ketma-ket qayta ishlovchi zanjir interfeysini quring.

## Yechim (C# kodi):
```csharp
using System;

interface IMiddleware
{
    void Invoke(string sorov, Action keyingi);
}

class AutentifikatsiyaMiddleware : IMiddleware
{
    public void Invoke(string sorov, Action keyingi)
    {
        Console.WriteLine("1. Autentifikatsiya tekshirildi.");
        keyingi();
    }
}

class LogMiddleware : IMiddleware
{
    public void Invoke(string sorov, Action keyingi)
    {
        Console.WriteLine("2. So'rov qayd etildi.");
        keyingi();
    }
}

internal class Program
{
    static void Main()
    {
        IMiddleware m1 = new AutentifikatsiyaMiddleware();
        IMiddleware m2 = new LogMiddleware();

        m1.Invoke("GET /api/user", () =>
        {
            m2.Invoke("GET /api/user", () =>
            {
                Console.WriteLine("3. Yakuniy Controller javob qaytardi.");
            });
        });
    }
}

```

## Tushuntirish va Mantiq:
ASP.NET Core HTTP Request Pipeline aynan shu uslubda qurilgan bo'lib, har bir qatlam (middleware) o'z ishini bajarib, so'rovni keyingisiga uzatadi.

## Ishlash natijasi:
```text
1. Autentifikatsiya tekshirildi.
2. So'rov qayd etildi.
3. Yakuniy Controller javob qaytardi.
```

# 346-Topshiriq: Ko'p shartli generik cheklovlar interfeyslar bilan
## Topshiriq sharti:
Metod parametriga bir vaqtning o'zida ikkita interfeysni talab qiluvchi cheklov qo'ying.

## Yechim (C# kodi):
```csharp
using System;

interface INomli { string Nomi { get; } }
interface INarxli { decimal Narxi { get; } }

class Kitob : INomli, INarxli
{
    public string Nomi { get; set; } = "C# Qo'llanma";
    public decimal Narxi { get; set; } = 80000m;
}

internal class Program
{
    static void MalumotBer<T>(T element) where T : INomli, INarxli
    {
        Console.WriteLine($"Mahsulot: '{element.Nomi}', Narxi: {element.Narxi:N0} so'm");
    }

    static void Main()
    {
        MalumotBer(new Kitob());
    }
}

```

## Tushuntirish va Mantiq:
Generik cheklovlarda `where T : I1, I2` sintaksisi parametrning bir vaqtning o'zida barcha ko'rsatilgan interfeyslarni amalga oshirgan bo'lishini qat'iy kafolatlaydi.

## Ishlash natijasi:
```text
Mahsulot: 'C# Qo'llanma', Narxi: 80,000 so'm
```

# 347-Topshiriq: Custom IDisposable va unmanaged resurs tozalash
## Topshiriq sharti:
`IDisposable` ni `bool disposing` himoyalangan metodi bilan xavfsiz amalga oshirish standart shablonini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

class XavfsizResurs : IDisposable
{
    private bool disposed = false;

    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this);
    }

    protected virtual void Dispose(bool disposing)
    {
        if (!disposed)
        {
            if (disposing)
            {
                Console.WriteLine("Boshqariladigan resurslar tozalandi.");
            }
            disposed = true;
        }
    }
}

internal class Program
{
    static void Main()
    {
        using (var r = new XavfsizResurs())
        {
            Console.WriteLine("Ish bajarildi.");
        }
    }
}

```

## Tushuntirish va Mantiq:
Ushbu 'Dispose Pattern' Microsoft tomonidan tavsiya etilgan standart shablon bo'lib, resurslarni xavfsiz va bir martagina tozalanishini kafolatlaydi.

## Ishlash natijasi:
```text
Ish bajarildi.
Boshqariladigan resurslar tozalandi.
```

# 348-Topshiriq: Interfeys orqali State Pattern
## Topshiriq sharti:
Tizimning holatiga qarab harakatini o'zgartiruvchi State naqshini interfeys bilan quring.

## Yechim (C# kodi):
```csharp
using System;

interface IHolat
{
    void Bosilganda();
}

class QizilHolat : IHolat
{
    public void Bosilganda() => Console.WriteLine("Qizil chiroq: Harakat to'xtatildi!");
}

class YashilHolat : IHolat
{
    public void Bosilganda() => Console.WriteLine("Yashil chiroq: Harakatga ruxsat!");
}

class Svetafor
{
    public IHolat JoriyHolat { get; set; } = new QizilHolat();
    public void TugmaniBos() => JoriyHolat.Bosilganda();
}

internal class Program
{
    static void Main()
    {
        var s = new Svetafor();
        s.TugmaniBos();

        s.JoriyHolat = new YashilHolat();
        s.TugmaniBos();
    }
}

```

## Tushuntirish va Mantiq:
State Pattern murakkab `switch` va `if-else` shartlarini polimorfik interfeys obyektlariga ajratib boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Qizil chiroq: Harakat to'xtatildi!
Yashil chiroq: Harakatga ruxsat!
```

# 349-Topshiriq: Interfeys orqali Visitor Pattern asoslari
## Topshiriq sharti:
Mavjud sinflar tuzilishini o'zgartirmasdan ularga yangi operatsiyalar qo'shish.

## Yechim (C# kodi):
```csharp
using System;

interface IShakl
{
    void QabulQil(IShaklMehmon mehmon);
}

interface IShaklMehmon
{
    void Tashrif(Doira d);
}

class Doira : IShakl
{
    public double Radius { get; set; } = 5;
    public void QabulQil(IShaklMehmon mehmon) => mehmon.Tashrif(this);
}

class EksportMehmon : IShaklMehmon
{
    public void Tashrif(Doira d) => Console.WriteLine($"Doira radius {d.Radius} bilan eksport qilindi.");
}

internal class Program
{
    static void Main()
    {
        IShakl shakl = new Doira();
        shakl.QabulQil(new EksportMehmon());
    }
}

```

## Tushuntirish va Mantiq:
Visitor Pattern obyekt tuzilmasini uning ustida bajariladigan operatsiyalardan to'liq ajratish uchun ishlatiladi.

## Ishlash natijasi:
```text
Doira radius 5 bilan eksport qilindi.
```

# 350-Topshiriq: Interfeyslar va Abstraksiya bo'limi integratsiyalashgan loyihasi
## Topshiriq sharti:
Dependency Injection, Repository, UnitOfWork va Auditing tamoyillarini birlashtiruvchi to'liq arxitektura shartnomasini yarating.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

interface IEntity { int Id { get; set; } }
interface IAuditable { DateTime Yaratildi { get; set; } }

record Xaridor(int Id, string Ism) : IEntity, IAuditable
{
    public DateTime Yaratildi { get; set; } = DateTime.UtcNow;
}

interface IXaridorRepozitoriy
{
    void Saqla(Xaridor xaridor);
    Xaridor? Top(int id);
}

class XotiraXaridorRepo : IXaridorRepozitoriy
{
    private readonly Dictionary<int, Xaridor> baza = new();

    public void Saqla(Xaridor x)
    {
        baza[x.Id] = x;
        Console.WriteLine($"[REPO]: Xaridor '{x.Ism}' saqlandi.");
    }

    public Xaridor? Top(int id) => baza.GetValueOrDefault(id);
}

class XaridorServisi(IXaridorRepozitoriy repo)
{
    public void YangiXaridorQosh(int id, string ism)
    {
        var x = new Xaridor(id, ism);
        repo.Saqla(x);
    }
}

internal class Program
{
    static void Main()
    {
        IXaridorRepozitoriy repo = new XotiraXaridorRepo();
        var servis = new XaridorServisi(repo);

        servis.YangiXaridorQosh(1, "Alisher");
        Console.WriteLine("Interfeyslar va Abstraksiya tizimi 100% muvaffaqiyatli yakunlandi.");
    }
}

```

## Tushuntirish va Mantiq:
Ushbu loyiha zamonaviy korporativ .NET dasturlashining eng muhim poydevori bo'lib, barcha modullarning interfeyslar orqali bir-biridan mustaqil, oson testlanadigan va xavfsiz ishlashini ta'minlaydi.

## Ishlash natijasi:
```text
[REPO]: Xaridor 'Alisher' saqlandi.
Interfeyslar va Abstraksiya tizimi 100% muvaffaqiyatli yakunlandi.
```

