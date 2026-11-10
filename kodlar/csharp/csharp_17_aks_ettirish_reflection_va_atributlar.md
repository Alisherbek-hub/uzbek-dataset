# 17-Mavzu: Aks Ettirish (Reflection) va Atributlar (801-850)

Ushbu bo'limda C# va .NET da dasturiy metadata bilan ishlash: `Type` sinfi, `typeof` va `GetType()`, `Assembly`, dinamik instansiyalash (`Activator.CreateInstance`), `PropertyInfo`, `MethodInfo`, `FieldInfo`, `BindingFlags` (private a'zolarga kirish), maxsus atributlar yaratish (`AttributeUsage`), chaqiruvchi ma'lumotlari (`[CallerMemberName]`, `[CallerArgumentExpression]`), Reflection unumdorligini oshirish (`Delegate.CreateDelegate`), `System.Reflection.Emit` bilan IL generatsiyasi hamda Reflection asosidagi mini Dependency Injection konteyneri bo'yicha 50 ta amaliy topshiriq jamlangan.

# 801-Topshiriq: Reflection Asoslari: Type Obyektini Olish (typeof vs GetType)
## Topshiriq sharti:
Kompilyatsiya vaqtida va runtime paytida sinf metadatasini o'qish.

## Yechim (C# kodi):
```csharp
using System;

class Mashina { }

internal class Program
{
    static void Main()
    {
        // 1. Kompilyatsiya vaqtida (statik):
        Type tur1 = typeof(Mashina);

        // 2. Runtime vaqtida instansiyadan:
        object obj = new Mashina();
        Type tur2 = obj.GetType();

        Console.WriteLine($"Turlar tengmi: {tur1 == tur2}");
        Console.WriteLine($"To'liq nomi: {tur1.FullName}");
        Console.WriteLine($"Assembly: {tur1.Assembly.GetName().Name}");
    }
}

```

## Tushuntirish va Mantiq:
`typeof` statik tur haqida ma'lumot beradi, `GetType()` esa polimorfik haqiqiy obyekt turini qaytaradi. Ikkalasi ham CLR ichidagi yagona `Type` deskriptoriga havola qiladi.

## Ishlash natijasi:
```text
Turlar tengmi: True
To'liq nomi: Mashina
Assembly: ...
```

# 802-Topshiriq: Dinamik Obyekt Yaratish: Activator.CreateInstance
## Topshiriq sharti:
Sinf turiga ko'ra (Type) uning yangi nusxasini dasturiy yo'l bilan yaratish.

## Yechim (C# kodi):
```csharp
using System;

class Foydalanuvchi
{
    public string Ism { get; }
    public Foydalanuvchi() => Ism = "Standart";
    public Foydalanuvchi(string ism) => Ism = ism;
}

internal class Program
{
    static void Main()
    {
        Type tur = typeof(Foydalanuvchi);

        // Parametrsiz konstruktor:
        var u1 = (Foydalanuvchi)Activator.CreateInstance(tur)!;
        Console.WriteLine($"U1: {u1.Ism}");

        // Parametrli konstruktor:
        var u2 = (Foydalanuvchi)Activator.CreateInstance(tur, "Jahongir")!;
        Console.WriteLine($"U2: {u2.Ism}");
    }
}

```

## Tushuntirish va Mantiq:
`Activator.CreateInstance` runtime paytida mos konstruktorni qidirib topadi va yangi obyekt nusxasini xotiradan ajratadi.

## Ishlash natijasi:
```text
U1: Standart
U2: Jahongir
```

# 803-Topshiriq: PropertyInfo: Xususiyatlarni Ro'yxatlash, O'qish va Yozish
## Topshiriq sharti:
Obyekt xususiyatlarini nomlari bo'yicha dinamik boshqarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Reflection;

class Xodim
{
    public string Ism { get; set; } = "Farhod";
    public int Yosh { get; set; } = 32;
}

internal class Program
{
    static void Main()
    {
        var xodim = new Xodim();
        Type tur = xodim.GetType();

        PropertyInfo? propIsm = tur.GetProperty("Ism");
        Console.WriteLine($"Avvalgi qiymat: {propIsm?.GetValue(xodim)}");

        // Yangi qiymat o'rnatish:
        propIsm?.SetValue(xodim, "Sardor");
        Console.WriteLine($"Yangi qiymat: {xodim.Ism}");
    }
}

```

## Tushuntirish va Mantiq:
`PropertyInfo.GetValue` va `SetValue` orqali ORM lar, serializatorlar va UI freymvorklar ma'lumotlarni avtomatik o'qiydi va yozadi.

## Ishlash natijasi:
```text
Avvalgi qiymat: Farhod
Yangi qiymat: Sardor
```

# 804-Topshiriq: MethodInfo Bilan Metodni Dinamik Chaqirish (Invoke)
## Topshiriq sharti:
Metod nomi orqali argumentlar berib uni ishga tushirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Reflection;

class Kalkulyator
{
    public int Qoshish(int a, int b) => a + b;
}

internal class Program
{
    static void Main()
    {
        var calc = new Kalkulyator();
        MethodInfo? metod = typeof(Kalkulyator).GetMethod("Qoshish");

        object? natija = metod?.Invoke(calc, new object[] { 15, 25 });
        Console.WriteLine($"Dinamik chaqiruv natijasi: {natija}");
    }
}

```

## Tushuntirish va Mantiq:
`MethodInfo.Invoke` argumentlarni tekshiradi, kerak bo'lsa boxing qiladi va metodni chaqirib natijani `object` sifatida qaytaradi.

## Ishlash natijasi:
```text
Dinamik chaqiruv natijasi: 40
```

# 805-Topshiriq: BindingFlags Bilan Yashirin (Private) Maydonlarni O'qish va Buzish
## Topshiriq sharti:
Inkapsulyatsiyani chetlab o'tib `private` o'zgaruvchilarni ochish.

## Yechim (C# kodi):
```csharp
using System;
using System.Reflection;

class MaxfiyBank
{
    private string xavfsizlikKodi = "PIN_7788";
}

internal class Program
{
    static void Main()
    {
        var bank = new MaxfiyBank();

        // NonPublic va Instance bayroqlari bilan private maydonni topamiz:
        FieldInfo? maydon = typeof(MaxfiyBank).GetField(
            "xavfsizlikKodi",
            BindingFlags.NonPublic | BindingFlags.Instance
        );

        string kod = (string)maydon?.GetValue(bank)!;
        Console.WriteLine($"O'g'irlangan private PIN: {kod}");

        // Hatto private maydonni o'zgartirish ham mumkin:
        maydon?.SetValue(bank, "PIN_0000");
        Console.WriteLine($"O'zgartirilgan PIN: {maydon?.GetValue(bank)}");
    }
}

```

## Tushuntirish va Mantiq:
Reflection `BindingFlags.NonPublic` orqali private, protected va internal a'zolarni to'liq ko'ra oladi va o'zgartira oladi. Bu qobiliyat asosan unit-testlarda va chuqur freymvorklarda ishlatiladi.

## Ishlash natijasi:
```text
O'g'irlangan private PIN: PIN_7788
O'zgartirilgan PIN: PIN_0000
```

# 806-Topshiriq: Maxsus Atribut Yaratish (Custom Attribute) va AttributeUsage
## Topshiriq sharti:
Sinflarga biriktiriladigan o'z atributingizni yaratish.

