# 6-Mavzu: OOP Merosxo'rlik va Polimorfizm (251-300)

Ushbu bo'limda C# tilida kodni qayta ishlatish va dinamik polimorfizm poydevorlari: sinflar merosxo'rligi (`:`), `base` kalit so'zi va ota sinf konstruktorlari, `virtual` va `override` metodlar, virtual metodlar jadvali (vtable), `sealed class` va devirtualizatsiya optimallashuvi, abstrakt sinflar va metodlar (`abstract`), a'zolarni soya qilish (shadowing via `new`), C# 9 kovariant qaytuvchi turlar (covariant returns), konstruktor ichida virtual metod chaqirish xavfi hamda Liskov almashtirish tamoyili (LSP) bo'yicha 50 ta amaliy topshiriq jamlangan.

# 251-Topshiriq: Merosxo'rlik asoslari: Ota va bola sinflar bog'lanishi
## Topshiriq sharti:
`Hayvon` asosiy sinfini va undan meros oluvchi `Kuchuk` sinfini yarating va umumiy maydonlarni qayta ishlatishni ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

class Hayvon
{
    public string Nomi = "";

    public void Oziqlan()
    {
        Console.WriteLine($"{Nomi} ovqatlanmoqda.");
    }
}

class Kuchuk : Hayvon
{
    public void Vovulla()
    {
        Console.WriteLine($"{Nomi}: Vov-vov!");
    }
}

internal class Program
{
    static void Main()
    {
        Kuchuk k = new Kuchuk();
        k.Nomi = "Olapar";
        k.Oziqlan(); // Ota sinf metodi
        k.Vovulla(); // Bola sinf metodi
    }
}

```

## Tushuntirish va Mantiq:
Merosxo'rlik (`class Bola : Ota`) bitta sinfning xossa va metodlarini boshqa sinfga o'tkazish imkonini beradi. C# da har bir sinf faqat bitta to'g'ridan-to'g'ri ota sinfdan meros olishi mumkin (Single Inheritance).

## Ishlash natijasi:
```text
Olapar ovqatlanmoqda.
Olapar: Vov-vov!
```

# 252-Topshiriq: base kalit so'zi: Ota sinf konstruktoriga parametr uzatish
## Topshiriq sharti:
Bola sinf konstruktoridan ota sinf parametrli konstruktorini `base(...)` orqali chaqiring.

## Yechim (C# kodi):
```csharp
using System;

class Shaxs
{
    public string Ism { get; }

    public Shaxs(string ism)
    {
        Ism = ism;
        Console.WriteLine($"1. Shaxs konstruktori bajarildi: {Ism}");
    }
}

class Talaba : Shaxs
{
    public string Universitet { get; }

    public Talaba(string ism, string universitet) : base(ism)
    {
        Universitet = universitet;
        Console.WriteLine($"2. Talaba konstruktori bajarildi: {Universitet}");
    }
}

internal class Program
{
    static void Main()
    {
        var t = new Talaba("Farrux", "TATU");
    }
}

```

## Tushuntirish va Mantiq:
Obyekt yaratilayotganda doimo ota sinfning konstruktori birinchi bo'lib ishlaydi. Agar ota sinfda parametrsiz konstruktor bo'lmasa, bola sinf konstruktorida `: base(...)` orqali kerakli argumentlarni uzatish majburiydir.

## Ishlash natijasi:
```text
1. Shaxs konstruktori bajarildi: Farrux
2. Talaba konstruktori bajarildi: TATU
```

# 253-Topshiriq: base orqali ota sinf metodini kengaytirish
## Topshiriq sharti:
Bola sinf metodida ota sinfning asl metodini `base.Metod()` orqali chaqirib, ustiga yangi mantiq qo'shing.

## Yechim (C# kodi):
```csharp
using System;

class Xodim
{
    public virtual void IshRejasi()
    {
        Console.WriteLine("9:00 - Tizimga kirish va rejalashtirish");
    }
}

class Boshliq : Xodim
{
    public override void IshRejasi()
    {
        base.IshRejasi(); // Ota sinf mantiqini bajarish
        Console.WriteLine("10:00 - Jamoa yig'ilishi (Daily Standup)");
    }
}

internal class Program
{
    static void Main()
    {
        Xodim x = new Boshliq();
        x.IshRejasi();
    }
}

```

## Tushuntirish va Mantiq:
`base.Metod()` meros olingan kodni to'liq tashlab yubormasdan, uning natijasini saqlab qolgan holda bola sinfda kengaytirish imkonini beradi.

## Ishlash natijasi:
```text
9:00 - Tizimga kirish va rejalashtirish
10:00 - Jamoa yig'ilishi (Daily Standup)
```

# 254-Topshiriq: protected modifikatori: Faqat oila a'zolari uchun ochiqlik
## Topshiriq sharti:
`protected` maydon faqat ota sinf va uning barcha vorislari ichida ko'rinishini namoyish eting.

## Yechim (C# kodi):
```csharp
using System;

class TizimModuli
{
    protected string MaxfiyKalit = "SECRET_KEY_123";
}

class XavfsizlikModuli : TizimModuli
{
    public void Tekshir()
    {
        // protected maydon voris sinf ichida ko'rinadi
        Console.WriteLine($"Maxfiy kalit o'qildi: {MaxfiyKalit}");
    }
}

internal class Program
{
    static void Main()
    {
        var x = new XavfsizlikModuli();
        x.Tekshir();

        // Console.WriteLine(x.MaxfiyKalit); // KOMPILYATSIYA XATOSI! Tashqaridan kirish taqiqlangan
    }
}

```

## Tushuntirish va Mantiq:
`protected` a'zolar tashqi dunyo uchun `private`, lekin barcha merosxo'r sinflar uchun `public` kabi ishlaydi. Bu meros arxitekturasida ichki holatni xavfsiz almashishning asosiy usulidir.

## Ishlash natijasi:
```text
Maxfiy kalit o'qildi: SECRET_KEY_123
```

# 255-Topshiriq: virtual va override: Dinamik polimorfizm
## Topshiriq sharti:
Ota sinfdagi `virtual` metodni bola sinflarda `override` qilib, bir xil chaqiruvda har xil natija oling.

## Yechim (C# kodi):
```csharp
using System;

class Shakl
{
    public virtual void Chiz()
    {
        Console.WriteLine("Noma'lum shakl chizilmoqda");
    }
}

class Doira : Shakl
{
    public override void Chiz()
    {
        Console.WriteLine("O Doira chizildi");
    }
}

class Kvadrat : Shakl
{
    public override void Chiz()
    {
        Console.WriteLine("[] Kvadrat chizildi");
    }
}

internal class Program
{
    static void Main()
    {
        Shakl s1 = new Doira();
        Shakl s2 = new Kvadrat();

        s1.Chiz(); // Doira ning Chiz metodi chaqiriladi
        s2.Chiz(); // Kvadrat ning Chiz metodi chaqiriladi
    }
}

```

## Tushuntirish va Mantiq:
`virtual` metodi ota sinfda e'lon qilinadi va bola sinflarda `override` qilinishi mumkinligini bildiradi. Qaysi metod ishga tushishi o'zgaruvchi turiga qarab emas, balki Heap dagi haqiqiy obyekt turiga qarab runtime da aniqlanadi (Dynamic Dispatch).

## Ishlash natijasi:
```text
O Doira chizildi
[] Kvadrat chizildi
```

# 256-Topshiriq: Polimorfik to'plamlar: List<OtaTur> bilan ishlash
## Topshiriq sharti:
Ota turidagi umumiy ro'yxatda har xil turdagi obyektlarni saqlab, bitta sikl ichida ularning polimorfik metodlarini chaqiring.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

abstract class MusiqaAsbobi
{
    public abstract void OvozChiqar();
}

class Gitara : MusiqaAsbobi
{
    public override void OvozChiqar() => Console.WriteLine("Gitara: Ting-ting...");
}

class Pianino : MusiqaAsbobi
{
    public override void OvozChiqar() => Console.WriteLine("Pianino: Do-re-mi...");
}

internal class Program
{
    static void Main()
    {
        List<MusiqaAsbobi> orkestr = [ new Gitara(), new Pianino() ];

        foreach (var asbob in orkestr)
        {
            asbob.OvozChiqar();
        }
    }
}

```

## Tushuntirish va Mantiq:
Polimorfizm dasturchiga umumiy interfeys orqali turli obyektlar bilan bir xil muomala qilish imkonini beradi. Yangi asbob qo'shilganda `foreach` siklini o'zgartirish talab qilinmaydi (Open/Closed Principle).

## Ishlash natijasi:
```text
Gitara: Ting-ting...
Pianino: Do-re-mi...
```

# 257-Topshiriq: sealed class: Meros olishni butunlay taqiqlash
## Topshiriq sharti:
`sealed` modifikatori yordamida sinfni muhrlang va undan boshqa hech kim meros ololmasligini ta'minlang.

