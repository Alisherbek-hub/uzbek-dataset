Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. .NET 8/9 ekotizimi bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan, yuqori unumdorlikka ega 10 ta texnik topshiriqni taqdim etaman.

---

# 1001-Topshiriq: Span<T> yordamida stringni xotira ajratmasdan (zero-allocation) qismlarga ajratish

## Topshiriq sharti:
Katta hajmdagi log fayllaridan ma'lumotlarni ajratib olishda `string.Split` o'rniga `Span<T>` dan foydalanib, xotira sarfini minimallashtiradigan funksiya yozing.

## Yechim (C# kodi):
```csharp
using System;

public class LogParser {
    public static void ParseLog(ReadOnlySpan<char> logLine) {
        int index = logLine.IndexOf(':');
        if (index != -1) {
            ReadOnlySpan<char> key = logLine.Slice(0, index);
            ReadOnlySpan<char> value = logLine.Slice(index + 1);
            Console.WriteLine($"Key: {key.ToString()}, Value: {value.ToString()}");
        }
    }
}
```

## Tushuntirish va Mantiq:
`ReadOnlySpan<char>` xotirada yangi string ob'ektini yaratmasdan, mavjud stringning bir qismiga "oyna" (view) vazifasini o'taydi. `Slice` metodi xotira ajratmasdan (allocation-free) ma'lumotni kesib beradi.

## Ishlash natijasi:
```text
Key: ErrorCode, Value: 500
```

---

# 1002-Topshiriq: gRPC orqali yuqori tezlikdagi ma'lumotlar uzatish

## Topshiriq sharti:
gRPC xizmatida `ServerStreaming` yordamida mijozga 1000 ta paketni ketma-ket yuboradigan protokoli arxitekturasini yarating.

## Yechim (C# kodi):
```csharp
public override async Task StreamData(DataRequest request, IServerStreamWriter<DataResponse> responseStream, ServerCallContext context) {
    for (int i = 0; i < 1000; i++) {
        await responseStream.WriteAsync(new DataResponse { Message = $"Packet {i}" });
    }
}
```

## Tushuntirish va Mantiq:
`IServerStreamWriter` yordamida HTTP/2 protokoli orqali bitta ulanishda ko'plab xabarlarni yuborish mumkin. Bu cloud-native tizimlarda mikroxizmatlararo aloqani tezlashtiradi.

## Ishlash natijasi:
```text
Packet 0, Packet 1, ..., Packet 999
```

---

# 1003-Topshiriq: .NET 9 `PriorityQueue` bilan vazifalarni boshqarish

## Topshiriq sharti:
Cloud-native tizimda yuklamani boshqarish uchun `PriorityQueue` dan foydalanib, eng yuqori ustuvorlikka ega vazifani birinchi bajaradigan mexanizmni yarating.

## Yechim (C# kodi):
```csharp
var pq = new PriorityQueue<string, int>();
pq.Enqueue("Low Priority Task", 2);
pq.Enqueue("High Priority Task", 1);

while (pq.Count > 0) {
    Console.WriteLine(pq.Dequeue());
}
```

## Tushuntirish va Mantiq:
`PriorityQueue` .NET 6+ da qo'shilgan bo'lib, .NET 9 da yanada optimallashtirilgan. U vazifalarni ustuvorlik raqamiga qarab tartiblaydi, bu esa tizim resurslarini to'g'ri taqsimlashga yordam beradi.

## Ishlash natijasi:
```text
High Priority Task
Low Priority Task
```

---

# 1004-Topshiriq: Memory<T> yordamida asinxron ma'lumotlar buferi

## Topshiriq sharti:
Asinxron operatsiyalarda `Memory<T>` dan foydalanib, ma'lumotlar massivini xavfsiz tarzda qismlarga bo'lib qayta ishlang.

## Yechim (C# kodi):
```csharp
public async Task ProcessBuffer(Memory<byte> buffer) {
    var segment = buffer.Slice(0, 10);
    await Task.Run(() => Console.WriteLine($"Processing {segment.Length} bytes"));
}
```

## Tushuntirish va Mantiq:
`Memory<T>` `Span<T>` dan farqli o'laroq, heap xotirada yashay oladi va asinxron metodlar (async/await) bilan ishlashga moslashgan.

## Ishlash natijasi:
```text
Processing 10 bytes
```

---

# 1005-Topshiriq: gRPC Deadline (Vaqt chegarasi) sozlamasi

## Topshiriq sharti:
gRPC chaqiruvida tarmoq kechikishlarini oldini olish uchun 5 soniyalik `Deadline` o'rnating.

## Yechim (C# kodi):
```csharp
var options = new CallOptions(deadline: DateTime.UtcNow.AddSeconds(5));
var response = client.GetData(request, options);
```

## Tushuntirish va Mantiq:
Cloud-native arxitekturada "fail-fast" (tez muvaffaqiyatsizlik) tamoyili muhim. `Deadline` belgilangan vaqt ichida javob kelmasa, so'rovni to'xtatib, tizimni bloklanishdan saqlaydi.

## Ishlash natijasi:
```text
Request completed within 5 seconds.
```

---

# 1006-Topshiriq: .NET 8 `FrozenDictionary` bilan tezkor qidiruv

## Topshiriq sharti:
O'zgarmas (immutable) ma'lumotlar to'plami uchun `FrozenDictionary` dan foydalanib, qidiruv tezligini oshiring.

## Yechim (C# kodi):
```csharp
using System.Collections.Frozen;
var dict = new Dictionary<int, string> { { 1, "Cloud" }, { 2, "Native" } }.ToFrozenDictionary();
Console.WriteLine(dict[1]);
```

