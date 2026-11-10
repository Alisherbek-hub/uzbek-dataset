# Box Model va O'lchamlar (401-450)

# 401-Topshiriq: CSS Box Model anatomiyasi
## Topshiriq sharti:
Content, padding, border va margin qatlamlarini to'laqonli namoyish etuvchi blok tuzing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Box Model Anatomiyasi</title>
    <style>
        body { font-family: sans-serif; padding: 40px; background: #f8fafc; }
        .box-demo {
            width: 260px;
            padding: 20px;
            border: 10px solid #3b82f6;
            margin: 30px;
            background-color: #fef08a;
            color: #0f172a;
            font-weight: bold;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="box-demo">Content (260px)</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
CSS Box Model 4 qatlamdan iborat: 1) Content — matn yoki rasm maydoni; 2) Padding — kontent va hoshiya orasidagi ichki oraliq; 3) Border — elementning chegaraviy hoshiyasi; 4) Margin — elementni boshqa qo'shnilardan itarib turuvchi tashqi oraliq.

## Ishlash natijasi:
```text
Sariq kontent, uning atrofida 20px bo'shliq, ko'k qalin hoshiya va tashqarisida 30px oraliqqa ega to'rtburchak ko'rinadi.
```

---

# 402-Topshiriq: box-sizing: content-box (standart xatti-harakat)
## Topshiriq sharti:
Nima uchun padding va border element kengligini shishirib yuborishini tushuntiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Content Box</title>
    <style>
        .box {
            box-sizing: content-box;
            width: 200px;
            padding: 20px;
            border: 5px solid #dc2626;
            background: #fee2e2;
        }
    </style>
</head>
<body>
    <div class="box">Haqiqiy eni: 200 + 40 + 10 = 250px!</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`content-box` brauzerning tabiiy sukut bo'yicha rejimidir. Bunda `width: 200px` faqat kontentga tegishli bo'lib, padding (20+20) va border (5+5) qo'shilganda element ekranda 250px joy egallaydi va ko'pincha maketni buzib yuboradi.

## Ishlash natijasi:
```text
Qizil hoshiyali blok belgilangan 200px dan ancha kengayib, 250px hajmda ko'rinadi.
```

---

# 403-Topshiriq: box-sizing: border-box va uning global qo'llanilishi
## Topshiriq sharti:
Padding va border berilganda ham element kengligi o'zgarmasligini ta'minlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Border Box</title>
    <style>
        * { box-sizing: border-box; }
        .box {
            width: 200px;
            padding: 20px;
            border: 5px solid #16a34a;
            background: #dcfce7;
        }
    </style>
</head>
<body>
    <div class="box">Haqiqiy eni qat'iy 200px qoladi.</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`border-box` rejimida brauzer padding va borderni ko'rsatilgan `width` ning ichiga siqib kiritadi. 200px kenglik qat'iy saqlanadi, kontent maydoni esa 150px ga qisqaradi.

## Ishlash natijasi:
```text
Yashil hoshiyali blok aniq 200px kenglikni saqlab turadi.
```

---

# 404-Topshiriq: Padding 4 tomoni: top, right, bottom, left
## Topshiriq sharti:
Har bir tomonga alohida mustaqil ichki oraliq berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Padding Tomonlari</title>
    <style>
        .custom-pad {
            padding-top: 40px;
            padding-right: 15px;
            padding-bottom: 10px;
            padding-left: 30px;
            background: #eff6ff;
            border: 1px solid #3b82f6;
            width: 250px;
        }
    </style>
</head>
<body>
    <div class="custom-pad">Turli tomonlama padding</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Tepa (40px), o'ng (15px), past (10px) va chap (30px) bo'yicha alohida xususiyatlar orqali ichki matn joylashuvi nozik sozlanadi.

## Ishlash natijasi:
```text
Tepasi ancha keng, chapdan o'rtacha surilgan moviy quti chiqadi.
```

---

