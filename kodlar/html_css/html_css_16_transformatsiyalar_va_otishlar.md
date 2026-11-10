# HTML va CSS: Transformatsiyalar va O'tishlar (Topshiriqlar 751 - 800)

# 751-Topshiriq: Transition asoslari: transition-property va transition-duration
## Topshiriq sharti:
Tugma foni sichqoncha olib kelinganda 0.4 soniya davomida silliq o'zgarishini ta'minlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Transition Property and Duration</title>
  <style>
    .smooth-btn {
      background-color: #2563eb;
      color: white;
      border: none;
      padding: 12px 24px;
      border-radius: 6px;
      font-size: 15px;
      cursor: pointer;
      font-family: sans-serif;
      transition-property: background-color;
      transition-duration: 0.4s;
    }
    .smooth-btn:hover {
      background-color: #1e40af;
    }
  </style>
</head>
<body>
  <button class="smooth-btn">Silliq O'tish Tugmasi</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
`transition-property: background-color` qaysi xususiyat silliq o'zgarishini belgilaydi, `transition-duration: 0.4s` esa o'tish davomiyligini ko'rsatadi. Bu holatda rang to'satdan emas, 0.4 soniya ichida mayin almashadi.

## Ishlash natijasi:
```text
Tugma ustiga kursor borganda uning ko'k rangi sekinlik bilan to'q ko'k rangga o'tadi.
```

---

