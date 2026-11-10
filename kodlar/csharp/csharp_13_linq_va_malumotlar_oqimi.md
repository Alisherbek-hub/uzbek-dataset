# 13-Mavzu: LINQ va Ma'lumotlar Oqimi (601-650)

Ushbu bo'limda C# tilining kuchli so'rovlar tili bo'lgan LINQ (Language Integrated Query): Query Syntax va Method Syntax, kechiktirilgan bajarilish (Deferred Execution) va darhol bajarilish (Immediate Execution), filtrlash (`Where`), proyeksiya (`Select`, `SelectMany`), saralash (`OrderBy`, `ThenBy`), guruhlash (`GroupBy`, `ToLookup`), bog'lash (`Join`, `GroupJoin`), .NET 6/7/8 zamonaviy metodlari (`Chunk`, `DistinctBy`, `MaxBy`, `MinBy`), to'plam amallari, agregatsiya (`Aggregate`), kvantorlar (`Any`, `All`), maxsus LINQ kengaytmalari hamda `IEnumerable` va `IQueryable` farqlari bo'yicha 50 ta amaliy topshiriq jamlangan.

# 601-Topshiriq: LINQ So'rov Sintaksisi (Query Syntax) vs Metod Sintaksisi (Method Syntax)
## Topshiriq sharti:
Bir xil amallarni SQL uslubidagi query syntax va lambda metod sintaksisida solishtiring.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;

internal class Program
{
    static void Main()
    {
        int[] sonlar = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

        // 1. Query Syntax (from ... in ... where ... select)
        var q1 = from s in sonlar
                 where s % 2 == 0
                 select s * 10;

        // 2. Method Syntax (.Where().Select())
        var q2 = sonlar.Where(s => s % 2 == 0).Select(s => s * 10);

        Console.WriteLine($"Query:  {string.Join(", ", q1)}");
        Console.WriteLine($"Method: {string.Join(", ", q2)}");
    }
}

```

## Tushuntirish va Mantiq:
Kompilyator barcha LINQ Query sintaksisini avtomatik ravishda Method sintaksisiga (Where, Select extension metodlariga) aylantiradi. Ikkala usul bir xil IL kodini hosil qiladi.

## Ishlash natijasi:
```text
Query:  20, 40, 60, 80, 100
Method: 20, 40, 60, 80, 100
```

# 602-Topshiriq: Kechiktirilgan Bajarilish (Deferred / Lazy Execution)
## Topshiriq sharti:
LINQ so'rovi faqat `foreach` yoki `ToList()` chaqirilgandagina hisoblanishini isbotlang.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

internal class Program
{
    static void Main()
    {
        List<int> sonlar = new() { 1, 2, 3 };

        // So'rov e'lon qilindi, lekin HALI BAJARILMADI:
        var sorov = sonlar.Select(x =>
        {
            Console.WriteLine($"[Hisoblandi]: {x}");
            return x * 10;
        });

        Console.WriteLine("So'rov e'lon qilindi, ro'yxatga yangi son qo'shamiz:");
        sonlar.Add(4);

        Console.WriteLine("Endi iteratsiya qilamiz:");
        foreach (var n in sorov)
        {
            Console.WriteLine($"Chiqdi: {n}");
        }
    }
}

```

## Tushuntirish va Mantiq:
LINQ metodlarining aksariyati (`Where`, `Select`, `Take`) kechiktirilgan hisoblash rejimida ishlaydi. Ular ma'lumotlarni oldindan hisoblab xotirada saqlamaydi, balki har bir element kerak bo'lgan paytda oqim bo'yicha tortib olinadi.

## Ishlash natijasi:
```text
So'rov e'lon qilindi, ro'yxatga yangi son qo'shamiz:
Endi iteratsiya qilamiz:
[Hisoblandi]: 1
Chiqdi: 10
[Hisoblandi]: 2
Chiqdi: 20
[Hisoblandi]: 3
Chiqdi: 30
[Hisoblandi]: 4
Chiqdi: 40
```

# 603-Topshiriq: Darhol Bajarilish (Immediate Execution): ToList, ToArray va Count
## Topshiriq sharti:
Kechiktirilgan so'rovni xotiraga mixlab (materialize) qo'yish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

internal class Program
{
    static void Main()
    {
        List<string> ismlar = new() { "Ali", "Vali" };

        // ToList() darhol natijani hisoblab, xotirada yangi List<string> yaratadi:
        List<string> xotiradagi = ismlar.Select(i => i.ToUpper()).ToList();

        ismlar.Add("G'ani");

        Console.WriteLine($"Materializatsiya qilingan ro'yxat: {string.Join(", ", xotiradagi)}");
        Console.WriteLine($"Asosiy ro'yxat: {string.Join(", ", ismlar)}");
    }
}

```

## Tushuntirish va Mantiq:
`ToList()`, `ToArray()`, `Count()`, `Sum()` kabi metodlar darhol bajarilishni talab qiladi va so'rovni o'sha zahoti oxirigacha aylantirib chiqadi.

## Ishlash natijasi:
```text
Materializatsiya qilingan ro'yxat: ALI, VALI
Asosiy ro'yxat: Ali, Vali, G'ani
```

# 604-Topshiriq: Where Metodining Indekslangan Ko'rinishi (Indexed Where)
## Topshiriq sharti:
Element bilan birga uning indeksini ham tekshiruvchi filtr.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;

internal class Program
{
    static void Main()
    {
        string[] mevalar = ["Olma", "Banan", "Gilos", "Shaftoli", "O'rik"];

        // Indeksi toq bo'lgan va uzunligi 4 dan katta bo'lgan mevalar
        var tanlangan = mevalar.Where((meva, index) => index % 2 != 0 && meva.Length > 4);

        foreach (var m in tanlangan)
        {
            Console.WriteLine($"Mos keldi: {m}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`Where((element, index) => ...)` ortiqcha sanagich o'zgaruvchilari ochmasdan elementning o'rni bo'yicha filtrlash imkonini beradi.

## Ishlash natijasi:
```text
Mos keldi: Banan
Mos keldi: Shaftoli
```

# 605-Topshiriq: SelectMany bilan Ichma-Ich Kolleksiyalarni Yassilash (Flattening)
## Topshiriq sharti:
Ro'yxatlar ro'yxatini (1 to Many) bitta tekis ro'yxatga aylantirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Sinf
{
    public string Guruh { get; set; } = "";
    public List<string> Oquvchilar { get; set; } = new();
}

internal class Program
{
    static void Main()
    {
        var sinflar = new List<Sinf>
        {
            new Sinf { Guruh = "A", Oquvchilar = ["Ali", "Vali"] },
            new Sinf { Guruh = "B", Oquvchilar = ["Soliq", "Botir"] }
        };

        // SelectMany barcha o'quvchilar ro'yxatlarini yagona tekis oqimga yoyadi
        var barchaOquvchilar = sinflar.SelectMany(s => s.Oquvchilar);

        Console.WriteLine($"Barcha o'quvchilar: {string.Join(", ", barchaOquvchilar)}");
    }
}

```

## Tushuntirish va Mantiq:
`SelectMany` funksional dasturlashdagi `flat_map` yoki `bind` operatsiyasi bo'lib, ierarxik ma'lumotlarni tekislaydi.

## Ishlash natijasi:
```text
Barcha o'quvchilar: Ali, Vali, Soliq, Botir
```

# 606-Topshiriq: OrderBy, OrderByDescending va ThenBy Zanjiri
## Topshiriq sharti:
Bir nechta mezonlar bo'yicha ketma-ket saralash.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

record Talaba(string Ism, int Kurs, double Ball);

