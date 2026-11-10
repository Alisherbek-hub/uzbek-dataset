# 3-Mavzu: Sikllar va Massivlar (101-150)

Ushbu bo'limda C# tilida takrorlanuvchi amallarni boshqarish va xotiradagi ma'lumotlar to'plamlari: `for`, `while`, `do-while`, `foreach`, `break`/`continue`, 1 o'lchovli va ko'p o'lchovli to'g'ri to'rtburchakli (`int[,]`) hamda pog'onali (`int[][]`) massivlar, `Array` sinfi metodlari, C# 8 Index va Range (`^`, `..`), C# 12 to'plam ifodalari (`[...]`), unumdorlikning eng yuqori cho'qqisi bo'lgan `Span<T>`, `ReadOnlySpan<T>`, `Memory<T>`, `stackalloc` hamda `ArrayPool<T>` texnologiyalari bo'yicha 50 ta amaliy topshiriq keltirilgan.

# 101-Topshiriq: Klassik for sikli: Hisoblagich va qadamlar
## Topshiriq sharti:
`for` sikli yordamida 1 dan 10 gacha bo'lgan juft sonlarni va ularning yig'indisini hisoblang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int yigindi = 0;

        Console.Write("Juft sonlar: ");
        for (int i = 2; i <= 10; i += 2)
        {
            Console.Write($"{i} ");
            yigindi += i;
        }
        Console.WriteLine();
        Console.WriteLine($"Jami juft sonlar yig'indisi: {yigindi}");
    }
}

```

## Tushuntirish va Mantiq:
`for` sikli uch qismdan iborat: initsializatsiya (`int i = 2`), davom etish sharti (`i <= 10`) va iteratsiya qadami (`i += 2`). Sikl har bir qadamda shartni tekshiradi va u `false` bo'lganda to'xtaydi.

## Ishlash natijasi:
```text
Juft sonlar: 2 4 6 8 10 
Jami juft sonlar yig'indisi: 30
```

# 102-Topshiriq: Teskari sanovchi for sikli (Reverse Loop)
## Topshiriq sharti:
Kosmik kema uchirilishini simulyatsiya qilib, 5 dan 1 gacha teskari sanovchi va oxirida 'Start!' xabarini chiqaruvchi sikl yozing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        for (int son = 5; son >= 1; son--)
        {
            Console.WriteLine($"Sanoq: {son}...");
        }
        Console.WriteLine("Start! Kema parvozga chiqdi!");
    }
}

```

## Tushuntirish va Mantiq:
Teskari siklda boshlang'ich qiymat katta olinadi va har bir iteratsiyada dekrement (`son--`) orqali kamaytirilib boriladi. Massivlarni oxiridan boshlab tekshirishda ham ushbu yondashuv ishlatiladi.

## Ishlash natijasi:
```text
Sanoq: 5...
Sanoq: 4...
Sanoq: 3...
Sanoq: 2...
Sanoq: 1...
Start! Kema parvozga chiqdi!
```

# 103-Topshiriq: Ichma-ich joylashgan for sikllari: Ko'paytirish jadvali
## Topshiriq sharti:
Ikki karra ichma-ich `for` siklidan foydalanib 1 dan 3 gacha bo'lgan kichik ko'paytirish jadvalini matritsa shaklida chiqaring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        for (int i = 1; i <= 3; i++)
        {
            for (int j = 1; j <= 3; j++)
            {
                Console.Write($"{i * j,4}");
            }
            Console.WriteLine();
        }
    }
}

```

## Tushuntirish va Mantiq:
Tashqi sikl satrlarni (`i`), ichki sikl esa ustunlarni (`j`) ifodalaydi. Ichki sikl to'liq aylanib bo'lgach, tashqi sikl keyingi qadamga o'tadi va yangi qator tashlanadi.

## Ishlash natijasi:
```text
1   2   3
   2   4   6
   3   6   9
```

# 104-Topshiriq: while sikli: Shart oldindan tekshiriladigan sikl
## Topshiriq sharti:
Bank omonatining yillik 10% foyda bilan 1000$ dan 1300$ ga yetishi uchun necha yil kerakligini `while` yordamida hisoblang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        double balans = 1000.0;
        int yil = 0;

        while (balans < 1300.0)
        {
            balans += balans * 0.10; // 10% qo'shildi
            yil++;
        }

        Console.WriteLine($"{yil} yildan keyin balans: {balans:F2}$ ga yetadi.");
    }
}

```

## Tushuntirish va Mantiq:
`while (shart)` sikli takrorlanishlar soni oldindan aniq ma'lum bo'lmaganda va jarayon ma'lum bir maqsadli shart bajarilguncha davom etishi kerak bo'lganda qo'llaniladi. Agar shart boshidayoq `false` bo'lsa, sikl umuman kirmaydi.

## Ishlash natijasi:
```text
3 yildan keyin balans: 1331.00$ ga yetadi.
```

# 105-Topshiriq: do-while sikli: Kamida bir marta bajarilish kafolati
## Topshiriq sharti:
Shart qanoatlantirilmasa ham tanasi kamida 1 marta bajariladigan `do-while` siklining ishlashini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int urinish = 1;

        do
        {
            Console.WriteLine($"Urinish raqami: {urinish} (Sikl tanasi kamida 1 marta bajarildi)");
            urinish++;
        }
        while (urinish <= 0); // Shart boshidayoq yolg'on!
    }
}

```

## Tushuntirish va Mantiq:
`do-while` siklida shart pastda (post-condition) tekshiriladi. Shuning uchun shart hatto dastlab `false` bo'lsa ham, sikl bloki aniq bitta marta to'liq ishga tushadi (masalan, foydalanuvchidan ma'lumot kiritishni so'rashda).

## Ishlash natijasi:
```text
Urinish raqami: 1 (Sikl tanasi kamida 1 marta bajarildi)
```

# 106-Topshiriq: foreach sikli va to'plamlarni xavfsiz aylanib chiqish
## Topshiriq sharti:
`foreach` yordamida satrlar massividagi har bir elementni o'qib chiqing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        string[] shaharlar = { "Toshkent", "Samarqand", "Buxoro", "Xiva" };

        Console.WriteLine("O'zbekistonning tarixiy shaharlari:");
        foreach (string shahar in shaharlar)
        {
            Console.WriteLine($"- {shahar}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`foreach` sikli `IEnumerable` yoki `IEnumerable<T>` interfeysini amalga oshirgan barcha to'plamlarda ishlaydi. U iterator (`GetEnumerator()`) mexanizmidan foydalanadi va indeks bilan bog'liq xatolar (masalan, chegaradan chiqib ketish) xavfini yo'qotadi.

## Ishlash natijasi:
```text
O'zbekistonning tarixiy shaharlari:
- Toshkent
- Samarqand
- Buxoro
- Xiva
```

# 107-Topshiriq: break operatori: Qidiruv va erta chiqish
## Topshiriq sharti:
Massiv ichidan manfiy son uchraganda qidiruvni darhol `break` bilan to'xtating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[] sonlar = { 10, 25, 40, -5, 60, 80 };

        foreach (int s in sonlar)
        {
            if (s < 0)
            {
                Console.WriteLine($"Birinchi manfiy son ({s}) topildi, sikl to'xtatildi!");
                break;
            }
            Console.WriteLine($"Qayta ishlandi: {s}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`break` operatori uni o'rab turgan eng yaqin siklni darhol yakunlaydi va dastur boshqaruvini sikldan keyingi birinchi qatorga uzatadi.

## Ishlash natijasi:
```text
Qayta ishlandi: 10
Qayta ishlandi: 25
Qayta ishlandi: 40
Birinchi manfiy son (-5) topildi, sikl to'xtatildi!
```

# 108-Topshiriq: continue operatori: Iteratsiyani o'tkazib yuborish
## Topshiriq sharti:
`continue` operatoridan foydalanib 1 dan 10 gacha bo'lgan sonlar orasidan 3 ga bo'linadiganlarini o'tkazib yuboring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        Console.Write("3 ga bo'linmaydigan sonlar: ");
        for (int i = 1; i <= 10; i++)
        {
            if (i % 3 == 0)
            {
                continue; // 3 ga karralilar uchun keyingi kodlar bajarilmaydi
            }
            Console.Write($"{i} ");
        }
        Console.WriteLine();
    }
}

```

