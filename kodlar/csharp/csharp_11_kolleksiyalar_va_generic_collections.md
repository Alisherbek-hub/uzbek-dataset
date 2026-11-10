# 11-Mavzu: Kolleksiyalar va Generic Collections (501-550)

Ushbu bo'limda C# va .NET ekotizimidagi to'plamlar: `List<T>`, `Dictionary<TKey, TValue>`, `HashSet<T>`, `Queue<T>`, `Stack<T>`, `LinkedList<T>`, `SortedList` va `SortedDictionary`, xotira boshqaruvi (`Capacity`, `TrimExcess`), Immutability (`ImmutableArray`, `ImmutableList`), .NET 8 `FrozenDictionary` va `FrozenSet`, ko'p oqimli `Concurrent` to'plamlar, maxsus kolleksiya tuzish hamda `IEnumerable<T>` va `yield return` mexanizmlari bo'yicha 50 ta amaliy topshiriq jamlangan.

# 501-Topshiriq: List<T> Ichki Tuzilmasi: Hajm (Capacity) va Kengayish (Reallocation)
## Topshiriq sharti:
Ro'yxatning dinamik kengayishi va ortiqcha xotira ko'chishini o'rganing.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        List<int> sonlar = new List<int>();

        Console.WriteLine($"Boshlang'ich - Count: {sonlar.Count}, Capacity: {sonlar.Capacity}");

        for (int i = 1; i <= 9; i++)
        {
            sonlar.Add(i);
            Console.WriteLine($"Qo'shildi: {i} -> Count: {sonlar.Count}, Capacity: {sonlar.Capacity}");
        }
    }
}

```

## Tushuntirish va Mantiq:
List<T> ichida oddiy `T[]` massiv saqlaydi. Sig'im (Capacity) to'lganda, ro'yxat avvalgi hajmidan 2 barobar katta yangi massiv yaratadi va eski elementlarni nusxalaydi. Katta ma'lumotlar uchun `new List<T>(kutilgan_hajm)` berish tavsiya etiladi.

## Ishlash natijasi:
```text
Boshlang'ich - Count: 0, Capacity: 0
Qo'shildi: 1 -> Count: 1, Capacity: 4
Qo'shildi: 2 -> Count: 2, Capacity: 4
Qo'shildi: 3 -> Count: 3, Capacity: 4
Qo'shildi: 4 -> Count: 4, Capacity: 4
Qo'shildi: 5 -> Count: 5, Capacity: 8
Qo'shildi: 6 -> Count: 6, Capacity: 8
Qo'shildi: 7 -> Count: 7, Capacity: 8
Qo'shildi: 8 -> Count: 8, Capacity: 8
Qo'shildi: 9 -> Count: 9, Capacity: 16
```

# 502-Topshiriq: List<T> TrimExcess() va EnsureCapacity() orqali xotirani tejash
## Topshiriq sharti:
Katta ro'yxatdan elementlar o'chirilgach, bo'sh xotirani operatsion tizimga qaytarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        List<int> royxat = new List<int>();
        royxat.EnsureCapacity(100);
        Console.WriteLine($"EnsureCapacity dan keyin: {royxat.Capacity}");

        for (int i = 0; i < 10; i++) royxat.Add(i);
        Console.WriteLine($"Elementlar: {royxat.Count}, Capacity: {royxat.Capacity}");

        royxat.TrimExcess();
        Console.WriteLine($"TrimExcess dan keyin Capacity: {royxat.Capacity}");
    }
}

```

## Tushuntirish va Mantiq:
`TrimExcess()` ortiqcha massiv xotirasini kesib tashlab, Capacity ni Count ga tenglashtiradi.

## Ishlash natijasi:
```text
EnsureCapacity dan keyin: 100
Elementlar: 10, Capacity: 100
TrimExcess dan keyin Capacity: 10
```

# 503-Topshiriq: List<T>.BinarySearch bilan logarifmik $O(\log N)$ qidiruv
## Topshiriq sharti:
Tartiblangan ro'yxat ichidan eng tezkor usulda element qidirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        List<int> sonlar = new() { 12, 25, 37, 48, 59, 64, 88, 99 };

        int qidirilayotgan = 59;
        int indeks = sonlar.BinarySearch(qidirilayotgan);

        Console.WriteLine($"{qidirilayotgan} soni indeksi: {indeks}");

        int topilmagan = 50;
        int manfiyIndeks = sonlar.BinarySearch(topilmagan);
        Console.WriteLine($"{topilmagan} topilmadi (bit bo'yicha teskari kiritish indeksi): {manfiyIndeks}");
    }
}

```

## Tushuntirish va Mantiq:
BinarySearch binar qidiruv algoritmi bo'lib, tartiblangan massivda elementni $O(\log N)$ vaqtda topadi. Agar element topilmasa, uning manfiy bitwise complement (`~index`) qiymatini qaytaradi.

## Ishlash natijasi:
```text
59 soni indeksi: 4
50 topilmadi (bit bo'yicha teskari kiritish indeksi): -5
```

# 504-Topshiriq: List<T>.TrueForAll, Find, FindAll va RemoveAll metodlari
## Topshiriq sharti:
Predikatlar yordamida ro'yxat ustida guruh amallarini bajarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        List<int> sonlar = new() { 5, 8, 12, 17, 20, 25, 30 };

        bool barchasiMusbat = sonlar.TrueForAll(x => x > 0);
        int birinchiJuft = sonlar.Find(x => x % 2 == 0);
        List<int> juftlar = sonlar.FindAll(x => x % 2 == 0);

        Console.WriteLine($"Barchasi musbat: {barchasiMusbat}");
        Console.WriteLine($"Birinchi juft: {birinchiJuft}");
        Console.WriteLine($"Juftlar soni: {juftlar.Count}");

        int ochirilganlar = sonlar.RemoveAll(x => x < 15);
        Console.WriteLine($"O'chirilganlar: {ochirilganlar}, qolganlar: {string.Join(", ", sonlar)}");
    }
}

```

## Tushuntirish va Mantiq:
RemoveAll predikatga mos elementlarni massivni siljitib (in-place) bitta $O(N)$ yurishda o'chiradi.

## Ishlash natijasi:
```text
Barchasi musbat: True
Birinchi juft: 8
Juftlar soni: 4
O'chirilganlar: 3, qolganlar: 17, 20, 25, 30
```

# 505-Topshiriq: Dictionary<TKey, TValue> Ichki Tuzilishi va Xesh Kolliziyasi
## Topshiriq sharti:
Dictionary qanday ishlashi: Buckets, Entries massivlari va zanjirli kolliziya (Separate Chaining).

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        Dictionary<string, string> lugat = new Dictionary<string, string>
        {
            ["kitob"] = "book",
            ["qalam"] = "pen",
            ["daftar"] = "notebook"
        };

        if (lugat.TryGetValue("kitob", out string? tarjima))
        {
            Console.WriteLine($"Topildi: kitob -> {tarjima}");
        }

        // ContainsKey - O(1) amali
        Console.WriteLine($"'stol' bormi: {lugat.ContainsKey("stol")}");
    }
}

```

## Tushuntirish va Mantiq:
Dictionary kalitning `GetHashCode()` qiymatini olib, chelak (bucket) indeksini topadi. O'rtacha qidirish, qo'shish va o'chirish tezligi $O(1)$ ni tashkil etadi.

## Ishlash natijasi:
```text
Topildi: kitob -> book
'stol' bormi: False
```

# 506-Topshiriq: Dictionary da Maxsus IEqualityComparer<TKey> ishlatish
## Topshiriq sharti:
Katta-kichik harflarni farqlamaydigan maxsus komparatorli lug'at yarating.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        // StringComparer.OrdinalIgnoreCase orqali registrni hisobga olmaslik
        var foydalanuvchilar = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase)
        {
            ["ali"] = 101,
            ["VALI"] = 102
        };

        Console.WriteLine($"'Ali' qiymati: {foydalanuvchilar["Ali"]}");
        Console.WriteLine($"'vali' bormi: {foydalanuvchilar.ContainsKey("vali")}");
    }
}

```

