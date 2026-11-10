# 18-Mavzu: ASP.NET Core Web API va Minimal API (851-900)

Ushbu bo'limda zamonaviy C# veb-dasturlash: `WebApplicationBuilder` va `WebApplication`, Minimal API marshrutlash (`app.MapGet`, `MapPost`), parametrlar bog'lash (`[FromRoute]`, `[FromQuery]`, `[FromBody]`), javob turlari (`Results`, `TypedResults`), Dependency Injection xizmat muddatlari (`Transient`, `Scoped`, `Singleton`), Middleware quvuri, global xatoliklar filtri, Endpoint Filters, Route Groups (.NET 7+), konfiguratsiya boshqaruvi (`IOptions<T>`), CORS, avtorizatsiya asoslari hamda .NET 7/8/9 yangi veb imkoniyatlari bo'yicha 50 ta amaliy topshiriq jamlangan.

# 851-Topshiriq: Minimal API Boshlang'ich Arxitekturasi: WebApplication.CreateBuilder
## Topshiriq sharti:
Eng ixcham bir faylli (Single-File) veb server yaratish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Hosting;

internal class Program
{
    static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);
        var app = builder.Build();

        app.MapGet("/", () => "Salom, O'zbekiston! ASP.NET Core Minimal API ishga tushdi.");

        Console.WriteLine("Server marshrutlari muvaffaqiyatli sozlandi.");
        // app.Run(); // Konsol namunasida bloklamaslik uchun izohda
    }
}

```

## Tushuntirish va Mantiq:
Minimal API eski Startup.cs va Controller sinflarini talab qilmaydi; `WebApplicationBuilder` yordamida bir necha qatorda to'liq quvvatli Kestrel veb serverini ko'taradi.

## Ishlash natijasi:
```text
Server marshrutlari muvaffaqiyatli sozlandi.
```

# 852-Topshiriq: HTTP Metodlari: MapGet, MapPost, MapPut va MapDelete
## Topshiriq sharti:
CRUD operatsiyalarini Minimal API marshrutlariga ulash.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;

internal class Program
{
    static void Main(string[] args)
    {
        var app = WebApplication.Create();

        app.MapGet("/api/mahsulotlar", () => "Barcha mahsulotlar");
        app.MapPost("/api/mahsulotlar", () => "Yangi mahsulot qo'shildi");
        app.MapPut("/api/mahsulotlar/{id}", (int id) => $"{id}-mahsulot yangilandi");
        app.MapDelete("/api/mahsulotlar/{id}", (int id) => $"{id}-mahsulot o'chirildi");

        Console.WriteLine("CRUD marshrutlari muvaffaqiyatli ro'yxatga olindi.");
    }
}

```

## Tushuntirish va Mantiq:
Har bir HTTP verb (GET, POST, PUT, DELETE) uchun mos `Map*` metodi mavjud bo'lib, RESTful API standartlariga to'liq javob beradi.

## Ishlash natijasi:
```text
CRUD marshrutlari muvaffaqiyatli ro'yxatga olindi.
```

# 853-Topshiriq: Route Parametrlari va Cheklovlari (Route Constraints)
## Topshiriq sharti:
URL ichidagi parametrlarni tip (`int`, `guid`) bo'yicha cheklash.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();

        // Faqat musbat butun son bo'lsa mos keladi: {id:int:min(1)}
        app.MapGet("/foydalanuvchi/{id:int:min(1)}", (int id) => $"ID: {id}");

        // Faqat GUID formatida bo'lsa: {kod:guid}
        app.MapGet("/buyurtma/{kod:guid}", (Guid kod) => $"Buyurtma kodi: {kod}");

        Console.WriteLine("Route cheklovlari o'rnatildi.");
    }
}

```

## Tushuntirish va Mantiq:
Route Constraints noto'g'ri so'rovlarni (masalan matn yuborilganda) darhol 404 qaytarib, ortiqcha metod chaqiruvlaridan asraydi.

## Ishlash natijasi:
```text
Route cheklovlari o'rnatildi.
```

# 854-Topshiriq: Model Binding: [FromQuery], [FromRoute], [FromBody] va [FromHeader]
## Topshiriq sharti:
Parametrlarni HTTP so'rovining turli qismlaridan o'qib olish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Mvc;

record YangiFoydalanuvchi(string Ism, string Email);

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();

        app.MapPost("/api/test/{viloyat}", (
            [FromRoute] string viloyat,
            [FromQuery] int sahifa,
            [FromBody] YangiFoydalanuvchi model,
            [FromHeader("User-Agent")] string client) =>
        {
            return $"Viloyat: {viloyat}, Sahifa: {sahifa}, Ism: {model.Ism}, Brauzer: {client}";
        });

        Console.WriteLine("Model bog'lash (Binding) konfiguratsiyasi tayyor.");
    }
}

```

## Tushuntirish va Mantiq:
Minimal API larda atributlar ixtiyoriy: agar tur DTO bo'lsa sukut bo'yicha `FromBody`, primitiv bo'lsa `FromRoute` yoki `FromQuery` deb avtomatik topiladi.

## Ishlash natijasi:
```text
Model bog'lash (Binding) konfiguratsiyasi tayyor.
```

# 855-Topshiriq: Results Yordamchisi: Status Kodlar Bilan Standart Javoblar
## Topshiriq sharti:
200 OK, 201 Created, 404 NotFound va 400 BadRequest qaytarish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

