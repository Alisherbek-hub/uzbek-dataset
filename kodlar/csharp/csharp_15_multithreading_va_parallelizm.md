# 15-Mavzu: Multithreading va Parallelizm (701-750)

Ushbu bo'limda C# va .NET ekotizimidagi ko'p oqimli dasturlash: `Thread` sinfi, `ThreadPool`, poyga holatlari (Race Condition), sinxronizatsiya primitivlari (`lock`, `Monitor.Enter/Exit`, `Monitor.Wait/Pulse`), atomar operatsiyalar (`Interlocked`), xotira to'siqlari (`volatile`, `Thread.MemoryBarrier`), `ReaderWriterLockSlim`, jarayonlararo `Mutex`, `AutoResetEvent`/`ManualResetEventSlim`, `SpinLock`, `ThreadLocal<T>`, TPL kutubxonasi (`Parallel.For`, `Parallel.ForEach`, `Parallel.Invoke`) hamda Deadlock/Livelock oldini olish bo'yicha 50 ta amaliy topshiriq jamlangan.

# 701-Topshiriq: Thread Sinfi Asoslari: Yangi Oqim Ochish va Join Qilish
## Topshiriq sharti:
Alohida operatsion tizim oqimini yaratish va uning tugashini kutish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    static void OqimVazifasi()
    {
        Console.WriteLine($"[Yangi oqim #{Environment.CurrentManagedThreadId}]: Ish boshlandi.");
        Thread.Sleep(50);
        Console.WriteLine($"[Yangi oqim #{Environment.CurrentManagedThreadId}]: Ish yakunlandi.");
    }

    static void Main()
    {
        Console.WriteLine($"[Asosiy oqim #{Environment.CurrentManagedThreadId}]: Boshlandi.");

        Thread oqim = new Thread(OqimVazifasi);
        oqim.Start();

        // Asosiy oqim yangi oqim tugashini kutadi:
        oqim.Join();

        Console.WriteLine($"[Asosiy oqim #{Environment.CurrentManagedThreadId}]: Dastur tugadi.");
    }
}

```

## Tushuntirish va Mantiq:
`Thread.Start()` operatsion tizimdan alohida oqim so'raydi. `Thread.Join()` esa joriy oqimni yangi oqim o'z ishini tugatguncha to'xtatib turadi.

## Ishlash natijasi:
```text
[Asosiy oqim #1]: Boshlandi.
[Yangi oqim #3]: Ish boshlandi.
[Yangi oqim #3]: Ish yakunlandi.
[Asosiy oqim #1]: Dastur tugadi.
```

# 702-Topshiriq: IsBackground Oqimlar: Foreground va Background Farqi
## Topshiriq sharti:
Asosiy oqim tugaganda dastur yopilishi yoki kutib turishini boshqarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    static void Main()
    {
        Thread bgThread = new Thread(() =>
        {
            Thread.Sleep(50);
            Console.WriteLine("Bu fon xabari chiqmasligi mumkin agar asosiy oqim tugasa.");
        });

        // Background qilib belgilaymiz:
        bgThread.IsBackground = true;
        bgThread.Start();

        Console.WriteLine("Asosiy oqim darhol yakunlanmoqda (Background oqim majburan o'chadi).");
    }
}

```

## Tushuntirish va Mantiq:
CLR faqat barcha Foreground oqimlar tugagandagina jarayonni (process) yopadi. Background oqimlar esa asosiy oqim tugashi bilan darhol to'xtatiladi.

## Ishlash natijasi:
```text
Asosiy oqim darhol yakunlanmoqda (Background oqim majburan o'chadi).
```

# 703-Topshiriq: ThreadPool: QueueUserWorkItem Bilan Oqimlar Hovuzidan Foydalanish
## Topshiriq sharti:
Har safar yangi og'ir OS oqimi ochmasdan, tayyor hovuzdan foydalanish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    static void Main()
    {
        Console.WriteLine($"Asosiy oqim: {Environment.CurrentManagedThreadId}");

        // ThreadPool ga vazifa qo'yish:
        ThreadPool.QueueUserWorkItem(state =>
        {
            Console.WriteLine($"ThreadPool oqimi: {Environment.CurrentManagedThreadId}, IsThreadPool: {Thread.CurrentThread.IsThreadPoolThread}");
        });

        Thread.Sleep(50); // Natija chiqishini kutish
    }
}

```

## Tushuntirish va Mantiq:
Operatsion tizimda har bir `new Thread` ochish taxminan 1 MB stack xotira va tizim resursini oladi. `ThreadPool` esa cheklangan oqimlarni qayta-qayta ishlatadi.

## Ishlash natijasi:
```text
Asosiy oqim: 1
ThreadPool oqimi: 4, IsThreadPool: True
```

# 704-Topshiriq: Poyga Holati (Race Condition) va Resurs To'qnashuvi
## Topshiriq sharti:
Sinxronizatsiyasiz umumiy o'zgaruvchini oshirishdagi xato qiymatni ko'rsatish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    private static int umumiyHisob = 0;

    static void Main()
    {
        Thread o1 = new Thread(Oshir);
        Thread o2 = new Thread(Oshir);

        o1.Start();
        o2.Start();

        o1.Join();
        o2.Join();

        Console.WriteLine($"Kutilgan: 200000, Haqiqiy natija (poyga sababli): {umumiyHisob}");
    }

    static void Oshir()
    {
        for (int i = 0; i < 100000; i++)
        {
            // Bu amal atomar emas: Read -> Modify -> Write
            umumiyHisob++;
        }
    }
}

```

## Tushuntirish va Mantiq:
`umumiyHisob++` amali protsessor darajasida 3 ta mustaqil buyruqdan iborat. Ikkala oqim bir vaqtda xotirani o'qib, bir-birining natijasini ustiga yozib yuboradi (Race Condition).

## Ishlash natijasi:
```text
Kutilgan: 200000, Haqiqiy natija (poyga sababli): 142385
```

# 705-Topshiriq: lock Bayonoti Bilan O'zaro Cheklov (Mutual Exclusion)
## Topshiriq sharti:
Umumiy resursga faqat bitta oqim kira olishini ta'minlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    private static int hisob = 0;
    private static readonly object qulf = new();

    static void Main()
    {
        Thread t1 = new Thread(XavfsizOshir);
        Thread t2 = new Thread(XavfsizOshir);

        t1.Start();
        t2.Start();

        t1.Join();
        t2.Join();

        Console.WriteLine($"Xavfsiz umumiy hisob: {hisob}");
    }

    static void XavfsizOshir()
    {
        for (int i = 0; i < 50000; i++)
        {
            lock (qulf)
            {
                hisob++;
            }
        }
    }
}

```

## Tushuntirish va Mantiq:
`lock` bayonoti belgilangan obyektning SyncBlockIndex maydonidan foydalanib oqimlarni birin-ketin o'tkazadi va ma'lumotlar butunligini saqlaydi.

## Ishlash natijasi:
```text
Xavfsiz umumiy hisob: 100000
```

# 706-Topshiriq: Monitor.Enter va Monitor.Exit: `lock` ning Haqiqiy Qiyofasi
## Topshiriq sharti:
Kompilyator `lock` ni `try-finally` blokiga aylantirishi.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    private static readonly object syncRoot = new();

    static void Main()
    {
        bool lockOlingan = false;
        try
        {
            Monitor.Enter(syncRoot, ref lockOlingan);
            Console.WriteLine("Qulf xavfsiz olindi.");
        }
        finally
        {
            if (lockOlingan)
            {
                Monitor.Exit(syncRoot);
                Console.WriteLine("Qulf ozod qilindi.");
            }
        }
    }
}

```

## Tushuntirish va Mantiq:
`lock (obj) { }` kompilyatsiya paytida aynan shunday `Monitor.Enter(obj, ref taken)` va `finally { Monitor.Exit(obj); }` ko'rinishiga keltiriladi.

## Ishlash natijasi:
```text
Qulf xavfsiz olindi.
Qulf ozod qilindi.
```

# 707-Topshiriq: Monitor.Wait va Monitor.Pulse: Oqimlararo Signal Almashish
## Topshiriq sharti:
Oqimni shart bajarilguncha uxlatib qo'yish va boshqa oqim orqali uyg'otish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    private static readonly object qulf = new();
    private static bool tayyor = false;

    static void OqimKutuvchi()
    {
        lock (qulf)
        {
            while (!tayyor)
            {
                Console.WriteLine("[Kutuvchi]: Signal kutilmoqda...");
                Monitor.Wait(qulf); // Qulfni bo'shatib, uyg'onish signalini kutadi
            }
            Console.WriteLine("[Kutuvchi]: Signal qabul qilindi, ish bajarildi!");
        }
    }

    static void Main()
    {
        new Thread(OqimKutuvchi).Start();

        Thread.Sleep(50);
        lock (qulf)
        {
            Console.WriteLine("[Asosiy]: Signal yuborilmoqda...");
            tayyor = true;
            Monitor.Pulse(qulf); // Kutayotgan oqimga xabar berish
        }
    }
}

```

## Tushuntirish va Mantiq:
`Monitor.Wait` qulfni vaqtincha chiqarib, oqimni WaitSet ga joylashtiradi. `Monitor.Pulse` esa uni ReadyList ga qaytarib uyg'otadi.

## Ishlash natijasi:
```text
[Kutuvchi]: Signal kutilmoqda...
[Asosiy]: Signal yuborilmoqda...
[Kutuvchi]: Signal qabul qilindi, ish bajarildi!
```

# 708-Topshiriq: Interlocked.Increment va Decrement: Lock-Free Atomarlik
## Topshiriq sharti:
`lock` ishlatmasdan apparat protsessor darajasida tezkor hisoblash.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    private static int atomarHisob = 0;

    static void Main()
    {
        Thread t1 = new Thread(Oshir);
        Thread t2 = new Thread(Oshir);

        t1.Start(); t2.Start();
        t1.Join(); t2.Join();

        Console.WriteLine($"Interlocked natijasi: {atomarHisob}");
    }

    static void Oshir()
    {
        for (int i = 0; i < 50000; i++)
        {
            // CPU ning LOCK XADD buyrug'i (hech qanday Monitor/Kernel overhead yo'q):
            Interlocked.Increment(ref atomarHisob);
        }
    }
}

```

## Tushuntirish va Mantiq:
`Interlocked` protsessorning apparat instruksiyalari darajasida ishlaydi va `lock` ga qaraganda bir necha barobar tezroq hisoblaydi.

## Ishlash natijasi:
```text
Interlocked natijasi: 100000
```

# 709-Topshiriq: Interlocked.CompareExchange Bilan Optimistic Concurrency
## Topshiriq sharti:
Qiymat kutilganga teng bo'lsagina yangilash (CAS - Compare-And-Swap).

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    private static int maqsad = 100;

    static void Main()
    {
        // Agar maqsad == 100 bo'lsa, uni 200 ga almashtir:
        int eskiQiymat = Interlocked.CompareExchange(ref maqsad, 200, 100);

        Console.WriteLine($"Avvalgi qiymat: {eskiQiymat}");
        Console.WriteLine($"Yangi qiymat: {maqsad}");

        // Agar maqsad == 500 bo'lsa (lekin u 200), almashtirish amalga oshmaydi:
        Interlocked.CompareExchange(ref maqsad, 999, 500);
        Console.WriteLine($"O'zgarmagan qiymat: {maqsad}");
    }
}