# 405-Topshiriq: Padding qisqartmalari (shorthand 1, 2, 3, 4 qiymatlar)
## Topshiriq sharti:
Soat strelkasi bo'yicha (TRBL qoidasi) qisqa kod yozish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Padding Shorthand</title>
    <style>
        body { font-family: sans-serif; padding: 20px; line-height: 2; }
        .p4 { padding: 10px 20px 30px 40px; background: #e2e8f0; margin-bottom: 10px; }
        .p2 { padding: 15px 30px; background: #cbd5e1; }
    </style>
</head>
<body>
    <div class="p4">4 ta qiymat: Top Right Bottom Left</div>
    <div class="p2">2 ta qiymat: Vertikal (15px) va Gorizontal (30px)</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`padding: 15px 30px` — birinchi son tepa/pastni, ikkinchisi o'ng/chapni bildiradi. 4 ta qiymat bo'lsa: Tepa, O'ng, Past, Chap (soat strelkasi).

## Ishlash natijasi:
```text
Ikkita kulrang blok; biri har tomonlama har xil, ikkinchisi nosimmetrik oraliqli.
```

---

# 406-Topshiriq: Margin 4 tomoni va uning tashqi oraliqdagi roli
## Topshiriq sharti:
Elementlar orasida xavfsiz tashqi masofa hosil qilish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Margin Tomonlari</title>
    <style>
        .block1 { background: #fee2e2; padding: 10px; margin-bottom: 25px; }
        .block2 { background: #e0e7ff; padding: 10px; }
    </style>
</head>
<body>
    <div class="block1">1-Blok (pastga 25px itaradi)</div>
    <div class="block2">2-Blok</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`margin` elementning o'zini emas, uning atrofidagi qo'shni bloklarni surish uchun xizmat qiluvchi shaffof tashqi maydondir.

## Ishlash natijasi:
```text
Ikkita rangli blok o'rtasida 25px toza bo'shliq hosil bo'ladi.
```

---

# 407-Topshiriq: Margin Collapsing (Vertikal marginlarning yutilishi)
## Topshiriq sharti:
Ustma-ust tushgan ikki margin nima uchun qo'shilmasligini tushuntirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Margin Collapsing</title>
    <style>
        .top-box { margin-bottom: 30px; background: #dcfce7; padding: 10px; }
        .bottom-box { margin-top: 20px; background: #fef9c3; padding: 10px; }
    </style>
</head>
<body>
    <div class="top-box">margin-bottom: 30px</div>
    <div class="bottom-box">margin-top: 20px</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
CSS qoidasiga ko'ra ikki vertikal margin to'qnashganda ular qo'shilmaydi (30+20=50 bo'lmaydi), balki eng kattasi (30px) qoladi va kichigi uning ichiga yutilib ketadi.

## Ishlash natijasi:
```text
Oraliq masofa 50px emas, aynan kattasi bo'lgan 30px bo'lib qoladi.
```

---

# 408-Topshiriq: Salbiy (Negative) marginlar
## Topshiriq sharti:
Elementni o'zining tabiiy joyidan tepaga yoki chapga tortish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Negative Margin</title>
    <style>
        .card { width: 300px; background: white; border: 1px solid #cbd5e1; padding: 20px; margin: 50px auto; border-radius: 8px; }
        .badge-overlap { margin-top: -35px; background: #2563eb; color: white; padding: 6px 12px; border-radius: 20px; display: inline-block; }
    </style>
</head>
<body>
    <div class="card">
        <div class="badge-overlap">Yangi</div>
        <p>Salbiy margin yordamida nishon kartochkaning tepa chegarasi ustiga chiqarildi.</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`margin-top: -35px` elementni yuqoriga surib ota blokning chegarasini bosib o'tishiga imkon beradi.

## Ishlash natijasi:
```text
Moviy nishoncha kartochkaning tepa hoshiyasiga minib turgan zamonaviy dizayn chiqadi.
```

---

# 409-Topshiriq: margin: 0 auto orqali markazlashtirish
## Topshiriq sharti:
Qat'iy kenglikka ega blokni ekranning qoq o'rtasiga joylashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Margin Auto</title>
    <style>
        .centered {
            width: 400px;
            margin: 0 auto;
            background: #1e293b;
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="centered">Markazlashtirilgan Blok (margin: 0 auto)</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`margin: 0 auto` chap va o'ng tomondagi barcha bo'sh joyni teng ikkiga bo'lib blokni brauzer darchasining markaziga tekislaydi (blokda `width` bo'lishi shart).

## Ishlash natijasi:
```text
Ekran kengligidan qat'i nazar, qoq markazda turgan to'q rangli blok ko'rinadi.
```

---

# 410-Topshiriq: Chegara stillari: border-style turlari
## Topshiriq sharti:
Solid, dashed, dotted, double kabi hoshiya chiziqlari.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Border Style</title>
    <style>
        body { font-family: sans-serif; display: flex; gap: 15px; padding: 25px; flex-wrap: wrap; }
        .b { width: 100px; height: 60px; border-width: 4px; border-color: #3b82f6; display: flex; align-items: center; justify-content: center; }
        .solid { border-style: solid; }
        .dashed { border-style: dashed; }
        .dotted { border-style: dotted; }
        .double { border-style: double; border-width: 6px; }
    </style>
</head>
<body>
    <div class="b solid">Solid</div>
    <div class="b dashed">Dashed</div>
    <div class="b dotted">Dotted</div>
    <div class="b double">Double</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`solid` qattiq to'g'ri chiziq, `dashed` uzuq-uzuq tirelar, `dotted` nuqtalar, `double` esa qo'shaloq chiziq hosil qiladi.

## Ishlash natijasi:
```text
To'rt xil chiziq uslubidagi ko'k hoshiyali qutichalar qatori namoyon bo'ladi.
```

---

# 411-Topshiriq: border qisqartma (shorthand) xususiyati
## Topshiriq sharti:
Qalinlik, stil va rangni bitta qatorda belgilash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Border Shorthand</title>
    <style>
        .box { border: 2px solid #10b981; padding: 15px; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="box">border: 2px solid #10b981</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`border: 2px solid #10b981;` bitta qatorda qalinlik (2px), stil (solid) va rangni (#10b981) e'lon qiladi.

## Ishlash natijasi:
```text
Yashil 2 pikselli chegaraga ega ixcham blok chiqadi.
```

---

# 412-Topshiriq: Faqat bitta tomonga chegara berish
## Topshiriq sharti:
border-bottom yoki border-left bilan ajratuvchi chiziqlar yasash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Border Single Side</title>
    <style>
        .quote {
            border-left: 4px solid #f59e0b;
            padding-left: 15px;
            font-style: italic;
            color: #334155;
        }
    </style>
</head>
<body>
    <div class="quote">"Bilim olish — har bir insonning oliy burchidir."</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`border-left: 4px solid #f59e0b;` faqat chap tomonga chiziq qo'yib, zamonaviy iqtibos uslubini yaratadi.

## Ishlash natijasi:
```text
Chap tomonida sariq vertikal chizig'i bor qiya matn ko'rinadi.
```

---

# 413-Topshiriq: border-radius bilan burchaklarni yumaloqlash
## Topshiriq sharti:
Piksel va foizlarda burchaklarni silliqlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Border Radius</title>
    <style>
        body { font-family: sans-serif; display: flex; gap: 20px; padding: 25px; }
        .r8 { width: 100px; height: 100px; background: #3b82f6; border-radius: 8px; }
        .r24 { width: 100px; height: 100px; background: #3b82f6; border-radius: 24px; }
        .circle { width: 100px; height: 100px; background: #3b82f6; border-radius: 50%; }
    </style>
</head>
<body>
    <div class="r8"></div>
    <div class="r24"></div>
    <div class="circle"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`border-radius: 8px` biroz yumaloqlaydi, `24px` kuchli yumaloqlaydi, `50%` esa kvadratni mukammal aylanaga aylantiradi.

## Ishlash natijasi:
```text
Biri ozgina yumaloq, biri ancha yumaloq va biri to'liq doira bo'lgan uchta ko'k figura chiqadi.
```

---

# 414-Topshiriq: border-radius ga 4 xil burchak berish (Barg shakli)
## Topshiriq sharti:
Har bir burchakka alohida radius berib noodatiy shakllar yasash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Asimmetrik Radius</title>
    <style>
        .leaf {
            width: 120px;
            height: 120px;
            background: #10b981;
            /* Yuqori-chap, Yuqori-o'ng, Quyi-o'ng, Quyi-chap */
            border-radius: 40px 0 40px 0;
        }
    </style>
</head>
<body>
    <div class="leaf"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`border-radius: 40px 0 40px 0` qarama-qarshi burchaklarni yumaloqlab, qolganlarini to'g'ri burchak qoldirishi orqali tabiiy barg shaklini hosil qiladi.

## Ishlash natijasi:
```text
Yashil rangdagi geometrik barg shakli paydo bo'ladi.
```

---

# 415-Topshiriq: Outline vs Border farqi
## Topshiriq sharti:
Outline maydon egallamasligi va joylashuvni siljitmasligini ko'rsatish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Outline vs Border</title>
    <style>
        body { font-family: sans-serif; padding: 30px; display: flex; gap: 40px; }
        .b-box { width: 120px; height: 80px; background: #eee; border: 6px solid #2563eb; }
        .o-box { width: 120px; height: 80px; background: #eee; outline: 6px solid #ef4444; }
    </style>
</head>
<body>
    <div class="b-box">Border (Ichki/tashqi joy oladi)</div>
    <div class="o-box">Outline (Joy olmaydi)</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`outline` Box Modelga kirmaydi, ya'ni elementning o'lchamini kattalashtirmaydi va qo'shni elementlarni surib yubormaydi. U fokus berishda qo'llaniladi.

## Ishlash natijasi:
```text
Biri ko'k chegara, biri qizil outline bilan o'ralgan ikkita blok chiqadi.
```

---

# 416-Topshiriq: outline-offset xususiyati
## Topshiriq sharti:
Hoshiyani element chegarasidan tashqariga surish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Outline Offset</title>
    <style>
        .btn {
            background: #2563eb;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            outline: 2px dashed #2563eb;
            outline-offset: 4px;
        }
    </style>
</head>
<body>
    <button class="btn">Masofali Halqa</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
`outline-offset: 4px` element va uning tashqi chizig'i orasida 4 pikselli shaffof havo bo'shlig'i qoldiradi.

## Ishlash natijasi:
```text
Tugma atrofida 4px masofada turgan punktir ko'k ramka ko'rinadi.
```

---

# 417-Topshiriq: box-shadow asoslari (x, y, blur, color)
## Topshiriq sharti:
Blok ortiga tabiiy 3D chuqurlik beruvchi soya tushirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Box Shadow</title>
    <style>
        .card {
            width: 250px;
            padding: 20px;
            background: white;
            border-radius: 8px;
            /* X: 0, Y: 10px, Blur: 15px, Color */
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body>
    <div class="card">Yumshoq Soyali Kartochka</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`box-shadow: 0 10px 15px rgba(0,0,0,0.1)` pastga qarab 10px tushgan va 15px xiralashgan yumshoq tabiiy soyani yaratadi.

## Ishlash natijasi:
```text
Stol ustida ko'tarilib turgandek ko'rinuvchi oq kartochka chiqadi.
```

---

# 418-Topshiriq: box-shadow spread (tarqalish) radiusi
## Topshiriq sharti:
Soyaning har tomonga qanchalik kengayishini sozlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Shadow Spread</title>
    <style>
        .halo {
            width: 200px;
            padding: 20px;
            background: white;
            border-radius: 6px;
            box-shadow: 0 0 0 10px rgba(59, 130, 246, 0.3);
        }
    </style>
</head>
<body>
    <div class="halo">Spread orqali halqa soyasi</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
To'rtinchi parametr `spread: 10px` blur bo'lmagan holda ham element atrofida 10 pikselli qalin nurlanish halqasini hosil qiladi.

## Ishlash natijasi:
```text
Oq blok atrofida 10px qalinlikdagi moviy shaffof halqa paydo bo'ladi.
```

---

# 419-Topshiriq: box-shadow inset ichki soyasi
## Topshiriq sharti:
Blokni ichkariga botib kirgandek ko'rsatish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Shadow Inset</title>
    <style>
        .recessed {
            width: 200px;
            padding: 20px;
            background: #f1f5f9;
            border-radius: 6px;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
        }
    </style>
</head>
<body>
    <div class="recessed">Ichkariga botgan blok</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`inset` kalit so'zi soyani tashqariga emas, blokning ichki tomoniga yo'naltiradi va chuqurcha taassurotini beradi.

## Ishlash natijasi:
```text
Ichkariga botgan kulrang quticha ko'rinadi.
```

---

# 420-Topshiriq: Ko'p qavatli silliq soyalar (Multi-layered shadow)
## Topshiriq sharti:
Dizaynerlar uslubidagi juda tabiiy va qimmat ko'rinuvchi soya.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Multi Layer Shadow</title>
    <style>
        .pro-card {
            width: 280px;
            padding: 25px;
            background: white;
            border-radius: 12px;
            box-shadow:
                0 1px 3px rgba(0,0,0,0.05),
                0 10px 20px -5px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="pro-card">Professional Ko'p Qavatli Soya</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Bir vaqtning o'zida ikkita soya qatlami beriladi: birinchisi qirralarni ushlab turuvchi mayda soya, ikkinchisi esa uzoqqa tarqaluvchi havodor soya.

## Ishlash natijasi:
```text
Zamonaviy ilovalardagidek nihoyatda chiroyli va yumshoq ko'tarilib turgan kartochka chiqadi.
```

---

# 421-Topshiriq: width va height asosiy chegaralari
## Topshiriq sharti:
Elementlarning qat'iy piksellarda balandlik va kengligini berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Width Height</title>
    <style>
        .fixed-box { width: 300px; height: 150px; background: #e2e8f0; }
    </style>
</head>
<body>
    <div class="fixed-box">300x150 o'lchamdagi quti</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`width` va `height` blokning o'lchamlarini qat'iy belgilaydi.

## Ishlash natijasi:
```text
To'rtburchak kulrang blok aks etadi.
```

---

# 422-Topshiriq: max-width va responsiv dizayn
## Topshiriq sharti:
Katta ekranda cheklovchi, kichik ekranda esa erkin qisqaruvchi kenglik.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Max Width</title>
    <style>
        .container {
            width: 100%;
            max-width: 600px;
            background: #dbeafe;
            padding: 20px;
            margin: 0 auto;
        }
    </style>
</head>
<body>
    <div class="container">Katta ekranda 600px dan oshmayman, telefonda esa 100% qisqaraman.</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`width: 100%; max-width: 600px;` kombinatsiyasi responsiv maketlarning poydevoridir — telefon ekranida hoshiyadan chiqib ketmaydi, kompyuterda esa o'ta cho'zilib ketmaydi.

## Ishlash natijasi:
```text
Telefonda to'liq sig'adigan, kompyuterda esa 600px da to'xtaydigan markaziy blok chiqadi.
```

---

# 423-Topshiriq: min-height va kontent erkinligi
## Topshiriq sharti:
Boshida ma'lum balandlikka ega bo'lib, matn ko'payganda erkin pastga cho'zilish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Min Height</title>
    <style>
        .box {
            min-height: 120px;
            background: #fef08a;
            padding: 15px;
            border: 1px solid #ca8a04;
        }
    </style>
</head>
<body>
    <div class="box">Agar matn bitta qator bo'lsa ham bo'yim kamida 120px bo'ladi. Matn toshsa, o'zim cho'zilib sig'diraman.</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`height` qat'iy qotirib qo'yadi va matn toshib ketishiga sabab bo'ladi. `min-height` esa eng kamida 120px kafolatlaydi, matn ko'payganda esa cheklovsiz kengayadi.

## Ishlash natijasi:
```text
Kamida 120px balandlikka ega sariq quti chiqadi.
```

---

# 424-Topshiriq: fit-content, min-content, max-content
## Topshiriq sharti:
Element o'lchamini uning ichki matniga qarab aqlli moslashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Intrinsik O'lchamlar</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .fit { width: fit-content; background: #38bdf8; padding: 8px 16px; border-radius: 4px; color: white; margin-bottom: 10px; }
        .max { width: max-content; background: #4ade80; padding: 8px; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="fit">fit-content: Faqat matnga loyiq eni egallayman</div>
    <div class="max">max-content: Bitta uzun satr bo'lib cho'zilaman</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`width: fit-content` blokli elementni butun ekran bo'ylab yoyilishini to'xtatib, aynan uning ichidagi matn hajmiga moslashtiradi.

## Ishlash natijasi:
```text
Matn uzunligiga mos ixcham ikkita rangli blok chiqadi.
```

---

# 425-Topshiriq: overflow: visible (standart)
## Topshiriq sharti:
Katakdan toshgan kontentning tashqariga chiqib ketishi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Overflow Visible</title>
    <style>
        .box { width: 150px; height: 60px; border: 2px solid black; overflow: visible; }
    </style>
</head>
<body>
    <div class="box">Ushbu juda uzun matn qutidan tashqariga chiqib ketadi va ko'rinib turadi.</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`overflow: visible` rejimida ramkaga sig'magan matnlar pastki chegarani buzib o'tib tashqarida ko'rinadi.

## Ishlash natijasi:
```text
Qora ramkaning pastki chizig'ini kesib o'tib pastga osilib turgan matn ko'rinadi.
```

---

# 426-Topshiriq: overflow: hidden va qirqish
## Topshiriq sharti:
Sig'magan kontentni berkitish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Overflow Hidden</title>
    <style>
        .box { width: 150px; height: 60px; border: 2px solid #2563eb; overflow: hidden; }
    </style>
</head>
<body>
    <div class="box">Sig'magan matnlar qirqiladi va mutlaqo ko'rinmaydi.</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`overflow: hidden` ramkadan tashqariga chiqqan har qanday narsani ko'rinmas qilib qirqib tashlaydi.

## Ishlash natijasi:
```text
Ramka ichidagi matn qirqilib, ramkadan tashqari joylari yo'qoladi.
```

---

# 427-Topshiriq: overflow: scroll va skrollbar
## Topshiriq sharti:
Konteyner ichida doimiy varaqlash chizig'ini hosil qilish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Overflow Scroll</title>
    <style>
        .scroll-box { width: 200px; height: 80px; border: 1px solid #94a3b8; overflow: scroll; }
    </style>
</head>
<body>
    <div class="scroll-box">1-Qator<br>2-Qator<br>3-Qator<br>4-Qator<br>5-Qator<br>6-Qator</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`overflow: scroll` matn sig'sa ham, sig'masa ham skrollbar chiziqlarini har doim ekranda ko'rsatib turadi.

## Ishlash natijasi:
```text
Yonida va ostida doimiy skroll tasmallari bo'lgan darcha chiqadi.
```

---

# 428-Topshiriq: overflow: auto aqlli varaqlash
## Topshiriq sharti:
Faqat matn sig'may toshgandagina skrollbarni chiqarish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Overflow Auto</title>
    <style>
        .auto-box { width: 220px; height: 90px; border: 1px solid #3b82f6; overflow: auto; padding: 10px; }
    </style>
</head>
<body>
    <div class="auto-box">
        Ushbu matn sig'magani bois brauzer faqat vertikal skrollbarni chizadi. Agar sig'ganida edi, hech qanday skroll chiqmas edi.
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`overflow: auto` eng ommabop va qulay yechimdir: zaruriyat tug'ilgandagina skroll paydo bo'ladi.

## Ishlash natijasi:
```text
Faqat vertikal bo'yicha chiroyli aylanuvchi matn darchasi chiqadi.
```

---

# 429-Topshiriq: overflow-x va overflow-y ni alohida boshqarish
## Topshiriq sharti:
Eniga varaqlashni taqiqlab, faqat bo'yiga ruxsat berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Overflow X va Y</title>
    <style>
        .box { width: 200px; height: 100px; border: 1px solid #cbd5e1; overflow-x: hidden; overflow-y: auto; }
    </style>
</head>
<body>
    <div class="box">Bo'yiga aylanadi, eniga esa hech qachon skroll chiqmaydi.</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`overflow-x: hidden; overflow-y: auto;` mobil versiyalarda sahifaning ikki tomonga qaltirab ketishini (gorizontal oqish) to'xtatishda standart usuldir.

## Ishlash natijasi:
```text
Faqatgina vertikal bo'yicha varaqlanuvchi qat'iy blok hosil bo'ladi.
```

---

# 430-Topshiriq: Custom scrollbar: webkit va zamonaviy standart
## Topshiriq sharti:
Skrollbar rangini va enini CSS orqali nafis qilish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Custom Scrollbar</title>
    <style>
        .styled-scroll {
            width: 250px;
            height: 120px;
            overflow-y: auto;
            border: 1px solid #e2e8f0;
            padding: 10px;
            /* Standart W3C */
            scrollbar-width: thin;
            scrollbar-color: #3b82f6 #f1f5f9;
        }
        /* Webkit brauzerlar (Chrome, Safari, Edge) */
        .styled-scroll::-webkit-scrollbar { width: 6px; }
        .styled-scroll::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="styled-scroll">
        1-Satr<br>2-Satr<br>3-Satr<br>4-Satr<br>5-Satr<br>6-Satr<br>7-Satr<br>8-Satr
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`scrollbar-color: #3b82f6 #f1f5f9` (yugurgich va yo'lakcha rangi) hamda `::-webkit-scrollbar` xunuk standart kulrang skrollbarni yupqa ko'k zamonaviy tasmaga aylantiradi.

## Ishlash natijasi:
```text
Yupqa 6 pikselli moviy skrollga ega chiroyli aylanuvchi oyna chiqadi.
```

---

# 431-Topshiriq: resize xususiyati bilan blokni qo'lda cho'zish
## Topshiriq sharti:
Foydalanuvchiga sichqoncha bilan blok o'lchamini kattalashtirishga ruxsat berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Resize Property</title>
    <style>
        .resizable {
            width: 200px;
            height: 100px;
            border: 2px solid #0f172a;
            padding: 10px;
            overflow: auto; /* resize ishlashi uchun overflow zarur! */
            resize: both;
        }
    </style>
</head>
<body>
    <div class="resizable">O'ng pastki burchakdan ushlab meni cho'zing!</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`resize: both; overflow: auto;` kombinatsiyasi oddiy div ga ham xuddi textarea dagi kabi burchakdan tortib cho'zish imkoniyatini baxsh etadi.

## Ishlash natijasi:
```text
Pastki o'ng burchagida cho'zish belgisi bor dinamik to'rtburchak paydo bo'ladi.
```

---

# 432-Topshiriq: Block va inline elementlarda margin/padding farqi
## Topshiriq sharti:
Inline elementlarda (masalan span) vertikal margin va padding nega to'liq ishlamasligini ko'rsatish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Inline vs Block Box</title>
    <style>
        body { font-family: sans-serif; padding: 25px; line-height: 2; }
        .inline-span { margin: 30px; padding: 20px; background: #fef08a; }
    </style>
</head>
<body>
    <p>Matn orasida <span class="inline-span">Inline Span</span> joylashgan.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`inline` elementlarga berilgan `margin-top` va `margin-bottom` atrofdagi qatorlarni itarmaydi! Ular faqat gorizontal (chap va o'ng) oraliq hosil qiladi.

## Ishlash natijasi:
```text
Span ichki fonga ega, lekin tepa va pastdagi qatorlarni o'z o'rnidan siljita olmaydi.
```

---

# 433-Topshiriq: Doira shaklidagi karta (Circle Card)
## Topshiriq sharti:
Width va height teng bo'lganda border-radius 50% orqali doira yasash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Circle Card</title>
    <style>
        .circle-card {
            width: 140px;
            height: 140px;
            border-radius: 50%;
            background: #2563eb;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            text-align: center;
            box-shadow: 0 4px 10px rgba(37,99,235,0.3);
        }
    </style>
</head>
<body>
    <div class="circle-card">100% Doira</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Kvadrat blok (`140x140px`) va `border-radius: 50%` bilan mukammal doiraviy interfeys komponenti yaratiladi.

## Ishlash natijasi:
```text
Markazida matni bo'lgan soya berilgan ko'k ajoyib doira ko'rinadi.
```

---

# 434-Topshiriq: Tabletka (Pill) shaklidagi nishon
## Topshiriq sharti:
Cheksiz katta border-radius (9999px) berish usuli.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Pill Badge</title>
    <style>
        .pill {
            display: inline-block;
            padding: 8px 24px;
            background: #f1f5f9;
            color: #0f172a;
            border: 1px solid #cbd5e1;
            border-radius: 9999px;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <span class="pill">Kapsula Shakli</span>
</body>
</html>
```

## Tushuntirish va Mantiq:
`border-radius: 9999px` berilsa, elementning kengligi qancha bo'lishidan qat'i nazar, ikki cheti doimo mukammal yarim doira (kapsula) bo'lib turadi.

## Ishlash natijasi:
```text
Tabletka ko'rinishidagi ikki tomoni to'liq yumaloq oq-kulrang nishon chiqadi.
```

---

# 435-Topshiriq: Neumorphism (Soft UI) botiq va qabariq soyalar
## Topshiriq sharti:
Yorug'lik va soyaning qarama-qarshi tushishi orqali plastik bo'rtma hosil qilish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Neumorphism</title>
    <style>
        body { background: #e0e5ec; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; font-family: sans-serif; }
        .neu-card {
            width: 200px;
            height: 120px;
            background: #e0e5ec;
            border-radius: 20px;
            box-shadow:
                9px 9px 16px rgb(163,177,198,0.6),
                -9px -9px 16px rgba(255,255,255, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #475569;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="neu-card">Neumorphism</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
O'ng pastki burchakdan to'q soya, chap yuqori burchakdan esa oq yorug'lik nuri bir vaqtda berilib silliq bo'rtib chiqqan plastik korpus effekti olinadi.

## Ishlash natijasi:
```text
Fon bilan bir xil rangdagi, go'yo fondan bo'rtib chiqqandek ko'rinuvchi 3D kartochka aks etadi.
```

---

# 436-Topshiriq: Ichki chiziq effekti (box-shadow yordamida border imitatsiyasi)
## Topshiriq sharti:
Haqiqiy border ishlatmasdan o'lchamni buzmaydigan ichki chiziq tortish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Inner Border</title>
    <style>
        .inner-line {
            width: 250px;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: inset 0 0 0 2px #2563eb;
        }
    </style>
</head>
<body>
    <div class="inner-line">box-shadow inset orqali hoshiya</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`box-shadow: inset 0 0 0 2px #2563eb` hech qanday blur siz toza 2px lik chiziq chizadi va `border` dan farqli ravishda element o'lchamini 1 pikselga ham oshirmaydi.

## Ishlash natijasi:
```text
Ichki moviy hoshiyaga ega toza oq kartochka ko'rinadi.
```

---

# 437-Topshiriq: Konteyner kengligi va responsive padding
## Topshiriq sharti:
Ekran chetiga yopishib qolmaslik uchun konteynerga xavfsiz ichki oraliq berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Container Padding</title>
    <style>
        .safe-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 0 20px;
            background: #f8fafc;
        }
    </style>
</head>
<body>
    <div class="safe-container">
        <h2>Xavfsiz Konteyner</h2>
        <p>Telefonda ochilganda ham yozuvlar ekranning oynasiga yopishib qolmaydi, doim 20px masofa saqlanadi.</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`max-width: 800px; margin: 0 auto; padding: 0 20px;` har qanday zamonaviy veb-saytning markaziy konteyneri uchun eng muhim uchlik hisoblanadi.

## Ishlash natijasi:
```text
Markazda joylashgan, mobil ekranda ham 20px yon oraliq saqlovchi toza blok chiqadi.
```

---

# 438-Topshiriq: CSS orqali sof uchburchak shaklini yasash
## Topshiriq sharti:
Kengligi 0 bo'lgan elementga qalin borderlar berish xaki.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>CSS Uchburchak</title>
    <style>
        .triangle-down {
            width: 0;
            height: 0;
            border-left: 15px solid transparent;
            border-right: 15px solid transparent;
            border-top: 20px solid #2563eb;
        }
    </style>
</head>
<body>
    <div class="triangle-down"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`width: 0; height: 0;` qilinadi, ikki yoniga shaffof border berilib, faqat tepasiga rangli chegara berilganda burchaklar to'qnashib mukammal uchburchak hosil bo'ladi.

## Ishlash natijasi:
```text
Pastga qaratilgan moviy geometrik uchburchak paydo bo'ladi.
```

---

# 439-Topshiriq: Lenta / Bayroq shakli (Ribbon)
## Topshiriq sharti:
Uchburchak va salbiy marginlar bilan mahsulot burchagiga chegirma lentasi qo'yish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Ribbon</title>
    <style>
        .card { width: 250px; background: white; border: 1px solid #cbd5e1; padding: 30px; position: relative; margin: 40px; }
        .ribbon {
            position: absolute;
            top: 10px;
            left: -10px;
            background: #ef4444;
            color: white;
            padding: 4px 15px;
            font-weight: bold;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="ribbon">-30% Chegirma</div>
        <p>Aksiya doirasidagi mahsulot</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`position: absolute; left: -10px` orqali lenta kartochka hoshiyasidan chapga oshirib chiqariladi.

## Ishlash natijasi:
```text
Qizil lenta kartochkaning chap burchagidan bo'rtib chiqib turadi.
```

---

# 440-Topshiriq: Salbiy margin bilan rasmni kartochka chegarasiga yoyish (Full-bleed)
## Topshiriq sharti:
Padding berilgan oq kartochka ichidagi rasmni devorlarigacha yoyish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Full Bleed</title>
    <style>
        .card { width: 300px; padding: 20px; background: white; border: 1px solid #cbd5e1; border-radius: 8px; }
        .card img {
            width: calc(100% + 40px);
            margin: -20px -20px 15px -20px;
            border-radius: 8px 8px 0 0;
            display: block;
        }
    </style>
</head>
<body>
    <div class="card">
        <img src="https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=300" alt="Banner">
        <h3>Kartochka Sarlavhasi</h3>
        <p>Rasm ota blokning 20px paddingini salbiy margin bilan yengib chekkagacha yoyildi.</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`margin: -20px -20px 15px -20px` rasmning ota blokdagi 20px li bo'shliqlarini 'yeb qo'yadi' va to'liq chekkadan chekkagacha yopishib turadi.

## Ishlash natijasi:
```text
Tepasi to'liq rasm bilan qoplangan, matnlari esa 20px ichkarida turgan ideal kartochka chiqadi.
```

---

# 441-Topshiriq: Elevated Hover Card (Balandlikka sakrash)
## Topshiriq sharti:
Kursor kelganda transform va soya orqali havoda ko'tarilish effekti.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Elevated Card</title>
    <style>
        .lift-card {
            width: 250px;
            padding: 20px;
            background: white;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            cursor: pointer;
        }
        .lift-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.12);
        }
    </style>
</head>
<body>
    <div class="lift-card">
        <h4>Interaktiv Karta</h4>
        <p>Ustiga kelsangiz yuqoriga ko'tarilaman.</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`transform: translateY(-6px)` blokni 6px tepaga siljitadi, `box-shadow` esa kengayadi, natijada element jismonan havoga ko'tarilgandek ko'rinadi.

## Ishlash natijasi:
```text
Sichqoncha borganda stol ustidan jismonan ko'tarilib soya tashlovchi kartochka.
```

---

# 442-Topshiriq: 100vh va mobil qurilmalarda 100dvh yangi standarti
## Topshiriq sharti:
Brauzerning URL satri ochilib-yopilganda sakramaydigan to'liq ekran balandligi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dynamic Viewport</title>
    <style>
        body { margin: 0; }
        .full-screen {
            height: 100vh; /* Zaxira eski brauzerlar */
            height: 100dvh; /* Dynamic Viewport Height */
            background: #0f172a;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: sans-serif;
            font-size: 24px;
        }
    </style>
</head>
<body>
    <div class="full-screen">100dvh To'liq Ekran</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`100dvh` (Dynamic Viewport Height) smartfonlarda manzil satri ko'ringanda yoki yashiringanda ekranning haqiqiy ko'rinadigan hajmiga real vaqtda moslashadi.

## Ishlash natijasi:
```text
Telefonda pastki tugmalari kesilib ketmaydigan to'liq ekranli to'q blok chiqadi.
```

---

# 443-Topshiriq: aspect-ratio bilan mukammal kvadrat kataklar
## Topshiriq sharti:
Balandlikni bermasdan proporsiyani saqlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Aspect Ratio</title>
    <style>
        .square-box {
            width: 50%;
            max-width: 200px;
            aspect-ratio: 1 / 1;
            background: #3b82f6;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="square-box"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`aspect-ratio: 1 / 1` kenglik qancha o'zgarsa ham, balandlikni doim unga teng qilib ushlab turadi.

## Ishlash natijasi:
```text
Ekran torayganda ham doim mukammal kvadrat bo'lib qoluvchi ko'k blok chiqadi.
```

---

# 444-Topshiriq: overflow: clip xususiyati
## Topshiriq sharti:
Skroll mexanizmini butunlay o'chirib xotirani tejovchi yangi qirqish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Overflow Clip</title>
    <style>
        .clipped {
            width: 200px;
            height: 60px;
            border: 2px solid #ef4444;
            overflow: clip;
        }
    </style>
</head>
<body>
    <div class="clipped">Ushbu matn qat'iy qirqiladi, dasturiy skroll qilib ham unga yetib bo'lmaydi.</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`overflow: clip` brauzerda skroll konteyneri (scroll container) yaratmaydi, natijada apparat resurslarini kamroq sarflab qirqadi.

## Ishlash natijasi:
```text
Qizil ramkadan oshgan matn toza qirqib tashlanadi.
```

---

# 445-Topshiriq: Matn toshganda uch nuqta qo'yish (Ellipsis)
## Topshiriq sharti:
Sig'magan uzun matnni kesib '...' belgisini chiqarish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Text Ellipsis</title>
    <style>
        .truncate {
            width: 220px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            border: 1px solid #cbd5e1;
            padding: 8px;
        }
    </style>
</head>
<body>
    <div class="truncate">Juda ham uzun xabarnoma sarlavhasi bitta qatordan oshib ketmasligi kerak.</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`white-space: nowrap; overflow: hidden; text-overflow: ellipsis;` bitta qatorli matnni qirqib oxiriga nafis '...' qo'yishning klassik oltin formulasidir.

## Ishlash natijasi:
```text
Matn oxirida '...' bo'lib qirqilgan toza bir qatorli yozuv chiqadi.
```

---

# 446-Topshiriq: clamp() funksiyasi bilan suyuq o'lcham
## Topshiriq sharti:
Minimal, optimal va maksimal o'lchamlar orasida o'zgaruvchi blok kengligi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Clamp O'lcham</title>
    <style>
        .fluid-box {
            width: clamp(250px, 50vw, 600px);
            background: #a855f7;
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin: 0 auto;
        }
    </style>
</head>
<body>
    <div class="fluid-box">Kengligim hech qachon 250px dan kamaymaydi va 600px dan oshmaydi.</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`clamp(min, val, max)` media query yozmasdan turib element kengligini ekran kengligining 50% iga tenglaydi, biroq 250px dan kamayishiga va 600px dan oshishiga yo'l qo'ymaydi.

## Ishlash natijasi:
```text
Ekran kattalashganda silliq kengayuvchi, lekin belgilangan oraliqdan chiqmaydigan binafsha blok aks etadi.
```

---

# 447-Topshiriq: Ko'p qatorli matnni 2-qatorda uch nuqta bilan kesish (-webkit-line-clamp)
## Topshiriq sharti:
Faqat 2 yoki 3 satr matn ko'rsatib qolganini yashirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Line Clamp</title>
    <style>
        .clamp-2 {
            width: 250px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            font-family: sans-serif;
            line-height: 1.5;
        }
    </style>
</head>
<body>
    <p class="clamp-2">
        Sun'iy intellekt texnologiyalari har bir sohada inqilobiy o'zgarishlar yasamoqda va insonlar hayotini yengillashtirishda yangi ufqlar ochmoqda.
    </p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`-webkit-line-clamp: 2` matnni aynan 2-qator tugashi bilan to'xtatadi va qolganini uch nuqta bilan yashiradi.

## Ishlash natijasi:
```text
Aynan 2 satr ko'rinadi va ikkinchi qator oxirida '...' belgisi chiqadi.
```

---

# 448-Topshiriq: Konteyner chegarasidan oshib chiquvchi yopishqoq ko'rsatkich
## Topshiriq sharti:
Absolute positioning va box-sizing birikmasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Floating Indicator</title>
    <style>
        .card { position: relative; width: 220px; padding: 25px; background: white; border: 1px solid #cbd5e1; border-radius: 8px; }
        .pin { position: absolute; top: -10px; right: -10px; width: 24px; height: 24px; background: #ef4444; border-radius: 50%; color: white; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <div class="pin">3</div>
        <p>Xabarlar qutisi</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Kartochkaning o'ng tepa burchagiga `top: -10px; right: -10px` bilan qizil bildirishnoma doirachasi qadaladi.

## Ishlash natijasi:
```text
Oq karta burchagiga minib turgan qizil '3' raqamli xabarlar belgisi ko'rinadi.
```

---

# 449-Topshiriq: Balandligi avtomatik tenglashuvchi kartalar
## Topshiriq sharti:
Bir qatordagi barcha kartalarning balandligini eng uzuniga tenglashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Equal Height</title>
    <style>
        .grid { display: flex; gap: 15px; }
        .card { flex: 1; background: #f8fafc; border: 1px solid #cbd5e1; padding: 20px; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="grid">
        <div class="card">Qisqa matn.</div>
        <div class="card">Ushbu kartada matn ancha ko'proq, shuning uchun u pastga cho'ziladi. Lekin qo'shnisi ham unga tenglashadi.</div>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Flexbox konteyneridagi bolalar sukut bo'yicha `align-items: stretch` bo'lgani sababli bir qatordagi barcha kartalar avtomatik ravishda teng balandlik oladi.

## Ishlash natijasi:
```text
Biri qisqa, biri uzun matnli bo'lsa ham bir xil balandlikka ega ikkita kartochka ko'rinadi.
```

---

# 450-Topshiriq: To'liq Box Model master-klassi va barcha o'lchamlar arxitekturasi
## Topshiriq sharti:
Content, padding, border, margin, box-sizing, box-shadow va overflow imkoniyatlarini jamlagan mukammal mahsulot kartochkasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Box Model Master-klass</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f1f5f9; padding: 40px 20px; display: flex; justify-content: center; }
        .product-box {
            width: 100%;
            max-width: 320px;
            background: white;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 10px 15px -3px rgba(0,0,0,0.1);
            position: relative;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .product-box:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
        }
        .tag-sale {
            position: absolute;
            top: -10px;
            right: 20px;
            background: #ef4444;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(239,68,68,0.3);
        }
        .thumb {
            width: calc(100% + 40px);
            height: 180px;
            margin: -20px -20px 15px -20px;
            border-radius: 12px 12px 0 0;
            overflow: hidden;
        }
        .thumb img { width: 100%; height: 100%; object-fit: cover; }
        .title { font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .desc { font-size: 14px; color: #64748b; line-height: 1.5; height: 42px; overflow: hidden; margin-bottom: 15px; }
        .price-row { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #f1f5f9; padding-top: 15px; }
        .price { font-size: 20px; font-weight: 800; color: #059669; }
        .btn-cart { background: #2563eb; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600; cursor: pointer; }
    </style>
</head>
<body>
    <div class="product-box">
        <span class="tag-sale">TOP</span>
        <div class="thumb">
            <img src="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400" alt="Krossovka">
        </div>
        <h3 class="title">Nike Air Max Hyper Pro 2026</h3>
        <p class="desc">Yuqori qulaylikka ega eng so'nggi avlod yugurish poyabzali.</p>
        <div class="price-row">
            <span class="price">1 250 000 UZS</span>
            <button class="btn-cart">Savatga</button>
        </div>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu yakuniy andoza Box Model nazariyasining to'liq gultojidir: global `border-box`, salbiy margin bilan rasm yoyish, qirralarning yumaloqligi, suzuvchi absolut nishon, matnni uch nuqta bilan kesish va ko'p qavatli yumshoq hover soyalari to'liq qamrab olingan.

## Ishlash natijasi:
```text
Zamonaviy do'kon vitrinasiga xos qizil 'TOP' nishoni bor, yuqorisida chekkagacha yoyilgan qizil krossovka rasmi, sarlavhasi, yashil narxi va ko'k tugmasi bo'lgan mukammal kartochka gavdalanadi.
```

---