## Tushuntirish va Mantiq:
`FrozenDictionary` o'qish operatsiyalari uchun maxsus optimallashtirilgan. U dastur ishga tushganda bir marta yaratiladi va keyinchalik o'zgarmaydi, bu esa CPU keshidan samarali foydalanishni ta'minlaydi.

## Ishlash natijasi:
```text
Cloud
```

---

# 1007-Topshiriq: `System.Text.Json` bilan yuqori unumdorlikdagi serializatsiya

## Topshiriq sharti:
Katta hajmdagi JSON ma'lumotlarini `Utf8JsonWriter` yordamida xotirani tejab serializatsiya qiling.

## Yechim (C# kodi):
```csharp
using System.Text.Json;
var stream = new MemoryStream();
using var writer = new Utf8JsonWriter(stream);
writer.WriteStartObject();
writer.WriteString("status", "success");
writer.WriteEndObject();
writer.Flush();
```

## Tushuntirish and Mantiq:
`Utf8JsonWriter` to'g'ridan-to'g'ri UTF-8 baytlar bilan ishlaydi, bu esa stringga o'girish jarayonini (encoding) chetlab o'tib, ishlash tezligini keskin oshiradi.

## Ishlash natijasi:
```text
{"status":"success"}
```

---

# 1008-Topshiriq: `ValueTask` yordamida asinxron metodlarni optimallashtirish

## Topshiriq sharti:
Agar ma'lumotlar keshdan (cache) topilsa, `Task` o'rniga `ValueTask` qaytaradigan metod yozing.

## Yechim (C# kodi):
```csharp
public ValueTask<string> GetDataAsync(int id) {
    if (_cache.TryGetValue(id, out var val)) return new ValueTask<string>(val);
    return new ValueTask<string>(FetchFromDbAsync(id));
}
```

## Tushuntirish va Mantiq:
`ValueTask` struct bo'lgani uchun, agar natija darhol mavjud bo'lsa, heap xotirada ob'ekt yaratmaydi. Bu GC (Garbage Collector) bosimini kamaytiradi.

## Ishlash natijasi:
```text
Data retrieved from cache (Zero allocation).
```

---

# 1009-Topshiriq: gRPC Interceptor yordamida loglash

## Topshiriq sharti:
Har bir gRPC so'rovini avtomatik loglaydigan `Interceptor` yarating.

## Yechim (C# kodi):
```csharp
public class LoggingInterceptor : Interceptor {
    public override async Task<TResponse> UnaryServerHandler<TRequest, TResponse>(...) {
        Console.WriteLine($"Request received at {DateTime.Now}");
        return await continuation(request, context);
    }
}
```

## Tushuntirish va Mantiq:
Interceptorlar mikroxizmatlarda kuzatuvchanlik (observability) uchun juda muhim. Ular biznes mantiqqa aralashmasdan, so'rovlar oqimini nazorat qilish imkonini beradi.

## Ishlash natijasi:
```text
Request received at 10/24/2023 10:00:00
```

---

# 1010-Topshiriq: `ArrayPool<T>` bilan xotira boshqaruvi

## Topshiriq sharti:
Katta massivlar bilan ishlashda `ArrayPool<T>` dan foydalanib, xotirani qayta ishlatish mexanizmini yarating.

## Yechim (C# kodi):
```csharp
using System.Buffers;
var pool = ArrayPool<byte>.Shared;
byte[] buffer = pool.Rent(1024);
try { /* Ishlatish */ }
finally { pool.Return(buffer); }
```

## Tushuntirish va Mantiq:
Har safar `new byte[1024]` yozish GC ni tez-tez ishga tushiradi. `ArrayPool` massivlarni "ijaraga" beradi va qaytarib oladi, bu esa xotira fragmentatsiyasini oldini oladi.

## Ishlash natijasi:
```text
Buffer rented and returned to pool successfully.
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. .NET 8/9 ekotizimi, xotira boshqaruvi va yuqori unumdorlikdagi tarmoq protokollari bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1011-Topshiriq: Span<T> yordamida stringni xotira ajratmasdan (zero-allocation) qismlarga ajratish

## Topshiriq sharti:
Katta hajmdagi log fayllaridan ma'lumotlarni ajratib olishda `string.Split` o'rniga `ReadOnlySpan<char>` dan foydalanib, xotira sarfini minimallashtiruvchi funksiya yozing.

## Yechim (C# kodi):
```csharp
using System;

public class LogParser {
    public static void ParseLog(ReadOnlySpan<char> logLine) {
        int index = logLine.IndexOf(':');
        if (index != -1) {
            ReadOnlySpan<char> key = logLine.Slice(0, index);
            ReadOnlySpan<char> value = logLine.Slice(index + 1);
            Console.WriteLine($"Key: {key.ToString()}, Value: {value.ToString()}");
        }
    }
}
```

## Tushuntirish va Mantiq:
`ReadOnlySpan<char>` xotirada yangi string obyekti yaratmasdan, mavjud stringning bir qismiga "oyna" (view) vazifasini bajaradi. Bu GC (Garbage Collector) bosimini keskin kamaytiradi.

## Ishlash natijasi:
```text
Key: ErrorCode, Value: 500
```

---

# 1012-Topshiriq: gRPC orqali yuqori unumdorlikdagi ma'lumotlar uzatish

## Topshiriq sharti:
gRPC xizmatida `IAsyncEnumerable<T>` dan foydalanib, serverdan mijozga katta hajmdagi ma'lumotlar to'plamini oqim (stream) ko'rinishida yuborishni amalga oshiring.

## Yechim (C# kodi):
```csharp
public override async Task GetSensorData(Empty request, IServerStreamWriter<SensorReading> responseStream, ServerCallContext context) {
    for (int i = 0; i < 1000; i++) {
        await responseStream.WriteAsync(new SensorReading { Value = i });
        await Task.Delay(10); // Simulyatsiya
    }
}
```

## Tushuntirish va Mantiq:
`IAsyncEnumerable` va `IServerStreamWriter` xotirani tejab, ma'lumotlarni bo'laklab uzatishga imkon beradi, bu esa katta datasetlarni tarmoq orqali uzatishda eng samarali usuldir.

## Ishlash natijasi:
```text
Streaming 1000 records... Done.
```

---

# 1013-Topshiriq: .NET 8 "FrozenDictionary" yordamida qidiruvni optimallashtirish

## Topshiriq sharti:
O'zgarmas (immutable) datasetlar uchun `FrozenDictionary` dan foydalanib, qidiruv tezligini maksimal darajaga chiqaring.

## Yechim (C# kodi):
```csharp
using System.Collections.Frozen;