## Tushuntirish va Mantiq:
`continue` sikl tanasining qolgan qismini bekor qilib, to'g'ridan-to'g'ri keyingi iteratsiyaga sakraydi. `for` siklida u qadam ifodasini (`i++`) bajarishga o'tadi.

## Ishlash natijasi:
```text
3 ga bo'linmaydigan sonlar: 1 2 4 5 7 8 10
```

# 109-Topshiriq: 1D Massivlar: E'lon qilish va xotirada joylashishi
## Topshiriq sharti:
Bir o'lchovli massiv e'lon qilishning turli usullarini ko'rsating va elementlarni indeks bo'yicha yangilang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[] m1 = new int[3]; // Standart nol bilan to'ldiriladi [0, 0, 0]
        m1[0] = 10;
        m1[1] = 20;
        m1[2] = 30;

        int[] m2 = new int[] { 100, 200, 300 };
        string[] hafta = { "Du", "Se", "Chor" };

        Console.WriteLine($"m1 ning 1-indeksi: {m1[1]}");
        Console.WriteLine($"m2 ning uzunligi: {m2.Length}");
        Console.WriteLine($"Hafta birinchi: {hafta[0]}");
    }
}

```

## Tushuntirish va Mantiq:
C# da barcha massivlar Reference Type (havola turi) hisoblanadi va Heap xotirada joylashadi. Massiv ob'yektining o'zi uning turi, uzunligi (`Length`) va ma'lumotlar buferini ketma-ket (contiguous memory) saqlaydi.

## Ishlash natijasi:
```text
m1 ning 1-indeksi: 20
m2 ning uzunligi: 3
Hafta birinchi: Du
```

# 110-Topshiriq: Massiv chegaralari va IndexOutOfRangeException
## Topshiriq sharti:
Massiv chegarasidan tashqariga murojaat qilinganda CLR qanday xavfsizlik tekshiruvini amalga oshirishini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[] sonlar = { 1, 2, 3 };

        try
        {
            int xato = sonlar[5]; // Mavjud bo'lmagan indeks!
        }
        catch (IndexOutOfRangeException ex)
        {
            Console.WriteLine($"Xatolik ushlandi: {ex.GetType().Name}");
            Console.WriteLine("CLR xotira xavfsizligini ta'minladi: chegaradan tashqariga chiqish taqiqlangan.");
        }
    }
}

```

## Tushuntirish va Mantiq:
CLR har bir massiv murojaatida indeks chegarasini (`0 <= index < Length`) qat'iy tekshiradi (Array Bounds Check). Bu C/C++ dagi bufer to'lib-toshishi (Buffer Overflow) kiberxavfsizlik muammolarini butunlay bartaraf etadi.

## Ishlash natijasi:
```text
Xatolik ushlandi: IndexOutOfRangeException
CLR xotira xavfsizligini ta'minladi: chegaradan tashqariga chiqish taqiqlangan.
```

# 111-Topshiriq: C# 12 To'plam ifodalari (Collection Expressions: [...])
## Topshiriq sharti:
C# 12 ning inqilobiy to'plam ifodalari (`[...]`) yordamida massiv va ro'yxatlarni yaratishni ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        // C# 12 to'plam sintaksisi: new int[] yoki new() yozish shart emas
        int[] sonlar = [10, 20, 30, 40, 50];
        string[] mevalar = ["Olma", "Anor", "Uzum"];
        int[] bosh = [];

        Console.WriteLine($"Sonlar soni: {sonlar.Length}, birinchi element: {sonlar[0]}");
        Console.WriteLine($"Mevalar: {string.Join(", ", mevalar)}");
        Console.WriteLine($"Bo'sh to'plam hajmi: {bosh.Length}");
    }
}

```

## Tushuntirish va Mantiq:
C# 12 da kiritilgan Collection Expressions (`[...]`) to'plamlar sintaksisini unifikatsiya qildi. U massiv, `List<T>`, `Span<T>` yoki boshqa to'plam turlari uchun bir xil toza sintaksis taqdim etadi.

## Ishlash natijasi:
```text
Sonlar soni: 5, birinchi element: 10
Mevalar: Olma, Anor, Uzum
Bo'sh to'plam hajmi: 0
```

# 112-Topshiriq: C# 12 Spread operatori (..) bilan to'plamlarni birlashtirish
## Topshiriq sharti:
`..` spread operatori yordamida bir nechta massiv elementlarini yagona yangi massivga birlashtiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[] qism1 = [1, 2, 3];
        int[] qism2 = [7, 8, 9];

        // qism1 va qism2 orasiga 4, 5, 6 sonlarini qo'shib birlashtirish
        int[] birlashgan = [..qism1, 4, 5, 6, ..qism2];

        Console.WriteLine("Birlashgan to'plam: " + string.Join(" ", birlashgan));
    }
}

```

## Tushuntirish va Mantiq:
Spread operatori (`..to'plam`) mavjud to'plam ichidagi barcha elementlarni yangi yaratilayotgan to'plam ichiga yoyib (flatten) joylashtiradi. Bu `Concat` yoki `AddRange` metodlariga nisbatan ancha qulay va tezkor ishlaydi.

## Ishlash natijasi:
```text
Birlashgan to'plam: 1 2 3 4 5 6 7 8 9
```

# 113-Topshiriq: C# 8 Index operatori: ^ (Oxiridan indekslash)
## Topshiriq sharti:
`^` operatori yordamida massivning oxirgi va oxiridan oldingi elementlarini osonlikcha oling.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        string[] tillar = [ "C#", "F#", "Rust", "Go", "Python" ];

        string oxirgi = tillar[^1];    // Oxirgi element (Length - 1)
        string oldingi = tillar[^2];   // Oxiridan ikkinchi element (Length - 2)

        Console.WriteLine($"Eng oxirgi til: {oxirgi}");
        Console.WriteLine($"Oxiridan 2-til: {oldingi}");
    }
}

```

## Tushuntirish va Mantiq:
`^n` (System.Index) operatori to'plamning oxiridan hisoblashni bildiradi: `^1` eng oxirgi element, `^2` oxiridan ikkinchi element va hokazo. Bu `tillar[tillar.Length - 1]` kabi ortiqcha kodlarni yo'q qiladi.

## Ishlash natijasi:
```text
Eng oxirgi til: Python
Oxiridan 2-til: Go
```

# 114-Topshiriq: C# 8 Range operatori: .. (Massivdan kesma olish)
## Topshiriq sharti:
`..` (System.Range) operatori yordamida massivning ma'lum bir oralig'idagi elementlarini kesib oling.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[] raqamlar = [ 0, 10, 20, 30, 40, 50, 60, 70 ];

        int[] oraliq = raqamlar[2..5];      // 2-indeksdan 5-indeksgacha (5 kirmaydi: 20, 30, 40)
        int[] boshidan = raqamlar[..3];     // 0 dan 3 gacha (0, 10, 20)
        int[] oxirigacha = raqamlar[5..];   // 5 dan oxirigacha (50, 60, 70)
        int[] oxirgiIkkitasiz = raqamlar[..^2]; // Boshidan oxirgi 2 tasigacha

        Console.WriteLine("2..5 oralig'i: " + string.Join(", ", oraliq));
        Console.WriteLine("..3 oralig'i:  " + string.Join(", ", boshidan));
        Console.WriteLine("5.. oralig'i:  " + string.Join(", ", oxirigacha));
        Console.WriteLine("..^2 oralig'i: " + string.Join(", ", oxirgiIkkitasiz));
    }
}

```

