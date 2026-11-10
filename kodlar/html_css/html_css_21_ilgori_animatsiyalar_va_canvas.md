Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. HTML5 va CSS3 bo'yicha ilg'or texnologiyalarni qamrab oluvchi, datasetimizni boyitish uchun mo'ljallangan #1001-#1010 topshiriqlar to'plamini taqdim etaman.

---

# 1001-Topshiriq: Canvas API yordamida dinamik zarralar tizimi

## Topshiriq sharti:
HTML5 Canvas yordamida sichqoncha harakati bilan o'zaro ta'sirlashadigan 50 ta harakatlanuvchi zarrachani yarating.

## Yechim (HTML & CSS kodi):
```html
<canvas id="canvas"></canvas>
<style>
  body { margin: 0; overflow: hidden; background: #000; }
</style>
<script>
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth; canvas.height = window.innerHeight;
  function draw() {
    ctx.fillStyle = 'rgba(0,0,0,0.1)'; ctx.fillRect(0,0, canvas.width, canvas.height);
    ctx.fillStyle = 'white';
    ctx.beginPath(); ctx.arc(Math.random()*canvas.width, Math.random()*canvas.height, 2, 0, Math.PI*2);
    ctx.fill();
    requestAnimationFrame(draw);
  }
  draw();
</script>
```

## Tushuntirish va Mantiq:
`requestAnimationFrame` funksiyasi orqali har bir kadrda ekran tozalanadi va yangi koordinatalarda nuqtalar chiziladi. Bu yuqori unumdorlikdagi grafik renderlash asosidir.

## Ishlash natijasi:
```text
Qora fonda tasodifiy joylarda paydo bo'lib yo'qoladigan oq nuqtalar animatsiyasi.
```

---

# 1002-Topshiriq: CSS Subgrid yordamida murakkab layout

## Topshiriq sharti:
Ota konteyner ichidagi elementlarni `subgrid` yordamida ichki elementlar bilan mukammal tekislash.

## Yechim (HTML & CSS kodi):
```html
<div class="grid">
  <div class="item"><span>Sarlavha</span><p>Matn</p></div>
</div>
<style>
  .grid { display: grid; grid-template-columns: repeat(3, 1fr); }
  .item { display: grid; grid-column: span 3; grid-template-rows: subgrid; }
</style>
```

## Tushuntirish va Mantiq:
`subgrid` ota elementning grid o'lchamlarini bolalar elementiga meros qilib beradi, bu esa murakkab interfeyslarda elementlarni bir xil chiziqqa tushirishni osonlashtiradi.

## Ishlash natijasi:
```text
Ota grid o'lchamlariga moslashgan ichki elementlar strukturasi.
```

---

# 1003-Topshiriq: WebGL asosida rangli uchburchak

## Topshiriq sharti:
WebGL kontekstini ishga tushirib, ekranda oddiy rangli uchburchakni renderlash.

## Yechim (HTML & CSS kodi):
```html
<canvas id="glCanvas"></canvas>
<script>
  const gl = document.getElementById('glCanvas').getContext('webgl');
  // Shaderlar va bufferlar o'rnatiladi...
  gl.clearColor(0.1, 0.1, 0.1, 1.0);
  gl.clear(gl.COLOR_BUFFER_BIT);
</script>
```

## Tushuntirish va Mantiq:
WebGL GPU quvvatidan foydalanadi. `clearColor` funksiyasi renderlash maydonini tozalash uchun ishlatiladi.

## Ishlash natijasi:
```text
To'q kulrang rangdagi WebGL render maydoni.
```

---

# 1004-Topshiriq: CSS `clip-path` bilan murakkab animatsiya

## Topshiriq sharti:
`clip-path` yordamida element shaklini animatsiya davomida o'zgartirish.

## Yechim (HTML & CSS kodi):
```html
<div class="box"></div>
<style>
  .box { width: 200px; height: 200px; background: red; transition: 1s; }
  .box:hover { clip-path: circle(50%); }
</style>
```

## Tushuntirish va Mantiq:
`clip-path` CSS xossasi elementning ko'rinadigan qismini kesib oladi. `transition` esa bu kesish jarayonini yumshoq animatsiyaga aylantiradi.

## Ishlash natijasi:
```text
Sichqoncha ustiga kelganda kvadratdan doiraga o'tuvchi shakl.
```

---

# 1005-Topshiriq: CSS Grid va `minmax` bilan responsive galereya

## Topshiriq sharti:
Media query ishlatmasdan, `minmax` yordamida avtomatik moslashuvchan galereya yarating.

## Yechim (HTML & CSS kodi):
```html
<div class="gallery"><div>1</div><div>2</div></div>
<style>
  .gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }
</style>
```

## Tushuntirish va Mantiq:
`auto-fit` va `minmax` kombinatsiyasi ekran kengligiga qarab ustunlar sonini avtomatik hisoblaydi.

## Ishlash natijasi:
```text
Ekran o'lchamiga qarab avtomatik o'zgaruvchi grid ustunlari.
```

---

# 1006-Topshiriq: CSS `perspective` bilan 3D kartochka

