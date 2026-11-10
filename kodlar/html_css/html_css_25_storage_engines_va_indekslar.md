# Khorazmiy AI: HTML & CSS - Modul 25
## Mavzu: Ma'lumotlar bazasi ichki tuzilishi: LSM-Trees, B+Trees, WAL va Indekslash

### Topshiriq #1201: B+Tree Indeks Vizualizatsiyasi
**Tavsif:** Ma'lumotlar bazasidagi B+Tree indekslarining ierarxik tuzilishini tushunish uchun interaktiv vizualizatsiya komponentini yaratish.
**Talablar:** CSS Grid yordamida tugunlar (nodes) orasidagi bog'liqlikni ko'rsatish, o'lchov birligi sifatida `rem` dan foydalanish.
**Yechim (HTML & CSS):**
```html
<div class="b-tree-container">
  <div class="node root">Root: [10, 20]</div>
  <div class="node-children">
    <div class="node leaf">Leaf: [10, 15]</div>
    <div class="node leaf">Leaf: [16, 20]</div>
  </div>
</div>
<style>
  .b-tree-container { display: grid; justify-content: center; gap: 2rem; }
  .node { padding: 1rem; border: 2px solid #2c3e50; border-radius: 8px; background: #ecf0f1; }
  .node-children { display: flex; gap: 1rem; }
</style>
```
**Tushuntirish:** B+Tree tuzilishini vizualizatsiya qilishda `flex` va `grid` kombinatsiyasi ma'lumotlar darajalarini aniq ko'rsatishga yordam beradi.

### Topshiriq #1202: WAL (Write-Ahead Logging) Holat Indikatori
**Tavsif:** WAL jarayonining "yozish" va "tasdiqlash" bosqichlarini foydalanuvchi interfeysida real vaqtda ko'rsatish.
**Talablar:** CSS animatsiyalari yordamida log yozish jarayonini simulyatsiya qilish.
**Yechim (HTML & CSS):**
```html
<div class="wal-log">
  <div class="status-bar"></div>
  <span>WAL Yozilmoqda...</span>
</div>
<style>
  .status-bar { width: 0; height: 10px; background: #3498db; animation: progress 2s infinite; }
  @keyframes progress { to { width: 100%; } }
</style>
```
**Tushuntirish:** WAL tizimida ma'lumotlar xavfsizligi uchun yozish jarayoni uzluksiz ekanligini foydalanuvchiga vizual tasdiqlash muhim.

### Topshiriq #1203: LSM-Tree "SSTable" Qatlamlari
**Tavsif:** LSM-Tree tarkibidagi turli darajadagi (L0, L1, L2) SSTable fayllarini vizual guruhlash.
**Talablar:** `z-index` va `opacity` yordamida qatlamlar ierarxiyasini ko'rsatish.
**Yechim (HTML & CSS):**
```html
<div class="lsm-stack">
  <div class="layer l0">L0: MemTable</div>
  <div class="layer l1">L1: SSTable</div>
</div>
<style>
  .lsm-stack { position: relative; }
  .layer { padding: 1rem; border: 1px solid #ccc; margin-bottom: -10px; background: white; }
  .l0 { z-index: 2; opacity: 0.9; }
</style>
```
**Tushuntirish:** LSM-Tree'da ma'lumotlar qatlamlari ustma-ust yozilishi (compaction) jarayonini tushuntirish uchun qatlamli dizayn tanlandi.

### Topshiriq #1204: Indeks Qidiruv Tezligi Indikatori
**Tavsif:** Indekslash qidiruvni qanchalik tezlashtirishini ko'rsatuvchi taqqoslash paneli.
**Talablar:** CSS `transition` xususiyatidan foydalanib, qidiruv vaqtini vizual qisqartirish.
**Yechim (HTML & CSS):**
```html
<div class="search-bar">
  <div class="speed-meter" style="width: 20%;">Indekssiz</div>
  <div class="speed-meter optimized" style="width: 80%;">Indeksli</div>
</div>
<style>
  .speed-meter { height: 20px; transition: width 1s ease-in-out; background: #27ae60; }
  .optimized { background: #e67e22; }
</style>
```
**Tushuntirish:** Indekslashning ishlash samaradorligini foydalanuvchi uchun intuitiv tushunarli qilish uchun o'lchovli bar ishlatildi.

### Topshiriq #1205: B-Tree Tugunlari uchun Konteyner
**Tavsif:** B-Tree tugunlaridagi kalitlar (keys) sonini boshqarish uchun moslashuvchan konteyner.
**Talablar:** `flex-wrap` yordamida tugun ichidagi kalitlarning sig'imini boshqarish.
**Yechim (HTML & CSS):**
```html
<div class="b-node">
  <span class="key">K1</span><span class="key">K2</span><span class="key">K3</span>
</div>
<style>
  .b-node { display: flex; border: 1px solid #000; padding: 5px; width: 100px; flex-wrap: wrap; }
  .key { border: 1px solid #ddd; margin: 2px; padding: 2px; }
</style>
```
**Tushuntirish:** B-Tree tugunlari ma'lum miqdordagi kalitlarni saqlaydi, `flex-wrap` esa tugun to'lib qolganda yangi qatorga o'tishni ta'minlaydi.