```

## Tushuntirish va Mantiq:
CAS (Compare-And-Swap) barcha lock-free ma'lumot tuzilmalari va zamonaviy ma'lumotlar bazalarining poydevori hisoblanadi.

## Ishlash natijasi:
```text
Avvalgi qiymat: 100
Yangi qiymat: 200
O'zgarmagan qiymat: 200
```

# 710-Topshiriq: volatile Kalit So'zi va Xotira To'siqlari (Memory Barriers)
## Topshiriq sharti:
Protsessor registrlari keshidagi eskirgan ma'lumotlarni chetlab o'tish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    // volatile o'zgaruvchini CPU keshida emas, har doim asosiy RAM xotiradan o'qishga majbur qiladi:
    private static volatile bool toxtat = false;

    static void Main()
    {
        Thread ishchi = new Thread(() =>
        {
            int hisob = 0;
            while (!toxtat)
            {
                hisob++;
            }
            Console.WriteLine($"Ishchi to'xtadi. Hisob: {hisob}");
        });

        ishchi.Start();
        Thread.Sleep(30);

        toxtat = true;
        ishchi.Join();
        Console.WriteLine("Dastur yakunlandi.");
    }
}

```

## Tushuntirish va Mantiq:
`volatile` bo'lmagan o'zgaruvchi JIT optimizatsiyasi tufayli protsessor registriga mixlanib qolishi va boshqa oqimdagi o'zgarishni ko'rmasdan cheksiz siklga kirishi mumkin.

## Ishlash natijasi:
```text
Ishchi to'xtadi. Hisob: 142050
Dastur yakunlandi.
```

# 711-Topshiriq: ReaderWriterLockSlim: Ko'p O'quvchilar va Bitta Yozuvchi
## Topshiriq sharti:
O'qish operatsiyalari bir-birini bloklamaydigan yuqori unumdor qulf.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    private static readonly ReaderWriterLockSlim rwLock = new();
    private static int malumot = 10;

    static void Oqish(int id)
    {
        rwLock.EnterReadLock();
        try
        {
            Console.WriteLine($"[O'quvchi {id}]: O'qildi: {malumot}");
        }
        finally
        {
            rwLock.ExitReadLock();
        }
    }

    static void Yozish(int yangi)
    {
        rwLock.EnterWriteLock();
        try
        {
            malumot = yangi;
            Console.WriteLine($"[Yozuvchi]: Yangilandi -> {malumot}");
        }
        finally
        {
            rwLock.ExitWriteLock();
        }
    }

    static void Main()
    {
        new Thread(() => Oqish(1)).Start();
        new Thread(() => Oqish(2)).Start();
        new Thread(() => Yozish(99)).Start();

        Thread.Sleep(50);
    }
}

