# 10-Mavzu: Generics va Umumiy Turlar (451-500)

Ushbu bo'limda C# tilida umumiy dasturlash (Generic Programming) va tip xavfsizligi: generik sinflar, metodlar va interfeyslar, generik cheklovlar (`where T : class`, `struct`, `notnull`, `new()`, `unmanaged`, `enum`, `delegate`), kovariantlik (`out T`) va kontravariantlik (`in T`), invariantlik sabablari, JIT kompilyatsiyasi va ixtisoslashgan kod generatsiyasi, generik statik kesh naqshi hamda maxsus ma'lumot tuzilmalari bo'yicha 50 ta amaliy topshiriq jamlangan.

# 451-Topshiriq: Generiklar (Generics) falsafasi: Boxing dan qutulish va tip xavfsizligi
## Topshiriq sharti:
Eski `ArrayList` (object) bilan yangi generik `List<int>` ning boxing va tip xavfsizligi farqini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        // 1. Eski xavfli usul (.NET 1.0):
        ArrayList eski = new ArrayList();
        eski.Add(10); // Boxing!
        eski.Add("Matn"); // Xavfli! Har xil turlar aralashib ketadi
        // int xato = (int)eski[1]; // Runtime InvalidCastException!

        // 2. Zamonaviy Generik usul (.NET 2.0+):
        List<int> xavfsiz = new List<int>();
        xavfsiz.Add(10); // 0 boxing!
        // xavfsiz.Add("Matn"); // KOMPILYATSIYA XATOSI! Tip xavfsizligi kafolatlangan

        Console.WriteLine($"Generik ro'yxat birinchi soni: {xavfsiz[0]}");
    }
}

```

## Tushuntirish va Mantiq:
Generiklar (Generics) kodni ma'lum bir aniq turga bog'lamasdan, parametr sifatida tur qabul qilish imkonini beradi. Bu boxing va unboxing xarajatlarini butunlay yo'qotadi va barcha tip xatolarini runtime dan kompilyatsiya bosqichiga olib chiqadi.

## Ishlash natijasi:
```text
Generik ro'yxat birinchi soni: 10
```

# 452-Topshiriq: Generik sinf (Generic Class): Konteyner<T>
## Topshiriq sharti:
Har qanday turdagi qiymatni o'zida saqlay oluvchi umumiy `Konteyner<T>` sinfini yozing.

## Yechim (C# kodi):
```csharp
using System;

class Konteyner<T>
{
    private T element;

    public Konteyner(T dastlabki) => element = dastlabki;

    public void O'zgartir(T yangi) => element = yangi;
    public T Olish() => element;
}

internal class Program
{
    static void Main()
    {
        var sonKonteyner = new Konteyner<int>(100);
        var matnKonteyner = new Konteyner<string>("C# Generik");

        Console.WriteLine($"Son konteyner: {sonKonteyner.Olish()}");
        Console.WriteLine($"Matn konteyner: {matnKonteyner.Olish()}");
    }
}

```

## Tushuntirish va Mantiq:
`Konteyner<T>` e'lon qilinganda `T` o'rнига `int` yoki `string` berilsa, CLR har bir tur uchun toza tiplangan sinf instansiyasini hosil qiladi.

## Ishlash natijasi:
```text
Son konteyner: 100
Matn konteyner: C# Generik
```

# 453-Topshiriq: Generik metod: Swap<T>
## Topshiriq sharti:
Ixtiyoriy turdagi ikkita o'zgaruvchi qiymatini xavfsiz almashtiruvchi `Swap<T>` metodini yozing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Swap<T>(ref T a, ref T b)
    {
        T vaqtinchalik = a;
        a = b;
        b = vaqtinchalik;
    }

    static void Main()
    {
        int x = 10, y = 20;
        Swap(ref x, ref y);
        Console.WriteLine($"int Swap: x={x}, y={y}");

        string s1 = "Olma", s2 = "Anor";
        Swap(ref s1, ref s2);
        Console.WriteLine($"string Swap: s1={s1}, s2={s2}");
    }
}

```

## Tushuntirish va Mantiq:
Generik metod chaqirilganda C# kompilyatori argumentlar turiga qarab `<T>` parametrini o'zi avtomatik aniqlaydi (Type Inference). Shuning uchun `Swap<int>(ref x, ref y)` o'rniga oddiy `Swap(ref x, ref y)` yozish yetarli.

## Ishlash natijasi:
```text
int Swap: x=20, y=10
string Swap: s1=Anor, s2=Olma
```

# 454-Topshiriq: Generik interfeys: IRepository<T>
## Topshiriq sharti:
Domen obyektlarini saqlash va qidirish uchun umumiy generik shartnomani belgilang.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

interface IRepository<T>
{
    void Saqla(T element);
    T? Qidir(Predicate<T> shart);
}

class XotiraRepo<T> : IRepository<T>
{
    private readonly List<T> ro'yxat = new();

    public void Saqla(T element) => ro'yxat.Add(element);
    public T? Qidir(Predicate<T> shart) => ro'yxat.Find(shart);
}

internal class Program
{
    static void Main()
    {
        IRepository<string> repo = new XotiraRepo<string>();
        repo.Saqla("Toshkent");
        repo.Saqla("Buxoro");

        string? topildi = repo.Qidir(s => s.StartsWith("B"));
        Console.WriteLine($"Topilgan shahar: {topildi}");
    }
}

```

## Tushuntirish va Mantiq:
Generik interfeyslar dasturiy ta'minot arxitekturasida ma'lumotlar bilan ishlash qatlamini (Data Access Layer) yagona qolipga keltirish imkonini beradi.

## Ishlash natijasi:
```text
Topilgan shahar: Buxoro
```

# 455-Topshiriq: Generik cheklov: where T : class (Reference Type talabi)
## Topshiriq sharti:
Faqat havola turlari (sinflar) bilan ishlovchi va `null` bo'lishi mumkin bo'lgan generik sinf yozing.

## Yechim (C# kodi):
```csharp
using System;

class HavolaKonteyner<T> where T : class
{
    public T? Qiymat { get; set; }

    public bool Bo'shmi() => Qiymat == null;
}

internal class Program
{
    static void Main()
    {
        var k = new HavolaKonteyner<string>();
        Console.WriteLine($"Bo'shmi: {k.Bo'shmi()}");

        // var xato = new HavolaKonteyner<int>(); // KOMPILYATSIYA XATOSI! int ValueType, class emas!
    }
}

```

## Tushuntirish va Mantiq:
`where T : class` cheklovi `T` ning faqat Reference Type bo'lishini talab qiladi. Bu orqali `T` ga `null` o'zlashtirish va `== null` tekshiruvlarini bemalol bajarish mumkin bo'ladi.

## Ishlash natijasi:
```text
Bo'shmi: True
```

# 456-Topshiriq: Generik cheklov: where T : struct (Value Type talabi)
## Topshiriq sharti:
Faqat qiymat turlari bilan ishlovchi va Stack da xotira tejovchi generik tur e'lon qiling.

## Yechim (C# kodi):
```csharp
using System;

class QiymatKonteyner<T> where T : struct
{
    public T Qiymat { get; set; }
    public QiymatKonteyner(T q) => Qiymat = q;
}

internal class Program
{
    static void Main()
    {
        var son = new QiymatKonteyner<int>(42);
        var sana = new QiymatKonteyner<DateTime>(DateTime.Today);

        Console.WriteLine($"Son: {son.Qiymat}");
        Console.WriteLine($"Sana yili: {sana.Qiymat.Year}");

        // var xato = new QiymatKonteyner<string>("Xato"); // KOMPILYATSIYA XATOSI! string struct emas!
    }
}

```

## Tushuntirish va Mantiq:
`where T : struct` cheklovi `T` ning qiymat turi (primitiv sonlar, enum yoki struct) bo'lishini kafolatlaydi (`Nullable<T>` bundan mustasno).

## Ishlash natijasi:
```text
Son: 42
Sana yili: 2026
```

# 457-Topshiriq: Generik cheklov: where T : new() (Parametrsiz konstruktor talabi)
## Topshiriq sharti:
Generik metod ichida `new T()` orqali yangi instansiya hosil qilish uchun konstruktor cheklovini qo'llang.

## Yechim (C# kodi):
```csharp
using System;

class Zavod
{
    public static T IshlabChiqar<T>() where T : new()
    {
        // 'new()' cheklovi bo'lgani uchungina 'new T()' yozishga ruxsat etiladi!
        return new T();
    }
}

class Avto
{
    public string Model { get; set; } = "Standart Model";
}