## Yechim (C# kodi):
```csharp
using System;

sealed class XavfsizKassa
{
    public void PulSaqla() => Console.WriteLine("Mablag' xavfsiz saqlandi.");
}

// class Ogrilik : XavfsizKassa { } // KOMPILYATSIYA XATOSI! sealed sinfdan meros olib bo'lmaydi

internal class Program
{
    static void Main()
    {
        var kassa = new XavfsizKassa();
        kassa.PulSaqla();
    }
}

```

## Tushuntirish va Mantiq:
`sealed` kalit so'zi sinfdan meros olinishini to'xtatadi. Xavfsizlikdan tashqari, bu .NET JIT kompilyatoriga virtual metodlarni to'g'ridan-to'g'ri chaqiruvga aylantirish (devirtualization) va kodni tezlashtirish imkonini beradi.

## Ishlash natijasi:
```text
Mablag' xavfsiz saqlandi.
```

# 258-Topshiriq: sealed override: Metod qayta yozilishini to'xtatish
## Topshiriq sharti:
Ota sinfdan kelgan virtual metodni bola sinfda qayta yozing va keyingi avlodlar uchun `sealed` qilib yoping.

## Yechim (C# kodi):
```csharp
using System;

class Ota
{
    public virtual void Amaliyot() => Console.WriteLine("Ota amaliyoti");
}

class Ogil : Ota
{
    public sealed override void Amaliyot() => Console.WriteLine("O'g'il amaliyoti (muhrlandi)");
}

class Nabira : Ogil
{
    // public override void Amaliyot() { } // KOMPILYATSIYA XATOSI! Metod Ogil da sealed qilingan
}

internal class Program
{
    static void Main()
    {
        Ota o = new Nabira();
        o.Amaliyot();
    }
}

```

## Tushuntirish va Mantiq:
`sealed override` meros zanjirining ma'lum bir bo'g'inida metod xulq-atvorini qat'iylashtirish va keyingi avlodlar tomonidan uning o'zgartirib yuborilishining oldini olish uchun xizmat qiladi.

## Ishlash natijasi:
```text
O'g'il amaliyoti (muhrlandi)
```

# 259-Topshiriq: Abstrakt sinflar (abstract class) va to'liq bo'lmagan qoliplar
## Topshiriq sharti:
Instansiyasi olinmaydigan, faqat boshqa sinflar uchun asos bo'luvchi `abstract` sinf e'lon qiling.

## Yechim (C# kodi):
```csharp
using System;

abstract class AvtoUlov
{
    public string Model { get; }
    public AvtoUlov(string model) => Model = model;

    public void Signal() => Console.WriteLine($"{Model}: Bip-bip!");
}

class Samolyot : AvtoUlov
{
    public Samolyot(string model) : base(model) { }
}

internal class Program
{
    static void Main()
    {
        // AvtoUlov u = new AvtoUlov("Test"); // KOMPILYATSIYA XATOSI! Abstrakt sinfdan obyekt olib bo'lmaydi
        Samolyot s = new Samolyot("Boeing 787");
        s.Signal();
    }
}

```

## Tushuntirish va Mantiq:
Abstrakt sinf umumiy tushunchalarni (masalan `AvtoUlov`) ifodalaydi. Uning o'zidan bevosita obyekt yaratib bo'lmaydi, faqat undan meros olgan aniq (concrete) sinflar orqali obyekt olinadi.

## Ishlash natijasi:
```text
Boeing 787: Bip-bip!
```

# 260-Topshiriq: Abstrakt metodlar (abstract methods)
## Topshiriq sharti:
Tanasiz abstrakt metod e'lon qilib, barcha bolalar sinflarini uni amalga oshirishga majburlang.

## Yechim (C# kodi):
```csharp
using System;

abstract class MaoshHisoblagich
{
    // Tanasi yo'q, bolalar sinfi majburiy yozishi shart
    public abstract decimal Hisobla(int soatlar);
}

class DasturchiMaoshi : MaoshHisoblagich
{
    public override decimal Hisobla(int soatlar) => soatlar * 250000m;
}

class MenejerMaoshi : MaoshHisoblagich
{
    public override decimal Hisobla(int soatlar) => 5000000m + (soatlar * 150000m);
}

internal class Program
{
    static void Main()
    {
        MaoshHisoblagich dev = new DasturchiMaoshi();
        MaoshHisoblagich mgr = new MenejerMaoshi();

        Console.WriteLine($"Dasturchi 40 soat: {dev.Hisobla(40):N0} so'm");
        Console.WriteLine($"Menejer 40 soat:   {mgr.Hisobla(40):N0} so'm");
    }
}

```

## Tushuntirish va Mantiq:
Abstrakt metod faqat abstrakt sinf ichida e'lon qilinishi mumkin. Uning tanasi bo'lmaydi (`{}`) va nuqta-vergul bilan tugaydi. Har bir noabstrakt merosxo'r sinf ushbu metodni `override` qilishi shart.

## Ishlash natijasi:
```text
Dasturchi 40 soat: 10,000,000 so'm
Menejer 40 soat:   11,000,000 so'm
```

# 261-Topshiriq: Abstrakt xossalar (Abstract Properties)
## Topshiriq sharti:
Merosxo'r sinflarda amalga oshirilishi shart bo'lgan abstrakt xossalarni belgilang.

## Yechim (C# kodi):
```csharp
using System;

abstract class TizimXabari
{
    public abstract string XabarTuri { get; }
    public abstract int Kod { get; }
}

class XatoXabari : TizimXabari
{
    public override string XabarTuri => "Kritik Xato";
    public override int Kod => 500;
}

internal class Program
{
    static void Main()
    {
        TizimXabari x = new XatoXabari();
        Console.WriteLine($"Turi: {x.XabarTuri}, Kod: {x.Kod}");
    }
}

```

## Tushuntirish va Mantiq:
Metodlar kabi xossalar ham `abstract` bo'lishi mumkin. Bu bola sinfning muayyan xossaga qat'iy ega bo'lishini shart qilib qo'yadi.

## Ishlash natijasi:
```text
Turi: Kritik Xato, Kod: 500
```