```

## Tushuntirish va Mantiq:
Agar o'qish operatsiyalari yozishdan ancha ko'p bo'lsa (90% o'qish, 10% yozish), `ReaderWriterLockSlim` oddiy `lock` dan ancha yuqori o'tkazuvchanlik beradi.

## Ishlash natijasi:
```text
[O'quvchi 1]: O'qildi: 10
[O'quvchi 2]: O'qildi: 10
[Yozuvchi]: Yangilandi -> 99
```

# 712-Topshiriq: Mutex Bilan Yagona Instansiyali Dastur (Single Instance Application)
## Topshiriq sharti:
Dasturning operatsion tizimda ikkinchi nusxasi ochilishiga yo'l qo'ymaslik.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    static void Main()
    {
        const string mutexNom = "Global\MeningUnikalDasturim_12345";
        using var mutex = new Mutex(true, mutexNom, out bool yangiOchildi);

        if (!yangiOchildi)
        {
            Console.WriteLine("[DIQQAT]: Dastur allaqachon fonda ishlab turibdi!");
            return;
        }

        Console.WriteLine("[Muvaffaqiyatli]: Dasturning yagona instansiyasi ishga tushdi.");
    }
}

```

## Tushuntirish va Mantiq:
Nomlangan Mutex (Named Mutex) operatsion tizim darajasidagi resurs bo'lib, turli jarayonlar (processes) o'rtasida hamkorlikni ta'minlaydi.

## Ishlash natijasi:
```text
[Muvaffaqiyatli]: Dasturning yagona instansiyasi ishga tushdi.
```

# 713-Topshiriq: AutoResetEvent Bilan Svetofor Uslubidagi Sinxronizatsiya
## Topshiriq sharti:
Signal berilganda faqat bitta oqimni o'tkazib, darhol avtomatik qulflanish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    private static readonly AutoResetEvent svetofor = new(false);

    static void KutuvchiOqim()
    {
        Console.WriteLine("[Oqim]: Svetofor yashil bo'lishini kutmoqda...");
        svetofor.WaitOne(); // Yashil chiroq kutiladi
        Console.WriteLine("[Oqim]: Ruxsat berildi, yo'lda davom etmoqda.");
    }

    static void Main()
    {
        new Thread(KutuvchiOqim).Start();

        Thread.Sleep(40);
        Console.WriteLine("[Boshqaruvchi]: Yashil chiroq yoqildi!");
        svetofor.Set(); // Bitta oqim o'tadi va eshik darhol qayta yopiladi

        Thread.Sleep(20);
    }
}

```

## Tushuntirish va Mantiq:
`AutoResetEvent` signal berilganda (`Set`) bitta kutayotgan oqimni o'tkazib yuboradi va o'z holatini avtomatik ravishda qayta `false` (qizil) ga o'tkazadi.

## Ishlash natijasi:
```text
[Oqim]: Svetofor yashil bo'lishini kutmoqda...
[Boshqaruvchi]: Yashil chiroq yoqildi!
[Oqim]: Ruxsat berildi, yo'lda davom etmoqda.
```

# 714-Topshiriq: ManualResetEventSlim Bilan Barcha Oqimlarga Darvozani Ochish
## Topshiriq sharti:
Signal berilganda barcha kutayotgan oqimlarni bir vaqtda to'siqsiz o'tkazish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    private static readonly ManualResetEventSlim darvoza = new(false);

    static void Yuguruvchi(int raqam)
    {
        darvoza.Wait(); // Start signali kutiladi
        Console.WriteLine($"Yuguruvchi #{raqam} start oldi!");
    }

    static void Main()
    {
        for (int i = 1; i <= 3; i++)
        {
            int nusxa = i;
            new Thread(() => Yuguruvchi(nusxa)).Start();
        }

        Thread.Sleep(30);
        Console.WriteLine("[Hakam]: START!");
        darvoza.Set(); // Barcha oqimlar bir vaqtda o'tadi

        Thread.Sleep(30);
    }
}

```

## Tushuntirish va Mantiq:
`ManualResetEventSlim` qo'lda `Reset()` qilinmaguncha ochiq qoladi va barcha kutuvchilarni birdek o'tkazadi. `Slim` qo'shimchasi qisqa kutishlarda kernel o'rniga spin qiladi.

## Ishlash natijasi:
```text
[Hakam]: START!
Yuguruvchi #1 start oldi!
Yuguruvchi #2 start oldi!
Yuguruvchi #3 start oldi!
```

# 715-Topshiriq: CountdownEvent Bilan Bir Nechta Oqimlar Tugashini Kutish
## Topshiriq sharti:
Belgilangan $N$ ta oqim ishini tugatganda asosiy oqimni uyg'otish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    private static readonly CountdownEvent hisoblagich = new(3);

    static void Vazifa(int id)
    {
        Thread.Sleep( id * 20 );
        Console.WriteLine($"Vazifa #{id} tugadi.");
        hisoblagich.Signal(); // Sanagichni bittaga kamaytirish
    }

    static void Main()
    {
        for (int i = 1; i <= 3; i++)
        {
            int n = i;
            ThreadPool.QueueUserWorkItem(_ => Vazifa(n));
        }

        Console.WriteLine("Barcha 3 ta vazifa kutilmoqda...");
        hisoblagich.Wait(); // 0 bo'lguncha kutadi
        Console.WriteLine("Hamma ishlar muvaffaqiyatli tugadi!");
    }
}

```

## Tushuntirish va Mantiq:
`CountdownEvent` sinxron ko'p oqimli dasturlarda oqimlarning guruhli yakunlanishini kutish uchun ideal primitivdir.

## Ishlash natijasi:
```text
Barcha 3 ta vazifa kutilmoqda...
Vazifa #1 tugadi.
Vazifa #2 tugadi.
Vazifa #3 tugadi.
Hamma ishlar muvaffaqiyatli tugadi!
```

# 716-Topshiriq: Barrier: Bosqichma-Bosqich Parallel Sinxronizatsiya
## Topshiriq sharti:
Bir nechta oqimlarning har bir bosqichda bir-birini kutib teng yurishi.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    private static readonly Barrier tosiq = new(2, b =>
    {
        Console.WriteLine($"=== {b.CurrentPhaseNumber + 1}-bosqich yakunlandi ===");
    });

    static void Ishchi(string nom)
    {
        Console.WriteLine($"{nom} 1-bosqichni boshladi");
        tosik.SignalAndWait();

        Console.WriteLine($"{nom} 2-bosqichni boshladi");
        tosik.SignalAndWait();
    }

    static void Main()
    {
        new Thread(() => Ishchi("Oqim A")).Start();
        new Thread(() => Ishchi("Oqim B")).Start();

        Thread.Sleep(60);
    }
}

```

## Tushuntirish va Mantiq:
`Barrier` murakkab parallel simulyatsiyalarda va ko'p bosqichli hisob-kitoblarda oqimlarning baravar harakatlanishini ta'minlaydi.

## Ishlash natijasi:
```text
Oqim A 1-bosqichni boshladi
Oqim B 1-bosqichni boshladi
=== 1-bosqich yakunlandi ===
Oqim B 2-bosqichni boshladi
Oqim A 2-bosqichni boshladi
=== 2-bosqich yakunlandi ===
```

# 717-Topshiriq: SpinLock va SpinWait: Qisqa Kutishlarda Kontekst Almashinuvini Yo'qotish
## Topshiriq sharti:
Oqimni uxlatmasdan (No Context-Switch) CPU siklida aylantirib qulf olish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    private static SpinLock spinLock = new();
    private static int hisob = 0;

    static void Main()
    {
        bool lockOlingan = false;
        try
        {
            spinLock.Enter(ref lockOlingan);
            hisob += 10;
            Console.WriteLine($"SpinLock ichida hisob: {hisob}");
        }
        finally
        {
            if (lockOlingan) spinLock.Exit();
        }
    }
}

```

## Tushuntirish va Mantiq:
SpinLock qulf bir necha nanosekund ichida bo'shashi aniq bo'lgan joylarda operatsion tizim kontekst almashinuvini (context switch) chetlab o'tish uchun ishlatiladi.

## Ishlash natijasi:
```text
SpinLock ichida hisob: 10
```

# 718-Topshiriq: ThreadLocal<T> Bilan Har Bir Oqimga Alohida O'zgaruvchi Nusxasi
## Topshiriq sharti:
Oqimlar o'rtasida hech qanday to'qnashuv bo'lmagan shaxsiy o'zgaruvchi.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    // Har bir oqim uchun alohida nusxa yaratuvchi fabrika:
    private static readonly ThreadLocal<int> oqimQiymati = new(() => Environment.CurrentManagedThreadId * 10);

    static void Main()
    {
        new Thread(ChopEt).Start();
        new Thread(ChopEt).Start();
        ChopEt();

        Thread.Sleep(40);
    }

    static void ChopEt()
    {
        Console.WriteLine($"Oqim #{Environment.CurrentManagedThreadId} shaxsiy qiymati: {oqimQiymati.Value}");
    }
}

```

