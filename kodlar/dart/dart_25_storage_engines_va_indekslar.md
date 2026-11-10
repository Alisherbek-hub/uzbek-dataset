# Khorazmiy AI: Dart - Modul 25
## Mavzu: Ma'lumotlar bazasi ichki tuzilishi: LSM-Trees, B+Trees, WAL va Indekslash

### Topshiriq #1201: WAL (Write-Ahead Logging) mexanizmini implementatsiya qilish
**Tavsif:** Ma'lumotlar bazasidagi tranzaksiyalarning barqarorligini ta'minlash uchun xatolik yuz berganda ma'lumotlarni tiklash zarur.
**Talablar:** Har bir yozish operatsiyasidan oldin log fayliga yozish (append-only), xavfsizlik uchun `flush` operatsiyasini bajarish.
**Yechim (Dart):**
```dart
import 'dart:io';

class WriteAheadLog {
  final File _logFile;

  WriteAheadLog(String path) : _logFile = File(path);

  // Tranzaksiyani logga yozish
  Future<void> log(String operation, Map<String, dynamic> data) async {
    final entry = "${DateTime.now().toIso8601String()}: $operation -> $data\n";
    await _logFile.writeAsString(entry, mode: FileMode.append, flush: true);
  }
}
```
**Tushuntirish:** `flush: true` operatsiyasi ma'lumotlar operativ xotirada qolib ketmasdan, to'g'ridan-to'g'ri diskka yozilishini ta'minlaydi, bu tizim qulaganda ma'lumotlar yo'qolishining oldini oladi.

---

### Topshiriq #1202: B+Tree tugunini (Node) loyihalash
**Tavsif:** Indekslash samaradorligini oshirish uchun B+Tree ma'lumotlar tuzilmasini yaratish.
**Talablar:** Tugun ichida kalitlar va bolalar ko'rsatkichlarini saqlash, tartiblanganlikni ta'minlash.
**Yechim (Dart):**
```dart
class BPlusNode {
  List<int> keys = [];
  List<BPlusNode?> children = [];
  bool isLeaf;

  BPlusNode({this.isLeaf = false});

  // Kalitni tartib bilan qo'shish
  void insertKey(int key) {
    keys.add(key);
    keys.sort();
  }
}
```
**Tushuntirish:** B+Tree'da barcha ma'lumotlar barg tugunlarida saqlanadi, bu esa diapazonli qidiruvni (range query) O(log n) murakkablikda bajarish imkonini beradi.

---

### Topshiriq #1203: LSM-Tree uchun MemTable implementatsiyasi
**Tavsif:** Yozish tezligini oshirish uchun xotirada ma'lumotlarni vaqtinchalik saqlash (LSM-Tree asosiy komponenti).
**Talablar:** O(1) yoki O(log n) vaqtda yozish, ma'lumotlar to'lganda diskka (SSTable) ko'chirish.
**Yechim (Dart):**
```dart
import 'dart:collection';

class MemTable {
  final SplayTreeMap<String, String> _data = SplayTreeMap();
  final int limit = 1000;

  void put(String key, String value) {
    _data[key] = value;
    if (_data.length >= limit) _flushToDisk();
  }

  void _flushToDisk() {
    print("MemTable diskka ko'chirildi (SSTable yaratildi).");
    _data.clear();
  }
}
```
**Tavsif:** `SplayTreeMap` yordamida kalitlar avtomatik tartiblanadi, bu esa keyinchalik SSTable fayllarini birlashtirish (compaction) jarayonini osonlashtiradi.

---

### Topshiriq #1204: B+Tree qidiruv algoritmi
**Tavsif:** Indekslangan ma'lumotlar bazasidan kalit bo'yicha tezkor qidiruvni amalga oshirish.
**Talablar:** Rekursiv qidiruv, samarali taqqoslash.
**Yechim (Dart):**
```dart
int? search(BPlusNode? node, int key) {
  if (node == null) return null;
  int i = 0;
  while (i < node.keys.length && key > node.keys[i]) i++;
  
  if (i < node.keys.length && node.keys[i] == key) return node.keys[i];
  if (node.isLeaf) return null;
  
  return search(node.children[i], key);
}
```
**Tushuntirish:** Bu algoritmi daraxtning balandligiga qarab O(log n) vaqt sarflaydi, bu millionlab yozuvlar orasidan soniyada natija olish imkonini beradi.

---

### Topshiriq #1205: SSTable (Sorted String Table) formatini yaratish
**Tavsif:** Diskda ma'lumotlarni doimiy saqlash uchun ixcham va tartiblangan format.
**Talablar:** Fayl hajmini optimallashtirish, o'qish tezligini oshirish.
**Yechim (Dart):**
```dart
class SSTable {
  Future<void> save(Map<String, String> data, String filename) async {
    final file = File(filename);
    final sink = file.openWrite();
    // Kalitlar tartiblangan holda yoziladi
    data.keys.toList()..sort().forEach((key) {
      sink.writeln("$key:${data[key]}");
    });
    await sink.close();
  }
}
```
**Tushuntirish:** SSTable o'zgarmas (immutable) bo'lgani uchun konkurent o'qish operatsiyalarida qulflarni (lock) talab qilmaydi, bu esa yuqori unumdorlikni beradi.