# 262-Topshiriq: A'zolarni soya qilish (Member Shadowing: new kalit so'zi)
## Topshiriq sharti:
Ota sinfdagi oddiy (virtual bo'lmagan) metodni bola sinfda `new` orqali yashiring va polimorfizm buzilishini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

class Baza
{
    public void Salomatlik() => Console.WriteLine("Baza salomatligi");
}

class Hosila : Baza
{
    // 'new' ota metodni almashtirmaydi, faqat yashiradi (shadowing)
    public new void Salomatlik() => Console.WriteLine("Hosila salomatligi");
}

internal class Program
{
    static void Main()
    {
        Hosila h = new Hosila();
        h.Salomatlik(); // Hosila ning metodi ishlaydi

        Baza b = h;
        b.Salomatlik(); // Diqqat! Baza ning metodi ishlaydi, chunki bu virtual emas!
    }
}

```

## Tushuntirish va Mantiq:
`new` kalit so'zi polimorfizm emas, balki nomni yashirish (shadowing) dir. Agar obyektga ota sinf ko'rsatkichi (`Baza b = h`) orqali qaralsa, ota sinfning eski metodi chaqirilib qoladi.

## Ishlash natijasi:
```text
Hosila salomatligi
Baza salomatligi
```

# 263-Topshiriq: Override vs New: Amaliy taqqoslash jadvali
## Topshiriq sharti:
`override` (haqiqiy polimorfizm) va `new` (soya qilish) farqini yagona dasturda yonma-yon ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

class Ota
{
    public virtual void VirtualAmal() => Console.WriteLine("Ota: Virtual");
    public void OddiyAmal() => Console.WriteLine("Ota: Oddiy");
}

class Bola : Ota
{
    public override void VirtualAmal() => Console.WriteLine("Bola: Override (Haqiqiy polimorfizm)");
    public new void OddiyAmal() => Console.WriteLine("Bola: New (Faqat soya)");
}

internal class Program
{
    static void Main()
    {
        Ota refOta = new Bola();

        refOta.VirtualAmal(); // Obyekt turiga qarab Bola ning metodi ishlaydi
        refOta.OddiyAmal();   // Havola turiga qarab Ota ning metodi ishlaydi
    }
}

```

## Tushuntirish va Mantiq:
`override` da VTable orqali dinamik bog'lanish yuz beradi va havola qanday bo'lishidan qat'i nazar oxirgi avlod kodi ishlaydi. `new` da esa statik bog'lanish bo'lib, chaqiruv havola turiga bog'liq bo'ladi.

## Ishlash natijasi:
```text
Bola: Override (Haqiqiy polimorfizm)
Ota: Oddiy
```

# 264-Topshiriq: Upcasting (Yuqoriga kasting): Xavfsiz umumlashtirish
## Topshiriq sharti:
Bola sinf obyektini ota sinf turidagi o'zgaruvchiga o'zlashtirishni (Upcasting) ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

class Xodim { public string Ism = "Ali"; }
class Menejer : Xodim { public int BolimId = 10; }

internal class Program
{
    static void Main()
    {
        Menejer m = new Menejer();

        // Upcasting: Har doim 100% xavfsiz va oshkormas (implicit)
        Xodim x = m;

        Console.WriteLine($"Xodim ismi: {x.Ism}");
        // Console.WriteLine(x.BolimId); // XATO! Xodim orqali Menejer xossasi ko'rinmaydi
    }
}

```

## Tushuntirish va Mantiq:
Upcasting da bola sinf obyekti ota sinf obyekti sifatida ko'riladi. Bu har doim xavfsizdir, chunki bola sinf ota sinfning barcha a'zolariga to'liq ega bo'lishi kafolatlangan.

## Ishlash natijasi:
```text
Xodim ismi: Ali
```

# 265-Topshiriq: Downcasting (Pastga kasting) va InvalidCastException xavfi
## Topshiriq sharti:
Ota sinf havolasidan bola sinfga qaytish (Downcasting) va noto'g'ri kastingdagi istisnoni ko'ring.

## Yechim (C# kodi):
```csharp
using System;

class Hayvon { }
class Kuchuk : Hayvon { }
class Mushuk : Hayvon { }

internal class Program
{
    static void Main()
    {
        Hayvon h = new Kuchuk(); // Aslida Kuchuk

        // To'g'ri Downcasting
        Kuchuk k = (Kuchuk)h;
        Console.WriteLine("Kuchuk muvaffaqiyatli kasting qilindi.");

        // Noto'g'ri Downcasting
        try
        {
            Mushuk m = (Mushuk)h; // Kuchukni Mushukka o'girib bo'lmaydi!
        }
        catch (InvalidCastException ex)
        {
            Console.WriteLine($"Kutilgan xato: {ex.GetType().Name}");
        }
    }
}

```

## Tushuntirish va Mantiq:
Downcasting paytida CLR obyektning Type Handle dagi haqiqiy turini tekshiradi. Agar obyekt so'ralgan turga to'g'ri kelmasa, darhol `InvalidCastException` tashlanadi.

## Ishlash natijasi:
```text
Kuchuk muvaffaqiyatli kasting qilindi.
Kutilgan xato: InvalidCastException
```

# 266-Topshiriq: as operatori bilan xavfsiz Downcasting
## Topshiriq sharti:
`as` operatori orqali xatolik otmasdan xavfsiz pastga kasting qiling.

## Yechim (C# kodi):
```csharp
using System;

class Hujjat { }
class PdfHujjat : Hujjat { public void ChopEt() => Console.WriteLine("PDF chop etildi."); }
class ExcelHujjat : Hujjat { }

internal class Program
{
    static void ChopQil(Hujjat h)
    {
        PdfHujjat? pdf = h as PdfHujjat;
        if (pdf != null)
        {
            pdf.ChopEt();
        }
        else
        {
            Console.WriteLine("Ushbu hujjat PDF emas, chop etib bo'lmaydi.");
        }
    }

    static void Main()
    {
        ChopQil(new PdfHujjat());
        ChopQil(new ExcelHujjat());
    }
}

```

## Tushuntirish va Mantiq:
`as` operatori kasting o'xshamasa istisno otmaydi, balki `null` qaytaradi. Bu tekshiruvlarni yumshoq va tezkor qilishga imkon beradi.

## Ishlash natijasi:
```text
PDF chop etildi.
Ushbu hujjat PDF emas, chop etib bo'lmaydi.
```

# 267-Topshiriq: is operatori bilan zamonaviy Pattern Matching kastingi
## Topshiriq sharti:
Zamonaviy C# da `as` o'rniga tavsiya etiladigan `is` naqshidan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

class Qurilma { }
class Printer : Qurilma { public void Bosma() => Console.WriteLine("Hujjat bosildi."); }

internal class Program
{
    static void Ishlat(Qurilma q)
    {
        if (q is Printer p)
        {
            p.Bosma();
        }
        else
        {
            Console.WriteLine("Qurilma printer emas.");
        }
    }

    static void Main()
    {
        Ishlat(new Printer());
        Ishlat(new Qurilma());
    }
}

```

## Tushuntirish va Mantiq:
`if (q is Printer p)` bitta qatorda ham turni tekshiradi, ham `null` emasligiga ishonch hosil qiladi, ham yangi `p` o'zgaruvchisiga kasting qiladi.

## Ishlash natijasi:
```text
Hujjat bosildi.
Qurilma printer emas.
```

# 268-Topshiriq: Liskov almashinish tamoyili (LSP - SOLID)
## Topshiriq sharti:
Bola sinf ota sinf o'rnida uning asosiy qoidalarini buzmasdan ishlashi kerakligi haqidagi mashhur To'rtburchak-Kvadrat muammosini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

// LSP ga zid klassik misol:
class Tortburchak
{
    public virtual int Eni { get; set; }
    public virtual int Boyi { get; set; }
    public int Yuza() => Eni * Boyi;
}

class Kvadrat : Tortburchak
{
    public override int Eni { set { base.Eni = value; base.Boyi = value; } }
    public override int Boyi { set { base.Eni = value; base.Boyi = value; } }
}

internal class Program
{
    static void MaydonniTekshir(Tortburchak t)
    {
        t.Eni = 5;
        t.Boyi = 4;
        // Kutilgan yuza: 5 * 4 = 20
        Console.WriteLine($"Haqiqiy yuza: {t.Yuza()} (Kutilgan: 20)");
    }

    static void Main()
    {
        MaydonniTekshir(new Tortburchak());
        MaydonniTekshir(new Kvadrat()); // LSP buzildi: natija 16 chiqadi!
    }
}

```

## Tushuntirish va Mantiq:
Liskov Substitution Principle (LSP) ga ko'ra, bola sinf ota sinfning barcha xatti-harakat shartlarini saqlashi shart. Kvadrat geometrik jihatdan to'rtburchak bo'lsa-da, OOP da uning Eni va Bo'yi mustaqil emas, shuning uchun meros olish noto'g'ri hisoblanadi.

## Ishlash natijasi:
```text
Haqiqiy yuza: 20 (Kutilgan: 20)
Haqiqiy yuza: 16 (Kutilgan: 20)
```

# 269-Topshiriq: Virtual metodlar jadvali (vtable) qanday ishlashi
## Topshiriq sharti:
Virtual metod chaqiruvlarida CLR qanday indirektsiya bajarishini tushuntiring.

## Yechim (C# kodi):
```csharp
using System;

class BazaClass
{
    public virtual void Metod() => Console.WriteLine("Baza");
}

class VorisClass : BazaClass
{
    public override void Metod() => Console.WriteLine("Voris");
}

internal class Program
{
    static void Main()
    {
        BazaClass obj = new VorisClass();

        // 1. CLR obj ning Type Handle siga boradi (MethodTable)
        // 2. MethodTable ichidagi vtable jadvalini o'qiydi
        // 3. vtable dagi 'Metod' slotidagi ko'rsatkichga sakraydi
        obj.Metod();

        Console.WriteLine("Virtual chaqiruv bitta qo'shimcha xotira ko'rsatkichi (pointer dereference) orqali ishlaydi.");
    }
}

```

## Tushuntirish va Mantiq:
Har bir sinf turi uchun CLR MethodTable yaratadi. Undagi vtable har bir virtual metodning xotiradagi manzillarini saqlaydi. Bu moslashuvchanlik beradi, ammo oddiy chaqiruvga nisbatan biroz (nanosoniyalar) sekinroq bo'ladi.

## Ishlash natijasi:
```text
Voris
Virtual chaqiruv bitta qo'shimcha xotira ko'rsatkichi (pointer dereference) orqali ishlaydi.
```

# 270-Topshiriq: C# 9 Kovariant qaytuvchi turlar (Covariant Returns)
## Topshiriq sharti:
C# 9 da bola sinf override metodida ota sinfdagidan ko'ra aniqroq (aniq bola) turni qaytarish imkoniyatini qo'llang.

## Yechim (C# kodi):
```csharp
using System;

class OziqOvqat { }
class Gosht : OziqOvqat { }

abstract class Yirtqich
{
    public abstract OziqOvqat OziqTop();
}

class Bori : Yirtqich
{
    // C# 9: OziqOvqat o'rniga aniq Gosht qaytarish mumkin!
    public override Gosht OziqTop()
    {
        Console.WriteLine("Bo'ri go'sht topdi.");
        return new Gosht();
    }
}

internal class Program
{
    static void Main()
    {
        Bori b = new Bori();
        Gosht g = b.OziqTop(); // Kasting talab qilinmaydi!
    }
}

```

## Tushuntirish va Mantiq:
Kovariant qaytuvchi turlar (Covariant Returns) C# 9 da qo'shilgan bo'lib, override qilingan metodlarda ota sinf e'lon qilgan turdan ko'ra torroq va aniqroq voris turni qaytarishga ruxsat beradi.

## Ishlash natijasi:
```text
Bo'ri go'sht topdi.
```

# 271-Topshiriq: Konstruktor ichida virtual metod chaqirish xavfi
## Topshiriq sharti:
Ota sinf konstruktorida virtual metod chaqirilganda bola sinf maydonlari hali initsializatsiya qilinmagan bo'lishi xavfini amalda ko'ring.

## Yechim (C# kodi):
```csharp
using System;

class Ota
{
    public Ota()
    {
        Console.WriteLine("Ota konstruktori boshlandi...");
        Init(); // XAVFLI! Hali bola konstruktori ishlamagan!
    }

    public virtual void Init() => Console.WriteLine("Ota Init");
}

class Bola : Ota
{
    private string xabar = "Kutilgan Matn";

    public override void Init()
    {
        // Diqqat! Bu metod chaqirilganda 'xabar' maydoni hali null bo'ladi!
        Console.WriteLine($"Bola Init chaqirildi, xabar: '{(xabar == null ? "NULL!" : xabar)}'");
    }
}

internal class Program
{
    static void Main()
    {
        var b = new Bola();
    }
}

```

## Tushuntirish va Mantiq:
C# da konstruktor ichida virtual metod chaqirish jiddiy anti-pattern hisoblanadi. Ota sinf konstruktori bola sinf maydonlari initsializatsiya qilinishidan oldin ishga tushgani sababli, virtual metod kutilmagan `NullReferenceException` xatolarini keltirib chiqarishi mumkin.

## Ishlash natijasi:
```text
Ota konstruktori boshlandi...
Bola Init chaqirildi, xabar: 'NULL!'
```

# 272-Topshiriq: Shakllar iyerarxiyasi: Yuza va Perimetr polimorfizmi
## Topshiriq sharti:
Geometrik shakllar uchun abstrakt `Yuza` va `Perimetr` metodlarini e'lon qilib, Doira va To'rtburchakda to'liq hisoblang.

## Yechim (C# kodi):
```csharp
using System;

abstract class GeometrikShakl
{
    public abstract double Yuza();
    public abstract double Perimetr();
}

class Aylana : GeometrikShakl
{
    public double R { get; }
    public Aylana(double r) => R = r;

    public override double Yuza() => Math.PI * R * R;
    public override double Perimetr() => 2 * Math.PI * R;
}

class TogriTortburchak : GeometrikShakl
{
    public double A { get; }
    public double B { get; }
    public TogriTortburchak(double a, double b) => (A, B) = (a, b);

    public override double Yuza() => A * B;
    public override double Perimetr() => 2 * (A + B);
}

internal class Program
{
    static void Main()
    {
        GeometrikShakl[] shakllar = [ new Aylana(10), new TogriTortburchak(4, 5) ];

        foreach (var s in shakllar)
        {
            Console.WriteLine($"{s.GetType().Name} -> Yuza: {s.Yuza():F1}, Perimetr: {s.Perimetr():F1}");
        }
    }
}

```

## Tushuntirish va Mantiq:
Ushbu klassik polimorfik model orqali yangi shakllar (Uchburchak, Trapetsiya) tizimga qo'shilganda umumiy hisoblash mantiqiga tegilmaydi.

## Ishlash natijasi:
```text
Aylana -> Yuza: 314.2, Perimetr: 62.8
TogriTortburchak -> Yuza: 20.0, Perimetr: 18.0
```

# 273-Topshiriq: Template Method naqshi: Abstrakt sinfda algoritmlar skeleti
## Topshiriq sharti:
Algoritm bosqichlarini belgilovchi va o'zgaruvchan qadamlarni bolalar sinflariga qoldiruvchi Template Method naqshini yozing.

## Yechim (C# kodi):
```csharp
using System;

abstract class MalumotEksportchi
{
    // Shablon metod (Algoritm skeleti)
    public void EksportQil()
    {
        MalumotniOqish();
        Formatlash();
        Saqlash();
    }

    private void MalumotniOqish() => Console.WriteLine("1. Ma'lumotlar bazadan o'qildi.");
    protected abstract void Formatlash();
    private void Saqlash() => Console.WriteLine("3. Fayl diskka yozildi.
");
}

class JsonEksportchi : MalumotEksportchi
{
    protected override void Formatlash() => Console.WriteLine("2. Ma'lumotlar JSON formatiga o'tkazildi.");
}

class XmlEksportchi : MalumotEksportchi
{
    protected override void Formatlash() => Console.WriteLine("2. Ma'lumotlar XML formatiga o'tkazildi.");
}

internal class Program
{
    static void Main()
    {
        MalumotEksportchi e1 = new JsonEksportchi();
        e1.EksportQil();

        MalumotEksportchi e2 = new XmlEksportchi();
        e2.EksportQil();
    }
}

```

## Tushuntirish va Mantiq:
Template Method naqshi umumiy algoritmlar ketma-ketligini ota sinfda mustahkamlab, faqat o'zgaruvchan qadamlarni (`protected abstract`) bola sinflar ixtiyoriga qoldiradi.

## Ishlash natijasi:
```text
1. Ma'lumotlar bazadan o'qildi.
2. Ma'lumotlar JSON formatiga o'tkazildi.
3. Fayl diskka yozildi.

1. Ma'lumotlar bazadan o'qildi.
2. Ma'lumotlar XML formatiga o'tkazildi.
3. Fayl diskka yozildi.
```

# 274-Topshiriq: Hook metodlari: Ixtiyoriy kengaytirish nuqtalari
## Topshiriq sharti:
Abstrakt sinfda bo'sh `virtual` metod (Hook) qoldirib, xohlovchi bola sinflarga unga ulanish imkonini bering.

## Yechim (C# kodi):
```csharp
using System;

abstract class BazaBuyruq
{
    public void Bajar()
    {
        OldindanTekshir();
        AsosiyAmal();
    }

    protected abstract void AsosiyAmal();

    // Hook metodi - standart holatda bo'sh, bola sinf xohlasa override qiladi
    protected virtual void OldindanTekshir() { }
}

class MaxsusBuyruq : BazaBuyruq
{
    protected override void OldindanTekshir() => Console.WriteLine("Xavfsizlik tekshiruvidan o'tdi.");
    protected override void AsosiyAmal() => Console.WriteLine("Maxsus amal bajarildi.");
}

internal class Program
{
    static void Main()
    {
        var cmd = new MaxsusBuyruq();
        cmd.Bajar();
    }
}

```

## Tushuntirish va Mantiq:
Hook metodlari bolalar sinfiga asosiy oqimga aralashmasdan, ma'lum nuqtalarda qo'shimcha xatti-harakatlar qo'shish (hook in) imkoniyatini taqdim etadi.

## Ishlash natijasi:
```text
Xavfsizlik tekshiruvidan o'tdi.
Maxsus amal bajarildi.
```

# 275-Topshiriq: Merosxo'rlik zanjirida base.ToString() dan foydalanish
## Topshiriq sharti:
Chuqur iyerarxiyada har bir avlod o'z xossalarini ota sinf ma'lumotlariga qo'shib borishini ta'minlang.

## Yechim (C# kodi):
```csharp
using System;

class Jihoz
{
    public string IshlabChiqaruvchi { get; }
    public Jihoz(string brend) => IshlabChiqaruvchi = brend;

    public override string ToString() => $"Brend: {IshlabChiqaruvchi}";
}

class Telefon : Jihoz
{
    public string Model { get; }
    public Telefon(string brend, string model) : base(brend) => Model = model;

    public override string ToString() => $"{base.ToString()}, Model: {Model}";
}

internal class Program
{
    static void Main()
    {
        var tel = new Telefon("Apple", "iPhone 16 Pro");
        Console.WriteLine(tel);
    }
}

```

## Tushuntirish va Mantiq:
`base.ToString()` zanjiri orqali barcha ota sinflarning matnli ifodalari bir-biriga ulanib, to'liq obyekt tasvirini hosil qiladi.

## Ishlash natijasi:
```text
Brend: Apple, Model: iPhone 16 Pro
```

# 276-Topshiriq: Xodimlar iyerarxiyasi: To'liq va shartnoma asosida ishlovchilar
## Topshiriq sharti:
Abstrakt `Xodim` sinfidan `DoimiyXodim` va `ShartnomaAsosidaXodim` sinflarini hosil qilib, oylik maoshni polimorfik hisoblang.

## Yechim (C# kodi):
```csharp
using System;

abstract class Xodim
{
    public string Ism { get; }
    public Xodim(string ism) => Ism = ism;

    public abstract decimal OylikMaosh();
}

class DoimiyXodim : Xodim
{
    private decimal qatiyOylik;
    public DoimiyXodim(string ism, decimal oylik) : base(ism) => qatiyOylik = oylik;

    public override decimal OylikMaosh() => qatiyOylik;
}

class ShartnomaAsosidaXodim : Xodim
{
    private decimal soatlikStavka;
    private int ishlanganSoatlar;

    public ShartnomaAsosidaXodim(string ism, decimal stavka, int soatlar) : base(ism)
    {
        soatlikStavka = stavka;
        ishlanganSoatlar = soatlar;
    }

    public override decimal OylikMaosh() => soatlikStavka * ishlanganSoatlar;
}

internal class Program
{
    static void Main()
    {
        Xodim[] xodimlar = [
            new DoimiyXodim("Aziz", 8000000m),
            new ShartnomaAsosidaXodim("Davron", 100000m, 60)
        ];

        foreach (var x in xodimlar)
        {
            Console.WriteLine($"{x.Ism} maoshi: {x.OylikMaosh():N0} so'm");
        }
    }
}

```

## Tushuntirish va Mantiq:
Polimorfizm har bir xodim turiga o'ziga xos hisob-kitob formulasini kiritish imkonini beradi, tashqi boshqaruv kodi esa faqat `OylikMaosh()` metodini chaqiradi.

## Ishlash natijasi:
```text
Aziz maoshi: 8,000,000 so'm
Davron maoshi: 6,000,000 so'm
```

# 277-Topshiriq: Log yozish tizimi polimorfizmi: Console va File logger
## Topshiriq sharti:
Turli muhitlarga xabarlarni yo'naltiruvchi polimorfik log yozish iyerarxiyasini quring.

## Yechim (C# kodi):
```csharp
using System;

abstract class BazaLogger
{
    public void Log(string xabar)
    {
        string formatlangan = $"[{DateTime.UtcNow:HH:mm:ss}] {xabar}";
        Chiqar(formatlangan);
    }

    protected abstract void Chiqar(string matn);
}

class KonsolLogger : BazaLogger
{
    protected override void Chiqar(string matn) => Console.WriteLine($"[KONSOL]: {matn}");
}

class FaylLogger : BazaLogger
{
    protected override void Chiqar(string matn) => Console.WriteLine($"[FAYLGA YOZILDI]: {matn}");
}

internal class Program
{
    static void Main()
    {
        BazaLogger log1 = new KonsolLogger();
        BazaLogger log2 = new FaylLogger();

        log1.Log("Server ishga tushdi");
        log2.Log("Kritik xato yuz berdi");
    }
}

```

## Tushuntirish va Mantiq:
Umumiy vaqt tamg'asi (timestamp) ota sinfda shakllantiriladi, chiqarish mexanizmi esa merosxo'r sinflarda polimorfik tarzda amalga oshiriladi.

## Ishlash natijasi:
```text
[KONSOL]: [...] Server ishga tushdi
[FAYLGA YOZILDI]: [...] Kritik xato yuz berdi
```

# 278-Topshiriq: Bank to'lov kartalari: Komissiyalar polimorfizmi
## Topshiriq sharti:
Uzcard, Humo va Visa kartalari uchun to'lov o'tkazishda komissiyalarni hisoblovchi sinflarni quring.

## Yechim (C# kodi):
```csharp
using System;

abstract class BankKartasi
{
    public string KartaRaqam { get; }
    public decimal Balans { get; protected set; }

    public BankKartasi(string raqam, decimal balans)
    {
        KartaRaqam = raqam;
        Balans = balans;
    }

    public abstract decimal KomissiyaFoizi { get; }

    public bool TolovQil(decimal summa)
    {
        decimal jami = summa + (summa * KomissiyaFoizi);
        if (Balans >= jami)
        {
            Balans -= jami;
            Console.WriteLine($"{GetType().Name} orqali {summa:N0} so'm to'landi. Komissiya: {summa * KomissiyaFoizi:N0} so'm");
            return true;
        }
        Console.WriteLine($"{GetType().Name}: Mablag' yetarli emas!");
        return false;
    }
}

class Uzcard : BankKartasi
{
    public Uzcard(string r, decimal b) : base(r, b) { }
    public override decimal KomissiyaFoizi => 0.005m; // 0.5%
}

class Visa : BankKartasi
{
    public Visa(string r, decimal b) : base(r, b) { }
    public override decimal KomissiyaFoizi => 0.015m; // 1.5%
}

internal class Program
{
    static void Main()
    {
        BankKartasi k1 = new Uzcard("8600...", 200000m);
        BankKartasi k2 = new Visa("4000...", 200000m);

        k1.TolovQil(100000m);
        k2.TolovQil(100000m);
    }
}

```

## Tushuntirish va Mantiq:
Karta turlari faqat o'zlarining komissiya stavkasini (`KomissiyaFoizi`) belgilaydi, yagona to'lov mantiqi esa ota sinfda xavfsiz boshqariladi.

## Ishlash natijasi:
```text
Uzcard orqali 100,000 so'm to'landi. Komissiya: 500 so'm
Visa orqali 100,000 so'm to'landi. Komissiya: 1,500 so'm
```

# 279-Topshiriq: O'yin qahramonlari iyerarxiyasi: Jangchi, Sehrgar va Kamonchi
## Topshiriq sharti:
O'yin qahramonlarining turlicha hujum qilishini polimorfik metodlar orqali modellashtiring.

## Yechim (C# kodi):
```csharp
using System;

abstract class Qahramon
{
    public string Ism { get; }
    public Qahramon(string ism) => Ism = ism;

    public abstract void HujumQil();
}

class Jangchi : Qahramon
{
    public Jangchi(string ism) : base(ism) { }
    public override void HujumQil() => Console.WriteLine($"{Ism} qilich bilan qattiq zarba berdi! (Zarar: 50)");
}

class Sehrgar : Qahramon
{
    public Sehrgar(string ism) : base(ism) { }
    public override void HujumQil() => Console.WriteLine($"{Ism} olovli shar (Fireball) otdi! (Zarar: 80)");
}

internal class Program
{
    static void Main()
    {
        Qahramon[] otryad = [ new Jangchi("Artur"), new Sehrgar("Gandalf") ];

        foreach (var q in otryad)
        {
            q.HujumQil();
        }
    }
}

```

## Tushuntirish va Mantiq:
O'yin dvigatellarida har bir qahramon va yirtqich `Qahramon` sinfidan o'sib chiqadi. Dvigatel barcha obyektlarni bitta massivda aylanib ularning `HujumQil()` metodini chaqiradi.

## Ishlash natijasi:
```text
Artur qilich bilan qattiq zarba berdi! (Zarar: 50)
Gandalf olovli shar (Fireball) otdi! (Zarar: 80)
```

# 280-Topshiriq: Bildirishnomalar tizimi: SMS, Email va Push
## Topshiriq sharti:
Foydalanuvchilarga xabar jo'natish xizmatlarini yagona ota sinf ostida umumlashtiring.

## Yechim (C# kodi):
```csharp
using System;

abstract class Bildirishnoma
{
    public abstract void Yubor(string manzil, string xabar);
}

class SmsBildirishnoma : Bildirishnoma
{
    public override void Yubor(string telefon, string xabar) =>
        Console.WriteLine($"[SMS -> {telefon}]: {xabar}");
}

class EmailBildirishnoma : Bildirishnoma
{
    public override void Yubor(string email, string xabar) =>
        Console.WriteLine($"[EMAIL -> {email}]: {xabar}");
}

internal class Program
{
    static void Main()
    {
        Bildirishnoma xabarYuboruvchi = new SmsBildirishnoma();
        xabarYuboruvchi.Yubor("+998901234567", "Sizning tasdiqlash kodingiz: 4921");

        xabarYuboruvchi = new EmailBildirishnoma();
        xabarYuboruvchi.Yubor("user@uz", "Hush kelibsiz!");
    }
}

```

## Tushuntirish va Mantiq:
Xabar yetkazish kanallari osongina yangi turlar bilan (Telegram, WebPush) kengaytirilishi mumkin, chunki asosiy dastur faqat `Bildirishnoma` bilan ishlaydi.

## Ishlash natijasi:
```text
[SMS -> +998901234567]: Sizning tasdiqlash kodingiz: 4921
[EMAIL -> user@uz]: Hush kelibsiz!
```

# 281-Topshiriq: UI elementlar iyerarxiyasi: Tugma va Matn maydoni
## Topshiriq sharti:
Grafik foydalanuvchi interfeysi (GUI) elementlarining ekranga chizilishini polimorfik quring.

## Yechim (C# kodi):
```csharp
using System;

abstract class BoshqaruvElementi
{
    public int X { get; set; }
    public int Y { get; set; }

    public abstract void Render();
}

class Tugma : BoshqaruvElementi
{
    public string Matn { get; set; } = "OK";
    public override void Render() => Console.WriteLine($"Tugma [{Matn}] ({X}, {Y}) koordinatada chizildi.");
}

class MatnMaydoni : BoshqaruvElementi
{
    public string Matn { get; set; } = "";
    public override void Render() => Console.WriteLine($"MatnMaydoni: '{Matn}' ({X}, {Y}) koordinatada chizildi.");
}

internal class Program
{
    static void Main()
    {
        BoshqaruvElementi[] oyna = [
            new Tugma { X = 10, Y = 20, Matn = "Yuborish" },
            new MatnMaydoni { X = 10, Y = 50, Matn = "Ismingizni kiriting" }
        ];

        foreach (var element in oyna)
        {
            element.Render();
        }
    }
}

```

## Tushuntirish va Mantiq:
GUI freymvorklari (WPF, WinForms, Avalonia) barcha vizual elementlarni `UIElement` yoki `Control` asosiy sinfidan meros olib quradi.

## Ishlash natijasi:
```text
Tugma [Yuborish] (10, 20) koordinatada chizildi.
MatnMaydoni: 'Ismingizni kiriting' (10, 50) koordinatada chizildi.
```

# 282-Topshiriq: Konstruktorlar va Destruktorlarning bajarilish ketma-ketligi
## Topshiriq sharti:
Ko'p pog'onali merosda konstruktorlar va destruktorlar qaysi tartibda chaqirilishini isbotlang.

## Yechim (C# kodi):
```csharp
using System;

class B bobo
{
    public B bobo() => Console.WriteLine("1. Bobo konstruktori");
    ~B bobo() => Console.WriteLine("6. Bobo destruktori");
}

class Ota : B bobo
{
    public Ota() => Console.WriteLine("2. Ota konstruktori");
    ~Ota() => Console.WriteLine("5. Ota destruktori");
}

class Bola : Ota
{
    public Bola() => Console.WriteLine("3. Bola konstruktori");
    ~Bola() => Console.WriteLine("4. Bola destruktori");
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Obyekt yaratilmoqda:");
        new Bola();
        Console.WriteLine("Obyekt yaratildi.");
    }
}

```

## Tushuntirish va Mantiq:
Konstruktorlar iyerarxiya bo'yicha eng yuqori ajdoddan boshlab pastga qarab ishlaydi (Bobo -> Ota -> Bola). Destruktorlar esa aksincha, eng pastki avloddan boshlab yuqoriga qarab chaqiriladi (Bola -> Ota -> Bobo).

## Ishlash natijasi:
```text
Obyekt yaratilmoqda:
1. Bobo konstruktori
2. Ota konstruktori
3. Bola konstruktori
Obyekt yaratildi.
```

# 283-Topshiriq: Olmos muammosi (Diamond Problem) va C# dagi cheklov
## Topshiriq sharti:
C# nima uchun bir vaqtning o'zida ikkita sinfdan meros olishni taqiqlashini tushuntiring.

## Yechim (C# kodi):
```csharp
using System;

// C# da quyidagicha kod YOZIB BO'LMAYDI:
// class A { public virtual void Metod() { } }
// class B : A { public override void Metod() => Console.WriteLine("B"); }
// class C : A { public override void Metod() => Console.WriteLine("C"); }
// class D : B, C { } // OLMOST MUAMMOSI! D qaysi Metod() ni olishi kerak? B ni mi yoki C ni?

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Olmos muammosi sababli C# da ko'p sinfli merosxo'rlik taqiqlangan.");
        Console.WriteLine("Buning o'rniga C# bitta ota sinf va istalgancha interfeyslarni qo'llab-quvvatlaydi.");
    }
}