## Tushuntirish va Mantiq:
IEqualityComparer berilganda Dictionary kalitlarni tenglash va xesh kodini hisoblashda aynan shu taqqoslagichdan foydalanadi.

## Ishlash natijasi:
```text
'Ali' qiymati: 101
'vali' bormi: True
```

# 507-Topshiriq: HashSet<T> va To'plamlar Matematikasi (Set Operations)
## Topshiriq sharti:
Noyob elementlar to'plami va UnionWith, IntersectWith, ExceptWith amallari.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        HashSet<int> a = new() { 1, 2, 3, 4, 5 };
        HashSet<int> b = new() { 4, 5, 6, 7, 8 };

        HashSet<int> kesishma = new(a);
        kesishma.IntersectWith(b);
        Console.WriteLine($"Kesishma (a ∩ b): {string.Join(", ", kesishma)}");

        HashSet<int> birlashma = new(a);
        birlashma.UnionWith(b);
        Console.WriteLine($"Birlashma (a ∪ b): {string.Join(", ", birlashma)}");

        HashSet<int> ayirma = new(a);
        ayirma.ExceptWith(b);
        Console.WriteLine($"Ayirma (a \ b): {string.Join(", ", ayirma)}");
    }
}

```

## Tushuntirish va Mantiq:
HashSet<T> faqat unikal elementlarni $O(1)$ qidirish tezligi bilan saqlaydi va diskret matematika amallarini samarali bajaradi.

## Ishlash natijasi:
```text
Kesishma (a ∩ b): 4, 5
Birlashma (a ∪ b): 1, 2, 3, 4, 5, 6, 7, 8
Ayirma (a \ b): 1, 2, 3
```

# 508-Topshiriq: HashSet<T>.Overlaps va SetEquals metodlari
## Topshiriq sharti:
Ikkita to'plamning o'zaro umumiyligi va to'liq tengligini tekshirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        HashSet<string> mevalar1 = new() { "Olma", "Anor", "Uzum" };
        HashSet<string> mevalar2 = new() { "Uzum", "Banan" };
        HashSet<string> mevalar3 = new() { "Anor", "Olma", "Uzum" };

        Console.WriteLine($"mevalar1 va mevalar2 ustma-ust tushadimi: {mevalar1.Overlaps(mevalar2)}");
        Console.WriteLine($"mevalar1 va mevalar3 to'liq tengmi: {mevalar1.SetEquals(mevalar3)}");
    }
}

```

## Tushuntirish va Mantiq:
SetEquals elementlar tartibi qanday bo'lishidan qat'i nazar ikkala to'plam aynan bir xil a'zolarga egaligini tekshiradi.

## Ishlash natijasi:
```text
mevalar1 va mevalar2 ustma-ust tushadimi: True
mevalar1 va mevalar3 to'liq tengmi: True
```

# 509-Topshiriq: Queue<T> (FIFO) va TryDequeue / TryPeek metodlari
## Topshiriq sharti:
Xatoliksiz ishlovchi zamonaviy navbat amaliyoti.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        Queue<string> xabarlar = new();
        xabarlar.Enqueue("1-buyruq");
        xabarlar.Enqueue("2-buyruq");

        if (xabarlar.TryPeek(out string? korish))
        {
            Console.WriteLine($"Navbat boshida: {korish}");
        }

        while (xabarlar.TryDequeue(out string? xabar))
        {
            Console.WriteLine($"Bajarildi: {xabar}");
        }

        Console.WriteLine($"Qolgan elementlar: {xabarlar.Count}");
    }
}

```

## Tushuntirish va Mantiq:
TryDequeue bo'sh navbatdan element o'qilganda InvalidOperationException otmasdan xavfsiz `false` qaytaradi.

## Ishlash natijasi:
```text
Navbat boshida: 1-buyruq
Bajarildi: 1-buyruq
Bajarildi: 2-buyruq
Qolgan elementlar: 0
```

# 510-Topshiriq: Stack<T> (LIFO) va Qavslar To'g'riligini Tekshirish Masalasi
## Topshiriq sharti:
Stack yordamida qavslar muvozanatini (Bracket Matching) tekshiring.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static bool Tekshir(string ifoda)
    {
        Stack<char> stack = new();
        foreach (char c in ifoda)
        {
            if (c == '(' || c == '{' || c == '[')
                stack.Push(c);
            else if (c == ')' || c == '}' || c == ']')
            {
                if (stack.Count == 0) return false;
                char ochuvchi = stack.Pop();
                if ((c == ')' && ochuvchi != '(') ||
                    (c == '}' && ochuvchi != '{') ||
                    (c == ']' && ochuvchi != '['))
                    return false;
            }
        }
        return stack.Count == 0;
    }

    static void Main()
    {
        Console.WriteLine($"Tekshir '([{}])': {Tekshir("([{}])")}");
        Console.WriteLine($"Tekshir '([)]': {Tekshir("([)]")}");
    }
}

```

## Tushuntirish va Mantiq:
Stack klassik LIFO (Last-In-First-Out) tuzilmasi bo'lib, sintaktik analizatorlar va rekursiyani boshqarishda qo'llaniladi.

## Ishlash natijasi:
```text
Tekshir '([{}])': True
Tekshir '([)]': False
```

# 511-Topshiriq: LinkedList<T> (Ikki Yo'nalishli Bog'langan Ro'yxat)
## Topshiriq sharti:
Elementlarni o'rtasiga va boshiga $O(1)$ da qo'shish va o'chirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        LinkedList<string> stansiyalar = new();
        LinkedListNode<string> markaz = stansiyalar.AddFirst("Amir Temur");
        stansiyalar.AddBefore(markaz, "Paxtakor");
        stansiyalar.AddAfter(markaz, "Hamid Olimjon");

        Console.Write("Metro yo'nalishi: ");
        foreach (var s in stansiyalar)
        {
            Console.Write($"{s} -> ");
        }
        Console.WriteLine("Tamom");
    }
}

```

## Tushuntirish va Mantiq:
LinkedList da ma'lum bir tugun (node) ma'lum bo'lsa, uning yoniga qo'shish massiv kabi elementlarni surishni talab qilmaydi, shuning uchun $O(1)$ bo'ladi.

## Ishlash natijasi:
```text
Metro yo'nalishi: Paxtakor -> Amir Temur -> Hamid Olimjon -> Tamom
```

# 512-Topshiriq: SortedDictionary<TKey, TValue> (Qizil-Qora Daraxt)
## Topshiriq sharti:
Kalitlari doimo avtomatik tartiblangan holda saqlanuvchi lug'at.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        // Red-Black Tree asosida tartiblaydi
        SortedDictionary<int, string> reyting = new()
        {
            [95] = "A'lo",
            [70] = "Yaxshi",
            [100] = "Super",
            [85] = "Yaxshi+"
        };

        foreach (var kvp in reyting)
        {
            Console.WriteLine($"{kvp.Key} ball: {kvp.Value}");
        }
    }
}

```

## Tushuntirish va Mantiq:
SortedDictionary Red-Black Tree daraxti orqali doimiy tartibni saqlaydi. Qo'shish, o'chirish va qidirish har doim $O(\log N)$ vaqt oladi.

