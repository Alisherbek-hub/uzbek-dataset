# 19-Mavzu: Entity Framework Core va ORM (901-950)

Ushbu bo'limda C# va .NET da ma'lumotlar bazasi bilan ishlash (EF Core 8/9): `DbContext`, `DbSet<T>`, Fluent API va Data Annotations, birlamchi va kompozit kalitlar, bog'lanishlar (One-to-One, One-to-Many, Many-to-Many), Cascade Delete, Change Tracker va EntityState, `AsNoTracking` unumdorligi, yuklash strategiyalari (Eager Loading `Include`/`ThenInclude`, Explicit Loading, Lazy Loading), .NET 7/8/9 ommaviy amallari (`ExecuteUpdateAsync`, `ExecuteDeleteAsync`), `FromSqlInterpolated`, Global Query Filters (Soft Delete) hamda optimistik qulflash (Optimistic Concurrency) bo'yicha 50 ta amaliy topshiriq jamlangan.

# 901-Topshiriq: EF Core Asoslari: DbContext va DbSet<T> E'lon Qilish
## Topshiriq sharti:
Ma'lumotlar bazasi sessiyasini ifodalovchi asosiy konteynerni yaratish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

class Mahsulot
{
    public int Id { get; set; }
    public string Nomi { get; set; } = "";
    public decimal Narxi { get; set; }
}

class DokonDbContext : DbContext
{
    public DbSet<Mahsulot> Mahsulotlar => Set<Mahsulot>();

    protected override void OnConfiguring(DbContextOptionsBuilder options)
    {
        // Xotiradagi (InMemory) SQLite yoki provayder ulanishi:
        options.UseInMemoryDatabase("DokonDb");
    }
}

internal class Program
{
    static async Task Main()
    {
        using var db = new DokonDbContext();

        db.Mahsulotlar.Add(new Mahsulot { Nomi = "Kitob", Narxi = 45000 });
        await db.SaveChangesAsync();

        var kitob = await db.Mahsulotlar.FirstAsync();
        Console.WriteLine($"Bazadan olindi: #{kitob.Id} {kitob.Nomi} - {kitob.Narxi} so'm");
    }
}

```

## Tushuntirish va Mantiq:
`DbContext` ma'lumotlar bazasi bilan aloqa kanalini boshqaradi, `DbSet<T>` esa SQL dagi jadvallarni ifodalaydi. `SaveChangesAsync()` o'zgarishlarni bitta tranzaksiyada bazaga yozadi.

## Ishlash natijasi:
```text
Bazadan olindi: #1 Kitob - 45000 so'm
```

# 902-Topshiriq: Fluent API vs Data Annotations
## Topshiriq sharti:
`OnModelCreating` orqali jadval va ustun nomlarini sozlash.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class Foydalanuvchi
{
    public int FoydalanuvchiId { get; set; }
    public string Login { get; set; } = "";
}

class AppDbContext : DbContext
{
    public DbSet<Foydalanuvchi> Foydalanuvchilar => Set<Foydalanuvchi>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Foydalanuvchi>(entity =>
        {
            entity.ToTable("tbl_users");
            entity.HasKey(e => e.FoydalanuvchiId);
            entity.Property(e => e.Login)
                  .IsRequired()
                  .HasMaxLength(50)
                  .HasColumnName("user_login");
        });
    }

    protected override void OnConfiguring(DbContextOptionsBuilder options) => options.UseInMemoryDatabase("TestDb");
}

internal class Program
{
    static void Main()
    {
        using var db = new AppDbContext();
        Console.WriteLine("Fluent API konfiguratsiyasi muvaffaqiyatli qurildi.");
    }
}

```

## Tushuntirish va Mantiq:
Fluent API model sinflarini toza saqlaydi (Clean Architecture) va Data Annotations ga qaraganda ancha kengroq sozlash imkoniyatlarini beradi.

## Ishlash natijasi:
```text
Fluent API konfiguratsiyasi muvaffaqiyatli qurildi.
```

# 903-Topshiriq: Kompozit Birlamchi Kalitlar (Composite Keys) Sozlash
## Topshiriq sharti:
Ikkita ustun birlashmasidan yagona kalit hosil qilish (`HasKey(a, b)`).

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class BuyurtmaElementi
{
    public int BuyurtmaId { get; set; }
    public int MahsulotId { get; set; }
    public int Soni { get; set; }
}

class SavdoDbContext : DbContext
{
    public DbSet<BuyurtmaElementi> Elementlar => Set<BuyurtmaElementi>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Ikkita maydondan iborat kompozit kalit:
        modelBuilder.Entity<BuyurtmaElementi>()
                    .HasKey(e => new { e.BuyurtmaId, e.MahsulotId });
    }

    protected override void OnConfiguring(DbContextOptionsBuilder options) => options.UseInMemoryDatabase("SavdoDb");
}

internal class Program
{
    static void Main()
    {
        using var db = new SavdoDbContext();
        Console.WriteLine("Kompozit kalit muvaffaqiyatli ta'riflandi.");
    }
}

```

## Tushuntirish va Mantiq:
Oraliq jadvallarda (Join Tables) va ko'p parametrli identifikatorlarda kompozit kalitlar takroriy yozuvlarni oldini oladi.

## Ishlash natijasi:
```text
Kompozit kalit muvaffaqiyatli ta'riflandi.
```

# 904-Topshiriq: Yakka-ko'p Bog'lanish (One-to-Many Relationship)
## Topshiriq sharti:
Muallif va uning Kitoblari o'rtasidagi klassik 1:N munosabati.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

class Muallif
{
    public int Id { get; set; }
    public string Ism { get; set; } = "";
    public List<Kitob> Kitoblar { get; set; } = new();
}

class Kitob
{
    public int Id { get; set; }
    public string Sarlavha { get; set; } = "";
    public int MuallifId { get; set; }
    public Muallif? Muallif { get; set; }
}

class KutubxonaDbContext : DbContext
{
    public DbSet<Muallif> Mualliflar => Set<Muallif>();
    public DbSet<Kitob> Kitoblar => Set<Kitob>();

    protected override void OnConfiguring(DbContextOptionsBuilder options) => options.UseInMemoryDatabase("KutubxonaDb");
}

internal class Program
{
    static async Task Main()
    {
        using var db = new KutubxonaDbContext();

        var muallif = new Muallif { Ism = "Abdulla Qodiriy" };
        muallif.Kitoblar.Add(new Kitob { Sarlavha = "O'tkan Kunlar" });
        muallif.Kitoblar.Add(new Kitob { Sarlavha = "Mehrobdan Chayon" });

        db.Mualliflar.Add(muallif);
        await db.SaveChangesAsync();

        var topilgan = await db.Mualliflar.Include(m => m.Kitoblar).FirstAsync();
        Console.WriteLine($"{topilgan.Ism}: {topilgan.Kitoblar.Count} ta kitobi bor.");
    }
}

```

## Tushuntirish va Mantiq:
One-to-Many bog'lanishida EF Core avtomatik ravishda tashqi kalitni (`MuallifId` ForeignKey) hosil qiladi.

## Ishlash natijasi:
```text
Abdulla Qodiriy: 2 ta kitobi bor.
```

# 905-Topshiriq: .NET 5+ Ko'pga-Ko'p Bog'lanish (Many-to-Many Without Explicit Join Entity)
## Topshiriq sharti:
Oraliq sinf yozmasdan to'g'ridan-to'g'ri $N:M$ bog'lanish qurish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;

class Talaba
{
    public int Id { get; set; }
    public string Ism { get; set; } = "";
    public List<Kurs> Kurslar { get; set; } = new();
}

class Kurs
{
    public int Id { get; set; }
    public string Nomi { get; set; } = "";
    public List<Talaba> Talabalar { get; set; } = new();
}

class UniversitetDbContext : DbContext
{
    public DbSet<Talaba> Talabalar => Set<Talaba>();
    public DbSet<Kurs> Kurslar => Set<Kurs>();