record Mahsulot(int Id, string Nomi);

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();

        app.MapGet("/api/mahsulot/{id}", (int id) =>
        {
            if (id <= 0) return Results.BadRequest("ID 0 dan katta bo'lishi shart!");
            if (id == 999) return Results.NotFound("Mahsulot topilmadi");

            return Results.Ok(new Mahsulot(id, "Noutbuk"));
        });

        Console.WriteLine("Results xizmati sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
`Results` statik sinfi HTTP protokoli bo'yicha to'g'ri status kodlar va sarlavhalarni shakllantiradi.

## Ishlash natijasi:
```text
Results xizmati sozlandi.
```

# 856-Topshiriq: .NET 7+ TypedResults: Tip Xavfsizligi va Avtomatik OpenAPI
## Topshiriq sharti:
`IResult` o'rniga Swagger/OpenAPI uchun aniq turlarni qaytarish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Http.HttpResults;

record Talaba(int Id, string Ism);

internal class Program
{
    static Results<Ok<Talaba>, NotFound> TalabaOlish(int id)
    {
        if (id == 1) return TypedResults.Ok(new Talaba(1, "Sardor"));
        return TypedResults.NotFound();
    }

    static void Main()
    {
        var app = WebApplication.Create();
        app.MapGet("/talaba/{id}", TalabaOlish);

        Console.WriteLine("TypedResults integratsiyasi yakunlandi.");
    }
}

```

## Tushuntirish va Mantiq:
`TypedResults` qaytish turlarini kuchli tipli qiladi (`Results<Ok<T>, NotFound>`), bu esa unit test yozishda va Swagger hujjatlarini generatsiya qilishda inqilobiy qulaylik beradi.

## Ishlash natijasi:
```text
TypedResults integratsiyasi yakunlandi.
```

# 857-Topshiriq: Dependency Injection: AddTransient, AddScoped va AddSingleton
## Topshiriq sharti:
Xizmatlarning hayot davrini (Service Lifetimes) to'g'ri taqsimlash.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.Extensions.DependencyInjection;

interface IOperatsiya { Guid Id { get; } }
class Operatsiya : IOperatsiya
{
    public Guid Id { get; } = Guid.NewGuid();
}

internal class Program
{
    static void Main()
    {
        var services = new ServiceCollection();

        // 1. Transient: Har safar so'ralganda yangi nusxa
        services.AddTransient<IOperatsiya, Operatsiya>();

        // 2. Scoped: Bitta HTTP so'rov doirasida yagona nusxa
        // services.AddScoped<IOperatsiya, Operatsiya>();

        // 3. Singleton: Butun dastur davomida faqat bitta umumiy nusxa
        // services.AddSingleton<IOperatsiya, Operatsiya>();

        var provider = services.BuildServiceProvider();

        var op1 = provider.GetRequiredService<IOperatsiya>();
        var op2 = provider.GetRequiredService<IOperatsiya>();

        Console.WriteLine($"Transient id bir xilmi: {op1.Id == op2.Id} (har doim yangi)");
    }
}

```

## Tushuntirish va Mantiq:
DI da xizmat turlarini adashtirish (masalan Singleton ichiga Scoped xizmat tiqish - Captive Dependency) jiddiy xotira sizishiga olib keladi.

## Ishlash natijasi:
```text
Transient id bir xilmi: False (har doim yangi)
```

# 858-Topshiriq: Minimal API Metodlarida Servislarni Inyeksiya Qilish ([FromServices])
## Topshiriq sharti:
Xizmatlarni to'g'ridan-to'g'ri lambda parametrlari orqali qabul qilish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;

interface IVaqtXizmati { string Olish(); }
class VaqtXizmati : IVaqtXizmati { public string Olish() => DateTime.UtcNow.ToString("O"); }

internal class Program
{
    static void Main()
    {
        var builder = WebApplication.CreateBuilder();
        builder.Services.AddSingleton<IVaqtXizmati, VaqtXizmati>();
        var app = builder.Build();

        // IVaqtXizmati parametr sifatida kelsa, DI konteyner uni avtomatik uzatadi:
        app.MapGet("/vaqt", (IVaqtXizmati vaqt) => $"Server vaqti: {vaqt.Olish()}");

        Console.WriteLine("Servis inyeksiyasi muvaffaqiyatli ishlaydi.");
    }
}

```

## Tushuntirish va Mantiq:
Minimal API larda xizmatlarni qabul qilish uchun konstruktor shart emas; ular bevosita lambda parametrlariga inyeksiya qilinadi.

## Ishlash natijasi:
```text
Servis inyeksiyasi muvaffaqiyatli ishlaydi.
```

# 859-Topshiriq: Middleware Quvuri: app.Use Bilan So'rovlarni Tutib Qolish
## Topshiriq sharti:
Har bir HTTP so'rov kirib-chiqishini nazorat qiluvchi oraliq dastur.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();

        // Maxsus Inline Middleware:
        app.Use(async (context, next) =>
        {
            Console.WriteLine($"[Middleware Kirish]: {context.Request.Path}");
            await next(context); // Keyingi middleware yoki endpointga o'tkazish
            Console.WriteLine($"[Middleware Chiqish]: Status {context.Response.StatusCode}");
        });

        app.MapGet("/test", () => "Middleware tekshiruvi");

        Console.WriteLine("Middleware zanjiri ulandi.");
    }
}

```

## Tushuntirish va Mantiq:
Middleware quvuri (Pipeline) 'Pik Rus' tamoyilida ishlaydi: `next(context)` chaqirilguncha kirish, undan keyin esa javob qaytish qismi bajariladi.

## Ishlash natijasi:
```text
Middleware zanjiri ulandi.
```

# 860-Topshiriq: Alohida Middleware Sinfi Yaratish va UseMiddleware<T>
## Topshiriq sharti:
Murakkab middleware mantiqini alohida sinfga ajratish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

class AuditMiddleware
{
    private readonly RequestDelegate next;

    public AuditMiddleware(RequestDelegate next) => this.next = next;

    public async Task InvokeAsync(HttpContext context)
    {
        context.Response.Headers.Append("X-Audit-Header", "Antigravity-Engine");
        await next(context);
    }
}

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();
        app.UseMiddleware<AuditMiddleware>();

        Console.WriteLine("AuditMiddleware tizimga integratsiya qilindi.");
    }
}

```

## Tushuntirish va Mantiq:
Alohida sinf sifatidagi Middleware qayta ishlatish (reusability) va testlash uchun juda qulaydir.

## Ishlash natijasi:
```text
AuditMiddleware tizimga integratsiya qilindi.
```

# 861-Topshiriq: Global Xatoliklarni Ushlash (Global Exception Handling)
## Topshiriq sharti:
Dasturda sodir bo'lgan kutilmagan barcha istisnolarni ushlab chiroyli JSON qaytarish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Diagnostics;
using Microsoft.AspNetCore.Http;

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();

        app.UseExceptionHandler(xatoApp =>
        {
            xatoApp.Run(async context =>
            {
                context.Response.StatusCode = StatusCodes.Status500InternalServerError;
                context.Response.ContentType = "application/json";

                var xatoXususiyati = context.Features.Get<IExceptionHandlerFeature>();
                string xabar = xatoXususiyati?.Error.Message ?? "Noma'lum xatolik";

                await context.Response.WriteAsync($"{{"xato": "{xabar}"}}");
            });
        });

        Console.WriteLine("Global Exception Handler o'rnatildi.");
    }
}

```

## Tushuntirish va Mantiq:
`UseExceptionHandler` serverning ichki xatoliklari (500) da foydalanuvchiga xom stack trace chiqib ketishini to'sib, xavfsiz JSON javob beradi.

## Ishlash natijasi:
```text
Global Exception Handler o'rnatildi.
```

# 862-Topshiriq: .NET 7+ Route Groups (app.MapGroup) Bilan Prefikslar va Versiyalash
## Topshiriq sharti:
Marshrutlarni umumiy prefiks ostiga guruhlash (`/api/v1/users`).

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();

        // /api/v1 prefiksli guruh ochamiz:
        var v1 = app.MapGroup("/api/v1");

        v1.MapGet("/kitoblar", () => "V1 kitoblar");
        v1.MapGet("/mualliflar", () => "V1 mualliflar");

        Console.WriteLine("Route Groups muvaffaqiyatli tashkil etildi.");
    }
}