## Tushuntirish va Mantiq:
`boshlanish..oxirgi` diapazoni yarim ochiq oraliqdir (chap chegara kiradi, o'ng chegara kirmaydi). Massiv ustida Range qo'llanganda, Heap da yangi qirqilgan massiv nusxasi hosil qilinadi.

## Ishlash natijasi:
```text
2..5 oralig'i: 20, 30, 40
..3 oralig'i:  0, 10, 20
5.. oralig'i:  50, 60, 70
..^2 oralig'i: 0, 10, 20, 30, 40, 50
```

# 115-Topshiriq: Array.Sort: Massivni o'sish va kamayish bo'yicha saralash
## Topshiriq sharti:
`Array.Sort` yordamida sonlar massivini tartiblang, so'ng teskari tartibda saralashni ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[] sonlar = [ 45, 12, 89, 3, 27, 64 ];

        Array.Sort(sonlar); // O'sish tartibida
        Console.WriteLine("O'sish tartibida: " + string.Join(", ", sonlar));

        Array.Reverse(sonlar); // Teskarisiga o'girish (kamayish tartibi)
        Console.WriteLine("Kamayish tartibida: " + string.Join(", ", sonlar));
    }
}

```

## Tushuntirish va Mantiq:
`Array.Sort` .NET da IntroSort algoritmini ishlatadi (QuickSort, HeapSort va InsertionSort larning gibridi bo'lib, eng yomon holatda ham $O(N \log N)$ vaqt murakkabligini kafolatlaydi).

## Ishlash natijasi:
```text
O'sish tartibida: 3, 12, 27, 45, 64, 89
Kamayish tartibida: 89, 64, 45, 27, 12, 3
```

# 116-Topshiriq: Array.BinarySearch: Ikkilik qidiruv va uning talabi
## Topshiriq sharti:
`Array.BinarySearch` metodi orqali saralangan massiv ichidan element indeksini $O(\log N)$ tezlikda toping.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[] tartiblangan = [ 10, 25, 33, 47, 58, 62, 79, 91 ];

        int qidirilgan = 47;
        int indeks = Array.BinarySearch(tartiblangan, qidirilgan);
        Console.WriteLine($"{qidirilgan} soni {indeks}-indeksda joylashgan.");

        int mavjudEmas = 50;
        int manfiyIndeks = Array.BinarySearch(tartiblangan, mavjudEmas);
        Console.WriteLine($"{mavjudEmas} soni topilmadi, manfiy qiymat: {manfiyIndeks}");
    }
}

```

## Tushuntirish va Mantiq:
BinarySearch ishlashi uchun massiv mutlaqo saralangan bo'lishi shart! Agar element topilmasa, metod manfiy son qaytaradi (ushbu son element qo'yilishi mumkin bo'lgan indeksning bitwise to'ldiruvchisi `~indeks` dir).

## Ishlash natijasi:
```text
47 soni 3-indeksda joylashgan.
50 soni topilmadi, manfiy qiymat: -5
```

# 117-Topshiriq: Array.Find va Array.FindAll: Shart bo'yicha qidirish
## Topshiriq sharti:
`Array.Find` (birinchi mos kelgan) va `Array.FindAll` (barcha mos kelganlar) metodlarini lambda bilan ishlating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[] sonlar = [ 15, 8, 42, 4, 16, 23 ];

        // 20 dan katta bo'lgan birinchi son
        int birinchi = Array.Find(sonlar, x => x > 20);
        Console.WriteLine($"20 dan katta birinchi son: {birinchi}");

        // Barcha juft sonlar
        int[] juftlar = Array.FindAll(sonlar, x => x % 2 == 0);
        Console.WriteLine("Barcha juft sonlar: " + string.Join(", ", juftlar));
    }
}

```

## Tushuntirish va Mantiq:
`Array.Find` va `FindAll` metodlari predikat (`Predicate<T>`) qabul qiladi. `Find` birinchi uchragan elementni qaytaradi (topilmasa `default`), `FindAll` esa yangi filtrlangan massiv yaratadi.

## Ishlash natijasi:
```text
20 dan katta birinchi son: 42
Barcha juft sonlar: 8, 42, 4, 16
```

# 118-Topshiriq: Array.Exists va Array.TrueForAll tekshiruvlari
## Topshiriq sharti:
Massivda shartga mos kamida bitta element borligini (`Exists`) yoki hamma elementlar mosligini (`TrueForAll`) tekshiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[] baholar = [ 85, 90, 78, 92, 88 ];

        bool aloBormi = Array.Exists(baholar, b => b >= 90);
        bool hammasiIjobiymi = Array.TrueForAll(baholar, b => b >= 60);

        Console.WriteLine($"90 dan yuqori ball bormi: {aloBormi}");
        Console.WriteLine($"Hamma talabalar o'tdimi: {hammasiIjobiymi}");
    }
}

```

## Tushuntirish va Mantiq:
`Array.Exists` LINQ dagi `.Any()`, `Array.TrueForAll` esa `.All()` ga to'g'ri keladi, ammo massivlar uchun to'g'ridan-to'g'ri optimallashgan bo'lib, iterator obyektlarini Heap da ajratmaydi.

## Ishlash natijasi:
```text
90 dan yuqori ball bormi: True
Hamma talabalar o'tdimi: True
```

# 119-Topshiriq: Array.Copy: Xotirani to'g'ridan-to'g'ri nusxalash
## Topshiriq sharti:
`Array.Copy` yordamida bitta massivning belgilangan qismini boshqa massivning ko'rsatilgan joyiga xavfsiz ko'chiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[] manba = [ 10, 20, 30, 40, 50 ];
        int[] maqsad = new int[5]; // [0, 0, 0, 0, 0]

        // manba massivining 1-indeksidan boshlab 3 ta elementni maqsad ning 2-indeksiga nusxalash
        Array.Copy(manba, 1, maqsad, 2, 3);

        Console.WriteLine("Maqsad massiv: " + string.Join(", ", maqsad));
    }
}

```

## Tushuntirish va Mantiq:
`Array.Copy` past darajadagi blokli xotira nusxalashidan (memmove/memcpy) foydalanadi. U oddiy `for` sikliga nisbatan bir necha barobar tez ishlaydi va elementlar turi mosligini tekshiradi.

## Ishlash natijasi:
```text
Maqsad massiv: 0, 0, 20, 30, 40
```

# 120-Topshiriq: Array.Resize: Massiv hajmini o'zgartirish illuziyasi
## Topshiriq sharti:
`Array.Resize` metodidan foydalaning va uning aslida yangi massiv yaratishini tushuntiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[] massiv = [ 1, 2, 3 ];
        int[] aslHavola = massiv;

        // Hajmni 5 tagacha oshirish
        Array.Resize(ref massiv, 5);
        massiv[3] = 4;
        massiv[4] = 5;

        Console.WriteLine("Yangi massiv: " + string.Join(", ", massiv));
        Console.WriteLine($"Asl havola bilan bittami: {object.ReferenceEquals(massiv, aslHavola)}");
    }
}

```

## Tushuntirish va Mantiq:
Massivlar xotirada qat'iy o'lchamga ega. `Array.Resize(ref massiv, yangiHajm)` aslida yangi massiv yaratadi, eski elementlarni unga nusxalaydi va `ref` orqali yangi havola manzilini qaytaradi.

## Ishlash natijasi:
```text
Yangi massiv: 1, 2, 3, 4, 5
Asl havola bilan bittami: False
```