### Topshiriq #1206: WAL "Checkpoint" Holati
**Tavsif:** WAL fayllarida "checkpoint" (tekshiruv nuqtasi) olinganligini bildiruvchi UI elementi.
**Talablar:** CSS `box-shadow` yordamida "checkpoint" holatini ajratib ko'rsatish.
**Yechim (HTML & CSS):**
```html
<div class="checkpoint active">Checkpoint: 12:00:00</div>
<style>
  .checkpoint { padding: 10px; border-radius: 5px; border: 1px solid #333; }
  .active { box-shadow: 0 0 10px #2ecc71; background: #f1fcf4; }
</style>
```
**Tushuntirish:** Checkpoint tizimning barqarorligini bildiradi, shuning uchun yashil rang va soyadan foydalanildi.

### Topshiriq #1207: LSM-Tree Compaction Vizualizatsiyasi
**Tavsif:** LSM-Tree'da kichik fayllarning birlashish jarayonini (compaction) ko'rsatish.
**Talablar:** `transform: scale()` yordamida fayllarning birlashish effektini yaratish.
**Yechim (HTML & CSS):**
```html
<div class="compaction-box">
  <div class="file">File A</div>
  <div class="file">File B</div>
</div>
<style>
  .compaction-box:hover .file { transform: scale(0.8); transition: 0.5s; }
</style>
```
**Tushuntirish:** Compaction jarayoni bir nechta faylni bitta optimallashtirilgan faylga aylantiradi, `scale` effekti buni vizual ifodalaydi.

### Topshiriq #1208: Indeks turi tanlov menyusi
**Tavsif:** Foydalanuvchiga turli indeks turlari (B-Tree, Hash, GIN) orasida tanlov qilish imkonini beruvchi interfeys.
**Talablar:** CSS `radio` tugmalari uchun maxsus dizayn.
**Yechim (HTML & CSS):**
```html
<label class="index-option">
  <input type="radio" name="index"> B-Tree
</label>
<style>
  .index-option { display: block; padding: 10px; border: 1px solid #ccc; cursor: pointer; }
  input:checked + .index-option { background: #3498db; color: white; }
</style>
```
**Tushuntirish:** Indeks turlari o'rtasidagi tanlovni aniq va qulay qilish uchun `radio` tugmalari uslublandi.

### Topshiriq #1209: Ma'lumotlar bazasi "Buffer Pool" holati
**Tavsif:** Xotiradagi ma'lumotlar buferi (Buffer Pool) to'lish darajasini ko'rsatish.
**Talablar:** `linear-gradient` yordamida xotira to'lish darajasini ko'rsatuvchi progress bar.
**Yechim (HTML & CSS):**
```html
<div class="buffer-pool">
  <div class="fill" style="width: 65%;"></div>
</div>
<style>
  .buffer-pool { width: 100%; height: 20px; background: #eee; }
  .fill { height: 100%; background: linear-gradient(to right, #f1c40f, #e67e22); }
</style>
```
**Tushuntirish:** Buffer Pool holati tizim unumdorligi uchun muhim, rangli gradient esa to'lish darajasini tez anglashga yordam beradi.

### Topshiriq #1210: Indekslash xatolarini qayd etish paneli
**Tavsif:** Indekslash jarayonida yuzaga kelgan xatolarni (duplicate keys, overflow) ko'rsatish paneli.
**Talablar:** CSS `flexbox` yordamida xabar turlarini (error, warning) ajratish.
**Yechim (HTML & CSS):**
```html
<div class="alert error">Xatolik: Duplicate Key aniqlandi!</div>
<style>
  .alert { padding: 10px; margin: 5px; border-left: 5px solid; }
  .error { border-color: #e74c3c; background: #fdeaea; }
</style>
```
**Tushuntirish:** Indekslashda xatolarni vizual ajratish (qizil chiziq) tizim administratoriga muammoni tezroq aniqlashga yordam beradi.

---

### Topshiriq #1211: LSM-Tree MemTable vizualizatsiyasi
**Tavsif:** LSM-Tree arxitekturasida ma'lumotlar avval xotirada (MemTable) to'planadi. Ushbu jarayonni foydalanuvchi interfeysida real vaqtda kuzatish uchun komponent yaratish.
**Talablar:** CSS Grid yordamida xotira bloklarini dinamik ko'rsatish, o'zgarishlarni animatsiya qilish.
**Yechim (HTML & CSS):**
```html
<div class="memtable-container">
  <!-- MemTable bloklari -->
  <div class="block">Key: 101 | Val: A</div>
  <div class="block">Key: 102 | Val: B</div>
</div>

<style>
  .memtable-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 10px; padding: 20px; }
  .block { border: 2px solid #2c3e50; padding: 10px; background: #ecf0f1; transition: transform 0.3s; }
  .block:hover { transform: scale(1.05); background: #3498db; color: white; }
</style>
```
**Tushuntirish:** Grid tizimi xotira bloklarining tartibli joylashuvini ta'minlaydi, bu esa LSM-Tree'dagi "Sorted String Table" (SSTable) ga o'tish jarayonini vizual modellashtirish uchun qulaydir.