internal class Program
{
    static void Main()
    {
        Avto m = Zavod.IshlabChiqar<Avto>();
        Console.WriteLine($"Yaratilgan avto: {m.Model}");
    }
}

```

## Tushuntirish va Mantiq:
`where T : new()` cheklovi `T` turining ommaviy parametrsiz konstruktorga (`public T()`) ega bo'lishini majburiy qiladi. Kompilyator ushbu cheklov orqali `new T()` chaqiruvini IL darajasida generatsiya qiladi.

## Ishlash natijasi:
```text
Yaratilgan avto: Standart Model
```

# 458-Topshiriq: Generik cheklov: where T : BaseClass va where T : Interface
## Topshiriq sharti:
Muayyan ota sinfdan meros olgan va belgilangan interfeysni bajargan turlar uchungina ishlovchi servis yozing.

## Yechim (C# kodi):
```csharp
using System;

abstract class Foydalanuvchi { public string Ism { get; set; } = ""; }
interface IHuquqli { bool RuxsatBormi(); }

class Admin : Foydalanuvchi, IHuquqli
{
    public bool RuxsatBormi() => true;
}

class XavfsizlikTekshiruvchi
{
    public static void Tekshir<T>(T shaxs) where T : Foydalanuvchi, IHuquqli
    {
        Console.WriteLine($"Foydalanuvchi: {shaxs.Ism}, Ruxsat: {shaxs.RuxsatBormi()}");
    }
}

internal class Program
{
    static void Main()
    {
        var admin = new Admin { Ism = "Botir" };
        XavfsizlikTekshiruvchi.Tekshir(admin);
    }
}

```

## Tushuntirish va Mantiq:
Bir vaqtning o'zida ham ota sinf (`Foydalanuvchi`), ham interfeys (`IHuquqli`) cheklovlarini qo'yish orqali metod ichida ikkala turdagi barcha xossa va metodlarni to'g'ridan-to'g'ri chaqirish mumkin bo'ladi.

## Ishlash natijasi:
```text
Foydalanuvchi: Botir, Ruxsat: True
```

# 459-Topshiriq: Generik cheklov: where T : unmanaged (Xom xotira turlari)
## Topshiriq sharti:
Heap havolalariga mutlaqo ega bo'lmagan, faqat xom xotira strukturalari uchun `unmanaged` cheklovidan foydalaning.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.InteropServices;

internal class Program
{
    static unsafe int BaytHajmi<T>() where T : unmanaged
    {
        // unmanaged cheklovi 'sizeof(T)' ni unsafe kontekstda chaqirishga ruxsat beradi
        return sizeof(T);
    }

    struct Nuqta { public int X, Y; }

    static void Main()
    {
        Console.WriteLine($"int hajmi: {BaytHajmi<int>()} bayt");
        Console.WriteLine($"double hajmi: {BaytHajmi<double>()} bayt");
        Console.WriteLine($"Nuqta hajmi: {BaytHajmi<Nuqta>()} bayt");

        // BaytHajmi<string>(); // XATO! string unmanaged emas (Heap obyekti)
    }
}

```

## Tushuntirish va Mantiq:
`where T : unmanaged` C# 7.3 da kiritilgan bo'lib, `T` ning faqat primitiv sonlar yoki ichida birorta ham havola turi bo'lmagan struktura ekanligini kafolatlaydi. Bu ko'rsatkichlar (pointers) va past darajadagi xotira amallari uchun kerak.

## Ishlash natijasi:
```text
int hajmi: 4 bayt
double hajmi: 8 bayt
Nuqta hajmi: 8 bayt
```

# 460-Topshiriq: default(T) va default literali: Turlarning nol qiymatini olish
## Topshiriq sharti:
Generik parametrning standart qiymatini xavfsiz qaytaruvchi metod yozing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static T? StandartniOl<T>()
    {
        // T int bo'lsa 0, bool bo'lsa false, string bo'lsa null qaytaradi
        return default;
    }

    static void Main()
    {
        int defInt = StandartniOl<int>();
        bool defBool = StandartniOl<bool>();
        string? defStr = StandartniOl<string>();

        Console.WriteLine($"int default: {defInt}");
        Console.WriteLine($"bool default: {defBool}");
        Console.WriteLine($"string default: {(defStr == null ? "null" : defStr)}");
    }
}

```

## Tushuntirish va Mantiq:
`default(T)` yoki qisqa `default` generik parametrning xotiradagi nol qiymatini qaytaradi. Bu `T` qiymat yoki havola turi bo'lishidan qat'i nazar 100% xavfsiz initsializatsiyani ta'minlaydi.

## Ishlash natijasi:
```text
int default: 0
bool default: False
string default: null
```

# 461-Topshiriq: Generik statik a'zolar va alohida xotira taqsimoti
## Topshiriq sharti:
Generik sinfning statik maydonlari har bir `T` turi uchun butunlay alohida nusxada yashashini isbotlang.

## Yechim (C# kodi):
```csharp
using System;

class Sanagich<T>
{
    public static int Soni = 0;
}

internal class Program
{
    static void Main()
    {
        Sanagich<int>.Soni = 10;
        Sanagich<string>.Soni = 50;

        Console.WriteLine($"Sanagich<int>:    {Sanagich<int>.Soni}");
        Console.WriteLine($"Sanagich<string>: {Sanagich<string>.Soni}");
    }
}

```

## Tushuntirish va Mantiq:
CLR har bir yopiq generik tur (`Sanagich<int>` va `Sanagich<string>`) uchun alohida MethodTable va alohida statik xotira maydoni ajratadi. Ular bir-biriga mutlaqo aralashmaydi.

## Ishlash natijasi:
```text
Sanagich<int>:    10
Sanagich<string>: 50
```

# 462-Topshiriq: Generik statik kesh naqshi (Generic Type Caching)
## Topshiriq sharti:
`typeof(T)` ni har safar chaqirmasdan, generik statik sinf orqali ma'lumotlarni o'ta tezkor keshlashtiring.

## Yechim (C# kodi):
```csharp
using System;

static class TurKeshi<T>
{
    // Bir martagina hisoblanadi va har bir T uchun xotirada qoladi
    public static readonly string Turi = typeof(T).FullName ?? "";
    public static readonly int XotiraHajmi = System.Runtime.CompilerServices.Unsafe.SizeOf<T>();
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine($"Kesh int:    {TurKeshi<int>.Turi}, Hajmi: {TurKeshi<int>.XotiraHajmi} bayt");
        Console.WriteLine($"Kesh double: {TurKeshi<double>.Turi}, Hajmi: {TurKeshi<double>.XotiraHajmi} bayt");
    }
}

```

## Tushuntirish va Mantiq:
Generik statik kesh naqshi lug'at (`Dictionary<Type, ...>`) qidiruviga nisbatan bir necha barobar tez ishlaydi, chunki unda xesh hisoblash yo'q — protsessor to'g'ridan-to'g'ri statik xotira manziliga sakraydi.

## Ishlash natijasi:
```text
Kesh int:    System.Int32, Hajmi: 4 bayt
Kesh double: System.Double, Hajmi: 8 bayt
```

# 463-Topshiriq: Bir nechta tur parametriga ega sinf: Juftlik<TKey, TValue>
## Topshiriq sharti:
Kalit va qiymat juftligini ifodalovchi ikki parametrli generik sinf yarating.

## Yechim (C# kodi):
```csharp
using System;

class Juftlik<TKey, TValue>
{
    public TKey Kalit { get; }
    public TValue Qiymat { get; }

    public Juftlik(TKey k, TValue v) => (Kalit, Qiymat) = (k, v);

    public override string ToString() => $"[{Kalit}] => {Qiymat}";
}

internal class Program
{
    static void Main()
    {
        var sozlama = new Juftlik<string, int>("MaxLimit", 500);
        var xodim = new Juftlik<int, string>(101, "Dilshod");

        Console.WriteLine(sozlama);
        Console.WriteLine(xodim);
    }
}

