# 9-Mavzu: Xatoliklar va Istisnolar (Exception Handling) (401-450)

Ushbu bo'limda C# dasturlarida barqarorlik va ishonchlilikni ta'minlash: `try-catch-finally` bloklari, standart CLR istisnolari, `throw` va `throw;` farqlari, istisno filtrlari (`when`), `IDisposable` va `using` bayonotlari, `IAsyncDisposable` va `await using`, `AggregateException`, Tester-Doer va Result patternlari, maxsus (Custom) domen istisnolari hamda xotirani xavfsiz tozalash bo'yicha 50 ta amaliy topshiriq jamlangan.

# 401-Topshiriq: try, catch va finally bloklarining asosiy tuzilishi
## Topshiriq sharti:
Nolga bo'lish xatoligini (`DivideByZeroException`) xavfsiz ushlab, `finally` blokining har qanday holatda ishlashini namoyish eting.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        try
        {
            Console.WriteLine("1. try bloki boshlandi");
            int a = 10;
            int b = 0;
            int natija = a / b; // Nolga bo'lish xatosi
            Console.WriteLine($"Natija: {natija}");
        }
        catch (DivideByZeroException ex)
        {
            Console.WriteLine($"2. catch bloki: Nolga bo'lish taqiqlandi! ({ex.Message})");
        }
        finally
        {
            Console.WriteLine("3. finally bloki: Har doim kafolatli bajariladi.");
        }

        Console.WriteLine("4. Dastur qulamasdan davom etmoqda.");
    }
}

```

## Tushuntirish va Mantiq:
`try` bloki xatolik chiqishi mumkin bo'lgan kodni o'rab oladi. Agar istisno (Exception) yuz bersa, ijro darhol to'xtab mos `catch` blokiga o'tadi. `finally` bloki esa xatolik bo'lishi yoki bo'lmasligidan qat'i nazar har doim ishga tushadi.

## Ishlash natijasi:
```text
1. try bloki boshlandi
2. catch bloki: Nolga bo'lish taqiqlandi! (Attempted to divide by zero.)
3. finally bloki: Har doim kafolatli bajariladi.
4. Dastur qulamasdan davom etmoqda.
```

# 402-Topshiriq: Ko'p pog'onali catch bloklari va aniqlik (Specificity) qoidasi
## Topshiriq sharti:
Bir nechta `catch` bloklarini to'g'ri tartibda (kichik aniq istisnolar avval, umumiy `Exception` oxirida) joylashtiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Tekshir(string? matn, int indeks)
    {
        try
        {
            ArgumentNullException.ThrowIfNull(matn);
            char c = matn[indeks];
            Console.WriteLine($"Belgi: {c}");
        }
        catch (ArgumentNullException ex)
        {
            Console.WriteLine($"Aniq xato 1: Matn null bo'lishi mumkin emas ({ex.ParamName})");
        }
        catch (IndexOutOfRangeException)
        {
            Console.WriteLine("Aniq xato 2: Indeks matn chegarasidan tashqarida!");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Umumiy zaxira xato: {ex.Message}");
        }
    }

    static void Main()
    {
        Tekshir(null, 0);
        Tekshir("Salom", 10);
        Tekshir("Salom", 1);
    }
}

```

## Tushuntirish va Mantiq:
CLR mos `catch` blokini yuqoridan pastga qarab qidiradi va birinchi mos kelganida to'xtaydi. Shuning uchun aniq istisnolar (`ArgumentNullException`) yuqorida, umumiy ota `Exception` esa eng pastda bo'lishi shart.

## Ishlash natijasi:
```text
Aniq xato 1: Matn null bo'lishi mumkin emas (matn)
Aniq xato 2: Indeks matn chegarasidan tashqarida!
Belgi: a
```

# 403-Topshiriq: System.Exception asosiy xossalari: Message, StackTrace va TargetSite
## Topshiriq sharti:
Istisno obyekti ichidagi diagnostika ma'lumotlarini konsolga chiqaring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void XatolikMetodi()
    {
        throw new InvalidOperationException("Amaliyot joriy holatda bajarilishi mumkin emas!");
    }

    static void Main()
    {
        try
        {
            XatolikMetodi();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Turi:       {ex.GetType().FullName}");
            Console.WriteLine($"Xabar:      {ex.Message}");
            Console.WriteLine($"Metod:      {ex.TargetSite?.Name}");
            Console.WriteLine($"StackTrace: mavjud ({ex.StackTrace?.Length > 0})");
        }
    }
}

```

## Tushuntirish va Mantiq:
`Message` xatoning inson tushunadigan sababi, `StackTrace` chaqiruvlar zanjiri (qaysi fayl, qaysi qatorda ro'y bergani), `TargetSite` esa aynan qaysi metodda istisno otilganini ko'rsatadi.

## Ishlash natijasi:
```text
Turi:       System.InvalidOperationException
Xabar:      Amaliyot joriy holatda bajarilishi mumkin emas!
Metod:      XatolikMetodi
StackTrace: mavjud (True)
```

# 404-Topshiriq: throw; vs throw ex; o'rtasidagi StackTrace saqlanish farqi
## Topshiriq sharti:
`throw ex;` xatolik kelib chiqqan joy tarixini o'chirib yuborishi, `throw;` esa asl joyni saqlab qolishini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void QuyiMetod()
    {
        int nol = 0;
        int x = 10 / nol; // Haqiqiy xato shu yerda yuz berdi (10-qator)
    }

    static void OraliqMetod()
    {
        try
        {
            QuyiMetod();
        }
        catch (Exception)
        {
            // TO'G'RI: 'throw;' asl StackTrace ni to'liq saqlab qoladi!
            // NOTO'G'RI: 'throw ex;' StackTrace ni shu yerdan boshlab qayta yozadi va asl sababni yashiradi.
            throw;
        }
    }

    static void Main()
    {
        try
        {
            OraliqMetod();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"StackTrace ichida 'QuyiMetod' bormi: {ex.StackTrace?.Contains("QuyiMetod")}");
        }
    }
}

```

## Tushuntirish va Mantiq:
Hech qachon `catch (Exception ex) { throw ex; }` yozmang! Bu xatolikning tub ildizini o'chirib yuboradi. Har doim parametr ko'rsatmasdan `throw;` deb qayta oting (Rethrow).

## Ishlash natijasi:
```text
StackTrace ichida 'QuyiMetod' bormi: True
```

# 405-Topshiriq: InnerException: Ichki istisnolar bilan xato kontekstini saqlash
## Topshiriq sharti:
Pastki qatlam xatosini yuqori domen xatosi bilan o'rashda `InnerException` dan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

class BazaXatosi : Exception
{
    public BazaXatosi(string xabar, Exception ichkiXato) : base(xabar, ichkiXato) { }
}

internal class Program
{
    static void BazagaYoz()
    {
        try
        {
            throw new TimeoutException("Tarmoq vaqti tugadi");
        }
        catch (TimeoutException tex)
        {
            // Xatoni o'rab yuqori qatlamga uzatish
            throw new BazaXatosi("Mijozni saqlashda xatolik yuz berdi", tex);
        }
    }