### Topshiriq #1212: B+Tree tugunlari iyerarxiyasi
**Tavsif:** B+Tree daraxtining ichki va barg tugunlarini vizual ajratish.
**Talablar:** Flexbox yordamida daraxt iyerarxiyasini ko'rsatish, tugunlar orasidagi bog'liqlikni chiziqlar bilan ifodalash.
**Yechim (HTML & CSS):**
```html
<div class="tree-node">Root (Index)
  <div class="children">
    <div class="leaf">Leaf 1</div>
    <div class="leaf">Leaf 2</div>
  </div>
</div>

<style>
  .tree-node { text-align: center; border: 1px solid #000; padding: 10px; }
  .children { display: flex; justify-content: space-around; margin-top: 20px; }
  .leaf { border: 1px dashed #e74c3c; padding: 5px; }
</style>
```
**Tushuntirish:** B+Tree'da qidiruv tezligini ta'minlash uchun iyerarxik tuzilma muhim. Flexbox bu yerda tugunlar orasidagi masofani avtomatik optimallashtiradi.

### Topshiriq #1213: WAL (Write-Ahead Logging) holat paneli
**Tavsif:** Ma'lumotlar bazasiga yozishdan oldin log faylga yozish jarayonini (WAL) ko'rsatuvchi status bar.
**Talablar:** Progress bar orqali log yozish jarayonini ko'rsatish.
**Yechim (HTML & CSS):**
```html
<div class="wal-progress">
  <div class="bar" style="width: 70%;"></div>
</div>

<style>
  .wal-progress { width: 100%; height: 20px; background: #ddd; border-radius: 10px; overflow: hidden; }
  .bar { height: 100%; background: #27ae60; transition: width 0.5s ease; }
</style>
```
**Tushuntirish:** WAL ma'lumotlar xavfsizligini ta'minlaydi. Progress bar foydalanuvchiga operatsiya xavfsiz tarzda jurnalga yozilayotganini bildiradi.

### Topshiriq #1214: Indekslash samaradorligi grafigi
**Tavsif:** Indekslangan va indekslanmagan qidiruv tezligini solishtiruvchi grafik.
**Talablar:** CSS `height` xususiyatidan foydalanib ustunli diagramma yaratish.
**Yechim (HTML & CSS):**
```html
<div class="chart">
  <div class="bar" style="height: 20px;">No Index</div>
  <div class="bar" style="height: 150px;">Indexed</div>
</div>

<style>
  .chart { display: flex; align-items: flex-end; gap: 20px; height: 200px; }
  .bar { width: 50px; background: #8e44ad; }
</style>
```
**Tushuntirish:** Indekslash ma'lumotlar bazasi so'rovlarini tezlashtiradi. Grafik bu farqni vizual ravishda yaqqol ko'rsatadi.

### Topshiriq #1215: SSTable qatlamlari (Compaction)
**Tavsif:** LSM-Tree'da "Compaction" jarayonini vizualizatsiya qilish.
**Talablar:** Bir nechta kichik qatlamlarni bitta katta qatlamga birlashtirish animatsiyasi.
**Yechim (HTML & CSS):**
```html
<div class="compaction-zone">
  <div class="layer">SSTable 1</div>
  <div class="layer">SSTable 2</div>
</div>

<style>
  .compaction-zone { display: flex; flex-direction: column; gap: 5px; }
  .layer { padding: 10px; background: #f39c12; animation: merge 2s infinite; }
  @keyframes merge { to { background: #d35400; } }
</style>
```
**Tushuntirish:** Compaction jarayoni diskdagi bo'sh joyni tozalaydi. Animatsiya bu jarayonning davomiyligini anglatadi.

### Topshiriq #1216: B+Tree barg tugunlari bog'lanishi
**Tavsif:** B+Tree'dagi barg tugunlarining o'zaro ikki tomonlama bog'liqligini (linked list) ko'rsatish.
**Talablar:** CSS `::after` psevdo-elementi yordamida o'qlar chizish.
**Yechim (HTML & CSS):**
```html
<div class="node">Node A</div>
<div class="node">Node B</div>

<style>
  .node { display: inline-block; padding: 10px; border: 1px solid #333; position: relative; }
  .node::after { content: '→'; position: absolute; right: -15px; }
</style>
```
**Tushuntirish:** Barg tugunlarining bog'liqligi diapazonli so'rovlar (range queries) uchun juda muhimdir.

### Topshiriq #1217: Ma'lumotlar bazasi "Lock" holati
**Tavsif:** Yozish jarayonida ma'lumotlar bazasi bloklanganligini (Lock) ko'rsatuvchi interfeys.
**Talablar:** Qulf (lock) ikonkasini CSS orqali yaratish.
**Yechim (HTML & CSS):**
```html
<div class="lock-icon"></div>

<style>
  .lock-icon { width: 20px; height: 15px; border: 2px solid red; border-radius: 5px; position: relative; }
  .lock-icon::before { content: ''; position: absolute; top: -10px; left: 4px; width: 8px; height: 8px; border: 2px solid red; border-radius: 50%; }
</style>
```
**Tushuntirish:** Tranzaksion izolyatsiyani ta'minlash uchun qulflar muhim. Bu kod minimal CSS bilan funksional ikonka yaratadi.

### Topshiriq #1218: Disk I/O operatsiyalari monitori
**Tavsif:** Diskka yozish va o'qish tezligini ko'rsatuvchi dashboard elementi.
**Talablar:** CSS `conic-gradient` yordamida aylana diagramma.
**Yechim (HTML & CSS):**
```html
<div class="disk-usage" style="background: conic-gradient(blue 60%, #eee 0);"></div>

<style>
  .disk-usage { width: 100px; height: 100px; border-radius: 50%; }
</style>
```
**Tushuntirish:** Disk I/O ma'lumotlar bazasi unumdorligining asosiy ko'rsatkichidir. `conic-gradient` eng samarali vizualizatsiya usulidir.