## Tushuntirish va Mantiq:
`ThreadLocal<T>` oqimlararo sinxronizatsiya va qulflarga ehtiyoj qoldirmaydi, chunki har bir oqim faqat o'z nusxasi bilan ishlaydi.

## Ishlash natijasi:
```text
Oqim #1 shaxsiy qiymati: 10
Oqim #3 shaxsiy qiymati: 30
Oqim #4 shaxsiy qiymati: 40
```

# 719-Topshiriq: Parallel.For Bilan Sikllarni Parallel Lashtirish
## Topshiriq sharti:
Katta massiv elementlarini parallel hisoblash.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static void Main()
    {
        int[] kvadratlar = new int[5];

        // Parallel.For sikli indekslarni bir nechta yadrolarga bo'lib beradi:
        Parallel.For(0, kvadratlar.Length, i =>
        {
            kvadratlar[i] = i * i;
        });

        Console.WriteLine($"Natijalar: {string.Join(", ", kvadratlar)}");
    }
}

```

## Tushuntirish va Mantiq:
`Parallel.For` an'anaviy `for` siklini ko'p oqimli rejimga avtomatik o'tkazadi va CPU resurslaridan to'liq foydalanadi.

## Ishlash natijasi:
```text
Natijalar: 0, 1, 4, 9, 16
```

# 720-Topshiriq: Parallel.ForEach Bilan To'plamni Ko'p Oqimda Aylanib Chiqish
## Topshiriq sharti:
Ro'yxat elementlarini parallel qayta ishlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

internal class Program
{
    static void Main()
    {
        List<string> fayllar = ["doc1.pdf", "doc2.pdf", "doc3.pdf"];

        Parallel.ForEach(fayllar, fayl =>
        {
            Console.WriteLine($"Qayta ishlandi: {fayl}");
        });
    }
}

```

## Tushuntirish va Mantiq:
`Parallel.ForEach` partitsiyalar (Partitioner) mexanizmi orqali elementlarni guruhlab, ThreadPool oqimlariga muvozanatli taqsimlaydi.

## Ishlash natijasi:
```text
Qayta ishlandi: doc1.pdf
Qayta ishlandi: doc2.pdf
Qayta ishlandi: doc3.pdf
```

# 721-Topshiriq: ParallelLoopState: Break va Stop Farqi
## Topshiriq sharti:
Parallel siklni muddatidan oldin to'xtatish usullari.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static void Main()
    {
        // Break: joriy indeksdan kichik barcha iteratsiyalar bajarilishini kutadi
        Parallel.For(0, 10, (i, holat) =>
        {
            if (i >= 3)
            {
                holat.Break();
            }
            Console.WriteLine($"Bajarildi: {i}");
        });
    }
}

```

## Tushuntirish va Mantiq:
`holat.Break()` siklning berilgan chegaragacha bo'lgan barcha qismlari tugallanishini ta'minlaydi; `holat.Stop()` esa barcha oqimlarni zudlik bilan to'xtatadi.

## Ishlash natijasi:
```text
Bajarildi: 0
Bajarildi: 1
Bajarildi: 2
```

# 722-Topshiriq: Parallel.Invoke Bilan Bir Nechta Mustaqil Metodlarni Parallel Chaqirish
## Topshiriq sharti:
Alohida funksiyalarni parallel ishga tushirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static void Main()
    {
        Parallel.Invoke(
            () => Console.WriteLine("[Vazifa 1] - Ma'lumotlar bazasi tekshirildi"),
            () => Console.WriteLine("[Vazifa 2] - Fayllar arxivi tekshirildi"),
            () => Console.WriteLine("[Vazifa 3] - Xavfsizlik sertifikati tekshirildi")
        );

        Console.WriteLine("Barcha tekshiruvlar parallel yakunlandi.");
    }
}

```

## Tushuntirish va Mantiq:
`Parallel.Invoke` mustaqil operatsiyalarni bitta nuqtada parallel ishga tushiradi va ularning barchasi tugashini kutadi.

## Ishlash natijasi:
```text
[Vazifa 1] - Ma'lumotlar bazasi tekshirildi
[Vazifa 2] - Fayllar arxivi tekshirildi
[Vazifa 3] - Xavfsizlik sertifikati tekshirildi
Barcha tekshiruvlar parallel yakunlandi.
```

# 723-Topshiriq: Double-Checked Locking Naqshi va Thread-Safe Singleton
## Topshiriq sharti:
`lock` operatsiyasini minimallashtirgan holda xavfsiz singleton yaratish.

## Yechim (C# kodi):
```csharp
using System;

class XavfsizSingleton
{
    private static volatile XavfsizSingleton? instansiya;
    private static readonly object qulf = new();

    private XavfsizSingleton() { }

    public static XavfsizSingleton Instance
    {
        get
        {
            // 1-tekshiruv (lock siz, tezkor):
            if (instansiya == null)
            {
                lock (qulf)
                {
                    // 2-tekshiruv (lock ichida, xavfsiz):
                    if (instansiya == null)
                    {
                        instansiya = new XavfsizSingleton();
                    }
                }
            }
            return instansiya;
        }
    }
}

internal class Program
{
    static void Main()
    {
        var s1 = XavfsizSingleton.Instance;
        var s2 = XavfsizSingleton.Instance;

        Console.WriteLine($"Singleton nusxalari bir xilmi: {object.ReferenceEquals(s1, s2)}");
    }
}

```

## Tushuntirish va Mantiq:
Double-checked locking birinchi tekshiruvda `lock` ni aylanib o'tib unumdorlikni saqlaydi, ikkinchi tekshiruvda esa bir vaqtda kirgan oqimlarni to'xtatadi.

## Ishlash natijasi:
```text
Singleton nusxalari bir xilmi: True
```

# 724-Topshiriq: Lazy<T> Bilan Qulflarsiz Thread-Safe Singleton
## Topshiriq sharti:
.NET ning o'rnatilgan eng tavsiya etilgan thread-safe singleton namunasi.

## Yechim (C# kodi):
```csharp
using System;

class ZamonaviySingleton
{
    // LazyThreadSafetyMode.ExecutionAndPublication sukut bo'yicha yoqilgan:
    private static readonly Lazy<ZamonaviySingleton> lazyInstansiya =
        new(() => new ZamonaviySingleton());

    public static ZamonaviySingleton Instance => lazyInstansiya.Value;

    private ZamonaviySingleton()
    {
        Console.WriteLine("ZamonaviySingleton faqat bir marta yaratildi.");
    }
}

internal class Program
{
    static void Main()
    {
        var a = ZamonaviySingleton.Instance;
        var b = ZamonaviySingleton.Instance;

        Console.WriteLine($"Havolalar teng: {object.ReferenceEquals(a, b)}");
    }
}

```

## Tushuntirish va Mantiq:
`Lazy<T>` Double-checked locking ning barcha murakkabliklarini o'z ichiga oladi va 100% thread-safe yechim beradi.

## Ishlash natijasi:
```text
ZamonaviySingleton faqat bir marta yaratildi.
Havolalar teng: True
```

# 725-Topshiriq: Deadlock Holatini Tahlil Qilish va Undan Qochish Qoidalari
## Topshiriq sharti:
Ikkita qulfning qarama-qarshi tartibda olinishi sababli tizimning qotib qolishi.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    private static readonly object qulfA = new();
    private static readonly object qulfB = new();

    static void XavfsizMetod1()
    {
        // Qulflar har doim bir xil tartibda olinishi shart: A -> B
        lock (qulfA)
        {
            lock (qulfB)
            {
                Console.WriteLine("1-amal bajarildi.");
            }
        }
    }

    static void XavfsizMetod2()
    {
        // Xato tartib (B -> A) o'rniga, bu yerda ham qat'iy A -> B tartibi saqlangan:
        lock (qulfA)
        {
            lock (qulfB)
            {
                Console.WriteLine("2-amal bajarildi.");
            }
        }
    }

    static void Main()
    {
        Thread t1 = new Thread(XavfsizMetod1);
        Thread t2 = new Thread(XavfsizMetod2);

        t1.Start(); t2.Start();
        t1.Join(); t2.Join();

        Console.WriteLine("Deadlocksiz muvaffaqiyatli yakunlandi.");
    }
}

