# Khorazmiy AI: Go - Modul 25
## Mavzu: Ma'lumotlar bazasi ichki tuzilishi: LSM-Trees, B+Trees, WAL va Indekslash

### Topshiriq #1201: WAL (Write-Ahead Logging) mexanizmini implementatsiya qilish
**Tavsif:** Ma'lumotlar bazasida kutilmagan o'chishlar (crash) sodir bo'lganda ma'lumotlar yaxlitligini saqlash uchun operatsiyalarni diskka yozishdan oldin log faylga yozish zarurati.
**Talablar:** Faylga yozish operatsiyasi atomar bo'lishi va `fsync` orqali diskka majburiy yozilishi kerak.
**Yechim (Go):**
```go
package main

import (
	"os"
)

// WAL strukturasi
type WAL struct {
	file *os.File
}

// Log yozish va diskka majburiy saqlash
func (w *WAL) Write(data []byte) error {
	_, err := w.file.Write(data)
	if err != nil {
		return err
	}
	// Ma'lumotni diskka fizik yozish
	return w.file.Sync()
}
```
**Tushuntirish:** `Sync()` funksiyasi operatsion tizim keshini chetlab o'tib, ma'lumotni to'g'ridan-to'g'ri diskka yozishni ta'minlaydi, bu ma'lumotlar xavfsizligi uchun kritik ahamiyatga ega.

### Topshiriq #1202: LSM-Tree uchun MemTable (In-memory buffer)
**Tavsif:** LSM-Tree arxitekturasida yozish tezligini oshirish uchun ma'lumotlarni avval xotirada (RAM) to'plash va keyin diskka "flush" qilish.
**Talablar:** Thread-safe yozish va ma'lumotlar hajmi chegarasi (threshold).
**Yechim (Go):**
```go
import "sync"

type MemTable struct {
	data  map[string][]byte
	mu    sync.RWMutex
	limit int
}

func (m *MemTable) Put(key string, value []byte) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.data[key] = value
}
```
**Tushuntirish:** `sync.RWMutex` yordamida yozish operatsiyalari bloklanadi, bu esa yuqori yuklamali tizimlarda ma'lumotlar poygasining (race condition) oldini oladi.

### Topshiriq #1203: B+Tree tugunini (Node) loyihalash
**Tavsif:** Indekslash samaradorligini oshirish uchun ma'lumotlarni daraxtsimon tuzilmada saqlash.
**Talablar:** Tugun ichida kalitlar tartiblangan bo'lishi va qidiruv O(log n) vaqtda bajarilishi.
**Yechim (Go):**
```go
type Node struct {
	Keys     []int
	Children []*Node
	IsLeaf   bool
}

// Binary search orqali kalitni topish
func (n *Node) Find(key int) int {
	low, high := 0, len(n.Keys)-1
	for low <= high {
		mid := (low + high) / 2
		if n.Keys[mid] == key { return mid }
		if n.Keys[mid] < key { low = mid + 1 } else { high = mid - 1 }
	}
	return -1
}
```
**Tushuntirish:** B+Tree barg tugunlarida ma'lumotlarni saqlash va ularni o'zaro bog'lash (linked list) diapazonli qidiruvni (range scan) tezlashtiradi.

### Topshiriq #1204: LSM-Tree uchun SSTable (Sorted String Table)
**Tavsif:** MemTable to'lganida uni diskka tartiblangan holda yozish.
**Talablar:** Yozish jarayonida kalitlar bo'yicha saralangan bo'lishi shart.
**Yechim (Go):**
```go
import "sort"

func WriteSSTable(data map[string][]byte) {
	keys := make([]string, 0, len(data))
	for k := range data { keys = append(keys, k) }
	sort.Strings(keys) // Diskka yozishdan oldin tartiblash
	// Faylga yozish logikasi...
}
```
**Tushuntirish:** SSTable diskda tartiblangan bo'lishi qidiruv vaqtida "Binary Search" imkonini beradi, bu esa o'qish tezligini sezilarli oshiradi.

### Topshiriq #1205: Bloom Filter yordamida qidiruvni optimallashtirish
**Tavsif:** LSM-Tree'da kalit mavjudligini tekshirish uchun diskka murojaat qilmasdan avval xotirada tezkor tekshiruv o'tkazish.
**Talablar:** Ehtimollik nazariyasiga asoslangan tezkor tekshiruv.
**Yechim (Go):**
```go
type BloomFilter struct {
	bits []bool
	size int
}

func (b *BloomFilter) Add(key string) {
	// Hash funksiyalar orqali bitlarni belgilash
}
```
**Tushuntirish:** Bloom Filter "yo'q" degan javobni 100% aniqlik bilan beradi, bu esa keraksiz disk operatsiyalarini (I/O) keskin kamaytiradi.

