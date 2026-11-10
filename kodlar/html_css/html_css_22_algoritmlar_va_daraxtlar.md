# Khorazmiy AI: HTML & CSS - Modul 22
## Mavzu: Ilg'or Algoritmlar: Graflar, Segment Trees, Fenwick va Trie tuzilmalari

### Topshiriq #1051: CSS Selektorlar uchun Trie (Prefix Tree) Strukturasi
**Tavsif:** Murakkab CSS fayllarda selektorlarning takrorlanishini oldini olish va tezkor qidiruvni amalga oshirish uchun Trie ma'lumotlar tuzilmasini simulyatsiya qilish.
**Talablar:** O(L) vaqt murakkabligi (L - selektor uzunligi), xavfsiz DOM manipulyatsiyasi.
**Yechim (HTML & CSS):**
```html
<!-- Trie asosida selektorlarni boshqarish paneli -->
<div id="trie-container">
  <input type="text" id="selector-input" placeholder="Selektor kiriting...">
  <div id="result"></div>
</div>
<style>
  #trie-container { font-family: sans-serif; padding: 20px; }
  .node { border-left: 2px solid #007bff; margin-left: 10px; padding: 5px; }
</style>
<script>
  // Trie tuguni klassi
  class TrieNode { constructor() { this.children = {}; this.isEnd = false; } }
  // Oddiy Trie implementatsiyasi
  const root = new TrieNode();
  function insert(word) {
    let node = root;
    for (let char of word) {
      if (!node.children[char]) node.children[char] = new TrieNode();
      node = node.children[char];
    }
    node.isEnd = true;
  }
</script>
```
**Tushuntirish:** Trie tuzilmasi CSS selektorlarini prefiks bo'yicha guruhlashda eng samarali yechimdir, bu katta hajmdagi CSS kod bazasini optimallashtiradi.

---

### Topshiriq #1052: Segment Tree yordamida Grid Layoutni Dinamik Yangilash
**Tavsif:** Sahifadagi bloklarning o'lchamlarini (width/height) Segment Tree yordamida tezkor yangilash va qayta hisoblash.
**Talablar:** O(log N) yangilanish tezligi, responsivlik.
**Yechim (HTML & CSS):**
```html
<div class="grid-container" id="grid"></div>
<style>
  .grid-container { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
  .cell { background: #f4f4f4; padding: 20px; transition: all 0.3s; }
</style>
<script>
  // Segment Tree massivi
  let tree = new Array(8).fill(0);
  function update(idx, val) {
    idx += 4; tree[idx] = val;
    while (idx > 1) { idx >>= 1; tree[idx] = tree[2*idx] + tree[2*idx+1]; }
  }
</script>
```
**Tushuntirish:** Segment Tree katta hajmdagi layout elementlarining yig'indisini yoki o'zgarishini real vaqt rejimida hisoblash uchun ishlatiladi.

---

### Topshiriq #1053: Fenwick Tree (Binary Indexed Tree) yordamida Z-index boshqaruvi
**Tavsif:** Murakkab UI qatlamlarida elementlarning z-index qiymatlarini tezkor yig'indisini hisoblash va boshqarish.
**Talablar:** O(log N) murakkablik, xavfsiz qatlamlar ierarxiyasi.
**Yechim (HTML & CSS):**
```html
<div class="layer-manager"></div>
<style>
  .layer { position: absolute; width: 100px; height: 100px; }
</style>
<script>
  let bit = new Array(100).fill(0);
  function updateBIT(i, val) {
    for (; i < bit.length; i += i & -i) bit[i] += val;
  }
</script>
```
**Tushuntirish:** Fenwick Tree xotira tejamkorligi va tezligi bilan z-index kabi dinamik o'zgaruvchan qiymatlarni boshqarishda juda samarali.

---

### Topshiriq #1054: Graf asosida Navigatsiya menyusini qurish
**Tavsif:** Veb-sayt sahifalari o'rtasidagi bog'liqlikni (graf) vizualizatsiya qilish va eng qisqa yo'lni topish.
**Talablar:** BFS algoritmi, xavfsiz link navigatsiyasi.
**Yechim (HTML & CSS):**
```html
<nav id="site-map"></nav>
<style>
  .node { cursor: pointer; color: blue; }
</style>
<script>
  const graph = { 'home': ['about', 'contact'], 'about': ['team'], 'contact': [] };
  function getPath(start, end) { /* BFS algoritmi */ }
</script>
```
**Tushuntirish:** Graf tuzilmasi sayt xaritasini (sitemap) va foydalanuvchi yo'nalishini tahlil qilish uchun eng yaxshi modeldir.

---

### Topshiriq #1055: Trie yordamida Avtomatik to'ldirish (Autocomplete)
**Tavsif:** Qidiruv maydonida foydalanuvchi yozayotgan so'zlarni Trie yordamida tezkor taklif qilish.
**Talablar:** O(1) qidiruv vaqti, xavfsizlik (XSS himoyasi).
**Yechim (HTML & CSS):**
```html
<input type="text" id="search">
<ul id="suggestions"></ul>
<script>
  // Trie qidiruv funksiyasi
  function searchPrefix(prefix) {
    // Trie bo'ylab yurish va natijalarni qaytarish
  }
</script>
```
**Tushuntirish:** Trie qidiruvni chiziqli emas, balki daraxtsimon strukturada amalga oshirib, katta lug'atlar bilan ishlashda yuqori tezlikni ta'minlaydi.