internal class Program
{
    static void Main()
    {
        List<Talaba> talabalar =
        [
            new("Ali", 2, 85.5),
            new("Vali", 1, 92.0),
            new("G'ani", 2, 95.0),
            new("Salim", 1, 85.5)
        ];

        // Avval kursi bo'yicha o'sish tartibida, keyin bali bo'yicha kamayish tartibida:
        var saralangan = talabalar
            .OrderBy(t => t.Kurs)
            .ThenByDescending(t => t.Ball);

        foreach (var t in saralangan)
        {
            Console.WriteLine($"{t.Kurs}-kurs | {t.Ball} ball | {t.Ism}");
        }
    }
}

```

## Tushuntirish va Mantiq:
Doimiy xato: ikkinchi saralashda yana `OrderBy` chaqirilsa, avvalgi saralash bekor qilinadi. Ko'p mezonli saralash uchun albatta `ThenBy` yoki `ThenByDescending` ishlatilishi shart.

## Ishlash natijasi:
```text
1-kurs | 92 ball | Vali
1-kurs | 85.5 ball | Salim
2-kurs | 95 ball | G'ani
2-kurs | 85.5 ball | Ali
```

# 607-Topshiriq: GroupBy va IGrouping<TKey, TElement> Bilan Guruhlash
## Topshiriq sharti:
Kategoriyalar bo'yicha elementlarni guruhlarga ajratish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

record Xodim(string Ism, string Bolim, int Maosh);

internal class Program
{
    static void Main()
    {
        List<Xodim> jamoa =
        [
            new("Nodir", "IT", 1500),
            new("Zebo", "HR", 1000),
            new("Sarvar", "IT", 2000),
            new("Malika", "HR", 1200)
        ];

        var guruhlar = jamoa.GroupBy(x => x.Bolim);

        foreach (var g in guruhlar)
        {
            Console.WriteLine($"Bo'lim: {g.Key} (Xodimlar soni: {g.Count()})");
            foreach (var x in g)
            {
                Console.WriteLine($"  - {x.Ism}: ${x.Maosh}");
            }
        }
    }
}

```

## Tushuntirish va Mantiq:
`GroupBy` kechiktirilgan bajariladi va natijada har biri o'zining `Key` xususiyatiga ega bo'lgan `IGrouping` to'plamlarini hosil qiladi.

## Ishlash natijasi:
```text
Bo'lim: IT (Xodimlar soni: 2)
  - Nodir: $1500
  - Sarvar: $2000
Bo'lim: HR (Xodimlar soni: 2)
  - Zebo: $1000
  - Malika: $1200
```

# 608-Topshiriq: ToLookup: O'zgarmas Xotiradagi Guruhlash Jadvali
## Topshiriq sharti:
GroupBy dan farqli o'laroq darhol hisoblanuvchi ko'p qiymatli xarita (Multi-map).

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

internal class Program
{
    static void Main()
    {
        string[] sozlar = ["olma", "nok", "o'rik", "anor", "shaftoli"];

        // Bosh harfi bo'yicha Lookup yaratamiz (Immediate execution)
        ILookup<char, string> lugat = sozlar.ToLookup(s => s[0]);

        Console.WriteLine("'o' harfi bilan boshlanadiganlar:");
        foreach (var s in lugat['o'])
        {
            Console.WriteLine($"- {s}");
        }

        Console.WriteLine($"'z' harfi bormi (xatosiz bo'sh qaytaradi): {lugat['z'].Count()}");
    }
}