### Topshiriq #1206: B+Tree bo'linish (Split) mexanizmi
**Tavsif:** Tugun to'lib qolganda daraxt balansini saqlash uchun tugunni ikkiga bo'lish.
**Talablar:** Daraxt balansi saqlanishi va ota-tugunga yangi kalit ko'tarilishi.
**Yechim (Go):**
```go
func (n *Node) Split() (*Node, int) {
	mid := len(n.Keys) / 2
	newNode := &Node{Keys: n.Keys[mid+1:]}
	median := n.Keys[mid]
	n.Keys = n.Keys[:mid]
	return newNode, median
}
```
**Tushuntirish:** Bu mexanizm B+Tree'ning har doim muvozanatli (balanced) bo'lishini ta'minlaydi, bu esa qidiruv vaqtini doimiy O(log n) darajasida ushlab turadi.

### Topshiriq #1207: Ma'lumotlarni siqish (Compaction) jarayoni
**Tavsif:** LSM-Tree'da eski va yangi ma'lumotlar to'plamini birlashtirib, dublikatlarni o'chirish.
**Talablar:** Xotira sarfini minimallashtirish va eski fayllarni tozalash.
**Yechim (Go):**
```go
func Compact(tables ...[]string) []string {
	// Merge sort algoritmi yordamida birlashtirish
	return mergedData
}
```
**Tushuntirish:** Compaction jarayoni diskdagi "fragmentatsiya"ni yo'qotadi va o'qish jarayonini tezlashtiradi, chunki qidiruv kamroq fayllar bo'ylab amalga oshiriladi.

### Topshiriq #1208: Indeks fayli uchun Offset Map
**Tavsif:** Katta ma'lumotlar faylida kalit qayerda joylashganini tez topish uchun indeks yaratish.
**Talablar:** O(1) vaqtda offsetni aniqlash.
**Yechim (Go):**
```go
type Index struct {
	offsets map[string]int64
}

func (idx *Index) GetOffset(key string) (int64, bool) {
	val, ok := idx.offsets[key]
	return val, ok
}
```
**Tushuntirish:** Xotirada saqlanadigan `map` yordamida diskdagi ma'lumotning aniq manzilini (offset) bilish, diskdan o'qish operatsiyasini bitta `Seek` amali bilan bajarishga imkon beradi.

### Topshiriq #1209: WAL Recovery (Qayta tiklash)
**Tavsif:** Tizim kutilmaganda o'chganda, WAL fayldan ma'lumotlarni o'qib MemTable'ni qayta tiklash.
**Talablar:** Fayl oxirigacha o'qish va ma'lumotlarni qayta yuklash.
**Yechim (Go):**
```go
func (w *WAL) Recover() {
	// Faylni ochiq va har bir qatorni MemTable'ga qayta yozish
	// ...
}
```
**Tushuntirish:** Tizim ishga tushganda WAL faylini qayta ishlash, tranzaksiyalarning yo'qolmasligini ta'minlaydigan "Durability" (ACID) xususiyatini ta'minlaydi.

### Topshiriq #1210: Range Query (Diapazonli qidiruv)
**Tavsif:** B+Tree'da ma'lum bir oraliqdagi (masalan, 100 dan 200 gacha) barcha kalitlarni olish.
**Talablar:** Barg tugunlari orasidagi bog'lanishdan (Leaf pointers) foydalanish.
**Yechim (Go):**
```go
func (n *Node) RangeScan(start, end int) []int {
	// Barg tugunlari bo'ylab iteratsiya qilish
	return results
}
```
**Tushuntirish:** B+Tree'ning barg tugunlari o'zaro bog'langanligi sababli, diapazonli qidiruv daraxtni qayta-qayta aylanib chiqmasdan, shunchaki ro'yxat bo'ylab yurish orqali amalga oshiriladi.

---

### Topshiriq #1211: WAL (Write-Ahead Logging) mexanizmini implementatsiya qilish
**Tavsif:** Ma'lumotlar bazasida kutilmagan o'chishlar (crash) yuz berganda ma'lumotlar yaxlitligini ta'minlash uchun operatsiyalarni diskka yozishdan oldin log faylga yozish zarurati.
**Talablar:** `fsync` orqali diskka ma'lumotni to'liq yozish, atomiklikni ta'minlash.
**Yechim (Go):**
```go
package main

import (
	"os"
)

// WAL strukturasi
type WAL struct {
	file *os.File
}

// Log yozish va diskka majburiy saqlash
func (w *WAL) Write(data []byte) error {
	_, err := w.file.Write(data)
	if err != nil {
		return err
	}
	// Ma'lumotni diskka fizik yozish
	return w.file.Sync() 
}
```
**Tushuntirish:** `Sync()` funksiyasi operatsion tizim keshini chetlab o'tib, ma'lumotni to'g'ridan-to'g'ri diskka yozadi, bu esa tizim qulaganda ma'lumot yo'qolishining oldini oladi.