### Topshiriq #1219: B+Tree qidiruv yo'li (Highlight)
**Tavsif:** B+Tree ichida ma'lum bir kalitni qidirish yo'lini ajratib ko'rsatish.
**Talablar:** CSS `box-shadow` yordamida tanlangan tugunni yoritish.
**Yechim (HTML & CSS):**
```html
<div class="node active">Target Node</div>

<style>
  .node { padding: 10px; border: 1px solid #ccc; }
  .active { box-shadow: 0 0 10px yellow; border-color: gold; }
</style>
```
**Tushuntirish:** Qidiruv jarayonida foydalanuvchiga qaysi tugun tekshirilayotganini ko'rsatish tushunarlilikni oshiradi.

### Topshiriq #1220: WAL Checkpoint jarayoni
**Tavsif:** WAL faylidan ma'lumotlarni asosiy bazaga ko'chirish (Checkpoint) jarayoni.
**Talablar:** CSS `transition` yordamida ma'lumotlarning "oqimi"ni ko'rsatish.
**Yechim (HTML & CSS):**
```html
<div class="data-flow"></div>

<style>
  .data-flow { width: 50px; height: 10px; background: blue; position: relative; animation: move 2s infinite; }
  @keyframes move { from { left: 0; } to { left: 100px; } }
</style>
```
**Tushuntirish:** Checkpoint jarayoni bazaning tiklanish vaqtini qisqartiradi. Animatsiya ma'lumotlarning logdan bazaga ko'chishini simulyatsiya qiladi.

---

### Topshiriq #1221: LSM-Tree MemTable vizualizatsiyasi
**Tavsif:** LSM-Tree arxitekturasida ma'lumotlar avval xotirada (MemTable) to'planadi. Ushbu topshiriq MemTable to'lish jarayonini real vaqtda kuzatish uchun interfeys yaratishni talab qiladi.
**Talablar:** CSS Grid yordamida dinamik kataklar, ma'lumot hajmi oshganda rang o'zgarishi (gradient).
**Yechim (HTML & CSS):**
```html
<div class="memtable">
  <div class="cell filled">Key: 101</div>
  <div class="cell filled">Key: 102</div>
  <div class="cell empty">Empty</div>
</div>
<style>
  .memtable { display: grid; grid-template-columns: repeat(3, 100px); gap: 10px; }
  .cell { padding: 20px; border: 1px solid #333; transition: background 0.3s; }
  .filled { background: #4CAF50; color: white; } /* To'lgan katak */
  .empty { background: #f4f4f4; }
</style>
```
**Tushuntirish:** LSM-Tree'da MemTable xotira chegarasiga yetganda diskka "flush" qilinadi. Grid tizimi ma'lumotlar tuzilmasini vizual tushunish uchun eng samarali usuldir.

### Topshiriq #1222: B+Tree tugunlari ierarxiyasi
**Tavsif:** B+Tree daraxtida ma'lumotlar faqat barg (leaf) tugunlarida saqlanadi. Ushbu tuzilmani vizual ifodalash.
**Talablar:** Flexbox yordamida ierarxik daraxt ko'rinishi, tugunlar orasidagi bog'liqlik chiziqlari.
**Yechim (HTML & CSS):**
```html
<div class="tree">
  <div class="node">Root (Index)</div>
  <div class="leaf-container">
    <div class="node leaf">Leaf 1</div>
    <div class="node leaf">Leaf 2</div>
  </div>
</div>
<style>
  .tree { display: flex; flex-direction: column; align-items: center; }
  .leaf { border-top: 2px solid blue; margin-top: 10px; }
</style>
```
**Tushuntirish:** B+Tree qidiruv tezligini O(log n) darajasida ushlab turadi. Flexbox ierarxiyani vizualizatsiya qilishda eng toza kodni taqdim etadi.

### Topshiriq #1223: WAL (Write-Ahead Logging) Log-fayl paneli
**Tavsif:** Ma'lumotlar bazasi xavfsizligi uchun har bir operatsiya avval WAL fayliga yoziladi. Ushbu loglarni kuzatish paneli.
**Talablar:** Monospaced shrift, avtomatik yangilanuvchi loglar ro'yxati (CSS animation).
**Yechim (HTML & CSS):**
```html
<div class="wal-log">
  <p><span>[10:00:01]</span> INSERT INTO users VALUES (1, 'Ali');</p>
</div>
<style>
  .wal-log { font-family: 'Courier New', monospace; background: #000; color: #0f0; padding: 15px; }
</style>
```
**Tushuntirish:** WAL tizimi tizim qulaganda ma'lumotlar yo'qolmasligini ta'minlaydi. Monospaced shrift loglarning o'qilishini osonlashtiradi.

