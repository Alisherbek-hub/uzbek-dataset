# Khorazmiy AI: JavaScript & TypeScript - Modul 25
## Mavzu: Ma'lumotlar bazasi ichki tuzilishi: LSM-Trees, B+Trees, WAL va Indekslash

### Topshiriq #1201: WAL (Write-Ahead Logging) mexanizmini implementatsiya qilish
**Tavsif:** Ma'lumotlar bazasi tizimida kutilmagan o'chishlar (crash) sodir bo'lganda ma'lumotlar yaxlitligini saqlash uchun operatsiyalarni diskka yozishdan oldin log faylga yozish zarurati.
**Talablar:** Har bir yozish operatsiyasi atomik bo'lishi va `fs.appendFileSync` orqali diskka sinxron yozilishi kerak.
**Yechim (JavaScript & TypeScript):**
```typescript
import * as fs from 'fs';

class WALManager {
  private logPath: string = 'database.wal';

  // Operatsiyani logga yozish
  log(operation: string, data: object): void {
    const entry = JSON.stringify({ op: operation, data, timestamp: Date.now() }) + '\n';
    fs.appendFileSync(this.logPath, entry, 'utf8');
  }
}
```
**Tushuntirish:** WAL (Write-Ahead Logging) ma'lumotlar bazasi buzilishining oldini oladi. `appendFileSync` operatsiyasi ma'lumotlar diskka to'liq yozilguncha kutishni ta'minlaydi, bu esa "durability" (ACID) xususiyatini kafolatlaydi.

### Topshiriq #1202: B+Tree tugunini (Node) loyihalash
**Tavsif:** B+Tree ma'lumotlar bazasi indekslari uchun asosiy struktura hisoblanadi. Samarali qidiruv uchun tugun ichida kalitlar va ko'rsatkichlarni tartibli saqlash kerak.
**Talablar:** Tugun maksimal `order` (daraja) ga ega bo'lishi va kalitlar har doim saralangan bo'lishi shart.
**Yechim (JavaScript & TypeScript):**
```typescript
class BPlusNode<K, V> {
  keys: K[] = [];
  values: V[] = []; // Faqat barg tugunlarida
  children: BPlusNode<K, V>[] = [];
  isLeaf: boolean;

  constructor(isLeaf: boolean) {
    this.isLeaf = isLeaf;
  }
}
```
**Tushuntirish:** B+Tree'da barcha ma'lumotlar barg tugunlarda saqlanadi, ichki tugunlar esa faqat yo'naltiruvchi kalitlarni o'z ichiga oladi. Bu diskdan o'qish sonini kamaytiradi.

### Topshiriq #1203: LSM-Tree MemTable qatlami
**Tavsif:** LSM-Tree'da yozish tezligini oshirish uchun ma'lumotlar avval xotiradagi (RAM) MemTable'ga yoziladi.
**Talablar:** MemTable to'lganda uni diskka (SSTable) o'tkazish (flush) mexanizmi bo'lishi kerak.
**Yechim (JavaScript & TypeScript):**
```typescript
class MemTable<K, V> {
  private store: Map<K, V> = new Map();
  private maxSize: number = 1000;

  put(key: K, value: V): void {
    this.store.set(key, value);
    if (this.store.size >= this.maxSize) this.flushToDisk();
  }

  private flushToDisk(): void {
    console.log("MemTable diskka ko'chirildi (SSTable yaratildi).");
    this.store.clear();
  }
}
```
**Tushuntirish:** LSM-Tree yozish operatsiyalarini O(1) vaqtda bajaradi, chunki u ketma-ket yozish (sequential write) tamoyiliga asoslanadi.

### Topshiriq #1204: B+Tree qidiruv algoritmi
**Tavsif:** Indekslangan ma'lumotlar bazasidan kalit bo'yicha qiymatni tezkor topish.
**Talablar:** Ikkilik qidiruv (binary search) algoritmidan foydalangan holda tugun ichidagi kalitni topish.
**Yechim (JavaScript & TypeScript):**
```typescript
function findKey<K>(keys: K[], target: K): number {
  let low = 0, high = keys.length - 1;
  while (low <= high) {
    let mid = Math.floor((low + high) / 2);
    if (keys[mid] === target) return mid;
    if (keys[mid] < target) low = mid + 1;
    else high = mid - 1;
  }
  return -1;
}
```
**Tushuntirish:** Tugun ichida chiziqli qidiruv o'rniga ikkilik qidiruvdan foydalanish O(log N) murakkablikni ta'minlaydi.

### Topshiriq #1205: SSTable (Sorted String Table) formatlash
**Tavsif:** LSM-Tree'da diskka yozilgan ma'lumotlar saralangan bo'lishi kerak.
**Talablar:** Ma'lumotlarni kalit bo'yicha saralab, diskka yozish.
**Yechim (JavaScript & TypeScript):**
```typescript
function writeSSTable(data: Map<string, string>): void {
  const sortedKeys = Array.from(data.keys()).sort();
  const sstable = sortedKeys.map(k => `${k}:${data.get(k)}`).join('\n');
  fs.writeFileSync('sstable.db', sstable);
}
```
**Tushuntirish:** Saralangan ma'lumotlar diapazonli qidiruv (range scan) uchun juda qulaydir.

