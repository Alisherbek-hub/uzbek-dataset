# Khorazmiy AI: Python - Modul 25
## Mavzu: Ma'lumotlar Bazasi Ichki Dvigatellari (Storage Engines): LSM-Trees (MemTable, WAL, SSTable, Leveled Compaction), B+Tree noldan qurish, Bitcask Log-Structured Storage, Bloom Filters va Buffer Pool Manager


---

### Topshiriq #1201: MemTable: Xotirada tartiblangan SkipList ma'lumotlar strukturasi
**Tavsif:** LSM-Tree (Log-Structured Merge-Tree) saqlash dvigatelida ma'lumotlarni xotirada doimo tartiblangan (sorted) holatda ushlab turish va $O(\log N)$ vaqtda kiritish hamda qidirish uchun SkipList tuzilmasini yaratish lozim.
**Talablar:** Ehtimollik asosidagi darajalar (probabilistic levels, $p=0.5$), maksimal balandlik (MAX_LEVEL=16), `put`, `get`, va `contains` metodlarini to'liq implementatsiya qilish.
**Yechim (Python):**
```python
import random

class SkipNode:
    def __init__(self, key, value, level):
        self.key = key
        self.value = value
        # Har bir daraja bo'yicha oldinga ko'rsatkichlar massivi
        self.forward = [None] * level

class SkipListMemTable:
    MAX_LEVEL = 16
    P = 0.5

    def __init__(self):
        self.header = SkipNode(None, None, self.MAX_LEVEL)
        self.level = 1
        self.size_bytes = 0

    def _random_level(self) -> int:
        lvl = 1
        while random.random() < self.P and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def put(self, key: bytes, value: bytes):
        update = [None] * self.MAX_LEVEL
        current = self.header

        for i in range(self.level - 1, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current and current.key == key:
            # Mavjud kalit qiymatini yangilash
            self.size_bytes += len(value) - len(current.value)
            current.value = value
        else:
            new_level = self._random_level()
            if new_level > self.level:
                for i in range(self.level, new_level):
                    update[i] = self.header
                self.level = new_level

            new_node = SkipNode(key, value, new_level)
            for i in range(new_level):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node

            self.size_bytes += len(key) + len(value) + (new_level * 8)

    def get(self, key: bytes):
        current = self.header
        for i in range(self.level - 1, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]
        if current and current.key == key:
            return current.value
        return None
```
**Tushuntirish:** SkipList qizil-qora daraxtlarga (Red-Black Tree) nisbatan ancha sodda va amalda tezroq ishlaydi, chunki murakkab daraxtni aylantirish (rebalancing) operatsiyalarini talab qilmaydi. Ehtimollik asosidagi balandlik taqsimoti qidirish va kiritish amallarining o'rtacha murakkabligini $O(\log N)$ bo'lishini ta'minlaydi.


---