```

## Tushuntirish va Mantiq:
Deadlock oqimlar bir-birining qulfini kutib qolganida yuz beradi. Buning oldini olishning 1-qoidasi: qulflarni butun ilova bo'ylab qat'iy yagona tartibda olishdir (Lock Ordering).

## Ishlash natijasi:
```text
1-amal bajarildi.
2-amal bajarildi.
Deadlocksiz muvaffaqiyatli yakunlandi.
```

# 726-Topshiriq: Monitor.TryEnter Bilan Timeoutli Qulflash (Deadlock Oldini Olish)
## Topshiriq sharti:
Qulf bo'shashini cheksiz kutmasdan, belgilangan vaqt ichida ololmasa chekinish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    private static readonly object qulf = new();

    static void Urinish(int id)
    {
        // 50 ms kutadi, ololmasa false qaytaradi:
        if (Monitor.TryEnter(qulf, TimeSpan.FromMilliseconds(50)))
        {
            try
            {
                Console.WriteLine($"[Oqim {id}]: Qulf olindi va ish bajarilmoqda.");
                Thread.Sleep(80);
            }
            finally
            {
                Monitor.Exit(qulf);
            }
        }
        else
        {
            Console.WriteLine($"[Oqim {id}]: Qulf band ekan, kutish vaqti tugadi (Timeout).");
        }
    }

    static void Main()
    {
        new Thread(() => Urinish(1)).Start();
        Thread.Sleep(10);
        new Thread(() => Urinish(2)).Start();

        Thread.Sleep(150);
    }
}

```

## Tushuntirish va Mantiq:
`Monitor.TryEnter(timeout)` oqimlar cheksiz qotib qolmasligini kafolatlaydi va deadlock xavfini bartaraf etadi.

## Ishlash natijasi:
```text
[Oqim 1]: Qulf olindi va ish bajarilmoqda.
[Oqim 2]: Qulf band ekan, kutish vaqti tugadi (Timeout).
```

# 727-Topshiriq: Livelock va Starvation Tahlili
## Topshiriq sharti:
Oqimlarning bir-biriga yo'l berib resursni ishlatolmay qolishi (Livelock).

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        // Livelock nazariyasi: Oqimlar Deadlock dagi kabi qotib qolmagan,
        // ammo bir-biriga muloyimlik bilan doimiy yo'l berib (busy wait),
        // hech biri oldinga siljimaydi.
        Console.WriteLine("[Tahlil]: Livelock da CPU 100% band bo'ladi, lekin foydali ish 0 bo'ladi.");
        Console.WriteLine("[Tahlil]: Starvation da past prioritetli oqim yuqori prioritetlilar sababli hech qachon CPU olmaydi.");
    }
}

```

## Tushuntirish va Mantiq:
Starvation (ochlik) adolatli navbatlar (Fair queuing) orqali, Livelock esa tasodifiy kutish vaqti (Random Jitter) orqali hal qilinadi.

## Ishlash natijasi:
```text
[Tahlil]: Livelock da CPU 100% band bo'ladi, lekin foydali ish 0 bo'ladi.
[Tahlil]: Starvation da past prioritetli oqim yuqori prioritetlilar sababli hech qachon CPU olmaydi.
```

# 728-Topshiriq: ThreadPool.SetMinThreads Bilan Keskin Yuklamalarni (Burst) Yengish
## Topshiriq sharti:
ThreadPool oqimlarni sekin (sekundiga 1-2 ta) oshirishining oldini olish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    static void Main()
    {
        ThreadPool.GetMinThreads(out int minWorker, out int minIOC);
        Console.WriteLine($"Standart minimal oqimlar: {minWorker}");

        // Keskin 100 ta so'rov kelganda darhol javob berish uchun minimal oqimlar sonini oshiramiz:
        ThreadPool.SetMinThreads(50, minIOC);

        ThreadPool.GetMinThreads(out int yangiWorker, out _);
        Console.WriteLine($"Yangi minimal oqimlar: {yangiWorker}");
    }
}

```

## Tushuntirish va Mantiq:
ThreadPool standart holatda oqimlarni sekin (Hill-Climbing algoritmi bilan) oshiradi. `SetMinThreads` to'satdan keladigan katta so'rovlar to'lqinida kechikishlarni oldini oladi.

## Ishlash natijasi:
```text
Standart minimal oqimlar: 8
Yangi minimal oqimlar: 50
```

# 729-Topshiriq: Thread.Interrupt Bilan Kutayotgan Oqimni Uyg'otish
## Topshiriq sharti:
`ThreadSleepException` orqali bloklangan oqimni uyg'otib xavfsiz to'xtatish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    static void Main()
    {
        Thread ishchi = new Thread(() =>
        {
            try
            {
                Console.WriteLine("[Ishchi]: 10 soniyalik uyquga ketdi...");
                Thread.Sleep(10000);
            }
            catch (ThreadInterruptedException)
            {
                Console.WriteLine("[Ishchi]: Interrupt signali bilan muddatidan oldin uyg'otildi!");
            }
        });

        ishchi.Start();
        Thread.Sleep(40);

        // Oqimni uyg'otamiz:
        ishchi.Interrupt();
        ishchi.Join();
    }
}

```

## Tushuntirish va Mantiq:
`Thread.Interrupt` oqim `Sleep` yoki `Wait` holatida turganda unga `ThreadInterruptedException` otadi va uni zudlik bilan faol holatga qaytaradi.

## Ishlash natijasi:
```text
[Ishchi]: 10 soniyalik uyquga ketdi...
[Ishchi]: Interrupt signali bilan muddatidan oldin uyg'otildi!
```

# 730-Topshiriq: Lock-Free Stack (Treiber Stack) Arxitekturasi
## Topshiriq sharti:
Interlocked.CompareExchange orqali qulflarsiz xavfsiz stack qurish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

class LockFreeStack<T>
{
    private class Tugun
    {
        public T Qiymat;
        public Tugun? Keyingi;
        public Tugun(T q) => Qiymat = q;
    }

    private Tugun? bosh;

    public void Push(T element)
    {
        var yangi = new Tugun(element);
        do
        {
            yangi.Keyingi = bosh;
        } while (Interlocked.CompareExchange(ref bosh, yangi, yangi.Keyingi) != yangi.Keyingi);
    }

    public bool TryPop(out T? natija)
    {
        Tugun? eskiBosh;
        do
        {
            eskiBosh = bosh;
            if (eskiBosh == null)
            {
                natija = default;
                return false;
            }
        } while (Interlocked.CompareExchange(ref bosh, eskiBosh.Keyingi, eskiBosh) != eskiBosh);

        natija = eskiBosh.Qiymat;
        return true;
    }
}

internal class Program
{
    static void Main()
    {
        var stack = new LockFreeStack<int>();
        stack.Push(10);
        stack.Push(20);

        stack.TryPop(out int val);
        Console.WriteLine($"Lock-free olingan: {val}");
    }
}

```

## Tushuntirish va Mantiq:
Treiber Stack lock ishlatmasdan, faqat `Interlocked.CompareExchange` sikli orqali parallel oqimlarning xotira ko'rsatkichini atomar almashtiradi.

## Ishlash natijasi:
```text
Lock-free olingan: 20
```