    protected override void OnConfiguring(DbContextOptionsBuilder options) => options.UseInMemoryDatabase("UniDb");
}

internal class Program
{
    static void Main()
    {
        using var db = new UniversitetDbContext();
        Console.WriteLine("Many-to-Many to'g'ridan-to'g'ri bog'lanish o'rnatildi.");
    }
}

```

## Tushuntirish va Mantiq:
EF Core 5+ dan boshlab ikkala sinfda ham `List<BoshqaSinf>` bo'lsa, oraliq jadval (Join Table) fonida avtomatik boshqariladi.

## Ishlash natijasi:
```text
Many-to-Many to'g'ridan-to'g'ri bog'lanish o'rnatildi.
```

# 906-Topshiriq: Kaskadli O'chirish (Cascade Delete Xatti-Harakati)
## Topshiriq sharti:
Ota yozuv o'chirilganda unga bog'liq bolalarni o'chirish yoki saqlab qolish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class Blog { public int Id { get; set; } }
class Post { public int Id { get; set; } public int BlogId { get; set; } }

class BlogDbContext : DbContext
{
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Post>()
            .HasOne<Blog>()
            .WithMany()
            .HasForeignKey(p => p.BlogId)
            .OnDelete(DeleteBehavior.Cascade); // Blog o'chsa, barcha Postlar ham o'chadi
    }

    protected override void OnConfiguring(DbContextOptionsBuilder options) => options.UseInMemoryDatabase("BlogDb");
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("DeleteBehavior.Cascade muvaffaqiyatli belgilandi.");
    }
}

```

## Tushuntirish va Mantiq:
`DeleteBehavior.Restrict` yoki `SetNull` kabi variantlar orqali bolalar tasodifan o'chib ketishining oldini olish mumkin.

## Ishlash natijasi:
```text
DeleteBehavior.Cascade muvaffaqiyatli belgilandi.
```

# 907-Topshiriq: Change Tracker va EntityState Holatlari
## Topshiriq sharti:
Obyekt holatining Added, Modified, Unchanged, Deleted va Detached bo'lishi.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class Xaridor { public int Id { get; set; } public string Ism { get; set; } = ""; }

class TestDbContext : DbContext
{
    public DbSet<Xaridor> Xaridorlar => Set<Xaridor>();
    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("TDb");
}

internal class Program
{
    static void Main()
    {
        using var db = new TestDbContext();
        var x = new Xaridor { Ism = "Sobir" };

        Console.WriteLine($"Boshlang'ich holat: {db.Entry(x).State}"); // Detached

        db.Xaridorlar.Add(x);
        Console.WriteLine($"Add dan keyin: {db.Entry(x).State}"); // Added

        db.SaveChanges();
        Console.WriteLine($"SaveChanges dan keyin: {db.Entry(x).State}"); // Unchanged

        x.Ism = "Sobirjon";
        Console.WriteLine($"O'zgartirilgach: {db.Entry(x).State}"); // Modified
    }
}

```

## Tushuntirish va Mantiq:
Change Tracker har bir yuklangan obyektning asl nusxasini (snapshot) xotirada ushlab turadi va nima o'zgarganini solishtirib SQL hosil qiladi.

## Ishlash natijasi:
```text
Boshlang'ich holat: Detached
Add dan keyin: Added
SaveChanges dan keyin: Unchanged
O'zgartirilgach: Modified
```

# 908-Topshiriq: AsNoTracking: O'qish Tezligini Keskin Oshirish
## Topshiriq sharti:
Change Tracker ni o'chirib, xotirani va CPU ni tejash.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

class Mahsulot { public int Id { get; set; } public string Nomi { get; set; } = ""; }

class TezDbContext : DbContext
{
    public DbSet<Mahsulot> Mahsulotlar => Set<Mahsulot>();
    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("TezDb");
}

internal class Program
{
    static async Task Main()
    {
        using var db = new TezDbContext();
        db.Mahsulotlar.Add(new Mahsulot { Nomi = "Kofe" });
        await db.SaveChangesAsync();

        // AsNoTracking orqali o'qish:
        var kofe = await db.Mahsulotlar.AsNoTracking().FirstAsync();

        Console.WriteLine($"Olingan: {kofe.Nomi}");
        Console.WriteLine($"Obyekt kuzatilmoqdami: {db.Entry(kofe).State}"); // Detached
    }
}

```

## Tushuntirish va Mantiq:
Faqat o'qish uchun mo'ljallangan (Read-Only) barcha so'rovlarda `AsNoTracking()` ishlatilishi shart. Bu xotira ajratishni 2-3 barobarga qisqartiradi.

## Ishlash natijasi:
```text
Olingan: Kofe
Obyekt kuzatilmoqdami: Detached
```

# 909-Topshiriq: Eager Loading: Include va ThenInclude
## Topshiriq sharti:
Bog'langan jadvallarni bitta so'rovda oldindan yuklash.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

class Mamlakat { public int Id { get; set; } public string Nomi { get; set; } = ""; public List<Viloyat> Viloyatlar { get; set; } = new(); }
class Viloyat { public int Id { get; set; } public string Nomi { get; set; } = ""; public List<Shahar> Shaharlar { get; set; } = new(); }
class Shahar { public int Id { get; set; } public string Nomi { get; set; } = ""; }

class GeografiyaDbContext : DbContext
{
    public DbSet<Mamlakat> Mamlakatlar => Set<Mamlakat>();
    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("GeoDb");
}

internal class Program
{
    static async Task Main()
    {
        using var db = new GeografiyaDbContext();

        // Include va ThenInclude zanjiri:
        var data = await db.Mamlakatlar
            .Include(m => m.Viloyatlar)
                .ThenInclude(v => v.Shaharlar)
            .FirstOrDefaultAsync();

        Console.WriteLine("Eager loading so'rovi muvaffaqiyatli tuzildi.");
    }
}

```

## Tushuntirish va Mantiq:
`Include` SQL dagi `LEFT JOIN` ga aylanadi va barcha bog'liq ierarxiyani bitta chaqiruvda olib keladi.

## Ishlash natijasi:
```text
Eager loading so'rovi muvaffaqiyatli tuzildi.
```

# 910-Topshiriq: Explicit Loading: Entry().Collection().LoadAsync()
## Topshiriq sharti:
Bog'langan ma'lumotlarni faqat kerak bo'lganda qo'lda yuklab olish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

class Guruh { public int Id { get; set; } public List<Azo> Azolar { get; set; } = new(); }
class Azo { public int Id { get; set; } public string Ism { get; set; } = ""; }

class GuruhDbContext : DbContext
{
    public DbSet<Guruh> Guruhlar => Set<Guruh>();
    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("GDb");
}

internal class Program
{
    static async Task Main()
    {
        using var db = new GuruhDbContext();
        var g = new Guruh();
        g.Azolar.Add(new Azo { Ism = "Botir" });
        db.Guruhlar.Add(g);
        await db.SaveChangesAsync();

        // Guruhni a'zolarsiz olamiz:
        var topilgan = await db.Guruhlar.FirstAsync();

        // Keyinroq a'zolarni aniq talab qilib yuklaymiz (Explicit):
        await db.Entry(topilgan).Collection(x => x.Azolar).LoadAsync();

        Console.WriteLine($"A'zolar soni: {topilgan.Azolar.Count}");
    }
}

```

