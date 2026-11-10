# Ranglar, Fonlar va Shriftlar (351-400)

# 351-Topshiriq: Nomlangan ranglar (Named colors) va ularning chegaralari
## Topshiriq sharti:
Brauzerda 140 dan ortiq inglizcha nomlangan ranglar (red, teal, coral) namoyishi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Nomlangan Ranglar</title>
    <style>
        body { font-family: sans-serif; display: flex; gap: 10px; padding: 25px; }
        .swatch { padding: 15px 20px; color: white; border-radius: 6px; font-weight: bold; }
        .teal { background-color: teal; }
        .coral { background-color: coral; }
        .gold { background-color: gold; color: black; }
    </style>
</head>
<body>
    <div class="swatch teal">Teal</div>
    <div class="swatch coral">Coral</div>
    <div class="swatch gold">Gold</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
HTML/CSS da `teal`, `coral`, `gold` kabi nomlar qulay bo'lsa-da, ular professional dizaynda cheklangan (atigi 140 ta) bo'lganligi bois zamonaviy vebda HEX, RGB va HSL modellari qo'llaniladi.

## Ishlash natijasi:
```text
Uchta rangli to'rtburchak: yashil-moviy (teal), shaftolirang (coral) va tilla (gold) ko'rinadi.
```

---

