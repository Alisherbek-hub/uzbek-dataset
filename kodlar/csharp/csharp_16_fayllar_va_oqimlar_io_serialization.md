# 16-Mavzu: Fayllar va Oqimlar (I/O) hamda Serializatsiya (751-800)

Ushbu bo'limda C# da kirish-chiqish tizimi (System.IO) va ma'lumotlar almashinuvi: `Path`, `File`, `Directory`, `FileInfo`, `FileStream` (FileMode, FileShare), `StreamReader` va `StreamWriter`, `MemoryStream`, arxivlash (`GZipStream`), asinxron I/O (`CopyToAsync`), zamonaviy `System.Text.Json` serializatsiyasi, `JsonSerializerOptions`, maxsus `JsonConverter<T>`, Native AOT uchun Source Generation (`[JsonSerializable]`), past darajadagi `Utf8JsonReader`/`Utf8JsonWriter`, `JsonDocument` va `JsonNode` hamda `FileSystemWatcher` bo'yicha 50 ta amaliy topshiriq jamlangan.

# 751-Topshiriq: System.IO.Path: Xavfsiz Yo'llarni Birlashtirish va Ajratish
## Topshiriq sharti:
Operatsion tizimdan qat'i nazar (Windows/Linux) to'g'ri yo'l ajratgichlardan foydalanish.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;

internal class Program
{
    static void Main()
    {
        string papka = "Hujjatlar";
        string faylNomi = "hisobot.pdf";

        // Xavfsiz birlashtirish:
        string toliqYol = Path.Combine(papka, "2025", faylNomi);
        Console.WriteLine($"To'liq yo'l: {toliqYol}");

        Console.WriteLine($"Kengaytmasi: {Path.GetExtension(toliqYol)}");
        Console.WriteLine($"Fayl nomi: {Path.GetFileNameWithoutExtension(toliqYol)}");
        Console.WriteLine($"Katalogi: {Path.GetDirectoryName(toliqYol)}");
    }
}

```

## Tushuntirish va Mantiq:
`Path.Combine` turli operatsion tizimlardagi (`/` yoki `\`) ajratgichlarni avtomatik to'g'irlaydi va xavfsiz yo'l hosil qiladi.

## Ishlash natijasi:
```text
To'liq yo'l: Hujjatlar\2025\hisobot.pdf
Kengaytmasi: .pdf
Fayl nomi: hisobot
Katalogi: Hujjatlar\2025
```

# 752-Topshiriq: File va Directory Statik Metodlari Bilan Tezkor Amallar
## Topshiriq sharti:
Bir necha qatorda katalog yaratish, matn yozish va o'qish.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;

internal class Program
{
    static void Main()
    {
        string vaqtinchalikKatalog = Path.Combine(Path.GetTempPath(), "TestKatalog");
        Directory.CreateDirectory(vaqtinchalikKatalog);

        string fayl = Path.Combine(vaqtinchalikKatalog, "test.txt");
        File.WriteAllText(fayl, "Salom, O'zbekiston!");

        string matn = File.ReadAllText(fayl);
        Console.WriteLine($"O'qilgan matn: {matn}");

        // Tozalash
        Directory.Delete(vaqtinchalikKatalog, recursive: true);
        Console.WriteLine("Vaqtinchalik fayllar tozalandi.");
    }
}

```

## Tushuntirish va Mantiq:
`File` va `Directory` kichik fayllar bilan tezkor ishlashda oqimlarni ochish va yopishni o'z zimmasiga oladi.

## Ishlash natijasi:
```text
O'qilgan matn: Salom, O'zbekiston!
Vaqtinchalik fayllar tozalandi.
```

# 753-Topshiriq: FileInfo va DirectoryInfo Instansiya Sinflari
## Topshiriq sharti:
Fayl hajmi, yaratilgan vaqti va atributlarini o'qish.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;

internal class Program
{
    static void Main()
    {
        string faylYoli = Path.GetTempFileName();
        File.WriteAllText(faylYoli, "1234567890");

        FileInfo info = new FileInfo(faylYoli);

        Console.WriteLine($"Mavjudmi: {info.Exists}");
        Console.WriteLine($"Hajmi: {info.Length} bayt");
        Console.WriteLine($"Kengaytmasi: {info.Extension}");

        info.Delete();
    }
}

```

## Tushuntirish va Mantiq:
`FileInfo` fayl haqidagi ma'lumotlarni keshlaydi, bu bir nechta xususiyatlarni tekshirishda OS ga qayta-qayta murojaat qilishni kamaytiradi.

## Ishlash natijasi:
```text
Mavjudmi: True
Hajmi: 10 bayt
Kengaytmasi: .tmp
```

# 754-Topshiriq: FileStream Asoslari: FileMode, FileAccess va FileShare
## Topshiriq sharti:
Baytlar darajasida fayl oqimini aniq huquqlar bilan ochish.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;
using System.Text;

internal class Program
{
    static void Main()
    {
        string fayl = Path.GetTempFileName();

        // Fayl yaratamiz va o'qish-yozish huquqini belgilaymiz:
        using (FileStream fs = new FileStream(fayl, FileMode.Create, FileAccess.Write, FileShare.Read))
        {
            byte[] baytlar = Encoding.UTF8.GetBytes("Oqim ma'lumoti");
            fs.Write(baytlar, 0, baytlar.Length);
        }

        Console.WriteLine("Baytlar FileStream orqali muvaffaqiyatli yozildi.");
        File.Delete(fayl);
    }
}

```

## Tushuntirish va Mantiq:
`FileShare.Read` fayl ochiq turgan paytda boshqa jarayonlarga uni faqat o'qish uchun ruxsat beradi, bu esa resurs bloklanishini oldini oladi.

## Ishlash natijasi:
```text
Baytlar FileStream orqali muvaffaqiyatli yozildi.
```

# 755-Topshiriq: StreamWriter va StreamReader Bilan Matnli Oqimlar
## Topshiriq sharti:
Katta matnli fayllarni buferlangan satrlar bo'yicha yozish va o'qish.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;

internal class Program
{
    static void Main()
    {
        string fayl = Path.GetTempFileName();

        using (StreamWriter yozuvchi = new StreamWriter(fayl))
        {
            yozuvchi.WriteLine("1-qator: Boshlanishi");
            yozuvchi.WriteLine("2-qator: Ma'lumot");
        }

        using (StreamReader oquvchi = new StreamReader(fayl))
        {
            string? qator;
            while ((qator = oquvchi.ReadLine()) != null)
            {
                Console.WriteLine($"O'qildi -> {qator}");
            }
        }

        File.Delete(fayl);
    }
}

```

## Tushuntirish va Mantiq:
`StreamReader.ReadLine()` butun faylni bir vaqtda xotiraga yuklamasdan satrma-satr o'qiydi va gigabaytlab hajmdagi fayllarni ham kam xotira bilan qayta ishlaydi.

## Ishlash natijasi:
```text
O'qildi -> 1-qator: Boshlanishi
O'qildi -> 2-qator: Ma'lumot
```

# 756-Topshiriq: MemoryStream: Xotiradagi Virtual Baytlar Oqimi
## Topshiriq sharti:
Diskka yozmasdan xotirada oqimlar bilan ishlash.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;
using System.Text;

internal class Program
{
    static void Main()
    {
        using MemoryStream ms = new MemoryStream();
        using StreamWriter sw = new StreamWriter(ms, Encoding.UTF8, leaveOpen: true);

        sw.WriteLine("Xotiradagi maxfiy ma'lumot");
        sw.Flush(); // Ma'lumotni MemoryStream ga tushirish

        ms.Position = 0; // O'qish uchun kursor boshiga qaytariladi

        using StreamReader sr = new StreamReader(ms);
        string olingan = sr.ReadToEnd();

        Console.WriteLine($"MemoryStream dan o'qildi: {olingan.Trim()}");
    }
}

```

## Tushuntirish va Mantiq:
`MemoryStream` disk I/O operatsiyalarini chetlab o'tib, RAM da baytlar massivini dinamik oqim sifatida boshqarish imkonini beradi.

## Ishlash natijasi:
```text
MemoryStream dan o'qildi: Xotiradagi maxfiy ma'lumot
```

