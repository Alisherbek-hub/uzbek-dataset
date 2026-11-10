# Khorazmiy AI: Java - Modul 25
## Mavzu: Ma'lumotlar bazasi ichki tuzilishi: LSM-Trees, B+Trees, WAL va Indekslash

### Topshiriq #1201: WAL (Write-Ahead Logging) mexanizmini implementatsiya qilish
**Tavsif:** Ma'lumotlar bazasida kutilmagan o'chishlar (crash) yuz berganda ma'lumotlar yaxlitligini saqlash uchun operatsiyalarni diskka yozishdan oldin log faylga yozish zarurati.
**Talablar:** Log faylga yozish atomar bo'lishi va `flush()` operatsiyasi orqali diskka majburiy yozilishi kerak.
**Yechim (Java):**
```java
import java.io.*;

public class WriteAheadLog {
    private final PrintWriter writer;

    public WriteAheadLog(String filePath) throws IOException {
        // Append rejimida ochish
        this.writer = new PrintWriter(new BufferedWriter(new FileWriter(filePath, true)));
    }

    public synchronized void log(String operation) {
        writer.println(System.currentTimeMillis() + ": " + operation);
        writer.flush(); // Diskka majburiy yozish
    }
}
```
**Tushuntirish:** `flush()` metodi operatsion tizim buferini tozalab, ma'lumotni fizik diskka o'tkazishni ta'minlaydi, bu esa "durability" (ACID) uchun muhim.

---

### Topshiriq #1202: B+Tree tugunini (Node) loyihalash
**Tavsif:** B+Tree ma'lumotlar bazasi indekslarida ma'lumotlarni tartibli saqlash va qidiruvni O(log n) vaqtda bajarish uchun tugun tuzilmasi.
**Talablar:** Tugun ichida kalitlar va bolalar (child) ko'rsatkichlari massiv ko'rinishida bo'lishi kerak.
**Yechim (Java):**
```java
public class BPlusNode {
    int[] keys;
    BPlusNode[] children;
    boolean isLeaf;
    int n; // Hozirgi kalitlar soni

    public BPlusNode(int degree, boolean isLeaf) {
        this.keys = new int[2 * degree - 1];
        this.children = new BPlusNode[2 * degree];
        this.isLeaf = isLeaf;
        this.n = 0;
    }
}
```
**Tushuntirish:** B+Tree'da faqat barg (leaf) tugunlar ma'lumotni saqlaydi, ichki tugunlar esa faqat yo'naltiruvchi kalitlardir. Bu diskdagi qidiruvni optimallashtiradi.

---

### Topshiriq #1203: LSM-Tree uchun MemTable (In-memory buffer)
**Tavsif:** LSM-Tree'da yozish operatsiyalarini tezlashtirish uchun ma'lumotlarni avval xotirada (RAM) tartibli saqlash.
**Talablar:** `TreeMap` yordamida kalitlar doimiy tartibda saqlanishi va xotira chegarasi oshganda diskka "flush" qilinishi kerak.
**Yechim (Java):**
```java
import java.util.TreeMap;

public class MemTable {
    private final TreeMap<String, String> buffer = new TreeMap<>();
    private final int MAX_SIZE = 1024; // 1KB limit

    public synchronized void put(String key, String value) {
        buffer.put(key, value);
        if (buffer.size() >= MAX_SIZE) {
            flushToDisk();
        }
    }

    private void flushToDisk() {
        // SSTable fayliga yozish logikasi shu yerda bo'ladi
        buffer.clear();
    }
}
```
**Tushuntirish:** `TreeMap` qizil-qora daraxt (Red-Black Tree) asosida ishlaydi, bu esa yozish va qidirishni O(log n) vaqtda bajarish imkonini beradi.

---

### Topshiriq #1204: B+Tree'da qidiruv algoritmi
**Tavsif:** Indekslangan ma'lumotlar bazasidan kalit bo'yicha qiymatni samarali topish.
**Talablar:** Rekursiv qidiruv va tugunlar bo'ylab harakatlanish.
**Yechim (Java):**
```java
public BPlusNode search(BPlusNode node, int key) {
    int i = 0;
    while (i < node.n && key > node.keys[i]) i++;
    
    if (i < node.n && node.keys[i] == key) return node;
    if (node.isLeaf) return null;
    
    return search(node.children[i], key);
}
```
**Tushuntirish:** Bu yondashuv daraxt balandligini minimal darajada ushlab turadi, natijada diskdan o'qish operatsiyalari kamayadi.

---

### Topshiriq #1205: SSTable (Sorted String Table) formatini yaratish
**Tavsif:** LSM-Tree'ning diskdagi qismi bo'lgan SSTable'ni o'qish uchun formatlash.
**Talablar:** Fayl tartiblangan bo'lishi va qidiruvni tezlashtirish uchun "Index Block" bo'lishi kerak.
**Yechim (Java):**
```java
import java.io.*;

public class SSTableWriter {
    public void writeSortedData(TreeMap<String, String> data, String fileName) throws IOException {
        try (DataOutputStream out = new DataOutputStream(new FileOutputStream(fileName))) {
            for (var entry : data.entrySet()) {
                out.writeUTF(entry.getKey());
                out.writeUTF(entry.getValue());
            }
        }
    }
}
```
**Tushuntirish:** Ma'lumotlar tartiblangan holda yozilgani uchun, keyinchalik Binary Search orqali diskdan tezkor qidirish mumkin.

---