### Topshiriq #1212: LSM-Tree uchun MemTable tuzilmasi
**Tavsif:** LSM-Tree'da yozish operatsiyalarini tezlashtirish uchun xotirada joylashgan (in-memory) tartiblangan tuzilma zarur.
**Talablar:** O(log n) vaqt murakkabligida qidiruv va qo'shish.
**Yechim (Go):**
```go
import "github.com/emirpasic/gods/trees/redblacktree"

// MemTable - LSM-Tree uchun xotira buferi
type MemTable struct {
	tree *redblacktree.Tree
}

func NewMemTable() *MemTable {
	return &MemTable{tree: redblacktree.NewWithStringComparator()}
}

func (m *MemTable) Put(key, value string) {
	m.tree.Put(key, value) // Qizil-qora daraxt yordamida tartiblash
}
```
**Tushuntirish:** Qizil-qora daraxtlar (Red-Black Trees) yozish va o'qishda barqaror O(log n) tezlikni ta'minlaydi, bu esa MemTable uchun idealdir.

### Topshiriq #1213: B+Tree tugunini (Node) loyihalash
**Tavsif:** Diskdagi ma'lumotlarni sahifalash (paging) uchun B+Tree tugunlarini optimallashtirilgan formatda saqlash.
**Talablar:** Tugun hajmini disk sahifasi hajmiga (4KB) moslashtirish.
**Yechim (Go):**
```go
type Node struct {
	IsLeaf   bool
	Keys     []int64
	Values   [][]byte
	Children []int64 // Keyingi tugunlarning diskdagi manzillari
}
```
**Tushuntirish:** B+Tree'da faqat barg (leaf) tugunlar qiymatlarni saqlaydi, bu esa qidiruvni tezlashtiradi va diskga murojaatlarni kamaytiradi.

### Topshiriq #1214: LSM-Tree uchun SSTable (Sorted String Table) yaratish
**Tavsif:** MemTable to'lganda uni diskka o'zgarmas (immutable) fayl sifatida yozish.
**Talablar:** Fayl formatini ixcham saqlash va indekslash.
**Yechim (Go):**
```go
func FlushToSSTable(data map[string]string, filename string) error {
	f, _ := os.Create(filename)
	defer f.Close()
	// Ma'lumotlarni tartiblangan holda yozish
	return nil 
}
```
**Tushuntirish:** SSTable o'zgarmas bo'lgani uchun uni o'qish juda tez va konkurentlik muammolarini keltirib chiqarmaydi.

### Topshiriq #1215: B+Tree qidiruv algoritmi
**Tavsif:** B+Tree ichida kalit bo'yicha samarali qidiruvni amalga oshirish.
**Talablar:** O(log M N) vaqt murakkabligi.
**Yechim (Go):**
```go
func (n *Node) Search(key int64) []byte {
	// Binary search orqali kalitni topish
	idx := sort.Search(len(n.Keys), func(i int) bool { return n.Keys[i] >= key })
	if n.IsLeaf {
		return n.Values[idx]
	}
	return nil // Rekursiv davom etish
}
```
**Tushuntirish:** `sort.Search` funksiyasi xotira ichida binar qidiruvni amalga oshiradi, bu esa tugun ichidagi qidiruvni maksimal tezlashtiradi.

### Topshiriq #1216: LSM-Tree Compaction (Siqish) jarayoni
**Tavsif:** Eski SSTable fayllarini birlashtirib, o'chirilgan ma'lumotlarni tozalash.
**Talablar:** I/O operatsiyalarini minimallashtirish.
**Yechim (Go):**
```go
func Compact(tables []string) {
	// Ikki yoki undan ortiq SSTable'ni birlashtirib, 
	// eng yangi versiyani saqlab qolish
}
```
**Tushuntirish:** Compaction jarayoni LSM-Tree'ning ishlash unumdorligini saqlab qolish uchun muhim, chunki u diskdagi "chiqindilarni" tozalaydi.

### Topshiriq #1217: Indekslash: Hash Index implementatsiyasi
**Tavsif:** Kalit-qiymat juftliklarini tezkor topish uchun xotirada Hash Map saqlash.
**Talablar:** O(1) qidiruv tezligi.
**Yechim (Go):**
```go
type HashIndex struct {
	index map[string]int64 // Kalit -> Diskdagi offset
}

func (h *HashIndex) GetOffset(key string) (int64, bool) {
	offset, ok := h.index[key]
	return offset, ok
}
```
**Tushuntirish:** Hash Index eng tezkor qidiruv usuli hisoblanadi, lekin u katta hajmdagi ma'lumotlar uchun ko'p RAM talab qilishi mumkin.

### Topshiriq #1218: B+Tree Split operatsiyasi
**Tavsif:** B+Tree tuguni to'lganda uni ikkiga bo'lish va daraxt muvozanatini saqlash.
**Talablar:** Daraxt balandligini bir xil saqlash.
**Yechim (Go):**
```go
func (n *Node) Split() (*Node, *Node) {
	mid := len(n.Keys) / 2
	// Tugunni ikkiga ajratish logikasi
	return left, right
}
```
**Tushuntirish:** Split operatsiyasi B+Tree'ning doimiy muvozanatda bo'lishini ta'minlaydi, bu esa qidiruv vaqtini barqarorlashtiradi.

