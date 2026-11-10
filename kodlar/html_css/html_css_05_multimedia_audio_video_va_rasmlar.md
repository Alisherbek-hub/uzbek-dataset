# Multimedia, Audio, Video va Rasmlar (201-250)

# 201-Topshiriq: <img> tegi, src va alt atributlari
## Topshiriq sharti:
Veb-sahifaga rasm joylashtirish va unga muqobil matn berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Img Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        img { max-width: 100%; height: auto; border-radius: 8px; }
    </style>
</head>
<body>
    <img src="https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=400" alt="Milliylik va naqshlar bilan bezatilgan Registon maydoni">
</body>
</html>
```

## Tushuntirish va Mantiq:
`<img>` tegi bo'sh element (yopiluvchi tegsiz) bo'lib, `src` (source) tasvir manzilini, `alt` (alternative text) esa tasvir yuklanmaganda yoki ekranni o'quvchi dasturlar uchun matnli tavsifni ifodalaydi.

## Ishlash natijasi:
```text
Sahifada burchaklari yumaloqlangan Samarqand Registon maydoni tasviri ko'rinadi.
```

---

# 202-Topshiriq: alt atributining SEO va a11y roli
## Topshiriq sharti:
Ko'rish qobiliyati cheklanganlar va qidiruv tizimlari uchun aniq tavsifli alt yozish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Alt Matni Qoidalari</title>
    <style>
        body { font-family: sans-serif; padding: 20px; line-height: 1.6; }
    </style>
</head>
<body>
    <!-- Yomon amaliyot: alt="rasm" yoki alt="foto" -->
    <!-- Mukammal amaliyot: tasvirdagi detal va harakatni aytish -->
    <img src="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='100' height='60'><rect width='100' height='60' fill='%2322c55e'/><text x='50%' y='50%' fill='white' dominant-baseline='middle' text-anchor='middle'>Grafik</text></svg>"
         alt="2026-yilgi IT eksport hajmining o'sish dinamikasi chizmasi">
</body>
</html>
```

## Tushuntirish va Mantiq:
Qidiruv robotlari rasmni 'ko'ra' olmaydi, ular rasm ma'nosini faqat `alt` orqali tushunadi. Shuningdek ko'zi ojiz insonlar kompyuterdan foydalanganda ularning dasturi aynan `alt` matnini o'qib beradi.

## Ishlash natijasi:
```text
Yashil to'rtburchak shaklidagi grafik tasviri chiqadi; texnik jihatdan u boy ma'lumotga ega.
```

---

# 203-Topshiriq: width va height atributlari va CLS muammosini hal qilish
## Topshiriq sharti:
Sahifa yuklanayotganda kontent pastga-tepaga sakrab ketishining (Cumulative Layout Shift) oldini olish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>CLS Oldini Olish</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        img { width: 100%; max-width: 400px; height: auto; }
    </style>
</head>
<body>
    <img src="https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400"
         width="400" height="267"
         alt="Dasturchi noutbukda kod yozmoqda">
    <p>Ushbu matn rasm yuklanguncha o'z joyida qimirlamay turadi, chunki brauzer rasm uchun joy ajratib qo'ygan.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