## Ishlash natijasi:
```text
70 ball: Yaxshi
85 ball: Yaxshi+
95 ball: A'lo
100 ball: Super
```

# 513-Topshiriq: SortedList<TKey, TValue> va SortedDictionary Farqi
## Topshiriq sharti:
Ikkita massiv asosidagi SortedList va uning xotira hamda qidiruv xususiyatlari.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        // Ikkita saralangan massiv saqlaydi (keys[] va values[])
        SortedList<string, int> narxlar = new()
        {
            ["Non"] = 3000,
            ["Choy"] = 5000,
            ["Sut"] = 8000
        };

        // Indeks bo'yicha to'g'ridan-to'g'ri kirish imkoniyati bor:
        Console.WriteLine($"0-indeksdagi kalit: {narxlar.Keys[0]}, qiymat: {narxlar.Values[0]}");
    }
}

```

## Tushuntirish va Mantiq:
SortedList kamroq xotira yeydi va indeks orqali to'g'ridan-to'g'ri kirish imkonini beradi ($O(1)$), lekin element qo'shish massivni siljitish talab qilgani uchun $O(N)$ bo'lishi mumkin. SortedDictionary esa qo'shishda doim $O(\log N)$.

## Ishlash natijasi:
```text
0-indeksdagi kalit: Choy, qiymat: 5000
```

# 514-Topshiriq: SortedSet<T> va GetViewBetween Metodi
## Topshiriq sharti:
Tartiblangan to'plamdan ma'lum diapazondagi elementlarni ajratib ko'rsatish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        SortedSet<int> yoshlar = new() { 15, 18, 22, 25, 30, 35, 40, 50 };

        // 20 dan 35 gacha bo'lgan oraliqni ajratib olish:
        var yoshGuruh = yoshlar.GetViewBetween(20, 35);

        Console.WriteLine($"20-35 oralig'idagi yoshlar: {string.Join(", ", yoshGuruh)}");
    }
}

```

## Tushuntirish va Mantiq:
GetViewBetween yangi xotira ajratmasdan mavjud daraxt ustida faol ko'rinish (view) hosil qiladi.

## Ishlash natijasi:
```text
20-35 oralig'idagi yoshlar: 22, 25, 30, 35
```

# 515-Topshiriq: ReadOnlyCollection<T> (O'zgartirib Bo'lmaydigan Qoplama)
## Topshiriq sharti:
Mavjud ro'yxatni tashqi dunyoga faqat o'qish uchun havola qilish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;

internal class Program
{
    static void Main()
    {
        List<string> asosiy = new() { "A", "B", "C" };
        ReadOnlyCollection<string> oqishUchun = asosiy.AsReadOnly();

        Console.WriteLine($"Elementlar soni: {oqishUchun.Count}");
        // oqishUchun.Add("D"); // Kompilyatsiya xatosi!

        // Ammo asosiy ro'yxat o'zgarsa, o'qish qoplamasida ham aks etadi:
        asosiy.Add("D");
        Console.WriteLine($"Asosiy ro'yxat o'zgargach: {oqishUchun.Count}");
    }
}

```

## Tushuntirish va Mantiq:
ReadOnlyCollection<T> o'zida ma'lumot nusxasini saqlamaydi, u faqat asl ro'yxatni o'zgartirishdan himoyalovchi yupqa qobiq (wrapper) hisoblanadi.

## Ishlash natijasi:
```text
Elementlar soni: 3
Asosiy ro'yxat o'zgargach: 4
```

# 516-Topshiriq: ReadOnlyDictionary<TKey, TValue> Qoplamasi
## Topshiriq sharti:
Lug'atni o'zgarishlardan himoyalovchi o'qish qobig'ini hosil qilish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;

internal class Program
{
    static void Main()
    {
        var ichkiLugat = new Dictionary<string, string> { ["uz"] = "Uzbekistan" };
        var himoyalangan = new ReadOnlyDictionary<string, string>(ichkiLugat);

        Console.WriteLine($"Mamlakat: {himoyalangan["uz"]}");
        // himoyalangan["en"] = "England"; // Mumkin emas!
    }
}

```

## Tushuntirish va Mantiq:
ReadOnlyDictionary tashqi mijozlarga kalit-qiymat ma'lumotlarini o'zgartirmasdan taqdim etish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Mamlakat: Uzbekistan
```

# 517-Topshiriq: System.Collections.Immutable: ImmutableList<T>
## Topshiriq sharti:
Har qanday qo'shish yoki o'chirish yangi nusxa qaytaruvchi o'zgarmas ro'yxat.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Immutable;

internal class Program
{
    static void Main()
    {
        ImmutableList<int> royxat1 = ImmutableList.Create(1, 2, 3);
        ImmutableList<int> royxat2 = royxat1.Add(4);

        Console.WriteLine($"royxat1: {string.Join(", ", royxat1)}");
        Console.WriteLine($"royxat2: {string.Join(", ", royxat2)}");
    }
}

```

## Tushuntirish va Mantiq:
Immutable to'plamlarda asl obyekt hech qachon o'zgarmaydi (AVL-tree orqali struktura tugunlari ulashiladi - Structural Sharing).

## Ishlash natijasi:
```text
royxat1: 1, 2, 3
royxat2: 1, 2, 3, 4
```

# 518-Topshiriq: ImmutableArray<T> va Uning Yuqori Unumdorligi
## Topshiriq sharti:
Oddiy massiv tezligidagi o'zgarmas tuzilma.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Immutable;

internal class Program
{
    static void Main()
    {
        ImmutableArray<string> shaharlar = ["Toshkent", "Buxoro", "Xiva"];

        Console.WriteLine($"Shaharlar soni: {shaharlar.Length}");
        Console.WriteLine($"1-shahar: {shaharlar[0]}");
    }
}

```

## Tushuntirish va Mantiq:
ImmutableArray<T> struct bo'lib, uning ichida oddiy `T[]` yotadi. Hech qanday daraxt tugunlari yaratmaydi va ketma-ket o'qishda oddiy massiv bilan bir xil tezlik beradi.

## Ishlash natijasi:
```text
Shaharlar soni: 3
1-shahar: Toshkent
```

# 519-Topshiriq: ImmutableDictionary<TKey, TValue> Amaliyoti
## Topshiriq sharti:
Ko'p oqimli muhitda qulflashlarsiz (lock-free) xavfsiz o'zgarmas lug'at.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Immutable;

internal class Program
{
    static void Main()
    {
        var sozlamalar = ImmutableDictionary<string, string>.Empty
            .Add("Mavzu", "Qorong'i")
            .Add("Til", "O'zbek");

        var yangiSozlamalar = sozlamalar.SetItem("Mavzu", "Yorug'");

        Console.WriteLine($"Eski sozlama mavzusi: {sozlamalar["Mavzu"]}");
        Console.WriteLine($"Yangi sozlama mavzusi: {yangiSozlamalar["Mavzu"]}");
    }
}

```

## Tushuntirish va Mantiq:
Immutable to'plamlar funksional dasturlashda va ko'p oqimli xavfsizlikda mukammal yechimdir.

## Ishlash natijasi:
```text
Eski sozlama mavzusi: Qorong'i
Yangi sozlama mavzusi: Yorug'
```

# 520-Topshiriq: .NET 8 FrozenDictionary<TKey, TValue> va Mutlaq Qidiruv Tezligi
## Topshiriq sharti:
Dastur ishga tushgach faqat o'qiladigan ma'lumotlar uchun maxsus optimallashgan muzlatilgan lug'at.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Collections.Frozen;