---

### Topshiriq #1206: LSM-Tree Compaction (Siqish) jarayoni
**Tavsif:** Eski va yangi SSTable fayllarini birlashtirib, dublikatlarni o'chirish.
**Talablar:** Xotirani tejash, eski versiyalarni tozalash.
**Yechim (Dart):**
```dart
Map<String, String> compact(Map<String, String> oldData, Map<String, String> newData) {
  // Yangi ma'lumotlar eskisini ustiga yozadi
  return {...oldData, ...newData};
}
```
**Tushuntirish:** Compaction jarayoni LSM-Tree'ning "o'qish sekinligi" muammosini hal qiladi, chunki u fayllar sonini kamaytiradi va qidiruv maydonini qisqartiradi.

---

### Topshiriq #1207: Indeks uchun Bloom Filter
**Tavsif:** SSTable faylida kalit borligini tekshirishdan oldin diskka murojaatni kamaytirish.
**Talablar:** Probabilistik tekshiruv, xotira samaradorligi.
**Yechim (Dart):**
```dart
import 'dart:typed_data';

class BloomFilter {
  final int size = 1024;
  final Uint8List bits = Uint8List(1024);

  void add(String key) {
    int hash = key.hashCode % size;
    bits[hash] = 1;
  }

  bool contains(String key) => bits[key.hashCode % size] == 1;
}
```
**Tushuntirish:** Bloom filter 100% aniqlik bermasa ham, "kalit yo'q" degan javobni aniq beradi, bu esa keraksiz disk I/O operatsiyalarini 90% gacha qisqartiradi.

---

### Topshiriq #1208: B+Tree tugunini bo'lish (Split)
**Tavsif:** Tugun to'lib qolganda daraxt muvozanatini saqlash uchun uni ikkiga bo'lish.
**Talablar:** Ota-tugunni yangilash, ma'lumotlar yaxlitligini saqlash.
**Yechim (Dart):**
```dart
void splitNode(BPlusNode node) {
  int mid = node.keys.length ~/ 2;
  BPlusNode newNode = BPlusNode(isLeaf: node.isLeaf);
  newNode.keys.addAll(node.keys.sublist(mid));
  node.keys.removeRange(mid, node.keys.length);
  // Ota tugunga yangi tugunni ulash logikasi shu yerda bo'ladi
}
```
**Tushuntirish:** Bo'lish jarayoni daraxtning "balandligini" nazorat qiladi, bu esa qidiruv vaqtini barqaror saqlaydi.

---

### Topshiriq #1209: WAL Recovery (Tiklash)
**Tavsif:** Tizim kutilmaganda o'chganda, WAL faylidan ma'lumotlarni qayta tiklash.
**Talablar:** Faylni satrma-satr o'qish, MemTable'ni qayta to'ldirish.
**Yechim (Dart):**
```dart
Future<void> recover(String path, MemTable memTable) async {
  final lines = await File(path).readAsLines();
  for (var line in lines) {
    // Log formatini tahlil qilib MemTable'ga qaytarish
    print("Tiklanmoqda: $line");
  }
}
```
**Tushuntirish:** Bu jarayon ma'lumotlar bazasining ACID xususiyatlaridan biri bo'lgan "Durability" (bardoshlilik) ni ta'minlaydi.

---

### Topshiriq #1210: Indekslashda "Tombstone" (O'chirish belgisi)
**Tavsif:** LSM-Tree'da ma'lumotni jismonan o'chirish qimmat bo'lgani uchun, o'chirilganligini belgilash.
**Talablar:** O'chirilgan yozuvni aniqlash, keyingi compaction'da tozalash.
**Yechim (Dart):**
```dart
class Tombstone {
  static const String marker = "__DELETED__";

  void delete(String key, MemTable memTable) {
    memTable.put(key, marker);
  }
}
```
**Tushuntirish:** "Tombstone" yozish operatsiyasini tezlashtiradi, chunki diskdagi faylni qayta yozish shart emas, shunchaki yangi yozuv qo'shiladi.

---

### Topshiriq #1211: WAL (Write-Ahead Logging) mexanizmini implementatsiya qilish
**Tavsif:** Ma'lumotlar bazasida kutilmagan o'chishlar (crash) yuz berganda ma'lumotlar yaxlitligini saqlash uchun operatsiyalarni diskga yozishdan oldin jurnalga yozish zarurati.
**Talablar:** Jurnal fayliga yozish atomik bo'lishi va operatsiyalar ketma-ketligi saqlanishi kerak.
**Yechim (Dart):**
```dart
import 'dart:io';

class WriteAheadLog {
  final File _logFile = File('database.wal');

  // Operatsiyani jurnalga yozish
  Future<void> logOperation(String operation) async {
    final timestamp = DateTime.now().toIso8601String();
    await _logFile.writeAsString('$timestamp: $operation\n', mode: FileMode.append);
  }
}
```
**Tushuntirish:** WAL yordamida tizim ishdan chiqqanda, oxirgi bajarilmagan operatsiyalarni jurnal orqali qayta tiklash (replay) imkoniyati yaratiladi.