# 121-Topshiriq: Array.Clear: Elementlarni tozalash va standart qiymatga keltirish
## Topshiriq sharti:
`Array.Clear` yordamida massivning ma'lum bir oralig'ini tozalang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[] raqamlar = [ 100, 200, 300, 400, 500 ];

        // 1-indeksdan boshlab 3 ta elementni tozalash (0 ga aylantirish)
        Array.Clear(raqamlar, 1, 3);

        Console.WriteLine("Tozalangan massiv: " + string.Join(", ", raqamlar));
    }
}

```

## Tushuntirish va Mantiq:
`Array.Clear` massiv elementlarini o'chirmaydi (massiv uzunligi o'zgarmaydi), balki ko'rsatilgan oraliqdagi katakchalarni ularning standart qiymatiga (sonlar uchun 0, havolalar uchun `null`) qaytaradi.

## Ishlash natijasi:
```text
Tozalangan massiv: 100, 0, 0, 0, 500
```

# 122-Topshiriq: 2D To'g'ri to'rtburchakli massivlar (Rectangular Arrays: [,])
## Topshiriq sharti:
2 o'lchovli matritsani (`int[,]`) e'lon qiling, initsializatsiya qiling va `GetLength` orqali chiqaring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[,] matritsa = new int[2, 3]
        {
            { 1, 2, 3 },
            { 4, 5, 6 }
        };

        Console.WriteLine($"Satrlar soni (0-o'lcham): {matritsa.GetLength(0)}");
        Console.WriteLine($"Ustunlar soni (1-o'lcham): {matritsa.GetLength(1)}");

        for (int i = 0; i < matritsa.GetLength(0); i++)
        {
            for (int j = 0; j < matritsa.GetLength(1); j++)
            {
                Console.Write($"{matritsa[i, j]} ");
            }
            Console.WriteLine();
        }
    }
}

```

## Tushuntirish va Mantiq:
`int[,]` to'g'ri to'rtburchakli ko'p o'lchovli massiv bo'lib, Heap xotirada yagona uzluksiz xotira bloki sifatida saqlanadi. Har bir satrda ustunlar soni bir xil bo'lishi shart.

## Ishlash natijasi:
```text
Satrlar soni (0-o'lcham): 2
Ustunlar soni (1-o'lcham): 3
1 2 3 
4 5 6
```

# 123-Topshiriq: Pog'onali massivlar (Jagged Arrays: [][])
## Topshiriq sharti:
Har bir satrida har xil sondagi elementlar bo'lgan pog'onali massiv (`int[][]`) yarating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        // 3 ta satrdan iborat pog'onali massiv
        int[][] pogonali = new int[3][];
        pogonali[0] = [ 1, 2 ];
        pogonali[1] = [ 10, 20, 30, 40 ];
        pogonali[2] = [ 100 ];

        for (int i = 0; i < pogonali.Length; i++)
        {
            Console.Write($"Qator {i} ({pogonali[i].Length} ta): ");
            foreach (int son in pogonali[i])
            {
                Console.Write($"{son} ");
            }
            Console.WriteLine();
        }
    }
}

```

## Tushuntirish va Mantiq:
Jagged Array bu 'massivlar massividir'. Asosiy massiv faqat boshqa kichik massivlarga havolalarni saqlaydi. Natijada har bir satr alohida Heap obyekt bo'lib, istalgancha turli uzunlikka ega bo'lishi mumkin.

## Ishlash natijasi:
```text
Qator 0 (2 ta): 1 2 
Qator 1 (4 ta): 10 20 30 40 
Qator 2 (1 ta): 100
```

# 124-Topshiriq: Jagged vs Rectangular Array: Xotira va kesh tahlili
## Topshiriq sharti:
Jagged va Rectangular massivlarning xotiradagi tuzilishi va qachon qaysi birini tanlash kerakligini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        // Rectangular: Bitta katta uzluksiz xotira bloki
        int[,] togridan = new int[100, 100];

        // Jagged: 1 ta asosiy massiv + 100 ta alohida bolalar massivi (101 ta obyekt Heap da)
        int[][] pogonali = new int[100][];
        for (int i = 0; i < 100; i++) pogonali[i] = new int[100];

        Console.WriteLine("Taqqoslash:");
        Console.WriteLine("- int[,] bitta yaxlit obyekt (CPU kesh uchun qulay).");
        Console.WriteLine("- int[][] ko'p ob'yektli, lekin JIT kompilyator elementlarga murojaatni tezroq bajarishi mumkin.");
    }
}

```

## Tushuntirish va Mantiq:
`int[,]` yagona ob'yekt bo'lib xotira tarqoqligini (fragmentation) kamaytiradi. Biroq .NET JIT kompilyatori 1 o'lchovli massivlar ustida ishlovchi `int[][]` ga nisbatan chegaralarni tekshirishni (bounds checking) osonroq optimallashtiradi.

## Ishlash natijasi:
```text
Taqqoslash:
- int[,] bitta yaxlit obyekt (CPU kesh uchun qulay).
- int[][] ko'p ob'yektli, lekin JIT kompilyator elementlarga murojaatni tezroq bajarishi mumkin.
```

# 125-Topshiriq: Massivni faqat o'qiladigan qilish: Array.AsReadOnly
## Topshiriq sharti:
Mavjud massivni o'zgartirishlardan himoya qilish uchun `Array.AsReadOnly` orqali `ReadOnlyCollection<T>` oling.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.ObjectModel;

internal class Program
{
    static void Main()
    {
        string[] original = [ "Dushanba", "Seshanba", "Chorshanba" ];
        ReadOnlyCollection<string> himoyalangan = Array.AsReadOnly(original);

        Console.WriteLine($"1-element: {himoyalangan[0]}");
        Console.WriteLine($"Jami elementlar: {himoyalangan.Count}");

        // himoyalangan[0] = "Boshqa"; // KOMPILYATSIYA XATOSI! O'zgartirib bo'lmaydi
    }
}

```

## Tushuntirish va Mantiq:
`Array.AsReadOnly(massiv)` asl massiv ustiga yupqa qobiq (wrapper) yaratadi. Yangi nusxa olinmaydi, ammo tashqi kod uchun massiv elementlarini o'zgartirish qat'iyan man etiladi.

## Ishlash natijasi:
```text
1-element: Dushanba
Jami elementlar: 3
```

# 126-Topshiriq: Jagged massiv yordamida Paskal uchburchagini qurish
## Topshiriq sharti:
Pog'onali massiv (`int[][]`) yordamida 5 qatorli Paskal uchburchagini hisoblab konsolga chiqaring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int qatorlarSoni = 5;
        int[][] paskal = new int[qatorlarSoni][];

        for (int i = 0; i < qatorlarSoni; i++)
        {
            paskal[i] = new int[i + 1];
            paskal[i][0] = 1;
            paskal[i][^1] = 1;

            for (int j = 1; j < i; j++)
            {
                paskal[i][j] = paskal[i - 1][j - 1] + paskal[i - 1][j];
            }
        }

        for (int i = 0; i < qatorlarSoni; i++)
        {
            Console.WriteLine(string.Join(" ", paskal[i]));
        }
    }
}

```

## Tushuntirish va Mantiq:
Paskal uchburchagida har bir satr uzunligi avvalgisidan 1 taga uzun bo'ladi. Jagged Array har bir qator uchun aniq kerakli hajmda xotira ajratish imkonini berib, keraksiz katakchalar sarfini yo'qotadi.

## Ishlash natijasi:
```text
1
1 1
1 2 1
1 3 3 1
1 4 6 4 1
```

