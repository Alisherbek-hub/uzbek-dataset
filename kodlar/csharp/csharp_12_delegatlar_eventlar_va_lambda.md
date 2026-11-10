# 12-Mavzu: Delegatlar, Eventlar va Lambda Ifodalari (551-600)

Ushbu bo'limda C# tilining funksional asosi bo'lgan delegatlar: `delegate`, `MulticastDelegate`, `Action`, `Func`, `Predicate`, anonim metodlar, lambda ifodalari, yopilishlar (Closures) va kompilyatorning `DisplayClass` mexanizmi, xotira ajratmasdan ishlovchi `static` lambdalar, hodisalar (`event`), `EventHandler<T>`, maxsus `add/remove` accessorlar, eventlar sababli xotira oqishi (Memory Leaks) hamda C# 10/11/12 zamonaviy lambda xususiyatlari bo'yicha 50 ta amaliy topshiriq jamlangan.

# 551-Topshiriq: Delegat Asoslari: Funksiyalarga Xavfsiz Ko'rsatkich (Type-Safe Function Pointer)
## Topshiriq sharti:
Oddiy delegat e'lon qiling va uni turli metodlarga bog'lang.

## Yechim (C# kodi):
```csharp
using System;

// Delegat signaturasi: int qabul qilib, int qaytaradi
delegate int MatematikAmal(int x);

internal class Program
{
    static int Kvadrat(int son) => son * son;
    static int Kub(int son) => son * son * son;

    static void Main()
    {
        MatematikAmal amal = Kvadrat;
        Console.WriteLine($"5 ning kvadrati: {amal(5)}");

        amal = Kub;
        Console.WriteLine($"5 ning kubi: {amal(5)}");
    }
}

```

## Tushuntirish va Mantiq:
Delegat C/C++ dagi funksiya ko'rsatkichlarining (function pointers) .NET CLR dagi to'liq tip-xavfsiz va obyektga yo'naltirilgan ko'rinishidir.

## Ishlash natijasi:
```text
5 ning kvadrati: 25
5 ning kubi: 125
```

# 552-Topshiriq: MulticastDelegate va Zanjirli Chaqiruv (`+=` va `-=`)
## Topshiriq sharti:
Bitta delegat orqali ketma-ket bir nechta metodlarni chaqirish.

## Yechim (C# kodi):
```csharp
using System;

delegate void Bildirishnoma(string xabar);

internal class Program
{
    static void KonsolgaChop(string xabar) => Console.WriteLine($"[Konsol]: {xabar}");
    static void FaylgaYoz(string xabar) => Console.WriteLine($"[Fayl]: {xabar}");

    static void Main()
    {
        Bildirishnoma xabarTarqatuvchi = KonsolgaChop;
        xabarTarqatuvchi += FaylgaYoz;

        Console.WriteLine("--- Ikkita metod chaqiriladi ---");
        xabarTarqatuvchi("Tizim yangilandi");

        xabarTarqatuvchi -= KonsolgaChop;
        Console.WriteLine("--- Bitta metod qoldi ---");
        xabarTarqatuvchi("Xatolik aniqlandi");
    }
}

```

## Tushuntirish va Mantiq:
C# dagi har qanday delegat aslida `System.MulticastDelegate` dan meros oladi va ichki chaqiruv ro'yxatida (invocation list) bir nechta metodlarni zanjir qilib saqlay oladi.

## Ishlash natijasi:
```text
--- Ikkita metod chaqiriladi ---
[Konsol]: Tizim yangilandi
[Fayl]: Tizim yangilandi
--- Bitta metod qoldi ---
[Fayl]: Xatolik aniqlandi
```

# 553-Topshiriq: MulticastDelegate.GetInvocationList() orqali Xavfsiz Qaytarish
## Topshiriq sharti:
Qiymat qaytaruvchi multicast delegatlarda barcha natijalarni to'plash.

## Yechim (C# kodi):
```csharp
using System;

delegate int SonHisoblagich(int x);

internal class Program
{
    static int IkkiKarra(int a) => a * 2;
    static int UchKarra(int a) => a * 3;

    static void Main()
    {
        SonHisoblagich hisob = IkkiKarra;
        hisob += UchKarra;

        // Oddiy chaqiruv faqat oxirgi metod natijasini beradi:
        Console.WriteLine($"Oddiy chaqiriq natijasi: {hisob(10)}");

        // Har bir metod natijasini alohida olish:
        Console.WriteLine("Har bir metodning natijalari:");
        foreach (Delegate d in hisob.GetInvocationList())
        {
            int res = (int)d.DynamicInvoke(10)!;
            Console.WriteLine($"- Natija: {res}");
        }
    }
}

```

## Tushuntirish va Mantiq:
Agar multicast delegat qiymat qaytarsa, to'g'ridan-to'g'ri chaqiruv faqat ro'yxatdagi eng oxirgi chaqirilgan metod natijasini qaytaradi. Barcha natijalarni olish uchun `GetInvocationList()` ishlatiladi.

## Ishlash natijasi:
```text
Oddiy chaqiriq natijasi: 30
Har bir metodning natijalari:
- Natija: 20
- Natija: 30
```

# 554-Topshiriq: Delegate.Target va Method Xususiyatlari
## Topshiriq sharti:
Delegat qaysi obyekt instansiyasiga va qaysi metodga bog'langanligini ko'rish.

## Yechim (C# kodi):
```csharp
using System;

class Xodim
{
    public string Ism { get; set; } = "Jamshid";
    public void Salomlash() => Console.WriteLine($"Salom, men {Ism}man.");
}

internal class Program
{
    static void Main()
    {
        var x = new Xodim();
        Action salom = x.Salomlash;

        Console.WriteLine($"Obyekt turi (Target): {salom.Target?.GetType().Name}");
        Console.WriteLine($"Metod nomi (Method): {salom.Method.Name}");
    }
}

```

## Tushuntirish va Mantiq:
Agar metod instansiya metodi bo'lsa, `Target` shu obyektga havola saqlaydi; statik metodlar uchun `Target` `null` bo'ladi.

## Ishlash natijasi:
```text
Obyekt turi (Target): Xodim
Metod nomi (Method): Salomlash
```

# 555-Topshiriq: Standart Delegat: Action va Action<T>
## Topshiriq sharti:
Hech qanday qiymat qaytarmaydigan (void) amallar uchun tayyor `Action` delegatlari.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        Action salom = () => Console.WriteLine("Salom Dunyo!");
        Action<string, int> malumot = (ism, yosh) => Console.WriteLine($"{ism} {yosh} yoshda.");

        salom();
        malumot("Nodir", 28);
    }
}

```

## Tushuntirish va Mantiq:
`Action` 0 tadan 16 tagacha parametr qabul qiluvchi va hech qanday qiymat qaytarmaydigan tayyor generik delegatdir.

## Ishlash natijasi:
```text
Salom Dunyo!
Nodir 28 yoshda.
```

# 556-Topshiriq: Standart Delegat: Func<TResult> va Func<T, TResult>
## Topshiriq sharti:
Natija qaytaruvchi barcha funksiyalar uchun standart `Func` delegati.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        Func<int, int, int> qoshish = (a, b) => a + b;
        Func<string, int> uzunlik = matn => matn.Length;

        Console.WriteLine($"5 + 7 = {qoshish(5, 7)}");
        Console.WriteLine($"'O'zbekiston' uzunligi: {uzunlik("O'zbekiston")}");
    }
}

```

## Tushuntirish va Mantiq:
`Func` delegatining eng oxirgi tipi har doim qaytish turini (`TResult`) bildiradi.

## Ishlash natijasi:
```text
5 + 7 = 12
'O'zbekiston' uzunligi: 11
```