internal class Program
{
    static void Main()
    {
        var oddiy = new Dictionary<string, int>
        {
            ["GET"] = 1,
            ["POST"] = 2,
            ["PUT"] = 3,
            ["DELETE"] = 4
        };

        // .NET 8 da FrozenDictionary ga o'tkazish
        FrozenDictionary<string, int> muzlatilgan = oddiy.ToFrozenDictionary();

        Console.WriteLine($"POST kodi: {muzlatilgan["POST"]}");
        Console.WriteLine($"Hajmi: {muzlatilgan.Count}");
    }
}

```

## Tushuntirish va Mantiq:
Frozen to'plamlar yaratilish vaqtida barcha kalitlarni analiz qilib, ideal xesh jadvali (Perfect Hash) yoki qisqa matnlar uchun to'g'ridan-to'g'ri string-switch mashina kodini quradi. O'qish tezligi standart Dictionary dan ancha yuqori.

## Ishlash natijasi:
```text
POST kodi: 2
Hajmi: 4
```

# 521-Topshiriq: .NET 8 FrozenSet<T> To'plami
## Topshiriq sharti:
Faqat o'qiladigan to'plamda super-tezkor `Contains` tekshiruvi.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Collections.Frozen;

internal class Program
{
    static void Main()
    {
        string[] ruxsatlar = ["admin", "moderator", "operator"];
        FrozenSet<string> ruxsatToplami = ruxsatlar.ToFrozenSet();

        Console.WriteLine($"'admin' bormi: {ruxsatToplami.Contains("admin")}");
        Console.WriteLine($"'mehmon' bormi: {ruxsatToplami.Contains("mehmon")}");
    }
}

```

## Tushuntirish va Mantiq:
FrozenSet ro'yxat o'zgarmas bo'lgan holda qidirish amallarini eng yuqori darajada tezlashtiradi.

## Ishlash natijasi:
```text
'admin' bormi: True
'mehmon' bormi: False
```

# 522-Topshiriq: ConcurrentDictionary<TKey, TValue> va GetOrAdd Metodi
## Topshiriq sharti:
Ko'p oqimli muhitda poygasiz (thread-safe) ma'lumot qo'shish va olish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Concurrent;

internal class Program
{
    static void Main()
    {
        var kesh = new ConcurrentDictionary<string, int>();

        int q1 = kesh.GetOrAdd("olma", kalit => kalit.Length * 100);
        int q2 = kesh.GetOrAdd("olma", kalit => kalit.Length * 100);

        Console.WriteLine($"Qiymat 1: {q1}");
        Console.WriteLine($"Qiymat 2: {q2}");
        Console.WriteLine($"Lug'at hajmi: {kesh.Count}");
    }
}

```

## Tushuntirish va Mantiq:
ConcurrentDictionary butun lug'atni emas, faqat tegishli chelakni (bucket lock striping) qulflaydi, bu esa yuqori parallellik beradi.

## Ishlash natijasi:
```text
Qiymat 1: 400
Qiymat 2: 400
Lug'at hajmi: 1
```

# 523-Topshiriq: ConcurrentDictionary: AddOrUpdate va TryUpdate Atomarligi
## Topshiriq sharti:
Xavfsiz hisoblagich yoki yangilovchi concurrent amallar.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Concurrent;

internal class Program
{
    static void Main()
    {
        var hisoblar = new ConcurrentDictionary<string, int>();

        // Bor bo'lsa yangilaydi, yo'q bo'lsa qo'shadi:
        hisoblar.AddOrUpdate("tashrif", 1, (kalit, eski) => eski + 1);
        hisoblar.AddOrUpdate("tashrif", 1, (kalit, eski) => eski + 1);

        Console.WriteLine($"Tashriflar soni: {hisoblar["tashrif"]}");
    }
}

```

## Tushuntirish va Mantiq:
AddOrUpdate atomar operatsiya bo'lib, oqimlar o'rtasida poyga holati (race condition) keltirib chiqarmaydi.

## Ishlash natijasi:
```text
Tashriflar soni: 2
```

# 524-Topshiriq: ConcurrentQueue<T> bilan Oqimlararo Xabarlar Navbati
## Topshiriq sharti:
Ko'p oqimlar xavfsiz element qo'shib olishi mumkin bo'lgan lock-free navbat.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Concurrent;

internal class Program
{
    static void Main()
    {
        ConcurrentQueue<string> loglar = new();
        loglar.Enqueue("Tizim boshlandi");
        loglar.Enqueue("Foydalanuvchi kirdi");

        while (loglar.TryDequeue(out string? yozuv))
        {
            Console.WriteLine($"Log: {yozuv}");
        }
    }
}

```

## Tushuntirish va Mantiq:
ConcurrentQueue lock-free arxitektura (Interlocked amallari) asosida ishlaydi va oqimlarni to'xtatib qo'ymaydi.

## Ishlash natijasi:
```text
Log: Tizim boshlandi
Log: Foydalanuvchi kirdi
```

# 525-Topshiriq: ConcurrentStack<T> va PushRange / TryPopRange
## Topshiriq sharti:
Guruhlab elementlarni xavfsiz push va pop qilish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Concurrent;

internal class Program
{
    static void Main()
    {
        ConcurrentStack<int> stack = new();
        stack.PushRange([10, 20, 30]);

        int[] bufer = new int[2];
        int olinganlar = stack.TryPopRange(bufer);

        Console.WriteLine($"Olingan elementlar soni: {olinganlar}");
        Console.WriteLine($"Olinganlar: {string.Join(", ", bufer)}");
    }
}

```

## Tushuntirish va Mantiq:
TryPopRange oqimlararo bir vaqtning o'zida bir nechta elementni o'qib olish imkoniyatini beradi.

## Ishlash natijasi:
```text
Olingan elementlar soni: 2
Olinganlar: 30, 20
```

# 526-Topshiriq: ConcurrentBag<T> va 'Work-Stealing' Algoritmi
## Topshiriq sharti:
Ko'p oqimli muhitda tartibsiz elementlarni eng yuqori unumdorlikda saqlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Concurrent;
using System.Threading.Tasks;

internal class Program
{
    static void Main()
    {
        ConcurrentBag<int> xalta = new();

        Parallel.For(1, 6, i =>
        {
            xalta.Add(i * 10);
        });

        Console.WriteLine($"Xaltadagi elementlar soni: {xalta.Count}");
        foreach (var item in xalta)
        {
            Console.WriteLine($"Element: {item}");
        }
    }
}

```

## Tushuntirish va Mantiq:
ConcurrentBag har bir oqim uchun alohida thread-local navbat yaratadi, faqat boshqa oqimlar bo'sh qolgandagina bir-biridan element 'o'g'irlaydi' (work-stealing).

## Ishlash natijasi:
```text
Xaltadagi elementlar soni: 5
Element: 10
Element: 20
Element: 30
Element: 40
Element: 50
```

# 527-Topshiriq: BlockingCollection<T> bilan Cheklangan Hajmli Navbat (Bounded Capacity)
## Topshiriq sharti:
Producer-Consumer naqshida ishlab chiqaruvchi va iste'molchini muvozanatlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Concurrent;

internal class Program
{
    static void Main()
    {
        // Maksimal 2 ta element sig'diruvchi to'siqli to'plam
        using BlockingCollection<int> ombor = new(boundedCapacity: 2);

        ombor.Add(10);
        ombor.Add(20);
        Console.WriteLine("Ombor to'ldi (2 ta element)");

        // ombor.Add(30); // Bu chaqiruv ombordan element olinmaguncha oqimni to'xtatib turadi (block)

        int olingan = ombor.Take();
        Console.WriteLine($"Ombordan olindi: {olingan}");

        ombor.Add(30);
        Console.WriteLine("30 muvaffaqiyatli qo'shildi!");
    }
}

```