### Topshiriq #1224: Indekslash samaradorligi grafigi
**Tavsif:** Indekslangan va indekslanmagan qidiruv tezligini solishtiruvchi progress bar.
**Talablar:** CSS Transitions yordamida animatsiyali progress bar.
**Yechim (HTML & CSS):**
```html
<div class="bar-container">
  <div class="bar indexed" style="width: 10%;">10ms</div>
  <div class="bar unindexed" style="width: 90%;">900ms</div>
</div>
<style>
  .bar { height: 30px; transition: width 1s; }
  .indexed { background: green; }
  .unindexed { background: red; }
</style>
```
**Tushuntirish:** Indekslash qidiruvni chiziqli vaqtdan logarifmik vaqtga o'tkazadi. Vizual farq foydalanuvchiga optimizatsiya ahamiyatini ko'rsatadi.

### Topshiriq #1225: B+Tree "Split" jarayoni animatsiyasi
**Tavsif:** Tugun to'lganda uning ikkiga bo'linish jarayonini (split) ko'rsatish.
**Talablar:** CSS Keyframes yordamida elementlarning siljishi.
**Yechim (HTML & CSS):**
```html
<div class="node split"></div>
<style>
  @keyframes split { to { transform: translateX(50px); } }
  .split { animation: split 2s infinite; }
</style>
```
**Tushuntirish:** Split jarayoni B+Tree muvozanatini saqlash uchun muhim. Animatsiya jarayonning dinamikligini aks ettiradi.

### Topshiriq #1226: Ma'lumotlar bazasi "Lock" holati
**Tavsif:** Tranzaksiyalar vaqtida ma'lumotlar bazasi bloklanishi (Locking).
**Talablar:** Qulflangan holatda qizil ramka va "Locked" belgisi.
**Yechim (HTML & CSS):**
```html
<div class="data-row locked">Ma'lumot 1</div>
<style>
  .locked { border: 2px solid red; opacity: 0.6; cursor: not-allowed; }
</style>
```
**Tushuntirish:** Qulflash (Locking) ma'lumotlar yaxlitligini (ACID) ta'minlaydi. Vizual belgi foydalanuvchini kutishga undaydi.

### Topshiriq #1227: LSM-Tree Compaction jarayoni
**Tavsif:** Eski va yangi ma'lumotlarni birlashtirish (Compaction).
**Talablar:** Ikki qatlamni birlashtiruvchi CSS flex-box.
**Yechim (HTML & CSS):**
```html
<div class="compaction">
  <div class="layer">SSTable 1</div>
  <div class="layer">SSTable 2</div>
</div>
<style>
  .compaction { display: flex; flex-direction: column; gap: 5px; }
  .layer { border: 1px dashed #ccc; }
</style>
```
**Tushuntirish:** Compaction diskdagi ortiqcha ma'lumotlarni tozalaydi. Bu jarayon tizim unumdorligini oshiradi.

### Topshiriq #1228: Indeks qidiruv indeksi (B-Tree)
**Tavsif:** B-Tree qidiruv yo'lini ko'rsatuvchi interfeys.
**Talablar:** Hover effekti bilan tanlangan yo'lni ajratib ko'rsatish.
**Yechim (HTML & CSS):**
```html
<ul class="path">
  <li>Root</li><li>Branch</li><li>Leaf</li>
</ul>
<style>
  .path li:hover { color: orange; font-weight: bold; }
</style>
```
**Tushuntirish:** Qidiruv yo'li (Traversal) qanchalik qisqa bo'lsa, so'rov shunchalik tez bajariladi.

### Topshiriq #1229: WAL Checkpoint vizualizatsiyasi
**Tavsif:** WAL faylidan diskka ma'lumot ko'chirish (Checkpoint) holati.
**Talablar:** Dumaloq progress indikatori.
**Yechim (HTML & CSS):**
```html
<div class="checkpoint-circle">60%</div>
<style>
  .checkpoint-circle { border-radius: 50%; border: 5px solid blue; width: 50px; height: 50px; }
</style>
```
**Tushuntirish:** Checkpoint tizimning qayta tiklanish vaqtini qisqartiradi. Dumaloq shakl jarayonning davriyligini ifodalaydi.

### Topshiriq #1230: Ma'lumotlar bazasi "Buffer Pool" xotirasi
**Tavsif:** Diskdagi ma'lumotlarning RAMdagi keshlangan qismi.
**Talablar:** "Cache Hit" va "Cache Miss" holatlari uchun rangli indikatorlar.
**Yechim (HTML & CSS):**
```html
<div class="status">Cache Hit: <span class="hit">OK</span></div>
<style>
  .hit { background: green; color: white; padding: 2px 5px; }
</style>
```
**Tushuntirish:** Buffer Pool ma'lumotlar bazasi tezligining asosiy omilidir. Keshlash (Caching) disk I/O operatsiyalarini kamaytiradi.

---

### Topshiriq #1231: LSM-Tree MemTable vizualizatsiyasi
**Tavsif:** LSM-Tree arxitekturasida ma'lumotlar avval xotirada (MemTable) to'planadi. Ushbu jarayonni foydalanuvchi interfeysida real vaqtda ko'rsatish tizim monitoringi uchun zarur.
**Talablar:** MemTable to'lish darajasini ko'rsatuvchi progress bar va ma'lumotlar oqimini vizualizatsiya qilish.
**Yechim (HTML & CSS):**
```html
<div class="memtable-container">
  <h3>MemTable Holati</h3>
  <div class="progress-bar">
    <div class="fill" style="width: 75%;"></div> <!-- 75% to'lgan -->
  </div>
  <p>Status: Flush jarayoni kutilmoqda...</p>
</div>

<style>
  .memtable-container { font-family: sans-serif; border: 1px solid #ccc; padding: 15px; border-radius: 8px; }
  .progress-bar { background: #eee; height: 20px; border-radius: 10px; overflow: hidden; }
  .fill { background: #4caf50; height: 100%; transition: width 0.5s; }
</style>
```
**Tushuntirish:** CSS `transition` xususiyati MemTable holati o'zgarganda vizual silliqlikni ta'minlaydi, bu esa tizimning "flush" jarayonini foydalanuvchiga tushunarli qiladi.