# 557-Topshiriq: Standart Delegat: Predicate<T>
## Topshiriq sharti:
Shartni tekshirib, `bool` qaytaruvchi predikat delegati.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        Predicate<int> juftmi = son => son % 2 == 0;
        Predicate<string> boshmi = string.IsNullOrWhiteSpace;

        Console.WriteLine($"14 juftmi: {juftmi(14)}");
        Console.WriteLine($"15 juftmi: {juftmi(15)}");
        Console.WriteLine($"'   ' bo'shmi: {boshmi("   ")}");
    }
}

```

## Tushuntirish va Mantiq:
`Predicate<T>` aslida `Func<T, bool>` ga teng bo'lib, filtrlash va qidirish amallarida maxsus semantik nom sifatida xizmat qiladi.

## Ishlash natijasi:
```text
14 juftmi: True
15 juftmi: False
'   ' bo'shmi: True
```

# 558-Topshiriq: Anonim Metodlar (Anonymous Methods - delegate kalit so'zi)
## Topshiriq sharti:
Lambda ifodalardan oldingi C# 2.0 sintaksisi va uning xususiyatlari.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        // C# 2.0 anonim metod sintaksisi:
        Func<int, int, int> kopaytma = delegate (int a, int b)
        {
            return a * b;
        };

        Console.WriteLine($"Kopaytma: {kopaytma(6, 7)}");
    }
}

```

## Tushuntirish va Mantiq:
Anonim metodlar C# 2.0 da kiritilgan bo'lib, alohida nomlangan metod yaratmasdan joyida blok kod yozish imkonini bergan. C# 3.0 dan boshlab lambda ifodalari ularning o'rnini egalladi.

## Ishlash natijasi:
```text
Kopaytma: 42
```

# 559-Topshiriq: Expression Lambda (=>) va Statement Lambda Farqi
## Topshiriq sharti:
Bitta qatordan iborat ifodali va blokli ko'p qatorli lambdalar.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        // Expression lambda (bitta ifoda, return yozilmaydi):
        Func<int, int> kv = x => x * x;

        // Statement lambda (jingalak qavslar ichida to'liq blok):
        Func<int, string> bahola = ball =>
        {
            if (ball >= 90) return "A'lo";
            if (ball >= 70) return "Yaxshi";
            return "Qoniqarli";
        };

        Console.WriteLine($"Kv: {kv(4)}");
        Console.WriteLine($"Baho: {bahola(85)}");
    }
}

```

## Tushuntirish va Mantiq:
Expression lambda darhol ifoda qiymatini qaytaradi va Expression Tree ga aylantirilishi mumkin. Statement lambda esa to'liq bayonotlar blokidan iborat bo'ladi.

## Ishlash natijasi:
```text
Kv: 16
Baho: Yaxshi
```

# 560-Topshiriq: Yopilishlar (Closures) va Kompilyatorning DisplayClass Mexanizmi
## Topshiriq sharti:
Lambda tashqi lokal o'zgaruvchini qamrab olganda (capture) xotirada nima yuz beradi.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static Func<int> HisoblagichYarat()
    {
        int hisob = 0; // Tashqi lokal o'zgaruvchi

        // Lambda 'hisob' ni o'z ichiga qamrab oladi (capture):
        return () =>
        {
            hisob++;
            return hisob;
        };
    }

    static void Main()
    {
        Func<int> counter1 = HisoblagichYarat();
        Console.WriteLine(counter1());
        Console.WriteLine(counter1());

        Func<int> counter2 = HisoblagichYarat();
        Console.WriteLine(counter2());
    }
}

```

## Tushuntirish va Mantiq:
Kompilyator kapture qilingan o'zgaruvchini saqlash uchun maxsus yashirin sinf (`<>c__DisplayClass`) yaratadi va o'zgaruvchini stackdan heap xotiraga ko'chiradi. Shuning uchun lokal o'zgaruvchi metod tugagandan keyin ham yashashda davom etadi.

## Ishlash natijasi:
```text
1
2
1
```

# 561-Topshiriq: Sikllar Ichidagi Closure Tuzog'i (Loop Variable Capture Trap)
## Topshiriq sharti:
Foreach va For sikllarida lambdalarni ro'yxatga yig'ishdagi farq.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        List<Action> harakatlar = new();

        for (int i = 0; i < 3; i++)
        {
            int nusxa = i; // Lokal nusxa olish
            harakatlar.Add(() => Console.Write($"{nusxa} "));
        }

        Console.Write("Natija: ");
        foreach (var act in harakatlar)
        {
            act();
        }
        Console.WriteLine();
    }
}

```

## Tushuntirish va Mantiq:
Agar sikl o'zgaruvchisi `i` to'g'ridan-to'g'ri kapture qilinsa, barcha delegatlar `i` ning eng oxirgi yakuniy qiymatini ko'rsatib qoladi. Har bir iteratsiyada lokal o'zgaruvchi yaratish bu xatoni bartaraf etadi.

## Ishlash natijasi:
```text
Natija: 0 1 2
```

# 562-Topshiriq: C# 9+ Static Lambdalar (Zero Memory Allocation)
## Topshiriq sharti:
Tasodifiy kapture va ortiqcha xotira ajratilishidan saqlovchi `static () =>` sintaksisi.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int tashqi = 10;

        // static lambdalar tashqi lokal o'zgaruvchilarni kapture qila olmaydi!
        // Func<int, int> xato = static x => x + tashqi; // KOMPILYATSIYA XATOSI!

        Func<int, int> toza = static x => x * 2;
        Console.WriteLine($"Toza natija: {toza(5)}");
    }
}

```

## Tushuntirish va Mantiq:
`static` lambdalar heap xotirada DisplayClass obyektini yaratishni mutlaqo taqiqlaydi va GC bosimini nolga tushiradi.

## Ishlash natijasi:
```text
Toza natija: 10
```

# 563-Topshiriq: C# 10+ Lambdalarda Aniq Qaytish Turi (Explicit Return Types)
## Topshiriq sharti:
Kompilyator tur aniqlashda ikkilangan paytda qaytish turini aniq ko'rsatish.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        // Aniq 'object' qaytarish turi ko'rsatilgan:
        var tanla = object (bool bayroq) => bayroq ? 100 : "Salom";

        Console.WriteLine($"1: {tanla(true)} (Turi: {tanla(true).GetType().Name})");
        Console.WriteLine($"2: {tanla(false)} (Turi: {tanla(false).GetType().Name})");
    }
}

```

## Tushuntirish va Mantiq:
C# 10 dan boshlab lambda oldidan qaytish turi yozilishi mumkin (`object (...) => ...`), bu var bilan birga turlarni aniq boshqarish imkonini beradi.

## Ishlash natijasi:
```text
1: 100 (Turi: Int32)
2: Salom (Turi: String)
```

# 564-Topshiriq: C# 11+ Lambdalarda Standart Parametr Qiymatlari (Default Parameter Values)
## Topshiriq sharti:
Lambdalarga ixtiyoriy (optional) parametrlar berish imkoniyati.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        var salomlash = (string ism = "Mehmon") => $"Salom, {ism}!";

        Console.WriteLine(salomlash("Rustam"));
        Console.WriteLine(salomlash());
    }
}

```

## Tushuntirish va Mantiq:
C# 11 dan boshlab lambda parametrlariga standart boshlang'ich qiymat berish mumkin.

## Ishlash natijasi:
```text
Salom, Rustam!
Salom, Mehmon!
```

