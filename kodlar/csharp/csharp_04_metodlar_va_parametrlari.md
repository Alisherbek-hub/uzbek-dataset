# 4-Mavzu: Metodlar va Parametrlari (151-200)

Ushbu bo'limda C# metodlarining to'liq anatomiyasi: metod signaturalari, qiymat va havola bo'yicha uzatish (`ref`, `out`, `in`, `ref readonly`), ixtiyoriy va nomlangan argumentlar, `params` kalit so'zi va C# 13 `params` to'plamlari, metodlarni qayta yuklash (Overloading), rekursiya va dum rekursiya, mahalliy funksiyalar (Local Functions), statik mahalliy metodlar, qisqa ifodali metodlar (`=>`), kengaytirish metodlari (Extension Methods) hamda xatoliklarni erta tekshiruvchi Guard metodlari bo'yicha 50 ta amaliy topshiriq jamlangan.

# 151-Topshiriq: Metod signaturasi va qiymat qaytarish
## Topshiriq sharti:
Ikki sonning ko'paytmasini hisoblab qaytaruvchi va natijani konsolga chiqaruvchi toza metod yozing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static int Kopaytir(int a, int b)
    {
        return a * b;
    }

    static void Main()
    {
        int natija = Kopaytir(7, 8);
        Console.WriteLine($"7 * 8 = {natija}");
    }
}

```

## Tushuntirish va Mantiq:
Metod signaturasi uning nomi va parametrlari turlari/tartibidan iboratdir. Qaytuvchi tur (`int`) signaturaga kirmaydi, lekin kompilyator tomonidan tekshiriladi. `return` operatori natijani chaqiruvchiga qaytaradi va metodni yakunlaydi.

## Ishlash natijasi:
```text
7 * 8 = 56
```

# 152-Topshiriq: Qiymat bo'yicha uzatish (Pass-by-value): Asl qiymat o'zgarmasligi
## Topshiriq sharti:
Oddiy qiymat turidagi o'zgaruvchi metodga uzatilganda uning faqat nusxasi olinishi va asl qiymat o'zgarmasligini isbotlang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void QiymatniOshir(int son)
    {
        son += 100;
        Console.WriteLine($"Metod ichida son: {son}");
    }

    static void Main()
    {
        int original = 50;
        QiymatniOshir(original);
        Console.WriteLine($"Main ichida original: {original}");
    }
}

```

## Tushuntirish va Mantiq:
C# da standart holatda barcha parametrlar qiymat bo'yicha (by value) uzatiladi. Metod chaqirilganda Stack da yangi freym ochilib, argument nusxasi o'sha yerga ko'chiriladi. Metod tugashi bilan bu nusxa o'chiriladi, asl o'zgaruvchi o'zgarishsiz qoladi.

## Ishlash natijasi:
```text
Metod ichida son: 150
Main ichida original: 50
```

# 153-Topshiriq: ref modifikatori: O'zgaruvchini havola bo'yicha uzatish
## Topshiriq sharti:
`ref` kalit so'zidan foydalanib ikkita o'zgaruvchi qiymatlarini o'zaro almashtiruvchi (`Swap`) metodini yozing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Swap(ref int x, ref int y)
    {
        int vaqtinchalik = x;
        x = y;
        y = vaqtinchalik;
    }

    static void Main()
    {
        int a = 10;
        int b = 20;

        Console.WriteLine($"Avval: a = {a}, b = {b}");
        Swap(ref a, ref b);
        Console.WriteLine($"Keyin: a = {a}, b = {b}");
    }
}

```

## Tushuntirish va Mantiq:
`ref` modifikatori parametr nusxasini emas, balki to'g'ridan-to'g'ri o'zgaruvchining Stack dagi xotira manzilini (managed pointer) uzatadi. Shuning uchun metod ichidagi har qanday o'zgartirish bevosita asl o'zgaruvchida aks etadi. `ref` parametriga uzatishdan oldin dastlabki qiymat berilgan bo'lishi shart.

## Ishlash natijasi:
```text
Avval: a = 10, b = 20
Keyin: a = 20, b = 10
```

# 154-Topshiriq: out modifikatori: Metoddan bir nechta natija qaytarish
## Topshiriq sharti:
Bo'lish amalini bajarib, ham butun qismini, ham qoldig'ini `out` parametri orqali bir vaqtda qaytaring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static bool Bolish(int bolinuvchi, int boluvchi, out int butun, out int qoldiq)
    {
        if (boluvchi == 0)
        {
            butun = 0;
            qoldiq = 0;
            return false;
        }

        butun = bolinuvchi / boluvchi;
        qoldiq = bolinuvchi % boluvchi;
        return true;
    }

    static void Main()
    {
        if (Bolish(23, 5, out int b, out int q))
        {
            Console.WriteLine($"23 / 5 = {b}, qoldiq: {q}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`out` modifikatori metoddan tashqariga qiymat chiqarish uchun mo'ljallangan. `ref` dan farqli ravishda, argumentga oldindan qiymat berish shart emas, lekin metod tanasidan chiqishdan oldin unga albatta qiymat biriktirilishi shart.

## Ishlash natijasi:
```text
23 / 5 = 4, qoldiq: 3
```

# 155-Topshiriq: in modifikatori: Readonly havola uzatish (Xotira optimallashuvi)
## Topshiriq sharti:
Katta `struct` turini nusxalash xarajatlaridan qutulish, ammo metod ichida uni o'zgartirishga yo'l qo'ymaslik uchun `in` parametridan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

struct KattaMatritsa
{
    public double M11, M12, M21, M22;
}

internal class Program
{
    static double Determinant(in KattaMatritsa m)
    {
        // m.M11 = 10; // KOMPILYATSIYA XATOSI! in parametri faqat o'qish uchun (readonly)
        return m.M11 * m.M22 - m.M12 * m.M21;
    }

    static void Main()
    {
        var mat = new KattaMatritsa { M11 = 4, M12 = 2, M21 = 3, M22 = 5 };
        double det = Determinant(in mat);
        Console.WriteLine($"Determinant: {det}");
    }
}

```

## Tushuntirish va Mantiq:
`in` parametri qiymatni nusxalamasdan havola bo'yicha (pointer kabi) uzatadi va xotirani tejaydi, biroq uni metod ichida o'zgartirishni qat'iyan taqiqlaydi (readonly reference). Katta strukturalar bilan ishlashda yuqori unumdorlik beradi.

## Ishlash natijasi:
```text
Determinant: 14
```

# 156-Topshiriq: ref readonly qaytuvchi qiymat (Ref Returns)
## Topshiriq sharti:
Massiv elementining xotiradagi manziliga faqat o'qish uchun havola qaytaruvchi metod yozing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static int[] massiv = [ 100, 200, 300 ];

    static ref readonly int ElementniOl(int indeks)
    {
        return ref massiv[indeks];
    }

    static void Main()
    {
        ref readonly int val = ref ElementniOl(1);
        Console.WriteLine($"Olingan qiymat: {val}");
        // val = 999; // XATO! Readonly havola orqali o'zgartirib bo'lmaydi
    }
}