```

## Tushuntirish va Mantiq:
Generik turlar bir nechta parametrlarga ega bo'lishi mumkin (masalan `Dictionary<TKey, TValue>`, `Tuple<T1, T2, T3>`). Har bir parametr o'zining shaxsiy cheklovlariga ega bo'lishi mumkin.

## Ishlash natijasi:
```text
[MaxLimit] => 500
[101] => Dilshod
```

# 464-Topshiriq: Kovariantlik (Covariance: out T): Quvvatli o'qish shartnomasi
## Topshiriq sharti:
`out T` modifikatori yordamida bola turdagi to'plamni ota turdagi interfeysga xavfsiz o'zlashtiring.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

interface IOqiladiganOqim<out T>
{
    T ElementniBer(); // Faqat chiqish (out) pozitsiyasida bo'lishi shart!
}

class Oqim<T> : IOqiladiganOqim<T>
{
    private T val;
    public Oqim(T v) => val = v;
    public T ElementniBer() => val;
}

class Ota { }
class Bola : Ota { }

internal class Program
{
    static void Main()
    {
        IOqiladiganOqim<Bola> bolaOqim = new Oqim<Bola>(new Bola());

        // Kovariantlik tufayli: Bola o'rniga Ota interfeysiga o'tish mumkin!
        IOqiladiganOqim<Ota> otaOqim = bolaOqim;

        Console.WriteLine($"Kovariant chaqiruv muvaffaqiyatli: {otaOqim.ElementniBer().GetType().Name}");
    }
}

```

## Tushuntirish va Mantiq:
Kovariantlik (`out T`) faqat qiymat qaytaruvchi metodlarga ruxsat beradi (parametr qabul qila olmaydi). Bu bola turdagi obyektlar oqimini ota turdagi oqimga bemalol o'girish (masalan `IEnumerable<string>` ni `IEnumerable<object>` deb ishlatish) imkonini yaratadi.

## Ishlash natijasi:
```text
Kovariant chaqiruv muvaffaqiyatli: Bola
```

# 465-Topshiriq: Kontravariantlik (Contravariance: in T): Moslashuvchan qabul qiluvchi
## Topshiriq sharti:
`in T` modifikatori yordamida ota turni qabul qiluvchi xizmatni bola turni qabul qiluvchi joyda ishlating.

## Yechim (C# kodi):
```csharp
using System;

interface IQabulQiluvchi<in T>
{
    void QabulQil(T element); // Faqat kirish (in) pozitsiyasida bo'lishi shart!
}

class Ota { }
class Bola : Ota { }

class OtaQabulchi : IQabulQiluvchi<Ota>
{
    public void QabulQil(Ota e) => Console.WriteLine($"Ota qabul qilindi: {e.GetType().Name}");
}

internal class Program
{
    static void Main()
    {
        IQabulQiluvchi<Ota> otaServis = new OtaQabulchi();

        // Kontravariantlik: Ota ni qabul qiluvchi servis Bola ni ham bemalol qabul qila oladi!
        IQabulQiluvchi<Bola> bolaServis = otaServis;

        bolaServis.QabulQil(new Bola());
    }
}

```

## Tushuntirish va Mantiq:
Kontravariantlik (`in T`) teskari yo'nalishda ishlaydi: agar servis `Ota` ni qabul qila olsa, uning har qanday vorisi bo'lgan `Bola` ni ham bemalol qabul qila oladi. `Action<T>` va `IComparable<T>` aynan shunday ishlaydi.

## Ishlash natijasi:
```text
Ota qabul qilindi: Bola
```

# 466-Topshiriq: Invariantlik: Nega IList<T> kovariant bo'la olmaydi?
## Topshiriq sharti:
Ham o'quvchi, ham yozuvchi to'plamlarda kovariantlik nima uchun xavfsizlik nuqtai nazaridan taqiqlanganini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        // Agar List<T> kovariant bo'lganida quyidagi xatolik ro'y berardi:
        // List<string> satrlar = new List<string>();
        // List<object> obyektlar = satrlar; // XAYOLAN
        // obyektlar.Add(12345); // XATO! Satrlar ro'yxatiga butun son tushib qolardi!

        Console.WriteLine("Invariantlik qoidasi: Agar to'plam ham o'qisa, ham yozsa (IList<T>),");
        Console.WriteLine("u qat'iy Invariant bo'lishi shart, ya'ni List<Bola> ni List<Ota> ga berib bo'lmaydi.");
    }
}

```

## Tushuntirish va Mantiq:
Agar ham o'qish, ham yozish mumkin bo'lgan to'plamlar kovariant bo'lganida, ro'yxatga noto'g'ri turdagi ob'yektlarni tiqib yuborish mumkin bo'lib qolardi. Shuning uchun `List<T>` faqat o'z turiga teng bo'lishi shart (Invariant).

## Ishlash natijasi:
```text
Invariantlik qoidasi: Agar to'plam ham o'qisa, ham yozsa (IList<T>),
u qat'iy Invariant bo'lishi shart, ya'ni List<Bola> ni List<Ota> ga berib bo'lmaydi.
```

# 467-Topshiriq: Generik strukturalar: Option<T> modeli
## Topshiriq sharti:
`null` ishlatmasdan qiymat bor yoki yo'qligini ifodalovchi yengil generik struct yarating.

## Yechim (C# kodi):
```csharp
using System;

readonly struct Option<T>
{
    private readonly bool mavjud;
    private readonly T qiymat;

    public bool HasValue => mavjud;
    public T Value => mavjud ? qiymat : throw new InvalidOperationException("Qiymat mavjud emas!");

    public Option(T val)
    {
        mavjud = true;
        qiymat = val;
    }

    public static Option<T> None => default;
    public static Option<T> Some(T val) => new(val);
}

internal class Program
{
    static void Main()
    {
        var bor = Option<int>.Some(42);
        var yoq = Option<int>.None;

        Console.WriteLine($"bor.HasValue: {bor.HasValue}, Qiymat: {bor.Value}");
        Console.WriteLine($"yoq.HasValue: {yoq.HasValue}");
    }
}

```

## Tushuntirish va Mantiq:
Generik strukturalar Stack xotirada yashab, Heap da ortiqcha ob'yekt ajratmasdan zamonaviy funksional tushunchalarni (masalan `Option<T>`) tezkor amalga oshirish imkonini beradi.

## Ishlash natijasi:
```text
bor.HasValue: True, Qiymat: 42
yoq.HasValue: False
```

# 468-Topshiriq: Curiously Recurring Template Pattern (CRTP) C# da
## Topshiriq sharti:
`where T : IComparable<T>` kabi o'z-o'ziga bog'langan rekursiv generik cheklovni tahlil qiling.

## Yechim (C# kodi):
```csharp
using System;

abstract class BazaModel<T> where T : BazaModel<T>
{
    public abstract bool BirXilmi(T boshqa);
}

class Foydalanuvchi : BazaModel<Foydalanuvchi>
{
    public int Id { get; set; }

    public override bool BirXilmi(Foydalanuvchi boshqa) => Id == boshqa.Id;
}

internal class Program
{
    static void Main()
    {
        var f1 = new Foydalanuvchi { Id = 10 };
        var f2 = new Foydalanuvchi { Id = 10 };

        Console.WriteLine($"Bir xilmi: {f1.BirXilmi(f2)}");
    }
}

```

## Tushuntirish va Mantiq:
CRTP naqshida bola sinf o'z nomini ota sinfning generik parametri sifatida uzatadi (`class Foydalanuvchi : BazaModel<Foydalanuvchi>`). Bu ota sinfda aynan bola sinf turidagi metodlarni kuchli tiplash bilan yozishga imkon beradi.

## Ishlash natijasi:
```text
Bir xilmi: True
```

# 469-Topshiriq: C# 7.3 Enum generik cheklovi: where T : System.Enum
## Topshiriq sharti:
Faqat `enum` turlari bilan ishlovchi va ularning barcha nomlarini chiqaruvchi yordamchi metod yozing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void EnumElementlariniChiqar<T>() where T : struct, Enum
    {
        Console.WriteLine($"[{typeof(T).Name}] elementlari:");
        foreach (var nom in Enum.GetNames<T>())
        {
            Console.WriteLine($"- {nom}");
        }
    }

    enum Rang { Oq, Qora }

    static void Main()
    {
        EnumElementlariniChiqar<Rang>();
    }
}

```

## Tushuntirish va Mantiq:
C# 7.3 gacha `enum` cheklovini qo'yish taqiqlangan edi. Endilikda `where T : struct, Enum` orqali faqat sanab o'tiladigan turlar bilan ishlovchi xavfsiz metodlar yozish mumkin.

## Ishlash natijasi:
```text
[Rang] elementlari:
- Oq
- Qora
```

# 470-Topshiriq: C# 7.3 Delegate generik cheklovi: where T : System.Delegate
## Topshiriq sharti:
Faqat delegatlar bilan ishlovchi generik metod tuzing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void DelegatTekshir<T>(T delegat) where T : Delegate
    {
        Console.WriteLine($"Delegat metodi nomi: {delegat.Method.Name}");
    }

    static void Salom() => Console.WriteLine("Salom!");

    static void Main()
    {
        Action act = Salom;
        DelegatTekshir(act);
    }
}