# 565-Topshiriq: C# 12 Lambdalarda `params` Massiv Parametrlari
## Topshiriq sharti:
O'zgaruvchan sondagi parametrlarni qabul qiluvchi zamonaviy lambda.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        var hisoblaYigindi = (params int[] sonlar) =>
        {
            int sum = 0;
            foreach (var s in sonlar) sum += s;
            return sum;
        };

        Console.WriteLine($"Yig'indi (1, 2, 3): {hisoblaYigindi(1, 2, 3)}");
        Console.WriteLine($"Yig'indi (10, 20): {hisoblaYigindi(10, 20)}");
    }
}

```

## Tushuntirish va Mantiq:
C# 12 lambdalarda `params` kalit so'zini qo'llab-quvvatlaydi, bu qulay chaqiruvlarni ta'minlaydi.

## Ishlash natijasi:
```text
Yig'indi (1, 2, 3): 6
Yig'indi (10, 20): 30
```

# 566-Topshiriq: Event Kalit So'zi: Delegat va Event O'rtasidagi Asosiy Farq
## Topshiriq sharti:
Nima uchun oddiy ochiq delegat maydonidan ko'ra `event` ishlatilishi shart?

## Yechim (C# kodi):
```csharp
using System;

class BankHisobi
{
    // Ochiq delegat emas, balki 'event':
    public event Action<decimal>? PulYechildi;

    public void Yechish(decimal summa)
    {
        PulYechildi?.Invoke(summa);
    }
}

internal class Program
{
    static void Main()
    {
        var hisob = new BankHisobi();
        hisob.PulYechildi += s => Console.WriteLine($"SMS: {s} so'm yechildi.");

        // hisob.PulYechildi = null; // KOMPILYATSIYA XATOSI! Boshqa obunachilarni o'chirib tashlay olmaydi!
        // hisob.PulYechildi(500);   // KOMPILYATSIYA XATOSI! Tashqaridan to'g'ridan-to'g'ri chaqirib bo'lmaydi!

        hisob.Yechish(50000);
    }
}

```

## Tushuntirish va Mantiq:
`event` kalit so'zi delegat ustiga inkapsulyatsiya qatlamini qo'yadi: tashqi kod faqat `+=` va `-=` amallarini bajara oladi, hodisani faqat e'lon qilgan sinfning o'zi chaqira oladi.

## Ishlash natijasi:
```text
SMS: 50000 so'm yechildi.
```

# 567-Topshiriq: Standart .NET Event Pattern: EventHandler va EventArgs
## Topshiriq sharti:
Framework tavsiyalariga 100% mos keluvchi standart hodisa namunasi.

## Yechim (C# kodi):
```csharp
using System;

class HaroratOzgardiArgs : EventArgs
{
    public double YangiHarorat { get; }
    public HaroratOzgardiArgs(double h) => YangiHarorat = h;
}

class Termometr
{
    public event EventHandler<HaroratOzgardiArgs>? HaroratOzgardi;

    public void Yangila(double h)
    {
        HaroratOzgardi?.Invoke(this, new HaroratOzgardiArgs(h));
    }
}

internal class Program
{
    static void Main()
    {
        var t = new Termometr();
        t.HaroratOzgardi += (sender, e) =>
        {
            Console.WriteLine($"[Ogohlantirish]: Harorat {e.YangiHarorat} gradusga yetdi.");
        };

        t.Yangila(38.5);
    }
}

```

## Tushuntirish va Mantiq:
Standart hodisa patterni `(object sender, TEventArgs e)` signaturasini talab qiladi va kengayish uchun qulaylik yaratadi.

## Ishlash natijasi:
```text
[Ogohlantirish]: Harorat 38.5 gradusga yetdi.
```

# 568-Topshiriq: Tegishli Hodisa O'chiruvchisi (Thread-Safe Event Invocation `?.Invoke`)
## Topshiriq sharti:
Ko'p oqimli muhitda NullReferenceException xavfisiz xavfsiz event chaqirish.

## Yechim (C# kodi):
```csharp
using System;

class Xizmat
{
    public event Action? IshBajarildi;

    public void Bajar()
    {
        // 1. Zamonaviy xavfsiz usul:
        IshBajarildi?.Invoke();

        // Bu usul fonda quyidagiga aylanadi (poygadan himoya):
        // Action? nusxa = IshBajarildi;
        // if (nusxa != null) nusxa();
    }
}

internal class Program
{
    static void Main()
    {
        var x = new Xizmat();
        x.IshBajarildi += () => Console.WriteLine("Xizmat muvaffaqiyatli yakunlandi.");
        x.Bajar();
    }
}

```

## Tushuntirish va Mantiq:
`?.Invoke()` sintaksisi delegat havolasini avval lokal o'zgaruvchiga nusxalaydi, bu esa boshqa oqim aynan shu vaqtda obunani bekor qilsa ham `NullReferenceException` oldini oladi.

## Ishlash natijasi:
```text
Xizmat muvaffaqiyatli yakunlandi.
```

# 569-Topshiriq: Maxsus Event Accessorlar (Custom add / remove)
## Topshiriq sharti:
Hodisaga obuna bo'lish va bekor qilish jarayonini loglash yoki nazorat qilish.

## Yechim (C# kodi):
```csharp
using System;

class SignalTizimi
{
    private Action? signalDelegati;

    public event Action Signal
    {
        add
        {
            Console.WriteLine("[Audit]: Yangi obunachi ulandi.");
            signalDelegati += value;
        }
        remove
        {
            Console.WriteLine("[Audit]: Obunachi o'chirildi.");
            signalDelegati -= value;
        }
    }

    public void Fire() => signalDelegati?.Invoke();
}

internal class Program
{
    static void Main()
    {
        var st = new SignalTizimi();
        Action tinglovchi = () => Console.WriteLine("Signal qabul qilindi!");

        st.Signal += tinglovchi;
        st.Fire();
        st.Signal -= tinglovchi;
    }
}

```

## Tushuntirish va Mantiq:
Custom event accessors propertylarning get/set bloklariga o'xshash bo'lib, obunachilar ro'yxatini to'liq nazorat qilish imkonini beradi.

## Ishlash natijasi:
```text
[Audit]: Yangi obunachi ulandi.
Signal qabul qilindi!
[Audit]: Obunachi o'chirildi.
```

# 570-Topshiriq: Eventlar Sababli Xotira Oqishi (Memory Leak via Event Subscription)
## Topshiriq sharti:
O'chirilmagan hodisa obunasi obyektni Garbage Collector dan qanday yashirishini tahlil qiling.

## Yechim (C# kodi):
```csharp
using System;

class YangiliklarNashriyoti
{
    public event Action? Yangilik;
    public void E'lonQilish() => Yangilik?.Invoke();
}

class O'quvchi
{
    public string Ism { get; }
    public O'quvchi(string ism, YangiliklarNashriyoti pub)
    {
        Ism = ism;
        pub.Yangilik += XabarOlish;
    }

    private void XabarOlish() => Console.WriteLine($"{Ism} yangilikni o'qidi.");
}

internal class Program
{
    static void Main()
    {
        var pub = new YangiliklarNashriyoti();
        var user = new O'quvchi("Aziz", pub);

        // 'user' ga boshqa havola qolmadi deb hisoblaymiz:
        user = null;
        GC.Collect();

        // LEKIN 'pub' ning delegat zanjirida 'user' ga havola (Target) yashayotgani sababli
        // user obyekti GC tomonidan tozalanmadi!
        pub.E'lonQilish();
    }
}

```

## Tushuntirish va Mantiq:
Uzoq yashovchi obyekt (Publisher) ning hodisasiga obuna bo'lgan qisqa yashovchi obyekt (Subscriber) obunasi bekor qilinmasa (`-=`), xotiradan tozalanmaydi va Memory Leak yuzaga keladi.

## Ishlash natijasi:
```text
Aziz yangilikni o'qidi.
```

# 571-Topshiriq: IDisposable bilan Hodisalarni Xavfsiz Bekor Qilish (Unsubscribe Pattern)
## Topshiriq sharti:
Rx uslubida `IDisposable` orqali toza obunani yakunlash.

## Yechim (C# kodi):
```csharp
using System;