```

## Tushuntirish va Mantiq:
`ref readonly` katta ob'yektlarning nusxalanmasdan, to'g'ridan-to'g'ri asl xotiradagi manzilini qaytaradi, shu bilan birga chaqiruvchining ushbu manzilni o'zgartirib yuborishining oldini oladi.

## Ishlash natijasi:
```text
Olingan qiymat: 200
```

# 157-Topshiriq: Ixtiyoriy parametrlar (Optional Parameters)
## Topshiriq sharti:
Standart qiymatga ega bo'lgan ixtiyoriy parametrli metod yarating va uni turli usullarda chaqiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void XabarChiqar(string matn, string prefiks = "INFO", bool yangiQator = true)
    {
        string natija = $"[{prefiks}]: {matn}";
        if (yangiQator)
            Console.WriteLine(natija);
        else
            Console.Write(natija);
    }

    static void Main()
    {
        XabarChiqar("Tizim ishga tushdi"); // Standart "INFO" va true ishlatiladi
        XabarChiqar("Fayl topilmadi", "OGOHLANTIRISH");
    }
}

```

## Tushuntirish va Mantiq:
Ixtiyoriy parametrlar parametrlar ro'yxatining eng oxirida joylashishi shart. Kompilyator ularning qiymatini chaqiruv nuqtasiga avtomatik qo'yib beradi.

## Ishlash natijasi:
```text
[INFO]: Tizim ishga tushdi
[OGOHLANTIRISH]: Fayl topilmadi
```

# 158-Topshiriq: Nomlangan argumentlar (Named Arguments)
## Topshiriq sharti:
Parametrlarni ularning nomi orqali ixtiyoriy tartibda uzatishni namoyish eting.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void FoydalanuvchiYarat(string ism, int yosh, string shahar)
    {
        Console.WriteLine($"Ism: {ism}, Yosh: {yosh}, Shahar: {shahar}");
    }

    static void Main()
    {
        // Parametrlar tartibi o'zgartirib uzatilmoqda
        FoydalanuvchiYarat(shahar: "Buxoro", ism: "Nodir", yosh: 26);
    }
}

```

## Tushuntirish va Mantiq:
Nomlangan argumentlar kodning o'qiluvchanligini (readability) sezilarli darajada oshiradi va parametrlari ko'p bo'lgan metodlarda qaysi qiymat nima uchun uzatilayotganini darhol anglash imkonini beradi.

## Ishlash natijasi:
```text
Ism: Nodir, Yosh: 26, Shahar: Buxoro
```

# 159-Topshiriq: params kalit so'zi: O'zgaruvchan sondagi argumentlar
## Topshiriq sharti:
`params` modifikatori yordamida ixtiyoriy sondagi butun sonlarni qabul qilib ularning yig'indisini hisoblang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static int Yigindi(params int[] sonlar)
    {
        int jami = 0;
        foreach (int s in sonlar)
        {
            jami += s;
        }
        return jami;
    }

    static void Main()
    {
        Console.WriteLine($"2 ta son yig'indisi: {Yigindi(5, 10)}");
        Console.WriteLine($"4 ta son yig'indisi: {Yigindi(1, 2, 3, 4)}");
        Console.WriteLine($"Bo'sh yig'indi: {Yigindi()}");
    }
}

```

## Tushuntirish va Mantiq:
`params` parametri metodning eng oxirgi parametri bo'lishi shart. Kompilyator chaqiruvdagi alohida argumentlarni avtomatik ravishda bitta massiv ichiga o'rab metodga jo'natadi.

## Ishlash natijasi:
```text
2 ta son yig'indisi: 15
4 ta son yig'indisi: 10
Bo'sh yig'indi: 0
```

# 160-Topshiriq: C# 13 params Collections: params ReadOnlySpan<T>
## Topshiriq sharti:
C# 13 da kengaytirilgan `params` imkoniyatidan foydalanib, Heap da massiv ajratmasdan `params ReadOnlySpan<int>` bilan ishlang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static int Maksimum(params ReadOnlySpan<int> sonlar)
    {
        if (sonlar.IsEmpty) return 0;
        int max = sonlar[0];
        foreach (int s in sonlar)
        {
            if (s > max) max = s;
        }
        return max;
    }

    static void Main()
    {
        // C# 13 da bu chaqiruv Heap da int[] yaratmaydi!
        int engKatta = Maksimum(12, 85, 43, 99, 7);
        Console.WriteLine($"Eng katta son: {engKatta}");
    }
}

```

## Tushuntirish va Mantiq:
C# 13 gacha `params` faqat oddiy massivlar (`T[]`) bilan cheklangan edi, bu esa har bir chaqiruvda Heap da keraksiz massiv ob'yektini yaratardi. C# 13 da `params ReadOnlySpan<T>` orqali argumentlar to'g'ridan-to'g'ri Stack da saqlanib, 0-allocation unumdorlikka erishildi.

## Ishlash natijasi:
```text
Eng katta son: 99
```

# 161-Topshiriq: Metodlarni qayta yuklash (Method Overloading)
## Topshiriq sharti:
Bir xil nomli, ammo har xil turdagi parametrlarni qabul qiluvchi `ChopEt` metodlarini yozing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void ChopEt(int son) => Console.WriteLine($"Son: {son}");
    static void ChopEt(string matn) => Console.WriteLine($"Matn: '{matn}'");
    static void ChopEt(int son, string matn) => Console.WriteLine($"Son va Matn: {son}, {matn}");

    static void Main()
    {
        ChopEt(42);
        ChopEt("Salom");
        ChopEt(100, "Asr");
    }
}

```

## Tushuntirish va Mantiq:
Metodlarni qayta yuklash (Overloading) metod nomi bir xil bo'lib, ularning parametrlari soni yoki turlari har xil bo'lishini talab qiladi. Qaysi metod chaqirilishi kompilyatsiya vaqtida aniqlanadi (Early Binding).

## Ishlash natijasi:
```text
Son: 42
Matn: 'Salom'
Son va Matn: 100, Asr
```

# 162-Topshiriq: Overloading da noaniqlik va tip tanlash qoidalari
## Topshiriq sharti:
Kompilyatorning eng mos (best match) metodni tanlash mexanizmini namoyish eting.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Tekshir(long son) => Console.WriteLine("long qabul qilindi");
    static void Tekshir(double son) => Console.WriteLine("double qabul qilindi");

    static void Main()
    {
        int x = 10;
        Tekshir(x); // int -> long implicit conversion double ga qaraganda yaqinroq
        Tekshir(10.5);
    }
}

```

## Tushuntirish va Mantiq:
Kompilyator eng kam konvertatsiyani talab qiluvchi aniqroq metodni tanlaydi. Butun sonli `int` avval butun sonli `long` ga o'tadi, suzuvchi nuqtali `double` ga emas.

## Ishlash natijasi:
```text
long qabul qilindi
double qabul qilindi
```

# 163-Topshiriq: Rekursiv metodlar: Faktorial hisoblash va Base Case
## Topshiriq sharti:
Rekursiyaning asosiy qoidasi bo'lgan to'xtash sharti (Base Case) bilan faktorialni hisoblang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static long Faktorial(int n)
    {
        if (n <= 1) return 1; // To'xtash sharti (Base Case)
        return n * Faktorial(n - 1); // Rekursiv qadam
    }

    static void Main()
    {
        Console.WriteLine($"5! = {Faktorial(5)}");
        Console.WriteLine($"7! = {Faktorial(7)}");
    }
}

```

## Tushuntirish va Mantiq:
Rekursiya o'z-o'zini chaqiruvchi funksiyadir. Har bir chaqiruv Stack da yangi freym ochadi. Agar to'xtash sharti bo'lmasa yoki noto'g'ri yozilsa, Stack to'lib `StackOverflowException` ro'y beradi.

## Ishlash natijasi:
```text
5! = 120
7! = 5040
```