### Topshiriq #1202: Write-Ahead Log (WAL): Crash recovery uchun append-only jurnal va CRC32 cheksum
**Tavsif:** Xotiradagi MemTable ga ma'lumot yozishdan oldin elektr toki o'chganda ma'lumotlar yo'qolmasligi (Durability) uchun har bir operatsiyani diskdagi ketma-ket jurnalga (WAL) yaxlitlik nazorati bilan yozish lozim.
**Talablar:** Binar format: `[CRC32: 4 bayt][KeyLen: 2 bayt][ValLen: 4 bayt][Type: 1 bayt][Key][Value]`, zlib CRC32 hisoblash va tasdiqlash.
**Yechim (Python):**
```python
import os
import struct
import zlib

class WriteAheadLog:
    # 4B CRC + 2B KeyLen + 4B ValLen + 1B OpType (0=Delete, 1=Put)
    HEADER_FORMAT = ">IIHB"
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.file = open(filepath, "a+b")

    def append(self, op_type: int, key: bytes, value: bytes = b""):
        key_len = len(key)
        val_len = len(value)
        payload = key + value
        
        # Payload yaxlitligi uchun CRC32 cheksum
        crc = zlib.crc32(payload) & 0xFFFFFFFF
        
        # Binar sarlavhani paketlash
        header = struct.pack(self.HEADER_FORMAT, crc, val_len, key_len, op_type)
        
        self.file.write(header + payload)
        self.file.flush()
        os.fsync(self.file.fileno()) # Diskka majburiy yozish

    def close(self):
        self.file.close()
```
**Tushuntirish:** WAL append-only (faqat oxiriga qo'shish) printsipida ishlaydi. Qattiq disklarda (HDD va NVMe SSD) ketma-ket yozish (sequential write) tasodifiy yozishdan 100 barobargacha tezroq bo'ladi. `os.fsync` operatsion tizim buferini majburiy ravishda jismoniy flesh-xotiraga tushiradi.


---

### Topshiriq #1203: MemTable hajmi chegaralanganda (Flush threshold) diskka immutabel holatda yozish
**Tavsif:** MemTable xotira hajmi belgilangan chegaraga (masalan 4 MB yoki 64 MB) yetganda, yangi yozishlarni to'xtatmaslik uchun faol MemTable o'zgarmas (immutable) holatga o'tkazilib, fonda diskdagi SSTable ga to'kilishi (Flush) kerak.
**Talablar:** Threshold tekshiruvi, faol va muzlatilgan (immutable) xotira hovuzlarini ajratish, atomik almashish.
**Yechim (Python):**
```python
class MemTableManager:
    def __init__(self, flush_threshold_bytes: int = 4 * 1024 * 1024):
        self.flush_threshold = flush_threshold_bytes
        self.active_memtable = SkipListMemTable()
        self.immutable_memtable = None

    def put(self, key: bytes, value: bytes) -> bool:
        self.active_memtable.put(key, value)
        
        # Agar chegara to'lsa va avvalgi flush tugagan bo'lsa
        if self.active_memtable.size_bytes >= self.flush_threshold and self.immutable_memtable is None:
            # Faol MemTable ni muzlatish
            self.immutable_memtable = self.active_memtable
            self.active_memtable = SkipListMemTable()
            return True # Flush signali
        return False

    def get(self, key: bytes):
        # Avval faol xotiradan, keyin immutable xotiradan qidiramiz
        val = self.active_memtable.get(key)
        if val is not None:
            return val
        if self.immutable_memtable:
            return self.immutable_memtable.get(key)
        return None
```
**Tushuntirish:** Ushbu ikki qatlamli xotira modeli LSM-Tree ning uzluksiz yuqori yozish tezligini (high write throughput) kafolatlaydi. Diskka yozish jarayoni sekin bo'lsa ham, mijozlar yangi bo'shatilgan faol MemTable ga o'z tranzaksiyalarini hech qanday kechikishsiz yozishda davom etaveradi.


---

### Topshiriq #1204: WAL segmentatsiyasi va eskirgan loglarni tozalash (Log Truncation)
**Tavsif:** MemTable diskka SSTable sifatida to'liq yozib bo'lingach, unga tegishli WAL yozuvlari ortiqcha bo'lib qoladi va diskni to'ldirmaslik uchun o'chirilishi lozim.
**Talablar:** Segment nomerlash (`wal_00001.log`), flush yakunlangach eski segmentlarni xavfsiz o'chirish yoki arxivlash.
**Yechim (Python):**
```python
import os
import glob

class WalSegmentManager:
    def __init__(self, wal_dir: str):
        self.wal_dir = wal_dir
        os.makedirs(wal_dir, exist_ok=True)
        self.current_segment_id = self._get_latest_segment_id() + 1
        self.active_wal = WriteAheadLog(self._segment_path(self.current_segment_id))

    def _segment_path(self, seg_id: int) -> str:
        return os.path.join(self.wal_dir, f"wal_{seg_id:06d}.log")

    def _get_latest_segment_id(self) -> int:
        files = glob.glob(os.path.join(self.wal_dir, "wal_*.log"))
        if not files:
            return 0
        ids = [int(os.path.basename(f).split("_")[1].split(".")[0]) for f in files]
        return max(ids)

    def rotate(self) -> int:
        self.active_wal.close()
        old_id = self.current_segment_id
        self.current_segment_id += 1
        self.active_wal = WriteAheadLog(self._segment_path(self.current_segment_id))
        return old_id

    def delete_segments_up_to(self, flushed_segment_id: int):
        for f in glob.glob(os.path.join(self.wal_dir, "wal_*.log")):
            seg_id = int(os.path.basename(f).split("_")[1].split(".")[0])
            if seg_id <= flushed_segment_id:
                try:
                    os.remove(f)
                except OSError:
                    pass
```
**Tushuntirish:** WAL fayllarini cheksiz o'sishiga yo'l qo'ymaslik log truncation orqali amalga oshiriladi. Har safar MemTable diskka SSTable bo'lib flush qilinganda, yangi WAL segmenti ochiladi va bazaning qat'iy holati (checkpoint) qayd etilib, eski loglar o'chiriladi.


---

### Topshiriq #1205: Avariyadan keyin WAL orqali xotirani to'liq tiklash (Crash Recovery Engine)
**Tavsif:** Tizim serveri kutilmaganda o'chib qolsa, qayta ishga tushish vaqtida barcha WAL segmentlarini noldan o'qib, buzilmagan yozuvlarni MemTable ga qayta tiklash zarur.
**Talablar:** Buzilgan (corrupt) oxirgi yozuvlarni aniqlash, CRC32 tekshiruvi orqali xatoliklarni ajratish va toza tiklash.
**Yechim (Python):**
```python
class WalRecoveryEngine:
    @staticmethod
    def recover_from_file(filepath: str, memtable: SkipListMemTable) -> int:
        recovered_count = 0
        if not os.path.exists(filepath):
            return 0

        with open(filepath, "rb") as f:
            while True:
                header_bytes = f.read(WriteAheadLog.HEADER_SIZE)
                if len(header_bytes) < WriteAheadLog.HEADER_SIZE:
                    break # Fayl oxiri

                crc, val_len, key_len, op_type = struct.unpack(
                    WriteAheadLog.HEADER_FORMAT, header_bytes
                )

                payload = f.read(key_len + val_len)
                if len(payload) < (key_len + val_len):
                    # Tugallanmagan yozuv (chala yozilgan)
                    break

                # CRC yaxlitligini tekshirish
                if (zlib.crc32(payload) & 0xFFFFFFFF) != crc:
                    print(f"Ogohlantirish: {filepath} da buzilgan yozuv aniqlandi, to'xtatildi")
                    break

                key = payload[:key_len]
                value = payload[key_len:]

                if op_type == 1: # PUT
                    memtable.put(key, value)
                elif op_type == 0: # DELETE
                    memtable.put(key, b"__TOMBSTONE__")

                recovered_count += 1

        return recovered_count
```
**Tushuntirish:** Crash Recovery dvigateli ma'lumotlar bazasi ishonchliligining (Reliability) kafolatidir. Elektr o'chgan paytda oxirgi yozuv yarimta yozilib qolishi mumkin. CRC tekshiruvi buzilgan yarimta baytlarni darhol fosh qiladi va bazani xavfsiz oxirgi izchil holatgacha tiklaydi.


---

### Topshiriq #1206: O'chirish amallarini boshqarish: Qabr toshlari (Tombstones) va kechiktirilgan o'chirish
**Tavsif:** LSM-Tree dvigatelida diskdagi ma'lumotlarni darhol jismoniy o'chirish imkonsiz (chunki fayllar o'zgarmas). Shu sababli o'chirish amali 'Qabr toshi' (Tombstone) markeri orqali amalga oshiriladi.
**Talablar:** Tombstone konstantasini belgilash, `delete` metodida tombstone yozish, `get` paytida o'chirilgan deb qaytarish.
**Yechim (Python):**
```python
TOMBSTONE_MARKER = b"__DELETED_TOMBSTONE_V1__"

class LsmKeyValueStore:
    def __init__(self):
        self.memtable = SkipListMemTable()

    def put(self, key: str, value: str):
        self.memtable.put(key.encode("utf-8"), value.encode("utf-8"))

    def delete(self, key: str):
        # Jismoniy o'chirish o'rniga qabr toshi yozamiz
        self.memtable.put(key.encode("utf-8"), TOMBSTONE_MARKER)

    def get(self, key: str):
        raw_val = self.memtable.get(key.encode("utf-8"))
        if raw_val is None or raw_val == TOMBSTONE_MARKER:
            return None # Kalit mavjud emas yoki o'chirilgan
        return raw_val.decode("utf-8")
```
**Tushuntirish:** Tombstone LSM-Tree ning o'ziga xos arxitektura tamoyilidir. O'chirish ham xuddi yangi ma'lumot kiritish kabi ketma-ket yoziladi. Eski ma'lumotlar esa keyinchalik Compaction (zichlashtirish) jarayonida to'liq yo'q qilinadi.


---

### Topshiriq #1207: MemTable iteratorlari: Diapazon bo'yicha qidiruv (Range Scan [start, end))
**Tavsif:** Foydalanuvchi ma'lum bir prefiks yoki oraliqdagi barcha kalitlarni (masalan `user:100` dan `user:200` gacha) tartiblangan holda o'qishi uchun samarali iterator zarur.
**Talablar:** SkipList bo'ylab `start_key` ni topish, `forward[0]` orqali ketma-ket harakatlanish va `end_key` ga yetganda to'xtash.
**Yechim (Python):**
```python
class MemTableIterator:
    def __init__(self, memtable: SkipListMemTable, start_key: bytes = None, end_key: bytes = None):
        self.end_key = end_key
        # Boshlang'ich nuqtaga o'tish
        current = memtable.header
        if start_key:
            for i in range(memtable.level - 1, -1, -1):
                while current.forward[i] and current.forward[i].key < start_key:
                    current = current.forward[i]
            self.current = current.forward[0]
        else:
            self.current = memtable.header.forward[0]

    def __iter__(self):
        return self

    def __next__(self):
        if not self.current:
            raise StopIteration
        if self.end_key and self.current.key >= self.end_key:
            raise StopIteration

        key, val = self.current.key, self.current.value
        self.current = self.current.forward[0] # 0-daraja bo'ylab ketma-ket yurish
        return key, val
```
**Tushuntirish:** SkipList ning 0-darajasi (bottom level) oddiy bog'langan ro'yxatdir (Linked List). Boshlang'ich nuqtani $O(\log N)$ da topgandan so'ng, keyingi elementlarni o'qish $O(1)$ tezlikda bo'ladi, bu esa Range Scan so'rovlarini nihoyatda tez bajaradi.


---

### Topshiriq #1208: Bir vaqtda o'qish va yozish: Immutable MemTable va faol MemTable ajratilishi
**Tavsif:** Flush vaqtida diskka yozilayotgan ma'lumotlar bilan yangi kiruvchi so'rovlar o'rtasida ziddiyat yuzaga kelmasligi uchun qulflar (locks) bilan ajratish kerak.
**Talablar:** `threading.Lock` yordamida himoyalash, o'qish amallari uchun bloklanmaydigan oqimlar.
**Yechim (Python):**
```python
import threading

class ThreadSafeMemTableRouter:
    def __init__(self):
        self.lock = threading.Lock()
        self.active = SkipListMemTable()
        self.flushing = None

    def put(self, key: bytes, value: bytes):
        with self.lock:
            self.active.put(key, value)

    def freeze_for_flush(self) -> SkipListMemTable:
        with self.lock:
            if self.flushing is not None:
                raise RuntimeError("Oldingi flush hali yakunlanmadi")
            self.flushing = self.active
            self.active = SkipListMemTable()
            return self.flushing

    def clear_flushed(self):
        with self.lock:
            self.flushing = None
```
**Tushuntirish:** Faol va o'zgarmas MemTable larni ajratish qulflanish vaqtini (lock contention) minimal darajaga tushiradi. Faqatgina havola (pointer) almashtirilayotgan bir necha nanosekund ichida qulf ushlanadi, og'ir disk amallari esa qulfdan tashqarida bajariladi.


---

### Topshiriq #1209: WAL fsync siyosatlari: always, every_second, no_sync (Chidamlilik vs Unumdorlik)
**Tavsif:** Har bir yozishda `fsync` qilish diskni sekinlashtiradi. MySQL/PostgreSQL kabi turli talablarga mos keluvchi chidamlilik siyosatlarini joriy etish lozim.
**Talablar:** Siyosatlar: `ALWAYS` (100% xavfsiz), `EVERY_SECOND` (muvozanatli), `NO_SYNC` (ultra-tezkor).
**Yechim (Python):**
```python
import time
import threading

class FsyncPolicy:
    ALWAYS = 1
    EVERY_SECOND = 2
    NO_SYNC = 3

class ConfigurableWal:
    def __init__(self, filepath: str, policy: int = FsyncPolicy.EVERY_SECOND):
        self.file = open(filepath, "a+b")
        self.policy = policy
        self.running = True

        if self.policy == FsyncPolicy.EVERY_SECOND:
            self.sync_thread = threading.Thread(target=self._background_syncer, daemon=True)
            self.sync_thread.start()

    def write_entry(self, data: bytes):
        self.file.write(data)
        if self.policy == FsyncPolicy.ALWAYS:
            self.file.flush()
            os.fsync(self.file.fileno())

    def _background_syncer(self):
        while self.running:
            time.sleep(1.0)
            try:
                self.file.flush()
                os.fsync(self.file.fileno())
            except OSError:
                break
```
**Tushuntirish:** Fsync siyosati ACID xususiyatlarining 'Durability' darajasini belgilaydi. `ALWAYS` har bir INSERT da disknikallani kutadi (100-500 IOPS). `EVERY_SECOND` esa sekundiga 100 000 ta operatsiyaga erishishga imkon beradi, biroq to'satdan elektr o'chganda maksimal 1 soniyalik ma'lumot yo'qolishi mumkin.


---

### Topshiriq #1210: Binary serialization: WAL yozuvlarini ixcham baytlar shaklida qadoqlash
**Tavsif:** Disk xotirasini tejash va I/O yuklamasini qisqartirish uchun yozuvlarni Varint (Variable Length Integer) formatida ixcham kodlash kerak.
**Talablar:** Protocol Buffers uslubidagi Varint kodlash algoritmi, 64-bitli sonlarni 1-10 bayt oralig'ida siqish.
**Yechim (Python):**
```python
class VarintEncoder:
    @staticmethod
    def encode_uint(val: int) -> bytes:
        result = bytearray()
        while val >= 0x80:
            result.append((val & 0x7F) | 0x80)
            val >>= 7
        result.append(val & 0x7F)
        return bytes(result)

    @staticmethod
    def decode_uint(stream) -> int:
        res = 0
        shift = 0
        while True:
            b = stream.read(1)
            if not b:
                raise EOFError
            byte_val = ord(b)
            res |= (byte_val & 0x7F) << shift
            if (byte_val & 0x80) == 0:
                break
            shift += 7
        return res
```
**Tushuntirish:** Standart 64-bit butun son har doim 8 bayt oladi. Varint algoritmi kichik sonlarni (masalan 15 sonini) atigi 1 baytda saqlaydi. Ko'p hollarda kalit va qiymat uzunliklari kichik bo'lgani sababli, Varint jurnali hajmini 40% gacha tejaydi.


---

### Topshiriq #1211: SSTable fayl formati: Data Block, Index Block, Footer va Magic number
**Tavsif:** SSTable (Sorted String Table) diskdagi o'zgarmas asosiy ma'lumotlar konteyneridir. Fayl so'ngida indeks joylashgan va tezkor o'qishga mos format yaratish kerak.
**Talablar:** Magic number `0x57746534` (LevelDB), Data Blocklar, Index Block va 48 baytlik Footer strukturasi.
**Yechim (Python):**
```python
class SSTableLayout:
    # LevelDB standarti: Magic raqami (8 bayt)
    MAGIC_NUMBER = 0xDB4775248B80FB57
    FOOTER_SIZE = 48

    @staticmethod
    def pack_footer(index_offset: int, index_size: int) -> bytes:
        # Metaindex va Index bloklari uchun BlockHandle
        # Format: IndexOffset (8B) + IndexSize (8B) + Magic (8B) + Padding (24B)
        footer = struct.pack(">QQQ", index_offset, index_size, SSTableLayout.MAGIC_NUMBER)
        padding = b"\x00" * (SSTableLayout.FOOTER_SIZE - len(footer))
        return footer + padding

    @staticmethod
    def unpack_footer(raw_bytes: bytes):
        if len(raw_bytes) != SSTableLayout.FOOTER_SIZE:
            raise ValueError("Footer hajmi noto'g'ri")
        offset, size, magic = struct.unpack(">QQQ", raw_bytes[:24])
        if magic != SSTableLayout.MAGIC_NUMBER:
            raise ValueError("Yaroqsiz SSTable magic raqami!")
        return offset, size
```
**Tushuntirish:** SSTable larda indeks har doim fayl oxirida joylashadi. Chunki ma'lumotlar diskka ketma-ket yozilayotganda barcha Data Bloklarning offsetlari faqat oxirida ma'lum bo'ladi. Footer orqali o'quvchi dastur fayl oxiridan 48 bayt o'qib, butun fayl indeksini xotiraga yuklaydi.


---

### Topshiriq #1212: SSTable Index Block: Sparse Index (siyrak indeks) orqali binar qidiruv
**Tavsif:** Har bir kalitni indeksga kiritish RAM ni to'ldirib yuboradi. Har 4KB blok uchun faqat oxirgi kalitni saqlovchi Siyrak Indeks (Sparse Index) yaratish lozim.
**Talablar:** Sparse Index yaratish, binary search (`bisect`) yordamida qaysi blokda kalit joylashganligini topish.
**Yechim (Python):**
```python
import bisect

class SparseIndex:
    def __init__(self):
        self.keys = []
        self.block_handles = [] # (offset, size)

    def add_entry(self, last_key_in_block: bytes, offset: int, size: int):
        self.keys.append(last_key_in_block)
        self.block_handles.append((offset, size))

    def find_block(self, target_key: bytes):
        # Binar qidiruv orqali mos keluvchi blokni aniqlash
        idx = bisect.bisect_left(self.keys, target_key)
        if idx < len(self.keys):
            return self.block_handles[idx]
        return None # Kalit mavjud diapazondan katta
```
**Tushuntirish:** Siyrak indekslash (Sparse Indexing) xotirani 99% ga tejaydi. 1 milliard yozuv bo'lganda ham, xotirada faqat 10 000 ta blok ko'rsatkichi saqlanadi. Dastur avval indeksdan blokni topadi, so'ng diskdan faqatgina bitta 4KB blokni o'qib qidiradi.


---

### Topshiriq #1213: SSTable ichida Prefix Compression (kalit prefikslarini siqish)
**Tavsif:** Tartiblangan kalitlar ko'pincha umumiy boshlanishga ega bo'ladi (masalan `user:profile:1001`, `user:profile:1002`). Kalit prefikslarini siqib saqlash zarur.
**Talablar:** Shared length (umumiy prefiks uzunligi) va Unshared length (qoldiq qism) formatida saqlash.
**Yechim (Python):**
```python
class PrefixCompressor:
    @staticmethod
    def common_prefix_len(k1: bytes, k2: bytes) -> int:
        min_len = min(len(k1), len(k2))
        for i in range(min_len):
            if k1[i] != k2[i]:
                return i
        return min_len

    @staticmethod
    def compress_key(prev_key: bytes, current_key: bytes):
        shared = PrefixCompressor.common_prefix_len(prev_key, current_key)
        unshared = current_key[shared:]
        return shared, len(unshared), unshared

    @staticmethod
    def decompress_key(prev_key: bytes, shared_len: int, unshared_part: bytes) -> bytes:
        return prev_key[:shared_len] + unshared_part
```
**Tushuntirish:** Prefiks siqish algoritmi tartiblangan satrlar bilan ishlaganda hayratlanarli darajada yuqori samaradorlik beradi. Takrorlanuvchi domen nomlari, URL lar yoki prefiksli ID larda SSTable o'lchami 50-70% gacha kichrayadi.


---

### Topshiriq #1214: SSTable Block Builder: 4KB bloklarga bo'lish va Snappy/ZSTD siqish
**Tavsif:** Data Bloklari qat'iy 4096 bayt (OS sahifasi) bo'yicha shakllantirilishi va har bir blok alohida siqilib (compression) diskka yozilishi lozim.
**Talablar:** Restart points (qayta tiklash nuqtalari), blok hajmi to'lganda siqish va xom baytlarni qaytarish.
**Yechim (Python):**
```python
class BlockBuilder:
    def __init__(self, target_block_size: int = 4096):
        self.target_size = target_block_size
        self.buffer = bytearray()
        self.prev_key = b""
        self.restarts = [0]
        self.counter = 0

    def add(self, key: bytes, value: bytes) -> bool:
        shared, unshared_len, unshared_bytes = PrefixCompressor.compress_key(self.prev_key, key)
        
        # Yozuv formati: SharedLen(1B) + UnsharedLen(2B) + ValLen(4B) + UnsharedKey + Val
        entry = struct.pack(">BHI", shared, unshared_len, len(value)) + unshared_bytes + value
        self.buffer.extend(entry)
        self.prev_key = key
        self.counter += 1

        # Har 16 ta yozuvda restart point qo'yamiz
        if self.counter % 16 == 0:
            self.restarts.append(len(self.buffer))

        return len(self.buffer) >= self.target_size

    def finish(self) -> bytes:
        # Blok oxiriga restart pointlar massivi yoziladi
        for offset in self.restarts:
            self.buffer.extend(struct.pack(">I", offset))
        self.buffer.extend(struct.pack(">I", len(self.restarts)))
        return bytes(self.buffer)
```
**Tushuntirish:** Restart pointlar prefiks siqishining 'Ahilliy tovonini' yo'qotadi. Butun blokni boshidan parslash o'rniga, dastur restart nuqtalari bo'yicha binar sakrab, kerakli kalitni tezda topadi.


---

### Topshiriq #1215: Ko'p SSTable fayllari bo'ylab binar qidiruv va eng so'nggi versiyani topish
**Tavsif:** Kalit bir nechta SSTable fayllarida uchrashi mumkin. Eng yangi fayldan boshlab eng eskisiga qarab qidirish va birinchi topilgan natijani qaytarish lozim.
**Talablar:** SSTable ro'yxatini vaqt bo'yicha tartiblash, fayllar bo'ylab qidiruv va topilganda to'xtash.
**Yechim (Python):**
```python
class SSTableReaderMock:
    def __init__(self, filepath: str, data_dict: dict):
        self.filepath = filepath
        self.data = data_dict

    def get(self, key: bytes):
        return self.data.get(key)

class MultiTableSearchEngine:
    def __init__(self):
        # Eng yangi fayl birinchi turadi
        self.tables = []

    def add_table(self, table: SSTableReaderMock):
        self.tables.insert(0, table)

    def get(self, key: bytes):
        for table in self.tables:
            val = table.get(key)
            if val is not None:
                if val == TOMBSTONE_MARKER:
                    return None # Eng so'nggi versiya o'chirilgan
                return val
        return None
```
**Tushuntirish:** LSM-Tree da eng yangi ma'lumotlar L0 (yuqori daraja) da bo'ladi. Qidiruv yuqoridan pastga qarab boradi. Agar birinchi faylda kalit topilsa (yoki u Tombstone bo'lsa), quyi darajadagi eskirgan fayllarga hatto murojaat ham qilinmaydi.


---

### Topshiriq #1216: K-Way Merge Iterator: Bir nechta SSTable oqimlarini Min-Heap orqali birlashtirish
**Tavsif:** Zichlashtirish (Compaction) yoki keng qamrovli Range Scan qilishda bir nechta tartiblangan fayllarni $O(N \log K)$ murakkablikda bitta tartiblangan oqimga birlashtirish lozim.
**Talablar:** Python `heapq` moduli, Min-Heap elementlari `(key, table_index, value)`, duplikatsiyalarni eng yangi versiya foydasiga hal qilish.
**Yechim (Python):**
```python
import heapq

class KWayMergeIterator:
    def __init__(self, iterators):
        # iterators: har biri (key, value) qaytaruvchi iteratorlar massivi
        self.heap = []
        for i, it in enumerate(iterators):
            try:
                k, v = next(it)
                # Heap elementi: (key, table_idx, val, iterator)
                heapq.heappush(self.heap, (k, i, v, it))
            except StopIteration:
                pass

        self.last_emitted_key = None

    def __iter__(self):
        return self

    def __next__(self):
        while self.heap:
            key, idx, val, it = heapq.heappop(self.heap)

            # Navbatdagi elementni heapga qo'shish
            try:
                next_k, next_v = next(it)
                heapq.heappush(self.heap, (next_k, idx, next_v, it))
            except StopIteration:
                pass

            # Duplikat kalitlarni tashlab yuborish (eng yangisi avval chiqadi)
            if key == self.last_emitted_key:
                continue

            self.last_emitted_key = key
            return key, val

        raise StopIteration
```
**Tushuntirish:** K-Way Merge - tashqi saralash (External Sorting) algoritmlarining poydevoridir. Min-Heap orqali $K$ ta turli fayllardan minimal kalitni tanlash $O(\log K)$ vaqt oladi. Bu gigabaytlab ma'lumotlarni RAM ga sig'dirmasdan tartiblash imkonini beradi.


---

### Topshiriq #1217: SSTable Range Query: Diapazon so'rovlarini birlashtirilgan oqimda bajarish
**Tavsif:** Barcha diskdagi SSTable fayllari va xotiradagi MemTable ni bitta umumiy Range Iteratorga ulab, berilgan oraliqni so'rov qilish talab etiladi.
**Talablar:** MemTable va SSTable iteratorlarini `KWayMergeIterator` ga topshirish, oraliqni filtrlab natijalarni qaytarish.
**Yechim (Python):**
```python
class UnifiedRangeScanner:
    def __init__(self, memtable, sstables):
        self.memtable = memtable
        self.sstables = sstables

    def scan(self, start_key: bytes, end_key: bytes):
        iterators = []
        # MemTable iteratori
        iterators.append(iter(MemTableIterator(self.memtable, start_key, end_key)))
        
        # Har bir SSTable uchun iterator (simulyatsiya)
        for sst in self.sstables:
            iterators.append(iter([(k, v) for k, v in sst.data.items() if start_key <= k < end_key]))

        merged = KWayMergeIterator(iterators)
        results = []
        for k, v in merged:
            if v != TOMBSTONE_MARKER:
                results.append((k, v))
        return results
```
**Tushuntirish:** Birlashgan diapazon skanerlash dvigateli LSM-Tree ning murakkab ko'p qatlamli tuzilishini foydalanuvchidan to'liq yashiradi. Foydalanuvchi bitta sodda so'rov beradi, ichki tizim esa xotira va diskdagi qatlamlarni birlashtirib sof ma'lumotlarni beradi.


---

### Topshiriq #1218: Diskka yozilgan SSTable yaxlitligini tekshirish (Block-level Checksums)
**Tavsif:** Diskdagi sektorlarning buzilishi (Bit rot / Silent Data Corruption) oqibatida ma'lumotlar o'zgarib ketishini aniqlash uchun har bir blok oxiriga CRC32 yozish va o'qishda tekshirish lozim.
**Talablar:** Blok baytlari + CRC32, o'qish paytida tekshiruv, nomutanosiblikda `CorruptedBlockError` tashlash.
**Yechim (Python):**
```python
class CorruptedBlockError(Exception):
    pass

class BlockChecksumValidator:
    @staticmethod
    def append_checksum(raw_block_data: bytes) -> bytes:
        crc = zlib.crc32(raw_block_data) & 0xFFFFFFFF
        return raw_block_data + struct.pack(">I", crc)

    @staticmethod
    def verify_and_strip(block_with_crc: bytes) -> bytes:
        if len(block_with_crc) < 4:
            raise CorruptedBlockError("Blok hajmi juda kichik")

        data = block_with_crc[:-4]
        stored_crc, = struct.unpack(">I", block_with_crc[-4:])
        calculated_crc = zlib.crc32(data) & 0xFFFFFFFF

        if stored_crc != calculated_crc:
            raise CorruptedBlockError(f"Checksum xatosi! Kutilgan: {stored_crc}, Hisoblangan: {calculated_crc}")

        return data
```
**Tushuntirish:** Zamonaviy saqlash tizimlari operatsion tizimning drayverlariga ko'r-ko'rona ishonmaydi. Blok darajasidagi cheksunlar apparatdagi magnit/kremniy buzilishlarini darhol fosh qiladi va buzilgan ma'lumotlar mijozga yetib borishining oldini oladi.


---

### Topshiriq #1219: Manifest fayli: Barcha faol SSTable darajalari va fayllar metama'lumotlari jurnali
**Tavsif:** Qaysi SSTable fayllari L0, L1 yoki L2 darajasida ekanligini, qaysi fayllar o'chirilganligini doimiy kuzatib boruvchi VersionSet va Manifest jurnali talab qilinadi.
**Talablar:** VersionEdit strukturasini yaratish (yangi fayl qo'shildi, eski fayl o'chirildi), Manifest fayliga yozish.
**Yechim (Python):**
```python
import json

class VersionEdit:
    def __init__(self):
        self.added_files = []   # (level, file_number, min_key, max_key)
        self.deleted_files = [] # (level, file_number)

    def encode(self) -> bytes:
        payload = {
            "added": self.added_files,
            "deleted": self.deleted_files
        }
        return json.dumps(payload).encode("utf-8") + b"\n"

class ManifestLogger:
    def __init__(self, manifest_path: str):
        self.file = open(manifest_path, "a+b")

    def log_edit(self, edit: VersionEdit):
        self.file.write(edit.encode())
        self.file.flush()
        os.fsync(self.file.fileno())
```
**Tushuntirish:** Manifest fayli LSM-Tree ning 'Konstitutsiyasi'dir. U barcha fayllarning jismoniy holatini saqlaydi. Compaction yakunlanganda atomik VersionEdit yoziladi, bu esa tizim o'chib qolganda fayllarning adashib ketmasligini ta'minlaydi.


---

### Topshiriq #1220: SSTable fayl nomeri va VersionSet boshqaruvi
**Tavsif:** Har bir yangi yaratilayotgan SSTable fayli global tartibdagi unikal raqamga ega bo'lishi (masalan `000042.ldb`) va ketma-ketlik buzilmasligi kerak.
**Talablar:** Thread-safe File Number Generator, joriy versiya holatini (Active SSTables ro'yxati) saqlash.
**Yechim (Python):**
```python
class VersionSet:
    def __init__(self):
        self.next_file_number = 1
        self.levels = {0: [], 1: [], 2: []} # level => [file_numbers]

    def alloc_file_number(self) -> int:
        num = self.next_file_number
        self.next_file_number += 1
        return num

    def apply_edit(self, edit: VersionEdit):
        for level, file_num in edit.deleted_files:
            if file_num in self.levels[level]:
                self.levels[level].remove(file_num)

        for level, file_num, _, _ in edit.added_files:
            self.levels[level].append(file_num)
```
**Tushuntirish:** VersionSet xotirada joriy barcha SSTable fayllarining daraxtini ushlab turadi. Har bir yangi fayl unikal raqam oladi va eski raqamlar hech qachon takrorlanmaydi, bu fayl nomlarining ziddiyatini (collision) mutlaqo bartaraf etadi.


---

### Topshiriq #1221: Size-Tiered Compaction: O'lchami teng bo'lgan SSTablelarni birlashtirish
**Tavsif:** Apache Cassandra da qo'llaniladigan ushbu usulda taxminan bir xil hajmga ega bo'lgan 4 ta SSTable paydo bo'lishi bilan ular bitta katta faylga birlashtiriladi.
**Talablar:** Hajmlarni tahlil qilish, threshold (4 ta fayl) to'lganda ularni K-Way Merge orqali birlashtirish va yangi kattaroq fayl chiqarish.
**Yechim (Python):**
```python
class SizeTieredCompactor:
    def __init__(self, tier_size_threshold = 4):
        self.threshold = tier_size_threshold

    def find_compaction_candidates(self, file_sizes: dict):
        # file_sizes: {file_id: size_in_bytes}
        sorted_files = sorted(file_sizes.items(), key=lambda x: x[1])
        candidates = []
        for fid, size in sorted_files:
            candidates.append(fid)
            if len(candidates) >= self.threshold:
                return candidates # 4 ta teng fayl topildi
        return []
```
**Tushuntirish:** Size-Tiered Compaction o'ta yuqori yozish tezligini (high write workload) ta'minlaydi. Fayllar darhol qat'iy tartiblanmaydi, balki o'lchami bo'yicha to'planadi. Bu yozish ko'payishini (Write Amplification) kamaytiradi.


---

### Topshiriq #1222: Leveled Compaction (LevelDB / RocksDB uslubi): L0 dan L1 ga ko'chirish
**Tavsif:** L0 darajasidagi fayllar o'zaro kalitlar bo'yicha kesishadi (overlapping). L1 va undan quyi darajalarda esa har bir darajadagi fayllar kesishmaydigan (non-overlapping) oraliqlarga ega bo'lishi lozim.
**Talablar:** L0 dan faylni tanlash, L1 dagi kalitlari kesishuvchi barcha fayllarni topish va ularni birlashtirish.
**Yechim (Python):**
```python
class LeveledCompactor:
    @staticmethod
    def get_overlapping_files(candidate_min: bytes, candidate_max: bytes, l1_files: list):
        # l1_files: [(file_id, min_key, max_key)]
        overlapping = []
        for fid, min_k, max_k in l1_files:
            if not (candidate_max < min_k or candidate_min > max_k):
                overlapping.append(fid)
        return overlapping
```
**Tushuntirish:** Leveled Compaction o'qish unumdorligini (Read Performance) keskin oshiradi. L1, L2, L3 darajalarida fayllar kesishmagani sababli, bitta kalit har bir darajada faqat bitta faylda uchrashi kafolatlanadi. Qidiruv tezligi $O(1)$ disk murojaatiga tushadi.


---

### Topshiriq #1223: Qabr toshlarini (Tombstone) tozalash: Eng quyi darajada o'chirilgan kalitlarni yo'q qilish
**Tavsif:** Agar qabr toshi darhol o'chirib yuborilsa, quyi darajadagi eski qiymat qayta 'tirilib' qolishi mumkin. Qabr toshini faqat u bazaning eng quyi darajasiga (Bottom Level) yetgandagina jismoniy o'chirish lozim.
**Talablar:** Kalit eng quyi darajadami yoki undan pastda yana SSTable bormi tekshirish, agar oxirgi daraja bo'lsa o'chirish.
**Yechim (Python):**
```python
class TombstonePurger:
    @staticmethod
    def can_drop_tombstone(key: bytes, current_level: int, max_level_in_db: int, lower_levels_keys: set) -> bool:
        # Agar eng pastki daraja bo'lsa, xavfsiz o'chirish mumkin
        if current_level >= max_level_in_db:
            return True
        # Yoki undan pastki barcha darajalarda bu kalit umuman yo'q bo'lsa
        if key not in lower_levels_keys:
            return True
        return False
```
**Tushuntirish:** Tombstone Garbage Collection LSM-Tree ning eng ehtiyotkor amallaridan biridir. Agar pastki qatlamlarda hali eski versiya mavjud bo'lsa, qabr toshini yo'qotib bo'lmaydi. U faqat barcha eski nusxalarni o'zi bilan 'yondirib' yuborgandagina butunlay yo'q qilinadi.


---

### Topshiriq #1224: Compaction paytida Disk Write Amplification (yozish ko'payishi) ni minimallashtirish
**Tavsif:** Foydalanuvchi 1 MB ma'lumot yozganda, Compaction jarayonlari tufayli diskka jami 10 MB yoki 30 MB yozilishi mumkin (Write Amplification Factor). Uni hisoblash va minimallashtirish algoritmi kerak.
**Talablar:** WAF formulasini hisoblash: $\text{WAF} = \frac{\text{Jami diskka yozilgan baytlar}}{\text{Foydalanuvchi kiritgan baytlar}}$, dinamik limit sozlash.
**Yechim (Python):**
```python
class WriteAmplificationTracker:
    def __init__(self):
        self.user_bytes_written = 0
        self.disk_bytes_written = 0

    def record_user_write(self, nbytes: int):
        self.user_bytes_written += nbytes

    def record_disk_write(self, nbytes: int):
        self.disk_bytes_written += nbytes

    def get_waf(self) -> float:
        if self.user_bytes_written == 0:
            return 1.0
        return self.disk_bytes_written / self.user_bytes_written
```
**Tushuntirish:** Write Amplification Factor (WAF) SSD disklarining ishlash muddatiga to'g'ridan-to'g'ri ta'sir qiladi. Agar WAF=30 bo'lsa, 1 TB ma'lumot diskka 30 TB bo'lib tushadi va flesh-hujayralarni tez qaritadi. LSM-Tree ni sozlashda WAF ni 5-10 atrofida ushlab turish asosiy maqsaddir.


---

### Topshiriq #1225: Compaction Picker: Qaysi fayllarni zichlashtirish kerakligini aniqlovchi algoritm
**Tavsif:** Dvigatel qaysi darajada limit oshib ketganini (Score) hisoblab, eng kritik darajani birinchi navbatda zichlashtirish uchun tanlashi lozim.
**Talablar:** Har bir daraja uchun `score = current_size / max_size` hisoblash, Score > 1.0 bo'lgan eng katta darajani tanlash.
**Yechim (Python):**
```python
class CompactionPicker:
    MAX_LEVEL_BYTES = {
        0: 4 * 1024 * 1024,      # L0: 4 MB (fayllar soni bo'yicha)
        1: 10 * 1024 * 1024,     # L1: 10 MB
        2: 100 * 1024 * 1024,    # L2: 100 MB
        3: 1000 * 1024 * 1024    # L3: 1 GB
    }

    @staticmethod
    def pick_level_for_compaction(current_level_sizes: dict):
        best_level = None
        best_score = 0.0

        for level, size in current_level_sizes.items():
            max_size = CompactionPicker.MAX_LEVEL_BYTES.get(level, 10**9)
            score = size / max_size
            if score > 1.0 and score > best_score:
                best_score = score
                best_level = level

        return best_level, best_score
```
**Tushuntirish:** Compaction Picker tizimdagi muvozanatni saqlaydi. Agar L0 da fayllar ko'payib ketsa, qidiruv sekinlashadi, shuning uchun L0 har doim eng yuqori ustuvorlikka (priority) ega bo'ladi.


---

### Topshiriq #1226: Asinxron fon zichlashtiruvchisi (Background Compaction Worker)
**Tavsif:** Zichlashtirish (Compaction) jarayoni gigabaytlab ma'lumotlarni o'qib-yozgani uchun u alohida fonda (Background Worker Thread) mijozlarning `put`/`get` so'rovlariga to'sqinlik qilmasdan ishlashi shart.
**Talablar:** `threading.Thread` va `queue.Queue` orqali vazifalarni qabul qilish, fon ishini boshqarish va to'xtatish.
**Yechim (Python):**
```python
import threading
import queue
import time

class BackgroundCompactor:
    def __init__(self, execute_compaction_fn):
        self.task_queue = queue.Queue()
        self.execute_compaction_fn = execute_compaction_fn
        self.running = True
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()

    def schedule_compaction(self, level: int):
        self.task_queue.put(level)

    def _worker_loop(self):
        while self.running:
            try:
                level = self.task_queue.get(timeout=1.0)
                print(f"[FONDA COMPACTION] Level {level} zichlashtirish boshlandi...")
                self.execute_compaction_fn(level)
                self.task_queue.task_done()
                print(f"[FONDA COMPACTION] Level {level} muvaffaqiyatli yakunlandi")
            except queue.Empty:
                continue

    def stop(self):
        self.running = False
        self.worker_thread.join()
```
**Tushuntirish:** Background Compaction worker dvigatelning barqaror ishlashini ta'minlaydi. Mijozlar o'zlarining tranzaksiyalarini bajarishda davom etadi, fon oqimi esa eski fayllarni saralab yangi darajaga ko'chirib turadi.


---

### Topshiriq #1227: Zichlashtirish paytida o'qish va yozishni to'xtatmaslin (Non-blocking snapshots)
**Tavsif:** Compaction paytida eski SSTable fayllari o'chirilayotganda, ularni o'qiyotgan faol so'rovlar (Snapshots) xatoga uchramasligi (Read-after-delete) lozim.
**Talablar:** Reference Counting (havolalar hisoblagichi) yoki File Descriptor pinning mexanizmini joriy etish.
**Yechim (Python):**
```python
class TrackedSSTable:
    def __init__(self, file_id: int):
        self.file_id = file_id
        self.ref_count = 0
        self.obsolete = False

    def acquire(self):
        self.ref_count += 1

    def release(self):
        self.ref_count -= 1
        if self.ref_count == 0 and self.obsolete:
            self._physically_delete()

    def mark_obsolete(self):
        self.obsolete = True
        if self.ref_count == 0:
            self._physically_delete()

    def _physically_delete(self):
        print(f"[O'CHIRILDI] SSTable #{self.file_id} jismoniy diskdan o'chirildi")
```
**Tushuntirish:** Reference Counting LSM-Tree da xavfsiz xotira tozalashni ta'minlaydi. Compaction eski faylni `obsolete` (eskirgan) deb belgilaydi, ammo agar biron foydalanuvchi hozirda o'sha fayldan ma'lumot o'qiyotgan bo'lsa (`ref_count > 0`), fayl o'chirilmaydi. O'quvchi o'z ishini tugatgandagina fayl jismonan diskdan yo'qotiladi.


---

### Topshiriq #1228: Read Amplification (o'qish ko'payishi) ni baholash va tahlil qilish
**Tavsif:** Bitta `get(key)` so'rovi uchun tizim necha marta diskka murojaat qilayotganligini (Read Amplification) o'lchash va Bloom Filter yordamida uni kamaytirish zarur.
**Talablar:** Diskka murojaatlar sonini hisoblash, RAF = Disk Reads / Logical Reads formulasini joriy etish.
**Yechim (Python):**
```python
class ReadAmplificationTracker:
    def __init__(self):
        self.logical_gets = 0
        self.disk_block_reads = 0

    def record_get(self):
        self.logical_gets += 1

    def record_disk_read(self):
        self.disk_block_reads += 1

    def get_raf(self) -> float:
        if self.logical_gets == 0:
            return 0.0
        return self.disk_block_reads / self.logical_gets
```
**Tushuntirish:** B+Tree larda Read Amplification juda past (3-4 ta disk murojaati). LSM-Tree larda esa har bir darajada fayllar bo'lgani sababli RAF 20-30 gacha yetishi mumkin. Bloom Filter va Block Cache lar yordamida bu ko'rsatkich amalda 1.1 - 1.5 ga tushiriladi.


---

### Topshiriq #1229: Dynamic Level Size Multiplier (L_i = 10 * L_{i-1})
**Tavsif:** Har bir quyi daraja o'zidan yuqoridagi darajadan 10 barobar ko'proq ma'lumot saqlashi lozim: L1=10MB, L2=100MB, L3=1GB, L4=10GB.
**Talablar:** Multiplikator (T=10), darajalar hajmini avtomatik hisoblash va dinamik moslashuvchanlik.
**Yechim (Python):**
```python
class LevelHierarchyCalculator:
    def __init__(self, base_level_mb: int = 10, multiplier: int = 10, max_levels: int = 7):
        self.base_level = base_level_mb
        self.multiplier = multiplier
        self.max_levels = max_levels

    def get_capacity_mb(self, level: int) -> int:
        if level == 0:
            return self.base_level # L0 odatda L1 ga teng bo'ladi
        return self.base_level * (self.multiplier ** (level - 1))
```
**Tushuntirish:** Eksponentsial o'sish geometriyasi sababli barcha ma'lumotlarning 90% i eng quyi darajada (masalan L4 yoki L5 da) joylashadi. Bu esa xotirani rejalashtirish va qidiruv chuqurligini chegaralash imkonini beradi.


---

### Topshiriq #1230: Favqulodda to'xtatish: Yozish tezligi zichlashtirishdan oshib ketganda Write Stall mexanizmi
**Tavsif:** Mijozlar yozish tezligi diskning zichlashtirish (Compaction) quvvatidan oshib ketsa, L0 da yuzlab fayllar to'planib qolib tizim qulashi mumkin. Bu vaqtda kiruvchi yozishlarni majburiy sekinlashtirish (Write Stall) kerak.
**Talablar:** L0 fayllar soni > 8 bo'lsa sun'iy 1 ms kechikish kiritish, soni > 20 bo'lsa so'rovlarni butunlay to'xtatib turish.
**Yechim (Python):**
```python
class WriteStallController:
    def __init__(self):
        self.SLOWDOWN_THRESHOLD = 8
        self.STOP_THRESHOLD = 20

    def check_and_throttle(self, l0_file_count: int):
        if l0_file_count >= self.STOP_THRESHOLD:
            # Qat'iy to'xtatish (MemTable to'lib qoldi, Compaction yetisholmayapti)
            print("[WRITE STALL] Disk to'ldi! Barcha yozishlar vaqtincha muzlatildi!")
            time.sleep(0.1) # 100 ms kutish
            return "STOPPED"
        elif l0_file_count >= self.SLOWDOWN_THRESHOLD:
            # Sekinlashtirish (Backpressure)
            time.sleep(0.001) # 1 ms sun'iy kechikish
            return "THROTTLED"
        return "OK"
```
**Tushuntirish:** Write Stall LSM-Tree larning o'z-o'zini asrash tizimidir (Backpressure). U mijozlarning shiddatini sekinlashtirib, fon disk jarayonlariga ma'lumotlarni tartibga keltirib olish uchun imkoniyat yaratadi.


---

### Topshiriq #1231: Bitcask arxitekturasi: Append-only log va xotiradagi Hash Index (Keydir)
**Tavsif:** Bitcask - Erlang va Riak da qo'llaniluvchi ultra-sodda va o'ta tezkor saqlash dvigatelidir. Barcha kalitlar va ularning diskdagi ofsetlari xotiradagi Hash Table da (Keydir) saqlanadi.
**Talablar:** Keydir xotira lug'ati: `key => (file_id, value_size, value_offset, timestamp)`, $O(1)$ disk murojaati.
**Yechim (Python):**
```python
class BitcaskKeydirEntry:
    def __init__(self, file_id: int, val_sz: int, val_pos: int, timestamp: int):
        self.file_id = file_id
        self.val_sz = val_sz
        self.val_pos = val_pos
        self.timestamp = timestamp

class BitcaskKeydir:
    def __init__(self):
        self.index = {} # key => BitcaskKeydirEntry

    def put(self, key: bytes, file_id: int, val_sz: int, val_pos: int, ts: int):
        self.index[key] = BitcaskKeydirEntry(file_id, val_sz, val_pos, ts)

    def get(self, key: bytes):
        return self.index.get(key)
```
**Tushuntirish:** Bitcask ning asosiy afzalligi: Har qanday GET operatsiyasi atigi 1 ta disk murojaatini (1 disk seek) talab qiladi, chunki kalitning fayldagi aniq joylashuvi (offset) allaqachon RAM dagi hash-jadvalda ma'lum.


---

### Topshiriq #1232: Bitcask yozuv formati: CRC, Timestamp, KeySz, ValueSz, Key, Value
**Tavsif:** Bitcask faylidagi har bir yozuv qat'iy binar struktura bo'yicha diskka append-only qilib yozilishi shart.
**Talablar:** Format: `[CRC: 4B][Timestamp: 4B][KeySz: 2B][ValSz: 4B][Key][Value]`, yozuvni qadoqlash va diskka chiqarish.
**Yechim (Python):**
```python
class BitcaskRecordCodec:
    HEADER_FORMAT = ">IIHI" # CRC(4B), Timestamp(4B), KeySz(2B), ValSz(4B)
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    @staticmethod
    def encode_record(key: bytes, value: bytes) -> bytes:
        ts = int(time.time())
        key_sz = len(key)
        val_sz = len(value)
        payload = key + value
        
        # CRC hisoblash
        crc_data = struct.pack(">IHI", ts, key_sz, val_sz) + payload
        crc = zlib.crc32(crc_data) & 0xFFFFFFFF
        
        header = struct.pack(BitcaskRecordCodec.HEADER_FORMAT, crc, ts, key_sz, val_sz)
        return header + payload
```
**Tushuntirish:** Ushbu format xotira faylining o'zini o'zi tushuntiruvchi (self-describing) bo'lishini ta'minlaydi. Server buzilib qayta yoqilganda barcha fayllar boshidan oxirigacha o'qilib, xotiradagi Keydir noldan bir necha soniyada tiklanadi.


---

### Topshiriq #1233: Bitcask Get operatsiyasi: Xotiradan fayl offsetini topib os.pread orqali o'qish
**Tavsif:** Keydir dan ofset olingach, fayl ko'rsatkichini (seek) siljitmasdan, ko'p oqimli rejimda xavfsiz `os.pread` yordamida to'g'ridan-to'g'ri qiymatni o'qib olish lozim.
**Talablar:** `os.pread(fd, length, offset)` dan foydalanish, ko'p oqimlar uchun qulflarsiz xavfsiz o'qish.
**Yechim (Python):**
```python
class BitcaskReader:
    def __init__(self, file_descriptors: dict, keydir: BitcaskKeydir):
        self.fds = file_descriptors # file_id => open_fd
        self.keydir = keydir

    def get(self, key: bytes):
        entry = self.keydir.get(key)
        if not entry:
            return None # Kalit yo'q

        fd = self.fds.get(entry.file_id)
        if fd is None:
            raise FileNotFoundError(f"Fayl topilmadi: #{entry.file_id}")

        # os.pread orqali fayl kursorini o'zgartirmasdan atomar o'qish
        raw_val = os.pread(fd, entry.val_sz, entry.val_pos)
        return raw_val
```
**Tushuntirish:** `os.pread` (POSIX pread) standart `f.seek()` va `f.read()` ga qaraganda parallel tizimlarda ancha ustundir. Bir vaqtda 100 ta oqim bitta ochiq fayl deskriptoridan turli ofsetlar bo'yicha bir-biriga xalaqit bermasdan parallel ma'lumot o'qiydi.


---

### Topshiriq #1234: Bitcask Merge & Compaction: Eskirgan qiymatlarni olib tashlab yangi fayllarga yozish
**Tavsif:** Append-only modelida bitta kalit 100 marta o'zgartirilsa, diskda 100 ta yozuv paydo bo'ladi. Eski yozuvlarni tozalab, faqat eng so'nggi qiymatlarni yangi ixcham faylga ko'chirish kerak.
**Talablar:** Barcha muzlatilgan log fayllarini o'qish, Keydir dagi joriy ofset bilan solishtirish, faqat faol yozuvlarni yangi faylga ko'chirish.
**Yechim (Python):**
```python
class BitcaskMerger:
    @staticmethod
    def merge_files(old_files, keydir: BitcaskKeydir, new_active_file):
        # new_active_file: yangi toza fayl
        new_pos = 0
        for old_file_id, filepath in old_files:
            with open(filepath, "rb") as f:
                pos = 0
                while True:
                    header = f.read(BitcaskRecordCodec.HEADER_SIZE)
                    if not header:
                        break
                    _, ts, ksz, vsz = struct.unpack(BitcaskRecordCodec.HEADER_FORMAT, header)
                    key = f.read(ksz)
                    val = f.read(vsz)
                    
                    val_pos = pos + BitcaskRecordCodec.HEADER_SIZE + ksz
                    current_entry = keydir.get(key)
                    
                    # Agar ushbu yozuv hali ham Keydir dagi eng so'nggi versiya bo'lsa
                    if current_entry and current_entry.file_id == old_file_id and current_entry.val_pos == val_pos:
                        new_record = BitcaskRecordCodec.encode_record(key, val)
                        new_active_file.write(new_record)
                        # Keydir ni yangi fayl va ofsetga yangilash
                        keydir.put(key, 9999, vsz, new_pos + BitcaskRecordCodec.HEADER_SIZE + ksz, ts)
                        new_pos += len(new_record)
                    pos += BitcaskRecordCodec.HEADER_SIZE + ksz + vsz
```
**Tushuntirish:** Bitcask Merge jarayoni disk maydonini qayta tiklaydi. Eskirgan va o'chirilgan barcha yozuvlar tashlab ketiladi, natijada disk hajmi 80-90% gacha bo'shaydi.


---

### Topshiriq #1235: Hint fayllari: Server qayta yonganda tez yuklanish uchun faqat kalit va offsetlarni saqlash
**Tavsif:** Merge dan so'ng ulkan ma'lumot fayllarini qayta parslash o'rniga, faqatgina kalitlar va ularning ofsetlarini saqlovchi maxsus 'Hint' (maslahat) fayli yaratiladi.
**Talablar:** Hint fayli formati: `[Timestamp][KeySz][ValSz][ValPos][Key]`, server ishga tushganda faqat hint faylini o'qib Keydir ni bir zumda tiklash.
**Yechim (Python):**
```python
class BitcaskHintFile:
    HINT_HEADER = ">IIHQ" # TS(4B), KeySz(2B), ValSz(4B), ValPos(8B)

    @staticmethod
    def write_hint_entry(hint_file, ts: int, key: bytes, val_sz: int, val_pos: int):
        header = struct.pack(">IIHQ", ts, len(key), val_sz, val_pos)
        hint_file.write(header + key)

    @staticmethod
    def load_hint_file(hint_filepath: str, file_id: int, keydir: BitcaskKeydir):
        with open(hint_filepath, "rb") as f:
            while True:
                hdr = f.read(18)
                if not hdr:
                    break
                ts, ksz, vsz, vpos = struct.unpack(">IIHQ", hdr)
                key = f.read(ksz)
                keydir.put(key, file_id, vsz, vpos, ts)
```
**Tushuntirish:** Hint fayllari Bitcask ning o'ziga xos ixtirosidir. Gigabaytlab qiymatlarni (Values) chetlab o'tib, faqat ixcham Hint fayli o'qiladi. Natijada 100 GB hajmdagi baza server qayta yonganda atigi 1-2 soniyada to'liq ishchi holatga keladi.


---

### Topshiriq #1236: Bitcask fayl rotatsiyasi: 100 MB ga yetganda faol faylni muzlatib yangi fayl ochish
**Tavsif:** Bitta fayl haddan tashqari ulkan bo'lib ketmasligi uchun joriy faol fayl 100 MB ga yetganda u faqat o'qish (Read-Only) rejimiga o'tkazilib, yangi faol fayl ochilishi kerak.
**Talablar:** Fayl hajmini kuzatish, yangi `file_id` generatsiyasi va xavfsiz almashish.
**Yechim (Python):**
```python
class BitcaskFileManager:
    MAX_FILE_SIZE = 100 * 1024 * 1024 # 100 MB

    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.active_file_id = 1
        self.active_file_pos = 0
        self.active_file = open(self._path(self.active_file_id), "a+b")

    def _path(self, fid: int) -> str:
        return os.path.join(self.base_dir, f"data_{fid:06d}.bitcask")

    def write_record(self, record_bytes: bytes) -> tuple:
        if self.active_file_pos + len(record_bytes) > self.MAX_FILE_SIZE:
            self.active_file.close()
            self.active_file_id += 1
            self.active_file = open(self._path(self.active_file_id), "a+b")
            self.active_file_pos = 0

        pos = self.active_file_pos
        self.active_file.write(record_bytes)
        self.active_file_pos += len(record_bytes)
        return self.active_file_id, pos
```
**Tushuntirish:** Fayl rotatsiyasi parallel zichlashtirish (Compaction) uchun zarur shartdir. Qadimgi fayllar o'zgarmas holatda qolgani sababli, fondagi Merger ularni xavfsiz o'qib tozalashi mumkin.


---

### Topshiriq #1237: Bitcask Delete: Qiymat uzunligi -1 yoki maxsus tombstone bilan logga yozish
**Tavsif:** Bitcask da ma'lumotni o'chirish log fayliga maxsus o'chirish belgisi yozish va Keydir dan kalitni olib tashlash orqali amalga oshiriladi.
**Talablar:** Tombstone yozish, `keydir.pop(key)` chaqirish, o'chirilgan yozuv keyingi so'rovlarda topilmasligi.
**Yechim (Python):**
```python
class BitcaskStore:
    def __init__(self, file_mgr: BitcaskFileManager, keydir: BitcaskKeydir):
        self.file_mgr = file_mgr
        self.keydir = keydir

    def delete(self, key: bytes):
        # Qiymat sifatida bo'sh bayt va maxsus o'chirish yozuvi
        rec = BitcaskRecordCodec.encode_record(key, TOMBSTONE_MARKER)
        self.file_mgr.write_record(rec)
        # Xotiradagi indeksdan olib tashlaymiz
        self.keydir.index.pop(key, None)
```
**Tushuntirish:** Keydir dan kalit o'chirilishi bilanoq, keyingi barcha `get` so'rovlari 0 soniyada 'Not Found' qaytaradi. Diskdagi tombstone yozuvi esa faqat keyingi Merge paytida eski yozuvlar bilan birga tozalab tashlanadi.


---

### Topshiriq #1238: Bitcask Crash Recovery: Barcha log fayllarini ketma-ket o'qib Keydir ni qayta tiklash
**Tavsif:** Hint fayllari bo'lmagan taqdirda, barcha mavjud `.bitcask` ma'lumot fayllarini tartib bilan o'qib, xotiradagi indeksni to'liq tiklash lozim.
**Talablar:** Fayllarni vaqt/id bo'yicha saralash, har bir yozuvni o'qish, eng so'nggi ofsetlarni Keydir ga kiritish.
**Yechim (Python):**
```python
class BitcaskCrashRecovery:
    @staticmethod
    def rebuild_keydir(file_paths: list, keydir: BitcaskKeydir):
        # Fayllarni ID bo'yicha saralash
        for fid, path in sorted(file_paths, key=lambda x: x[0]):
            with open(path, "rb") as f:
                pos = 0
                while True:
                    hdr = f.read(BitcaskRecordCodec.HEADER_SIZE)
                    if not hdr:
                        break
                    _, ts, ksz, vsz = struct.unpack(BitcaskRecordCodec.HEADER_FORMAT, hdr)
                    key = f.read(ksz)
                    val = f.read(vsz)
                    
                    val_pos = pos + BitcaskRecordCodec.HEADER_SIZE + ksz
                    if val == TOMBSTONE_MARKER:
                        keydir.index.pop(key, None)
                    else:
                        keydir.put(key, fid, vsz, val_pos, ts)
                    pos += BitcaskRecordCodec.HEADER_SIZE + ksz + vsz
```
**Tushuntirish:** Append-only jurnallarning go'zalligi shundaki, eng so'nggi operatsiya avtomatik tarzda eski operatsiyalarning ustiga yoziladi (overwrite). Hech qanday murakkab tiklash algoritmlari talab qilinmaydi.


---

### Topshiriq #1239: Bitcask Range Query cheklovlari va ularni yengish usullari
**Tavsif:** Bitcask ning eng katta kamchiligi - uning kalitlari xotirada tartiblanmagan (Hash Map) bo'lishidir. Range Query (`start_key` dan `end_key` gacha) amallarini bajarish uchun xotirada qo'shimcha tartiblangan indeks yaratish kerak.
**Talablar:** B-Tree yoki Sorted List ni parallel yuritish, oraliq so'rovlarini tartiblangan kalitlar ro'yxatidan bajarish.
**Yechim (Python):**
```python
class BitcaskWithRangeScan:
    def __init__(self, keydir: BitcaskKeydir):
        self.keydir = keydir
        self.sorted_keys = []

    def put(self, key: bytes, fid: int, vsz: int, vpos: int, ts: int):
        if key not in self.keydir.index:
            bisect.insort(self.sorted_keys, key)
        self.keydir.put(key, fid, vsz, vpos, ts)

    def scan_range(self, start_key: bytes, end_key: bytes):
        idx_start = bisect.bisect_left(self.sorted_keys, start_key)
        idx_end = bisect.bisect_right(self.sorted_keys, end_key)
        return self.sorted_keys[idx_start:idx_end]
```
**Tushuntirish:** Oddiy Bitcask faqat Point Query (`get/put`) uchun mo'ljallangan. Ammo xotirada qo'shimcha `sorted_keys` massivini saqlash orqali unga Range Scan imkoniyatini ham qo'shish mumkin, biroq bu xotira sarfini 20% ga oshiradi.


---

### Topshiriq #1240: Bitcask va LSM-Tree solishtirmasi: Disk va xotira balansi
**Tavsif:** Dasturiy arxitekturada qachon Bitcask va qachon LSM-Tree tanlanishi kerakligini tahlil qiluvchi taqqoslash modeli.
**Talablar:** RAM sarfi va disk IOPS ni solishtiruvchi hisoblagich, to'g'ri storage engine tanlash tavsiyanomasi.
**Yechim (Python):**
```python
class StorageEngineSelector:
    @staticmethod
    def evaluate(workload: dict) -> str:
        # workload: {total_keys, avg_val_size, ram_budget_gb, needs_range_scans}
        ram_needed_bitcask_gb = (workload["total_keys"] * 32) / (1024**3)
        
        if workload["needs_range_scans"]:
            return "LSM-Tree (RocksDB/LevelDB) - Chunki SSTable va MemTable tartiblangan"
        
        if ram_needed_bitcask_gb <= workload["ram_budget_gb"]:
            return "Bitcask - O'ta past kechikish (1 Disk Seek) va maksimal yozish tezligi"
        else:
            return "LSM-Tree - Kalitlar xotiraga sig'maydi, Sparse Index talab qilinadi"
```
**Tushuntirish:** Bitcask agar barcha kalitlar operativ xotiraga sig'sa (masalan 100 million kalit = 3.2 GB RAM) dunyodagi eng tezkor dvigateldir. Agar kalitlar milliardlab bo'lsa yoki murakkab oraliq so'rovlari kerak bo'lsa, LSM-Tree yagona tanlov hisoblanadi.


---

### Topshiriq #1241: Bloom Filter: Murakkab matematik hash funksiyalari (Murmur3) bilan kalit mavjudligini tezkor tekshirish
**Tavsif:** Diskdagi SSTable ichida kalit yo'q bo'lsa, behuda diskni o'qimaslik uchun 99% aniqlik bilan 'Bu kalit faylda aniq yo'q' deb javob beruvchi Bloom Filter yaratish kerak.
**Talablar:** Bit massivi, $k$ ta mustaqil xesh funksiyalari (Kirsch-Mitzenmacher texnikasi: $h_i(x) = h_1(x) + i \cdot h_2(x)$), `add` va `contains` metodlari.
**Yechim (Python):**
```python
class BloomFilter:
    def __init__(self, size_in_bits: int, num_hashes: int):
        self.size = size_in_bits
        self.k = num_hashes
        self.bit_array = bytearray((size_in_bits + 7) // 8)

    def _hashes(self, key: bytes):
        # 2 ta bazaviy xeshdan k ta xesh hosil qilish
        h1 = zlib.crc32(key) & 0xFFFFFFFF
        h2 = (zlib.adler32(key) ^ 0x5bd1e995) & 0xFFFFFFFF
        for i in range(self.k):
            yield (h1 + i * h2) % self.size

    def add(self, key: bytes):
        for bit_index in self._hashes(key):
            byte_idx = bit_index // 8
            bit_offset = bit_index % 8
            self.bit_array[byte_idx] |= (1 << bit_offset)

    def contains(self, key: bytes) -> bool:
        for bit_index in self._hashes(key):
            byte_idx = bit_index // 8
            bit_offset = bit_index % 8
            if (self.bit_array[byte_idx] & (1 << bit_offset)) == 0:
                return False # Aniq yo'q!
        return True # Bo'lishi mumkin (False positive ehtimoli bor)
```
**Tushuntirish:** Bloom Filter LSM-Tree larning eng mo''jizaviy komponentidir. Agar Bloom Filter 'YO'Q' desa, kalit diskda 100% yo'q va SSTable faylini ochish shart emas. Bu mavjud bo'lmagan kalitlarni qidirishda disk I/O sarfini deyarli nolga tushiradi.


---

### Topshiriq #1242: Bloom Filter False Positive ehtimolligini hisoblash va optimal bit massivi hajmi
**Tavsif:** Kutilayotgan elementlar soni $n$ va qabul qilinuvchi xato ehtimolligi $p=0.01$ (1%) bo'lganda, optimal bit massivi hajmi $m$ va xeshlar soni $k$ ni hisoblovchi formula.
**Talablar:** Formulalar: $m = -\frac{n \ln p}{(\ln 2)^2}$, $k = \frac{m}{n} \ln 2$. Har bir element uchun bitlar soni (~10 bit).
**Yechim (Python):**
```python
import math

class OptimalBloomCalculator:
    @staticmethod
    def calculate_params(expected_elements: int, false_positive_rate: float = 0.01):
        # m = - (n * ln(p)) / (ln(2)^2)
        m = - (expected_elements * math.log(false_positive_rate)) / (math.log(2) ** 2)
        # k = (m / n) * ln(2)
        k = (m / expected_elements) * math.log(2)
        
        bits_per_element = m / expected_elements
        return int(math.ceil(m)), int(math.ceil(k)), bits_per_element
```
**Tushuntirish:** Matematika shuni ko'rsatadiki, har bir kalit uchun atigi 10 bit xotira ajratilsa va 7 ta xesh funksiya ishlatilsa, xato qilish (False Positive) ehtimoli roppa-rosa 1% ni tashkil qiladi. Ya'ni 99 ta keraksiz disk murojaati to'xtatiladi.


---

### Topshiriq #1243: B+Tree Node strukturasi: Leaf va Internal tugunlar, kalitlar va ko'rsatkichlar
**Tavsif:** Relyatsion ma'lumotlar bazalarining (PostgreSQL, InnoDB) asosi bo'lgan B+Tree daraxtini qurish: Barg tugunlar (faqat ma'lumot saqlovchi) va Ichki yo'naltiruvchi tugunlar arxitekturasi.
**Talablar:** Maksimal sig'im (Degree $M=4$), `is_leaf` bayrog'i, `keys` va `children` massivlari.
**Yechim (Python):**
```python
class BPlusNode:
    def __init__(self, is_leaf: bool = False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = [] # Agar leaf bo'lsa qiymatlar, bo'lmasa BPlusNode obyektlari
        self.next = None   # Leaf larni bir-biriga bog'lovchi Linked List ko'rsatkichi
```
**Tushuntirish:** Klassik B-Tree dan farqli ravishda, B+Tree da barcha haqiqiy qiymatlar faqat barglarda (Leaf nodes) saqlanadi. Ichki tugunlar faqat yo'l ko'rsatuvchi kalitlarni saqlaydi, bu esa ichki tugunlarning zichligini oshirib, daraxt balandligini 3-4 darajada ushlab turadi.


---

### Topshiriq #1244: B+Tree Insert: Tugun to'lganda o'rtasidan bo'lish (Node Splitting)
**Tavsif:** Tugun sig'imi (Degree) to'lganda, u ikkita teng yarmiga bo'linadi (split) va o'rta kalit ota-tugunga (parent) ko'tariladi.
**Talablar:** Tugunni bo'lish algoritmi, yangi ildiz (Root) yaratish agar ildiz bo'linsa, barglar o'rtasida bog'langan ro'yxatni saqlash.
**Yechim (Python):**
```python
class BPlusTree:
    def __init__(self, degree: int = 4):
        self.root = BPlusNode(is_leaf=True)
        self.degree = degree

    def insert(self, key, value):
        root = self.root
        if len(root.keys) >= self.degree - 1:
            # Yangi ildiz yaratish va bo'lish
            new_root = BPlusNode(is_leaf=False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
            self._insert_non_full(self.root, key, value)
        else:
            self._insert_non_full(root, key, value)

    def _split_child(self, parent: BPlusNode, idx: int):
        node = parent.children[idx]
        mid = len(node.keys) // 2
        split_key = node.keys[mid]

        sibling = BPlusNode(is_leaf=node.is_leaf)
        if node.is_leaf:
            sibling.keys = node.keys[mid:]
            sibling.children = node.children[mid:]
            node.keys = node.keys[:mid]
            node.children = node.children[:mid]
            sibling.next = node.next
            node.next = sibling
        else:
            sibling.keys = node.keys[mid + 1:]
            sibling.children = node.children[mid + 1:]
            node.keys = node.keys[:mid]
            node.children = node.children[:mid + 1]

        parent.keys.insert(idx, split_key)
        parent.children.insert(idx + 1, sibling)

    def _insert_non_full(self, node: BPlusNode, key, value):
        if node.is_leaf:
            idx = bisect.bisect_left(node.keys, key)
            node.keys.insert(idx, key)
            node.children.insert(idx, value)
        else:
            idx = bisect.bisect_right(node.keys, key)
            child = node.children[idx]
            if len(child.keys) >= self.degree - 1:
                self._split_child(node, idx)
                if key > node.keys[idx]:
                    child = node.children[idx + 1]
            self._insert_non_full(child, key, value)
```
**Tushuntirish:** B+Tree pastdan yuqoriga qarab o'sadi. Faqat ildiz bo'lingandagina daraxtning balandligi 1 ga oshadi. Bu barcha barglarning har doim mutlaqo bir xil chuqurlikda bo'lishini (Strict Balance) kafolatlaydi.


---

### Topshiriq #1245: B+Tree Search: Ildizdan barggacha O(log N) binar qidiruv
**Tavsif:** Ildizdan boshlab har bir ichki tugunda binar qidiruv bilan to'g'ri bolaga o'tib, barg tuguniga yetib borish va kalit qiymatini olish.
**Talablar:** Rekursiv yoki iterativ qidiruv, $O(\log N)$ murakkablik, kalit topilmasa `None` qaytarish.
**Yechim (Python):**
```python
def search(self, key):
        current = self.root
        while not current.is_leaf:
            idx = bisect.bisect_right(current.keys, key)
            current = current.children[idx]

        idx = bisect.bisect_left(current.keys, key)
        if idx < len(current.keys) and current.keys[idx] == key:
            return current.children[idx]
        return None
```
**Tushuntirish:** B+Tree qidiruvida har bir ichki tugun 100-500 ta kalitni saqlashi mumkin. 1 milliard yozuv bo'lganda ham daraxt balandligi atigi 3 yoki 4 bo'ladi, ya'ni xohlagan yozuvni topish uchun atigi 3 ta qadam yetarli.


---

### Topshiriq #1246: B+Tree Leaf Linked List: Qatorli skanerlash (Sequential Range Scan)
**Tavsif:** B+Tree ning oddiy B-Tree dan eng katta ustunligi: Barcha barglar bir-biriga zanjir bo'lib ulangan (`next` ko'rsatkichi). Qidiruv boshlangach, daraxtni qayta aylanmasdan to'g'ridan-to'g'ri zanjir bo'ylab yurish mumkin.
**Talablar:** Oraliq qidiruv `[start, end]`, birinchi bargni topish va `node.next` bo'ylab yig'ish.
**Yechim (Python):**
```python
def range_scan(self, start_key, end_key):
        current = self.root
        # Boshlang'ich bargni topish
        while not current.is_leaf:
            idx = bisect.bisect_right(current.keys, start_key)
            current = current.children[idx]

        results = []
        while current:
            for k, val in zip(current.keys, current.children):
                if k > end_key:
                    return results
                if k >= start_key:
                    results.append((k, val))
            current = current.next # To'g'ridan-to'g'ri keyingi bargga o'tish
        return results
```
**Tushuntirish:** B+Tree ning barglari zanjirli bo'lgani uchun SQL dagi `WHERE age BETWEEN 20 AND 30` so'rovlari o'ta yuqori tezlikda bajariladi. Daraxt bo'ylab qayta tushib-chiqishga hojat yo'q, barglar o'zi ketma-ket ro'yxatdir.


---

### Topshiriq #1247: Buffer Pool Manager: Disk sahifalarini (Pages) xotirada ushlab turuvchi bufer hovuzi
**Tavsif:** Ma'lumotlar bazasi har safar diskka bormasligi uchun 4KB li disk sahifalarini xotiradagi doimiy bufer hovuzida (Buffer Pool) boshqarish talab etiladi.
**Talablar:** Frame massivi, Page Table (`page_id => frame_id`), sahifani xotiraga pin qilish (pin_count) va unpin qilish.
**Yechim (Python):**
```python
class BufferFrame:
    def __init__(self, frame_id: int):
        self.frame_id = frame_id
        self.page_id = None
        self.data = bytearray(4096)
        self.is_dirty = False
        self.pin_count = 0

class BufferPoolManager:
    def __init__(self, pool_size: int = 100):
        self.pool_size = pool_size
        self.frames = [BufferFrame(i) for i in range(pool_size)]
        self.page_table = {} # page_id => frame_id
        self.free_frames = list(range(pool_size))

    def fetch_page(self, page_id: int) -> BufferFrame:
        if page_id in self.page_table:
            frame = self.frames[self.page_table[page_id]]
            frame.pin_count += 1
            return frame

        # Yangi freym ajratish
        if not self.free_frames:
            raise RuntimeError("Bufer to'lgan! Eviction talab etiladi")

        fid = self.free_frames.pop(0)
        frame = self.frames[fid]
        frame.page_id = page_id
        frame.pin_count = 1
        frame.is_dirty = False
        self.page_table[page_id] = fid
        return frame

    def unpin_page(self, page_id: int, is_dirty: bool):
        if page_id in self.page_table:
            frame = self.frames[self.page_table[page_id]]
            frame.pin_count = max(0, frame.pin_count - 1)
            if is_dirty:
                frame.is_dirty = True
```
**Tushuntirish:** Buffer Pool Manager PostgreSQL va MySQL InnoDB ning eng muhim organidir. U operatsion tizimning keshiga tayanmasdan, qaysi sahifa o'zgarganligi (dirty) va qaysi sahifa ayni paytda o'qilayotganligini (`pin_count`) o'zi qat'iy nazorat qiladi.


---

### Topshiriq #1248: LRU-K (LRU-2) sahifalarni almashtirish (Eviction) siyosati
**Tavsif:** Klassik LRU bir marta butun jadvalni skanerlaganda (Sequential Scan) barcha foydali keshni yuvib yuboradi (Cache Pollution). Oxirgi $K=2$ ta murojaat vaqtini hisobga oluvchi LRU-2 algoritmini joriy etish lozim.
**Talablar:** Har bir sahifa uchun oxirgi 2 ta murojaat vaqtini saqlash, 2 marta murojaat qilinmagan sahifalarni birinchi navbatda keshdan haydash.
**Yechim (Python):**
```python
class LRU2Replacer:
    def __init__(self):
        # frame_id => [history_timestamps]
        self.history = {}

    def record_access(self, frame_id: int):
        now = time.time()
        if frame_id not in self.history:
            self.history[frame_id] = []
        self.history[frame_id].append(now)
        if len(self.history[frame_id]) > 2:
            self.history[frame_id].pop(0)

    def victim(self, candidate_frames: list):
        # 1. Avval faqat 1 marta murojaat qilinganlarni haydaymiz (Sequential scan himoyasi)
        single_access = [f for f in candidate_frames if len(self.history.get(f, [])) < 2]
        if single_access:
            return single_access[0]

        # 2. Keyin 2-orqadagi murojaati eng eski bo'lganini tanlaymiz
        oldest_frame = None
        oldest_time = float("inf")
        for f in candidate_frames:
            t2 = self.history[f][0]
            if t2 < oldest_time:
                oldest_time = t2
                oldest_frame = f
        return oldest_frame
```
**Tushuntirish:** LRU-2 algoritmi 'Bir martalik so'rovlar' (Sequential Scan pollution) balosidan keshni to'liq himoya qiladi. Agar biron so'rov butun 10 GB li jadvalni o'qib chiqsa ham, sahifalarga ikkinchi marta murojaat bo'lmasa, ular asosiy keshdagi doimiy issiq ma'lumotlarni chiqarib yubora olmaydi.


---

### Topshiriq #1249: Dirty Pages Flush va Checkpointing: O'zgargan sahifalarni diskka atomar yozish
**Tavsif:** Xotirada o'zgartirilgan 'iflos' (Dirty) sahifalarni vaqti-vaqti bilan diskka yozib, WAL jurnalini qisqartirish uchun Checkpoint tizimi zarur.
**Talablar:** Barcha `is_dirty == True` va `pin_count == 0` bo'lgan sahifalarni topish, diskka yozish va bayroqni tozalash.
**Yechim (Python):**
```python
class CheckpointManager:
    def __init__(self, bpm: BufferPoolManager, disk_writer_fn):
        self.bpm = bpm
        self.disk_writer = disk_writer_fn

    def checkpoint(self):
        flushed_pages = 0
        for frame in self.bpm.frames:
            # Faqat faol ishlatilmayotgan va o'zgargan sahifalarni yozamiz
            if frame.is_dirty and frame.pin_count == 0 and frame.page_id is not None:
                self.disk_writer(frame.page_id, bytes(frame.data))
                frame.is_dirty = False
                flushed_pages += 1
        print(f"[CHECKPOINT] {flushed_pages} ta iflos sahifa diskka xavfsiz saqlandi")
```
**Tushuntirish:** Checkpoint operatsiyasi ma'lumotlar bazasining qayta tiklanish vaqtini (Recovery Time Objective - RTO) bir necha soatdan bir necha soniyaga qisqartiradi. Tizim o'chib qolsa, faqat oxirgi Checkpoint dan keyingi WAL yozuvlari o'qiladi.


---

### Topshiriq #1250: To'liq integratsiyalashgan gibrid Storage Engine (LSM-Tree + Bloom Filter + Buffer Cache)
**Tavsif:** Barcha komponentlarni: MemTable, Bloom Filter, SSTable va K-Way Merge ni yagona ishlab chiqarishga tayyor (production-ready) yuqori unumdor saqlash dvigateliga birlashtirish.
**Talablar:** Kompakt API: `put`, `get`, `delete`, `flush`, xotira nazorati va kiber-chidamlilik testi.
**Yechim (Python):**
```python
class EnterpriseStorageEngine:
    def __init__(self):
        self.memtable = SkipListMemTable()
        self.bloom_filter = BloomFilter(10000, 7)
        self.disk_tables = []

    def put(self, key: str, value: str):
        k_bytes = key.encode("utf-8")
        v_bytes = value.encode("utf-8")
        self.memtable.put(k_bytes, v_bytes)
        self.bloom_filter.add(k_bytes)

    def delete(self, key: str):
        k_bytes = key.encode("utf-8")
        self.memtable.put(k_bytes, TOMBSTONE_MARKER)

    def get(self, key: str):
        k_bytes = key.encode("utf-8")
        # 1. Avval xotiradagi MemTable dan qidirish
        val = self.memtable.get(k_bytes)
        if val is not None:
            return None if val == TOMBSTONE_MARKER else val.decode("utf-8")

        # 2. Bloom filter: Agar yo'q desa diskka bormaymiz!
        if not self.bloom_filter.contains(k_bytes):
            return None

        # 3. Diskdagi SSTable lardan qidirish
        for table in reversed(self.disk_tables):
            val = table.get(k_bytes)
            if val is not None:
                return None if val == TOMBSTONE_MARKER else val.decode("utf-8")

        return None

    def flush_memtable(self):
        # Simulyatsiya qilingan flush
        snapshot = {}
        for k, v in MemTableIterator(self.memtable):
            snapshot[k] = v
        self.disk_tables.append(SSTableReaderMock("table.sst", snapshot))
        self.memtable = SkipListMemTable()
        print("[ENGINE] MemTable muvaffaqiyatli diskka to'kildi!")
```
**Tushuntirish:** Ushbu arxitektura zamonaviy Big Data ma'lumotlar bazalarining (Google Bigtable, Apache Cassandra, RocksDB) asosidir. Yozishlar xotiradagi SkipList ga $O(1)$ tezlikda tushadi, o'qishlar esa Bloom Filter orqali disk I/O ni chetlab o'tadi, natijada dvigatel soniyasiga yuz minglab operatsiyalarni bemalol qayta ishlaydi.

