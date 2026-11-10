# CSS Asoslari va Selektorlar (301-350)

# 301-Topshiriq: CSS ulashning 3 usuli: Inline, Internal va External
## Topshiriq sharti:
Uch xil CSS ulash usulini bitta sahifada qo'llab, ularning farqini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>CSS Ulash Usullari</title>
    <!-- 1. External CSS (Tashqi fayl) -->
    <link rel="stylesheet" href="style.css">
    <!-- 2. Internal CSS (Ichki stil tegi) -->
    <style>
        .internal-box { background: #e0f2fe; padding: 15px; border-radius: 6px; }
    </style>
</head>
<body>
    <!-- 3. Inline CSS (Qator ichi stillash) -->
    <div style="color: #dc2626; font-weight: bold;">Inline CSS: To'g'ridan-to'g'ri elementda</div>
    <div class="internal-box">Internal CSS: Head ichidagi style tegida</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Inline CSS faqat bitta elementga tegishli bo'lib, `style` atributi orqali yoziladi. Internal CSS butun sahifaga `<style>` tegi orqali ta'sir qiladi. External CSS esa `.css` kengaytmali alohida faylda saqlanadi va butun saytdagi barcha sahifalar uchun umumiy uslub yaratishning eng to'g'ri yo'lidir.

## Ishlash natijasi:
```text
Qizil rangli inline matn va ostida moviy fondagi internal stil berilgan blok ko'rinadi.
```

---

# 302-Topshiriq: Tashqi CSS faylining keshlanishi va afzalliklari
## Topshiriq sharti:
Saytning barcha sahifalari uchun yagona style.css faylini ulash va tezlik afzalligi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>External CSS</title>
    <link rel="stylesheet" href="/assets/css/main.css">
</head>
<body>
    <h1>Tashqi CSS Fayli</h1>
    <p>Brauzer ushbu CSS faylini bir marta yuklab oladi va keshda (cache) saqlaydi. Keyingi sahifalar ochilganda internet trafigi sarflanmaydi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`<link rel='stylesheet' href='...'>` tashqi CSS faylini ulaydi. U kodning HTML bilan aralashib ketishini oldini oladi (Separation of Concerns) va keshlanish hisobiga saytni soniyaning ulushlarida ochilishini ta'minlaydi.

## Ishlash natijasi:
```text
Tashqi fayl stillari yuklangan toza va mustaqil sahifa aks etadi.
```

---

# 303-Topshiriq: @import qoidasi va uning ishlash mexanizmi
## Topshiriq sharti:
Bitta CSS fayli ichidan boshqa CSS fayllarini import qilish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>CSS Import</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        body { font-family: 'Roboto', sans-serif; padding: 25px; }
    </style>
</head>
<body>
    <p>Ushbu sahifada Google Fonts shriflari @import orqali yuklandi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`@import url('...');` har doim CSS faylning eng birinchi qatorida turishi shart. Biroq uning kamchiligi shundaki, u brauzerda ketma-ket (parallel emas) yuklanish zanjirini hosil qiladi va sahifani sekinlashtirishi mumkin.

## Ishlash natijasi:
```text
Google Roboto zamonaviy shriftida yozilgan chiroyli matn chiqadi.
```

---

# 304-Topshiriq: Universal selektor * va CSS Reset
## Topshiriq sharti:
Barcha elementlarning standart noqulay oraliqlarini tozalash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Universal Reset</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body { font-family: sans-serif; padding: 20px; }
    </style>
</head>
<body>
    <h1>Toza Boshlanish</h1>
    <p>Barcha brauzerlarning sukut bo'yicha beriladigan har xil margin va paddinglari nolga tushirildi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`*` (yulduzcha) universal selektori sahifadagi har bitta HTML elementini nishonga oladi. `box-sizing: border-box; margin: 0; padding: 0;` barcha zamonaviy frontend dasturchilarining standart boshlang'ich qoidasidir.

## Ishlash natijasi:
```text
Elementlar bir-biriga noo'rin yopishmasdan, toza va aniq nolga tushirilgan oraliqlarda ko'rinadi.
```

---

# 305-Topshiriq: Element (Type) selektori
## Topshiriq sharti:
HTML tegi nomi bo'yicha to'g'ridan-to'g'ri stillash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Element Selektori</title>
    <style>
        p { color: #334155; line-height: 1.6; font-size: 16px; }
        h2 { color: #0f172a; border-bottom: 2px solid #e2e8f0; }
    </style>
</head>
<body>
    <h2>Bob Nomi</h2>
    <p>Ushbu sahifadagi barcha p teglari avtomatik ravishda ushbu rang va o'lchamni oladi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Element selektori teg nomi (`p`, `h1`, `table`) orqali sahifadagi barcha bir xil teglarga umumiy qoida beradi. Uning o'ziga xoslik vazni (specificity) past bo'lib, global matn stillari uchun juda qulay.

## Ishlash natijasi:
```text
Hoshiyali sarlavha va kulrang-to'q xatboshi matni namoyon bo'ladi.
```

---

# 306-Topshiriq: Class selektori (.nomi) va qayta ishlatiluvchanlik
## Topshiriq sharti:
Nuqta bilan boshlanuvchi klasslar orqali ko'p marotaba ishlatiluvchi komponentlar yaratish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Class Selektori</title>
    <style>
        .badge { display: inline-block; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: bold; }
        .badge-success { background: #dcfce7; color: #15803d; }
        .badge-danger { background: #fee2e2; color: #b91c1c; }
    </style>
</head>
<body>
    <span class="badge badge-success">Muvaffaqiyatli</span>
    <span class="badge badge-danger">Rad etildi</span>
</body>
</html>
```

## Tushuntirish va Mantiq:
Klass selektori nuqta bilan belgilanadi (`.badge`). Bitta sahifada istalgancha element bir xil klassga ega bo'lishi mumkin. Bu CSS dagi modullilik va qayta foydalanishning asosiy poydevoridir.

## Ishlash natijasi:
```text
Biri yashil, biri qizil rangli yumaloq holat nishonlari (badges) chiqadi.
```

---

# 307-Topshiriq: ID selektori (#nomi) va uning o'ziga xosligi
## Topshiriq sharti:
Panjara (#) bilan boshlanuvchi yagona element selektori.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>ID Selektori</title>
    <style>
        #main-header { background: #1e293b; color: white; padding: 20px; }
    </style>
</head>
<body>
    <header id="main-header">
        <h1>Yagona Asosiy Boshqaruv Paneli</h1>
    </header>
</body>
</html>
```

## Tushuntirish va Mantiq:
ID selektori `#` belgisi bilan yoziladi. Sahifada bitta ID nom faqat bir marta uchrashi shart. Uning o'ziga xoslik vazni (specificity) juda yuqori bo'lganligi bois, oddiy stillashda klasslardan foydalanish afzal ko'riladi.

## Ishlash natijasi:
```text
To'q ko'k rangli yagona sarlavha paneli aks etadi.
```

---

# 308-Topshiriq: Bir nechta klasslarni birlashtirish (Multi-class)
## Topshiriq sharti:
Bitta elementga bir nechta xizmat klasslarini probel bilan biriktirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Multi Class</title>
    <style>
        .btn { padding: 10px 18px; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; }
        .btn-primary { background: #2563eb; color: white; }
        .btn-large { font-size: 18px; padding: 14px 28px; }
    </style>
</head>
<body>
    <button class="btn btn-primary btn-large">Katta Moviy Tugma</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
`class='btn btn-primary btn-large'` sintaksisida har bir klass o'z vazifasini bajaradi: `btn` shaklni, `btn-primary` rangni, `btn-large` esa o'lchamni belgilaydi.

## Ishlash natijasi:
```text
Katta va yorqin moviy bosiluvchi tugma ko'rinadi.
```

---

# 309-Topshiriq: Bir nechta selektorlarni guruhlash (Vergul bilan)
## Topshiriq sharti:
Bir xil qoidalarni bir nechta elementlarga kodni takrorlamasdan berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Guruhlash</title>
    <style>
        h1, h2, h3, .custom-title {
            font-family: 'Georgia', serif;
            color: #1e3a8a;
            margin-bottom: 8px;
        }
    </style>
</head>
<body>
    <h1>1-Sarlavha</h1>
    <h2>2-Sarlavha</h2>
    <div class="custom-title">Maxsus Sarlavha</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Vergul (`,`) bir xil CSS blokini bir nechta mustaqil selektorlarga qo'llashga imkon beradi va kod hajmini (DRY printsipi) qisqartiradi.

## Ishlash natijasi:
```text
Barcha uchta sarlavha bir xil nafis to'q ko'k serif shriftida chiqadi.
```

---

# 310-Topshiriq: Avlod (Descendant) kombinatori (Bo'shliq)
## Topshiriq sharti:
Ota elementning ichida qancha chuqurlikda bo'lishidan qat'i nazar barcha bolalarni tanlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Descendant Combinator</title>
    <style>
        article p { color: #047857; font-size: 17px; }
    </style>
</head>
<body>
    <article>
        <p>Maqola ichidagi birinchi xatboshi.</p>
        <div>
            <p>Div ichiga o'ralgan bo'lsa ham yashil bo'ladi.</p>
        </div>
    </article>
    <p>Maqoladan tashqaridagi oddiy xatboshi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`article p` selektori (o'rtada probel) `article` ichidagi barcha `p` teglarni chuqurlik darajasidan qat'i nazar tanlaydi. Tashqaridagi `p` ga esa teginmaydi.

## Ishlash natijasi:
```text
Maqola ichidagi ikkita matn to'q yashil, tashqaridagi esa oddiy qora bo'lib ko'rinadi.
```

---

# 311-Topshiriq: To'g'ridan-to'g'ri bola (Child) kombinatori (>)
## Topshiriq sharti:
Faqat bevosita birinchi pog'ona farzandlarini tanlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Child Combinator</title>
    <style>
        ul > li { font-weight: bold; color: #2563eb; }
    </style>
</head>
<body>
    <ul>
        <li>Bevosita bola (Qalin ko'k)
            <div>
                <span>Ichki matn</span>
            </div>
        </li>
    </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
`>` belgisi faqat ota elementning darhol ostidagi birinchi darajali bolalarini nishonga oladi. Ichkaridagi chuqurroq nevaralarga bu qoida o'tmaydi.

## Ishlash natijasi:
```text
Faqatgina ro'yxatning asosiy satri qalin ko'k bo'ladi.
```

---

# 312-Topshiriq: Qo'shni qardosh (Adjacent sibling) kombinatori (+)
## Topshiriq sharti:
Elementdan darhol keyin kelgan yagona qo'shnisini tanlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Adjacent Sibling</title>
    <style>
        h2 + p { font-size: 20px; color: #475569; font-style: italic; }
    </style>
</head>
<body>
    <h2>Asosiy Mavzu</h2>
    <p>Sarlavhadan keyingi birinchi xatboshi (Katta va qiya).</p>
    <p>Ikkinchi xatboshi esa oddiy holatda qoladi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`h2 + p` faqatgina `h2` tugashi bilanoq darhol undan keyin keluvchi birinchi `p` elementiga ta'sir qiladi.

## Ishlash natijasi:
```text
Sarlavhadan keyingi birinchi jumla yirik va qiya bo'ladi, qolganlari oddiy qoladi.
```

---

# 313-Topshiriq: Umumiy qardosh (General sibling) kombinatori (~)
## Topshiriq sharti:
Elementdan keyin keluvchi bir ota ostidagi barcha qardoshlarni tanlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>General Sibling</title>
    <style>
        h3 ~ p { color: #dc2626; }
    </style>
</head>
<body>
    <p>Sarlavhadan oldingi matn (Qora).</p>
    <h3>Sarlavha</h3>
    <p>Sarlavhadan keyingi 1-matn (Qizil).</p>
    <p>Sarlavhadan keyingi 2-matn (Qizil).</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`h3 ~ p` `h3` dan keyin joylashgan barcha qardosh `p` larni tanlaydi, oralarida boshqa bloklar bo'lsa ham ularni qamrab oladi.

## Ishlash natijasi:
```text
Sarlavhadan oldingi matn qora, keyingi barcha matnlar esa qizil tusda chiqadi.
```

---

# 314-Topshiriq: Atribut mavjudligi selektori [atribut]
## Topshiriq sharti:
Muayyan atributga ega bo'lgan har qanday elementni nishonga olish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Attribute Exists</title>
    <style>
        [required] { border: 2px solid #ef4444; background: #fff5f5; }
    </style>
</head>
<body>
    <input type="text" placeholder="Ixtiyoriy">
    <input type="text" required placeholder="Majburiy katak">
</body>
</html>
```

## Tushuntirish va Mantiq:
`[required]` selektori o'zida `required` atributi mavjud bo'lgan barcha elementlarni qiymatiga qaramasdan topadi.

## Ishlash natijasi:
```text
Ikkinchi majburiy katak qizil hoshiya va pushti fon bilan ajraladi.
```

---

# 315-Topshiriq: Atributning aniq qiymati selektori [attr='qiymat']
## Topshiriq sharti:
Aniq ko'rsatilgan qiymatga ega bo'lgan elementni tanlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Attribute Exact</title>
    <style>
        input[type="submit"] { background: #16a34a; color: white; border: none; padding: 10px 20px; border-radius: 4px; }
    </style>
</head>
<body>
    <input type="text" value="Oddiy">
    <input type="submit" value="Yuborish">
</body>
</html>
```

## Tushuntirish va Mantiq:
`input[type='submit']` faqat submit turidagi tugmalarga stillarni yo'naltiradi.

## Ishlash natijasi:
```text
Yashil rangdagi chiroyli forma yuborish tugmasi chiqadi.
```

---

# 316-Topshiriq: Atribut qiymati boshlanishi selektori [attr^='qiymat']
## Topshiriq sharti:
Boshlanish harflari bo'yicha saralash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Attribute Prefix</title>
    <style>
        a[href^="https://"] { color: #16a34a; font-weight: bold; }
    </style>
</head>
<body>
    <a href="http://oddiy-sayt.uz">Xavfsiz bo'lmagan HTTP</a><br>
    <a href="https://xavfsiz-bank.uz">Xavfsiz HTTPS Havola</a>
</body>
</html>
```

## Tushuntirish va Mantiq:
`^=` belgisi qiymat aynan ko'rsatilgan so'z bilan boshlanishini talab qiladi (masalan, `https://`).

## Ishlash natijasi:
```text
Faqat xavfsiz HTTPS havolasi yashil va qalin bo'lib ko'rinadi.
```

---

# 317-Topshiriq: Atribut qiymati tugashi selektori [attr$='qiymat']
## Topshiriq sharti:
Fayl formati yoki oxirgi so'z bo'yicha stillash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Attribute Suffix</title>
    <style>
        a[href$=".zip"] { color: #d97706; text-decoration: underline wavy; }
    </style>
</head>
<body>
    <a href="/fayllar/dastur.zip">Arxiv Fayli (.zip)</a>
</body>
</html>
```

## Tushuntirish va Mantiq:
`$=` belgisi satr oxiri ko'rsatilgan kengaytma bilan tugashini tekshiradi.

## Ishlash natijasi:
```text
Arxiv havolasi to'lqinsimon to'q sariq chiziq bilan belgilanadi.
```

---

# 318-Topshiriq: Atribut qiymati ichida uchrashi [attr*='qiymat']
## Topshiriq sharti:
Satrning istalgan joyida kerakli ibora uchrashini aniqlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Attribute Substring</title>
    <style>
        [class*="theme-dark"] { background: #0f172a; color: white; padding: 15px; }
    </style>
</head>
<body>
    <div class="card-component-theme-dark-active">Qorong'u Mavzu Bloki</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`*=` selektori so'z klass nomining boshida, o'rtasida yoki oxirida uchrashidan qat'i nazar uni aniqlab oladi.

## Ishlash natijasi:
```text
To'q qora fonda oq matnli blok hosil bo'ladi.
```

---

# 319-Topshiriq: So'zlar ro'yxatida uchrashi [attr~='qiymat']
## Topshiriq sharti:
Probellar bilan ajratilgan so'zlar ichidan to'liq so'zni qidirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Attribute Word</title>
    <style>
        [data-tags~="sport"] { border-left: 5px solid #2563eb; padding-left: 10px; }
    </style>
</head>
<body>
    <div data-tags="yangiliklar sport salomatlik">Futbol yangiliklari</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`~=` atribut ichidagi bo'shliqlar bilan ajratilgan so'zlar ro'yxatidan aniq 'sport' so'zini qidiradi.

## Ishlash natijasi:
```text
Chap tomonida ko'k qalin chizig'i bo'lgan sport yangiligi chiqadi.
```

---

# 320-Topshiriq: Til kodi selektori [lang|='uz']
## Topshiriq sharti:
Til kodi va uning hududiy variantlarini (masalan, uz-Latn, uz-Cyrl) tanlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Language Selector</title>
    <style>
        [lang|="uz"] { font-style: italic; color: #1e40af; }
    </style>
</head>
<body>
    <p lang="uz-UZ">O'zbek tilidagi rasmiy xatboshi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`|=` selektori aniq qiymatni yoki defis bilan boshlanuvchi prefikslarni (masalan 'uz' yoki 'uz-UZ') topadi.

## Ishlash natijasi:
```text
Qiya moviy matn ko'rinadi.
```

---

# 321-Topshiriq: Registrga sezgir bo'lmagan atribut selektori [attr='val' i]
## Topshiriq sharti:
Katta va kichik harflar farqini yo'qotuvchi 'i' bayrog'i.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Case Insensitive</title>
    <style>
        a[href$=".jpg" i] { color: #9333ea; font-weight: bold; }
    </style>
</head>
<body>
    <a href="foto.JPG">Katta harfli JPG</a><br>
    <a href="rasm.jpg">Kichik harfli jpg</a>
</body>
</html>
```

## Tushuntirish va Mantiq:
Selektor oxiridagi `i` belgisi `.jpg` hamda `.JPG` ni bir xil deb hisoblaydi.

## Ishlash natijasi:
```text
Ikkala havola ham bir xil binafsharang bo'lib ochiladi.
```

---

# 322-Topshiriq: CSS Specificity (O'ziga xoslik) darajalari
## Topshiriq sharti:
Qaysi qoida kuchliroq ekanini hal qiluvchi iyerarxiya tajribasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Specificity</title>
    <style>
        p { color: black; }           /* 0, 0, 0, 1 (Eng zaif) */
        .text { color: blue; }         /* 0, 0, 1, 0 (Kuchliroq) */
        #unique { color: green; }      /* 0, 1, 0, 0 (Juda kuchli) */
    </style>
</head>
<body>
    <p id="unique" class="text">Mening rangim qanday bo'ladi?</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu elementga uchta rang berilgan: qora (teg), ko'k (klass) va yashil (ID). ID eng yuqori specificity ga ega bo'lganligi sababli matn yashil rangda chiqadi.

## Ishlash natijasi:
```text
Matn yashil rangda aks etadi.
```

---

# 323-Topshiriq: Specificity hisoblash formulasi (0, 0, 0, 0)
## Topshiriq sharti:
Murakkab selektorlar to'qnashganda ballarni matematik hisoblash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Specificity Hisobi</title>
    <style>
        /* A: 0, B: 0, C: 2, D: 1 -> 0,0,2,1 */
        nav.menu ul li a { color: #d97706; }
        /* A: 0, B: 1, C: 0, D: 1 -> 0,1,0,1 (G'olib!) */
        #nav a { color: #2563eb; }
    </style>
</head>
<body>
    <nav id="nav" class="menu">
        <ul><li><a href="#">Havola rangi</a></li></ul>
    </nav>
</body>
</html>
```

## Tushuntirish va Mantiq:
`#nav a` bitta ID ga ega bo'lgani uchun u 2 ta klass va 3 ta elementga ega uzun selektordan ham ustun keladi.

## Ishlash natijasi:
```text
Havola moviy (#2563eb) rangda chiqadi.
```

---

# 324-Topshiriq: !important qoidasi va uning kuchi
## Topshiriq sharti:
Barcha specificity hisoblarini yorib o'tuvchi mutlaq ustunlik.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Important Qoidasi</title>
    <style>
        #danger-box { color: black; }
        .force-red { color: #dc2626 !important; }
    </style>
</head>
<body>
    <p id="danger-box" class="force-red">ID kuchli bo'lsa ham bu matn qizil bo'ladi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`!important` oddiy kaskad qoidalarini chetlab o'tib majburiy birinchi o'ringa chiqadi. Undan faqat o'ta zarur favqulodda hollarda foydalanish lozim.

## Ishlash natijasi:
```text
ID qora bo'lishiga qaramay matn yorqin qizil rangda chiqadi.
```

---

# 325-Topshiriq: Kaskad (Cascade) va Source Order qoidasi
## Topshiriq sharti:
Specificity teng bo'lganda eng oxirgi yozilgan qoidaning g'alaba qilishi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Source Order</title>
    <style>
        .box { background: red; padding: 15px; }
        .box { background: blue; } /* Oxirgi yozilgani g'olib bo'ladi */
    </style>
</head>
<body>
    <div class="box" style="color:white;">Ko'k fonli quti</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Agar ikki selektorning o'ziga xosligi mutlaqo teng bo'lsa, faylda eng oxirgi navbatda kelgan qoida avvalgilarini ustiga yozadi (override).

## Ishlash natijasi:
```text
Qizil fon emas, oxirgi ko'k fon aks etadi.
```

---

# 326-Topshiriq: CSS Vorislik (Inheritance): Meros bo'luvchi xususiyatlar
## Topshiriq sharti:
Shriftlar va ranglarning ota elementdan bolalarga avtomatik o'tishi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Vorislik</title>
    <style>
        .parent { font-family: 'Courier New', monospace; color: #7c3aed; }
    </style>
</head>
<body>
    <div class="parent">
        <h2>Sarlavha (Meros oldi)</h2>
        <p>Xatboshi ham <span>ichki so'zlar ham</span> binafsharang va monospaced bo'ladi.</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Tipografik xususiyatlar (`color`, `font-family`, `line-height`) tabiiy ravishda bolalarga meros bo'ladi. Chegaralar (`border`), `padding` va `margin` esa hech qachon avtomatik meros bo'lmaydi.

## Ishlash natijasi:
```text
Barcha ichki matnlar ota blokdan binafsha rang va maxsus shriftni meros oladi.
```

---

# 327-Topshiriq: inherit kalit so'zi
## Topshiriq sharti:
Meros bo'lmaydigan xususiyatni otasidan olishga majburlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Inherit</title>
    <style>
        .card { border: 2px solid #2563eb; padding: 15px; }
        .card-inner { border: inherit; padding: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <div class="card-inner">Men ham ota kabi ko'k ramkaga ega bo'ldim.</div>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`border: inherit;` xususiyati tabiiy meros bo'lmaydigan hoshiyani ota elementidan majburan nusxalab oladi.

## Ishlash natijasi:
```text
Ichma-ich ikkita bir xil ko'k hoshiyali blok ko'rinadi.
```

---

# 328-Topshiriq: initial kalit so'zi
## Topshiriq sharti:
Xususiyatni W3C spetsifikatsiyasidagi asl tug'ma qiymatiga qaytarish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Initial</title>
    <style>
        body { color: #dc2626; }
        .reset-text { color: initial; }
    </style>
</head>
<body>
    <p>Qizil matn</p>
    <p class="reset-text">Qora matn (standart initial holatiga qaytdi)</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`color: initial` brauzerning eng dastlabki sukut bo'yicha qora rangiga majburan qaytaradi.

## Ishlash natijasi:
```text
Birinchi gap qizil, ikkinchi gap esa standart qora rangda chiqadi.
```

---

# 329-Topshiriq: unset kalit so'zi
## Topshiriq sharti:
Agar meros bo'lsa inherit, bo'lmasa initial kabi ishlovchi aqlli qaytaruvchi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Unset</title>
    <style>
        .box { color: green; border: 2px solid green; padding: 10px; }
        .child { color: unset; border: unset; }
    </style>
</head>
<body>
    <div class="box">
        <div class="child">Matn yashil (meros oldi), hoshiya esa yo'q (meros bo'lmadi).</div>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`unset` universal sozlagichdir: rang meros bo'lgani uchun yashil bo'lib qoladi, hoshiya esa meros bo'lmagani uchun nolga tushadi.

## Ishlash natijasi:
```text
Hoshiyasiz yashil matn ko'rinadi.
```

---

# 330-Topshiriq: all: unset bilan barcha stillarni tozalash
## Topshiriq sharti:
Tugma yoki havolaning barcha standart stillarini bitta qatorda o'chirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>All Unset</title>
    <style>
        .naked-btn {
            all: unset;
            cursor: pointer;
            padding: 8px 16px;
            background: #e2e8f0;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <button class="naked-btn">Tozalangan Tugma</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
`all: unset` brauzer tomonidan berilgan barcha ramkalar, fonlar va shriftlarni tozalab elementni toza xomashyoga aylantiradi.

## Ishlash natijasi:
```text
Oddiy matn ko'rinishiga kelgan, faqat kursor borganda qo'lcha chiquvchi tugma ko'rinadi.
```

---

# 331-Topshiriq: :hover psevdo-sinfi
## Topshiriq sharti:
Sichqoncha kursorining ustiga kelish harakatini stillash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Hover</title>
    <style>
        .box { width: 150px; padding: 15px; background: #3b82f6; color: white; text-align: center; border-radius: 6px; transition: background 0.3s; }
        .box:hover { background: #1d4ed8; }
    </style>
</head>
<body>
    <div class="box">Ustiga keling</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:hover` elementi foydalanuvchi sichqonchani uning ustiga olib borganda faollashadi.

## Ishlash natijasi:
```text
Kursor kelganda moviy quti to'q ko'k rangga o'zgaradi.
```

---

# 332-Topshiriq: :active psevdo-sinfi
## Topshiriq sharti:
Foydalanuvchi sichqoncha tugmasini bosib turgan lahzani stillash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Active</title>
    <style>
        .click-btn { padding: 10px 20px; background: #10b981; color: white; border: none; border-radius: 6px; cursor: pointer; }
        .click-btn:active { transform: scale(0.95); background: #059669; }
    </style>
</head>
<body>
    <button class="click-btn">Meni Bosing</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:active` bosish boshlanganidan qo'yib yuborilguncha bo'lgan qisqa vaqt oralig'ida jismoniy tugmachaning ichkariga botish effektini beradi.

## Ishlash natijasi:
```text
Bosib turganda kichrayib quyuq yashil rangga kiruvchi reaktiv tugma chiqadi.
```

---

# 333-Topshiriq: :focus psevdo-sinfi
## Topshiriq sharti:
Element klaviatura yoki sichqoncha orqali tanlanganda.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Focus</title>
    <style>
        input:focus { outline: 3px solid #f59e0b; }
    </style>
</head>
<body>
    <input type="text" placeholder="Tab bosing yoki cherting">
</body>
</html>
```

## Tushuntirish va Mantiq:
`:focus` elementi ayni damda foydalanuvchi diqqat markazida bo'lgan elementni sariq chegara bilan ko'rsatadi.

## Ishlash natijasi:
```text
Kursor tushganda sariq ramka bilan ajraladi.
```

---

# 334-Topshiriq: :visited psevdo-sinfi va maxfiylik cheklovlari
## Topshiriq sharti:
Tarixda avval tashrif buyurilgan havolalar.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Visited</title>
    <style>
        a:visited { color: #8b5cf6; }
    </style>
</head>
<body>
    <a href="https://google.com">Google (Avval kirilgan)</a>
</body>
</html>
```

## Tushuntirish va Mantiq:
Xavfsizlik sababli (saytlar foydalanuvchi qaysi saytlarga kirganini o'g'irlamasligi uchun) `:visited` faqat rang xususiyatlarini (`color`) o'zgartirishga ruxsat beradi.

## Ishlash natijasi:
```text
Avval kirilgan havola och siyohrang tusda ko'rinadi.
```

---

# 335-Topshiriq: :first-child birinchi farzand
## Topshiriq sharti:
Konteyner ichidagi eng birinchi elementni tanlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>First Child</title>
    <style>
        li:first-child { color: #dc2626; font-weight: bold; }
    </style>
</head>
<body>
    <ul>
        <li>Birinchi band (Qizil qalin)</li>
        <li>Ikkinchi band</li>
    </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
`li:first-child` ro'yxatning eng birinchi turgan elementini ajratib oladi.

## Ishlash natijasi:
```text
Faqatgina ro'yxatning birinchi bandi qizil va qalin bo'ladi.
```

---

# 336-Topshiriq: :last-child oxirgi farzand
## Topshiriq sharti:
Konteyner ichidagi eng so'nggi elementni stillash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Last Child</title>
    <style>
        p:last-child { border-bottom: 2px solid #000; padding-bottom: 10px; }
    </style>
</head>
<body>
    <div>
        <p>1-Xatboshi</p>
        <p>Oxirgi xatboshi ostida chiziq bor.</p>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:last-child` o'zining ota bloki ichidagi eng oxirgi elementni nishonga oladi.

## Ishlash natijasi:
```text
Eng quyi matn ostida qora chiziq tortiladi.
```

---

# 337-Topshiriq: :only-child yagona farzand
## Topshiriq sharti:
Konteyner ichida yolg'iz o'zi turgan elementni tanlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Only Child</title>
    <style>
        p:only-child { color: #d97706; font-weight: bold; }
    </style>
</head>
<body>
    <div><p>Men bu yerda yolg'izman (Sariq qalin).</p></div>
    <div><p>Biz ikkitamiz.</p><p>Biz ikkitamiz.</p></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:only-child` faqat o'z ota blokida boshqa qardoshi bo'lmagan yagona elementga ishlaydi.

## Ishlash natijasi:
```text
Birinchi qutidagi yolg'iz matn to'q sariq qalin bo'lib chiqadi.
```

---

# 338-Topshiriq: :nth-child(n) matematik formulalari
## Topshiriq sharti:
Har 3-chi elementni yoki juft/toqlarni tanlash (`3n`, `even`, `odd`).

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Nth Child</title>
    <style>
        li:nth-child(3n) { background: #fef08a; }
    </style>
</head>
<body>
    <ul>
        <li>1</li><li>2</li><li>3 (Sariq)</li>
        <li>4</li><li>5</li><li>6 (Sariq)</li>
    </ul>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:nth-child(3n)` har uchinchi (3, 6, 9...) elementni tanlaydi. Matematik formulalar orqali istalgan davriy tartibni belgilash mumkin.

## Ishlash natijasi:
```text
Har uchinchi qator sariq fonga bo'yaladi.
```

---

# 339-Topshiriq: :nth-of-type(n) va uning :nth-child dan farqi
## Topshiriq sharti:
Boshqa teglarni e'tiborsiz qoldirib faqat o'z turidagi elementlarni sanash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Nth of Type</title>
    <style>
        p:nth-of-type(2) { color: #2563eb; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Sarlavha</h1>
    <p>1-Xatboshi</p>
    <div>E'lon</div>
    <p>2-Xatboshi (Bu yerda p turlarining ikkinchisi!)</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:nth-child` umumiy bolalar soni bo'yicha hisoblaydi, `:nth-of-type` esa faqat aynan `p` teglarini alohida sanaydi va boshqa teglarga chalg'imaydi.

## Ishlash natijasi:
```text
Ikkinchi p tegi moviy qalin bo'lib ajraladi.
```

---

# 340-Topshiriq: :first-of-type va :last-of-type
## Topshiriq sharti:
O'z turidagi birinchi va oxirgi elementlarni tanlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>First of Type</title>
    <style>
        img:first-of-type { border: 3px solid #10b981; }
    </style>
</head>
<body>
    <p>Matn</p>
    <img src="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='50' height='50'><rect width='50' height='50' fill='%23ccc'/></svg>">
</body>
</html>
```

## Tushuntirish va Mantiq:
Garchi uning oldida `p` turgan bo'lsa ham, u sahifadagi eng birinchi `img` bo'lgani uchun yashil hoshiyaga ega bo'ladi.

## Ishlash natijasi:
```text
Yashil hoshiyali birinchi rasm chiqadi.
```

---

# 341-Topshiriq: :not() inkor selektori
## Topshiriq sharti:
Ko'rsatilgan klassga ega bo'lmagan barcha elementlarni tanlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Not Selektori</title>
    <style>
        p:not(.special) { color: #94a3b8; }
        p.special { color: #000; font-weight: bold; }
    </style>
</head>
<body>
    <p>Oddiy xira matn</p>
    <p class="special">Maxsus qora matn</p>
    <p>Yana bir oddiy xira matn</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`:not(.special)` maxsus klassi bo'lmagan barcha xatboshilarni xira rangga bo'yaydi.

## Ishlash natijasi:
```text
O'rtadagi bitta qalin qora matn va uning atrofidagi xira kulrang matnlar ko'rinadi.
```

---

# 342-Topshiriq: :empty bo'sh elementlarni nishonga olish
## Topshiriq sharti:
Ichida hech qanday matn yoki bola tegi bo'lmagan bo'sh kataklarni yashirish yoki stillash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Empty Selektori</title>
    <style>
        .badge:empty { display: none; }
        .badge { background: red; color: white; padding: 4px; border-radius: 50%; }
    </style>
</head>
<body>
    <span class="badge">5</span>
    <span class="badge"></span> <!-- Yashiriladi -->
</body>
</html>
```

## Tushuntirish va Mantiq:
`:empty` bo'sh elementlarni avtomatik `display: none` qilib ekranda ortiqcha qizil nuqta ko'rinishining oldini oladi.

## Ishlash natijasi:
```text
Faqat '5' soni bor nishon ko'rinadi, bo'shi esa butunlay yo'qoladi.
```

---

# 343-Topshiriq: ::before va content xususiyati
## Topshiriq sharti:
Element matnidan oldin vizual belgi kiritish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Before Psevdo Elementi</title>
    <style>
        .phone::before { content: "📞 "; font-size: 18px; }
    </style>
</head>
<body>
    <span class="phone">+998 71 200-00-00</span>
</body>
</html>
```

## Tushuntirish va Mantiq:
`::before` HTML kodiga yangi teg yozmasdan CSS orqali element boshiga belgi yoki dekorativ shakl qo'shish imkonini beradi.

## Ishlash natijasi:
```text
Telefon raqami oldida avtomatik trubka belgisi paydo bo'ladi.
```

---

# 344-Topshiriq: ::after dekorativ elementlar
## Topshiriq sharti:
Elementdan keyin o'q belgisi yoki chiziq qo'shish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>After Psevdo Elementi</title>
    <style>
        .more-link::after { content: " →"; font-weight: bold; }
    </style>
</head>
<body>
    <a href="#" class="more-link">Batafsil o'qish</a>
</body>
</html>
```

## Tushuntirish va Mantiq:
`::after` matn oxiriga strelka piktogrammasini qo'shadi.

## Ishlash natijasi:
```text
'Batafsil o'qish →' shaklidagi chiroyli havola chiqadi.
```

---

# 345-Topshiriq: ::first-letter bosh harf
## Topshiriq sharti:
Birinchi harfga maxsus rang berish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>First Letter</title>
    <style>
        p::first-letter { font-size: 24px; color: #dc2626; font-weight: bold; }
    </style>
</head>
<body>
    <p>O'zbekiston — buyuk davlat.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`::first-letter` butun xatboshining faqat ilk harfiga ta'sir qiladi.

## Ishlash natijasi:
```text
Boshidagi 'O'' harfi katta qizil bo'lib chiqadi.
```

---

# 346-Topshiriq: ::first-line birinchi satr
## Topshiriq sharti:
Ekran kengligiga qarab xatboshining aynan birinchi satrini qalinlashtirish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>First Line</title>
    <style>
        p::first-line { font-weight: bold; color: #1e3a8a; }
    </style>
</head>
<body>
    <p style="width: 250px;">Ushbu xatboshining aynan birinchi qatori to'q ko'k va qalin bo'lib turadi, keyingi qatorlar esa oddiy bo'ladi.</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ekran o'lchami o'zgarganda qaysi so'zlar birinchi satrda qolsa, faqat o'shalar qalin bo'ladi.

## Ishlash natijasi:
```text
Birinchi satr to'q ko'k rangda ajraladi.
```

---

# 347-Topshiriq: ::selection matn tanlanganda chiqadigan rang
## Topshiriq sharti:
Foydalanuvchi sichqoncha bilan matnni belgilaganda ochiladigan fon rangi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Selection</title>
    <style>
        ::selection { background-color: #fde047; color: #000; }
    </style>
</head>
<body>
    <p>Ushbu matnni sichqoncha bilan belgilab ko'ring!</p>
</body>
</html>
```

## Tushuntirish va Mantiq:
`::selection` standart ko'k belgilash rangini brendga mos sariq yoki boshqa yorqin rangga almashtiradi.

## Ishlash natijasi:
```text
Matn belgilanganda ko'k emas, yoqimli sariq fon bilan ajraladi.
```

---

# 348-Topshiriq: ::placeholder maslahat matnini stillash
## Topshiriq sharti:
Input ichidagi xira maslahat yozuvining rangi va shriftini boshqarish.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Placeholder Stillash</title>
    <style>
        input::placeholder { color: #a855f7; font-style: italic; }
    </style>
</head>
<body>
    <input type="text" placeholder="Qidiruv so'zini kiriting...">
</body>
</html>
```

## Tushuntirish va Mantiq:
`::placeholder` yordamida standart kulrang ko'rsatmani binafsharang va qiya qilish mumkin.

## Ishlash natijasi:
```text
Binafsharang qiya maslahat yozuvli katak ko'rinadi.
```

---

# 349-Topshiriq: CSS sharhlari /* ... */ va toza kod arxitekturasi
## Topshiriq sharti:
CSS kodini mantiqiy bo'limlarga ajratib izohlash.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>CSS Sharhlar</title>
    <style>
        /* =========================================
           1. TIPOGRAFIKA VA ASOSIY STILLAR
           ========================================= */
        body { font-family: sans-serif; color: #333; }

        /* 2. TUGMALAR KOMPONENTI */
        .btn { padding: 8px 16px; background: #2563eb; color: white; border: none; }
    </style>
</head>
<body>
    <button class="btn">Tugma</button>
</body>
</html>
```

## Tushuntirish va Mantiq:
`/* ... */` brauzer tomonidan o'qilmaydi va dasturchilar uchun loyiha kodini tartibli saqlashga xizmat qiladi.

## Ishlash natijasi:
```text
Tartibli sharhlangan toza kod natijasi.
```

---

# 350-Topshiriq: To'liq CSS selektorlar va Specificity arxitekturasi namunasi
## Topshiriq sharti:
Kombinatorlar, atribut selektorlar, pseudo-klass va psevdo-elementlarni jamlagan mukammal veb-komponent.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mukammal CSS Selektorlar</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', sans-serif; padding: 40px; background: #f8fafc; }
        .post-card { background: white; border-radius: 10px; max-width: 500px; padding: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        .post-card > h2 { color: #0f172a; margin-bottom: 12px; }
        .post-card > p:first-of-type { font-size: 18px; color: #475569; margin-bottom: 15px; }
        .post-card a[href^="https://"]::after { content: " ↗"; font-weight: bold; }
        .tags-list { display: flex; gap: 8px; list-style: none; margin-top: 15px; }
        .tags-list li:first-child { background: #dbeafe; color: #1e40af; font-weight: bold; }
        .tags-list li { background: #f1f5f9; padding: 4px 10px; border-radius: 4px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="post-card">
        <h2>Zamonaviy CSS Selektorlar</h2>
        <p>Selektorlar yordamida HTML strukturasini hech qanday ortiqcha klasslarsiz aniq boshqarish mumkin.</p>
        <a href="https://w3.org" target="_blank" rel="noopener">W3C Standartlari</a>
        <ul class="tags-list">
            <li>#CSS3</li>
            <li>#WebDev</li>
            <li>#Frontend</li>
        </ul>
    </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu yakuniy andoza bolalar kombinatori (`>`), `first-of-type`, atribut prefiksi (`^=`), `::after`, `first-child` kabi barcha muhim selektorlarni bitta nafis kartochkada uyg'unlashtiradi.

## Ishlash natijasi:
```text
Oq kartochka ichida sarlavha, yirik birinchi xatboshi, strelkali tashqi havola va birinchi tegi ko'k rangda ajratilgan zamonaviy xabarnoma bloki namoyon bo'ladi.
```

---