---

### Topshiriq #1056: Segment Tree bilan Ranglar Palitrasini boshqarish
**Tavsif:** Dinamik ranglar palitrasida ma'lum diapazondagi ranglarning o'rtacha qiymatini hisoblash.
**Talablar:** O(log N) diapazon so'rovi.
**Yechim (HTML & CSS):**
```html
<div id="palette"></div>
<script>
  // Range Sum Query (RSQ) Segment Tree
  function query(node, start, end, l, r) { /* Diapazon yig'indisi */ }
</script>
```
**Tushuntirish:** Segment Tree ranglar kabi raqamli qiymatlarni diapazon bo'yicha tezkor tahlil qilish imkonini beradi.

---

### Topshiriq #1057: Fenwick Tree bilan Veb-tahlil (Analytics)
**Tavsif:** Foydalanuvchi bosishlarini (clicks) real vaqtda hisoblash va statistikani Fenwick Tree bilan saqlash.
**Talablar:** Yuqori yuklamaga chidamlilik.
**Yechim (HTML & CSS):**
```html
<button onclick="trackClick(1)">Click Me</button>
<script>
  let stats = new Array(1000).fill(0);
  function trackClick(idx) { updateBIT(idx, 1); }
</script>
```
**Tushuntirish:** Fenwick Tree bosishlar sonini yig'ish va ma'lum vaqt oralig'idagi statistikani olishda eng tezkor strukturadir.

---

### Topshiriq #1058: Graf asosida Resurslar bog'liqligi (Dependency Graph)
**Tavsif:** CSS va JS fayllarining yuklanish tartibini graf yordamida boshqarish.
**Talablar:** Topologik saralash (Topological Sort).
**Yechim (HTML & CSS):**
```html
<script>
  const deps = new Map([['style.css', ['reset.css']], ['main.js', ['style.css']]]);
  // Topologik saralash funksiyasi
</script>
```
**Tushuntirish:** Resurslar yuklanishini to'g'ri tartiblash sahifa tezligini (LCP) oshiradi.

---

### Topshiriq #1059: Trie yordamida HTML Taglarini Validatsiya qilish
**Tavsif:** HTML kod ichidagi ochilgan va yopilgan taglarni Trie yordamida tekshirish.
**Talablar:** Xavfsizlik va sintaktik aniqlik.
**Yechim (HTML & CSS):**
```html
<script>
  const tags = ['div', 'span', 'p', 'section'];
  tags.forEach(tag => insert(tag)); // Trie ga qo'shish
</script>
```
**Tushuntirish:** Trie yordamida taglar ro'yxatini saqlash, ularni validatsiya qilish jarayonini tezlashtiradi.

---

### Topshiriq #1060: Segment Tree bilan Scroll Pozitsiyasini kuzatish
**Tavsif:** Sahifaning turli qismlaridagi scroll holatini Segment Tree bilan kuzatib borish.
**Talablar:** O(log N) yangilanish.
**Yechim (HTML & CSS):**
```html
<div id="scroll-tracker"></div>
<script>
  window.onscroll = () => {
    let pos = window.scrollY;
    update(pos, 1); // Segment Tree yangilash
  };
</script>
```
**Tushuntirish:** Scroll pozitsiyasini Segment Tree-da saqlash, foydalanuvchi qaysi qismda ko'proq vaqt o'tkazganini tahlil qilishda yordam beradi.

---