---

### Topshiriq #1232: B+Tree tugunlari iyerarxiyasi
**Tavsif:** B+Tree daraxti ma'lumotlarni qidirish tezligini $O(\log n)$ darajasida ushlab turadi. Interfeysda daraxt tugunlarini iyerarxik ko'rsatish kerak.
**Talablar:** Flexbox yordamida tugunlar orasidagi bog'liqlikni vizual aks ettirish.
**Yechim (HTML & CSS):**
```html
<div class="tree-node">
  <div class="parent">Root (Index)</div>
  <div class="children">
    <div class="leaf">Leaf 1</div>
    <div class="leaf">Leaf 2</div>
  </div>
</div>

<style>
  .tree-node { display: flex; flex-direction: column; align-items: center; }
  .children { display: flex; gap: 20px; margin-top: 10px; }
  .leaf { border: 1px solid blue; padding: 10px; border-radius: 5px; }
</style>
```
**Tushuntirish:** Flexbox daraxt tuzilishini dinamik ravishda markazlashtirish va tugunlar o'rtasidagi masofani boshqarish uchun eng samarali usuldir.

---

### Topshiriq #1233: WAL (Write-Ahead Log) jurnal paneli
**Tavsif:** Ma'lumotlar bazasi xavfsizligi uchun har bir yozuv avval WAL fayliga yoziladi. Ushbu loglarni kuzatish paneli.
**Talablar:** Loglar ro'yxati, yangi yozuvlar uchun "append-only" dizayn.
**Yechim (HTML & CSS):**
```html
<ul class="wal-log">
  <li>[10:01:02] INSERT INTO users...</li>
  <li>[10:01:05] UPDATE balance...</li>
</ul>

<style>
  .wal-log { list-style: none; background: #000; color: #0f0; padding: 10px; font-family: monospace; }
</style>
```
**Tushuntirish:** Monospace shrifti va qora fon tizim loglari uchun standart bo'lib, ma'lumotlarning o'qilishini osonlashtiradi.

---

### Topshiriq #1234: Indekslash samaradorligi grafigi
**Tavsif:** Indekslangan va indekslanmagan qidiruv tezligini solishtirish uchun vizual dashboard.
**Talablar:** Ikki xil ustunli grafik (CSS Grid).
**Yechim (HTML & CSS):**
```html
<div class="chart">
  <div class="bar" style="height: 20px;">No Index</div>
  <div class="bar" style="height: 100px;">Indexed</div>
</div>

<style>
  .chart { display: grid; grid-template-columns: 1fr 1fr; align-items: end; height: 120px; }
  .bar { background: #3498db; margin: 5px; }
</style>
```
**Tushuntirish:** CSS Grid yordamida qidiruv tezligidagi farqni vizual ravishda yaqqol ko'rsatish imkoniyati yaratildi.

---

### Topshiriq #1235: SSTable fayl tuzilishi
**Tavsif:** LSM-Tree'da SSTable fayllari o'zgarmas (immutable) hisoblanadi. Ushbu fayllarni boshqarish interfeysi.
**Talablar:** Fayl holatini (Active/Compacted) ko'rsatuvchi kartalar.
**Yechim (HTML & CSS):**
```html
<div class="sstable-card">
  <h4>SSTable #882</h4>
  <span class="badge">Compacted</span>
</div>

<style>
  .sstable-card { border-left: 5px solid green; padding: 10px; background: #f9f9f9; }
  .badge { background: green; color: white; padding: 2px 5px; border-radius: 3px; }
</style>
```
**Tushuntirish:** `border-left` yordamida fayl holatini rang bilan kodlash, foydalanuvchiga tezkor vizual ma'lumot beradi.

---

### Topshiriq #1236: Bloom Filter vizualizatsiyasi
**Tavsif:** Bloom filter - qidiruvni tezlashtirish uchun ishlatiladigan ehtimollik ma'lumotlar strukturasi.
**Talablar:** Bit-array (0 va 1) katakchalarini vizualizatsiya qilish.
**Yechim (HTML & CSS):**
```html
<div class="bit-array">
  <div class="bit">0</div><div class="bit">1</div><div class="bit">0</div>
</div>

<style>
  .bit-array { display: flex; gap: 5px; }
  .bit { width: 30px; height: 30px; border: 1px solid #333; text-align: center; }
</style>
```
**Tushuntirish:** Flexbox yordamida bitlar qatorini yaratish, xotira bloklarini vizual tushunishga yordam beradi.

---