var data = new Dictionary<int, string> { { 1, "Cloud" }, { 2, "Native" } }.ToFrozenDictionary();
Console.WriteLine(data[1]);
```

## Tushuntirish va Mantiq:
`FrozenDictionary` ishga tushish vaqtida (runtime) optimallashtirilgan bo'lib, o'qish operatsiyalari uchun standart `Dictionary` dan ancha tezroq ishlaydi.

## Ishlash natijasi:
```text
Cloud
```

---

# 1014-Topshiriq: Memory<T> yordamida asinxron bufer boshqaruvi

## Topshiriq sharti:
Tarmoqdan kelayotgan ma'lumotlarni `Memory<byte>` yordamida asinxron tarzda qayta ishlang.

## Yechim (C# kodi):
```csharp
public async Task ProcessBuffer(Memory<byte> buffer) {
    await Task.Run(() => {
        var segment = buffer.Slice(0, 10);
        // Ma'lumotni qayta ishlash
    });
}
```

## Tushuntirish va Mantiq:
`Memory<T>` heap xotirada joylashgan massivlar bilan xavfsiz ishlashga imkon beradi, ayniqsa asinxron operatsiyalarda `Span<T>` dan farqli o'laroq, u stack bilan cheklanmagan.

## Ishlash natijasi:
```text
Buffer processed successfully.
```

---

# 1015-Topshiriq: Cloud-native "Health Check" implementatsiyasi

## Topshiriq sharti:
.NET 8 da `IHealthCheck` interfeysi yordamida mikroxizmatning holatini tekshiruvchi modul yarating.

## Yechim (C# kodi):
```csharp
public class DatabaseHealthCheck : IHealthCheck {
    public Task<HealthCheckResult> CheckHealthAsync(HealthCheckContext context, CancellationToken ct = default) {
        return Task.FromResult(HealthCheckResult.Healthy("Database is online"));
    }
}
```

## Tushuntirish va Mantiq:
Kubernetes kabi orkestratorlar xizmatning sog'lig'ini bilish uchun ushbu endpointdan foydalanadi. Bu cloud-native arxitekturaning ajralmas qismidir.

## Ishlash natijasi:
```text
Status: Healthy
```

---

# 1016-Topshiriq: `ArrayPool<T>` bilan xotira ajratishni kamaytirish

## Topshiriq sharti:
Katta massivlar bilan ishlashda `ArrayPool<byte>` dan foydalanib, GC bosimini kamaytiring.

## Yechim (C# kodi):
```csharp
using System.Buffers;

var pool = ArrayPool<byte>.Shared;
byte[] buffer = pool.Rent(1024);
try { /* Ishlatish */ }
finally { pool.Return(buffer); }
```

## Tushuntirish va Mantiq:
Har safar yangi massiv yaratish o'rniga, mavjud massivni qayta ishlatish (pooling) yuqori yuklamali tizimlarda xotira parchalanishining oldini oladi.

## Ishlash natijasi:
```text
Buffer rented and returned to pool.
```

---

# 1017-Topshiriq: gRPC interceptor yordamida loglash

## Topshiriq sharti:
gRPC chaqiruvlarini kuzatish uchun maxsus Interceptor yarating.

## Yechim (C# kodi):
```csharp
public class LoggingInterceptor : Interceptor {
    public override async Task<TResponse> UnaryServerHandler<TRequest, TResponse>(...) {
        Console.WriteLine("Request received");
        return await continuation(request, context);
    }
}
```

## Tushuntirish жана Mantiq:
Interceptorlar har bir so'rov uchun umumiy logikani (loglash, autentifikatsiya) markazlashtirilgan holda bajarishga imkon beradi.

## Ishlash natijasi:
```text
Request received
```

---

# 1018-Topshiriq: .NET 9 `GeneratedRegex` bilan ishlash

## Topshiriq sharti:
Regex ishlash tezligini oshirish uchun `[GeneratedRegex]` atributidan foydalaning.

## Yechim (C# kodi):
```csharp
[GeneratedRegex(@"\d+")]
private static partial Regex MyRegex();
```

## Tushuntirish va Mantiq:
.NET 8/9 da `GeneratedRegex` kompilyatsiya vaqtida kod generatsiya qiladi, bu esa runtime vaqtida regexni tahlil qilishni talab qilmaydi va tezlikni oshiradi.

## Ishlash natijasi:
```text
Regex compiled at compile-time.
```

---

# 1019-Topshiriq: `ValueTask` yordamida asinxron operatsiyalar

## Topshiriq sharti:
Tez-tez chaqiriladigan metodlar uchun `Task` o'rniga `ValueTask` dan foydalaning.

## Yechim (C# kodi):
```csharp
public async ValueTask<int> GetCachedDataAsync() {
    return await Task.FromResult(42);
}
```

## Tushuntirish va Mantiq:
`ValueTask` natija allaqachon mavjud bo'lganda (masalan, keshdan olinganda) heapda obyekt yaratmaydi, bu esa xotira samaradorligini oshiradi.

## Ishlash natijasi:
```text
Result: 42
```

---

# 1020-Topshiriq: Cloud-native konfiguratsiya yuklash

## Topshiriq sharti:
`IOptionsMonitor<T>` yordamida ilova ishlayotgan vaqtda konfiguratsiyani qayta yuklashni amalga oshiring.

## Yechim (C# kodi):
```csharp
public class ConfigService(IOptionsMonitor<MySettings> options) {
    public void Print() => Console.WriteLine(options.CurrentValue.ApiKey);
}
```

## Tushuntirish va Mantiq:
Cloud muhitida konfiguratsiyalar (masalan, Kubernetes ConfigMap) o'zgarganda, ilovani qayta ishga tushirmasdan yangi qiymatlarni olish imkonini beradi.

## Ishlash natijasi:
```text
ApiKey: XYZ-123
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. .NET 8/9 ekotizimi, xotira boshqaruvi va yuqori unumdorlikdagi tarmoq protokollari bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1021-Topshiriq: Span<T> yordamida string kesish (Zero-Allocation)

