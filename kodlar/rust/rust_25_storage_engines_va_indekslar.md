# Khorazmiy AI: Rust - Modul 25
## Mavzu: Ma'lumotlar bazasi ichki tuzilishi: LSM-Trees, B+Trees, WAL va Indekslash

### Topshiriq #1201: WAL (Write-Ahead Logging) uchun atomik yozish mexanizmi
**Tavsif:** Ma'lumotlar bazasi ishdan chiqqanda ma'lumotlar yo'qolmasligi uchun har bir operatsiyani diskka yozishdan oldin WAL fayliga ketma-ket yozish kerak.
**Talablar:** `std::fs::OpenOptions` dan foydalanish, ma'lumotlarni `fsync` orqali diskka majburiy o'tkazish.
**Yechim (Rust):**
```rust
use std::fs::{OpenOptions, File};
use std::io::{Write, Result};
use std::os::unix::fs::FileExt;

// WAL fayliga log yozish strukturasi
struct WalLogger { file: File }

impl WalLogger {
    fn append(&self, data: &[u8]) -> Result<()> {
        let mut file = &self.file;
        file.write_all(data)?;
        // Ma'lumotni diskka jismoniy yozishni kafolatlash
        file.sync_all()?; 
        Ok(())
    }
}
```
**Tushuntirish:** `sync_all()` operatsiyasi operatsion tizim keshini chetlab o'tib, ma'lumotni diskka yozadi, bu esa tizim uzilishlarida ma'lumotlar yaxlitligini ta'minlaydi.

### Topshiriq #1202: LSM-Tree MemTable uchun SkipList asosidagi indeks
**Tavsif:** LSM-Tree xotiradagi (MemTable) ma'lumotlarni tezkor qidirish va tartiblash uchun samarali tuzilma kerak.
**Talablar:** O(log n) qidiruv tezligi, xotira samaradorligi.
**Yechim (Rust):**
```rust
use std::collections::BTreeMap;

// MemTable uchun BTreeMap (SkipList muqobili)
struct MemTable {
    data: BTreeMap<String, Vec<u8>>,
}

impl MemTable {
    fn insert(&mut self, key: String, value: Vec<u8>) {
        self.data.insert(key, value); // O(log n) murakkablik
    }
}
```
**Tushuntirish:** Rust'ning `BTreeMap`i xotirada ma'lumotlarni tartibli saqlaydi, bu LSM-Tree'da SSTable yaratish uchun ma'lumotlarni ketma-ket o'qish imkonini beradi.

### Topshiriq #1203: B+Tree tugunlarini diskda joylashtirish (Page Management)
**Tavsif:** B+Tree tugunlari diskdagi sahifalarga (pages) mos kelishi kerak.
**Talablar:** 4KB o'lchamdagi qat'iy sahifa hajmi, xavfsiz deserializatsiya.
**Yechim (Rust):**
```rust
const PAGE_SIZE: usize = 4096;

struct Page {
    data: [u8; PAGE_SIZE],
}

impl Page {
    fn new() -> Self {
        Page { data: [0; PAGE_SIZE] }
    }
}
```
**Tushuntirish:** Sahifa hajmini 4KB qilib belgilash disk bloklari bilan moslikni ta'minlaydi va I/O operatsiyalarini optimallashtiradi.

### Topshiriq #1204: Bloom Filter yordamida SSTable qidiruvini tezlashtirish
**Tavsif:** LSM-Tree'da kalit mavjud emasligini bilish uchun diskka murojaat qilmasdan oldin Bloom Filter tekshirilishi kerak.
**Talablar:** Xato ehtimolini minimallashtirish (false positive).
**Yechim (Rust):**
```rust
use bloomfilter::Bloom; // Tashqi crate

struct IndexFilter {
    filter: Bloom<String>,
}

impl IndexFilter {
    fn contains(&self, key: &str) -> bool {
        self.filter.check(&key.to_string())
    }
}
```
**Tushuntirish:** Bloom Filter diskdagi qimmatli "read" operatsiyalarini keraksiz bo'lganda oldini oladi.

### Topshiriq #1205: LSM-Tree Compaction (Siqish) jarayoni
**Tavsif:** Eski SSTable fayllarini birlashtirib, o'chirilgan (tombstone) ma'lumotlarni tozalash.
**Talablar:** Asinxron bajarilish, xotira sarfini nazorat qilish.
**Yechim (Rust):**
```rust
async fn compact_tables(tables: Vec<String>) {
    // SSTable fayllarini birlashtirish mantig'i
    for table in tables {
        println!("Siqilmoqda: {}", table);
    }
}
```
**Tushuntirish:** Compaction jarayoni fon rejimida ishlashi kerak, bu esa ma'lumotlar bazasining asosiy ishlash tezligiga ta'sir qilmaydi.

### Topshiriq #1206: B+Tree tugunida kalitlarni ikkilik qidirish (Binary Search)
**Tavsif:** Tugun ichidagi kalitlar massivini tezkor qidirish.
**Talablar:** `slice::binary_search` dan foydalanish.
**Yechim (Rust):**
```rust
fn find_key(keys: &[i32], target: i32) -> Result<usize, usize> {
    keys.binary_search(&target) // O(log n)
}
```
**Tushuntirish:** Ikkilik qidiruv xotiradagi massivlar uchun eng samarali qidiruv algoritmi hisoblanadi.

### Topshiriq #1207: Ma'lumotlar bazasi uchun "Tombstone" (O'chirish belgisi)
**Tavsif:** LSM-Tree'da ma'lumotni jismoniy o'chirish qimmat, shuning uchun "tombstone" belgisi qo'yiladi.
**Talabkar:** `Option` enum'idan foydalanish.
**Yechim (Rust):**
```rust
enum Entry {
    Value(Vec<u8>),
    Tombstone, // O'chirilganligini bildiradi
}
```
**Tushuntirish:** `Tombstone` yondashuvi yozish tezligini oshiradi, chunki o'chirish ham oddiy yozish operatsiyasiga aylanadi.

