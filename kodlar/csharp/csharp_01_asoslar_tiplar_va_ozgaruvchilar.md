# 1-Mavzu: C# Asoslari, Ma'lumot Turlari va O'zgaruvchilar (1-50)

Ushbu bo'limda zamonaviy C# (.NET 8/9, C# 12/13) dasturlash tilining poydevori: qiymat va havola turlari (Value vs Reference types), o'zgaruvchilar va o'zgarmaslar (`var`, `const`, `readonly`), nolga ruxsat beruvchi turlar (Nullable Value Types `T?`), satrlar va satr interpolyatsiyasi, xavfsiz va xavfli tip o'zgartirishlar (casting, checked/unchecked), parsing hamda xotirada ma'lumotlarni saqlash tamoyillari chuqur amaliy topshiriqlar bilan o'rganiladi.

# 1-Topshiriq: C# dasturining kirish nuqtasi va Console.WriteLine
## Topshiriq sharti:
C# tilida `Program` sinfi va `Main` statik metodi yordamida konsolga 'Assalomu alaykum, C# dunyosi!' xabarini chiqaruvchi boshlang'ich dasturni yozing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Assalomu alaykum, C# dunyosi!");
    }
}

```

## Tushuntirish va Mantiq:
C# dasturlarining standart kirish nuqtasi `Main` metodi hisoblanadi. CLR (Common Language Runtime) dasturni ishga tushirishda ushbu metodni qidiradi va chaqiradi. `Console.WriteLine` matn oxiriga avtomatik yangi qator belgisini (`\r\n` yoki `\n`) qo'shadi.

## Ishlash natijasi:
```text
Assalomu alaykum, C# dunyosi!
```

# 2-Topshiriq: Kichik butun sonlar: byte va sbyte turlari
## Topshiriq sharti:
1 baytli butun sonlar bo'lgan `byte` (0 dan 255 gacha) va `sbyte` (-128 dan 127 gacha) turlarida o'zgaruvchilar e'lon qiling, ularning eng kichik va eng katta qiymatlarini konsolga chiqaring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        byte musbatBayt = 200;
        sbyte ishoraliBayt = -50;

        Console.WriteLine($"byte qiymati: {musbatBayt}, Diapazoni: [{byte.MinValue} .. {byte.MaxValue}]");
        Console.WriteLine($"sbyte qiymati: {ishoraliBayt}, Diapazoni: [{sbyte.MinValue} .. {sbyte.MaxValue}]");
    }
}

```

## Tushuntirish va Mantiq:
`byte` (System.Byte) unsigned 8-bitli son bo'lib, faqat musbat sonlarni oladi. `sbyte` (System.SByte) signed 8-bitli son bo'lib, ikkilik qo'shimcha (two's complement) ko'rinishida manfiy sonlarni ham ifodalaydi. Ikkalasi ham Stack xotirada 1 bayt joy egallaydi.

## Ishlash natijasi:
```text
byte qiymati: 200, Diapazoni: [0 .. 255]
sbyte qiymati: -50, Diapazoni: [-128 .. 127]
```

# 3-Topshiriq: 16-bitli butun sonlar: short va ushort
## Topshiriq sharti:
2 bayt (16-bit) xotira egallovchi `short` (System.Int16) va `ushort` (System.UInt16) o'zgaruvchilarini e'lon qilib, ularning chegaraviy qiymatlarini namoyish eting.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        short harorat = -25;
        ushort portRaqami = 8080;

        Console.WriteLine($"short: {harorat}, oralig'i: {short.MinValue} dan {short.MaxValue} gacha");
        Console.WriteLine($"ushort: {portRaqami}, oralig'i: {ushort.MinValue} dan {ushort.MaxValue} gacha");
    }
}

```

## Tushuntirish va Mantiq:
`short` 16-bitli ishorali butun son bo'lib, -32,768 dan 32,767 gacha qiymat oladi. `ushort` faqat musbat 0 dan 65,535 gacha bo'ladi (tarmoq portlari uchun juda mos). Stack da aniq 2 bayt joy ajratiladi.

## Ishlash natijasi:
```text
short: -25, oralig'i: -32768 dan 32767 gacha
ushort: 8080, oralig'i: 0 dan 65535 gacha
```

# 4-Topshiriq: 32-bitli butun sonlar: int va uint
## Topshiriq sharti:
C# tilida eng ko'p ishlatiladigan 32-bitli `int` (System.Int32) va `uint` (System.UInt32) turlaridan foydalanib o'zgaruvchilar e'lon qiling va ularning xotira hajmi hamda diapazonini chop eting.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int aholi = 36_000_000; // Raqamlar orasida _ ajratuvchi sifatida ishlatilishi mumkin
        uint id = 4_000_000_000U;

        Console.WriteLine($"O'zbekiston aholisi: {aholi}");
        Console.WriteLine($"Foydalanuvchi ID: {id}");
        Console.WriteLine($"int hajmi: {sizeof(int)} bayt, uint hajmi: {sizeof(uint)} bayt");
    }
}

```

## Tushuntirish va Mantiq:
`int` 32-bit (4 bayt) standart butun son turi. Katta sonlarni o'qish qulay bo'lishi uchun C# da raqamlar orasiga pastki chiziq (`_`) qo'yish mumkin (digit separator). `uint` oxiriga `U` qo'shimchasi qo'yiladi.

## Ishlash natijasi:
```text
O'zbekiston aholisi: 36000000
Foydalanuvchi ID: 4000000000
int hajmi: 4 bayt, uint hajmi: 4 bayt
```

# 5-Topshiriq: 64-bitli butun sonlar: long va ulong
## Topshiriq sharti:
Katta sonlar bilan ishlash uchun 64-bitli (8 bayt) `long` (System.Int64) va `ulong` (System.UInt64) turlaridan foydalaning. Literallar uchun `L` va `UL` suffikslarini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        long yoruglikYiliKm = 9_460_730_472_580_800L;
        ulong maksimalKattaSon = 18_446_744_073_709_551_615UL;

        Console.WriteLine($"1 yorug'lik yili: {yoruglikYiliKm} km");
        Console.WriteLine($"ulong maksimal: {maksimalKattaSon}");
        Console.WriteLine($"long diapazoni: {long.MinValue} .. {long.MaxValue}");
    }
}

```

## Tushuntirish va Mantiq:
`long` 8 bayt bo'lib, astronomik va moliyaviy hisob-kitoblar, bazadagi BigInt ID lar uchun qo'llaniladi. `L` suffiksi sonni `int` emas, balki `long` deb interpretatsiya qilishni kompilyatorga buyuradi.

## Ishlash natijasi:
```text
1 yorug'lik yili: 9460730472580800 km
ulong maksimal: 18446744073709551615
long diapazoni: -9223372036854775808 .. 9223372036854775807
```

# 6-Topshiriq: Suzuvchi nuqtali sonlar: float vs double
## Topshiriq sharti:
Yakka aniqlikdagi `float` (32-bit, `F` suffiksi) va qo'shaloq aniqlikdagi `double` (64-bit) turlarini e'lon qilib, ularning aniqlik darajasini solishtiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        float fNum = 1.0f / 3.0f;
        double dNum = 1.0 / 3.0;

        Console.WriteLine($"float natija (7 ta belgigacha):   {fNum}");
        Console.WriteLine($"double natija (15-17 belgigacha): {dNum}");
    }
}

```

## Tushuntirish va Mantiq:
`float` IEEE 754 standarti bo'yicha 32-bitli bo'lib, 7 xonali aniqlikka ega. `double` esa 64-bitli bo'lib, 15-17 xonali aniqlikni ta'minlaydi. Standart o'nlik kasr literallari (masalan, `1.0`) C# da avtomatik `double` hisoblanadi.

## Ishlash natijasi:
```text
float natija (7 ta belgigacha):   0.33333334
double natija (15-17 belgigacha): 0.3333333333333333
```