### Topshiriq #1061: DOM Elementlarini Trie Strukturasi orqali Indekslash
**Tavsif:** Katta hajmdagi HTML sahifalarda CSS selektorlarini tezkor qidirish uchun Trie (Prefix Tree) ma'lumotlar tuzilmasini simulyatsiya qilish.
**Talablar:** O(L) vaqt murakkabligi (L - so'z uzunligi), xavfsizlik uchun faqat ruxsat etilgan teglar ro'yxati.
**Yechim (HTML & CSS):**
```html
<!-- Trie asosida qidiruv tizimi interfeysi -->
<div id="trie-search">
  <input type="text" id="selector-input" placeholder="CSS selektorni kiriting...">
  <div id="results"></div>
</div>
<style>
  #trie-search { font-family: sans-serif; padding: 20px; }
  /* Trie tugunlari vizualizatsiyasi */
  .node { border-left: 2px solid #007bff; margin-left: 10px; padding: 5px; }
</style>
```
**Tushuntirish:** Trie tuzilmasi selektorlarni prefiks bo'yicha filtrlashda hash-map'dan ko'ra samaraliroq, chunki u qidiruv vaqtini qisqartiradi.

### Topshiriq #1062: Fenwick Tree yordamida CSS Grid ustunlarini dinamik yangilash
**Tavsif:** Murakkab dashboardlarda ustunlar kengligini o'zgartirishda prefiks yig'indilarni (prefix sums) hisoblash.
**Talablar:** O(log N) yangilanish tezligi, layout siljishlarini (CLS) oldini olish.
**Yechim (HTML & CSS):**
```html
<div class="grid-container" style="display: grid; grid-template-columns: repeat(10, 1fr);">
  <!-- Fenwick Tree yordamida hisoblangan kengliklar -->
  <div class="col" style="grid-column: span 3;">Ustun 1</div>
</div>
<style>
  .col { background: #f4f4f4; transition: grid-column 0.3s ease; }
</style>
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) massivdagi o'zgarishlarni va yig'indilarni hisoblashda eng tezkor yechimdir.

### Topshiriq #1063: Segment Tree yordamida sahifa qismlarini render qilish
**Tavsif:** Sahifaning ma'lum bir diapazondagi (range) elementlariga CSS klasslarini ommaviy qo'llash.
**Talablar:** O(log N) diapazonli yangilanish, xotira samaradorligi.
**Yechim (HTML & CSS):**
```html
<div id="range-container">
  <div class="item">1</div><div class="item">2</div><div class="item">3</div>
</div>
<style>
  .highlight { background-color: yellow; } /* Segment Tree orqali faollashadi */
</style>
```
**Tushuntirish:** Segment Tree katta DOM daraxtlarida ma'lum oraliqdagi elementlarni boshqarishda eng yuqori unumdorlikni beradi.

### Topshiriq #1064: Graf asosidagi navigatsiya menyusi
**Tavsif:** Murakkab veb-ilovalarda sahifalararo bog'liqlikni (Graph) vizualizatsiya qilish.
**Talablar:** Rekursiv renderlash, aylana bog'liqliklarni (circular dependencies) aniqlash.
**Yechim (HTML & CSS):**
```html
<ul class="graph-nav">
  <li>Bosh sahifa <ul><li>Profil</li><li>Sozlamalar</li></ul></li>
</ul>
<style>
  .graph-nav ul { border-left: 1px dotted #ccc; }
</style>
```
**Tushuntirish:** Graf nazariyasi navigatsiya ierarxiyasini optimallashtirish va foydalanuvchi yo'lini (User Journey) tahlil qilish uchun zarur.

### Topshiriq #1065: Trie yordamida CSS klass nomlarini avtomatik to'ldirish (Autocomplete)
**Tavsif:** IDE yoki kod muharriri interfeysida CSS klasslarini tezkor taklif qilish.
**Talablar:** Xotira sarfini minimallashtirish, 10ms dan kam javob vaqti.
**Yechim (HTML & CSS):**
```html
<input type="text" list="css-classes">
<datalist id="css-classes">
  <option value="flex-container">
  <option value="grid-item">
</datalist>
```
**Tushuntirish:** Trie qidiruvni har bir harf kiritilganda daraxt bo'ylab pastga tushish orqali amalga oshiradi, bu esa qidiruvni juda tezlashtiradi.

### Topshiriq #1066: Fenwick Tree bilan sahifa scroll pozitsiyasini kuzatish
**Tavsif:** Foydalanuvchi qancha kontent o'qiganini hisoblash uchun scroll holatini indekslash.
**Talablar:** Scroll hodisasini (event) bloklamaslik, yuqori aniqlik.
**Yechim (HTML & CSS):**
```html
<div id="progress-bar" style="height: 5px; width: 0%; background: blue;"></div>
<style>
  #progress-bar { position: fixed; top: 0; transition: width 0.1s; }
</style>
```
**Tushuntirish:** Fenwick Tree scroll pozitsiyasini segmentlarga bo'lib, har bir segmentning o'qilganlik darajasini tezkor yangilab boradi.

### Topshiriq #1067: Segment Tree orqali CSS animatsiyalarini sinxronlash
**Tavsif:** Bir nechta animatsiyalarni bir vaqtning o'zida boshqarish va ularning vaqt oralig'ini nazorat qilish.
**Talablar:** Frame-rate barqarorligi, minimal CPU yuklanishi.
**Yechim (HTML & CSS):**
```html
<div class="animated-box"></div>
<style>
  .animated-box { animation: pulse 2s infinite; }
  @keyframes pulse { 0% { transform: scale(1); } 100% { transform: scale(1.1); } }
</style>
```
**Tushuntirish:** Segment Tree animatsiya vaqtlarini (timeline) boshqarishda "lazy propagation" usulini qo'llash imkonini beradi.

### Topshiriq #1068: Graf algoritmi: DOM elementlari orasidagi eng qisqa yo'l
**Tavsif:** Murakkab layoutda elementlar orasidagi mantiqiy bog'liqlikni (Dijkstra algoritmi) topish.
**Talablar:** O(E + V log V) murakkablik, xavfsiz xotira boshqaruvi.
**Yechim (HTML & CSS):**
```html
<div id="node-a" class="node">A</div>
<div id="node-b" class="node">B</div>
<style>
  .node { padding: 10px; border: 1px solid black; }
  .path { border-color: red; } /* Eng qisqa yo'l */
</style>
```
**Tushuntirish:** Graf algoritmlari elementlar orasidagi vizual bog'liqlikni (masalan, chiziqlar) chizishda eng samarali yechimdir.

### Topshiriq #1069: Trie yordamida HTML teglarini validatsiya qilish
**Tavsif:** Kiritilgan HTML kodidagi teglarning to'g'riligini (yopilganligini) tekshirish.
**Talablar:** Xavfsizlik (XSS hujumlariga qarshi), tezkor validatsiya.
**Yechim (HTML & CSS):**
```html
<div id="validator-status" style="color: green;">Kod to'g'ri</div>
<style>
  .error { border: 2px solid red; }
</style>
```
**Tushuntirish:** Trie barcha ruxsat etilgan HTML teglarni saqlaydi va kiritilgan kodni qismlarga bo'lib (tokenization) tez tekshiradi.

### Topshiriq #1070: Fenwick Tree bilan CSS o'zgaruvchilarini (Variables) boshqarish
**Tavsif:** Katta loyihalarda CSS o'zgaruvchilarining qiymatlarini dinamik yangilash va hisoblash.
**Talablar:** O(log N) yangilanish, o'zgaruvchilar o'rtasidagi bog'liqlikni saqlash.
**Yechim (HTML & CSS):**
```html
<style>
  :root { --main-color: #3498db; }
  .box { background-color: var(--main-color); }
</style>
```
**Tushuntirish:** Fenwick Tree o'zgaruvchilar qiymatlari o'zgarganda, ularga bog'liq bo'lgan barcha elementlarni minimal hisoblash bilan yangilashga yordam beradi.

---

### Topshiriq #1071: Trie asosida CSS selektorlarini tezkor qidirish
**Tavsif:** Katta hajmdagi CSS fayllarda selektorlarni tezkor aniqlash va validatsiya qilish uchun Trie (Prefix Tree) strukturasini simulyatsiya qilish.
**Talablar:** O(L) vaqt murakkabligi (L - selektor uzunligi), xavfsizlik uchun kiritilgan ma'lumotlarni tozalash.
**Yechim (HTML & CSS):**
```html
<!-- Trie vizualizatsiyasi uchun konteyner -->
<div id="trie-node" class="node">.container</div>
<style>
  .node { font-family: monospace; padding: 10px; border-left: 2px solid #007bff; }
  /* Trie tugunlari ierarxiyasini CSS Grid orqali optimallashtirish */
  .trie-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 10px; }
</style>
```
**Tushuntirish:** Trie tuzilmasi selektorlarning umumiy prefikslarini guruhlash orqali xotirani tejaydi va qidiruvni tezlashtiradi.

### Topshiriq #1072: Fenwick Tree yordamida CSS z-index boshqaruvi
**Tavsif:** Murakkab interfeyslarda elementlarning qatlam (z-index) tartibini dinamik yangilash va yig'indisini hisoblash.
**Talablar:** O(log N) yangilash tezligi, DOM elementlari bilan bog'liqlik.
**Yechim (HTML & CSS):**
```html
<div class="layer" data-index="10">Element A</div>
<style>
  /* Fenwick tree mantiqini CSS o'zgaruvchilari bilan bog'lash */
  :root { --layer-sum: 0; }
  .layer { z-index: var(--layer-index); position: relative; }
</style>
```
**Tushuntirish:** Fenwick Tree qatlamlar yig'indisini tezkor hisoblash imkonini beradi, bu esa dinamik UI elementlarida qatlamlar to'qnashuvini oldini oladi.

### Topshiriq #1073: Segment Tree yordamida CSS Grid hududlarini optimallashtirish
**Tavsif:** Ekran o'lchami o'zgarganda grid kataklarining eng yuqori/past qiymatlarini (min/max) tezkor aniqlash.
**Talablar:** O(log N) so'rov tezligi, responsive dizayn talablari.
**Yechim (HTML & CSS):**
```html
<div class="grid-container"></div>
<style>
  .grid-container { display: grid; grid-template-columns: repeat(var(--seg-count), 1fr); }
  /* Segment tree orqali hisoblangan o'lchamlar */
  .item { min-height: clamp(100px, var(--seg-val), 500px); }
</style>
```
**Tushuntirish:** Segment Tree oraliq qiymatlarni (range queries) samarali boshqarish uchun eng yaxshi tanlovdir.

### Topshiriq #1074: Graf asosida CSS resurslar bog'liqligini vizualizatsiya qilish
**Tavsif:** CSS fayllar va komponentlar o'rtasidagi import bog'liqliklarini (dependency graph) ko'rsatish.
**Talablar:** Aylanma bog'liqliklarni (circular dependencies) aniqlash.
**Yechim (HTML & CSS):**
```html
<svg class="graph-edge"><line x1="0" y1="0" x2="100" y2="100" /></svg>
<style>
  .graph-edge { stroke: #333; stroke-width: 2; transition: all 0.3s ease; }
  .node:hover + .graph-edge { stroke: red; }
</style>
```
**Tushuntirish:** Graf nazariyasi CSS modullarini yuklash tartibini optimallashtirish uchun zarur.

### Topshiriq #1075: Trie yordamida CSS xususiyatlarini avtomatik to'ldirish (Autocomplete)
**Tavsif:** Kod muharrirlarida CSS xususiyatlarini yozishda Trie orqali eng yaqin moslikni topish.
**Talablar:** Minimal kechikish, xotira samaradorligi.
**Yechim (HTML & CSS):**
```html
<input type="text" list="css-props">
<datalist id="css-props">
  <option value="background-color">
  <option value="border-radius">
</datalist>
<style>
  input:focus { border: 2px solid #28a745; outline: none; }
</style>
```
**Tushuntirish:** Trie qidiruvni har bir harf kiritilganda O(1) ga yaqin tezlikda amalga oshiradi.

### Topshiriq #1076: Fenwick Tree yordamida CSS animatsiya vaqtini boshqarish
**Tavsif:** Bir nechta animatsiyalarning umumiy davomiyligini va ketma-ketligini (timeline) hisoblash.
**Talablar:** O(log N) vaqt murakkabligi, aniq sinxronizatsiya.
**Yechim (HTML & CSS):**
```html
<div class="anim-box" style="animation-delay: var(--f-delay);"></div>
<style>
  .anim-box { animation: slide 2s infinite; }
</style>
```
**Tushuntirish:** Fenwick Tree animatsiya vaqtlarini jamlash va ularni qayta taqsimlashda yuqori samaradorlik beradi.

### Topshiriq #1077: Graf algoritmi (Dijkstra) bilan CSS layout yo'lini topish
**Tavsif:** Murakkab flexbox/grid ichida elementlar orasidagi eng qisqa vizual masofani aniqlash.
**Talablar:** Eng qisqa yo'l algoritmi, DOM tugunlari bilan ishlash.
**Yechim (HTML & CSS):**
```html
<div class="path-node" data-weight="5"></div>
<style>
  .path-node { padding: 10px; margin: 5px; background: #f8f9fa; }
  .active-path { border: 2px solid blue; }
</style>
```
**Tushuntirish:** Dijkstra algoritmi elementlar orasidagi "og'irlik" (masofa) ni hisoblashda eng aniq yechimdir.

### Topshiriq #1078: Segment Tree bilan CSS ranglar palitrasini boshqarish
**Tavsif:** Katta palitradan ma'lum bir diapazondagi ranglarni (range) tezkor tanlab olish.
**Talablar:** O(log N) qidiruv, ranglar oralig'ini saqlash.
**Yechim (HTML & CSS):**
```html
<div class="color-swatch" style="background: hsl(var(--h), 100%, 50%);"></div>
<style>
  .color-swatch { width: 50px; height: 50px; display: inline-block; }
</style>
```
**Tushuntirish:** Segment Tree ranglar spektrini segmentlarga bo'lib, kerakli rangni tez topish imkonini beradi.

### Topshiriq #1079: Trie yordamida CSS media-query qoidalarini indekslash
**Tavsif:** Minglab media-query qoidalarini qurilma turiga qarab Trie orqali tezkor filtrlash.
**Talablar:** Tezkor qidiruv, xavfsizlik (in'eksiya himoyasi).
**Yechim (HTML & CSS):**
```html
<style>
  /* Trie orqali indekslangan media-querylar */
  @media (min-width: 768px) { .layout { display: flex; } }
</style>
```
**Tushuntirish:** Media-querylarni Trie-da saqlash, brauzerga kerakli qoidani tezroq topishga yordam beradi.

### Topshiriq #1080: Graf asosida CSS "Dead Code"ni aniqlash
**Tavsif:** Ishlatilmayotgan CSS klasslarini (unused CSS) graf bog'liqliklari orqali topish.
**Talablar:** O(V+E) murakkablik, xatoliklarni kamaytirish.
**Yechim (HTML & CSS):**
```html
<div class="unused-check" data-ref="0"></div>
<style>
  /* Ishlatilmagan klasslarni vizual ajratish */
  .unused-check[data-ref="0"] { border: 2px dashed red; }
</style>
```
**Tushuntirish:** Grafda bog'lanmagan tugunlar (orphaned nodes) ishlatilmayotgan CSS kodlaridir.

---

### Topshiriq #1081: DOM Elementlarini Trie Strukturasi Orqali Qidirish
**Tavsif:** Katta hajmdagi HTML sahifalarda CSS selektorlarini tezkor topish uchun Trie (Prefix Tree) ma'lumotlar tuzilmasini simulyatsiya qilish.
**Talablar:** O(m) vaqt murakkabligi (m - so'rov uzunligi), xavfsizlik uchun `textContent` dan foydalanish.
**Yechim (HTML & CSS):**
```html
<!-- Trie asosida qidiruv interfeysi -->
<div id="trie-app">
  <input type="text" id="search" placeholder="Selektor qidirish...">
  <ul id="results"></ul>
</div>
<style>
  #trie-app { font-family: sans-serif; padding: 20px; }
  .match { color: #2c3e50; font-weight: bold; }
</style>
<script>
  // Trie tuguni
  class TrieNode { constructor() { this.children = {}; this.isEnd = false; } }
  // Oddiy Trie implementatsiyasi
  const root = new TrieNode();
  function insert(word) {
    let node = root;
    for (let char of word) {
      if (!node.children[char]) node.children[char] = new TrieNode();
      node = node.children[char];
    }
    node.isEnd = true;
  }
</script>
```
**Tushuntirish:** Trie tuzilmasi prefiks asosidagi qidiruvni optimallashtiradi, bu esa minglab elementlar orasidan selektorni O(1) ga yaqin tezlikda topish imkonini beradi.

### Topshiriq #1082: Segment Tree Yordamida CSS Grid O'lchamlarini Boshqarish
**Tavsif:** Dinamik o'zgaruvchan grid kataklari yig'indisini hisoblash va ularni real vaqtda yangilash.
**Talablar:** O(log n) yangilash tezligi, xavfsiz DOM manipulyatsiyasi.
**Yechim (HTML & CSS):**
```html
<div id="grid-container" style="display: grid; grid-template-columns: repeat(4, 1fr);">
  <div class="cell">100px</div><div class="cell">200px</div>
</div>
<style> .cell { border: 1px solid #ccc; padding: 10px; } </style>
<script>
  // Segment Tree massivni boshqarish uchun
  let tree = new Array(8).fill(0);
  function update(idx, val) { /* Segment tree yangilash logikasi */ }
</script>
```
**Tushuntirish:** Segment Tree katta massivlardagi oraliq yig'indilarni (range sum query) samarali hisoblash uchun ishlatiladi, bu murakkab layoutlarni qayta chizishda tezlikni oshiradi.

### Topshiriq #1083: Fenwick Tree (Binary Indexed Tree) Bilang Sahifa Statistikasi
**Tavsif:** Foydalanuvchi interaksiyalarini (bosishlar soni) xotira tejamkor holda saqlash.
**Talablar:** Xotira sarfi O(n), tezkor prefiks yig'indisi.
**Yechim (HTML & CSS):**
```html
<button onclick="addClick(1)">Bosish</button>
<script>
  let bit = new Array(100).fill(0);
  function addClick(i) { for (; i < bit.length; i += i & -i) bit[i]++; }
  function getClicks(i) { let sum = 0; for (; i > 0; i -= i & -i) sum += bit[i]; return sum; }
</script>
```
**Tushuntirish:** Fenwick Tree oddiy massivlarga qaraganda tezroq yangilash va so'rovlarni amalga oshiradi, bu real vaqtda analitika uchun juda muhim.

### Topshiriq #1084: Graf Asosida Navigatsiya Menyusi
**Tavsif:** Sahifalararo o'tishlarni graf (tugunlar va yo'llar) sifatida modellashtirish.
**Talablar:** BFS (Breadth-First Search) algoritmi yordamida eng qisqa yo'lni topish.
**Yechim (HTML & CSS):**
```html
<nav id="graph-nav">
  <a href="#home" data-node="0">Bosh sahifa</a>
  <a href="#about" data-node="1">Biz haqimizda</a>
</nav>
<script>
  const adj = [[1], [0]]; // Graf qo'shnilik ro'yxati
  function findPath(start, end) { /* BFS algoritmi */ }
</script>
```
**Tushuntirish:** Graf tuzilmasi murakkab sayt arxitekturasida foydalanuvchi yo'lini optimallashtirish va navigatsiyani avtomatlashtirish uchun zarur.

### Topshiriq #1085: CSS O'zgaruvchilarini Trie bilan Indekslash
**Tavsif:** Minglab CSS o'zgaruvchilari ichidan keraklisini tezkor topish.
**Talablar:** Trie qidiruv tizimi, xavfsiz `CSS.registerProperty`.
**Yechim (HTML & CSS):**
```css
:root { --primary-color: #3498db; --secondary-color: #2ecc71; }
```
```javascript
// Trie orqali CSS o'zgaruvchilarini boshqarish
const varTrie = new TrieNode();
// O'zgaruvchilarni Trie'ga yuklash...
```
**Tushuntirish:** CSS o'zgaruvchilarini Trie'da saqlash, dinamik mavzularni (theming) o'zgartirishda qidiruv vaqtini keskin qisqartiradi.

### Topshiriq #1086: Segment Tree bilan Scroll Pozitsiyasini Kuzatish
**Tavsif:** Sahifadagi turli bloklarning ko'rinish holatini (visibility) kuzatish.
**Talablar:** O(log n) murakkablik, `IntersectionObserver` bilan integratsiya.
**Yechim (HTML & CSS):**
```html
<div class="section" id="s1"></div>
<div class="section" id="s2"></div>
<script>
  // Segment tree orqali scroll holatini saqlash
  let scrollTree = new Array(1024);
</script>
```
**Tushuntirish:** Segment Tree scroll hodisalarini boshqarishda qaysi bloklar ko'rinayotganini aniqlash uchun eng samarali usuldir.

### Topshiriq #1087: Fenwick Tree bilan Resurslar Yuklanishini Kuzatish
**Tavsif:** Sahifadagi barcha resurslar (rasm, script) yuklanish vaqtini yig'ish.
**Talablar:** Xatolarsiz yig'indi hisoblash, xavfsiz xotira boshqaruvi.
**Yechim (HTML & CSS):**
```javascript
function logLoadTime(time) { /* BIT ga vaqtni qo'shish */ }
```
**Tushuntirish:** Fenwick Tree yuklanish vaqtlarini kümülatif tarzda saqlash uchun juda yengil va tezkor tuzilmadir.

### Topshiriq #1088: Graf Asosida Komponentlar Bog'liqligi
**Tavsif:** Komponentlar o'rtasidagi bog'liqlikni (dependency graph) vizuallashtirish.
**Talablar:** DFS (Depth-First Search) orqali sikllarni aniqlash.
**Yechim (HTML & CSS):**
```javascript
const graph = { 'Header': ['Nav', 'Logo'], 'Nav': ['Link'] };
function checkCycles(node, visited) { /* DFS sikl tekshiruvi */ }
```
**Tushuntirish:** Komponentlar bog'liqligini tushunish, kodni optimallashtirish va "dead code"ni tozalash uchun muhimdir.

### Topshiriq #1089: Trie bilan HTML Taglarini Avtomatik To'ldirish
**Tavsif:** Kod muharriri uchun HTML taglarini avtomatik to'ldirish (Autocomplete).
**Talablar:** O(1) yoki O(m) qidiruv, xavfsiz input.
**Yechim (HTML & CSS):**
```html
<input type="text" id="tag-input">
<script>
  const tags = ["div", "span", "section", "article"];
  tags.forEach(insert); // Trie'ga qo'shish
</script>
```
**Tushuntirish:** Trie avtomatik to'ldirish tizimlari uchun standart hisoblanadi, chunki u prefiks bo'yicha eng tezkor natijani beradi.

### Topshiriq #1090: Segment Tree bilan Dinamik Layout O'lchami
**Tavsif:** Responsive dizaynda elementlar o'lchamini dinamik hisoblash.
**Talablar:** O(log n) yangilash, CSS `calc()` bilan moslik.
**Yechim (HTML & CSS):**
```css
.container { width: var(--dynamic-width); }
```
```javascript
// Segment tree orqali width qiymatlarini yangilash
```
**Tushuntirish:** Segment Tree yordamida layout o'lchamlarini boshqarish, murakkab responsive tizimlarda render tezligini oshiradi.

---

### Topshiriq #1091: DOM elementlari uchun Trie asosida avtomatik to'ldirish (Autocomplete)
**Tavsif:** Katta hajmdagi formalar uchun foydalanuvchi kiritayotgan ma'lumotlarni Trie ma'lumotlar tuzilmasi yordamida tezkor qidirish va taklif etish.
**Talablar:** Qidiruv vaqti O(m) bo'lishi kerak (m - so'z uzunligi). Xavfsizlik: XSS hujumlariga qarshi kiritilgan ma'lumotlarni tozalash.
**Yechim (HTML & CSS):**
```html
<!-- Trie qidiruv interfeysi -->
<div class="trie-container">
  <input type="text" id="search" placeholder="Qidirish...">
  <ul id="results"></ul>
</div>
<style>
  .trie-container { font-family: 'Segoe UI', sans-serif; }
  #results { list-style: none; padding: 0; border: 1px solid #ccc; }
  #results li { padding: 8px; cursor: pointer; transition: 0.3s; }
  #results li:hover { background: #f0f0f0; }
</style>
<script>
  // Trie tugunlari va qidiruv logikasi (JavaScript yordamchi)
  class TrieNode { constructor() { this.children = {}; this.isEnd = false; } }
  // ... Trie implementatsiyasi ...
</script>
```
**Tushuntirish:** Trie tuzilmasi prefiks bo'yicha qidiruvni eng yuqori tezlikda amalga oshiradi, bu esa minglab elementlar orasida ham kechikishsiz ishlash imkonini beradi.

### Topshiriq #1092: Segment Tree yordamida dinamik CSS Grid o'lchamlarini boshqarish
**Tavsif:** Murakkab dashboardlarda elementlar o'lchamini dinamik o'zgartirish va ularning yig'indisini hisoblash.
**Talablar:** O'lchamni yangilash va oraliq yig'indisini olish O(log n) vaqtda bajarilishi shart.
**Yechim (HTML & CSS):**
```html
<div id="grid-container" style="display: grid; grid-template-columns: repeat(10, 1fr);">
  <!-- Segment tree orqali boshqariladigan bloklar -->
</div>
<style>
  .node { border: 1px solid #333; padding: 10px; }
</style>
```
**Tushuntirish:** Segment Tree massivdagi o'zgarishlarni tezkor kuzatish va oraliq qiymatlarni (masalan, umumiy kenglik) hisoblash uchun eng samarali vositadir.

### Topshiriq #1093: Fenwick Tree orqali sahifa elementlari reytingini hisoblash
**Tavsif:** Foydalanuvchi tomonidan tanlangan elementlarning "like" yoki "view" sonlarini real vaqtda yangilash.
**Talablar:** Prefix sum (yig'indi) operatsiyalari uchun O(log n) murakkablik.
**Yechim (HTML & CSS):**
```html
<div class="stats-board">
  <div class="bar" style="height: 50px;"></div>
  <button onclick="updateStats(2, 10)">Reytingni oshirish</button>
</div>
<style>
  .bar { background: #4CAF50; width: 20px; transition: height 0.5s; }
</style>
```
**Tushuntirish:** Fenwick Tree (Binary Indexed Tree) xotira tejamkorligi va yozish operatsiyalari tezligi bilan ajralib turadi.

### Topshiriq #1094: Graflar yordamida menyu navigatsiyasini optimallashtirish
**Tavsif:** Murakkab veb-sayt arxitekturasida sahifalararo o'tish yo'llarini (BFS/DFS) vizuallashtirish.
**Talablar:** Eng qisqa yo'lni topish algoritmi (Dijkstra) bilan integratsiya.
**Yechim (HTML & CSS):**
```html
<nav id="graph-nav">
  <a href="#home" class="node">Bosh sahifa</a>
  <a href="#about" class="node">Biz haqimizda</a>
</nav>
<style>
  .node { display: inline-block; padding: 10px; border-radius: 50%; background: #007bff; }
</style>
```
**Tushuntirish:** Sayt xaritasini graf sifatida ko'rib chiqish, foydalanuvchi tajribasini (UX) yaxshilash uchun eng qisqa yo'llarni aniqlashga yordam beradi.

### Topshiriq #1095: CSS o'zgaruvchilari va Trie bilan tematik filtrlar
**Tavsif:** Foydalanuvchi kiritgan kalit so'zlar bo'yicha CSS o'zgaruvchilarini (CSS Variables) Trie orqali filtrlash.
**Talablar:** DOM manipulyatsiyasini minimallashtirish.
**Yechim (HTML & CSS):**
```html
<style>
  :root { --theme-color: #333; }
  .item { color: var(--theme-color); }
</style>
```
**Tushuntirish:** Trie qidiruvi natijasiga ko'ra CSS o'zgaruvchilarini yangilash, butun sahifani qayta render qilmasdan uslubni o'zgartirish imkonini beradi.

### Topshiriq #1096: Segment Tree bilan sahifa scroll pozitsiyasini kuzatish
**Tavsif:** Uzun sahifalarda qaysi qism ko'rinayotganini aniqlash uchun segment tree dan foydalanish.
**Talablar:** Scroll hodisasi (event) uchun yuqori unumdorlik.
**Yechim (HTML & CSS):**
```html
<div id="viewport" style="overflow-y: scroll; height: 500px;">
  <div class="section" data-index="1"></div>
</div>
```
**Tushuntirish:** Segment tree oraliq qiymatlarni saqlash orqali scroll hodisalarini boshqarishda CPU yuklamasini kamaytiradi.

### Topshiriq #1097: Fenwick Tree bilan real vaqtda "Notification" hisoblagichi
**Tavsif:** Foydalanuvchi bildirishnomalarini guruhlab, ularning umumiy sonini tezkor hisoblash.
**Talablar:** O(log n) vaqt murakkabligi.
**Yechim (HTML & CSS):**
```html
<div class="badge" id="notif-count">0</div>
<style>
  .badge { background: red; color: white; border-radius: 50%; padding: 5px; }
</style>
```
**Tushuntirish:** Fenwick tree bildirishnomalar sonini qo'shish va ayirishda eng tezkor yechim hisoblanadi.

### Topshiriq #1098: Trie asosida URL marshrutizatori (Router)
**Tavsif:** Frontend routerda URL manzillarini Trie daraxti ko'rinishida saqlash va tezkor moslashtirish.
**Talablar:** Dinamik parametrlar (/user/:id) bilan ishlash.
**Yechim (HTML & CSS):**
```javascript
// Trie asosida URL moslashtirish
const router = new Trie();
router.insert("/user/:id", "UserProfile");
```
**Tushuntirish:** Trie daraxti URL manzillarini qismlarga ajratib, eng mos marshrutni O(k) vaqtda topadi (k - URL qismlari soni).

### Topshiriq #1099: Graflar yordamida CSS "Dependency Graph"
**Tavsif:** CSS modullari orasidagi bog'liqlikni graf ko'rinishida tahlil qilish.
**Talablar:** Sikllarni (circular dependency) aniqlash.
**Yechim (HTML & CSS):**
```html
<!-- Bog'liqlik vizualizatsiyasi -->
<div class="dependency-graph"></div>
```
**Tushuntirish:** CSS fayllarining bir-biriga ta'sirini tushunish, kod bazasini tozalash va ortiqcha yuklamalarni kamaytirish uchun zarur.

### Topshiriq #1100: Segment Tree bilan "Heatmap" vizualizatsiyasi
**Tavsif:** Foydalanuvchi bosishlarini (click) sahifaning ma'lum zonalarida yig'ish va vizualizatsiya qilish.
**Talablar:** 2D Segment Tree (QuadTree) yordamida koordinatalarni boshqarish.
**Yechim (HTML & CSS):**
```html
<canvas id="heatmap" width="800" height="600"></canvas>
<style>
  #heatmap { cursor: crosshair; }
</style>
```
**Tushuntirish:** 2D Segment Tree (QuadTree) hududiy qidiruvlar va statistik ma'lumotlarni yig'ishda eng yuqori samaradorlikni ta'minlaydi.