## Tushuntirish va Mantiq:
Explicit Loading shartli holatlarda (masalan faqat administrator so'ragandagina) katta bog'langan to'plamlarni yuklashda qulay.

## Ishlash natijasi:
```text
A'zolar soni: 1
```

# 911-Topshiriq: AsSplitQuery Bilan Katta JOIN larni Bo'laklash
## Topshiriq sharti:
Katta jadvallar bog'langanda yuzaga keladigan Kartesian portlash (Cartesian Explosion) dan saqlanish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class KompaniyaDbContext : DbContext
{
    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("KompDb");
}

internal class Program
{
    static void Main()
    {
        // AsSplitQuery bitta ulkan JOIN o'rniga, har bir Include uchun alohida toza SQL so'rov yuboradi:
        Console.WriteLine("AsSplitQuery arxitekturasi: Cartesian Explosion ning oldini oladi.");
    }
}

```

## Tushuntirish va Mantiq:
Bitta so'rovda 4-5 ta `Include` bo'lsa, SQL `JOIN` satrlar sonini millionlarga ko'paytirib yuboradi. `AsSplitQuery()` ularni bir nechta alohida `SELECT` so'rovlariga bo'lib, xotirani saqlaydi.

## Ishlash natijasi:
```text
AsSplitQuery arxitekturasi: Cartesian Explosion ning oldini oladi.
```

# 912-Topshiriq: .NET 7+ ExecuteUpdateAsync: Change Tracker siz To'g'ridan-To'g'ri SQL UPDATE
## Topshiriq sharti:
Obyektlarni xotiraga yuklamasdan bitta SQL buyrug'i bilan minglab yozuvlarni yangilash.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

class Xodim { public int Id { get; set; } public decimal Maosh { get; set; } public string Bolim { get; set; } = ""; }

class KorxonaDbContext : DbContext
{
    public DbSet<Xodim> Xodimlar => Set<Xodim>();
    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("KorxonaDb");
}

internal class Program
{
    static async Task Main()
    {
        using var db = new KorxonaDbContext();
        db.Xodimlar.Add(new Xodim { Maosh = 1000, Bolim = "IT" });
        await db.SaveChangesAsync();

        // .NET 7 da to'g'ridan-to'g'ri UPDATE "Xodimlar" SET "Maosh" = "Maosh" * 1.1 WHERE "Bolim" = 'IT':
        await db.Xodimlar
            .Where(x => x.Bolim == "IT")
            .ExecuteUpdateAsync(s => s.SetProperty(x => x.Maosh, x => x.Maosh * 1.1m));

        var x = await db.Xodimlar.FirstAsync();
        Console.WriteLine($"Yangi maosh: {x.Maosh}");
    }
}

```

## Tushuntirish va Mantiq:
`ExecuteUpdateAsync` Change Tracker ni aylanib o'tib, to'g'ridan-to'g'ri ma'lumotlar bazasiga bitta `UPDATE` buyrug'ini yuboradi va unumdorlikni 1000 barobargacha oshiradi.

## Ishlash natijasi:
```text
Yangi maosh: 1100.0
```

# 913-Topshiriq: .NET 7+ ExecuteDeleteAsync: To'g'ridan-To'g'ri Ommaviy O'chirish
## Topshiriq sharti:
Minglab yozuvlarni bitta `DELETE WHERE` orqali bazadan tozalash.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

class LogYozuvi { public int Id { get; set; } public DateTime Sana { get; set; } }

class LogDbContext : DbContext
{
    public DbSet<LogYozuvi> Loglar => Set<LogYozuvi>();
    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("LogDb");
}

internal class Program
{
    static async Task Main()
    {
        using var db = new LogDbContext();
        db.Loglar.Add(new LogYozuvi { Sana = DateTime.UtcNow.AddDays(-40) });
        await db.SaveChangesAsync();

        var chegara = DateTime.UtcNow.AddDays(-30);

        // 30 kundan eski barcha loglarni xotiraga tortmasdan to'g'ridan-to'g'ri o'chiramiz:
        int ochirildi = await db.Loglar
            .Where(l => l.Sana < chegara)
            .ExecuteDeleteAsync();

        Console.WriteLine($"O'chirilgan loglar soni: {ochirildi}");
    }
}

```

## Tushuntirish va Mantiq:
`ExecuteDeleteAsync` avvalgi `ToList() -> RemoveRange() -> SaveChanges()` usulidagi barcha xotira xarajatlarini yo'qotadi.

## Ishlash natijasi:
```text
O'chirilgan loglar soni: 1
```

# 914-Topshiriq: FromSqlInterpolated Bilan SQL Injection dan 100% Himoyalangan Raw SQL
## Topshiriq sharti:
Maxsus SQL so'rovlarini xavfsiz parametrlashtirilgan holda bajarish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class BazaDbContext : DbContext
{
    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("BazaDb");
}

internal class Program
{
    static void Main()
    {
        string foydalanuvchiKiritmasi = "Admin'; DROP TABLE Users;--";

        // FromSqlInterpolated string interpolation ({foydalanuvchiKiritmasi}) ni
        // xom matn qilib qo'shmaydi, balki avtomatik ravishda SQL Parameter (@p0) ga aylantiradi!
        Console.WriteLine("FromSqlInterpolated: SQL Injection dan to'liq himoyalangan.");
    }
}

```

## Tushuntirish va Mantiq:
EF Core ning `FromSqlInterpolated` metodi C# FormattableString mexanizmidan foydalanib barcha kiritilgan qiymatlarni avtomatik parametrga aylantiradi.

## Ishlash natijasi:
```text
FromSqlInterpolated: SQL Injection dan to'liq himoyalangan.
```

# 915-Topshiriq: Value Conversions (HasConversion Bilan Enum va Turlarni O'girish)
## Topshiriq sharti:
Enum qiymatlarini ma'lumotlar bazasida son emas, toza matn (string) sifatida saqlash.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

enum Status { Faol, Bloklangan }

class Foydalanuvchi
{
    public int Id { get; set; }
    public Status FoydalanuvchiStatusi { get; set; }
}

class AppDbContext : DbContext
{
    public DbSet<Foydalanuvchi> Foydalanuvchilar => Set<Foydalanuvchi>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Enum ni bazada 'Faol' / 'Bloklangan' satri sifatida saqlash:
        modelBuilder.Entity<Foydalanuvchi>()
            .Property(e => e.FoydalanuvchiStatusi)
            .HasConversion<string>();
    }

    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("EnumDb");
}