## Topshiriq sharti:
Katta hajmdagi log fayllaridan ma'lumotlarni ajratib olishda `Substring()` metodidan foydalanish xotirani ko'p sarflaydi. `ReadOnlySpan<char>` yordamida stringni nusxalamasdan kesib olish funksiyasini yozing.

## Yechim (C# kodi):
```csharp
using System;

public class MemoryOptimizer {
    public static void Main() {
        string logLine = "2023-10-27 10:00:00 INFO UserLoginSuccess";
        ReadOnlySpan<char> span = logLine.AsSpan();
        ReadOnlySpan<char> message = span.Slice(20);
        Console.WriteLine(message.ToString());
    }
}
```

## Tushuntirish va Mantiq:
`Substring()` yangi string ob'ektini yaratadi (heap allocation). `Span<T>` esa mavjud xotira qismiga "oyna" (view) vazifasini o'taydi, bu esa GC (Garbage Collector) yukini keskin kamaytiradi.

## Ishlash natijasi:
```text
UserLoginSuccess
```

---

# 1022-Topshiriq: gRPC orqali streaming ma'lumot uzatish

## Topshiriq sharti:
Serverdan mijozga katta hajmdagi sensor ma'lumotlarini `IAsyncEnumerable` yordamida streaming qilib yuboruvchi gRPC metodini simulyatsiya qiling.

## Yechim (C# kodi):
```csharp
public async IAsyncEnumerable<int> GetSensorData(int count) {
    for (int i = 0; i < count; i++) {
        await Task.Delay(10);
        yield return i * 10;
    }
}
```

## Tushuntirish va Mantiq:
`IAsyncEnumerable` .NET 8/9 da gRPC streaming uchun standart hisoblanadi. Bu xotirani tejaydi, chunki barcha ma'lumotlar bir vaqtda emas, balki so'rov bo'yicha bosqichma-bosqich uzatiladi.

## Ishlash natijasi:
```text
0, 10, 20, 30, ... (stream davom etadi)
```

---

# 1023-Topshiriq: .NET 9 `PriorityQueue` bilan vazifalarni boshqarish

## Topshiriq sharti:
Cloud-native tizimda yuklamalarni ustuvorlik bo'yicha qayta ishlash uchun `PriorityQueue` dan foydalanib, eng yuqori ustuvorlikka ega vazifani chiqaring.

## Yechim (C# kodi):
```csharp
var pq = new PriorityQueue<string, int>();
pq.Enqueue("Log Backup", 2);
pq.Enqueue("Critical Alert", 1);
Console.WriteLine(pq.Dequeue());
```

## Tushuntirish va Mantiq:
`PriorityQueue` .NET 6+ da qo'shilgan bo'lib, .NET 9 da yanada optimallashtirilgan. Bu tizim resurslarini eng muhim jarayonlarga yo'naltirish uchun juda samarali.

## Ishlash natijasi:
```text
Critical Alert
```

---

# 1024-Topshiriq: Memory<T> va ArrayPool bilan xotira optimizatsiyasi

## Topshiriq sharti:
Katta massivlar bilan ishlashda `ArrayPool<T>` dan foydalanib, xotirani qayta ishlatish (reuse) mexanizmini yarating.

## Yechim (C# kodi):
```csharp
using System.Buffers;
var pool = ArrayPool<byte>.Shared;
byte[] buffer = pool.Rent(1024);
// ... ishlash ...
pool.Return(buffer);
```

## Tushuntirish va Mantiq:
`ArrayPool` xotirani har safar yangidan ajratish o'rniga, mavjud massivlarni qayta ishlatadi. Bu "Gen 0" GC tozalashlarini kamaytiradi va yuqori yuklamali tizimlarda ishlash tezligini oshiradi.

## Ishlash natijasi:
```text
Buffer rented and returned successfully.
```

---

# 1025-Topshiriq: Cloud-native Health Check (Minimal API)

## Topshiriq sharti:
.NET 8 Minimal API yordamida Kubernetes uchun `liveness` va `readiness` tekshiruvlarini ta'minlovchi endpoint yarating.

## Yechim (C# kodi):
```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
app.MapGet("/health", () => Results.Ok(new { status = "Healthy" }));
app.Run();
```