### Topshiriq #1219: Bloom Filter (LSM-Tree optimizatsiyasi)
**Tavsif:** SSTable'da kalit yo'qligini tez aniqlash uchun Bloom Filter'dan foydalanish.
**Talablar:** Xotirani tejash va noto'g'ri musbat (false positive) natijalarni minimallashtirish.
**Yechim (Go):**
```go
import "github.com/bits-and-blooms/bloom/v3"

func CheckKey(filter *bloom.BloomFilter, key string) bool {
	return filter.Test([]byte(key))
}
```
**Tushuntirish:** Bloom Filter diskka murojaat qilishdan oldin kalitning mavjudligini tekshiradi, bu esa keraksiz disk o'qishlarini oldini oladi.

### Topshiriq #1220: Ma'lumotlar bazasi uchun Page Cache
**Tavsif:** Diskdagi sahifalarni xotirada vaqtincha saqlash orqali unumdorlikni oshirish.
**Talablar:** LRU (Least Recently Used) algoritmi bo'yicha eski sahifalarni chiqarib tashlash.
**Yechim (Go):**
```go
type PageCache struct {
	cache map[int64][]byte
	size  int
}

func (pc *PageCache) Get(pageID int64) []byte {
	return pc.cache[pageID]
}
```
**Tushuntirish:** LRU kesh tizimi eng ko'p ishlatiladigan ma'lumotlarni RAMda saqlab, disk I/O yuklamasini keskin kamaytiradi.

---

### Topshiriq #1221: B+Tree tugunini bo'lish (Split) algoritmi
**Tavsif:** B+Tree ma'lumotlar bazasida tugun to'lib qolganda, uni ikkiga ajratish va ota tugunni yangilash zarurati. Bu indekslash samaradorligini ta'minlaydi.
**Talablar:** O(log n) murakkablik, xotira xavfsizligi va pointerlar bilan ishlashda xatolik bo'lmasligi.
**Yechim (Go):**
```go
type Node struct {
    Keys     []int
    Children []*Node
    IsLeaf   bool
}

// SplitNode tugunni ikkiga ajratadi
func SplitNode(n *Node, mid int) (*Node, int) {
    newNode := &Node{
        Keys:   append([]int{}, n.Keys[mid+1:]...),
        IsLeaf: n.IsLeaf,
    }
    midKey := n.Keys[mid]
    n.Keys = n.Keys[:mid]
    return newNode, midKey
}
```
**Tushuntirish:** B+Tree balansini saqlash uchun `mid` elementni yuqoriga ko'tarish va qolgan qismlarni yangi tugunga o'tkazish eng samarali yondashuvdir.

### Topshiriq #1222: WAL (Write-Ahead Logging) uchun log yozish
**Tavsif:** Ma'lumotlar bazasi kutilmaganda o'chib qolganda ma'lumotlar yo'qolmasligi uchun operatsiyani diskka yozish.
**Talablar:** Atomik yozish, `fsync` orqali ma'lumotni diskka majburiy saqlash.
**Yechim (Go):**
```go
func WriteWAL(file *os.File, data []byte) error {
    _, err := file.Write(data)
    if err != nil { return err }
    return file.Sync() // Diskka fizik yozishni kafolatlaydi
}
```
**Tushuntirish:** `Sync()` funksiyasi operatsion tizim keshini chetlab o'tib, ma'lumotni diskka yozadi, bu esa ACID tamoyillaridan biri bo'lgan "Chidamlilik"ni ta'minlaydi.

### Topshiriq #1223: LSM-Tree MemTable qidiruvi
**Tavsif:** LSM-Tree'da ma'lumotlar avval xotiradagi MemTable'da saqlanadi. Qidiruvni tezlashtirish uchun samarali qidiruv algoritmi.
**Talablar:** O(log n) vaqt murakkabligi, `sort.Search` dan foydalanish.
**Yechim (Go):**
```go
func SearchMemTable(keys []string, target string) (int, bool) {
    idx := sort.Search(len(keys), func(i int) bool { return keys[i] >= target })
    if idx < len(keys) && keys[idx] == target {
        return idx, true
    }
    return -1, false
}
```
**Tushuntirish:** `sort.Search` ikkilik qidiruv (binary search) asosida ishlaydi, bu xotiradagi tartiblangan ma'lumotlar uchun eng tezkor usuldir.