# 7-Topshiriq: Yuqori aniqlikdagi moliyaviy tur: decimal
## Topshiriq sharti:
Moliya va bank tizimlarida yaxlitlashdagi xatoliklarning oldini olish uchun 128-bitli `decimal` turidan (`M` suffiksi) foydalaning va `double` bilan hisoblashdagi farqni ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        double d1 = 0.1;
        double d2 = 0.2;
        Console.WriteLine($"double 0.1 + 0.2 == 0.3: {d1 + d2 == 0.3} (Haqiqiy qiymat: {d1 + d2})");

        decimal m1 = 0.1m;
        decimal m2 = 0.2m;
        Console.WriteLine($"decimal 0.1m + 0.2m == 0.3m: {m1 + m2 == 0.3m} (Haqiqiy qiymat: {m1 + m2})");
    }
}

```

## Tushuntirish va Mantiq:
`decimal` 128-bit (16 bayt) o'nlik asosidagi suzuvchi nuqta turi bo'lib, 28-29 ta xonagacha mutlaq aniqlikni ta'minlaydi. Ikkilik suzuvchi nuqta (double/float) 0.1 kabi sonlarni cheksiz davriy kasr sifatida ko'radi, ammo `decimal` uni aniq ifodalaydi.

## Ishlash natijasi:
```text
double 0.1 + 0.2 == 0.3: False (Haqiqiy qiymat: 0.30000000000000004)
decimal 0.1m + 0.2m == 0.3m: True (Haqiqiy qiymat: 0.3)
```

# 8-Topshiriq: Mantiqiy tur: bool va shartli amallar
## Topshiriq sharti:
`bool` (System.Boolean) turidagi o'zgaruvchilar bilan mantiqiy amallarni (`true`, `false`) bajaring va natijani konsolga chiqaring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        bool tizimFaol = true;
        bool xatoBor = false;

        bool ruxsat = tizimFaol && !xatoBor;
        Console.WriteLine($"Tizim holati: {tizimFaol}");
        Console.WriteLine($"Xato mavjudligi: {xatoBor}");
        Console.WriteLine($"Amalga ruxsat bormi: {ruxsat}");
    }
}

```

## Tushuntirish va Mantiq:
`bool` turi faqat `true` yoki `false` qiymat qabul qiladi. Xotirada mantiqiy 1 bit bo'lsa-da, protsessor arxitekturasi va manzillash qulayligi uchun Stack da 1 bayt joy egallaydi. C/C++ dan farqli ravishda C# da sonlarni (`1` yoki `0`) to'g'ridan-to'g'ri `bool` ga o'tkazib bo'lmaydi.

## Ishlash natijasi:
```text
Tizim holati: True
Xato mavjudligi: False
Amalga ruxsat bormi: True
```

# 9-Topshiriq: Belgilar bilan ishlash: char turi va Unicode
## Topshiriq sharti:
`char` (System.Char) 16-bitli UTF-16 belgi turidan foydalanib belgi e'lon qiling, uning kodini ko'ring hamda `char.IsLetter`, `char.IsDigit` metodlarini sinab ko'ring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        char belgi = 'A';
        char raqam = '7';
        char ozbekHarf = 'O';

        Console.WriteLine($"Belgi: {belgi}, ASCII/Unicode kodi: {(int)belgi}");
        Console.WriteLine($"'{belgi}' harfmi: {char.IsLetter(belgi)}");
        Console.WriteLine($"'{raqam}' raqammi: {char.IsDigit(raqam)}");
        Console.WriteLine($"Kichik harfga o'tkazish: {char.ToLower(belgi)}");
    }
}

```

## Tushuntirish va Mantiq:
`char` C# da 2 bayt (16-bit) xotira oladi va Unicode (UTF-16) belgilarini to'liq qo'llab-quvvatlaydi. Belgilar bitta qo'shtirnoq (`'`) ichiga olinadi va sonli qiymatga (ushort ga teng) bevosita o'girilishi mumkin.

## Ishlash natijasi:
```text
Belgi: A, ASCII/Unicode kodi: 65
'A' harfmi: True
'7' raqammi: True
Kichik harfga o'tkazish: a
```

# 10-Topshiriq: Matnlar: string turi va o'zgarmaslik (Immutability)
## Topshiriq sharti:
`string` (System.String) havola turidagi o'zgaruvchi yarating, uning uzunligi (`Length`) va indeks bo'yicha belgilarga murojaat qiling.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        string til = "C# Dasturlash Tili";

        Console.WriteLine($"Matn: {til}");
        Console.WriteLine($"Uzunligi: {til.Length}");
        Console.WriteLine($"Birinchi belgi: {til[0]}");
        Console.WriteLine($"Oxirgi belgi: {til[^1]}"); // C# 8 Index operatori
    }
}

```

## Tushuntirish va Mantiq:
`string` reference type (havola turi) bo'lib, Heap xotirada joylashadi. Satrlar o'zgarmas (immutable) hisoblanadi: har qanday satr amallari mavjud ob'yektni o'zgartirmasdan, Heap da yangi satr ob'yekti yaratadi. `^1` oxirgi elementni bildiradi.

## Ishlash natijasi:
```text
Matn: C# Dasturlash Tili
Uzunligi: 18
Birinchi belgi: C
Oxirgi belgi: i
```

# 11-Topshiriq: Satr interpolyatsiyasi ($) va formatlash
## Topshiriq sharti:
`$` belgisi orqali satr interpolyatsiyasidan foydalanib, o'zgaruvchilarni matn ichiga xavfsiz va toza joylashtiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        string ism = "Temur";
        int yosh = 28;
        string shahar = "Samarqand";

        string xabar = $"Salom, mening ismim {ism}. Yoshim {yosh} da va men {shahar} shahrida yashayman.";
        Console.WriteLine(xabar);
    }
}

```

## Tushuntirish va Mantiq:
Satr interpolyatsiyasi (`$"..."`) kompilyatsiya vaqtida `string.Format` ga yoki yuqori unumdorlikka ega `DefaultInterpolatedStringHandler` ga (.NET 6+) aylanadi. Bu matn birlashtirishdagi xotira ajratishni (allocation) sezilarli darajada kamaytiradi.

## Ishlash natijasi:
```text
Salom, mening ismim Temur. Yoshim 28 da va men Samarqand shahrida yashayman.
```

# 12-Topshiriq: Format ko'rsatkichlari (Specifiers) va tekislash (Alignment)
## Topshiriq sharti:
Satr interpolyatsiyasida pul birligi (`:C`), foiz (`:P`), o'nlik kasr (`:F2`), va ustun tekislash (`{x,10}`) imkoniyatlarini qo'llang.

## Yechim (C# kodi):
```csharp
using System;
using System.Globalization;

internal class Program
{
    static void Main()
    {
        double narx = 1250000.75;
        double foiz = 0.175;
        int id = 42;

        Console.WriteLine($"ID: {id:D5}"); // 5 xonali nol bilan to'ldirish
        Console.WriteLine($"Narx: {narx:N2} so'm"); // Guruhlangan son
        Console.WriteLine($"Stavka: {foiz:P1}"); // Foiz ko'rinishida
        Console.WriteLine($"{"Mahsulot",-15} | {"Narxi",10}");
        Console.WriteLine($"{"Laptop Pro",-15} | {narx,10:N0}");
    }
}

```

## Tushuntirish va Mantiq:
Format ko'rsatkichlari o'zgaruvchidan keyin ikki nuqta (`:`) bilan yoziladi. Vergul (`,`) esa ustun kengligi va tekislashni belgilaydi: musbat son o'ngga, manfiy son chapga tekislaydi.

## Ishlash natijasi:
```text
ID: 00042
Narx: 1,250,000.75 so'm
Stavka: 17.5%
Mahsulot         |      Narxi
Laptop Pro      |  1,250,001
```

