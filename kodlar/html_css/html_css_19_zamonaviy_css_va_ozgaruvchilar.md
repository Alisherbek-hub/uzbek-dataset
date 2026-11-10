# HTML va CSS: Zamonaviy CSS va O'zgaruvchilar (Topshiriqlar 901 - 950)

# 901-Topshiriq: CSS Custom Properties (O'zgaruvchilar): :root va var() asoslari
## Topshiriq sharti:
:root psevdo-klassida global rang o'zgaruvchisi e'lon qilib, uni tugma va sarlavhada qo'llang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>CSS Variables Root</title>
  <style>
    :root {
      --primary-color: #2563eb;
      --primary-hover: #1d4ed8;
      --text-main: #0f172a;
    }
    body { font-family: sans-serif; color: var(--text-main); padding: 20px; }
    h2 { color: var(--primary-color); }
    .btn {
      background-color: var(--primary-color);
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 6px;
      cursor: pointer;
    }
    .btn:hover {
      background-color: var(--primary-hover);
    }
  </style>
</head>
<body>
  <h2>CSS O'zgaruvchilari</h2>
  <button class="btn">Asosiy Tugma</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:root` barcha HTML elementlari uchun global ota hisoblanadi. Unda `--nom` bilan boshlangan o'zgaruvchilar e'lon qilinadi va `var(--nom)` orqali butun loyiha bo'yicha qayta-qayta ishlatiladi.

## Ishlash natijasi:
```text
Ko'k rangli sarlavha va ko'k fonli tugma, hover qilinganda to'q ko'k rangga o'tadi.
```

---

# 902-Topshiriq: Var() funksiyasida zaxira qiymat (Fallback value)
## Topshiriq sharti:
Agar o'zgaruvchi topilmasa yoki e'lon qilinmagan bo'lsa, var(--custom, #fallback) zaxira rangidan foydalanish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Variable Fallback</title>
  <style>
    .card {
      /* --theme-color e'lon qilinmagan, shu sababli zaxiradagi #10b981 ishlaydi */
      background-color: var(--theme-color, #10b981);
      color: white;
      padding: 16px;
      border-radius: 8px;
      font-family: sans-serif;
      width: fit-content;
    }
  </style>
</head>
<body>
  <div class="card">Zaxira (Fallback) yashil rangida</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`var(--nom, zaxira)` sintaksisida ikkinchi parametr zaxira hisoblanadi. Bu katta komponentlar kutubxonalarida o'zgaruvchi berilmagan holatlarda xatolik yuz bermasligini ta'minlaydi.

## Ishlash natijasi:
```text
O'zgaruvchi topilmagani uchun quti yashil (#10b981) zaxira rangida chiqadi.
```

---

# 903-Topshiriq: Lokal o'zgaruvchilar va ularning doirasi (Variable Scope)
## Topshiriq sharti:
Bitta komponent ichida o'zgaruvchini qayta e'lon qilib faqat shu komponent rangini o'zgartiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Variable Scope</title>
  <style>
    :root { --card-bg: #f1f5f9; --card-color: #334155; }
    .card {
      background: var(--card-bg);
      color: var(--card-color);
      padding: 16px;
      border-radius: 6px;
      font-family: sans-serif;
      margin-bottom: 10px;
      width: 220px;
    }
    .card-danger {
      /* Faqat shu sinf ichida o'zgaruvchilar qayta yoziladi */
      --card-bg: #fee2e2;
      --card-color: #b91c1c;
    }
  </style>
</head>
<body>
  <div class="card">Oddiy Karta</div>
  <div class="card card-danger">Xavfli Karta (Lokal Scope)</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
CSS o'zgaruvchilari iyerarxiya bo'yicha meros qilib olinadi. `.card-danger` ichida `--card-bg` o'zgartirilishi boshqa elementlarga ta'sir qilmasdan faqat shu blokda amal qiladi.

## Ishlash natijasi:
```text
Birinchi karta kulrang, ikkinchi karta esa lokal o'zgaruvchi sababli qizil tusda chiqadi.
```

---

# 904-Topshiriq: Calc() matematik funksiyasi bilan o'lchamlarni hisoblash
## Topshiriq sharti:
Element kengligini 100% minus 40px qilib hisoblash orqali ramkaga mukammal sig'diring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>CSS Calc Function</title>
  <style>
    .parent {
      background: #e2e8f0;
      padding: 20px;
      width: 300px;
    }
    .child-calc {
      width: calc(100% - 40px); /* 100% dan 40px chegiriladi */
      background: #2563eb;
      color: white;
      padding: 10px;
      font-family: sans-serif;
      text-align: center;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="parent">
    <div class="child-calc">calc(100% - 40px)</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`calc()` piksel (`px`), foiz (`%`), `rem` va boshqa turli birliklarni bir-biri bilan qo'shish, ayirish, ko'paytirish va bo'lish imkonini beradi. Muhim: belgilar orasida bo'shliq bo'lishi shart (`-`, `+`).

## Ishlash natijasi:
```text
Kulrang quti ichida ikki tomonidan 20px dan ochiq qolgan ko'k to'rtburchak joylashadi.
```

---

# 905-Topshiriq: Min() va Max() matematik funksiyalari
## Topshiriq sharti:
Kenglikni min(100%, 320px) orqali hech qachon 320px dan oshmaydigan qilib belgilang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>CSS Min and Max</title>
  <style>
    .smart-card {
      width: min(100%, 320px);
      background: #10b981;
      color: white;
      padding: 20px;
      border-radius: 8px;
      font-family: sans-serif;
      box-sizing: border-box;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="smart-card">width: min(100%, 320px)</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`min(A, B)` berilgan ikki qiymatdan eng kichigini tanlaydi. Ekran 500px bo'lsa 320px tanlanadi, ekran 250px bo'lsa 100% (250px) tanlanadi.

## Ishlash natijasi:
```text
Katta ekranda 320px, kichik ekranda esa butun ekranni egallovchi yashil quti.
```

---

# 906-Topshiriq: :is() psevdo-klassi bilan selektorlarni ixchamlashtirish
## Topshiriq sharti:
h1, h2, h3 teglarining ichidagi spanlarni :is(h1, h2, h3) span orqali bitta qatorda belgilang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>CSS Is Selector</title>
  <style>
    /* Eskirgan: h1 span, h2 span, h3 span o'rniga: */
    :is(h1, h2, h3) span {
      color: #ef4444;
      text-decoration: underline;
    }
    body { font-family: sans-serif; }
  </style>
</head>
<body>
  <h1>Birinchi <span>ajratilgan</span> so'z</h1>
  <h2>Ikkinchi <span>ajratilgan</span> so'z</h2>
  <p>Oddiy <span>matn</span> o'zgarmaydi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:is()` takrorlanuvchi selektorlar guruhini ixchamlashtiradi. Uning o'ziga xosligi (specificity) ro'yxatdagi eng kuchli selektor darajasiga tenglashadi.