# 164-Topshiriq: Rekursiya: Fibonachchi ketma-ketligi
## Topshiriq sharti:
Fibonachchi ketma-ketligining $n$-hadini rekursiya orqali toping.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static int Fibonachchi(int n)
    {
        if (n <= 0) return 0;
        if (n == 1) return 1;
        return Fibonachchi(n - 1) + Fibonachchi(n - 2);
    }

    static void Main()
    {
        Console.Write("Fibonachchi sonlari (1..7): ");
        for (int i = 1; i <= 7; i++)
        {
            Console.Write($"{Fibonachchi(i)} ");
        }
        Console.WriteLine();
    }
}

```

## Tushuntirish va Mantiq:
Oddiy daraxtsimon rekursiya $O(2^N)$ vaqt oladi, chunki bir xil qiymatlar qayta-qayta hisoblanadi. Katta $n$ uchun memoizatsiya yoki iterativ usul qo'llanilishi lozim.

## Ishlash natijasi:
```text
Fibonachchi sonlari (1..7): 1 1 2 3 5 8 13
```

# 165-Topshiriq: Dum rekursiya (Tail Recursion) va iterativ yondashuv
## Topshiriq sharti:
Faktorialni akkumulyator yordamida dum rekursiya ko'rinishida yozing va uni oddiy iterativ sikl bilan solishtiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static long FaktorialDum(int n, long acc = 1)
    {
        if (n <= 1) return acc;
        return FaktorialDum(n - 1, n * acc); // Oxirgi amal faqat metod chaqiruvi
    }

    static void Main()
    {
        Console.WriteLine($"6! (Dum rekursiya): {FaktorialDum(6)}");
    }
}

```

## Tushuntirish va Mantiq:
Dum rekursiyada metodning eng oxirgi amali faqat o'zini chaqirishdan iborat bo'ladi (qo'shimcha ko'paytirish qolmaydi). Bu chaqiruvlar zanjirida stack hajmini optimallashtirish imkonini beradi.

## Ishlash natijasi:
```text
6! (Dum rekursiya): 720
```

# 166-Topshiriq: Mahalliy funksiyalar (Local Functions)
## Topshiriq sharti:
C# 7 da kiritilgan metod ichidagi yordamchi funksiyalardan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void MassivniFormatla(int[] sonlar)
    {
        // Mahalliy funksiya - faqat ushbu metod ichida ko'rinadi
        int Kvadrat(int x) => x * x;

        foreach (var s in sonlar)
        {
            Console.WriteLine($"{s} kvadrati: {Kvadrat(s)}");
        }
    }

    static void Main()
    {
        MassivniFormatla([2, 3, 4]);
    }
}

```

## Tushuntirish va Mantiq:
Mahalliy funksiyalar sinf maydonini keraksiz xususiy (private) metodlar bilan to'ldirmasdan, faqat bitta metodga tegishli bo'lgan yordamchi mantiqni o'sha metod ichida yashirish (inkapsulyatsiya) imkonini beradi.

## Ishlash natijasi:
```text
2 kvadrati: 4
3 kvadrati: 9
4 kvadrati: 16
```

# 167-Topshiriq: static mahalliy funksiyalar (Zero Allocation Closures)
## Topshiriq sharti:
C# 8 da kiritilgan `static local functions` yordamida tashqi o'zgaruvchilarni ushlab qolmaslik (closure allocation yo'qligi) kafolatini bering.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static int Hisobla(int a, int b)
    {
        // static mahalliy metod tashqi o'zgaruvchilarni ko'ra olmaydi
        return Yigindi(a, b);

        static int Yigindi(int x, int y) => x + y;
    }

    static void Main()
    {
        Console.WriteLine($"Natija: {Hisobla(15, 25)}");
    }
}

```

## Tushuntirish va Mantiq:
`static` modifikatori mahalliy funksiyaga berilganda, u tashqi metodning o'zgaruvchilarini ushlay olmaydi (capture qila olmaydi). Bu Heap da closure ob'yekti yaratilishini 100% istisno qiladi va unumdorlikni oshiradi.

## Ishlash natijasi:
```text
Natija: 40
```

# 168-Topshiriq: Expression-Bodied Methods: Qisqa metodlar (=>)
## Topshiriq sharti:
Bitta satrdan iborat ifodalarni `=>` sintaksisi orqali ixcham yozing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static int Kvadrat(int x) => x * x;
    static bool Juftmi(int x) => x % 2 == 0;
    static string Salomlash(string ism) => $"Assalomu alaykum, {ism}!";

    static void Main()
    {
        Console.WriteLine($"5 kvadrati: {Kvadrat(5)}");
        Console.WriteLine($"6 juftmi: {Juftmi(6)}");
        Console.WriteLine(Salomlash("Sardor"));
    }
}

```

## Tushuntirish va Mantiq:
Expression-bodied a'zolar (`=>`) jingalak qavslar `{ return ...; }` o'rniga ishlatiladi. Ular kodni o'ta toza va zamonaviy ko'rinishga keltiradi.

## Ishlash natijasi:
```text
5 kvadrati: 25
6 juftmi: True
Assalomu alaykum, Sardor!
```

# 169-Topshiriq: Kengaytirish metodlari (Extension Methods): this kalit so'zi
## Topshiriq sharti:
Mavjud sinf kodini o'zgartirmasdan, statik sinf va `this` parametri orqali yangi metod qo'shing.

## Yechim (C# kodi):
```csharp
using System;

static class StringExtensions
{
    public static int SozlarSoni(this string matn)
    {
        if (string.IsNullOrWhiteSpace(matn)) return 0;
        return matn.Split(' ', StringSplitOptions.RemoveEmptyEntries).Length;
    }
}

internal class Program
{
    static void Main()
    {
        string gap = "C# dasturlash tili juda kuchli";
        int soni = gap.SozlarSoni(); // Go'yo string ning o'zida shunday metod bordek chaqiriladi

        Console.WriteLine($"Gapdagi so'zlar soni: {soni}");
    }
}

```

## Tushuntirish va Mantiq:
Kengaytirish metodlari statik sinf ichida `static` qilib yoziladi va birinchi parametrida `this KengaytirilayotganTur nom` ko'rsatiladi. Bu .NET LINQ arxitekturasining tamal toshidir.

## Ishlash natijasi:
```text
Gapdagi so'zlar soni: 5
```

# 170-Topshiriq: Matnlar uchun amaliy Extension metod: IsValidEmail
## Topshiriq sharti:
Oddiy qoidalar asosida satr elektron pochta manziliga mosligini tekshiruvchi kengaytirish metodini yozing.

## Yechim (C# kodi):
```csharp
using System;

static class ValidatorExtensions
{
    public static bool IsValidEmail(this string email)
    {
        if (string.IsNullOrWhiteSpace(email)) return false;
        return email.Contains('@') && email.Contains('.') && email.IndexOf('@') < email.LastIndexOf('.');
    }
}

internal class Program
{
    static void Main()
    {
        string e1 = "foydalanuvchi@mail.uz";
        string e2 = "notogri_email.com";

        Console.WriteLine($"{e1} to'g'rimi: {e1.IsValidEmail()}");
        Console.WriteLine($"{e2} to'g'rimi: {e2.IsValidEmail()}");
    }
}

