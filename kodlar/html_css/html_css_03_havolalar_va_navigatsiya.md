# Havolalar va Navigatsiya (101-150)

# 101-Topshiriq: <a> tegi asosiy sintaksisi va href atributi
## Topshiriq sharti:
Boshqa veb-sahifaga yo'naltiruvchi klassik giperhavolani <a> tegi va href atributi orqali yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Asosiy Havola</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        a { color: #2563eb; font-size: 18px; font-weight: 500; }
    </style>
</head>
<body>
    <p>O'zbekiston Milliy Ensiklopediyasi: <a href="https://ziyouz.uz">ZiyoUz portaliga tashrif buyuring</a>.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<a>` (anchor) tegi vebning asosiy poydevori — gipermatnli aloqani ta'minlaydi. `href` (hypertext reference) atributi manzilni saqlaydi. Usiz teg oddiy bosilmaydigan matnga aylanadi.

## Ishlash natijasi:
```text
Matn ichida moviy rangli tagiga chizilgan chiroyli giperhavola ko'rinadi.
```

---

# 102-Topshiriq: Mutloq (Absolute) va nisbiy (Relative) havolalar
## Topshiriq sharti:
Tashqi to'liq manzil (Absolute) va saytning o'z ichki fayliga yo'naltiruvchi (Relative) havolalarni qo'llang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Havola Turlari</title>
    <style>
        body { font-family: sans-serif; padding: 20px; line-height: 2; }
    </style>
</head>
<body>
    <ul>
        <li>Mutlaq (Absolute) havola: <a href="https://kun.uz/news">Kun.uz Yangiliklari</a></li>
        <li>Nisbiy (Relative) havola: <a href="/about.html">Kompaniyamiz Haqida</a></li>
        <li>Bitta papka yuqoriga: <a href="../index.html">Bosh sahifaga</a></li>
    </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
Mutlaq havola to'liq protokol (https://) va domenni o'z ichiga oladi va boshqa serverdagi sahifalarga o'tadi. Nisbiy havola esa joriy loyiha papkasiga nisbatan yo'lni ifodalaydi va sayt boshqa domenga ko'chganda ham ishlayveradi.

## Ishlash natijasi:
```text
Uch xil yo'l uslubidagi havolalar ro'yxati chiqadi.
```

---

# 103-Topshiriq: target='_blank' bilan yangi oynada ochish
## Topshiriq sharti:
Havola bosilganda foydalanuvchini joriy saytdan chiqarib yubormasdan yangi vkladkada ochilishini ta'minlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Target Blank</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
    </style>
</head>
<body>
    <p>Google qidiruv tizimini yangi oynada ochish: <a href="https://google.com" target="_blank" rel="noopener noreferrer">Google.com</a></p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`target='_blank'` brauzerga ko'rsatilgan sahifani yangi yorliq yoki darchada ochishni buyuradi. Bu foydalanuvchi joriy saytni yo'qotib qo'ymasligi uchun juda qulay.

## Ishlash natijasi:
```text
Bosilganda brauzerda yangi vkladka ochuvchi havola ko'rinadi.
```

---