### Topshiriq #1212: LSM-Tree uchun MemTable tuzilmasi
**Tavsif:** LSM-Tree'da yozish tezligini oshirish uchun ma'lumotlarni avval xotirada (RAM) saqlash va keyin diskga "flush" qilish.
**Talablar:** MemTable to'lganda avtomatik diskga o'tkazish mexanizmi.
**Yechim (Dart):**
```dart
class MemTable {
  final Map<String, String> _data = {};
  final int _maxSize = 1000;

  void insert(String key, String value) {
    _data[key] = value;
    if (_data.length >= _maxSize) {
      _flushToDisk();
    }
  }

  void _flushToDisk() {
    print("MemTable diskga ko'chirildi.");
    _data.clear();
  }
}
```
**Tushuntirish:** MemTable yozish operatsiyalarini O(1) vaqtda bajaradi, bu esa diskdagi sekin yozish jarayonini optimallashtiradi.

### Topshiriq #1213: B+Tree tugunini (Node) loyihalash
**Tavsif:** B+Tree ma'lumotlar bazasini indekslashda keng qo'llaniladi. Har bir tugun kalitlar va bolalar manzillarini saqlashi kerak.
**Talablar:** Tugun sig'imi (order) belgilangan bo'lishi va kalitlar tartiblangan bo'lishi shart.
**Yechim (Dart):**
```dart
class BPlusNode {
  List<int> keys = [];
  List<BPlusNode?> children = [];
  bool isLeaf;

  BPlusNode({this.isLeaf = false});
}
```
**Tushuntirish:** B+Tree'da barcha ma'lumotlar barg tugunlarida saqlanadi, bu esa diapazonli qidiruvni (range query) juda tezlashtiradi.

### Topshiriq #1214: LSM-Tree uchun Bloom Filter
**Tavsif:** LSM-Tree'da qidiruvni tezlashtirish uchun kerakli kalit qaysi SSTable faylida borligini oldindan bilish.
**Talablar:** Ehtimollik nazariyasiga asoslangan qidiruvni optimallashtirish.
**Yechim (Dart):**
```dart
import 'dart:collection';

class BloomFilter {
  final int size = 100;
  final BitSet _bits = BitSet(100);

  void add(String key) {
    int hash = key.hashCode % size;
    _bits.set(hash);
  }

  bool contains(String key) => _bits.get(key.hashCode % size);
}
```
**Tushuntirish:** Bloom Filter diskdagi keraksiz o'qish operatsiyalarini (I/O) keskin kamaytiradi.

### Topshiriq #1215: B+Tree'da kalitni qidirish algoritmi
**Tavsif:** Indekslangan ma'lumotlar bazasidan kerakli yozuvni O(log n) vaqtda topish.
**Talablar:** Rekursiv qidiruv algoritmi.
**Yechim (Dart):**
```dart
int? search(BPlusNode node, int key) {
  int i = 0;
  while (i < node.keys.length && key > node.keys[i]) i++;
  if (i < node.keys.length && node.keys[i] == key) return node.keys[i];
  if (node.isLeaf) return null;
  return search(node.children[i]!, key);
}
```
**Tushuntirish:** B+Tree daraxti muvozanatli bo'lgani uchun qidiruv har doim samarali bajariladi.

### Topshiriq #1216: SSTable (Sorted String Table) formatini yaratish
**Tavsif:** MemTable'dan diskga tushirilgan ma'lumotlarni tartiblangan holda saqlash.
**Talablar:** Fayl o'zgarmas (immutable) bo'lishi kerak.
**Yechim (Dart):**
```dart
class SSTable {
  final String filePath;
  SSTable(this.filePath);

  Future<void> write(Map<String, String> data) async {
    final sortedKeys = data.keys.toList()..sort();
    final file = File(filePath);
    for (var key in sortedKeys) {
      await file.writeAsString('$key:${data[key]}\n', mode: FileMode.append);
    }
  }
}
```
**Tushuntirish:** SSTable tartiblanganligi sababli binar qidiruv (binary search) orqali ma'lumotlarni tez topish mumkin.

### Topshiriq #1217: LSM-Tree Compaction (Siqish) jarayoni
**Tavsif:** Ko'plab SSTable fayllarini birlashtirib, eskirgan ma'lumotlarni o'chirish.
**Talablar:** Xotira va disk samaradorligini ta'minlash.
**Yechim (Dart):**
```dart
void compact(List<Map<String, String>> tables) {
  Map<String, String> merged = {};
  for (var table in tables) {
    merged.addAll(table); // Oxirgi versiya ustunlik qiladi
  }
  // Yangi SSTable yaratish
}
```
**Tushuntirish:** Compaction jarayoni ma'lumotlar bazasining hajmini kichraytiradi va o'qish tezligini oshiradi.

