# 14-Mavzu: Asinxron Dasturlash (async / await) (651-700)

Ushbu bo'limda C# tilining zamonaviy asinxron imkoniyatlari: `Task` va `Task<T>`, `async`/`await` mexanizmi, kompilyatorning `IAsyncStateMachine` holat mashinasi, I/O-bound va CPU-bound farqlari, `SynchronizationContext` va `ConfigureAwait(false)`, bekor qilish mexanizmi (`CancellationTokenSource`, `CancellationToken`), `Task.WhenAll` va `Task.WhenAny`, `ValueTask` bilan nol xotira ajratish, `TaskCompletionSource`, `IAsyncDisposable` (`await using`), `PeriodicTimer` hamda asinxron qulflash (`SemaphoreSlim.WaitAsync`) bo'yicha 50 ta amaliy topshiriq jamlangan.

# 651-Topshiriq: Asinxron Dasturlash Asoslari: Task va Task<T>
## Topshiriq sharti:
Sinxron bloklanishsiz kelajakdagi natijani (`Task`) qaytaruvchi metod yozing.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static async Task<string> MalumotniYuklashAsync()
    {
        // Thread ni uxlatmasdan, asinxron taymer kutish:
        await Task.Delay(50);
        return "Serverdan olingan ma'lumot";
    }

    static async Task Main()
    {
        Console.WriteLine("So'rov yuborildi...");
        string natija = await MalumotniYuklashAsync();
        Console.WriteLine($"Natija: {natija}");
    }
}

```

## Tushuntirish va Mantiq:
`Task` va `Task<T>` kelajakda yakunlanadigan asinxron operatsiyaning holatini (Status, Result, Exception) ifodalaydi. `await` operatori oqimni to'xtatib qo'ymasdan boshqaruvni chaqiruvchiga qaytaradi.

## Ishlash natijasi:
```text
So'rov yuborildi...
Natija: Serverdan olingan ma'lumot
```

# 652-Topshiriq: Task.Delay vs Thread.Sleep: Bloklanmaslik Falsafasi
## Topshiriq sharti:
Asinxron kutish va sinxron oqimni to'xtatish o'rtasidagi farqni amalda ko'ring.

## Yechim (C# kodi):
```csharp
using System;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;

internal class Program
{
    static async Task AsinxronKutish()
    {
        // ThreadPool oqimini bo'shatadi, boshqa vazifalar bajarilishi mumkin:
        await Task.Delay(100);
    }

    static void SinxronKutish()
    {
        // Butun operatsion tizim oqimini qotirib qo'yadi (CPU resursi isrof bo'ladi):
        Thread.Sleep(100);
    }

    static async Task Main()
    {
        var sw = Stopwatch.StartNew();
        await AsinxronKutish();
        Console.WriteLine($"Asinxron kutish tugadi: {sw.ElapsedMilliseconds} ms");

        sw.Restart();
        SinxronKutish();
        Console.WriteLine($"Sinxron kutish tugadi: {sw.ElapsedMilliseconds} ms");
    }
}

```

## Tushuntirish va Mantiq:
`Thread.Sleep` operatsion tizim oqimini zanjirlab qo'yadi. `Task.Delay` esa o'z oqimini ThreadPool ga qaytarib beradi va vaqt o'tgach CLR taymeri orqali bo'sh oqimni uyg'otadi.

## Ishlash natijasi:
```text
Asinxron kutish tugadi: 100 ms
Sinxron kutish tugadi: 100 ms
```

# 653-Topshiriq: I/O-Bound va CPU-Bound Operatsiyalar Farqi
## Topshiriq sharti:
`Task.Run` (CPU) va tabiiy asinxron I/O operatsiyalarini to'g'ri tanlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    // CPU-bound: Protsessorni qizdiradigan og'ir hisoblash (Task.Run kerak)
    static Task<long> OgirHisoblashAsync(int n)
    {
        return Task.Run(() =>
        {
            long yigindi = 0;
            for (int i = 0; i < n; i++) yigindi += i;
            return yigindi;
        });
    }

    // I/O-bound: Tarmoq, disk yoki DB so'rovi (Task.Run KERAK EMAS!)
    static async Task<string> TarmoqSoroviAsync()
    {
        await Task.Delay(50); // Disk/tarmoq drayveri kontrolida
        return "200 OK";
    }

    static async Task Main()
    {
        long hisob = await OgirHisoblashAsync(100000);
        string status = await TarmoqSoroviAsync();

        Console.WriteLine($"Hisob: {hisob}, Status: {status}");
    }
}

```

## Tushuntirish va Mantiq:
I/O operatsiyalarda protsessor kutib turmaydi, shuning uchun ularni `Task.Run` ichiga o'rash zararli bo'lib, ThreadPool oqimlarini behuda band qiladi.

## Ishlash natijasi:
```text
Hisob: 4999950000, Status: 200 OK
```

# 654-Topshiriq: Kompilyatorning Holat Mashinasi: IAsyncStateMachine
## Topshiriq sharti:
`async/await` kompilyatsiya qilinganda qanday yashirin `struct` yaratilishini tahlil qiling.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static async Task BajarAsync()
    {
        Console.WriteLine("1-qadam (boshlandi)");
        await Task.Yield(); // Majburiy asinxron uzilish
        Console.WriteLine("2-qadam (davom etdi)");
    }

    static async Task Main()
    {
        await BajarAsync();
        Console.WriteLine("Tugatildi");
    }
}

```

## Tushuntirish va Mantiq:
Kompilyator `async` metodni `IAsyncStateMachine` interfeysini amalga oshiruvchi struktura shakliga o'tkazadi. `await` uchraganda metod joriy holatini saqlab chiqadi va davomini qayta tiklaydi (continuation).

## Ishlash natijasi:
```text
1-qadam (boshlandi)
2-qadam (davom etdi)
Tugatildi
```

# 655-Topshiriq: ConfigureAwait(false) va Kontekstni Yo'qotish (Context Switching)
## Topshiriq sharti:
Kutubxona kodlarida UI oqimiga qaytish xarajatlarini yo'qotish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

internal class Program
{
    static async Task KutubxonaMetodiAsync()
    {
        Console.WriteLine($"Boshlang'ich oqim ID: {Environment.CurrentManagedThreadId}");

        // ConfigureAwait(false) chaqirilganda, davomi istalgan bo'sh oqimda davom etaveradi:
        await Task.Delay(50).ConfigureAwait(false);

        Console.WriteLine($"Kutishdan keyingi oqim ID: {Environment.CurrentManagedThreadId}");
    }

    static async Task Main()
    {
        await KutubxonaMetodiAsync();
    }
}

```

## Tushuntirish va Mantiq:
`ConfigureAwait(false)` sinxronizatsiya kontekstini (SynchronizationContext) saqlab qolmaslikni aytadi. Bu kutubxonalarda (class libraries) deadlocklarning oldini oladi va unumdorlikni oshiradi.

## Ishlash natijasi:
```text
Boshlang'ich oqim ID: 1
Kutishdan keyingi oqim ID: 4
```

# 656-Topshiriq: CancellationToken va CancellationTokenSource Asoslari
## Topshiriq sharti:
Asinxron operatsiyaga to'xtatish signali (cancellation request) yuborish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

internal class Program
{
    static async Task SiklAsync(CancellationToken ct)
    {
        for (int i = 1; i <= 5; i++)
        {
            ct.ThrowIfCancellationRequested(); // Agar bekor qilingan bo'lsa xato otadi
            Console.WriteLine($"Ishlamoqda: {i}");
            await Task.Delay(50, ct); // Task.Delay ga ham token beriladi
        }
    }

    static async Task Main()
    {
        using var cts = new CancellationTokenSource();

        // 120 ms dan so'ng avtomatik bekor qilish:
        cts.CancelAfter(120);

        try
        {
            await SiklAsync(cts.Token);
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine("[Ogohlantirish]: Operatsiya foydalanuvchi yoki taymer tomonidan to'xtatildi!");
        }
    }
}