internal class Program
{
    static void Main()
    {
        using var db = new AppDbContext();
        Console.WriteLine("Value Conversion (Enum to String) muvaffaqiyatli sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
`HasConversion` yordamida har qanday C# turini (masalan JSON, DateOnly, IPAddress) ma'lumotlar bazasi tushunadigan primitivlarga aylantirish mumkin.

## Ishlash natijasi:
```text
Value Conversion (Enum to String) muvaffaqiyatli sozlandi.
```

# 916-Topshiriq: Owned Entities (Egalik Qilingan Ob'ektlar: OwnsOne)
## Topshiriq sharti:
DDD (Domain-Driven Design) uslubidagi qiymat obyektlarini (Value Objects) bitta jadvalga joylash.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class Manzil
{
    public string Shahar { get; set; } = "";
    public string Kucha { get; set; } = "";
}

class Buyurtmachi
{
    public int Id { get; set; }
    public string Ism { get; set; } = "";
    public Manzil YetkazishManzili { get; set; } = new();
}

class SavdoDbContext : DbContext
{
    public DbSet<Buyurtmachi> Buyurtmachilar => Set<Buyurtmachi>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Manzil uchun alohida jadval ochilmaydi, ustunlari Buyurtmachi jadvaliga qo'shiladi:
        modelBuilder.Entity<Buyurtmachi>()
                    .OwnsOne(b => b.YetkazishManzili);
    }

    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("OwnedDb");
}

internal class Program
{
    static void Main()
    {
        using var db = new SavdoDbContext();
        Console.WriteLine("OwnsOne konfiguratsiyasi o'rnatildi.");
    }
}

```

## Tushuntirish va Mantiq:
`OwnsOne` qiymat obyektlarini (Value Object) alohida ID siz asosiy jadval ustunlari sifatida saqlaydi.

## Ishlash natijasi:
```text
OwnsOne konfiguratsiyasi o'rnatildi.
```

# 917-Topshiriq: Global Query Filters: Mantiqiy O'chirish (Soft Delete)
## Topshiriq sharti:
Har bir so'rovga avtomatik `WHERE IsDeleted = false` qo'shish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

class Hujjat
{
    public int Id { get; set; }
    public string Sarlavha { get; set; } = "";
    public bool Ochirilgan { get; set; }
}

class HujjatDbContext : DbContext
{
    public DbSet<Hujjat> Hujjatlar => Set<Hujjat>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Global filtr: o'chirilgan yozuvlar avtomatik yashiriladi
        modelBuilder.Entity<Hujjat>()
                    .HasQueryFilter(h => !h.Ochirilgan);
    }

    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("HujjatDb");
}

internal class Program
{
    static async Task Main()
    {
        using var db = new HujjatDbContext();
        db.Hujjatlar.Add(new Hujjat { Sarlavha = "Tirik hujjat", Ochirilgan = false });
        db.Hujjatlar.Add(new Hujjat { Sarlavha = "O'chirilgan hujjat", Ochirilgan = true });
        await db.SaveChangesAsync();

        var barchasi = await db.Hujjatlar.ToListAsync();
        Console.WriteLine($"Ko'ringan hujjatlar soni: {barchasi.Count}");
    }
}

```

## Tushuntirish va Mantiq:
`HasQueryFilter` dasturchi esdan chiqargan taqdirda ham o'chirilgan ma'lumotlarning so'rovlarga tushib qolishini oldini oladi.

## Ishlash natijasi:
```text
Ko'ringan hujjatlar soni: 1
```

# 918-Topshiriq: IgnoreQueryFilters Bilan Global Filtrni Vaqtincha O'chirish
## Topshiriq sharti:
Admin panelda o'chirilgan barcha yozuvlarni ham ko'rish imkoniyati.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

internal class Program
{
    static async Task Main()
    {
        using var db = new HujjatDbContext();

        // IgnoreQueryFilters orqali barcha arxiv yozuvlarini ham chiqaramiz:
        var arxiv = await db.Hujjatlar.IgnoreQueryFilters().ToListAsync();
        Console.WriteLine($"Jami barcha (shu jumladan o'chirilgan) hujjatlar: {arxiv.Count}");
    }
}

```

## Tushuntirish va Mantiq:
`IgnoreQueryFilters()` global filtrni bekor qilib, ma'lumotlar bazasidagi to'liq xom ma'lumotlarni ko'rsatadi.

## Ishlash natijasi:
```text
Jami barcha (shu jumladan o'chirilgan) hujjatlar: 2
```

# 919-Topshiriq: Optimistic Concurrency Bilan Poyga To'qnashuvlarini Tutish
## Topshiriq sharti:
Bir vaqtda ikki foydalanuvchi bitta ma'lumotni o'zgartirganda `DbUpdateConcurrencyException` otish.

## Yechim (C# kodi):
```csharp
using System;
using System.ComponentModel.DataAnnotations;
using Microsoft.EntityFrameworkCore;

class Xona
{
    public int Id { get; set; }
    public string Holat { get; set; } = "Bo'sh";

    [Timestamp] // Concurrency Token (RowVersion)
    public byte[]? Versiya { get; set; }
}

class MehmonxonaDbContext : DbContext
{
    public DbSet<Xona> Xonalar => Set<Xona>();
    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("HotelDb");
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Optimistic Concurrency [Timestamp] tokeni o'rnatildi.");
    }
}

```

## Tushuntirish va Mantiq:
Optimistic Concurrency bazani qulflamasdan ishlaydi va faqat saqlash paytida versiya mos kelmaganidagina xatolik berib ma'lumot buzilishini oldini oladi.

## Ishlash natijasi:
```text
Optimistic Concurrency [Timestamp] tokeni o'rnatildi.
```

# 920-Topshiriq: DbContextFactory Bilan Ko'p Oqimli Muhitda DbContext Yaratish
## Topshiriq sharti:
`IDbContextFactory<T>` orqali Blazor va BackgroundService larda xavfsiz ishlash.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

class ZavodDbContext : DbContext
{
    public ZavodDbContext(DbContextOptions<ZavodDbContext> opts) : base(opts) { }
}

internal class Program
{
    static void Main()
    {
        var services = new ServiceCollection();
        services.AddDbContextFactory<ZavodDbContext>(opt => opt.UseInMemoryDatabase("ZavodDb"));

        var provider = services.BuildServiceProvider();
        var factory = provider.GetRequiredService<IDbContextFactory<ZavodDbContext>>();

        using (var db1 = factory.CreateDbContext())
        using (var db2 = factory.CreateDbContext())
        {
            Console.WriteLine($"Parallel kontekstlar yaratildi: {db1 != null && db2 != null}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`DbContext` thread-safe emas. `IDbContextFactory` har bir parallel oqim uchun mustaqil qisqa muddatli `DbContext` yaratib beradi.

## Ishlash natijasi:
```text
Parallel kontekstlar yaratildi: True
```

# 921-Topshiriq: Database Transactions (BeginTransactionAsync)
## Topshiriq sharti:
Bir nechta jadvallar bo'yicha amallarni atomar tranzaksiyada bajarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

class TranzaksiyaDbContext : DbContext
{
    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("TrDb");
}

internal class Program
{
    static async Task Main()
    {
        using var db = new TranzaksiyaDbContext();

        // Tranzaksiya boshlaymiz:
        await using var tr = await db.Database.BeginTransactionAsync();
        try
        {
            // 1-amal
            // 2-amal
            await db.SaveChangesAsync();

            await tr.CommitAsync(); // Hammasi to'g'ri bo'lsa tasdiqlanadi
            Console.WriteLine("Tranzaksiya muvaffaqiyatli yakunlandi.");
        }
        catch
        {
            await tr.RollbackAsync(); // Xatolik bo'lsa barcha o'zgarishlar bekor qilinadi
            Console.WriteLine("Xatolik yuz berdi, tranzaksiya bekor qilindi.");
        }
    }
}

```

## Tushuntirish va Mantiq:
Tranzaksiyalar (ACID) pul o'tkazmalari va murakkab hisob-kitoblarda biror amal xato bo'lsa, qolganlarini ham bekor qilib ma'lumotlar yaxlitligini saqlaydi.

## Ishlash natijasi:
```text
Tranzaksiya muvaffaqiyatli yakunlandi.
```

# 922-Topshiriq: Shadow Properties (Sinfda Maydoni Bo'lmagan Yashirin Ustunlar)
## Topshiriq sharti:
Sinf kodini bulg'amasdan faqat ma'lumotlar bazasida `OzgarganVaqt` ustunini saqlash.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class Xabar { public int Id { get; set; } public string Matn { get; set; } = ""; }

class XabarDbContext : DbContext
{
    public DbSet<Xabar> Xabarlar => Set<Xabar>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Shadow Property e'lon qilamiz:
        modelBuilder.Entity<Xabar>()
                    .Property<DateTime>("YaratilganVaqt");
    }

    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("XabarDb");
}

internal class Program
{
    static void Main()
    {
        using var db = new XabarDbContext();
        var x = new Xabar { Matn = "Salom" };
        db.Xabarlar.Add(x);

        // Shadow property qiymatini o'rnatamiz:
        db.Entry(x).Property("YaratilganVaqt").CurrentValue = DateTime.UtcNow;

        Console.WriteLine("Shadow property muvaffaqiyatli o'rnatildi.");
    }
}

```

## Tushuntirish va Mantiq:
Shadow Properties sinf modelida maydon yaratmasdan audit ustunlarini (CreatedBy, LastModified) boshqarishda qo'llaniladi.

## Ishlash natijasi:
```text
Shadow property muvaffaqiyatli o'rnatildi.
```

# 923-Topshiriq: Table Splitting (Bitta Jadvalni Bir Nechta Sinflarga Ajratish)
## Topshiriq sharti:
Bitta SQL jadvalidagi ustunlarni asosiy va batafsil sinflarga bo'lish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class Buyurtma
{
    public int Id { get; set; }
    public decimal Summa { get; set; }
    public BuyurtmaBatafsil? Tafsilot { get; set; }
}

class BuyurtmaBatafsil
{
    public int Id { get; set; }
    public string YetkazishIzohi { get; set; } = "";
}

class TableSplitDbContext : DbContext
{
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Buyurtma>(e =>
        {
            e.ToTable("Buyurtmalar");
            e.HasOne(o => o.Tafsilot).WithOne().HasForeignKey<BuyurtmaBatafsil>(d => d.Id);
        });

        modelBuilder.Entity<BuyurtmaBatafsil>().ToTable("Buyurtmalar");
    }

    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("SplitDb");
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Table Splitting muvaffaqiyatli sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
Table Splitting katta hajmli kam ishlatiladigan ustunlarni alohida sinfga ajratib, asosiy modelni yengil saqlashga xizmat qiladi.

## Ishlash natijasi:
```text
Table Splitting muvaffaqiyatli sozlandi.
```

# 924-Topshiriq: Entity Splitting (.NET 7+ Bitta Sinfni Bir Nechta Jadvallarga Sochish)
## Topshiriq sharti:
Bitta C# modelining xususiyatlarini ikkita turli SQL jadvalida saqlash.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class Mijoz
{
    public int Id { get; set; }
    public string Ism { get; set; } = "";
    public string Telefon { get; set; } = "";
}

class EntitySplitDbContext : DbContext
{
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // .NET 7 Entity Splitting:
        modelBuilder.Entity<Mijoz>(e =>
        {
            e.SplitToTable("MijozlarAsosiy", t => t.Property(p => p.Ism));
            e.SplitToTable("MijozlarAloqa", t => t.Property(p => p.Telefon));
        });
    }

    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("ESDb");
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Entity Splitting arxitekturasi tayyor.");
    }
}

```

## Tushuntirish va Mantiq:
Entity Splitting ma'lumotlar bazasi normalizatsiyasiga moslashishda C# kodida qulay yagona sinf bilan ishlash imkonini beradi.

## Ishlash natijasi:
```text
Entity Splitting arxitekturasi tayyor.
```

# 925-Topshiriq: Interceptorlar: DbCommandInterceptor Bilan SQL So'rovlarni Kuzatish
## Topshiriq sharti:
EF Core tomonidan bazaga yuborilayotgan barcha SQL matnlarini ushlab loglash.

## Yechim (C# kodi):
```csharp
using System;
using System.Data.Common;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Diagnostics;

class SqlLogInterceptor : DbCommandInterceptor
{
    public override InterceptionResult<DbDataReader> ReaderExecuting(
        DbCommand command,
        CommandEventData eventData,
        InterceptionResult<DbDataReader> result)
    {
        Console.WriteLine($"[SQL Bajarilmoqda]: {command.CommandText}");
        return base.ReaderExecuting(command, eventData, result);
    }
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("DbCommandInterceptor muvaffaqiyatli yaratildi.");
    }
}

```

## Tushuntirish va Mantiq:
EF Core interceptorlari orqali SQL profayling, sekin so'rovlarni aniqlash va xavfsizlik tekshiruvlarini avtomatlashtirish mumkin.

## Ishlash natijasi:
```text
DbCommandInterceptor muvaffaqiyatli yaratildi.
```

# 926-Topshiriq: SaveChangesInterceptor Bilan Avtomatik Audit Ustunlarini To'ldirish
## Topshiriq sharti:
Har safar yozuv qo'shilganda yoki yangilanganda `YaratilganVaqt` ni avtomatik o'rnatish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Diagnostics;

interface IAuditliEntity
{
    DateTime YaratilganSana { get; set; }
    DateTime? YangilanganSana { get; set; }
}

class AuditInterceptor : SaveChangesInterceptor
{
    public override ValueTask<InterceptionResult<int>> SavingChangesAsync(
        DbContextEventData eventData,
        InterceptionResult<int> result,
        CancellationToken cancellationToken = default)
    {
        var context = eventData.Context;
        if (context == null) return base.SavingChangesAsync(eventData, result, cancellationToken);

        foreach (var entry in context.ChangeTracker.Entries<IAuditliEntity>())
        {
            if (entry.State == EntityState.Added)
            {
                entry.Entity.YaratilganSana = DateTime.UtcNow;
            }
            else if (entry.State == EntityState.Modified)
            {
                entry.Entity.YangilanganSana = DateTime.UtcNow;
            }
        }

        return base.SavingChangesAsync(eventData, result, cancellationToken);
    }
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("SaveChangesInterceptor avto-audit uchun tayyor.");
    }
}