## Tushuntirish va Mantiq:
BlockingCollection boundedCapacity to'lganda Add chaqiruvini, bo'sh bo'lganda esa Take chaqiruvini avtomatik bloklab sinxronizatsiya qiladi.

## Ishlash natijasi:
```text
Ombor to'ldi (2 ta element)
Ombordan olindi: 10
30 muvaffaqiyatli qo'shildi!
```

# 528-Topshiriq: BlockingCollection.CompleteAdding va GetConsumingEnumerable
## Topshiriq sharti:
Ish tugaganligini e'lon qilish va barcha qolgan elementlarni xavfsiz o'qib tugatish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Concurrent;

internal class Program
{
    static void Main()
    {
        using BlockingCollection<string> navbat = new();
        navbat.Add("Xabar 1");
        navbat.Add("Xabar 2");

        navbat.CompleteAdding(); // Boshqa yangi ma'lumot qabul qilinmaydi

        // GetConsumingEnumerable navbat bo'shaguncha va CompleteAdding chaqirilguncha elementlarni sug'urib beradi
        foreach (var xabar in navbat.GetConsumingEnumerable())
        {
            Console.WriteLine($"Qayta ishlandi: {xabar}");
        }

        Console.WriteLine($"Navbat qoldig'i: {navbat.Count}");
    }
}

```

## Tushuntirish va Mantiq:
CompleteAdding navbat yopilganini bildiradi va iste'molchi foreach tsiklidan avtomatik ravishda xavfsiz chiqib ketishini ta'minlaydi.

## Ishlash natijasi:
```text
Qayta ishlandi: Xabar 1
Qayta ishlandi: Xabar 2
Navbat qoldig'i: 0
```

# 529-Topshiriq: System.Threading.Channels (Kanal Asosidagi Xabarlar Navbati)
## Topshiriq sharti:
Yuqori unumdor asinxron xabarlar almashinuvi (`Channel<T>`).

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Channels;
using System.Threading.Tasks;

internal class Program
{
    static async Task Main()
    {
        var kanal = Channel.CreateBounded<int>(new BoundedChannelOptions(5)
        {
            FullMode = BoundedChannelFullMode.Wait
        });

        // Ishlab chiqaruvchi
        _ = Task.Run(async () =>
        {
            for (int i = 1; i <= 3; i++)
            {
                await kanal.Writer.WriteAsync(i);
            }
            kanal.Writer.Complete();
        });

        // Iste'molchi
        await foreach (int son in kanal.Reader.ReadAllAsync())
        {
            Console.WriteLine($"Kanal orqali qabul qilindi: {son}");
        }
    }
}

```

## Tushuntirish va Mantiq:
Channel<T> zamonaviy asinxron navbat bo'lib, xotirani bloklamasdan ValueTask orqali maksimal o'tkazuvchanlikni ta'minlaydi.

## Ishlash natijasi:
```text
Kanal orqali qabul qilindi: 1
Kanal orqali qabul qilindi: 2
Kanal orqali qabul qilindi: 3
```

# 530-Topshiriq: BitArray bilan Bitlar Massivini Boshqarish
## Topshiriq sharti:
Har bir baytda 8 ta boolean qiymatni tejab saqlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections;

internal class Program
{
    static void Main()
    {
        // 8 ta bit (1 bayt)
        BitArray bitlar = new BitArray(8);
        bitlar.Set(0, true);
        bitlar.Set(3, true);

        Console.Write("Bitlar ketma-ketligi: ");
        for (int i = 0; i < bitlar.Length; i++)
        {
            Console.Write(bitlar[i] ? "1" : "0");
        }
        Console.WriteLine();

        bitlar.Not(); // Barcha bitlarni teskarisiga aylantirish
        Console.Write("Inversiya natijasi: ");
        for (int i = 0; i < bitlar.Length; i++)
        {
            Console.Write(bitlar[i] ? "1" : "0");
        }
        Console.WriteLine();
    }
}

```

## Tushuntirish va Mantiq:
BitArray bool massivga nisbatan xotirani 8 barobarga tejaydi, chunki oddiy `bool` C# da 1 bayt (8 bit) joy oladi.

## Ishlash natijasi:
```text
Bitlar ketma-ketligi: 10010000
Inversiya natijasi: 01101111
```

# 531-Topshiriq: BitVector32 bilan Yengil Strukturaviy Flaglar
## Topshiriq sharti:
Stack xotirada 32-bit ichida ko'p sonli flag va qismlarni boshqarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Specialized;

internal class Program
{
    static void Main()
    {
        BitVector32 vektor = new BitVector32(0);

        int mask1 = BitVector32.CreateMask();
        int mask2 = BitVector32.CreateMask(mask1);

        vektor[mask1] = true;  // 1-bit yoqildi
        vektor[mask2] = false; // 2-bit o'chiq

        Console.WriteLine($"1-flag holati: {vektor[mask1]}");
        Console.WriteLine($"2-flag holati: {vektor[mask2]}");
        Console.WriteLine($"Butun son qiymati: {vektor.Data}");
    }
}

```

## Tushuntirish va Mantiq:
BitVector32 qiymat turi (struct) bo'lib, heap xotirada hech qanday obyekt yaratmaydi va operatsion tizim deskriptorlarida keng qo'llaniladi.

## Ishlash natijasi:
```text
1-flag holati: True
2-flag holati: False
Butun son qiymati: 1
```

# 532-Topshiriq: Custom Enumerator: IEnumerator<T> ni qo'lda yaratish
## Topshiriq sharti:
Sinfni `foreach` siklida aylanuvchi qilish mexanizmini ichki darajada tushunish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections;
using System.Collections.Generic;

class Sanagich : IEnumerable<int>
{
    private readonly int max;
    public Sanagich(int max) => this.max = max;

    public IEnumerator<int> GetEnumerator() => new SanagichEnumerator(max);
    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

    private class SanagichEnumerator : IEnumerator<int>
    {
        private readonly int max;
        private int joriy = 0;

        public SanagichEnumerator(int max) => this.max = max;

        public int Current => joriy;
        object IEnumerator.Current => Current;

        public bool MoveNext()
        {
            if (joriy < max)
            {
                joriy++;
                return true;
            }
            return false;
        }

        public void Reset() => joriy = 0;
        public void Dispose() { }
    }
}