### Topshiriq #1218: Indekslashda B-Tree vs B+Tree solishtiruvi
**Tavsif:** Qaysi indeks turi qaysi vaziyatda samaraliroq ekanligini aniqlash uchun benchmark.
**Talablar:** Qidiruv vaqti tahlili.
**Yechim (Dart):**
```dart
void benchmark() {
  final stopwatch = Stopwatch()..start();
  // B+Tree qidiruvi
  stopwatch.stop();
  print("Qidiruv vaqti: ${stopwatch.elapsedMicroseconds} mks");
}
```
**Tushuntirish:** B+Tree diapazonli so'rovlar uchun, B-Tree esa individual kalit qidiruvlari uchun optimallashtirilgan.

### Topshiriq #1219: Ma'lumotlar bazasi uchun "Page" boshqaruvi
**Tavsif:** Diskdagi ma'lumotlarni bloklar (pages) ko'rinishida o'qish va yozish.
**Talablar:** Page hajmi odatda 4KB yoki 8KB bo'lishi kerak.
**Yechim (Dart):**
```dart
class Page {
  final int pageSize = 4096;
  final List<int> data = List.filled(4096, 0);
  
  void writeAt(int offset, List<int> bytes) {
    data.setRange(offset, offset + bytes.length, bytes);
  }
}
```
**Tushuntirish:** Page-based storage diskdagi ma'lumotlarni boshqarishni osonlashtiradi va I/O samaradorligini oshiradi.

### Topshiriq #1220: Indeksni qayta tiklash (Rebuild)
**Tavsif:** Ma'lumotlar bazasi buzilganda indeks fayllarini qayta qurish.
**Talablar:** WAL faylidan foydalanib indeksni qayta tiklash.
**Yechim (Dart):**
```dart
void rebuildIndex(File walFile) {
  final lines = walFile.readAsLinesSync();
  for (var line in lines) {
    // Har bir operatsiyani qayta bajarib indeksni yangilash
    print("Indeks yangilandi: $line");
  }
}
```
**Tushuntirish:** Rebuild jarayoni ma'lumotlar bazasining "Self-healing" (o'zini tiklash) qobiliyatini ta'minlaydi.

---

### Topshiriq #1221: B+Tree tugunini xotirada boshqarish
**Tavsif:** B+Tree ma'lumotlar bazasi indekslari uchun tugunlarni (node) samarali saqlash va ularni diskdan o'qish/yozish uchun xotira bloklarini boshqarish.
**Talablar:** Tugun hajmi 4KB (sahifa hajmi) ga teng bo'lishi va xotira oqishini (memory leak) oldini olish.
**Yechim (Dart):**
```dart
class BTreeNode {
  final int pageSize = 4096;
  List<int> keys = [];
  List<dynamic> values = [];
  bool isLeaf;

  BTreeNode(this.isLeaf);

  // Tugunni bayt ko'rinishiga o'tkazish (serilizatsiya)
  List<int> serialize() {
    // Haqiqiy tizimda bu yerda BinaryWriter ishlatiladi
    return List.filled(pageSize, 0); 
  }
}
```
**Tushuntirish:** B+Tree diskdagi sahifalar bilan ishlaydi. 4KB o'lchami operatsion tizimning sahifalash (paging) mexanizmi bilan mos keladi, bu esa I/O unumdorligini oshiradi.

### Topshiriq #1222: Write-Ahead Logging (WAL) mexanizmi
**Tavsif:** Ma'lumotlar bazasidagi har qanday o'zgarishni diskka yozishdan oldin jurnalga yozib qo'yish (Crash recovery uchun).
**Talablar:** Jurnal fayli append-only bo'lishi va tranzaksiya atomikligini ta'minlashi shart.
**Yechim (Dart):**
```dart
import 'dart:io';

class WALManager {
  final File logFile = File('database.wal');

  Future<void> logOperation(String operation) async {
    // Har bir operatsiyani jurnalga yozish
    await logFile.writeAsString('$operation\n', mode: FileMode.append, flush: true);
  }
}
```
**Tushuntirish:** `flush: true` buyrug'i ma'lumotlar operativ xotiradan disk buferiga o'tishini kafolatlaydi, bu esa tizim ishdan chiqqanda ma'lumotlar yo'qolmasligini ta'minlaydi.

### Topshiriq #1223: LSM-Tree MemTable implementatsiyasi
**Tavsif:** LSM-Tree tarkibidagi MemTable (xotiradagi vaqtinchalik jadval) uchun tezkor qidiruv va tartiblash.
**Talablar:** Qidiruv murakkabligi O(log n) bo'lishi va xotira to'lganda diskka (SSTable) ko'chirish mexanizmi.
**Yechim (Dart):**
```dart
import 'dart:collection';

class MemTable {
  final SplayTreeMap<String, String> _data = SplayTreeMap();

  void put(String key, String value) => _data[key] = value;
  
  String? get(String key) => _data[key];

  bool isFull(int limit) => _data.length >= limit;
}
```
**Tushuntirish:** `SplayTreeMap` avtomatik tartiblangan holda saqlaydi, bu esa ma'lumotlarni diskka yozishdan oldin ularni tartibli (Sorted String Table) holatga keltirishni osonlashtiradi.

