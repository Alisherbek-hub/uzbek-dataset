# Formalar va Input Turlari (251-300)

# 251-Topshiriq: <form> tegi, action va method atributlari
## Topshiriq sharti:
Foydalanuvchi ma'lumotlarini serverga uzatuvchi asosiy formani shakllantiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Form Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        form { background: #f8fafc; border: 1px solid #e2e8f0; padding: 20px; border-radius: 8px; max-width: 400px; }
    </style>
</head>
<body>
    <form action="/server-qabul" method="POST">
        <p>Ma'lumotlar serverga xavfsiz POST usulida jo'natiladi.</p>
        <button type="submit">Yuborish</button>
    </form>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<form>` tegi barcha interaktiv kiritish elementlarini o'rab turadi. `action` ma'lumotlar qaysi manzilga (URL) borishini ko'rsatadi. `method='POST'` maxfiy ma'lumotlar (parollar, shaxsiy fayllar) uchun, `method='GET'` esa qidiruv kabi URL satrida ko'rinadigan so'rovlar uchun ishlatiladi.

## Ishlash natijasi:
```text
Kulrang hoshiyali blok ichida tushuntirish va 'Yuborish' tugmasi ko'rinadi.
```

---

# 252-Topshiriq: <label> tegi va uning for atributi
## Topshiriq sharti:
Input nomini uning maydoni bilan bog'lab bosish maydonini kengaytirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Label Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        label { display: block; margin-bottom: 6px; font-weight: 500; cursor: pointer; }
        input { padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 4px; width: 250px; }
    </style>
</head>
<body>
    <label for="username">Foydalanuvchi nomi:</label>
    <input type="text" id="username" name="username">
</body>
</html>
```

## Tushuntirish va Mantiq:
`<label for='ID'>` va `<input id='ID'>` bir xil nom bilan bog'lanadi. Natijada foydalanuvchi matn ustiga bosganda ham kursor avtomatik ravishda input ichiga tushadi.

## Ishlash natijasi:
```text
Matn ustiga bosilganda kursor to'g'ridan-to'g'ri o'ngdagi katakka o'tadi.
```

---

# 253-Topshiriq: <input type='text'>, placeholder va maxlength
## Topshiriq sharti:
Oddiy matn kiritish maydoni va uning ko'rsatma hamda chegara atributlari.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Text Input</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        input { padding: 10px; border: 1px solid #94a3b8; border-radius: 6px; width: 280px; font-size: 15px; }
    </style>
</head>
<body>
    <input type="text" placeholder="Ismingizni kiriting..." maxlength="30" value="Sanjarbek">
</body>
</html>
```

## Tushuntirish va Mantiq:
`placeholder` bo'sh katakda ko'rinib turuvchi xira maslahat matni. `maxlength='30'` belgilar sonini 30 tadan oshirmaydi. `value` esa boshlang'ich kiritilgan qiymatni belgilaydi.

## Ishlash natijasi:
```text
Ichida 'Sanjarbek' matni yozilgan, 30 belgidan oshirib bo'lmaydigan qulay katakcha chiqadi.
```

---

# 254-Topshiriq: <input type='password'> xavfsiz kiritish
## Topshiriq sharti:
Belgilarni nuqtalar orqali yashiruvchi parol maydoni.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Password Input</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        input { padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px; width: 250px; }
    </style>
</head>
<body>
    <label for="pwd">Maxfiy parol:</label><br>
    <input type="password" id="pwd" name="password" placeholder="Parol...">
</body>
</html>
```

## Tushuntirish va Mantiq:
`type='password'` foydalanuvchi klaviaturadan kiritayotgan harflarni qora doirachalar yoki yulduzchalar ko'rinishida niqoblab begona ko'zlardan himoya qiladi.

## Ishlash natijasi:
```text
Kiritilgan harflar o'rnida qora yashirin nuqtalar paydo bo'ladi.
```

---