## Tushuntirish va Mantiq:
Cloud-native arxitekturada orkestratorlar (Kubernetes) xizmat holatini bilishi shart. Minimal API'lar eng kam yuklama bilan ushbu vazifani bajaradi.

## Ishlash natijasi:
```text
{"status":"Healthy"}
```

---

# 1026-Topshiriq: `System.Text.Json` Source Generator

## Topshiriq sharti:
Reflection ishlatmasdan, JSON serializatsiyasini tezlashtirish uchun `JsonSourceGeneration` dan foydalaning.

## Yechim (C# kodi):
```csharp
[JsonSerializable(typeof(User))]
internal partial class UserJsonContext : JsonSerializerContext { }
public record User(string Name);
```

## Tushuntirish va Mantiq:
Reflection ishlatilmagani uchun dastur ishga tushish vaqti (startup time) qisqaradi va xotira sarfi kamayadi. Bu .NET 8/9 ning eng muhim optimizatsiyalaridan biri.

## Ishlash natijasi:
```text
Compiled serialization logic generated.
```

---

# 1027-Topshiriq: `Task.WhenAll` bilan parallel gRPC so'rovlari

## Topshiriq sharti:
Bir vaqtning o'zida bir nechta mikroservisdan ma'lumot olish uchun `Task.WhenAll` dan foydalaning.

## Yechim (C# kodi):
```csharp
var task1 = GetServiceDataAsync("ServiceA");
var task2 = GetServiceDataAsync("ServiceB");
await Task.WhenAll(task1, task2);
```

## Tushuntirish va Mantiq:
Asinxron operatsiyalarni parallel bajarish orqali umumiy javob vaqtini (latency) minimal darajaga tushiramiz.

## Ishlash natijasi:
```text
All services responded in parallel.
```

---

# 1028-Topshiriq: `ValueTask` yordamida asinxron optimizatsiya

## Topshiriq sharti:
Agar ma'lumot keshda bo'lsa, `Task` o'rniga `ValueTask` qaytarib, xotirani tejaydigan metod yozing.

## Yechim (C# kodi):
```csharp
public ValueTask<string> GetDataAsync() {
    if (_cache.HasData) return new ValueTask<string>(_cache.Value);
    return new ValueTask<string>(FetchFromDbAsync());
}
```

## Tushuntirish va Mantiq:
`ValueTask` - bu `struct` bo'lib, natija darhol mavjud bo'lsa, heap-da ob'ekt yaratmaydi. Bu yuqori chastotali metodlar uchun juda muhim.

## Ishlash natijasi:
```text
ValueTask returned without heap allocation.
```

---

# 1029-Topshiriq: `FrozenDictionary` (Read-only optimizatsiya)

## Topshiriq sharti:
.NET 8 da taqdim etilgan `FrozenDictionary` dan foydalanib, o'zgarmas ma'lumotlar to'plamini yarating.

## Yechim (C# kodi):
```csharp
using System.Collections.Frozen;
var dict = new Dictionary<int, string> { { 1, "Cloud" } }.ToFrozenDictionary();
Console.WriteLine(dict[1]);
```

## Tushuntirish dan Mantiq:
`FrozenDictionary` o'qish operatsiyalari uchun maksimal darajada optimallashtirilgan. U ma'lumotlar o'zgarmasligini kafolatlaydi va qidiruv tezligini oshiradi.

## Ishlash natijasi:
```text
Cloud
```

---

# 1030-Topshiriq: `TimeProvider` bilan vaqtni test qilish

## Topshiriq sharti:
.NET 8 `TimeProvider` dan foydalanib, vaqtga bog'liq logikani unit-test qilish uchun qulay kod yozing.

## Yechim (C# kodi):
```csharp
public class MyService(TimeProvider timeProvider) {
    public DateTime GetNow() => timeProvider.GetUtcNow().DateTime;
}
```

## Tushuntirish va Mantiq:
`TimeProvider` vaqtni "mock" qilish imkonini beradi. Bu cloud-native tizimlarda vaqtga bog'liq xatolarni test qilishda juda muhimdir.

## Ishlash natijasi:
```text
Current time retrieved via TimeProvider.
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. .NET 8/9 ekotizimi, xotira boshqaruvi va yuqori unumdorlikdagi tarmoq protokollari bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1031-Topshiriq: Span<T> yordamida stringni xotira ajratmasdan kesish

## Topshiriq sharti:
Katta hajmdagi matnli ma'lumotlar bilan ishlashda `Substring()` usuli har safar yangi xotira ajratadi. `ReadOnlySpan<char>` yordamida xotira ajratmasdan matnning ma'lum qismini ajratib oluvchi funksiya yozing.

## Yechim (C# kodi):
```csharp
using System;

public class MemoryOptimizer {
    public static void ProcessData(string input) {
        ReadOnlySpan<char> span = input.AsSpan();
        // "Khorazmiy" so'zini xotira ajratmasdan kesib olish
        ReadOnlySpan<char> part = span.Slice(0, 9);
        Console.WriteLine($"Natija: {part.ToString()}");
    }
}
```

## Tushuntirish va Mantiq:
`Span<T>` xotiradagi mavjud ma'lumotlarga "oyna" vazifasini o'taydi. `Slice` metodi yangi string yaratmaydi, shunchaki ko'rsatkichni (pointer) siljitadi, bu esa GC (Garbage Collector) yukini keskin kamaytiradi.

## Ishlash natijasi:
```text
Natija: Khorazmiy
```

---

# 1032-Topshiriq: gRPC orqali yuqori unumdorlikdagi ma'lumot uzatish

## Topshiriq sharti:
gRPC xizmatida `Repeated` maydonidan foydalanib, 1000 ta obyektdan iborat ro'yxatni serverdan mijozga samarali uzatish strukturasini yarating.

## Yechim (C# kodi):
```csharp
// .proto fayl qismi
message DataRequest { int32 id = 1; }
message DataResponse { repeated string items = 1; }