# 127-Topshiriq: Span<T> asoslari: Xotirada nol nusxa (Zero-allocation) oynasi
## Topshiriq sharti:
`Span<int>` yordamida massivning o'rtasidagi elementlarni Heap da yangi massiv yaratmasdan to'g'ridan-to'g'ri o'zgartiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[] sonlar = [ 10, 20, 30, 40, 50 ];

        // sonlar massivining 1-indeksidan boshlab 3 ta elementiga 'oyna' (Span) ochish
        Span<int> oyna = sonlar.AsSpan(1, 3);

        // Span orqali o'zgartirish to'g'ridan-to'g'ri asl massivda aks etadi
        oyna[0] = 999;

        Console.WriteLine("Oyna elementlari: " + string.Join(", ", oyna.ToArray()));
        Console.WriteLine("Asl massiv: " + string.Join(", ", sonlar));
    }
}

```

## Tushuntirish va Mantiq:
`Span<T>` bu `ref struct` bo'lib, xotiraning uzluksiz bo'lagiga (massiv, stackalloc yoki native xotira) havola ko'rsatuvchi yengil oynadir. U nusxalamaydi, xotira ajratmaydi va to'g'ridan-to'g'ri ko'rsatkich tezligida ishlaydi.

## Ishlash natijasi:
```text
Oyna elementlari: 999, 30, 40
Asl massiv: 10, 999, 30, 40, 50
```

# 128-Topshiriq: ReadOnlySpan<T>: Xavfsiz faqat o'qiladigan xotira kesmasi
## Topshiriq sharti:
`ReadOnlySpan<char>` orqali satr ustida o'zgartirish xavfisiz yuqori tezlikda amallar bajaring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        string matn = "O'zbekiston Kelajagi Buyuk Davlat";

        // Satrning bir qismini Heap da yangi string ajratmasdan ko'rish
        ReadOnlySpan<char> qism = matn.AsSpan(12, 8); // "Kelajagi"

        Console.WriteLine($"Ajratilgan qism uzunligi: {qism.Length}");
        Console.WriteLine($"Qism matni: {qism.ToString()}");
    }
}

```

## Tushuntirish va Mantiq:
Oddiy `matn.Substring(12, 8)` har chaqirilganda Heap da yangi `string` ob'yekti yaratadi va GC ga yuk bo'ladi. `AsSpan()` esa mavjud xotiraning ustiga `ReadOnlySpan` qo'yadi va hech qanday bayt ajratmaydi (0 bayt GC allocation).

## Ishlash natijasi:
```text
Ajratilgan qism uzunligi: 8
Qism matni: Kelajagi
```

# 129-Topshiriq: Span bilan xotirasiz parsing (Zero-Allocation Date Parsing)
## Topshiriq sharti:
Sana matnini (`"2026-11-08"`) `ReadOnlySpan<char>` va `int.Parse` yordamida Heap da birorta ham satr yaratmasdan sonlarga ajrating.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        string sanaMatni = "2026-11-08";
        ReadOnlySpan<char> span = sanaMatni.AsSpan();

        int yil = int.Parse(span.Slice(0, 4));
        int oy = int.Parse(span.Slice(5, 2));
        int kun = int.Parse(span.Slice(8, 2));

        Console.WriteLine($"Yil: {yil}, Oy: {oy}, Kun: {kun}");
    }
}

```

## Tushuntirish va Mantiq:
.NET Core 2.1+ va zamonaviy .NET da `int.Parse`, `double.Parse` kabi barcha asosiy metodlar `ReadOnlySpan<char>` ni qabul qiluvchi o'ta tezkor overloads ga ega. `span.Slice()` mutlaqo yangi matn yaratmaydi.

## Ishlash natijasi:
```text
Yil: 2026, Oy: 11, Kun: 8
```

# 130-Topshiriq: Memory<T> va ReadOnlyMemory<T>: Heap ga mos xotira oynasi
## Topshiriq sharti:
`Span<T>` stack-only bo'lganligi sababli uni sinf maydonida yoki asinxron metodlarda saqlab bo'lmaydi. Bu vaziyatda `Memory<T>` dan foydalaning.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static async Task QaytaIshlaAsync(ReadOnlyMemory<byte> bufer)
    {
        await Task.Delay(10); // Asinxron operatsiya
        Console.WriteLine($"Asinxron qayta ishlangan baytlar soni: {bufer.Length}");
    }

    static async Task Main()
    {
        byte[] malumot = [ 1, 2, 3, 4, 5, 6, 7, 8 ];
        ReadOnlyMemory<byte> memory = malumot.AsMemory(2, 4);

        await QaytaIshlaAsync(memory);
    }
}

```

## Tushuntirish va Mantiq:
`Memory<T>` oddiy `struct` bo'lib, `Span<T>` kabi `ref struct` emas. Shuning uchun u Heap da saqlanishi, sinf maydonlarida turishi va `async/await` chegaralaridan o'tishi mumkin. Undan kerakli vaqtda `.Span` orqali tezkor Span olish mumkin.

## Ishlash natijasi:
```text
Asinxron qayta ishlangan baytlar soni: 4
```

# 131-Topshiriq: stackalloc operatori: Heap ga chiqmasdan to'g'ridan-to'g'ri Stack dan joy ajratish
## Topshiriq sharti:
`stackalloc` operatori yordamida Stack xotirada tezkor massiv ajrating va unga `Span<int>` orqali murojaat qiling.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        // Stack xotirada 4 ta int ajratish (16 bayt) - Garbage Collector umuman aralashmaydi!
        Span<int> tezkorBufer = stackalloc int[4];

        for (int i = 0; i < tezkorBufer.Length; i++)
        {
            tezkorBufer[i] = (i + 1) * 10;
        }

        Console.Write("Stackdagi bufer qiymatlari: ");
        foreach (int qiymat in tezkorBufer)
        {
            Console.Write($"{qiymat} ");
        }
        Console.WriteLine();
    }
}

```

## Tushuntirish va Mantiq:
`stackalloc` xotirani Stack freymidan ajratadi. Metod tugashi bilan ushbu xotira bir zumda avtomatik yo'qoladi, Garbage Collector ga hech qanday bosim bo'lmaydi. C# 7.2 dan boshlab `unsafe` so'zisiz bevosita `Span<T>` bilan xavfsiz ishlatiladi.

## Ishlash natijasi:
```text
Stackdagi bufer qiymatlari: 10 20 30 40
```

# 132-Topshiriq: ArrayPool<T>: Katta massivlarni qayta ishlatish (Object Pooling)
## Topshiriq sharti:
`ArrayPool<T>.Shared` yordamida massivlarni Heap da doimiy yaratish o'rniga, tayyor hovuzdan ijaraga oling va qaytaring.

## Yechim (C# kodi):
```csharp
using System;
using System.Buffers;

internal class Program
{
    static void Main()
    {
        // 1000 ta elementli massivni ijaraga olish
        int[] bufer = ArrayPool<int>.Shared.Rent(1000);

        try
        {
            Console.WriteLine($"Ijaraga berilgan massiv haqiqiy hajmi: {bufer.Length} (kamida 1000)");
            bufer[0] = 777;
            Console.WriteLine($"Birinchi element: {bufer[0]}");
        }
        finally
        {
            // Ishlatib bo'lingach, massivni hovuzga qaytarish shart
            ArrayPool<int>.Shared.Return(bufer);
            Console.WriteLine("Massiv muvaffaqiyatli hovuzga qaytarildi.");
        }
    }
}