class Kanal
{
    public event Action? Xabar;

    public IDisposable ObunaBol(Action harakat)
    {
        Xabar += harakat;
        return new ObunaTugatuvchi(() => Xabar -= harakat);
    }

    public void Yubor() => Xabar?.Invoke();

    private class ObunaTugatuvchi : IDisposable
    {
        private Action? bekorQilish;
        public ObunaTugatuvchi(Action b) => bekorQilish = b;
        public void Dispose()
        {
            bekorQilish?.Invoke();
            bekorQilish = null;
        }
    }
}

internal class Program
{
    static void Main()
    {
        var kanal = new Kanal();
        using (kanal.ObunaBol(() => Console.WriteLine("Xabar yetib keldi!")))
        {
            kanal.Yubor();
        } // using bloki tugashi bilan obuna avtomatik o'chiriladi!

        Console.WriteLine("Obuna tugatildi:");
        kanal.Yubor(); // Hech narsa chiqmaydi
    }
}

```

## Tushuntirish va Mantiq:
IDisposable orqali obunani boshqarish Reactive Extensions (Rx) va zamonaviy arxitekturalarda eng toza va xavfsiz naqsh hisoblanadi.

## Ishlash natijasi:
```text
Xabar yetib keldi!
Obuna tugatildi:
```

# 572-Topshiriq: Funksional Kompozitsiya: Delegatlarni Birlashtirish (Function Composition)
## Topshiriq sharti:
Matematik $f(g(x))$ kompozitsiyasini generik delegat bilan yaratish.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static Func<T, TResult> Birlashtir<T, TMid, TResult>(Func<T, TMid> f1, Func<TMid, TResult> f2)
    {
        return x => f2(f1(x));
    }

    static void Main()
    {
        Func<int, int> kvadrat = x => x * x;
        Func<int, string> formatlash = s => $"Natija: {s}";

        var kompozitsiya = Birlashtir(kvadrat, formatlash);

        Console.WriteLine(kompozitsiya(6));
    }
}

```

## Tushuntirish va Mantiq:
Funksional kompozitsiya kichik va toza funksiyalardan murakkab qayta ishlash quvurlarini (Pipelines) qurish imkonini beradi.

## Ishlash natijasi:
```text
Natija: 36
```

# 573-Topshiriq: Predikatlar Kompozitsiyasi: And, Or, Not Extension Metodlari
## Topshiriq sharti:
`Predicate<T>` lar ustida mantiqiy amallarni zanjirlash.

## Yechim (C# kodi):
```csharp
using System;

static class PredicateExtensions
{
    public static Predicate<T> And<T>(this Predicate<T> bir, Predicate<T> ikki)
        => x => bir(x) && ikki(x);

    public static Predicate<T> Or<T>(this Predicate<T> bir, Predicate<T> ikki)
        => x => bir(x) || ikki(x);
}

internal class Program
{
    static void Main()
    {
        Predicate<int> musbat = x => x > 0;
        Predicate<int> juft = x => x % 2 == 0;

        var musbatVaJuft = musbat.And(juft);

        Console.WriteLine($"4 musbat va juftmi: {musbatVaJuft(4)}");
        Console.WriteLine($"-2 musbat va juftmi: {musbatVaJuft(-2)}");
    }
}

```

## Tushuntirish va Mantiq:
Extension metodlar orqali delegatlarni mantiqiy algebrik operatorlar bilan boyitish mumkin.

## Ishlash natijasi:
```text
4 musbat va juftmi: True
-2 musbat va juftmi: False
```

# 574-Topshiriq: Karyerlash (Currying) va Qisman Qo'llash (Partial Application)
## Topshiriq sharti:
Ko'p parametrli funksiyani bir parametrli funksiyalar zanjiriga ajratish.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        // 3 parametrli qo'shish funksiyasini karyerlash:
        Func<int, Func<int, Func<int, int>>> qosh = a => b => c => a + b + c;

        var qosh10 = qosh(10);
        var qosh10Va20 = qosh10(20);
        int yakun = qosh10Va20(5);

        Console.WriteLine($"Karyerlangan natija: {yakun}");
    }
}

```

## Tushuntirish va Mantiq:
Currying funksional dasturlashning asosiy ustunlaridan biri bo'lib, konfiguratsiya qilingan oraliq funksiyalarni qayta ishlatishda qo'l keladi.

## Ishlash natijasi:
```text
Karyerlangan natija: 35
```

# 575-Topshiriq: Asinxron Delegatlar va Asinxron Hodisalar (Async EventHandler)
## Topshiriq sharti:
`Func<Task>` va asinxron voqealarni to'g'ri boshqarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

class AsinxronXizmat
{
    // void o'rniga Func<Task> ishlatish asinxron xatolarni yo'qotmaydi
    public event Func<string, Task>? YangilikKeldi;

    public async Task Tarqat(string xabar)
    {
        if (YangilikKeldi != null)
        {
            foreach (Func<string, Task> handler in YangilikKeldi.GetInvocationList())
            {
                await handler(xabar);
            }
        }
    }
}

internal class Program
{
    static async Task Main()
    {
        var xizmat = new AsinxronXizmat();
        xizmat.YangilikKeldi += async msg =>
        {
            await Task.Delay(50);
            Console.WriteLine($"Asinxron qayta ishlandi: {msg}");
        };

        await xizmat.Tarqat("Serverga so'rov keldi");
    }
}

```

## Tushuntirish va Mantiq:
Standart `async void` event handlerlar xatolik yuz berganda jarayonni qulatishi mumkin. `Func<Task>` delegati esa har bir obunachini to'liq `await` qilish imkonini beradi.

## Ishlash natijasi:
```text
Asinxron qayta ishlandi: Serverga so'rov keldi
```

# 576-Topshiriq: Expression Trees Asoslari: Kodni Ma'lumot Sifatida Ko'rish
## Topshiriq sharti:
`Func<int, bool>` va `Expression<Func<int, bool>>` o'rtasidagi fundamental farq.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq.Expressions;

internal class Program
{
    static void Main()
    {
        // 1. Delegat - bu bevosita bajariladigan mashina kodi:
        Func<int, bool> delegat = x => x > 5;

        // 2. Expression Tree - bu sintaktik daraxt (AST - Abstract Syntax Tree):
        Expression<Func<int, bool>> daraxt = x => x > 5;

        Console.WriteLine($"Daraxt ifodasi: {daraxt}");
        Console.WriteLine($"Tugun turi: {daraxt.NodeType}");
        Console.WriteLine($"Tana turi: {daraxt.Body.NodeType}");
    }
}

```

## Tushuntirish va Mantiq:
Expression Tree kodni bajarish o'rniga uning ichki tuzilishini obyektlar daraxti sifatida taqdim etadi. Bu Entity Framework ga C# kodini SQL so'roviga tarjima qilish imkonini beradi.

## Ishlash natijasi:
```text
Daraxt ifodasi: x => (x > 5)
Tugun turi: Lambda
Tana turi: GreaterThan
```

# 577-Topshiriq: Expression Tree ni Dinamik Tahlil Qilish (Inspecting AST)
## Topshiriq sharti:
Lambda ifodaning parametrlari va operatorlarini dastur ichida ochib o'qish.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq.Expressions;

internal class Program
{
    static void Main()
    {
        Expression<Func<int, int, int>> ifoda = (a, b) => a + b;

        var tana = (BinaryExpression)ifoda.Body;

        Console.WriteLine($"Chap parametr: {tana.Left}");
        Console.WriteLine($"Operator: {tana.NodeType}");
        Console.WriteLine($"O'ng parametr: {tana.Right}");
    }
}

```