### Topshiriq #1224: B+Tree'da ma'lumotlarni o'chirish (Underflow)
**Tavsif:** Tugundagi elementlar soni minimumdan kamayib ketganda, qo'shni tugunlardan element olish (rebalancing).
**Talablar:** Pointerlar xavfsizligi, rekursiv balanslash.
**Yechim (Go):**
```go
func BorrowFromSibling(left, right *Node, parent *Node, idx int) {
    // Chap tugundan o'ng tugunga element ko'chirish mantig'i
    right.Keys = append([]int{parent.Keys[idx]}, right.Keys...)
    parent.Keys[idx] = left.Keys[len(left.Keys)-1]
    left.Keys = left.Keys[:len(left.Keys)-1]
}
```
**Tushuntirish:** `BorrowFromSibling` daraxt balandligini o'zgartirmasdan, tugunlarni to'ldirish orqali daraxtni optimallashtiradi.

### Topshiriq #1225: LSM-Tree'da SSTable (Sorted String Table) yaratish
**Tavsif:** MemTable to'lganda uni diskka tartiblangan fayl (SSTable) sifatida yozish.
**Talablar:** I/O optimizatsiyasi, bufferlash.
**Yechim (Go):**
```go
func FlushToDisk(data map[string]string, filename string) error {
    f, _ := os.Create(filename)
    defer f.Close()
    writer := bufio.NewWriter(f)
    for k, v := range data {
        fmt.Fprintf(writer, "%s:%s\n", k, v)
    }
    return writer.Flush()
}
```
**Tushuntirish:** `bufio` dan foydalanish diskka yozish operatsiyalari sonini kamaytirib, yozish tezligini oshiradi.

### Topshiriq #1226: Indekslashda Bloom Filter qo'llash
**Tavsif:** LSM-Tree'da qidiruvni tezlashtirish uchun kalit mavjudligini oldindan tekshirish.
**Talablar:** Xotira tejamkorligi, bit-array operatsiyalari.
**Yechim (Go):**
```go
type BloomFilter struct { bits []bool; size int }

func (bf *BloomFilter) Add(key string) {
    hash := hashFunction(key) % bf.size
    bf.bits[hash] = true
}
```
**Tushuntirish:** Bloom Filter diskka murojaat qilishdan oldin kalitning yo'qligini 100% aniqlik bilan tasdiqlaydi, bu esa "disk read" operatsiyalarini keskin kamaytiradi.

### Topshiriq #1227: WAL faylini qayta tiklash (Recovery)
**Tavsif:** Tizim ishga tushganda WAL faylini o'qib, MemTable'ni qayta tiklash.
**Talablar:** Xatolarni boshqarish, ma'lumotlar yaxlitligi.
**Yechim (Go):**
```go
func Recover(filename string) ([]string, error) {
    data, _ := os.ReadFile(filename)
    lines := strings.Split(string(data), "\n")
    return lines, nil
}
```
**Tushuntirish:** Tizim qayta ishga tushganda oxirgi yozilmagan tranzaksiyalarni tiklash ma'lumotlar bazasi ishonchliligi uchun muhimdir.

### Topshiriq #1228: B+Tree'da diapazonli qidiruv (Range Scan)
**Tavsif:** B+Tree'da `SELECT * WHERE id BETWEEN 10 AND 20` kabi so'rovlarni bajarish.
**Talablar:** Leaf tugunlari o'rtasidagi bog'lanish (linked list) orqali o'tish.
**Yechim (Go):**
```go
func RangeScan(startNode *Node, min, max int) []int {
    var result []int
    curr := startNode
    for curr != nil {
        for _, k := range curr.Keys {
            if k >= min && k <= max { result = append(result, k) }
        }
        curr = curr.Next // Leaf tugunlar o'zaro bog'langan
    }
    return result
}
```
**Tushuntirish:** B+Tree barglari o'zaro bog'langan ro'yxat kabi ishlashi diapazonli qidiruvni O(k) murakkablikda bajarishga imkon beradi.

### Topshiriq #1229: LSM-Tree Compaction (Siqish)
**Tavsif:** Eski SSTable fayllarini birlashtirish va o'chirilgan ma'lumotlarni tozalash.
**Talablar:** Background goroutine, resurslarni boshqarish.
**Yechim (Go):**
```go
func Compact(tables []string) {
    go func() {
        // Fayllarni birlashtirish va dublikatlarni o'chirish mantig'i
    }()
}
```
**Tushuntirish:** Compaction jarayoni fon rejimida ishlashi kerak, chunki u katta hajmdagi I/O resurslarini talab qiladi va asosiy so'rovlarga ta'sir qilmasligi lozim.

### Topshiriq #1230: Indeks keshini boshqarish (LRU Cache)
**Tavsif:** Tez-tez ishlatiladigan indeks tugunlarini xotirada saqlash.
**Talablar:** O(1) murakkablik, `container/list` dan foydalanish.
**Yechim (Go):**
```go
type LRUCache struct {
    capacity int
    items    map[int]*list.Element
    list     *list.List
}
```
**Tushuntirish:** LRU (Least Recently Used) algoritmi eng kam ishlatilgan indekslarni xotiradan chiqarib, tezkor kirishni ta'minlaydi.

---

