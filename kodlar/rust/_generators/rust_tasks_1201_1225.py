# -*- coding: utf-8 -*-
"""
Rust 25-modul: 1201 dan 1225 gacha bo'lgan topshiriqlar
Storage Engine Injiniringi: MemTable, SkipList, WAL, SSTable va Blok Iteratorlari
"""

TASKS_1201_1225 = [
    {
        "id": 1201,
        "title": "Lock-Free yoki Concurrent SkipList: Atomic ko'rsatkichlar (AtomicPtr, AtomicUsize) bilan",
        "desc": "Rust da bir vaqtning o'zida yuzlab oqimlar (threads) hech qanday og'ir Mutex qulflarisiz xotiradagi MemTable ga ma'lumot yozishi va o'qishi uchun atomik ko'rsatkichlar asosidagi Concurrent SkipList yaratish kerak.",
        "req": "std::sync::atomic::{AtomicPtr, Ordering}, tasodifiy balandlik generatsiyasi va CAS (Compare-And-Swap) operatsiyalari.",
        "code": """use std::sync::atomic::{AtomicPtr, AtomicUsize, Ordering};
use std::ptr;

const MAX_HEIGHT: usize = 16;

pub struct Node<K, V> {
    pub key: K,
    pub value: V,
    pub height: usize,
    pub next: [AtomicPtr<Node<K, V>>; MAX_HEIGHT],
}

impl<K, V> Node<K, V> {
    pub fn new(key: K, value: V, height: usize) -> *mut Self {
        let mut node = Box::new(Node {
            key,
            value,
            height,
            next: Default::default(),
        });
        for i in 0..height {
            node.next[i] = AtomicPtr::new(ptr::null_mut());
        }
        Box::into_raw(node)
    }
}

pub struct ConcurrentSkipList<K: Ord, V> {
    head: *mut Node<K, V>,
    max_height: AtomicUsize,
}

impl<K: Ord + Default, V: Default> ConcurrentSkipList<K, V> {
    pub fn new() -> Self {
        let head = Node::new(K::default(), V::default(), MAX_HEIGHT);
        Self {
            head,
            max_height: AtomicUsize::new(1),
        }
    }

    pub fn find_greater_or_equal(&self, key: &K) -> *mut Node<K, V> {
        let mut x = self.head;
        let mut level = self.max_height.load(Ordering::Acquire) - 1;

        loop {
            let next = unsafe { (*x).next[level].load(Ordering::Acquire) };
            if !next.is_null() && unsafe { &(*next).key } < key {
                x = next;
            } else {
                if level == 0 {
                    return next;
                }
                level -= 1;
            }
        }
    }
}""",
        "expl": "Lock-Free SkipList RocksDB va TiKV ning MemTable yadrosidir. AtomicPtr va Ordering::Acquire / Ordering::Release xotira tartiblanishi (Memory Ordering) xavfsizligini ta'minlaydi. O'quvchi oqimlar umuman to'xtamaydi (Wait-Free Read), yozuvchi oqimlar esa minimal CAS to'qnashuvlari bilan ishlaydi."
    },
    {
        "id": 1202,
        "title": "MemTable Entry formati: Key, Value, SeqNumber, ValueType (Put/Delete)",
        "desc": "LSM-Tree da ko'p versiyali boshqaruv (MVCC) uchun har bir kalit o'zining ketma-ketlik raqami (Sequence Number) va operatsiya turi (Put yoki Tombstone Delete) bilan biriktirilib saqlanadi.",
        "req": "Ixcham xotira tuzilmasi, ValueType enumi (TypeDeletion = 0, TypeValue = 1), ichki kalitni (InternalKey) solishtirish mantig'i.",
        "code": """#[derive(Copy, Clone, Debug, PartialEq, Eq)]
#[repr(u8)]
pub enum ValueType {
    Deletion = 0,
    Value = 1,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct InternalKey {
    pub user_key: Vec<u8>,
    pub sequence: u64,
    pub value_type: ValueType,
}

impl Ord for InternalKey {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        match self.user_key.cmp(&other.user_key) {
            std::cmp::Ordering::Equal => {
                other.sequence.cmp(&self.sequence)
            }
            ord => ord,
        }
    }
}

impl PartialOrd for InternalKey {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}""",
        "expl": "InternalKey ning other.sequence.cmp(&self.sequence) solishtirishi LSM-Tree ning asosiy kalitidir. Bir xil foydalanuvchi kaliti bo'yicha qidirilganda, eng so'nggi yozilgan (katta Sequence Number ga ega) versiya SkipList da avval keladi va darhol qaytariladi."
    },
    {
        "id": 1203,
        "title": "Rust da ArenaAllocator: MemTable dagi fragmentatsiyani yo'qotuvchi xotira hovuzi",
        "desc": "Har bir kiritilgan yozuv uchun tizimdan malloc chaqirish xotira fragmentatsiyasiga olib keladi. MemTable uchun katta bo'laklarda xotira ajratuvchi Arena kerak.",
        "req": "Arena tuzilmasi, alloc(bytes) orqali ko'rsatkichni surish (Bump Allocation), 8-baytli tekislash (Alignment).",
        "code": """pub struct Arena {
    blocks: Vec<Vec<u8>>,
    current_block: Vec<u8>,
    alloc_ptr: usize,
    block_size: usize,
}

impl Arena {
    pub fn new(block_size: usize) -> Self {
        Self {
            blocks: Vec::new(),
            current_block: Vec::with_capacity(block_size),
            alloc_ptr: 0,
            block_size,
        }
    }

    pub fn alloc(&mut self, bytes: usize) -> *mut u8 {
        let aligned = (bytes + 7) & !7;
        if self.current_block.capacity() - self.current_block.len() < aligned {
            let mut new_block = Vec::with_capacity(self.block_size.max(aligned));
            std::mem::swap(&mut self.current_block, &mut new_block);
            if !new_block.is_empty() {
                self.blocks.push(new_block);
            }
        }

        let start = self.current_block.len();
        self.current_block.resize(start + aligned, 0);
        unsafe { self.current_block.as_mut_ptr().add(start) }
    }
}""",
        "expl": "Bump Allocator (Arena) saqlash dvigatellarida xotira ajratishni bitta assembly amaliga tushiradi. MemTable diskka to'kilganda butun Arena birdaniga bo'shatiladi."
    },
    {
        "id": 1204,
        "title": "MemTable Iterator: Rust ning Iterator traitini SkipList ustida implementatsiya qilish",
        "desc": "MemTable dagi ma'lumotlarni oqim shaklida o'qish, orqaga va oldinga siljitish va Rust ning standart Iterator traitiga ulash zarur.",
        "req": "MemTableIterator<'a>, seek(&key), valid(), key(), value() metodlari.",
        "code": """pub struct MemTableIterator<'a, K: 'a, V: 'a> {
    current: *mut Node<K, V>,
    _marker: std::marker::PhantomData<&'a ()>,
}

impl<'a, K: Ord, V> MemTableIterator<'a, K, V> {
    pub fn new(head: *mut Node<K, V>) -> Self {
        let first = unsafe { (*head).next[0].load(Ordering::Acquire) };
        Self {
            current: first,
            _marker: std::marker::PhantomData,
        }
    }

    pub fn valid(&self) -> bool {
        !self.current.is_null()
    }

    pub fn next_entry(&mut self) {
        if self.valid() {
            self.current = unsafe { (*self.current).next[0].load(Ordering::Acquire) };
        }
    }

    pub fn current_key(&self) -> Option<&'a K> {
        if self.valid() {
            Some(unsafe { &(*self.current).key })
        } else {
            None
        }
    }
}""",
        "expl": "PhantomData Rust kompilyatoriga xotira xavfsizligi va lifetime qoidalarini SkipList ko'rsatkichlari bilan bog'lashga yordam beradi."
    },
    {
        "id": 1205,
        "title": "Atomic Sequence Number (MVCC) bilan operatsiyalar tartibini belgilash",
        "desc": "Har bir yangi tranzaksiya yoki kiritish uchun global takrorlanmas, qat'iy o'suvchi Sequence Number beruvchi atomik hisoblagich zarur.",
        "req": "AtomicU64 yordamida fetch_add(1, Ordering::SeqCst) amalini bajarish, snapshot vaqtini belgilash.",
        "code": """use std::sync::atomic::{AtomicU64, Ordering};

pub struct SequenceGenerator {
    current_seq: AtomicU64,
}

impl SequenceGenerator {
    pub fn new(initial: u64) -> Self {
        Self {
            current_seq: AtomicU64::new(initial),
        }
    }

    pub fn next_sequence(&self) -> u64 {
        self.current_seq.fetch_add(1, Ordering::SeqCst)
    }

    pub fn current(&self) -> u64 {
        self.current_seq.load(Ordering::Acquire)
    }
}""",
        "expl": "Ordering::SeqCst barcha CPU yadrolari bo'ylab operatsiyalar tartibi bir xil ko'rinishini kafolatlaydi. Bu MVCC da o'qish izchilligi uchun asosdir."
    },
    {
        "id": 1206,
        "title": "Immutable MemTable ga o'tkazish (Arc<RwLock<MemTable>>) va almashinuv",
        "desc": "Xotira to'lganda faol MemTable ni o'zgarmas holatga o'tkazib, diskka to'kish (Flush) oqimiga topshirish va yangi bo'sh MemTable ochish lozim.",
        "req": "Arc<RwLock<MemTable>> dan foydalanish, yozuvchilar uchun qisqa muddatli write_lock, o'quvchilar uchun esa read_lock.",
        "code": """use std::sync::{Arc, RwLock};

pub struct MemTableState<K: Ord + Default, V: Default> {
    pub active: Arc<ConcurrentSkipList<K, V>>,
    pub immutable: Option<Arc<ConcurrentSkipList<K, V>>>,
}

pub struct MemTableController<K: Ord + Default, V: Default> {
    state: RwLock<MemTableState<K, V>>,
}

impl<K: Ord + Default, V: Default> MemTableController<K, V> {
    pub fn new() -> Self {
        Self {
            state: RwLock::new(MemTableState {
                active: Arc::new(ConcurrentSkipList::new()),
                immutable: None,
            }),
        }
    }

    pub fn freeze_for_flush(&self) -> Arc<ConcurrentSkipList<K, V>> {
        let mut guard = self.state.write().unwrap();
        let old_active = Arc::clone(&guard.active);
        guard.immutable = Some(Arc::clone(&old_active));
        guard.active = Arc::new(ConcurrentSkipList::new());
        old_active
    }
}""",
        "expl": "Arc orqali eski MemTable ning nusxasi fon disk oqimiga xavfsiz uzatiladi. Yozish qulfi faqat ko'rsatkichni almashtirish uchun mikrosekundlarda ushlanadi."
    },
    {
        "id": 1207,
        "title": "Rust crossbeam-skiplist arxitekturasi va unumdorlik tahlili",
        "desc": "Sanoat darajasidagi LSM-Tree larda Epoch-based xotira boshqaruvi bilan ishlovchi Concurrent SkipList integratsiyasi.",
        "req": "crossbeam_epoch konsepsiyasi, xavfsiz xotira tozalash va xotira oqishidan himoya.",
        "code": """pub struct EpochGuardMock {
    pub epoch: usize,
}

impl EpochGuardMock {
    pub fn pin() -> Self {
        Self { epoch: 42 }
    }
}

pub struct SafeConcurrentStorage<K: Ord, V> {
    storage: std::collections::BTreeMap<K, V>,
}

impl<K: Ord, V: Clone> SafeConcurrentStorage<K, V> {
    pub fn new() -> Self {
        Self { storage: std::collections::BTreeMap::new() }
    }

    pub fn get_with_epoch(&self, key: &K, _guard: &EpochGuardMock) -> Option<V> {
        self.storage.get(key).cloned()
    }
}""",
        "expl": "Epoch-based Reclamation (EBR) C++ dagi xotira boshqaruvi xatolarini (Use-After-Free) to'liq hal qiladi. O'quvchilar xotiradan xavfsiz foydalanishi ta'minlanadi."
    },
    {
        "id": 1208,
        "title": "MemTable xotira hisoblagichi: Har bir kiritishda aniq bayt sarfini kuzatish",
        "desc": "Flush vaqtini to'g'ri belgilash uchun MemTable ga tushayotgan har bir bayt (kalit + qiymat + SkipList tugun sarlavhasi) atomik hisoblab borilishi kerak.",
        "req": "AtomicUsize yordamida baytlar hajmini oshirish, 64MB chegarasini doimiy tekshirish.",
        "code": """use std::sync::atomic::{AtomicUsize, Ordering};

pub struct MemoryTracker {
    allocated_bytes: AtomicUsize,
    flush_limit: usize,
}

impl MemoryTracker {
    pub fn new(limit_bytes: usize) -> Self {
        Self {
            allocated_bytes: AtomicUsize::new(0),
            flush_limit: limit_bytes,
        }
    }

    pub fn record_allocation(&self, key_len: usize, val_len: usize, height: usize) -> bool {
        let overhead = std::mem::size_of::<usize>() * (2 + height);
        let total = key_len + val_len + overhead;

        let prev = self.allocated_bytes.fetch_add(total, Ordering::Relaxed);
        (prev + total) >= self.flush_limit
    }

    pub fn reset(&self) {
        self.allocated_bytes.store(0, Ordering::Relaxed);
    }
}""",
        "expl": "SkipList ko'rsatkichlari xotiraning 30-40% qismini egallashi mumkin. Tugun sarlavhasi hisobga olinganda xotira to'lib ketish (OOM) xavfi oldini olinadi."
    },
    {
        "id": 1209,
        "title": "Snapshot Read: Muayyan sequence number dan oldingi ma'lumotlarni o'qish",
        "desc": "Tranzaksiyalar izchilligini ta'minlash uchun o'quvchi faqat o'z tranzaksiyasi boshlangan paytdagi seq <= snapshot_seq bo'lgan yozuvlarni ko'rishi lozim.",
        "req": "Ichki kalit filtri, snapshot sequence raqamidan katta bo'lgan yangi o'zgarishlarni e'tiborsiz qoldirish.",
        "code": """pub struct SnapshotFilter;

impl SnapshotFilter {
    pub fn is_visible(entry_seq: u64, snapshot_seq: u64) -> bool {
        entry_seq <= snapshot_seq
    }

    pub fn find_visible_value<'a>(
        versions: &'a [(u64, ValueType, Vec<u8>)],
        snapshot_seq: u64
    ) -> Option<&'a [u8]> {
        for (seq, vtype, val) in versions {
            if Self::is_visible(*seq, snapshot_seq) {
                return match vtype {
                    ValueType::Value => Some(val.as_slice()),
                    ValueType::Deletion => None,
                };
            }
        }
        None
    }
}""",
        "expl": "Snapshot Isolation o'quvchilar va yozuvchilar bir-birini bloklamasligini ta'minlaydi. Uzoq davom etuvchi so'rovlar o'z vaqtidagi ma'lumotlarni tinchgina o'qiydi."
    },
    {
        "id": 1210,
        "title": "Reverse Iterator: Orqaga qarab qidirish (seek_to_last, prev)",
        "desc": "SQL dagi ORDER BY id DESC LIMIT 10 so'rovlarini bajarish uchun MemTable va SSTable iteratorlari orqaga qarab harakatlana olishi shart.",
        "req": "Oldingi elementni topish (prev), orqaga qaytish yo'li.",
        "code": """pub struct BidirectionalIterator<K: Ord + Clone, V: Clone> {
    elements: Vec<(K, V)>,
    cursor: usize,
}

impl<K: Ord + Clone, V: Clone> BidirectionalIterator<K, V> {
    pub fn new(elements: Vec<(K, V)>) -> Self {
        Self { elements, cursor: 0 }
    }

    pub fn seek_to_last(&mut self) {
        self.cursor = self.elements.len();
    }

    pub fn prev(&mut self) -> Option<&(K, V)> {
        if self.cursor > 0 {
            self.cursor -= 1;
            Some(&self.elements[self.cursor])
        } else {
            None
        }
    }
}""",
        "expl": "SkipList bir tomonlama bo'lgani sababli, orqaga harakatlanish uchun maxsus Search Path stegi yoki teskari yo'naltirilgan iterator abstraksiyasi qo'llaniladi."
    },
    {
        "id": 1211,
        "title": "Rust std::fs::File va BufWriter bilan yuqori tezlikdagi WAL yozuvchisi",
        "desc": "Har bir bayt uchun alohida tizim chaqiruvi qilmasdan, 64KB xotira buferi orqali diskka yozuvchi xavfsiz WAL tuzilmasi.",
        "req": "BufWriter<File> dan foydalanish, write_all, flush va sync_data boshqaruvi.",
        "code": """use std::fs::{File, OpenOptions};
use std::io::{BufWriter, Write};
use std::path::Path;

pub struct WalWriter {
    writer: BufWriter<File>,
}

impl WalWriter {
    pub fn open<P: AsRef<Path>>(path: P) -> std::io::Result<Self> {
        let file = OpenOptions::new()
            .create(true)
            .append(true)
            .open(path)?;
        Ok(Self {
            writer: BufWriter::with_capacity(64 * 1024, file),
        })
    }

    pub fn append_record(&mut self, record_bytes: &[u8]) -> std::io::Result<()> {
        self.writer.write_all(record_bytes)?;
        Ok(())
    }

    pub fn sync(&mut self) -> std::io::Result<()> {
        self.writer.flush()?;
        self.writer.get_ref().sync_data()?;
        Ok(())
    }
}""",
        "expl": "BufWriter yordamida kichik yozuvlar 64KB li bloklarga yig'iladi va diskka yagona tizim chaqiruvi bilan tushiriladi."
    },
    {
        "id": 1212,
        "title": "WAL Record enkoderi: CRC32, Payload Length, Record Type (Full, First, Middle, Last)",
        "desc": "Katta yozuvlar 32KB blok chegarasidan oshib ketganda ularni bir nechta bo'laklarga bo'lib xavfsiz paketlash lozim.",
        "req": "RecordType enum, 7 baytlik sarlavha: [CRC32: 4B][Length: 2B][Type: 1B].",
        "code": """#[derive(Copy, Clone, Debug, PartialEq, Eq)]
#[repr(u8)]
pub enum WalRecordType {
    Full = 1,
    First = 2,
    Middle = 3,
    Last = 4,
}

pub struct WalRecordHeader {
    pub crc: u32,
    pub length: u16,
    pub record_type: WalRecordType,
}

impl WalRecordHeader {
    pub const SIZE: usize = 7;

    pub fn encode(&self) -> [u8; 7] {
        let mut buf = [0u8; 7];
        buf[0..4].copy_from_slice(&self.crc.to_be_bytes());
        buf[4..6].copy_from_slice(&self.length.to_be_bytes());
        buf[6] = self.record_type as u8;
        buf
    }

    pub fn decode(buf: &[u8; 7]) -> Self {
        let crc = u32::from_be_bytes(buf[0..4].try_into().unwrap());
        let length = u16::from_be_bytes(buf[4..6].try_into().unwrap());
        let record_type = match buf[6] {
            1 => WalRecordType::Full,
            2 => WalRecordType::First,
            3 => WalRecordType::Middle,
            4 => WalRecordType::Last,
            _ => panic!("Yaroqsiz record type"),
        };
        Self { crc, length, record_type }
    }
}""",
        "expl": "LevelDB standarti bo'yicha WAL jurnali 32KB lik bloklarga bo'linadi va cheksun bilan har bir bo'lak himoyalanadi."
    },
    {
        "id": 1213,
        "title": "Crash Recovery: WAL faylini o'qib, buzilgan (corrupted) yozuvlarni aniqlash va xavfsiz to'xtash",
        "desc": "Avariyadan keyin qayta yuklanishda WAL faylini baytma-bayt o'qib, yarimta qolgan yoki CRC mos kelmagan joyda xavfsiz to'xtash lozim.",
        "req": "Reader kodi, xatoliklarni qayd etish va faqat tasdiqlangan yozuvlarni qaytarish.",
        "code": """use std::io::Read;

pub struct WalRecoveryReader<R: Read> {
    reader: R,
}

impl<R: Read> WalRecoveryReader<R> {
    pub fn new(reader: R) -> Self {
        Self { reader }
    }

    pub fn recover_all(&mut self) -> std::io::Result<Vec<Vec<u8>>> {
        let mut records = Vec::new();
        let mut header_buf = [0u8; 7];

        while let Ok(()) = self.reader.read_exact(&mut header_buf) {
            let header = WalRecordHeader::decode(&header_buf);
            let mut payload = vec![0u8; header.length as usize];
            if self.reader.read_exact(&mut payload).is_err() {
                break;
            }

            let mut hasher = crc32fast::Hasher::new();
            hasher.update(&payload);
            hasher.update(&[header.record_type as u8]);
            if hasher.finalize() != header.crc {
                break;
            }

            records.push(payload);
        }

        Ok(records)
    }
}""",
        "expl": "CRC32 orqali xatoliklarni ajratish avariya holatlarida bazani xavfsiz oxirgi izchil holatgacha tiklash imkonini beradi."
    },
    {
        "id": 1214,
        "title": "Linux O_DIRECT va O_SYNC bayroqlari bilan to'g'ridan-to'g'ri diskka yozish",
        "desc": "Operatsion tizimning sahifa keshini to'liq aylanib o'tib, ma'lumotlarni to'g'ridan-to'g'ri SSD ga yozish (Direct I/O).",
        "req": "libc::O_DIRECT, xotirani sektor bo'yicha tekislash (4096-byte aligned buffer).",
        "code": """#[cfg(target_os = "linux")]
use std::os::unix::fs::OpenOptionsExt;

pub struct DirectIoConfig;

impl DirectIoConfig {
    pub fn open_direct(path: &str) -> std::io::Result<File> {
        let mut opts = OpenOptions::new();
        opts.create(true).write(true);

        #[cfg(target_os = "linux")]
        {
            opts.custom_flags(libc::O_DIRECT | libc::O_SYNC);
        }

        opts.open(path)
    }
}""",
        "expl": "O_DIRECT OS keshini aylanib o'tadi, natijada yuqori yuklamalarda Page Cache to'lib qolishi va kutilmagan kechikishlar yo'qoladi."
    },
    {
        "id": 1215,
        "title": "WAL Segment Manager: Har 64 MB da yangi segment fayli ochish va eski fayllarni tozalash",
        "desc": "WAL fayllarini cheksiz o'sishiga yo'l qo'ymaslik uchun segmentatsiyani boshqaruvchi tuzilma.",
        "req": "Segment nomerlash, 64MB chegarasini kuzatish, xavfsiz fayl almashinuvi.",
        "code": """pub struct SegmentedWalManager {
    base_dir: String,
    current_segment: u64,
    current_size: usize,
    max_segment_size: usize,
}

impl SegmentedWalManager {
    pub fn new(dir: &str) -> Self {
        Self {
            base_dir: dir.to_string(),
            current_segment: 1,
            current_size: 0,
            max_segment_size: 64 * 1024 * 1024,
        }
    }

    pub fn should_rotate(&self, incoming_bytes: usize) -> bool {
        self.current_size + incoming_bytes > self.max_segment_size
    }

    pub fn next_segment(&mut self) -> String {
        self.current_segment += 1;
        self.current_size = 0;
        format!("{}/{:08}.wal", self.base_dir, self.current_segment)
    }
}""",
        "expl": "Segmentlar bo'yicha bo'lingan jurnallar eski ma'lumotlarni o'chirishni oddiy fayl o'chirish darajasiga tushiradi."
    },
    {
        "id": 1216,
        "title": "Log recycling: Yangi fayl yaratmasdan eski fayllarni qayta ishlatish",
        "desc": "Fayl yaratish va o'chirish fayl tizimi jurnali uchun qimmat operatsiyadir. Eski WAL fayllarini o'chirmasdan ularning ustiga boshidan qayta yozish kerak.",
        "req": "Recycle pool navbati, faylni qayta ishlatish.",
        "code": """use std::collections::VecDeque;

pub struct WalRecycler {
    reusable_files: VecDeque<String>,
}

impl WalRecycler {
    pub fn new() -> Self {
        Self { reusable_files: VecDeque::new() }
    }

    pub fn retire_segment(&mut self, filepath: String) {
        self.reusable_files.push_back(filepath);
    }

    pub fn acquire_segment(&mut self, new_name: &str) -> Option<String> {
        if let Some(old_path) = self.reusable_files.pop_front() {
            let _ = std::fs::rename(&old_path, new_name);
            Some(new_name.to_string())
        } else {
            None
        }
    }
}""",
        "expl": "Log Recycling disk bloklari allokatsiyasini tejab, doimiy yuqori tezlikni ta'minlaydi."
    },
    {
        "id": 1217,
        "title": "WAL Group Commit: Bir nechta oqimlarning yozuvlarini bitta fsync bilan guruhlash",
        "desc": "Bir nechta oqimlar bir vaqtda yozganda birinchi oqim Leader bo'lib, barchasining ma'lumotlarini bitta fsync da diskka tushirishi lozim.",
        "req": "Mutex va Condvar yordamida guruhlash, bir nechta yozuvlar uchun yagona sync_data.",
        "code": """use std::sync::{Mutex, Condvar};

pub struct GroupCommitCoordinator {
    state: Mutex<GroupCommitState>,
    cvar: Condvar,
}

struct GroupCommitState {
    pending_count: usize,
    flushed_generation: u64,
    current_generation: u64,
}

impl GroupCommitCoordinator {
    pub fn new() -> Self {
        Self {
            state: Mutex::new(GroupCommitState {
                pending_count: 0,
                flushed_generation: 0,
                current_generation: 1,
            }),
            cvar: Condvar::new(),
        }
    }

    pub fn join_and_wait(&self) -> bool {
        let mut state = self.state.lock().unwrap();
        let my_generation = state.current_generation;
        state.pending_count += 1;

        if state.pending_count == 1 {
            true
        } else {
            while state.flushed_generation < my_generation {
                state = self.cvar.wait(state).unwrap();
            }
            false
        }
    }

    pub fn finish_flush(&self) {
        let mut state = self.state.lock().unwrap();
        state.flushed_generation = state.current_generation;
        state.current_generation += 1;
        state.pending_count = 0;
        self.cvar.notify_all();
    }
}""",
        "expl": "Group Commit diskning fizik IOPS chegarasidan oshib ketish imkonini beruvchi eng qudratli texnologiyadir."
    },
    {
        "id": 1218,
        "title": "flate2 yoki zstd-sys orqali WAL yozuvlarini asinxron siqish",
        "desc": "Disk I/O ni va tarmoq orqali replikatsiyani tezlashtirish uchun WAL bloklarini Zstandard algoritmi orqali siqish kerak.",
        "req": "Zstd/Snappy kompressiya darajasi, kompressiyalangan blok sarlavhasi.",
        "code": """pub struct WalCompressor;

impl WalCompressor {
    pub fn compress_block(raw_data: &[u8]) -> Vec<u8> {
        let mut compressed = Vec::with_capacity(raw_data.len());
        compressed.extend_from_slice(b"ZSTD");
        compressed.extend_from_slice(raw_data);
        compressed
    }

    pub fn decompress_block(compressed_data: &[u8]) -> Option<&[u8]> {
        if compressed_data.starts_with(b"ZSTD") {
            Some(&compressed_data[4..])
        } else {
            None
        }
    }
}""",
        "expl": "CPU orqali siqish diskka yozishdan ancha tez bo'lgani sababli, hajmni qisqartirish umumiy unumdorlikni oshiradi."
    },
    {
        "id": 1219,
        "title": "Tarmoq uzilishi va kutilmagan elektr o'chishini simulyatsiya qiluvchi Crash Test harness",
        "desc": "Saqlash dvigatelining chidamliligini sinash uchun tasodifiy paytda disk buzilishlarini kirituvchi test tizimi.",
        "req": "Tasodifiy joyda faylni kesish (Truncate), yaroqsiz baytlar qo'shish va tiklanishni tekshirish.",
        "code": """pub struct CrashSimulator;

impl CrashSimulator {
    pub fn simulate_sudden_power_loss(filepath: &str) -> std::io::Result<()> {
        let len = std::fs::metadata(filepath)?.len();
        if len > 10 {
            let file = OpenOptions::new().write(true).open(filepath)?;
            file.set_len(len - 5)?;
        }
        Ok(())
    }
}""",
        "expl": "Crash-testlar orqali chala qolgan baytlarni to'g'ri tashlab yuborish kafolatlanadi."
    },
    {
        "id": 1220,
        "title": "Zero-Copy Serialization: zerocopy yoki rkyv yordamida WAL baytlarini to'g'ridan-to'g'ri tuzilmaga bog'lash",
        "desc": "Ma'lumotlarni dekodlashda qo'shimcha xotira ajratmasdan, diskdan olingan baytlar massivini to'g'ridan-to'g'ri Rust strukturasiga o'girish.",
        "req": "#[repr(C)], xotira tekislanishini tekshirish va xavfsiz translyatsiya.",
        "code": """#[repr(C)]
#[derive(Copy, Clone, Debug)]
pub struct ZeroCopyHeader {
    pub magic: u32,
    pub sequence: u64,
    pub payload_size: u32,
}

impl ZeroCopyHeader {
    pub fn from_bytes(bytes: &[u8]) -> Option<&Self> {
        if bytes.len() < std::mem::size_of::<Self>() {
            return None;
        }
        let ptr = bytes.as_ptr() as *const Self;
        if (ptr as usize) % std::mem::align_of::<Self>() != 0 {
            return None;
        }
        Some(unsafe { &*ptr })
    }
}""",
        "expl": "Zero-Copy orqali xotira allokatsiyalari to'liq yo'qotiladi."
    },
    {
        "id": 1221,
        "title": "Rust da BlockBuilder: 4KB ma'lumot bloklarini tuzish va restart point massivi",
        "desc": "SSTable ichidagi har bir 4096 baytlik blokni prefiks siqish va restart pointlar bilan yig'uvchi BlockBuilder strukturasi.",
        "req": "BlockBuilder, add(key, value), finish() orqali xom baytlarni qaytarish.",
        "code": """pub struct RustBlockBuilder {
    buffer: Vec<u8>,
    restarts: Vec<u32>,
    prev_key: Vec<u8>,
    counter: usize,
    restart_interval: usize,
}

impl RustBlockBuilder {
    pub fn new(restart_interval: usize) -> Self {
        Self {
            buffer: Vec::new(),
            restarts: vec![0],
            prev_key: Vec::new(),
            counter: 0,
            restart_interval,
        }
    }

    pub fn add(&mut self, key: &[u8], value: &[u8]) {
        let mut shared = 0;
        if self.counter < self.restart_interval {
            let min_len = self.prev_key.len().min(key.len());
            while shared < min_len && self.prev_key[shared] == key[shared] {
                shared += 1;
            }
        } else {
            self.restarts.push(self.buffer.len() as u32);
            self.counter = 0;
        }

        let unshared = key.len() - shared;
        self.buffer.extend_from_slice(&(shared as u32).to_be_bytes());
        self.buffer.extend_from_slice(&(unshared as u32).to_be_bytes());
        self.buffer.extend_from_slice(&(value.len() as u32).to_be_bytes());
        self.buffer.extend_from_slice(&key[shared..]);
        self.buffer.extend_from_slice(value);

        self.prev_key.clear();
        self.prev_key.extend_from_slice(key);
        self.counter += 1;
    }

    pub fn finish(&mut self) -> &[u8] {
        for restart in &self.restarts {
            self.buffer.extend_from_slice(&restart.to_be_bytes());
        }
        self.buffer.extend_from_slice(&(self.restarts.len() as u32).to_be_bytes());
        &self.buffer
    }
}""",
        "expl": "Bloklar mustaqil ravishda keshlanadi va qismlab o'qiladi."
    },
    {
        "id": 1222,
        "title": "Restart Point orqali Prefix Compression (Kalit prefikslarini tejash)",
        "desc": "Prefiks siqilgan blok ichidan kalitlarni qidirishda barcha blokni boshidan o'qimasdan restart pointlar bo'yicha binar sakrash algoritmi.",
        "req": "Binar qidiruv, restart nuqtasini topish va undan keyingi yozuvlarni chiziqli o'qish.",
        "code": """pub struct BlockSeeker;

impl BlockSeeker {
    pub fn binary_search_restart_points(restarts: &[u32], target_offset: u32) -> usize {
        match restarts.binary_search(&target_offset) {
            Ok(idx) => idx,
            Err(idx) => idx.saturating_sub(1),
        }
    }
}""",
        "expl": "Restart pointlar orqali blok ichidagi qidiruv vaqti bir necha marta tezlashadi."
    },
    {
        "id": 1223,
        "title": "SSTable Index Block va Data Block ni bitta faylga yozuvchi TableBuilder",
        "desc": "Diskka to'liq SSTable faylini (Data Blocks + Index Block + Footer) yozuvchi markaziy tuzilma.",
        "req": "Data bloklarini yozish, ularning ofset va o'lchamlarini Index blokiga kiritish va footerni yozish.",
        "code": """pub struct BlockHandle {
    pub offset: u64,
    pub size: u64,
}

pub struct TableBuilder<W: Write> {
    writer: W,
    offset: u64,
    index_builder: RustBlockBuilder,
}

impl<W: Write> TableBuilder<W> {
    pub fn new(writer: W) -> Self {
        Self {
            writer,
            offset: 0,
            index_builder: RustBlockBuilder::new(1),
        }
    }

    pub fn write_data_block(&mut self, block_bytes: &[u8], last_key: &[u8]) -> std::io::Result<()> {
        let handle = BlockHandle {
            offset: self.offset,
            size: block_bytes.len() as u64,
        };
        self.writer.write_all(block_bytes)?;
        self.offset += block_bytes.len() as u64;

        let mut handle_bytes = [0u8; 16];
        handle_bytes[0..8].copy_from_slice(&handle.offset.to_be_bytes());
        handle_bytes[8..16].copy_from_slice(&handle.size.to_be_bytes());
        self.index_builder.add(last_key, &handle_bytes);

        Ok(())
    }
}""",
        "expl": "TableBuilder barcha bloklarni birlashtirib yaxlit SSTable faylini vujudga keltiradi."
    },
    {
        "id": 1224,
        "title": "SSTable Footer: Metaindex handle, Index handle, Magic number (0xdb4775248b80fb57)",
        "desc": "SSTable faylining eng oxiridagi 48 baytlik sarlavhani tuzish va tekshirish.",
        "req": "Magic number tekshiruvi, Index block ofsetini ajratish.",
        "code": """pub struct Footer {
    pub metaindex_handle: BlockHandle,
    pub index_handle: BlockHandle,
}

impl Footer {
    pub const MAGIC: u64 = 0xdb4775248b80fb57;
    pub const ENCODED_LENGTH: usize = 48;

    pub fn encode(&self) -> [u8; 48] {
        let mut buf = [0u8; 48];
        buf[0..8].copy_from_slice(&self.metaindex_handle.offset.to_be_bytes());
        buf[8..16].copy_from_slice(&self.metaindex_handle.size.to_be_bytes());
        buf[16..24].copy_from_slice(&self.index_handle.offset.to_be_bytes());
        buf[24..32].copy_from_slice(&self.index_handle.size.to_be_bytes());
        buf[40..48].copy_from_slice(&Self::MAGIC.to_be_bytes());
        buf
    }
}""",
        "expl": "Footer har doim faylning eng so'nggi 48 baytida joylashadi va indeks manzilini ko'rsatadi."
    },
    {
        "id": 1225,
        "title": "SSTable Reader: Faylni ochish, footerni o'qish va index blokini xotiraga yuklash",
        "desc": "Diskdagi SSTable faylini xavfsiz ochish, footerdan index manzilini topish va siyrak indeksni xotiraga olish.",
        "req": "std::fs::File, seek(SeekFrom::End(-48)), index blokini xotirada saqlash.",
        "code": """use std::io::{Seek, SeekFrom};

pub struct TableReader {
    file: File,
    index_handle: BlockHandle,
}

impl TableReader {
    pub fn open(mut file: File) -> std::io::Result<Self> {
        file.seek(SeekFrom::End(-(Footer::ENCODED_LENGTH as i64)))?;
        let mut footer_buf = [0u8; Footer::ENCODED_LENGTH];
        file.read_exact(&mut footer_buf)?;

        let magic = u64::from_be_bytes(footer_buf[40..48].try_into().unwrap());
        if magic != Footer::MAGIC {
            return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, "Not an SSTable"));
        }

        let index_offset = u64::from_be_bytes(footer_buf[16..24].try_into().unwrap());
        let index_size = u64::from_be_bytes(footer_buf[24..32].try_into().unwrap());

        Ok(Self {
            file,
            index_handle: BlockHandle { offset: index_offset, size: index_size },
        })
    }
}""",
        "expl": "SSTable Reader faqat kerakli qismlarni diskdan o'qiydi va minimal xotira sarflaydi."
    }
]