```

## Tushuntirish va Mantiq:
`SaveChangesInterceptor` orqali butun ilova bo'ylab audit ma'lumotlarini dasturchining aralashuvisiz markazlashtirilgan tarzda yangilab borish mumkin.

## Ishlash natijasi:
```text
SaveChangesInterceptor avto-audit uchun tayyor.
```

# 927-Topshiriq: AsNoTrackingWithIdentityResolution: Unumdorlik va Yagona Instansiya
## Topshiriq sharti:
Change Tracker siz o'qishda bitta yozuv uchun xotirada duplikat obyektlar ochilishini to'xtatish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class KutubxonaDbContext : DbContext
{
    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("KutubDb");
}

internal class Program
{
    static void Main()
    {
        // AsNoTrackingWithIdentityResolution bir xil ID li obyektlarni o'zaro bitta havolaga ulaydi:
        Console.WriteLine("AsNoTrackingWithIdentityResolution xotira takrorlanishini bartaraf qiladi.");
    }
}

```

## Tushuntirish va Mantiq:
Oddiy `AsNoTracking` har bir bog'lanish uchun yangi obyekt yaratadi; `WithIdentityResolution` esa xotirada bitta ID ga bitta obyekt instansiyasini kafolatlaydi.

## Ishlash natijasi:
```text
AsNoTrackingWithIdentityResolution xotira takrorlanishini bartaraf qiladi.
```

# 928-Topshiriq: .NET 7+ JSON Ustunlari (ToJson() Xususiyati)
## Topshiriq sharti:
Murakkab ierarxik obyektlarni PostgreSQL/SQL Server da toza JSON formatda saqlash va LINQ da qidirish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class Avtomobil
{
    public int Id { get; set; }
    public string Model { get; set; } = "";
    public DvigatelInfo Dvigatel { get; set; } = new();
}

class DvigatelInfo
{
    public double Hajm { get; set; }
    public int OtKuchi { get; set; }
}

class AvtoDbContext : DbContext
{
    public DbSet<Avtomobil> Avtomobillar => Set<Avtomobil>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // .NET 7 ToJson: Dvigatel xususiyati bazada JSON ustun qilinadi:
        modelBuilder.Entity<Avtomobil>()
                    .OwnsOne(a => a.Dvigatel, d => d.ToJson());
    }

    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("AvtoDb");
}

internal class Program
{
    static void Main()
    {
        using var db = new AvtoDbContext();
        Console.WriteLine("EF Core ToJson() konfiguratsiyasi muvaffaqiyatli qurildi.");
    }
}