## Tushuntirish va Mantiq:
BinaryExpression ikkita operand va bitta operatorga ega bo'lgan amallarni ifodalaydi.

## Ishlash natijasi:
```text
Chap parametr: a
Operator: Add
O'ng parametr: b
```

# 578-Topshiriq: Expression Tree ni Runtime da Kompilyatsiya Qilish (`.Compile()`)
## Topshiriq sharti:
Daraxt ko'rinishidagi kodni runtime da haqiqiy bajariluvchi delegatga aylantirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq.Expressions;

internal class Program
{
    static void Main()
    {
        Expression<Func<int, int>> ifoda = x => x * 3;

        // Daraxtni IL bayt-kodga va mashina kodiga kompilyatsiya qilamiz:
        Func<int, int> bajariluvchiDelegat = ifoda.Compile();

        int natija = bajariluvchiDelegat(7);
        Console.WriteLine($"Dinamik kompilyatsiya natijasi: {natija}");
    }
}

```

## Tushuntirish va Mantiq:
Compile() metodi CLR ning `System.Reflection.Emit` imkoniyatlaridan foydalanib, xotirada tezkor IL kod hosil qiladi.

## Ishlash natijasi:
```text
Dinamik kompilyatsiya natijasi: 21
```

# 579-Topshiriq: Dinamik Expression Daraxtini Qo'lda Qurish (Code Generation)
## Topshiriq sharti:
Birorta ham matn yozmasdan, faqat `Expression` sinflari bilan funksiya yaratish.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq.Expressions;

internal class Program
{
    static void Main()
    {
        // Maqsad: (x, y) => x * y funksiyasini dasturiy yo'l bilan yaratish
        var p1 = Expression.Parameter(typeof(int), "x");
        var p2 = Expression.Parameter(typeof(int), "y");

        var kopaytma = Expression.Multiply(p1, p2);
        var lambda = Expression.Lambda<Func<int, int, int>>(kopaytma, p1, p2);

        var funksiya = lambda.Compile();
        Console.WriteLine($"Qurilgan funksiya: {lambda}");
        Console.WriteLine($"Chaqiruv (4, 5): {funksiya(4, 5)}");
    }
}

```

## Tushuntirish va Mantiq:
Dinamik expressionlar ORM lar, qidiruv filtrlari va serializatorlarda yuqori tezlikdagi dinamik kod ishlab chiqarishda ishlatiladi.

## Ishlash natijasi:
```text
Qurilgan funksiya: (x, y) => (x * y)
Chaqiruv (4, 5): 20
```

# 580-Topshiriq: Middleware / Pipeline Pattern Delegatlar Zanjiri
## Topshiriq sharti:
ASP.NET Core quvuriga o'xshash zanjirli qayta ishlash delegatini quring.

## Yechim (C# kodi):
```csharp
using System;

delegate void MiddlewareDelegate(string context, Action keyingi);

internal class Program
{
    static void Main()
    {
        Action pipeline = () => Console.WriteLine("[Asosiy Handler]: So'rov bajarildi.");

        // 1-middleware: Vaqtni o'lchash
        Action orabTuruvchi1 = () =>
        {
            Console.WriteLine("[Middleware 1]: Boshlandi");
            pipeline();
            Console.WriteLine("[Middleware 1]: Tugadi");
        };

        // 2-middleware: Autentifikatsiya
        Action orabTuruvchi2 = () =>
        {
            Console.WriteLine("[Middleware 2]: Tekshirildi");
            orabTuruvchi1();
        };

        orabTuruvchi2();
    }
}

```

## Tushuntirish va Mantiq:
Bu naqsh 'Pik Rus' (Russian Doll) uslubi deb ataladi: har bir oraliq qatlam keyingi qatlamni chaqiradi va javob qaytgach o'z ishini yakunlaydi.

## Ishlash natijasi:
```text
[Middleware 2]: Tekshirildi
[Middleware 1]: Boshlandi
[Asosiy Handler]: So'rov bajarildi.
[Middleware 1]: Tugadi
```

# 581-Topshiriq: Funksional Keshlash (Memoization) Higher-Order Function
## Topshiriq sharti:
Har qanday bir parametrli funksiyani keshlovchi umumiy o'rovchi (wrapper) yozing.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static Func<T, TResult> Memoize<T, TResult>(Func<T, TResult> funksiya) where T : notnull
    {
        var kesh = new Dictionary<T, TResult>();
        return arg =>
        {
            if (kesh.TryGetValue(arg, out var natija))
            {
                Console.WriteLine($"[Keshdan olindi]: {arg}");
                return natija;
            }
            Console.WriteLine($"[Hisoblanmoqda]: {arg}");
            natija = funksiya(arg);
            kesh[arg] = natija;
            return natija;
        };
    }

    static void Main()
    {
        Func<int, int> ogirHisob = n => n * n;
        var keshliHisob = Memoize(ogirHisob);

        Console.WriteLine(keshliHisob(5));
        Console.WriteLine(keshliHisob(5));
    }
}

```

## Tushuntirish va Mantiq:
Memoization funksiyaning kirish parametrlariga ko'ra natijasini eslab qoladi va takroriy hisoblashlarni oldini oladi.

## Ishlash natijasi:
```text
[Hisoblanmoqda]: 5
25
[Keshdan olindi]: 5
25
```

# 582-Topshiriq: Retry Pattern Funksional Delegat Yordamida
## Topshiriq sharti:
Xatolik berganda amalni bir necha bor qayta takrorlovchi umumiy delegat.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static T TakrorBajar<T>(Func<T> amal, int urinishlarSoni)
    {
        for (int i = 1; i <= urinishlarSoni; i++)
        {
            try
            {
                return amal();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Urinish {i} muvaffaqiyatsiz: {ex.Message}");
                if (i == urinishlarSoni) throw;
            }
        }
        throw new InvalidOperationException();
    }

    static void Main()
    {
        int sanagich = 0;
        Func<string> beqarorXizmat = () =>
        {
            sanagich++;
            if (sanagich < 3) throw new Exception("Tarmoq uzildi!");
            return "Muvaffaqiyatli ma'lumot!";
        };

        string javob = TakrorBajar(beqarorXizmat, 3);
        Console.WriteLine($"Yakuniy javob: {javob}");
    }
}

```

## Tushuntirish va Mantiq:
Retry pattern tarmoq so'rovlari va beqaror xizmatlar bilan ishlashda eng muhim barqarorlik mexanizmidir.

## Ishlash natijasi:
```text
Urinish 1 muvaffaqiyatsiz: Tarmoq uzildi!
Urinish 2 muvaffaqiyatsiz: Tarmoq uzildi!
Yakuniy javob: Muvaffaqiyatli ma'lumot!
```

# 583-Topshiriq: Funksional Profiler: Metod Vaqtini O'lchash
## Topshiriq sharti:
Amalning bajarilish vaqtini o'lchovchi yuqori tartibli funksiya (Higher-Order Function).

## Yechim (C# kodi):
```csharp
using System;
using System.Diagnostics;
using System.Threading;

internal class Program
{
    static void ProfilingQilish(string nom, Action amal)
    {
        var sw = Stopwatch.StartNew();
        amal();
        sw.Stop();
        Console.WriteLine($"[{nom}] bajarildi: {sw.ElapsedMilliseconds} ms");
    }

    static void Main()
    {
        ProfilingQilish("Yuklash jarayoni", () =>
        {
            Thread.Sleep(100);
        });
    }
}

```

## Tushuntirish va Mantiq:
Delegatlarni argument sifatida qabul qilish orqali butun ilova bo'ylab o'lchov va diagnostika kodlarini markazlashtirish mumkin.