internal class Program
{
    static void Main()
    {
        var sanash = new Sanagich(3);
        foreach (int son in sanash)
        {
            Console.WriteLine($"Son: {son}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`foreach` sintaktik shakari aslida `GetEnumerator()`, `MoveNext()` va `Current` chaqiriqlariga aylanadi.

## Ishlash natijasi:
```text
Son: 1
Son: 2
Son: 3
```

# 533-Topshiriq: yield return Mexanizmi va Kompilyator Holat Mashinasi (State Machine)
## Topshiriq sharti:
`yield return` qanday qilib kodni lazy (dangasa) generatsiyaga aylantiradi.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static IEnumerable<int> KetmaKetlik()
    {
        Console.WriteLine("-> 1-bosqich boshlandi");
        yield return 10;

        Console.WriteLine("-> 2-bosqich boshlandi");
        yield return 20;

        Console.WriteLine("-> 3-bosqich boshlandi");
        yield return 30;
    }

    static void Main()
    {
        Console.WriteLine("Metod chaqirildi, lekin kod hali ishga tushmadi!");
        var oqim = KetmaKetlik();

        Console.WriteLine("Iteratsiya boshlanmoqda:");
        foreach (var son in oqim)
        {
            Console.WriteLine($"Olingan: {son}");
        }
    }
}

```

## Tushuntirish va Mantiq:
Kompilyator `yield return` uchraganda yashirin sinf (State Machine) generatsiya qiladi. Metod faqat navbatdagi element so'ralganda (MoveNext) keyingi `yield` gacha ishlaydi.

## Ishlash natijasi:
```text
Metod chaqirildi, lekin kod hali ishga tushmadi!
Iteratsiya boshlanmoqda:
-> 1-bosqich boshlandi
Olingan: 10
-> 2-bosqich boshlandi
Olingan: 20
-> 3-bosqich boshlandi
Olingan: 30
```

# 534-Topshiriq: yield break bilan Iteratsiyani Muddatidan Oldin Yakunlash
## Topshiriq sharti:
Shart bajarilganda ketma-ketlikni darhol to'xtatish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static IEnumerable<int> Musbatlar(int[] sonlar)
    {
        foreach (var s in sonlar)
        {
            if (s < 0) yield break; // Manfiy son ko'rinsa, ro'yxat to'xtatiladi
            yield return s;
        }
    }

    static void Main()
    {
        int[] data = [1, 5, 8, -3, 10, 15];
        foreach (var item in Musbatlar(data))
        {
            Console.WriteLine($"Element: {item}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`yield break` enumeratorning `MoveNext()` metodidan `false` qaytarishga teng bo'lib, siklni tugatadi.

## Ishlash natijasi:
```text
Element: 1
Element: 5
Element: 8
```

# 535-Topshiriq: Cheksiz Ketma-Ketliklar (Infinite Sequence) va Fibonachchi Sonlari
## Topshiriq sharti:
`yield return` yordamida cheksiz oqim generatsiya qilish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static IEnumerable<long> Fibonachchi()
    {
        long a = 0, b = 1;
        while (true)
        {
            yield return a;
            long temp = a + b;
            a = b;
            b = temp;
        }
    }

    static void Main()
    {
        int hisob = 0;
        foreach (long fib in Fibonachchi())
        {
            Console.Write($"{fib} ");
            if (++hisob == 7) break; // Cheksiz sikldan kerakli miqdorni olib chiqish
        }
        Console.WriteLine();
    }
}

```

## Tushuntirish va Mantiq:
Dangasa hisoblash (Lazy evaluation) orqali cheksiz ma'lumotlar oqimini xotirani to'ldirmasdan boshqarish mumkin.

## Ishlash natijasi:
```text
0 1 1 2 3 5 8
```

# 536-Topshiriq: ICollection<T> Interfeysini Amalga Oshirish
## Topshiriq sharti:
Maxsus to'plam sinfida `Add`, `Remove`, `Contains` va `CopyTo` mantiqini yozing.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections;
using System.Collections.Generic;

class MaxsusTo'plam<T> : ICollection<T>
{
    private readonly List<T> ichki = new();

    public int Count => ichki.Count;
    public bool IsReadOnly => false;

    public void Add(T item) => ichki.Add(item);
    public void Clear() => ichki.Clear();
    public bool Contains(T item) => ichki.Contains(item);
    public void CopyTo(T[] array, int arrayIndex) => ichki.CopyTo(array, arrayIndex);
    public bool Remove(T item) => ichki.Remove(item);

    public IEnumerator<T> GetEnumerator() => ichki.GetEnumerator();
    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}

internal class Program
{
    static void Main()
    {
        ICollection<string> to'plam = new MaxsusTo'plam<string>();
        to'plam.Add("Olma");
        to'plam.Add("Nok");

        Console.WriteLine($"Soni: {to'plam.Count}, 'Olma' bormi: {to'plam.Contains("Olma")}");
    }
}

```

## Tushuntirish va Mantiq:
ICollection<T> IEnumerable<T> dan meros olib, kolleksiya o'lchami va uni modifikatsiya qilish kontraktini belgilaydi.

## Ishlash natijasi:
```text
Soni: 2, 'Olma' bormi: True
```

# 537-Topshiriq: IList<T> Interfeysi va Indeksator Bilan Ishlash
## Topshiriq sharti:
Indeks orqali murojaat qilinadigan maxsus ro'yxat tuzilishi.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections;
using System.Collections.Generic;

class MaxsusRoyxat<T> : IList<T>
{
    private readonly List<T> data = new();

    public T this[int index]
    {
        get => data[index];
        set => data[index] = value;
    }

    public int Count => data.Count;
    public bool IsReadOnly => false;

    public void Add(T item) => data.Add(item);
    public void Clear() => data.Clear();
    public bool Contains(T item) => data.Contains(item);
    public void CopyTo(T[] array, int arrayIndex) => data.CopyTo(array, arrayIndex);
    public int IndexOf(T item) => data.IndexOf(item);
    public void Insert(int index, T item) => data.Insert(index, item);
    public bool Remove(T item) => data.Remove(item);
    public void RemoveAt(int index) => data.RemoveAt(index);

    public IEnumerator<T> GetEnumerator() => data.GetEnumerator();
    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}

internal class Program
{
    static void Main()
    {
        IList<int> royxat = new MaxsusRoyxat<int>();
        royxat.Add(100);
        royxat.Add(200);
        royxat[0] = 150;

        Console.WriteLine($"0-indeksdagi element: {royxat[0]}");
    }
}

```

## Tushuntirish va Mantiq:
IList<T> indeks bo'yicha kirish (`this[int]`), belgilangan joyga qo'shish (`Insert`) va o'chirish (`RemoveAt`) imkoniyatlarini qo'shadi.

## Ishlash natijasi:
```text
0-indeksdagi element: 150
```

# 538-Topshiriq: IReadOnlyList<T> va IReadOnlyDictionary<TKey, TValue> Mavhumligi
## Topshiriq sharti:
Kodni xavfsiz arxitekturada faqat o'qish interfeyslari orqali loyihalash.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

class FoydalanuvchiXizmati
{
    private readonly List<string> foydalanuvchilar = new() { "Anvar", "Dilshod" };

    // Tashqi dunyoga faqat IReadOnlyList ko'rsatamiz:
    public IReadOnlyList<string> Foydalanuvchilar => foydalanuvchilar;
}

internal class Program
{
    static void Main()
    {
        var xizmat = new FoydalanuvchiXizmati();
        IReadOnlyList<string> r = xizmat.Foydalanuvchilar;

        Console.WriteLine($"Birinchi foydalanuvchi: {r[0]}");
        // r.Add("Yangi"); // Kompilyatsiya xatosi: IReadOnlyList da Add mavjud emas!
    }
}

```

## Tushuntirish va Mantiq:
IReadOnlyList interfeysi ichki holatni tashqi ta'sirlardan saqlab, inkapsulyatsiyani ta'minlaydi.

## Ishlash natijasi:
```text
Birinchi foydalanuvchi: Anvar
```

# 539-Topshiriq: C# 12 Kolleksiya Ifodalari (Collection Expressions) va Spread `..` Operatori
## Topshiriq sharti:
Yangi qisqa va qulay `[...]` sintaksisi bilan to'plamlarni birlashtirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        int[] bir = [1, 2, 3];
        List<int> ikki = [4, 5, 6];

        // Spread .. operatori orqali ikkalasini ulab yangi massiv hosil qilamiz
        int[] birlashgan = [..bir, 99, ..ikki];

        Console.WriteLine($"Birlashgan massiv: {string.Join(", ", birlashgan)}");
    }
}

```

## Tushuntirish va Mantiq:
C# 12 da qavslar `[...]` massivlar, ro'yxatlar, Spanlar uchun yagona sintaksisni taqdim etadi va spread operatori `..` elementlarni qulay yoyadi.

## Ishlash natijasi:
```text
Birlashgan massiv: 1, 2, 3, 99, 4, 5, 6
```

# 540-Topshiriq: Maxsus [CollectionBuilder] Atributi (.NET 8+)
## Topshiriq sharti:
O'zingiz yaratgan maxsus sinfni C# 12 collection expressions `[...]` bilan ishlatish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.CompilerServices;

[CollectionBuilder(typeof(MaxsusKolleksiyaBuilder), "Create")]
class MaxsusKolleksiya : IEnumerable<int>
{
    private readonly int[] items;
    public MaxsusKolleksiya(ReadOnlySpan<int> span) => items = span.ToArray();

    public IEnumerator<int> GetEnumerator() => ((IEnumerable<int>)items).GetEnumerator();
    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}

static class MaxsusKolleksiyaBuilder
{
    public static MaxsusKolleksiya Create(ReadOnlySpan<int> span) => new(span);
}

internal class Program
{
    static void Main()
    {
        // C# 12 collection expression orqali maxsus sinf yaratish:
        MaxsusKolleksiya to'plam = [10, 20, 30, 40];

        Console.WriteLine($"Maxsus to'plam elementlari: {string.Join(", ", to'plam)}");
    }
}

```

## Tushuntirish va Mantiq:
[CollectionBuilder] atributi kompilyatorga `[...]` sintaksisi ishlatilganda qaysi builder metodni chaqirish kerakligini aytadi.

## Ishlash natijasi:
```text
Maxsus to'plam elementlari: 10, 20, 30, 40
```

# 541-Topshiriq: KeyedCollection<TKey, TItem> Gibrid Kolleksiyasi
## Topshiriq sharti:
Element ichidagi xususiyatni avtomatik kalit sifatida ishlatuvchi lug'at-ro'yxat gibridi.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.ObjectModel;

class Mahsulot
{
    public int Kod { get; set; }
    public string Nomi { get; set; } = "";
}

class MahsulotlarToplami : KeyedCollection<int, Mahsulot>
{
    protected override int GetKeyForItem(Mahsulot item) => item.Kod;
}

internal class Program
{
    static void Main()
    {
        var ombor = new MahsulotlarToplami();
        ombor.Add(new Mahsulot { Kod = 101, Nomi = "Monitor" });
        ombor.Add(new Mahsulot { Kod = 102, Nomi = "Klaviatura" });

        // Ham indeks orqali (0-element), ham kalit orqali (101-kod) murojaat qilish mumkin:
        Console.WriteLine($"Indeks bo'yicha: {ombor[0].Nomi}");
        Console.WriteLine($"Kalit bo'yicha: {ombor[102].Nomi}");
    }
}

```

## Tushuntirish va Mantiq:
KeyedCollection<TKey, TItem> ro'yxat kabi indekslangan tartibni saqlab qoladi va bir vaqtning o'zida kalit orqali $O(1)$ da elementni topish imkonini beradi.

## Ishlash natijasi:
```text
Indeks bo'yicha: Monitor
Kalit bo'yicha: Klaviatura
```

# 542-Topshiriq: ObservableCollection<T> va INotifyCollectionChanged
## Topshiriq sharti:
To'plamga element qo'shilganda yoki o'chirilganda voqea hosil qiluvchi kuzatuvchi ro'yxat.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.ObjectModel;
using System.Collections.Specialized;

internal class Program
{
    static void Main()
    {
        var kuzatiladigan = new ObservableCollection<string>();

        kuzatiladigan.CollectionChanged += (sender, e) =>
        {
            Console.WriteLine($"Hodisa turi: {e.Action}");
            if (e.NewItems != null)
            {
                foreach (var item in e.NewItems)
                    Console.WriteLine($"Yangi qo'shildi: {item}");
            }
        };

        kuzatiladigan.Add("Birinchi vazifa");
    }
}

```

## Tushuntirish va Mantiq:
ObservableCollection UI freymvorklarda (WPF, MAUI, Blazor) modeldagi o'zgarishlarni ekranda avtomatik aks ettirishda ishlatiladi.

## Ishlash natijasi:
```text
Hodisa turi: Add
Yangi qo'shildi: Birinchi vazifa
```

# 543-Topshiriq: Collection Initializer va Extension Add Metodi
## Topshiriq sharti:
Extension metod orqali mavjud sinfga `{ element1, element2 }` sintaksisini joriy qilish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections;
using System.Collections.Generic;

class Guruh : IEnumerable<string>
{
    private readonly List<string> a'zolar = new();

    public void AzoQosh(string ism) => a'zolar.Add(ism);

    public IEnumerator<string> GetEnumerator() => a'zolar.GetEnumerator();
    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}

static class GuruhExtensions
{
    // Kompilyator "Add" nomli metod qidiradi
    public static void Add(this Guruh g, string ism) => g.AzoQosh(ism);
}

internal class Program
{
    static void Main()
    {
        // Extension Add tufayli collection initializer ishlaydi:
        var guruh = new Guruh { "Sherzod", "Bobur", "Jasur" };

        Console.WriteLine($"A'zolar: {string.Join(", ", guruh)}");
    }
}

```

## Tushuntirish va Mantiq:
C# kompilyatori kolleksiya initsializatorlarida nafaqat sinfning o'z `Add` metodini, balki mos extension `Add` metodlarini ham qidiradi va chaqiradi.

## Ishlash natijasi:
```text
A'zolar: Sherzod, Bobur, Jasur
```

# 544-Topshiriq: Ko'p O'lchamli va Turli Tipli Indeksatorlar (Multi-Parameter Indexers)
## Topshiriq sharti:
Sinfga matritsa kabi `[qator, ustun]` yoki matnli indeksatorlar berish.

## Yechim (C# kodi):
```csharp
using System;

class Jadval
{
    private readonly string[,] kataklar = new string[3, 3];

    public string this[int qator, int ustun]
    {
        get => kataklar[qator, ustun];
        set => kataklar[qator, ustun] = value;
    }
}

internal class Program
{
    static void Main()
    {
        var jadval = new Jadval();
        jadval[0, 0] = "X";
        jadval[1, 1] = "O";
        jadval[2, 2] = "X";

        Console.WriteLine($"Markaziy katak: {jadval[1, 1]}");
    }
}

```

## Tushuntirish va Mantiq:
Indeksatorlar bittadan ortiq parametrlarni va turli xil tiplarni qabul qila oladi.

## Ishlash natijasi:
```text
Markaziy katak: O
```

# 545-Topshiriq: ReadOnlySpan<T> Ustida Xotira Ajratmasdan Sikl Aylanmasi
## Topshiriq sharti:
Hech qanday IEnumerable va Heap obyektlarsiz stack ustida to'plam aylanmasi.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        ReadOnlySpan<int> sonlar = stackalloc int[] { 10, 20, 30, 40 };

        int yigindi = 0;
        foreach (int n in sonlar)
        {
            yigindi += n;
        }

        Console.WriteLine($"Stackalloc va ReadOnlySpan yig'indisi: {yigindi}");
    }
}

```

## Tushuntirish va Mantiq:
ReadOnlySpan `GetEnumerator()` metodi ref struct qaytaradi va GC ga umuman yuk tushirmaydi.

## Ishlash natijasi:
```text
Stackalloc va ReadOnlySpan yig'indisi: 100
```

# 546-Topshiriq: ArrayPool<T>.Shared bilan Massivlarni Qayta Ishlatish
## Topshiriq sharti:
GC yukini kamaytirish uchun massivlarni ijaraga olish (Rent) va qaytarish (Return).

## Yechim (C# kodi):
```csharp
using System;
using System.Buffers;

internal class Program
{
    static void Main()
    {
        // 100 ta int uchun massiv ijaraga olamiz:
        int[] massiv = ArrayPool<int>.Shared.Rent(100);

        try
        {
            massiv[0] = 777;
            massiv[1] = 888;
            Console.WriteLine($"Massiv hajmi: {massiv.Length} (kamida 100)");
            Console.WriteLine($"0-element: {massiv[0]}");
        }
        finally
        {
            // Ishlatib bo'lgach havzaga qaytaramiz:
            ArrayPool<int>.Shared.Return(massiv);
            Console.WriteLine("Massiv havzaga muvaffaqiyatli qaytarildi.");
        }
    }
}

```

## Tushuntirish va Mantiq:
ArrayPool yirik massivlarni bot-bot `new` qilish o'rniga umumiy hovuzdan qayta-qayta foydalanish imkonini beradi va LOH (Large Object Heap) parchalanishini yo'qotadi.

## Ishlash natijasi:
```text
Massiv hajmi: 128 (kamida 100)
0-element: 777
Massiv havzaga muvaffaqiyatli qaytarildi.
```

# 547-Topshiriq: MemoryPool<T>.Shared va IMemoryOwner<T>
## Topshiriq sharti:
`IDisposable` orqali xotira buferlarini xavfsiz boshqarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Buffers;

internal class Program
{
    static void Main()
    {
        using (IMemoryOwner<byte> bufer = MemoryPool<byte>.Shared.Rent(1024))
        {
            Memory<byte> memory = bufer.Memory;
            memory.Span[0] = 255;

            Console.WriteLine($"Xotira buferi o'lchami: {memory.Length}");
            Console.WriteLine($"0-bayt: {memory.Span[0]}");
        } // using tugaganda avtomatik ravishda havzaga qaytariladi!

        Console.WriteLine("Xotira egasi xavfsiz tozalandi.");
    }
}

```

## Tushuntirish va Mantiq:
IMemoryOwner xotira blokiga egalik qiladi va uning `Dispose()` metodi xotirani avtomatik MemoryPool ga qaytaradi.

## Ishlash natijasi:
```text
Xotira buferi o'lchami: 1024
0-bayt: 255
Xotira egasi xavfsiz tozalandi.
```

# 548-Topshiriq: Aylanma Bufer (Circular Buffer / Ring Buffer) Kolleksiyasi
## Topshiriq sharti:
Oxirgi N ta ma'lumotni eslab qoluvchi o'zgarmas hajmli aylanma navbat.

## Yechim (C# kodi):
```csharp
using System;

class RingBuffer<T>
{
    private readonly T[] bufer;
    private int bosh = 0;
    private int oxir = 0;
    private int soni = 0;

    public RingBuffer(int hajm) => bufer = new T[hajm];

    public void Yozish(T item)
    {
        bufer[oxir] = item;
        oxir = (oxir + 1) % bufer.Length;
        if (soni < bufer.Length) soni++;
        else bosh = (bosh + 1) % bufer.Length; // Eskisini ustiga yozish
    }

    public void Chop()
    {
        Console.Write("Bufer tarkibi: ");
        for (int i = 0; i < soni; i++)
        {
            int indeks = (bosh + i) % bufer.Length;
            Console.Write($"{bufer[indeks]} ");
        }
        Console.WriteLine();
    }
}

internal class Program
{
    static void Main()
    {
        var rb = new RingBuffer<int>(3);
        rb.Yozish(1);
        rb.Yozish(2);
        rb.Yozish(3);
        rb.Chop();

        rb.Yozish(4); // 1 o'rniga 4 yoziladi
        rb.Chop();
    }
}

```

## Tushuntirish va Mantiq:
Aylanma bufer audio signallar, tarmoq paketlari va so'nggi loglar tarixini xotira kengaytirmasdan saqlashda ishlatiladi.

## Ishlash natijasi:
```text
Bufer tarkibi: 1 2 3 
Bufer tarkibi: 2 3 4
```

# 549-Topshiriq: PriorityQueue bilan K-ta Eng Katta Elementni Topish (Top-K Elements)
## Topshiriq sharti:
O'lchami cheklangan Min-Heap yordamida oqimdagi eng katta sonlarni ajratish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static List<int> TopK(int[] sonlar, int k)
    {
        var heap = new PriorityQueue<int, int>();

        foreach (var son in sonlar)
        {
            heap.Enqueue(son, son);
            if (heap.Count > k)
            {
                heap.Dequeue(); // Eng kichigini chiqarib tashlash
            }
        }

        List<int> natija = new();
        while (heap.Count > 0) natija.Add(heap.Dequeue());
        return natija;
    }

