# HTML va CSS: Amaliy Zamonaviy Web Interfeyslar (Topshiriqlar 951 - 1000)

# 951-Topshiriq: To'liq zamonaviy SaaS Landing Page (Hero, Xizmatlar, Fikrlar va Footer)
## Topshiriq sharti:
Landing sahifasining to'liq arxitekturasini zamonaviy semantik HTML5 va toza CSS bilan quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SaaS Landing Page</title>
  <style>
    body { margin: 0; font-family: sans-serif; color: #0f172a; background: #ffffff; }
    .nav { display: flex; justify-content: space-between; align-items: center; padding: 16px 30px; background: white; border-bottom: 1px solid #e2e8f0; }
    .hero { text-align: center; padding: 60px 20px; background: linear-gradient(180deg, #f8fafc 0%, #eff6ff 100%); }
    .hero h1 { font-size: 36px; margin: 0 0 16px 0; color: #1e3a8a; }
    .btn-cta { background: #2563eb; color: white; border: none; padding: 14px 28px; border-radius: 8px; font-weight: bold; cursor: pointer; }
    .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; padding: 40px 30px; max-width: 900px; margin: 0 auto; }
    .f-card { padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px; text-align: center; }
    footer { background: #0f172a; color: #94a3b8; text-align: center; padding: 20px; font-size: 13px; }
  </style>
</head>
<body>
  <header class="nav">
    <strong>CloudSoft</strong>
    <button style="padding: 8px 16px; background: #e2e8f0; border: none; border-radius: 4px;">Kirish</button>
  </header>
  <section class="hero">
    <h1>Biznesingizni Avtomatlashtiring</h1>
    <p style="color: #64748b; margin-bottom: 24px;">Eng ilg'or sun'iy intellekt vositalari bilan ishingizni 10 barobar tezlashtiring.</p>
    <button class="btn-cta">Bepul Boshlash</button>
  </section>
  <section class="features">
    <div class="f-card"><h3>Tezkor Tahlil</h3><p>Soniyalar ichida hisobotlar.</p></div>
    <div class="f-card"><h3>Xavfsiz Bulut</h3><p>256-bitli shifrlash tizimi.</p></div>
    <div class="f-card"><h3>24/7 Qo'llab-quvvatlash</h3><p>Har doim aloqadamiz.</p></div>
  </section>
  <footer>&copy; 2026 CloudSoft Inc. Barcha huquqlar himoyalangan.</footer>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ushbu maketda navbar, gradient Hero bloki, moslashuvchan Grid xizmatlar bo'limi va to'liq footer professional darajada birlashtirilgan.

## Ishlash natijasi:
```text
Zamonaviy IT startaplariga xos toza oq-moviy fonli SaaS landing sahifasi.
```

---

# 952-Topshiriq: Dashboard Admin Sidebar UI (Kompakt ikonkalari va aktiv indikatori bilan)
## Topshiriq sharti:
To'liq admin paneli yon menyusi (Sidebar) interfeysini quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Admin Sidebar UI</title>
  <style>
    body { margin: 0; display: flex; height: 100vh; font-family: sans-serif; }
    .sidebar { width: 220px; background: #0f172a; color: white; display: flex; flex-direction: column; padding: 20px 0; }
    .logo { padding: 0 20px 20px; font-size: 18px; font-weight: bold; border-bottom: 1px solid #1e293b; color: #38bdf8; }
    .menu { list-style: none; padding: 0; margin: 15px 0; flex: 1; }
    .menu a { display: flex; align-items: center; gap: 12px; padding: 12px 20px; color: #94a3b8; text-decoration: none; font-size: 14px; }
    .menu a.active { background: #1e293b; color: #38bdf8; border-left: 4px solid #38bdf8; font-weight: bold; }
    .user-footer { padding: 15px 20px; border-top: 1px solid #1e293b; display: flex; align-items: center; gap: 10px; font-size: 13px; }
    .avatar { width: 32px; height: 32px; background: #2563eb; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
  </style>
</head>
<body>
  <aside class="sidebar">
    <div class="logo">AdminPanel</div>
    <ul class="menu">
      <li><a href="#" class="active">&#128202; Statistika</a></li>
      <li><a href="#">&#128100; Mijozlar</a></li>
      <li><a href="#">&#128230; Mahsulotlar</a></li>
      <li><a href="#">&#9881; Sozlamalar</a></li>
    </ul>
    <div class="user-footer">
      <div class="avatar">AZ</div>
      <div><strong>Azizbek</strong><br><small style="color:#64748b;">Superadmin</small></div>
    </div>
  </aside>
</body>
</html>
```

## Tushuntirish va Mantiq:
Sidebar iyerarxiyasi logotip, faol ko'k chiziqli menyu bandlari va pastki profil kartasini qat'iy o'lchovda ushlab turadi.

## Ishlash natijasi:
```text
Qora fonda moviy aktiv ko'rsatkichli professional admin boshqaruv paneli menyusi.
```

---

# 953-Topshiriq: Glassmorphism UI: Yarim shaffof shisha kartalar (Frosted Glass Effect)
## Topshiriq sharti:
Rangli gradient fon ustida backdrop-filter: blur(16px) va shaffof oq hoshiyali shisha effektini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Glassmorphism UI</title>
  <style>
    body {
      margin: 0;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(45deg, #ec4899, #8b5cf6, #3b82f6);
      font-family: sans-serif;
    }
    .glass-card {
      width: 280px;
      padding: 30px;
      background: rgba(255, 255, 255, 0.2);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.4);
      border-radius: 16px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
      color: white;
    }
    .glass-btn {
      background: rgba(255, 255, 255, 0.3);
      border: 1px solid rgba(255, 255, 255, 0.5);
      color: white;
      padding: 10px 20px;
      border-radius: 8px;
      cursor: pointer;
      font-weight: bold;
      width: 100%;
    }
  </style>
</head>
<body>
  <div class="glass-card">
    <h3 style="margin-top:0;">Glassmorphism</h3>
    <p style="font-size: 14px; opacity: 0.9;">Shisha foni orqali orqa ranglar xiralashib ko'rinadi.</p>
    <button class="glass-btn">Shisha Tugma</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`backdrop-filter: blur(16px)` va `rgba(255, 255, 255, 0.2)` zamonaviy iOS va macOS dizayn tizimlaridagi haqiqiy xira shisha (frosted glass) taassurotini beradi.

## Ishlash natijasi:
```text
Yorqin binafsha gradient ustida muzlatilgan xira shisha ko'rinishidagi oqish karta.
```

---

# 954-Topshiriq: Neumorphism (Soft UI) Button va Karta dizayni
## Topshiriq sharti:
Ikkita qarama-qarshi yorug'lik va soya (box-shadow: -5px -5px va 5px 5px) orqali plastik bo'rtma hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Neumorphism Soft UI</title>
  <style>
    body {
      margin: 0;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #e0e5ec;
      font-family: sans-serif;
    }
    .neu-card {
      width: 240px;
      padding: 24px;
      background-color: #e0e5ec;
      border-radius: 20px;
      box-shadow: 9px 9px 16px #bec3c9, -9px -9px 16px #ffffff;
      text-align: center;
      color: #4a5568;
    }
    .neu-btn {
      margin-top: 16px;
      padding: 12px 24px;
      background-color: #e0e5ec;
      border: none;
      border-radius: 12px;
      box-shadow: 5px 5px 10px #bec3c9, -5px -5px 10px #ffffff;
      color: #2b6cb0;
      font-weight: bold;
      cursor: pointer;
    }
    .neu-btn:active {
      box-shadow: inset 4px 4px 8px #bec3c9, inset -4px -4px 8px #ffffff;
    }
  </style>
</head>
<body>
  <div class="neu-card">
    <h3 style="margin-top:0;">Neumorphism</h3>
    <p style="font-size: 13px;">Plastik sirtga bosilgan tugma</p>
    <button class="neu-btn">Tugmani Bosing</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Neumorphism bir tomondan oq nur (`-9px -9px #ffffff`), ikkinchi tomondan to'q soya (`9px 9px #bec3c9`) orqali elementning xuddi plastmassadan bo'rtib chiqqanidek ko'rinishini ta'minlaydi.

## Ishlash natijasi:
```text
Kulrang maydondan silliq bo'rtib chiqqan karta va bosilganda ichkariga botuvchi yumshoq tugma.
```

---

# 955-Topshiriq: Foydalanuvchi do'stona Modal Dialog oynasi (Qorong'i parda va yopish tugmasi)
## Topshiriq sharti:
To'liq ekranni to'suvchi overlay va markazda ochilgan, oson yopiluvchi modal dialog quting.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Accessible Modal Dialog</title>
  <style>
    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.7);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 16px;
      z-index: 1000;
      font-family: sans-serif;
    }
    .modal-box {
      position: relative;
      background: white;
      width: 100%;
      max-width: 340px;
      padding: 24px;
      border-radius: 12px;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
    }
    .close-x {
      position: absolute;
      top: 14px;
      right: 14px;
      background: none;
      border: none;
      font-size: 20px;
      color: #94a3b8;
      cursor: pointer;
    }
    .actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }
  </style>
</head>
<body>
  <div class="modal-backdrop">
    <div class="modal-box">
      <button class="close-x">&times;</button>
      <h3 style="margin-top: 0;">Hisobni o'chirish</h3>
      <p style="color: #64748b; font-size: 14px; line-height: 1.5;">Haqiqatan ham hisobingizni butunlay o'chirmoqchimisiz? Ushbu amal qaytarilmaydi.</p>
      <div class="actions">
        <button style="padding: 8px 14px; border: 1px solid #cbd5e1; background: white; border-radius: 6px;">Bekor</button>
        <button style="padding: 8px 14px; background: #ef4444; color: white; border: none; border-radius: 6px;">O'chirish</button>
      </div>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`position: fixed; inset: 0` orqali butun ekran to'siladi va foydalanuvchining e'tibori faqat markaziy xabar darchasiga qaratiladi.

## Ishlash natijasi:
```text
Qoramtir pardalangan fonda oq toza ogohlantirish darchasi, burchakda 'x' va pastda tasdiqlash tugmalari.
```

---

# 956-Topshiriq: Mega Menyu: Ko'p ustunli navigatsiya paneli (Mega Dropdown)
## Topshiriq sharti:
Hover qilinganda 3 ta ustunga bo'lingan boy ma'lumotli katta navigatsiya menyusini oching.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mega Menu Layout</title>
  <style>
    .nav-bar { background: #0f172a; padding: 0 20px; font-family: sans-serif; }
    .mega-parent { position: relative; display: inline-block; }
    .mega-trigger { background: none; border: none; color: white; padding: 16px 20px; cursor: pointer; font-size: 15px; }
    .mega-menu {
      display: none;
      position: absolute;
      top: 100%;
      left: 0;
      width: 480px;
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.15);
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      z-index: 100;
    }
    .mega-parent:hover .mega-menu { display: grid; }
    .col h4 { margin: 0 0 10px 0; color: #2563eb; font-size: 14px; }
    .col a { display: block; color: #334155; text-decoration: none; font-size: 13px; margin-bottom: 6px; }
  </style>
</head>
<body>
  <div class="nav-bar">
    <div class="mega-parent">
      <button class="mega-trigger">Katalog &#9662;</button>
      <div class="mega-menu">
        <div class="col">
          <h4>Frontend</h4>
          <a href="#">HTML & CSS</a><a href="#">JavaScript</a><a href="#">React</a>
        </div>
        <div class="col">
          <h4>Backend</h4>
          <a href="#">Python</a><a href="#">NodeJS</a><a href="#">PostgreSQL</a>
        </div>
        <div class="col">
          <h4>Mobil</h4>
          <a href="#">Flutter</a><a href="#">Kotlin</a><a href="#">Swift</a>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Katta korporativ va ta'lim portallarida Mega Menyu orqali yuzlab havolalarni bitta qulay 3 ustunli panjara orqali ko'rsatish mumkin.

## Ishlash natijasi:
```text
'Katalog' tugmasi ustiga sichqoncha kelganda ostidan 480px kenglikdagi 3 ustunli oq darcha ochiladi.
```

---

# 957-Topshiriq: Zamonaviy AI Chatbot UI Qobig'i (Muloqot darchasi va yozuv paneli)
## Topshiriq sharti:
Foydalanuvchi va AI xabarlari, kiritish inputi va yuborish tugmasidan iborat to'liq chat qobig'i.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Chatbot UI</title>
  <style>
    .chat-app {
      width: 320px;
      height: 420px;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      display: flex;
      flex-direction: column;
      background: #f8fafc;
      font-family: sans-serif;
      overflow: hidden;
      box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .chat-header { background: #1e293b; color: white; padding: 14px; font-weight: bold; display: flex; align-items: center; gap: 8px; }
    .chat-body { flex: 1; padding: 14px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
    .msg { max-width: 80%; padding: 8px 12px; border-radius: 8px; font-size: 13px; line-height: 1.4; }
    .msg-bot { align-self: flex-start; background: white; border: 1px solid #cbd5e1; }
    .msg-user { align-self: flex-end; background: #2563eb; color: white; }
    .chat-footer { padding: 10px; background: white; border-top: 1px solid #e2e8f0; display: flex; gap: 8px; }
    .chat-input { flex: 1; padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 20px; outline: none; }
  </style>
</head>
<body>
  <div class="chat-app">
    <div class="chat-header"><span>&#129302;</span> Antigravity AI Assistant</div>
    <div class="chat-body">
      <div class="msg msg-bot">Assalomu alaykum! Sizga qanday yordam bera olaman?</div>
      <div class="msg msg-user">HTML va CSS da grid qanday ishlaydi?</div>
      <div class="msg msg-bot">CSS Grid ikki o'lchamli qolip yaratish uchun xizmat qiladi...</div>
    </div>
    <div class="chat-footer">
      <input type="text" class="chat-input" placeholder="Savol bering...">
      <button style="background:#2563eb; color:white; border:none; width:34px; height:34px; border-radius:50%; cursor:pointer;">&uarr;</button>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Flexbox ustun maketi yordamida xabarlar oqimi avtomatik skroll bo'ladi, AI va foydalanuvchi xabarlari `align-self` bilan ikki tomonga taqsimlanadi.

## Ishlash natijasi:
```text
Tepadagi qora sarlavha, o'rtada suhbat pufakchalari va pastda yumaloq yuborish tugmasi bo'lgan zamonaviy AI chat.
```

---

# 958-Topshiriq: Toast Notifications Stack (Xabarnomalar qatlami)
## Topshiriq sharti:
Ekranning pastki o'ng burchagida ustma-ust chiquvchi Muvaffaqiyat va Ogohlantirish xabarnomalari.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Toast Notifications Stack</title>
  <style>
    .toast-container {
      position: fixed;
      bottom: 20px;
      right: 20px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      font-family: sans-serif;
      z-index: 999;
    }
    .toast {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 12px 18px;
      border-radius: 8px;
      color: white;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      font-size: 14px;
      animation: slideIn 0.3s ease;
    }
    .toast-success { background: #16a34a; }
    .toast-warn { background: #ea580c; }
    @keyframes slideIn { from { transform: translateX(100%); } to { transform: translateX(0); } }
  </style>
</head>
<body>
  <div class="toast-container">
    <div class="toast toast-success">&#10003; Foydalanuvchi saqlandi!</div>
    <div class="toast toast-warn">&#9888; Xotira to'lib bormoqda</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`position: fixed; bottom: 20px; right: 20px` va `flex-direction: column` barcha tizim xabarnomalarini o'ng burchakda qulay taxlaydi.

## Ishlash natijasi:
```text
Ekranning o'ng quyi burchagida yashil va to'q sariq rangli ikkita zamonaviy xabarnoma.
```

---

# 959-Topshiriq: E-Commerce Mahsulot Kartasi (Savatga qo'shish va Tanlovlar)
## Topshiriq sharti:
Mahsulot rasmi, o'lcham tanlovchi chiplar va 'Savatga' tugmasidan iborat savdo kartasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Product Details Card</title>
  <style>
    .product-box {
      width: 240px;
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 10px;
      overflow: hidden;
      font-family: sans-serif;
      box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .p-pic { height: 140px; background: #64748b; }
    .p-body { padding: 14px; }
    .sizes { display: flex; gap: 6px; margin: 10px 0; }
    .size-btn { width: 30px; height: 30px; border: 1px solid #cbd5e1; background: none; border-radius: 4px; cursor: pointer; }
    .size-btn.active { background: #0f172a; color: white; border-color: #0f172a; }
    .btn-buy { width: 100%; padding: 10px; background: #2563eb; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }
  </style>
</head>
<body>
  <div class="product-box">
    <div class="p-pic"></div>
    <div class="p-body">
      <h4 style="margin:0 0 6px 0;">Krossovka Air Max</h4>
      <strong style="color: #2563eb; font-size: 18px;">$120</strong>
      <div class="sizes">
        <button class="size-btn">40</button>
        <button class="size-btn active">41</button>
        <button class="size-btn">42</button>
      </div>
      <button class="btn-buy">Savatga qo'shish</button>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
E-tijorat kartochkasida surat, narx, o'lcham tugmalari va to'liq enli xarid tugmasi ixcham va chiroyli birlashtirilgan.

## Ishlash natijasi:
```text
Zamonaviy internet do'kon krossovka kartasi.
```

---

# 960-Topshiriq: Kirish va Ro'yxatdan o'tish (Auth Login / Register Form) zamonaviy shakli
## Topshiriq sharti:
Email, Parol, 'Meni eslab qol' va zamonaviy gradient fonli Kirish darchasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Modern Login UI</title>
  <style>
    body { margin: 0; height: 100vh; display: flex; align-items: center; justify-content: center; background: #f1f5f9; font-family: sans-serif; }
    .login-box {
      width: 280px;
      padding: 30px;
      background: white;
      border-radius: 12px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.06);
    }
    .field { margin-bottom: 14px; }
    .field label { display: block; font-size: 12px; margin-bottom: 4px; color: #475569; font-weight: bold; }
    .field input { width: 100%; box-sizing: border-box; padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px; }
    .submit-btn { width: 100%; padding: 12px; background: #2563eb; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }
  </style>
</head>
<body>
  <div class="login-box">
    <h3 style="margin: 0 0 16px 0; text-align: center;">Tizimga Kirish</h3>
    <div class="field">
      <label>Email</label>
      <input type="email" placeholder="nom@sayt.uz">
    </div>
    <div class="field">
      <label>Parol</label>
      <input type="password" placeholder="••••••••">
    </div>
    <button class="submit-btn">Kirish</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Toza maydonlar, ixcham soyalar va aniq yozuvlar kirish formasini foydalanuvchi uchun yoqimli va ishonchli qiladi.

## Ishlash natijasi:
```text
Oq fonli toza va tartibli tizimga kirish formasi.
```

---

# 961-Topshiriq: Foydalanuvchi Profil Sahifasi (Header Cover, Avatar va Statistika)
## Topshiriq sharti:
Foydalanuvchi sahifasi tepasidagi banner, unga minib turgan dumaloq avatar va obunachilar soni.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>User Profile Header</title>
  <style>
    .profile-wrap {
      width: 320px;
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 12px;
      overflow: hidden;
      font-family: sans-serif;
    }
    .cover { height: 90px; background: linear-gradient(135deg, #3b82f6, #9333ea); }
    .profile-info { padding: 0 20px 20px; text-align: center; }
    .avatar-pop {
      width: 64px;
      height: 64px;
      border-radius: 50%;
      background: #0f172a;
      color: white;
      border: 4px solid white;
      margin: -32px auto 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      font-weight: bold;
    }
    .stats { display: flex; justify-content: space-around; margin-top: 16px; border-top: 1px solid #e2e8f0; padding-top: 12px; font-size: 13px; }
  </style>
</head>
<body>
  <div class="profile-wrap">
    <div class="cover"></div>
    <div class="profile-info">
      <div class="avatar-pop">MS</div>
      <h4 style="margin: 0;">Madina Saidova</h4>
      <small style="color: #64748b;">UI/UX Dizayner</small>
      <div class="stats">
        <div><strong>1.2k</strong><br><small>Obunachi</small></div>
        <div><strong>480</strong><br><small>Loyihalar</small></div>
      </div>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`margin: -32px auto 8px` orqali avatar banner va matn o'rtasiga yarim minib turadi (Twitter/LinkedIn profillari uslubi).

## Ishlash natijasi:
```text
Gradient bannerli va o'rtasida dumaloq oq hoshiyali avatari bo'lgan profil kartasi.
```

---

# 962-Topshiriq: Kanban Board Ustunlari (Vazifalar boshqaruv paneli)
## Topshiriq sharti:
'Rejada' va 'Bajarildi' ustunlari va ularning ichidagi harakatlanuvchi kartochkalar.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Kanban Board Grid</title>
  <style>
    .board { display: flex; gap: 14px; padding: 20px; background: #f1f5f9; font-family: sans-serif; }
    .column { width: 150px; background: #e2e8f0; border-radius: 8px; padding: 10px; display: flex; flex-direction: column; gap: 8px; }
    .col-title { font-size: 13px; font-weight: bold; color: #475569; margin-bottom: 4px; }
    .task { background: white; padding: 10px; border-radius: 6px; font-size: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
  </style>
</head>
<body>
  <div class="board">
    <div class="column">
      <div class="col-title">Rejada (2)</div>
      <div class="task">Grid maketini tuzish</div>
      <div class="task">Animatsiya qo'shish</div>
    </div>
    <div class="column">
      <div class="col-title">Bajarildi (1)</div>
      <div class="task" style="border-left: 3px solid #16a34a;">HTML semantikasi</div>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Trello va Jira uslubidagi kanban ustunlari vazifalarni bosqichma-bosqich boshqarish uchun eng mashhur tartibdir.

## Ishlash natijasi:
```text
Ikkita kulrang ustun ichidagi oq vazifalar kartachalari.
```

---

# 963-Topshiriq: Fayl Yuklash uchun Drag & Drop (Dropzone) maydoni
## Topshiriq sharti:
Faylni tashlash maydoni, papka ikonkasi va qabul qilinadigan formatlar ro'yxati.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dropzone UI</title>
  <style>
    .dropzone {
      width: 260px;
      padding: 30px;
      border: 2px dashed #93c5fd;
      background: #eff6ff;
      border-radius: 12px;
      text-align: center;
      font-family: sans-serif;
      cursor: pointer;
      transition: border-color 0.2s, background-color 0.2s;
    }
    .dropzone:hover { border-color: #2563eb; background: #dbeafe; }
    .drop-icon { font-size: 36px; color: #2563eb; margin-bottom: 8px; }
  </style>
</head>
<body>
  <div class="dropzone">
    <div class="drop-icon">&#128193;</div>
    <strong>Faylni bu yerga torting</strong>
    <p style="margin: 4px 0 0; font-size: 11px; color: #64748b;">PNG, JPG yoki PDF (Maks. 25MB)</p>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Punktirli ramka va hover effekti foydalanuvchiga faylni sudrab tashlash mumkinligini darhol bildiradi.

## Ishlash natijasi:
```text
Moviy fondagi chiroyli fayl yuklash maydonchasi.
```

---

# 964-Topshiriq: Audio Player Vidjeti: Trek nomi, ijro va vaqt chizig'i
## Topshiriq sharti:
Ixcham musiqa pleeri: albom muqovasi, ijro tugmasi va progress chizig'i.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Audio Player Widget</title>
  <style>
    .player-card {
      display: flex;
      align-items: center;
      gap: 12px;
      width: 280px;
      background: #1e293b;
      color: white;
      padding: 12px;
      border-radius: 10px;
      font-family: sans-serif;
    }
    .p-cover { width: 44px; height: 44px; background: #3b82f6; border-radius: 6px; display: flex; align-items: center; justify-content: center; }
    .p-info { flex: 1; }
    .p-bar { height: 4px; background: #334155; border-radius: 2px; margin-top: 6px; overflow: hidden; }
    .p-fill { width: 45%; height: 100%; background: #38bdf8; }
  </style>
</head>
<body>
  <div class="player-card">
    <div class="p-cover">&#9835;</div>
    <div class="p-info">
      <div style="font-size: 13px; font-weight: bold;">Audio Dars 01</div>
      <div class="p-bar"><div class="p-fill"></div></div>
    </div>
    <button style="background:white; border:none; width:32px; height:32px; border-radius:50%; cursor:pointer;">&#9658;</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Qora fonda ko'k progress chizig'i va oq ijro tugmasi bilan zamonaviy audio pleer komponenti.

## Ishlash natijasi:
```text
To'q qora fondagi ixcham musiqa pleeri darchasi.
```

---

# 965-Topshiriq: Akkordeon FAQ Qidiruv paneli bilan integratsiyalashgan
## Topshiriq sharti:
Yuqorida savollarni qidirish inputi, pastda ochiluvchi savol-javoblar ro'yxati.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FAQ Search Accordion</title>
  <style>
    .faq-wrapper { width: 280px; font-family: sans-serif; }
    .search-faq { width: 100%; box-sizing: border-box; padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 6px; margin-bottom: 12px; }
    .faq-q { background: #f8fafc; border: 1px solid #e2e8f0; padding: 10px; border-radius: 6px; margin-bottom: 6px; font-weight: bold; font-size: 13px; cursor: pointer; }
    .faq-a { padding: 8px 10px; font-size: 12px; color: #64748b; }
  </style>
</head>
<body>
  <div class="faq-wrapper">
    <input type="text" class="search-faq" placeholder="Savollarni izlash...">
    <div class="faq-q">Kurs materiallari qancha vaqt ochiq?</div>
    <div class="faq-a">Darslar sizda umrbod qoladi.</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Qidiruv va akkordeon FAQ integratsiyasi yordam markazi sahifalarining asosi hisoblanadi.

## Ishlash natijasi:
```text
Qidiruv qatori ostidagi savol va uning javob qutisi.
```

---

# 966-Topshiriq: To'lov jarayoni Stepper (Checkout Steps): Savat &rarr; Manzil &rarr; To'lov
## Topshiriq sharti:
Uch bosqichli buyurtma berish zanjirini raqamli ko'rsatkichlar bilan quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Checkout Stepper</title>
  <style>
    .stepper-row { display: flex; align-items: center; justify-content: space-between; width: 280px; font-family: sans-serif; }
    .step-node { display: flex; flex-direction: column; align-items: center; font-size: 11px; }
    .circle { width: 26px; height: 26px; border-radius: 50%; background: #cbd5e1; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-bottom: 4px; }
    .circle.active { background: #16a34a; }
    .line { flex: 1; height: 2px; background: #cbd5e1; margin: 0 6px 16px; }
    .line.active { background: #16a34a; }
  </style>
</head>
<body>
  <div class="stepper-row">
    <div class="step-node"><div class="circle active">&#10003;</div><span>Savat</span></div>
    <div class="line active"></div>
    <div class="step-node"><div class="circle active">2</div><span>Manzil</span></div>
    <div class="line"></div>
    <div class="step-node"><div class="circle">3</div><span>To'lov</span></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Yashil rang faol va bajarilgan qadamlarni, kulrang esa kelgusi bosqichni ko'rsatadi.

## Ishlash natijasi:
```text
3 bosqichli chiroyli gorizontal to'lov qadamlari.
```

---

# 967-Topshiriq: Foydalanuvchi Sozlamalari (Tungi rejim, Ovoz, Xabarlar switch paneli)
## Topshiriq sharti:
3 ta qatorda sozlama matni va o'ng tomonida zamonaviy switch yoqgichlarini quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Settings Switch Panel</title>
  <style>
    .settings-list { width: 260px; background: white; border: 1px solid #cbd5e1; border-radius: 8px; font-family: sans-serif; }
    .s-row { display: flex; justify-content: space-between; align-items: center; padding: 12px; border-bottom: 1px solid #e2e8f0; font-size: 13px; }
    .s-row:last-child { border-bottom: none; }
  </style>
</head>
<body>
  <div class="settings-list">
    <div class="s-row"><span>Tungi rejim</span><input type="checkbox" checked style="accent-color:#2563eb;"></div>
    <div class="s-row"><span>Bildirishnomalar</span><input type="checkbox" checked style="accent-color:#2563eb;"></div>
    <div class="s-row"><span>Ovozli signallar</span><input type="checkbox" style="accent-color:#2563eb;"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Sozlamalar ro'yxati parametr va `accent-color` bilan bezatilgan switch orqali toza yig'ilgan.

## Ishlash natijasi:
```text
Uch qatorli parametrlar va ularning o'ng tomonidagi ko'k tanlov belgilari.
```

---

# 968-Topshiriq: Kompakt Mobil Qidiruv va Filtr dialogi (Search Overlay)
## Topshiriq sharti:
Mobilda ekranning tepasida paydo bo'luvchi qidiruv maydoni va tozalash tugmasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mobile Search Bar</title>
  <style>
    .search-bar-mob {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 20px;
      width: 260px;
      font-family: sans-serif;
    }
    .s-inp { flex: 1; border: none; outline: none; font-size: 13px; }
    .s-clear { background: #e2e8f0; border: none; width: 18px; height: 18px; border-radius: 50%; font-size: 11px; cursor: pointer; }
  </style>
</head>
<body>
  <div class="search-bar-mob">
    <span>&#128269;</span>
    <input type="text" class="s-inp" value="CSS Grid darslari">
    <button class="s-clear">&times;</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Lupa ikonkasi, matn va o'chirish 'x' doirachasi mobil ilovalardagi qidiruv tajribasini to'liq beradi.

## Ishlash natijasi:
```text
Ichida qidiruv so'zi va tozalash tugmasi bor yumaloq darcha.
```

---

# 969-Topshiriq: Cookie Rozilik Banneri (Cookie Consent Bar)
## Topshiriq sharti:
Ekranning tagida qotib turadigan 'Cookie-fayllarni qabul qilish' bildirishnomasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cookie Consent Banner</title>
  <style>
    .cookie-bar {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: #0f172a;
      color: white;
      padding: 14px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      font-family: sans-serif;
      font-size: 13px;
    }
    .cookie-btn { background: #2563eb; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-weight: bold; }
  </style>
</head>
<body>
  <div class="cookie-bar">
    <span>Sayt tajribasini yaxshilash uchun cookie-fayllardan foydalanamiz.</span>
    <button class="cookie-btn">Roziman</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`position: fixed; bottom: 0` sahifa tubida foydalanuvchiga xalal bermasdan rozilik olish mezonidir.

## Ishlash natijasi:
```text
Ekranning eng pastki qismida qora tasma va ko'k 'Roziman' tugmasi.
```

---

# 970-Topshiriq: 404 Xatolik Sahifasi (Sahifa topilmadi) zamonaviy dizayni
## Topshiriq sharti:
Katta 404 raqami, xabar matni va 'Bosh sahifaga qaytish' tugmasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>404 Not Found Page</title>
  <style>
    body { margin: 0; height: 100vh; display: flex; align-items: center; justify-content: center; background: #f8fafc; font-family: sans-serif; text-align: center; }
    .err-num { font-size: 72px; font-weight: 900; color: #2563eb; margin: 0; line-height: 1; }
    .err-title { font-size: 20px; color: #0f172a; margin: 10px 0; }
    .err-desc { color: #64748b; font-size: 14px; margin-bottom: 20px; }
    .home-btn { display: inline-block; padding: 10px 20px; background: #2563eb; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; }
  </style>
</head>
<body>
  <div>
    <h1 class="err-num">404</h1>
    <h2 class="err-title">Sahifa Topilmadi</h2>
    <p class="err-desc">Kechirasiz, siz qidirayotgan sahifa mavjud emas yoki o'chirilgan.</p>
    <a href="#" class="home-btn">Bosh sahifaga qaytish</a>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Katta yorqin 404 raqami va aniq harakat tugmasi adashib qolgan foydalanuvchini saytga qaytaradi.

## Ishlash natijasi:
```text
Katta ko'k 404 soni, tushuntirish va bosh sahifaga qaytish tugmasi.
```

---

# 971-Topshiriq: Xabarlar lentasi (Timeline Feed) kartalari
## Topshiriq sharti:
Vertikal chiziq ustida nuqtalar va vaqtga bog'langan xabarlar lentasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Timeline Feed</title>
  <style>
    .timeline { position: relative; padding-left: 24px; border-left: 2px solid #cbd5e1; font-family: sans-serif; }
    .t-node { position: relative; margin-bottom: 20px; }
    .t-node::before { content: ""; position: absolute; left: -31px; top: 4px; width: 12px; height: 12px; background: #2563eb; border-radius: 50%; }
  </style>
</head>
<body>
  <div class="timeline">
    <div class="t-node"><strong>10:00</strong> - Yangi dars yuklandi</div>
    <div class="t-node"><strong>11:30</strong> - Mentor savollarga javob berdi</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Vertikal chiziq va nuqtalar voqealarning ketma-ketlik vaqtini toza ko'rsatadi.

## Ishlash natijasi:
```text
Chapda vertikal chiziq va ko'k nuqtalar, o'ngda vaqt va voqea matni.
```

---

# 972-Topshiriq: Mahsulotlar Taqqoslash Jadvali (Feature Matrix)
## Topshiriq sharti:
3 ta tarif bo'yicha imkoniyatlarni qushchalar bilan taqqoslovchi jadval.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Comparison Matrix</title>
  <style>
    table { width: 100%; max-width: 340px; border-collapse: collapse; font-family: sans-serif; font-size: 13px; }
    th, td { padding: 8px; border-bottom: 1px solid #e2e8f0; text-align: center; }
    th:first-child, td:first-child { text-align: left; }
    .check { color: #16a34a; font-weight: bold; }
  </style>
</head>
<body>
  <table>
    <tr><th>Imkoniyat</th><th>Start</th><th>Pro</th></tr>
    <tr><td>Darslar</td><td class="check">&#10003;</td><td class="check">&#10003;</td></tr>
    <tr><td>Mentor</td><td>&mdash;</td><td class="check">&#10003;</td></tr>
  </table>
</body>
</html>
```

## Tushuntirish va Mantiq:
Tariflar imkoniyatini taqqoslash jadvali.

## Ishlash natijasi:
```text
Qushchali va chiziqli toza taqqoslash jadvali.
```

---

# 973-Topshiriq: Portfolio Loyihasi Kartasi (Surat, Teglar va Havola)
## Topshiriq sharti:
Dasturchi portfoliosi uchun loyiha surati va texnologiya teglari bo'lgan karta.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Portfolio Project Card</title>
  <style>
    .p-card { width: 240px; border: 1px solid #cbd5e1; border-radius: 8px; overflow: hidden; font-family: sans-serif; }
    .p-thumb { height: 110px; background: #3b82f6; }
    .p-info { padding: 12px; }
    .tag { display: inline-block; background: #e0e7ff; color: #4338ca; font-size: 11px; padding: 2px 6px; border-radius: 4px; margin-right: 4px; }
  </style>
</head>
<body>
  <div class="p-card">
    <div class="p-thumb"></div>
    <div class="p-info">
      <h4 style="margin: 0 0 6px 0;">E-Bozor Ilovasi</h4>
      <span class="tag">HTML</span><span class="tag">CSS</span><span class="tag">Grid</span>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Portfolio kartochkasida surat va texnologiya chiplari joylashgan.

## Ishlash natijasi:
```text
Ko'k rasmli va teglari bor portfolio kartasi.
```

---

# 974-Topshiriq: Mijozlar Fikrlari Slayderi (Testimonial Card)
## Topshiriq sharti:
Foydalanuvchi rasmi, yulduzcha reytingi va iliq fikr matnini joylang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Testimonial Card</title>
  <style>
    .testi-card { width: 260px; padding: 18px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; font-family: sans-serif; }
    .stars { color: #f59e0b; margin-bottom: 8px; }
    p { font-size: 13px; font-style: italic; color: #334155; margin: 0 0 10px 0; }
  </style>
</head>
<body>
  <div class="testi-card">
    <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
    <p>"Ushbu 1000 ta topshiriq orqali HTML va CSS bo'yicha bilimlarim tubdan o'zgardi!"</p>
    <strong>- Otabek N.</strong>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Yulduzlar va iqtibos matni ishonch uyg'otuvchi komponent yaratadi.

## Ishlash natijasi:
```text
5 ta sariq yulduzchali va muallif ismli fikr qutisi.
```

---

# 975-Topshiriq: Video Dars Pleylist Kartasi (Faol video indikatori)
## Topshiriq sharti:
Pleylistdagi joriy o'ynalayotgan videoni ajratib ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Video Playlist Item</title>
  <style>
    .pl-item { display: flex; align-items: center; gap: 10px; padding: 8px; border-radius: 6px; font-family: sans-serif; font-size: 13px; }
    .pl-item.playing { background: #eff6ff; color: #1d4ed8; font-weight: bold; }
    .pl-thumb { width: 50px; height: 30px; background: #cbd5e1; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="pl-item playing">
    <div class="pl-thumb"></div>
    <span>15. CSS Grid Murakkab Maketlar (Ijro etilmoqda)</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Faol dars fon rangi va qalin shrift bilan ajratiladi.

## Ishlash natijasi:
```text
Ochiq ko'k fondagi joriy ijro video bandi.
```

---

# 976-Topshiriq: Bildirishnomalar Markazi (Notification Dropdown Panel)
## Topshiriq sharti:
O'qilmagan xabarlar nuqtasi bilan bildirishnomalar ro'yxati darchasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Notification Center</title>
  <style>
    .notif-box { width: 260px; background: white; border: 1px solid #cbd5e1; border-radius: 8px; font-family: sans-serif; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .n-head { padding: 10px 14px; font-weight: bold; border-bottom: 1px solid #e2e8f0; }
    .n-row { display: flex; align-items: center; gap: 8px; padding: 10px 14px; border-bottom: 1px solid #f1f5f9; font-size: 12px; }
    .unread-dot { width: 6px; height: 6px; background: #2563eb; border-radius: 50%; }
  </style>
</head>
<body>
  <div class="notif-box">
    <div class="n-head">Bildirishnomalar</div>
    <div class="n-row"><span class="unread-dot"></span> Yangi topshiriq qo'shildi</div>
    <div class="n-row">Mentor javob qaytardi</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
O'qilmagan xabar yonidagi ko'k nuqtacha foydalanuvchini ogohlantiradi.

## Ishlash natijasi:
```text
Oq darchada ko'k nuqtali yangi xabar.
```

---

# 977-Topshiriq: Kupon / Promokod kiritish formasi (Input + Apply Button)
## Topshiriq sharti:
Chegirma promokodini kiritish va 'Qo'llash' tugmasidan iborat birikkan maydon.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Coupon Code Input</title>
  <style>
    .coupon-box { display: flex; width: 260px; font-family: sans-serif; }
    .c-inp { flex: 1; padding: 8px 12px; border: 1px solid #cbd5e1; border-right: none; border-radius: 6px 0 0 6px; outline: none; }
    .c-btn { background: #0f172a; color: white; border: none; padding: 8px 14px; border-radius: 0 6px 6px 0; cursor: pointer; }
  </style>
</head>
<body>
  <div class="coupon-box">
    <input type="text" class="c-inp" placeholder="PROMO2026">
    <button class="c-btn">Qo'llash</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Birikkan input va qora tugma ixcham promokod kiritish darchasi.

## Ishlash natijasi:
```text
Chapda maydon, o'ngda 'Qo'llash' tugmasi tutashgan blok.
```

---

# 978-Topshiriq: Xaridlar Savati ro'yxat bandi (Cart Item Row)
## Topshiriq sharti:
Mahsulot surati, nomi, soni (+/-) va narxi bo'lgan savat qatori.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Cart Item Row</title>
  <style>
    .cart-row { display: flex; align-items: center; gap: 10px; width: 280px; padding: 10px; border-bottom: 1px solid #e2e8f0; font-family: sans-serif; }
    .c-pic { width: 40px; height: 40px; background: #64748b; border-radius: 4px; }
    .c-title { flex: 1; font-size: 13px; }
    .c-price { font-weight: bold; color: #2563eb; }
  </style>
</head>
<body>
  <div class="cart-row">
    <div class="c-pic"></div>
    <div class="c-title">Dasturlash kitobi</div>
    <div class="c-price">$25</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Savatdagi mahsulot qatori.

## Ishlash natijasi:
```text
Rasm, kitob nomi va $25 narxidan iborat satr.
```

---

# 979-Topshiriq: Foydalanuvchi Ro'yxati / Kontaktlar jadvali (User Table Row)
## Topshiriq sharti:
Ism, Email, Rol (Admin badge) va Status ko'rsatilgan jadval qatori.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>User Table Row</title>
  <style>
    .user-table-row { display: flex; align-items: center; justify-content: space-between; width: 300px; padding: 10px; border-bottom: 1px solid #e2e8f0; font-family: sans-serif; font-size: 13px; }
    .role-badge { background: #dcfce7; color: #15803d; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: bold; }
  </style>
</head>
<body>
  <div class="user-table-row">
    <div><strong>Alisher R.</strong><br><small style="color:#64748b;">alisher@sayt.uz</small></div>
    <span class="role-badge">Admin</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Foydalanuvchilar boshqaruvi ro'yxati qatori.

## Ishlash natijasi:
```text
Chapda ism va email, o'ngda yashil 'Admin' nishoni.
```

---

# 980-Topshiriq: Yuklanish Skeleton Kartasi (Card Skeleton)
## Topshiriq sharti:
Surat va matn o'rnida turuvchi to'lqinlanuvchi kulrang placeholder karta.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Card Skeleton</title>
  <style>
    .sk-card { width: 220px; padding: 14px; border: 1px solid #e2e8f0; border-radius: 8px; }
    .sk-img { height: 100px; background: #e2e8f0; border-radius: 6px; margin-bottom: 10px; }
    .sk-line { height: 12px; background: #e2e8f0; border-radius: 3px; margin-bottom: 6px; }
  </style>
</head>
<body>
  <div class="sk-card">
    <div class="sk-img"></div>
    <div class="sk-line" style="width: 70%;"></div>
    <div class="sk-line" style="width: 40%;"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ma'lumotlar yuklangunga qadar qolip sifatida turadi.

## Ishlash natijasi:
```text
Kulrang rasm va chiziqchalardan iborat yuklanish qutisi.
```

---

# 981-Topshiriq: Reyting va Baholash Komponenti (Star Rating UI)
## Topshiriq sharti:
5 ta oltin yulduzcha va o'rtacha baho sonini ko'rsatuvchi vidjet.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Rating Widget</title>
  <style>
    .rate-box { display: flex; align-items: center; gap: 6px; font-family: sans-serif; }
    .stars { color: #f59e0b; font-size: 18px; }
    .score { font-weight: bold; font-size: 15px; color: #0f172a; }
  </style>
</head>
<body>
  <div class="rate-box">
    <span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
    <span class="score">4.9</span>
    <small style="color:#64748b;">(128 sharh)</small>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Mahsulot yoki kurs reytingini ifodalovchi yulduzlar qatori.

## Ishlash natijasi:
```text
Sariq yulduzchalar, '4.9' balli va sharhlar soni.
```

---

# 982-Topshiriq: Kompakt Narxlar Kalendari / Sana tanlash (Date Picker Day UI)
## Topshiriq sharti:
Oyning kunlari katakchalari va faol tanlangan kun nishoni.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Date Picker Days</title>
  <style>
    .days-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; width: 220px; font-family: sans-serif; text-align: center; }
    .d-box { padding: 8px; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 12px; cursor: pointer; }
    .d-box.selected { background: #2563eb; color: white; border-color: #2563eb; font-weight: bold; }
  </style>
</head>
<body>
  <div class="days-grid">
    <div class="d-box">Du 10</div>
    <div class="d-box selected">Se 11</div>
    <div class="d-box">Ch 12</div>
    <div class="d-box">Pa 13</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Sana tanlash panelidagi faol ko'k kun.

## Ishlash natijasi:
```text
Tanlangan 'Se 11' ko'k rangda ajralgan kunlar qatori.
```

---

# 983-Topshiriq: Avtomatik qisqaruvchi qidiruv teglari (Removable Tag List)
## Topshiriq sharti:
Tanlangan qidiruv teglari ro'yxati va ularning o'chirish belgilari.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Removable Tags List</title>
  <style>
    .tags-wrap { display: flex; gap: 8px; flex-wrap: wrap; font-family: sans-serif; }
    .tag-item { display: inline-flex; align-items: center; gap: 4px; background: #eff6ff; color: #1e40af; padding: 4px 10px; border-radius: 12px; font-size: 12px; }
  </style>
</head>
<body>
  <div class="tags-wrap">
    <span class="tag-item">HTML5 &times;</span>
    <span class="tag-item">CSS3 &times;</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
X belgili qidiruv chiplari.

## Ishlash natijasi:
```text
Ikkita moviy fonli o'chirish belgili teglar.
```

---

# 984-Topshiriq: Parol kuchliligi indikatori (Password Strength Meter)
## Topshiriq sharti:
Parol mustahkamligiga qarab 3 ta rangli chiziqchaning to'lishi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Password Strength Meter</title>
  <style>
    .meter-wrap { width: 220px; font-family: sans-serif; }
    .bars { display: flex; gap: 4px; margin-top: 6px; }
    .m-bar { flex: 1; height: 4px; background: #e2e8f0; border-radius: 2px; }
    .m-bar.filled { background: #16a34a; }
  </style>
</head>
<body>
  <div class="meter-wrap">
    <input type="password" value="KuchsizParol123" style="width:100%; padding:6px; box-sizing:border-box;">
    <div class="bars">
      <div class="m-bar filled"></div>
      <div class="m-bar filled"></div>
      <div class="m-bar filled"></div>
    </div>
    <small style="color:#16a34a; font-size:11px;">Kuchli parol</small>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
3 ta yashil chiziqcha orqali kuchli parol ko'rsatkichi.

## Ishlash natijasi:
```text
Yashil 3 ta chiziq va 'Kuchli parol' yozuvi.
```

---

# 985-Topshiriq: Mobil Ilova Navigatsiyasi (Floating Bottom Nav Bar)
## Topshiriq sharti:
Ekranning tagida suzib turuvchi yumaloq burchakli mobil navigatsiya.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Floating Bottom Bar</title>
  <style>
    .float-bar {
      position: fixed;
      bottom: 16px;
      left: 50%;
      transform: translateX(-50%);
      width: 260px;
      background: #0f172a;
      border-radius: 30px;
      display: flex;
      justify-content: space-around;
      padding: 10px 0;
      box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    }
    .nav-icon { color: #94a3b8; text-decoration: none; font-size: 20px; }
    .nav-icon.active { color: #38bdf8; }
  </style>
</head>
<body>
  <div class="float-bar">
    <a href="#" class="nav-icon active">&#8962;</a>
    <a href="#" class="nav-icon">&#128269;</a>
    <a href="#" class="nav-icon">&#128100;</a>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Markazlashtirilgan suzuvchi qora mobil navigatsiya paneli.

## Ishlash natijasi:
```text
Ekranning pastida qora doirasimon suzuvchi menyu.
```

---

# 986-Topshiriq: Statistika Taqqoslash Vidjeti (Growth KPI Delta)
## Topshiriq sharti:
O'tgan oyga nisbatan foiz o'sishi va yashil strelka ko'rsatkichi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Growth KPI Delta</title>
  <style>
    .kpi-card { width: 160px; padding: 14px; background: white; border: 1px solid #e2e8f0; border-radius: 8px; font-family: sans-serif; }
    .delta { display: flex; align-items: center; gap: 4px; color: #16a34a; font-size: 12px; font-weight: bold; margin-top: 6px; }
  </style>
</head>
<body>
  <div class="kpi-card">
    <small style="color:#64748b;">Foydalanuvchilar</small>
    <h3 style="margin: 4px 0 0 0;">8,450</h3>
    <div class="delta">&uarr; +24.8% o'sish</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Yashil yuqoriga strelka va foiz o'sishi.

## Ishlash natijasi:
```text
8,450 soni va ostida yashil '+24.8%' o'sish ko'rsatkichi.
```

---

# 987-Topshiriq: Yuklanish Foizi Halqasi (Circular Loader 85%)
## Topshiriq sharti:
85% to'lgan kamalaksimon yuklanish halqasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Circle Loader 85%</title>
  <style>
    .circle-wrap { width: 70px; height: 70px; border-radius: 50%; background: conic-gradient(#10b981 85%, #e2e8f0 0); display: flex; align-items: center; justify-content: center; }
    .circle-core { width: 54px; height: 54px; background: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: sans-serif; font-weight: bold; font-size: 13px; }
  </style>
</head>
<body>
  <div class="circle-wrap">
    <div class="circle-core">85%</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Yashil doiraviy 85% ko'rsatkich.

## Ishlash natijasi:
```text
Yashil halqa ichida 85% yozuvi.
```

---

# 988-Topshiriq: Yangiliklar Sarlavhasi Kartasi (Image Overlap Headline)
## Topshiriq sharti:
Surat ustiga qisman tushgan oq sarlavha qutisi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Headline Overlap</title>
  <style>
    .story-card { width: 240px; font-family: sans-serif; }
    .story-img { height: 120px; background: #64748b; border-radius: 8px; }
    .story-text { margin: -20px 10px 0; background: white; padding: 12px; border-radius: 6px; box-shadow: 0 4px 6px rgba(0,0,0,0.06); }
  </style>
</head>
<body>
  <div class="story-card">
    <div class="story-img"></div>
    <div class="story-text">
      <h4 style="margin:0 0 4px 0;">Muhim Voqea</h4>
      <small style="color:#64748b;">Yangilik matni</small>
    </div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`margin: -20px 10px 0` orqali matn qutisi rasm ustiga chiroyli chiqadi.

## Ishlash natijasi:
```text
Kulrang rasmga minib turgan oq sarlavha qutisi.
```

---

# 989-Topshiriq: Avtomatik Balandlikka Moslashuvchi Matn Maydoni (Chat Textarea)
## Topshiriq sharti:
Chat yoki izoh uchun ixcham yumaloq matn kiritish darchasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Chat Textarea</title>
  <style>
    .chat-row { display: flex; gap: 8px; align-items: flex-end; width: 280px; font-family: sans-serif; }
    textarea { flex: 1; resize: none; padding: 8px; border: 1px solid #cbd5e1; border-radius: 8px; height: 36px; box-sizing: border-box; }
    .send-icon-btn { background: #2563eb; color: white; border: none; width: 36px; height: 36px; border-radius: 8px; cursor: pointer; }
  </style>
</head>
<body>
  <div class="chat-row">
    <textarea placeholder="Fikringiz..."></textarea>
    <button class="send-icon-btn">&#10148;</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ixcham chat maydoni va ko'k yuborish tugmasi.

## Ishlash natijasi:
```text
Matn kiritish qutisi va o'ngda ko'k samolyotcha tugmasi.
```

---

# 990-Topshiriq: Tezkor Yordamchi Maslahat oynachasi (Hover Tooltip Card)
## Topshiriq sharti:
Kursor borganda paydo bo'luvchi qora maslahat oynasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Info Tooltip Card</title>
  <style>
    .tip-wrap { position: relative; display: inline-block; font-family: sans-serif; margin: 40px; }
    .tip-box { display: none; position: absolute; bottom: 120%; left: 50%; transform: translateX(-50%); background: #0f172a; color: white; padding: 6px 12px; border-radius: 4px; font-size: 12px; white-space: nowrap; }
    .tip-wrap:hover .tip-box { display: block; }
  </style>
</head>
<body>
  <div class="tip-wrap">
    <span style="color:#2563eb; cursor:pointer;">&#9432; Maslahat</span>
    <div class="tip-box">Bu yerda foydali ma'lumot bor!</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Hoverda ochiluvchi toza qora maslahat oynasi.

## Ishlash natijasi:
```text
So'z ustiga borganda tepasida to'q qora quticha ochiladi.
```

---

# 991-Topshiriq: Oddiy va Katta Rejim Switcheri (View Mode Toggle)
## Topshiriq sharti:
Jadval va Galereya ko'rinishlarini almashtiruvchi ikonkali tugma.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>View Mode Switch</title>
  <style>
    .toggle-bar { display: inline-flex; border: 1px solid #cbd5e1; border-radius: 6px; overflow: hidden; }
    .t-btn { padding: 6px 12px; border: none; background: white; cursor: pointer; }
    .t-btn.active { background: #2563eb; color: white; }
  </style>
</head>
<body>
  <div class="toggle-bar">
    <button class="t-btn active">&#9776; Ro'yxat</button>
    <button class="t-btn">&#8862; Panjara</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Ro'yxat va grid rejimlarini almashtirish tugmasi.

## Ishlash natijasi:
```text
Biri ko'k, biri oq tutashgan rejim almashtiruvchi.
```

---

# 992-Topshiriq: Fayl Yuklash Taraqqiyoti (Uploading Progress Item)
## Topshiriq sharti:
Fayl nomi, yuklangan foizi va qizil bekor qilish 'x' tugmasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Upload Progress Row</title>
  <style>
    .upload-row { width: 260px; padding: 10px; border: 1px solid #e2e8f0; border-radius: 6px; font-family: sans-serif; font-size: 12px; }
    .u-bar { height: 4px; background: #e2e8f0; border-radius: 2px; margin-top: 6px; overflow: hidden; }
    .u-fill { width: 65%; height: 100%; background: #16a34a; }
  </style>
</head>
<body>
  <div class="upload-row">
    <div style="display:flex; justify-content:space-between;">
      <strong>video_dars.mp4</strong>
      <span>65%</span>
    </div>
    <div class="u-bar"><div class="u-fill"></div></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Yashil chiziq bilan 65% yuklangan fayl ko'rsatkichi.

## Ishlash natijasi:
```text
Video fayl nomi, 65% va yashil to'ldirilgan tasma.
```

---

# 993-Topshiriq: Avtomatik Qorong'i / Yorug' rejim tanlagichi (Theme Toggle UI)
## Topshiriq sharti:
Quyosh va Oy ikonkalari bilan chiroyli tema tugmasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Theme Toggle Switch</title>
  <style>
    .theme-toggle { display: inline-flex; align-items: center; gap: 8px; padding: 6px 12px; background: #1e293b; color: white; border-radius: 20px; font-family: sans-serif; font-size: 13px; cursor: pointer; }
  </style>
</head>
<body>
  <div class="theme-toggle">
    <span>&#9728; Kunduz</span> | <span>&#9790; Tun</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Kunduzgi va tungi rejim tanlovchi ixcham panel.

## Ishlash natijasi:
```text
Qora dumaloq tugma ichida quyosh va oy yozuvlari.
```

---

# 994-Topshiriq: Tarmoq Ulanish Holati (Online / Offline Status Banner)
## Topshiriq sharti:
Internet uzilganda qizil fonli, ulanganda yashil fonli holat xabarnomasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Network Status Banner</title>
  <style>
    .net-banner { padding: 8px; text-align: center; font-family: sans-serif; font-size: 13px; font-weight: bold; }
    .online { background: #dcfce7; color: #166534; }
  </style>
</head>
<body>
  <div class="net-banner online">&#10003; Internetga muvaffaqiyatli ulandi</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Internet holati xabarnomasi.

## Ishlash natijasi:
```text
Och yashil fonda 'Internetga ulandi' yozuvi.
```

---

# 995-Topshiriq: Kupon chegirmasi hisoblangan savat yakuni (Order Summary)
## Topshiriq sharti:
Oraliq jami, chegirma va yakuniy to'lov miqdori ko'rsatilgan hisob-kitob bloki.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Order Summary Box</title>
  <style>
    .summary-card { width: 240px; padding: 16px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; font-family: sans-serif; font-size: 13px; }
    .sum-row { display: flex; justify-content: space-between; margin-bottom: 6px; }
    .total { border-top: 1px solid #cbd5e1; padding-top: 8px; font-weight: bold; font-size: 15px; color: #0f172a; }
  </style>
</head>
<body>
  <div class="summary-card">
    <div class="sum-row"><span>Oraliq narx:</span><span>$100</span></div>
    <div class="sum-row" style="color:#16a34a;"><span>Chegirma:</span><span>-$20</span></div>
    <div class="sum-row total"><span>Jami to'lov:</span><span>$80</span></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Chegirma va yakuniy narx hisoboti.

## Ishlash natijasi:
```text
Yashil chegirma va $80 yakuniy narx ko'rsatilgan kassa cheki.
```

---

# 996-Topshiriq: Parol tiklash (Forgot Password) minimalistik formasi
## Topshiriq sharti:
Email kiritish va tiklash havolasini yuborish darchasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Forgot Password UI</title>
  <style>
    .recover-box { width: 260px; padding: 20px; background: white; border: 1px solid #cbd5e1; border-radius: 8px; font-family: sans-serif; }
    input { width: 100%; box-sizing: border-box; padding: 8px; margin: 10px 0; border: 1px solid #cbd5e1; border-radius: 4px; }
    button { width: 100%; padding: 10px; background: #2563eb; color: white; border: none; border-radius: 4px; cursor: pointer; }
  </style>
</head>
<body>
  <div class="recover-box">
    <h4 style="margin:0;">Parolni tiklash</h4>
    <input type="email" placeholder="Emailingizni kiriting">
    <button>Havolani yuborish</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Parol tiklash uchun ixcham forma.

## Ishlash natijasi:
```text
Oq qutida email maydoni va ko'k tiklash tugmasi.
```

---

# 997-Topshiriq: Sayt Qidiruv Natijalari Kartasi (Search Result Snippet)
## Topshiriq sharti:
Sarlavha, yashil URL manzil va qisqa matnli qidiruv parchasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Search Snippet</title>
  <style>
    .snippet { max-width: 320px; font-family: sans-serif; }
    .s-url { font-size: 11px; color: #15803d; }
    .s-title { font-size: 16px; color: #1d4ed8; text-decoration: none; margin: 2px 0 4px; display: block; }
    .s-desc { font-size: 13px; color: #475569; margin: 0; }
  </style>
</head>
<body>
  <div class="snippet">
    <span class="s-url">https://edu.uz &gt; html-css</span>
    <a href="#" class="s-title">HTML va CSS to'liq o'quv kursi</a>
    <p class="s-desc">1,000 ta amaliy topshiriq va chuqur tushuntirishlar to'plami.</p>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Google qidiruv tizimi natijalari uslubidagi ko'rinish.

## Ishlash natijasi:
```text
Yashil havola, ko'k sarlavha va kulrang tavsif matni.
```

---

# 998-Topshiriq: Foydalanuvchi Ro'yxatdan O'tish Muvaffaqiyati (Success Celebration)
## Topshiriq sharti:
Katta yashil qushcha belgisi, tabrik matni va kabinetga o'tish tugmasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Registration Success</title>
  <style>
    .success-card { width: 260px; padding: 24px; background: white; border: 1px solid #cbd5e1; border-radius: 12px; text-align: center; font-family: sans-serif; }
    .check-circle { width: 48px; height: 48px; background: #16a34a; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; margin: 0 auto 12px; }
  </style>
</head>
<body>
  <div class="success-card">
    <div class="check-circle">&#10003;</div>
    <h3 style="margin: 0 0 6px 0;">Tabriklaymiz!</h3>
    <p style="margin: 0 0 16px 0; font-size: 13px; color: #64748b;">Hisobingiz muvaffaqiyatli yaratildi.</p>
    <button style="padding: 10px 20px; background: #16a34a; color: white; border: none; border-radius: 6px; cursor: pointer;">Kabinetga o'tish</button>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Muvaffaqiyatli ro'yxatdan o'tish tasdiq darchasi.

## Ishlash natijasi:
```text
Katta yashil qushchali oq qutlov oynasi.
```

---

# 999-Topshiriq: Dashboard Analitika Mini Vidjeti (Today vs Yesterday Bar)
## Topshiriq sharti:
Bugungi va kechagi savdo hajmini ikkita yonma-yon ustunchada solishtiring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Sales Delta Bars</title>
  <style>
    .comp-bars { display: flex; gap: 12px; align-items: flex-end; height: 80px; width: 140px; background: #f8fafc; padding: 10px; border-radius: 6px; font-family: sans-serif; font-size: 11px; }
    .b-wrap { display: flex; flex-direction: column; align-items: center; flex: 1; }
    .col-bar { width: 100%; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="comp-bars">
    <div class="b-wrap"><div class="col-bar" style="height: 45px; background: #94a3b8;"></div>Kecha</div>
    <div class="b-wrap"><div class="col-bar" style="height: 65px; background: #2563eb;"></div>Bugun</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Kecha va bugun ko'rsatkichini solishtiruvchi mini ustunli diagramma.

## Ishlash natijasi:
```text
Kulrang va ko'k ustunchali mini taqqoslash diagrammasi.
```

---

# 1000-Topshiriq: To'liq Zamonaviy Web Ilova Interfeysi: 1000-Topshiriq Cho'qqisi
## Topshiriq sharti:
Barcha 20 ta mavzuni (Semantika, Box Model, Flexbox, Grid, 3D Transforms, Animatsiyalar, O'zgaruvchilar va Responsive) o'zida birlashtirgan mukammal Web Ilova qobig'ini yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>1000-Topshiriq: Mukammal Web Ilova</title>
  <style>
    :root {
      --bg: #0f172a;
      --card-bg: #1e293b;
      --primary: #38bdf8;
      --text: #f8fafc;
      --radius: 12px;
    }
    body {
      margin: 0;
      min-height: 100vh;
      display: grid;
      grid-template-rows: auto 1fr auto;
      background-color: var(--bg);
      color: var(--text);
      font-family: sans-serif;
    }
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 24px;
      background: var(--card-bg);
      border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    main {
      padding: 24px;
      max-width: 900px;
      margin: 0 auto;
      width: 100%;
      box-sizing: border-box;
    }
    .hero-banner {
      background: linear-gradient(135deg, #2563eb, #7c3aed);
      padding: 30px;
      border-radius: var(--radius);
      text-align: center;
      margin-bottom: 24px;
      box-shadow: 0 10px 25px rgba(37,99,235,0.3);
    }
    .grid-cards {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
    }
    .card {
      background: var(--card-bg);
      padding: 20px;
      border-radius: var(--radius);
      border: 1px solid rgba(255,255,255,0.06);
      transition: transform 0.3s ease, border-color 0.3s;
    }
    .card:hover {
      transform: translateY(-5px);
      border-color: var(--primary);
    }
    footer {
      text-align: center;
      padding: 16px;
      font-size: 13px;
      color: #94a3b8;
      border-top: 1px solid rgba(255,255,255,0.08);
    }
  </style>
</head>
<body>
  <header>
    <strong style="color: var(--primary); font-size: 18px;">Antigravity Web Portal</strong>
    <span>1,000 / 1,000 Yakunlandi &#127881;</span>
  </header>
  <main>
    <div class="hero-banner">
      <h1 style="margin: 0 0 10px 0;">1,000 ta Topshiriq Cho'qqisi!</h1>
      <p style="margin: 0;">HTML5 va CSS3 bo'yicha eng to'liq va professional bilimlar poydevori.</p>
    </div>
    <div class="grid-cards">
      <div class="card">
        <h4 style="color: var(--primary); margin: 0 0 8px 0;">Semantika & Asoslar</h4>
        <p style="margin: 0; font-size: 13px; color: #94a3b8;">1 - 300 topshiriqlar to'liq o'zlashtirildi.</p>
      </div>
      <div class="card">
        <h4 style="color: var(--primary); margin: 0 0 8px 0;">Box Model & Flexbox</h4>
        <p style="margin: 0; font-size: 13px; color: #94a3b8;">301 - 650 topshiriqlar mukammal yechildi.</p>
      </div>
      <div class="card">
        <h4 style="color: var(--primary); margin: 0 0 8px 0;">Grid & Animatsiyalar</h4>
        <p style="margin: 0; font-size: 13px; color: #94a3b8;">651 - 1000 topshiriqlar muvaffaqiyatli yakunlandi.</p>
      </div>
    </div>
  </main>
  <footer>&copy; 2026 O'zbek Tili Ta'limiy Dasturlash Dataseti. Barcha huquqlar himoyalangan.</footer>
</body>
</html>
```

## Tushuntirish va Mantiq:
1000-topshiriq butun kursning yakuniy toji bo'lib, unda CSS Custom Properties, CSS Grid, Flexbox, Hover Transforms, Gradientlar va toza HTML5 semantikasi bir joyda to'liq mujassamlashtirilgan.

## Ishlash natijasi:
```text
Qorong'i rejimli to'q fonda gradient banner, 3 ta hoverda ko'tariluvchi karta va tepadagi bayramona navigatsiya paneli bilan to'liq web ilova.
```

---