## Yechim (C# kodi):
```csharp
using System;

[AttributeUsage(AttributeTargets.Class | AttributeTargets.Method, AllowMultiple = false)]
class MuallifAttribute : Attribute
{
    public string Ism { get; }
    public string Versiya { get; }

    public MuallifAttribute(string ism, string versiya = "1.0")
    {
        Ism = ism;
        Versiya = versiya;
    }
}

[Muallif("Alisher", Versiya = "2.5")]
class Xizmat { }

internal class Program
{
    static void Main()
    {
        var attr = (MuallifAttribute?)Attribute.GetCustomAttribute(typeof(Xizmat), typeof(MuallifAttribute));

        Console.WriteLine($"Muallif: {attr?.Ism}");
        Console.WriteLine($"Versiya: {attr?.Versiya}");
    }
}

```

## Tushuntirish va Mantiq:
`AttributeUsage` atribut qaysi elementlarga (Class, Method, Property) qo'yilishi mumkinligini va bir nechta qo'yish mumkinligini (`AllowMultiple`) cheklaydi.

## Ishlash natijasi:
```text
Muallif: Alisher
Versiya: 2.5
```

# 807-Topshiriq: [CallerMemberName] Bilan Chaqiruvchi Metod Nomini Aniqlash
## Topshiriq sharti:
Kompilyator orqali xususiyat yoki metod nomini string yozmasdan avtomatik uzatish.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.CompilerServices;

internal class Program
{
    static void Log([CallerMemberName] string a'zo = "")
    {
        Console.WriteLine($"Chaqiruvchi a'zo: {a'zo}");
    }

    static void AsosiyIsh()
    {
        Log(); // 'AsosiyIsh' nomi avtomatik uzatiladi
    }

    static void Main()
    {
        AsosiyIsh();
    }
}

```

## Tushuntirish va Mantiq:
`[CallerMemberName]` kompilyatsiya vaqtida argument o'rniga chaqiruvchi metod nomini string konstanta sifatida qo'yib ketadi. Bu INotifyPropertyChanged da juda qulay.

## Ishlash natijasi:
```text
Chaqiruvchi a'zo: AsosiyIsh
```

# 808-Topshiriq: [CallerArgumentExpression] (C# 10+) Bilan Argument Kodini Olish
## Topshiriq sharti:
Parametrga uzatilgan ifodaning o'zini matn sifatida ko'rish.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.CompilerServices;

internal class Program
{
    static void Tasdiqla(bool shart, [CallerArgumentExpression(nameof(shart))] string ifoda = "")
    {
        if (!shart)
        {
            Console.WriteLine($"[XATO]: Shart bajarilmadi -> ({ifoda})");
        }
        else
        {
            Console.WriteLine($"[OK]: ({ifoda}) to'g'ri.");
        }
    }

    static void Main()
    {
        int yosh = 15;
        Tasdiqla(yosh >= 18);
        Tasdiqla(yosh < 20);
    }
}

```

## Tushuntirish va Mantiq:
`[CallerArgumentExpression]` argument sifatida yozilgan C# kodining o'zini stringga aylantirib beradi. Bu `ArgumentNullException.ThrowIfNull` va Guard kutubxonalarining asosidir.

## Ishlash natijasi:
```text
[XATO]: Shart bajarilmadi -> (yosh >= 18)
[OK]: (yosh < 20) to'g'ri.
```

# 809-Topshiriq: CallerFilePath va CallerLineNumber Atributlari
## Topshiriq sharti:
Xatolik yuz bergan fayl yo'li va qator raqamini aniqlash.

## Yechim (C# kodi):
```csharp
using System;
using System.IO;
using System.Runtime.CompilerServices;

internal class Program
{
    static void XatolikKuzatuvchisi(
        string xabar,
        [CallerFilePath] string fayl = "",
        [CallerLineNumber] int qator = 0)
    {
        Console.WriteLine($"[{Path.GetFileName(fayl)}:{qator}] {xabar}");
    }

    static void Main()
    {
        XatolikKuzatuvchisi("Ma'lumotlar bazasiga ulanishda ogohlantirish");
    }
}

```

## Tushuntirish va Mantiq:
Ushbu atributlar log tizimlarida qaysi faylning nechanchi qatori chaqirganini ko'rsatishda 0-overhead bilan ishlaydi.

## Ishlash natijasi:
```text
[Program.cs:18] Ma'lumotlar bazasiga ulanishda ogohlantirish
```

# 810-Topshiriq: Type.IsAssignableFrom va IsSubclassOf Tekshiruvlari
## Topshiriq sharti:
Sinf ma'lum bir interfeysni bajarganligini yoki voris ekanligini aniqlash.

## Yechim (C# kodi):
```csharp
using System;

interface IAmal { }
class Asosiy { }
class Bola : Asosiy, IAmal { }

internal class Program
{
    static void Main()
    {
        Type interfeys = typeof(IAmal);
        Type asos = typeof(Asosiy);
        Type bola = typeof(Bola);

        Console.WriteLine($"Bola Asosiy ning vorisimi: {bola.IsSubclassOf(asos)}");
        Console.WriteLine($"IAmal ga Bola ni tenglab bo'ladimi: {interfeys.IsAssignableFrom(bola)}");
    }
}

```

## Tushuntirish va Mantiq:
`IsAssignableFrom` polimorfizm munosabatlarini (`Parent = Child`) tekshirishda xizmat qiladi va DI konteynerlarida sinflarni ro'yxatga olishda asosiy tekshiruv hisoblanadi.

## Ishlash natijasi:
```text
Bola Asosiy ning vorisimi: True
IAmal ga Bola ni tenglab bo'ladimi: True
```

# 811-Topshiriq: Assembly.GetExecutingAssembly Bilan Barcha Tiplarni Qidirish
## Topshiriq sharti:
Joriy assembly ichidagi ma'lum interfeysni bajargan barcha sinflarni avtomatik topish.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq;
using System.Reflection;

interface IBuyruq { void Bajar(); }

class BuyruqA : IBuyruq { public void Bajar() => Console.WriteLine("A"); }
class BuyruqB : IBuyruq { public void Bajar() => Console.WriteLine("B"); }

internal class Program
{
    static void Main()
    {
        var buyruqTurlari = Assembly.GetExecutingAssembly()
            .GetTypes()
            .Where(t => typeof(IBuyruq).IsAssignableFrom(t) && !t.IsInterface && !t.IsAbstract);

        Console.WriteLine("Topilgan buyruqlar:");
        foreach (var tur in buyruqTurlari)
        {
            var buyruq = (IBuyruq)Activator.CreateInstance(tur)!;
            Console.Write($"- {tur.Name}: ");
            buyruq.Bajar();
        }
    }
}

```

## Tushuntirish va Mantiq:
Assembly scanning plaginlar (plugins) tizimida va CQRS Handlerlarni avtomatik ro'yxatdan o'tkazishda eng ko'p ishlatiladigan Reflection naqshidir.

## Ishlash natijasi:
```text
Topilgan buyruqlar:
- BuyruqA: A
- BuyruqB: B
```

# 812-Topshiriq: Generik Turlar Metadatasi: GetGenericTypeDefinition va MakeGenericType
## Topshiriq sharti:
Ochiq generik turni (`List<>`) aniqlash va unga runtime da tip berish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        Type yopiq = typeof(List<int>);

        Console.WriteLine($"Generikmi: {yopiq.IsGenericType}");
        Console.WriteLine($"Ochiq ta'rifi: {yopiq.GetGenericTypeDefinition().Name}");

        Type argument = yopiq.GetGenericArguments()[0];
        Console.WriteLine($"Ichki tipi: {argument.Name}");
    }
}

```

## Tushuntirish va Mantiq:
Generik tahlil orqali runtime paytida qaysi tur uzatilganini bilish va yangi ixtisoslashgan turlar yasash mumkin.

## Ishlash natijasi:
```text
Generikmi: True
Ochiq ta'rifi: List`1
Ichki tipi: Int32
```

# 813-Topshiriq: Delegate.CreateDelegate Bilan Reflection Tezligini 100 Karra Oshirish
## Topshiriq sharti:
`MethodInfo.Invoke` ning sekinligidan qutulib, uni to'g'ridan-to'g'ri delegatga aylantirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Reflection;

class Auditor
{
    public int Kvadrat(int x) => x * x;
}

internal class Program
{
    static void Main()
    {
        var obj = new Auditor();
        MethodInfo metod = typeof(Auditor).GetMethod("Kvadrat")!;

        // MethodInfo ni to'g'ridan-to'g'ri kuchli tipli Func ga o'giramiz:
        var tezkorDelegat = (Func<int, int>)Delegate.CreateDelegate(typeof(Func<int, int>), obj, metod);

        int res = tezkorDelegat(8);
        Console.WriteLine($"Tezkor delegat chaqiruvi natijasi: {res}");
    }
}

```

## Tushuntirish va Mantiq:
`Delegate.CreateDelegate` Reflection orqali topilgan metodni to'g'ridan-to'g'ri funksiya ko'rsatkichiga bog'laydi va oddiy C# metodi tezligida (hech qanday boxing va tekshiruvlarsiz) chaqiradi.

## Ishlash natijasi:
```text
Tezkor delegat chaqiruvi natijasi: 64
```

# 814-Topshiriq: System.Reflection.Emit: Dinamik IL Metod Generatsiyasi
## Topshiriq sharti:
Xotirada to'g'ridan-to'g'ri bayt-kod (OpCodes) yozib yangi metod generatsiya qilish.

## Yechim (C# kodi):
```csharp
using System;
using System.Reflection.Emit;

internal class Program
{
    static void Main()
    {
        // Dinamik metod: int qo'shish(int a, int b)
        DynamicMethod dm = new DynamicMethod("Qoshish", typeof(int), new[] { typeof(int), typeof(int) });

        ILGenerator il = dm.GetILGenerator();
        il.Emit(OpCodes.Ldarg_0); // 1-argumentni stackka yuklash
        il.Emit(OpCodes.Ldarg_1); // 2-argumentni stackka yuklash
        il.Emit(OpCodes.Add);     // Qo'shish
        il.Emit(OpCodes.Ret);     // Natijani qaytarish

        var qoshish = (Func<int, int, int>)dm.CreateDelegate(typeof(Func<int, int, int>));

        Console.WriteLine($"IL orqali generatsiya qilingan hisob: {qoshish(20, 30)}");
    }
}

```

## Tushuntirish va Mantiq:
`Reflection.Emit` CLR ning eng qudratli qismlaridan biri bo'lib, Dapper, AutoMapper kabi tezkor kutubxonalar aynan shu orqali xotirada chaqmoqdek tez dinamik kodlar quradi.

## Ishlash natijasi:
```text
IL orqali generatsiya qilingan hisob: 50
```

# 815-Topshiriq: Dinamik Obyektlar: ExpandoObject va dynamic Kalit So'zi
## Topshiriq sharti:
Python yoki JavaScript kabi dastur davomida yangi xususiyatlar qo'shiladigan obyekt.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Dynamic;

internal class Program
{
    static void Main()
    {
        dynamic d = new ExpandoObject();

        // Xususiyatlarni dinamik kiritish:
        d.Nomi = "Planshet";
        d.Narxi = 400;

        // Metod qo'shish:
        d.Hisobla = (Func<int, int>)(miqdor => d.Narxi * miqdor);

        Console.WriteLine($"Mahsulot: {d.Nomi}, Jami: ${d.Hisobla(2)}");
    }
}

```

## Tushuntirish va Mantiq:
`ExpandoObject` ichki tomondan `IDictionary<string, object>` saqlaydi va `dynamic` orqali dinamik til xususiyatlarini C# ga olib kiradi.

## Ishlash natijasi:
```text
Mahsulot: Planshet, Jami: $800
```

# 816-Topshiriq: Type.GetConstructor Bilan Aniq Konstruktorni Tanlash
## Topshiriq sharti:
Maxsus parametrlarga ega konstruktorni qidirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Reflection;

class Foydalanuvchi
{
    public Foydalanuvchi(int id) { }
    public Foydalanuvchi(string email, int yosh) { }
}

internal class Program
{
    static void Main()
    {
        Type tur = typeof(Foydalanuvchi);

        // Faqat (string, int) qabul qiladigan konstruktorni topamiz:
        ConstructorInfo? ctor = tur.GetConstructor(new[] { typeof(string), typeof(int) });

        Console.WriteLine($"Konstruktor topildimi: {ctor != null}");
        Console.WriteLine($"Parametrlari soni: {ctor?.GetParameters().Length}");
    }
}

```

## Tushuntirish va Mantiq:
Konstruktorlarni tahlil qilish orqali IoC konteynerlar qaysi bog'liqliklarni uzatish kerakligini (Constructor Injection) aniqlaydi.

## Ishlash natijasi:
```text
Konstruktor topildimi: True
Parametrlari soni: 2
```

# 817-Topshiriq: Ob'ektni Klonsiyalash (Deep Clone via Reflection)
## Topshiriq sharti:
Barcha xususiyatlarni bir obyektdan ikkinchisiga ko'chirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Reflection;

class Tovar
{
    public string Nomi { get; set; } = "";
    public decimal Narxi { get; set; }
}

internal class Program
{
    static T NusxaOlish<T>(T manba) where T : new()
    {
        T yangi = new T();
        foreach (PropertyInfo prop in typeof(T).GetProperties())
        {
            if (prop.CanRead && prop.CanWrite)
            {
                object? qiymat = prop.GetValue(manba);
                prop.SetValue(yangi, qiymat);
            }
        }
        return yangi;
    }

