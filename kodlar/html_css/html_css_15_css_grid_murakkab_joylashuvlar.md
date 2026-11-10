# HTML va CSS: CSS Grid Murakkab Joylashuvlar (Topshiriqlar 701 - 750)

# 701-Topshiriq: Grid-column: span 2 bilan elementni ikki ustunga cho'zish
## Topshiriq sharti:
Birinchi elementning 2 ta ustunni egallab, qolgan elementlarni keyingi ustun va satrga surishini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Column Span</title>
  <style>
    .grid-container {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      font-family: sans-serif;
    }
    .box {
      background: #3b82f6;
      color: white;
      padding: 16px;
      text-align: center;
      border-radius: 6px;
    }
    .wide-box {
      grid-column: span 2; /* 2 ta ustunni qamrab oladi */
      background: #1d4ed8;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="grid-container">
    <div class="box wide-box">Keng Element (span 2)</div>
    <div class="box">Katak 2</div>
    <div class="box">Katak 3</div>
    <div class="box">Katak 4</div>
    <div class="box">Katak 5</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-column: span 2` elementga o'zi turgan joydan boshlab o'ng tomonga qarab 2 ta ustunni qamrab olishni buyuradi. Qolgan elementlar esa avtomatik tarzda keyingi bo'sh kataklarga oqib o'tadi.

## Ishlash natijasi:
```text
Birinchi qatorda to'q ko'k keng element (2 hissa) va bitta oddiy katak, ikkinchi qatorda esa qolgan 3 ta kataklar joylashadi.
```

---

# 702-Topshiriq: Grid-column: 1 / -1 bilan to'liq kenglikni egallash
## Topshiriq sharti:
Elementning panjaradagi barcha ustunlarni boshidan oxirigacha to'liq qoplab turishini -1 ko'rsatkichi orqali ta'minlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Full Width Span</title>
  <style>
    .grid-box {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      font-family: sans-serif;
    }
    .header-bar {
      grid-column: 1 / -1; /* 1-chiziqdan eng oxirgi chiziqqacha */
      background: #0f172a;
      color: white;
      padding: 14px;
      text-align: center;
      border-radius: 6px;
    }
    .col { background: #64748b; color: white; padding: 12px; text-align: center; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="grid-box">
    <div class="header-bar">To'liq Enli Sarlavha (1 / -1)</div>
    <div class="col">1</div><div class="col">2</div><div class="col">3</div><div class="col">4</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-column: 1 / -1` ifodasidagi `-1` panjaraning eng oxirgi vertikal chizig'ini anglatadi. Ustunlar soni nechta bo'lishidan qat'i nazar, element boshidan oxirigacha butun satrni to'liq qoplaydi.

## Ishlash natijasi:
```text
Tepadagi qora sarlavha barcha 4 ta ustun ustidan to'liq cho'ziladi, pastda esa 4 ta kulrang katak turadi.
```

---

# 703-Topshiriq: Grid-row: span 2 bilan elementni vertikal ikki satrga cho'zish
## Topshiriq sharti:
Chapdagi elementni vertikal 2 qavatga cho'zib, o'ngda ikkita kichik blokni ustma-ust joylashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Row Span</title>
  <style>
    .row-grid {
      display: grid;
      grid-template-columns: 140px 1fr;
      grid-template-rows: 80px 80px;
      gap: 12px;
      font-family: sans-serif;
    }
    .tall-item {
      grid-row: span 2; /* Vertikal 2 satrni egallaydi */
      background: #059669;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
      font-weight: bold;
    }
    .box { background: #e2e8f0; padding: 12px; border-radius: 6px; display: flex; align-items: center; }
  </style>
</head>
<body>
  <div class="row-grid">
    <div class="tall-item">Baland Blok (span 2)</div>
    <div class="box">Yuqori Matn</div>
    <div class="box">Quyi Matn</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-row: span 2` xususiyati elementni vertikal o'q bo'yicha ikkita satr balandligiga cho'zadi. Bu portal va dashboardlarda asosiy bannerlarni yon bloklar bilan yonma-yon qo'yishda keng qo'llaniladi.

## Ishlash natijasi:
```text
Chapda yashil rangli 160px li baland blok, o'ng tomonda esa ustma-ust tushgan ikkita kulrang quti aks etadi.
```

---

# 704-Topshiriq: Grid-area shorthand xususiyati (row-start / col-start / row-end / col-end)
## Topshiriq sharti:
Bitta grid-area xususiyati orqali elementning koordinatalarini 1 / 2 / 3 / 4 shaklida belgilang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Area Shorthand</title>
  <style>
    .area-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: repeat(2, 70px);
      gap: 10px;
      font-family: sans-serif;
    }
    .item-placed {
      grid-area: 1 / 2 / 3 / 4; /* row-start / col-start / row-end / col-end */
      background: #7c3aed;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
    }
    .bg-cell { background: #f1f5f9; border: 1px dashed #cbd5e1; border-radius: 6px; }
  </style>
</head>
<body>
  <div class="area-grid">
    <div class="bg-cell">1-katak</div>
    <div class="item-placed">Grid Area (2x2 maydon)</div>
    <div class="bg-cell">4-katak</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-area: row-start / col-start / row-end / col-end` to'rtala chiziq koordinatasini bitta qatorda ifodalaydi: 1-qatordan 3-qatordacha, 2-ustundan 4-ustungacha bo'lgan 2x2 to'rtburchakni egallaydi.

## Ishlash natijasi:
```text
Binafsha rangli to'rtburchak o'ng tarafdagi 4 ta katakcha o'rnini yaxlit holda qoplaydi.
```

---

# 705-Topshiriq: Grid-template-areas asoslari (Semantik vizual xarita)
## Topshiriq sharti:
header, sidebar, content va footer nomlangan maydonlari orqali veb sahifa karkasini chizing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Template Areas</title>
  <style>
    .site-layout {
      display: grid;
      grid-template-columns: 180px 1fr;
      grid-template-rows: 60px 1fr 40px;
      grid-template-areas:
        "header  header"
        "sidebar content"
        "footer  footer";
      height: 240px;
      gap: 10px;
      font-family: sans-serif;
    }
    .header-area  { grid-area: header;  background: #0f172a; color: white; padding: 12px; }
    .sidebar-area { grid-area: sidebar; background: #334155; color: white; padding: 12px; }
    .content-area { grid-area: content; background: #f8fafc; border: 1px solid #cbd5e1; padding: 12px; }
    .footer-area  { grid-area: footer;  background: #0284c7; color: white; padding: 10px; text-align: center; }
  </style>
</head>
<body>
  <div class="site-layout">
    <header class="header-area">Sarlavha (Header)</header>
    <aside class="sidebar-area">Yon Menyu</aside>
    <main class="content-area">Asosiy Maqola</main>
    <footer class="footer-area">Footer &copy; 2026</footer>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-template-areas` CSS da sahifa maketini ASCII-art kabi vizual xaritada yozish imkonini beradi. Har bir element o'zining `grid-area` nomi orqali xaritadagi o'z zonasiga avtomatik bog'lanadi.

## Ishlash natijasi:
```text
Tepada to'liq sarlavha, o'rtada yon panel va kontent, pastda esa to'liq enli ko'k footer joylashadi.
```

---

# 706-Topshiriq: Grid-template-areas da nuqta (.) orqali bo'sh joy qoldirish
## Topshiriq sharti:
Sxemada ma'lum katakni bo'sh (unoccupied) qoldirish uchun nuqta belgisidan foydalaning.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Area Dot Empty</title>
  <style>
    .empty-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: repeat(2, 60px);
      grid-template-areas:
        "box1 . box2"
        "box3 box3 box3";
      gap: 10px;
      font-family: sans-serif;
    }
    .b1 { grid-area: box1; background: #ef4444; color: white; padding: 10px; border-radius: 4px; }
    .b2 { grid-area: box2; background: #10b981; color: white; padding: 10px; border-radius: 4px; }
    .b3 { grid-area: box3; background: #3b82f6; color: white; padding: 10px; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="empty-grid">
    <div class="b1">Quti 1</div>
    <div class="b2">Quti 2</div>
    <div class="b3">Quti 3 (Pastki butun satr)</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-template-areas` da nuqta (`.`) belgisi o'sha katakning bo'sh qoldirilishini anglatadi. Birinchi satr o'rtasida bo'shliq qolib, qutilar ikki chetga suriladi.

## Ishlash natijasi:
```text
Tepada chapda qizil, o'ngda yashil quti va ularning o'rtasida bo'sh joy, pastda esa butun qatorni egallagan moviy quti.
```

---

# 707-Topshiriq: Bento Grid Layout (Zamonaviy Apple uslubidagi mozaika)
## Topshiriq sharti:
Katta to'rtburchak, baland ustun va kichik kvadratlardan iborat zamonaviy Bento grid interfeysini quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Bento Grid Layout</title>
  <style>
    .bento {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: 110px 110px;
      gap: 14px;
      width: 320px;
      font-family: sans-serif;
    }
    .bento-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 14px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.04);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .hero-bento {
      grid-column: span 2;
      background: #eff6ff;
      border-color: #bfdbfe;
    }
    .tall-bento {
      grid-row: span 2;
      background: #f0fdf4;
      border-color: #bbf7d0;
    }
  </style>
</head>
<body>
  <div class="bento">
    <div class="bento-card hero-bento">
      <h4 style="margin: 0; color: #1e40af;">Asosiy Mahsulot</h4>
      <p style="margin: 0; font-size: 12px; color: #3b82f6;">Katta e'tibor qaratiladigan maydon</p>
    </div>
    <div class="bento-card tall-bento">
      <h4 style="margin: 0; color: #166534;">Statistika</h4>
      <p style="margin: 0; font-size: 12px; color: #15803d;">Vertikal baland karta</p>
    </div>
    <div class="bento-card">
      <h4 style="margin: 0;">Tezlik</h4>
      <small style="color: #64748b;">99.9%</small>
    </div>
    <div class="bento-card">
      <h4 style="margin: 0;">Xavfsizlik</h4>
      <small style="color: #64748b;">SSL 256-bit</small>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Bento Grid dizaynida turli xil `span 2` kombinatsiyalari orqali turli o'lchamdagi to'rtburchak kartalar yapon bento qutisidek estetik uyg'unlikda joylashtiriladi.

## Ishlash natijasi:
```text
Biri keng moviy karta, biri baland yashil karta va ikkita kichik oq kartadan iborat ko'rkam bento mozaikasi.
```

---

# 708-Topshiriq: Holy Grail Layout (CSS Grid Template Areas orqali)
## Topshiriq sharti:
Sarlavha, ikkita yon ustun (nav va ads), asosiy maqola va footerni to'liq grid-template-areas orqali shakllantiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Holy Grail Grid Areas</title>
  <style>
    .grail-container {
      display: grid;
      grid-template-columns: 140px 1fr 120px;
      grid-template-rows: 50px 1fr 40px;
      grid-template-areas:
        "hdr  hdr  hdr"
        "nav  main ads"
        "ftr  ftr  ftr";
      height: 240px;
      gap: 10px;
      font-family: sans-serif;
    }
    .h { grid-area: hdr; background: #0f172a; color: white; display: flex; align-items: center; padding-left: 15px; }
    .n { grid-area: nav; background: #e2e8f0; padding: 10px; }
    .m { grid-area: main; background: #ffffff; border: 1px solid #cbd5e1; padding: 15px; }
    .a { grid-area: ads; background: #fef3c7; padding: 10px; }
    .f { grid-area: ftr; background: #1e293b; color: white; display: flex; align-items: center; justify-content: center; }
  </style>
</head>
<body>
  <div class="grail-container">
    <header class="h">Sarlavha</header>
    <nav class="n">Navigatsiya</nav>
    <main class="m">Asosiy Kontent</main>
    <aside class="a">Reklama</aside>
    <footer class="f">Footer</footer>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-template-areas` tufayli klassik Holy Grail maketi atigi bir necha qatorda o'ta tushunarli va xatosiz yoziladi.

## Ishlash natijasi:
```text
Tepadagi va pastdagi butun enli panellar o'rtasida chap menyu, markaziy maqola va o'ng reklama qutilari.
```

---

# 709-Topshiriq: Grid Overlapping (Elementlarni ustma-ust tushirish)
## Topshiriq sharti:
Ikkita elementning katak koordinatalarini bir-biriga kiritib, ustma-ust soya bilan ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Overlap</title>
  <style>
    .overlap-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: repeat(2, 90px);
      width: 300px;
      font-family: sans-serif;
    }
    .base-card {
      grid-column: 1 / 3;
      grid-row: 1 / 3;
      background: #3b82f6;
      border-radius: 8px;
    }
    .floating-card {
      grid-column: 2 / 4;
      grid-row: 2 / 3;
      background: white;
      border: 1px solid #e2e8f0;
      padding: 14px;
      border-radius: 8px;
      box-shadow: 0 10px 20px rgba(0,0,0,0.15);
      z-index: 2;
    }
  </style>
</head>
<body>
  <div class="overlap-grid">
    <div class="base-card"></div>
    <div class="floating-card">
      <h4 style="margin: 0 0 4px 0;">Ustki Karta</h4>
      <small style="color: #64748b;">Grid overlap usuli</small>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
CSS Gridda bir element `1 / 3`, ikkinchisi esa `2 / 4` ustunlarni egallasa, ular 2-ustunda o'zaro to'qnashadi. `z-index: 2` orqali ikkinchi element birinchisining ustiga chiroyli soya bilan chiqadi.

## Ishlash natijasi:
```text
Ko'k fonli katta to'rtburchak ustiga o'ng pastki tomondan oq soyali karta qisman minib turadi.
```

---

# 710-Topshiriq: Gazeta/Jurnal uslubidagi murakkab maket (Magazine Layout)
## Topshiriq sharti:
Bosh maqolani katta qilib, yonidagi kichik yangiliklarni 2 ta qatorga tizuvchi jurnal panjarasini quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Magazine Grid</title>
  <style>
    .mag-grid {
      display: grid;
      grid-template-columns: 2fr 1fr;
      grid-template-rows: 90px 90px;
      gap: 12px;
      width: 320px;
      font-family: sans-serif;
    }
    .mag-lead {
      grid-row: span 2;
      background: #0f172a;
      color: white;
      padding: 16px;
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
    }
    .mag-side {
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      padding: 10px;
      border-radius: 6px;
      font-size: 12px;
    }
  </style>
</head>
<body>
  <div class="mag-grid">
    <div class="mag-lead">
      <h3 style="margin: 0 0 6px 0;">Bosh Yangilik</h3>
      <small style="color: #94a3b8;">Katta xalqaro forum boshlandi</small>
    </div>
    <div class="mag-side"><strong>Qisqa 1:</strong> Yangi qonun loyihasi</div>
    <div class="mag-side"><strong>Qisqa 2:</strong> Texnologik startaplar</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Chapdagi bosh maqola `grid-row: span 2` orqali ikkala satr balandligini egallaydi, o'ngdagi 1fr ustunga esa ikkita kichik xabar ketma-ket joylashadi.

## Ishlash natijasi:
```text
Chapda qora fondagi yirik yangilik, o'ngda esa ikkita kichikroq yangiliklar bloki.
```

---

# 711-Topshiriq: Responsive Grid Template Areas (Media Query orqali sxemani o'zgartirish)
## Topshiriq sharti:
Ekran tor bo'lganda sidebar va contentni ustun holatiga keltiruvchi mobil qayta tartiblash tamoyili.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Responsive Grid Areas</title>
  <style>
    .resp-layout {
      display: grid;
      grid-template-columns: 1fr;
      grid-template-areas:
        "header"
        "content"
        "sidebar"
        "footer";
      gap: 10px;
      font-family: sans-serif;
      width: 260px;
    }
    .h { grid-area: header; background: #1e293b; color: white; padding: 10px; }
    .c { grid-area: content; background: #3b82f6; color: white; padding: 15px; }
    .s { grid-area: sidebar; background: #64748b; color: white; padding: 10px; }
    .f { grid-area: footer; background: #0f172a; color: white; padding: 8px; text-align: center; }
  </style>
</head>
<body>
  <div class="resp-layout">
    <div class="h">Header</div>
    <div class="c">Asosiy Kontent (Mobilda birinchi)</div>
    <div class="s">Sidebar (Mobilda pastga tushadi)</div>
    <div class="f">Footer</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-template-areas` ning kuchi shundaki, bitta media query orqali qatorlar xaritasini almashtirib, HTML ga teginmasdan butun dizaynni mobildan desktopga o'girish mumkin.

## Ishlash natijasi:
```text
Mobil o'lchamda barcha bo'limlar bitta vertikal ustunga ketma-ket tartibda teriladi.
```

---

# 712-Topshiriq: Grid yordamida Full-Bleed Section maketi (Markaziy konteyner va chetga cho'ziluvchi fon)
## Topshiriq sharti:
[full-start] [content-start] [content-end] [full-end] 3 ustunli zamonaviy veb arxitekturasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Full Bleed Grid</title>
  <style>
    .page-wrapper {
      display: grid;
      grid-template-columns: 1fr minmax(auto, 260px) 1fr;
      font-family: sans-serif;
    }
    .normal-content {
      grid-column: 2;
      background: #f1f5f9;
      padding: 16px;
    }
    .full-bleed-banner {
      grid-column: 1 / -1;
      background: #2563eb;
      color: white;
      padding: 20px;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="page-wrapper">
    <div class="normal-content">Ushbu matn markaziy 260px ustun ichida cheklangan.</div>
    <div class="full-bleed-banner">Ushbu banner esa butun ekranning chekkalarigacha to'liq cho'ziladi!</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`1fr minmax(auto, 260px) 1fr` tizimida markaziy blok `grid-column: 2` bilan o'rtada cheklanadi, banner esa `grid-column: 1 / -1` bilan ekranning chetlariga borib yopishadi.

## Ishlash natijasi:
```text
Markazda turgan ixcham matn bloki va uning ostida butun enni qoplagan ko'k banner.
```

---

# 713-Topshiriq: Admin Dashboard Grid (KPI lar, Grafika va So'nggi buyurtmalar jadvali)
## Topshiriq sharti:
Header, 2 ta KPI karta, katta grafika maydoni va buyurtmalar jadvalini grid-template-areas orqali yig'ing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Admin Dashboard Areas</title>
  <style>
    .dashboard {
      display: grid;
      grid-template-columns: 1fr 1fr;
      grid-template-rows: auto auto 100px;
      grid-template-areas:
        "kpi1   kpi2"
        "chart  chart"
        "table  table";
      gap: 12px;
      width: 320px;
      font-family: sans-serif;
    }
    .kpi { background: white; border: 1px solid #cbd5e1; padding: 12px; border-radius: 6px; }
    .k1 { grid-area: kpi1; }
    .k2 { grid-area: kpi2; }
    .ch { grid-area: chart; height: 90px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 6px; padding: 10px; }
    .tb { grid-area: table; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px; }
  </style>
</head>
<body>
  <div class="dashboard">
    <div class="kpi k1"><strong>Mijozlar:</strong> 1,200</div>
    <div class="kpi k2"><strong>Daromad:</strong> $14k</div>
    <div class="ch">Oylik sotuvlar grafigi maydoni</div>
    <div class="tb">So'nggi buyurtmalar ro'yxati</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ikkita yuqori KPI 1fr dan yonma-yon turadi, grafik va jadval esa `chart chart` hamda `table table` orqali butun enni qoplab, haqiqiy boshqaruv paneli ko'rinishini beradi.

## Ishlash natijasi:
```text
Tepada 2 ta statistika kartasi, ostida keng grafik maydoni va eng pastda buyurtmalar paneli.
```

---

# 714-Topshiriq: Grid yordamida rasm va matnli qatorlarning shaxmat tartibi (Alternating Grid)
## Topshiriq sharti:
1-qatorda Rasm-Matn, 2-qatorda Matn-Rasm tartibini grid-column koordinatalari bilan hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Alternating Chess Grid</title>
  <style>
    .chess-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      width: 300px;
      font-family: sans-serif;
    }
    .thumb { height: 70px; background: #64748b; border-radius: 6px; }
    .desc { background: #f8fafc; padding: 10px; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 13px; }
    .order-flip-img { grid-column: 2; grid-row: 2; }
    .order-flip-txt { grid-column: 1; grid-row: 2; }
  </style>
</head>
<body>
  <div class="chess-grid">
    <div class="thumb"></div>
    <div class="desc">1-Qator: Chapda rasm, o'ngda matn.</div>
    <div class="thumb order-flip-img"></div>
    <div class="desc order-flip-txt">2-Qator: Chapda matn, o'ngda rasm.</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ikkinchi qatordagi elementlarning `grid-column` qiymatlarini 2 va 1 qilib belgilash orqali HTML manzilini buzmasdan shaxmat tartibida almashuvchi chiroyli dizayn olinadi.

## Ishlash natijasi:
```text
Birinchi qatorda rasm-matn, ikkinchi qatorda esa aksincha matn-rasm joylashgan tartib.
```

---

# 715-Topshiriq: Grid-column: 2 / span 2 orqali offset (surilgan) element yaratish
## Topshiriq sharti:
Birinchi ustunni bo'sh qoldirib, elementni 2-ustundan boshlab 2 ta katakcha kengligida joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Column Offset</title>
  <style>
    .offset-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      background: #f1f5f9;
      padding: 14px;
      font-family: sans-serif;
    }
    .offset-item {
      grid-column: 2 / span 2; /* 2-ustundan boshlanib 2 ta ustunni oladi */
      background: #8b5cf6;
      color: white;
      padding: 14px;
      text-align: center;
      border-radius: 6px;
    }
  </style>
</head>
<body>
  <div class="offset-grid">
    <div class="offset-item">Surilgan Blok (2-chiziqdan boshlanadi)</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-column: 2 / span 2` 1-ustunni to'liq bo'sh qoldiradi va elementni 2-ustundan boshlab 2 ta ustunga cho'zadi. Bu maketlarda bo'shliqlar va chekinishlar bilan ishlashning oson yo'lidir.

## Ishlash natijasi:
```text
Chapdan 1 katak bo'sh joy qolib, o'rtada binafsharang blok aks etadi.
```

---

# 716-Topshiriq: Asimmetrik Fotogalereya (Asymmetric Hero Grid)
## Topshiriq sharti:
1 ta katta kvadrat surat va yonida 4 ta kichik kvadrat suratdan iborat panjara tuzing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Asymmetric Gallery</title>
  <style>
    .asym-gallery {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: 70px 70px;
      gap: 8px;
      width: 300px;
    }
    .big-photo {
      grid-column: span 2;
      grid-row: span 2;
      background: #0284c7;
      border-radius: 6px;
    }
    .small-photo { background: #94a3b8; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="asym-gallery">
    <div class="big-photo"></div>
    <div class="small-photo"></div>
    <div class="small-photo"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`big-photo` `grid-column: span 2; grid-row: span 2` orqali 2x2 maydonni oladi, qolgan 1 ta ustunda esa ikkita kichik fotosurat vertikal joylashadi.

## Ishlash natijasi:
```text
Chapda katta moviy surat maydoni, o'ngda esa ikkita kichikroq kulrang kvadratlar.
```

---

# 717-Topshiriq: Grid yordamida Markaziy Modal oynani qoplash (No Absolute)
## Topshiriq sharti:
Butun ekranni qoplovchi grid yaratib, place-items: center bilan modal darchani markazlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Modal with Grid</title>
  <style>
    .grid-overlay {
      display: grid;
      place-items: center;
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.6);
      font-family: sans-serif;
    }
    .modal-card {
      background: white;
      padding: 24px;
      border-radius: 10px;
      width: 260px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
  </style>
</head>
<body>
  <div class="grid-overlay">
    <div class="modal-card">
      <h3 style="margin-top:0;">Grid Modal</h3>
      <p style="color: #64748b; font-size: 14px;">place-items: center orqali ekranning mutlaq o'rtasida joylashgan.</p>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: grid; place-items: center` modal darchani har ikkala o'q bo'yicha markazga joylashtirish uchun yozilishi mumkin bo'lgan eng qisqa CSS kodidir.

## Ishlash natijasi:
```text
To'q qora xira fonda qoq markazda turgan oq modal darcha.
```

---

# 718-Topshiriq: Grid-row bo'yicha manfiy chiziqlar (-1) bilan ishlash
## Topshiriq sharti:
Elementning barcha vertikal satrlarni yuqoridan pastgacha to'liq qoplab turishini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Row Negative Line</title>
  <style>
    .full-row-grid {
      display: grid;
      grid-template-columns: 100px 1fr;
      grid-template-rows: repeat(3, 50px);
      gap: 10px;
      font-family: sans-serif;
    }
    .sidebar-strip {
      grid-row: 1 / -1; /* Barcha satrlarni yuqoridan pastgacha qoplaydi */
      background: #1e293b;
      color: white;
      padding: 10px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .r-item { background: #e2e8f0; border-radius: 4px; padding: 10px; }
  </style>
</head>
<body>
  <div class="full-row-grid">
    <div class="sidebar-strip">Ustun (1 / -1)</div>
    <div class="r-item">Qator 1</div>
    <div class="r-item">Qator 2</div>
    <div class="r-item">Qator 3</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-row: 1 / -1` chap tomondagi ustunning barcha satrlarni (1 dan oxirgisigacha) bitta yaxlit vertikal blok sifatida qamrab olishini ta'minlaydi.

## Ishlash natijasi:
```text
Chapda to'liq balandlikdagi qora tasma, o'ngda esa 3 ta kulrang qatorlar.
```

---

# 719-Topshiriq: Grid orqali 3D kartaning orqa va old tomonini qavatlash
## Topshiriq sharti:
Bir xil grid katagiga ikkita elementni joylab, biri ikkinchisining foni bo'lishini hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Card Stacking Grid</title>
  <style>
    .card-stack {
      display: grid;
      width: 240px;
      height: 140px;
      font-family: sans-serif;
    }
    .bg-gradient {
      grid-area: 1 / 1;
      background: linear-gradient(135deg, #4f46e5, #06b6d4);
      border-radius: 10px;
    }
    .content-front {
      grid-area: 1 / 1;
      color: white;
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      z-index: 1;
    }
  </style>
</head>
<body>
  <div class="card-stack">
    <div class="bg-gradient"></div>
    <div class="content-front">
      <strong>Bank Kartasi</strong>
      <span>**** 8842</span>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-area: 1 / 1` fon va matnni aynan bir katak ustiga qatlamlab qo'yadi. Natijada qo'shimcha wrapper va absolut joylashuvlarsiz toza plastik karta dizayni olinadi.

## Ishlash natijasi:
```text
Gradient rangli chiroyli bank kartasi va uning ustida oq rangli ma'lumotlar.
```

---

# 720-Topshiriq: To'liq murakkab Grid Portali: 6 zonali Grid Template Areas
## Topshiriq sharti:
Logo, Nav, Hero, Sidebar, Feed va Footer maydonlarini to'liq birlashtiruvchi ekotizim maketini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Complete Complex Grid Portal</title>
  <style>
    .portal-master {
      display: grid;
      grid-template-columns: 160px 1fr 140px;
      grid-template-rows: 50px 100px 1fr 40px;
      grid-template-areas:
        "logo    topbar  topbar"
        "sidebar hero    hero"
        "sidebar feed    widgets"
        "footer  footer  footer";
      height: 320px;
      gap: 10px;
      font-family: sans-serif;
    }
    .z-logo { grid-area: logo; background: #2563eb; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; }
    .z-top { grid-area: topbar; background: #1e293b; color: white; display: flex; align-items: center; padding-left: 15px; }
    .z-side { grid-area: sidebar; background: #f1f5f9; padding: 12px; border: 1px solid #cbd5e1; }
    .z-hero { grid-area: hero; background: #dbeafe; padding: 15px; border-radius: 6px; }
    .z-feed { grid-area: feed; background: white; border: 1px solid #e2e8f0; padding: 12px; }
    .z-widg { grid-area: widgets; background: #fef3c7; padding: 10px; }
    .z-foot { grid-area: footer; background: #0f172a; color: white; display: flex; align-items: center; justify-content: center; }
  </style>
</head>
<body>
  <div class="portal-master">
    <div class="z-logo">LOGO</div>
    <div class="z-top">Qidiruv va Profil</div>
    <div class="z-side">Yon Menyu</div>
    <div class="z-hero">Katta Yangilik Banneri</div>
    <div class="z-feed">Yangiliklar Lentasi</div>
    <div class="z-widg">Ob-havo</div>
    <div class="z-foot">Barcha huquqlar himoyalangan &copy; 2026</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu arxitektura zamonaviy murakkab web ilovalarning yadro karkasini tashkil qiladi. 6 ta xilma-xil zona `grid-template-areas` orqali to'liq muvozanatda birlashtirilgan.

## Ishlash natijasi:
```text
Ko'k logotip, qora topbar, yon panel, o'rtada banner va lenta, o'ngda vidjet hamda pastda footer bilan to'liq portal.
```

---

# 721-Topshiriq: Grid-template-areas bilan mobil qidiruv va filtr oynasi
## Topshiriq sharti:
Filtr paneli, saralash tugmasi va natijalar maydonini nomlangan hududlar orqali tartiblang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Filter Areas</title>
  <style>
    .filter-layout {
      display: grid;
      grid-template-columns: 1fr 100px;
      grid-template-areas:
        "search sort"
        "results results";
      gap: 10px;
      width: 300px;
      font-family: sans-serif;
    }
    .s-search { grid-area: search; padding: 8px; border: 1px solid #cbd5e1; border-radius: 4px; }
    .s-sort { grid-area: sort; background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 4px; }
    .s-results { grid-area: results; background: #ffffff; border: 1px solid #e2e8f0; padding: 12px; }
  </style>
</head>
<body>
  <div class="filter-layout">
    <input type="text" class="s-search" placeholder="Qidirish...">
    <button class="s-sort">Saralash</button>
    <div class="s-results">12 ta natija topildi.</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Qidiruv va Saralash birinchi qatorda yonma-yon turadi, 'results' esa ikkala ustunni qoplab pastda aks etadi.

## Ishlash natijasi:
```text
Tepada qidiruv va saralash tugmasi, pastda esa to'liq kenglikdagi natijalar paneli.
```

---

# 722-Topshiriq: Grid yordamida shaxmat taxtasi (8x8 Chessboard)
## Topshiriq sharti:
repeat(8, 1fr) va nth-child formulasi orqali 8x8 qora va oq shaxmat taxtasi yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Chessboard Grid</title>
  <style>
    .board {
      display: grid;
      grid-template-columns: repeat(8, 24px);
      grid-template-rows: repeat(8, 24px);
      border: 2px solid #334155;
      width: fit-content;
    }
    .sq { background: #f8fafc; }
    .board div:nth-child(16n+1), .board div:nth-child(16n+3),
    .board div:nth-child(16n+5), .board div:nth-child(16n+7),
    .board div:nth-child(16n+10), .board div:nth-child(16n+12),
    .board div:nth-child(16n+14), .board div:nth-child(16n+16) {
      background: #475569;
    }
  </style>
</head>
<body>
  <div class="board">
    <div class="sq"></div><div class="sq"></div><div class="sq"></div><div class="sq"></div><div class="sq"></div><div class="sq"></div><div class="sq"></div><div class="sq"></div>
    <div class="sq"></div><div class="sq"></div><div class="sq"></div><div class="sq"></div><div class="sq"></div><div class="sq"></div><div class="sq"></div><div class="sq"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
CSS Grid 8 ta ustun va 8 ta satrni mukammal panjaraga soladi, ranglar esa shaxmat tartibida almashadi.

## Ishlash natijasi:
```text
Kvadrat katakchalardan iborat shaxmat taxtasi qolipi.
```

---

# 723-Topshiriq: Grid-column span yordamida matn ichiga katta iqtibos (Pull Quote) kiritish
## Topshiriq sharti:
3 ustunli maqola matni orasida 2 ta ustunni egallaydigan diqqatga sazovor iqtibos qutisini joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Pull Quote Grid</title>
  <style>
    .article-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      font-family: sans-serif;
      width: 320px;
      font-size: 12px;
    }
    .text-block { background: #f8fafc; padding: 10px; border-radius: 4px; }
    .pull-quote {
      grid-column: span 2;
      background: #eff6ff;
      border-left: 4px solid #2563eb;
      padding: 12px;
      font-style: italic;
      font-size: 13px;
      color: #1e40af;
    }
  </style>
</head>
<body>
  <div class="article-grid">
    <div class="text-block">1-paragraf matni...</div>
    <div class="pull-quote">"Kelajak veb-texnologiyalari CSS Grid va Flexbox uyg'unligida rivojlanmoqda."</div>
    <div class="text-block">2-paragraf matni...</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-column: span 2` muhim iqtibosni 2 ustunga yoyib, kitobxonda vizual urg'u hosil qiladi.

## Ishlash natijasi:
```text
Matnlar orasida ko'k hoshiyali kengaytirilgan iqtibos bloki turadi.
```

---

# 724-Topshiriq: Grid yordamida dinamik solishtirish jadvali (Feature Comparison)
## Topshiriq sharti:
Chapda imkoniyatlar nomi, o'ngda esa Reja A va Reja B ko'rsatkichlari bo'lgan 3 ustunli jadval quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Comparison Grid</title>
  <style>
    .comp-grid {
      display: grid;
      grid-template-columns: 140px 80px 80px;
      gap: 1px;
      background: #cbd5e1;
      width: 302px;
      font-family: sans-serif;
      font-size: 12px;
    }
    .c-cell { background: white; padding: 8px; text-align: center; }
    .c-title { text-align: left; font-weight: bold; }
    .c-head { background: #1e293b; color: white; font-weight: bold; }
  </style>
</head>
<body>
  <div class="comp-grid">
    <div class="c-cell c-head">Xususiyat</div><div class="c-cell c-head">Oddiy</div><div class="c-cell c-head">Pro</div>
    <div class="c-cell c-title">Xotira hajmi</div><div class="c-cell">5 GB</div><div class="c-cell">50 GB</div>
    <div class="c-cell c-title">Foydalanuvchilar</div><div class="c-cell">1</div><div class="c-cell">Cheksiz</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`140px 80px 80px` ustunlari orqali har bir qator 1px li toza chegara bilan taqqoslash paneli hosil qiladi.

## Ishlash natijasi:
```text
Chiroyli chiziqli 3 ustunli tariflar taqqoslash jadvali.
```

---

# 725-Topshiriq: Grid elementining burchagini manfiy margin bilan chiqarish
## Topshiriq sharti:
Grid katagidagi elementni o'z maydonidan 10px tashqariga chiqarib vizual chuqurlik bering.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Negative Margin</title>
  <style>
    .wrap-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      background: #e2e8f0;
      padding: 24px;
      font-family: sans-serif;
      width: 260px;
    }
    .pop-card {
      background: #ef4444;
      color: white;
      padding: 16px;
      border-radius: 8px;
      margin-top: -12px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }
    .base-box { background: white; padding: 16px; border-radius: 8px; }
  </style>
</head>
<body>
  <div class="wrap-grid">
    <div class="pop-card">Bo'rtib chiqqan karta</div>
    <div class="base-box">Oddiy karta</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Grid katagi ichidagi elementga `margin-top: -12px` berilsa, u panjara chegarasini buzib yuqoriga chiqadi va dinamik chuqurlik beradi.

## Ishlash natijasi:
```text
Qizil karta kulrang maydondan biroz yuqoriga chiqib soyali turadi.
```

---

# 726-Topshiriq: Grid yordamida mahsulot rasmining kattalashtirilgan ko'rinishi (Zoom Showcase)
## Topshiriq sharti:
Chapda 4 ta kichik rasm ustuni, o'ngda esa 1 ta katta faol rasm maydonini quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Product Showcase Grid</title>
  <style>
    .showcase {
      display: grid;
      grid-template-columns: 50px 1fr;
      gap: 10px;
      width: 260px;
      font-family: sans-serif;
    }
    .thumb-col { display: grid; gap: 6px; }
    .thumb { height: 35px; background: #cbd5e1; border-radius: 4px; }
    .main-view { background: #3b82f6; border-radius: 6px; }
  </style>
</head>
<body>
  <div class="showcase">
    <div class="thumb-col">
      <div class="thumb"></div>
      <div class="thumb"></div>
      <div class="thumb"></div>
    </div>
    <div class="main-view"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Chapdagi `50px` ustun kichik prevyular uchun, `1fr` esa katta rasm uchun xizmat qiladi.

## Ishlash natijasi:
```text
Chapda 3 ta kichik to'rtburchak prevyu, o'ngda esa katta ko'k rasm ekrani.
```

---

# 727-Topshiriq: Grid yordamida murakkab foydalanuvchi profili (Avatar, Bio, Statistika)
## Topshiriq sharti:
Avatar (chapda baland), ism va kasb (o'ng tepada), statistika (o'ng pastda) ko'rinishidagi profil kartasini quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>User Profile Grid</title>
  <style>
    .profile-card {
      display: grid;
      grid-template-columns: 80px 1fr;
      grid-template-rows: auto auto;
      gap: 12px;
      background: white;
      border: 1px solid #cbd5e1;
      padding: 16px;
      border-radius: 8px;
      font-family: sans-serif;
      width: 280px;
    }
    .p-avatar {
      grid-row: span 2;
      width: 80px;
      height: 80px;
      background: #6366f1;
      border-radius: 8px;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="profile-card">
    <div class="p-avatar">JS</div>
    <div><strong>Jasur Saidov</strong><br><small style="color:#64748b;">Frontend Dasturchi</small></div>
    <div style="font-size: 12px; color: #16a34a;">&#9679; Masofadan ishlashga tayyor</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`p-avatar` `grid-row: span 2` bilan chap tomonda to'liq balandlikni oladi, o'ngdagi ikkita qatorga esa ma'lumotlar tushadi.

## Ishlash natijasi:
```text
Chapda katta kvadrat avatar, o'ngda ism, lavozim va status yozuvi.
```

---

# 728-Topshiriq: Grid-template-columns: repeat(auto-fit, minmax(60px, 1fr)) mini piktogrammalar
## Topshiriq sharti:
Har biri kamida 60px bo'lgan texnologiyalar piktogrammalari panjarasini yasang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Tech Icons Auto-Fit</title>
  <style>
    .icons-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(60px, 1fr));
      gap: 10px;
      width: 280px;
      font-family: sans-serif;
    }
    .tech-box {
      aspect-ratio: 1;
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: bold;
      color: #334155;
    }
  </style>
</head>
<body>
  <div class="icons-grid">
    <div class="tech-box">HTML</div>
    <div class="tech-box">CSS</div>
    <div class="tech-box">JS</div>
    <div class="tech-box">REACT</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`minmax(60px, 1fr)` va `aspect-ratio: 1` orqali to'rtta kvadrat piktogramma ekranga moslashib joylashadi.

## Ishlash natijasi:
```text
Kvadrat kulrang katakchalarda texnologiyalar qisqartmalari.
```

---

# 729-Topshiriq: Grid yordamida dialog oynasi (Header, Content, Action Buttons)
## Topshiriq sharti:
Grid rows yordamida sarlavha, ichki matn va harakat tugmalarini qat'iy tartibda yig'ing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Dialog Grid</title>
  <style>
    .dialog {
      display: grid;
      grid-template-rows: auto 1fr auto;
      gap: 12px;
      width: 260px;
      height: 160px;
      background: white;
      border: 1px solid #cbd5e1;
      padding: 16px;
      border-radius: 8px;
      font-family: sans-serif;
    }
    .d-head { font-weight: bold; }
    .d-body { color: #64748b; font-size: 13px; }
    .d-btns { display: flex; justify-content: flex-end; gap: 8px; }
  </style>
</head>
<body>
  <div class="dialog">
    <div class="d-head">O'chirishni tasdiqlaysizmi?</div>
    <div class="d-body">Bu amalni keyinchalik bekor qilib bo'lmaydi.</div>
    <div class="d-btns">
      <button style="padding: 4px 8px;">Yo'q</button>
      <button style="padding: 4px 8px; background: #ef4444; color: white; border: none; border-radius: 3px;">Ha</button>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-template-rows: auto 1fr auto` sarlavha va tugmalarni qirralarga taqab, o'rta sohani elastik ushlab turadi.

## Ishlash natijasi:
```text
Tepadagi ogohlantirish, o'rtadagi tushuntirish va pastki o'ngdagi tasdiqlash tugmalari.
```

---

# 730-Topshiriq: Gridda elementlarni kesishuvchi chiziqlarga qo'yish (Grid Line Crossing)
## Topshiriq sharti:
Elementni 1-satrdan 3-satrgacha, 2-ustundan 4-ustungacha aniq chiziq raqamlari bilan o'tkazing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Line Crossing</title>
  <style>
    .cross-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      grid-template-rows: repeat(3, 50px);
      gap: 8px;
      background: #f8fafc;
      padding: 10px;
      font-family: sans-serif;
    }
    .target-box {
      grid-row: 1 / 3;
      grid-column: 2 / 4;
      background: #10b981;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
    }
    .empty-cell { background: #e2e8f0; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="cross-grid">
    <div class="empty-cell"></div>
    <div class="target-box">2x2 Yashil Maydon</div>
    <div class="empty-cell"></div>
    <div class="empty-cell"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Chiziqlar bo'yicha aniq koordinatalash orqali panjaraning istalgan joyida to'rtburchaklar hosil qilish mumkin.

## Ishlash natijasi:
```text
Panjaraning markazida 2x2 o'lchamli yashil to'rtburchak joylashadi.
```

---

# 731-Topshiriq: Grid yordamida ikkita ustunli sozlamalar (Settings) paneli
## Topshiriq sharti:
Chapda parametr nomi va tavsifi, o'ngda esa yoqish/o'chirish tugmachasi bo'lgan sozlamalar qatorini quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Settings Grid</title>
  <style>
    .settings-row {
      display: grid;
      grid-template-columns: 1fr 50px;
      gap: 12px;
      align-items: center;
      width: 300px;
      padding: 12px;
      background: white;
      border-bottom: 1px solid #e2e8f0;
      font-family: sans-serif;
    }
  </style>
</head>
<body>
  <div class="settings-row">
    <div>
      <strong>Qorong'i rejim</strong><br>
      <small style="color: #64748b;">Tungi rejimni yoqish</small>
    </div>
    <input type="checkbox" checked style="width: 20px; height: 20px;">
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`1fr 50px` matn sohasiga maksimal bo'sh joy beradi va checkboxni o'ng tomonda bir xil tekislikda ushlaydi.

## Ishlash natijasi:
```text
Chapda sozlama sarlavhasi va tavsifi, o'ngda esa checkbox tugmasi.
```

---

# 732-Topshiriq: Grid-template-areas yordamida ko'p qatorli yangiliklar bloki
## Topshiriq sharti:
Foto, sarlavha, sana va batafsil tugmasini nomlangan maydonlar bilan birlashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>News Card Areas</title>
  <style>
    .news-box {
      display: grid;
      grid-template-columns: 90px 1fr;
      grid-template-areas:
        "img title"
        "img date"
        "img btn";
      gap: 6px 12px;
      width: 280px;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      padding: 10px;
      border-radius: 8px;
      font-family: sans-serif;
    }
    .n-img { grid-area: img; background: #64748b; border-radius: 6px; }
    .n-title { grid-area: title; font-weight: bold; font-size: 14px; }
    .n-date { grid-area: date; font-size: 11px; color: #94a3b8; }
    .n-btn { grid-area: btn; color: #2563eb; font-size: 12px; text-decoration: none; font-weight: bold; }
  </style>
</head>
<body>
  <div class="news-box">
    <div class="n-img"></div>
    <div class="n-title">Yangi standartlar</div>
    <div class="n-date">08 Noyabr 2026</div>
    <a href="#" class="n-btn">Batafsil &rarr;</a>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`img` maydoni uchala qator bo'ylab cho'zilib turadi, o'ng tomonga esa ketma-ket sarlavha, sana va havola tushadi.

## Ishlash natijasi:
```text
Chapda baland rasm foni, o'ngda sarlavha, sana va ko'k havola.
```

---

# 733-Topshiriq: Grid yordamida video pleer va yon pleylist (Video Playlist Layout)
## Topshiriq sharti:
Chapda 2fr li katta video ekrani, o'ngda esa 1fr li video darslar ro'yxatini shakllantiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Video Playlist Grid</title>
  <style>
    .player-grid {
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 14px;
      width: 320px;
      font-family: sans-serif;
    }
    .main-screen { height: 120px; background: #0f172a; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: white; }
    .playlist { display: grid; gap: 6px; }
    .pl-item { background: #f1f5f9; padding: 6px; font-size: 11px; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="player-grid">
    <div class="main-screen">&#9658; Asosiy Video</div>
    <div class="playlist">
      <div class="pl-item">1. Kirish</div>
      <div class="pl-item">2. Grid asoslari</div>
      <div class="pl-item">3. Amaliyot</div>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
2fr va 1fr nisbatidagi ustunlar video darslar portalining eng qulay ko'rinishini hosil qiladi.

## Ishlash natijasi:
```text
Chapda katta qora video maydoni, o'ngda esa 3 ta darslar ro'yxati.
```

---

# 734-Topshiriq: Grid yordamida audio mikser slayderlari paneli
## Topshiriq sharti:
5 ta ovoz kanalini repeat(5, 1fr) va vertical align bilan tartiblang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Audio Mixer Grid</title>
  <style>
    .mixer {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 8px;
      background: #1e293b;
      padding: 16px;
      border-radius: 8px;
      width: 220px;
      font-family: sans-serif;
      text-align: center;
    }
    .track {
      height: 90px;
      background: #334155;
      border-radius: 4px;
      display: flex;
      align-items: flex-end;
      padding: 4px;
    }
    .bar { width: 100%; background: #10b981; border-radius: 2px; }
  </style>
</head>
<body>
  <div class="mixer">
    <div class="track"><div class="bar" style="height: 60%;"></div></div>
    <div class="track"><div class="bar" style="height: 85%;"></div></div>
    <div class="track"><div class="bar" style="height: 40%;"></div></div>
    <div class="track"><div class="bar" style="height: 70%;"></div></div>
    <div class="track"><div class="bar" style="height: 95%;"></div></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Grid 5 ta teng vertikal yo'lak ajratib beradi, ichidagi barlar esa turli balandlikda ekvalayzer hosil qiladi.

## Ishlash natijasi:
```text
Qora fonda 5 ta yashil ovoz darajalari ko'rsatkichi.
```

---

# 735-Topshiriq: Gridda auto-fit va minmax orqali responsiv jadvallar
## Topshiriq sharti:
Kichik ekranda satrlar ustun shakliga o'tuvchi responsiv karta jadvali.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Responsive Table Grid</title>
  <style>
    .r-table {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 10px;
      width: 280px;
      font-family: sans-serif;
    }
    .r-row {
      background: white;
      border: 1px solid #cbd5e1;
      padding: 12px;
      border-radius: 6px;
    }
  </style>
</head>
<body>
  <div class="r-table">
    <div class="r-row"><strong>Ali:</strong> 95 ball</div>
    <div class="r-row"><strong>Vali:</strong> 88 ball</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`repeat(auto-fit, minmax(130px, 1fr))` kichik qurilmalarda ham jadvalning gorizontal skroll bo'lib ketmasligini ta'minlaydi.

## Ishlash natijasi:
```text
Ikkita ma'lumot qutisi ekranga qarab yonma-yon yoki ustma-ust turadi.
```

---

# 736-Topshiriq: Grid-template-areas da bo'shliqlar va simmetriya (T-Shaped Layout)
## Topshiriq sharti:
T harfi shaklidagi sarlavha va markaziy ustun maketini nuqtalar yordamida quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>T-Shape Grid</title>
  <style>
    .t-grid {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      grid-template-areas:
        "top  top  top"
        ".    stem .";
      gap: 10px;
      width: 280px;
      font-family: sans-serif;
    }
    .g-top { grid-area: top; background: #2563eb; color: white; padding: 12px; text-align: center; border-radius: 4px; }
    .g-stem { grid-area: stem; background: #93c5fd; padding: 20px; text-align: center; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="t-grid">
    <div class="g-top">T-Sarlavha (3 ustun)</div>
    <div class="g-stem">Markaziy Ustun</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ikkinchi satrdagi `. stem .` ifodasi chap va o'ng kataklarni bo'sh qoldirib, faqat markaziy katakni to'ldiradi.

## Ishlash natijasi:
```text
T harfi shaklidagi ko'k rangli geometrik struktura.
```

---

# 737-Topshiriq: Grid yordamida status kartochkasi (Ikonka, Matn, Foiz o'sishi)
## Topshiriq sharti:
3 ustunli gorizontal status lentasini grid bilan tekislang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Status Row Grid</title>
  <style>
    .status-item {
      display: grid;
      grid-template-columns: 40px 1fr 60px;
      align-items: center;
      gap: 10px;
      width: 280px;
      background: #f8fafc;
      padding: 10px;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      font-family: sans-serif;
    }
  </style>
</head>
<body>
  <div class="status-item">
    <span style="font-size: 20px;">&#128176;</span>
    <div><strong>Daromad</strong><br><small style="color:#64748b;">Bugungi</small></div>
    <span style="color: #16a34a; font-weight: bold; text-align: right;">+18%</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`40px 1fr 60px` tuzilishi chekka elementlarni qat'iy ushlab, markazga to'liq maydon beradi.

## Ishlash natijasi:
```text
Pul xaltasi ikonkasi, 'Daromad' yozuvi va o'ngda yashil '+18%' foizi.
```

---

# 738-Topshiriq: Grid yordamida ko'p bosqichli test savoli interfeysi
## Topshiriq sharti:
Savol raqami (40px) va variant matni (1fr) juftligini grid qilib bering.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Quiz Option Grid</title>
  <style>
    .quiz-opt {
      display: grid;
      grid-template-columns: 36px 1fr;
      align-items: center;
      gap: 10px;
      width: 280px;
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 8px;
      font-family: sans-serif;
      margin-bottom: 8px;
    }
    .opt-letter {
      width: 36px;
      height: 36px;
      background: #eff6ff;
      color: #2563eb;
      font-weight: bold;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="quiz-opt">
    <div class="opt-letter">A</div>
    <div>display: grid xususiyati</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Kvadrat harf katagi va uning yonidagi javob matni grid orqali bir xil o'qda turadi.

## Ishlash natijasi:
```text
Moviy 'A' harfi va uning o'ng tomonida test varianti matni.
```

---

# 739-Topshiriq: Grid yordamida moslashuvchan ko'p qatlamli kalendar rejasi
## Topshiriq sharti:
Soat ustuni (60px) va rejalashtirilgan ishlar maydoni (1fr) bo'lgan kunlik reja paneli.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Schedule Grid</title>
  <style>
    .schedule {
      display: grid;
      grid-template-columns: 60px 1fr;
      gap: 10px;
      width: 280px;
      font-family: sans-serif;
      font-size: 13px;
    }
    .time-slot { color: #64748b; font-weight: bold; text-align: right; }
    .task-slot { background: #eff6ff; border-left: 3px solid #3b82f6; padding: 6px 10px; border-radius: 0 4px 4px 0; }
  </style>
</head>
<body>
  <div class="schedule">
    <div class="time-slot">09:00</div>
    <div class="task-slot">Jamoaviy miting</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Vaqt va rejalashtirilgan vazifalar grid orqali bir chiziqda tekis chiqadi.

## Ishlash natijasi:
```text
Chapda '09:00' vaqti, o'ngda esa ko'k hoshiyali 'Jamoaviy miting' qutisi.
```

---

# 740-Topshiriq: Grid-column: span va grid-row: span birgalikda (2x2 katta blok)
## Topshiriq sharti:
Mozaika ichidagi bitta elementga ham 2 ustun, ham 2 satr kenglik bering.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid 2x2 Span</title>
  <style>
    .mosaic-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: repeat(2, 60px);
      gap: 8px;
      width: 260px;
      font-family: sans-serif;
    }
    .big-square {
      grid-column: span 2;
      grid-row: span 2;
      background: #7c3aed;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
      font-weight: bold;
    }
    .s-box { background: #cbd5e1; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="mosaic-grid">
    <div class="big-square">2x2 Katta Blok</div>
    <div class="s-box"></div>
    <div class="s-box"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-column: span 2; grid-row: span 2` elementni ikkala o'q bo'yicha 2 hissa kengaytirib, katta kvadrat hosil qiladi.

## Ishlash natijasi:
```text
Chapda binafsharang katta kvadrat, o'ngda esa ikkita kichikroq kulrang to'rtburchaklar.
```

---

# 741-Topshiriq: Gridda elementlarni teskari tartibda joylash (grid-column start)
## Topshiriq sharti:
HTML dagi 1-elementni 2-ustunga, 2-elementni esa 1-ustunga grid-column bilan ko'chiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Column Reorder</title>
  <style>
    .flip-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      font-family: sans-serif;
      width: 260px;
    }
    .box-a { grid-column: 2; background: #ef4444; color: white; padding: 12px; text-align: center; border-radius: 4px; }
    .box-b { grid-column: 1; background: #3b82f6; color: white; padding: 12px; text-align: center; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="flip-grid">
    <div class="box-a">A (HTML da birinchi, ekranda o'ngda)</div>
    <div class="box-b">B (HTML da ikkinchi, ekranda chapda)</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Grid chiziqlarini ko'rsatish orqali elementlarning ekrandagi o'rnini xohlagancha almashtirish mumkin.

## Ishlash natijasi:
```text
Chapda ko'k B bloki, o'ngda esa qizil A bloki ko'rinadi.
```

---

# 742-Topshiriq: Grid yordamida fayllar ro'yxati (Ikonka, Nomi, Hajmi, Harakat)
## Topshiriq sharti:
4 ustunli fayl menejeri jadvalini grid-template-columns bilan yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>File Manager Grid</title>
  <style>
    .file-row {
      display: grid;
      grid-template-columns: 30px 1fr 70px 40px;
      gap: 10px;
      align-items: center;
      width: 300px;
      padding: 8px;
      border-bottom: 1px solid #e2e8f0;
      font-family: sans-serif;
      font-size: 13px;
    }
  </style>
</head>
<body>
  <div class="file-row">
    <span>&#128196;</span>
    <strong>dars_01.pdf</strong>
    <span style="color:#64748b;">2.4 MB</span>
    <button style="border:none; background:none; cursor:pointer;">&#8942;</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`30px 1fr 70px 40px` ustunlari fayl ikonkasi, fayl nomi, hajmi va amallar menyusini toza tekislaydi.

## Ishlash natijasi:
```text
Hujjat ikonkasi, nomi, 2.4 MB hajmi va uch nuqta amallar tugmasi bir qatorda.
```

---

# 743-Topshiriq: Grid yordamida audio pleer ekvalayzeri (10 kanalli)
## Topshiriq sharti:
repeat(10, 1fr) yordamida audio spektr ko'rinishini hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Equalizer Spectrum</title>
  <style>
    .spectrum {
      display: grid;
      grid-template-columns: repeat(10, 1fr);
      gap: 3px;
      height: 60px;
      width: 200px;
      align-items: end;
      background: #0f172a;
      padding: 8px;
      border-radius: 6px;
    }
    .bar { background: #38bdf8; border-radius: 1px; }
  </style>
</head>
<body>
  <div class="spectrum">
    <div class="bar" style="height: 20px;"></div>
    <div class="bar" style="height: 40px;"></div>
    <div class="bar" style="height: 55px;"></div>
    <div class="bar" style="height: 35px;"></div>
    <div class="bar" style="height: 50px;"></div>
    <div class="bar" style="height: 30px;"></div>
    <div class="bar" style="height: 45px;"></div>
    <div class="bar" style="height: 25px;"></div>
    <div class="bar" style="height: 15px;"></div>
    <div class="bar" style="height: 5px;"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`align-items: end` va `repeat(10, 1fr)` ustunlari barlarni pastki chiziqdan boshlab ekvalayzer shaklida o'stiradi.

## Ishlash natijasi:
```text
Qora fonda 10 ta moviy audio spektr to'lqinlari.
```

---

# 744-Topshiriq: Grid yordamida ob-havo vidjeti (Bugun va haftalik prognoz)
## Topshiriq sharti:
Yuqorida bugungi harorat (katta), pastda 3 kunlik prognoz katakchalarini joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Weather Widget Grid</title>
  <style>
    .weather {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      width: 240px;
      background: #0284c7;
      color: white;
      padding: 16px;
      border-radius: 10px;
      font-family: sans-serif;
      text-align: center;
    }
    .today-box { grid-column: span 3; font-size: 28px; font-weight: bold; margin-bottom: 8px; }
    .forecast { background: rgba(255,255,255,0.15); padding: 6px; border-radius: 4px; font-size: 11px; }
  </style>
</head>
<body>
  <div class="weather">
    <div class="today-box">+24&deg;C Toshkent</div>
    <div class="forecast">Ertaga<br>+25&deg;</div>
    <div class="forecast">Indinga<br>+22&deg;</div>
    <div class="forecast">Yakshanba<br>+20&deg;</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`today-box` `span 3` bilan butun qatorni oladi, 3 kunlik prognoz esa ostida 3 ta teng katakchaga tushadi.

## Ishlash natijasi:
```text
To'q ko'k ob-havo kartasida yirik +24°C yozuvi va ostida 3 kunlik prognoz.
```

---

# 745-Topshiriq: Gridda satrlar bo'yicha teng oraliq qoldirish (grid-row offset)
## Topshiriq sharti:
1-satrda element, 2-satr bo'sh, 3-satrda keyingi element turishini grid-row bilan belgilang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Row Offset</title>
  <style>
    .gap-rows {
      display: grid;
      grid-template-rows: 40px 30px 40px;
      font-family: sans-serif;
      width: 240px;
    }
    .item-top { grid-row: 1; background: #10b981; color: white; padding: 10px; border-radius: 4px; }
    .item-bot { grid-row: 3; background: #6366f1; color: white; padding: 10px; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="gap-rows">
    <div class="item-top">Yuqori (1-satr)</div>
    <div class="item-bot">Quyi (3-satr, 2-satr bo'sh)</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
2-satrga hech qanday element qo'yilmaganligi sababli u tabiiy bo'sh masofa vazifasini bajaradi.

## Ishlash natijasi:
```text
Yashil blok va binafsharang blok orasida 30px li bo'shliq saqlanadi.
```

---

# 746-Topshiriq: Grid yordamida ikkita ustunli kontaktlar formasi
## Topshiriq sharti:
Ism, Email, Telefon va Xabar (butun qator) maydonlarini grid orqali tekislang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Contact Form Grid</title>
  <style>
    .contact-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      width: 300px;
      font-family: sans-serif;
    }
    .full-span { grid-column: span 2; }
    input, textarea { width: 100%; box-sizing: border-box; padding: 8px; border: 1px solid #cbd5e1; border-radius: 4px; }
  </style>
</head>
<body>
  <form class="contact-grid">
    <div><input type="text" placeholder="Ism"></div>
    <div><input type="email" placeholder="Email"></div>
    <div class="full-span"><textarea placeholder="Xabaringiz..." rows="3"></textarea></div>
  </form>
</body>
</html>
```

## Tushuntirish va Mantiq:
Birinchi ikkita maydon 1fr dan, textarea esa `span 2` orqali butun enni qamrab oladi.

## Ishlash natijasi:
```text
Tepada ikkita yonma-yon input, pastda esa keng xabar yozish maydoni.
```

---

# 747-Topshiriq: Gridda auto-fill bilan galereya kartalari va hover effekti
## Topshiriq sharti:
Kartalar ustiga kursor borganda biroz ko'tariluvchi auto-fill panjarasi hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Hover Cards Grid</title>
  <style>
    .hover-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
      gap: 10px;
      width: 260px;
      font-family: sans-serif;
    }
    .h-card {
      background: white;
      border: 1px solid #cbd5e1;
      padding: 14px;
      text-align: center;
      border-radius: 6px;
      transition: transform 0.2s, box-shadow 0.2s;
      cursor: pointer;
    }
    .h-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
  </style>
</head>
<body>
  <div class="hover-grid">
    <div class="h-card">1</div>
    <div class="h-card">2</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Grid maketi kartalarni tartib bilan ushlab turadi, CSS hover esa har bir katakka interaktivlik baxsh etadi.

## Ishlash natijasi:
```text
Ustiga sichqoncha borganda yuqoriga biroz ko'tarilib soya tashlaydigan oq kartalar.
```

---

# 748-Topshiriq: Grid yordamida kredit karta orqa va old tomoni maketi
## Topshiriq sharti:
Karta raqami (span 2), amal qilish muddati va CVV ni 2 ustunli gridda joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Credit Card Input Grid</title>
  <style>
    .card-form {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      width: 240px;
      font-family: sans-serif;
    }
    .card-full { grid-column: span 2; }
    input { width: 100%; box-sizing: border-box; padding: 8px; border: 1px solid #cbd5e1; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="card-form">
    <div class="card-full"><input type="text" placeholder="Karta raqami (16 ta son)"></div>
    <div><input type="text" placeholder="MM/YY"></div>
    <div><input type="text" placeholder="CVV"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Karta raqami 2 ustunni to'liq oladi, muddat va CVV esa pastdagi qatorda 50% dan taqsimlanadi.

## Ishlash natijasi:
```text
Bank kartasi to'lov ma'lumotlarini kiritishning qulay forma bloki.
```

---

# 749-Topshiriq: Grid-template-areas da sarlavha va ikki yonlama harakat paneli
## Topshiriq sharti:
Orqaga tugmasi (chapda), Sarlavha (o'rtada) va Qo'shish tugmasi (o'ngda) maydonlarini nomlangan zonalar orqali quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Header Areas Grid</title>
  <style>
    .mobile-header {
      display: grid;
      grid-template-columns: 40px 1fr 40px;
      grid-template-areas: "back title add";
      align-items: center;
      background: #0f172a;
      color: white;
      padding: 10px 14px;
      width: 280px;
      font-family: sans-serif;
    }
    .btn-back { grid-area: back; cursor: pointer; }
    .h-title { grid-area: title; text-align: center; font-weight: bold; }
    .btn-add { grid-area: add; text-align: right; cursor: pointer; }
  </style>
</head>
<body>
  <header class="mobile-header">
    <span class="btn-back">&larr;</span>
    <span class="h-title">Sozlamalar</span>
    <span class="btn-add">&#43;</span>
  </header>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-template-areas: 'back title add'` mobil header elementlarini aniq o'z joyiga qadab qo'yadi.

## Ishlash natijasi:
```text
Qora navigatsiya paneli: chapda orqaga strelka, markazda 'Sozlamalar' va o'ngda '+' belgisi.
```

---

# 750-Topshiriq: To'liq Bento Grid Portali: Mahsulot ekotizimi namoyishi
## Topshiriq sharti:
7 ta turli xil o'lchamdagi bento qutilarini CSS Grid murakkab joylashuvlari bilan yakunlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Ultimate Bento Portfolio</title>
  <style>
    .bento-master {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      grid-template-rows: 90px 90px;
      gap: 12px;
      width: 320px;
      font-family: sans-serif;
    }
    .b-cell {
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 10px;
      font-size: 11px;
    }
    .b-main { grid-column: span 2; grid-row: span 2; background: #2563eb; color: white; padding: 16px; border-radius: 8px; }
    .b-wide { grid-column: span 2; background: #f8fafc; }
  </style>
</head>
<body>
  <div class="bento-master">
    <div class="b-main">
      <h3 style="margin: 0 0 6px 0;">Bento Asosiy</h3>
      <p style="margin:0; font-size: 12px;">2x2 Katta maydon</p>
    </div>
    <div class="b-wide">Keng karta (span 2)</div>
    <div class="b-cell">Kichik 1</div>
    <div class="b-cell">Kichik 2</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Bento arxitekturasida `grid-column: span 2; grid-row: span 2` orqali asosiy diqqat markazi hosil qilinadi, qolgan sohalar esa kichikroq modullar bilan to'ldiriladi.

## Ishlash natijasi:
```text
Chapda ko'k katta kvadrat, o'ngda bitta cho'ziq to'rtburchak va ostida ikkita kichik oq kartalar mozaikasi.
```

---