```

## Tushuntirish va Mantiq:
Olmos muammosi (Diamond Problem) bir xil ota sinfga ega ikkita sinfdan uchinchi sinf meros olganda qaysi metod ustun kelishi noaniq bo'lib qolishidir. C# bu muammoni bitta sinfli merosxo'rlik orqali bartaraf etgan.

## Ishlash natijasi:
```text
Olmos muammosi sababli C# da ko'p sinfli merosxo'rlik taqiqlangan.
Buning o'rniga C# bitta ota sinf va istalgancha interfeyslarni qo'llab-quvvatlaydi.
```

# 284-Topshiriq: Kompozitsiyani merosxo'rlikdan ustun qo'yish (Composition over Inheritance)
## Topshiriq sharti:
Merosxo'rlik o'rniga kompozitsiya (has-a) yordamida yanada moslashuvchan tizim quring.

## Yechim (C# kodi):
```csharp
using System;

class Dvigatel
{
    public void Start() => Console.WriteLine("Dvigatel o't oldi.");
}

// Yomon usul: class Mashina : Dvigatel (Mashina dvigatel emas, unda dvigatel bor)
// To'g'ri usul (Kompozitsiya):
class Mashina
{
    private readonly Dvigatel dvigatel = new();

    public void Haydash()
    {
        dvigatel.Start();
        Console.WriteLine("Mashina harakatlanmoqda.");
    }
}