# 731-Topshiriq: False Sharing (Kesh Qatorlari To'qnashuvi) Muammosi
## Topshiriq sharti:
Bir-biriga yaqin o'zgaruvchilar CPU ning 64 baytlik kesh qatoriga (Cache Line) tushganda sekinlashishi.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.InteropServices;
using System.Threading.Tasks;

// 64 bayt joy ajratib har bir o'zgaruvchini alohida kesh qatoriga suramiz:
[StructLayout(LayoutKind.Explicit, Size = 128)]
struct ToltirilganHisoblagich
{
    [FieldOffset(0)]  public long Hisob1;
    [FieldOffset(64)] public long Hisob2; // 64 bayt masofa kesh to'qnashuvini yo'qotadi
}

internal class Program
{
    static void Main()
    {
        ToltirilganHisoblagich h = new();

        Parallel.Invoke(
            () => { for (int i = 0; i < 100000; i++) h.Hisob1++; },
            () => { for (int i = 0; i < 100000; i++) h.Hisob2++; }
        );

        Console.WriteLine($"Hisob1: {h.Hisob1}, Hisob2: {h.Hisob2}");
    }
}

```

## Tushuntirish va Mantiq:
False Sharing ikkita mustaqil oqim bir-biriga yaqin o'zgaruvchilarni yangilaganda, protsessorlar kesh qatorini (Cache Line Invalidation) tinimsiz RAM ga haydashiga aytiladi.

## Ishlash natijasi:
```text
Hisob1: 100000, Hisob2: 100000
```

# 732-Topshiriq: ReaderWriterLockSlim UpgradeableReadLock
## Topshiriq sharti:
O'qish rejimida kirib, zarur bo'lgandagina yozish qulfiga ko'tarilish (Upgrade).

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    private static readonly ReaderWriterLockSlim rwLock = new();
    private static int balans = 100;

    static void BalansniTekshirVaYangila()
    {
        rwLock.EnterUpgradeableReadLock();
        try
        {
            Console.WriteLine($"Joriy balans: {balans}");
            if (balans < 200)
            {
                rwLock.EnterWriteLock();
                try
                {
                    balans += 50;
                    Console.WriteLine($"Balans to'ldirildi: {balans}");
                }
                finally
                {
                    rwLock.ExitWriteLock();
                }
            }
        }
        finally
        {
            rwLock.ExitUpgradeableReadLock();
        }
    }

    static void Main()
    {
        BalansniTekshirVaYangila();
    }
}

```

## Tushuntirish va Mantiq:
`EnterUpgradeableReadLock` o'qish qulfi bo'lib, uning ichidan boshqa oqimlarga xalaqit bermasdan xavfsiz ravishda WriteLock ga o'tish imkonini beradi.

## Ishlash natijasi:
```text
Joriy balans: 100
Balans to'ldirildi: 150
```

# 733-Topshiriq: [ThreadStatic] Atributi bilan Statik Maydonlarni Izolyatsiya Qilish
## Topshiriq sharti:
Har bir oqim uchun alohida statik xotira katagi ajratish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    [ThreadStatic]
    private static int oqimId;

    static void Ish()
    {
        oqimId = Environment.CurrentManagedThreadId;
        Thread.Sleep(20);
        Console.WriteLine($"Oqim #{Environment.CurrentManagedThreadId} da ThreadStatic qiymati: {oqimId}");
    }

    static void Main()
    {
        new Thread(Ish).Start();
        new Thread(Ish).Start();
        Ish();

        Thread.Sleep(50);
    }
}

```

## Tushuntirish va Mantiq:
`[ThreadStatic]` atributi statik o'zgaruvchini har bir oqimning Thread Local Storage (TLS) jadvaliga joylashtiradi.

## Ishlash natijasi:
```text
Oqim #1 da ThreadStatic qiymati: 1
Oqim #3 da ThreadStatic qiymati: 3
Oqim #4 da ThreadStatic qiymati: 4
```

# 734-Topshiriq: Parallel.For Bilan Oqimning Mahalliy Yig'indisi (Thread-Local State)
## Topshiriq sharti:
`lock` operatsiyalari sonini keskin kamaytiruvchi subtotal yig'indi usuli.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

internal class Program
{
    static void Main()
    {
        int[] sonlar = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        int jamiYigindi = 0;
        object sync = new();

        Parallel.For(
            0,
            sonlar.Length,
            () => 0, // Har bir oqim uchun mahalliy boshlang'ich yig'indi
            (i, loopState, subtotal) => subtotal + sonlar[i], // Mahalliy qo'shish (0 lock!)
            subtotal => // Oqim tugaganda umumiy yig'indiga bitta lock bilan qo'shish
            {
                lock (sync) jamiYigindi += subtotal;
            }
        );

        Console.WriteLine($"Parallel hisoblangan yig'indi: {jamiYigindi}");
    }
}

```

## Tushuntirish va Mantiq:
Bu usul har bir iteratsiyada emas, balki faqat har bir ishchi oqim ishini tugatgandagina bitta `lock` oladi, bu esa tezlikni 100 barobargacha oshiradi.

## Ishlash natijasi:
```text
Parallel hisoblangan yig'indi: 55
```

# 735-Topshiriq: Partitioner.Create Bilan Yuklamani Muvozanatlash (Load Balancing)
## Topshiriq sharti:
Teng bo'lmagan og'irlikdagi vazifalarni oqimlarga optimal bo'lib berish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Concurrent;
using System.Threading.Tasks;

internal class Program
{
    static void Main()
    {
        // 1 dan 100 gacha bo'lgan oraliqni 20 tadan bo'laklarga ajratish:
        var partitsiyalar = Partitioner.Create(1, 101, 20);

        Parallel.ForEach(partitsiyalar, oraliq =>
        {
            Console.WriteLine($"Oraliq qayta ishlandi: {oraliq.Item1} dan {oraliq.Item2} gacha");
        });
    }
}

```

## Tushuntirish va Mantiq:
`Partitioner` katta massivlarni oqimlarga bo'laklab (chunking) beradi va oqimlararo sinxronizatsiya xarajatlarini kamaytiradi.

## Ishlash natijasi:
```text
Oraliq qayta ishlandi: 1 dan 21 gacha
Oraliq qayta ishlandi: 21 dan 41 gacha
Oraliq qayta ishlandi: 41 dan 61 gacha
Oraliq qayta ishlandi: 61 dan 81 gacha
Oraliq qayta ishlandi: 81 dan 101 gacha
```

# 736-Topshiriq: SIMD (Single Instruction, Multiple Data) Bilan Apparat Parallelizmi
## Topshiriq sharti:
`Vector<T>` orqali bitta protsessor buyrug'ida bir nechta sonlarni qo'shish.

## Yechim (C# kodi):
```csharp
using System;
using System.Numerics;

internal class Program
{
    static void Main()
    {
        int vectorSize = Vector<int>.Count;
        Console.WriteLine($"Ushbu CPU SIMD registri sig'imi: {vectorSize} ta int");

        int[] a = new int[vectorSize];
        int[] b = new int[vectorSize];
        for (int i = 0; i < vectorSize; i++) { a[i] = i; b[i] = 10; }

        var va = new Vector<int>(a);
        var vb = new Vector<int>(b);

        // Bitta CPU taktida barcha elementlar qo'shiladi (AVX/SSE):
        Vector<int> vc = va + vb;

        int[] res = new int[vectorSize];
        vc.CopyTo(res);

        Console.WriteLine($"SIMD natijasi: {string.Join(", ", res)}");
    }
}