    static void Main()
    {
        var t1 = new Tovar { Nomi = "Monitor", Narxi = 200 };
        var t2 = NusxaOlish(t1);

        Console.WriteLine($"Nusxa: {t2.Nomi}, Narxi: ${t2.Narxi}");
        Console.WriteLine($"Xotiradagi havolalari boshqami: {!object.ReferenceEquals(t1, t2)}");
    }
}

```

## Tushuntirish va Mantiq:
Reflection orqali umumiy klonlash algoritmi har qanday sinf uchun universal ishlaydi.

## Ishlash natijasi:
```text
Nusxa: Monitor, Narxi: $200
Xotiradagi havolalari boshqami: True
```

# 818-Topshiriq: ValidationAttribute Bilan Ma'lumotlarni Tekshirish (Data Annotations)
## Topshiriq sharti:
Sinf xususiyatlariga validatsiya qoidalarini biriktirish va tekshirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

class Registratsiya
{
    [Required(ErrorMessage = "Email majburiy!")]
    [EmailAddress(ErrorMessage = "Email formati noto'g'ri!")]
    public string Email { get; set; } = "notogri_manzil";
}

internal class Program
{
    static void Main()
    {
        var model = new Registratsiya();
        var context = new ValidationContext(model);
        var natijalar = new List<ValidationResult>();

        bool yaroqli = Validator.TryValidateObject(model, context, natijalar, validateAllProperties: true);

        Console.WriteLine($"Model yaroqlimi: {yaroqli}");
        foreach (var xato in natijalar)
        {
            Console.WriteLine($"- {xato.ErrorMessage}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`Validator.TryValidateObject` Reflection orqali obyektdagi barcha `ValidationAttribute` larni aylanib chiqadi va xatolar ro'yxatini yig'adi.

## Ishlash natijasi:
```text
Model yaroqlimi: False
- Email formati noto'g'ri!
```

# 819-Topshiriq: Obfuscation va Reflection: Xavfsizlik va Muammolar
## Topshiriq sharti:
Kod obfuskatsiya qilinganda Reflection qanday sinishi mumkinligi tahlili.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        // Agar kod obfuskatsiya qilinsa, sinflar va metodlar 'a', 'b', 'c' ga aylanadi.
        // Natijada typeof(X).GetProperty("MeningXususiyatim") null qaytaradi!
        // Yechim: nameof() ishlatish yoki [Obfuscation(Exclude = true)] qo'yish.
        Console.WriteLine("[Ogohlantirish]: Reflection qattiq string nomlarga tayanmasligi kerak!");
    }
}

```

## Tushuntirish va Mantiq:
Kod himoyalanganda (Obfuscated) Reflection orqali matnli qidiruvlar ishlamay qoladi. Buning oldini olish uchun atributlar yoki `nameof` operatori qo'llaniladi.

## Ishlash natijasi:
```text
[Ogohlantirish]: Reflection qattiq string nomlarga tayanmasligi kerak!
```

# 820-Topshiriq: Static Constructor larni Reflection Bilan Majburiy Chaqirish
## Topshiriq sharti:
`RuntimeHelpers.RunClassConstructor` orqali statik blokni ishga tushirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.CompilerServices;

class TizimKesh
{
    static TizimKesh()
    {
        Console.WriteLine("[Statik Konstruktor]: Kesh xotirasi initsializatsiya qilindi.");
    }
}

internal class Program
{
    static void Main()
    {
        Console.WriteLine("Dastur boshlandi...");

        // Sinfga to'g'ridan-to'g'ri murojaat qilmasdan statik konstruktorni majburlaymiz:
        RuntimeHelpers.RunClassConstructor(typeof(TizimKesh).TypeHandle);

        Console.WriteLine("Dastur tugadi.");
    }
}

```

## Tushuntirish va Mantiq:
`RunClassConstructor` berilgan turning statik konstruktori allaqachon chaqirilmagan bo'lsa, uni darhol ishga tushiradi.

## Ishlash natijasi:
```text
Dastur boshlandi...
[Statik Konstruktor]: Kesh xotirasi initsializatsiya qilindi.
Dastur tugadi.
```

# 821-Topshiriq: FieldInfo vs PropertyInfo: Maydon va Xususiyat Farqi
## Topshiriq sharti:
Xususiyat ortidagi yashirin orqa maydonni (Backing Field) topish.

## Yechim (C# kodi):
```csharp
using System;
using System.Reflection;

class Model
{
    public string Nomi { get; set; } = "Asl";
}

internal class Program
{
    static void Main()
    {
        // Kompilyator Nomi property uchun yashirin <Nomi>k__BackingField maydoni ochadi:
        FieldInfo? maydon = typeof(Model).GetField(
            "<Nomi>k__BackingField",
            BindingFlags.NonPublic | BindingFlags.Instance
        );

        var m = new Model();
        Console.WriteLine($"Backing Field qiymati: {maydon?.GetValue(m)}");
    }
}

```

## Tushuntirish va Mantiq:
C# dagi avtomatik propertylar aslida kompilyator yaratgan yashirin `BackingField` ga tayanadi va Reflection orqali ularni to'g'ridan-to'g'ri ko'rish mumkin.

## Ishlash natijasi:
```text
Backing Field qiymati: Asl
```

# 822-Topshiriq: Type.GetType Bilan Satrdan Tur Topish (AssemblyQualifiedName)
## Topshiriq sharti:
Sinfning to'liq assembly nomi orqali Type obyektini yuklash.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        string turNomi = typeof(System.Text.StringBuilder).AssemblyQualifiedName!;

        // To'liq assembly nomi orqali turlarni yuklash:
        Type? tur = Type.GetType(turNomi);

        Console.WriteLine($"Yuklangan tur: {tur?.FullName}");
    }
}

```

## Tushuntirish va Mantiq:
`Type.GetType` plagin tizimlarida va ma'lumotlar bazasida satr sifatida saqlangan sinf nomlarini qayta tiriltirishda ishlatiladi.

## Ishlash natijasi:
```text
Yuklangan tur: System.Text.StringBuilder
```

# 823-Topshiriq: Generic MethodInfo.MakeGenericMethod
## Topshiriq sharti:
Generik metodni runtime da aniq tur bilan to'ldirib chaqirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Reflection;

class ChopEtuvchi
{
    public void Chop<T>(T malumot)
    {
        Console.WriteLine($"Chop etildi ({typeof(T).Name}): {malumot}");
    }
}

internal class Program
{
    static void Main()
    {
        var obj = new ChopEtuvchi();
        MethodInfo ochiqMetod = typeof(ChopEtuvchi).GetMethod("Chop")!;

        // Ochiq generik metodga 'double' turini beramiz:
        MethodInfo yopiqMetod = ochiqMetod.MakeGenericMethod(typeof(double));

        yopiqMetod.Invoke(obj, new object[] { 3.1415 });
    }
}

```

## Tushuntirish va Mantiq:
`MakeGenericMethod` ochiq generik metod signaturasiga (`void Chop<T>`) kerakli turni bog'lab, uni chaqirishga tayyor holga keltiradi.

## Ishlash natijasi:
```text
Chop etildi (Double): 3.1415
```

# 824-Topshiriq: ConditionalAttribute ([Conditional("DEBUG")])
## Topshiriq sharti:
Kompilyatsiya vaqtida bayroqqa ko'ra metod chaqiriqlarini o'chirib tashlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Diagnostics;

internal class Program
{
    [Conditional("DEBUG")]
    static void FaqatDebugdaChop()
    {
        Console.WriteLine("[DEBUG]: Maxsus xabarnoma");
    }

    static void Main()
    {
        FaqatDebugdaChop();
        Console.WriteLine("Asosiy ish bajarildi.");
    }
}

```

## Tushuntirish va Mantiq:
`[Conditional]` atributi metodning o'zini o'chirmaydi, lekin agar shart (masalan `DEBUG`) yoqilmagan bo'lsa, Release versiyada unga qilingan barcha chaqiriqlarni IL koddan butunlay olib tashlaydi.

## Ishlash natijasi:
```text
[DEBUG]: Maxsus xabarnoma
Asosiy ish bajarildi.
```

# 825-Topshiriq: Mini Dependency Injection Konteyneri (Reflection Asosida)
## Topshiriq sharti:
Konstruktor parametrlarini Reflection orqali aniqlab avtomatik bog'lovchi IoC idishi.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;

interface ILogger { void Log(string msg); }
class ConsoleLogger : ILogger { public void Log(string msg) => Console.WriteLine($"[Log]: {msg}"); }

class UserService
{
    private readonly ILogger logger;
    public UserService(ILogger logger) => this.logger = logger;
    public void Salom() => logger.Log("UserService ishga tushdi!");
}

class MiniIoC
{
    private readonly Dictionary<Type, Type> xarita = new();