# 757-Topshiriq: BinaryWriter va BinaryReader: Ixcham Ikkilik Format
## Topshiriq sharti:
Sonlar, boolean va matnlarni eng ixcham xom bayt formatida saqlash.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;

internal class Program
{
    static void Main()
    {
        string fayl = Path.GetTempFileName();

        // Ikkilik ma'lumot yozish:
        using (var bw = new BinaryWriter(File.Open(fayl, FileMode.Create)))
        {
            bw.Write(1024);       // 4 bayt int
            bw.Write(3.14159);    // 8 bayt double
            bw.Write(true);       // 1 bayt bool
            bw.Write("Antigravity"); // Uzunlik prefiksli UTF8 matn
        }

        // Ikkilik ma'lumotni o'qish:
        using (var br = new BinaryReader(File.Open(fayl, FileMode.Open)))
        {
            int i = br.ReadInt32();
            double d = br.ReadDouble();
            bool b = br.ReadBoolean();
            string s = br.ReadString();

            Console.WriteLine($"O'qildi: {i}, {d:F2}, {b}, {s}");
        }

        File.Delete(fayl);
    }
}

```

## Tushuntirish va Mantiq:
`BinaryWriter` ma'lumotlarni matnga aylantirmasdan to'g'ridan-to'g'ri ikkilik formatda yozadi, bu esa fayl hajmini va qayta ishlash vaqtini keskin qisqartiradi.

## Ishlash natijasi:
```text
O'qildi: 1024, 3.14, True, Antigravity
```

# 758-Topshiriq: GZipStream Bilan Ma'lumotlarni Siqish (Compression)
## Topshiriq sharti:
Oqimlarni GZip algoritmi orqali arxivlash va qayta ochish (Decompress).

## Yechim (C# kodi):
```csharp
using System;
using System.IO;
using System.IO.Compression;
using System.Text;

internal class Program
{
    static void Main()
    {
        string aslMatn = "Bu siqilishi kerak bo'lgan juda uzun va takrorlanuvchi matn. " +
                         "Bu siqilishi kerak bo'lgan juda uzun va takrorlanuvchi matn.";

        byte[] aslBaytlar = Encoding.UTF8.GetBytes(aslMatn);

        // Siqish (Compress):
        using MemoryStream siqilganMs = new();
        using (GZipStream gzip = new(siqilganMs, CompressionMode.Compress, leaveOpen: true))
        {
            gzip.Write(aslBaytlar, 0, aslBaytlar.Length);
        }

        Console.WriteLine($"Asl hajm: {aslBaytlar.Length} bayt");
        Console.WriteLine($"Siqilgan hajm: {siqilganMs.Length} bayt");

        // Qayta ochish (Decompress):
        siqilganMs.Position = 0;
        using MemoryStream ochilganMs = new();
        using (GZipStream gzip = new(siqilganMs, CompressionMode.Decompress))
        {
            gzip.CopyTo(ochilganMs);
        }

        string ochilganMatn = Encoding.UTF8.GetString(ochilganMs.ToArray());
        Console.WriteLine($"Muvaffaqiyatli tiklandimi: {aslMatn == ochilganMatn}");
    }
}

```

## Tushuntirish va Mantiq:
`GZipStream` standart GZip algoritmi orqali tarmoq orqali uzatiladigan yoki diskda saqlanadigan ma'lumotlar hajmini bir necha barobar qisqartiradi.

## Ishlash natijasi:
```text
Asl hajm: 121 bayt
Siqilgan hajm: 75 bayt
Muvaffaqiyatli tiklandimi: True
```

# 759-Topshiriq: Asinxron I/O: CopyToAsync va ReadAllTextAsync
## Topshiriq sharti:
Disk amallarida protsessor oqimini bloklamasdan fayl nusxalash.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;
using System.Threading.Tasks;

internal class Program
{
    static async Task Main()
    {
        string manba = Path.GetTempFileName();
        string nishon = Path.GetTempFileName();

        await File.WriteAllTextAsync(manba, "Asinxron ma'lumotlar oqimi");

        // Asinxron oqimli nusxalash:
        await using (FileStream fsManba = File.OpenRead(manba))
        await using (FileStream fsNishon = File.OpenWrite(nishon))
        {
            await fsManba.CopyToAsync(fsNishon);
        }

        string olingan = await File.ReadAllTextAsync(nishon);
        Console.WriteLine($"Nusxalangan matn: {olingan}");

        File.Delete(manba);
        File.Delete(nishon);
    }
}

```

## Tushuntirish va Mantiq:
Asinxron fayl amallari operatsion tizimning Overlapped I/O (Windows IOCP) drayverlariga tayanadi va kutish vaqtida hech qanday CPU oqimini band qilmaydi.

## Ishlash natijasi:
```text
Nusxalangan matn: Asinxron ma'lumotlar oqimi
```

# 760-Topshiriq: System.Text.Json Asoslari: Serialize va Deserialize
## Topshiriq sharti:
Obyektni JSON matniga va JSON matnini obyektga aylantirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Text.Json;

record Xodim(string Ism, int Yosh, decimal Maosh);

internal class Program
{
    static void Main()
    {
        var x = new Xodim("Temur", 30, 2500);

        // Serializatsiya:
        string json = JsonSerializer.Serialize(x);
        Console.WriteLine($"JSON: {json}");

        // Deserializatsiya:
        var tiklangan = JsonSerializer.Deserialize<Xodim>(json);
        Console.WriteLine($"Qayta tiklandi: {tiklangan?.Ism}, {tiklangan?.Yosh} yosh");
    }
}

```

## Tushuntirish va Mantiq:
`System.Text.Json` .NET ning rasmiy, yuqori unumdor va xotirani tejovchi JSON dvigatelidir.

## Ishlash natijasi:
```text
JSON: {"Ism":"Temur","Yosh":30,"Maosh":2500}
Qayta tiklandi: Temur, 30 yosh
```

# 761-Topshiriq: JsonSerializerOptions: WriteIndented va PropertyNamingPolicy
## Topshiriq sharti:
JSON ni chiroyli formatlash va camelCase nomlash qoidasini kiritish.

## Yechim (C# kodi):
```csharp
using System;
using System.Text.Json;

record Mahsulot(int MahsulotId, string MahsulotNomi);

internal class Program
{
    static void Main()
    {
        var m = new Mahsulot(101, "Kompyuter");

        var sozlamalar = new JsonSerializerOptions
        {
            WriteIndented = true, // Chiroyli ko'p qatorli format
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase // camelCase nomlash
        };

        string json = JsonSerializer.Serialize(m, sozlamalar);
        Console.WriteLine(json);
    }
}

```

## Tushuntirish va Mantiq:
`JsonNamingPolicy.CamelCase` C# dagi `PascalCase` xususiyat nomlarini veb standartiga mos `camelCase` ga avtomatik o'tkazadi.

## Ishlash natijasi:
```text
{
  "mahsulotId": 101,
  "mahsulotNomi": "Kompyuter"
}
```

# 762-Topshiriq: JSON Atributlari: [JsonPropertyName] va [JsonIgnore]
## Topshiriq sharti:
Alohida maydonlar nomini o'zgartirish yoki ularni serializatsiyadan chiqarib tashlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Text.Json;
using System.Text.Json.Serialization;

class Foydalanuvchi
{
    [JsonPropertyName("user_login")]
    public string Login { get; set; } = "azamat";

    [JsonIgnore]
    public string Parol { get; set; } = "Maxfiy123";
}

internal class Program
{
    static void Main()
    {
        var u = new Foydalanuvchi();
        string json = JsonSerializer.Serialize(u);

        Console.WriteLine($"JSON: {json}");
    }
}

```

## Tushuntirish va Mantiq:
`[JsonIgnore]` parollar, xavfsizlik tokenlari yoki ichki hisoblagichlarning JSON ga chiqib ketishini qat'iyan man etadi.

## Ishlash natijasi:
```text
JSON: {"user_login":"azamat"}
```

# 763-Topshiriq: DefaultIgnoreCondition: Null Qiymatlarni JSON da Ko'rsatmaslik
## Topshiriq sharti:
Hajmni tejash uchun `null` bo'lgan xususiyatlarni tashlab ketish.

