# Ro'yxatlar va Jadvallar (151-200)

# 151-Topshiriq: Tartibsiz ro'yxat <ul> va <li> asoslari
## Topshiriq sharti:
Mavzuga oid tartibi qat'iy bo'lmagan elementlar ro'yxatini shakllantiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Tartibsiz Ro'yxat</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        ul { line-height: 1.8; color: #1e293b; }
    </style>
</head>
<body>
    <h3>Dasturlashda kerak bo'ladigan ko'nikmalar:</h3>
    <ul>
        <li>Mantiqiy fikrlash</li>
        <li>Algoritmik tahlil</li>
        <li>Doimiy izlanish va sabr</li>
        <li>Jamoada ishlash madaniyati</li>
    </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<ul>` (unordered list) elementi bandlar ketma-ketligi qat'iy tartib talab qilmaydigan ro'yxatlar uchun ishlatiladi. Har bir element `<li>` (list item) ichiga joylashtiriladi va brauzer ularga nuqta (bullet) belgisini qo'yadi.

## Ishlash natijasi:
```text
Qora dumaloq nuqtalar bilan ajratilgan to'rtta ko'nikma ro'yxati chiqadi.
```

---

# 152-Topshiriq: Tartibli ro'yxat <ol> va uning type atributi
## Topshiriq sharti:
Raqamlar, rim raqamlari va harflar bilan belgilanuvchi tartibli ro'yxat tuzing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Tartibli Ro'yxat Turlari</title>
    <style>
        body { font-family: sans-serif; padding: 25px; line-height: 1.6; }
    </style>
</head>
<body>
    <h4>1. Raqamli tartib (Standart):</h4>
    <ol type="1">
        <li>Reja tuzish</li>
        <li>Kod yozish</li>
    </ol>
    <h4>2. Rim raqamlari (type="I"):</h4>
    <ol type="I">
        <li>Kirish qismi</li>
        <li>Amaliy tadqiqot</li>
    </ol>
    <h4>3. Harfli tartib (type="A"):</h4>
    <ol type="A">
        <li>A varianti</li>
        <li>B varianti</li>
    </ol>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<ol>` (ordered list) qat'iy tartibdagi jarayonlarni bildiradi. `type` atributi orqali raqamlash turini o'zgartirish mumkin: '1' (arab raqamlari), 'I' / 'i' (katta/kichik rim raqamlari), 'A' / 'a' (katta/kichik lotin harflari).

## Ishlash natijasi:
```text
Uch xil tartibda (1, 2; I, II; A, B) belgilangan ro'yxatlar ko'rinadi.
```

---

# 153-Topshiriq: <ol> ning start va reversed atributlari
## Topshiriq sharti:
Raqamlashni ixtiyoriy sondan boshlash yoki teskari sanash tartibini o'rnatish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Start va Reversed</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
    </style>
</head>
<body>
    <h4>50-raqamdan boshlanuvchi ro'yxat:</h4>
    <ol start="50">
        <li>HTML Asoslari</li>
        <li>CSS Stillash</li>
    </ol>
    <h4>Ortga sanash (Reversed):</h4>
    <ol reversed>
        <li>Startga tayyorgarlik</li>
        <li>Dvigatelni yoqish</li>
        <li>Uchish!</li>
    </ol>
</body>
</html>
```

## Tushuntirish va Mantiq:
`start='50'` ro'yxat sanog'ini 50 dan boshlaydi. `reversed` mantiqiy atributi esa ro'yxatni teskari tartibda (masalan, 3, 2, 1) raqamlaydi.

## Ishlash natijasi:
```text
Birinchi ro'yxat 50, 51 raqamlarida, ikkinchi ro'yxat 3, 2, 1 ko'rinishida teskari chiqadi.
```

---

# 154-Topshiriq: Ichma-ich joylashgan ro'yxatlar (Nested Lists)
## Topshiriq sharti:
Ko'p pog'onali mundarija yoki mavzular shajarasini tuzish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Ichma-ich Ro'yxatlar</title>
    <style>
        body { font-family: sans-serif; padding: 25px; line-height: 1.6; }
    </style>
</head>
<body>
    <ul>
        <li>Frontend Texnologiyalari
            <ul>
                <li>HTML5
                    <ol>
                        <li>Semantika</li>
                        <li>Formalar</li>
                    </ol>
                </li>
                <li>CSS3</li>
            </ul>
        </li>
        <li>Backend Texnologiyalari</li>
    </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ichki ro'yxat har doim o'z ota `<li>` elementi ichida ochilishi va yopilishi shart. Ochiq qolgan `<ul>` orasiga boshqa `<ul>` qo'yish sintaktik xato hisoblanadi.

## Ishlash natijasi:
```text
Pogonama-pogona o'ngga surilgan chiroyli daraxtsimon aralash ro'yxat aks etadi.
```

---

# 155-Topshiriq: Ta'riflar ro'yxati: <dl>, <dt> va <dd>
## Topshiriq sharti:
Atamalar va ularning izohlarini ifodalovchi semantik lug'at tuzilmasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Definition List</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        dt { font-weight: bold; color: #1e40af; margin-top: 15px; }
        dd { margin-left: 20px; color: #475569; }
    </style>
</head>
<body>
    <h2>Internet Atamalari</h2>
    <dl>
        <dt>DNS (Domain Name System)</dt>
        <dd>Domen nomlarini IP-manzillarga aylantiruvchi global taqsimlangan tizim.</dd>
        <dt>HTTP (Hypertext Transfer Protocol)</dt>
        <dd>Gipermatnli hujjatlarni uzatishning asosiy tarmoq protokoli.</dd>
    </dl>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<dl>` (description list) atamalar va ularning ta'riflari ro'yxatini ifodalaydi. `<dt>` (description term) atama nomi bo'lsa, `<dd>` (description details) uning batafsil tavsifidir.

## Ishlash natijasi:
```text
Ko'k qalin atamalar va ularning ostida biroz surilgan qora-kulrang tavsiflar chiqadi.
```

---

# 156-Topshiriq: list-style-type xususiyati
## Topshiriq sharti:
Ro'yxat markerlarining geometrik shakllarini CSS orqali boshqarish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>List Style Type</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .circle { list-style-type: circle; }
        .square { list-style-type: square; }
        .none { list-style-type: none; padding-left: 0; }
    </style>
</head>
<body>
    <ul class="circle"><li>Doira (circle)</li></ul>
    <ul class="square"><li>Kvadrat (square)</li></ul>
    <ul class="none"><li>Markersiz (none)</li></ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
`list-style-type` xususiyati yordamida standart qora dumaloqni bo'sh ichli aylanaga (circle), to'rtburchakka (square) yoki butunlay ko'rinmas qilib (none) sozlash mumkin.

## Ishlash natijasi:
```text
Uch xil markerli ro'yxat bandlari namoyon bo'ladi.
```

---

# 157-Topshiriq: list-style-image bilan rasm-marker o'rnatish
## Topshiriq sharti:
Ro'yxat bandlari boshiga kichik tasvir belgisini joylashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>List Style Image</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        ul.custom-check {
            list-style-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="%2316a34a"><path d="M20.285 2l-11.285 11.567-5.286-5.011-3.714 3.716 9 8.728 15-15.285z"/></svg>');
            line-height: 2;
        }
    </style>
</head>
<body>
    <ul class="custom-check">
        <li>Tezkor yetkazib berish xizmati</li>
        <li>100% sifat kafolati</li>
        <li>24/7 mijozlar yordami</li>
    </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