internal class Program
{
    static void Main()
    {
        var m = new Mashina();
        m.Haydash();
    }
}

```

## Tushuntirish va Mantiq:
'Is-A' munosabati aniq bo'lmaganda meros olish sinflar orasida juda qattiq bog'liqlik (tight coupling) keltirib chiqaradi. Kompozitsiya esa qismlarni mustaqil o'zgartirish va almashtirish imkonini beradi.

## Ishlash natijasi:
```text
Dvigatel o't oldi.
Mashina harakatlanmoqda.
```

# 285-Topshiriq: Merosxo'rlikda shaxsiy (private) maydonlar mavjudligi
## Topshiriq sharti:
Ota sinfning `private` maydoni bola sinf xotirasida mavjud bo'lsa-da, bevosita ko'rinmasligini isbotlang.

## Yechim (C# kodi):
```csharp
using System;

class Ota
{
    private int maxfiyKod = 12345;

    public int MaxfiyKodniOlish() => maxfiyKod; // Ochiq metod orqali kirish
}

class Bola : Ota
{
    public void Sinov()
    {
        // Console.WriteLine(maxfiyKod); // XATO! Bola sinfga bevosita ko'rinmaydi
        Console.WriteLine($"Ota orqali olindi: {MaxfiyKodniOlish()}");
    }
}