### Topshiriq #1206: Bloom Filter (Qidiruvni optimallashtirish)
**Tavsif:** LSM-Tree'da qidiruv vaqtida kerakli kalit qaysi SSTable'da borligini tekshirish (diskka murojaatni kamaytirish).
**Talablar:** Ehtimollik asosida ishlaydigan bit-massiv tuzilmasi.
**Yechim (Java):**
```java
import java.util.BitSet;

public class BloomFilter {
    private final BitSet bits = new BitSet(1000);

    public void add(String key) {
        bits.set(key.hashCode() % 1000);
    }

    public boolean mightContain(String key) {
        return bits.get(key.hashCode() % 1000);
    }
}
```
**Tushuntirish:** Bloom Filter diskka murojaat qilishdan oldin kalitning yo'qligini aniq tasdiqlaydi, bu esa "false positive" (yolg'on musbat) ehtimolini kamaytiradi.

---

### Topshiriq #1207: B+Tree'da tugunni bo'lish (Split)
**Tavsif:** Tugun to'lib qolganda daraxt muvozanatini saqlash uchun uni ikkiga ajratish.
**Talablar:** O'rta elementni yuqori darajadagi tugunga ko'tarish.
**Yechim (Java):**
```java
public void splitChild(BPlusNode parent, int i, BPlusNode fullNode) {
    BPlusNode newNode = new BPlusNode(3, fullNode.isLeaf);
    // Yarim ma'lumotni yangi tugunga ko'chirish logikasi
    // Parent tugunni yangilash
}
```
**Tushuntirish:** Split operatsiyasi daraxtning "balanslangan" bo'lishini ta'minlaydi, bu esa har qanday qidiruvning barqaror O(log n) bo'lishiga kafolat beradi.

---

### Topshiriq #1208: LSM-Tree Compaction (Siqish)
**Tavsif:** Bir nechta SSTable fayllarini birlashtirib, eskirgan ma'lumotlarni o'chirish va disk hajmini optimallashtirish.
**Tavsif:** Ikki tartiblangan faylni birlashtiruvchi (Merge) algoritm.
**Yechim (Java):**
```java
public void mergeSSTables(String file1, String file2, String outputFile) {
    // Ikki faylni o'qib, kalitlar bo'yicha tartiblab yangi faylga yozish
    // Merge Sort algoritmining "merge" qismi kabi ishlaydi
}
```
**Tushuntirish:** Compaction jarayoni ma'lumotlar bazasining o'qish tezligini oshiradi va diskdagi "fragmentatsiya"ni yo'qotadi.

---

### Topshiriq #1209: Indeks fayli (Sparse Index)
**Tavsif:** Katta fayllarni o'qishda har N-chi yozuv uchun indeks saqlash.
**Talablar:** Indeks xotirada saqlanib, diskdagi ofsetni (offset) ko'rsatishi kerak.
**Yechim (Java):**
```java
import java.util.TreeMap;

public class SparseIndex {
    private final TreeMap<String, Long> index = new TreeMap<>();

    public void addEntry(String key, long offset) {
        index.put(key, offset);
    }

    public long getOffset(String key) {
        return index.floorEntry(key).getValue();
    }
}
```
**Tushuntirish:** Sparse index butun faylni xotirada saqlamasdan, kerakli ma'lumot joylashgan qismga tezda "sakrash" (seek) imkonini beradi.

---

### Topshiriq #1210: ACID tranzaksiya menejeri (Skelet)
**Tavsif:** Bir nechta yozish operatsiyalarini bitta tranzaksiya sifatida bajarish.
**Talablar:** `commit` va `rollback` funksionalligi.
**Yechim (Java):**
```java
public class TransactionManager {
    public void executeTransaction(Runnable task) {
        try {
            // 1. Log yozish
            // 2. Taskni bajarish
            // 3. Commit (WAL-ni tozalash)
        } catch (Exception e) {
            // Rollback (Log orqali eski holatga qaytish)
        }
    }
}
```
**Tushuntirish:** Tranzaksiya menejeri ma'lumotlar bazasining izchilligini (Consistency) ta'minlaydi, xatolik yuz berganda tizimni xavfsiz holatga qaytaradi.

---

### Topshiriq #1211: B+Tree tugunini bo'lish (Split) mexanizmi
**Tavsif:** B+Tree ma'lumotlar bazasi indekslarida tugun to'lib qolganda, uni ikkiga ajratish va ota tugunni yangilash operatsiyasi. Bu ma'lumotlar bazasining muvozanatli ishlashini ta'minlaydi.
**Talablar:** O(log n) murakkablik, xotira xavfsizligi va tugunlarning to'g'ri bog'lanishi.
**Yechim (Java):**
```java
public class BPlusNode {
    int[] keys;
    BPlusNode[] children;
    int n; // Kalitlar soni
    boolean isLeaf;

    // Tugunni o'rtasidan bo'lish va yangi tugun qaytarish
    public BPlusNode splitChild(int index, BPlusNode fullNode) {
        BPlusNode newNode = new BPlusNode();
        newNode.isLeaf = fullNode.isLeaf;
        int mid = fullNode.n / 2;
        
        // Yarim ma'lumotlarni yangi tugunga ko'chirish
        for (int i = 0; i < mid; i++) {
            newNode.keys[i] = fullNode.keys[i + mid + 1];
        }
        fullNode.n = mid;
        return newNode;
    }
}
```
**Tushuntirish:** B+Tree balansini saqlash uchun "split" operatsiyasi eng muhim qismdir. Bu yondashuv xotirani samarali boshqarish va qidiruv tezligini barqaror saqlash uchun tanlangan.

---

### Topshiriq #1212: WAL (Write-Ahead Logging) tizimini simulyatsiya qilish
**Tavsif:** Ma'lumotlar bazasi ishdan chiqqanda (crash) ma'lumotlar yo'qolmasligi uchun operatsiyani diskka yozishdan oldin log faylga yozish.
**Talablar:** I/O operatsiyalarini minimallashtirish va atomiklikni ta'minlash.
**Yechim (Java):**
```java
import java.io.*;

public class WALManager {
    private PrintWriter logWriter;

    public WALManager(String path) throws IOException {
        this.logWriter = new PrintWriter(new FileWriter(path, true));
    }

    public synchronized void logOperation(String operation) {
        logWriter.println(System.currentTimeMillis() + ": " + operation);
        logWriter.flush(); // Diskka yozishni majburiy qilish
    }
}
```
**Tushuntirish:** `flush()` metodi ma'lumotlarning operativ xotiradan diskka o'tishini kafolatlaydi, bu esa ACID tamoyillaridan biri bo'lgan "Durability"ni ta'minlaydi.

