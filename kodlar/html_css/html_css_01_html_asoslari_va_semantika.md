# HTML Asoslari va Semantika (1-50)

# 1-Topshiriq: <!DOCTYPE html> deklaratsiyasi va HTML5 standarti
## Topshiriq sharti:
HTML5 standartiga to'liq mos keluvchi minimal, toza hujjat deklaratsiyasini tuzing. Brauzer sahifani zamonaviy standartlar rejimida (Standards mode) render qilishi uchun zarur kodni yozing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>HTML5 Standarti</title>
</head>
<body>
    <h1>Salom, O'zbekiston!</h1>
    <p>Ushbu sahifa zamonaviy HTML5 standarti asosida yuklandi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
<!DOCTYPE html> deklaratsiyasi HTML tegi hisoblanmaydi, balki brauzerga hujjat qaysi HTML versiyasida (bu o'rinda HTML5) yozilganligini bildiruvchi ko'rsatmadir. U har doim faylning eng birinchi qatorida joylashishi shart. Ushbu deklaratsiya bo'lmasa, brauzer 'Quirks mode' (moslik rejimi)ga o'tib ketadi va CSS qoidalarini xato talqin qilishi mumkin.

## Ishlash natijasi:
```text
Brauzer yorlig'ida (tab) 'HTML5 Standarti' sarlavhasi chiqadi.
Sahifa maydonida qora rangda katta qalin 'Salom, O'zbekiston!' sarlavhasi va uning ostida standart shriftda matn ko'rinadi.
```

---

# 2-Topshiriq: <html lang='uz'> tili va uning ahamiyati
## Topshiriq sharti:
Veb-sahifaning asosiy ildiz tegi `<html>` ga til atributini (lang='uz') to'g'ri biriktirgan holda xalqaro standartlarga mos boshlang'ich strukturani tuzing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Til Atributi</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 20px; }
        .lang-badge { display: inline-block; background: #007bff; color: #fff; padding: 4px 10px; border-radius: 4px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="lang-badge">UZ</div>
    <h1>O'zbek tili uchun moslashtirilgan hujjat</h1>
    <p>Brauzer va ekran o'quvchi (screen reader) dasturlari sahifa o'zbek tilida ekanligini lang="uz" atributi orqali aniqlaydi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`lang='uz'` atributi qidiruv tizimlari (SEO) va ekranni ovozli o'qish vositalari (accessibility - a11y) uchun juda muhimdir. U brauzerga matnni to'g'ri talaffuz qilish, so'zlarni to'g'ri ajratish (hyphenation) va avtomatik tarjima qilish tizimlariga sahifaning asl tilini tushunishga yordam beradi.

## Ishlash natijasi:
```text
Moviy rangli fon bilan oq rangda 'UZ' belgisi, uning ostida sarlavha va tushuntirish matni chiroyli shriftda chiqadi.
```

---

# 3-Topshiriq: <head> tegi va uning metadata vazifasi
## Topshiriq sharti:
Sahifa foydalanuvchiga to'g'ridan-to'g'ri ko'rinmaydigan, lekin brauzer va texnik xizmatlar uchun o'ta muhim bo'lgan `<head>` qismini to'liq shakllantiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Head Elementi Metama'lumotlari</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }
        .code-box { background: #f4f4f4; border-left: 4px solid #333; padding: 10px; }
    </style>
</head>
<body>
    <h2>Head tegi haqida</h2>
    <div class="code-box">
        Head ichida sahifaning kodi, shriflari, stillari, sarlavhasi va metadata qoidalari saqlanadi.
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
<head> konteyneri hujjat haqidagi texnik ma'lumotlarni (metadata) o'z ichiga oladi. Bu yerga kiritilgan elementlar (title, meta, link, style, script) brauzer ko'rinishida to'g'ridan-to'g'ri sahifaning tana qismida chizilmaydi, biroq sahifaning ishlashi va xulq-atvorini to'liq boshqaradi.

## Ishlash natijasi:
```text
Kulrang fonga ega va chap tomonida qalin qora chizig'i bo'lgan blok ichida head tegining vazifasi matni aks etadi.
```

---

# 4-Topshiriq: <meta charset='UTF-8'> kodlash standarti
## Topshiriq sharti:
O'zbek tilidagi barcha o'ziga xos harflar (o'zbekcha o', g', sh, ch) va xalqaro belgilarni to'g'ri ko'rsatuvchi UTF-8 kodlashini o'rnating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>UTF-8 Kodirovkasi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .highlight { color: #d9534f; font-weight: bold; }
    </style>
</head>
<body>
    <h1>O'zbekiston — go'zal va jo'shqin diyor!</h1>
    <p>Belgilar: <span class="highlight">O', G', o', g', Ғ, Қ, Ҳ, Ў, €, £, ¥, ©, ®, ™</span></p>
    <p>UTF-8 bo'lmasa, yuqoridagi harflar 'krokozyabra' (buzilgan belgilar) bo'lib qoladi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
<meta charset='UTF-8'> brauzerga sahifadagi baytlarni belgilar jadvalining universal formati bo'lgan UTF-8 orqali o'qishni buyuradi. Bu o'zbek kirill va lotin yozuvlari, shuningdek jahonning deyarli barcha alifbolari va emojilarining xatosiz aks etishini ta'minlaydi.

## Ishlash natijasi:
```text
Qizil rangda ajratilgan o'zbekcha maxsus harflar va xalqaro belgilar ro'yxati hech qanday xatosiz aniq va toza ko'rinadi.
```

---

# 5-Topshiriq: <title> sahifa sarlavhasi va SEO roli
## Topshiriq sharti:
Brauzer yorlig'ida va qidiruv tizimlarida professional ko'rinadigan, aniq brending va sahifa mavzusini ifodalovchi `<title>` tegi yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>IT Kurslar va Dasturlash Akademiyasi | Toshkent</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding-top: 50px; }
        .card { max-width: 500px; margin: 0 auto; border: 1px solid #ccc; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <div class="card">
        <h3>Brauzer sarlavhasi (Title)</h3>
        <p>Tepadagi brauzer yorlig'iga qarang: u yerda 'IT Kurslar va Dasturlash Akademiyasi | Toshkent' yozuvi aks etmoqda.</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
<title> elementi har qanday HTML hujjatida majburiy bo'lib, veb-sahifaning nomini belgilaydi. U Google kabi qidiruv tizimlari natijalarida asosiy havola ko'rinishida paydo bo'ladi, xatcho'plar (bookmarks) saqlanganda nom sifatida olinadi.

## Ishlash natijasi:
```text
Markazlashtirilgan oq kartochka ichida sarlavha va matn ko'rinadi; brauzer tabida esa to'liq firma nomi yoziladi.
```

---

# 6-Topshiriq: <meta name='viewport'> mobil moslashuvchanlik deklaratsiyasi
## Topshiriq sharti:
Smartfon va planshetlarda veb-sahifaning to'g'ri masshtabda ochilishini ta'minlovchi viewport meta tegini joylashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mobil Moslashuvchanlik</title>
    <style>
        body { font-family: sans-serif; margin: 0; padding: 15px; }
        .box { background: #28a745; color: white; padding: 20px; text-align: center; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="box">
        <h3>Responsive Tayyorgarlik</h3>
        <p>width=device-width ekranni qurilma kengligiga tenglaydi, initial-scale=1.0 esa boshlang'ich masshtabni 100% ga o'rnatadi.</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu tegsiz mobil brauzerlar veb-saytni xuddi kompyuter monitori (masalan 980px kenglik) uchun yaratilgandek tasavvur qiladi va matnlarni juda kichraytirib, noqulay ko'rsatadi. 'width=device-width' ekranning fizik piksellariga moslashishni, 'initial-scale=1.0' esa kattalashtirmasdan tabiiy hajmda ochishni belgilaydi.

## Ishlash natijasi:
```text
Yashil fonli konteyner mobil qurilmada ham, kompyuterda ham to'liq qulay o'qiladigan hajmda paydo bo'ladi.
```

---

# 7-Topshiriq: <meta name='description'> qidiruv tizimlari uchun tavsif
## Topshiriq sharti:
Google va Yandex natijalarida sahifa nomi ostida chiquvchi 'snippet' matnini belgilovchi meta description tegini yozing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="O'zbekistonda eng zamonaviy Frontend dasturlash bo'yicha to'liq amaliy qo'llanma va bepul darslar to'plami.">
    <title>Frontend Darslari</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 25px; }
        .snippet { border: 1px solid #dfe1e5; border-radius: 8px; padding: 16px; max-width: 600px; font-family: Roboto, Arial, sans-serif; }
        .snippet-title { color: #1a0dab; font-size: 20px; cursor: pointer; text-decoration: none; }
        .snippet-url { color: #202124; font-size: 14px; margin: 4px 0; }
        .snippet-desc { color: #4d5156; font-size: 14px; line-height: 1.5; }
    </style>
</head>
<body>
    <h2>Google Qidiruv Natijasi Imitatsiyasi:</h2>
    <div class="snippet">
        <a href="#" class="snippet-title">Frontend Darslari - Mukammal Ta'lim</a>
        <div class="snippet-url">https://frontend.uz/kurslar</div>
        <div class="snippet-desc">O'zbekistonda eng zamonaviy Frontend dasturlash bo'yicha to'liq amaliy qo'llanma va bepul darslar to'plami.</div>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<meta name='description' content='...'>` sahifaning qisqacha mazmunini ifodalaydi. Tavsiya etilgan uzunligi 150-160 belgidan oshmasligi kerak. Qidiruv tizimlari ushbu matndan foydalanuvchiga qidiruv natijalarida (snippet) ko'rsatish uchun foydalanadi.

## Ishlash natijasi:
```text
Google qidiruv natijalariga o'xshash ko'k sarlavhali, yashil/kulrang havolali va pastida tavsif matni bo'lgan blok ko'rinadi.
```

---

# 8-Topshiriq: <meta name='keywords'> kalit so'zlar
## Topshiriq sharti:
Sahifaning mavzusiga aloqador kalit so'zlarni meta keywords tegi orqali ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="keywords" content="html, css, web dizayn, dasturlash, frontend, o'zbekcha darslar">
    <title>Kalit So'zlar Namoyishi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .tag { background: #e9ecef; border: 1px solid #ced4da; padding: 5px 12px; border-radius: 20px; display: inline-block; margin: 4px; font-size: 13px; }
    </style>
</head>
<body>
    <h3>Sahifaga biriktirilgan kalit so'zlar:</h3>
    <span class="tag">HTML</span>
    <span class="tag">CSS</span>
    <span class="tag">Web dizayn</span>
    <span class="tag">Frontend</span>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<meta name='keywords' content='...'>` tegi qidiruv tizimlariga sahifaning asosiy mavzulari va tegishli atamalarini bildiradi. Zamonaviy Google qidiruv algoritmi spam tufayli unga kamroq e'tibor qaratsa-da, ichki qidiruv tizimlari va korporativ kataloglarda saqlanadi.

## Ishlash natijasi:
```text
Kulrang yumaloq burchakli 'tag' kapsulalari shaklida kalit so'zlar ro'yxati chiziladi.
```

---

# 9-Topshiriq: <meta name='author'> mualliflik atributi
## Topshiriq sharti:
Muallif va ishlab chiquvchi haqidagi ma'lumotni saqlovchi meta author tegini joylashtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="author" content="Alisher Navoiy nomidagi Milliy IT Markazi">
    <title>Mualliflik Ma'lumoti</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .info { background: #e8f4fd; border-left: 4px solid #17a2b8; padding: 12px; }
    </style>
</head>
<body>
    <div class="info">
        <p>Ushbu kod mualliflik huquqiga ega bo'lib, metadata orqali muallif ko'rsatilgan.</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<meta name='author' content='...'>` veb-sahifani yaratgan shaxs, jamoa yoki kompaniya nomini texnik metama'lumot sifatida kiritish imkonini beradi.

## Ishlash natijasi:
```text
Och havorang fon va ko'k hoshiyali xabarnoma ko'rinadi.
```

---

# 10-Topshiriq: <meta name='robots'> qidiruv botlarini boshqarish
## Topshiriq sharti:
Sahifani qidiruv tizimlari indekslashi va undagi havolalarni kuzatishini (yoki taqiqlashini) nazorat qiluvchi robots meta tegini yozing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="robots" content="index, follow">
    <title>Robots Boshqaruvi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .status { padding: 10px; background: #d4edda; color: #155724; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="status">
        Robots: <strong>index, follow</strong> (Indekslashga va havolalar bo'ylab o'tishga ruxsat berilgan).
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`content='index, follow'` qidiruv botlariga sahifani o'z bazasiga kiritish va undagi havolalarni tekshirishni bildiradi. Agar 'noindex, nofollow' yozilsa, sahifa qidiruv natijalaridan yashiriladi (masalan, admin panellarda).

## Ishlash natijasi:
```text
Yashil muvaffaqiyat blokida robots holati tasvirlanadi.
```

---

# 11-Topshiriq: <link rel='icon'> veb-sayt faviconi qo'shish
## Topshiriq sharti:
Brauzer yorlig'ida veb-sayt logotipi (favicon) ko'rinishi uchun SVG yoki PNG formatidagi ikonkani bog'lovchi kodni yozing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><circle cx='50' cy='50' r='50' fill='%23007bff'/><text x='50%' y='65%' font-size='50' text-anchor='middle' fill='white'>A</text></svg>">
    <title>Favicon Namoyishi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; text-align: center; }
        .fav-demo { display: inline-flex; align-items: center; gap: 8px; border: 1px solid #ccc; padding: 8px 16px; border-radius: 20px; }
    </style>
</head>
<body>
    <div class="fav-demo">
        <svg width="24" height="24" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="50" fill="#007bff"/>
            <text x="50%" y="65%" font-size="50" text-anchor="middle" fill="white">A</text>
        </svg>
        <span>Brauzer yorlig'ida ushbu belgi paydo bo'ladi</span>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<link rel='icon' type='image/svg+xml' href='...'>` brauzerning sarlavha panelida sayt logotipini aks ettiradi. Zamonaviy vebda inline data URI yoki SVG faviconlardan foydalanish yuqori tiniqlikni (Retina ekranlar) ta'minlaydi.

## Ishlash natijasi:
```text
Dumaloq ko'k rangli va markazida oq 'A' harfi bor logotip va uning yonida matnli tushuntirish paneli aks etadi.
```

---

# 12-Topshiriq: <body> tegi va hujjat tanasi
## Topshiriq sharti:
Foydalanuvchiga ko'rinadigan barcha vizual elementlarni o'zida birlashtiruvchi `<body>` tegining asosiy tuzilishini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Body Elementi</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background-color: #fafafa;
            color: #333;
            font-family: Arial, sans-serif;
        }
    </style>
</head>
<body>
    <h1>Sahifa Tanasi (Body)</h1>
    <p>Foydalanuvchi ekranda ko'radigan barcha matnlar, rasmlar, videolar va tugmalar aynan body tegi ichida joylashadi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<body>` tegi HTML hujjatining barcha ko'rinadigan tarkibini (matnlar, giperhavolalar, tasvirlar, jadvallar, ro'yxatlar) o'z ichiga oladi. Bir hujjatda faqat bitta <body> tegi bo'lishi mumkin.

## Ishlash natijasi:
```text
Och kulrang orqa fon ustida qora rangdagi sarlavha va matn ko'rinadi.
```

---

# 13-Topshiriq: <header> semantik tegi
## Topshiriq sharti:
Saytning yoki alohida bir bo'limning kirish va tanishtiruv qismini ifodalovchi semantik `<header>` blokini hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Header Semantikasi</title>
    <style>
        body { font-family: sans-serif; margin: 0; }
        .site-header { background: #2c3e50; color: white; padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 24px; font-weight: bold; }
        .tagline { font-size: 14px; opacity: 0.8; }
    </style>
</head>
<body>
    <header class="site-header">
        <div class="logo">UzbekDev</div>
        <div class="tagline">O'zbekiston dasturchilar hamjamiyati</div>
    </header>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<header>` tegi sahifa yoki muayyan maqolaning yuqori tanishtiruv qismini bildiradi. Odatda uning ichida logotip, shior, qidiruv paneli yoki navigatsiya havolalari joylashadi. Uni oddiy `<div>` dan farqi — semantik jihatdan qidiruv botlari va ekran o'quvchilarga sahifa boshini anglatishidir.

## Ishlash natijasi:
```text
To'q ko'k fonda chap tomonda 'UzbekDev' logotipi, o'ng tomonda esa shior matni bir tekisda joylashgan sarlavha paneli hosil bo'ladi.
```

---

# 14-Topshiriq: <nav> navigatsiya semantik tegi
## Topshiriq sharti:
Faqat asosiy sahifalararo o'tish havolalarini saqlaydigan semantik `<nav>` menyusini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Nav Semantikasi</title>
    <style>
        body { font-family: sans-serif; margin: 0; }
        .main-nav { background: #34495e; padding: 10px 30px; }
        .nav-list { list-style: none; margin: 0; padding: 0; display: flex; gap: 20px; }
        .nav-list a { color: #ecf0f1; text-decoration: none; font-weight: 500; }
        .nav-list a:hover { color: #3498db; }
    </style>
</head>
<body>
    <nav class="main-nav">
        <ul class="nav-list">
            <li><a href="#home">Bosh sahifa</a></li>
            <li><a href="#courses">Kurslar</a></li>
            <li><a href="#about">Biz haqimizda</a></li>
            <li><a href="#contact">Aloqa</a></li>
        </ul>
    </nav>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<nav>` elementi veb-saytning asosiy navigatsiya blokini bildiradi. Sahifadagi barcha havolalar nav ichiga olinmaydi, faqat asosiy menyular, mundarija yoki sahifalash (pagination) bloklari uning ichida bo'lishi semantik jihatdan to'g'ri hisoblanadi.

## Ishlash natijasi:
```text
To'q kulrang tasmada gorizontal joylashgan 'Bosh sahifa', 'Kurslar', 'Biz haqimizda', 'Aloqa' havolalaridan iborat chiroyli navigatsiya menyusi paydo bo'ladi.
```

---

# 15-Topshiriq: <main> asosiy kontent bloki
## Topshiriq sharti:
Sahifadagi yagona va asosiy mazmunni o'zida saqlaydigan semantik `<main>` blokini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Main Elementi</title>
    <style>
        body { font-family: sans-serif; margin: 0; background: #f8f9fa; }
        main { max-width: 800px; margin: 30px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.08); }
    </style>
</head>
<body>
    <main>
        <h1>Web Dasturlash Asoslari</h1>
        <p>Ushbu bo'lim sahifaning asosiy va takrorlanmas kontentini ifodalaydi. Bir sahifada faqat bitta ko'rinuvchi main tegi bo'lishi shart.</p>
    </main>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<main>` tegi sahifaning asosiy mavzusiga bevosita tegishli bo'lgan kontentni saqlaydi. Unda sayt bo'ylab takrorlanuvchi elementlar (header, nav menyulari, footer, mualliflik huquqi ma'lumotlari) joylashtirilmasligi lozim.

## Ishlash natijasi:
```text
Ekran markazida oq soya berilgan blok ichida asosiy sarlavha va matn ko'rinadi.
```

---

# 16-Topshiriq: <section> mantiqiy bo'lim tegi
## Topshiriq sharti:
Umumiy mavzuga oid va o'z sarlavhasiga ega bo'lgan alohida mantiqiy blokni `<section>` orqali ifodalang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Section Semantikasi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        section { border: 1px solid #e1e4e8; border-radius: 6px; padding: 20px; margin-bottom: 20px; }
        section h2 { color: #24292e; border-bottom: 2px solid #0366d6; padding-bottom: 6px; }
    </style>
</head>
<body>
    <section>
        <h2>Frontend Texnologiyalari</h2>
        <p>HTML, CSS va JavaScript zamonaviy veb-ilovalarning asosiy poydevoridir.</p>
    </section>
    <section>
        <h2>Backend Texnologiyalari</h2>
        <p>Node.js, Python, Java va Go server qismini yaratishda ishlatiladi.</p>
    </section>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<section>` tegi hujjatning umumiy mavzuga ega bo'lgan mantiqiy bo'limini ifodalaydi. Har bir `<section>` deyarli har doim o'zining sarlavhasi (`<h1>`-`<h6>`)ga ega bo'lishi qat'iy tavsiya etiladi.

## Ishlash natijasi:
```text
Har biri ko'k chiziqli sarlavhaga ega ikkita alohida hoshiyalangan ma'lumot bo'limi namoyon bo'ladi.
```

---

# 17-Topshiriq: <article> mustaqil maqola bloki
## Topshiriq sharti:
Boshqa sahifalarda yoki platformalarda (masalan, RSS tasmada) mustaqil ma'noga ega bo'la oladigan `<article>` blog xabarini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Article Semantikasi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; background: #eef2f5; }
        article { background: white; padding: 24px; border-radius: 8px; max-width: 600px; margin: 0 auto; }
        .meta { color: #6c757d; font-size: 13px; margin-bottom: 12px; }
    </style>
</head>
<body>
    <article>
        <h2>Sun'iy intellektning veb-dasturlashdagi o'rni</h2>
        <div class="meta">Muallif: Sanjarbek | Sana: 2026-yil 12-may</div>
        <p>Bugungi kunda sun'iy intellekt kod yozish tezligini va sifatini oshirishda dasturchilarning ajralmas yordamchisiga aylanmoqda.</p>
    </article>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<article>` tegi o'z-o'zidan mustaqil, to'laqonli ma'lumot birligini anglatadi (masalan, blog posti, yangilik maqolasi, forum xabari, mahsulot sharhi). U kontekstdan ajratib olinganda ham o'z mustaqil ma'nosini saqlab qoladi.

## Ishlash natijasi:
```text
Markazlashtirilgan oq kartochkada maqola sarlavhasi, sana/muallif metasi va qisqa mazmuni joylashadi.
```

---

# 18-Topshiriq: <aside> qo'shimcha yon panel bloki
## Topshiriq sharti:
Asosiy kontentga bilvosita bog'liq bo'lgan tavsiyalar, tegishli havolalar yoki reklamalarni ifodalovchi `<aside>` blokini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Aside Semantikasi</title>
    <style>
        body { font-family: sans-serif; display: flex; gap: 20px; padding: 20px; }
        .content { flex: 3; background: #fff; padding: 20px; border: 1px solid #ddd; }
        aside { flex: 1; background: #f9f9f9; padding: 20px; border-left: 3px solid #ff9800; }
    </style>
</head>
<body>
    <div class="content">
        <h1>HTML5 O'rganish Bo'yicha Asosiy Qo'llanma</h1>
        <p>Semantik teglardan to'g'ri foydalanish veb-saytning qulayligi va SEO samaradorligini kafolatlaydi.</p>
    </div>
    <aside>
        <h3>Foydali manbalar</h3>
        <ul>
            <li>MDN Web Docs</li>
            <li>W3C Standartlari</li>
            <li>CSS-Tricks</li>
        </ul>
    </aside>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<aside>` tegi asosiy matnga bilvosita daxldor bo'lgan qo'shimcha ma'lumotlarni saqlaydi. Bu odatda saytning yon paneli (sidebar), atamalar lug'ati yoki tavsiya etilayotgan maqolalar ro'yxati bo'ladi.

## Ishlash natijasi:
```text
Chap tomonda asosiy maqola maydoni, o'ng tomonda sariq chiziqli yon panel va unda havolalar ro'yxati chiqadi.
```

---

# 19-Topshiriq: <footer> sahifa yoki blok quyi qismi
## Topshiriq sharti:
Mualliflik huquqi (copyright), ijtimoiy tarmoqlar va kontakt ma'lumotlarini o'z ichiga oluvchi semantik `<footer>` tuzing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Footer Semantikasi</title>
    <style>
        body { font-family: sans-serif; margin: 0; min-height: 100vh; display: flex; flex-direction: column; }
        .main-body { flex: 1; padding: 20px; }
        footer { background: #1a1a1a; color: #aaa; padding: 25px 20px; text-align: center; }
        footer a { color: #fff; text-decoration: none; margin: 0 10px; }
        footer a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="main-body">
        <h1>Sahifaning asosiy maydoni</h1>
    </div>
    <footer>
        <p>&copy; 2026 IT Park Uzbekistan. Barcha huquqlar himoyalangan.</p>
        <nav>
            <a href="#privacy">Maxfiylik siyosati</a>
            <a href="#terms">Foydalanish qoidalari</a>
            <a href="#support">Qo'llab-quvvatlash</a>
        </nav>
    </footer>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<footer>` tegi sahifa yoki uning biror qismining eng quyi ma'lumotlarini o'z ichiga oladi. U yerda mualliflik huquqlari, aloqa havolalari, xaritadagi manzil va huquqiy hujjatlarga havolalar beriladi.

## Ishlash natijasi:
```text
Sahifaning pastki qismida to'q qora fonda kulrang matn va oq rangdagi havolalar joylashgan podval chiqadi.
```

---

# 20-Topshiriq: <figure> va <figcaption> illyustratsiya teglari
## Topshiriq sharti:
Rasm yoki diagrammaga rasmiy tushuntirish yozuvi biriktirilgan semantik `<figure>` va `<figcaption>` blokini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Figure va Figcaption</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        figure { margin: 0; max-width: 400px; border: 1px solid #ccc; padding: 8px; border-radius: 6px; background: #fff; }
        figure svg { width: 100%; height: auto; border-radius: 4px; display: block; }
        figcaption { font-size: 13px; color: #555; text-align: center; padding-top: 8px; font-style: italic; }
    </style>
</head>
<body>
    <figure>
        <svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg">
            <rect width="400" height="200" fill="#4a90e2"/>
            <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#fff" font-size="22">Grafik Namoyish</text>
        </svg>
        <figcaption>1.1-shakl. Tizim arxitekturasining soddalashtirilgan modeli.</figcaption>
    </figure>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<figure>` o'z-o'zidan mustaqil rasmlar, diagrammalar, kod parchalari yoki illyustratsiyalarni o'rash uchun xizmat qiladi. `<figcaption>` esa ushbu media tarkibiga rasmiy izoh beruvchi yagona semantik teg hisoblanadi.

## Ishlash natijasi:
```text
Moviy illyustratsiya to'g'ri to'rtburchagi ostida qiya shriftda '1.1-shakl. Tizim arxitekturasining soddalashtirilgan modeli.' yozuvi markazda aks etadi.
```

---

# 21-Topshiriq: <time> tegi va uning datetime atributi
## Topshiriq sharti:
Foydalanuvchi va mashina tushunadigan sanani ko'rsatish uchun `<time>` tegidan to'g'ri foydalanishni amalga oshiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Time Elementi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        time { font-weight: bold; color: #2e7d32; }
    </style>
</head>
<body>
    <article>
        <h3>Veb Texnologiyalar Konferensiyasi</h3>
        <p>Tadbir boshlanish sanasi: <time datetime="2026-09-01T09:00">2026-yil 1-sentyabr, 09:00</time></p>
    </article>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<time>` tegi vaqt yoki sanani belgilaydi. `datetime` atributi esa ISO 8601 standartidagi mashina o'qiy oladigan formatni (masalan '2026-09-01T09:00') kiritish uchun ishlatiladi. Bu taqvim ilovalari va qidiruv botlari tadbir vaqtini aniq anglashiga yordam beradi.

## Ishlash natijasi:
```text
Yashil va qalin shriftda tadbir sanasi va soati matn ichida ifodalanadi.
```

---

# 22-Topshiriq: <address> aloqa va muallif ma'lumotlari
## Topshiriq sharti:
Hujjat yoki maqola muallifining aloqa ma'lumotlarini qonuniy va semantik tarzda taqdim etuvchi `<address>` blokini tuzing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Address Semantikasi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        address { font-style: normal; line-height: 1.6; border: 1px dashed #7b1fa2; padding: 15px; border-radius: 6px; width: fit-content; }
        address a { color: #7b1fa2; font-weight: bold; }
    </style>
</head>
<body>
    <address>
        <strong>Kompaniya Bosh Qarorgohi:</strong><br>
        Amir Temur shoh ko'chasi, 108-uy<br>
        Toshkent shahri, O'zbekiston<br>
        Email: <a href="mailto:info@company.uz">info@company.uz</a><br>
        Telefon: <a href="tel:+998712000000">+998 (71) 200-00-00</a>
    </address>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<address>` tegi faqatgina jismoniy manzil uchun emas, balki sahifa yoki eng yaqin `<article>` muallifi bilan bog'lanish kontaktlari (email, telefon, manzil, veb-sayt) uchun mo'ljallangan.

## Ishlash natijasi:
```text
Siyohrang punktir hoshiyaga olingan blok ichida kompaniya manzili va bosiladigan aloqa havolalari ko'rinadi.
```

---

# 23-Topshiriq: <details> va <summary> mahalliy interaktiv blok
## Topshiriq sharti:
JavaScript ishlatmasdan, sof HTML orqali ochilib-yopiluvchi savol-javob akordeonini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Details va Summary</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        details { background: #f1f8ff; border: 1px solid #c8e1ff; border-radius: 6px; padding: 12px; margin-bottom: 10px; }
        summary { font-weight: bold; cursor: pointer; outline: none; }
        details[open] { background: #e6f3ff; }
        p { margin-top: 10px; margin-bottom: 0; }
    </style>
</head>
<body>
    <details>
        <summary>HTML5 nima uchun semantik hisoblanadi?</summary>
        <p>Chunki undagi teglarning nomlari o'z ichidagi kontentning ma'nosini va rolini brauzer, dasturchi va qidiruv tizimlariga aniq ifoda etadi.</p>
    </details>
    <details>
        <summary>CSS Box Model nimalardan tashkil topgan?</summary>
        <p>Box Model 4 ta qatlamdan iborat: Content, Padding, Border va Margin.</p>
    </details>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<details>` brauzer tomonidan taqdim etiladigan tabiiy interaktiv vidjetdir. `<summary>` uning har doim ko'rinib turadigan sarlavhasini belgilaydi. Foydalanuvchi unga bosganda brauzer avtomatik ravishda unga `open` atributini qo'shadi va yashirin matn ochiladi.

## Ishlash natijasi:
```text
Bosilganda pastga qarab yoyiluvchi ikkita och moviy rangli savol-javob vidjeti chiqadi.
```

---

# 24-Topshiriq: <dialog> mahalliy modal oyna tegi
## Topshiriq sharti:
HTML5 ning zamonaviy modal muloqot oynasi `<dialog>` tegini yaratish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Dialog Elementi</title>
    <style>
        body { font-family: sans-serif; padding: 30px; text-align: center; }
        dialog { border: none; border-radius: 8px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); padding: 25px; max-width: 400px; }
        dialog::backdrop { background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(3px); }
        .btn { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Modal Oyna Namoyishi</h1>
    <button class="btn" onclick="document.getElementById('myModal').showModal()">Oynani ochish</button>

    <dialog id="myModal">
        <h3>Muhim bildirishnoma</h3>
        <p>Siz tizimga muvaffaqiyatli kirdingiz!</p>
        <button class="btn" onclick="document.getElementById('myModal').close()">Yopish</button>
    </dialog>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<dialog>` tegi brauzer darajasidagi rasmiy pop-up va dialog oynasini ifodalaydi. `showModal()` metodi orqali ochilganda brauzer orqa fonni xiralashtiruvchi `::backdrop` psevdo-elementini faollashtiradi va klaviaturadagi ESC tugmasi bilan yopilishni tabiiy ta'minlaydi.

## Ishlash natijasi:
```text
Tugma bosilganda ekranning qoq o'rtasida qorong'ilatilgan fon ustida oq rangli chiroyli bildirishnoma oynasi chiqadi.
```

---

# 25-Topshiriq: <template> HTML shablon tegi
## Topshiriq sharti:
Sahifaga dastlab render qilinmaydigan, faqat talab etilganda JavaScript tomonidan nusxa olinadigan shablon blokini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Template Tege</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .user-card { border: 1px solid #ddd; padding: 10px; margin-top: 10px; border-radius: 4px; }
    </style>
</head>
<body>
    <h2>Foydalanuvchilar Ro'yxati</h2>
    <div id="container"></div>

    <template id="userTemplate">
        <div class="user-card">
            <h4 class="name">Ism Familiya</h4>
            <span class="role">Lavozim</span>
        </div>
    </template>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<template>` tegi ichidagi HTML elementlar sahifa ochilganda brauzer DOM daraxtida saqlanadi, lekin ekranga chizilmaydi va rasmlari yoki skriptlari darhol yuklanmaydi. U faqat dinamik ravishda klonlash uchun xizmat qiladi.

## Ishlash natijasi:
```text
Ekranda faqatgina 'Foydalanuvchilar Ro'yxati' sarlavhasi ko'rinadi, shablon esa ekranda ko'rinmasdan xotirada turadi.
```

---

# 26-Topshiriq: <mark> matnni ajratib ko'rsatish tegi
## Topshiriq sharti:
Qidiruv natijalarida yoki muhim qaydlarda topilgan matn qismini semantik ajratuvchi `<mark>` tegini qo'llang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Mark Elementi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; line-height: 1.6; }
        mark { background-color: #ffe066; padding: 2px 4px; border-radius: 2px; }
    </style>
</head>
<body>
    <p>Qidiruv natijasi: Bizning maqsadimiz <mark>zamonaviy IT</mark> ta'limini har bir yoshga yetkazish va <mark>zamonaviy IT</mark> sohasida yuqori maoshli mutaxassislar tayyorlashdir.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<mark>` tegi xuddi marker qalami bilan bo'yalgandek matn qismini yorqin sariq fon bilan ajratib ko'rsatadi. U o'quvchining diqqatini qaratish yoki qidirilgan so'zlarni ta'kidlash uchun mo'ljallangan.

## Ishlash natijasi:
```text
Matn ichidagi 'zamonaviy IT' iboralari och sariq fonga bo'yalib diqqatni tortadi.
```

---

# 27-Topshiriq: <div> nosemantik blok konteyneri
## Topshiriq sharti:
Hech qanday ma'no yuklanmagan, faqatgina stillash va joylashtirish (CSS layout) uchun ishlatiladigan `<div>` tegi misolini tuzing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Div Elementi</title>
    <style>
        .grid-container { display: flex; gap: 15px; padding: 20px; }
        .box { flex: 1; height: 100px; background: #6c5ce7; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; }
    </style>
</head>
<body>
    <div class="grid-container">
        <div class="box">Blok 1</div>
        <div class="box">Blok 2</div>
        <div class="box">Blok 3</div>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<div>` (division) elementi hech qanday semantik ma'noga ega emas. U faqatgina CSS orqali dizayn berish, elementlarni guruhlash yoki JavaScript orqali boshqarish uchun blokli konteyner vazifasini bajaradi.

## Ishlash natijasi:
```text
Gorizontal ravishda yonma-yon joylashgan 3 ta binafsharang to'rtburchak blok ko'rinadi.
```

---

# 28-Topshiriq: <span> nosemantik qator ichi konteyneri
## Topshiriq sharti:
Matn ichidagi muayyan so'zni stil berish uchun ajratib oluvchi inline `<span>` tegini yozing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Span Elementi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; font-size: 18px; }
        .gradient-text { background: linear-gradient(45deg, #ff6b6b, #4ecdc4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold; }
    </style>
</head>
<body>
    <p>Kelajak kasblari ichida eng daromadlisi — bu <span class="gradient-text">Sun'iy Intellekt Muhandisligi</span> hisoblanadi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<span>` tegi qator ichi (inline) bo'lgan nosemantik konteynerdir. U matn oqimini buzmagan holda uning alohida bir qismiga CSS ranglari, shriftlari yoki stillarini berish uchun qo'llaniladi.

## Ishlash natijasi:
```text
Oddiy matn orasida 'Sun'iy Intellekt Muhandisligi' iborasi rang-barang gradient tusda jilolanadi.
```

---

# 29-Topshiriq: Semantik blog posti to'liq tuzilmasi
## Topshiriq sharti:
Header, nav, main, article, aside va footer teglarini birlashtirib, mukammal semantik blog sahifasini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog Post Maketi</title>
    <style>
        body { font-family: sans-serif; margin: 0; background: #f0f2f5; }
        header { background: #1e293b; color: white; padding: 15px 30px; display: flex; justify-content: space-between; }
        nav a { color: #94a3b8; text-decoration: none; margin-left: 15px; }
        .layout { display: flex; max-width: 1000px; margin: 20px auto; gap: 20px; padding: 0 15px; }
        main { flex: 3; }
        article { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        aside { flex: 1; background: white; padding: 20px; border-radius: 8px; height: fit-content; }
        footer { background: #0f172a; color: white; text-align: center; padding: 20px; margin-top: 40px; }
    </style>
</head>
<body>
    <header>
        <div><strong>TexnoBlog</strong></div>
        <nav><a href="#">Bosh sahifa</a><a href="#">Maqolalar</a></nav>
    </header>
    <div class="layout">
        <main>
            <article>
                <h1>CSS Grid va Flexbox Taqqoslovi</h1>
                <p>Ushbu maqolada ikki asosiy joylashtirish tizimining farqlari yoritiladi...</p>
            </article>
        </main>
        <aside>
            <h3>Tegishli mavzular</h3>
            <p>HTML Semantikasi</p>
        </aside>
    </div>
    <footer>&copy; 2026 TexnoBlog</footer>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu maket barcha asosiy semantik teglarni o'z o'rnida ishlatishning namunaviy andozasidir: sayt yuqorisi `<header>`, menyu `<nav>`, asosiy o'zak `<main>`, mustaqil kontent `<article>`, yon bo'lim `<aside>` va pastki yakun `<footer>` bilan qamrab olingan.

## Ishlash natijasi:
```text
Tepadagi to'q boshqaruv paneli, o'rtada keng oq maqola bloki va yonida qo'shimcha menyu, pastda esa podval bilan to'liq blog ko'rinishi hosil bo'ladi.
```

---

# 30-Topshiriq: Yangiliklar portali bosh sahifasi semantikasi
## Topshiriq sharti:
Kun yangiliklari, dolzarb mavzular va tasmadan iborat axborot portali strukturasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Kun Yangiliklari</title>
    <style>
        body { font-family: 'Georgia', serif; margin: 0; background: #fff; }
        header { border-bottom: 2px solid #000; padding: 20px; text-align: center; }
        .breaking { background: #c0392b; color: white; padding: 8px 20px; font-weight: bold; }
        .grid { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; padding: 20px; max-width: 1000px; margin: 0 auto; }
        article { border-bottom: 1px solid #ddd; padding-bottom: 15px; }
    </style>
</head>
<body>
    <header>
        <h1>O'ZBEKISTON AXBOROTI</h1>
    </header>
    <div class="breaking">Tezkor: Yangi texnologik park ochildi!</div>
    <main class="grid">
        <section>
            <article>
                <h2>Iqtisodiyot sohasidagi islohotlar</h2>
                <p>Bugun poytaxtda muhim iqtisodiy forum o'z ishini boshladi.</p>
            </article>
        </section>
        <aside>
            <h3>Qisqa xabarlar</h3>
            <p>Ob-havo: Ertaga iliq va quyoshli bo'ladi.</p>
        </aside>
    </main>
</body>
</html>
```

## Tushuntirish va Mantiq:
Gazeta uslubidagi veb-sahifa klassik semantikaga ega. Sarlavha qismi `<header>`, dolzarb ogohlantirish, asosiy voqealar `<main>` ichidagi `<section>` va `<article>`lar hamda qisqa xabarlar `<aside>` da berilgan.

## Ishlash natijasi:
```text
Klassik gazeta formatidagi qora qalin sarlavha, qizil rangli tezkor xabar tasmallari va ikki ustunli yangiliklar joylashuvi namoyon bo'ladi.
```

---

# 31-Topshiriq: Mahsulot sahifasi (e-commerce product) semantik tuzilishi
## Topshiriq sharti:
Onlayn do'konda mahsulot rasmi, narxi, xususiyatlari va sotib olish tugmasini to'g'ri teglarda shakllantiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Smartfon Mahsulot Kartochkasi</title>
    <style>
        body { font-family: sans-serif; background: #f5f5f5; padding: 20px; }
        .product-card { max-width: 700px; margin: 0 auto; background: white; border-radius: 8px; display: flex; padding: 20px; gap: 20px; }
        .product-media { flex: 1; }
        .product-details { flex: 1; }
        .price { font-size: 24px; color: #2ecc71; font-weight: bold; margin: 15px 0; }
        .btn-buy { background: #e67e22; color: white; border: none; padding: 12px 24px; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <main>
        <article class="product-card">
            <figure class="product-media">
                <svg viewBox="0 0 200 200" width="100%"><rect width="200" height="200" fill="#34495e" rx="10"/><text x="50%" y="50%" fill="#fff" dominant-baseline="middle" text-anchor="middle">Smartfon</text></svg>
                <figcaption>Rangi: To'q kulrang</figcaption>
            </figure>
            <section class="product-details">
                <h1>Galaxy Pro Max 2026</h1>
                <p>256GB xotira, 12GB tezkor xotira, AMOLED ekran.</p>
                <div class="price">9 499 000 so'm</div>
                <button class="btn-buy">Savatga qo'shish</button>
            </section>
        </article>
    </main>
</body>
</html>
```

## Tushuntirish va Mantiq:
Mahsulot kartochkasi o'z-o'zidan mustaqil savdo obyekti bo'lganligi sababli u `<article>` ichiga olinadi. Rasm `<figure>` va `<figcaption>` ga, uning xususiyatlari esa `<section>` ga ajratilgan.

## Ishlash natijasi:
```text
Chap tomonda to'q fonli smartfon rasmi, o'ng tomonda mahsulot nomi, texnik ko'rsatkichlari, yashil rangli narx va to'q sariq xarid tugmasi joylashadi.
```

---

# 32-Topshiriq: Foydalanuvchi profili sahifasi semantik maketi
## Topshiriq sharti:
Foydalanuvchi avatari, tarjimai holi, statistikasi va kontaktlarini o'z ichiga olgan profil sahifasi tuzing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Foydalanuvchi Profili</title>
    <style>
        body { font-family: sans-serif; background: #e9ecef; padding: 30px; }
        .profile { max-width: 500px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        .profile-header { background: #3f51b5; color: white; padding: 30px; text-align: center; }
        .stats { display: flex; justify-content: space-around; padding: 20px; border-bottom: 1px solid #eee; }
        .bio { padding: 20px; }
    </style>
</head>
<body>
    <main>
        <article class="profile">
            <header class="profile-header">
                <h2>Jasurbek Karimov</h2>
                <p>Senior Frontend Dasturchi</p>
            </header>
            <section class="stats">
                <div><strong>48</strong><br>Loyihalar</div>
                <div><strong>1.2k</strong><br>Obunachilar</div>
            </section>
            <section class="bio">
                <h3>Biografiya</h3>
                <p>O'zbekistonda zamonaviy interfeyslar va yuqori samarali web tizimlar yaratish bilan shug'ullanaman.</p>
            </section>
        </article>
    </main>
</body>
</html>
```

## Tushuntirish va Mantiq:
Profil kartochkasi alohida `<article>` bo'lib, uning ichida foydalanuvchining shaxsiy kirish qismi uchun `<header>`, statistik ma'lumotlar va biografiya uchun alohida `<section>` bloklari xizmat qiladi.

## Ishlash natijasi:
```text
To'q ko'k shapkali, o'rtada raqamli statistikasi va pastida biografik matni bo'lgan professional foydalanuvchi profili paydo bo'ladi.
```

---

# 33-Topshiriq: Portfolio veb-sayt semantik arxitekturasi
## Topshiriq sharti:
Frilanser dasturchining o'z ishlarini taqdim etuvchi bir sahifali portfolio strukturasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Dasturchi Portfoliosi</title>
    <style>
        body { font-family: sans-serif; margin: 0; line-height: 1.6; }
        header { background: #111; color: #fff; padding: 60px 20px; text-align: center; }
        section { padding: 40px 20px; max-width: 800px; margin: 0 auto; }
        .projects-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .project-card { border: 1px solid #ddd; padding: 15px; border-radius: 6px; }
    </style>
</head>
<body>
    <header>
        <h1>Madina Rustamova</h1>
        <p>UI/UX Dizayner va Web Dasturchi</p>
    </header>
    <main>
        <section id="about">
            <h2>Haqimda</h2>
            <p>5 yildan buyon xalqaro mijozlar uchun jozibador dizayn va kod yarataman.</p>
        </section>
        <section id="projects">
            <h2>Bajarilgan ishlar</h2>
            <div class="projects-grid">
                <article class="project-card">
                    <h3>FinTech Ilovasi</h3>
                    <p>To'lov tizimi uchun to'liq responsive veb-sayt.</p>
                </article>
                <article class="project-card">
                    <h3>E-Kutubxona</h3>
                    <p>Elektron kitoblar platformasi interfeysi.</p>
                </article>
            </div>
        </section>
    </main>
</body>
</html>
```

## Tushuntirish va Mantiq:
Portfolio saytining asosiy bo'limlari `<section>` bilan o'raladi (haqimda, ishlar), har bir bajarilgan loyiha esa o'zining sarlavhasi va tavsifiga ega bo'lgan mustaqil `<article>` sifatida shakllantiriladi.

## Ishlash natijasi:
```text
Qora sarlavhali hero qism, uning ostida biografiya va 2 ustunli loyihalar ko'rgazmasi joylashadi.
```

---

# 34-Topshiriq: Onlayn kurs sahifasi semantik bo'limlari
## Topshiriq sharti:
Kurs davomiyligi, narxi, o'quv rejasi (sillabus) va o'qituvchi blokidan iborat o'quv kursi semantikasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>HTML & CSS Professional Kursi</title>
    <style>
        body { font-family: sans-serif; margin: 0; padding: 20px; background: #fafafa; }
        .course-container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }
        .badge { background: #27ae60; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
    </style>
</head>
<body>
    <main class="course-container">
        <header>
            <span class="badge">Yangi</span>
            <h1>HTML & CSS Professional Dasturi</h1>
            <p>Noldan boshlab professional junior frontend darajasigacha.</p>
        </header>
        <section>
            <h2>O'quv dasturi</h2>
            <details>
                <summary>1-Modul: HTML Asoslari va Semantika</summary>
                <p>Teglar, atributlar, qidiruv tizimlari va to'g'ri tuzilma.</p>
            </details>
            <details>
                <summary>2-Modul: CSS3 va Flexbox/Grid</summary>
                <p>Zamonaviy joylashtirish, stillash va responsivlik.</p>
            </details>
        </section>
    </main>
</body>
</html>
```

## Tushuntirish va Mantiq:
Kurs kartochkasi ichidagi `<header>` kirish ma'lumotlarini taqdim etadi, o'quv dasturi esa `<section>` ichida yig'ilib, modullar `<details>` orqali foydalanuvchiga interaktiv ochilish imkonini beradi.

## Ishlash natijasi:
```text
Oq kartochka ichida kurs nomi, yashil yorliq, kurs tavsifi va ochilib-yopiluvchi modullar mundarijasi ko'rinadi.
```

---

# 35-Topshiriq: Qonuniy hujjat (Foydalanish shartlari) hujjati
## Topshiriq sharti:
Raqamlangan qoidalar, bo'limlar va yuridik ma'lumotlarni o'z ichiga olgan hujjat semantikasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Foydalanish Shartlari</title>
    <style>
        body { font-family: Georgia, serif; line-height: 1.8; max-width: 750px; margin: 40px auto; padding: 0 20px; }
        header { border-bottom: 1px solid #ccc; margin-bottom: 30px; }
        section { margin-bottom: 25px; }
    </style>
</head>
<body>
    <article>
        <header>
            <h1>Saytdan Foydalanish Qoidalari va Shartlari</h1>
            <p><small>Oxirgi yangilanish: <time datetime="2026-01-15">2026-yil 15-yanvar</time></small></p>
        </header>
        <section>
            <h2>1. Umumiy qoidalar</h2>
            <p>Ushbu platformadan foydalanish orqali siz barcha qonuniy talablarga rozilik bildirasiz.</p>
        </section>
        <section>
            <h2>2. Mualliflik huquqlari</h2>
            <p>Saytdagi barcha materiallar intellektual mulk to'g'risidagi qonunchilik bilan himoyalanadi.</p>
        </section>
    </article>
</body>
</html>
```

## Tushuntirish va Mantiq:
Yuridik hujjatlar alohida butun hujjat hisoblangani sababli `<article>` tegi bilan o'raladi. Vaqt `<time>` tegi bilan belgilanadi, har bir moddiy qism esa o'z sarlavhasiga ega `<section>` lar orqali ifodalanadi.

## Ishlash natijasi:
```text
Rasmiy qog'oz formatidagi, chiroyli serif shriftida yozilgan moddalar va yangilanish sanasiga ega yuridik hujjat paydo bo'ladi.
```

---

# 36-Topshiriq: Kompaniya 'Biz haqimizda' semantik sahifasi
## Topshiriq sharti:
Missiya, qadriyatlar va jamoani ifodalovchi korporativ sahifa bo'limlari.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Biz haqimizda</title>
    <style>
        body { font-family: sans-serif; margin: 0; padding: 30px; background: #fdfdfd; }
        .about-wrap { max-width: 800px; margin: 0 auto; }
        .grid-values { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .val-box { background: #f1f3f5; padding: 15px; border-radius: 6px; }
    </style>
</head>
<body>
    <main class="about-wrap">
        <h1>Bizning Kompaniya</h1>
        <section id="mission">
            <h2>Bizning Missiyamiz</h2>
            <p>O'zbekistonda raqamli iqtisodiyotni rivojlantirish va biznes jarayonlarini avtomatlashtirish.</p>
        </section>
        <section id="values">
            <h2>Qadriyatlarimiz</h2>
            <div class="grid-values">
                <div class="val-box">
                    <h3>Shaffoflik</h3>
                    <p>Mijozlarimiz bilan halol va ochiq munosabat.</p>
                </div>
                <div class="val-box">
                    <h3>Innovatsiya</h3>
                    <p>Har bir loyihada eng so'nggi texnologiyalar.</p>
                </div>
            </div>
        </section>
    </main>
</body>
</html>
```

## Tushuntirish va Mantiq:
Kompaniya taqdimoti sahifasida missiya va qadriyatlar har biri alohida semantik `<section>` ga ajratilgan bo'lib, o'quvchi va robotlar uchun mantiqiy tartib yaratadi.

## Ishlash natijasi:
```text
Kompaniya missiyasi matni va pastida ikki ustunli qadriyatlar katakchalari joylashgan toza sahifa.
```

---

# 37-Topshiriq: Voqealar va tadbirlar (Event) semantikasi
## Topshiriq sharti:
Tadbir sanasi, o'tkazilish joyi va dasturini ifodalovchi semantik blok.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Tadbir Dasturi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .event-card { border: 2px solid #3498db; border-radius: 8px; padding: 20px; max-width: 500px; }
        .date-box { color: #e74c3c; font-weight: bold; }
    </style>
</head>
<body>
    <article class="event-card">
        <h2>Toshkent Dasturchilar Xakatoni 2026</h2>
        <p class="date-box">Sana: <time datetime="2026-10-10">10-Oktabr, 2026</time></p>
        <p>Manzil: <address style="display:inline;">IT Park binosi, Toshkent</address></p>
        <p>Eng iqtidorli jamoalar uchun 100 mln so'mlik sovrin jamg'armasi.</p>
    </article>
</body>
</html>
```

## Tushuntirish va Mantiq:
Tadbir kartochkasi mustaqil `<article>` hisoblanadi. Vaqt `<time>` tegi, o'tkazilish joyi esa `<address>` tegi orqali berilib, brauzerga axborotning aniq tabiatini bildiradi.

## Ishlash natijasi:
```text
Moviy hoshiyali kartochkada qizil sana bilan ajratilgan xakaton e'loni ko'rinadi.
```

---

# 38-Topshiriq: Restoran taomnoma sahifasi semantikasi
## Topshiriq sharti:
Taomlar ro'yxati, tarkibi va narxlarini to'g'ri semantika bilan taqdim etish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Restoran Taomnomasi</title>
    <style>
        body { font-family: Georgia, serif; max-width: 600px; margin: 20px auto; padding: 20px; }
        .menu-item { display: flex; justify-content: space-between; border-bottom: 1px dotted #888; padding: 10px 0; }
        .desc { font-size: 13px; color: #666; font-style: italic; }
    </style>
</head>
<body>
    <main>
        <h1>Milliy Taomlar Menusi</h1>
        <section>
            <h2>Asosiy Taomlar</h2>
            <article class="menu-item">
                <div>
                    <strong>Toshkentcha To'y Oshi</strong>
                    <div class="desc">Lazer guruchi, mol go'shti, sariq sabzi, bedana tuxumi</div>
                </div>
                <div>45 000 so'm</div>
            </article>
            <article class="menu-item">
                <div>
                    <strong>Gijduvon Shashlik</strong>
                    <div class="desc">Mayin mol go'shti, ziravorlar</div>
                </div>
                <div>18 000 so'm</div>
            </article>
        </section>
    </main>
</body>
</html>
```

## Tushuntirish va Mantiq:
Har bir taom o'zining narxi va tarkibiga ega mustaqil obyekt bo'lgani uchun `<article>` tegi bilan ifodalanadi, barcha asosiy taomlar esa bitta `<section>` ichiga jamlanadi.

## Ishlash natijasi:
```text
Restoran menyusi formatidagi nuqtali chiziqlar bilan narxlari ko'rsatilgan mazali milliy taomlar ro'yxati chiqadi.
```

---

# 39-Topshiriq: FAQ (Ko'p beriladigan savollar) semantikasi
## Topshiriq sharti:
Foydalanuvchilarni qiziqtiruvchi tez-tez beriladigan savollar bo'limining toza semantik tuzilishi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>FAQ Bo'limi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; max-width: 650px; margin: 0 auto; }
        details { border: 1px solid #ddd; border-radius: 4px; margin-bottom: 8px; padding: 12px; }
        summary { font-weight: 600; cursor: pointer; }
    </style>
</head>
<body>
    <section>
        <h2>Ko'p So'raladigan Savollar (FAQ)</h2>
        <details>
            <summary>Kursni tamomlagach sertifikat beriladimi?</summary>
            <p>Ha, yakuniy amaliy imtihonni muvaffaqiyatli topshirgan barcha talabalarga maxsus QR-kodli elektron sertifikat taqdim etiladi.</p>
        </details>
        <details>
            <summary>Darslar qaysi tilda olib boriladi?</summary>
            <p>Barcha darslar to'liq o'zbek tilida, tushunarli va amaliy misollar bilan o'tiladi.</p>
        </details>
    </section>
</body>
</html>
```

## Tushuntirish va Mantiq:
FAQ bo'limi umumiy tematik bo'lim sifatida `<section>` ga olinadi, har bir savol esa `<details>` va `<summary>` juftligi orqali to'liq semantik va qulay interaktiv tarzda beriladi.

## Ishlash natijasi:
```text
Ustiga bosilganda javobi ochiladigan chiroyli savol-javoblar bloklari ko'rinadi.
```

---

# 40-Topshiriq: Ilmiy dissertatsiya yoki maqola semantik arxitekturasi
## Topshiriq sharti:
Annotatsiya, kalit so'zlar, kirish, tahlil va xulosa qismlarini o'z ichiga oluvchi ilmiy maqola strukturasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Ilmiy Maqola</title>
    <style>
        body { font-family: 'Times New Roman', Times, serif; line-height: 1.8; max-width: 750px; margin: 30px auto; padding: 0 20px; }
        .abstract { background: #f8f9fa; padding: 15px; border-left: 3px solid #333; font-style: italic; }
    </style>
</head>
<body>
    <article>
        <header>
            <h1>O'zbek Tilidagi Katta Til Modellarini O'qitish Usullari</h1>
            <p><strong>Muallif:</strong> Prof. A. Qodirov</p>
        </header>
        <div class="abstract">
            <strong>Annotatsiya:</strong> Ushbu maqolada o'zbek tili korpusi asosida sun'iy intellekt modellarini tokenizatsiya qilish muammolari ko'rib chiqiladi.
        </div>
        <section>
            <h2>1. Kirish</h2>
            <p>Tabiiy tilni qayta ishlash (NLP) zamonaviy texnologiyalarning eng tez o'sayotgan yo'nalishlaridan biridir.</p>
        </section>
    </article>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ilmiy maqola butunligicha `<article>` da joylashadi, uning nomi va muallifi `<header>` da, annotatsiya qismi alohida izoh sifatida, har bir bob esa `<section>` orqali ifodalanadi.

## Ishlash natijasi:
```text
Times New Roman shriftida akademik ilmiy maqola formati gavdalanadi.
```

---

# 41-Topshiriq: ARIA `role` atributlari bilan semantikani boyitish
## Topshiriq sharti:
Eski yoki maxsus elementlarga qo'shimcha qulaylik (accessibility) taqdim etuvchi ARIA rollarini qo'shish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>ARIA Rollari</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .custom-button { display: inline-block; padding: 10px 20px; background: #28a745; color: white; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <div role="button" tabindex="0" class="custom-button" onclick="alert('Bajarildi!')">
        Maxsus Tugma
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Agar semantik teg o'rniga boshqa element ishlatilsa, `role='button'` va `tabindex='0'` orqali ekran o'quvchi qurilmalarga ushbu elementning tugma ekanligi va klaviatura bilan boshqarilishi mumkinligi bildiriladi.

## Ishlash natijasi:
```text
Yashil tugma ko'rinishidagi element chiqadi, ustiga bosilganda xabar paydo bo'ladi.
```

---

# 42-Topshiriq: role='banner' va <header> o'zaro bog'liqligi
## Topshiriq sharti:
Sahifaning eng yuqori asosiy brend qismini ARIA mezonlari bo'yicha belgilash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Banner Roli</title>
    <style>
        header { background: #2c3e50; color: white; padding: 15px; }
    </style>
</head>
<body>
    <header role="banner">
        <h1>Milliy Portal</h1>
    </header>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<header>` tegi sahifaning eng yuqori qismida turganda sukut bo'yicha `role='banner'` vazifasini bajaradi. U ekranni ovozli o'quvchi dasturlarga sahifaning asosiy sarlavha paneli ekanini aytadi.

## Ishlash natijasi:
```text
To'q moviy rangli tasmada yirik oq harflarda 'Milliy Portal' sarlavhasi aks etadi.
```

---

# 43-Topshiriq: role='navigation' va <nav> mosligi
## Topshiriq sharti:
Ekran o'quvchilar menyularni tez topishi uchun `role='navigation'` ni qo'llash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Navigation Roli</title>
    <style>
        nav ul { display: flex; gap: 15px; list-style: none; padding: 0; }
        nav a { text-decoration: none; color: #007bff; font-weight: bold; }
    </style>
</head>
<body>
    <nav role="navigation" aria-label="Asosiy menyu">
        <ul>
            <li><a href="#">Bosh sahifa</a></li>
            <li><a href="#">Xizmatlar</a></li>
        </ul>
    </nav>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<nav>` tegi tabiiy ravishda navigation roliga ega, ammo unga `aria-label='Asosiy menyu'` qo'shilsa, ko'zi ojiz foydalanuvchilar bir nechta menyular orasidan aynan asosiy menyuni oson topishadi.

## Ishlash natijasi:
```text
Ko'k rangli havolalardan iborat gorizontal toza menyu chiziladi.
```

---

# 44-Topshiriq: role='main' va <main> munosabati
## Topshiriq sharti:
Asosiy kontent maydonini ekran o'quvchilar bir tugma bilan ochishi uchun semantik ta'minlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Main Roli</title>
    <style>
        main { padding: 20px; background: #fff; border: 1px solid #eee; }
    </style>
</head>
<body>
    <main role="main">
        <h2>Asosiy Kontent Bo'limi</h2>
        <p>Ekran o'quvchi dasturlar to'g'ridan-to'g'ri ushbu blokga sakrab o'tish imkoniyatiga ega.</p>
    </main>
</body>
</html>
```

## Tushuntirish va Mantiq:
`role='main'` sahifaning asosiy tanasini aniqlaydi. Zamonaviy HTML5 da `<main>` tegining o'zi kifoya, biroq eski brauzerlar va maxsus o'quvchi dasturlar uchun eksplitsit rol qo'shish qulaylikni oshiradi.

## Ishlash natijasi:
```text
Oq fonli toza blok ichida asosiy kontent ko'rinadi.
```

---

# 45-Topshiriq: role='contentinfo' va <footer> bog'liqligi
## Topshiriq sharti:
Podval qismini qidiruv va ovozli o'quvchi vositalar uchun xabardor qiluvchi rol.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Contentinfo Roli</title>
    <style>
        footer { background: #333; color: white; padding: 15px; text-align: center; }
    </style>
</head>
<body>
    <footer role="contentinfo">
        <p>&copy; 2026 Barcha huquqlar himoyalangan.</p>
    </footer>
</body>
</html>
```

## Tushuntirish va Mantiq:
`role='contentinfo'` atributi sahifa haqidagi ma'lumotlar (mualliflik, maxfiylik bayonoti) saqlanadigan qismini belgilaydi va bu bevosita `<footer>` ga mos keladi.

## Ishlash natijasi:
```text
To'q qora fonga ega ixcham podval matni aks etadi.
```

---

# 46-Topshiriq: role='complementary' va <aside>
## Topshiriq sharti:
Qo'shimcha kontentni yordamchi vositalar uchun qulay formatlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Complementary Roli</title>
    <style>
        aside { background: #fff3cd; border: 1px solid #ffeeba; padding: 15px; border-radius: 4px; }
    </style>
</head>
<body>
    <aside role="complementary" aria-label="Valyuta kurslari">
        <h4>Valyuta Kurslari</h4>
        <p>1 USD = 12 800 UZS</p>
    </aside>
</body>
</html>
```

## Tushuntirish va Mantiq:
`role='complementary'` asosiy mavzuni to'ldiruvchi, biroq alohida ham ma'noga ega bo'lgan blokni bildiradi (ob-havo, valyuta kurslari, yangiliklar tasmallari).

## Ishlash natijasi:
```text
Och sariq fonda valyuta kurslari haqidagi ma'lumot qutisi paydo bo'ladi.
```

---

# 47-Topshiriq: aria-label va aria-labelledby semantik nomlash
## Topshiriq sharti:
Ekranda matnsiz, faqat piktogramma bilan ifodalangan tugmalarga tushunarli semantik nom berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Aria Label Namoyishi</title>
    <style>
        .icon-btn { background: #e74c3c; color: white; border: none; width: 40px; height: 40px; border-radius: 50%; cursor: pointer; font-size: 18px; }
    </style>
</head>
<body>
    <button class="icon-btn" aria-label="Xabarni o'chirish">
        &times;
    </button>
</body>
</html>
```

## Tushuntirish va Mantiq:
`aria-label` atributi ekranda faqat belgi (masalan 'x' yoki lupaning rasmi) bo'lgan elementlarga ekran o'quvchilari uchun aniq matnli nom (masalan 'Xabarni o'chirish') biriktirish imkonini beradi.

## Ishlash natijasi:
```text
Qizil dumaloq tugma ichida oq xochi belgisi ko'rinadi; ovozli o'quvchi esa uni 'Xabarni o'chirish tugmasi' deb o'qiydi.
```

---

# 48-Topshiriq: HTML hujjati iyerarxiyasi (Document Outline)
## Topshiriq sharti:
H1 dan H6 gacha bo'lgan sarlavhalarning mantiqiy to'g'ri joylashuv tartibini qurish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Document Outline</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .level-1 { margin-left: 0; }
        .level-2 { margin-left: 20px; color: #2c3e50; }
        .level-3 { margin-left: 40px; color: #7f8c8d; }
    </style>
</head>
<body>
    <h1 class="level-1">Web Dasturlash Entsiklopediyasi</h1>
    <h2 class="level-2">1-Bob: HTML Tili</h2>
    <h3 class="level-3">1.1. Semantik Teglar</h3>
    <h3 class="level-3">1.2. ARIA Standartlari</h3>
    <h2 class="level-2">2-Bob: CSS Stillari</h2>
</body>
</html>
```

## Tushuntirish va Mantiq:
To'g'ri hujjat strukturasi har doim yagona `<h1>` bilan boshlanib, uning ichki qismlari tartib bilan `<h2>`, `<h3>` ko'rinishida davom etishi shart. Bosqichlarni tashlab o'tish (h1 dan birdan h4 ga o'tish) tavsiya etilmaydi.

## Ishlash natijasi:
```text
Iyerarxik ravishda surilgan boblar va kichik bandlar sarlavhalari daraxtsimon ko'rinishda aks etadi.
```

---

# 49-Topshiriq: HTML validatsiyasi (W3C standarti talablari)
## Topshiriq sharti:
Teglarning to'g'ri yopilishi, atributlar sintaksisi va xatolarsiz toza HTML yozish madaniyati.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>W3C Toza Kod Standarti</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .valid-box { border: 2px solid #27ae60; background: #eafaf1; padding: 15px; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="valid-box">
        <h3>Validatsiya talablari:</h3>
        <p>Barcha teglar to'g'ri yopilgan, atributlar qo'shtirnoqqa olingan va DOCTYPE ko'rsatilgan.</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
W3C validatsiyasi veb-sahifaning barcha brauzerlarda bir xil va xatosiz ishlashini ta'minlaydi. Ochiq qolgan teglar, noto'g'ri o'ralgan elementlar sahifaning kutilmagan buzilishlariga sabab bo'ladi.

## Ishlash natijasi:
```text
Yashil hoshiyali va toza matnli muvaffaqiyat bloki ko'rinadi.
```

---

# 50-Topshiriq: To'liq professional HTML5 semantik veb-sahifa andozasi
## Topshiriq sharti:
Barcha o'rganilgan semantik teglarni jamlagan tayyor, ishlab chiqarishga (production) mos korporativ veb-sayt shabloni.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Zamonaviy axborot texnologiyalari markazi rasmiy veb-sayti.">
    <title>Milliy Texnologiyalar Markazi</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', sans-serif; line-height: 1.6; color: #333; background: #f4f6f8; }
        header { background: #0f172a; color: white; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; }
        nav ul { display: flex; list-style: none; gap: 1.5rem; }
        nav a { color: #94a3b8; text-decoration: none; font-weight: 500; }
        nav a:hover { color: white; }
        .container { display: flex; max-width: 1200px; margin: 2rem auto; gap: 2rem; padding: 0 1rem; }
        main { flex: 3; }
        article { background: white; padding: 2rem; border-radius: 8px; margin-bottom: 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        aside { flex: 1; background: white; padding: 1.5rem; border-radius: 8px; height: fit-content; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        footer { background: #0f172a; color: #94a3b8; text-align: center; padding: 1.5rem; margin-top: 2rem; }
    </style>
</head>
<body>
    <header role="banner">
        <h2>TexnoMarkaz</h2>
        <nav role="navigation" aria-label="Asosiy">
            <ul>
                <li><a href="#home">Asosiy</a></li>
                <li><a href="#news">Yangiliklar</a></li>
                <li><a href="#contact">Aloqa</a></li>
            </ul>
        </nav>
    </header>

    <div class="container">
        <main role="main">
            <article>
                <header>
                    <h1>2026-yilda Veb Texnologiyalar Rivoji</h1>
                    <p><small>Chop etildi: <time datetime="2026-05-18">18-May, 2026</time></small></p>
                </header>
                <p>Veb standartlari va semantik arxitektura qidiruv tizimlari va qulaylik (accessibility) uchun birlamchi mezon bo'lib qolmoqda.</p>
            </article>
        </main>
        <aside role="complementary">
            <h3>E'lonlar</h3>
            <p>Yangi kurslarimizga qabul boshlandi.</p>
        </aside>
    </div>

    <footer role="contentinfo">
        <p>&copy; 2026 Milliy Texnologiyalar Markazi. Barcha huquqlar himoyalangan.</p>
    </footer>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu to'liq andoza HTML5 semantikasi va ARIA standartlarining eng yuqori darajasini namoyish etadi: to'g'ri DOCTYPE, meta teglar, header, nav, main, article, aside va footer bloklari to'liq qamrab olingan.

## Ishlash natijasi:
```text
Zamonaviy korporativ veb-sayt: qora tepa navigatsiya paneli, o'rtada keng oq maqola bloki, o'ng tomonda e'lonlar yon paneli va pastda toza podval joylashgan to'liq interfeys.
```

---