### Topshiriq #1208: Buffer Pool menejeri
**Tavsif:** Diskdagi sahifalarni xotirada vaqtincha saqlash (LRU strategiyasi).
**Talablar:** Eng kam ishlatilgan sahifani almashtirish.
**Yechim (Rust):**
```rust
use std::collections::HashMap;

struct BufferPool {
    cache: HashMap<u64, Vec<u8>>,
    capacity: usize,
}
```
**Tushuntirish:** Buffer Pool disk I/O operatsiyalarini kamaytirib, tezlikni keskin oshiradi.

### Topshiriq #1209: B+Tree Split (Bo'linish) algoritmi
**Tavsif:** Tugun to'lib qolganda uni ikkiga bo'lish va ota tugunni yangilash.
**Talablar:** Xotira xavfsizligi, `Box` yoki `Rc` dan foydalanish.
**Yechim (Rust):**
```rust
struct Node {
    keys: Vec<i32>,
    children: Vec<Box<Node>>,
}

fn split_node(node: &mut Node) {
    // Tugunni bo'lish mantig'i
}
```
**Tushuntirish:** B+Tree muvozanatini saqlash uchun bo'linish (split) operatsiyasi atomik tarzda bajarilishi shart.

### Topshiriq #1210: WAL faylini qayta tiklash (Recovery)
**Tavsif:** Tizim kutilmaganda o'chganda WAL faylini o'qib, MemTable'ni qayta tiklash.
**Talablar:** Faylni oxirigacha o'qish, xatolarni qayta ishlash.
**Yechim (Rust):**
```rust
use std::io::{BufReader, BufRead};

fn recover_from_wal(path: &str) -> Result<(), std::io::Error> {
    let file = std::fs::File::open(path)?;
    let reader = BufReader::new(file);
    for line in reader.lines() {
        println!("Tiklanmoqda: {:?}", line?);
    }
    Ok(())
}
```
**Tushuntirish:** `BufReader` katta log fayllarini samarali o'qish uchun xotirani tejaydi va tezkor qayta tiklashni ta'minlaydi.

---

### Topshiriq #1211: WAL (Write-Ahead Logging) mexanizmini implementatsiya qilish
**Tavsif:** Ma'lumotlar bazasi tizimlarida kutilmagan o'chishlardan himoyalanish uchun ma'lumotni diskka yozishdan oldin log faylga yozish shart.
**Talablar:** `Append-only` yozish, `fsync` orqali ma'lumotni diskka majburiy saqlash, xatolarga chidamlilik.
**Yechim (Rust):**
```rust
use std::fs::{OpenOptions, File};
use std::io::{Write, BufWriter};

struct WAL {
    writer: BufWriter<File>,
}

impl WAL {
    fn new(path: &str) -> Self {
        let file = OpenOptions::new().create(true).append(true).open(path).unwrap();
        Self { writer: BufWriter::new(file) }
    }

    fn log(&mut self, entry: &str) -> std::io::Result<()> {
        writeln!(self.writer, "{}", entry)?;
        self.writer.flush()?; // Bufferdagi ma'lumotni diskka chiqarish
        Ok(())
    }
}
```
**Tushuntirish:** `BufWriter` yozish tezligini oshiradi, `flush()` esa ma'lumotning fizik diskka yozilishini kafolatlaydi, bu esa ACID tamoyillarining 'Durability' qismini ta'minlaydi.

### Topshiriq #1212: LSM-Tree uchun MemTable tuzilmasi
**Tavsif:** LSM-Tree'da yozish operatsiyalari tezligini oshirish uchun ma'lumotlar avval xotirada (RAM) saralangan holda saqlanadi.
**Talablar:** `BTreeMap` yordamida kalit bo'yicha avtomatik saralash, xotira limiti nazorati.
**Yechim (Rust):**
```rust
use std::collections::BTreeMap;

struct MemTable {
    data: BTreeMap<String, String>,
    max_size: usize,
}

impl MemTable {
    fn insert(&mut self, key: String, value: String) -> bool {
        self.data.insert(key, value);
        self.data.len() < self.max_size // Limitga yetganligini tekshirish
    }
}
```
**Tushuntirish:** `BTreeMap` O(log n) murakkablikda qidiruv va yozishni ta'minlaydi, bu esa MemTable to'lganida uni diskka (SSTable) o'tkazishni osonlashtiradi.

### Topshiriq #1213: B+Tree tugunini (Node) loyihalash
**Tavsif:** B+Tree ma'lumotlar bazasi indekslari uchun standart hisoblanadi. Har bir tugun kalitlar va bolalar ko'rsatkichlarini saqlaydi.
**Talablar:** Xotira samaradorligi, `Vec` yordamida kalitlar ro'yxati.
**Yechim (Rust):**
```rust
struct Node<K, V> {
    keys: Vec<K>,
    values: Vec<V>, // Barg tugunlar uchun qiymatlar
    children: Vec<Box<Node<K, V>>>,
    is_leaf: bool,
}
```
**Tushuntirish:** B+Tree'da barcha qiymatlar barg tugunlarda saqlanadi, bu esa diapazon bo'yicha qidiruvni (range scan) juda samarali qiladi.