## Ishlash natijasi:
```text
[Yuklash jarayoni] bajarildi: 100 ms
```

# 584-Topshiriq: Safe Execution Wrapper (Xatolarni Xavfsiz Qaytarish)
## Topshiriq sharti:
Try-catch bloklarini delegat ichiga yashirib, Result qaytarish.

## Yechim (C# kodi):
```csharp
using System;

record struct AmalNatijasi<T>(bool Muvaffaqiyatli, T? Qiymat, string? Xato);

internal class Program
{
    static AmalNatijasi<T> XavfsizChaqiruv<T>(Func<T> funksiya)
    {
        try
        {
            return new(true, funksiya(), null);
        }
        catch (Exception ex)
        {
            return new(false, default, ex.Message);
        }
    }

    static void Main()
    {
        var res1 = XavfsizChaqiruv(() => 10 / 2);
        Console.WriteLine($"Res1 muvaffaqiyat: {res1.Muvaffaqiyatli}, Qiymat: {res1.Qiymat}");

        var res2 = XavfsizChaqiruv(() => int.Parse("xato_son"));
        Console.WriteLine($"Res2 muvaffaqiyat: {res2.Muvaffaqiyatli}, Xato: {res2.Xato}");
    }
}

```

## Tushuntirish va Mantiq:
Safe Wrapper funksional uslubda xatolar bilan ishlashni qulaylashtiradi va qatorlararo try-catch takrorlanishini yo'qotadi.

## Ishlash natijasi:
```text
Res1 muvaffaqiyat: True, Qiymat: 5
Res2 muvaffaqiyat: False, Xato: The input string 'xato_son' was not in a correct format.
```

# 585-Topshiriq: C# 10 Natural Types for Lambdas
## Topshiriq sharti:
Kompilyator lambda turini avtomatik aniqlashi (`var` bilan lambda e'lon qilish).

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        // C# 10 gacha Func<string, int> deb aniq yozish shart edi.
        // C# 10 dan boshlab lambdalarning o'z 'Natural Type' i bor:
        var uzunlik = (string s) => s.Length;

        Console.WriteLine($"Uzunlik: {uzunlik("Antigravity")}");
        Console.WriteLine($"Delegat turi: {uzunlik.GetType().Name}");
    }
}

```

## Tushuntirish va Mantiq:
C# 10 dan boshlab kompilyator parametrlari ko'rsatilgan lambdalarni avtomatik ravishda mos `Func` yoki `Action` turiga bog'laydi.

## Ishlash natijasi:
```text
Uzunlik: 11
Delegat turi: Func`2
```

# 586-Topshiriq: Lambdalarga Atributlar Biriktirish (C# 10+ Lambda Attributes)
## Topshiriq sharti:
Lambda ifodalarning o'ziga va parametrlariga maxsus atributlar qo'yish.

## Yechim (C# kodi):
```csharp
using System;
using System.ComponentModel.DataAnnotations;

internal class Program
{
    static void Main()
    {
        // Parametrga va lambdaning o'ziga atribut berish:
        var tekshir = ([Required] string email) => email.Contains("@");

        Console.WriteLine($"Tekshirish: {tekshir("user@mail.com")}");
    }
}

```

## Tushuntirish va Mantiq:
Bu imkoniyat ASP.NET Core Minimal API larda `app.MapGet` lambdalariga `[FromQuery]`, `[FromBody]`, `[Authorize]` atributlarini qo'yish uchun yaratilgan.

## Ishlash natijasi:
```text
Tekshirish: True
```

# 587-Topshiriq: Native Function Pointers (`delegate*<int, int>` - C# 9+)
## Topshiriq sharti:
Zero-overhead: GC va CLR obyektisiz to'g'ridan-to'g'ri xotira ko'rsatkichi darajasidagi funksiya chaqiruvi.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.CompilerServices;

internal class Program
{
    [MethodImpl(MethodImplOptions.NoInlining)]
    static int Kvadrat(int x) => x * x;

    unsafe static void Main()
    {
        // Unmanaged / Native funksiya ko'rsatkichi:
        delegate*<int, int> ptr = &Kvadrat;

        int res = ptr(6);
        Console.WriteLine($"Native Function Pointer natijasi: {res}");
    }
}

```

## Tushuntirish va Mantiq:
`delegate*` qiymat turi (pointer) bo'lib, heap xotirada hech qanday `Delegate` obyekti yaratmaydi va `calli` IL buyrug'i orqali to'g'ridan-to'g'ri C tezligida chaqiriladi.

## Ishlash natijasi:
```text
Native Function Pointer natijasi: 36
```

# 588-Topshiriq: Delegatlar Tengligi (Equality of Delegates)
## Topshiriq sharti:
Ikkita alohida delegat qachon o'zaro teng (`==`) hisoblanadi?

## Yechim (C# kodi):
```csharp
using System;

class Hisobchi
{
    public void Amal() { }
}

internal class Program
{
    static void StatikAmal() { }

    static void Main()
    {
        // Statik metod delegatlari:
        Action s1 = StatikAmal;
        Action s2 = StatikAmal;
        Console.WriteLine($"Statik metodlar tengmi: {s1 == s2}");

        // Instansiya metod delegatlari:
        var obj1 = new Hisobchi();
        var obj2 = new Hisobchi();

        Action o1 = obj1.Amal;
        Action o2 = obj1.Amal;
        Action o3 = obj2.Amal;

        Console.WriteLine($"Bir xil obyekt delegatlari tengmi: {o1 == o2}");
        Console.WriteLine($"Har xil obyekt delegatlari tengmi: {o1 == o3}");
    }
}

```

## Tushuntirish va Mantiq:
Delegatlar agar ularning `Target` (obyekt instansiyasi) va `Method` (metod identifikatori) aynan bir xil bo'lsagina o'zaro teng hisoblanadi.

## Ishlash natijasi:
```text
Statik metodlar tengmi: True
Bir xil obyekt delegatlari tengmi: True
Har xil obyekt delegatlari tengmi: False
```

# 589-Topshiriq: Delegatlarda Kovariantlik va Kontravariantlik
## Topshiriq sharti:
`Func<out T>` va `Action<in T>` ning delegatlar darajasidagi o'zgarishi.

## Yechim (C# kodi):
```csharp
using System;

class Hayvon { }
class Kuchuk : Hayvon { }

internal class Program
{
    static Kuchuk KuchukYarat() => new Kuchuk();
    static void HayvonniQabulQil(Hayvon h) => Console.WriteLine("Hayvon qabul qilindi.");

    static void Main()
    {
        // Qaytish turi bo'yicha kovariantlik: Kuchuk qaytaruvchi metod Func<Hayvon> ga mos tushadi!
        Func<Hayvon> hayvonBer = KuchukYarat;
        Console.WriteLine($"Olingan tur: {hayvonBer().GetType().Name}");

        // Kirish parametri bo'yicha kontravariantlik: Hayvon qabul qiluvchi metod Action<Kuchuk> ga beriladi!
        Action<Kuchuk> kuchukniQabulQil = HayvonniQabulQil;
        kuchukniQabulQil(new Kuchuk());
    }
}

```

## Tushuntirish va Mantiq:
C# dagi delegat parametrlari kontravariant, qaytish turlari esa kovariant bo'lib, polimorfizmni eng yuqori darajada qo'llab-quvvatlaydi.

## Ishlash natijasi:
```text
Olingan tur: Kuchuk
Hayvon qabul qilindi.
```

# 590-Topshiriq: WeakReference Yordamida Kuchsiz Obuna (Weak Event Pattern)
## Topshiriq sharti:
Xotira oqishini (Memory Leak) oldini olish uchun kuchsiz havolalardan foydalanish.

## Yechim (C# kodi):
```csharp
using System;