```

## Tushuntirish va Mantiq:
`CancellationToken` kooperativ (kelishilgan) bekor qilish modelidir: oqim zo'ravonlik bilan o'ldirilmaydi, balki token holatini tekshirib toza chiqib ketadi.

## Ishlash natijasi:
```text
Ishlamoqda: 1
Ishlamoqda: 2
[Ogohlantirish]: Operatsiya foydalanuvchi yoki taymer tomonidan to'xtatildi!
```

# 657-Topshiriq: CancellationToken.Register bilan Tozalash Callbackini Bog'lash
## Topshiriq sharti:
Bekor qilish signali kelganda drayver yoki soketni darhol yopish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;

internal class Program
{
    static void Main()
    {
        var cts = new CancellationTokenSource();

        // Token bekor qilinganda ishga tushadigan qutqaruv callbacki:
        cts.Token.Register(() =>
        {
            Console.WriteLine("[Callback]: Bekor qilish signali ushlandi, resurslar yopilmoqda!");
        });

        Console.WriteLine("Operatsiya boshlandi...");
        cts.Cancel(); // Signal berildi
    }
}

```

## Tushuntirish va Mantiq:
`ct.Register(callback)` token bekor qilingan daqiqada sinxron yoki asinxron bajariladigan delegatni ro'yxatga oladi.

## Ishlash natijasi:
```text
Operatsiya boshlandi...
[Callback]: Bekor qilish signali ushlandi, resurslar yopilmoqda!
```

# 658-Topshiriq: Bir Nechta CancellationToken larni Birlashtirish (Linked Token)
## Topshiriq sharti:
Global timeout va foydalanuvchi bekor qilish tugmasini bitta tokenga bog'lash.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

internal class Program
{
    static async Task Main()
    {
        using var foydalanuvchiCts = new CancellationTokenSource();
        using var vaqtCts = new CancellationTokenSource(TimeSpan.FromMilliseconds(50));

        // Ikkala tokenni birlashtiramiz (qaysi biri birinchi bekor bo'lsa ham ishlaydi):
        using var birlashganCts = CancellationTokenSource.CreateLinkedTokenSource(foydalanuvchiCts.Token, vaqtCts.Token);

        try
        {
            await Task.Delay(200, birlashganCts.Token);
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine("Birlashgan token orqali operatsiya to'xtatildi!");
        }
    }
}

```

## Tushuntirish va Mantiq:
`CreateLinkedTokenSource` bir nechta mustaqil bekor qilish manbalarini bitta boshqaruv nuqtasiga yig'adi.

## Ishlash natijasi:
```text
Birlashgan token orqali operatsiya to'xtatildi!
```

# 659-Topshiriq: Task.WhenAll Bilan Bir Nechta Vazifalarni Parallel Bajarish
## Topshiriq sharti:
Bir vaqtda bir nechta serverdan ma'lumotlarni parallel yuklash.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static async Task<string> YuklashAsync(string manzil, int kechikish)
    {
        await Task.Delay(kechikish);
        return $"{manzil} ma'lumotlari";
    }

    static async Task Main()
    {
        Task<string> v1 = YuklashAsync("Server A", 80);
        Task<string> v2 = YuklashAsync("Server B", 40);
        Task<string> v3 = YuklashAsync("Server C", 60);

        // Barchasini parallel kutamiz:
        string[] natijalar = await Task.WhenAll(v1, v2, v3);

        foreach (var n in natijalar)
        {
            Console.WriteLine($"Qabul qilindi: {n}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`Task.WhenAll` barcha tasklar to'liq tugashini parallel kutadi va ularning natijalarini massiv ko'rinishida qaytaradi. Umumiy vaqt eng sekin ishlagan task vaqtiga teng bo'ladi.

## Ishlash natijasi:
```text
Qabul qilindi: Server A ma'lumotlari
Qabul qilindi: Server B ma'lumotlari
Qabul qilindi: Server C ma'lumotlari
```

# 660-Topshiriq: Task.WhenAny Bilan Eng Tezkor Natijani Tanlash (Race Pattern)
## Topshiriq sharti:
Bir nechta replikalardan eng birinchi javob berganini qabul qilish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static async Task<string> ServerdanOlish(string server, int ms)
    {
        await Task.Delay(ms);
        return $"Javob keldi: {server}";
    }

    static async Task Main()
    {
        Task<string> t1 = ServerdanOlish("Server 1 (sekin)", 100);
        Task<string> t2 = ServerdanOlish("Server 2 (tezkor)", 30);

        // Eng birinchi tayyor bo'lgan taskni olamiz:
        Task<string> birinchi = await Task.WhenAny(t1, t2);

        string natija = await birinchi;
        Console.WriteLine($"G'olib: {natija}");
    }
}

```

## Tushuntirish va Mantiq:
`Task.WhenAny` uzatilgan tasklardan eng birinchisi yakunlanishi bilanoq qaytadi va qolganlarini kutib o'tirmaydi.

## Ishlash natijasi:
```text
G'olib: Javob keldi: Server 2 (tezkor)
```

# 661-Topshiriq: Asinxron Metodlarda Xatolarni Tutish (Exception Handling)
## Topshiriq sharti:
Bir nechta parallel tasklar xato berganda barcha istisnolarni ochib o'qish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static async Task XatoMetod(string nom)
    {
        await Task.Delay(20);
        throw new InvalidOperationException($"Xatolik: {nom}");
    }

    static async Task Main()
    {
        Task t1 = XatoMetod("Vazifa 1");
        Task t2 = XatoMetod("Vazifa 2");

        Task barchasi = Task.WhenAll(t1, t2);

        try
        {
            await barchasi;
        }
        catch
        {
            // 'await' faqat birinchi xatoni otadi, lekin barcha xatolar Task.Exception ichida bo'ladi:
            foreach (var ex in barchasi.Exception!.InnerExceptions)
            {
                Console.WriteLine($"Ushlandi: {ex.Message}");
            }
        }
    }
}

```

## Tushuntirish va Mantiq:
Oddiy `await Task.WhenAll` faqat birinchi uchragan xatoni otadi. Barcha xatolarni ko'rish uchun `Task.Exception.InnerExceptions` to'plamini aylanib chiqish kerak.

## Ishlash natijasi:
```text
Ushlandi: Xatolik: Vazifa 1
Ushlandi: Xatolik: Vazifa 2
```

# 662-Topshiriq: Nima uchun `async void` Dan Qochish Kerak?
## Topshiriq sharti:
`async Task` va `async void` o'rtasidagi halokatli farq.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static async Task XavfsizAsync()
    {
        await Task.Delay(10);
        Console.WriteLine("Xavfsiz asinxron metod bajarildi.");
    }

    // async void faqatgina UI hodisalarida (Event Handlers) ruxsat etiladi!
    // Chunki uni await qilib bo'lmaydi va undagi istisno butun jarayonni qulatadi.
    static async Task Main()
    {
        await XavfsizAsync();
        Console.WriteLine("Tizim barqaror ishlamoqda.");
    }
}

```

## Tushuntirish va Mantiq:
`async void` metodlar `Task` qaytarmagani sababli chaqiruvchi ularni `await` qila olmaydi va ichida chiqqan istisnolarni `try/catch` bilan tutib bo'lmaydi.

## Ishlash natijasi:
```text
Xavfsiz asinxron metod bajarildi.
Tizim barqaror ishlamoqda.
```

# 663-Topshiriq: ValueTask va ValueTask<T> Bilan Nol Heap Xotira Sarfi
## Topshiriq sharti:
Natijasi darhol tayyor bo'lgan hollarda `Task` obyekti yaratmaslik.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    private static int keshланганQiymat = 42;

    static ValueTask<int> OlishAsync(bool keshdanmi)
    {
        if (keshdanmi)
        {
            // Natija sinxron tayyor bo'lsa, xotirada hech qanday Task obyekti ajratilmaydi (struct):
            return new ValueTask<int>(keshланганQiymat);
        }

        return new ValueTask<int>(OgirlikBilanOlishAsync());
    }

    static async Task<int> OgirlikBilanOlishAsync()
    {
        await Task.Delay(20);
        return 100;
    }

    static async Task Main()
    {
        int v1 = await OlishAsync(true);
        int v2 = await OlishAsync(false);

        Console.WriteLine($"Keshdan: {v1}, Diskdan: {v2}");
    }
}