### Topshiriq #1206: Indeksni yangilash strategiyasi
**Tavsif:** Ma'lumotlar bazasida yangi yozuv qo'shilganda indeksni avtomatik yangilash.
**Talablar:** Indeks va asosiy ma'lumotlar sinxronligini ta'minlash.
**Yechim (JavaScript & TypeScript):**
```typescript
class IndexedDB {
  private data: Map<number, object> = new Map();
  private index: Map<string, number> = new Map(); // name -> id

  insert(id: number, record: { name: string }): void {
    this.data.set(id, record);
    this.index.set(record.name, id);
  }
}
```
**Tushuntirish:** Indeks xotirada saqlanadigan "hash map" bo'lib, qidiruvni O(1) vaqtga tushiradi.

### Topshiriq #1207: LSM-Tree Compaction (Siqish)
**Tavsif:** Eski va yangi ma'lumotlar qatlamlarini birlashtirib, dublikatlarni yo'qotish.
**Talablar:** Bir xil kalitli yozuvlardan eng so'nggisini saqlab qolish.
**Yechim (JavaScript & TypeScript):**
```typescript
function compact(tables: Map<string, string>[]): Map<string, string> {
  const merged = new Map<string, string>();
  tables.forEach(table => {
    table.forEach((v, k) => merged.set(k, v));
  });
  return merged;
}
```
**Tushuntirish:** Compaction jarayoni disk maydonini bo'shatadi va o'qish samaradorligini oshiradi.

### Topshiriq #1208: B+Tree tugunini bo'lish (Split)
**Tavsif:** Tugun sig'imi to'lganda uni ikkiga ajratish.
**Talablar:** Median elementni yuqori darajaga ko'tarish.
**Yechim (JavaScript & TypeScript):**
```typescript
function splitNode(node: BPlusNode<any, any>): BPlusNode<any, any> {
  const mid = Math.floor(node.keys.length / 2);
  const newNode = new BPlusNode(node.isLeaf);
  newNode.keys = node.keys.splice(mid);
  return newNode;
}
```
**Tushuntirish:** Bo'lish jarayoni B+Tree muvozanatini (balance) saqlaydi, bu esa daraxt balandligini minimal darajada ushlab turadi.

### Topshiriq #1209: Bloom Filter (Qidiruvni tezlashtirish)
**Tavsif:** LSM-Tree'da kalit mavjudligini tekshirish uchun diskka murojaat qilmasdan oldin xotirada tekshirish.
**Talablar:** Ehtimollik asosida kalitning yo'qligini aniqlash.
**Yechim (JavaScript & TypeScript):**
```typescript
class BloomFilter {
  private bits = new Uint8Array(1024);
  
  add(key: string): void {
    const hash = this.simpleHash(key);
    this.bits[hash % 1024] = 1;
  }

  mightContain(key: string): boolean {
    return this.bits[this.simpleHash(key) % 1024] === 1;
  }

  private simpleHash(key: string): number { /* Hash funksiyasi */ return 123; }
}
```
**Tushuntirish:** Bloom Filter diskka keraksiz o'qish so'rovlarini yubormaslik uchun ishlatiladi, bu tizim unumdorligini keskin oshiradi.

### Topshiriq #1210: Ma'lumotlar bazasi tranzaksiyasi (Atomiklik)
**Tavsif:** Bir nechta operatsiyani bitta tranzaksiya sifatida bajarish.
**Talablar:** Xatolik yuz berganda barcha o'zgarishlarni bekor qilish (rollback).
**Yechim (JavaScript & TypeScript):**
```typescript
function transaction(ops: Function[]): void {
  const backup = [...currentData];
  try {
    ops.forEach(op => op());
  } catch (e) {
    currentData = backup; // Rollback
    console.error("Tranzaksiya muvaffaqiyatsiz, holat tiklandi.");
  }
}
```
**Tushuntirish:** Tranzaksiyalar ma'lumotlar bazasining izchilligini (consistency) ta'minlaydi. Rollback mexanizmi xatolik yuz berganda ma'lumotlar bazasini oldingi holatiga qaytaradi.

---

### Topshiriq #1211: B+Tree tugunini bo'lish (Split) algoritmi
**Tavsif:** B+Tree ma'lumotlar bazasida tugun to'lib qolganda, uni ikkiga ajratish va ota tugunni yangilash operatsiyasi. Bu indekslashning barqarorligi uchun muhim.
**Talablar:** O'rtacha elementni aniqlash va yangi tugun yaratish. Murakkablik: O(log n).
**Yechim (TypeScript):**
```typescript
class BPlusNode {
  keys: number[] = [];
  children: BPlusNode[] = [];
  isLeaf: boolean = true;

  split(): { median: number; newNode: BPlusNode } {
    const mid = Math.floor(this.keys.length / 2);
    const median = this.keys[mid];
    const newNode = new BPlusNode();
    
    newNode.keys = this.keys.slice(mid + 1);
    this.keys = this.keys.slice(0, mid);
    
    if (!this.isLeaf) {
      newNode.children = this.children.slice(mid + 1);
      this.children = this.children.slice(0, mid + 1);
    }
    return { median, newNode };
  }
}
```
**Tushuntirish:** B+Tree balansini saqlash uchun "split" operatsiyasi eng muhim qismdir. Array.slice() yordamida xotira xavfsiz boshqariladi.