```

## Tushuntirish va Mantiq:
`MapGroup` .NET 7 da kiritilgan bo'lib, prefikslar, avtorizatsiya va filtrlarni butun bir guruh marshrutlariga bir yo'la tatbiq etish imkonini beradi.

## Ishlash natijasi:
```text
Route Groups muvaffaqiyatli tashkil etildi.
```

# 863-Topshiriq: .NET 7+ Endpoint Filters (AddEndpointFilter)
## Topshiriq sharti:
Minimal API larda har bir endpoint atrofida validatsiya va tekshiruvlar qilish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();

        app.MapGet("/maxfiy", () => "Maxfiy ma'lumot")
           .AddEndpointFilter(async (context, next) =>
           {
               Console.WriteLine("[Filter]: Endpoint chaqirilishidan oldin tekshiruv.");
               var natija = await next(context);
               Console.WriteLine("[Filter]: Endpoint chaqirilgandan keyin.");
               return natija;
           });

        Console.WriteLine("Endpoint filtri muvaffaqiyatli bog'landi.");
    }
}

```

## Tushuntirish va Mantiq:
`EndpointFilter` eski Controller Action Filterlarining Minimal API dagi zamonaviy, engil va yuqori tezlikdagi muqobilidir.

## Ishlash natijasi:
```text
Endpoint filtri muvaffaqiyatli bog'landi.
```

# 864-Topshiriq: Configuration: builder.Configuration va IOptions<T>
## Topshiriq sharti:
`appsettings.json` sozlamalarini kuchli tipli sinflarga bog'lash.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Options;

class SmsSozlamalari
{
    public string Provayder { get; set; } = "Eskiz";
    public string ApiKalit { get; set; } = "ABC123XYZ";
}

internal class Program
{
    static void Main()
    {
        var builder = WebApplication.CreateBuilder();

        // Sozlamani DI ga ro'yxatdan o'tkazamiz:
        builder.Services.Configure<SmsSozlamalari>(builder.Configuration.GetSection("Sms"));

        var app = builder.Build();

        app.MapGet("/sms-provayder", (IOptions<SmsSozlamalari> opts) =>
        {
            return $"Provayder: {opts.Value.Provayder}";
        });

        Console.WriteLine("Options sozlamalari ulandi.");
    }
}

```

## Tushuntirish va Mantiq:
`IOptions<T>` sozlamalarni markazlashgan holda boshqaradi va sinflarni to'g'ridan-to'g'ri konfiguratsiya fayllariga bog'lanishdan xalos qiladi.

## Ishlash natijasi:
```text
Options sozlamalari ulandi.
```

# 865-Topshiriq: CORS (Cross-Origin Resource Sharing) Sozlamalari
## Topshiriq sharti:
Frontend ilovalariga (React/Vue/Angular) API ga murojaat qilish huquqini berish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;

internal class Program
{
    static void Main()
    {
        var builder = WebApplication.CreateBuilder();

        builder.Services.AddCors(options =>
        {
            options.AddPolicy("FrontendPolicy", siyosat =>
            {
                siyosat.WithOrigins("http://localhost:3000")
                       .AllowAnyHeader()
                       .AllowAnyMethod();
            });
        });

        var app = builder.Build();
        app.UseCors("FrontendPolicy");

        Console.WriteLine("CORS siyosati xavfsiz sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
CORS brauzer xavfsizlik to'sig'ini boshqaradi. Faqat ruxsat etilgan domenlarga API dan ma'lumot olish imkoniyatini taqdim etadi.

## Ishlash natijasi:
```text
CORS siyosati xavfsiz sozlandi.
```

# 866-Topshiriq: JWT Bearer Autentifikatsiya Asoslari va [Authorize]
## Topshiriq sharti:
Endpointlarni faqat tokenli foydalanuvchilar uchun himoyalash.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;

internal class Program
{
    static void Main()
    {
        var builder = WebApplication.CreateBuilder();

        builder.Services.AddAuthentication().AddJwtBearer();
        builder.Services.AddAuthorization();

        var app = builder.Build();

        app.UseAuthentication();
        app.UseAuthorization();

        // Ochiq marshrut:
        app.MapGet("/ochiq", () => "Hammaga ochiq");

        // Himoyalangan marshrut:
        app.MapGet("/himoyalangan", () => "Faqat autentifikatsiyadan o'tganlarga")
           .RequireAuthorization();

        Console.WriteLine("Autentifikatsiya va avtorizatsiya yoqildi.");
    }
}

```

## Tushuntirish va Mantiq:
`RequireAuthorization()` zanjir metodi endpointni qulflaydi va so'rovda to'g'ri `Bearer <token>` bo'lmaganda 401 Unauthorized qaytaradi.

## Ishlash natijasi:
```text
Autentifikatsiya va avtorizatsiya yoqildi.
```

# 867-Topshiriq: Role-Based va Policy-Based Avtorizatsiya
## Topshiriq sharti:
Faqat ma'lum rolga ega foydalanuvchilarga ruxsat berish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();

        // Faqat 'Admin' roli egalariga ruxsat:
        app.MapGet("/boshqaruv", () => "Boshqaruv paneli")
           .RequireAuthorization(policy => policy.RequireRole("Admin"));

        Console.WriteLine("Rolga asoslangan cheklov o'rnatildi.");
    }
}

```

## Tushuntirish va Mantiq:
RBAC (Role-Based Access Control) orqali xodimlar va foydalanuvchilarning lavozimiga ko'ra tizim imkoniyatlarini chegaralash mumkin.

## Ishlash natijasi:
```text
Rolga asoslangan cheklov o'rnatildi.
```

# 868-Topshiriq: .NET 7+ Rate Limiting Middleware (So'rovlar Tezligini Cheklash)
## Topshiriq sharti:
DDOS hujumlaridan himoyalanish uchun bitta IP dan keladigan so'rovlarni chegaralash.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.RateLimiting;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.RateLimiting;
using Microsoft.Extensions.DependencyInjection;

internal class Program
{
    static void Main()
    {
        var builder = WebApplication.CreateBuilder();

        builder.Services.AddRateLimiter(options =>
        {
            // 1 daqiqada maksimal 10 ta so'rov:
            options.AddFixedWindowLimiter("FixedPolicy", opt =>
            {
                opt.Window = TimeSpan.FromMinutes(1);
                opt.PermitLimit = 10;
                opt.QueueLimit = 0;
            });
        });

        var app = builder.Build();
        app.UseRateLimiter();

        app.MapGet("/cheklangan", () => "Cheklangan so'rov")
           .RequireRateLimiting("FixedPolicy");

        Console.WriteLine("Rate Limiter muvaffaqiyatli o'rnatildi.");
    }
}

```

## Tushuntirish va Mantiq:
`AddRateLimiter` .NET 7 da o'rnatilgan rasmiy middleware bo'lib, FixedWindow, SlidingWindow, TokenBucket kabi algoritmlar bilan serverni ortiqcha so'rovlar to'lqinidan saqlaydi.

## Ishlash natijasi:
```text
Rate Limiter muvaffaqiyatli o'rnatildi.
```

# 869-Topshiriq: .NET 7+ Output Caching (Javoblarni Server Xotirasida Keshlash)
## Topshiriq sharti:
Og'ir API javoblarini ma'lum muddatga avtomatik keshlab qo'yish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;