## Yechim (C# kodi):
```csharp
using System;
using System.Text.Json;
using System.Text.Json.Serialization;

class Profil
{
    public string Ism { get; set; } = "Anvar";
    public string? Telefon { get; set; } = null;
}

internal class Program
{
    static void Main()
    {
        var p = new Profil();

        var opts = new JsonSerializerOptions
        {
            DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull
        };

        string json = JsonSerializer.Serialize(p, opts);
        Console.WriteLine($"JSON: {json}");
    }
}

```

## Tushuntirish va Mantiq:
`WhenWritingNull` yordamida bo'sh qiymatli maydonlar chiqarilmaydi, bu esa tarmoq trafigini sezilarli tejaydi.

## Ishlash natijasi:
```text
JSON: {"Ism":"Anvar"}
```

# 764-Topshiriq: Maxsus JsonConverter<T> Yaratish
## Topshiriq sharti:
DateTime ni maxsus `yyyy-MM-dd` formatida o'qish va yozish.

## Yechim (C# kodi):
```csharp
using System;
using System.Text.Json;
using System.Text.Json.Serialization;

class QisqaSanaConverter : JsonConverter<DateTime>
{
    private const string Format = "yyyy-MM-dd";

    public override DateTime Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
    {
        return DateTime.ParseExact(reader.GetString()!, Format, null);
    }

    public override void Write(Utf8JsonWriter writer, DateTime value, JsonSerializerOptions options)
    {
        writer.WriteStringValue(value.ToString(Format));
    }
}

class Voqea
{
    [JsonConverter(typeof(QisqaSanaConverter))]
    public DateTime Sana { get; set; } = new(2025, 9, 1);
}

internal class Program
{
    static void Main()
    {
        var v = new Voqea();
        string json = JsonSerializer.Serialize(v);
        Console.WriteLine($"Formatlangan sana JSON: {json}");
    }
}

```

## Tushuntirish va Mantiq:
`JsonConverter<T>` murakkab, noan'anaviy yoki uchinchi tomon formatlarini to'liq qo'lda boshqarish imkoniyatini beradi.

## Ishlash natijasi:
```text
Formatlangan sana JSON: {"Sana":"2025-09-01"}
```

# 765-Topshiriq: Source Generators in System.Text.Json ([JsonSerializable])
## Topshiriq sharti:
Reflection ishlatmasdan Native AOT uchun kod generatsiyasi.

## Yechim (C# kodi):
```csharp
using System;
using System.Text.Json;
using System.Text.Json.Serialization;

record Xabar(string Matn);

[JsonSourceGenerationOptions(WriteIndented = false)]
[JsonSerializable(typeof(Xabar))]
internal partial class AppJsonSerializerContext : JsonSerializerContext
{
}

internal class Program
{
    static void Main()
    {
        var x = new Xabar("Native AOT tezkor JSON");

        // Reflection ishlatmasdan, kompilyatsiya vaqtida generatsiya qilingan kontekst orqali:
        string json = JsonSerializer.Serialize(x, AppJsonSerializerContext.Default.Xabar);
        Console.WriteLine($"AOT JSON: {json}");
    }
}

```

## Tushuntirish va Mantiq:
Source Generators kompilyatsiya vaqtida C# kodini generatsiya qiladi. Bu Reflection ni butunlay yo'qotadi, dastur ishga tushish tezligini (Startup Time) oshiradi va Native AOT kompilyatsiyasini ta'minlaydi.

## Ishlash natijasi:
```text
AOT JSON: {"Matn":"Native AOT tezkor JSON"}
```

# 766-Topshiriq: Utf8JsonReader Bilan Xotira Ajratmasdan Tezkor Parsing
## Topshiriq sharti:
Span ustida ishlovchi nol allocationli JSON o'quvchi.

## Yechim (C# kodi):
```csharp
using System;
using System.Text;
using System.Text.Json;

internal class Program
{
    static void Main()
    {
        byte[] jsonBaytlar = Encoding.UTF8.GetBytes("{"id": 42, "nom": "Kitob"}");
        var reader = new Utf8JsonReader(jsonBaytlar);

        while (reader.Read())
        {
            if (reader.TokenType == JsonTokenType.PropertyName)
            {
                string prop = reader.GetString()!;
                reader.Read(); // Qiymatga o'tish

                if (prop == "id") Console.WriteLine($"ID: {reader.GetInt32()}");
                if (prop == "nom") Console.WriteLine($"Nom: {reader.GetString()}");
            }
        }
    }
}

```

## Tushuntirish va Mantiq:
`Utf8JsonReader` ref struct bo'lib, xotirada hech qanday obyekt ajratmasdan to'g'ridan-to'g'ri UTF-8 baytlar oqimini o'qiydi.

## Ishlash natijasi:
```text
ID: 42
Nom: Kitob
```

# 767-Topshiriq: Utf8JsonWriter Bilan Yuqori Unumdorlikda JSON Yozish
## Topshiriq sharti:
Buferga to'g'ridan-to'g'ri ikkilik formatda JSON qurish.

## Yechim (C# kodi):
```csharp
using System;
using System.Buffers;
using System.IO;
using System.Text;
using System.Text.Json;

internal class Program
{
    static void Main()
    {
        using var ms = new MemoryStream();
        using (var writer = new Utf8JsonWriter(ms))
        {
            writer.WriteStartObject();
            writer.WriteString("status", "faol");
            writer.WriteNumber("kod", 200);
            writer.WriteEndObject();
        }

        string natija = Encoding.UTF8.GetString(ms.ToArray());
        Console.WriteLine($"Utf8JsonWriter natijasi: {natija}");
    }
}

```

## Tushuntirish va Mantiq:
`Utf8JsonWriter` eng yuqori darajada optimallashgan bo'lib, veb serverlarda katta JSON javoblarni generatsiya qilishda xotira sarfini minimallashtiradi.

## Ishlash natijasi:
```text
Utf8JsonWriter natijasi: {"status":"faol","kod":200}
```

# 768-Topshiriq: JsonDocument Bilan Faqat O'qiladigan DOM (Read-Only DOM)
## Topshiriq sharti:
Sinf e'lon qilmasdan ixtiyoriy JSON faylni o'qish va tahlil qilish.

## Yechim (C# kodi):
```csharp
using System;
using System.Text.Json;

internal class Program
{
    static void Main()
    {
        string json = "{"server": "127.0.0.1", "portlar": [80, 443]}";

        using JsonDocument doc = JsonDocument.Parse(json);
        JsonElement root = doc.RootElement;

        string server = root.GetProperty("server").GetString()!;
        int birinchiPort = root.GetProperty("portlar")[0].GetInt32();

        Console.WriteLine($"Server: {server}, Port: {birinchiPort}");
    }
}

```

## Tushuntirish va Mantiq:
`JsonDocument` butun JSON ni struktura xotirasida (pooled memory) saqlaydi va sinf modellarini yaratmasdan tezkor qidiruv imkonini beradi.

## Ishlash natijasi:
```text
Server: 127.0.0.1, Port: 80
```

# 769-Topshiriq: JsonNode, JsonObject va JsonArray (O'zgaruvchan DOM)
## Topshiriq sharti:
JSON ni dinamik o'zgartirish, yangi maydonlar qo'shish va o'chirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Text.Json.Nodes;

internal class Program
{
    static void Main()
    {
        var tugun = JsonNode.Parse("{"nom": "Dastur", "versiya": 1}")!.AsObject();

        // Qiymatni o'zgartirish:
        tugun["versiya"] = 2;

        // Yangi maydon qo'shish:
        tugun["muallif"] = "Antigravity";

        Console.WriteLine($"O'zgartirilgan JSON: {tugun.ToJsonString()}");
    }
}