```

## Tushuntirish va Mantiq:
`where T : Delegate` cheklovi parametr faqat metod ko'rsatkichi (delegat) bo'lishini kafolatlaydi va uning `Method` hamda `Target` xossalaridan xavfsiz foydalanish imkonini beradi.

## Ishlash natijasi:
```text
Delegat metodi nomi: Salom
```

# 471-Topshiriq: JIT kompilyatsiyasi: Reference vs Value Types generiklari
## Topshiriq sharti:
.NET JIT kompilyatori Value Type va Reference Type generiklarini qanday mashina kodiga aylantirishini tushuntiring.

## Yechim (C# kodi):
```csharp
using System;

class Konteyner<T> { public T Element; }

internal class Program
{
    static void Main()
    {
        // Value Type: Har bir struct uchun (int, double) alohida optimallashgan mashina kodi yaratiladi!
        var c1 = new Konteyner<int>();
        var c2 = new Konteyner<double>();

        // Reference Type: Barcha sinflar (string, object, Xodim) uchun bitta umumiy ko'rsatkichli kod ulashiladi!
        var c3 = new Konteyner<string>();
        var c4 = new Konteyner<object>();

        Console.WriteLine("JIT arxitekturasi: Value Types uchun ixtisoslashuv (Specialization),");
        Console.WriteLine("Reference Types uchun esa kod bo'lishish (Code Sharing) orqali xotira tejaladi.");
    }
}

```

## Tushuntirish va Mantiq:
CLR generiklarni ajoyib tarzda optimallashtiradi: barcha havolali turlar 64-bit ko'rsatkich bo'lgani uchun bitta umumiy mashina kodi generatsiya qilinadi. Har bir `struct` uchun esa alohida moslashtirilgan tezyurar xotira kodi hosil qilinadi.

## Ishlash natijasi:
```text
JIT arxitekturasi: Value Types uchun ixtisoslashuv (Specialization),
Reference Types uchun esa kod bo'lishish (Code Sharing) orqali xotira tejaladi.
```

# 472-Topshiriq: Generik Ro'yxatni noldan qurish: GenericList<T>
## Topshiriq sharti:
O'z ichida massiv saqlovchi va avtomatik kengayuvchi oddiy `GenericList<T>` sinfini yarating.

## Yechim (C# kodi):
```csharp
using System;

class OddiyList<T>
{
    private T[] massiv = new T[2];
    public int Count { get; private set; } = 0;

    public void Add(T element)
    {
        if (Count == massiv.Length)
        {
            Array.Resize(ref massiv, massiv.Length * 2); // 2 barobar kengaytirish
        }
        massiv[Count++] = element;
    }

    public T this[int indeks] => massiv[indeks];
}

internal class Program
{
    static void Main()
    {
        var royxat = new OddiyList<int>();
        royxat.Add(10);
        royxat.Add(20);
        royxat.Add(30);

        Console.WriteLine($"Elementlar soni: {royxat.Count}");
        Console.WriteLine($"2-indeks: {royxat[2]}");
    }
}

```

## Tushuntirish va Mantiq:
`List<T>` ning ichki arxitekturasi aynan shunday ishlaydi: hajmi to'lganda massiv 2 barobar kattalashtiriladi va elementlar ko'chiriladi.

## Ishlash natijasi:
```text
Elementlar soni: 3
2-indeks: 30
```

# 473-Topshiriq: Generik Stack (LIFO) ni noldan amalga oshirish
## Topshiriq sharti:
Oxirgi kirgan birinchi chiqadi (LIFO) qoidasi asosida ishlovchi generik `MyStack<T>` sinfini yozing.

## Yechim (C# kodi):
```csharp
using System;

class MyStack<T>
{
    private T[] elementlar = new T[4];
    private int tepaIndeks = 0;

    public void Push(T element)
    {
        if (tepaIndeks == elementlar.Length) Array.Resize(ref elementlar, elementlar.Length * 2);
        elementlar[tepaIndeks++] = element;
    }

    public T Pop()
    {
        if (tepaIndeks == 0) throw new InvalidOperationException("Stack bo'sh!");
        T olingan = elementlar[--tepaIndeks];
        elementlar[tepaIndeks] = default!; // Xotirani tozalash (GC uchun)
        return olingan;
    }
}

internal class Program
{
    static void Main()
    {
        var st = new MyStack<string>();
        st.Push("Birinchi");
        st.Push("Ikkinchi");

        Console.WriteLine($"Pop: {st.Pop()}");
        Console.WriteLine($"Pop: {st.Pop()}");
    }
}

```

## Tushuntirish va Mantiq:
Stack ma'lumotlar tuzilmasi rekursiya, orqaga qaytish (Undo) va qavslarni tekshirish algoritmlarining poydevoridir.

## Ishlash natijasi:
```text
Pop: Ikkinchi
Pop: Birinchi
```

# 474-Topshiriq: Generik Queue (FIFO) ni noldan amalga oshirish
## Topshiriq sharti:
Birinchi kelgan birinchi chiqadi (FIFO) qoidasi bo'yicha navbat sinfini yozing.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

class MyQueue<T>
{
    private readonly List<T> royxat = new();

    public void Enqueue(T element) => royxat.Add(element);

    public T Dequeue()
    {
        if (royxat.Count == 0) throw new InvalidOperationException("Navbat bo'sh!");
        T birinchi = royxat[0];
        royxat.RemoveAt(0);
        return birinchi;
    }

    public int Count => royxat.Count;
}

internal class Program
{
    static void Main()
    {
        var q = new MyQueue<int>();
        q.Enqueue(100);
        q.Enqueue(200);

        Console.WriteLine($"Navbatdan chiqdi: {q.Dequeue()}");
        Console.WriteLine($"Navbatdan chiqdi: {q.Dequeue()}");
    }
}

```

## Tushuntirish va Mantiq:
Queue to'plami xabarlar navbati (Message Queuing), printer navbatlari va kenglik bo'yicha qidiruv (BFS) algoritmlarida qo'llaniladi.

## Ishlash natijasi:
```text
Navbatdan chiqdi: 100
Navbatdan chiqdi: 200
```

# 475-Topshiriq: Generik Bog'langan Ro'yxat (LinkedList) va Tugunlar (Node<T>)
## Topshiriq sharti:
O'zaro havolalar bilan bog'langan generik zanjir elementlarini quring.

## Yechim (C# kodi):
```csharp
using System;

class Tugun<T>
{
    public T Qiymat { get; }
    public Tugun<T>? Keyingi { get; set; }

    public Tugun(T q) => Qiymat = q;
}

internal class Program
{
    static void Main()
    {
        var t1 = new Tugun<string>("Bosh");
        var t2 = new Tugun<string>("O'rta");
        var t3 = new Tugun<string>("Oxir");

        t1.Keyingi = t2;
        t2.Keyingi = t3;

        Tugun<string>? joriy = t1;
        Console.Write("Zanjir: ");
        while (joriy != null)
        {
            Console.Write($"{joriy.Qiymat} -> ");
            joriy = joriy.Keyingi;
        }
        Console.WriteLine("null");
    }
}

```

## Tushuntirish va Mantiq:
Bog'langan ro'yxatlarda elementlar xotiraning ixtiyoriy joylarida tarqoq yashaydi va faqat ko'rsatkichlar orqali bir-biriga ulanadi. Bu o'rtaga yangi element qo'shishni $O(1)$ qiladi.

## Ishlash natijasi:
```text
Zanjir: Bosh -> O'rta -> Oxir -> null
```

# 476-Topshiriq: Generik Lug'at (Dictionary<TKey, TValue>) va GetHashCode mantiqi
## Topshiriq sharti:
Generik kalit-qiymat saqlovchi mini `Lugat<TKey, TValue>` tuzilmasini yozing.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

class Element<TKey, TValue>
{
    public TKey Kalit { get; }
    public TValue Qiymat { get; set; }
    public Element(TKey k, TValue q) { Kalit = k; Qiymat = q; }
}

class OddiyLugat<TKey, TValue> where TKey : notnull
{
    private List<Element<TKey, TValue>> royxat = new();

    public void Add(TKey kalit, TValue qiymat)
    {
        foreach (var item in royxat)
        {
            if (EqualityComparer<TKey>.Default.Equals(item.Kalit, kalit))
                throw new ArgumentException("Kalit allaqachon mavjud!");
        }
        royxat.Add(new Element<TKey, TValue>(kalit, qiymat));
    }

    public TValue this[TKey kalit]
    {
        get
        {
            foreach (var item in royxat)
            {
                if (EqualityComparer<TKey>.Default.Equals(item.Kalit, kalit))
                    return item.Qiymat;
            }
            throw new KeyNotFoundException();
        }
    }
}