internal class Program
{
    static void Main()
    {
        var builder = WebApplication.CreateBuilder();
        builder.Services.AddOutputCache();

        var app = builder.Build();
        app.UseOutputCache();

        // 30 soniyaga keshlanadi:
        app.MapGet("/statistika", () =>
        {
            Console.WriteLine("[Bajarildi]: Og'ir hisoblash qilindi!");
            return $"Hosil qilingan vaqt: {DateTime.UtcNow:T}";
        }).CacheOutput(p => p.Expire(TimeSpan.FromSeconds(30)));

        Console.WriteLine("Output Cache sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
`OutputCache` takroriy so'rovlarda butun endpoint kodini qayta bajarmasdan, avvalgi tayyorlangan JSON javobni xotiradan bir zumda uzatadi.

## Ishlash natijasi:
```text
Output Cache sozlandi.
```

# 870-Topshiriq: Health Checks (.NET Salomatlik Tekshiruvi)
## Topshiriq sharti:
Docker va Kubernetes uchun `/health` monitoring yo'lini ochish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;

internal class Program
{
    static void Main()
    {
        var builder = WebApplication.CreateBuilder();
        builder.Services.AddHealthChecks();

        var app = builder.Build();
        app.MapHealthChecks("/health");

        Console.WriteLine("Health Checks yo'li faollashtirildi.");
    }
}

```

## Tushuntirish va Mantiq:
Health Checks Kubernetes clusteriga konteynerning tirik (liveness) va so'rov qabul qilishga tayyorligini (readiness) bildiradi.

## Ishlash natijasi:
```text
Health Checks yo'li faollashtirildi.
```

# 871-Topshiriq: IHostedService va BackgroundService Fon Xizmati
## Topshiriq sharti:
Veb server bilan birga fonda mustaqil ishlaydigan davriy xizmat.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Hosting;

class FonXizmati : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        Console.WriteLine("[Fon Xizmati]: Ishga tushirildi.");
        await Task.Delay(50, stoppingToken);
        Console.WriteLine("[Fon Xizmati]: Davriy vazifa bajarildi.");
    }
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("BackgroundService arxitekturasi tayyor.");
    }
}

```

## Tushuntirish va Mantiq:
`BackgroundService` xabarlar navbatlarini tinglash, email jo'natish yoki keshni tozalash kabi uzoq davom etuvchi ishlarni fonda bajaradi.

## Ishlash natijasi:
```text
BackgroundService arxitekturasi tayyor.
```

# 872-Topshiriq: Minimal API da Fayl Yuklash (File Upload: IFormFile)
## Topshiriq sharti:
Foydalanuvchidan rasm yoki hujjat qabul qilib diskka saqlash.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();

        app.MapPost("/yuklash", async (IFormFile fayl) =>
        {
            if (fayl.Length == 0) return Results.BadRequest("Fayl bo'sh!");

            string saqlashYoli = Path.Combine(Path.GetTempPath(), fayl.FileName);
            using (var stream = File.Create(saqlashYoli))
            {
                await fayl.CopyToAsync(stream);
            }

            return Results.Ok(new { Fayl = fayl.FileName, Hajm = fayl.Length });
        });

        Console.WriteLine("Fayl yuklash endpointi sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
`IFormFile` `multipart/form-data` so'rovlaridan kelgan fayllarni xavfsiz va oqimli tarzda qabul qiladi.

## Ishlash natijasi:
```text
Fayl yuklash endpointi sozlandi.
```

# 873-Topshiriq: Custom Binding (BindAsync Metodi)
## Topshiriq sharti:
Sinfning o'zi o'zini HTTP so'rovidan qanday yig'ishini belgilashi.

## Yechim (C# kodi):
```csharp
using System;
using System.Reflection;
using Microsoft.AspNetCore.Http;

class Paginatsiya
{
    public int Sahifa { get; set; } = 1;
    public int Hajm { get; set; } = 10;

    public static ValueTask<Paginatsiya> BindAsync(HttpContext context, ParameterInfo parameter)
    {
        int.TryParse(context.Request.Query["page"], out int page);
        int.TryParse(context.Request.Query["size"], out int size);

        return ValueTask.FromResult(new Paginatsiya
        {
            Sahifa = page > 0 ? page : 1,
            Hajm = size > 0 ? size : 10
        });
    }
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Maxsus BindAsync metodi muvaffaqiyatli ta'riflandi.");
    }
}

```

## Tushuntirish va Mantiq:
Sinfga `public static BindAsync` metodi qo'shilsa, Minimal API uning parametrlarini shu metod orqali avtomatik yig'adi.

## Ishlash natijasi:
```text
Maxsus BindAsync metodi muvaffaqiyatli ta'riflandi.
```

# 874-Topshiriq: AsParameters Atributi (.NET 7+) Bilan Ko'p Parametrlarni Guruhlsh
## Topshiriq sharti:
Endpoint signaturasini 10 ta parametrdan bitta toza tuzilmaga aylantirish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

struct QidiruvSo'rovi
{
    public string? Matn { get; set; }
    public int Sahifa { get; set; }
    public string? Tartib { get; set; }
}

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();

        // [AsParameters] struct ichidagi xususiyatlarni query/route dan avtomatik to'ldiradi:
        app.MapGet("/qidiruv", ([AsParameters] QidiruvSo'rovi sorov) =>
        {
            return $"Qidirilmoqda: {sorov.Matn}, Sahifa: {sorov.Sahifa}";
        });

        Console.WriteLine("AsParameters strukturasi sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
`[AsParameters]` ko'p sonli parametrlar bilan uzun bo'lib ketgan endpoint metodlarini chiroyli va ixcham qiladi.

## Ishlash natijasi:
```text
AsParameters strukturasi sozlandi.
```

# 875-Topshiriq: ProblemDetails Bilan RFC 7807 Xatolik Standarti
## Topshiriq sharti:
Barcha xatolarni xalqaro standartlashtirilgan formatda qaytarish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();

        app.MapGet("/xato-namuna", () =>
        {
            return Results.Problem(
                detail: "Mablag' yetarli emas",
                statusCode: StatusCodes.Status400BadRequest,
                title: "Tranzaksiya Xatoligi",
                type: "https://example.com/errors/insufficient-funds"
            );
        });

        Console.WriteLine("RFC 7807 ProblemDetails formati sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
`ProblemDetails` (RFC 7807) zamonaviy veb standartlarida API xatolarini bir xil strukturada taqdim etishning qat'iy talabidir.

## Ishlash natijasi:
```text
RFC 7807 ProblemDetails formati sozlandi.
```

# 876-Topshiriq: .NET 8+ Keyed Services (Kalitli Xizmatlar: [FromKeyedServices])
## Topshiriq sharti:
Bitta interfeysning bir nechta variantlarini maxsus kalit bilan ro'yxatdan o'tkazish va chaqirish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;

interface IXabarchi { void Yubor(string xabar); }
class TelegramXabarchi : IXabarchi { public void Yubor(string x) => Console.WriteLine($"[Telegram]: {x}"); }
class SmsXabarchi : IXabarchi { public void Yubor(string x) => Console.WriteLine($"[SMS]: {x}"); }

internal class Program
{
    static void Main()
    {
        var builder = WebApplication.CreateBuilder();

        // .NET 8 da kalitli ro'yxatga olish:
        builder.Services.AddKeyedSingleton<IXabarchi, TelegramXabarchi>("tg");
        builder.Services.AddKeyedSingleton<IXabarchi, SmsXabarchi>("sms");

        var app = builder.Build();

        app.MapPost("/xabar/{tur}", (string tur, IServiceProvider sp) =>
        {
            var xizmat = sp.GetRequiredKeyedService<IXabarchi>(tur);
            xizmat.Yubor("Salom, muhim bildirishnoma!");
            return "Yuborildi";
        });

        Console.WriteLine("Keyed Services muvaffaqiyatli ro'yxatga olindi.");
    }
}

```

## Tushuntirish va Mantiq:
Keyed Services .NET 8 ning eng kutilgan xususiyati bo'lib, xizmat nomlari yoki kalitlar orqali bir xil interfeysli turli xizmatlarni oson ajratish imkonini beradi.

## Ishlash natijasi:
```text
Keyed Services muvaffaqiyatli ro'yxatga olindi.
```

# 877-Topshiriq: .NET 8+ Short-Circuiting Marshrutlash (ShortCircuit())
## Topshiriq sharti:
Middleware quvurining og'ir qismlarini chetlab o'tib, zudlik bilan javob qaytarish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();

        // Masalan, robots.txt yoki favicon uchun butun middleware zanjiri shart emas:
        app.MapGet("/robots.txt", () => "User-agent: *
Disallow: /")
           .ShortCircuit();

        Console.WriteLine("Short-circuiting yo'li ochildi.");
    }
}

```

## Tushuntirish va Mantiq:
`ShortCircuit()` marshrutni ro'yxatga olishda avtorizatsiya, kesh yoki maxsus middleware larni chetlab o'tib, javobni zudlik bilan qaytaradi va tezlikni oshiradi.

## Ishlash natijasi:
```text
Short-circuiting yo'li ochildi.
```

# 878-Topshiriq: IHttpClientFactory Bilan Resilient HTTP So'rovlari
## Topshiriq sharti:
Soketlar tugab qolishining (Socket Exhaustion) oldini oluvchi to'g'ri HTTP mijoz.

## Yechim (C# kodi):
```csharp
using System;
using System.Net.Http;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;

internal class Program
{
    static void Main()
    {
        var builder = WebApplication.CreateBuilder();

        // HttpClient factory ni ro'yxatga olamiz:
        builder.Services.AddHttpClient("ValyutaApi", client =>
        {
            client.BaseAddress = new Uri("https://cbu.uz/uz/arkhiv-kursov-valyut/json/");
            client.Timeout = TimeSpan.FromSeconds(5);
        });

        var app = builder.Build();

        app.MapGet("/kurs", async (IHttpClientFactory factory) =>
        {
            var client = factory.CreateClient("ValyutaApi");
            return "HttpClient tayyor";
        });

        Console.WriteLine("IHttpClientFactory sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
`IHttpClientFactory` `HttpMessageHandler` larning hayot davrini boshqaradi, DNS o'zgarishlarini kuzatadi va ochiq qolib ketuvchi soketlarni qayta ishlatadi.

## Ishlash natijasi:
```text
IHttpClientFactory sozlandi.
```

# 879-Topshiriq: .NET 8+ TimeProvider Bilan Vaqtga Bog'liq Kodlarni Testlash
## Topshiriq sharti:
`DateTime.UtcNow` o'rniga soxtalashtirish (Mocking) mumkin bo'lgan rasmiy vaqt provayderi.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.Extensions.DependencyInjection;

class ChegirmaXizmati
{
    private readonly TimeProvider timeProvider;
    public ChegirmaXizmati(TimeProvider timeProvider) => this.timeProvider = timeProvider;

    public bool JumaChegirmasiBormi()
    {
        var hozir = timeProvider.GetUtcNow();
        return hozir.DayOfWeek == DayOfWeek.Friday;
    }
}

internal class Program
{
    static void Main()
    {
        var services = new ServiceCollection();
        // Haqiqiy tizim vaqti provayderi:
        services.AddSingleton(TimeProvider.System);
        services.AddTransient<ChegirmaXizmati>();

        var provider = services.BuildServiceProvider();
        var xizmat = provider.GetRequiredService<ChegirmaXizmati>();

        Console.WriteLine($"Bugun chegirma bormi: {xizmat.JumaChegirmasiBormi()}");
    }
}

```

## Tushuntirish va Mantiq:
`TimeProvider` .NET 8 da kiritilgan bo'lib, testlarda vaqtni oldinga surish, muzlatish yoki o'zgartirishni osonlashtiradi.

## Ishlash natijasi:
```text
Bugun chegirma bormi: ...
```

# 880-Topshiriq: Response Compression Middleware Bilan JSON Siqish
## Topshiriq sharti:
Tarmoq orqali yuboriladigan API javoblarini GZip yoki Brotli bilan avtomatik kichraytirish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.ResponseCompression;
using Microsoft.Extensions.DependencyInjection;

internal class Program
{
    static void Main()
    {
        var builder = WebApplication.CreateBuilder();

        builder.Services.AddResponseCompression(options =>
        {
            options.EnableForHttps = true;
            options.Providers.Add<BrotliCompressionProvider>();
            options.Providers.Add<GzipCompressionProvider>();
        });

        var app = builder.Build();
        app.UseResponseCompression();

        Console.WriteLine("Response siqish quvuri sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
Response Compression katta JSON javoblarni brauzerga yetkazishda tarmoq kechikishini keskin kamaytiradi.

## Ishlash natijasi:
```text
Response siqish quvuri sozlandi.
```

# 881-Topshiriq: Server-Sent Events (SSE) Bilan Real Vaqtli Matn Oqimi
## Topshiriq sharti:
Sun'iy intellekt (ChatGPT/LLM) kabi matnni so'zma-so'z oqim qilib uzatish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

internal class Program
{
    static async IAsyncEnumerable<string> AiJavobGeneratori()
    {
        string[] sozlar = ["Sun'iy", "intellekt", "javobi", "oqim", "bo'ylab", "kelmoqda."];
        foreach (var s in sozlar)
        {
            await Task.Delay(20);
            yield return s + " ";
        }
    }

    static void Main()
    {
        var app = WebApplication.Create();

        app.MapGet("/ai/stream", () => AiJavobGeneratori());

        Console.WriteLine("SSE oqim marshruti tayyor.");
    }
}

```

## Tushuntirish va Mantiq:
`IAsyncEnumerable` orqali Minimal API avtomatik ravishda Chunked Transfer Encoding yoki Server-Sent Events oqimini yoqadi.

## Ishlash natijasi:
```text
SSE oqim marshruti tayyor.
```

# 882-Topshiriq: OpenAPI / Swagger Integratsiyasi va Metadata
## Topshiriq sharti:
Minimal API larda WithSummary, WithDescription va Produces atributlari.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();

        app.MapGet("/api/mahsulot/{id}", (int id) => Results.Ok("Mahsulot"))
           .WithName("MahsulotniOlish")
           .WithSummary("ID bo'yicha mahsulotni qaytaradi")
           .WithDescription("Batafsil ma'lumotlar bilan to'liq obyektni beradi")
           .Produces(StatusCodes.Status200OK)
           .Produces(StatusCodes.Status404NotFound);

        Console.WriteLine("OpenAPI metadata muvaffaqiyatli o'rnatildi.");
    }
}

```

## Tushuntirish va Mantiq:
Ushbu metadata metodlari Swagger UI da chiroyli dokumentatsiya va tushuntirishlarni hosil qiladi.

## Ishlash natijasi:
```text
OpenAPI metadata muvaffaqiyatli o'rnatildi.
```

# 883-Topshiriq: .NET 8+ IExceptionHandler Interfeysi Bilan Xatoliklarni Tutish
## Topshiriq sharti:
Sinflashtirilgan, zamonaviy va DI ga bog'langan global xatolik nazoratchisi.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Diagnostics;
using Microsoft.AspNetCore.Http;

class GlobalExceptionHandler : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken cancellationToken)
    {
        Console.WriteLine($"[IExceptionHandler Tutdi]: {exception.Message}");

        httpContext.Response.StatusCode = StatusCodes.Status500InternalServerError;
        await httpContext.Response.WriteAsJsonAsync(new
        {
            Xato = "Ichki server muammosi",
            Sabab = exception.Message
        }, cancellationToken);

        return true; // Xato to'liq hal qilindi
    }
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine(".NET 8 IExceptionHandler arxitekturasi tayyor.");
    }
}

```

## Tushuntirish va Mantiq:
`IExceptionHandler` .NET 8 da kiritilgan toza interfeys bo'lib, eski middleware uslubini butunlay standartlashtiradi.

## Ishlash natijasi:
```text
.NET 8 IExceptionHandler arxitekturasi tayyor.
```

# 884-Topshiriq: ForwardedHeadersMiddleware: Reverse Proxy (Nginx/K8s) Orqasidagi Real IP
## Topshiriq sharti:
Proksi ortida yo'qolib ketadigan mijoz IP manzili va protokollarini tiklash.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.HttpOverrides;

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();

        app.UseForwardedHeaders(new ForwardedHeadersOptions
        {
            ForwardedHeaders = ForwardedHeaders.XForwardedFor | ForwardedHeaders.XForwardedProto
        });

        app.MapGet("/mening-ipim", (Microsoft.AspNetCore.Http.HttpContext ctx) =>
        {
            return $"Mijoz IP manzili: {ctx.Connection.RemoteIpAddress}";
        });

        Console.WriteLine("Forwarded Headers sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
Docker va Nginx ortida ishlayotgan har qanday ASP.NET Core ilovasi real foydalanuvchi IP sini bilish uchun ushbu middleware ni yoqishi shart.

## Ishlash natijasi:
```text
Forwarded Headers sozlandi.
```

# 885-Topshiriq: HttpLoggingMiddleware Bilan So'rovlarni Avtomatik Audit Qilish
## Topshiriq sharti:
Barcha kiruvchi so'rov sarlavhalari va javoblarini avtomatik loglash.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.HttpLogging;
using Microsoft.Extensions.DependencyInjection;

internal class Program
{
    static void Main()
    {
        var builder = WebApplication.CreateBuilder();

        builder.Services.AddHttpLogging(logging =>
        {
            logging.LoggingFields = HttpLoggingFields.RequestPath |
                                   HttpLoggingFields.RequestMethod |
                                   HttpLoggingFields.ResponseStatusCode;
        });

        var app = builder.Build();
        app.UseHttpLogging();

        Console.WriteLine("HTTP Logging tizimi yoqildi.");
    }
}

```

## Tushuntirish va Mantiq:
`AddHttpLogging` .NET 6 da qo'shilgan bo'lib, xavfsizlik va debugging uchun HTTP oqimini avtomat loglaydi.

## Ishlash natijasi:
```text
HTTP Logging tizimi yoqildi.
```

# 886-Topshiriq: Kestrel MaxRequestBodySize Bilan Katta Fayllar Cheklovini Belgilash
## Topshiriq sharti:
Serverga yuboriladigan maksimal so'rov hajmini oshirish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Server.Kestrel.Core;
using Microsoft.Extensions.DependencyInjection;

internal class Program
{
    static void Main()
    {
        var builder = WebApplication.CreateBuilder();

        // 100 MB gacha ruxsat beramiz:
        builder.Services.Configure<KestrelServerOptions>(options =>
        {
            options.Limits.MaxRequestBodySize = 100 * 1024 * 1024;
        });

        Console.WriteLine("Kestrel limitlari 100 MB ga kengaytirildi.");
    }
}

```

## Tushuntirish va Mantiq:
Kestrel sukut bo'yicha so'rov tanasini 30 MB bilan cheklaydi; katta fayllar yuklashda bu limit oshirilishi kerak.

## Ishlash natijasi:
```text
Kestrel limitlari 100 MB ga kengaytirildi.
```

# 887-Topshiriq: Kestrel HTTP/3 (QUIC) Protokolini Faollashtirish
## Topshiriq sharti:
UDP asosidagi eng zamonaviy HTTP/3 protokoli orqali tezlikni oshirish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Server.Kestrel.Core;

internal class Program
{
    static void Main()
    {
        var builder = WebApplication.CreateBuilder();

        builder.WebHost.ConfigureKestrel(options =>
        {
            options.ConfigureEndpointDefaults(listen =>
            {
                // HTTP/1.1, HTTP/2 va HTTP/3 ni parallel yoqish:
                listen.Protocols = HttpProtocols.Http1AndHttp2AndHttp3;
            });
        });

        Console.WriteLine("HTTP/3 protokoli muvaffaqiyatli faollashtirildi.");
    }
}

```

## Tushuntirish va Mantiq:
HTTP/3 QUIC protokoli TCP ning paket yo'qotishdagi kechikishlarini yo'qotadi va mobil tarmoqlarda super-tezlik beradi.

## Ishlash natijasi:
```text
HTTP/3 protokoli muvaffaqiyatli faollashtirildi.
```

# 888-Topshiriq: .NET 9 Yangi HybridCache Texnologiyasi
## Topshiriq sharti:
L1 (In-Memory) va L2 (Distributed/Redis) keshlarini birlashtiruvchi zamonaviy arxitektura.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;

class SoxtaHybridKesh
{
    public async Task<T> GetOrCreateAsync<T>(string kalit, Func<Task<T>> yuklovchi)
    {
        Console.WriteLine($"[HybridCache]: '{kalit}' xotirada qidirildi...");
        return await yuklovchi();
    }
}

internal class Program
{
    static async Task Main()
    {
        var kesh = new SoxtaHybridKesh();

        string natija = await kesh.GetOrCreateAsync("foydalanuvchi_1", async () =>
        {
            await Task.Delay(20);
            return "Akmal (Bazadan olingan)";
        });

        Console.WriteLine($"Natija: {natija}");
    }
}

```

## Tushuntirish va Mantiq:
`HybridCache` .NET 9 da rasmiy kiritilgan bo'lib, 'Cache Stampede' muammosini yo'qotadi va xotira va Redis o'rtasida muvozanatni ushlaydi.

## Ishlash natijasi:
```text
[HybridCache]: 'foydalanuvchi_1' xotirada qidirildi...
Natija: Akmal (Bazadan olingan)
```

# 889-Topshiriq: SignalR Bilan Minimal API Integratsiyasi (MapHub<T>)
## Topshiriq sharti:
Real vaqtli ikki tomonlama WebSockets aloqa xabini o'rnatish.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.SignalR;
using Microsoft.Extensions.DependencyInjection;

class ChatHub : Hub
{
    public async Task XabarYubor(string xabar)
    {
        await Clients.All.SendAsync("XabarKeldi", xabar);
    }
}

internal class Program
{
    static void Main()
    {
        var builder = WebApplication.CreateBuilder();
        builder.Services.AddSignalR();

        var app = builder.Build();
        app.MapHub<ChatHub>("/chat");

        Console.WriteLine("SignalR Hub Minimal API ga ulandi.");
    }
}

```

## Tushuntirish va Mantiq:
`MapHub<T>` veb soketlar orqali mijozlar va server o'rtasida bir zumda xabar almashish imkonini yaratadi.

## Ishlash natijasi:
```text
SignalR Hub Minimal API ga ulandi.
```

# 890-Topshiriq: CSRF / Antiforgery Himoyasi (.NET 8+ Minimal API)
## Topshiriq sharti:
Saytlararo so'rovlarni soxtalashtirish (Cross-Site Request Forgery) hujumlaridan himoya.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;

internal class Program
{
    static void Main()
    {
        var builder = WebApplication.CreateBuilder();
        builder.Services.AddAntiforgery();

        var app = builder.Build();
        app.UseAntiforgery();

        // .NET 8 da Minimal API larda Antiforgery token tekshiruvini yoqish:
        app.MapPost("/xavfsiz-forma", () => "Forma qabul qilindi!")
           .RequireAntiforgery();

        Console.WriteLine("Antiforgery himoyasi muvaffaqiyatli yoqildi.");
    }
}

```

## Tushuntirish va Mantiq:
.NET 8 gacha Minimal API larda o'rnatilgan Antiforgery yo'q edi. Yangi `.RequireAntiforgery()` xavfsizlikni kuchaytiradi.

## Ishlash natijasi:
```text
Antiforgery himoyasi muvaffaqiyatli yoqildi.
```

# 891-Topshiriq: Custom Route Constraint Yaratish (IRouteConstraint)
## Topshiriq sharti:
Marshrut parametrlariga maxsus mantiqiy qoida yozish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;

class FaqatUzbekTelefoniConstraint : IRouteConstraint
{
    public bool Match(
        HttpContext? httpContext,
        IRouter? route,
        string routeKey,
        RouteValueDictionary values,
        RouteDirection routeDirection)
    {
        if (values.TryGetValue(routeKey, out var qiymat) && qiymat is string telefon)
        {
            return telefon.StartsWith("+998");
        }
        return false;
    }
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Custom Route Constraint sinfi tayyor.");
    }
}

```

## Tushuntirish va Mantiq:
`IRouteConstraint` orqali URL dagi har qanday maxsus formatni (telefon raqami, pasport seriyasi) tekshirish mumkin.

## Ishlash natijasi:
```text
Custom Route Constraint sinfi tayyor.
```

# 892-Topshiriq: Request Decompression (.NET 7+) Bilan Siqilgan So'rovlarni Qabul Qilish
## Topshiriq sharti:
Mijozdan kelgan GZip siqilgan HTTP so'rovlarini avtomatik ochish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;

internal class Program
{
    static void Main()
    {
        var builder = WebApplication.CreateBuilder();
        builder.Services.AddRequestDecompression();

        var app = builder.Build();
        app.UseRequestDecompression();

        Console.WriteLine("Request Decompression yoqildi.");
    }
}

```

## Tushuntirish va Mantiq:
IoT qurilmalari va mobil ilovalar serverga trafikni tejash uchun so'rovlarni GZip qilib yuborganida server ularni avtomatik ochadi.

## Ishlash natijasi:
```text
Request Decompression yoqildi.
```

# 893-Topshiriq: Response Caching Middleware va Cache-Control Sarlavhalari
## Topshiriq sharti:
HTTP `Cache-Control` sarlavhalarini klient brauzeriga to'g'ri yetkazish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();

        app.MapGet("/keshlanuvchi-resurs", (HttpResponse res) =>
        {
            res.Headers.CacheControl = "public, max-age=3600"; // 1 soat brauzer keshida saqlansin
            return "Ushbu ma'lumot brauzerda keshlanadi";
        });

        Console.WriteLine("Cache-Control sarlavhalari sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
To'g'ri sozlangan HTTP kesh sarlavhalari serverga keladigan so'rovlar sonini keskin kamaytiradi.

## Ishlash natijasi:
```text
Cache-Control sarlavhalari sozlandi.
```

# 894-Topshiriq: WebSockets Asoslari Minimal API da
## Topshiriq sharti:
Past darajadagi WebSocket oqimini ochish va ulanish.

## Yechim (C# kodi):
```csharp
using System;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();
        app.UseWebSockets();

        app.Map("/ws", async (HttpContext ctx) =>
        {
            if (ctx.WebSockets.IsWebSocketRequest)
            {
                using var ws = await ctx.WebSockets.AcceptWebSocketAsync();
                byte[] bufer = Encoding.UTF8.GetBytes("Salom WebSocket");
                await ws.SendAsync(bufer, WebSocketMessageType.Text, true, CancellationToken.None);
            }
            else
            {
                ctx.Response.StatusCode = 400;
            }
        });

        Console.WriteLine("WebSocket quvuri muvaffaqiyatli tayyorlandi.");
    }
}

```

## Tushuntirish va Mantiq:
`ctx.WebSockets.AcceptWebSocketAsync()` HTTP ulanishini ikki tomonlama doimiy ochiq bayt oqimiga aylantiradi.

## Ishlash natijasi:
```text
WebSocket quvuri muvaffaqiyatli tayyorlandi.
```

# 895-Topshiriq: EndpointFilterFactory Bilan Dinamik Filtr Generatsiyasi
## Topshiriq sharti:
Har bir endpoint parametrlariga ko'ra dinamik filtr ishlab chiqarish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();

        app.MapGet("/dinamik", () => "OK")
           .AddEndpointFilterFactory((routeHandlerContext, next) =>
           {
               Console.WriteLine($"[Filtr Fabrikasi]: {routeHandlerContext.MethodInfo.Name} uchun filtr qurildi.");
               return async invocationContext =>
               {
                   return await next(invocationContext);
               };
           });

        Console.WriteLine("Filter Factory ulandi.");
    }
}

```

## Tushuntirish va Mantiq:
Filter Factory kompilyatsiya vaqtida bir marta ishga tushib, har bir endpoint uchun moslashtirilgan filtr yaratadi.

## Ishlash natijasi:
```text
Filter Factory ulandi.
```

# 896-Topshiriq: Minimal API va Controllers Gibrid Arxitekturasi
## Topshiriq sharti:
Ikkala yondashuvni bitta loyihada parallel yuritish.

## Yechim (C# kodi):
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.DependencyInjection;

[ApiController]
[Route("api/[controller]")]
class TestController : ControllerBase
{
    [HttpGet] public IActionResult Get() => Ok("Controller javobi");
}

internal class Program
{
    static void Main()
    {
        var builder = WebApplication.CreateBuilder();
        builder.Services.AddControllers();

        var app = builder.Build();

        app.MapControllers(); // Controllerlar marshrutlash
        app.MapGet("/minimal", () => "Minimal API javobi"); // Minimal API

        Console.WriteLine("Gibrid Web API arxitekturasi sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
Yirik loyihalarda mavjud kontrollerlarni saqlab qolgan holda, yangi yuqori tezlikdagi mikroxizmatlarni Minimal API da yozish keng tarqalgan amaliyotdir.

## Ishlash natijasi:
```text
Gibrid Web API arxitekturasi sozlandi.
```

# 897-Topshiriq: IP-ga Asoslangan Filtr Middleware
## Topshiriq sharti:
Faqat ichki tarmoqdagi (Whitelist) IP larga kirishga ruxsat berish.

## Yechim (C# kodi):
```csharp
using System;
using System.Net;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();

        app.Use(async (context, next) =>
        {
            var ip = context.Connection.RemoteIpAddress;
            if (ip != null && IPAddress.IsLoopback(ip))
            {
                await next(context);
            }
            else
            {
                context.Response.StatusCode = StatusCodes.Status403Forbidden;
            }
        });

        Console.WriteLine("IP Whitelist xavfsizlik filtri sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
Ichki boshqaruv panellari va metrikalar xavfsizligini ta'minlashda IP filtri birinchi darajali to'siq vazifasini o'taydi.

## Ishlash natijasi:
```text
IP Whitelist xavfsizlik filtri sozlandi.
```

# 898-Topshiriq: FluentValidation bilan Model Validatsiyasi Endpoint Filtrida
## Topshiriq sharti:
DTO ma'lumotlarini qat'iy biznes qoidalari asosida tekshirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

record MahsulotKiritish(string Nomi, decimal Narxi);

internal class Program
{
    static void Main()
    {
        var app = WebApplication.Create();

        app.MapPost("/mahsulot", (MahsulotKiritish dto) => Results.Ok("Qabul qilindi"))
           .AddEndpointFilter(async (context, next) =>
           {
               var dto = context.GetArgument<MahsulotKiritish>(0);
               if (string.IsNullOrWhiteSpace(dto.Nomi))
                   return Results.BadRequest("Mahsulot nomi bo'sh bo'lishi mumkin emas!");
               if (dto.Narxi <= 0)
                   return Results.BadRequest("Narx musbat bo'lishi shart!");

               return await next(context);
           });

        Console.WriteLine("Validatsiya filtri sozlandi.");
    }
}

```

## Tushuntirish va Mantiq:
Endpoint Filterlari DTO larni biznes mantiqqa kirmasdan oldin tekshirib, xatolarni toza ushlab qoladi.

## Ishlash natijasi:
```text
Validatsiya filtri sozlandi.
```

# 899-Topshiriq: Custom Results (IResult Interfeysini Qo'lda Amalga Oshirish)
## Topshiriq sharti:
Maxsus HTTP javob turini (masalan CSV yoki XML) o'z ichiga olgan natija obyekti.

## Yechim (C# kodi):
```csharp
using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;

class HtmlResult : IResult
{
    private readonly string html;
    public HtmlResult(string html) => this.html = html;

    public async Task ExecuteAsync(HttpContext httpContext)
    {
        httpContext.Response.ContentType = "text/html; charset=utf-8";
        await httpContext.Response.WriteAsync(html);
    }
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Custom IResult sinfi tayyorlandi.");
    }
}

```

## Tushuntirish va Mantiq:
`IResult` interfeysi Minimal API javoblarini to'liq inkapsulyatsiya qilish imkonini beradi.

## Ishlash natijasi:
```text
Custom IResult sinfi tayyorlandi.
```

# 900-Topshiriq: Web API Xulosasi: To'liq RESTful In-Memory Savdo Minimal API Dvigateli
## Topshiriq sharti:
CRUD, DI, Validation, Results, TypedResults, Route Groups va Exception Handling ni birlashtirgan to'liq xizmat.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.DependencyInjection;

record Kitob(int Id, string Sarlavha, decimal Narx);
record KitobYaratishDto(string Sarlavha, decimal Narx);

interface IKitobOmbori
{
    IEnumerable<Kitob> Hamma();
    Kitob? Top(int id);
    Kitob Qosh(KitobYaratishDto dto);
}

class InMemoryKitobOmbori : IKitobOmbori
{
    private readonly ConcurrentDictionary<int, Kitob> ombor = new();
    private int hisob = 0;

    public IEnumerable<Kitob> Hamma() => ombor.Values;
    public Kitob? Top(int id) => ombor.TryGetValue(id, out var k) ? k : null;
    public Kitob Qosh(KitobYaratishDto dto)
    {
        int id = System.Threading.Interlocked.Increment(ref hisob);
        var k = new Kitob(id, dto.Sarlavha, dto.Narx);
        ombor[id] = k;
        return k;
    }
}

internal class Program
{
    static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);
        builder.Services.AddSingleton<IKitobOmbori, InMemoryKitobOmbori>();

        var app = builder.Build();

        var api = app.MapGroup("/api/kitoblar");

        api.MapGet("/", (IKitobOmbori repo) => Results.Ok(repo.Hamma()));

        api.MapGet("/{id:int}", (int id, IKitobOmbori repo) =>
        {
            var k = repo.Top(id);
            return k is not null ? Results.Ok(k) : Results.NotFound("Kitob topilmadi");
        });

        api.MapPost("/", (KitobYaratishDto dto, IKitobOmbori repo) =>
        {
            if (string.IsNullOrWhiteSpace(dto.Sarlavha))
                return Results.BadRequest("Sarlavha bo'sh bo'lmasligi kerak!");

            var yangi = repo.Qosh(dto);
            return Results.Created($"/api/kitoblar/{yangi.Id}", yangi);
        });

        Console.WriteLine("To'liq RESTful Minimal API arxitekturasi muvaffaqiyatli yaratildi.");
    }
}

```

## Tushuntirish va Mantiq:
Ushbu to'liq Minimal API arxitekturasi zamonaviy C#/.NET 8/9 mikroxizmatlari uchun benchmark darajasidagi toza andoza hisoblanadi.

## Ishlash natijasi:
```text
To'liq RESTful Minimal API arxitekturasi muvaffaqiyatli yaratildi.
```