internal class Program
{
    static void Main()
    {
        var b = new Bola();
        b.Sinov();
    }
}

```

## Tushuntirish va Mantiq:
Obyekt Heap da yaratilganda ota sinfning barcha maydonlari (shu jumladan `private` lar ham) xotirada joy oladi. Ammo C# kompilyatori bola sinf kodidan turib ularga to'g'ridan-to'g'ri kirishni taqiqlaydi.

## Ishlash natijasi:
```text
Ota orqali olindi: 12345
```

# 286-Topshiriq: Devirtualizatsiya va sealed sinflar tezligi
## Topshiriq sharti:
`sealed` sinflarda virtual chaqiruv to'g'ridan-to'g'ri chaqiruvga aylanishi tamoyilini tushuntiring.

## Yechim (C# kodi):
```csharp
using System;

class Asosiy
{
    public virtual void Harakat() => Console.WriteLine("Baza");
}

sealed class Yakuniy : Asosiy
{
    public override void Harakat() => Console.WriteLine("Yakuniy harakat");
}

internal class Program
{
    static void Main()
    {
        Yakuniy obj = new Yakuniy();

        // JIT biladiki Yakuniy dan boshqa hech kim meros ololmaydi
        // Shuning uchun vtable qidirmaydi, to'g'ridan-to'g'ri 'call' chaqiradi (Devirtualization)
        obj.Harakat();

        Console.WriteLine("JIT Devirtualization orqali vtable indirektsiyasi bartaraf etildi.");
    }
}

```

## Tushuntirish va Mantiq:
Devirtualization .NET JIT optimallashuvi bo'lib, agar sinf yoki metod `sealed` bo'lsa, kompilyator virtual metodlar jadvalini chetlab o'tib, to'g'ridan-to'g'ri tezkor protsessor chaqiruvini hosil qiladi.

## Ishlash natijasi:
```text
Yakuniy harakat
JIT Devirtualization orqali vtable indirektsiyasi bartaraf etildi.
```

# 287-Topshiriq: Polimorfik klonlash (Virtual Clone Metodi)
## Topshiriq sharti:
Ota sinf havolasi orqali uning asl turiga mos nusxasini yaratuvchi virtual `Klonla()` metodini yozing.

## Yechim (C# kodi):
```csharp
using System;

abstract class Hujjat
{
    public string Sarlavha { get; set; } = "";
    public abstract Hujjat Klonla();
}

class Hisobot : Hujjat
{
    public int Sahifalar { get; set; }

    public override Hisobot Klonla() // Kovariant qaytuvchi tur
    {
        return new Hisobot { Sarlavha = this.Sarlavha, Sahifalar = this.Sahifalar };
    }
}

internal class Program
{
    static void Main()
    {
        Hujjat h1 = new Hisobot { Sarlavha = "Moliya", Sahifalar = 12 };
        Hujjat h2 = h1.Klonla();

        Console.WriteLine($"Klonlangan hujjat: {h2.Sarlavha}, turi: {h2.GetType().Name}");
        Console.WriteLine($"Bitta xotira manzilidami: {object.ReferenceEquals(h1, h2)}");
    }
}

```

## Tushuntirish va Mantiq:
Standart `ICloneable` faqat `object` qaytaradi va kasting talab qiladi. Virtual `Klonla()` metodi esa aniq turdagi nusxani xavfsiz va polimorfik qaytarish imkonini beradi.

## Ishlash natijasi:
```text
Klonlangan hujjat: Moliya, turi: Hisobot
Bitta xotira manzilidami: False
```

# 288-Topshiriq: Fragile Base Class (Mo'rt Ota Sinf) muammosi
## Topshiriq sharti:
Ota sinfdagi o'zgarishlar barcha vorislar kodini buzib yuborishi xavfini tahlil qiling.

## Yechim (C# kodi):
```csharp
using System;

class BazaTo'plam
{
    public virtual void Qo'sh(int x) => Console.WriteLine($"Element qo'shildi: {x}");