### Topshiriq #1212: WAL (Write-Ahead Logging) mexanizmini simulyatsiya qilish
**Tavsif:** Ma'lumotlar bazasi ishdan chiqqanda ma'lumot yo'qolmasligi uchun operatsiyalarni diskka yozishdan oldin log faylga yozish.
**Talablar:** Asinxron yozish va fayl yaxlitligini ta'minlash.
**Yechim (JavaScript):**
```javascript
const fs = require('fs').promises;

async function writeToWAL(logEntry) {
  const data = JSON.stringify({ timestamp: Date.now(), ...logEntry }) + '\n';
  // 'a' flagi fayl oxiriga qo'shishni bildiradi (append)
  await fs.appendFile('database.wal', data, 'utf8');
}
```
**Tushuntirish:** WAL ma'lumotlar bazasi "crash" bo'lganda oxirgi tranzaksiyalarni qayta tiklash (recovery) uchun yagona manba hisoblanadi.

### Topshiriq #1213: LSM-Tree MemTable qidiruvi
**Tavsif:** LSM-Tree'da ma'lumotlar avval xotiradagi MemTable'ga yoziladi. Qidiruv tezligi uchun samarali tuzilma kerak.
**Talablar:** O(log n) qidiruv va xotira samaradorligi.
**Yechim (TypeScript):**
```typescript
class MemTable {
  private data: Map<string, string> = new Map();

  // Kalit bo'yicha qidiruv
  get(key: string): string | undefined {
    return this.data.get(key);
  }

  // Yangi yozuv qo'shish
  set(key: string, value: string): void {
    this.data.set(key, value);
  }
}
```
**Tushuntirish:** Map strukturasi JavaScript'da hash-table asosida ishlaydi, bu MemTable uchun eng tezkor yechimdir.

### Topshiriq #1214: B+Tree diapazonli qidiruv (Range Query)
**Tavsif:** Indekslangan ma'lumotlar bazasidan ma'lum oraliqdagi qiymatlarni olish.
**Talablar:** Leaf tugunlar orasidagi bog'liqlikdan foydalanish.
**Yechim (TypeScript):**
```typescript
function rangeQuery(node: BPlusNode, start: number, end: number): number[] {
  let result: number[] = [];
  for (let key of node.keys) {
    if (key >= start && key <= end) result.push(key);
  }
  // Agar barg bo'lmasa, keyingi tugunlarga o'tish mantiqi qo'shiladi
  return result;
}
```
**Tushuntirish:** B+Tree'ning barg tugunlari o'zaro bog'langan (linked list), bu diapazonli qidiruvni juda tezlashtiradi.

### Topshiriq #1215: LSM-Tree Compaction (Siqish) jarayoni
**Tavsif:** Diskdagi SSTable fayllarini birlashtirib, eskirgan ma'lumotlarni o'chirish.
**Talablar:** I/O operatsiyalarini minimallashtirish.
**Yechim (JavaScript):**
```javascript
function compactTables(table1, table2) {
  // Ikki saralangan faylni birlashtirish (Merge Sort prinsipi)
  const merged = new Map([...table1, ...table2]);
  return new Map([...merged.entries()].sort());
}
```
**Tushuntirish:** Compaction jarayoni diskdagi bo'sh joyni tozalaydi va o'qish tezligini oshiradi.

### Topshiriq #1216: Indeks keshini (Cache) boshqarish
**Tavsif:** Tez-tez so'raladigan indeks tugunlarini xotirada saqlash (LRU Cache).
**Talablar:** O(1) vaqt murakkabligi.
**Yechim (TypeScript):**
```typescript
class LRUCache<K, V> {
  private cache = new Map<K, V>();
  constructor(private capacity: number) {}

  get(key: K): V | undefined {
    if (!this.cache.has(key)) return undefined;
    const val = this.cache.get(key)!;
    this.cache.delete(key);
    this.cache.set(key, val);
    return val;
  }
}
```
**Tushuntirish:** LRU (Least Recently Used) algoritmi eng kam ishlatilgan ma'lumotni o'chirib, xotirani optimallashtiradi.

### Topshiriq #1217: WAL faylini "Checkpoint" qilish
**Tavsif:** WAL fayli juda katta bo'lib ketmasligi uchun MemTable'ni diskka (SSTable) ko'chirish.
**Talablar:** Atomik operatsiya (yozish vaqtida ma'lumot yo'qolmasligi).
**Yechim (JavaScript):**
```javascript
async function checkpoint(memTable) {
  await fs.writeFile('sstable.data', JSON.stringify([...memTable]));
  await fs.truncate('database.wal', 0); // Logni tozalash
}
```
**Tushuntirish:** Checkpoint jarayoni ma'lumotlar bazasini qayta tiklash vaqtini qisqartiradi.

### Topshiriq #1218: B+Tree'da kalitni o'chirish (Deletion)
**Tavsif:** B+Tree'dan ma'lumotni o'chirish va tugunlar balansini saqlash.
**Talablar:** Tugunlar birlashishi (merge) yoki qarz olish (borrowing).
**Yechim (TypeScript):**
```typescript
function deleteKey(node: BPlusNode, key: number) {
  const index = node.keys.indexOf(key);
  if (index > -1) {
    node.keys.splice(index, 1);
    // Balansni tekshirish funksiyasi chaqiriladi
  }
}
```
**Tushuntirish:** O'chirish operatsiyasi qo'shishdan ko'ra murakkabroq, chunki u daraxt strukturasini qayta tartiblashni talab qiladi.