```

## Tushuntirish va Mantiq:
`ValueTask<T>` qiymat turi (struct) bo'lib, agar ma'lumot sinxron tayyor bo'lsa Heap xotirada `Task` obyekti yaratmaydi va GC bosimini keskin kamaytiradi.

## Ishlash natijasi:
```text
Keshdan: 42, Diskdan: 100
```

# 664-Topshiriq: ValueTask ni Faqat Bir Marta `await` Qilish Qoidasi
## Topshiriq sharti:
Nima uchun ValueTask ni ikki marta await qilish yoki `.Result` bilan aralashtirish taqiqlanadi?

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static ValueTask<string> MalumotBer() => new("Tezkor");

    static async Task Main()
    {
        ValueTask<string> vt = MalumotBer();

        // 1-await: To'g'ri va xavfsiz
        string s = await vt;
        Console.WriteLine($"1-chaqiruv: {s}");

        // DIQQAT: ValueTask ichidagi ob'ekt hovuzga (IValueTaskSource) qaytarilishi mumkin,
        // shuning uchun uni ikkinchi marta await qilish taqiqlanadi!
        // Agar bir necha marta kerak bo'lsa: vt.AsTask() ishlatiladi.
    }
}

```

## Tushuntirish va Mantiq:
ValueTask qayta ishlatiluvchi (pooled) `IValueTaskSource` obyektlariga tayanishi mumkin. Shuning uchun uni faqat bir marta `await` qilish shart.

## Ishlash natijasi:
```text
1-chaqiruv: Tezkor
```

# 665-Topshiriq: TaskCompletionSource<T> bilan Callbacklarni Taskga Aylantirish
## Topshiriq sharti:
Eski voqealarga asoslangan API larni zamonaviy `await` qilinadigan Task ga aylantirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;
using System.Timers;

internal class Program
{
    static Task<string> TaymerKutishAsync(double ms)
    {
        var tcs = new TaskCompletionSource<string>();
        var timer = new System.Timers.Timer(ms) { AutoReset = false };

        timer.Elapsed += (s, e) =>
        {
            timer.Dispose();
            tcs.SetResult("Taymer signali muvaffaqiyatli yetib keldi!");
        };

        timer.Start();
        return tcs.Task;
    }

    static async Task Main()
    {
        Console.WriteLine("Taymer ishga tushirildi...");
        string xabar = await TaymerKutishAsync(50);
        Console.WriteLine(xabar);
    }
}

```

## Tushuntirish va Mantiq:
`TaskCompletionSource<T>` asinxron dasturlashning 'ko'prigi' hisoblanib, istalgan eski event yoki callback mexanizmini toza `Task<T>` ga o'rab beradi.

## Ishlash natijasi:
```text
Taymer ishga tushirildi...
Taymer signali muvaffaqiyatli yetib keldi!
```

# 666-Topshiriq: IAsyncDisposable va `await using` Bayonoti
## Topshiriq sharti:
Tarmoq ulanishlari va oqimlarni asinxron tozalash.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

class AsinxronUlanish : IAsyncDisposable
{
    public void SorovYubor() => Console.WriteLine("So'rov yuborildi.");

    public async ValueTask DisposeAsync()
    {
        Console.WriteLine("Asinxron ulanish yopilmoqda...");
        await Task.Delay(30); // Tarmoqqa uzilish paketini yuborish
        Console.WriteLine("Ulanish xavfsiz yakunlandi.");
    }
}

internal class Program
{
    static async Task Main()
    {
        await using (var conn = new AsinxronUlanish())
        {
            conn.SorovYubor();
        } // DisposeAsync avtomatik ravishda await qilinadi!

        Console.WriteLine("Dastur davom etmoqda.");
    }
}

```

## Tushuntirish va Mantiq:
`IAsyncDisposable` va `await using` resurslarni oqimni qotirmasdan asinxron tarzda tozalash imkonini beradi.

## Ishlash natijasi:
```text
So'rov yuborildi.
Asinxron ulanish yopilmoqda...
Ulanish xavfsiz yakunlandi.
Dastur davom etmoqda.
```

# 667-Topshiriq: .NET 6+ PeriodicTimer Bilan Toza Siklik Asinxron Jarayon
## Topshiriq sharti:
`System.Threading.Timer` o'rniga xotirani to'ldirmaydigan asinxron taymer.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

internal class Program
{
    static async Task Main()
    {
        using var taymer = new PeriodicTimer(TimeSpan.FromMilliseconds(40));
        int hisob = 0;

        Console.WriteLine("Davriy jarayon boshlandi:");
        while (await taymer.WaitForNextTickAsync())
        {
            Console.WriteLine($"Takt: {++hisob}");
            if (hisob == 3) break;
        }
    }
}

```

## Tushuntirish va Mantiq:
`PeriodicTimer` bitta vaqtda bir nechta chaqiruvlarning bir-biriga urilib ketishi (tick overlapping) xavfini yo'qotadi va `while (await ...)` bilan juda qulay yoziladi.

## Ishlash natijasi:
```text
Davriy jarayon boshlandi:
Takt: 1
Takt: 2
Takt: 3
```

# 668-Topshiriq: Asinxron Deadlock Xavfi: `.Result` va `.Wait()` Tuzog'i
## Topshiriq sharti:
Nima uchun asinxron metodni sinxron bloklab chaqirish butun tizimni muzlatadi?

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static async Task<int> HisoblaAsync()
    {
        await Task.Delay(20);
        return 100;
    }

    static void Main()
    {
        // Katta xato: UI yoki ASP.NET kontekstida HisoblaAsync().Result chaqirilsa,
        // SynchronizationContext asosiy oqimni kutadi, asosiy oqim esa Taskni kutib Deadlock hosil qiladi!
        // To'g'ri yondashuv: butun zanjirni 'async Task' va 'await' qilish.

        int natija = Task.Run(() => HisoblaAsync()).GetAwaiter().GetResult();
        Console.WriteLine($"Xavfsiz hisob: {natija}");
    }
}

```

## Tushuntirish va Mantiq:
Asinxron dunyoda 'Sync over Async' (asinxron kod ustidan `.Result` yoki `.Wait()` chaqirish) qat'iyan man etiladi. Bu oqimlar ochligi (Thread Starvation) va Deadlockka sabab bo'ladi.

## Ishlash natijasi:
```text
Xavfsiz hisob: 100
```

# 669-Topshiriq: SemaphoreSlim.WaitAsync Bilan Asinxron Qulflash (Async Lock)
## Topshiriq sharti:
`lock` bayonoti asinxron bloklarda ishlamasligi va uning o'rniga `SemaphoreSlim` ishlatish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

internal class Program
{
    private static readonly SemaphoreSlim semafor = new(1, 1);
    private static int umumiyHisob = 0;

    static async Task OshirishAsync()
    {
        // C# da 'lock' ichida 'await' yozish taqiqlangan!
        // Shuning uchun SemaphoreSlim.WaitAsync ishlatiladi:
        await semafor.WaitAsync();
        try
        {
            int temp = umumiyHisob;
            await Task.Delay(10);
            umumiyHisob = temp + 1;
        }
        finally
        {
            semafor.Release();
        }
    }

    static async Task Main()
    {
        Task t1 = OshirishAsync();
        Task t2 = OshirishAsync();

        await Task.WhenAll(t1, t2);
        Console.WriteLine($"Umumiy hisob: {umumiyHisob}");
    }
}