```

## Tushuntirish va Mantiq:
Kengaytirish metodlari orqali domen qoidalarini tabiiy va o'qilishi yoqimli ko'rinishda (`email.IsValidEmail()`) ifodalash mumkin.

## Ishlash natijasi:
```text
foydalanuvchi@mail.uz to'g'rimi: True
notogri_email.com to'g'rimi: False
```

# 171-Topshiriq: Sonlar uchun amaliy Extension metod: ToCurrency va IsEven
## Topshiriq sharti:
Butun va kasr sonlar uchun valyuta formatini beruvchi hamda juftlikni aniqlovchi metodlar qo'shing.

## Yechim (C# kodi):
```csharp
using System;

static class NumberExtensions
{
    public static bool IsEven(this int son) => son % 2 == 0;
    public static string ToCurrencyUz(this decimal narx) => $"{narx:N0} so'm";
}

internal class Program
{
    static void Main()
    {
        int n = 44;
        decimal narx = 1500000m;

        Console.WriteLine($"{n} juftmi: {n.IsEven()}");
        Console.WriteLine($"Mahsulot narxi: {narx.ToCurrencyUz()}");
    }
}

```

## Tushuntirish va Mantiq:
Extension metodlar primitiv qiymat turlariga (`int`, `decimal`, `double`) ham bemalol biriktirilishi mumkin.

## Ishlash natijasi:
```text
44 juftmi: True
Mahsulot narxi: 1,500,000 so'm
```

# 172-Topshiriq: Generik kengaytirish metodlari (Generic Extension Methods)
## Topshiriq sharti:
Ixtiyoriy turdagi massivlar orasidan tasodifiy element tanlab beruvchi generik extension yozing.

## Yechim (C# kodi):
```csharp
using System;

static class ArrayExtensions
{
    public static T RandomElement<T>(this T[] toplay, Random? rng = null)
    {
        rng ??= Random.Shared;
        int index = rng.Next(toplay.Length);
        return toplay[index];
    }
}

internal class Program
{
    static void Main()
    {
        string[] ismlar = [ "Ali", "Vali", "G'ani" ];
        int[] sonlar = [ 10, 20, 30, 40, 50 ];

        var rng = new Random(42);
        Console.WriteLine($"Tasodifiy ism: {ismlar.RandomElement(rng)}");
        Console.WriteLine($"Tasodifiy son: {sonlar.RandomElement(rng)}");
    }
}

```

## Tushuntirish va Mantiq:
Generik kengaytirish metodlari (`this T[] to'plam`) barcha turlar bilan bir xil ishlay oluvchi universal funksionallikni ta'minlaydi.

## Ishlash natijasi:
```text
Tasodifiy ism: Vali
Tasodifiy son: 30
```

# 173-Topshiriq: Metoddan bir nechta qiymat qaytarish: ValueTuple
## Topshiriq sharti:
`out` parametrlar o'rniga zamonaviy nomlangan `ValueTuple` orqali natija qaytaring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static (int Min, int Max, double Avg) TahlilQil(int[] massiv)
    {
        int min = massiv[0];
        int max = massiv[0];
        int sum = 0;

        foreach (var x in massiv)
        {
            if (x < min) min = x;
            if (x > max) max = x;
            sum += x;
        }

        return (min, max, (double)sum / massiv.Length);
    }

    static void Main()
    {
        var (min, max, avg) = TahlilQil([10, 20, 30, 40, 50]);
        Console.WriteLine($"Min: {min}, Max: {max}, O'rtacha: {avg}");
    }
}

```

## Tushuntirish va Mantiq:
`ValueTuple` metodlardan bir nechta qiymat qaytarishning eng toza va xavfsiz usulidir. U Stack da yashaydi va Heap da hech qanday ortiqcha xotira ajratmaydi.

## Ishlash natijasi:
```text
Min: 10, Max: 50, O'rtacha: 30
```

# 174-Topshiriq: C# 11 ArgumentNullException.ThrowIfNull Guard metodi
## Topshiriq sharti:
Metod parametrlarini tekshirishda zamonaviy bir qatorli Guard metodlaridan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void FoydalanuvchiniSaqlash(string? ism)
    {
        // C# 11 da kiritilgan statik Guard metodi
        ArgumentNullException.ThrowIfNull(ism);

        Console.WriteLine($"Foydalanuvchi muvaffaqiyatli saqlandi: {ism}");
    }

    static void Main()
    {
        FoydalanuvchiniSaqlash("Bobur");

        try
        {
            FoydalanuvchiniSaqlash(null);
        }
        catch (ArgumentNullException ex)
        {
            Console.WriteLine($"Xatolik ushlandi: {ex.ParamName} null bo'lishi mumkin emas!");
        }
    }
}

```

## Tushuntirish va Mantiq:
Eski `if (ism == null) throw new ArgumentNullException(nameof(ism));` o'rniga .NET 6/7/8 da `ArgumentNullException.ThrowIfNull(ism);` bir qatorda yoziladi. U `[CallerArgumentExpression]` orqali o'zgaruvchi nomini avtomatik ushlaydi.

## Ishlash natijasi:
```text
Foydalanuvchi muvaffaqiyatli saqlandi: Bobur
Xatolik ushlandi: ism null bo'lishi mumkin emas!
```

# 175-Topshiriq: C# 11 ArgumentOutOfRangeException Guard metodlari
## Topshiriq sharti:
`ThrowIfNegative` va `ThrowIfGreaterThan` metodlari orqali sonli diapazonlarni himoyalang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void MaoshBelgila(decimal maosh, int ishHaqiKunlari)
    {
        ArgumentOutOfRangeException.ThrowIfNegative(maosh);
        ArgumentOutOfRangeException.ThrowIfGreaterThan(ishHaqiKunlari, 31);

        Console.WriteLine($"Tasdiqlandi: Maosh={maosh:N0}, Kunlar={ishHaqiKunlari}");
    }

    static void Main()
    {
        MaoshBelgila(5000000m, 22);

        try
        {
            MaoshBelgila(-100m, 20);
        }
        catch (ArgumentOutOfRangeException ex)
        {
            Console.WriteLine($"Chegaradan chiqish xatosi: {ex.ParamName}");
        }
    }
}

```

## Tushuntirish va Mantiq:
.NET 8 da kiritilgan ushbu Guard metodlari nafaqat kodni qisqartiradi, balki JIT kompilyatoriga metodni yaxshiroq inline qilish imkonini beradi.

## Ishlash natijasi:
```text
Tasdiqlandi: Maosh=5,000,000, Kunlar=22
Chegaradan chiqish xatosi: maosh
```

# 176-Topshiriq: Rekursiya bilan Ikkilik Qidiruv Daraxtini (BST) aylanib chiqish
## Topshiriq sharti:
Ikkilik daraxt tugunlarini (TreeNode) In-Order usulida rekursiv aylanib chiquvchi metod yozing.

## Yechim (C# kodi):
```csharp
using System;

class DaraxtTuguni
{
    public int Qiymat;
    public DaraxtTuguni? Chap;
    public DaraxtTuguni? Ong;

    public DaraxtTuguni(int qiymat) => Qiymat = qiymat;
}

internal class Program
{
    static void InOrderAylan(DaraxtTuguni? tugun)
    {
        if (tugun == null) return;

        InOrderAylan(tugun.Chap);
        Console.Write($"{tugun.Qiymat} ");
        InOrderAylan(tugun.Ong);
    }

    static void Main()
    {
        var ildiz = new DaraxtTuguni(10)
        {
            Chap = new DaraxtTuguni(5),
            Ong = new DaraxtTuguni(15)
        };

        Console.Write("In-Order tartib: ");
        InOrderAylan(ildiz);
        Console.WriteLine();
    }
}