internal class Program
{
    static void Main()
    {
        var lugat = new OddiyLugat<string, int>();
        lugat.Add("Toshkent", 3000000);
        lugat.Add("Samarqand", 600000);

        Console.WriteLine($"Toshkent aholisi: {lugat["Toshkent"]}");
    }
}

```

## Tushuntirish va Mantiq:
TKey uchun `EqualityComparer<TKey>.Default` ishlatiladi, bu boxing sodir etmasdan IEqualityComparer interfeysi orqali xesh va tenglikni tekshiradi.

## Ishlash natijasi:
```text
Toshkent aholisi: 3000000
```

# 477-Topshiriq: Generik Binar Daraxt (Binary Search Tree - BST)
## Topshiriq sharti:
Tugunlarida tartiblangan ma'lumot saqlovchi generik binar qidiruv daraxtini yarating.

## Yechim (C# kodi):
```csharp
using System;

class DaraxtTuguni<T> where T : IComparable<T>
{
    public T Qiymat { get; set; }
    public DaraxtTuguni<T>? Chap { get; set; }
    public DaraxtTuguni<T>? Ong { get; set; }

    public DaraxtTuguni(T qiymat) => Qiymat = qiymat;

    public void Qoshish(T yangi)
    {
        if (yangi.CompareTo(Qiymat) < 0)
        {
            if (Chap == null) Chap = new DaraxtTuguni<T>(yangi);
            else Chap.Qoshish(yangi);
        }
        else
        {
            if (Ong == null) Ong = new DaraxtTuguni<T>(yangi);
            else Ong.Qoshish(yangi);
        }
    }

    public void InOrderChop()
    {
        Chap?.InOrderChop();
        Console.Write($"{Qiymat} ");
        Ong?.InOrderChop();
    }
}

internal class Program
{
    static void Main()
    {
        var ildiz = new DaraxtTuguni<int>(50);
        ildiz.Qoshish(30);
        ildiz.Qoshish(70);
        ildiz.Qoshish(20);
        ildiz.Qoshish(40);

        Console.Write("Tartiblangan daraxt: ");
        ildiz.InOrderChop();
        Console.WriteLine();
    }
}

```

## Tushuntirish va Mantiq:
IComparable<T> cheklovi elementlarni kattalik bo'yicha chap va o'ng tarmoqlarga ajratish imkonini beradi.

## Ishlash natijasi:
```text
Tartiblangan daraxt: 20 30 40 50 70
```

# 478-Topshiriq: Prioritet Navbati (.NET 6+ PriorityQueue<TElement, TPriority>)
## Topshiriq sharti:
Muhimlik darajasi (priority) bo'yicha ishlovchi standart `PriorityQueue` dan foydalaning.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        // Kichik son = yuqori prioritet (Min-Heap)
        var navbat = new PriorityQueue<string, int>();

        navbat.Enqueue("Keshni tozalash", 3);
        navbat.Enqueue("Tizim halokati (CRITICAL)", 1);
        navbat.Enqueue("Email jo'natish", 2);

        Console.WriteLine("Navbat tartibi:");
        while (navbat.Count > 0)
        {
            string vazifa = navbat.Dequeue();
            Console.WriteLine($"- {vazifa}");
        }
    }
}

```

## Tushuntirish va Mantiq:
PriorityQueue<TElement, TPriority> ikkilik piramida (Binary Heap) asosida qurilgan bo'lib, eng ustuvor elementni $O(\log N)$ vaqtda sug'urib oladi.

## Ishlash natijasi:
```text
Navbat tartibi:
- Tizim halokati (CRITICAL)
- Email jo'natish
- Keshni tozalash
```

# 479-Topshiriq: Kovariantlik (Covariance: out T) tushunchasi
## Topshiriq sharti:
Kichik tipdan katta tipga havolani xavfsiz o'tkazuvchi kovariant interfeys yarating.

## Yechim (C# kodi):
```csharp
using System;

class Hayvon { public string Tur => "Hayvon"; }
class Mushuk : Hayvon { }

interface IMahsulotBeruvchi<out T>
{
    T IshlabChiqar(); // T faqat chiqish (output) pozitsiyasida bo'lishi shart!
}

class MushukKopaytiruvchi : IMahsulotBeruvchi<Mushuk>
{
    public Mushuk IshlabChiqar() => new Mushuk();
}

internal class Program
{
    static void Main()
    {
        IMahsulotBeruvchi<Mushuk> mushukchi = new MushukKopaytiruvchi();
        
        // Kovariantlik tufayli IMahsulotBeruvchi<Mushuk> ni IMahsulotBeruvchi<Hayvon> ga tenglash mumkin:
        IMahsulotBeruvchi<Hayvon> hayvonchi = mushukchi;

        Hayvon h = hayvonchi.IshlabChiqar();
        Console.WriteLine($"Kovariantlik orqali olingan obyekt turi: {h.GetType().Name}");
    }
}

```

## Tushuntirish va Mantiq:
`out T` kalit so'zi kovariantlikni bildiradi. Bu yerda Mushuk Hayvondan kelib chiqqani sababli `IMahsulotBeruvchi<Mushuk>` bemalol `IMahsulotBeruvchi<Hayvon>` sifatida qaralishi mumkin. Chunki u faqat Mushuk qaytaradi, bu esa Hayvon talabiga to'liq mos keladi.

## Ishlash natijasi:
```text
Kovariantlik orqali olingan obyekt turi: Mushuk
```

# 480-Topshiriq: Kovariantlik amaliyoti: IEnumerable<out T> va IReadOnlyList<out T>
## Topshiriq sharti:
.NET BCL dagi o'rnatilgan kovariant interfeyslarning xatti-harakatini tekshiring.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

class Bino { public virtual string Nomi => "Oddiy bino"; }
class Maktab : Bino { public override string Nomi => "Prezident maktabi"; }

internal class Program
{
    static void Main()
    {
        List<Maktab> maktablar = new List<Maktab>
        {
            new Maktab(),
            new Maktab()
        };

        // IEnumerable<out T> kovariant, shuning uchun List<Maktab> ni IEnumerable<Bino> ga o'tkazish mumkin!
        IEnumerable<Bino> binolar = maktablar;

        foreach (var b in binolar)
        {
            Console.WriteLine(b.Nomi);
        }
    }
}

```

## Tushuntirish va Mantiq:
IEnumerable<out T> faqat elementlarni o'qish (output) imkonini berganligi uchun unga nisbatan kovariantlik 100% xavfsiz hisoblanadi.

## Ishlash natijasi:
```text
Prezident maktabi
Prezident maktabi
```

# 481-Topshiriq: Kontravariantlik (Contravariance: in T) tushunchasi
## Topshiriq sharti:
Katta tipdan kichik tipga o'tuvchi `in T` parametrli interfeys yarating.

## Yechim (C# kodi):
```csharp
using System;

class Ozuqa { public string Nomi { get; set; } = "Oddiy ozuqa"; }
class BaliqOzuqasi : Ozuqa { }

interface IYeyuvchi<in T>
{
    void Yeyish(T ozuqa); // T faqat kirish (input) pozitsiyasida bo'lishi shart!
}

class HayvonOzuqaQabulQiluvchi : IYeyuvchi<Ozuqa>
{
    public void Yeyish(Ozuqa ozuqa) => Console.WriteLine($"Hayvon ozuqani yedi: {ozuqa.Nomi}");
}

internal class Program
{
    static void Main()
    {
        IYeyuvchi<Ozuqa> umumiyYeyuvchi = new HayvonOzuqaQabulQiluvchi();

        // Kontravariantlik: IYeyuvchi<Ozuqa> ni IYeyuvchi<BaliqOzuqasi> ga o'giramiz!
        IYeyuvchi<BaliqOzuqasi> baliqchi = umumiyYeyuvchi;

        baliqchi.Yeyish(new BaliqOzuqasi { Nomi = "Mayda baliq donasi" });
    }
}

```

## Tushuntirish va Mantiq:
`in T` kontravariantlikni bildiradi. Agar metod umumiy `Ozuqa`ni qabul qila olsa, demak u har qanday xususiy `BaliqOzuqasi`ni ham qabul qila oladi. Shuning uchun havola yo'nalishi teskariga buriladi.

## Ishlash natijasi:
```text
Hayvon ozuqani yedi: Mayda baliq donasi
```

# 482-Topshiriq: Kontravariantlik amaliyoti: Action<in T> va IComparer<in T>
## Topshiriq sharti:
Standart `Action<in T>` delegatining kontravariant imkoniyatini ko'ring.

## Yechim (C# kodi):
```csharp
using System;