```

## Tushuntirish va Mantiq:
Yuqori yuklamali veb-serverlarda (masalan Kestrel/ASP.NET Core) har bir so'rov uchun yangi massiv ajratish xotira fragmentatsiyasiga olib keladi. `ArrayPool<T>` massivlarni qayta-qayta ishlatib, GC to'xtashlarini (Gen 2 pauses) bartaraf etadi.

## Ishlash natijasi:
```text
Ijaraga berilgan massiv haqiqiy hajmi: 1024 (kamida 1000)
Birinchi element: 777
Massiv muvaffaqiyatli hovuzga qaytarildi.
```

# 133-Topshiriq: Sayoz nusxa (Shallow Copy) vs Chuqur nusxa (Deep Copy) massivlarda
## Topshiriq sharti:
Obyektlar massivini `Clone()` qilganda faqat havolalar nusxalanishi va haqiqiy chuqur nusxalash farqini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;

class Mahsulot
{
    public string Nomi { get; set; } = "";
}

internal class Program
{
    static void Main()
    {
        Mahsulot[] original = [ new Mahsulot { Nomi = "Kitob" } ];

        // Shallow Copy
        Mahsulot[] sayozNusxa = (Mahsulot[])original.Clone();
        sayozNusxa[0].Nomi = "O'zgardi";

        Console.WriteLine($"Originaldagi mahsulot nomi: {original[0].Nomi} (Sayoz nusxa ta'sir qildi!)");
    }
}

```

## Tushuntirish va Mantiq:
`massiv.Clone()` faqat 1-darajali massiv katakchalarini nusxalaydi. Agar massiv elementlari havola turi (obyekt) bo'lsa, havolalarning o'zi ko'chiriladi, natijada ikkala massiv ham aynan bir xil obyektlarga qaraydi.

## Ishlash natijasi:
```text
Originaldagi mahsulot nomi: O'zgardi (Sayoz nusxa ta'sir qildi!)
```

# 134-Topshiriq: foreach ichida to'plamni o'zgartirish taqiqlanishi
## Topshiriq sharti:
`foreach` aylanayotganda massiv yoki ro'yxat elementlarini o'chirib bo'lmasligi va `InvalidOperationException` sababini ko'rsating.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        var sonlar = new List<int> { 1, 2, 3, 4, 5 };

        try
        {
            foreach (var son in sonlar)
            {
                if (son == 3)
                {
                    sonlar.Add(99); // Iteratsiya paytida to'plamni o'zgartirish!
                }
            }
        }
        catch (InvalidOperationException ex)
        {
            Console.WriteLine($"Kutilgan xatolik: {ex.GetType().Name}");
            Console.WriteLine("Izoh: IEnumerator to'plam versiyasi o'zgarganini aniqladi va xavfsizlik uchun to'xtatdi.");
        }
    }
}

```

## Tushuntirish va Mantiq:
`IEnumerator` har safar `MoveNext()` chaqirilganda to'plamning ichki `version` o'zgaruvchisini solishtiradi. Agar to'plamga yangi element qo'shilsa yoki o'chirilsa, versiya ortadi va darhol `InvalidOperationException` chiqariladi.

## Ishlash natijasi:
```text
Kutilgan xatolik: InvalidOperationException
Izoh: IEnumerator to'plam versiyasi o'zgarganini aniqladi va xavfsizlik uchun to'xtatdi.
```

# 135-Topshiriq: Cheksiz sikl va uning xavfsiz to'xtatilishi
## Topshiriq sharti:
`while(true)` cheksiz siklini ma'lum shart bajarilganda `break` orqali to'xtatuvchi xavfsiz mexanizm yozing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int hisoblagich = 0;

        while (true)
        {
            hisoblagich++;
            if (hisoblagich >= 3)
            {
                Console.WriteLine($"Chegara {hisoblagich} ga yetdi, chiqildi.");
                break;
            }
        }
    }
}

```

## Tushuntirish va Mantiq:
Cheksiz sikllar mikroservislarda, xabarlar navbatini tinglashda (listener) va o'yin dvigatellarining asosiy siklida (game loop) keng qo'llaniladi. Muhimi, ichida har doim chiqish kafolati yoki to'xtatuvchi bayroq bo'lishi shart.

## Ishlash natijasi:
```text
Chegara 3 ga yetdi, chiqildi.
```

# 136-Topshiriq: Ko'p qavatli sikllarda etiketka (label) va goto
## Topshiriq sharti:
Uch qavatli chuqur sikldan bittada to'liq tashqariga chiqish uchun `goto` yorlig'idan foydalaning.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        for (int i = 0; i < 5; i++)
        {
            for (int j = 0; j < 5; j++)
            {
                if (i == 2 && j == 3)
                {
                    Console.WriteLine($"Maqsad topildi: i={i}, j={j}. Barcha sikllar tashqarisiga sakrash.");
                    goto Tashqariga;
                }
            }
        }

    Tashqariga:
        Console.WriteLine("Sikllardan to'liq chiqildi.");
    }
}

```

## Tushuntirish va Mantiq:
C# da oddiy `break` faqat eng ichki bitta sikldan chiqaradi. Ko'p qavatli sikllardan bitta amalda sakrab chiqish uchun `goto Etiketka;` eng toza va samarali usullardan biridir.

## Ishlash natijasi:
```text
Maqsad topildi: i=2, j=3. Barcha sikllar tashqarisiga sakrash.
Sikllardan to'liq chiqildi.
```

# 137-Topshiriq: Matritsani transponirlash (Matrix Transpose)
## Topshiriq sharti:
N x M o'lchamli to'rtburchakli matritsaning satr va ustunlarini almashtirib M x N matritsa hosil qiling.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[,] original = {
            { 1, 2, 3 },
            { 4, 5, 6 }
        }; // 2x3

        int[,] transponirlangan = new int[3, 2];

        for (int i = 0; i < 2; i++)
        {
            for (int j = 0; j < 3; j++)
            {
                transponirlangan[j, i] = original[i, j];
            }
        }

        Console.WriteLine("Transponirlangan matritsa (3x2):");
        for (int i = 0; i < 3; i++)
        {
            for (int j = 0; j < 2; j++)
            {
                Console.Write($"{transponirlangan[i, j]} ");
            }
            Console.WriteLine();
        }
    }
}

```

## Tushuntirish va Mantiq:
Matritsani transponirlashda satr va ustun indekslari o'zaro o'rin almashadi: `A[i, j] -> T[j, i]`. Bu kompyuter grafikasi va chiziqli algebrada fundamental amaldir.

## Ishlash natijasi:
```text
Transponirlangan matritsa (3x2):
1 4 
2 5 
3 6
```

# 138-Topshiriq: Matritsalarni ko'paytirish algoritmi (Matrix Multiplication)
## Topshiriq sharti:
Ikki matritsani algebraik qoidalar asosida ko'paytiruvchi $O(N^3)$ algoritmini yozing.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[,] A = { { 1, 2 }, { 3, 4 } };
        int[,] B = { { 5, 6 }, { 7, 8 } };
        int[,] C = new int[2, 2];

        for (int i = 0; i < 2; i++)
        {
            for (int j = 0; j < 2; j++)
            {
                for (int k = 0; k < 2; k++)
                {
                    C[i, j] += A[i, k] * B[k, j];
                }
            }
        }

        Console.WriteLine($"C[0,0] = {C[0, 0]}, C[0,1] = {C[0, 1]}");
        Console.WriteLine($"C[1,0] = {C[1, 0]}, C[1,1] = {C[1, 1]}");
    }
}

```

## Tushuntirish va Mantiq:
Matritsalarni ko'paytirishda A ning satri B ning ustuniga skalyar ko'paytiriladi. 2x2 holatda: C[0,0] = 1*5 + 2*7 = 19; C[0,1] = 1*6 + 2*8 = 22.

## Ishlash natijasi:
```text
C[0,0] = 19, C[0,1] = 22
C[1,0] = 43, C[1,1] = 50
```

# 139-Topshiriq: Pufakchali saralash (Bubble Sort) algoritmi
## Topshiriq sharti:
Qo'shni elementlarni taqqoslab o'rin almashtirish orqali massivni saralang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[] sonlar = [ 64, 34, 25, 12, 22, 11, 90 ];
        int n = sonlar.Length;

        for (int i = 0; i < n - 1; i++)
        {
            for (int j = 0; j < n - i - 1; j++)
            {
                if (sonlar[j] > sonlar[j + 1])
                {
                    // Almashtirish (Tuple swap)
                    (sonlar[j], sonlar[j + 1]) = (sonlar[j + 1], sonlar[j]);
                }
            }
        }

        Console.WriteLine("Bubble Sort natijasi: " + string.Join(", ", sonlar));
    }
}

```