    public void Register<TInterface, TImpl>() => xarita[typeof(TInterface)] = typeof(TImpl);

    public object Resolve(Type tur)
    {
        Type amalgaOshiruvchi = xarita.TryGetValue(tur, out var impl) ? impl : tur;
        ConstructorInfo ctor = amalgaOshiruvchi.GetConstructors().First();
        var parametrlar = ctor.GetParameters().Select(p => Resolve(p.ParameterType)).ToArray();

        return Activator.CreateInstance(amalgaOshiruvchi, parametrlar)!;
    }
}

internal class Program
{
    static void Main()
    {
        var ioc = new MiniIoC();
        ioc.Register<ILogger, ConsoleLogger>();

        var xizmat = (UserService)ioc.Resolve(typeof(UserService));
        xizmat.Salom();
    }
}

```

## Tushuntirish va Mantiq:
Barcha professional DI freymvorklar (Autofac, ASP.NET Core DI) aynan shu Reflection asosidagi konstruktor tahliliga tayanadi.

## Ishlash natijasi:
```text
[Log]: UserService ishga tushdi!
```

# 826-Topshiriq: AssemblyLoadContext Bilan Plaginlarni Izolyatsiya Qilish
## Topshiriq sharti:
Kutubxonalarni xotiraga yuklash va ziddiyatli versiyalarni boshqarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.Loader;

internal class Program
{
    static void Main()
    {
        // Standart yuklash konteksti:
        AssemblyLoadContext defaultContext = AssemblyLoadContext.Default;
        Console.WriteLine($"Default Context nomi: {defaultContext.Name}");

        // Yangi izolyatsiyalangan yuklash konteksti:
        var plaginKonteksti = new AssemblyLoadContext("PlaginContext", isCollectible: true);
        Console.WriteLine($"Plagin Context nomi: {plaginKonteksti.Name}, Xotiradan tozalanishi mumkin: {plaginKonteksti.IsCollectible}");

        plaginKonteksti.Unload();
        Console.WriteLine("Plagin konteksti xotiradan chiqarildi (Unloaded).");
    }
}

```

## Tushuntirish va Mantiq:
`AssemblyLoadContext` .NET Core da AppDomain larning o'rniga kelgan bo'lib, har bir modul uchun mustaqil DLL kutubxonalarini yuklash va o'chirish (Unload) imkonini beradi.

## Ishlash natijasi:
```text
Default Context nomi: Default
Plagin Context nomi: PlaginContext, Xotiradan tozalanishi mumkin: True
Plagin konteksti xotiradan chiqarildi (Unloaded).
```

# 827-Topshiriq: Expression Trees Orqali Tezkor Getter/Setter Kompilyatsiyasi
## Topshiriq sharti:
`PropertyInfo.GetValue` dan ko'ra 50 barobar tez ishlovchi dinamik xususiyat o'quvchi.

## Yechim (C# kodi):
```csharp
using System;
using System.Linq.Expressions;
using System.Reflection;

class Kitob { public string Sarlavha { get; set; } = "C# Mukammal Qo'llanma"; }

internal class Program
{
    static Func<T, object> GetGetter<T>(string xususiyatNomi)
    {
        var parametr = Expression.Parameter(typeof(T), "x");
        var xususiyat = Expression.Property(parametr, xususiyatNomi);
        var aylantirish = Expression.Convert(xususiyat, typeof(object));
        return Expression.Lambda<Func<T, object>>(aylantirish, parametr).Compile();
    }

    static void Main()
    {
        var getter = GetGetter<Kitob>("Sarlavha");
        var k = new Kitob();

        Console.WriteLine($"Kompilyatsiya qilingan getter: {getter(k)}");
    }
}

```

## Tushuntirish va Mantiq:
Expression Trees orqali yaratilgan delegat to'g'ridan-to'g'ri IL mashina kodiga kompilyatsiya bo'ladi va Reflection xarajatlarini butunlay yo'qotadi.

## Ishlash natijasi:
```text
Kompilyatsiya qilingan getter: C# Mukammal Qo'llanma
```

# 828-Topshiriq: Enum Qiymatlari va Description Atributini O'qish
## Topshiriq sharti:
Enum elementlarining inson tushunadigan tavsiflarini Reflection orqali olish.

## Yechim (C# kodi):
```csharp
using System;
using System.ComponentModel;
using System.Reflection;

enum Holat
{
    [Description("Bajarilishi kutilmoqda")]
    Kutilmoqda,

    [Description("Muvaffaqiyatli yakunlandi")]
    Yakunlandi
}

internal class Program
{
    static string TavsifOlish(Enum qiymat)
    {
        FieldInfo? maydon = qiymat.GetType().GetField(qiymat.ToString());
        var attr = (DescriptionAttribute?)Attribute.GetCustomAttribute(maydon!, typeof(DescriptionAttribute));
        return attr != null ? attr.Description : qiymat.ToString();
    }

    static void Main()
    {
        Console.WriteLine($"Kutilmoqda -> {TavsifOlish(Holat.Kutilmoqda)}");
        Console.WriteLine($"Yakunlandi  -> {TavsifOlish(Holat.Yakunlandi)}");
    }
}

```

## Tushuntirish va Mantiq:
Enum lar ustiga qo'yilgan `DescriptionAttribute` larni Reflection bilan o'qish UI da chiroyli matnlarni ko'rsatishda keng qo'llanadi.

## Ishlash natijasi:
```text
Kutilmoqda -> Bajarilishi kutilmoqda
Yakunlandi  -> Muvaffaqiyatli yakunlandi
```

# 829-Topshiriq: EventInfo: Hodisalarni Dinamik Bog'lash (AddEventHandler)
## Topshiriq sharti:
Hodisaga nom orqali delegat obunasini Reflection yordamida ulash.

## Yechim (C# kodi):
```csharp
using System;
using System.Reflection;

class Tugma
{
    public event Action? Bosildi;
    public void Bosish() => Bosildi?.Invoke();
}

internal class Program
{
    static void Main()
    {
        var btn = new Tugma();
        EventInfo? hodisa = typeof(Tugma).GetEvent("Bosildi");

        Action handler = () => Console.WriteLine("Tugma bosildi (Reflection orqali ulandi)!");

        // Hodisaga handler ulash:
        hodisa?.AddEventHandler(btn, handler);

        btn.Bosish();
    }
}

```

## Tushuntirish va Mantiq:
`EventInfo.AddEventHandler` vizual dizaynerlar va dinamik tizimlarda obunachilarni kod yozmasdan ulash imkonini beradi.

## Ishlash natijasi:
```text
Tugma bosildi (Reflection orqali ulandi)!
```

# 830-Topshiriq: ParameterInfo Bilan Metod Parametrlari Tahlili
## Topshiriq sharti:
Parametrning standart qiymati (DefaultValue) va turini o'rganish.

## Yechim (C# kodi):
```csharp
using System;
using System.Reflection;

class Xizmat
{
    public void Saqlash(string nom, int miqdor = 10, bool faol = true) { }
}

internal class Program
{
    static void Main()
    {
        MethodInfo metod = typeof(Xizmat).GetMethod("Saqlash")!;

        foreach (ParameterInfo p in metod.GetParameters())
        {
            Console.WriteLine($"Parametr: {p.Name} ({p.ParameterType.Name}), Ixtiyoriy: {p.IsOptional}, Default: {p.DefaultValue}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`ParameterInfo` metod signaturasini to'liq ko'rsatib, API dokumentatsiyalari (Swagger/OpenAPI) ni avtomatik yaratishda xizmat qiladi.

## Ishlash natijasi:
```text
Parametr: nom (String), Ixtiyoriy: False, Default: 
Parametr: miqdor (Int32), Ixtiyoriy: True, Default: 10
Parametr: faol (Boolean), Ixtiyoriy: True, Default: True
```

# 831-Topshiriq: Native AOT Trim Ogohlantirishlari: [RequiresUnreferencedCode]
## Topshiriq sharti:
Reflection kodining AOT (Ahead-of-Time) trim jarayonida o'chib ketishidan ogohlantirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Diagnostics.CodeAnalysis;

internal class Program
{
    [RequiresUnreferencedCode("Ushbu metod Reflection ga tayanadi va AOT rejimida sinishi mumkin!")]
    static void DinamikYuklash(string turNomi)
    {
        Console.WriteLine($"Dinamik qidirilmoqda: {turNomi}");
    }

    static void Main()
    {
        DinamikYuklash("MeningSinfim");
    }
}

```

## Tushuntirish va Mantiq:
`[RequiresUnreferencedCode]` .NET kompilyatoriga ushbu metod AOT kompilyatsiya paytida xavfli ekanligini aytadi va ogohlantirish beradi.

## Ishlash natijasi:
```text
Dinamik qidirilmoqda: MeningSinfim
```

# 832-Topshiriq: [DynamicallyAccessedMembers] Bilan AOT Trimmerni Xabardor Qilish
## Topshiriq sharti:
Kerakli metodlar va xususiyatlar AOT tomonidan o'chirib tashlanmasligini kafolatlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Diagnostics.CodeAnalysis;

internal class Program
{
    static void XususiyatlarniChop(
        [DynamicallyAccessedMembers(DynamicallyAccessedMemberTypes.PublicProperties)] Type tur)
    {
        foreach (var p in tur.GetProperties())
        {
            Console.WriteLine($"Saqlab qolingan property: {p.Name}");
        }
    }