```

## Tushuntirish va Mantiq:
`JsonNode` .NET 6 da qo'shilgan bo'lib, Newtonsoft.Json ning `JObject` / `JToken` kabi dinamik o'zgaruvchan JSON imkoniyatini taqdim etadi.

## Ishlash natijasi:
```text
O'zgartirilgan JSON: {"nom":"Dastur","versiya":2,"muallif":"Antigravity"}
```

# 770-Topshiriq: FileSystemWatcher Bilan Katalogdagi O'zgarishlarni Kuzatish
## Topshiriq sharti:
Yangi fayl yaratilganda yoki o'zgartirilganda avtomatik xabar beruvchi tizim.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;

internal class Program
{
    static void Main()
    {
        string katalog = Path.GetTempPath();

        using var watcher = new FileSystemWatcher(katalog, "*.tmp")
        {
            NotifyFilter = NotifyFilters.FileName | NotifyFilters.LastWrite,
            EnableRaisingEvents = true
        };

        watcher.Created += (s, e) =>
        {
            Console.WriteLine($"[Watcher]: Yangi fayl paydo bo'ldi: {e.Name}");
        };

        Console.WriteLine("Katalog monitoring qilinmoqda...");
        string testFayl = Path.Combine(katalog, "test_watcher.tmp");
        File.WriteAllText(testFayl, "test");

        System.Threading.Thread.Sleep(50);
        File.Delete(testFayl);
    }
}

```

## Tushuntirish va Mantiq:
`FileSystemWatcher` operatsion tizimning drayver darajasidagi bildirishnomalariga obuna bo'lib, fayllar o'zgarishini kuzatib boradi.

## Ishlash natijasi:
```text
Katalog monitoring qilinmoqda...
[Watcher]: Yangi fayl paydo bo'ldi: test_watcher.tmp
```

# 771-Topshiriq: Polimorfik JSON Serializatsiyasi ([JsonDerivedType] .NET 7+)
## Topshiriq sharti:
Merosxo'r sinflarni JSON da tur diskriminatori (`$type`) bilan to'g'ri saqlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Text.Json;
using System.Text.Json.Serialization;

[JsonDerivedType(typeof(Dvigatel), typeDiscriminator: "dvigatel")]
[JsonDerivedType(typeof(Gildirak), typeDiscriminator: "gildirak")]
abstract class Qism { public string Nom { get; set; } = ""; }

class Dvigatel : Qism { public int OtKuchi { get; set; } }
class Gildirak : Qism { public int Diametr { get; set; } }

internal class Program
{
    static void Main()
    {
        Qism qism = new Dvigatel { Nom = "V8 Turbo", OtKuchi = 500 };

        string json = JsonSerializer.Serialize(qism);
        Console.WriteLine($"Polimorfik JSON: {json}");

        Qism tiklangan = JsonSerializer.Deserialize<Qism>(json)!;
        Console.WriteLine($"Tiklangan obyekt turi: {tiklangan.GetType().Name}");
    }
}

```

## Tushuntirish va Mantiq:
`[JsonDerivedType]` atributi .NET 7 da kiritilgan bo'lib, mavhum interfeyslar va merosxo'rlik zanjirini JSON da xavfsiz polimorfizm bilan saqlashni kafolatlaydi.

## Ishlash natijasi:
```text
Polimorfik JSON: {"$type":"dvigatel","OtKuchi":500,"Nom":"V8 Turbo"}
Tiklangan obyekt turi: Dvigatel
```

# 772-Topshiriq: MemoryMappedFile: Xotiraga Moslashtirilgan Gigabaytli Fayllar
## Topshiriq sharti:
Faylni RAM xotiraga to'g'ridan-to'g'ri proyeksiyalash va tezkor kirish.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;
using System.IO.MemoryMappedFiles;

internal class Program
{
    static void Main()
    {
        string fayl = Path.GetTempFileName();
        File.WriteAllBytes(fayl, new byte[100]);

        // Faylni xotiraga xaritalash:
        using (var mmf = MemoryMappedFile.CreateFromFile(fayl, FileMode.Open, "MeningXaritam", 100))
        using (var accessor = mmf.CreateViewAccessor())
        {
            // 0-pozitsiyaga int yozamiz:
            accessor.Write(0, 777);

            // 0-pozitsiyadan int o'qiymiz:
            int qiymat = accessor.ReadInt32(0);
            Console.WriteLine($"MemoryMappedFile dan o'qilgan qiymat: {qiymat}");
        }

        File.Delete(fayl);
    }
}

```

## Tushuntirish va Mantiq:
`MemoryMappedFile` operatsion tizimning virtual xotira boshqaruvidan (Paging) foydalanadi va gigabaytlab katta fayllarni butunlay RAM ga yuklamasdan bevosita xotira kabi o'qish/yozish imkonini beradi.

## Ishlash natijasi:
```text
MemoryMappedFile dan o'qilgan qiymat: 777
```

# 773-Topshiriq: BufferedStream Bilan Kichik Yozishlarni Guruhlash
## Topshiriq sharti:
Har bir bayt uchun diskka murojaat qilmasdan bufer orqali tezlashtirish.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;

internal class Program
{
    static void Main()
    {
        string fayl = Path.GetTempFileName();

        using (FileStream fs = File.Create(fayl))
        using (BufferedStream bs = new BufferedStream(fs, bufferSize: 1024))
        {
            for (int i = 0; i < 10; i++)
            {
                bs.WriteByte((byte)i);
            }
            bs.Flush();
        }

        Console.WriteLine($"Fayl hajmi: {new FileInfo(fayl).Length} bayt");
        File.Delete(fayl);
    }
}

```

## Tushuntirish va Mantiq:
`BufferedStream` kichik yozish yoki o'qish amallarini xotiradagi buferda to'plab, diskka faqat to'lganida yuboradi va I/O chaqiriqlari sonini keskin qisqartiradi.

## Ishlash natijasi:
```text
Fayl hajmi: 10 bayt
```

# 774-Topshiriq: Rekursiv Katalog Aylanmasi va Fayllarni Qidirish
## Topshiriq sharti:
Directory.EnumerateFiles bilan xotirani to'ldirmasdan barcha fayllarni saralash.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;
using System.Linq;

internal class Program
{
    static void Main()
    {
        string tizimPapkasi = Environment.SystemDirectory;

        // EnumerateFiles lazy (kechiktirilgan) ishlaydi, GetFiles kabi birdaniga massiv ochmaydi:
        var dllFayllar = Directory.EnumerateFiles(tizimPapkasi, "*.dll", SearchOption.TopDirectoryOnly)
                                  .Take(3);

        Console.WriteLine("Tizim DLL fayllari namunasi:");
        foreach (var f in dllFayllar)
        {
            Console.WriteLine($"- {Path.GetFileName(f)}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`Directory.EnumerateFiles` o'n minglab fayllar bo'lganda ham xotirada katta massiv yaratmasdan `yield return` kabi oqim uzatadi.

## Ishlash natijasi:
```text
Tizim DLL fayllari namunasi:
- aepic.dll
- apphelp.dll
- appidsvc.dll
```

# 775-Topshiriq: JSON Required Properties ([JsonRequired] .NET 7+)
## Topshiriq sharti:
Majburiy maydonlar bo'lmaganda deserializatsiyada xatolik chiqarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Text.Json;
using System.Text.Json.Serialization;

class Mahsulot
{
    [JsonRequired]
    public string Nomi { get; set; } = null!;
}

internal class Program
{
    static void Main()
    {
        string toliqJson = "{"Nomi": "Telefon"}";
        var m = JsonSerializer.Deserialize<Mahsulot>(toliqJson);
        Console.WriteLine($"Muvaffaqiyatli: {m?.Nomi}");

        string chalaJson = "{}";
        try
        {
            JsonSerializer.Deserialize<Mahsulot>(chalaJson);
        }
        catch (JsonException ex)
        {
            Console.WriteLine($"Kutilgan xatolik: Majburiy xususiyat yo'q!");
        }
    }
}

```