---

### Topshiriq #1213: LSM-Tree MemTable qidiruvi
**Tavsif:** LSM-Tree tarkibidagi MemTable (xotiradagi jadval)da ma'lumotlarni tezkor qidirish.
**Talablar:** O(log n) qidiruv tezligi va thread-safe (xavfsiz) kirish.
**Yechim (Java):**
```java
import java.util.concurrent.ConcurrentSkipListMap;

public class MemTable {
    private ConcurrentSkipListMap<String, String> table = new ConcurrentSkipListMap<>();

    public void put(String key, String value) {
        table.put(key, value);
    }

    public String get(String key) {
        return table.get(key); // SkipList yordamida tezkor qidiruv
    }
}
```
**Tushuntirish:** `ConcurrentSkipListMap` LSM-Tree uchun ideal, chunki u ham qidiruvda, ham yozishda yuqori unumdorlikni ta'minlaydi va qulflarsiz (lock-free) ishlaydi.

---

### Topshiriq #1214: B+Tree diapazonli qidiruv (Range Query)
**Tavsif:** B+Tree barg tugunlari o'zaro bog'langanligi sababli, ma'lum oraliqdagi kalitlarni samarali olish.
**Talablar:** Iterator pattern va xotira samaradorligi.
**Yechim (Java):**
```java
public void rangeSearch(int start, int end, BPlusNode node) {
    // Barg tugunigacha yetib borish
    while (!node.isLeaf) node = node.children[0];
    
    // Barglar bo'ylab ketma-ket yurish
    while (node != null) {
        for (int key : node.keys) {
            if (key >= start && key <= end) System.out.println(key);
        }
        node = node.next; // Keyingi bargga o'tish
    }
}
```
**Tushuntirish:** B+Tree ning asosiy afzalligi - barg tugunlarining bog'langan ro'yxat kabi ulanishi. Bu diapazonli so'rovlarni O(k) vaqtda bajarish imkonini beradi.

---

### Topshiriq #1215: LSM-Tree Compaction (Siqish) jarayoni
**Tavsif:** LSM-Tree da eski va yangi ma'lumotlarni birlashtirib, dublikatlarni o'chirish jarayoni.
**Talablar:** Disk I/O ni optimallashtirish va xotira oqishini oldini olish.
**Yechim (Java):**
```java
public void compact(Map<String, String> sstable1, Map<String, String> sstable2) {
    // Ikki SSTable ni birlashtirib, oxirgi qiymatni saqlash
    Map<String, String> merged = new TreeMap<>(sstable1);
    merged.putAll(sstable2);
    // Natijani yangi faylga yozish...
}
```
**Tushuntirish:** Compaction jarayoni LSM-Tree unumdorligini saqlab qolish uchun zarur. `TreeMap` yordamida kalitlar tartiblanadi va dublikatlar avtomatik tozalanadi.

---

### Topshiriq #1216: Indekslashda Bloom Filter qo'llash
**Tavsif:** Ma'lumotlar bazasida kalit mavjudligini tezkor tekshirish uchun Bloom Filterdan foydalanish.
**Talablar:** Xotira tejamkorligi va noto'g'ri musbat (false positive) natijalarni minimallashtirish.
**Yechim (Java):**
```java
import java.util.BitSet;

public class BloomFilter {
    private BitSet bits = new BitSet(1000);

    public void add(String key) {
        bits.set(key.hashCode() % 1000);
    }

    public boolean mightContain(String key) {
        return bits.get(key.hashCode() % 1000);
    }
}
```
**Tushuntirish:** Bloom Filter diskka murojaat qilishdan oldin kalitning yo'qligini aniqlash orqali qidiruv tezligini keskin oshiradi.

---

### Topshiriq #1217: B+Tree tugunini o'chirish (Deletion)
**Tavsif:** B+Tree dan kalitni o'chirish va tugunlar muvozanatini qayta tiklash (Rebalancing).
**Talablar:** O'chirishdan keyin daraxt xususiyatlarini saqlash.
**Yechim (Java):**
```java
public void delete(int key) {
    // O'chirish logikasi: tugun to'ldirilganlik darajasini tekshirish
    // Agar tugun yarimidan kam bo'lsa, qo'shni tugun bilan birlashtirish (Merge)
    if (needsRebalance()) {
        mergeWithSibling();
    }
}
```
**Tushuntirish:** O'chirish operatsiyasi qo'shishdan murakkabroq, chunki u daraxtning strukturaviy yaxlitligini saqlash uchun "Merge" yoki "Redistribution"ni talab qiladi.

---

### Topshiriq #1218: Diskdagi ma'lumotlarni sahifalash (Paging)
**Tavsif:** Ma'lumotlar bazasini diskda sahifalarga (pages) bo'lib saqlash.
**Talablar:** Sahifa hajmini belgilash va to'g'ridan-to'g'ri manzilga murojaat.
**Yechim (Java):**
```java
public class PageManager {
    private static final int PAGE_SIZE = 4096; // 4KB sahifa

    public byte[] readPage(int pageId) throws IOException {
        RandomAccessFile file = new RandomAccessFile("db.dat", "r");
        file.seek((long) pageId * PAGE_SIZE);
        byte[] page = new byte[PAGE_SIZE];
        file.read(page);
        return page;
    }
}
```
**Tushuntirish:** `RandomAccessFile` yordamida ma'lumotlarga sahifa bo'yicha murojaat qilish, butun faylni o'qishdan ko'ra ancha tezroq va samaraliroqdir.