## Ishlash natijasi:
```text
H1 va H2 ichidagi 'ajratilgan' so'zlari qizil va tagiga chizilgan, paragraf ichidagi so'z esa oddiy qoladi.
```

---

# 907-Topshiriq: :where() psevdo-klassi va nol o'ziga xoslik (Zero Specificity)
## Topshiriq sharti:
O'ziga xosligi 0 bo'lgan standart stillar yozish uchun :where() dan foydalaning.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>CSS Where Selector</title>
  <style>
    /* :where() specificity = 0 beradi */
    :where(section, article) p {
      color: #64748b;
      font-family: sans-serif;
    }
    /* Oddiy klass osonlikcha :where ni yengadi */
    .special {
      color: #2563eb;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <article>
    <p>Kulrang matn (:where)</p>
    <p class="special">Ko'k matn (oddiy sinf uni oson qayta yozadi)</p>
  </article>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:where()` xuddi `:is()` kabi ishlaydi, lekin uning specificity (aniqlik darajasi) doimo 0 ga teng. Bu CSS CSS-reset va UI kutubxonalarini tuzishda stilar oson qayta yozilishi uchun juda qulay.

## Ishlash natijasi:
```text
Biri kulrang matn, maxsus sinfli paragraf esa ko'k qalin rangda chiqadi.
```

---

# 908-Topshiriq: :has() psevdo-klassi: Ota elementni selektlash inqilobi
## Topshiriq sharti:
Ichida rasmi bo'lgan kartochkaning o'ziga alohida hoshiya berish uchun .card:has(img) qo'llang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>CSS Parent Selector Has</title>
  <style>
    .card {
      padding: 16px;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      font-family: sans-serif;
      margin-bottom: 12px;
      width: 240px;
    }
    /* Agar karta ichida .badge bo'lsa, kartaning o'zi yashil chegara oladi */
    .card:has(.badge) {
      border: 2px solid #10b981;
      background: #f0fdf4;
    }
    .badge {
      background: #10b981;
      color: white;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 11px;
    }
  </style>
</head>
<body>
  <div class="card">
    <h4>Oddiy Karta</h4>
  </div>
  <div class="card">
    <span class="badge">Aktiv</span>
    <h4>Maxsus Karta (:has)</h4>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:has()` uzoq yillar kutilgan 'Parent Selector'dir. U farzand element mavjudligiga qarab uning OTA elementiga stil berish imkonini yaratadi (JavaScript talab etilmaydi!).

## Ishlash natijasi:
```text
Nishoni bor ikkinchi karta avtomatik tarzda yashil hoshiya va och yashil fon oladi.
```

---

# 909-Topshiriq: :has() orqali formadagi xatolikni butun guruhga yoyish
## Topshiriq sharti:
Agar input noto'g'ri bo'lsa (:invalid), butun .form-group foni qizil tusga kirsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Form Group Has Invalid</title>
  <style>
    .form-group {
      padding: 12px;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      width: 240px;
      font-family: sans-serif;
      transition: background-color 0.3s;
    }
    .form-group:has(input:invalid:focus) {
      border-color: #ef4444;
      background-color: #fef2f2;
    }
    input { width: 90%; padding: 6px; }
  </style>
</head>
<body>
  <div class="form-group">
    <label>Email kiriting:</label>
    <input type="email" placeholder="nom@sayt.uz" required>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`.form-group:has(input:invalid:focus)` ichidagi input xato to'ldirilganda ota guruh ramkasi va fonini ogohlantiruvchi qizil qiladi.

## Ishlash natijasi:
```text
Noto'g'ri email yozilganda butun forma bloki qizg'ish tusga kiradi.
```

---

# 910-Topshiriq: :not() psevdo-klassi bilan istisnolarni belgilash
## Topshiriq sharti:
Oxirgi elementdan tashqari barcha bandlar ostiga chiziq tortish uchun :not(:last-child) qo'llang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>CSS Not Selector</title>
  <style>
    .menu-list {
      list-style: none;
      padding: 0;
      width: 200px;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      font-family: sans-serif;
    }
    .menu-item {
      padding: 10px 14px;
    }
    .menu-item:not(:last-child) {
      border-bottom: 1px solid #e2e8f0; /* Oxirgisidan boshqa barchasida chiziq bo'ladi */
    }
  </style>
</head>
<body>
  <ul class="menu-list">
    <li class="menu-item">Profil</li>
    <li class="menu-item">Sozlamalar</li>
    <li class="menu-item">Chiqish</li>
  </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:not(selektor)` berilgan shartga to'g'ri kelmaydigan barcha elementlarni tanlaydi. Oxirgi band tagida ortiqcha chegara qolishining oldini oladi.

## Ishlash natijasi:
```text
Profil va Sozlamalar ostida chiziq bor, oxirgi Chiqish bandi ostida esa chiziq yo'q.
```

---

# 911-Topshiriq: :focus-visible vs :focus (Klaviatura foydalanuvchilari qulayligi)
## Topshiriq sharti:
Sichqoncha bilan bosilganda noqulay ko'k ramka chiqmasin, lekin Tab klaviaturasi bilan yurilganda yorqin fokus ramkasi ko'rinsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Focus Visible</title>
  <style>
    .access-btn {
      padding: 10px 18px;
      background: #0284c7;
      color: white;
      border: none;
      border-radius: 4px;
      font-family: sans-serif;
      cursor: pointer;
    }
    .access-btn:focus {
      outline: none; /* Sichqoncha bosilganda outline chiqmaydi */
    }
    .access-btn:focus-visible {
      outline: 3px solid #f59e0b; /* Faqat klaviatura Tab bilan kelganda chiqadi */
      outline-offset: 2px;
    }
  </style>
</head>
<body>
  <button class="access-btn">Tab tugmasini bosing</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:focus-visible` faqat foydalanuvchi klaviatura (Tab) orqali elementga kelgandagina fokus ramkasini yoqadi. Sichqoncha bosilganda esa dizaynni buzuvchi ramka paydo bo'lmaydi.

## Ishlash natijasi:
```text
Sichqoncha bilan bosganda ramka chiqmaydi, klaviaturadan Tab bosilganda esa yorqin sariq ramka paydo bo'ladi.
```

---

# 912-Topshiriq: ::before va ::after bilan dekorativ qo'shtirnoqlar qo'yish
## Topshiriq sharti:
Iqtibos matnining boshiga va oxiriga psevdo-elementlar yordamida katta nafis qo'shtirnoqlar joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Before and After Quotes</title>
  <style>
    .quote-box {
      font-family: serif;
      font-size: 18px;
      font-style: italic;
      color: #334155;
      padding: 20px;
      background: #f8fafc;
      border-radius: 8px;
      width: 280px;
    }
    .quote-box::before {
      content: "“";
      font-size: 36px;
      color: #2563eb;
      line-height: 0;
      margin-right: 6px;
      vertical-align: -10px;
    }
    .quote-box::after {
      content: "”";
      font-size: 36px;
      color: #2563eb;
      line-height: 0;
      margin-left: 6px;
      vertical-align: -10px;
    }
  </style>
</head>
<body>
  <div class="quote-box">Ilm olish eng yaxshi boylikdir.</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`::before` va `::after` HTML ga ortiqcha teglar qo'shmasdan CSS orqali sof vizual elementlar kiritish imkonini beradi. `content` xususiyati bo'lishi shart.

## Ishlash natijasi:
```text
Matn boshida va oxirida chiroyli ko'k rangli katta qo'shtirnoqlar aks etadi.
```

---

# 913-Topshiriq: ::marker psevdo-elementi bilan ro'yxat nuqtalarini bezash
## Topshiriq sharti:
ul li ro'yxatining nuqtalarini yashil qushcha yoki qizil rangga aylantiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Marker Pseudo Element</title>
  <style>
    ul.custom-markers {
      font-family: sans-serif;
      padding-left: 20px;
    }
    ul.custom-markers li::marker {
      color: #16a34a;
      content: "✔ ";
      font-size: 14px;
    }
  </style>
</head>
<body>
  <ul class="custom-markers">
    <li>HTML5 Semantikasi</li>
    <li>CSS3 Flexbox va Grid</li>
    <li>Responsive Dizayn</li>
  </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
`::marker` ro'yxatlardagi (`li`) standart qora nuqta yoki raqamlarning rangini, o'lchamini yoki belgisini to'g'ridan-to'g'ri boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Standart qora doiralar o'rnida chiroyli yashil qushcha belgilari chiqadi.
```

---

# 914-Topshiriq: ::selection psevdo-elementi bilan matn belgilash rangini o'zgartirish
## Topshiriq sharti:
Foydalanuvchi kursor bilan matnni belgilaganda fon sariq, matn esa to'q qora bo'lsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Selection Pseudo Element</title>
  <style>
    ::selection {
      background-color: #fef08a; /* Och sariq marker foni */
      color: #0f172a;            /* Qora matn */
    }
    p { font-family: sans-serif; font-size: 16px; line-height: 1.6; }
  </style>
</head>
<body>
  <p>Ushbu matnni sichqoncha bilan belgilab ko'ring. Standart ko'k rang o'rniga maxsus sariq marker rangi paydo bo'ladi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`::selection` foydalanuvchi sahifadagi matnni nusxalash yoki o'qish uchun kursor bilan ajratgan paytidagi fon va harf rangini boshqaradi.

## Ishlash natijasi:
```text
Matn kursor bilan belgilanganda kantselyariya flomasteri bilan chizilgandek sariq bo'yaladi.
```

---

# 915-Topshiriq: ::placeholder psevdo-elementi bilan kiritish maydonini bezash
## Topshiriq sharti:
Inputdagi maslahat matnini kursiv va och moviy rangda ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Placeholder Style</title>
  <style>
    .custom-input {
      width: 220px;
      padding: 10px;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      font-family: sans-serif;
    }
    .custom-input::placeholder {
      color: #93c5fd;
      font-style: italic;
      font-size: 13px;
    }
  </style>
</head>
<body>
  <input type="text" class="custom-input" placeholder="Ismingizni yozing...">
</body>
</html>
```

## Tushuntirish va Mantiq:
`::placeholder` input yoki textarea ichidagi yo'riqnoma matnining rangi, shrifti va shaffofligini stillashtirish uchun xizmat qiladi.

## Ishlash natijasi:
```text
Input ichida och moviy qiya harflar bilan maslahat yozuvi ko'rinadi.
```

---

# 916-Topshiriq: CSS Nesting (Mahalliy ichma-ich yozish sintaksisi)
## Topshiriq sharti:
Sass ishlatmasdan toza brauzer CSS ichida `&` belgisi bilan nesting qoidasini qo'llang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>CSS Native Nesting</title>
  <style>
    .card {
      background: #f8fafc;
      padding: 16px;
      border-radius: 8px;
      font-family: sans-serif;

      & h3 {
        color: #2563eb;
        margin-top: 0;
      }

      & p {
        color: #64748b;
        font-size: 14px;
      }

      &:hover {
        background: #f1f5f9;
      }
    }
  </style>
</head>
<body>
  <div class="card">
    <h3>Ichma-ich Nesting</h3>
    <p>Toza CSS endi Sass kabi nestingni to'liq qo'llab-quvvatlaydi!</p>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Zamonaviy CSS barcha brauzerlarda mahalliy (native) nestingni qo'llab-quvvatlaydi. `&` joriy selektorga ishora qiladi va kodni o'ta ixcham qiladi.

## Ishlash natijasi:
```text
Ochiq kulrang kartadagi ko'k sarlavha va matn, hover bo'lganda fon to'qroq kulrang bo'ladi.
```

---

# 917-Topshiriq: Accent-color xususiyati bilan barcha inputlarni brendlash
## Topshiriq sharti:
Checkbox, radio va range slayderlarini bitta accent-color: #7c3aed qatori bilan binafsha rangga bo'yang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>CSS Accent Color</title>
  <style>
    body {
      accent-color: #7c3aed; /* Barcha standart inputlar binafsha bo'ladi */
      font-family: sans-serif;
      padding: 20px;
    }
  </style>
</head>
<body>
  <label><input type="checkbox" checked> Qabul qilaman</label><br><br>
  <label><input type="radio" checked> Tanlov A</label><br><br>
  <input type="range" value="70">
</body>
</html>
```

## Tushuntirish va Mantiq:
`accent-color` brauzerning standart checkbox, radio tugma va range slayderlarining faol rangini 1 qatorda o'zgartiradi. Murakkab custom shakllar yasashga ehtiyoj qolmaydi.

## Ishlash natijasi:
```text
Checkbox va radio tanlanganda zamonaviy to'q binafsha rangda yonadi.
```

---

# 918-Topshiriq: Color-mix() funksiyasi bilan ranglarni dinamik aralashtirish
## Topshiriq sharti:
Ko'k rangni 20% oq rang bilan aralashtirib yangi tus hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Color Mix Function</title>
  <style>
    .palette {
      display: flex;
      gap: 10px;
      font-family: sans-serif;
    }
    .swatch {
      width: 100px;
      padding: 14px;
      color: white;
      text-align: center;
      border-radius: 6px;
    }
    .base { background: #2563eb; }
    .mixed {
      /* 70% ko'k va 30% oq aralashmasi */
      background: color-mix(in srgb, #2563eb 70%, white);
      color: #0f172a;
    }
  </style>
</head>
<body>
  <div class="palette">
    <div class="swatch base">Asl ko'k</div>
    <div class="swatch mixed">Color-Mix</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`color-mix(in srgb, rang1 foiz, rang2)` yangi CSS Color 4 standarti bo'lib, ranglarni to'g'ridan-to'g'ri brauzerda aralashtirish imkonini beradi.

## Ishlash natijasi:
```text
Asl to'q ko'k rang yonida uning oq bilan aralashtirilgan yoqimli och moviy tusi chiqadi.
```

---

# 919-Topshiriq: @supports qoidasi (Feature Queries) bilan yangi xususiyatlarni tekshirish
## Topshiriq sharti:
Agar brauzer display: grid ni qo'llab-quvvatlasa maxsus fon beruvchi @supports shartini yozing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>CSS Supports Feature Query</title>
  <style>
    .feature-test {
      padding: 16px;
      background: #f1f5f9;
      font-family: sans-serif;
      border-radius: 6px;
    }
    @supports (display: grid) {
      .feature-test {
        background: #dcfce7;
        color: #15803d;
        border: 1px solid #86efac;
      }
    }
  </style>
</head>
<body>
  <div class="feature-test">Brauzeringiz CSS Grid texnologiyasini to'liq qo'llab-quvvatlaydi!</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`@supports (xususiyat: qiymat)` brauzer ma'lum bir yangi CSS xususiyatini tushunish yoki tushunmasligini tekshiradi. Progressiv takomillashtirish (progressive enhancement) uchun xizmat qiladi.

## Ishlash natijasi:
```text
Zamonaviy brauzerda yashil hoshiyali tasdiqlovchi quti chiqadi.
```

---

# 920-Topshiriq: Dark Mode boshqaruvi: Data-theme atributi va CSS o'zgaruvchilari
## Topshiriq sharti:
html[data-theme='dark'] orqali barcha ranglarni o'zgaruvchilar bilan bir zumda o'zgartiruvchi tizim quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <title>Data Theme Dark Mode</title>
  <style>
    :root {
      --bg-page: #ffffff;
      --text-page: #0f172a;
      --card-bg: #f8fafc;
      --card-border: #e2e8f0;
    }
    [data-theme="dark"] {
      --bg-page: #0f172a;
      --text-page: #f8fafc;
      --card-bg: #1e293b;
      --card-border: #334155;
    }
    body {
      background-color: var(--bg-page);
      color: var(--text-page);
      font-family: sans-serif;
      padding: 20px;
    }
    .panel {
      background-color: var(--card-bg);
      border: 1px solid var(--card-border);
      padding: 20px;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <div class="panel">
    <h3>Tungi Rejim Faol</h3>
    <p>data-theme="dark" yordamida o'zgaruvchilar bir lahzada yangilandi.</p>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`data-theme` atributi va CSS o'zgaruvchilari kombinatsiyasi dunyodagi eng ilg'or saytlarning (GitHub, Twitter) mavzularni almashtirish mezonidir.

## Ishlash natijasi:
```text
To'q qora fonda oq matnli va to'q kulrang panelli mukammal qorong'i rejim.
```

---

# 921-Topshiriq: CSS Custom Properties bilan dinamik masofalar va chekinishlar
## Topshiriq sharti:
--spacing-unit o'zgaruvchisi orqali padding va gap o'lchamlarini proporsional hisoblang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Spacing Variables</title>
  <style>
    :root { --space: 8px; }
    .box {
      padding: calc(var(--space) * 3); /* 24px */
      margin-bottom: calc(var(--space) * 2); /* 16px */
      background: #f1f5f9;
      border-radius: var(--space);
      font-family: sans-serif;
    }
  </style>
</head>
<body>
  <div class="box">Proporsional Masofa</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Bitta `--space: 8px` qiymatini o'zgartirish orqali butun saytdagi hoshiyalar masshtabini darhol o'zgartirish mumkin.

## Ishlash natijasi:
```text
24px padding va 8px burchakka ega kulrang to'rtburchak.
```

---

# 922-Topshiriq: CSS Nesting da bevosita bola selektori (& > child)
## Topshiriq sharti:
Nesting ichida bevosita farzand elementlarni qat'iy stillashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Nesting Direct Child</title>
  <style>
    .menu {
      list-style: none;
      padding: 0;
      font-family: sans-serif;

      & > li {
        padding: 8px;
        background: #e2e8f0;
        margin-bottom: 4px;
      }
    }
  </style>
</head>
<body>
  <ul class="menu">
    <li>Band 1</li>
    <li>Band 2</li>
  </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
`& > li` faqat bevosita farzand bo'lgan ro'yxat bandlariga qo'llaniladi.

## Ishlash natijasi:
```text
Kulrang fonli ikkita ro'yxat bandi.
```

---

# 923-Topshiriq: :has() bilan checkbox tanlanganda ota kartaning belgilanishi
## Topshiriq sharti:
Checkbox tanlangan onda (:checked) uning butun ota kartasi yashil bo'lsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Has Checked</title>
  <style>
    .select-card {
      padding: 14px;
      border: 2px solid #cbd5e1;
      border-radius: 6px;
      font-family: sans-serif;
      width: 220px;
      margin-bottom: 8px;
      cursor: pointer;
    }
    .select-card:has(input:checked) {
      border-color: #2563eb;
      background-color: #eff6ff;
    }
  </style>
</head>
<body>
  <label class="select-card">
    <input type="checkbox" checked> Premium Obuna
  </label>
</body>
</html>
```

## Tushuntirish va Mantiq:
Foydalanuvchi checkboxga bosganda uning ota kartasi ko'k hoshiyaga kiradi va to'liq interaktiv ko'rinadi.

## Ishlash natijasi:
```text
Tanlangan checkbox sababli karta och ko'k fon va to'q ko'k chegarada turadi.
```

---

# 924-Topshiriq: Color-mix() bilan shaffof fon hosil qilish (Opacity alternativi)
## Topshiriq sharti:
color-mix orqali asosiy rangdan 15% olib, shaffof fon hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Color Mix Transparent</title>
  <style>
    :root { --brand: #2563eb; }
    .tint-box {
      background: color-mix(in srgb, var(--brand) 15%, transparent);
      color: var(--brand);
      padding: 14px;
      border-radius: 6px;
      font-family: sans-serif;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="tint-box">15% Brand Rangi Foni</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`color-mix(in srgb, rang 15%, transparent)` matn rangiga ta'sir qilmasdan toza 15% lik fon yaratadi.

## Ishlash natijasi:
```text
Och moviy shaffof fonga ega ko'k yozuvli nishon.
```

---

# 925-Topshiriq: Scroll-driven Animatsiyalar uchun animation-timeline: scroll() tayyorgarligi
## Topshiriq sharti:
Sahifa skroll bo'lishiga qarab o'sib boruvchi progress bar strukturasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Scroll Progress Bar</title>
  <style>
    .scroll-line {
      position: fixed;
      top: 0;
      left: 0;
      height: 4px;
      background: #2563eb;
      width: 100%;
      transform-origin: left;
    }
  </style>
</head>
<body>
  <div class="scroll-line"></div>
  <p style="font-family:sans-serif; padding-top:20px;">Sahifaning yuqori qismidagi o'qish ko'rsatkichi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Skroll jarayonini kuzatuvchi yuqori tasma zamonaviy veb maqolalarining ajralmas qismidir.

## Ishlash natijasi:
```text
Ekranning eng yuqori chetida ko'k rangli ingichka chiziqcha.
```

---

# 926-Topshiriq: Nesting ichida psevdo-elementlar qo'llash (&::before)
## Topshiriq sharti:
Nesting ichida &::before orqali ikonka yoki rangli nuqta qo'ying.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Nesting Pseudo</title>
  <style>
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: sans-serif;

      &::before {
        content: "";
        width: 8px;
        height: 8px;
        background: #10b981;
        border-radius: 50%;
      }
    }
  </style>
</head>
<body>
  <span class="badge">Faol Tizim</span>
</body>
</html>
```

## Tushuntirish va Mantiq:
`&::before` sintaksisi nesting qoidasi ichida soxta elementlarni juda toza yozish imkonini beradi.

## Ishlash natijasi:
```text
Yashil nuqtacha va uning yonida 'Faol Tizim' yozuvi.
```

---

# 927-Topshiriq: CSS Custom Properties yordamida dinamik soyalar (Box Shadow System)
## Topshiriq sharti:
Soyaning xiraligini va masofasini o'zgaruvchilar bilan boshqaring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Shadow Variables</title>
  <style>
    :root {
      --sh-y: 4px;
      --sh-blur: 10px;
      --sh-color: rgba(0, 0, 0, 0.1);
    }
    .shadow-card {
      box-shadow: 0 var(--sh-y) var(--sh-blur) var(--sh-color);
      padding: 20px;
      background: white;
      border-radius: 8px;
      font-family: sans-serif;
      width: 200px;
      transition: --sh-y 0.3s;
    }
  </style>
</head>
<body>
  <div class="shadow-card">O'zgaruvchan Soya</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Soya parametrlarini o'zgaruvchilarga chiqarish dizayn tizimlarida (Design Systems) bir xil chuqurlikni saqlaydi.

## Ishlash natijasi:
```text
Yumshoq soyaga ega oq kartochka.
```

---

# 928-Topshiriq: :is() bilan bir nechta tugma holatlarini birlashtirish
## Topshiriq sharti:
:is(:hover, :focus, :active) orqali tugmaning barcha faol holatlariga bitta stil bering.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Is State Combine</title>
  <style>
    .interactive-btn {
      padding: 10px 18px;
      background: #e2e8f0;
      border: 1px solid #cbd5e1;
      border-radius: 4px;
      cursor: pointer;
      font-family: sans-serif;

      &:is(:hover, :focus) {
        background: #2563eb;
        color: white;
        border-color: #2563eb;
      }
    }
  </style>
</head>
<body>
  <button class="interactive-btn">Hover yoki Focus</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
Nesting va `:is(:hover, :focus)` kodi bir vaqtning o'zida ham sichqoncha, ham klaviatura reaksiyasini yozadi.

## Ishlash natijasi:
```text
Tugma ustiga kelganda yoki Tab bilan fokuslanganda ko'k fonga o'tadi.
```

---

# 929-Topshiriq: Text-wrap: balance bilan sarlavhalarni estetik tenglash
## Topshiriq sharti:
Sarlavhaning ikkinchi qatorida yolg'iz bitta so'z qolib ketmasligi uchun text-wrap: balance qo'llang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Text Wrap Balance</title>
  <style>
    .balanced-title {
      font-family: sans-serif;
      font-size: 20px;
      width: 260px;
      text-wrap: balance; /* Qatorlardagi so'zlar sonini teng taqsimlaydi */
      background: #f8fafc;
      padding: 12px;
      border-left: 3px solid #2563eb;
    }
  </style>
</head>
<body>
  <h3 class="balanced-title">HTML va CSS bo'yicha eng mukammal ta'limiy qo'llanma</h3>
</body>
</html>
```

## Tushuntirish va Mantiq:
`text-wrap: balance` yangi CSS xususiyati bo'lib, sarlavha satrlaridagi so'zlarni avtomatik muvozanatlaydi va so'nggi qatordagi bitta yetim so'zni (widow) yo'qotadi.

## Ishlash natijasi:
```text
So'zlari ikki qatorga chiroyli va teng taqsimlangan ko'rkam sarlavha.
```

---

# 930-Topshiriq: O'zgaruvchilar orqali tugma o'lchamlari (Small, Medium, Large)
## Topshiriq sharti:
--btn-size o'zgaruvchisiga qarab tugmaning padding va shrifti o'zgarsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Button Size Variables</title>
  <style>
    .btn {
      --size: 14px;
      font-size: var(--size);
      padding: calc(var(--size) * 0.6) calc(var(--size) * 1.2);
      background: #3b82f6;
      color: white;
      border: none;
      border-radius: 4px;
      font-family: sans-serif;
    }
    .btn-lg { --size: 18px; }
  </style>
</head>
<body>
  <button class="btn">Oddiy</button>
  <button class="btn btn-lg">Katta Tugma</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
Bitta `--size` o'zgaruvchisi barcha ichki mutanosibliklarni avtomatik hisoblaydi.

## Ishlash natijasi:
```text
Biri ixcham, biri esa mutanosib katta ikkita ko'k tugma.
```

---

# 931-Topshiriq: :has() bilan bo'sh bo'lmagan ro'yxatni aniqlash
## Topshiriq sharti:
Agar ro'yxat ichida li bo'lsa hoshiya chiqsin, bo'sh bo'lsa hech narsa ko'rinmasin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Has Child Elements</title>
  <style>
    ul.feed-list:has(li) {
      border: 1px solid #cbd5e1;
      padding: 10px 24px;
      border-radius: 6px;
      font-family: sans-serif;
    }
  </style>
</head>
<body>
  <ul class="feed-list">
    <li>Yangi bildirishnoma</li>
  </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:has(li)` ro'yxatda kamida bitta element borligini tekshiradi va bo'sh bloklarning xunuk hoshiya bilan turishining oldini oladi.

## Ishlash natijasi:
```text
Ichida xabar bo'lgani uchun hoshiyali toza ro'yxat paneli chiqadi.
```

---

# 932-Topshiriq: CSS Custom Properties bilan SVG ranglarini boshqarish
## Topshiriq sharti:
SVG fill va stroke parametrlarini --icon-color o'zgaruvchisiga bog'lang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>SVG Color Variables</title>
  <style>
    :root { --icon-color: #ef4444; }
    .icon-svg {
      fill: var(--icon-color);
      width: 32px;
      height: 32px;
    }
  </style>
</head>
<body>
  <svg class="icon-svg" viewBox="0 0 24 24">
    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
  </svg>
</body>
</html>
```

## Tushuntirish va Mantiq:
SVG ichidagi chiziq va bo'yoqlarni CSS o'zgaruvchilari orqali xohlagan joyda boshqarish mumkin.

## Ishlash natijasi:
```text
Qizil rangdagi vektor yurakcha ikonkasi.
```

---

# 933-Topshiriq: Nesting ichida media queries yozish (Co-located Responsive Styles)
## Topshiriq sharti:
Komponentning media querysini to'g'ridan-to'g'ri o'z blokining ichiga joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Nested Media Queries</title>
  <style>
    .widget {
      padding: 12px;
      background: #f1f5f9;
      font-family: sans-serif;

      @media (min-width: 600px) {
        padding: 24px;
        background: #dbeafe;
      }
    }
  </style>
</head>
<body>
  <div class="widget">Ichki Media Query</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Media so'rovlarni alohida fayl oxirida emas, komponentning o'z qavslari ichida yozish kod arxitekturasini juda toza saqlaydi.

## Ishlash natijasi:
```text
Mobilda kulrang, 600px dan oshganda esa ko'k rangga aylanuvchi quti.
```

---

# 934-Topshiriq: Min() va Max() orqali responsiv shrift o'lchami
## Topshiriq sharti:
max(16px, 1.2vw) orqali shrift hech qachon 16px dan kichik bo'lmasligini kafolatlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Max Function Typography</title>
  <style>
    .safe-text {
      font-size: max(16px, 1.2vw);
      font-family: sans-serif;
    }
  </style>
</head>
<body>
  <p class="safe-text">Ushbu matn hech qachon 16px dan kichraymaydi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`max(16px, 1.2vw)` kichik ekranlarda ham matnning 16px dan kichik bo'lib o'qilmay qolishiga yo'l qo'ymaydi.

## Ishlash natijasi:
```text
Xavfsiz va qulay o'qiluvchi matn.
```

---

# 935-Topshiriq: Color-mix() bilan hover rangini avtomatik to'qroq qilish
## Topshiriq sharti:
Har bir rang uchun alohida hover kodi yozmasdan, 15% qora aralashtiruvchi universal hover qoidasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Auto Darken Hover</title>
  <style>
    .btn-mix {
      --bg: #10b981;
      background: var(--bg);
      color: white;
      border: none;
      padding: 10px 18px;
      border-radius: 4px;
      cursor: pointer;
      font-family: sans-serif;
    }
    .btn-mix:hover {
      background: color-mix(in srgb, var(--bg), black 15%);
    }
  </style>
</head>
<body>
  <button class="btn-mix">Avtomatik To'qroq Hover</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
`color-mix` har qanday rangni 15% qora bilan aralashtirib tabiiy to'q rang hosil qiladi.

## Ishlash natijasi:
```text
Yashil tugma ustiga kursor borganda u 15% to'qroq yashil tus oladi.
```

---

# 936-Topshiriq: Psevdo-element ::before yordamida raqamli bosqichlar doirasi
## Topshiriq sharti:
Har bir qator oldiga ::before bilan avtomatik doira qo'ying.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Step Circles Before</title>
  <style>
    .step-item {
      position: relative;
      padding-left: 30px;
      font-family: sans-serif;
      margin-bottom: 12px;
    }
    .step-item::before {
      content: "";
      position: absolute;
      left: 0;
      top: 2px;
      width: 16px;
      height: 16px;
      background: #2563eb;
      border-radius: 50%;
    }
  </style>
</head>
<body>
  <div class="step-item">1-Bosqich: Ro'yxatdan o'tish</div>
  <div class="step-item">2-Bosqich: Darsni boshlash</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`::before` orqali matn oldida chiroyli ko'k doirachalar hosil qilinadi.

## Ishlash natijasi:
```text
Har bir bosqich oldida kichik ko'k dumaloq belgi ko'rinadi.
```

---

# 937-Topshiriq: CSS O'zgaruvchilari yordamida ko'p mavzuli (Multi-theme) kartalar
## Topshiriq sharti:
bitta karta strukturasiga faqat tema sinfini qo'shish bilan qizil, ko'k yoki yashil tus bering.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Multi-theme Component</title>
  <style>
    .theme-card {
      --accent: #64748b;
      border-left: 4px solid var(--accent);
      background: #f8fafc;
      padding: 12px;
      font-family: sans-serif;
      margin-bottom: 8px;
      width: 220px;
    }
    .theme-blue { --accent: #2563eb; }
    .theme-green { --accent: #16a34a; }
  </style>
</head>
<body>
  <div class="theme-card theme-blue">Ko'k mavzudagi karta</div>
  <div class="theme-card theme-green">Yashil mavzudagi karta</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Bitta `--accent` o'zgaruvchisi barcha hoshiya va matn tuslarini o'zgartirish uchun yetarlidir.

## Ishlash natijasi:
```text
Biri ko'k, biri yashil vertikal chiziqli ikkita quti.
```

---

# 938-Topshiriq: :has() bilan tugmasiz formani aniqlash
## Topshiriq sharti:
Agar formada button bo'lmasa, ogohlantiruvchi qizil ramka bering.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Form Not Has Button</title>
  <style>
    form:not(:has(button)) {
      border: 2px dashed #ef4444;
      padding: 10px;
      font-family: sans-serif;
    }
  </style>
</head>
<body>
  <form>
    <input type="text" placeholder="Tugmasiz forma">
    <small style="color:#ef4444;"><br>Ushbu formada yuborish tugmasi yo'q!</small>
  </form>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:not(:has(button))` forma ichida yuborish tugmasi bor-yo'qligini tekshirish uchun o'ta qudratli vositadir.

## Ishlash natijasi:
```text
Tugmasi yo'q forma atrofida qizil punktir ramka paydo bo'ladi.
```

---

# 939-Topshiriq: Text-wrap: pretty bilan so'nggi qator so'zlarini tartibga solish
## Topshiriq sharti:
Paragraf oxirida yolg'iz so'z qolmasligi uchun text-wrap: pretty qo'llang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Text Wrap Pretty</title>
  <style>
    p {
      width: 220px;
      font-family: sans-serif;
      text-wrap: pretty;
      background: #f1f5f9;
      padding: 10px;
    }
  </style>
</head>
<body>
  <p>Veb-dasturlashda matnlar ko'rinishi va ularning o'qilishi eng asosiy omildir.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`text-wrap: pretty` matn oxiridagi bitta so'z pastki qatorga yolg'iz tushib qolishini oldini oladi.

## Ishlash natijasi:
```text
So'zlari silliq taqsimlangan ixcham paragraf matni.
```

---

# 940-Topshiriq: Psevdo-element ::after bilan tashqi havola ikonkasi
## Topshiriq sharti:
Barcha target='_blank' bo'lgan havolalar yoniga avtomatik &nearr; belgisini qo'shing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>External Link After</title>
  <style>
    a[target="_blank"]::after {
      content: " ↗";
      font-size: 12px;
      color: #64748b;
    }
  </style>
</head>
<body>
  <p style="font-family: sans-serif;">
    <a href="https://google.com" target="_blank">Google qidiruvi</a>
  </p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`a[target="_blank"]::after` tashqi havolalarga avtomatik o'q belgisini qo'yadi va foydalanuvchini yangi oynada ochilishi haqida ogohlantiradi.

## Ishlash natijasi:
```text
Havola matni ketidan kichik diagonal strelka (↗) ko'rinadi.
```

---

# 941-Topshiriq: CSS Custom Properties bilan harakatlanuvchi progress aylanasi
## Topshiriq sharti:
--percent: 75 o'zgaruvchisi orqali doiraviy diagrammani bo'yang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Conic Variable Progress</title>
  <style>
    .pie-progress {
      --percent: 75%;
      width: 80px;
      height: 80px;
      border-radius: 50%;
      background: conic-gradient(#2563eb var(--percent), #e2e8f0 0);
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .pie-inner {
      width: 60px;
      height: 60px;
      background: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: sans-serif;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="pie-progress">
    <div class="pie-inner">75%</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`conic-gradient(#2563eb var(--percent), #e2e8f0 0)` orqali faqat bitta o'zgaruvchini o'zgartirish bilan butun progress aylanadi.

## Ishlash natijasi:
```text
75 foizi ko'k bilan to'ldirilgan doiraviy statistika diagrammasi.
```

---

# 942-Topshiriq: Nesting ichida &:nth-child() bilan rangli qatorlar
## Topshiriq sharti:
Nesting sintaksisi ichida juft va toq qatorlar rangini boshqaring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Nesting Nth Child</title>
  <style>
    .strip-list {
      list-style: none;
      padding: 0;
      font-family: sans-serif;

      & li {
        padding: 8px;

        &:nth-child(even) { background: #f8fafc; }
        &:nth-child(odd) { background: #ffffff; }
      }
    }
  </style>
</head>
<body>
  <ul class="strip-list">
    <li>1-Qator</li>
    <li>2-Qator</li>
    <li>3-Qator</li>
  </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
Nesting ichida `&:nth-child(even)` kodni toza va tartibli saqlashga xizmat qiladi.

## Ishlash natijasi:
```text
Oq va och kulrang almashinuvchi qatorlar.
```

---

# 943-Topshiriq: :has() yordamida audio ijro etilayotgan kartani ajratish
## Topshiriq sharti:
Karta ichidagi video yoki audio ijro bo'lganda karta hoshiyasi yonsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Has Playing Media</title>
  <style>
    .media-card {
      padding: 12px;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      width: 240px;
      font-family: sans-serif;
    }
    .media-card:has(audio) {
      background: #eff6ff;
      border-color: #3b82f6;
    }
  </style>
</head>
<body>
  <div class="media-card">
    <p style="margin: 0 0 6px 0;">Audio darslik</p>
    <audio controls style="width: 100%; height: 30px;"></audio>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Media elementining mavjudligi bo'yicha kartani belgilash.

## Ishlash natijasi:
```text
Audio pleeri bor karta ko'k tusda ajralib turadi.
```

---

# 944-Topshiriq: CSS Custom Properties bilan shrift o'lchamlari shkalasi (Typography Scale)
## Topshiriq sharti:
--font-sm, --font-base, --font-lg, --font-xl o'zgaruvchilari tizimini tuzing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Font Scale Variables</title>
  <style>
    :root {
      --text-sm: 12px;
      --text-base: 16px;
      --text-lg: 20px;
    }
    body { font-family: sans-serif; }
    .sm { font-size: var(--text-sm); color: #64748b; }
    .base { font-size: var(--text-base); }
    .lg { font-size: var(--text-lg); font-weight: bold; }
  </style>
</head>
<body>
  <div class="lg">Katta sarlavha</div>
  <div class="base">Asosiy matn o'lchami</div>
  <div class="sm">Kichik izoh matni</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Shrift shkalasi butun loyihada tipografik uyg'unlikni kafolatlaydi.

## Ishlash natijasi:
```text
Uch xil kattalikdagi tartibli iyerarxik matnlar.
```

---

# 945-Topshiriq: :is() va :where() birgalikda (Murakkab selektor zanjiri)
## Topshiriq sharti:
:is(.header, .footer) :where(a, button) sintaksisi bilan havolalarni tekislang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Is Where Combo</title>
  <style>
    :is(header, footer) :where(a) {
      color: #2563eb;
      text-decoration: none;
      font-family: sans-serif;
    }
  </style>
</head>
<body>
  <header><a href="#">Header Havolasi</a></header>
  <footer><a href="#">Footer Havolasi</a></footer>
</body>
</html>
```

## Tushuntirish va Mantiq:
Bir nechta konteynerlar ichidagi turli elementlarni bitta qatorda boshqarish.

## Ishlash natijasi:
```text
Header va footer ichidagi havolalar ko'k rangda chiqadi.
```

---

# 946-Topshiriq: Nesting ichida &:disabled holatini stillashtirish
## Topshiriq sharti:
Nesting ichida nofaol tugmaga kulrang rang va kursor berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Nesting Disabled</title>
  <style>
    .btn {
      padding: 10px 16px;
      background: #2563eb;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-family: sans-serif;

      &:disabled {
        background: #cbd5e1;
        color: #94a3b8;
        cursor: not-allowed;
      }
    }
  </style>
</head>
<body>
  <button class="btn" disabled>Faol Emas</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
`&:disabled` blok ichida nofaol holatni juda qulay boshqaradi.

## Ishlash natijasi:
```text
Kulrang nofaol tugma va taqiqlangan kursor belgisi.
```

---

# 947-Topshiriq: Color-mix() bilan qorong'i va yorug' rejim oraliq rangi
## Topshiriq sharti:
50% oq va 50% qora bilan toza kulrang tus hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Neutral Gray Color Mix</title>
  <style>
    .gray-mix {
      background: color-mix(in srgb, black 50%, white);
      color: white;
      padding: 16px;
      border-radius: 6px;
      font-family: sans-serif;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="gray-mix">50% Black + 50% White</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ranglarni matematik aniqlikda aralashtirish orqali mukammal oraliq tuslar yaratiladi.

## Ishlash natijasi:
```text
O'rta neytral kulrang fonda oq matn.
```

---

# 948-Topshiriq: Psevdo-element ::before bilan yuklanish yoritgichi (Status Dot Glow)
## Topshiriq sharti:
Yashil status nuqtasi atrofida nozik halqa nuri qo'ying.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Status Dot Glow</title>
  <style>
    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-family: sans-serif;
    }
    .dot-glow {
      position: relative;
      width: 10px;
      height: 10px;
      background: #10b981;
      border-radius: 50%;
    }
    .dot-glow::after {
      content: "";
      position: absolute;
      inset: -3px;
      border: 2px solid rgba(16, 185, 129, 0.4);
      border-radius: 50%;
    }
  </style>
</head>
<body>
  <div class="status-badge">
    <div class="dot-glow"></div>
    <span>Server Onlayn</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`::after` nuqtaning atrofida 3px masofada nozik nurli halqacha hosil qiladi.

## Ishlash natijasi:
```text
Halqali yashil onlayn nuqtacha va uning yonida yozuv.
```

---

# 949-Topshiriq: :has() bilan barcha elementlar to'ldirilgan formani aniqlash
## Topshiriq sharti:
Formada barcha maydonlar to'g'ri to'ldirilganda Yuborish tugmasini faollashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Has Form Validation</title>
  <style>
    .smart-form {
      display: flex;
      flex-direction: column;
      gap: 10px;
      width: 240px;
      font-family: sans-serif;
    }
    .submit-btn {
      padding: 10px;
      background: #cbd5e1;
      color: #64748b;
      border: none;
      border-radius: 4px;
      cursor: not-allowed;
    }
    /* Agar forma ichida xato bo'lmasa, tugma yashil bo'ladi */
    .smart-form:not(:has(input:invalid)) .submit-btn {
      background: #16a34a;
      color: white;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <form class="smart-form">
    <input type="text" placeholder="Ism" required value="Anvar">
    <button type="submit" class="submit-btn">Yuborish</button>
  </form>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:not(:has(input:invalid))` forma ichida birorta ham xato qolmaganda tugmani avtomatik yashil va bosiluvchi qiladi.

## Ishlash natijasi:
```text
Input to'g'ri to'ldirilgani sababli yashil faol yuborish tugmasi chiqadi.
```

---

# 950-Topshiriq: To'liq Zamonaviy CSS Dizayn Tizimi (Design Tokens & Theming)
## Topshiriq sharti:
CSS Custom Properties, Nesting, Clamp, Has va Color-Mix ni birlashtirgan to'liq UI kartasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Complete Modern CSS Component</title>
  <style>
    :root {
      --primary: #4f46e5;
      --surface: #ffffff;
      --text: #0f172a;
      --radius: 12px;
    }
    .token-card {
      background: var(--surface);
      color: var(--text);
      border-radius: var(--radius);
      padding: clamp(16px, 3vw, 28px);
      box-shadow: 0 4px 12px color-mix(in srgb, var(--primary) 12%, transparent);
      border: 1px solid color-mix(in srgb, var(--primary) 20%, transparent);
      font-family: sans-serif;
      max-width: 300px;

      & h3 {
        margin: 0 0 8px 0;
        font-size: clamp(18px, 2.5vw, 24px);
        color: var(--primary);
      }

      & p {
        margin: 0;
        font-size: 14px;
        line-height: 1.5;
        color: #64748b;
      }

      &:has(button:hover) {
        border-color: var(--primary);
      }
    }
    .btn-act {
      margin-top: 14px;
      padding: 8px 16px;
      background: var(--primary);
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div class="token-card">
    <h3>Design Tokens</h3>
    <p>O'zgaruvchilar, nesting, clamp va color-mix uyg'unligi.</p>
    <button class="btn-act">Faollashtirish</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu komponent zamonaviy CSS ning barcha ilg'or imkoniyatlarini (Design Tokens, Nesting, Clamp, Has, Color-Mix) mukammal mujassam etgan.

## Ishlash natijasi:
```text
Chiroyli ko'k tusli, soyali va sarlavhali zamonaviy karta va uning ichidagi binafsharang tugma.
```

---