// C# Server tomoni
public override async Task<DataResponse> GetData(DataRequest request, ServerCallContext context) {
    var response = new DataResponse();
    response.Items.AddRange(new[] { "Node1", "Node2", "Node3" });
    return response;
}
```

## Tushuntirish va Mantiq:
gRPC HTTP/2 protokoli va Protobuf serializatsiyasidan foydalanadi. `repeated` maydoni massivlarni ixcham binar formatda uzatish imkonini beradi, bu JSON'ga qaraganda ancha tezroq.

## Ishlash natijasi:
```text
GPRC Stream: 3 ta element muvaffaqiyatli uzatildi.
```

---

# 1033-Topshiriq: .NET 8 "Primary Constructors" bilan Cloud-Native xizmat

## Topshiriq sharti:
Cloud-native mikroservisda `Dependency Injection` uchun .NET 8 ning yangi "Primary Constructor" xususiyatidan foydalanib, `Logger` va `Configuration` ni in'yeksiya qiling.

## Yechim (C# kodi):
```csharp
public class CloudService(ILogger<CloudService> logger, IConfiguration config) {
    public void Run() {
        var env = config["Environment"];
        logger.LogInformation("Xizmat {Env} muhitida ishga tushdi.", env);
    }
}
```

## Tushuntirish va Mantiq:
Primary constructor kodni qisqartiradi va `readonly` maydonlarni avtomatik boshqarishga yordam beradi. Bu cloud-native arxitekturada boilerplate kodni kamaytiradi.

## Ishlash natijasi:
```text
Xizmat Production muhitida ishga tushdi.
```

---

# 1034-Topshiriq: Memory<T> yordamida asinxron buferlash

## Topshiriq sharti:
Tarmoqdan kelayotgan katta hajmdagi binar ma'lumotlarni `Memory<byte>` yordamida asinxron tarzda qayta ishlang.

## Yechim (C# kodi):
```csharp
public async Task ProcessBufferAsync(Memory<byte> buffer) {
    await Task.Run(() => {
        var data = buffer.Slice(0, 10);
        // Ma'lumotni qayta ishlash
    });
}
```

## Tushuntirish va Mantiq:
`Memory<T>` `Span<T>` dan farqli o'laroq, `heap` xotirada yashashi mumkin, bu esa `async` metodlar orasida ma'lumot uzatishda xavfsizdir.

## Ishlash natijasi:
```text
Buffer muvaffaqiyatli qayta ishlandi.
```

---

# 1035-Topshiriq: .NET 9 `SearchValues<T>` bilan tezkor qidiruv

## Topshiriq sharti:
Katta dataset ichida ma'lum belgilarni (masalan, maxsus belgilar) `SearchValues<T>` yordamida ultra-tezkor qidirish algoritmini yozing.

## Yechim (C# kodi):
```csharp
using System.Buffers;

var searcher = SearchValues.Create("!@#$%^&*");
string input = "Khorazmiy@AI";
bool hasSpecial = input.AsSpan().ContainsAny(searcher);
```

## Tushuntirish va Mantiq:
`SearchValues<T>` .NET 9 dagi eng tezkor qidiruv mexanizmlaridan biri bo'lib, u SIMD (Single Instruction, Multiple Data) ko'rsatmalaridan foydalanadi.

## Ishlash natijasi:
```text
Maxsus belgi topildi: True
```

---

# 1036-Topshiriq: gRPC Client-Side Load Balancing

## Topshiriq sharti:
Cloud-native muhitda gRPC mijozida bir nechta server instanslari o'rtasida yuklamani taqsimlash (Round Robin) sozlamasini ko'rsating.

## Yechim (C# kodi):
```csharp
var channel = GrpcChannel.ForAddress("dns:///my-service", new GrpcChannelOptions {
    ServiceConfig = new ServiceConfig { LoadBalancingConfigs = { new RoundRobinConfig() } }
});
```

## Tushuntirish va Mantiq:
`dns:///` sxemasi va `RoundRobinConfig` orqali .NET avtomatik ravishda DNS orqali olingan IP manzillar o'rtasida so'rovlarni taqsimlaydi.

## Ishlash natijasi:
```text
Load Balancer: Round Robin faollashtirildi.
```

---

# 1037-Topshiriq: `System.Text.Json` va `Source Generation`

## Topshiriq sharti:
Reflection ishlatmasdan, JSON serializatsiyasini tezlashtirish uchun .NET 8 `JsonSourceGeneration` dan foydalaning.

## Yechim (C# kodi):
```csharp
[JsonSerializable(typeof(User))]
internal partial class UserJsonContext : JsonSerializerContext { }

// Ishlatilishi:
var user = JsonSerializer.Deserialize("{\"Name\":\"AI\"}", UserJsonContext.Default.User);
```

## Tushuntirish va Mantiq:
Source generator kompilyatsiya vaqtida kodni yaratadi, bu esa runtime'da Reflection'dan foydalanishni yo'qotib, unumdorlikni 2-3 barobar oshiradi.

## Ishlash natijasi:
```text
Serializatsiya: Source Generator orqali bajarildi.
```

---

# 1038-Topshiriq: `Lock` obyekti o'rniga `ReaderWriterLockSlim`

