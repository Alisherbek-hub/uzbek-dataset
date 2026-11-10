# HTML va CSS: CSS Grid Asoslari va Shablonlar (Topshiriqlar 651 - 700)

# 651-Topshiriq: Display: grid konteyneri yaratish va 2D o'qlar tizimi
## Topshiriq sharti:
display: grid orqali ikki o'lchamli (satr va ustun) panjara hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>CSS Grid Asoslari</title>
  <style>
    .grid-container {
      display: grid;
      grid-template-columns: 120px 120px;
      grid-template-rows: 60px 60px;
      gap: 10px;
      background: #f1f5f9;
      padding: 16px;
      font-family: sans-serif;
      width: fit-content;
    }
    .grid-item {
      background: #2563eb;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="grid-container">
    <div class="grid-item">1</div>
    <div class="grid-item">2</div>
    <div class="grid-item">3</div>
    <div class="grid-item">4</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: grid` elementni ikki o'lchamli qolipga aylantiradi. `grid-template-columns` vertikal ustunlar kengligini, `grid-template-rows` esa gorizontal satrlar balandligini belgilaydi.

## Ishlash natijasi:
```text
2 ustun va 2 satrdan iborat 4 ta ko'k katakcha aniq panjara shaklida ko'rinadi.
```

---

# 652-Topshiriq: Fr (Fractional Unit) ulush birligining ishlash mexanizmi
## Topshiriq sharti:
Konteyner enini 1fr va 2fr nisbatida ikki qismga bo'luvchi grid yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>CSS Grid FR Unit</title>
  <style>
    .fr-grid {
      display: grid;
      grid-template-columns: 1fr 2fr;
      gap: 15px;
      background: #e2e8f0;
      padding: 16px;
      font-family: sans-serif;
    }
    .fr-item {
      padding: 20px;
      color: white;
      text-align: center;
      border-radius: 6px;
    }
    .col-a { background: #0d9488; }
    .col-b { background: #0f766e; }
  </style>
</head>
<body>
  <div class="fr-grid">
    <div class="fr-item col-a">1fr (33.3%)</div>
    <div class="fr-item col-b">2fr (66.6%)</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`fr` (fractional unit) mavjud erkin maydonning hissasini (ulushini) bildiradi. 1fr va 2fr umumiy 3 ulush degani bo'lib, birinchi ustun butun maydonning 1/3 qismini, ikkinchi ustun 2/3 qismini oladi.

## Ishlash natijasi:
```text
Ikkinchi to'q firuza ustun birinchisidan ikki barobar keng bo'lib yonma-yon turadi.
```

---

# 653-Topshiriq: Repeat() funksiyasi yordamida takrorlanuvchi ustunlar
## Topshiriq sharti:
repeat(3, 1fr) orqali 3 ta bir xil kenglikdagi ustunlar panjarasini hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>CSS Grid Repeat</title>
  <style>
    .repeat-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      font-family: sans-serif;
    }
    .box {
      background: #8b5cf6;
      color: white;
      padding: 20px;
      text-align: center;
      border-radius: 6px;
    }
  </style>
</head>
<body>
  <div class="repeat-grid">
    <div class="box">Ustun 1</div>
    <div class="box">Ustun 2</div>
    <div class="box">Ustun 3</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`repeat(3, 1fr)` ifodasi `1fr 1fr 1fr` deb yozishning qisqartmasidir. U kodni toza va o'qishli qiladi hamda ko'p ustunli jadvallar yaratishda xatoliklarni kamaytiradi.

## Ishlash natijasi:
```text
Uchta teng kenglikdagi binafsharang qutilar bitta qatorda tekis joylashadi.
```

---

# 654-Topshiriq: Minmax() funksiyasi bilan moslashuvchan chegaralar
## Topshiriq sharti:
Ustun kengligi kamida 150px bo'lsin, bo'sh joy qolsa 1fr gacha kengaysin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>CSS Grid MinMax</title>
  <style>
    .minmax-grid {
      display: grid;
      grid-template-columns: minmax(150px, 1fr) 2fr;
      gap: 14px;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      padding: 16px;
      font-family: sans-serif;
    }
    .box { padding: 16px; color: white; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="minmax-grid">
    <div class="box" style="background: #e11d48;">minmax(150px, 1fr)</div>
    <div class="box" style="background: #475569;">2fr</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`minmax(150px, 1fr)` funksiyasi ustunga eng kamida 150px kafolat beradi. Agar ekran toraysa u 150px dan kam bo'la olmaydi, kengayganda esa 1fr hissasiga qadar cho'ziladi.

## Ishlash natijasi:
```text
Qizil ustun minimal 150px dan pastga tushmaydi, kulrang ustun esa unga nisbatan 2 barobar keng maydonni oladi.
```

---

# 655-Topshiriq: Auto-fill vs Auto-fit (Dinamik responsive grid siri)
## Topshiriq sharti:
Auto-fit va minmax yordamida media queries yozmasdan avtomatik moslashuvchi kartalar panjarasini quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Auto-fit Responsive Grid</title>
  <style>
    .cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
      gap: 16px;
      font-family: sans-serif;
    }
    .card {
      background: #3b82f6;
      color: white;
      padding: 24px;
      border-radius: 8px;
      text-align: center;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="cards-grid">
    <div class="card">Karta 1</div>
    <div class="card">Karta 2</div>
    <div class="card">Karta 3</div>
    <div class="card">Karta 4</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`repeat(auto-fit, minmax(140px, 1fr))` zamonaviy CSS ning eng qudratli texnikasidir. Ekran o'lchamiga qarab qatordagi kartalar soni 4 ta, 3 ta, 2 ta yoki 1 taga avtomatik aylanadi va bo'shliq to'liq 1fr orqali to'ldiriladi.

## Ishlash natijasi:
```text
Keng oynada 4 ta karta bir qatorda turadi, oyna toraytirilganda avtomatik ravishda 2 tadan yoki 1 tadan qatorga o'tadi.
```

---

# 656-Topshiriq: Auto-fill xususiyatining auto-fit dan farqi
## Topshiriq sharti:
Auto-fill bo'sh ustunlar uchun joy ajratib qo'yishi va elementlarni cho'zmasligini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Auto-Fill Grid</title>
  <style>
    .fill-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
      gap: 10px;
      background: #fef3c7;
      padding: 14px;
      font-family: sans-serif;
    }
    .item {
      background: #d97706;
      color: white;
      padding: 16px;
      text-align: center;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="fill-grid">
    <div class="item">Element 1</div>
    <div class="item">Element 2</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`auto-fill` konteynerga sig'adigan barcha potentsial ustunlar o'rnini saqlab turadi (bo'sh qolsa ham). `auto-fit` esa bo'sh ustunlarni siqib yuborib, mavjud elementlarni butun eni bo'yicha cho'zadi.

## Ishlash natijasi:
```text
Ikkita to'q sariq element faqat o'zining minimal hajmini olib chapda turadi, qolgan soha kelajakdagi ustunlar uchun bo'sh turadi.
```

---

# 657-Topshiriq: Grid Gap (gap, row-gap, column-gap) imkoniyatlari
## Topshiriq sharti:
Satrlar orasiga 24px, ustunlar orasiga esa 12px oraliq qo'ying.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Gap</title>
  <style>
    .gap-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      row-gap: 24px;
      column-gap: 12px;
      background: #f0fdf4;
      padding: 16px;
      font-family: sans-serif;
    }
    .box {
      background: #16a34a;
      color: white;
      padding: 16px;
      text-align: center;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="gap-grid">
    <div class="box">1</div><div class="box">2</div><div class="box">3</div>
    <div class="box">4</div><div class="box">5</div><div class="box">6</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`row-gap: 24px` satrlar o'rtasida katta oraliq yaratadi, `column-gap: 12px` esa ustunlar orasiga nozik oraliq beradi. Shorthand: `gap: 24px 12px;`.

## Ishlash natijasi:
```text
6 ta yashil katakcha: qatorlar orasida 24px keng masofa, yonlarida esa 12px ixcham oraliq.
```

---

# 658-Topshiriq: Klassik 12 ustunli CSS Grid tizimi (12-Column Grid)
## Topshiriq sharti:
Veb freymvorklar (Bootstrap, Tailwind) asosini tashkil etuvchi 12 ustunli grid maketini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>12 Column Grid</title>
  <style>
    .twelve-grid {
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 8px;
      font-family: sans-serif;
    }
    .col-item {
      background: #cbd5e1;
      padding: 10px 0;
      text-align: center;
      font-size: 11px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="twelve-grid">
    <div class="col-item">1</div><div class="col-item">2</div>
    <div class="col-item">3</div><div class="col-item">4</div>
    <div class="col-item">5</div><div class="col-item">6</div>
    <div class="col-item">7</div><div class="col-item">8</div>
    <div class="col-item">9</div><div class="col-item">10</div>
    <div class="col-item">11</div><div class="col-item">12</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-template-columns: repeat(12, 1fr)` 12 ta teng bo'lak yaratadi. Bu istalgan nisbatdagi (masalan 4 va 8, 3 va 9, 6 va 6) ustunlarni hosil qilish uchun universal asosdir.

## Ishlash natijasi:
```text
Ekran bo'ylab 1 dan 12 gacha raqamlangan nozik kulrang ustunchalar tizmasi.
```

---

# 659-Topshiriq: Sidebar va Asosiy kontent shabloni (240px 1fr)
## Topshiriq sharti:
Chap ustun qat'iy 240px bo'lsin, o'ngdagi asosiy kontent esa qolgan butun bo'sh joyni egallasin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Sidebar Layout Grid</title>
  <style>
    .layout-grid {
      display: grid;
      grid-template-columns: 240px 1fr;
      gap: 20px;
      min-height: 200px;
      font-family: sans-serif;
    }
    aside {
      background: #1e293b;
      color: white;
      padding: 20px;
      border-radius: 8px;
    }
    main {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      padding: 20px;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <div class="layout-grid">
    <aside>
      <h3>Menyu</h3>
      <p>Yon panel (240px)</p>
    </aside>
    <main>
      <h2>Bosh Sahifa</h2>
      <p>Asosiy kontent 1fr bilan kengayadi.</p>
    </main>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-template-columns: 240px 1fr` yon menyuni qat'iy o'lchamda ushlab turadi, asosiy darchaga esa ekranning qolgan barcha kengligini moslashuvchan beradi.

## Ishlash natijasi:
```text
Chapda 240px li to'q ko'k yon panel, o'ngda esa oynaning qolgan qismini to'liq qoplagan ochiq kontent.
```

---

# 660-Topshiriq: Grid-auto-rows va kutilmagan elementlarning balandligi
## Topshiriq sharti:
Dinamik ravishda qo'shilgan yangi satrlar balandligi grid-auto-rows: 100px orqali boshqarilishini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Auto Rows</title>
  <style>
    .implicit-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      grid-auto-rows: 90px; /* Shablon belgilanmagan yangi satrlarga 90px beradi */
      gap: 12px;
      font-family: sans-serif;
    }
    .cell {
      background: #0284c7;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
    }
  </style>
</head>
<body>
  <div class="implicit-grid">
    <div class="cell">Katak 1</div>
    <div class="cell">Katak 2</div>
    <div class="cell">Katak 3 (avto satr)</div>
    <div class="cell">Katak 4 (avto satr)</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-template-rows` faqat oldindan ko'zda tutilgan satrlar uchun ishlaydi. Noaniq (implicit) ravishda paydo bo'ladigan qo'shimcha satrlar balandligini esa `grid-auto-rows` tartibga soladi.

## Ishlash natijasi:
```text
Har biri 90px balandlikka ega bo'lgan 4 ta ko'k rangli kataklar 2 satrga teriladi.
```

---

# 661-Topshiriq: Grid-auto-flow: column bilan elementlarni ustun bo'yicha to'ldirish
## Topshiriq sharti:
Sukut bo'yicha qatorlab emas, balki ustunma-ustun to'lib boruvchi grid hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Auto Flow Column</title>
  <style>
    .col-flow-grid {
      display: grid;
      grid-auto-flow: column;
      grid-template-rows: repeat(2, 60px);
      gap: 10px;
      background: #fef2f2;
      padding: 12px;
      font-family: sans-serif;
    }
    .box {
      background: #dc2626;
      color: white;
      padding: 10px 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="col-flow-grid">
    <div class="box">1</div>
    <div class="box">2</div>
    <div class="box">3</div>
    <div class="box">4</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-auto-flow: column` elementlarning joylashish oqimini o'zgartiradi: 1-element yuqori chapda, 2-element uning pastida (ustun to'lgach), 3-element ikkinchi ustun tepasida joylashadi.

## Ishlash natijasi:
```text
Katakchalar vertikal ustun bo'ylab 1, 2 va undan keyingi ustunda 3, 4 tartibida teriladi.
```

---

# 662-Topshiriq: Grid-auto-flow: dense va bo'shliqlarni zich to'ldirish (Masonry effekti)
## Topshiriq sharti:
Katta elementlardan keyin qolib ketgan teshiklarni kichik elementlar bilan avtomatik yopish uchun dense qo'llang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Dense Packing</title>
  <style>
    .dense-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-auto-flow: dense; /* Teshiklarni avtomatik to'ldiradi */
      gap: 10px;
      font-family: sans-serif;
    }
    .item { background: #3b82f6; color: white; padding: 16px; border-radius: 4px; text-align: center; }
    .wide { grid-column: span 2; background: #e11d48; }
  </style>
</head>
<body>
  <div class="dense-grid">
    <div class="item">1</div>
    <div class="item wide">2 (Keng)</div>
    <div class="item">3</div>
    <div class="item">4</div>
    <div class="item">5</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-auto-flow: dense` algoritmi agar biror katta element sababli orqada bo'sh katak qolib ketsa, keyingi kichikroq elementlarni orqaga qaytarib o'sha bo'shliqqa joylashtiradi.

## Ishlash natijasi:
```text
Gridda hech qanday bo'sh teshiklar qolmaydi, elementlar zich mozaika kabi joylashadi.
```

---

# 663-Topshiriq: Ustunlar va satrlarni nomlangan chiziqlar (Named Lines) bilan belgilash
## Topshiriq sharti:
Chiziqlarga nom berish orqali [main-start] va [main-end] oralig'ini qamrab oling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Named Grid Lines</title>
  <style>
    .named-grid {
      display: grid;
      grid-template-columns: [sidebar-start] 160px [sidebar-end content-start] 1fr [content-end];
      gap: 16px;
      font-family: sans-serif;
    }
    .side {
      grid-column: sidebar-start / sidebar-end;
      background: #0f172a;
      color: white;
      padding: 16px;
      border-radius: 6px;
    }
    .content {
      grid-column: content-start / content-end;
      background: #eff6ff;
      padding: 16px;
      border-radius: 6px;
    }
  </style>
</head>
<body>
  <div class="named-grid">
    <div class="side">Sidebar</div>
    <div class="content">Asosiy Kontent</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Grid chiziqlarini qavs ichida nomlash (`[sidebar-start]`, `[content-start]`) katta loyihalarda raqamlar o'rniga so'zlardan foydalanish imkonini beradi va kod o'qilishini yengillashtiradi.

## Ishlash natijasi:
```text
Nomlangan chiziqlar orqali aniq ajratilgan sidebar va asosiy maydon ko'rinadi.
```

---

# 664-Topshiriq: Grid konteynerida elementlarni tekislash (justify-items va align-items)
## Topshiriq sharti:
Barcha katakchalarning ichki elementlarini justify-items: center va align-items: center bilan markazlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Align and Justify Items</title>
  <style>
    .aligned-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      grid-template-rows: repeat(2, 100px);
      justify-items: center;
      align-items: center;
      background: #f1f5f9;
      gap: 10px;
      font-family: sans-serif;
    }
    .cell-box {
      background: #10b981;
      color: white;
      padding: 10px 18px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="aligned-grid">
    <div class="cell-box">Markaz 1</div>
    <div class="cell-box">Markaz 2</div>
    <div class="cell-box">Markaz 3</div>
    <div class="cell-box">Markaz 4</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`justify-items: center` (gorizontal) va `align-items: center` (vertikal) har bir katakchaning ichidagi elementni o'z katagining qoq o'rtasiga joylashtiradi.

## Ishlash natijasi:
```text
Har bir katak o'rtasida yashil nishonlar markazlashgan holda turadi.
```

---

# 665-Topshiriq: Grid butun panjarasini tekislash (justify-content va align-content)
## Topshiriq sharti:
Umumiy grid o'lchami ota elementdan kichik bo'lganda butun panjarani markazga to'plang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Content Alignment</title>
  <style>
    .stage-grid {
      display: grid;
      grid-template-columns: repeat(2, 80px);
      grid-template-rows: repeat(2, 60px);
      justify-content: center;
      align-content: center;
      height: 200px;
      background: #e0e7ff;
      gap: 10px;
      border-radius: 8px;
      font-family: sans-serif;
    }
    .box { background: #4338ca; color: white; display: flex; align-items: center; justify-content: center; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="stage-grid">
    <div class="box">1</div>
    <div class="box">2</div>
    <div class="box">3</div>
    <div class="box">4</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`justify-content: center` va `align-content: center` butun panjaraning o'zini ota konteyner ichida ikkala o'q bo'yicha markazlashtiradi.

## Ishlash natijasi:
```text
200px li katta maydonning qoq o'rtasida ixchamgina 4 ta to'q binafsha katakchalar to'dasi ko'rinadi.
```

---

# 666-Topshiriq: Fotogalereya mozaikasi (CSS Grid Photo Gallery)
## Topshiriq sharti:
3 ustunli chiroyli fotogalereya panjarasini gap va rasmlar uchun aspect-ratio bilan tuzing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Photo Gallery Grid</title>
  <style>
    .gallery {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      width: 320px;
      font-family: sans-serif;
    }
    .photo-slot {
      aspect-ratio: 1 / 1;
      background: #94a3b8;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="gallery">
    <div class="photo-slot">1</div><div class="photo-slot">2</div><div class="photo-slot">3</div>
    <div class="photo-slot">4</div><div class="photo-slot">5</div><div class="photo-slot">6</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`aspect-ratio: 1 / 1` har bir rasm uyasining mukammal kvadrat bo'lishini ta'minlaydi, `repeat(3, 1fr)` esa 3 ustunga bo'ladi.

## Ishlash natijasi:
```text
3x2 formatdagi 6 ta kvadrat kulrang surat uyalari panjarasi.
```

---

# 667-Topshiriq: Grid-template-columns da foiz va pikselni aralashtirish
## Topshiriq sharti:
150px qat'iy o'lcham va 1fr ulushli ustunlarni uyg'unlashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Mixed Units Grid</title>
  <style>
    .mixed-grid {
      display: grid;
      grid-template-columns: 150px 1fr 100px;
      gap: 10px;
      font-family: sans-serif;
    }
    .box { padding: 12px; color: white; border-radius: 4px; text-align: center; }
  </style>
</head>
<body>
  <div class="mixed-grid">
    <div class="box" style="background:#0284c7;">150px</div>
    <div class="box" style="background:#0369a1;">1fr (Erkin maydon)</div>
    <div class="box" style="background:#075985;">100px</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
CSS Grid piksel (`px`), ulush (`fr`), foiz (`%`) va `auto` birliklarini bitta shablonda aralashtirib ishlatish imkonini beradi.

## Ishlash natijasi:
```text
Chetki ikki blok o'zgarmas piksel o'lchamda turadi, markaziy blok esa oynaning qolgan kengligiga moslashadi.
```

---

# 668-Topshiriq: Fit-content() funksiyasi bilan kontentga moslashuvchi ustun
## Topshiriq sharti:
Ustun kengligi kontent hajmiga mos bo'lsin, lekin 200px dan oshmasin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Fit-Content Grid</title>
  <style>
    .fit-grid {
      display: grid;
      grid-template-columns: fit-content(200px) 1fr;
      gap: 16px;
      font-family: sans-serif;
    }
    .fit-box { background: #f59e0b; color: white; padding: 12px; border-radius: 4px; }
    .grow-box { background: #64748b; color: white; padding: 12px; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="fit-grid">
    <div class="fit-box">Qisqa matn</div>
    <div class="grow-box">Qolgan butun maydon</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`fit-content(200px)` element o'z ichidagi matn qanchalik qisqa bo'lsa shuncha torayadi, lekin matn uzayganda ham 200px dan oshmaydi.

## Ishlash natijasi:
```text
Sariq quti faqat o'z matnining kengligini oladi, kulrang quti esa qolgan butun enni qoplaydi.
```

---

# 669-Topshiriq: Statistika ko'rsatkichlari kartalari panjarasi (Dashboard KPI Grid)
## Topshiriq sharti:
4 ta asosiy biznes ko'rsatkichlarini 4 ustunli gridda joylashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>KPI Grid</title>
  <style>
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      font-family: sans-serif;
    }
    .kpi-card {
      background: white;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 16px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .kpi-title { font-size: 12px; color: #64748b; margin-bottom: 6px; }
    .kpi-value { font-size: 20px; font-weight: bold; color: #0f172a; }
  </style>
</head>
<body>
  <div class="kpi-grid">
    <div class="kpi-card"><div class="kpi-title">Daromad</div><div class="kpi-value">$24,500</div></div>
    <div class="kpi-card"><div class="kpi-title">Foydalanuvchilar</div><div class="kpi-value">1,240</div></div>
    <div class="kpi-card"><div class="kpi-title">Buyurtmalar</div><div class="kpi-value">385</div></div>
    <div class="kpi-card"><div class="kpi-title">Konversiya</div><div class="kpi-value">4.8%</div></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-template-columns: repeat(4, 1fr)` orqali 4 ta karta har biri 25% dan teng kenglikka ega bo'ladi.

## Ishlash natijasi:
```text
Bir qatorda 4 ta oq rangli chiroyli statistika kartochkalari aks etadi.
```

---

# 670-Topshiriq: Subgrid asoslari haqida tushuncha
## Topshiriq sharti:
Ichki bolalar ham ota grid ustunlariga mos tushishi uchun subgrid konsepsiyasini namoyish eting.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Subgrid Konsepsiyasi</title>
  <style>
    .parent-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      font-family: sans-serif;
    }
    .nested-card {
      grid-column: span 3;
      display: grid;
      grid-template-columns: subgrid; /* Ota elementning 3 ta ustuniga to'liq moslashadi */
      background: #eff6ff;
      padding: 10px;
      border-radius: 6px;
    }
    .sub-item { background: #3b82f6; color: white; padding: 10px; text-align: center; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="parent-grid">
    <div class="nested-card">
      <div class="sub-item">Sub 1</div>
      <div class="sub-item">Sub 2</div>
      <div class="sub-item">Sub 3</div>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-template-columns: subgrid` ichki grid bolalariga ota gridning chiziqlari va o'lchamlarini to'g'ridan-to'g'ri meros qilib olish imkonini beradi.

## Ishlash natijasi:
```text
Ichki kartaning 3 ta elementi ota elementning 3 ta ustuniga to'liq mos ravishda teriladi.
```

---

# 671-Topshiriq: Taqvim (Calendar) oy ko'rinishi panjarasi
## Topshiriq sharti:
Haftaning 7 kuni uchun repeat(7, 1fr) yordamida taqvim panjarasini quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Calendar Grid</title>
  <style>
    .calendar {
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 6px;
      width: 320px;
      font-family: sans-serif;
      text-align: center;
    }
    .day-head { font-weight: bold; font-size: 12px; color: #64748b; padding: 6px 0; }
    .day-num { background: #f1f5f9; padding: 10px 0; border-radius: 4px; font-size: 13px; }
    .today { background: #2563eb; color: white; font-weight: bold; }
  </style>
</head>
<body>
  <div class="calendar">
    <div class="day-head">Du</div><div class="day-head">Se</div><div class="day-head">Ch</div>
    <div class="day-head">Pa</div><div class="day-head">Ju</div><div class="day-head">Sh</div><div class="day-head">Ya</div>
    <div class="day-num">1</div><div class="day-num">2</div><div class="day-num today">3</div>
    <div class="day-num">4</div><div class="day-num">5</div><div class="day-num">6</div><div class="day-num">7</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-template-columns: repeat(7, 1fr)` orqali haftaning 7 kuni mukammal taqsimlanadi va sanalar avtomatik yangi satrlarga tushadi.

## Ishlash natijasi:
```text
Hafta kunlari sarlavhasi va ostida 7 ta teng katakchada sanalar aks etgan ixcham taqvim.
```

---

# 672-Topshiriq: Mahsulotlar katalogi (E-Commerce Product Grid)
## Topshiriq sharti:
3 ustunli mahsulotlar ro'yxatini kartalar va narxlar bilan shakllantiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Product Catalog Grid</title>
  <style>
    .catalog {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      font-family: sans-serif;
    }
    .prod {
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 12px;
      text-align: center;
    }
    .prod-pic { height: 80px; background: #e2e8f0; border-radius: 4px; margin-bottom: 8px; }
  </style>
</head>
<body>
  <div class="catalog">
    <div class="prod"><div class="prod-pic"></div><strong>Noutbuk</strong></div>
    <div class="prod"><div class="prod-pic"></div><strong>Smartfon</strong></div>
    <div class="prod"><div class="prod-pic"></div><strong>Planshet</strong></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Grid yordamida e-tijorat do'konidagi tovarlar bir xil balandlik va kenglikdagi tartibli panjaraga oson joylashadi.

## Ishlash natijasi:
```text
Bir xil o'lchamdagi 3 ta tovar kartasi bitta gorizontal chiziqda turadi.
```

---

# 673-Topshiriq: Grid-template-rows bilan qat'iy sarlavha va elastik kontent
## Topshiriq sharti:
Balandligi 300px bo'lgan konteynerda sarlavha 50px, qolgan soha 1fr bo'lsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Rows Fixed and Fr</title>
  <style>
    .app-window {
      display: grid;
      grid-template-rows: 50px 1fr;
      height: 220px;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      overflow: hidden;
      font-family: sans-serif;
    }
    .app-header { background: #1e293b; color: white; display: flex; align-items: center; padding: 0 16px; }
    .app-main { background: #f8fafc; padding: 16px; overflow-y: auto; }
  </style>
</head>
<body>
  <div class="app-window">
    <div class="app-header">Ilova Sarlavhasi (50px)</div>
    <div class="app-main">Asosiy ish maydoni (1fr balandlikka cho'ziladi).</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-template-rows: 50px 1fr` tepadagi panelni qat'iy 50px da ushlaydi, pastki qism esa qolgan balandlikni to'liq qamrab oladi.

## Ishlash natijasi:
```text
Tepada qora 50px li qotirilgan sarlavha, pastda esa oqish ish maydoni.
```

---

# 674-Topshiriq: Grid-template-columns: min-content va max-content farqi
## Topshiriq sharti:
Ustun kengligini eng uzun so'z (min-content) va butun gap (max-content) bo'yicha moslang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Min-Content vs Max-Content</title>
  <style>
    .content-grid {
      display: grid;
      grid-template-columns: min-content max-content;
      gap: 16px;
      background: #f1f5f9;
      padding: 14px;
      font-family: sans-serif;
    }
    .box { background: #0284c7; color: white; padding: 10px; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="content-grid">
    <div class="box">EngUzunSozBuYerda va boshqa so'zlar</div>
    <div class="box">Ushbu gap qatorga buzilmasdan to'liq cho'ziladi</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`min-content` ustunni ichidagi eng uzun so'z o'lchamigacha toraytiradi. `max-content` esa matnni yangi qatorga tushirmasdan butun gap uzunligicha kengaytiradi.

## Ishlash natijasi:
```text
Birinchi quti so'z sig'adigan eng tor hajmda, ikkinchi quti esa gap bo'yicha cho'zilgan holda aks etadi.
```

---

# 675-Topshiriq: Grid yordamida kalkulyator tugmalari panjarasi
## Topshiriq sharti:
4x4 o'lchamli kalkulyator tugmalari panjarasini repeat(4, 1fr) bilan quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Calculator Grid</title>
  <style>
    .calc-pad {
      display: grid;
      grid-template-columns: repeat(4, 50px);
      grid-template-rows: repeat(4, 50px);
      gap: 8px;
      background: #0f172a;
      padding: 12px;
      border-radius: 8px;
      width: fit-content;
      font-family: sans-serif;
    }
    .key {
      background: #334155;
      color: white;
      border: none;
      border-radius: 6px;
      font-size: 16px;
      cursor: pointer;
    }
    .key-op { background: #f97316; }
  </style>
</head>
<body>
  <div class="calc-pad">
    <button class="key">7</button><button class="key">8</button><button class="key">9</button><button class="key key-op">/</button>
    <button class="key">4</button><button class="key">5</button><button class="key">6</button><button class="key key-op">*</button>
    <button class="key">1</button><button class="key">2</button><button class="key">3</button><button class="key key-op">-</button>
    <button class="key">0</button><button class="key">.</button><button class="key key-op">=</button><button class="key key-op">+</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-template-columns: repeat(4, 50px)` va `grid-template-rows: repeat(4, 50px)` yordamida kalkulyator tugmalari mukammal 4x4 panjaraga teriladi.

## Ishlash natijasi:
```text
Qora fonda to'q kulrang raqamlar va to'q sariq amallar tugmalaridan iborat kalkulyator klaviaturasi.
```

---

# 676-Topshiriq: Grid elementini o'z katagi ichida alohida tekislash (justify-self / align-self)
## Topshiriq sharti:
Faqat bitta katakcha elementini katagining o'ng quyi burchagiga joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Self Alignment</title>
  <style>
    .grid-box {
      display: grid;
      grid-template-columns: 140px 140px;
      grid-template-rows: 100px;
      gap: 10px;
      background: #e2e8f0;
      padding: 10px;
      font-family: sans-serif;
    }
    .cell-normal { background: #64748b; color: white; border-radius: 4px; padding: 10px; }
    .cell-corner {
      justify-self: end;
      align-self: end;
      background: #ef4444;
      color: white;
      padding: 6px 12px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="grid-box">
    <div class="cell-normal">Standart (cho'zilgan)</div>
    <div class="cell-corner">Burchakda</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`justify-self: end` elementni o'z katagining o'ng chetiga, `align-self: end` esa pastki poliga suradi.

## Ishlash natijasi:
```text
Kulrang quti butun katakni egallaydi, qizil element esa o'z katagining pastki o'ng burchagida ixchamgina turadi.
```

---

# 677-Topshiriq: Auto-fit bilan dinamik o'lchamdagi blog postlari ro'yxati
## Topshiriq sharti:
Kartalar eni 200px dan kam bo'lmagan holda ekranga qarab avtomatik qatorlarga ajralsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Blog Posts Auto-Fit</title>
  <style>
    .posts-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      font-family: sans-serif;
    }
    .post-card {
      background: white;
      border: 1px solid #cbd5e1;
      padding: 16px;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <div class="posts-grid">
    <div class="post-card"><h4>Post 1</h4><p>Qisqa tavsif.</p></div>
    <div class="post-card"><h4>Post 2</h4><p>Qisqa tavsif.</p></div>
    <div class="post-card"><h4>Post 3</h4><p>Qisqa tavsif.</p></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`repeat(auto-fit, minmax(200px, 1fr))` har doim elementlarni konteynerga moslaydi, ortiqcha bo'shliq qoldirmaydi.

## Ishlash natijasi:
```text
Keng ekranda 3 ta, o'rtacha ekranda 2 ta, kichik ekranda 1 ta ustun bo'lib o'zgaruvchi blog kartalari.
```

---

# 678-Topshiriq: Grid yordamida forma maydonlarini 2 ustunga taqsimlash
## Topshiriq sharti:
Ism va familiya yonma-yon, manzil esa ikkala ustunni egallaydigan forma quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Form Grid</title>
  <style>
    .form-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      width: 320px;
      font-family: sans-serif;
    }
    .full-width { grid-column: span 2; }
    input { width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #cbd5e1; border-radius: 4px; }
  </style>
</head>
<body>
  <form class="form-grid">
    <div><input type="text" placeholder="Ism"></div>
    <div><input type="text" placeholder="Familiya"></div>
    <div class="full-width"><input type="text" placeholder="To'liq manzil"></div>
  </form>
</body>
</html>
```

## Tushuntirish va Mantiq:
Birinchi ikkita input 1fr dan teng en oladi, uchinchi input esa `grid-column: span 2` orqali butun qatorni qoplaydi.

## Ishlash natijasi:
```text
Tepadagi ikkita input yonma-yon, pastdagi manzil kiritish maydoni esa keng bo'lib turadi.
```

---

# 679-Topshiriq: Grid-auto-columns bilan gorizontal skroll panjarasi
## Topshiriq sharti:
grid-auto-flow: column va grid-auto-columns: 140px orqali gorizontal kartalar lentasini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Horizontal Scroll Grid</title>
  <style>
    .h-grid {
      display: grid;
      grid-auto-flow: column;
      grid-auto-columns: 140px;
      gap: 12px;
      overflow-x: auto;
      padding: 10px;
      background: #f8fafc;
      font-family: sans-serif;
    }
    .h-card {
      background: #0284c7;
      color: white;
      padding: 20px;
      border-radius: 6px;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="h-grid">
    <div class="h-card">Karta A</div>
    <div class="h-card">Karta B</div>
    <div class="h-card">Karta C</div>
    <div class="h-card">Karta D</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-auto-flow: column` yangi elementlarni gorizontal ravishda yangi ustunlarga qo'shadi, `grid-auto-columns: 140px` esa ularning enini belgilaydi.

## Ishlash natijasi:
```text
O'ngga qarab skroll bo'ladigan 140px kenglikdagi to'rtta moviy karta zanjiri.
```

---

# 680-Topshiriq: Grid yordamida qavatma-qavat joylashuv (Stacking Items without Absolute)
## Topshiriq sharti:
Position: absolute ishlatmasdan, bitta grid katagi ustiga rasm va matnni ustma-ust qo'ying.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Item Stacking</title>
  <style>
    .stack-grid {
      display: grid;
      width: 260px;
      height: 160px;
      border-radius: 8px;
      overflow: hidden;
      font-family: sans-serif;
    }
    .layer-bg {
      grid-area: 1 / 1;
      background: #3b82f6;
    }
    .layer-text {
      grid-area: 1 / 1;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: bold;
      z-index: 1;
    }
  </style>
</head>
<body>
  <div class="stack-grid">
    <div class="layer-bg"></div>
    <div class="layer-text">Grid orqali qoplangan matn</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ikkala elementga ham bir xil `grid-area: 1 / 1` (1-satr, 1-ustun) berilsa, ular bir-birining ustiga tushadi. Bu mutlaq joylashtirish (`absolute`) o'rniga eng toza zamonaviy yechimdir.

## Ishlash natijasi:
```text
Ko'k fon ustida qoq markazda turgan oq rangli sarlavha.
```

---

# 681-Topshiriq: Responsive narxlar taqqoslash jadvali (3 ustunli)
## Topshiriq sharti:
Bepul, Standart va Premium tariflarini 3 ustunli grid panjarasida taqdim eting.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Pricing Grid</title>
  <style>
    .pricing-table {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      font-family: sans-serif;
    }
    .plan {
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 18px;
      text-align: center;
    }
    .plan.pro { border-color: #2563eb; background: #eff6ff; }
  </style>
</head>
<body>
  <div class="pricing-table">
    <div class="plan"><h4>Oddiy</h4><h2>$0</h2></div>
    <div class="plan pro"><h4>Pro</h4><h2>$29</h2></div>
    <div class="plan"><h4>Kompaniya</h4><h2>$99</h2></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-template-columns: repeat(3, 1fr)` tarif rejalarini bir tekisda taqsimlaydi, `pro` klassi esa markaziy rejani ko'k tusda ajratib ko'rsatadi.

## Ishlash natijasi:
```text
3 ta yonma-yon tarif kartasi, o'rtadagisi ochiq ko'k tusda.
```

---

# 682-Topshiriq: Grid yordamida ikonkalar va sarlavhalar ro'yxati (Icon List Grid)
## Topshiriq sharti:
Chapda 40px li ikonka ustuni, o'ngda esa 1fr li matn ustunini grid qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Icon List Grid</title>
  <style>
    .feature-row {
      display: grid;
      grid-template-columns: 40px 1fr;
      gap: 12px;
      align-items: center;
      width: 280px;
      font-family: sans-serif;
      margin-bottom: 12px;
    }
    .icon-box {
      width: 40px;
      height: 40px;
      background: #10b981;
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  </style>
</head>
<body>
  <div class="feature-row">
    <div class="icon-box">&#10003;</div>
    <div><strong>Tezkor yetkazish</strong><br><small style="color:#64748b;">24 soat ichida</small></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-template-columns: 40px 1fr` ikonka doirasi uchun aniq o'lcham va matn uchun moslashuvchan maydon yaratadi.

## Ishlash natijasi:
```text
Yashil dumaloq belgi va uning o'ng tomonida sarlavha hamda izoh matni.
```

---

# 683-Topshiriq: Grid gap o'rniga ichki chiziqli jadval effekti (1px Gap Table)
## Topshiriq sharti:
Orqa fonga to'q rang berib, gap: 1px orqali kataklar orasida nozik chegara chiziqlari hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>1px Gap Table</title>
  <style>
    .grid-table {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1px;
      background: #cbd5e1; /* Ushbu fon chiziq vazifasini o'taydi */
      border: 1px solid #cbd5e1;
      font-family: sans-serif;
      width: 300px;
    }
    .t-cell {
      background: white;
      padding: 10px;
      text-align: center;
    }
    .t-head { background: #f1f5f9; font-weight: bold; }
  </style>
</head>
<body>
  <div class="grid-table">
    <div class="t-cell t-head">№</div><div class="t-cell t-head">Ism</div><div class="t-cell t-head">Ball</div>
    <div class="t-cell">1</div><div class="t-cell">Ali</div><div class="t-cell">95</div>
    <div class="t-cell">2</div><div class="t-cell">Vali</div><div class="t-cell">88</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ota foni to'q kulrang qilinib `gap: 1px` berilsa va ichki kataklar oq fonli qilinsa, 1px li mukammal toza panjara chiziqlari hosil bo'ladi.

## Ishlash natijasi:
```text
Nozik 1px li toza ichki chiziqlarga ega bo'lgan zamonaviy jadval.
```

---

# 684-Topshiriq: Auto-fit orqali mahsulot filtr chiplari panjarasi
## Topshiriq sharti:
Kamida 90px li filtr chiplarini avtomatik qatorlarga taxlovchi grid yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Chips Grid</title>
  <style>
    .chips-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(90px, 1fr));
      gap: 8px;
      width: 300px;
      font-family: sans-serif;
    }
    .chip {
      background: #e0e7ff;
      color: #3730a3;
      padding: 8px 12px;
      text-align: center;
      border-radius: 4px;
      font-size: 13px;
    }
  </style>
</head>
<body>
  <div class="chips-grid">
    <div class="chip">Hammasi</div>
    <div class="chip">Yangilar</div>
    <div class="chip">Ommabop</div>
    <div class="chip">Arzon</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`minmax(90px, 1fr)` bilan chiplar 300px kenglikda bir qatorga 3 tadan sig'ib, qolgani keyingi satrga tushadi.

## Ishlash natijasi:
```text
Och binafsharang to'rtburchak chiplar tartibli panjara bo'lib turadi.
```

---

# 685-Topshiriq: Grid-template-columns: repeat(auto-fill, 80px) belgilangan o'lcham
## Topshiriq sharti:
Kataklar kengaymasdan faqat qat'iy 80px bo'lib qoluvchi auto-fill panjarasi yasang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Auto-Fill Fixed Size</title>
  <style>
    .icons-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, 80px);
      gap: 10px;
      background: #f8fafc;
      padding: 10px;
      font-family: sans-serif;
    }
    .icon-box {
      width: 80px;
      height: 80px;
      background: #f43f5e;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <div class="icons-grid">
    <div class="icon-box">1</div>
    <div class="icon-box">2</div>
    <div class="icon-box">3</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`repeat(auto-fill, 80px)` kataklarni 80px o'lchamda ushlab turadi, ortiqcha bo'shliq qolsa ham ularni cho'zib yubormaydi.

## Ishlash natijasi:
```text
Aniq 80x80px kvadrat qizil katakchalar qatorda turadi.
```

---

# 686-Topshiriq: Grid va Flexboxni birgalikda ishlatish (Karta ichida Flex)
## Topshiriq sharti:
Tashqi sahifani Grid panjarasida, har bir karta ichidagi elementlarni esa Flexbox bilan tekislang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid + Flexbox</title>
  <style>
    .outer-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
      font-family: sans-serif;
    }
    .inner-flex-card {
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  </style>
</head>
<body>
  <div class="outer-grid">
    <div class="inner-flex-card">
      <span>Dars 1</span>
      <button style="background: #2563eb; color: white; border: none; padding: 4px 8px; border-radius: 4px;">Boshlash</button>
    </div>
    <div class="inner-flex-card">
      <span>Dars 2</span>
      <button style="background: #2563eb; color: white; border: none; padding: 4px 8px; border-radius: 4px;">Boshlash</button>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Professional veb-dasturlashda sahifaning umumiy 2D karkasi CSS Grid orqali, kartalar ichidagi 1D yo'nalishli elementlar esa Flexbox orqali boshqariladi.

## Ishlash natijasi:
```text
2 ustunli grid ichidagi har bir kartada matn chapda, ko'k tugma esa o'ngda turadi.
```

---

# 687-Topshiriq: Grid yordamida vertikal matn va rasm juftligi
## Topshiriq sharti:
Har bir katakda rasm tepada, sarlavha va matn pastda bo'lgan 2 ustunli qolip tuzing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Media Cards Grid</title>
  <style>
    .media-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      font-family: sans-serif;
      width: 320px;
    }
    .media-card {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      overflow: hidden;
    }
    .media-thumb { height: 70px; background: #64748b; }
    .media-desc { padding: 10px; }
  </style>
</head>
<body>
  <div class="media-grid">
    <div class="media-card">
      <div class="media-thumb"></div>
      <div class="media-desc"><strong>Kurs A</strong></div>
    </div>
    <div class="media-card">
      <div class="media-thumb"></div>
      <div class="media-desc"><strong>Kurs B</strong></div>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Grid maketi har bir kartaga teng kenglik beradi va ularning ichki qismlari tartibli namoyon bo'ladi.

## Ishlash natijasi:
```text
Yonma-yon turgan ikkita media kartochkasi.
```

---

# 688-Topshiriq: Grid-template-rows da auto va minmax() uyg'unligi
## Topshiriq sharti:
Sarlavha auto balandlikda, asosiy maydon minmax(120px, 1fr) bo'lsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Grid Rows Auto Minmax</title>
  <style>
    .panel-grid {
      display: grid;
      grid-template-rows: auto minmax(120px, 1fr);
      height: 200px;
      border: 1px solid #cbd5e1;
      font-family: sans-serif;
    }
    .panel-top { background: #f1f5f9; padding: 12px; font-weight: bold; }
    .panel-content { background: white; padding: 12px; }
  </style>
</head>
<body>
  <div class="panel-grid">
    <div class="panel-top">Panel Sarlavhasi (auto)</div>
    <div class="panel-content">Kontent maydoni kamida 120px.</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`auto` satr balandligini matn sig'ishi uchun kerakli miqdorda oladi, `minmax(120px, 1fr)` esa qolgan balandlikni to'ldiradi.

## Ishlash natijasi:
```text
Yuqori sarlavha o'z hajmida, pastki qismi esa 120px dan kam bo'lmagan keng maydonda turadi.
```

---

# 689-Topshiriq: Grid yordamida moslashuvchan ko'rsatkichlar to'plami (Metrics Matrix)
## Topshiriq sharti:
3x2 o'lchamli 6 ta statistik ko'rsatkichni gridda tekis joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Metrics Matrix</title>
  <style>
    .matrix {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      font-family: sans-serif;
    }
    .cell {
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      padding: 12px;
      text-align: center;
      border-radius: 6px;
    }
    .c-val { font-size: 18px; font-weight: bold; color: #1e40af; }
    .c-lbl { font-size: 11px; color: #64748b; }
  </style>
</head>
<body>
  <div class="matrix">
    <div class="cell"><div class="c-val">99.9%</div><div class="c-lbl">Uptime</div></div>
    <div class="cell"><div class="c-val">12ms</div><div class="c-lbl">Latency</div></div>
    <div class="cell"><div class="c-val">4.5k</div><div class="c-lbl">Req/s</div></div>
    <div class="cell"><div class="c-val">0.01%</div><div class="c-lbl">Errors</div></div>
    <div class="cell"><div class="c-val">128GB</div><div class="c-lbl">RAM</div></div>
    <div class="cell"><div class="c-val">24 Core</div><div class="c-lbl">CPU</div></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`repeat(3, 1fr)` va 6 ta element avtomatik 2 ta qatorga teng bo'linib 3x2 matritsa hosil qiladi.

## Ishlash natijasi:
```text
Moviy hoshiyali 6 ta server ko'rsatkichi 2 satr va 3 ustunda simmetrik aks etadi.
```

---

# 690-Topshiriq: Grid gap xususiyatini o'chirish (Border Collapse effekti)
## Topshiriq sharti:
gap: 0 qilib bir-biriga yopishgan 4 ta rangli blok hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Zero Gap Grid</title>
  <style>
    .zero-gap {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0;
      width: 200px;
      height: 120px;
      font-family: sans-serif;
    }
    .b1 { background: #ef4444; color: white; display: flex; align-items: center; justify-content: center; }
    .b2 { background: #3b82f6; color: white; display: flex; align-items: center; justify-content: center; }
    .b3 { background: #10b981; color: white; display: flex; align-items: center; justify-content: center; }
    .b4 { background: #f59e0b; color: white; display: flex; align-items: center; justify-content: center; }
  </style>
</head>
<body>
  <div class="zero-gap">
    <div class="b1">1</div>
    <div class="b2">2</div>
    <div class="b3">3</div>
    <div class="b4">4</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`gap: 0` bilan barcha kataklar bir-biriga zich yopishadi va yaxlit to'rtburchak bayroqsimon mozaika hosil qiladi.

## Ishlash natijasi:
```text
O'rtasida oraliqsiz 4 xil rangli kataklar bitta 200x120px to'rtburchak hosil qiladi.
```

---

# 691-Topshiriq: Grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)) mobil ko'rinish
## Topshiriq sharti:
Kichik ekranda avtomatik bitta ustunga aylanuvchi grid namunasini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Mobile Responsive Auto-Fit</title>
  <style>
    .adaptive-wrap {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
      gap: 10px;
      width: 240px; /* Tor mobil ekran simulyatsiyasi */
      font-family: sans-serif;
    }
    .box {
      background: #7c3aed;
      color: white;
      padding: 14px;
      text-align: center;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="adaptive-wrap">
    <div class="box">Modul 1</div>
    <div class="box">Modul 2</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
240px kenglikda har bir element 110px minmax sababli 2 ta ustun bo'lib sig'adi, agar kenglik 200px ga tushsa avtomatik 1 ta ustun bo'ladi.

## Ishlash natijasi:
```text
Binafsharang ikkita quti 240px kenglikda yonma-yon turadi.
```

---

# 692-Topshiriq: Gridda qatorlar bo'yicha markazlashtirish (Place-items shorthand)
## Topshiriq sharti:
justify-items va align-items o'rniga bitta `place-items: center` shorthandini qo'llang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Place Items Shorthand</title>
  <style>
    .place-grid {
      display: grid;
      place-items: center; /* Ikkala o'q bo'yicha markazlaydi */
      height: 140px;
      background: #f1f5f9;
      border-radius: 8px;
      font-family: sans-serif;
    }
    .badge {
      background: #0284c7;
      color: white;
      padding: 10px 20px;
      border-radius: 20px;
    }
  </style>
</head>
<body>
  <div class="place-grid">
    <div class="badge">Place Items Center</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`place-items: center` xususiyati `align-items: center` va `justify-items: center` larni birlashtiruvchi zamonaviy CSS shorthandidir.

## Ishlash natijasi:
```text
Kulrang maydon markazida bitta ko'k dumaloq nishon turadi.
```

---

# 693-Topshiriq: Grid yordamida vertikal Timeline (Vaqt chizig'i) arxitekturasi
## Topshiriq sharti:
Chapda sana, o'rtada chiziq va o'ngda voqea matni bo'lgan 3 ustunli timeline quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Timeline Grid</title>
  <style>
    .timeline {
      display: grid;
      grid-template-columns: 80px 20px 1fr;
      gap: 12px;
      align-items: center;
      font-family: sans-serif;
      width: 320px;
    }
    .date { text-align: right; font-size: 12px; color: #64748b; font-weight: bold; }
    .dot { width: 12px; height: 12px; background: #2563eb; border-radius: 50%; justify-self: center; }
    .event { background: #f8fafc; padding: 10px; border-radius: 6px; border: 1px solid #e2e8f0; }
  </style>
</head>
<body>
  <div class="timeline">
    <div class="date">2026-yil</div>
    <div class="dot"></div>
    <div class="event">Yangi platforma ishga tushirildi.</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Grid chiziqlari aniq 80px, 20px va 1fr ga ajratilib, sana, nuqtacha va matn bir chiziqqa teriladi.

## Ishlash natijasi:
```text
Chapda '2026-yil', o'rtada ko'k doiracha va o'ngda voqea matni aks etadi.
```

---

# 694-Topshiriq: Grid yordamida FAQ savol-javoblar ro'yxati
## Topshiriq sharti:
Savol va javob juftliklarini 1fr li grid orqali bir tekisda tartiblang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>FAQ Grid</title>
  <style>
    .faq-grid {
      display: grid;
      gap: 12px;
      width: 300px;
      font-family: sans-serif;
    }
    .faq-card {
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 12px;
    }
  </style>
</head>
<body>
  <div class="faq-grid">
    <div class="faq-card"><strong>Sertifikat beriladimi?</strong><p style="margin: 4px 0 0; font-size: 13px; color: #64748b;">Ha, kurs yakunida rasmiy sertifikat taqdim etiladi.</p></div>
    <div class="faq-card"><strong>Mentor bormi?</strong><p style="margin: 4px 0 0; font-size: 13px; color: #64748b;">Har bir o'quvchiga shaxsiy mentor biriktiriladi.</p></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Grid orqali savollar bloklari orasiga `gap: 12px` bilan chiroyli oraliq beriladi.

## Ishlash natijasi:
```text
Ikkita oq ramkali savol-javob darchalari ketma-ket joylashadi.
```

---

# 695-Topshiriq: Grid yordamida xabarnomalar ro'yxati (Notifications Feed)
## Topshiriq sharti:
Ikonka (30px), xabar matni (1fr) va vaqt (60px) dan iborat 3 ustunli bildirishnoma paneli.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Notifications Grid</title>
  <style>
    .noti-row {
      display: grid;
      grid-template-columns: 30px 1fr 60px;
      gap: 10px;
      align-items: center;
      background: #f8fafc;
      border-bottom: 1px solid #e2e8f0;
      padding: 10px;
      font-family: sans-serif;
      font-size: 13px;
      width: 320px;
    }
    .noti-time { text-align: right; color: #94a3b8; font-size: 11px; }
  </style>
</head>
<body>
  <div class="noti-row">
    <span>&#128276;</span>
    <span>Yangi dars yuklandi</span>
    <span class="noti-time">5 daq</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`30px 1fr 60px` tuzilmasi chekka ma'lumotlarni qat'iy ushlab, xabar matniga butun o'rta maydonni ajratadi.

## Ishlash natijasi:
```text
Qo'ng'iroqcha ikonkasi chapda, xabar o'rtada va '5 daq' vaqti o'ng chetda turadi.
```

---

# 696-Topshiriq: Gridda place-content: center bilan butun panjarani markazlash
## Topshiriq sharti:
place-content shorthandidan foydalanib barcha kataklarni konteyner o'rtasiga to'plang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Place Content Center</title>
  <style>
    .stage {
      display: grid;
      grid-template-columns: 80px 80px;
      grid-template-rows: 60px;
      place-content: center; /* justify-content va align-content ni markazlaydi */
      gap: 10px;
      height: 160px;
      background: #fdf2f8;
      font-family: sans-serif;
    }
    .box { background: #db2777; color: white; display: flex; align-items: center; justify-content: center; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="stage">
    <div class="box">A</div>
    <div class="box">B</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`place-content: center` ota konteyner ichidagi butun grid blokining o'zini gorizontal va vertikal markazga yig'adi.

## Ishlash natijasi:
```text
Och pushti katta soha markazida ikkita to'q pushti katakcha joylashadi.
```

---

# 697-Topshiriq: Grid orqali 3 ustunli Footer menyusi
## Topshiriq sharti:
Sayt etagidagi uchta havola guruhlarini repeat(3, 1fr) bilan taqsimlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Footer Grid</title>
  <style>
    footer {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      background: #0f172a;
      color: white;
      padding: 24px;
      font-family: sans-serif;
    }
    h5 { margin: 0 0 10px 0; color: #38bdf8; }
    p { margin: 0; font-size: 13px; color: #94a3b8; }
  </style>
</head>
<body>
  <footer>
    <div><h5>Biz haqimizda</h5><p>Zamonaviy ta'lim portali.</p></div>
    <div><h5>Kurslar</h5><p>HTML, CSS, JavaScript.</p></div>
    <div><h5>Aloqa</h5><p>info@sayt.uz</p></div>
  </footer>
</body>
</html>
```

## Tushuntirish va Mantiq:
Grid footer ichidagi har bir ustunga 33.3% dan kenglik berib, simmetrik pastki qism hosil qiladi.

## Ishlash natijasi:
```text
To'q qora fonda uchta teng ko'k sarlavhali ma'lumotlar bloki.
```

---

# 698-Topshiriq: Grid yordamida ikkita rasm va bitta katta matn juftligi
## Topshiriq sharti:
Chapda 2 ta rasm ustma-ust, o'ngda esa 1fr li katta tavsif matnini joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Feature Grid Pair</title>
  <style>
    .feature-grid {
      display: grid;
      grid-template-columns: 100px 1fr;
      gap: 12px;
      font-family: sans-serif;
      width: 320px;
    }
    .img-thumb { height: 45px; background: #64748b; border-radius: 4px; margin-bottom: 8px; }
  </style>
</head>
<body>
  <div class="feature-grid">
    <div>
      <div class="img-thumb"></div>
      <div class="img-thumb"></div>
    </div>
    <div style="background: #f1f5f9; padding: 12px; border-radius: 6px;">
      <h4 style="margin: 0 0 6px 0;">Portfolio Loyihalari</h4>
      <p style="margin: 0; font-size: 13px; color: #475569;">O'quvchilar tomonidan tayyorlangan real veb sahifalar.</p>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Chapdagi 100px li ustun kichik rasmlar uchun, o'ngdagi 1fr ustun esa asosiy tavsif uchun xizmat qiladi.

## Ishlash natijasi:
```text
Chapda ikkita kulrang mini rasm, o'ngda esa ularning umumiy tavsif maydoni.
```

---

# 699-Topshiriq: Grid yordamida progress qadamlar ko'rsatkichi
## Topshiriq sharti:
4 ta bosqichni 4 ustunli grid panjarasida teng oraliqda raqamlar bilan ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Step Indicator Grid</title>
  <style>
    .steps-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      font-family: sans-serif;
      text-align: center;
    }
    .step-box {
      padding: 10px;
      background: #f1f5f9;
      border-bottom: 3px solid #cbd5e1;
      font-size: 13px;
    }
    .step-box.active {
      border-color: #2563eb;
      color: #2563eb;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="steps-grid">
    <div class="step-box active">1. Ro'yxat</div>
    <div class="step-box">2. Profil</div>
    <div class="step-box">3. To'lov</div>
    <div class="step-box">4. Tugatish</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`repeat(4, 1fr)` bosqichlarni teng 4 ga bo'lib beradi, faol qadam esa ko'k tagchiziq bilan ajratiladi.

## Ishlash natijasi:
```text
To'rtta qadam qatorda turadi, birinchisining ostida ko'k qalin chiziq ko'rinadi.
```

---

# 700-Topshiriq: To'liq CSS Grid Portali (Header, Sidebar, Main va Widgets)
## Topshiriq sharti:
Faqat CSS Grid shablonlaridan foydalanib to'liq axborot portali maketini quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Complete CSS Grid Portal</title>
  <style>
    body {
      margin: 0;
      min-height: 100vh;
      display: grid;
      grid-template-columns: 200px 1fr 180px;
      grid-template-rows: 60px 1fr 50px;
      font-family: sans-serif;
    }
    header { grid-column: 1 / -1; background: #0f172a; color: white; display: flex; align-items: center; padding: 0 20px; }
    aside.nav { background: #1e293b; color: white; padding: 15px; }
    main { background: #f8fafc; padding: 20px; }
    aside.widgets { background: #f1f5f9; padding: 15px; border-left: 1px solid #e2e8f0; }
    footer { grid-column: 1 / -1; background: #0284c7; color: white; display: flex; align-items: center; justify-content: center; }
  </style>
</head>
<body>
  <header><strong>Portal Header</strong></header>
  <aside class="nav">Chap Menyu</aside>
  <main>
    <h2>Asosiy Kontent</h2>
    <p>CSS Grid yordamida yaratilgan to'liq 3 ustunli portal tizimi.</p>
  </main>
  <aside class="widgets">O'ng Vidjetlar</aside>
  <footer>Portal Footer &copy; 2026</footer>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-template-columns: 200px 1fr 180px` va `grid-template-rows: 60px 1fr 50px` butun sahifa geometriyasini aniq belgilaydi. `grid-column: 1 / -1` sarlavha va footerning butun eni bo'ylab cho'zilishini ta'minlaydi.

## Ishlash natijasi:
```text
Tepadagi qora navbar, pastdagi ko'k footer va o'rtadagi uchta (menyu, maqola, vidjet) ustunlar to'plami.
```

---