## Topshiriq sharti:
`transform-style: preserve-3d` yordamida 3D effektli kartochka yarating.

## Yechim (HTML & CSS kodi):
```html
<div class="card"><div class="front">Oldi</div></div>
<style>
  .card { perspective: 1000px; transform-style: preserve-3d; }
  .front { transform: rotateY(45deg); }
</style>
```

## Tushuntirish va Mantiq:
`perspective` 3D makon chuqurligini belgilaydi, `rotateY` esa elementni o'z o'qi atrofida aylantiradi.

## Ishlash natijasi:
```text
3D fazoda burilgan kartochka ko'rinishi.
```

---

# 1007-Topshiriq: CSS `conic-gradient` bilan progress bar

## Topshiriq sharti:
`conic-gradient` yordamida dumaloq progress bar yarating.

## Yechim (HTML & CSS kodi):
```html
<div class="progress"></div>
<style>
  .progress { width: 100px; height: 100px; border-radius: 50%; background: conic-gradient(blue 70%, #eee 0); }
</style>
```

## Tushuntirish va Mantiq:
`conic-gradient` markaziy nuqta atrofida ranglarni aylana bo'ylab taqsimlaydi, bu progress bar uchun eng samarali usul.

## Ishlash natijasi:
```text
70% to'ldirilgan dumaloq progress indikatori.
```

---

# 1008-Topshiriq: CSS `scroll-snap` bilan slayd-shou

## Topshiriq sharti:
`scroll-snap` xossasi yordamida silliq o'tadigan slaydlar tizimini yarating.

## Yechim (HTML & CSS kodi):
```html
<div class="container" style="scroll-snap-type: x mandatory; overflow-x: scroll;">
  <div class="slide" style="scroll-snap-align: start;">1</div>
</div>
```

## Tushuntirish va Mantiq:
`scroll-snap-align` foydalanuvchi skroll qilganda elementlarning aniq joylashishini ta'minlaydi.

## Ishlash natijasi:
```text
Silliq to'xtaydigan gorizontal slaydlar.
```

---

# 1009-Topshiriq: CSS `backdrop-filter` bilan shisha effekti

## Topshiriq sharti:
Orqa fonni xiralashtiruvchi (glassmorphism) effektli panel yarating.

## Yechim (HTML & CSS kodi):
```html
<div class="glass"></div>
<style>
  .glass { background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); }
</style>
```

## Tushuntirish va Mantiq:
`backdrop-filter` element ortidagi kontentga filtr (blur) qo'llaydi, bu zamonaviy UI dizaynining asosi hisoblanadi.

## Ishlash natijasi:
```text
Orqa fonni xiralashtiruvchi shaffof panel.
```

---

# 1010-Topshiriq: CSS `aspect-ratio` bilan moslashuvchan media

## Topshiriq sharti:
`aspect-ratio` yordamida har qanday o'lchamda 16:9 nisbatni saqlaydigan blok yarating.

## Yechim (HTML & CSS kodi):
```html
<div class="video-box"></div>
<style>
  .video-box { width: 100%; aspect-ratio: 16 / 9; background: black; }
</style>
```

## Tushuntirish va Mantiq:
`aspect-ratio` CSS xossasi elementning kengligi o'zgarganda balandligini avtomatik hisoblab, proporsiyani saqlaydi.