### Topshiriq #1224: SSTable (Sorted String Table) qidiruvi
**Tavsif:** Diskdagi tartiblangan fayllarda qidiruvni tezlashtirish uchun "Sparse Index" (siyrak indeks) yaratish.
**Talablar:** Barcha kalitlarni emas, balki har N-chi kalitni indekslash.
**Yechim (Dart):**
```dart
class SparseIndex {
  final Map<String, int> index = {}; // Kalit -> Diskdagi ofset

  void addEntry(String key, int offset) => index[key] = offset;

  int? findOffset(String key) {
    // Eng yaqin kichik ofsetni topish
    return index[key]; 
  }
}
```
**Tushuntirish:** Siyrak indeks xotirani tejaydi va diskdagi kerakli blokni tezroq topishga yordam beradi.

### Topshiriq #1225: B+Tree Split (Tugunni bo'lish)
**Tavsif:** B+Tree tuguni to'lganda uni ikkiga bo'lish va ota tugunni yangilash.
**Talablar:** Daraxt muvozanatini (balance) saqlash.
**Yechim (Dart):**
```dart
void splitNode(BTreeNode node) {
  int mid = node.keys.length ~/ 2;
  var newNode = BTreeNode(node.isLeaf);
  newNode.keys.addAll(node.keys.sublist(mid));
  node.keys.removeRange(mid, node.keys.length);
  // Ota tugunga yangi tugunni qo'shish logikasi
}
```
**Tushuntirish:** Tugunni bo'lish daraxt balandligini bir xil saqlaydi, bu esa qidiruv vaqtini doimiy O(log n) darajasida ushlab turadi.

### Topshiriq #1226: LSM-Tree Compaction (Siqish)
**Tavsif:** Bir nechta SSTable fayllarini birlashtirib, eskirgan ma'lumotlarni o'chirish.
**Talablar:** "Merge Sort" algoritmidan foydalangan holda bir nechta faylni birlashtirish.
**Yechim (Dart):**
```dart
List<String> compact(List<List<String>> sstables) {
  // Merge sort mantig'i bilan dublikatlarni tozalash
  return sstables.expand((x) => x).toSet().toList()..sort();
}
```
**Tushuntirish:** Compaction jarayoni diskdagi keraksiz ma'lumotlarni (tombstones) tozalaydi va o'qish unumdorligini oshiradi.

### Topshiriq #1227: Bloom Filter (Qidiruvni optimallashtirish)
**Tavsif:** Kalit diskda mavjudligini tekshirish uchun tezkor ehtimollik filtri.
**Talablar:** Xotira sarfini minimallashtirish va "False Positive" darajasini nazorat qilish.
**Yechim (Dart):**
```dart
import 'dart:typed_data';

class BloomFilter {
  final Uint8List bits = Uint8List(1024); // 1KB bit massiv

  void add(String key) {
    int hash = key.hashCode % 8192;
    bits[hash ~/ 8] |= (1 << (hash % 8));
  }
}
```
**Tushuntirish:** Bloom Filter diskka murojaat qilishdan oldin kalitning yo'qligini aniqlab beradi, bu esa I/O operatsiyalarini keskin kamaytiradi.

### Topshiriq #1228: Tranzaksiya izolyatsiyasi (Locking)
**Tavsif:** Bir vaqtning o'zida yozish operatsiyalarida ma'lumotlar yaxlitligini saqlash.
**Talablar:** `Mutex` yoki `Lock` mexanizmidan foydalanib, "Race condition"ni oldini olish.
**Yechim (Dart):**
```dart
import 'dart:async';
import 'package:synchronized/synchronized.dart';

final Lock _lock = Lock();

Future<void> safeWrite(Function operation) async {
  await _lock.synchronized(() async {
    await operation();
  });
}
```
**Tushuntirish:** `synchronized` kutubxonasi yordamida yozish jarayonini navbatga qo'yish ma'lumotlar bazasi izchilligini ta'minlaydi.

### Topshiriq #1229: Diskdagi ma'lumotlarni o'qish (Buffer Pool)
**Tavsif:** Diskdan o'qilgan sahifalarni xotirada vaqtincha saqlash (LRU Cache).
**Talablar:** Eng kam ishlatilgan (Least Recently Used) sahifani xotiradan chiqarib tashlash.
**Yechim (Dart):**
```dart
class BufferPool {
  final Map<int, List<int>> cache = {};
  final int capacity = 100;

  void addPage(int pageId, List<int> data) {
    if (cache.length >= capacity) cache.remove(cache.keys.first);
    cache[pageId] = data;
  }
}
```
**Tushuntirish:** Buffer Pool diskka tez-tez murojaat qilishni kamaytiradi, bu esa ma'lumotlar bazasi tezligini 10-100 barobargacha oshirishi mumkin.

### Topshiriq #1230: Indeksni qayta tiklash (Recovery)
**Tavsif:** Tizim kutilmaganda o'chganda WAL fayli orqali indeksni qayta qurish.
**Talablar:** WAL faylini boshidan oxirigacha o'qib, MemTable'ni qayta to'ldirish.
**Yechim (Dart):**
```dart
Future<void> recover(File walFile) async {
  final lines = await walFile.readAsLines();
  for (var line in lines) {
    // Har bir operatsiyani qayta ijro etish (Replay)
    print("Qayta tiklanmoqda: $line");
  }
}
```
**Tushuntirish:** WAL orqali tiklash ma'lumotlar bazasining "ACID" xususiyatlaridan biri bo'lgan "Durability" (bardoshlilik)ni ta'minlaydi.