# 13-Topshiriq: Verbatim satrlar: @ belgisi va fayl yo'llari
## Topshiriq sharti:
Escape belgilarini (`\`) inkor qiluvchi va ko'p qatorli matnlarni to'g'ridan-to'g'ri yozishga imkon beruvchi `@` (verbatim string) belgisidan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        // Oddiy satrda har bir slesh uchun qo'shaloq \ yozish kerak
        string oddiyYol = "C:\\Users\\User\\Documents\\loyiha.txt";

        // Verbatim satrda sleshlar o'z holicha o'qiladi
        string verbatimYol = @"C:\Users\User\Documents\loyiha.txt";

        string kopQatorli = @"Birinchi qator
Ikkinchi qator
Uchinchi qator";

        Console.WriteLine($"Verbatim yo'l: {verbatimYol}");
        Console.WriteLine(kopQatorli);
    }
}

```

## Tushuntirish va Mantiq:
`@` belgisi satrdagi barcha escape belgilarini (masalan, `\n`, `\t`) o'chiradi va ularni oddiy matn sifatida qabul qiladi. Faqat qo'shtirnoq belgisi kiritilishi kerak bo'lsa, uni juft qilib `""` yoziladi.

## Ishlash natijasi:
```text
Verbatim yo'l: C:\Users\User\Documents\loyiha.txt
Birinchi qator
Ikkinchi qator
Uchinchi qator
```

# 14-Topshiriq: C# 11 Raw String Literals: """ sintaksisi
## Topshiriq sharti:
C# 11 da kiritilgan Raw String Literals (`"""`) orqali JSON va XML matnlarini hech qanday qo'shtirnoq yoki slesh muammosisiz yozing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        string json = """
        {
            "id": 101,
            "ism": "Jasur",
            "kasbi": "Dasturchi"
        }
        """;

        Console.WriteLine("Raw JSON matni:");
        Console.WriteLine(json);
    }
}

```

## Tushuntirish va Mantiq:
Kamida uchta qo'shtirnoq (`"""`) bilan boshlanuvchi Raw String Literals satr ichidagi har qanday qo'shtirnoq va yangi qatorlarni asl holicha saqlaydi. Yopiluvchi `"""` ning surilishi (indentation) matnning chap chegarasini avtomatik belgilaydi.

## Ishlash natijasi:
```text
Raw JSON matni:
{
    "id": 101,
    "ism": "Jasur",
    "kasbi": "Dasturchi"
}
```

# 15-Topshiriq: var kalit so'zi va tipni avtomatik aniqlash (Type Inference)
## Topshiriq sharti:
`var` kalit so'zi yordamida har xil tiplardagi o'zgaruvchilarni e'lon qiling va ularning asl .NET turlarini `GetType()` orqali aniqlang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        var ism = "Olim";
        var yosh = 24;
        var vazn = 72.5;
        var faol = true;

        Console.WriteLine($"ism tipi: {ism.GetType().Name}");
        Console.WriteLine($"yosh tipi: {yosh.GetType().Name}");
        Console.WriteLine($"vazn tipi: {vazn.GetType().Name}");
        Console.WriteLine($"faol tipi: {faol.GetType().Name}");
    }
}

```

## Tushuntirish va Mantiq:
`var` bu dinamik tip emas! Kompilyatsiya paytida C# kompilyatori o'ng tomondagi qiymatga qarab o'zgaruvchi turini qat'iy (strongly-typed) belgilaydi. Dastur ishlash tezligiga (runtime) hech qanday salbiy ta'sir ko'rsatmaydi.

## Ishlash natijasi:
```text
ism tipi: String
yosh tipi: Int32
vazn tipi: Double
faol tipi: Boolean
```

# 16-Topshiriq: const kalit so'zi: Kompilyatsiya vaqtidagi o'zgarmaslar
## Topshiriq sharti:
`const` orqali qiymati hech qachon o'zgarmas bo'lgan o'zgarmaslarni e'lon qiling va ularni formulada qo'llang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    const double Pi = 3.141592653589793;
    const string DasturNomi = "Geometriya Hisoblagich";

    static void Main()
    {
        double radius = 5.0;
        double doiraYuzi = Pi * radius * radius;

        Console.WriteLine($"{DasturNomi}");
        Console.WriteLine($"Radius {radius} bo'lgan doira yuzi: {doiraYuzi:F2}");
    }
}

```

## Tushuntirish va Mantiq:
`const` o'zgaruvchilari kompilyatsiya vaqtida ma'lum bo'lishi shart. Kompilyator ularning qiymatini to'g'ridan-to'g'ri IL (Intermediate Language) kodi ichiga kiritib yuboradi (inlining). Shuning uchun `const` ga obyektlar yoki runtime hisob-kitoblar berilmaydi.

## Ishlash natijasi:
```text
Geometriya Hisoblagich
Radius 5 bo'lgan doira yuzi: 78.54
```

# 17-Topshiriq: readonly modifikatori: Dastur ishlashi paytidagi o'zgarmas
## Topshiriq sharti:
Sinf maydonlarida `readonly` modifikatorini e'lon qiling va unga faqat konstruktorda qiymat berish mumkinligini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class ServerSozlama
{
    public readonly string Host;
    public readonly int Port;
    public readonly DateTime BoshlanganVaqt;

    public ServerSozlama(string host, int port)
    {
        Host = host;
        Port = port;
        BoshlanganVaqt = DateTime.Now;
    }
}

internal class Program
{
    static void Main()
    {
        var sozlama = new ServerSozlama("127.0.0.1", 5000);
        Console.WriteLine($"Server: {sozlama.Host}:{sozlama.Port}");
        Console.WriteLine($"Ishga tushgan vaqt yili: {sozlama.BoshlanganVaqt.Year}");
        // sozlama.Port = 8080; // XATO! readonly maydonni qayta o'zgartirib bo'lmaydi
    }
}

```

## Tushuntirish va Mantiq:
`readonly` maydonlar faqat e'lon qilingan joyda yoki sinf konstruktorida bir martagina initsializatsiya qilinishi mumkin. `const` dan farqli ravishda ularga qiymat dastur ishlashi paytida (runtime) beriladi.

## Ishlash natijasi:
```text
Server: 127.0.0.1:5000
Ishga tushgan vaqt yili: 2026
```

# 18-Topshiriq: Nullable Value Types: int? va Nullable<T> tushunchasi
## Topshiriq sharti:
Odatda `null` qiymat qabul qilmaydigan qiymat turlariga (Value types) `?` belgisi orqali `null` qiymat berishni va `.HasValue` xossasini tekshiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int? yosh = null;

        Console.WriteLine($"yosh o'zgaruvchisida qiymat bormi: {yosh.HasValue}");

        yosh = 25;
        Console.WriteLine($"yosh o'zgaruvchisida qiymat bormi: {yosh.HasValue}");
        if (yosh.HasValue)
        {
            Console.WriteLine($"Foydalanuvchi yoshi: {yosh.Value}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`int?` bu aslida `System.Nullable<int>` strukturasining qisqartmasidir. U ikkita maydondan iborat: haqiqiy qiymat va mantiqiy `hasValue` bayrog'i. Agar qiymat `null` bo'lganda `.Value` chaqirilsa, `InvalidOperationException` yuzaga keladi.

## Ishlash natijasi:
```text
yosh o'zgaruvchisida qiymat bormi: False
yosh o'zgaruvchisida qiymat bormi: True
Foydalanuvchi yoshi: 25
```

# 19-Topshiriq: GetValueOrDefault() metodi bilan xavfsiz qiymat olish
## Topshiriq sharti:
`Nullable<T>` turlarida `null` bo'lgan holatda standart qiymat yoki berilgan zaxira qiymatni qaytaruvchi `GetValueOrDefault()` metodini qo'llang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        double? maosh = null;

        double standartMaosh = maosh.GetValueOrDefault(); // double ning default qiymati 0.0
        double belgilanganMaosh = maosh.GetValueOrDefault(3000.0);

        Console.WriteLine($"Standart zaxira: {standartMaosh}");
        Console.WriteLine($"Belgilangan zaxira: {belgilanganMaosh}");

        maosh = 4500.50;
        Console.WriteLine($"Haqiqiy maosh: {maosh.GetValueOrDefault(3000.0)}");
    }
}

```

## Tushuntirish va Mantiq:
`GetValueOrDefault()` metodi xatolik otmasdan xavfsiz ishlashni kafolatlaydi. Agar o'zgaruvchi `null` bo'lsa, ko'rsatilgan zaxira qiymatni qaytaradi; agar qiymat mavjud bo'lsa, o'sha qiymatni o'zini uzatadi.

## Ishlash natijasi:
```text
Standart zaxira: 0
Belgilangan zaxira: 3000
Haqiqiy maosh: 4500.5
```

# 20-Topshiriq: Noaniq (Implicit) tip konvertatsiyasi: Kengaytirish
## Topshiriq sharti:
Kichikroq hajmdagi qiymat turini kattaroq hajmdagi turga hech qanday ma'lumot yo'qotishsiz avtomatik o'tkazishni namoyish eting.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int kichikSon = 12345;
        long kattaSon = kichikSon; // int -> long avtomatik
        float suzuvchiSon = kichikSon; // int -> float avtomatik
        double aniqSon = suzuvchiSon; // float -> double avtomatik

        Console.WriteLine($"int: {kichikSon}");
        Console.WriteLine($"long: {kattaSon}");
        Console.WriteLine($"float: {suzuvchiSon}");
        Console.WriteLine($"double: {aniqSon}");
    }
}

```

## Tushuntirish va Mantiq:
Implicit (oshkormas) o'girish ma'lumot yo'qolishi xavfi bo'lmaganda (kichik tur kattaroq turga o'tganda) C# kompilyatori tomonidan avtomatik bajariladi. Masalan, 32-bitli `int` 64-bitli `long` ga hech qanday maxsus sintaksissiz o'tadi.

## Ishlash natijasi:
```text
int: 12345
long: 12345
float: 12345
double: 12345
```

# 21-Topshiriq: Oshkora (Explicit) tip konvertatsiyasi: Qisqartirish va kasting
## Topshiriq sharti:
Kattaroq turdan kichikroq turga qasddan o'tishda `(tur)` kasting operatoridan foydalaning va ma'lumot yo'qolish holatini kuzating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        double pi = 3.99999;
        int butunPi = (int)pi; // Kasr qismi shunchaki tashlab yuboriladi

        long katta = 300L;
        byte bayt = (byte)katta; // 300 > 255 bo'lgani uchun to'lib-toshish sodir bo'ladi

        Console.WriteLine($"double {pi} -> int {butunPi}");
        Console.WriteLine($"long {katta} -> byte {bayt} (300 % 256 = {300 % 256})");
    }
}

```

## Tushuntirish va Mantiq:
Explicit (oshkora) kastingda dasturchi ma'lumot yo'qolishini o'z zimmasiga oladi. `double` dan `int` ga o'tishda yaxlitlanmaydi, balki kasr qismi kesib tashlanadi (truncation). `byte` ga sig'magan bitlar esa tashqariga chiqib ketadi.

## Ishlash natijasi:
```text
double 3.99999 -> int 3
long 300 -> byte 44 (300 % 256 = 44)
```

# 22-Topshiriq: checked va unchecked bloklari: Xotira to'lib-toshish nazorati
## Topshiriq sharti:
Butun sonli hisoblashlarda xotira to'lib-toshishi (integer overflow) yuz berganda `checked` orqali `OverflowException` tutishni va `unchecked` xatti-harakatini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int maks = int.MaxValue;

        // unchecked: xato otmaydi, son aylanib eng kichik manfiyga o'tadi
        int aylanma = unchecked(maks + 1);
        Console.WriteLine($"unchecked natija: {aylanma}");

        try
        {
            // checked: to'lib-toshish sodir bo'lsa istisno otadi
            int xavfsiz = checked(maks + 1);
        }
        catch (OverflowException)
        {
            Console.WriteLine("checked bloki: Xotira to'lib toshishi muvaffaqiyatli ushlandi!");
        }
    }
}

```

## Tushuntirish va Mantiq:
C# da standart holatda arifmetik amallar unumdorlik uchun `unchecked` rejimda ishlaydi. Biroq moliyaviy hisob-kitoblarda `checked` bloki kutilmagan aylanma sonlarning (masalan musbatdan manfiyga aylanib qolish) oldini oladi va `OverflowException` chiqaradi.

## Ishlash natijasi:
```text
unchecked natija: -2147483648
checked bloki: Xotira to'lib toshishi muvaffaqiyatli ushlandi!
```

# 23-Topshiriq: Satrlarni sonlarga aylantirish: int.Parse va FormatException
## Topshiriq sharti:
`int.Parse` va `double.Parse` metodlaridan foydalanib matnni songa o'giring va noto'g'ri format berilgandagi istisnoni ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        string sonMatn = "1024";
        int son = int.Parse(sonMatn);
        Console.WriteLine($"Muvaffaqiyatli aylantirildi: {son * 2}");

        string notogriMatn = "1024a";
        try
        {
            int xato = int.Parse(notogriMatn);
        }
        catch (FormatException ex)
        {
            Console.WriteLine($"Kutilgan xatolik ushlandi: {ex.GetType().Name}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`Parse` metodi matnni qat'iy tekshiradi. Agar matn kutilgan formatga to'liq mos kelmasa, dastur darhol `FormatException` xatoligini vujudga keltiradi. Shuning uchun foydalanuvchi kiritgan ma'lumotlar uchun `TryParse` tavsiya etiladi.

## Ishlash natijasi:
```text
Muvaffaqiyatli aylantirildi: 2048
Kutilgan xatolik ushlandi: FormatException
```

# 24-Topshiriq: Xavfsiz parsing: int.TryParse va out parametri
## Topshiriq sharti:
`int.TryParse` metodi yordamida dastur to'xtab qolishining oldini olib, satrni xavfsiz songa o'tkazuvchi dastur tuzing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        string[] qiymatlar = { "550", "salom", "99999999999999999999", "12" };

        foreach (var q in qiymatlar)
        {
            if (int.TryParse(q, out int natija))
            {
                Console.WriteLine($"'{q}' -> Muvaffaqiyatli: {natija}");
            }
            else
            {
                Console.WriteLine($"'{q}' -> Songa aylantirib bo'lmadi!");
            }
        }
    }
}

```

## Tushuntirish va Mantiq:
`TryParse` metodi istisno otmaydi (zero-exception overhead). U amaliyot muvaffaqiyatli bo'lsa `true`, aks holda `false` qaytaradi va natijani `out` o'zgaruvchisiga yozib beradi. Bu server unumdorligini keskin oshiradi.

## Ishlash natijasi:
```text
'550' -> Muvaffaqiyatli: 550
'salom' -> Songa aylantirib bo'lmadi!
'99999999999999999999' -> Songa aylantirib bo'lmadi!
'12' -> Muvaffaqiyatli: 12
```

# 25-Topshiriq: Convert sinfi orqali universal konvertatsiya va sanoq sistemalari
## Topshiriq sharti:
`System.Convert` sinfidan foydalanib sonlarni ikkilik (binary), o'n oltilik (hexadecimal) satrlarga va aksincha aylantiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int son = 255;

        string ikkilik = Convert.ToString(son, 2);
        string onOltilik = Convert.ToString(son, 16).ToUpper();

        Console.WriteLine($"O'nlik son: {son}");
        Console.WriteLine($"Ikkilikda (Base 2): {ikkilik}");
        Console.WriteLine($"O'n oltilikda (Base 16): {onOltilik}");

        int qaytaOlingan = Convert.ToInt32(ikkilik, 2);
        Console.WriteLine($"Ikkilikdan qayta tiklangan son: {qaytaOlingan}");
    }
}

```

## Tushuntirish va Mantiq:
`Convert` sinfi .NET ning asosiy turlari o'rtasida universal ko'prik vazifasini o'taydi. `Convert.ToString(son, asos)` metodi sonni 2, 8, 10 yoki 16 sanoq sistemasidagi matnga o'girish imkoniyatini taqdim etadi.

## Ishlash natijasi:
```text
O'nlik son: 255
Ikkilikda (Base 2): 11111111
O'n oltilikda (Base 16): FF
Ikkilikdan qayta tiklangan son: 255
```

# 26-Topshiriq: default operatori va turlarning boshlang'ich qiymatlari
## Topshiriq sharti:
C# da turli ma'lumot turlarining (`int`, `bool`, `char`, `double`, `string`, `DateTime`) `default` qiymatlarini ekranga chiqaring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int defInt = default;
        bool defBool = default;
        char defChar = default;
        double defDouble = default;
        string? defString = default;
        DateTime defDate = default;

        Console.WriteLine($"int default: {defInt}");
        Console.WriteLine($"bool default: {defBool}");
        Console.WriteLine($"char default: {(int)defChar} (bo'sh belgi '\0')");
        Console.WriteLine($"double default: {defDouble}");
        Console.WriteLine($"string default: {(defString == null ? "null" : defString)}");
        Console.WriteLine($"DateTime default: {defDate}");
    }
}

```

## Tushuntirish va Mantiq:
C# da barcha turlar avtomatik ravishda xotirada nolga (zero-initialized) tenglashtiriladi. Sonli turlar uchun bu 0, mantiqiy tur uchun `false`, havolali turlar (reference types) uchun esa `null` hisoblanadi. C# 7.1 dan boshlab `default(T)` o'rniga qisqa `default` literali yetarli.

## Ishlash natijasi:
```text
int default: 0
bool default: False
char default: 0 (bo'sh belgi '\0')
double default: 0
string default: null
DateTime default: 1/1/0001 12:00:00 AM
```

# 27-Topshiriq: sizeof operatori va qiymat turlarining xotira hajmi
## Topshiriq sharti:
`sizeof` operatoridan foydalanib barcha asosiy qiymat turlarining xotiradagi aniq bayt hajmini aniqlang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        Console.WriteLine($"bool:    {sizeof(bool)} bayt");
        Console.WriteLine($"byte:    {sizeof(byte)} bayt");
        Console.WriteLine($"char:    {sizeof(char)} bayt");
        Console.WriteLine($"short:   {sizeof(short)} bayt");
        Console.WriteLine($"int:     {sizeof(int)} bayt");
        Console.WriteLine($"long:    {sizeof(long)} bayt");
        Console.WriteLine($"float:   {sizeof(float)} bayt");
        Console.WriteLine($"double:  {sizeof(double)} bayt");
        Console.WriteLine($"decimal: {sizeof(decimal)} bayt");
    }
}

```

## Tushuntirish va Mantiq:
`sizeof` operatori kompilyatsiya vaqtida qiymat turining Stack dagi bayt hajmini qaytaradi. Masalan, `decimal` 16 bayt, `double` va `long` 8 bayt xotira oladi. Bu xotira samaradorligini tahlil qilishda juda muhimdir.

## Ishlash natijasi:
```text
bool:    1 bayt
byte:    1 bayt
char:    2 bayt
short:   2 bayt
int:     4 bayt
long:    8 bayt
float:   4 bayt
double:  8 bayt
decimal: 16 bayt
```

# 28-Topshiriq: typeof operatori va System.Type metama'lumotlari
## Topshiriq sharti:
`typeof` operatori orqali ma'lumot turlarining to'liq nomlari, ularning qiymat (ValueType) yoki havola (Class) turi ekanligini tekshiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        Type intTip = typeof(int);
        Type strTip = typeof(string);

        Console.WriteLine($"int to'liq nomi: {intTip.FullName}");
        Console.WriteLine($"int ValueType mi: {intTip.IsValueType}");
        Console.WriteLine($"string to'liq nomi: {strTip.FullName}");
        Console.WriteLine($"string ValueType mi: {strTip.IsValueType}");
        Console.WriteLine($"string Class mi: {strTip.IsClass}");
    }
}

```

## Tushuntirish va Mantiq:
`typeof` kompilyatsiya vaqtida turga oid `System.Type` ob'yektini oladi. U Reflection (aks ettirish) tizimining poydevori bo'lib, Turning tuzilishi va metama'lumotlarini dastur kodida tekshirish imkonini beradi.

## Ishlash natijasi:
```text
int to'liq nomi: System.Int32
int ValueType mi: True
string to'liq nomi: System.String
string ValueType mi: False
string Class mi: True
```

# 29-Topshiriq: Math sinfi: Yaxlitlash usullari va Bankir qoidasi
## Topshiriq sharti:
`Math.Round`, `Math.Floor`, `Math.Ceiling` metodlarini qo'llang va C# dagi Bankir yaxlitlash qoidasini (`MidpointRounding.ToEven`) namoyish eting.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        double son1 = 2.5;
        double son2 = 3.5;

        Console.WriteLine($"Math.Round(2.5): {Math.Round(son1)} (Eng yaqin juft songa: 2)");
        Console.WriteLine($"Math.Round(3.5): {Math.Round(son2)} (Eng yaqin juft songa: 4)");
        Console.WriteLine($"Oddiy arifmetik yaxlitlash (2.5 -> AwayFromZero): {Math.Round(son1, MidpointRounding.AwayFromZero)}");
        Console.WriteLine($"Math.Floor(2.9): {Math.Floor(2.9)} (Pastga)");
        Console.WriteLine($"Math.Ceiling(2.1): {Math.Ceiling(2.1)} (Yuqoriga)");
    }
}

```

## Tushuntirish va Mantiq:
IEEE 754 standarti bo'yicha `Math.Round` standart holatda 'Bankir yaxlitlashi'ni (ToEven) ishlatadi. Bu o'rtadagi .5 qiymatlarini eng yaqin juft songa qarab yaxlitlaydi va katta statistik hisob-kitoblarda xatolik yig'ilib ketishining oldini oladi.

## Ishlash natijasi:
```text
Math.Round(2.5): 2 (Eng yaqin juft songa: 2)
Math.Round(3.5): 4 (Eng yaqin juft songa: 4)
Oddiy arifmetik yaxlitlash (2.5 -> AwayFromZero): 3
Math.Floor(2.9): 2 (Pastga)
Math.Ceiling(2.1): 3 (Yuqoriga)
```

# 30-Topshiriq: Math sinfi: Clamp, Min, Max va Abs funksiyalari
## Topshiriq sharti:
Qiymatlarni oraliqda chegaralash uchun `Math.Clamp`, ekstremumlarni topish uchun `Math.Min`/`Math.Max` va modul uchun `Math.Abs` funksiyalaridan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int tezlik = 140;
        int ruxsatEtilgan = Math.Clamp(tezlik, 0, 110);
        int kichik = Math.Min(45, 90);
        int katta = Math.Max(45, 90);
        int modul = Math.Abs(-50);

        Console.WriteLine($"Haqiqiy tezlik: {tezlik}, Chegaralangan tezlik: {ruxsatEtilgan}");
        Console.WriteLine($"Min: {kichik}, Max: {katta}, Abs(-50): {modul}");
    }
}

```

## Tushuntirish va Mantiq:
`Math.Clamp(qiymat, min, max)` .NET Core 2.0 da kiritilgan juda foydali metod bo'lib, o'zgaruvchining berilgan oraliqdan chiqib ketmasligini ta'minlaydi: agar qiymat `min` dan kichik bo'lsa `min`, `max` dan katta bo'lsa `max` qaytaradi.

## Ishlash natijasi:
```text
Haqiqiy tezlik: 140, Chegaralangan tezlik: 110
Min: 45, Max: 90, Abs(-50): 50
```

# 31-Topshiriq: Bitwise operatorlar: Mantiqiy VA (&) hamda Mantiqiy YOKI (|)
## Topshiriq sharti:
Bit darajasidagi `&` va `|` operatorlari yordamida ikkilik bitlar ustida amallar bajaring va natijani ikkilik ko'rinishda ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        byte a = 0b1100; // O'nlikda 12
        byte b = 0b1010; // O'nlikda 10

        int vaNatija = a & b;  // 0b1000 = 8
        int yokiNatija = a | b; // 0b1110 = 14

        Console.WriteLine($"a & b: {vaNatija} (Ikkilikda: {Convert.ToString(vaNatija, 2).PadLeft(4, '0')})");
        Console.WriteLine($"a | b: {yokiNatija} (Ikkilikda: {Convert.ToString(yokiNatija, 2).PadLeft(4, '0')})");
    }
}

```

## Tushuntirish va Mantiq:
`&` amali har ikkala sonning mos biti 1 bo'lgandagina 1 beradi. `|` amali esa kamida bitta bit 1 bo'lsa 1 beradi. Bu amallar tarmoq maskalari, ruxsatlar va apparat darajasidagi drayverlar bilan ishlashda asosiy vositadir.

## Ishlash natijasi:
```text
a & b: 8 (Ikkilikda: 1000)
a | b: 14 (Ikkilikda: 1110)
```

# 32-Topshiriq: Bitwise operatorlar: XOR (^) va Inversiya (~)
## Topshiriq sharti:
Bit darajasidagi istisno qiluvchi YOKI (`^`) va birga to'ldiruvchi inkor (`~`) amallarini namoyish eting.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        byte x = 0b1100; // 12
        byte y = 0b1010; // 10

        int xorNatija = x ^ y; // 0b0110 = 6
        int inkor = ~x;        // Barcha bitlarni teskarisiga aylantirish

        Console.WriteLine($"x ^ y: {xorNatija} (Ikkilikda: {Convert.ToString(xorNatija, 2).PadLeft(4, '0')})");
        Console.WriteLine($"~x: {inkor}");
    }
}

```

## Tushuntirish va Mantiq:
`^` (XOR) amali bitlar har xil bo'lganda 1, bir xil bo'lganda 0 qaytaradi (kriptografiya va oddiy shifrlashda ko'p qo'llanadi). `~` amali sonning barcha bitlarini 0 dan 1 ga va 1 dan 0 ga ag'daradi.

## Ishlash natijasi:
```text
x ^ y: 6 (Ikkilikda: 0110)
~x: -13
```

# 33-Topshiriq: Bitwise siljitish: Chapga (<<) va O'ngga (>>) siljitish
## Topshiriq sharti:
Bitlarni chapga va o'ngga siljitish operatorlarini 2 ning darajalariga tezkor ko'paytirish va bo'lish uchun qo'llang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int son = 5; // 0b0101

        int chapga = son << 2; // 5 * 2^2 = 20 (0b010100)
        int ongga = son >> 1;  // 5 / 2^1 = 2 (0b0010)

        Console.WriteLine($"5 << 2 = {chapga}");
        Console.WriteLine($"5 >> 1 = {ongga}");
    }
}

```

## Tushuntirish va Mantiq:
`x << n` amali son bitlarini `n` pozitsiyaga chapga siljitadi, bu `x * 2^n` ga teng. `x >> n` esa o'ngga siljitadi, bu butun sonli `x / 2^n` ga teng. Ushbu amallar protsessor registrlarida eng tez bajariluvchi instruksiyalardir.

## Ishlash natijasi:
```text
5 << 2 = 20
5 >> 1 = 2
```

# 34-Topshiriq: Enum (Sanab o'tiladigan turlar) asoslari
## Topshiriq sharti:
Hafta kunlarini ifodalovchi `enum` e'lon qiling, o'zgaruvchiga qiymat bering va uning nomini hamda raqamli qiymatini ekranga chiqaring.

## Yechim (C# kodi):
```csharp
using System;

enum HaftaKuni
{
    Dushanba,
    Seshanba,
    Chorshanba,
    Payshanba,
    Juma,
    Shanba,
    Yakshanba
}

internal class Program
{
    static void Main()
    {
        HaftaKuni bugun = HaftaKuni.Juma;

        Console.WriteLine($"Bugungi kun: {bugun}");
        Console.WriteLine($"Raqamli indeksi: {(int)bugun}");
    }
}

```

## Tushuntirish va Mantiq:
`enum` o'zgarmas sonli qiymatlar to'plamini inson tushunadigan nomlar bilan bog'laydi. Standart holatda indekslash 0 dan boshlanadi (`Dushanba = 0`) va har bir keyingi element 1 taga ortadi.

## Ishlash natijasi:
```text
Bugungi kun: Juma
Raqamli indeksi: 4
```

# 35-Topshiriq: Enum asosiy turlarini (Underlying Types) belgilash
## Topshiriq sharti:
Xotirani tejash maqsadida `enum` asosiy turini `byte` ga o'zgartiring va elementlarga qo'lda sonli qiymatlar biriktiring.

## Yechim (C# kodi):
```csharp
using System;

enum HTTPStatus : ushort
{
    OK = 200,
    Created = 201,
    BadRequest = 400,
    Unauthorized = 401,
    NotFound = 404,
    InternalServerError = 500
}

internal class Program
{
    static void Main()
    {
        HTTPStatus javob = HTTPStatus.NotFound;

        Console.WriteLine($"Status nomi: {javob}");
        Console.WriteLine($"Status kodi: {(ushort)javob}");
        Console.WriteLine($"Enum asosi: {Enum.GetUnderlyingType(typeof(HTTPStatus)).Name}");
    }
}

```

## Tushuntirish va Mantiq:
Standart holatda `enum` ichida `int` (4 bayt) ishlatiladi. Katta hajmdagi massivlar yoki tarmoq paketlarida xotirani tejash uchun `enum Nom : byte` yoki `: ushort` yordamida kichikroq turlarni belgilash mumkin.

## Ishlash natijasi:
```text
Status nomi: NotFound
Status kodi: 404
Enum asosi: UInt16
```

# 36-Topshiriq: [Flags] atributi bilan bitmask Enum yaratish
## Topshiriq sharti:
Bir vaqtning o'zida bir nechta huquqlarni belgilash imkonini beruvchi `[Flags]` atributli `enum` yarating va `HasFlag` metodini sinang.

## Yechim (C# kodi):
```csharp
using System;

[Flags]
enum FoydalanuvchiHuquqi
{
    HechQanday = 0,
    Oqish = 1 << 0,     // 1
    Yozish = 1 << 1,    // 2
    Ochirish = 1 << 2,  // 4
    Admin = Oqish | Yozish | Ochirish // 7
}

internal class Program
{
    static void Main()
    {
        FoydalanuvchiHuquqi huquq = FoydalanuvchiHuquqi.Oqish | FoydalanuvchiHuquqi.Yozish;

        Console.WriteLine($"Foydalanuvchi huquqlari: {huquq}");
        Console.WriteLine($"Yozish huquqi bormi: {huquq.HasFlag(FoydalanuvchiHuquqi.Yozish)}");
        Console.WriteLine($"O'chirish huquqi bormi: {huquq.HasFlag(FoydalanuvchiHuquqi.Ochirish)}");
    }
}

```

## Tushuntirish va Mantiq:
`[Flags]` atributi kompilyatorga ushbu enum bitlar kombinatsiyasi (bitmask) sifatida ishlatilishini bildiradi. Har bir element 2 ning darajasida (`1, 2, 4, 8...`) bo'lishi shart. `ToString()` chaqirilganda birlashtirilgan nomlar vergul bilan ajratib ko'rsatiladi.

## Ishlash natijasi:
```text
Foydalanuvchi huquqlari: Oqish, Yozish
Yozish huquqi bormi: True
O'chirish huquqi bormi: False
```

# 37-Topshiriq: Enum metodlari: GetNames, GetValues va Parse
## Topshiriq sharti:
`System.Enum` yordamida enum ichidagi barcha nomlar va qiymatlarni aylanib chiqing hamda matndan enumga o'giring.

## Yechim (C# kodi):
```csharp
using System;

enum Rang { Qizil, Yashil, Kok }

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Mavjud ranglar:");
        foreach (string nom in Enum.GetNames<Rang>()) // C# .NET 5+ generic GetNames
        {
            Console.WriteLine($"- {nom}");
        }

        string matn = "Yashil";
        Rang tanlangan = Enum.Parse<Rang>(matn);
        Console.WriteLine($"Matndan olingan rang: {tanlangan}");
    }
}

```

## Tushuntirish va Mantiq:
`Enum.GetNames<T>()` barcha elementlar nomini satr massivi sifatida qaytaradi. `Enum.Parse<T>()` esa satrli ifodani tegishli enum qiymatiga o'tkazadi (katta-kichik harf sezgirligini nazorat qilish ham mumkin).

## Ishlash natijasi:
```text
Mavjud ranglar:
- Qizil
- Yashil
- Kok
Matndan olingan rang: Yashil
```

# 38-Topshiriq: Value Type vs Reference Type: Nusxalash harakati
## Topshiriq sharti:
Qiymat turi (`int`, `struct`) va havola turi (`class`) o'zgaruvchilari boshqa o'zgaruvchiga o'zlashtirilganda ularning qanday nusxalanishini solishtiring.

## Yechim (C# kodi):
```csharp
using System;

class NusxaObyekt
{
    public int Qiymat;
}

internal class Program
{
    static void Main()
    {
        // Value Type nusxalanishi
        int a = 10;
        int b = a;
        b = 99;
        Console.WriteLine($"Value Type -> a: {a}, b: {b}");

        // Reference Type nusxalanishi
        var obj1 = new NusxaObyekt { Qiymat = 10 };
        var obj2 = obj1;
        obj2.Qiymat = 99;
        Console.WriteLine($"Reference Type -> obj1: {obj1.Qiymat}, obj2: {obj2.Qiymat}");
    }
}

```

## Tushuntirish va Mantiq:
Value Type (qiymat turi) Stack da saqlanadi va yangi o'zgaruvchiga o'tganda uning qiymati to'liq nusxalanadi. Reference Type (havola turi) ob'yektining o'zi Heap da saqlanadi, Stack da esa unga havola (manzil) turadi; havolani nusxalaganda ikkala ko'rsatkich ham bitta ob'yektga qarab qoladi.

## Ishlash natijasi:
```text
Value Type -> a: 10, b: 99
Reference Type -> obj1: 99, obj2: 99
```

# 39-Topshiriq: String Immutability: Heap da yangi ob'yekt yaratilishi
## Topshiriq sharti:
Satrlarni o'zgartirish amallarida mavjud ob'yekt o'zgarmasligi, aksincha xotirada yangi havola hosil bo'lishini `object.ReferenceEquals` orqali ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        string satr1 = "Salom";
        string dastlabkiHavola = satr1;

        satr1 += " Dunyo"; // Matn birlashtirildi

        Console.WriteLine($"satr1: {satr1}");
        Console.WriteLine($"dastlabkiHavola: {dastlabkiHavola}");
        Console.WriteLine($"Ular bitta xotira manzilidami: {object.ReferenceEquals(satr1, dastlabkiHavola)}");
    }
}

```

## Tushuntirish va Mantiq:
C# da satrlar xavfsizlik va ko'p oqimli ishlash qulayligi uchun qat'iy o'zgarmas (immutable) qilingan. Satrga qo'shimcha kiritilganda CLR Heap da butunlay yangi string nusxasini yaratadi va manzilini o'zgaruvchiga biriktiradi.

## Ishlash natijasi:
```text
satr1: Salom Dunyo
dastlabkiHavola: Salom
Ular bitta xotira manzilidami: False
```

# 40-Topshiriq: String Interning va String Pool mexanizmi
## Topshiriq sharti:
CLR tomonidan bir xil literallarni birlashtiruvchi String Pool jadvali va `string.Intern` metodining ishlashini namoyish eting.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        string s1 = "Toshkent";
        string s2 = "Toshkent";

        // Literallar avtomatik intern qilinadi
        Console.WriteLine($"Literallar bitta manzildami: {object.ReferenceEquals(s1, s2)}");

        // Runtime da yig'ilgan satr
        string qism = "Tosh";
        string s3 = qism + "kent";
        Console.WriteLine($"Runtime satr avtomatik intern bo'ladimi: {object.ReferenceEquals(s1, s3)}");

        // Qo'lda intern qilish
        string s4 = string.Intern(s3);
        Console.WriteLine($"string.Intern(s3) original s1 bilan tengmi: {object.ReferenceEquals(s1, s4)}");
    }
}

```

## Tushuntirish va Mantiq:
CLR xotirani tejash uchun String Interning mexanizmidan foydalanadi. Kodda ko'rsatilgan literallar ichki String Pool lug'atiga saqlanadi va qayta foydalaniladi. `string.Intern()` metodi runtime da yaratilgan satrlarni ham shu hovuzga qo'shish imkonini beradi.

## Ishlash natijasi:
```text
Literallar bitta manzildami: True
Runtime satr avtomatik intern bo'ladimi: False
string.Intern(s3) original s1 bilan tengmi: True
```

# 41-Topshiriq: StringBuilder: Katta matnlarni yig'ishda xotira samaradorligi
## Topshiriq sharti:
`System.Text.StringBuilder` yordamida sikl ichida minglab satrlarni Heap da keraksiz axlat (garbage) yaratmasdan birlashtiring.

## Yechim (C# kodi):
```csharp
using System;
using System.Text;

internal class Program
{
    static void Main()
    {
        var sb = new StringBuilder();
        sb.Append("Boshlanish: ");

        for (int i = 1; i <= 5; i++)
        {
            sb.Append($"[{i}] ");
        }

        sb.Replace("[3]", "[UCH]");
        string yakuniy = sb.ToString();

        Console.WriteLine(yakuniy);
    }
}

```

## Tushuntirish va Mantiq:
Oddiy `string +=` sikl ichida har safar yangi satr yaratib, Garbage Collector ga katta yuk yuklaydi. `StringBuilder` esa o'z ichida dinamik kengayuvchi belgilar buferini (char array) saqlaydi va modifikatsiyalarni o'sha bufer ustida bajaradi.

## Ishlash natijasi:
```text
Boshlanish: [1] [2] [UCH] [4] [5]
```

# 42-Topshiriq: ValueTuple: Inline kortejlar va dekonstruksiya (Deconstruction)
## Topshiriq sharti:
C# 7+ da kiritilgan `ValueTuple` orqali alohida sinf ochmasdan bir nechta qiymatni guruhlang va ularni alohida o'zgaruvchilarga dekonstruksiya qiling.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        // Anonim tuple
        var talaba = ("Sarvar", 21, 4.8);

        // Dekonstruksiya qilish
        var (ism, yosh, gpa) = talaba;

        Console.WriteLine($"Talaba: {ism}, Yoshi: {yosh}, Ball: {gpa}");
    }
}

```

## Tushuntirish va Mantiq:
`ValueTuple` bu yengil `struct` (qiymat turi) bo'lib, Stack da saqlanadi va Heap da ob'yekt ajratmaydi. Dekonstruksiya sintaksisi kortej ichidagi elementlarni bir qatorda mustaqil mahalliy o'zgaruvchilarga taqsimlab beradi.

## Ishlash natijasi:
```text
Talaba: Sarvar, Yoshi: 21, Ball: 4.8
```

# 43-Topshiriq: Nomlangan Tuple (Named Tuples) va kod o'qiluvchanligi
## Topshiriq sharti:
Elementlariga aniq nomlar berilgan tuple yarating va ularga nomlari orqali murojaat qiling.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static (int Son, string Matn, bool Holat) MalumotBer()
    {
        return (42, "Muvaffaqiyatli", true);
    }

    static void Main()
    {
        var natija = MalumotBer();

        Console.WriteLine($"Kod: {natija.Son}");
        Console.WriteLine($"Xabar: {natija.Matn}");
        Console.WriteLine($"Status: {natija.Holat}");
    }
}

```

## Tushuntirish va Mantiq:
Nomlangan tuple elementlari dasturchi uchun qulay bo'lib, `Item1, Item2` o'rniga ma'noli nomlar bilan murojaat qilish imkonini beradi. Ushbu nomlar faqat kompilyatsiya vaqtida mavjud bo'lib, runtime da hech qanday ortiqcha yuk yaratmaydi.

## Ishlash natijasi:
```text
Kod: 42
Xabar: Muvaffaqiyatli
Status: True
```

# 44-Topshiriq: Sana va vaqt: DateTime va DateTimeOffset
## Topshiriq sharti:
`DateTime` va vaqt mintaqasini hisobga oluvchi `DateTimeOffset` strukturalaridan foydalanib joriy vaqtni chiqaring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        DateTime hozir = DateTime.Now;
        DateTime utc = DateTime.UtcNow;
        DateTimeOffset mintaqaBilan = DateTimeOffset.Now;

        Console.WriteLine($"Mahalliy vaqt yili: {hozir.Year}");
        Console.WriteLine($"UTC vaqt soati: {utc.Hour}");
        Console.WriteLine($"Vaqt mintaqasi surilishi: {mintaqaBilan.Offset}");
    }
}

```

## Tushuntirish va Mantiq:
`DateTimeOffset` UTC vaqtiga nisbatan mintaqaviy surilishni (masalan `+05:00` Toshkent vaqti) o'z ichida saqlaydi. Serverlararo va bulutli tizimlarda vaqt chalkashliklarining oldini olish uchun zamonaviy .NET da `DateTimeOffset` tavsiya etiladi.

## Ishlash natijasi:
```text
Mahalliy vaqt yili: 2026
UTC vaqt soati: 6
Vaqt mintaqasi surilishi: 05:00:00
```

# 45-Topshiriq: TimeSpan: Vaqt oraliqlari va davomiylik hisobi
## Topshiriq sharti:
`TimeSpan` yordamida ikki sana orasidagi farqni (kun, soat, daqiqa) hisoblang va ma'lum vaqt oralig'ini sanaga qo'shing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        DateTime boshlanish = new DateTime(2026, 1, 1);
        DateTime tugash = new DateTime(2026, 1, 10, 12, 30, 0);

        TimeSpan farq = tugash - boshlanish;

        Console.WriteLine($"Jami kunlar: {farq.TotalDays}");
        Console.WriteLine($"Jami soatlar: {farq.TotalHours}");
        Console.WriteLine($"Kun va soat ko'rinishi: {farq.Days} kun, {farq.Hours} soat, {farq.Minutes} daqiqa");
    }
}

```

## Tushuntirish va Mantiq:
`TimeSpan` vaqt davomiyligini ifodalovchi qiymat turi (struct) bo'lib, ichki 100 nanosoniyalik tiktaklar (ticks) asosida ishlaydi. Sanalar o'rtasidagi ayirish amali avtomatik `TimeSpan` hosil qiladi.

## Ishlash natijasi:
```text
Jami kunlar: 9.520833333333334
Jami soatlar: 228.5
Kun va soat ko'rinishi: 9 kun, 12 soat, 30 daqiqa
```

# 46-Topshiriq: Guid: Takrorlanmas global identifikatorlar generatsiyasi
## Topshiriq sharti:
Ma'lumotlar bazasida birlamchi kalitlar yoki sessiya ID lari uchun `Guid.NewGuid()` yordamida 128-bitli takrorlanmas qiymat hosil qiling.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        Guid id1 = Guid.NewGuid();
        Guid boshGuid = Guid.Empty;

        Console.WriteLine($"Yaratilgan GUID uzunligi: {id1.ToString().Length} ta belgi");
        Console.WriteLine($"Bo'sh GUID: {boshGuid}");
        Console.WriteLine($"Standart format: {id1:D}");
        Console.WriteLine($"Chiziqchalarsiz: {id1:N}");
    }
}

```

## Tushuntirish va Mantiq:
`Guid` (Globally Unique Identifier) 16 bayt (128 bit) hajmdagi struktura bo'lib, dunyo miqyosida takrorlanmaslik ehtimoli juda yuqori bo'lgan raqamlar hosil qiladi. Tarmoqlangan (distributed) tizimlarda identifikatorlar yaratish uchun standart vositadir.

## Ishlash natijasi:
```text
Yaratilgan GUID uzunligi: 36 ta belgi
Bo'sh GUID: 00000000-0000-0000-0000-000000000000
Standart format: e3b0c442-98fc-1c14-9afb-4c8996fb9242
Chiziqchalarsiz: e3b0c44298fc1c149afb4c8996fb9242
```

# 47-Topshiriq: object turi va System.Object imkoniyatlari
## Topshiriq sharti:
C# dagi barcha turlarning ildizi bo'lgan `object` turiga ixtiyoriy qiymatni o'zlashtiring va uning `ToString()`, `GetType()` metodlarini tekshiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        object obj1 = 123;
        object obj2 = "Salom";
        object obj3 = 45.67;

        Console.WriteLine($"obj1 tipi: {obj1.GetType().Name}, qiymati: {obj1}");
        Console.WriteLine($"obj2 tipi: {obj2.GetType().Name}, qiymati: {obj2}");
        Console.WriteLine($"obj3 tipi: {obj3.GetType().Name}, qiymati: {obj3}");
    }
}

```

## Tushuntirish va Mantiq:
`System.Object` .NET tip iyerarxiyasining eng yuqori pog'onasida turadi. Barcha turlar (shu jumladan primitiv sonlar ham) bevosita yoki bilvosita `object` dan meros oladi va uning 4 ta asosiy metodiga (`Equals`, `GetHashCode`, `GetType`, `ToString`) ega bo'ladi.

## Ishlash natijasi:
```text
obj1 tipi: Int32, qiymati: 123
obj2 tipi: String, qiymati: Salom
obj3 tipi: Double, qiymati: 45.67
```

# 48-Topshiriq: Boxing (Qutilash) jarayoni va uning xotira yuki
## Topshiriq sharti:
Qiymat turini (`int`) `object` turiga o'tkazishda Stack dan Heap ga ma'lumot ko'chirilishi (Boxing) jarayonini kuzating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int son = 777; // Stack da joylashgan

        // Boxing: Stack dagi qiymat Heap dagi yangi ob'yekt ichiga qadoqlanadi
        object quti = son;

        son = 888; // Original son o'zgardi

        Console.WriteLine($"Stack dagi son: {son}");
        Console.WriteLine($"Heap dagi quti: {quti}");
    }
}

```

## Tushuntirish va Mantiq:
Boxing paytida CLR Heap da yangi ob'yekt ajratadi va qiymat turidagi baytlarni o'sha ob'yekt tanasiga nusxalaydi. Bu Heap xotirada joy egallashi va keyinchalik Garbage Collector tomonidan tozalanishi sababli, unumdorlikka salbiy ta'sir ko'rsatadi.

## Ishlash natijasi:
```text
Stack dagi son: 888
Heap dagi quti: 777
```

# 49-Topshiriq: Unboxing (Qutidan chiqarish) va InvalidCastException xavfi
## Topshiriq sharti:
Heap dagi `object` ichidan qiymat turini asl holiga qaytarish (Unboxing) va noto'g'ri turga o'girishdagi xatolikni ko'ring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int original = 500;
        object quti = original; // Boxing

        // To'g'ri Unboxing
        int ochilgan = (int)quti;
        Console.WriteLine($"Muvaffaqiyatli ochildi: {ochilgan}");

        // Noto'g'ri Unboxing
        try
        {
            // int qutisidan to'g'ridan-to'g'ri short qilib ochib bo'lmaydi
            short xato = (short)quti;
        }
        catch (InvalidCastException ex)
        {
            Console.WriteLine($"Ushlangan xato: {ex.GetType().Name} - Tur aynan mos bo'lishi shart!");
        }
    }
}

```

## Tushuntirish va Mantiq:
Unboxing jarayonida CLR avval ob'yekt aynan so'ralgan turga tegishli ekanligini qat'iy tekshiradi, so'ngra baytlarni Stack ga nusxalaydi. Agar kasting kutilgan turga aniq mos kelmasa, dastur darhol `InvalidCastException` beradi.

## Ishlash natijasi:
```text
Muvaffaqiyatli ochildi: 500
Ushlangan xato: InvalidCastException - Tur aynan mos bo'lishi shart!
```

# 50-Topshiriq: dynamic kalit so'zi va DLR (Dynamic Language Runtime)
## Topshiriq sharti:
`dynamic` kalit so'zidan foydalanib kompilyatsiya vaqtidagi tip tekshiruvini chetlab o'ting va uning `var` hamda `object` dan farqini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        dynamic dinamikQiymat = 100;
        Console.WriteLine($"Dastlabki: {dinamikQiymat}, turi: {dinamikQiymat.GetType().Name}");

        dinamikQiymat = "Endi men matnman";
        Console.WriteLine($"Keyingi: {dinamikQiymat}, turi: {dinamikQiymat.GetType().Name}");

        dinamikQiymat = dinamikQiymat.ToUpper(); // Kompilyator tekshirmaydi, runtime da chaqiriladi
        Console.WriteLine($"Natija: {dinamikQiymat}");
    }
}

```

## Tushuntirish va Mantiq:
`dynamic` C# 4 da kiritilgan bo'lib, barcha tekshiruvlarni dastur ishlashi paytiga (runtime) suradi. `var` faqat sintaktik qulaylik (kompilyatsiyada aniqlanadi), `object` da esa metodlarni to'g'ridan-to'g'ri kastingiz chaqirib bo'lmaydi. `dynamic` esa DLR (Dynamic Language Runtime) orqali metodlarni dinamik qidiradi.

## Ishlash natijasi:
```text
Dastlabki: 100, turi: Int32
Keyingi: Endi men matnman, turi: String
Natija: ENDI MEN MATNMAN
```