---

### Topshiriq #1219: LSM-Tree SSTable formatini yaratish
**Tavsif:** MemTable diskka yozilganda SSTable (Sorted String Table) formatiga o'tkazish.
**Talablar:** Ma'lumotlarni tartiblangan holda saqlash.
**Yechim (Java):**
```java
public void flushToSSTable(Map<String, String> memTable) throws IOException {
    try (BufferedWriter writer = new BufferedWriter(new FileWriter("sstable.db"))) {
        for (Map.Entry<String, String> entry : memTable.entrySet()) {
            writer.write(entry.getKey() + ":" + entry.getValue());
            writer.newLine();
        }
    }
}
```
**Tushuntirish:** SSTable - LSM-Tree ning asosi. Tartiblangan yozuvlar qidiruvni diskda `Binary Search` yordamida amalga oshirish imkonini beradi.

---

### Topshiriq #1220: Indeksli qidiruvda "Covering Index" optimizatsiyasi
**Tavsif:** So'rov uchun kerakli barcha ma'lumotlar indeksning o'zida bo'lsa, asosiy jadvalga murojaat qilmaslik.
**Talablar:** Indeks strukturasi va ma'lumotlar bazasi so'rovini optimallashtirish.
**Yechim (Java):**
```java
public class IndexOptimizer {
    // Agar indeksda kerakli qiymat bo'lsa, diskdan butun qatorni o'qimaymiz
    public String getFromIndexOnly(String key, Map<String, String> index) {
        if (index.containsKey(key)) {
            return index.get(key); // Covering Index
        }
        return null;
    }
}
```
**Tushuntirish:** "Covering Index" ma'lumotlar bazasi unumdorligini oshirishning eng kuchli usullaridan biridir, chunki u diskdagi "Random I/O" ni butunlay yo'q qiladi.

---

### Topshiriq #1221: B+ Tree tugunini qidirish algoritmi
**Tavsif:** B+ Tree ma'lumotlar bazasi indekslarining asosi hisoblanadi. Diskdagi ma'lumotlarni samarali topish uchun tugun ichidagi kalitlarni binar qidirish orqali aniqlash kerak.
**Talablar:** O(log n) murakkablik, xotira xavfsizligi va null-pointer tekshiruvi.
**Yechim (Java):**
```java
public class BPlusNode {
    private long[] keys; // Tugundagi kalitlar
    
    public int findKeyIndex(long key) {
        int low = 0, high = keys.length - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (keys[mid] == key) return mid;
            else if (keys[mid] < key) low = mid + 1;
            else high = mid - 1;
        }
        return low; // Keyingi tugunga o'tish uchun o'rnini qaytaradi
    }
}
```
**Tushuntirish:** Binar qidiruv (Binary Search) diskdagi o'qish operatsiyalarini minimallashtirish uchun eng samarali usuldir.

### Topshiriq #1222: Write-Ahead Logging (WAL) mexanizmi
**Tavsif:** Ma'lumotlar bazasi kutilmaganda o'chib qolganda ma'lumotlar yaxlitligini saqlash uchun operatsiyani avval log faylga yozish shart.
**Talablar:** I/O operatsiyalarini buferlash va "flush" qilish.
**Yechim (Java):**
```java
import java.io.*;

public class WALManager {
    private BufferedWriter writer;

    public synchronized void log(String operation) throws IOException {
        writer.write(System.currentTimeMillis() + ":" + operation);
        writer.newLine();
        writer.flush(); // Ma'lumotni diskka majburiy yozish
    }
}
```
**Tushuntirish:** `flush()` metodi ma'lumotlarning operativ xotirada qolib ketmasligini va diskka yozilishini kafolatlaydi.

### Topshiriq #1223: LSM-Tree MemTable to'lib qolganda flush qilish
**Tavsif:** LSM-Tree'da ma'lumotlar avval xotiradagi MemTable'ga yoziladi. U to'lgach, diskdagi SSTable'ga o'tkazilishi kerak.
**Talablar:** Thread-safe yondashuv va ma'lumotlar ketma-ketligini saqlash.
**Yechim (Java):**
```java
import java.util.TreeMap;

public class MemTable {
    private TreeMap<String, String> data = new TreeMap<>();
    private final int MAX_SIZE = 1000;

    public synchronized void put(String key, String value) {
        if (data.size() >= MAX_SIZE) {
            flushToSSTable();
        }
        data.put(key, value);
    }

    private void flushToSSTable() {
        // Diskka yozish logikasi
        data.clear();
    }
}
```
**Tushuntirish:** `TreeMap` kalitlarni avtomatik tartiblaydi, bu esa SSTable yaratishda diskdagi yozish tezligini oshiradi.

### Topshiriq #1224: B+ Tree tugunini bo'lish (Split)
**Tavsif:** Tugun to'lib qolganda, uni ikkiga bo'lish va o'rta elementni ota tugunga ko'tarish kerak.
**Talablar:** Strukturaviy yaxlitlik va xotira ajratish samaradorligi.
**Yechim (Java):**
```java
public class BPlusTreeSplitter {
    public void splitNode(Node node) {
        int mid = node.size() / 2;
        Node newNode = new Node();
        // O'rta elementdan keyingilarni yangi tugunga ko'chirish
        for (int i = mid; i < node.size(); i++) {
            newNode.add(node.getKey(i));
        }
        node.truncate(mid);
    }
}
```
**Tushuntirish:** Tugunni bo'lish daraxt muvozanatini (balance) saqlaydi, bu esa qidiruv tezligini barqaror qiladi.