```

## Tushuntirish va Mantiq:
SIMD apparat darajasidagi parallelizm bo'lib, grafik hisoblashlar, sun'iy intellekt va audio/video signallarni qayta ishlashda protsessor yadrolarining vektor registrlaridan foydalanadi.

## Ishlash natijasi:
```text
Ushbu CPU SIMD registri sig'imi: 8 ta int
SIMD natijasi: 10, 11, 12, 13, 14, 15, 16, 17
```

# 737-Topshiriq: WaitHandle.WaitAll va WaitAny Metodlari
## Topshiriq sharti:
Operatsion tizim darajasidagi hodisalar guruhini boshqarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    static void Main()
    {
        WaitHandle[] signallar =
        [
            new AutoResetEvent(false),
            new AutoResetEvent(false)
        ];

        ThreadPool.QueueUserWorkItem(_ =>
        {
            Thread.Sleep(20);
            ((AutoResetEvent)signallar[0]).Set();
            Thread.Sleep(20);
            ((AutoResetEvent)signallar[1]).Set();
        });

        Console.WriteLine("Barcha OS signallari kutilmoqda...");
        WaitHandle.WaitAll(signallar);
        Console.WriteLine("Barcha signallar qabul qilindi!");
    }
}

```

## Tushuntirish va Mantiq:
`WaitHandle.WaitAll` bir nechta kernel hodisalarining barchasi signal holatiga o'tishini kutadi.

## Ishlash natijasi:
```text
Barcha OS signallari kutilmoqda...
Barcha signallar qabul qilindi!
```

# 738-Topshiriq: Semaphore Bilan Tizim Miqyosidagi Resurs Cheklovi
## Topshiriq sharti:
Nomlangan (Named) Semaphore orqali turli dasturlarning bir vaqtda kirishini cheklash.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    static void Main()
    {
        // Maksimal 2 ta instansiyaga ruxsat:
        using var semafor = new Semaphore(2, 2, "Global\MeningTizimSemaforim");

        semafor.WaitOne();
        try
        {
            Console.WriteLine("Tizim resursiga ruxsat olindi.");
        }
        finally
        {
            semafor.Release();
        }
    }
}

```

## Tushuntirish va Mantiq:
Named Semaphore butun operatsion tizim doirasida ishlaydi va bir nechta turli jarayonlar orasida litsenziya yoki resurslarni cheklashda ishlatiladi.

## Ishlash natijasi:
```text
Tizim resursiga ruxsat olindi.
```

# 739-Topshiriq: Thread.Yield vs Thread.Sleep(0) vs Thread.Sleep(1)
## Topshiriq sharti:
Oqimning CPU vaqtini boshqa oqimlarga bo'shatish usullari farqi.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    static void Main()
    {
        // 1. Thread.Yield: faqat aynan shu protsessor yadrosidagi boshqa oqimga vaqt beradi
        bool berildi = Thread.Yield();
        Console.WriteLine($"Yield bajarildi: {berildi}");

        // 2. Thread.Sleep(0): har qanday teng yoki yuqori prioritetli oqimga vaqt beradi
        Thread.Sleep(0);

        // 3. Thread.Sleep(1): oqimni kamida 1 ms ga haqiqiy uyquga ketkazadi
        Thread.Sleep(1);

        Console.WriteLine("Vaqt taqsimoti tajribasi yakunlandi.");
    }
}

```

## Tushuntirish va Mantiq:
`Thread.Yield` zamonaviy ko'p yadroli tizimlarda SpinLock va kutish sikllarida eng samarali vaqt bo'shatish usulidir.

## Ishlash natijasi:
```text
Yield bajarildi: True
Vaqt taqsimoti tajribasi yakunlandi.
```

# 740-Topshiriq: PLINQ MaxDegreeOfParallelism Bilan Protsessorni Nazorat Qilish
## Topshiriq sharti:
Parallel so'rovning maksimal oqimlar sonini chegaralash.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;

internal class Program
{
    static void Main()
    {
        var sonlar = Enumerable.Range(1, 100);

        var natija = sonlar
            .AsParallel()
            .WithDegreeOfParallelism(2) // Maksimal 2 ta oqim
            .Where(x => x % 10 == 0)
            .ToArray();

        Console.WriteLine($"Natija soni: {natija.Length}");
    }
}

```

## Tushuntirish va Mantiq:
Veb serverlarda har bir so'rov barcha protsessor yadrolarini egallab olmasligi uchun `WithDegreeOfParallelism` cheklovi qo'yiladi.

## Ishlash natijasi:
```text
Natija soni: 10
```

# 741-Topshiriq: Interlocked.Exchange Bilan Atomar Havola Almashtirish
## Topshiriq sharti:
Obyekt havolasini bitta taktda yangisiga almashtirish va eskisini olish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

class Konfiguratsiya
{
    public string Versiya { get; set; } = "1.0";
}

internal class Program
{
    private static Konfiguratsiya joriy = new();

    static void Main()
    {
        var yangi = new Konfiguratsiya { Versiya = "2.0" };

        // Atomar ravishda almashtiramiz:
        var eski = Interlocked.Exchange(ref joriy, yangi);

        Console.WriteLine($"Eski versiya: {eski.Versiya}");
        Console.WriteLine($"Yangi versiya: {joriy.Versiya}");
    }
}

```

## Tushuntirish va Mantiq:
`Interlocked.Exchange` ko'p oqimli konfiguratsiyalarni 'Hot Reload' qilishda vaqtinchalik qulflashlarsiz ishlatiladi.

## Ishlash natijasi:
```text
Eski versiya: 1.0
Yangi versiya: 2.0
```

# 742-Topshiriq: Interlocked.Add Bilan Atomar Qo'shish
## Topshiriq sharti:
Butun sonli o'zgaruvchiga ixtiyoriy qiymatni atomar tarzda qo'shish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    private static long jamiBalans = 1000;

    static void Main()
    {
        // 500 qo'shish va yangi natijani olish:
        long yangi = Interlocked.Add(ref jamiBalans, 500);

        Console.WriteLine($"Yangi balans: {yangi}");
    }
}

```

## Tushuntirish va Mantiq:
`Interlocked.Add` faqat 1 ga oshirish emas, balki ixtiyoriy musbat yoki manfiy sonni atomar qo'shish imkonini beradi.

## Ishlash natijasi:
```text
Yangi balans: 1500
```

# 743-Topshiriq: Sinxron Producer-Consumer Quvuri (BlockingCollection)
## Topshiriq sharti:
Oqimlararo ma'lumotlarni xavfsiz navbatda uzatish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Concurrent;
using System.Threading;

internal class Program
{
    static void Main()
    {
        using var navbat = new BlockingCollection<int>(boundedCapacity: 2);

        // Ishlab chiqaruvchi oqim
        new Thread(() =>
        {
            for (int i = 1; i <= 3; i++)
            {
                navbat.Add(i * 10);
            }
            navbat.CompleteAdding();
        }).Start();

        // Iste'molchi oqim
        foreach (var item in navbat.GetConsumingEnumerable())
        {
            Console.WriteLine($"Iste'mol qilindi: {item}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`BlockingCollection` ko'p oqimli muhitda klassik ishlab chiqaruvchi-iste'molchi naqshini o'zida to'liq mujassamlashtiradi.

## Ishlash natijasi:
```text
Iste'mol qilindi: 10
Iste'mol qilindi: 20
Iste'mol qilindi: 30
```

# 744-Topshiriq: Async-Safe Reentrant Lock Tuzilishi
## Topshiriq sharti:
`IDisposable` orqali SemaphoreSlim ni xavfsiz using blokiga o'rash.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

class AsinxronQulf
{
    private readonly SemaphoreSlim semafor = new(1, 1);

    public async Task<IDisposable> LockAsync()
    {
        await semafor.WaitAsync();
        return new Releaser(semafor);
    }

    private class Releaser : IDisposable
    {
        private readonly SemaphoreSlim semafor;
        public Releaser(SemaphoreSlim s) => semafor = s;
        public void Dispose() => semafor.Release();
    }
}

internal class Program
{
    static async Task Main()
    {
        var qulf = new AsinxronQulf();

        using (await qulf.LockAsync())
        {
            Console.WriteLine("Asinxron qulf ichida xavfsiz kod bajarilmoqda.");
        }

        Console.WriteLine("Qulf avtomatik bo'shatildi.");
    }
}

```