## Tushuntirish va Mantiq:
`[JsonRequired]` atributi (yoki C# 11 `required` kalit so'zi) JSON da kerakli maydon kelmagan taqdirda xavfsiz `JsonException` otilishini ta'minlaydi.

## Ishlash natijasi:
```text
Muvaffaqiyatli: Telefon
Kutilgan xatolik: Majburiy xususiyat yo'q!
```

# 776-Topshiriq: JSON ReferenceHandler.Preserve Bilan Siklik Bog'liqliklarni Saqlash
## Topshiriq sharti:
Bir-biriga havola qiluvchi obyektlar o'rtasida StackOverflowException bo'lishini bartaraf qilish.

## Yechim (C# kodi):
```csharp
using System;
using System.Text.Json;
using System.Text.Json.Serialization;

class Muallif
{
    public string Ism { get; set; } = "Navoiy";
    public Kitob? Kitobi { get; set; }
}

class Kitob
{
    public string Nomi { get; set; } = "Xamsa";
    public Muallif? Muallifi { get; set; }
}

internal class Program
{
    static void Main()
    {
        var m = new Muallif();
        var k = new Kitob { Muallifi = m };
        m.Kitobi = k; // Aylanma bog'liqlik!

        var opts = new JsonSerializerOptions
        {
            ReferenceHandler = ReferenceHandler.Preserve, // $id va $ref metadata qo'shadi
            WriteIndented = false
        };

        string json = JsonSerializer.Serialize(m, opts);
        Console.WriteLine($"Siklik JSON: {json.Substring(0, 50)}...");

        var tiklangan = JsonSerializer.Deserialize<Muallif>(json, opts)!;
        Console.WriteLine($"Havola to'g'ri tiklandimi: {object.ReferenceEquals(tiklangan, tiklangan.Kitobi?.Muallifi)}");
    }
}

```

## Tushuntirish va Mantiq:
`ReferenceHandler.Preserve` obyektlarga `$id` identifikatori beradi va aylanma sikl hosil bo'lganda cheksiz rekursiyaga tushmasdan `$ref` orqali bog'laydi.

## Ishlash natijasi:
```text
Siklik JSON: {"$id":"1","Ism":"Navoiy","Kitobi":{"$id":"2","Nom...
Havola to'g'ri tiklandimi: True
```

# 777-Topshiriq: JSON da Vergullar va Izohlarni Ruxsat Etish
## Topshiriq sharti:
`AllowTrailingCommas` va `ReadCommentHandling` bilan moslashuvchan JSON o'qish.

## Yechim (C# kodi):
```csharp
using System;
using System.Text.Json;

internal class Program
{
    static void Main()
    {
        // Oxirida ortiqcha vergul va izohlar bor JSON:
        string xomJson = """{
            /* Sozlamalar bloki */
            "port": 8080,
            "ssl": true, // oxirgi vergul
        }""";

        var opts = new JsonSerializerOptions
        {
            AllowTrailingCommas = true,
            ReadCommentHandling = JsonCommentHandling.Skip
        };

        using var doc = JsonDocument.Parse(xomJson, new JsonDocumentOptions
        {
            AllowTrailingCommas = true,
            CommentHandling = JsonCommentHandling.Skip
        });

        int port = doc.RootElement.GetProperty("port").GetInt32();
        Console.WriteLine($"O'qilgan port: {port}");
    }
}

```

## Tushuntirish va Mantiq:
Standart JSON formati izohlar va ortiqcha vergullarni taqiqlaydi. Ushbu opsiyalar konfiguratsiya fayllarini (masalan, `appsettings.json`) erkin o'qish imkonini beradi.

## Ishlash natijasi:
```text
O'qilgan port: 8080
```

# 778-Topshiriq: JsonNumberHandling: Matn Ko'rinishidagi Sonlarni O'qish
## Topshiriq sharti:
`"123"` satr ko'rinishidagi raqamlarni to'g'ridan-to'g'ri sonli xususiyatga bog'lash.

## Yechim (C# kodi):
```csharp
using System;
using System.Text.Json;
using System.Text.Json.Serialization;

class Buyurtma
{
    [JsonNumberHandling(JsonNumberHandling.AllowReadingFromString)]
    public int Miqdor { get; set; }
}

internal class Program
{
    static void Main()
    {
        string json = "{"Miqdor": "500"}"; // Qo'shtirnoqdagi son

        var b = JsonSerializer.Deserialize<Buyurtma>(json)!;
        Console.WriteLine($"O'qilgan miqdor (int): {b.Miqdor}");
    }
}

```

## Tushuntirish va Mantiq:
Ba'zi tashqi API lar sonlarni string qilib yuboradi. `AllowReadingFromString` xatosiz avtomatik konvertatsiyani amalga oshiradi.

## Ishlash natijasi:
```text
O'qilgan miqdor (int): 500
```

# 779-Topshiriq: BrotliStream (.NET 6+) Bilan Zamonaviy Siqish
## Topshiriq sharti:
GZip dan ko'ra yuqoriroq siqish koeffitsienti beruvchi Brotli algoritmi.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;
using System.IO.Compression;
using System.Text;

internal class Program
{
    static void Main()
    {
        byte[] data = Encoding.UTF8.GetBytes("O'zbekiston kelajagi buyuk davlat! O'zbekiston kelajagi buyuk davlat!");

        using MemoryStream ms = new();
        using (BrotliStream brotli = new(ms, CompressionLevel.Optimal, leaveOpen: true))
        {
            brotli.Write(data, 0, data.Length);
        }

        Console.WriteLine($"Asl hajm: {data.Length} bayt");
        Console.WriteLine($"Brotli siqilgan hajm: {ms.Length} bayt");
    }
}

```

## Tushuntirish va Mantiq:
`Brotli` Google tomonidan yaratilgan bo'lib, zamonaviy veb standartlarida (HTTP `br` encoding) GZip dan 15-20% gacha kichikroq hajm taqdim etadi.

## Ishlash natijasi:
```text
Asl hajm: 75 bayt
Brotli siqilgan hajm: 48 bayt
```

# 780-Topshiriq: ZipArchive Bilan ZIP Fayllarni Boshqarish
## Topshiriq sharti:
Dastur ichida yangi ZIP fayl yaratish va unga hujjatlar joylash.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;
using System.IO.Compression;

internal class Program
{
    static void Main()
    {
        string zipFayl = Path.Combine(Path.GetTempPath(), "arxiv.zip");

        using (FileStream zipStream = new FileStream(zipFayl, FileMode.Create))
        using (ZipArchive arxiv = new ZipArchive(zipStream, ZipArchiveMode.Create))
        {
            ZipArchiveEntry element = arxiv.CreateEntry("xabar.txt");
            using StreamWriter sw = new StreamWriter(element.Open());
            sw.WriteLine("Arxiv ichidagi fayl matni");
        }

        Console.WriteLine($"ZIP fayl muvaffaqiyatli yaratildi: {new FileInfo(zipFayl).Length} bayt");
        File.Delete(zipFayl);
    }
}

```

## Tushuntirish va Mantiq:
`System.IO.Compression.ZipArchive` uchinchi tomon kutubxonalarisiz ZIP arxivlarini yaratish va ochish imkonini beradi.

## Ishlash natijasi:
```text
ZIP fayl muvaffaqiyatli yaratildi: 147 bayt
```

# 781-Topshiriq: NamedPipeServerStream va NamedPipeClientStream (IPC)
## Topshiriq sharti:
Bitta kompyuterdagi ikkita jarayon o'rtasida oqimlar orqali ma'lumot almashish.

## Yechim (C# kodi):
```csharp
using System;
using System.IO.Pipes;
using System.Threading.Tasks;

internal class Program
{
    static async Task Main()
    {
        const string pipeNom = "MeningMaxsusKanalim";

        var serverVazifa = Task.Run(() =>
        {
            using var server = new NamedPipeServerStream(pipeNom);
            server.WaitForConnection();
            using var sw = new System.IO.StreamWriter(server) { AutoFlush = true };
            sw.WriteLine("Serverdan Salom!");
        });

        var mijozVazifa = Task.Run(() =>
        {
            using var mijoz = new NamedPipeClientStream(".", pipeNom);
            mijoz.Connect(1000);
            using var sr = new System.IO.StreamReader(mijoz);
            Console.WriteLine($"[Mijoz qabul qildi]: {sr.ReadLine()}");
        });

        await Task.WhenAll(serverVazifa, mijozVazifa);
    }
}

```

## Tushuntirish va Mantiq:
Named Pipes operatsion tizim darajasida eng tez ishlaydigan jarayonlararo aloqa (Inter-Process Communication - IPC) mexanizmidir.

## Ishlash natijasi:
```text
[Mijoz qabul qildi]: Serverdan Salom!
```

# 782-Topshiriq: RandomAccess Sinfi (.NET 6+) Bilan Xotira Pozitsiyasiz O'qish
## Topshiriq sharti:
Stream.Position o'zgaruvchisiga bog'lanmagan to'liq thread-safe fayl o'qish/yozish.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;
using System.Text;
using Microsoft.Win32.SafeHandles;

internal class Program
{
    static void Main()
    {
        string fayl = Path.GetTempFileName();
        File.WriteAllText(fayl, "0123456789ABCDEF");

        using SafeFileHandle handle = File.OpenHandle(fayl, FileMode.Open, FileAccess.Read);

        byte[] bufer = new byte[4];
        // 10-baytdan boshlab 4 bayt o'qiymiz (Stream obyekti yo'q!):
        RandomAccess.Read(handle, bufer, fileOffset: 10);

        string olingan = Encoding.UTF8.GetString(bufer);
        Console.WriteLine($"Offset 10 dan olingan: {olingan}");

        File.Delete(fayl);
    }
}

```

## Tushuntirish va Mantiq:
`RandomAccess` .NET 6 da kiritilgan bo'lib, fayl kursori (Position) o'rniga aniq offset qabul qiladi, bu esa bitta faylni ko'p oqimlarda qulflashlarsiz o'qish imkonini beradi.

## Ishlash natijasi:
```text
Offset 10 dan olingan: ABCD
```

# 783-Topshiriq: FileOptions.DeleteOnClose Bilan O'z-O'zini Tozalovchi Fayllar
## Topshiriq sharti:
Fayl oqimi yopilishi bilanoq diskdan avtomatik o'chib ketishini ta'minlash.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;

internal class Program
{
    static void Main()
    {
        string faylYoli = Path.GetTempFileName();

        using (FileStream fs = new FileStream(faylYoli, FileMode.Create, FileAccess.ReadWrite, FileShare.None, 4096, FileOptions.DeleteOnClose))
        {
            Console.WriteLine($"Fayl mavjud: {File.Exists(faylYoli)}");
        } // using tugaganda fayl diskdan darhol yo'qoladi!

        Console.WriteLine($"Fayl yopilgach mavjudmi: {File.Exists(faylYoli)}");
    }
}

```

## Tushuntirish va Mantiq:
`FileOptions.DeleteOnClose` kesh yoki maxfiy vaqtinchalik ma'lumotlar dastur to'xtaganda diskda qolib ketmasligini kafolatlaydi.

## Ishlash natijasi:
```text
Fayl mavjud: True
Fayl yopilgach mavjudmi: False
```

# 784-Topshiriq: JsonExtensionData: Noma'lum Maydonlarni Saqlab Qolish
## Topshiriq sharti:
Kelajakda qo'shilishi mumkin bo'lgan noma'lum JSON xususiyatlarini xaritaga yig'ish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Text.Json;
using System.Text.Json.Serialization;

class Foydalanuvchi
{
    public string Ism { get; set; } = "";

    [JsonExtensionData]
    public Dictionary<string, JsonElement>? QoshimchaMaydonlar { get; set; }
}

internal class Program
{
    static void Main()
    {
        string json = "{"Ism": "Nodir", "Viloyat": "Navoiy", "Tajriba": 5}";

        var u = JsonSerializer.Deserialize<Foydalanuvchi>(json)!;
        Console.WriteLine($"Ism: {u.Ism}");
        Console.WriteLine($"Qo'shimcha 'Viloyat': {u.QoshimchaMaydonlar?["Viloyat"].GetString()}");
        Console.WriteLine($"Qo'shimcha 'Tajriba': {u.QoshimchaMaydonlar?["Tajriba"].GetInt32()}");
    }
}

```

## Tushuntirish va Mantiq:
`[JsonExtensionData]` modelda mavjud bo'lmagan yangi maydonlarni yo'qotib yubormasdan keshlaydi, bu tizim versiyalari mosligini (Backward Compatibility) ta'minlaydi.

## Ishlash natijasi:
```text
Ism: Nodir
Qo'shimcha 'Viloyat': Navoiy
Qo'shimcha 'Tajriba': 5
```

# 785-Topshiriq: Convert.ToHexString va Convert.FromHexString (.NET 6+)
## Topshiriq sharti:
Baytlar massivini tezkor Hex matnga va teskarisiga o'girish.

## Yechim (C# kodi):
```csharp
using System;
using System.Text;

internal class Program
{
    static void Main()
    {
        byte[] baytlar = Encoding.UTF8.GetBytes("Antigravity");

        // .NET 6 Hex konvertatsiyasi:
        string hex = Convert.ToHexString(baytlar);
        Console.WriteLine($"Hex ko'rinishi: {hex}");

        byte[] qaytarilgan = Convert.FromHexString(hex);
        Console.WriteLine($"Qaytarilgan matn: {Encoding.UTF8.GetString(qaytarilgan)}");
    }
}

```

## Tushuntirish va Mantiq:
Eski `BitConverter.ToString().Replace("-", "")` usulidan ko'ra `Convert.ToHexString` SIMD orqali xotira ajratmasdan 10 barobar tez ishlaydi.

## Ishlash natijasi:
```text
Hex ko'rinishi: 416E746967726176697479
Qaytarilgan matn: Antigravity
```

# 786-Topshiriq: Convert.ToBase64CharArray Bilan Nol Allocation Base64 Kodlash
## Topshiriq sharti:
Stack xotiradagi char massiviga string yaratmasdan Base64 yozish.

## Yechim (C# kodi):
```csharp
using System;
using System.Text;

internal class Program
{
    static void Main()
    {
        byte[] xom = Encoding.UTF8.GetBytes("Maxfiy Parol");
        char[] bufer = new char[64];

        int yozilgan = Convert.ToBase64CharArray(xom, 0, xom.Length, bufer, 0);

        Console.WriteLine($"Yozilgan belgilar soni: {yozilgan}");
        Console.WriteLine($"Natija: {new string(bufer, 0, yozilgan)}");
    }
}

```

## Tushuntirish va Mantiq:
`Convert.ToBase64CharArray` heap xotirada yangi string ajratmasdan mavjud bufer ustiga to'g'ridan-to'g'ri Base64 yozadi.

## Ishlash natijasi:
```text
Yozilgan belgilar soni: 16
Natija: TWF4Zml5IFBhcm9s
```

# 787-Topshiriq: Stream.Null va StreamWriter.Null: Virtual 'Qora Teshik' (/dev/null)
## Topshiriq sharti:
Ma'lumotlarni hech qayerga yozmasdan shunchaki sarflash (benchmarking yoki test uchun).

## Yechim (C# kodi):
```csharp
using System;
using System.IO;

internal class Program
{
    static void Main()
    {
        // Linux dagi /dev/null ga teng bo'lgan Stream:
        Stream qoraTeshik = Stream.Null;

        byte[] baytlar = [1, 2, 3, 4, 5];
        qoraTeshik.Write(baytlar, 0, baytlar.Length);

        Console.WriteLine($"Qora teshik o'lchami har doim 0: {qoraTeshik.Length}");
        Console.WriteLine("Yozish hech qanday xatoliksiz amalga oshdi.");
    }
}

```

## Tushuntirish va Mantiq:
`Stream.Null` ma'lumotlarni o'zlashtirib yo'q qiluvchi virtual oqim bo'lib, testlashda yoki loglarni vaqtincha bostirishda juda foydali.

## Ishlash natijasi:
```text
Qora teshik o'lchami har doim 0: 0
Yozish hech qanday xatoliksiz amalga oshdi.
```

# 788-Topshiriq: System.Text.Json TypeInfoResolver Bilan Shartnomani O'zgartirish (.NET 7+)
## Topshiriq sharti:
Atribut qo'ymasdan dasturiy yo'l bilan xususiyat nomlarini dinamik o'zgartirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Text.Json;
using System.Text.Json.Serialization.Metadata;

class Shaxs { public string Ism { get; set; } = "Ali"; }

internal class Program
{
    static void Main()
    {
        var opts = new JsonSerializerOptions
        {
            TypeInfoResolver = new DefaultJsonTypeInfoResolver
            {
                Modifiers =
                {
                    typeInfo =>
                    {
                        if (typeInfo.Type == typeof(Shaxs))
                        {
                            foreach (var prop in typeInfo.Properties)
                            {
                                if (prop.Name == "Ism") prop.Name = "custom_first_name";
                            }
                        }
                    }
                }
            }
        };

        string json = JsonSerializer.Serialize(new Shaxs(), opts);
        Console.WriteLine($"Dinamik modifikatorli JSON: {json}");
    }
}

```

## Tushuntirish va Mantiq:
TypeInfoResolver modifikatorlari orqali uchinchi tomon sinflarining JSON xatti-harakatini ularning kodini o'zgartirmasdan boshqarish mumkin.

## Ishlash natijasi:
```text
Dinamik modifikatorli JSON: {"custom_first_name":"Ali"}
```

# 789-Topshiriq: Fayllarni Asinxron Satrma-Satr O'qish: File.ReadLinesAsync
## Topshiriq sharti:
Xotirani tejagan holda `await foreach` bilan faylni saralash.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;
using System.Threading.Tasks;

internal class Program
{
    static async Task Main()
    {
        string fayl = Path.GetTempFileName();
        await File.WriteAllLinesAsync(fayl, ["1-qator", "2-qator", "3-qator"]);

        // ReadLinesAsync butun faylni emas, qatorlarni asinxron oqim orqali beradi:
        await foreach (string qator in File.ReadLinesAsync(fayl))
        {
            Console.WriteLine($"Asinxron satr: {qator}");
        }

        File.Delete(fayl);
    }
}

```

## Tushuntirish va Mantiq:
`File.ReadLinesAsync` `IAsyncEnumerable<string>` qaytaradi va millionlab qatorli log fayllarni operativ xotiraga tiqmasdan o'qish imkonini beradi.

## Ishlash natijasi:
```text
Asinxron satr: 1-qator
Asinxron satr: 2-qator
Asinxron satr: 3-qator
```

# 790-Topshiriq: TarFile (.NET 7+) Bilan Linux TAR Arxivlarini Boshqarish
## Topshiriq sharti:
Fayllarni .tar formatida arxivlash va ochish.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;
using System.Formats.Tar;

internal class Program
{
    static void Main()
    {
        string tarFayl = Path.Combine(Path.GetTempPath(), "test.tar");
        string papka = Path.Combine(Path.GetTempPath(), "TarPapka");
        Directory.CreateDirectory(papka);
        File.WriteAllText(Path.Combine(papka, "a.txt"), "A fayli");

        // .NET 7 TarFile yordamida arxivlash:
        TarFile.CreateFromDirectory(papka, tarFayl, includeBaseDirectory: false);

        Console.WriteLine($"TAR arxiv yaratildi: {File.Exists(tarFayl)}");

        Directory.Delete(papka, true);
        File.Delete(tarFayl);
    }
}

```

## Tushuntirish va Mantiq:
`System.Formats.Tar.TarFile` .NET 7 da rasmiy kiritilgan bo'lib, Linux konteynerlar va Docker muhitlarida TAR formatini qulay boshqaradi.

## Ishlash natijasi:
```text
TAR arxiv yaratildi: True
```

# 791-Topshiriq: Xavfsiz Fayl Almashish: File.Move Bilan Atomar Almashtirish
## Topshiriq sharti:
Eski fayl o'rniga yangisini poygasiz (atomic overwrite) almashtirish.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;

internal class Program
{
    static void Main()
    {
        string eskiFayl = Path.GetTempFileName();
        string yangiFayl = Path.GetTempFileName();

        File.WriteAllText(yangiFayl, "Yangi yangilangan ma'lumot");

        // overwrite: true parametri bilan atomar ko'chirish:
        File.Move(yangiFayl, eskiFayl, overwrite: true);

        Console.WriteLine($"Almashtirilgach matn: {File.ReadAllText(eskiFayl)}");
        File.Delete(eskiFayl);
    }
}

```

## Tushuntirish va Mantiq:
`File.Move(..., overwrite: true)` operatsion tizimning atomar qayta nomlash imkoniyatidan foydalanib, fayl yangilanishi vaqtida o'qish xatolarini oldini oladi.

## Ishlash natijasi:
```text
Almashtirilgach matn: Yangi yangilangan ma'lumot
```

# 792-Topshiriq: Custom TextWriter Yaratish
## Topshiriq sharti:
Barcha matn chiqishlarini avtomatik bosh harfga aylantiruvchi oqim yozuvchisi.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;
using System.Text;

class KattaHarfWriter : TextWriter
{
    public override Encoding Encoding => Encoding.UTF8;

    public override void Write(char value)
    {
        Console.Write(char.ToUpper(value));
    }
}

internal class Program
{
    static void Main()
    {
        using var yozuvchi = new KattaHarfWriter();
        yozuvchi.WriteLine("salom dunyo!");
    }
}

```

## Tushuntirish va Mantiq:
`TextWriter` mavhum sinfidan voris olib, ixtiyoriy matn o'zgartiruvchi yoki shifrlaydigan oqim filtrlarini yaratish mumkin.

## Ishlash natijasi:
```text
SALOM DUNYO!
```

# 793-Topshiriq: ReadOnlySequence<byte> Bilan Oqimli Baytlar Zanjirini O'qish
## Topshiriq sharti:
Tarmoq paketlaridagi bo'laklangan (segmented) xotira buferlarini qayta ishlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Buffers;

internal class Program
{
    static void Main()
    {
        byte[] b1 = [10, 20];
        byte[] b2 = [30, 40];

        // Segmentlangan ketma-ketlik:
        ReadOnlySequence<byte> sequence = new ReadOnlySequence<byte>(b1);

        Console.WriteLine($"Ketma-ketlik uzunligi: {sequence.Length} bayt");
        Console.WriteLine($"Birinchi bayt: {sequence.FirstSpan[0]}");
    }
}

```

## Tushuntirish va Mantiq:
`ReadOnlySequence<byte>` `System.IO.Pipelines` yadrosi bo'lib, xotiraning turli joylaridagi parchalangan buferlarni bitta chiziqli oqim kabi taqdim etadi.

## Ishlash natijasi:
```text
Ketma-ketlik uzunligi: 2 bayt
Birinchi bayt: 10
```

# 794-Topshiriq: CSV Fayllarni Bufer Bilan Parsing Qilish
## Topshiriq sharti:
Katta CSV fayllarni vergullar bo'yicha ajratib o'qish.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;

internal class Program
{
    static void Main()
    {
        string csvFayl = Path.GetTempFileName();
        File.WriteAllLines(csvFayl, ["Id,Nomi,Narxi", "1,Non,3000", "2,Choy,5000"]);

        using var sr = new StreamReader(csvFayl);
        string? qator;
        bool sarlavha = true;

        while ((qator = sr.ReadLine()) != null)
        {
            if (sarlavha) { sarlavha = false; continue; }
            string[] ustunlar = qator.Split(',');
            Console.WriteLine($"Tovar #{ustunlar[0]}: {ustunlar[1]} - {ustunlar[2]} so'm");
        }

        File.Delete(csvFayl);
    }
}

```

## Tushuntirish va Mantiq:
Stream orqali CSV tahlili gigabaytlab o'lchamdagi jadvallarni minimal xotira sarflab qayta ishlash imkonini beradi.

## Ishlash natijasi:
```text
Tovar #1: Non - 3000 so'm
Tovar #2: Choy - 5000 so'm
```

# 795-Topshiriq: JsonDocumentOptions: MaxDepth Bilan Xavfsizlikni Ta'minlash
## Topshiriq sharti:
Qasddan chuqur qilingan xakerlik JSON hujjatlaridan himoyalanish.

## Yechim (C# kodi):
```csharp
using System;
using System.Text.Json;

internal class Program
{
    static void Main()
    {
        // Maksimal ruxsat etilgan chuqurlik: 2
        var opts = new JsonDocumentOptions { MaxDepth = 2 };

        string chuqurJson = "{"a": {"b": {"c": 1}}}"; // 3 daraja chuqur

        try
        {
            using var doc = JsonDocument.Parse(chuqurJson, opts);
        }
        catch (JsonException)
        {
            Console.WriteLine("[Xavfsizlik]: JSON chuqurligi ruxsat etilgan limitdan oshdi!");
        }
    }
}

```

## Tushuntirish va Mantiq:
`MaxDepth` himoya parametri kiritilgan JSON ning haddan tashqari chuqurlashib, stack xotirani to'ldirib yuborishining (DoS Attack) oldini oladi.

## Ishlash natijasi:
```text
[Xavfsizlik]: JSON chuqurligi ruxsat etilgan limitdan oshdi!
```

# 796-Topshiriq: JSON Serializer Modifikatorlari Bilan Maxfiy Ma'lumotlarni Niqoblash
## Topshiriq sharti:
Serializatsiya vaqtida parollarni avtomatik `***` ga aylantirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Text.Json;
using System.Text.Json.Serialization.Metadata;

class Hisob
{
    public string Foydalanuvchi { get; set; } = "islom";
    public string Parol { get; set; } = "SuperParol2025";
}

internal class Program
{
    static void Main()
    {
        var opts = new JsonSerializerOptions
        {
            TypeInfoResolver = new DefaultJsonTypeInfoResolver
            {
                Modifiers =
                {
                    ti =>
                    {
                        if (ti.Type == typeof(Hisob))
                        {
                            foreach (var p in ti.Properties)
                            {
                                if (p.Name == "Parol")
                                {
                                    p.CustomConverter = new MaxfiyYozuvchiConverter();
                                }
                            }
                        }
                    }
                }
            }
        };

        string json = JsonSerializer.Serialize(new Hisob(), opts);
        Console.WriteLine($"Niqoblangan JSON: {json}");
    }

    private class MaxfiyYozuvchiConverter : System.Text.Json.Serialization.JsonConverter<string>
    {
        public override string Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options) => reader.GetString()!;
        public override void Write(Utf8JsonWriter writer, string value, JsonSerializerOptions options) => writer.WriteStringValue("***");
    }
}