### Topshiriq #1225: LSM-Tree Compaction (Siqish)
**Tavsif:** SSTable fayllari ko'payib ketganda, ularni birlashtirib, eskirgan ma'lumotlarni o'chirish jarayoni.
**Talablar:** O(n) murakkablik va xotirani tejash.
**Yechim (Java):**
```java
public void compact(List<SSTable> tables) {
    // Merge-sort algoritmi yordamida fayllarni birlashtirish
    // Eskirgan kalitlarni (tombstones) olib tashlash
}
```
**Tushuntirish:** Compaction o'qish tezligini oshiradi, chunki qidiruv kamroq fayllar ichida amalga oshiriladi.

### Topshiriq #1226: Indekslashda "Tombstone" belgisi
**Tavsif:** LSM-Tree'da o'chirilgan ma'lumotlarni darhol diskdan o'chirish qimmatga tushadi. Buning o'rniga "tombstone" (o'lim belgisi) qo'yiladi.
**Talablar:** O'chirilganlik holatini aniqlash va filtrlash.
**Yechim (Java):**
```java
public class Record {
    private String value;
    private boolean isDeleted; // Tombstone belgisi

    public boolean isVisible() {
        return !isDeleted;
    }
}
```
**Tushuntirish:** Bu yondashuv yozish operatsiyasini tezlashtiradi, o'chirish esa keyingi "compaction" jarayonida amalga oshiriladi.

### Topshiriq #1227: B+ Tree diapazonli qidiruv (Range Query)
**Tavsif:** Ma'lum bir oraliqdagi (masalan, 100 dan 200 gacha) kalitlarni tezkor topish.
**Talablar:** Leaf tugunlaridagi bog'langan ro'yxatdan foydalanish.
**Yechim (Java):**
```java
public void rangeQuery(long start, long end) {
    Node current = findLeaf(start);
    while (current != null && current.getMinKey() <= end) {
        for (long key : current.getKeys()) {
            if (key >= start && key <= end) process(key);
        }
        current = current.getNext(); // Keyingi barg tuguniga o'tish
    }
}
```
**Tushuntirish:** Barg tugunlarini o'zaro bog'lash (linked list) diapazonli qidiruvni chiziqli vaqtda bajarish imkonini beradi.

### Topshiriq #1228: WAL Recovery (Qayta tiklash)
**Tavsif:** Tizim ishdan chiqqandan so'ng, WAL faylini o'qib, MemTable'ni qayta tiklash.
**Talablar:** Faylni oxirigacha o'qish va xatolarni boshqarish.
**Yechim (Java):**
```java
public void recover(File walFile) throws IOException {
    try (BufferedReader reader = new BufferedReader(new FileReader(walFile))) {
        String line;
        while ((line = reader.readLine()) != null) {
            applyToMemTable(line);
        }
    }
}
```
**Tushuntirish:** WAL fayli ketma-ket yozilgani uchun uni o'qish juda tez amalga oshiriladi.

### Topshiriq #1229: Bloom Filter (Indekslash optimizatsiyasi)
**Tavsif:** SSTable'da kalit borligini tekshirishdan oldin Bloom Filter orqali tekshirib, diskdan keraksiz o'qishni oldini olish.
**Talablar:** Xesh funksiyalaridan samarali foydalanish.
**Yechim (Java):**
```java
public class BloomFilter {
    private BitSet bits = new BitSet(1024);

    public void add(String key) {
        bits.set(key.hashCode() % 1024);
    }

    public boolean mightContain(String key) {
        return bits.get(key.hashCode() % 1024);
    }
}
```
**Tushuntirish:** Bloom Filter "ehtimoliy" javob beradi, bu esa disk I/O operatsiyalarini 90% gacha kamaytirishi mumkin.

### Topshiriq #1230: B+ Tree Ota tugunni yangilash
**Tavsif:** Barg tugunidagi o'zgarishlardan so'ng, ota tugundagi indeks kalitlarini yangilash.
**Talablar:** Rekursiv yangilash va xatolarni oldini olish.
**Yechim (Java):**
```java
public void updateParent(Node node, long oldKey, long newKey) {
    if (node.isRoot()) return;
    Node parent = node.getParent();
    parent.replaceKey(oldKey, newKey);
    if (parent.needsRebalance()) updateParent(parent, oldKey, newKey);
}
```
**Tushuntirish:** Indeks tuzilmasini yangilash daraxtning izchilligini (consistency) ta'minlaydi.

---

### Topshiriq #1231: B+Tree tugunida kalitlarni qidirish (Binary Search)
**Tavsif:** B+Tree ma'lumotlar bazasi indekslarida tugun ichidagi kalitlarni tezkor topish kerak. Chiziqli qidiruv sekin, shuning uchun ikkilik qidiruv (binary search) talab etiladi.
**Talablar:** O(log n) murakkablik, xotira xavfsizligi.
**Yechim (Java):**
```java
public class BTreeSearch {
    // Tugun ichidagi kalitlar massividan maqsadli qiymatni topish
    public static int findKeyIndex(int[] keys, int target) {
        int low = 0, high = keys.length - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (keys[mid] == target) return mid;
            if (keys[mid] < target) low = mid + 1;
            else high = mid - 1;
        }
        return low; // Insert pozitsiyasini qaytaradi
    }
}
```
**Tushuntirish:** B+Tree tugunlari saralangan bo'lgani uchun ikkilik qidiruv eng samarali usuldir. `low` qiymatini qaytarish, yangi elementni qo'shishda `shift` operatsiyasini osonlashtiradi.

---