class Inson { public string Ism { get; set; } = "Noma'lum"; }
class Xodim : Inson { public decimal Maosh { get; set; } }

internal class Program
{
    static void Main()
    {
        // Inson qabul qiluvchi delegat
        Action<Inson> chopEtish = inson => Console.WriteLine($"Inson ismi: {inson.Ism}");

        // Action<in T> kontravariant bo'lgani uchun uni Action<Xodim> ga berish mumkin
        Action<Xodim> xodimChopEtish = chopEtish;

        xodimChopEtish(new Xodim { Ism = "Alisher", Maosh = 5000000 });
    }
}

```

## Tushuntirish va Mantiq:
`Action<in T>` delegati parametrlarni faqat qabul qiladi (iste'molchi). Xodim Inson ekan, Insonni qabul qiluvchi har qanday funksiya Xodimni ham bemalol qabul qila oladi.

## Ishlash natijasi:
```text
Inson ismi: Alisher
```

# 483-Topshiriq: Invariantlik: Nima uchun List<T> kovariant bo'la olmaydi?
## Topshiriq sharti:
`List<T>` ning invariant ekanligini va nima uchun `List<Hayvon> = List<Mushuk>` taqiqlanganligini tahlil qiling.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

class Hayvon { }
class Kuchuk : Hayvon { }
class Mushuk : Hayvon { }

internal class Program
{
    static void Main()
    {
        List<Mushuk> mushuklar = new List<Mushuk>();

        // Agar bu kompilyatsiya bo'lganida nima sodir bo'lardi?
        // List<Hayvon> hayvonlar = mushuklar; // KOMPILYATSIYA XATOSI!
        // hayvonlar.Add(new Kuchuk()); // DAHSHAT: Mushuklar ro'yxatiga Kuchuk qo'shilib qolardi!

        Console.WriteLine("List<T> invariant: Ham o'qiydi (out), ham yozadi (in). Tip xavfsizligi kafolatlangan.");
    }
}

```

## Tushuntirish va Mantiq:
Agar konteyner ham o'qish (out), ham yozish (in) operatsiyalarini bajarsa, u invariant (o'zgarmas) bo'lishi shart. Aks holda boshqa voris sinflar begona ro'yxatga tushib, xotirani buzar edi.

## Ishlash natijasi:
```text
List<T> invariant: Ham o'qiydi (out), ham yozadi (in). Tip xavfsizligi kafolatlangan.
```

# 484-Topshiriq: CRTP (Curiously Recurring Template Pattern) va IComparable<T>
## Topshiriq sharti:
Sinf o'zining turini generik parametr qilib uzatuvchi CRTP arxitektura naqshini yozing.

## Yechim (C# kodi):
```csharp
using System;

abstract class Obekt<T> : IComparable<T> where T : Obekt<T>
{
    public int Id { get; set; }
    public abstract int CompareTo(T? other);
}

class Mahsulot : Obekt<Mahsulot>
{
    public string Nomi { get; set; } = "";

    public override int CompareTo(Mahsulot? other)
    {
        if (other == null) return 1;
        return Id.CompareTo(other.Id);
    }
}

internal class Program
{
    static void Main()
    {
        var m1 = new Mahsulot { Id = 10, Nomi = "Non" };
        var m2 = new Mahsulot { Id = 20, Nomi = "Choy" };

        int natija = m1.CompareTo(m2);
        Console.WriteLine($"m1 m2 dan kichikmi: {natija < 0}");
    }
}

```

## Tushuntirish va Mantiq:
CRTP naqshida bazaviy sinf o'z vorisining aniq turidan xabardor bo'ladi va tiplar orasida type-cast qilishga ehtiyoj qoldirmaydi.

## Ishlash natijasi:
```text
m1 m2 dan kichikmi: True
```

# 485-Topshiriq: Generik statik konstruktor va alohida statik xotira
## Topshiriq sharti:
Generik sinfning statik a'zolari har bir alohida yopiq tur (closed type) uchun mustaqil yaratilishini isbotlang.

## Yechim (C# kodi):
```csharp
using System;

class Hisoblagich<T>
{
    public static int Son = 0;

    static Hisoblagich()
    {
        Console.WriteLine($"Statik konstruktor ishga tushdi: {typeof(T).Name}");
    }
}

internal class Program
{
    static void Main()
    {
        Hisoblagich<int>.Son++;
        Hisoblagich<int>.Son++;

        Hisoblagich<string>.Son++;

        Console.WriteLine($"Hisoblagich<int>.Son = {Hisoblagich<int>.Son}");
        Console.WriteLine($"Hisoblagich<string>.Son = {Hisoblagich<string>.Son}");
    }
}

```

## Tushuntirish va Mantiq:
CLR har bir yopiq generik tur (`Hisoblagich<int>`, `Hisoblagich<string>`) uchun metodlar jadvali (Method Table) va alohida statik ma'lumotlar maydonini ajratadi. Ular umumiy statik maydonga ega emas.

## Ishlash natijasi:
```text
Statik konstruktor ishga tushdi: Int32
Statik konstruktor ishga tushdi: String
Hisoblagich<int>.Son = 2
Hisoblagich<string>.Son = 1
```

# 486-Topshiriq: Generik Statik Kesh Naqshi (Generic Static Cache Pattern)
## Topshiriq sharti:
Dictionary qidiruvidan ko'ra $O(1)$ darajasida tez ishlovchi statik generik kesh yarating.

## Yechim (C# kodi):
```csharp
using System;

class TurIdentifikatori<T>
{
    public static readonly int Id;
    private static int hisob = 0;

    static TurIdentifikatori()
    {
        Id = ++hisob;
    }
}

class Generator
{
    private static int globalId = 0;
    public static int OlishId<T>() => StaticCache<T>.Id;

    private static class StaticCache<T>
    {
        public static readonly int Id = System.Threading.Interlocked.Increment(ref globalId);
    }
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine($"int ID: {Generator.OlishId<int>()}");
        Console.WriteLine($"string ID: {Generator.OlishId<string>()}");
        Console.WriteLine($"double ID: {Generator.OlishId<double>()}");
        Console.WriteLine($"int qayta ID: {Generator.OlishId<int>()}");
    }
}

```

## Tushuntirish va Mantiq:
Generik statik kesh hech qanday qulflash (lock) yoki xesh-jadval qidiruvisiz, to'g'ridan-to'g'ri statik maydon xotirasiga murojaat orqali bir necha nanosekundda ishlaydi.

## Ishlash natijasi:
```text
int ID: 1
string ID: 2
double ID: 3
int qayta ID: 1
```

# 487-Topshiriq: Generik Metodda JIT 'Dead Code Elimination'
## Topshiriq sharti:
`typeof(T) == typeof(...)` tekshiruvi JIT tomonidan qanday optimallashishini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void TezChop<T>(T qiymat)
    {
        // JIT har bir qiymat turi uchun alohida mashina kodi generatsiya qiladi
        // va mos kelmagan if shoxlarini butunlay o'chirib tashlaydi (Branch elimination)
        if (typeof(T) == typeof(int))
        {
            Console.WriteLine($"JIT optimallashtirilgan int: {qiymat}");
        }
        else if (typeof(T) == typeof(string))
        {
            Console.WriteLine($"JIT optimallashtirilgan string: {qiymat}");
        }
        else
        {
            Console.WriteLine($"Umumiy obekt: {qiymat}");
        }
    }

    static void Main()
    {
        TezChop(100);
        TezChop("Salom .NET");
        TezChop(true);
    }
}

```

## Tushuntirish va Mantiq:
C# da `typeof(T) == typeof(int)` kabi tekshiruvlar JIT kompilyatsiyasi paytida o'zgarmas (const) deb topiladi va faqat bitta to'g'ri filial mashina kodida qoldirilib, qolganlari tozalanadi.

## Ishlash natijasi:
```text
JIT optimallashtirilgan int: 100
JIT optimallashtirilgan string: Salom .NET
Umumiy obekt: True
```

# 488-Topshiriq: Generik Record Struct: Result<T>
## Topshiriq sharti:
Xatolik yoki qiymatni nol xotira ajratish (zero heap allocation) bilan qaytaruvchi generik tuzilma yarating.

## Yechim (C# kodi):
```csharp
using System;

public readonly record struct Result<T>(bool IsSuccess, T? Value, string? Error)
{
    public static Result<T> Success(T value) => new(true, value, null);
    public static Result<T> Failure(string error) => new(false, default, error);
}

internal class Program
{
    static Result<int> Bolish(int a, int b)
    {
        if (b == 0) return Result<int>.Failure("Nolga bo'lish mumkin emas");
        return Result<int>.Success(a / b);
    }