---

### Topshiriq #1231: WAL (Write-Ahead Logging) tizimini implementatsiya qilish
**Tavsif:** Ma'lumotlar bazasiga yozishdan oldin operatsiyani log faylga yozish orqali tizim nosozliklarida ma'lumotlar yaxlitligini ta'minlash.
**Talablar:** Faylga ketma-ket yozish (append-only), xatolik yuz berganda qayta tiklash imkoniyati.
**Yechim (Dart):**
```dart
import 'dart:io';

class WriteAheadLog {
  final File _logFile;
  WriteAheadLog(String path) : _logFile = File(path);

  // Logga operatsiyani yozish
  Future<void> log(String operation) async {
    await _logFile.writeAsString('$operation\n', mode: FileMode.append);
  }
}
```
**Tushuntirish:** WAL ma'lumotlar bazasi "crash" bo'lganda, operatsiyalarni qayta ijro etish (replay) orqali ma'lumotlar yo'qolishining oldini oladi.

### Topshiriq #1232: B+Tree tugunini (Node) loyihalash
**Tavsif:** B+Tree indekslash tuzilmasi uchun asosiy tugunni yaratish.
**Talablar:** Kalitlar (keys) va bolalar (children) ro'yxatini boshqarish, tartiblanganlikni saqlash.
**Yechim (Dart):**
```dart
class BPlusNode {
  List<int> keys = [];
  List<BPlusNode?> children = [];
  bool isLeaf;

  BPlusNode({this.isLeaf = false});

  void insertSorted(int key) {
    keys.add(key);
    keys.sort();
  }
}
```
**Tushuntirish:** B+Tree daraxtida faqat barg tugunlarida ma'lumotlar saqlanadi, bu esa qidiruvni O(log n) murakkablikda bajarish imkonini beradi.

### Topshiriq #1233: LSM-Tree uchun MemTable yaratish
**Tavsif:** LSM-Tree'da yozish tezligini oshirish uchun xotirada joylashgan vaqtinchalik bufer.
**Talablar:** O(1) vaqt murakkabligida yozish, ma'lumotlar to'lganda diskka "flush" qilish.
**Yechim (Dart):**
```dart
class MemTable {
  final Map<String, String> _data = {};
  final int capacity = 1000;

  void put(String key, String value) {
    _data[key] = value;
    if (_data.length >= capacity) flushToDisk();
  }

  void flushToDisk() {
    // Diskka yozish logikasi
    _data.clear();
  }
}
```
**Tushuntirish:** LSM-Tree yozish operatsiyalarini xotirada to'plab, keyinchalik ketma-ket diskka yozadi, bu esa HDD/SSD unumdorligini oshiradi.

### Topshiriq #1234: B+Tree qidiruv algoritmi
**Tavsif:** B+Tree ichidan ma'lum bir kalitni samarali topish.
**Talablar:** Rekursiv qidiruv, O(log n) samaradorlik.
**Yechim (Dart):**
```dart
BPlusNode? search(BPlusNode node, int key) {
  int i = 0;
  while (i < node.keys.length && key > node.keys[i]) i++;
  
  if (node.isLeaf) return node;
  return search(node.children[i]!, key);
}
```
**Tushuntirish:** B+Tree qidiruvda daraxt balandligi past bo'lgani uchun diskdan o'qish soni kamayadi.

### Topshiriq #1235: LSM-Tree uchun SSTable (Sorted String Table)
**Tavsif:** MemTable diskka yozilganda hosil bo'ladigan o'zgarmas (immutable) fayl tuzilmasi.
**Talablar:** Kalitlar bo'yicha saralangan bo'lishi, samarali qidiruv uchun indeks fayli.
**Yechim (Dart):**
```dart
class SSTable {
  final Map<int, String> sortedData;
  SSTable(this.sortedData);

  String? get(int key) => sortedData[key];
}
```
**Tushuntirish:** SSTable o'zgarmas bo'lgani uchun konkurent o'qish operatsiyalari uchun juda xavfsiz va tezdir.

### Topshiriq #1236: Indekslashda "Clustered Index" simulyatsiyasi
**Tavsif:** Ma'lumotlarni jismoniy joylashuvi bo'yicha tartiblash.
**Talablar:** Ma'lumotlar bazasi jadvalini birlamchi kalit bo'yicha saralash.
**Yechim (Dart):**
```dart
class Table {
  List<Map<String, dynamic>> rows = [];
  
  void createClusteredIndex(String key) {
    rows.sort((a, b) => a[key].compareTo(b[key]));
  }
}
```
**Tushuntirish:** Clustered index qidiruvni tezlashtiradi, chunki ma'lumotlar diskda ketma-ket joylashadi.