### Topshiriq #1232: WAL (Write-Ahead Log) yozuvini amalga oshirish
**Tavsif:** Ma'lumotlar bazasi kutilmaganda o'chib qolsa, ma'lumotlar yo'qolmasligi uchun har bir operatsiyani diskka yozib borish (WAL).
**Talablar:** I/O operatsiyalarini minimallashtirish, xatolarga chidamlilik.
**Yechim (Java):**
```java
import java.io.*;

public class WALManager {
    private PrintWriter logWriter;
    public WALManager(String filePath) throws IOException {
        this.logWriter = new PrintWriter(new FileWriter(filePath, true));
    }
    // Operatsiyani jurnalga yozish
    public synchronized void log(String operation) {
        logWriter.println(System.currentTimeMillis() + ":" + operation);
        logWriter.flush(); // Diskka majburiy yozish
    }
}
```
**Tushuntirish:** `flush()` metodi ma'lumotlarning operativ xotiradan diskka o'tishini kafolatlaydi, bu esa ACID tamoyillaridan biri bo'lgan "Durability"ni ta'minlaydi.

---

### Topshiriq #1233: LSM-Tree MemTable (SkipList) tuzilmasi
**Tavsif:** LSM-Tree'da ma'lumotlar avval xotirada (MemTable) saqlanadi. Tezkor qidiruv va qo'shish uchun SkipList kerak.
**Talablar:** O(log n) o'rtacha murakkablik.
**Yechim (Java):**
```java
import java.util.concurrent.ConcurrentSkipListMap;

public class MemTable {
    // Kalit-qiymat juftligini xotirada saqlash
    private final ConcurrentSkipListMap<String, String> table = new ConcurrentSkipListMap<>();

    public void put(String key, String value) {
        table.put(key, value);
    }
    public String get(String key) {
        return table.get(key);
    }
}
```
**Tavsif:** `ConcurrentSkipListMap` thread-safe bo'lib, LSM-Tree'ning yozish tezligini oshiradi va qulflarsiz (lock-free) o'qish imkonini beradi.

---

### Topshiriq #1234: B+Tree tugunini bo'lish (Node Split)
**Tavsif:** B+Tree tuguni to'lib qolganda, uni ikkiga ajratish va o'rta elementni yuqori darajaga ko'tarish kerak.
**Talablar:** Strukturaviy yaxlitlikni saqlash.
**Yechim (Java):**
```java
public class BTreeSplitter {
    public void splitNode(Node parent, Node child) {
        int mid = child.keys.length / 2;
        Node newNode = new Node();
        // O'rta elementdan keyingilarni yangi tugunga ko'chirish
        System.arraycopy(child.keys, mid + 1, newNode.keys, 0, mid);
        parent.insertKey(child.keys[mid]);
        parent.addChild(newNode);
    }
}
```
**Tushuntirish:** Bu jarayon daraxtning muvozanatini (balanced) saqlaydi, bu esa qidiruv vaqtini doimiy ravishda logarifmik darajada ushlab turadi.

---

### Topshiriq #1235: LSM-Tree Compaction (SSTable birlashtirish)
**Tavsif:** Eski SSTable fayllarini birlashtirib, o'chirilgan yoki eskirgan ma'lumotlarni tozalash.
**Talablar:** Disk I/O ni optimallashtirish.
**Yechim (Java):**
```java
public class CompactionEngine {
    public void compact(SSTable old1, SSTable old2) {
        // Ikkita saralangan faylni merge-sort kabi birlashtirish
        // Faqat eng yangi versiyadagi ma'lumotlarni saqlash
        System.out.println("SSTable fayllari birlashtirilmoqda...");
    }
}
```
**Tushuntirish:** Compaction LSM-Tree'ning "o'qish kuchaytirgichi" (read amplification) muammosini hal qiladi va disk bo'shlig'ini qayta tiklaydi.

---

### Topshiriq #1236: Indekslash: Hash Index implementatsiyasi
**Tavsif:** Kalit bo'yicha O(1) vaqtda ma'lumot topish uchun Hash Index yaratish.
**Talablar:** To'qnashuvlarni (collision) boshqarish.
**Yechim (Java):**
```java
import java.util.HashMap;

public class HashIndex {
    private HashMap<Integer, Long> index = new HashMap<>(); // Kalit -> Disk offset

    public void addEntry(int key, long offset) {
        index.put(key, offset);
    }
    public long getOffset(int key) {
        return index.getOrDefault(key, -1L);
    }
}
```
**Tushuntirish:** Hash Index juda tez, lekin diapazonli qidiruv (range query) uchun yaroqsiz. Shuning uchun u faqat aniq kalit qidiruvlarida qo'llaniladi.

---

### Topshiriq #1237: B+Tree Leaf Node Linker
**Tavsif:** B+Tree barg tugunlarini o'zaro bog'lash (linked list), bu diapazonli qidiruvni (range scan) tezlashtiradi.
**Talablar:** Pointerlar orqali bog'lanish.
**Yechim (Java):**
```java
class Node {
    Node next; // Keyingi barg tuguniga havola
    int[] keys;
}
public class RangeScanner {
    public void scan(Node startNode) {
        Node current = startNode;
        while (current != null) {
            // Bargdagi barcha kalitlarni o'qish
            current = current.next;
        }
    }
}
```
**Tushuntirish:** Barg tugunlarining bog'langan ro'yxati `SELECT * FROM table WHERE id BETWEEN 10 AND 50` kabi so'rovlarni daraxtni qayta-qayta aylanmasdan bajarishga imkon beradi.

---

### Topshiriq #1238: Ma'lumotlar bazasi "Buffer Pool" boshqaruvi
**Tavsif:** Diskdagi sahifalarni (pages) xotirada saqlash uchun LRU (Least Recently Used) mexanizmi.
**Talablar:** Xotira limitini nazorat qilish.
**Yechim (Java):**
```java
import java.util.LinkedHashMap;
import java.util.Map;

public class BufferPool<K, V> extends LinkedHashMap<K, V> {
    private final int capacity;
    public BufferPool(int capacity) {
        super(capacity, 0.75f, true);
        this.capacity = capacity;
    }
    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > capacity;
    }
}
```
**Tushuntirish:** `LinkedHashMap`ning `accessOrder=true` rejimi eng kam ishlatilgan sahifani avtomatik o'chirib, eng yangilarini saqlab qoladi.