```

## Tushuntirish va Mantiq:
C# dagi `lock` bayonoti bitta oqimga bog'langan (Thread-Affinity). Asinxron amalda esa `await` dan keyin boshqa oqim davom etishi mumkinligi sababli `SemaphoreSlim.WaitAsync()` tanlanadi.

## Ishlash natijasi:
```text
Umumiy hisob: 2
```

# 670-Topshiriq: Asinxron Resurs Hovuzi (Async Object Pool) Bilan Cheklash
## Topshiriq sharti:
Bir vaqtning o'zida maksimal 2 ta asinxron ulanishga ruxsat beruvchi semafor.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

internal class Program
{
    private static readonly SemaphoreSlim cheklovchi = new(2); // Maksimal 2 ta parallel kirish

    static async Task Yuklash(int id)
    {
        await cheklovchi.WaitAsync();
        try
        {
            Console.WriteLine($"Vazifa #{id} ruxsat oldi.");
            await Task.Delay(40);
            Console.WriteLine($"Vazifa #{id} tugadi.");
        }
        finally
        {
            cheklovchi.Release();
        }
    }

    static async Task Main()
    {
        Task[] vazifalar = [Yuklash(1), Yuklash(2), Yuklash(3)];
        await Task.WhenAll(vazifalar);
    }
}

```

## Tushuntirish va Mantiq:
SemaphoreSlim orqali tashqi sekin API yoki ma'lumotlar bazasiga bir vaqtning o'zida keladigan so'rovlar sonini xavfsiz cheklash (Throttling) mumkin.

## Ishlash natijasi:
```text
Vazifa #1 ruxsat oldi.
Vazifa #2 ruxsat oldi.
Vazifa #1 tugadi.
Vazifa #3 ruxsat oldi.
Vazifa #2 tugadi.
Vazifa #3 tugadi.
```

# 671-Topshiriq: Task.Yield Bilan Majburiy Asinxron Kontekstga O'tish
## Topshiriq sharti:
Sinxron ishlayotgan og'ir metodni majburan ThreadPool ga chekintirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static async Task IshniBoshlash()
    {
        Console.WriteLine("Chaqiruvchi oqimda boshlandi");

        // UI yoki asosiy oqim qotib qolmasligi uchun darhol boshqaruvni qaytaradi:
        await Task.Yield();

        Console.WriteLine("ThreadPool da davom etmoqda");
    }

    static async Task Main()
    {
        await IshniBoshlash();
    }
}

```

## Tushuntirish va Mantiq:
`Task.Yield` operatsiyani zudlik bilan navbatga qo'yadi va chaqiruvchi oqimga zudlik bilan boshqaruvni qaytaradi.

## Ishlash natijasi:
```text
Chaqiruvchi oqimda boshlandi
ThreadPool da davom etmoqda
```

# 672-Topshiriq: Asinxron Lazy Initsializatsiya (AsyncLazy Pattern)
## Topshiriq sharti:
Resursni faqat birinchi talab qilinganda asinxron yuklab keshlovchi tuzilma.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

class AsinxronKesh<T>
{
    private readonly Lazy<Task<T>> ichkiLazy;

    public AsinxronKesh(Func<Task<T>> yuklovchi)
    {
        ichkiLazy = new Lazy<Task<T>>(() => Task.Run(yuklovchi));
    }

    public Task<T> QiymatAsync => ichkiLazy.Value;
}

internal class Program
{
    static async Task Main()
    {
        var kesh = new AsinxronKesh<string>(async () =>
        {
            Console.WriteLine("[Og'ir ish]: Ma'lumotlar yuklanmoqda...");
            await Task.Delay(50);
            return "Konfiguratsiya tayyor";
        });

        Console.WriteLine("Kesh e'lon qilindi (hali hech narsa yuklanmadi).");
        string q1 = await kesh.QiymatAsync;
        string q2 = await kesh.QiymatAsync; // Ikkinchi marta darhol qaytadi

        Console.WriteLine($"1: {q1}");
        Console.WriteLine($"2: {q2}");
    }
}

```

## Tushuntirish va Mantiq:
`AsyncLazy` naqshi ko'p oqimli muhitda bir vaqtning o'zida bir nechta yuklash amallari boshlanib ketishini oldini oladi.

## Ishlash natijasi:
```text
Kesh e'lon qilindi (hali hech narsa yuklanmadi).
[Og'ir ish]: Ma'lumotlar yuklanmoqda...
1: Konfiguratsiya tayyor
2: Konfiguratsiya tayyor
```

# 673-Topshiriq: Task.FromResult, FromCanceled va FromException
## Topshiriq sharti:
Tayyor holatdagi Task obyektlarini yaratishning optimal usullari.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

internal class Program
{
    static Task<int> TayyorNatija() => Task.FromResult(200);
    static Task XatolikNatijasi() => Task.FromException(new TimeoutException("Vaqt tugadi"));

    static async Task Main()
    {
        int kod = await TayyorNatija();
        Console.WriteLine($"Tayyor status: {kod}");

        try
        {
            await XatolikNatijasi();
        }
        catch (TimeoutException ex)
        {
            Console.WriteLine($"Kutilgan xato: {ex.Message}");
        }
    }
}

```

## Tushuntirish va Mantiq:
Sinxron shoxchalarda `async/await` qo'shmasdan to'g'ridan-to'g'ri `Task.FromResult` yoki `Task.CompletedTask` qaytarish ancha samaralidir.

## Ishlash natijasi:
```text
Tayyor status: 200
Kutilgan xato: Vaqt tugadi
```

# 674-Topshiriq: Asinxron Rekursiya va Call Stack Xavfsizligi
## Topshiriq sharti:
Asinxron metodlarda rekursiv chaqiruvlarni xavfsiz boshqarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static async Task<int> AsinxronFaktorial(int n)
    {
        if (n <= 1) return 1;
        await Task.Yield(); // Chuqur rekursiyada stack to'lib ketishidan saqlaydi
        return n * await AsinxronFaktorial(n - 1);
    }

    static async Task Main()
    {
        int res = await AsinxronFaktorial(5);
        Console.WriteLine($"5! = {res}");
    }
}

```

## Tushuntirish va Mantiq:
Asinxron metodlarda har bir `await` dan keyingi qism yangi oqimda davom etishi mumkinligi sababli, rekursiya stack xotirani oddiy sinxron metod kabi to'ldirib yubormaydi.

## Ishlash natijasi:
```text
5! = 120
```

# 675-Topshiriq: Asinxron Metodlarda Bekor Qilishni Graceful Handle Qilish
## Topshiriq sharti:
Operatsiya to'xtatilganda qisman bajarilgan ishlarni toza holatga qaytarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

internal class Program
{
    static async Task FaylSaqlashAsync(CancellationToken ct)
    {
        try
        {
            Console.WriteLine("Fayl yozilmoqda...");
            await Task.Delay(100, ct);
            Console.WriteLine("Fayl to'liq yozildi.");
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine("[Tozalash]: Fayl yozish to'xtatildi, chala fayllar o'chirildi.");
            throw; // Yuqoriga xabar berish
        }
    }

    static async Task Main()
    {
        using var cts = new CancellationTokenSource(30);

        try
        {
            await FaylSaqlashAsync(cts.Token);
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine("Asosiy dastur: operatsiya bekor qilinganini tasdiqladi.");
        }
    }
}

```

## Tushuntirish va Mantiq:
Bekor qilish vaqtida chala qolgan fayllar, ochiq tranzaksiyalar yoki tarmoq ulanishlarini tozalash 'Graceful Degradation' tamoyilidir.

## Ishlash natijasi:
```text
Fayl yozilmoqda...
[Tozalash]: Fayl yozish to'xtatildi, chala fayllar o'chirildi.
Asosiy dastur: operatsiya bekor qilinganini tasdiqladi.
```

# 676-Topshiriq: .NET 6+ Task.WaitAsync(TimeSpan) Bilan Aniq Timeout Belgilash
## Topshiriq sharti:
Eski `Task.WhenAny(task, Task.Delay)` usulini almashtiruvchi zamonaviy timeout metodi.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static async Task SekinMetod()
    {
        await Task.Delay(200);
    }

    static async Task Main()
    {
        try
        {
            // .NET 6 da qo'shilgan WaitAsync metodi:
            await SekinMetod().WaitAsync(TimeSpan.FromMilliseconds(50));
            Console.WriteLine("Muvaffaqiyatli yakunlandi.");
        }
        catch (TimeoutException)
        {
            Console.WriteLine("[Timeout]: Operatsiya belgilangan 50 ms ichida ulgurmadi!");
        }
    }
}

```