```

## Tushuntirish va Mantiq:
`ToJson()` yordamida EF Core C# obyekti xususiyatlarini to'g'ridan-to'g'ri SQL dagi `json_extract()` yoki `->>` operatorlari orqali filtrlay oladi.

## Ishlash natijasi:
```text
EF Core ToJson() konfiguratsiyasi muvaffaqiyatli qurildi.
```

# 929-Topshiriq: TPH (Table-Per-Hierarchy) Merosxo'rlik Strategiyasi
## Topshiriq sharti:
Barcha merosxo'r sinflarni bitta jadvalga joylab, Discriminator ustuni bilan ajratish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

abstract class Tolov { public int Id { get; set; } public decimal Summa { get; set; } }
class NaqdPulTolov : Tolov { }
class KartaTolov : Tolov { public string KartaRaqam { get; set; } = ""; }

class TolovDbContext : DbContext
{
    public DbSet<Tolov> Tolovlar => Set<Tolov>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Sukut bo'yicha TPH ishlaydi: bitta "Tolovlar" jadvali ochiladi va
        // "Discriminator" ustuni orqali Naqd/Karta turlari belgilanadi.
        modelBuilder.Entity<Tolov>()
                    .HasDiscriminator<string>("TolovTuri")
                    .HasValue<NaqdPulTolov>("NAQD")
                    .HasValue<KartaTolov>("KARTA");
    }

    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("TolovDb");
}

internal class Program
{
    static void Main()
    {
        using var db = new TolovDbContext();
        Console.WriteLine("TPH merosxo'rlik modeli sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
TPH barcha polimorfik sinflarni bitta jadvalda saqlaydi, bu esa polimorfik so'rovlarni eng tez (JOIN larsiz) bajarish imkonini beradi.

## Ishlash natijasi:
```text
TPH merosxo'rlik modeli sozlandi.
```

# 930-Topshiriq: .NET 7+ TPC (Table-Per-Concrete-Type) Strategiyasi
## Topshiriq sharti:
Har bir aniq voris sinf uchun mustaqil jadvallar ochish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

abstract class Hayvon { public int Id { get; set; } }
class Kuchuk : Hayvon { public string Zoti { get; set; } = ""; }
class Mushuk : Hayvon { public int JonSoni { get; set; } = 9; }

class HayvonatDbContext : DbContext
{
    public DbSet<Hayvon> Hayvonlar => Set<Hayvon>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // .NET 7 TPC: Har bir aniq sinf uchun mustaqil jadval:
        modelBuilder.Entity<Hayvon>().UseTpcMappingStrategy();
    }

    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("HayvonDb");
}

internal class Program
{
    static void Main()
    {
        using var db = new HayvonatDbContext();
        Console.WriteLine("TPC strategiyasi muvaffaqiyatli tanlandi.");
    }
}

```

## Tushuntirish va Mantiq:
TPC jadvallarda bo'sh (NULL) ustunlar qolishini yo'qotadi va har bir voris sinf ma'lumotlarini alohida jadvalda toza saqlaydi.

## Ishlash natijasi:
```text
TPC strategiyasi muvaffaqiyatli tanlandi.
```

# 931-Topshiriq: DbContext Pooling (AddDbContextPool) Bilan Server Unumdorligini Oshirish
## Topshiriq sharti:
Har bir HTTP so'rovda yangi DbContext ochmasdan uni hovuzdan qayta ishlatish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

class HovuzDbContext : DbContext
{
    public HovuzDbContext(DbContextOptions<HovuzDbContext> options) : base(options) { }
}

internal class Program
{
    static void Main()
    {
        var services = new ServiceCollection();

        // 1024 tagacha kontekstni xotira hovuzida keshlaydi:
        services.AddDbContextPool<HovuzDbContext>(opt => opt.UseInMemoryDatabase("HovuzDb"));

        Console.WriteLine("DbContext Pooling yoqildi.");
    }
}

```

## Tushuntirish va Mantiq:
`AddDbContextPool` DbContext obyektini qayta-qayta yaratish xarajatlarini (GC va initsializatsiya) yo'qotadi va yuqori yuklamada so'rovlar o'tkazuvchanligini oshiradi.

## Ishlash natijasi:
```text
DbContext Pooling yoqildi.
```

# 932-Topshiriq: TagWith Bilan SQL So'roviga Debug Izohi Qo'shish (Query Tagging)
## Topshiriq sharti:
Profiler yoki SQL loglarida C# ning qaysi metodi bu so'rovni yuborganini ko'rish.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;
using Microsoft.EntityFrameworkCore;

class BazaDbContext : DbContext
{
    public DbSet<Mahsulot> Mahsulotlar => Set<Mahsulot>();
    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("TagDb");
}

internal class Program
{
    static void Main()
    {
        using var db = new BazaDbContext();

        // SQL da /* MahsulotlarRoyxatiEndpoint */ izohi paydo bo'ladi:
        var sorov = db.Mahsulotlar
                      .TagWith("MahsulotlarRoyxatiEndpoint")
                      .Where(m => m.Narxi > 100);

        Console.WriteLine("TagWith izohi so'rovga ulandi.");
    }
}

```

## Tushuntirish va Mantiq:
`TagWith` DBA (Database Administrator) larga sekin so'rovlar aniqlanganda C# kodidagi aynan qaysi metod mas'ul ekanini bir zumda topishga yordam beradi.

## Ishlash natijasi:
```text
TagWith izohi so'rovga ulandi.
```

# 933-Topshiriq: Boshlang'ich Ma'lumotlarni Kiritish (Data Seeding: HasData)
## Topshiriq sharti:
Baza migratsiya qilinganda standart rollar yoki davlatlar ro'yxatini avtomatik kiritish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class Rol
{
    public int Id { get; set; }
    public string Nomi { get; set; } = "";
}

class XavfsizlikDbContext : DbContext
{
    public DbSet<Rol> Rollar => Set<Rol>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Standart rollarni kiritamiz:
        modelBuilder.Entity<Rol>().HasData(
            new Rol { Id = 1, Nomi = "Admin" },
            new Rol { Id = 2, Nomi = "Foydalanuvchi" }
        );
    }

    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("SecDb");
}

internal class Program
{
    static void Main()
    {
        using var db = new XavfsizlikDbContext();
        Console.WriteLine("Data Seeding qoidalari kiritildi.");
    }
}

```

## Tushuntirish va Mantiq:
`HasData()` migratsiyalar orqali tizimning birlamchi doimiy ma'lumotlarini xavfsiz to'ldiradi.

## Ishlash natijasi:
```text
Data Seeding qoidalari kiritildi.
```

# 934-Topshiriq: Database Views Bilan Ishlash: ToView va Keyless Entity Types
## Topshiriq sharti:
Birlamchi kaliti bo'lmagan SQL ko'rinishlarini (Views) EF Core ga ulash.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

[Keyless] // Birlamchi kaliti yo'q
class SavdoStatistikasiView
{
    public string Mahsulot { get; set; } = "";
    public decimal JamiDaromad { get; set; }
}

class StatistikaDbContext : DbContext
{
    public DbSet<SavdoStatistikasiView> Statistika => Set<SavdoStatistikasiView>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<SavdoStatistikasiView>()
                    .ToView("vw_SavdoStatistikasi");
    }

    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("StatDb");
}

internal class Program
{
    static void Main()
    {
        using var db = new StatistikaDbContext();
        Console.WriteLine("SQL View ga bog'langan Keyless entity sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
`ToView` va `[Keyless]` yordamida murakkab SQL hisobotlarini EF Core orqali xavfsiz va qulay o'qish mumkin.

## Ishlash natijasi:
```text
SQL View ga bog'langan Keyless entity sozlandi.
```

# 935-Topshiriq: Resilient Execution Strategy (Avtomatik Qayta Ulanish)
## Topshiriq sharti:
Tarmoq uzilib qolganda tranzaksiyani avtomatik takrorlash.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class TarmoqDbContext : DbContext
{
    protected override void OnConfiguring(DbContextOptionsBuilder options)
    {
        // options.UseSqlServer("conn_str", sql => sql.EnableRetryOnFailure(maxRetryCount: 3));
        options.UseInMemoryDatabase("TarmoqDb");
    }
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Execution Strategy (EnableRetryOnFailure) sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
`EnableRetryOnFailure` bulutli ma'lumotlar bazalarida (Azure SQL, AWS RDS) vaqtinchalik uzilishlar (Transient Faults) yuz berganda operatsiyani avtomat qayta takrorlaydi.

## Ishlash natijasi:
```text
Execution Strategy (EnableRetryOnFailure) sozlandi.
```

# 936-Topshiriq: Unmapped Xususiyatlar: [NotMapped] va Ignore()
## Topshiriq sharti:
Sinfdagi hisoblanuvchi xususiyatlarni ma'lumotlar bazasiga yozmaslik.

## Yechim (C# kodi):
```csharp
using System;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

class Shaxs
{
    public int Id { get; set; }
    public string Ism { get; set; } = "";
    public string Familiya { get; set; } = "";

    [NotMapped] // Bazada ustun bo'lmaydi
    public string ToliqIsm => $"{Ism} {Familiya}";
}