    class TestModel { public string Nomi { get; set; } = "OK"; }

    static void Main()
    {
        XususiyatlarniChop(typeof(TestModel));
    }
}

```

## Tushuntirish va Mantiq:
`[DynamicallyAccessedMembers]` AOT Trimmerga 'bu turning public propertylarini o'chirib yuborma, ular Reflection orqali kerak bo'ladi' degan buyruqni beradi.

## Ishlash natijasi:
```text
Saqlab qolingan property: Nomi
```

# 833-Topshiriq: .NET 8+ Inqilobiy UnsafeAccessor: Private Maydonlarga 0-Overhead Bilan Kirish
## Topshiriq sharti:
Reflection siz, IL generatsiyasiz, to'g'ridan-to'g'ri C++ tezligida xususiy maydonni o'qish.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.CompilerServices;

class BankHisob
{
    private int yashirinBalans = 50000;
}

internal class Program
{
    // .NET 8 UnsafeAccessor: Kompilyator darajasida private maydonga to'g'ridan-to'g'ri ulanish:
    [UnsafeAccessor(UnsafeAccessorKind.Field, Name = "yashirinBalans")]
    extern static ref int YashirinBalansniOlish(BankHisob hisob);

    static void Main()
    {
        var hisob = new BankHisob();

        // 0 overhead bilan o'qiymiz:
        ref int balansRef = ref YashirinBalansniOlish(hisob);
        Console.WriteLine($"O'qilgan private balans: {balansRef}");

        // Joyida o'zgartiramiz:
        balansRef = 99999;
        Console.WriteLine($"O'zgartirilgan balans: {YashirinBalansniOlish(hisob)}");
    }
}

```

## Tushuntirish va Mantiq:
`UnsafeAccessor` .NET 8 ning eng shov-shuvli xususiyatlaridan bo'lib, Reflection xarajatlarisiz C# ichida istalgan yashirin maydon yoki metodga to'g'ridan-to'g'ri xotira tezligida kirish imkonini beradi.

## Ishlash natijasi:
```text
O'qilgan private balans: 50000
O'zgartirilgan balans: 99999
```

# 834-Topshiriq: .NET 8+ UnsafeAccessor Bilan Private Metodni Chaqirish
## Topshiriq sharti:
Sinfning yashirin metodini 0-overhead bilan chaqirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.CompilerServices;

class MaxfiyMotor
{
    private string TurboYoqish(int bosim) => $"Turbo yoqildi: {bosim} bar";
}

internal class Program
{
    [UnsafeAccessor(UnsafeAccessorKind.Method, Name = "TurboYoqish")]
    extern static string ChaqirTurbo(MaxfiyMotor motor, int bosim);