## Tushuntirish va Mantiq:
Task.WaitAsync kutish vaqtini oson boshqarish imkonini beradi va vaqt oshib ketganda TimeoutException otadi.

## Ishlash natijasi:
```text
[Timeout]: Operatsiya belgilangan 50 ms ichida ulgurmadi!
```

# 677-Topshiriq: Parallel.ForEachAsync (.NET 6+) Bilan Asinxron To'plamni Qayta Ishlash
## Topshiriq sharti:
Bir vaqtning o'zida bir nechta asinxron operatsiyalarni parallel oqimda boshqarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static async Task Main()
    {
        string[] saytlar = ["sayt1.uz", "sayt2.uz", "sayt3.uz", "sayt4.uz"];

        // Maksimal 2 ta parallel so'rov bilan asinxron aylanib chiqish:
        await Parallel.ForEachAsync(saytlar, new ParallelOptions { MaxDegreeOfParallelism = 2 }, async (sayt, ct) =>
        {
            await Task.Delay(30, ct);
            Console.WriteLine($"Tekshirildi: {sayt}");
        });

        Console.WriteLine("Barcha saytlar muvaffaqiyatli tekshirildi.");
    }
}

```

## Tushuntirish va Mantiq:
`Parallel.ForEachAsync` .NET 6 da kiritilgan bo'lib, eski `Task.WhenAll(list.Select(...))` usuliga nisbatan xotirani ancha tejaydi va parallelizm sonini aniq cheklash imkonini beradi.

## Ishlash natijasi:
```text
Tekshirildi: sayt1.uz
Tekshirildi: sayt2.uz
Tekshirildi: sayt3.uz
Tekshirildi: sayt4.uz
Barcha saytlar muvaffaqiyatli tekshirildi.
```

# 678-Topshiriq: Asinxron Oqimlarda Bekor Qilish: [EnumeratorCancellation]
## Topshiriq sharti:
`IAsyncEnumerable<T>` oqimiga `CancellationToken` uzatish va uni to'g'ri bog'lash.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;

internal class Program
{
    static async IAsyncEnumerable<int> SonlarGeneratori([EnumeratorCancellation] CancellationToken ct = default)
    {
        for (int i = 1; i <= 10; i++)
        {
            ct.ThrowIfCancellationRequested();
            await Task.Delay(30, ct);
            yield return i;
        }
    }

    static async Task Main()
    {
        using var cts = new CancellationTokenSource(80);

        try
        {
            // WithCancellation orqali oqimga tokenni uzatamiz:
            await foreach (var s in SonlarGeneratori().WithCancellation(cts.Token))
            {
                Console.WriteLine($"Olingan son: {s}");
            }
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine("Asinxron oqim vaqt tugashi bilan to'xtatildi.");
        }
    }
}

```

## Tushuntirish va Mantiq:
`[EnumeratorCancellation]` atributi `WithCancellation(token)` orqali uzatilgan tokenni metod ichidagi parametrga avtomatik biriktiradi.

## Ishlash natijasi:
```text
Olingan son: 1
Olingan son: 2
Asinxron oqim vaqt tugashi bilan to'xtatildi.
```

# 679-Topshiriq: AsyncLocal<T> Bilan Asinxron Oqimlararo Kontekst Uzatish
## Topshiriq sharti:
Oqimlar almashsa ham qiymatni o'zida saqlab qoluvchi asinxron xotira.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    // Oqimlar almashganda ham ExecutionContext orqali o'tuvchi o'zgaruvchi:
    private static readonly AsyncLocal<string> So'rovIdentifikatori = new();

    static async Task BajaruvchiQadam()
    {
        await Task.Delay(30); // Oqim o'zgarishi mumkin
        Console.WriteLine($"Ichki qadamda ID: {So'rovIdentifikatori.Value}");
    }

    static async Task Main()
    {
        So'rovIdentifikatori.Value = "REQ-998877";

        Console.WriteLine($"Asosiy oqimda ID: {So'rovIdentifikatori.Value}");
        await BajaruvchiQadam();
    }
}

```

## Tushuntirish va Mantiq:
`AsyncLocal<T>` `ThreadLocal<T>` dan farqli o'laroq, `await` chaqirilgandan keyin boshqa ThreadPool oqimiga o'tsa ham qiymatini yo'qotmaydi. Bu Correlation ID va Tracing uchun asosiy vositadir.

## Ishlash natijasi:
```text
Asosiy oqimda ID: REQ-998877
Ichki qadamda ID: REQ-998877
```

# 680-Topshiriq: ExecutionContext Flow va ExecutionContext.SuppressFlow
## Topshiriq sharti:
Asinxron kontekst o'tishini vaqtincha to'xtatib unumdorlikni oshirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

internal class Program
{
    private static readonly AsyncLocal<string> Foydalanuvchi = new();

    static async Task Main()
    {
        Foydalanuvchi.Value = "Admin";

        // Kontekst oqishini to'xtatamiz (SuppressFlow):
        using (ExecutionContext.SuppressFlow())
        {
            await Task.Run(() =>
            {
                // Bu yerda kontekst ko'chmadi:
                Console.WriteLine($"Yangi oqimda: '{Foydalanuvchi.Value}' (bo'sh)");
            });
        }

        Console.WriteLine($"Asosiy oqimda: {Foydalanuvchi.Value}");
    }
}

```

## Tushuntirish va Mantiq:
`SuppressFlow` xavfsizlik kontekstlari yoki xotira ma'lumotlarini keraksiz o'tkazishni to'xtatib, yuqori yuklamali tizimlarda unumdorlikni oshiradi.

## Ishlash natijasi:
```text
Yangi oqimda: '' (bo'sh)
Asosiy oqimda: Admin
```

# 681-Topshiriq: TaskCreationOptions.LongRunning Bilan Alohida Oqim Yaratish
## Topshiriq sharti:
Cheksiz davom etuvchi fon jarayonlarini ThreadPool oqimiga tiqmaslik.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

internal class Program
{
    static void Main()
    {
        // LongRunning ThreadPool dan oqim olmaydi, balki alohida OS oqimi ochadi:
        Task fonVazifasi = Task.Factory.StartNew(() =>
        {
            Console.WriteLine($"Fon oqim ID: {Environment.CurrentManagedThreadId}, IsThreadPool: {Thread.CurrentThread.IsThreadPoolThread}");
        }, TaskCreationOptions.LongRunning);

        fonVazifasi.Wait();
    }
}

```

## Tushuntirish va Mantiq:
Uzoq vaqt ishlaydigan fon xizmatlari (Background Workers) uchun `TaskCreationOptions.LongRunning` ishlatiladi, aks holda ular ThreadPool oqimlarini bloklab, boshqa so'rovlarni sekinlashtiradi.

## Ishlash natijasi:
```text
Fon oqim ID: 3, IsThreadPool: False
```

# 682-Topshiriq: UnobservedTaskException Hodisasi
## Topshiriq sharti:
`await` qilinmagan xatoli tasklarning fojiasini oldini olish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

internal class Program
{
    static void Main()
    {
        TaskScheduler.UnobservedTaskException += (sender, e) =>
        {
            Console.WriteLine($"[Kuzatilmagan Xato Tutildi]: {e.Exception.InnerException?.Message}");
            e.SetObserved(); // Jarayon qulashining oldini olish
        };

        // Hech kim kutmagan (unawaited) va xato otadigan task:
        Task.Run(() => throw new Exception("Yashirin asinxron xato!"));

        Thread.Sleep(50);
        GC.Collect();
        GC.WaitForPendingFinalizers();
    }
}

```

## Tushuntirish va Mantiq:
Kuzatilmagan tasklar GC tomonidan tozalanganda `UnobservedTaskException` chaqiriladi. `e.SetObserved()` dastur qulab tushishidan himoya qiladi.

## Ishlash natijasi:
```text
[Kuzatilmagan Xato Tutildi]: Yashirin asinxron xato!
```

