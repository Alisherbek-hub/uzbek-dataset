# HTML va CSS: Flexbox Asoslari va Yo'nalishlar (Topshiriqlar 551 - 600)

# 551-Topshiriq: Display: flex konteyneri yaratish va o'qlar tushunchasi
## Topshiriq sharti:
display: flex orqali konteyner yaratib, ichidagi blok elementlarning bir qatorga gorizontal o'q bo'ylab tizilishini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flexbox Asoslari</title>
  <style>
    .flex-container {
      display: flex;
      background-color: #f1f5f9;
      padding: 16px;
      gap: 12px;
      border-radius: 8px;
      font-family: sans-serif;
    }
    .flex-item {
      background-color: #3b82f6;
      color: white;
      padding: 16px 24px;
      border-radius: 6px;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="flex-container">
    <div class="flex-item">1-Band</div>
    <div class="flex-item">2-Band</div>
    <div class="flex-item">3-Band</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: flex` konteyner ichidagi farzand elementlarni (flex items) avtomatik ravishda bitta gorizontal asosiy o'q (main axis) bo'ylab tartibga soladi. Odatiy blok xususiyatidagi yangi qatordan tushish to'xtatiladi.

## Ishlash natijasi:
```text
Kulrang maydon ichida 3 ta moviy to'rtburchak element yonma-yon qatorda turadi.
```

---

# 552-Topshiriq: Display: inline-flex orqali inline o'lchamli flex konteyner
## Topshiriq sharti:
Flex konteynerning butun kenglikni egallamasdan, faqat o'z bolalari hajmiga mos inline darajasida turishini namoyish eting.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Inline Flex</title>
  <style>
    .inline-flex-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background-color: #10b981;
      color: white;
      padding: 10px 18px;
      border-radius: 20px;
      font-family: sans-serif;
      text-decoration: none;
      font-weight: 500;
    }
  </style>
</head>
<body>
  <p style="font-family: sans-serif;">
    Matn o'rtasida 
    <a href="#" class="inline-flex-btn">
      <span>&#128100;</span>
      <span>Profil</span>
    </a> 
    inline-flex tugmasi turibdi.
  </p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: inline-flex` konteynerning tashqi oqimda `inline` kabi turishini, lekin o'z ichida `flex` qoidalari (alignment, gap) bo'yicha ishlashini ta'minlaydi. Ikonkali tugmalar yaratish uchun ajoyib yechim.

## Ishlash natijasi:
```text
Matn ichida yashil rangli doirasimon kichik tugma oqimni buzmasdan joylashadi.
```

---

# 553-Topshiriq: Flex-direction: row (Asosiy standart gorizontal yo'nalish)
## Topshiriq sharti:
Elementlarning chapdan o'ngga qarab odatiy asosiy o'qda tartiblanishini tushuntiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Direction Row</title>
  <style>
    .box-row {
      display: flex;
      flex-direction: row;
      background-color: #e2e8f0;
      padding: 15px;
      gap: 10px;
      font-family: sans-serif;
    }
    .box {
      background: #0284c7;
      color: white;
      padding: 12px 20px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="box-row">
    <div class="box">A</div>
    <div class="box">B</div>
    <div class="box">C</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-direction: row` flex konteynerning sukut bo'yicha qiymatidir. Unda asosiy o'q (main axis) gorizontal bo'lib, chapdan o'ngga (LTR tizimida) yo'nalgan bo'ladi.

## Ishlash natijasi:
```text
A, B, C qutilari chapdan boshlanib bir qatorda tartib bilan ko'rinadi.
```

---

# 554-Topshiriq: Flex-direction: row-reverse bilan elementlar o'rnini teskari qilish
## Topshiriq sharti:
HTML tuzilmasiga teginmasdan elementlar tartibini o'ngdan chapga teskari joylashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Direction Row-Reverse</title>
  <style>
    .box-reverse {
      display: flex;
      flex-direction: row-reverse;
      background-color: #f8fafc;
      border: 1px solid #cbd5e1;
      padding: 15px;
      gap: 10px;
      font-family: sans-serif;
    }
    .box {
      background: #8b5cf6;
      color: white;
      padding: 12px 20px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="box-reverse">
    <div class="box">1-qadam</div>
    <div class="box">2-qadam</div>
    <div class="box">3-qadam</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-direction: row-reverse` asosiy o'q yo'nalishini 180 gradusga o'zgartiradi: elementlar ekranning o'ng chetidan boshlab teskari tartibda (3, 2, 1) joylashadi.

## Ishlash natijasi:
```text
Qutilar o'ng tomonda joylashib, eng o'ngda 1-qadam, undan chapda 2-qadam va 3-qadam ko'rinadi.
```

---

# 555-Topshiriq: Flex-direction: column bilan vertikal ustun tartibi
## Topshiriq sharti:
Flex elementlarni tepadan pastga qarab vertikal ustun shaklida tizishni bajaring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Direction Column</title>
  <style>
    .box-column {
      display: flex;
      flex-direction: column;
      background-color: #f1f5f9;
      padding: 15px;
      gap: 10px;
      width: 200px;
      font-family: sans-serif;
    }
    .col-item {
      background: #0d9488;
      color: white;
      padding: 10px;
      border-radius: 4px;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="box-column">
    <div class="col-item">Profil</div>
    <div class="col-item">Bildirishnomalar</div>
    <div class="col-item">Chiqish</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-direction: column` asosiy o'qni (main axis) vertikal holatga o'tkazadi (yuqoridan pastga). Endi barcha bo'ylama tekislashlar asosiy o'q hisobiga aylanadi.

## Ishlash natijasi:
```text
Eni 200px bo'lgan qutida 3 ta firuza rangli menyu bandlari ustun shaklida teriladi.
```

---

# 556-Topshiriq: Flex-direction: column-reverse bilan teskari ustun
## Topshiriq sharti:
Ustun elementlarini pastdan yuqoriga qarab teskari tartibda chiqaring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Direction Column-Reverse</title>
  <style>
    .box-col-rev {
      display: flex;
      flex-direction: column-reverse;
      background-color: #fef2f2;
      border: 1px solid #fecaca;
      padding: 15px;
      gap: 8px;
      width: 220px;
      font-family: sans-serif;
    }
    .rev-item {
      background: #dc2626;
      color: white;
      padding: 10px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="box-col-rev">
    <div class="rev-item">Xabar 1 (eng eski)</div>
    <div class="rev-item">Xabar 2</div>
    <div class="rev-item">Xabar 3 (eng yangi)</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-direction: column-reverse` vertikal asosiy o'qni pastdan tepaga qaratadi. Bu chat tizimlarida yangi xabarlarni pastki qismda ushlab turish kabi holatlarda qulaydir.

## Ishlash natijasi:
```text
Xabar 1 eng pastda, Xabar 3 esa eng tepada joylashgan qizil qutilar ro'yxati chiqadi.
```

---

# 557-Topshiriq: Flex-wrap: wrap bilan yangi qatorga o'tish
## Topshiriq sharti:
Konteyner eni torayganda bolalarning siqilib ketmasdan yangi qatorga tushishini ta'minlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Wrap</title>
  <style>
    .tags-container {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      width: 260px;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      padding: 12px;
      font-family: sans-serif;
    }
    .tag {
      background: #e0e7ff;
      color: #3730a3;
      padding: 6px 12px;
      border-radius: 16px;
      font-size: 13px;
    }
  </style>
</head>
<body>
  <div class="tags-container">
    <span class="tag">#html</span>
    <span class="tag">#css</span>
    <span class="tag">#javascript</span>
    <span class="tag">#frontend</span>
    <span class="tag">#webdev</span>
    <span class="tag">#flexbox</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-wrap: wrap` elementi bitta qatorga sig'may qolgan flex itemlarni avtomatik keyingi qatorga ko'chiradi. Sukutdagi `nowrap` esa elementlarni qisib tashlagan bo'lardi.

## Ishlash natijasi:
```text
Teglar 260px kenglikdagi chegaraga sig'ganicha yonma-yon turib, sig'maganlari pastki qatorga chiroyli o'tadi.
```

---

# 558-Topshiriq: Flex-wrap: nowrap va elementlarning siqilishi
## Topshiriq sharti:
Sukut bo'yicha nowrap rejimida elementlar bitta qatorda siqilib turishini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Nowrap</title>
  <style>
    .nowrap-box {
      display: flex;
      flex-wrap: nowrap;
      width: 280px;
      background: #fff1f2;
      border: 1px solid #fecdd3;
      padding: 10px;
      gap: 10px;
      font-family: sans-serif;
    }
    .item {
      flex: 0 0 100px; /* har biri 100px bo'lishi kerak, lekin 280px ga 3 tasi sig'may siqiladi */
      background: #e11d48;
      color: white;
      text-align: center;
      padding: 10px 0;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="nowrap-box">
    <div class="item">Quti 1</div>
    <div class="item">Quti 2</div>
    <div class="item">Quti 3</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-wrap: nowrap` sukutdagi qoida bo'lib, barcha elementlarni qanday qilib bo'lmasin yagona qator ichiga tiqishga majbur qiladi (agar flex-shrink 0 qilinmasa).

## Ishlash natijasi:
```text
Uchta qizil quti bitta qator ichida bir-biriga siqilib joylashadi.
```

---

# 559-Topshiriq: Flex-flow shorthand xususiyatidan foydalanish
## Topshiriq sharti:
flex-direction va flex-wrap xususiyatlarini bitta `flex-flow: row wrap` shorthand orqali ifodalang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Flow Shorthand</title>
  <style>
    .flow-container {
      display: flex;
      flex-flow: row wrap;
      gap: 12px;
      background: #f0fdf4;
      padding: 16px;
      border: 1px solid #bbf7d0;
      font-family: sans-serif;
    }
    .chip {
      background: #16a34a;
      color: white;
      padding: 8px 16px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="flow-container">
    <div class="chip">Toshkent</div>
    <div class="chip">Samarqand</div>
    <div class="chip">Buxoro</div>
    <div class="chip">Xiva</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-flow` xususiyati birinchi qiymatda yo'nalishni (`row`, `column`), ikkinchi qiymatda esa o'rash rejimini (`wrap`, `nowrap`) birlashtiradi: masalan `flex-flow: row wrap;`.

## Ishlash natijasi:
```text
Yashil chiplar satr bo'ylab terilib, sig'magan holatda yangi qatorga tushadi.
```

---

# 560-Topshiriq: Justify-content: flex-start (Boshlanish nuqtasiga tekislash)
## Topshiriq sharti:
Asosiy o'qdagi elementlarni satr boshiga qarab to'plang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Justify Flex Start</title>
  <style>
    .jc-start {
      display: flex;
      justify-content: flex-start;
      gap: 10px;
      background: #f1f5f9;
      padding: 15px;
      font-family: sans-serif;
    }
    .elem {
      background: #475569;
      color: white;
      padding: 10px 20px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="jc-start">
    <div class="elem">Start 1</div>
    <div class="elem">Start 2</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`justify-content: flex-start` sukutdagi boshlang'ich tekislash bo'lib, elementlarni asosiy o'qning boshlanish tomoniga (odatda chap tomonga) mahkamlab to'playdi.

## Ishlash natijasi:
```text
Ikkita to'q kulrang quti satrning eng chap tomonida yonma-yon turadi.
```

---

# 561-Topshiriq: Justify-content: flex-end (Oxirgi nuqtaga tekislash)
## Topshiriq sharti:
Elementlarni asosiy o'qning oxiriga, ya'ni satrning eng o'ng chetiga suring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Justify Flex End</title>
  <style>
    .jc-end {
      display: flex;
      justify-content: flex-end;
      gap: 10px;
      background: #f1f5f9;
      padding: 15px;
      font-family: sans-serif;
    }
    .btn-action {
      background: #2563eb;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 4px;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div class="jc-end">
    <button class="btn-action" style="background: #94a3b8;">Bekor qilish</button>
    <button class="btn-action">Saqlash</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`justify-content: flex-end` elementlarni satrning oxiriga qarab suradi. Bu modal oynalarning quyi harakat tugmalari panelida juda ko'p ishlatiladi.

## Ishlash natijasi:
```text
Tugmalar qatorning eng o'ng burchagida qulay joylashadi.
```

---

# 562-Topshiriq: Justify-content: center (Markaziy tekislash)
## Topshiriq sharti:
Asosiy gorizontal o'q bo'ylab barcha elementlarni konteyner markaziga to'plang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Justify Center</title>
  <style>
    .jc-center {
      display: flex;
      justify-content: center;
      gap: 12px;
      background: #f8fafc;
      padding: 20px;
      border: 1px solid #cbd5e1;
      font-family: sans-serif;
    }
    .badge {
      background: #7c3aed;
      color: white;
      padding: 8px 16px;
      border-radius: 6px;
    }
  </style>
</head>
<body>
  <div class="jc-center">
    <div class="badge">Markaziy 1</div>
    <div class="badge">Markaziy 2</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`justify-content: center` ota konteynerdagi ortiqcha bo'sh joyni elementlarning ikki tomoniga teng taqsimlab, barcha elementlarni markazga keltiradi.

## Ishlash natijasi:
```text
Ikkita binafsharang nishon konteynerning qoq o'rtasida yonma-yon turadi.
```

---

# 563-Topshiriq: Justify-content: space-between bilan qirralarga yoyish
## Topshiriq sharti:
Birinchi element eng chapda, oxirgisi eng o'ngda, qolganlari esa oraliqda teng masofada tarqaladigan navbar yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Space Between Navbar</title>
  <style>
    .nav-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #0f172a;
      color: white;
      padding: 12px 24px;
      font-family: sans-serif;
    }
    .nav-links {
      display: flex;
      gap: 16px;
    }
    a { color: #94a3b8; text-decoration: none; }
  </style>
</head>
<body>
  <header class="nav-bar">
    <div style="font-weight: bold; font-size: 18px;">TechPortal</div>
    <div class="nav-links">
      <a href="#">Darslar</a>
      <a href="#">Loyihalar</a>
      <a href="#">Aloqa</a>
    </div>
  </header>
</body>
</html>
```

## Tushuntirish va Mantiq:
`justify-content: space-between` chetki elementlarni to'liq konteyner qirralariga yopishtiradi va bo'sh joyni faqat elementlarning o'rtalariga teng miqdorda taqsimlaydi.

## Ishlash natijasi:
```text
Logotip eng chapda, havola menyulari esa eng o'ng tomonda joylashgan toza navbar hosil bo'ladi.
```

---

# 564-Topshiriq: Justify-content: space-around bilan element atrofida bo'shliq
## Topshiriq sharti:
Har bir elementning ikki tomoniga teng bo'shliq beruvchi space-around qiymatini namoyish qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Space Around</title>
  <style>
    .around-box {
      display: flex;
      justify-content: space-around;
      background: #ecfeff;
      border: 1px solid #a5f3fc;
      padding: 15px 0;
      font-family: sans-serif;
    }
    .around-item {
      background: #0891b2;
      color: white;
      padding: 10px 18px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="around-box">
    <div class="around-item">Karta A</div>
    <div class="around-item">Karta B</div>
    <div class="around-item">Karta C</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`justify-content: space-around` har bir elementning chap va o'ng tomoniga bir xil bo'shliq ajratadi. Natijada chekka oraliqlar (yarim hajm) o'rtadagi oraliqlardan (ikkita yarim = bitta to'liq) ikki barobar torroq bo'ladi.

## Ishlash natijasi:
```text
Elementlar atrofida bir tekis maydon ajralib turadi.
```

---

# 565-Topshiriq: Justify-content: space-evenly bilan mutlaq teng oraliqlar
## Topshiriq sharti:
Elementlar orasidagi va chekkadagi barcha bo'shliqlar 100% bir xil o'lchamda taqsimlanishini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Space Evenly</title>
  <style>
    .evenly-box {
      display: flex;
      justify-content: space-evenly;
      background: #fdf4ff;
      border: 1px solid #f0abfc;
      padding: 16px 0;
      font-family: sans-serif;
    }
    .item {
      background: #c026d3;
      color: white;
      padding: 10px 16px;
      border-radius: 6px;
    }
  </style>
</head>
<body>
  <div class="evenly-box">
    <div class="item">Birinchi</div>
    <div class="item">Ikkinchi</div>
    <div class="item">Uchinchi</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`justify-content: space-evenly` barcha oraliqlarni, shu jumladan eng chekka hoshiya bilan elementlar orasidagi masofani ham bir xil qilib hisoblaydi. Bu vizual jihatdan eng simmetrik tekislashdir.

## Ishlash natijasi:
```text
Har uchala binafsha quti va chekkalar oralig'idagi oq bo'shliqlar millimetrigacha teng bo'ladi.
```

---

# 566-Topshiriq: Align-items: stretch (Ko'ndalang o'q bo'ylab to'liq cho'zilish)
## Topshiriq sharti:
Sukut bo'yicha flex bolalarning balandligi ota elementning balandligiga mos cho'zilishi xususiyatini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Align Items Stretch</title>
  <style>
    .stretch-parent {
      display: flex;
      align-items: stretch; /* sukutdagi rejim */
      height: 120px;
      background: #e2e8f0;
      gap: 12px;
      padding: 12px;
      font-family: sans-serif;
    }
    .stretch-child {
      flex: 1;
      background: #0284c7;
      color: white;
      padding: 10px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="stretch-parent">
    <div class="stretch-child">Qisqa matn</div>
    <div class="stretch-child">Ushbu elementning bo'yi ham qisqa bo'lishiga qaramay ota balandligicha cho'ziladi.</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`align-items: stretch` cross axis (ko'ndalang o'q) bo'yicha sukutdagi qiymat bo'lib, agar elementlarda qat'iy `height` belgilanmagan bo'lsa, ularni eng baland element yoki ota konteyner bo'yiga to'liq moslab cho'zadi.

## Ishlash natijasi:
```text
Ikkala karta ham bir xil to'liq 120px balandlikka cho'zilib tekis turadi.
```

---

# 567-Topshiriq: Align-items: center (Vertikal markazlashtirish)
## Topshiriq sharti:
Ko'ndalang o'q bo'yicha elementlarni konteynerning vertikal o'rtasiga tekislang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Align Items Center</title>
  <style>
    .center-row {
      display: flex;
      align-items: center;
      height: 100px;
      background: #f1f5f9;
      padding: 0 16px;
      gap: 15px;
      font-family: sans-serif;
    }
    .badge-sm { background: #10b981; color: white; padding: 4px 8px; border-radius: 4px; }
    .badge-lg { background: #3b82f6; color: white; padding: 14px 20px; border-radius: 6px; }
  </style>
</head>
<body>
  <div class="center-row">
    <span class="badge-sm">Kichik</span>
    <span class="badge-lg">Katta Element</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`align-items: center` elementlarni ko'ndalang o'q bo'ylab qoq o'rtasiga joylashtiradi. Bu orqali har xil o'lchamdagi elementlar bir chiziqda uyg'un ko'rinadi.

## Ishlash natijasi:
```text
Kichik yashil nishon va katta ko'k blok 100px lik qator ichida vertikal markazda tekis turadi.
```

---

# 568-Topshiriq: Align-items: flex-start va flex-end
## Topshiriq sharti:
Elementlarni ko'ndalang o'qning yuqori yoki quyi chizig'iga tekislash farqini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Align Flex Start vs End</title>
  <style>
    .wrapper {
      display: flex;
      align-items: flex-end;
      height: 120px;
      background: #fffbeb;
      border: 1px solid #fde68a;
      padding: 10px;
      gap: 10px;
      font-family: sans-serif;
    }
    .col { background: #d97706; color: white; padding: 10px; border-radius: 4px; }
    .c1 { height: 40px; }
    .c2 { height: 70px; }
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="col c1">Pastga 40px</div>
    <div class="col c2">Pastga 70px</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`align-items: flex-end` turli balandlikdagi elementlarni konteynerning eng pastki chegarasiga (yoki flex-direction: row da poliga) tekkazib tekislaydi.

## Ishlash natijasi:
```text
Turli bo'yli to'q sariq qutilarning pastki qirralari bir tekis qatorda turadi.
```

---

# 569-Topshiriq: Align-items: baseline (Matn asosiy chizig'i bo'yicha tekislash)
## Topshiriq sharti:
Har xil shrift o'lchamidagi matnlarning pastki asosiy chizig'i (baseline) bir tekis chiqishini ta'minlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Align Baseline</title>
  <style>
    .baseline-row {
      display: flex;
      align-items: baseline;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      padding: 16px;
      gap: 12px;
      font-family: sans-serif;
    }
    .price-num { font-size: 36px; font-weight: bold; color: #0f172a; }
    .price-curr { font-size: 18px; color: #64748b; }
    .price-period { font-size: 14px; color: #94a3b8; }
  </style>
</head>
<body>
  <div class="baseline-row">
    <span class="price-num">99</span>
    <span class="price-curr">USD</span>
    <span class="price-period">/ oyiga</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`align-items: baseline` harflarning pastki asosi (harf tayanchi) bo'yicha tekislaydi. Shrift o'lchamlari 36px, 18px, 14px bo'lishiga qaramay ularning o'qilish chizig'i buzilmaydi.

## Ishlash natijasi:
```text
'99', 'USD' va '/ oyiga' so'zlari pastki matn chizig'i bo'yicha bir chiziqda turadi.
```

---

# 570-Topshiriq: Divni ekranning mutlaq markaziga qo'yish (The Perfect Center)
## Topshiriq sharti:
Justify-content: center va align-items: center yordamida qutini butun ekranning qoq o'rtasiga joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Perfect Center</title>
  <style>
    body {
      margin: 0;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #0f172a;
      font-family: sans-serif;
    }
    .modal-box {
      background: white;
      padding: 30px;
      border-radius: 12px;
      text-align: center;
      box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
  </style>
</head>
<body>
  <div class="modal-box">
    <h3 style="margin: 0 0 10px 0;">Mukammal Markaz</h3>
    <p style="margin: 0; color: #64748b;">Flexbox yordamida ikkala o'q bo'yicha markazlashtirildi.</p>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: flex`, `justify-content: center` (gorizontal markaz) va `align-items: center` (vertikal markaz) qoidalarini `height: 100vh` bo'lgan body elementiga berish vebdagi eng mashhur markazlashtirish usulidir.

## Ishlash natijasi:
```text
To'q qora ekran markazida oq darcha gorizontal va vertikal teng masofada joylashadi.
```

---

# 571-Topshiriq: Align-content: center ko'p qatorli flex konteynerda
## Topshiriq sharti:
Bir nechta qatorga o'ralgan (flex-wrap: wrap) qatorlarni konteyner o'rtasiga yig'ing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Align Content Center</title>
  <style>
    .multi-row-box {
      display: flex;
      flex-wrap: wrap;
      align-content: center;
      height: 240px;
      background: #f1f5f9;
      gap: 10px;
      padding: 10px;
      font-family: sans-serif;
    }
    .box {
      width: 120px;
      height: 40px;
      background: #6366f1;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="multi-row-box">
    <div class="box">1</div>
    <div class="box">2</div>
    <div class="box">3</div>
    <div class="box">4</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`align-content` faqat ko'p qatorli flexboxlarda (`flex-wrap: wrap`) ishlaydi. U alohida elementlarni emas, balki qatorlarning butun blokini ko'ndalang o'q bo'yicha markazlashtiradi.

## Ishlash natijasi:
```text
240px li baland maydonning qoq o'rtasida 2 qatorga terilgan qutilar to'planadi.
```

---

# 572-Topshiriq: Align-content: space-between va qatorlararo bo'shliq
## Topshiriq sharti:
Ko'p qatorli flex konteynerida birinchi qatorni tepaga, oxirgisini pastga surishni bajaring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Align Content Space-Between</title>
  <style>
    .rows-between {
      display: flex;
      flex-wrap: wrap;
      align-content: space-between;
      height: 220px;
      background: #fafaf9;
      border: 1px solid #d6d3d1;
      padding: 10px;
      gap: 10px;
      font-family: sans-serif;
    }
    .box { width: 45%; height: 40px; background: #e11d48; color: white; border-radius: 4px; display: flex; align-items: center; justify-content: center; }
  </style>
</head>
<body>
  <div class="rows-between">
    <div class="box">Qator 1 (Chap)</div>
    <div class="box">Qator 1 (O'ng)</div>
    <div class="box">Qator 2 (Chap)</div>
    <div class="box">Qator 2 (O'ng)</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`align-content: space-between` qatorlar bloklarini yuqori va pastki chegaralarga surib, ular orasidagi vertikal masofani teng taqsimlaydi.

## Ishlash natijasi:
```text
Qator 1 tepada, Qator 2 esa pastki chegarada yopishib turadi.
```

---

# 573-Topshiriq: Flex gap (row-gap va column-gap) xususiyatlari
## Topshiriq sharti:
Margin o'rniga zamonaviy CSS gap xususiyati bilan flex elementlar orasiga toza masofa qo'ying.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Gap</title>
  <style>
    .gap-demo {
      display: flex;
      flex-wrap: wrap;
      row-gap: 20px;
      column-gap: 12px;
      background: #f0fdf4;
      padding: 15px;
      font-family: sans-serif;
    }
    .card {
      width: 140px;
      height: 60px;
      background: #22c55e;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
    }
  </style>
</head>
<body>
  <div class="gap-demo">
    <div class="card">1</div>
    <div class="card">2</div>
    <div class="card">3</div>
    <div class="card">4</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`gap` flex konteyner ichidagi elementlar orasidagi bo'shliqni boshqaradi. U chekkalarda ortiqcha margin qoldirmaydi, `row-gap` qatorlar oralig'ini, `column-gap` esa ustunlar oralig'ini boshqaradi.

## Ishlash natijasi:
```text
Kartalar orasida gorizontal 12px, vertikal 20px oraliq toza taqsimlangan holda chiqadi.
```

---

# 574-Topshiriq: Gorizontal pivo vidjeti (Badge li statistika qatori)
## Topshiriq sharti:
Ikonka, son va o'sish foizini bitta gorizontal chiziqda align-items: center bilan joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Stat Widget</title>
  <style>
    .stat-row {
      display: flex;
      align-items: center;
      gap: 12px;
      background: white;
      padding: 12px 18px;
      border-radius: 8px;
      border: 1px solid #e2e8f0;
      width: fit-content;
      font-family: sans-serif;
    }
    .icon { font-size: 24px; }
    .value { font-size: 20px; font-weight: bold; color: #1e293b; }
    .badge-growth {
      background: #dcfce7;
      color: #16a34a;
      font-size: 12px;
      padding: 2px 8px;
      border-radius: 10px;
      font-weight: 600;
    }
  </style>
</head>
<body>
  <div class="stat-row">
    <span class="icon">&#128200;</span>
    <span class="value">$12,450</span>
    <span class="badge-growth">+14.2%</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Flexbox tufayli har xil balandlikka ega bo'lgan ikonka, 20px son va kichik foiz nishoni vertikal markaz bo'yicha mukammal tekislanadi.

## Ishlash natijasi:
```text
Grafik ikonkasi, narx va yashil '+14.2%' nishoni bir chiziqda toza aks etadi.
```

---

# 575-Topshiriq: Flexbox yordamida forma qidiruv maydoni (Input + Button)
## Topshiriq sharti:
Input va Submit tugmasini oraliqsiz bir-biriga tutashgan holda flex qilib birlashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Search Bar Flex</title>
  <style>
    .search-group {
      display: flex;
      width: 320px;
      font-family: sans-serif;
    }
    .search-input {
      flex: 1;
      padding: 10px 14px;
      border: 1px solid #cbd5e1;
      border-right: none;
      border-radius: 6px 0 0 6px;
      outline: none;
    }
    .search-btn {
      background: #2563eb;
      color: white;
      border: 1px solid #2563eb;
      padding: 10px 18px;
      border-radius: 0 6px 6px 0;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div class="search-group">
    <input type="text" class="search-input" placeholder="Qidiruv...">
    <button class="search-btn">Izlash</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: flex` yordamida `input` va `button` birlashtirilib, `border-radius` burchaklari orqali yagona yaxlit qidiruv komponenti yaratiladi.

## Ishlash natijasi:
```text
Chap tomoni oq maydon, o'ng tomoni esa ko'k 'Izlash' tugmasi bilan yaxlitlangan qidiruv paneli hosil bo'ladi.
```

---

# 576-Topshiriq: Margin: auto yordamida elementni oxirgi chekkaga itarish
## Topshiriq sharti:
Flex qatorida oxirgi elementga margin-left: auto berib, uni o'ng chetga suring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Margin Auto</title>
  <style>
    .toolbar {
      display: flex;
      align-items: center;
      gap: 10px;
      background: #f8fafc;
      padding: 10px 16px;
      border: 1px solid #e2e8f0;
      font-family: sans-serif;
    }
    .tool-btn { padding: 6px 12px; background: #e2e8f0; border: none; border-radius: 4px; }
    .push-right {
      margin-left: auto;
      background: #ef4444;
      color: white;
    }
  </style>
</head>
<body>
  <div class="toolbar">
    <button class="tool-btn">Nusxa</button>
    <button class="tool-btn">Tahrirlash</button>
    <button class="tool-btn push-right">O'chirish</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Flexboxda `margin-left: auto` bo'sh joyning barchasini o'ziga oladi va elementni o'ng chetga itaradi. Bu `space-between` ga ehtiyoj sezmasdan bitta elementni chekkaga chiqarishning eng aqlli usulidir.

## Ishlash natijasi:
```text
'Nusxa' va 'Tahrirlash' chapda qoladi, qizil 'O'chirish' esa eng o'ng chekkaga suriladi.
```

---

# 577-Topshiriq: Flexboxda tugmalar guruhi (Button Group)
## Topshiriq sharti:
Uchta tugmani bitta birikkan blok shaklida tutashtirib ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Button Group</title>
  <style>
    .btn-group {
      display: inline-flex;
      border-radius: 6px;
      overflow: hidden;
      border: 1px solid #cbd5e1;
      font-family: sans-serif;
    }
    .group-btn {
      padding: 8px 16px;
      background: white;
      border: none;
      border-right: 1px solid #cbd5e1;
      cursor: pointer;
    }
    .group-btn:last-child { border-right: none; }
    .group-btn.active { background: #3b82f6; color: white; }
  </style>
</head>
<body>
  <div class="btn-group">
    <button class="group-btn active">Kun</button>
    <button class="group-btn">Hafta</button>
    <button class="group-btn">Oy</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: inline-flex` orqali tugmalar bir qatorda zich joylashadi, chegaralar o'zaro tutashtirilib, `border-radius: 6px` butun guruhga beriladi.

## Ishlash natijasi:
```text
Yonma-yon ulangan 'Kun', 'Hafta', 'Oy' tugmalar guruhi paydo bo'ladi.
```

---

# 578-Topshiriq: Fikrlar (Testimonials) qutilarining teng balandlikda turishi
## Topshiriq sharti:
Har xil hajmdagi fikrlar kartochkalari flexbox align-items: stretch tufayli bir xil balandlikda ko'rinishini ta'minlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Equal Height Testimonials</title>
  <style>
    .reviews-grid {
      display: flex;
      gap: 16px;
      font-family: sans-serif;
    }
    .review-card {
      flex: 1;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
  </style>
</head>
<body>
  <div class="reviews-grid">
    <div class="review-card">
      <p>"Ajoyib platforma, juda ma'qul bo'ldi!"</p>
      <strong>- Sardor</strong>
    </div>
    <div class="review-card">
      <p>"Darslar sifati va tushuntirish metodikasi nihoyatda yuqori darajada. Men HTML va CSS ni 1 oyda to'liq o'zlashtirdim."</p>
      <strong>- Kamola</strong>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Flexboxda farzand elementlar sukut bo'yicha eng baland element darajasiga tenglashadi (`align-items: stretch`). Ichidagi `justify-content: space-between` esa muallif ismini karta tubiga tushiradi.

## Ishlash natijasi:
```text
Ikkala fikr kartasi har xil matn hajmiga ega bo'lsa-da, bo'yi bir xil tekis ko'rinadi.
```

---

# 579-Topshiriq: Flexbox bilan Pagination (Sahifalash) paneli
## Topshiriq sharti:
Raqamli sahifalash havolalarini flex orqali markazlashtirilgan tarzda tartibga soling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Pagination</title>
  <style>
    .pagination {
      display: flex;
      justify-content: center;
      gap: 8px;
      list-style: none;
      padding: 0;
      font-family: sans-serif;
    }
    .page-link {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 36px;
      height: 36px;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      text-decoration: none;
      color: #334155;
    }
    .page-link.active {
      background: #2563eb;
      color: white;
      border-color: #2563eb;
    }
  </style>
</head>
<body>
  <ul class="pagination">
    <li><a href="#" class="page-link">&laquo;</a></li>
    <li><a href="#" class="page-link active">1</a></li>
    <li><a href="#" class="page-link">2</a></li>
    <li><a href="#" class="page-link">3</a></li>
    <li><a href="#" class="page-link">&raquo;</a></li>
  </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
`ul` ro'yxatiga `display: flex; justify-content: center; gap: 8px` berilib, har bir havola `display: flex; align-items: center; justify-content: center` bilan raqamni o'rtada ushlaydi.

## Ishlash natijasi:
```text
Sahifa markazida 1 dan 3 gacha sahifa tugmalari tartibli tizilgan holda turadi.
```

---

# 580-Topshiriq: Tepadan pastga qarab o'suvchi xabarlar lentasi
## Topshiriq sharti:
Foydalanuvchi yangiliklari lentasini flex-direction: column va gap yordamida yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Feed Column</title>
  <style>
    .feed {
      display: flex;
      flex-direction: column;
      gap: 16px;
      width: 300px;
      font-family: sans-serif;
    }
    .feed-item {
      background: white;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 14px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
  </style>
</head>
<body>
  <div class="feed">
    <div class="feed-item">
      <strong>Ali</strong> yangi dars yukladi.
    </div>
    <div class="feed-item">
      <strong>Nodir</strong> savol qoldirdi.
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-direction: column` barcha postlarni vertikal ravishda joylashtiradi, `gap: 16px` esa postlar orasida toza masofa qoldiradi.

## Ishlash natijasi:
```text
Oq fonli ikkita yangilik kartochkasi vertikal ustunda teriladi.
```

---

# 581-Topshiriq: Flexboxda Media Object shabloni (Avatar + Matn)
## Topshiriq sharti:
Chap tomonda doiraviy rasm, o'ng tomonda matn blokini flex bilan uyg'unlashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Media Object</title>
  <style>
    .media-card {
      display: flex;
      align-items: flex-start;
      gap: 14px;
      padding: 16px;
      background: #f8fafc;
      border-radius: 8px;
      width: 320px;
      font-family: sans-serif;
    }
    .avatar {
      width: 48px;
      height: 48px;
      background-color: #6366f1;
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      flex-shrink: 0;
    }
  </style>
</head>
<body>
  <div class="media-card">
    <div class="avatar">UM</div>
    <div>
      <h4 style="margin: 0 0 4px 0;">Ulug'bek M.</h4>
      <p style="margin: 0; font-size: 13px; color: #64748b;">Assalomu alaykum! Loyiha topshirildi.</p>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-shrink: 0` xususiyati matn uzun bo'lgan taqdirda ham avatarning siqilib o'lchami o'zgarishini oldini oladi. `align-items: flex-start` esa elementlarni yuqoridan tekislaydi.

## Ishlash natijasi:
```text
Chapda dumaloq 'UM' avatari, o'ngda ism va xabar matni chiroyli joylashadi.
```

---

# 582-Topshiriq: Ustun ichida elementlarni gorizontal va vertikal markazlashtirish
## Topshiriq sharti:
flex-direction: column bo'lgan konteynerda justify-content va align-items orqali elementlarni markazlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Column Center</title>
  <style>
    .banner-col {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      height: 180px;
      background: #f0fdfa;
      border: 1px dashed #0d9488;
      border-radius: 8px;
      font-family: sans-serif;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="banner-col">
    <h3 style="margin: 0 0 8px 0; color: #0f766e;">Faylni bu yerga tashlang</h3>
    <p style="margin: 0; font-size: 13px; color: #115e59;">PNG, JPG (Maks. 10MB)</p>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Diqqat: `flex-direction: column` qilinganda `justify-content` vertikal o'qni boshqaradi, `align-items` esa gorizontal o'qni boshqaradi! Bu juda muhim qoidadir.

## Ishlash natijasi:
```text
Yashilroq fondagi ramka o'rtasida matnlar mukammal markazlashgan.
```

---

# 583-Topshiriq: Flexboxda rasm va caption matnining yonma-yon turishi
## Topshiriq sharti:
Kichik rasm va uning yonida tushuntirish matnini flex qatorida joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Image Caption Flex</title>
  <style>
    .photo-row {
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 12px;
      background: #f1f5f9;
      border-radius: 8px;
      font-family: sans-serif;
    }
    .img-placeholder {
      width: 70px;
      height: 70px;
      background: #94a3b8;
      border-radius: 6px;
      flex-shrink: 0;
    }
  </style>
</head>
<body>
  <div class="photo-row">
    <div class="img-placeholder"></div>
    <div>
      <h4 style="margin: 0 0 6px 0;">Toshkent teleminorasi</h4>
      <p style="margin: 0; font-size: 13px; color: #475569;">Balandligi 375 metr bo'lgan O'rta Osiyodagi eng baland inshoot.</p>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Flexbox tufayli rasm va uning yonidagi matn o'zaro siqilmaydi va `align-items: center` tufayli vertikal bir o'qda turadi.

## Ishlash natijasi:
```text
Kulrang to'rtburchak rasm o'rnida turadi, o'ngida esa teleminora haqidagi ma'lumot joylashadi.
```

---

# 584-Topshiriq: Flexbox bilan xabarnoma (Alert) darchasi
## Topshiriq sharti:
Ogohlantirish belgisini chapda, matnni o'rtada va yopish tugmasini o'ngda ushlab turuvchi alert komponenti yasang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Alert</title>
  <style>
    .alert-banner {
      display: flex;
      align-items: center;
      gap: 12px;
      background-color: #eff6ff;
      border: 1px solid #bfdbfe;
      color: #1e40af;
      padding: 12px 16px;
      border-radius: 6px;
      font-family: sans-serif;
    }
    .alert-icon { font-size: 20px; }
    .alert-text { flex: 1; font-size: 14px; }
    .close-btn {
      background: none;
      border: none;
      font-size: 18px;
      color: #1e40af;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div class="alert-banner">
    <span class="alert-icon">&#9432;</span>
    <span class="alert-text">Profilingiz muvaffaqiyatli faollashtirildi!</span>
    <button class="close-btn">&times;</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`alert-text` ga `flex: 1` berilgani tufayli u qolgan barcha bo'sh joyni egallaydi va yopish tugmasini tabiiy ravishda eng o'ng chetga itaradi.

## Ishlash natijasi:
```text
Ko'k fondagi alert qutisida chapda belgi, o'rtada xabar va o'ngda 'x' tugmasi turadi.
```

---

# 585-Topshiriq: Ikki qatorli kartalar panjarasi (Flex Card Grid)
## Topshiriq sharti:
flex-wrap: wrap va foizli kenglik yordamida 2 qatorli 4 ta kartadan iborat grid hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Card Grid</title>
  <style>
    .grid-container {
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      width: 320px;
      font-family: sans-serif;
    }
    .grid-card {
      flex: 1 1 calc(50% - 8px);
      background: #e0e7ff;
      padding: 20px 10px;
      text-align: center;
      border-radius: 6px;
      box-sizing: border-radius;
      font-weight: bold;
      color: #3730a3;
    }
  </style>
</head>
<body>
  <div class="grid-container">
    <div class="grid-card">Modul 1</div>
    <div class="grid-card">Modul 2</div>
    <div class="grid-card">Modul 3</div>
    <div class="grid-card">Modul 4</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex: 1 1 calc(50% - 8px)` har bir qatorga aniq 2 tadan element tushishini kafolatlaydi (`gap: 16px` ning yarmi chegiriladi).

## Ishlash natijasi:
```text
2 qator va 2 ustun shaklida to'rtta chiroyli binafsha kartalar joylashadi.
```

---

# 586-Topshiriq: Flexboxda havolalar paneli va chiziqli ajratgichlar (Breadcrumb)
## Topshiriq sharti:
Non ushoqlari (Breadcrumb) navigatsiyasini flexbox orqali '/' belgilari bilan tekislang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Breadcrumb</title>
  <style>
    .breadcrumb {
      display: flex;
      align-items: center;
      gap: 8px;
      list-style: none;
      padding: 0;
      font-family: sans-serif;
      font-size: 14px;
    }
    .breadcrumb a { color: #2563eb; text-decoration: none; }
    .separator { color: #94a3b8; }
    .current { color: #475569; font-weight: bold; }
  </style>
</head>
<body>
  <nav>
    <ul class="breadcrumb">
      <li><a href="#">Bosh sahifa</a></li>
      <li class="separator">/</li>
      <li><a href="#">Kurslar</a></li>
      <li class="separator">/</li>
      <li class="current">HTML & CSS</li>
    </ul>
  </nav>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ro'yxat flex qatoriga aylantirilib, `gap: 8px` va `align-items: center` orqali matnlar va ajratuvchi slash belgilari bir chiziqda tekislanadi.

## Ishlash natijasi:
```text
Bosh sahifa / Kurslar / HTML & CSS ko'rinishidagi gorizontal navigatsiya zanjiri hosil bo'ladi.
```

---

# 587-Topshiriq: Pastki navigatsiya menyusi (Mobile Bottom Nav)
## Topshiriq sharti:
Mobil telefonlar uchun ekranning tagida 4 ta ikonkani teng taqsimlovchi panel quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Mobile Bottom Nav</title>
  <style>
    .bottom-nav {
      display: flex;
      justify-content: space-around;
      align-items: center;
      height: 56px;
      background: white;
      border-top: 1px solid #e2e8f0;
      width: 320px;
      font-family: sans-serif;
    }
    .nav-btn {
      display: flex;
      flex-direction: column;
      align-items: center;
      font-size: 11px;
      color: #64748b;
      text-decoration: none;
    }
    .nav-btn.active { color: #2563eb; font-weight: bold; }
    .icon { font-size: 18px; margin-bottom: 2px; }
  </style>
</head>
<body>
  <div class="bottom-nav">
    <a href="#" class="nav-btn active"><span class="icon">&#8962;</span>Asosiy</a>
    <a href="#" class="nav-btn"><span class="icon">&#128269;</span>Qidiruv</a>
    <a href="#" class="nav-btn"><span class="icon">&#128172;</span>Chat</a>
    <a href="#" class="nav-btn"><span class="icon">&#9881;</span>Sozlama</a>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ota konteyner `justify-content: space-around` bilan tugmalarni teng masofada joylashtiradi, har bir tugmaning o'zi esa `flex-direction: column` bilan ikonka va yozuvni ustun qiladi.

## Ishlash natijasi:
```text
Mobil ilovalardagi kabi 4 ta teng oraliqdagi ikonka va pastki yozuvdan iborat pastki panel.
```

---

# 588-Topshiriq: Statistika raqamlarini vertikal markazlashtirish
## Topshiriq sharti:
Katta raqam va kichik tavsifni kartochka ichida markaziy joylashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Stat Box</title>
  <style>
    .kpi-box {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      width: 140px;
      height: 100px;
      background: #faf5ff;
      border: 1px solid #e9d5ff;
      border-radius: 8px;
      font-family: sans-serif;
    }
    .kpi-num { font-size: 28px; font-weight: bold; color: #7e22ce; }
    .kpi-lbl { font-size: 12px; color: #6b21a8; }
  </style>
</head>
<body>
  <div class="kpi-box">
    <span class="kpi-num">1,000+</span>
    <span class="kpi-lbl">Topshiriqlar</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-direction: column` hamda `justify-content: center; align-items: center` raqam va matnni ikkala o'q bo'yicha kartaning mutlaq markaziga qo'yadi.

## Ishlash natijasi:
```text
Binafsha rangli to'rtburchak ichida '1,000+' va 'Topshiriqlar' markazda toza joylashadi.
```

---

# 589-Topshiriq: Flexboxda tugmalar o'rtasida separator (ajratuvchi chiziq)
## Topshiriq sharti:
Ikkita amallar bloki o'rtasiga vertikal ingichka chiziqcha qo'yib flex qatorini shakllantiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Separator</title>
  <style>
    .split-bar {
      display: flex;
      align-items: center;
      gap: 12px;
      background: #f1f5f9;
      padding: 8px 16px;
      border-radius: 6px;
      font-family: sans-serif;
      width: fit-content;
    }
    .divider {
      width: 1px;
      height: 20px;
      background: #cbd5e1;
    }
  </style>
</head>
<body>
  <div class="split-bar">
    <button style="border:none; background:none; cursor:pointer;">Yuklab olish</button>
    <div class="divider"></div>
    <button style="border:none; background:none; cursor:pointer;">Ulashish</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`divider` blokiga `width: 1px; height: 20px` berilib, flexbox `align-items: center` tufayli tugmalar o'rtasida chiroyli vertikal chiziqcha hosil bo'ladi.

## Ishlash natijasi:
```text
Ikkita harakat tugmasi o'rtasida 20px bo'yli och kulrang vertikal ajratgich ko'rinadi.
```

---

# 590-Topshiriq: Flexbox orqali ro'yxat tartibini dinamik teskari qilish
## Topshiriq sharti:
flex-direction: row-reverse orqali qatordagi elementlar joylashuvini akslantiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Dynamic Reverse</title>
  <style>
    .steps {
      display: flex;
      flex-direction: row-reverse;
      gap: 15px;
      font-family: sans-serif;
    }
    .step {
      background: #f97316;
      color: white;
      padding: 10px 16px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="steps">
    <div class="step">Qadam 1</div>
    <div class="step">Qadam 2</div>
    <div class="step">Qadam 3</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-direction: row-reverse` yordamida HTML manbasidagi elementlar tartibini o'zgartirmasdan, ularni vizual ravishda o'ngdan chapga teskari tartibda render qilish mumkin.

## Ishlash natijasi:
```text
O'ng tomonda 'Qadam 1', undan chapda 'Qadam 2' va 'Qadam 3' ko'rinadi.
```

---

# 591-Topshiriq: Flexboxda matn uzunligiga qarab tugmalar avtomatik sig'ishi
## Topshiriq sharti:
Har xil uzunlikdagi teglar (chiplar) qatorda siqilmay o'z o'lchamini saqlab wrap bo'lishini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Auto Sizing Chips</title>
  <style>
    .chip-cloud {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      width: 250px;
      font-family: sans-serif;
    }
    .chip-item {
      white-space: nowrap;
      background: #e2e8f0;
      padding: 6px 12px;
      border-radius: 12px;
      font-size: 12px;
    }
  </style>
</head>
<body>
  <div class="chip-cloud">
    <span class="chip-item">AI</span>
    <span class="chip-item">Machine Learning</span>
    <span class="chip-item">Data Science</span>
    <span class="chip-item">Deep Learning</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`white-space: nowrap` chip ichidagi matnni ikkiga bo'linib ketishdan saqlaydi, `flex-wrap: wrap` esa uzun chiplarni keyingi satrga tushiradi.

## Ishlash natijasi:
```text
Tor qutida kalit so'zlar bo'linmasdan bir necha qatorga toza o'tadi.
```

---

# 592-Topshiriq: Footer bo'limlarini flexbox bilan ustunlarga ajratish
## Topshiriq sharti:
Sayt footerida 3 ta menyu ustunini space-between bilan kenglik bo'yicha teng yoying.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Footer Columns Flex</title>
  <style>
    .footer-content {
      display: flex;
      justify-content: space-between;
      background: #0f172a;
      color: white;
      padding: 30px;
      font-family: sans-serif;
    }
    .col h4 { margin-top: 0; color: #38bdf8; }
    .col ul { list-style: none; padding: 0; margin: 0; font-size: 13px; }
    .col li { margin-bottom: 6px; }
  </style>
</head>
<body>
  <footer class="footer-content">
    <div class="col">
      <h4>Kompaniya</h4>
      <ul><li>Biz haqimizda</li><li>Karyera</li></ul>
    </div>
    <div class="col">
      <h4>Mahsulotlar</h4>
      <ul><li>Veb ilova</li><li>Mobil ilova</li></ul>
    </div>
    <div class="col">
      <h4>Bog'lanish</h4>
      <ul><li>info@sayt.uz</li><li>+998712000000</li></ul>
    </div>
  </footer>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: flex; justify-content: space-between` footer ichidagi barcha ustunlarni chapdan o'nggacha butun kenglik bo'ylab tekis yoyib beradi.

## Ishlash natijasi:
```text
Qora fonda uchta ko'k sarlavhali ma'lumotlar ustuni teng oraliqda turadi.
```

---

# 593-Topshiriq: Flexboxda elementlarni qatorga teskari yig'ish (wrap-reverse)
## Topshiriq sharti:
flex-wrap: wrap-reverse orqali sig'magan yangi qatorlarni yuqoriga qarab o'stirib ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Wrap Reverse</title>
  <style>
    .wrap-rev-box {
      display: flex;
      flex-wrap: wrap-reverse;
      gap: 10px;
      width: 200px;
      background: #fdf2f8;
      border: 1px solid #fbcfe8;
      padding: 10px;
      font-family: sans-serif;
    }
    .badge {
      background: #db2777;
      color: white;
      padding: 6px 12px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="wrap-rev-box">
    <div class="badge">A1</div>
    <div class="badge">A2</div>
    <div class="badge">B1</div>
    <div class="badge">B2</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-wrap: wrap-reverse` odatiy pastga qarab yangi qator ochish o'rniga, yangi paydo bo'lgan qatorlarni tepaga qarab taxlaydi.

## Ishlash natijasi:
```text
Ikkinchi qator birinchi qatorning tagida emas, balki uning ustida paydo bo'ladi.
```

---

# 594-Topshiriq: Kartochka ichida harakat tugmasini tubiga mahkamlash
## Topshiriq sharti:
Baland kartochka ichida 'Batafsil' tugmasini pastki chegara bo'yicha mahkamlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Card Bottom Button</title>
  <style>
    .product-card {
      display: flex;
      flex-direction: column;
      width: 200px;
      height: 220px;
      background: white;
      border: 1px solid #cbd5e1;
      padding: 16px;
      border-radius: 8px;
      font-family: sans-serif;
    }
    .buy-btn {
      margin-top: auto; /* Bo'sh joyni yuqoriga itarib, tugmani tubga mahkamlaydi */
      background: #10b981;
      color: white;
      border: none;
      padding: 8px;
      border-radius: 4px;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div class="product-card">
    <h4>Dasturlash kitobi</h4>
    <p style="font-size: 13px; color: #64748b;">Mukammal qo'llanma.</p>
    <button class="buy-btn">Sotib olish</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-direction: column` bo'lgan kartada `margin-top: auto` berilgan tugma yuqoridagi barcha bo'sh joyni o'zlashtirib, avtomatik ravishda pastki polga yopishadi.

## Ishlash natijasi:
```text
Matn tepada turadi, yashil xarid tugmasi esa kartaning eng tagida mustahkam o'rnashadi.
```

---

# 595-Topshiriq: Flexboxda ko'ndalang o'q bo'ylab cho'zilishni to'xtatish
## Topshiriq sharti:
align-items: flex-start orqali elementlarning o'z tabiiy bo'yini saqlab qolishini ta'minlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Prevent Stretch</title>
  <style>
    .no-stretch {
      display: flex;
      align-items: flex-start; /* stretch bekor qilinadi */
      height: 120px;
      background: #f1f5f9;
      gap: 10px;
      padding: 10px;
      font-family: sans-serif;
    }
    .box {
      background: #3b82f6;
      color: white;
      padding: 8px 12px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="no-stretch">
    <div class="box">Bo'yi cho'zilmaydi</div>
    <div class="box">O'z hajmida qoladi</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Standart `align-items: stretch` bo'yicha elementlar 120px ga cho'zilib ketgan bo'lardi. `align-items: flex-start` qo'yilishi bilan har bir element o'zining tabiiy kontent balandligiga qaytadi.

## Ishlash natijasi:
```text
Ko'k elementlar butun 120px balandlikka cho'zilmasdan, faqat yozuv hajmida tepada turadi.
```

---

# 596-Topshiriq: Flexboxda izohlar (Comments) daraxti tuzilishi
## Topshiriq sharti:
Foydalanuvchi sharhlarini birin-ketin va javoblarni ichkariga surilgan holda flex ustunida shakllantiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flex Comments</title>
  <style>
    .comments-tree {
      display: flex;
      flex-direction: column;
      gap: 12px;
      font-family: sans-serif;
      width: 300px;
    }
    .comment-bubble {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      padding: 10px 14px;
      border-radius: 8px;
    }
    .reply {
      margin-left: 28px;
      background: #f0fdf4;
      border-color: #bbf7d0;
    }
  </style>
</head>
<body>
  <div class="comments-tree">
    <div class="comment-bubble">
      <strong>Akmal:</strong> Dars juda tushunarli bo'ldi.
    </div>
    <div class="comment-bubble reply">
      <strong>O'qituvchi:</strong> Rahmat, keyingi darslar yanada qiziqarli bo'ladi!
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Flex ustun strukturasida javob xabariga `margin-left: 28px` berilishi daraxtsimon iyerarxiyani chiroyli ta'minlaydi.

## Ishlash natijasi:
```text
Asosiy fikr chapda, unga bildirilgan javob esa o'ngroqqa surilgan holda aks etadi.
```

---

# 597-Topshiriq: Flexboxda tugmalar orasidagi gorizontal o'q bo'ylab teskari tartib
## Topshiriq sharti:
O'ngdan chapga qarab saralangan dialog oynasi tasdiqlash tugmalarini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Dialog Actions</title>
  <style>
    .actions {
      display: flex;
      flex-direction: row-reverse;
      gap: 10px;
      background: #ffffff;
      padding: 12px;
      border-top: 1px solid #e2e8f0;
      font-family: sans-serif;
    }
    .btn { padding: 8px 16px; border-radius: 4px; border: none; cursor: pointer; }
    .btn-primary { background: #2563eb; color: white; }
    .btn-secondary { background: #e2e8f0; color: #334155; }
  </style>
</head>
<body>
  <div class="actions">
    <button class="btn btn-primary">Tasdiqlash</button>
    <button class="btn btn-secondary">Bekor qilish</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-direction: row-reverse` bilan Asosiy harakat (Tasdiqlash) eng o'ng burchakda turadi, Bekor qilish esa uning chap tomonida joylashadi.

## Ishlash natijasi:
```text
O'ng tomonda ko'k 'Tasdiqlash', chaprog'ida kulrang 'Bekor qilish' tugmalari joylashadi.
```

---

# 598-Topshiriq: Flexboxda matn sarlavhasi yoniga to'liq chiziq tortish
## Topshiriq sharti:
Sarlavha yonidagi bo'sh joyni gorizontal kulrang chiziq bilan to'ldiruvchi flex elementi yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Heading Line Flex</title>
  <style>
    .header-with-line {
      display: flex;
      align-items: center;
      gap: 14px;
      font-family: sans-serif;
    }
    .title-text { font-size: 18px; font-weight: bold; color: #1e293b; white-space: nowrap; }
    .line-fill {
      flex: 1;
      height: 2px;
      background-color: #cbd5e1;
    }
  </style>
</head>
<body>
  <div class="header-with-line">
    <span class="title-text">So'nggi Yangiliklar</span>
    <span class="line-fill"></span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`line-fill` ga `flex: 1` berilgani tufayli u qatorning qolgan barcha bo'shlig'ini to'ldirib, sarlavha yonida uzluksiz chiziq tortadi.

## Ishlash natijasi:
```text
'So'nggi Yangiliklar' matni va uning ketidan konteyner oxirigacha cho'zilgan 2px qalinlikdagi chiziq.
```

---

# 599-Topshiriq: Flexboxda narxlar jadvali sarlavha va afzalliklari
## Topshiriq sharti:
Tarif rejasidagi har bir qatorda yashil qushcha belgisi va matnni flex orqali tekislang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Pricing Features Flex</title>
  <style>
    .features-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
      font-family: sans-serif;
      width: 240px;
    }
    .feature-item {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 14px;
      color: #334155;
    }
    .check-icon {
      color: #16a34a;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="features-list">
    <div class="feature-item">
      <span class="check-icon">&#10003;</span>
      <span>Cheksiz darslar</span>
    </div>
    <div class="feature-item">
      <span class="check-icon">&#10003;</span>
      <span>24/7 Mentor yordami</span>
    </div>
    <div class="feature-item">
      <span class="check-icon">&#10003;</span>
      <span>Sertifikat taqdimoti</span>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Har bir qator `display: flex; align-items: center; gap: 10px` orqali yashil tasdiq belgisini matn bilan bir xil darajada ushlab turadi.

## Ishlash natijasi:
```text
Yashil qushchali uchta tarif xususiyati bir chiziqda toza terilgan holda chiqadi.
```

---

# 600-Topshiriq: To'liq Flexbox boshqaruv paneli (Header, Content va Footer)
## Topshiriq sharti:
Faqat flexbox qoidalaridan foydalanib to'liq veb-sahifa maketini hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Complete Flexbox Layout</title>
  <style>
    body {
      margin: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      font-family: sans-serif;
    }
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #1e293b;
      color: white;
      padding: 14px 20px;
    }
    .main-body {
      flex: 1;
      display: flex;
      background: #f8fafc;
    }
    aside {
      width: 180px;
      background: #f1f5f9;
      border-right: 1px solid #e2e8f0;
      padding: 16px;
    }
    main {
      flex: 1;
      padding: 20px;
    }
    footer {
      background: #0f172a;
      color: #94a3b8;
      text-align: center;
      padding: 12px;
      font-size: 13px;
    }
  </style>
</head>
<body>
  <header>
    <div>FlexPortal</div>
    <nav>Profil | Chiqish</nav>
  </header>
  <div class="main-body">
    <aside>
      <strong>Menyu</strong>
      <p>Boshqaruv</p>
    </aside>
    <main>
      <h2>Bosh Sahifa</h2>
      <p>Asosiy kontent maydoni to'liq kenglikni egallaydi.</p>
    </main>
  </div>
  <footer>&copy; 2026 FlexPortal</footer>
</body>
</html>
```

## Tushuntirish va Mantiq:
Tashqi `body` flex ustun shaklida, ichki `.main-body` esa gorizontal flex qatori shaklida qurilgan. `flex: 1` xususiyati asosiy maydonga butun bo'sh joyni egallash imkonini beradi.

## Ishlash natijasi:
```text
Tepadagi navbar, chapdagi yon panel, o'rtadagi katta ish maydoni va pastdagi footer mukammal birlashadi.
```

---

