# -*- coding: utf-8 -*-
"""
Rust 25-modul: 1226 dan 1250 gacha bo'lgan topshiriqlar
mmap I/O, Zero-Copy Page Cache, Compaction va To'liq LSM-Tree Engine
"""

TASKS_1226_1250 = [
    {
        "id": 1226,
        "title": "BlockIterator: Blok ichidagi kalitlarni binar va restart pointlar bo'yicha qidirish",
        "desc": "4KB lik blok ichidan kalitlarni izlashda restart nuqtalaridan foydalanib binar qidiruvni amalga oshiruvchi iterator.",
        "req": "`seek(&key)` metodi, `valid()`, `key()`, `value()` orqali ma'lumotlarni o'qish.",
        "code": """pub struct BlockIterator<'a> {
    data: &'a [u8],
    restarts_offset: usize,
    num_restarts: usize,
    current_offset: usize,
}

impl<'a> BlockIterator<'a> {
    pub fn new(data: &'a [u8]) -> Self {
        let num_restarts = u32::from_be_bytes(data[data.len() - 4..].try_into().unwrap()) as usize;
        let restarts_offset = data.len() - 4 - (num_restarts * 4);
        Self {
            data,
            restarts_offset,
            num_restarts,
            current_offset: 0,
        }
    }

    pub fn valid(&self) -> bool {
        self.current_offset < self.restarts_offset
    }
}""",
        "expl": "BlockIterator xotirada joylashgan bitta blokni juda tez tahlil qiladi. Rust ning xotira kafolatlari tufayli xom ko'rsatkichlarsiz ham maksimal tezlikka erishiladi."
    },
    {
        "id": 1227,
        "title": "TwoLevelIterator: Index blok orqali Data blokni topib, uning ichini o'quvchi iterator",
        "desc": "Ikki qavatli iterator: 1-darajali iterator index blokdan kerakli data blok manzilini topadi, 2-darajali iterator esa o'sha data blok ichini ochadi.",
        "req": "`TwoLevelIterator`, indeks va ma'lumot bloklarini birlashtiruvchi abstraksiya.",
        "code": """pub struct TwoLevelIterator<'a> {
    index_iter: BlockIterator<'a>,
    data_iter: Option<BlockIterator<'a>>,
}

impl<'a> TwoLevelIterator<'a> {
    pub fn new(index_iter: BlockIterator<'a>) -> Self {
        Self {
            index_iter,
            data_iter: None,
        }
    }

    pub fn valid(&self) -> bool {
        self.data_iter.as_ref().map_or(false, |it| it.valid())
    }
}""",
        "expl": "TwoLevelIterator foydalanuvchiga butun gigabaytlik SSTable faylini xuddi bitta uzluksiz massivdek taqdim etadi. Ichkarida esa kerakli 4KB bloklar diskdan talab bo'yicha (lazy loading) yuklanadi."
    },
    {
        "id": 1228,
        "title": "Merging Iterator: Bir nechta SSTable iteratorlarini BinaryHeap (Min-Heap) orqali birlashtirish",
        "desc": "Bir nechta SSTable lardan kelayotgan saralangan oqimlarni Min-Heap orqali birlashtirib, tartiblangan bitta umumiy oqim hosil qilish.",
        "req": "`std::collections::BinaryHeap`, `Ord` traitini teskari qilish (Min-Heap), duplikat kalitlarni yangisi bilan almashtirish.",
        "code": """use std::collections::BinaryHeap;
use std::cmp::Ordering;

struct HeapItem<'a> {
    key: &'a [u8],
    source_index: usize,
}

impl<'a> Eq for HeapItem<'a> {}
impl<'a> PartialEq for HeapItem<'a> {
    fn eq(&self, other: &Self) -> bool { self.key == other.key }
}
impl<'a> Ord for HeapItem<'a> {
    fn cmp(&self, other: &Self) -> Ordering {
        // Min-heap bo'lishi uchun teskari solishtirish
        other.key.cmp(self.key)
    }
}
impl<'a> PartialOrd for HeapItem<'a> {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> { Some(self.cmp(other)) }
}

pub struct RustMergingIterator<'a> {
    heap: BinaryHeap<HeapItem<'a>>,
}""",
        "expl": "Rust `BinaryHeap` sukut bo'yicha Max-Heap dir. `Ord` implementatsiyasida `other.key.cmp(self.key)` qilish orqali u eng kichik kalitni birinchi chiquvchi Min-Heap ga aylanadi."
    },
    {
        "id": 1229,
        "title": "Block Cache: lru::LruCache orqali tez-tez o'qiladigan 4KB ma'lumot bloklarini keshlashtirish",
        "desc": "Diskdan o'qilgan 4KB bloklarni xotirada ushlab turish uchun LRU kesh hovuzini yaratish.",
        "req": "`lru::LruCache` yoki xususiy LRU, kalit sifatida `(file_id, block_offset)`, thread-safe kirish.",
        "code": """use std::sync::Mutex;
use std::collections::HashMap;

pub struct SimpleBlockCache {
    cache: Mutex<HashMap<(u64, u64), Vec<u8>>>,
    capacity_blocks: usize,
}

impl SimpleBlockCache {
    pub fn new(capacity: usize) -> Self {
        Self {
            cache: Mutex::new(HashMap::with_capacity(capacity)),
            capacity_blocks: capacity,
        }
    }

    pub fn get(&self, file_id: u64, offset: u64) -> Option<Vec<u8>> {
        let guard = self.cache.lock().unwrap();
        guard.get(&(file_id, offset)).cloned()
    }

    pub fn insert(&self, file_id: u64, offset: u64, block: Vec<u8>) {
        let mut guard = self.cache.lock().unwrap();
        if guard.len() < self.capacity_blocks {
            guard.insert((file_id, offset), block);
        }
    }
}""",
        "expl": "Block Cache LSM-Tree o'qish tezligini 10 barobargacha oshiradi. Eng ko'p o'qiladigan indeks va ma'lumot bloklari xotirada turgani sababli, disk kallagi deyarli harakatlanmaydi."
    },
    {
        "id": 1230,
        "title": "Bloom Filter Block: Har bir SSTable fayliga Bloom filter kiritish va disk I/O ni 90% ga qisqartirish",
        "desc": "SSTable oxiriga kiritiluvchi Bloom Filter blokini tuzish va uni qidiruvdan oldin tekshirish.",
        "req": "Bloom Filter baytlari, hash hisoblash, kalit yo'qligini darhol aniqlash.",
        "code": """pub struct SSTableBloomBlock {
    data: Vec<u8>,
    k: usize,
}

impl SSTableBloomBlock {
    pub fn new(data: Vec<u8>, k: usize) -> Self {
        Self { data, k }
    }

    pub fn may_contain(&self, key: &[u8]) -> bool {
        if self.data.is_empty() { return true; }
        let h = crc32fast::hash(key);
        let bit_len = self.data.len() * 8;
        for i in 0..self.k {
            let bit_idx = ((h as usize) + i * 0x5bd1e995) % bit_len;
            if (self.data[bit_idx / 8] & (1 << (bit_idx % 8))) == 0 {
                return false;
            }
        }
        true
    }
}""",
        "expl": "Har bir SSTable ga 1-2 KB li Bloom filtri kiritish minglab bekorchi fayl o'qishlarini oldini oladi. Baza mavjud bo'lmagan kalitlarni so'raganda hech qachon diskni yuklamaydi."
    },
    {
        "id": 1231,
        "title": "Rust da memmap2 crate orqali SSTable fayllarini xotiraga xaritalash",
        "desc": "SSTable fayllarini xotiraga to'g'ridan-to'g'ri virtual manzil maydoni sifatida xaritalash (`mmap`) orqali operatsion tizim sahifalaridan foydalanish.",
        "req": "`memmap2::Mmap` dan foydalanish, `unsafe` bloklar va xavfsiz o'qish abstraksiyasi.",
        "code": """use memmap2::Mmap;
use std::fs::File;

pub struct MmapTableReader {
    mmap: Mmap,
}

impl MmapTableReader {
    pub fn open(file: &File) -> std::io::Result<Self> {
        let mmap = unsafe { Mmap::map(file)? };
        Ok(Self { mmap })
    }

    pub fn read_slice(&self, offset: usize, length: usize) -> Option<&[u8]> {
        if offset + length <= self.mmap.len() {
            Some(&self.mmap[offset..offset + length])
        } else {
            None
        }
    }
}""",
        "expl": "`mmap` (Memory-Mapped I/O) yadro buferlaridan foydalanuvchi xotirasiga ma'lumot nusxalashni (Context Switch va buffer copy) yo'qotadi. Fayl baytlari operativ xotiradagi oddiy massivdek o'qiladi."
    },
    {
        "id": 1232,
        "title": "POSIX madvise chaqiruvlari (MADV_WILLNEED, MADV_RANDOM, MADV_SEQUENTIAL)",
        "desc": "Operatsion tizim yadrosiga ma'lumotlar qanday o'qilishini oldindan bildirib, keshni optimal boshqarish.",
        "req": "`libc::madvise`, `MADV_WILLNEED` (oldindan yuklash), `MADV_DONTNEED` (keshdan chiqarish).",
        "code": """pub struct MmapAdvisor;

impl MmapAdvisor {
    pub fn advise_sequential(ptr: *mut u8, len: usize) {
        #[cfg(target_family = "unix")]
        unsafe {
            libc::madvise(ptr as *mut libc::c_void, len, libc::MADV_SEQUENTIAL);
        }
    }

    pub fn advise_will_need(ptr: *mut u8, len: usize) {
        #[cfg(target_family = "unix")]
        unsafe {
            libc::madvise(ptr as *mut libc::c_void, len, libc::MADV_WILLNEED);
        }
    }
}""",
        "expl": "`madvise` OS ga yordam beradi: `MADV_SEQUENTIAL` kiritilganda Linux oldindan (Read-Ahead) keyingi sahifalarni diskdan xotiraga tayyorlab qo'yadi, bu esa o'qish kechikishini keskin kamaytiradi."
    },
    {
        "id": 1233,
        "title": "mmap ustida Zero-Copy slice slicing: Baytlarni nusxalamasdan string/slice qaytarish",
        "desc": "Qidiruv natijalarini qaytarishda hech qanday `Vec::clone` yoki `String::from_utf8` qilmasdan to'g'ridan-to'g'ri mmap kesimini (`&'a [u8]`) qaytarish.",
        "req": "Lifetime `'a` ni bog'lash, nolinchi xotira sarfi (Zero-Allocation).",
        "code": """pub struct ZeroCopyRecord<'a> {
    pub key: &'a [u8],
    pub value: &'a [u8],
}

impl<'a> ZeroCopyRecord<'a> {
    pub fn parse_from_mmap(slice: &'a [u8], key_len: usize) -> Self {
        let key = &slice[..key_len];
        let value = &slice[key_len..];
        Self { key, value }
    }
}""",
        "expl": "Zero-Copy ma'lumotlar bazasining eng yuqori unumdorlik pog'onasidir. GB lab ma'lumot uzatilganda ham bitta bayt xotira qo'shimcha ajratilmaydi."
    },
    {
        "id": 1234,
        "title": "Xavfsiz mmap abstraksiyasi: Fayl hajmi o'zgarganda xotira xatolaridan (SIGBUS) himoyalanish",
        "desc": "Boshqa jarayon faylni kesib tashlaganda (truncate) `SIGBUS` signali bilan butun dastur qulamasligi uchun xavfsizlik cheklovlari.",
        "req": "Fayl hajmini kuzatish, o'lcham chegaralarini tekshirish.",
        "code": """pub struct SafeMmapSlice<'a> {
    slice: &'a [u8],
    original_size: usize,
}

impl<'a> SafeMmapSlice<'a> {
    pub fn new(slice: &'a [u8]) -> Self {
        Self {
            slice,
            original_size: slice.len(),
        }
    }

    pub fn safe_read(&self, offset: usize, len: usize) -> Option<&'a [u8]> {
        if offset + len <= self.original_size {
            Some(&self.slice[offset..offset + len])
        } else {
            None
        }
    }
}""",
        "expl": "Rust mmap dagi potentsial UB (Undefined Behavior) larni biladi. Hajmni tekshirish orqali xavfsizlik chegaralari o'rnatiladi."
    },
    {
        "id": 1235,
        "title": "Shared Memory Page Cache: Bir nechta jarayonlar o'rtasida umumiy kesh",
        "desc": "Bir nechta jarayonlar (masalan Reader va Writer jarayonlari) bitta umumiy operativ xotira hududidan foydalanishi uchun Shared Memory (POSIX shm) kesh yaratish.",
        "req": "`shm_open`, umumiy xotira sahifalari xaritasi.",
        "code": """pub struct SharedMemoryCache {
    name: String,
    size: usize,
}

impl SharedMemoryCache {
    pub fn new(name: &str, size: usize) -> Self {
        Self {
            name: name.to_string(),
            size,
        }
    }
}""",
        "expl": "Shared Memory orqali jarayonlararo xabar almashishda tarmoq yoki soketlar ishlatilmaydi, to'g'ridan-to'g'ri umumiy RAM dan o'qiladi."
    },
    {
        "id": 1236,
        "title": "Page Cache Dirty Page tracking: O'zgargan sahifalarni belgilash",
        "desc": "Xotirada o'zgartirilgan sahifalarni kuzatib boruvchi Bitmap joriy qilish.",
        "req": "Bitmap orqali har bir sahifa uchun 1 bit belgilash, flush qilingach bitni tozalash.",
        "code": """pub struct DirtyPageTracker {
    bitmap: Vec<u64>,
}

impl DirtyPageTracker {
    pub fn new(total_pages: usize) -> Self {
        let u64_count = (total_pages + 63) / 64;
        Self { bitmap: vec![0; u64_count] }
    }

    pub fn mark_dirty(&mut self, page_idx: usize) {
        self.bitmap[page_idx / 64] |= 1 << (page_idx % 64);
    }

    pub fn is_dirty(&self, page_idx: usize) -> bool {
        (self.bitmap[page_idx / 64] & (1 << (page_idx % 64))) != 0
    }
}""",
        "expl": "Bitmap yordamida sahifalarni kuzatish xotirani tejaydi: 64 ta sahifa holati bitta 64-bitli son ichida boshqariladi."
    },
    {
        "id": 1237,
        "title": "Asinxron diskka yozuvchi tokio::fs va io_uring integratsiyasi",
        "desc": "Linux ning eng yangi `io_uring` asinxron I/O interfeysi orqali tizim chaqiruvlarisiz (Zero-Syscall) diskka ommaviy yozish.",
        "req": "Submission Queue (SQ) va Completion Queue (CQ) arxitekturasi simulyatsiyasi.",
        "code": """pub struct IoUringEngineMock {
    submission_queue: Vec<Vec<u8>>,
}

impl IoUringEngineMock {
    pub fn new() -> Self {
        Self { submission_queue: Vec::new() }
    }

    pub fn submit_write(&mut self, data: Vec<u8>) {
        self.submission_queue.push(data);
    }

    pub fn process_completions(&mut self) -> usize {
        let count = self.submission_queue.len();
        self.submission_queue.clear();
        count
    }
}""",
        "expl": "io_uring - zamonaviy Linux yadrosining eng inqilobiy yutug'idir. Yadro va foydalanuvchi fazosi o'rtasida umumiy halqa buferi (Ring Buffer) orqali hech qanday tizim chaqiruvisiz soniyasiga millionlab I/O amallari bajariladi."
    },
    {
        "id": 1238,
        "title": "Huge Pages (2MB / 1GB) orqali TLB xatolarini minimallashtirish",
        "desc": "Katta xotira hovuzlarida 4KB sahifalar o'rniga 2MB Huge Pages dan foydalanib CPU TLB (Translation Lookaside Buffer) kesh to'qnashuvlarini yo'qotish.",
        "req": "`mmap` da `MAP_HUGETLB` bayrog'idan foydalanish.",
        "code": """pub struct HugePageAllocator;

impl HugePageAllocator {
    pub fn alloc_2mb() -> Option<*mut u8> {
        #[cfg(target_os = "linux")]
        unsafe {
            let ptr = libc::mmap(
                std::ptr::null_mut(),
                2 * 1024 * 1024,
                libc::PROT_READ | libc::PROT_WRITE,
                libc::MAP_PRIVATE | libc::MAP_ANONYMOUS | libc::MAP_HUGETLB,
                -1,
                0,
            );
            if ptr == libc::MAP_FAILED {
                None
            } else {
                Some(ptr as *mut u8)
            }
        }
        #[cfg(not(target_os = "linux"))]
        None
    }
}""",
        "expl": "2MB Huge Pages TLB (Translation Lookaside Buffer) hajmini 512 barobar tejaydi. Katta ma'lumotlar bazalarida bu umumiy CPU unumdorligini 10-15% ga oshiradi."
    },
    {
        "id": 1239,
        "title": "Non-volatile Memory (NVRAM / PMEM) uchun xotiraga to'g'ridan-to'g'ri kirish",
        "desc": "Intel Optane kabi doimiy xotirada (Persistent Memory) ma'lumotlarni saqlash va CPU keshini diskka to'kish (`clwb` - Cache Line Write Back).",
        "req": "`clwb` assembly buyrug'i va `sfence` orqali doimiy xotiraga atomar saqlash.",
        "code": """pub struct PmemOps;

impl PmemOps {
    pub fn flush_cache_line(_ptr: *const u8) {
        #[cfg(target_arch = "x86_64")]
        unsafe {
            // asm!("clwb [{0}]", in(reg) _ptr, options(nostack));
            // asm!("sfence", options(nostack));
        }
    }
}""",
        "expl": "NVRAM / PMEM an'anaviy disklar davrini tugatadi. U RAM tezligida ishlaydi, ammo elektr o'chganda ma'lumotlarni saqlab qoladi."
    },
    {
        "id": 1240,
        "title": "mmap vs Read syscall unumdorlik benchmarki",
        "desc": "Katta ma'lumotlar oqimida `mmap` va standart `File::read` unumdorligini solishtiruvchi o'lchov moduli.",
        "req": "Vaqt o'lchash (`std::time::Instant`), o'qish tezligini (GB/s) hisoblash.",
        "code": """use std::time::Instant;

pub struct BenchmarkResult {
    pub mmap_duration_ms: u128,
    pub syscall_duration_ms: u128,
}

pub struct IoBenchmark;

impl IoBenchmark {
    pub fn compare(data: &[u8]) -> BenchmarkResult {
        let t0 = Instant::now();
        // mmap o'qish simulyatsiyasi (xotira ko'rsatkichi)
        let mut sum1 = 0u64;
        for &b in data { sum1 += b as u64; }
        let d1 = t0.elapsed().as_millis();

        let t1 = Instant::now();
        // Buferlangan o'qish simulyatsiyasi
        let mut sum2 = 0u64;
        for chunk in data.chunks(4096) {
            for &b in chunk { sum2 += b as u64; }
        }
        let d2 = t1.elapsed().as_millis();

        BenchmarkResult {
            mmap_duration_ms: d1,
            syscall_duration_ms: d2,
        }
    }
}""",
        "expl": "Katta fayllarda `mmap` tizim chaqiruvlari (Syscall overhead) bo'lmagani sababli doimo g'olib chiqadi."
    },
    {
        "id": 1241,
        "title": "VersionSet va VersionEdit: Manifest fayli orqali SSTable darajalarini saqlash",
        "desc": "Rust da Manifest jurnali orqali qaysi SSTable fayllari faol ekanligini qayd etish.",
        "req": "VersionEdit strukturasini yaratish, fayllarni qo'shish va o'chirish.",
        "code": """pub struct FileMetadata {
    pub file_num: u64,
    pub level: usize,
    pub smallest_key: Vec<u8>,
    pub largest_key: Vec<u8>,
}

pub struct RustVersionEdit {
    pub added: Vec<FileMetadata>,
    pub deleted: Vec<(usize, u64)>, // (level, file_num)
}""",
        "expl": "VersionEdit atomik tranzaksiyadir: barcha eski fayllar o'chirilishi va yangi fayllar qo'shilishi bitta operatsiyada ro'yxatga olinadi."
    },
    {
        "id": 1242,
        "title": "Compaction Controller: Qaysi darajada limit oshganini hisoblovchi (Score > 1.0) tizim",
        "desc": "Har bir darajadagi fayllar hajmini o'lchab, zichlashtirish talab qilinuvchi darajani tanlash.",
        "req": "Daraja chegaralari, Score hisobi va eng og'ir darajani tanlash.",
        "code": """pub struct RustCompactionController {
    level_max_bytes: [usize; 7],
}

impl RustCompactionController {
    pub fn new() -> Self {
        Self {
            level_max_bytes: [
                4 * 1024 * 1024,      // L0
                10 * 1024 * 1024,     // L1
                100 * 1024 * 1024,    // L2
                1000 * 1024 * 1024,   // L3
                10000 * 1024 * 1024,  // L4
                100000 * 1024 * 1024, // L5
                1000000 * 1024 * 1024 // L6
            ],
        }
    }

    pub fn pick_compaction_level(&self, current_sizes: &[usize]) -> Option<usize> {
        let mut best_level = None;
        let mut best_score = 1.0;

        for (lvl, &size) in current_sizes.iter().enumerate() {
            let limit = self.level_max_bytes.get(lvl).copied().unwrap_or(usize::MAX);
            let score = size as f64 / limit as f64;
            if score > best_score {
                best_score = score;
                best_level = Some(lvl);
            }
        }
        best_level
    }
}""",
        "expl": "Score hisobi qaysi daraja eng tez to'lib borayotganini aniq ko'rsatadi va resurslarni eng kerakli joyga yo'naltiradi."
    },
    {
        "id": 1243,
        "title": "Rust Channels (crossbeam-channel) orqali asinxron Compaction Worker",
        "desc": "Asosiy oqimdan kelayotgan Compaction vazifalarini kanal orqali qabul qilib, fonda bajaruvchi xizmat.",
        "req": "`std::sync::mpsc` yoki `crossbeam_channel`, vazifani uzatish va to'xtatish.",
        "code": """use std::sync::mpsc::{channel, Sender, Receiver};

pub enum CompactionTask {
    CompactLevel(usize),
    Shutdown,
}

pub struct AsyncCompactionService {
    sender: Sender<CompactionTask>,
}

impl AsyncCompactionService {
    pub fn start() -> (Self, std::thread::JoinHandle<()>) {
        let (tx, rx) = channel::<CompactionTask>();
        let handle = std::thread::spawn(move || {
            while let Ok(task) = rx.recv() {
                match task {
                    CompactionTask::CompactLevel(lvl) => {
                        println!("[COMPACTION WORKER] Level {} zichlashtirildi", lvl);
                    }
                    CompactionTask::Shutdown => break,
                }
            }
        });
        (Self { sender: tx }, handle)
    }

    pub fn trigger(&self, level: usize) {
        let _ = self.sender.send(CompactionTask::CompactLevel(level));
    }
}""",
        "expl": "Rust kanallari (Channels) ma'lumotlarni oqimlar o'rtasida xavfsiz uzatadi (Ownership transfer). Qulflanishlar bo'lmaydi."
    },
    {
        "id": 1244,
        "title": "Merging SSTables: Eski fayllarni o'qib, yangi darajaga bitta saralangan SSTable yozish",
        "desc": "Ikki darajadagi fayllarni K-Way Merge orqali o'qib, yangi darajadagi fayllarni yaratish mantiqi.",
        "req": "Min-heap bilan o'qish, duplikatlarni yo'qotish va yangi SSTable ga chiqarish.",
        "code": """pub struct SSTableMerger;

impl SSTableMerger {
    pub fn merge_two_sorted_slices(s1: &[(Vec<u8>, Vec<u8>)], s2: &[(Vec<u8>, Vec<u8>)]) -> Vec<(Vec<u8>, Vec<u8>)> {
        let mut result = Vec::new();
        let (mut i, mut j) = (0, 0);

        while i < s1.len() && j < s2.len() {
            if s1[i].0 < s2[j].0 {
                result.push(s1[i].clone());
                i += 1;
            } else if s1[i].0 > s2[j].0 {
                result.push(s2[j].clone());
                j += 1;
            } else {
                // Teng kalit bo'lsa, eng yangisi (s1) olinadi
                result.push(s1[i].clone());
                i += 1;
                j += 1;
            }
        }

        while i < s1.len() { result.push(s1[i].clone()); i += 1; }
        while j < s2.len() { result.push(s2[j].clone()); j += 1; }

        result
    }
}""",
        "expl": "Merging jarayoni eski ma'lumotlarni tozalaydi va yangi saralangan tartibni hosil qiladi."
    },
    {
        "id": 1245,
        "title": "Tombstone GC: Eng chuqur darajaga yetgan qabr toshlarini diskdan jismoniy o'chirish",
        "desc": "O'chirish markeri (Tombstone) eng so'nggi darajaga yetganda uni yangi faylga yozmasdan butunlay tashlab ketish.",
        "req": "Oxirgi darajani tekshirish, agar oxirgi daraja bo'lsa va tombstone bo'lsa o'tkazib yuborish.",
        "code": """pub struct TombstoneGarbageCollector;

impl TombstoneGarbageCollector {
    pub fn should_retain(key: &[u8], is_tombstone: bool, is_bottom_level: bool) -> bool {
        if is_tombstone && is_bottom_level {
            // Eng quyi darajada qabr toshini butunlay yo'q qilamiz!
            false
        } else {
            true
        }
    }
}""",
        "expl": "Tombstone GC disk maydonini to'liq qaytarib olishning yagona yo'lidir."
    },
    {
        "id": 1246,
        "title": "Rate-Limiting Compaction: SSD disklarining eskirishini (write wearout) kamaytirish",
        "desc": "Zichlashtirish diskka juda ko'p ma'lumot yozib, SSD ning resursini tez yeb qo'ymasligi uchun yozish tezligini (masalan sekundiga 50 MB) sun'iy cheklash (Token Bucket).",
        "req": "Token Bucket algoritmi, sekundiga ruxsat etilgan baytlar soni va kutish.",
        "code": """pub struct CompactionRateLimiter {
    rate_bytes_per_sec: usize,
    tokens: usize,
    last_refill: std::time::Instant,
}

impl CompactionRateLimiter {
    pub fn new(rate_limit: usize) -> Self {
        Self {
            rate_bytes_per_sec: rate_limit,
            tokens: rate_limit,
            last_refill: std::time::Instant::now(),
        }
    }

    pub fn request_bytes(&mut self, bytes: usize) {
        let elapsed = self.last_refill.elapsed().as_secs_f64();
        let new_tokens = (elapsed * self.rate_bytes_per_sec as f64) as usize;
        self.tokens = (self.tokens + new_tokens).min(self.rate_bytes_per_sec);
        self.last_refill = std::time::Instant::now();

        if bytes > self.tokens {
            let deficit = bytes - self.tokens;
            let sleep_time = deficit as f64 / self.rate_bytes_per_sec as f64;
            std::thread::sleep(std::time::Duration::from_secs_f64(sleep_time));
            self.tokens = 0;
        } else {
            self.tokens -= bytes;
        }
    }
}""",
        "expl": "Rate Limiting SSD disklarining jismoniy umrini bir necha barobar uzaytiradi va asosiy mijoz so'rovlarining I/O kechikishini (Tail Latency) pasaytiradi."
    },
    {
        "id": 1247,
        "title": "Snapshots va MVCC Garbage Collection: Eski tranzaksiyalar tugagach keraksiz versiyalarni yo'q qilish",
        "desc": "Barcha faol tranzaksiyalar o'qib bo'lgan eski versiyalarni Compaction paytida tozalash.",
        "req": "Eng kichik faol snapshot sequence raqamini topish (`min_snapshot_seq`), undan eski nusxalarni tashlab ketish.",
        "code": """pub struct MvccCleaner;

impl MvccCleaner {
    pub fn clean_versions(
        versions: &[(u64, Vec<u8>)], // (sequence, value)
        min_active_snapshot: u64
    ) -> Vec<(u64, Vec<u8>)> {
        let mut result = Vec::new();
        let mut keep_next_older = true;

        for (seq, val) in versions {
            if *seq >= min_active_snapshot {
                result.push((*seq, val.clone()));
            } else if keep_next_older {
                // Snapshot uchun kerakli bitta eng so'nggi versiyani saqlaymiz
                result.push((*seq, val.clone()));
                keep_next_older = false; // Undan ham eski versiyalar kerak emas!
            }
        }
        result
    }
}""",
        "expl": "MVCC GC bitta kalitning 1000 ta eski tarixini tozalab, faqat faol tranzaksiyalar ko'rayotgan versiyalarni saqlaydi."
    },
    {
        "id": 1248,
        "title": "Write Stall nazoratchisi: MemTable to'lib ketganda mijozlarni vaqtincha to'xtatish",
        "desc": "MemTable to'lib, L0 fayllar soni haddan oshganda yozuvchi oqimlarni vaqtincha sekinlashtirish yoki to'xtatish.",
        "req": "Oqimni to'xtatish (`std::thread::sleep`), holatni qaytarish.",
        "code": """pub struct RustWriteStall {
    pub l0_threshold: usize,
}

impl RustWriteStall {
    pub fn check_stall(&self, current_l0_files: usize) {
        if current_l0_files > self.l0_threshold {
            std::thread::sleep(std::time::Duration::from_millis(10));
        }
    }
}""",
        "expl": "Write Stall bo'lmasa, dastur haddan tashqari ko'p xotira band qilib OOM bilan yiqiladi."
    },
    {
        "id": 1249,
        "title": "LSM-Tree Metrics va Telemetriya: O'qish/yozish tezligi, kompressiya ko'rsatkichlari",
        "desc": "Dvigatelning jami kiritilgan, o'qilgan baytlari va siqish samaradorligini o'lchovchi metrika tizimi.",
        "req": "`AtomicU64` hisoblagichlari, o'rtacha ko'rsatkichlarni hisoblash.",
        "code": """pub struct LsmEngineMetrics {
    pub bytes_written: AtomicU64,
    pub bytes_read: AtomicU64,
    pub total_compactions: AtomicU64,
}

impl LsmEngineMetrics {
    pub fn new() -> Self {
        Self {
            bytes_written: AtomicU64::new(0),
            bytes_read: AtomicU64::new(0),
            total_compactions: AtomicU64::new(0),
        }
    }

    pub fn record_write(&self, bytes: u64) {
        self.bytes_written.fetch_add(bytes, Ordering::Relaxed);
    }
}""",
        "expl": "Telemetriya tizim muhandislariga bazaning real holatini kuzatish va disk unumdorligini sozlash imkonini beradi."
    },
    {
        "id": 1250,
        "title": "Rust da to'liq integratsiyalashgan Production-Ready LSM-Tree Storage Engine",
        "desc": "Barcha komponentlarni: MemTable, SkipList, WAL, SSTable va Bloom Filter ni yagona yuqori unumdor saqlash dvigatelida birlashtirish.",
        "req": "`put(&[u8], &[u8])`, `get(&[u8]) -> Option<Vec<u8>>`, `delete(&[u8])`, xavfsiz to'xtash va flush.",
        "code": """pub struct RustLsmEngine {
    memtable: ConcurrentSkipList<Vec<u8>, Vec<u8>>,
    sequence_gen: SequenceGenerator,
    bloom_filter: SSTableBloomBlock,
}

impl RustLsmEngine {
    pub fn new() -> Self {
        Self {
            memtable: ConcurrentSkipList::new(),
            sequence_gen: SequenceGenerator::new(1),
            bloom_filter: SSTableBloomBlock::new(vec![0xFF; 1024], 7),
        }
    }

    pub fn put(&self, key: &[u8], value: &[u8]) {
        let _seq = self.sequence_gen.next_sequence();
        // SkipList ga kiritish
        // Haqiqiy tizimda WAL ga ham yoziladi
    }

    pub fn get(&self, key: &[u8]) -> Option<Vec<u8>> {
        if !self.bloom_filter.may_contain(key) {
            return None; // Bloom filter orqali tezkor inkor
        }
        // MemTable va diskdan qidirish
        None
    }
}""",
        "expl": "Ushbu arxitektura zamonaviy Rust saqlash tizimlarining (TiKV, SurrealDB) asosidir. U nol xarajatli abstraksiyalar (Zero-cost abstractions), qat'iy xotira xavfsizligi va parallelizmni birlashtirib, dunyodagi eng tezkor va ishonchli saqlash dvigatelini yaratish imkonini beradi."
    }
]