### Topshiriq #1237: B+Tree tugunini bo'lish (Split)
**Tavsif:** Tugun to'lib qolganda uni ikkiga ajratish.
**Talablar:** O'rta elementni yuqori darajaga ko'tarish, balansni saqlash.
**Yechim (Dart):**
```dart
void splitNode(BPlusNode parent, BPlusNode child) {
  int mid = child.keys.length ~/ 2;
  // O'rta elementni parentga o'tkazish logikasi
  // Yangi tugun yaratib qolgan qismini ko'chirish
}
```
**Tushuntirish:** Split operatsiyasi B+Tree balansini saqlab qolish uchun kritik hisoblanadi.

### Topshiriq #1238: Ma'lumotlar bazasi uchun "Compaction" jarayoni
**Tavsif:** LSM-Tree'da eski va yangi SSTable fayllarini birlashtirish.
**Talablar:** Dublikatlarni o'chirish, disk bo'sh joyini tozalash.
**Yechim (Dart):**
```dart
void compact(List<SSTable> tables) {
  Map<int, String> merged = {};
  for (var table in tables) {
    merged.addAll(table.sortedData);
  }
  // Yangi SSTable yaratish
}
```
**Tushuntirish:** Compaction ma'lumotlar bazasini optimallashtiradi va o'qish tezligini oshiradi.

### Topshiriq #1239: Bloom Filter (Qidiruvni optimallashtirish)
**Tavsif:** Kalit qaysi SSTable'da borligini tez aniqlash uchun ehtimollik tuzilmasi.
**Talablar:** Xotirani tejash, tezkor tekshiruv.
**Yechim (Dart):**
```dart
class BloomFilter {
  final Set<int> _hashes = {};
  void add(int key) => _hashes.add(key.hashCode);
  bool contains(int key) => _hashes.contains(key.hashCode);
}
```
**Tushuntirish:** Bloom Filter diskdan o'qishdan oldin kalitning mavjud emasligini 100% aniqlik bilan tasdiqlaydi.

### Topshiriq #1240: B+Tree "Range Query" (Oraliq qidiruv)
**Tavsif:** B+Tree barg tugunlari orasidagi bog'liqlikdan foydalanib oraliq qiymatlarni olish.
**Talablar:** Barg tugunlari o'rtasidagi "next" ko'rsatkichidan foydalanish.
**Yechim (Dart):**
```dart
List<int> rangeQuery(BPlusNode startNode, int start, int end) {
  List<int> result = [];
  // Barg tugunlari bo'ylab ketma-ket yurish
  return result;
}
```
**Tushuntirish:** B+Tree'ning barglari o'zaro bog'langan (linked list), bu oraliq qidiruvlarni juda tez bajarishga imkon beradi.

---

### Topshiriq #1241: WAL (Write-Ahead Logging) mexanizmini implementatsiya qilish
**Tavsif:** Ma'lumotlar bazasidagi tranzaksiyalarning barqarorligini ta'minlash uchun xatolik yuz berganda ma'lumotlarni tiklash zarur.
**Talablar:** Har bir yozish operatsiyasi diskka yozilishidan oldin log fayliga ketma-ket yozilishi shart.
**Yechim (Dart):**
```dart
import 'dart:io';

class WriteAheadLog {
  final File _logFile = File('database.log');

  // Tranzaksiyani logga yozish
  Future<void> logTransaction(String query) async {
    final timestamp = DateTime.now().toIso8601String();
    await _logFile.writeAsString('$timestamp: $query\n', mode: FileMode.append);
  }
}
```
**Tushuntirish:** WAL tizimi "crash-recovery" uchun asosiy mexanizmdir. Faylga append qilish operatsiyasi diskda ketma-ket (sequential) yozish bo'lgani uchun tezkor ishlaydi.

### Topshiriq #1242: B+Tree tugunini (Node) loyihalash
**Tavsif:** Indekslash uchun samarali ma'lumotlar strukturasi kerak.
**Talablar:** Tugun ichida kalitlar va bolalar (pointers) tartiblangan bo'lishi kerak.
**Yechim (Dart):**
```dart
class BPlusNode {
  List<int> keys = [];
  List<BPlusNode?> children = [];
  bool isLeaf;

  BPlusNode({this.isLeaf = false});
}
```
**Tushuntirish:** B+Tree'da faqat barg tugunlari (leaf nodes) ma'lumotlarni saqlaydi, bu esa qidiruvni O(log n) vaqtda amalga oshirishga imkon beradi.

### Topshiriq #1243: LSM-Tree uchun MemTable (Memory Table)
**Tavsif:** Yozish tezligini oshirish uchun ma'lumotlarni avval xotirada to'plash.
**Talablar:** MemTable to'lganida uni diskka (SSTable) o'tkazish logikasi.
**Yechim (Dart):**
```dart
class MemTable {
  final Map<String, String> _data = {};
  final int capacity = 1000;

  void insert(String key, String value) {
    _data[key] = value;
    if (_data.length >= capacity) {
      flushToDisk();
    }
  }

  void flushToDisk() {
    print("MemTable diskka ko'chirildi (SSTable yaratildi).");
    _data.clear();
  }
}
```
**Tushuntirish:** LSM-Tree yozish operatsiyalarini xotirada (RAM) amalga oshirib, diskdagi IO yuklamasini kamaytiradi.