# 683-Topshiriq: Asinxron Retry Mexanizmi (Backoff Bilan Qayta Urinish)
## Topshiriq sharti:
Eksponentsial kechikish (Exponential Backoff) bilan asinxron qayta chaqirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static async Task<T> RetryAsync<T>(Func<Task<T>> amal, int urinishlar, int boshlangichKechikishMs)
    {
        for (int i = 1; i <= urinishlar; i++)
        {
            try
            {
                return await amal();
            }
            catch (Exception ex) when (i < urinishlar)
            {
                int kutish = boshlangichKechikishMs * (int)Math.Pow(2, i - 1);
                Console.WriteLine($"Xatolik: {ex.Message}. {kutish} ms dan so'ng {i + 1}-urinish...");
                await Task.Delay(kutish);
            }
        }
        return await amal();
    }

    static async Task Main()
    {
        int hisob = 0;
        var javob = await RetryAsync(async () =>
        {
            if (++hisob < 3) throw new Exception("503 Service Unavailable");
            await Task.Delay(10);
            return "200 Success";
        }, urinishlar: 3, boshlangichKechikishMs: 20);

        Console.WriteLine($"Yakun: {javob}");
    }
}

```

## Tushuntirish va Mantiq:
Exponential Backoff tarmoq yukini bir vaqtning o'zida oshirib yubormaslik uchun har bir urinishda kutish vaqtini 2 barobarga oshirib boradi.

## Ishlash natijasi:
```text
Xatolik: 503 Service Unavailable. 20 ms dan so'ng 2-urinish...
Xatolik: 503 Service Unavailable. 40 ms dan so'ng 3-urinish...
Yakun: 200 Success
```

# 684-Topshiriq: Asinxron Circuit Breaker Asoslari
## Topshiriq sharti:
Doimiy xatolik berayotgan tashqi xizmatni vaqtincha butunlay o'chirib qo'yish (Open State).

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

enum Holat { Yopiq, Ochiq }

class CircuitBreaker
{
    private Holat holat = Holat.Yopiq;
    private int xatolarSoni = 0;

    public async Task<string> BajarAsync(Func<Task<string>> amal)
    {
        if (holat == Holat.Ochiq)
            throw new InvalidOperationException("[Circuit Breaker OCHIQ]: Xizmat vaqtincha to'xtatilgan!");

        try
        {
            return await amal();
        }
        catch
        {
            if (++xatolarSoni >= 2)
            {
                holat = Holat.Ochiq;
                Console.WriteLine("[Ogohlantirish]: 2 ta xatodan so'ng kontaktlar uzildi (Ochiq holatga o'tdi).");
            }
            throw;
        }
    }
}

internal class Program
{
    static async Task Main()
    {
        var cb = new CircuitBreaker();

        for (int i = 1; i <= 3; i++)
        {
            try
            {
                await cb.BajarAsync(async () =>
                {
                    await Task.Delay(10);
                    throw new Exception("Xizmat javob bermayapti!");
                });
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Urinish #{i}: {ex.Message}");
            }
        }
    }
}

```

## Tushuntirish va Mantiq:
Circuit Breaker buzilgan tashqi xizmatga tinimsiz so'rov yuborib resurslarni tugatmasdan, ma'lum muddat unga murojaat qilishni to'xtatib turadi.

## Ishlash natijasi:
```text
Urinish #1: Xizmat javob bermayapti!
[Ogohlantirish]: 2 ta xatodan so'ng kontaktlar uzildi (Ochiq holatga o'tdi).
Urinish #2: Xizmat javob bermayapti!
Urinish #3: [Circuit Breaker OCHIQ]: Xizmat vaqtincha to'xtatilgan!
```

# 685-Topshiriq: Channel<T> Bilan Asinxron Ishchi Oqimlar Quvuri (Pipelines)
## Topshiriq sharti:
Yuqori tezlikdagi ma'lumotlarni parallel yozish va o'qish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Channels;
using System.Threading.Tasks;

internal class Program
{
    static async Task Main()
    {
        var kanal = Channel.CreateUnbounded<int>();

        // 1. Ishlab chiqaruvchi vazifa
        var yozuvchi = Task.Run(async () =>
        {
            for (int i = 1; i <= 3; i++)
            {
                await kanal.Writer.WriteAsync(i * 100);
            }
            kanal.Writer.Complete();
        });

        // 2. Iste'molchi vazifa
        var oquvchi = Task.Run(async () =>
        {
            while (await kanal.Reader.WaitToReadAsync())
            {
                while (kanal.Reader.TryRead(out int raqam))
                {
                    Console.WriteLine($"Kanal qabul qildi: {raqam}");
                }
            }
        });

        await Task.WhenAll(yozuvchi, oquvchi);
    }
}

```

## Tushuntirish va Mantiq:
`Channel<T>` yuqori unumdor asinxron xabarlar almashish kanali bo'lib, xotira sarfini minimallashtiradi va lock-free ishlaydi.

## Ishlash natijasi:
```text
Kanal qabul qildi: 100
Kanal qabul qildi: 200
Kanal qabul qildi: 300
```

# 686-Topshiriq: Asinxron Paketlash (Async Batching / Buffering)
## Topshiriq sharti:
So'rovlarni donalab emas, paket qilib guruhlab bazaga yuborish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

class AsinxronPaketlovchi
{
    private readonly List<string> bufer = new();

    public async Task Qo'shishAsync(string xabar)
    {
        bufer.Add(xabar);
        if (bufer.Count >= 3)
        {
            await JonatishAsync();
        }
    }

    private async Task JonatishAsync()
    {
        Console.WriteLine($"[Paket yuborildi]: {string.Join(", ", bufer)}");
        bufer.Clear();
        await Task.Delay(20);
    }
}

internal class Program
{
    static async Task Main()
    {
        var paketchi = new AsinxronPaketlovchi();
        await paketchi.Qo'shishAsync("Log 1");
        await paketchi.Qo'shishAsync("Log 2");
        await paketchi.Qo'shishAsync("Log 3"); // Bu yerda paket to'lib jo'natiladi
    }
}

```

## Tushuntirish va Mantiq:
Batching har bir ma'lumot uchun alohida tarmoq so'rovi ochish o'rniga ularni to'plab jo'natadi va tarmoq xarajatlarini keskin qisqartiradi.

## Ishlash natijasi:
```text
[Paket yuborildi]: Log 1, Log 2, Log 3
```

# 687-Topshiriq: Custom Awaiter Yaratish (GetAwaiter Pattern)
## Topshiriq sharti:
Har qanday sinfni `await` qilinadigan qilish mexanizmi.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.CompilerServices;
using System.Threading.Tasks;

class MaxsusKutish : INotifyCompletion
{
    public bool IsCompleted => true; // Darhol yakunlangan deb hisoblaymiz
    public void OnCompleted(Action continuation) => continuation();
    public string GetResult() => "Maxsus Awaiter muvaffaqiyatli ishladi!";

    public MaxsusKutish GetAwaiter() => this;
}

internal class Program
{
    static async Task Main()
    {
        var kutish = new MaxsusKutish();

        // O'zimiz yozgan sinfni bevosita await qilamiz:
        string natija = await kutish;
        Console.WriteLine(natija);
    }
}

```

## Tushuntirish va Mantiq:
C# da `await` operatori sinfning `Task` bo'lishini talab qilmaydi; unda shunchaki `GetAwaiter()` metodi va `INotifyCompletion` shartnomasi bo'lishi kifoya.

## Ishlash natijasi:
```text
Maxsus Awaiter muvaffaqiyatli ishladi!
```

# 688-Topshiriq: TimeSpan ni To'g'ridan-To'g'ri `await` Qilish Extension Metodi
## Topshiriq sharti:
C# dagi `TimeSpan` ustiga maxsus Awaiter yozish.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.CompilerServices;
using System.Threading.Tasks;

static class TimeSpanExtensions
{
    public static TaskAwaiter GetAwaiter(this TimeSpan timeSpan)
    {
        return Task.Delay(timeSpan).GetAwaiter();
    }
}

internal class Program
{
    static async Task Main()
    {
        Console.WriteLine("Kutish boshlandi...");

        // TimeSpan ni to'g'ridan-to'g'ri await qilamiz!
        await TimeSpan.FromMilliseconds(50);

        Console.WriteLine("Kutish yakunlandi.");
    }
}

```