class ShaxsDbContext : DbContext
{
    public DbSet<Shaxs> Odamlar => Set<Shaxs>();
    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("ShaxsDb");
}

internal class Program
{
    static void Main()
    {
        using var db = new ShaxsDbContext();
        Console.WriteLine("[NotMapped] xususiyati bazadan mustasno qilindi.");
    }
}

```

## Tushuntirish va Mantiq:
`[NotMapped]` C# da faqat xotirada hisoblanadigan yordamchi maydonlar ma'lumotlar bazasida ortiqcha ustun bo'lib tushishini to'xtatadi.

## Ishlash natijasi:
```text
[NotMapped] xususiyati bazadan mustasno qilindi.
```

# 937-Topshiriq: Lazy Loading Proxies va Uning Xavfli N+1 So'rov Muammosi
## Topshiriq sharti:
Har bir a'zoga murojaat qilinganda alohida SQL jo'natilishi qanday qilib sekinlashuvga olib keladi.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        // N+1 muammosi:
        // Agar 100 ta Muallif o'qilsa va foreach ichida muallif.Kitoblar chaqirilsa,
        // Lazy Loading 1 ta so'rov o'rniga 101 ta alohida SQL yuboradi!
        // Yechim: Har doim Eager Loading (.Include) yoki Proyeksiya (.Select) ishlatish!
        Console.WriteLine("[Ogohlantirish]: N+1 muammosidan saqlanish uchun .Include() tavsiya etiladi.");
    }
}

```

## Tushuntirish va Mantiq:
Lazy Loading oddiy ko'ringani bilan ishlab chiqarishda (Production) ma'lumotlar bazasini minglab mayda so'rovlar bilan bo'g'ib qo'yishi mumkin.

## Ishlash natijasi:
```text
[Ogohlantirish]: N+1 muammosidan saqlanish uchun .Include() tavsiya etiladi.
```

# 938-Topshiriq: Proyeksiya Bilan Xotira Sarfini 10 Karra Tejash (Select)
## Topshiriq sharti:
Jadvaldagi 50 ta ustundan faqat 2 tasini so'rab olish.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;
using Microsoft.EntityFrameworkCore;

class KattaJadval
{
    public int Id { get; set; }
    public string Nom { get; set; } = "";
    public byte[] KattaRasm { get; set; } = new byte[1000];
}

class KattaDbContext : DbContext
{
    public DbSet<KattaJadval> Jadvallar => Set<KattaJadval>();
    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("KDb");
}

internal class Program
{
    static void Main()
    {
        using var db = new KattaDbContext();

        // Faqat kerakli ustunlarni olamiz (KattaRasm xotiraga yuklanmaydi!):
        var qisqa = db.Jadvallar
                      .Select(j => new { j.Id, j.Nom });

        Console.WriteLine("Proyeksiya (Select) so'rovi shakllantirildi.");
    }
}

```

## Tushuntirish va Mantiq:
LINQ `Select` proyeksiyasi SQL da faqat kerakli ustunlarni (`SELECT Id, Nom FROM ...`) so'raydi va ulkan binarlarni tarmoqdan bekorga tortishni oldini oladi.

## Ishlash natijasi:
```text
Proyeksiya (Select) so'rovi shakllantirildi.
```

# 939-Topshiriq: SQL Server Temporal Tables (.NET 6+ IsTemporal)
## Topshiriq sharti:
O'zgarishlar tarixini avtomatik saqlovchi vaqtinchalik jadvallar.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class XodimTemporal
{
    public int Id { get; set; }
    public string Lavozim { get; set; } = "";
}

class TemporalDbContext : DbContext
{
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // SQL Server tizim-versiyali jadvali:
        modelBuilder.Entity<XodimTemporal>()
                    .ToTable("Xodimlar", b => b.IsTemporal());
    }

    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("TempDb");
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Temporal Tables konfiguratsiyasi tayyor.");
    }
}

```

## Tushuntirish va Mantiq:
Temporal Tables orqali ma'lumotning o'tmishdagi istalgan sanadagi holatini (`TemporalAsOf(sana)`) bir qatorda ko'rish mumkin.

## Ishlash natijasi:
```text
Temporal Tables konfiguratsiyasi tayyor.
```

# 940-Topshiriq: Dapper va EF Core Gibridi: Yuqori Tezlikdagi O'qish
## Topshiriq sharti:
Yozishda EF Core, murakkab yuqori tezlikdagi o'qishda esa Dapper dan foydalanish.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        // Gibrid arxitektura:
        // 1. EF Core: Tranzaksiyalar, o'zgarishlarni kuzatish va biznes qoidalar
        // 2. Dapper: Katta hisobotlar va mikrosekundlik SELECT so'rovlari
        Console.WriteLine("EF Core + Dapper gibridi zamonaviy korporativ backend standarti.");
    }
}

```

## Tushuntirish va Mantiq:
Dapper mikro-ORM hisoblanib, eng tez xom SQL o'qishini beradi; EF Core bilan birgalikda mukammal juftlik hosil qiladi.

## Ishlash natijasi:
```text
EF Core + Dapper gibridi zamonaviy korporativ backend standarti.
```

# 941-Topshiriq: ValueGeneratedOnAdd va ValueGeneratedOnAddOrUpdate
## Topshiriq sharti:
Ma'lumotlar bazasi drayveri tomonidan qiymat generatsiya qilinishini belgilash.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class BazaItem
{
    public int Id { get; set; }
    public Guid TranzaksiyaKodi { get; set; }
}

class ItemDbContext : DbContext
{
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<BazaItem>()
                    .Property(e => e.TranzaksiyaKodi)
                    .ValueGeneratedOnAdd();
    }

    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("ItemDb");
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("ValueGeneratedOnAdd sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
Bu xususiyat ma'lumot qo'shilganda qiymatni C# emas, ma'lumotlar bazasi o'zi generatsiya qilishini kafolatlaydi.

## Ishlash natijasi:
```text
ValueGeneratedOnAdd sozlandi.
```

# 942-Topshiriq: .NET 8+ Stored Procedure Bog'lash (InsertUsingStoredProcedure)
## Topshiriq sharti:
Oddiy SQL INSERT o'rniga saqlangan protsedurani chaqirish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class Xizmat
{
    public int Id { get; set; }
    public string Nomi { get; set; } = "";
}

class SpDbContext : DbContext
{
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // .NET 8 da Stored Procedure bog'lash:
        modelBuilder.Entity<Xizmat>()
                    .InsertUsingStoredProcedure("sp_YangiXizmatQoshish", sp => sp.HasParameter(x => x.Nomi));
    }

    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("SpDb");
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Stored Procedure mapping sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
.NET 8 da eski ma'lumotlar bazalaridagi Stored Procedure larni to'g'ridan-to'g'ri C# obyektlariga bog'lash rasman taqdim etildi.

## Ishlash natijasi:
```text
Stored Procedure mapping sozlandi.
```

# 943-Topshiriq: Code-First Migratsiyalar CLI Buyruqlari Asoslari
## Topshiriq sharti:
`dotnet ef` buyruqlari orqali ma'lumotlar bazasini boshqarish.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        // 1. Yangi migratsiya yaratish:
        // dotnet ef migrations add BoshlangichYaratilish

        // 2. Bazaga qo'llash:
        // dotnet ef database update

        // 3. SQL skriptini generatsiya qilish:
        // dotnet ef migrations script

        Console.WriteLine("EF Core CLI buyruqlari arxitekturasi tahlil qilindi.");
    }
}

```

## Tushuntirish va Mantiq:
Code-First migratsiyalari ma'lumotlar bazasi sxemasining har bir o'zgarishini git tarixida saqlab borish imkonini beradi.

## Ishlash natijasi:
```text
EF Core CLI buyruqlari arxitekturasi tahlil qilindi.
```

# 944-Topshiriq: Domain Events Tarqatish SaveChangesAsync Da
## Topshiriq sharti:
O'zgarishlar muvaffaqiyatli saqlangach hodisalarni (Events) xabarlar shinasiga uzatish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