class ZaifTinglovchi
{
    private readonly WeakReference<Action> kuchsizHavola;

    public ZaifTinglovchi(Action amal)
    {
        kuchsizHavola = new WeakReference<Action>(amal);
    }

    public void Chaqlir()
    {
        if (kuchsizHavola.TryGetTarget(out var amal))
        {
            amal();
        }
        else
        {
            Console.WriteLine("[ZaifTinglovchi]: Obyekt allaqachon GC tomonidan tozalangan.");
        }
    }
}

internal class Program
{
    static void Main()
    {
        Action harakat = () => Console.WriteLine("Tirik harakat bajarildi!");
        var zt = new ZaifTinglovchi(harakat);

        zt.Chaqlir();
    }
}

```

## Tushuntirish va Mantiq:
WeakReference GC ga obyektni tozalashga to'sqinlik qilmaydi. Bu orqali hodisa obunalari xotirani asir qilib ushlab qolmaydi.

## Ishlash natijasi:
```text
Tirik harakat bajarildi!
```

# 591-Topshiriq: INotifyPropertyChanged MVVM Pattern Hodisasi
## Topshiriq sharti:
Xususiyat o'zgarganda UI ni avtomatik xabardor qiluvchi hodisa shartnomasi.

## Yechim (C# kodi):
```csharp
using System;
using System.ComponentModel;
using System.Runtime.CompilerServices;

class FoydalanuvchiModeli : INotifyPropertyChanged
{
    private string ism = "";

    public event PropertyChangedEventHandler? PropertyChanged;

    public string Ism
    {
        get => ism;
        set
        {
            if (ism != value)
            {
                ism = value;
                OnPropertyChanged();
            }
        }
    }

    protected void OnPropertyChanged([CallerMemberName] string? propName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propName));
    }
}

internal class Program
{
    static void Main()
    {
        var model = new FoydalanuvchiModeli();
        model.PropertyChanged += (sender, e) =>
        {
            Console.WriteLine($"Xususiyat o'zgardi: {e.PropertyName}");
        };

        model.Ism = "Sanjar";
    }
}

```

## Tushuntirish va Mantiq:
INotifyPropertyChanged WPF, WinUI, MAUI va Avalonia kabi barcha .NET UI freymvorklarining ma'lumot bog'lash (Data Binding) yadrosidir.

## Ishlash natijasi:
```text
Xususiyat o'zgardi: Ism
```

# 592-Topshiriq: Bekor Qilinadigan Hodisalar (Cancellable Events: CancelEventArgs)
## Topshiriq sharti:
Obunachiga amalni to'xtatish yoki bekor qilish vakolatini berish.

## Yechim (C# kodi):
```csharp
using System;
using System.ComponentModel;

class HujjatTahrirlovchi
{
    public event EventHandler<CancelEventArgs>? SaqlashOldidan;

    public void Saqlash()
    {
        var args = new CancelEventArgs();
        SaqlashOldidan?.Invoke(this, args);

        if (args.Cancel)
        {
            Console.WriteLine("[Bekor qilindi]: Saqlash jarayoni to'xtatildi!");
            return;
        }

        Console.WriteLine("[Muvaffaqiyatli]: Hujjat saqlandi.");
    }
}

internal class Program
{
    static void Main()
    {
        var editor = new HujjatTahrirlovchi();

        editor.SaqlashOldidan += (sender, e) =>
        {
            Console.WriteLine("Tekshiruv: Xatolik bor, saqlashni bekor qilamiz!");
            e.Cancel = true;
        };

        editor.Saqlash();
    }
}

```

## Tushuntirish va Mantiq:
CancelEventArgs orqali hodisa obunachisi `e.Cancel = true` qilib, asosiy jarayonni to'xtatib qolishi mumkin.

## Ishlash natijasi:
```text
Tekshiruv: Xatolik bor, saqlashni bekor qilamiz!
[Bekor qilindi]: Saqlash jarayoni to'xtatildi!
```

# 593-Topshiriq: Funksional Debounce Pattern (Chaqiruvlarni Siquvchi Delegat)
## Topshiriq sharti:
Ketma-ket tez kelgan hodisalardan faqat eng oxirgisini belgilangan vaqtdan keyin bajarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

internal class Program
{
    static Action Debounce(Action amal, int kutishVaqtiMs)
    {
        CancellationTokenSource? cts = null;

        return () =>
        {
            cts?.Cancel();
            cts = new CancellationTokenSource();
            var token = cts.Token;

            Task.Delay(kutishVaqtiMs, token).ContinueWith(t =>
            {
                if (!t.IsCanceled) amal();
            }, token);
        };
    }

    static void Main()
    {
        Action qidirish = () => Console.WriteLine("Qidiruv so'rovi serverga yuborildi!");
        var debounced = Debounce(qidirish, 100);

        Console.WriteLine("Foydalanuvchi tez-tez klavish bosmoqda...");
        debounced();
        debounced();
        debounced();

        Thread.Sleep(200); // Kutish
    }
}

```

## Tushuntirish va Mantiq:
Debounce qidiruv satriga harf kiritilganda har bir harf uchun alohida so'rov jo'natmasdan, foydalanuvchi yozishdan to'xtaganidagina bitta so'rov yuborishda qo'llanadi.

## Ishlash natijasi:
```text
Foydalanuvchi tez-tez klavish bosmoqda...
Qidiruv so'rovi serverga yuborildi!
```

# 594-Topshiriq: Event Aggregator Pattern (Global Voqealar Markazi)
## Topshiriq sharti:
Sinflarning to'g'ridan-to'g'ri bir-birini tanimasdan xabarlashuvi.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

class EventAggregator
{
    private static readonly Dictionary<Type, List<Delegate>> obunalar = new();

    public static void ObunaBo'l<T>(Action<T> amal)
    {
        var tur = typeof(T);
        if (!obunalar.ContainsKey(tur)) obunalar[tur] = new();
        obunalar[tur].Add(amal);
    }

    public static void Tarqat<T>(T xabar)
    {
        var tur = typeof(T);
        if (obunalar.TryGetValue(tur, out var list))
        {
            foreach (var d in list) ((Action<T>)d)(xabar);
        }
    }
}

record FoydalanuvchiTizimgaKirdi(string Login);

internal class Program
{
    static void Main()
    {
        EventAggregator.ObunaBo'l<FoydalanuvchiTizimgaKirdi>(e =>
        {
            Console.WriteLine($"[Audit Xizmati]: {e.Login} tizimga kirdi.");
        });

        EventAggregator.Tarqat(new FoydalanuvchiTizimgaKirdi("akmal_dev"));
    }
}

```

## Tushuntirish va Mantiq:
Event Aggregator arxitekturasi yirik ilovalarda komponentlar orasidagi bog'liqlikni minimallashtiradi.

## Ishlash natijasi:
```text
[Audit Xizmati]: akmal_dev tizimga kirdi.
```

# 595-Topshiriq: Asinxron Hodisalarni Task.WhenAll Bilan Parallel Chaqirish
## Topshiriq sharti:
Barcha obunachilarni bir vaqtda parallel ishga tushirib kutish.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;
using System.Threading.Tasks;

class AsinxronBroker
{
    public event Func<string, Task>? XabarKeltirildi;

    public async Task Tarqatish(string xabar)
    {
        if (XabarKeltirildi == null) return;

        var delegatlar = XabarKeltirildi.GetInvocationList().Cast<Func<string, Task>>();
        var vazifalar = delegatlar.Select(d => d(xabar));

        await Task.WhenAll(vazifalar);
        Console.WriteLine("Barcha asinxron tinglovchilar yakunlandi.");
    }
}

internal class Program
{
    static async Task Main()
    {
        var broker = new AsinxronBroker();
        broker.XabarKeltirildi += async msg =>
        {
            await Task.Delay(30);
            Console.WriteLine($"Tinglovchi 1 qabul qildi: {msg}");
        };
        broker.XabarKeltirildi += async msg =>
        {
            await Task.Delay(10);
            Console.WriteLine($"Tinglovchi 2 qabul qildi: {msg}");
        };

        await broker.Tarqatish("Muhim yangilanish");
    }
}

```