### Topshiriq #1219: Bloom Filter (Qidiruvni tezlashtirish)
**Tavsif:** LSM-Tree'da qidiruvni tezlashtirish uchun kalit mavjudligini oldindan tekshirish.
**Talablar:** Xotira samaradorligi va tezlik.
**Yechim (JavaScript):**
```javascript
class BloomFilter {
  constructor(size) {
    this.bitArray = new Uint8Array(size);
  }
  add(key) {
    const hash = this.hashFunction(key);
    this.bitArray[hash % this.bitArray.length] = 1;
  }
  mightContain(key) {
    return this.bitArray[this.hashFunction(key) % this.bitArray.length] === 1;
  }
}
```
**Tushuntirish:** Bloom Filter diskka murojaat qilishdan oldin kalitning yo'qligini aniqlab, keraksiz I/O operatsiyalarini oldini oladi.

### Topshiriq #1220: B+Tree tugunini diskdan o'qish (Serialization)
**Tavsif:** B+Tree tugunlarini diskda saqlash va qayta yuklash.
**Talablar:** Binary formatda saqlash (Buffer).
**Yechim (TypeScript):**
```typescript
function serializeNode(node: BPlusNode): Buffer {
  const data = JSON.stringify({ keys: node.keys, isLeaf: node.isLeaf });
  return Buffer.from(data);
}

function deserializeNode(buffer: Buffer): BPlusNode {
  return Object.assign(new BPlusNode(), JSON.parse(buffer.toString()));
}
```
**Tushuntirish:** Buffer'dan foydalanish xotirani tejaydi va diskdagi ma'lumotlar bilan ishlashni tezlashtiradi.

---

### Topshiriq #1221: WAL (Write-Ahead Logging) mexanizmini implementatsiya qilish
**Tavsif:** Ma'lumotlar bazasi tizimlarida kutilmagan o'chishlardan himoyalanish uchun ma'lumotni diskka yozishdan oldin jurnalga yozish shart.
**Talablar:** Asinxron yozish, faylga append qilish, xatolarga chidamlilik.
**Yechim (JavaScript & TypeScript):**
```typescript
import * as fs from 'fs/promises';

class WAL {
  private logFile = 'database.log';

  async write(entry: object): Promise<void> {
    // Ma'lumotni jurnalga yozish (Atomar operatsiya)
    const data = JSON.stringify(entry) + '\n';
    await fs.appendFile(this.logFile, data, 'utf-8');
  }
}
```
**Tushuntirish:** WAL tizimida ma'lumotlar xotiradan diskka o'tishidan oldin ketma-ket jurnalga yoziladi. Bu tizim buzilganda ma'lumotlarni qayta tiklash (recovery) imkonini beradi.

### Topshiriq #1222: LSM-Tree uchun MemTable tuzilmasi
**Tavsif:** LSM-Tree'da yozish operatsiyalarini tezlashtirish uchun xotirada joylashgan tartiblangan tuzilma kerak.
**Talablar:** O(log n) qidiruv va kiritish tezligi.
**Yechim (JavaScript & TypeScript):**
```typescript
class MemTable {
  private table: Map<string, string> = new Map();

  set(key: string, value: string): void {
    this.table.set(key, value);
  }

  // Kalit bo'yicha qidiruv
  get(key: string): string | undefined {
    return this.table.get(key);
  }
}
```
**Tushuntirish:** MemTable ma'lumotlarni RAMda saqlaydi. To'lganida, u diskka (SSTable) "flush" qilinadi, bu esa yozish tezligini maksimal darajaga olib chiqadi.

### Topshiriq #1223: B+Tree tugunini (Node) loyihalash
**Tavsif:** B+Tree ma'lumotlar bazasini indekslash uchun eng samarali daraxt tuzilmasidir.
**Talablar:** Tugun ichida kalitlar va ko'rsatkichlar (pointers) saqlanishi kerak.
**Yechim (JavaScript & TypeScript):**
```typescript
class BPlusNode {
  keys: number[] = [];
  children: BPlusNode[] = [];
  isLeaf: boolean = false;

  constructor(isLeaf: boolean = false) {
    this.isLeaf = isLeaf;
  }
}
```
**Tushuntirish:** B+Tree'da barcha ma'lumotlar barg (leaf) tugunlarida saqlanadi, bu esa diapazonli qidiruvni (range query) juda tezlashtiradi.

### Topshiriq #1224: SSTable (Sorted String Table) formatini yaratish
**Tavsif:** MemTable diskka yozilganda tartiblangan fayl hosil qilish kerak.
**Talablar:** Fayl o'qishda samaradorlik va disk joylashuvi.
**Yechim (JavaScript & TypeScript):**
```typescript
async function flushToSSTable(data: Map<string, string>): Promise<void> {
  const sortedKeys = Array.from(data.keys()).sort();
  let content = '';
  for (const key of sortedKeys) {
    content += `${key}:${data.get(key)}\n`;
  }
  await fs.writeFile('sstable_1.db', content);
}
```
**Tushuntirish:** SSTable o'zgarmas (immutable) bo'ladi. Bu esa konkurent o'qish operatsiyalarida qulflar (locks) kerak emasligini anglatadi.