```

## Tushuntirish va Mantiq:
Daraxtsimon tuzilmalarni qayta ishlash rekursiyaning eng tabiiy va qulay sohasidir. In-Order usulida avval chap shox, so'ng joriy tugun, keyin o'ng shox aylanib chiqiladi va natijada sonlar o'sish tartibida chiqadi.

## Ishlash natijasi:
```text
In-Order tartib: 5 10 15
```

# 177-Topshiriq: Bo'lib tashla va hukmronlik qil (Divide and Conquer): Rekursiv Maksimum
## Topshiriq sharti:
Massivdagi eng katta elementni ikkiga bo'lish rekursiv usuli bilan toping.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static int MaxTop(int[] massiv, int chap, int ong)
    {
        if (chap == ong) return massiv[chap];

        int orta = (chap + ong) / 2;
        int maxChap = MaxTop(massiv, chap, orta);
        int maxOng = MaxTop(massiv, orta + 1, ong);

        return Math.Max(maxChap, maxOng);
    }

    static void Main()
    {
        int[] sonlar = [ 14, 82, 35, 99, 12, 73 ];
        int engKatta = MaxTop(sonlar, 0, sonlar.Length - 1);
        Console.WriteLine($"Maksimal element: {engKatta}");
    }
}

```

## Tushuntirish va Mantiq:
Divide and Conquer tamoyili muammoni kichikroq bo'laklarga ajratadi va ularning natijalarini birlashtiradi. Bu MergeSort va QuickSort kabi klassik algoritmlarning negizidir.

## Ishlash natijasi:
```text
Maksimal element: 99
```

# 178-Topshiriq: Rekursiv Evklid algoritmi (EKUB - Eng Katta Umumiy Bo'luvchi)
## Topshiriq sharti:
Ikki sonning eng katta umumiy bo'luvchisini (GCD) rekursiv Evklid algoritmi orqali hisoblang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static int Ekub(int a, int b)
    {
        if (b == 0) return a;
        return Ekub(b, a % b);
    }

    static void Main()
    {
        Console.WriteLine($"EKUB(48, 18): {Ekub(48, 18)}");
        Console.WriteLine($"EKUB(100, 25): {Ekub(100, 25)}");
    }
}

```

## Tushuntirish va Mantiq:
Evklid algoritmi $O(\log(\min(a, b)))$ vaqt oladi. Har bir qadamda ikkinchi son birinchi songa, ikkinchi songa esa qoldiq o'tkaziladi. Qoldiq 0 bo'lganda birinchi son javob bo'ladi.

## Ishlash natijasi:
```text
EKUB(48, 18): 6
EKUB(100, 25): 25
```

# 179-Topshiriq: Rekursiya bilan satrni teskarisiga o'girish
## Topshiriq sharti:
Satr belgilarini rekursiv ravishda teskari tartibda birlashtiruvchi metod yozing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static string Teskari(string s)
    {
        if (s.Length <= 1) return s;
        return Teskari(s[1..]) + s[0];
    }

    static void Main()
    {
        string matn = "TOSHKENT";
        Console.WriteLine($"Original: {matn}");
        Console.WriteLine($"Teskari:  {Teskari(matn)}");
    }
}

```

## Tushuntirish va Mantiq:
Ushbu rekursiv metod satrning boshidagi birinchi belgisini oxiriga qo'yadi va qolgan qismini yana o'ziga uzatadi. To'xtash sharti satr uzunligi 1 yoki undan kichik bo'lishidir.

## Ishlash natijasi:
```text
Original: TOSHKENT
Teskari:  TNEKHSOT
```

# 180-Topshiriq: Call Stack chuqurligi va StackOverflowException oldini olish
## Topshiriq sharti:
Juda chuqur rekursiya o'rniga nima uchun iterativ sikllar tanlanishi kerakligini tahlil qiling.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        // 100,000 marta rekursiv chaqiruv Stack xotirani to'ldirib dasturni qulatishi mumkin
        // Ammo iterativ sikl Stack da faqat 1 ta freym bilan cheksiz ishlay oladi
        long yigindi = 0;
        int n = 1_000_000;

        for (int i = 1; i <= n; i++)
        {
            yigindi += i;
        }

        Console.WriteLine($"1 dan {n} gacha yig'indi: {yigindi}");
        Console.WriteLine("Iterativ sikl StackOverflow xavfisiz xavfsiz bajarildi.");
    }
}

```

## Tushuntirish va Mantiq:
.NET da har bir oqim (Thread) uchun standart 1 MB Stack xotira ajratiladi. Har bir metod chaqiruvida parametrlar va qaytish manzili Stack ga joylashadi. Shuning uchun juda chuqur zanjirlarda doimo sikllardan foydalanish tavsiya etiladi.

## Ishlash natijasi:
```text
1 dan 1000000 gacha yig'indi: 500000500000
Iterativ sikl StackOverflow xavfisiz xavfsiz bajarildi.
```

# 181-Topshiriq: ref struct parametrlari bilan ishlovchi metodlar
## Topshiriq sharti:
`ReadOnlySpan<char>` parametrini qabul qiluvchi va satrdagi raqamlarni sanovchi yuqori tezlikdagi metod yozing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static int RaqamlarniSana(ReadOnlySpan<char> matn)
    {
        int sanoq = 0;
        foreach (char c in matn)
        {
            if (char.IsDigit(c)) sanoq++;
        }
        return sanoq;
    }

    static void Main()
    {
        string malumot = "Buyurtma №9482, sana: 2026-yil, narx: 75000";
        int sonlar = RaqamlarniSana(malumot);

        Console.WriteLine($"Matndagi raqamlar soni: {sonlar}");
    }
}

```

## Tushuntirish va Mantiq:
`ReadOnlySpan<T>` kabi `ref struct` lar metod parametrlari sifatida juda samarali. Ular nafaqat `string`, balki `char[]` yoki `stackalloc` orqali uzatilgan xotira qismlarini ham bir xil qabul qiladi.

## Ishlash natijasi:
```text
Matndagi raqamlar soni: 13
```

# 182-Topshiriq: Stack Frame hayot sikli: Metod ochilishi va yopilishi
## Topshiriq sharti:
Metod chaqirilganda lokal o'zgaruvchilar Stack da qanday yaratilishi va metod tugaganda qanday yo'qolishini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Hisoblash()
    {
        int lokalSon = 42; // Stack Frame ga yoziladi
        Console.WriteLine($"Lokal o'zgaruvchi yaratildi: {lokalSon}");
    } // Metod yakunlandi: Stack Frame tozalanishi bilan lokalSon xotiradan o'chadi

    static void Main()
    {
        Console.WriteLine("Main boshlandi");
        Hisoblash();
        Console.WriteLine("Main yakunlandi");
    }
}

```

## Tushuntirish va Mantiq:
Metod chaqiruvi protsessorda `call` instruksiyasini, tugashi esa `ret` (return) instruksiyasini bajaradi. Stack pointer (ESP/RSP registri) avvalgi joyiga qaytadi va barcha lokal o'zgaruvchilar 0 nanosaniyada yo'q qilinadi.

## Ishlash natijasi:
```text
Main boshlandi
Lokal o'zgaruvchi yaratildi: 42
Main yakunlandi
```

# 183-Topshiriq: Overloading va modifikatorlar: ref va out bo'yicha cheklov
## Topshiriq sharti:
Faqat `ref` va `out` farqi bo'yicha bir xil nomli metodlarni qayta yuklab bo'lmasligini tushuntiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    // static void Amal(ref int x) { }
    // static void Amal(out int x) { x = 0; } // XATO! Kompilyator faqat ref/out farqi bo'yicha overload qilishga ruxsat bermaydi

    static void Amal(ref int x) { x += 10; }
    static void Amal(int x) { Console.WriteLine($"Oddiy qiymat: {x}"); } // Bu esa ruxsat etiladi!

    static void Main()
    {
        int son = 5;
        Amal(son);
        Amal(ref son);
        Console.WriteLine($"ref bilan o'zgardi: {son}");
    }
}

```