    static void Main()
    {
        var res1 = Bolish(10, 2);
        if (res1.IsSuccess)
            Console.WriteLine($"Muvaffaqiyatli: {res1.Value}");

        var res2 = Bolish(10, 0);
        if (!res2.IsSuccess)
            Console.WriteLine($"Xatolik: {res2.Error}");
    }
}

```

## Tushuntirish va Mantiq:
readonly record struct stack xotirada joylashadi va heap xotiraga hech qanday yuk tushirmaydi.

## Ishlash natijasi:
```text
Muvaffaqiyatli: 5
Xatolik: Nolga bo'lish mumkin emas
```

# 489-Topshiriq: Generik Either<L, R> Funksional Naqshi
## Topshiriq sharti:
Ikkita turdan birini o'zida ifodalovchi funksional `Either` naqshini yarating.

## Yechim (C# kodi):
```csharp
using System;

class Either<TLeft, TRight>
{
    private readonly TLeft? chap;
    private readonly TRight? ong;
    private readonly bool isRight;

    private Either(TLeft chap) { this.chap = chap; isRight = false; }
    private Either(TRight ong) { this.ong = ong; isRight = true; }

    public static Either<TLeft, TRight> Left(TLeft chap) => new(chap);
    public static Either<TLeft, TRight> Right(TRight ong) => new(ong);

    public void Match(Action<TLeft> chapAmal, Action<TRight> ongAmal)
    {
        if (isRight) ongAmal(ong!);
        else chapAmal(chap!);
    }
}

internal class Program
{
    static Either<string, int> YoshniAniqlash(string matn)
    {
        if (int.TryParse(matn, out int yosh))
            return Either<string, int>.Right(yosh);
        return Either<string, int>.Left("Kiritilgan qiymat butun son emas!");
    }

    static void Main()
    {
        var res = YoshniAniqlash("25");
        res.Match(
            err => Console.WriteLine($"Xatolik: {err}"),
            yosh => Console.WriteLine($"Foydalanuvchi yoshi: {yosh}")
        );
    }
}

```

## Tushuntirish va Mantiq:
Funksional dasturlashda `Either` odatda xato (Left) yoki to'g'ri natijani (Right) ifodalash uchun ishlatiladi.

## Ishlash natijasi:
```text
Foydalanuvchi yoshi: 25
```

# 490-Topshiriq: Generik Builder (Fluent API) Naqshi
## Topshiriq sharti:
Generik tarzda ixtiyoriy obyektni quruvchi Fluent Builder sinfini yozing.

## Yechim (C# kodi):
```csharp
using System;

class ObyektQuruvchi<T> where T : class, new()
{
    private readonly T obekt = new();

    public ObyektQuruvchi<T> Sozlash(Action<T> amal)
    {
        amal(obekt);
        return this;
    }

    public T Qurish() => obekt;
}

class Kompyuter
{
    public string Protsessor { get; set; } = "";
    public int RAM { get; set; }
}

internal class Program
{
    static void Main()
    {
        var pc = new ObyektQuruvchi<Kompyuter>()
            .Sozlash(c => c.Protsessor = "Core i7")
            .Sozlash(c => c.RAM = 32)
            .Qurish();

        Console.WriteLine($"Qurilgan kompyuter: {pc.Protsessor}, {pc.RAM}GB RAM");
    }
}

```

## Tushuntirish va Mantiq:
Fluent API usulida metodlar o'z obyekti havolasini (`this`) qaytarib, chaqiriqlar zanjirini hosil qiladi.

## Ishlash natijasi:
```text
Qurilgan kompyuter: Core i7, 32GB RAM
```

# 491-Topshiriq: Generik Factory va `new()` cheklovi
## Topshiriq sharti:
Yangi obyekt nusxalarini xavfsiz yaratuvchi generik fabrika (Factory) tuzing.

## Yechim (C# kodi):
```csharp
using System;

interface IService
{
    void IshgaTush();
}

class EmailXizmati : IService
{
    public void IshgaTush() => Console.WriteLine("Email xizmati ishga tushirildi.");
}

class Fabrika
{
    public static T Yaratish<T>() where T : IService, new()
    {
        return new T();
    }
}

internal class Program
{
    static void Main()
    {
        IService xizmat = Fabrika.Yaratish<EmailXizmati>();
        xizmat.IshgaTush();
    }
}

```

## Tushuntirish va Mantiq:
`where T : new()` cheklovi CLR darajasida Activator chaqiruvini optimal tarzda bajarish yoki standart konstruktorni to'g'ridan-to'g'ri chaqirishni kafolatlaydi.

## Ishlash natijasi:
```text
Email xizmati ishga tushirildi.
```

# 492-Topshiriq: Generik Repository Pattern arxitekturasi
## Topshiriq sharti:
Ma'lumotlar ombori uchun tipik `IRepository<T>` generik interfeysini taqdim eting.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

interface IRepository<T> where T : class
{
    void Qo'shish(T obyekt);
    IEnumerable<T> HammasiniOlish();
}

class InMemoryRepository<T> : IRepository<T> where T : class
{
    private readonly List<T> ombor = new();

    public void Qo'shish(T obyekt) => ombor.Add(obyekt);
    public IEnumerable<T> HammasiniOlish() => ombor;
}

class Foydalanuvchi
{
    public string Login { get; set; } = "";
}

internal class Program
{
    static void Main()
    {
        var repo = new InMemoryRepository<Foydalanuvchi>();
        repo.Qo'shish(new Foydalanuvchi { Login = "admin" });
        repo.Qo'shish(new Foydalanuvchi { Login = "azamat" });

        foreach (var u in repo.HammasiniOlish())
        {
            Console.WriteLine($"Foydalanuvchi: {u.Login}");
        }
    }
}

```

## Tushuntirish va Mantiq:
Repository naqshi ma'lumotlar qatlamini biznes mantiqdan to'liq ajratadi va kodni oson testlash (Mocking) imkonini yaratadi.

## Ishlash natijasi:
```text
Foydalanuvchi: admin
Foydalanuvchi: azamat
```

# 493-Topshiriq: Generik Unmanaged Xotira Buferi (`where T : unmanaged`)
## Topshiriq sharti:
Stack yoki Native xotirada generik unmanaged elementlar buferini boshqaring.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.InteropServices;

unsafe class XotiraBuferi<T> : IDisposable where T : unmanaged
{
    private T* korsatkich;
    public int Hajm { get; }

    public XotiraBuferi(int hajm)
    {
        Hajm = hajm;
        korsatkich = (T*)NativeMemory.Alloc((nuint)(hajm * sizeof(T)));
    }

    public void O'rnatish(int indeks, T qiymat)
    {
        if (indeks < 0 || indeks >= Hajm) throw new IndexOutOfRangeException();
        *(korsatkich + indeks) = qiymat;
    }

    public T Olish(int indeks)
    {
        if (indeks < 0 || indeks >= Hajm) throw new IndexOutOfRangeException();
        return *(korsatkich + indeks);
    }

    public void Dispose()
    {
        if (korsatkich != null)
        {
            NativeMemory.Free(korsatkich);
            korsatkich = null;
        }
    }
}

internal class Program
{
    static void Main()
    {
        using var bufer = new XotiraBuferi<int>(3);
        bufer.O'rnatish(0, 100);
        bufer.O'rnatish(1, 200);
        bufer.O'rnatish(2, 300);

        Console.WriteLine($"Native xotiradan 1-indeks: {bufer.Olish(1)}");
    }
}

```

## Tushuntirish va Mantiq:
`where T : unmanaged` ko'rsatkichi T ning faqat blittable (GC nazorat qilmaydigan oddiy tuzilma) ekanligini kafolatlaydi va `sizeof(T)` hamda `T*` bilan to'g'ridan-to'g'ri ishlashga ruxsat beradi.

## Ishlash natijasi:
```text
Native xotiradan 1-indeks: 200
```

# 494-Topshiriq: Generik Matematika (.NET 7+ INumber<T>): Yig'indi hisoblash
## Topshiriq sharti:
C# 11+ da har qanday sonli tur (`int`, `double`, `decimal`) uchun yig'indi hisoblovchi generik metod yozing.

## Yechim (C# kodi):
```csharp
using System;
using System.Numerics;

internal class Program
{
    static T Yigindi<T>(T[] massiv) where T : INumber<T>
    {
        T jami = T.Zero;
        foreach (var item in massiv)
        {
            jami += item; // INumber<T> statik operatori tufayli generik qo'shish ishlaydi!
        }
        return jami;
    }

