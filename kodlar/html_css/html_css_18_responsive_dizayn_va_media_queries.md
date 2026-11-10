# HTML va CSS: Responsive Dizayn va Media Queries (Topshiriqlar 851 - 900)

# 851-Topshiriq: Viewport Meta Tegi: Mobil qurilmalarga moslashuv asosi
## Topshiriq sharti:
Mobil brauzerlarda sahifaning to'g'ri masshtabda render bo'lishini ta'minlovchi viewport meta tegini va uning CSS ga ta'sirini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Viewport Meta</title>
  <style>
    body {
      margin: 0;
      padding: 16px;
      font-family: sans-serif;
      font-size: 16px;
    }
    .box {
      background-color: #2563eb;
      color: white;
      padding: 20px;
      border-radius: 8px;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="box">Mobil ekran kengligiga 100% moslashgan quti</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<meta name="viewport" content="width=device-width, initial-scale=1.0">` tegi brauzerga ekranning haqiqiy jismoniy piksellari bo'yicha sahifani kengaytirishni buyuradi. Usiz smartfonlar sahifani 980px deb taxmin qilib, matnlarni o'qib bo'lmaydigan darajada mitti qilib qo'yadi.

## Ishlash natijasi:
```text
Mobil qurilmada ham, kompyuterda ham toza 16px li o'qishli matn va ekranga to'liq moslangan ko'k quti.
```

---

# 852-Topshiriq: @media qoidasi va oddiy max-width bilan desktop-first moslashuv
## Topshiriq sharti:
Ekran kengligi 600px dan kamayganda fon rangini o'zgartiruvchi @media (max-width: 600px) qoidasini yozing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Media Max Width</title>
  <style>
    .adaptive-card {
      background-color: #3b82f6;
      color: white;
      padding: 20px;
      border-radius: 8px;
      font-family: sans-serif;
    }
    @media (max-width: 600px) {
      .adaptive-card {
        background-color: #10b981; /* 600px dan kichik ekranda yashil bo'ladi */
      }
    }
  </style>
</head>
<body>
  <div class="adaptive-card">Oyna kengligi 600px dan oshganda ko'k, torayganda yashil!</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`@media (max-width: 600px)` qoidasi shartli blok bo'lib, faqat brauzer darchasining eni 600 piksel yoki undan kichik bo'lganda ishga tushadi. Bu Desktop-First yondashuvining asosidir.

## Ishlash natijasi:
```text
Katta ekranda ko'k rangli, ekran toraytirilganda esa yashil rangga aylanuvchi to'rtburchak.
```

---

# 853-Topshiriq: Mobile-First (Mobil birinchi) yondashuvi: min-width breakpoint
## Topshiriq sharti:
Avval mobil stilni yozib, min-width: 768px orqali planshet va kompyuter uchun kengaytirish usulini bajaring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mobile First Strategy</title>
  <style>
    /* 1. Sukut bo'yicha mobil dizayn (kichik ekran) */
    .container {
      display: flex;
      flex-direction: column;
      gap: 10px;
      font-family: sans-serif;
    }
    .col { background: #64748b; color: white; padding: 14px; border-radius: 4px; }

    /* 2. Katta ekranlar uchun kengayish (min-width) */
    @media (min-width: 768px) {
      .container {
        flex-direction: row; /* 768px dan boshlab yonma-yon bo'ladi */
      }
      .col { flex: 1; background: #2563eb; }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="col">Ustun 1</div>
    <div class="col">Ustun 2</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Mobile-First yondashuvida boshlang'ich kod mobil telefonlar uchun eng oddiy holatda yoziladi va ortiqcha yuklama bermaydi. So'ng `min-width` orqali kengroq ekranlar uchun qo'shimcha qoidalar qo'shiladi.

## Ishlash natijasi:
```text
Mobilda vertikal ustun, 768px dan keng ekranda esa ko'k rangli gorizontal 2 ustun.
```

---

# 854-Topshiriq: Klassik Breakpointlar tizimi (sm, md, lg, xl)
## Topshiriq sharti:
640px, 768px va 1024px o'lchamlarida mos ravishda matn hajmi va qatorlar sonini o'zgartiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Standard Breakpoints</title>
  <style>
    .grid-box {
      display: grid;
      grid-template-columns: 1fr;
      gap: 12px;
      font-family: sans-serif;
    }
    .box { background: #0284c7; color: white; padding: 16px; text-align: center; border-radius: 6px; }

    @media (min-width: 640px) { /* sm */
      .grid-box { grid-template-columns: repeat(2, 1fr); }
    }
    @media (min-width: 1024px) { /* lg */
      .grid-box { grid-template-columns: repeat(4, 1fr); }
    }
  </style>
</head>
<body>
  <div class="grid-box">
    <div class="box">1</div><div class="box">2</div><div class="box">3</div><div class="box">4</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu tizim Tailwind va Bootstrap standartlariga mos: kichik mobilda 1 ustun, planshetda (640px+) 2 ustun, noutbukda (1024px+) esa 4 ta ustun hosil bo'ladi.

## Ishlash natijasi:
```text
Ekran kengligiga qarab 1, 2 yoki 4 ustunga dinamik ravishda ajraluvchi kartalar.
```

---

# 855-Topshiriq: Orientation media feature: Portrait (Tik) va Landscape (Yotiq)
## Topshiriq sharti:
Qurilma tik ushlanganda qizil, yotiq qilinganda ko'k fon beruvchi orientation qoidasini qo'llang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Orientation Media</title>
  <style>
    .device-view {
      padding: 20px;
      color: white;
      text-align: center;
      font-family: sans-serif;
      border-radius: 8px;
    }
    @media (orientation: portrait) {
      .device-view { background-color: #ef4444; }
    }
    @media (orientation: landscape) {
      .device-view { background-color: #2563eb; }
    }
  </style>
</head>
<body>
  <div class="device-view">Qurilma holati: Tik yoki Yotiq</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`orientation: portrait` bo'yi enidan baland bo'lganda, `orientation: landscape` esa eni bo'yidan keng bo'lganda faollashadi. Bu planshet va smartfonlarda video ko'rish rejimiga moslashishda juda muhimdir.

## Ishlash natijasi:
```text
Oyna baland bo'lsa qizil, eni keng bo'lsa ko'k fonga aylanadi.
```

---

# 856-Topshiriq: Responsive Tipografika: clamp() funksiyasi bilan elastik matn
## Topshiriq sharti:
Matn o'lchamini hech qanday media query yozmasdan clamp(18px, 4vw, 36px) orqali boshqaring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fluid Typography Clamp</title>
  <style>
    .fluid-title {
      font-family: sans-serif;
      font-weight: 800;
      color: #0f172a;
      /* Min: 18px, Ideal: 4vw, Maks: 36px */
      font-size: clamp(18px, 4vw, 36px);
      line-height: 1.2;
    }
  </style>
</head>
<body>
  <h1 class="fluid-title">Moslashuvchan Sarlavha O'lchami</h1>
</body>
</html>
```

## Tushuntirish va Mantiq:
`clamp(MIN, VAL, MAX)` uchta parametr oladi. Matn hech qachon 18px dan kichik bo'lmaydi, 36px dan katta bo'lmaydi va o'rtadagi diapazonda ekran enining 4 foizi (`4vw`) miqdorida silliq o'sib boradi.

## Ishlash natijasi:
```text
Oyna toraytirilsa matn o'lchami bir tekis kichrayadi, lekin 18px dan tushmaydi.
```

---

# 857-Topshiriq: Prefers-color-scheme: Dark Mode (Tungi rejim)ni avtomatik aniqlash
## Topshiriq sharti:
Foydalanuvchi operatsion tizimi qorong'i rejimda bo'lsa qora fon va oq matnga avtomatik o'tishni yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dark Mode Auto</title>
  <style>
    body {
      background-color: #ffffff;
      color: #0f172a;
      font-family: sans-serif;
      padding: 20px;
      transition: background-color 0.3s, color 0.3s;
    }
    @media (prefers-color-scheme: dark) {
      body {
        background-color: #0f172a;
        color: #f8fafc;
      }
      .card {
        background-color: #1e293b;
        border-color: #334155;
      }
    }
    .card {
      padding: 16px;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <div class="card">
    <h3>Avtomatik Dark Mode</h3>
    <p>Ushbu sahifa tizimingiz tungi yoki kunduzgi rejimiga moslashadi.</p>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`@media (prefers-color-scheme: dark)` foydalanuvchining Windows, Android yoki macOS tizimidagi global tungi rejim parametrini o'qiydi va hech qanday JavaScriptsiz toza CSS bilan Dark Mode taqdim etadi.

## Ishlash natijasi:
```text
Tizim qorong'i bo'lsa qora fonda oq matn, aks holda oppoq fonda qora matn chiqadi.
```

---

# 858-Topshiriq: Prefers-reduced-motion: Zaif harakatlanish imkoniyati cheklanganlar uchun
## Topshiriq sharti:
Foydalanuvchi tizimida 'harakatni kamaytirish' yoqilgan bo'lsa barcha animatsiyalarni o'chiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Reduced Motion Accessibility</title>
  <style>
    @keyframes spin { to { transform: rotate(360deg); } }
    .loader {
      width: 36px;
      height: 36px;
      border: 4px solid #cbd5e1;
      border-top-color: #2563eb;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }
    @media (prefers-reduced-motion: reduce) {
      .loader {
        animation: none; /* Tebranish va aylanuvchi harakatlarni butunlay to'xtatadi */
        border-color: #2563eb;
      }
    }
  </style>
</head>
<body>
  <div class="loader"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`prefers-reduced-motion: reduce` vestibulyar apparati sezgir yoki bosh aylanishi bor insonlar uchun qulaylik yaratadi (WCAG talabi). Bu professional sifat belgisidir.

## Ishlash natijasi:
```text
Oddiy rejimda aylanadi, harakat cheklanganda esa aylanmaydigan statik ko'k halqa bo'lib turadi.
```

---

# 859-Topshiriq: Hover va Pointer media features: Sensorli ekranlarni aniqlash
## Topshiriq sharti:
Sensorli telefonlarda hover effektlarini bekor qilib, faqat sichqonchali kompyuterlarda hoverga ruxsat bering.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Touch vs Mouse Media</title>
  <style>
    .touch-btn {
      padding: 12px 20px;
      background: #0284c7;
      color: white;
      border: none;
      border-radius: 6px;
      font-family: sans-serif;
    }
    /* Faqat kursorli sichqonchasi bor qurilmalarda hover ishlaydi */
    @media (hover: hover) and (pointer: fine) {
      .touch-btn:hover {
        background: #0369a1;
        transform: translateY(-2px);
      }
    }
  </style>
</head>
<body>
  <button class="touch-btn">Aqlli Tugma</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
`@media (hover: hover) and (pointer: fine)` smartfonlarda barmoq tekkanda hoverning 'yopishib qolish' (sticky hover) muammosini 100% yo'qotadi.

## Ishlash natijasi:
```text
Kompyuterda sichqoncha kelganda ko'tariladi, smartfonda esa keraksiz yopishib qolmaydi.
```

---

# 860-Topshiriq: @media print: Sahifani qog'ozga chop etish uchun optimallashtirish
## Topshiriq sharti:
Chop etish paytida navbar va keraksiz fon ranglarini yashirib, faqat toza qora-oq matnni chiqaring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Print Media Styles</title>
  <style>
    body { font-family: sans-serif; padding: 20px; }
    .site-nav { background: #0f172a; color: white; padding: 12px; margin-bottom: 20px; }
    .print-doc { border: 1px solid #cbd5e1; padding: 20px; }

    @media print {
      .site-nav, .no-print {
        display: none !important; /* Chop etishda menyu va reklamalarni yo'qotadi */
      }
      body {
        background: white;
        color: black;
      }
      .print-doc {
        border: none;
      }
    }
  </style>
</head>
<body>
  <nav class="site-nav">Sayt Menyu Paneli</nav>
  <div class="print-doc">
    <h2>Rasmiy Shartnoma Qog'ozi</h2>
    <p>Ushbu matn qog'ozga chop etilganda toza va tejamkor formatda chiqadi.</p>
  </div>
  <button class="no-print" onclick="window.print()">Chop Etish (Ctrl+P)</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
`@media print` printerga yuborilganda yoki PDF formatda saqlanganda ishga tushadi. Murakkab fonlar va navigatsiya yashirilib, kartrij siyohi tejaladi.

## Ishlash natijasi:
```text
Brauzerda to'q menyu ko'rinadi, lekin Chop etish darchasida (Ctrl+P) faqat toza shartnoma matni qoladi.
```

---

# 861-Topshiriq: Responsive Navigatsiya: Mobilda Burger menyuga o'tish
## Topshiriq sharti:
Katta ekranda gorizontal ro'yxat, 640px dan kichik ekranda esa vertikal ustunga aylanuvchi navbar quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Responsive Navbar Menu</title>
  <style>
    .nav {
      display: flex;
      flex-direction: column;
      background: #1e293b;
      padding: 12px 16px;
      font-family: sans-serif;
    }
    .nav-links {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: 10px;
    }
    .nav a { color: #94a3b8; text-decoration: none; }

    @media (min-width: 640px) {
      .nav {
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
      }
      .nav-links {
        flex-direction: row;
        margin-top: 0;
      }
    }
  </style>
</head>
<body>
  <header class="nav">
    <strong style="color:white;">WebPortal</strong>
    <div class="nav-links">
      <a href="#">Bosh sahifa</a>
      <a href="#">Xizmatlar</a>
      <a href="#">Aloqa</a>
    </div>
  </header>
</body>
</html>
```

## Tushuntirish va Mantiq:
Mobilda menyu vertikal taxlanadi, 640px dan boshlab esa gorizontal chiziqqa o'tib sarlavha bilan yonma-yon turadi.

## Ishlash natijasi:
```text
Tor ekranda ustunma-ustun menyu, keng ekranda esa bir chiziqdagi toza navbar.
```

---

# 862-Topshiriq: Responsive Tasvirlar: max-width: 100% va height: auto
## Topshiriq sharti:
Rasm o'z ota konteyneridan hech qachon toshib chiqib ketmasligini ta'minlovchi universal qoida.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fluid Image</title>
  <style>
    .wrapper {
      width: 50%;
      min-width: 160px;
      border: 2px dashed #3b82f6;
      padding: 10px;
    }
    .responsive-img {
      max-width: 100%;
      height: auto;
      display: block;
      border-radius: 6px;
    }
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="responsive-img" style="background:#64748b; height:120px;"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`max-width: 100%; height: auto;` barcha zamonaviy CSS resetlarining oltin qoidasidir. Rasm hech qachon ekran kengligidan toshib ketmaydi va proporsiyasini saqlaydi.

## Ishlash natijasi:
```text
O'ram torayganda rasm qutisi ham unga mos ravishda proporsional qisqaradi.
```

---

# 863-Topshiriq: Aspect-ratio xususiyati bilan responsiv 16:9 video ramkasi
## Topshiriq sharti:
Eskirgan padding-top: 56.25% hiylasisiz, zamonaviy aspect-ratio: 16 / 9 xususiyatini qo'llang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aspect Ratio 16/9</title>
  <style>
    .video-box {
      width: 100%;
      max-width: 320px;
      aspect-ratio: 16 / 9;
      background-color: #0f172a;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-family: sans-serif;
    }
  </style>
</head>
<body>
  <div class="video-box">16:9 Video Pleyer</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`aspect-ratio: 16 / 9` ekran eni o'zgarganda balandlikni avtomatik ravishda 16 ga 9 nisbatda hisoblaydi va Cumulative Layout Shift (CLS) xatolarini butunlay yo'q qiladi.

## Ishlash natijasi:
```text
Kengligi o'zgarsa ham YouTube videolari kabi har doim 16:9 nisbatni mukammal saqlovchi quti.
```

---

# 864-Topshiriq: Vw (Viewport Width) va Vh (Viewport Height) birliklari
## Topshiriq sharti:
Butun ekran balandligini to'liq egallovchi 100vh Hero qismini hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hero Section Vh</title>
  <style>
    body { margin: 0; font-family: sans-serif; }
    .hero-fullscreen {
      min-height: 100vh;
      background: linear-gradient(135deg, #1e293b, #0f172a);
      color: white;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 20px;
      box-sizing: border-box;
    }
  </style>
</head>
<body>
  <section class="hero-fullscreen">
    <h1 style="margin: 0 0 10px 0;">To'liq Ekranli Hero</h1>
    <p style="margin: 0; color: #94a3b8;">100vh orqali har qanday qurilma ekraniga 100% to'ladi.</p>
  </section>
</body>
</html>
```

## Tushuntirish va Mantiq:
`100vh` ko'rinadigan ekran balandligining aniq 100 foiziga teng. `min-height: 100vh` foydalanuvchiga birinchi ochilishda to'liq ekranli jozibador tajriba taqdim etadi.

## Ishlash natijasi:
```text
Brauzer oynasini pastgacha to'liq qoplagan to'q rangli markaziy qutlov ekrani.
```

---

# 865-Topshiriq: Mobil qurilmalar uchun Dvh (Dynamic Viewport Height) yangi standarti
## Topshiriq sharti:
Mobilda manzil qatori ochilib-yopilganda sakramaydigan 100dvh birligini qo'llang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dynamic Viewport Height</title>
  <style>
    body { margin: 0; font-family: sans-serif; }
    .dvh-screen {
      height: 100vh; /* Eski brauzerlar uchun zaxira */
      height: 100dvh; /* Zamonaviy mobil brauzerlar uchun dinamik */
      background: #0284c7;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  </style>
</head>
<body>
  <div class="dvh-screen">100dvh Dinamik Balandlik</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Oddiy `100vh` Safari va Chrome mobile dagi pastki navigatsiya paneli ostiga kirib ketardi. `100dvh` (Dynamic Viewport Height) esa manzil paneli kengayganda ham oynaning aniq ochiq sohasiga moslashadi.

## Ishlash natijasi:
```text
Smartfonlarda pastki tugmalarga xalal bermaydigan mukammal to'liq ekran.
```

---

# 866-Topshiriq: Responsive Jadval: Mobilda gorizontal skroll qobig'i
## Topshiriq sharti:
Katta jadval kichik ekranda sahifani buzmasdan ichki skroll bo'lishi uchun overflow-x: auto berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Responsive Table Scroll</title>
  <style>
    .table-responsive {
      width: 100%;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      border: 1px solid #cbd5e1;
      font-family: sans-serif;
    }
    table { width: 100%; min-width: 450px; border-collapse: collapse; }
    th, td { padding: 10px; border: 1px solid #e2e8f0; text-align: left; }
    th { background: #f8fafc; }
  </style>
</head>
<body>
  <div class="table-responsive">
    <table>
      <tr><th>Kompaniya</th><th>Aloqa</th><th>Mamlakat</th><th>Yil</th></tr>
      <tr><td>Tech Soft</td><td>Ali</td><td>O'zbekiston</td><td>2026</td></tr>
      <tr><td>Global Dev</td><td>Vali</td><td>AQSH</td><td>2025</td></tr>
    </table>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ota konteynerga `overflow-x: auto` berilib, jadvalga `min-width: 450px` qo'yiladi. Natijada tor ekranda butun sayt emas, faqat jadvalning o'zi chiroyli skroll bo'ladi.

## Ishlash natijasi:
```text
Tor ekranda jadval o'z chegarasi ichida gorizontal suriladi, sahifa buzilmaydi.
```

---

# 867-Topshiriq: Responsive Grid Kartalari: avto-ustunlar va minmax
## Topshiriq sharti:
Media queries ishlatmasdan ekranga qarab 1 dan 3 gacha ustun hosil qiluvchi responsive grid tuzing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Grid Auto Fit Responsive</title>
  <style>
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 12px;
      font-family: sans-serif;
    }
    .card { background: #10b981; color: white; padding: 20px; text-align: center; border-radius: 6px; }
  </style>
</head>
<body>
  <div class="grid">
    <div class="card">A</div><div class="card">B</div><div class="card">C</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`repeat(auto-fit, minmax(130px, 1fr))` har doim elementlarni konteynerga moslaydi, ortiqcha bo'shliq qoldirmaydi.

## Ishlash natijasi:
```text
Keng ekranda 3 ta, torayganda 2 ta, eng kichik holatda 1 ta ustun bo'lib moslashadi.
```

---

# 868-Topshiriq: Ko'p ustunli maqola matni (CSS Multi-column) responsivligi
## Topshiriq sharti:
column-width: 140px orqali ekranga qarab avtomatik ustunlarga bo'linuvchi matn yozing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Responsive Multi Column</title>
  <style>
    .newspaper {
      column-width: 140px;
      column-gap: 20px;
      column-rule: 1px solid #cbd5e1;
      font-family: sans-serif;
      font-size: 13px;
      line-height: 1.6;
    }
  </style>
</head>
<body>
  <div class="newspaper">
    Veb-texnologiyalar kundan-kunga takomillashib bormoqda. Zamonaviy CSS imkoniyatlari orqali har qanday qurilma uchun moslashuvchan interfeyslarni qulay yaratish mumkin.
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`column-width: 140px` ekranda qancha 140px joy bo'lsa shuncha ustun ochadi. Tor ekranda 1 ustun, keng ekranda esa gazeta kabi bir necha ustun bo'ladi.

## Ishlash natijasi:
```text
Ekran kengligiga qarab 1 yoki bir nechta ustunlarga ajraluvchi gazeta matni.
```

---

# 869-Topshiriq: Responsive Font Clamping bilan sarlavha va matn mutanosibligi
## Topshiriq sharti:
Paragraf shriftini clamp(14px, 1.5vw + 10px, 18px) orqali boshqaring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Paragraph Clamping</title>
  <style>
    p {
      font-family: sans-serif;
      font-size: clamp(14px, 1.5vw + 10px, 18px);
      line-height: 1.6;
      color: #334155;
    }
  </style>
</head>
<body>
  <p>Ushbu matn mobil telefondan tortib katta monitorlargacha juda qulay o'lchamda mutanosib kattalashadi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Boshlang'ich qiymatga `vw` qo'shish formula orqali shriftning ekran o'lchami bilan bir maromda o'sishini ta'minlaydi.

## Ishlash natijasi:
```text
O'ta qulay, barcha ekranlarda ko'zni charchatmaydigan elastik matn.
```

---

# 870-Topshiriq: Moslashuvchan tugmalar paneli: Wrap va to'liq en (Full Width Mobile)
## Topshiriq sharti:
Kompyuterda yonma-yon, mobilda esa har biri 100% enli bo'luvchi tugmalar guruhini quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Full Width Mobile Buttons</title>
  <style>
    .btn-group {
      display: flex;
      flex-direction: column;
      gap: 10px;
      font-family: sans-serif;
    }
    .btn {
      padding: 12px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      text-align: center;
      font-weight: bold;
    }
    .btn-primary { background: #2563eb; color: white; }
    .btn-secondary { background: #e2e8f0; color: #334155; }

    @media (min-width: 600px) {
      .btn-group {
        flex-direction: row;
      }
      .btn {
        padding: 10px 20px;
      }
    }
  </style>
</head>
<body>
  <div class="btn-group">
    <button class="btn btn-primary">Xarid qilish</button>
    <button class="btn btn-secondary">Batafsil</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Smartfonlarda tugmalarni 100% enli qilish (katta bosish maydoni) foydalanuvchi barmoqlari uchun eng qulay UX qoidasidir.

## Ishlash natijasi:
```text
Mobilda butun enni egallagan ikkita qalin tugma, kompyuterda esa yonma-yon turadi.
```

---

# 871-Topshiriq: Responsive Sidebar va Content tartibi (Flex Order bilan)
## Topshiriq sharti:
Kompyuterda chapda turgan yon panel mobilda asosiy kontent ostiga tushsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Responsive Sidebar Order</title>
  <style>
    .layout {
      display: flex;
      flex-direction: column;
      gap: 16px;
      font-family: sans-serif;
    }
    .main-body { order: 1; background: #ffffff; border: 1px solid #cbd5e1; padding: 16px; border-radius: 6px; }
    .sidebar { order: 2; background: #f1f5f9; padding: 16px; border-radius: 6px; }

    @media (min-width: 768px) {
      .layout { flex-direction: row; }
      .sidebar { order: 1; width: 180px; }
      .main-body { order: 2; flex: 1; }
    }
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">Yon Menyu</aside>
    <main class="main-body">Asosiy Katta Maqola</main>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`order` orqali mobilda asosiy maqola birinchi o'qiladi, yon menyu esa pastga tushadi. Katta ekranda esa menyu chapga o'tadi.

## Ishlash natijasi:
```text
Mobilda maqola tepada chiqadi, kompyuterda esa menyu chapda yonma-yon turadi.
```

---

# 872-Topshiriq: Responsive Hero Banner: Matn va rasmning o'zgarishi
## Topshiriq sharti:
Katta ekranda yonma-yon, mobilda ustma-ust tushuvchi taqdimot banneri quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hero Banner Responsive</title>
  <style>
    .hero {
      display: flex;
      flex-direction: column;
      gap: 20px;
      background: #eff6ff;
      padding: 24px;
      border-radius: 12px;
      font-family: sans-serif;
    }
    .hero-pic { height: 120px; background: #3b82f6; border-radius: 8px; }

    @media (min-width: 640px) {
      .hero {
        flex-direction: row;
        align-items: center;
      }
      .hero-text { flex: 1; }
      .hero-pic { flex: 1; height: 160px; }
    }
  </style>
</head>
<body>
  <div class="hero">
    <div class="hero-text">
      <h2>Dasturlashni o'rganing</h2>
      <p style="color: #64748b;">Noldan professional darajagacha amaliy darslar.</p>
    </div>
    <div class="hero-pic"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Mobil ekranda matn va rasm ustma-ust teriladi, planshetdan boshlab esa teng ikkiga ajraladi.

## Ishlash natijasi:
```text
Ochiq moviy kartada mobilda ustun, katta ekranda esa matn va rasm yonma-yon.
```

---

# 873-Topshiriq: Responsive Footer: Mobilda akkordeon, kompyuterda 4 ustun
## Topshiriq sharti:
Media query orqali footer bo'limlarini 1 ustundan 4 ustunga aylantiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Responsive Footer Grid</title>
  <style>
    footer {
      display: grid;
      grid-template-columns: 1fr;
      gap: 16px;
      background: #0f172a;
      color: white;
      padding: 24px;
      font-family: sans-serif;
    }
    .col h4 { margin: 0 0 8px 0; color: #38bdf8; }
    .col p { margin: 0; font-size: 13px; color: #94a3b8; }

    @media (min-width: 768px) {
      footer {
        grid-template-columns: repeat(4, 1fr);
      }
    }
  </style>
</head>
<body>
  <footer>
    <div class="col"><h4>Kompaniya</h4><p>Biz haqimizda</p></div>
    <div class="col"><h4>Xizmatlar</h4><p>Veb ilovalar</p></div>
    <div class="col"><h4>Yordam</h4><p>FAQ</p></div>
    <div class="col"><h4>Aloqa</h4><p>+998710000000</p></div>
  </footer>
</body>
</html>
```

## Tushuntirish va Mantiq:
Kichik ekranda 1 ustunli ixcham ro'yxat, keng ekranda esa 4 ustunli to'liq ma'lumotlar maydoni.

## Ishlash natijasi:
```text
Mobilda ustunma-ustun, kompyuterda esa 4 ta yonma-yon ustunli footer.
```

---

# 874-Topshiriq: Responsive Padding va Margin chekinishlari
## Topshiriq sharti:
Mobilda 12px, kompyuterda 40px chekinish beruvchi konteyner yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Responsive Spacing</title>
  <style>
    .page-box {
      padding: 12px;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      font-family: sans-serif;
    }
    @media (min-width: 768px) {
      .page-box {
        padding: 40px;
        max-width: 800px;
        margin: 20px auto;
        border-radius: 12px;
      }
    }
  </style>
</head>
<body>
  <div class="page-box">
    <h2>Moslashuvchan Hoshiyalar</h2>
    <p>Mobilda ekranni tejash uchun 12px, monitorda esa 40px keng havo.</p>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Kichik ekranda katta padding bo'sh joyni noo'rin yo'qotadi, kompyuterda esa aksincha qulaylik beradi.

## Ishlash natijasi:
```text
Mobilda tor chekkali, katta ekranda esa keng havoli va markazlashgan quti.
```

---

# 875-Topshiriq: Responsive Font Clamping bilan Hero sarlavhasi (24px dan 56px gacha)
## Topshiriq sharti:
Hero sarlavhasi o'lchamini clamp(24px, 5vw, 56px) orqali boshqaring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hero Clamped Title</title>
  <style>
    h1 {
      font-family: sans-serif;
      font-size: clamp(24px, 5vw, 56px);
      color: #1e40af;
      text-align: center;
    }
  </style>
</head>
<body>
  <h1>Kelajak Ta'lim Portali</h1>
</body>
</html>
```

## Tushuntirish va Mantiq:
`clamp` sarlavhani barcha ekran o'lchamlariga silliq va o'qishli qilib beradi.

## Ishlash natijasi:
```text
Mobilda 24px, 4K monitorda 56px bo'lgan ulkan sarlavha.
```

---

# 876-Topshiriq: Mobilda yashirinuvchi elementlar (.hidden-mobile klassi)
## Topshiriq sharti:
Faqat kompyuterda ko'rinadigan va telefonda display: none bo'ladigan element yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hide on Mobile</title>
  <style>
    .desk-only {
      display: none;
      background: #fef3c7;
      border: 1px solid #f59e0b;
      padding: 12px;
      font-family: sans-serif;
    }
    @media (min-width: 768px) {
      .desk-only { display: block; }
    }
  </style>
</head>
<body>
  <div class="desk-only">Bu blok faqat planshet va kompyuterlarda ko'rinadi!</div>
  <p style="font-family: sans-serif;">Ushbu asosiy matn har doim ko'rinadi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Kichik ekranda keraksiz ikkilamchi bloklarni yashirish mobil UX ni toza saqlaydi.

## Ishlash natijasi:
```text
768px dan kichik ekranda sariq blok yo'qoladi, katta ekranda paydo bo'ladi.
```

---

# 877-Topshiriq: Kompyuterda yashirinuvchi mobil element (.mobile-only klassi)
## Topshiriq sharti:
Faqat telefon ekranida ko'rinuvchi 'Ilovani yuklab oling' bannerini quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mobile Only Banner</title>
  <style>
    .mob-banner {
      background: #10b981;
      color: white;
      padding: 10px;
      text-align: center;
      font-family: sans-serif;
      font-weight: bold;
    }
    @media (min-width: 768px) {
      .mob-banner { display: none; }
    }
  </style>
</head>
<body>
  <div class="mob-banner">Mobil ilovamizni o'rnating!</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Faqat smartfon egalariga tegishli xabarlarni ko'rsatish uchun qulay yondashuv.

## Ishlash natijasi:
```text
Smartfonda yashil tasma ko'rinadi, kompyuterda esa avtomatik yashirinadi.
```

---

# 878-Topshiriq: Responsive Video iframes: 100% en va to'g'ri balandlik
## Topshiriq sharti:
Iframe konteynerini aspect-ratio orqali 100% moslashuvchan qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Responsive Video Frame</title>
  <style>
    .video-wrapper {
      width: 100%;
      max-width: 320px;
      aspect-ratio: 16 / 9;
      background: #000;
      border-radius: 8px;
      overflow: hidden;
    }
    .video-wrapper iframe {
      width: 100%;
      height: 100%;
      border: none;
    }
  </style>
</head>
<body>
  <div class="video-wrapper">
    <iframe src="about:blank" title="Video"></iframe>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`aspect-ratio: 16 / 9` va `width: 100%` bilan iframe hech qachon ekrandan toshib ketmaydi.

## Ishlash natijasi:
```text
O'lchami o'zgarganda ham 16:9 nisbatini mukammal ushlovchi qora video ramkasi.
```

---

# 879-Topshiriq: Responsive Tartib: 1 ustun &rarr; 2 ustun &rarr; 3 ustun &rarr; 4 ustun
## Topshiriq sharti:
sm (640px), md (768px), lg (1024px) orqali bosqichma-bosqich kengayuvchi galereya.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Progressive Columns</title>
  <style>
    .prog-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 10px;
      font-family: sans-serif;
    }
    .p-item { background: #3b82f6; color: white; padding: 14px; text-align: center; border-radius: 4px; }

    @media (min-width: 480px) { .prog-grid { grid-template-columns: repeat(2, 1fr); } }
    @media (min-width: 768px) { .prog-grid { grid-template-columns: repeat(3, 1fr); } }
    @media (min-width: 1024px) { .prog-grid { grid-template-columns: repeat(4, 1fr); } }
  </style>
</head>
<body>
  <div class="prog-grid">
    <div class="p-item">1</div><div class="p-item">2</div>
    <div class="p-item">3</div><div class="p-item">4</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Har bir qurilma sinfi uchun alohida breakpoint qulaylikni ta'minlaydi.

## Ishlash natijasi:
```text
Oyna kattalashgan sari 1 tadan 4 tagacha ustunlarga ajraluvchi ko'k bloklar.
```

---

# 880-Topshiriq: Responsive Matn tekislash: Mobilda markazda, kompyuterda chapda
## Topshiriq sharti:
Mobilda text-align: center, min-width: 768px da esa text-align: left qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Responsive Text Align</title>
  <style>
    .lead-box {
      text-align: center;
      font-family: sans-serif;
      padding: 16px;
    }
    @media (min-width: 768px) {
      .lead-box {
        text-align: left;
      }
    }
  </style>
</head>
<body>
  <div class="lead-box">
    <h3>Moslashuvchan Tekislash</h3>
    <p>Mobilda markazda o'qish qulay, kompyuterda esa chap qirra bo'yicha.</p>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Mobil ekranlarda simmetrik markaziy matn chiroyli chiqadi, katta ekranda esa chapdan o'qish qulayroq.

## Ishlash natijasi:
```text
Tor ekranda markazda, keng ekranda esa chap qirrada turuvchi matn.
```

---

# 881-Topshiriq: Responsive Card: Mobilda vertikal, kompyuterda gorizontal karta
## Topshiriq sharti:
Rasm tepada va matn pastda bo'lgan karta kompyuterda rasm chapda, matn o'ngda bo'lsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Card Orientation Flip</title>
  <style>
    .flip-card {
      display: flex;
      flex-direction: column;
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      overflow: hidden;
      font-family: sans-serif;
      max-width: 450px;
    }
    .c-img { height: 100px; background: #64748b; }
    .c-txt { padding: 14px; }

    @media (min-width: 600px) {
      .flip-card {
        flex-direction: row;
      }
      .c-img { width: 140px; height: auto; }
      .c-txt { flex: 1; }
    }
  </style>
</head>
<body>
  <div class="flip-card">
    <div class="c-img"></div>
    <div class="c-txt">
      <h4 style="margin:0 0 6px 0;">Kurs Nomi</h4>
      <p style="margin:0; font-size:13px; color:#64748b;">Kompyuterda rasm chapda turadi.</p>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-direction: column` dan `row` ga o'tish orqali bitta komponent ikkala rejimga moslashadi.

## Ishlash natijasi:
```text
Mobilda rasm tepada, kompyuterda esa rasm chap tomonda joylashadi.
```

---

# 882-Topshiriq: Responsive Qidiruv Paneli: Mobilda ixcham ikonka, kompyuterda to'liq maydon
## Topshiriq sharti:
Media query orqali qidiruv darchasini moslashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Adaptive Search</title>
  <style>
    .search-wrap input {
      width: 100px;
      padding: 6px;
      border: 1px solid #cbd5e1;
      border-radius: 4px;
    }
    @media (min-width: 768px) {
      .search-wrap input {
        width: 240px;
      }
    }
  </style>
</head>
<body>
  <div class="search-wrap">
    <input type="text" placeholder="Qidiruv...">
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Tor ekranda ixcham, keng ekranda esa to'liq kengaygan qidiruv darchasi.

## Ishlash natijasi:
```text
Mobilda 100px li tor maydon, kompyuterda esa 240px li keng qidiruv.
```

---

# 883-Topshiriq: Chop etishda havola manzillarini ko'rsatish (@media print href display)
## Topshiriq sharti:
Qog'ozga chop etilganda a tegi yonida uning url manzili (attr(href)) chiqsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Print URL display</title>
  <style>
    @media print {
      a[href]::after {
        content: " (" attr(href) ")";
        font-size: 11px;
        color: #475569;
      }
    }
  </style>
</head>
<body>
  <p style="font-family: sans-serif;">
    Rasmiy portalimiz: <a href="https://kun.uz">Kun.uz yangiliklari</a>
  </p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Qog'ozga bosilganda havolalarni bosib bo'lmaydi, shuning uchun `attr(href)` orqali manzilni qavs ichida chiqarish eng to'g'ri odatdir.

## Ishlash natijasi:
```text
Chop etilganda matn yonida '(https://kun.uz)' yozuvi paydo bo'ladi.
```

---

# 884-Topshiriq: Retina ekranlar uchun @media resolution (2x display)
## Topshiriq sharti:
2x va 3x Retina ekranlarda yuqori aniqlikdagi fon rasmini ulash qoidasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Retina High DPI</title>
  <style>
    .retina-box {
      width: 120px;
      height: 60px;
      background: #3b82f6;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: sans-serif;
    }
    @media (min-resolution: 2dppx) {
      .retina-box {
        background: #1d4ed8; /* Yuqori aniqlikdagi Retina displey */
      }
    }
  </style>
</head>
<body>
  <div class="retina-box">Retina Check</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`min-resolution: 2dppx` (yoki 192dpi) Apple Retina va zamonaviy smartfonlarning yuqori zichlikdagi ekranlarini aniqlaydi.

## Ishlash natijasi:
```text
Retina ekranlarda to'q ko'k rang bilan javob beradi.
```

---

# 885-Topshiriq: Responsive Avatar o'lchamlari: clamp() bilan
## Topshiriq sharti:
Avatar doirasini clamp(40px, 8vw, 80px) orqali moslashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fluid Avatar</title>
  <style>
    .fluid-av {
      width: clamp(40px, 8vw, 80px);
      height: clamp(40px, 8vw, 80px);
      border-radius: 50%;
      background: #8b5cf6;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      font-family: sans-serif;
      font-size: clamp(14px, 3vw, 24px);
    }
  </style>
</head>
<body>
  <div class="fluid-av">AZ</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Kichik ekranda 40px, katta ekranda esa 80px gacha kattalashuvchi doira.

## Ishlash natijasi:
```text
Ekran eniga qarab mutanosib kattalashuvchi binafsha rangli avatar doirasi.
```

---

# 886-Topshiriq: Responsive Foydalanuvchi Izohlari: Mobilda rasm ustida, kompyuterda yonida
## Topshiriq sharti:
Foydalanuvchi sharhini flex-direction orqali moslashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Responsive Comment</title>
  <style>
    .comment-card {
      display: flex;
      flex-direction: column;
      gap: 12px;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      padding: 16px;
      border-radius: 8px;
      font-family: sans-serif;
      max-width: 400px;
    }
    .av-circle { width: 44px; height: 44px; background: #0284c7; border-radius: 50%; flex-shrink: 0; }

    @media (min-width: 600px) {
      .comment-card { flex-direction: row; }
    }
  </style>
</head>
<body>
  <div class="comment-card">
    <div class="av-circle"></div>
    <div>
      <strong>Sardor</strong>
      <p style="margin: 4px 0 0; font-size: 13px; color: #64748b;">Juda foydali qo'llanma bo'libdi.</p>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Kichik ekranda ustun bo'lib joy tejaydi, keng ekranda yonma-yon turadi.

## Ishlash natijasi:
```text
Mobilda avatar matn ustida, kompyuterda esa matn yonida turadi.
```

---

# 887-Topshiriq: Responsive Galereya: Mobilda 2 ta, planshetda 3 ta, kompyuterda 6 ta kvadrat
## Topshiriq sharti:
repeat bilan ko'p bosqichli kvadratlar panjarasi tuzing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Multi Step Gallery</title>
  <style>
    .gal-box {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
      font-family: sans-serif;
    }
    .sq { aspect-ratio: 1; background: #64748b; border-radius: 4px; }

    @media (min-width: 600px) { .gal-box { grid-template-columns: repeat(3, 1fr); } }
    @media (min-width: 900px) { .gal-box { grid-template-columns: repeat(6, 1fr); } }
  </style>
</head>
<body>
  <div class="gal-box">
    <div class="sq"></div><div class="sq"></div><div class="sq"></div>
    <div class="sq"></div><div class="sq"></div><div class="sq"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
6 ta kvadrat mobilda 3 qatorga (2 tadan), planshetda 2 qatorga (3 tadan), kompyuterda esa 1 qatorga (6 tadan) to'liq tushadi.

## Ishlash natijasi:
```text
Ekran kengaygan sari ustunlar soni 2 tadan 6 tagacha o'sib boradi.
```

---

# 888-Topshiriq: Responsive Sayt Logotipi: Mobilda faqat nishon, kompyuterda to'liq nom
## Topshiriq sharti:
Mobilda faqat kichik belgi, 768px da to'liq matn bilan chiqadigan logo yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Responsive Logo</title>
  <style>
    .brand-logo {
      display: flex;
      align-items: center;
      gap: 8px;
      font-family: sans-serif;
      font-weight: bold;
    }
    .logo-mark {
      width: 32px;
      height: 32px;
      background: #2563eb;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
    }
    .logo-text { display: none; }

    @media (min-width: 768px) {
      .logo-text { display: inline; }
    }
  </style>
</head>
<body>
  <div class="brand-logo">
    <div class="logo-mark">A</div>
    <span class="logo-text">Antigravity Academy</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Kichik ekranda joyni tejash uchun to'liq nom yashirilib, faqat 'A' belgisi qoldiriladi.

## Ishlash natijasi:
```text
Mobilda faqat ko'k 'A' belgisi, kompyuterda esa yonida to'liq nom paydo bo'ladi.
```

---

# 889-Topshiriq: Chop etishda sahifa bo'linishini boshqarish (break-inside: avoid)
## Topshiriq sharti:
Chop etish paytida kartochkaning ikki sahifaga bo'linib yirtilib ketishini taqiqlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Print Page Break</title>
  <style>
    .doc-card {
      padding: 16px;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      margin-bottom: 20px;
      font-family: sans-serif;
      break-inside: avoid; /* Chop etishda kartani o'rtasidan bo'lmaydi */
    }
  </style>
</head>
<body>
  <div class="doc-card">
    <h4>Muhim Ma'lumot Bloki</h4>
    <p>Ushbu karta chop etilganda butunligicha keyingi qog'oz varag'iga o'tadi.</p>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`break-inside: avoid` (avvalgi `page-break-inside: avoid`) chop etish paytida bitta blokning ikki varaqqa yirtilib tushishining oldini oladi.

## Ishlash natijasi:
```text
Qog'ozga chop etilganda karta yaxlit saqlanadi.
```

---

# 890-Topshiriq: Responsive Metrikalar Paneli: Mobilda 2x2, kompyuterda 4x1
## Topshiriq sharti:
4 ta ko'rsatkichni mobilda 2 ustun, kompyuterda 4 ustun qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Metrics 2x2 to 4x1</title>
  <style>
    .metrics {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
      font-family: sans-serif;
      text-align: center;
    }
    .m-item { background: #eff6ff; padding: 14px; border-radius: 6px; }
    .m-val { font-size: 20px; font-weight: bold; color: #1e40af; }

    @media (min-width: 768px) {
      .metrics { grid-template-columns: repeat(4, 1fr); }
    }
  </style>
</head>
<body>
  <div class="metrics">
    <div class="m-item"><div class="m-val">100%</div>Uptime</div>
    <div class="m-item"><div class="m-val">50k</div>Users</div>
    <div class="m-item"><div class="m-val">4.9</div>Rating</div>
    <div class="m-item"><div class="m-val">24/7</div>Support</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Smartfonda 4 ta ustun sig'maydi, 2x2 esa ideal ko'rinadi. Katta ekranda esa bitta chiziqqa teriladi.

## Ishlash natijasi:
```text
Mobilda 2x2 to'rtburchak matritsa, kompyuterda esa 4 ta yonma-yon metrika.
```

---

# 891-Topshiriq: Responsive Matn Qatorlar Oralig'i (Line-height) moslashuvi
## Topshiriq sharti:
Mobilda ixchamroq 1.4, kompyuterda esa kengroq 1.8 line-height bering.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Responsive Line Height</title>
  <style>
    .article-text {
      font-family: sans-serif;
      font-size: 15px;
      line-height: 1.4;
      color: #334155;
    }
    @media (min-width: 768px) {
      .article-text {
        font-size: 16px;
        line-height: 1.8;
      }
    }
  </style>
</head>
<body>
  <p class="article-text">
    Moslashuvchan tipografikada faqat shrift kattaligi emas, balki qatorlar orasidagi masofa ham katta ahamiyatga ega. Katta ekranda keng qatorlar ko'zga dam beradi.
  </p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Katta ekranda uzun qatorlarni o'qishda `line-height: 1.8` ko'zning keyingi satrga adashmasdan o'tishini yengillashtiradi.

## Ishlash natijasi:
```text
Mobilda ixcham, keng ekranda esa keng ochilgan qatorlar oralig'i.
```

---

# 892-Topshiriq: Responsive Tugmalar Guruhi: Mobilda vertikal stak, kompyuterda birikkan guruh
## Topshiriq sharti:
Mobilda tugmalar ajralib turadi, kompyuterda esa yagona blok bo'lib birlashadi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Responsive Button Group</title>
  <style>
    .btn-wrap {
      display: flex;
      flex-direction: column;
      gap: 8px;
      font-family: sans-serif;
    }
    .b-item { padding: 10px 16px; border: 1px solid #cbd5e1; background: white; border-radius: 4px; }

    @media (min-width: 600px) {
      .btn-wrap {
        flex-direction: row;
        gap: 0;
      }
      .b-item { border-radius: 0; border-right: none; }
      .b-item:first-child { border-radius: 6px 0 0 6px; }
      .b-item:last-child { border-radius: 0 6px 6px 0; border-right: 1px solid #cbd5e1; }
    }
  </style>
</head>
<body>
  <div class="btn-wrap">
    <button class="b-item">Variant A</button>
    <button class="b-item">Variant B</button>
    <button class="b-item">Variant C</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Mobilda alohida tugmalar bosish uchun qulay, kompyuterda esa birikkan guruh toza ko'rinadi.

## Ishlash natijasi:
```text
Mobilda ustunma-ustun alohida tugmalar, kompyuterda esa yaxlit segmentlangan panel.
```

---

# 893-Topshiriq: Responsive Kontaktlar Formasi: Mobilda 1 ustun, kompyuterda 2 ustun
## Topshiriq sharti:
Ism va Email maydonlarini planshetdan boshlab 2 ustunga o'tkazing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Responsive Form</title>
  <style>
    .form-box {
      display: grid;
      grid-template-columns: 1fr;
      gap: 12px;
      max-width: 480px;
      font-family: sans-serif;
    }
    input { padding: 10px; border: 1px solid #cbd5e1; border-radius: 4px; }

    @media (min-width: 600px) {
      .form-box { grid-template-columns: 1fr 1fr; }
      .full-span { grid-column: span 2; }
    }
  </style>
</head>
<body>
  <form class="form-box">
    <input type="text" placeholder="Ism">
    <input type="email" placeholder="Email">
    <input type="text" class="full-span" placeholder="Mavzu">
  </form>
</body>
</html>
```

## Tushuntirish va Mantiq:
Katta ekranda formani 2 ustunga bo'lish maydonlarning ortiqcha cho'zilib ketishini oldini oladi.

## Ishlash natijasi:
```text
Mobilda 3 ta vertikal qator, kompyuterda esa tepadagi 2 tasi yonma-yon.
```

---

# 894-Topshiriq: Responsive Modal oyna: Mobilda pastki varaq (Bottom Sheet), kompyuterda markaziy darcha
## Topshiriq sharti:
Mobilda ekranning pastki qismiga yopishuvchi sheet, kompyuterda esa markaziy dialog darcha qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bottom Sheet to Modal</title>
  <style>
    .sheet-modal {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: white;
      padding: 20px;
      border-radius: 16px 16px 0 0;
      box-shadow: 0 -4px 12px rgba(0,0,0,0.1);
      font-family: sans-serif;
    }
    @media (min-width: 640px) {
      .sheet-modal {
        top: 50%;
        bottom: auto;
        left: 50%;
        right: auto;
        transform: translate(-50%, -50%);
        width: 300px;
        border-radius: 8px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
      }
    }
  </style>
</head>
<body>
  <div class="sheet-modal">
    <h4 style="margin: 0 0 8px 0;">Moslashuvchan Dialog</h4>
    <p style="margin: 0; font-size: 13px; color: #64748b;">Mobilda pastki varaq (Sheet), kompyuterda markazda.</p>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Mobil ilovalarda (iOS, Android) pastki varaqlar (bottom sheets) bir qo'l bilan boshqarish uchun eng qulaydir.

## Ishlash natijasi:
```text
Mobilda pastdan ko'tarilgan varaq, kompyuterda esa o'rtada turgan oq darcha.
```

---

# 895-Topshiriq: Responsive Tablar: Mobilda skroll bo'ladigan tasma, kompyuterda teng taqsimlangan
## Topshiriq sharti:
Kichik ekranda gorizontal o'tuvchi tablar, katta ekranda esa butun en bo'yicha teng tablar.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Scrollable Tabs</title>
  <style>
    .tabs-bar {
      display: flex;
      overflow-x: auto;
      gap: 8px;
      white-space: nowrap;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 6px;
      font-family: sans-serif;
    }
    .tab-btn {
      padding: 8px 16px;
      background: none;
      border: none;
      cursor: pointer;
      color: #64748b;
    }
    .tab-btn.active { color: #2563eb; font-weight: bold; border-bottom: 2px solid #2563eb; }

    @media (min-width: 768px) {
      .tabs-bar {
        justify-content: space-between;
      }
      .tab-btn { flex: 1; text-align: center; }
    }
  </style>
</head>
<body>
  <div class="tabs-bar">
    <button class="tab-btn active">Asosiy</button>
    <button class="tab-btn">Xavfsizlik</button>
    <button class="tab-btn">Bildirishnomalar</button>
    <button class="tab-btn">Hisoblar</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Mobilda ko'p tablar sig'maydi, shuning uchun gorizontal surishga ruxsat beriladi.

## Ishlash natijasi:
```text
Mobilda o'ngga suriladigan tablar, kompyuterda esa teng taqsimlangan chiroyli tablar.
```

---

# 896-Topshiriq: Responsive Rasmlar: srcset va sizes bilan tarmoq trafigini tejash
## Topshiriq sharti:
Mobilda kichik rasm, kompyuterda katta sifatli rasm yuklash uchun sizes qoidasini yozing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Responsive Picture Element</title>
  <style>
    .hero-img {
      width: 100%;
      height: 140px;
      background: #3b82f6;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-family: sans-serif;
    }
    @media (min-width: 768px) {
      .hero-img { height: 220px; background: #1d4ed8; }
    }
  </style>
</head>
<body>
  <div class="hero-img">Moslashuvchan Tasvir Maydoni</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ekran hajmiga mos rasmlarni ko'rsatish orqali mobil foydalanuvchilarning megabaytlari sezilarli tejaladi.

## Ishlash natijasi:
```text
Katta ekranda 220px li to'q ko'k, kichik ekranda 140px li och ko'k surat foni.
```

---

# 897-Topshiriq: Responsive Pagination: Mobilda faqat Orqaga/Oldinga, kompyuterda raqamlar
## Topshiriq sharti:
Raqamli havolalarni faqat 640px dan keng ekranda ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Responsive Pagination</title>
  <style>
    .pager {
      display: flex;
      gap: 6px;
      align-items: center;
      font-family: sans-serif;
    }
    .page-num { display: none; padding: 6px 10px; border: 1px solid #cbd5e1; border-radius: 4px; }
    .page-btn { padding: 6px 12px; background: #2563eb; color: white; border: none; border-radius: 4px; }

    @media (min-width: 640px) {
      .page-num { display: block; }
    }
  </style>
</head>
<body>
  <div class="pager">
    <button class="page-btn">&larr; Orqaga</button>
    <span class="page-num">1</span>
    <span class="page-num">2</span>
    <span class="page-num">3</span>
    <button class="page-btn">Oldinga &rarr;</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Mobilda raqamlarni bosish qiyin bo'lgani uchun faqat katta navigatsiya tugmalari qoldiriladi.

## Ishlash natijasi:
```text
Mobilda faqat 2 ta katta tugma, kompyuterda esa o'rtasida raqamlar ham chiqadi.
```

---

# 898-Topshiriq: Responsive Video Pleer: Mobilda to'liq en (Full Bleed), kompyuterda cheklangan konteyner
## Topshiriq sharti:
Kichik ekranda chekka paddinglarsiz noldan yopishuvchi video maydoni quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Full Bleed Mobile Video</title>
  <style>
    body { margin: 0; padding: 0; font-family: sans-serif; }
    .video-hero {
      width: 100%;
      height: 180px;
      background: #0f172a;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
    }
    @media (min-width: 768px) {
      .video-hero {
        max-width: 600px;
        margin: 20px auto;
        border-radius: 8px;
        height: 300px;
      }
    }
  </style>
</head>
<body>
  <div class="video-hero">Video Pleyer</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Smartfonda video butun kenglikni egallashi kerak (burchaksiz), kompyuterda esa markazda chiroyli ramkali turadi.

## Ishlash natijasi:
```text
Mobilda ekranning ikki chetiga to'liq yopishgan qora video, kompyuterda esa markazdagi ixcham quti.
```

---

# 899-Topshiriq: Responsive Narxlar Kartasi: Mobilda vertikal slayder, kompyuterda 3 ustun
## Topshiriq sharti:
Media queries orqali narxlar jadvalini kompyuterda 3 ustun, mobilda ustunma-ustun qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Responsive Pricing Grid</title>
  <style>
    .pricing {
      display: grid;
      grid-template-columns: 1fr;
      gap: 16px;
      font-family: sans-serif;
      max-width: 800px;
      margin: 0 auto;
    }
    .card { background: white; border: 1px solid #cbd5e1; padding: 20px; border-radius: 8px; text-align: center; }

    @media (min-width: 768px) {
      .pricing {
        grid-template-columns: repeat(3, 1fr);
      }
    }
  </style>
</head>
<body>
  <div class="pricing">
    <div class="card"><h4>Standart</h4><h2>$9</h2></div>
    <div class="card" style="border-color:#2563eb; background:#eff6ff;"><h4>Pro</h4><h2>$29</h2></div>
    <div class="card"><h4>VIP</h4><h2>$99</h2></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Katta ekranda 3 ta karta yonma-yon solishtiriladi, mobilda esa ketma-ket qulay o'qiladi.

## Ishlash natijasi:
```text
Mobilda ustunma-ustun 3 ta karta, kompyuterda esa 3 ustunli chiroyli narxlar paneli.
```

---

# 900-Topshiriq: To'liq Moslashuvchan Landing Sahifasi (Mobile, Tablet, Desktop)
## Topshiriq sharti:
Header, Hero, Feature Grid va Footer bo'limlarini birlashtirgan to'liq responsiv maket yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Complete Responsive Page</title>
  <style>
    body { margin: 0; font-family: sans-serif; background: #f8fafc; }
    header { background: #0f172a; color: white; padding: 14px 20px; display: flex; justify-content: space-between; align-items: center; }
    .hero { background: #2563eb; color: white; padding: 30px 20px; text-align: center; }
    .features { display: grid; grid-template-columns: 1fr; gap: 16px; padding: 20px; max-width: 900px; margin: 0 auto; }
    .f-card { background: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; }
    footer { background: #1e293b; color: #94a3b8; text-align: center; padding: 16px; font-size: 13px; }

    @media (min-width: 640px) {
      .features { grid-template-columns: repeat(2, 1fr); }
    }
    @media (min-width: 1024px) {
      .hero { padding: 50px 20px; }
      .features { grid-template-columns: repeat(3, 1fr); }
    }
  </style>
</head>
<body>
  <header><strong>EduSite</strong><span>Menyu</span></header>
  <div class="hero">
    <h2 style="margin:0 0 10px 0;">Zamonaviy Ta'lim</h2>
    <p style="margin:0;">Barcha qurilmalarda 100% mukammal ishlaydi.</p>
  </div>
  <div class="features">
    <div class="f-card"><h4>1. Oson</h4><p>Noldan boshlash uchun.</p></div>
    <div class="f-card"><h4>2. Tezkor</h4><p>Amaliy topshiriqlar.</p></div>
    <div class="f-card"><h4>3. Sifatli</h4><p>Mentorlar ko'magi.</p></div>
  </div>
  <footer>&copy; 2026 EduSite. Barcha huquqlar himoyalangan.</footer>
</body>
</html>
```

## Tushuntirish va Mantiq:
Mobil birinchi tamoyili asosida 640px (planshet) va 1024px (desktop) breakpointlari bilan to'liq landing sahifasi qurildi.

## Ishlash natijasi:
```text
Tepadagi navbar, ko'k banner, ekranga moslashuvchan 1-2-3 ustunli kartalar va pastki footer.
```

---