## Tushuntirish va Mantiq:
CLR darajasida `ref` va `out` ikkalasi ham bir xil boshqariladigan ko'rsatkich (managed pointer `&`) sifatida ifodalanadi. Shuning uchun ularning faqat biri bilan overload qilish binar chalkashlikka olib keladi.

## Ishlash natijasi:
```text
Oddiy qiymat: 5
ref bilan o'zgardi: 15
```

# 184-Topshiriq: Ixtiyoriy parametrlar va Binar nomutanosiblik xavfi (Binary Compatibility)
## Topshiriq sharti:
Ixtiyoriy parametrlarning standart qiymati chaqiruvchi dastur ichiga yozilib qolishi (compile-time constant) sababli kutubxona yangilanishida yuz beradigan xavfni tushuntiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void SozlamaOqish(int timeoutSec = 30)
    {
        Console.WriteLine($"Joriy timeout: {timeoutSec} soniya");
    }

    static void Main()
    {
        SozlamaOqish(); // Kompilyator bu yerga 'SozlamaOqish(30)' deb yozib qo'yadi
    }
}

```

## Tushuntirish va Mantiq:
Agar kutubxonada `timeoutSec = 60` deb o'zgartirilsa, lekin asosiy dastur qayta kompilyatsiya qilinmasa, u hali ham eski `30` qiymatini uzatishda davom etadi. Shuning uchun umumiy API larda ixtiyoriy parametrlar o'rniga metod overloading tavsiya etiladi.

## Ishlash natijasi:
```text
Joriy timeout: 30 soniya
```

# 185-Topshiriq: Nomlangan argumentlar bilan ixtiyoriy parametrlarni aralashtirish
## Topshiriq sharti:
Ko'p ixtiyoriy parametrlar orasidan faqat kerakli bittasini nomlangan argument bilan uzatish usulini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void XabarYubor(string xabar, bool shifrlangan = false, int urinishlar = 3, string kanal = "SMS")
    {
        Console.WriteLine($"Xabar: '{xabar}', Kanal: {kanal}, Urinishlar: {urinishlar}, Shifrlangan: {shifrlangan}");
    }

    static void Main()
    {
        // O'rtadagi shifrlangan va urinishlar parametrlarini o'tkazib yuborib, faqat kanalni o'zgartirish
        XabarYubor("Parol tasdiqlandi", kanal: "Telegram");
    }
}

```

## Tushuntirish va Mantiq:
Nomlangan argumentlar yordamida o'rtadagi barcha ixtiyoriy parametrlarni yozib o'tirmasdan, faqat o'zingizga kerakli bo'lgan oxirgi parametrlarga qiymat berish mumkin.

## Ishlash natijasi:
```text
Xabar: 'Parol tasdiqlandi', Kanal: Telegram, Urinishlar: 3, Shifrlangan: False
```

# 186-Topshiriq: Local Function vs Lambda: Xotira va unumdorlik tahlili
## Topshiriq sharti:
Mahalliy funksiya (Local function) nima uchun anonim delegate va lambda ifodasiga qaraganda tezroq va xotira tejamkor ekanligini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        // Mahalliy funksiya: oddiy xususiy metodga aylanadi, delegate ob'yekti yaratmaydi
        int MahalliyQoshish(int a, int b) => a + b;

        // Lambda ifodasi: Func<int, int, int> delegate obyektini Heap da yaratadi
        Func<int, int, int> lambdaQoshish = (a, b) => a + b;

        Console.WriteLine($"Mahalliy funksiya: {MahalliyQoshish(10, 20)}");
        Console.WriteLine($"Lambda ifodasi:    {lambdaQoshish(10, 20)}");
    }
}

```

## Tushuntirish va Mantiq:
Mahalliy funksiyalar kompilyatsiya vaqtida oddiy statik yoki xususiy metodlarga aylanadi va to'g'ridan-to'g'ri chaqiriladi (`call`). Lambda esa `Func<>` ob'yektini Heap da ajratadi va virtual chaqiruv orqali ishlaydi.

## Ishlash natijasi:
```text
Mahalliy funksiya: 30
Lambda ifodasi:    30
```

# 187-Topshiriq: yield return bilan generator metod yaratish
## Topshiriq sharti:
`yield return` kalit so'zidan foydalanib xotirani to'ldirmasdan talab bo'yicha (on-demand) sonlar generatsiya qiluvchi metod yozing.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static IEnumerable<int> SonlarKetmaKetligi(int gacha)
    {
        for (int i = 1; i <= gacha; i++)
        {
            Console.WriteLine($"--> [Generatsiya qilindi: {i}]");
            yield return i;
        }
    }

    static void Main()
    {
        Console.WriteLine("Sikl boshlanmoqda:");
        foreach (int son in SonlarKetmaKetligi(3))
        {
            Console.WriteLine($"Qabul qilindi: {son}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`yield return` C# kompilyatori tomonidan orqada maxsus Holat Mashinasiga (State Machine) aylantiriladi. U barcha sonlarni birdaniga xotiraga yuklamaydi, balki har bir iteratsiyada faqat bittadan qiymat hosil qilib uzatadi.

## Ishlash natijasi:
```text
Sikl boshlanmoqda:
--> [Generatsiya qilindi: 1]
Qabul qilindi: 1
--> [Generatsiya qilindi: 2]
Qabul qilindi: 2
--> [Generatsiya qilindi: 3]
Qabul qilindi: 3
```

# 188-Topshiriq: yield break bilan ketma-ketlikni to'xtatish
## Topshiriq sharti:
Ma'lum shart bajarilganda generator faoliyatini `yield break` orqali yakunlang.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static IEnumerable<string> XabarlarOqimi()
    {
        yield return "1-Xabar: Aloqa o'rnatildi";
        yield return "2-Xabar: Ma'lumot uzatilmoqda";
        yield break; // Shu yerda to'xtatiladi
        yield return "3-Xabar: Bu qatorga yetib kelinmaydi";
    }

    static void Main()
    {
        foreach (var x in XabarlarOqimi())
        {
            Console.WriteLine(x);
        }
    }
}

```

## Tushuntirish va Mantiq:
`yield break` iterator blokidan erta chiqishni ta'minlaydi. U chaqiruvchi `foreach` ga boshqa elementlar yo'qligini bildiradi va `MoveNext()` ning `false` qaytarishiga sabab bo'ladi.

## Ishlash natijasi:
```text
1-Xabar: Aloqa o'rnatildi
2-Xabar: Ma'lumot uzatilmoqda
```

# 189-Topshiriq: Kechiktirilgan bajarilish (Deferred Execution) yield bilan
## Topshiriq sharti:
Metod chaqirilgan zahoti emas, balki to'plam elementlari aylanib chiqilgandagina ishga tushishini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static IEnumerable<int> KuchsizHisoblash()
    {
        Console.WriteLine(">> KuchsizHisoblash metodi ishga tushdi!");
        yield return 100;
    }

    static void Main()
    {
        Console.WriteLine("Metod chaqirilmoqda...");
        var oqim = KuchsizHisoblash(); // Hozircha hech narsa bajarilmaydi!

        Console.WriteLine("Endi foreach boshlanmoqda:");
        foreach (var x in oqim) // Aynan shu yerda kod ishlashni boshlaydi
        {
            Console.WriteLine($"Natija: {x}");
        }
    }
}