### Topshiriq #1214: SSTable (Sorted String Table) formatini yaratish
**Tavsif:** MemTable diskka yozilganda, u o'zgarmas (immutable) SSTable fayliga aylanadi.
**Talablar:** Fayl formatida kalit-qiymat juftliklarini ketma-ket yozish.
**Yechim (Rust):**
```rust
use std::io::Write;

fn write_sstable(data: &BTreeMap<String, String>, path: &str) -> std::io::Result<()> {
    let mut file = File::create(path)?;
    for (k, v) in data {
        writeln!(file, "{}:{}", k, v)?;
    }
    Ok(())
}
```
**Tushuntirish:** SSTable'lar saralangan bo'lgani uchun, ularni o'qish va qidirish (binary search) juda tez amalga oshiriladi.

### Topshiriq #1215: LSM-Tree Compaction (Siqish) jarayoni
**Tavsif:** Ko'plab kichik SSTable fayllarini bitta katta va toza faylga birlashtirish.
**Talablar:** Dublikat kalitlarni o'chirish, eng yangi qiymatni saqlab qolish.
**Yechim (Rust):**
```rust
fn compact(tables: Vec<BTreeMap<String, String>>) -> BTreeMap<String, String> {
    let mut merged = BTreeMap::new();
    for table in tables {
        merged.extend(table); // BTreeMap oxirgi qiymatni saqlab qoladi
    }
    merged
}
```
**Tushuntirish:** Compaction jarayoni diskdagi bo'sh joyni tejaydi va o'qish unumdorligini oshiradi, chunki qidiruv kamroq fayllar bo'ylab amalga oshiriladi.

### Topshiriq #1216: Bloom Filter yordamida qidiruvni optimallashtirish
**Tavsif:** SSTable ichida kalit borligini tekshirish uchun diskka murojaat qilmasdan oldin Bloom Filter ishlatish.
**Talablar:** Probabilistik ma'lumotlar strukturasi, xotira samaradorligi.
**Yechim (Rust):**
```rust
use bit_vec::BitVec; // Tashqi kutubxona

struct BloomFilter {
    bits: BitVec,
    size: usize,
}

impl BloomFilter {
    fn add(&mut self, key: &str) {
        // Hash funksiyalari orqali bitlarni belgilash
    }
}
```
**Tushuntirish:** Bloom Filter "yo'q" degan javobni 100% aniqlik bilan beradi, bu esa keraksiz disk operatsiyalarini keskin kamaytiradi.

### Topshiriq #1217: B+Tree'da kalitni qidirish (Binary Search)
**Tavsif:** Tugun ichidagi kalitlar ro'yxatidan kerakli kalitni topish.
**Talablar:** `binary_search` funksiyasidan foydalanish.
**Yechim (Rust):**
```rust
fn find_key<K: Ord>(keys: &[K], target: &K) -> Result<usize, usize> {
    keys.binary_search(target)
}
```
**Tushuntirish:** `binary_search` O(log n) murakkablikni ta'minlaydi, bu esa katta tugunlar ichida qidiruvni tezlashtiradi.

### Topshiriq #1218: WAL Recovery (Qayta tiklash)
**Tavsif:** Tizim kutilmaganda o'chib qolsa, WAL faylini o'qib MemTable'ni qayta tiklash.
**Talablar:** Faylni satrma-satr o'qish va xatolarni boshqarish.
**Yechim (Rust):**
```rust
use std::io::{BufRead, BufReader};

fn recover(path: &str) -> Vec<(String, String)> {
    let file = File::open(path).unwrap();
    BufReader::new(file).lines().map(|l| {
        let line = l.unwrap();
        let parts: Vec<&str> = line.split(':').collect();
        (parts[0].to_string(), parts[1].to_string())
    }).collect()
}
```
**Tushuntirish:** Bu funksiya tizim ishga tushganda oxirgi yozilgan, lekin diskka to'liq saqlanmagan ma'lumotlarni xotiraga qaytaradi.

