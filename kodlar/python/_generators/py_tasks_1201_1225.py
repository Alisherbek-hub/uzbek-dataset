# -*- coding: utf-8 -*-
"""
Python 25-modul: 1201 dan 1225 gacha bo'lgan topshiriqlar
Storage Engines: LSM-Trees (MemTable, WAL, SSTable, Compaction)
"""

TASKS_1201_1225 = [
    {
        "id": 1201,
        "title": "MemTable: Xotirada tartiblangan SkipList ma'lumotlar strukturasi",
        "desc": "LSM-Tree (Log-Structured Merge-Tree) saqlash dvigatelida ma'lumotlarni xotirada doimo tartiblangan (sorted) holatda ushlab turish va $O(\\log N)$ vaqtda kiritish hamda qidirish uchun SkipList tuzilmasini yaratish lozim.",
        "req": "Ehtimollik asosidagi darajalar (probabilistic levels, $p=0.5$), maksimal balandlik (MAX_LEVEL=16), `put`, `get`, va `contains` metodlarini to'liq implementatsiya qilish.",
        "code": """import random

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
        return None""",
        "expl": "SkipList qizil-qora daraxtlarga (Red-Black Tree) nisbatan ancha sodda va amalda tezroq ishlaydi, chunki murakkab daraxtni aylantirish (rebalancing) operatsiyalarini talab qilmaydi. Ehtimollik asosidagi balandlik taqsimoti qidirish va kiritish amallarining o'rtacha murakkabligini $O(\\log N)$ bo'lishini ta'minlaydi."
    },
    {
        "id": 1202,
        "title": "Write-Ahead Log (WAL): Crash recovery uchun append-only jurnal va CRC32 cheksum",
        "desc": "Xotiradagi MemTable ga ma'lumot yozishdan oldin elektr toki o'chganda ma'lumotlar yo'qolmasligi (Durability) uchun har bir operatsiyani diskdagi ketma-ket jurnalga (WAL) yaxlitlik nazorati bilan yozish lozim.",
        "req": "Binar format: `[CRC32: 4 bayt][KeyLen: 2 bayt][ValLen: 4 bayt][Type: 1 bayt][Key][Value]`, zlib CRC32 hisoblash va tasdiqlash.",
        "code": """import os
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
        self.file.close()""",
        "expl": "WAL append-only (faqat oxiriga qo'shish) printsipida ishlaydi. Qattiq disklarda (HDD va NVMe SSD) ketma-ket yozish (sequential write) tasodifiy yozishdan 100 barobargacha tezroq bo'ladi. `os.fsync` operatsion tizim buferini majburiy ravishda jismoniy flesh-xotiraga tushiradi."
    },
    {
        "id": 1203,
        "title": "MemTable hajmi chegaralanganda (Flush threshold) diskka immutabel holatda yozish",
        "desc": "MemTable xotira hajmi belgilangan chegaraga (masalan 4 MB yoki 64 MB) yetganda, yangi yozishlarni to'xtatmaslik uchun faol MemTable o'zgarmas (immutable) holatga o'tkazilib, fonda diskdagi SSTable ga to'kilishi (Flush) kerak.",
        "req": "Threshold tekshiruvi, faol va muzlatilgan (immutable) xotira hovuzlarini ajratish, atomik almashish.",
        "code": """class MemTableManager:
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
        return None""",
        "expl": "Ushbu ikki qatlamli xotira modeli LSM-Tree ning uzluksiz yuqori yozish tezligini (high write throughput) kafolatlaydi. Diskka yozish jarayoni sekin bo'lsa ham, mijozlar yangi bo'shatilgan faol MemTable ga o'z tranzaksiyalarini hech qanday kechikishsiz yozishda davom etaveradi."
    },
    {
        "id": 1204,
        "title": "WAL segmentatsiyasi va eskirgan loglarni tozalash (Log Truncation)",
        "desc": "MemTable diskka SSTable sifatida to'liq yozib bo'lingach, unga tegishli WAL yozuvlari ortiqcha bo'lib qoladi va diskni to'ldirmaslik uchun o'chirilishi lozim.",
        "req": "Segment nomerlash (`wal_00001.log`), flush yakunlangach eski segmentlarni xavfsiz o'chirish yoki arxivlash.",
        "code": """import os
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
                    pass""",
        "expl": "WAL fayllarini cheksiz o'sishiga yo'l qo'ymaslik log truncation orqali amalga oshiriladi. Har safar MemTable diskka SSTable bo'lib flush qilinganda, yangi WAL segmenti ochiladi va bazaning qat'iy holati (checkpoint) qayd etilib, eski loglar o'chiriladi."
    },
    {
        "id": 1205,
        "title": "Avariyadan keyin WAL orqali xotirani to'liq tiklash (Crash Recovery Engine)",
        "desc": "Tizim serveri kutilmaganda o'chib qolsa, qayta ishga tushish vaqtida barcha WAL segmentlarini noldan o'qib, buzilmagan yozuvlarni MemTable ga qayta tiklash zarur.",
        "req": "Buzilgan (corrupt) oxirgi yozuvlarni aniqlash, CRC32 tekshiruvi orqali xatoliklarni ajratish va toza tiklash.",
        "code": """class WalRecoveryEngine:
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

        return recovered_count""",
        "expl": "Crash Recovery dvigateli ma'lumotlar bazasi ishonchliligining (Reliability) kafolatidir. Elektr o'chgan paytda oxirgi yozuv yarimta yozilib qolishi mumkin. CRC tekshiruvi buzilgan yarimta baytlarni darhol fosh qiladi va bazani xavfsiz oxirgi izchil holatgacha tiklaydi."
    },
    {
        "id": 1206,
        "title": "O'chirish amallarini boshqarish: Qabr toshlari (Tombstones) va kechiktirilgan o'chirish",
        "desc": "LSM-Tree dvigatelida diskdagi ma'lumotlarni darhol jismoniy o'chirish imkonsiz (chunki fayllar o'zgarmas). Shu sababli o'chirish amali 'Qabr toshi' (Tombstone) markeri orqali amalga oshiriladi.",
        "req": "Tombstone konstantasini belgilash, `delete` metodida tombstone yozish, `get` paytida o'chirilgan deb qaytarish.",
        "code": """TOMBSTONE_MARKER = b"__DELETED_TOMBSTONE_V1__"

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
        return raw_val.decode("utf-8")""",
        "expl": "Tombstone LSM-Tree ning o'ziga xos arxitektura tamoyilidir. O'chirish ham xuddi yangi ma'lumot kiritish kabi ketma-ket yoziladi. Eski ma'lumotlar esa keyinchalik Compaction (zichlashtirish) jarayonida to'liq yo'q qilinadi."
    },
    {
        "id": 1207,
        "title": "MemTable iteratorlari: Diapazon bo'yicha qidiruv (Range Scan [start, end))",
        "desc": "Foydalanuvchi ma'lum bir prefiks yoki oraliqdagi barcha kalitlarni (masalan `user:100` dan `user:200` gacha) tartiblangan holda o'qishi uchun samarali iterator zarur.",
        "req": "SkipList bo'ylab `start_key` ni topish, `forward[0]` orqali ketma-ket harakatlanish va `end_key` ga yetganda to'xtash.",
        "code": """class MemTableIterator:
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
        return key, val""",
        "expl": "SkipList ning 0-darajasi (bottom level) oddiy bog'langan ro'yxatdir (Linked List). Boshlang'ich nuqtani $O(\\log N)$ da topgandan so'ng, keyingi elementlarni o'qish $O(1)$ tezlikda bo'ladi, bu esa Range Scan so'rovlarini nihoyatda tez bajaradi."
    },
    {
        "id": 1208,
        "title": "Bir vaqtda o'qish va yozish: Immutable MemTable va faol MemTable ajratilishi",
        "desc": "Flush vaqtida diskka yozilayotgan ma'lumotlar bilan yangi kiruvchi so'rovlar o'rtasida ziddiyat yuzaga kelmasligi uchun qulflar (locks) bilan ajratish kerak.",
        "req": "`threading.Lock` yordamida himoyalash, o'qish amallari uchun bloklanmaydigan oqimlar.",
        "code": """import threading

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
            self.flushing = None""",
        "expl": "Faol va o'zgarmas MemTable larni ajratish qulflanish vaqtini (lock contention) minimal darajaga tushiradi. Faqatgina havola (pointer) almashtirilayotgan bir necha nanosekund ichida qulf ushlanadi, og'ir disk amallari esa qulfdan tashqarida bajariladi."
    },
    {
        "id": 1209,
        "title": "WAL fsync siyosatlari: always, every_second, no_sync (Chidamlilik vs Unumdorlik)",
        "desc": "Har bir yozishda `fsync` qilish diskni sekinlashtiradi. MySQL/PostgreSQL kabi turli talablarga mos keluvchi chidamlilik siyosatlarini joriy etish lozim.",
        "req": "Siyosatlar: `ALWAYS` (100% xavfsiz), `EVERY_SECOND` (muvozanatli), `NO_SYNC` (ultra-tezkor).",
        "code": """import time
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
                break""",
        "expl": "Fsync siyosati ACID xususiyatlarining 'Durability' darajasini belgilaydi. `ALWAYS` har bir INSERT da disknikallani kutadi (100-500 IOPS). `EVERY_SECOND` esa sekundiga 100 000 ta operatsiyaga erishishga imkon beradi, biroq to'satdan elektr o'chganda maksimal 1 soniyalik ma'lumot yo'qolishi mumkin."
    },
    {
        "id": 1210,
        "title": "Binary serialization: WAL yozuvlarini ixcham baytlar shaklida qadoqlash",
        "desc": "Disk xotirasini tejash va I/O yuklamasini qisqartirish uchun yozuvlarni Varint (Variable Length Integer) formatida ixcham kodlash kerak.",
        "req": "Protocol Buffers uslubidagi Varint kodlash algoritmi, 64-bitli sonlarni 1-10 bayt oralig'ida siqish.",
        "code": """class VarintEncoder:
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
        return res""",
        "expl": "Standart 64-bit butun son har doim 8 bayt oladi. Varint algoritmi kichik sonlarni (masalan 15 sonini) atigi 1 baytda saqlaydi. Ko'p hollarda kalit va qiymat uzunliklari kichik bo'lgani sababli, Varint jurnali hajmini 40% gacha tejaydi."
    },
    {
        "id": 1211,
        "title": "SSTable fayl formati: Data Block, Index Block, Footer va Magic number",
        "desc": "SSTable (Sorted String Table) diskdagi o'zgarmas asosiy ma'lumotlar konteyneridir. Fayl so'ngida indeks joylashgan va tezkor o'qishga mos format yaratish kerak.",
        "req": "Magic number `0x57746534` (LevelDB), Data Blocklar, Index Block va 48 baytlik Footer strukturasi.",
        "code": """class SSTableLayout:
    # LevelDB standarti: Magic raqami (8 bayt)
    MAGIC_NUMBER = 0xDB4775248B80FB57
    FOOTER_SIZE = 48

    @staticmethod
    def pack_footer(index_offset: int, index_size: int) -> bytes:
        # Metaindex va Index bloklari uchun BlockHandle
        # Format: IndexOffset (8B) + IndexSize (8B) + Magic (8B) + Padding (24B)
        footer = struct.pack(">QQQ", index_offset, index_size, SSTableLayout.MAGIC_NUMBER)
        padding = b"\\x00" * (SSTableLayout.FOOTER_SIZE - len(footer))
        return footer + padding

    @staticmethod
    def unpack_footer(raw_bytes: bytes):
        if len(raw_bytes) != SSTableLayout.FOOTER_SIZE:
            raise ValueError("Footer hajmi noto'g'ri")
        offset, size, magic = struct.unpack(">QQQ", raw_bytes[:24])
        if magic != SSTableLayout.MAGIC_NUMBER:
            raise ValueError("Yaroqsiz SSTable magic raqami!")
        return offset, size""",
        "expl": "SSTable larda indeks har doim fayl oxirida joylashadi. Chunki ma'lumotlar diskka ketma-ket yozilayotganda barcha Data Bloklarning offsetlari faqat oxirida ma'lum bo'ladi. Footer orqali o'quvchi dastur fayl oxiridan 48 bayt o'qib, butun fayl indeksini xotiraga yuklaydi."
    },
    {
        "id": 1212,
        "title": "SSTable Index Block: Sparse Index (siyrak indeks) orqali binar qidiruv",
        "desc": "Har bir kalitni indeksga kiritish RAM ni to'ldirib yuboradi. Har 4KB blok uchun faqat oxirgi kalitni saqlovchi Siyrak Indeks (Sparse Index) yaratish lozim.",
        "req": "Sparse Index yaratish, binary search (`bisect`) yordamida qaysi blokda kalit joylashganligini topish.",
        "code": """import bisect

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
        return None # Kalit mavjud diapazondan katta""",
        "expl": "Siyrak indekslash (Sparse Indexing) xotirani 99% ga tejaydi. 1 milliard yozuv bo'lganda ham, xotirada faqat 10 000 ta blok ko'rsatkichi saqlanadi. Dastur avval indeksdan blokni topadi, so'ng diskdan faqatgina bitta 4KB blokni o'qib qidiradi."
    },
    {
        "id": 1213,
        "title": "SSTable ichida Prefix Compression (kalit prefikslarini siqish)",
        "desc": "Tartiblangan kalitlar ko'pincha umumiy boshlanishga ega bo'ladi (masalan `user:profile:1001`, `user:profile:1002`). Kalit prefikslarini siqib saqlash zarur.",
        "req": "Shared length (umumiy prefiks uzunligi) va Unshared length (qoldiq qism) formatida saqlash.",
        "code": """class PrefixCompressor:
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
        return prev_key[:shared_len] + unshared_part""",
        "expl": "Prefiks siqish algoritmi tartiblangan satrlar bilan ishlaganda hayratlanarli darajada yuqori samaradorlik beradi. Takrorlanuvchi domen nomlari, URL lar yoki prefiksli ID larda SSTable o'lchami 50-70% gacha kichrayadi."
    },
    {
        "id": 1214,
        "title": "SSTable Block Builder: 4KB bloklarga bo'lish va Snappy/ZSTD siqish",
        "desc": "Data Bloklari qat'iy 4096 bayt (OS sahifasi) bo'yicha shakllantirilishi va har bir blok alohida siqilib (compression) diskka yozilishi lozim.",
        "req": "Restart points (qayta tiklash nuqtalari), blok hajmi to'lganda siqish va xom baytlarni qaytarish.",
        "code": """class BlockBuilder:
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
        return bytes(self.buffer)""",
        "expl": "Restart pointlar prefiks siqishining 'Ahilliy tovonini' yo'qotadi. Butun blokni boshidan parslash o'rniga, dastur restart nuqtalari bo'yicha binar sakrab, kerakli kalitni tezda topadi."
    },
    {
        "id": 1215,
        "title": "Ko'p SSTable fayllari bo'ylab binar qidiruv va eng so'nggi versiyani topish",
        "desc": "Kalit bir nechta SSTable fayllarida uchrashi mumkin. Eng yangi fayldan boshlab eng eskisiga qarab qidirish va birinchi topilgan natijani qaytarish lozim.",
        "req": "SSTable ro'yxatini vaqt bo'yicha tartiblash, fayllar bo'ylab qidiruv va topilganda to'xtash.",
        "code": """class SSTableReaderMock:
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
        return None""",
        "expl": "LSM-Tree da eng yangi ma'lumotlar L0 (yuqori daraja) da bo'ladi. Qidiruv yuqoridan pastga qarab boradi. Agar birinchi faylda kalit topilsa (yoki u Tombstone bo'lsa), quyi darajadagi eskirgan fayllarga hatto murojaat ham qilinmaydi."
    },
    {
        "id": 1216,
        "title": "K-Way Merge Iterator: Bir nechta SSTable oqimlarini Min-Heap orqali birlashtirish",
        "desc": "Zichlashtirish (Compaction) yoki keng qamrovli Range Scan qilishda bir nechta tartiblangan fayllarni $O(N \\log K)$ murakkablikda bitta tartiblangan oqimga birlashtirish lozim.",
        "req": "Python `heapq` moduli, Min-Heap elementlari `(key, table_index, value)`, duplikatsiyalarni eng yangi versiya foydasiga hal qilish.",
        "code": """import heapq

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

        raise StopIteration""",
        "expl": "K-Way Merge - tashqi saralash (External Sorting) algoritmlarining poydevoridir. Min-Heap orqali $K$ ta turli fayllardan minimal kalitni tanlash $O(\\log K)$ vaqt oladi. Bu gigabaytlab ma'lumotlarni RAM ga sig'dirmasdan tartiblash imkonini beradi."
    },
    {
        "id": 1217,
        "title": "SSTable Range Query: Diapazon so'rovlarini birlashtirilgan oqimda bajarish",
        "desc": "Barcha diskdagi SSTable fayllari va xotiradagi MemTable ni bitta umumiy Range Iteratorga ulab, berilgan oraliqni so'rov qilish talab etiladi.",
        "req": "MemTable va SSTable iteratorlarini `KWayMergeIterator` ga topshirish, oraliqni filtrlab natijalarni qaytarish.",
        "code": """class UnifiedRangeScanner:
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
        return results""",
        "expl": "Birlashgan diapazon skanerlash dvigateli LSM-Tree ning murakkab ko'p qatlamli tuzilishini foydalanuvchidan to'liq yashiradi. Foydalanuvchi bitta sodda so'rov beradi, ichki tizim esa xotira va diskdagi qatlamlarni birlashtirib sof ma'lumotlarni beradi."
    },
    {
        "id": 1218,
        "title": "Diskka yozilgan SSTable yaxlitligini tekshirish (Block-level Checksums)",
        "desc": "Diskdagi sektorlarning buzilishi (Bit rot / Silent Data Corruption) oqibatida ma'lumotlar o'zgarib ketishini aniqlash uchun har bir blok oxiriga CRC32 yozish va o'qishda tekshirish lozim.",
        "req": "Blok baytlari + CRC32, o'qish paytida tekshiruv, nomutanosiblikda `CorruptedBlockError` tashlash.",
        "code": """class CorruptedBlockError(Exception):
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

        return data""",
        "expl": "Zamonaviy saqlash tizimlari operatsion tizimning drayverlariga ko'r-ko'rona ishonmaydi. Blok darajasidagi cheksunlar apparatdagi magnit/kremniy buzilishlarini darhol fosh qiladi va buzilgan ma'lumotlar mijozga yetib borishining oldini oladi."
    },
    {
        "id": 1219,
        "title": "Manifest fayli: Barcha faol SSTable darajalari va fayllar metama'lumotlari jurnali",
        "desc": "Qaysi SSTable fayllari L0, L1 yoki L2 darajasida ekanligini, qaysi fayllar o'chirilganligini doimiy kuzatib boruvchi VersionSet va Manifest jurnali talab qilinadi.",
        "req": "VersionEdit strukturasini yaratish (yangi fayl qo'shildi, eski fayl o'chirildi), Manifest fayliga yozish.",
        "code": """import json

class VersionEdit:
    def __init__(self):
        self.added_files = []   # (level, file_number, min_key, max_key)
        self.deleted_files = [] # (level, file_number)

    def encode(self) -> bytes:
        payload = {
            "added": self.added_files,
            "deleted": self.deleted_files
        }
        return json.dumps(payload).encode("utf-8") + b"\\n"

class ManifestLogger:
    def __init__(self, manifest_path: str):
        self.file = open(manifest_path, "a+b")

    def log_edit(self, edit: VersionEdit):
        self.file.write(edit.encode())
        self.file.flush()
        os.fsync(self.file.fileno())""",
        "expl": "Manifest fayli LSM-Tree ning 'Konstitutsiyasi'dir. U barcha fayllarning jismoniy holatini saqlaydi. Compaction yakunlanganda atomik VersionEdit yoziladi, bu esa tizim o'chib qolganda fayllarning adashib ketmasligini ta'minlaydi."
    },
    {
        "id": 1220,
        "title": "SSTable fayl nomeri va VersionSet boshqaruvi",
        "desc": "Har bir yangi yaratilayotgan SSTable fayli global tartibdagi unikal raqamga ega bo'lishi (masalan `000042.ldb`) va ketma-ketlik buzilmasligi kerak.",
        "req": "Thread-safe File Number Generator, joriy versiya holatini (Active SSTables ro'yxati) saqlash.",
        "code": """class VersionSet:
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
            self.levels[level].append(file_num)""",
        "expl": "VersionSet xotirada joriy barcha SSTable fayllarining daraxtini ushlab turadi. Har bir yangi fayl unikal raqam oladi va eski raqamlar hech qachon takrorlanmaydi, bu fayl nomlarining ziddiyatini (collision) mutlaqo bartaraf etadi."
    },
    {
        "id": 1221,
        "title": "Size-Tiered Compaction: O'lchami teng bo'lgan SSTablelarni birlashtirish",
        "desc": "Apache Cassandra da qo'llaniladigan ushbu usulda taxminan bir xil hajmga ega bo'lgan 4 ta SSTable paydo bo'lishi bilan ular bitta katta faylga birlashtiriladi.",
        "req": "Hajmlarni tahlil qilish, threshold (4 ta fayl) to'lganda ularni K-Way Merge orqali birlashtirish va yangi kattaroq fayl chiqarish.",
        "code": """class SizeTieredCompactor:
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
        return []""",
        "expl": "Size-Tiered Compaction o'ta yuqori yozish tezligini (high write workload) ta'minlaydi. Fayllar darhol qat'iy tartiblanmaydi, balki o'lchami bo'yicha to'planadi. Bu yozish ko'payishini (Write Amplification) kamaytiradi."
    },
    {
        "id": 1222,
        "title": "Leveled Compaction (LevelDB / RocksDB uslubi): L0 dan L1 ga ko'chirish",
        "desc": "L0 darajasidagi fayllar o'zaro kalitlar bo'yicha kesishadi (overlapping). L1 va undan quyi darajalarda esa har bir darajadagi fayllar kesishmaydigan (non-overlapping) oraliqlarga ega bo'lishi lozim.",
        "req": "L0 dan faylni tanlash, L1 dagi kalitlari kesishuvchi barcha fayllarni topish va ularni birlashtirish.",
        "code": """class LeveledCompactor:
    @staticmethod
    def get_overlapping_files(candidate_min: bytes, candidate_max: bytes, l1_files: list):
        # l1_files: [(file_id, min_key, max_key)]
        overlapping = []
        for fid, min_k, max_k in l1_files:
            if not (candidate_max < min_k or candidate_min > max_k):
                overlapping.append(fid)
        return overlapping""",
        "expl": "Leveled Compaction o'qish unumdorligini (Read Performance) keskin oshiradi. L1, L2, L3 darajalarida fayllar kesishmagani sababli, bitta kalit har bir darajada faqat bitta faylda uchrashi kafolatlanadi. Qidiruv tezligi $O(1)$ disk murojaatiga tushadi."
    },
    {
        "id": 1223,
        "title": "Qabr toshlarini (Tombstone) tozalash: Eng quyi darajada o'chirilgan kalitlarni yo'q qilish",
        "desc": "Agar qabr toshi darhol o'chirib yuborilsa, quyi darajadagi eski qiymat qayta 'tirilib' qolishi mumkin. Qabr toshini faqat u bazaning eng quyi darajasiga (Bottom Level) yetgandagina jismoniy o'chirish lozim.",
        "req": "Kalit eng quyi darajadami yoki undan pastda yana SSTable bormi tekshirish, agar oxirgi daraja bo'lsa o'chirish.",
        "code": """class TombstonePurger:
    @staticmethod
    def can_drop_tombstone(key: bytes, current_level: int, max_level_in_db: int, lower_levels_keys: set) -> bool:
        # Agar eng pastki daraja bo'lsa, xavfsiz o'chirish mumkin
        if current_level >= max_level_in_db:
            return True
        # Yoki undan pastki barcha darajalarda bu kalit umuman yo'q bo'lsa
        if key not in lower_levels_keys:
            return True
        return False""",
        "expl": "Tombstone Garbage Collection LSM-Tree ning eng ehtiyotkor amallaridan biridir. Agar pastki qatlamlarda hali eski versiya mavjud bo'lsa, qabr toshini yo'qotib bo'lmaydi. U faqat barcha eski nusxalarni o'zi bilan 'yondirib' yuborgandagina butunlay yo'q qilinadi."
    },
    {
        "id": 1224,
        "title": "Compaction paytida Disk Write Amplification (yozish ko'payishi) ni minimallashtirish",
        "desc": "Foydalanuvchi 1 MB ma'lumot yozganda, Compaction jarayonlari tufayli diskka jami 10 MB yoki 30 MB yozilishi mumkin (Write Amplification Factor). Uni hisoblash va minimallashtirish algoritmi kerak.",
        "req": "WAF formulasini hisoblash: $\\text{WAF} = \\frac{\\text{Jami diskka yozilgan baytlar}}{\\text{Foydalanuvchi kiritgan baytlar}}$, dinamik limit sozlash.",
        "code": """class WriteAmplificationTracker:
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
        return self.disk_bytes_written / self.user_bytes_written""",
        "expl": "Write Amplification Factor (WAF) SSD disklarining ishlash muddatiga to'g'ridan-to'g'ri ta'sir qiladi. Agar WAF=30 bo'lsa, 1 TB ma'lumot diskka 30 TB bo'lib tushadi va flesh-hujayralarni tez qaritadi. LSM-Tree ni sozlashda WAF ni 5-10 atrofida ushlab turish asosiy maqsaddir."
    },
    {
        "id": 1225,
        "title": "Compaction Picker: Qaysi fayllarni zichlashtirish kerakligini aniqlovchi algoritm",
        "desc": "Dvigatel qaysi darajada limit oshib ketganini (Score) hisoblab, eng kritik darajani birinchi navbatda zichlashtirish uchun tanlashi lozim.",
        "req": "Har bir daraja uchun `score = current_size / max_size` hisoblash, Score > 1.0 bo'lgan eng katta darajani tanlash.",
        "code": """class CompactionPicker:
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

        return best_level, best_score""",
        "expl": "Compaction Picker tizimdagi muvozanatni saqlaydi. Agar L0 da fayllar ko'payib ketsa, qidiruv sekinlashadi, shuning uchun L0 har doim eng yuqori ustuvorlikka (priority) ega bo'ladi."
    }
]