# 752-Topshiriq: Transition-timing-function (ease, linear, ease-in, ease-out)
## Topshiriq sharti:
Turli vaqt tezlashuv egri chiziqlariga ega bo'lgan 4 ta qutining harakatlanishini namoyish eting.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Transition Timing Functions</title>
  <style>
    .track {
      width: 280px;
      background: #f1f5f9;
      padding: 10px;
      border-radius: 8px;
      font-family: sans-serif;
    }
    .bar {
      width: 40px;
      height: 24px;
      color: white;
      font-size: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 6px;
      border-radius: 4px;
      transition: width 1s;
    }
    .track:hover .bar { width: 100%; }
    .b-linear { background: #ef4444; transition-timing-function: linear; }
    .b-ease { background: #3b82f6; transition-timing-function: ease; }
    .b-in { background: #10b981; transition-timing-function: ease-in; }
    .b-out { background: #f59e0b; transition-timing-function: ease-out; }
  </style>
</head>
<body>
  <div class="track">
    <div class="bar b-linear">linear</div>
    <div class="bar b-ease">ease</div>
    <div class="bar b-in">ease-in</div>
    <div class="bar b-out">ease-out</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`linear` o'zgarmas tezlikda harakatlanadi, `ease` sekin boshlanib tezlashadi va sekinlashib tugaydi, `ease-in` sekin boshlanadi, `ease-out` esa sekin tugaydi.

## Ishlash natijasi:
```text
Kulrang maydonga kursor tushganda 4 xil rangli tasmalar turli tezlik profilida o'ngga qarab cho'ziladi.
```

---

# 753-Topshiriq: Transition-delay bilan animatsiyani kechiktirib ishga tushirish
## Topshiriq sharti:
Kursor tekkandan so'ng 0.3 soniya kutib, keyin 0.5 soniyada kattalashadigan karta yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Transition Delay</title>
  <style>
    .delay-card {
      width: 140px;
      padding: 16px;
      background: #8b5cf6;
      color: white;
      border-radius: 8px;
      text-align: center;
      font-family: sans-serif;
      transition: transform 0.5s ease 0.3s; /* 0.3s kechikish */
    }
    .delay-card:hover {
      transform: scale(1.15);
    }
  </style>
</head>
<body>
  <div class="delay-card">0.3s kechikish</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`transition: transform 0.5s ease 0.3s` qoidasidagi to'rtinchi parametr (`0.3s`) kechikish vaqti hisoblanadi. Foydalanuvchi tasodifan teginib ketganda darhol animatsiya boshlanishini oldini oladi.

## Ishlash natijasi:
```text
Karta ustiga kursor kelganda 0.3 soniyalik sokinlikdan so'ng u silliq 1.15 barobar kattalashadi.
```

---

# 754-Topshiriq: Bir nechta xususiyatlar uchun alohida transition belgilash
## Topshiriq sharti:
background-color 0.3s da, transform esa 0.5s da mustaqil o'tishini ta'minlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Multiple Transitions</title>
  <style>
    .multi-btn {
      background-color: #0284c7;
      color: white;
      padding: 12px 20px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-family: sans-serif;
      transition: background-color 0.3s ease, transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .multi-btn:hover {
      background-color: #0369a1;
      transform: translateY(-4px);
    }
  </style>
</head>
<body>
  <button class="multi-btn">Ko'p Qirrali O'tish</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
Vergul orqali turli CSS xususiyatlariga o'ziga xos davomiylik va timing-funksiya berish mumkin. Bu elementga tabiiy va professional hissiyot bag'ishlaydi.

## Ishlash natijasi:
```text
Tugma rangi 0.3s da to'qroq bo'ladi, o'zi esa 0.5s ichida prujinasimon tepaga sakrab ko'tariladi.
```

---

# 755-Topshiriq: Transform: translate (translateX va translateY) bilan siljitish
## Topshiriq sharti:
Elementni o'z o'rnidan o'ngga 30px va pastga 15px suring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Transform Translate</title>
  <style>
    .trans-box {
      width: 160px;
      padding: 14px;
      background: #10b981;
      color: white;
      border-radius: 6px;
      font-family: sans-serif;
      transform: translate(30px, 15px);
    }
  </style>
</head>
<body>
  <div class="trans-box">translate(30px, 15px)</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`transform: translate(x, y)` elementni sahifa oqimini buzmasdan geometrik siljitadi. Bu `top/left` siljitishlaridan farqli ravishda brauzerning GPU tezlatgichida ishlaydi va o'ta yuqori unumdorlik (60fps) beradi.

## Ishlash natijasi:
```text
Yashil quti o'zining tabiiy o'rnidan 30px o'ngga va 15px pastga surilgan holda turadi.
```

---

# 756-Topshiriq: Transform: rotate (2D Aylantirish)
## Topshiriq sharti:
Elementni soat yo'nalishi bo'yicha 45 gradusga burib ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Transform Rotate</title>
  <style>
    .rotate-box {
      width: 90px;
      height: 90px;
      background: #f59e0b;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 8px;
      font-family: sans-serif;
      margin: 40px;
      transform: rotate(45deg);
    }
  </style>
</head>
<body>
  <div class="rotate-box">45&deg;</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`transform: rotate(45deg)` elementni o'z markazi atrofida 45 gradus burchakka buradi. Manfiy graduslar (masalan `-45deg`) esa soat strelkasiga qarshi buradi.

## Ishlash natijasi:
```text
To'rtburchak sariq quti romb shaklida 45 gradus burchakka burilib ko'rinadi.
```

---

# 757-Topshiriq: Transform: scale (Masshtabni kattalashtirish va kichraytirish)
## Topshiriq sharti:
Kursor olib kelinganda karta masshtabi 1.1 barobar kattalashishini bajaring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Transform Scale</title>
  <style>
    .zoom-card {
      width: 160px;
      padding: 16px;
      background: #ec4899;
      color: white;
      border-radius: 8px;
      text-align: center;
      font-family: sans-serif;
      transition: transform 0.3s ease;
      cursor: pointer;
    }
    .zoom-card:hover {
      transform: scale(1.1);
    }
  </style>
</head>
<body>
  <div class="zoom-card">scale(1.1)</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`transform: scale(1.1)` elementning o'lchamini barcha o'qlar bo'yicha 10 foizga kattalashtiradi. Qo'shni elementlarning o'rniga ta'sir qilmaydi.

## Ishlash natijasi:
```text
Pushti quti ustiga kelganda silliq 1.1 barobar kattalashib diqqatni tortadi.
```

---

# 758-Topshiriq: Transform: skew (Qiyalashtirish)
## Topshiriq sharti:
Elementni gorizontal o'q bo'yicha -15 gradusga qiyalashtirib zamonaviy parallelogramm hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Transform Skew</title>
  <style>
    .skew-badge {
      display: inline-block;
      background: #0f172a;
      color: white;
      padding: 10px 24px;
      font-family: sans-serif;
      font-weight: bold;
      transform: skewX(-15deg);
      border-radius: 4px;
      margin: 20px;
    }
    .skew-content {
      display: inline-block;
      transform: skewX(15deg); /* Ichki matn qiyalanib ketmasligi uchun kompensatsiya */
    }
  </style>
</head>
<body>
  <div class="skew-badge">
    <span class="skew-content">YANGI TAKLIF</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`transform: skewX(-15deg)` qutini qiya parallelogrammga aylantiradi. Ichki matnga aksincha `skewX(15deg)` berilsa, quti qiya bo'lsa-da matn to'g'ri va o'qishli qoladi.

## Ishlash natijasi:
```text
Sport va kiberxavfsizlik brendlari uslubidagi qiya qora lentali nishon.
```

---

# 759-Topshiriq: Bir nechta transformatsiyalarni birlashtirish (Chaining Transforms)
## Topshiriq sharti:
Bitta qatorda rotate, scale va translateY ni ketma-ket qo'llang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Chaining Transforms</title>
  <style>
    .combo-btn {
      padding: 12px 24px;
      background: #6366f1;
      color: white;
      border: none;
      border-radius: 6px;
      font-family: sans-serif;
      cursor: pointer;
      transition: transform 0.3s;
    }
    .combo-btn:hover {
      transform: translateY(-5px) scale(1.05) rotate(2deg);
    }
  </style>
</head>
<body>
  <button class="combo-btn">Kompleks Harakat</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
Transformatsiyalar bo'sh joy bilan ketma-ket yoziladi: `transform: translateY(-5px) scale(1.05) rotate(2deg)`. Ular chapdan o'ngga qarab bajariladi.

## Ishlash natijasi:
```text
Tugma ustiga kursor borganda u bir vaqtning o'zida ko'tariladi, kattalashadi va biroz qiyalanadi.
```

---

# 760-Topshiriq: Transform-origin xususiyati (Aylanish nuqtasini o'zgartirish)
## Topshiriq sharti:
Elementning markazdan emas, balki yuqori chap burchagidan (top left) aylanib osilishini bajaring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Transform Origin</title>
  <style>
    .hinge-box {
      width: 140px;
      padding: 14px;
      background: #dc2626;
      color: white;
      border-radius: 6px;
      font-family: sans-serif;
      margin: 30px;
      transform-origin: top left;
      transition: transform 0.5s ease;
      cursor: pointer;
    }
    .hinge-box:hover {
      transform: rotate(25deg);
    }
  </style>
</head>
<body>
  <div class="hinge-box">Origin: Top Left</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Sukut bo'yicha `transform-origin: 50% 50%` bo'ladi. `top left` berilsa, element yuqori chap burchagidan mixlangan osma lavha kabi aylanadi.

## Ishlash natijasi:
```text
Qizil to'rtburchak ustiga kelganda yuqori chap nuqtasi qotib turgan holda pastga qiya osilib tushadi.
```

---

# 761-Topshiriq: Rasm galereyasida silliq Zoom In effekti (Image Hover Zoom)
## Topshiriq sharti:
Karta o'lchami o'zgarmasdan (overflow: hidden), ichidagi rasm hover paytida 1.15 barobar kattalashsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Image Hover Zoom</title>
  <style>
    .img-container {
      width: 220px;
      height: 140px;
      border-radius: 8px;
      overflow: hidden;
      cursor: pointer;
    }
    .zoom-bg {
      width: 100%;
      height: 100%;
      background: #0284c7;
      transition: transform 0.4s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-family: sans-serif;
    }
    .img-container:hover .zoom-bg {
      transform: scale(1.15);
    }
  </style>
</head>
<body>
  <div class="img-container">
    <div class="zoom-bg">Rasm foni</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ota blokdagi `overflow: hidden` rasmni ramka chegarasidan chiqib ketishiga yo'l qo'ymaydi, ichki rasm esa `scale(1.15)` orqali mayin kattalashadi.

## Ishlash natijasi:
```text
Karta hoshiyasi buzilmagan holda uning ichidagi ko'k fon silliq kattalashadi.
```

---

# 762-Topshiriq: Hamburger menyuning 'X' yopish belgisiga aylanishi
## Topshiriq sharti:
3 ta gorizontal chiziqcha bosilganda yoki hoverda aylanib 'X' belgisini hosil qilsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Hamburger to X</title>
  <style>
    .hamburger {
      width: 32px;
      height: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      cursor: pointer;
    }
    .bar {
      height: 4px;
      width: 100%;
      background: #1e293b;
      border-radius: 2px;
      transition: transform 0.3s ease, opacity 0.3s ease;
    }
    .hamburger:hover .bar:nth-child(1) {
      transform: translateY(10px) rotate(45deg);
    }
    .hamburger:hover .bar:nth-child(2) {
      opacity: 0;
    }
    .hamburger:hover .bar:nth-child(3) {
      transform: translateY(-10px) rotate(-45deg);
    }
  </style>
</head>
<body>
  <div class="hamburger">
    <div class="bar"></div>
    <div class="bar"></div>
    <div class="bar"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
1-chiziq pastga tushib 45 gradus buriladi, 2-chiziq shaffof bo'lib yo'qoladi, 3-chiziq esa tepaga chiqib -45 gradus buriladi va mukammal 'X' belgisi vujudga keladi.

## Ishlash natijasi:
```text
3 ta qora chiziqcha ustiga kelganda silliq 'X' shakliga kiradi.
```

---

# 763-Topshiriq: 3D Transform Asoslari: Perspective va RotateY
## Topshiriq sharti:
Konteynerga perspective berib, kartani Y o'qi bo'ylab 3D fazoda 35 gradus burang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>3D Perspective Rotate</title>
  <style>
    .scene {
      perspective: 600px; /* 3D fazo chuqurligi */
      width: fit-content;
      margin: 40px;
    }
    .card-3d {
      width: 160px;
      padding: 24px;
      background: #3b82f6;
      color: white;
      border-radius: 8px;
      font-family: sans-serif;
      text-align: center;
      transform: rotateY(35deg);
      transition: transform 0.5s;
    }
    .scene:hover .card-3d {
      transform: rotateY(0deg);
    }
  </style>
</head>
<body>
  <div class="scene">
    <div class="card-3d">3D RotateY (35&deg;)</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`perspective: 600px` ko'rish nuqtasining ekrandan masofasini belgilaydi. Usiz `rotateY` shunchaki tekis siqilish kabi ko'rinardi, perspective bilan esa haqiqiy 3D chuqurlik vujudga keladi.

## Ishlash natijasi:
```text
Ko'k to'rtburchak 3D fazoda o'ng qirrasi uzoqlashgan burchakda turadi, ustiga borganda tekislanadi.
```

---

# 764-Topshiriq: 3D Flip Card (Aylanuvchi ikki tomonli karta)
## Topshiriq sharti:
Kursor tekkanda 180 gradus aylanib, orqa tomonidagi ma'lumotni ko'rsatuvchi karta yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>3D Flip Card</title>
  <style>
    .flip-box {
      width: 180px;
      height: 120px;
      perspective: 1000px;
      font-family: sans-serif;
    }
    .flip-inner {
      position: relative;
      width: 100%;
      height: 100%;
      transform-style: preserve-3d;
      transition: transform 0.6s;
    }
    .flip-box:hover .flip-inner {
      transform: rotateY(180deg);
    }
    .face {
      position: absolute;
      inset: 0;
      backface-visibility: hidden;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: bold;
    }
    .front { background: #4f46e5; }
    .back { background: #059669; transform: rotateY(180deg); }
  </style>
</head>
<body>
  <div class="flip-box">
    <div class="flip-inner">
      <div class="face front">Old tomoni</div>
      <div class="face back">Orqa tomoni</div>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`transform-style: preserve-3d` bolalarning 3D fazosini saqlaydi, `backface-visibility: hidden` esa teskari o'girilgan yuzning ko'rinmasligini ta'minlaydi.

## Ishlash natijasi:
```text
Binafsha rangli 'Old tomoni' kartasi ustiga kursor borganda aylanib yashil 'Orqa tomoni' ochiladi.
```

---

# 765-Topshiriq: Cubic-bezier() bilan prujinali (Bounce/Elastic) sakrash effekti
## Topshiriq sharti:
Tugma bosilganda yoki hover bo'lganda rezinasimon tebranuvchi cubic-bezier egri chizig'ini qo'llang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Cubic Bezier Bounce</title>
  <style>
    .bounce-btn {
      padding: 12px 24px;
      background: #7c3aed;
      color: white;
      border: none;
      border-radius: 30px;
      font-family: sans-serif;
      font-weight: bold;
      cursor: pointer;
      transition: transform 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    .bounce-btn:hover {
      transform: scale(1.18);
    }
  </style>
</head>
<body>
  <button class="bounce-btn">Prujina Effekti</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
`cubic-bezier(0.68, -0.55, 0.265, 1.55)` egri chizig'idagi 1 dan katta qiymat elementni oldin mo'ljaldan oshirib, so'ng joyiga qaytaradi (overshoot/bounce effekti).

## Ishlash natijasi:
```text
Tugma ustiga kursor borganda u to'satdan shishib ketib, so'ng elastik holatda qotadi.
```

---

# 766-Topshiriq: Kartochkalar hover micro-interaction: Ko'tarilish va soya
## Topshiriq sharti:
translateY(-6px) va box-shadow orqali professional interfeys hover reaksiyasini quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Card Lift Interaction</title>
  <style>
    .lift-card {
      width: 200px;
      padding: 18px;
      background: white;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      font-family: sans-serif;
      box-shadow: 0 2px 4px rgba(0,0,0,0.04);
      transition: transform 0.25s ease, box-shadow 0.25s ease;
      cursor: pointer;
    }
    .lift-card:hover {
      transform: translateY(-6px);
      box-shadow: 0 12px 20px rgba(0,0,0,0.1);
    }
  </style>
</head>
<body>
  <div class="lift-card">
    <h4 style="margin: 0 0 6px 0;">CSS Kursi</h4>
    <p style="margin: 0; font-size: 13px; color: #64748b;">Yuqori darajadagi zamonaviy uslublar.</p>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`transform: translateY(-6px)` va `box-shadow` birgalikda elementning stoldan yuqoriga ko'tarilgani illyuziyasini hosil qiladi.

## Ishlash natijasi:
```text
Karta ustiga kursor tekkanda u ohista 6px yuqoriga ko'tarilib, ostiga yumshoq chuqur soya tushadi.
```

---

# 767-Topshiriq: Transform: rotateX bilan pastdan ochiluvchi menyu (Dropdown Flip)
## Topshiriq sharti:
Menyu ro'yxatini rotateX(-90deg) dan 0deg ga silliq yoyib oching.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Dropdown RotateX</title>
  <style>
    .menu-parent {
      position: relative;
      display: inline-block;
      perspective: 500px;
      font-family: sans-serif;
    }
    .menu-panel {
      position: absolute;
      top: 100%;
      left: 0;
      width: 140px;
      background: #1e293b;
      color: white;
      padding: 10px;
      border-radius: 6px;
      transform-origin: top center;
      transform: rotateX(-90deg);
      opacity: 0;
      transition: transform 0.4s ease, opacity 0.3s;
    }
    .menu-parent:hover .menu-panel {
      transform: rotateX(0deg);
      opacity: 1;
    }
  </style>
</head>
<body>
  <div class="menu-parent">
    <button style="padding: 10px 16px; cursor: pointer;">Bo'limlar &#9662;</button>
    <div class="menu-panel">
      <div>HTML</div>
      <div style="margin-top: 6px;">CSS</div>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`transform-origin: top center` menyuning yuqori chetiga ilashib ochilishini ta'minlaydi, `rotateX(-90deg)` esa uni ko'rinmas qilib yuqoriga yig'ib turadi.

## Ishlash natijasi:
```text
Tugma ustiga borganda qora menyu paneli eshikdek pastga qarab silliq tushadi.
```

---

# 768-Topshiriq: Aylanuvchi ikonka bilan Accordion strelkasi
## Topshiriq sharti:
Panel ochilganda pastga qaragan strelka 180 gradus aylanib yuqoriga qarasin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Accordion Arrow Rotate</title>
  <style>
    .acc-btn {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 220px;
      padding: 12px;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      font-family: sans-serif;
      cursor: pointer;
    }
    .arrow-icon {
      transition: transform 0.3s ease;
      font-size: 12px;
    }
    .acc-btn:hover .arrow-icon {
      transform: rotate(180deg);
    }
  </style>
</head>
<body>
  <div class="acc-btn">
    <span>Savol matni</span>
    <span class="arrow-icon">&#9660;</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`transform: rotate(180deg)` ikonkani o'z o'qi atrofida silliq teskari qaratadi. Bu zamonaviy akkordeonlarning ajralmas mikro-harakatidir.

## Ishlash natijasi:
```text
Kursor tekkanda pastga qaragan qora uchburchak silliq aylanib yuqoriga qaraydi.
```

---

# 769-Topshiriq: Tugma ichidagi chiziq nuri effekti (Shine / Shimmer Hover)
## Topshiriq sharti:
Hover paytida tugma ustidan oq nurli chiziq translateX bilan tezda o'tib ketsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Button Shine Hover</title>
  <style>
    .shine-btn {
      position: relative;
      padding: 12px 28px;
      background: #0f172a;
      color: white;
      border: none;
      border-radius: 6px;
      font-family: sans-serif;
      font-weight: bold;
      overflow: hidden;
      cursor: pointer;
    }
    .shine-btn::before {
      content: "";
      position: absolute;
      top: 0;
      left: -100%;
      width: 60%;
      height: 100%;
      background: linear-gradient(120deg, transparent, rgba(255,255,255,0.4), transparent);
      transform: skewX(-25deg);
      transition: transform 0.6s ease;
    }
    .shine-btn:hover::before {
      transform: translateX(350%) skewX(-25deg);
    }
  </style>
</head>
<body>
  <button class="shine-btn">Yaltirovchi Tugma</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
Qiyalatilgan yarim shaffof oq tasma `translateX` orqali butun tugma ustidan chopib o'tadi va metall nuri tovlanishi effektini hosil qiladi.

## Ishlash natijasi:
```text
Qora tugma ustiga kursor tekkanda uning yuzasidan oq yaltiroq nur sirpanib o'tadi.
```

---

# 770-Topshiriq: Isometrik 3D Karta (Isometric Transform)
## Topshiriq sharti:
rotateX, rotateZ va scale kombinatsiyasi orqali kartani isometrik 3D proyeksiyaga joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Isometric Card</title>
  <style>
    .iso-stage {
      margin: 40px;
    }
    .iso-card {
      width: 160px;
      height: 100px;
      background: #3b82f6;
      color: white;
      padding: 16px;
      border-radius: 8px;
      font-family: sans-serif;
      transform: rotateX(55deg) rotateZ(-45deg);
      box-shadow: -10px 10px 0 #1d4ed8;
      transition: transform 0.4s;
    }
    .iso-card:hover {
      transform: rotateX(55deg) rotateZ(-45deg) translateZ(20px);
    }
  </style>
</head>
<body>
  <div class="iso-stage">
    <div class="iso-card">Isometrik 3D</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`rotateX(55deg) rotateZ(-45deg)` klassik isometrik o'yinlar va zamonaviy UI illyustratsiyalaridagi 3D yotgan quti effektini hosil qiladi.

## Ishlash natijasi:
```text
Fazoda diagonal qiya yotgan 3D ko'k karta va uning to'q ko'k qalin qirrasi.
```

---

# 771-Topshiriq: Silliq kattalashuvchi Modal oyna (Scale & Opacity Transition)
## Topshiriq sharti:
Modal darchasi sukutda scale(0.8) va opacity: 0 bo'lib, ochilganda scale(1) ga silliq o'tsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Modal Scale Transition</title>
  <style>
    .modal-box {
      width: 240px;
      padding: 20px;
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.1);
      font-family: sans-serif;
      transform: scale(0.85);
      opacity: 0.5;
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.3s ease;
      cursor: pointer;
    }
    .modal-box:hover {
      transform: scale(1);
      opacity: 1;
    }
  </style>
</head>
<body>
  <div class="modal-box">
    <h4>Diqqat</h4>
    <p style="font-size: 13px; color: #64748b;">Kursor kelganda to'liq o'lchamga kattalashadi.</p>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`scale(0.85)` va `opacity: 0.5` dan `scale(1)` va `opacity: 1` ga o'tish dasturiy darchalarning foydalanuvchiga qarab ochilish hissiyotini beradi.

## Ishlash natijasi:
```text
Karta ustiga kelganda u ichkaridan tashqariga qarab kattalashib ravshan tortadi.
```

---

# 772-Topshiriq: Avatarlar guruhi hoverda yoyilishi (Stack to Spread)
## Topshiriq sharti:
Ustma-ust turgan 3 ta avatarga kursor kelganda translateX bilan yon tomonga yoyilib ochilsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Avatar Spread</title>
  <style>
    .avatar-stack {
      display: flex;
      padding: 20px;
      font-family: sans-serif;
    }
    .av {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      border: 2px solid white;
      margin-left: -15px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: bold;
      transition: transform 0.3s ease;
    }
    .av:first-child { margin-left: 0; }
    .avatar-stack:hover .av-2 { transform: translateX(10px); }
    .avatar-stack:hover .av-3 { transform: translateX(20px); }
  </style>
</head>
<body>
  <div class="avatar-stack">
    <div class="av" style="background:#ef4444;">A</div>
    <div class="av av-2" style="background:#10b981;">B</div>
    <div class="av av-3" style="background:#3b82f6;">C</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`translateX` siljishlari avatarlarni bir-birining ortidan yoyib ko'rsatadi, har bir foydalanuvchi alohida ko'rinadi.

## Ishlash natijasi:
```text
Birlashgan uch doira ustiga kursor tushganda ular o'ng tomonga qarab bir tekisda yoyiladi.
```

---

# 773-Topshiriq: Tugma bosilishi reaksiyasi (Active state transform scale: 0.95)
## Topshiriq sharti:
Tugma bosilgan onda (:active) biroz ichkariga ezilib bosilish effektini bering.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Button Click Press Effect</title>
  <style>
    .press-btn {
      padding: 12px 24px;
      background: #2563eb;
      color: white;
      border: none;
      border-radius: 6px;
      font-family: sans-serif;
      font-weight: bold;
      cursor: pointer;
      transition: transform 0.1s ease;
    }
    .press-btn:active {
      transform: scale(0.95);
    }
  </style>
</head>
<body>
  <button class="press-btn">Meni Bosing</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:active` holatida `scale(0.95)` tugmaga taktil (fizik tugma bosilishiga o'xshash) hissiyot beradi.

## Ishlash natijasi:
```text
Tugmaga sichqoncha bosilganda u biroz qisqarib ichkariga kiradi.
```

---

# 774-Topshiriq: Matn ostidagi chiziqning chapdan o'ngga qarab chizilishi
## Topshiriq sharti:
Havola ostidagi chiziq transform scaleX(0) dan scaleX(1) ga silliq cho'zilsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Underline ScaleX</title>
  <style>
    .fancy-link {
      position: relative;
      text-decoration: none;
      color: #0f172a;
      font-family: sans-serif;
      font-weight: bold;
      font-size: 16px;
    }
    .fancy-link::after {
      content: "";
      position: absolute;
      bottom: -4px;
      left: 0;
      width: 100%;
      height: 2px;
      background: #2563eb;
      transform: scaleX(0);
      transform-origin: bottom left;
      transition: transform 0.3s ease;
    }
    .fancy-link:hover::after {
      transform: scaleX(1);
    }
  </style>
</head>
<body>
  <a href="#" class="fancy-link">Zamonaviy Havola</a>
</body>
</html>
```

## Tushuntirish va Mantiq:
`transform: scaleX(0)` boshida chiziqni ko'rinmas qiladi, hover bo'lganda `transform-origin: bottom left` tufayli u chapdan o'ngga qarab yugurib chiziladi.

## Ishlash natijasi:
```text
Matn ustiga kursor kelganda uning ostida chapdan o'ngga qarab ko'k chiziqcha tortiladi.
```

---

# 775-Topshiriq: Ijtimoiy tarmoq ikonkalarining hoverda aylanib rang olishi
## Topshiriq sharti:
Ikonka hoverda rotate(360deg) bilan aylanib, fonini yashil rangga o'tkazsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Social Icon Spin</title>
  <style>
    .social-circle {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: #e2e8f0;
      color: #334155;
      text-decoration: none;
      font-size: 18px;
      transition: transform 0.4s ease, background-color 0.4s ease, color 0.4s;
    }
    .social-circle:hover {
      transform: rotate(360deg);
      background-color: #10b981;
      color: white;
    }
  </style>
</head>
<body>
  <a href="#" class="social-circle">&#9993;</a>
</body>
</html>
```

## Tushuntirish va Mantiq:
`transform: rotate(360deg)` to'liq bir aylanish yasaydi, transition orqali rang ham bir vaqtda silliq o'zgaradi.

## Ishlash natijasi:
```text
Kulrang xat belgisi ustiga borganda aylanib yashil fonga o'tadi.
```

---

# 776-Topshiriq: Quyi qatlamli xabarnoma darchasining tepaga sirpanib chiqishi
## Topshiriq sharti:
Toast xabari translateY(100%) dan translateY(0) ga silliq ko'tarilsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Toast Notification Slide</title>
  <style>
    .toast-box {
      width: 220px;
      padding: 12px 16px;
      background: #1e293b;
      color: white;
      border-radius: 6px;
      font-family: sans-serif;
      transform: translateY(20px);
      opacity: 0.2;
      transition: transform 0.3s ease, opacity 0.3s ease;
      cursor: pointer;
    }
    .toast-box:hover {
      transform: translateY(0);
      opacity: 1;
    }
  </style>
</head>
<body>
  <div class="toast-box">Muvaffaqiyatli saqlandi!</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`translateY` va `opacity` kombinatsiyasi barcha zamonaviy bildirishnomalar (toasts, alerts) uchun standart animatsiyadir.

## Ishlash natijasi:
```text
Xira turgan qora xabarnoma qutisi ustiga kelganda yuqoriga sirpanib ravshanlashadi.
```

---

# 777-Topshiriq: 3D Kartaning kursorni kuzatuvchi burchak burilishi (Tilt Effect)
## Topshiriq sharti:
Kartani rotateX(15deg) rotateY(-15deg) bilan qiya 3D fazoda tuting.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Tilt 3D Card</title>
  <style>
    .tilt-wrapper { perspective: 800px; width: fit-content; margin: 30px; }
    .tilt-box {
      width: 180px;
      padding: 20px;
      background: linear-gradient(135deg, #6366f1, #a855f7);
      color: white;
      border-radius: 10px;
      font-family: sans-serif;
      transform: rotateX(15deg) rotateY(-15deg);
      transition: transform 0.3s ease;
    }
    .tilt-wrapper:hover .tilt-box {
      transform: rotateX(0deg) rotateY(0deg);
    }
  </style>
</head>
<body>
  <div class="tilt-wrapper">
    <div class="tilt-box">3D Tilt Kartasi</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`rotateX` va `rotateY` birgalikda kartaning fazodagi 3D burchagini hosil qiladi.

## Ishlash natijasi:
```text
Gradient binafsha karta 3D qiya burchakda turadi, ustiga kelganda to'g'rilanadi.
```

---

# 778-Topshiriq: Rasm kartasining pastki tavsif paneli yuqoriga chiqishi
## Topshiriq sharti:
Karta ichidagi sarlavha paneli translateY(100%) dan translateY(0) ga hoverda chiqsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Slide Up Caption</title>
  <style>
    .card-wrap {
      position: relative;
      width: 200px;
      height: 140px;
      background: #0284c7;
      border-radius: 8px;
      overflow: hidden;
      font-family: sans-serif;
    }
    .slide-panel {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: rgba(15, 23, 42, 0.85);
      color: white;
      padding: 10px;
      transform: translateY(100%);
      transition: transform 0.3s ease;
    }
    .card-wrap:hover .slide-panel {
      transform: translateY(0);
    }
  </style>
</head>
<body>
  <div class="card-wrap">
    <div class="slide-panel">
      <h5 style="margin:0 0 4px 0;">Surat nomi</h5>
      <small>Tavsif matni</small>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Panel karta ostida yashirin turadi va faqat foydalanuvchi kartaga qaraganda yuqoriga sirpanib chiqadi.

## Ishlash natijasi:
```text
Ko'k to'rtburchak ustiga kelganda pastdan qora tavsif paneli ko'tariladi.
```

---

# 779-Topshiriq: Tugma yonidagi strelkaning o'ngga surilishi (Arrow Nudge)
## Topshiriq sharti:
Havoladagi strelka kursor kelganda translateX(6px) ga surilib harakat uyg'otsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Arrow Nudge</title>
  <style>
    .nudge-link {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: #2563eb;
      text-decoration: none;
      font-family: sans-serif;
      font-weight: bold;
    }
    .arrow {
      transition: transform 0.2s ease;
    }
    .nudge-link:hover .arrow {
      transform: translateX(6px);
    }
  </style>
</head>
<body>
  <a href="#" class="nudge-link">
    <span>Barcha kurslar</span>
    <span class="arrow">&rarr;</span>
  </a>
</body>
</html>
```

## Tushuntirish va Mantiq:
`translateX(6px)` foydalanuvchini oldinga intilishga undovchi klassik mikro-harakatdir.

## Ishlash natijasi:
```text
Havola ustiga borganda uning o'ngidagi strelka 6px o'ngga siljiydi.
```

---

# 780-Topshiriq: Transform: scale3d bilan 3D chuqurlikda kattalashtirish
## Topshiriq sharti:
3D fazoda X, Y va Z o'qlari bo'yicha element masshtabini oshiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Scale 3D</title>
  <style>
    .stage { perspective: 500px; width: fit-content; margin: 30px; }
    .box-3d {
      width: 140px;
      padding: 16px;
      background: #e11d48;
      color: white;
      border-radius: 6px;
      font-family: sans-serif;
      transition: transform 0.3s;
    }
    .stage:hover .box-3d {
      transform: scale3d(1.1, 1.1, 1.1);
    }
  </style>
</head>
<body>
  <div class="stage">
    <div class="box-3d">scale3d</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`scale3d(x, y, z)` elementni 3 o'lchamli fazoda masshtablaydi va apparat tezlatgichini to'liq safarbar qiladi.

## Ishlash natijasi:
```text
Qizil quti ustiga kursor kelganda 3D fazoda silliq kattalashadi.
```

---

# 781-Topshiriq: Transform: skewY bilan vertikal qiyalikli qirralar
## Topshiriq sharti:
Bo'lim chegarasini skewY(-3deg) orqali diagonal qiya chiziqqa aylantiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>SkewY Section</title>
  <style>
    .skew-section {
      background: #0f172a;
      color: white;
      padding: 40px 20px;
      transform: skewY(-4deg);
      font-family: sans-serif;
    }
    .unskew {
      transform: skewY(4deg); /* Matn qiya bo'lmasligi uchun qaytariladi */
    }
  </style>
</head>
<body>
  <div class="skew-section">
    <div class="unskew">
      <h3 style="margin:0;">Diagonal Bo'lim</h3>
      <p style="margin:4px 0 0 0; color:#94a3b8;">Zamonaviy landing sahifalari uslubi.</p>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`transform: skewY(-4deg)` butun bo'limning tepa va pastki chegarasini chiroyli diagonalga aylantiradi.

## Ishlash natijasi:
```text
Tepa va pasti qiya kesilgan to'q qora bo'lim, ichidagi matn esa tekis turadi.
```

---

# 782-Topshiriq: Aylanuvchi yuklanish indikatori (CSS Transition Rotate Spinner)
## Topshiriq sharti:
Doira hover bo'lganda 180 gradusga silliq burilsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Rotate Spinner</title>
  <style>
    .spinner-ring {
      width: 40px;
      height: 40px;
      border: 4px solid #cbd5e1;
      border-top-color: #2563eb;
      border-radius: 50%;
      transition: transform 0.6s ease;
      cursor: pointer;
    }
    .spinner-ring:hover {
      transform: rotate(180deg);
    }
  </style>
</head>
<body>
  <div class="spinner-ring"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Chala bo'yalgan aylana burilganda ko'k qismi yarim aylanib o'tadi.

## Ishlash natijasi:
```text
Kulrang-ko'k halqa ustiga kelganda 180 gradusga aylanadi.
```

---

# 783-Topshiriq: Transform translateZ bilan 3D qatlamni oldinga chiqarish
## Topshiriq sharti:
Karta ichidagi sarlavhani 3D chuqurlikda tomoshabinga qarab 30px oldinga suring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>TranslateZ Pop</title>
  <style>
    .card-3d-wrap {
      perspective: 600px;
      width: fit-content;
      margin: 30px;
    }
    .parent-card {
      width: 180px;
      padding: 20px;
      background: #1e293b;
      border-radius: 8px;
      transform-style: preserve-3d;
      transform: rotateX(15deg);
      font-family: sans-serif;
    }
    .pop-text {
      background: #3b82f6;
      color: white;
      padding: 10px;
      border-radius: 4px;
      transform: translateZ(30px); /* 30px oldinga chiqadi */
    }
  </style>
</head>
<body>
  <div class="card-3d-wrap">
    <div class="parent-card">
      <div class="pop-text">translateZ(30px)</div>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`translateZ(30px)` elementni ekrandan foydalanuvchi ko'zi tomon suradi va haqiqiy parvoz effektini beradi.

## Ishlash natijasi:
```text
To'q qora karta fonidan ko'k matn bo'rtib oldinga chiqib turadi.
```

---

# 784-Topshiriq: Hoverda rangli chegara qalinlashishi va transformatsiyasi
## Topshiriq sharti:
Kursor borganda chegarasi kattalashib ko'tariluvchi qidiruv inputi yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Focus Transform Input</title>
  <style>
    .fancy-input {
      width: 220px;
      padding: 10px 14px;
      border: 2px solid #cbd5e1;
      border-radius: 6px;
      outline: none;
      font-family: sans-serif;
      transition: border-color 0.2s, transform 0.2s;
    }
    .fancy-input:focus {
      border-color: #2563eb;
      transform: scale(1.02);
    }
  </style>
</head>
<body>
  <input type="text" class="fancy-input" placeholder="Inputga bosing...">
</body>
</html>
```

## Tushuntirish va Mantiq:
Input aktiv bo'lganda `scale(1.02)` va ko'k rang bilan foydalanuvchiga faollikni bildiradi.

## Ishlash natijasi:
```text
Input ichiga bosilganda u biroz kattalashadi va ko'k ramkaga kiradi.
```

---

# 785-Topshiriq: Karta burchagidagi nishonning qiya burilishi (Badge Rotate)
## Topshiriq sharti:
Nishonni -10 gradusga burib karta ustiga zamonaviy stiker kabi yopishtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Sticker Badge Rotate</title>
  <style>
    .card {
      position: relative;
      width: 180px;
      padding: 20px;
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      font-family: sans-serif;
    }
    .sticker {
      position: absolute;
      top: -8px;
      right: -8px;
      background: #f59e0b;
      color: white;
      padding: 4px 8px;
      font-size: 11px;
      font-weight: bold;
      border-radius: 4px;
      transform: rotate(-10deg);
      transition: transform 0.2s;
    }
    .card:hover .sticker {
      transform: rotate(0deg) scale(1.1);
    }
  </style>
</head>
<body>
  <div class="card">
    <span class="sticker">HOT</span>
    <h4>Mahsulot</h4>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Qiya stiker karta ustida qiziqarli ko'rinadi va hoverda to'g'rilanib kattalashadi.

## Ishlash natijasi:
```text
Kartaning burchagida qiya sariq 'HOT' stikeri ko'rinadi.
```

---

# 786-Topshiriq: Transform translateX bilan xabarlar darchasini yopish (Swipe to Dismiss)
## Topshiriq sharti:
Element ustiga kelganda o'ngga qarab 100% surilib yo'qolish effektini bering.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Swipe Dismiss</title>
  <style>
    .dismiss-box {
      width: 220px;
      padding: 12px;
      background: #fee2e2;
      border: 1px solid #fca5a5;
      color: #b91c1c;
      border-radius: 6px;
      font-family: sans-serif;
      transition: transform 0.4s ease, opacity 0.4s ease;
      cursor: pointer;
    }
    .dismiss-box:hover {
      transform: translateX(120%);
      opacity: 0;
    }
  </style>
</head>
<body>
  <div class="dismiss-box">Meni o'ngga suring &rarr;</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`translateX(120%)` va `opacity: 0` xabarning o'ngga uchib ketishini ko'rsatadi.

## Ishlash natijasi:
```text
Qizil xabar qutisi ustiga kelganda o'ng tomonga uchib ko'rinmay ketadi.
```

---

# 787-Topshiriq: Transform: perspective() bevosita xususiyat ichida
## Topshiriq sharti:
Ota elementga emas, bevosita transform ichida perspective(400px) berish usuli.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Inline Perspective</title>
  <style>
    .inline-3d {
      width: 150px;
      padding: 16px;
      background: #0d9488;
      color: white;
      border-radius: 6px;
      font-family: sans-serif;
      transform: perspective(400px) rotateY(25deg);
    }
  </style>
</head>
<body>
  <div class="inline-3d">perspective(400px)</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`transform: perspective(400px) rotateY(25deg)` alohida ota konteynerga `perspective` bermasdan ham bitta elementda 3D chuqurlik ochadi.

## Ishlash natijasi:
```text
Firuza quti 3D burchakda turadi.
```

---

# 788-Topshiriq: Hover paytida ikonkaning tebranishi (Wiggle Micro-Interaction)
## Topshiriq sharti:
Qo'ng'iroqcha ikonkasi kursor kelganda -15deg va 15deg orasida tebransin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Bell Wiggle</title>
  <style>
    .bell-icon {
      font-size: 32px;
      display: inline-block;
      cursor: pointer;
      transition: transform 0.15s ease-in-out;
    }
    .bell-icon:hover {
      transform: rotate(15deg);
    }
  </style>
</head>
<body>
  <span class="bell-icon">&#128276;</span>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: inline-block` berilgan ikonka transform rotate xususiyatiga to'liq bo'ysunadi.

## Ishlash natijasi:
```text
Qo'ng'iroqcha ustiga kelganda biroz o'ngga qiya buriladi.
```

---

# 789-Topshiriq: Transform-origin yordamida soat mili aylanishi
## Topshiriq sharti:
Chiziqcha pastki uchidan (bottom center) 90 gradusga aylansin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Clock Hand Rotate</title>
  <style>
    .clock-face {
      width: 80px;
      height: 80px;
      border: 3px solid #0f172a;
      border-radius: 50%;
      position: relative;
    }
    .hand {
      position: absolute;
      top: 10px;
      left: 38px;
      width: 4px;
      height: 30px;
      background: #ef4444;
      transform-origin: bottom center;
      transition: transform 0.5s ease;
    }
    .clock-face:hover .hand {
      transform: rotate(90deg);
    }
  </style>
</head>
<body>
  <div class="clock-face">
    <div class="hand"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`transform-origin: bottom center` qizil milning pastki nuqtasini aylana markaziga mahkamlaydi.

## Ishlash natijasi:
```text
Doira ichidagi qizil mil soat 12 dan soat 3 holatiga 90 gradus buriladi.
```

---

# 790-Topshiriq: Transform scaleX bilan ochiluvchi qidiruv maydoni
## Topshiriq sharti:
Ikonka bosilganda yoki hoverda qidiruv qatori eni 0 dan 100% ga ochilsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Expandable Search</title>
  <style>
    .search-box {
      display: flex;
      align-items: center;
      width: fit-content;
      font-family: sans-serif;
    }
    .s-input {
      width: 0;
      opacity: 0;
      padding: 6px;
      border: 1px solid #cbd5e1;
      border-radius: 4px;
      transition: width 0.4s ease, opacity 0.3s;
    }
    .search-box:hover .s-input {
      width: 140px;
      opacity: 1;
    }
  </style>
</head>
<body>
  <div class="search-box">
    <span style="font-size: 20px; cursor: pointer; margin-right: 6px;">&#128269;</span>
    <input type="text" class="s-input" placeholder="Izlash...">
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`width: 0` dan `140px` ga transition orqali qidiruv qutisi silliq yoyiladi.

## Ishlash natijasi:
```text
Lupa ikonkasi yonidan oq qidiruv maydoni silliq cho'zilib chiqadi.
```

---

# 791-Topshiriq: Transform translateY bilan matn ustma-ust almashishi (Ticker Roll)
## Topshiriq sharti:
Hoverda birinchi so'z yuqoriga chiqib ketib, o'rniga pastdan yangi so'z chiqsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Text Roll</title>
  <style>
    .roll-wrap {
      height: 24px;
      overflow: hidden;
      font-family: sans-serif;
      font-weight: bold;
      color: #2563eb;
      cursor: pointer;
    }
    .roll-item {
      transition: transform 0.3s;
    }
    .roll-wrap:hover .roll-item {
      transform: translateY(-24px);
    }
  </style>
</head>
<body>
  <div class="roll-wrap">
    <div class="roll-item">Xush kelibsiz!</div>
    <div class="roll-item">Darsni boshlang &rarr;</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`overflow: hidden` va `translateY(-24px)` bir satrni yuqoriga surib, ikkinchisini ko'rsatadi.

## Ishlash natijasi:
```text
Birinchi matn tepaga yo'qolib, o'rniga ikkinchi matn ko'tariladi.
```

---

# 792-Topshiriq: Transform scale va filter blur birgalikda (Glass Hover)
## Topshiriq sharti:
Hover bo'lganda karta kattalashib foni xiralashsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Blur and Scale</title>
  <style>
    .glass-card {
      width: 180px;
      padding: 16px;
      background: rgba(37, 99, 235, 0.85);
      color: white;
      border-radius: 8px;
      font-family: sans-serif;
      transition: transform 0.3s, backdrop-filter 0.3s;
    }
    .glass-card:hover {
      transform: scale(1.06);
    }
  </style>
</head>
<body>
  <div class="glass-card">
    <h4>Shisha Karta</h4>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Transform bilan vizual filtrlarning uyg'unligi zamonaviy interfeyslarda juda chiroyli ko'rinadi.

## Ishlash natijasi:
```text
Ko'k karta kursor borganda kattalashadi.
```

---

# 793-Topshiriq: Transform skewX bilan bayroqsimon lentalar yaratish
## Topshiriq sharti:
Ikkita qarama-qarshi qiyalangan blokdan iborat lenta yasang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Ribbon Skew</title>
  <style>
    .ribbon {
      display: inline-block;
      background: #e11d48;
      color: white;
      padding: 8px 20px;
      font-family: sans-serif;
      font-weight: bold;
      transform: skewX(-20deg);
    }
  </style>
</head>
<body>
  <div class="ribbon">TOP REYTINQ</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Qizil lenta 20 gradus qiyalanib nishon vazifasini o'taydi.

## Ishlash natijasi:
```text
Qizil qiya parallelogramm ichidagi 'TOP REYTINQ' yozuvi.
```

---

# 794-Topshiriq: Transform rotate va scale bilan yuklanish yulduzchasi
## Topshiriq sharti:
Yulduzcha hoverda ham aylanib ham 1.3 barobar kattalashsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Star Spin Scale</title>
  <style>
    .star-icon {
      font-size: 36px;
      color: #f59e0b;
      display: inline-block;
      cursor: pointer;
      transition: transform 0.4s ease;
    }
    .star-icon:hover {
      transform: rotate(144deg) scale(1.3);
    }
  </style>
</head>
<body>
  <span class="star-icon">&#9733;</span>
</body>
</html>
```

## Tushuntirish va Mantiq:
Rotate va scale birgalikda o'yin va reyting interfeyslarida juda jozibador bo'ladi.

## Ishlash natijasi:
```text
Sariq yulduzcha ustiga kelganda aylanib shishadi.
```

---

# 795-Topshiriq: Transform translateY bilan tugma ostidagi soya masofasini o'zgartirish
## Topshiriq sharti:
Tugma ko'tarilganda uning ostidagi soya pastroqqa tushsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Shadow Shift</title>
  <style>
    .shadow-btn {
      padding: 10px 20px;
      background: #10b981;
      color: white;
      border: none;
      border-radius: 6px;
      font-family: sans-serif;
      box-shadow: 0 4px 0 #059669;
      cursor: pointer;
      transition: transform 0.1s, box-shadow 0.1s;
    }
    .shadow-btn:active {
      transform: translateY(4px);
      box-shadow: 0 0 0 #059669;
    }
  </style>
</head>
<body>
  <button class="shadow-btn">Fizik Tugma</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
Tugma 4px pastga tushib soya yo'qolsa, haqiqiy bosiluvchi mexanik tugma effekti olinadi.

## Ishlash natijasi:
```text
Tugma bosilganda pastga botib soyasi yo'qoladi.
```

---

# 796-Topshiriq: Transform scale(0) dan scale(1) ga ochiluvchi Checkbox qushchasi
## Topshiriq sharti:
Checkbox bosilganda yashil tasdiq belgisi 0 dan kattalashib chiqsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Checkmark Pop</title>
  <style>
    .check-box {
      width: 28px;
      height: 28px;
      background: #10b981;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
      font-weight: bold;
      transform: scale(0);
      transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    body:hover .check-box {
      transform: scale(1);
    }
  </style>
</head>
<body>
  <div class="check-box">&#10003;</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Qushcha belgisi rezina kabi kattalashib chiqadi.

## Ishlash natijasi:
```text
Yashil kvadrat ichida oq tasdiq belgisi prujinasimon paydo bo'ladi.
```

---

# 797-Topshiriq: 3D Kubning bitta tomoni aylanishi (Cube Turn)
## Topshiriq sharti:
Karta rotateX(-90deg) bilan pastga qarab yiqilib tushsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Cube Turn</title>
  <style>
    .cube-scene { perspective: 600px; width: fit-content; margin: 30px; }
    .cube-face {
      width: 140px;
      padding: 16px;
      background: #475569;
      color: white;
      border-radius: 6px;
      font-family: sans-serif;
      transform-origin: bottom center;
      transition: transform 0.5s;
    }
    .cube-scene:hover .cube-face {
      transform: rotateX(-90deg);
    }
  </style>
</head>
<body>
  <div class="cube-scene">
    <div class="cube-face">Pastga yiqilish</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`transform-origin: bottom center` va `rotateX(-90deg)` elementni polga tekis yiqitadi.

## Ishlash natijasi:
```text
Kulrang quti pastga qarab yiqilib polga aylanadi.
```

---

# 798-Topshiriq: Transform scaleX bilan to'ldiriluvchi progress indikatori
## Topshiriq sharti:
scaleX(0) dan scaleX(1) ga transform-origin: left bilan to'lib boruvchi progress bar.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Progress ScaleX</title>
  <style>
    .track {
      width: 240px;
      height: 8px;
      background: #e2e8f0;
      border-radius: 4px;
      overflow: hidden;
    }
    .fill {
      width: 100%;
      height: 100%;
      background: #2563eb;
      transform: scaleX(0);
      transform-origin: left;
      transition: transform 0.8s ease;
    }
    body:hover .fill {
      transform: scaleX(0.75);
    }
  </style>
</head>
<body>
  <div class="track">
    <div class="fill"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`scaleX` orqali progress bar animatsiyasi width o'zgarishiga qaraganda 10 barobar silliqroq ishlaydi.

## Ishlash natijasi:
```text
Kulrang yo'lakcha ichida ko'k chiziq 75% gacha silliq to'ladi.
```

---

# 799-Topshiriq: Tugma ichidagi matn va ikonka oralig'ining kengayishi
## Topshiriq sharti:
Hoverda ikonka 4px o'ngga surilib, tugma fon rangi o'zgarsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Icon Shift Button</title>
  <style>
    .btn-shift {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 18px;
      background: #0f172a;
      color: white;
      border: none;
      border-radius: 6px;
      font-family: sans-serif;
      cursor: pointer;
      transition: background-color 0.2s;
    }
    .btn-shift span { transition: transform 0.2s ease; }
    .btn-shift:hover { background-color: #2563eb; }
    .btn-shift:hover span { transform: translateX(4px); }
  </style>
</head>
<body>
  <button class="btn-shift">Davom etish <span>&rarr;</span></button>
</body>
</html>
```

## Tushuntirish va Mantiq:
Matn va o'q birgalikda o'zgaradi va harakat signali beradi.

## Ishlash natijasi:
```text
Qora tugma ko'k rangga o'tib, strelkasi 4px o'ngga siljiydi.
```

---

# 800-Topshiriq: To'liq 3D Interaktiv Mahsulot Showcase Kartasi
## Topshiriq sharti:
3D fazoda hover bo'lganda karta aylanib, soyasi chuqurlashib, rasmi oldinga chiquvchi to'liq vitrina kartasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Ultimate 3D Showcase Card</title>
  <style>
    .card-scene {
      perspective: 800px;
      width: fit-content;
      margin: 30px;
    }
    .show-card {
      width: 220px;
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 12px;
      padding: 20px;
      font-family: sans-serif;
      transform-style: preserve-3d;
      transition: transform 0.4s ease, box-shadow 0.4s ease;
      box-shadow: 0 4px 6px rgba(0,0,0,0.05);
      cursor: pointer;
    }
    .card-scene:hover .show-card {
      transform: rotateX(10deg) rotateY(-10deg) translateY(-8px);
      box-shadow: 0 20px 30px rgba(0,0,0,0.15);
    }
    .inner-badge {
      display: inline-block;
      background: #ef4444;
      color: white;
      font-size: 11px;
      padding: 3px 8px;
      border-radius: 4px;
      transform: translateZ(25px);
    }
  </style>
</head>
<body>
  <div class="card-scene">
    <div class="show-card">
      <span class="inner-badge">YANGI</span>
      <h3 style="margin: 12px 0 6px 0;">Smart Soat Pro</h3>
      <p style="margin: 0; font-size: 13px; color: #64748b;">Yuqori aniqlikdagi 3D interfeys namoyishi.</p>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`rotateX`, `rotateY`, `translateY`, `translateZ` va `box-shadow` barcha transformatsiyalarni bitta yuqori darajadagi 3D mahsulot kartasida birlashtiradi.

## Ishlash natijasi:
```text
Karta kursor kelganda 3D fazoda egilib yuqoriga ko'tariladi, ichidagi qizil nishon esa kartadan tashqariga bo'rtib chiqadi.
```

---