# 255-Topshiriq: <input type='email'> avtomatik tekshiruvi
## Topshiriq sharti:
Brauzer darajasida @ belgisi va domen borligini tekshirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Email Input</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        input { padding: 8px 12px; border: 1px solid #64748b; border-radius: 4px; }
    </style>
</head>
<body>
    <form>
        <label for="user-email">Email:</label>
        <input type="email" id="user-email" required placeholder="nomi@domen.uz">
        <button type="submit">Tasdiqlash</button>
    </form>
</body>
</html>
```

## Tushuntirish va Mantiq:
`type='email'` maydoni mobil klaviaturalarda avtomatik ravishda `@` va `.com` tugmalarini chiqarib beradi va shakl yuborilganda xato format bo'lsa ogohlantiradi.

## Ishlash natijasi:
```text
Xato email kiritib tugma bosilganda brauzer 'Email manzilida @ belgisi bo'lishi shart' deb ogohlantiradi.
```

---

# 256-Topshiriq: <input type='number'>, min, max, step
## Topshiriq sharti:
Faqat raqam kiritiladigan va qadami cheklangan maydon.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Number Input</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        input { padding: 8px; width: 120px; font-size: 16px; }
    </style>
</head>
<body>
    <label for="age">Yoshingiz (18 dan 60 gacha):</label><br>
    <input type="number" id="age" min="18" max="60" step="1" value="25">
</body>
</html>
```

## Tushuntirish va Mantiq:
`min` eng kichik, `max` eng katta chegarani beradi, `step` esa o'ngdagi strelkalar bosilganda son nechtaga o'zgarishini belgilaydi.

## Ishlash natijasi:
```text
O'ng tomonida sonni oshirish/kamaytirish strelkalari bor raqamli katakcha chiqadi.
```

---

# 257-Topshiriq: <input type='tel'> telefon kiritish
## Topshiriq sharti:
Smartfonlarda raqamli klaviaturani chaqiruvchi telefon maydoni.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Tel Input</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        input { padding: 10px; width: 220px; border-radius: 6px; border: 1px solid #cbd5e1; }
    </style>
</head>
<body>
    <label for="phone">Telefon raqam:</label><br>
    <input type="tel" id="phone" placeholder="+998 (__) ___-__-__">
</body>
</html>
```

## Tushuntirish va Mantiq:
`type='tel'` mobil qurilmalarda harfli klaviatura o'rniga qulay telefon raqamlarini terish panelini ochadi.

## Ishlash natijasi:
```text
O'zbekiston formati ko'rsatmasi bo'lgan telefon katakchasi ko'rinadi.
```

---

# 258-Topshiriq: <input type='url'> veb-manzil kiritish
## Topshiriq sharti:
To'g'ri internet havolasini talab qiluvchi maydon.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>URL Input</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        input { padding: 8px 12px; width: 280px; }
    </style>
</head>
<body>
    <form>
        <label for="site">Shaxsiy veb-saytingiz:</label><br>
        <input type="url" id="site" placeholder="https://dasturchi.uz" required>
        <button type="submit">Yuborish</button>
    </form>
</body>
</html>
```

## Tushuntirish va Mantiq:
`type='url'` foydalanuvchidan `http://` yoki `https://` bilan boshlanuvchi to'g'ri manzil kiritishni talab qiladi.

## Ishlash natijasi:
```text
Noto'g'ri manzil yozilganda brauzer manzil protokolini to'g'rilashni so'raydi.
```

---

# 259-Topshiriq: <input type='search'> qidiruv maydoni
## Topshiriq sharti:
Matn kiritilganda o'ng tomonida 'x' tozalash tugmasi chiqadigan maydon.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Search Input</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        input { padding: 8px 14px; border-radius: 20px; border: 1px solid #94a3b8; width: 260px; }
    </style>
</head>
<body>
    <input type="search" placeholder="Sayt bo'yicha qidiruv...">
</body>
</html>
```

## Tushuntirish va Mantiq:
`type='search'` qidiruv uchun ixtisoslashgan bo'lib, foydalanuvchi matn yozishi bilanoq uni bitta bosishda o'chiruvchi krestik tugmachasini ko'rsatadi.

## Ishlash natijasi:
```text
Dumaloq burchakli qidiruv katakchasi; matn yozilsa o'ngida tozalash belgisi paydo bo'ladi.
```

---

# 260-Topshiriq: <input type='date'> sana tanlash kalendari
## Topshiriq sharti:
Brauzerning interaktiv taqvimidan kun, oy va yilni tanlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Date Input</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        input { padding: 8px; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 15px; }
    </style>
</head>
<body>
    <label for="bday">Tug'ilgan sana:</label><br>
    <input type="date" id="bday" min="1950-01-01" max="2026-12-31">
</body>
</html>
```

## Tushuntirish va Mantiq:
`type='date'` bosilganda to'laqonli vizual taqvim oynasini ochadi va sanani xatosiz tanlashni ta'minlaydi.

## Ishlash natijasi:
```text
Katak chetida kalendar belgisi turadi; bosilganda sana tanlash taqvimi ochiladi.
```

---

# 261-Topshiriq: <input type='time'> vaqt tanlash
## Topshiriq sharti:
Soat va daqiqani kiritish maydoni.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Time Input</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        input { padding: 8px 12px; font-size: 16px; }
    </style>
</head>
<body>
    <label for="meet">Uchrashuv vaqti:</label><br>
    <input type="time" id="meet" value="14:30">
</body>
</html>
```

## Tushuntirish va Mantiq:
`type='time'` soat va daqiqalarni boshqarish vositasini ekranga chiqaradi.

## Ishlash natijasi:
```text
Ichida '14:30' soati turgan vaqt sozlash darchasi chiqadi.
```

---

# 262-Topshiriq: <input type='datetime-local'> sana va vaqt birga
## Topshiriq sharti:
Reys, bron yoki tadbir uchun sana va soatni yagona katakda kiritish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>DateTime Local</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        input { padding: 8px; }
    </style>
</head>
<body>
    <label for="event">Tadbir boshlanishi:</label><br>
    <input type="datetime-local" id="event" name="event-time">
</body>
</html>
```

## Tushuntirish va Mantiq:
Foydalanuvchining mahalliy vaqt mintaqasi (timezone) bo'yicha sana va aniq soatni birgalikda tanlatadi.

## Ishlash natijasi:
```text
Ham sana, ham soat/daqiqa ko'rsatilgan birlashgan kiritish katagi chiqadi.
```

---

# 263-Topshiriq: <input type='month'> va <input type='week'>
## Topshiriq sharti:
Faqat oyni yoki yilning nechanchi haftasini tanlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Month va Week</title>
    <style>
        body { font-family: sans-serif; padding: 25px; line-height: 2; }
    </style>
</head>
<body>
    <label>Oyni tanlang: <input type="month"></label><br>
    <label>Haftani tanlang: <input type="week"></label>
</body>
</html>
```

## Tushuntirish va Mantiq:
`month` faqat yil va oyni (masalan 2026-iyun), `week` esa yilning haftasini (masalan 2026-yil 24-hafta) tanlaydi.

## Ishlash natijasi:
```text
Oy va hafta bo'yicha hisobot topshirish uchun qulay ikkita tanlash darchasi chiqadi.
```

---

# 264-Topshiriq: <input type='color'> rang tanlash palitrasi
## Topshiriq sharti:
HEX rang kodini grafik palitra orqali tanlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Color Input</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        input[type="color"] { border: none; width: 50px; height: 50px; border-radius: 50%; cursor: pointer; }
    </style>
</head>
<body>
    <label for="favcolor">Sayt foni rangini tanlang:</label><br>
    <input type="color" id="favcolor" value="#3b82f6">
</body>
</html>
```

## Tushuntirish va Mantiq:
`type='color'` bosilganda operatsion tizimning to'liq ranglar spektrini (Color Picker) ochadi va tanlangan rangning `#rrggbb` kodini qiymat sifatida saqlaydi.

## Ishlash natijasi:
```text
Dumaloq ko'k rangli tugmacha; bosilganda millionlab ranglar palitrasi ochiladi.
```

---

# 265-Topshiriq: <input type='range'> suriluvchi slayder (Slider)
## Topshiriq sharti:
Hajm, narx yoki ovozni qulay surish orqali sozlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Range Input</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        input[type="range"] { width: 300px; }
    </style>
</head>
<body>
    <label for="vol">Ovoz balandligi (0-100%):</label><br>
    <input type="range" id="vol" min="0" max="100" value="70">
</body>
</html>
```

## Tushuntirish va Mantiq:
`type='range'` sonli qiymatni aniq yozib o'tirmasdan vizual 'polzunok' orqali tanlash imkonini beradi.

## Ishlash natijasi:
```text
Gorizontal suriluvchi chiziq va uning ustida yumaloq slayder darchasi paydo bo'ladi.
```

---

# 266-Topshiriq: <input type='file'> va accept atributi
## Topshiriq sharti:
Kompyuterdan rasm yoki hujjat fayllarini yuklash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>File Input</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
    </style>
</head>
<body>
    <label for="doc">Pasport nusxasini yuklang (faqat PDF yoki rasm):</label><br>
    <input type="file" id="doc" accept=".pdf, image/*">
</body>
</html>
```

## Tushuntirish va Mantiq:
`accept='.pdf, image/*'` foydalanuvchi fayl tanlash darchasini ochganda faqat ruxsat etilgan kengaytmalarni ko'rsatishni filtrlash uchun xizmat qiladi.

## Ishlash natijasi:
```text
'Faylni tanlang' tugmasi va uning yonida 'Fayl tanlanmagan' yozuvi chiqadi.
```

---

# 267-Topshiriq: <input type='file' multiple> ko'p faylli yuklash
## Topshiriq sharti:
Bir vaqtning o'zida bir nechta faylni birdaniga tanlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Multiple File</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
    </style>
</head>
<body>
    <input type="file" multiple accept="image/*">
</body>
</html>
```

## Tushuntirish va Mantiq:
`multiple` mantiqiy atributi foydalanuvchiga Ctrl yoki Shift orqali 5-10 ta rasmni birdaniga belgilash imkonini beradi.

## Ishlash natijasi:
```text
Bir nechta fayllarni qabul qiluvchi yuklash tugmachasi aks etadi.
```

---

# 268-Topshiriq: enctype='multipart/form-data' fayl yuklash standarti
## Topshiriq sharti:
Serverga binar fayllarni xatosiz uzatuvchi majburiy forma shifrlash usuli.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Multipart Form</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
    </style>
</head>
<body>
    <form action="/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="avatar" required><br><br>
        <button type="submit">Serverga Yuklash</button>
    </form>
</body>
</html>
```

## Tushuntirish va Mantiq:
Agar formada fayl yuborilayotgan bo'lsa, `enctype='multipart/form-data'` ko'rsatilishi shart! Aks holda serverga faqat fayl nomi matn bo'lib boradi, faylning o'zi yuklanmaydi.

## Ishlash natijasi:
```text
Fayl tanlash va uni serverga uzatish tugmasi ko'rinadi.
```

---

# 269-Topshiriq: <input type='checkbox'> bayroqchalari
## Topshiriq sharti:
Bir vaqtning o'zida bir nechta mustaqil variantni tanlash imkoniyati.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Checkbox</title>
    <style>
        body { font-family: sans-serif; padding: 25px; line-height: 1.8; }
    </style>
</head>
<body>
    <p>Qaysi chet tillarini bilasiz?</p>
    <label><input type="checkbox" name="lang" value="en" checked> Ingliz tili</label><br>
    <label><input type="checkbox" name="lang" value="ru" checked> Rus tili</label><br>
    <label><input type="checkbox" name="lang" value="de"> Nemis tili</label>
</body>
</html>
```

## Tushuntirish va Mantiq:
`checkbox` mustaqil variantlardir. Foydalanuvchi hammasini tanlashi yoki hech birini tanlamasligi mumkin. `checked` uni oldindan belgilangan qilib qo'yadi.

## Ishlash natijasi:
```text
Ikkita belgilangan va bitta bo'sh kvadrat katakchalar ko'rinadi.
```

---

# 270-Topshiriq: <input type='radio'> va uning name atributi
## Topshiriq sharti:
Guruhdan faqat bitta variantni tanlash sharti.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Radio Tugmalar</title>
    <style>
        body { font-family: sans-serif; padding: 25px; line-height: 1.8; }
    </style>
</head>
<body>
    <p>Yetkazib berish usulini tanlang:</p>
    <label><input type="radio" name="delivery" value="standard" checked> Standart (3 kun) - Bepul</label><br>
    <label><input type="radio" name="delivery" value="express"> Tezkor (1 kun) - 30 000 UZS</label>
</body>
</html>
```

## Tushuntirish va Mantiq:
Radio tugmalarda bitta variant tanlanganda ikkinchisi avtomatik o'chishi uchun ularning barchasida `name='delivery'` atributi bir xil bo'lishi shart!

## Ishlash natijasi:
```text
Dumaloq tanlash tugmalari; biri bosilganda ikkinchisidan belgi o'chadi.
```

---

# 271-Topshiriq: <input type='hidden'> yashirin ma'lumot
## Topshiriq sharti:
Foydalanuvchiga ko'rinmaydigan, lekin serverga kerakli bo'lgan ID yoki tokenni uzatish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Hidden Input</title>
</head>
<body>
    <form action="/buyurtma" method="POST">
        <input type="hidden" name="product_id" value="89421">
        <input type="hidden" name="csrf_token" value="xyz987token">
        <p>Mahsulotni sotib olasizmi?</p>
        <button type="submit">Tasdiqlash</button>
    </form>
</body>
</html>
```

## Tushuntirish va Mantiq:
`type='hidden'` sahifada umuman ko'rinmaydi, lekin forma yuborilganda uning `name` va `value` qiymatlari serverga xavfsiz ma'lumot sifatida ketadi.

## Ishlash natijasi:
```text
Ekranda faqat savol va tugma ko'rinadi, maxfiy ID lar esa kod ichida yashiringan.
```

---

# 272-Topshiriq: <textarea> ko'p qatorli matn maydoni
## Topshiriq sharti:
Fikr-mulohaza, sharh yoki xabarlar yozish uchun keng matn maydoni.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Textarea</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        textarea { padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px; font-family: sans-serif; }
    </style>
</head>
<body>
    <label for="comment">Fikringizni qoldiring:</label><br>
    <textarea id="comment" rows="4" cols="40" placeholder="Taklif va mulohazalaringiz..."></textarea>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<textarea>` bir necha satrli matnlar uchun ishlatiladi. `rows` balandlikdagi satrlar sonini, `cols` esa enidagi belgilar sonini bildiradi.

## Ishlash natijasi:
```text
Keng to'rtburchak matn kiritish darchasi chiqadi.
```

---

# 273-Topshiriq: textarea o'lchamini CSS da boshqarish (resize)
## Topshiriq sharti:
Foydalanuvchi maydonni cho'zganda dizayn buzilib ketishining oldini olish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Textarea Resize</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .fixed-box { resize: none; width: 300px; height: 100px; }
        .vert-box { resize: vertical; width: 300px; min-height: 80px; max-height: 200px; }
    </style>
</head>
<body>
    <p>Cho'zib bo'lmaydigan (resize: none):</p>
    <textarea class="fixed-box"></textarea>
    <p>Faqat pastga cho'ziladigan (resize: vertical):</p>
    <textarea class="vert-box"></textarea>
</body>
</html>
```

## Tushuntirish va Mantiq:
`resize: none` burchakdagi cho'zish uchburchagini yo'qotadi. `resize: vertical` esa faqat bo'yiga cho'zishga ruxsat beradi va yon atrofdagi bloklarni buzilishdan saqlaydi.

## Ishlash natijasi:
```text
Biri qat'iy o'lchamdagi, ikkinchisi faqat pastga cho'ziladigan ikkita matn qutisi chiqadi.
```

---

# 274-Topshiriq: <select> va <option> ochiluvchi ro'yxati
## Topshiriq sharti:
Foydalanuvchiga ro'yxatdan bitta variantni tanlash imkonini beruvchi darcha.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Select Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        select { padding: 8px 12px; border-radius: 6px; border: 1px solid #94a3b8; font-size: 15px; }
    </style>
</head>
<body>
    <label for="city">Shaharni tanlang:</label><br>
    <select id="city" name="city">
        <option value="">-- Tanlang --</option>
        <option value="tashkent" selected>Toshkent</option>
        <option value="samarkand">Samarqand</option>
        <option value="bukhara">Buxoro</option>
    </select>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<select>` konteyner bo'lib, uning ichida bir nechta `<option>` bandlari joylashadi. `selected` sukut bo'yicha tanlangan variantni bildiradi.

## Ishlash natijasi:
```text
Ochiluvchi menyu; bosilganda shahar variantlari ro'yxati chiqadi.
```

---

# 275-Topshiriq: <optgroup> bilan variantlarni guruhlash
## Topshiriq sharti:
Katta ro'yxatdagi variantlarni mantiqiy toifalarga ajratish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Optgroup Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        select { padding: 8px; font-size: 14px; }
    </style>
</head>
<body>
    <select name="car">
        <optgroup label="Elektromobillar">
            <option value="byd">BYD Song Plus</option>
            <option value="tesla">Tesla Model Y</option>
        </optgroup>
        <optgroup label="Benzinli avtomobillar">
            <option value="malibu">Chevrolet Malibu</option>
            <option value="monza">Chevrolet Monza</option>
        </optgroup>
    </select>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<optgroup label='...'>` ro'yxat ichida tanlab bo'lmaydigan qalin toifa sarlavhasini hosil qiladi.

## Ishlash natijasi:
```text
Ikki bo'limga ajratilgan avtomobillar ro'yxati ko'rinadi.
```

---

# 276-Topshiriq: <select multiple> ko'p variantli tanlov
## Topshiriq sharti:
Ctrl tugmasini bosib bir vaqtning o'zida bir nechta bandni tanlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Select Multiple</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        select { width: 220px; padding: 6px; }
    </style>
</head>
<body>
    <label>Qiziqishlaringiz (Ctrl bilan belgilang):</label><br>
    <select multiple size="4">
        <option value="ai">Sun'iy Intellekt</option>
        <option value="web">Web Dasturlash</option>
        <option value="mobile">Mobil Ilovalar</option>
        <option value="cloud">Cloud Tizimlar</option>
    </select>
</body>
</html>
```

## Tushuntirish va Mantiq:
`multiple` atributi va `size='4'` ro'yxatni ochiluvchi emas, to'rtta satri birdaniga ko'rinib turuvchi darchaga aylantiradi.

## Ishlash natijasi:
```text
To'rt qatorli ochiq ro'yxat oynasi ko'rinadi.
```

---

# 277-Topshiriq: <datalist> avtomatik taklif beruvchi aqlli input
## Topshiriq sharti:
Foydalanuvchi yozayotganda variantlarni tavsiya qiluvchi, lekin ixtiyoriy matn yozishga ham imkon beruvchi vosita.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Datalist Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        input { padding: 8px 12px; border-radius: 4px; border: 1px solid #94a3b8; width: 250px; }
    </style>
</head>
<body>
    <label for="browser">Sevimli brauzeringiz:</label><br>
    <input list="browsers" id="browser" placeholder="Tanlang yoki yozing...">
    <datalist id="browsers">
        <option value="Google Chrome">
        <option value="Mozilla Firefox">
        <option value="Apple Safari">
        <option value="Microsoft Edge">
    </datalist>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<input list='ID'>` va `<datalist id='ID'>` kombinatsiyasi qidiruv maslahatlarini (autocomplete) beradi, lekin oddiy selectdan farqli o'laroq, ro'yxatda yo'q so'zni ham yozishga ruxsat etadi.

## Ishlash natijasi:
```text
Harf yozilganda unga mos brauzer nomlari pastida taklif sifatida ochiladi.
```

---

# 278-Topshiriq: <fieldset> va <legend> bilan guruhlash
## Topshiriq sharti:
Katta formalarning qismlarini ramkaga olib estetik sarlavha berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Fieldset va Legend</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        fieldset { border: 2px solid #3b82f6; border-radius: 8px; padding: 15px 20px; max-width: 350px; }
        legend { font-weight: bold; color: #1e40af; padding: 0 8px; }
    </style>
</head>
<body>
    <fieldset>
        <legend>Yetkazib berish manzili</legend>
        <label>Shahar: <input type="text"></label><br><br>
        <label>Ko'cha: <input type="text"></label>
    </fieldset>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<fieldset>` tegishli inputlarni chiroyli ramka ichiga oladi. `<legend>` esa to'g'ridan-to'g'ri ramkaning yuqori chizig'i ustiga chiroyli sarlavha o'rnatadi.

## Ishlash natijasi:
```text
Ko'k ramkali blok va uning chizig'i ustiga qadalgan 'Yetkazib berish manzili' sarlavhasi chiqadi.
```

---

# 279-Topshiriq: <button> turlari: submit, reset, button
## Topshiriq sharti:
Tugmalarning uchta asosiy vazifasini to'g'ri belgilash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Button Turlari</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        button { padding: 8px 16px; border-radius: 4px; cursor: pointer; border: 1px solid #ccc; }
        .sub { background: #2563eb; color: white; border: none; }
        .res { background: #ef4444; color: white; border: none; }
    </style>
</head>
<body>
    <form>
        <input type="text" value="Dastlabki matn"><br><br>
        <button type="submit" class="sub">Yuborish (Submit)</button>
        <button type="reset" class="res">Tozalash (Reset)</button>
        <button type="button" onclick="alert('Salom!')">Oddiy Amal (Button)</button>
    </form>
</body>
</html>
```

## Tushuntirish va Mantiq:
`type='submit'` formani serverga yuboradi, `type='reset'` formadagi barcha kataklarni dastlabki holatiga qaytaradi, `type='button'` esa hech qanday standart harakatsiz faqat JavaScript buyruqlari uchun xizmat qiladi.

## Ishlash natijasi:
```text
Ko'k yuborish, qizil tozalash va kulrang amaliy tugmalar yonma-yon ko'rinadi.
```

---

# 280-Topshiriq: required majburiy to'ldirish atributi
## Topshiriq sharti:
Katak bo'sh qolganda formani yuborishga yo'l qo'ymaslik.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Required Atributi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        input:required { border-left: 4px solid #ef4444; }
    </style>
</head>
<body>
    <form>
        <label>Ismingiz (Majburiy):</label><br>
        <input type="text" required><br><br>
        <button type="submit">Ro'yxatdan o'tish</button>
    </form>
</body>
</html>
```

## Tushuntirish va Mantiq:
`required` mantiqiy atributi brauzerga ushbu maydon to'ldirilmaguncha shaklni yubormaslikni talab qiladi. CSS dagi `:required` selektori bilan unga qizil chegara berish mumkin.

## Ishlash natijasi:
```text
Chap tomonida qizil chizig'i bor katakcha; to'ldirmasdan yuborilganda brauzer to'ldirishni talab qiladi.
```

---

# 281-Topshiriq: pattern atributi va Regular Expression (RegEx)
## Topshiriq sharti:
Input qiymatini qat'iy shablon bo'yicha (masalan, O'zbekiston avtoraqami) tekshirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Pattern RegEx</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        input { padding: 8px; width: 220px; }
    </style>
</head>
<body>
    <form>
        <label>Avtomobil raqami (masalan 01A777AA):</label><br>
        <input type="text" pattern="[0-9]{2}[A-Z]{1}[0-9]{3}[A-Z]{2}"
               title="Format: 01A777AA (2 ta raqam, 1 ta harf, 3 ta raqam, 2 ta harf)" required>
        <button type="submit">Tekshirish</button>
    </form>
</body>
</html>
```

## Tushuntirish va Mantiq:
`pattern` atributiga kiritilgan RegEx shabloni kiritilgan ma'lumotning qat'iy formatga mosligini tekshiradi. `title` atributi esa xato kiritilganda nima xato ekanini tushuntiradi.

## Ishlash natijasi:
```text
Noto'g'ri raqam yozilganda talab qilinayotgan shablon haqida ogohlantirish oynasi chiqadi.
```

---

# 282-Topshiriq: minlength va maxlength belgilar chegaralari
## Topshiriq sharti:
Parol yoki login uzunligining quyi va yuqori chegaralarini qo'yish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Minlength Maxlength</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        input { padding: 8px; width: 250px; }
    </style>
</head>
<body>
    <form>
        <label>Parol (8 dan 16 tagacha belgi):</label><br>
        <input type="password" minlength="8" maxlength="16" required>
        <button type="submit">Saqlash</button>
    </form>
</body>
</html>
```

## Tushuntirish va Mantiq:
`minlength='8'` foydalanuvchining 8 tadan kam belgi kiritishini taqiqlaydi, `maxlength='16'` esa 16 tadan ortiq harf yozishga jismonan yo'l qo'ymaydi.

## Ishlash natijasi:
```text
8 tadan kam belgi kiritilsa brauzer ogohlantiradi, 16 tadan ko'p belgi yozib bo'lmaydi.
```

---

# 283-Topshiriq: disabled va readonly o'rtasidagi farq
## Topshiriq sharti:
Tahrirlab bo'lmaydigan maydonlarning ikki xil tabiati.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Disabled vs Readonly</title>
    <style>
        body { font-family: sans-serif; padding: 25px; line-height: 2; }
        input { padding: 6px 10px; }
    </style>
</head>
<body>
    <!-- Readonly: tahrirlanmaydi, lekin serverga yuboriladi -->
    <label>Readonly: <input type="text" value="ID-1002" readonly></label><br>
    <!-- Disabled: butunlay o'chirilgan, serverga HAM yuborilmaydi -->
    <label>Disabled: <input type="text" value="Bloklangan" disabled></label>
</body>
</html>
```

## Tushuntirish va Mantiq:
`readonly` qiymatni o'zgartirishga yo'l qo'ymaydi, lekin forma yuborilganda uning qiymati serverga ketadi. `disabled` esa maydonni butunlay to'xtatadi va serverga uning ma'lumoti yuborilmaydi.

## Ishlash natijasi:
```text
Birinchi katak oq va nusxa olsa bo'ladi, ikkinchi katak esa xira kulrangda to'liq qotirilgan.
```

---

# 284-Topshiriq: autofocus atributi
## Topshiriq sharti:
Sahifa yuklanganda kursor avtomatik birinchi qatorga tushishi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Autofocus</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        input { padding: 10px; width: 280px; }
    </style>
</head>
<body>
    <input type="text" autofocus placeholder="Kursor darhol shu yerda miltillaydi">
</body>
</html>
```

## Tushuntirish va Mantiq:
`autofocus` foydalanuvchi sichqoncha bilan bosmasdan darhol klaviaturadan yozishni boshlashi uchun kursorni avtomatik faollashtiradi (masalan, Google qidiruv sahifasidagi kabi).

## Ishlash natijasi:
```text
Sahifa ochilishi bilanoq ko'k hoshiyali faol kursor miltillab turadi.
```

---

# 285-Topshiriq: autocomplete atributi va xavfsizlik
## Topshiriq sharti:
Brauzerning avtomatik to'ldirish xotirasini boshqarish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Autocomplete</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
    </style>
</head>
<body>
    <form autocomplete="on">
        <label>Ism: <input type="text" name="name" autocomplete="name"></label><br><br>
        <!-- Bir martalik SMS kod uchun auto-to'ldirishni o'chirish -->
        <label>SMS Kod: <input type="text" name="otp" autocomplete="one-time-code"></label>
    </form>
</body>
</html>
```

## Tushuntirish va Mantiq:
`autocomplete='one-time-code'` telefonga kelgan SMS kodni brauzer darhol bitta bosishda taklif qilishiga yordam beradi. `autocomplete='new-password'` esa eski parollar taklif qilinishining oldini oladi.

## Ishlash natijasi:
```text
Ism qatorida avvalgi ismlar taklifi, SMS qatorida esa xavfsiz kod kiritish oynasi chiqadi.
```

---

# 286-Topshiriq: formnovalidate bilan qoralama saqlash
## Topshiriq sharti:
Majburiy talablarni tekshirmasdan ma'lumotni qoralama (draft) sifatida saqlash tugmasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Form No Validate</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        button { padding: 8px 16px; margin-right: 10px; }
    </style>
</head>
<body>
    <form action="/submit" method="POST">
        <label>Email: <input type="email" required></label><br><br>
        <button type="submit">Rasmiy Yuborish</button>
        <button type="submit" formnovalidate name="draft" value="true">Qoralama sifatida saqlash</button>
    </form>
</body>
</html>
```

## Tushuntirish va Mantiq:
`formnovalidate` atributi tugmaga qo'yiladi va u bosilganda formadagi barcha `required` va `pattern` cheklovlari vaqtincha chetlab o'tiladi.

## Ishlash natijasi:
```text
Katak bo'sh bo'lsa ham 'Qoralama sifatida saqlash' tugmasi xatosiz ishlaydi.
```

---

# 287-Topshiriq: :focus va :focus-visible zamonaviy stillari
## Topshiriq sharti:
Klaviatura foydalanuvchilari uchun chiroyli ko'rsatkich halqasi (focus ring).

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Focus Visible</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        input {
            padding: 10px 14px;
            border: 1px solid #94a3b8;
            border-radius: 6px;
            outline: none;
            transition: all 0.2s;
        }
        input:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25);
        }
    </style>
</head>
<body>
    <input type="text" placeholder="Ustiga bosing...">
</body>
</html>
```

## Tushuntirish va Mantiq:
`outline: none` dan so'ng `box-shadow: 0 0 0 3px ...` orqali zamonaviy Apple va Google interfeyslariga xos mayin nurli chegara hosil qilinadi.

## Ishlash natijasi:
```text
Kursor tushganda katak atrofida havorang mayin nurli halqa taraladi.
```

---

# 288-Topshiriq: :valid va :invalid psevdo-sinflari
## Topshiriq sharti:
To'g'ri kiritilganda yashil, xato kiritilganda qizil hoshiya berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Valid Invalid</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        input { padding: 8px 12px; border: 2px solid #cbd5e1; border-radius: 6px; outline: none; }
        input:focus:invalid { border-color: #ef4444; background-color: #fef2f2; }
        input:focus:valid { border-color: #22c55e; background-color: #f0fdf4; }
    </style>
</head>
<body>
    <label>Email manzil:</label><br>
    <input type="email" required placeholder="nomi@mail.uz">
</body>
</html>
```

## Tushuntirish va Mantiq:
`:invalid` kiritilgan qiymat mezonlarga to'g'ri kelmaganda qizil fon va chegara beradi, to'liq to'g'ri yozilishi bilan `:valid` ishga tushib yashil tusga kiradi.

## Ishlash natijasi:
```text
Harf yozilayotganda qizil bo'lib turadi, '@' va domen qo'shilishi bilanoq yashil tus oladi.
```

---

# 289-Topshiriq: :required va :optional stillash
## Topshiriq sharti:
Majburiy va ixtiyoriy maydonlarni avtomatik farqlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Required Optional</title>
    <style>
        body { font-family: sans-serif; padding: 25px; line-height: 2; }
        input:required { border-left: 3px solid #2563eb; }
        input:optional { border-left: 3px solid #94a3b8; }
    </style>
</head>
<body>
    <label>FIO: <input type="text" required></label><br>
    <label>Veb-sayt: <input type="url"></label>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:required` majburiy kataklarni ko'k chiziq bilan, `:optional` esa ixtiyoriy kataklarni kulrang chiziq bilan avtomatik belgilaydi.

## Ishlash natijasi:
```text
Majburiy maydonda ko'k, ixtiyoriy maydonda esa kulrang chap chiziq ko'rinadi.
```

---

# 290-Topshiriq: :checked selektori bilan dinamik stillash
## Topshiriq sharti:
Tanlangan variantning fonini va matnini o'zgartirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Checked Selektori</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .plan-label {
            display: inline-block;
            padding: 12px 20px;
            border: 2px solid #cbd5e1;
            border-radius: 8px;
            cursor: pointer;
            margin-right: 10px;
        }
        input[type="radio"] { display: none; }
        input[type="radio"]:checked + .plan-label {
            border-color: #2563eb;
            background: #eff6ff;
            color: #1e40af;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <label><input type="radio" name="p" checked><span class="plan-label">Oylik Reja</span></label>
    <label><input type="radio" name="p"><span class="plan-label">Yillik Reja</span></label>
</body>
</html>
```

## Tushuntirish va Mantiq:
Haqiqiy radio tugma `display: none` bilan yashiriladi va `:checked + .plan-label` orqali bosilgan kartochka ko'k hoshiya va fonga ega bo'ladi.

## Ishlash natijasi:
```text
Ikkita tugmasimon kartochka; bosilgani ko'k rangda faol bo'lib ajraladi.
```

---

# 291-Topshiriq: Maxsus moslashtirilgan checkbox (Custom Checkbox)
## Topshiriq sharti:
Standart ko'rimsiz kvadratni zamonaviy gradientli galochkali katakka aylantirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Custom Checkbox</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        .custom-chk { display: flex; align-items: center; gap: 10px; cursor: pointer; }
        .custom-chk input { display: none; }
        .checkmark {
            width: 20px; height: 20px;
            border: 2px solid #94a3b8;
            border-radius: 4px;
            display: flex; align-items: center; justify-content: center;
            transition: all 0.2s;
        }
        .custom-chk input:checked + .checkmark {
            background-color: #2563eb;
            border-color: #2563eb;
        }
        .custom-chk input:checked + .checkmark::after {
            content: "✓";
            color: white;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <label class="custom-chk">
        <input type="checkbox" checked>
        <span class="checkmark"></span>
        <span>Xizmat ko'rsatish shartlariga roziman</span>
    </label>
</body>
</html>
```

## Tushuntirish va Mantiq:
`display: none` qilingan input yonidagi `span.checkmark` orqali to'liq nazorat qilinadigan estetik katakcha yasaladi.

## Ishlash natijasi:
```text
Moviy fonda oq galochka belgisi bilan jihozlangan chiroyli zamonaviy belgilash katakchasi.
```

---

# 292-Topshiriq: Maxsus moslashtirilgan radio tugma (Custom Radio)
## Topshiriq sharti:
Standart nuqtali radio tugmani chiroyli aylanaga aylantirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Custom Radio</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .custom-radio { display: flex; align-items: center; gap: 10px; cursor: pointer; margin-bottom: 10px; }
        .custom-radio input { display: none; }
        .dot {
            width: 20px; height: 20px;
            border: 2px solid #94a3b8;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
        }
        .custom-radio input:checked + .dot {
            border-color: #2563eb;
        }
        .custom-radio input:checked + .dot::after {
            content: '';
            width: 10px; height: 10px;
            background: #2563eb;
            border-radius: 50%;
        }
    </style>
</head>
<body>
    <label class="custom-radio"><input type="radio" name="opt" checked><span class="dot"></span> 1-Tanlov</label>
    <label class="custom-radio"><input type="radio" name="opt"><span class="dot"></span> 2-Tanlov</label>
</body>
</html>
```

## Tushuntirish va Mantiq:
`::after` orqali tanlangan holatda doira markaziga ko'k nuqta joylashtirilib toza radio dizayni yasaladi.

## Ishlash natijasi:
```text
Ko'k hoshiyali va markazida ko'k doirasi bor zamonaviy radio elementlari ko'rinadi.
```

---

# 293-Topshiriq: Zamonaviy almashtiruvchi svitcher (Toggle Switch)
## Topshiriq sharti:
Mobil sozlamalardagi kabi suriluvchi yoqish/o'chirish tugmachasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Toggle Switch</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        .switch { position: relative; display: inline-block; width: 50px; height: 26px; }
        .switch input { opacity: 0; width: 0; height: 0; }
        .slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #cbd5e1; transition: .3s; border-radius: 34px; }
        .slider:before { position: absolute; content: ""; height: 20px; width: 20px; left: 3px; bottom: 3px; background-color: white; transition: .3s; border-radius: 50%; }
        input:checked + .slider { background-color: #10b981; }
        input:checked + .slider:before { transform: translateX(24px); }
    </style>
</head>
<body>
    <label class="switch">
        <input type="checkbox" checked>
        <span class="slider"></span>
    </label>
    <span style="margin-left: 10px; vertical-align: super;">Bildirishnomalarni yoqish</span>
</body>
</html>
```

## Tushuntirish va Mantiq:
`transform: translateX(24px)` va `transition: .3s` oq tugmachani yashil fonda o'ngga mayin surib professional svitcher hosil qiladi.

## Ishlash natijasi:
```text
Bosilganda o'ngga surilib yashil rangga kiruvchi, qayta bosilganda chapga surilib kulrang bo'luvchi yoqgich vidjeti chiqadi.
```

---

# 294-Topshiriq: Yulduzli baholash vidjeti (Star Rating faqat CSS)
## Topshiriq sharti:
Foydalanuvchi mahsulotga 1 dan 5 gacha yulduzcha qo'yishi uchun sof CSS vidjeti.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Star Rating</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        .rating { display: flex; flex-direction: row-reverse; justify-content: flex-end; }
        .rating input { display: none; }
        .rating label { font-size: 30px; color: #cbd5e1; cursor: pointer; }
        .rating label:hover,
        .rating label:hover ~ label,
        .rating input:checked ~ label { color: #facc15; }
    </style>
</head>
<body>
    <div class="rating">
        <input type="radio" id="star5" name="rate" value="5"><label for="star5">&#9733;</label>
        <input type="radio" id="star4" name="rate" value="4"><label for="star4">&#9733;</label>
        <input type="radio" id="star3" name="rate" value="3"><label for="star3">&#9733;</label>
        <input type="radio" id="star2" name="rate" value="2"><label for="star2">&#9733;</label>
        <input type="radio" id="star1" name="rate" value="1"><label for="star1">&#9733;</label>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`flex-direction: row-reverse` va umumiy qardosh selektori `~` birikmasi orqali qaysi yulduzcha tanlansa, undan oldingi barcha yulduzchalar ham sariq rangga bo'yaladi.

## Ishlash natijasi:
```text
Kursor qaysi yulduzga borsa, ungacha bo'lgan barcha yulduzlar yorqin sariq bo'lib yonadi.
```

---

# 295-Topshiriq: Suzib yuruvchi matn sarlavhasi (Floating Label effekti)
## Topshiriq sharti:
Matn yozilganda sarlavha yuqori hoshiyaga ko'tariluvchi zamonaviy Google Material dizayn uslubi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Floating Label</title>
    <style>
        body { font-family: sans-serif; padding: 35px; }
        .field { position: relative; width: 280px; }
        .field input {
            width: 100%;
            padding: 12px 14px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            font-size: 16px;
            outline: none;
        }
        .field label {
            position: absolute;
            left: 14px;
            top: 14px;
            color: #94a3b8;
            transition: all 0.2s ease;
            pointer-events: none;
            background: white;
            padding: 0 4px;
        }
        .field input:focus ~ label,
        .field input:not(:placeholder-shown) ~ label {
            top: -8px;
            font-size: 12px;
            color: #2563eb;
        }
    </style>
</head>
<body>
    <div class="field">
        <input type="text" id="fl-name" placeholder=" ">
        <label for="fl-name">Ism va Familiyangiz</label>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`input:focus ~ label` kursor tushganda yoki ichiga matn yozilganda (`:not(:placeholder-shown)`) yozuvni tepa hoshiyaga ko'tarib kichraytiradi.

## Ishlash natijasi:
```text
Katakka bosilganda 'Ism va Familiyangiz' matni mayin harakat bilan yuqori hoshiya ustiga ko'tarilib ko'k rangga kiradi.
```

---

# 296-Topshiriq: Input ichida SVG ikonka joylashtirish (Search bar with icon)
## Topshiriq sharti:
Qidiruv katagining chap tomonida lupa belgisini joylashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Icon Input</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .search-box { position: relative; width: 300px; }
        .search-box svg { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); width: 18px; height: 18px; fill: #94a3b8; }
        .search-box input { width: 100%; padding: 10px 14px 10px 40px; border: 1px solid #cbd5e1; border-radius: 20px; box-sizing: border-box; }
    </style>
</head>
<body>
    <div class="search-box">
        <svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
        <input type="text" placeholder="Katalogdan qidirish...">
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Chap tomondagi `padding-left: 40px` yoziladigan matnning lupa belgisi ustiga chiqib ketishiga yo'l qo'ymaydi.

## Ishlash natijasi:
```text
Ichida lupa belgisi chizilgan professional qidiruv katakchasi aks etadi.
```

---

# 297-Topshiriq: Parolni ko'rsatuvchi ko'z tugmasi maketi
## Topshiriq sharti:
Katakning o'ng tomonida parolni ochish/yopish piktogrammasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Password Toggle UI</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .pwd-wrap { position: relative; width: 280px; }
        .pwd-wrap input { width: 100%; padding: 10px 40px 10px 12px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; }
        .pwd-wrap button { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; color: #64748b; font-size: 16px; }
    </style>
</head>
<body>
    <div class="pwd-wrap">
        <input type="password" placeholder="Parolni kiriting">
        <button type="button" aria-label="Parolni ko'rsatish">&#128065;</button>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
O'ng burchakdagi ko'zcha tugmasi kiritilgan maxfiy parolni ko'rish imkoniyatini taqdim etuvchi qulay interfeys yaratadi.

## Ishlash natijasi:
```text
O'ng chekkasida ko'zcha belgisi bo'lgan parol katakchasi ko'rinadi.
```

---

# 298-Topshiriq: Bank kartasi ma'lumotlarini kiritish qobig'i
## Topshiriq sharti:
Karta raqami, amal qilish muddati va CVV maydonlarini qulay guruhlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Bank Card Form</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .card-form { max-width: 350px; background: #f8fafc; border: 1px solid #e2e8f0; padding: 20px; border-radius: 8px; }
        .card-form input { width: 100%; padding: 8px; margin-bottom: 12px; box-sizing: border-box; border: 1px solid #cbd5e1; border-radius: 4px; }
        .row { display: flex; gap: 10px; }
    </style>
</head>
<body>
    <div class="card-form">
        <label>Karta raqami:</label>
        <input type="text" placeholder="8600 0000 0000 0000" maxlength="19">
        <div class="row">
            <div><label>Muddat:</label><input type="text" placeholder="MM/YY" maxlength="5"></div>
            <div><label>CVV:</label><input type="password" placeholder="***" maxlength="3"></div>
        </div>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Bir qatorda ikkita yonma-yon maydon (muddat va CVV) bilan kartalar to'lov formasining standart tartibi hosil qilinadi.

## Ishlash natijasi:
```text
To'lov tizimlariga xos bank kartasi ma'lumotlarini kiritish kartochkasi paydo bo'ladi.
```

---

# 299-Topshiriq: Ko'p bosqichli forma progress indikatori
## Topshiriq sharti:
1-2-3 qadamlardan iborat ro'yxatdan o'tish marshruti.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Form Stepper</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        .stepper { display: flex; justify-content: space-between; max-width: 300px; position: relative; margin-bottom: 30px; }
        .stepper::before { content: ''; position: absolute; top: 14px; left: 0; width: 100%; height: 2px; background: #cbd5e1; z-index: 1; }
        .step { width: 30px; height: 30px; border-radius: 50%; background: #cbd5e1; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; position: relative; z-index: 2; }
        .step.active { background: #2563eb; }
    </style>
</head>
<body>
    <div class="stepper">
        <div class="step active">1</div>
        <div class="step active">2</div>
        <div class="step">3</div>
    </div>
    <p>2-Bosqich: Shaxsiy ma'lumotlarni to'ldiring.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Chiziq ustidagi doiralar qaysi bosqichda turganlikni ifodalaydi. Birinchi va ikkinchi qadam ko'k rangda faol bo'ladi.

## Ishlash natijasi:
```text
1 va 2 raqamlari ko'k, 3 raqami kulrang bo'lgan chiroyli bosqichlar indikatori chiqadi.
```

---

# 300-Topshiriq: To'liq professional ro'yxatdan o'tish (Register) formasi
## Topshiriq sharti:
Barcha validation mezonlari, chiroyli dizayn, shartlarga rozilik checkboxi va submit tugmasiga ega mukammal forma.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ro'yxatdan O'tish</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f1f5f9; display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 20px; }
        .form-card { background: white; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); padding: 35px; width: 100%; max-width: 420px; }
        .form-card h2 { color: #0f172a; margin-bottom: 8px; }
        .form-card p { color: #64748b; font-size: 14px; margin-bottom: 25px; }
        .form-group { margin-bottom: 18px; }
        label { display: block; font-size: 13px; font-weight: 600; color: #334155; margin-bottom: 6px; }
        input[type="text"], input[type="email"], input[type="password"] {
            width: 100%; padding: 11px 14px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 15px; outline: none; transition: border-color 0.2s, box-shadow 0.2s;
        }
        input:focus { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.15); }
        .terms { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #475569; margin: 20px 0; }
        .btn-submit { width: 100%; background: #2563eb; color: white; padding: 12px; border: none; border-radius: 6px; font-size: 16px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
        .btn-submit:hover { background: #1d4ed8; }
    </style>
</head>
<body>
    <div class="form-card">
        <h2>Akkaunt Yaratish</h2>
        <p>Barcha imkoniyatlardan foydalanish uchun ro'yxatdan o'ting.</p>
        <form action="/register" method="POST">
            <div class="form-group">
                <label for="reg-name">To'liq ismingiz</label>
                <input type="text" id="reg-name" name="name" required placeholder="Ali Valiyev">
            </div>
            <div class="form-group">
                <label for="reg-email">Elektron pochta</label>
                <input type="email" id="reg-email" name="email" required placeholder="ali@misol.uz">
            </div>
            <div class="form-group">
                <label for="reg-pass">Parol</label>
                <input type="password" id="reg-pass" name="password" minlength="8" required placeholder="Kamida 8 ta belgi">
            </div>
            <div class="terms">
                <input type="checkbox" id="terms-agree" required>
                <label for="terms-agree" style="margin:0; font-weight:normal;">Men foydalanish shartlariga roziman</label>
            </div>
            <button type="submit" class="btn-submit">Ro'yxatdan O'tish</button>
        </form>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu yakuniy andoza zamonaviy forma dizaynining barcha talablarini (aniq label bog'lanishlari, to'g'ri type lar, xavfsiz POST usuli, required va minlength tekshiruvlari, nurli focus effekti va rozilik bayroqchasi) qamragan professional registration shablonidir.

## Ishlash natijasi:
```text
Zamonaviy fintech yoki SaaS ilovalariga xos, oq kartochkada joylashgan jozibali ro'yxatdan o'tish formasi paydo bo'ladi.
```

---

