# Matn Stili va Tipografika (451-500)

# 451-Topshiriq: text-align turlari: left, right, center, justify
## Topshiriq sharti:
Matnni to'rt xil yo'nalishda tekislash usullarini namoyish eting.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Text Align</title>
    <style>
        body { font-family: sans-serif; padding: 25px; line-height: 1.6; }
        .left { text-align: left; background: #f8fafc; padding: 10px; margin-bottom: 8px; }
        .center { text-align: center; background: #eff6ff; padding: 10px; margin-bottom: 8px; }
        .right { text-align: right; background: #fef2f2; padding: 10px; margin-bottom: 8px; }
        .justify { text-align: justify; background: #f0fdf4; padding: 10px; width: 300px; }
    </style>
</head>
<body>
    <div class="left">Chapga tekislangan matn</div>
    <div class="center">Markazga tekislangan matn</div>
    <div class="right">O'ngga tekislangan matn</div>
    <div class="justify">Ikki tomonga tekislangan (justify) matn xuddi gazeta va kitoblardagidek qator bo'yicha so'zlar orasidagi probellarni teng taqsimlaydi.</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`text-align` blok ichidagi inline elementlar va matn oqimini gorizontal yo'naltiradi. `justify` kitobiy format bo'lib, har ikki chetni qat'iy tekis chiziqqa keltiradi.

## Ishlash natijasi:
```text
To'rt xil rangli fonlarda mos ravishda chap, markaz, o'ng va ikki tomonga tekislangan xatboshilar ko'rinadi.
```

---

# 452-Topshiriq: text-align-last xususiyati
## Topshiriq sharti:
Justify qilingan matnning eng oxirgi tugovchi qatorini tekislash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Text Align Last</title>
    <style>
        .article {
            width: 320px;
            text-align: justify;
            text-align-last: center;
            background: #f1f5f9;
            padding: 15px;
            border-radius: 6px;
        }
    </style>
</head>
<body>
    <p class="article">
        Dasturlash olamida kod yozish nafaqat texnik jarayon, balki ijodiy tafakkur hamdir. Ushbu xatboshining oxirgi qatori markazda turadi.
    </p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`text-align-last: center` matnning oxirgi qisqa satrini markazga joylashtiradi va qatorning xunuk cho'zilib ketishining oldini oladi.

## Ishlash natijasi:
```text
Matn to'liq tekis, lekin uning eng so'nggi jumlasi markazda joylashgan holda chiqadi.
```

---

# 453-Topshiriq: text-decoration-line turlari: underline, overline, line-through
## Topshiriq sharti:
Matn tagiga, ustiga yoki o'rtasiga chiziq tortish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Text Decoration Line</title>
    <style>
        body { font-family: sans-serif; padding: 25px; line-height: 2; font-size: 18px; }
        .under { text-decoration-line: underline; }
        .over { text-decoration-line: overline; }
        .through { text-decoration-line: line-through; }
    </style>
</head>
<body>
    <p class="under">Tagiga chizilgan (underline)</p>
    <p class="over">Tepasiga chizilgan (overline)</p>
    <p class="through">O'rtasidan chizilgan (line-through)</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`text-decoration-line` chiziqning qayerdan o'tishini belgilaydi. Bitta qatorda bir nechta qiymat (masalan `underline overline`) berish ham mumkin.

## Ishlash natijasi:
```text
Uch xil chiziq chizilgan matnlar ketma-ketligi ko'rinadi.
```

---

# 454-Topshiriq: text-decoration-color va text-decoration-style
## Topshiriq sharti:
To'lqinsimon, nuqtali va rangli chiziqlar tortish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Decoration Style</title>
    <style>
        body { font-family: sans-serif; padding: 25px; font-size: 18px; }
        .wavy-red {
            text-decoration-line: underline;
            text-decoration-style: wavy;
            text-decoration-color: #ef4444;
        }
    </style>
</head>
<body>
    <p>Matndagi <span class="wavy-red">imloviy xato</span> so'zlar tagiga to'lqin chiziladi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`wavy` to'lqinli qizil chiziq chizib, matn muharrirlaridagi grammatik xato taassurotini uyg'otadi.

## Ishlash natijasi:
```text
'imloviy xato' so'zi ostida qizil to'lqinsimon chiziq aks etadi.
```

---

# 455-Topshiriq: text-decoration-thickness va text-underline-offset
## Topshiriq sharti:
Chiziq qalinligi va uning harflardan qochish masofasini sozlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Underline Offset</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        .custom-link {
            font-size: 22px;
            color: #0f172a;
            text-decoration: underline;
            text-decoration-color: #3b82f6;
            text-decoration-thickness: 3px;
            text-underline-offset: 6px;
        }
    </style>
</head>
<body>
    <a href="#" class="custom-link">Nafis Ajratilgan Havola</a>
</body>
</html>
```

## Tushuntirish va Mantiq:
`text-underline-offset: 6px` chiziqni harflarning 'p', 'g', 'y' kabi dumlari ustiga tushib xunuk bo'lib qolmasligi uchun pastroqqa suradi, `thickness: 3px` esa unga qalinlik beradi.

## Ishlash natijasi:
```text
Moviy qalin chizig'i harflardan 6px pastda nafis turgan zamonaviy havola chiqadi.
```

---

# 456-Topshiriq: letter-spacing bilan harflar oralig'ini sozlash
## Topshiriq sharti:
Sarlavhalarga jiddiylik va estetika berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Letter Spacing</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .luxury {
            font-size: 20px;
            text-transform: uppercase;
            letter-spacing: 6px;
            color: #1e3a8a;
            font-weight: 700;
        }
    </style>
</head>
<body>
    <div class="luxury">PREMIUM BREND</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`letter-spacing: 6px` harflar orasiga masofa qo'shib, premium brendlar va logotiplarga xos nafis kengaytirilgan tipografika hosil qiladi.

## Ishlash natijasi:
```text
Harflari bir-biridan 6px oraliqda turgan, katta bosh harflarda yozilgan hashamatli yozuv chiqadi.
```

---

# 457-Topshiriq: word-spacing bilan so'zlar orasini kengaytirish
## Topshiriq sharti:
So'zlar o'rtasidagi bo'shliqni boshqarish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Word Spacing</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .wide-words { word-spacing: 8px; font-size: 18px; }
    </style>
</head>
<body>
    <p class="wide-words">Har bir so'z orasida keng oraliq mavjud.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`word-spacing: 8px` har bir so'z o'rtasidagi probel hajmiga 8px qo'shadi.

## Ishlash natijasi:
```text
So'zlari bir-biridan sezilarli uzoqda turgan matn ko'rinadi.
```

---

# 458-Topshiriq: text-transform: uppercase, lowercase, capitalize
## Topshiriq sharti:
Harflarning katta-kichikligini avtomatik o'zgartirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Text Transform</title>
    <style>
        body { font-family: sans-serif; padding: 25px; line-height: 2; }
        .upper { text-transform: uppercase; }
        .lower { text-transform: lowercase; }
        .cap { text-transform: capitalize; }
    </style>
</head>
<body>
    <div class="upper">barcha harflar katta bo'ladi</div>
    <div class="lower">BARCHA HARFLAR KICHIK BO'LADI</div>
    <div class="cap">har bir so'z bosh harf bilan boshlanadi</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`text-transform` HTML kodidagi matnga tegmasdan uni CSS orqali BOSH HARFLARGA, kichik harflarga yoki Har Bir So'zni Katta Harfli qilib o'zgartiradi.

## Ishlash natijasi:
```text
Uch xil registrda qayta formatlangan matnlar ko'rinadi.
```

---

# 459-Topshiriq: text-indent bilan qizil qator (Abzas) tashlash
## Topshiriq sharti:
Kitob va maqolalarda xatboshi boshini ichkariga surish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Text Indent</title>
    <style>
        body { font-family: Georgia, serif; padding: 30px; line-height: 1.8; max-width: 600px; }
        p { text-indent: 35px; margin: 0; }
    </style>
</head>
<body>
    <p>O'zbek xalqining boy madaniy merosi va asriy an'analari milliy o'zligimizning mustahkam tayanchidir.</p>
    <p>Har bir yangi xatboshi kitoblardagidek 35 pikselli qizil qator bilan boshlanadi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`text-indent: 35px` faqat birinchi satrning boshlanishini o'ngga suradi, qolgan barcha satrlar esa normal chap tekislikda davom etadi.

## Ishlash natijasi:
```text
Klassik kitobdagidek har bir xatboshisi o'ngga surilib boshlanuvchi matn chiqadi.
```

---

# 460-Topshiriq: white-space xususiyatlari: nowrap, pre, pre-wrap
## Topshiriq sharti:
Probel va yangi satrlarni saqlash yoki yangi qatorga tushishni taqiqlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>White Space</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .nowrap { white-space: nowrap; width: 200px; border: 1px solid red; overflow: hidden; }
        .pre-wrap { white-space: pre-wrap; background: #f1f5f9; padding: 10px; }
    </style>
</head>
<body>
    <p class="nowrap">Ushbu matn hech qachon yangi qatorga tushmaydi!</p>
    <div class="pre-wrap">HTML ichida qoldirilgan
        barcha bo'shliqlar     va enterlar
    saqlanib qoladi.</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`nowrap` matnni yagona satrda ushlab turadi. `pre-wrap` esa `<pre>` tegisiz ham barcha bo'shliqlarni saqlaydi va qutiga yetganda o'zidan o'zi yangi qatorga ko'chadi.

## Ishlash natijasi:
```text
Biri bitta qatorda siqilgan, ikkinchisi probellari saqlangan ikkita blok chiqadi.
```

---

# 461-Topshiriq: word-break va overflow-wrap (Uzun so'zlarni sindirish)
## Topshiriq sharti:
Uzun URL manzillar qutidan chiqib ketmasligi uchun ularni kuch bilan sindirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Word Break</title>
    <style>
        .box {
            width: 180px;
            border: 2px solid #3b82f6;
            padding: 10px;
            overflow-wrap: break-word;
            word-break: break-all;
        }
    </style>
</head>
<body>
    <div class="box">
        https://kun.uz/news/2026/06/15/juda-uzun-maqola-manzili-ramkadan-chiqmasin
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`word-break: break-all` juda uzun so'z yoki URL manzilni harflar orasidan sindirib yangi satrga tushiradi va konteyner kengligini buzilishdan qutqaradi.

## Ishlash natijasi:
```text
Tor ko'k quti ichiga to'liq sig'dirib sindirilgan uzun havola ko'rinadi.
```

---

# 462-Topshiriq: hyphens: auto bilan o'zbek tilida chiziqcha bilan bo'g'inlash
## Topshiriq sharti:
So'zlar oxiriga defis (-) qo'yib bo'g'inlab ko'chirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Hyphens</title>
    <style>
        .hyphen-box {
            width: 150px;
            text-align: justify;
            hyphens: auto;
            border: 1px solid #94a3b8;
            padding: 10px;
        }
    </style>
</head>
<body>
    <div class="hyphen-box" lang="uz">
        O'zbekistonda raqamlashtirish jarayonlari jadal sur'atlarda rivojlanmoqda.
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`hyphens: auto` brauzerning ichki lug'ati asosida uzun so'zlarni tabiiy ravishda bo'g'inlarga ajratib chiziqcha qo'yadi.

## Ishlash natijasi:
```text
Tor qutida so'zlar qator oxirida chiziqcha bilan chiroyli bo'linib tushadi.
```

---

# 463-Topshiriq: text-shadow asoslari
## Topshiriq sharti:
Matn ortiga gorizontal, vertikal va xira soya tashlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Text Shadow</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        .shadow-text {
            font-size: 32px;
            font-weight: bold;
            color: #1e3a8a;
            /* X: 2px, Y: 4px, Blur: 6px, Color */
            text-shadow: 2px 4px 6px rgba(0, 0, 0, 0.25);
        }
    </style>
</head>
<body>
    <div class="shadow-text">Soyali Sarlavha</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`text-shadow: 2px 4px 6px rgba(0,0,0,0.25)` matnning orqasiga yumshoq soya berib, uning fondan ajralib turishini ta'minlaydi.

## Ishlash natijasi:
```text
To'q ko'k harflar ortida tabiiy soya ko'rinadi.
```

---

# 464-Topshiriq: 3D matn effekti (Qatlamli text-shadow)
## Topshiriq sharti:
Bir nechta soyalarni 1 pikselli qadam bilan terib hajmdor harflar yasash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>3D Matn</title>
    <style>
        body { background: #3b82f6; padding: 40px; font-family: sans-serif; }
        .three-d {
            font-size: 44px;
            font-weight: 900;
            color: white;
            text-shadow:
                0 1px 0 #1d4ed8,
                0 2px 0 #1d4ed8,
                0 3px 0 #1d4ed8,
                0 4px 0 #1d4ed8,
                0 5px 10px rgba(0,0,0,0.3);
        }
    </style>
</head>
<body>
    <div class="three-d">3D HAJMDOR MATN</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Bir necha qavatli qoramtir soyalar yordamida harflarning qalin yon qirralari chiziladi va haqiqiy plastmassadan yasalgan 3D harflar effekti hosil bo'ladi.

## Ishlash natijasi:
```text
Moviy fonda bo'rtib turgan qalin oq 3D harflar gavdalanadi.
```

---

# 465-Topshiriq: writing-mode: vertical-rl (Vertikal matn)
## Topshiriq sharti:
Matnni yuqoridan pastga qarab vertikal ustun ko'rinishida yozish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Writing Mode</title>
    <style>
        .vert-badge {
            writing-mode: vertical-rl;
            text-orientation: mixed;
            background: #0f172a;
            color: white;
            padding: 20px 10px;
            font-family: sans-serif;
            font-weight: bold;
            letter-spacing: 2px;
            border-radius: 6px;
            width: fit-content;
        }
    </style>
</head>
<body>
    <div class="vert-badge">2026-KOLLEKSIYA</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`writing-mode: vertical-rl` matn oqimini 90 darajaga buradi va sharqiy Osiyo yozuvlari yoki zamonaviy plakat uslubidagi vertikal yozuvlarni hosil qiladi.

## Ishlash natijasi:
```text
To'q qora tasmada vertikal yozilgan oq harflar paydo bo'ladi.
```

---

# 466-Topshiriq: Ko'p ustunli matn: column-count va column-gap
## Topshiriq sharti:
Gazetalardagi kabi matnni bir nechta parallel ustunlarga avtomatik bo'lish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>CSS Columns</title>
    <style>
        .newspaper {
            column-count: 3;
            column-gap: 30px;
            font-family: 'Times New Roman', serif;
            line-height: 1.7;
            text-align: justify;
        }
    </style>
</head>
<body>
    <div class="newspaper">
        O'zbekiston axborot texnologiyalari sohasida ulkan marralarni zabt etmoqda. Yoshlar dasturlash va innovatsion loyihalar yaratishda faol ishtirok etmoqda. Ta'lim tizimida ham xalqaro standartlar joriy etilib, yangi avlod muhandislari yetishib chiqmoqda.
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`column-count: 3` matnni JavaScript ishlatmasdan avtomatik ravishda teng 3 ta ustunga taqsimlaydi va o'qish qulayligini oshiradi.

## Ishlash natijasi:
```text
Klassik gazeta uslubida uch ustunga ajratilgan qulay matn chiqadi.
```

---

# 467-Topshiriq: column-rule bilan ustunlar orasiga chiziq tortish
## Topshiriq sharti:
Ustunlar orasida estetik vertikal ajratuvchi chegara o'rnatish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Column Rule</title>
    <style>
        .news-rule {
            column-count: 2;
            column-gap: 40px;
            column-rule: 2px solid #cbd5e1;
            font-family: Georgia, serif;
            line-height: 1.8;
        }
    </style>
</head>
<body>
    <div class="news-rule">
        Birinchi ustun mazmuni bu yerda joylashadi va u tugagach matn avtomatik ravishda ikkinchi ustunga o'tib ketadi. Oraliqda esa chiroyli kulrang chiziq turadi.
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`column-rule: 2px solid #cbd5e1` xuddi `border` kabi ustunlar orasidagi bo'shliqning qoq o'rtasiga vertikal ajratuvchi chiziq tortadi.

## Ishlash natijasi:
```text
Ikki ustun orasida nafis kulrang vertikal chiziq ko'rinadi.
```

---

# 468-Topshiriq: column-span: all bilan sarlavhani barcha ustunlar ustiga yoyish
## Topshiriq sharti:
Sarlavha ustunlarni ikkiga bo'lmasdan ularning barchasini qamrab olishi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Column Span</title>
    <style>
        .layout { column-count: 2; column-gap: 30px; font-family: sans-serif; }
        .full-span { column-span: all; text-align: center; color: #1e3a8a; margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class="layout">
        <h2 class="full-span">Barcha Ustunlarni Qamrovchi Sarlavha</h2>
        <p>Chap ustundagi matn oqimi davom etadi...</p>
        <p>O'ng ustundagi matn oqimi davom etadi...</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`column-span: all` sarlavhaga ko'p ustunli setkani yorib o'tib butun kenglik bo'yicha yoyilishga imkon beradi.

## Ishlash natijasi:
```text
Sarlavha tepada to'liq eni egallaydi, uning ostidagi matn esa 2 ustunga bo'linadi.
```

---

# 469-Topshiriq: user-select: none bilan nusxa olishni boshqarish
## Topshiriq sharti:
Tugmalar va piktogrammalarni adashib belgilanib qolishdan himoya qilish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>User Select</title>
    <style>
        .no-select { user-select: none; background: #e2e8f0; padding: 10px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="no-select">Ushbu tugma matnini sichqoncha bilan belgilab (ko'kartirib) bo'lmaydi.</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`user-select: none` tugmalar bir necha marta tez-tez bosilganda matnning ko'k bo'lib tanlanib ketishini to'xtatadi va ilovalarga xos tabiiy tajriba beradi.

## Ishlash natijasi:
```text
Sichqoncha bilan ustidan tortilganda ham belgilanmaydigan blok.
```

---

# 470-Topshiriq: caret-color bilan kursor rangini o'zgartirish
## Topshiriq sharti:
Matn kiritish katagidagi miltillovchi vertikal tayoqcha rangini sozlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Caret Color</title>
    <style>
        input {
            padding: 10px;
            font-size: 18px;
            caret-color: #ef4444; /* Qizil kursor */
            border: 2px solid #cbd5e1;
            border-radius: 6px;
        }
    </style>
</head>
<body>
    <input type="text" placeholder="Yozing...">
</body>
</html>
```

## Tushuntirish va Mantiq:
`caret-color: #ef4444` standart qora miltillovchi kursorni brend rangiga (masalan yorqin qizil) moslaydi.

## Ishlash natijasi:
```text
Katakka bosilganda qizil rangli kursor miltillab turadi.
```

---

# 471-Topshiriq: Katta harfli tarixiy sarlavhalar (letter-spacing va small-caps)
## Topshiriq sharti:
Muzeylar va tarixiy asarlar uslubidagi hashamatli sarlavha.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Trajan Tipografika</title>
    <style>
        .monumental {
            font-family: 'Times New Roman', serif;
            letter-spacing: 5px;
            font-variant: small-caps;
            font-size: 26px;
            color: #78350f;
            text-align: center;
            border-top: 1px solid #78350f;
            border-bottom: 1px solid #78350f;
            padding: 10px 0;
            width: 400px;
            margin: 20px auto;
        }
    </style>
</head>
<body>
    <div class="monumental">Amir Temur Saltanati</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Kengaytirilgan harflar oralig'i va `small-caps` qadimiy toshbitiklarga xos ulug'vor sarlavha dizaynini beradi.

## Ishlash natijasi:
```text
Tepa va pastida nafis jigar chiziqlari bor, harflari keng terilgan hashamatli tarixiy sarlavha ko'rinadi.
```

---

# 472-Topshiriq: Narxlar tipografikasi (Valyuta belgisi kichik, son katta)
## Topshiriq sharti:
Foydalanuvchi nigohini eng muhim songa qaratuvchi tipografik uslub.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Narx Tipografikasi</title>
    <style>
        .price-badge { font-family: sans-serif; display: flex; align-items: baseline; color: #16a34a; }
        .currency { font-size: 16px; font-weight: 500; margin-left: 4px; }
        .value { font-size: 36px; font-weight: 900; }
    </style>
</head>
<body>
    <div class="price-badge">
        <span class="value">499 000</span>
        <span class="currency">UZS / oy</span>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`align-items: baseline` son va kichik valyuta yozuvini bir tekis pastki tayanch chizig'ida ushlab turadi.

## Ishlash natijasi:
```text
Ulkan 36px yashil son va uning pastki chizig'iga to'g'rilangan kichikroq 'UZS / oy' yozuvi chiqadi.
```

---

# 473-Topshiriq: Matn ichidagi emojilarni mukammal tekislash (vertical-align)
## Topshiriq sharti:
Harflar va piktogrammalar bir qatorda chiroyli markazlashishi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Emoji Alignment</title>
    <style>
        body { font-family: sans-serif; padding: 25px; font-size: 20px; }
        .icon { display: inline-block; vertical-align: -3px; }
    </style>
</head>
<body>
    <p>Xush kelibsiz <span class="icon">🚀</span> Yangi marralar sari!</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`vertical-align: -3px` emojini qatorning yuqorisiga osilib qolmasdan matnning markazi bilan bir chiziqda turishini ta'minlaydi.

## Ishlash natijasi:
```text
Raketa emojisi matn harflari bilan bir tekis joylashgan xatboshi chiqadi.
```

---

# 474-Topshiriq: Yozuv mashinkasi (Typewriter) animatsiyasi
## Topshiriq sharti:
Harflar birma-bir yozilib borayotgandek ko'rinuvchi mashhur effekt.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Typewriter</title>
    <style>
        .typewriter {
            font-family: monospace;
            font-size: 24px;
            white-space: nowrap;
            overflow: hidden;
            border-right: 3px solid #2563eb;
            width: 20ch; /* 20 ta belgi */
            animation: typing 3s steps(20), blink 0.5s step-end infinite alternate;
        }
        @keyframes typing { from { width: 0; } }
        @keyframes blink { 50% { border-color: transparent; } }
    </style>
</head>
<body>
    <div class="typewriter">Salom, kelajak bu yerda!</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`ch` (belgi kengligi) va `steps(20)` orqali matn xuddi yozuv mashinkasidagi kabi bosqichma-bosqich chop etiladi, miltillovchi kursor esa effektni to'ldiradi.

## Ishlash natijasi:
```text
Harflari birma-bir yozilib ochiladigan va o'ng tomonida ko'k kursor miltillovchi animatsion yozuv paydo bo'ladi.
```

---

# 475-Topshiriq: Glitch (Kiber xato) matn effekti
## Topshiriq sharti:
Qizil va ko'k ranglar siljishi bilan kiberpank illyuziyasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Glitch Effect</title>
    <style>
        body { background: #000; padding: 40px; }
        .glitch {
            color: white;
            font-size: 32px;
            font-weight: bold;
            font-family: monospace;
            text-shadow: -2px 0 #ef4444, 2px 0 #06b6d4;
        }
    </style>
</head>
<body>
    <div class="glitch">TIZIMDA NOSOZLIK (GLITCH)</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Chapga qizil soya, o'ngga zangori ko'k soya berilib 3D ko'zoynaklardagi kabi kiber-nosozlik taassuroti yasaladi.

## Ishlash natijasi:
```text
Qora fonda qizil va moviy ranglari biroz surilgan g'ayritabiiy kiber matn ko'rinadi.
```

---

# 476-Topshiriq: Matn ostiga ikkita parallel chiziq tortish
## Topshiriq sharti:
text-decoration-style: double bilan rasmiy xalqaro andoza.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Double Underline</title>
    <style>
        .total {
            font-size: 24px;
            font-weight: bold;
            text-decoration: underline double #2563eb;
            text-underline-offset: 5px;
        }
    </style>
</head>
<body>
    <div class="total">Yakuniy Balans: 15 000 000 UZS</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`underline double` ikkita parallel chiroyli chiziq tortadi va moliya jadvallaridagi yakuniy qatorlar uchun ayni muddao.

## Ishlash natijasi:
```text
Tagida ikkita ko'k chizig'i bor qalin moliyaviy yozuv chiqadi.
```

---

# 477-Topshiriq: Har bir so'zning birinchi harfini alohida bezash
## Topshiriq sharti:
Akronimlar yoki shiorlar uchun bosh harflarni yorqin rangda chiqarish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Acronym Styling</title>
    <style>
        body { font-family: sans-serif; padding: 25px; font-size: 22px; }
        .motto span { color: #2563eb; font-weight: bold; font-size: 28px; }
    </style>
</head>
<body>
    <div class="motto"><span>I</span>lm <span>T</span>afakkur <span>P</span>oydevoridir</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
So'z boshidagi harflar `<span>` bilan olinib kattalashtiriladi va qalinlashtiriladi.

## Ishlash natijasi:
```text
'I', 'T', 'P' harflari ko'k va katta bo'lib ajralib turadi.
```

---

# 478-Topshiriq: Suyuq tipografika: clamp(1rem, 2.5vw, 2rem)
## Topshiriq sharti:
Ekran kattalashgan sari o'z-o'zidan kattalashuvchi o'lchovsiz sarlavha.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fluid Typography</title>
    <style>
        h1 {
            font-size: clamp(1.5rem, 4vw, 3rem);
            color: #0f172a;
            font-family: sans-serif;
            text-align: center;
        }
    </style>
</head>
<body>
    <h1>Moslashuvchan Suyuq Sarlavha</h1>
</body>
</html>
```

## Tushuntirish va Mantiq:
`clamp(1.5rem, 4vw, 3rem)` media querylarsiz telefonlarda 24px, planshetlarda 35px, monitorlarda esa aniq 48px bo'lib erkin oqadi.

## Ishlash natijasi:
```text
Brauzer darchasi toraytirilsa sarlavha bir tekis kichrayadi, kengaytirilsa kattalashadi.
```

---

# 479-Topshiriq: break-inside: avoid bilan blokning bo'linib ketishini to'xtatish
## Topshiriq sharti:
Ko'p ustunli maqolalarda kartochka yoki iqtibos ikkiga yorilib ketmasligini ta'minlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Break Inside Avoid</title>
    <style>
        .multi-col { column-count: 2; column-gap: 20px; }
        .quote-card {
            break-inside: avoid;
            background: #f1f5f9;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="multi-col">
        <p>Matnlar...</p>
        <div class="quote-card">Ushbu kartochka birinchi ustun tugasa ham ikkiga bo'linmay, butun holda ikkinchi ustunga ko'chadi.</div>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`break-inside: avoid` ko'p ustunli jurnallarda rasmlar va muhim xabarlarning yarmisi birinchi ustunda, yarmisi ikkinchisida qolib ketishining oldini oladi.

## Ishlash natijasi:
```text
Butunligi saqlangan toza kartochka ko'rinadi.
```

---

# 480-Topshiriq: To'liq professional jurnalistik editorial maqola andozasi
## Topshiriq sharti:
Lead paragraph, ko'p ustunlar, drop cap, iqtiboslar, chiziqlar va mukammal tipografikani jamlagan shablon.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jurnalistika Tipografikasi</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Georgia', serif; background: #fffdf9; color: #1c1917; padding: 40px 20px; line-height: 1.8; }
        article { max-width: 820px; margin: 0 auto; }
        h1 { font-size: clamp(2rem, 5vw, 3rem); line-height: 1.15; letter-spacing: -0.01em; margin-bottom: 15px; text-align: center; }
        .meta-byline { text-align: center; font-style: italic; color: #78716c; margin-bottom: 30px; font-size: 15px; }
        .lead-text { font-size: 20px; line-height: 1.6; font-weight: 500; color: #44403c; margin-bottom: 25px; text-align: justify; }
        .article-columns { column-count: 2; column-gap: 35px; column-rule: 1px solid #e7e5e4; text-align: justify; }
        .article-columns p { margin-bottom: 20px; }
        .article-columns p:first-of-type::first-letter { font-size: 3.8em; float: left; line-height: 0.8; margin-right: 8px; color: #991b1b; font-weight: bold; }
        blockquote { column-span: all; border-top: 2px solid #1c1917; border-bottom: 2px solid #1c1917; padding: 15px 0; margin: 25px 0; font-size: 22px; text-align: center; font-style: italic; }
    </style>
</head>
<body>
    <article>
        <h1>Yangi Asrning Buyuk Kiber Uyg'onishi</h1>
        <div class="meta-byline">Muallif: Rustam Saidov &bull; Toshkent, 2026-yil</div>
        <p class="lead-text">
            Texnologiya va insoniyat uyg'unligi bugun har qachongidan ham dolzarb ahamiyat kasb etmoqda. Sun'iy intellekt va milliy qadriyatlar kesishgan nuqtada yangi intellektual poydevor qurilmoqda.
        </p>
        <div class="article-columns">
            <p>
                Tarixdan ma'lumki, har bir ilm-fan to'lqini o'z davrining eng ilg'or uslublarini talab qilgan. Bugungi dasturchilar nafaqat kod yozmoqda, balki kelajak sivilizatsiyasining raqamli poydevorini shakllantirmoqda.
            </p>
            <blockquote>
                "Haqiqiy taraqqiyot — bu bilimning insonparvarlik bilan birlashuvidir."
            </blockquote>
            <p>
                Raqamli olamda o'zbek tilining nufuzini oshirish, boy korpuslar va milliy sun'iy intellekt modellarini yaratish har birimizning oldimizda turgan eng sharafli vazifadir.
            </p>
        </div>
    </article>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu yakuniy andoza dunyoning eng mashhur gazeta va jurnallari (The New York Times, The Atlantic) andozalarini o'zida mujassam etgan oliy toifali tipografik durdonadir.

## Ishlash natijasi:
```text
Markazlashgan ulkan sarlavha, qizil rangli ulkan bosh harf (Drop Cap) bilan boshlanuvchi 2 ustunli gazeta matni va o'rtasida qora parallel chiziqlar bilan ajratilgan ifodali iqtibos chiqadi.
```

---

# 481-Topshiriq: Matnga gradient fon quyish
## Topshiriq sharti:
-webkit-background-clip va gradient orqali jilolangan matn.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Gradient Matn</title>
    <style>
        .grad-title {
            font-size: 36px;
            font-weight: 800;
            background: linear-gradient(90deg, #2563eb, #10b981);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
</head>
<body>
    <h1 class="grad-title">Ko'kdan Yashilga Gradient Matn</h1>
</body>
</html>
```

## Tushuntirish va Mantiq:
`-webkit-background-clip: text` va `-webkit-text-fill-color: transparent` birgalikda matnning o'zini rang-barang gradient bo'yog'iga aylantiradi.

## Ishlash natijasi:
```text
Ko'kdan yashilga o'tuvchi yaltiroq gradientli sarlavha namoyon bo'ladi.
```

---

# 482-Topshiriq: tab-size bilan Tab probellari sonini boshqarish
## Topshiriq sharti:
Kod bloklarida Tab tugmasi 4 ta yoki 2 ta bo'shliq bo'lishini sozlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Tab Size</title>
    <style>
        pre { tab-size: 2; font-family: monospace; background: #f1f5f9; padding: 15px; }
    </style>
</head>
<body>
    <pre><code>function test() {
	return true; // 2 ta probel kengligidagi tab
}</code></pre>
</body>
</html>
```

## Tushuntirish va Mantiq:
`tab-size: 2` standart keng 8 pikselli xunuk tab o'rniga zamonaviy 2 ta probelli ixcham tab kengligini o'rnatadi.

## Ishlash natijasi:
```text
Toza 2 probelli oraliqqa ega monospaced kod bloki ko'rinadi.
```

---

# 483-Topshiriq: font-feature-settings: 'tnum' (Tabular numbers)
## Topshiriq sharti:
Jadval raqamlarining bir xil eni bo'ylab qatorlashishini ta'minlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Tabular Numbers</title>
    <style>
        .mono-nums { font-feature-settings: "tnum"; font-variant-numeric: tabular-nums; font-family: sans-serif; font-size: 20px; }
    </style>
</head>
<body>
    <div class="mono-nums">111,111 UZS</div>
    <div class="mono-nums">888,888 UZS</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`tabular-nums` barcha raqamlarning kengligini tenglaydi (1 soni 8 soni bilan bir xil en egallaydi). Bu moliyaviy hisobotlarda sonlarning ostma-ost toza turishi uchun muhim.

## Ishlash natijasi:
```text
Har bir raqami qoq bir-birining tagiga tushgan ikkita summa chiqadi.
```

---

# 484-Topshiriq: &shy; (Soft Hyphen) bilan yashirin bo'g'inlash
## Topshiriq sharti:
Faqat satr sig'magandagina ochiladigan yashirin chiziqcha.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Soft Hyphen</title>
    <style>
        .box { width: 120px; border: 1px solid #ccc; padding: 10px; }
    </style>
</head>
<body>
    <div class="box">
        Trans&shy;for&shy;mat&shy;siya
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`&shy;` belgisi ekranda ko'rinmaydi. Lekin so'z tor konteyner chegarasiga yetganda, brauzer aynan shu yashirin nuqtadan so'zni bo'g'inlab defis bilan pastga tushiradi.

## Ishlash natijasi:
```text
Tor qutida 'Trans-' va 'formatsiya' bo'lib chiziqcha bilan ajralgan so'z ko'rinadi.
```

---

# 485-Topshiriq: CSS bilan Marquee (yuguruvchi satr) animatsiyasi
## Topshiriq sharti:
Eski tegsiz toza zamonaviy CSS yuguruvchi matn tasmasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>CSS Marquee</title>
    <style>
        .marquee-wrap { width: 300px; overflow: hidden; background: #0f172a; color: #facc15; padding: 8px 0; }
        .marquee-content { display: inline-block; white-space: nowrap; animation: scrollLeft 6s linear infinite; }
        @keyframes scrollLeft { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    </style>
</head>
<body>
    <div class="marquee-wrap">
        <div class="marquee-content">★ DIQQAT: YANGI KURS BOSHLANDI ★</div>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Toza CSS `transform: translateX()` orqali eski `<marquee>` tegidan xalos bo'lib barcha qurilmalarda silliq yuguruvchi e'lonlar lentasi hosil qilinadi.

## Ishlash natijasi:
```text
Qora tasmada o'ngdan chapga qarab yugurib o'tuvchi sariq harflar paydo bo'ladi.
```

---

# 486-Topshiriq: Matn ichidagi havolalarni to'lqinsimon chiziq bilan bezash
## Topshiriq sharti:
hover paytida to'lqin rangini o'zgartirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Wavy Hover Link</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .wavy-link {
            color: #2563eb;
            text-decoration: underline wavy #93c5fd 2px;
            text-underline-offset: 4px;
            transition: text-decoration-color 0.2s;
        }
        .wavy-link:hover { text-decoration-color: #2563eb; }
    </style>
</head>
<body>
    <p>Batafsil ma'lumot olish uchun <a href="#" class="wavy-link">rasmiy portalga</a> o'ting.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`text-decoration: underline wavy #93c5fd 2px` och moviy to'lqin chizadi, hover bo'lganda to'lqin quyuq ko'k rangga aylanadi.

## Ishlash natijasi:
```text
Tagida nafis to'lqini bor, kursor borganda to'q ko'karuvchi havola chiqadi.
```

---

# 487-Topshiriq: Bo'rtib chiqqan (Embossed) matn effekti
## Topshiriq sharti:
Oq va to'q soyalarning kesishishi bilan toshga o'yilgan matn illyuziyasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Embossed Text</title>
    <style>
        body { background: #cbd5e1; padding: 40px; font-family: sans-serif; }
        .embossed {
            font-size: 36px;
            font-weight: 800;
            color: #cbd5e1;
            text-shadow:
                -1px -1px 1px #ffffff,
                1px 1px 1px #64748b;
        }
    </style>
</head>
<body>
    <div class="embossed">O'YILGAN BO'RTMA MATN</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Matn rangi fon bilan bir xil qilinadi, tepasiga oq nur, pastiga esa to'q kulrang soya berilganda matn sirtga bo'rtib chiqqandek ko'rinadi.

## Ishlash natijasi:
```text
Kulrang fondan qabariq bo'lib o'yib chiqarilgandek ko'rinuvchi harflar ko'rinadi.
```

---

# 488-Topshiriq: Debossed (Ichkariga botgan) matn effekti
## Topshiriq sharti:
Soyalarni teskarisiga burib sirt ichiga bosilgan harflar.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Debossed Text</title>
    <style>
        body { background: #94a3b8; padding: 40px; font-family: sans-serif; }
        .debossed {
            font-size: 36px;
            font-weight: 800;
            color: #64748b;
            text-shadow:
                0 1px 1px rgba(255,255,255,0.6),
                0 -1px 1px rgba(0,0,0,0.6);
        }
    </style>
</head>
<body>
    <div class="debossed">ICHKARIGA BOTGAN MATN</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Pastki qismiga oq nur, yuqori qismiga esa qora soya berilganda harflar metall plastinka ichiga bosib tushirilgandek taassurot qoldiradi.

## Ishlash natijasi:
```text
Kulrang metall sirt ichiga muhrlangandek botib turgan matn ko'rinadi.
```

---

# 489-Topshiriq: ::selection da neon yashil nur berish
## Topshiriq sharti:
Matn tanlanganda kiberpank yashil nurlanish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Neon Selection</title>
    <style>
        body { background: #111; color: #eee; font-family: sans-serif; padding: 30px; }
        p::selection {
            background: #22c55e;
            color: #000;
            text-shadow: 0 0 8px #4ade80;
        }
    </style>
</head>
<body>
    <p>Ushbu qorong'u sahifadagi matnni sichqoncha bilan belgilab ko'ring!</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Tanlangan matnga yashil fon va neon text-shadow berilib interaktiv jilo yaratiladi.

## Ishlash natijasi:
```text
Sichqoncha bilan belgilanganda matn yashil neon nur bilan porlaydi.
```

---

# 490-Topshiriq: text-transform: capitalize xususiyatining nozik jihatlari
## Topshiriq sharti:
Har bir so'zning bosh harfini avtomatik bosh harfga aylantirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Capitalize</title>
    <style>
        .book-title { text-transform: capitalize; font-family: Georgia, serif; font-size: 20px; color: #1e3a8a; }
    </style>
</head>
<body>
    <div class="book-title">o'zbekistonning yangi taraqqiyot strategiyasi</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`capitalize` so'zlarning har birining birinchi harfini avtomatik bosh harf qiladi. Kitob nomlari va rasmiy sarlavhalar uchun juda qo'l keladi.

## Ishlash natijasi:
```text
'O'zbekistonning Yangi Taraqqiyot Strategiyasi' shaklida bosh harflar bilan chiqadi.
```

---

# 491-Topshiriq: font-style: normal orqali <em> va <i> ni to'g'rilash
## Topshiriq sharti:
Semantik urg'uni saqlab qiyalikni bekor qilish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Reset Italic</title>
    <style>
        em.upright { font-style: normal; color: #dc2626; font-weight: bold; }
    </style>
</head>
<body>
    <p>Bu matnda <em class="upright">muhim so'z</em> qiya emas, tik va qizil bo'lib turadi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Semantik jihatdan `<em>` qoladi, ammo vizual jihatdan `font-style: normal` bilan uning qiyaligi yo'qotiladi.

## Ishlash natijasi:
```text
Qiya bo'lmagan, lekin qizil va qalin semantik urg'uli so'z aks etadi.
```

---

# 492-Topshiriq: line-height ni shrift o'lchami bilan bir xil qilish (Vertikal markazlash)
## Topshiriq sharti:
Bitta qatorli tugma yoki nishon ichidagi matnni vertikal markazlashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Line Height Centering</title>
    <style>
        .badge {
            height: 36px;
            line-height: 36px;
            background: #2563eb;
            color: white;
            padding: 0 16px;
            border-radius: 18px;
            display: inline-block;
            font-family: sans-serif;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="badge">Mukammal Markazlashgan</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Agar elementning balandligi `36px` bo'lsa va `line-height: 36px` berilsa, bitta satrli matn flexboxsiz ham qoq vertikal markazga tushadi.

## Ishlash natijasi:
```text
Ichidagi matni vertikal qoq o'rtada turgan ko'k oval tugmacha ko'rinadi.
```

---

# 493-Topshiriq: white-space: pre-line bilan ortiqcha probellarni yutish
## Topshiriq sharti:
Yangi satrlarni (Enter) saqlab, ortiqcha probellarni bitta probelga aylantirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Pre Line</title>
    <style>
        .cleaned { white-space: pre-line; background: #f8fafc; padding: 15px; border: 1px solid #cbd5e1; }
    </style>
</head>
<body>
    <div class="cleaned">
        1-Satr:     ko'p    probellar     bitta bo'ladi.
        2-Satr: lekin yangi satrga tushish saqlanadi!
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`white-space: pre-line` foydalanuvchi qoldirgan `Enter` larni saqlaydi, lekin xatolik bilan ketgan 5-10 ta ortiqcha probellarni tozalaydi.

## Ishlash natijasi:
```text
Ikki qatorda tartibli turgan, ortiqcha probellari tozalangan xatboshilar chiqadi.
```

---

# 494-Topshiriq: Matn qirralarini chizish (-webkit-text-stroke)
## Topshiriq sharti:
Harflarning ichini bo'sh qoldirib faqat tashqi konturini bo'yash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Text Stroke</title>
    <style>
        .outline-text {
            font-size: 48px;
            font-weight: 900;
            font-family: sans-serif;
            color: transparent;
            -webkit-text-stroke: 2px #2563eb;
        }
    </style>
</head>
<body>
    <div class="outline-text">FAAQAT KONTUR</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`-webkit-text-stroke: 2px #2563eb` va `color: transparent` harflarning ichini shaffof qilib faqat ko'k konturini qoldiradi.

## Ishlash natijasi:
```text
Ichi bo'sh, faqat 2px lik ko'k chiziq bilan chizilgan ulkan zamonaviy harflar chiqadi.
```

---

# 495-Topshiriq: Matn ustidagi yulduzchali litsenziya eslatmasi
## Topshiriq sharti:
sup va tipografik qoidalar bilan rasmiy eslatma berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Footnote Callout</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        sup.ref { color: #dc2626; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <p>O'zbekistonning IT xizmatlari eksporti rekord darajaga yetdi<sup class="ref">[1]</sup>.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Akademik maqolalarda manbaga havola beruvchi qizil indeks qulay va tushunarli formatlanadi.

## Ishlash natijasi:
```text
Matn oxirida kichik qizil '[1]' raqamli ko'rsatkich paydo bo'ladi.
```

---

# 496-Topshiriq: Ko'p tilli aralash matnda font-family tanlash
## Topshiriq sharti:
Lotin, kirill va emojilar uchun turli shriftlar kaskadini belgilash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Multi Script Font</title>
    <style>
        p {
            font-family: 'Helvetica Neue', 'Arial', 'Apple Color Emoji', 'Segoe UI Emoji', sans-serif;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <p>Salom O'zbekiston! 🎉 100% Sifat кафолати.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Agar birinchi shriftda emojilar bo'lmasa, brauzer avtomatik ravishda navbatdagi 'Apple Color Emoji' shriftidan foydalanadi.

## Ishlash natijasi:
```text
Barcha harflar va emojilar xatosiz uyg'unlashgan go'zal qator ko'rinadi.
```

---

# 497-Topshiriq: column-fill: balance xususiyati
## Topshiriq sharti:
Ustunlar bo'ylab matn teng balandlikda to'lishini ta'minlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Column Fill</title>
    <style>
        .balanced {
            column-count: 2;
            column-fill: balance;
            height: 150px;
            border: 1px solid #cbd5e1;
            padding: 10px;
        }
    </style>
</head>
<body>
    <div class="balanced">
        Ushbu matn ikkala ustunga teng taqsimlanadi, biri to'lib ikkinchisi bo'sh qolmaydi.
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`column-fill: balance` ikkala ustunning pastki chegarasini bir xil tekis balandlikda muvozanatlaydi.

## Ishlash natijasi:
```text
Konteyner ichida teng ikkiga bo'lingan matn ustunlari ko'rinadi.
```

---

# 498-Topshiriq: Matn ostiga marker chizig'i berish (background-size bilan)
## Topshiriq sharti:
Kursor kelganda chapdan o'ngga qarab to'ladigan sarg'ish flomaster effekti.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Marker Transition</title>
    <style>
        body { font-family: sans-serif; padding: 30px; font-size: 22px; }
        .pen-mark {
            background-image: linear-gradient(#fde047, #fde047);
            background-repeat: no-repeat;
            background-position: 0 100%;
            background-size: 0% 40%;
            transition: background-size 0.3s ease;
            cursor: pointer;
        }
        .pen-mark:hover { background-size: 100% 40%; }
    </style>
</head>
<body>
    <p>Muhim fikr: <span class="pen-mark">har bir narsani puxta o'rganing</span> va davom eting.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Hover bo'lganda `background-size: 100% 40%` ga o'tib, matn tagiga sarg'ish marker chizig'i jonlanadi.

## Ishlash natijasi:
```text
Kursor borganda matn tagiga sariq flomaster chizig'i mayin to'lib boradi.
```

---

# 499-Topshiriq: Matnning birinchi harfini aylanaga olish (Initial Circle)
## Topshiriq sharti:
Xatboshi ilk harfini doiraviy fon bilan bezash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Initial Circle</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        p.circle-drop::first-letter {
            float: left;
            font-size: 28px;
            font-weight: bold;
            background: #2563eb;
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-right: 12px;
            line-height: 50px;
            text-align: center;
        }
    </style>
</head>
<body>
    <p class="circle-drop">Dasturlash kasbi bugun har bir sohani o'zgartirib yangi imkoniyatlar yaratmoqda.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`::first-letter` va `border-radius: 50%` bilan harf ko'k dumaloq medal ichida markazlashib ko'rinadi.

## Ishlash natijasi:
```text
Boshidagi 'D' harfi ko'k aylanma nishon ichida oq bo'lib ajralib turadi.
```

---

# 500-Topshiriq: To'liq professional matn va tipografika tahririyat shabloni
## Topshiriq sharti:
Barcha tipografik qoidalarni jamlagan tayyor akademik va axborot maqolasi andozasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mukammal Tipografika</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Georgia', serif; background: #fafaf9; color: #292524; padding: 50px 20px; line-height: 1.8; }
        article { max-width: 760px; margin: 0 auto; background: white; padding: 45px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.04); }
        h1 { font-family: -apple-system, sans-serif; font-size: 2.25rem; font-weight: 800; line-height: 1.2; color: #0c0a09; margin-bottom: 12px; letter-spacing: -0.02em; }
        .meta { font-family: sans-serif; font-size: 13px; color: #78716c; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 25px; border-bottom: 1px solid #e7e5e4; padding-bottom: 12px; }
        .lead { font-size: 1.2rem; line-height: 1.6; color: #44403c; margin-bottom: 20px; }
        p { font-size: 1.05rem; margin-bottom: 18px; text-align: justify; }
        blockquote { border-left: 3px solid #2563eb; padding-left: 20px; margin: 25px 0; font-style: italic; color: #44403c; }
    </style>
</head>
<body>
    <article>
        <h1>Zamonaviy Vebda Matn Madaniyati va Tipografika</h1>
        <div class="meta">Chop etildi: 2026-YIL &bull; 5 DAQIQALIK MUTOLAA</div>
        <p class="lead">Inson axborotni qabul qilishida tipografikaning aniqligi va shriftlar mutanosibligi hal qiluvchi ahamiyatga egadir.</p>
        <p>To'g'ri tanlangan qator balandligi (1.8) va o'qish uchun mos matn kengligi (760px) foydalanuvchini charchatmasdan o'qish jarayonini maroqli qiladi.</p>
        <blockquote>"Tipografika — bu so'zlarning vizual ovozidir."</blockquote>
    </article>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu yakuniy andoza matn dizaynining eng oliy mezonlarini o'zida mujassam etgan mukammal tahririyat shablonidir.

## Ishlash natijasi:
```text
Oq toza qog'oz formatidagi, ko'zga nihoyatda yoqimli serif matnli professional maqola sahifasi ko'rinadi.
```

---