# 104-Topshiriq: rel='noopener noreferrer' xavfsizlik atributi
## Topshiriq sharti:
target='_blank' ishlatilganda xavfsizlik zaifliklarini (tabnabbing xujumi) bartaraf etish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Xavfsiz Havola</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .secure-link { color: #059669; font-weight: bold; }
    </style>
</head>
<body>
    <a href="https://external-bank-site.uz" target="_blank" rel="noopener noreferrer" class="secure-link">
        Xavfsiz To'lov Tizimi
    </a>
</body>
</html>
```

## Tushuntirish va Mantiq:
`rel='noopener'` yangi ochilgan sahifaga `window.opener` orqali eski sahifani boshqarishga yo'l qo'ymaydi. `noreferrer` esa yangi saytga qaysi sahifadan o'tilganini (Referer header) yashiradi.

## Ishlash natijasi:
```text
Yashil rangli xavfsiz havola ko'rinadi.
```

---

# 105-Topshiriq: target='_self', '_parent', '_top' atributlari
## Topshiriq sharti:
Frame va iframe ichidagi sahifalarni ochish yo'nalishlarini belgilash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Target Qadriyatlari</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
    </style>
</head>
<body>
    <p><a href="page.html" target="_self">_self (Standart o'z oynasida ochish)</a></p>
    <p><a href="page.html" target="_parent">_parent (Ota freym oynasida ochish)</a></p>
    <p><a href="page.html" target="_top">_top (Barcha freymlarni yorib butun darchada ochish)</a></p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`_self` odatiy rejim bo'lib joriy freymda ochadi. `_top` esa barcha iframe qatlamlarini tozalab, butun brauzer darchasini yangi sahifa bilan to'ldiradi.

## Ishlash natijasi:
```text
Uch xil freym boshqaruvi havolalari ro'yxati ko'rinadi.
```

---

# 106-Topshiriq: download atributi bilan fayllarni yuklab olish
## Topshiriq sharti:
Foydalanuvchi havolani bosganda sahifani ochmasdan to'g'ridan-to'g'ri fayl yuklanishini ta'minlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Download Atributi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .download-btn {
            display: inline-block;
            background: #2563eb;
            color: white;
            padding: 10px 18px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 500;
        }
    </style>
</head>
<body>
    <a href="/files/qollanma.pdf" download="HTML5_Qollanma_2026.pdf" class="download-btn">
        Qo'llanmani Yuklab Olish (PDF)
    </a>
</body>
</html>
```

## Tushuntirish va Mantiq:
`download` atributi ko'rsatilgan faylni brauzerda ochish o'rniga foydalanuvchi kompyuteriga yuklab olishni boshlaydi. Agar unga qiymat berilsa, saqlanadigan fayl nomi o'zgartiriladi.

## Ishlash natijasi:
```text
Moviy tugmacha ko'rinishidagi faylni yuklab oluvchi havola ko'rinadi.
```

---

# 107-Topshiriq: mailto: protokoli bilan elektron pochta havolasi
## Topshiriq sharti:
Bosilganda foydalanuvchining pochta dasturini ochuvchi havola.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Mailto Havola</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
    </style>
</head>
<body>
    <p>Savollaringiz bormi? <a href="mailto:support@dasturchi.uz">support@dasturchi.uz</a> manziliga yozing.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`mailto:pochta@domen` protokoli bosilganda kompyuter yoki telefondagi standart pochta mijozi (Outlook, Mail, Gmail) ochilib, manzil avtomatik kiritiladi.

## Ishlash natijasi:
```text
Email havolasi ko'rinadi; bosilganda pochta dasturi ochiladi.
```

---

# 108-Topshiriq: mailto: parametrlarini (subject va body) to'ldirish
## Topshiriq sharti:
Xat mavzusi va dastlabki matnini oldindan kiritilgan holda pochtani ochish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Mailto Murakkab Parametrlar</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .email-link { color: #7c3aed; font-weight: bold; }
    </style>
</head>
<body>
    <a href="mailto:vakansiya@itpark.uz?subject=Frontend%20Dasturchi%20Vakansiyasi&body=Assalomu%20alaykum,%20mening%20rezyumem%20ilova%20qilindi." class="email-link">
        Rezyume yuborish
    </a>
</body>
</html>
```

## Tushuntirish va Mantiq:
URL kodlash (`%20` probel uchun) orqali `?subject=` va `&body=` parametrlarini biriktirib pochta sarlavhasi va mazmunini avtomatik to'ldirish mumkin.

## Ishlash natijasi:
```text
Siyohrang rezyume yuborish havolasi aks etadi.
```

---

# 109-Topshiriq: tel: protokoli bilan telefon qo'ng'irog'i qilish
## Topshiriq sharti:
Smartfonlarda bir bosish bilan qo'ng'iroq qilish imkonini beruvchi havola.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Tel Protokoli</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .call-btn { background: #16a34a; color: white; padding: 8px 16px; border-radius: 4px; text-decoration: none; display: inline-block; }
    </style>
</head>
<body>
    <p>Aloqa markazi: <a href="tel:+998711234567" class="call-btn">+998 71 123-45-67</a></p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`tel:+998...` protokoli telefon raqamlarini xalqaro formatda kiritish uchun xizmat qiladi. Mobil qurilmalarda unga bosilganda to'g'ridan-to'g'ri terish oynasi ochiladi.

## Ishlash natijasi:
```text
Yashil tugma ichida terish mumkin bo'lgan telefon raqami ko'rinadi.
```

---

# 110-Topshiriq: sms: protokoli bilan SMS yozish
## Topshiriq sharti:
Mobil foydalanuvchilar uchun SMS ilovasini ochib beruvchi havola.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>SMS Protokoli</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
    </style>
</head>
<body>
    <a href="sms:+998901234567?body=Salom,%20buyurtma%20holatini%20bilmoqchiman">SMS orqali buyurtma berish</a>
</body>
</html>
```

## Tushuntirish va Mantiq:
`sms:+998...?body=...` protokoli mobil operatsion tizimlariga xabarlar ilovasini ko'rsatilgan qisqa matn bilan ochishga imkon beradi.

## Ishlash natijasi:
```text
SMS yuborish havolasi chiqadi.
```

---

# 111-Topshiriq: Sahifa ichidagi xatcho'p (bookmark) langar linklari (#id)
## Topshiriq sharti:
Bitta uzun sahifaning pastki yoki yuqori bo'limlariga darhol sakrash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Bookmark Linklar</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .space { height: 600px; background: #f8fafc; margin: 20px 0; padding: 20px; }
    </style>
</head>
<body>
    <a href="#pastki-bolim">Pastki bo'limga sakrash &darr;</a>
    <div class="space">Sahifa tarkibi... (uzun matn)</div>
    <div id="pastki-bolim" style="background:#e0f2fe; padding:20px;">
        <h3>Pastki Bo'limga Xush Kelibsiz!</h3>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Havola `href='#id'` qiymatiga ega bo'lganda va sahifadagi biror elementda xuddi shu `id='...'` bo'lsa, brauzer darhol ekranni o'sha element turgan joyga suradi.

## Ishlash natijasi:
```text
Boshidagi havolaga bosilganda sahifa darhol pastdagi ko'k rangli blokga sakrab tushadi.
```

---

# 112-Topshiriq: 'Yuqoriga qaytish' (Back to top) langar havolasi
## Topshiriq sharti:
Sahifaning eng yuqori boshlanish nuqtasiga qaytuvchi qulay havola.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Yuqoriga Qaytish</title>
    <style>
        body { font-family: sans-serif; margin: 0; padding: 20px; }
        .tall { height: 1200px; background: linear-gradient(white, #cbd5e1); }
        .back-top { position: fixed; bottom: 20px; right: 20px; background: #0f172a; color: white; padding: 10px 15px; border-radius: 50px; text-decoration: none; font-size: 14px; }
    </style>
</head>
<body>
    <div id="top"></div>
    <h1>Sahifa Boshi</h1>
    <div class="tall">Pastga aylantiring...</div>
    <a href="#top" class="back-top">&uarr; Yuqoriga</a>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<a href='#top'>` yoki bo'sh `href='#'` sahifaning boshlanish nuqtasini ifodalaydi. `position: fixed` orqali u doimo ekranning pastki burchagida qulay turadi.

## Ishlash natijasi:
```text
O'ng pastki burchakda mahkamlangan yumaloq qora tugmacha; bosilganda sahifa tepasiga olib chiqadi.
```

---

# 113-Topshiriq: <a> va <button> o'rtasidagi semantik farq
## Topshiriq sharti:
Qachon havola, qachon tugma ishlatish kerakligini to'g'ri taqsimlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Link vs Button</title>
    <style>
        body { font-family: sans-serif; padding: 25px; display: flex; gap: 20px; align-items: center; }
        .ui-btn { background: #3b82f6; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; }
        .ui-link { color: #3b82f6; text-decoration: underline; }
    </style>
</head>
<body>
    <!-- Havola: boshqa sahifaga o'tish uchun -->
    <a href="/login" class="ui-link">Kirish sahifasiga o'tish</a>

    <!-- Tugma: harakat bajarish, modal ochish, ma'lumot yuborish uchun -->
    <button type="button" class="ui-btn" onclick="alert('Saqlandi!')">Ma'lumotni Saqlash</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
Oltin qoida: Agar foydalanuvchi yangi sahifaga yoki boshqa URL manzilga o'tsa — `<a>` ishlatiladi. Agar sahifaning o'zida harakat sodir bo'lsa (forma yuborish, modal ochish, o'chirish) — `<button>` ishlatilishi shart.

## Ishlash natijasi:
```text
Chapda havola matni, o'ngda esa bosilganda harakat bajaruvchi ko'k tugma ko'rinadi.
```

---

# 114-Topshiriq: Havolaning 5 ta holati (States): link, visited, hover, active, focus
## Topshiriq sharti:
Foydalanuvchi bilan o'zaro ta'sirda bo'lgan barcha CSS psevdo-sinflarini to'liq stillash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Havola Holatlari</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        .state-link:link { color: #2563eb; }
        .state-link:visited { color: #7c3aed; }
        .state-link:hover { color: #dc2626; text-decoration: underline; }
        .state-link:active { color: #ea580c; }
        .state-link:focus { outline: 2px dashed #059669; outline-offset: 4px; }
    </style>
</head>
<body>
    <a href="#test" class="state-link">Interaktiv Havola Holatlari</a>
</body>
</html>
```

## Tushuntirish va Mantiq:
Havola tartibi (LVHA qoidasi): :link (ochilmagan), :visited (avval kirilgan), :hover (sichqoncha borganda), :active (bosib turilganda) va :focus (klaviaturadan Tab bosilganda).

## Ishlash natijasi:
```text
Kursor kelganda qizil rangga aylanuvchi, bosilganda to'q sariq bo'luvchi interaktiv havola namoyon bo'ladi.
```

---

# 115-Topshiriq: Matnsiz havolalar va aria-label
## Topshiriq sharti:
Faqatgina piktogrammadan iborat havolalarni ekranni o'qish vositalari uchun ochiqlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Aria Label Havola</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .icon-link { display: inline-flex; width: 36px; height: 36px; background: #f1f5f9; border-radius: 50%; align-items: center; justify-content: center; text-decoration: none; }
    </style>
</head>
<body>
    <a href="https://twitter.com" class="icon-link" aria-label="Kompaniyamizning Twitter sahifasiga o'tish">
        &#128038;
    </a>
</body>
</html>
```

## Tushuntirish va Mantiq:
Agar havola ichida faqat rasm, ikonka yoki emoji bo'lsa, ko'zi ojiz insonlar uning qayerga olib borishini bila olmaydi. `aria-label='...'` unga to'liq eshitiladigan ma'no beradi.

## Ishlash natijasi:
```text
Kulrang aylanada qushcha emojisi ko'rinadi; ovozli o'quvchi esa uning Twitter havolasi ekanini aytadi.
```

---

# 116-Topshiriq: text-decoration boshqaruvi va hover effekti
## Topshiriq sharti:
Tagchiziqni toza olib tashlash va kursor borganda nafis chiqarish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Text Decoration</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .clean-link {
            color: #0f172a;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.2s, text-decoration 0.2s;
        }
        .clean-link:hover {
            color: #2563eb;
            text-decoration: underline;
            text-underline-offset: 5px;
        }
    </style>
</head>
<body>
    <a href="#" class="clean-link">Zamonaviy va Toza Havola</a>
</body>
</html>
```

## Tushuntirish va Mantiq:
`text-decoration: none` standart xunuk chiziqni yo'qotadi. `text-underline-offset: 5px` esa chiziqni harflarga yopishib qolmasdan biroz pastroqda joylashishini ta'minlaydi.

## Ishlash natijasi:
```text
Boshida qora va chiziqsiz havola; kursor borganda ko'k rangga o'tib, matndan 5px pastda chiziq tortiladi.
```

---

# 117-Topshiriq: Gorizontal navigatsiya menyusi
## Topshiriq sharti:
Nav, ul, li va a teglari yordamida to'liq veb menyu yaratish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Gorizontal Menyu</title>
    <style>
        body { font-family: sans-serif; margin: 0; background: #f8fafc; }
        nav { background: #1e293b; padding: 0 20px; }
        ul { list-style: none; margin: 0; padding: 0; display: flex; }
        li a { display: block; color: #f1f5f9; text-decoration: none; padding: 16px 20px; }
        li a:hover { background: #334155; color: #38bdf8; }
    </style>
</head>
<body>
    <nav>
        <ul>
            <li><a href="#home">Asosiy</a></li>
            <li><a href="#services">Xizmatlar</a></li>
            <li><a href="#portfolio">Loyihalar</a></li>
            <li><a href="#contact">Bog'lanish</a></li>
        </ul>
    </nav>
</body>
</html>
```

## Tushuntirish va Mantiq:
Semantik ro'yxat `<ul>` va `display: flex` orqali gorizontal qatorga teriladi. `li a` ga `display: block` va padding berilishi bosish maydonini sezilarli kattalashtiradi.

## Ishlash natijasi:
```text
To'q fonga ega toza gorizontal navigatsiya menyusi paydo bo'ladi.
```

---

# 118-Topshiriq: Vertikal yon menyu (Sidebar Navigation)
## Topshiriq sharti:
Boshqaruv panellari (Dashboard) uchun vertikal navigatsiya menyusi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Vertikal Menyu</title>
    <style>
        body { font-family: sans-serif; margin: 0; display: flex; height: 100vh; }
        .sidebar { width: 240px; background: #0f172a; color: white; padding-top: 20px; }
        .nav-vertical { list-style: none; padding: 0; margin: 0; }
        .nav-vertical a { display: block; padding: 12px 24px; color: #94a3b8; text-decoration: none; border-left: 4px solid transparent; }
        .nav-vertical a:hover, .nav-vertical a.active { color: white; background: #1e293b; border-left-color: #38bdf8; }
    </style>
</head>
<body>
    <nav class="sidebar">
        <ul class="nav-vertical">
            <li><a href="#" class="active">Boshqaruv</a></li>
            <li><a href="#">Foydalanuvchilar</a></li>
            <li><a href="#">Moliya</a></li>
            <li><a href="#">Sozlamalar</a></li>
        </ul>
    </nav>
</body>
</html>
```

## Tushuntirish va Mantiq:
Yon panel menyularida havolaning butun kengligi bo'ylab bosilishi (`display: block`) va chap chetida rangli hoshiya (border-left) o'zgarishi qulay foydalanuvchi tajribasini (UX) beradi.

## Ishlash natijasi:
```text
Chap tomonda qora rangli baland panel va chap tomonida moviy chizig'i bilan ajralib turuvchi faol band ko'rinadi.
```

---

# 119-Topshiriq: Quyi podval havolalari klasteri (Footer links)
## Topshiriq sharti:
Katta portallar uchun ko'p ustunli podval havolalari strukturasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Podval Havolalari</title>
    <style>
        body { font-family: sans-serif; margin: 0; }
        footer { background: #111827; color: white; padding: 40px 20px; }
        .footer-grid { display: grid; grid-template-columns: repeat(3, 1fr); max-width: 800px; margin: 0 auto; gap: 30px; }
        .col h4 { margin-top: 0; color: #9ca3af; font-size: 14px; text-transform: uppercase; }
        .col ul { list-style: none; padding: 0; margin: 0; }
        .col li { margin-bottom: 8px; }
        .col a { color: #d1d5db; text-decoration: none; font-size: 14px; }
        .col a:hover { color: white; }
    </style>
</head>
<body>
    <footer>
        <div class="footer-grid">
            <div class="col">
                <h4>Mahsulot</h4>
                <ul><li><a href="#">Xususiyatlar</a></li><li><a href="#">Xavfsizlik</a></li></ul>
            </div>
            <div class="col">
                <h4>Resurslar</h4>
                <ul><li><a href="#">Hujjatlar</a></li><li><a href="#">Darsliklar</a></li></ul>
            </div>
            <div class="col">
                <h4>Kompaniya</h4>
                <ul><li><a href="#">Haqimizda</a></li><li><a href="#">Karyera</a></li></ul>
            </div>
        </div>
    </footer>
</body>
</html>
```

## Tushuntirish va Mantiq:
Uch ustunli toza semantik klaster foydalanuvchiga saytning barcha muhim burchaklariga oson kirish imkonini taqdim etadi.

## Ishlash natijasi:
```text
To'q qora fonda uchta tartibli ustunda oq-kulrang podval havolalari joylashadi.
```

---

# 120-Topshiriq: Non ushog'i (Breadcrumb) navigatsiyasi
## Topshiriq sharti:
Foydalanuvchi saytning qaysi chuqurlikdagi sahifasida turganini ko'rsatuvchi zanjir.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Breadcrumb</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .breadcrumb { list-style: none; padding: 0; margin: 0; display: flex; font-size: 14px; }
        .breadcrumb li + li::before { content: "/"; padding: 0 10px; color: #94a3b8; }
        .breadcrumb a { color: #2563eb; text-decoration: none; }
        .breadcrumb a:hover { text-decoration: underline; }
        .breadcrumb [aria-current="page"] { color: #64748b; font-weight: bold; }
    </style>
</head>
<body>
    <nav aria-label="Breadcrumb">
        <ol class="breadcrumb">
            <li><a href="/">Bosh sahifa</a></li>
            <li><a href="/texnika">Texnika</a></li>
            <li><a href="/smartfonlar">Smartfonlar</a></li>
            <li aria-current="page">Galaxy S24</li>
        </ol>
    </nav>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<ol>` (tartibli ro'yxat) orqali yasaladi va `li + li::before` bilan oraliqqa qiya chiziq (`/`) qo'yiladi. So'nggi band `aria-current='page'` bilan joriy sahifa ekanligi belgilanadi.

## Ishlash natijasi:
```text
'Bosh sahifa / Texnika / Smartfonlar / Galaxy S24' ko'rinishidagi zamonaviy navigatsiya zanjiri hosil bo'ladi.
```

---

# 121-Topshiriq: Sahifalash (Pagination) navigatsiya paneli
## Topshiriq sharti:
Ko'p sahifali ro'yxatlar bo'ylab o'tish uchun raqamlangan sahifalash vidjeti.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Pagination</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        .pagination { display: flex; list-style: none; padding: 0; gap: 6px; }
        .pagination a { display: block; padding: 8px 14px; border: 1px solid #cbd5e1; border-radius: 6px; text-decoration: none; color: #1e293b; font-weight: 500; }
        .pagination a:hover { background: #f1f5f9; }
        .pagination .active a { background: #2563eb; color: white; border-color: #2563eb; }
    </style>
</head>
<body>
    <nav aria-label="Sahifalar">
        <ul class="pagination">
            <li><a href="#">&laquo; Oldingi</a></li>
            <li><a href="#">1</a></li>
            <li class="active"><a href="#" aria-current="page">2</a></li>
            <li><a href="#">3</a></li>
            <li><a href="#">Keyingi &raquo;</a></li>
        </ul>
    </nav>
</body>
</html>
```

## Tushuntirish va Mantiq:
Pagination blokida joriy raqam ko'k fonda ajratiladi, oldingi va keyingi tugmalari bilan foydalanuvchi ma'lumotlar sahifalari orasida sayohat qiladi.

## Ishlash natijasi:
```text
Kvadrat burchaklari yumaloq raqamli tugmachalar qatori chiqadi, 2-raqam ko'k rangda faol turadi.
```

---

# 122-Topshiriq: Faol (Current) sahifa havolasini ajratish
## Topshiriq sharti:
Foydalanuvchi aynan qaysi bo'limda turganini ko'rsatuvchi stillash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Active Link</title>
    <style>
        nav ul { display: flex; gap: 20px; list-style: none; font-family: sans-serif; }
        nav a { text-decoration: none; color: #4b5563; padding-bottom: 4px; }
        nav a.active { color: #2563eb; font-weight: bold; border-bottom: 2px solid #2563eb; }
    </style>
</head>
<body>
    <nav>
        <ul>
            <li><a href="/">Asosiy</a></li>
            <li><a href="/xizmatlar" class="active">Xizmatlar</a></li>
            <li><a href="/kontakt">Kontakt</a></li>
        </ul>
    </nav>
</body>
</html>
```

## Tushuntirish va Mantiq:
Joriy sahifa havolasiga maxsus `.active` klassi biriktirilib, qalin shrift va pastki chiziq beriladi.

## Ishlash natijasi:
```text
'Xizmatlar' so'zi ostida ko'k chiziq bilan faol holatda aks etadi.
```

---

# 123-Topshiriq: aria-current='page' atributining vazifasi
## Topshiriq sharti:
Faol sahifani faqat ko'rinishda emas, ovozli o'quvchi qurilmalar uchun ham bildirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Aria Current</title>
    <style>
        nav a[aria-current="page"] { background: #dbeafe; color: #1d4ed8; padding: 4px 8px; border-radius: 4px; }
    </style>
</head>
<body>
    <nav>
        <a href="/">Asosiy</a> |
        <a href="/kurslar" aria-current="page">Kurslar</a> |
        <a href="/forum">Forum</a>
    </nav>
</body>
</html>
```

## Tushuntirish va Mantiq:
`aria-current='page'` ekranni o'quvchi dasturga 'Siz aynan ushbu sahifadasiz' degan axborotni taqdim etadi. CSS da uni `a[aria-current='page']` selektori orqali klassiz ham stillash mumkin.

## Ishlash natijasi:
```text
'Kurslar' havolasi och ko'k fonda ajraladi.
```

---

# 124-Topshiriq: 'Asosiy kontentga sakrash' (Skip to content) havolasi
## Topshiriq sharti:
Klaviaturadan foydalanuvchilar har safar uzun menyuni aylanib o'tirmasligi uchun yashirin qulay havola.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Skip to Content</title>
    <style>
        .skip-link {
            position: absolute;
            top: -40px;
            left: 10px;
            background: #000;
            color: #fff;
            padding: 8px 12px;
            z-index: 100;
            transition: top 0.2s;
        }
        .skip-link:focus {
            top: 10px;
        }
    </style>
</head>
<body>
    <a href="#main-content" class="skip-link">Asosiy kontentga o'tish</a>
    <nav>Menyu elementlari...</nav>
    <main id="main-content" style="margin-top: 50px;">
        <h1>Asosiy Maqola</h1>
    </main>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu havola odatda ekrandan tashqarida (`top: -40px`) yashirin turadi. Lekin sahifa ochilib `Tab` tugmasi bosilganda ekranda paydo bo'ladi va barcha menyuni o'tkazib asosiy maqolaga olib boradi.

## Ishlash natijasi:
```text
Faqat Tab bosilganda tepadan tushib keladigan xavfsiz qulaylik havolasi.
```

---

# 125-Topshiriq: Havolani CTA (Call-to-Action) tugmasi sifatida stillash
## Topshiriq sharti:
Foydalanuvchini ro'yxatdan o'tishga undovchi yorqin havola.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>CTA Button</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        .cta-btn {
            display: inline-block;
            background: #2563eb;
            color: white;
            padding: 14px 28px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            text-decoration: none;
            box-shadow: 0 4px 6px rgba(37,99,235,0.25);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .cta-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(37,99,235,0.35);
        }
    </style>
</head>
<body>
    <a href="/register" class="cta-btn">Hoziroq Boshlang &rarr;</a>
</body>
</html>
```

## Tushuntirish va Mantiq:
Tugma ko'rinishidagi havola har doim `display: inline-block` bo'lishi kerak, shundagina padding, margin va transformatsiyalar unga to'liq ta'sir qiladi.

## Ishlash natijasi:
```text
Bosganda biroz yuqoriga ko'tariluvchi va soya beruvchi jozibali ko'k havola tugmasi chiqadi.
```

---

# 126-Topshiriq: Gradient fonli interaktiv havola
## Topshiriq sharti:
Ko'zga tashlanuvchi rangli gradientli jilolangan havola tugmasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Gradient Link</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        .grad-btn {
            display: inline-block;
            background: linear-gradient(135deg, #6366f1, #a855f7);
            color: white;
            padding: 12px 24px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <a href="#" class="grad-btn">Premium Obuna</a>
</body>
</html>
```

## Tushuntirish va Mantiq:
Binafsharangdan to'q pushtiga o'tuvchi gradient fon zamonaviy startaplar va mahsulot sahifalarida qo'llaniladi.

## Ishlash natijasi:
```text
Yumaloq oval shaklidagi binafsha gradientli nafis tugmacha paydo bo'ladi.
```

---

# 127-Topshiriq: Havola ichiga rasm joylashtirish (Rasmli havola)
## Topshiriq sharti:
Bosilganda bosh sahifaga olib boruvchi logotip yoki banner rasmini yasash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Rasmli Havola</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .logo-link img { display: block; border-radius: 8px; }
    </style>
</head>
<body>
    <a href="/" class="logo-link">
        <svg width="150" height="50" viewBox="0 0 150 50">
            <rect width="150" height="50" fill="#0f172a" rx="6"/>
            <text x="50%" y="55%" fill="#38bdf8" dominant-baseline="middle" text-anchor="middle" font-weight="bold">LOGOTIP</text>
        </svg>
    </a>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<a>` tegi ichiga `<img>` yoki `<svg>` kiritish orqali butun tasvir bosiluvchi faol obyektga aylanadi.

## Ishlash natijasi:
```text
Qora fonda moviy 'LOGOTIP' yozuvli rasm ko'rinadi; uning ustiga bosish mumkin.
```

---

# 128-Topshiriq: Havola ichiga SVG ikonka va matn joylashtirish
## Topshiriq sharti:
Matn yonida ikonka bo'lgan havola yaratish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>SVG Havola</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .icon-link { display: inline-flex; align-items: center; gap: 8px; color: #0284c7; text-decoration: none; font-weight: 500; }
        .icon-link:hover { color: #0369a1; }
    </style>
</head>
<body>
    <a href="#" class="icon-link">
        <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zm0 9l-10-5v6l10 5 10-5v-6l-10 5z"/></svg>
        <span>Akademiya Darslari</span>
    </a>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: inline-flex` va `align-items: center` vositasida SVG ikonka va yonidagi matn bitta qatorda vertikal mukammal markazlashadi.

## Ishlash natijasi:
```text
Kichik shlyapa ikonchasi va yonida moviy 'Akademiya Darslari' matnli chiroyli havola chiqadi.
```

---

# 129-Topshiriq: Kursor kelganda tagchiziq animatsiyasi (Underline animation)
## Topshiriq sharti:
Chapdan o'ngga qarab yuguruvchi chiroyli CSS chiziq animatsiyasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Chiziq Animatsiyasi</title>
    <style>
        body { font-family: sans-serif; padding: 40px; }
        .animated-link {
            position: relative;
            color: #0f172a;
            text-decoration: none;
            font-size: 20px;
            font-weight: 600;
        }
        .animated-link::after {
            content: '';
            position: absolute;
            width: 100%;
            height: 2px;
            bottom: -4px;
            left: 0;
            background-color: #3b82f6;
            transform: scaleX(0);
            transform-origin: bottom right;
            transition: transform 0.3s ease-out;
        }
        .animated-link:hover::after {
            transform: scaleX(1);
            transform-origin: bottom left;
        }
    </style>
</head>
<body>
    <a href="#" class="animated-link">Bizning Tariximiz</a>
</body>
</html>
```

## Tushuntirish va Mantiq:
`::after` va `transform: scaleX(0)` boshlang'ich yashirin holatni beradi, hover bo'lganda `scaleX(1)` ga silliq o'tib estetik chiziq oqib keladi.

## Ishlash natijasi:
```text
Sichqoncha borganda matn tagidan chapdan o'ngga ko'k chiziq silliq yugurib o'tadi.
```

---

# 130-Topshiriq: Ochilib tushuvchi menyu (Dropdown navigation)
## Topshiriq sharti:
Faqat HTML va CSS orqali sichqoncha kelganda ostidan menyu ochilishi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Dropdown Menyu</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .dropdown { position: relative; display: inline-block; }
        .drop-btn { background: #1e293b; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; display: block; }
        .drop-menu { display: none; position: absolute; top: 100%; left: 0; background: white; min-width: 160px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 4px; padding: 0; list-style: none; }
        .drop-menu a { color: #333; padding: 10px 15px; display: block; text-decoration: none; }
        .drop-menu a:hover { background: #f1f5f9; color: #2563eb; }
        .dropdown:hover .drop-menu { display: block; }
    </style>
</head>
<body>
    <div class="dropdown">
        <a href="#" class="drop-btn">Xizmatlar &darr;</a>
        <ul class="drop-menu">
            <li><a href="#">Web Saytlar</a></li>
            <li><a href="#">Mobil Ilovalar</a></li>
            <li><a href="#">UI/UX Dizayn</a></li>
        </ul>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ota element `.dropdown` ga `position: relative`, menyuga `position: absolute` beriladi va hover bo'lganda `display: none` dan `display: block` ga o'zgartiriladi.

## Ishlash natijasi:
```text
'Xizmatlar' ustiga sichqoncha borganda pastga qarab oq qutida 3 ta xizmat ro'yxati ochiladi.
```

---

# 131-Topshiriq: Ikki pog'onali ochiluvchi menyu (Multi-level dropdown)
## Topshiriq sharti:
Menyu ichidagi menyu yon tomonga ochilishi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Ko'p Pog'onali Menyu</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        ul { list-style: none; margin: 0; padding: 0; }
        .menu > li { position: relative; display: inline-block; }
        .menu a { display: block; padding: 10px 15px; background: #0f172a; color: white; text-decoration: none; }
        .sub-menu { display: none; position: absolute; top: 100%; left: 0; width: 180px; }
        .sub-item { position: relative; }
        .sub-sub-menu { display: none; position: absolute; top: 0; left: 100%; width: 180px; }
        li:hover > ul { display: block; }
    </style>
</head>
<body>
    <ul class="menu">
        <li>
            <a href="#">Mahsulotlar &darr;</a>
            <ul class="sub-menu">
                <li class="sub-item">
                    <a href="#">Elektronika &rarr;</a>
                    <ul class="sub-sub-menu">
                        <li><a href="#">Noutbuklar</a></li>
                        <li><a href="#">Telefonlar</a></li>
                    </ul>
                </li>
            </ul>
        </li>
    </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
`li:hover > ul` selektori bevosita bola ro'yxatni ochadi. Uchinchi pog'ona `left: 100%` orqali ikkinchisining o'ng tomoniga chiroyli suriladi.

## Ishlash natijasi:
```text
Kursor borganda avval pastga, so'ngra uning ichidan o'ng tomonga qarab yangi menyu zanjiri ochiladi.
```

---

# 132-Topshiriq: Mobil gamburger menyu belgisi (Faqat CSS)
## Topshiriq sharti:
Uchta chiziqdan iborat zamonaviy gamburger tugmasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Gamburger Belgisi</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        .hamburger {
            width: 30px;
            height: 22px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            cursor: pointer;
        }
        .bar {
            width: 100%;
            height: 4px;
            background-color: #0f172a;
            border-radius: 2px;
        }
    </style>
</head>
<body>
    <div class="hamburger">
        <span class="bar"></span>
        <span class="bar"></span>
        <span class="bar"></span>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Flexbox va uchta `<span>` yordamida har qanday piktogramma faylisiz toza CSS gamburger belgisi hosil qilinadi.

## Ishlash natijasi:
```text
Mobil ilovalardagi kabi parallel 3 ta chiziqli toza menyu belgisi chiqadi.
```

---

# 133-Topshiriq: Yorliqlar (Tabs) navigatsiyasi langar orqali
## Topshiriq sharti:
Bitta sahifada bo'limlararo almashinuvchi yorliqlar paneli.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Tabs Navigatsiyasi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .tabs { display: flex; border-bottom: 2px solid #e2e8f0; }
        .tab-link { padding: 10px 20px; text-decoration: none; color: #64748b; font-weight: 500; border-bottom: 2px solid transparent; margin-bottom: -2px; }
        .tab-link.active { color: #3b82f6; border-bottom-color: #3b82f6; }
    </style>
</head>
<body>
    <div class="tabs">
        <a href="#umumiy" class="tab-link active">Umumiy ma'lumot</a>
        <a href="#sharhlar" class="tab-link">Sharhlar (14)</a>
        <a href="#yetkazish" class="tab-link">Yetkazib berish</a>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`margin-bottom: -2px` va chegara chiziqlari birikishi orqali zamonaviy brauzer oynalariga o'xshash yorliqlar dizayni hosil qilinadi.

## Ishlash natijasi:
```text
Bitta chiziq ustida joylashgan yorliqlar; birinchisi ko'k chiziq bilan tanlangan holatda turadi.
```

---

# 134-Topshiriq: Tashqi havolani bildiruvchi avtomatik ikonka
## Topshiriq sharti:
CSS selektori orqali 'http' bilan boshlanuvchi saytlarga avtomatik tashqi havola belgisini chiqarish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>External Link Ikonkasi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        a[href^="http"]::after {
            content: " 97"; /* Shimoliy-sharqiy o'q belgisi */
            font-size: 14px;
            color: #64748b;
        }
    </style>
</head>
<body>
    <p>Ichki havola: <a href="/kontakt">Biz bilan bog'lanish</a></p>
    <p>Tashqi havola: <a href="https://t.me">Telegram Kanali</a></p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`a[href^='http']` atribut selektori `http` bilan boshlanuvchi barcha havolalarni avtomatik taniydi va `::after` orqali ularning orqasiga tashqi havola strelkasini qo'yadi.

## Ishlash natijasi:
```text
Telegram so'zi yonida avtomatik ravishda tashqariga yo'naltirilgan strelka paydo bo'ladi.
```

---

# 135-Topshiriq: Fayl turini ko'rsatuvchi havola nishoni
## Topshiriq sharti:
CSS orqali .pdf bilan tugaydigan fayllarga maxsus qizil nishon biriktirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>PDF Havola</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        a[href$=".pdf"]::after {
            content: " [PDF]";
            color: #dc2626;
            font-weight: bold;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <a href="/docs/shartnoma.pdf">Foydalanish shartnomasi</a>
</body>
</html>
```

## Tushuntirish va Mantiq:
`a[href$='.pdf']` selektori manzil oxiri `.pdf` bilan tugashini tekshiradi va matn ketidan qizil [PDF] belgisini joylashtiradi.

## Ishlash natijasi:
```text
Havola oxirida qizil qalin '[PDF]' yozuvi ko'rinadi.
```

---

# 136-Topshiriq: Ovozli o'qish uchun havola kontekstini to'g'ri nomlash
## Topshiriq sharti:
'Bu yerni bosing' xatosidan qochib, to'liq ma'noli havolalar tuzish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>A11y Havola Nomlanishi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; line-height: 1.6; }
        .bad { color: #dc2626; }
        .good { color: #16a34a; }
    </style>
</head>
<body>
    <p class="bad">Xato: Kurs jadvalini ko'rish uchun <a href="/jadval">bu yerni bosing</a>.</p>
    <p class="good">To'g'ri: Marhamat, <a href="/jadval">2026-yilgi kurslar jadvali</a> bilan tanishing.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ekran o'quvchi dasturlar havolalar ro'yxatini alohida chiqarib bera oladi. Agar hammasi 'bu yerni bosing' bo'lsa, inson qayerga borishini tushunmaydi. Havola matni manzil mohiyatini ifodalashi shart.

## Ishlash natijasi:
```text
Yashil to'g'ri variantda havola to'liq ma'noga ega bo'lgan jumla sifatida ko'rsatiladi.
```

---

# 137-Topshiriq: Ijtimoiy tarmoqlar havolalari bloki
## Topshiriq sharti:
Telegram, YouTube, GitHub kabi tarmoqlarga olib boruvchi chiroyli doiralar.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Ijtimoiy Tarmoqlar</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        .socials { display: flex; gap: 12px; }
        .social-btn {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: #f1f5f9;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            color: #0f172a;
            font-weight: bold;
            transition: all 0.2s;
        }
        .social-btn:hover { background: #0284c7; color: white; transform: translateY(-3px); }
    </style>
</head>
<body>
    <div class="socials">
        <a href="#" class="social-btn" aria-label="Telegram">TG</a>
        <a href="#" class="social-btn" aria-label="YouTube">YT</a>
        <a href="#" class="social-btn" aria-label="GitHub">GH</a>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Doira shaklidagi ijtimoiy tarmoq piktogrammalari hover bo'lganda yuqoriga sakraydi va rangini o'zgartiradi.

## Ishlash natijasi:
```text
Yonma-yon turgan uchta chiroyli kulrang aylanalar; sichqoncha borganda ko'karib ko'tariladi.
```

---

# 138-Topshiriq: Telegram yoki WhatsApp chatiga to'g'ridan-to'g'ri havola
## Topshiriq sharti:
Mijoz bilan tezkor chat boshlash havolasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Telegram Havola</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .tg-btn {
            display: inline-block;
            background: #229ed9;
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            text-decoration: none;
            font-weight: 500;
        }
    </style>
</head>
<body>
    <a href="https://t.me/menejer_aloqa" target="_blank" rel="noopener noreferrer" class="tg-btn">
        Telegram orqali bog'lanish
    </a>
</body>
</html>
```

## Tushuntirish va Mantiq:
`https://t.me/username` manzili foydalanuvchini to'g'ridan-to'g'ri ko'rsatilgan akkaunt bilan Telegramda suhbatlashishga yo'naltiradi.

## Ishlash natijasi:
```text
Telegramning rasmiy havorang tusidagi oval tugmacha paydo bo'ladi.
```

---

# 139-Topshiriq: Kalendar hodisasini yuklab olish havolasi
## Topshiriq sharti:
iCalendar (.ics) faylini yaratib taqvimga hodisa biriktirish havolasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Kalendar Havolasi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .cal-link { color: #d97706; font-weight: 600; text-decoration: none; }
    </style>
</head>
<body>
    <p>Vebinarga yozildingiz: <a href="/event.ics" download="vebinar.ics" class="cal-link">&#128197; Taqvimga qo'shish</a></p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Foydalanuvchi taqvimiga hodisa qo'shishi uchun `.ics` faylga havola beriladi va `download` bilan yuklatiladi.

## Ishlash natijasi:
```text
Kalendar emojisi bilan bezatilgan to'q sariq havola ko'rinadi.
```

---

# 140-Topshiriq: Geolokatsiya xaritasiga yo'naltiruvchi havola
## Topshiriq sharti:
Google Maps yoki Yandex Xaritalarda aniq manzilni ochish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Geo Havola</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .map-link { color: #dc2626; font-weight: bold; }
    </style>
</head>
<body>
    <p>Ofisimiz: <a href="https://maps.google.com/?q=41.311081,69.240562" target="_blank" rel="noopener noreferrer" class="map-link">&#128205; Xaritada ko'rish (Toshkent)</a></p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Kenglik va uzunlik (latitude/longitude) koordinatalari bilan xaritaga to'g'ridan-to'g'ri yo'naltiriladi.

## Ishlash natijasi:
```text
Lokatsiya belgisi bilan qizil rangli xarita havolasi aks etadi.
```

---

# 141-Topshiriq: Sticky (Yopishqoq) navigatsiya paneli
## Topshiriq sharti:
Sahifa pastga aylantirilganda ham ekranning yuqori qismida yopishib qoluvchi menyu.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Sticky Nav</title>
    <style>
        body { font-family: sans-serif; margin: 0; }
        header { background: #3b82f6; color: white; padding: 30px 20px; text-align: center; }
        nav {
            position: sticky;
            top: 0;
            background: #1e293b;
            padding: 12px 20px;
            color: white;
            z-index: 1000;
        }
        nav a { color: white; text-decoration: none; margin-right: 15px; }
        .content { height: 1500px; padding: 20px; background: #f8fafc; }
    </style>
</head>
<body>
    <header>Banner Qismi</header>
    <nav>
        <a href="#1">Bo'lim 1</a>
        <a href="#2">Bo'lim 2</a>
    </nav>
    <div class="content">Sahifani pastga aylantirib yopishqoq menyuni ko'ring...</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`position: sticky` va `top: 0` berilgan element o'z ota blokining chegarasi doirasida belgilangan nuqtaga yetganda ekranda mahkamlanib qoladi.

## Ishlash natijasi:
```text
Sahifa pastga aylantirilganda qora navigatsiya tasmallari tepada mahkam yopishib turadi.
```

---

# 142-Topshiriq: Silliq aylanish (Smooth scrolling) havolalari
## Topshiriq sharti:
Langar linklar bosilganda sahifani sakramasdan, mayin suzib borishi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Smooth Scroll</title>
    <style>
        html { scroll-behavior: smooth; }
        body { font-family: sans-serif; padding: 20px; }
        .block { height: 700px; padding: 20px; margin: 20px 0; border-radius: 8px; }
        #sec1 { background: #fee2e2; }
        #sec2 { background: #e0e7ff; }
    </style>
</head>
<body>
    <nav><a href="#sec1">1-Qismga o'tish</a> | <a href="#sec2">2-Qismga o'tish</a></nav>
    <div id="sec1" class="block"><h2>1-Bo'lim</h2></div>
    <div id="sec2" class="block"><h2>2-Bo'lim</h2></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`html { scroll-behavior: smooth; }` barcha langar havolalarining sakrashini bekor qilib, kinematoqrafik silliq siljish bilan almashtiradi.

## Ishlash natijasi:
```text
Havolaga bosilganda sahifa ko'zni quvontiradigan darajada silliq pastga qarab oqadi.
```

---

# 143-Topshiriq: Off-canvas suriluvchi yon navigatsiya karkasi
## Topshiriq sharti:
Ekranning chetidan surilib chiqadigan zamonaviy mobil menyu uslubi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Off Canvas</title>
    <style>
        body { font-family: sans-serif; margin: 0; overflow-x: hidden; }
        .off-canvas {
            position: fixed;
            top: 0;
            left: -260px;
            width: 250px;
            height: 100%;
            background: #0f172a;
            color: white;
            transition: left 0.3s ease;
            padding: 20px;
            box-shadow: 2px 0 10px rgba(0,0,0,0.2);
        }
        .off-canvas:hover, .off-canvas:focus-within { left: 0; }
        .hint { padding: 20px; }
    </style>
</head>
<body>
    <nav class="off-canvas">
        <h3>Yashirin Menyu</h3>
        <p><a href="#" style="color:#38bdf8;">Bo'lim 1</a></p>
        <p><a href="#" style="color:#38bdf8;">Bo'lim 2</a></p>
    </nav>
    <div class="hint">Chap qirg'oqqa yaqinlashganda menyu surilib chiqadi.</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`left: -260px` boshida menyuni ekrandan tashqariga chiqarib turadi, kerakli holatda `left: 0` ga o'tib ekranga surilib kiradi.

## Ishlash natijasi:
```text
Chap chekkada turgan panel sichqoncha borganda ekranning ichiga silliq kirib keladi.
```

---

# 144-Topshiriq: Mega menyu asosiy navigatsiya karkasi
## Topshiriq sharti:
Katta portallarda barcha toifalarni keng oyna shaklida namoyon etuvchi kengaytirilgan menyu.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Mega Menyu</title>
    <style>
        body { font-family: sans-serif; margin: 0; }
        .navbar { background: #1e293b; padding: 0 40px; position: relative; }
        .nav-item { display: inline-block; }
        .nav-link { color: white; text-decoration: none; padding: 20px; display: block; }
        .mega-box {
            display: none;
            position: absolute;
            left: 0;
            top: 100%;
            width: 100%;
            background: white;
            box-shadow: 0 10px 20px rgba(0,0,0,0.15);
            padding: 30px;
            box-sizing: border-box;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }
        .nav-item:hover .mega-box { display: grid; }
        .col h4 { margin-top: 0; color: #2563eb; }
        .col a { display: block; color: #475569; text-decoration: none; padding: 6px 0; }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-item">
            <a href="#" class="nav-link">Katalog &darr;</a>
            <div class="mega-box">
                <div class="col">
                    <h4>Kompaniyalar</h4>
                    <a href="#">Boshqaruv</a><a href="#">Xodimlar</a>
                </div>
                <div class="col">
                    <h4>Dasturlar</h4>
                    <a href="#">Frontend</a><a href="#">Backend</a>
                </div>
                <div class="col">
                    <h4>Manbalar</h4>
                    <a href="#">Kutubxona</a><a href="#">Fayllar</a>
                </div>
            </div>
        </div>
    </nav>
</body>
</html>
```

## Tushuntirish va Mantiq:
Mega menyu butun ekran eni bo'yicha (`width: 100%`, `left: 0`) ochilib, ichida bir nechta ustunli to'liq katalog tizimini aks ettiradi.

## Ishlash natijasi:
```text
'Katalog' ustiga borganda butun kenglik bo'yicha uch ustunli ulkan toifalar jadvali ochiladi.
```

---

# 145-Topshiriq: :target selektori bilan bo'limni nurli ajratish
## Topshiriq sharti:
Langar havola bosilganda o'sha bo'limni CSS orqali miltillatib belgilash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Target Selektori</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .comment { padding: 15px; border: 1px solid #e2e8f0; margin-bottom: 10px; border-radius: 6px; }
        .comment:target {
            background-color: #fef08a;
            border-color: #eab308;
            box-shadow: 0 0 10px rgba(234,179,8,0.5);
        }
    </style>
</head>
<body>
    <p><a href="#sharh-3">3-sharhga sakrash</a></p>
    <div id="sharh-1" class="comment">1-sharh: Ajoyib dars!</div>
    <div id="sharh-2" class="comment">2-sharh: Foydali ma'lumotlar.</div>
    <div id="sharh-3" class="comment">3-sharh: Rahmat, barchasini tushundim!</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:target` selektori URL manzilidagi xatcho'p (hash fragment `#sharh-3`) qaysi element ID siga teng kelsa, aynan o'sha elementga alohida stil beradi.

## Ishlash natijasi:
```text
Havolaga bosilganda 3-sharh bloki darhol sariq rangli jozibador nur bilan ajralib turadi.
```

---

# 146-Topshiriq: Nuqtali navigatsiya (Dot Navigation)
## Topshiriq sharti:
Zamonaviy slayderlar va bir sahifali taqdimotlar uchun vertikal nuqtali navigatsiya.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Dot Navigation</title>
    <style>
        body { font-family: sans-serif; margin: 0; }
        .dot-nav { position: fixed; right: 20px; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; gap: 12px; }
        .dot { width: 12px; height: 12px; background: #cbd5e1; border-radius: 50%; display: block; text-decoration: none; transition: all 0.2s; }
        .dot:hover, .dot.active { background: #3b82f6; transform: scale(1.3); }
    </style>
</head>
<body>
    <nav class="dot-nav">
        <a href="#slide1" class="dot active" aria-label="1-slayd"></a>
        <a href="#slide2" class="dot" aria-label="2-slayd"></a>
        <a href="#slide3" class="dot" aria-label="3-slayd"></a>
    </nav>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ekranning o'ng tomonida vertikal joylashgan nuqtachalar foydalanuvchiga slaydlarni yoki sahifa qismlarini bitta bosishda almashtirish imkonini beradi.

## Ishlash natijasi:
```text
O'ng chekkada ustma-ust uchta nafis nuqta turadi; birinchisi ko'k rangda yiriklashgan bo'ladi.
```

---

# 147-Topshiriq: To'liq kartochkani bosiluvchi qilish (Stretched link)
## Topshiriq sharti:
Ichidagi bitta havola orqali butun bir blokni bosiluvchi zonaga aylantirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Stretched Link</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        .card { position: relative; border: 1px solid #cbd5e1; padding: 20px; border-radius: 8px; width: 300px; transition: transform 0.2s; }
        .card:hover { transform: translateY(-4px); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .card-link::after {
            content: "";
            position: absolute;
            top: 0; right: 0; bottom: 0; left: 0;
            z-index: 1;
        }
    </style>
</head>
<body>
    <div class="card">
        <h3><a href="/kurs" class="card-link">Frontend Kursi</a></h3>
        <p>HTML va CSS dan boshlab React gacha professional o'rganing.</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`::after` orqali havolaga `position: absolute; inset: 0` berilsa, u butun nisbiy (`position: relative`) kartochkani qoplab oladi va foydalanuvchi qayerga bosmasin havola ishlaydi.

## Ishlash natijasi:
```text
Kartochkaning istalgan bo'sh joyiga bosilganda ham havola ishga tushadi.
```

---

# 148-Topshiriq: Havolani nofaol (Disabled) qilish
## Topshiriq sharti:
CSS orqali havolani bosilmaydigan holatga keltirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Disabled Link</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .disabled-link {
            color: #94a3b8;
            pointer-events: none;
            cursor: not-allowed;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <a href="/keyingi" class="disabled-link" aria-disabled="true">Keyingi Sahifa (Mavjud emas)</a>
</body>
</html>
```

## Tushuntirish va Mantiq:
`pointer-events: none` brauzerning havola bosilishiga oid barcha reaksiyalarini butunlay o'chirib qo'yadi. `aria-disabled='true'` esa ovozli yordamchilarga nofaollikni aytadi.

## Ishlash natijasi:
```text
Xira kulrang bosilmaydigan havola ko'rinadi.
```

---

# 149-Topshiriq: Barcha sahifalar xaritasi (Sitemap list)
## Topshiriq sharti:
Qidiruv robotlari va odamlar uchun barcha bo'limlar daraxtsimon navigatsiyasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Sitemap</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .sitemap-tree ul { list-style-type: square; color: #3b82f6; }
        .sitemap-tree a { color: #1e293b; text-decoration: none; }
        .sitemap-tree a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="sitemap-tree">
        <h2>Sayt Xaritasi</h2>
        <ul>
            <li><a href="/">Bosh sahifa</a></li>
            <li><a href="/kurslar">Kurslar</a>
                <ul>
                    <li><a href="/kurslar/html">HTML5 Asoslari</a></li>
                    <li><a href="/kurslar/css">CSS3 Stillash</a></li>
                </ul>
            </li>
            <li><a href="/kontakt">Aloqa</a></li>
        </ul>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ichma-ich joylashgan `<ul>` ro'yxatlari saytning to'liq arxitekturasini qidiruv tizimlari va tashrif buyuruvchilarga ochiq namoyon etadi.

## Ishlash natijasi:
```text
Kvadrat nuqtali daraxtsimon ichki va tashqi havolalar shajarasi chiqadi.
```

---

# 150-Topshiriq: To'liq korporativ navigatsiya headeri
## Topshiriq sharti:
Logotip, asosiy menyu, qidiruv paneli va harakat tugmasini birlashtirgan professional boshqaruv qismi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Professional Navbar</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', sans-serif; background: #f8fafc; }
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #ffffff;
            padding: 15px 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        }
        .logo { font-size: 22px; font-weight: bold; color: #1e3a8a; text-decoration: none; }
        .nav-links { display: flex; list-style: none; gap: 25px; }
        .nav-links a { text-decoration: none; color: #475569; font-weight: 500; transition: color 0.2s; }
        .nav-links a:hover { color: #2563eb; }
        .btn-portal {
            background: #2563eb;
            color: white;
            padding: 9px 20px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <header>
        <nav class="navbar">
            <a href="/" class="logo">O'zbekiston IT</a>
            <ul class="nav-links">
                <li><a href="#about">Biz haqimizda</a></li>
                <li><a href="#services">Xizmatlar</a></li>
                <li><a href="#academy">Akademiya</a></li>
                <li><a href="#contacts">Aloqa</a></li>
            </ul>
            <a href="#login" class="btn-portal">Tizimga kirish</a>
        </nav>
    </header>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu andoza zamonaviy veb-navigatsiyaning ideal namunasidir: chapda brend logotipi, o'rtada oraliqlari teng tarqalgan asosiy menyu bandlari va o'ngda asosiy harakat (CTA) tugmasi joylashgan.

## Ishlash natijasi:
```text
Oq rangli zamonaviy veb-shapka: ko'k logotip, toza menyu havolalari va o'ngda ko'k rangli 'Tizimga kirish' tugmasi bilan mukammal korporativ header paydo bo'ladi.
```

---