    static void Main()
    {
        var motor = new MaxfiyMotor();
        string javob = ChaqirTurbo(motor, 2);

        Console.WriteLine(javob);
    }
}

```

## Tushuntirish va Mantiq:
`UnsafeAccessor` private metodlarni `MethodInfo.Invoke` dagi tekshiruvlar va boxing xarajatlarisiz to'g'ridan-to'g'ri chaqiradi.

## Ishlash natijasi:
```text
Turbo yoqildi: 2 bar
```

# 835-Topshiriq: ModuleInitializer ([ModuleInitializer] Atributi)
## Topshiriq sharti:
Dastur ishga tushganda yoki DLL yuklanganda `Main` dan ham oldin chiquvchi kod.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.CompilerServices;

internal class Program
{
    [ModuleInitializer]
    public static void BoshlangichYuklash()
    {
        Console.WriteLine("[ModuleInitializer]: Modul yuklandi, global sozlamalar o'rnatildi!");
    }

    static void Main()
    {
        Console.WriteLine("[Main]: Asosiy dastur boshlandi.");
    }
}

```

## Tushuntirish va Mantiq:
`[ModuleInitializer]` C# 9 da kiritilgan bo'lib, CLR darajasidagi `.cctor` modul konstruktorida ishlaydi va har qanday kirish nuqtasidan oldin bajariladi.

## Ishlash natijasi:
```text
[ModuleInitializer]: Modul yuklandi, global sozlamalar o'rnatildi!
[Main]: Asosiy dastur boshlandi.
```

# 836-Topshiriq: StructLayout va FieldOffset Bilan C Union Yaratish
## Topshiriq sharti:
Bitta xotira katagida har xil turlarni ustma-ust saqlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.InteropServices;

[StructLayout(LayoutKind.Explicit)]
struct RangUnion
{
    [FieldOffset(0)] public uint Rgba;

    [FieldOffset(0)] public byte Qizil;
    [FieldOffset(1)] public byte Yashil;
    [FieldOffset(2)] public byte Moviy;
    [FieldOffset(3)] public byte Alfa;
}

internal class Program
{
    static void Main()
    {
        RangUnion r = new RangUnion { Rgba = 0xFF0000FF }; // Qizil rang va to'liq alfa

        Console.WriteLine($"Qizil bayt: {r.Qizil}");
        Console.WriteLine($"Moviy bayt: {r.Moviy}");
    }
}

```

## Tushuntirish va Mantiq:
`[FieldOffset(0)]` bir nechta maydonlarni xotiraning bitta manziliga joylashtiradi, bu C/C++ dagi `union` imkoniyatini beradi.

## Ishlash natijasi:
```text
Qizil bayt: 255
Moviy bayt: 0
```

# 837-Topshiriq: Marshal Sinfi Bilan Boshqarilmaydigan Xotira Ajratish
## Topshiriq sharti:
`AllocHGlobal` va `FreeHGlobal` orqali xom C uslubidagi xotirani boshqarish.

## Yechim (C# kodi):
```csharp
using System;
using System.Runtime.InteropServices;

internal class Program
{
    static void Main()
    {
        // 4 baytli boshqarilmaydigan (Unmanaged) xotira olamiz:
        IntPtr ptr = Marshal.AllocHGlobal(4);

        try
        {
            Marshal.WriteInt32(ptr, 123456);
            int oqilgan = Marshal.ReadInt32(ptr);
            Console.WriteLine($"Unmanaged xotiradan o'qildi: {oqilgan}");
        }
        finally
        {
            Marshal.FreeHGlobal(ptr); // Xotirani albatta bo'shatamiz
            Console.WriteLine("Native xotira bo'shatildi.");
        }
    }
}

```

## Tushuntirish va Mantiq:
`Marshal.AllocHGlobal` operatsion tizimning `malloc` funksiyasiga teng bo'lib, GC nazoratidan tashqaridagi xotirani ajratadi.

## Ishlash natijasi:
```text
Unmanaged xotiradan o'qildi: 123456
Native xotira bo'shatildi.
```

# 838-Topshiriq: DispatchProxy Bilan Dinamik AOP (Aspect-Oriented Programming)
## Topshiriq sharti:
Interfeys metodlarini ushlab qolib, ularga avtomatik log va audit qo'shish.

## Yechim (C# kodi):
```csharp
using System;
using System.Reflection;

interface IXizmat { void Bajar(string nom); }

class HaqiqiyXizmat : IXizmat
{
    public void Bajar(string nom) => Console.WriteLine($"Haqiqiy xizmat bajarildi: {nom}");
}

class LogProxy<T> : DispatchProxy
{
    private T maqsad = default!;