## Tushuntirish va Mantiq:
Bubble Sort sodda saralash algoritmi bo'lib, har bir o'tishda eng katta element suv yuziga chiqqan pufak kabi massiv oxiriga surilib boradi. C# da `(a, b) = (b, a)` kortej sintaksisi orqali vaqtinchalik o'zgaruvchisiz almashtirish mumkin.

## Ishlash natijasi:
```text
Bubble Sort natijasi: 11, 12, 22, 25, 34, 64, 90
```

# 140-Topshiriq: Tanlash orqali saralash (Selection Sort) algoritmi
## Topshiriq sharti:
Har bir qadamda qolgan qismning minimal elementini topib boshiga qo'yuvchi Selection Sort ni amalga oshiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[] massiv = [ 29, 10, 14, 37, 13 ];
        int n = massiv.Length;

        for (int i = 0; i < n - 1; i++)
        {
            int minIndeks = i;
            for (int j = i + 1; j < n; j++)
            {
                if (massiv[j] < massiv[minIndeks])
                {
                    minIndeks = j;
                }
            }

            if (minIndeks != i)
            {
                (massiv[i], massiv[minIndeks]) = (massiv[minIndeks], massiv[i]);
            }
        }

        Console.WriteLine("Selection Sort natijasi: " + string.Join(", ", massiv));
    }
}

```

## Tushuntirish va Mantiq:
Selection Sort algoritmi har doim $O(N^2)$ taqqoslash bajaradi, ammo Bubble Sort ga nisbatan ancha kam (maksimal $N$ marta) xotirada almashtirish (swap) amalga oshiradi.

## Ishlash natijasi:
```text
Selection Sort natijasi: 10, 13, 14, 29, 37
```

# 141-Topshiriq: Massivdagi takrorlangan elementlarni joyida o'chirish (In-Place Deduplication)
## Topshiriq sharti:
Saralangan massivdagi dublikatlarni qo'shimcha massiv ochmasdan $O(1)$ xotira bilan tozalang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[] tartibli = [ 1, 1, 2, 2, 3, 4, 4, 5 ];

        int unikalIndex = 0;
        for (int i = 1; i < tartibli.Length; i++)
        {
            if (tartibli[i] != tartibli[unikalIndex])
            {
                unikalIndex++;
                tartibli[unikalIndex] = tartibli[i];
            }
        }

        int unikalSoni = unikalIndex + 1;
        Console.WriteLine($"Unikal elementlar soni: {unikalSoni}");
        Console.Write("Unikal qism: ");
        for (int i = 0; i < unikalSoni; i++)
        {
            Console.Write($"{tartibli[i]} ");
        }
        Console.WriteLine();
    }
}

```

## Tushuntirish va Mantiq:
Ikki ko'rsatkichli (Two Pointers) texnikasi yordamida massivning o'zida harakatlanib, yangi Heap massivi yaratmasdan takrorlarni oldingi o'rinlarga siqib chiqarish mumkin.

## Ishlash natijasi:
```text
Unikal elementlar soni: 5
Unikal qism: 1 2 3 4 5
```

# 142-Topshiriq: Span.IndexOf va SequenceEqual bilan ultra tezkor taqqoslash
## Topshiriq sharti:
`Span` ning yuqori optimallashtirilgan `SequenceEqual` va `IndexOf` metodlarini qo'llang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        ReadOnlySpan<byte> a1 = [ 10, 20, 30, 40 ];
        ReadOnlySpan<byte> a2 = [ 10, 20, 30, 40 ];
        ReadOnlySpan<byte> a3 = [ 10, 20, 99, 40 ];

        Console.WriteLine($"a1 == a2 (SequenceEqual): {a1.SequenceEqual(a2)}");
        Console.WriteLine($"a1 == a3 (SequenceEqual): {a1.SequenceEqual(a3)}");

        int pos = a3.IndexOf((byte)99);
        Console.WriteLine($"99 soni a3 ning {pos}-indeksida topildi.");
    }
}

```

## Tushuntirish va Mantiq:
`Span<T>.SequenceEqual` protsessorning SIMD (vektor) instruksiyalaridan foydalanib, baytlarni 128/256-bitli registrlarda bir paytning o'zida parallel tekshiradi. Bu oddiy siklga nisbatan 5-10 barobar tezroqdir.

## Ishlash natijasi:
```text
a1 == a2 (SequenceEqual): True
a1 == a3 (SequenceEqual): False
99 soni a3 ning 2-indeksida topildi.
```

# 143-Topshiriq: 2D Matritsada asosiy va yordamchi diagonallar yig'indisi
## Topshiriq sharti:
Kvadrat matritsaning asosiy diagonali va yordamchi diagonali yig'indisini hisoblang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[,] m = {
            { 1, 2, 3 },
            { 4, 5, 6 },
            { 7, 8, 9 }
        };
        int n = 3;

        int asosiyYigindi = 0;
        int yordamchiYigindi = 0;

        for (int i = 0; i < n; i++)
        {
            asosiyYigindi += m[i, i];
            yordamchiYigindi += m[i, n - 1 - i];
        }

        Console.WriteLine($"Asosiy diagonal (1+5+9): {asosiyYigindi}");
        Console.WriteLine($"Yordamchi diagonal (3+5+7): {yordamchiYigindi}");
    }
}

```

## Tushuntirish va Mantiq:
Asosiy diagonal elementlarida satr va ustun indeksi teng (`i == j`). Yordamchi diagonalda esa indekslar yig'indisi `n - 1` ga teng bo'ladi (`m[i, n - 1 - i]`). Bitta sikl ichida har ikkala yig'indini $O(N)$ da topish mumkin.

## Ishlash natijasi:
```text
Asosiy diagonal (1+5+9): 15
Yordamchi diagonal (3+5+7): 15
```

# 144-Topshiriq: Massivda aylanma siljitish (Cyclic Shift)
## Topshiriq sharti:
Massiv elementlarini o'ng tomonga 1 pozitsiyaga aylanma siljiting (oxirgi element birinchi o'ringa o'tadi).

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[] massiv = [ 1, 2, 3, 4, 5 ];
        int oxirgi = massiv[^1];

        for (int i = massiv.Length - 1; i > 0; i--)
        {
            massiv[i] = massiv[i - 1];
        }
        massiv[0] = oxirgi;

        Console.WriteLine("O'ngga 1 qadam siljitildi: " + string.Join(", ", massiv));
    }
}

```

## Tushuntirish va Mantiq:
Aylanma siljitish buferlash algoritmlarida, kriptografik shifrlashda (masalan Caesar cipher) va tarmoq drayverlarida keng qo'llaniladi.

## Ishlash natijasi:
```text
O'ngga 1 qadam siljitildi: 5, 1, 2, 3, 4
```

# 145-Topshiriq: MemoryMarshal: Past darajadagi xotira kastingi
## Topshiriq sharti:
`System.Runtime.InteropServices.MemoryMarshal` yordamida `Span<int>` ni xotiradagi baytlar (`Span<byte>`) sifatida ko'ring.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.InteropServices;

internal class Program
{
    static void Main()
    {
        int[] sonlar = [ 1 ]; // 1 ta 32-bitli int (4 bayt)
        Span<int> intSpan = sonlar.AsSpan();

        // int oynasini baytlar oynasiga qayta xaritalash
        Span<byte> baytSpan = MemoryMarshal.AsBytes(intSpan);

        Console.WriteLine($"int Span uzunligi: {intSpan.Length}");
        Console.WriteLine($"Bayt Span uzunligi: {baytSpan.Length} bayt");
        Console.WriteLine($"Little-Endian 1-bayt: {baytSpan[0]}");
    }
}

```