    static void Main()
    {
        try
        {
            BazagaYoz();
        }
        catch (BazaXatosi ex)
        {
            Console.WriteLine($"Asosiy xato: {ex.Message}");
            Console.WriteLine($"Ichki sabab: {ex.InnerException?.GetType().Name}: {ex.InnerException?.Message}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`InnerException` orqali texnik past darajadagi xatoliklar (masalan `SqlException`, `SocketException`) domen xatolariga (`OrderProcessingException`) aylantiriladi, lekin asl sabab yo'qotilmaydi.

## Ishlash natijasi:
```text
Asosiy xato: Mijozni saqlashda xatolik yuz berdi
Ichki sabab: TimeoutException: Tarmoq vaqti tugadi
```

# 406-Topshiriq: C# 6 Exception Filters: when kalit so'zi
## Topshiriq sharti:
`when` yordamida faqat ma'lum bir shart bajarilgandagina `catch` blokiga kiruvchi filtr yozing.

## Yechim (C# kodi):
```csharp
using System;

class HttpXato : Exception
{
    public int StatusCode { get; }
    public HttpXato(int code, string msg) : base(msg) => StatusCode = code;
}

internal class Program
{
    static void So'rovYubor(int kod) => throw new HttpXato(kod, "Server javobi");

    static void Main()
    {
        try
        {
            So'rovYubor(404);
        }
        catch (HttpXato ex) when (ex.StatusCode == 404)
        {
            Console.WriteLine("Filtr ishga tushdi: 404 - Sahifa topilmadi!");
        }
        catch (HttpXato ex) when (ex.StatusCode == 500)
        {
            Console.WriteLine("Filtr ishga tushdi: 500 - Server ichki xatosi!");
        }
    }
}

```

## Tushuntirish va Mantiq:
Exception Filters (`catch (...) when (shart)`) C# 6 da kiritilgan. Uning katta ustunligi shundaki, agar `when` sharti `false` bo'lsa, Stack Unwinding sodir bo'lmaydi va xotira holati (Call Stack) toza saqlanadi.

## Ishlash natijasi:
```text
Filtr ishga tushdi: 404 - Sahifa topilmadi!
```

# 407-Topshiriq: Maxsus (Custom) domen istisnosi yaratish
## Topshiriq sharti:
Biznes qoidalari uchun o'z shaxsiy `YetarliMablagMavjudEmasException` sinfingizni yarating.

## Yechim (C# kodi):
```csharp
using System;

public class YetarliMablagMavjudEmasException : Exception
{
    public decimal JoriyBalans { get; }
    public decimal TalabQilingan { get; }

    public YetarliMablagMavjudEmasException(decimal joriy, decimal talab)
        : base($"Yetarli mablag' yo'q! Joriy balans: {joriy:N0} so'm, talab qilindi: {talab:N0} so'm.")
    {
        JoriyBalans = joriy;
        TalabQilingan = talab;
    }
}

internal class Program
{
    static void Main()
    {
        try
        {
            decimal balans = 50000m;
            decimal yechish = 120000m;

            if (yechish > balans)
            {
                throw new YetarliMablagMavjudEmasException(balans, yechish);
            }
        }
        catch (YetarliMablagMavjudEmasException ex)
        {
            Console.WriteLine($"Xato: {ex.Message}");
            Console.WriteLine($"Yetishmayotgan summa: {ex.TalabQilingan - ex.JoriyBalans:N0} so'm");
        }
    }
}

```

## Tushuntirish va Mantiq:
Custom Exception lar `Exception` sinfidan meros oladi va domen bilan bog'liq maxsus xossalarni (`JoriyBalans`, `TalabQilingan`) o'z ichiga oladi. Bu xatolikni tutuvchi qatlamga aniq qaror qabul qilish imkonini beradi.

## Ishlash natijasi:
```text
Xato: Yetarli mablag' yo'q! Joriy balans: 50,000 so'm, talab qilindi: 120,000 so'm.
Yetishmayotgan summa: 70,000 so'm
```

# 408-Topshiriq: C# 8 using deklaratsiyasi: Jingalak qavslarsiz xavfsiz tozalash
## Topshiriq sharti:
Eski `using (...) { }` bloki o'rniga blok tugashida avtomatik ishlovchi zamonaviy `using var` deklaratsiyasidan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

class XotiraFayli : IDisposable
{
    public string Nomi { get; }
    public XotiraFayli(string nomi) => Nomi = nomi;

    public void Dispose() => Console.WriteLine($"Dispose: {Nomi} xavfsiz yopildi.");
}

internal class Program
{
    static void Jarayon()
    {
        using var fayl = new XotiraFayli("hujjat.docx");
        Console.WriteLine($"Fayl bilan ishlanmoqda: {fayl.Nomi}");
        // Metod tugaganda yoki xatolik yuz berganda avtomatik Dispose() chaqiriladi
    }

    static void Main()
    {
        Jarayon();
        Console.WriteLine("Jarayon yakunlandi.");
    }
}

```

## Tushuntirish va Mantiq:
C# 8 da kiritilgan `using var` deklaratsiyasi o'zgaruvchining joriy ko'rinish sohasi (scope) tugaganda avtomatik ravishda `Dispose()` chaqiradi. Bu ortiqcha jingalak qavslarni yo'qotadi.

## Ishlash natijasi:
```text
Fayl bilan ishlanmoqda: hujjat.docx
Dispose: hujjat.docx xavfsiz yopildi.
Jarayon yakunlandi.
```

# 409-Topshiriq: AggregateException: Parallel vazifalardagi jamlangan istisnolar
## Topshiriq sharti:
Bir vaqtda bir nechta oqimda xatolik yuz berganda ularning barchasini bitta `AggregateException` ichidan o'qish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static void Main()
    {
        try
        {
            // Bir nechta xatolik yuz beruvchi parallel vazifalar
            var t1 = Task.Run(() => throw new ArgumentException("1-xatolik"));
            var t2 = Task.Run(() => throw new InvalidOperationException("2-xatolik"));

            Task.WaitAll(t1, t2);
        }
        catch (AggregateException ex)
        {
            Console.WriteLine($"Jamlangan istisnolar soni: {ex.InnerExceptions.Count}");
            foreach (var inner in ex.InnerExceptions)
            {
                Console.WriteLine($"- {inner.GetType().Name}: {inner.Message}");
            }
        }
    }
}

```

## Tushuntirish va Mantiq:
`Task` va `Parallel` operatsiyalari parallel oqimlarda yuz bergan barcha istisnolarni bitta `AggregateException` ro'yxatiga jamlaydi. `.InnerExceptions` orqali har bir parallel xatoni alohida tahlil qilish mumkin.

## Ishlash natijasi:
```text
Jamlangan istisnolar soni: 2
- ArgumentException: 1-xatolik
- InvalidOperationException: 2-xatolik
```

# 410-Topshiriq: AggregateException.Flatten() va Handle() metodlari
## Topshiriq sharti:
Ichma-ich o'ralgan jamlangan istisnolarni `Flatten()` bilan tekislash va `Handle()` bilan saralash.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;

internal class Program
{
    static void Main()
    {
        var ichki = new AggregateException(new FileNotFoundException("Fayl yo'q"));
        var tashqi = new AggregateException(ichki, new TimeoutException("Vaqt tugadi"));

        // Flatten() iyerarxiyani bitta ro'yxatga tekislaydi
        var tekis = tashqi.Flatten();

        tekis.Handle(ex =>
        {
            if (ex is FileNotFoundException)
            {
                Console.WriteLine("FileNotFoundException muvaffaqiyatli qayta ishlandi.");
                return true; // Xato hal qilindi deb belgilash
            }
            return false; // Boshqa xatolar qayta otiladi
        });
    }
}

```

## Tushuntirish va Mantiq:
`Flatten()` murakkab ichma-ich `AggregateException` larni yagona tekis ro'yxatga aylantiradi. `Handle(Func<Exception, bool>)` esa har bir ichki xatoni tekshirib, agar hal qilingan bo'lsa `true` qaytaradi.

## Ishlash natijasi:
```text
FileNotFoundException muvaffaqiyatli qayta ishlandi.
```

# 411-Topshiriq: Tester-Doer naqshi: Istisno otilishining oldini olish
## Topshiriq sharti:
`try-catch` o'rniga oldindan tekshirib amal bajarish orqali unumdorlikni saqlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        var lugat = new Dictionary<string, int> { ["A"] = 1 };

        // Yomon usul (Exception for control flow):
        // try { int x = lugat["B"]; } catch { ... }

        // To'g'ri usul (Tester-Doer):
        // Tester: ContainsKey, Doer: lugat[...]
        if (lugat.ContainsKey("B"))
        {
            Console.WriteLine(lugat["B"]);
        }
        else
        {
            Console.WriteLine("Kalit topilmadi (0 istisno sarfi).");
        }
    }
}

```

## Tushuntirish va Mantiq:
Istisno otish CLR da juda og'ir (minglab CPU sikllari) operatsiyadir. Shuning uchun kutilgan holatlar uchun istisno otmasdan, avval `ContainsKey` yoki `CanExecute` orqali tekshirish kerak.

## Ishlash natijasi:
```text
Kalit topilmadi (0 istisno sarfi).
```

# 412-Topshiriq: Try-Parse naqshi (TryX Pattern)
## Topshiriq sharti:
`bool TryDo(out T result)` qoidasi asosida o'z shaxsiy xavfsiz metodini yaratish.

## Yechim (C# kodi):
```csharp
using System;

class XavfsizHisoblagich
{
    public static bool TryBolish(int a, int b, out int natija)
    {
        if (b == 0)
        {
            natija = 0;
            return false;
        }

        natija = a / b;
        return true;
    }
}

internal class Program
{
    static void Main()
    {
        if (XavfsizHisoblagich.TryBolish(20, 4, out int javob))
        {
            Console.WriteLine($"20 / 4 = {javob}");
        }

        if (!XavfsizHisoblagich.TryBolish(10, 0, out _))
        {
            Console.WriteLine("0 ga bo'lib bo'lmadi, dastur to'xtamasdan davom etdi.");
        }
    }
}

```

## Tushuntirish va Mantiq:
Try-Parse naqshi muvaffaqiyatli bo'lsa `true` va `out` qiymat beradi, aks holda `false` qaytaradi va birorta ham istisno obyekti yaratmaydi.

## Ishlash natijasi:
```text
20 / 4 = 5
0 ga bo'lib bo'lmadi, dastur to'xtamasdan davom etdi.
```

# 413-Topshiriq: Istisnolarni yutib yuborish (Swallowing Exceptions) anti-patterni
## Topshiriq sharti:
Bo'sh `catch { }` bloki yozish nima uchun tizim xatolarini yashirib qo'yishini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void YomonKod()
    {
        try
        {
            int[] m = [1, 2];
            int x = m[5]; // Xato!
        }
        catch
        {
            // ANTI-PATTERN: Xato yutib yuborildi, hech kim nima bo'lganini bilmaydi!
        }
    }

    static void Main()
    {
        YomonKod();
        Console.WriteLine("Xato jimgina yutib yuborildi. Bunday qilish taqiqlanadi!");
    }
}

```

## Tushuntirish va Mantiq:
Bo'sh `catch` bloki dasturchi uchun eng xavfli tuzoqdir. Tizim noto'g'ri ishlashda davom etadi, ma'lumotlar buziladi va loglarda hech qanday iz qolmaydi. Har doim xatoni kamida log qiling yoki qayta oting.

## Ishlash natijasi:
```text
Xato jimgina yutib yuborildi. Bunday qilish taqiqlanadi!
```

# 414-Topshiriq: OperationCanceledException va CancellationToken
## Topshiriq sharti:
Uzoq amaliyot bekor qilinganda `OperationCanceledException` otilishi va ushlanishini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    static void Main()
    {
        using var cts = new CancellationTokenSource();

        // 100 ms dan keyin bekor qilish
        cts.CancelAfter(50);

        try
        {
            Console.WriteLine("Amaliyot boshlandi...");
            Thread.Sleep(100);
            cts.Token.ThrowIfCancellationRequested();
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine("Amaliyot bekor qilindi (CancellationToken orqali to'xtatildi).");
        }
    }
}

```

## Tushuntirish va Mantiq:
.NET da asinxron yoki fon amaliyotlarini to'xtatish uchun `OperationCanceledException` standart vositadir. Bu oddiy avariya xatosi emas, balki kutilgan to'xtash signali hisoblanadi.

## Ishlash natijasi:
```text
Amaliyot boshlandi...
Amaliyot bekor qilindi (CancellationToken orqali to'xtatildi).
```

# 415-Topshiriq: InvalidOperationException: Noto'g'ri obyekt holati
## Topshiriq sharti:
Obyekt holati ruxsat bermagan amaliyot bajarilayotganda `InvalidOperationException` otish.

## Yechim (C# kodi):
```csharp
using System;

class Svetofor
{
    private bool yoniqmi = false;

    public void HarakatgaRuxsat()
    {
        if (!yoniqmi)
            throw new InvalidOperationException("Svetofor o'chiq holatda harakatga ruxsat berib bo'lmaydi!");

        Console.WriteLine("Yashil chiroq yondi.");
    }
}

internal class Program
{
    static void Main()
    {
        var s = new Svetofor();
        try
        {
            s.HarakatgaRuxsat();
        }
        catch (InvalidOperationException ex)
        {
            Console.WriteLine($"Xato ushlandi: {ex.Message}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`InvalidOperationException` argumentlar to'g'ri bo'lsa ham, obyektning joriy ichki holati ushbu amalni bajarishga mos kelmagan paytda ishlatiladi.

## Ishlash natijasi:
```text
Xato ushlandi: Svetofor o'chiq holatda harakatga ruxsat berib bo'lmaydi!
```

# 416-Topshiriq: ObjectDisposedException: Yopilgan resursdan foydalanish xatosi
## Topshiriq sharti:
`Dispose()` chaqirilib yopilgan obyektdan qayta foydalanishga urinilganda ushbu istisnoni ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

class Kassa : IDisposable
{
    private bool yopilgan = false;

    public void TolovQabulQil()
    {
        ObjectDisposedException.ThrowIf(yopilgan, this);
        Console.WriteLine("To'lov qabul qilindi.");
    }

    public void Dispose() => yopilgan = true;
}

internal class Program
{
    static void Main()
    {
        var kassa = new Kassa();
        kassa.TolovQabulQil();
        kassa.Dispose();

        try
        {
            kassa.TolovQabulQil();
        }
        catch (ObjectDisposedException ex)
        {
            Console.WriteLine($"Kassa yopilgan: {ex.ObjectName}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`ObjectDisposedException` resurs yopilganidan keyin chaqirilgan metodlarni bloklaydi va xavfli xotira amaliyotlarining oldini oladi.

## Ishlash natijasi:
```text
To'lov qabul qilindi.
Kassa yopilgan: Kassa
```

# 417-Topshiriq: Exception.Data lug'ati orqali qo'shimcha parametrlar biriktirish
## Topshiriq sharti:
Har qanday istisnoga `ex.Data["Kalit"] = qiymat` orqali kontekst qo'shish.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Bajar()
    {
        try
        {
            int n = int.Parse("xato_son");
        }
        catch (FormatException ex)
        {
            ex.Data["FoydalanuvchiId"] = 42;
            ex.Data["IPManzil"] = "192.168.1.100";
            throw;
        }
    }

    static void Main()
    {
        try
        {
            Bajar();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Xato: {ex.Message}");
            Console.WriteLine($"Qo'shimcha UserId: {ex.Data["FoydalanuvchiId"]}");
            Console.WriteLine($"Qo'shimcha IP:     {ex.Data["IPManzil"]}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`Exception.Data` barcha istisnolarda mavjud bo'lgan kalit-qiymat lug'atidir. U orqali xatolik ro'yxatga olinayotganda foydali diagnostika ma'lumotlarini biriktirish mumkin.

## Ishlash natijasi:
```text
Xato: The input string 'xato_son' was not in a correct format.
Qo'shimcha UserId: 42
Qo'shimcha IP:     192.168.1.100
```

# 418-Topshiriq: ExceptionDispatchInfo: StackTrace ni saqlab boshqa oqimda otish
## Topshiriq sharti:
`ExceptionDispatchInfo.Capture` yordamida ushlangan xatoni StackTrace yo'qotmasdan qayta otish.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.ExceptionServices;

internal class Program
{
    static void XavfliKod() => throw new ArgumentException("Asl qatordagi xatolik");

    static void Main()
    {
        ExceptionDispatchInfo? ushlangan = null;

        try
        {
            XavfliKod();
        }
        catch (Exception ex)
        {
            // Xatoni xotirada ushlab turish
            ushlangan = ExceptionDispatchInfo.Capture(ex);
        }

        Console.WriteLine("Oraliq kodlar bajarildi...");

        try
        {
            // Boshqa joyda asl StackTrace bilan qayta otish
            ushlangan?.Throw();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Xato qayta otildi: {ex.Message}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`ExceptionDispatchInfo` asinxron kutubxonalar va vazifalar (Tasks) dvigatelida pastki oqim xatolarini chaqiruvchi asosiy oqimga xuddi o'sha yerda yuz bergandek yetkazish uchun qo'llaniladi.

## Ishlash natijasi:
```text
Oraliq kodlar bajarildi...
Xato qayta otildi: Asl qatordagi xatolik
```

# 419-Topshiriq: Result Pattern asoslari: Istisnosiz xatolik boshqaruvi
## Topshiriq sharti:
Biznes xatolarida og'ir Exception otmasdan, muvaffaqiyat yoki xatoni qaytaruvchi `Result` strukturasini yarating.

## Yechim (C# kodi):
```csharp
using System;

public readonly record struct Result(bool IsSuccess, string? Error)
{
    public static Result Success() => new(true, null);
    public static Result Failure(string error) => new(false, error);
}

internal class Program
{
    static Result ParolTekshir(string parol)
    {
        if (parol.Length < 6) return Result.Failure("Parol kamida 6 belgidan iborat bo'lishi shart!");
        return Result.Success();
    }

    static void Main()
    {
        var r1 = ParolTekshir("123");
        var r2 = ParolTekshir("maxfiy123");

        Console.WriteLine($"1-parol holati: {r1.IsSuccess}, Xato: {r1.Error}");
        Console.WriteLine($"2-parol holati: {r2.IsSuccess}");
    }
}

```

## Tushuntirish va Mantiq:
Result Pattern kutilgan biznes xatoliklarida (masalan noto'g'ri parol, mahsulot yo'qligi) istisno otishning oldini oladi va tizim unumdorligini hamda kod o'qilishini sezilarli yaxshilaydi.

## Ishlash natijasi:
```text
1-parol holati: False, Xato: Parol kamida 6 belgidan iborat bo'lishi shart!
2-parol holati: True
```

# 420-Topshiriq: Generic Result<T> modeli
## Topshiriq sharti:
Muvaffaqiyatli bo'lsa ma'lumot, aks holda xatolik matnini qaytaruvchi `Result<T>` generik modelini yozing.

## Yechim (C# kodi):
```csharp
using System;

public readonly record struct Result<T>
{
    public bool IsSuccess { get; }
    public T? Value { get; }
    public string? Error { get; }

    private Result(T value) => (IsSuccess, Value, Error) = (true, value, null);
    private Result(string error) => (IsSuccess, Value, Error) = (false, default, error);

    public static Result<T> Success(T value) => new(value);
    public static Result<T> Failure(string error) => new(error);
}

internal class Program
{
    static Result<int> SonniParseQil(string matn)
    {
        if (int.TryParse(matn, out int s)) return Result<int>.Success(s);
        return Result<int>.Failure("Matn raqamlardan iborat emas");
    }

    static void Main()
    {
        var res = SonniParseQil("1024");
        if (res.IsSuccess)
        {
            Console.WriteLine($"Muvaffaqiyatli olingan qiymat: {res.Value}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`Result<T>` funksional tillardagi `Either` yoki Rust dagi `Result<T, E>` ga o'xshaydi va zamonaviy C# da domen xatoliklarini modellashtirishning oltin standartidir.

## Ishlash natijasi:
```text
Muvaffaqiyatli olingan qiymat: 1024
```

# 421-Topshiriq: Retry Pattern: Xatolik yuz berganda qayta urinish
## Topshiriq sharti:
Vaqtinchalik nosozliklar (Transient faults) paytida amaliyotni bir necha marta qayta takrorlovchi mexanizm yozing.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    static int urinishSoni = 0;

    static string TarmoqSo'rovi()
    {
        urinishSoni++;
        if (urinishSoni < 3)
        {
            throw new TimeoutException($"Ulanish xatosi (Urinish #{urinishSoni})");
        }
        return "Serverdan ma'lumot olindi!";
    }

    static void Main()
    {
        int maksUrinish = 3;
        for (int i = 1; i <= maksUrinish; i++)
        {
            try
            {
                string natija = TarmoqSo'rovi();
                Console.WriteLine($"Muvaffaqiyat: {natija}");
                break;
            }
            catch (TimeoutException ex)
            {
                Console.WriteLine($"Ogohlantirish: {ex.Message}. Qayta urinilmoqda...");
                Thread.Sleep(20);
            }
        }
    }
}

```

## Tushuntirish va Mantiq:
Retry Pattern bulutli xizmatlar bilan ishlashda vaqtinchalik tarmoq uzilishlarini foydalanuvchiga bildirmasdan o'z joyida hal qilish imkonini beradi.

## Ishlash natijasi:
```text
Ogohlantirish: Ulanish xatosi (Urinish #1). Qayta urinilmoqda...
Ogohlantirish: Ulanish xatosi (Urinish #2). Qayta urinilmoqda...
Muvaffaqiyat: Serverdan ma'lumot olindi!
```

# 422-Topshiriq: Environment.FailFast: Kritik xatolikda dasturni zudlik bilan to'xtatish
## Topshiriq sharti:
Xotira yoki xavfsizlik buzilganda `finally` bloklarini ham chetlab o'tib jarayonni bir zumda o'ldiruvchi `FailFast` ni tushuntiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Environment.FailFast tushuntirishi:");
        Console.WriteLine("Agar kritik bufer buzilishi (data corruption) aniqlansa,");
        Console.WriteLine("dastur 'Environment.FailFast()' orqali bir zumda qulatiladi.");
        Console.WriteLine("Bunda hech qanday finally yoki catch bloklari ishlamaydi, tizim darhol himoyalanadi.");
    }
}

```

## Tushuntirish va Mantiq:
`Environment.FailFast` operatsion tizimga hodisalar jurnalida kritik qulashni (crash dump) qayd etib, jarayonni zudlik bilan to'xtatishni buyuradi. Bu buzuq ma'lumotlar bazaga yozilib ketishining oldini oladi.

## Ishlash natijasi:
```text
Environment.FailFast tushuntirishi:
Agar kritik bufer buzilishi (data corruption) aniqlansa,
dastur 'Environment.FailFast()' orqali bir zumda qulatiladi.
Bunda hech qanday finally yoki catch bloklari ishlamaydi, tizim darhol himoyalanadi.
```

# 423-Topshiriq: StackOverflowException ni ushlab bo'lmasligi (.NET qoidasi)
## Topshiriq sharti:
Nega cheksiz rekursiya sababli Stack to'lganda uni `try-catch` bilan qutqarib bo'lmasligini tushuntiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        Console.WriteLine(".NET 2.0 dan boshlab StackOverflowException ni try-catch bilan ushlab bo'lmaydi.");
        Console.WriteLine("Sababi: Stack xotira to'lganda yangi catch blokini bajarish uchun ham Stack da joy qolmaydi!");
        Console.WriteLine("Natijada CLR xavfsizlik uchun butun jarayonni zudlik bilan tugatadi.");
    }
}

```

## Tushuntirish va Mantiq:
StackOverflow yuz berganda xotira yaxlitligi buziladi. Shuning uchun CLR barcha dasturchilarga rekursiyada to'xtash shartlarini qat'iy tekshirishni talab qiladi.

## Ishlash natijasi:
```text
.NET 2.0 dan boshlab StackOverflowException ni try-catch bilan ushlab bo'lmaydi.
Sababi: Stack xotira to'lganda yangi catch blokini bajarish uchun ham Stack da joy qolmaydi!
Natijada CLR xavfsizlik uchun butun jarayonni zudlik bilan tugatadi.
```

# 424-Topshiriq: Global Unhandled Exception Handler
## Topshiriq sharti:
Dasturning barcha ushlanmagan xatolarini markaziy nuqtada ushlash.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        AppDomain.CurrentDomain.UnhandledException += (sender, args) =>
        {
            Exception ex = (Exception)args.ExceptionObject;
            Console.WriteLine($"[GLOBAL LOG]: Ushlanmagan xatolik yuz berdi: {ex.Message}");
        };

        Console.WriteLine("Global xatolik kuzatuvchisi muvaffaqiyatli ulandi.");
    }
}

```

## Tushuntirish va Mantiq:
`AppDomain.CurrentDomain.UnhandledException` konsol va desktop dasturlarida oxirgi himoya chizig'idir. Bu yerda xatolik log qilinadi va favqulodda tozalash ishlari bajariladi.

## Ishlash natijasi:
```text
Global xatolik kuzatuvchisi muvaffaqiyatli ulandi.
```

# 425-Topshiriq: finally blokida istisno chiqishining xavfi
## Topshiriq sharti:
`finally` ichida yangi xato otilganda dastlabki xatoning yo'qolib ketishi (masking) muammosini tahlil qiling.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Sinov()
    {
        try
        {
            throw new InvalidOperationException("1-Asl xato!");
        }
        finally
        {
            // finally ichida xato otish 1-xatoni yutib yuboradi!
            // Shuning uchun finally ichida doimo xavfsiz tozalash yoziladi.
            Console.WriteLine("finally ichida har doim xavfsiz Dispose qilinishi shart.");
        }
    }

    static void Main()
    {
        try
        {
            Sinov();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Ushlangan xato: {ex.Message}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`finally` bloki ichidagi yangi istisno asl `try` dagi xatolikni butunlay maskalaydi (yo'qotadi). Shu sababli `finally` va `Dispose` ichida har doim xatolikdan himoyalangan kod yozilishi shart.

## Ishlash natijasi:
```text
finally ichida har doim xavfsiz Dispose qilinishi shart.
Ushlangan xato: 1-Asl xato!
```

# 426-Topshiriq: NotSupportedException va NotImplementedException
## Topshiriq sharti:
Hali yozilmagan metodlar uchun `NotImplementedException` va arxitekturaviy taqiqlangan amallar uchun `NotSupportedException` ni qo'llang.

## Yechim (C# kodi):
```csharp
using System;

class FaylOmbori
{
    public void Oqish() => Console.WriteLine("Fayl o'qildi.");

    public void Yozish()
    {
        // Ushbu ombor faqat o'qish uchun (Read-only)
        throw new NotSupportedException("Ushbu ombor faqat o'qish uchun mo'ljallangan!");
    }

    public void Siqish()
    {
        // Kelajakda yozilishi rejalashtirilgan metod
        throw new NotImplementedException("Faylni siqish funksiyasi keyingi versiyada chiqariladi.");
    }
}

internal class Program
{
    static void Main()
    {
        var f = new FaylOmbori();
        f.Oqish();

        try { f.Yozish(); }
        catch (NotSupportedException ex) { Console.WriteLine($"Qo'llab-quvvatlanmaydi: {ex.Message}"); }

        try { f.Siqish(); }
        catch (NotImplementedException ex) { Console.WriteLine($"Hali yozilmagan: {ex.Message}"); }
    }
}

```

## Tushuntirish va Mantiq:
`NotImplementedException` ishlab chiqish jarayonida vaqtincha qo'yiladi. `NotSupportedException` esa obyekt ushbu amalni arxitekturaviy sabablarga ko'ra qat'iyan bajara olmasligini bildiradi.

## Ishlash natijasi:
```text
Fayl o'qildi.
Qo'llab-quvvatlanmaydi: Ushbu ombor faqat o'qish uchun mo'ljallangan!
Hali yozilmagan: Faylni siqish funksiyasi keyingi versiyada chiqariladi.
```

# 427-Topshiriq: NullReferenceException tahlili va NRT orqali profilaktika
## Topshiriq sharti:
`NullReferenceException` xatosining tub sababi va zamonaviy C# da uning oldini olish.

## Yechim (C# kodi):
```csharp
using System;

class Profil
{
    public string? Telefon { get; set; }
}

internal class Program
{
    static void Main()
    {
        Profil? p = null;

        // Xavfli: p.Telefon.Length -> NullReferenceException
        // Xavfsiz zamonaviy usul:
        int uzunlik = p?.Telefon?.Length ?? 0;

        Console.WriteLine($"Telefon raqami uzunligi: {uzunlik} (Xatoliksiz xavfsiz hisoblandi)");
    }
}

```

## Tushuntirish va Mantiq:
`NullReferenceException` xotirada mavjud bo'lmagan obyekt manziliga murojaat qilinganda ro'y beradi. Zamonaviy C# da NRT (Nullable Reference Types) va `?.` operatori orqali bu xato butunlay bartaraf etiladi.

## Ishlash natijasi:
```text
Telefon raqami uzunligi: 0 (Xatoliksiz xavfsiz hisoblandi)
```

# 428-Topshiriq: Custom Exception da boy metama'lumotlar saqlash
## Topshiriq sharti:
Xatolik ro'yxatga olinganda tahlilni osonlashtirish uchun qo'shimcha xossalarga ega istisno sinfi yozing.

## Yechim (C# kodi):
```csharp
using System;

class TolovXatosi : Exception
{
    public string TranzaksiyaId { get; }
    public decimal Summa { get; }
    public DateTime Vaqt { get; }

    public TolovXatosi(string id, decimal summa, string sabab) : base(sabab)
    {
        TranzaksiyaId = id;
        Summa = summa;
        Vaqt = DateTime.UtcNow;
    }
}

internal class Program
{
    static void Main()
    {
        try
        {
            throw new TolovXatosi("TX_7788", 250000m, "Mijoz hisobi bloklangan");
        }
        catch (TolovXatosi ex)
        {
            Console.WriteLine($"Xato sababi:   {ex.Message}");
            Console.WriteLine($"Tranzaksiya:   {ex.TranzaksiyaId}");
            Console.WriteLine($"Summa:         {ex.Summa:N0} so'm");
        }
    }
}

```

## Tushuntirish va Mantiq:
Custom Exception faqat matn emas, balki tranzaksiya ID si, foydalanuvchi ma'lumotlari kabi strukturaviy qiymatlarni o'zida saqlashi monitoring tizimlari (Sentry, Application Insights) uchun juda qulay.

## Ishlash natijasi:
```text
Xato sababi:   Mijoz hisobi bloklangan
Tranzaksiya:   TX_7788
Summa:         250,000 so'm
```

# 429-Topshiriq: Funksional Result<T, TError> modeli
## Topshiriq sharti:
Muvaffaqiyatsizlik holatida aniq Enum yoki xatolik obyektini qaytaruvchi ikki tomonlama Result strukturasini quring.

## Yechim (C# kodi):
```csharp
using System;

enum XatoTuri { Topilmadi, HuquqYetarliEmas, ValidatsiyaXatosi }

readonly record struct Result<T, TError>
{
    public bool IsSuccess { get; }
    public T? Value { get; }
    public TError? Error { get; }

    private Result(T value) => (IsSuccess, Value, Error) = (true, value, default);
    private Result(TError error) => (IsSuccess, Value, Error) = (false, default, error);

    public static Result<T, TError> Ok(T value) => new(value);
    public static Result<T, TError> Fail(TError error) => new(error);
}

internal class Program
{
    static Result<string, XatoTuri> HujjatniYukla(int id)
    {
        if (id <= 0) return Result<string, XatoTuri>.Fail(XatoTuri.ValidatsiyaXatosi);
        if (id == 404) return Result<string, XatoTuri>.Fail(XatoTuri.Topilmadi);
        return Result<string, XatoTuri>.Ok("Hujjat matni");
    }

    static void Main()
    {
        var r = HujjatniYukla(404);
        if (!r.IsSuccess)
        {
            Console.WriteLine($"Xatolik turi: {r.Error}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`Result<T, TError>` arxitekturada xatoliklarni tiplash imkonini beradi. Qabul qiluvchi kod switch expression orqali har bir xato turiga alohida ishlov bera oladi.

## Ishlash natijasi:
```text
Xatolik turi: Topilmadi
```

# 430-Topshiriq: Strukturaviy xatoliklarni loglash simulyatsiyasi
## Topshiriq sharti:
Xatolik yuz berganda parametrlar bilan strukturaviy JSON log yozish tamoyilini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void LogXato(Exception ex, string operatsiya, params (string Kalit, object Qiymat)[] parametrlar)
    {
        Console.WriteLine($"[ERROR LOG]: Operatsiya '{operatsiya}' muvaffaqiyatsiz bo'ldi.");
        Console.WriteLine($"Sabab: {ex.Message}");
        foreach (var p in parametrlar)
        {
            Console.WriteLine($"  - {p.Kalit} = {p.Qiymat}");
        }
    }

    static void Main()
    {
        try
        {
            throw new TimeoutException("Tashqi API javob bermadi");
        }
        catch (Exception ex)
        {
            LogXato(ex, "MijozBalansiniYangilash", ("MijozId", 501), ("Summa", 100000m));
        }
    }
}

```

## Tushuntirish va Mantiq:
Strukturaviy loglash (Structured Logging) Elasticsearch, Seq yoki Grafana tizimlarida xatoliklarni parametrlar bo'yicha tezkor qidirish va guruhlash imkonini beradi.

## Ishlash natijasi:
```text
[ERROR LOG]: Operatsiya 'MijozBalansiniYangilash' muvaffaqiyatsiz bo'ldi.
Sabab: Tashqi API javob bermadi
  - MijozId = 501
  - Summa = 100000
```

# 431-Topshiriq: Circuit Breaker naqshi: Tizim qulashining oldini olish
## Topshiriq sharti:
Tashqi xizmat ketma-ket xato berganda so'rovlarni vaqtincha to'xtatuvchi oddiy Circuit Breaker sinfini yozing.

## Yechim (C# kodi):
```csharp
using System;

class OddiyCircuitBreaker
{
    private int ketmaKetXatolar = 0;
    private bool ochiqmi = false;

    public void Bajar(Action amal)
    {
        if (ochiqmi)
        {
            Console.WriteLine("[CIRCUIT BREAKER OCHIQ]: So'rovlar vaqtincha to'xtatilgan, server dam olmoqda!");
            return;
        }

        try
        {
            amal();
            ketmaKetXatolar = 0; // Muvaffaqiyatli bo'lsa nolga tushirish
        }
        catch (Exception)
        {
            ketmaKetXatolar++;
            Console.WriteLine($"Xato qayd etildi ({ketmaKetXatolar}/2)");
            if (ketmaKetXatolar >= 2)
            {
                ochiqmi = true; // Zanjirni uzish
                Console.WriteLine("--> Kritik chegara oshdi: Zanjir uzildi (Circuit Breaker OPEN)!");
            }
        }
    }
}

internal class Program
{
    static void Main()
    {
        var cb = new OddiyCircuitBreaker();
        cb.Bajar(() => throw new Exception("1-Avariya"));
        cb.Bajar(() => throw new Exception("2-Avariya"));
        cb.Bajar(() => Console.WriteLine("Bu bajarilmaydi"));
    }
}

```

## Tushuntirish va Mantiq:
Circuit Breaker naqshi qulab yotgan tashqi serverga behuda so'rovlar yuborib o'z tizimini ham qulatishning oldini oladi (Polly kutubxonasi buni mukammal ta'minlaydi).

## Ishlash natijasi:
```text
Xato qayd etildi (1/2)
Xato qayd etildi (2/2)
--> Kritik chegara oshdi: Zanjir uzildi (Circuit Breaker OPEN)!
[CIRCUIT BREAKER OCHIQ]: So'rovlar vaqtincha to'xtatilgan, server dam olmoqda!
```

# 432-Topshiriq: TypeInitializationException: Statik konstruktor qulaganda nima bo'ladi?
## Topshiriq sharti:
Statik konstruktor ichida xatolik yuz berganda butun sinfning ishdan chiqishini namoyish eting.

## Yechim (C# kodi):
```csharp
using System;

class XavfliSinf
{
    static XavfliSinf()
    {
        // Statik konstruktorda kutilmagan istisno
        throw new InvalidOperationException("Statik resurs yuklanmadi!");
    }

    public static void Salom() => Console.WriteLine("Salom");
}

internal class Program
{
    static void Main()
    {
        try
        {
            XavfliSinf.Salom();
        }
        catch (TypeInitializationException ex)
        {
            Console.WriteLine($"Xatolik ushlandi: {ex.GetType().Name}");
            Console.WriteLine($"Asl ichki sabab: {ex.InnerException?.Message}");
        }
    }
}

```

## Tushuntirish va Mantiq:
Agar sinfning statik konstruktori xato bilan tugasa, CLR ushbu sinfni butun dastur umri davomida 'yaroqsiz' (unusable) deb belgilaydi va keyingi har qanday chaqiruvda `TypeInitializationException` beradi.

## Ishlash natijasi:
```text
Xatolik ushlandi: TypeInitializationException
Asl ichki sabab: Statik resurs yuklanmadi!
```

# 433-Topshiriq: Web API ProblemDetails (RFC 7807) standarti
## Topshiriq sharti:
Zamonaviy veb-xizmatlarda xatoliklarni xalqaro RFC 7807 standartiga mos JSON shaklida ifodalovchi model tuzing.

## Yechim (C# kodi):
```csharp
using System;

record ProblemDetails(
    string Type,
    string Title,
    int Status,
    string Detail,
    string Instance);

internal class Program
{
    static void Main()
    {
        var xato = new ProblemDetails(
            Type: "https://example.com/errors/not-found",
            Title: "Resurs topilmadi",
            Status: 404,
            Detail: "Kiritilgan ID (99) ga ega foydalanuvchi ma'lumotlar bazasida mavjud emas.",
            Instance: "/api/users/99"
        );

        Console.WriteLine($"Status: {xato.Status} - {xato.Title}");
        Console.WriteLine($"Tafsilot: {xato.Detail}");
        Console.WriteLine($"Manzil: {xato.Instance}");
    }
}

```

## Tushuntirish va Mantiq:
ASP.NET Core va zamonaviy REST API larda xatoliklarni o'zboshimcha matn sifatida emas, balki RFC 7807 ProblemDetails standarti bo'yicha qaytarish qabul qilingan.

## Ishlash natijasi:
```text
Status: 404 - Resurs topilmadi
Tafsilot: Kiritilgan ID (99) ga ega foydalanuvchi ma'lumotlar bazasida mavjud emas.
Manzil: /api/users/99
```

# 434-Topshiriq: Middleware darajasida markazlashtirilgan Exception Handling
## Topshiriq sharti:
Veb-so'rovlar konveyerida barcha xatoliklarni yagona nuqtada tutib oluvchi Exception Middleware simulyatsiyasi.

## Yechim (C# kodi):
```csharp
using System;

class XatolikMiddleware
{
    public void Invoke(Action keyingi)
    {
        try
        {
            keyingi();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[GLOBAL MIDDLEWARE]: Xatolik markazlashgan holda ushlandi: {ex.Message}");
            Console.WriteLine("[GLOBAL MIDDLEWARE]: Mijozga 500 Internal Server Error qaytarildi.");
        }
    }
}

internal class Program
{
    static void Main()
    {
        var middleware = new XatolikMiddleware();

        middleware.Invoke(() =>
        {
            Console.WriteLine("Controller kodi bajarilmoqda...");
            throw new Exception("Bazada kutilmagan nosozlik!");
        });
    }
}

```

## Tushuntirish va Mantiq:
Har bir Controller yoki metod ichida `try-catch` yozish o'rniga, ASP.NET Core da markazlashtirilgan Exception Middleware (yoki `IExceptionHandler`) o'rnatiladi.

## Ishlash natijasi:
```text
Controller kodi bajarilmoqda...
[GLOBAL MIDDLEWARE]: Xatolik markazlashgan holda ushlandi: Bazada kutilmagan nosozlik!
[GLOBAL MIDDLEWARE]: Mijozga 500 Internal Server Error qaytarildi.
```

# 435-Topshiriq: Xavfsizlik: Xatoliklarda maxfiy ma'lumotlarni ko'rsatmaslik
## Topshiriq sharti:
Foydalanuvchiga faqat xavfsiz xabar berish va haqiqiy xatoni ichki logda saqlash.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void BazagaUlansin(string parol)
    {
        try
        {
            throw new Exception($"Ulanish xatosi: Parol='{parol}' bilan serverga ulanib bo'lmadi.");
        }
        catch (Exception ex)
        {
            // Ichki tizimga to'liq log
            Console.WriteLine($"[ICHKI MAXFIY LOG]: {ex.Message}");

            // Tashqariga esa xavfsiz umumiy xabar
            Console.WriteLine("[MIJOZGA KO'RSATILADI]: Tizimda nosozlik yuz berdi. Iltimos keyinroq urinib ko'ring.");
        }
    }

    static void Main()
    {
        BazagaUlansin("SuperSecretPass123!");
    }
}

```

## Tushuntirish va Mantiq:
Kiberxavfsizlik talablariga binoan, foydalanuvchiga aslo server yo'llari, ma'lumotlar bazasi parollari yoki StackTrace ko'rsatilmasligi kerak (Information Disclosure zaifligi).

## Ishlash natijasi:
```text
[ICHKI MAXFIY LOG]: Ulanish xatosi: Parol='SuperSecretPass123!' bilan serverga ulanib bo'lmadi.
[MIJOZGA KO'RSATILADI]: Tizimda nosozlik yuz berdi. Iltimos keyinroq urinib ko'ring.
```

# 436-Topshiriq: async void metodlarda istisno xavfi (Nega async Task ishlatish kerak?)
## Topshiriq sharti:
`async void` metodlardagi xatolikni `try-catch` bilan ushlab bo'lmasligi va dasturni qulatishi sababini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        Console.WriteLine("async void xavflari:");
        Console.WriteLine("1. async void chaqiruvchini kuttira olmaydi (await qilib bo'lmaydi).");
        Console.WriteLine("2. async void ichidagi istisno SynchronizationContext ga borib tushadi va dasturni qulatadi!");
        Console.WriteLine("Qoida: Faqat UI hodisalaridan (Event Handlers) tashqari barcha joyda 'async Task' ishlatilishi shart!");
    }
}

```

## Tushuntirish va Mantiq:
`async void` metodlardan `Task` obyekti qaytmagani sababli chaqiruvchi kod uning xatolarini `try-catch` bloki bilan tuta olmaydi. Shuning uchun barcha asinxron metodlar `async Task` bo'lishi shart.

## Ishlash natijasi:
```text
async void xavflari:
1. async void chaqiruvchini kuttira olmaydi (await qilib bo'lmaydi).
2. async void ichidagi istisno SynchronizationContext ga borib tushadi va dasturni qulatadi!
Qoida: Faqat UI hodisalaridan (Event Handlers) tashqari barcha joyda 'async Task' ishlatilishi shart!
```

# 437-Topshiriq: Task.WhenAll da bir nechta istisnolarni to'liq ushlash
## Topshiriq sharti:
Oddiy `await Task.WhenAll` faqat birinchi xatoni otishi, barcha xatolarni ko'rish uchun `Task.Exception` ni tekshirish kerakligini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static async Task Main()
    {
        var t1 = Task.FromException(new ArgumentException("1-xatolik"));
        var t2 = Task.FromException(new InvalidOperationException("2-xatolik"));

        Task barchasi = Task.WhenAll(t1, t2);

        try
        {
            await barchasi;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"await faqat 1-xatoni ko'rsatadi: {ex.Message}");
        }

        // Barcha xatolarni to'liq ko'rish uchun:
        if (barchasi.Exception != null)
        {
            Console.WriteLine($"Haqiqiy jami xatolar soni: {barchasi.Exception.InnerExceptions.Count}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`await` kalit so'zi qulaylik uchun `AggregateException` ni ochib, uning faqat birinchi ichki xatosini qaytaradi. Agar barcha xatolar kerak bo'lsa, `Task.Exception.InnerExceptions` ga murojaat qilish lozim.

## Ishlash natijasi:
```text
await faqat 1-xatoni ko'rsatadi: 1-xatolik
Haqiqiy jami xatolar soni: 2
```

# 438-Topshiriq: Validatsiya xatolarini to'plash: Notification Pattern
## Topshiriq sharti:
Har bir xatoda darhol Exception otmasdan, barcha xatolarni bitta ro'yxatga to'plab qaytarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

class XatoliklarXaltasi
{
    public List<string> Xatolar { get; } = new();
    public bool XatoBormi => Xatolar.Count > 0;

    public void Qosh(string xato) => Xatolar.Add(xato);
}

internal class Program
{
    static void Main()
    {
        var xalta = new XatoliklarXaltasi();

        string ism = "";
        int yosh = -2;

        if (string.IsNullOrWhiteSpace(ism)) xalta.Qosh("Ism bo'sh bo'lishi mumkin emas!");
        if (yosh < 0) xalta.Qosh("Yosh noldan kichik bo'lishi mumkin emas!");

        if (xalta.XatoBormi)
        {
            Console.WriteLine($"Validatsiya xatoliklari ({xalta.Xatolar.Count} ta):");
            foreach (var x in xalta.Xatolar) Console.WriteLine($"- {x}");
        }
    }
}

```

## Tushuntirish va Mantiq:
Foydalanuvchi anketani to'ldirayotganda bittadan xato otish o'rniga, Notification Pattern orqali barcha xatolarni bir vaqtda to'plab ko'rsatish ancha qulaydir.

## Ishlash natijasi:
```text
Validatsiya xatoliklari (2 ta):
- Ism bo'sh bo'lishi mumkin emas!
- Yosh noldan kichik bo'lishi mumkin emas!
```

# 439-Topshiriq: Exception vs Result: Qachon qaysi birini ishlatish kerak?
## Topshiriq sharti:
Tizimli favqulodda avariyalar bilan kutilgan biznes qoidalari farqini tahlil qilish.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        Console.WriteLine("=== XATOLIKLAR STRATEGIYASI ===");
        Console.WriteLine("1. EXCEPTIONS (Istisnolar):");
        Console.WriteLine("   - Kutilmagan, favqulodda texnik avariyalar uchun (Baza uzildi, Disk to'ldi, NullReference).");
        Console.WriteLine("2. RESULTS (Natija modeli):");
        Console.WriteLine("   - Biznes mantiqining kutilgan xatoliklari uchun (Mablag' yetarli emas, Parol noto'g'ri, Mahsulot qolmagan).");
    }
}

```

## Tushuntirish va Mantiq:
Ushbu qoida dasturiy arxitekturani toza, tezkor va barqaror qiladi. Istisnolarni biznes mantiqini boshqarish uchun suiiste'mol qilish qat'iyan man etiladi.

## Ishlash natijasi:
```text
=== XATOLIKLAR STRATEGIYASI ===
1. EXCEPTIONS (Istisnolar):
   - Kutilmagan, favqulodda texnik avariyalar uchun (Baza uzildi, Disk to'ldi, NullReference).
2. RESULTS (Natija modeli):
   - Biznes mantiqining kutilgan xatoliklari uchun (Mablag' yetarli emas, Parol noto'g'ri, Mahsulot qolmagan).
```

# 440-Topshiriq: Korporativ darajadagi bazaviy istisno sinfi: AppException
## Topshiriq sharti:
Barcha domen xatolari uchun yagona ota sinf va xatolik kodi (ErrorCode) tizimini quring.

## Yechim (C# kodi):
```csharp
using System;

public abstract class AppException : Exception
{
    public string XatoKodi { get; }

    protected AppException(string kod, string xabar) : base(xabar)
    {
        XatoKodi = kod;
    }
}

public class MijozTopilmadiException : AppException
{
    public MijozTopilmadiException(int id)
        : base("ERR_CUSTOMER_NOT_FOUND", $"ID {id} bo'lgan mijoz topilmadi.") { }
}

internal class Program
{
    static void Main()
    {
        try
        {
            throw new MijozTopilmadiException(77);
        }
        catch (AppException ex)
        {
            Console.WriteLine($"Kodi: {ex.XatoKodi}");
            Console.WriteLine($"Xabar: {ex.Message}");
        }
    }
}

```

## Tushuntirish va Mantiq:
Katta korporativ tizimlarda barcha shaxsiy istisnolar yagona `AppException` dan o'sib chiqadi. Bu ularni tizimli avariyalardan (CLR exceptions) oson ajratib olish imkonini beradi.

## Ishlash natijasi:
```text
Kodi: ERR_CUSTOMER_NOT_FOUND
Xabar: ID 77 bo'lgan mijoz topilmadi.
```

# 441-Topshiriq: Tranzaksiyalarda xatolik yuz berganda avtomatik Rollback
## Topshiriq sharti:
Amallardan biri qulaganda barcha avvalgi o'zgarishlarni bekor qiluvchi xavfsiz tranzaksiya mantiqi.

## Yechim (C# kodi):
```csharp
using System;

class Hisob
{
    public decimal Balans = 100000m;
}

internal class Program
{
    static void PulOtkaz(Hisob manba, Hisob maqsad, decimal summa)
    {
        decimal eskiManba = manba.Balans;
        decimal eskiMaqsad = maqsad.Balans;

        try
        {
            manba.Balans -= summa;
            // 2-bosqichda kutilmagan xatolik yuz berdi:
            throw new InvalidOperationException("Tarmoq uzildi!");
            // maqsad.Balans += summa;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[TRANZAKSIYA XATOSI]: {ex.Message}");
            // Rollback (Ortga qaytarish)
            manba.Balans = eskiManba;
            maqsad.Balans = eskiMaqsad;
            Console.WriteLine("Rollback bajarildi: Pullar joyiga qaytarildi.");
        }
    }

    static void Main()
    {
        var h1 = new Hisob();
        var h2 = new Hisob();

        PulOtkaz(h1, h2, 50000m);
        Console.WriteLine($"Yakuniy h1 balans: {h1.Balans:N0} so'm");
    }
}

```

## Tushuntirish va Mantiq:
Tranzaksiya yaxlitligi (ACID) qoidasiga binoan, agar birorta qadam xato bilan tugasa, butun tizim boshlang'ich holatiga qaytarilishi (Rollback) shart.

## Ishlash natijasi:
```text
[TRANZAKSIYA XATOSI]: Tarmoq uzildi!
Rollback bajarildi: Pullar joyiga qaytarildi.
Yakuniy h1 balans: 100,000 so'm
```

# 442-Topshiriq: Idempotent xatoliklarni qayta ishlash tamoyili
## Topshiriq sharti:
So'rov takroran yuborilganda ikkinchi marta pul yechilmasligi yoki xatolik bermasligini ta'minlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

class IdempotentTolovServisi
{
    private readonly HashSet<string> bajarilganlar = new();

    public void Tolov(string tranzaksiyaId, decimal summa)
    {
        if (bajarilganlar.Contains(tranzaksiyaId))
        {
            Console.WriteLine($"[IDEMPOTENT]: {tranzaksiyaId} allaqachon bajarilgan, qayta pul yechilmaydi.");
            return;
        }

        bajarilganlar.Add(tranzaksiyaId);
        Console.WriteLine($"To'lov amalga oshirildi: {summa:N0} so'm (ID: {tranzaksiyaId})");
    }
}

internal class Program
{
    static void Main()
    {
        var servis = new IdempotentTolovServisi();
        servis.Tolov("TX_1001", 50000);
        servis.Tolov("TX_1001", 50000); // Tarmoq takroriy so'rovi
    }
}

```

## Tushuntirish va Mantiq:
Tarmoq uzilishlari tufayli mijoz so'rovni qayta yuborishi mumkin. Idempotentlik printsipi xatolikdan keyingi takroriy so'rovlar tizimni buzmasligini ta'minlaydi.

## Ishlash natijasi:
```text
To'lov amalga oshirildi: 50,000 so'm (ID: TX_1001)
[IDEMPOTENT]: TX_1001 allaqachon bajarilgan, qayta pul yechilmaydi.
```

# 443-Topshiriq: Timeout bilan Deadlock xatolaridan qutulish
## Topshiriq sharti:
Resurslarni cheksiz kutib to'xtab qolmaslik uchun `Monitor.TryEnter` da timeout ishlatish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    static readonly object qulf = new();

    static void Main()
    {
        // 100 ms kutish, agar qulf bo'shamasasa xatolik qaytarish
        bool qulflanadi = Monitor.TryEnter(qulf, TimeSpan.FromMilliseconds(100));

        if (qulflanadi)
        {
            try
            {
                Console.WriteLine("Qulf xavfsiz olindi.");
            }
            finally
            {
                Monitor.Exit(qulf);
            }
        }
        else
        {
            Console.WriteLine("Timeout: Resurs band bo'lgani sababli kutish to'xtatildi (Deadlock dan qochildi).");
        }
    }
}

```

## Tushuntirish va Mantiq:
Doimiy `lock` (cheksiz kutish) o'rniga timeout li `TryEnter` ishlatish tizimning bir-birini kutib butunlay to'xtab qolishining (Deadlock) oldini oladi.

## Ishlash natijasi:
```text
Qulf xavfsiz olindi.
```

# 444-Topshiriq: Performance: Istisno otish narxi (Exception vs Bool Benchmark)
## Topshiriq sharti:
Nega istisnolarni faqat kritik holatlar uchun saqlash kerakligini raqamlar bilan tushuntirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Diagnostics;

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Unumdorlik taqqoslash:");
        Console.WriteLine("- 'int.TryParse' (Bool qaytarish): ~1-2 nanosaniya, 0 bayt GC xotira.");
        Console.WriteLine("- 'int.Parse + catch' (Istisno otish): ~5,000 - 10,000 nanosaniya (5000 barobar sekin!).");
        Console.WriteLine("Xulosa: Oddiy mantiqiy holatlarda istisno otish tizim tezligini falaj qiladi.");
    }
}

```

## Tushuntirish va Mantiq:
Istisno otilganda OS yadrosi bilan muloqot, StackTrace matnini yig'ish, metadata qidirish va xotira ajratish ro'y beradi. Bu oddiy `if-else` ga nisbatan minglab barobar ko'p resurs yeydi.

## Ishlash natijasi:
```text
Unumdorlik taqqoslash:
- 'int.TryParse' (Bool qaytarish): ~1-2 nanosaniya, 0 bayt GC xotira.
- 'int.Parse + catch' (Istisno otish): ~5,000 - 10,000 nanosaniya (5000 barobar sekin!).
Xulosa: Oddiy mantiqiy holatlarda istisno otish tizim tezligini falaj qiladi.
```

# 445-Topshiriq: C# 11 statik Throw yordamchi metodlari
## Topshiriq sharti:
`ArgumentNullException.ThrowIfNull` ning JIT optimallashuvi va kodni kichraytirishi.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Metod(string? matn)
    {
        ArgumentNullException.ThrowIfNull(matn);
        Console.WriteLine($"Matn uzunligi: {matn.Length}");
    }

    static void Main()
    {
        Metod("C# 11");
    }
}

```

## Tushuntirish va Mantiq:
Eski `if (x == null) throw ...` usuli har bir metod ichiga og'ir IL kod qo'shardi va Inlining ni qiyinlashtirardi. Yangi statik `ThrowIfNull` metodi chaqiruvchi metodni ixcham saqlaydi va JIT inline qilishini osonlashtiradi.

## Ishlash natijasi:
```text
Matn uzunligi: 5
```

# 446-Topshiriq: Deep InnerException Flattening: Barcha ichki xatolarni ajratish
## Topshiriq sharti:
Chuqur zanjirlangan istisnolarning barcha `InnerException` larini to'liq chiqaruvchi rekursiv yordamchi metod.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void BarchaXatolarniChiqar(Exception? ex)
    {
        while (ex != null)
        {
            Console.WriteLine($"-> {ex.GetType().Name}: {ex.Message}");
            ex = ex.InnerException;
        }
    }

    static void Main()
    {
        var e1 = new InvalidOperationException("Baza ulanishi yo'q");
        var e2 = new ArgumentException("Mijoz ma'lumotlari xato", e1);
        var e3 = new Exception("Yuqori darajadagi buyurtma xatosi", e2);

        BarchaXatolarniChiqar(e3);
    }
}

```

## Tushuntirish va Mantiq:
Ushbu rekursiv usul murakkab server xatoliklarida har bir qatlamning sabablarini yuqoridan to quyi apparat darajasigacha to'liq ko'rish imkonini beradi.

## Ishlash natijasi:
```text
-> Exception: Yuqori darajadagi buyurtma xatosi
-> ArgumentException: Mijoz ma'lumotlari xato
-> InvalidOperationException: Baza ulanishi yo'q
```

# 447-Topshiriq: Parallel.ForEach da xatoliklarni xavfsiz boshqarish
## Topshiriq sharti:
Ko'p oqimli `Parallel.ForEach` siklida xatoliklarni to'plash.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Concurrent;
using System.Threading.Tasks;

internal class Program
{
    static void Main()
    {
        int[] sonlar = [ 10, 0, 5, 0, 20 ];
        var xatolar = new ConcurrentBag<string>();

        Parallel.ForEach(sonlar, son =>
        {
            try
            {
                int natija = 100 / son;
            }
            catch (DivideByZeroException)
            {
                xatolar.Add($"0 ga bo'lish xatosi ushlandi (Thread #{Environment.CurrentManagedThreadId})");
            }
        });

        Console.WriteLine($"Jami ushlangan xatolar: {xatolar.Count} ta");
    }
}

```

## Tushuntirish va Mantiq:
`ConcurrentBag<string>` oqimlararo xavfsiz bo'lib, parallel siklda yuz bergan har qanday istisnolar ro'yxatini boshqa oqimlarni to'xtatmasdan to'plashga imkon beradi.

## Ishlash natijasi:
```text
Jami ushlangan xatolar: 2 ta
```

# 448-Topshiriq: Custom Exception da JSON formatida xatolik qaytarish
## Topshiriq sharti:
Xatolik obyektini to'g'ridan-to'g'ri JSON ko'rinishida formatlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Text.Json;

class ValidatsiyaXatosi : Exception
{
    public string Maydon { get; }

    public ValidatsiyaXatosi(string maydon, string xabar) : base(xabar)
    {
        Maydon = maydon;
    }

    public string ToJson() => JsonSerializer.Serialize(new
    {
        Xato = Message,
        Maydon = Maydon,
        Sana = DateTime.UtcNow
    });
}

internal class Program
{
    static void Main()
    {
        var ex = new ValidatsiyaXatosi("Email", "Email formati noto'g'ri");
        Console.WriteLine(ex.ToJson());
    }
}

```

## Tushuntirish va Mantiq:
API arxitekturasida bunday metodlar xatolik yuz berganda uni to'g'ridan-to'g'ri HTTP javobiga (JSON body) chiqarishni nihoyatda osonlashtiradi.

## Ishlash natijasi:
```text
{"Xato":"Email formati noto'g'ri","Maydon":"Email","Sana":"2026-11-08T00:00:00"}
```

# 449-Topshiriq: UnobservedTaskException: E'tiborsiz qolgan asinxron xatoliklar
## Topshiriq sharti:
`await` qilinmagan fon vazifalaridagi xatoliklarni ushlab qoluvchi hodisa.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static void Main()
    {
        TaskScheduler.UnobservedTaskException += (sender, e) =>
        {
            Console.WriteLine("[UNOBSERVED EXCEPTION]: Fon vazifasida xatolik ushlandi!");
            e.SetObserved(); // Jarayon qulashini bekor qilish
        };

        Console.WriteLine("UnobservedTaskException xavfsizlik registratsiyasi bajarildi.");
    }
}

```

## Tushuntirish va Mantiq:
Agar Task `await` qilinmasa va unda xatolik chiqsa, Garbage Collector ushbu taskni tozalayotganda `UnobservedTaskException` chaqiriladi. `SetObserved()` dasturning avariya bilan yopilishini to'xtatadi.

## Ishlash natijasi:
```text
UnobservedTaskException xavfsizlik registratsiyasi bajarildi.
```

# 450-Topshiriq: Xatoliklar va Istisnolar bo'limi integratsiyalashgan arxitekturasi
## Topshiriq sharti:
`Result<T>`, `try-catch-finally`, `using var`, `Exception Filter` va maxsus domen istisnolarini birlashtirgan to'liq xavfsiz to'lov tizimini yakunlang.

## Yechim (C# kodi):
```csharp
using System;

public readonly record struct Result<T>(bool IsSuccess, T? Value, string? Error)
{
    public static Result<T> Success(T val) => new(true, val, null);
    public static Result<T> Fail(string err) => new(false, default, err);
}

class BankTranzaksiyasi : IDisposable
{
    public void Dispose() => Console.WriteLine("[DISPOSE]: Bank ulanishi xavfsiz yopildi.");
}

internal class Program
{
    static Result<decimal> MablagOtkaz(decimal balans, decimal summa)
    {
        if (summa <= 0) return Result<decimal>.Fail("Summa musbat bo'lishi shart!");
        if (summa > balans) return Result<decimal>.Fail("Yetarli mablag' mavjud emas.");

        try
        {
            using var ulanish = new BankTranzaksiyasi();
            decimal qolgan = balans - summa;
            return Result<decimal>.Success(qolgan);
        }
        catch (Exception ex) when (ex is not OutOfMemoryException)
        {
            return Result<decimal>.Fail($"Tranzaksiya texnik xatosi: {ex.Message}");
        }
    }

    static void Main()
    {
        var r1 = MablagOtkaz(100000m, 30000m);
        Console.WriteLine($"Muvaffaqiyatli: {r1.IsSuccess}, Yangi balans: {r1.Value:N0} so'm
");

        var r2 = MablagOtkaz(100000m, 150000m);
        Console.WriteLine($"Muvaffaqiyatli: {r2.IsSuccess}, Xato: {r2.Error}");
    }
}

```

## Tushuntirish va Mantiq:
Ushbu integratsiyalashgan yechim zamonaviy .NET ning barcha ishonchlilik tamoyillarini o'z ichiga oladi: kutilgan xatolarda Result, resurslar tozalanishida `using var`, texnik xatolarda xavfsiz `catch` va filtrlar.

## Ishlash natijasi:
```text
[DISPOSE]: Bank ulanishi xavfsiz yopildi.
Muvaffaqiyatli: True, Yangi balans: 70,000 so'm

Muvaffaqiyatli: False, Xato: Yetarli mablag' mavjud emas.
```