### Topshiriq #1237: Compaction jarayoni indikatori
**Tavsif:** LSM-Tree'da eski ma'lumotlarni birlashtirish (Compaction) fon jarayoni.
**Talablar:** Aylanuvchi yuklanish belgisi (spinner).
**Yechim (HTML & CSS):**
```html
<div class="spinner"></div>

<style>
  .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 30px; height: 30px; animation: spin 2s linear infinite; }
  @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
</style>
```
**Tushuntirish:** CSS `keyframes` yordamida og'ir fon jarayonlari (compaction) uchun foydalanuvchi tajribasini yaxshilash.

---

### Topshiriq #1238: Ma'lumotlar bazasi klasteri holati
**Tavsif:** Bir nechta tugunlardan iborat klaster holatini monitoring qilish.
**Talablar:** Tugunlar holati (Online/Offline) uchun rangli indikatorlar.
**Yechim (HTML & CSS):**
```html
<div class="node online">Node 1</div>
<div class="node offline">Node 2</div>

<style>
  .node { padding: 10px; margin: 5px; border-radius: 4px; }
  .online { background: #d4edda; }
  .offline { background: #f8d7da; }
</style>
```
**Tushuntirish:** Semantik ranglar (yashil/qizil) tizim nosozliklarini darhol aniqlash imkonini beradi.

---

