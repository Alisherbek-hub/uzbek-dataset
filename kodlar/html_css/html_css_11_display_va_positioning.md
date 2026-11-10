# HTML va CSS: Display va Positioning (Topshiriqlar 501 - 550)

# 501-Topshiriq: Display: block elementlar xususiyatlari va oqim qoidalari
## Topshiriq sharti:
Standart blok (display: block) elementlarning sahifada butun qator kengligini egallashi va yangi qatordan boshlanishi xususiyatini ko'rsatuvchi misol tuzing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Display Block</title>
  <style>
    .block-element {
      display: block;
      background-color: #2563eb;
      color: #ffffff;
      padding: 15px;
      margin-bottom: 12px;
      border-radius: 6px;
      font-family: sans-serif;
    }
  </style>
</head>
<body>
  <div class="block-element">Birinchi blok element (100% enni egallaydi)</div>
  <div class="block-element">Ikkinchi blok element (yangi qatordan chiqadi)</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Blok darajasidagi elementlar (`display: block`) ota elementning butun mavjud kengligini egallaydi va avtomatik tarzda yangi qatordan joylashadi. `width`, `height`, `margin` va `padding` qiymatlari ularda to'liq hisobga olinadi.

## Ishlash natijasi:
```text
Ikkita to'q ko'k rangli to'rtburchak blok butun eni bo'ylab birin-ketin vertikal joylashadi.
```

---

# 502-Topshiriq: Display: inline elementlar va ularning o'lcham chegaralari
## Topshiriq sharti:
Matn ichidagi inline elementlar ketma-ket joylashishi va ularga width/height berilganda ta'sir qilmasligini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Display Inline</title>
  <style>
    .inline-elem {
      display: inline;
      background-color: #fef08a;
      color: #854d0e;
      padding: 4px 8px;
      border: 1px solid #ca8a04;
      font-family: sans-serif;
      /* width va height inline elementlarga ta'sir qilmaydi */
      width: 200px;
      height: 100px;
    }
  </style>
</head>
<body>
  <p style="font-family: sans-serif; line-height: 1.8;">
    Ushbu matnda <span class="inline-elem">inline qism 1</span> va darhol ketidan
    <span class="inline-elem">inline qism 2</span> joylashadi. Eni va bo'yi o'zgarmaydi.
  </p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: inline` elementi faqat o'zining ichidagi kontent hajmini egallaydi va qatorni buzmaydi. Ularga `width`, `height`, yuqori va quyi `margin` qiymatlari ta'sir o'tkazmaydi.

## Ishlash natijasi:
```text
Matn ichida sariq fonli ikkita so'z yonma-yon uzluksiz oqimda turadi, berilgan 200px width inobatga olinmagan.
```

---

# 503-Topshiriq: Display: inline-block elementlar gibrid xususiyati
## Topshiriq sharti:
Elementlar qatorda yonma-yon turishi, lekin ayni paytda alohida width va height qabul qilishi uchun inline-block dan foydalaning.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Display Inline-Block</title>
  <style>
    .card {
      display: inline-block;
      width: 140px;
      height: 90px;
      background-color: #10b981;
      color: white;
      margin: 8px;
      padding: 10px;
      box-sizing: border-box;
      border-radius: 6px;
      font-family: sans-serif;
      vertical-align: top;
    }
  </style>
</head>
<body>
  <div class="card">Karta 1</div>
  <div class="card">Karta 2</div>
  <div class="card">Karta 3</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: inline-block` ikkala xususiyatni birlashtiradi: tashqi tomondan inline kabi yonma-yon oqimda joylashadi, ichki tomondan esa blok kabi kenglik, balandlik va vertikal chekinishlarni to'liq qo'llab-quvvatlaydi.

## Ishlash natijasi:
```text
Yashil rangli 3 ta 140x90px o'lchamli to'rtburchak kartalar bir qatorda yonma-yon teriladi.
```

---