### Topshiriq #1231: LSM-Tree uchun MemTable implementatsiyasi
**Tavsif:** LSM-Tree arxitekturasida ma'lumotlar avval xotirada (MemTable) saqlanadi. Yuqori unumdorlik uchun thread-safe va tartiblangan tuzilma zarur.
**Talablar:** `sync.RWMutex` yordamida konkurentlikni boshqarish va `redblacktree` yoki `skiplist` algoritmidan foydalanish.
**Yechim (Go):**
```go
package main
import "sync"

// MemTable xotiradagi ma'lumotlar tuzilmasi
type MemTable struct {
	mu   sync.RWMutex
	data map[string]string // Oddiylik uchun map, realda Skiplist ishlatiladi
}

func (m *MemTable) Put(key, value string) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.data[key] = value
}

func (m *MemTable) Get(key string) (string, bool) {
	m.mu.RLock()
	defer m.mu.RUnlock()
	val, ok := m.data[key]
	return val, ok
}
```
**Tushuntirish:** `RWMutex` o'qish operatsiyalarini parallel bajarishga imkon beradi, bu esa o'qish ko'p bo'lgan tizimlarda unumdorlikni oshiradi.

---

### Topshiriq #1232: Write-Ahead Log (WAL) yozish mexanizmi
**Tavsif:** Tizim ishdan chiqqanda ma'lumotlar yo'qolmasligi uchun har bir yozish operatsiyasi diskka (WAL) yozilishi shart.
**Talablar:** `os.O_APPEND` va `fsync` orqali ma'lumotlarning diskka jismoniy yozilishini kafolatlash.
**Yechim (Go):**
```go
import "os"

func WriteWAL(entry string) error {
	f, _ := os.OpenFile("data.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	defer f.Close()
	_, err := f.WriteString(entry + "\n")
	return f.Sync() // Diskka jismoniy yozishni majburlash
}
```
**Tushuntirish:** `f.Sync()` chaqiruvi operatsion tizim keshini chetlab o'tib, ma'lumotni diskka yozadi, bu ma'lumotlar xavfsizligi uchun kritik ahamiyatga ega.

---

### Topshiriq #1233: B+Tree tugunini (Node) loyihalash
**Tavsif:** B+Tree indekslash tizimida ma'lumotlarni sahifalash (paging) uchun tugun tuzilmasini aniqlash.
**Talablar:** Tugun ichida kalitlar va bolalar (child pointers) massivini samarali boshqarish.
**Yechim (Go):**
```go
type Node struct {
	IsLeaf   bool
	Keys     []int
	Children []*Node
	Next     *Node // Barg tugunlar uchun bog'langan ro'yxat
}
```
**Tushuntirish:** `Next` ko'rsatkichi range-query (oraliq qidiruv) operatsiyalarini $O(k + \log n)$ vaqtda bajarishga imkon beradi.

---

### Topshiriq #1234: SSTable faylini diskka ketma-ket yozish
**Tavsif:** MemTable to'lganida uni diskka SSTable (Sorted String Table) sifatida saqlash.
**Talablar:** Ma'lumotlarni kalit bo'yicha tartiblab, diskka ketma-ket (sequential) yozish.
**Yechim (Go):**
```go
import ("encoding/json"; "os")

func FlushToSSTable(data map[string]string, filename string) error {
	file, _ := os.Create(filename)
	defer file.Close()
	return json.NewEncoder(file).Encode(data)
}
```
**Tushuntirish:** Ketma-ket yozish (sequential I/O) tasodifiy yozishga (random I/O) qaraganda diskda ancha tezroq ishlaydi.

---

### Topshiriq #1235: Bloom Filter yordamida qidiruvni optimallashtirish
**Tavsif:** SSTable ichida kalit yo'qligini tez aniqlash uchun Bloom Filterdan foydalanish.
**Talablar:** `hash` funksiyalaridan foydalanib, kalit mavjudligini ehtimoliy tekshirish.
**Yechim (Go):**
```go
type BloomFilter struct {
	bits []bool
	size int
}

func (b *BloomFilter) Add(key string) {
	// Hash funksiyalari orqali bitlarni belgilash
}
```
**Tushuntirish:** Bloom Filter diskka murojaat qilishdan oldin kalitning yo'qligini 100% aniqlik bilan tasdiqlaydi, bu esa I/O operatsiyalarini kamaytiradi.

---

### Topshiriq #1236: B+Tree qidiruv algoritmi
**Tavsif:** B+Tree daraxtida kalitni samarali izlash.
**Talablar:** Rekursiv yoki iterativ qidiruv, $O(\log n)$ vaqt murakkabligi.
**Yechim (Go):**
```go
func (n *Node) Search(key int) int {
	for i, k := range n.Keys {
		if key <= k {
			if n.IsLeaf { return n.Keys[i] }
			return n.Children[i].Search(key)
		}
	}
	return -1
}
```
**Tushuntirish:** B+Tree daraxti chuqurligi kam bo'lgani uchun diskdagi sahifalarni o'qish soni minimal bo'ladi.

---