---

### Topshiriq #1239: WAL Replay (Crash Recovery)
**Tavsif:** Tizim qayta ishga tushganda WAL faylini o'qib, bajarilmay qolgan operatsiyalarni tiklash.
**Talablar:** Fayl oxirigacha o'qish va ma'lumotlarni qayta tiklash.
**Yechim (Java):**
```java
import java.nio.file.*;
import java.util.List;

public class RecoveryManager {
    public void recover(String logPath) throws IOException {
        List<String> logs = Files.readAllLines(Paths.get(logPath));
        for (String log : logs) {
            // Logdagi operatsiyani qayta bajarish
            System.out.println("Tiklanmoqda: " + log);
        }
    }
}
```
**Tushuntirish:** Bu jarayon ma'lumotlar bazasining "Atomicity" xususiyatini ta'minlaydi, ya'ni tranzaksiya yo to'liq bajariladi, yo umuman bajarilmaydi.

---

### Topshiriq #1240: B+Tree'da kalitni o'chirish (Underflow handling)
**Tavsif:** B+Tree'dan kalit o'chirilganda, tugun to'lib qolish minimal chegarasidan pastga tushsa, qo'shni tugun bilan birlashtirish.
**Talablar:** Daraxt muvozanatini saqlash.
**Yechim (Java):**
```java
public class BTreeDeleter {
    public void handleUnderflow(Node node) {
        if (node.keys.length < MIN_KEYS) {
            // Qo'shni tugundan kalit olish yoki birlashtirish
            System.out.println("Underflow aniqlandi, qayta muvozanatlash...");
        }
    }
}
```
**Tushuntirish:** O'chirish operatsiyasi qo'shishdan murakkabroq, chunki u daraxtning barcha darajalariga ta'sir qilishi mumkin. Ushbu yondashuv daraxtning doimiy samaradorligini ta'minlaydi.

---

### Topshiriq #1241: B+ Tree tugunini qidirish algoritmi
**Tavsif:** B+ Tree ma'lumotlar bazasi indekslarining asosi hisoblanadi. Katta hajmdagi ma'lumotlar ichidan kerakli kalitni (key) tezkor topish uchun binar qidiruvni amalga oshirish zarur.
**Talablar:** O(log n) murakkablik, xotira xavfsizligi va null-pointer tekshiruvi.
**Yechim (Java):**
```java
public class BPlusNode {
    private long[] keys; // Tugundagi kalitlar
    
    public int findKeyIndex(long key) {
        int low = 0, high = keys.length - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (keys[mid] == key) return mid;
            else if (keys[mid] < key) low = mid + 1;
            else high = mid - 1;
        }
        return low; // Kalit topilmasa, joylashish o'rnini qaytaradi
    }
}
```
**Tushuntirish:** Binar qidiruv (Binary Search) katta tugunlar ichida qidiruvni optimallashtiradi, bu esa diskdan o'qish sonini kamaytiradi.

### Topshiriq #1242: WAL (Write-Ahead Logging) uchun log yozuvchi
**Tavsif:** Ma'lumotlar bazasi kutilmaganda o'chib qolganda ma'lumotlar yo'qolmasligi uchun har bir operatsiyani diskka yozib borish (WAL).
**Talablar:** Thread-safe yozish va ma'lumotlar yaxlitligi (integrity).
**Yechim (Java):**
```java
import java.io.*;
import java.nio.file.*;

public class WALManager {
    private final BufferedWriter writer;

    public WALManager(String path) throws IOException {
        this.writer = Files.newBufferedWriter(Paths.get(path), StandardOpenOption.APPEND, StandardOpenOption.CREATE);
    }

    public synchronized void log(String operation) throws IOException {
        writer.write(System.currentTimeMillis() + ":" + operation);
        writer.newLine();
        writer.flush(); // Har bir yozuvdan so'ng diskka majburiy yozish
    }
}
```
**Tushuntirish:** `flush()` metodi ma'lumotlarning operativ xotirada qolib ketmasligini va real diskka yozilishini ta'minlaydi.

### Topshiriq #1243: LSM-Tree MemTable to'lib qolganda flush qilish
**Tavsif:** LSM-Tree xotiradagi (MemTable) ma'lumotlar to'lganda ularni diskka (SSTable) ko'chirish jarayoni.
**Talablar:** ConcurrentSkipListMap yordamida thread-safe tuzilma yaratish.
**Yechim (Java):**
```java
import java.util.concurrent.ConcurrentSkipListMap;

public class MemTable {
    private final ConcurrentSkipListMap<String, String> data = new ConcurrentSkipListMap<>();
    private final int MAX_SIZE = 1000;

    public void put(String key, String value) {
        if (data.size() >= MAX_SIZE) {
            flushToDisk();
        }
        data.put(key, value);
    }

    private void flushToDisk() {
        // Diskka yozish logikasi (SSTable yaratish)
        data.clear();
    }
}
```
**Tushuntirish:** `ConcurrentSkipListMap` ma'lumotlarni avtomatik tartiblaydi, bu esa keyinchalik diskka yozishda vaqtni tejaydi.

### Topshiriq #1244: B+ Tree tugunini bo'lish (Split)
**Tavsif:** B+ Tree tuguni to'lib qolganda, uni ikkiga ajratish va ota tugunni yangilash.
**Talablar:** Strukturaviy yaxlitlikni saqlash va pointerlarni to'g'ri qayta ulash.
**Yechim (Java):**
```java
public class NodeSplitter {
    public void split(BPlusNode parent, BPlusNode child) {
        int mid = child.getKeys().length / 2;
        BPlusNode newNode = new BPlusNode();
        // O'ng qismni yangi tugunga ko'chirish
        System.arraycopy(child.getKeys(), mid, newNode.getKeys(), 0, mid);
        // Ota tugunga o'rta elementni qo'shish
        parent.insertKey(child.getKeys()[mid]);
    }
}
```
**Tushuntirish:** Tugunni bo'lish daraxt muvozanatini saqlaydi, bu esa qidiruv tezligini barqarorlashtiradi.