# 504-Topshiriq: Display: none va elementni sahifa oqimidan butunlay o'chirish
## Topshiriq sharti:
Elementni ko'rinmas qilish va u egallagan bo'sh joyni DOM oqimidan to'liq bo'shatish uchun display: none qo'llang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Display None</title>
  <style>
    .box {
      padding: 15px;
      margin: 10px 0;
      font-family: sans-serif;
      border-radius: 5px;
    }
    .box-1 { background-color: #93c5fd; }
    .box-hidden { display: none; background-color: #f87171; }
    .box-2 { background-color: #86efac; }
  </style>
</head>
<body>
  <div class="box box-1">1-Blok: Mavjud va ko'rinadi</div>
  <div class="box box-hidden">Yashirin Blok (display: none)</div>
  <div class="box box-2">2-Blok: Yashirin blok bo'shlig'isiz darhol keyin keladi</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: none` elementni ekrandan va sahifaning geometrik hisob-kitobidan (layout) butunlay olib tashlaydi. U hech qanday bo'sh joy qoldirmaydi va keyingi elementlar uning o'rnini egallaydi.

## Ishlash natijasi:
```text
Moviy va yashil bloklar orasida hech qanday bo'shliqsiz ketma-ket chiqadi, yashirin blok izsiz yo'qolgan.
```

---

# 505-Topshiriq: Visibility: hidden vs display: none solishtirmasi
## Topshiriq sharti:
Visibility: hidden orqali elementni ko'rinmas qilib, lekin uning bo'sh joyini saqlab qolish mexanizmini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Visibility Hidden</title>
  <style>
    .item {
      padding: 15px;
      font-family: sans-serif;
      color: white;
      margin-bottom: 10px;
    }
    .visible-1 { background-color: #3b82f6; }
    .invisible { visibility: hidden; background-color: #ef4444; }
    .visible-2 { background-color: #10b981; }
  </style>
</head>
<body>
  <div class="item visible-1">Ko'rinuvchi blok 1</div>
  <div class="item invisible">Ko'rinmas blok (joyi saqlanadi)</div>
  <div class="item visible-2">Ko'rinuvchi blok 2</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`visibility: hidden` elementni shaffof qiladi, lekin uning egallagan maydoni saqlanib qoladi (oqim buzilmaydi). `display: none` esa elementni maydon bilan birga oqimdan chiqarib tashlaydi.

## Ishlash natijasi:
```text
Blok 1 va Blok 2 o'rtasida bo'sh qolgan oq masofa paydo bo'ladi.
```

---

# 506-Topshiriq: Position: static (Standart oqim holati)
## Topshiriq sharti:
Elementning standart position: static holatida top/left qiymatlari unga ta'sir qilmasligini isbotlovchi misol yozing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Position Static</title>
  <style>
    .static-box {
      position: static;
      top: 50px;
      left: 100px;
      background-color: #e2e8f0;
      border: 2px dashed #64748b;
      padding: 20px;
      font-family: sans-serif;
    }
  </style>
</head>
<body>
  <div class="static-box">
    position: static (standart). top: 50px va left: 100px unga ta'sir qilmaydi!
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Barcha HTML elementlari sukut bo'yicha `position: static` ga ega. Bunday elementlar me'yoriy sahifa oqimida turadi va ularga `top`, `bottom`, `left`, `right` va `z-index` koordinatalari ta'sir qilmaydi.

## Ishlash natijasi:
```text
Kulrang chiziqli quti sahifaning yuqori chap standart burchagidan boshlanadi, surilishlar ishlamaydi.
```

---

# 507-Topshiriq: Position: relative bilan elementni o'z o'rnidan surish
## Topshiriq sharti:
Elementni o'zining tabiiy o'rnidan 25px pastga va 40px o'ngga suring, bunda uning asl o'rni saqlanib qolsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Position Relative</title>
  <style>
    .container {
      background-color: #f1f5f9;
      padding: 20px;
      border: 1px solid #cbd5e1;
      font-family: sans-serif;
    }
    .rel-box {
      position: relative;
      top: 25px;
      left: 40px;
      background-color: #8b5cf6;
      color: white;
      padding: 15px;
      border-radius: 6px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div>Oldingi oddiy matn</div>
    <div class="rel-box">Relative blok (o'z o'rniga nisbatan surilgan)</div>
    <div>Keyingi oddiy matn</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`position: relative` elementni o'zining normal oqimdagi koordinatalariga nisbatan siljitadi. Eng muhimi, elementning avvalgi egallagan joyi oqimda bo'sh qolib, boshqa elementlar uning ustiga yoki ostiga tushmaydi.

## Ishlash natijasi:
```text
Binafsharang blok biroz pastga va o'ngga suriladi, keyingi matn esa u surilmaganidek o'z joyida turaveradi.
```

---

# 508-Topshiriq: Position: relative ota element sifatida (Konteyner vazifasi)
## Topshiriq sharti:
Ota elementga relative berib, uning ichidagi mutlaq elementlar uchun hisoblash koordinata markazi yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Relative Context</title>
  <style>
    .parent-card {
      position: relative;
      width: 280px;
      height: 180px;
      background-color: #f8fafc;
      border: 2px solid #3b82f6;
      border-radius: 8px;
      padding: 15px;
      font-family: sans-serif;
    }
    .child-badge {
      position: absolute;
      top: 10px;
      right: 10px;
      background-color: #ef4444;
      color: white;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 12px;
    }
  </style>
</head>
<body>
  <div class="parent-card">
    <h3>Karta Sarlavhasi</h3>
    <p>Ota element relative bo'lgani uchun burchak nishoni karta ichida qoladi.</p>
    <span class="child-badge">Yangi</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`position: absolute` elementi o'ziga eng yaqin joylashgan `position: static` bo'lmagan ota element burchaklarini koordinata boshi deb hisoblaydi. Shu bois `position: relative` eng keng tarqalgan konteyner vositasidir.

## Ishlash natijasi:
```text
Karta ichida yuqori o'ng burchakda qizil 'Yangi' nishoni aniq joylashadi.
```

---

# 509-Topshiriq: Position: absolute elementni sahifa burchagiga joylashtirish
## Topshiriq sharti:
Hech qanday relative ota bo'lmaganda absolute element to'g'ridan-to'g'ri viewport (body) ga nisbatan joylashishini namoyish eting.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Absolute Viewport</title>
  <style>
    .absolute-pin {
      position: absolute;
      top: 20px;
      right: 20px;
      background-color: #10b981;
      color: white;
      padding: 10px 16px;
      border-radius: 20px;
      font-family: sans-serif;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
  </style>
</head>
<body>
  <div class="absolute-pin">Viewport burchagidagi nishon</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Agar absolute elementning ajdodlarida `position: relative/absolute/fixed` berilmagan bo'lsa, u butun hujjat (initial containing block) koordinatalariga bog'lanadi va `top: 20px; right: 20px` to'g'ridan-to'g'ri sahifa chetidan hisoblanadi.

## Ishlash natijasi:
```text
Brauzer oynasining yuqori o'ng burchagida yashil tugmasimon nishon ko'rinadi.
```

---

# 510-Topshiriq: Position: fixed bilan qotirilgan yuqori navigatsiya paneli (Navbar)
## Topshiriq sharti:
Foydalanuvchi sahifani qancha pastga aylantirmasin, ekranning eng yuqori qismida doim qotib turadigan navbar yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Position Fixed Navbar</title>
  <style>
    body {
      margin: 0;
      padding-top: 60px;
      font-family: sans-serif;
    }
    .fixed-nav {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 50px;
      background-color: #0f172a;
      color: white;
      display: flex;
      align-items: center;
      padding: 0 20px;
      box-sizing: border-box;
      z-index: 1000;
    }
    .content {
      height: 1500px;
      padding: 20px;
      background: linear-gradient(#f8fafc, #cbd5e1);
    }
  </style>
</head>
<body>
  <header class="fixed-nav">
    <strong>EduPortal Navigatsiya</strong>
  </header>
  <main class="content">
    <h2>Skroll qilib ko'ring</h2>
    <p>Navbar o'z o'rnini tark etmaydi va ekranning tepasida mahkamlangan holatda qoladi.</p>
  </main>
</body>
</html>
```

## Tushuntirish va Mantiq:
`position: fixed` elementni butunlay ekran darchasiga (viewport) mahkamlaydi. Hujjat pastga yoki yuqoriga aylantirilganda ham bu element o'z o'rnini o'zgartirmaydi.

## Ishlash natijasi:
```text
Qora fondagi menyu tepada doimiy turadi, pastdagi uzun kontent skroll qilinganda menyu ostidan o'tadi.
```

---

# 511-Topshiriq: Position: sticky bilan skroll qilinganda yopishuvchi bo'lim sarlavhasi
## Topshiriq sharti:
Kontent ichidagi bo'lim sarlavhasi o'z o'rnida turishi, lekin skroll qilinganda ekranning yuqori chetiga borib yopishib qolishini amalga oshiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Position Sticky</title>
  <style>
    body { font-family: sans-serif; margin: 20px; }
    .sticky-header {
      position: sticky;
      top: 0;
      background-color: #f59e0b;
      color: white;
      padding: 12px 16px;
      font-weight: bold;
      border-radius: 4px;
    }
    .article-box {
      height: 800px;
      background-color: #fef3c7;
      padding: 15px;
      margin-bottom: 20px;
    }
  </style>
</head>
<body>
  <p>Oddiy kirish matni bo'lim tepasida...</p>
  <div class="sticky-header">Yopishqoq sarlavha (top: 0)</div>
  <div class="article-box">
    <p>Pastga skroll qilganingizda, yuqoridagi sarlavha ekranning yuqori chetida qoladi.</p>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`position: sticky` gibrid rejimdir: element ma'lum chegaragacha `relative` kabi odatiy oqimda harakatlanadi, belgilangan koordinataga (masalan `top: 0`) yetganda esa o'z ota elementi chegarasi ichida `fixed` kabi qotib turadi.

## Ishlash natijasi:
```text
To'q sariq sarlavha sahifa aylantirilganda ekranning yuqorisiga yetgach yopishib qoladi.
```

---

# 512-Topshiriq: Z-index va qatlamlar iyerarxiyasini boshqarish
## Topshiriq sharti:
Ikkita ustma-ust tushgan elementning qaysi biri tepada ko'rinishini z-index xususiyati orqali hal eting.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Z-Index Asoslari</title>
  <style>
    .layer-container {
      position: relative;
      height: 180px;
      font-family: sans-serif;
    }
    .box {
      position: absolute;
      width: 140px;
      height: 120px;
      padding: 10px;
      color: white;
      border-radius: 8px;
    }
    .box-bottom {
      top: 20px;
      left: 20px;
      background-color: #ef4444;
      z-index: 1;
    }
    .box-top {
      top: 50px;
      left: 60px;
      background-color: #3b82f6;
      z-index: 2;
    }
  </style>
</head>
<body>
  <div class="layer-container">
    <div class="box box-bottom">Qizil (z-index: 1)</div>
    <div class="box box-top">Moviy (z-index: 2)</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`z-index` elementlarning Z o'qi (ekranning chuqurligi) bo'yicha joylashuvini belgilaydi. Yuqoriroq musbat qiymatga ega element pastroq qiymatli element ustiga chiqadi. Muhim: `z-index` faqat pozitsiyalangan (`relative`, `absolute`, `fixed`, `sticky`) elementlarda ishlaydi.

## Ishlash natijasi:
```text
Moviy quti qizil qutining ustini qoplab ko'rinadi.
```

---

# 513-Topshiriq: Stacking Context va z-index ishlamaslik holatini bartaraf etish
## Topshiriq sharti:
Ota elementning stacking konteksti bolaning z-index qiymatini cheklab qo'yishini va uni qanday to'g'rilashni ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Stacking Context</title>
  <style>
    .parent-a {
      position: relative;
      z-index: 1;
      background: #e2e8f0;
      padding: 20px;
      margin-bottom: 20px;
      font-family: sans-serif;
    }
    .child-super {
      position: absolute;
      top: 30px;
      right: 20px;
      background: #dc2626;
      color: white;
      padding: 10px;
      z-index: 9999; /* Ota element z-index: 1 bo'lgani uchun b ning ustiga chiqolmasligi mumkin */
    }
    .parent-b {
      position: relative;
      z-index: 2; /* Yuqori qatlam */
      background: #60a5fa;
      color: white;
      padding: 20px;
      font-family: sans-serif;
    }
  </style>
</head>
<body>
  <div class="parent-a">
    Ota A (z-index: 1)
    <div class="child-super">Bola (z-index: 9999)</div>
  </div>
  <div class="parent-b">
    Ota B (z-index: 2) - Bola z-index 9999 bo'lsa ham Ota B ustiga chiqa olmaydi!
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Stacking Context (qatlamlar muhiti) hosil bo'lgach, uning ichidagi barcha bolalarning `z-index` darajasi faqat shu muhit ichida amal qiladi. Agar Ota elementning z-indexi 1, qo'shni otaning z-indexi 2 bo'lsa, birinchi otaning bolasi z-index: 999999 bo'lsa ham ikkinchi ota ustiga chiqa olmaydi.

## Ishlash natijasi:
```text
Ota B qutisi z-index 9999 bo'lgan qizil bolaning ustini to'sib qoladi.
```

---

# 514-Topshiriq: Inset xususiyati bilan barcha 4 tomon koordinatalarini qisqa yozish
## Topshiriq sharti:
top: 0; right: 0; bottom: 0; left: 0 o'rniga zamonaviy CSS `inset: 0` xususiyatini qo'llab to'liq qoplovchi overlay yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>CSS Inset</title>
  <style>
    .banner {
      position: relative;
      width: 320px;
      height: 180px;
      background-color: #3b82f6;
      border-radius: 8px;
      overflow: hidden;
      font-family: sans-serif;
    }
    .overlay {
      position: absolute;
      inset: 0; /* top: 0, right: 0, bottom: 0, left: 0 ga teng */
      background-color: rgba(15, 23, 42, 0.7);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
    }
  </style>
</head>
<body>
  <div class="banner">
    <div class="overlay">
      <h3>Xush kelibsiz!</h3>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`inset: 0` xususiyati bir vaqtning o'zida `top: 0; right: 0; bottom: 0; left: 0` qiymatlarini belgilovchi zamonaviy shorthand hisoblanadi. U absolut elementni butun ota element maydoniga cho'zish uchun eng qisqa va qulay usuldir.

## Ishlash natijasi:
```text
320x180 o'lchamdagi ko'k to'rtburchak ustiga yarim-shaffof to'q qora qatlam to'liq yopilib, markazida oq matn paydo bo'ladi.
```

---

# 515-Topshiriq: Avatarga onlayn status indikatori (yashil nuqta) ulash
## Topshiriq sharti:
Foydalanuvchi profil rasmining pastki o'ng burchagida position: absolute yordamida yashil status nuqtachasini joylashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Avatar Status</title>
  <style>
    .avatar-wrapper {
      position: relative;
      display: inline-block;
      width: 60px;
      height: 60px;
    }
    .avatar-img {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background-color: #6366f1;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: bold;
      font-family: sans-serif;
    }
    .status-dot {
      position: absolute;
      bottom: 2px;
      right: 2px;
      width: 14px;
      height: 14px;
      background-color: #22c55e;
      border: 2px solid #ffffff;
      border-radius: 50%;
    }
  </style>
</head>
<body>
  <div class="avatar-wrapper">
    <div class="avatar-img">AZ</div>
    <span class="status-dot"></span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Dumaloq avatar o'ralgan `.avatar-wrapper` ga `position: relative` berilib, ichidagi `.status-dot` ga `position: absolute; bottom: 2px; right: 2px` qo'llaniladi. Oq hoshiya esa uni avatar fonidan ajratib turadi.

## Ishlash natijasi:
```text
Dumaloq binafsha rangli 'AZ' profil avatari va uning pastki o'ng qismida oq hoshiyali yashil onlayn nuqtacha ko'rinadi.
```

---

# 516-Topshiriq: Floating Action Button (FAB) suzuvchi harakat tugmasi
## Topshiriq sharti:
Ekranning pastki o'ng burchagida qotib turadigan yumaloq harakat tugmasini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>FAB Button</title>
  <style>
    body { font-family: sans-serif; min-height: 1000px; margin: 20px; }
    .fab-button {
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 56px;
      height: 56px;
      border-radius: 50%;
      background-color: #2563eb;
      color: white;
      border: none;
      font-size: 24px;
      cursor: pointer;
      box-shadow: 0 4px 10px rgba(37, 99, 235, 0.4);
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .fab-button:hover { background-color: #1d4ed8; }
  </style>
</head>
<body>
  <h2>Asosiy sahifa kontenti</h2>
  <p>Sahifani aylantirsangiz ham tugma pastki o'ng burchakda qoladi.</p>
  <button class="fab-button" title="Qo'shish">+</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
`position: fixed; bottom: 24px; right: 24px` qoidasi tugmani har doim ko'rinadigan sohaning pastki o'ng burchagiga mahkamlaydi. Bu mobil va veb ilovalarda asosiy harakat (masalan yangi post yaratish) uchun klassik yechimdir.

## Ishlash natijasi:
```text
Ekranning o'ng quyi burchagida ko'k rangli, soyali doirasimon '+' tugmasi doimiy turadi.
```

---

# 517-Topshiriq: Kartochkada narx va chegirma nishoni (Discount Badge)
## Topshiriq sharti:
Mahsulot kartasining yuqori chap burchagiga qiya yoki burchakli chegirma lentasini absolute orqali joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Discount Badge</title>
  <style>
    .product-card {
      position: relative;
      width: 220px;
      padding: 16px;
      background: white;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      font-family: sans-serif;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .badge {
      position: absolute;
      top: -8px;
      left: -8px;
      background-color: #ef4444;
      color: white;
      font-size: 12px;
      font-weight: bold;
      padding: 4px 8px;
      border-radius: 4px;
      box-shadow: 0 2px 4px rgba(239, 68, 68, 0.3);
    }
  </style>
</head>
<body>
  <div class="product-card">
    <span class="badge">-30%</span>
    <h4>Smartfon X</h4>
    <p>Narxi: 3,500,000 so'm</p>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Karta nisbiy joylashtirilib (`position: relative`), nishon esa manfiy koordinata bilan (`top: -8px; left: -8px`) chiqariladi. Bu zamonaviy e-commerce dizaynlarida nishonni karta hoshiyasidan biroz tashqariga chiqarib ko'rsatish usulidir.

## Ishlash natijasi:
```text
Mahsulot kartasining yuqori chap burchagidan biroz tashqariga chiqib turgan qizil '-30%' nishoni ko'rinadi.
```

---

# 518-Topshiriq: CSS Tooltip (Ko'rsatma darchasi) yaratish
## Topshiriq sharti:
Tugma ustiga sichqoncha olib kelinganda uning tepasida paydo bo'ladigan tooltip yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>CSS Tooltip</title>
  <style>
    .tooltip-wrapper {
      position: relative;
      display: inline-block;
      margin: 60px 40px;
      font-family: sans-serif;
    }
    .tooltip-box {
      visibility: hidden;
      opacity: 0;
      position: absolute;
      bottom: 125%;
      left: 50%;
      transform: translateX(-50%);
      background-color: #1e293b;
      color: #fff;
      padding: 6px 10px;
      border-radius: 4px;
      font-size: 13px;
      white-space: nowrap;
      transition: opacity 0.2s;
    }
    .tooltip-wrapper:hover .tooltip-box {
      visibility: visible;
      opacity: 1;
    }
  </style>
</head>
<body>
  <div class="tooltip-wrapper">
    <button style="padding: 10px 16px; cursor: pointer;">Menga bosing</button>
    <div class="tooltip-box">Foydali maslahat matni!</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Tooltip ota elementga nisbatan `position: absolute; bottom: 125%; left: 50%; transform: translateX(-50%)` orqali markazlashtiriladi. Hover bo'lganda `visibility: visible` va `opacity: 1` orqali silliq namoyon bo'ladi.

## Ishlash natijasi:
```text
Tugma ustiga kelganda uning ustki qismida to'q kulrang maslahat qutisi chiqadi.
```

---

# 519-Topshiriq: Modal darcha qobig'i (Overlay va markaziy darcha)
## Topshiriq sharti:
Butun ekranni xiralashtiruvchi fixed overlay va uning markazida joylashgan modal oynani yasang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Modal Overlay</title>
  <style>
    .modal-overlay {
      position: fixed;
      inset: 0;
      background-color: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 9999;
      font-family: sans-serif;
    }
    .modal-content {
      background: white;
      padding: 24px;
      border-radius: 8px;
      width: 320px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }
  </style>
</head>
<body>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3 style="margin-top: 0;">Ogohlantirish</h3>
      <p>Amalni bajarishni tasdiqlaysizmi?</p>
      <button style="padding: 8px 16px; background: #2563eb; color: white; border: none; border-radius: 4px;">Ha, tasdiqlash</button>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`modal-overlay` ekranga `position: fixed; inset: 0` bilan qotirilib, fon yarim qora qilinadi va `z-index: 9999` orqali barcha qatlamlardan yuqoriga chiqariladi. Ichki darcha esa uning markazida render qilinadi.

## Ishlash natijasi:
```text
Butun ekran qoramtir pardalanib, o'rtada oq fonli toza ogohlantirish oynasi ochilgan holda turadi.
```

---

# 520-Topshiriq: Scroll to Top (Tepaga qaytish) tugmasi
## Topshiriq sharti:
Ekran pastki chap burchagida qotib turuvchi yumaloq yuqoriga qaytish tugmasini joylashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Back to Top</title>
  <style>
    body { height: 1200px; font-family: sans-serif; margin: 20px; }
    .scroll-top-btn {
      position: fixed;
      bottom: 20px;
      left: 20px;
      width: 44px;
      height: 44px;
      background-color: #334155;
      color: white;
      border-radius: 50%;
      text-decoration: none;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
  </style>
</head>
<body>
  <h2>Uzun maqola sahifasi</h2>
  <a href="#" class="scroll-top-btn" title="Tepaga">&#8593;</a>
</body>
</html>
```

## Tushuntirish va Mantiq:
Fixed joylashuvli anhor havola (`href='#'`) `bottom: 20px; left: 20px` da turadi. Foydalanuvchi sahifani qancha pastga sursa ham tugma shu burchakda turib, bosilganda boshlang'ich nuqtaga qaytaradi.

## Ishlash natijasi:
```text
Ekranning chap quyi burchagida yuqoriga qaratilgan strelkali doira qotib turadi.
```

---

# 521-Topshiriq: Notification Badge (Bildirishnoma qizil raqamchasi)
## Topshiriq sharti:
Qo'ng'iroqcha ikonkasining yuqori o'ng burchagida o'qilmagan xabarlar sonini ko'rsatuvchi raqamli badge joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Notification Badge</title>
  <style>
    .bell-btn {
      position: relative;
      display: inline-block;
      padding: 12px;
      background-color: #f1f5f9;
      border-radius: 8px;
      font-size: 20px;
      border: none;
      cursor: pointer;
    }
    .badge-count {
      position: absolute;
      top: -4px;
      right: -4px;
      background-color: #ef4444;
      color: white;
      font-size: 11px;
      font-family: sans-serif;
      font-weight: bold;
      min-width: 18px;
      height: 18px;
      border-radius: 9px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 2px solid white;
    }
  </style>
</head>
<body>
  <div class="bell-btn">
    &#128276;
    <span class="badge-count">5</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Tugmaga `position: relative` berilib, raqamli doiraga `position: absolute; top: -4px; right: -4px` ko'rsatiladi. Bu orqali badge tugma chegarasini qisman qoplaydi va diqqatni tortadi.

## Ishlash natijasi:
```text
Qo'ng'iroqcha ikonkasi ustki o'ng chetida oq hoshiyali qizil '5' raqami aks etadi.
```

---

# 522-Topshiriq: Dropdown menyuni relative va absolute orqali shakllantirish
## Topshiriq sharti:
Navigatsiya elementi bosilganda yoki hover qilinganda ostidan chiqadigan dropdown menyu yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Dropdown Menu</title>
  <style>
    .menu-item {
      position: relative;
      display: inline-block;
      font-family: sans-serif;
    }
    .menu-btn {
      background: #0284c7;
      color: white;
      padding: 10px 16px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    .dropdown-content {
      display: none;
      position: absolute;
      top: 100%;
      left: 0;
      background-color: white;
      min-width: 160px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      border-radius: 4px;
      overflow: hidden;
      z-index: 10;
    }
    .dropdown-content a {
      color: #333;
      padding: 10px 14px;
      text-decoration: none;
      display: block;
    }
    .dropdown-content a:hover { background-color: #f0f9ff; }
    .menu-item:hover .dropdown-content { display: block; }
  </style>
</head>
<body>
  <div class="menu-item">
    <button class="menu-btn">Xizmatlar &#9662;</button>
    <div class="dropdown-content">
      <a href="#">Veb-dizayn</a>
      <a href="#">Dasturlash</a>
      <a href="#">SEO tahlil</a>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ota element `position: relative`, ichki ro'yxat esa `position: absolute; top: 100%; left: 0` qilib belgilanadi. `top: 100%` ro'yxatni tugmaning to'g'ridan-to'g'ri tagidan boshlanishini ta'minlaydi.

## Ishlash natijasi:
```text
'Xizmatlar' tugmasi ustiga sichqoncha borganda pastga qarab 3 ta bandli menyu ochiladi.
```

---

# 523-Topshiriq: Position: sticky bilan yopishuvchi yon panel (Sticky Sidebar)
## Topshiriq sharti:
Uzun blog sahifasida o'ng tomondagi vidjet panelini ekranda siljib ketmasdan ushlab turishni yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Sticky Sidebar</title>
  <style>
    .layout {
      display: flex;
      gap: 20px;
      font-family: sans-serif;
      margin: 20px;
    }
    .main-content {
      flex: 3;
      height: 1200px;
      background-color: #f1f5f9;
      padding: 20px;
    }
    .sidebar {
      flex: 1;
    }
    .sticky-widget {
      position: sticky;
      top: 20px;
      background: white;
      border: 1px solid #cbd5e1;
      padding: 16px;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <div class="layout">
    <main class="main-content">
      <h2>Katta Maqola Matni</h2>
      <p>Sahifani pastga skroll qiling va yon panelni kuzating...</p>
    </main>
    <aside class="sidebar">
      <div class="sticky-widget">
        <h4>O'xshash maqolalar</h4>
        <p>Ushbu panel skroll paytida yuqoridan 20px masofada to'xtab turadi.</p>
      </div>
    </aside>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Sidebar ichidagi qutiga `position: sticky; top: 20px` berilgan. U o'z ota ustunining chegarasi bo'yicha harakatlanadi va foydalanuvchi asosiy maqolani o'qiyotganda qulay ko'rinib turadi.

## Ishlash natijasi:
```text
Asosiy maqola pastga skroll qilinganda o'ngdagi vidjet ekranning yuqorisidan 20px pastda qotib turadi.
```

---

# 524-Topshiriq: Rasm ustiga qoplangan sarlavha va gradient (Card Overlay)
## Topshiriq sharti:
Karta fonidagi rasm ustiga absolut joylashuv orqali matnli qora gradient tushiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Image Card Overlay</title>
  <style>
    .card-photo {
      position: relative;
      width: 280px;
      height: 200px;
      background: #64748b;
      border-radius: 8px;
      overflow: hidden;
      font-family: sans-serif;
    }
    .card-gradient {
      position: absolute;
      inset: 0;
      background: linear-gradient(to top, rgba(0,0,0,0.85) 0%, transparent 60%);
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      padding: 16px;
      color: white;
    }
  </style>
</head>
<body>
  <div class="card-photo">
    <div class="card-gradient">
      <h3 style="margin: 0 0 4px 0;">Samarqand Manzarasi</h3>
      <p style="margin: 0; font-size: 13px; color: #cbd5e1;">Tarixiy obidalar siri</p>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Karta konteyneriga `overflow: hidden; position: relative` berilib, gradient qatlami `position: absolute; inset: 0` bilan butun maydonni qoplaydi va `justify-content: flex-end` bilan matnni pastga tushiradi.

## Ishlash natijasi:
```text
To'rtburchak kartaning pastki qismida qoramtir gradient ustida oq rangli sarlavha ko'rinadi.
```

---

# 525-Topshiriq: Custom Toggle Switch tugmachasi joylashuvi
## Topshiriq sharti:
Relative va absolute yordamida zamonaviy yoqish/o'chirish (toggle switch) elementini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Toggle Switch</title>
  <style>
    .switch {
      position: relative;
      display: inline-block;
      width: 50px;
      height: 26px;
    }
    .switch input { opacity: 0; width: 0; height: 0; }
    .slider {
      position: absolute;
      inset: 0;
      background-color: #cbd5e1;
      border-radius: 26px;
      cursor: pointer;
      transition: 0.3s;
    }
    .slider::before {
      position: absolute;
      content: "";
      height: 20px;
      width: 20px;
      left: 3px;
      bottom: 3px;
      background-color: white;
      border-radius: 50%;
      transition: 0.3s;
    }
    input:checked + .slider { background-color: #3b82f6; }
    input:checked + .slider::before { transform: translateX(24px); }
  </style>
</head>
<body>
  <label class="switch">
    <input type="checkbox" checked>
    <span class="slider"></span>
  </label>
</body>
</html>
```

## Tushuntirish va Mantiq:
Yashirin checkbox ustiga o'ralgan `.slider` mutlaq joylashtiriladi, uning ichki dumaloq tugmasi esa `::before` orqali `transform: translateX` bilan o'ngga suriladi.

## Ishlash natijasi:
```text
Ko'k fondagi o'ng tomonga surilgan oq dumaloqli zamonaviy yoqilgan switch tugmasi paydo bo'ladi.
```

---

# 526-Topshiriq: Display: contents va konteyner chegarasini bekor qilish
## Topshiriq sharti:
Display: contents orqali elementning o'zini qutisini yo'q qilib, uning bolalarini to'g'ridan-to'g'ri ota grid/flex ga ulash usulini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Display Contents</title>
  <style>
    .grid-parent {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      font-family: sans-serif;
    }
    .wrapper-phantom {
      display: contents; /* wrapper o'z qutisini yo'qotadi, bolalari to'g'ridan-to'g'ri grid a'zosi bo'ladi */
    }
    .box {
      background: #0ea5e9;
      color: white;
      padding: 15px;
      text-align: center;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="grid-parent">
    <div class="box">1</div>
    <div class="wrapper-phantom">
      <div class="box">2 (ichki)</div>
      <div class="box">3 (ichki)</div>
    </div>
    <div class="box">4</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: contents` elementning o'zining chegarasini, foni va marginlarini DOM vizual daraxtidan olib tashlaydi, natijada uning ichidagi barcha bolalari bevosita bobo konteynerning bevosita farzandi kabi joylashadi.

## Ishlash natijasi:
```text
Garchi 2 va 3 alohida o'ram ichida bo'lsa ham, ular 1 va 4 bilan bir xil grid ustunlariga teng taqsimlanadi.
```

---

# 527-Topshiriq: Display: flow-root bilan clearfix muammosini hal qilish
## Topshiriq sharti:
Float elementlar ota qutidan chiqib ketishini to'xtatuvchi zamonaviy display: flow-root vositasidan foydalaning.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Display Flow-Root</title>
  <style>
    .container {
      display: flow-root; /* Yangi BFC yaratadi va float elementlarni ichida ushlab qoladi */
      background-color: #f1f5f9;
      border: 2px solid #94a3b8;
      padding: 15px;
      font-family: sans-serif;
    }
    .floating-img {
      float: left;
      width: 100px;
      height: 80px;
      background-color: #f97316;
      margin-right: 15px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="floating-img"></div>
    <p>Ushbu matn float qilingan element yonida oqib o'tadi. display: flow-root tufayli ota quti to'liq balandlikni hisoblaydi.</p>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: flow-root` yangi Block Formatting Context (BFC) hosil qiladi. U eskirgan `clearfix` hiylalari (`::after { clear: both }`) o'rniga zamonaviy va xavfsiz standart hisoblanadi.

## Ishlash natijasi:
```text
Ota blok to'q sariq float elementni o'z ichiga to'liq qamrab olib, hoshiya balandligini to'g'ri o'rab turadi.
```

---

# 528-Topshiriq: Absolute elementni ikkala o'q bo'yicha aniq markazlashtirish (Transform usuli)
## Topshiriq sharti:
Konteyner ichidagi qutini top: 50%; left: 50%; transform: translate(-50%, -50%) orqali markazlashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Absolute Center</title>
  <style>
    .parent {
      position: relative;
      width: 300px;
      height: 200px;
      background-color: #e0f2fe;
      border: 2px dashed #0284c7;
      font-family: sans-serif;
    }
    .centered-box {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background-color: #0284c7;
      color: white;
      padding: 12px 20px;
      border-radius: 6px;
    }
  </style>
</head>
<body>
  <div class="parent">
    <div class="centered-box">Aniq Markaz</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`top: 50%; left: 50%` elementning yuqori chap nuqtasini markazga olib keladi. `transform: translate(-50%, -50%)` esa elementni o'zining eni va bo'yining yarmi miqdorida orqaga surib, mukammal geometrik markazlashtiradi.

## Ishlash natijasi:
```text
Moviy quti tashqi ramkaning qoq o'rtasida har ikkala o'q bo'yicha markazlashgan.
```

---

# 529-Topshiriq: Margin: auto orqali absolute elementni to'liq markazlashtirish
## Topshiriq sharti:
top: 0, bottom: 0, left: 0, right: 0 va margin: auto yordamida o'lchamli absolute qutini markazlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Absolute Margin Auto</title>
  <style>
    .stage {
      position: relative;
      width: 320px;
      height: 180px;
      background-color: #f3e8ff;
      border-radius: 8px;
      font-family: sans-serif;
    }
    .modal-box {
      position: absolute;
      inset: 0;
      margin: auto;
      width: 160px;
      height: 80px;
      background-color: #7e22ce;
      color: white;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  </style>
</head>
<body>
  <div class="stage">
    <div class="modal-box">Margin Auto</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Barcha to'rt tomondan `inset: 0` berilgan va aniq `width` hamda `height` ga ega mutlaq elementda `margin: auto` qolgan bo'shliqlarni to'rt tomondan teng taqsimlab, markazlashtirish hosil qiladi.

## Ishlash natijasi:
```text
Binafsha rangli quti och binafsharang maydonning markazida joylashadi.
```

---

# 530-Topshiriq: Isolate xususiyati va yangi stacking context hosil qilish
## Topshiriq sharti:
CSS isolation: isolate orqali z-index elementlarning tashqi sahifaga oqib ketishini cheklovchi lokal qatlam yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>CSS Isolation</title>
  <style>
    .card-isolated {
      isolation: isolate; /* Yangi stacking context yaratadi */
      position: relative;
      background-color: #ffffff;
      border: 1px solid #e2e8f0;
      padding: 20px;
      border-radius: 8px;
      font-family: sans-serif;
      box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .deco-bg {
      position: absolute;
      inset: 0;
      background-color: #eff6ff;
      z-index: -1; /* Ota kartaning o'z fonidan pastga emas, isolation tufayli uning ichida qoladi */
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <div class="card-isolated">
    <div class="deco-bg"></div>
    <h3>Izolyatsiyalangan Karta</h3>
    <p>z-index: -1 element kartaning orqasiga ketib qolmaydi, faqat matn ostida qoladi.</p>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`isolation: isolate` qoidasi element uchun yangi stacking context ochadi. Bu `z-index: -1` berilgan dekorativ elementlarning butun ota blok foni orqasiga yashirinib qolmasligini ta'minlaydi.

## Ishlash natijasi:
```text
Oq fonli karta ichidagi moviy bezak qatlami matn ostida, lekin kartaning o'zida saqlanadi.
```

---

# 531-Topshiriq: Accordion menyuda panelni yashirish va ochish mexanizmi
## Topshiriq sharti:
CSS display xususiyatini o'zgartirish orqali ochiluvchi/yopiluvchi FAQ paneli hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Accordion Toggle</title>
  <style>
    .faq-item {
      font-family: sans-serif;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      width: 320px;
      overflow: hidden;
    }
    .faq-title {
      background: #f8fafc;
      padding: 12px 16px;
      font-weight: bold;
      cursor: pointer;
    }
    .faq-body {
      display: none;
      padding: 14px 16px;
      background: white;
      border-top: 1px solid #cbd5e1;
    }
    /* Hover yoki sinov uchun ko'rsatish */
    .faq-item:hover .faq-body {
      display: block;
    }
  </style>
</head>
<body>
  <div class="faq-item">
    <div class="faq-title">Kurs qancha davom etadi?</div>
    <div class="faq-body">Kurs davomiyligi 3 oy bo'lib, haftasiga 3 ta dars o'tiladi.</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: none` holatida element xotirada mavjud bo'lsa-da ekranda ko'rinmaydi. Foydalanuvchi amal bajarganda (hover yoki sinf qo'shilganda) `display: block` ga o'tkazilib ochiladi.

## Ishlash natijasi:
```text
Savol ustiga kursor olib kelinganda pastdan javob bloki yoyilib ochiladi.
```

---

# 532-Topshiriq: Rasm galereyasida hover paytida kattalashuvchi ko'rish ikonkasi
## Topshiriq sharti:
Rasm kartasi ustiga sichqoncha kelganda paydo bo'luvchi qidiruv ikonkasi va qora parda overlayini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Gallery Overlay</title>
  <style>
    .thumb-box {
      position: relative;
      width: 240px;
      height: 160px;
      background-color: #38bdf8;
      border-radius: 8px;
      overflow: hidden;
      cursor: pointer;
      font-family: sans-serif;
    }
    .overlay-view {
      position: absolute;
      inset: 0;
      background-color: rgba(0, 0, 0, 0.4);
      display: flex;
      align-items: center;
      justify-content: center;
      opacity: 0;
      transition: opacity 0.3s;
      color: white;
      font-size: 28px;
    }
    .thumb-box:hover .overlay-view {
      opacity: 1;
    }
  </style>
</head>
<body>
  <div class="thumb-box">
    <div class="overlay-view">&#128269;</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`overlay-view` `position: absolute; inset: 0` orqali butun rasm ustiga yoyiladi. Sukutda `opacity: 0` bo'lib, `:hover` da `opacity: 1` ga o'zgaradi.

## Ishlash natijasi:
```text
Moviy kartochka ustiga sichqoncha borganda qoramtir fonda lupa ikonkasi silliq chiqadi.
```

---

# 533-Topshiriq: Chat ilovasida pastki qismdagi xabar yozish qutisi (Fixed Chat Input)
## Topshiriq sharti:
Mobil chat interfeysida xabarlar qancha bo'lmasin, yozish qutisi har doim ekranning pastki qismida qotib turishini ta'minlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Fixed Chat Input</title>
  <style>
    body { margin: 0; padding-bottom: 70px; font-family: sans-serif; background: #f8fafc; }
    .chat-messages { padding: 16px; }
    .msg { background: white; padding: 10px 14px; border-radius: 8px; margin-bottom: 10px; width: fit-content; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .chat-bottom-bar {
      position: fixed;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 60px;
      background-color: white;
      border-top: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      padding: 0 16px;
      box-sizing: border-box;
      gap: 10px;
    }
    .chat-input {
      flex: 1;
      padding: 10px;
      border: 1px solid #cbd5e1;
      border-radius: 20px;
      outline: none;
    }
  </style>
</head>
<body>
  <div class="chat-messages">
    <div class="msg">Salom! Dars soat nechada?</div>
    <div class="msg">Assalomu alaykum! Soat 15:00 da boshlanadi.</div>
  </div>
  <div class="chat-bottom-bar">
    <input type="text" class="chat-input" placeholder="Xabar yozing...">
    <button style="padding: 8px 16px; background: #3b82f6; color: white; border: none; border-radius: 20px;">Yuborish</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`chat-bottom-bar` ga `position: fixed; bottom: 0; left: 0; width: 100%` beriladi. Sahifa pastiga yozuv panelining balandligiga teng `padding-bottom: 70px` berilib, so'nggi xabarlar uning orqasida ko'rinmay qolishi oldi olinadi.

## Ishlash natijasi:
```text
Ekranning tagida oppoq rangli xabar yozish maydoni va tugmasi doimiy turadi.
```

---

# 534-Topshiriq: Position: sticky bilan yopishuvchi jadval sarlavhasi (Sticky Table Header)
## Topshiriq sharti:
Uzun ma'lumotlar jadvalida pastga skroll qilinganda <thead> ustun nomlari tepada yopishib turishini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Sticky Table Header</title>
  <style>
    .table-container {
      max-height: 200px;
      overflow-y: auto;
      border: 1px solid #cbd5e1;
      font-family: sans-serif;
    }
    table { width: 100%; border-collapse: collapse; }
    th {
      position: sticky;
      top: 0;
      background-color: #1e293b;
      color: white;
      padding: 10px;
      text-align: left;
      z-index: 2;
    }
    td { padding: 8px 10px; border-bottom: 1px solid #e2e8f0; }
  </style>
</head>
<body>
  <div class="table-container">
    <table>
      <thead>
        <tr><th>ID</th><th>Ism</th><th>Kasb</th></tr>
      </thead>
      <tbody>
        <tr><td>1</td><td>Aziz</td><td>Dasturchi</td></tr>
        <tr><td>2</td><td>Malika</td><td>Dizayner</td></tr>
        <tr><td>3</td><td>Jamshid</td><td>Menejer</td></tr>
        <tr><td>4</td><td>Sardor</td><td>DevOps</td></tr>
        <tr><td>5</td><td>Nilufar</td><td>QA Muhandis</td></tr>
      </tbody>
    </table>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<th>` kataklariga `position: sticky; top: 0` beriladi. Ota `.table-container` da `overflow-y: auto` bo'lganda, jadval aylantirilganda sarlavha qatori darchaning tepasida qotib qoladi.

## Ishlash natijasi:
```text
Jadval 200px darchada pastga surilganda to'q rangli ustun nomlari tepada qimirlamay turadi.
```

---

# 535-Topshiriq: Video ustiga Play (Ijro) tugmasini markazlashtirib qo'yish
## Topshiriq sharti:
Video pleer oynasining qoq o'rtasida shaffof dumaloq Play tugmasini absolute yordamida joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Video Play Button</title>
  <style>
    .video-preview {
      position: relative;
      width: 320px;
      height: 180px;
      background-color: #0f172a;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
    }
    .play-btn {
      position: absolute;
      width: 56px;
      height: 56px;
      background-color: rgba(255, 255, 255, 0.2);
      border: 2px solid white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 24px;
      transition: transform 0.2s, background-color 0.2s;
    }
    .video-preview:hover .play-btn {
      transform: scale(1.15);
      background-color: rgba(239, 68, 68, 0.9);
      border-color: #ef4444;
    }
  </style>
</head>
<body>
  <div class="video-preview">
    <div class="play-btn">&#9658;</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Play tugmasi ota qutining markazida turadi va hover bo'lganda `transform: scale(1.15)` bilan qizil rangda kattalashib chiroyli mikro-animatsiya hosil qiladi.

## Ishlash natijasi:
```text
Qora fonli to'rtburchak o'rtasida oq uchburchakli Play doirasi aks etadi.
```

---

# 536-Topshiriq: Sticky Footer (Pastki yopishuvchi qism)
## Topshiriq sharti:
Sahifa kontenti kam bo'lsa ham footer ekranning eng tagida turishini ta'minlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Sticky Footer</title>
  <style>
    html, body { height: 100%; margin: 0; }
    .site-wrapper {
      min-height: 100%;
      display: flex;
      flex-direction: column;
      font-family: sans-serif;
    }
    .page-content { flex: 1; padding: 20px; }
    footer {
      background-color: #0f172a;
      color: #94a3b8;
      text-align: center;
      padding: 16px;
    }
  </style>
</head>
<body>
  <div class="site-wrapper">
    <main class="page-content">
      <h2>Qisqa kontentli sahifa</h2>
      <p>Bu yerda matn juda oz bo'lsa ham footer ekranning eng pastiga tushadi.</p>
    </main>
    <footer>&copy; 2026 Barcha huquqlar himoyalangan.</footer>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Flexbox va `min-height: 100%` orqali asosiy kontentga `flex: 1` berilib, footer avtomatik tarzda oynaning tubiga itariladi.

## Ishlash natijasi:
```text
Kam matnli sahifada ham to'q rangli footer brauzer oynasining tubida mustahkam turadi.
```

---

# 537-Topshiriq: Yuklanish indikatori (Loading Spinner) overlay
## Topshiriq sharti:
Butun blok ustiga yarim shaffof oq parda va uning markazida aylanuvchi spinner joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Loading Overlay</title>
  <style>
    .card-loading {
      position: relative;
      width: 260px;
      padding: 20px;
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      font-family: sans-serif;
    }
    .loading-shield {
      position: absolute;
      inset: 0;
      background: rgba(255, 255, 255, 0.8);
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 8px;
      z-index: 5;
    }
    .spinner {
      width: 32px;
      height: 32px;
      border: 4px solid #e2e8f0;
      border-top-color: #2563eb;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
  </style>
</head>
<body>
  <div class="card-loading">
    <div class="loading-shield">
      <div class="spinner"></div>
    </div>
    <h3>Foydalanuvchi ma'lumotlari</h3>
    <p>Yuklanmoqda...</p>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`loading-shield` `position: absolute; inset: 0` orqali kartani to'liq to'sadi, foydalanuvchini chalg'itmaydi va markazda aylana spinner ko'rsatiladi.

## Ishlash natijasi:
```text
Kartochka ustida xira oq qatlam va uning markazida tinimsiz aylanayotgan ko'k halqa ko'rinadi.
```

---

# 538-Topshiriq: Ko'p darajali qatlamlar (3 qatlamli karta kolleksiyasi)
## Topshiriq sharti:
Z-index orqali 3 ta kartaning bir-birining ustiga ketma-ket taxlanib turishi effektini hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Stacked Cards</title>
  <style>
    .stack-wrapper {
      position: relative;
      width: 220px;
      height: 140px;
      margin: 40px auto;
      font-family: sans-serif;
    }
    .stacked-card {
      position: absolute;
      width: 100%;
      height: 100%;
      border-radius: 8px;
      padding: 12px;
      box-sizing: border-box;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .card-c { top: 16px; left: 16px; background: #93c5fd; z-index: 1; }
    .card-b { top: 8px; left: 8px; background: #60a5fa; z-index: 2; }
    .card-a { top: 0; left: 0; background: #2563eb; color: white; z-index: 3; }
  </style>
</head>
<body>
  <div class="stack-wrapper">
    <div class="stacked-card card-c">Orqa qatlam</div>
    <div class="stacked-card card-b">O'rta qatlam</div>
    <div class="stacked-card card-a">Eng yuqori qatlam</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Har bir kartaga mutanosib `top`, `left` siljishi va ortib boruvchi `z-index` (1, 2, 3) berilib, jildlar yoki qog'ozlar to'plami effekti vujudga keltiriladi.

## Ishlash natijasi:
```text
3 ta moviy rangli to'rtburchak karta bir-birining ortidan ko'rinib taxlangan holda turadi.
```

---

# 539-Topshiriq: Sidebar navigatsiyasida aktiv bo'lim indikatori chizig'i
## Topshiriq sharti:
Tanlangan menyu bandining chap tomoniga absolute yordamida vertikal ko'k chiziqcha qo'ying.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Active Sidebar Line</title>
  <style>
    .sidebar-menu {
      width: 200px;
      background: white;
      border: 1px solid #e2e8f0;
      font-family: sans-serif;
      border-radius: 6px;
    }
    .menu-link {
      position: relative;
      display: block;
      padding: 12px 18px;
      color: #64748b;
      text-decoration: none;
    }
    .menu-link.active {
      color: #2563eb;
      font-weight: bold;
      background-color: #eff6ff;
    }
    .menu-link.active::before {
      content: "";
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 4px;
      background-color: #2563eb;
      border-radius: 0 2px 2px 0;
    }
  </style>
</head>
<body>
  <div class="sidebar-menu">
    <a href="#" class="menu-link active">Bosh sahifa</a>
    <a href="#" class="menu-link">Statistika</a>
    <a href="#" class="menu-link">Sozlamalar</a>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Aktiv menyu bandining `::before` soxta elementiga `position: absolute; left: 0; top: 0; bottom: 0; width: 4px` berish orqali chap tomonda toza vertikal chiziq hosil qilinadi.

## Ishlash natijasi:
```text
Faol menyu bandining chap tomonida 4px enli ko'k rangli vertikal chiziqcha paydo bo'ladi.
```

---

# 540-Topshiriq: Sticky Navbar ichida qisqaruvchi logo va soya effekti
## Topshiriq sharti:
Yuqorida sticky turgan navbarga pastki yumshoq chegara va soya berib, skroll qilinganda ajralib turishini ta'minlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Sticky Navbar Shadow</title>
  <style>
    body { margin: 0; font-family: sans-serif; height: 1200px; }
    .top-bar {
      position: sticky;
      top: 0;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid rgba(0, 0, 0, 0.08);
      padding: 14px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 4px 12px rgba(0,0,0,0.05);
      z-index: 100;
    }
  </style>
</head>
<body>
  <header class="top-bar">
    <div style="font-weight: bold; color: #1e293b;">Logotip</div>
    <nav>Bosh sahifa | Xizmatlar | Aloqa</nav>
  </header>
  <main style="padding: 24px;">
    <h2>Asosiy Kontent</h2>
    <p>Skroll qilinganda navbar xira oq shisha fonida tepada mustahkam turadi.</p>
  </main>
</body>
</html>
```

## Tushuntirish va Mantiq:
`position: sticky; top: 0` va `backdrop-filter: blur(8px)` kombinatsiyasi zamonaviy qotib turuvchi panellarda ostidagi kontentni xiralashtirib o'tkazish imkonini beradi.

## Ishlash natijasi:
```text
Oq yarim shaffof navigatsiya paneli sahifa aylanganda tepada qolib, ostidagi matnni xiralashtirib ko'rsatadi.
```

---

# 541-Topshiriq: Custom Radio Button dizayni (Absolute qoplama)
## Topshiriq sharti:
Brauzerning standart radio inputini yashirib, absolute yordamida stil berilgan radio tugma yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Custom Radio</title>
  <style>
    .radio-label {
      position: relative;
      padding-left: 28px;
      cursor: pointer;
      font-family: sans-serif;
      display: inline-block;
      user-select: none;
    }
    .radio-label input {
      position: absolute;
      opacity: 0;
      cursor: pointer;
    }
    .custom-circle {
      position: absolute;
      top: 0;
      left: 0;
      height: 18px;
      width: 18px;
      background-color: white;
      border: 2px solid #94a3b8;
      border-radius: 50%;
    }
    .radio-label input:checked ~ .custom-circle {
      border-color: #2563eb;
    }
    .radio-label input:checked ~ .custom-circle::after {
      content: "";
      position: absolute;
      top: 3px;
      left: 3px;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #2563eb;
    }
  </style>
</head>
<body>
  <label class="radio-label">
    Variant A
    <input type="radio" name="option" checked>
    <span class="custom-circle"></span>
  </label>
</body>
</html>
```

## Tushuntirish va Mantiq:
Standart radio input shaffof qilib `.custom-circle` ustiga qo'yiladi. Tanlanganda `::after` orqali markazda 8px li ko'k ichki doira hosil bo'ladi.

## Ishlash natijasi:
```text
Chiroyli ko'k hoshiyali va ichida to'q ko'k nuqtasi bo'lgan radio tugma paydo bo'ladi.
```

---

# 542-Topshiriq: Yopishuvchi jadvalning birinchi ustuni (Sticky First Column)
## Topshiriq sharti:
Gorizontal skroll bo'ladigan keng jadvalda chap tomondagi ID ustunini qotirib qo'ying.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Sticky Column</title>
  <style>
    .scroll-table {
      width: 320px;
      overflow-x: auto;
      border: 1px solid #cbd5e1;
      font-family: sans-serif;
    }
    table { border-collapse: collapse; min-width: 500px; }
    th, td { padding: 8px 12px; border: 1px solid #e2e8f0; }
    .sticky-col {
      position: sticky;
      left: 0;
      background-color: #f8fafc;
      z-index: 1;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="scroll-table">
    <table>
      <tr><th class="sticky-col">Ism</th><th>Telefon</th><th>Manzil</th><th>Kompaniya</th></tr>
      <tr><td class="sticky-col">Anvar</td><td>+99890123</td><td>Toshkent</td><td>Tech LLC</td></tr>
      <tr><td class="sticky-col">Zulayho</td><td>+99893456</td><td>Samarqand</td><td>Design Studio</td></tr>
    </table>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`position: sticky; left: 0` gorizontal skroll paytida birinchi ustunni chap tomonga mahkamlab turadi. Bu mobil qurilmalarda katta jadvallarni o'qishni juda osonlashtiradi.

## Ishlash natijasi:
```text
Jadval o'ngga surilganda 'Ism' ustuni o'z o'rnida qotib turadi, boshqa ustunlar esa uning ostiga kirib siljiydi.
```

---

# 543-Topshiriq: Rasm burchagida o'chirish tugmasi (Delete Cross Badge)
## Topshiriq sharti:
Yuklangan fotosuratning yuqori o'ng burchagiga xorijiy qizil 'x' o'chirish tugmasini joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Delete Badge</title>
  <style>
    .photo-item {
      position: relative;
      display: inline-block;
      width: 90px;
      height: 90px;
      background: #e2e8f0;
      border-radius: 8px;
      margin: 15px;
    }
    .remove-btn {
      position: absolute;
      top: -6px;
      right: -6px;
      width: 22px;
      height: 22px;
      background-color: #ef4444;
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: sans-serif;
      font-size: 13px;
      cursor: pointer;
      box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
  </style>
</head>
<body>
  <div class="photo-item">
    <span class="remove-btn" title="O'chirish">&times;</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Rasmni o'rab turgan ota qutiga `position: relative`, o'chirish doirachasiga `position: absolute; top: -6px; right: -6px` berilib, u fotosurat burchagini chiroyli qoplab turadi.

## Ishlash natijasi:
```text
Kulrang qutining yuqori o'ng burchagida x belgisiga ega kichik qizil aylana turadi.
```

---

# 544-Topshiriq: Position: absolute bilan to'liq bosiluvchi karta (Stretched Link)
## Topshiriq sharti:
Karta ichidagi bitta havola orqali butun karta maydonini bosiluvchi (clickable) holatga keltiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Stretched Link</title>
  <style>
    .card-link-box {
      position: relative;
      width: 260px;
      padding: 16px;
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      font-family: sans-serif;
      transition: box-shadow 0.2s;
    }
    .card-link-box:hover {
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .stretched-link {
      position: absolute;
      inset: 0;
      z-index: 1;
    }
  </style>
</head>
<body>
  <div class="card-link-box">
    <h3>Yangilik sarlavhasi</h3>
    <p>Ushbu kartaning istalgan joyiga bosganda havola ishlaydi.</p>
    <a href="#batafsil" class="stretched-link"></a>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Havola (`<a>`) ga `position: absolute; inset: 0` berilsa, u shaffof holatda butun ota element maydonini qoplaydi. Bu foydalanuvchi tajribasini (UX) sezilarli darajada oshiradi.

## Ishlash natijasi:
```text
Kartaning istalgan burchagiga bosilganda havola ochiladi.
```

---

# 545-Topshiriq: Vertikal o'q bo'ylab markazlashtirish (top: 50% va translateY)
## Topshiriq sharti:
Faqat vertikal bo'yicha mutlaq markazlashtirish usulini amalda ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Vertical Center</title>
  <style>
    .banner-row {
      position: relative;
      height: 120px;
      background-color: #047857;
      color: white;
      padding-left: 20px;
      font-family: sans-serif;
    }
    .vert-center-btn {
      position: absolute;
      top: 50%;
      right: 20px;
      transform: translateY(-50%);
      background-color: white;
      color: #047857;
      border: none;
      padding: 10px 18px;
      border-radius: 4px;
      font-weight: bold;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div class="banner-row">
    <h3>Maxsus Taklif</h3>
    <p>Faqat bugun 50% chegirma!</p>
    <button class="vert-center-btn">Qatnashish</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`top: 50%; transform: translateY(-50%)` qoidasi elementni o'ng yoki chap burchagidan qat'i nazar vertikal o'q bo'yicha mukammal o'rtaga joylashtiradi.

## Ishlash natijasi:
```text
Yashil banner ichida o'ng tomondagi oq tugma balandlik bo'yicha teng markazda turadi.
```

---

# 546-Topshiriq: Sticky bo'lim ajratuvchilar (Sticky Contact List A-Z)
## Topshiriq sharti:
Telefon kontaktlari ro'yxatida har bir harf boshlanishi (`A`, `B`, `C`) skroll paytida yuqoriga yopishib turishini ta'minlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Sticky Contact List</title>
  <style>
    .contact-container {
      max-height: 220px;
      overflow-y: auto;
      width: 260px;
      border: 1px solid #cbd5e1;
      font-family: sans-serif;
    }
    .char-header {
      position: sticky;
      top: 0;
      background-color: #f1f5f9;
      color: #475569;
      font-weight: bold;
      padding: 6px 12px;
      border-bottom: 1px solid #e2e8f0;
    }
    .contact-name {
      padding: 8px 12px;
      border-bottom: 1px solid #f8fafc;
    }
  </style>
</head>
<body>
  <div class="contact-container">
    <div class="char-header">A</div>
    <div class="contact-name">Akbar</div>
    <div class="contact-name">Anvar</div>
    <div class="contact-name">Aziza</div>
    <div class="char-header">B</div>
    <div class="contact-name">Bobur</div>
    <div class="contact-name">Baxtiyor</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Har bir `.char-header` sarlavhasiga `position: sticky; top: 0` berilgan. 'A' guruhi skroll bo'layotganda 'B' guruhi kelguniga qadar tepada yopishib turadi, so'ng 'B' uni itarib chiqaradi.

## Ishlash natijasi:
```text
Kontaktlar ro'yxati skroll qilinganda harflar ketma-ket darcha tepasida almashib qotib turadi.
```

---

# 547-Topshiriq: Absolute yordamida chiziqli orqa fon dekoratsiyasi
## Topshiriq sharti:
Sarlavhaning orqasida shaffof katta rangli doira fon bezagi yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Background Blob Decoration</title>
  <style>
    .hero-box {
      position: relative;
      padding: 40px;
      background: #0f172a;
      color: white;
      border-radius: 12px;
      overflow: hidden;
      font-family: sans-serif;
    }
    .circle-blob {
      position: absolute;
      top: -50px;
      right: -50px;
      width: 180px;
      height: 180px;
      background: #6366f1;
      border-radius: 50%;
      filter: blur(40px);
      opacity: 0.6;
      z-index: 0;
    }
    .hero-content {
      position: relative;
      z-index: 1;
    }
  </style>
</head>
<body>
  <div class="hero-box">
    <div class="circle-blob"></div>
    <div class="hero-content">
      <h2>Zamonaviy Web Dasturlash</h2>
      <p>CSS positioning yordamida chuqur vizual effektlar.</p>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Binafsharang doiraga `position: absolute; top: -50px; right: -50px; filter: blur(40px)` berilib, matn esa `position: relative; z-index: 1` orqali uning ustiga o'tkaziladi.

## Ishlash natijasi:
```text
To'q qora bannerning yuqori o'ng qismida xiralashgan neon binafsha nur taralib turadi.
```

---

# 548-Topshiriq: Display: none va Accessibility (aria-hidden)
## Topshiriq sharti:
Ekrandan yashirilgan elementni skrinriderlar va klaviatura foydalanuvchilaridan ham to'g'ri izolyatsiya qilishni ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Accessible Hiding</title>
  <style>
    .visually-hidden-panel {
      display: none;
    }
  </style>
</head>
<body>
  <button aria-expanded="false" aria-controls="extra-panel">
    Qo'shimcha ma'lumotni ko'rsatish
  </button>
  <div id="extra-panel" class="visually-hidden-panel" aria-hidden="true">
    <p>Ushbu maxfiy ma'lumot faqat tugma bosilganda ochiq bo'ladi.</p>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: none` qoidasi ko'rish imkoniyati cheklangan foydalanuvchilarning ovozli skrinrider dasturlaridan ham ma'lumotni yashiradi. Uni to'g'ri ARIA atributlari (`aria-hidden='true'`, `aria-expanded='false'`) bilan birga ishlatish tavsiya etiladi.

## Ishlash natijasi:
```text
Tugma ko'rinadi, ammo qo'shimcha panel na ekranda va na skrinriderda seziladi.
```

---

# 549-Topshiriq: Quyi qatlamli suv belgisi (Watermark) fon
## Topshiriq sharti:
Hujjat yoki sertifikat foniga katta yarim shaffof 'NUSXA' matnini absolute va z-index bilan joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Watermark Background</title>
  <style>
    .document {
      position: relative;
      width: 320px;
      padding: 30px;
      border: 1px solid #94a3b8;
      background: white;
      font-family: sans-serif;
      overflow: hidden;
    }
    .watermark {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%) rotate(-35deg);
      font-size: 54px;
      font-weight: 900;
      color: rgba(239, 68, 68, 0.12);
      user-select: none;
      pointer-events: none;
      z-index: 0;
    }
    .doc-content {
      position: relative;
      z-index: 1;
    }
  </style>
</head>
<body>
  <div class="document">
    <div class="watermark">NUSXA</div>
    <div class="doc-content">
      <h3>Rasmiy Shartnoma</h3>
      <p>Ushbu hujjat tomonlarning kelishuvi bo'yicha tuzildi va yuridik kuchga ega.</p>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`pointer-events: none` va `user-select: none` suv belgisini kursor bilan bosish yoki belgilashga to'sqinlik qiladi. `z-index: 0` esa uni matn ostiga tushiradi.

## Ishlash natijasi:
```text
Hujjat matni tagida diagonal qiya holatda xira qizil rangli ulkan 'NUSXA' so'zi aks etadi.
```

---

# 550-Topshiriq: To'liq interfeys: Sticky sarlavha, Absolute nishonlar va Fixed yordam paneli
## Topshiriq sharti:
Display va barcha position turlarini (sticky, absolute, fixed, relative) birlashtirgan mini boshqaruv paneli interfeysini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Complete Positioning UI</title>
  <style>
    body { margin: 0; font-family: sans-serif; background: #f8fafc; height: 1000px; }
    .sticky-nav {
      position: sticky;
      top: 0;
      background: #1e293b;
      color: white;
      padding: 12px 20px;
      display: flex;
      justify-content: space-between;
      z-index: 50;
    }
    .dashboard-grid {
      display: flex;
      gap: 16px;
      padding: 20px;
    }
    .kpi-card {
      position: relative;
      flex: 1;
      background: white;
      padding: 20px;
      border-radius: 8px;
      border: 1px solid #e2e8f0;
      box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    .kpi-badge {
      position: absolute;
      top: 12px;
      right: 12px;
      background: #dcfce7;
      color: #15803d;
      font-size: 11px;
      font-weight: bold;
      padding: 3px 8px;
      border-radius: 12px;
    }
    .fixed-help-btn {
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: #2563eb;
      color: white;
      padding: 12px 18px;
      border-radius: 30px;
      border: none;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(37,99,235,0.3);
      z-index: 100;
    }
  </style>
</head>
<body>
  <header class="sticky-nav">
    <strong>Admin Panel</strong>
    <span>Admin</span>
  </header>
  <div class="dashboard-grid">
    <div class="kpi-card">
      <span class="kpi-badge">+18%</span>
      <h4 style="margin: 0; color: #64748b;">Daromad</h4>
      <h2 style="margin: 8px 0 0 0;">$24,500</h2>
    </div>
    <div class="kpi-card">
      <span class="kpi-badge">+8%</span>
      <h4 style="margin: 0; color: #64748b;">Mijozlar</h4>
      <h2 style="margin: 8px 0 0 0;">1,420</h2>
    </div>
  </div>
  <button class="fixed-help-btn">&#128172; Yordam</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu loyihada barcha pozitsiyalash mexanizmlari uyg'unlashgan: Sticky Navbar tepada mahkamlangan, Karta ichidagi Badge absolute orqali joylangan va Yordam tugmasi fixed bilan ekranning pastki qismida doimiy turadi.

## Ishlash natijasi:
```text
Tepadagi mahkamlangan qora menyu, ichida yashil nishonlari bor ikkita oq karta va pastki burchakdagi suzuvchi ko'k yordam tugmasi.
```

---