### Topshiriq #1239: Query qidiruv paneli
**Tavsif:** Ma'lumotlar bazasiga so'rov yuborish uchun interfeys.
**Talablar:** Kengaytirilgan qidiruv maydoni va tugma.
**Yechim (HTML & CSS):**
```html
<input type="text" placeholder="SELECT * FROM table...">
<button>Run Query</button>

<style>
  input { padding: 10px; width: 300px; border: 2px solid #ddd; }
  button { padding: 10px; background: #333; color: white; border: none; }
</style>
```
**Tushuntirish:** Minimalistik dizayn foydalanuvchining asosiy vazifaga (so'rov yozish) diqqatini qaratadi.

---

### Topshiriq #1240: Ma'lumotlar bazasi xavfsizlik ogohlantirishi
**Tavsif:** B+Tree yoki WAL fayllariga ruxsatsiz kirish urinishlarini ogohlantirish.
**Talablar:** Modal oynasi yoki ogohlantirish bloki.
**Yechim (HTML & CSS):**
```html
<div class="alert">Xavfsizlik: WAL fayli o'zgartirildi!</div>

<style>
  .alert { background: #ffcc00; padding: 15px; font-weight: bold; border: 1px solid #999; }
</style>
```
**Tushuntirish:** Sariq fon va qalin shrift tizim administratorining e'tiborini darhol jalb qilish uchun tanlangan.

---

### Topshiriq #1241: B+Tree Indeks Vizualizatori
**Tavsif:** Ma'lumotlar bazasidagi B+Tree tuzilishini tushunish uchun tugunlar (nodes) ierarxiyasini vizual aks ettirish.
**Talablar:** CSS Grid yordamida daraxt ierarxiyasini saqlash, o'qilishi oson bo'lgan vizual bloklar.
**Yechim (HTML & CSS):**
```html
<div class="b-tree">
  <div class="node root">Root: [10, 20]</div>
  <div class="children">
    <div class="node leaf">Leaf: [1-9]</div>
    <div class="node leaf">Leaf: [11-19]</div>
    <div class="node leaf">Leaf: [21+]</div>
  </div>
</div>
<style>
  .b-tree { display: flex; flex-direction: column; align-items: center; gap: 20px; }
  .node { border: 2px solid #2c3e50; padding: 10px; border-radius: 5px; background: #ecf0f1; }
  .children { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
</style>
```
**Tushuntirish:** CSS Grid yordamida daraxtning tarmoqlanishini aniq ko'rsatish, bu ma'lumotlar bazasi indekslarining qidiruv tezligini vizual tushunishga yordam beradi.

### Topshiriq #1242: WAL (Write-Ahead Logging) Holat Paneli
**Tavsif:** Tranzaksiyalar jurnalini (WAL) real vaqtda kuzatish uchun interfeys komponenti.
**Talablar:** "Pending" va "Committed" holatlari uchun rangli indikatorlar.
**Yechim (HTML & CSS):**
```html
<div class="wal-log">
  <div class="entry committed">TX_001: Commit</div>
  <div class="entry pending">TX_002: Write...</div>
</div>
<style>
  .entry { padding: 5px; margin: 2px; border-left: 5px solid; }
  .committed { border-color: green; background: #e8f5e9; }
  .pending { border-color: orange; background: #fff3e0; }
</style>
```
**Tushuntirish:** WAL tizimida ma'lumotlar bazasi yaxlitligini ta'minlash uchun tranzaksiya holatini vizual ajratish juda muhim.

### Topshiriq #1243: LSM-Tree "SSTable" Qatlamlari
**Tavsif:** LSM-Tree tarkibidagi turli darajadagi (Level 0, 1, 2) SSTable fayllarini ko'rsatish.
**Talablar:** Qatlamlar bo'yicha o'lcham farqini CSS `scale` orqali ko'rsatish.
**Yechim (HTML & CSS):**
```html
<div class="lsm-stack">
  <div class="level l0">L0: MemTable</div>
  <div class="level l1">L1: Sorted Table</div>
</div>
<style>
  .lsm-stack { display: flex; flex-direction: column; gap: 5px; }
  .level { padding: 10px; border: 1px solid #333; transition: 0.3s; }
  .l0 { width: 100px; background: #ffcccc; }
  .l1 { width: 200px; background: #ccffcc; }
</style>
```
**Tushuntirish:** LSM-Tree'da ma'lumotlar bazasi yozish tezligini oshirish uchun qatlamlar (levels) bo'yicha taqsimlanadi.

### Topshiriq #1244: Indeks Qidiruv "Latency" Indikatori
**Tavsif:** Indekslash samaradorligini (O(log n)) ko'rsatuvchi progress bar.
**Talablar:** Qidiruv vaqti qancha qisqa bo'lsa, bar rangi yashil bo'lishi kerak.
**Yechim (HTML & CSS):**
```html
<div class="latency-container">
  <div class="bar" style="width: 15%;"></div>
</div>
<style>
  .latency-container { width: 100%; background: #eee; height: 20px; }
  .bar { height: 100%; background: #27ae60; transition: width 0.5s; }
</style>
```
**Tushuntirish:** Indekslash algoritmlari qidiruv vaqtini qisqartiradi, bu vizualizatsiya foydalanuvchiga tizim tezligini ko'rsatadi.

### Topshiriq #1245: B+Tree Tugunini To'ldirish (Fill Factor)
**Tavsif:** B+Tree tugunlarining to'lish darajasini ko'rsatuvchi vizual element.
**Talablar:** 80% dan oshsa, ogohlantirish rangini ko'rsatish.
**Yechim (HTML & CSS):**
```html
<div class="node-fill" style="--fill: 85%;"></div>
<style>
  .node-fill { width: 200px; height: 30px; background: linear-gradient(to right, red var(--fill), #ddd var(--fill)); }
</style>
```
**Tushuntirish:** B+Tree'da tugunlar to'lib qolsa, "split" (bo'linish) jarayoni yuz beradi, buni kuzatish ishlash samaradorligi uchun muhim.

### Topshiriq #1246: Ma'lumotlar Bazasi "Flush" Animatsiyasi
**Tavsif:** MemTable'dan SSTable'ga ma'lumot ko'chish jarayonini (Flush) aks ettirish.
**Talablar:** CSS `keyframes` yordamida harakatlanish effekti.
**Yechim (HTML & CSS):**
```html
<div class="data-packet"></div>
<style>
  .data-packet { width: 20px; height: 20px; background: blue; animation: move 2s infinite; }
  @keyframes move { from { transform: translateY(0); } to { transform: translateY(50px); } }
</style>
```
**Tushuntirish:** LSM-Tree'da ma'lumotlar xotiradan diskka o'tkaziladi, bu "Flush" deb ataladi.

### Topshiriq #1247: Indeks Turlari (Clustered vs Non-Clustered)
**Tavsif:** Ikki xil indeks turini taqqoslovchi kartalar.
**Talablar:** Flexbox yordamida yonma-yon joylashtirish.
**Yechim (HTML & CSS):**
```html
<div class="index-types">
  <div class="card">Clustered: Data Sorted</div>
  <div class="card">Non-Clustered: Pointer</div>
</div>
<style>
  .index-types { display: flex; gap: 10px; }
  .card { padding: 15px; border: 1px solid #000; flex: 1; }
</style>
```
**Tushuntirish:** Indekslash strategiyasini tanlash ma'lumotlar bazasi arxitekturasining asosi hisoblanadi.

### Topshiriq #1248: WAL "Checkpoint" Belgisi
**Tavsif:** WAL jurnalida "Checkpoint" (xavfsiz nuqta) belgisini qo'yish.
**Talablar:** CSS `::before` psevdo-elementidan foydalanish.
**Yechim (HTML & CSS):**
```html
<div class="log-item">Data Entry</div>
<style>
  .log-item::before { content: "✔"; color: blue; margin-right: 5px; }
</style>
```
**Tushuntirish:** Checkpoint'lar tizim ishdan chiqqanda ma'lumotlarni tiklash uchun zarur bo'lgan nuqtalardir.

### Topshiriq #1249: B+Tree "Split" Vizualizatsiyasi
**Tavsif:** Tugun bo'linish jarayonini (Split) ko'rsatuvchi interfeys.
**Talablar:** Tugun ikkiga ajralganda animatsiya qo'shish.
**Yechim (HTML & CSS):**
```html
<div class="split-container">
  <div class="node">Node A</div>
  <div class="arrow">→</div>
  <div class="node">Node B</div>
</div>
<style>
  .split-container { display: flex; align-items: center; gap: 10px; }
  .node { border: 1px solid red; padding: 10px; }
</style>
```
**Tushuntirish:** B+Tree muvozanatini saqlash uchun tugunlar doimiy ravishda bo'linadi va birlashadi.

### Topshiriq #1250: Ma'lumotlar Bazasi "Compaction" Jarayoni
**Tavsif:** LSM-Tree'da eski ma'lumotlarni tozalash (Compaction) jarayonini ko'rsatish.
**Talablar:** CSS `opacity` orqali eski ma'lumotlarning yo'qolishini ko'rsatish.
**Yechim (HTML & CSS):**
```html
<div class="compaction-box">Old Data</div>
<style>
  .compaction-box { opacity: 0.5; transition: opacity 2s; }
  .compaction-box:hover { opacity: 0; }
</style>
```
**Tushuntirish:** Compaction - bu LSM-Tree'da disk maydonini optimallashtirish va eski ma'lumotlarni o'chirish jarayoni.