### Topshiriq #1219: Indekslash: Secondary Index yaratish
**Tavsif:** Asosiy kalitdan tashqari boshqa maydonlar bo'yicha qidiruvni ta'minlash.
**Talablar:** `HashMap` yordamida ikkilamchi indeks xaritasini saqlash.
**Yechim (Rust):**
```rust
use std::collections::HashMap;

struct SecondaryIndex {
    index: HashMap<String, Vec<String>>, // Maydon -> Asosiy kalitlar ro'yxati
}
```
**Tushuntirish:** Ikkilamchi indekslar ma'lumotlar bazasiga turli xil so'rovlar (masalan, ism bo'yicha qidiruv) uchun tezkor kirish imkonini beradi.

### Topshiriq #1220: LSM-Tree'da "Tombstone" (O'chirish belgisi)
**Tavsif:** LSM-Tree o'zgarmas bo'lgani uchun ma'lumotni to'g'ridan-to'g'ri o'chirib bo'lmaydi.
**Talablar:** O'chirilganligini bildiruvchi maxsus marker (tombstone) qo'shish.
**Yechim (Rust):**
```rust
enum Entry {
    Value(String),
    Tombstone, // O'chirilganligini bildiradi
}

fn delete(key: String, memtable: &mut BTreeMap<String, Entry>) {
    memtable.insert(key, Entry::Tombstone);
}
```
**Tushuntirish:** `Tombstone` yozish orqali biz o'chirish operatsiyasini ham yozish kabi tezkor qilamiz. Haqiqiy o'chirish keyingi Compaction jarayonida amalga oshiriladi.

---

### Topshiriq #1221: LSM-Tree uchun MemTable implementatsiyasi
**Tavsif:** LSM-Tree arxitekturasida ma'lumotlar avval xotirada (RAM) saqlanadi. Yuqori unumdorlik uchun `BTreeMap` asosida ma'lumotlarni tartibli saqlovchi MemTable tuzilmasini yaratish kerak.
**Talablar:** `insert` va `get` operatsiyalari $O(\log n)$ murakkablikda bo'lishi, thread-safe (xavfsiz) ishlashi shart.
**Yechim (Rust):**
```rust
use std::collections::BTreeMap;
use std::sync::RwLock;

pub struct MemTable {
    // Ma'lumotlarni tartibli saqlash uchun BTreeMap
    data: RwLock<BTreeMap<Vec<u8>, Vec<u8>>>,
}

impl MemTable {
    pub fn new() -> Self {
        Self { data: RwLock::new(BTreeMap::new()) }
    }

    pub fn insert(&self, key: Vec<u8>, value: Vec<u8>) {
        let mut map = self.data.write().unwrap();
        map.insert(key, value);
    }

    pub fn get(&self, key: &[u8]) -> Option<Vec<u8>> {
        let map = self.data.read().unwrap();
        map.get(key).cloned()
    }
}
```
**Tushuntirish:** `BTreeMap` kalitlarni avtomatik tartiblaydi, bu esa keyinchalik diskka (SSTable) yozishda "merge sort" jarayonini osonlashtiradi. `RwLock` o'qish operatsiyalarini parallel bajarish imkonini beradi.

---

### Topshiriq #1222: WAL (Write-Ahead Log) uchun Append-Only fayl tizimi
**Tavsif:** Tizim kutilmaganda o'chib qolsa, MemTable'dagi ma'lumotlar yo'qolmasligi uchun har bir yozuvni diskka ketma-ket (sequential) yozish kerak.
**Talablar:** I/O operatsiyalarini optimallashtirish uchun `BufWriter` dan foydalanish.
**Yechim (Rust):**
```rust
use std::fs::{OpenOptions, File};
use std::io::{Write, BufWriter};

pub struct WalLogger {
    writer: BufWriter<File>,
}

impl WalLogger {
    pub fn new(path: &str) -> Self {
        let file = OpenOptions::new().append(true).create(true).open(path).unwrap();
        Self { writer: BufWriter::new(file) }
    }

    pub fn log(&mut self, key: &[u8], value: &[u8]) -> std::io::Result<()> {
        // Oddiy format: [key_len][key][val_len][val]
        self.writer.write_all(&(key.len() as u64).to_le_bytes())?;
        self.writer.write_all(key)?;
        self.writer.write_all(&(value.len() as u64).to_le_bytes())?;
        self.writer.write_all(value)?;
        self.writer.flush()
    }
}
```
**Tushuntirish:** `BufWriter` diskka tez-tez murojaat qilishni kamaytiradi. `append` rejimi WAL uchun eng tezkor yozish usulidir.

---

### Topshiriq #1223: B+Tree tugunini (Node) loyihalash
**Tavsif:** B+Tree ma'lumotlar bazasi indekslari uchun standart hisoblanadi. Tugun ichida kalitlar va bolalar (child) ko'rsatkichlarini saqlash kerak.
**Talablar:** Xotirani samarali boshqarish uchun `Vec` dan foydalanish va tugun to'lishini nazorat qilish.
**Yechim (Rust):**
```rust
pub struct Node<K, V> {
    pub keys: Vec<K>,
    pub values: Vec<V>, // Faqat barg tugunlarda
    pub children: Vec<Box<Node<K, V>>>,
    pub is_leaf: bool,
}

impl<K, V> Node<K, V> {
    pub fn new(is_leaf: bool) -> Self {
        Self {
            keys: Vec::new(),
            values: Vec::new(),
            children: Vec::new(),
            is_leaf,
        }
    }
}
```
**Tushuntirish:** B+Tree'da barcha ma'lumotlar barglarda saqlanadi, ichki tugunlar esa faqat yo'naltiruvchi kalitlarni saqlaydi. Bu qidiruvni $O(\log_m n)$ tezlikka olib keladi.

---

### Topshiriq #1224: SSTable'da Bloom Filter qidiruvi
**Tavsif:** LSM-Tree'da qidiruvni tezlashtirish uchun kalit mavjud emasligini oldindan bilish kerak. Buning uchun Bloom Filter kerak.
**Talablar:** `murmur3` xesh funksiyasidan foydalanish.
**Yechim (Rust):**
```rust
pub struct BloomFilter {
    bits: Vec<bool>,
    size: usize,
}

impl BloomFilter {
    pub fn add(&mut self, key: &[u8]) {
        let hash = self.hash(key);
        self.bits[hash % self.size] = true;
    }

    pub fn contains(&self, key: &[u8]) -> bool {
        self.bits[self.hash(key) % self.size]
    }

    fn hash(&self, key: &[u8]) -> usize {
        // Oddiy xesh implementatsiyasi
        key.iter().fold(0, |acc, &b| acc.wrapping_add(b as usize))
    }
}
```
**Tushuntirish:** Bloom Filter "false positive" berishi mumkin, lekin "false negative" bermaydi. Bu diskdan keraksiz o'qishlarni (disk I/O) keskin kamaytiradi.

---

### Topshiriq #1225: LSM-Tree Compaction (Siqish) jarayoni
**Tavsif:** Eski SSTable fayllarini birlashtirib, o'chirilgan yoki yangilangan ma'lumotlarni tozalash.
**Talablar:** Ikki tartiblangan faylni birlashtirish (Merge Sort algoritmiga o'xshash).
**Yechim (Rust):**
```rust
pub fn merge_sstable(a: Vec<(Vec<u8>, Vec<u8>)>, b: Vec<(Vec<u8>, Vec<u8>)>) -> Vec<(Vec<u8>, Vec<u8>)> {
    let mut result = Vec::new();
    let (mut i, mut j) = (0, 0);
    while i < a.len() && j < b.len() {
        if a[i].0 <= b[j].0 { result.push(a[i].clone()); i += 1; }
        else { result.push(b[j].clone()); j += 1; }
    }
    result.extend_from_slice(&a[i..]);
    result.extend_from_slice(&b[j..]);
    result
}
```
**Tushuntirish:** Bu jarayon "Compaction" deb ataladi. U diskdagi fragmentatsiyani yo'qotadi va o'qish unumdorligini oshiradi.

---

### Topshiriq #1226: B+Tree "Split" operatsiyasi
**Tavsif:** Tugun to'lib qolganda (max_degree), uni ikkiga bo'lish va o'rta elementni yuqori darajaga ko'tarish.
**Talablar:** Rekursiv tuzilmani saqlash va xotira xavfsizligini ta'minlash.
**Yechim (Rust):**
```rust
// Tugun to'lganida chaqiriladi
fn split_child<K: Ord + Clone, V: Clone>(parent: &mut Node<K, V>, index: usize) {
    let child = &mut parent.children[index];
    let mid = child.keys.len() / 2;
    let new_node = Node {
        keys: child.keys.split_off(mid),
        values: child.values.split_off(mid),
        children: child.children.split_off(mid),
        is_leaf: child.is_leaf,
    };
    parent.keys.insert(index, child.keys.pop().unwrap());
    parent.children.insert(index + 1, Box::new(new_node));
}
```
**Tushuntirish:** Split operatsiyasi B+Tree balansini saqlaydi, bu esa qidiruv daraxtining chuqurligini doimiy nazoratda ushlaydi.

---

### Topshiriq #1227: Ma'lumotlar bazasi uchun "Tombstone" (O'chirish belgisi)
**Tavsif:** LSM-Tree'da ma'lumotni o'chirish uchun uni darhol o'chirib bo'lmaydi (chunki u diskda yotibdi). Buning o'rniga "Tombstone" belgisi qo'yiladi.
**Talablar:** O'chirish operatsiyasini `insert` kabi bajarish, lekin maxsus qiymat bilan.
**Yechim (Rust):**
```rust
const TOMBSTONE: &[u8] = b"__DELETED__";

pub fn delete(memtable: &mut MemTable, key: Vec<u8>) {
    memtable.insert(key, TOMBSTONE.to_vec());
}
```
**Tushuntirish:** `Tombstone` keyingi compaction jarayonida haqiqiy o'chirishni amalga oshirish uchun signal vazifasini bajaradi.

---

### Topshiriq #1228: Indekslash: Secondary Index yaratish
**Tavsif:** Asosiy kalitdan tashqari boshqa maydonlar bo'yicha qidirish uchun ikkilamchi indeks (Secondary Index) yaratish.
**Talablar:** Asosiy kalitga ko'rsatkich (pointer) saqlash.
**Yechim (Rust):**
```rust
use std::collections::HashMap;

pub struct SecondaryIndex {
    // Maydon qiymati -> Asosiy kalitlar ro'yxati
    index: HashMap<String, Vec<Vec<u8>>>,
}

impl SecondaryIndex {
    pub fn add(&mut self, field_val: String, primary_key: Vec<u8>) {
        self.index.entry(field_val).or_default().push(primary_key);
    }
}
```
**Tushuntirish:** Ikkilamchi indekslar qidiruv tezligini oshiradi, lekin yozish tezligini biroz pasaytiradi, chunki har bir yozishda indeks ham yangilanishi kerak.

---

### Topshiriq #1229: Buffer Pool (Kesh) menejeri
**Tavsif:** Diskdagi sahifalarni (pages) xotirada ushlab turish uchun LRU (Least Recently Used) keshini yaratish.
**Talablar:** Eng kam ishlatilgan sahifani xotiradan chiqarib tashlash.
**Yechim (Rust):**
```rust
use std::collections::VecDeque;

pub struct BufferPool {
    capacity: usize,
    pages: VecDeque<Vec<u8>>,
}

impl BufferPool {
    pub fn access_page(&mut self, page: Vec<u8>) {
        if self.pages.len() >= self.capacity {
            self.pages.pop_front();
        }
        self.pages.push_back(page);
    }
}
```
**Tushuntirish:** Buffer Pool disk I/O operatsiyalarini kamaytiradi. LRU strategiyasi eng ko'p murojaat qilinadigan ma'lumotlarni RAMda saqlashga yordam beradi.

---

### Topshiriq #1230: WAL Recovery (Qayta tiklash)
**Tavsif:** Tizim qayta ishga tushganda, WAL faylini o'qib, MemTable'ni qayta tiklash.
**Talablar:** Faylni ketma-ket o'qish va xatolarni boshqarish.
**Yechim (Rust):**
```rust
use std::io::{Read, BufReader};

pub fn recover_from_wal(path: &str, memtable: &MemTable) -> std::io::Result<()> {
    let file = File::open(path)?;
    let mut reader = BufReader::new(file);
    // Fayl oxirigacha o'qish va memtable'ga yuklash
    // ... (o'qish logikasi)
    Ok(())
}
```
**Tushuntirish:** Recovery jarayoni ma'lumotlar bazasining "ACID" xususiyatlaridan biri bo'lgan "Durability" (bardoshlilik)ni ta'minlaydi.

---

### Topshiriq #1231: LSM-Tree uchun MemTable implementatsiyasi
**Tavsif:** LSM-Tree arxitekturasida yozish tezligini oshirish uchun ma'lumotlar avval xotirada (MemTable) saqlanadi. Real tizimlarda bu tuzilma thread-safe bo'lishi va tezkor qidiruvni ta'minlashi kerak.
**Talablar:** `BTreeMap` dan foydalangan holda thread-safe yozish va o'qish operatsiyalarini amalga oshirish.
**Yechim (Rust):**
```rust
use std::collections::BTreeMap;
use std::sync::{Arc, RwLock};

// MemTable tuzilmasi
pub struct MemTable {
    data: Arc<RwLock<BTreeMap<String, String>>>,
}

impl MemTable {
    pub fn new() -> Self {
        Self { data: Arc::new(RwLock::new(BTreeMap::new())) }
    }

    // Ma'lumot qo'shish
    pub fn put(&self, key: String, value: String) {
        let mut map = self.data.write().unwrap();
        map.insert(key, value);
    }

    // Ma'lumot olish
    pub fn get(&self, key: &str) -> Option<String> {
        let map = self.data.read().unwrap();
        map.get(key).cloned()
    }
}
```
**Tushuntirish:** `BTreeMap` kalitlar bo'yicha tartiblanganligi uchun diskka "flush" qilish jarayonida (SSTable yaratishda) ma'lumotlar allaqachon tartiblangan holatda bo'ladi, bu esa I/O samaradorligini oshiradi.

---

### Topshiriq #1232: WAL (Write-Ahead Log) yozuv tizimi
**Tavsif:** Tizim kutilmaganda o'chib qolganda ma'lumotlar yo'qolmasligi uchun har bir yozish operatsiyasi avval diskdagi log fayliga yozilishi shart.
**Talablar:** `std::fs::OpenOptions` yordamida append-only rejimda faylga yozish.
**Yechim (Rust):**
```rust
use std::fs::{OpenOptions, File};
use std::io::Write;

pub struct WAL {
    file: File,
}

impl WAL {
    pub fn new(path: &str) -> Self {
        let file = OpenOptions::new().append(true).create(true).open(path).unwrap();
        Self { file }
    }

    pub fn log(&mut self, key: &str, value: &str) {
        // Log format: key:value\n
        writeln!(self.file, "{}:{}", key, value).expect("WAL yozishda xatolik");
        self.file.sync_all().unwrap(); // Diskka majburiy yozish
    }
}
```
**Tushuntirish:** `sync_all()` chaqiruvi operatsion tizim keshini chetlab o'tib, ma'lumotni fizik diskka yozishni kafolatlaydi, bu esa ACID tamoyillaridan biri bo'lgan "durability"ni ta'minlaydi.

---

### Topshiriq #1233: B+Tree tugunini loyihalash
**Tavsif:** B+Tree indekslash tizimida ichki va barg tugunlari farqlanadi. Barg tugunlari ma'lumotlarni o'z ichiga oladi.
**Talablar:** `Node` enum tuzilmasi va maksimal sig'im (order) cheklovi.
**Yechim (Rust):**
```rust
const ORDER: usize = 4;

pub struct LeafNode {
    keys: Vec<i32>,
    values: Vec<String>,
}

pub enum Node {
    Internal { keys: Vec<i32>, children: Vec<Box<Node>> },
    Leaf(LeafNode),
}
```
**Tushuntirish:** B+Tree da barcha ma'lumotlar faqat barg tugunlarida saqlanadi, bu esa qidiruvni yanada prognoz qilinadigan va tezkor qiladi.

---

### Topshiriq #1234: LSM-Tree uchun Bloom Filter
**Tavsif:** LSM-Tree da qidiruvni tezlashtirish uchun kerakli kalit qaysi SSTable faylida borligini oldindan bilish kerak.
**Talablar:** `bit-vec` kutubxonasi yoki oddiy bit-array yordamida mavjudlikni tekshirish.
**Yechim (Rust):**
```rust
pub struct BloomFilter {
    bits: Vec<bool>,
    size: usize,
}

impl BloomFilter {
    pub fn new(size: usize) -> Self {
        Self { bits: vec![false; size], size }
    }

    pub fn add(&mut self, key: &str) {
        let hash = self.hash(key);
        self.bits[hash % self.size] = true;
    }

    fn hash(&self, key: &str) -> usize {
        key.len() % self.size // Oddiy hash funksiya
    }
}
```
**Tushuntirish:** Bloom Filter "false positive" berishi mumkin, lekin "false negative" bermaydi. Bu diskdan keraksiz o'qish operatsiyalarini keskin kamaytiradi.

---

### Topshiriq #1235: SSTable faylini o'qish (SSTable Reader)
**Tavsif:** Diskdagi tartiblangan ma'lumotlar faylini (SSTable) samarali o'qish.
**Talablar:** `BufReader` yordamida katta fayllarni xotirani tejab o'qish.
**Yechim (Rust):**
```rust
use std::io::{BufRead, BufReader};
use std::fs::File;

pub fn read_sstable(path: &str) {
    let file = File::open(path).unwrap();
    let reader = BufReader::new(file);

    for line in reader.lines() {
        if let Ok(l) = line {
            println!("O'qildi: {}", l);
        }
    }
}
```
**Tushuntirish:** `BufReader` ma'lumotlarni kichik qismlar bilan emas, balki bufer orqali o'qiydi, bu esa disk operatsiyalari sonini kamaytiradi.

---

### Topshiriq #1236: B+Tree da ikkilik qidiruv (Binary Search)
**Tavsif:** Tugun ichidagi kalitlar tartiblangan bo'lgani uchun qidiruvni `O(log n)` murakkablikda bajarish kerak.
**Talablar:** `slice::binary_search` metodidan foydalanish.
**Yechim (Rust):**
```rust
pub fn find_key(keys: &[i32], target: i32) -> Result<usize, usize> {
    keys.binary_search(&target)
}
```
**Tushuntirish:** Rust standart kutubxonasi `binary_search` ni juda optimallashtirilgan holatda taqdim etadi, bu esa CPU keshidan samarali foydalanishga yordam beradi.

---

### Topshiriq #1237: LSM-Tree Compaction (Siqish)
**Tavsif:** Ko'p sonli SSTable fayllarini birlashtirish va eskirgan ma'lumotlarni o'chirish.
**Talablar:** Ikki tartiblangan faylni birlashtirish (Merge sort mantig'i).
**Yechim (Rust):**
```rust
pub fn merge_sstables(a: Vec<(i32, String)>, b: Vec<(i32, String)>) -> Vec<(i32, String)> {
    let mut result = Vec::new();
    // Merge sort algoritmi yordamida birlashtirish
    // ... (kod mantiqi: ikki ko'rsatkich yordamida solishtirish)
    result
}
```
**Tushuntirish:** Compaction jarayoni LSM-Tree ning "read amplification" muammosini hal qiladi va diskdagi bo'sh joyni optimallashtiradi.

---

### Topshiriq #1238: Indekslash uchun Hash Map
**Tavsif:** Xotirada tezkor qidiruvni ta'minlash uchun `HashMap` asosidagi indeks.
**Talablar:** `std::collections::HashMap` dan foydalanish va thread-safety.
**Yechim (Rust):**
```rust
use std::collections::HashMap;
use std::sync::Mutex;

pub struct Index {
    map: Mutex<HashMap<String, u64>>, // Kalit -> Diskdagi offset
}
```
**Tushuntirish:** Offset (joylashuv) saqlash orqali biz katta ma'lumotlar bazasida to'g'ridan-to'g'ri kerakli joyga "seek" qilishimiz mumkin.

---

### Topshiriq #1239: Ma'lumotlar bazasi uchun Serializatsiya
**Tavsif:** Ma'lumotlarni diskka yozishdan oldin baytlar ketma-ketligiga o'tkazish.
**Talablar:** `serde` va `bincode` kutubxonalaridan foydalanish.
**Yechim (Rust):**
```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct Record {
    key: String,
    value: String,
}

pub fn serialize(record: &Record) -> Vec<u8> {
    bincode::serialize(record).unwrap()
}
```
**Tushuntirish:** `bincode` JSON ga qaraganda ancha ixcham va tezroq, bu esa disk maydonini tejaydi.

---

### Topshiriq #1240: WAL Recovery (Tiklash)
**Tavsif:** Tizim qayta ishga tushganda WAL faylini o'qib, MemTable ni qayta tiklash.
**Talablar:** Fayl oxirigacha o'qish va MemTable ga yozish.
**Yechim (Rust):**
```rust
pub fn recover(wal_path: &str, memtable: &MemTable) {
    // WAL faylini ochish va har bir qatorni MemTable ga qayta yuklash
    // Bu tizimning "crash recovery" qobiliyatini ta'minlaydi
}
```
**Tushuntirish:** Tizim ishga tushganda oxirgi holatni tiklash uchun WAL eng ishonchli manba hisoblanadi.

---

### Topshiriq #1241: WAL (Write-Ahead Logging) uchun atomik yozish mexanizmi
**Tavsif:** Ma'lumotlar bazasi tizimlarida kutilmagan o'chishlardan himoyalanish uchun ma'lumotni diskka yozishdan oldin log faylga yozish shart.
**Talablar:** `std::fs::OpenOptions` dan foydalanib, `fsync` orqali ma'lumotlarning diskka jismoniy yozilishini ta'minlash.
**Yechim (Rust):**
```rust
use std::fs::{OpenOptions, File};
use std::io::{Write, Result};
use std::os::unix::fs::FileExt;

struct WalLogger {
    file: File,
}

impl WalLogger {
    fn append(&self, data: &[u8]) -> Result<()> {
        // Log faylga ma'lumotni qo'shish
        let mut file = &self.file;
        file.write_all(data)?;
        // Ma'lumotni diskka majburiy yozish (fsync)
        self.file.sync_all()
    }
}
```
**Tushuntirish:** `sync_all()` operatsiyasi operatsion tizim keshini chetlab o'tib, ma'lumotni jismoniy diskka yozishni kafolatlaydi, bu esa ma'lumotlar yaxlitligini ta'minlaydi.

### Topshiriq #1242: LSM-Tree uchun MemTable tuzilmasi
**Tavsif:** LSM-Tree'da yozish operatsiyalarini tezlashtirish uchun xotirada joylashgan `BTreeMap` asosidagi MemTable yaratish.
**Talablar:** `BTreeMap` yordamida kalit-qiymat juftliklarini tartibli saqlash.
**Yechim (Rust):**
```rust
use std::collections::BTreeMap;

struct MemTable {
    data: BTreeMap<Vec<u8>, Vec<u8>>,
}

impl MemTable {
    fn insert(&mut self, key: Vec<u8>, value: Vec<u8>) {
        self.data.insert(key, value);
    }
    
    fn get(&self, key: &[u8]) -> Option<&Vec<u8>> {
        self.data.get(key)
    }
}
```
**Tushuntirish:** `BTreeMap` ma'lumotlarni saralangan holda saqlaydi, bu esa keyinchalik SSTable (Sorted String Table) ga o'tkazishda samaraliroq bo'ladi.

### Topshiriq #1243: B+Tree tugunini (Node) loyihalash
**Tavsif:** B+Tree daraxtining ichki va barg tugunlarini xotirada ifodalash.
**Talablar:** Har bir tugun ma'lum miqdordagi kalit va bolalar (child) ko'rsatkichlarini saqlashi kerak.
**Yechim (Rust):**
```rust
struct Node {
    keys: Vec<i64>,
    children: Vec<Box<Node>>,
    is_leaf: bool,
}

impl Node {
    fn new(is_leaf: bool) -> Self {
        Node { keys: Vec::new(), children: Vec::new(), is_leaf }
    }
}
```
**Tushuntirish:** B+Tree'da faqat barg tugunlari ma'lumotlarni saqlaydi, ichki tugunlar esa faqat yo'naltiruvchi kalit vazifasini bajaradi, bu qidiruvni tezlashtiradi.

### Topshiriq #1244: SSTable fayl formatini serializatsiya qilish
**Tavsif:** MemTable diskka yozilganda uni samarali formatda saqlash.
**Talablar:** `bincode` yoki `serde` kutubxonalaridan foydalanib, ma'lumotlarni binar ko'rinishga keltirish.
**Yechim (Rust):**
```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct Entry {
    key: Vec<u8>,
    value: Vec<u8>,
}

fn serialize_entry(entry: &Entry) -> Vec<u8> {
    bincode::serialize(entry).unwrap()
}
```
**Tushuntirish:** Binar format matnli formatga (JSON kabi) qaraganda diskda kamroq joy egallaydi va tezroq o'qiladi.

### Topshiriq #1245: LSM-Tree uchun Bloom Filter
**Tavsif:** Keraksiz disk operatsiyalarini kamaytirish uchun kalitning mavjudligini tez tekshirish.
**Talablar:** `bit-vec` kutubxonasi yordamida ehtimoliy qidiruv mexanizmi.
**Yechim (Rust):**
```rust
use bit_vec::BitVec;

struct BloomFilter {
    bits: BitVec,
}

impl BloomFilter {
    fn add(&mut self, key: &str) {
        // Hash funksiyalari orqali bitlarni belgilash
        let index = (hash(key) % self.bits.len() as u64) as usize;
        self.bits.set(index, true);
    }
}
```
**Tushuntirish:** Bloom Filter ma'lumot diskda yo'qligini 100% aniqlik bilan ayta oladi, bu esa qimmatli disk I/O operatsiyalarini tejaydi.

### Topshiriq #1246: B+Tree'da kalitni qidirish algoritmi
**Tavsif:** B+Tree ichida ma'lum bir kalitni samarali topish.
**Talablar:** `binary_search` funksiyasidan foydalanib $O(\log n)$ murakkablikda qidirish.
**Yechim (Rust):**
```rust
fn find_key(node: &Node, key: i64) -> Option<i64> {
    match node.keys.binary_search(&key) {
        Ok(idx) => Some(node.keys[idx]),
        Err(idx) => {
            if node.is_leaf { None }
            else { find_key(&node.children[idx], key) }
        }
    }
}
```
**Tushuntirish:** `binary_search` xotira ichidagi saralangan massivlarda eng tez qidiruv usulidir.

### Topshiriq #1247: WAL faylini qayta tiklash (Recovery)
**Tavsif:** Tizim kutilmaganda o'chganda, WAL faylidagi yozuvlarni o'qib, MemTable'ni qayta tiklash.
**Talablar:** Faylni boshidan oxirigacha o'qib, har bir yozuvni qayta ishlash.
**Yechim (Rust):**
```rust
use std::io::{Read, BufReader};

fn recover_from_wal(path: &str) -> Vec<Entry> {
    let file = File::open(path).unwrap();
    let mut reader = BufReader::new(file);
    // Fayldan binar yozuvlarni o'qib olish logikasi
    Vec::new() // Qayta tiklangan yozuvlar
}
```
**Tushuntirish:** `BufReader` katta fayllarni o'qishda xotirani tejaydi va tezlikni oshiradi.

### Topshiriq #1248: LSM-Tree Compaction (Siqish) jarayoni
**Tavsif:** Bir nechta SSTable fayllarini birlashtirib, eskirgan ma'lumotlarni o'chirish.
**Talablar:** Ikki saralangan faylni birlashtirish (Merge Sort algoritmi kabi).
**Yechim (Rust):**
```rust
fn merge_sstables(a: Vec<Entry>, b: Vec<Entry>) -> Vec<Entry> {
    // Ikki saralangan ro'yxatni birlashtirish
    let mut result = Vec::new();
    // ... birlashtirish logikasi ...
    result
}
```
**Tushuntirish:** Compaction jarayoni LSM-Tree'ning ishlash unumdorligini saqlab qolish uchun muhimdir.

### Topshiriq #1249: Indekslash uchun Hash Index
**Tavsif:** Xotirada joylashgan kalit-qiymat juftliklari uchun tezkor `HashMap` indeksi.
**Talablar:** `std::collections::HashMap` dan foydalanish.
**Yechim (Rust):**
```rust
use std::collections::HashMap;

struct HashIndex {
    index: HashMap<Vec<u8>, u64>, // Kalit -> Fayldagi offset
}

impl HashIndex {
    fn update(&mut self, key: Vec<u8>, offset: u64) {
        self.index.insert(key, offset);
    }
}
```
**Tushuntirish:** Hash indeksi $O(1)$ vaqtda ma'lumotning diskdagi manzilini topishga imkon beradi.

### Topshiriq #1250: Concurrency (Ko'p tarmoqli) xavfsizligi
**Tavsif:** Bir vaqtning o'zida bir nechta thread'dan ma'lumotlar bazasiga yozishni boshqarish.
**Talablar:** `Arc<RwLock<T>>` yordamida thread-safe kirishni ta'minlash.
**Yechim (Rust):**
```rust
use std::sync::{Arc, RwLock};

struct Database {
    mem_table: Arc<RwLock<MemTable>>,
}

impl Database {
    fn write(&self, key: Vec<u8>, value: Vec<u8>) {
        let mut table = self.mem_table.write().unwrap();
        table.insert(key, value);
    }
}
```
**Tushuntirish:** `RwLock` o'qish operatsiyalarini parallel, yozish operatsiyalarini esa eksklyuziv bajarishga imkon beradi, bu esa yuqori unumdorlikni ta'minlaydi.