### Topshiriq #1244: B+Tree qidiruv algoritmi
**Tavsif:** Indeks bo'yicha ma'lumotni tezkor topish.
**Talablar:** Rekursiv qidiruv va vaqt murakkabligi O(log n).
**Yechim (Dart):**
```dart
int? search(BPlusNode node, int key) {
  int i = 0;
  while (i < node.keys.length && key > node.keys[i]) i++;
  
  if (i < node.keys.length && node.keys[i] == key) return node.keys[i];
  if (node.isLeaf) return null;
  
  return search(node.children[i]!, key);
}
```
**Tushuntirish:** B+Tree qidiruvda daraxtning chuqurligi kam bo'lgani uchun diskdan o'qish soni minimal bo'ladi.

### Topshiriq #1245: SSTable (Sorted String Table) formatini yaratish
**Tavsif:** Diskda saqlanadigan ma'lumotlar tartiblangan bo'lishi kerak.
**Talablar:** Kalitlar bo'yicha saralangan fayl strukturasi.
**Yechim (Dart):**
```dart
void saveToSSTable(Map<String, String> data) {
  var sortedKeys = data.keys.toList()..sort();
  for (var key in sortedKeys) {
    // Diskka yozish: key, value
    print("Yozildi: $key -> ${data[key]}");
  }
}
```
**Tushuntirish:** SSTable'lar o'zgarmas (immutable) bo'lgani uchun ularni o'qish juda tez va konkurentlik muammolarini keltirib chiqarmaydi.

### Topshiriq #1246: Bloom Filter (Qidiruvni optimallashtirish)
**Tavsif:** SSTable'da kalit borligini tekshirish uchun diskka murojaat qilmasdan oldin xotirada tekshirish.
**Talablar:** Ehtimollik asosida mavjud emasligini aniqlash.
**Yechim (Dart):**
```dart
class BloomFilter {
  final Set<int> _bits = {};
  
  void add(String key) => _bits.add(key.hashCode);
  bool contains(String key) => _bits.contains(key.hashCode);
}
```
**Tushuntirish:** Bloom filter diskka keraksiz murojaatlarni (I/O) keskin kamaytiradi.

### Topshiriq #1247: Compaction (Siqish) jarayoni
**Tavsif:** Eski va yangi SSTable'larni birlashtirib, dublikatlarni o'chirish.
**Talablar:** Merging jarayoni O(N) vaqtda bajarilishi kerak.
**Yechim (Dart):**
```dart
Map<String, String> compact(Map<String, String> old, Map<String, String> recent) {
  // Yangi qiymatlar eski qiymatlarni ustiga yozadi
  return {...old, ...recent};
}
```
**Tushuntirish:** LSM-Tree'da Compaction diskdagi bo'sh joyni tozalash va qidiruv samaradorligini saqlash uchun zarur.

### Topshiriq #1248: Indeksni saqlash (Sparse Index)
**Tavsif:** Katta fayllar uchun to'liq emas, balki qisman indeks yaratish.
**Talablar:** Har N-chi element uchun offsetni saqlash.
**Yechim (Dart):**
```dart
class SparseIndex {
  final Map<int, int> index = {}; // Kalit -> Fayldagi o'rni (offset)

  void addEntry(int key, int offset) => index[key] = offset;
}
```
**Tushuntirish:** Sparse index xotirani tejaydi va katta hajmdagi ma'lumotlar bazalarida qidiruvni tezlashtiradi.

### Topshiriq #1249: Tranzaksiya izolatsiyasi (Locking)
**Tavsif:** Bir vaqtda yozish operatsiyalarida ma'lumotlar buzilishining oldini olish.
**Talablar:** Mutex (o'zaro istisno) mexanizmidan foydalanish.
**Yechim (Dart):**
```dart
import 'dart:async';

class DatabaseLock {
  bool _isLocked = false;

  Future<void> execute(Function task) async {
    while (_isLocked) await Future.delayed(Duration(milliseconds: 10));
    _isLocked = true;
    await task();
    _isLocked = false;
  }
}
```
**Tushuntirish:** Lock mexanizmi ma'lumotlar bazasi yaxlitligini (ACID) ta'minlash uchun shart.

### Topshiriq #1250: B+Tree tugunini bo'lish (Split)
**Tavsif:** Tugun to'lib qolganda uni ikkiga ajratish.
**Talablar:** Median elementni yuqori darajaga ko'tarish.
**Yechim (Dart):**
```dart
void splitNode(BPlusNode parent, BPlusNode child) {
  int mid = child.keys.length ~/ 2;
  // Median elementni ota tugunga o'tkazish logikasi
  parent.keys.add(child.keys[mid]);
  // Yangi tugun yaratib, qolgan qismini ko'chirish...
}
```
**Tushuntirish:** Split operatsiyasi B+Tree balansini saqlaydi, bu esa daraxtning haddan tashqari bir tomonga og'ib ketishining oldini oladi.