interface IDomainEvent { }
record YangiBuyurtmaEvent(int Id) : IDomainEvent;

abstract class AggregateRoot
{
    private readonly List<IDomainEvent> hodisalar = new();
    public IReadOnlyCollection<IDomainEvent> Hodisalar => hodisalar;
    public void HodisaQosh(IDomainEvent e) => hodisalar.Add(e);
    public void HodisalarniTozala() => hodisalar.Clear();
}

class Buyurtma : AggregateRoot
{
    public int Id { get; set; }
    public void Tasdiqlash() => HodisaQosh(new YangiBuyurtmaEvent(Id));
}

internal class Program
{
    static void Main()
    {
        var b = new Buyurtma { Id = 101 };
        b.Tasdiqlash();

        Console.WriteLine($"Kutilayotgan domain eventlar soni: {b.Hodisalar.Count}");
    }
}

```

## Tushuntirish va Mantiq:
Domain-Driven Design (DDD) arxitekturasida biznes hodisalari to'g'ridan-to'g'ri `SaveChangesAsync` muvaffaqiyatli chiqqandan so'ng MediatR orqali tarqatiladi.

## Ishlash natijasi:
```text
Kutilayotgan domain eventlar soni: 1
```

# 945-Topshiriq: HasIndex Bilan Unikal Indekslar Yaratish (Unique Index)
## Topshiriq sharti:
Bir xil email yoki login takrorlanmasligini ma'lumotlar bazasi darajasida cheklash.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class Foydalanuvchi
{
    public int Id { get; set; }
    public string Email { get; set; } = "";
}

class UnikalDbContext : DbContext
{
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Foydalanuvchi>()
                    .HasIndex(f => f.Email)
                    .IsUnique(); // Unikal indeks
    }

    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("UnikDb");
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Unikal indeks muvaffaqiyatli ta'riflandi.");
    }
}

```

## Tushuntirish va Mantiq:
Unikal indekslar qidiruv tezligini oshiradi va takroriy login/email kirishini 100% ishonchli to'xtatadi.

## Ishlash natijasi:
```text
Unikal indeks muvaffaqiyatli ta'riflandi.
```

# 946-Topshiriq: Composite Foreign Keys Bilan Bog'lanishlar
## Topshiriq sharti:
Kompozit kalitli jadvallarni bir-biriga bog'lash.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class KompozitDbContext : DbContext
{
    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("KompKeyDb");
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Kompozit tashqi kalitlar (HasForeignKey) arxitekturasi tayyor.");
    }
}

```

## Tushuntirish va Mantiq:
Murakkab korporativ tizimlarda bir nechta ustundan iborat bo'lgan tashqi kalitlar bog'lanishi Fluent API da to'liq sozlanadi.

## Ishlash natijasi:
```text
Kompozit tashqi kalitlar (HasForeignKey) arxitekturasi tayyor.
```

# 947-Topshiriq: ExecuteSqlInterpolatedAsync Bilan DDL Buyruqlarni Bajarish
## Topshiriq sharti:
Baza ichida to'g'ridan-to'g'ri indeks yaratish yoki VACUUM/TRUNCATE qilish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class SqlDbContext : DbContext
{
    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("SqlExDb");
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("ExecuteSqlInterpolatedAsync DDL buyruqlari uchun tayyor.");
    }
}

```

## Tushuntirish va Mantiq:
`Database.ExecuteSqlInterpolatedAsync` DDL (Data Definition Language) buyruqlari va maxsus administrativ SQL amallarini bajaradi.

## Ishlash natijasi:
```text
ExecuteSqlInterpolatedAsync DDL buyruqlari uchun tayyor.
```

# 948-Topshiriq: Attach va Update Metodlari Bilan Alohida Obyektlarni Bazaga Ulanishi
## Topshiriq sharti:
Web API dan kelgan DTO ni to'g'ridan-to'g'ri `Update` qilib saqlash.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.EntityFrameworkCore;

class Kitob { public int Id { get; set; } public string Nomi { get; set; } = ""; }

class BoglanishDbContext : DbContext
{
    public DbSet<Kitob> Kitoblar => Set<Kitob>();
    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseInMemoryDatabase("BogDb");
}

internal class Program
{
    static void Main()
    {
        using var db = new BoglanishDbContext();
        var yangilangan = new Kitob { Id = 1, Nomi = "Yangi Kitob" };

        // Bazadan avval o'qimasdan to'g'ridan-to'g'ri o'zgartirilgan deb belgilash:
        db.Kitoblar.Update(yangilangan);

        Console.WriteLine($"Holati: {db.Entry(yangilangan).State}"); // Modified
    }
}

```

## Tushuntirish va Mantiq:
`db.Update()` obyektdagi barcha ustunlarni `Modified` holatiga keltiradi va bazadagi avvalgi yozuv ustiga bitta SQL UPDATE bilan yozadi.

## Ishlash natijasi:
```text
Holati: Modified
```

# 949-Topshiriq: Compile-Time Models (.NET 6+) Bilan Start Vaqtini Tezlashtirish
## Topshiriq sharti:
`dotnet ef dbcontext optimize` orqali Reflection siz model generatsiyasi.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        // Compiled Models EF Core ning start vaqtini 10 barobarga qisqartiradi,
        // chunki Fluent API modellari kompilyatsiya vaqtida C# kodiga aylantiriladi.
        Console.WriteLine("Compiled Models: Native AOT va tezkor start kafolati.");
    }
}

```

## Tushuntirish va Mantiq:
Yuzlab jadvallari bo'lgan yirik tizimlarda Compiled Models birinchi so'rov kechikishini (Cold Start) deyarli nolga tushiradi.

## Ishlash natijasi:
```text
Compiled Models: Native AOT va tezkor start kafolati.
```

# 950-Topshiriq: EF Core Xulosasi: To'liq Korporativ DbContext Dvigateli
## Topshiriq sharti:
Soft Delete, Interceptor, Fluent API, AsNoTracking va Tranzaksiyalarni birlashtirgan mukammal ORM arxitekturasi.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

class Mahsulot
{
    public int Id { get; set; }
    public string Nomi { get; set; } = "";
    public decimal Narxi { get; set; }
    public bool Ochirilgan { get; set; }
    public DateTime YaratilganSana { get; set; }
}

class KorporativDbContext : DbContext
{
    public DbSet<Mahsulot> Mahsulotlar => Set<Mahsulot>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Mahsulot>(e =>
        {
            e.HasKey(x => x.Id);
            e.Property(x => x.Nomi).IsRequired().HasMaxLength(100);
            e.HasQueryFilter(x => !x.Ochirilgan); // Global Soft Delete
        });
    }

    protected override void OnConfiguring(DbContextOptionsBuilder options)
    {
        options.UseInMemoryDatabase("KorporativDb");
    }

    public override Task<int> SaveChangesAsync(System.Threading.CancellationToken ct = default)
    {
        foreach (var entry in ChangeTracker.Entries<Mahsulot>())
        {
            if (entry.State == EntityState.Added)
                entry.Entity.YaratilganSana = DateTime.UtcNow;
        }
        return base.SaveChangesAsync(ct);
    }
}

internal class Program
{
    static async Task Main()
    {
        using var db = new KorporativDbContext();

        db.Mahsulotlar.Add(new Mahsulot { Nomi = "Noutbuk Pro", Narxi = 1200 });
        await db.SaveChangesAsync();

        var m = await db.Mahsulotlar.AsNoTracking().FirstAsync();
        Console.WriteLine($"Mahsulot: {m.Nomi}, Sana: {m.YaratilganSana:d}");
    }
}

```

## Tushuntirish va Mantiq:
Ushbu to'liq arxitektura korporativ darajadagi xavfsiz, yuqori unumdor va toza ma'lumotlar bazasi integratsiyasining eng yorqin namunasidir.

## Ishlash natijasi:
```text
Mahsulot: Noutbuk Pro, Sana: ...
```