### Topshiriq #1237: Kompaktlash (Compaction) jarayoni
**Tavsif:** LSM-Tree'da eski va yangi SSTable fayllarini birlashtirib, o'chirilgan ma'lumotlarni tozalash.
**Talablar:** Ikki faylni birlashtirishda kalitlar bo'yicha saralash (Merge Sort).
**Yechim (Go):**
```go
func Compact(files []string) {
	// Fayllarni o'qib, kalitlarni birlashtirish va yangi faylga yozish
}
```
**Tushuntirish:** Kompaktlash diskdagi bo'sh joyni bo'shatadi va o'qish unumdorligini oshiradi.

---

### Topshiriq #1238: Indekslashda "Tombstone" mexanizmi
**Tavsif:** Ma'lumotni o'chirishda uni darhol diskdan o'chirmasdan, "tombstone" (o'lim belgisi) qo'yish.
**Talablar:** O'chirilgan ma'lumotni qidiruv natijasida ko'rsatmaslik.
**Yechim (Go):**
```go
type Record struct {
	Value     string
	IsDeleted bool
}
```
**Tushuntirish:** Bu yondashuv yozish operatsiyasini tezlashtiradi, chunki diskda o'chirish qimmat jarayon hisoblanadi.

---

### Topshiriq #1239: B+Tree tugunini bo'lish (Split)
**Tavsif:** Tugun to'lib qolganda uni ikkiga bo'lish va ota tugunni yangilash.
**Talablar:** Daraxt muvozanatini saqlash.
**Yechim (Go):**
```go
func Split(n *Node) (*Node, *Node) {
	mid := len(n.Keys) / 2
	// Tugunni ikkiga ajratish logikasi
	return left, right
}
```
**Tushuntirish:** Split operatsiyasi daraxtning har doim muvozanatli (balanced) bo'lishini ta'minlaydi.

---

### Topshiriq #1240: Ma'lumotlar bazasi uchun Page Cache
**Tavsif:** Diskdagi sahifalarni xotirada keshlab turish.
**Talablar:** LRU (Least Recently Used) algoritmi yordamida keshni boshqarish.
**Yechim (Go):**
```go
type Cache struct {
	items map[int][]byte
	order []int
}
// LRU logikasi: eng eski foydalanilgan sahifani o'chirish
```
**Tushuntirish:** LRU kesh tez-tez murojaat qilinadigan ma'lumotlarni xotirada saqlab, disk I/O yuklamasini keskin kamaytiradi.

---

### Topshiriq #1241: WAL (Write-Ahead Logging) mexanizmini implementatsiya qilish
**Tavsif:** Ma'lumotlar bazasi tizimlarida kutilmagan o'chishlarda ma'lumotlar yo'qolmasligi uchun operatsiyalarni diskka yozishdan oldin log faylga yozish shart.
**Talablar:** `fsync` orqali ma'lumotlarning diskka jismoniy yozilishini ta'minlash, atomik yozish.
**Yechim (Go):**
```go
package main

import (
	"os"
)

// WAL log faylga ma'lumotni xavfsiz yozadi
func WriteToWAL(filename string, data []byte) error {
	f, err := os.OpenFile(filename, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}
	defer f.Close()

	_, err = f.Write(data)
	if err != nil {
		return err
	}
	// Ma'lumotni diskka majburiy yozish (fsync)
	return f.Sync() 
}
```
**Tushuntirish:** `f.Sync()` operatsiyasi operatsion tizim keshini chetlab o'tib, ma'lumotni jismoniy diskka yozadi, bu esa "durability" (ACID) uchun muhimdir.

---

### Topshiriq #1242: B+Tree tugunini (Node) loyihalash
**Tavsif:** B+Tree daraxti ma'lumotlarni qidirish tezligini $O(\log n)$ darajasida saqlaydi. Tugun tuzilmasini xotirada samarali joylashtirish kerak.
**Talablar:** Kalitlar va ko'rsatkichlar (pointers) uchun xotira samaradorligi.
**Yechim (Go):**
```go
type Node struct {
	IsLeaf   bool
	Keys     []int
	Children []*Node
	Values   [][]byte // Faqat barg tugunlar uchun
}
```
**Tushuntirish:** B+Tree'da barcha ma'lumotlar barglarda saqlanadi, ichki tugunlar esa faqat yo'naltiruvchi kalitlardir. Bu qidiruvni tezlashtiradi.

---

### Topshiriq #1243: LSM-Tree uchun MemTable yaratish
**Tavsif:** LSM-Tree yozish operatsiyalarini xotirada (RAM) to'playdi. MemTable to'lganida diskka (SSTable) ko'chirilishi kerak.
**Talablar:** Thread-safe yozish, `sync.RWMutex` dan foydalanish.
**Yechim (Go):**
```go
import "sync"

type MemTable struct {
	mu   sync.RWMutex
	data map[string][]byte
}

func (m *MemTable) Put(key string, value []byte) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.data[key] = value
}
```
**Tushuntirish:** MemTable yozish tezligini oshiradi, chunki u diskka emas, RAM'ga yozadi. Mutex esa konkurent yozishlarda ma'lumotlar buzilishini oldini oladi.