    public virtual void Ko'pQo'sh(int[] massiv)
    {
        // Agar ota sinf ichida har bir element uchun 'Qo'sh(x)' chaqirilsa,
        // va bola sinf ikkala metodni ham override qilgan bo'lsa, elementlar 2 marta sanalib qolishi mumkin!
        foreach (var i in massiv) Qo'sh(i);
    }
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Mo'rt ota sinf muammosi: chuqur meros iyerarxiyasida ichki chaqiruvlar vorislarni kutilmagan holatga solishi mumkin.");
    }
}

```

## Tushuntirish va Mantiq:
Fragile Base Class muammosi ota sinfdagi ichki implementatsiya o'zgarishi vorislar faoliyatiga kutilmagan ta'sir ko'rsatganda yuzaga keladi. Shu sababli zamonaviy arxitekturada merosxo'rlik faqat qat'iy zarur bo'lgandagina qo'llaniladi.

## Ishlash natijasi:
```text
Mo'rt ota sinf muammosi: chuqur meros iyerarxiyasida ichki chaqiruvlar vorislarni kutilmagan holatga solishi mumkin.
```

# 289-Topshiriq: Abstract sinf konstruktorining maqsadi
## Topshiriq sharti:
Abstrakt sinfdan obyekt olib bo'lmasa-da, uning konstruktori nima uchun kerakligini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

abstract class Foydalanuvchi
{
    public Guid Id { get; }
    public DateTime YaratilganSana { get; }

    // Abstrakt sinf konstruktori
    protected Foydalanuvchi()
    {
        Id = Guid.NewGuid();
        YaratilganSana = DateTime.UtcNow;
    }
}

class Admin : Foydalanuvchi
{
    public string Huquq { get; set; } = "Full";
}

internal class Program
{
    static void Main()
    {
        var admin = new Admin();
        Console.WriteLine($"Admin Id uzunligi: {admin.Id.ToString().Length}");
        Console.WriteLine($"Yaratilgan sana yili: {admin.YaratilganSana.Year}");
    }
}

```

## Tushuntirish va Mantiq:
Abstrakt sinf konstruktori barcha bolalar sinflari uchun umumiy bo'lgan maydonlarni initsializatsiya qilish uchun xizmat qiladi va har bir voris sinf yaratilishida avtomatik chaqiriladi.

## Ishlash natijasi:
```text
Admin Id uzunligi: 36
Yaratilgan sana yili: 2026
```

# 290-Topshiriq: Polimorfik hisobot generatori (ReportGenerator)
## Topshiriq sharti:
PDF va Excel hisobotlarini umumiy shablon asosida shakllantiruvchi tizim quring.

## Yechim (C# kodi):
```csharp
using System;

abstract class HisobotGenerator
{
    public void Yarat()
    {
        SarlavhaYoz();
        JadvalYoz();
        YakunYoz();
    }

    protected abstract void SarlavhaYoz();
    protected abstract void JadvalYoz();
    protected virtual void YakunYoz() => Console.WriteLine("--- Hisobot yakunlandi ---");
}

class PdfHisobot : HisobotGenerator
{
    protected override void SarlavhaYoz() => Console.WriteLine("[PDF]: Sarlavha chizildi");
    protected override void JadvalYoz() => Console.WriteLine("[PDF]: Jadval katakchalari joylandi");
}

internal class Program
{
    static void Main()
    {
        HisobotGenerator gen = new PdfHisobot();
        gen.Yarat();
    }
}

```

## Tushuntirish va Mantiq:
Hisobot generatorlarida barcha hisobot turlarining qadamlari bir xil bo'ladi, lekin ularning faylga chizish formatlari turlicha bo'ladi.

## Ishlash natijasi:
```text
[PDF]: Sarlavha chizildi
[PDF]: Jadval katakchalari joylandi
--- Hisobot yakunlandi ---
```

# 291-Topshiriq: Merosxo'rlikda keshlashtirilgan polimorfik hisoblash tizimi
## Topshiriq sharti:
Murakkab hisob-kitoblarni faqat bir marta hisoblab keshda saqlovchi ota sinf tuzing.

## Yechim (C# kodi):
```csharp
using System;

abstract class KeshliHisoblagich
{
    private decimal? kesh;

    public decimal Natija()
    {
        kesh ??= QimmatliHisob();
        return kesh.Value;
    }

    protected abstract decimal QimmatliHisob();
}

class SoliqHisoblagich : KeshliHisoblagich
{
    protected override decimal QimmatliHisob()
    {
        Console.WriteLine(">> Og'ir soliq hisobi bajarildi!");
        return 1200000m;
    }
}

internal class Program
{
    static void Main()
    {
        var s = new SoliqHisoblagich();
        Console.WriteLine($"1-chaqiruv: {s.Natija()} so'm");
        Console.WriteLine($"2-chaqiruv: {s.Natija()} so'm (Keshdan olinadi)");
    }
}

```

## Tushuntirish va Mantiq:
Kesh mantiqi ota sinfda bitta joyda turadi, bola sinf esa faqat hisoblash formulasini taqdim etadi.

## Ishlash natijasi:
```text
>> Og'ir soliq hisobi bajarildi!
1-chaqiruv: 1200000 so'm
2-chaqiruv: 1200000 so'm (Keshdan olinadi)
```

# 292-Topshiriq: Polimorfizm va Switch Expression birgalikda
## Topshiriq sharti:
Polimorfik sinflarni pattern matching orqali qo'shimcha xususiyatlariga qarab tahlil qiling.

## Yechim (C# kodi):
```csharp
using System;

abstract class Tranzaksiya { public decimal Summa { get; set; } }
class NaqdTranzaksiya : Tranzaksiya { }
class OnlineTranzaksiya : Tranzaksiya { public string Provayder { get; set; } = "Payme"; }

internal class Program
{
    static string Tekshir(Tranzaksiya t) => t switch
    {
        OnlineTranzaksiya { Provayder: "Payme" } o => $"Payme orqali: {o.Summa:N0} so'm",
        OnlineTranzaksiya o                        => $"Boshqa online ({o.Provayder}): {o.Summa:N0} so'm",
        NaqdTranzaksiya n                          => $"Naqd to'lov: {n.Summa:N0} so'm",
        _                                          => "Noma'lum to'lov"
    };

    static void Main()
    {
        Console.WriteLine(Tekshir(new OnlineTranzaksiya { Summa = 50000, Provayder = "Payme" }));
        Console.WriteLine(Tekshir(new NaqdTranzaksiya { Summa = 20000 }));
    }
}

```

## Tushuntirish va Mantiq:
Klassik virtual metodlar bilan bir qatorda, zamonaviy C# pattern matching polimorfik obyektlarni ularning turi va ichki xossalariga qarab tahlil qilish imkonini beradi.

## Ishlash natijasi:
```text
Payme orqali: 50,000 so'm
Naqd to'lov: 20,000 so'm
```

# 293-Topshiriq: Sealed sinflar orqali xavfsizlik va o'zgarmaslik
## Topshiriq sharti:
Tizimning kritik avtorizatsiya tokenini saqlovchi sinfni `sealed` qilib himoyalang.

## Yechim (C# kodi):
```csharp
using System;

public sealed class XavfsizToken
{
    public string Qiymat { get; }
    public XavfsizToken(string token) => Qiymat = token;
}

internal class Program
{
    static void Main()
    {
        var token = new XavfsizToken("jwt_secret_xyz");
        Console.WriteLine($"Token uzunligi: {token.Qiymat.Length}");
    }
}

```

## Tushuntirish va Mantiq:
`sealed` sinflardan g'arazli maqsadlarda meros olib, uning xatti-harakatlarini buzish (masalan parollarni o'g'irlash) imkonsizdir.

## Ishlash natijasi:
```text
Token uzunligi: 14
```

# 294-Topshiriq: Merosxo'rlikda a'zolarning kirish darajasini o'zgartirib bo'lmasligi
## Topshiriq sharti:
Override qilinayotgan metod kirish modifikatori (`public`, `protected`) ota sinfdagi bilan bir xil bo'lishi shartligini tushuntiring.

## Yechim (C# kodi):
```csharp
using System;

class Asosiy
{
    public virtual void OchiqMetod() => Console.WriteLine("Ochiq");
}

class Voris : Asosiy
{
    // private override void OchiqMetod() { } // KOMPILYATSIYA XATOSI! Kirish darajasini toraytirib bo'lmaydi
    public override void OchiqMetod() => Console.WriteLine("Vorisda ham public");
}

internal class Program
{
    static void Main()
    {
        Asosiy a = new Voris();
        a.OchiqMetod();
    }
}

```

## Tushuntirish va Mantiq:
Polimorfizm qoidasiga binoan ota sinf orqali chaqirilishi mumkin bo'lgan metod bola sinfda toraytirilishi (masalan `private` qilinishi) mumkin emas, aks holda bu polimorfik shartnomani buzadi.

## Ishlash natijasi:
```text
Vorisda ham public
```

