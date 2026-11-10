# HTML va CSS: Flexbox Elementlari va Moslashuvchanlik (Topshiriqlar 601 - 650)

# 601-Topshiriq: Flex-grow: 1 bilan barcha bo'sh joyni egallash
## Topshiriq sharti:
Qatordagi elementlardan biriga flex-grow: 1 berib, ota konteynerdagi ortiqcha bo'shliqni to'liq qamrab olishini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Grow 1</title>
  <style>
    .grow-container {
      display: flex;
      background: #f1f5f9;
      padding: 14px;
      gap: 10px;
      font-family: sans-serif;
    }
    .static-item {
      background: #94a3b8;
      color: white;
      padding: 10px 16px;
      border-radius: 4px;
    }
    .growing-item {
      flex-grow: 1; /* Qolgan bo'sh joyni egallaydi */
      background: #2563eb;
      color: white;
      padding: 10px 16px;
      border-radius: 4px;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="grow-container">
    <div class="static-item">Chap</div>
    <div class="growing-item">O'suvchi Markaz (flex-grow: 1)</div>
    <div class="static-item">O'ng</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-grow: 1` xususiyati flex itemga ota konteynerdagi mavjud barcha bo'sh maydonni o'zlashtirish huquqini beradi. Qolgan elementlar esa faqat o'z kontenti hajmida qoladi.

## Ishlash natijasi:
```text
Chap va O'ng qutilari kichik bo'lib qoladi, markazdagi ko'k quti esa butun qatorni to'ldirib cho'ziladi.
```

---

# 602-Topshiriq: Flex-grow proporsiyalari (1 ga 2 nisbatda o'sish)
## Topshiriq sharti:
Ikkita elementning bo'sh joyni 1:2 nisbatida o'zaro taqsimlashini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Grow Proportions</title>
  <style>
    .prop-container {
      display: flex;
      background: #e2e8f0;
      padding: 12px;
      gap: 12px;
      font-family: sans-serif;
    }
    .box-1 {
      flex-grow: 1;
      background: #0d9488;
      color: white;
      padding: 12px;
      border-radius: 4px;
      text-align: center;
    }
    .box-2 {
      flex-grow: 2;
      background: #0f766e;
      color: white;
      padding: 12px;
      border-radius: 4px;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="prop-container">
    <div class="box-1">1 hissa (flex-grow: 1)</div>
    <div class="box-2">2 hissa (flex-grow: 2)</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-grow` koeffitsientlari ota konteynerdagi ortiqcha bo'sh joyni mutanosib ravishda bo'lib beradi. `box-2` bo'shliqdan `box-1` ga qaraganda 2 barobar ko'proq ulush oladi.

## Ishlash natijasi:
```text
O'ngdagi to'q firuza blok chapdagi blokdan sezilarli darajada kengroq bo'lib render bo'ladi.
```

---

# 603-Topshiriq: Flex-shrink: 0 bilan elementning siqilishini taqiqlash
## Topshiriq sharti:
Konteyner kengligi torayganda rasm yoki ikonka asl o'lchamini yo'qotmasligi uchun flex-shrink: 0 qo'llang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Shrink 0</title>
  <style>
    .card-row {
      display: flex;
      align-items: center;
      gap: 12px;
      width: 240px; /* Tor konteyner */
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      padding: 10px;
      font-family: sans-serif;
    }
    .fixed-avatar {
      flex-shrink: 0; /* Hech qachon siqilmaydi */
      width: 50px;
      height: 50px;
      background: #e11d48;
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="card-row">
    <div class="fixed-avatar">AI</div>
    <div>Juda uzun matnli tavsif bo'lsa ham avatar doirasi o'z shaklini yo'qotmaydi.</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Sukut bo'yicha `flex-shrink: 1` bo'ladi, ya'ni joy yetmaganda elementlar siqiladi. `flex-shrink: 0` berilsa, element o'zining `width` yoki `flex-basis` o'lchamini qat'iy saqlab qoladi.

## Ishlash natijasi:
```text
Qizil doirasimon avatar tuxumsimon bo'lib ezilib qolmaydi, mukammal 50x50px dumaloqligicha turadi.
```

---

# 604-Topshiriq: Flex-shrink koeffitsientlari (2 barobar tezroq siqilish)
## Topshiriq sharti:
Ikkita elementning torayish paytida har xil tezlikda siqilishini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Shrink Rate</title>
  <style>
    .shrink-wrapper {
      display: flex;
      width: 300px;
      background: #fef2f2;
      padding: 10px;
      gap: 10px;
      font-family: sans-serif;
    }
    .box {
      width: 200px;
      padding: 10px;
      color: white;
      text-align: center;
      border-radius: 4px;
    }
    .shrink-1 { flex-shrink: 1; background: #ef4444; }
    .shrink-2 { flex-shrink: 2; background: #b91c1c; }
  </style>
</head>
<body>
  <div class="shrink-wrapper">
    <div class="box shrink-1">shrink: 1</div>
    <div class="box shrink-2">shrink: 2</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Konteyner eni 300px, lekin elementlarning umumiy eni 400px bo'lgani uchun ular siqilishga majbur bo'ladi. `flex-shrink: 2` bo'lgan quti boshqasiga qaraganda 2 barobar ko'proq siqiladi.

## Ishlash natijasi:
```text
To'q qizil quti ochiq qizil qutiga nisbatan ko'proq torayib qisqarganini ko'rish mumkin.
```

---

# 605-Topshiriq: Flex-basis: px bilan aniq boshlang'ich hajm belgilash
## Topshiriq sharti:
Elementning o'sish va siqilishdan oldingi boshlang'ich o'lchamini flex-basis orqali 180px qilib o'rnating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Basis Px</title>
  <style>
    .basis-box {
      display: flex;
      background: #f0fdf4;
      padding: 15px;
      gap: 12px;
      font-family: sans-serif;
    }
    .sidebar-base {
      flex-basis: 180px;
      background: #16a34a;
      color: white;
      padding: 12px;
      border-radius: 4px;
    }
    .content-base {
      flex-grow: 1;
      background: #86efac;
      color: #14532d;
      padding: 12px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="basis-box">
    <div class="sidebar-base">Yon ustun (180px)</div>
    <div class="content-base">Asosiy kontent maydoni</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-basis` asosiy o'qdagi elementning boshlang'ich o'lchamidir (`flex-direction: row` da kenglik, `column` da esa balandlik vazifasini bajaradi).

## Ishlash natijasi:
```text
Yashil yon panel aniq 180px bo'lib turadi, asosiy maydon esa qolgan butun kenglikni to'ldiradi.
```

---

# 606-Topshiriq: Flex-basis: 0 vs flex-basis: auto farqi
## Topshiriq sharti:
Matn uzunligiga qarab emas, balki qat'iy teng ustunlar yaratishda flex-basis: 0 ning ustunligini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Basis 0 vs Auto</title>
  <style>
    .equal-columns {
      display: flex;
      gap: 10px;
      background: #f1f5f9;
      padding: 12px;
      font-family: sans-serif;
    }
    .col-equal {
      flex-grow: 1;
      flex-basis: 0; /* Ichidagi matn hajmiga qaramasdan mutlaq teng taqsimlanadi */
      background: #6366f1;
      color: white;
      padding: 12px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="equal-columns">
    <div class="col-equal">Qisqa</div>
    <div class="col-equal">Bu yerda esa ancha uzunroq matn yozilgan bo'lsa ham ustunlar eni bir xil bo'ladi.</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-basis: auto` bo'lsa, elementning ichidagi matn hisobga olinib, uzunroq element ko'proq joy oladi. Ammo `flex-basis: 0` qilinsa, butun konteyner hajmi noldan boshlab teng ulushlarda bo'lib beriladi.

## Ishlash natijasi:
```text
Ikkala binafsha quti ichidagi matn hajmiga qaramay 50% dan teng kenglikka ega bo'ladi.
```

---

# 607-Topshiriq: Flex: 1 shorthand xususiyatining to'liq tahlili
## Topshiriq sharti:
flex: 1 (flex: 1 1 0%) shorthandidan foydalanib 3 ta bir xil kenglikdagi karta yasang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex 1 Shorthand</title>
  <style>
    .cards-row {
      display: flex;
      gap: 16px;
      font-family: sans-serif;
    }
    .card-item {
      flex: 1; /* flex-grow: 1, flex-shrink: 1, flex-basis: 0% ga teng */
      background: #ffffff;
      border: 1px solid #e2e8f0;
      padding: 16px;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="cards-row">
    <div class="card-item">Karta 1</div>
    <div class="card-item">Karta 2</div>
    <div class="card-item">Karta 3</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex: 1` bu `flex-grow: 1`, `flex-shrink: 1` va `flex-basis: 0%` larning qisqa yozilishidir. U elementlarning konteyner ichida mutanosib va bir xil o'lchamda turishini ta'minlovchi eng mashhur usuldir.

## Ishlash natijasi:
```text
Uchta oq kartochka qatorda 33.3% dan teng joy egallab turadi.
```

---

# 608-Topshiriq: Flex: initial, flex: auto va flex: none kalit so'zlari
## Topshiriq sharti:
Tugmachalar uchun flex: none berib ularning hech qachon o'zgarmasligini namoyish qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex None</title>
  <style>
    .bar {
      display: flex;
      background: #f8fafc;
      padding: 10px;
      gap: 10px;
      font-family: sans-serif;
    }
    .grow-field {
      flex: auto; /* flex: 1 1 auto */
      padding: 8px 12px;
      border: 1px solid #cbd5e1;
      border-radius: 4px;
    }
    .fixed-btn {
      flex: none; /* flex: 0 0 auto (o'smaydi, siqilmaydi) */
      background: #0284c7;
      color: white;
      border: none;
      padding: 8px 18px;
      border-radius: 4px;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div class="bar">
    <input type="text" class="grow-field" placeholder="Izlash...">
    <button class="fixed-btn">Qidirish</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex: none` elementni mutlaqo moslashuvchan bo'lmagan (`flex: 0 0 auto`) holatga keltiradi. U o'zining tabiiy o'lchamida qoladi va qisqarish yoki kengayishga bo'ysunmaydi.

## Ishlash natijasi:
```text
Input qidiruv maydoni qolgan butun bo'sh joyni egallaydi, tugma esa qat'iy o'z hajmida turadi.
```

---

# 609-Topshiriq: Order xususiyati bilan elementlar ketma-ketligini o'zgartirish
## Topshiriq sharti:
HTML da uchinchi o'rinda turgan elementni order: -1 yordamida eng boshiga chiqarib qo'ying.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Order</title>
  <style>
    .order-container {
      display: flex;
      gap: 12px;
      font-family: sans-serif;
    }
    .item {
      padding: 14px 20px;
      border-radius: 6px;
      color: white;
      font-weight: bold;
    }
    .i1 { background: #64748b; }
    .i2 { background: #64748b; }
    .i3-special {
      background: #ef4444;
      order: -1; /* Manfiy tartib uni eng birinchi qilib chiqaradi */
    }
  </style>
</head>
<body>
  <div class="order-container">
    <div class="item i1">Element 1</div>
    <div class="item i2">Element 2</div>
    <div class="item i3-special">Element 3 (Maxsus)</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`order` xususiyati elementning vizual navbatini belgilaydi. Standart qiymat `0` dir. Kichikroq qiymat (masalan `-1`) elementni boshqa standart elementlardan oldinga chiqaradi.

## Ishlash natijasi:
```text
HTML da uchinchi bo'lgan qizil 'Element 3' ekranda eng birinchi bo'lib ko'rinadi.
```

---

# 610-Topshiriq: Align-self: center bilan bitta elementni alohida markazlashtirish
## Topshiriq sharti:
Boshqa elementlar yuqorida turgan holda faqat bitta elementni alohida vertikal o'rtaga tekislang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Align Self Center</title>
  <style>
    .container {
      display: flex;
      align-items: flex-start;
      height: 140px;
      background: #f1f5f9;
      gap: 12px;
      padding: 12px;
      font-family: sans-serif;
    }
    .box { background: #3b82f6; color: white; padding: 10px 16px; border-radius: 4px; }
    .special-box {
      align-self: center; /* Otaning align-items qoidasini inkor etadi */
      background: #8b5cf6;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="box">Tepada 1</div>
    <div class="box special-box">O'rtada (align-self: center)</div>
    <div class="box">Tepada 2</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`align-self` xususiyati ota konteynerning `align-items` qoidasini faqat shu alohida bola uchun inkor etish (override) imkonini beradi.

## Ishlash natijasi:
```text
Ikkita ko'k quti yuqori chetda turadi, o'rtadagi binafsharang quti esa balandlik bo'yicha markazda turadi.
```

---

# 611-Topshiriq: Align-self: flex-end bilan bitta elementni tubga tushirish
## Topshiriq sharti:
Bitta elementni o'zining ota balandligi bo'yicha pastki qirrasiga tekkizib qo'ying.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Align Self End</title>
  <style>
    .box-row {
      display: flex;
      align-items: flex-start;
      height: 120px;
      background: #fef3c7;
      gap: 10px;
      padding: 10px;
      font-family: sans-serif;
    }
    .item { background: #f59e0b; color: white; padding: 8px 14px; border-radius: 4px; }
    .bottom-item {
      align-self: flex-end;
      background: #b45309;
    }
  </style>
</head>
<body>
  <div class="box-row">
    <div class="item">Yuqorida</div>
    <div class="item bottom-item">Pastda (align-self: flex-end)</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`align-self: flex-end` alohida elementni ko'ndalang o'qning oxiriga tushiradi, bu esa boshqa elementlarning joylashuviga mutlaqo xalal bermaydi.

## Ishlash natijasi:
```text
Ochiq sariq fonda bir quti tepada, to'q sariq quti esa polga yopishib ko'rinadi.
```

---

# 612-Topshiriq: Zamonaviy Navbar arxitekturasi (Logo, Markaziy qidiruv, Profil)
## Topshiriq sharti:
Logo va profil o'z o'lchamini saqlasin, qidiruv paneli esa flex: 1 bilan markazni to'ldirsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Modern Navbar Layout</title>
  <style>
    .navbar {
      display: flex;
      align-items: center;
      gap: 20px;
      background: #0f172a;
      padding: 12px 24px;
      color: white;
      font-family: sans-serif;
    }
    .nav-logo { flex: 0 0 auto; font-weight: bold; font-size: 18px; }
    .nav-search {
      flex: 1; /* Markazdagi barcha bo'sh joyni qamraydi */
      max-width: 480px;
    }
    .search-input {
      width: 100%;
      padding: 8px 14px;
      border-radius: 20px;
      border: none;
      box-sizing: border-box;
      outline: none;
    }
    .nav-actions { flex: 0 0 auto; display: flex; gap: 12px; }
  </style>
</head>
<body>
  <header class="navbar">
    <div class="nav-logo">DevAcademy</div>
    <div class="nav-search">
      <input type="text" class="search-input" placeholder="Kurslarni izlang...">
    </div>
    <div class="nav-actions">
      <span>&#128276;</span>
      <span>&#128100; Profil</span>
    </div>
  </header>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu maketda chetki bloklarga `flex: 0 0 auto` berilib, markazdagi qidiruvga `flex: 1` beriladi. Natijada qidiruv maydoni ekran o'lchami o'zgarganda qisqarib va kengayib turadi.

## Ishlash natijasi:
```text
Chapda logotip, markazda cho'ziluvchan qidiruv darchasi va o'ngda profil havolalari.
```

---

# 613-Topshiriq: Flexboxda Media Object shabloni (Avatar o'zgarmas, matn elastik)
## Topshiriq sharti:
Avatar har doim 60x60px bo'lib tursin, yonidagi matn esa qolgan kenglikka moslashsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Elastic Media Object</title>
  <style>
    .media {
      display: flex;
      gap: 16px;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      padding: 16px;
      border-radius: 8px;
      width: 320px;
      font-family: sans-serif;
    }
    .media-avatar {
      flex: 0 0 60px; /* Aniq 60px kenglik va siqilmaslik */
      height: 60px;
      background: #3b82f6;
      border-radius: 8px;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
    }
    .media-body {
      flex: 1; /* Qolgan kenglikni to'liq qoplaydi */
    }
  </style>
</head>
<body>
  <div class="media">
    <div class="media-avatar">&#9733;</div>
    <div class="media-body">
      <h4 style="margin: 0 0 6px 0;">Premium A'zolik</h4>
      <p style="margin: 0; font-size: 13px; color: #64748b;">Barcha yopiq video darslar va kodlar omboriga cheksiz kirish huquqi.</p>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex: 0 0 60px` avatarni qat'iy o'lchamda mustahkamlaydi, `flex: 1` esa matn blokiga qolgan enni to'liq berib, responsivlikni ta'minlaydi.

## Ishlash natijasi:
```text
Chapda ko'k yulduzli 60x60px kvadrat ikonka, o'ngda esa moslashuvchan matn maydoni.
```

---

# 614-Topshiriq: Holy Grail Layout (Sarlavha, 2 ta yon ustun, markaz va footer)
## Topshiriq sharti:
Klassik 3 ustunli sayt maketini flexbox yordamida to'liq amalga oshiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Holy Grail Flex</title>
  <style>
    body {
      margin: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      font-family: sans-serif;
    }
    header, footer { background: #1e293b; color: white; padding: 15px; text-align: center; }
    .main-area {
      flex: 1;
      display: flex;
    }
    .nav-side { flex: 0 0 150px; background: #e2e8f0; padding: 15px; }
    .content-center { flex: 1; background: #ffffff; padding: 20px; }
    .ads-side { flex: 0 0 140px; background: #f1f5f9; padding: 15px; }
  </style>
</head>
<body>
  <header>Sayt Sarlavhasi</header>
  <div class="main-area">
    <nav class="nav-side">Chap Menyu</nav>
    <main class="content-center">Asosiy Katta Maqola Matni</main>
    <aside class="ads-side">O'ng Reklama</aside>
  </div>
  <footer>Footer &copy; 2026</footer>
</body>
</html>
```

## Tushuntirish va Mantiq:
Asosiy `.main-area` ga `flex: 1` berilib oyna bo'yicha to'liq cho'ziladi. Ichidagi ustunlar esa `flex: 0 0 150px` (nav), `flex: 1` (center) va `flex: 0 0 140px` (ads) bo'yicha taqsimlanadi.

## Ishlash natijasi:
```text
Yuqori sarlavha, pastki footer va o'rtada uch ustunli to'liq veb sahifa arxitekturasi.
```

---

# 615-Topshiriq: Flexboxda tugmalar tartibini mobil ekranda o'zgartirish (Order: 1)
## Topshiriq sharti:
Kichik ekranlarda tasdiqlash tugmasini yuqoriga yoki birinchi o'ringa ko'chirish mexanizmi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Responsive Order</title>
  <style>
    .dialog-btns {
      display: flex;
      flex-direction: column;
      gap: 8px;
      width: 220px;
      font-family: sans-serif;
    }
    .btn-cancel {
      order: 2; /* Pastga tushadi */
      padding: 10px;
      background: #e2e8f0;
      border: none;
      border-radius: 4px;
    }
    .btn-confirm {
      order: 1; /* Yuqoriga chiqadi */
      padding: 10px;
      background: #16a34a;
      color: white;
      border: none;
      border-radius: 4px;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="dialog-btns">
    <button class="btn-cancel">Bekor qilish</button>
    <button class="btn-confirm">Oldinga davom etish</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
HTML da bekor qilish tugmasi birinchi turgan bo'lsa ham, `order: 1` va `order: 2` orqali yashil 'Davom etish' tugmasi vizual tarzda ustiga ko'tariladi.

## Ishlash natijasi:
```text
Yashil 'Oldinga davom etish' birinchi, kulrang 'Bekor qilish' esa uning tagida ko'rinadi.
```

---

# 616-Topshiriq: Flexboxda matn sarlavhasi qisqarishi (Text Ellipsis muammosi)
## Topshiriq sharti:
Flex item ichidagi uzun matn qatoridan chiqib ketmasdan '...' bilan qisqarishi uchun min-width: 0 dan foydalaning.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Min-Width Ellipsis</title>
  <style>
    .user-row {
      display: flex;
      align-items: center;
      gap: 12px;
      width: 220px;
      background: #f1f5f9;
      padding: 10px;
      border-radius: 6px;
      font-family: sans-serif;
    }
    .avatar { width: 36px; height: 36px; background: #64748b; border-radius: 50%; flex-shrink: 0; }
    .text-info {
      flex: 1;
      min-width: 0; /* Flexboxda ellipsis ishlashi uchun shart! */
    }
    .truncate-text {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin: 0;
    }
  </style>
</head>
<body>
  <div class="user-row">
    <div class="avatar"></div>
    <div class="text-info">
      <p class="truncate-text">juda_uzun_foydalanuvchi_email_manzili@domen.uz</p>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Flex elementlarda sukut bo'yicha `min-width: auto` bo'ladi va matn o'z kontentidan torayolmaydi. `min-width: 0` berilishi bilan `text-overflow: ellipsis` mukammal ishlaydi.

## Ishlash natijasi:
```text
Uzun email manzili qutidan chiqib ketmay, oxirida '...' belgisi bilan qisqaradi.
```

---

# 617-Topshiriq: Flexbox bilan moslashuvchan narxlar jadvali (Pricing Cards)
## Topshiriq sharti:
O'rtadagi tavsiya etilgan kartani align-self va transform orqali biroz kattaroq qilib ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Pricing Table Flex</title>
  <style>
    .pricing-wrap {
      display: flex;
      align-items: center;
      gap: 16px;
      font-family: sans-serif;
    }
    .price-card {
      flex: 1;
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 20px;
      text-align: center;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .price-card.featured {
      border: 2px solid #2563eb;
      transform: scale(1.05);
      box-shadow: 0 8px 16px rgba(37,99,235,0.15);
    }
  </style>
</head>
<body>
  <div class="pricing-wrap">
    <div class="price-card">
      <h4>Boshlang'ich</h4>
      <h2>Bepul</h2>
    </div>
    <div class="price-card featured">
      <h4 style="color: #2563eb;">Professional</h4>
      <h2>$19</h2>
    </div>
    <div class="price-card">
      <h4>Korxona</h4>
      <h2>$49</h2>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Barcha kartalar `flex: 1` orqali teng en oladi, o'rtadagi `.featured` karta esa `transform: scale(1.05)` va ko'k ramka orqali e'tiborni tortadi.

## Ishlash natijasi:
```text
Uchta tarif rejasi, o'rtadagi 'Professional' kartasi boshqalaridan biroz yirikroq bo'lib ajralib turadi.
```

---

# 618-Topshiriq: Flexbox bilan ko'p qatorli Taglar filtri
## Topshiriq sharti:
Foydalanuvchi qiziqishlari ro'yxatini flex-wrap va flex: 0 0 auto orqali toza chiplar shaklida joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Tags Filter Flex</title>
  <style>
    .filter-group {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      width: 280px;
      font-family: sans-serif;
    }
    .filter-chip {
      flex: 0 0 auto;
      padding: 6px 14px;
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      border-radius: 20px;
      font-size: 13px;
      cursor: pointer;
    }
    .filter-chip.active {
      background: #2563eb;
      color: white;
      border-color: #2563eb;
    }
  </style>
</head>
<body>
  <div class="filter-group">
    <span class="filter-chip active">Barchasi</span>
    <span class="filter-chip">Frontend</span>
    <span class="filter-chip">Backend</span>
    <span class="filter-chip">DevOps</span>
    <span class="filter-chip">Mobile</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex: 0 0 auto` teglarni o'z ichidagi matn uzunligiga qarab shakllantiradi va toraytirib siqib qo'ymaydi.

## Ishlash natijasi:
```text
Ochiq kulrang va bitta ko'k faol filtr chiplari bir necha qatorga chiroyli joylashadi.
```

---

# 619-Topshiriq: Flexboxda tugmalar qatori: chapga, o'rtaga va o'ngga taqsimlash
## Topshiriq sharti:
3 ta amallar guruhini bitta navigatsiya panelida margin-left/right: auto orqali joylashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Tri-Section Bar</title>
  <style>
    .nav-three {
      display: flex;
      align-items: center;
      background: #ffffff;
      border: 1px solid #e2e8f0;
      padding: 10px 18px;
      font-family: sans-serif;
    }
    .left-zone { margin-right: auto; }
    .center-zone { margin: 0 auto; }
    .right-zone { margin-left: auto; }
  </style>
</head>
<body>
  <div class="nav-three">
    <div class="left-zone"><strong>Mavzu 12</strong></div>
    <div class="center-zone"><button>&lt;</button> 5 / 20 <button>&gt;</button></div>
    <div class="right-zone"><button style="background: #2563eb; color: white; border: none; padding: 6px 12px; border-radius: 4px;">Tugatish</button></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Flexboxda margin avtomatlashtirish qobiliyati juda kuchli: `margin-right: auto` chap zonani qoldirib qolganini o'ngga itaradi, `margin: 0 auto` esa markaziy zonani qoq o'rtada ushlaydi.

## Ishlash natijasi:
```text
Mavzu nomi chapda, sahifalash o'rtada va 'Tugatish' tugmasi eng o'ngda mukammal turadi.
```

---

# 620-Topshiriq: Flexbox bilan moslashuvchan qadamlar ko'rsatkichi (Stepper UI)
## Topshiriq sharti:
Ro'yxatdan o'tish qadamlarini ko'rsatuvchi raqamli bosqichlar zanjirini flex orqali yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Stepper UI</title>
  <style>
    .stepper {
      display: flex;
      align-items: center;
      width: 320px;
      font-family: sans-serif;
    }
    .step-circle {
      width: 30px;
      height: 30px;
      border-radius: 50%;
      background: #cbd5e1;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      flex-shrink: 0;
    }
    .step-circle.done { background: #16a34a; }
    .step-line {
      flex: 1;
      height: 3px;
      background: #cbd5e1;
      margin: 0 8px;
    }
    .step-line.done { background: #16a34a; }
  </style>
</head>
<body>
  <div class="stepper">
    <div class="step-circle done">&#10003;</div>
    <div class="step-line done"></div>
    <div class="step-circle done">2</div>
    <div class="step-line"></div>
    <div class="step-circle">3</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Doiralar `flex-shrink: 0` bilan doimo 30px bo'lib turadi, o'rtadagi chiziqlar esa `flex: 1` bilan barcha oraliq bo'shliqni to'ldirib o'sadi.

## Ishlash natijasi:
```text
1- va 2-qadamlari yashil, 3-qadami esa kulrang bo'lgan ko'rkam qadamlar chizig'i.
```

---

# 621-Topshiriq: Flexboxda tugmalar ichidagi yuklanish aylanasi va matn
## Topshiriq sharti:
Tugma bosilganda matn va yuklanish ikonkasi bir chiziqda turishi uchun display: inline-flex qo'llang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Loading Button Flex</title>
  <style>
    .btn-loading {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      background: #2563eb;
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 6px;
      font-family: sans-serif;
      font-size: 14px;
      cursor: wait;
    }
    .spin {
      width: 14px;
      height: 14px;
      border: 2px solid white;
      border-top-color: transparent;
      border-radius: 50%;
      animation: rotate 0.8s linear infinite;
    }
    @keyframes rotate { to { transform: rotate(360deg); } }
  </style>
</head>
<body>
  <button class="btn-loading">
    <span class="spin"></span>
    <span>Yuklanmoqda...</span>
  </button>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: inline-flex` tugma ichidagi aylanayotgan doira va matnni vertikal o'qda bir xil tekislikda ushlab turadi.

## Ishlash natijasi:
```text
Ko'k tugma ichida oq aylanayotgan spinner va 'Yuklanmoqda...' matni yonma-yon ko'rinadi.
```

---

# 622-Topshiriq: Chat interfeysi: Xabarlar oqimi va skroll hududi
## Topshiriq sharti:
Flex-direction: column va flex: 1 bilan faqat xabarlar maydoni skroll bo'ladigan chat ramkasini quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Chat Box Flex</title>
  <style>
    .chat-box {
      display: flex;
      flex-direction: column;
      width: 280px;
      height: 250px;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      font-family: sans-serif;
    }
    .chat-top { background: #1e293b; color: white; padding: 10px; font-weight: bold; }
    .chat-body {
      flex: 1; /* O'rta soha cho'ziladi va skroll bo'ladi */
      overflow-y: auto;
      padding: 10px;
      background: #f8fafc;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .msg-in { align-self: flex-start; background: white; padding: 6px 10px; border-radius: 6px; font-size: 13px; }
    .msg-out { align-self: flex-end; background: #3b82f6; color: white; padding: 6px 10px; border-radius: 6px; font-size: 13px; }
  </style>
</head>
<body>
  <div class="chat-box">
    <div class="chat-top">Muloqot</div>
    <div class="chat-body">
      <div class="msg-in">Salom!</div>
      <div class="msg-out">Salom, qandaysiz?</div>
      <div class="msg-in">Dars bo'yicha savolim bor edi.</div>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`align-self: flex-start` kiruvchi xabarni chapda ushlaydi, `align-self: flex-end` esa chiquvchi xabarni o'ng chetga tekislaydi. `flex: 1; overflow-y: auto` esa xabarlar ko'payganda o'rta sohani skroll qiladi.

## Ishlash natijasi:
```text
Tepa qora sarlavhali, ichida chap va o'ngga terilgan xabarlar darchasi.
```

---

# 623-Topshiriq: Flexboxda bir xil o'lchamdagi 4 ta ijtimoiy tarmoq tugmalari
## Topshiriq sharti:
Instagram, Telegram, YouTube va GitHub ikonkalari bitta qatorda teng masofada bo'lsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Social Icons Flex</title>
  <style>
    .social-bar {
      display: flex;
      justify-content: space-between;
      width: 220px;
      background: #f1f5f9;
      padding: 10px;
      border-radius: 8px;
      font-family: sans-serif;
    }
    .icon-link {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 40px;
      height: 40px;
      background: white;
      border-radius: 50%;
      text-decoration: none;
      color: #334155;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      font-size: 18px;
    }
  </style>
</head>
<body>
  <div class="social-bar">
    <a href="#" class="icon-link">&#9993;</a>
    <a href="#" class="icon-link">&#9742;</a>
    <a href="#" class="icon-link">&#127760;</a>
    <a href="#" class="icon-link">&#9881;</a>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ota blok `justify-content: space-between` orqali 4 ta doirani chetlarga tekis taqsimlaydi, har bir doira ichida esa `display: flex; align-items: center; justify-content: center` belgini markazda ushlaydi.

## Ishlash natijasi:
```text
Kulrang panel ichida 4 ta oppoq dumaloq tugmalar chiroyli tizilgan holda turadi.
```

---

# 624-Topshiriq: Flexbox bilan ko'p ustunli ro'yxat tartiblash (Multi-column Checklist)
## Topshiriq sharti:
10 ta afzalliklar bandini 2 ustunga flex-wrap va 50% kenglik bilan taqsimlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Two Column Checklist</title>
  <style>
    .checklist {
      display: flex;
      flex-wrap: wrap;
      width: 320px;
      gap: 8px 0;
      list-style: none;
      padding: 0;
      font-family: sans-serif;
      font-size: 13px;
    }
    .checklist li {
      flex: 0 0 50%; /* Har biri qatorning teng yarmini egallaydi */
      box-sizing: border-box;
      padding-right: 8px;
    }
  </style>
</head>
<body>
  <ul class="checklist">
    <li>&#10004; HTML5</li>
    <li>&#10004; CSS3</li>
    <li>&#10004; Flexbox</li>
    <li>&#10004; CSS Grid</li>
    <li>&#10004; Responsive</li>
    <li>&#10004; Animations</li>
  </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex: 0 0 50%` va `flex-wrap: wrap` orqali har bir `li` elementi qatorning roppa-rosa yarmini egallaydi va avtomatik ravishda 2 ustunli toza ro'yxat hosil bo'ladi.

## Ishlash natijasi:
```text
2 ustunga tartib bilan ajratilgan 6 ta qushchali texnologiyalar ro'yxati.
```

---

# 625-Topshiriq: Flexboxda mahsulot narxi va eskirgan narx (Strikethrough)
## Topshiriq sharti:
Chegirmali yangi narx va chizib tashlangan eski narxni flex qatorida chiroyli ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Price Tag Flex</title>
  <style>
    .price-row {
      display: flex;
      align-items: baseline;
      gap: 10px;
      font-family: sans-serif;
    }
    .current-price {
      font-size: 24px;
      font-weight: bold;
      color: #059669;
    }
    .old-price {
      font-size: 15px;
      color: #94a3b8;
      text-decoration: line-through;
    }
  </style>
</head>
<body>
  <div class="price-row">
    <span class="current-price">350,000 so'm</span>
    <span class="old-price">500,000 so'm</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`align-items: baseline` yordamida har xil o'lchamdagi 24px yangi narx va 15px chizilgan eski narx pastki harf chizig'i bo'yicha mukammal bir xil darajada turadi.

## Ishlash natijasi:
```text
Yashil katta yangi narx yonida chizilgan kulrang eski narx chiroyli aks etadi.
```

---

# 626-Topshiriq: Flexbox bilan moslashuvchan progress bar (Taraqqiyot chizig'i)
## Topshiriq sharti:
Chiziqning to'lgan qismini flex: 0.7 (70%) orqali dinamik ifodalang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Progress Bar Flex</title>
  <style>
    .progress-track {
      display: flex;
      width: 260px;
      height: 12px;
      background: #e2e8f0;
      border-radius: 6px;
      overflow: hidden;
    }
    .progress-fill {
      flex: 0 0 70%; /* 70% to'lgan */
      background: #2563eb;
    }
  </style>
</head>
<body>
  <div class="progress-track">
    <div class="progress-fill"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex: 0 0 70%` progress chizig'ining to'ldirilgan qismini ota konteyner eniga nisbatan aniq 70 foizini egallashini ta'minlaydi.

## Ishlash natijasi:
```text
Kulrang chiziq ichida 70% qismi to'q ko'k rang bilan to'ldirilgan taraqqiyot chizig'i.
```

---

# 627-Topshiriq: Flexboxda ustun ichida elementlarni ikki qirra bo'ylab ajratish
## Topshiriq sharti:
Vertikal kartochkada sarlavhani eng tepada, muallifni esa eng pastda ushlab turishni space-between bilan qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Column Space Between</title>
  <style>
    .quote-box {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      width: 200px;
      height: 150px;
      background: #fdf4ff;
      border: 1px solid #f5d0fe;
      border-radius: 8px;
      padding: 16px;
      font-family: sans-serif;
    }
  </style>
</head>
<body>
  <div class="quote-box">
    <p style="margin: 0; font-style: italic;">"Ilm olish igna bilan quduq qazish kabidir."</p>
    <small style="color: #a21caf; font-weight: bold;">Xalq maqoli</small>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-direction: column` qilinganda `justify-content: space-between` elementlarni vertikal yuqori va pastki qirralarga ajratib tashlaydi.

## Ishlash natijasi:
```text
Iqtibos matni kartaning eng tepasida, muallif esa eng pastki qismida joylashadi.
```

---

# 628-Topshiriq: Flexbox bilan moslashuvchan qidiruv teglari filtri
## Topshiriq sharti:
Tanlangan filtr teglari yonida kichik 'x' tugmasini inline-flex bilan birlashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Dismissible Chip</title>
  <style>
    .removable-chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      color: #1d4ed8;
      padding: 4px 10px;
      border-radius: 16px;
      font-family: sans-serif;
      font-size: 13px;
    }
    .chip-close {
      cursor: pointer;
      font-weight: bold;
      font-size: 14px;
    }
  </style>
</head>
<body>
  <div class="removable-chip">
    <span>Kategoriya: Dasturlash</span>
    <span class="chip-close">&times;</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: inline-flex; align-items: center` chip ichidagi matn va 'x' belgisini vertikal markazda tekislaydi.

## Ishlash natijasi:
```text
Moviy fonli chip ichida matn va o'ng tomonida 'x' o'chirish belgisi.
```

---

# 629-Topshiriq: Flexboxda tugmalar qatorida o'ngdagi amallarni alohida ajratish
## Topshiriq sharti:
Matn muharriri asboblar panelida shrift tugmalarini chapda, yordam tugmasini margin-left: auto bilan o'ngda ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Editor Toolbar</title>
  <style>
    .toolbar {
      display: flex;
      align-items: center;
      gap: 6px;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      padding: 6px 12px;
      font-family: sans-serif;
    }
    .tool-btn { padding: 4px 8px; border: 1px solid #cbd5e1; background: white; border-radius: 4px; cursor: pointer; }
    .help-btn { margin-left: auto; background: #e0e7ff; color: #4338ca; border-color: #c7d2fe; }
  </style>
</head>
<body>
  <div class="toolbar">
    <button class="tool-btn"><strong>B</strong></button>
    <button class="tool-btn"><em>I</em></button>
    <button class="tool-btn"><u>U</u></button>
    <button class="tool-btn help-btn">Yordam</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`margin-left: auto` berilgan '.help-btn' qolgan barcha bo'sh joyni o'zlashtirib, o'zini eng o'ng burchakka qaratadi.

## Ishlash natijasi:
```text
Qalin, kursiv va osti chizilgan tugmalar chapda, 'Yordam' tugmasi esa o'ng tomonda turadi.
```

---

# 630-Topshiriq: Flexbox orqali rasm va matnli mahsulot kartasi (E-Commerce Card)
## Topshiriq sharti:
Mahsulot surati, nomi, tavsifi, narxi va 'Savatga' tugmasini flex-direction: column bilan to'liq yig'ing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Shop Card Flex</title>
  <style>
    .shop-card {
      display: flex;
      flex-direction: column;
      width: 220px;
      background: white;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      overflow: hidden;
      font-family: sans-serif;
      box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
    .card-img { height: 120px; background: #cbd5e1; display: flex; align-items: center; justify-content: center; color: #64748b; }
    .card-info { padding: 14px; display: flex; flex-direction: column; flex: 1; }
    .card-price { margin-top: auto; padding-top: 10px; font-weight: bold; color: #0284c7; }
  </style>
</head>
<body>
  <div class="shop-card">
    <div class="card-img">Rasm</div>
    <div class="card-info">
      <h4 style="margin: 0 0 6px 0;">Simsiz Quloqchin</h4>
      <p style="margin: 0; font-size: 12px; color: #64748b;">Shovqinni bekor qiluvchi yangi avlod texnologiyasi.</p>
      <div class="card-price">299,000 so'm</div>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`card-info` dagi `display: flex; flex-direction: column` va narxdagi `margin-top: auto` narxni har doim kartaning eng pastki qismiga joylashtiradi.

## Ishlash natijasi:
```text
Tepada rasm foni, markazda sarlavha va matn, pastki polida esa narx ko'rsatilgan karta.
```

---

# 631-Topshiriq: Flexboxda ro'yxat tartibini dinamik almashtirish (Sidebar joylashuvi)
## Topshiriq sharti:
Order xususiyati orqali yon menyuni chapdan o'ng tomonga bir qatorda ko'chirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Swap Sidebar Order</title>
  <style>
    .site-container {
      display: flex;
      gap: 16px;
      font-family: sans-serif;
    }
    .sidebar {
      flex: 0 0 160px;
      background: #f1f5f9;
      padding: 12px;
      border-radius: 6px;
      order: 2; /* O'ng tomonga o'tadi */
    }
    .main-body {
      flex: 1;
      background: #ffffff;
      border: 1px solid #cbd5e1;
      padding: 16px;
      border-radius: 6px;
      order: 1; /* Chap tomonga o'tadi */
    }
  </style>
</head>
<body>
  <div class="site-container">
    <aside class="sidebar">Menyu Ustuni</aside>
    <main class="main-body">Asosiy Maqola</main>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
HTML kodida `sidebar` birinchi yozilgan bo'lsa-da, unga `order: 2` va `main-body` ga `order: 1` berilgani tufayli ular o'rni almashadi.

## Ishlash natijasi:
```text
Asosiy maqola chapda, yon menyu esa o'ng tomonda aks etadi.
```

---

# 632-Topshiriq: Flexbox bilan moslashuvchan ko'p variantli tanlov (Card Radio UI)
## Topshiriq sharti:
Foydalanuvchi tanlashi uchun 3 ta kartani flex qatorida teng o'lchamda ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Card Radio UI</title>
  <style>
    .plan-grid {
      display: flex;
      gap: 12px;
      font-family: sans-serif;
      width: 320px;
    }
    .plan-option {
      flex: 1;
      border: 2px solid #e2e8f0;
      border-radius: 8px;
      padding: 12px;
      text-align: center;
      cursor: pointer;
    }
    .plan-option.selected {
      border-color: #2563eb;
      background: #eff6ff;
    }
  </style>
</head>
<body>
  <div class="plan-grid">
    <div class="plan-option">1 Oy</div>
    <div class="plan-option selected">6 Oy</div>
    <div class="plan-option">12 Oy</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex: 1` orqali 3 ta tanlov bloki konteyner bo'ylab teng taqsimlanadi va har biri bosiluvchi tanlov kartasi kabi xizmat qiladi.

## Ishlash natijasi:
```text
Teng o'lchamdagi uchta karta, o'rtadagi '6 Oy' kartasi ko'k hoshiya va fon bilan faollashtirilgan.
```

---

# 633-Topshiriq: Flexboxda taglavha va muallif ma'lumotlarini markazlashtirish
## Topshiriq sharti:
Kichik doiraviy rasm, ism va nashr qilingan vaqtni bitta chiziqda joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Author Info Flex</title>
  <style>
    .author-meta {
      display: flex;
      align-items: center;
      gap: 10px;
      font-family: sans-serif;
      font-size: 13px;
    }
    .avatar-mini {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: #10b981;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
    }
    .meta-date { color: #94a3b8; }
  </style>
</head>
<body>
  <div class="author-meta">
    <div class="avatar-mini">A</div>
    <strong>Anvar Z.</strong>
    <span class="meta-date">&bull; 2 soat oldin</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: flex; align-items: center` tufayli avatar doirasi, qalin ism va sana nuqta bilan birga tekis qatorda turadi.

## Ishlash natijasi:
```text
Yashil mini avatar, qalin yozilgan muallif ismi va kulrang '2 soat oldin' yozuvi.
```

---

# 634-Topshiriq: Flexbox bilan moslashuvchan ko'rsatkichli metrikalar
## Topshiriq sharti:
Statistika panelida 3 ta ko'rsatkichni ajratuvchi vertikal chiziqlar bilan yonma-yon qo'ying.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Metrics Bar Flex</title>
  <style>
    .metrics-bar {
      display: flex;
      align-items: center;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 12px 0;
      font-family: sans-serif;
    }
    .metric-item {
      flex: 1;
      text-align: center;
    }
    .metric-item:not(:last-child) {
      border-right: 1px solid #e2e8f0;
    }
    .val { font-size: 18px; font-weight: bold; color: #1e293b; }
    .lbl { font-size: 11px; color: #64748b; }
  </style>
</head>
<body>
  <div class="metrics-bar">
    <div class="metric-item"><div class="val">1,240</div><div class="lbl">Foydalanuvchi</div></div>
    <div class="metric-item"><div class="val">89%</div><div class="lbl">Qoniqish</div></div>
    <div class="metric-item"><div class="val">4.9</div><div class="lbl">Reyting</div></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Har bir metrikaga `flex: 1` berilib kenglik 3 ga teng bo'linadi, `border-right` orqali esa ular orasiga nozik vertikal chiziq tortiladi.

## Ishlash natijasi:
```text
Uchta metrika teng maydonda, o'rtalarida ajratuvchi chiziqlar bilan aks etadi.
```

---

# 635-Topshiriq: Flexboxda audio pleer boshqaruv tugmalari paneli
## Topshiriq sharti:
Orqaga, Ijro (katta) va Oldinga tugmalarini gorizontal o'q bo'ylab markazlashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Player Controls Flex</title>
  <style>
    .player-controls {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 18px;
      background: #1e293b;
      padding: 14px;
      border-radius: 30px;
      width: fit-content;
    }
    .ctrl-btn { background: none; border: none; color: white; font-size: 18px; cursor: pointer; }
    .play-circle {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: #2563eb;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
    }
  </style>
</head>
<body>
  <div class="player-controls">
    <button class="ctrl-btn">&#9198;</button>
    <button class="ctrl-btn play-circle">&#9658;</button>
    <button class="ctrl-btn">&#9197;</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`align-items: center` tufayli katta 44px li ko'k Play doirasi bilan yonidagi kichikroq o'tkazish tugmalari bir vertikal o'qda uyg'unlashadi.

## Ishlash natijasi:
```text
To'q qora yumaloq paneldagi o'rtada ko'k Play va yonlarida orqaga/oldinga strelkalari.
```

---

# 636-Topshiriq: Flexboxda tugmalar blokini polga tekislash (Card Footer Alignment)
## Topshiriq sharti:
Karta kontenti turli uzunlikda bo'lsa ham pastki harakat tugmalarini bir xil pol chizig'iga keltiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Card Footer Floor</title>
  <style>
    .card-deck {
      display: flex;
      gap: 16px;
      font-family: sans-serif;
    }
    .card {
      flex: 1;
      display: flex;
      flex-direction: column;
      background: #ffffff;
      border: 1px solid #cbd5e1;
      padding: 16px;
      border-radius: 8px;
    }
    .btn-bottom {
      margin-top: auto;
      padding: 8px;
      background: #3b82f6;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div class="card-deck">
    <div class="card">
      <h4>Qisqa Karta</h4>
      <p>Bir qator matn.</p>
      <button class="btn-bottom">Ko'rish</button>
    </div>
    <div class="card">
      <h4>Uzun Karta</h4>
      <p>Bu kartaning matni ancha ko'p bo'lib, bir necha qatorni egallaydi va balandlikni oshiradi.</p>
      <button class="btn-bottom">Ko'rish</button>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: flex; flex-direction: column` qilingan kartada `margin-top: auto` berilgan tugma pastki chegara poliga qadalib, ikkala kartada ham tugmalar bir xil chiziqda turishini kafolatlaydi.

## Ishlash natijasi:
```text
Matn uzunligidan qat'i nazar ikkala tugma ham mutlaqo bir xil pastki gorizontal chiziqda turadi.
```

---

# 637-Topshiriq: Flexboxda ro'yxat tartibini dinamik saralash (order: 0, 1, 2)
## Topshiriq sharti:
Order atributi orqali uchta elementni 3, 1, 2 tartibida qayta joylashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Reorder Elements</title>
  <style>
    .reorder-box {
      display: flex;
      gap: 10px;
      font-family: sans-serif;
    }
    .box { padding: 12px 18px; color: white; border-radius: 4px; }
    .b-first { background: #ef4444; order: 2; }
    .b-second { background: #10b981; order: 3; }
    .b-third { background: #3b82f6; order: 1; }
  </style>
</head>
<body>
  <div class="reorder-box">
    <div class="box b-first">Qizil (1-kodda)</div>
    <div class="box b-second">Yashil (2-kodda)</div>
    <div class="box b-third">Moviy (3-kodda)</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`order: 1` berilgan Moviy blok eng boshiga chiqadi, `order: 2` berilgan Qizil ikkinchi bo'ladi, `order: 3` berilgan Yashil esa eng oxiriga o'tadi.

## Ishlash natijasi:
```text
Ekranda tartib Moviy, Qizil, Yashil ketma-ketligida ko'rinadi.
```

---

# 638-Topshiriq: Flexboxda inline elementlarni tekislash (Badgelar ro'yxati)
## Topshiriq sharti:
Matn qatori ichida inline-flex bilan bezatilgan nishonlarni joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Inline Flex Badges</title>
  <style>
    .badge-inline {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: #e0f2fe;
      color: #0369a1;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-family: sans-serif;
    }
  </style>
</head>
<body>
  <p style="font-family: sans-serif; line-height: 2;">
    Loyiha holati: 
    <span class="badge-inline"><span>&#9679;</span> Faol</span> 
    va server: 
    <span class="badge-inline"><span>&#10003;</span> Barqaror</span>
  </p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: inline-flex` matn oqimini buzmaydi, lekin nishon ichidagi nuqta yoki belgini matn bilan vertikal tekislaydi.

## Ishlash natijasi:
```text
Matn orasida och moviy nishonlar va ularning ichida nuqta hamda qushcha belgilari.
```

---

# 639-Topshiriq: Flexbox bilan moslashuvchan fayl yuklash darchasi (Dropzone)
## Topshiriq sharti:
Katta ikonka, sarlavha va yuklash tugmasini vertikal markazda tartibga soling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Dropzone Flex</title>
  <style>
    .dropzone {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 10px;
      width: 280px;
      height: 160px;
      border: 2px dashed #94a3b8;
      border-radius: 8px;
      background: #f8fafc;
      font-family: sans-serif;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="dropzone">
    <span style="font-size: 32px;">&#128194;</span>
    <strong style="color: #334155;">Fayllarni bu yerga torting</strong>
    <button style="padding: 6px 14px; background: #2563eb; color: white; border: none; border-radius: 4px; cursor: pointer;">Fayl tanlash</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: flex; flex-direction: column; align-items: center; justify-content: center` uchala elementni ramkaning markazida vertikal tizadi.

## Ishlash natijasi:
```text
Punktir ramkali to'rtburchak markazida papka ikonkasi, yozuv va ko'k tugma.
```

---

# 640-Topshiriq: Flexboxda kenglikni cheklovchi max-width bilan moslashuvchanlik
## Topshiriq sharti:
Flex item o'ssin, lekin belgilangan maksimal kenglikdan (masalan 300px) oshib ketmasin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Max-Width</title>
  <style>
    .wrap {
      display: flex;
      background: #f1f5f9;
      padding: 16px;
      font-family: sans-serif;
    }
    .bounded-box {
      flex: 1;
      max-width: 300px;
      background: #4f46e5;
      color: white;
      padding: 12px;
      border-radius: 6px;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="bounded-box">flex: 1 lekin max-width: 300px</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex: 1` elementni o'sishga undaydi, lekin `max-width: 300px` uning ma'lum chegaradan ortiq kengayib ketishiga chek qo'yadi.

## Ishlash natijasi:
```text
Katta ekranda ham to'q ko'k quti 300px dan oshmay to'xtaydi.
```

---

# 641-Topshiriq: Flexboxda izohlar shakli: Avatar chapda, input va tugma o'ngda
## Topshiriq sharti:
Foydalanuvchi yangi sharh qoldirishi uchun ixcham izoh yozish qatorini tuzing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Comment Input Flex</title>
  <style>
    .comment-bar {
      display: flex;
      align-items: center;
      gap: 12px;
      width: 320px;
      font-family: sans-serif;
    }
    .avatar { width: 36px; height: 36px; border-radius: 50%; background: #0284c7; flex-shrink: 0; }
    .input-field {
      flex: 1;
      padding: 8px 12px;
      border: 1px solid #cbd5e1;
      border-radius: 20px;
      outline: none;
    }
  </style>
</head>
<body>
  <div class="comment-bar">
    <div class="avatar"></div>
    <input type="text" class="input-field" placeholder="Fikringizni yozing...">
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`avatar` da `flex-shrink: 0` berilgan, `input-field` esa `flex: 1` orqali butun qatorni egallaydi.

## Ishlash natijasi:
```text
Dumaloq ko'k avatar va uning yonida cho'zilgan oq qidiruvsimon yozuv darchasi.
```

---

# 642-Topshiriq: Flexboxda elementlarni o'zaro teng ikkiga ajratish (50% / 50%)
## Topshiriq sharti:
Ikkita blokni bitta qatorda har biriga teng 50% joy ajratib flex bilan joylashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Split 50-50 Flex</title>
  <style>
    .split-row {
      display: flex;
      gap: 12px;
      font-family: sans-serif;
    }
    .split-item {
      flex: 1 1 0;
      padding: 20px;
      border-radius: 6px;
      color: white;
      text-align: center;
    }
    .c-left { background: #059669; }
    .c-right { background: #0284c7; }
  </style>
</head>
<body>
  <div class="split-row">
    <div class="split-item c-left">Chap tomon (50%)</div>
    <div class="split-item c-right">O'ng tomon (50%)</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex: 1 1 0` har ikkala blokning teng miqdorda 50% kenglik olishini eng toza va xatosiz usulda ta'minlaydi.

## Ishlash natijasi:
```text
Biri yashil, biri ko'k rangli teng ikkita to'rtburchak blok yonma-yon turadi.
```

---

# 643-Topshiriq: Flexboxda vertikal akkordeon sarlavhasi (Ikonka va Strelka)
## Topshiriq sharti:
Savol matni chapda, ochilish strelkasi esa margin-left: auto bilan eng o'ng chetda tursin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Accordion Header Flex</title>
  <style>
    .acc-header {
      display: flex;
      align-items: center;
      width: 280px;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      padding: 10px 14px;
      border-radius: 6px;
      font-family: sans-serif;
      cursor: pointer;
    }
    .arrow { margin-left: auto; color: #64748b; font-size: 14px; }
  </style>
</head>
<body>
  <div class="acc-header">
    <strong>Flexbox qanday ishlaydi?</strong>
    <span class="arrow">&#9660;</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Matndan so'nggi strelkaga `margin-left: auto` berish uni avtomatik o'ng chetga mahkamlaydi.

## Ishlash natijasi:
```text
Chapda qalin savol nomi, o'ngda esa pastga qaragan kichik strelka.
```

---

# 644-Topshiriq: Flexboxda tugmalar blokining gorizontal o'ralishi (Responsive Action Bar)
## Topshiriq sharti:
Ekran torayganda tugmalar siqilmasdan flex-wrap: wrap bilan keyingi qatorga o'tsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Wrap Actions</title>
  <style>
    .action-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      width: 250px;
      background: #f1f5f9;
      padding: 12px;
      font-family: sans-serif;
    }
    .act-btn {
      flex: 1 1 100px;
      padding: 8px;
      background: #3b82f6;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div class="action-bar">
    <button class="act-btn">Eksport</button>
    <button class="act-btn">Import</button>
    <button class="act-btn">Chop etish</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex: 1 1 100px` har bir tugmaga kamida 100px beradi va 250px kenglikda ular 2 tasi yuqorida, uchinchisi esa pastda chiroyli cho'zilib joylashadi.

## Ishlash natijasi:
```text
Tepadagi qatorda ikkita, pastdagi qatorda bitta to'liq cho'zilgan ko'k tugma.
```

---

# 645-Topshiriq: Flexboxda rasm va ikonkalar qatorini baseline tekislash
## Topshiriq sharti:
Har xil balandlikdagi harflar va ikonkalar tagidagi tagchiziqni align-items: baseline orqali tutashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Baseline Row</title>
  <style>
    .base-row {
      display: flex;
      align-items: baseline;
      gap: 8px;
      font-family: sans-serif;
    }
    .big-num { font-size: 32px; font-weight: bold; color: #2563eb; }
    .label { font-size: 14px; color: #64748b; }
  </style>
</head>
<body>
  <div class="base-row">
    <span class="big-num">45</span>
    <span class="label">daqiqada yetkazish</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`align-items: baseline` yirik raqam asosi bilan kichik yozuv asosini optik jihatdan bir chiziqqa keltiradi.

## Ishlash natijasi:
```text
Katta '45' ko'k soni va uning yonidagi kichik yozuvning pastki qirralari tekis turadi.
```

---

# 646-Topshiriq: Flexboxda bitta elementni ikkala o'q bo'yicha markazlashtiruvchi universal quti
## Topshiriq sharti:
Har qanday ikonka yoki raqamni aylana markaziga qo'yish uchun universal flex qolip tayyorlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Universal Center Icon</title>
  <style>
    .icon-badge {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: #fef08a;
      color: #854d0e;
      font-size: 22px;
    }
  </style>
</head>
<body>
  <div class="icon-badge">&#9733;</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: inline-flex; align-items: center; justify-content: center` har qanday belgini o'z doirasining geometrik markaziga qo'yishning eng ishonchli usulidir.

## Ishlash natijasi:
```text
Sariq dumaloq nishon markazida tillarang yulduzcha aks etadi.
```

---

# 647-Topshiriq: Flexboxda mobil ekran uchun vertikal, kompyuter uchun gorizontal tartib
## Topshiriq sharti:
flex-direction ni boshqaruvchi moslashuvchan o'tish mexanizmi tamoyilini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Adaptive Direction</title>
  <style>
    .adaptive-deck {
      display: flex;
      flex-direction: row; /* Katta ekranda row */
      gap: 12px;
      font-family: sans-serif;
    }
    .deck-item {
      flex: 1;
      padding: 16px;
      background: #f1f5f9;
      border-radius: 6px;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="adaptive-deck">
    <div class="deck-item">Blok 1</div>
    <div class="deck-item">Blok 2</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-direction: row` dan `column` ga o'tish orqali butun sahifa maketini osonlikcha mobil va desktop o'rtasida o'zgartirish mumkin.

## Ishlash natijasi:
```text
Ikkita kulrang blok qatorda yonma-yon turadi.
```

---

# 648-Topshiriq: Flexboxda tugmalar guruhi ichida to'liq bo'yicha cho'zilish (Stretch)
## Topshiriq sharti:
align-self: stretch orqali tugmaning qo'shni uzun blok balandligiga tenglashishini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Align Self Stretch</title>
  <style>
    .box-wrap {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      font-family: sans-serif;
    }
    .tall-content {
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      padding: 20px;
      width: 180px;
    }
    .stretch-action {
      align-self: stretch; /* Otaning flex-start ini bekor qilib to'liq cho'ziladi */
      background: #2563eb;
      color: white;
      border: none;
      padding: 0 16px;
      border-radius: 4px;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div class="box-wrap">
    <div class="tall-content">Ushbu blok ancha uzun kontentga ega.</div>
    <button class="stretch-action">Tugma</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ota konteyner `align-items: flex-start` bo'lsa ham, tugmaga `align-self: stretch` berilsa, u qo'shni baland blokning bo'yiga to'liq yetib cho'ziladi.

## Ishlash natijasi:
```text
Ko'k tugma chapdagi baland blok bilan aynan bir xil balandlikka cho'zilib turadi.
```

---

# 649-Topshiriq: Flexboxda chat dialogida xabarlar va vaqt ko'rsatkichi
## Topshiriq sharti:
Xabar matni va kichik vaqt yozuvini bitta xabar pufakchasida flex bilan joylashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Chat Bubble Meta</title>
  <style>
    .bubble {
      display: inline-flex;
      align-items: flex-end;
      gap: 8px;
      background: #dbeafe;
      color: #1e40af;
      padding: 8px 12px;
      border-radius: 12px 12px 0 12px;
      font-family: sans-serif;
      font-size: 14px;
    }
    .time { font-size: 10px; color: #60a5fa; }
  </style>
</head>
<body>
  <div class="bubble">
    <span>Ertaga soat 10:00 da uchrashamiz.</span>
    <span class="time">14:32</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: inline-flex; align-items: flex-end` xabar matnini va pastki o'ng burchakdagi vaqtni Telegram yoki WhatsApp dagi kabi joylashtiradi.

## Ishlash natijasi:
```text
Moviy xabar pufakchasining pastki o'ng chetida kichik '14:32' vaqti aks etadi.
```

---

# 650-Topshiriq: To'liq Dashboard Flexbox Layout (Sidebar, Topbar, KPI Grid va Table)
## Topshiriq sharti:
Faqat flexbox mexanizmidan foydalanib to'liq admin paneli interfeysini shakllantiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Complete Admin Flex</title>
  <style>
    body {
      margin: 0;
      height: 100vh;
      display: flex;
      font-family: sans-serif;
      background: #f8fafc;
    }
    .side-panel {
      flex: 0 0 200px;
      background: #0f172a;
      color: white;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .content-area {
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow-y: auto;
    }
    .top-bar {
      flex: 0 0 50px;
      background: white;
      border-bottom: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
    }
    .dashboard-main {
      flex: 1;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    .kpi-row {
      display: flex;
      gap: 16px;
    }
    .kpi {
      flex: 1;
      background: white;
      padding: 16px;
      border-radius: 8px;
      border: 1px solid #e2e8f0;
    }
  </style>
</head>
<body>
  <aside class="side-panel">
    <h3>AdminPanel</h3>
    <nav>Asosiy</nav>
    <nav>Foydalanuvchilar</nav>
  </aside>
  <div class="content-area">
    <header class="top-bar">
      <span>Dashboard</span>
      <span>Profil</span>
    </header>
    <main class="dashboard-main">
      <div class="kpi-row">
        <div class="kpi">
          <small>Foydalanuvchilar</small>
          <h2>2,450</h2>
        </div>
        <div class="kpi">
          <small>Daromad</small>
          <h2>$18,900</h2>
        </div>
      </div>
    </main>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Tashqi `body` gorizontal flex, ichki `.content-area` vertikal flex, `.kpi-row` esa gorizontal flex qatori bo'lib, butunlay flexboxga asoslangan mukammal Dashboard arxitekturasini hosil qiladi.

## Ishlash natijasi:
```text
Chapda qora menyu, tepada oq navbar va markazda ikkita statistika kartochkasi bilan to'liq admin paneli.
```

---