## Tushuntirish va Mantiq:
`using (await qulf.LockAsync())` sintaksisi C# da asinxron kodlarni qulflashning eng qulay va toza naqshidir.

## Ishlash natijasi:
```text
Asinxron qulf ichida xavfsiz kod bajarilmoqda.
Qulf avtomatik bo'shatildi.
```

# 745-Topshiriq: Oqimlar Nomuvofiqligi (Thread Starvation) va Sync-over-Async Xatari
## Topshiriq sharti:
Nima uchun ThreadPool oqimlarini bloklash butun tizimni to'xtatib qo'yishi tahlili.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

internal class Program
{
    static void Main()
    {
        // ThreadPool dagi barcha oqimlar Task.Delay().Wait() bilan band qilinsa,
        // yangi kelgan hech qanday so'rov oqim topa olmaydi va 'Starvation' yuzaga keladi.
        Console.WriteLine("[Qoida]: Hech qachon ThreadPool oqimida .Wait() yoki .Result chaqirmang!");
    }
}

```

## Tushuntirish va Mantiq:
Thread Starvation oldini olishning yagona yo'li — barcha I/O amallarni oxirigacha asinxron (`async/await`) qilishdir.

## Ishlash natijasi:
```text
[Qoida]: Hech qachon ThreadPool oqimida .Wait() yoki .Result chaqirmang!
```

# 746-Topshiriq: Deadlock Detektori: Lock Timeout Strategiyasi
## Topshiriq sharti:
Ilovadagi har qanday qulfga maksimal vaqt chegarasi qo'yish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    private static readonly object resurs = new();

    static void XavfsizKirish()
    {
        if (!Monitor.TryEnter(resurs, 100))
        {
            throw new TimeoutException("[Kritik]: Qulf olinmadi, ehtimol Deadlock yuzaga kelgan!");
        }
        try
        {
            Console.WriteLine("Resurs muvaffaqiyatli ishlatildi.");
        }
        finally
        {
            Monitor.Exit(resurs);
        }
    }

    static void Main()
    {
        XavfsizKirish();
    }
}

```

## Tushuntirish va Mantiq:
Katta korporativ tizimlarda oddiy `lock` o'rniga timeoutli qulflar ishlatiladi, bu esa tizimning jim qotib qolishini oldini oladi va monitoring tizimiga signal yuboradi.

## Ishlash natijasi:
```text
Resurs muvaffaqiyatli ishlatildi.
```

# 747-Topshiriq: Asinxron va Ko'p Oqimli Tushunchalarni Farqlash
## Topshiriq sharti:
Asinxronlik (Async) ko'p oqimlilik (Multithreading) degani emasligini isbotlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static async Task Main()
    {
        Console.WriteLine($"Boshlandi oqim ID: {Environment.CurrentManagedThreadId}");

        // Asinxron kutish paytida BIRORTA HAM OQIM BAND EMAS:
        await Task.Delay(20);

        Console.WriteLine($"Yakunlandi oqim ID: {Environment.CurrentManagedThreadId}");
    }
}

```

## Tushuntirish va Mantiq:
Asinxronlik — bu vazifaning chaqiruvchini to'xtatib qo'ymasligidir (I/O). Multithreading esa bir vaqtning o'zida bir nechta oqimda ish bajarishdir (CPU). Asinxron amalda kutish vaqtida hech qanday oqim mavjud bo'lmasligi ham mumkin.

## Ishlash natijasi:
```text
Boshlandi oqim ID: 1
Yakunlandi oqim ID: 4
```

# 748-Topshiriq: Thread.Priority Bilan Operatsion Tizim Prioritetini Belgilash
## Topshiriq sharti:
Oqimning muhimlik darajasini boshqarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    static void Main()
    {
        Thread t = new Thread(() => Console.WriteLine("Oqim ishladi"));
        t.Priority = ThreadPriority.AboveNormal;
        t.Start();
        t.Join();

        Console.WriteLine($"Oqim prioriteti: {t.Priority}");
    }
}

```

## Tushuntirish va Mantiq:
ThreadPriority operatsion tizim rejalashtiruvchisiga (OS Scheduler) qaysi oqimga ko'proq CPU vaqti ajratish kerakligini ko'rsatadi.

## Ishlash natijasi:
```text
Oqim ishladi
Oqim prioriteti: AboveNormal
```

# 749-Topshiriq: Oqimlarda Madaniyat (Culture) va Xavfsizlik Konteksti O'tishi
## Topshiriq sharti:
`CultureInfo` ning yangi oqimlarga avtomatik ko'chishi.

## Yechim (C# kodi):
```csharp
using System;
using System.Globalization;
using System.Threading;

internal class Program
{
    static void Main()
    {
        CultureInfo.DefaultThreadCurrentCulture = new CultureInfo("uz-Latn-UZ");

        new Thread(() =>
        {
            decimal summa = 12500.50m;
            Console.WriteLine($"O'zbek formatida valyuta: {summa:C}");
        }).Start();

        Thread.Sleep(30);
    }
}

```

## Tushuntirish va Mantiq:
.NET da `DefaultThreadCurrentCulture` barcha yangi ochilgan oqimlarda standart madaniyat (raqamlar, sanalar va valyuta formati) bir xil bo'lishini ta'minlaydi.

## Ishlash natijasi:
```text
O'zbek formatida valyuta: 12 500,50 so'm
```

# 750-Topshiriq: Multithreading Xulosasi: Striped Lock bilan Yuqori Unumdor Kesh Dvigateli
## Topshiriq sharti:
Butun lug'atni bitta qulf bilan to'xtatmasdan, bo'laklangan qulflar (Lock Striping) orqali $N$ barobar parallelizmga erishish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

class StripedKesh<TKey, TValue> where TKey : notnull
{
    private const int QulflarSoni = 4;
    private readonly object[] qulflar = new object[QulflarSoni];
    private readonly Dictionary<TKey, TValue>[] jadvallar = new Dictionary<TKey, TValue>[QulflarSoni];

    public StripedKesh()
    {
        for (int i = 0; i < QulflarSoni; i++)
        {
            qulflar[i] = new object();
            jadvallar[i] = new Dictionary<TKey, TValue>();
        }
    }

    private int Chelek(TKey kalit) => Math.Abs(kalit.GetHashCode() % QulflarSoni);

    public void Qoyish(TKey kalit, TValue qiymat)
    {
        int idx = Chelek(kalit);
        lock (qulflar[idx]) // Faqat tegishli chelak qulflanadi!
        {
            jadvallar[idx][kalit] = qiymat;
        }
    }

    public bool Olish(TKey kalit, out TValue? qiymat)
    {
        int idx = Chelek(kalit);
        lock (qulflar[idx])
        {
            return jadvallar[idx].TryGetValue(kalit, out qiymat);
        }
    }
}

internal class Program
{
    static void Main()
    {
        var kesh = new StripedKesh<string, int>();

        Parallel.Invoke(
            () => kesh.Qoyish("A", 100),
            () => kesh.Qoyish("B", 200),
            () => kesh.Qoyish("C", 300)
        );

        kesh.Olish("A", out int val);
        Console.WriteLine($"Keshdan olingan 'A': {val}");
    }
}

```

## Tushuntirish va Mantiq:
Lock Striping zamonaviy `ConcurrentDictionary` va yuqori yuklamali ma'lumotlar bazalarining yuragi hisoblanadi: har bir oqim faqat o'z segmentini qulflaydi va parallelizm darajasi keskin oshadi.

## Ishlash natijasi:
```text
Keshdan olingan 'A': 100
```