    static void Main()
    {
        int[] butunSonlar = [1, 2, 3, 4, 5];
        double[] haqiqiySonlar = [1.5, 2.5, 3.0];

        Console.WriteLine($"Int yig'indi: {Yigindi(butunSonlar)}");
        Console.WriteLine($"Double yig'indi: {Yigindi(haqiqiySonlar)}");
    }
}

```

## Tushuntirish va Mantiq:
INumber<T> interfeysi Static Abstract Interface Members imkoniyati asosida qurilgan bo'lib, generik darajada `+`, `-`, `*`, `/` operatorlarini qo'llashga imkon beradi.

## Ishlash natijasi:
```text
Int yig'indi: 15
Double yig'indi: 7
```

# 495-Topshiriq: Generik Matematika: O'rtacha arifmetik hisoblash
## Topshiriq sharti:
`INumber<T>` orqali o'rtacha arifmetik qiymatni hisoblang.

## Yechim (C# kodi):
```csharp
using System;
using System.Numerics;

internal class Program
{
    static T Ortacha<T>(ReadOnlySpan<T> qator) where T : INumber<T>
    {
        if (qator.Length == 0) return T.Zero;

        T yigindi = T.Zero;
        for (int i = 0; i < qator.Length; i++)
        {
            yigindi += qator[i];
        }

        T soni = T.CreateChecked(qator.Length);
        return yigindi / soni;
    }

    static void Main()
    {
        int[] ballar = [80, 90, 100];
        Console.WriteLine($"O'rtacha ball: {Ortacha<int>(ballar)}");
    }
}

```

## Tushuntirish va Mantiq:
`T.CreateChecked(length)` metodi butun sonli o'lchamni ixtiyoriy `T` turiga xavfsiz konvertatsiya qilib beradi.

## Ishlash natijasi:
```text
O'rtacha ball: 90
```

# 496-Topshiriq: Kovariant Ishlab Chiqaruvchi va Kontravariant Qabul Qiluvchi pipeline
## Topshiriq sharti:
`IProducer<out T>` va `IConsumer<in T>` interfeyslarini birlashtiruvchi quvur (pipeline) yarating.

## Yechim (C# kodi):
```csharp
using System;

interface IProducer<out T>
{
    T Produce();
}

interface IConsumer<in T>
{
    void Consume(T item);
}

class MatnGenerator : IProducer<string>
{
    public string Produce() => "Muhim xabar";
}

class ObektChopEtuvchi : IConsumer<object>
{
    public void Consume(object item) => Console.WriteLine($"Qabul qilindi: {item}");
}

internal class Program
{
    static void Main()
    {
        IProducer<object> producer = new MatnGenerator(); // Kovariantlik!
        IConsumer<string> consumer = new ObektChopEtuvchi(); // Kontravariantlik!

        object xabar = producer.Produce();
        consumer.Consume((string)xabar);
    }
}

```

## Tushuntirish va Mantiq:
Bu naqsh xabarlar almashinuvi tizimlarida (Producer-Consumer) tiplar erkinligini ta'minlashda arxitekturaning asosi hisoblanadi.

## Ishlash natijasi:
```text
Qabul qilindi: Muhim xabar
```

# 497-Topshiriq: Generik ValueTuple Dekonstruksiyasi
## Topshiriq sharti:
Generik juftliklarni Tuple yordamida qulay va yengil ajratib olishni ko'ring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static (TBir, TIkki) Juftlik<TBir, TIkki>(TBir a, TIkki b)
    {
        return (a, b);
    }

    static void Main()
    {
        var (nomi, narxi) = Juftlik("Olma", 12000);
        Console.WriteLine($"Tovar: {nomi}, Narxi: {narxi} so'm");
    }
}

```

## Tushuntirish va Mantiq:
ValueTuple tuzilmasi generik qiymatlarni heap xotirada qo'shimcha obyekt ajratmasdan eng tezkor tarzda guruhlaydi.

## Ishlash natijasi:
```text
Tovar: Olma, Narxi: 12000 so'm
```

# 498-Topshiriq: Generik Event Handler: EventHandler<TEventArgs>
## Topshiriq sharti:
Voqea sodir bo'lganda generik ma'lumot uzatuvchi voqea arxitekturasini yarating.

## Yechim (C# kodi):
```csharp
using System;

class YangiliklarArg : EventArgs
{
    public string Sarlavha { get; }
    public YangiliklarArg(string s) => Sarlavha = s;
}

class YangilikKompaniyasi
{
    public event EventHandler<YangiliklarArg>? YangilikChiqdi;

    public void ChopEtish(string sarlavha)
    {
        YangilikChiqdi?.Invoke(this, new YangiliklarArg(sarlavha));
    }
}

internal class Program
{
    static void Main()
    {
        var agentlik = new YangilikKompaniyasi();
        agentlik.YangilikChiqdi += (sender, e) =>
        {
            Console.WriteLine($"Shoshilinch xabar: {e.Sarlavha}");
        };

        agentlik.ChopEtish("Yangi .NET versiyasi e'lon qilindi!");
    }
}

```

## Tushuntirish va Mantiq:
`EventHandler<TEventArgs>` standart .NET delegati bo'lib, har qanday hodisaga xos ma'lumotlarni xavfsiz yuborish imkonini beradi.

## Ishlash natijasi:
```text
Shoshilinch xabar: Yangi .NET versiyasi e'lon qilindi!
```

# 499-Topshiriq: Generik Reflection: Type.MakeGenericType
## Topshiriq sharti:
Dastur ishlash jarayonida (Runtime) generik tur yaratish va uni ishlatish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        // Ro'yxat turining ochiq generik ta'rifi (List<>)
        Type ochiqTur = typeof(List<>);

        // Int turini unga parametr qilib beramiz: List<int>
        Type yopiqTur = ochiqTur.MakeGenericType(typeof(int));

        // Yangi obyekt instansiyasini olamiz
        var royxat = Activator.CreateInstance(yopiqTur);

        // Metodni chaqiramiz
        yopiqTur.GetMethod("Add")?.Invoke(royxat, new object[] { 777 });

        int hisob = (int)yopiqTur.GetProperty("Count")?.GetValue(royxat)!;
        Console.WriteLine($"Runtime generik ro'yxat elementlari soni: {hisob}");
    }
}

```

## Tushuntirish va Mantiq:
Reflection orqali runtime paytida `MakeGenericType` bilan ochiq generik turlarga argument berilib, yopiq (closed generic type) turlar yaratiladi.

## Ishlash natijasi:
```text
Runtime generik ro'yxat elementlari soni: 1
```

# 500-Topshiriq: Generik In-Memory Event Bus (Pub/Sub) Arxitekturasi
## Topshiriq sharti:
Kuchsiz bog'langan komponentlar o'rtasida xabarlashuvchi generik voqealar shinasini quring.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

interface IEvent { }

class BuyurtmaTushdi : IEvent
{
    public int BuyurtmaId { get; set; }
}

class EventBus
{
    private static readonly Dictionary<Type, List<Action<object>>> obunachilar = new();

    public static void Subscribe<T>(Action<T> harakat) where T : IEvent
    {
        Type tur = typeof(T);
        if (!obunachilar.ContainsKey(tur))
            obunachilar[tur] = new List<Action<object>>();

        obunachilar[tur].Add(e => harakat((T)e));
    }

    public static void Publish<T>(T voqea) where T : IEvent
    {
        Type tur = typeof(T);
        if (obunachilar.TryGetValue(tur, out var ro'yxat))
        {
            foreach (var obuna in ro'yxat)
            {
                obuna(voqea);
            }
        }
    }
}

internal class Program
{
    static void Main()
    {
        EventBus.Subscribe<BuyurtmaTushdi>(e =>
        {
            Console.WriteLine($"[Ombor]: #{e.BuyurtmaId} buyurtma tovarlari tayyorlanmoqda.");
        });

        EventBus.Subscribe<BuyurtmaTushdi>(e =>
        {
            Console.WriteLine($"[Kuryer]: #{e.BuyurtmaId} yetkazib berishga rejalashtirildi.");
        });

        Console.WriteLine("Voqea chop etilmoqda...");
        EventBus.Publish(new BuyurtmaTushdi { BuyurtmaId = 1042 });
    }
}

```

## Tushuntirish va Mantiq:
Generik Event Bus arxitekturasi xizmatlar o'rtasidagi to'g'ridan-to'g'ri bog'liqlikni yo'qotadi va dastur modullarini bir-biridan mustaqil qiladi.

## Ishlash natijasi:
```text
Voqea chop etilmoqda...
[Ombor]: #1042 buyurtma tovarlari tayyorlanmoqda.
[Kuryer]: #1042 yetkazib berishga rejalashtirildi.
```

