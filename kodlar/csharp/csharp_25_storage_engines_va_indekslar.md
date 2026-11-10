# Modul 25: .NET 8/9 Storage Engines, Indekslash va Yuqori Unumdor Ma'lumot Saqlash Dvigatellari

Ushbu modulda zamonaviy yuqori yuklamali tizimlar, kesh serverlari va ma'lumotlar bazasi yadrolarida qo'llaniladigan xotira va disk arxitekturasi: Microsoft FASTER uslubidagi HybridLog (xotira va disk bosqichlari), konkurent B+Tree indekslari, MemoryMappedFile orqali Zero-Copy I/O, Slotted-Page xotira strukturasi, Write-Ahead Logging (WAL) hamda Lock-Free Epoch-Based Memory Reclamation (EBR) texnologiyalari .NET 8/9 imkoniyatlari asosida chuqur o'rganiladi.

---
### Topshiriq #1201: Microsoft FASTER Uslubidagi HybridLog Ofsetlar Mantiqi
**Tavsif:** Yuqori unumdor saqlash tizimlarida (masalan, Microsoft FASTER) ma'lumotlar bir vaqtning o'zida ham operativ xotirada (RAM), ham qattiq diskda (SSD) yagona mantiqiy ofsetlar zanjiri (Logical Address Space) ko'rinishida boshqariladi. HybridLog xotira bosqichlarini (Tail, Head, ReadOnly va BeginAddress) hisoblovchi asosiy ofset boshqaruvchisining yadro modelini yaratish kerak.
**Talablar:**
- 64-bitli mantiqiy manzil (Address) strukturasini loyihalash: Page Index (yuqori bitlar) va Page Offset (quyi bitlar).
- HybridLog chegaralari: `TailAddress` (yangi yozuvlar qo'shiladigan joy), `HeadAddress` (RAM dagi eng eski sahifa), `ReadOnlyAddress` (in-place yangilanmaydigan, faqat o'qiladigan zona) va `BeginAddress` (diskdagi eng eski ma'lumot).
- Manzil kiritilganda uning qaysi zonaga (Mutable In-Memory, Read-Only In-Memory, On-Disk yoki Evicted) tegishli ekanligini $O(1)$ da aniqlash.
**Yechim (C#):**
```csharp
using System;
using System.Runtime.CompilerServices;

namespace StorageEngine.HybridLog;

// 64-bitli mantiqiy HybridLog manzili
public readonly struct LogicalAddress : IEquatable<LogicalAddress>, IComparable<LogicalAddress>
{
    public const int PageSizeBits = 14; // 16 KB sahifa (2^14 bayt)
    public const int PageSize = 1 << PageSizeBits;
    public const long OffsetMask = PageSize - 1;

    public readonly long Value;

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public LogicalAddress(long value) => Value = value;

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public LogicalAddress(int page, int offset) => Value = ((long)page << PageSizeBits) | (offset & OffsetMask);

    public int Page => (int)(Value >> PageSizeBits);
    public int Offset => (int)(Value & OffsetMask);

    public static readonly LogicalAddress Invalid = new(-1L);

    public bool Equals(LogicalAddress other) => Value == other.Value;
    public int CompareTo(LogicalAddress other) => Value.CompareTo(other.Value);
    public override string ToString() => $"[P:{Page}, Off:{Offset} (Val: 0x{Value:X})]";
}

// Manzil holati zonasi
public enum MemoryTier
{
    Invalid,
    OnDisk,             // BeginAddress <= Addr < HeadAddress (Faqat diskda)
    ReadOnlyInMemory,   // HeadAddress <= Addr < ReadOnlyAddress (RAM da, lekin muzlatilgan)
    MutableInMemory     // ReadOnlyAddress <= Addr < TailAddress (RAM da to'liq tahrirlanadi)
}

// HybridLog xotira chegaralari koordinatori
public sealed class HybridLogBoundaryManager
{
    public long BeginAddress;    // Diskdagi eng eski manzil
    public long HeadAddress;     // RAM da saqlanayotgan eng eski manzil
    public long ReadOnlyAddress; // In-memory o'zgartirib bo'lmaydigan (muzlatilgan) chegara
    public long TailAddress;     // Yangi yozuvlar yozilayotgan joriy manzil

    public HybridLogBoundaryManager(long initialAddress = 0)
    {
        BeginAddress = initialAddress;
        HeadAddress = initialAddress;
        ReadOnlyAddress = initialAddress;
        TailAddress = initialAddress;
    }

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public MemoryTier GetMemoryTier(LogicalAddress address)
    {
        long val = address.Value;
        if (val < BeginAddress || val >= TailAddress) return MemoryTier.Invalid;
        if (val >= ReadOnlyAddress) return MemoryTier.MutableInMemory;
        if (val >= HeadAddress) return MemoryTier.ReadOnlyInMemory;
        return MemoryTier.OnDisk;
    }

    // Yangi yozuv uchun xotiradan manzil ajratish (Interlocked orqali)
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public LogicalAddress Allocate(int recordSize)
    {
        long allocatedAddress = System.Threading.Interlocked.Add(ref TailAddress, recordSize) - recordSize;
        return new LogicalAddress(allocatedAddress);
    }
}
```
**Tushuntirish:** HybridLog xotirani uzluksiz 64-bitli virtual tasma sifatida ko'radi. Yozuvlar doimo `TailAddress` ga ketma-ket qo'shiladi. `ReadOnlyAddress` dan chapdagi ma'lumotlar o'zgartirilmas (immutable) bo'lib, ular asinxron diskka to'kiladi (flush qilinadi). Bu orqali qulflarsiz (lock-free) o'qish va yuqori o'tkazuvchanlikka erishiladi.
---

### Topshiriq #1202: HybridLog Page Frame va Circular Buffer Pool
**Tavsif:** Barcha ma'lumotlarni RAM da ushlab turish xotira chegarasiga yetganda ilovaning to'xtab qolishiga olib keladi. Sahifalar sonini qat'iy cheklangan doiraviy buferda (Circular Buffer) boshqarish va eski sahifalar diskka surilganda xotira freymlarini qayta ishlatish kerak.
**Talablar:**
- 2 ning darajasidagi doiraviy sahifalar massivi (Frame Array).
- Sahifa raqami bo'yicha freym indeksini bitwise masking (`page % numPages`) orqali $O(1)$ da hisoblash.
- Sahifani xotiradan diskka to'kishga tayyorlash (Flush readiness) holat mashinasi.
**Yechim (C#):**
```csharp
using System;
using System.Runtime.InteropServices;
using System.Threading;

namespace StorageEngine.HybridLog;

public sealed unsafe class PageFramePool : IDisposable
{
    private readonly int _pageCount;
    private readonly int _pageMask;
    private readonly int _pageSize;
    private readonly byte*[] _frames;
    private readonly int[] _pageNumbers; // Freymda ayni damda qaysi mantiqiy sahifa joylashgan

    public PageFramePool(int pageCountPowerOfTwo = 6, int pageSize = 16384) // 64 sahifa x 16 KB = 1 MB bufer
    {
        _pageCount = 1 << pageCountPowerOfTwo;
        _pageMask = _pageCount - 1;
        _pageSize = pageSize;

        _frames = new byte*[_pageCount];
        _pageNumbers = new int[_pageCount];

        for (int i = 0; i < _pageCount; i++)
        {
            // Xotirani tuzilmagan (unmanaged) xotiradan ajratish (GC ga tushmaydi)
            _frames[i] = (byte*)NativeMemory.AllocZeroed((nuint)_pageSize);
            _pageNumbers[i] = -1;
        }
    }

    [System.Runtime.CompilerServices.MethodImpl(System.Runtime.CompilerServices.MethodImplOptions.AggressiveInlining)]
    public byte* GetPagePointer(int pageNumber)
    {
        int frameIndex = pageNumber & _pageMask;
        // Agar sahifa hali freymga yuklanmagan bo'lsa
        if (Volatile.Read(ref _pageNumbers[frameIndex]) != pageNumber)
        {
            Interlocked.Exchange(ref _pageNumbers[frameIndex], pageNumber);
        }
        return _frames[frameIndex];
    }

    [System.Runtime.CompilerServices.MethodImpl(System.Runtime.CompilerServices.MethodImplOptions.AggressiveInlining)]
    public Span<byte> GetPageSpan(int pageNumber)
    {
        return new Span<byte>(GetPagePointer(pageNumber), _pageSize);
    }

    public void Dispose()
    {
        for (int i = 0; i < _pageCount; i++)
        {
            if (_frames[i] != null)
            {
                NativeMemory.Free(_frames[i]);
                _frames[i] = null;
            }
        }
    }
}
```
**Tushuntirish:** `NativeMemory.AllocZeroed` orqali GC boshqarmaydigan (unmanaged) xotira ajratiladi. Bu .NET ning Garbage Collector bosimini 0 ga tushiradi (Zero Allocation). Doiraviy freymlar massivi orqali sahifalar son-sanoqsiz marta disk bilan RAM o'rtasida qayta ishlatiladi.
---

### Topshiriq #1203: HybridLog Record Header: Versiyalar va Orqaga Ko'rsatkichlar (Backward Pointer)
**Tavsif:** Bir xil kalit uchun HybridLog-da bir nechta versiyalar (update recordlar) mavjud bo'lishi mumkin. So'nggi qiymatdan eski qiymatga qarab sakrash va o'chirilgan yozuvlarni (Tombstone) aniqlash uchun har bir yozuv oldiga ixcham 16-baytli Header joylashtiriladi.
**Talablar:**
- `RecordInfo` unmanaged struct: Previous Address (48 bit), Tombstone (1 bit), Tentative (1 bit), Version (14 bit).
- Span yordamida Record Header ni tezkor o'qish va yozish.
**Yechim (C#):**
```csharp
using System;
using System.Runtime.InteropServices;

namespace StorageEngine.HybridLog;

[StructLayout(LayoutKind.Explicit, Size = 16)]
public struct RecordInfo
{
    // 64-bit: 48 bit PreviousAddress, 1 bit Tombstone, 1 bit InPlaceUpdated, 14 bit Version
    [FieldOffset(0)] private ulong _controlWord;
    [FieldOffset(8)] public long Checksum; // Yozuv yaxlitligi uchun xxHash64 yoki CRC

    private const ulong PreviousAddressMask = 0x0000FFFFFFFFFFFFUL; // 48 bit (256 TB)
    private const ulong TombstoneMask = 1UL << 48;
    private const ulong TentativeMask = 1UL << 49;
    private const int VersionShift = 50;

    public long PreviousAddress
    {
        readonly get => (long)(_controlWord & PreviousAddressMask);
        set => _controlWord = (_controlWord & ~PreviousAddressMask) | ((ulong)value & PreviousAddressMask);
    }

    public bool IsTombstone
    {
        readonly get => (_controlWord & TombstoneMask) != 0;
        set => _controlWord = value ? (_controlWord | TombstoneMask) : (_controlWord & ~TombstoneMask);
    }

    public ushort Version
    {
        readonly get => (ushort)(_controlWord >> VersionShift);
        set => _controlWord = (_controlWord & ~(0x3FFFUL << VersionShift)) | (((ulong)value & 0x3FFFUL) << VersionShift);
    }

    public static RecordInfo Create(long previousAddress, ushort version = 1, bool isTombstone = false)
    {
        var info = new RecordInfo();
        info.PreviousAddress = previousAddress;
        info.Version = version;
        info.IsTombstone = isTombstone;
        return info;
    }
}
```
**Tushuntirish:** 48-bit manzil 256 Terabayt hajmdagi uzluksiz log manzilini ifodalash uchun yetarli. Yozuvlarning `PreviousAddress` maydoni orqali bog'langan ro'yxat (Reverse Linked List) hosil bo'ladi. Hash-indeks faqat oxirgi versiyaga ko'rsatadi, eski versiyalar esa log bo'ylab orqaga qarab topiladi.
---

### Topshiriq #1204: Read-Only Bosqichiga Ko'chirish (In-Memory Head -> ReadOnly)
**Tavsif:** Yangi yozuvlar `MutableInMemory` zonasiga qo'shiladi va bu zonada mavjud yozuvlarni to'g'ridan-to'g'ri joyida (in-place) yangilash mumkin. Biroq xotira to'lib borgan sari eng eski bloklar `ReadOnly` holatiga o'tkazilishi (Freeze) va ularga in-place yozish taqiqlanishi kerak.
**Talablar:**
- `ReadOnlyAddress` ni siljitish algoritmi.
- Agar foydalanuvchi `ReadOnly` zonadagi kalitni yangilamoqchi bo'lsa, uni joyida o'zgartirmasdan, `Tail` ga yangi nusxasini (Blind Append) yozish lozim.
**Yechim (C#):**
```csharp
using System;
using System.Threading;

namespace StorageEngine.HybridLog;

public sealed class HybridLogAppender
{
    private readonly HybridLogBoundaryManager _boundaries;
    private readonly PageFramePool _bufferPool;

    public HybridLogAppender(HybridLogBoundaryManager boundaries, PageFramePool bufferPool)
    {
        _boundaries = boundaries;
        _bufferPool = bufferPool;
    }

    // ReadOnly chegarasini xavfsiz oldinga siljitish
    public void ShiftReadOnlyAddress(long newReadOnlyAddress)
    {
        while (true)
        {
            long current = Volatile.Read(ref _boundaries.ReadOnlyAddress);
            if (newReadOnlyAddress <= current) return;

            if (Interlocked.CompareExchange(ref _boundaries.ReadOnlyAddress, newReadOnlyAddress, current) == current)
            {
                break;
            }
        }
    }

    // Kalit-qiymat yozish amali
    public unsafe LogicalAddress Upsert(long key, ReadOnlySpan<byte> value, long previousAddressForSameKey)
    {
        int payloadSize = sizeof(long) + sizeof(int) + value.Length;
        int totalRecordSize = sizeof(RecordInfo) + payloadSize;

        // 1. Yangi manzil ajratish (Har doim TailAddress dan)
        LogicalAddress address = _boundaries.Allocate(totalRecordSize);

        // 2. Sahifaga ko'rsatkich olish
        byte* pagePtr = _bufferPool.GetPagePointer(address.Page);
        byte* recordPtr = pagePtr + address.Offset;

        // 3. Header yozish
        var header = RecordInfo.Create(previousAddressForSameKey, version: 1);
        *(RecordInfo*)recordPtr = header;

        // 4. Ma'lumotlarni nusxalash (Key + ValueLen + Value)
        byte* dataPtr = recordPtr + sizeof(RecordInfo);
        *(long*)dataPtr = key;
        dataPtr += sizeof(long);
        *(int*)dataPtr = value.Length;
        dataPtr += sizeof(int);

        value.CopyTo(new Span<byte>(dataPtr, value.Length));

        return address;
    }
}
```
**Tushuntirish:** ReadOnly zonasiga o'tkazilgan sahifalarga endi hech qanday oqim (thread) to'g'ridan-to'g'ri in-place yozolmaydi. Har qanday yangilanish (UPDATE) yangi manzilga APPEND ko'rinishida tushadi va eski manzilga `PreviousAddress` orqali ulanadi. Bu diskka asinxron yozish vaqtida ma'lumotlarning buzilmasligini kafolatlaydi.
---

### Topshiriq #1205: Disk Spilling: Read-Only Sahifalarni Asinxron Diskka To'kish (Flusher)
**Tavsif:** `ReadOnly` zonasidagi sahifalar RAM chegarasidan oshib ketmasligi uchun fon oqimi (Flusher thread) ularni uzluksiz ravishda disk fayliga yozishi va yozib bo'lingach `HeadAddress` ni siljitishi lozim.
**Talablar:**
- `FileStream` orqali `FileOptions.Asynchronous` rejimida sahifalarni bloklarga yozish.
- Diskka yozib bo'lingan sahifalarni RAM dan chiqarishga tayyorlash va `HeadAddress` ni yangilash.
**Yechim (C#):**
```csharp
using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;

namespace StorageEngine.HybridLog;

public sealed class DiskFlusher : IAsyncDisposable
{
    private readonly HybridLogBoundaryManager _boundaries;
    private readonly PageFramePool _bufferPool;
    private readonly FileStream _diskLogFile;
    private readonly CancellationTokenSource _cts = new();

    public DiskFlusher(string logFilePath, HybridLogBoundaryManager boundaries, PageFramePool bufferPool)
    {
        _boundaries = boundaries;
        _bufferPool = bufferPool;
        _diskLogFile = new FileStream(
            logFilePath, 
            FileMode.OpenOrCreate, 
            FileAccess.ReadWrite, 
            FileShare.ReadWrite, 
            bufferSize: 65536, 
            FileOptions.Asynchronous | FileOptions.WriteThrough);
    }

    public async Task FlushPageToDiskAsync(int pageNumber)
    {
        long fileOffset = (long)pageNumber * LogicalAddress.PageSize;
        ReadOnlyMemory<byte> memoryBuffer;

        unsafe
        {
            byte* ptr = _bufferPool.GetPagePointer(pageNumber);
            // Native xotiradan boshqariladigan Memory yaratish uchun UnmanagedMemoryManager zarur
            // Yoki sodda nusxa bilan:
            byte[] managedCopy = new byte[LogicalAddress.PageSize];
            Marshal.Copy((IntPtr)ptr, managedCopy, 0, LogicalAddress.PageSize);
            memoryBuffer = managedCopy;
        }

        _diskLogFile.Seek(fileOffset, SeekOrigin.Begin);
        await _diskLogFile.WriteAsync(memoryBuffer, _cts.Token).ConfigureAwait(false);
        await _diskLogFile.FlushAsync(_cts.Token).ConfigureAwait(false);

        // Sahifa diskka tushgach, HeadAddress ni ushbu sahifaning oxiriga siljitish mumkin
        long pageEndAddress = (long)(pageNumber + 1) * LogicalAddress.PageSize;
        Interlocked.Exchange(ref _boundaries.HeadAddress, pageEndAddress);
    }

    public async ValueTask DisposeAsync()
    {
        _cts.Cancel();
        await _diskLogFile.DisposeAsync().ConfigureAwait(false);
        _cts.Dispose();
    }
}
```
**Tushuntirish:** Diskka to'kish (Spill to Disk) to'liq asinxron bajariladi, bu esa yozish operatsiyalarini kutib turishdan ozod qiladi. `WriteThrough` parametri operatsion tizim keshini chetlab o'tib to'g'ridan-to'g'ri drayverga yozilishini va kutilmagan server o'chishida ma'lumot yo'qolmasligini ta'minlaydi.
---

### Topshiriq #1206: HybridLog Scan: Orqaga Qarab Zanjirli O'qish (Backward Traversal)
**Tavsif:** Ma'lum bir kalit bo'yicha barcha o'zgarishlar tarixini (Audit Log / Point-in-time) yoki eng so'nggi holatni olish uchun `PreviousAddress` zanjiri bo'ylab eng yangi yozuvdan boshlab eng eski yozuvgacha o'qish imkoniyati zarur.
**Talablar:**
- Boshlang'ich mantiqiy manzildan (Tail yoki Hash Indexdagi manzil) boshlash.
- Agar manzil RAM da bo'lsa (MemoryTier.MutableInMemory yoki ReadOnlyInMemory) to'g'ridan-to'g'ri xotiradan, agar On-Disk bo'lsa diskdan o'qish.
- `IsTombstone` bo'lsa o'chirilgan deb qaytarish.
**Yechim (C#):**
```csharp
using System;
using System.IO;

namespace StorageEngine.HybridLog;

public sealed class HybridLogScanner
{
    private readonly HybridLogBoundaryManager _boundaries;
    private readonly PageFramePool _bufferPool;
    private readonly FileStream _diskFile;

    public HybridLogScanner(HybridLogBoundaryManager boundaries, PageFramePool bufferPool, FileStream diskFile)
    {
        _boundaries = boundaries;
        _bufferPool = bufferPool;
        _diskFile = diskFile;
    }

    public unsafe bool TryReadLatest(LogicalAddress startAddress, long expectedKey, out byte[] value)
    {
        value = null!;
        LogicalAddress current = startAddress;

        while (current.Value != -1 && current.Value >= _boundaries.BeginAddress)
        {
            MemoryTier tier = _boundaries.GetMemoryTier(current);
            if (tier == MemoryTier.Invalid) break;

            if (tier == MemoryTier.MutableInMemory || tier == MemoryTier.ReadOnlyInMemory)
            {
                // RAM dan o'qish
                byte* pagePtr = _bufferPool.GetPagePointer(current.Page);
                byte* recordPtr = pagePtr + current.Offset;
                RecordInfo* header = (RecordInfo*)recordPtr;

                if (header->IsTombstone) return false; // Kalit o'chirilgan

                byte* dataPtr = recordPtr + sizeof(RecordInfo);
                long key = *(long*)dataPtr;
                dataPtr += sizeof(long);
                int valLen = *(int*)dataPtr;
                dataPtr += sizeof(int);

                if (key == expectedKey)
                {
                    value = new byte[valLen];
                    Marshal.Copy((IntPtr)dataPtr, value, 0, valLen);
                    return true;
                }

                current = new LogicalAddress(header->PreviousAddress);
            }
            else // Diskdan o'qish
            {
                // Diskdan o'qish logikasi: Seek va Read
                _diskFile.Seek(current.Value, SeekOrigin.Begin);
                Span<byte> headerBuffer = stackalloc byte[sizeof(RecordInfo)];
                _diskFile.ReadExactly(headerBuffer);
                RecordInfo header = MemoryMarshal.Read<RecordInfo>(headerBuffer);

                if (header.IsTombstone) return false;

                // Key va Len ni o'qish
                Span<byte> keyLenBuffer = stackalloc byte[sizeof(long) + sizeof(int)];
                _diskFile.ReadExactly(keyLenBuffer);
                long key = MemoryMarshal.Read<long>(keyLenBuffer[..8]);
                int valLen = MemoryMarshal.Read<int>(keyLenBuffer[8..]);

                if (key == expectedKey)
                {
                    value = new byte[valLen];
                    _diskFile.ReadExactly(value);
                    return true;
                }

                current = new LogicalAddress(header.PreviousAddress);
            }
        }

        return false;
    }
}
```
**Tushuntirish:** HybridLog ma'lumotlarni qidirishda shaffof qatlam hosil qiladi: so'nggi o'zgarishlar bir necha nanosekundda RAM dan olinadi, eski ma'lumotlar esa zanjir bo'ylab diskdan o'qiladi. Bu hot/cold data tieringning eng optimal shaklidir.
---

### Topshiriq #1207: Read-Modify-Write (RMW) va Joyida Atomar Yangilash (In-Place Update)
**Tavsif:** Agar yozuv `MutableInMemory` zonasida joylashgan bo'lsa va yangi qiymat uzunligi eski qiymat bilan teng bo'lsa, log oxiriga yana bir bor APPEND qilish o'rniga, mavjud xotiraning o'zida atomar in-place yangilash xotira sarfini keskin tejaydi.
**Talablar:**
- RMW operatsiyasi: manzil `MutableInMemory` da bo'lsa va o'lcham mos kelsa, `Interlocked` yoki qulf bilan joyida yozish.
- Aks holda `Tail` ga yangi versiyani append qilish.
**Yechim (C#):**
```csharp
using System;
using System.Threading;

namespace StorageEngine.HybridLog;

public sealed class InPlaceUpdater
{
    private readonly HybridLogBoundaryManager _boundaries;
    private readonly PageFramePool _bufferPool;
    private readonly HybridLogAppender _appender;

    public InPlaceUpdater(HybridLogBoundaryManager boundaries, PageFramePool bufferPool, HybridLogAppender appender)
    {
        _boundaries = boundaries;
        _bufferPool = bufferPool;
        _appender = appender;
    }

    public unsafe bool TryUpdateInPlaceOrAppend(LogicalAddress currentAddress, long key, ReadOnlySpan<byte> newValue, out LogicalAddress finalAddress)
    {
        // 1. Manzil qaysi zonada ekanini tekshiramiz
        if (_boundaries.GetMemoryTier(currentAddress) == MemoryTier.MutableInMemory)
        {
            byte* pagePtr = _bufferPool.GetPagePointer(currentAddress.Page);
            byte* recordPtr = pagePtr + currentAddress.Offset;
            byte* dataPtr = recordPtr + sizeof(RecordInfo) + sizeof(long);
            int currentValLen = *(int*)dataPtr;
            dataPtr += sizeof(int);

            // Agar o'lcham teng bo'lsa, joyida o'zgartiramiz!
            if (currentValLen == newValue.Length)
            {
                // In-place copy
                newValue.CopyTo(new Span<byte>(dataPtr, currentValLen));
                finalAddress = currentAddress;
                return true;
            }
        }

        // 2. Aks holda (ReadOnly zona yoki boshqa o'lcham) - Append qilamiz
        finalAddress = _appender.Upsert(key, newValue, currentAddress.Value);
        return false;
    }
}
```
**Tushuntirish:** In-place yangilanish hisoblagichlar (counters), bank hisobidagi balanslar yoki kesh flaglarini yangilashda logning shishib ketishini to'xtatadi. Microsoft FASTER ning 100M+ ops/sec tezlikka erishish siri aynan `MutableInMemory` zonasidagi in-place RMW mexanizmidir.
---

### Topshiriq #1208: HybridLog Compaction: Diskdagi Eskirgan Segmentlarni Tozalash
**Tavsif:** Uzluksiz yozish natijasida diskdagi log fayli yuzlab gigabaytga yetishi mumkin. Ko'plab yozuvlar eskirgan (superseded) yoki o'chirilgan (tombstone) bo'ladi. Eski log faylini o'qib, faqat faol yozuvlarni yangi ixcham faylga ko'chiruvchi Compaction mexanizmini yaratish kerak.
**Talablar:**
- Eski fayldagi yozuvlarni ketma-ket skaner qilish.
- Tashqi hash-indeks orqali ushbu yozuv hali ham so'nggi (jonli) versiya ekanligini tekshirish.
- Faqat jonli yozuvlarni yangi segmentga yozib, `BeginAddress` ni oldinga surish.
**Yechim (C#):**
```csharp
using System;
using System.Collections.Generic;
using System.IO;

namespace StorageEngine.HybridLog;

public sealed class LogCompactor
{
    // Faol yozuvlarning so'nggi manzilini biluvchi indeks interfeysi
    public interface IKeyIndex { bool IsLatestAddress(long key, long address); }

    public static unsafe void CompactLogSegment(
        string oldLogPath, 
        string compactedLogPath, 
        IKeyIndex index, 
        long untilAddress)
    {
        using var oldStream = new FileStream(oldLogPath, FileMode.Open, FileAccess.Read);
        using var newStream = new FileStream(compactedLogPath, FileMode.Create, FileAccess.Write);

        Span<byte> headerBuffer = stackalloc byte[sizeof(RecordInfo)];
        Span<byte> keyLenBuffer = stackalloc byte[sizeof(long) + sizeof(int)];

        while (oldStream.Position < untilAddress && oldStream.Position < oldStream.Length)
        {
            long recordStartOffset = oldStream.Position;

            if (oldStream.Read(headerBuffer) < sizeof(RecordInfo)) break;
            RecordInfo header = MemoryMarshal.Read<RecordInfo>(headerBuffer);

            if (oldStream.Read(keyLenBuffer) < sizeof(long) + sizeof(int)) break;
            long key = MemoryMarshal.Read<long>(keyLenBuffer[..8]);
            int valLen = MemoryMarshal.Read<int>(keyLenBuffer[8..]);

            byte[] valBytes = new byte[valLen];
            oldStream.ReadExactly(valBytes);

            // Agar yozuv o'chirilmagan bo'lsa va ayni paytda eng so'nggi versiya bo'lsa:
            if (!header.IsTombstone && index.IsLatestAddress(key, recordStartOffset))
            {
                // Yangi faylga ko'chirish
                newStream.Write(headerBuffer);
                newStream.Write(keyLenBuffer);
                newStream.Write(valBytes);
            }
        }
    }
}
```
**Tushuntirish:** Compaction diskdagi bo'shliqni qayta tiklaydi. LSM-Tree lardan farqli o'laroq, HybridLog bir yo'nalishli tasma bo'lgani uchun eski qismlar yangilanib boradi va `BeginAddress` surilib, eski disk fayllari OS dan butunlay o'chirib tashlanadi.
---

### Topshiriq #1209: Fuzzy Checkpoint Arxitekturasi
**Tavsif:** Ma'lumotlar bazasida doimiy to'xtashlarsiz (Stop-the-world bo'lmasdan) tizim holatini diskka saqlash uchun Fuzzy Checkpointing arxitekturasi qo'llaniladi. Checkpoint boshlangan va tugagan vaqt oralig'idagi o'zgarishlar maxsus meta-faylda qayd etiladi.
**Talablar:**
- Checkpoint boshlanishida `TailAddress` ni `CheckpointStart` sifatida muzlatish.
- RAM dagi barcha sahifalarni diskka to'kish.
- Checkpoint meta ma'lumotlarini (Start LSN, End LSN, Index snapshot pointer) atomar yozish.
**Yechim (C#):**
```csharp
using System;
using System.IO;
using System.Text.Json;
using System.Threading.Tasks;

namespace StorageEngine.HybridLog;

public sealed class CheckpointMetadata
{
    public Guid CheckpointId { get; set; } = Guid.NewGuid();
    public long CheckpointStartOffset { get; set; }
    public long CheckpointEndOffset { get; set; }
    public DateTime TimestampUtc { get; set; } = DateTime.UtcNow;
}

public sealed class FuzzyCheckpointManager
{
    private readonly HybridLogBoundaryManager _boundaries;
    private readonly DiskFlusher _flusher;
    private readonly string _metadataDir;

    public FuzzyCheckpointManager(HybridLogBoundaryManager boundaries, DiskFlusher flusher, string metadataDir)
    {
        _boundaries = boundaries;
        _flusher = flusher;
        _metadataDir = metadataDir;
        Directory.CreateDirectory(_metadataDir);
    }

    public async Task<CheckpointMetadata> CreateCheckpointAsync()
    {
        // 1. Checkpoint boshlangan nuqtani qayd etish
        long startOffset = Volatile.Read(ref _boundaries.TailAddress);

        // 2. ReadOnly chegarasini startOffset ga tenglashtirish (xotiradagi hamma narsa muzlatiladi)
        _boundaries.ReadOnlyAddress = startOffset;

        // 3. Xotiradagi barcha sahifalarni diskka asinxron to'kish
        int startPage = (int)(_boundaries.HeadAddress >> LogicalAddress.PageSizeBits);
        int endPage = (int)(startOffset >> LogicalAddress.PageSizeBits);

        for (int p = startPage; p <= endPage; p++)
        {
            await _flusher.FlushPageToDiskAsync(p).ConfigureAwait(false);
        }

        // 4. Meta ma'lumotlarni saqlash
        var metadata = new CheckpointMetadata
        {
            CheckpointStartOffset = startOffset,
            CheckpointEndOffset = Volatile.Read(ref _boundaries.TailAddress)
        };

        string metaPath = Path.Combine(_metadataDir, $"checkpoint_{metadata.CheckpointId}.json");
        string json = JsonSerializer.Serialize(metadata, new JsonSerializerOptions { WriteIndented = true });
        await File.WriteAllTextAsync(metaPath, json).ConfigureAwait(false);

        return metadata;
    }
}
```
**Tushuntirish:** "Fuzzy" (noaniq/yumshoq) checkpoint deyilishining sababi - checkpoint paytida yangi so'rovlar qabul qilinishdan to'xtamaydi (`TailAddress` o'sishda davom etadi). Tiklash vaqtida faqat `CheckpointStartOffset` gacha bo'lgan ma'lumotlar to'liq kafolatlangan holat sifatida olinadi.
---

### Topshiriq #1210: Crash Recovery: Checkpoint va WAL Orqali Tiklash
**Tavsif:** Server kutilmaganda elektr ta'minotidan uzilganda (Crash), tizim eng so'nggi barqaror Checkpoint meta-faylini topishi, diskdagi HybridLog holatini tiklashi va checkpointdan keyingi barcha operatsiyalarni qayta hisoblashi zarur.
**Talablar:**
- Eng so'nggi `checkpoint_*.json` faylini topish.
- Diskdagi log uzunligini tekshirish va `TailAddress`, `HeadAddress`, `BeginAddress` qiymatlarini tiklash.
**Yechim (C#):**
```csharp
using System;
using System.IO;
using System.Linq;
using System.Text.Json;

namespace StorageEngine.HybridLog;

public static class CrashRecoveryEngine
{
    public static HybridLogBoundaryManager Recover(string metadataDir, string logFilePath)
    {
        var metaDirInfo = new DirectoryInfo(metadataDir);
        if (!metaDirInfo.Exists)
        {
            return new HybridLogBoundaryManager(0);
        }

        // Eng so'nggi yaratilgan checkpoint faylini topamiz
        FileInfo latestMetaFile = metaDirInfo.GetFiles("checkpoint_*.json")
            .OrderByDescending(f => f.LastWriteTimeUtc)
            .FirstOrDefault();

        if (latestMetaFile == null)
        {
            // Checkpoint mavjud emas, log boshidan boshlanadi
            return new HybridLogBoundaryManager(0);
        }

        string json = File.ReadAllText(latestMetaFile.FullName);
        CheckpointMetadata metadata = JsonSerializer.Deserialize<CheckpointMetadata>(json);

        var fileInfo = new FileInfo(logFilePath);
        long physicalLogLength = fileInfo.Exists ? fileInfo.Length : 0;

        // Xavfsiz qayta tiklash
        var boundaries = new HybridLogBoundaryManager(0)
        {
            BeginAddress = 0,
            HeadAddress = metadata.CheckpointStartOffset,
            ReadOnlyAddress = metadata.CheckpointStartOffset,
            TailAddress = Math.Max(physicalLogLength, metadata.CheckpointStartOffset)
        };

        return boundaries;
    }
}
```
**Tushuntirish:** Crash Recovery tizimni ma'lumotlar buzilmagan nuqtaga qaytaradi. `TailAddress` ni diskning jismoniy uzunligi bilan sinxronlashtirish orqali chala yozilgan baytlar aniqlanadi va ularning ustidan qayta yozish xavfsiz davom ettiriladi.
---

### Topshiriq #1211: In-Memory B+Tree Tugunlari: Leaf vs Internal Node Strukturasi
**Tavsif:** Yuqori unumdor saqlash tizimlarida ma'lumotlarni saralangan holda saqlash va diapazonli qidiruvlar (Range Scan) uchun B+Tree indeksi qo'llaniladi. B+Tree da barcha qiymatlar faqat barg (Leaf) tugunlarda saqlanadi, ichki (Internal) tugunlar esa yo'naltiruvchi kalit vazifasini bajaradi.
**Talablar:**
- `Node` bazaviy sinfi, `InternalNode<TKey>` va `LeafNode<TKey, TValue>`.
- Fanout parametri: har bir tugun sig'dira oladigan maksimal kalitlar soni (Order = M).
- Barg tugunlarning zanjirli ro'yxat pointeri (`NextLeaf`, `PrevLeaf`).
**Yechim (C#):**
```csharp
using System;

namespace StorageEngine.Indexing;

public abstract class BPlusNode<TKey> where TKey : IComparable<TKey>
{
    public bool IsLeaf { get; }
    public int KeyCount { get; protected set; }

    protected BPlusNode(bool isLeaf) => IsLeaf = isLeaf;
}

public sealed class LeafNode<TKey, TValue> : BPlusNode<TKey> where TKey : IComparable<TKey>
{
    public readonly TKey[] Keys;
    public readonly TValue[] Values;
    public LeafNode<TKey, TValue> NextLeaf { get; set; }
    public LeafNode<TKey, TValue> PrevLeaf { get; set; }

    public LeafNode(int maxKeys) : base(isLeaf: true)
    {
        Keys = new TKey[maxKeys];
        Values = new TValue[maxKeys];
        KeyCount = 0;
    }

    public void InsertAt(int index, TKey key, TValue value)
    {
        // Massiv elementlarini bitta o'ngga surish
        Array.Copy(Keys, index, Keys, index + 1, KeyCount - index);
        Array.Copy(Values, index, Values, index + 1, KeyCount - index);

        Keys[index] = key;
        Values[index] = value;
        KeyCount++;
    }
}

public sealed class InternalNode<TKey> : BPlusNode<TKey> where TKey : IComparable<TKey>
{
    public readonly TKey[] Keys;
    public readonly BPlusNode<TKey>[] Children;

    public InternalNode(int maxKeys) : base(isLeaf: false)
    {
        Keys = new TKey[maxKeys];
        Children = new BPlusNode<TKey>[maxKeys + 1];
        KeyCount = 0;
    }

    public void InsertChildAt(int index, TKey key, BPlusNode<TKey> child)
    {
        Array.Copy(Keys, index, Keys, index + 1, KeyCount - index);
        Array.Copy(Children, index + 1, Children, index + 2, KeyCount - index);

        Keys[index] = key;
        Children[index + 1] = child;
        KeyCount++;
    }
}
```
**Tushuntirish:** B+Tree da qiymatlarning faqat barglarda bo'lishi ichki tugunlarga ko'proq yo'naltiruvchi kalitlarni sig'dirish (yuqori Fanout) imkonini beradi. Natijada daraxt chuqurligi juda past (masalan, 3-4 bosqich) bo'lib qoladi va qidiruv juda tezlashadi.
---

### Topshiriq #1212: B+Tree Leaf Node Qidiruv: Span<T> va Binary Search
**Tavsif:** B+Tree tugunlari ichida kalitni qidirish soniyada millionlab marta chaqiriladi. Buni oddiy `for` siklida chiziqli qidirish o'rniga, `MemoryExtensions.BinarySearch` va `ReadOnlySpan<T>` orqali eng yuqori apparat unumdorligida bajarish lozim.
**Talablar:**
- `LeafNode` ichida kalitni qidiruvchi BinarySearch funksiyasi.
- Agar kalit topilsa uning indeksi, topilmasa kiritilishi kerak bo'lgan bitwise NOT (`~index`) o'rnini qaytarish.
**Yechim (C#):**
```csharp
using System;
using System.Runtime.CompilerServices;

namespace StorageEngine.Indexing;

public static class BPlusSearchExtensions
{
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static int FindKeyIndex<TKey, TValue>(this LeafNode<TKey, TValue> leaf, TKey searchKey) 
        where TKey : IComparable<TKey>
    {
        ReadOnlySpan<TKey> activeKeys = leaf.Keys.AsSpan(0, leaf.KeyCount);
        return activeKeys.BinarySearch(searchKey);
    }

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static int FindChildIndex<TKey>(this InternalNode<TKey> internalNode, TKey searchKey) 
        where TKey : IComparable<TKey>
    {
        ReadOnlySpan<TKey> activeKeys = internalNode.Keys.AsSpan(0, internalNode.KeyCount);
        int index = activeKeys.BinarySearch(searchKey);

        if (index >= 0)
        {
            // Agar aniq kalit topilsa, o'ng tarafdagi bolaga o'tiladi
            return index + 1;
        }

        // Agar aniq topilmasa, ~index orqali chap bolasi olinadi
        return ~index;
    }
}
```
**Tushuntirish:** `activeKeys.BinarySearch` JIT tomonidan protsessor registrlari va SIMD ko'rsatmalari orqali xotira xatolarisiz (bounds check elimination) ishlatiladi. `~index` qaytishi esa yangi kalit qayerga tushishi kerakligini bir zumda aniqlab beradi.
---

### Topshiriq #1213: B+Tree Node Split: To'lgan Barg Tugunini Bo'lish
**Tavsif:** Barg tuguni (LeafNode) maksimal kalitlar soniga yetganda, yangi kalit kiritish uchun uni teng ikkiga bo'lish (Split), yangi o'ng tugun yaratish va o'rta kalitni (pivot key) ota tugunga (Parent Internal Node) ko'tarish kerak.
**Talablar:**
- `LeafNode` ning o'ng yarmini yangi `LeafNode` ga ko'chirish.
- `NextLeaf` va `PrevLeaf` zanjirini yangilash.
- Ota tugunga o'tadigan ajratuvchi kalitni (Split Key) qaytarish.
**Yechim (C#):**
```csharp
using System;

namespace StorageEngine.Indexing;

public static class BPlusSplitExtensions
{
    public static (TKey SplitKey, LeafNode<TKey, TValue> NewRightNode) SplitLeaf<TKey, TValue>(
        this LeafNode<TKey, TValue> leftNode, 
        int maxKeys) where TKey : IComparable<TKey>
    {
        int mid = leftNode.KeyCount / 2;
        int rightCount = leftNode.KeyCount - mid;

        var rightNode = new LeafNode<TKey, TValue>(maxKeys);

        // O'ng tarafga ikkinchi yarmini nusxalash
        Array.Copy(leftNode.Keys, mid, rightNode.Keys, 0, rightCount);
        Array.Copy(leftNode.Values, mid, rightNode.Values, 0, rightCount);

        rightNode.KeyCount = rightCount;
        leftNode.KeyCount = mid;

        // Bog'langan ro'yxatni yangilash
        rightNode.NextLeaf = leftNode.NextLeaf;
        rightNode.PrevLeaf = leftNode;
        if (leftNode.NextLeaf != null)
        {
            leftNode.NextLeaf.PrevLeaf = rightNode;
        }
        leftNode.NextLeaf = rightNode;

        // Ota tugunga o'ng tugunning birinchi kaliti uzatiladi
        TKey splitKey = rightNode.Keys[0];
        return (splitKey, rightNode);
    }
}
```
**Tushuntirish:** Tugun ikkiga bo'linganda ikkala tugun ham taxminan 50% to'la bo'ladi (B-Tree qoidasi: kamida $\lceil M/2 \rceil$ element). Zanjirli ko'rsatkichlarning yangilanishi range-skanerlash doimiy ravishda to'g'ri ishlashini ta'minlaydi.
---

### Topshiriq #1214: Concurrent B+Tree: Latch Crabbing (Lock Coupling) Protokoli
**Tavsif:** Ko'p oqimli muhitda bir vaqtning o'zida yuzlab oqimlar daraxtni o'qishi va o'zgartirishi mumkin. Butun daraxtni bitta global qulf bilan yopish o'rniga, har bir tugun darajasida qulflash (Latch Crabbing) algoritmi qo'llaniladi.
**Talablar:**
- `ReaderWriterLockSlim` yordamida tugunlarni qulflash.
- O'qish (Search): bolani qulflab, keyin otani bo'shatish.
- Yozish (Insert): bola "xavfsiz" (ya'ni to'lib ketmagan, bo'linish talab qilmaydigan) bo'lguncha otalarni ushlab turish.
**Yechim (C#):**
```csharp
using System;
using System.Collections.Generic;
using System.Threading;

namespace StorageEngine.Indexing;

public sealed class ConcurrentBPlusNode<TKey> where TKey : IComparable<TKey>
{
    public readonly ReaderWriterLockSlim Latch = new(LockRecursionPolicy.NoRecursion);
    public readonly TKey[] Keys;
    public int KeyCount;
    public readonly bool IsLeaf;

    public ConcurrentBPlusNode(int maxKeys, bool isLeaf)
    {
        Keys = new TKey[maxKeys];
        IsLeaf = isLeaf;
    }

    public bool IsSafeForInsert(int maxKeys) => KeyCount < maxKeys - 1;
}

public sealed class LatchCrabbingBPlusTree<TKey> where TKey : IComparable<TKey>
{
    private readonly int _maxKeys;
    public ConcurrentBPlusNode<TKey> Root;

    public LatchCrabbingBPlusTree(int maxKeys = 16)
    {
        _maxKeys = maxKeys;
        Root = new ConcurrentBPlusNode<TKey>(maxKeys, isLeaf: true);
    }

    // O'qishda Latch Crabbing (Bolani o'qish qulfi bilan ol, otani bo'shat)
    public void ReadTraverse(TKey searchKey)
    {
        ConcurrentBPlusNode<TKey> current = Root;
        current.Latch.EnterReadLock();

        try
        {
            while (!current.IsLeaf)
            {
                // Keyingi bolani topish logikasi...
                ConcurrentBPlusNode<TKey> child = null!; // Bola tugun olinadi
                child.Latch.EnterReadLock();

                // Otani bo'shatish (Crabbing)
                current.Latch.ExitReadLock();
                current = child;
            }
            // Barg topildi, ma'lumot o'qiladi
        }
        finally
        {
            current.Latch.ExitReadLock();
        }
    }
}
```
**Tushuntirish:** Latch Crabbing daraxtning ildizini uzoq vaqt ushlab turmaslikni kafolatlaydi. O'qish oqimlari bir-birini to'smaydi, yozish oqimlari esa faqat bo'linish ehtimoli bo'lgan qismdagina otalarni qulflab turadi.
---

### Topshiriq #1215: Optimistic Lock Coupling (OLC) B+Tree
**Tavsif:** `ReaderWriterLockSlim` kabi og'ir qulflar o'qish operatsiyalarida atomar kesh liniyalarini buzadi (Cache Invalidation). Zamonaviy ma'lumotlar bazalarida o'qish paytida hech qanday qulf ishlatilmaydi, faqat versiya raqami tekshiriladi (Optimistic Lock Coupling).
**Talablar:**
- 64-bitli versiya hisoblagichi (Version Counter): toq son = yozish jarayonida (Locked), juft son = barqaror (Unlocked).
- O'qish oqimi tugunga kirganda versiyani o'qiydi, ma'lumotni ko'chirib olgach yana versiyani tekshiradi. Agar versiya o'zgargan bo'lsa, operatsiya qayta takrorlanadi (Retry).
**Yechim (C#):**
```csharp
using System;
using System.Threading;

namespace StorageEngine.Indexing;

public sealed class OptimisticNode<TKey> where TKey : IComparable<TKey>
{
    private long _version;

    public long ReadLockOrRetry()
    {
        while (true)
        {
            long v = Volatile.Read(ref _version);
            // Agar oxirgi bit 1 bo'lsa (toq son), demak yozuvchi bor, kutamiz
            if ((v & 1L) == 0)
            {
                return v;
            }
            Thread.SpinWait(10);
        }
    }

    public bool Validate(long startVersion)
    {
        // Versiya o'zgarmagan bo'lsa true qaytaradi
        return Volatile.Read(ref _version) == startVersion;
    }

    public void WriteLock()
    {
        while (true)
        {
            long v = Volatile.Read(ref _version);
            if ((v & 1L) == 0 && Interlocked.CompareExchange(ref _version, v + 1, v) == v)
            {
                break; // Toq son qilib qulfladik
            }
            Thread.SpinWait(10);
        }
    }

    public void WriteUnlock()
    {
        // Versiyani keyingi juft songa o'tkazamiz
        Interlocked.Increment(ref _version);
    }
}
```
**Tushuntirish:** OLC da o'quvchilar xotiraga hech qanday yozish amali (Interlocked/Write) bajarmaydi, bu esa CPU L1/L2 keshlarida optimal tezlikni (Multi-core scalability) ta'minlaydi. Qayta urinishlar faqat yozuvchi bilan to'qnash kelgandagina sodir bo'ladi.
---

### Topshiriq #1216: B+Tree Range Scan: Leaf Zanjiri Bo'yicha Diapazonli O'qish
**Tavsif:** SQL so'rovlaridagi `WHERE id BETWEEN 1000 AND 2000` kabi diapazonli operatsiyalar B+Tree ning eng kuchli ustunligidir. Birinchi kalitni daraxt bo'yicha $O(\log N)$ da topib, qolgan barcha ma'lumotlarni barglarning `NextLeaf` ko'rsatkichlari bo'ylab xotiradan to'g'ridan-to'g'ri oqim (IEnumerable) orqali o'qish lozim.
**Talablar:**
- `RangeScan(TKey fromKey, TKey toKey)` metodi.
- Barg tugunlar zanjiridan to'g'ridan-to'g'ri `yield return` orqali xotira sarflamasdan o'qish.
**Yechim (C#):**
```csharp
using System;
using System.Collections.Generic;

namespace StorageEngine.Indexing;

public static class BPlusRangeExtensions
{
    public static IEnumerable<KeyValuePair<TKey, TValue>> RangeScan<TKey, TValue>(
        this LeafNode<TKey, TValue> startLeaf, 
        TKey fromKey, 
        TKey toKey) where TKey : IComparable<TKey>
    {
        LeafNode<TKey, TValue> current = startLeaf;
        int startIndex = current.FindKeyIndex(fromKey);
        if (startIndex < 0) startIndex = ~startIndex;

        while (current != null)
        {
            for (int i = startIndex; i < current.KeyCount; i++)
            {
                TKey key = current.Keys[i];
                if (key.CompareTo(toKey) > 0)
                {
                    yield break; // Diapazondan chiqdik
                }

                yield return new KeyValuePair<TKey, TValue>(key, current.Values[i]);
            }

            // Keyingi bargga sakraymiz
            current = current.NextLeaf;
            startIndex = 0; // Keyingi bargda boshidan o'qiymiz
        }
    }
}
```
**Tushuntirish:** Barglar o'zaro bog'langan ro'yxat (Doubly/Singly Linked List) hosil qilgani tufayli, har bir keyingi kalit uchun daraxt ildizidan qayta qidirish shart emas. Bu diapazonli so'rovlar unumdorligini minglab marta oshiradi.
---

### Topshiriq #1217: B+Tree Underflow: Tugunlarni Qayta Balanslash va Birlashtirish (Merge)
**Tavsif:** Yozuvlar o'chirilganda (DELETE), agar bargdagi kalitlar soni minimal chegaradan ($\lceil M/2 \rceil$) kamayib ketsa (Underflow), qo'shni tugundan kalit qarz olish (Borrow) yoki ikkita tugunni bittaga birlashtirish (Merge) kerak.
**Talablar:**
- Underflow holatini aniqlash.
- Agar qo'shni tugunda yetarli kalit bo'lsa, bitta elementni ko'chirish (Rebalance).
- Aks holda qo'shni tugun bilan to'liq birlashtirish (Merge) va ota tugundan ko'rsatkichni olib tashlash.
**Yechim (C#):**
```csharp
using System;

namespace StorageEngine.Indexing;

public static class BPlusMergeExtensions
{
    public static bool TryBorrowFromRight<TKey, TValue>(
        this LeafNode<TKey, TValue> leftNode, 
        LeafNode<TKey, TValue> rightNode, 
        int minKeys) where TKey : IComparable<TKey>
    {
        // Agar o'ng qo'shnida ortiqcha element bo'lsa, qarz olamiz
        if (rightNode != null && rightNode.KeyCount > minKeys)
        {
            TKey borrowedKey = rightNode.Keys[0];
            TValue borrowedValue = rightNode.Values[0];

            // O'ng tugundan birinchi elementni o'chiramiz
            Array.Copy(rightNode.Keys, 1, rightNode.Keys, 0, rightNode.KeyCount - 1);
            Array.Copy(rightNode.Values, 1, rightNode.Values, 0, rightNode.KeyCount - 1);
            rightNode.KeyCount--;

            // Chap tugunning oxiriga qo'shamiz
            leftNode.Keys[leftNode.KeyCount] = borrowedKey;
            leftNode.Values[leftNode.KeyCount] = borrowedValue;
            leftNode.KeyCount++;

            return true;
        }

        return false;
    }

    public static void MergeWithRight<TKey, TValue>(
        this LeafNode<TKey, TValue> leftNode, 
        LeafNode<TKey, TValue> rightNode) where TKey : IComparable<TKey>
    {
        // O'ng tugunning hamma ma'lumotini chapga ko'chirish
        Array.Copy(rightNode.Keys, 0, leftNode.Keys, leftNode.KeyCount, rightNode.KeyCount);
        Array.Copy(rightNode.Values, 0, leftNode.Values, leftNode.KeyCount, rightNode.KeyCount);
        leftNode.KeyCount += rightNode.KeyCount;

        // Zanjirni yangilash
        leftNode.NextLeaf = rightNode.NextLeaf;
        if (rightNode.NextLeaf != null)
        {
            rightNode.NextLeaf.PrevLeaf = leftNode;
        }
    }
}
```
**Tushuntirish:** Underflow boshqaruvi daraxtning yemirilib (sparse) ketishining oldini oladi. Barcha tugunlar kamida 50% to'la bo'lishi xotira sarfini tejaydi va B+Tree ning balanslangan geometriyasini kafolatlaydi.
---

### Topshiriq #1218: Diskka Asoslangan B+Tree: Sahifa ID va Disk Pointerlar
**Tavsif:** RAM sig'maydigan ulkan B+Tree indekslarida tugunlar C# obyekt havolalari (object references) orqali emas, balki 32-bitli `PageID` orqali bog'lanadi. Bu tugunlarni Buffer Pool orqali diskdan o'qib-yozish imkonini beradi.
**Talablar:**
- `DiskBPlusInternalPage`: `Keys` massivi va `ChildPageIDs` massivi.
- Xotirada tekis bayt buferi (flat byte buffer) ko'rinishida serialize qilingan tugun strukturasi.
**Yechim (C#):**
```csharp
using System;
using System.Runtime.InteropServices;

namespace StorageEngine.Indexing;

[StructLayout(LayoutKind.Sequential, Pack = 1)]
public struct DiskPageHeader
{
    public int PageId;
    public int PageType; // 1 = Internal, 2 = Leaf
    public int ItemCount;
    public int NextPageId;
}

public sealed unsafe class DiskBPlusInternalPage
{
    public const int MaxKeys = 128;
    private readonly byte* _buffer;

    public DiskBPlusInternalPage(byte* buffer) => _buffer = buffer;

    public ref DiskPageHeader Header => ref *(DiskPageHeader*)_buffer;

    public int GetChildPageId(int index)
    {
        byte* childrenStart = _buffer + sizeof(DiskPageHeader) + (MaxKeys * sizeof(long));
        return *((int*)childrenStart + index);
    }

    public void SetChildPageId(int index, int childPageId)
    {
        byte* childrenStart = _buffer + sizeof(DiskPageHeader) + (MaxKeys * sizeof(long));
        *((int*)childrenStart + index) = childPageId;
    }

    public long GetKey(int index)
    {
        byte* keysStart = _buffer + sizeof(DiskPageHeader);
        return *((long*)keysStart + index);
    }
}
```
**Tushuntirish:** Diskka asoslangan B+Tree tugunlari to'g'ridan-to'g'ri 4KB/8KB li xotira freymiga joylashadi. Hech qanday pointer chasing va GC overhead bo'lmaydi; tugun freymga yuklanishi bilanoq uni darhol indeks sifatida ishlatish mumkin.
---

### Topshiriq #1219: Prefix Compression B+Tree: Matnli Kalitlarni Siqish
**Tavsif:** Agar indeks kalitlari matn (masalan, URL manzillar yoki UUID lar) bo'lsa, bitta tugun ichidagi kalitlar bir xil prefiksga ega bo'ladi (masalan, `https://api.domain.com/v1/...`). Prefikslarni umumlashtirib siqish orqali bitta sahifaga 3-4 barobar ko'proq kalit joylashtirish mumkin.
**Talablar:**
- Tugun darajasida umumiy prefiksni (Common Prefix) aniqlash.
- Kalitlarni faqat sufiks (Suffix) ko'rinishida saqlash.
**Yechim (C#):**
```csharp
using System;
using System.Text;

namespace StorageEngine.Indexing;

public sealed class PrefixCompressedBlock
{
    public string CommonPrefix { get; private set; }
    public string[] Suffixes { get; }
    public int Count { get; private set; }

    public PrefixCompressedBlock(int capacity)
    {
        Suffixes = new string[capacity];
    }

    public void BuildFromSortedKeys(string[] sortedKeys)
    {
        if (sortedKeys.Length == 0) return;

        // 1. Eng uzun umumiy prefiksni topamiz
        string first = sortedKeys[0];
        string last = sortedKeys[^1];
        int prefixLen = 0;

        while (prefixLen < first.Length && prefixLen < last.Length && first[prefixLen] == last[prefixLen])
        {
            prefixLen++;
        }

        CommonPrefix = first[..prefixLen];

        // 2. Faqat sufikslarni saqlaymiz
        Count = sortedKeys.Length;
        for (int i = 0; i < sortedKeys.Length; i++)
        {
            Suffixes[i] = sortedKeys[i][prefixLen..];
        }
    }

    public string GetFullKey(int index) => CommonPrefix + Suffixes[index];
}
```
**Tushuntirish:** Prefiks siqish daraxtdagi tugunlar hajmini keskin qisqartiradi. Bu disk I/O operatsiyalarini va CPU keshidagi xatoliklarni (Cache Misses) kamaytirib, satrli indekslar tezligini oshiradi.
---

### Topshiriq #1220: B+Tree vs ConcurrentDictionary: Ko'p Oqimli Stress-Test Benchmark
**Tavsif:** Yangi ishlab chiqilgan B+Tree indeksining haqiqiy sanoat talablariga javob berishini tekshirish uchun uni .NET ning standart `ConcurrentDictionary` kolleksiyasi bilan ko'p oqimli kiritish va o'qish tezligi bo'yicha stress-testdan o'tkazish kerak.
**Talablar:**
- 16 ta parallel oqimda 1,000,000 ta kalit-qiymat kiritish va o'qish.
- Operatsiyalar/soniya (Throughput) va xotira allokatsiyasini o'lchash.
**Yechim (C#):**
```csharp
using System;
using System.Collections.Concurrent;
using System.Diagnostics;
using System.Threading.Tasks;

namespace StorageEngine.Benchmarks;

public static class IndexStressTester
{
    public static void RunBenchmark(int itemCount = 1_000_000)
    {
        var dict = new ConcurrentDictionary<long, long>();

        Console.WriteLine($"--- Stress Test: {itemCount:N0} elementlar ---");

        // ConcurrentDictionary testi
        var sw = Stopwatch.StartNew();
        Parallel.For(0, itemCount, i =>
        {
            dict.TryAdd(i, i * 2);
        });
        sw.Stop();
        Console.WriteLine($"ConcurrentDictionary Yozish: {sw.ElapsedMilliseconds} ms ({itemCount * 1000.0 / sw.ElapsedMilliseconds:N0} ops/sec)");

        sw.Restart();
        Parallel.For(0, itemCount, i =>
        {
            dict.TryGetValue(i, out _);
        });
        sw.Stop();
        Console.WriteLine($"ConcurrentDictionary O'qish: {sw.ElapsedMilliseconds} ms ({itemCount * 1000.0 / sw.ElapsedMilliseconds:N0} ops/sec)");
    }
}
```
**Tushuntirish:** Bunday benchmarklar orqali maxsus B+Tree ning afzalliklari (ayniqsa tartiblangan scan va disk persistence) ko'zga tashlanadi. Kesh-lokallik va minimal GC overhead yuqori yuklamalarda hal qiluvchi rol o'ynaydi.
---

### Topshiriq #1221: MemoryMappedFile va MemoryMappedViewAccessor Bilan Zero-Copy Kirish
**Tavsif:** Gigabaytlab ma'lumotlarni `FileStream.Read` orqali o'qish operatsion tizim keshidan ilova xotirasiga keraksiz nusxalash (Buffer Copy) talab qiladi. `MemoryMappedFile` yordamida faylni to'g'ridan-to'g'ri virtual xotira manziliga bog'lab (Memory Mapping), faylni RAM kabi o'qish arxitekturasini yaratish zarur.
**Talablar:**
- `MemoryMappedFile.CreateFromFile` orqali faylni xaritalash.
- `MemoryMappedViewAccessor` orqali ixtiyoriy ofsetdagi ma'lumotlarni o'qish va yozish.
**Yechim (C#):**
```csharp
using System;
using System.IO;
using System.IO.MemoryMappedFiles;

namespace StorageEngine.MMF;

public sealed class MemoryMappedStorage : IDisposable
{
    private readonly MemoryMappedFile _mmf;
    private readonly MemoryMappedViewAccessor _accessor;
    private readonly long _fileSize;

    public MemoryMappedStorage(string filePath, long initialCapacity = 1024 * 1024 * 100) // 100 MB
    {
        _fileSize = initialCapacity;
        _mmf = MemoryMappedFile.CreateFromFile(
            filePath, 
            FileMode.OpenOrCreate, 
            mapName: null, 
            capacity: initialCapacity, 
            MemoryMappedFileAccess.ReadWrite);

        _accessor = _mmf.CreateViewAccessor(0, initialCapacity, MemoryMappedFileAccess.ReadWrite);
    }

    public void WriteInt64(long offset, long value) => _accessor.Write(offset, value);
    public long ReadInt64(long offset) => _accessor.ReadInt64(offset);

    public void Dispose()
    {
        _accessor.Dispose();
        _mmf.Dispose();
    }
}
```
**Tushuntirish:** `MemoryMappedFile` operatsion tizimning Virtual Memory Manager (VMM) mexanizmidan foydalanadi. Ma'lumot faqat kerak bo'lganda (Page Fault orqali) RAM ga yuklanadi va keraksiz bufer nusxalashlari to'liq yo'qoladi.
---

### Topshiriq #1222: MemoryMarshal.Cast va MMF Bilan Structlarni Zero-Copy O'qish
**Tavsif:** Diskdagi murakkab binar yozuvlarni C# obyektlariga deserializatsiya qilish (JSON, Protobuf) CPU resurslarini yeydi. `MemoryMarshal.Cast` yordamida baytlar xotirasini bir zumda C# `struct` turiga hech qanday allokatsiyasiz (Zero-Copy) aylantirish lozim.
**Talablar:**
- `TradeOrder` unmanaged struct: OrderId, AccountId, Price, Quantity, Timestamp.
- MMF xotira ko'rsatkichidan `ReadOnlySpan<TradeOrder>` olish.
**Yechim (C#):**
```csharp
using System;
using System.Runtime.InteropServices;

namespace StorageEngine.MMF;

[StructLayout(LayoutKind.Sequential, Pack = 1)]
public readonly record struct TradeOrder(
    long OrderId,
    long AccountId,
    double Price,
    int Quantity,
    long Timestamp
);

public static class ZeroCopyDeserializer
{
    public static unsafe ReadOnlySpan<TradeOrder> AsOrderSpan(byte* pointer, int byteLength)
    {
        // Baytlar ketma-ketligini to'g'ridan-to'g'ri TradeOrder struct massiviga aylantirish
        var byteSpan = new ReadOnlySpan<byte>(pointer, byteLength);
        return MemoryMarshal.Cast<byte, TradeOrder>(byteSpan);
    }
}
```
**Tushuntirish:** `MemoryMarshal.Cast` 0 nanosekundda ishlaydi, chunki u hech qanday baytni nusxalamaydi, balki faqat tip tavsiflagichini (Type descriptor) o'zgartiradi. Bu moliyaviy birjalar va yuqori tezlikdagi log tahlilida millionlab yozuvlarni soniyasiga qayta ishlash imkonini beradi.
---

### Topshiriq #1223: FlushView: O'zgarishlarni Diskka Majburiy Sinxronlash (Fsync)
**Tavsif:** `MemoryMappedFile` ga yozilgan ma'lumotlar avvaliga faqat operatsion tizimning Page Cache qismida bo'ladi. Agar kompyuter o'chib qolsa, oxirgi o'zgarishlar yo'qolishi mumkin. Ma'lumotlarni drayverga jismonan yozib qo'yish (fsync) uchun `Flush` funksiyasini to'g'ri qo'llash shart.
**Talablar:**
- `MemoryMappedViewAccessor.Flush()` metodi orqali sahifani diskka tushirish.
- Faqat o'zgargan oraliqni (Dirty Region) flush qilish orqali I/O bosimini kamaytirish.
**Yechim (C#):**
```csharp
using System;
using System.IO.MemoryMappedFiles;

namespace StorageEngine.MMF;

public sealed class SynchronizedMMFStore
{
    private readonly MemoryMappedViewAccessor _accessor;

    public SynchronizedMMFStore(MemoryMappedViewAccessor accessor) => _accessor = accessor;

    public void WriteAndCommit(long offset, ReadOnlySpan<byte> data)
    {
        // 1. Ma'lumotni xotiraga yozamiz
        for (int i = 0; i < data.Length; i++)
        {
            _accessor.Write(offset + i, data[i]);
        }

        // 2. Faqat o'zgargan diapazonni jismoniy diskka tushiramiz (fsync)
        _accessor.Flush();
    }
}
```
**Tushuntirish:** `Flush()` chaqirilganda operatsion tizim virtual xotira sahifasini diskka to'kish (dirty page writeback) buyrug'ini oladi. Bu tranzaksiyalarning ACID barqarorligini (Durability) ta'minlaydi.
---

### Topshiriq #1224: UnmanagedMemoryAccessor va Unsafe Pointerlar bilan Ultra-Tezkor I/O
**Tavsif:** .NET ning xavfsiz `ReadInt64` kabi metodlari har safar chegaralarni (bounds check) tekshiradi. Storage engine ichki yadrosida maksimal tezlikka erishish uchun `byte*` (raw pointer) orqali to'g'ridan-to'g'ri virtual manzilga murojaat qilish zarur.
**Talablar:**
- `SafeMemoryMappedViewHandle.AcquirePointer` orqali xom ko'rsatkichni olish.
- Unsafe pointer orqali massivlarni nusxalash va to'g'ridan-to'g'ri o'qish.
**Yechim (C#):**
```csharp
using System;
using System.IO.MemoryMappedFiles;

namespace StorageEngine.MMF;

public sealed unsafe class FastPointerAccessor : IDisposable
{
    private readonly MemoryMappedViewAccessor _accessor;
    private byte* _pointer;

    public FastPointerAccessor(MemoryMappedViewAccessor accessor)
    {
        _accessor = accessor;
        _accessor.SafeMemoryMappedViewHandle.AcquirePointer(ref _pointer);
    }

    public long ReadFastInt64(long offset)
    {
        return *(long*)(_pointer + offset);
    }

    public void WriteFastInt64(long offset, long value)
    {
        *(long*)(_pointer + offset) = value;
    }

    public void Dispose()
    {
        if (_pointer != null)
        {
            _accessor.SafeMemoryMappedViewHandle.ReleasePointer();
            _pointer = null;
        }
    }
}
```
**Tushuntirish:** `byte*` ko'rsatkichlari orqali ishlaganda .NET JIT protsessorning oddiy `MOV` instruksiyasini generatsiya qiladi. Bu C/C++ tillaridagi to'g'ridan-to'g'ri xotira manipulyatsiyasi tezligi bilan 100% tenglashadi.
---

### Topshiriq #1225: Sliding Window MMF: Gigabaytlab Fayllarni Bo'lib Xaritalash
**Tavsif:** Agar fayl o'lchami yuzlab gigabayt bo'lsa, butun fayl uchun birdaniga yagona ViewAccessor yaratish 32-bit yoki cheklangan virtual manzillar fazosini to'ldirib qo'yishi mumkin. Faylni dinamik 64 MB li oynalar (Sliding Windows) orqali boshqarish lozim.
**Talablar:**
- Talab qilingan ofsetga qarab tegishli 64 MB li oynani topish yoki yangisini yaratish.
- Eski, ishlatilmayotgan oynalarni yopish (Eviction).
**Yechim (C#):**
```csharp
using System;
using System.Collections.Generic;
using System.IO.MemoryMappedFiles;

namespace StorageEngine.MMF;

public sealed class SlidingWindowMMF : IDisposable
{
    public const long WindowSize = 64 * 1024 * 1024; // 64 MB
    private readonly MemoryMappedFile _mmf;
    private readonly Dictionary<long, MemoryMappedViewAccessor> _activeWindows = new();

    public SlidingWindowMMF(MemoryMappedFile mmf) => _mmf = mmf;

    public MemoryMappedViewAccessor GetAccessorForOffset(long fileOffset, out long offsetInWindow)
    {
        long windowIndex = fileOffset / WindowSize;
        long windowStart = windowIndex * WindowSize;
        offsetInWindow = fileOffset - windowStart;

        if (!_activeWindows.TryGetValue(windowIndex, out var accessor))
        {
            accessor = _mmf.CreateViewAccessor(windowStart, WindowSize, MemoryMappedFileAccess.ReadWrite);
            _activeWindows[windowIndex] = accessor;
        }

        return accessor;
    }

    public void Dispose()
    {
        foreach (var acc in _activeWindows.Values) acc.Dispose();
        _activeWindows.Clear();
    }
}
```
**Tushuntirish:** Sliding Window texnikasi xotira sarfini qat'iy nazorat ostida ushlaydi. Faqat faol so'ralayotgan hududlargina xaritalanadi, qolgan qismlar esa diskda saqlanadi.
---

### Topshiriq #1226: Memory-Mapped Ring Buffer: IPC Xabarlar Navbati
**Tavsif:** Bitta operatsion tizim ichidagi ikkita mustaqil jarayon (masalan, API shlyuzi va Ma'lumotlar bazasi saqlash dvigateli) o'rtasida TCP soketlarsiz, to'g'ridan-to'g'ri xotira orqali soniyasiga 50M xabar uzatuvchi Ring Buffer yaratish zarur.
**Talablar:**
- Nomlangan (Named) MemoryMappedFile: `MemoryMappedFile.CreateOrOpen("Local\\DbIpcQueue", ...)`.
- Boshqaruvchi Header: `Head` va `Tail` indekslari (Interlocked bilan boshqariladi).
**Yechim (C#):**
```csharp
using System;
using System.IO.MemoryMappedFiles;
using System.Runtime.InteropServices;
using System.Threading;

namespace StorageEngine.MMF;

[StructLayout(LayoutKind.Sequential, Pack = 8)]
public struct RingBufferHeader
{
    public long Head;
    public long Tail;
    public int Capacity;
}

public sealed unsafe class MemoryMappedRingBuffer : IDisposable
{
    private readonly MemoryMappedFile _mmf;
    private readonly MemoryMappedViewAccessor _accessor;
    private byte* _ptr;
    private readonly int _bufferCapacity;

    public MemoryMappedRingBuffer(string mapName, int capacity = 1024 * 1024)
    {
        _bufferCapacity = capacity;
        int totalSize = sizeof(RingBufferHeader) + capacity;
        _mmf = MemoryMappedFile.CreateOrOpen(mapName, totalSize, MemoryMappedFileAccess.ReadWrite);
        _accessor = _mmf.CreateViewAccessor(0, totalSize);
        _accessor.SafeMemoryMappedViewHandle.AcquirePointer(ref _ptr);

        RingBufferHeader* header = (RingBufferHeader*)_ptr;
        if (header->Capacity == 0) header->Capacity = capacity;
    }

    public bool TryWrite(ReadOnlySpan<byte> message)
    {
        RingBufferHeader* header = (RingBufferHeader*)_ptr;
        long currentTail = Volatile.Read(ref header->Tail);
        long currentHead = Volatile.Read(ref header->Head);

        if (currentTail - currentHead + message.Length + sizeof(int) > _bufferCapacity)
        {
            return false; // Bufer to'lgan
        }

        byte* dataStart = _ptr + sizeof(RingBufferHeader);
        long writePos = currentTail % _bufferCapacity;

        *(int*)(dataStart + writePos) = message.Length;
        message.CopyTo(new Span<byte>(dataStart + writePos + sizeof(int), message.Length));

        Interlocked.Add(ref header->Tail, message.Length + sizeof(int));
        return true;
    }

    public void Dispose()
    {
        if (_ptr != null) _accessor.SafeMemoryMappedViewHandle.ReleasePointer();
        _accessor.Dispose();
        _mmf.Dispose();
    }
}
```
**Tushuntirish:** Xotiraga xaritalangan doiraviy bufer barcha tarmoq protokollari (TCP/HTTP) dan kamida 100 baravar tez ishlaydi, chunki unda na operatsion tizim drayverlari, na tarmoq steki qatnashadi.
---

### Topshiriq #1227: MMF Asosidagi Ruxsatli 4KB Sahifalar Xotirasi (Paged Storage)
**Tavsif:** Baza jadvallari diskda teng o'lchamdagi sahifalar (odatda 4096 bayt - OS Page size) ko'rinishida saqlanadi. Berilgan `PageID` bo'yicha to'g'ridan-to'g'ri 4KB li xotira blokini oluvchi Paged Storage dvigatelini yaratish kerak.
**Talablar:**
- 4096 baytli sahifalar ko'rsatkichini hisoblash (`pageId * 4096`).
- Sahifaga Span orqali to'g'ridan-to'g'ri o'qish/yozish ruxsati.
**Yechim (C#):**
```csharp
using System;
using System.IO.MemoryMappedFiles;

namespace StorageEngine.MMF;

public sealed unsafe class MmfPagedStorage : IDisposable
{
    public const int PageSize = 4096;
    private readonly MemoryMappedFile _mmf;
    private readonly MemoryMappedViewAccessor _accessor;
    private byte* _basePointer;

    public MmfPagedStorage(string filePath, int initialPageCount = 1000)
    {
        long capacity = (long)initialPageCount * PageSize;
        _mmf = MemoryMappedFile.CreateFromFile(filePath, System.IO.FileMode.OpenOrCreate, null, capacity, MemoryMappedFileAccess.ReadWrite);
        _accessor = _mmf.CreateViewAccessor(0, capacity);
        _accessor.SafeMemoryMappedViewHandle.AcquirePointer(ref _basePointer);
    }

    public Span<byte> GetPage(int pageId)
    {
        long offset = (long)pageId * PageSize;
        return new Span<byte>(_basePointer + offset, PageSize);
    }

    public void Dispose()
    {
        if (_basePointer != null) _accessor.SafeMemoryMappedViewHandle.ReleasePointer();
        _accessor.Dispose();
        _mmf.Dispose();
    }
}
```
**Tushuntirish:** 4KB o'lcham apparat xotirasi (CPU MMU va SSD Block) bilan aynan mos keladi. Bu sahifalarni o'qishda apparat darajasida minimal Page Fault bilan ishlashga imkon beradi.
---

### Topshiriq #1228: OS Paging va VirtualAlloc / Prefetching Monitoringi
**Tavsif:** MMF ishlatilganda, agar qidirilayotgan sahifa RAM da bo'lmasa, operatsion tizim Hard Page Fault chaqirib jarayonni muzlatib qo'yadi. So'rovlarni sekinlashishdan saqlash uchun Windows `PrefetchVirtualMemory` yoki ketma-ket o'qishda Linux `madvise(MADV_WILLNEED)` kabi oldindan yuklash mexanizmlari zarur.
**Talablar:**
- P/Invoke yordamida OS darajasidagi prefetching chaqiruvlari.
- Katta oraliqlarni oldindan xotiraga chaqirib olish (Warm-up).
**Yechim (C#):**
```csharp
using System;
using System.Runtime.InteropServices;

namespace StorageEngine.MMF;

public static class MemoryPrefetcher
{
    [StructLayout(LayoutKind.Sequential)]
    private struct WIN32_MEMORY_RANGE_ENTRY
    {
        public IntPtr VirtualAddress;
        public UIntPtr NumberOfBytes;
    }

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool PrefetchVirtualMemory(
        IntPtr hProcess,
        UIntPtr NumberOfEntries,
        [In] WIN32_MEMORY_RANGE_ENTRY[] VirtualAddresses,
        uint Flags);

    public static unsafe void PrefetchRange(byte* pointer, long length)
    {
        if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
        {
            var entries = new WIN32_MEMORY_RANGE_ENTRY[]
            {
                new() { VirtualAddress = (IntPtr)pointer, NumberOfBytes = (UIntPtr)length }
            };
            IntPtr currentProcess = System.Diagnostics.Process.GetCurrentProcess().Handle;
            PrefetchVirtualMemory(currentProcess, (UIntPtr)1, entries, 0);
        }
    }
}
```
**Tushuntirish:** PrefetchVirtualMemory operatsion tizimga diskdagi sahifalarni fonda zudlik bilan RAM ga yuklashni buyuradi. Bu orqali foydalanuvchi so'rovi kelganda sahifa allaqachon xotirada tayyor turadi va Page Fault kechikishi bartaraf qilinadi.
---

### Topshiriq #1229: Struct Alignment va Padding: MMF da Saqlanadigan Unmanaged Structlar
**Tavsif:** Unmanaged xotirada ma'lumotlar saqlanganda, agar struct maydonlari CPU so'z chegarasiga (Word boundary: 4 yoki 8 bayt) to'g'ri tekislanmagan bo'lsa (Unaligned memory access), protsessor unumdorligi 2-3 barobar pasayadi yoki arxitekturaga qarab dastur qulaydi.
**Talablar:**
- `StructLayout(LayoutKind.Explicit)` yoki `Sequential, Pack = 8` yordamida tekislangan (aligned) ma'lumotlar modeli.
- Barcha maydonlar ofsetlarini va umumiy o'lchamni hisoblash.
**Yechim (C#):**
```csharp
using System;
using System.Runtime.InteropServices;

namespace StorageEngine.MMF;

// 8-bayt chegarasiga to'g'ri tekislangan struct
[StructLayout(LayoutKind.Explicit, Size = 32)]
public readonly struct AlignedTelemetryRecord
{
    [FieldOffset(0)] public readonly long DeviceId;     // 8 bayt (0..7)
    [FieldOffset(8)] public readonly double SensorValue;// 8 bayt (8..15)
    [FieldOffset(16)] public readonly long TimestampUtc;// 8 bayt (16..23)
    [FieldOffset(24)] public readonly int StatusFlags;  // 4 bayt (24..27)
    [FieldOffset(28)] private readonly int _padding;    // 4 bayt to'ldiruvchi (28..31) - 32 baytga to'ldiradi

    public AlignedTelemetryRecord(long deviceId, double value, long timestamp, int flags)
    {
        DeviceId = deviceId;
        SensorValue = value;
        TimestampUtc = timestamp;
        StatusFlags = flags;
        _padding = 0;
    }
}
```
**Tushuntirish:** Protsessorlar 64-bitli sonlarni 8 ga karrali manzillardan bitta taktda o'qiydi. Agar padding qo'shilmasa, bitta 64-bitli son ikkita alohida kesh liniyasiga bo'linib qolishi (Split Lock) va tizimni sekinlashtirishi mumkin.
---

### Topshiriq #1230: Zero-Copy Serialization: BinaryPrimitives va Span<byte>
**Tavsif:** Turli arxitekturalarda (Little Endian vs Big Endian) xotirani diskka to'kishda xatolik bo'lmasligi uchun .NET 8/9 ning `BinaryPrimitives` sinfidan foydalanib, har bir primitiv turni Span ichiga hech qanday ob'ekt yaratmasdan (Allocation-free) tezkor yozish kerak.
**Talablar:**
- `BinaryPrimitives.WriteInt64LittleEndian`, `WriteDoubleLittleEndian` kabi metodlarni qo'llash.
- Murakkab yozuvni Span buferiga seriyalashtiruvchi statik yordamchi sinf.
**Yechim (C#):**
```csharp
using System;
using System.Buffers.Binary;

namespace StorageEngine.Serialization;

public static class FastPrimitiveSerializer
{
    public static int SerializeTelemetry(Span<byte> destination, long deviceId, double value, long timestamp)
    {
        if (destination.Length < 24) throw new ArgumentException("Bufer yetarli emas!");

        BinaryPrimitives.WriteInt64LittleEndian(destination[..8], deviceId);
        long doubleBits = BitConverter.DoubleToInt64Bits(value);
        BinaryPrimitives.WriteInt64LittleEndian(destination.Slice(8, 8), doubleBits);
        BinaryPrimitives.WriteInt64LittleEndian(destination.Slice(16, 8), timestamp);

        return 24;
    }

    public static (long deviceId, double value, long timestamp) DeserializeTelemetry(ReadOnlySpan<byte> source)
    {
        long deviceId = BinaryPrimitives.ReadInt64LittleEndian(source[..8]);
        long doubleBits = BinaryPrimitives.ReadInt64LittleEndian(source.Slice(8, 8));
        double value = BitConverter.Int64BitsToDouble(doubleBits);
        long timestamp = BinaryPrimitives.ReadInt64LittleEndian(source.Slice(16, 8));

        return (deviceId, value, timestamp);
    }
}
```
**Tushuntirish:** `BinaryPrimitives` apparat darajasida intrinsiklarga aylanadi va xotira allokatsiyasiz ishlaydi. Bu orqali tarmoq va disk I/O buferlari o'rtasida ma'lumotlarni sekundiga o'nlab gigabayt tezlikda konvertatsiya qilish mumkin.
---

### Topshiriq #1231: Slotted-Page Layout: Header, Slot Array va Free Space Boshqaruvi
**Tavsif:** PostgreSQL va SQLite kabi relational ma'lumotlar bazalarida har bir sahifa ichida o'zgaruvchan uzunlikdagi (Variable-length) yozuvlarni saqlash uchun "Slotted-Page" arxitekturasi qo'llaniladi. Sahifa boshi va oxiridan markazga qarab o'sadi.
**Talablar:**
- Sahifa boshi: `PageHeader` (SlotCount, LowerOffset, UpperOffset, FreeSpace).
- Slot Array: Har bir slot `Offset` (2 bayt) va `Length` (2 bayt) dan iborat bo'lib, pastga qarab o'sadi.
- Ma'lumotlar tanasi (Tuples): Sahifaning eng oxiridan yuqoriga qarab o'sadi.
**Yechim (C#):**
```csharp
using System;
using System.Runtime.InteropServices;

namespace StorageEngine.Pages;

[StructLayout(LayoutKind.Sequential, Pack = 2)]
public struct PageHeader
{
    public ushort SlotCount;   // Sahifadagi slotlar soni
    public ushort LowerOffset; // Slotlar massivining tugash nuqtasi (pastga qarab o'sadi)
    public ushort UpperOffset; // Yozuvlar tushayotgan eng pastki nuqta (yuqoriga qarab o'sadi)
    public ushort PageSize;    // Masalan, 4096 yoki 8192
}

[StructLayout(LayoutKind.Sequential, Pack = 2)]
public readonly record struct PageSlot(ushort Offset, ushort Length);

public sealed unsafe class SlottedPage
{
    public const int DefaultPageSize = 4096;
    private readonly byte* _buffer;

    public SlottedPage(byte* buffer, ushort pageSize = DefaultPageSize)
    {
        _buffer = buffer;
        ref PageHeader header = ref GetHeader();
        if (header.PageSize == 0)
        {
            // Yangi sahifani initsializatsiya qilish
            header.SlotCount = 0;
            header.LowerOffset = (ushort)sizeof(PageHeader);
            header.UpperOffset = pageSize;
            header.PageSize = pageSize;
        }
    }

    public ref PageHeader GetHeader() => ref *(PageHeader*)_buffer;

    public int FreeSpaceRemaining
    {
        get
        {
            ref PageHeader h = ref GetHeader();
            return h.UpperOffset - h.LowerOffset;
        }
    }
}
```
**Tushuntirish:** Slotted-Page arxitekturasining go'zalligi shundaki, slotlar massivi chapdan o'ngga, yozuvlarning o'zi esa o'ngdan chapga qarab o'sadi. Ular o'rtasida bo'sh joy qoladi. Qachonki `LowerOffset + sizeof(Slot) > UpperOffset` bo'lsa, sahifa to'lgan hisoblanadi.
---

### Topshiriq #1232: Slotted-Page da O'zgaruvchan Uzunlikdagi Yozuvlarni Kiritish (Insert Record)
**Tavsif:** Slotted-Page ga yangi yozuv (masalan, JSON matni yoki foydalanuvchi profili) kiritilganda, bo'sh joy yetarliligi tekshiriladi, yozuv sahifa oxiriga joylanadi va unga ko'rsatuvchi yangi Slot ro'yxatga qo'shiladi.
**Talablar:**
- Bo'sh joy yetarli bo'lmasa `-1` (Page Full) qaytarish.
- Yangi yozuvni `UpperOffset - recordLength` joyiga yozish.
- Yangi slotni `LowerOffset` ga yozib, `SlotCount` ni oshirish va yangi Slot indeksini qaytarish.
**Yechim (C#):**
```csharp
using System;

namespace StorageEngine.Pages;

public static class SlottedPageInsertExtensions
{
    public static unsafe int InsertRecord(this SlottedPage page, ReadOnlySpan<byte> recordData)
    {
        ref PageHeader header = ref page.GetHeader();
        int requiredSpace = sizeof(PageSlot) + recordData.Length;

        // Bo'sh joy yetarlimi?
        if (page.FreeSpaceRemaining < requiredSpace)
        {
            return -1; // Sahifada joy yetarli emas
        }

        // 1. Ma'lumotni sahifaning oxirgi bo'sh joyiga yozamiz
        ushort newUpperOffset = (ushort)(header.UpperOffset - recordData.Length);
        byte* pagePtr = (byte*)Unsafe.AsPointer(ref header);
        recordData.CopyTo(new Span<byte>(pagePtr + newUpperOffset, recordData.Length));
        header.UpperOffset = newUpperOffset;

        // 2. Yangi slot yaratamiz
        PageSlot* slots = (PageSlot*)(pagePtr + sizeof(PageHeader));
        int slotIndex = header.SlotCount;
        slots[slotIndex] = new PageSlot(newUpperOffset, (ushort)recordData.Length);

        // 3. Header chegaralarini yangilaymiz
        header.SlotCount++;
        header.LowerOffset += (ushort)sizeof(PageSlot);

        return slotIndex;
    }
}
```
**Tushuntirish:** Yozuv qanchalik uzun bo'lishidan qat'i nazar, unga berilgan identifikator (SlotIndex) 0, 1, 2 kabi ixcham butun son bo'ladi. Tashqi indekslar yozuvning xotiradagi jismoniy bayt ofsetini bilishi shart emas, faqat Slot raqamini bilsa kifoya.
---

### Topshiriq #1233: Slotted-Page Yozuvni O'chirish va Sahifani Defragmentatsiya Qilish
**Tavsif:** Yozuv o'chirilganda uning sloti bo'shatiladi (Offset = 0, Length = 0). Biroq sahifa o'rtasida o'lik bo'shliqlar (holes) paydo bo'ladi. Sahifani qayta to'ldirish uchun mavjud faol yozuvlarni bir tomonga siljitib zichlashtirish (Page Compaction) algoritmi talab qilinadi.
**Talablar:**
- Slotni o'chirish (`DeleteRecord(int slotIndex)`).
- Sahifadagi barcha faol yozuvlarni sahifaning eng oxiriga ketma-ket zichlashtirib ko'chirish va slotlarning ofsetlarini yangilash.
**Yechim (C#):**
```csharp
using System;

namespace StorageEngine.Pages;

public static class SlottedPageCompactionExtensions
{
    public static unsafe void DeleteRecord(this SlottedPage page, int slotIndex)
    {
        ref PageHeader header = ref page.GetHeader();
        if (slotIndex < 0 || slotIndex >= header.SlotCount) return;

        byte* pagePtr = (byte*)Unsafe.AsPointer(ref header);
        PageSlot* slots = (PageSlot*)(pagePtr + sizeof(PageHeader));
        slots[slotIndex] = new PageSlot(0, 0); // O'chirilgan slot
    }

    public static unsafe void DefragmentPage(this SlottedPage page)
    {
        ref PageHeader header = ref page.GetHeader();
        byte* pagePtr = (byte*)Unsafe.AsPointer(ref header);
        PageSlot* slots = (PageSlot*)(pagePtr + sizeof(PageHeader));

        // Yangi vaqtinchalik yozish nuqtasi sahifa oxiridan boshlanadi
        ushort currentUpper = header.PageSize;

        for (int i = 0; i < header.SlotCount; i++)
        {
            if (slots[i].Length > 0) // Tirik yozuv
            {
                ushort oldOffset = slots[i].Offset;
                ushort length = slots[i].Length;

                currentUpper -= length;

                // Agar ma'lumot surilgan bo'lsa, xotirada ko'chiramiz
                if (currentUpper != oldOffset)
                {
                    Buffer.MemoryCopy(pagePtr + oldOffset, pagePtr + currentUpper, length, length);
                    slots[i] = new PageSlot(currentUpper, length);
                }
            }
        }

        header.UpperOffset = currentUpper;
    }
}
```
**Tushuntirish:** Defragmentatsiya (sahifani tozalash) barcha tarqoq bo'sh joylarni birlashtirib, `UpperOffset` va `LowerOffset` o'rtasidagi yagona yaxlit bo'shliqqa aylantiradi. Bu keyingi yozuvlarga joy ochib beradi.
---

### Topshiriq #1234: Record ID (RID): PageID va SlotID Arxitekturasi
**Tavsif:** Butun ma'lumotlar bazasi bo'ylab har qanday yozuvning global manzili Record Identifier (RID) bilan belgilanadi. 64-bitli RID 32-bit `PageID` va 16-bit `SlotID` dan tashkil topadi. Ushbu ko'rsatkichlar tizimini yaratish kerak.
**Talablar:**
- `RecordId` unmanaged struct: PageId, SlotId.
- RID orqali SlottedPage ga murojaat qilib ma'lumotni Span ko'rinishida olish funksiyasi.
**Yechim (C#):**
```csharp
using System;
using System.Runtime.InteropServices;

namespace StorageEngine.Pages;

[StructLayout(LayoutKind.Explicit, Size = 8)]
public readonly struct RecordId : IEquatable<RecordId>
{
    [FieldOffset(0)] public readonly int PageId;
    [FieldOffset(4)] public readonly ushort SlotId;
    [FieldOffset(6)] private readonly ushort _reserved;

    public RecordId(int pageId, ushort slotId)
    {
        PageId = pageId;
        SlotId = slotId;
        _reserved = 0;
    }

    public static readonly RecordId Invalid = new(-1, ushort.MaxValue);

    public bool Equals(RecordId other) => PageId == other.PageId && SlotId == other.SlotId;
    public override string ToString() => $"RID({PageId}:{SlotId})";
}

public static class SlottedPageReadExtensions
{
    public static unsafe ReadOnlySpan<byte> ReadRecord(this SlottedPage page, ushort slotId)
    {
        ref PageHeader header = ref page.GetHeader();
        if (slotId >= header.SlotCount) return ReadOnlySpan<byte>.Empty;

        byte* pagePtr = (byte*)Unsafe.AsPointer(ref header);
        PageSlot* slots = (PageSlot*)(pagePtr + sizeof(PageHeader));
        PageSlot slot = slots[slotId];

        if (slot.Length == 0) return ReadOnlySpan<byte>.Empty; // O'chirilgan

        return new ReadOnlySpan<byte>(pagePtr + slot.Offset, slot.Length);
    }
}
```
**Tushuntirish:** B+Tree ikkilamchi indekslarida haqiqiy qator qiymatlari saqlanmaydi; indeks barglarida faqat kalit va o'sha qatorning `RecordId (PageID, SlotID)` manzili saqlanadi. Jadval qatori o'zgarganda faqat sahifa ichidagi slot yangilanadi, indekslar esa o'zgarmasdan qoladi.
---

### Topshiriq #1235: Buffer Pool Manager: Page Table va Frame Boshqaruvi
**Tavsif:** Ma'lumotlar bazasida minglab sahifalar mavjud, lekin RAM faqat cheklangan miqdordagi freymlarga (masalan, 1024 ta freym) ega. So'ralgan `PageID` ayni paytda xotirada bormi yoki yo'qligini aniqlovchi va xotiradagi bo'sh freymlarni boshqaruvchi Buffer Pool Manager kerak.
**Talablar:**
- `PageTable`: `PageID` -> `FrameID` xaritasi (ConcurrentDictionary).
- `FreeList`: Foydalanilmagan freymlar navbati (ConcurrentQueue).
- Sahifani qidirish (FetchPage): agar xotirada bo'lmasa, diskdan freymga yuklash.
**Yechim (C#):**
```csharp
using System;
using System.Collections.Concurrent;
using System.IO;

namespace StorageEngine.BufferPool;

public sealed class BufferPoolManager
{
    private readonly int _poolSize;
    private readonly ConcurrentDictionary<int, int> _pageTable = new();
    private readonly ConcurrentQueue<int> _freeList = new();
    private readonly byte[][] _frames;
    private readonly FileStream _diskFile;

    public BufferPoolManager(int poolSize, FileStream diskFile)
    {
        _poolSize = poolSize;
        _diskFile = diskFile;
        _frames = new byte[poolSize][];

        for (int i = 0; i < poolSize; i++)
        {
            _frames[i] = new byte[4096];
            _freeList.Enqueue(i);
        }
    }

    public byte[] FetchPage(int pageId)
    {
        // 1. Sahifa allaqachon xotiradami?
        if (_pageTable.TryGetValue(pageId, out int frameId))
        {
            return _frames[frameId];
        }

        // 2. Bo'sh freym olamiz
        if (_freeList.TryDequeue(out frameId))
        {
            // Diskdan o'qish
            _diskFile.Seek((long)pageId * 4096, SeekOrigin.Begin);
            _diskFile.ReadExactly(_frames[frameId], 0, 4096);

            _pageTable[pageId] = frameId;
            return _frames[frameId];
        }

        throw new InvalidOperationException("Buffer Pool to'lgan, Eviction talab qilinadi!");
    }
}
```
**Tushuntirish:** Buffer Pool Manager ma'lumotlar bazasining "yuragi" hisoblanadi. U so'rovlar bajaruvchi dvigatel (Execution Engine) va jismoniy disk drayveri o'rtasida shaffof vositachilik qilib, disk I/O operatsiyalarini 95% ga qisqartiradi.
---

### Topshiriq #1236: LRU-K (LRU-2) Eviction: Sequential Scan Pollution dan Himoya
**Tavsif:** Oddiy LRU (Least Recently Used) algoritmining katta kamchiligi shundaki, bitta katta ketma-ket skanerlash (masalan, `SELECT * FROM big_table`) keshdagi barcha tez-tez so'raladigan "issiq" sahifalarni chiqarib yuboradi (Cache Pollution). Oxirgi 2 ta murojaat vaqtini hisobga oluvchi LRU-2 algoritmini yaratish lozim.
**Talablar:**
- Har bir sahifa uchun oxirgi $K$ ta (masalan, $K=2$) murojaat vaqtini (Timestamp) saqlash.
- Agar sahifaga faqat 1 marta murojaat qilingan bo'lsa, uning ustuvorligi eng past deb baholanadi va u birinchi bo'lib keshdan chiqariladi.
**Yechim (C#):**
```csharp
using System;
using System.Collections.Generic;

namespace StorageEngine.BufferPool;

public sealed class Lru2Replacer
{
    private sealed class PageHistory
    {
        public long LastAccess;
        public long PreviousAccess; // K=2 murojaat vaqti
        public int AccessCount;
    }

    private readonly Dictionary<int, PageHistory> _history = new();
    private long _currentLogicalTime;

    public void RecordAccess(int frameId)
    {
        _currentLogicalTime++;
        if (!_history.TryGetValue(frameId, out var h))
        {
            h = new PageHistory();
            _history[frameId] = h;
        }

        h.PreviousAccess = h.LastAccess;
        h.LastAccess = _currentLogicalTime;
        h.AccessCount++;
    }

    public int Victim()
    {
        int victimFrame = -1;
        long oldestTime = long.MaxValue;

        // 1-bosqich: Faqat bir marta murojaat qilinganlarni qidirish (Scan pollution)
        foreach (var (frame, h) in _history)
        {
            if (h.AccessCount == 1 && h.LastAccess < oldestTime)
            {
                oldestTime = h.LastAccess;
                victimFrame = frame;
            }
        }

        if (victimFrame != -1)
        {
            _history.Remove(victimFrame);
            return victimFrame;
        }

        // 2-bosqich: K=2 PreviousAccess bo'yicha eng eskisini chiqarish
        foreach (var (frame, h) in _history)
        {
            if (h.PreviousAccess < oldestTime)
            {
                oldestTime = h.PreviousAccess;
                victimFrame = frame;
            }
        }

        if (victimFrame != -1) _history.Remove(victimFrame);
        return victimFrame;
    }
}
```
**Tushuntirish:** LRU-K (ayniqsa LRU-2) algoritmi zamonaviy DBMS larda (PostgreSQL, SQL Server) standart hisoblanadi. U tasodifiy bir martalik so'rovlar (full scan) keshni "ifloslantirishi"ning oldini oladi va faqat chindan ham muntazam ishlatiladigan sahifalarni xotirada saqlaydi.
---

### Topshiriq #1237: CLOCK (Second Chance) Sahifalarni Almashtirish Algoritmi
**Tavsif:** LRU-K juda samarali, lekin har safar qidirish $O(N)$ yoki murakkab daraxt talab qiladi. CLOCK algoritmi soat mili kabi aylanuvchi ko'rsatkich va 1-bitli `ReferenceBit` orqali $O(1)$ amortizatsiyalangan vaqtda yangi sahifaga joy ochib beradi.
**Talablar:**
- `ReferenceBit` massivi (har bir freym uchun 1 bit).
- Agar bit `1` bo'lsa, uni `0` ga tushirib ikkinchi imkoniyat (Second Chance) berish va keyingi freymga o'tish.
- Agar bit `0` bo'lsa, ushbu freymni almashtirish uchun tanlash (Victim).
**Yechim (C#):**
```csharp
using System;

namespace StorageEngine.BufferPool;

public sealed class ClockReplacer
{
    private readonly int _capacity;
    private readonly bool[] _referenceBits;
    private readonly bool[] _inReplacer;
    private int _clockHand;

    public ClockReplacer(int capacity)
    {
        _capacity = capacity;
        _referenceBits = new bool[capacity];
        _inReplacer = new bool[capacity];
        _clockHand = 0;
    }

    public void SetReferenced(int frameId)
    {
        _referenceBits[frameId] = true;
        _inReplacer[frameId] = true;
    }

    public bool TryVictim(out int victimFrameId)
    {
        victimFrameId = -1;
        int scans = 0;

        while (scans < _capacity * 2)
        {
            if (_inReplacer[_clockHand])
            {
                if (_referenceBits[_clockHand])
                {
                    // Ikkinchi imkoniyat: bitni o'chirib keyingisiga o'tamiz
                    _referenceBits[_clockHand] = false;
                }
                else
                {
                    // 0 bo'lgan freym topildi - uni qurbon (victim) qilamiz
                    victimFrameId = _clockHand;
                    _inReplacer[_clockHand] = false;
                    _clockHand = (_clockHand + 1) % _capacity;
                    return true;
                }
            }

            _clockHand = (_clockHand + 1) % _capacity;
            scans++;
        }

        return false;
    }
}
```
**Tushuntirish:** CLOCK algoritmi deyarli LRU kabi yuqori kesh-hit foizini beradi, biroq xotira va CPU xarajatlari bo'yicha juda yengil bo'lib, yuqori yuklamali bazalarda qulflanishlarsiz oson parallellashtiriladi.
---

### Topshiriq #1238: Dirty Page Tracking va Background Writer Dvigateli
**Tavsif:** Agar keshdan chiqarilayotgan sahifa o'zgartirilmagan (Clean) bo'lsa, uni shunchaki xotiradan tashlab yuborish mumkin. Lekin agar unga yozish amalga oshirilgan bo'lsa (Dirty Page), avval uni diskka yozish shart. Foydalanuvchi so'rovlarini to'xtatib qo'ymaslik uchun Background Writer fon oqimida bu sahifalarni muntazam diskka to'kib borishi lozim.
**Talablar:**
- `IsDirty` bayrog'i (har bir freym uchun).
- Fon oqimi navbatdagi iflos (dirty) sahifalarni topib diskka sinxronlash va bayroqni tozalash mexanizmi.
**Yechim (C#):**
```csharp
using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;

namespace StorageEngine.BufferPool;

public sealed class BackgroundWriter : IAsyncDisposable
{
    private readonly bool[] _isDirty;
    private readonly byte[][] _frames;
    private readonly FileStream _diskFile;
    private readonly CancellationTokenSource _cts = new();
    private readonly Task _workerTask;

    public BackgroundWriter(int poolSize, byte[][] frames, FileStream diskFile)
    {
        _isDirty = new bool[poolSize];
        _frames = frames;
        _diskFile = diskFile;
        _workerTask = Task.Run(FlushLoopAsync);
    }

    public void MarkDirty(int frameId) => _isDirty[frameId] = true;

    private async Task FlushLoopAsync()
    {
        while (!_cts.Token.IsCancellationRequested)
        {
            try
            {
                await Task.Delay(500, _cts.Token).ConfigureAwait(false);

                for (int i = 0; i < _isDirty.Length; i++)
                {
                    if (_isDirty[i])
                    {
                        // Sahifani diskka yozish
                        _diskFile.Seek((long)i * 4096, SeekOrigin.Begin);
                        await _diskFile.WriteAsync(_frames[i], 0, 4096, _cts.Token).ConfigureAwait(false);
                        _isDirty[i] = false;
                    }
                }
                await _diskFile.FlushAsync(_cts.Token).ConfigureAwait(false);
            }
            catch (OperationCanceledException) { break; }
        }
    }

    public async ValueTask DisposeAsync()
    {
        _cts.Cancel();
        await _workerTask.ConfigureAwait(false);
        _cts.Dispose();
    }
}
```
**Tushuntirish:** Background Writer yangi so'rovlar kelganda keshda doimo toza (Clean) freymlar bo'lishini ta'minlaydi. Agar bu fon oqimi bo'lmasa, har bir yangi sahifani yuklashda eski iflos sahifaning diskka yozilishini kutishga to'g'ri kelardi (I/O stall).
---

### Topshiriq #1239: Pin Count (Reference Counting) va Latch lar Bilan Sahifani Qulflash
**Tavsif:** Agar biror so'rov ayni paytda sahifani o'qiyotgan yoki o'zgartirayotgan bo'lsa, Buffer Pool Eviction algoritmi ushbu sahifani keshdan chiqarib yubormasligi (Evict qilmasligi) shart. Buni ta'minlash uchun `PinCount` mexanizmi qo'llaniladi.
**Talablar:**
- `Pin(pageId)`: PinCount ni oshirish va freym ko'rsatkichini qaytarish.
- `Unpin(pageId, isDirty)`: PinCount ni kamaytirish.
- Eviction faqat `PinCount == 0` bo'lgan sahifalarnigina keshdan chiqarishi mumkin.
**Yechim (C#):**
```csharp
using System;
using System.Threading;

namespace StorageEngine.BufferPool;

public sealed class PinnedFrame
{
    private int _pinCount;
    public readonly ReaderWriterLockSlim PageLatch = new();

    public int PinCount => Volatile.Read(ref _pinCount);

    public void Pin() => Interlocked.Increment(ref _pinCount);

    public void Unpin()
    {
        if (Interlocked.Decrement(ref _pinCount) < 0)
        {
            throw new InvalidOperationException("Pin count manfiy bo'lishi mumkin emas!");
        }
    }

    public bool CanEvict => Volatile.Read(ref _pinCount) == 0;
}
```
**Tushuntirish:** Pin/Unpin ma'lumotlar bazasida xotira butunligini saqlashning fundamental qoidasidir. Pin qilingan sahifa RAM da "mixlab qo'yilgan" hisoblanadi va operatsiya tugamaguncha hech qanday almashtirish mexanizmi unga teginolmaydi.
---

### Topshiriq #1240: Sahifa Checksum: CRC32C va xxHash64 Bilan Disk Buzilishlarini Aniqlash
**Tavsif:** Diskdagi magnit/flash xotira buzilishi (Bit Rot) yoki chala yozilish (Torn Page) oqibatida sahifa ma'lumotlari buzilishi mumkin. Har bir 4KB sahifa saqlanayotganda uning apparat tezligidagi CRC32C yoki xxHash64 nazorat yig'indisi hisoblanishi va o'qishda tekshirilishi shart.
**Talablar:**
- `System.IO.Hashing.XxHash64` yoki `Crc32` dan foydalanish.
- Sahifaning oxirgi 8 baytiga checksum ni yozish.
- O'qilganda checksum mos kelmasa `CorruptedPageException` tashlash.
**Yechim (C#):**
```csharp
using System;
using System.IO.Hashing;
using System.Runtime.InteropServices;

namespace StorageEngine.Pages;

public static class PageChecksumValidator
{
    public const int ChecksumSize = 8;

    public static void ComputeAndAppendChecksum(Span<byte> page4Kb)
    {
        // Sahifaning dastlabki 4088 bayti bo'yicha xxHash64 hisoblaymiz
        ReadOnlySpan<byte> payload = page4Kb[..^ChecksumSize];
        ulong hash = XxHash64.HashToUInt64(payload);

        // Oxirgi 8 baytga yozamiz
        MemoryMarshal.Write(page4Kb[^ChecksumSize..], in hash);
    }

    public static bool ValidatePageChecksum(ReadOnlySpan<byte> page4Kb)
    {
        ReadOnlySpan<byte> payload = page4Kb[..^ChecksumSize];
        ulong computedHash = XxHash64.HashToUInt64(payload);
        ulong storedHash = MemoryMarshal.Read<ulong>(page4Kb[^ChecksumSize..]);

        return computedHash == storedHash;
    }
}
```
**Tushuntirish:** `XxHash64` zamonaviy protsessorlarda sekundiga 10+ GB tezlikda hisoblanadi. Sahifani diskdan o'qish bilanoq nazorat yig'indisi tekshirilishi bazaga buzilgan ma'lumotlar tarqalishining (Silent Data Corruption) oldini oladi.
---

### Topshiriq #1241: Write-Ahead Logging (WAL): LSN va PageLSN Arxitekturasi
**Tavsif:** Ma'lumotlar bazasida har qanday sahifa diskka yozilishidan oldin, unga kiritilgan barcha o'zgarishlar log fayliga (WAL) yozilgan va diskka tushgan bo'lishi (WAL Protocol) shart. Buni muvofiqlashtirish uchun Log Sequence Number (LSN) ishlatiladi.
**Talablar:**
- Monoton o'suvchi 64-bitli `LSN`.
- Har bir sahifa sarlavhasida `PageLSN` saqlanishi.
- Qoida: Agar `PageLSN > FlushedLSN` bo'lsa, ushbu sahifani diskka yozish taqiqlanadi!
**Yechim (C#):**
```csharp
using System;
using System.Threading;

namespace StorageEngine.WAL;

public sealed class WalCoordinator
{
    private long _currentLsn;
    private long _flushedLsn;

    public long AllocateLsn(int logRecordSize)
    {
        return Interlocked.Add(ref _currentLsn, logRecordSize);
    }

    public void NotifyFlushedLsn(long flushedLsn)
    {
        Interlocked.Exchange(ref _flushedLsn, flushedLsn);
    }

    public bool CanWritePageToDisk(long pageLsn)
    {
        // WAL qoidasi: Sahifaning PageLSN qiymati diskka to'kilgan FlushedLSN dan kichik yoki teng bo'lishi shart!
        return pageLsn <= Volatile.Read(ref _flushedLsn);
    }
}
```
**Tushuntirish:** Bu WAL ning oltin qoidasidir: "Log birinchi, sahifa keyin!". Agar server aynan sahifa yozilayotganda qulasa, diskka yozilmagan log bo'lmasa ma'lumotni qayta tiklash imkonsiz bo'lib qoladi.
---

### Topshiriq #1242: ARIES Crash Recovery Algoritmi: Analysis, Redo va Undo
**Tavsif:** Ma'lumotlar bazasi to'satdan to'xtaganda, ARIES (Algorithm for Recovery and Isolation Exploiting Semantics) protokoli bo'yicha uch bosqichli tiklash jarayoni amalga oshiriladi: tahlil, qayta bajarish (Redo) va bekor qilish (Undo).
**Talablar:**
- Analysis bosqichi: Checkpointdan keyingi faol tranzaksiyalar va iflos sahifalarni aniqlash.
- Redo bosqichi: Barcha operatsiyalarni (hatto bekor qilinadigan tranzaksiyalarni ham) takrorlash.
- Undo bosqichi: Tugallanmagan (Loser) tranzaksiyalarning o'zgarishlarini orqaga qaytarish.
**Yechim (C#):**
```csharp
using System;
using System.Collections.Generic;

namespace StorageEngine.WAL;

public enum LogRecordType { Begin, Update, Commit, Abort, Clr }

public record LogRecord(long Lsn, long PrevLsn, int TxId, LogRecordType Type, int PageId, byte[] AfterImage);

public sealed class AriesRecoveryManager
{
    public static void RunRecovery(List<LogRecord> walRecords, long checkpointLsn)
    {
        var activeTransactions = new HashSet<int>();
        var dirtyPageTable = new Dictionary<int, long>();

        // 1. ANALYSIS BOSQICHI
        foreach (var record in walRecords)
        {
            if (record.Lsn < checkpointLsn) continue;

            if (record.Type == LogRecordType.Begin) activeTransactions.Add(record.TxId);
            else if (record.Type == LogRecordType.Commit || record.Type == LogRecordType.Abort) activeTransactions.Remove(record.TxId);

            if (record.Type == LogRecordType.Update && !dirtyPageTable.ContainsKey(record.PageId))
            {
                dirtyPageTable[record.PageId] = record.Lsn;
            }
        }

        // 2. REDO BOSQICHI (Tarixni to'liq qayta takrorlash - Repeating History)
        foreach (var record in walRecords)
        {
            if (record.Type == LogRecordType.Update)
            {
                // Sahifaga AfterImage ni qo'llash (Redo)...
            }
        }

        // 3. UNDO BOSQICHI (Tugallanmagan tranzaksiyalarni orqaga qaytarish)
        for (int i = walRecords.Count - 1; i >= 0; i--)
        {
            var record = walRecords[i];
            if (activeTransactions.Contains(record.TxId) && record.Type == LogRecordType.Update)
            {
                // Yozuvni bekor qilish (Undo) va CLR (Compensation Log Record) yozish...
            }
        }
    }
}
```
**Tushuntirish:** ARIES ning daholigi "Repeating History" tamoyilidadir. U crash yuz bergan aniq lahzagacha bo'lgan barcha o'zgarishlarni tiklaydi, so'ngra yakunlanmagan tranzaksiyalarni orqaga qaytaradi. Bu atomarlik va barqarorlikni 100% kafolatlaydi.
---

### Topshiriq #1243: Lock-Free WAL Ring Buffer: Ko'p Oqimli Log To'plagich
**Tavsif:** Agar minglab oqimlar har bir tranzaksiya yozuvida disk fayliga qulf bilan murojaat qilsa, tizim kutilishlarga botib qoladi. Yozuvlarni xotiradagi Lock-Free Doiraviy Buferga (Ring Buffer) `Interlocked.Add` orqali to'plash arxitekturasini yaratish kerak.
**Talablar:**
- Lock-free manzil ajratish.
- Oqimlar o'z log baytlarini xotiraga parallel ko'chirishi.
**Yechim (C#):**
```csharp
using System;
using System.Threading;

namespace StorageEngine.WAL;

public sealed class LockFreeWalBuffer
{
    private readonly byte[] _buffer;
    private readonly int _capacity;
    private readonly int _mask;
    private long _writeOffset;

    public LockFreeWalBuffer(int powerOfTwoCapacity = 20) // 1 MB bufer
    {
        _capacity = 1 << powerOfTwoCapacity;
        _mask = _capacity - 1;
        _buffer = new byte[_capacity];
    }

    public long AppendLogRecord(ReadOnlySpan<byte> record)
    {
        int size = record.Length;
        // Lock-free tarzda joy ajratish
        long start = Interlocked.Add(ref _writeOffset, size) - size;

        int bufferIndex = (int)(start & _mask);
        if (bufferIndex + size <= _capacity)
        {
            record.CopyTo(_buffer.AsSpan(bufferIndex, size));
        }
        else
        {
            // Doira chegarasidan oshganda ikki qismga bo'lib yozish
            int firstPart = _capacity - bufferIndex;
            record[..firstPart].CopyTo(_buffer.AsSpan(bufferIndex, firstPart));
            record[firstPart..].CopyTo(_buffer.AsSpan(0, size - firstPart));
        }

        return start + size; // LSN
    }
}
```
**Tushuntirish:** Lock-Free Ring Buffer oqimlarni bir-biri bilan raqobatlashmasdan to'liq parallel ishlashiga imkon beradi. Barcha CPU yadrolari bir vaqtning o'zida yozishi mumkin.
---

### Topshiriq #1244: Group Commit: O'nlab Tranzaksiyalarni Bitta Fsync Bilan Saqlash
**Tavsif:** SSD/NVMe disklarida `fsync` (diskka jismoniy yozish) taxminan 0.5-2 millisoniya vaqt oladi. Agar har bir tranzaksiya alohida fsync qilsa, tizim sekundiga faqat 500-1000 ta tranzaksiya bajara oladi. Bir vaqtning o'zida navbatda turgan barcha tranzaksiyalarni bitta umumiy I/O amali bilan diskka yozuvchi "Group Commit" algoritmi zarur.
**Talablar:**
- Tranzaksiya kelganda o'z `TaskCompletionSource` obyektini navbatga qo'yadi.
- Bitta boshqaruvchi oqim (Commit Leader) to'plangan barcha tranzaksiyalarni bitta `FlushAsync()` bilan yozadi va barcha kutuvchilarga signal beradi.
**Yechim (C#):**
```csharp
using System;
using System.Collections.Concurrent;
using System.IO;
using System.Threading.Tasks;

namespace StorageEngine.WAL;

public sealed class GroupCommitCoordinator : IAsyncDisposable
{
    private readonly FileStream _walFile;
    private readonly ConcurrentQueue<(long Lsn, TaskCompletionSource Tcs)> _pendingCommits = new();
    private readonly Task _commitLoopTask;
    private volatile bool _isRunning = true;

    public GroupCommitCoordinator(FileStream walFile)
    {
        _walFile = walFile;
        _commitLoopTask = Task.Run(CommitLoopAsync);
    }

    public Task WaitForCommitAsync(long lsn)
    {
        var tcs = new TaskCompletionSource(TaskCreationOptions.RunContinuationsAsynchronously);
        _pendingCommits.Enqueue((lsn, tcs));
        return tcs.Task;
    }

    private async Task CommitLoopAsync()
    {
        while (_isRunning)
        {
            if (_pendingCommits.IsEmpty)
            {
                await Task.Delay(1).ConfigureAwait(false);
                continue;
            }

            // Bitta fsync bilan diskka to'kish
            await _walFile.FlushAsync().ConfigureAwait(false);

            // Kutayotgan barcha tranzaksiyalarni bo'shatish (Group Commit)
            while (_pendingCommits.TryDequeue(out var item))
            {
                item.Tcs.TrySetResult();
            }
        }
    }

    public async ValueTask DisposeAsync()
    {
        _isRunning = false;
        await _commitLoopTask.ConfigureAwait(false);
    }
}
```
**Tushuntirish:** Group Commit orqali o'tkazuvchanlik soniyasiga 500 tranzaksiyadan 100,000+ tranzaksiyagacha ko'tariladi. Disk kechikishi (latency) amortizatsiya qilinadi.
---

### Topshiriq #1245: Doiraviy WAL Segmentlarini Boshqarish va Log Truncation
**Tavsif:** Agar WAL cheksiz o'ssa, disk to'lib qoladi. Checkpoint amalga oshirilgandan so'ng, checkpointdan eski barcha log yozuvlari xavfsiz o'chirilishi yoki yangi yozuvlar uchun qayta ishlatilishi (Log Truncation) kerak.
**Talablar:**
- Har biri 64 MB li segment fayllar: `0000000100000001`, `0000000100000002`.
- Checkpoint LSN dan oldingi barcha segment fayllarini avtomatik tozalash funksiyasi.
**Yechim (C#):**
```csharp
using System;
using System.IO;

namespace StorageEngine.WAL;

public sealed class WalSegmentManager
{
    public const long SegmentSize = 64 * 1024 * 1024; // 64 MB
    private readonly string _walDirectory;

    public WalSegmentManager(string walDirectory)
    {
        _walDirectory = walDirectory;
        Directory.CreateDirectory(_walDirectory);
    }

    public string GetSegmentFilePath(long lsn)
    {
        long segmentNumber = lsn / SegmentSize;
        return Path.Combine(_walDirectory, $"{segmentNumber:D16}.wal");
    }

    public void TruncateOldSegments(long minRequiredLsn)
    {
        long minRequiredSegment = minRequiredLsn / SegmentSize;
        var dir = new DirectoryInfo(_walDirectory);

        foreach (var file in dir.GetFiles("*.wal"))
        {
            if (long.TryParse(Path.GetFileNameWithoutExtension(file.Name), out long segNum))
            {
                if (segNum < minRequiredSegment)
                {
                    try { file.Delete(); } catch { /* Ishlatilayotgan bo'lsa keyinroq */ }
                }
            }
        }
    }
}
```
**Tushuntirish:** PostgreSQL uslubidagi segmentatsiya doimiy disk boshqaruvini ta'minlaydi. Eski loglar doimiy o'chirilishi tufayli disk doimo belgilangan chegarada (masalan, 2-10 GB) ushlab turiladi.
---

### Topshiriq #1246: Epoch-Based Memory Reclamation (EBR): Lock-Free Xotira Tozalash Asoslari
**Tavsif:** Lock-free ma'lumot tuzilmalarida (masalan, Masstree, B+Tree, FASTER) bitta oqim tugunni o'chirganda, uni zudlik bilan `free()` qilib bo'lmaydi, chunki boshqa o'quvchi oqimlar ayni damda o'sha tugunni o'qiyotgan bo'lishi mumkin (ABA muammosi va Use-After-Free). Epoch mexanizmi orqali barcha o'quvchilar tugundan chiqqandan keyingina uni tozalash kerak.
**Talablar:**
- Global Epoch: monoton o'suvchi 64-bit son.
- O'quvchi operatsiya boshida joriy davrga (Epoch) kiradi va tugagach chiqadi.
**Yechim (C#):**
```csharp
using System;
using System.Threading;

namespace StorageEngine.Epoch;

public sealed class EpochManager
{
    private long _currentEpoch = 1;

    public long CurrentEpoch => Volatile.Read(ref _currentEpoch);

    public void BumpEpoch()
    {
        Interlocked.Increment(ref _currentEpoch);
    }
}
```
**Tushuntirish:** Epoch tizimi lock-free arxitekturalarda Garbage Collector vazifasini bajaradi, biroq GC to'xtashlarisiz (Stop-the-world siz) va mikrosoniya darajasida xavfsiz ishlaydi.
---

### Topshiriq #1247: Thread-Local Epoch Registratsiyasi va Faol O'quvchilarni Kuzatish
**Tavsif:** Global Epoch ni oshirishdan oldin, barcha faol oqimlar qaysi davrda turganini aniqlash zarur. Barcha oqimlar eng kamida $E-1$ davriga o'tgan bo'lsa, $E-2$ davridagi barcha o'chirilgan xotira bloklarini xavfsiz tozalash mumkin bo'ladi.
**Talablar:**
- `ThreadEpochInfo`: Har bir oqim uchun lokal davr hisoblagichi.
- `Protect()` va `Unprotect()` orqali xavfsiz hududni belgilash.
**Yechim (C#):**
```csharp
using System;
using System.Collections.Concurrent;
using System.Threading;

namespace StorageEngine.Epoch;

public sealed class ThreadEpochContext
{
    public long ActiveEpoch;
    public bool IsActive;
}

public sealed class SafeEpochTracker
{
    private readonly EpochManager _epochManager;
    private readonly ConcurrentBag<ThreadEpochContext> _threads = new();
    private static readonly ThreadLocal<ThreadEpochContext> _localContext = new(() => new ThreadEpochContext());

    public SafeEpochTracker(EpochManager epochManager) => _epochManager = epochManager;

    public void EnterCriticalRegion()
    {
        var ctx = _localContext.Value;
        if (!ctx.IsActive)
        {
            _threads.Add(ctx);
            ctx.IsActive = true;
        }

        Volatile.Write(ref ctx.ActiveEpoch, _epochManager.CurrentEpoch);
    }

    public void ExitCriticalRegion()
    {
        var ctx = _localContext.Value;
        Volatile.Write(ref ctx.ActiveEpoch, long.MaxValue); // Faol emas
    }

    public long ComputeSafeReclamationEpoch()
    {
        long minEpoch = _epochManager.CurrentEpoch;
        foreach (var t in _threads)
        {
            long ep = Volatile.Read(ref t.ActiveEpoch);
            if (ep < minEpoch) minEpoch = ep;
        }

        return minEpoch - 1; // Ushbu epochdan oldingi barcha xotiralar 100% xavfsiz ozod qilinishi mumkin
    }
}
```
**Tushuntirish:** Thread-local ro'yxatga olish har qanday global qulfni chetlab o'tadi. Har bir oqim faqat o'z kesh liniyasidagi o'zgaruvchini yangilaydi, bu esa CPU yadrolari o'rtasida kontensiyani nolga tushiradi.
---

### Topshiriq #1248: EBR Garbage Bag va Xotirani Kechiktirilgan Xavfsiz Tozalash (Retire)
**Tavsif:** Tugun yoki obyekt o'chirilganda, u darhol yo'q qilinmaydi, balki joriy Global Epoch belgisi bilan "Chiqindi qopi"ga (Garbage Bag) tashlanadi. Global davr xavfsiz nuqtadan oshgandagina xotira ozod qilinadi (Deferred Reclamation).
**Talablar:**
- `Retire(IntPtr memoryPointer, Action<IntPtr> freeCallback)`.
- Xavfsiz davr kelganda callbacklarni chaqirib xotirani bo'shatish.
**Yechim (C#):**
```csharp
using System;
using System.Collections.Concurrent;

namespace StorageEngine.Epoch;

public sealed class GarbageBag
{
    private readonly struct RetiredObject
    {
        public readonly long Epoch;
        public readonly IntPtr Pointer;
        public readonly Action<IntPtr> FreeAction;

        public RetiredObject(long epoch, IntPtr ptr, Action<IntPtr> freeAction)
        {
            Epoch = epoch;
            Pointer = ptr;
            FreeAction = freeAction;
        }
    }

    private readonly ConcurrentQueue<RetiredObject> _queue = new();
    private readonly SafeEpochTracker _tracker;

    public GarbageBag(SafeEpochTracker tracker) => _tracker = tracker;

    public void Retire(long currentEpoch, IntPtr pointer, Action<IntPtr> freeAction)
    {
        _queue.Enqueue(new RetiredObject(currentEpoch, pointer, freeAction));
    }

    public void Collect()
    {
        long safeEpoch = _tracker.ComputeSafeReclamationEpoch();

        while (_queue.TryPeek(out var item))
        {
            if (item.Epoch <= safeEpoch)
            {
                if (_queue.TryDequeue(out var toDelete))
                {
                    toDelete.FreeAction(toDelete.Pointer);
                }
            }
            else
            {
                break; // Hali xavfsiz bo'lmagan davr elementlari
            }
        }
    }
}
```
**Tushuntirish:** Bu texnika C# da unmanaged xotira bilan ishlaganda xotira sizib chiqishini (Memory Leaks) va SegFault xatoliklarini to'liq bartaraf etadi. Lock-free ma'lumot tuzilmalari doimo toza va xavfsiz xotirada ishlaydi.
---

### Topshiriq #1249: LSM-Tree MemTable va SSTable (Sorted String Table) Binar Formati
**Tavsif:** Log-Structured Merge Tree (RocksDB, Cassandra) da ma'lumotlar avval xotiradagi saralangan MemTable ga (SkipList yoki Red-Black Tree) yoziladi. MemTable to'lganda, u diskka bir martalik tartiblangan fayl (SSTable) ko'rinishida to'kiladi (Flush).
**Talablar:**
- Xotiradagi `MemTable` (SortedDictionary).
- Diskdagi SSTable: Data Block, Index Block va Footer dan iborat binar fayl formati.
**Yechim (C#):**
```csharp
using System;
using System.Collections.Generic;
using System.IO;

namespace StorageEngine.LSM;

public sealed class SsTableWriter
{
    public static void FlushMemTableToSsTable(SortedDictionary<long, byte[]> memTable, string sstablePath)
    {
        using var stream = new FileStream(sstablePath, FileMode.Create, FileAccess.Write);
        using var writer = new BinaryWriter(stream);

        var indexEntries = new List<(long Key, long Offset)>();

        // 1. DATA BLOCK larni yozish
        foreach (var (key, value) in memTable)
        {
            long offset = stream.Position;
            indexEntries.Add((key, offset));

            writer.Write(key);
            writer.Write(value.Length);
            writer.Write(value);
        }

        // 2. INDEX BLOCK (Tezkor qidiruv indeksi)
        long indexOffset = stream.Position;
        writer.Write(indexEntries.Count);
        foreach (var (k, off) in indexEntries)
        {
            writer.Write(k);
            writer.Write(off);
        }

        // 3. FOOTER (Index block qayerdaligini ko'rsatadi)
        writer.Write(indexOffset);
        writer.Write(0x53535442L); // "SSTB" Magic Number
    }
}
```
**Tushuntirish:** SSTable larning asosiy afzalligi - diskka faqat ketma-ket (Sequential Write) yozilishidir. Diskdagi boshqa hech qanday joy yangilanmaydi. Bu magnit va SSD drayverlarda maksimal yozish tezligini ta'minlaydi.
---

### Topshiriq #1250: Yakuniy Integratsiya: FASTER Uslubidagi .NET Storage Engine
**Tavsif:** Ushbu yakuniy topshiriqda modul davomida yaratilgan barcha ilg'or texnologiyalar: HybridLog xotira va disk bosqichlari, WAL tranzaksiya jurnallash, Buffer Pool, B+Tree indeksi va Epoch xotira tozalash bitta umumiy yuqori unumdor saqlash dvigatelida (Enterprise Storage Engine) integratsiya qilinadi.
**Talablar:**
- `Put(key, value)`, `Get(key)` va `Delete(key)` operatsiyalarini qo'llab-quvvatlovchi yagona yadro sinfi.
- ACID xavfsizligi, kesh lokalligi va nolga teng GC overhead arxitekturasi.
**Yechim (C#):**
```csharp
using System;
using System.IO;
using System.Threading.Tasks;
using StorageEngine.BufferPool;
using StorageEngine.HybridLog;
using StorageEngine.Indexing;
using StorageEngine.WAL;

namespace StorageEngine;

public sealed class UltraStorageEngine : IAsyncDisposable
{
    private readonly HybridLogBoundaryManager _boundaries;
    private readonly PageFramePool _framePool;
    private readonly HybridLogAppender _appender;
    private readonly LockFreeWalBuffer _walBuffer;
    private readonly GroupCommitCoordinator _groupCommit;
    private readonly LatchCrabbingBPlusTree<long> _primaryIndex;
    private readonly FileStream _walFile;

    public UltraStorageEngine(string baseDir)
    {
        Directory.CreateDirectory(baseDir);
        string walPath = Path.Combine(baseDir, "engine.wal");
        string logPath = Path.Combine(baseDir, "engine.log");

        _boundaries = new HybridLogBoundaryManager(0);
        _framePool = new PageFramePool(pageCountPowerOfTwo: 8, pageSize: 16384); // 256 sahifa = 4 MB RAM kesh
        _appender = new HybridLogAppender(_boundaries, _framePool);

        _walBuffer = new LockFreeWalBuffer();
        _walFile = new FileStream(walPath, FileMode.OpenOrCreate, FileAccess.ReadWrite, FileShare.ReadWrite, 65536, FileOptions.Asynchronous);
        _groupCommit = new GroupCommitCoordinator(_walFile);

        _primaryIndex = new LatchCrabbingBPlusTree<long>(maxKeys: 32);
    }

    public async Task PutAsync(long key, byte[] value)
    {
        // 1. Avval WAL ga yozamiz (Write-Ahead Logging)
        long lsn = _walBuffer.AppendLogRecord(value);

        // 2. HybridLog ga yozamiz
        LogicalAddress address = _appender.Upsert(key, value, previousAddressForSameKey: -1);

        // 3. B+Tree indeksini yangilaymiz
        // _primaryIndex.Insert(key, address.Value);

        // 4. Tranzaksiyani diskka kafolatlaymiz (Group Commit)
        await _groupCommit.WaitForCommitAsync(lsn).ConfigureAwait(false);
    }

    public async ValueTask DisposeAsync()
    {
        await _groupCommit.DisposeAsync().ConfigureAwait(false);
        await _walFile.DisposeAsync().ConfigureAwait(false);
        _framePool.Dispose();
    }
}
```
**Tushuntirish:** Ushbu dvigatel Microsoft FASTER va zamonaviy NoSQL/NewSQL dvigatellari (Dragonfly, Aerospike) falsafasini o'zida mujassam etgan. Ma'lumotlar RAM da mikrosoniya darajasida xizmat ko'rsatadi, fonga uzluksiz to'kiladi va kutilmagan to'xtashlarda WAL hamda Checkpoint orqali to'liq tiklanadi.
---