## Tushuntirish va Mantiq:
`MemoryMarshal.AsBytes` hech qanday xotira ko'chirmasdan, xuddi C dagi pointer casting kabi bir xotira hududiga boshqa turdagi `Span` orqali qarash imkonini beradi. Zamonaviy x86/ARM arxitekturasida sonlar Little-Endian formatda saqlanadi.

## Ishlash natijasi:
```text
int Span uzunligi: 1
Bayt Span uzunligi: 4 bayt
Little-Endian 1-bayt: 1
```

# 146-Topshiriq: SIMD va Vektorlashtirish asoslari (System.Numerics.Vector<T>)
## Topshiriq sharti:
Hardware-accelerated `Vector<int>` yordamida protsessor registrlarida bir vaqtning o'zida bir nechta sonlarni qo'shish tamoyilini tushuntiring.

## Yechim (C# kodi):
```csharp
using System;
using System.Numerics;

internal class Program
{
    static void Main()
    {
        Console.WriteLine($"SIMD apparat tezlanishi mavjudmi: {Vector.IsHardwareAccelerated}");
        Console.WriteLine($"Bitta registrga sig'adigan int elementlar soni: {Vector<int>.Count}");

        if (Vector.IsHardwareAccelerated)
        {
            var v1 = new Vector<int>(10); // Barcha elementlari 10
            var v2 = new Vector<int>(20); // Barcha elementlari 20
            var v3 = v1 + v2;             // Barcha elementlar bitta CPU siklida parallel qo'shiladi

            Console.WriteLine($"Vektor yig'indisining birinchi elementi: {v3[0]}");
        }
    }
}

```

## Tushuntirish va Mantiq:
SIMD (Single Instruction, Multiple Data) yordamida zamonaviy protsessorlar bitta CPU instruksiyasida 4, 8 yoki 16 ta sonni parallel qo'shishi mumkin. .NET ning `Vector<T>` sinfi AVX2, AVX-512 yoki ARM NEON instruksiyalarini avtomatik ishlatadi.

## Ishlash natijasi:
```text
SIMD apparat tezlanishi mavjudmi: True
Bitta registrga sig'adigan int elementlar soni: 8
Vektor yig'indisining birinchi elementi: 30
```

# 147-Topshiriq: Massivda eng katta va eng kichik elementlarni bitta siklda topish
## Topshiriq sharti:
Massivni faqat bitta marta aylanib chiqish ($O(N)$) orqali minimum va maksimum qiymatlarni aniqlang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[] sonlar = [ 42, 17, 88, 3, 99, 56, 1 ];

        int min = sonlar[0];
        int max = sonlar[0];

        for (int i = 1; i < sonlar.Length; i++)
        {
            if (sonlar[i] < min) min = sonlar[i];
            if (sonlar[i] > max) max = sonlar[i];
        }

        Console.WriteLine($"Minimal qiymat: {min}");
        Console.WriteLine($"Maksimal qiymat: {max}");
    }
}

```

## Tushuntirish va Mantiq:
Ikki alohida `sonlar.Min()` va `sonlar.Max()` LINQ chaqiruvlari massivni ikki marta aylanib chiqadi. Bitta siklda ikkalasini topish xotira keshini tejaydi va tezlikni 2 barobar oshiradi.

## Ishlash natijasi:
```text
Minimal qiymat: 1
Maksimal qiymat: 99
```

# 148-Topshiriq: Massiv o'rtacha qiymatini va dispersiyasini hisoblash
## Topshiriq sharti:
Sonlar massivining o'rta arifmetik qiymatini va dispersiyasini hisoblang.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        double[] ballar = [ 80.0, 85.0, 90.0, 95.0, 100.0 ];

        double yigindi = 0;
        foreach (var b in ballar) yigindi += b;
        double orta = yigindi / ballar.Length;

        double kvadratFarqYigindi = 0;
        foreach (var b in ballar)
        {
            kvadratFarqYigindi += Math.Pow(b - orta, 2);
        }
        double dispersiya = kvadratFarqYigindi / ballar.Length;

        Console.WriteLine($"O'rtacha qiymat: {orta}");
        Console.WriteLine($"Dispersiya: {dispersiya}");
    }
}

```

## Tushuntirish va Mantiq:
Statistik hisob-kitoblarda massivlar ustida ko'p o'tishli amallar bajariladi. Ushbu mantiq ma'lumotlar tahlili va mashinaviy o'rganish (Machine Learning) formulalarining asosidir.

## Ishlash natijasi:
```text
O'rtacha qiymat: 90
Dispersiya: 50
```

# 149-Topshiriq: Massiv elementlarini tasodifiy aralashtirish (Fisher-Yates Shuffle)
## Topshiriq sharti:
Tasodifiy sonlar generatori yordamida massiv elementlarini teng ehtimollik bilan aralashtiring.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        int[] sonlar = [ 1, 2, 3, 4, 5, 6 ];
        var rng = new Random(42); // Qat'iy seed bilan

        for (int i = sonlar.Length - 1; i > 0; i--)
        {
            int j = rng.Next(i + 1);
            (sonlar[i], sonlar[j]) = (sonlar[j], sonlar[i]);
        }

        Console.WriteLine("Aralashtirilgan massiv: " + string.Join(", ", sonlar));
    }
}

```

## Tushuntirish va Mantiq:
Fisher-Yates (yoki Knuth Shuffle) algoritmi $O(N)$ vaqtda har bir mumkin bo'lgan permutatsiya teng ehtimollikda chiqishini matematik jihatdan kafolatlaydi.

## Ishlash natijasi:
```text
Aralashtirilgan massiv: 5, 4, 3, 2, 1, 6
```

# 150-Topshiriq: Zero-Allocation xotira strategiyalari yakuniy xulosasi
## Topshiriq sharti:
`Span`, `ReadOnlySpan`, `stackalloc` va `ArrayPool` vositalarini bitta yuqori unumdorlikdagi ma'lumotlarni qayta ishlash konveyerida jamlang.

## Yechim (C# kodi):
```csharp
using System;
using System.Buffers;

internal class Program
{
    static void Main()
    {
        // 1. Kichik ma'lumotlar uchun Stack xotira
        Span<int> kichikBufer = stackalloc int[3] { 10, 20, 30 };

        // 2. Katta ma'lumotlar uchun qayta ishlatiluvchi ArrayPool
        int[] kattaHovuz = ArrayPool<int>.Shared.Rent(500);
        try
        {
            Span<int> faolQism = kattaHovuz.AsSpan(0, 3);
            kichikBufer.CopyTo(faolQism);

            Console.WriteLine($"Hovuzga ko'chirilgan faol qism: {faolQism[0]}, {faolQism[1]}, {faolQism[2]}");
            Console.WriteLine("Xulosa: Zamonaviy .NET da 0 bayt GC yuk bilan maksimal unumdorlikka erishildi!");
        }
        finally
        {
            ArrayPool<int>.Shared.Return(kattaHovuz);
        }
    }
}

```

## Tushuntirish va Mantiq:
Ushbu yondashuv zamonaviy .NET dasturlashining eng muhim xotira qoidasini namoyish etadi: kichik hajmlar uchun `stackalloc Span<T>`, katta va dinamik hajmlar uchun `ArrayPool<T>`. Natijada dastur sekundiga millionlab so'rovlarni birorta ham GC to'xtashlarisiz amalga oshira oladi.

## Ishlash natijasi:
```text
Hovuzga ko'chirilgan faol qism: 10, 20, 30
Xulosa: Zamonaviy .NET da 0 bayt GC yuk bilan maksimal unumdorlikka erishildi!
```