`list-style-image` yordamida har qanday SVG yoki PNG rasmni marker sifatida qo'yish mumkin. Bu veb-saytning o'ziga xos brend uslubini yaratishga yordam beradi.

## Ishlash natijasi:
```text
Yashil 'galochka' tasvirli belgilari bilan boshlanuvchi afzalliklar ro'yxati ko'rinadi.
```

---

# 158-Topshiriq: list-style-position (inside vs outside)
## Topshiriq sharti:
Marker matn blokining ichida yoki tashqarisida joylashishini boshqarish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>List Style Position</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        ul { width: 300px; background: #f1f5f9; padding: 15px; margin-bottom: 20px; border: 1px solid #cbd5e1; }
        .out { list-style-position: outside; }
        .ins { list-style-position: inside; }
    </style>
</head>
<body>
    <ul class="out">
        <li><strong>Outside:</strong> Ikkinchi qator marker ostiga kirmaydi, matn tekis joylashadi.</li>
    </ul>
    <ul class="ins">
        <li><strong>Inside:</strong> Marker matnning ichiga kiradi va ikkinchi qator uning tagidan boshlanadi.</li>
    </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
`outside` (standart) rejimida marker matn chegarasidan tashqariga chiqariladi. `inside` rejimida esa marker xuddi oddiy birinchi so'z kabi matn qatorining ichida o'rin oladi.

## Ishlash natijasi:
```text
Kulrang bloklar ichida ikki xil marker joylashuv uslubi taqqoslab ko'rsatiladi.
```

---

# 159-Topshiriq: list-style qisqartma (shorthand) xususiyati
## Topshiriq sharti:
Type, position va image qoidalarini bitta qatorda birlashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>List Style Shorthand</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        ul { list-style: square inside; color: #1e3a8a; font-weight: 500; }
    </style>
</head>
<body>
    <ul>
        <li>Qisqartma sintaksis</li>
        <li>Toza va ixcham kod</li>
    </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
`list-style: square inside;` bitta qatorda ham marker shaklini (square) ham joylashuvini (inside) belgilaydi.

## Ishlash natijasi:
```text
Ichkariga surilgan to'rtburchakli ko'k ro'yxat bandlari paydo bo'ladi.
```

---

# 160-Topshiriq: ::marker psevdo-elementini stillash
## Topshiriq sharti:
Ro'yxat nuqtalari yoki raqamlarining o'lchami va rangini alohida bo'yash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Marker Psevdo Elementi</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        ol li::marker {
            color: #ef4444;
            font-size: 22px;
            font-weight: bold;
        }
        ol { line-height: 2; }
    </style>
</head>
<body>
    <ol>
        <li>Birinchi bosqich</li>
        <li>Ikkinchi bosqich</li>
        <li>Uchinchi bosqich</li>
    </ol>
</body>
</html>
```

## Tushuntirish va Mantiq:
`::marker` zamonaviy CSS psevdo-elementi bo'lib, ro'yxat elementining o'z matniga teginmasdan, faqat uning oldidagi nuqta yoki raqamiga rang, hajm va shrift berish imkonini beradi.

## Ishlash natijasi:
```text
Qizil katta va qalin raqamlar bilan boshlanuvchi qora matnli ro'yxat chiqadi.
```

---

# 161-Topshiriq: CSS hisoblagichlari (Counters: 1.1, 1.2 formatida)
## Topshiriq sharti:
Avtomatik ko'p pog'onali boblar raqamlanishini CSS orqali hosil qilish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>CSS Counters</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        ol.counter-list { list-style-type: none; counter-reset: item; padding-left: 0; }
        ol.counter-list > li { counter-increment: item; margin-bottom: 10px; }
        ol.counter-list > li::before {
            content: "Bob " counter(item) ". ";
            color: #2563eb;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <ol class="counter-list">
        <li>Kirish va asosiy tushunchalar</li>
        <li>Arxitektura va loyihalash</li>
        <li>Xulosa va tavsiyalar</li>
    </ol>
</body>
</html>
```

## Tushuntirish va Mantiq:
`counter-reset` hisoblagichni ishga tushiradi, `counter-increment` har bir bandda uni 1 taga oshiradi, `counter(item)` esa 'Bob 1. ', 'Bob 2. ' ko'rinishida chiqaradi.

## Ishlash natijasi:
```text
Har bir qator oldida moviy rangda 'Bob 1. ', 'Bob 2. ', 'Bob 3. ' yozuvlari bilan boshlanuvchi ro'yxat ko'rinadi.
```

---

# 162-Topshiriq: Ro'yxatdan gorizontal teglar yoki filtrlar yasash
## Topshiriq sharti:
`<ul>` va `<li>` larni zamonaviy qidiruv teglari (tags/badges) ko'rinishiga keltirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Gorizontal Teglar</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .tag-list { list-style: none; padding: 0; display: flex; gap: 10px; flex-wrap: wrap; }
        .tag-list li {
            background: #e0f2fe;
            color: #0369a1;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
        }
        .tag-list li:hover { background: #bae6fd; }
    </style>
</head>
<body>
    <ul class="tag-list">
        <li>#Frontend</li>
        <li>#JavaScript</li>
        <li>#CSS3</li>
        <li>#WebDev</li>
    </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
Semantik ro'yxat `display: flex` yordamida gorizontal teriladi va chegaralari yumaloqlashtirilib interaktiv teglarga aylantiriladi.

## Ishlash natijasi:
```text
Moviy oval shakldagi bosiladigan zamonaviy heshteglar qatori chiqadi.
```

---

# 163-Topshiriq: Vazifalar ro'yxati (Todo list) checkbox bilan
## Topshiriq sharti:
Bajarilgan va rejalashtirilgan amallarni vizual formatlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Todo List</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        .todo-list { list-style: none; padding: 0; max-width: 350px; }
        .todo-item { display: flex; align-items: center; gap: 10px; padding: 10px; border-bottom: 1px solid #f1f5f9; }
        .done { text-decoration: line-through; color: #94a3b8; }
    </style>
</head>
<body>
    <ul class="todo-list">
        <li class="todo-item"><input type="checkbox" checked disabled><span class="done">HTML darslarini tugatish</span></li>
        <li class="todo-item"><input type="checkbox" checked disabled><span class="done">CSS selektorlarini o'rganish</span></li>
        <li class="todo-item"><input type="checkbox"><span style="font-weight:500;">Flexbox layout yaratish</span></li>
    </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ro'yxat ichida `input type='checkbox'` joylashtirilib, bajarilgan amallar `text-decoration: line-through` bilan o'chirilgan uslubda ko'rsatiladi.

## Ishlash natijasi:
```text
Ikkita bajarilgan (usti chizilgan) va bitta rejadagi qator bilan chiroyli ishlar ro'yxati chiqadi.
```

---

# 164-Topshiriq: Vaqt chizig'i (Timeline) ro'yxati
## Topshiriq sharti:
Voqealar ketma-ketligini vertikal chiziq va nuqtalar orqali aks ettiruvchi ro'yxat.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Timeline Ro'yxati</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        .timeline { list-style: none; padding-left: 20px; border-left: 3px solid #3b82f6; margin: 0; }
        .timeline li { position: relative; margin-bottom: 25px; padding-left: 20px; }
        .timeline li::before {
            content: '';
            position: absolute;
            left: -29px;
            top: 2px;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: #3b82f6;
            border: 3px solid #fff;
            box-shadow: 0 0 0 2px #3b82f6;
        }
    </style>
</head>
<body>
    <ul class="timeline">
        <li><strong>2024-yil:</strong> Kompaniyaga asos solindi</li>
        <li><strong>2025-yil:</strong> 10 000-foydalanuvchi qamrab olindi</li>
        <li><strong>2026-yil:</strong> Xalqaro bozorga chiqildi</li>
    </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
Chap tomondagi `border-left` vertikal marshrut chizig'ini, `li::before` esa ushbu marshrut ustidagi yorqin stansiya nuqtalarini yasab beradi.

## Ishlash natijasi:
```text
Chap tomonida ko'k vertikal chiziq va unda nuqtalar qadalgan chiroyli xronologik tarix ro'yxati gavdalanadi.
```

---

# 165-Topshiriq: Jadvalning asosiy poydevori: <table>, <tr>, <th>, <td>
## Topshiriq sharti:
Eng toza va minimal HTML jadval strukturasini yaratish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Asosiy Jadval</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #cbd5e1; padding: 10px 14px; text-align: left; }
        th { background: #f8fafc; font-weight: 600; }
    </style>
</head>
<body>
    <table>
        <tr>
            <th>Ism</th>
            <th>Kasb</th>
            <th>Shahar</th>
        </tr>
        <tr>
            <td>Davron</td>
            <td>Muhandis</td>
            <td>Toshkent</td>
        </tr>
        <tr>
            <td>Nilufar</td>
            <td>Dizayner</td>
            <td>Samarqand</td>
        </tr>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<table>` konteyner, `<tr>` (table row) qator, `<th>` (table header) qalin sarlavha katagi, `<td>` (table data) esa oddiy ma'lumot katakchasi hisoblanadi.

## Ishlash natijasi:
```text
Toza kulrang chegaralarga ega uch ustun va ikki qatordan iborat klassik ma'lumotlar jadvali ko'rinadi.
```

---

# 166-Topshiriq: Jadval sarlavhasi tegi <caption>
## Topshiriq sharti:
Jadvalga rasmiy sarlavha berish va uni to'g'ri joylashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Table Caption</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { border-collapse: collapse; width: 400px; margin: 0 auto; }
        caption { caption-side: top; font-weight: bold; font-size: 16px; margin-bottom: 10px; color: #1e293b; }
        th, td { border: 1px solid #94a3b8; padding: 8px 12px; }
    </style>
</head>
<body>
    <table>
        <caption>2026-yil 1-Chorak Moliyaviy Ko'rsatkichlari</caption>
        <tr><th>Ko'rsatkich</th><th>Qiymat</th></tr>
        <tr><td>Daromad</td><td>120 mln UZS</td></tr>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<caption>` tegi jadvalning rasmiy sarlavhasi bo'lib, har doim `<table>` ochilishi bilanoq birinchi bo'lib yoziladi. U butun jadval kengligi bo'yicha markazlashadi.

## Ishlash natijasi:
```text
Jadval tepasida qalin harflar bilan uning nomi va ostida ma'lumotlar qatori joylashadi.
```

---

# 167-Topshiriq: Semantik jadval bo'limlari: <thead>, <tbody>, <tfoot>
## Topshiriq sharti:
Katta jadvallarni mantiqiy yuqori, o'rta va quyi qismlarga ajratish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Semantik Jadval</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: left; }
        thead { background: #1e293b; color: white; }
        tfoot { background: #f8fafc; font-weight: bold; }
    </style>
</head>
<body>
    <table>
        <thead>
            <tr><th>Mahsulot</th><th>Narx</th></tr>
        </thead>
        <tbody>
            <tr><td>Klaviatura</td><td>250 000</td></tr>
            <tr><td>Sichqoncha</td><td>120 000</td></tr>
        </tbody>
        <tfoot>
            <tr><td>Jami:</td><td>370 000 so'm</td></tr>
        </tfoot>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<thead>` sarlavha qatorini, `<tbody>` asosiy axborot tanasini, `<tfoot>` esa jamlovchi yakuniy qatorni ifodalaydi. Sahifa chop etilganda brauzer har bir yangi varaqda thead ni avtomatik takrorlaydi.

## Ishlash natijasi:
```text
Qora shapkali, o'rtada ma'lumotlari bor va pastida qalin yakuniy summa yozilgan nafis jadval paydo bo'ladi.
```

---

# 168-Topshiriq: Ustunlarni birlashtirish: colspan atributi
## Topshiriq sharti:
Bitta katakchani bir necha ustun bo'ylab cho'zish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Colspan</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        table { border-collapse: collapse; width: 350px; }
        th, td { border: 1px solid #64748b; padding: 8px; text-align: center; }
    </style>
</head>
<body>
    <table>
        <tr>
            <th colspan="2">Foydalanuvchi Ma'lumotlari</th>
        </tr>
        <tr>
            <td>Ism</td>
            <td>Telefon</td>
        </tr>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
`colspan='2'` atributi katakka ikkita ustun kengligini egallashni buyuradi. Bu umumiy sarlavhalar va guruhlash uchun ishlatiladi.

## Ishlash natijasi:
```text
Tepadagi sarlavha katagi pastdagi ikki katak kengligini to'liq qoplab turadi.
```

---

# 169-Topshiriq: Qatorlarni birlashtirish: rowspan atributi
## Topshiriq sharti:
Bitta katakchani bir necha qator bo'yicha vertikal birlashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Rowspan</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { border-collapse: collapse; }
        th, td { border: 1px solid #475569; padding: 10px 15px; }
    </style>
</head>
<body>
    <table>
        <tr>
            <th rowspan="2">Toshkent</th>
            <td>Chilonzor tumani</td>
        </tr>
        <tr>
            <td>Yunusobod tumani</td>
        </tr>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
`rowspan='2'` katakni vertikal bo'yicha 2 ta qator balandligida cho'zadi va pastki qatorning birinchi o'rnini to'ldiradi.

## Ishlash natijasi:
```text
Chap tomonda baland bo'lib turgan 'Toshkent' katagi va o'ngida ikkita tuman qatorlari chiqadi.
```

---

# 170-Topshiriq: <colgroup> va <col> orqali butun ustunlarni stillash
## Topshiriq sharti:
Har bir katakka alohida stil bermasdan, butun bir ustunga rang biriktirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Colgroup</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #cbd5e1; padding: 10px; }
    </style>
</head>
<body>
    <table>
        <colgroup>
            <col style="background-color: #f8fafc; width: 30%;">
            <col style="background-color: #fef3c7; width: 70%;">
        </colgroup>
        <tr><th>ID</th><th>Tavsif</th></tr>
        <tr><td>#001</td><td>Loyiha ma'qullandi</td></tr>
        <tr><td>#002</td><td>Bajarilmoqda</td></tr>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<colgroup>` jadval ustunlarini boshqarishning eng tezkor usulidir. Butun boshli ustunning kengligi va fon rangini bitta `<col>` tegi orqali o'zgartirish mumkin.

## Ishlash natijasi:
```text
Birinchi ustun kulrang fonli, ikkinchi keng ustun esa och sariq fonga bo'yaladi.
```

---

# 171-Topshiriq: border-collapse (collapse vs separate)
## Topshiriq sharti:
Kataklar orasidagi qo'shaloq chiziqlarni yagona chiziqqa aylantirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Border Collapse</title>
    <style>
        body { font-family: sans-serif; padding: 20px; display: flex; gap: 30px; }
        table { width: 200px; border: 1px solid #000; }
        td { border: 1px solid #000; padding: 8px; text-align: center; }
        .sep { border-collapse: separate; }
        .col { border-collapse: collapse; }
    </style>
</head>
<body>
    <table class="sep"><tr><td>Separate</td><td>Qo'shaloq</td></tr></table>
    <table class="col"><tr><td>Collapse</td><td>Yagona</td></tr></table>
</body>
</html>
```

## Tushuntirish va Mantiq:
Sukut bo'yicha brauzerlar `border-collapse: separate` ishlatadi va kataklar orasida oraliq qoladi. Zamonaviy toza dizayn uchun deyarli doim `border-collapse: collapse` tanlanadi.

## Ishlash natijasi:
```text
Chapda qo'shaloq chiziqli eski ko'rinish, o'ngda esa bitta yupqa qora chiziqli zamonaviy jadval ko'rinadi.
```

---

# 172-Topshiriq: border-spacing xususiyati
## Topshiriq sharti:
`separate` rejimida kataklar orasiga masofa qo'yish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Border Spacing</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { border-collapse: separate; border-spacing: 12px; }
        td { background: #3b82f6; color: white; padding: 15px 25px; border-radius: 8px; font-weight: bold; }
    </style>
</head>
<body>
    <table>
        <tr><td>Blok 1</td><td>Blok 2</td></tr>
        <tr><td>Blok 3</td><td>Blok 4</td></tr>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
`border-spacing: 12px` kataklarni bir-biridan mustaqil oraliqqa suradi va har bir katakka `border-radius` berib blokli mozaika yasashga imkon beradi.

## Ishlash natijasi:
```text
Bir-biriga tegmay turgan to'rtta ko'k yumaloq burchakli 'plitka' katakchalari hosil bo'ladi.
```

---

# 173-Topshiriq: empty-cells (show vs hide)
## Topshiriq sharti:
Bo'sh kataklarning hoshiyalarini yashirish yoki ko'rsatish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Empty Cells</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { border-collapse: separate; empty-cells: hide; }
        td { border: 1px solid #dc2626; padding: 10px 20px; }
    </style>
</head>
<body>
    <table>
        <tr><td>To'ldirilgan</td><td>Mavjud</td></tr>
        <tr><td>To'ldirilgan</td><td></td></tr>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
`empty-cells: hide` ichida hech qanday belgi yoki matn bo'lmagan bo'sh kataklarning chegarasi va fonini avtomatik yashiradi.

## Ishlash natijasi:
```text
Ikkinchi qatordagi o'ng tomon bo'sh katakda qizil hoshiya chizilmaydi, bo'sh joy bo'lib qoladi.
```

---

# 174-Topshiriq: caption-side (top vs bottom)
## Topshiriq sharti:
Jadval sarlavhasi uning tepasida yoki pastida chiqishini belgilash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Caption Side</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { border-collapse: collapse; width: 300px; }
        th, td { border: 1px solid #ccc; padding: 8px; }
        caption { caption-side: bottom; font-size: 13px; color: #64748b; padding-top: 8px; }
    </style>
</head>
<body>
    <table>
        <caption>Manba: Davlat Statistika Qo'mitasi, 2026-yil.</caption>
        <tr><th>Viloyat</th><th>Aholi soni</th></tr>
        <tr><td>Samarqand</td><td>4.1 mln</td></tr>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
`caption-side: bottom` jadval izohi yoki manba ma'lumotini jadvalning pastki qismiga joylashtiradi.

## Ishlash natijasi:
```text
Jadval ostida kulrang mayda manba yozuvi paydo bo'ladi.
```

---

# 175-Topshiriq: table-layout: fixed va uning tezligi
## Topshiriq sharti:
Brauzer jadvalni tezkor hisoblab chizishi uchun qat'iy ustun o'lchamlarini belgilash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Table Layout Fixed</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { width: 100%; table-layout: fixed; border-collapse: collapse; }
        th, td { border: 1px solid #cbd5e1; padding: 10px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    </style>
</head>
<body>
    <table>
        <tr>
            <th style="width: 25%;">Foydalanuvchi</th>
            <th style="width: 75%;">JudaUzunKomentariyaMatniKatakdanChiqibKetmasligiKerak</th>
        </tr>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
`table-layout: fixed` rejimida brauzer barcha qatorlardagi matnlarni tahlil qilib o'tirmaydi, balki birinchi qator o'lchamiga qarab butun jadvalni bir zumda render qiladi. Bu minglab qatorli katta jadvallarda sahifa tezligini keskin oshiradi.

## Ishlash natijasi:
```text
To'liq belgilangan foizda turgan, sig'magan matni '...' bo'lib qirqiladigan qat'iy jadval chiqadi.
```

---

# 176-Topshiriq: Zebra chiziqli jadvallar (:nth-child)
## Topshiriq sharti:
Qatorlarni navbatma-navbat oq va och kulrang fonga bo'yash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Zebra Jadval</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; }
        thead { background: #0f172a; color: white; }
        tbody tr:nth-child(even) { background-color: #f8fafc; }
        tbody tr:nth-child(odd) { background-color: #ffffff; }
    </style>
</head>
<body>
    <table>
        <thead><tr><th>#</th><th>Nomi</th><th>Holati</th></tr></thead>
        <tbody>
            <tr><td>1</td><td>Dasturiy ta'minot</td><td>Faol</td></tr>
            <tr><td>2</td><td>Mobil ilova</td><td>Tekshiruvda</td></tr>
            <tr><td>3</td><td>Server klasteri</td><td>Faol</td></tr>
        </tbody>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
`tbody tr:nth-child(even)` juft qatorlarga och fon beradi. Bu ko'zning qator bo'ylab adashmasdan o'qishini osonlashtiradi.

## Ishlash natijasi:
```text
Bir qatori oq, bir qatori och kulrang bo'lib almashinuvchi qulay jadval paydo bo'ladi.
```

---

# 177-Topshiriq: Kursor kelganda qatorni yoritish (Row hover effect)
## Topshiriq sharti:
Foydalanuvchi sichqoncha bilan ko'rib turgan qatorni alohida rang bilan belgilash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Hover Row</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; border-bottom: 1px solid #e2e8f0; }
        tbody tr { transition: background-color 0.15s ease; }
        tbody tr:hover { background-color: #e0f2fe; cursor: pointer; }
    </style>
</head>
<body>
    <table>
        <thead><tr><th>Mijoz</th><th>Hisob raqami</th></tr></thead>
        <tbody>
            <tr><td>"Grand" MCHJ</td><td>2020800099...</td></tr>
            <tr><td>"Ideal" XK</td><td>2020800055...</td></tr>
        </tbody>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
`tbody tr:hover` qoidasi sichqoncha qaysi qatorda turgan bo'lsa, o'sha butun qatorni och moviy rangga bo'yab, foydalanuvchiga qulaylik yaratadi.

## Ishlash natijasi:
```text
Kursor qaysi qator ustiga borsa, o'sha qator chiroyli havorang tusga kiradi.
```

---

# 178-Topshiriq: Jadval bosh qatorini mahkamlash (Sticky Table Header)
## Topshiriq sharti:
Pastga varaqlaganda ham ustun nomlari yo'qolmasdan qolishi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Sticky Header</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .table-wrap { height: 200px; overflow-y: auto; border: 1px solid #cbd5e1; }
        table { width: 100%; border-collapse: collapse; }
        th { position: sticky; top: 0; background: #1e293b; color: white; padding: 10px; z-index: 10; }
        td { padding: 10px; border-bottom: 1px solid #eee; }
    </style>
</head>
<body>
    <div class="table-wrap">
        <table>
            <thead><tr><th>ID</th><th>Mahsulot</th></tr></thead>
            <tbody>
                <tr><td>1</td><td>Tovar A</td></tr>
                <tr><td>2</td><td>Tovar B</td></tr>
                <tr><td>3</td><td>Tovar C</td></tr>
                <tr><td>4</td><td>Tovar D</td></tr>
                <tr><td>5</td><td>Tovar E</td></tr>
                <tr><td>6</td><td>Tovar F</td></tr>
            </tbody>
        </table>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`th { position: sticky; top: 0; }` orqali konteyner ichida varaqlash sodir bo'lganda sarlavha kataklari o'z o'rnida yopishib turadi.

## Ishlash natijasi:
```text
Kichik oynada ro'yxat pastga surilganda qora sarlavha paneli o'zgarmay qoladi.
```

---

# 179-Topshiriq: Jadvalning birinchi ustunini mahkamlash (Sticky first column)
## Topshiriq sharti:
Gorizontal varaqlaganda ism yoki ID ustuni qimirlamay turishi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Sticky Column</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .scroll-box { width: 350px; overflow-x: auto; border: 1px solid #94a3b8; }
        table { border-collapse: collapse; width: 600px; }
        th, td { padding: 8px 12px; border: 1px solid #cbd5e1; white-space: nowrap; }
        .sticky-col { position: sticky; left: 0; background: #f8fafc; z-index: 5; font-weight: bold; }
    </style>
</head>
<body>
    <div class="scroll-box">
        <table>
            <tr><th class="sticky-col">Ism</th><th>Yan</th><th>Fev</th><th>Mar</th><th>Apr</th><th>May</th></tr>
            <tr><td class="sticky-col">Ali</td><td>10</td><td>20</td><td>30</td><td>40</td><td>50</td></tr>
        </table>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`position: sticky; left: 0;` qoidasi ustunni chap burchakka mahkamlaydi. O'ng tomonga qancha surilsa ham birinchi ustun ko'rinib turadi.

## Ishlash natijasi:
```text
Gorizontal surilganda 'Ism' va 'Ali' kataklari chap tomonda mahkam qoladi.
```

---

# 180-Topshiriq: Gorizontal aylanuvchi responsiv jadval
## Topshiriq sharti:
Kichik telefon ekranlarida sahifa buzilmasligi uchun konteynerga aylantirish berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsive Jadval</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .responsive-table { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; }
        table { width: 100%; min-width: 500px; border-collapse: collapse; }
        th, td { border: 1px solid #cbd5e1; padding: 10px; }
    </style>
</head>
<body>
    <div class="responsive-table">
        <table>
            <tr><th>№</th><th>To'liq Ism</th><th>Email Manzil</th><th>Telefon</th><th>Manzil</th></tr>
            <tr><td>1</td><td>Sardor Aliyev</td><td>sardor@mail.uz</td><td>+998901234567</td><td>Toshkent</td></tr>
        </table>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Jadvalni `overflow-x: auto` konteyneriga o'rash mobil qurilmalarda butun sahifani buzmasdan faqat jadvalning o'zini barmoq bilan gorizontal surish imkonini yaratadi.

## Ishlash natijasi:
```text
Keng jadval mobil ekranda ham chiroyli aylanadi, sayt tartibi buzilmaydi.
```

---

# 181-Topshiriq: Mobil ekranda kartochkaga aylanuvchi jadval (Data-label)
## Topshiriq sharti:
Media query orqali jadval qatorlarini alohida kartochka qilib chizish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Card Table</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        table { width: 100%; border-collapse: collapse; }
        @media (max-width: 600px) {
            thead { display: none; }
            tr { display: block; border: 1px solid #cbd5e1; margin-bottom: 12px; border-radius: 8px; padding: 10px; }
            td { display: flex; justify-content: space-between; border: none; padding: 6px 0; }
            td::before { content: attr(data-label); font-weight: bold; color: #475569; }
        }
    </style>
</head>
<body>
    <table>
        <thead><tr><th>Mahsulot</th><th>Narxi</th></tr></thead>
        <tbody>
            <tr>
                <td data-label="Mahsulot:">Noutbuk</td>
                <td data-label="Narxi:">8 000 000 UZS</td>
            </tr>
        </tbody>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
`attr(data-label)` yordamida har bir katak yonida uning sarlavhasi chiqariladi va ekran 600px dan kichrayganda an'anaviy jadval chiroyli kartochkaga aylanadi.

## Ishlash natijasi:
```text
Telefonda ustunlar yo'qolib, o'rniga qulay mobil kartochka shakli paydo bo'ladi.
```

---

# 182-Topshiriq: Talabalar baholari reyting jadvali
## Topshiriq sharti:
Ballar, guruh va reyting o'rnini ifodalovchi akademik jadval.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Reyting Jadvali</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { width: 100%; border-collapse: collapse; max-width: 600px; }
        th, td { padding: 10px 15px; border-bottom: 1px solid #e2e8f0; text-align: left; }
        .rank { font-weight: bold; color: #d97706; }
        .score { font-weight: 600; color: #16a34a; }
    </style>
</head>
<body>
    <table>
        <thead><tr><th>O'rin</th><th>Talaba</th><th>Ball</th></tr></thead>
        <tbody>
            <tr><td class="rank">🥇 1</td><td>Javohir Toshmatov</td><td class="score">98.5</td></tr>
            <tr><td class="rank">🥈 2</td><td>Dildora Rahimova</td><td class="score">96.0</td></tr>
            <tr><td class="rank">🥉 3</td><td>Bobur Mirzayev</td><td class="score">94.2</td></tr>
        </tbody>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
Akademik jadvalda o'rinlar medallar bilan, yuqori ballar esa yashil rangda aniq va o'qishli formatda ajratiladi.

## Ishlash natijasi:
```text
Medallar va yashil baholar bilan bezatilgan toza reyting jadvali chiqadi.
```

---

# 183-Topshiriq: Mahsulot narxlari solishtirma jadvali (Pricing table)
## Topshiriq sharti:
Tarif rejalari va ularning imkoniyatlarini taqqoslash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Pricing Table</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { width: 100%; border-collapse: collapse; text-align: center; }
        th, td { padding: 12px; border: 1px solid #e2e8f0; }
        th:first-child, td:first-child { text-align: left; }
        .highlight { background: #eff6ff; font-weight: bold; color: #2563eb; }
    </style>
</head>
<body>
    <table>
        <thead>
            <tr><th>Imkoniyatlar</th><th>Boshlang'ich</th><th class="highlight">Professional</th></tr>
        </thead>
        <tbody>
            <tr><td>Loyihalar soni</td><td>5 ta</td><td class="highlight">Cheksiz</td></tr>
            <tr><td>Foydalanuvchilar</td><td>1 kishi</td><td class="highlight">10 kishi</td></tr>
            <tr><td>24/7 Yordam</td><td>&times;</td><td class="highlight">&check;</td></tr>
        </tbody>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
O'rta yoki eng ommabop tarif ustuni `.highlight` orqali och moviy rangda ajratilib, mijoz diqqatini jalb qiladi.

## Ishlash natijasi:
```text
Professional ustuni moviy fon bilan alohida ta'kidlangan taqqoslash jadvali chiqadi.
```

---

# 184-Topshiriq: Haftalik dars jadvali (Timetable)
## Topshiriq sharti:
Hafta kunlari va dars soatlarini qamrab oluvchi to'liq setka.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Dars Jadvali</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        table { width: 100%; border-collapse: collapse; text-align: center; }
        th, td { border: 1px solid #94a3b8; padding: 10px; }
        th { background: #334155; color: white; }
    </style>
</head>
<body>
    <table>
        <tr><th>Vaqt</th><th>Dushanba</th><th>Seshanba</th><th>Chorshanba</th></tr>
        <tr><td>09:00 - 10:30</td><td>Matematika</td><td>Fizika</td><td>Dasturlash</td></tr>
        <tr><td>10:45 - 12:15</td><td>Ingliz tili</td><td>Tarix</td><td>Web dizayn</td></tr>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
Hafta kunlari va dars vaqtlari qat'iy matrisa asosida tartiblangan.

## Ishlash natijasi:
```text
Universitet va maktablar uchun mos darslar jadvali paydo bo'ladi.
```

---

# 185-Topshiriq: Xodimlar ma'lumotnomasi jadvali
## Topshiriq sharti:
Lavozim, bo'lim va email kontaktlaridan iborat korporativ ro'yxat.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Xodimlar Jadvali</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px 14px; border-bottom: 1px solid #cbd5e1; }
        .badge { background: #dcfce7; color: #166534; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
    </style>
</head>
<body>
    <table>
        <thead><tr><th>Xodim</th><th>Lavozim</th><th>Holati</th></tr></thead>
        <tbody>
            <tr><td>Nodir Qosimov</td><td>Bosh Dasturchi</td><td><span class="badge">Ishda</span></td></tr>
            <tr><td>Ziyoda Ergasheva</td><td>HR Menejer</td><td><span class="badge">Ishda</span></td></tr>
        </tbody>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
Xodimning ish holati kichik yashil nishon (badge) orqali yorqin ifodalanadi.

## Ishlash natijasi:
```text
Xodimlar ismi va yashil 'Ishda' ko'rsatkichli toza korporativ jadval ko'rinadi.
```

---

# 186-Topshiriq: Moliyaviy balans hisoboti jadvali (tfoot da jami summa)
## Topshiriq sharti:
Kirim, chiqim va yakuniy qoldiqni hisoblovchi buxgalteriya hujjati.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Moliyaviy Balans</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums; }
        th, td { padding: 8px 12px; border-bottom: 1px solid #e2e8f0; text-align: right; }
        th:first-child, td:first-child { text-align: left; }
        tfoot td { font-weight: bold; border-top: 2px solid #0f172a; border-bottom: 2px double #0f172a; }
    </style>
</head>
<body>
    <table>
        <thead><tr><th>Modda</th><th>Kirim</th><th>Chiqim</th></tr></thead>
        <tbody>
            <tr><td>Xizmat ko'rsatish</td><td>50 000 000</td><td>-</td></tr>
            <tr><td>Server ijarasi</td><td>-</td><td>4 500 000</td></tr>
        </tbody>
        <tfoot>
            <tr><td>Sof foyda:</td><td colspan="2">45 500 000 UZS</td></tr>
        </tfoot>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
`font-variant-numeric: tabular-nums` sonlarning raqamlari bir tekis qatorlashishini ta'minlaydi. Ikki qavatli chiziq (`border-bottom: 2px double`) esa xalqaro buxgalteriya standarti hisoblanadi.

## Ishlash natijasi:
```text
Raqamlari o'ngga tekislangan, tagida klassik buxgalteriya chizig'i bor moliyaviy jadval aks etadi.
```

---

# 187-Topshiriq: Sport turnir jadvali va ochkolar
## Topshiriq sharti:
Futbol chempionati jadvali (O'yinlar, G'alaba, Durang, Mag'lubiyat, Ochko).

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Turnir Jadvali</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { width: 100%; border-collapse: collapse; text-align: center; }
        th, td { padding: 10px; border-bottom: 1px solid #cbd5e1; }
        th:nth-child(2), td:nth-child(2) { text-align: left; font-weight: bold; }
        .pts { font-weight: bold; color: #2563eb; }
    </style>
</head>
<body>
    <table>
        <thead><tr><th>№</th><th>Jamoa</th><th>O'</th><th>G'</th><th>D</th><th>M</th><th>Ochko</th></tr></thead>
        <tbody>
            <tr><td>1</td><td>Paxtakor</td><td>10</td><td>8</td><td>1</td><td>1</td><td class="pts">25</td></tr>
            <tr><td>2</td><td>Navbahor</td><td>10</td><td>7</td><td>2</td><td>1</td><td class="pts">23</td></tr>
        </tbody>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
Jamoa nomi chapga, o'yin statistikasi esa markazga va ochkolar qalin moviy rangda ajratilgan.

## Ishlash natijasi:
```text
Sport saytlariga xos futbol ligasi turnir jadvali namoyon bo'ladi.
```

---

# 188-Topshiriq: Aeroport reyslari uchish/qo'nish doskasi
## Topshiriq sharti:
Xalqaro aviaparvozlar holatini bildiruvchi tablo jadvali.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Parvozlar Tablosi</title>
    <style>
        body { font-family: 'Courier New', monospace; background: #000; color: #facc15; padding: 30px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; border-bottom: 1px dashed #444; text-align: left; }
        th { color: #fff; }
        .on-time { color: #22c55e; }
    </style>
</head>
<body>
    <h2>UCHISH TABLOSI / DEPARTURES</h2>
    <table>
        <thead><tr><th>Reys</th><th>Yo'nalish</th><th>Vaqt</th><th>Holati</th></tr></thead>
        <tbody>
            <tr><td>HY-101</td><td>Nyu-York</td><td>11:45</td><td class="on-time">Uchib ketdi</td></tr>
            <tr><td>HY-271</td><td>Istanbul</td><td>12:30</td><td style="color:#facc15;">Ro'yxatga olish</td></tr>
        </tbody>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
Qora fonga sariq va yashil monospaced shrift berilib haqiqiy aeroport tablolari dizayni hosil qilinadi.

## Ishlash natijasi:
```text
Aeroport zalidagi yorug'lik tablosiga o'xshash qora-sariq reyslar jadvali paydo bo'ladi.
```

---

# 189-Topshiriq: Pochta jo'natmasini kuzatish bosqichlari jadvali
## Topshiriq sharti:
Posilkaning qabul qilinishi, bojxona va yetkazilish yo'li jadvali.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Jo'natma Kuzatuvi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: left; }
        .date { color: #64748b; font-size: 13px; }
    </style>
</head>
<body>
    <table>
        <thead><tr><th>Sana / Vaqt</th><th>Manzil</th><th>Holat</th></tr></thead>
        <tbody>
            <tr><td class="date">2026-06-01 10:30</td><td>Toshkent Saralash Markazi</td><td>Yetib keldi</td></tr>
            <tr><td class="date">2026-06-02 14:15</td><td>Chilonzor Aloqa Bo'limi</td><td>Topshirishga tayyor</td></tr>
        </tbody>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
Jo'natmaning har bir nuqtasi sana va vaqt bilan tartibli qayd etiladi.

## Ishlash natijasi:
```text
Posilka bosqichlari aniq yozilgan toza kuzatuv jadvali ko'rinadi.
```

---

# 190-Topshiriq: Taomlar kaloriyasi va ozuqaviy qiymati jadvali
## Topshiriq sharti:
Oqsillar, yog'lar va uglevodlar grammini aks ettiruvchi fitnes jadvali.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Kaloriya Jadvali</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { width: 100%; border-collapse: collapse; max-width: 500px; }
        th, td { border: 1px solid #e2e8f0; padding: 8px 12px; text-align: center; }
        th:first-child, td:first-child { text-align: left; font-weight: bold; }
    </style>
</head>
<body>
    <table>
        <thead><tr><th>Mahsulot (100g)</th><th>Kkal</th><th>Oqsil</th><th>Yog'</th><th>Uglevod</th></tr></thead>
        <tbody>
            <tr><td>Tovuq filesi</td><td>165</td><td>31g</td><td>3.6g</td><td>0g</td></tr>
            <tr><td>Guruch</td><td>130</td><td>2.7g</td><td>0.3g</td><td>28g</td></tr>
        </tbody>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ozuqa moddalari grammlari va kaloriya miqdori qat'iy ustunlarda ko'rsatiladi.

## Ishlash natijasi:
```text
Sportchilar va to'g'ri ovqatlanuvchilar uchun mos ozuqa qiymati jadvali chiqadi.
```

---

# 191-Topshiriq: Texnik spetsifikatsiyalar taqqoslovi jadvali
## Topshiriq sharti:
Ikki smartfon yoki kompyuter parametrlarini yuzma-yuz solishtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Spetsifikatsiyalar</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; border-bottom: 1px solid #cbd5e1; }
        .param { font-weight: bold; color: #475569; width: 30%; }
    </style>
</head>
<body>
    <table>
        <thead><tr><th>Parametr</th><th>Model X</th><th>Model Y</th></tr></thead>
        <tbody>
            <tr><td class="param">Protsessor</td><td>Snapdragon 8 Gen 3</td><td>Apple A18 Pro</td></tr>
            <tr><td class="param">Akkumulyator</td><td>5000 mAh</td><td>4422 mAh</td></tr>
            <tr><td class="param">Ekran yangilanishi</td><td>120 Hz</td><td>120 Hz</td></tr>
        </tbody>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
Birinchi ustun parametr nomi, qolgan ikki ustun esa modellarning ko'rsatkichlarini solishtirishga xizmat qiladi.

## Ishlash natijasi:
```text
Texnika do'konlari uchun parametrlar taqqoslash jadvali paydo bo'ladi.
```

---

# 192-Topshiriq: Jadval ichida progress-bar ko'rsatkichlari
## Topshiriq sharti:
Katak ichiga foizli vizual yuklanish chizig'ini joylashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Progress Table</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; border-bottom: 1px solid #e2e8f0; }
        .progress-bar { background: #e2e8f0; border-radius: 4px; height: 10px; width: 100%; overflow: hidden; }
        .progress-fill { background: #2563eb; height: 100%; }
    </style>
</head>
<body>
    <table>
        <thead><tr><th>Vazifa</th><th>Bajarilish Foizi</th></tr></thead>
        <tbody>
            <tr>
                <td>Dizayn bosqichi</td>
                <td>
                    <div class="progress-bar"><div class="progress-fill" style="width: 100%;"></div></div>
                </td>
            </tr>
            <tr>
                <td>Frontend dasturlash</td>
                <td>
                    <div class="progress-bar"><div class="progress-fill" style="width: 65%;"></div></div>
                </td>
            </tr>
        </tbody>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
Jadval katagi ichiga oddiy matn bilan birga HTML progress chiziqlari o'rnatilib vizual tahlil imkoniyati kengaytiriladi.

## Ishlash natijasi:
```text
Bir qatorda to'liq 100%, ikkinchisida 65% to'ldirilgan ko'k indikator chiziqlari ko'rinadi.
```

---

# 193-Topshiriq: Foydalanuvchilar qonuniy huquqlari matritsa jadvali
## Topshiriq sharti:
Admin, tahrirchi va oddiy foydalanuvchilarning ruxsatlarini (CRUD) aks ettirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Huquqlar Matritsasi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { width: 100%; border-collapse: collapse; text-align: center; }
        th, td { border: 1px solid #cbd5e1; padding: 10px; }
        th:first-child, td:first-child { text-align: left; }
        .yes { color: #16a34a; font-weight: bold; }
        .no { color: #dc2626; font-weight: bold; }
    </style>
</head>
<body>
    <table>
        <tr><th>Amallar</th><th>Admin</th><th>Muharrir</th><th>Mehmon</th></tr>
        <tr><td>Ko'rish</td><td class="yes">&check;</td><td class="yes">&check;</td><td class="yes">&check;</td></tr>
        <tr><td>Yaratish</td><td class="yes">&check;</td><td class="yes">&check;</td><td class="no">&times;</td></tr>
        <tr><td>O'chirish</td><td class="yes">&check;</td><td class="no">&times;</td><td class="no">&times;</td></tr>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
Yashil 'galochka' va qizil 'xoch' belgilari orqali tizim rollarining vakolat chegaralari ko'rsatiladi.

## Ishlash natijasi:
```text
Ruxsatnomalar matritsasi ko'rgazmali tarzda chiqadi.
```

---

# 194-Topshiriq: Serverlar holati va monitoringi jadvali
## Topshiriq sharti:
Server nomi, CPU yuklanishi va jonli holat (Online/Offline) nishonlari.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Server Monitoring</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; border-bottom: 1px solid #e2e8f0; }
        .dot { height: 10px; width: 10px; border-radius: 50%; display: inline-block; margin-right: 6px; }
        .online { background-color: #22c55e; }
        .offline { background-color: #ef4444; }
    </style>
</head>
<body>
    <table>
        <thead><tr><th>Server Nomi</th><th>Yuklanish</th><th>Holat</th></tr></thead>
        <tbody>
            <tr><td>SRV-Tashkent-01</td><td>24%</td><td><span class="dot online"></span>Online</td></tr>
            <tr><td>SRV-Backup-02</td><td>0%</td><td><span class="dot offline"></span>Offline</td></tr>
        </tbody>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
Dumaloq rangli svetofor chiroqchalari yordamida tizim holati tezkor tushuniladi.

## Ishlash natijasi:
```text
Yashil va qizil chiroqchali serverlar monitoringi tablosini ko'rish mumkin.
```

---

# 195-Topshiriq: E-tijorat savatchasi va buyurtmalar jami jadvali
## Topshiriq sharti:
Savatdagi mahsulotlar miqdori, narxi, o'chirish tugmasi va yakuniy hisob-kitob.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Savatcha Jadvali</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; border-bottom: 1px solid #cbd5e1; }
        .remove-btn { color: #ef4444; cursor: pointer; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <table>
        <thead><tr><th>Mahsulot</th><th>Dona</th><th>Narx</th><th>Amal</th></tr></thead>
        <tbody>
            <tr><td>Wireless Sichqoncha</td><td>2</td><td>240 000</td><td><a href="#" class="remove-btn">&times; O'chirish</a></td></tr>
            <tr><td>USB fleshka 64GB</td><td>1</td><td>80 000</td><td><a href="#" class="remove-btn">&times; O'chirish</a></td></tr>
        </tbody>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
Har bir qatorda mahsulot hisobi va o'chirish harakat havolasi joylashadi.

## Ishlash natijasi:
```text
Internet do'kon savatchasi sahifasidagi kabi interaktiv buyurtmalar ro'yxati chiqadi.
```

---

# 196-Topshiriq: Kalendar oylik setkasi jadvali
## Topshiriq sharti:
Jadval orqali bir oylik 7 kunlik taqvim kataklarini shakllantirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Kalendar Jadvali</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        table { width: 350px; border-collapse: collapse; text-align: center; }
        th { background: #3b82f6; color: white; padding: 8px; }
        td { border: 1px solid #e2e8f0; padding: 10px; }
        .today { background: #dbeafe; font-weight: bold; color: #1d4ed8; }
    </style>
</head>
<body>
    <table>
        <thead><tr><th>Du</th><th>Se</th><th>Ch</th><th>Pa</th><th>Ju</th><th>Sh</th><th>Ya</th></tr></thead>
        <tbody>
            <tr><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td></tr>
            <tr><td>8</td><td>9</td><td class="today">10</td><td>11</td><td>12</td><td>13</td><td>14</td></tr>
        </tbody>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
7 ustunli jadval yordamida oylik taqvim tuziladi va bugungi kun alohida fonga olinadi.

## Ishlash natijasi:
```text
Moviy shapkali, 10-kuni belgilangan oylik kalendar doskasi chiqadi.
```

---

# 197-Topshiriq: Saralash indikatorli jadval sarlavhalari (Sortable headers)
## Topshiriq sharti:
Foydalanuvchi bosganda ustun bo'yicha saralash mumkinligini bildiruvchi strelkalar.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Sortable Table</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { width: 100%; border-collapse: collapse; }
        th { background: #f1f5f9; padding: 10px; border: 1px solid #cbd5e1; cursor: pointer; text-align: left; }
        th:hover { background: #e2e8f0; }
        .sort-icon { font-size: 11px; margin-left: 6px; color: #64748b; }
    </style>
</head>
<body>
    <table>
        <thead>
            <tr>
                <th>Ism <span class="sort-icon">&#9650;</span></th>
                <th>Yoshi <span class="sort-icon">&#9660;</span></th>
                <th>Maosh <span class="sort-icon">&#9650;&#9660;</span></th>
            </tr>
        </thead>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
Sarlavha kataklariga kichik uchburchak piktogrammalari qo'shilib o'sish va kamayish tartibida saralash imkoniyati ko'rsatiladi.

## Ishlash natijasi:
```text
Tepaga va pastga qaratilgan saralash strelkalari bilan jihozlangan jadval sarlavhasi chiqadi.
```

---

# 198-Topshiriq: Jadval ichida checkboxlar bilan ko'p qatorli tanlash
## Topshiriq sharti:
Barcha qatorlarni birdaniga yoki alohida tanlash uchun boshqaruv paneli.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Bulk Select Table</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; border-bottom: 1px solid #e2e8f0; }
        th:first-child, td:first-child { width: 30px; text-align: center; }
    </style>
</head>
<body>
    <table>
        <thead>
            <tr><th><input type="checkbox"></th><th>Fayl Nomi</th><th>Hajmi</th></tr>
        </thead>
        <tbody>
            <tr><td><input type="checkbox"></td><td>hujjat.docx</td><td>24 KB</td></tr>
            <tr><td><input type="checkbox"></td><td>rasm.png</td><td>1.2 MB</td></tr>
        </tbody>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
Fayl boshqaruv tizimlari (File Managers) uchun har bir qator oldiga belgilash katakchasi qo'yiladi.

## Ishlash natijasi:
```text
Chap ustunida katakchalari (checkbox) bo'lgan fayllar ro'yxati jadvali ko'rinadi.
```

---

# 199-Topshiriq: Ichki jadvallar (Nested tables - HTML Email marketing)
## Topshiriq sharti:
HTML xabarlar (email shablonlari) uchun ichma-ich jadvalli mustahkam maket.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Email Maketi</title>
    <style>
        body { margin: 0; padding: 0; background-color: #f4f4f4; }
    </style>
</head>
<body>
    <table width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="#f4f4f4">
        <tr>
            <td align="center">
                <table width="600" border="0" cellpadding="20" cellspacing="0" bgcolor="#ffffff" style="margin-top: 20px; font-family: Arial, sans-serif;">
                    <tr>
                        <td align="center" style="background:#2563eb; color:#ffffff;">
                            <h1>Xush Kelibsiz!</h1>
                        </td>
                    </tr>
                    <tr>
                        <td style="color:#333333; line-height: 1.6;">
                            Bizning xizmatlardan foydalanayotganingizdan mamnunmiz.
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
Email xizmatlari (Gmail, Outlook) zamonaviy CSS Grid va Flexboxni qo'llab-quvvatlamasligi sababli barcha elektron xatlar aynan ichma-ich jadvallar (`cellpadding`, `bgcolor`, `width`) asosida yasaladi.

## Ishlash natijasi:
```text
Email maktublariga xos, o'rtada oq qutiga olingan ko'k sarlavhali xabarnoma chiqadi.
```

---

# 200-Topshiriq: Professional korporativ moliya boshqaruv tahlil jadvali
## Topshiriq sharti:
Semantik tuzilma, thead, tbody, tfoot, zebra chiziq, hover effekti va to'liq formatlashni jamlagan mukammal jadval.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boshqaruv Tahlil Jadvali</title>
    <style>
        * { box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 30px; background: #f8fafc; }
        .table-card { background: white; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); overflow: hidden; border: 1px solid #e2e8f0; }
        table { width: 100%; border-collapse: collapse; text-align: left; }
        thead { background: #0f172a; color: white; }
        th { padding: 14px 18px; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }
        td { padding: 14px 18px; border-bottom: 1px solid #f1f5f9; color: #334155; font-size: 14px; }
        tbody tr:hover { background-color: #f8fafc; }
        .status-pill { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; }
        .status-paid { background: #dcfce7; color: #15803d; }
        .status-pending { background: #fef9c3; color: #a16207; }
        .amount { font-family: monospace; font-weight: bold; text-align: right; }
        tfoot { background: #f8fafc; font-weight: bold; }
        tfoot td { border-top: 2px solid #cbd5e1; }
    </style>
</head>
<body>
    <div class="table-card">
        <table>
            <thead>
                <tr>
                    <th>Tranzaksiya ID</th>
                    <th>Mijoz</th>
                    <th>Xizmat</th>
                    <th>Holati</th>
                    <th style="text-align: right;">Summa</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>#TR-9821</td>
                    <td>Olimov Bekzod</td>
                    <td>Web Dasturlash</td>
                    <td><span class="status-pill status-paid">To'langan</span></td>
                    <td class="amount">14 500 000 UZS</td>
                </tr>
                <tr>
                    <td>#TR-9822</td>
                    <td>Karimova Zarina</td>
                    <td>Mobil Ilova</td>
                    <td><span class="status-pill status-pending">Kutilmoqda</span></td>
                    <td class="amount">28 000 000 UZS</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="4">Umumiy Tushum:</td>
                    <td class="amount">42 500 000 UZS</td>
                </tr>
            </tfoot>
        </table>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu to'liq andoza jadvallash san'atining barcha qoidalarini (semantika, kartochka ichida o'rash, to'q thead, holat kapsulalari, monospaced summa va tfoot dagi jamlovchi qator) birlashtirgan mukammal namunadir.

## Ishlash natijasi:
```text
Zamonaviy fintech bank ilovalariga o'xshash, oq kartochkada to'q ko'k shapkali, yashil va sariq to'lov holatlari nishonlari bilan boyitilgan oliy toifali moliyaviy tranzaksiyalar jadvali paydo bo'ladi.
```

---