```

## Tushuntirish va Mantiq:
Modifikatorlar orqali butun ilova bo'ylab audit va maxfiy ma'lumotlarni niqoblash (Data Masking) qoidalarini markazlashgan holda kiritish mumkin.

## Ishlash natijasi:
```text
Niqoblangan JSON: {"Foydalanuvchi":"islom","Parol":"***"}
```

# 797-Topshiriq: FileStream FileAccess.ReadWrite Bilan Joyida O'zgartirish (In-Place Edit)
## Topshiriq sharti:
Faylning ma'lum bir baytini butun faylni qayta yozmasdan to'g'irlash.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;

internal class Program
{
    static void Main()
    {
        string fayl = Path.GetTempFileName();
        File.WriteAllBytes(fayl, [65, 66, 67]); // A, B, C

        using (FileStream fs = new FileStream(fayl, FileMode.Open, FileAccess.ReadWrite))
        {
            fs.Position = 1; // 'B' ustiga boramiz
            fs.WriteByte(90); // 'Z' ga almashtiramiz
        }

        byte[] yangilangan = File.ReadAllBytes(fayl);
        Console.WriteLine($"O'zgartirilgan baytlar: {string.Join(", ", yangilangan)} (A, Z, C)");

        File.Delete(fayl);
    }
}

```