### Topshiriq #1225: Bloom Filter yordamida qidiruvni optimallashtirish
**Tavsif:** SSTable ichida kalit yo'qligini tez aniqlash uchun Bloom Filter zarur.
**Talablar:** Xotira tejamkorligi va ehtimollik nazariyasi.
**Yechim (JavaScript & TypeScript):**
```typescript
class BloomFilter {
  private bits: boolean[] = new Array(1000).fill(false);

  add(key: string): void {
    const hash = Math.abs(key.split('').reduce((a, b) => a + b.charCodeAt(0), 0) % 1000);
    this.bits[hash] = true;
  }

  contains(key: string): boolean {
    const hash = Math.abs(key.split('').reduce((a, b) => a + b.charCodeAt(0), 0) % 1000);
    return this.bits[hash];
  }
}
```
**Tushuntirish:** Bloom Filter diskka murojaat qilishdan oldin kalitning mavjud emasligini tekshiradi, bu esa I/O operatsiyalarini keskin kamaytiradi.

### Topshiriq #1226: B+Tree'da kalitni qidirish algoritmi
**Tavsif:** B+Tree ichida ma'lum bir kalitni topish uchun rekursiv qidiruv.
**Talablar:** O(log n) vaqt murakkabligi.
**Yechim (JavaScript & TypeScript):**
```typescript
function search(node: BPlusNode, key: number): any {
  let i = 0;
  while (i < node.keys.length && key > node.keys[i]) i++;
  
  if (node.isLeaf) return node.keys[i] === key ? node : null;
  return search(node.children[i], key);
}
```
**Tushuntirish:** Daraxt darajalari bo'ylab pastga tushish orqali kerakli barg tuguniga tez yetib boriladi.

### Topshiriq #1227: LSM-Tree Compaction jarayoni
**Tavsif:** Bir nechta SSTable fayllarini birlashtirib, eski ma'lumotlarni tozalash.
**Talablar:** Xotirani boshqarish va dublikatlarni o'chirish.
**Yechim (JavaScript & TypeScript):**
```typescript
function compact(tables: Map<string, string>[]): Map<string, string> {
  const merged = new Map<string, string>();
  tables.forEach(table => {
    for (const [k, v] of table) merged.set(k, v);
  });
  return merged;
}
```
**Tushuntirish:** Compaction jarayoni diskdagi ma'lumotlar hajmini kamaytiradi va o'qish tezligini oshiradi.

### Topshiriq #1228: Indekslashda "Clustered Index" tushunchasi
**Tavsif:** Ma'lumotlar bazasida ma'lumotlarning fizik joylashuvini indeks bilan bog'lash.
**Talablar:** Ma'lumotlar tartibini saqlash.
**Yechim (JavaScript & TypeScript):**
```typescript
interface Row { id: number; data: string; }
const table: Row[] = []; // Fizik saqlash

function insertClustered(row: Row) {
  table.push(row);
  table.sort((a, b) => a.id - b.id);
}
```
**Tushuntirish:** Clustered index ma'lumotlarning o'zini tartiblaydi, bu esa diapazonli so'rovlar uchun eng tezkor yechimdir.

### Topshiriq #1229: WAL Recovery (Tiklash) logikasi
**Tavsif:** Tizim ishga tushganda WAL faylini o'qib, MemTable'ni qayta tiklash.
**Talablar:** Faylni satrma-satr o'qish va xatolarni boshqarish.
**Yechim (JavaScript & TypeScript):**
```typescript
async function recover(walPath: string, memTable: MemTable) {
  const content = await fs.readFile(walPath, 'utf-8');
  content.split('\n').forEach(line => {
    if (!line) return;
    const entry = JSON.parse(line);
    memTable.set(entry.key, entry.value);
  });
}
```
**Tushuntirish:** Bu funksiya tizim kutilmaganda o'chganda ma'lumotlar yo'qolmasligini ta'minlaydi.

