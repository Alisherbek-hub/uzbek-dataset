# -*- coding: utf-8 -*-
"""
Python 25-modul: 1226 dan 1250 gacha bo'lgan topshiriqlar
Compaction, Bitcask Storage Engine, Bloom Filters va B+Tree / Buffer Pool
"""

TASKS_1226_1250 = [
    {
        "id": 1226,
        "title": "Asinxron fon zichlashtiruvchisi (Background Compaction Worker)",
        "desc": "Zichlashtirish (Compaction) jarayoni gigabaytlab ma'lumotlarni o'qib-yozgani uchun u alohida fonda (Background Worker Thread) mijozlarning `put`/`get` so'rovlariga to'sqinlik qilmasdan ishlashi shart.",
        "req": "`threading.Thread` va `queue.Queue` orqali vazifalarni qabul qilish, fon ishini boshqarish va to'xtatish.",
        "code": """import threading
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
        self.worker_thread.join()""",
        "expl": "Background Compaction worker dvigatelning barqaror ishlashini ta'minlaydi. Mijozlar o'zlarining tranzaksiyalarini bajarishda davom etadi, fon oqimi esa eski fayllarni saralab yangi darajaga ko'chirib turadi."
    },
    {
        "id": 1227,
        "title": "Zichlashtirish paytida o'qish va yozishni to'xtatmaslin (Non-blocking snapshots)",
        "desc": "Compaction paytida eski SSTable fayllari o'chirilayotganda, ularni o'qiyotgan faol so'rovlar (Snapshots) xatoga uchramasligi (Read-after-delete) lozim.",
        "req": "Reference Counting (havolalar hisoblagichi) yoki File Descriptor pinning mexanizmini joriy etish.",
        "code": """class TrackedSSTable:
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
        print(f"[O'CHIRILDI] SSTable #{self.file_id} jismoniy diskdan o'chirildi")""",
        "expl": "Reference Counting LSM-Tree da xavfsiz xotira tozalashni ta'minlaydi. Compaction eski faylni `obsolete` (eskirgan) deb belgilaydi, ammo agar biron foydalanuvchi hozirda o'sha fayldan ma'lumot o'qiyotgan bo'lsa (`ref_count > 0`), fayl o'chirilmaydi. O'quvchi o'z ishini tugatgandagina fayl jismonan diskdan yo'qotiladi."
    },
    {
        "id": 1228,
        "title": "Read Amplification (o'qish ko'payishi) ni baholash va tahlil qilish",
        "desc": "Bitta `get(key)` so'rovi uchun tizim necha marta diskka murojaat qilayotganligini (Read Amplification) o'lchash va Bloom Filter yordamida uni kamaytirish zarur.",
        "req": "Diskka murojaatlar sonini hisoblash, RAF = Disk Reads / Logical Reads formulasini joriy etish.",
        "code": """class ReadAmplificationTracker:
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
        return self.disk_block_reads / self.logical_gets""",
        "expl": "B+Tree larda Read Amplification juda past (3-4 ta disk murojaati). LSM-Tree larda esa har bir darajada fayllar bo'lgani sababli RAF 20-30 gacha yetishi mumkin. Bloom Filter va Block Cache lar yordamida bu ko'rsatkich amalda 1.1 - 1.5 ga tushiriladi."
    },
    {
        "id": 1229,
        "title": "Dynamic Level Size Multiplier (L_i = 10 * L_{i-1})",
        "desc": "Har bir quyi daraja o'zidan yuqoridagi darajadan 10 barobar ko'proq ma'lumot saqlashi lozim: L1=10MB, L2=100MB, L3=1GB, L4=10GB.",
        "req": "Multiplikator (T=10), darajalar hajmini avtomatik hisoblash va dinamik moslashuvchanlik.",
        "code": """class LevelHierarchyCalculator:
    def __init__(self, base_level_mb: int = 10, multiplier: int = 10, max_levels: int = 7):
        self.base_level = base_level_mb
        self.multiplier = multiplier
        self.max_levels = max_levels

    def get_capacity_mb(self, level: int) -> int:
        if level == 0:
            return self.base_level # L0 odatda L1 ga teng bo'ladi
        return self.base_level * (self.multiplier ** (level - 1))""",
        "expl": "Eksponentsial o'sish geometriyasi sababli barcha ma'lumotlarning 90% i eng quyi darajada (masalan L4 yoki L5 da) joylashadi. Bu esa xotirani rejalashtirish va qidiruv chuqurligini chegaralash imkonini beradi."
    },
    {
        "id": 1230,
        "title": "Favqulodda to'xtatish: Yozish tezligi zichlashtirishdan oshib ketganda Write Stall mexanizmi",
        "desc": "Mijozlar yozish tezligi diskning zichlashtirish (Compaction) quvvatidan oshib ketsa, L0 da yuzlab fayllar to'planib qolib tizim qulashi mumkin. Bu vaqtda kiruvchi yozishlarni majburiy sekinlashtirish (Write Stall) kerak.",
        "req": "L0 fayllar soni > 8 bo'lsa sun'iy 1 ms kechikish kiritish, soni > 20 bo'lsa so'rovlarni butunlay to'xtatib turish.",
        "code": """class WriteStallController:
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
        return "OK" """,
        "expl": "Write Stall LSM-Tree larning o'z-o'zini asrash tizimidir (Backpressure). U mijozlarning shiddatini sekinlashtirib, fon disk jarayonlariga ma'lumotlarni tartibga keltirib olish uchun imkoniyat yaratadi."
    },
    {
        "id": 1231,
        "title": "Bitcask arxitekturasi: Append-only log va xotiradagi Hash Index (Keydir)",
        "desc": "Bitcask - Erlang va Riak da qo'llaniluvchi ultra-sodda va o'ta tezkor saqlash dvigatelidir. Barcha kalitlar va ularning diskdagi ofsetlari xotiradagi Hash Table da (Keydir) saqlanadi.",
        "req": "Keydir xotira lug'ati: `key => (file_id, value_size, value_offset, timestamp)`, $O(1)$ disk murojaati.",
        "code": """class BitcaskKeydirEntry:
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
        return self.index.get(key)""",
        "expl": "Bitcask ning asosiy afzalligi: Har qanday GET operatsiyasi atigi 1 ta disk murojaatini (1 disk seek) talab qiladi, chunki kalitning fayldagi aniq joylashuvi (offset) allaqachon RAM dagi hash-jadvalda ma'lum."
    },
    {
        "id": 1232,
        "title": "Bitcask yozuv formati: CRC, Timestamp, KeySz, ValueSz, Key, Value",
        "desc": "Bitcask faylidagi har bir yozuv qat'iy binar struktura bo'yicha diskka append-only qilib yozilishi shart.",
        "req": "Format: `[CRC: 4B][Timestamp: 4B][KeySz: 2B][ValSz: 4B][Key][Value]`, yozuvni qadoqlash va diskka chiqarish.",
        "code": """class BitcaskRecordCodec:
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
        return header + payload""",
        "expl": "Ushbu format xotira faylining o'zini o'zi tushuntiruvchi (self-describing) bo'lishini ta'minlaydi. Server buzilib qayta yoqilganda barcha fayllar boshidan oxirigacha o'qilib, xotiradagi Keydir noldan bir necha soniyada tiklanadi."
    },
    {
        "id": 1233,
        "title": "Bitcask Get operatsiyasi: Xotiradan fayl offsetini topib os.pread orqali o'qish",
        "desc": "Keydir dan ofset olingach, fayl ko'rsatkichini (seek) siljitmasdan, ko'p oqimli rejimda xavfsiz `os.pread` yordamida to'g'ridan-to'g'ri qiymatni o'qib olish lozim.",
        "req": "`os.pread(fd, length, offset)` dan foydalanish, ko'p oqimlar uchun qulflarsiz xavfsiz o'qish.",
        "code": """class BitcaskReader:
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
        return raw_val""",
        "expl": "`os.pread` (POSIX pread) standart `f.seek()` va `f.read()` ga qaraganda parallel tizimlarda ancha ustundir. Bir vaqtda 100 ta oqim bitta ochiq fayl deskriptoridan turli ofsetlar bo'yicha bir-biriga xalaqit bermasdan parallel ma'lumot o'qiydi."
    },
    {
        "id": 1234,
        "title": "Bitcask Merge & Compaction: Eskirgan qiymatlarni olib tashlab yangi fayllarga yozish",
        "desc": "Append-only modelida bitta kalit 100 marta o'zgartirilsa, diskda 100 ta yozuv paydo bo'ladi. Eski yozuvlarni tozalab, faqat eng so'nggi qiymatlarni yangi ixcham faylga ko'chirish kerak.",
        "req": "Barcha muzlatilgan log fayllarini o'qish, Keydir dagi joriy ofset bilan solishtirish, faqat faol yozuvlarni yangi faylga ko'chirish.",
        "code": """class BitcaskMerger:
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
                    pos += BitcaskRecordCodec.HEADER_SIZE + ksz + vsz""",
        "expl": "Bitcask Merge jarayoni disk maydonini qayta tiklaydi. Eskirgan va o'chirilgan barcha yozuvlar tashlab ketiladi, natijada disk hajmi 80-90% gacha bo'shaydi."
    },
    {
        "id": 1235,
        "title": "Hint fayllari: Server qayta yonganda tez yuklanish uchun faqat kalit va offsetlarni saqlash",
        "desc": "Merge dan so'ng ulkan ma'lumot fayllarini qayta parslash o'rniga, faqatgina kalitlar va ularning ofsetlarini saqlovchi maxsus 'Hint' (maslahat) fayli yaratiladi.",
        "req": "Hint fayli formati: `[Timestamp][KeySz][ValSz][ValPos][Key]`, server ishga tushganda faqat hint faylini o'qib Keydir ni bir zumda tiklash.",
        "code": """class BitcaskHintFile:
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
                keydir.put(key, file_id, vsz, vpos, ts)""",
        "expl": "Hint fayllari Bitcask ning o'ziga xos ixtirosidir. Gigabaytlab qiymatlarni (Values) chetlab o'tib, faqat ixcham Hint fayli o'qiladi. Natijada 100 GB hajmdagi baza server qayta yonganda atigi 1-2 soniyada to'liq ishchi holatga keladi."
    },
    {
        "id": 1236,
        "title": "Bitcask fayl rotatsiyasi: 100 MB ga yetganda faol faylni muzlatib yangi fayl ochish",
        "desc": "Bitta fayl haddan tashqari ulkan bo'lib ketmasligi uchun joriy faol fayl 100 MB ga yetganda u faqat o'qish (Read-Only) rejimiga o'tkazilib, yangi faol fayl ochilishi kerak.",
        "req": "Fayl hajmini kuzatish, yangi `file_id` generatsiyasi va xavfsiz almashish.",
        "code": """class BitcaskFileManager:
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
        return self.active_file_id, pos""",
        "expl": "Fayl rotatsiyasi parallel zichlashtirish (Compaction) uchun zarur shartdir. Qadimgi fayllar o'zgarmas holatda qolgani sababli, fondagi Merger ularni xavfsiz o'qib tozalashi mumkin."
    },
    {
        "id": 1237,
        "title": "Bitcask Delete: Qiymat uzunligi -1 yoki maxsus tombstone bilan logga yozish",
        "desc": "Bitcask da ma'lumotni o'chirish log fayliga maxsus o'chirish belgisi yozish va Keydir dan kalitni olib tashlash orqali amalga oshiriladi.",
        "req": "Tombstone yozish, `keydir.pop(key)` chaqirish, o'chirilgan yozuv keyingi so'rovlarda topilmasligi.",
        "code": """class BitcaskStore:
    def __init__(self, file_mgr: BitcaskFileManager, keydir: BitcaskKeydir):
        self.file_mgr = file_mgr
        self.keydir = keydir

    def delete(self, key: bytes):
        # Qiymat sifatida bo'sh bayt va maxsus o'chirish yozuvi
        rec = BitcaskRecordCodec.encode_record(key, TOMBSTONE_MARKER)
        self.file_mgr.write_record(rec)
        # Xotiradagi indeksdan olib tashlaymiz
        self.keydir.index.pop(key, None)""",
        "expl": "Keydir dan kalit o'chirilishi bilanoq, keyingi barcha `get` so'rovlari 0 soniyada 'Not Found' qaytaradi. Diskdagi tombstone yozuvi esa faqat keyingi Merge paytida eski yozuvlar bilan birga tozalab tashlanadi."
    },
    {
        "id": 1238,
        "title": "Bitcask Crash Recovery: Barcha log fayllarini ketma-ket o'qib Keydir ni qayta tiklash",
        "desc": "Hint fayllari bo'lmagan taqdirda, barcha mavjud `.bitcask` ma'lumot fayllarini tartib bilan o'qib, xotiradagi indeksni to'liq tiklash lozim.",
        "req": "Fayllarni vaqt/id bo'yicha saralash, har bir yozuvni o'qish, eng so'nggi ofsetlarni Keydir ga kiritish.",
        "code": """class BitcaskCrashRecovery:
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
                    pos += BitcaskRecordCodec.HEADER_SIZE + ksz + vsz""",
        "expl": "Append-only jurnallarning go'zalligi shundaki, eng so'nggi operatsiya avtomatik tarzda eski operatsiyalarning ustiga yoziladi (overwrite). Hech qanday murakkab tiklash algoritmlari talab qilinmaydi."
    },
    {
        "id": 1239,
        "title": "Bitcask Range Query cheklovlari va ularni yengish usullari",
        "desc": "Bitcask ning eng katta kamchiligi - uning kalitlari xotirada tartiblanmagan (Hash Map) bo'lishidir. Range Query (`start_key` dan `end_key` gacha) amallarini bajarish uchun xotirada qo'shimcha tartiblangan indeks yaratish kerak.",
        "req": "B-Tree yoki Sorted List ni parallel yuritish, oraliq so'rovlarini tartiblangan kalitlar ro'yxatidan bajarish.",
        "code": """class BitcaskWithRangeScan:
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
        return self.sorted_keys[idx_start:idx_end]""",
        "expl": "Oddiy Bitcask faqat Point Query (`get/put`) uchun mo'ljallangan. Ammo xotirada qo'shimcha `sorted_keys` massivini saqlash orqali unga Range Scan imkoniyatini ham qo'shish mumkin, biroq bu xotira sarfini 20% ga oshiradi."
    },
    {
        "id": 1240,
        "title": "Bitcask va LSM-Tree solishtirmasi: Disk va xotira balansi",
        "desc": "Dasturiy arxitekturada qachon Bitcask va qachon LSM-Tree tanlanishi kerakligini tahlil qiluvchi taqqoslash modeli.",
        "req": "RAM sarfi va disk IOPS ni solishtiruvchi hisoblagich, to'g'ri storage engine tanlash tavsiyanomasi.",
        "code": """class StorageEngineSelector:
    @staticmethod
    def evaluate(workload: dict) -> str:
        # workload: {total_keys, avg_val_size, ram_budget_gb, needs_range_scans}
        ram_needed_bitcask_gb = (workload["total_keys"] * 32) / (1024**3)
        
        if workload["needs_range_scans"]:
            return "LSM-Tree (RocksDB/LevelDB) - Chunki SSTable va MemTable tartiblangan"
        
        if ram_needed_bitcask_gb <= workload["ram_budget_gb"]:
            return "Bitcask - O'ta past kechikish (1 Disk Seek) va maksimal yozish tezligi"
        else:
            return "LSM-Tree - Kalitlar xotiraga sig'maydi, Sparse Index talab qilinadi" """,
        "expl": "Bitcask agar barcha kalitlar operativ xotiraga sig'sa (masalan 100 million kalit = 3.2 GB RAM) dunyodagi eng tezkor dvigateldir. Agar kalitlar milliardlab bo'lsa yoki murakkab oraliq so'rovlari kerak bo'lsa, LSM-Tree yagona tanlov hisoblanadi."
    },
    {
        "id": 1241,
        "title": "Bloom Filter: Murakkab matematik hash funksiyalari (Murmur3) bilan kalit mavjudligini tezkor tekshirish",
        "desc": "Diskdagi SSTable ichida kalit yo'q bo'lsa, behuda diskni o'qimaslik uchun 99% aniqlik bilan 'Bu kalit faylda aniq yo'q' deb javob beruvchi Bloom Filter yaratish kerak.",
        "req": "Bit massivi, $k$ ta mustaqil xesh funksiyalari (Kirsch-Mitzenmacher texnikasi: $h_i(x) = h_1(x) + i \\cdot h_2(x)$), `add` va `contains` metodlari.",
        "code": """class BloomFilter:
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
        return True # Bo'lishi mumkin (False positive ehtimoli bor)""",
        "expl": "Bloom Filter LSM-Tree larning eng mo''jizaviy komponentidir. Agar Bloom Filter 'YO'Q' desa, kalit diskda 100% yo'q va SSTable faylini ochish shart emas. Bu mavjud bo'lmagan kalitlarni qidirishda disk I/O sarfini deyarli nolga tushiradi."
    },
    {
        "id": 1242,
        "title": "Bloom Filter False Positive ehtimolligini hisoblash va optimal bit massivi hajmi",
        "desc": "Kutilayotgan elementlar soni $n$ va qabul qilinuvchi xato ehtimolligi $p=0.01$ (1%) bo'lganda, optimal bit massivi hajmi $m$ va xeshlar soni $k$ ni hisoblovchi formula.",
        "req": "Formulalar: $m = -\\frac{n \\ln p}{(\\ln 2)^2}$, $k = \\frac{m}{n} \\ln 2$. Har bir element uchun bitlar soni (~10 bit).",
        "code": """import math

class OptimalBloomCalculator:
    @staticmethod
    def calculate_params(expected_elements: int, false_positive_rate: float = 0.01):
        # m = - (n * ln(p)) / (ln(2)^2)
        m = - (expected_elements * math.log(false_positive_rate)) / (math.log(2) ** 2)
        # k = (m / n) * ln(2)
        k = (m / expected_elements) * math.log(2)
        
        bits_per_element = m / expected_elements
        return int(math.ceil(m)), int(math.ceil(k)), bits_per_element""",
        "expl": "Matematika shuni ko'rsatadiki, har bir kalit uchun atigi 10 bit xotira ajratilsa va 7 ta xesh funksiya ishlatilsa, xato qilish (False Positive) ehtimoli roppa-rosa 1% ni tashkil qiladi. Ya'ni 99 ta keraksiz disk murojaati to'xtatiladi."
    },
    {
        "id": 1243,
        "title": "B+Tree Node strukturasi: Leaf va Internal tugunlar, kalitlar va ko'rsatkichlar",
        "desc": "Relyatsion ma'lumotlar bazalarining (PostgreSQL, InnoDB) asosi bo'lgan B+Tree daraxtini qurish: Barg tugunlar (faqat ma'lumot saqlovchi) va Ichki yo'naltiruvchi tugunlar arxitekturasi.",
        "req": "Maksimal sig'im (Degree $M=4$), `is_leaf` bayrog'i, `keys` va `children` massivlari.",
        "code": """class BPlusNode:
    def __init__(self, is_leaf: bool = False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = [] # Agar leaf bo'lsa qiymatlar, bo'lmasa BPlusNode obyektlari
        self.next = None   # Leaf larni bir-biriga bog'lovchi Linked List ko'rsatkichi""",
        "expl": "Klassik B-Tree dan farqli ravishda, B+Tree da barcha haqiqiy qiymatlar faqat barglarda (Leaf nodes) saqlanadi. Ichki tugunlar faqat yo'l ko'rsatuvchi kalitlarni saqlaydi, bu esa ichki tugunlarning zichligini oshirib, daraxt balandligini 3-4 darajada ushlab turadi."
    },
    {
        "id": 1244,
        "title": "B+Tree Insert: Tugun to'lganda o'rtasidan bo'lish (Node Splitting)",
        "desc": "Tugun sig'imi (Degree) to'lganda, u ikkita teng yarmiga bo'linadi (split) va o'rta kalit ota-tugunga (parent) ko'tariladi.",
        "req": "Tugunni bo'lish algoritmi, yangi ildiz (Root) yaratish agar ildiz bo'linsa, barglar o'rtasida bog'langan ro'yxatni saqlash.",
        "code": """class BPlusTree:
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
            self._insert_non_full(child, key, value)""",
        "expl": "B+Tree pastdan yuqoriga qarab o'sadi. Faqat ildiz bo'lingandagina daraxtning balandligi 1 ga oshadi. Bu barcha barglarning har doim mutlaqo bir xil chuqurlikda bo'lishini (Strict Balance) kafolatlaydi."
    },
    {
        "id": 1245,
        "title": "B+Tree Search: Ildizdan barggacha O(log N) binar qidiruv",
        "desc": "Ildizdan boshlab har bir ichki tugunda binar qidiruv bilan to'g'ri bolaga o'tib, barg tuguniga yetib borish va kalit qiymatini olish.",
        "req": "Rekursiv yoki iterativ qidiruv, $O(\\log N)$ murakkablik, kalit topilmasa `None` qaytarish.",
        "code": """    def search(self, key):
        current = self.root
        while not current.is_leaf:
            idx = bisect.bisect_right(current.keys, key)
            current = current.children[idx]

        idx = bisect.bisect_left(current.keys, key)
        if idx < len(current.keys) and current.keys[idx] == key:
            return current.children[idx]
        return None""",
        "expl": "B+Tree qidiruvida har bir ichki tugun 100-500 ta kalitni saqlashi mumkin. 1 milliard yozuv bo'lganda ham daraxt balandligi atigi 3 yoki 4 bo'ladi, ya'ni xohlagan yozuvni topish uchun atigi 3 ta qadam yetarli."
    },
    {
        "id": 1246,
        "title": "B+Tree Leaf Linked List: Qatorli skanerlash (Sequential Range Scan)",
        "desc": "B+Tree ning oddiy B-Tree dan eng katta ustunligi: Barcha barglar bir-biriga zanjir bo'lib ulangan (`next` ko'rsatkichi). Qidiruv boshlangach, daraxtni qayta aylanmasdan to'g'ridan-to'g'ri zanjir bo'ylab yurish mumkin.",
        "req": "Oraliq qidiruv `[start, end]`, birinchi bargni topish va `node.next` bo'ylab yig'ish.",
        "code": """    def range_scan(self, start_key, end_key):
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
        return results""",
        "expl": "B+Tree ning barglari zanjirli bo'lgani uchun SQL dagi `WHERE age BETWEEN 20 AND 30` so'rovlari o'ta yuqori tezlikda bajariladi. Daraxt bo'ylab qayta tushib-chiqishga hojat yo'q, barglar o'zi ketma-ket ro'yxatdir."
    },
    {
        "id": 1247,
        "title": "Buffer Pool Manager: Disk sahifalarini (Pages) xotirada ushlab turuvchi bufer hovuzi",
        "desc": "Ma'lumotlar bazasi har safar diskka bormasligi uchun 4KB li disk sahifalarini xotiradagi doimiy bufer hovuzida (Buffer Pool) boshqarish talab etiladi.",
        "req": "Frame massivi, Page Table (`page_id => frame_id`), sahifani xotiraga pin qilish (pin_count) va unpin qilish.",
        "code": """class BufferFrame:
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
                frame.is_dirty = True""",
        "expl": "Buffer Pool Manager PostgreSQL va MySQL InnoDB ning eng muhim organidir. U operatsion tizimning keshiga tayanmasdan, qaysi sahifa o'zgarganligi (dirty) va qaysi sahifa ayni paytda o'qilayotganligini (`pin_count`) o'zi qat'iy nazorat qiladi."
    },
    {
        "id": 1248,
        "title": "LRU-K (LRU-2) sahifalarni almashtirish (Eviction) siyosati",
        "desc": "Klassik LRU bir marta butun jadvalni skanerlaganda (Sequential Scan) barcha foydali keshni yuvib yuboradi (Cache Pollution). Oxirgi $K=2$ ta murojaat vaqtini hisobga oluvchi LRU-2 algoritmini joriy etish lozim.",
        "req": "Har bir sahifa uchun oxirgi 2 ta murojaat vaqtini saqlash, 2 marta murojaat qilinmagan sahifalarni birinchi navbatda keshdan haydash.",
        "code": """class LRU2Replacer:
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
        return oldest_frame""",
        "expl": "LRU-2 algoritmi 'Bir martalik so'rovlar' (Sequential Scan pollution) balosidan keshni to'liq himoya qiladi. Agar biron so'rov butun 10 GB li jadvalni o'qib chiqsa ham, sahifalarga ikkinchi marta murojaat bo'lmasa, ular asosiy keshdagi doimiy issiq ma'lumotlarni chiqarib yubora olmaydi."
    },
    {
        "id": 1249,
        "title": "Dirty Pages Flush va Checkpointing: O'zgargan sahifalarni diskka atomar yozish",
        "desc": "Xotirada o'zgartirilgan 'iflos' (Dirty) sahifalarni vaqti-vaqti bilan diskka yozib, WAL jurnalini qisqartirish uchun Checkpoint tizimi zarur.",
        "req": "Barcha `is_dirty == True` va `pin_count == 0` bo'lgan sahifalarni topish, diskka yozish va bayroqni tozalash.",
        "code": """class CheckpointManager:
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
        print(f"[CHECKPOINT] {flushed_pages} ta iflos sahifa diskka xavfsiz saqlandi")""",
        "expl": "Checkpoint operatsiyasi ma'lumotlar bazasining qayta tiklanish vaqtini (Recovery Time Objective - RTO) bir necha soatdan bir necha soniyaga qisqartiradi. Tizim o'chib qolsa, faqat oxirgi Checkpoint dan keyingi WAL yozuvlari o'qiladi."
    },
    {
        "id": 1250,
        "title": "To'liq integratsiyalashgan gibrid Storage Engine (LSM-Tree + Bloom Filter + Buffer Cache)",
        "desc": "Barcha komponentlarni: MemTable, Bloom Filter, SSTable va K-Way Merge ni yagona ishlab chiqarishga tayyor (production-ready) yuqori unumdor saqlash dvigateliga birlashtirish.",
        "req": "Kompakt API: `put`, `get`, `delete`, `flush`, xotira nazorati va kiber-chidamlilik testi.",
        "code": """class EnterpriseStorageEngine:
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
        print("[ENGINE] MemTable muvaffaqiyatli diskka to'kildi!")""",
        "expl": "Ushbu arxitektura zamonaviy Big Data ma'lumotlar bazalarining (Google Bigtable, Apache Cassandra, RocksDB) asosidir. Yozishlar xotiradagi SkipList ga $O(1)$ tezlikda tushadi, o'qishlar esa Bloom Filter orqali disk I/O ni chetlab o'tadi, natijada dvigatel soniyasiga yuz minglab operatsiyalarni bemalol qayta ishlaydi."
    }
]