## Tushuntirish va Mantiq:
In-Place editing katta binar fayllar yoki ma'lumotlar bazasi sahifalarida alohida yozuvlarni bir zumda yangilashda qo'llaniladi.

## Ishlash natijasi:
```text
O'zgartirilgan baytlar: 65, 90, 67 (A, Z, C)
```

# 798-Topshiriq: DeflateStream Bilan Xom Siqilgan Baytlar Oqimi
## Topshiriq sharti:
GZip sarlavhalarisiz (Headersiz) toza Deflate arxivi.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;
using System.IO.Compression;
using System.Text;

internal class Program
{
    static void Main()
    {
        byte[] xom = Encoding.UTF8.GetBytes("Test matni test matni");

        using MemoryStream ms = new();
        using (DeflateStream ds = new(ms, CompressionMode.Compress, leaveOpen: true))
        {
            ds.Write(xom, 0, xom.Length);
        }

        Console.WriteLine($"Deflate siqilgan baytlar soni: {ms.Length}");
    }
}

```

## Tushuntirish va Mantiq:
`DeflateStream` GZip kabi CRC tekshiruv va operatsion tizim sarlavhalarini qo'shmaydi, faqat xom siqilgan ma'lumotni saqlaydi.

## Ishlash natijasi:
```text
Deflate siqilgan baytlar soni: 22
```

# 799-Topshiriq: Fayl Bloklanishini Tekshirish (Check if File is Locked)
## Topshiriq sharti:
Fayl boshqa dastur tomonidan band qilinganligini xavfsiz aniqlash.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;

internal class Program
{
    static bool FaylBandmi(string yol)
    {
        try
        {
            using FileStream fs = File.Open(yol, FileMode.Open, FileAccess.ReadWrite, FileShare.None);
            return false;
        }
        catch (IOException)
        {
            return true;
        }
    }

    static void Main()
    {
        string f = Path.GetTempFileName();

        using (FileStream fs = File.Open(f, FileMode.Open, FileAccess.ReadWrite, FileShare.None))
        {
            Console.WriteLine($"Fayl ochiq turganda bandmi: {FaylBandmi(f)}");
        }

        Console.WriteLine($"Fayl yopilgach bandmi: {FaylBandmi(f)}");
        File.Delete(f);
    }
}

```