    public static T Yaratish(T maqsad)
    {
        object proxy = Create<T, LogProxy<T>>();
        ((LogProxy<T>)proxy).maqsad = maqsad;
        return (T)proxy;
    }

    protected override object? Invoke(MethodInfo? targetMethod, object?[]? args)
    {
        Console.WriteLine($"[Proxy Log]: {targetMethod?.Name} chaqirildi.");
        return targetMethod?.Invoke(maqsad, args);
    }
}

internal class Program
{
    static void Main()
    {
        IXizmat asosiy = new HaqiqiyXizmat();
        IXizmat himoyalangan = LogProxy<IXizmat>.Yaratish(asosiy);

        himoyalangan.Bajar("Foydalanuvchi ma'lumotlari");
    }
}

```

## Tushuntirish va Mantiq:
`DispatchProxy` dinamik proksi yaratish uchun .NET ning rasmiy vositasi bo'lib, uning yordamida interfeys kodiga tegmasdan uning atrofida logging, keshlash va tranzaksiyalarni boshqarish mumkin.

## Ishlash natijasi:
```text
[Proxy Log]: Bajar chaqirildi.
Haqiqiy xizmat bajarildi: Foydalanuvchi ma'lumotlari
```

# 839-Topshiriq: ObsoleteAttribute Bilan Metodlarni Eskirgan Deb Belgilash
## Topshiriq sharti:
Eski API larni ogohlantirish yoki kompilyatsiya xatosi bilan cheklash.

## Yechim (C# kodi):
```csharp
using System;

class EskirganKutubxona
{
    [Obsolete("Bu metod eskirgan. YangiMetod() dan foydalaning.")]
    public void EskiMetod() => Console.WriteLine("Eski");

