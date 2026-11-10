# Matnlar, Sarlavhalar va Formatlash (51-100)

# 51-Topshiriq: H1 sarlavhasi — sahifaning bosh mavzusi
## Topshiriq sharti:
Sahifaning yagona, eng muhim bosh sarlavhasini H1 tegi orqali to'g'ri joylashtiring va stillang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>H1 Sarlavhasi</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 30px; }
        h1 { font-size: 32px; color: #1e3a8a; border-bottom: 3px solid #3b82f6; padding-bottom: 10px; }
    </style>
</head>
<body>
    <h1>O'zbekistonning Raqamli Kelajagi va Texnologik Rivoji</h1>
    <p>Sahifaning bosh g'oyasi H1 orqali aniqlanadi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
H1 tegi sahifaning eng yuqori darajadagi sarlavhasi hisoblanadi. SEO va veb-standartlar qoidasiga ko'ra, har bir sahifada faqat bitta H1 bo'lishi maqsadga muvofiqdir. U qidiruv robotlariga sahifaning asosiy mavzusini e'lon qiladi.

## Ishlash natijasi:
```text
Sahifa yuqorisida to'q ko'k rangda yirik sarlavha va ostida och ko'k gorizontal chiziq ko'rinadi.
```

---

# 52-Topshiriq: H2 sarlavhasi — asosiy bo'lim sarlavhalari
## Topshiriq sharti:
Mavzuning yirik boblarini ajratib turuvchi H2 sarlavhasini shakllantiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>H2 Sarlavhasi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        h2 { color: #0d9488; font-size: 24px; margin-top: 25px; }
    </style>
</head>
<body>
    <h1>Web Texnologiyalari</h1>
    <h2>1. HTML — Sahifa Suyagi</h2>
    <p>HTML sahifaning barcha tarkibiy qismlarini strukturalaydi.</p>
    <h2>2. CSS — Sahifa Ko'rinishi</h2>
    <p>CSS ranglar, shriftlar va joylashuvlarni belgilaydi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
H2 tegi H1 dan keyingi ikkinchi darajali sarlavha bo'lib, sahifaning yirik tematik bo'limlari (boblar) uchun qo'llaniladi. Sahifada bir nechta H2 bo'lishi mumkin va bu tabiiy holatdir.

## Ishlash natijasi:
```text
Yashil-moviy tusdagi ikkita H2 sarlavhasi va ularning ostida qisqa tushuntirish xatboshilari ko'rinadi.
```

---

# 53-Topshiriq: H3 sarlavhasi — ichki kichik mavzular
## Topshiriq sharti:
H2 bo'limi ichidagi kichik mavzularni ajratuvchi H3 sarlavhalarini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>H3 Sarlavhasi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        h3 { color: #475569; font-size: 18px; margin-left: 15px; }
    </style>
</head>
<body>
    <h2>CSS Joylashuv Tizimlari</h2>
    <h3>A. Flexbox (Bir o'lchamli)</h3>
    <p style="margin-left: 15px;">Elementlarni qator yoki ustun bo'ylab taqsimlaydi.</p>
    <h3>B. CSS Grid (Ikki o'lchamli)</h3>
    <p style="margin-left: 15px;">Qatorlar va ustunlar to'rini hosil qiladi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
H3 elementi H2 ichidagi kichik bo'limlarni ifodalaydi. U orqali hujjatning mantiqiy daraxti yanada chuqurlashadi va o'quvchi ma'lumotni bosqichma-bosqich o'zlashtiradi.

## Ishlash natijasi:
```text
H2 ostida biroz o'ngga surilgan, kulrang-to'q rangdagi kichik mavzular ketma-ketligi paydo bo'ladi.
```

---

# 54-Topshiriq: H4 sarlavhasi — bloklar va vidjetlar sarlavhasi
## Topshiriq sharti:
Vidjetlar, kichik kartochkalar yoki modullar uchun mos keluvchi H4 sarlavhasini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>H4 Sarlavhasi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .card { border: 1px solid #cbd5e1; border-radius: 6px; padding: 15px; width: 250px; }
        h4 { margin: 0 0 10px 0; color: #1e293b; font-size: 16px; }
    </style>
</head>
<body>
    <div class="card">
        <h4>Tezkor Xabarnoma</h4>
        <p>Sizga yangi tizim yangilanishi keldi.</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
H4 to'rtinchi darajali sarlavha hisoblanadi. Odatda u saytdagi alohida kartochkalar, modallar yoki yon paneldagi kichik vidjet sarlavhalarida faol ishlatiladi.

## Ishlash natijasi:
```text
Ixcham oq kartochka ichida to'q kulrang aniq H4 sarlavhasi va uning ostida xabar matni aks etadi.
```

---

# 55-Topshiriq: H5 sarlavhasi — chuqur iyerarxiya va tafsilotlar
## Topshiriq sharti:
Murakkab ma'lumotlar ro'yxatida tafsilotlarni sarlavhalash uchun H5 tegi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>H5 Sarlavhasi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        h5 { color: #64748b; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    </style>
</head>
<body>
    <h5>Texnik Parametrlar</h5>
    <p>Operativ xotira: 32GB DDR5</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
H5 beshinchi darajali sarlavha bo'lib, mayda texnik parametrlar, ro'yxat ostidagi izoh sarlavhalari uchun mos keladi. Matn o'lchami odatda standart matndan ham biroz kichik yoki teng bo'lishi mumkin.

## Ishlash natijasi:
```text
Katta bosh harflar bilan yozilgan, harflar oralig'i kengaytirilgan kulrang H5 sarlavhasi ko'rinadi.
```

---

# 56-Topshiriq: H6 sarlavhasi — eng quyi darajadagi sarlavha
## Topshiriq sharti:
Hujjat sarlavhalari daraxtidagi eng so'nggi oltinchi darajali H6 tegini qo'llang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>H6 Sarlavhasi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        h6 { font-size: 12px; color: #94a3b8; font-weight: normal; margin: 0; }
    </style>
</head>
<body>
    <h6>Izoh va litsenziya talablari tafsiloti</h6>
    <p style="font-size: 13px;">Ushbu ma'lumotlar uchinchi shaxslarga berilishi taqiqlanadi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
H6 HTMLdagi eng quyi rasmiy sarlavha tegidir. Undan keyin H7 yoki H8 mavjud emas. U o'ta mayda bo'limlar yoki yuridik nozik izohlar sarlavhasida ishlatiladi.

## Ishlash natijasi:
```text
Juda mayda, xira kulrang sarlavha va uning ostida tushuntirish matni ko'rinadi.
```

---

# 57-Topshiriq: <p> xatboshi tegi va uning standart oraliqlari
## Topshiriq sharti:
Matnni o'qish uchun qulay bloklarga ajratuvchi `<p>` teglarini stillash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Paragraph Tegi</title>
    <style>
        body { font-family: 'Georgia', serif; padding: 30px; line-height: 1.8; }
        p { margin-bottom: 1.5em; text-align: justify; }
    </style>
</head>
<body>
    <p>Dasturlash — bu inson tafakkurini kompyuter tiliga ko'chirish san'atidir. Har bir yozilgan qator kod orqali biz yangi imkoniyatlar dunyosini quramiz.</p>
    <p>HTML tili veb-sahifalarning tamal toshidir. U har bir axborot bo'lagiga o'ziga xos ma'no va qat'iy mantiqiy tuzilma baxsh etadi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<p>` (paragraph) tegi matnni xatboshilarga ajratadi. Brauzer sukut bo'yicha har bir p tegining tepa va pastki qismiga 1em hajmda margin (tashqi oraliq) qo'yadi. Bu matnni bir-biriga yopishib qolishining oldini oladi.

## Ishlash natijasi:
```text
Bir-biridan qulay oraliq bilan ajratilgan, ikki tomonga tekislangan (justified) ikkita xatboshi matni namoyon bo'ladi.
```

---

# 58-Topshiriq: <br> qatorni ko'chirish tegi
## Topshiriq sharti:
Yangi xatboshi ochmasdan, bitta xatboshi ichida matnni yangi qatorga tushiruvchi `<br>` tegi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Br Tegi Namoyishi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; line-height: 1.5; }
        .poem { background: #fdf2e9; border-left: 4px solid #e67e22; padding: 15px; }
    </style>
</head>
<body>
    <div class="poem">
        Ona tilim — jon-u dilim,<br>
        Senda yangrar orzu-kuylarim.<br>
        Sen borsanki, o'zbek elim,<br>
        Baland doim g'urur-shonim.
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<br>` (break line) tegi bo'sh (yopiluvchi tegsiz) element bo'lib, faqatgina qatorni yangi satrdan boshlash uchun xizmat qiladi. She'rlar, qo'shiq matnlari yoki pochta manzillarida qator tashlash uchun ishlatiladi.

## Ishlash natijasi:
```text
To'rt misradan iborat she'riy parcha qator oralig'ida bo'shliq hosil qilmasdan bir tekis yangi satrlarga tushadi.
```

---

# 59-Topshiriq: <hr> tematik bo'linish chizig'i
## Topshiriq sharti:
Mavzular yoki fikrlar almashganda gorizontal ajratuvchi `<hr>` chizig'ini zamonaviy stillash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Hr Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 30px; }
        hr.modern-divider {
            border: 0;
            height: 2px;
            background-image: linear-gradient(to right, rgba(0,0,0,0), rgba(59,130,246,0.75), rgba(0,0,0,0));
            margin: 30px 0;
        }
    </style>
</head>
<body>
    <p>Birinchi bo'lim: HTML asoslari va matn teglari haqida qisqacha ma'lumot.</p>
    <hr class="modern-divider">
    <p>Ikkinchi bo'lim: CSS orqali ularni bezatish va zamonaviy ko'rinishga keltirish.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<hr>` (horizontal rule) elementi semantik jihatdan mavzuning tugashi va boshqa tematik bo'lim boshlanishini bildiradi. CSS orqali uni standart qora chiziqdan zamonaviy gradientli estetik ajratgichga aylantirish mumkin.

## Ishlash natijasi:
```text
Ikki xatboshi o'rtasida ikki cheti erib yo'qoluvchi moviy gradientli gorizontal nafis chiziq paydo bo'ladi.
```

---

# 60-Topshiriq: <strong> semantik muhimlik tegi
## Topshiriq sharti:
O'quvchi va qidiruv tizimlari uchun favqulodda muhim bo'lgan so'zlarni `<strong>` bilan belgilash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Strong Semantikasi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .warning { background: #fef2f2; border: 1px solid #f87171; color: #991b1b; padding: 15px; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="warning">
        <p><strong>DIQQAT:</strong> Parolingizni hech qachon uchinchi shaxslarga bermang! Bu <strong>xavfsizlik qoidalariga</strong> ziddir.</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<strong>` tegi semantik jihatdan matnning jiddiy ahamiyatga ega ekanligini (strong importance) bildiradi. Ekran o'quvchi qurilmalar bu so'zlarni jarangliroq va urg'u bilan o'qiydi. Brauzer esa ularni qalin (bold) qilib chizadi.

## Ishlash natijasi:
```text
Qizil ogohlantirish qutisi ichida 'DIQQAT:' va 'xavfsizlik qoidalariga' so'zlari to'q qora qalin harflar bilan ajralib turadi.
```

---

# 61-Topshiriq: <b> tegi — vizual qalinlashtirish
## Topshiriq sharti:
Hech qanday qo'shimcha semantik urg'usiz, faqat ko'rinish jihatdan qalin bo'lishi kerak bo'lgan so'zlarni `<b>` bilan yozish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>B Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
    </style>
</head>
<body>
    <p>Retsept: Xamirga 2 dona <b>tuxum</b>, 100g <b>sariyog'</b> va bir chimdim <b>tuz</b> solib qoring.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<b>` (bold) tegi matnni shunchaki qalin qilib ko'rsatish uchun xizmat qiladi, ammo unga `<strong>` kabi alohida muhimlik ma'nosi yuklanmaydi. Mahsulot tarkibi yoki kalit atamalarni vizual ajratishda qo'llaniladi.

## Ishlash natijasi:
```text
Matndagi 'tuxum', 'sariyog'' va 'tuz' so'zlari qalin harflar bilan ajratiladi.
```

---

# 62-Topshiriq: <em> tegi — semantik urg'u (emphasis)
## Topshiriq sharti:
Gapning ma'nosini o'zgartiruvchi og'zaki urg'uni `<em>` tegi orqali berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Em Semantikasi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; line-height: 1.6; }
    </style>
</head>
<body>
    <p>Men <em>ertaga</em> kelaman. (Boshqa kuni emas, aynan ertaga).</p>
    <p>Men ertaga <em>kelaman</em>. (Kelmasligim mumkin edi, lekin aniq kelaman).</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<em>` (emphasis) tegi gapdagi urg'u berilgan so'zni ifodalaydi. Ekran o'quvchi ovozli dastur urg'uli so'zni intonatsiya bilan o'qiydi. Brauzer sukut bo'yicha uni qiyalik (italic) uslubida ko'rsatadi.

## Ishlash natijasi:
```text
Ikki gapda tegishli so'zlar qiya shriftda ajratilib, urg'uning o'rni yaqqol ko'rinadi.
```

---

# 63-Topshiriq: <i> tegi — texnik yoki boshqa til atamalari
## Topshiriq sharti:
Semantik urg'u bo'lmagan, lekin ilmiy, biologik yoki chet tili so'zlarini qiyalikda ifodalovchi `<i>` tegi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>I Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
    </style>
</head>
<body>
    <p>Oq laylak lotin tilida <i>Ciconia ciconia</i> deb ataladi.</p>
    <p>Biznesda <i>status quo</i> holatini saqlash ko'pincha orqaga ketishni anglatadi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<i>` (idiomatic text) tegi muqobil ovoz yoki kayfiyatdagi matnlar, ilmiy nomlar, chet tilidagi iboralar yoki qahramonning ichki monologi uchun mo'ljallangan.

## Ishlash natijasi:
```text
Lotincha va xorijiy atamalar nafis qiyalikda aks etadi.
```

---

# 64-Topshiriq: <blockquote> va cite atributi — katta iqtibos
## Topshiriq sharti:
Boshqa manbadan olingan yirik iqtibosni semantik `<blockquote>` va havolali `cite` bilan stillash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Blockquote Tegi</title>
    <style>
        body { font-family: Georgia, serif; padding: 30px; }
        blockquote {
            margin: 0;
            padding: 15px 25px;
            background: #f8fafc;
            border-left: 5px solid #3b82f6;
            font-style: italic;
            font-size: 18px;
            color: #334155;
        }
        cite { display: block; margin-top: 10px; font-size: 14px; font-style: normal; color: #64748b; font-weight: bold; }
    </style>
</head>
<body>
    <blockquote cite="https://uz.wikipedia.org/wiki/Alisher_Navoiy">
        "Haq yo'lida kimki bir harf o'rgatmish ranj ila,<br>
        Aylamak bo'lmas ado oning haqin yuz ganj ila."
        <cite>— Alisher Navoiy</cite>
    </blockquote>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<blockquote>` tegi boshqa manbadan olingan mustaqil iqtibos bo'lagini ifodalaydi. `cite` atributi manba veb-manzilini (URL) saqlaydi, ichidagi `<cite>` tegi esa muallif yoki asar nomini ko'rsatish uchun ishlatiladi.

## Ishlash natijasi:
```text
Chap tomonida ko'k hoshiyasi bo'lgan nafis fonli iqtibos bloki va pastida qalin muallif nomi chiqadi.
```

---

# 65-Topshiriq: <q> qator ichidagi qisqa iqtibos
## Topshiriq sharti:
Matn oqimi ichidagi qisqa iqtiboslarni avtomatik qo'shtirnoqqa oluvchi `<q>` tegi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Q Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; font-size: 17px; }
    </style>
</head>
<body>
    <p>Ustozimiz doim: <q>Bilim olishdan hech qachon charchamang</q>, deb ta'kidlar edilar.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<q>` (inline quote) tegi matn ichidagi qisqa iqtiboslar uchundir. Brauzer uning atrofiga avtomatik tarzda tilga mos qo'shtirnoq belgisini (« » yoki “ ”) qo'yadi. Qo'lda qo'shtirnoq yozish talab etilmaydi.

## Ishlash natijasi:
```text
Matn ichida avtomatik qo'shtirnoqlarga olingan chiroyli iqtibos jumlasi aks etadi.
```

---

# 66-Topshiriq: <pre> oldindan formatlangan matn
## Topshiriq sharti:
Barcha bo'shliqlar, probellar va qator ko'chirishlarini aynan yozilganidek saqlab qoluvchi `<pre>` tegi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Pre Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        pre { background: #1e293b; color: #38bdf8; padding: 15px; border-radius: 6px; font-family: 'Courier New', monospace; }
    </style>
</head>
<body>
    <pre>
    * * *
   *     *
  *   *   *    ASCII SAN'ATI
   *     *
    * * *
    </pre>
</body>
</html>
```

## Tushuntirish va Mantiq:
Oddiy HTML teglari ichida bir nechta probel va `Enter` bosishlar bitta probelga aylanadi (whitespace collapse). `<pre>` tegi esa matndagi har bir bo'sh joy va yangi satrni asl holatida saqlaydi va monospaced (teng kenglikdagi) shriftda ko'rsatadi.

## Ishlash natijasi:
```text
To'q moviy fonda moviy rangli monospaced yulduzchalardan yasalgan figura va matn chiqadi.
```

---

# 67-Topshiriq: <code> dasturiy kod parchasini ifodalash
## Topshiriq sharti:
Matn ichida o'zgaruvchi yoki dasturlash kodi qismini semantik ajratuvchi `<code>` tegi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Code Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        code { background: #f1f5f9; color: #e11d48; padding: 2px 6px; border-radius: 4px; font-family: Consolas, monospace; font-size: 15px; }
    </style>
</head>
<body>
    <p>JavaScript-da konsolga ma'lumot chiqarish uchun <code>console.log('Salom')</code> buyrug'i qo'llaniladi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<code>` tegi dasturlash tillari kodi parchalarini ko'rsatish uchun semantik element hisoblanadi. U odatda monospaced shriftda aks etadi va CSS orqali fon hamda rang bilan boyitiladi.

## Ishlash natijasi:
```text
Matn orasida pushti-qizil rangda alohida ajralib turuvchi dastur kodi ko'rinadi.
```

---

# 68-Topshiriq: <kbd> klaviatura tugmalari belgisi
## Topshiriq sharti:
Foydalanuvchi bosishi kerak bo'lgan tugmalarni (shortcuts) ifodalovchi `<kbd>` tegi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Kbd Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        kbd {
            background-color: #f8fafc;
            border: 1px solid #94a3b8;
            border-bottom: 3px solid #64748b;
            border-radius: 4px;
            padding: 3px 8px;
            font-family: monospace;
            font-size: 13px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <p>Nusxa olish uchun <kbd>Ctrl</kbd> + <kbd>C</kbd>, joylashtirish uchun esa <kbd>Ctrl</kbd> + <kbd>V</kbd> tugmalarini bosing.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<kbd>` (keyboard input) tegi foydalanuvchi klaviaturadan kiritadigan tugmalar yoki kombinatsiyalarni bildiradi. CSS yordamida unga 3D tugmachasimon soya va relyef berish mumkin.

## Ishlash natijasi:
```text
Klaviaturaning jismoniy tugmachalariga o'xshash bo'rtib turuvchi kulrang tugmalar ko'rinadi.
```

---

# 69-Topshiriq: <samp> dastur yoki terminal natijasi
## Topshiriq sharti:
Kompyuter dasturi yoki buyruqlar satrining ekranga chiqargan natijasini ifodalovchi `<samp>` tegi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Samp Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .terminal { background: #000; color: #22c55e; padding: 15px; border-radius: 6px; font-family: monospace; }
    </style>
</head>
<body>
    <div class="terminal">
        <div>$ ping google.com</div>
        <samp>Reply from 142.250.185.78: bytes=32 time=24ms TTL=117</samp>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<samp>` (sample output) elementi dastur, skript yoki operatsion tizim bergan javob xabarini semantik belgilash uchun ishlatiladi.

## Ishlash natijasi:
```text
Qora terminal oynasida yashil rangda buyruq va dasturning javob natijasi aks etadi.
```

---

# 70-Topshiriq: <var> matematik va dasturlash o'zgaruvchisi
## Topshiriq sharti:
Formulalar yoki algoritmlardagi o'zgaruvchilarni ifodalovchi `<var>` tegi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Var Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        var { font-family: 'Times New Roman', serif; font-style: italic; font-weight: bold; color: #4338ca; }
    </style>
</head>
<body>
    <p>To'g'ri to'rtburchak yuzi: <var>S</var> = <var>a</var> &times; <var>b</var> formulasi orqali topiladi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<var>` (variable) tegi matematik tenglamalar yoki dasturiy tushuntirishlardagi o'zgaruvchilarni bildiradi va odatda qiyalikda ko'rsatiladi.

## Ishlash natijasi:
```text
Binafsharang qiyalikdagi S, a, b harflari bilan ifodalangan chiroyli geometrik formula chiqadi.
```

---

# 71-Topshiriq: <sub> quyi indeks tegi
## Topshiriq sharti:
Kimyoviy formulalar va matematik quyi indekslarni `<sub>` orqali formatlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Sub Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; font-size: 18px; }
    </style>
</head>
<body>
    <p>Suvning kimyoviy formulasi: <strong>H<sub>2</sub>O</strong></p>
    <p>Glyukoza formulasi: <strong>C<sub>6</sub>H<sub>12</sub>O<sub>6</sub></strong></p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<sub>` (subscript) tegi matnni qatordan biroz pastga tushirib, kichikroq hajmda yozadi. Bu kimyoviy elementlar sonini yoki matematik indekslarni (x1, x2) ko'rsatishda zarur.

## Ishlash natijasi:
```text
Raqamlari pastga tushirilgan to'g'ri kimyoviy formulalar ko'rinadi.
```

---

# 72-Topshiriq: <sup> yuqori indeks tegi
## Topshiriq sharti:
Matematik darajalar, kvadratlar va havolalarni `<sup>` bilan ko'rsatish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Sup Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; font-size: 18px; }
    </style>
</head>
<body>
    <p>Pifagor teoremasi: <var>a</var><sup>2</sup> + <var>b</var><sup>2</sup> = <var>c</var><sup>2</sup></p>
    <p>Eynshteyn formulasi: <var>E</var> = <var>m</var><var>c</var><sup>2</sup></p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<sup>` (superscript) tegi matnni qatordan yuqoriga chiqarib, kichik hajmda chizadi. Matematik darajalar, kvant fizikasi va sahifa osti izohlari raqamlarida ishlatiladi.

## Ishlash natijasi:
```text
Kvadrat darajalari yuqoriga ko'tarilgan klassik matematik teoremalar ko'rinadi.
```

---

# 73-Topshiriq: <del> o'chirilgan yoki bekor qilingan matn
## Topshiriq sharti:
Hujjatdan o'chirilgan yoki yangilangan eski matnni chizilgan holatda ifodalovchi `<del>` tegi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Del Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        del { color: #dc2626; }
    </style>
</head>
<body>
    <p>Ertangi dars soat <del>14:00 da</del> emas, balki 16:00 da boshlanadi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<del>` tegi hujjatning tahrirlanish tarixida o'chirilgan qismini bildiradi. Brauzer uning ustidan chiziq tortadi (strikethrough).

## Ishlash natijasi:
```text
Ustidan qizil chiziq tortilgan '14:00 da' so'zi aks etadi.
```

---

# 74-Topshiriq: <ins> yangi kiritilgan matn
## Topshiriq sharti:
Tahrir davomida yangidan qo'shilgan matnni semantik ifodalovchi `<ins>` tegi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Ins Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        ins { background: #dcfce7; color: #15803d; text-decoration: none; border-bottom: 2px solid #16a34a; }
    </style>
</head>
<body>
    <p>Bizning xizmatlar safiga <ins>Sun'iy Intellekt integratsiyasi</ins> ham qo'shildi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<ins>` (inserted text) elementi hujjatga yangi qo'shilgan axborotni ifodalaydi. Sukut bo'yicha tagiga chiziladi, CSS orqali yashil rang bilan boyitilishi odat tusiga kirgan.

## Ishlash natijasi:
```text
Yashil fon va tagchiziq bilan ajratilgan yangi xizmat nomi ko'rinadi.
```

---

# 75-Topshiriq: <s> endi dolzarb bo'lmagan matn
## Topshiriq sharti:
Chegirma e'lonlarida eski narxni ifodalash uchun `<s>` tegi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>S Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .old-price { color: #94a3b8; font-size: 16px; }
        .new-price { color: #16a34a; font-size: 22px; font-weight: bold; margin-left: 10px; }
    </style>
</head>
<body>
    <p>Yillik obuna: <s class="old-price">1 200 000 so'm</s> <span class="new-price">790 000 so'm</span></p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<s>` (strikethrough) tegi endi to'g'ri yoki dolzarb bo'lmagan ma'lumotni ustidan chizish uchun xizmat qiladi. Tijorat saytlarida eski narxni ko'rsatishda juda ommabop.

## Ishlash natijasi:
```text
Kulrang usti chizilgan eski narx va yonida yirik yashil yangi narx ko'rinadi.
```

---

# 76-Topshiriq: <small> mayda matn va nozik shartlar
## Topshiriq sharti:
Litsenziyalar, mualliflik eslatmalari va ogohlantirishlar uchun `<small>` tegi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Small Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
    </style>
</head>
<body>
    <p>Xaridingiz uchun 1 yil bepul kafolat beriladi.</p>
    <p><small>* Kafolat mexanik shikastlanishlarga nisbatan qo'llanilmaydi.</small></p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<small>` tegi asosiy matndan bir pog'ona kichikroq bo'lib, nozik shartlar, qo'shimcha yuridik eslatmalar yoki podval ma'lumotlari uchun semantik jihatdan xizmat qiladi.

## Ishlash natijasi:
```text
Yulduzcha bilan boshlanuvchi kichik shriftli ogohlantiruvchi yozuv ko'rinadi.
```

---

# 77-Topshiriq: <abbr> qisqartma so'zlar va uning title atributi
## Topshiriq sharti:
Abbreviatura va qisqartmalarning to'liq ma'nosini sichqoncha borganda ko'rsatuvchi `<abbr>` tegi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Abbr Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        abbr { text-decoration: underline dotted #0284c7; cursor: help; }
    </style>
</head>
<body>
    <p>O'zbekistonda <abbr title="Axborot Texnologiyalari">IT</abbr> sohasi jadal rivojlanmoqda.</p>
    <p>Veb standartlarini <abbr title="World Wide Web Consortium">W3C</abbr> tashkiloti boshqaradi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<abbr>` (abbreviation) tegi qisqartma so'zlar uchun qo'llaniladi. `title` atributiga qisqartmaning to'liq yoyilmasi yoziladi va foydalanuvchi uning ustiga borganda ochiluvchi qalqib chiquvchi oyna (tooltip) chiqadi.

## Ishlash natijasi:
```text
Nuqtali chiziq bilan belgilangan 'IT' va 'W3C' qisqartmalari ko'rinadi; kursor borganda to'liq nomi ochiladi.
```

---

# 78-Topshiriq: <dfn> atama ta'rifi tegi
## Topshiriq sharti:
Matnda birinchi bor tilga olinayotgan yangi ilmiy yoki texnik atama ta'rifini `<dfn>` orqali belgilash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Dfn Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        dfn { font-weight: bold; color: #7c3aed; }
    </style>
</head>
<body>
    <p><dfn>Semantika</dfn> — bu kod elementlarining faqat ko'rinishi emas, balki ularning asl ma'no va mohiyatini ifodalashidir.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<dfn>` (definition) tegi matnda ta'riflanayotgan asosiy atamani bildiradi. Qidiruv botlari va ensiklopedik tizimlar bu orqali qaysi so'z ta'riflanayotganini tushunadi.

## Ishlash natijasi:
```text
Binafsharang va qalin harflar bilan ta'kidlangan 'Semantika' so'zi va uning ortidan ta'rifi joylashadi.
```

---

# 79-Topshiriq: <bdi> ikki yo'nalishli matnlarni ajratish
## Topshiriq sharti:
O'ngdan chapga (RTL) va chapdan o'ngga (LTR) yoziluvchi matnlar aralashganda xatoliklarni oldini oluvchi `<bdi>` tegi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Bdi Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
    </style>
</head>
<body>
    <ul>
        <li>Foydalanuvchi <bdi>Ali</bdi>: 100 ball</li>
        <li>Foydalanuvchi <bdi>إبراهيم</bdi>: 95 ball</li>
    </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<bdi>` (Bi-Directional Isolation) tegi ichidagi matnni tashqi atrofdagi matn yo'nalishidan ajratadi. Arabcha yoki ibroniycha kabi o'ngdan chapga yoziladigan ismlar chapdan o'ngga yozilgan ro'yxat raqamlarini buzib yubormasligini ta'minlaydi.

## Ishlash natijasi:
```text
Arabcha ism va uning yonidagi ball sonlari o'rin almashib ketmasdan, tartibli ro'yxatda to'g'ri chiqadi.
```

---

# 80-Topshiriq: <bdo> matn yo'nalishini majburiy o'zgartirish
## Topshiriq sharti:
Matn harflarining o'qilish yo'nalishini sun'iy ravishda teskarisiga o'giruvchi `<bdo dir='rtl'>` tegi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Bdo Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; font-size: 18px; }
    </style>
</head>
<body>
    <p>Oddiy matn: Dasturlash</p>
    <p>O'ngdan chapga majburiy: <bdo dir="rtl">Dasturlash</bdo></p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<bdo>` (Bi-Directional Override) tegi matnning tabiiy yo'nalishini e'tiborsiz qoldirib, uni `dir` atributida ko'rsatilgan tartibda (rtl - o'ngdan chapga yoki ltr - chapdan o'ngga) chiqaradi.

## Ishlash natijasi:
```text
'Dasturlash' so'zi ikkinchi qatorda harflari teskari 'hsalrutsaD' ko'rinishida chiqadi.
```

---

# 81-Topshiriq: <ruby>, <rt> va <rp> fonetik talaffuz belgilari
## Topshiriq sharti:
Sharq tillari (yapon, xitoy) iyerogliflari ustiga talaffuzini ko'rsatuvchi ruby belgilari.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Ruby Elementlari</title>
    <style>
        body { font-family: sans-serif; padding: 30px; font-size: 24px; }
        ruby { font-size: 28px; }
        rt { font-size: 14px; color: #2563eb; }
    </style>
</head>
<body>
    <p>
        <ruby>
            漢 <rp>(</rp><rt>kan</rt><rp>)</rp>
            字 <rp>(</rp><rt>ji</rt><rp>)</rp>
        </ruby>
    </p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<ruby>` konteyneri sharq tillaridagi murakkab iyerogliflarni o'raydi. `<rt>` tegi uning ustidagi kichik talaffuz so'zini, `<rp>` esa ruby tegini qo'llab-quvvatlamaydigan eski brauzerlar uchun qavslarni belgilaydi.

## Ishlash natijasi:
```text
Yaponcha iyerogliflar ustida moviy rangda ularning lotincha 'kan' va 'ji' talaffuzlari joylashadi.
```

---

# 82-Topshiriq: <wbr> uzun so'zlarni xavfsiz bo'g'inlab ko'chirish
## Topshiriq sharti:
Ekran torayganda uzun so'z yoki URL manzillar qayerdan yangi qatorga tushishi mumkinligini bildiruvchi `<wbr>` tegi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Wbr Tegi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .box { width: 180px; border: 1px solid #94a3b8; padding: 10px; background: #f8fafc; }
    </style>
</head>
<body>
    <div class="box">
        JudaUzunSo'z<wbr>YangiQatorga<wbr>ChiroyliTushadi
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<wbr>` (word break opportunity) brauzerga agar zarurat tug'ilsa (masalan, mobil ekranda konteyner torayganda), so'zni aynan shu nuqtadan bo'lib keyingi satrga tushirishga ruxsat beradi.

## Ishlash natijasi:
```text
Tor qutida so'z hoshiyadan chiqib ketmasdan, ko'rsatilgan bo'g'in bo'yicha keyingi qatorga ko'chadi.
```

---

# 83-Topshiriq: HTML maxsus belgilari (Entities: &copy;, &lt;, &gt;, &amp;)
## Topshiriq sharti:
HTML sintaksisida band qilingan belgilar va maxsus belgilarni to'g'ri kodlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>HTML Entities</title>
    <style>
        body { font-family: monospace; padding: 25px; font-size: 16px; }
        .entity-card { background: #f1f5f9; padding: 15px; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="entity-card">
        &copy; Mualliflik huquqi<br>
        5 &lt; 10 (Kichik belgisi)<br>
        15 &gt; 8 (Katta belgisi)<br>
        HTML &amp; CSS (Ambersand belgisi)<br>
        Bo'shliq&nbsp;&nbsp;&nbsp;qoldirish
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<` va `>` belgilari teg ochish va yopish uchun ishlatilganligi sababli oddiy matnda `&lt;` va `&gt;` orqali yoziladi. `&copy;` mualliflik belgisini, `&nbsp;` esa uzilmas bo'shliqni yaratadi.

## Ishlash natijasi:
```text
Maxsus belgilar: ©, <, >, &, va uchta uzilmas probel bir xil monospaced formatda aks etadi.
```

---

# 84-Topshiriq: <cite> tegi bilan ijodiy asar nomini ko'rsatish
## Topshiriq sharti:
Kitob, film, qo'shiq yoki ilmiy maqola nomlarini semantik to'g'ri ifodalovchi `<cite>` tegi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Cite Tegi</title>
    <style>
        body { font-family: Georgia, serif; padding: 25px; }
        cite { color: #b45309; font-weight: 500; }
    </style>
</head>
<body>
    <p>Abdulla Qodiriyning <cite>O'tkan kunlar</cite> romani o'zbek adabiyotining durdonasidir.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<cite>` tegi kitob, rasm, spektakl, musiqa yoki veb-sayt kabi ijodiy asar nomlarini ifodalash uchun xizmat qiladi. Odam ismiga nisbatan emas, asarga nisbatan ishlatiladi.

## Ishlash natijasi:
```text
Jigarrang qiyalikdagi 'O'tkan kunlar' asari nomi matn ichida ifodali ajraladi.
```

---

# 85-Topshiriq: <pre> va <code> teglarini birlashtirib kod bloki yasash
## Topshiriq sharti:
Ko'p qatorli dasturlash kodlarini chiroyli sintaksis bilan o'rashning standart andozasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Pre va Code</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        pre { background: #0f172a; padding: 20px; border-radius: 8px; overflow-x: auto; }
        code { color: #38bdf8; font-family: 'Fira Code', Consolas, monospace; font-size: 14px; }
        .keyword { color: #f43f5e; }
        .string { color: #a3e635; }
    </style>
</head>
<body>
    <pre><code><span class="keyword">function</span> salomBer(ism) {
    <span class="keyword">return</span> <span class="string">`Salom, ${ism}!`</span>;
}</code></pre>
</body>
</html>
```

## Tushuntirish va Mantiq:
Web dasturlashda ko'p qatorli kod bloklarini chiqarish uchun `<pre><code>...</code></pre>` kombinatsiyasi qat'iy standartdir. `<pre>` formatni saqlaydi, `<code>` esa semantikasini beradi.

## Ishlash natijasi:
```text
Qora fonda qizil kalit so'zlar, moviy funksiya nomi va yashil matnli JavaScript kodi bloki chiqadi.
```

---

# 86-Topshiriq: Klaviatura yorliqlari (shortcuts) yordamchi paneli
## Topshiriq sharti:
Matn muharriri yoki dasturdagi tugmalar birikmasini chiroyli jadval ko'rinishida yasash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Shortcuts Ro'yxati</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .shortcut-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #e2e8f0; max-width: 350px; }
        kbd { background: #f1f5f9; border: 1px solid #cbd5e1; padding: 2px 6px; border-radius: 4px; font-size: 12px; }
    </style>
</head>
<body>
    <h3>Tezkor Tugmalar</h3>
    <div class="shortcut-row"><span>Qidiruv</span><span><kbd>Ctrl</kbd> + <kbd>F</kbd></span></div>
    <div class="shortcut-row"><span>Saqlash</span><span><kbd>Ctrl</kbd> + <kbd>S</kbd></span></div>
    <div class="shortcut-row"><span>Hammasini belgilash</span><span><kbd>Ctrl</kbd> + <kbd>A</kbd></span></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu tuzilmada amaliy buyruq nomi va unga mos tugmalar kombinatsiyasi `<kbd>` teglari orqali foydalanuvchiga qulay ko'rsatiladi.

## Ishlash natijasi:
```text
Chapda amal nomi, o'ngda esa 3D tugmacha uslubidagi klaviatura yorliqlari joylashgan ixcham jadval paydo bo'ladi.
```

---

# 87-Topshiriq: Kimyoviy reaksiya tenglamasini sub va sup bilan ifodalash
## Topshiriq sharti:
Ionlar va kimyoviy birikmalar reaksiyasini to'g'ri ilmiy formatda chiqarish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Kimyoviy Reaksiya</title>
    <style>
        body { font-family: sans-serif; padding: 25px; font-size: 20px; }
        .formula-box { background: #eff6ff; border: 1px solid #bfdbfe; padding: 15px; border-radius: 8px; display: inline-block; }
    </style>
</head>
<body>
    <div class="formula-box">
        2H<sub>2</sub> + O<sub>2</sub> &rarr; 2H<sub>2</sub>O
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Kimyoviy elementlar miqdori `<sub>` tegi orqali indeks qilinadi va `&rarr;` orqali reaksiya yo'nalishi ko'rsatiladi.

## Ishlash natijasi:
```text
Moviy qutida vodorod va kislorodning reaksiyaga kirishib suv hosil qilish tenglamasi ilmiy aniqlikda namoyon bo'ladi.
```

---

# 88-Topshiriq: Eski va yangi narx kombinatsiyasi (s va ins)
## Topshiriq sharti:
E-tijorat tizimlari uchun mahsulot chegirmasini semantik ko'rsatish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Chegirma Narxi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .price-tag s { color: #94a3b8; font-size: 16px; margin-right: 8px; }
        .price-tag ins { color: #059669; font-size: 24px; font-weight: bold; text-decoration: none; }
    </style>
</head>
<body>
    <div class="price-tag">
        <s>500 000 so'm</s>
        <ins>350 000 so'm</ins>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<s>` tegi eski narxni chizilgan ko'rsatadi, `<ins>` esa yangilangan narxni ifodalab beradi. Bu qidiruv botlariga narx o'zgarishi tarixini anglatadi.

## Ishlash natijasi:
```text
Chizilgan kulrang eski narx va uning yonida katta qalin yashil chegirmali narx ko'rinadi.
```

---

# 89-Topshiriq: Gazeta uslubidagi matn kirish qismi (Lead Paragraph)
## Topshiriq sharti:
Maqolaning birinchi xatboshisini kattaroq va ifodaliroq stillash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Lead Paragraph</title>
    <style>
        body { font-family: Georgia, serif; max-width: 650px; margin: 30px auto; padding: 0 15px; }
        .lead { font-size: 20px; line-height: 1.6; color: #1e293b; font-weight: 500; }
        p { line-height: 1.8; color: #475569; }
    </style>
</head>
<body>
    <h1>Samarqandda Katta IT Sammit Boshlandi</h1>
    <p class="lead">Dunyoning 40 dan ortiq mamlakatlaridan kelgan minglab mutaxassislar bugun qadimiy Samarqand zaminida sun'iy intellekt kelajagini muhokama qilmoqdalar.</p>
    <p>Tadbir davomida o'nlab yangi startaplar taqdimoti va innovatsion kelishuvlar imzolanishi kutilmoqda.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Jurnalistika va bloglarda 'Lead' xatboshi boshqa matnlarga nisbatan kattaroq hajm va yuqori kontrastga ega bo'lib, o'quvchini darhol mavzuga jalb qiladi.

## Ishlash natijasi:
```text
Sarlavhadan so'ng keladigan birinchi xatboshi ancha yirik va qalinroq bo'lib o'quvchi nigohini tortadi.
```

---

# 90-Topshiriq: Drop Cap effekti — matnning birinchi bosh harfini yiriklashtirish
## Topshiriq sharti:
Klassik kitob uslubida maqolaning ilk harfini bir necha satr bo'yi kattalashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Drop Cap Effekti</title>
    <style>
        body { font-family: 'Times New Roman', serif; max-width: 600px; margin: 40px auto; line-height: 1.8; }
        p.styled-text::first-letter {
            font-size: 3.5em;
            float: left;
            line-height: 0.8;
            margin-right: 10px;
            color: #1e3a8a;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <p class="styled-text">Tarix sahifalariga nazar tashlasak, ilm-fan va tafakkur rivojlangan davrlarda har doim jamiyat yuksak taraqqiyotga erishganini ko'rishimiz mumkin.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`::first-letter` psevdo-elementidan foydalanib, matnning birinchi harfi `float: left` bilan chapga suriladi va shrift o'lchami kattalashtirilib, kitobiy 'bosh harf' san'ati hosil qilinadi.

## Ishlash natijasi:
```text
Matn boshidagi 'T' harfi ulkan to'q ko'k harf bo'lib bir nechta qator bo'yicha ajralib turadi.
```

---

# 91-Topshiriq: Matnga maxsus marker effekti (Highlight effect)
## Topshiriq sharti:
CSS linear-gradient yordamida matn tagiga tabiiy kantselyariya flomasteri chizig'ini berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Marker Effekti</title>
    <style>
        body { font-family: sans-serif; padding: 30px; font-size: 20px; line-height: 1.6; }
        .highlight-pen {
            background: linear-gradient(104deg, rgba(254,240,138,0) 0.9%, rgba(254,240,138,1) 2.4%, rgba(254,240,138,0.7) 98%);
            padding: 2px 6px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <p>Muvaffaqiyatga erishishning asosiy siri — bu <span class="highlight-pen">har kuni to'xtovsiz intilish</span> va mehnatdir.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Gradientdan foydalanib flomaster chizig'i taassurotini qoldiruvchi qulay vizual effekt yaratiladi.

## Ishlash natijasi:
```text
Matn ichidagi 'har kuni to'xtovsiz intilish' jumlasi sariq kantselyariya markeri bilan bo'yalgan ko'rinishda bo'ladi.
```

---

# 92-Topshiriq: Iqtibos blokiga chiroyli qo'shtirnoq belgisi berish
## Topshiriq sharti:
CSS psevdo-elementlari orqali ulkan dekorativ tirnoq belgilarini joylashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Dekorativ Tirnoq</title>
    <style>
        body { font-family: Georgia, serif; padding: 40px; }
        .quote-box {
            position: relative;
            background: #f1f5f9;
            padding: 30px 40px;
            border-radius: 8px;
            max-width: 500px;
        }
        .quote-box::before {
            content: "“";
            position: absolute;
            top: 5px;
            left: 10px;
            font-size: 70px;
            color: #94a3b8;
            line-height: 1;
        }
    </style>
</head>
<body>
    <div class="quote-box">
        <p>Haqiqiy bilim — bu inson o'zining nimanidir bilmasligini anglashi va o'rganishda davom etishidir.</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`::before` psevdo-elementi va `content: '“'` orqali fon sifatida ulkan dekorativ qo'shtirnoq joylashtirilib, estetik iqtibos kartochkasi yaratiladi.

## Ishlash natijasi:
```text
Och kulrang kartochka tepasida yirik och kulrang qo'shtirnoq belgisi va uning ustida ifodali matn aks etadi.
```

---

# 93-Topshiriq: Linux Terminal / Konsol buyruqlari darchasi
## Topshiriq sharti:
Pre, code va samp yordamida haqiqiy dasturchilar terminali interfeysini stillash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Terminal Darchasi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .window { background: #1e1e1e; border-radius: 8px; overflow: hidden; max-width: 500px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
        .window-bar { background: #2d2d2d; padding: 8px 12px; display: flex; gap: 6px; }
        .dot { width: 12px; height: 12px; border-radius: 50%; }
        .dot-red { background: #ff5f56; }
        .dot-yellow { background: #ffbd2e; }
        .dot-green { background: #27c93f; }
        pre { margin: 0; padding: 15px; color: #fff; font-family: monospace; }
        .prompt { color: #4ade80; }
    </style>
</head>
<body>
    <div class="window">
        <div class="window-bar">
            <span class="dot dot-red"></span>
            <span class="dot dot-yellow"></span>
            <span class="dot dot-green"></span>
        </div>
        <pre><code><span class="prompt">user@server:~$</span> npm install antigravity
<samp>added 42 packages in 1.4s</samp>
<span class="prompt">user@server:~$</span></code></pre>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
MacOS va Linux uslubidagi 3 ta rangli tugmacha bilan jihozlangan qora terminal oynasi veb-saytda kod namoyishi uchun eng chiroyli vizual vositadir.

## Ishlash natijasi:
```text
Tepasida qizil, sariq, yashil tugmachalari bor qora darchada yashil rangli konsol buyrug'i va oq rangli o'rnatish natijasi ko'rinadi.
```

---

# 94-Topshiriq: Matematik teoremalar va formulalarni formatlash
## Topshiriq sharti:
Var, sup va sub bilan murakkab matematik tenglamalarni ifodalash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Kvadrat Tenglama</title>
    <style>
        body { font-family: 'Times New Roman', serif; padding: 30px; font-size: 22px; }
        .math-block { background: #fafafa; border: 1px solid #e5e5e5; padding: 20px; text-align: center; max-width: 400px; }
    </style>
</head>
<body>
    <div class="math-block">
        <var>a</var><var>x</var><sup>2</sup> + <var>b</var><var>x</var> + <var>c</var> = 0<br><br>
        <var>D</var> = <var>b</var><sup>2</sup> - 4<var>a</var><var>c</var>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
To'liq ilmiy matematik format: o'zgaruvchilar `<var>` da, daraja ko'rsatkichlari `<sup>` da, ko'paytuvchilar esa qat'iy standartda keltiriladi.

## Ishlash natijasi:
```text
Markazlashgan blokda toza va tiniq kvadrat tenglama hamda diskriminant formulasi ko'rinadi.
```

---

# 95-Topshiriq: Atamalar izohli lug'ati kartochkasi (dfn va abbr)
## Topshiriq sharti:
Lug'at atamasi, uning transkripsiyasi va izohini birlashtirgan semantik karta.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Lug'at Kartochkasi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .dict-card { border-left: 4px solid #8b5cf6; padding: 15px 20px; background: #f5f3ff; max-width: 450px; }
        .term { font-size: 20px; font-weight: bold; color: #6d28d9; }
    </style>
</head>
<body>
    <div class="dict-card">
        <div class="term"><dfn>API</dfn> [ay-pee-eye]</div>
        <p><abbr title="Application Programming Interface">Dasturiy interfeys</abbr> — ikki dasturning o'zaro ma'lumot almashishiga imkon beruvchi vosita.</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<dfn>` atama nomini, `<abbr>` uning to'liq yoyilmasini ta'minlaydi. Foydalanuvchi qisqartmani ham, uning ta'rifini ham bir joyda o'rganadi.

## Ishlash natijasi:
```text
Siyohrang chiziqli nafis kartochkada API atamasi, uning o'qilishi va batafsil izohi ko'rinadi.
```

---

# 96-Topshiriq: Ko'p tilli ro'yxatda bdi bilan xavfsiz ifodalash
## Topshiriq sharti:
Foydalanuvchilar turli tillarda (kirill, lotin, arab) kiritgan ismlarini tartibli ro'yxatlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Bdi Ro'yxat</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        ol { padding-left: 20px; }
        li { margin-bottom: 8px; }
    </style>
</head>
<body>
    <h3>G'oliblar ro'yxati:</h3>
    <ol>
        <li>Foydalanuvchi <bdi>Anvar</bdi> — 1-o'rin</li>
        <li>Foydalanuvchi <bdi>عمر</bdi> — 2-o'rin</li>
        <li>Foydalanuvchi <bdi>Diyora</bdi> — 3-o'rin</li>
    </ol>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<bdi>` bo'lmasa, arabcha harflar o'zidan keyingi '— 2-o'rin' yozuvini chapga surib, tartibni buzib yuborishi mumkin edi. `<bdi>` uni xavfsiz izolyatsiyalaydi.

## Ishlash natijasi:
```text
Uch kishilik tartibli ro'yxatda har bir ism va uning o'rni joy-joyida toza chiqadi.
```

---

# 97-Topshiriq: She'riy parchalarni pre va em orqali formatlash
## Topshiriq sharti:
Misralarning joylashuvi va ohangdorligini brauzerda buzmasdan ifodalash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>She'riy Format</title>
    <style>
        body { font-family: 'Georgia', serif; padding: 30px; background: #fffbeb; }
        pre { font-family: inherit; font-size: 18px; line-height: 1.8; color: #78350f; }
    </style>
</head>
<body>
    <pre><em>
        Yurtim, seni ko'rdim ko'ngil ko'zida,
        Har bir giyohingda oftob izi bor.
        Bobolar nafasi qolgan so'zingda,
        Har bir qarichingda buyuk tarix bor.
    </em></pre>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<pre>` va `font-family: inherit` kombinatsiyasi she'r misralaridagi barcha bo'shliqlarni saqlab qoladi, `<em>` esa she'riy ohangdorlik va nafislik baxsh etadi.

## Ishlash natijasi:
```text
Iliq sarg'ish fonda to'rt qatorli qiyalikdagi go'zal she'riy parcha monospaced bo'lmagan serif shriftda chiroyli ko'rinadi.
```

---

# 98-Topshiriq: Matn ichidagi maxfiy qismni yashirish (Spoiler effekti)
## Topshiriq sharti:
Faqat sichqoncha ustiga borganda ko'rinadigan sirli matn yaratish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Spoiler Effekti</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .spoiler {
            background-color: #1e293b;
            color: #1e293b;
            padding: 2px 6px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .spoiler:hover {
            background-color: #e2e8f0;
            color: #0f172a;
        }
    </style>
</head>
<body>
    <p>Filmning oxirida bosh qahramon <span class="spoiler">aslida politsiya xodimi</span> ekanligi ma'lum bo'ladi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Qora fon ustiga xuddi shu rangdagi matn beriladi, kursor ustiga borganda esa fon och kulrangga va matn to'q rangga o'zgarib maxfiy sir fosh bo'ladi.

## Ishlash natijasi:
```text
Matn ichida qora to'rtburchak turadi; kursor borganda uning ichidagi yashirin 'aslida politsiya xodimi' so'zlari ochiladi.
```

---

# 99-Topshiriq: Tipografik xatolar va muvaffaqiyat bildirishnomalari
## Topshiriq sharti:
Tizim xabarlari (Error, Success, Warning) uchun to'g'ri tipografika va ranglar mutanosibligi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Xabarnomalar Tipografikasi</title>
    <style>
        body { font-family: sans-serif; padding: 25px; }
        .alert { padding: 12px 16px; border-radius: 6px; margin-bottom: 12px; font-size: 14px; }
        .alert-success { background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
        .alert-error { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
    </style>
</head>
<body>
    <div class="alert alert-success">
        <strong>Muvaffaqiyat!</strong> Profil ma'lumotlaringiz yangilandi.
    </div>
    <div class="alert alert-error">
        <strong>Xatolik!</strong> Parol kamida 8 ta belgidan iborat bo'lishi kerak.
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Xabarnomalarda `<strong>` kalit so'zni ajratib ko'rsatadi, fonga mos yumshoq qoraytirilgan matn rangi esa ko'zni charchatmaydi va xabarni tez anglashga yordam beradi.

## Ishlash natijasi:
```text
Biri yashil, biri qizil rangli ikkita nafis bildirishnoma xabarlari aks etadi.
```

---

# 100-Topshiriq: Tipografik jihatdan mukammal uzun o'qish (Longread) maqola shabloni
## Topshiriq sharti:
O'qish uchun eng qulay shrift o'lchami, qator balandligi (line-height) va oraliqlarga ega ideal maqola maketi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ideal Tipografik Maqola</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #fff;
            color: #24292f;
            line-height: 1.75;
            padding: 40px 20px;
        }
        article {
            max-width: 680px;
            margin: 0 auto;
        }
        h1 {
            font-size: 2.25rem;
            line-height: 1.25;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }
        .byline {
            color: #57606a;
            font-size: 0.95rem;
            margin-bottom: 2rem;
        }
        p {
            font-size: 1.125rem;
            margin-bottom: 1.5rem;
        }
        blockquote {
            border-left: 4px solid #0969da;
            padding-left: 1rem;
            margin: 2rem 0;
            color: #57606a;
            font-style: italic;
        }
    </style>
</head>
<body>
    <article>
        <h1>Vebda Matn O'qish Madaniyati va Zamonaviy Tipografika</h1>
        <div class="byline">Muallif: Alisher Zokirov &bull; 8 daqiqalik o'qish</div>
        <p>Inson ko'zi kompyuter va mobil ekranlaridan matn o'qiyotganda qog'ozdagiga qaraganda ancha tez toliqadi. Shu bois zamonaviy veb-dizaynda qator kengligi 60-75 ta belgidan oshmasligi (max-width: 680px) oltin qoida sanaladi.</p>
        <blockquote>
            "Yaxshi tipografika sezilmaydi, yomon tipografika esa darhol ko'zga tashlanadi va o'quvchini charchatadi."
        </blockquote>
        <p>Qatorlararo masofa (line-height: 1.75) va kontrast ranglarning to'g'ri tanlanishi o'quvchiga maqolani bir nafasda o'qib tugatish imkonini beradi.</p>
    </article>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu andoza veb-tipografikaning barcha jahon standartlarini (oltin qator kengligi 680px, qulay 1.125rem shrift, 1.75 line-height, salbiy letter-spacing sarlavhada) o'zida mujassam etgan mukammal o'quv shablonidir.

## Ishlash natijasi:
```text
Medium yoki Apple kabi yetakchi platformalarga xos, ko'zga nihoyatda yoqadigan, o'qilishi juda yengil va professional maqola sahifasi gavdalanadi.
```

---