```

## Tushuntirish va Mantiq:
Deferred Execution (kechiktirilgan ijro) xotira va hisoblash resurslarini juda tejaydi. Agar ma'lumotlar o'qilmasa, ularni hisoblashga birorta ham protsessor vaqti sarflanmaydi.

## Ishlash natijasi:
```text
Metod chaqirilmoqda...
Endi foreach boshlanmoqda:
>> KuchsizHisoblash metodi ishga tushdi!
Natija: 100
```

# 190-Topshiriq: Extension metodda null obyekt bilan xavfsiz ishlash
## Topshiriq sharti:
Extension metodlar statik metod bo'lgani sababli `null` obyekt ustida chaqirilganda ham `NullReferenceException` bermasdan ishlashini namoyish eting.

## Yechim (C# kodi):
```csharp
using System;

static class SafeExtensions
{
    public static bool IsNullOrEmpty(this string? matn)
    {
        return string.IsNullOrEmpty(matn);
    }
}

internal class Program
{
    static void Main()
    {
        string? nullSatr = null;

        // null ustida xavfsiz metod chaqiruvi!
        bool boshmi = nullSatr.IsNullOrEmpty();

        Console.WriteLine($"nullSatr bo'shmi: {boshmi}");
    }
}

```

## Tushuntirish va Mantiq:
Kengaytirish metodlari chaqirilganda kompilyator uni `SafeExtensions.IsNullOrEmpty(nullSatr)` ko'rinishiga o'giradi. Shuning uchun ob'yektning o'zi `null` bo'lsa ham metod ichiga argument sifatida xavfsiz kirib boradi.

## Ishlash natijasi:
```text
nullSatr bo'shmi: True
```

# 191-Topshiriq: Fluent API va metodlarni zanjirlash (Method Chaining)
## Topshiriq sharti:
`return this` orqali metodlarni ketma-ket zanjir ko'rinishida chaqirish imkonini beruvchi Fluent Builder yarating.

## Yechim (C# kodi):
```csharp
using System;

class SqlSorovQuruvchi
{
    private string jadval = "";
    private string shart = "";

    public SqlSorovQuruvchi From(string jadvalNomi)
    {
        jadval = jadvalNomi;
        return this; // Zanjirni davom ettirish uchun o'zini qaytaradi
    }

    public SqlSorovQuruvchi Where(string shartMatni)
    {
        shart = shartMatni;
        return this;
    }

    public string Build() => $"SELECT * FROM {jadval} WHERE {shart};";
}

internal class Program
{
    static void Main()
    {
        var sorov = new SqlSorovQuruvchi()
            .From("Foydalanuvchilar")
            .Where("Yosh >= 18")
            .Build();

        Console.WriteLine(sorov);
    }
}

```

## Tushuntirish va Mantiq:
Fluent API uslubi kodni tabiiy til kabi o'qilishini ta'minlaydi. Har bir metod joriy obyekt holatini yangilab, `this` ni qaytaradi.

## Ishlash natijasi:
```text
SELECT * FROM Foydalanuvchilar WHERE Yosh >= 18;
```

# 192-Topshiriq: [CallerArgumentExpression] atributi bilan ifoda matnini olish
## Topshiriq sharti:
.NET 6+ da kiritilgan atribut yordamida parametrga uzatilgan kod ifodasining o'zini matn ko'rinishida oling.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.CompilerServices;

internal class Program
{
    static void Tasdiqla(bool shart, [CallerArgumentExpression(nameof(shart))] string? ifodaMatni = null)
    {
        if (!shart)
        {
            Console.WriteLine($"[TASDIQ XATOSI]: '{ifodaMatni}' ifodasi noto'g'ri bo'lib chiqdi!");
        }
        else
        {
            Console.WriteLine($"[TASDIQ MUVAFFOQIYATLI]: '{ifodaMatni}' to'g'ri.");
        }
    }

    static void Main()
    {
        int yosh = 20;
        Tasdiqla(yosh >= 18);
        Tasdiqla(yosh == 100);
    }
}

```

## Tushuntirish va Mantiq:
`[CallerArgumentExpression]` kompilyatsiya paytida chaqiruvchining argument sifatida yozgan kodini satr ko'rinishida ikkinchi parametrga avtomatik kiritadi. Bu test va tekshirish freymvorklari (xUnit, FluentAssertions) uchun juda muhim.

## Ishlash natijasi:
```text
[TASDIQ MUVAFFOQIYATLI]: 'yosh >= 18' to'g'ri.
[TASDIQ XATOSI]: 'yosh == 100' ifodasi noto'g'ri bo'lib chiqdi!
```

# 193-Topshiriq: Diagnostik atributlar: CallerMemberName, CallerFilePath va LineNumber
## Topshiriq sharti:
Log yozish metodiga chaqiruvchi metod nomi, fayl yo'li va qator raqamini kompilyator orqali avtomatik uzating.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.CompilerServices;

internal class Program
{
    static void Log(string xabar,
        [CallerMemberName] string metod = "",
        [CallerLineNumber] int qator = 0)
    {
        Console.WriteLine($"[{metod}:{qator}] - {xabar}");
    }

    static void SinovMetodi()
    {
        Log("Boshlang'ich amaliyot");
        Log("Tugallangan amaliyot");
    }

    static void Main()
    {
        SinovMetodi();
    }
}

```

## Tushuntirish va Mantiq:
`CallerInfo` atributlari kompilyatsiya vaqtida kod ichiga joylashtiriladi. Ular og'ir Reflection yoki StackTrace ob'yektlarini ishlatmasdan, 0 xarajat bilan aniq qator va metod ma'lumotlarini taqdim etadi.

## Ishlash natijasi:
```text
[SinovMetodi:16] - Boshlang'ich amaliyot
[SinovMetodi:17] - Tugallangan amaliyot
```

# 194-Topshiriq: [Conditional] atributi bilan shartli kompilyatsiya qilinuvchi metodlar
## Topshiriq sharti:
`[Conditional("DEBUG")]` atributidan foydalanib, faqat Debug rejimida ishlaydigan metod yozing.

## Yechim (C# kodi):
```csharp
using System;
using System.Diagnostics;

internal class Program
{
    [Conditional("DEBUG")]
    static void DebugLog(string xabar)
    {
        Console.WriteLine($"[DEBUG REJIMI]: {xabar}");
    }

    static void Main()
    {
        DebugLog("Bu xabar Debug rejimida chiqadi");
        Console.WriteLine("Asosiy dastur davom etmoqda.");
    }
}

```

## Tushuntirish va Mantiq:
`[Conditional]` atributli metodlar agar tegishli simvol (masalan `DEBUG`) aniqlanmagan bo'lsa (Release rejimida), kompilyator tomonidan chaqiruv nuqtalaridan butunlay olib tashlanadi (inlined away). Bu Release versiyada hech qanday unumdorlik yo'qotilishiga olib kelmaydi.

## Ishlash natijasi:
```text
[DEBUG REJIMI]: Bu xabar Debug rejimida chiqadi
Asosiy dastur davom etmoqda.
```

# 195-Topshiriq: Method Inlining: AggressiveInlining va NoInlining
## Topshiriq sharti:
JIT kompilyatoriga metodni to'g'ridan-to'g'ri chaqiruv joyiga kiritish (inline) yoki kiritmaslikni buyuruvchi atributlarni ko'rsating.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.CompilerServices;

internal class Program
{
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    static int TezkorQoshish(int a, int b) => a + b;

    [MethodImpl(MethodImplOptions.NoInlining)]
    static void OgirLog(string xabar) => Console.WriteLine(xabar);

    static void Main()
    {
        int natija = TezkorQoshish(10, 20);
        OgirLog($"Natija: {natija}");
    }
}

```