---

### Topshiriq #1244: SSTable (Sorted String Table) formatini loyihalash
**Tavsif:** MemTable diskka yozilganda, u tartiblangan bo'lishi kerak.
**Talablar:** Kalitlar bo'yicha saralangan fayl strukturasi.
**Yechim (Go):**
```go
type Entry struct {
	Key   string
	Value []byte
}

// SSTable yozish uchun saralangan ro'yxat talab qilinadi
func WriteSSTable(entries []Entry, path string) {
	// entries allaqachon sort qilingan bo'lishi shart
	// Faylga ketma-ket yozish (Sequential Write)
}
```
**Tushuntirish:** SSTable'ning asosiy kuchi - ketma-ket yozish (sequential I/O), bu HDD va SSD'larda tasodifiy yozishdan ancha tezdir.

---

### Topshiriq #1245: Bloom Filter yordamida qidiruvni optimallashtirish
**Tavsif:** LSM-Tree'da kalit yo'qligini aniqlash uchun barcha SSTable'larni tekshirish qimmat. Bloom Filter buni tezlashtiradi.
**Talablar:** Ehtimollik asosida kalit mavjudligini tekshirish.
**Yechim (Go):**
```go
// Oddiy Bloom Filter strukturasi
type BloomFilter struct {
	bitset []bool
	size   int
}
// Add va Contains metodlari bilan kalit mavjudligini tekshiradi
```
**Tushuntirish:** Bloom Filter "yo'q" degan javobni 100% aniqlik bilan beradi, bu esa keraksiz disk operatsiyalarini kamaytiradi.

---

### Topshiriq #1246: LSM-Tree Compaction jarayoni
**Tavsif:** Eski SSTable'larni birlashtirib, dublikatlarni o'chirish jarayoni.
**Talablar:** Merge-sort algoritmidan foydalanish.
**Yechim (Go):**
```go
func Compact(tables ...[]Entry) []Entry {
	// Merge-sort yordamida bir nechta saralangan ro'yxatni birlashtirish
	return mergedResult
}
```
**Tushuntirish:** Compaction diskdagi bo'sh joyni bo'shatadi va o'qish vaqtida qidiriladigan fayllar sonini kamaytiradi.

---

### Topshiriq #1247: B+Tree'da Range Query (Oraliq qidiruvi)
**Tavsif:** B+Tree barg tugunlari o'zaro bog'langan (linked list). Bu oraliq qidiruvni juda tez qiladi.
**Talablar:** `Next` ko'rsatkichidan foydalanish.
**Yechim (Go):**
```go
func RangeQuery(start, end int, root *Node) [][]byte {
	// Start kalitini topish va barg tugunlari bo'ylab yurish
	return results
}
```
**Tushuntirish:** B+Tree barglari bog'langan ro'yxat bo'lgani uchun, daraxtni qayta-qayta aylanib chiqish shart emas.

---

### Topshiriq #1248: Indekslash: Hash Index vs B+Tree
**Tavsif:** Qidiruv tezligi va xotira sarfi o'rtasidagi muvozanat.
**Talablar:** `map` asosidagi indeks va daraxt asosidagi indeksni taqqoslash.
**Yechim (Go):**
```go
// Hash Index (O(1) qidiruv)
type HashIndex map[string]int64 // Kalit -> Diskdagi ofset

// B+Tree (O(log n) qidiruv)
// ... daraxt strukturasi
```
**Tushuntirish:** Hash indekslar tez, lekin oraliq qidiruvni (range query) qo'llab-quvvatlamaydi.

---

### Topshiriq #1249: Buffer Pool menejeri
**Tavsif:** Diskdagi sahifalarni (pages) xotirada ushlab turish.
**Talablar:** LRU (Least Recently Used) algoritmi.
**Yechim (Go):**
```go
type BufferPool struct {
	pages map[int][]byte
	queue []int // LRU uchun
}
```
**Tushuntirish:** Buffer Pool diskka murojaatlarni kamaytiradi, eng ko'p ishlatiladigan sahifalarni RAM'da saqlaydi.

---

### Topshiriq #1250: WAL Replay (Crash Recovery)
**Tavsif:** Tizim o'chib qolganda, WAL fayldan ma'lumotlarni qayta tiklash.
**Talablar:** Faylni boshidan oxirigacha o'qib, MemTable'ni qayta to'ldirish.
**Yechim (Go):**
```go
func Recover(filename string, memTable *MemTable) {
	data, _ := os.ReadFile(filename)
	// Fayldagi har bir yozuvni o'qib, memTable.Put() qilish
}
```
**Tushuntirish:** Tizim qayta ishga tushganda, diskdagi oxirgi holatni tiklash uchun WAL yagona ishonchli manba hisoblanadi.