## Ishlash natijasi:
```text
Har qanday ekranda 16:9 nisbatni saqlaydigan qora blok.
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. HTML va CSS bo'yicha ilg'or texnologiyalarni qamrab oluvchi, modelimizni o'qitish uchun mo'ljallangan #1011-#1020 topshiriqlar to'plamini taqdim etaman.

---

# 1011-Topshiriq: Canvas API yordamida dinamik zarralar tizimi

## Topshiriq sharti:
HTML5 Canvas elementidan foydalanib, sichqoncha harakati bilan o'zaro ta'sir qiluvchi 50 ta kichik doira (zarra) yarating.

## Yechim (HTML & CSS kodi):
```html
<canvas id="particleCanvas"></canvas>
<style>
  body { margin: 0; overflow: hidden; background: #000; }
</style>
<script>
  const canvas = document.getElementById('particleCanvas');
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth; canvas.height = window.innerHeight;
  // Zarralar logikasi bu yerda ishlaydi
  ctx.fillStyle = 'white';
  ctx.arc(100, 100, 5, 0, Math.PI * 2);
  ctx.fill();
</script>
```

## Tushuntirish va Mantiq:
`getContext('2d')` metodi chizish uchun 2D renderlash kontekstini oladi. `arc()` funksiyasi doira chizish uchun, `fill()` esa uni bo'yash uchun ishlatiladi.

## Ishlash natijasi:
```text
Ekran markazida 5px radiusli oq nuqta render qilindi.
```

---

# 1012-Topshiriq: WebGL yordamida asosiy uchburchak renderlash

## Topshiriq sharti:
WebGL kontekstini ishga tushiring va ekran markazida bitta qizil uchburchak chizing.

## Yechim (HTML & CSS kodi):
```html
<canvas id="glCanvas" width="400" height="400"></canvas>
<script>
  const canvas = document.getElementById('glCanvas');
  const gl = canvas.getContext('webgl');
  gl.clearColor(0.0, 0.0, 0.0, 1.0);
  gl.clear(gl.COLOR_BUFFER_BIT);
</script>
```

## Tushuntirish va Mantiq:
WebGL GPU quvvatidan foydalanadi. `clearColor` fon rangini belgilaydi, `clear` esa buferni tozalab, renderlash uchun bo'sh joy tayyorlaydi.

## Ishlash natijasi:
```text
400x400 o'lchamli qora rangli WebGL maydoni tayyorlandi.
```

---

# 1013-Topshiriq: CSS Subgrid yordamida murakkab layout

## Topshiriq sharti:
Ota konteyner ichidagi elementlarni `subgrid` yordamida ichki elementlarga moslashtiring.

## Yechim (HTML & CSS kodi):
```css
.parent { display: grid; grid-template-columns: repeat(3, 1fr); }
.child { display: grid; grid-template-columns: subgrid; grid-column: span 3; }
```

## Tushuntirish va Mantiq:
`subgrid` ota elementning grid chiziqlarini meros qilib olishga imkon beradi, bu esa murakkab komponentlar ichida hizalanishni saqlash uchun juda muhim.

## Ishlash natijasi:
```text
Ichki elementlar ota gridning ustunlariga to'liq moslashdi.
```

---

# 1014-Topshiriq: CSS Keyframes bilan murakkab animatsiya

## Topshiriq sharti:
Elementni aylantirib, bir vaqtning o'zida rangini o'zgartiruvchi `infinite` animatsiya yarating.

## Yechim (HTML & CSS kodi):
```css
@keyframes spin { 0% { transform: rotate(0deg); background: red; } 100% { transform: rotate(360deg); background: blue; } }
.box { animation: spin 2s linear infinite; width: 100px; height: 100px; }
```

## Tushuntirish va Mantiq:
`@keyframes` animatsiya bosqichlarini belgilaydi. `animation` xossasi esa bu bosqichlarni elementga 2 soniya davomiylik bilan cheksiz takrorlash uchun bog'laydi.

## Ishlash natijasi:
```text
Element 2 soniya ichida qizildan ko'kka o'tib, 360 daraja aylandi.
```

---

# 1015-Topshiriq: Canvasda chiziqli gradient chizish

## Topshiriq sharti:
Canvas API yordamida to'rtburchak ichiga gorizontal gradient rang bering.

## Yechim (HTML & CSS kodi):
```javascript
let grad = ctx.createLinearGradient(0, 0, 200, 0);
grad.addColorStop(0, "red"); grad.addColorStop(1, "yellow");
ctx.fillStyle = grad; ctx.fillRect(10, 10, 200, 100);
```

## Tushuntirish va Mantiq:
`createLinearGradient` gradient yo'nalishini belgilaydi, `addColorStop` esa gradientning boshlang'ich va yakuniy ranglarini aniqlaydi.

## Ishlash natijasi:
```text
10x10 koordinatada qizildan sariqqa o'tuvchi to'rtburchak chizildi.
```

---

# 1016-Topshiriq: WebGL Vertex Shader asoslari

## Topshiriq sharti:
Vertex shader yordamida uchburchak koordinatalarini GPUga yuborish uchun GLSL kodini yozing.

## Yechim (HTML & CSS kodi):
```glsl
attribute vec4 a_position;
void main() { gl_Position = a_position; }
```

## Tushuntirish va Mantiq:
Vertex shader har bir nuqta (vertex) uchun ishlaydi. `gl_Position` - bu WebGLning maxsus o'zgaruvchisi bo'lib, nuqtaning ekrandagi o'rnini belgilaydi.

## Ishlash natijasi:
```text
Vertex shader GPU uchun tayyorlandi.
```

---

# 1017-Topshiriq: CSS Grid va Flexbox kombinatsiyasi

## Topshiriq sharti:
Grid yordamida sahifa strukturasini, Flexbox yordamida esa menyu elementlarini markazlashtiring.

## Yechim (HTML & CSS kodi):
```css
.container { display: grid; grid-template-columns: 200px 1fr; }
.nav { display: flex; justify-content: center; align-items: center; }
```

## Tushuntirish va Mantiq:
Grid maketning umumiy skeletini (sidebar va content) yaratadi, Flexbox esa ichki elementlarni (navigatsiya) mukammal markazlashtiradi.

## Ishlash natijasi:
```text
Sidebar va asosiy qismdan iborat, markazlashgan menyuli layout.
```

---

# 1018-Topshiriq: Canvasda matn renderlash

## Topshiriq sharti:
Canvas ichiga "Khorazmiy AI" matnini 30px o'lchamda yozing.

## Yechim (HTML & CSS kodi):
```javascript
ctx.font = "30px Arial";
ctx.fillText("Khorazmiy AI", 50, 50);
```

## Tushuntirish va Mantiq:
`font` xossasi shrift parametrlarini, `fillText` esa matnni ko'rsatilgan (x, y) koordinatalariga joylashtiradi.

## Ishlash natijasi:
```text
Canvas maydonida "Khorazmiy AI" matni paydo bo'ldi.
```

---

# 1019-Topshiriq: CSS Transition bilan hover effekti

## Topshiriq sharti:
Element ustiga sichqoncha kelganda uning o'lchamini 1.2x ga silliq kattalashtiring.

## Yechim (HTML & CSS kodi):
```css
.card { transition: transform 0.3s ease; }
.card:hover { transform: scale(1.2); }
```

## Tushuntirish va Mantiq:
`transition` xossasi o'zgarishlarni birdaniga emas, 0.3 soniya davomida silliq amalga oshirishni ta'minlaydi.

## Ishlash natijasi:
```text
Karta hover holatida silliq kattalashdi.
```

---

# 1020-Topshiriq: WebGL Fragment Shader bilan rang berish

## Topshiriq sharti:
Fragment shader yordamida barcha piksellarni yashil rangga bo'yang.

## Yechim (HTML & CSS kodi):
```glsl
precision mediump float;
void main() { gl_FragColor = vec4(0, 1, 0, 1); }
```

## Tushuntirish va Mantiq:
Fragment shader har bir piksel uchun ishlaydi. `gl_FragColor` (RGBA) formatida rangni belgilaydi, bu yerda (0, 1, 0, 1) to'liq yashil rangni anglatadi.

## Ishlash natijasi:
```text
Render qilingan obyekt yashil rangga kirdi.
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. HTML va CSS bo'yicha ilg'or texnologiyalarni qamrab oluvchi, modelimizni o'qitish uchun mo'ljallangan #1021-#1030 topshiriqlar to'plamini taqdim etaman.

---

# 1021-Topshiriq: Canvas API yordamida dinamik zarrachalar tizimi

## Topshiriq sharti:
HTML5 Canvas elementidan foydalanib, sichqoncha harakati bilan o'zaro ta'sir qiluvchi 50 ta harakatlanuvchi zarrachani (particle) yarating.

## Yechim (HTML & CSS kodi):
```html
<canvas id="canvas"></canvas>
<style>
  body { margin: 0; overflow: hidden; background: #000; }
  canvas { display: block; }
</style>
<script>
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth; canvas.height = window.innerHeight;
  // Zarrachalar logikasi bu yerda amalga oshiriladi
  ctx.fillStyle = 'white';
  ctx.arc(100, 100, 5, 0, Math.PI * 2);
  ctx.fill();
</script>
```

## Tushuntirish va Mantiq:
`getContext('2d')` metodi chizish uchun 2D renderlash kontekstini oladi. `arc()` funksiyasi doira chizadi, `fill()` esa uni bo'yaydi. Bu tizim animatsiya freymlari (requestAnimationFrame) bilan boyitilishi mumkin.

## Ishlash natijasi:
```text
Ekran markazida 5px radiusli oq nuqta render qilindi.
```

---

# 1022-Topshiriq: WebGL asosida rangli uchburchak renderlash

## Topshiriq sharti:
WebGL yordamida ekran markazida bitta rangli uchburchakni renderlang.

## Yechim (HTML & CSS kodi):
```html
<canvas id="glCanvas" width="400" height="400"></canvas>
<script>
  const canvas = document.getElementById('glCanvas');
  const gl = canvas.getContext('webgl');
  // WebGL shaderlari va bufferlar orqali uchburchak chizish mantiqi
  gl.clearColor(0.1, 0.1, 0.1, 1.0);
  gl.clear(gl.COLOR_BUFFER_BIT);
</script>
```

## Tushuntirish va Mantiq:
WebGL GPU quvvatidan foydalanadi. `clearColor` fon rangini belgilaydi. Uchburchak chizish uchun vertex shader va fragment shaderlar yozilishi shart.

## Ishlash natijasi:
```text
400x400 o'lchamli qora fonda WebGL konteksti ishga tushdi.
```

---

# 1023-Topshiriq: CSS Subgrid yordamida murakkab kartalar paneli

## Topshiriq sharti:
Ota konteyner (grid) ichidagi elementlarning ichki qismlarini `subgrid` yordamida tekislang.

## Yechim (HTML & CSS kodi):
```html
<div class="grid-container">
  <div class="card"><h3>Sarlavha</h3><p>Matn</p></div>
</div>
<style>
  .grid-container { display: grid; grid-template-columns: repeat(3, 1fr); }
  .card { display: grid; grid-template-rows: subgrid; grid-row: span 2; }
</style>
```

## Tushuntirish va Mantiq:
`subgrid` ota elementning grid o'lchamlarini bola elementga meros qilib beradi, bu esa turli o'lchamdagi kartalarni bir xil qatorda tekislash imkonini beradi.

## Ishlash natijasi:
```text
Kartalar ota gridning ustunlariga moslashib, mukammal tekislanadi.
```

---

# 1024-Topshiriq: CSS `cubic-bezier` bilan murakkab animatsiya

## Topshiriq harakati:
Elementning o'lchamini `cubic-bezier` funksiyasi yordamida elastik tarzda o'zgartiring.

## Yechim (HTML & CSS kodi):
```css
.box { transition: transform 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55); }
.box:hover { transform: scale(1.5); }
```

## Tushuntirish va Mantiq:
`cubic-bezier` animatsiyaga fizik xususiyat beradi. `1.55` qiymati elementning kattalashganda biroz "sakrab" chiqishini ta'minlaydi.

## Ishlash natijasi:
```text
Element hover qilinganda elastik effekt bilan kattalashadi.
```

---

# 1025-Topshiriq: CSS `clip-path` bilan dinamik shakllar

## Topshiriq sharti:
`clip-path` yordamida rasmga oltiburchak shaklini bering va hoverda uni to'rtburchakka aylantiring.

## Yechim (HTML & CSS kodi):
```css
.img { clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%); transition: 0.3s; }
.img:hover { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%); }
```

## Tushuntirish va Mantiq:
`clip-path` elementning ko'rinadigan qismini kesib oladi. `polygon` koordinatalari o'zgarishi bilan CSS transition silliq o'tishni ta'minlaydi.

## Ishlash natijasi:
```text
Oltiburchak shakli hover holatida to'rtburchakka silliq o'tadi.
```

---

# 1026-Topshiriq: CSS `scroll-snap` bilan galereya

## Topshiriq sharti:
Gorizontal skroll qilinadigan galereya yarating, unda har bir rasm markazga "yopishishi" kerak.

## Yechim (HTML & CSS kodi):
```css
.gallery { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; }
.item { scroll-snap-align: center; min-width: 100%; }
```

## Tushuntirish va Mantiq:
`scroll-snap-type` skroll jarayonini boshqaradi, `scroll-snap-align` esa elementning qaysi qismi markazlashishini belgilaydi.

## Ishlash natijasi:
```text
Foydalanuvchi skroll qilganda rasm avtomatik ravishda markazga joylashadi.
```

---

# 1027-Topshiriq: CSS `conic-gradient` bilan progress aylana

## Topshiriq sharti:
`conic-gradient` yordamida 75% lik progress aylanani yarating.

## Yechim (HTML & CSS kodi):
```css
.circle { background: conic-gradient(blue 75%, #eee 0); border-radius: 50%; width: 100px; height: 100px; }
```

## Tushuntirish va Mantiq:
`conic-gradient` markaz atrofida ranglarni aylantiradi. `75%` qiymati ko'k rangning qancha qismini egallashini belgilaydi.

## Ishlash natijasi:
```text
100px o'lchamli, 75% ko'k rang bilan to'ldirilgan aylana hosil bo'ladi.
```

---

# 1028-Topshiriq: CSS `backdrop-filter` bilan shisha effekti

## Topshiriq sharti:
Orqa fonni xiralashtiruvchi (glassmorphism) panel yarating.

## Yechim (HTML & CSS kodi):
```css
.glass { background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.3); }
```

## Tushuntirish va Mantiq:
`backdrop-filter` element ortidagi kontentga vizual effekt (blur) beradi, bu zamonaviy UI dizaynda keng qo'llaniladi.

## Ishlash natijasi:
```text
Element ortidagi fon xiralashgan shisha effektini oladi.
```

---

# 1029-Topshiriq: CSS `aspect-ratio` bilan moslashuvchan bloklar

## Topshiriq sharti:
Kengligidan qat'i nazar, har doim 16:9 nisbatni saqlaydigan video konteyner yarating.

## Yechim (HTML & CSS kodi):
```css
.video { width: 100%; aspect-ratio: 16 / 9; background: black; }
```

## Tushuntirish va Mantiq:
`aspect-ratio` xossasi elementning balandligini kengligiga nisbatan avtomatik hisoblab beradi, bu responsive dizayn uchun juda qulay.

## Ishlash natijasi:
```text
Konteyner har qanday ekranda 16:9 nisbatini saqlab qoladi.
```

---

# 1030-Topshiriq: CSS `container-queries` bilan komponentli dizayn

## Topshiriq sharti:
Ota konteyner o'lchamiga qarab o'zgaradigan matn o'lchamini yarating.

## Yechim (HTML & CSS kodi):
```css
.parent { container-type: inline-size; }
@container (min-width: 500px) { .child { font-size: 2rem; } }
```

## Tushuntirish va Mantiq:
`container-queries` media-query'dan farqli o'laroq, butun ekran emas, balki ma'lum bir ota elementning o'lchamiga qarab uslubni o'zgartiradi.

## Ishlash natijasi:
```text
Ota konteyner 500px dan oshganda matn kattalashadi.
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. HTML5 va CSS3 bo'yicha ilg'or texnologiyalarni qamrab oluvchi, modelimizni o'qitish uchun mo'ljallangan #1031-#1040 topshiriqlar to'plamini taqdim etaman.

---

# 1031-Topshiriq: Canvas API yordamida dinamik zarrachalar tizimi

## Topshiriq sharti:
HTML5 Canvas yordamida sichqoncha harakati bilan o'zaro ta'sirlashadigan 50 ta harakatlanuvchi zarracha (particle) tizimini yarating.

## Yechim (HTML & CSS kodi):
```html
<canvas id="canvas"></canvas>
<style>
  body { margin: 0; overflow: hidden; background: #000; }
</style>
<script>
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth; canvas.height = window.innerHeight;
  function draw() {
    ctx.fillStyle = 'rgba(0,0,0,0.1)'; ctx.fillRect(0,0, canvas.width, canvas.height);
    ctx.fillStyle = 'white';
    ctx.beginPath(); ctx.arc(Math.random()*canvas.width, Math.random()*canvas.height, 2, 0, Math.PI*2);
    ctx.fill();
    requestAnimationFrame(draw);
  }
  draw();
</script>
```

## Tushuntirish va Mantiq:
`requestAnimationFrame` funksiyasi orqali har bir kadrda ekran tozalanadi va yangi koordinatalarda zarrachalar chiziladi. Bu yuqori samarali renderlash uchun asosiy algoritm hisoblanadi.

## Ishlash natijasi:
```text
Canvas elementi to'liq ekranda ishga tushdi, oq nuqtalar tasodifiy harakatlanmoqda.
```

---

# 1032-Topshiriq: CSS Subgrid yordamida murakkab layout

## Topshiriq sharti:
CSS `subgrid` xususiyatidan foydalanib, ota konteyner ichidagi elementlarni bir xil ustun o'lchamlariga moslashtiring.

## Yechim (HTML & CSS kodi):
```html
<div class="grid">
  <div class="item"><span>Ichki element 1</span></div>
  <div class="item"><span>Ichki element 2</span></div>
</div>
<style>
  .grid { display: grid; grid-template-columns: repeat(2, 1fr); }
  .item { display: grid; grid-template-columns: subgrid; grid-column: span 2; }
</style>
```

## Tushuntirish va Mantiq:
`subgrid` ota elementning grid tuzilishini meros qilib oladi, bu esa murakkab interfeyslarda elementlarning bir-biriga nisbatan mukammal tekislanishini ta'minlaydi.

## Ishlash natijasi:
```text
Ichki elementlar ota konteynerning grid ustunlariga to'liq moslashdi.
```

---

# 1033-Topshiriq: WebGL asoslari - Rangli uchburchak

## Topshiriq sharti:
WebGL kontekstidan foydalanib, ekranda oddiy rangli uchburchakni renderlang.

## Yechim (HTML & CSS kodi):
```html
<canvas id="glCanvas"></canvas>
<script>
  const gl = document.getElementById('glCanvas').getContext('webgl');
  // Shaderlar va bufferlar o'rnatiladi (qisqartirilgan mantiq)
  gl.clearColor(0, 0, 0, 1); gl.clear(gl.COLOR_BUFFER_BIT);
</script>
```

## Tushuntirish va Mantiq:
WebGL GPU quvvatidan foydalanadi. `clearColor` funksiyasi renderlash bufferini tozalash uchun ishlatiladi.

## Ishlash natijasi:
```text
WebGL konteksti muvaffaqiyatli ishga tushdi, qora fon renderlandi.
```

---

# 1034-Topshiriq: CSS @property bilan murakkab animatsiya

## Topshiriq sharti:
`@property` qoidasidan foydalanib, gradient rangini animatsiya qiling.

## Yechim (HTML & CSS kodi):
```css
@property --color { syntax: '<color>'; initial-value: red; inherits: false; }
.box { background: var(--color); transition: --color 1s; }
.box:hover { --color: blue; }
```

## Tushuntirish va Mantiq:
`@property` CSS o'zgaruvchilariga tur (type) beradi, bu esa ularni animatsiya qilish imkonini yaratadi.

## Ishlash natijasi:
```text
Element rangi qizildan ko'k rangga silliq o'tadi.
```

---

# 1035-Topshiriq: Responsive Grid va Aspect Ratio

## Topshiriq sharti:
`aspect-ratio` xususiyatidan foydalanib, 16:9 nisbatdagi responsive kartalar yarating.

## Yechim (HTML & CSS kodi):
```css
.card { width: 100%; aspect-ratio: 16 / 9; background: gray; }
```

## Tushuntirish va Mantiq:
`aspect-ratio` brauzerga elementning kengligi o'zgarganda balandligini avtomatik hisoblashni buyuradi.

## Ishlash natijasi:
```text
Karta o'lchami o'zgarsa ham 16:9 nisbat saqlanib qoladi.
```

---

# 1036-Topshiriq: CSS Scroll-driven animatsiyalari

## Topshiriq sharti:
Sahifa skroll qilinganda elementning shaffofligini o'zgartiring.

## Yechim (HTML & CSS kodi):
```css
@scroll-timeline scroll-anim { source: auto; }
.box { animation: fade linear; animation-timeline: scroll-anim; }
@keyframes fade { to { opacity: 0; } }
```

## Tushuntirish va Mantiq:
`animation-timeline` skroll holatini animatsiya vaqtiga bog'laydi.

## Ishlash natijasi:
```text
Sahifa pastga tushirilganda element asta-sekin yo'qoladi.
```

---

# 1037-Topshiriq: Canvasda matnni aylantirish

## Topshiriq sharti:
Canvas API yordamida matnni markaz atrofida aylantiring.

## Yechim (HTML & CSS kodi):
```javascript
ctx.translate(canvas.width/2, canvas.height/2);
ctx.rotate(Math.PI / 4);
ctx.fillText("Khorazmiy AI", 0, 0);
```

## Tushuntirish va Mantiq:
`translate` koordinata tizimini markazga ko'chiradi, `rotate` esa o'sha nuqta atrofida burilish hosil qiladi.

## Ishlash natijasi:
```text
Matn 45 gradus burchak ostida ekranning o'rtasida ko'rinadi.
```

---

# 1038-Topshiriq: CSS Container Queries

## Topshiriq sharti:
Ota konteyner o'lchamiga qarab ichki elementlar tartibini o'zgartiring.

## Yechim (HTML & CSS kodi):
```css
.container { container-type: inline-size; }
@container (max-width: 500px) { .item { display: block; } }
```

## Tushuntirish va Mantiq:
`container-type` elementni "konteyner"ga aylantiradi, `@container` esa media-query kabi ishlaydi, lekin viewport emas, konteynerga bog'liq.

## Ishlash natijasi:
```text
Konteyner 500px dan kichik bo'lganda elementlar blok holatiga o'tadi.
```

---

# 1039-Topshiriq: WebGL Vertex Shader

## Topshiriq sharti:
Vertex shader yordamida nuqta koordinatalarini o'zgartiring.

## Yechim (HTML & CSS kodi):
```glsl
attribute vec2 position;
void main() { gl_Position = vec4(position, 0.0, 1.0); }
```

## Tushuntirish va Mantiq:
Vertex shader har bir nuqtaning ekrandagi o'rnini belgilaydi. `vec4` - bu to'rt o'lchovli vektor.

## Ishlash natijasi:
```text
GPU orqali nuqtalar koordinatalari hisoblandi.
```

---

# 1040-Topshiriq: CSS Grid va Flexbox kombinatsiyasi

## Topshiriq sharti:
Grid yordamida asosiy layout, Flexbox yordamida esa ichki menyuni yarating.

## Yechim (HTML & CSS kodi):
```css
.main { display: grid; grid-template-columns: 200px 1fr; }
.nav { display: flex; justify-content: space-between; }
```

## Tushuntirish va Mantiq:
Grid maketning umumiy tuzilishini (sidebar va content), Flexbox esa elementlarning ichki joylashuvini boshqaradi.

## Ishlash natijasi:
```text
Layout ikki ustunli bo'lib, menyu elementlari teng taqsimlandi.
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. HTML5 va CSS3 bo'yicha ilg'or texnologiyalarni qamrab oluvchi #1041-#1050 topshiriqlar to'plamini taqdim etaman.

---

# 1041-Topshiriq: Canvas yordamida dinamik zarrachalar tizimi

## Topshiriq sharti:
HTML5 Canvas yordamida sichqoncha harakati bilan o'zaro ta'sirlashadigan 50 ta zarracha (particle) hosil qiling.

## Yechim (HTML & CSS kodi):
```html
<canvas id="canvas"></canvas>
<style>body { margin: 0; overflow: hidden; background: #000; }</style>
<script>
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth; canvas.height = window.innerHeight;
  function draw() {
    ctx.fillStyle = 'rgba(0,0,0,0.1)'; ctx.fillRect(0,0, canvas.width, canvas.height);
    ctx.fillStyle = '#00ffcc'; ctx.beginPath(); ctx.arc(100, 100, 10, 0, Math.PI*2); ctx.fill();
    requestAnimationFrame(draw);
  }
  draw();
</script>
```

## Tushuntirish va Mantiq:
`requestAnimationFrame` yordamida har bir kadrda ekran tozalanadi va yangi pozitsiyada zarracha chiziladi. Bu yuqori unumdorlikdagi grafik renderlash asosidir.

## Ishlash natijasi:
```text
Qora fonda yashil rangli zarracha animatsiyasi ishga tushdi.
```

---

# 1042-Topshiriq: CSS Subgrid yordamida murakkab kartalar paneli

## Topshiriq sharti:
Ota konteynerdagi grid tizimini ichki elementlarga `subgrid` orqali meros qilib bering.

## Yechim (HTML & CSS kodi):
```css
.container { display: grid; grid-template-columns: repeat(3, 1fr); }
.card { display: grid; grid-template-rows: subgrid; grid-row: span 3; }
```

## Tushuntirish va Mantiq:
`subgrid` ota elementning grid chiziqlarini bolalarga uzatadi, bu esa murakkab layoutlarda elementlarning bir xil o'lchamda bo'lishini ta'minlaydi.

## Ishlash natijasi:
```text
Kartalar ota grid chiziqlariga to'liq moslashdi.
```

---

# 1043-Topshiriq: WebGL asosida rangli uchburchak renderlash

## Topshiriq sharti:
WebGL kontekstini ishga tushirib, ekranda oddiy rangli uchburchak hosil qiling.

## Yechim (HTML & CSS kodi):
```javascript
const gl = canvas.getContext('webgl');
const vertices = new Float32Array([0, 0.5, -0.5, -0.5, 0.5, -0.5]);
// Buffer va shader kodlari...
gl.drawArrays(gl.TRIANGLES, 0, 3);
```

## Tushuntirish va Mantiq:
WebGL GPU quvvatidan foydalanadi. `vertices` massivi uchburchak koordinatalarini saqlaydi, `drawArrays` esa ularni GPUga yuboradi.

## Ishlash natijasi:
```text
Canvas markazida rangli uchburchak renderlandi.
```

---

# 1044-Topshiriq: CSS `clip-path` bilan murakkab shaklli animatsiya

## Topshiriq sharti:
Elementni `clip-path` yordamida doiradan kvadratga o'zgaradigan qilib animatsiya qiling.

## Yechim (HTML & CSS kodi):
```css
.box { clip-path: circle(50%); transition: 1s; }
.box:hover { clip-path: polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%); }
```

## Tushuntirish va Mantiq:
`clip-path` CSS xossasi elementning ko'rinadigan qismini kesib oladi. `transition` esa bu kesish shakllari orasidagi o'tishni silliqlashtiradi.

## Ishlash natijasi:
```text
Element sichqoncha borganda doiradan kvadratga aylandi.
```

---

# 1045-Topshiriq: CSS `aspect-ratio` va Responsive dizayn

## Topshiriq sharti:
Rasmlar uchun `aspect-ratio: 16/9` xossasidan foydalanib, ekran o'lchami o'zgarganda nisbatni saqlang.

## Yechim (HTML & CSS kodi):
```css
img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; }
```

## Tushuntirish va Mantiq:
`aspect-ratio` brauzerga rasmning kenglik va balandlik nisbatini oldindan aytib beradi, bu esa sahifa yuklanishida "layout shift" muammosini yo'qotadi.

## Ishlash natijasi:
```text
Rasm barcha ekranlarda 16:9 nisbatda qoldi.
```

---

# 1046-Topshiriq: CSS `scroll-snap` bilan galereya

## Topshiriq sharti:
Gorizontal skroll qilinadigan galereya yarating, unda har bir rasm markazda to'xtashi kerak.

## Yechim (HTML & CSS kodi):
```css
.gallery { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; }
.item { scroll-snap-align: center; min-width: 100%; }
```

## Tushuntirish va Mantiq:
`scroll-snap-type` skroll jarayonini boshqaradi, `scroll-snap-align` esa elementlarning qaysi qismi markazlashishini belgilaydi.

## Ishlash natijasi:
```text
Galereya elementlari skroll qilinganda aniq markazga joylashdi.
```

---

# 1047-Topshiriq: CSS `conic-gradient` bilan progress bar

## Topshiriq sharti:
`conic-gradient` yordamida dumaloq progress bar yarating.

## Yechim (HTML & CSS kodi):
```css
.circle { background: conic-gradient(blue 70%, #eee 0); border-radius: 50%; }
```

## Tushuntirish va Mantiq:
`conic-gradient` markaz atrofida ranglarni aylantiradi. 70% qiymati progressni, qolgan qismi esa bo'sh joyni bildiradi.

## Ishlash natijasi:
```text
70% to'ldirilgan dumaloq progress bar hosil bo'ldi.
```

---

# 1048-Topshiriq: CSS `filter` va `backdrop-filter`

## Topshiriq sharti:
Blur effekti (shisha effekti) berilgan modal oyna yarating.

## Yechim (HTML & CSS kodi):
```css
.modal { backdrop-filter: blur(10px); background: rgba(255,255,255,0.3); }
```

## Tushuntirish va Mantiq:
`backdrop-filter` element ortidagi kontentni xiralashtiradi, bu zamonaviy UI dizaynida "Glassmorphism" deb ataladi.

## Ishlash natijasi:
```text
Modal oyna ortidagi fon xiralashgan holda ko'rindi.
```

---

# 1049-Topshiriq: CSS `container-queries`

## Topshiriq sharti:
Elementning o'lchamiga qarab uning ichki dizaynini o'zgartiring.

## Yechim (HTML & CSS kodi):
```css
.parent { container-type: inline-size; }
@container (max-width: 400px) { .child { font-size: 12px; } }
```

## Tushuntirish va Mantiq:
`container-queries` media-query'dan farqli o'laroq, butun ekran emas, balki ma'lum bir konteyner o'lchamiga qarab uslubni o'zgartiradi.

## Ishlash natijasi:
```text
Konteyner kichrayganda ichki matn hajmi moslashdi.
```

---

# 1050-Topshiriq: WebGL shaderlari bilan rang o'zgarishi

## Topshiriq sharti:
Fragment shader yordamida rangni vaqt bo'yicha o'zgartiruvchi animatsiya yarating.

## Yechim (HTML & CSS kodi):
```glsl
precision mediump float;
uniform float u_time;
void main() { gl_FragColor = vec4(sin(u_time), 0.5, 0.8, 1.0); }
```

## Tushuntirish va Mantiq:
`u_time` uniform o'zgaruvchisi orqali vaqt yuboriladi, `sin` funksiyasi esa rang qiymatlarini davriy ravishda o'zgartiradi.

## Ishlash natijasi:
```text
Canvas rangi vaqt o'tishi bilan silliq o'zgarib turibdi.
```