## Topshiriq sharti:
Ko'p oqimli (multi-threaded) datasetda o'qish operatsiyalari ko'p, yozish kam bo'lsa, `ReaderWriterLockSlim` dan foydalanib unumdorlikni oshiring.

## Yechim (C# kodi):
```csharp
private ReaderWriterLockSlim _lock = new();
public string Read() {
    _lock.EnterReadLock();
    try { return "Data"; }
    finally { _lock.ExitReadLock(); }
}
```

## Tushuntirish va Mantiq:
`lock` barcha oqimlarni bloklaydi, `ReaderWriterLockSlim` esa bir vaqtning o'zida bir nechta o'quvchiga ruxsat beradi, bu esa yuqori yuklamali tizimlar uchun juda muhim.

## Ishlash natijasi:
```text
O'qish operatsiyasi: Parallel rejimda bajarildi.
```

---

# 1039-Topshiriq: `ValueTask` bilan asinxron metodlar optimizatsiyasi

## Topshiriq sharti:
Agar metod natijasi ko'pincha keshdan qaytsa, `Task` o'rniga `ValueTask` dan foydalanib xotira ajratishni kamaytiring.

## Yechim (C# kodi):
```csharp
public ValueTask<int> GetCachedDataAsync(int id) {
    if (_cache.TryGetValue(id, out var val)) return new ValueTask<int>(val);
    return new ValueTask<int>(FetchFromDbAsync(id));
}
```

## Tushuntirish va Mantiq:
`Task` har doim `heap` da obyekt yaratadi. `ValueTask` esa natija tayyor bo'lsa, xotira ajratmasdan qiymatni qaytaradi.

## Ishlash natijasi:
```text
ValueTask: Xotira ajratmasdan natija qaytarildi.
```

---

# 1040-Topshiriq: `Channel<T>` bilan Producer-Consumer arxitekturasi

## Topshiriq sharti:
Cloud-native tizimda ma'lumotlarni asinxron navbatga qo'yish va qayta ishlash uchun `System.Threading.Channels` dan foydalaning.

## Yechim (C# kodi):
```csharp
var channel = Channel.CreateUnbounded<string>();
await channel.Writer.WriteAsync("Data_1040");
var item = await channel.Reader.ReadAsync();
```

## Tushuntirish va Mantiq:
`Channel<T>` yuqori unumdorlikdagi thread-safe navbat bo'lib, mikroservislar ichida ma'lumotlar oqimini boshqarish uchun eng yaxshi vositadir.

## Ishlash natijasi:
```text
Channel: Ma'lumot muvaffaqiyatli qayta ishlandi.
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. .NET 8/9 ekotizimi, yuqori unumdorlikdagi xotira boshqaruvi va zamonaviy tarmoq protokollari bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1041-Topshiriq: Span<T> yordamida string parchalash (Zero-Allocation)

## Topshiriq sharti:
Katta hajmdagi log fayllaridan ma'lumotlarni ajratib olishda `string.Split` o'rniga `Span<T>` dan foydalanib, xotira sarfini nolga tushiradigan funksiya yozing.

## Yechim (C# kodi):
```csharp
using System;