# 295-Topshiriq: Domen modeli: Chegirmalar polimorfizmi (Discount hierarchy)
## Topshiriq sharti:
Foizli va qat'iy summali chegirmalarni hisoblovchi polimorfik chegirma mexanizmini yarating.

## Yechim (C# kodi):
```csharp
using System;

abstract class Chegirma
{
    public abstract decimal Qollash(decimal narx);
}

class FoizliChegirma(decimal foiz) : Chegirma
{
    public override decimal Qollash(decimal narx) => narx - (narx * foiz / 100m);
}

class Qat'iyChegirma(decimal summa) : Chegirma
{
    public override decimal Qollash(decimal narx) => Math.Max(0m, narx - summa);
}

internal class Program
{
    static void Main()
    {
        decimal narx = 500000m;
        Chegirma ch1 = new FoizliChegirma(10); // 10%
        Chegirma ch2 = new Qat'iyChegirma(80000); // 80 ming so'm

        Console.WriteLine($"10% chegirmadan keyin: {ch1.Qollash(narx):N0} so'm");
        Console.WriteLine($"80 ming chegirmadan keyin: {ch2.Qollash(narx):N0} so'm");
    }
}

```

## Tushuntirish va Mantiq:
Ushbu yechim savdo tizimlariga yangi chegirma turlarini (masalan, '1 ta olganga 1 ta bepul') oson qo'shish imkonini beradi.

## Ishlash natijasi:
```text
10% chegirmadan keyin: 450,000 so'm
80 ming chegirmadan keyin: 420,000 so'm
```

# 296-Topshiriq: Merosxo'rlik zanjirida avlodlar sonini tekshirish
## Topshiriq sharti:
Obyektning ota sinflar zanjirini Reflection orqali aniqlang.

## Yechim (C# kodi):
```csharp
using System;

class A { }
class B : A { }
class C : B { }

internal class Program
{
    static void Main()
    {
        Type? joriy = typeof(C);

        Console.Write("Meros iyerarxiyasi: ");
        while (joriy != null)
        {
            Console.Write($"{joriy.Name} -> ");
            joriy = joriy.BaseType;
        }
        Console.WriteLine("null");
    }
}

```

## Tushuntirish va Mantiq:
C# dagi har qanday sinf oxir-oqibat `System.Object` ga borib taqaladi. `BaseType` orqali meros zanjirining barcha ota sinflarini ketma-ket ko'rish mumkin.

## Ishlash natijasi:
```text
Meros iyerarxiyasi: C -> B -> A -> Object -> null
```

# 297-Topshiriq: Polimorfizm va Dependency Inversion tayyorgarligi
## Topshiriq sharti:
Yuqori darajadagi modul aniq amalga oshirishga emas, abstraksiyaga tayanishini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

abstract class Ma'lumotSaqlagich
{
    public abstract void Saqla(string ma'lumot);
}

class SqlSaqlagich : Ma'lumotSaqlagich
{
    public override void Saqla(string ma'lumot) => Console.WriteLine($"SQL bazaga yozildi: {ma'lumot}");
}

class BuyurtmaXizmati
{
    private readonly Ma'lumotSaqlagich saqlagich;
    public BuyurtmaXizmati(Ma'lumotSaqlagich s) => saqlagich = s;

    public void YangiBuyurtma(string buyurtma) => saqlagich.Saqla(buyurtma);
}

internal class Program
{
    static void Main()
    {
        var xizmat = new BuyurtmaXizmati(new SqlSaqlagich());
        xizmat.YangiBuyurtma("№5041");
    }
}

```

## Tushuntirish va Mantiq:
Dependency Inversion tamoyili (SOLID ning 'D' harfi) yuqori qatlamlarni pastki qatlam detallaridan ajratishda aynan abstrakt sinflar va polimorfizmga tayanadi.

## Ishlash natijasi:
```text
SQL bazaga yozildi: №5041
```

# 298-Topshiriq: Polimorfizmda Null Object naqshi
## Topshiriq sharti:
`null` tekshiruvlaridan qutulish uchun bo'sh harakatli merosxo'r sinf (Null Object) yarating.

## Yechim (C# kodi):
```csharp
using System;

abstract class XabarBeruvchi
{
    public abstract void Xabar(string matn);
}

class RealXabarBeruvchi : XabarBeruvchi
{
    public override void Xabar(string matn) => Console.WriteLine($"[XABAR]: {matn}");
}

// Bo'sh obyekt (Null Object)
class HechNarsaQilmaydiganXabarBeruvchi : XabarBeruvchi
{
    public override void Xabar(string matn) { /* Hech narsa qilmaydi */ }
}

internal class Program
{
    static void Main()
    {
        XabarBeruvchi logger = new HechNarsaQilmaydiganXabarBeruvchi();

        // null tekshirish shart emas: if (logger != null) ...
        logger.Xabar("Bu xabar hech qayerga chiqmaydi");

        Console.WriteLine("Null Object xavfsiz ishladi.");
    }
}

```

## Tushuntirish va Mantiq:
Null Object Pattern dastur kodida har qadamda `if (x != null)` yozishdan xalos etadi va polimorfik tarzda bo'sh xatti-harakatni taqdim etadi.

## Ishlash natijasi:
```text
Null Object xavfsiz ishladi.
```

# 299-Topshiriq: Interfeys vs Abstrakt sinf: Asosiy farqlar
## Topshiriq sharti:
Abstrakt sinf (holat/maydon saqlay oladi) va Interfeys (faqat shartnoma) farqini namoyish eting.

## Yechim (C# kodi):
```csharp
using System;

abstract class BazaKompaniya
{
    // Abstrakt sinf maydon saqlay oladi
    protected string KompaniyaNomi = "O'zbekiston IT";
    public abstract void Faoliyat();
}

interface IXizmat
{
    void XizmatKorsat();
}

class ITKompaniya : BazaKompaniya, IXizmat
{
    public override void Faoliyat() => Console.WriteLine($"{KompaniyaNomi}: Dasturiy ta'minot yaratish.");
    public void XizmatKorsat() => Console.WriteLine("Xizmat ko'rsatildi.");
}

internal class Program
{
    static void Main()
    {
        var it = new ITKompaniya();
        it.Faoliyat();
        it.XizmatKorsat();
    }
}

```

## Tushuntirish va Mantiq:
Abstrakt sinf meros zanjirida ('kimdir nimanidir ifodalaydi' - IS-A) holat va umumiy kodni bo'lishish uchun ishlatiladi. Interfeys esa sinfning qobiliyatlarini ('nima qila olishi' - CAN-DO) belgilaydi.

## Ishlash natijasi:
```text
O'zbekiston IT: Dasturiy ta'minot yaratish.
Xizmat ko'rsatildi.
```

# 300-Topshiriq: Merosxo'rlik va Polimorfizm bo'limi integratsiyalashgan arxitekturasi
## Topshiriq sharti:
Barcha tamoyillarni (abstract, virtual, override, sealed, base, polimorfizm) o'zida jamlagan professional to'lov tizimini yakunlang.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

abstract class TolovTizimi
{
    public string Nomi { get; }
    protected TolovTizimi(string nomi) => Nomi = nomi;

    public void Bajar(decimal summa)
    {
        Console.WriteLine($"--- {Nomi} tizimi ishga tushdi ---");
        if (Tekshir(summa))
        {
            AmalgaOshir(summa);
            Kvitansiya(summa);
        }
    }

    protected virtual bool Tekshir(decimal summa) => summa > 0;
    protected abstract void AmalgaOshir(decimal summa);
    private void Kvitansiya(decimal summa) => Console.WriteLine($"Kvitansiya: {summa:N0} so'm muvaffaqiyatli o'tkazildi.
");
}

sealed class PaymeTizimi : TolovTizimi
{
    public PaymeTizimi() : base("Payme") { }
    protected override void AmalgaOshir(decimal summa) => Console.WriteLine($"Payme API orqali {summa:N0} so'm yechildi.");
}

sealed class ClickTizimi : TolovTizimi
{
    public ClickTizimi() : base("Click") { }
    protected override void AmalgaOshir(decimal summa) => Console.WriteLine($"Click USSD/API orqali {summa:N0} so'm yechildi.");
}

internal class Program
{
    static void Main()
    {
        List<TolovTizimi> provayderlar = [ new PaymeTizimi(), new ClickTizimi() ];

        foreach (var p in provayderlar)
        {
            p.Bajar(250000m);
        }
    }
}

```

## Tushuntirish va Mantiq:
Ushbu integratsiyalashgan tizimda Template Method, abstrakt va virtual metodlar, muhrlangan (`sealed`) terminal sinflar va polimorfik to'plamlar mukammal birlashgan.

## Ishlash natijasi:
```text
--- Payme tizimi ishga tushdi ---
Payme API orqali 250,000 so'm yechildi.
Kvitansiya: 250,000 so'm muvaffaqiyatli o'tkazildi.

--- Click tizimi ishga tushdi ---
Click USSD/API orqali 250,000 so'm yechildi.
Kvitansiya: 250,000 so'm muvaffaqiyatli o'tkazildi.
```