## Tushuntirish va Mantiq:
Extension metodlar orqali hatto BCL ning mavjud turlariga ham `GetAwaiter()` qo'shib, sintaksisni nihoyatda chiroyli qilish mumkin.

## Ishlash natijasi:
```text
Kutish boshlandi...
Kutish yakunlandi.
```

# 689-Topshiriq: Asinxron Singleton (Thread-Safe Asynchronous Initialization)
## Topshiriq sharti:
Faqat bitta oqim asinxron initsializatsiya qilishini kafolatlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

class AsinxronSingleton
{
    private static AsinxronSingleton? instansiya;
    private static readonly SemaphoreSlim lockSemafor = new(1, 1);

    private AsinxronSingleton() { }

    public static async Task<AsinxronSingleton> GetInstanceAsync()
    {
        if (instansiya != null) return instansiya;

        await lockSemafor.WaitAsync();
        try
        {
            if (instansiya == null)
            {
                Console.WriteLine("Asinxron obyekt yaratilmoqda...");
                await Task.Delay(30);
                instansiya = new AsinxronSingleton();
            }
            return instansiya;
        }
        finally
        {
            lockSemafor.Release();
        }
    }
}

internal class Program
{
    static async Task Main()
    {
        var s1 = await AsinxronSingleton.GetInstanceAsync();
        var s2 = await AsinxronSingleton.GetInstanceAsync();

        Console.WriteLine($"Ikkala havola tengmi: {object.ReferenceEquals(s1, s2)}");
    }
}

```

## Tushuntirish va Mantiq:
Asinxron singleton og'ir konfiguratsiyalar yoki masofaviy ulanishlarni faqat bir marta va xavfsiz yuklashda qo'llaniladi.

## Ishlash natijasi:
```text
Asinxron obyekt yaratilmoqda...
Ikkala havola tengmi: True
```

# 690-Topshiriq: Asinxron Shartli Hodisa: AsyncAutoResetEvent
## Topshiriq sharti:
Boshqa oqim signal bermaguncha asinxron oqimni uxlatib turish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

class AsyncAutoResetEvent
{
    private TaskCompletionSource<bool> tcs = new();

    public Task WaitAsync() => tcs.Task;

    public void Set()
    {
        var eskiTcs = tcs;
        tcs = new TaskCompletionSource<bool>();
        eskiTcs.TrySetResult(true);
    }
}

internal class Program
{
    static async Task Main()
    {
        var signal = new AsyncAutoResetEvent();

        _ = Task.Run(async () =>
        {
            await Task.Delay(40);
            Console.WriteLine("[Yordamchi]: Signal berildi!");
            signal.Set();
        });

        Console.WriteLine("[Asosiy]: Signal kutilmoqda...");
        await signal.WaitAsync();
        Console.WriteLine("[Asosiy]: Signal qabul qilindi, ish davom etadi.");
    }
}

```

## Tushuntirish va Mantiq:
AsyncAutoResetEvent sinxron `AutoResetEvent` kabi ishlaydi, lekin oqimni qotirmasdan `await` orqali kutadi.

## Ishlash natijasi:
```text
[Asosiy]: Signal kutilmoqda...
[Yordamchi]: Signal berildi!
[Asosiy]: Signal qabul qilindi, ish davom etadi.
```

# 691-Topshiriq: Asinxron Countdown: AsyncCountdownEvent
## Topshiriq sharti:
Belgilangan $N$ ta asinxron vazifa yakunlangach uyg'onuvchi vosita.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

class AsyncCountdown
{
    private int soni;
    private readonly TaskCompletionSource<bool> tcs = new();

    public AsyncCountdown(int soni) => this.soni = soni;

    public void Signal()
    {
        if (Interlocked.Decrement(ref soni) == 0)
        {
            tcs.TrySetResult(true);
        }
    }

    public Task WaitAsync() => tcs.Task;
}

internal class Program
{
    static async Task Main()
    {
        var hisoblagich = new AsyncCountdown(2);

        Task t1 = Task.Run(async () => { await Task.Delay(20); hisoblagich.Signal(); });
        Task t2 = Task.Run(async () => { await Task.Delay(40); hisoblagich.Signal(); });

        Console.WriteLine("2 ta vazifa tugashi kutilmoqda...");
        await hisoblagich.WaitAsync();
        Console.WriteLine("Barcha vazifalar yakunlandi!");
    }
}

```

## Tushuntirish va Mantiq:
Interlocked orqali atomar kamaytirish va `TaskCompletionSource` orqali asinxron uyg'otish amalga oshiriladi.

## Ishlash natijasi:
```text
2 ta vazifa tugashi kutilmoqda...
Barcha vazifalar yakunlandi!
```

# 692-Topshiriq: Asinxron Qatorli Navbat: Task.WhenAny Bilan Oqimni Tugashi Bo'yicha O'qish
## Topshiriq sharti:
Vazifalarni berilgan tartibda emas, qaysi biri birinchi tayyor bo'lsa o'sha tartibda qayta ishlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

internal class Program
{
    static async Task Main()
    {
        List<Task<string>> vazifalar =
        [
            Task.Run(async () => { await Task.Delay(80); return "Sekin vazifa"; }),
            Task.Run(async () => { await Task.Delay(20); return "Tezkor vazifa"; }),
            Task.Run(async () => { await Task.Delay(50); return "O'rtacha vazifa"; })
        ];

        while (vazifalar.Count > 0)
        {
            Task<string> tayyor = await Task.WhenAny(vazifalar);
            vazifalar.Remove(tayyor);

            string natija = await tayyor;
            Console.WriteLine($"Tayyor bo'ldi: {natija}");
        }
    }
}

```

## Tushuntirish va Mantiq:
Bu naqsh eng tezkor tayyor bo'lgan natijalarni darhol foydalanuvchiga ko'rsatish yoki quvurga yuborish imkonini beradi.

## Ishlash natijasi:
```text
Tayyor bo'ldi: Tezkor vazifa
Tayyor bo'ldi: O'rtacha vazifa
Tayyor bo'ldi: Sekin vazifa
```

# 693-Topshiriq: Asinxron Metodlarda Xotira Ajratmaslik: ValueTasks Hovuzi
## Topshiriq sharti:
`IValueTaskSource` orqali ValueTask ning xotirani tejash mexanizmini tushunish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static ValueTask<int> TezkorQiymat(int a, int b)
    {
        // Sinxron hisob-kitob bo'lgani uchun xotira 0 bayt:
        return ValueTask.FromResult(a + b);
    }

    static async Task Main()
    {
        int sum = await TezkorQiymat(15, 25);
        Console.WriteLine($"Yig'indi: {sum}");
    }
}

```

## Tushuntirish va Mantiq:
`ValueTask.FromResult` struct qaytargani sababli CLR Heap xotirada hech qanday obyekt yaratmaydi.

## Ishlash natijasi:
```text
Yig'indi: 40
```

# 694-Topshiriq: CancellationTokenSource.Cancel vs CancelAsync (.NET 8+)
## Topshiriq sharti:
.NET 8 da qo'shilgan `CancelAsync` metodi va uning afzalligi.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

internal class Program
{
    static async Task Main()
    {
        using var cts = new CancellationTokenSource();

        cts.Token.Register(() =>
        {
            Console.WriteLine("Bekor qilish xabarnomasi ishga tushdi.");
        });

        // .NET 8 CancelAsync barcha callbacklarni asinxron xavfsiz chaqiradi:
        await cts.CancelAsync();
        Console.WriteLine("Bekor qilish to'liq yakunlandi.");
    }
}

```

## Tushuntirish va Mantiq:
.NET 8 gacha bo'lgan `cts.Cancel()` barcha ro'yxatga olingan callbacklarni joriy oqimda sinxron chaqirib, oqimni to'xtatib qo'yishi mumkin edi. `CancelAsync` esa ularni asinxron bajaradi.

## Ishlash natijasi:
```text
Bekor qilish xabarnomasi ishga tushdi.
Bekor qilish to'liq yakunlandi.
```