# 352-Topshiriq: HEX rang modeli (#rrggbb)
## Topshiriq sharti:
O'n oltilik sanoq tizimidagi qizil, yashil va ko'k ranglar kombinatsiyasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>HEX Ranglar</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .card { background-color: #1e3a8a; color: #ffffff; padding: 20px; border-radius: 8px; }
        .accent { color: #f59e0b; }
    </style>
</head>
<body>
    <div class="card">
        <h2>HEX Ranglar Tizimi</h2>
        <p>Asosiy to'q ko'k: <span class="accent">#1e3a8a</span>, yorqin sariq: <span class="accent">#f59e0b</span></p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
HEX formati har biri 00 dan FF gacha (0 dan 255 gacha) bo'lgan uchta kanalni ifodalaydi: `#RR` (qizil), `GG` (yashil), `BB` (ko'k). Jami 16.7 milliondan ortiq turli xil rang hosil qiladi.

## Ishlash natijasi:
```text
To'q ko'k fonda sariq aksentli matn aks etadi.
```

---

# 353-Topshiriq: 8-belgili HEX (#rrggbbaa) bilan shaffoflik
## Topshiriq sharti:
HEX kodining oxirgi ikki belgisi orqali alfa-kanal shaffofligini o'rnatish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>8-Digit HEX</title>
    <style>
        body { background: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=400'); padding: 40px; font-family: sans-serif; }
        .glass { background-color: #ffffff80; /* 50% shaffof oq */ padding: 25px; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="glass">
        <h3>50% Shaffof HEX (#ffffff80)</h3>
        <p>Orqa fondagi manzara qisman ko'rinib turadi.</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`#ffffff80` dagi `80` o'n oltilikda 128 ga (255 ning 50% iga) teng bo'lib, oq rangga 50% shaffoflik (alpha) beradi.

## Ishlash natijasi:
```text
Rasm ustida orqasi xira ko'rinib turuvchi oq shaffof kartochka paydo bo'ladi.
```

---

# 354-Topshiriq: RGB rang modeli: rgb(red, green, blue)
## Topshiriq sharti:
0 dan 255 gacha bo'lgan fizik piksellar rang aralashmasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>RGB Modeli</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .box { background-color: rgb(37, 99, 235); color: rgb(255, 255, 255); padding: 15px; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="box">rgb(37, 99, 235) — Aniq Moviy Rang</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`rgb(37, 99, 235)` kompyuter monitorlarining qizil, yashil va ko'k diodlarining intensivlik darajasini 0-255 oralig'ida aniq belgilaydi.

## Ishlash natijasi:
```text
Yorqin moviy fonda oq matn ko'rinadi.
```

---

# 355-Topshiriq: Zamonaviy RGB sintaksisi: rgb(r g b / alpha)
## Topshiriq sharti:
Vergulsiz yangi CSS Color Module 4 standarti.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Modern RGB</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .modern-box {
            background-color: rgb(15 23 42 / 75%); /* 75% qorayish */
            color: white;
            padding: 20px;
            border-radius: 6px;
        }
    </style>
</head>
<body>
    <div class="modern-box">Zamonaviy Vergulsiz Sintaksis: rgb(15 23 42 / 75%)</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Yangi standartda parametrlar vergulsiz bo'shliq bilan ajratiladi, alfa kanali esa qiyshiq chiziq (`/ 75%`) bilan qo'shiladi.

## Ishlash natijasi:
```text
To'q qora-moviy rangli 75% shaffoflikka ega nafis blok chiqadi.
```

---

# 356-Topshiriq: HSL rang modeli: Hue, Saturation, Lightness
## Topshiriq sharti:
Inson ko'zi uchun eng tushunarli rang formati.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>HSL Modeli</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .hsl-box {
            background-color: hsl(210, 100%, 50%); /* 210 gradus - moviy */
            color: white;
            padding: 20px;
            border-radius: 6px;
        }
    </style>
</head>
<body>
    <div class="hsl-box">hsl(210, 100%, 50%) — Ideal Moviy</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Hue (0-360 gradus rang doirasi), Saturation (0-100% to'yinganlik) va Lightness (0% qora, 100% oq, 50% sof rang). Dizaynerlar uchun rang tusini o'zgartirish HSL da juda oson.

## Ishlash natijasi:
```text
Moviy rangdagi yorqin to'rtburchak namoyon bo'ladi.
```

---

# 357-Topshiriq: Zamonaviy HSL formati: hsl(h s l / a)
## Topshiriq sharti:
Shaffoflik biriktirilgan yangi HSL sintaksisi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Modern HSL</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .box { background-color: hsl(142 71% 45% / 0.8); color: white; padding: 15px; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="box">hsl(142 71% 45% / 0.8) — 80% Zangori Yashil</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Zamonaviy HSL sintaksisida ham vergullar o'rniga probel va slesh (`/ 0.8`) ishlatiladi.

## Ishlash natijasi:
```text
Chiroyli yashil yarim shaffof blok ko'rinadi.
```

---

# 358-Topshiriq: Ranglar uyg'unligi (Monoxrom va Komplementar)
## Topshiriq sharti:
HSL orqali qarama-qarshi (180 gradus) uyg'un ranglar juftligini yasash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Komplementar Ranglar</title>
    <style>
        body { font-family: sans-serif; padding: 25px; display: flex; gap: 15px; }
        .base { background: hsl(200, 90%, 40%); color: white; padding: 20px; border-radius: 6px; }
        .comp { background: hsl(20, 90%, 50%); color: white; padding: 20px; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="base">Asosiy Rang (200°)</div>
    <div class="comp">Qarama-qarshi Komplementar (200 - 180 = 20°)</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Rang g'ildiragida 180 daraja qarama-qarshi turgan ranglar (masalan, moviy 200° va to'q sariq 20°) bir-birini mukammal to'ldiradi va yuqori kontrast beradi.

## Ishlash natijasi:
```text
Moviy va to'q sariq rangli bir-biriga juda yarashgan ikkita blok chiqadi.
```

---

# 359-Topshiriq: currentColor kalit so'zining kuchi
## Topshiriq sharti:
Element hoshiyasi va piktogrammasini matn rangiga bog'lash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>CurrentColor</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .badge {
            color: #7c3aed;
            border: 2px solid currentColor;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <span class="badge">Rang o'zgarsa, hoshiya ham o'zgaradi</span>
</body>
</html>
```

## Tushuntirish va Mantiq:
`border: 2px solid currentColor;` hoshiya rangini har doim matn rangi (`color`) bilan bir xil qiladi. Bitta rangni o'zgartirish bilan butun komponent o'zgaradi.

## Ishlash natijasi:
```text
Siyohrang matn va aynan shu rangdagi siyohrang hoshiya ko'rinadi.
```

---

# 360-Topshiriq: opacity xususiyati va uning bolalarga ta'siri
## Topshiriq sharti:
Butun element va uning ichidagi barcha matnlarni xiralashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Opacity</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .faded { opacity: 0.5; background: #000; color: #fff; padding: 20px; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="faded">
        <p>DIQQAT: opacity nafaqat fonni, balki matnni ham yarim shaffof qilib qo'yadi!</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`opacity: 0.5` butun vizual daraxtga ta'sir qiladi. Agar faqat fon shaffof bo'lib, matn 100% tiniq qolishi kerak bo'lsa, opacity emas, `rgba()` ishlatilishi shart.

## Ishlash natijasi:
```text
Matni ham, foni ham 50% xiralashgan qora blok chiqadi.
```

---

# 361-Topshiriq: opacity va rgba() fon shaffofligi farqi
## Topshiriq sharti:
Matn ravshanligini saqlagan holda faqat fonni shaffof qilish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Opacity vs RGBA</title>
    <style>
        body { background: #3b82f6; font-family: sans-serif; padding: 30px; display: flex; gap: 20px; }
        .box-opacity { opacity: 0.5; background: white; padding: 20px; border-radius: 6px; }
        .box-rgba { background: rgba(255, 255, 255, 0.5); padding: 20px; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="box-opacity"><strong>Opacity:</strong> Matn ham xira</div>
    <div class="box-rgba"><strong>RGBA:</strong> Matn 100% tiniq</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
RGBA foni orqa fonni ko'rsatib tursa-da, ichidagi matn to'liq 100% to'yingan holda saqlanib o'qish qulayligini buzmaydi.

## Ishlash natijasi:
```text
Moviy fonda biri matni xiralashgan, ikkinchisi matni to'liq qora va tiniq bo'lgan ikkita oq quti ko'rinadi.
```

---

# 362-Topshiriq: background-color asosiy fon rangi
## Topshiriq sharti:
Sahifa yoki blok uchun qattiq toza fon berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Background Color</title>
    <style>
        body { background-color: #f1f5f9; padding: 30px; font-family: sans-serif; }
        .card { background-color: #ffffff; padding: 25px; border-radius: 8px; border: 1px solid #e2e8f0; }
    </style>
</head>
<body>
    <div class="card">Oq Fonli Kartochka</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`background-color` har qanday elementning eng pastki qatlamiga tekis rang beradi.

## Ishlash natijasi:
```text
Och kulrang sahifa fonida oppoq toza kartochka ko'rinadi.
```

---

# 363-Topshiriq: background-image bilan rasm joylashtirish
## Topshiriq sharti:
CSS orqali blok orqasiga rasm qo'yish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Background Image</title>
    <style>
        .banner {
            width: 400px;
            height: 200px;
            background-image: url('https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=400');
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="banner"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`background-image: url('...')` blok orqasiga tasvir o'rnatadi. U HTML dagi `<img>` dan farqli o'laroq sof dekorativ element sanaladi.

## Ishlash natijasi:
```text
Gradient rang-barang abstrakt rasm foni bilan to'ldirilgan blok chiqadi.
```

---

# 364-Topshiriq: background-repeat xususiyatlari
## Topshiriq sharti:
Rasmning plitkasimon takrorlanishini to'xtatish yoki boshqarish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Background Repeat</title>
    <style>
        .box {
            width: 300px;
            height: 150px;
            border: 1px solid #cbd5e1;
            background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30"><circle cx="15" cy="15" r="10" fill="%233b82f6"/></svg>');
            background-repeat: no-repeat;
        }
    </style>
</head>
<body>
    <div class="box"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Sukut bo'yicha rasm butun blok bo'ylab takrorlanadi (repeat). `no-repeat` uni faqat bir marta ko'rsatishni buyuradi.

## Ishlash natijasi:
```text
To'rtburchakning faqat yuqori chap burchagida bitta moviy doira turadi, takrorlanmaydi.
```

---

# 365-Topshiriq: background-position orqali rasmni tekislash
## Topshiriq sharti:
Fon tasvirini blokning qoq o'rtasiga yoki burchaklariga joylashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Background Position</title>
    <style>
        .center-bg {
            width: 300px;
            height: 150px;
            border: 2px dashed #94a3b8;
            background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40"><rect width="40" height="40" fill="%23ef4444"/></svg>');
            background-repeat: no-repeat;
            background-position: center center;
        }
    </style>
</head>
<body>
    <div class="center-bg"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`background-position: center center` rasmning markazini blok markaziga to'g'rilaydi. Shuningdek `top right`, `50% 50%` yoki piksellarda berish mumkin.

## Ishlash natijasi:
```text
Qizil kvadrat fon rasmi blokning qoq markazida joylashadi.
```

---

# 366-Topshiriq: background-size: cover va contain
## Topshiriq sharti:
Fon rasmining butun maydonni qoplashi yoki to'liq sig'ishi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Background Size</title>
    <style>
        .hero-cover {
            width: 100%;
            height: 250px;
            background-image: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800');
            background-size: cover;
            background-position: center;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="hero-cover"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`background-size: cover` tasvir proporsiyasini saqlagan holda butun maydonni 100% bo'shliqlarsiz qoplaydi va zamonaviy bannerlarning asosiy xususiyatidir.

## Ishlash natijasi:
```text
Ekran bo'ylab to'liq qoplagan chiroyli tabiat manzarasi chiqadi.
```

---

# 367-Topshiriq: background-attachment: fixed (Parallaks effekti)
## Topshiriq sharti:
Sahifa aylantirilganda orqa fon rasmining qimirlamay qotib turishi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Parallax Effect</title>
    <style>
        body { margin: 0; font-family: sans-serif; }
        .parallax {
            height: 300px;
            background-image: url('https://images.unsplash.com/photo-1519681393784-d120267933ba?w=800');
            background-attachment: fixed;
            background-size: cover;
            background-position: center;
        }
        .content { height: 800px; padding: 30px; background: white; }
    </style>
</head>
<body>
    <div class="parallax"></div>
    <div class="content">Sahifani pastga aylantiring: fon ekranda qotib turadi!</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`background-attachment: fixed` rasmni brauzer viewport darchasiga qotirib qo'yadi, kontent esa uning ustidan sirpanib o'tadi.

## Ishlash natijasi:
```text
Sahifa varaqlanganda tog'lar manzarasi oynadek qotib turadi, matn uning ustidan oqib o'tadi.
```

---

# 368-Topshiriq: background-clip: text bilan matnga rasm quyish
## Topshiriq sharti:
Matn harflari ichiga gradient yoki rasm joylashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Text Clip</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        .clip-text {
            font-size: 48px;
            font-weight: 900;
            background: linear-gradient(45deg, #f43f5e, #fbbf24);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
</head>
<body>
    <h1 class="clip-text">ZAMONAVIY VEB DIZAYN</h1>
</body>
</html>
```

## Tushuntirish va Mantiq:
`-webkit-background-clip: text` fonni faqat harflar konturi ichida ko'rinadigan qiladi, matn rangini `transparent` qilish esa fonning ko'rinishiga yo'l ochadi.

## Ishlash natijasi:
```text
Qizildan tillarang sariqqa o'tuvchi gradient bilan bo'yalgan ulkan jozibador sarlavha ko'rinadi.
```

---

# 369-Topshiriq: linear-gradient() chiziqli gradient
## Topshiriq sharti:
Ikki yoki undan ortiq ranglarning burchak bo'yicha silliq o'tishi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Linear Gradient</title>
    <style>
        .grad {
            width: 350px;
            height: 150px;
            background: linear-gradient(135deg, #6366f1, #ec4899);
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="grad"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`linear-gradient(135deg, rang1, rang2)` 135 daraja burchak ostida binafshadan och pushti rangga silliq oqib o'tuvchi zamonaviy fon yaratadi.

## Ishlash natijasi:
```text
Binafsha-pushti gradientli chiroyli to'rtburchak chiqadi.
```

---

# 370-Topshiriq: To'xtash nuqtalari bilan ko'p rangli gradient (Color stops)
## Topshiriq sharti:
Gradient ranglarining aniq foizlarda uchrashishi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Color Stops</title>
    <style>
        .uz-flag {
            width: 300px;
            height: 150px;
            background: linear-gradient(to bottom, #0099b5 33%, #ce1126 33%, #ce1126 35%, #ffffff 35%, #ffffff 65%, #ce1126 65%, #ce1126 67%, #1eb53a 67%);
            border: 1px solid #ccc;
        }
    </style>
</head>
<body>
    <div class="uz-flag"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Rang to'xtash nuqtalari bir xil foizda berilsa (`33%, 33%`), ranglar orasida xiralashish bo'lmaydi, keskin toza chegarali chiziqlar (O'zbekiston bayrog'i kabi) hosil bo'ladi.

## Ishlash natijasi:
```text
Moviy, oq va yashil chiziqli qizil hoshiyali bayroq andozasi paydo bo'ladi.
```

---

# 371-Topshiriq: radial-gradient() aylanma gradient
## Topshiriq sharti:
Markazdan chetga qarab tarqaluvchi dumaloq nur effekti.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Radial Gradient</title>
    <style>
        .radial {
            width: 300px;
            height: 200px;
            background: radial-gradient(circle at center, #60a5fa, #1e3a8a);
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="radial"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`radial-gradient(circle at center, ...)` markazdan chetlarga qarab quyosh nuri kabi yoyiluvchi yorug'lik effektini yaratadi.

## Ishlash natijasi:
```text
O'rtasi yorug' moviy, chekkalari to'q ko'k bo'lgan 3D sferik taassurot qoldiruvchi fon ko'rinadi.
```

---

# 372-Topshiriq: conic-gradient() konussimon gradient
## Topshiriq sharti:
Ranglar g'ildiragi va doiraviy diagrammalar (Pie Chart) foni.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Conic Gradient</title>
    <style>
        .pie {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: conic-gradient(#3b82f6 0% 70%, #ef4444 70% 100%);
        }
    </style>
</head>
<body>
    <div class="pie"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`conic-gradient` markaz atrofida 360 daraja aylanib rang tarqatadi. 0% dan 70% gacha ko'k, 70% dan 100% gacha qizil berilib sof CSS pie-chart yasaladi.

## Ishlash natijasi:
```text
70% ko'k va 30% qizil bo'lgan mukammal doiraviy diagramma chiqadi.
```

---

# 373-Topshiriq: repeating-linear-gradient() takrorlanuvchi chiziqlar
## Topshiriq sharti:
Zebra chiziqlari yoki ogohlantiruvchi qora-sariq tasmalar.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Repeating Gradient</title>
    <style>
        .stripes {
            width: 300px;
            height: 60px;
            background: repeating-linear-gradient(45deg, #facc15, #facc15 15px, #000 15px, #000 30px);
            border-radius: 6px;
        }
    </style>
</head>
<body>
    <div class="stripes"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Belgilangan piksellarda to'xtovsiz takrorlanuvchi gradient orqali teksturali naqshlar yasaladi.

## Ishlash natijasi:
```text
Ogohlantiruvchi qora va sariq qiya chiziqlardan iborat lenta hosil bo'ladi.
```

---

# 374-Topshiriq: Bir nechta fonlarni qatlamlash (Multiple backgrounds)
## Topshiriq sharti:
Bitta elementga bir vaqtning o'zida gradient va rasmni ustma-ust qo'yish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Multiple Backgrounds</title>
    <style>
        .multi-bg {
            width: 400px;
            height: 200px;
            border-radius: 8px;
            background:
                linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
                url('https://images.unsplash.com/photo-1518770660439-4636190af475?w=400');
            background-size: cover;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-family: sans-serif;
            font-size: 22px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="multi-bg">Texnologik Kelajak</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Vergul bilan ajratilgan birinchi fon tepada, ikkinchisi pastda yotadi. Qoraytiruvchi gradient to'g'ridan-to'g'ri rasm ustiga qatlamlanadi.

## Ishlash natijasi:
```text
Qoraytirilgan rasm ustida oq rangli sarlavha jilolanadi.
```

---

# 375-Topshiriq: font-family va zaxira steki (Font stack)
## Topshiriq sharti:
Asosiy shrift bo'lmaganda zaxira tizim shriftlariga avtomatik o'tish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Font Stack</title>
    <style>
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            padding: 25px;
        }
    </style>
</head>
<body>
    <p>Agar foydalanuvchida 'Inter' bo'lmasa, Apple Safari da San Francisco, Windows da esa Segoe UI ishlatiladi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Shriftlar chapdan o'ngga qarab tekshiriladi. Ro'yxat oxirida har doim umumiy oila nomi (`sans-serif` yoki `serif`) turishi kafolat beradi.

## Ishlash natijasi:
```text
Qurilmaning eng yuqori sifatli tizim shriftida chiroyli matn chiqadi.
```

---

# 376-Topshiriq: rem o'lchov birligi va a11y afzalligi
## Topshiriq sharti:
Ildiz html o'lchamiga bog'langan moslashuvchan tipografika.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Rem Birligi</title>
    <style>
        html { font-size: 16px; /* 1rem = 16px */ }
        h1 { font-size: 2rem; /* 32px */ }
        p { font-size: 1.125rem; /* 18px */ }
    </style>
</head>
<body>
    <h1>2rem Sarlavha</h1>
    <p>Foydalanuvchi brauzer sozlamalarida shriftni kattalashtirsa, barcha rem birliklari avtomatik proporsional kattalashadi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`rem` (root em) ildiz `<html>` shrift o'lchamiga tayanadi. Piksellardan (px) farqli ravishda u ko'rishida nuqsoni bor odamlar brauzer shriftini kattalashtirganda butun saytni moslashtirib beradi.

## Ishlash natijasi:
```text
Proporsional aniq o'lchamdagi sarlavha va matn ko'rinadi.
```

---

# 377-Topshiriq: font-weight raqamli qalinliklari (100 dan 900 gacha)
## Topshiriq sharti:
Ingichkadan qolingacha bo'lgan qat'iy standartlar.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Font Weight</title>
    <style>
        body { font-family: sans-serif; padding: 20px; line-height: 1.8; }
        .w300 { font-weight: 300; }
        .w400 { font-weight: 400; }
        .w700 { font-weight: 700; }
        .w900 { font-weight: 900; }
    </style>
</head>
<body>
    <div class="w300">Light (300) - Mayin ingichka</div>
    <div class="w400">Regular (400) - Standart matn</div>
    <div class="w700">Bold (700) - Qalin sarlavha</div>
    <div class="w900">Black (900) - O'ta qalin</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`400` normal matnga, `700` bold ga teng. Raqamli qiymatlar orqali zamonaviy shriftlarning nozik qalinlik pog'onalarini aniq sozlash mumkin.

## Ishlash natijasi:
```text
To'rt xil qalinlikdagi matnlar qatori chiqadi.
```

---

# 378-Topshiriq: line-height birliksiz nisbati
## Topshiriq sharti:
O'qish uchun eng qulay qator oralig'i (1.5 - 1.6).

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Line Height</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .tight { line-height: 1.1; margin-bottom: 20px; }
        .ideal { line-height: 1.6; }
    </style>
</head>
<body>
    <p class="tight"><strong>Zich (1.1):</strong> Qatorlar bir-biriga juda yaqin joylashgan bo'lib, uzun matnlarni o'qishda inson ko'zini charchatadi va adashtiradi.</p>
    <p class="ideal"><strong>Ideal (1.6):</strong> Har bir satr orasida havo bor, o'qilishi nihoyatda yengil va xalqaro veb mezonlariga to'la mos keladi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`line-height: 1.6` ga piksel yozmaslik tavsiya etiladi. Birliksiz ko'paytiruvchi berilsa, shrift kattalashganda qator oralig'i ham avtomatik proporsional kengayadi.

## Ishlash natijasi:
```text
Biri qatorlari yopishgan, ikkinchisi qulay keng qatorli ikkita qiyosiy xatboshi aks etadi.
```

---

# 379-Topshiriq: @font-face qoidasi bilan lokal WOFF2 shriftini ulash
## Topshiriq sharti:
O'z shaxsiy shrift fayllarini serverdan yuklab ishlatish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Font Face</title>
    <style>
        @font-face {
            font-family: 'MeningShriftim';
            src: url('fonts/custom.woff2') format('woff2'),
                 url('fonts/custom.woff') format('woff');
            font-weight: normal;
            font-style: normal;
            font-display: swap;
        }
        body { font-family: 'MeningShriftim', sans-serif; padding: 25px; }
    </style>
</head>
<body>
    <p>Ushbu sahifa serverdan yuklangan xavfsiz va siqilgan WOFF2 formatidagi maxsus shriftda ishlamoqda.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`WOFF2` (Web Open Font Format 2) zamonaviy vebning eng ixcham va tezkor formatidir. `font-display: swap` esa shrift fayli yuklanguncha matnni zaxira shriftda ko'rsatib turishga ruxsat beradi.

## Ishlash natijasi:
```text
Maxsus ulangan korporativ shrift bilan matn render bo'ladi.
```

---

# 380-Topshiriq: Google Fonts integratsiyasi
## Topshiriq sharti:
Google platformasidan bepul shriftlarni yuklashning eng tezkor usuli.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap" rel="stylesheet">
    <title>Google Fonts</title>
    <style>
        body { font-family: 'Poppins', sans-serif; padding: 30px; }
        h1 { font-weight: 800; color: #1e3a8a; }
    </style>
</head>
<body>
    <h1>Poppins Shriftida Sarlavha</h1>
    <p>Preconnect teglari Google serverlari bilan SSL aloqasini oldindan o'rnatib yuklanishni tezlashtiradi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`preconnect` teglari DNS qidiruvi va TLS muzokaralarini tezlashtiradi, `display=swap` esa sahifaning darhol ochilishini ta'minlaydi.

## Ishlash natijasi:
```text
Chiroyli dumaloq shaklli zamonaviy Poppins shriftida sarlavha va matn ko'rinadi.
```

---

# 381-Topshiriq: Glassmorphism effekti (backdrop-filter: blur)
## Topshiriq sharti:
Muzlagan yarim shaffof shisha ortidagi narsalarni xiralashtiruvchi zamonaviy UI.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Glassmorphism</title>
    <style>
        body {
            background: linear-gradient(45deg, #ff007f, #7928ca, #0070f3);
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            font-family: sans-serif;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 16px;
            padding: 30px;
            width: 300px;
            color: white;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        }
    </style>
</head>
<body>
    <div class="glass-card">
        <h3>Shisha Kartochka</h3>
        <p>Yorqin rang-barang fon ortida xiralashib ko'rinib turuvchi zamonaviy Glassmorphism effekti.</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`backdrop-filter: blur(12px)` kartochkaning o'zini emas, uning orqa tomonida turgan elementlarni xiralashtirib, haqiqiy xira shisha taassurotini uyg'otadi.

## Ishlash natijasi:
```text
Yorqin binafsha-qizil gradient ustida joylashgan muzlagan shishadek xira oq kartochka chiqadi.
```

---

# 382-Topshiriq: Mesh Gradient fon dizayni
## Topshiriq sharti:
Bir nechta radial gradientlarni birlashtirib suyuq abstrakt fon yasash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Mesh Gradient</title>
    <style>
        .mesh {
            width: 100%;
            height: 250px;
            border-radius: 12px;
            background-color: #ff99c8;
            background-image:
                radial-gradient(at 80% 0%, #fcf6bd 0px, transparent 50%),
                radial-gradient(at 0% 50%, #d0f4de 0px, transparent 50%),
                radial-gradient(at 70% 80%, #a9def9 0px, transparent 50%),
                radial-gradient(at 20% 90%, #e4c1f9 0px, transparent 50%);
        }
    </style>
</head>
<body>
    <div class="mesh"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
To'rtta turli burchakdagi shaffoflikka ega radial gradientlar bir-birining ustiga oqib kirib, zamonaviy 'mesh' fonini hosil qiladi.

## Ishlash natijasi:
```text
Pushti, sarg'ish, moviy va och binafsharang ohanglar bir-biriga erib ketgan ajoyib fon ko'rinadi.
```

---

# 383-Topshiriq: To'rli katak (Grid pattern) foni
## Topshiriq sharti:
Matematik daftarlarga o'xshash texnologik katakli CSS foni.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Grid Pattern</title>
    <style>
        .blueprint {
            width: 100%;
            height: 200px;
            background-color: #0f172a;
            background-image:
                linear-gradient(rgba(255, 255, 255, 0.07) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.07) 1px, transparent 1px);
            background-size: 20px 20px;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="blueprint"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Biri vertikal, biri gorizontal bo'lgan 1 pikselli oq chiziqlar `background-size: 20px 20px` bo'yicha takrorlanib chizma qog'ozi (blueprint) to'rini yasaydi.

## Ishlash natijasi:
```text
To'q moviy fonda mayda kvadrat katakchalardan iborat muhandislik foni paydo bo'ladi.
```

---

# 384-Topshiriq: Doirali nuqta (Polka Dot) foni
## Topshiriq sharti:
Radial gradient orqali nuqtali naqsh hosil qilish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Polka Dot</title>
    <style>
        .dots {
            width: 100%;
            height: 180px;
            background-color: #f8fafc;
            background-image: radial-gradient(#cbd5e1 1.5px, transparent 1.5px);
            background-size: 16px 16px;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="dots"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`radial-gradient(#cbd5e1 1.5px, transparent 1.5px)` va `16px` o'lcham har 16 pikselda bitta nuqta qo'yib nafis tekstura yaratadi.

## Ishlash natijasi:
```text
Och kulrang fonda bir tekis terilgan nafis nuqtachalar to'ri chiqadi.
```

---

# 385-Topshiriq: Neon chiroqli matn va fon (Glow effect)
## Topshiriq sharti:
Text-shadow va box-shadow orqali kiberpank yorug'lik effekti.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Neon Glow</title>
    <style>
        body { background: #050505; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .neon-text {
            font-family: sans-serif;
            font-size: 36px;
            color: #fff;
            text-shadow:
                0 0 5px #00f0ff,
                0 0 10px #00f0ff,
                0 0 20px #00f0ff,
                0 0 40px #0077ff;
        }
    </style>
</head>
<body>
    <div class="neon-text">KIBER O'ZBEKISTON</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Bir nechta qatlamli `text-shadow` ning radiusini kattalashtirib borish orqali qorong'uda neon lampalardek yonib turuvchi nur hosil qilinadi.

## Ishlash natijasi:
```text
Qop-qorong'u xonada zangori nur taratib turuvchi yorqin neon yozuv paydo bo'ladi.
```

---

# 386-Topshiriq: Interaktiv rang almashtiruvchi fon animatsiyasi
## Topshiriq sharti:
Gradient burchaklarini harakatlantiruvchi jonli fon.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Animated Gradient</title>
    <style>
        .animated-bg {
            width: 100%;
            height: 200px;
            border-radius: 8px;
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradientMove 8s ease infinite;
        }
        @keyframes gradientMove {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
    </style>
</head>
<body>
    <div class="animated-bg"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Fon o'lchami 400% qilib kattalashtiriladi va `@keyframes` orqali uning joylashuvi surilib turadi, natijada ranglar mayin oqib turadi.

## Ishlash natijasi:
```text
To'rt xil ranglar bir-biriga uzluksiz silliq oqib o'tuvchi jonli animatsion fon chiqadi.
```

---

# 387-Topshiriq: font-size-adjust bilan shrift almashganda sakrashni yo'qotish
## Topshiriq sharti:
Zaxira va asosiy shriftning x-balandligini tenglashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Font Size Adjust</title>
    <style>
        p {
            font-family: 'MaxsusShrift', Arial, sans-serif;
            font-size: 18px;
            font-size-adjust: 0.52;
        }
    </style>
</head>
<body>
    <p>Shrift yuklanguncha Arial ko'rinadi, lekin uning harflar balandligi yangi shrift bilan bir xil hajmda turadi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`font-size-adjust` kichik harflarning balandligini (x-height) qat'iy nazorat qiladi va shrift yuklanganda matn sakrab ketishining oldini oladi.

## Ishlash natijasi:
```text
Matn qatorlari o'zgarmas balandlikda turadi.
```

---

# 388-Topshiriq: font-variant: small-caps
## Topshiriq sharti:
Kichik harflarni kichraytirilgan bosh harflarga aylantirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Small Caps</title>
    <style>
        .small-caps { font-variant: small-caps; letter-spacing: 2px; }
    </style>
</head>
<body>
    <p class="small-caps">World Wide Web Consortium Standartlari</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`font-variant: small-caps` harflarni katta harf shakliga o'tkazadi, biroq ularning hajmini kichik harflar bo'yida saqlaydi.

## Ishlash natijasi:
```text
Rim yozuvlariga o'xshash nafis kichik bosh harflar ko'rinadi.
```

---

# 389-Topshiriq: Qorong'u va yorug' rejim ranglar palitrasi
## Topshiriq sharti:
CSS o'zgaruvchilari yordamida ranglar tizimini tashkil qilish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Ranglar Palitrasi</title>
    <style>
        :root {
            --bg-color: #ffffff;
            --text-color: #0f172a;
            --primary: #3b82f6;
        }
        .card { background: var(--bg-color); color: var(--text-color); border: 1px solid var(--primary); padding: 20px; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="card">
        <h3>Markazlashtirilgan Ranglar</h3>
        <p>Barcha ranglar :root o'zgaruvchilarida boshqariladi.</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:root` ichidagi CSS o'zgaruvchilari butun sayt ranglarini bitta joydan osongina o'zgartirish yoki Dark Mode ga o'tkazish imkonini beradi.

## Ishlash natijasi:
```text
Ko'k hoshiyali oq kartochka toza ranglar bilan aks etadi.
```

---

# 390-Topshiriq: font shorthand qisqartma sintaksisi
## Topshiriq sharti:
Style, weight, size, line-height va family parametrlarini bitta qatorda berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Font Shorthand</title>
    <style>
        body {
            /* style | weight | size / line-height | family */
            font: italic bold 18px/1.6 'Georgia', serif;
            padding: 30px;
        }
    </style>
</head>
<body>
    <p>Bitta qatorda e'lon qilingan to'liq tipografik qoida.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`font` qisqartmasida `size` va `family` majburiy bo'lib, `size/line-height` ko'rinishida yoziladi.

## Ishlash natijasi:
```text
Qalin qiya serif shriftida 18px o'lchamli chiroyli matn chiqadi.
```

---

# 391-Topshiriq: font-style: italic va oblique farqi
## Topshiriq sharti:
Tabiiy qiya xattotlik shrifti va majburiy burchakka og'dirilgan shrift.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Italic vs Oblique</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .ita { font-style: italic; }
        .obl { font-style: oblique 15deg; }
    </style>
</head>
<body>
    <p class="ita">Italic: Shrift muallifi chizgan tabiiy qiya harflar.</p>
    <p class="obl">Oblique: Harflarni 15 gradus burchakka majburiy og'dirish.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`italic` shrift dizayneri tomonidan maxsus chizilgan qiya kursiv gliflarni ulaydi, `oblique` esa oddiy harflarni burchakka qiyalashtiradi.

## Ishlash natijasi:
```text
Biri mayin xattotlik qiyaligida, ikkinchisi 15 gradusga og'dirilgan ikkita matn ko'rinadi.
```

---

# 392-Topshiriq: text-rendering xususiyati va uning tezlikka ta'siri
## Topshiriq sharti:
Brauzerga matnni tez chizish yoki harflar bog'lanishini (ligatures) chiroyli qilishni buyurish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Text Rendering</title>
    <style>
        .crisp { text-rendering: optimizeLegibility; font-size: 24px; font-family: 'Times New Roman', serif; }
    </style>
</head>
<body>
    <p class="crisp">Difficult official fluff (fi, ff, fl ligaturalari bog'lanadi)</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`text-rendering: optimizeLegibility` harflar orasidagi bog'lanish (ligature) va kernalashni mukammal chizadi.

## Ishlash natijasi:
```text
'fi' va 'fl' harflari bir-biriga uzluksiz ulangan klassik kitobiy matn chiqadi.
```

---

# 393-Topshiriq: font-smoothing (Antialiasing) bilan matn qirralarini silliqlash
## Topshiriq sharti:
Mac va iOS ekranlarida shriftlarning juda nozik va tiniq ko'rinishi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Font Smoothing</title>
    <style>
        body {
            background: #0f172a;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            padding: 30px;
        }
    </style>
</head>
<body>
    <p>Qorong'u fonda oq matnning qirralari silliqlashgan va nozik o'qiladi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`-webkit-font-smoothing: antialiased` subpikselli qirralarni yo'qotib, matnni yanada toza va nafis qiladi.

## Ishlash natijasi:
```text
Qora fonda oq matn o'ta tiniq va qirralari yumshoq bo'lib aks etadi.
```

---

# 394-Topshiriq: Variable Fonts va font-weight silliq animatsiyasi
## Topshiriq sharti:
Yagona fayldan 1 dan 1000 gacha uzluksiz o'zgaruvchi zamonaviy shrift.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Variable Fonts</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');
        .anim-weight {
            font-family: 'Inter', sans-serif;
            font-size: 36px;
            font-weight: 100;
            transition: font-weight 0.4s ease;
            cursor: pointer;
        }
        .anim-weight:hover { font-weight: 900; }
    </style>
</head>
<body>
    <div class="anim-weight">Ustiga kelsangiz qalinlashaman</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
O'zgaruvchan shriftlar (Variable Fonts) bitta faylda barcha qalinliklarni saqlaydi va CSS orqali vaznni silliq animatsiya qilish imkonini beradi.

## Ishlash natijasi:
```text
Kursor kelganda ingichka yozuv to'satdan emas, suyuq mayinlik bilan qalinlashadi.
```

---

# 395-Topshiriq: Dasturchilar kodi ligaturalari (font-variant-ligatures)
## Topshiriq sharti:
`=>`, `!=`, `===` belgilarini chiroyli bitta belgilarga aylantirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Code Ligatures</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code&display=swap');
        code {
            font-family: 'Fira Code', monospace;
            font-variant-ligatures: normal;
            font-size: 20px;
            background: #1e1e1e;
            color: #38bdf8;
            padding: 10px 15px;
            border-radius: 6px;
            display: inline-block;
        }
    </style>
</head>
<body>
    <code>const f = (x) => x !== null;</code>
</body>
</html>
```

## Tushuntirish va Mantiq:
`Fira Code` kabi shriftlar ligaturalar bilan dasturchilar kodini yanada chiroyli o'qilishini ta'minlaydi.

## Ishlash natijasi:
```text
`=>` belgisi chiroyli yagona strelkaga, `!==` esa teng emas belgisiga aylanib ko'rinadi.
```

---

# 396-Topshiriq: Ranglar kontrasti va WCAG AAA qulaylik standarti
## Topshiriq sharti:
Ko'rishida zaiflik bor insonlar ham matnni oson o'qiy olishini kafolatlovchi kontrast nisbati (4.5:1).

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Kontrast Nisbati</title>
    <style>
        body { font-family: sans-serif; padding: 25px; display: flex; gap: 20px; }
        .bad { background: #f1f5f9; color: #94a3b8; padding: 15px; border-radius: 6px; }
        .good { background: #0f172a; color: #f8fafc; padding: 15px; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="bad">Xato: O'qish juda qiyin (Kontrast past: 2:1)</div>
    <div class="good">Ideal: O'qish juda oson (Kontrast yuqori: 16:1)</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
WCAG xalqaro qoidasiga ko'ra matn va fon o'rtasidagi rang kontrasti kamida 4.5:1 (kichik matnlar uchun) bo'lishi shart.

## Ishlash natijasi:
```text
Biri xira ko'rinuvchi, ikkinchisi to'q fonda yaqqol ajralib turuvchi ikkita blok namoyon bo'ladi.
```

---

# 397-Topshiriq: background-origin va background-clip farqlari
## Topshiriq sharti:
Fon qayerdan boshlanishi (origin) va qayerda to'xtatilishi (clip) tajribasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Origin va Clip</title>
    <style>
        .box {
            width: 250px;
            padding: 20px;
            border: 10px dashed #3b82f6;
            background-color: #fef08a;
            background-clip: padding-box;
        }
    </style>
</head>
<body>
    <div class="box">Hoshiya ostiga fon kirmaydi (padding-box)</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`background-clip: padding-box` fon rangini chegara (`border`) ostiga kirmasdan padding chegarasida to'xtatadi.

## Ishlash natijasi:
```text
Ko'k punktir hoshiya osti bo'sh qoladi, sariq fon esa faqat ichkarida bo'ladi.
```

---

# 398-Topshiriq: CSS conic-gradient orqali yuklanish aylanasi (Spinner)
## Topshiriq sharti:
Pikselli rasmsiz toza konussimon aylanma yuklagich.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Conic Spinner</title>
    <style>
        .spinner {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: conic-gradient(#2563eb, transparent 60%);
            -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 6px), #000 0);
            mask: radial-gradient(farthest-side, transparent calc(100% - 6px), #000 0);
            animation: spin 1s linear infinite;
        }
        @keyframes spin { 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="spinner"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Mask va conic-gradient vositasida to'liq aylanuvchi chiroyli yuklanish halqasi yaratiladi.

## Ishlash natijasi:
```text
Ekranda to'xtovsiz aylanib turuvchi zamonaviy moviy yuklagich chiqadi.
```

---

# 399-Topshiriq: Fon xiralashuvi (Frosting) orqali yozuv taxtasi
## Topshiriq sharti:
To'q rangli fotoning ustiga qo'yilgan yarim shaffof ma'lumotlar bloki.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Frosting Panel</title>
    <style>
        .scene {
            width: 400px;
            height: 220px;
            background: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400');
            background-size: cover;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
        }
        .frosted-text {
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(6px);
            color: white;
            padding: 15px 25px;
            border-radius: 6px;
            font-family: sans-serif;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="scene">
        <div class="frosted-text">
            <h2>Okean Sohillari</h2>
            <p style="margin:0;">Sayyohlik agentligi rasmiy taklifi</p>
        </div>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Dengiz sohili fotosi ustida xiralashgan qora oynachali matn to'liq o'qishli va jozibali chiqadi.

## Ishlash natijasi:
```text
Sohil manzarasi markazida yarim shaffof qoraytirilgan muzli oyna ustida yozuvlar aks etadi.
```

---

# 400-Topshiriq: To'liq professional tipografik va estetik brend kitobi (Styleguide)
## Topshiriq sharti:
Barcha sarlavhalar, xatboshilar, ranglar palitrasi va shriftlarni jamlagan to'laqonli dizayn tizimi sahifasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dizayn Tizimi va Tipografika</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; color: #1e293b; padding: 40px 20px; line-height: 1.6; }
        .styleguide { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        h1.title { border-bottom: 2px solid #e2e8f0; padding-bottom: 15px; margin-bottom: 30px; }
        .palette { display: flex; gap: 15px; margin-bottom: 30px; }
        .swatch { flex: 1; height: 80px; border-radius: 8px; display: flex; align-items: flex-end; padding: 8px; color: white; font-size: 12px; font-weight: bold; }
        .c-primary { background: #2563eb; }
        .c-success { background: #10b981; }
        .c-warning { background: #f59e0b; }
        .c-dark { background: #0f172a; }
        .typo-sample { margin-bottom: 20px; }
        .h1-sample { font-size: 32px; font-weight: 800; color: #0f172a; }
        .lead-sample { font-size: 18px; color: #64748b; }
    </style>
</head>
<body>
    <div class="styleguide">
        <h1 class="title">Raqamli Brend Qo'llanmasi (Styleguide)</h1>
        <h3>1. Rasmiy Ranglar Palitrasi</h3>
        <div class="palette">
            <div class="swatch c-primary">#2563eb</div>
            <div class="swatch c-success">#10b981</div>
            <div class="swatch c-warning">#f59e0b</div>
            <div class="swatch c-dark">#0f172a</div>
        </div>
        <h3>2. Tipografik Ierarxiya</h3>
        <div class="typo-sample">
            <div class="h1-sample">Asosiy Katta Sarlavha (32px / 800)</div>
            <div class="lead-sample">Kirish xatboshisi: qulay 18px o'lcham va yumshoq kontrast.</div>
            <p style="margin-top: 10px;">Standart xatboshi matni: inson ko'zini charchatmaydigan 16px o'lcham va 1.6 qator balandligi.</p>
        </div>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu yakuniy andoza professional veb-loyihalarning asosiy 'Styleguide' hujjatidir. Unda brend ranglari palitrasi, shrift qalinliklari va iyerarxik matn namunalari to'liq qamrab olingan.

## Ishlash natijasi:
```text
Oq keng kartochkada to'rtta rasmiy ranglar bloki va pastida iyerarxik tarzda terilgan professional tipografik namunalar ko'rinadi.
```

---