## Tushuntirish va Mantiq:
Task.WhenAll barcha obunachilarni parallel bajaradi va umumiy kechikishni kamaytiradi.

## Ishlash natijasi:
```text
Tinglovchi 2 qabul qildi: Muhim yangilanish
Tinglovchi 1 qabul qildi: Muhim yangilanish
Barcha asinxron tinglovchilar yakunlandi.
```

# 596-Topshiriq: Metod Ko'rsatkichini Lambdaga Konvertatsiya Qilishdagi Allocations
## Topshiriq sharti:
Metod guruhi (Method Group) va Lambda ning xotira ajratish farqi.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void OddiyMetod() { }

    static void Main()
    {
        // .NET 7 gacha Method Group har safar yangi Action obyekti ajratardi.
        // .NET 7/8/9 dan boshlab esa Method Group ham keshlanadi!
        Action a1 = OddiyMetod;
        Action a2 = OddiyMetod;

        Console.WriteLine($"Delegatlar bir xil keshdanmi: {object.ReferenceEquals(a1, a2)}");
    }
}

```

## Tushuntirish va Mantiq:
Zamonaviy C# kompilyatori statik metod guruhlarini keshlaydi, bu esa har bir chaqiruvda yangi heap obyekti yaratilishini yo'qotadi.

## Ishlash natijasi:
```text
Delegatlar bir xil keshdanmi: True
```

# 597-Topshiriq: Predicate, Comparison va Converter Eski BCL Delegatlari
## Topshiriq sharti:
Array.Find, Array.Sort va Array.ConvertAll metodlarida funksional amallar.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        string[] sonMatnlari = ["10", "40", "20", "5"];

        // Converter delegati orqali int massivga o'girish:
        int[] sonlar = Array.ConvertAll(sonMatnlari, int.Parse);

        // Comparison delegati orqali kamayish tartibida saralash:
        Array.Sort(sonlar, (a, b) => b.CompareTo(a));

        Console.WriteLine($"Saralangan sonlar: {string.Join(", ", sonlar)}");
    }
}

```

## Tushuntirish va Mantiq:
Array sinfidagi generik yordamchi metodlar LINQ dan oldin paydo bo'lgan bo'lib, xotirani minimal ishlatishi bilan ajralib turadi.

## Ishlash natijasi:
```text
Saralangan sonlar: 40, 20, 10, 5
```

# 598-Topshiriq: Delegatlarni Dinamik Birlashtirish: Delegate.Combine va Remove
## Topshiriq sharti:
Metodlar orqali delegatlar ro'yxatini dasturiy boshqarish.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Bir() => Console.Write("1 ");
    static void Ikki() => Console.Write("2 ");

    static void Main()
    {
        Action d1 = Bir;
        Action d2 = Ikki;

        // Delegate.Combine operator += bilan bir xil:
        Delegate umumiy = Delegate.Combine(d1, d2)!;
        ((Action)umumiy)();

        // Delegate.Remove operator -= bilan bir xil:
        umumiy = Delegate.Remove(umumiy, d1)!;
        ((Action)umumiy)();

        Console.WriteLine();
    }
}

```

## Tushuntirish va Mantiq:
Operator `+=` va `-=` kompilyator tomonidan mos ravishda `Delegate.Combine` va `Delegate.Remove` statik metodlariga aylantiriladi.

## Ishlash natijasi:
```text
1 2 2
```

# 599-Topshiriq: Delegat va Interface: Qachon qaysi birini tanlash kerak?
## Topshiriq sharti:
Bitta metodlik shartnoma uchun delegat va to'liq interfeys tanlovi tahlili.

## Yechim (C# kodi):
```csharp
using System;

// 1. Interfeys usuli
interface ISolishdiruvchi<T>
{
    int Solishtir(T a, T b);
}

// 2. Delegat usuli: Func<T, T, int>

internal class Program
{
    static void Tartibla(int[] massiv, Func<int, int, int> solishtiruvchi)
    {
        // Delegat orqali bir satrda lambda uzatish mumkin
        Array.Sort(massiv, (x, y) => solishtiruvchi(x, y));
    }

    static void Main()
    {
        int[] sonlar = [5, 2, 8, 1];
        Tartibla(sonlar, (a, b) => a.CompareTo(b));

        Console.WriteLine($"Tartiblandi: {string.Join(", ", sonlar)}");
    }
}

```

## Tushuntirish va Mantiq:
Bitta operatsiya kerak bo'lganda va inline lambda qulay bo'lsa delegat (`Func/Action`) tanlanadi; agar sinf bir nechta bog'liq metodlar holatini ifodalasa interfeys afzal ko'riladi.

## Ishlash natijasi:
```text
Tartiblandi: 1, 2, 5, 8
```

# 600-Topshiriq: Delegatlar Xulosasi: To'liq Asinxron Middleware Pipeline Arxitekturasi
## Topshiriq sharti:
ASP.NET Core Web Application uslubidagi zanjirli request-processing pipeline qurish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

class HttpContext
{
    public string Path { get; set; } = "/";
    public int StatusCode { get; set; } = 200;
    public string Javob { get; set; } = "";
}

delegate Task RequestDelegate(HttpContext context);

class PipelineBuilder
{
    private readonly List<Func<RequestDelegate, RequestDelegate>> middlewares = new();

    public PipelineBuilder Use(Func<RequestDelegate, RequestDelegate> middleware)
    {
        middlewares.Add(middleware);
        return this;
    }

    public RequestDelegate Build()
    {
        RequestDelegate oxirgi = context =>
        {
            context.StatusCode = 404;
            context.Javob = "Sahifa topilmadi";
            return Task.CompletedTask;
        };

        for (int i = middlewares.Count - 1; i >= 0; i--)
        {
            oxirgi = middlewares[i](oxirgi);
        }

        return oxirgi;
    }
}

internal class Program
{
    static async Task Main()
    {
        var builder = new PipelineBuilder();

        // 1. Logger Middleware
        builder.Use(next => async ctx =>
        {
            Console.WriteLine($"[Log]: So'rov keldi: {ctx.Path}");
            await next(ctx);
            Console.WriteLine($"[Log]: So'rov tugadi: Status {ctx.StatusCode}");
        });

        // 2. Marshrutlash (Routing) Middleware
        builder.Use(next => async ctx =>
        {
            if (ctx.Path == "/salom")
            {
                ctx.StatusCode = 200;
                ctx.Javob = "Salom, dunyo!";
                return; // Keyingisiga o'tmaydi (Short-circuiting)
            }
            await next(ctx);
        });

        var pipeline = builder.Build();

        var ctx = new HttpContext { Path = "/salom" };
        await pipeline(ctx);
        Console.WriteLine($"Yakuniy javob: {ctx.Javob}");
    }
}

```

## Tushuntirish va Mantiq:
ASP.NET Core ning butun veb quvuri aynan shunday `Func<RequestDelegate, RequestDelegate>` delegatlar zanjiri asosida barpo etilgan.

## Ishlash natijasi:
```text
[Log]: So'rov keldi: /salom
[Log]: So'rov tugadi: Status 200
Yakuniy javob: Salom, dunyo!
```