# 695-Topshiriq: Task.Run Ichidagi Asinxron Lambdalarni Unwrapping Qilish
## Topshiriq sharti:
`Task<Task<T>>` va `Task<T>` farqi.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static async Task Main()
    {
        // Task.Run ichida asinxron lambda ishlatilganda, u Task<T> ni avtomatik 'unwrap' qiladi:
        Task<string> task = Task.Run(async () =>
        {
            await Task.Delay(20);
            return "Unwrapped natija";
        });

        string natija = await task;
        Console.WriteLine(natija);
    }
}

```

## Tushuntirish va Mantiq:
`Task.Run` kompilyator tomonidan ichma-ich o'ralgan tasklarni avtomatik unwrap qiladi, shuning uchun natija `Task<Task<string>>` emas, balki to'g'ridan-to'g'ri `Task<string>` bo'ladi.

## Ishlash natijasi:
```text
Unwrapped natija
```

# 696-Topshiriq: Asinxron Tarmoq Cheklovi (Rate Limiter) Naqshi
## Topshiriq sharti:
Sekundiga belgilangan sondan ortiq so'rov o'tkazmaydigan asinxron darvoza.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

class AsinxronRateLimiter
{
    private readonly SemaphoreSlim semafor;

    public AsinxronRateLimiter(int limit)
    {
        semafor = new SemaphoreSlim(limit, limit);
    }

    public async Task BajarAsync(Action amal)
    {
        await semafor.WaitAsync();
        try
        {
            amal();
        }
        finally
        {
            _ = Task.Delay(100).ContinueWith(_ => semafor.Release());
        }
    }
}

internal class Program
{
    static async Task Main()
    {
        var limiter = new AsinxronRateLimiter(2);

        await limiter.BajarAsync(() => Console.WriteLine("1-so'rov o'tdi"));
        await limiter.BajarAsync(() => Console.WriteLine("2-so'rov o'tdi"));
    }
}

```

## Tushuntirish va Mantiq:
Rate Limiter tashqi API kvotalarini oshirib yubormaslik va tizimni ortiqcha yuklamalardan himoyalash uchun qo'llaniladi.

## Ishlash natijasi:
```text
1-so'rov o'tdi
2-so'rov o'tdi
```

# 697-Topshiriq: Asinxron Blokda `ref struct` Ishlatish Cheklovi
## Topshiriq sharti:
Nima uchun `Span<T>` ni `async` metod ichida `await` orqali saqlab bo'lmaydi?

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static async Task XavfsizSpanQollash()
    {
        // Await dan oldin yoki keyin Span ishlatish mumkin:
        int[] massiv = [1, 2, 3];
        Span<int> span = massiv;
        span[0] = 99;

        // LEKIN Span 'await' orqali yashay olmaydi, chunki u Stackda qolishi shart!
        await Task.Delay(10);

        // Await dan keyin esa Memory<T> ishlatish tavsiya etiladi:
        Memory<int> xotira = massiv;
        Console.WriteLine($"0-element: {xotira.Span[0]}");
    }

    static async Task Main()
    {
        await XavfsizSpanQollash();
    }
}

```

## Tushuntirish va Mantiq:
`ref struct` (jumladan `Span<T>`) faqat joriy stack ramkasida yashashi mumkin. `await` esa holatni Heap xotiradagi `IAsyncStateMachine` ga ko'chirishi sababli, Span ni `await` orqali saqlash kompilyatsiya darajasida taqiqlangan. Buning uchun `Memory<T>` ishlatiladi.

## Ishlash natijasi:
```text
0-element: 99
```

# 698-Topshiriq: Asinxron Oqimda Xatolikni Qayta Tiklash (Catch and Fallback)
## Topshiriq sharti:
Xatolik yuz berganda ikkinchi darajali zaxira serverga murojaat qilish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

internal class Program
{
    static async Task<string> AsosiyServer()
    {
        await Task.Delay(10);
        throw new Exception("Asosiy server ishlamayapti");
    }

    static async Task<string> ZaxiraServer()
    {
        await Task.Delay(10);
        return "Zaxira serverdan ma'lumot olindi";
    }

    static async Task Main()
    {
        string natija;
        try
        {
            natija = await AsosiyServer();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Xato: {ex.Message}. Zaxiraga o'tilmoqda...");
            natija = await ZaxiraServer();
        }

        Console.WriteLine($"Javob: {natija}");
    }
}

```

## Tushuntirish va Mantiq:
Asinxron try-catch bloklari kutilmagan buzilishlarni yumshatish (Graceful Fallback) uchun juda qulaydir.

## Ishlash natijasi:
```text
Xato: Asosiy server ishlamayapti. Zaxiraga o'tilmoqda...
Javob: Zaxira serverdan ma'lumot olindi
```

# 699-Topshiriq: IAsyncEnumerable da `TakeAsync` va Filtrlash
## Topshiriq sharti:
Asinxron oqimni ma'lum bir shart bilan uzib olish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

internal class Program
{
    static async IAsyncEnumerable<int> Oqim()
    {
        for (int i = 1; i <= 10; i++)
        {
            await Task.Delay(10);
            yield return i;
        }
    }

    static async Task Main()
    {
        int hisob = 0;
        await foreach (int son in Oqim())
        {
            if (son % 2 == 0)
            {
                Console.WriteLine($"Juft son: {son}");
                if (++hisob == 2) break; // 2 ta juft son olingach asinxron oqimni to'xtatish
            }
        }
    }
}

```

## Tushuntirish va Mantiq:
`await foreach` ichidagi `break` bayonoti asinxron generatorning `DisposeAsync` metodini avtomatik chaqiradi va manbani xavfsiz tozalaydi.

## Ishlash natijasi:
```text
Juft son: 2
Juft son: 4
```

# 700-Topshiriq: Asinxronlik Xulosasi: Parallel Asinxron Yuklovchi Dvigateli (Concurrent Downloader Engine)
## Topshiriq sharti:
SemaphoreSlim, CancellationToken, Task.WhenAll va xatoliklar boshqaruvini birlashtirgan to'liq yuklovchi tizim.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

class YuklovchiDvigatel
{
    private readonly SemaphoreSlim semafor;

    public YuklovchiDvigatel(int maxParallelizm)
    {
        semafor = new SemaphoreSlim(maxParallelizm);
    }

    public async Task<string> YuklashAsync(string resursNom, CancellationToken ct)
    {
        await semafor.WaitAsync(ct);
        try
        {
            Console.WriteLine($"[Boshlandi]: {resursNom}");
            await Task.Delay(30, ct); // Simulyatsiya qilingan yuklash
            Console.WriteLine($"[Tugadi]: {resursNom}");
            return $"Tarkib ({resursNom})";
        }
        finally
        {
            semafor.Release();
        }
    }
}

internal class Program
{
    static async Task Main()
    {
        var dvigatel = new YuklovchiDvigatel(maxParallelizm: 2);
        using var cts = new CancellationTokenSource();

        string[] fayllar = ["Fayl_1.dat", "Fayl_2.dat", "Fayl_3.dat"];
        var vazifalar = new List<Task<string>>();

        foreach (var f in fayllar)
        {
            vazifalar.Add(dvigatel.YuklashAsync(f, cts.Token));
        }

        string[] natijalar = await Task.WhenAll(vazifalar);

        Console.WriteLine($"
Barcha {natijalar.Length} ta fayl muvaffaqiyatli yuklab olindi!");
    }
}

```

## Tushuntirish va Mantiq:
Bu arxitektura zamonaviy yuqori yuklamali .NET veb serverlari va yuklovchi tizimlarining asosi bo'lib, xotira va tarmoq resurslarini qat'iy nazorat ostida parallel boshqaradi.

## Ishlash natijasi:
```text
[Boshlandi]: Fayl_1.dat
[Boshlandi]: Fayl_2.dat
[Tugadi]: Fayl_1.dat
[Boshlandi]: Fayl_3.dat
[Tugadi]: Fayl_2.dat
[Tugadi]: Fayl_3.dat

Barcha 3 ta fayl muvaffaqiyatli yuklab olindi!
```