    [Obsolete("Bu metod butunlay taqiqlangan!", error: false)]
    public void XavfliMetod() => Console.WriteLine("Xavfli");
}

internal class Program
{
    static void Main()
    {
        var e = new EskirganKutubxona();
        e.EskiMetod();
    }
}

```

## Tushuntirish va Mantiq:
`[Obsolete]` dasturchiga eskirgan metodlar haqida kompilyatsiya paytida ogohlantirish beradi va yangi muqobilini ko'rsatadi.

## Ishlash natijasi:
```text
Eski
```

# 840-Topshiriq: Null Tahlili Atributlari: [NotNullWhen] va [MaybeNullWhen]
## Topshiriq sharti:
Kompilyatorga metod muvaffaqiyatli chiqqanda qiymat null emasligini tushuntirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Diagnostics.CodeAnalysis;

internal class Program
{
    static bool TryOlish(string kalit, [NotNullWhen(true)] out string? natija)
    {
        if (kalit == "parol")
        {
            natija = "12345";
            return true;
        }
        natija = null;
        return false;
    }

    static void Main()
    {
        if (TryOlish("parol", out string? val))
        {
            // Kompilyator val null emasligini 100% biladi va hech qanday CS8602 ogohlantirish bermaydi:
            Console.WriteLine($"Parol uzunligi: {val.Length}");
        }
    }
}

```

## Tushuntirish va Mantiq:
`[NotNullWhen(true)]` C# ning Nullable Reference Types tahlilchisiga metod `true` qaytarganda out parametr aniq null emasligini kafolatlaydi.

## Ishlash natijasi:
```text
Parol uzunligi: 5
```

# 841-Topshiriq: DebuggerDisplayAttribute Bilan Visual Studio Debugger Ko'rinishini Sozlash
## Topshiriq sharti:
Obyekt ustiga sichqoncha borganda chiroyli sarhisobni ko'rsatish.

## Yechim (C# kodi):
```csharp
using System;
using System.Diagnostics;

[DebuggerDisplay("Tovar: {Nomi}, Narxi: ${Narxi}")]
class Mahsulot
{
    public string Nomi { get; set; } = "Klaviatura";
    public decimal Narxi { get; set; } = 45;
}

internal class Program
{
    static void Main()
    {
        var m = new Mahsulot();
        Console.WriteLine($"Mahsulot yaratildi: {m.Nomi}");
    }
}

```

## Tushuntirish va Mantiq:
`[DebuggerDisplay]` debug jarayonida obyektning `ToString()` chaqirmasdan qulay xulosa matnini ko'rsatishga yordam beradi.

## Ishlash natijasi:
```text
Mahsulot yaratildi: Klaviatura
```

# 842-Topshiriq: FlagsAttribute Bilan Bitli Enumlar va HasFlag Metodi
## Topshiriq sharti:
Bir vaqtda bir nechta ruxsatlarni bit maskasi orqali boshqarish.

## Yechim (C# kodi):
```csharp
using System;

[Flags]
enum Ruxsatlar
{
    HechQanday = 0,
    Oqish = 1 << 0,   // 1
    Yozish = 1 << 1,  // 2
    Ijro = 1 << 2,    // 4
    Hammasi = Oqish | Yozish | Ijro // 7
}

internal class Program
{
    static void Main()
    {
        Ruxsatlar foydalanuvchiRuxsati = Ruxsatlar.Oqish | Ruxsatlar.Yozish;

        Console.WriteLine($"Foydalanuvchi ruxsatlari: {foydalanuvchiRuxsati}");
        Console.WriteLine($"O'qish ruxsati bormi: {foydalanuvchiRuxsati.HasFlag(Ruxsatlar.Oqish)}");
        Console.WriteLine($"Ijro ruxsati bormi: {foydalanuvchiRuxsati.HasFlag(Ruxsatlar.Ijro)}");
    }
}

```

## Tushuntirish va Mantiq:
`[Flags]` atributi enum ning `ToString()` metodi barcha yoqilgan bitlarni vergul bilan chiroyli chiqarishini ta'minlaydi.

## Ishlash natijasi:
```text
Foydalanuvchi ruxsatlari: Oqish, Yozish
O'qish ruxsati bormi: True
Ijro ruxsati bormi: False
```

# 843-Topshiriq: Type.GetInterfaces Bilan Barcha Interfeyslarni Ro'yxatlash
## Topshiriq sharti:
Sinf amalga oshirgan barcha shartnomalarni tekshirish.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;

internal class Program
{
    static void Main()
    {
        Type listTuri = typeof(List<int>);

        Console.WriteLine("List<int> interfeyslari namunasi:");
        foreach (var i in listTuri.GetInterfaces())
        {
            if (i.Name.StartsWith("I"))
            {
                Console.WriteLine($"- {i.Name}");
                break;
            }
        }
    }
}

```

## Tushuntirish va Mantiq:
`GetInterfaces()` sinfning butun meros zanjiridagi barcha interfeyslarni to'liq qidirib beradi.

## Ishlash natijasi:
```text
List<int> interfeyslari namunasi:
- IList`1
```

# 844-Topshiriq: Attributes va Inherited Parametri
## Topshiriq sharti:
Merosxo'r sinf ota sinfning atributini avtomatik meros qilib olishini boshqarish.

## Yechim (C# kodi):
```csharp
using System;

[AttributeUsage(AttributeTargets.Class, Inherited = true)]
class MerosliAttribute : Attribute { }

[Merosli]
class Ota { }

class Bola : Ota { }

internal class Program
{
    static void Main()
    {
        bool mavjud = Attribute.IsDefined(typeof(Bola), typeof(MerosliAttribute), inherit: true);
        Console.WriteLine($"Bola sinfida atribut bormi: {mavjud}");
    }
}

```

## Tushuntirish va Mantiq:
`Inherited = true` atributlar voris sinflarga ham avtomatik ta'sir qilishini ta'minlaydi.

## Ishlash natijasi:
```text
Bola sinfida atribut bormi: True
```

# 845-Topshiriq: MethodInfo.IsStatic va IsVirtual Xususiyatlari
## Topshiriq sharti:
Metodning statik yoki virtual ekanligini metadata orqali aniqlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Reflection;

class Test
{
    public static void S() { }
    public virtual void V() { }
}

internal class Program
{
    static void Main()
    {
        MethodInfo mS = typeof(Test).GetMethod("S")!;
        MethodInfo mV = typeof(Test).GetMethod("V")!;

        Console.WriteLine($"S statikmi: {mS.IsStatic}");
        Console.WriteLine($"V virtualmi: {mV.IsVirtual}");
    }
}

```

## Tushuntirish va Mantiq:
Metod bayroqlari kompyuterga uning polimorfizm jadvali (vtable) orqali chaqirilishini ko'rsatadi.

## Ishlash natijasi:
```text
S statikmi: True
V virtualmi: True
```

# 846-Topshiriq: Assembly.GetEntryAssembly Bilan Dastur Metadatasini Olish
## Topshiriq sharti:
Dasturning asosiy .exe fayli va versiyasini aniqlash.

## Yechim (C# kodi):
```csharp
using System;
using System.Reflection;

internal class Program
{
    static void Main()
    {
        Assembly? entry = Assembly.GetEntryAssembly();
        Console.WriteLine($"Asosiy Assembly nomi: {entry?.GetName().Name}");
        Console.WriteLine($"Versiyasi: {entry?.GetName().Version}");
    }
}

```

## Tushuntirish va Mantiq:
`GetEntryAssembly` jarayonni boshlagan asosiy loyihani ko'rsatadi.

## Ishlash natijasi:
```text
Asosiy Assembly nomi: ...
Versiyasi: 1.0.0.0
```

# 847-Topshiriq: DynamicMethod Bilan Massiv Elementlarini Tezkor O'qish
## Topshiriq sharti:
IL orqali massiv elementiga kiruvchi funksiya qurish.

## Yechim (C# kodi):
```csharp
using System;
using System.Reflection.Emit;

internal class Program
{
    static void Main()
    {
        DynamicMethod dm = new DynamicMethod("Olish", typeof(int), new[] { typeof(int[]), typeof(int) });
        ILGenerator il = dm.GetILGenerator();

        il.Emit(OpCodes.Ldarg_0); // massiv
        il.Emit(OpCodes.Ldarg_1); // indeks
        il.Emit(OpCodes.Ldelem_I4); // massiv[indeks] ni yuklash
        il.Emit(OpCodes.Ret);

        var oquvchi = (Func<int[], int, int>)dm.CreateDelegate(typeof(Func<int[], int, int>));

        int[] sonlar = [10, 20, 30];
        Console.WriteLine($"1-indeksdagi qiymat: {oquvchi(sonlar, 1)}");
    }
}

```

## Tushuntirish va Mantiq:
IL kod yordamida dinamik massiv o'quvchi oddiy kompilyatsiya qilingan C# kodi bilan bir xil mikrosekundlik tezlikda ishlaydi.

## Ishlash natijasi:
```text
1-indeksdagi qiymat: 20
```

# 848-Topshiriq: Custom Attribute Bilan Avtomatik Marshrutlash (Mini Web Router)
## Topshiriq sharti:
Atributlar orqali URL yo'llarini metodlarga bog'lash.

## Yechim (C# kodi):
```csharp
using System;
using System.Collections.Generic;
using System.Reflection;

[AttributeUsage(AttributeTargets.Method)]
class RouteAttribute : Attribute
{
    public string Path { get; }
    public RouteAttribute(string path) => Path = path;
}

class ApiController
{
    [Route("/api/users")]
    public void GetUsers() => Console.WriteLine("[HTTP 200]: Foydalanuvchilar ro'yxati qaytarildi.");
}

internal class Program
{
    static void Main()
    {
        var xarita = new Dictionary<string, MethodInfo>();
        var ctrl = new ApiController();

        foreach (var m in typeof(ApiController).GetMethods())
        {
            var route = m.GetCustomAttribute<RouteAttribute>();
            if (route != null) xarita[route.Path] = m;
        }

        Console.WriteLine("So'rov keldi: /api/users");
        if (xarita.TryGetValue("/api/users", out var handler))
        {
            handler.Invoke(ctrl, null);
        }
    }
}

```

## Tushuntirish va Mantiq:
ASP.NET Core Controllers aynan shu uslubda Reflection orqali marshrutlarni tekshirib, xaritaga yig'adi.

## Ishlash natijasi:
```text
So'rov keldi: /api/users
[HTTP 200]: Foydalanuvchilar ro'yxati qaytarildi.
```

# 849-Topshiriq: Type.IsValueType va IsPrimitive Tekshiruvlari
## Topshiriq sharti:
Sinfning primitiv son yoki murakkab tuzilma ekanligini ajratish.

## Yechim (C# kodi):
```csharp
using System;

internal class Program
{
    static void Main()
    {
        Type tInt = typeof(int);
        Type tString = typeof(string);
        Type tDateTime = typeof(DateTime);

        Console.WriteLine($"int primitivmi: {tInt.IsPrimitive}");
        Console.WriteLine($"string primitivmi: {tString.IsPrimitive}");
        Console.WriteLine($"DateTime ValueTypemi: {tDateTime.IsValueType}");
    }
}

```

## Tushuntirish va Mantiq:
Serializatorlar xususiyatning primitiv yoki ichki obyekt ekanligini ushbu metodlar orqali aniqlaydi.

## Ishlash natijasi:
```text
int primitivmi: True
string primitivmi: False
DateTime ValueTypemi: True
```

# 850-Topshiriq: Reflection Xulosasi: Mini AutoMapper Dvigateli
## Topshiriq sharti:
Bir xil nomli xususiyatlarni bir sinfdan boshqa sinfga avtomatik o'tkazuvchi to'liq xaritalagich.

## Yechim (C# kodi):
```csharp
using System;
using System.Reflection;

class XodimEntity
{
    public int Id { get; set; } = 1;
    public string Ism { get; set; } = "Farrux";
    public string MaxfiyKarta { get; set; } = "8600...";
}

class XodimDto
{
    public int Id { get; set; }
    public string Ism { get; set; } = "";
}

class MiniMapper
{
    public static TDest Map<TSrc, TDest>(TSrc manba) where TDest : new()
    {
        TDest nishon = new TDest();
        Type srcType = typeof(TSrc);
        Type destType = typeof(TDest);

        foreach (PropertyInfo destProp in destType.GetProperties())
        {
            PropertyInfo? srcProp = srcType.GetProperty(destProp.Name);
            if (srcProp != null && srcProp.PropertyType == destProp.PropertyType)
            {
                object? qiymat = srcProp.GetValue(manba);
                destProp.SetValue(nishon, qiymat);
            }
        }

        return nishon;
    }
}

internal class Program
{
    static void Main()
    {
        var entity = new XodimEntity();
        XodimDto dto = MiniMapper.Map<XodimEntity, XodimDto>(entity);

        Console.WriteLine($"DTO Id: {dto.Id}");
        Console.WriteLine($"DTO Ism: {dto.Ism}");
    }
}

```

## Tushuntirish va Mantiq:
MiniMapper Reflection orqali korporativ arxitekturalarda ma'lumotlar bazasi modellari (Entities) va foydalanuvchiga yuboriladigan DTO larni xavfsiz ajratadi.

## Ishlash natijasi:
```text
DTO Id: 1
DTO Ism: Farrux
```