## Tushuntirish va Mantiq:
`AggressiveInlining` JIT ga metod chaqiruvini (call instruksiyasini) yo'qotib, metod tanasini to'g'ridan-to'g'ri o'sha joyga joylashtirishni buyuradi, bu kichik sikllarda juda katta tezlik beradi. `NoInlining` esa kam chaqiriladigan xatoliklarni qayta ishlash metodlari keshni bulg'amasligi uchun ishlatiladi.

## Ishlash natijasi:
```text
Natija: 30
```

# 196-Topshiriq: Pure Functions: Sof funksiyalar va determinizm
## Topshiriq sharti:
Hech qanday tashqi o'zgaruvchilarni o'zgartirmaydigan (yon ta'siri bo'lmagan) sof matematik funksiya tuzing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    // Sof funksiya (Pure Function):
    // 1. Bir xil argumentlar uchun har doim bir xil natija qaytaradi
    // 2. Tashqi holatni o'zgartirmaydi (No side effects)
    static double DoiraYuzi(double radius) => Math.PI * radius * radius;

    static void Main()
    {
        Console.WriteLine($"Radius 3 yuzi: {DoiraYuzi(3):F2}");
        Console.WriteLine($"Radius 3 yuzi: {DoiraYuzi(3):F2}");
    }
}

```

## Tushuntirish va Mantiq:
Sof funksiyalar dasturni kutilmagan xatolardan xoli qiladi, ularni testlash (Unit Testing) va parallel oqimlarda xavfsiz chaqirish (Thread-safe) juda oson.

## Ishlash natijasi:
```text
Radius 3 yuzi: 28.27
Radius 3 yuzi: 28.27
```

# 197-Topshiriq: Funksional kompozitsiya va qisman qo'llash (Partial Application)
## Topshiriq sharti:
Yuqori tartibli funksiyalar orqali parametrni oldindan biriktirib yangi funksiya hosil qiling.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static Func<int, int> KoPaytiruvchiYarat(int koPaytuvchi)
    {
        return x => x * koPaytuvchi;
    }

    static void Main()
    {
        var ikkigaKopaytir = KoPaytiruvchiYarat(2);
        var beshgaKopaytir = KoPaytiruvchiYarat(5);

        Console.WriteLine($"7 * 2 = {ikkigaKopaytir(7)}");
        Console.WriteLine($"7 * 5 = {beshgaKopaytir(7)}");
    }
}

```

## Tushuntirish va Mantiq:
Funksiya qaytaruvchi metodlar (High-order functions) funksional dasturlashning asosiy vositasidir. Tashqi argument ichki lambda xotirasida (closure) saqlanib qoladi.

## Ishlash natijasi:
```text
7 * 2 = 14
7 * 5 = 35
```

# 198-Topshiriq: Metod parametrlarini Guard va Validation bilan zanjirlash
## Topshiriq sharti:
Bir nechta tekshiruvlarni toza va xavfsiz bajaruvchi foydalanuvchi yaratish metodini yozing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void FoydalanuvchiQosh(string ism, int yosh, string email)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(ism);
        ArgumentOutOfRangeException.ThrowIfLessThan(yosh, 18);
        ArgumentException.ThrowIfNullOrWhiteSpace(email);

        Console.WriteLine($"Foydalanuvchi tasdiqlandi: {ism}, {yosh} yosh, {email}");
    }

    static void Main()
    {
        FoydalanuvchiQosh("Akmal", 25, "akmal@example.com");
    }
}

```

## Tushuntirish va Mantiq:
.NET 8 ning zamonaviy Guard metodlari xatoliklarni darhol va aniq parametr nomi bilan chiqaradi. Biznes mantiq xavfsiz va toza saqlanadi.

## Ishlash natijasi:
```text
Foydalanuvchi tasdiqlandi: Akmal, 25 yosh, akmal@example.com
```

# 199-Topshiriq: Rekursiyani Memoizatsiya (Keshlashtirish) bilan optimallashtirish
## Topshiriq sharti:
Fibonachchi hisoblashni massiv kesh orqali $O(2^N)$ dan $O(N)$ tezlikka oshiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static long FibKesh(int n, long[] kesh)
    {
        if (n <= 1) return n;
        if (kesh[n] != 0) return kesh[n]; // Keshda bo'lsa darhol qaytarish

        kesh[n] = FibKesh(n - 1, kesh) + FibKesh(n - 2, kesh);
        return kesh[n];
    }

    static void Main()
    {
        int n = 40;
        long[] kesh = new long[n + 1];

        Console.WriteLine($"Fibonachchi({n}) kesh bilan: {FibKesh(n, kesh)}");
    }
}

```

## Tushuntirish va Mantiq:
Memoizatsiya rekursiyaning eng katta kamchiligi bo'lgan qayta hisoblashlarni xotirada saqlash orqali bartaraf etadi va hisoblash vaqtini daqiqalardan millisoniyalarga tushiradi.

## Ishlash natijasi:
```text
Fibonachchi(40) kesh bilan: 102334155
```

# 200-Topshiriq: Metodlar va parametrlar bo'limi integratsiyalashgan arxitekturasi
## Topshiriq sharti:
Ushbu bo'limdagi barcha ilg'or imkoniyatlarni (`in`, `out`, `ref readonly`, `params Span`, `Guard`) jamlovchi professional hisoblash tizimini yarating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static bool Hisobla(in decimal asosiyNarx, out decimal chegirma, ref decimal balans, params ReadOnlySpan<decimal> qoshimchalar)
    {
        ArgumentOutOfRangeException.ThrowIfNegative(asosiyNarx);

        decimal jamiQoshimcha = 0;
        foreach (var q in qoshimchalar) jamiQoshimcha += q;

        decimal umumiy = asosiyNarx + jamiQoshimcha;
        chegirma = umumiy > 1_000_000m ? umumiy * 0.10m : 0m;
        decimal tolanadigan = umumiy - chegirma;

        if (balans >= tolanadigan)
        {
            balans -= tolanadigan;
            return true;
        }

        return false;
    }

    static void Main()
    {
        decimal balans = 2_000_000m;
        decimal narx = 1_200_000m;

        if (Hisobla(in narx, out decimal chegirma, ref balans, 50_000m, 30_000m))
        {
            Console.WriteLine($"Muvaffaqiyatli to'landi! Chegirma: {chegirma:N0} so'm, Qolgan balans: {balans:N0} so'm");
        }
    }
}

```

## Tushuntirish va Mantiq:
Ushbu yechim zamonaviy C# metodlarining to'liq kuchini ifodalaydi: `in` orqali xavfsiz va xotirasiz kirish, `out` orqali natijani ajratish, `ref` orqali balansni joyida o'zgartirish va `params ReadOnlySpan` orqali qo'shimchalarni 0 bayt GC yuki bilan qayta ishlash.

## Ishlash natijasi:
```text
Muvaffaqiyatli to'landi! Chegirma: 128,000 so'm, Qolgan balans: 848,000 so'm
```