    static void Main()
    {
        int[] data = [4, 1, 9, 2, 8, 3, 7, 5];
        var top3 = TopK(data, 3);

        Console.WriteLine($"Eng katta 3 ta element: {string.Join(", ", top3)}");
    }
}

```

## Tushuntirish va Mantiq:
Min-Heap yordamida butun massivni saralamasdan $O(N \log K)$ murakkablikda eng katta $K$ ta element topiladi.

## Ishlash natijasi:
```text
Eng katta 3 ta element: 7, 8, 9
```

# 550-Topshiriq: Kolleksiyalar Xulosasi: LRU Kesh (Least Recently Used Cache) Arxitekturasi
## Topshiriq sharti:
`Dictionary` va `LinkedList` ni birlashtirib eng so'nggi ishlatilgan elementlarni boshqaruvchi $O(1)$ kesh quring.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

class LRUKesh<TKey, TValue> where TKey : notnull
{
    private readonly int hajm;
    private readonly Dictionary<TKey, LinkedListNode<(TKey Kalit, TValue Qiymat)>> xarita = new();
    private readonly LinkedList<(TKey Kalit, TValue Qiymat)> zanjir = new();

    public LRUKesh(int hajm) => this.hajm = hajm;

    public void Put(TKey kalit, TValue qiymat)
    {
        if (xarita.TryGetValue(kalit, out var tugun))
        {
            zanjir.Remove(tugun);
            zanjir.AddFirst(tugun);
            tugun.Value = (kalit, qiymat);
            return;
        }

        if (xarita.Count >= hajm)
        {
            var engEski = zanjir.Last!;
            xarita.Remove(engEski.Value.Kalit);
            zanjir.RemoveLast();
        }

        var yangiTugun = zanjir.AddFirst((kalit, qiymat));
        xarita[kalit] = yangiTugun;
    }

    public bool TryGet(TKey kalit, out TValue? qiymat)
    {
        if (xarita.TryGetValue(kalit, out var tugun))
        {
            zanjir.Remove(tugun);
            zanjir.AddFirst(tugun); // Eng boshiga ko'chiramiz
            qiymat = tugun.Value.Qiymat;
            return true;
        }
        qiymat = default;
        return false;
    }
}

internal class Program
{
    static void Main()
    {
        var kesh = new LRUKesh<int, string>(2);
        kesh.Put(1, "Bir");
        kesh.Put(2, "Ikki");

        kesh.TryGet(1, out _); // 1-elementga murojaat qilindi, demak 2 eng eski bo'lib qoldi

        kesh.Put(3, "Uch"); // 2 o'chiriladi!

        Console.WriteLine($"1 bormi: {kesh.TryGet(1, out _)}");
        Console.WriteLine($"2 bormi: {kesh.TryGet(2, out _)}");
        Console.WriteLine($"3 bormi: {kesh.TryGet(3, out _)}");
    }
}

```

## Tushuntirish va Mantiq:
LRU Kesh zamonaviy kesh tizimlarining (Redis, Memcached, HTTP Caching) asosi bo'lib, $O(1)$ qidiruv va $O(1)$ almashtirishni kafolatlaydi.

## Ishlash natijasi:
```text
1 bormi: True
2 bormi: False
3 bormi: True
```