```

## Tushuntirish va Mantiq:
ILookup `Dictionary<TKey, List<TValue>>` ga o'xshaydi, lekin o'zgarmas (immutable) bo'lib, mavjud bo'lmagan kalit so'ralganda `KeyNotFoundException` otmasdan bo'sh ketma-ketlik qaytaradi.

## Ishlash natijasi:
```text
'o' harfi bilan boshlanadiganlar:
- olma
- o'rik
'z' harfi bormi (xatosiz bo'sh qaytaradi): 0
```

# 609-Topshiriq: Ichki Bog'lanish (Inner Join) Amali
## Topshiriq sharti:
Ikkita to'plamni umumiy kalit bo'yicha birlashtirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

record Kategoriya(int Id, string Nom);
record Mahsulot(string Nom, int KatId);

internal class Program
{
    static void Main()
    {
        List<Kategoriya> kats = [new(1, "Ichimlik"), new(2, "Shirinlik")];
        List<Mahsulot> mahsulotlar = [new("Kola", 1), new("Tort", 2), new("Non", 99)];

        var birlashgan = mahsulotlar.Join(
            kats,
            m => m.KatId,       // Mahsulot kaliti
            k => k.Id,          // Kategoriya kaliti
            (m, k) => new { Mahsulot = m.Nom, Kategoriya = k.Nom }
        );

        foreach (var item in birlashgan)
        {
            Console.WriteLine($"{item.Mahsulot} -> {item.Kategoriya}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`Join` ichki xesh-jadval (Hash Join) quradi va ikkala tomonda ham mos kalit bo'lgandagina natija chiqaradi (99-kodli Non chiqmaydi).

## Ishlash natijasi:
```text
Kola -> Ichimlik
Tort -> Shirinlik
```

# 610-Topshiriq: Chap Tashqi Bog'lanish (Left Outer Join) va GroupJoin
## Topshiriq sharti:
Barcha asosiy elementlarni, hatto bog'langan jufti bo'lmasa ham saqlab qolish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

record Kategoriya(int Id, string Nom);
record Mahsulot(string Nom, int KatId);

internal class Program
{
    static void Main()
    {
        List<Kategoriya> kats = [new(1, "Ichimlik"), new(2, "Meva"), new(3, "Texnika")];
        List<Mahsulot> mahsulotlar = [new("Choy", 1), new("Olma", 2)];

        var chapBoglanish = kats.GroupJoin(
            mahsulotlar,
            k => k.Id,
            m => m.KatId,
            (k, mGuruh) => new { Kategoriya = k.Nom, Mahsulotlar = mGuruh.DefaultIfEmpty() }
        ).SelectMany(
            x => x.Mahsulotlar,
            (x, m) => new { x.Kategoriya, Mahsulot = m != null ? m.Nom : "[Mahsulot yo'q]" }
        );

        foreach (var item in chapBoglanish)
        {
            Console.WriteLine($"{item.Kategoriya}: {item.Mahsulot}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`GroupJoin` va `DefaultIfEmpty()` kombinatsiyasi SQL dagi klassik LEFT JOIN amalini C# LINQ da to'liq amalga oshiradi.

## Ishlash natijasi:
```text
Ichimlik: Choy
Meva: Olma
Texnika: [Mahsulot yo'q]
```

# 611-Topshiriq: Zip Operatori Bilan Ikkita Oqimni Juftlash
## Topshiriq sharti:
Ikkita massiv elementlarini parallel birlashtirib borish.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;

internal class Program
{
    static void Main()
    {
        string[] ismlar = ["Sanjar", "Akmal", "Jahongir"];
        int[] ballar = [85, 92, 78];

        var natijalar = ismlar.Zip(ballar, (ism, ball) => $"{ism} - {ball} ball");

        foreach (var qator in natijalar)
        {
            Console.WriteLine(qator);
        }
    }
}

```

## Tushuntirish va Mantiq:
`Zip` ikkita ketma-ketlikni bir vaqtda aylanib, ularni juftlaydi. Ketma-ketliklardan biri tugashi bilan operatsiya to'xtaydi.

## Ishlash natijasi:
```text
Sanjar - 85 ball
Akmal - 92 ball
Jahongir - 78 ball
```

# 612-Topshiriq: .NET 6+ Chunk Metodi Bilan Bo'laklash
## Topshiriq sharti:
Katta to'plamni kichik sahifalar (batch/page) ga bo'lib qayta ishlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;

internal class Program
{
    static void Main()
    {
        int[] sonlar = [1, 2, 3, 4, 5, 6, 7, 8];

        // 3 tadan qilib bo'laklarga ajratish
        int[][] bolaklar = sonlar.Chunk(3).ToArray();

        for (int i = 0; i < bolaklar.Length; i++)
        {
            Console.WriteLine($"Bo'lak {i + 1}: {string.Join(", ", bolaklar[i])}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`Chunk(size)` metodi .NET 6 da kiritilgan bo'lib, eski murakkab `GroupBy((x, i) => i / size)` yondashuvini almashtirib, yuqori unumdorlik beradi.

## Ishlash natijasi:
```text
Bo'lak 1: 1, 2, 3
Bo'lak 2: 4, 5, 6
Bo'lak 3: 7, 8
```

# 613-Topshiriq: .NET 6+ DistinctBy, MinBy va MaxBy Metodlari
## Topshiriq sharti:
Obyekt xususiyatiga ko'ra unikal qilish va ekstremumlarni topish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

record Tovar(string Nom, string Tur, decimal Narx);

internal class Program
{
    static void Main()
    {
        List<Tovar> tovarlar =
        [
            new("Kofe", "Ichimlik", 25000),
            new("Choy", "Ichimlik", 10000),
            new("Pirog", "Yegulik", 30000)
        ];

        // Har bir turdan bittadan noyob tovar:
        var unikalTurlar = tovarlar.DistinctBy(t => t.Tur);
        Console.WriteLine($"Unikal turlar: {string.Join(", ", unikalTurlar.Select(t => t.Nom))}");

        // Eng qimmat tovar:
        var engQimmat = tovarlar.MaxBy(t => t.Narx);
        Console.WriteLine($"Eng qimmat tovar: {engQimmat?.Nom} ({engQimmat?.Narx} so'm)");
    }
}

```

## Tushuntirish va Mantiq:
MaxBy va MinBy avvalgi `OrderByDescending().FirstOrDefault()` usulidagi $O(N \log N)$ saralash xarajatini butunlay yo'qotib, bitta $O(N)$ o'tishda kerakli obyektni topadi.

## Ishlash natijasi:
```text
Unikal turlar: Kofe, Pirog
Eng qimmat tovar: Pirog (30000 so'm)
```

# 614-Topshiriq: Aggregate Metodi Bilan Yig'ish (Fold / Reduce)
## Topshiriq sharti:
LINQ da o'z maxsus akkumulyator algoritmingizni qurish.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;

internal class Program
{
    static void Main()
    {
        int[] sonlar = [1, 2, 3, 4, 5];

        // Faktorial hisoblash (ko'paytirish akkumulyatori):
        int faktorial = sonlar.Aggregate(1, (akku, joriy) => akku * joriy);

        // Satrlarni maxsus formatda birlashtirish:
        string[] sozlar = ["C#", ".NET", "LINQ"];
        string matn = sozlar.Aggregate("Texnologiyalar:", (akku, s) => $"{akku} [{s}]");

        Console.WriteLine($"5! = {faktorial}");
        Console.WriteLine(matn);
    }
}

```

## Tushuntirish va Mantiq:
`Aggregate` funksional dasturlashdagi `reduce` hisoblanadi. U boshlang'ich urug' (seed) qiymatdan boshlab ketma-ketlikni yagona natijaga yig'adi.

## Ishlash natijasi:
```text
5! = 120
Texnologiyalar: [C#] [.NET] [LINQ]
```

# 615-Topshiriq: First, FirstOrDefault, Single va SingleOrDefault Farqlari
## Topshiriq sharti:
Element qidirish metodlarining xavfsiz va xavfli holatlari.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

internal class Program
{
    static void Main()
    {
        List<int> royxat = [10, 20, 20, 30];

        // FirstOrDefault: topilsa birinchisini oladi, topilmasa standart qiymat (0) qaytaradi
        Console.WriteLine($"Birinchi: {royxat.FirstOrDefault(x => x == 20)}");
        Console.WriteLine($"Topilmasa: {royxat.FirstOrDefault(x => x == 99)}");

        // SingleOrDefault: aniq BIR DONA bo'lishini talab qiladi. Agar 2 ta bo'lsa xato beradi!
        try
        {
            royxat.SingleOrDefault(x => x == 20); // 2 ta 20 bor -> InvalidOperationException!
        }
        catch (InvalidOperationException)
        {
            Console.WriteLine("SingleOrDefault xatosi: bir nechta mos element topildi!");
        }
    }
}

```

## Tushuntirish va Mantiq:
Single va SingleOrDefault to'plamda unikal yagona element borligini tekshirish uchun mo'ljallangan (masalan, ID bo'yicha). Agar bir nechta chiqsa, xatolik beradi.

## Ishlash natijasi:
```text
Birinchi: 20
Topilmasa: 0
SingleOrDefault xatosi: bir nechta mos element topildi!
```

# 616-Topshiriq: FirstOrDefault Standart Qiymatini Belgilash (.NET 6+)
## Topshiriq sharti:
Topilmaganda `default` o'rniga maxsus belgilangan qiymat qaytarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;

internal class Program
{
    static void Main()
    {
        int[] sonlar = [1, 3, 5, 7];

        // Mos element topilmasa -1 qaytarsin:
        int juftSon = sonlar.FirstOrDefault(x => x % 2 == 0, defaultValue: -1);

        Console.WriteLine($"Juft son topildimi: {juftSon}");
    }
}

```

## Tushuntirish va Mantiq:
.NET 6 dan boshlab `FirstOrDefault(predicate, defaultValue)` orqali nol o'rniga istalgan zaxira qiymat berish mumkin.

## Ishlash natijasi:
```text
Juft son topildimi: -1
```

# 617-Topshiriq: Any va All Kvantorlarining 'Short-Circuiting' Xususiyati
## Topshiriq sharti:
Butun massivni aylanmasdan birinchi mos kelgan joyda to'xtash.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;

internal class Program
{
    static void Main()
    {
        int[] sonlar = [2, 4, 6, 7, 8, 10];

        // All: bitta toq son topilishi bilanoq tekshirishni to'xtatadi (false)
        bool barchasiJuft = sonlar.All(x => x % 2 == 0);

        // Any: bitta toq son topilishi bilanoq to'xtaydi (true)
        bool toqSonBormi = sonlar.Any(x => x % 2 != 0);

        Console.WriteLine($"Barchasi juftmi: {barchasiJuft}");
        Console.WriteLine($"Kamida bitta toq son bormi: {toqSonBormi}");
    }
}

```

## Tushuntirish va Mantiq:
`Any` va `All` qisqa tutashuv (short-circuiting) qoidasiga amal qiladi, bu esa millionlab elementli to'plamlarda juda ko'p vaqtni tejaydi.

## Ishlash natijasi:
```text
Barchasi juftmi: False
Kamida bitta toq son bormi: True
```

# 618-Topshiriq: Take, Skip va C# Index/Range Sintaksisi
## Topshiriq sharti:
Paginatsiya qilishning zamonaviy usullari.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;

internal class Program
{
    static void Main()
    {
        int[] sonlar = [10, 20, 30, 40, 50, 60, 70];

        // Sahifalash: 2-sahifa, har bir sahifada 2 tadan
        var sahifa2 = sonlar.Skip(2).Take(2);
        Console.WriteLine($"Sahifa 2: {string.Join(", ", sahifa2)}");

        // .NET 8 da LINQ Take(Range) qo'llab-quvvatlaydi:
        var oraliq = sonlar.Take(1..4);
        Console.WriteLine($"Take(1..4): {string.Join(", ", oraliq)}");
    }
}

```

## Tushuntirish va Mantiq:
Skip va Take veb ilovalarda ma'lumotlar bazasidan yoki xotiradan ma'lumotlarni qismlab (Pagination) ko'rsatishda standart usuldir.

## Ishlash natijasi:
```text
Sahifa 2: 30, 40
Take(1..4): 20, 30, 40
```

# 619-Topshiriq: TakeWhile va SkipWhile Metodlari
## Topshiriq sharti:
Shart bajarilib turguncha olish yoki tashlab ketish.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;

internal class Program
{
    static void Main()
    {
        int[] tartiblangan = [1, 2, 3, 10, 2, 1];

        // 5 dan kichik bo'lib turguncha oladi (10 kelganda to'xtaydi):
        var olindi = tartiblangan.TakeWhile(x => x < 5);

        // 5 dan kichik bo'lib turguncha o'tkazib yuboradi:
        var tashlandi = tartiblangan.SkipWhile(x => x < 5);

        Console.WriteLine($"TakeWhile: {string.Join(", ", olindi)}");
        Console.WriteLine($"SkipWhile: {string.Join(", ", tashlandi)}");
    }
}

```

## Tushuntirish va Mantiq:
`TakeWhile` va `Where` ning farqi: `Where` to'plamning oxirigacha boradi, `TakeWhile` esa shart buzilgan zahoti keyingi elementlarni umuman tekshirmaydi.

## Ishlash natijasi:
```text
TakeWhile: 1, 2, 3
SkipWhile: 10, 2, 1
```

# 620-Topshiriq: Enumerable.Range va Enumerable.Repeat Generatorlari
## Topshiriq sharti:
Massiv yaratmasdan tezkor sonlar va elementlar oqimini hosil qilish.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;

internal class Program
{
    static void Main()
    {
        // 1 dan boshlab 5 ta son:
        var sonlar = Enumerable.Range(1, 5).Select(x => x * x);
        Console.WriteLine($"Kvadratlar: {string.Join(", ", sonlar)}");

        // Bitta qiymatni 3 marta takrorlash:
        var takror = Enumerable.Repeat("Salom", 3);
        Console.WriteLine($"Takror: {string.Join(" - ", takror)}");
    }
}

```

## Tushuntirish va Mantiq:
`Enumerable.Range` xotirada massiv yaratmaydi, balki `yield return` kabi talab qilinganda sonlarni generatsiya qiladi.

## Ishlash natijasi:
```text
Kvadratlar: 1, 4, 9, 16, 25
Takror: Salom - Salom - Salom
```

# 621-Topshiriq: ToDictionary va ToHashSet Materializatsiyasi
## Topshiriq sharti:
LINQ oqimini bir qatorda Dictionary yoki HashSet ga aylantirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

record Mahsulot(int Kod, string Nom);

internal class Program
{
    static void Main()
    {
        List<Mahsulot> ro'yxat = [new(101, "Non"), new(102, "Choy")];

        // Kalit: Kod, Qiymat: Nom
        Dictionary<int, string> lugat = ro'yxat.ToDictionary(m => m.Kod, m => m.Nom);
        Console.WriteLine($"101-kodli mahsulot: {lugat[101]}");

        // Takrorlanmas HashSet ga o'girish
        int[] sonlar = [1, 2, 2, 3, 3, 3];
        HashSet<int> unikal = sonlar.ToHashSet();
        Console.WriteLine($"Unikal elementlar: {string.Join(", ", unikal)}");
    }
}

```

## Tushuntirish va Mantiq:
ToDictionary kalitlar takrorlangan taqdirda ArgumentException otadi. Agar kalit takrorlanishi mumkin bo'lsa `GroupBy` yoki `ToLookup` tanlanishi kerak.

## Ishlash natijasi:
```text
101-kodli mahsulot: Non
Unikal elementlar: 1, 2, 3
```

# 622-Topshiriq: OfType<T> va Cast<T> Bilan Turlarni Filtrlash
## Topshiriq sharti:
Har xil turlar aralashgan to'plamdan faqat kerakli turni ajratib olish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections;
using System.Linq;

internal class Program
{
    static void Main()
    {
        ArrayList aralash = new ArrayList { 10, "Matn", 25, "Salom", 3.14 };

        // Faqat string larni ajratib oladi (xato bermaydi):
        var matnlar = aralash.OfType<string>();
        Console.WriteLine($"Matnlar: {string.Join(", ", matnlar)}");

        // Faqat int larni ajratib oladi:
        var butunSonlar = aralash.OfType<int>();
        Console.WriteLine($"Butun sonlar yig'indisi: {butunSonlar.Sum()}");
    }
}

```

## Tushuntirish va Mantiq:
`OfType<T>` `is T` tekshiruvini bajaradi va mos kelmaganlarini o'tkazib yuboradi; `Cast<T>` esa mos kelmaganda `InvalidCastException` otadi.

## Ishlash natijasi:
```text
Matnlar: Matn, Salom
Butun sonlar yig'indisi: 35
```

# 623-Topshiriq: DefaultIfEmpty bilan Bo'sh To'plamni Himoyalash
## Topshiriq sharti:
Bo'sh ketma-ketlikdan xatosiz bitta standart element qaytarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

internal class Program
{
    static void Main()
    {
        List<int> bosh = new();

        var natija = bosh.DefaultIfEmpty(999);

        foreach (var item in natija)
        {
            Console.WriteLine($"Element: {item}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`DefaultIfEmpty` to'plam bo'sh bo'lgan holda uning o'rniga bitta elementli standart qiymatli ketma-ketlik hosil qiladi.

## Ishlash natijasi:
```text
Element: 999
```

# 624-Topshiriq: SequenceEqual Bilan To'plamlarni Elementma-Element Solishtirish
## Topshiriq sharti:
Ikkita ro'yxatning qiymatlari va ularning tartibi aynan bir xilligini tekshirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;

internal class Program
{
    static void Main()
    {
        int[] a = [1, 2, 3];
        int[] b = [1, 2, 3];
        int[] c = [3, 2, 1];

        Console.WriteLine($"a va b tengmi: {a.SequenceEqual(b)}");
        Console.WriteLine($"a va c tengmi: {a.SequenceEqual(c)}");
    }
}

```

## Tushuntirish va Mantiq:
`SequenceEqual` ikkala to'plamning ham o'lchami, ham har bir elementining joylashuv tartibini tekshiradi.

## Ishlash natijasi:
```text
a va b tengmi: True
a va c tengmi: False
```

# 625-Topshiriq: Maxsus LINQ Extension Metodi Yaratish
## Topshiriq sharti:
O'z biznes mantiqingizga mos kechiktirilgan (deferred) LINQ metodini yozing.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

static class MaxsusLinqExtensions
{
    // Faqat har n-chi elementni tanlab oluvchi LINQ metodi
    public static IEnumerable<T> HarNchi<T>(this IEnumerable<T> manba, int n)
    {
        if (n <= 0) throw new ArgumentOutOfRangeException(nameof(n));

        int hisob = 0;
        foreach (var item in manba)
        {
            if (++hisob % n == 0)
            {
                yield return item;
            }
        }
    }
}

internal class Program
{
    static void Main()
    {
        int[] raqamlar = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

        var harUchinchi = raqamlar.HarNchi(3);

        Console.WriteLine($"Har 3-chi raqam: {string.Join(", ", harUchinchi)}");
    }
}

```

## Tushuntirish va Mantiq:
`yield return` yordamida yozilgan maxsus LINQ kengaytmalarining barchasi standart LINQ kabi deferred execution rejimida ishlaydi.

## Ishlash natijasi:
```text
Har 3-chi raqam: 3, 6, 9
```

# 626-Topshiriq: IEnumerable vs IQueryable: Xotira vs SQL Masofaviy Bajarilishi
## Topshiriq sharti:
Ikki asosiy interfeysning ma'lumotlar bazasi va xotiradagi farqini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

internal class Program
{
    static void Main()
    {
        // 1. IEnumerable: Barcha ma'lumotlar avval xotiraga tortiladi, keyin C# da filtrlanadi (In-Memory)
        IEnumerable<int> sonlar = new List<int> { 10, 20, 30, 40, 50 };
        var filtr1 = sonlar.Where(x => x > 25);

        // 2. IQueryable: So'rov Expression Tree shaklida saqlanadi va SQL ga tarjima qilinadi
        IQueryable<int> queryable = sonlar.AsQueryable();
        var filtr2 = queryable.Where(x => x > 25);

        Console.WriteLine($"IEnumerable natijasi: {string.Join(", ", filtr1)}");
        Console.WriteLine($"IQueryable ifoda turi: {filtr2.Expression.Type.Name}");
    }
}

```

## Tushuntirish va Mantiq:
IEnumerable `Func<T, bool>` delegatini qabul qilib, xotirada ishlaydi. IQueryable esa `Expression<Func<T, bool>>` daraxtini qabul qiladi va provayder (masalan, EF Core) uni toza SQL (`SELECT ... WHERE x > 25`) so'roviga aylantiradi.

## Ishlash natijasi:
```text
IEnumerable natijasi: 30, 40, 50
IQueryable ifoda turi: IQueryable`1
```

# 627-Topshiriq: IAsyncEnumerable<T> bilan Asinxron Oqimlarni LINQ da Qayta Ishlash
## Topshiriq sharti:
Har bir element asinxron keladigan ma'lumotlar oqimida iteratsiya.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

internal class Program
{
    static async IAsyncEnumerable<int> AsinxronSonlar()
    {
        for (int i = 1; i <= 3; i++)
        {
            await Task.Delay(30); // Tarmoqdan yoki diskdan kechikish
            yield return i * 10;
        }
    }

    static async Task Main()
    {
        Console.WriteLine("Asinxron oqim boshlanmoqda:");

        await foreach (int son in AsinxronSonlar())
        {
            Console.WriteLine($"Qabul qilindi: {son}");
        }
    }
}

```

## Tushuntirish va Mantiq:
IAsyncEnumerable<T> C# 8 da kiritilgan bo'lib, har bir elementni asinxron (non-blocking) tarzda `yield return` orqali uzatish imkonini beradi.

## Ishlash natijasi:
```text
Asinxron oqim boshlanmoqda:
Qabul qilindi: 10
Qabul qilindi: 20
Qabul qilindi: 30
```

# 628-Topshiriq: PLINQ (Parallel LINQ) Asoslari: AsParallel Bilan Ko'p Yadroli Hisoblash
## Topshiriq sharti:
Katta massiv ustida hisob-kitoblarni protsessorning barcha yadrolariga taqsimlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;

internal class Program
{
    static void Main()
    {
        var sonlar = Enumerable.Range(1, 10);

        // AsParallel() yordamida parallel hisoblash
        var kvadratlar = sonlar
            .AsParallel()
            .Where(x => x % 2 == 0)
            .Select(x => x * x)
            .ToArray();

        Console.WriteLine($"Juft sonlar kvadratlari soni: {kvadratlar.Length}");
        Console.WriteLine($"Elementlar mavjud: {string.Join(", ", kvadratlar.OrderBy(x => x))}");
    }
}

```

## Tushuntirish va Mantiq:
PLINQ oqimni ichki bo'laklarga (partitions) ajratib, ThreadPool ishchi oqimlarida parallel bajaradi.

## Ishlash natijasi:
```text
Juft sonlar kvadratlari soni: 5
Elementlar mavjud: 4, 16, 36, 64, 100
```

# 629-Topshiriq: PLINQ AsOrdered Bilan Tartibni Saqlab Qolish
## Topshiriq sharti:
Parallel ishlov berishda elementlarning dastlabki ketma-ketligini kafolatlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;

internal class Program
{
    static void Main()
    {
        int[] tartib = [1, 2, 3, 4, 5];

        // AsOrdered parallel bo'lsa ham tartibni tiklaydi:
        var natija = tartib
            .AsParallel()
            .AsOrdered()
            .Select(x => x * 2)
            .ToArray();

        Console.WriteLine($"Tartibli parallel natija: {string.Join(", ", natija)}");
    }
}

```

## Tushuntirish va Mantiq:
`AsOrdered()` parallel bajarilish natijalarini buferlab, asl ketma-ketlikda qaytaradi. Bu ozgina xotira xarajatiga ega bo'lsa-da, tartibni kafolatlaydi.

## Ishlash natijasi:
```text
Tartibli parallel natija: 2, 4, 6, 8, 10
```

# 630-Topshiriq: PLINQ WithDegreeOfParallelism va WithCancellation
## Topshiriq sharti:
Parallelizm darajasini cheklash va bekor qilish tokenini ulash.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;
using System.Threading;

internal class Program
{
    static void Main()
    {
        using var cts = new CancellationTokenSource();
        var data = Enumerable.Range(1, 20);

        // Maksimal 2 ta yadrodan foydalanish:
        var natija = data
            .AsParallel()
            .WithDegreeOfParallelism(2)
            .WithCancellation(cts.Token)
            .Select(x => x + 1)
            .Take(5)
            .ToList();

        Console.WriteLine($"Olingan sonlar: {string.Join(", ", natija)}");
    }
}

```

## Tushuntirish va Mantiq:
WithDegreeOfParallelism server protsessorini boshqa xizmatlarga xalaqit bermasligi uchun cheklashda muhim ahamiyatga ega.

## Ishlash natijasi:
```text
Olingan sonlar: 2, 3, 4, 5, 6
```

# 631-Topshiriq: PLINQ ForAll Operatori
## Topshiriq sharti:
Natijalarni yig'masdan joyida parallel iste'mol qilish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Concurrent;
using System.Linq;

internal class Program
{
    static void Main()
    {
        var xalta = new ConcurrentBag<int>();
        var sonlar = Enumerable.Range(1, 4);

        // ForAll har bir oqimda to'g'ridan-to'g'ri ishlaydi (hech qanday merge/birlashtirish yo'q)
        sonlar.AsParallel().ForAll(x =>
        {
            xalta.Add(x * 10);
        });

        Console.WriteLine($"Xaltadagi elementlar: {string.Join(", ", xalta.OrderBy(x => x))}");
    }
}

```

## Tushuntirish va Mantiq:
Oddiy `foreach` PLINQ oqimlarini bitta asosiy oqimga birlashtirishni talab qiladi. `ForAll` esa birlashtirish xarajatlarisiz parallel bajarilishini davom ettiradi.

## Ishlash natijasi:
```text
Xaltadagi elementlar: 10, 20, 30, 40
```

# 632-Topshiriq: Takroriy Iteratsiya Xavfi (Multiple Enumeration: CA1851)
## Topshiriq sharti:
Deferred so'rovni bir necha bor aylantirish qanday qilib og'ir oqibatlarga olib kelishini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

internal class Program
{
    static IEnumerable<int> OgirSo'rov()
    {
        Console.WriteLine("[DIQQAT]: Og'ir hisob-kitob bajarildi!");
        yield return 10;
        yield return 20;
    }

    static void Main()
    {
        var ketmaKetlik = OgirSo'rov();

        // 1-chaqiruv: Count tekshiruvi
        if (ketmaKetlik.Any())
        {
            // 2-chaqiruv: Foreach orqali aylanish
            foreach (var item in ketmaKetlik)
            {
                Console.WriteLine($"Qiymat: {item}");
            }
        }
    }
}

```

## Tushuntirish va Mantiq:
Agar ketma-ketlik `ToList()` qilib xotiraga olinmasa, `Any()`, `Count()`, `foreach` har safar butun manbani boshidan qayta hisoblab chiqadi. Bu 'Multiple Enumeration' xatosi deb ataladi.

## Ishlash natijasi:
```text
[DIQQAT]: Og'ir hisob-kitob bajarildi!
[DIQQAT]: Og'ir hisob-kitob bajarildi!
Qiymat: 10
Qiymat: 20
```

# 633-Topshiriq: .NET 6+ TryGetNonEnumeratedCount Metodi
## Topshiriq sharti:
To'plamni hisoblamasdan (non-greedy) uning sonini bilish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

internal class Program
{
    static void Main()
    {
        IEnumerable<int> ro'yxat = new List<int> { 1, 2, 3, 4, 5 };

        // Ro'yxatni aylanmasdan, uning ICollection.Count xususiyati borligini tezda tekshiradi:
        if (ro'yxat.TryGetNonEnumeratedCount(out int soni))
        {
            Console.WriteLine($"Tezkor topilgan hajm: {soni}");
        }
        else
        {
            Console.WriteLine("Hajmni bilish uchun to'liq aylanib chiqish shart.");
        }
    }
}

```

## Tushuntirish va Mantiq:
`TryGetNonEnumeratedCount` $O(1)$ da mavjud kolleksiya o'lchamini oladi va bekorga so'rovni hisoblab chiqishdan asraydi.

## Ishlash natijasi:
```text
Tezkor topilgan hajm: 5
```

# 634-Topshiriq: .NET 6+ IntersectBy va ExceptBy Operatorlari
## Topshiriq sharti:
Kalit selektori bo'yicha to'plamlar ayirmasi va kesishmasini olish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

record Xodim(int Id, string Ism);

internal class Program
{
    static void Main()
    {
        List<Xodim> barcha = [new(1, "Ali"), new(2, "Vali"), new(3, "G'ani")];
        int[] faolIdlar = [1, 3];

        // Faol bo'lmagan xodimlarni topish (ExceptBy):
        var nofaollar = barcha.ExceptBy(faolIdlar, x => x.Id);

        foreach (var x in nofaollar)
        {
            Console.WriteLine($"Nofaol: {x.Ism}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`ExceptBy` obyektlar to'plamidan oddiy kalitlar to'plamini ayirib tashlash imkonini beradi.

## Ishlash natijasi:
```text
Nofaol: Vali
```

# 635-Topshiriq: .NET 6+ UnionBy Operatori
## Topshiriq sharti:
Kalit bo'yicha birlashtirib, takroriy obyektlarni elash.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

record Mahsulot(int Id, string Nomi);

internal class Program
{
    static void Main()
    {
        List<Mahsulot> ombor1 = [new(1, "Olma"), new(2, "Nok")];
        List<Mahsulot> ombor2 = [new(2, "Nok yangi"), new(3, "Uzum")];

        // Id bo'yicha birlashtiramiz (takrorlangan Id tushib qoladi):
        var birlashgan = ombor1.UnionBy(ombor2, m => m.Id);

        foreach (var m in birlashgan)
        {
            Console.WriteLine($"{m.Id}: {m.Nomi}");
        }
    }
}

```

## Tushuntirish va Mantiq:
UnionBy ikkita to'plamni bitta qilib, belgilangan xususiyat bo'yicha unikal natija beradi.

## Ishlash natijasi:
```text
1: Olma
2: Nok
3: Uzum
```

# 636-Topshiriq: .NET 9 Yangi LINQ Operatori: CountBy
## Topshiriq sharti:
Elementlarni to'liq guruhlamasdan, ularning sonini tezkor xarita qilish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

internal class Program
{
    static void Main()
    {
        string[] matnlar = ["olma", "nok", "olma", "shaftoli", "nok", "olma"];

        // .NET 9 CountBy: GroupBy + Count amalini bitta optimal operatsiyaga aylantiradi
        var hisoblar = matnlar.CountBy(word => word);

        foreach (KeyValuePair<string, int> kvp in hisoblar)
        {
            Console.WriteLine($"{kvp.Key}: {kvp.Value} marta");
        }
    }
}

```

## Tushuntirish va Mantiq:
`CountBy` .NET 9 da qo'shilgan bo'lib, xotirada oraliq guruhlash ro'yxatlarini (IGrouping) yaratmasdan bevosita hisoblaydi.

## Ishlash natijasi:
```text
olma: 3 marta
nok: 2 marta
shaftoli: 1 marta
```

# 637-Topshiriq: .NET 9 Yangi LINQ Operatori: AggregateBy
## Topshiriq sharti:
Kalitlar bo'yicha akkumulyatsiyani bevosita yig'ish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

record Tranzaksiya(string Kategoriya, decimal Summa);

internal class Program
{
    static void Main()
    {
        List<Tranzaksiya> harajatlar =
        [
            new("Oziq-ovqat", 50000),
            new("Transport", 15000),
            new("Oziq-ovqat", 30000),
            new("Transport", 20000)
        ];

        // .NET 9 AggregateBy: Kategoriya bo'yicha summani to'g'ridan-to'g'ri yig'ish
        var natijalar = harajatlar.AggregateBy(
            t => t.Kategoriya,
            seed: 0m,
            (jami, t) => jami + t.Summa
        );

        foreach (var r in natijalar)
        {
            Console.WriteLine($"{r.Key}: {r.Value} so'm");
        }
    }
}

```

## Tushuntirish va Mantiq:
AggregateBy .NET 9 da kiritilgan yuqori unumdor operator bo'lib, SQL dagi `GROUP BY ... SUM(...)` so'roviga teng.

## Ishlash natijasi:
```text
Oziq-ovqat: 80000 so'm
Transport: 35000 so'm
```

# 638-Topshiriq: .NET 9 Yangi LINQ Operatori: Index()
## Topshiriq sharti:
Foreach siklida indeksni kuzatib boruvchi zamonaviy `Index()` operatori.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;

internal class Program
{
    static void Main()
    {
        string[] kunlar = ["Dushanba", "Seshanba", "Chorshanba"];

        // .NET 9 Index() har bir elementni (Index, Item) juftligiga aylantiradi:
        foreach (var (index, kun) in kunlar.Index())
        {
            Console.WriteLine($"{index + 1}-kun: {kun}");
        }
    }
}

```

## Tushuntirish va Mantiq:
Python dagi `enumerate()` kabi ishlovchi `.Index()` operatori C# 13 / .NET 9 da standart LINQ a'zosi bo'ldi.

## Ishlash natijasi:
```text
1-kun: Dushanba
2-kun: Seshanba
3-kun: Chorshanba
```

# 639-Topshiriq: Dinamik Predikatlar Birlashtiruvchisi (Dynamic Predicate Composer)
## Topshiriq sharti:
Foydalanuvchi interfeysidagi ixtiyoriy filtrlarni dinamik qo'shish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

record Avtomobil(string Model, int Yil, decimal Narx);

internal class Program
{
    static void Main()
    {
        List<Avtomobil> mashinalar =
        [
            new("Cobalt", 2022, 12000),
            new("Gentra", 2020, 11000),
            new("Tracker", 2023, 19000),
            new("Malibu", 2021, 25000)
        ];

        // So'rovni dinamik ravishda bosqichma-bosqich quramiz:
        IEnumerable<Avtomobil> sorov = mashinalar;

        int? filtrYil = 2021;
        decimal? maxNarx = 20000;

        if (filtrYil.HasValue)
            sorov = sorov.Where(m => m.Yil >= filtrYil.Value);

        if (maxNarx.HasValue)
            sorov = sorov.Where(m => m.Narx <= maxNarx.Value);

        foreach (var m in sorov)
        {
            Console.WriteLine($"{m.Model} ({m.Yil}) - ${m.Narx}");
        }
    }
}

```

## Tushuntirish va Mantiq:
LINQ ning deferred tabiati tufayli `Where` zanjirlarini `if` bloklari orqali dinamik qurish mumkin, so'rov faqat yakunda bir marta bajariladi.

## Ishlash natijasi:
```text
Cobalt (2022) - $12000
Tracker (2023) - $19000
```

# 640-Topshiriq: Dekart Ko'paytmasi (Cross Join) LINQ Query Sintaksisida
## Topshiriq sharti:
Har bir elementni boshqa to'plamning har bir elementi bilan juftlash ($N \times M$).

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;

internal class Program
{
    static void Main()
    {
        string[] ranglar = ["Qizil", "Moviy"];
        string[] olchamlar = ["S", "M", "L"];

        var kombinatsiyalar = from r in ranglar
                              from o in olchamlar
                              select $"{r} - {o}";

        foreach (var k in kombinatsiyalar)
        {
            Console.WriteLine(k);
        }
    }
}

```

## Tushuntirish va Mantiq:
Query sintaksisidagi bir nechta `from` operatorlari ketma-ketligi Dekart ko'paytmasini (`SelectMany`) hosil qiladi.

## Ishlash natijasi:
```text
Qizil - S
Qizil - M
Qizil - L
Moviy - S
Moviy - M
Moviy - L
```

# 641-Topshiriq: Ichma-Ich Guruhlash (Multi-Level Grouping)
## Topshiriq sharti:
Mamlakat va shahar bo'yicha 2 darajali ierarxik guruhlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

record Manzil(string Davlat, string Shahar, string Kucha);

internal class Program
{
    static void Main()
    {
        List<Manzil> manzillar =
        [
            new("Uzbekistan", "Toshkent", "Navoiy"),
            new("Uzbekistan", "Toshkent", "Chilonzor"),
            new("Uzbekistan", "Samarqand", "Registon"),
            new("Qazaqstan", "Almati", "Abay")
        ];

        var guruhlar = manzillar
            .GroupBy(m => m.Davlat)
            .Select(dGuruh => new
            {
                Davlat = dGuruh.Key,
                Shaharlar = dGuruh.GroupBy(m => m.Shahar)
            });

        foreach (var d in guruhlar)
        {
            Console.WriteLine($"Davlat: {d.Davlat}");
            foreach (var sh in d.Shaharlar)
            {
                Console.WriteLine($"  Shahar: {sh.Key} ({sh.Count()} ta ko'cha)");
            }
        }
    }
}

```

## Tushuntirish va Mantiq:
Ichma-ich guruhlash orqali murakkab statistik hisobotlarni oson shakllantirish mumkin.

## Ishlash natijasi:
```text
Davlat: Uzbekistan
  Shahar: Toshkent (2 ta ko'cha)
  Shahar: Samarqand (1 ta ko'cha)
Davlat: Qazaqstan
  Shahar: Almati (1 ta ko'cha)
```

# 642-Topshiriq: Harakatlanuvchi Oyna (Sliding Window) LINQ Kengaytmasi
## Topshiriq sharti:
Ketma-ket $K$ ta elementdan iborat oynani surib hisoblash.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

static class LinqWindowExtensions
{
    public static IEnumerable<T[]> Oyna<T>(this IEnumerable<T> manba, int hajm)
    {
        var navbat = new Queue<T>(hajm);
        foreach (var item in manba)
        {
            navbat.Enqueue(item);
            if (navbat.Count == hajm)
            {
                yield return navbat.ToArray();
                navbat.Dequeue();
            }
        }
    }
}

internal class Program
{
    static void Main()
    {
        int[] sonlar = [1, 2, 3, 4, 5];

        // 3 talik harakatlanuvchi oyna
        foreach (var w in sonlar.Oyna(3))
        {
            Console.WriteLine($"[{string.Join(", ", w)}]");
        }
    }
}

```

## Tushuntirish va Mantiq:
Sliding Window moliyaviy tahlilda harakatlanuvchi o'rtacha qiymatni (Moving Average) hisoblashda asosiy algoritmdir.

## Ishlash natijasi:
```text
[1, 2, 3]
[2, 3, 4]
[3, 4, 5]
```

# 643-Topshiriq: Rekursiv Daraxtni Tekislovchi LINQ (Flatten Hierarchy)
## Topshiriq sharti:
Kompaniya tashkiliy tuzilmasidagi barcha bo'limlarni rekursiv tekislash.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Bolim
{
    public string Nomi { get; set; } = "";
    public List<Bolim> QuyiBolimlar { get; set; } = new();
}

static class TreeExtensions
{
    public static IEnumerable<T> Yassila<T>(this IEnumerable<T> manba, Func<T, IEnumerable<T>> bolalarSelektori)
    {
        foreach (var element in manba)
        {
            yield return element;
            foreach (var bola in bolalarSelektori(element).Yassila(bolalarSelektori))
            {
                yield return bola;
            }
        }
    }
}

internal class Program
{
    static void Main()
    {
        var boshBolim = new Bolim
        {
            Nomi = "Bosh Ofis",
            QuyiBolimlar =
            [
                new Bolim { Nomi = "IT Bo'limi", QuyiBolimlar = [new Bolim { Nomi = "DevOps" }] },
                new Bolim { Nomi = "Moliya" }
            ]
        };

        var hamma = new[] { boshBolim }.Yassila(b => b.QuyiBolimlar);

        foreach (var b in hamma)
        {
            Console.WriteLine($"- {b.Nomi}");
        }
    }
}

```

## Tushuntirish va Mantiq:
Rekursiv LINQ orqali ixtiyoriy chuqurlikdagi daraxtsimon tuzilmalarni chiziqli ketma-ketlikka aylantirish mumkin.

## Ishlash natijasi:
```text
- Bosh Ofis
- IT Bo'limi
- DevOps
- Moliya
```

# 644-Topshiriq: Matritsani Transpozitsiya Qilish LINQ da
## Topshiriq sharti:
Satrlar va ustunlar o'rnini almashtirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

internal class Program
{
    static void Main()
    {
        int[][] matritsa =
        [
            [1, 2, 3],
            [4, 5, 6]
        ];

        // Transpozitsiya: 2x3 matritsani 3x2 ga aylantirish
        var transpozitsiya = Enumerable.Range(0, matritsa[0].Length)
            .Select(ustun => matritsa.Select(qator => qator[ustun]).ToArray())
            .ToArray();

        for (int i = 0; i < transpozitsiya.Length; i++)
        {
            Console.WriteLine(string.Join(" ", transpozitsiya[i]));
        }
    }
}

```

## Tushuntirish va Mantiq:
LINQ ning deklarativ kuchi orqali bir necha qatorda ikki o'lchamli massiv koordinatalarini o'girish mumkin.

## Ishlash natijasi:
```text
1 4
2 5
3 6
```

# 645-Topshiriq: LINQ to XML (XDocument va XElement)
## Topshiriq sharti:
XML hujjatini LINQ so'rovlari bilan oson tahlil qilish va yaratish.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;
using System.Xml.Linq;

internal class Program
{
    static void Main()
    {
        XDocument doc = new XDocument(
            new XElement("Kitoblar",
                new XElement("Kitob", new XAttribute("Janr", "Ilmiy"),
                    new XElement("Nom", "Koinot Sirlari"),
                    new XElement("Narx", 45000)
                ),
                new XElement("Kitob", new XAttribute("Janr", "Badiiy"),
                    new XElement("Nom", "O'tkan Kunlar"),
                    new XElement("Narx", 35000)
                )
            )
        );

        // LINQ orqali XML dan qidirish:
        var ilmiyKitoblar = from k in doc.Descendants("Kitob")
                            where (string)k.Attribute("Janr")! == "Ilmiy"
                            select k.Element("Nom")!.Value;

        Console.WriteLine($"Ilmiy kitob: {ilmiyKitoblar.First()}");
    }
}

```

## Tushuntirish va Mantiq:
LINQ to XML (`System.Xml.Linq`) eski DOM uslubidagi `XmlDocument` dan ancha qulay va yengil arxitekturadir.

## Ishlash natijasi:
```text
Ilmiy kitob: Koinot Sirlari
```

# 646-Topshiriq: LINQ orqali Xesh-Jadvalsiz O(N) To'plam Kesishmasi
## Topshiriq sharti:
Tartiblangan ikkita massiv kesishmasini ikkita ko'rsatkich (Two Pointers) bilan topish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

static class TwoPointerLinq
{
    public static IEnumerable<int> TartiblanganKesishma(this int[] a, int[] b)
    {
        int i = 0, j = 0;
        while (i < a.Length && j < b.Length)
        {
            if (a[i] == b[j])
            {
                yield return a[i];
                i++; j++;
            }
            else if (a[i] < b[j]) i++;
            else j++;
        }
    }
}

internal class Program
{
    static void Main()
    {
        int[] a = [1, 3, 4, 7, 9];
        int[] b = [2, 3, 7, 8, 9, 10];

        var kesishma = a.TartiblanganKesishma(b);
        Console.WriteLine($"Kesishma: {string.Join(", ", kesishma)}");
    }
}

```

## Tushuntirish va Mantiq:
Tartiblangan massivlarda HashSet yaratmasdan $O(1)$ qo'shimcha xotira va $O(N + M)$ vaqtda kesishmani olish mumkin.

## Ishlash natijasi:
```text
Kesishma: 3, 7, 9
```

# 647-Topshiriq: Zip bilan 3 ta Ketma-Ketlikni Birlashtirish
## Topshiriq sharti:
.NET 6 da qo'shilgan 3 argumentli `Zip` metodi.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;

internal class Program
{
    static void Main()
    {
        int[] idlar = [1, 2];
        string[] ismlar = ["Sanjar", "Akbar"];
        string[] lavozimlar = ["Dasturchi", "Dizayner"];

        // .NET 6 uchlik Zip operatori
        var jadval = idlar.Zip(ismlar, lavozimlar);

        foreach (var (id, ism, lavozim) in jadval)
        {
            Console.WriteLine($"#{id} {ism} - {lavozim}");
        }
    }
}

```

## Tushuntirish va Mantiq:
.NET 6 da `Zip` 3 ta to'plamni bir vaqtda qabul qilib, ValueTuple uchliklarini hosil qiladi.

## Ishlash natijasi:
```text
#1 Sanjar - Dasturchi
#2 Akbar - Dizayner
```

# 648-Topshiriq: DistinctBy bilan Murakkab Ob'ektlarni Duplikatsiz Saralash
## Topshiriq sharti:
Bir nechta parametrli unikal kalit bo'yicha saralash.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

record Bilet(string Shahar, string Sanasi, decimal Narx);

internal class Program
{
    static void Main()
    {
        List<Bilet> biletlar =
        [
            new("Samarqand", "2025-06-01", 100000),
            new("Samarqand", "2025-06-01", 120000), // Duplikat shahar va sana
            new("Buxoro", "2025-06-01", 150000)
        ];

        // Shahar va sana juftligi bo'yicha unikal qilish:
        var unikal = biletlar.DistinctBy(b => (b.Shahar, b.Sanasi));

        foreach (var b in unikal)
        {
            Console.WriteLine($"{b.Shahar} [{b.Sanasi}] - {b.Narx} so'm");
        }
    }
}

```

## Tushuntirish va Mantiq:
ValueTuple `(b.Shahar, b.Sanasi)` avtomatik ravishda strukturaviy tenglik va to'g'ri xesh-kodga ega bo'lgani sababli kalit sifatida ideal ishlaydi.

## Ishlash natijasi:
```text
Samarqand [2025-06-01] - 100000 so'm
Buxoro [2025-06-01] - 150000 so'm
```

# 649-Topshiriq: LINQ da Xotira Sarfini Kamaytirish (Boxing va Allocations)
## Topshiriq sharti:
Strukturalar bilan ishlashda boxing chaqirmaydigan to'g'ri agregatsiyani tanlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

readonly record struct Nuqta(int X, int Y);

internal class Program
{
    static void Main()
    {
        Nuqta[] nuqtalar = [new(1, 2), new(3, 4), new(5, 6)];

        // Select va Sum orqali boxing sodir bo'lmaydi:
        int jamiX = nuqtalar.Select(n => n.X).Sum();

        Console.WriteLine($"Jami X koordinatalari: {jamiX}");
    }
}

```

## Tushuntirish va Mantiq:
LINQ ning `Sum()`, `Average()` kabi primitiv metodlari `int`, `long`, `double` uchun maxsus yozilgan bo'lib, boxing yaratmaydi.

## Ishlash natijasi:
```text
Jami X koordinatalari: 9
```

# 650-Topshiriq: LINQ Xulosasi: Savdo Statistikasi Tahlili Tizimi (Sales Analytics Engine)
## Topshiriq sharti:
Murakkab ma'lumotlar ustida Where, GroupBy, Sum, OrderBy va Select operatsiyalarining yagona tahliliy hisoboti.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

record Buyurtma(int Id, string Mijoz, string Mahsulot, string Kategoriya, int Soni, decimal Narx);

internal class Program
{
    static void Main()
    {
        List<Buyurtma> savdo =
        [
            new(1, "Ali", "Telefon", "Elektronika", 1, 300),
            new(2, "Vali", "Noutbuk", "Elektronika", 2, 800),
            new(3, "Ali", "Kofta", "Kiyim", 3, 50),
            new(4, "G'ani", "Monitor", "Elektronika", 1, 200),
            new(5, "Vali", "Shalvar", "Kiyim", 2, 40)
        ];

        // 1. Kategoriya bo'yicha umumiy aylanma va eng ko'p sotilgan mahsulot
        var statistika = savdo
            .GroupBy(b => b.Kategoriya)
            .Select(g => new
            {
                Kategoriya = g.Key,
                JamiSumma = g.Sum(b => b.Soni * b.Narx),
                EngKopSotilgan = g.MaxBy(b => b.Soni)?.Mahsulot
            })
            .OrderByDescending(s => s.JamiSumma);

        Console.WriteLine("Kategoriya hisoboti:");
        foreach (var s in statistika)
        {
            Console.WriteLine($"- {s.Kategoriya}: Jami ${s.JamiSumma}, Top tovar: {s.EngKopSotilgan}");
        }

        // 2. Eng ko'p xarid qilgan top mijoz
        var topMijoz = savdo
            .GroupBy(b => b.Mijoz)
            .Select(g => new { Mijoz = g.Key, Xarid = g.Sum(b => b.Soni * b.Narx) })
            .MaxBy(m => m.Xarid);

        Console.WriteLine($"
Top mijoz: {topMijoz?.Mijoz} (${topMijoz?.Xarid})");
    }
}

```

## Tushuntirish va Mantiq:
LINQ biznes hisobotlarida murakkab agregatsiyalar, filtrlash va tartiblashlarni toza, o'qilishi oson va deklarativ tarzda bir necha qatorda bajarish imkonini beradi.

## Ishlash natijasi:
```text
Kategoriya hisoboti:
- Elektronika: Jami $2100, Top tovar: Noutbuk
- Kiyim: Jami $230, Top tovar: Kofta

Top mijoz: Vali ($1680)
```