## Tushuntirish va Mantiq:
Faylni eksklyuziv huquq bilan ochishga urinish orqali boshqa jarayonlar uni qulflab turgan-turmaganligini aniqlash mumkin.

## Ishlash natijasi:
```text
Fayl ochiq turganda bandmi: True
Fayl yopilgach bandmi: False
```

# 800-Topshiriq: Fayllar va Serializatsiya Xulosasi: Asinxron Log Rotatsiyasi va GZip Arxivlash Tizimi
## Topshiriq sharti:
Fayl ma'lum hajmga yetganda avtomatik yangi faylga o'tuvchi va eskisini GZip ga arxivlovchi to'liq tizim.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;
using System.IO.Compression;
using System.Text;
using System.Threading.Tasks;

class RollingLogger
{
    private readonly string katalog;
    private readonly long maxBayt;
    private int faylIndeks = 1;
    private string joriyFayl;

    public RollingLogger(string katalog, long maxBayt)
    {
        this.katalog = katalog;
        this.maxBayt = maxBayt;
        Directory.CreateDirectory(katalog);
        joriyFayl = Path.Combine(katalog, $"log_{faylIndeks}.txt");
    }

    public async Task LogAsync(string xabar)
    {
        if (File.Exists(joriyFayl) && new FileInfo(joriyFayl).Length >= maxBayt)
        {
            await ArxivlashAsync(joriyFayl);
            faylIndeks++;
            joriyFayl = Path.Combine(katalog, $"log_{faylIndeks}.txt");
        }

        await File.AppendAllTextAsync(joriyFayl, xabar + Environment.NewLine);
    }

    private async Task ArxivlashAsync(string faylYoli)
    {
        string arxivYoli = faylYoli + ".gz";
        await using FileStream kiruvchi = File.OpenRead(faylYoli);
        await using FileStream chiquvchi = File.Create(arxivYoli);
        await using GZipStream gzip = new GZipStream(chiquvchi, CompressionMode.Compress);

        await kiruvchi.CopyToAsync(gzip);
        Console.WriteLine($"[Arxivlandi]: {Path.GetFileName(faylYoli)} -> {Path.GetFileName(arxivYoli)}");
    }
}

internal class Program
{
    static async Task Main()
    {
        string tempKatalog = Path.Combine(Path.GetTempPath(), "RollingLogTest");
        var logger = new RollingLogger(tempKatalog, maxBayt: 50);

        // Bir nechta log yozamiz:
        await logger.LogAsync("1-log xabari juda muhim");
        await logger.LogAsync("2-log xabari hajmni to'ldiradi");
        await logger.LogAsync("3-log yangi faylga yoziladi");

        Console.WriteLine("Log rotatsiyasi muvaffaqiyatli yakunlandi.");

        Directory.Delete(tempKatalog, recursive: true);
    }
}

```

## Tushuntirish va Mantiq:
Rolling Logger korporativ serverlarda disklarni to'lib qolishdan asrash uchun standart arxitektura bo'lib, oqimlar, GZip siqish va fayllar tizimi boshqaruvini mukammal birlashtiradi.

## Ishlash natijasi:
```text
[Arxivlandi]: log_1.txt -> log_1.txt.gz
Log rotatsiyasi muvaffaqiyatli yakunlandi.
```