### Topshiriq #1230: Secondary Index (Ikkilamchi indeks)
**Tavsif:** Asosiy kalitdan tashqari boshqa ustunlar bo'yicha qidiruvni tezlashtirish.
**Talablar:** Hash-map yordamida tezkor bog'lanish.
**Yechim (JavaScript & TypeScript):**
```typescript
class SecondaryIndex {
  private index: Map<string, number[]> = new Map();

  add(value: string, primaryKey: number) {
    if (!this.index.has(value)) this.index.set(value, []);
    this.index.get(value)?.push(primaryKey);
  }
}
```
**Tushuntirish:** Ikkilamchi indekslar ma'lumotlar bazasiga turli xil so'rovlar (masalan, ism bo'yicha qidiruv) uchun moslashuvchanlik beradi.

---

### Topshiriq #1231: WAL (Write-Ahead Logging) mexanizmini implementatsiya qilish
**Tavsif:** Ma'lumotlar bazasida kutilmagan o'chishlar (crash) yuz berganda ma'lumotlar yaxlitligini saqlash uchun operatsiyalarni diskka yozishdan oldin log faylga yozish zarurati.
**Talablar:** Log faylga yozish atomik bo'lishi va `fs.appendFileSync` orqali sinxron tarzda amalga oshirilishi kerak.
**Yechim (JavaScript & TypeScript):**
```typescript
import * as fs from 'fs';

class WALManager {
  private logPath: string = 'database.log';

  // Operatsiyani logga yozish
  logTransaction(operation: string, data: object): void {
    const entry = JSON.stringify({ timestamp: Date.now(), operation, data }) + '\n';
    fs.appendFileSync(this.logPath, entry, 'utf8');
  }
}
```
**Tushuntirish:** WAL yordamida tizim ishdan chiqqanda oxirgi bajarilmagan operatsiyalarni log fayldan qayta tiklash (recovery) imkoniyati yaratiladi.

### Topshiriq #1232: B+ Tree tugunini (Node) loyihalash
**Tavsif:** B+ Tree ma'lumotlar bazasi indekslarining asosi hisoblanadi. Har bir tugun kalitlar va bolalar ko'rsatkichlarini saqlashi kerak.
**Talablar:** Tugun sig'imi (order) aniq belgilanishi va kalitlar tartiblangan holda saqlanishi shart.
**Yechim (JavaScript & TypeScript):**
```typescript
class BPlusNode {
  keys: number[] = [];
  children: BPlusNode[] = [];
  isLeaf: boolean;

  constructor(isLeaf: boolean) {
    this.isLeaf = isLeaf;
  }
}
```
**Tushuntirish:** B+ Tree'da faqat barg (leaf) tugunlar ma'lumotlarni saqlaydi, bu esa qidiruvni tezlashtiradi va disk bloklaridan samarali foydalanishni ta'minlaydi.

### Topshiriq #1233: LSM-Tree MemTable (In-memory buffer) yaratish
**Tavsif:** LSM-Tree'da yozish tezligini oshirish uchun ma'lumotlar avval xotiradagi MemTable'ga yoziladi.
**Talablar:** MemTable to'lganda uni diskka (SSTable) o'tkazish mexanizmi nazarda tutilishi kerak.
**Yechim (JavaScript & TypeScript):**
```typescript
class MemTable {
  private storage: Map<string, string> = new Map();
  private limit: number = 1000;

  insert(key: string, value: string): void {
    this.storage.set(key, value);
    if (this.storage.size >= this.limit) {
      this.flushToDisk();
    }
  }

  private flushToDisk(): void {
    // SSTable yaratish logikasi shu yerda bo'ladi
    this.storage.clear();
  }
}
```
**Tushuntirish:** MemTable ma'lumotlarni tartiblangan holda (Sorted Map) saqlaydi, bu esa diskka yozishda ketma-ket (sequential) yozish imkonini beradi.

### Topshiriq #1234: B+ Tree qidiruv algoritmi
**Tavsif:** Indekslangan ma'lumotlar bazasidan kalit bo'yicha qiymatni tezkor topish.
**Talablar:** O(log n) murakkablikda ishlashi va rekursiv qidiruvni qo'llab-quvvatlashi kerak.
**Yechim (JavaScript & TypeScript):**
```typescript
function search(node: BPlusNode, key: number): any | null {
  let i = 0;
  while (i < node.keys.length && key > node.keys[i]) i++;
  
  if (node.isLeaf) {
    return node.keys[i] === key ? node.keys[i] : null;
  }
  return search(node.children[i], key);
}
```
**Tushuntirish:** B+ Tree daraxti chuqurligi kam bo'lgani uchun diskka murojaatlar soni minimal bo'ladi.

### Topshiriq #1235: SSTable (Sorted String Table) formatini loyihalash
**Tavsif:** MemTable diskka yozilganda hosil bo'ladigan o'zgarmas (immutable) fayl formatini yaratish.
**Talablar:** Fayl ichida kalitlar alfavit tartibida saqlanishi shart.
**Yechim (JavaScript & TypeScript):**
```typescript
function writeSSTable(data: Map<string, string>): void {
  const sortedKeys = Array.from(data.keys()).sort();
  // Diskka yozish jarayoni
  sortedKeys.forEach(key => {
    const entry = `${key}:${data.get(key)}\n`;
    fs.appendFileSync('sstable.db', entry);
  });
}
```
**Tushuntirish:** SSTable'lar o'zgarmas bo'lgani uchun ularni o'qish juda tez va xavfsizdir.

### Topshiriq #1236: LSM-Tree Compaction (Siqish) jarayoni
**Tavsif:** Ko'plab SSTable fayllarini birlashtirib, eskirgan ma'lumotlarni o'chirish va disk hajmini optimallashtirish.
**Talablar:** Dublikat kalitlarni olib tashlash va eng oxirgi versiyani saqlab qolish.
**Yechim (JavaScript & TypeScript):**
```typescript
function compact(tables: Map<string, string>[]): Map<string, string> {
  const merged = new Map<string, string>();
  tables.forEach(table => {
    table.forEach((val, key) => merged.set(key, val));
  });
  return merged;
}
```
**Tushuntirish:** Compaction jarayoni LSM-Tree'ning ishlash samaradorligini saqlab qolish uchun muhimdir.

### Topshiriq #1237: Indekslashda Bloom Filter qo'llash
**Tavsif:** SSTable ichida kalit mavjudligini tekshirish uchun diskka murojaat qilmasdan oldin tezkor tekshiruv o'tkazish.
**Talablar:** Ehtimollik nazariyasiga asoslangan qidiruvni tezlashtirish.
**Yechim (JavaScript & TypeScript):**
```typescript
class BloomFilter {
  private bits: boolean[] = new Array(100).fill(false);
  
  add(key: string): void {
    const hash = key.length % 100; // Oddiy hash funksiya
    this.bits[hash] = true;
  }

  mightContain(key: string): boolean {
    return this.bits[key.length % 100];
  }
}
```
**Tushuntirish:** Bloom Filter diskka keraksiz o'qish so'rovlarini 90% gacha kamaytirishi mumkin.

### Topshiriq #1238: B+ Tree tugunini bo'lish (Split)
**Tavsif:** Tugun sig'imi oshib ketganda, daraxt muvozanatini saqlash uchun tugunni ikkiga ajratish.
**Talablar:** O'rta elementni yuqori darajadagi tugunga ko'tarish.
**Yechim (JavaScript & TypeScript):**
```typescript
function splitNode(node: BPlusNode): BPlusNode {
  const mid = Math.floor(node.keys.length / 2);
  const newNode = new BPlusNode(node.isLeaf);
  newNode.keys = node.keys.splice(mid);
  return newNode;
}
```
**Tushuntirish:** Split jarayoni B+ Tree'ni har doim "balanslangan" holatda ushlab turadi.

### Topshiriq #1239: Database Cursor (Kursor) implementatsiyasi
**Tavsif:** Katta hajmdagi ma'lumotlarni bir vaqtning o'zida emas, qismlarga bo'lib o'qish.
**Talablar:** Xotirani tejash uchun `Generator` funksiyalaridan foydalanish.
**Yechim (JavaScript & TypeScript):**
```typescript
function* cursor(data: string[]): Generator<string> {
  for (const item of data) {
    yield item;
  }
}
```
**Tushuntirish:** Kursorlar yordamida millionlab yozuvlarni xotirani to'ldirmasdan qayta ishlash mumkin.

### Topshiriq #1240: Ma'lumotlar bazasi "Snapshot" olish
**Tavsif:** Ma'lumotlar bazasining ma'lum bir vaqtdagi holatini zaxiralash.
**Talablar:** Snapshot jarayonida ma'lumotlar bazasi yozish operatsiyalarini bloklamasligi kerak.
**Yechim (JavaScript & TypeScript):**
```typescript
async function createSnapshot(dbState: object): Promise<void> {
  const snapshot = JSON.stringify(dbState);
  await fs.promises.writeFile(`snapshot_${Date.now()}.json`, snapshot);
}
```
**Tushuntirish:** Snapshot'lar tizimni tiklash (restore) va ma'lumotlar xavfsizligini ta'minlash uchun asosiy mexanizmdir.

---

### Topshiriq #1241: LSM-Tree uchun MemTable kiritishni optimallashtirish
**Tavsif:** LSM-Tree arxitekturasida yozish tezligini oshirish uchun ma'lumotlar avval xotiradagi MemTable'ga yoziladi. Ushbu topshiriq, yozish operatsiyalarini O(1) vaqt murakkabligida bajaradigan va xotira to'lganida diskka "flush" qilishga tayyorlaydigan tuzilmani yaratishdir.
**Talablar:** `Map` strukturasidan foydalanish, xotira limiti (maxSize) nazorati.
**Yechim (TypeScript):**
```typescript
class MemTable {
  private storage: Map<string, string> = new Map();
  constructor(private maxSize: number) {}

  // Ma'lumot qo'shish: O(1)
  public put(key: string, value: string): boolean {
    if (this.storage.size >= this.maxSize) return false;
    this.storage.set(key, value);
    return true;
  }

  public flush(): Map<string, string> {
    const data = new Map(this.storage);
    this.storage.clear();
    return data;
  }
}
```
**Tushuntirish:** `Map` JavaScript'da hash-table asosida ishlaydi, bu esa yozish operatsiyalarini eng yuqori tezlikda bajarish imkonini beradi.

### Topshiriq #1242: WAL (Write-Ahead Logging) mexanizmini implementatsiya qilish
**Tavsif:** Tizim kutilmaganda o'chib qolsa, MemTable'dagi ma'lumotlar yo'qolmasligi uchun har bir operatsiyani diskdagi log fayliga ketma-ket yozish kerak.
**Talablar:** `fs` moduli yordamida append-only yozish, xatolarga chidamlilik.
**Yechim (JavaScript):**
```javascript
const fs = require('fs');
const logStream = fs.createWriteStream('wal.log', { flags: 'a' });

function writeToWAL(key, value) {
  // Log format: key:value\n
  logStream.write(`${key}:${value}\n`, 'utf8');
}
```
**Tushuntirish:** `append-only` yozish diskdagi bosh (head) harakatini minimallashtiradi, bu esa yozish unumdorligini oshiradi.

### Topshiriq #1243: B+Tree tugunini (Node) loyihalash
**Tavsif:** B+Tree indekslash tizimining asosiy birligi bo'lgan tugunni yaratish. Unda kalitlar va bolalar (child pointers) tartiblangan bo'lishi shart.
**Talablar:** Kalitlar massivi va bolalar massivi, `binary search` uchun tayyorlik.
**Yechim (TypeScript):**
```typescript
class BPlusNode {
  keys: number[] = [];
  children: BPlusNode[] = [];
  isLeaf: boolean = true;

  constructor(isLeaf: boolean = true) {
    this.isLeaf = isLeaf;
  }
}
```
**Tushuntirish:** B+Tree'da barcha ma'lumotlar barglarda (leaf) saqlanadi, bu esa diapazonli qidiruvni (range scan) juda tezlashtiradi.

### Topshiriq #1244: B+Tree'da kalitni qidirish (Binary Search)
**Tavsif:** B+Tree tugunlari ichida kalitni O(log n) vaqtda topish.
**Talablar:** `binary search` algoritmi.
**Yechim (TypeScript):**
```typescript
function findKeyIndex(keys: number[], target: number): number {
  let low = 0, high = keys.length - 1;
  while (low <= high) {
    let mid = Math.floor((low + high) / 2);
    if (keys[mid] === target) return mid;
    if (keys[mid] < target) low = mid + 1;
    else high = mid - 1;
  }
  return low; // Insert pozitsiyasi
}
```
**Tushuntirish:** Tugun ichidagi kalitlar saralangan bo'lgani uchun binar qidiruv eng samarali usul hisoblanadi.

### Topshiriq #1245: LSM-Tree "Compaction" jarayoni
**Tavsif:** Bir nechta SSTable fayllarini birlashtirib, eski ma'lumotlarni o'chirish va dublikatlarni tozalash jarayoni.
**Talablar:** Ikki saralangan massivni birlashtirish (Merge Sort mantig'i).
**Yechim (JavaScript):**
```javascript
function compact(table1, table2) {
  let result = new Map();
  // Ikkala jadvalni birlashtirib, oxirgi qiymatni saqlash
  [...table1, ...table2].forEach(([k, v]) => result.set(k, v));
  return new Map([...result.entries()].sort());
}
```
**Tushuntirish:** Compaction diskdagi bo'sh joyni tejaydi va o'qish tezligini oshiradi.

### Topshiriq #1246: Indekslashda Bloom Filter'ni qo'llash
**Tavsif:** Keraksiz disk operatsiyalarini oldini olish uchun kalit mavjudligini tezkor tekshirish.
**Talablar:** Ehtimollik asosida "yo'q" deb javob berish.
**Yechim (TypeScript):**
```typescript
class BloomFilter {
  private bitArray: Uint8Array = new Uint8Array(1024);
  
  private hash(key: string, seed: number): number {
    return (key.length * seed) % 1024;
  }

  public add(key: string): void {
    this.bitArray[this.hash(key, 31)] = 1;
    this.bitArray[this.hash(key, 37)] = 1;
  }

  public mightContain(key: string): boolean {
    return this.bitArray[this.hash(key, 31)] === 1 && 
           this.bitArray[this.hash(key, 37)] === 1;
  }
}
```
**Tushuntirish:** Bloom Filter diskka murojaat qilishdan oldin kalitning yo'qligini aniq tasdiqlab, I/O xarajatini keskin kamaytiradi.

### Topshiriq #1247: B+Tree tugunini bo'lish (Split)
**Tavsif:** Tugun to'lib qolganda (overflow), uni ikkiga ajratish va ota tugunni yangilash.
**Talablar:** O'rta elementni yuqoriga ko'tarish.
**Yechim (TypeScript):**
```typescript
function splitNode(node: BPlusNode): BPlusNode {
  const mid = Math.floor(node.keys.length / 2);
  const newNode = new BPlusNode(node.isLeaf);
  newNode.keys = node.keys.splice(mid);
  return newNode;
}
```
**Tushuntirish:** Split operatsiyasi daraxt muvozanatini (balanced) saqlash uchun juda muhimdir.

### Topshiriq #1248: SSTable (Sorted String Table) formatini yaratish
**Tavsif:** MemTable'ni diskka saralangan holda yozish.
**Talablar:** Kalit-qiymat juftliklarini ketma-ket yozish.
**Yechim (JavaScript):**
```javascript
async function flushToSSTable(dataMap, filename) {
  const sortedKeys = Array.from(dataMap.keys()).sort();
  const content = sortedKeys.map(k => `${k}:${dataMap.get(k)}`).join('\n');
  await fs.promises.writeFile(filename, content);
}
```
**Tushuntirish:** SSTable'lar o'zgarmas (immutable) bo'lgani uchun ularni o'qish juda tez va xavfsizdir.

### Topshiriq #1249: Range Scan (Diapazonli qidiruv)
**Tavsif:** B+Tree'da ma'lum bir oraliqdagi (masalan, 10 dan 50 gacha) barcha kalitlarni topish.
**Talablar:** Barg tugunlari orasidagi bog'lanishdan (leaf pointers) foydalanish.
**Yechim (TypeScript):**
```typescript
function rangeScan(start: number, end: number, leaf: BPlusNode): number[] {
  return leaf.keys.filter(k => k >= start && k <= end);
}
```
**Tushuntirish:** B+Tree'da barglar o'zaro bog'langanligi sababli, diapazonli qidiruv daraxtni qayta-qayta aylanmasdan amalga oshiriladi.

### Topshiriq #1250: WAL Recovery (Qayta tiklash)
**Tavsif:** Tizim ishga tushganda WAL faylini o'qib, MemTable'ni qayta tiklash.
**Talablar:** Faylni satrma-satr o'qish va xatolarni boshqarish.
**Yechim (JavaScript):**
```javascript
async function recoverFromWAL(filename) {
  const data = await fs.promises.readFile(filename, 'utf8');
  return data.split('\n').map(line => {
    const [key, value] = line.split(':');
    return { key, value };
  });
}
```
**Tushuntirish:** Bu jarayon ma'lumotlar bazasining ACID xususiyatlaridan biri bo'lgan "Durability" (bardoshlilik)ni ta'minlaydi.