### Topshiriq #1245: SSTable qidiruvi (Bloom Filter)
**Tavsif:** LSM-Tree'da ma'lumot qaysi SSTable faylida ekanligini tez aniqlash uchun Bloom Filterdan foydalanish.
**Talablar:** Ehtimollik nazariyasiga asoslangan tezkor tekshiruv.
**Yechim (Java):**
```java
import java.util.BitSet;

public class BloomFilter {
    private BitSet bitSet = new BitSet(1024);

    public void add(String key) {
        bitSet.set(key.hashCode() % 1024);
    }

    public boolean mightContain(String key) {
        return bitSet.get(key.hashCode() % 1024);
    }
}
```
**Tushuntirish:** Bloom Filter diskka murojaat qilishdan oldin ma'lumot yo'qligini 100% aniqlik bilan tasdiqlaydi, bu esa I/O operatsiyalarini keskin kamaytiradi.

### Topshiriq #1246: Indekslash - Hash Index yaratish
**Tavsif:** Kalit-qiymat juftligini xotirada tezkor topish uchun Hash Index tuzilmasi.
**Talablar:** O(1) vaqt murakkabligi va to'qnashuvlarni (collision) boshqarish.
**Yechim (Java):**
```java
import java.util.HashMap;

public class HashIndex {
    private HashMap<String, Long> index = new HashMap<>();

    public void updateIndex(String key, long offset) {
        index.put(key, offset); // Offset - diskdagi manzil
    }

    public long getOffset(String key) {
        return index.getOrDefault(key, -1L);
    }
}
```
**Tushuntirish:** Hash Index xotirada saqlanadi va diskdagi ma'lumotlarning aniq manzilini (offset) ko'rsatib beradi.

### Topshiriq #1247: WAL Replay (Qayta tiklash)
**Tavsif:** Tizim ishdan chiqqandan so'ng, WAL faylini o'qib, ma'lumotlarni qayta tiklash.
**Talablar:** Fayl oxirigacha xatosiz o'qish va ma'lumotlar yaxlitligini tekshirish.
**Yechim (Java):**
```java
import java.nio.file.*;
import java.util.List;

public class WALReplayer {
    public void recover(String path) throws Exception {
        List<String> lines = Files.readAllLines(Paths.get(path));
        for (String line : lines) {
            String[] parts = line.split(":");
            // Ma'lumotlarni bazaga qayta yuklash
            System.out.println("Tiklanmoqda: " + parts[1]);
        }
    }
}
```
**Tushuntirish:** Bu mexanizm ma'lumotlar bazasining "ACID" xususiyatlaridan biri bo'lgan chidamlilikni (Durability) ta'minlaydi.

### Topshiriq #1248: LSM-Tree Compaction (Siqish)
**Tavsif:** Bir nechta SSTable fayllarini birlashtirib, eskirgan ma'lumotlarni o'chirish.
**Talablar:** Xotirani tejash va diskdagi fragmentatsiyani kamaytirish.
**Yechim (Java):**
```java
import java.util.*;

public class Compactor {
    public void compact(List<Map<String, String>> tables) {
        TreeMap<String, String> merged = new TreeMap<>();
        for (Map<String, String> table : tables) {
            merged.putAll(table); // Eng oxirgi qiymat qoladi
        }
        // Yangi SSTable yozish
    }
}
```
**Tushuntirish:** `TreeMap` yordamida kalitlar tartiblanadi va dublikatlar o'chiriladi, bu esa o'qish unumdorligini oshiradi.

### Topshiriq #1249: B+ Tree Range Query (Diapazonli qidiruv)
**Tavsif:** B+ Tree'ning barg tugunlari o'zaro bog'langanligi sababli, ma'lum diapazondagi ma'lumotlarni ketma-ket o'qish.
**Talablar:** Pointerlar orqali keyingi tugunga o'tish va diapazonni yig'ish.
**Yechim (Java):**
```java
public void rangeQuery(BPlusNode startNode, long startKey, long endKey) {
    BPlusNode current = startNode;
    while (current != null) {
        for (long key : current.getKeys()) {
            if (key >= startKey && key <= endKey) {
                System.out.println("Topildi: " + key);
            }
        }
        current = current.getNext(); // Barg tugunlar o'zaro bog'langan
    }
}
```
**Tushuntirish:** B+ Tree'ning barglaridagi bog'lanishlar (linked list) diapazonli qidiruvni juda samarali qiladi.

### Topshiriq #1250: Buffer Pool Manager
**Tavsif:** Diskdagi sahifalarni (pages) xotirada vaqtincha saqlash uchun LRU (Least Recently Used) kesh tizimi.
**Talablar:** Eng kam ishlatilgan ma'lumotni xotiradan chiqarib tashlash.
**Yechim (Java):**
```java
import java.util.LinkedHashMap;

public class BufferPool<K, V> extends LinkedHashMap<K, V> {
    private final int capacity;

    public BufferPool(int capacity) {
        super(capacity, 0.75f, true);
        this.capacity = capacity;
    }

    @Override
    protected boolean removeEldestEntry(java.util.Map.Entry<K, V> eldest) {
        return size() > capacity;
    }
}
```
**Tushuntirish:** `LinkedHashMap`ning `accessOrder` parametri orqali LRU algoritmi oson amalga oshiriladi, bu esa tez-tez murojaat qilinadigan ma'lumotlarni xotirada ushlab turadi.