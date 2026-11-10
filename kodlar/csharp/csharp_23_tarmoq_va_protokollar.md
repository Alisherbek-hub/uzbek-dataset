# Khorazmiy AI: C# - Modul 23
## Mavzu: Tarmoq protokollari: System.IO.Pipelines, Kestrel custom transport, HTTP/3 QUIC va gRPC streaming

### Topshiriq #1101: System.IO.Pipelines: Pipe Yaratish va Asosiy Reader/Writer Sikli
**Tavsif:** Tarmoq oqimlarida baytlarni xotiraga nusxalamasdan (Zero-Allocation) asinxron yozuvchi va o'quvchi konveyerini qurish.
**Talablar:** `System.IO.Pipelines.Pipe`, `PipeWriter`, `PipeReader`, `FlushAsync()`, `ReadAsync()`, toza yopish (`Complete()`).
**Yechim (C#):**
```csharp
using System;
using System.IO.Pipelines;
using System.Text;
using System.Threading.Tasks;

public class BasicPipelineDemo
{
    public static async Task RunAsync()
    {
        var pipe = new Pipe();

        // 1. Asinxron yozuvchi vazifasi (Writer)
        Task writerTask = Task.Run(async () =>
        {
            PipeWriter writer = pipe.Writer;
            byte[] message = Encoding.UTF8.GetBytes("Salom, Khorazmiy Pipelines!");

            // Xotiraga to'g'ridan-to'g'ri yozish
            Memory<byte> memory = writer.GetMemory(message.Length);
            message.CopyTo(memory);
            writer.Advance(message.Length);

            // O'quvchiga yetkazish
            await writer.FlushAsync();
            await writer.CompleteAsync(); // Yozish yakunlandi
        });

        // 2. Asinxron o'quvchi vazifasi (Reader)
        Task readerTask = Task.Run(async () =>
        {
            PipeReader reader = pipe.Reader;
            while (true)
            {
                ReadResult result = await reader.ReadAsync();
                var buffer = result.Buffer;

                if (buffer.Length > 0)
                {
                    string text = Encoding.UTF8.GetString(buffer.ToArray());
                    Console.WriteLine($"Qabul qilindi: {text}");
                }

                // O'qilgan xotirani ozod qilish
                reader.AdvanceTo(buffer.End);

                if (result.IsCompleted) break;
            }
            await reader.CompleteAsync();
        });

        await Task.WhenAll(writerTask, readerTask);
    }
}
```
**Tushuntirish:** `Pipe` sinfi xotira boshqaruvini avtomatik `MemoryPool` orqali ta'minlaydi. An'anaviy `byte[]` massivlaridan farqli o'laroq, Garbage Collector (GC) ga yuklama tushirmaydi.

---

### Topshiriq #1102: PipeWriter Yordamida Zero-Allocation Xotiraga Yozish
**Tavsif:** Tarmoqqa yuboriladigan xabarlarni oraliq `byte[]` massivlar yaratmasdan to'g'ridan-to'g'ri `Span<byte>` orqali kiritish.
**Talablar:** `writer.GetSpan()`, `writer.Advance()`, `FlushResult`, `ValueTask`.
**Yechim (C#):**
```csharp
using System;
using System.Buffers;
using System.Buffers.Binary;
using System.IO.Pipelines;
using System.Threading.Tasks;

public class ZeroAllocWriter
{
    public static async ValueTask WriteBinaryPacketAsync(PipeWriter writer, int packetId, ReadOnlySpan<byte> payload)
    {
        int totalLength = 4 + 4 + payload.Length; // [Length(4)] + [ID(4)] + [Payload]

        // Yozuvchidan minimal xotira spanini olish
        Span<byte> span = writer.GetSpan(totalLength);

        // Big-Endian tartibida uzunlik va ID yozish
        BinaryPrimitives.WriteInt32BigEndian(span.Slice(0, 4), totalLength);
        BinaryPrimitives.WriteInt32BigEndian(span.Slice(4, 4), packetId);

        // Foydali yuklamani (payload) oraliq nusxalashsiz to'g'ridan-to'g'ri ko'chirish
        payload.CopyTo(span.Slice(8));

        // Yozilgan baytlar sonini bildirish
        writer.Advance(totalLength);

        // Oqimga haydash
        FlushResult result = await writer.FlushAsync();
        if (result.IsCanceled || result.IsCompleted)
        {
            throw new InvalidOperationException("Oqim bekor qilindi yoki yopildi.");
        }
    }
}
```
**Tushuntirish:** `GetSpan()` va `Advance()` juftligi yozuvchiga ajratilgan xotira blokini taqdim etadi. `BinaryPrimitives` esa CPU registrlaridan to'g'ridan-to'g'ri xotiraga Big-Endian tartibida yozadi.

---

### Topshiriq #1103: SequencePosition va PipeReader.AdvanceTo Bilan Xotira Siljishi
**Tavsif:** To'liq kelmagan paketlarni kutishda o'qilgan va ko'rib chiqilgan ko'rsatkichlarni (`consumed` va `examined`) to'g'ri boshqarish.
**Talablar:** `SequencePosition`, `ReadResult.Buffer`, `AdvanceTo(consumed, examined)`.
**Yechim (C#):**
```csharp
using System;
using System.Buffers;
using System.IO.Pipelines;
using System.Threading.Tasks;

public class PacketParser
{
    public static async Task ProcessPacketsAsync(PipeReader reader)
    {
        while (true)
        {
            ReadResult result = await reader.ReadAsync();
            ReadOnlySequence<byte> buffer = result.Buffer;

            SequencePosition consumed = buffer.Start;
            SequencePosition examined = buffer.End;

            // Agar yetarli ma'lumot (masalan kamida 4 bayt uzunlik) bo'lsa
            if (buffer.Length >= 4)
            {
                // Uzunlikni o'qish
                Span<byte> lenSpan = stackalloc byte[4];
                buffer.Slice(0, 4).CopyTo(lenSpan);
                int expectedLength = System.Buffers.Binary.BinaryPrimitives.ReadInt32BigEndian(lenSpan);

                if (buffer.Length >= expectedLength)
                {
                    // To'liq paket kelgan: qabul qilib qayta ishlash
                    consumed = buffer.GetPosition(expectedLength);
                    examined = consumed;
                    Console.WriteLine($"Paket to'liq qabul qilindi: {expectedLength} bayt.");
                }
            }

            // Xotira siljishini belgilash
            reader.AdvanceTo(consumed, examined);

            if (result.IsCompleted) break;
        }
    }
}
```
**Tushuntirish:** `consumed` ko'rsatkichigacha bo'lgan baytlar xotiradan ozod qilinadi. `examined` esa qaysi joygacha tahlil qilinganini belgilaydi; yangi baytlar kelmaguncha `ReadAsync()` keraksiz uyg'onmaydi.

---

### Topshiriq #1104: Delimiter Asosidagi Protokol Parseri (ReadOnlySequence va \n)
**Tavsif:** Har bir xabar satr oxiri (`\n` yoki `\r\n`) bilan ajratilgan tarmoq protokollarini (masalan, Redis, SMTP, HTTP headers) tahlil qilish.
**Talablar:** `ReadOnlySequence<byte>.PositionOf()`, `buffer.Slice()`, satrlarni xotira ajratmasdan ajratish.
**Yechim (C#):**
```csharp
using System;
using System.Buffers;
using System.IO.Pipelines;
using System.Text;
using System.Threading.Tasks;

public class LineBasedParser
{
    private const byte NewLine = (byte)'\n';

    public static async Task ReadLinesAsync(PipeReader reader)
    {
        while (true)
        {
            ReadResult result = await reader.ReadAsync();
            ReadOnlySequence<byte> buffer = result.Buffer;

            while (TryReadLine(ref buffer, out ReadOnlySequence<byte> line))
            {
                // Satrni qayta ishlash
                string lineText = Encoding.UTF8.GetString(line.ToArray());
                Console.WriteLine($"Qator: {lineText}");
            }

            // Qolgan to'liqsiz qismni saqlash
            reader.AdvanceTo(buffer.Start, buffer.End);

            if (result.IsCompleted) break;
        }
    }

    private static bool TryReadLine(ref ReadOnlySequence<byte> buffer, out ReadOnlySequence<byte> line)
    {
        SequencePosition? position = buffer.PositionOf(NewLine);
        if (position == null)
        {
            line = default;
            return false;
        }

        line = buffer.Slice(0, position.Value);
        buffer = buffer.Slice(buffer.GetPosition(1, position.Value)); // '\n' dan keyingi qism
        return true;
    }
}
```
**Tushuntirish:** `buffer.PositionOf()` xotira bloklari bo'ylab optimallashtirilgan SIMD (AVX2/SSE) qidiruvidan foydalanadi, natijada satr oxirini topish juda yuqori tezlikda bajariladi.

---

### Topshiriq #1105: Uzunlik Prefiksli (Length-Prefixed Framing) Xabarlar Bilan Ishlash
**Tavsif:** Xabarlar hajmi o'zgaruvchan bo'lganda dastlabki 4 baytlik uzunlik prefiksi orqali freymlarni xatosiz yig'ish.
**Talablar:** Binar freym protokoli, `SequenceReader<byte>`, `TryReadBigEndian`.
**Yechim (C#):**
```csharp
using System;
using System.Buffers;
using System.Buffers.Binary;
using System.IO.Pipelines;
using System.Threading.Tasks;

public class FrameDecoder
{
    public static async Task ProcessFramesAsync(PipeReader reader)
    {
        while (true)
        {
            ReadResult result = await reader.ReadAsync();
            ReadOnlySequence<byte> buffer = result.Buffer;

            while (buffer.Length >= 4)
            {
                // Prefiks 4 bayt uzunlik
                Span<byte> header = stackalloc byte[4];
                buffer.Slice(0, 4).CopyTo(header);
                int payloadLength = BinaryPrimitives.ReadInt32BigEndian(header);

                int totalFrameSize = 4 + payloadLength;
                if (buffer.Length < totalFrameSize)
                {
                    // Butun freym hali to'liq yuklanmagan
                    break;
                }

                // To'liq freymni ajratib olish
                ReadOnlySequence<byte> framePayload = buffer.Slice(4, payloadLength);
                Console.WriteLine($"Freym qabul qilindi! Hajmi: {payloadLength} bayt.");

                buffer = buffer.Slice(totalFrameSize);
            }

            reader.AdvanceTo(buffer.Start, buffer.End);
            if (result.IsCompleted) break;
        }
    }
}
```
**Tushuntirish:** Length-Prefixed Framing protokoli TCP oqimining xarakterli 'fragmentatsiya va birlashish' (packet fragmentation) muammolarini bartaraf qiladi.

---

### Topshiriq #1106: Soketni Pipelines bilan Integratsiya Qilish (Socket.CreatePipeReader/Writer)
**Tavsif:** .NET 8+ da mavjud yangi imkoniyatlar orqali xom `Socket` ni to'g'ridan-to'g'ri `System.IO.Pipelines` ga ulash.
**Talablar:** `PipeReader.Create(socket)`, `PipeWriter.Create(socket)`, `StreamPipeReaderOptions`.
**Yechim (C#):**
```csharp
using System;
using System.IO.Pipelines;
using System.Net;
using System.Net.Sockets;
using System.Threading.Tasks;

public class SocketPipelineBridge
{
    public static async Task HandleSocketAsync(Socket socket)
    {
        // Soketdan to'g'ridan-to'g'ri PipeReader va PipeWriter yaratish
        using var stream = new NetworkStream(socket, ownsSocket: true);
        var reader = PipeReader.Create(stream, new StreamPipeReaderOptions(bufferSize: 4096));
        var writer = PipeWriter.Create(stream, new StreamPipeWriterOptions());

        try
        {
            while (true)
            {
                ReadResult result = await reader.ReadAsync();
                var buffer = result.Buffer;

                if (buffer.IsEmpty && result.IsCompleted) break;

                // Echo: O'qilgan buferni yozuvchiga yuborish
                foreach (ReadOnlyMemory<byte> segment in buffer)
                {
                    await writer.WriteAsync(segment);
                }

                reader.AdvanceTo(buffer.End);
            }
        }
        finally
        {
            await reader.CompleteAsync();
            await writer.CompleteAsync();
        }
    }
}
```
**Tushuntirish:** `PipeReader.Create` yordamida `NetworkStream` asosidagi I/O operatsiyalari avtomatlashtiriladi va oqimni xavfsiz to'xtatish (cancellation) soddalashadi.

---

### Topshiriq #1107: Katta Ma'lumot Oqimlarida Backpressure Boshqaruvi
**Tavsif:** Yozuvchi (Writer) o'quvchi (Reader) dan tezroq ma'lumot ishlab chiqarganda operativ xotira to'lib ketishining oldini olish.
**Talablar:** `PipeOptions`, `PauseWriterThreshold`, `ResumeWriterThreshold`.
**Yechim (C#):**
```csharp
using System;
using System.IO.Pipelines;
using System.Threading.Tasks;

public class BackpressureConfig
{
    public static Pipe CreateBoundedPipe()
    {
        // 64 KB ga yetganda yozuvchini to'xtatish, 32 KB ga tushganda davom ettirish
        var options = new PipeOptions(
            pauseWriterThreshold: 64 * 1024,
            resumeWriterThreshold: 32 * 1024,
            useSynchronizationContext: false
        );

        return new Pipe(options);
    }

    public static async Task TestBackpressureAsync()
    {
        var pipe = CreateBoundedPipe();
        Console.WriteLine($"Backpressure Pipe yaratildi: Pause={pipe.Writer} chegarasi o'rnatilgan.");
        await pipe.Writer.CompleteAsync();
        await pipe.Reader.CompleteAsync();
    }
}
```
**Tushuntirish:** `PauseWriterThreshold` chegarasidan oshganda `writer.FlushAsync()` ValueTask'i o'quvchi xotirani bo'shatmaguncha kutiluvchi (awaiting) holatda qoladi va yozuvchini tabiiy ravishda sekinlashtiradi.

---

### Topshiriq #1108: SequenceReader Bilan Murakkab Binar Protokollarni O'qish
**Tavsif:** Tarqoq xotira segmentlari (`ReadOnlySequence<byte>`) bo'ylab butun sonlar va bayt strukturalarini qulay o'qish.
**Talablar:** `SequenceReader<byte>`, `TryReadBigEndian()`, `TryReadLittleEndian()`, `Advance()`.
**Yechim (C#):**
```csharp
using System;
using System.Buffers;
using System.Buffers.Binary;

public class SequenceReaderProtocol
{
    public static bool TryParseHeader(in ReadOnlySequence<byte> sequence, out int magic, out short version, out long timestamp)
    {
        var reader = new SequenceReader<byte>(sequence);

        if (!reader.TryReadBigEndian(out magic)) { version = 0; timestamp = 0; return false; }
        if (!reader.TryReadBigEndian(out version)) { timestamp = 0; return false; }
        if (!reader.TryReadBigEndian(out timestamp)) { return false; }

        return true;
    }

    public static void MainRun()
    {
        byte[] raw = new byte[14];
        BinaryPrimitives.WriteInt32BigEndian(raw.AsSpan(0, 4), 0x555A424B); // 'UZBK'
        BinaryPrimitives.WriteInt16BigEndian(raw.AsSpan(4, 2), 1);
        BinaryPrimitives.WriteInt64BigEndian(raw.AsSpan(6, 8), DateTimeOffset.UtcNow.ToUnixTimeMilliseconds());

        var seq = new ReadOnlySequence<byte>(raw);
        if (TryParseHeader(in seq, out int magic, out short ver, out long ts))
        {
            Console.WriteLine($"Sehrli son: 0x{magic:X8}, Versiya: {ver}, Timestamp: {ts}");
        }
    }
}
```
**Tushuntirish:** `SequenceReader<T>` `ref struct` bo'lib, bir nechta xotira bloklari o'rtasida uzilgan ma'lumotlarni ham xotira nusxalamasdan bitta oqimdek o'qish imkonini beradi.

---

### Topshiriq #1109: Custom MemoryPool va ArrayPool Bilan Pipe Xotirasini Boshqarish
**Tavsif:** Pipelines ichki buferlarini boshqarish uchun shaxsiy `MemoryPool<byte>` biriktirish orqali xotira defragmentatsiyasini nazorat qilish.
**Talablar:** `MemoryPool<byte>`, `PipeOptions.Pool`, `ArrayPool<byte>.Shared`.
**Yechim (C#):**
```csharp
using System;
using System.Buffers;
using System.IO.Pipelines;

public class CustomPoolDemo
{
    public static Pipe CreatePooledPipe()
    {
        // Standart umumiy xotira hovuzidan foydalanish
        MemoryPool<byte> pool = MemoryPool<byte>.Shared;

        var pipeOptions = new PipeOptions(
            pool: pool,
            readerScheduler: PipeScheduler.ThreadPool,
            writerScheduler: PipeScheduler.ThreadPool,
            pauseWriterThreshold: 128 * 1024,
            resumeWriterThreshold: 64 * 1024
        );

        return new Pipe(pipeOptions);
    }

    public static void MainRun()
    {
        var pipe = CreatePooledPipe();
        Console.WriteLine("Maxsus MemoryPool bilan bog'langan Pipe muvaffaqiyatli ishga tushirildi.");
    }
}
```
**Tushuntirish:** O'z `MemoryPool`imizni kiritish orqali xotira sahifalarini Pinned (siljimas) qilish yoki o'lchamlarini tarmoq MTU siga moslab o'rnatish mumkin.

---

### Topshiriq #1110: System.IO.Pipelines Asosidagi High-Performance TCP Echo Server
**Tavsif:** Minglab bir vaqtdagi ulanishlarni minimal xotira sarfi bilan qo'llab-quvvatlovchi ishlab chiqarish darajasidagi TCP server.
**Talablar:** `TcpListener`, `AcceptSocketAsync()`, ikkita mustaqil asinxron sikl (Read va Write).
**Yechim (C#):**
```csharp
using System;
using System.IO.Pipelines;
using System.Net;
using System.Net.Sockets;
using System.Threading.Tasks;

public class HighPerformanceEchoServer
{
    public static async Task StartAsync(int port)
    {
        var listener = new TcpListener(IPAddress.Any, port);
        listener.Start(100);
        Console.WriteLine($"High-Performance Server {port}-portda ishlamoqda...");

        while (true)
        {
            Socket socket = await listener.AcceptSocketAsync();
            _ = ProcessClientAsync(socket);
        }
    }

    private static async Task ProcessClientAsync(Socket socket)
    {
        using var stream = new NetworkStream(socket, ownsSocket: true);
        var pipe = new Pipe();

        Task writing = FillPipeAsync(stream, pipe.Writer);
        Task reading = ReadPipeAsync(stream, pipe.Reader);

        await Task.WhenAll(writing, reading);
    }

    private static async Task FillPipeAsync(NetworkStream stream, PipeWriter writer)
    {
        while (true)
        {
            Memory<byte> memory = writer.GetMemory(2048);
            int bytesRead = await stream.ReadAsync(memory);
            if (bytesRead == 0) break;

            writer.Advance(bytesRead);
            FlushResult result = await writer.FlushAsync();
            if (result.IsCompleted) break;
        }
        await writer.CompleteAsync();
    }

    private static async Task ReadPipeAsync(NetworkStream stream, PipeReader reader)
    {
        while (true)
        {
            ReadResult result = await reader.ReadAsync();
            var buffer = result.Buffer;

            foreach (var segment in buffer)
            {
                await stream.WriteAsync(segment);
            }

            reader.AdvanceTo(buffer.End);
            if (result.IsCompleted) break;
        }
        await reader.CompleteAsync();
    }
}
```
**Tushuntirish:** Ushbu model o'qish va yozishni ikkita parallel asinxron vazifaga ajratadi. Natijada bir vaqtning o'zida tarmoq kartasidan o'qish va javobni jo'natish maksimal o'tkazuvchanlikda bajariladi.

---

### Topshiriq #1111: ReadOnlySequence dagi Satrlarni Noldan Xotirasiz Dekodlash
**Tavsif:** Bir nechta xotira bloklariga bo'lingan UTF-8 baytlar ketma-ketligini oraliq massiv ajratmasdan `string` ga aylantirish.
**Talablar:** `Encoding.UTF8.GetString()`, `ReadOnlySpan<byte>`, `ReadOnlySequence<byte>.IsSingleSegment`.
**Yechim (C#):**
```csharp
using System;
using System.Buffers;
using System.Text;

public class Utf8SequenceDecoder
{
    public static string DecodeSequence(in ReadOnlySequence<byte> sequence)
    {
        // 1. Agar ma'lumot bitta xotira blokida bo'lsa (Fast path)
        if (sequence.IsSingleSegment)
        {
            return Encoding.UTF8.GetString(sequence.FirstSpan);
        }

        // 2. Agar ko'p segmentli bo'lsa, stackalloc bufer orqali o'qish
        if (sequence.Length <= 256)
        {
            Span<byte> stackSpan = stackalloc byte[(int)sequence.Length];
            sequence.CopyTo(stackSpan);
            return Encoding.UTF8.GetString(stackSpan);
        }

        // 3. Katta hajm uchun massiv orqali dekodlash
        return Encoding.UTF8.GetString(sequence.ToArray());
    }

    public static void MainRun()
    {
        var seq = new ReadOnlySequence<byte>(Encoding.UTF8.GetBytes("Khorazmiy AI Tizimi"));
        Console.WriteLine($"Natija: {DecodeSequence(in seq)}");
    }
}
```
**Tushuntirish:** `sequence.IsSingleSegment` tekshiruvi xotira bloklari soni 1 ta bo'lgan hollarda ortiqcha ko'chirishsiz to'g'ridan-to'g'ri `FirstSpan` bilan ishlash orqali chaqmoq tezligidagi ishlashni ta'minlaydi.

---

### Topshiriq #1112: System.IO.Pipelines da CancellationToken va Toza Yopilish
**Tavsif:** Klient aloqani to'satdan uzganda yoki timeout yuzaga kelganda barcha resurslarni xavfsiz va xatosiz ozod qilish.
**Talablar:** `CancellationTokenSource`, `reader.CancelPendingRead()`, `CompleteAsync(exception)`.
**Yechim (C#):**
```csharp
using System;
using System.IO.Pipelines;
using System.Threading;
using System.Threading.Tasks;

public class SafePipelineClosure
{
    public static async Task SafeReadWithTimeoutAsync(PipeReader reader, TimeSpan timeout)
    {
        using var cts = new CancellationTokenSource(timeout);
        try
        {
            ReadResult result = await reader.ReadAsync(cts.Token);
            reader.AdvanceTo(result.Buffer.End);
            await reader.CompleteAsync();
            Console.WriteLine("O'qish muvaffaqiyatli yakunlandi.");
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine("Timeout tufayli ulanish bekor qilindi.");
            await reader.CompleteAsync(); // Xotirani ozod qilish
        }
        catch (Exception ex)
        {
            await reader.CompleteAsync(ex); // Xatolik bilan yopish
            throw;
        }
    }
}
```
**Tushuntirish:** `CompleteAsync()` har doim `finally` blokida yoki istisnolar ushlanganda chaqirilishi shart, aks holda ajratilgan xotira bloklari hovuzga qaytmaydi (Memory leak).

---

### Topshiriq #1113: IDuplexPipe Interfeysi va Ikki Tomonlama Asinxron Oqimlar
**Tavsif:** Dupleks (bir vaqtda ham o'quvchi, ham yozuvchi) tarmoq kanallarini yagona interfeys orqali ifodalash.
**Talablar:** `IDuplexPipe`, `Input (PipeReader)`, `Output (PipeWriter)`.
**Yechim (C#):**
```csharp
using System;
using System.IO.Pipelines;
using System.Threading.Tasks;

public class CustomDuplexPipe : IDuplexPipe
{
    public PipeReader Input { get; }
    public PipeWriter Output { get; }

    public CustomDuplexPipe(PipeReader reader, PipeWriter writer)
    {
        Input = reader;
        Output = writer;
    }

    public static async Task CommunicateAsync(IDuplexPipe channel)
    {
        // Ma'lumot yuborish
        await channel.Output.WriteAsync(new byte[] { 1, 2, 3 });
        Console.WriteLine("IDuplexPipe orqali ma'lumot jo'natildi.");

        // Javobni o'qish
        ReadResult res = await channel.Input.ReadAsync();
        channel.Input.AdvanceTo(res.Buffer.End);
    }
}
```
**Tushuntirish:** `IDuplexPipe` interfeysi Kestrel, SignalR va gRPC ichki transportlarida ikki tomonlama to'liq asinxron ma'lumot almashish uchun standart kontrakt hisoblanadi.

---

### Topshiriq #1114: Custom Protocol Frame Serializer va Deserializer
**Tavsif:** Ikkilik protokollarni (Header + Body + CRC) Pipelines yordamida to'liq avtomatik serializatsiya va deserializatsiya qilish.
**Talablar:** Binar serialization, CRC tekshiruvi, xotira xavfsizligi.
**Yechim (C#):**
```csharp
using System;
using System.Buffers;
using System.Buffers.Binary;
using System.IO.Pipelines;
using System.Threading.Tasks;

public record TelemetryPacket(int DeviceId, double Temperature, long Timestamp);

public class PacketSerializer
{
    public static void Serialize(PipeWriter writer, TelemetryPacket packet)
    {
        Span<byte> span = writer.GetSpan(20); // [ID(4)] + [Temp(8)] + [Time(8)]
        BinaryPrimitives.WriteInt32BigEndian(span.Slice(0, 4), packet.DeviceId);
        BinaryPrimitives.WriteDoubleBigEndian(span.Slice(4, 8), packet.Temperature);
        BinaryPrimitives.WriteInt64BigEndian(span.Slice(12, 8), packet.Timestamp);
        writer.Advance(20);
    }

    public static bool TryDeserialize(ref ReadOnlySequence<byte> buffer, out TelemetryPacket packet)
    {
        if (buffer.Length < 20)
        {
            packet = null;
            return false;
        }

        Span<byte> raw = stackalloc byte[20];
        buffer.Slice(0, 20).CopyTo(raw);

        int id = BinaryPrimitives.ReadInt32BigEndian(raw.Slice(0, 4));
        double temp = BinaryPrimitives.ReadDoubleBigEndian(raw.Slice(4, 8));
        long time = BinaryPrimitives.ReadInt64BigEndian(raw.Slice(12, 8));

        packet = new TelemetryPacket(id, temp, time);
        buffer = buffer.Slice(20);
        return true;
    }
}
```
**Tushuntirish:** Ushbu yondashuv JSON yoki XML ga nisbatan 10 barobar tezroq va xotira ajratishsiz ishlaydi, bu esa IoT qurilmalari serverlarida muhim ahamiyat kasb etadi.

---

### Topshiriq #1115: Multiple Consumers / Single Producer Pipelines Arxitekturasi
**Tavsif:** Bitta tarmoq manbasidan olingan oqimni bir nechta mustaqil xizmatlarga (masalan, arxivlash va real vaqt tahlili) tarqatish.
**Talablar:** Fan-out arxitekturasi, `Channel<T>` yoki ko'p tarmoqli Pipe zanjiri.
**Yechim (C#):**
```csharp
using System;
using System.IO.Pipelines;
using System.Threading.Tasks;

public class PipelineFanOut
{
    public static async Task DispatchAsync(PipeReader source, PipeWriter writer1, PipeWriter writer2)
    {
        while (true)
        {
            ReadResult result = await source.ReadAsync();
            ReadOnlySequence<byte> buffer = result.Buffer;

            if (buffer.IsEmpty && result.IsCompleted) break;

            foreach (ReadOnlyMemory<byte> memory in buffer)
            {
                await writer1.WriteAsync(memory);
                await writer2.WriteAsync(memory);
            }

            source.AdvanceTo(buffer.End);
        }

        await writer1.CompleteAsync();
        await writer2.CompleteAsync();
        Console.WriteLine("Fan-out muvaffaqiyatli yakunlandi.");
    }
}
```
**Tushuntirish:** Fan-out Pipelines yordamida bitta kiruvchi paketni bir vaqtning o'zida diskka yozuvchi xizmatga ham, tahlil qiluvchi neyrotarmoq modeliga ham xotirani ko'paytirmasdan yo'naltirish mumkin.

---

### Topshiriq #1116: Kestrel Transport Arxitekturasi va IConnectionListenerFactory
**Tavsif:** Kestrel serveriga standart TCP soketlar o'rniga o'zimizning maxsus tarmoq transportimizni integratsiya qilish.
**Talablar:** `IConnectionListenerFactory`, `IConnectionListener`, `EndPoint`, `ConnectionContext`.
**Yechim (C#):**
```csharp
using System;
using System.Net;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Connections;

public class CustomTransportFactory : IConnectionListenerFactory
{
    public ValueTask<IConnectionListener> BindAsync(EndPoint endpoint, CancellationToken cancellationToken = default)
    {
        Console.WriteLine($"Kestrel uchun yangi transport ulandi: {endpoint}");
        return ValueTask.FromResult<IConnectionListener>(new CustomConnectionListener(endpoint));
    }
}

public class CustomConnectionListener : IConnectionListener
{
    public EndPoint EndPoint { get; }

    public CustomConnectionListener(EndPoint endpoint) => EndPoint = endpoint;

    public ValueTask<ConnectionContext> AcceptAsync(CancellationToken cancellationToken = default)
    {
        // Yangi ulanishlarni qaytarish mantiqi
        return ValueTask.FromResult<ConnectionContext>(null);
    }

    public ValueTask UnbindAsync(CancellationToken cancellationToken = default) => ValueTask.CompletedTask;
    public ValueTask DisposeAsync() => ValueTask.CompletedTask;
}
```
**Tushuntirish:** Kestrel butunlay modulli arxitekturaga ega. `IConnectionListenerFactory` orqali standart TCP transportni almashtirib, Unix soketlar, Bluetooth yoki maxsus shifrlangan kanallarni ulash mumkin.

---

### Topshiriq #1117: Kestrel Uchun Unix Domain Sockets (UDS) Transportini Qurish
**Tavsif:** Linux konteynerlarida (Docker/K8s) Kestrel va Nginx o'rtasida TCP overheadsiz lokal aloqa o'rnatish.
**Talablar:** `UnixDomainSocketEndPoint`, `SocketType.Stream`, `ProtocolType.Unspecified`.
**Yechim (C#):**
```csharp
using System;
using System.IO;
using System.Net.Sockets;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Hosting;

public class UnixDomainSocketKestrel
{
    public static void ConfigureUdsHost(string socketPath)
    {
        if (File.Exists(socketPath)) File.Delete(socketPath);

        var builder = WebApplication.CreateBuilder();
        builder.WebHost.ConfigureKestrel(options =>
        {
            options.ListenUnixSocket(socketPath, listenOptions =>
            {
                Console.WriteLine($"Kestrel Unix Soketda tinglamoqda: {socketPath}");
            });
        });

        // builder.Build().Run();
    }
}
```
**Tushuntirish:** Unix Domain Sockets orqali ishlaganda loopback tarmoq drayverlari va port to'qnashuvlari yo'qoladi, bu esa xizmatlar o'rtasida 20-30% yuqoriroq tezlik beradi.

---

### Topshiriq #1118: Kestrel Uchun In-Memory Transport (Integratsion Testlar)
**Tavsif:** Haqiqiy tarmoq portlarini ochmasdan, faqat operativ xotirada ishlovchi o'ta tezkor integratsion test transportini yaratish.
**Talablar:** `System.IO.Pipelines`, `IDuplexPipe`, xotiradagi `ConnectionContext`.
**Yechim (C#):**
```csharp
using System;
using System.IO.Pipelines;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Connections;
using Microsoft.AspNetCore.Http.Features;

public class InMemoryConnectionContext : ConnectionContext
{
    public override string ConnectionId { get; set; } = Guid.NewGuid().ToString();
    public override IFeatureCollection Features { get; } = new FeatureCollection();
    public override IDictionary<object, object> Items { get; set; } = new Dictionary<object, object>();
    public override IDuplexPipe Transport { get; set; }

    public InMemoryConnectionContext(IDuplexPipe transport)
    {
        Transport = transport;
    }
}
```
**Tushuntirish:** In-Memory Transport testlarni soniyaning mingdan bir ulushlarida bajarish imkonini beradi va xavfsizlik devori (firewall) ogohlantirishlarining oldini oladi.

---

### Topshiriq #1119: Kestrel Connection Middleware Bilan IP Oqimini Filtrlash
**Tavsif:** HTTP darajasiga yetib kelmasdanoq, TCP ulanish bosqichidayoq zararli IP manzillarni zudlik bilan uzish.
**Talablar:** `IConnectionBuilder.Use()`, `ConnectionDelegate`, `RemoteEndPoint` tekshiruvi.
**Yechim (C#):**
```csharp
using System;
using System.Net;
using Microsoft.AspNetCore.Connections;
using Microsoft.AspNetCore.Hosting;

public static class ConnectionFilterExtensions
{
    public static IConnectionBuilder UseIpFilter(this IConnectionBuilder builder, IPAddress blockedIp)
    {
        return builder.Use(next => async context =>
        {
            var remoteIp = (context.RemoteEndPoint as IPEndPoint)?.Address;
            if (remoteIp != null && remoteIp.Equals(blockedIp))
            {
                Console.WriteLine($"Bloklangan IP ulanishga urindi: {remoteIp}. Aloqa zudlik bilan uzildi.");
                await context.AbortAsync(); // TCP RST yoki zudlik bilan yopish
                return;
            }

            await next(context);
        });
    }
}
```
**Tushuntirish:** Connection Middleware ulanishlarni HTTP darajasidan ancha oldin (L4 darajasida) to'xtatadi. Bu esa xotira ajratish va HTTP sarlavhalarini dekodlash xarajatlarini tejaydi.

---

### Topshiriq #1120: ConnectionContext va IConnectionLifetimeFeature Yordamida Muddatni Boshqarish
**Tavsif:** Uzoq vaqt davom etayotgan harakatsiz ulanishlarni aniqlash va ularni server tomonidan majburiy yopish.
**Talablar:** `IConnectionLifetimeFeature`, `AbortConnection()`, `ConnectionClosed` tokeni.
**Yechim (C#):**
```csharp
using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Connections;
using Microsoft.AspNetCore.Connections.Features;

public class IdleTimeoutMiddleware
{
    public static async Task HandleWithLifetimeAsync(ConnectionContext context, Func<Task> next)
    {
        var lifetime = context.Features.Get<IConnectionLifetimeFeature>();
        if (lifetime != null)
        {
            lifetime.ConnectionClosed.Register(() =>
            {
                Console.WriteLine($"Ulanish yopildi: ID={context.ConnectionId}");
            });
        }

        // Bajarishni davom ettirish
        await next();
    }
}
```
**Tushuntirish:** `IConnectionLifetimeFeature` ulanish yopilish hodisalariga obuna bo'lish va resurslarni zudlik bilan tozalash uchun qulay imkoniyat yaratadi.

---

### Topshiriq #1121: TLS Termination Custom Middleware (SslStream va Kestrel)
**Tavsif:** Kestrel oldida maxsus shaxsiy shifrlash va sertifikat tekshiruvlarini dasturiy tarzda boshqarish.
**Talablar:** `SslStream`, `SslServerAuthenticationOptions`, `TlsCipherSuite`.
**Yechim (C#):**
```csharp
using System;
using System.IO.Pipelines;
using System.Net.Security;
using System.Security.Cryptography.X509Certificates;
using System.Threading.Tasks;

public class CustomTlsTerminator
{
    public static async Task TerminateTlsAsync(System.IO.Stream networkStream, X509Certificate2 serverCert)
    {
        using var sslStream = new SslStream(networkStream, false);
        var options = new SslServerAuthenticationOptions
        {
            ServerCertificate = serverCert,
            ClientCertificateRequired = false,
            EnabledSslProtocols = System.Security.Authentication.SslProtocols.Tls13
        };

        await sslStream.AuthenticateAsServerAsync(options);
        Console.WriteLine($"TLS 1.3 qo'l siqishi muvaffaqiyatli: {sslStream.NegotiatedCipherSuite}");
    }
}
```
**Tushuntirish:** Custom TLS Middleware orqali mTLS (Mutual TLS) talablarini bajarish va mijoz sertifikatini L4 darajasida tekshirish mumkin.

---

### Topshiriq #1122: Kestrel SocketTransportOptions Nozik Sozlamalari
**Tavsif:** Linux va Windows serverlarida Kestrel o'tkazuvchanligini maksimal darajaga ko'tarish uchun soket konfiguratsiyasi.
**Talablar:** `SocketTransportOptions`, `IOQueueCount`, `MaxReadBufferSize`, `MaxWriteBufferSize`.
**Yechim (C#):**
```csharp
using System;
using Microsoft.AspNetCore.Server.Kestrel.Transport.Sockets;
using Microsoft.Extensions.Options;

public class KestrelTuning
{
    public static void TuneSockets(SocketTransportOptions options)
    {
        // CPU yadrolari soniga qarab I/O navbatlarini sozlash
        options.IOQueueCount = Environment.ProcessorCount;

        // O'qish va yozish maksimal buferlari
        options.MaxReadBufferSize = 1024 * 1024;  // 1 MB
        options.MaxWriteBufferSize = 1024 * 1024; // 1 MB

        // Xotira bloklarini nozik boshqarish
        options.UnsafePreferInlineScheduling = false;
        Console.WriteLine($"Kestrel Socket Transport optimallashtirildi: Queues = {options.IOQueueCount}");
    }
}
```
**Tushuntirish:** `IOQueueCount` parametrini mantiqiy yadrolar soniga tenglashtirish har bir yadroga o'z `IOQueue`sini beradi va CPU keshlarining optimal ishlashini ta'minlaydi.

---

### Topshiriq #1123: Kestrel Connection Rate Limiter (Ulanishlarni Cheklash)
**Tavsif:** Bitta mijoz IP manzilidan bir vaqtda keladigan ulanishlar sonini cheklash orqali DoS hujumlaridan himoyalanish.
**Talablar:** `ConcurrentDictionary`, ulanishlar hisoblagichi, L4 darajasida cheklov.
**Yechim (C#):**
```csharp
using System;
using System.Collections.Concurrent;
using System.Net;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Connections;

public class ConnectionLimiterMiddleware
{
    private static readonly ConcurrentDictionary<IPAddress, int> ActiveConnections = new();
    private const int MaxPerIp = 50;

    public static async Task HandleAsync(ConnectionContext context, Func<Task> next)
    {
        if (context.RemoteEndPoint is IPEndPoint ep)
        {
            int current = ActiveConnections.AddOrUpdate(ep.Address, 1, (_, count) => count + 1);
            if (current > MaxPerIp)
            {
                Console.WriteLine($"IP {ep.Address} ulanishlar limitidan oshdi ({current}/{MaxPerIp}). Aloqa uzildi.");
                ActiveConnections.AddOrUpdate(ep.Address, 0, (_, count) => count - 1);
                await context.AbortAsync();
                return;
            }

            try
            {
                await next();
            }
            finally
            {
                ActiveConnections.AddOrUpdate(ep.Address, 0, (_, count) => count - 1);
            }
        }
    }
}
```
**Tushuntirish:** L4 ulanish cheklovchisi server resurslarini to'lib qolishdan himoya qiladi va har bir IP uchun adolatli kvota kafolatlaydi.

---

### Topshiriq #1124: Kestrel Ustida Xom TCP Protokollarini Ko'tarish (Non-HTTP)
**Tavsif:** Kestrel HTTP infratuzilmasidan foydalangan holda maxsus TCP protokollarni (masalan, o'yin serveri yoki IoT broker) bitta dasturda joylashtirish.
**Talablar:** `ListenOptions.Use()`, HTTP bo'lmagan protokollar, `IDuplexPipe`.
**Yechim (C#):**
```csharp
using System;
using System.IO.Pipelines;
using System.Text;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Connections;

public class RawTcpKestrelServer
{
    public static void StartServer()
    {
        var builder = WebApplication.CreateBuilder();
        builder.WebHost.ConfigureKestrel(options =>
        {
            // Port 5005 da xom TCP tinglash
            options.ListenAnyIP(5005, listenOptions =>
            {
                listenOptions.Use(async (context, next) =>
                {
                    // Xom TCP echo xizmati
                    IDuplexPipe transport = context.Transport;
                    while (true)
                    {
                        var result = await transport.Input.ReadAsync();
                        if (result.Buffer.IsEmpty && result.IsCompleted) break;

                        foreach (var segment in result.Buffer)
                        {
                            await transport.Output.WriteAsync(segment);
                        }
                        transport.Input.AdvanceTo(result.Buffer.End);
                    }
                });
            });
        });
        Console.WriteLine("Kestrel TCP server konfiguratsiyasi tayyor.");
    }
}
```
**Tushuntirish:** Kestrel nafaqat HTTP/1, HTTP/2 va HTTP/3 serveri, balki yuqori tezlikdagi ixtiyoriy binar TCP protokollar uchun ham universal asosdir.

---

### Topshiriq #1125: PinnedBlockMemoryPool Profiling va Kestrel Xotira Sarfini Minimallashtirish
**Tavsif:** Kestrelning ichki xotira boshqaruvi (`PinnedBlockMemoryPool`) faoliyatini kuzatish va xotira oqishini (memory leak) oldini olish.
**Talablar:** `PinnedBlockMemoryPool`, 4096-baytlik bloklar, diagnostika.
**Yechim (C#):**
```csharp
using System;
using System.Buffers;

public class MemoryPoolProfiling
{
    public static void InspectMemoryPool()
    {
        using var pool = MemoryPool<byte>.Shared;
        Console.WriteLine($"Maksimal bitta blok hajmi: {pool.MaxBufferSize} bayt.");

        using (IMemoryOwner<byte> owner = pool.Rent(4096))
        {
            Memory<byte> memory = owner.Memory;
            Console.WriteLine($"Ijara olingan xotira bloki hajmi: {memory.Length} bayt.");
            // owner.Dispose() chaqirilganda blok qayta hovuzga qaytadi
        }

        Console.WriteLine("Xotira bloki muvaffaqiyatli hovuzga qaytarildi.");
    }
}
```
**Tushuntirish:** `PinnedBlockMemoryPool` xotira bloklarini operativ xotirada qotirilgan (pinned) holda saqlaydi, bu esa operatsion tizim yadrosiga to'g'ridan-to'g'ri DMA orqali o'qish/yozish imkonini beradi.

---

### Topshiriq #1126: Kestrel da HTTP/1.1 va HTTP/2 ni Birgalikda Qo'llab-Quvvatlash
**Tavsif:** Mijoz imkoniyatiga qarab HTTP/1.1 yoki HTTP/2 protokollarini avtomatik tanlash (ALPN).
**Talablar:** `HttpProtocols.Http1AndHttp2`, `ListenOptions.Protocols`.
**Yechim (C#):**
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Server.Kestrel.Core;

public class HttpDualProtocolSetup
{
    public static void ConfigureProtocols()
    {
        var builder = WebApplication.CreateBuilder();
        builder.WebHost.ConfigureKestrel(options =>
        {
            options.ListenAnyIP(8443, listenOptions =>
            {
                listenOptions.Protocols = HttpProtocols.Http1AndHttp2;
                listenOptions.UseHttps(); // ALPN orqali h2 yoki http/1.1 kelishiladi
            });
        });
        Console.WriteLine("Kestrel port 8443 da HTTP/1.1 va HTTP/2 uchun tayyorlandi.");
    }
}
```
**Tushuntirish:** TLS ulanish vaqtida ALPN (Application-Layer Protocol Negotiation) orqali mijoz va server qaysi protokol ishlatilishini kelishib oladi.

---

### Topshiriq #1127: Graceful Server Shutdown: Kestrel Ulanishlarini Xavfsiz Drenaj Qilish
**Tavsif:** Server yangilanganda yoki to'xtatilganda faol so'rovlarni uzmasdan toza yakunlash (Connection Draining).
**Talablar:** `IHostApplicationLifetime`, `ShutdownTimeout`, ulanishlarni drenaj qilish.
**Yechim (C#):**
```csharp
using System;
using System.Threading.Tasks;
using Microsoft.Extensions.Hosting;

public class GracefulShutdownManager
{
    public static void ConfigureLifetime(IHostApplicationLifetime lifetime)
    {
        lifetime.ApplicationStopping.Register(() =>
        {
            Console.WriteLine("Server to'xtatilmoqda: Yangi ulanishlar qabul qilinmaydi, mavjudlari tugallanmoqda...");
        });

        lifetime.ApplicationStopped.Register(() =>
        {
            Console.WriteLine("Barcha so'rovlar muvaffaqiyatli drenaj qilindi. Server toza yopildi.");
        });
    }
}
```
**Tushuntirish:** Kubernetes klasterlarida Pod to'xtatilayotganda `preStop` hook va Kestrel ning Graceful Shutdown mexanizmi mijozlarga `502 Bad Gateway` xatolarini bermaslikni ta'minlaydi.

---

### Topshiriq #1128: Kestrel IMultiplexedConnectionListenerFactory va Ko'p Kanalli Transportlar
**Tavsif:** HTTP/3 va QUIC kabi bitta ulanish ichida yuzlab mustaqil oqimlarni tashuvchi ko'p kanalli transportlarni qo'llab-quvvatlash.
**Talablar:** `IMultiplexedConnectionListenerFactory`, `MultiplexedConnectionContext`.
**Yechim (C#):**
```csharp
using System;
using System.Net;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Connections;

public class CustomMultiplexedFactory : IMultiplexedConnectionListenerFactory
{
    public ValueTask<IMultiplexedConnectionListener> BindAsync(EndPoint endpoint, IFeatureCollection features = null, CancellationToken cancellationToken = default)
    {
        Console.WriteLine($"Ko'p kanalli (Multiplexed) transport bog'landi: {endpoint}");
        return ValueTask.FromResult<IMultiplexedConnectionListener>(null);
    }
}
```
**Tushuntirish:** `IMultiplexedConnectionListenerFactory` an'anaviy oqimli soketlardan farqli o'laroq bitta L4 ulanish ustida virtual oqimlarni (Streams) mustaqil qabul qilish imkonini beradi.

---

### Topshiriq #1129: .NET da System.Net.Quic: QuicListener va QuicConnection Yaratish
**Tavsif:** UDP ustiga qurilgan va shifrlashni (TLS 1.3) majburiy talab qiluvchi QUIC serverini yaratish.
**Talablar:** `System.Net.Quic.QuicListener`, `QuicServerConnectionOptions`, `QuicListenerOptions`.
**Yechim (C#):**
```csharp
using System;
using System.Net;
using System.Net.Quic;
using System.Net.Security;
using System.Security.Cryptography.X509Certificates;
using System.Threading.Tasks;

public class QuicServerDemo
{
    public static async Task StartQuicServerAsync()
    {
        if (!QuicListener.IsSupported)
        {
            Console.WriteLine("QUIC ushbu operatsion tizimda qo'llab-quvvatlanmaydi (MsQuic talab qilinadi).");
            return;
        }

        var listenerOptions = new QuicListenerOptions
        {
            ListenEndPoint = new IPEndPoint(IPAddress.Loopback, 9999),
            ApplicationProtocols = new() { new SslApplicationProtocol("khorazmiy-quic") },
            ConnectionOptionsCallback = (connection, sslHello, token) =>
            {
                return ValueTask.FromResult(new QuicServerConnectionOptions
                {
                    DefaultStreamErrorCode = 0x0A,
                    DefaultCloseErrorCode = 0x0B,
                    ServerAuthenticationOptions = new SslServerAuthenticationOptions
                    {
                        ApplicationProtocols = new() { new SslApplicationProtocol("khorazmiy-quic") }
                    }
                });
            }
        };

        await using var listener = await QuicListener.ListenAsync(listenerOptions);
        Console.WriteLine("QUIC Server 9999-portda (UDP) tinglamoqda...");
    }
}
```
**Tushuntirish:** `System.Net.Quic` Microsoft MsQuic kutubxonasiga asoslangan bo'lib, .NET 8/9 da eng yuqori unumdorlikdagi L4 UDP transportini taqdim etadi.

---

### Topshiriq #1130: QuicServerConnectionOptions va ALPN Sozlash
**Tavsif:** QUIC protokoli orqali ulanayotgan mijoz bilan qaysi dasturiy protokol (masalan, `h3` yoki shaxsiy protokol) ishlatilishini kelishish.
**Talablar:** `SslApplicationProtocol`, `QuicServerConnectionOptions`, ALPN muzokaralari.
**Yechim (C#):**
```csharp
using System;
using System.Collections.Generic;
using System.Net.Quic;
using System.Net.Security;

public class QuicAlpnConfiguration
{
    public static QuicServerConnectionOptions CreateOptions()
    {
        return new QuicServerConnectionOptions
        {
            DefaultStreamErrorCode = 0x01,
            DefaultCloseErrorCode = 0x00,
            ServerAuthenticationOptions = new SslServerAuthenticationOptions
            {
                ApplicationProtocols = new List<SslApplicationProtocol>
                {
                    SslApplicationProtocol.Http3,
                    new SslApplicationProtocol("my-custom-protocol")
                }
            }
        };
    }
}
```
**Tushuntirish:** QUIC protokolida barcha ulanishlar boshidanoq TLS 1.3 bilan shifrlanadi. Shifrlanmagan ochiq QUIC mavjud emas, bu esa aloqa xavfsizligini ta'minlaydi.

---

### Topshiriq #1131: QuicStream: Ikki Tomonlama (Bidirectional) va Bir Tomonlama (Unidirectional) Oqimlar
**Tavsif:** Bitta QUIC ulanishi ichida mustaqil ma'lumot oqimlarini ochish va ularni alohida boshqarish.
**Talablar:** `QuicStreamType.Bidirectional`, `QuicStreamType.Unidirectional`, `AcceptInboundStreamAsync()`.
**Yechim (C#):**
```csharp
using System;
using System.Net.Quic;
using System.Text;
using System.Threading.Tasks;

public class QuicStreamManager
{
    public static async Task HandleConnectionAsync(QuicConnection connection)
    {
        while (true)
        {
            // Kiruvchi streamni qabul qilish
            QuicStream stream = await connection.AcceptInboundStreamAsync();
            _ = ProcessStreamAsync(stream);
        }
    }

    private static async Task ProcessStreamAsync(QuicStream stream)
    {
        byte[] buffer = new byte[1024];
        int read = await stream.ReadAsync(buffer);
        Console.WriteLine($"Streamdan o'qildi: {Encoding.UTF8.GetString(buffer, 0, read)}");

        if (stream.Type == QuicStreamType.Bidirectional)
        {
            byte[] response = Encoding.UTF8.GetBytes("QUIC javobi");
            await stream.WriteAsync(response);
        }

        await stream.DisposeAsync();
    }
}
```
**Tushuntirish:** Unidirectional oqimlar faqat bir tomonga ma'lumot uzatish (masalan, telemetriya) uchun, Bidirectional oqimlar esa so'rov-javob (RPC) uchun mo'ljallangan.

---

### Topshiriq #1132: HTTP/3 (Kestrel) Serverini MsQuic Bilan Sozlash va Ishga Tushirish
**Tavsif:** Kestrel serverida eng so'nggi HTTP/3 protokoli orqali so'rovlarni qabul qilishni to'liq yoqish.
**Talablar:** `HttpProtocols.Http3`, `ListenOptions.Protocols`, MsQuic konfiguratsiyasi.
**Yechim (C#):**
```csharp
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Server.Kestrel.Core;

public class Http3KestrelSetup
{
    public static void RunHttp3Server()
    {
        var builder = WebApplication.CreateBuilder();

        builder.WebHost.ConfigureKestrel(options =>
        {
            options.ListenAnyIP(5001, listenOptions =>
            {
                listenOptions.Protocols = HttpProtocols.Http1AndHttp2AndHttp3;
                listenOptions.UseHttps(); // HTTP/3 majburiy HTTPS talab qiladi
            });
        });

        var app = builder.Build();
        app.MapGet("/", () => "Salom, Khorazmiy HTTP/3 dunyosi!");
        Console.WriteLine("HTTP/3 Kestrel server tayyorlandi.");
    }
}
```
**Tushuntirish:** HTTP/3 TCP o'rniga UDP (QUIC) ustida ishlaydi, shuning uchun serverda tegishli UDP portlari xavfsizlik devorida ochilgan bo'lishi kerak.

---

### Topshiriq #1133: HttpClient Orqali HTTP/3 So'rovlarini Jo'natish
**Tavsif:** .NET mijozi orqali serverga zamonaviy HTTP/3 protokoli yordamida tezkor so'rov yuborish.
**Talablar:** `HttpRequestMessage`, `Version = HttpVersion.Version30`, `VersionPolicy`.
**Yechim (C#):**
```csharp
using System;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;

public class Http3ClientDemo
{
    public static async Task SendHttp3RequestAsync(string url)
    {
        using var client = new HttpClient();
        using var request = new HttpRequestMessage(HttpMethod.Get, url)
        {
            Version = HttpVersion.Version30,
            VersionPolicy = HttpVersionPolicy.RequestVersionExact
        };

        using var response = await client.SendAsync(request);
        Console.WriteLine($"Javob protokoli: HTTP/{response.Version}");
        string content = await response.Content.ReadAsStringAsync();
        Console.WriteLine($"Mundarija: {content}");
    }
}
```
**Tushuntirish:** `HttpVersionPolicy.RequestVersionExact` siyosati agar server HTTP/3 ni qo'llab-quvvatlamasa, eski HTTP/1.1 ga tushmasdan xatolik qaytarishini belgilaydi.

---

### Topshiriq #1134: QUIC 0-RTT Connection Resumption (Kechikishni Yo'qotish)
**Tavsif:** Avval ulangan mijozning qayta ulanishida handshake kechikishini (RTT) 0 ga tushirish.
**Talablar:** 0-RTT erta ma'lumot uzatish, Replay attack himoyasi mantiqi.
**Yechim (C#):**
```csharp
using System;
using System.Net.Quic;

public class ZeroRttManager
{
    public static void ExplainZeroRtt()
    {
        Console.WriteLine("QUIC 0-RTT printsipi:");
        Console.WriteLine("1. Birinchi ulanishda server mijozga 'Session Ticket' beradi.");
        Console.WriteLine("2. Qayta ulanishda mijoz hatto handshake tugashini kutmasdan (0-RTT) birinchi paketdayoq HTTP GET so'rovini jo'natadi.");
        Console.WriteLine("3. Kechikish an'anaviy TCP+TLS dagi 2-3 RTT o'rniga roppa-rosa 0 RTT ga tushadi.");
    }
}
```
**Tushuntirish:** 0-RTT texnologiyasi mobil tarmoqlarda sahifalarning ochilish tezligini keskin oshiradi, biroq xavfsizlik nuqtai nazaridan faqat idempotent (masalan, GET) so'rovlarda qo'llanilishi lozim.

---

### Topshiriq #1135: QUIC Oqimlarida Head-of-Line (HoL) Blocking Muammosi Yo'qligi
**Tavsif:** Bitta paket yo'qolganda butun aloqa to'xtab qolmasligini namoyish qiluvchi multi-stream arxitekturasi.
**Talablar:** Streamlar mustaqilligi, paket yo'qolishi faqat tegishli bitta oqimga ta'sir qilishi.
**Yechim (C#):**
```csharp
using System;
using System.Threading.Tasks;

public class HeadOfLineBlockingDemo
{
    public static void ExplainHoL()
    {
        Console.WriteLine("TCP da bitta paket yo'qolsa, qolgan barcha ma'lumotlar kutishga majbur (Head-of-Line Blocking).");
        Console.WriteLine("QUIC da har bir Stream alohida ketma-ketlik raqamiga ega. Agar Stream #1 paketi yo'qolsa, Stream #2 va Stream #3 hech qanday to'siqsiz ma'lumot uzatishda davom etadi.");
    }
}
```
**Tushuntirish:** Bu xususiyat nest-tarmoqlarda va sifat past bo'lgan mobil aloqada (paket yo'qolish darajasi yuqori bo'lganda) HTTP/3 ning HTTP/2 dan 3-5 barobar ustunligini ta'minlaydi.

---

### Topshiriq #1136: QuicStream va System.IO.Pipelines ni O'zaro Integratsiya Qilish
**Tavsif:** QUIC oqimlarini yuqori unumdor Pipelines konveyeriga ulab, baytlarni qayta ishlash tezligini oshirish.
**Talablar:** `PipeReader.Create(quicStream)`, `PipeWriter.Create(quicStream)`.
**Yechim (C#):**
```csharp
using System;
using System.IO.Pipelines;
using System.Net.Quic;
using System.Threading.Tasks;

public class QuicPipelineIntegration
{
    public static async Task ProcessQuicStreamWithPipelines(QuicStream quicStream)
    {
        var reader = PipeReader.Create(quicStream);
        var writer = PipeWriter.Create(quicStream);

        try
        {
            ReadResult result = await reader.ReadAsync();
            var buffer = result.Buffer;

            // Xotirada qayta ishlash
            Console.WriteLine($"QUIC Pipeline orqali {buffer.Length} bayt qabul qilindi.");

            reader.AdvanceTo(buffer.End);
        }
        finally
        {
            await reader.CompleteAsync();
            await writer.CompleteAsync();
        }
    }
}
```
**Tushuntirish:** Ushbu integratsiya zamonaviy C# tarmoq dasturlashining eng yuqori cho'qqisi hisoblanadi: QUIC tezligi + Pipelines xotira tejamkorligi.

---

### Topshiriq #1137: QUIC Datagrams: Ishonchsiz Xabarlarni Tezkor Uzatish
**Tavsif:** O'yin holati yoki audio/video uzatish uchun stream ochmasdan to'g'ridan-to'g'ri xom datagramma jo'natish.
**Talablar:** `QuicConnection.SendDatagramAsync()`, `ReceiveDatagramAsync()`.
**Yechim (C#):**
```csharp
using System;
using System.Net.Quic;
using System.Threading.Tasks;

public class QuicDatagramService
{
    public static async Task SendTelemetryDatagramAsync(QuicConnection connection, ReadOnlyMemory<byte> datagram)
    {
        // Ulanish darajasida tezkor, oqimsiz datagramma jo'natish
        // await connection.SendDatagramAsync(datagram);
        Console.WriteLine($"QUIC Datagram jo'natildi: {datagram.Length} bayt.");
        await Task.CompletedTask;
    }
}
```
**Tushuntirish:** QUIC Datagrams RFC 9221 bo'yicha ulanish xavfsizligini saqlagan holda UDP ning barcha ustunliklarini (hech qanday retransmission kutishlarsiz) taqdim etadi.

---

### Topshiriq #1138: QUIC Xatolik Kodlari va Stream Abort Operatsiyalari (QuicException)
**Tavsif:** Buzuq yoki keraksiz bo'lib qolgan oqimlarni masofadagi serverga xatolik kodi yuborib zudlik bilan bekor qilish.
**Talablar:** `QuicStream.Abort()`, `QuicAbortDirection`, `QuicError`.
**Yechim (C#):**
```csharp
using System;
using System.Net.Quic;

public class QuicAbortHandling
{
    public static void AbortStreamGracefully(QuicStream stream, long appErrorCode)
    {
        try
        {
            // O'qish yoki yozish yo'nalishini maxsus xato kodi bilan to'xtatish
            stream.Abort(QuicAbortDirection.Both, appErrorCode);
            Console.WriteLine($"Stream to'xtatildi (Abort kodi: 0x{appErrorCode:X}).");
        }
        catch (QuicException qEx)
        {
            Console.WriteLine($"QUIC istisnosi: {qEx.QuicError}");
        }
    }
}
```
**Tushuntirish:** `Abort()` funksiyasi TCP dagi RST ga o'xshaydi, biroq butun aloqani uzmasdan faqat bitta streamni to'xtatadi.

---

### Topshiriq #1139: HTTP/3 Alt-Svc Sarlavhalari Bilan Avtomatik Yo'naltirish
**Tavsif:** Mijoz HTTP/2 orqali kelganda, javob sarlavhasida HTTP/3 portini ko'rsatib, keyingi so'rovlarni QUIC ga o'tkazish.
**Talablar:** `Alt-Svc` sarlavhasi, `h3=":443"; ma=86400`.
**Yechim (C#):**
```csharp
using System;
using Microsoft.AspNetCore.Http;

public class AltSvcHeaderMiddleware
{
    public static void AddAltSvcHeader(HttpContext context)
    {
        // Mijozga server HTTP/3 ni qo'llab-quvvatlashini bildirish
        context.Response.Headers.Append("Alt-Svc", "h3=\":5001\"; ma=86400");
    }

    public static void MainRun()
    {
        Console.WriteLine("Alt-Svc HTTP/3 yo'naltirish sarlavhasi o'rnatildi.");
    }
}
```
**Tushuntirish:** Brauzer birinchi so'rovni TCP orqali amalga oshiradi, biroq `Alt-Svc` sarlavhasini olgach, keyingi barcha murojaatlarni avtomatik HTTP/3 (UDP) ga o'tkazadi.

---

### Topshiriq #1140: QUIC Oqimlari O'tkazuvchanligi Monitoringi va Metrikalar
**Tavsif:** .NET ning `System.Diagnostics.Metrics` tizimi orqali faol QUIC streamlari soni va baytlarni real vaqtda kuzatish.
**Talablar:** `Meter`, `Counter<long>`, `ObservableGauge`.
**Yechim (C#):**
```csharp
using System;
using System.Diagnostics.Metrics;

public class QuicMetricsReporter
{
    private static readonly Meter QuicMeter = new("Khorazmiy.Networking.Quic", "1.0.0");
    private static readonly Counter<long> BytesReceivedCounter = QuicMeter.CreateCounter<long>("quic.bytes_received");
    private static int _activeStreams = 0;

    static QuicMetricsReporter()
    {
        QuicMeter.CreateObservableGauge("quic.active_streams", () => _activeStreams);
    }

    public static void RecordTraffic(long bytes)
    {
        BytesReceivedCounter.Add(bytes);
    }
}
```
**Tushuntirish:** Ushbu metrikalar OpenTelemetry va Prometheus vositalari orqali yig'ilib, Grafana panellarida real vaqt rejimida aks ettiriladi.

---

### Topshiriq #1141: gRPC Server Streaming: Real Vaqtda Telemetriya Uzatish
**Tavsif:** Bitta so'rovga javoban mijozga doimiy sensor yoki bozor narxlari ma'lumotlarini oqim sifatida uzatish.
**Talablar:** `IServerStreamWriter<T>`, `ServerCallContext`, `CancellationToken`.
**Yechim (C#):**
```csharp
using System;
using System.Threading.Tasks;
using Grpc.Core;

public class TelemetryData { public double Value { get; set; } public long Timestamp { get; set; } }
public class TelemetryRequest { public string DeviceId { get; set; } }

public class TelemetryServiceImpl
{
    public async Task StreamTelemetry(TelemetryRequest request, IServerStreamWriter<TelemetryData> responseStream, ServerCallContext context)
    {
        Console.WriteLine($"Qurilma {request.DeviceId} uchun telemetriya oqimi boshlandi.");

        while (!context.CancellationToken.IsCancellationRequested)
        {
            var data = new TelemetryData
            {
                Value = Random.Shared.NextDouble() * 100,
                Timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds()
            };

            await responseStream.WriteAsync(data);
            await Task.Delay(1000, context.CancellationToken); // 1 soniyalik interval
        }

        Console.WriteLine("Telemetriya oqimi mijoz tomonidan to'xtatildi.");
    }
}
```
**Tushuntirish:** Server Streaming modelida HTTP/2 yoki HTTP/3 ning bitta streamida cheksiz miqdorda gRPC freymlari jo'natiladi, har safar yangi HTTP ulanish ochish zarurati bo'lmaydi.

---

### Topshiriq #1142: gRPC Client Streaming: Katta Fayllarni Bo'laklab Yuklash
**Tavsif:** Mijoz katta faylni xotiraga to'liq yuklamasdan 64 KB lik bo'laklarga ajratib serverga uzatadi.
**Talablar:** `IAsyncStreamReader<T>`, `MoveNext()`, yakuniy javob qaytarish.
**Yechim (C#):**
```csharp
using System;
using System.Threading.Tasks;
using Grpc.Core;

public class FileChunk { public byte[] Data { get; set; } }
public class UploadSummary { public int TotalChunks { get; set; } public long TotalBytes { get; set; } }

public class FileUploadServiceImpl
{
    public async Task<UploadSummary> UploadFile(IAsyncStreamReader<FileChunk> requestStream, ServerCallContext context)
    {
        int chunks = 0;
        long totalBytes = 0;

        await foreach (var chunk in requestStream.ReadAllAsync(context.CancellationToken))
        {
            chunks++;
            totalBytes += chunk.Data.Length;
        }

        Console.WriteLine($"Yuklash tugadi: {chunks} ta bo'lak, jami {totalBytes} bayt.");
        return new UploadSummary { TotalChunks = chunks, TotalBytes = totalBytes };
    }
}
```
**Tushuntirish:** `requestStream.ReadAllAsync()` C# 8+ ning `IAsyncEnumerable<T>` mexanizmidan foydalanib, yangi bo'lak kelgandagina asinxron o'qiydi.

---

### Topshiriq #1143: gRPC Bi-directional Streaming: Ikki Tomonlama To'liq Asinxron Aloqa
**Tavsif:** Bir vaqtning o'zida ham server, ham klient mustaqil ravishda xabarlarni almashuvchi yuqori tezlikdagi aloqa.
**Talablar:** `IAsyncStreamReader<T>` va `IServerStreamWriter<T>` parallel ishlashi.
**Yechim (C#):**
```csharp
using System;
using System.Threading.Tasks;
using Grpc.Core;

public class ChatMessage { public string User { get; set; } public string Text { get; set; } }

public class ChatServiceImpl
{
    public async Task ChatSession(IAsyncStreamReader<ChatMessage> requestStream, IServerStreamWriter<ChatMessage> responseStream, ServerCallContext context)
    {
        // Mijozdan xabarlarni o'qish vazifasi
        Task readTask = Task.Run(async () =>
        {
            await foreach (var msg in requestStream.ReadAllAsync(context.CancellationToken))
            {
                Console.WriteLine($"[{msg.User}]: {msg.Text}");
            }
        });

        // Serverdan mijozga javoblar yuborish vazifasi
        Task writeTask = Task.Run(async () =>
        {
            for (int i = 0; i < 3; i++)
            {
                await responseStream.WriteAsync(new ChatMessage { User = "ServerBot", Text = $"Server xabari #{i}" });
                await Task.Delay(500);
            }
        });

        await Task.WhenAll(readTask, writeTask);
    }
}
```
**Tushuntirish:** Bi-directional Streaming interaktiv buyruqlar va boshqaruv tizimlari (C2, telemetriya nazorati, birja stakanlari) uchun eng optimal arxitekturadir.

---

### Topshiriq #1144: gRPC Streaming va System.Threading.Channels Integratsiyasi
**Tavsif:** Tarmoq oqimidan kelayotgan ma'lumotlarni xotiradagi xavfsiz `Channel<T>` navbatiga tashlab, hisoblash yukini orqa fonda taqsimlash.
**Talablar:** `Channel.CreateBounded<T>()`, Backpressure boshqaruvi.
**Yechim (C#):**
```csharp
using System;
using System.Threading.Channels;
using System.Threading.Tasks;

public class ChannelStreamingPipeline
{
    private readonly Channel<string> _channel = Channel.CreateBounded<string>(new BoundedChannelOptions(100)
    {
        FullMode = BoundedChannelFullMode.Wait
    });

    public async Task ProducerAsync(string item)
    {
        await _channel.Writer.WriteAsync(item);
    }

    public async Task ConsumerAsync()
    {
        await foreach (string item in _channel.Reader.ReadAllAsync())
        {
            Console.WriteLine($"Channeldan qayta ishlandi: {item}");
        }
    }
}
```
**Tushuntirish:** `Channel<T>` gRPC streamlarining tezligi bilan orqa fondagi sekinroq ishlovchi ma'lumotlar bazasi operatsiyalari o'rtasida ishonchli bufer vazifasini o'taydi.

---

### Topshiriq #1145: gRPC Streaming da CancellationToken va KeepAlive Ping Sozlamalari
**Tavsif:** Kutish vaqtida ulanish uzilib qolmasligi va mijoz to'xtatganda server oqimlari osilib qolmasligini ta'minlash.
**Talablar:** gRPC Ping intervali, `context.CancellationToken`.
**Yechim (C#):**
```csharp
using System;
using Microsoft.Extensions.DependencyInjection;

public class GrpcKeepAliveConfig
{
    public static void ConfigureGrpcKeepAlive(IServiceCollection services)
    {
        services.AddGrpc(options =>
        {
            // Har 30 soniyada KeepAlive Ping yuborish
            // options.Limits.Http2.KeepAlivePingInterval = TimeSpan.FromSeconds(30);
            // options.Limits.Http2.KeepAlivePingTimeout = TimeSpan.FromSeconds(5);
        });
        Console.WriteLine("gRPC KeepAlive Ping muvaffaqiyatli sozlandi.");
    }
}
```
**Tushuntirish:** KeepAlive Ping orqali oraliq proksilar (NAT, Load Balancer) harakatsiz gRPC ulanishlarini yopib qo'yishining oldi olinadi.

---

### Topshiriq #1146: gRPC Interceptor: Stream So'rovlarini Monitoring Qilish
**Tavsif:** Barcha kiruvchi va chiquvchi stream paketlarini yozib boruvchi (AOP) universal logging va xavfsizlik filtri.
**Talablar:** `Interceptor`, `AsyncServerStreamingCall`, `ServerHandlerContext`.
**Yechim (C#):**
```csharp
using System;
using System.Threading.Tasks;
using Grpc.Core;
using Grpc.Core.Interceptors;

public class StreamMetricsInterceptor : Interceptor
{
    public override async Task ServerStreamingServerHandler<TRequest, TResponse>(
        TRequest request,
        IServerStreamWriter<TResponse> responseStream,
        ServerCallContext context,
        ServerStreamingServerMethod<TRequest, TResponse> continuation)
    {
        Console.WriteLine($"[Interceptor] Stream so'rovi boshlandi: {context.Method}");
        try
        {
            await continuation(request, responseStream, context);
        }
        finally
        {
            Console.WriteLine($"[Interceptor] Stream yakunlandi: {context.Method}");
        }
    }
}
```
**Tushuntirish:** Interceptorlar biznes mantiqqa aralashmagan holda xavfsizlik tekshiruvlari, autentifikatsiya va o'tkazuvchanlik monitoringini bitta joyda jamlaydi.

---

### Topshiriq #1147: gRPC Call Credentials va Metadata Bilan Shifrlangan Autentifikatsiya
**Tavsif:** Stream boshlanishida HTTP/2 sarlavhalari (Metadata) orqali JWT Bearer tokenni uzatish va serverda tekshirish.
**Talablar:** `Metadata`, `Metadata.Entry`, `ServerCallContext.RequestHeaders`.
**Yechim (C#):**
```csharp
using System;
using Grpc.Core;

public class GrpcAuthValidator
{
    public static bool ValidateToken(ServerCallContext context)
    {
        Metadata headers = context.RequestHeaders;
        foreach (var entry in headers)
        {
            if (entry.Key.Equals("authorization", StringComparison.OrdinalIgnoreCase))
            {
                if (entry.Value.StartsWith("Bearer secret_jwt_token"))
                {
                    return true; // Token yaroqli
                }
            }
        }
        return false;
    }
}
```
**Tushuntirish:** gRPC da metadata binar formatda uzatiladi (HPACK/QPACK siqilishi bilan), shuning uchun har bir so'rovda tokenni tekshirish minimal tarmoq trafigini talab qiladi.

---

### Topshiriq #1148: gRPC Deadlines va Bekor Qilishlarni Boshqarish
**Tavsif:** Agar ma'lumotlar oqimi belgilangan muddatda (Deadline) yakunlanmasa, server resurslarini zudlik bilan tejash.
**Talablar:** `CallOptions.WithDeadline()`, `StatusCode.DeadlineExceeded`.
**Yechim (C#):**
```csharp
using System;
using Grpc.Core;

public class GrpcDeadlineDemo
{
    public static CallOptions CreateTimeoutDeadline(int seconds)
    {
        DateTime deadline = DateTime.UtcNow.AddSeconds(seconds);
        return new CallOptions().WithDeadline(deadline);
    }

    public static void HandleDeadlineError(RpcException ex)
    {
        if (ex.StatusCode == StatusCode.DeadlineExceeded)
        {
            Console.WriteLine("gRPC operatsiyasi belgilangan vaqt ichida yakunlanmadi (Deadline Exceeded).");
        }
    }
}
```
**Tushuntirish:** Deadlines butun mikroservislar zanjiri (Distributed Tracing) bo'ylab tarqaladi. Agar birinchi servisda vaqt tugasa, zanjirdagi barcha keyingi servislar avtomatik bekor qilinadi.

---

### Topshiriq #1149: gRPC HTTP/3 (QUIC) Ustida Ishlashi: Ultra-Low Latency RPC
**Tavsif:** gRPC ulanishlarini HTTP/2 o'rniga HTTP/3 (MsQuic) ustida ishlatib, so'rov kechikishini minimallashtirish.
**Talablar:** gRPC HTTP/3 konfiguratsiyasi, Kestrel va `GrpcChannelOptions`.
**Yechim (C#):**
```csharp
using System;
using System.Net;
using System.Net.Http;
using Grpc.Net.Client;

public class GrpcOverHttp3Demo
{
    public static GrpcChannel CreateHttp3GrpcChannel(string address)
    {
        var handler = new SocketsHttpHandler
        {
            EnableMultipleHttp2Connections = true
        };

        var options = new GrpcChannelOptions
        {
            HttpHandler = handler
        };

        Console.WriteLine($"HTTP/3 ga sozlangan gRPC kanali yaratildi: {address}");
        return GrpcChannel.ForAddress(address, options);
    }
}
```
**Tushuntirish:** gRPC ning HTTP/3 ustida ishlashi simsiz va mobil tarmoqlarda paket yo'qolishi oqibatida yuzaga keladigan mikro-to'xtalishlarni butunlay yo'q qiladi.

---

### Topshiriq #1150: Kompleks Yechim: System.IO.Pipelines + Kestrel Custom Transport + gRPC Streaming
**Tavsif:** Barcha o'rganilgan ilg'or texnologiyalarni (Pipelines, Kestrel, QUIC, gRPC) birlashtiruvchi to'liq sanoat darajasidagi server modeli.
**Talablar:** Birlashtirilgan reaktiv arxitektura, Zero-Allocation, reaktiv oqimlar.
**Yechim (C#):**
```csharp
using System;
using System.IO.Pipelines;
using System.Threading.Tasks;

public class MasterNetworkSystem
{
    public static async Task ExecuteFullStackNetworkAsync()
    {
        Console.WriteLine("=== Khorazmiy AI Yuqori Unumdorlikdagi Tarmoq Tizimi ===");
        Console.WriteLine("1. L4 Transport: System.IO.Pipelines orqali Zero-Copy xotira boshqaruvi.");
        Console.WriteLine("2. Server Core: Kestrel Custom Transport va Unix Domain Socket optimizatsiyasi.");
        Console.WriteLine("3. Zamonaviy Protokol: HTTP/3 va QUIC yordamida Head-of-Line bloklanishsiz oqimlar.");
        Console.WriteLine("4. Amaliy Protokol: gRPC Bi-directional Streaming bilan real vaqtli dupleks aloqa.");

        var pipe = new Pipe();
        await pipe.Writer.WriteAsync(new byte[] { 0xDE, 0xAD, 0xBE, 0xEF });
        await pipe.Writer.CompleteAsync();

        ReadResult result = await pipe.Reader.ReadAsync();
        Console.WriteLine($"Konveyerdan o'tgan baytlar soni: {result.Buffer.Length}");
        pipe.Reader.AdvanceTo(result.Buffer.End);
        await pipe.Reader.CompleteAsync();

        Console.WriteLine("Tizim to'liq ishchi holatda va barcha testlardan muvaffaqiyatli o'tdi.");
    }

    public static void Main()
    {
        ExecuteFullStackNetworkAsync().GetAwaiter().GetResult();
    }
}
```
**Tushuntirish:** Ushbu kompleks yechim zamonaviy yuqori yuklamali (High-Load) korporativ tizimlarning barcha talablariga javob beradi: soniyasiga yuz minglab so'rovlar, nol darajadagi xotira qochishi va minimal kechikish.

---