HTML da `width` va `height` atributlarini ko'rsatish brauzerga rasm nisbatini (aspect-ratio) oldindan bilishga imkon beradi. Rasm sekin yuklansa ham uning bo'sh joyi saqlanadi va matnlar sakramaydi (CLS = 0 bo'ladi).

## Ishlash natijasi:
```text
Rasm o'zining aniq 400x267 o'lchamli maydonida yuklanadi, matn o'z o'rnida mustahkam turadi.
```

---

# 204-Topshiriq: loading='lazy' bilan rasmlarni kechiktirib yuklash
## Topshiriq sharti:
Faqat foydalanuvchi ekranni pastga aylantirib borgandagina rasmlarni yuklash orqali trafikni tejash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Lazy Loading</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .space { height: 1000px; background: #f8fafc; padding: 20px; }
    </style>
</head>
<body>
    <h1>Sahifa Boshlanishi</h1>
    <div class="space">Pastga aylantiring...</div>
    <img src="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=500"
         loading="lazy"
         alt="Matrix kodlari yashil chiroqlari"
         width="500" height="300">
</body>
</html>
```

## Tushuntirish va Mantiq:
`loading='lazy'` atributi brauzer darajasidagi mahalliy dangasa yuklash (native lazy loading) vositasidir. Ekrandan tashqaridagi rasmlar darhol yuklanmaydi, foydalanuvchi ularga yaqinlashgandagina yuklanadi.

## Ishlash natijasi:
```text
Sahifa ochilganda pastdagi rasm yuklanmay turadi; pastga aylantirilsa bir zumda yuklanadi.
```

---

# 205-Topshiriq: decoding='async' xususiyati
## Topshiriq sharti:
Rasmni dekodlash jarayonini asosiy potokdan (main thread) ajratib sahifa tezligini oshirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Decoding Async</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
    </style>
</head>
<body>
    <img src="https://images.unsplash.com/photo-1534972195531-a756b1126f24?w=400"
         decoding="async"
         alt="Texnologik laboratoriya"
         width="400" height="250">
</body>
</html>
```

## Tushuntirish va Mantiq:
`decoding='async'` brauzerga rasmni ochish va render qilishni asinxron fonda bajarishga ruxsat beradi. Bu asosiy interfeysning qotib qolmasligini ta'minlaydi.

## Ishlash natijasi:
```text
Sahifa elementlari rasm dekodlanishini kutmasdan darhol silliq ishga tushadi.
```

---

# 206-Topshiriq: <picture> tegi va uning arxitekturasi
## Topshiriq sharti:
Turli ekran o'lchamlari yoki rasm formatlariga qarab turli rasmlarni tanlash konteyneri.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Picture Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        picture img { max-width: 100%; height: auto; border-radius: 6px; }
    </style>
</head>
<body>
    <picture>
        <source media="(min-width: 800px)" srcset="https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800">
        <source media="(min-width: 400px)" srcset="https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=400">
        <img src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=300" alt="Go'zal tog' manzarasi">
    </picture>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<picture>` bir nechta `<source>` variantlarini o'z ichiga oladi. Brauzer shartlarga eng mos keluvchi birinchi source ni tanlaydi va eng oxiridagi `<img>` orqali uni ekranga chiqaradi.

## Ishlash natijasi:
```text
Katta ekranda katta tiniq rasm, tor ekranda esa kichik hajmdagi rasm yuklanadi.
```

---

# 207-Topshiriq: <source media='...'> bilan Art Direction (Badiiy yo'naltirish)
## Topshiriq sharti:
Kompyuterda keng panorama, telefonda esa vertikal qirqilgan portret rasmni ko'rsatish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Art Direction</title>
    <style>
        picture img { width: 100%; max-width: 600px; display: block; margin: 20px auto; }
    </style>
</head>
<body>
    <picture>
        <!-- Mobil ekranda kvadrat fokuslangan rasm -->
        <source media="(max-width: 600px)" srcset="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&h=400&fit=crop">
        <!-- Monitorlarda keng formatli rasm -->
        <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800&h=400&fit=crop" alt="Portret banner">
    </picture>
</body>
</html>
```

## Tushuntirish va Mantiq:
Art direction shunchaki rasmni kichraytirish emas, balki mobil qurilmada rasmning eng asosiy qismini yaqinlashtirib (krop qilib) ko'rsatishdir.

## Ishlash natijasi:
```text
Telefon o'lchamiga o'tganda rasm shakli kvadratga aylanib, markazdagi yuz yaqinlashadi.
```

---

# 208-Topshiriq: <source type='image/webp'> zamonaviy formatlarni yuklash
## Topshiriq sharti:
Brauzer qo'llab-quvvatlasa o'ta yengil WebP yoki AVIF, bo'lmasa an'anaviy JPEG yuklash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>WebP va AVIF</title>
</head>
<body>
    <picture>
        <source srcset="rasm.avif" type="image/avif">
        <source srcset="rasm.webp" type="image/webp">
        <img src="rasm.jpg" alt="Zamonaviy formatdagi rasm">
    </picture>
</body>
</html>
```

## Tushuntirish va Mantiq:
`type` atributi brauzerga formatni bildiradi. Zamonaviy brauzerlar AVIF yoki WebP ni tanlab 70% gacha trafikni tejaydi, eski brauzerlar esa zaxiradagi JPG ni ochadi.

## Ishlash natijasi:
```text
Eng zamonaviy va yengil format avtomatik tanlanib ochiladi.
```

---

# 209-Topshiriq: srcset va sizes atributlari (Resolution switching)
## Topshiriq sharti:
Bitta rasmning turli kenglikdagi nusxalarini brauzerga taklif qilish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Srcset va Sizes</title>
    <style>
        img { width: 100%; height: auto; }
    </style>
</head>
<body>
    <img src="manzara-800.jpg"
         srcset="manzara-400.jpg 400w, manzara-800.jpg 800w, manzara-1200.jpg 1200w"
         sizes="(max-width: 600px) 100vw, (max-width: 1200px) 50vw, 800px"
         alt="Keng formatdagi manzara">
</body>
</html>
```

## Tushuntirish va Mantiq:
`srcset` dagi `400w`, `800w` qiymatlari rasmning asl piksel kengligini bildiradi. `sizes` esa ekranning turli o'lchamlarida rasm qancha kenglik egallashini aytadi. Brauzer eng ideal faylni o'zi hisoblab yuklaydi.

## Ishlash natijasi:
```text
Har qanday qurilma o'ziga mos eng yengil va eng tiniq variantni avtomatik qabul qiladi.
```

---

# 210-Topshiriq: Retina (2x, 3x) ekranlar uchun piksel zichligi
## Topshiriq sharti:
Apple Retina va zamonaviy OLED ekranlar uchun yuqori tiniqlikdagi rasmlar taqdim etish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Retina Ekranlar</title>
</head>
<body>
    <img src="logo.png"
         srcset="logo.png 1x, logo-2x.png 2x, logo-3x.png 3x"
         alt="Yuqori tiniqlikdagi logotip"
         width="200" height="60">
</body>
</html>
```

## Tushuntirish va Mantiq:
`1x` oddiy monitorlar, `2x` Retina va flagman smartfonlar, `3x` esa o'ta yuqori zichlikdagi ekranlar uchun xizmat qiladi va logotipning xiralashib qolishini oldini oladi.

## Ishlash natijasi:
```text
Retina ekranlarda logotip kristalldek tiniq ko'rinadi.
```

---

# 211-Topshiriq: <audio> tegi va controls atributi
## Topshiriq sharti:
Veb-sahifaga audio pleyer joylashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Audio Pleyer</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
    </style>
</head>
<body>
    <h3>O'zbek Milliy Musiqasi (Shashmaqom)</h3>
    <audio controls>
        <source src="https://www.w3schools.com/html/horse.mp3" type="audio/mpeg">
        Brauzeringiz audio elementini qo'llab-quvvatlamaydi.
    </audio>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<audio>` tegi HTML5 da ovozli fayllarni o'ynatish uchun javobgardir. `controls` atributi bo'lmasa brauzer pleyer boshqaruv paneli (play, pause, ovoz)ni ekranda ko'rsatmaydi.

## Ishlash natijasi:
```text
Sahifada ijro tugmasi, vaqt chizig'i va ovoz balandligini sozlovchi to'liq audio pleyer chiqadi.
```

---

# 212-Topshiriq: audio atributlari: autoplay, loop, muted, preload
## Topshiriq sharti:
Audio ijrosining texnik parametrlarini nazorat qilish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Audio Sozlamalari</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
    </style>
</head>
<body>
    <!-- loop - takroriy ijro, preload="metadata" faqat davomiyligini yuklaydi -->
    <audio controls loop preload="metadata" muted>
        <source src="track.mp3" type="audio/mpeg">
    </audio>
</body>
</html>
```

## Tushuntirish va Mantiq:
`loop` qo'shiq tugagach uni boshidan qayta qo'yadi. `muted` sukut bo'yicha ovozni o'chirib turadi. `preload='metadata'` esa butun faylni yuklab trafik sarflamasdan faqat uning davomiyligini o'qiydi.

## Ishlash natijasi:
```text
Ovozi o'chirilgan (muted) holatdagi qayta takrorlanuvchi pleyer ko'rinadi.
```

---

# 213-Topshiriq: Audio ichida bir nechta <source> (mp3, ogg, wav)
## Topshiriq sharti:
Barcha brauzerlar tushunishi uchun turli formatlarni biriktirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Multi Audio Format</title>
</head>
<body>
    <audio controls>
        <source src="audio.ogg" type="audio/ogg">
        <source src="audio.mp3" type="audio/mpeg">
        <source src="audio.wav" type="audio/wav">
    </audio>
</body>
</html>
```

## Tushuntirish va Mantiq:
Agar birinchi formatni brauzer qo'llab-quvvatlamasa, avtomatik ravishda keyingi source ga o'tadi.

## Ishlash natijasi:
```text
Universal moslashuvchan audio boshqaruv paneli chiqadi.
```

---

# 214-Topshiriq: <video> tegi va uning asosiy atributlari
## Topshiriq sharti:
HTML5 video pleyerini sahifaga o'rnatish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Video Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        video { max-width: 100%; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.15); }
    </style>
</head>
<body>
    <video width="640" height="360" controls>
        <source src="https://www.w3schools.com/html/mov_bbb.mp4" type="video/mp4">
        Sizning brauzeringiz videoni qo'llab-quvvatlamaydi.
    </video>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<video>` elementi uchinchi tomon plaginlarisiz (Flashsiz) to'g'ridan-to'g'ri brauzerning o'zida videolarni o'ynatish imkonini yaratadi.

## Ishlash natijasi:
```text
Katta ekranli, pastida ijro paneli bo'lgan video pleyer paydo bo'ladi.
```

---

# 215-Topshiriq: <video poster='...'> muqova tasviri
## Topshiriq sharti:
Video boshlanmasidan oldin ekranda ko'rinib turadigan chiroyli muqova (thumbnail) o'rnatish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Video Poster</title>
</head>
<body>
    <video width="500" controls poster="https://images.unsplash.com/photo-1518770660439-4636190af475?w=500">
        <source src="video.mp4" type="video/mp4">
    </video>
</body>
</html>
```

## Tushuntirish va Mantiq:
`poster` atributi video yuklanguncha yoki foydalanuvchi play tugmasini bosgunga qadar ko'rinib turuvchi statik rasmni belgilaydi.

## Ishlash natijasi:
```text
Video o'ynatilmasdan oldin uning ustida texnologik chiroyli rasm turadi.
```

---

# 216-Topshiriq: <video playsinline> mobil moslashuv
## Topshiriq sharti:
iPhone va Android smartfonlarda videoni to'liq ekranga sakrab ketmasdan sahifa ichida o'ynatish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Playsinline</title>
</head>
<body>
    <video width="320" height="240" controls playsinline autoplay muted>
        <source src="video.mp4" type="video/mp4">
    </video>
</body>
</html>
```

## Tushuntirish va Mantiq:
`playsinline` ayniqsa iOS Safari da video bosilganda butun telefon ekranini qoplab olmasdan, sahifa dizayni ichida qolishini ta'minlaydi.

## Ishlash natijasi:
```text
Mobil ekranda sahifa tartibini buzmagan holda o'ynovchi ixcham video.
```

---

# 217-Topshiriq: <track> tegi bilan o'zbekcha subtitrlar qo'shish
## Topshiriq sharti:
Videoga o'zbek tilidagi subtitr va matnli tarjimalarni ulash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Video Subtitrlar</title>
</head>
<body>
    <video width="600" controls>
        <source src="dars.mp4" type="video/mp4">
        <track src="subtitr_uz.vtt" kind="subtitles" srclang="uz" label="O'zbekcha" default>
    </video>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<track>` tegi videoga matnli yo'lakchalarni ulaydi. `kind='subtitles'` subtitr ekanini, `srclang='uz'` tilini, `default` esa avtomatik yoqilishini belgilaydi.

## Ishlash natijasi:
```text
Video pastki qismida subtitrlarni tanlash tugmasi (CC) chiqadi.
```

---

# 218-Topshiriq: WebVTT (.vtt) formati sintaksisi
## Topshiriq sharti:
Subtitrlar qaysi soniyada chiqishi kerakligini belgilovchi matn fayli tuzilmasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>WebVTT Sintaksisi</title>
    <style>
        pre { background: #0f172a; color: #38bdf8; padding: 20px; border-radius: 6px; }
    </style>
</head>
<body>
    <h3>subtitr_uz.vtt faylining mazmuni:</h3>
    <pre><code>WEBVTT

00:00:01.000 --> 00:00:04.000
Assalomu alaykum, aziz talabalar!

00:00:04.500 --> 00:00:08.000
Bugun biz HTML5 multimedia imkoniyatlarini o'rganamiz.</code></pre>
</body>
</html>
```

## Tushuntirish va Mantiq:
WebVTT (Web Video Text Tracks) standarti `WEBVTT` sarlavhasi bilan boshlanadi va aniq millisekundlargacha bo'lgan vaqt oralig'i (`-->`) orqali matnlarni kadrga bog'laydi.

## Ishlash natijasi:
```text
Vaqt ko'rsatkichlari bilan yozilgan subtitr kodi namunasi chiqadi.
```

---

# 219-Topshiriq: <iframe> tegi va tashqi resurslarni kiritish
## Topshiriq sharti:
Sahifa ichida boshqa bir veb-sahifani darcha ko'rinishida ochish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Iframe Tegi</title>
    <style>
        iframe { border: 2px solid #cbd5e1; border-radius: 8px; }
    </style>
</head>
<body>
    <iframe src="https://example.com" width="500" height="300" title="Misol veb sahifasi"></iframe>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<iframe>` (inline frame) o'z sahifangiz ichida butunlay boshqa bir HTML hujjatini ochib beradi. Har doim ekranni o'quvchilar uchun `title` atributi yozilishi shart.

## Ishlash natijasi:
```text
Sahifa markazida 500x300 o'lchamdagi mustaqil veb darchasi paydo bo'ladi.
```

---

# 220-Topshiriq: iframe xavfsizligi: sandbox atributi
## Topshiriq sharti:
Tashqi saytlardan keluvchi viruslar, nojo'ya skriptlar va fishingni taqiqlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Iframe Sandbox</title>
</head>
<body>
    <!-- sandbox ichidagi sahifaga skript ishlatishni va forma yuborishni taqiqlaydi -->
    <iframe src="tashqi_sayt.html" sandbox="allow-scripts allow-same-origin" width="400" height="200" title="Himoyalangan freym"></iframe>
</body>
</html>
```

## Tushuntirish va Mantiq:
`sandbox` bo'sh qoldirilsa barcha xavfli xatti-harakatlar (JS ishga tushishi, pop-up ochish, forma jo'natish) to'xtatiladi. `allow-scripts` kabi ruxsatlar faqat kerakli imkoniyatlarni ehtiyotkorlik bilan ochish uchun qo'llaniladi.

## Ishlash natijasi:
```text
Qat'iy xavfsizlik cheklovlari ostida ishlovchi izolyatsiyalangan freym ko'rinadi.
```

---

# 221-Topshiriq: iframe ruxsatnomalari: allow atributi
## Topshiriq sharti:
Kamera, mikrofon va to'liq ekranga chiqish ruxsatnomalarini boshqarish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Iframe Permissions</title>
</head>
<body>
    <iframe src="video_chat.html"
            width="500" height="350"
            allow="camera; microphone; fullscreen"
            title="Video Chat">
    </iframe>
</body>
</html>
```

## Tushuntirish va Mantiq:
`allow` atributi brauzer Feature Policy mezoniga ko'ra freym ichidagi ilovaga faqat ko'rsatilgan apparat vositalaridan (kamera, mikrofon) foydalanishga ruxsat beradi.

## Ishlash natijasi:
```text
Video qo'ng'iroqlar uchun apparat vositalariga ulanish huquqiga ega bo'lgan darcha ochiladi.
```

---

# 222-Topshiriq: YouTube videolarini iframe orqali joylashtirish
## Topshiriq sharti:
YouTube platformasidagi videoni to'g'ri parametrlar bilan sahifaga integratsiya qilish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>YouTube Embed</title>
</head>
<body>
    <iframe width="560" height="315"
            src="https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ"
            title="YouTube video player"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen>
    </iframe>
</body>
</html>
```

## Tushuntirish va Mantiq:
`youtube-nocookie.com` foydalanuvchi maxfiyligini (GDPR standartlarini) himoya qiladi. `allowfullscreen` esa to'liq ekranga kattalashtirish imkonini beradi.

## Ishlash natijasi:
```text
Sahifada to'liq interaktiv YouTube video pleyeri paydo bo'ladi.
```

---

# 223-Topshiriq: Responsiv video konteyneri (aspect-ratio: 16 / 9)
## Topshiriq sharti:
Ekran kichrayganda yoki kattalashganda video nisbatini 16:9 da ushlab turish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsive Video</title>
    <style>
        .video-container {
            width: 100%;
            max-width: 700px;
            aspect-ratio: 16 / 9;
            margin: 0 auto;
        }
        .video-container iframe {
            width: 100%;
            height: 100%;
            border: none;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="video-container">
        <iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" title="Video" allowfullscreen></iframe>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Zamonaviy `aspect-ratio: 16 / 9` xususiyati eski `padding-top: 56.25%` xaklarini yo'qqa chiqarib, bir qator kod bilan videoni mukammal responsiv qiladi.

## Ishlash natijasi:
```text
Telefon yoki kompyuter o'lchamidan qat'i nazar, mukammal 16 ga 9 proporsiyasini saqlovchi video darchasi ko'rinadi.
```

---

# 224-Topshiriq: Inline <svg> tegi asoslari
## Topshiriq sharti:
Vektorli grafikani to'g'ridan-to'g'ri HTML sahifa kodiga joylashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Inline SVG</title>
</head>
<body>
    <svg width="100" height="100" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="40" stroke="#2563eb" stroke-width="4" fill="#93c5fd" />
    </svg>
</body>
</html>
```

## Tushuntirish va Mantiq:
Inline SVG alohida HTTP so'rovi talab qilmaydi, sifatini mutlaqo yo'qotmaydi va CSS orqali ranglarini bevosita boshqarish imkonini beradi.

## Ishlash natijasi:
```text
Moviy hoshiyali va och moviy rangda to'ldirilgan tiniq doira chiziladi.
```

---

# 225-Topshiriq: SVG primitivlari: <circle>, <rect>, <line>, <ellipse>
## Topshiriq sharti:
SVG ning asosiy geometrik shakllarini chizish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>SVG Shakllari</title>
</head>
<body>
    <svg width="350" height="100">
        <!-- To'rtburchak -->
        <rect x="10" y="20" width="60" height="60" fill="#f87171" rx="8"/>
        <!-- Aylana -->
        <circle cx="120" cy="50" r="30" fill="#60a5fa"/>
        <!-- Ellips -->
        <ellipse cx="210" cy="50" rx="40" ry="25" fill="#34d399"/>
        <!-- Chiziq -->
        <line x1="280" y1="20" x2="330" y2="80" stroke="#a78bfa" stroke-width="6"/>
    </svg>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<rect>` to'rtburchak, `<circle>` doira, `<ellipse>` cho'zinchoq doira, `<line>` esa to'g'ri chiziq yasaydi. `rx` to'rtburchak burchaklarini yumaloqlaydi.

## Ishlash natijasi:
```text
Qizil to'rtburchak, ko'k doira, yashil ellips va siyohrang qiya chiziq bitta qatorda chiziladi.
```

---

# 226-Topshiriq: SVG <polygon> va <polyline>
## Topshiriq sharti:
Ko'pburchaklar, yulduzchalar va singan chiziqlarni chizish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Polygon va Polyline</title>
</head>
<body>
    <svg width="250" height="120">
        <!-- Yulduzcha -->
        <polygon points="60,10 75,50 115,50 82,75 95,115 60,90 25,115 38,75 5,50 45,50" fill="#facc15" stroke="#eab308" stroke-width="2"/>
        <!-- Zinapoya singan chizig'i -->
        <polyline points="140,90 170,90 170,60 200,60 200,30" fill="none" stroke="#2563eb" stroke-width="4"/>
    </svg>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<polygon>` nuqtalar ketma-ketligi bo'yicha yopiq ko'pburchak yasaydi. `<polyline>` esa oxirgi nuqtani birinchisiga birlashtirmaydigan ochiq singan chiziq hosil qiladi.

## Ishlash natijasi:
```text
Sariq yulduzcha va ko'k rangli zinapoyasimon chiziq ko'rinadi.
```

---

# 227-Topshiriq: SVG <path> tegi va d atributi
## Topshiriq sharti:
Eng murakkab vektorli chizmalar va egri chiziqlarni yaratuvchi path.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>SVG Path</title>
</head>
<body>
    <svg width="100" height="100" viewBox="0 0 24 24" fill="#ef4444">
        <!-- Yurakcha belgisi -->
        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
    </svg>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<path>` ning `d` atributidagi buyruqlar: `M` (move to - ko'chirish), `L` (line to - chizish), `C` (curve - egri chiziq), `Z` (close path - yopish) orqali har qanday shaklni ifodalaydi.

## Ishlash natijasi:
```text
Qizil rangdagi juda tiniq yurakcha piktogrammasi chiziladi.
```

---

# 228-Topshiriq: SVG <defs> va <linearGradient>
## Topshiriq sharti:
Vektorli shakllar ichiga rang-barang gradientlar quyish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>SVG Gradient</title>
</head>
<body>
    <svg width="200" height="100">
        <defs>
            <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#3b82f6;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#ec4899;stop-opacity:1" />
            </linearGradient>
        </defs>
        <rect width="200" height="80" rx="15" fill="url(#grad1)" />
    </svg>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<defs>` (definitions) ichida resurslar saqlanadi. `linearGradient id='grad1'` yaratilib, shaklga `fill='url(#grad1)'` orqali biriktiriladi.

## Ishlash natijasi:
```text
Ko'kdan pushti rangga o'tuvchi gradient bilan bo'yalgan to'rtburchak hosil bo'ladi.
```

---

# 229-Topshiriq: SVG <symbol> va <use> (SVG Sprite tizimi)
## Topshiriq sharti:
Bitta ikonkani bir marta e'lon qilib, butun sayt bo'ylab ko'p marotaba nusxalash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>SVG Sprite</title>
    <style>
        .icon { width: 32px; height: 32px; fill: #2563eb; }
    </style>
</head>
<body>
    <svg style="display: none;">
        <symbol id="check-icon" viewBox="0 0 24 24">
            <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
        </symbol>
    </svg>

    <p><svg class="icon"><use href="#check-icon"/></svg> 1-Band tasdiqlandi</p>
    <p><svg class="icon"><use href="#check-icon"/></svg> 2-Band tasdiqlandi</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<symbol>` ikonkani xotirada shablon qiladi. `<use href='#id'/>` esa kerakli joyda uni chaqirib chiqaradi. Bu sahifa kodini yengillashtiradi.

## Ishlash natijasi:
```text
Ikkita qator boshida bir xil moviy tasdiqlash belgilari paydo bo'ladi.
```

---

# 230-Topshiriq: CSS orqali SVG ni boshqarish (fill, stroke, currentColor)
## Topshiriq sharti:
Matn rangiga qarab avtomatik o'zgaruvchi moslashuvchan ikonka.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>SVG currentColor</title>
    <style>
        .btn { display: inline-flex; align-items: center; gap: 8px; padding: 10px 16px; border-radius: 6px; border: 2px solid #2563eb; color: #2563eb; background: transparent; cursor: pointer; transition: all 0.2s; }
        .btn:hover { background: #2563eb; color: #ffffff; }
        .btn svg { fill: currentColor; width: 18px; height: 18px; }
    </style>
</head>
<body>
    <button class="btn">
        <svg viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg>
        <span>Saqlash</span>
    </button>
</body>
</html>
```

## Tushuntirish va Mantiq:
`fill: currentColor` xususiyati SVG rangini ota elementning joriy matn rangi (`color`)ga tenglashtiradi. Hover bo'lganda matn rangi oq bo'lsa, SVG ham avtomatik oqqa aylanadi.

## Ishlash natijasi:
```text
Kursor kelganda ko'k fonda oq matn va oq ikonchaga aylanuvchi tugmacha chiqadi.
```

---

# 231-Topshiriq: SVG hover animatsiyasi
## Topshiriq sharti:
Sichqoncha borganda aylanuvchi yoki kattalashuvchi vektorli piktogramma.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>SVG Animatsiya</title>
    <style>
        .gear-icon { width: 50px; height: 50px; fill: #475569; transition: transform 0.5s ease; cursor: pointer; }
        .gear-icon:hover { transform: rotate(180deg) scale(1.15); fill: #3b82f6; }
    </style>
</head>
<body>
    <svg class="gear-icon" viewBox="0 0 24 24">
        <path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/>
    </svg>
</body>
</html>
```

## Tushuntirish va Mantiq:
CSS `transition` va `transform: rotate(180deg)` orqali tishli g'ildirak (sozlamalar belgisi) ustiga kelganda silliq aylanadi.

## Ishlash natijasi:
```text
Kursor borganda 180 gradusga aylanib ko'k rangga kiruvchi tishli g'ildirak ikonchasi.
```

---

# 232-Topshiriq: <canvas> elementi va uning chizish maydoni
## Topshiriq sharti:
JavaScript orqali piksellarni chizish uchun mo'ljallangan dinamik mato.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Canvas Maydoni</title>
    <style>
        canvas { border: 2px solid #0f172a; border-radius: 6px; }
    </style>
</head>
<body>
    <canvas id="myCanvas" width="300" height="150"></canvas>
    <script>
        const ctx = document.getElementById('myCanvas').getContext('2d');
        ctx.fillStyle = '#10b981';
        ctx.fillRect(20, 20, 100, 80);
    </script>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<canvas>` tegi dasturlash orqali o'yinlar, grafiklar va animatsiyalar chizish uchun bo'sh pikselli konteynerdir. SVG dan farqli ravishda u raster (bitmap) grafikaga asoslangan.

## Ishlash natijasi:
```text
Qora hoshiyali darcha ichida JavaScript chizgan yashil to'rtburchak ko'rinadi.
```

---

# 233-Topshiriq: <embed> tegi va uning qo'llanishi
## Topshiriq sharti:
Tashqi plagin yoki multimedia resurslarini integratsiya qilish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Embed Tegi</title>
</head>
<body>
    <embed type="video/webm" src="video.webm" width="400" height="250">
</body>
</html>
```

## Tushuntirish va Mantiq:
`<embed>` tegi brauzerga multimedia yoki tashqi plagin kontentini kiritish uchun xizmat qiladi. Zamonaviy vebda video va audio uchun ixtisoslashgan teglardan foydalanish tavsiya etiladi.

## Ishlash natijasi:
```text
Ichki resursni o'ynatuvchi darcha paydo bo'ladi.
```

---

# 234-Topshiriq: <object> va <param> orqali PDF ochish
## Topshiriq sharti:
Veb-sahifa ichida PDF hujjatlarini zaxira matni bilan ko'rsatish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Object PDF</title>
</head>
<body>
    <object data="hujjat.pdf" type="application/pdf" width="100%" height="400">
        <p>Brauzeringizda PDF ko'rish o'chirilgan: <a href="hujjat.pdf">Hujjatni yuklab oling</a>.</p>
    </object>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<object>` tegi tashqi resursni (PDF, SVG) yuklaydi. Agar brauzer uni ocholmasa, uning ichidagi zaxira matn va yuklab olish havolasi avtomatik ko'rsatiladi.

## Ishlash natijasi:
```text
Sahifaga joylashtirilgan PDF o'quvchi oynasi chiqadi.
```

---

# 235-Topshiriq: Dumaloq avatar rasmi (border-radius va object-fit: cover)
## Topshiriq sharti:
Foydalanuvchi profil rasmini buzilmasdan ideal doira qilish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Dumaloq Avatar</title>
    <style>
        .avatar {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #3b82f6;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <img src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=200" class="avatar" alt="Foydalanuvchi avatari">
</body>
</html>
```

## Tushuntirish va Mantiq:
`border-radius: 50%` rasmni doiraga aylantiradi. `object-fit: cover` esa rasm to'rtburchak bo'lsa ham uning cho'zilib yoki yassilanib ketishiga yo'l qo'ymasdan markazdan qirqib moslaydi.

## Ishlash natijasi:
```text
Ko'k hoshiyali mukammal dumaloq yuz tasviri ko'rinadi.
```

---

# 236-Topshiriq: Rasm ustiga qoraytirilgan qatlam (Overlay)
## Topshiriq sharti:
Rasm ustidagi oq matn har doim tiniq o'qilishi uchun qoraytiruvchi shaffof qatlam.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Image Overlay</title>
    <style>
        .banner {
            position: relative;
            width: 500px;
            height: 250px;
            border-radius: 8px;
            overflow: hidden;
        }
        .banner img { width: 100%; height: 100%; object-fit: cover; }
        .overlay {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="banner">
        <img src="https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=500" alt="Jamoa">
        <div class="overlay">Bizning Jamoa</div>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`rgba(0, 0, 0, 0.5)` qora shaffof qatlam hosil qilib, tagdagi rasmning yorug'ligi qanday bo'lishidan qat'i nazar, ustidagi oq sarlavhaning 100% o'qilishini ta'minlaydi.

## Ishlash natijasi:
```text
Yarim qorong'ilatilgan rasm ustida oq rangda 'Bizning Jamoa' sarlavhasi yorqin ko'rinadi.
```

---

# 237-Topshiriq: object-fit xususiyatlari: contain, cover, fill
## Topshiriq sharti:
Belgilangan o'lchamli katak ichida rasm o'zini qanday tutishini boshqarish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Object Fit</title>
    <style>
        body { font-family: sans-serif; display: flex; gap: 20px; padding: 20px; }
        .box { width: 150px; height: 150px; border: 2px dashed #94a3b8; }
        img { width: 100%; height: 100%; }
        .fill { object-fit: fill; }
        .contain { object-fit: contain; background: #eee; }
        .cover { object-fit: cover; }
    </style>
</head>
<body>
    <div><p>Fill (Buziladi)</p><div class="box"><img src="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=200" class="fill"></div></div>
    <div><p>Contain (To'liq sig'adi)</p><div class="box"><img src="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=200" class="contain"></div></div>
    <div><p>Cover (Ideal qirqiladi)</p><div class="box"><img src="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=200" class="cover"></div></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`fill` rasmni ezib buzadi, `contain` proporsiyani saqlab katak ichiga to'liq sig'diradi, `cover` esa butun katakni bo'sh joy qoldirmasdan to'ldiradi.

## Ishlash natijasi:
```text
Uch xil moslashuv uslubida bitta krossovka rasmining taqqoslanishi chiqadi.
```

---

# 238-Topshiriq: object-position orqali rasm markazini to'g'irlash
## Topshiriq sharti:
Qirqilayotgan rasmning aynan qaysi burchagi ko'rinib turishi kerakligini sozlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Object Position</title>
    <style>
        img {
            width: 300px;
            height: 150px;
            object-fit: cover;
            object-position: top center;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300" alt="Inson yuzi">
</body>
</html>
```

## Tushuntirish va Mantiq:
`object-position: top center` rasmning tepa qismini (masalan, odam boshini) qirqilib ketishidan saqlab, e'tiborni aynan tepaga qaratadi.

## Ishlash natijasi:
```text
Odam boshi to'liq ko'rinadigan qirqilgan to'rtburchak rasm ko'rinadi.
```

---

# 239-Topshiriq: CSS filter: blur va grayscale effektlari
## Topshiriq sharti:
Rasmlarni xiralashtirish va oq-qora rangga o'tkazish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>CSS Filtrlari</title>
    <style>
        body { font-family: sans-serif; display: flex; gap: 20px; padding: 25px; }
        img { width: 180px; border-radius: 6px; }
        .gray { filter: grayscale(100%); }
        .blur { filter: blur(3px); }
    </style>
</head>
<body>
    <img src="https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=200" alt="Oddiy">
    <img src="https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=200" class="gray" alt="Oq-qora">
    <img src="https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=200" class="blur" alt="Xira">
</body>
</html>
```

## Tushuntirish va Mantiq:
`filter: grayscale(100%)` rasmni to'liq retro oq-qora qiladi, `blur(3px)` esa xiralashtiruvchi tuman effektini beradi.

## Ishlash natijasi:
```text
Oddiy, oq-qora va xiralashgan uchta bir xil rasm yonma-yon namoyon bo'ladi.
```

---

# 240-Topshiriq: filter: drop-shadow() va box-shadow farqi
## Topshiriq sharti:
Shaffof fonga ega PNG yoki SVG shaklining o'z konturi bo'yicha soya berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Drop Shadow vs Box Shadow</title>
    <style>
        body { font-family: sans-serif; padding: 30px; display: flex; gap: 40px; }
        .box-sh { box-shadow: 0 10px 15px rgba(0,0,0,0.3); }
        .drop-sh { filter: drop-shadow(0 10px 10px rgba(0,0,0,0.4)); }
    </style>
</head>
<body>
    <div>
        <p>box-shadow (Kvadrat soya beradi):</p>
        <svg width="80" height="80" class="box-sh" viewBox="0 0 100 100"><polygon points="50,10 90,90 10,90" fill="#3b82f6"/></svg>
    </div>
    <div>
        <p>drop-shadow (Uchburchak shakliga mos soya):</p>
        <svg width="80" height="80" class="drop-sh" viewBox="0 0 100 100"><polygon points="50,10 90,90 10,90" fill="#3b82f6"/></svg>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`box-shadow` rasmning tashqi kvadrat chegarasiga soya beradi. `filter: drop-shadow()` esa shaffof joylarni e'tiborsiz qoldirib, faqat haqiqiy chizilgan obyektning o'ziga tabiiy soya tashlaydi.

## Ishlash natijasi:
```text
Birinchi uchburchakning soxta kvadrat soyasi bor, ikkinchi uchburchakning soyasi esa aynan uchburchak shaklida tushadi.
```

---

# 241-Topshiriq: Rasmlar galereyasi setkasi (Photo Grid)
## Topshiriq sharti:
CSS Grid orqali zamonaviy fotogalereya tartibini yasash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Photo Grid</title>
    <style>
        .gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; padding: 20px; }
        .gallery img { width: 100%; height: 200px; object-fit: cover; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="gallery">
        <img src="https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=300">
        <img src="https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?w=300">
        <img src="https://images.unsplash.com/photo-1465146344425-f00d5f5c8f07?w=300">
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`grid-template-columns: repeat(auto-fit, minmax(200px, 1fr))` ekranning kengligiga qarab ustunlar sonini o'zi avtomatik ko'paytirib yoki kamaytirib turadi.

## Ishlash natijasi:
```text
Teng o'lchamdagi chiroyli uchta tabiat manzarasi katakchasi aks etadi.
```

---

# 242-Topshiriq: Zoom-on-hover effekti
## Topshiriq sharti:
Sichqoncha borganda katakdan chiqmasdan kattalashuvchi rasm.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Zoom Hover</title>
    <style>
        .card { width: 300px; height: 200px; overflow: hidden; border-radius: 8px; }
        .card img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease; }
        .card:hover img { transform: scale(1.1); }
    </style>
</head>
<body>
    <div class="card">
        <img src="https://images.unsplash.com/photo-1518791841217-8f162f1e1131?w=400" alt="Mushukcha">
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ota blokdagi `overflow: hidden` rasmni o'z ramkasida ushlab turadi, `transform: scale(1.1)` esa uning ichki maydonini 10% ga silliq kattalashtiradi.

## Ishlash natijasi:
```text
Kursor borganda ramka ichida turgan holda kattalashuvchi rasm effekti chiqadi.
```

---

# 243-Topshiriq: Video fonli qahramon bo'limi (Video Background Hero)
## Topshiriq sharti:
Saytning bosh sahifasida orqa fonda tovushsiz aylanib turuvchi video.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Video Background</title>
    <style>
        .hero { position: relative; height: 350px; overflow: hidden; display: flex; align-items: center; justify-content: center; }
        .hero video { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1; }
        .hero h1 { color: white; font-family: sans-serif; font-size: 36px; text-shadow: 0 2px 8px rgba(0,0,0,0.7); }
    </style>
</head>
<body>
    <div class="hero">
        <video autoplay muted loop playsinline>
            <source src="https://www.w3schools.com/html/mov_bbb.mp4" type="video/mp4">
        </video>
        <h1>Kelajak Texnologiyalari</h1>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`position: absolute; z-index: -1` va `object-fit: cover` videoni orqa fonga to'liq yoyadi. `autoplay muted loop` uni sahifa ochilishi bilanoq shovqinsiz abadiy aylanishini ta'minlaydi.

## Ishlash natijasi:
```text
Orqa fonda video harakatlanib turadi, old qatorda esa yirik oq 'Kelajak Texnologiyalari' sarlavhasi ko'rinadi.
```

---

# 244-Topshiriq: Maxsus stil berilgan mini audio pleyer kartochkasi
## Topshiriq sharti:
Ijrochi rasmi, trek nomi va audio pleyerni birlashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Audio Kartochkasi</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        .player-card { display: flex; align-items: center; gap: 15px; background: #1e293b; padding: 15px; border-radius: 12px; width: fit-content; }
        .player-card img { width: 60px; height: 60px; border-radius: 8px; }
        .track-info { color: white; }
        .track-info h4 { margin: 0 0 4px 0; }
        .track-info p { margin: 0; color: #94a3b8; font-size: 13px; }
    </style>
</head>
<body>
    <div class="player-card">
        <img src="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=100" alt="Albom">
        <div class="track-info">
            <h4>Baxshichilik Ohanglari</h4>
            <p>Milliy Folklor Ansambli</p>
        </div>
        <audio controls style="height: 35px;"><source src="track.mp3" type="audio/mpeg"></audio>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
To'q ko'k rangli kartochka ichida san'atkor surati, uning nomi va brauzer audio boshqaruvi joylashtiriladi.

## Ishlash natijasi:
```text
Spotify uslubidagi ixcham to'q rangli musiqa tinglash vidjeti paydo bo'ladi.
```

---

# 245-Topshiriq: Buzilgan rasm o'rnida chiroyli zaxira (Fallback image)
## Topshiriq sharti:
Rasm internetdan yuklanmay qolsa, sahifa ko'rinishini saqlab qoluvchi CSS.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Fallback Image</title>
    <style>
        img {
            width: 250px;
            height: 150px;
            border-radius: 8px;
            background-color: #f1f5f9;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-family: sans-serif;
            font-size: 13px;
            color: #64748b;
            text-align: center;
        }
    </style>
</head>
<body>
    <!-- Mavjud bo'lmagan rasm manzili -->
    <img src="mavjud_emas.jpg" alt="Tasvir yuklanmadi. Iltimos, internetingizni tekshiring.">
</body>
</html>
```

## Tushuntirish va Mantiq:
Rasm yuklanmasa brauzer uning `alt` matnini ko'rsatadi. CSS dagi `background-color` va `display: inline-flex` buzilgan belgini xunuk qilmasdan, chiroyli axborot qutisiga aylantiradi.

## Ishlash natijasi:
```text
Kulrang to'rtburchak ichida markazda 'Tasvir yuklanmadi...' yozuvi chiqadi.
```

---

# 246-Topshiriq: SVG orqali to'lqinsimon bo'lim ajratgich (Wave separator)
## Topshiriq sharti:
Ikki sahifa bo'limi o'rtasiga chiroyli to'lqin shaklidagi o'tishni yasash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>SVG To'lqin</title>
    <style>
        body { margin: 0; font-family: sans-serif; }
        .section-top { background: #3b82f6; color: white; padding: 40px 20px; text-align: center; }
        .wave-container { line-height: 0; }
        .wave-container svg { width: 100%; height: auto; }
        .section-bottom { background: #ffffff; padding: 40px 20px; }
    </style>
</head>
<body>
    <div class="section-top">
        <h1>Yuqori Moviy Bo'lim</h1>
    </div>
    <div class="wave-container">
        <svg viewBox="0 0 500 150" preserveAspectRatio="none">
            <path d="M0.00,49.98 C150.00,150.00 349.20,-50.00 500.00,49.98 L500.00,0.00 L0.00,0.00 Z" fill="#3b82f6"></path>
        </svg>
    </div>
    <div class="section-bottom">
        <p>Quyi oq rangli bo'lim...</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Vektorli to'lqin egri chizig'i `viewBox` va `preserveAspectRatio='none'` bilan yuqori fon rangiga moslab chiziladi va bo'limlararo suyuq o'tish effektini beradi.

## Ishlash natijasi:
```text
Moviy bo'limdan oq bo'limga silliq to'lqinsimon chiroyli o'tish chizig'i ko'rinadi.
```

---

# 247-Topshiriq: Blur-up (LQIP) sekin yuklanish effekti
## Topshiriq sharti:
Past sifatli xira rasmdan asta-sekin tiniq rasmga o'tish taassuroti.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Blur-up Effect</title>
    <style>
        .lqip-box {
            width: 350px;
            height: 200px;
            background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="10" height="6"><rect width="10" height="6" fill="%2394a3b8"/></svg>');
            background-size: cover;
            filter: blur(8px);
            transition: filter 0.5s ease-out;
            border-radius: 8px;
        }
        .lqip-box:hover { filter: blur(0); }
    </style>
</head>
<body>
    <div class="lqip-box"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Dastlabki past sifatli kichik pikselli fon xiralashtiriladi (`blur`), to'liq rasm yetib kelgach filtr `blur(0)` ga tushirilib tiniqlashtiriladi.

## Ishlash natijasi:
```text
Xiralashgan blok; kursor borganda to'liq tiniq holatga keladi.
```

---

# 248-Topshiriq: 360 darajali mahsulot interaktiv ko'rish piktogrammasi
## Topshiriq sharti:
Rasm burchagida aylanuvchi 3D belgisini joylashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>360 Mahsulot</title>
    <style>
        .product-360 { position: relative; width: 300px; }
        .product-360 img { width: 100%; border-radius: 8px; display: block; }
        .badge-360 {
            position: absolute;
            bottom: 15px;
            right: 15px;
            background: rgba(15, 23, 42, 0.8);
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-family: sans-serif;
            font-size: 13px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="product-360">
        <img src="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300" alt="Quloqchin">
        <div class="badge-360">&#8635; 360&deg; Ko'rish</div>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Kartochkaning o'ng quyi burchagiga `position: absolute` bilan yarim shaffof 360 darajali interaktivlik belgisi qadaladi.

## Ishlash natijasi:
```text
Quloqchin rasmi ustida qora shaffof nishon ichida '360° Ko'rish' yozuvi chiqadi.
```

---

# 249-Topshiriq: Rasm ostidagi matnga gradient soyabon (Gradient Scrim)
## Topshiriq sharti:
Kino afishalari uslubida rasm pastidan tepaga qorayuvchi gradient.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Gradient Scrim</title>
    <style>
        .movie-card {
            position: relative;
            width: 250px;
            height: 350px;
            border-radius: 10px;
            overflow: hidden;
            font-family: sans-serif;
        }
        .movie-card img { width: 100%; height: 100%; object-fit: cover; }
        .scrim {
            position: absolute;
            bottom: 0; left: 0; width: 100%; height: 50%;
            background: linear-gradient(to top, rgba(0,0,0,0.9), transparent);
            display: flex;
            align-items: flex-end;
            padding: 15px;
            box-sizing: border-box;
            color: white;
        }
    </style>
</head>
<body>
    <div class="movie-card">
        <img src="https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=300" alt="Kino afishasi">
        <div class="scrim">
            <div>
                <h3 style="margin:0;">Yulduzlar Jangi</h3>
                <small style="color:#cbd5e1;">Fantastika, Sarguzasht</small>
            </div>
        </div>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`linear-gradient(to top, rgba(0,0,0,0.9), transparent)` pastdan tepaga qarab erib ketuvchi tabiiy qora soya beradi va sarlavhalar mutlaqo aniq ko'rinadi.

## Ishlash natijasi:
```text
Afishaning pastki yarmida qorayib keluvchi gradient ustida oq kino sarlavhasi aks etadi.
```

---

# 250-Topshiriq: To'liq professional multimedia portfeli sahifasi
## Topshiriq sharti:
Rasmlar, video, audio va SVG larni zamonaviy interfeysda birlashtiruvchi to'liq maket.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multimedia Studiyasi</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #f8fafc; padding: 30px 15px; }
        .container { max-width: 900px; margin: 0 auto; }
        h1 { text-align: center; margin-bottom: 30px; color: #38bdf8; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
        .card { background: #1e293b; border-radius: 10px; overflow: hidden; padding: 15px; }
        .card h3 { margin-bottom: 10px; font-size: 18px; }
        img, video { width: 100%; border-radius: 6px; }
        audio { width: 100%; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Milliy Multimedia Studiyasi</h1>
        <div class="grid">
            <div class="card">
                <h3>Video Darslik</h3>
                <video controls poster="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=300">
                    <source src="https://www.w3schools.com/html/mov_bbb.mp4" type="video/mp4">
                </video>
            </div>
            <div class="card">
                <h3>Vektor San'ati (SVG)</h3>
                <svg viewBox="0 0 100 100" style="width:100%; height:180px;">
                    <circle cx="50" cy="50" r="40" fill="#0284c7" />
                    <polygon points="50,20 60,40 80,45 65,60 70,80 50,70 30,80 35,60 20,45 40,40" fill="#facc15" />
                </svg>
            </div>
            <div class="card">
                <h3>Podkast Epizodi</h3>
                <img src="https://images.unsplash.com/photo-1478737270239-2f02b77fc618?w=300" style="height:140px; object-fit:cover;">
                <audio controls><source src="https://www.w3schools.com/html/horse.mp3" type="audio/mpeg"></audio>
            </div>
        </div>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu yakuniy andoza zamonaviy multimedia standartlarining (video pleyer posteri bilan, sof inline SVG vektorli grafikasi, responsiv rasm va audio pleyer) barchasini to'q rangli (dark mode) nafis dizaynda uyg'unlashtiradi.

## Ishlash natijasi:
```text
To'q qora fonda uchta kartochkali zamonaviy multimedia galereyasi: chapda video, o'rtada yulduzli SVG illyustratsiya, o'ngda esa rasm va podkast audio pleyeri chiqadi.
```

---