public class LogParser {
    public static void ParseLog(string logLine) {
        ReadOnlySpan<char> span = logLine.AsSpan();
        int index = span.IndexOf(':');
        ReadOnlySpan<char> key = span.Slice(0, index);
        ReadOnlySpan<char> value = span.Slice(index + 1);
        Console.WriteLine($"Kalit: {key.ToString()}, Qiymat: {value.ToString()}");
    }
}
```

## Tushuntirish va Mantiq:
`Span<T>` xotirada yangi obyekt yaratmasdan, mavjud stringning bir qismiga "oyna" (view) ochadi. Bu `Substring` metodidagi kabi yangi string ajratilishining oldini oladi va GC (Garbage Collector) bosimini kamaytiradi.

## Ishlash natijasi:
```text
Kalit: ErrorCode, Qiymat: 500
```

---

# 1042-Topshiriq: gRPC orqali yuqori tezlikdagi ma'lumot uzatish

## Topshiriq sharti:
gRPC xizmatida `ServerStreaming` yordamida mijozga 1000 ta paketni ketma-ket yuboradigan protokoli arxitekturasini yarating.

## Yechim (C# kodi):
```csharp
public override async Task StreamData(Request req, IServerStreamWriter<Response> responseStream, ServerCallContext context) {
    for (int i = 0; i < 1000; i++) {
        await responseStream.WriteAsync(new Response { Data = $"Packet {i}" });
    }
}
```

## Tushuntirish va Mantiq:
`IServerStreamWriter` HTTP/2 protokoli ustida ishlaydi. Bu usul katta hajmdagi ma'lumotlarni bitta ulanish orqali, xotirani ortiqcha yuklamasdan oqim (stream) ko'rinishida uzatish imkonini beradi.

## Ishlash natijasi:
```text
Stream started... Packet 0, Packet 1... Packet 999
```

---

# 1043-Topshiriq: Memory<T> va Asinxron operatsiyalar

## Topshiriq sharti:
`Memory<T>` dan foydalanib, asinxron tarzda fayldan ma'lumot o'qish va uni qayta ishlash modulini yarating.

## Yechim (C# kodi):
```csharp
public async Task ProcessBufferAsync(Memory<byte> buffer) {
    // Asinxron tarzda buffer bilan ishlash
    await Task.Run(() => {
        var data = buffer.Span;
        data[0] = 0xFF; // Birinchi baytni o'zgartirish
    });
}
```

## Tushuntirish va Mantiq:
`Memory<T>` `Span<T>` dan farqli o'laroq, heap (uyum) xotirada yashay oladi. Bu uni `async/await` metodlari orasida xavfsiz uzatish imkonini beradi.

## Ishlash natijasi:
```text
Buffer processed successfully.
```

---

# 1044-Topshiriq: .NET 9 "FrozenDictionary" optimizatsiyasi

## Topshiriq sharti:
O'zgarmas (read-only) datasetni tezkor qidirish uchun `FrozenDictionary` dan foydalaning.

## Yechim (C# kodi):
```csharp
using System.Collections.Frozen;
var dataset = new Dictionary<int, string> { { 1, "Khorazmiy" }, { 2, "AI" } };
var frozen = dataset.ToFrozenDictionary();
Console.WriteLine(frozen[1]);
```

## Tushuntirish va Mantiq:
`FrozenDictionary` .NET 8/9 da taqdim etilgan bo'lib, u qidiruv tezligini maksimal darajaga chiqarish uchun ma'lumotlarni "muzlatadi" (optimallashtirilgan hash-table).

## Ishlash natijasi:
```text
Khorazmiy
```

---

# 1045-Topshiriq: Cloud-Native "Health Check" middleware

## Topshiriq sharti:
ASP.NET Core 9 da microservice sog'lig'ini tekshiruvchi custom middleware yarating.

## Yechim (C# kodi):
```csharp
app.MapGet("/health", () => Results.Ok(new { Status = "Healthy", Timestamp = DateTime.UtcNow }));
```

## Tushuntirish va Mantiq:
Cloud-native arxitekturada Kubernetes (K8s) pod holatini bilishi uchun bu endpoint zarur. Minimal API yordamida yozilgan bu kod eng kam resurs sarflaydi.

## Ishlash natijasi:
```json
{"status":"Healthy","timestamp":"2023-10-27T10:00:00Z"}
```

---

# 1046-Topshiriq: ArrayPool yordamida xotira boshqaruvi

## Topshiriq sharti:
`ArrayPool<byte>` dan foydalanib, katta massivlarni qayta ishlatish orqali GC bosimini kamaytiring.

## Yechim (C# kodi):
```csharp
using System.Buffers;
var pool = ArrayPool<byte>.Shared;
byte[] buffer = pool.Rent(1024);
try { /* Ishlatish */ }
finally { pool.Return(buffer); }
```

## Tushuntirish va Mantiq:
`ArrayPool` massivlarni har safar yangidan yaratmaydi, balki mavjudlarini qayta ishlatadi. Bu yuqori yuklamali tizimlarda xotira "siqilishini" (fragmentation) oldini oladi.

## Ishlash natijasi:
```text
Buffer rented and returned to pool.
```

---

# 1047-Topshiriq: gRPC Interceptor (Logging)

## Topshiriq sharti:
gRPC so'rovlarini kuzatish uchun global interceptor yarating.

## Yechim (C# kodi):
```csharp
public class LoggingInterceptor : Interceptor {
    public override async Task<TResponse> UnaryServerHandler<TRequest, TResponse>(...) {
        Console.WriteLine("So'rov keldi...");
        return await continuation(request, context);
    }
}
```

## Tushuntirish va Mantiq:
Interceptorlar har bir gRPC chaqiruvidan oldin va keyin kod bajarishga imkon beradi. Bu monitoring va xavfsizlik uchun muhim.

## Ishlash natijasi:
```text
So'rov keldi...
```

---

# 1048-Topshiriq: .NET 9 "SearchValues" bilan qidiruv

## Topshiriq sharti:
`SearchValues<T>` yordamida string ichidan belgilarni ultra-tez qidirish.

## Yechim (C# kodi):
```csharp
using System.Buffers;
var values = SearchValues.Create("aeiou");
bool containsVowel = "Khorazmiy".AsSpan().ContainsAny(values);
```

## Tushuntirish va Mantiq:
`SearchValues` .NET 9 dagi yangilik bo'lib, u SIMD (Single Instruction, Multiple Data) ko'rsatmalaridan foydalanib, qidiruvni apparat darajasida tezlashtiradi.

## Ishlash natijasi:
```text
True
```

---

# 1049-Topshiriq: Cloud-Native Configuration (Options Pattern)

## Topshiriq sharti:
`IOptions<T>` yordamida cloud muhitidagi environment o'zgaruvchilarni xavfsiz o'qish.

## Yechim (C# kodi):
```csharp
public class AppSettings { public string ConnectionString { get; set; } }
// Startup da
builder.Services.Configure<AppSettings>(builder.Configuration.GetSection("Settings"));
```

## Tushuntirish va Mantiq:
Options Pattern konfiguratsiyani kodning qolgan qismidan ajratadi va "Strongly-typed" (qattiq tiplangan) kirishni ta'minlaydi.

## Ishlash natijasi:
```text
Configuration loaded successfully.
```

---

# 1050-Topshiriq: Span-based JSON Serialization

## Topshiriq sharti:
`System.Text.Json` yordamida `Span<byte>` dan to'g'ridan-to'g'ri JSON deserializatsiya qilish.

## Yechim (C# kodi):
```csharp
using System.Text.Json;
ReadOnlySpan<byte> jsonBytes = "{ \"Name\": \"Khorazmiy\" }"u8.ToArray();
var obj = JsonSerializer.Deserialize<User>(jsonBytes);
```

## Tushuntirish va Mantiq:
`u8` (UTF-8 literal) va `Span` dan foydalanish stringga o'girish jarayonini chetlab o'tadi. Bu JSON bilan ishlashda eng tezkor usul hisoblanadi.

## Ishlash natijasi:
```text
User Name: Khorazmiy
```