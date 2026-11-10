# HTML va CSS: CSS Animatsiyalar va Keyframes (Topshiriqlar 801 - 850)

# 801-Topshiriq: @keyframes qoidasi va animation-name, animation-duration asoslari
## Topshiriq sharti:
@keyframes va oddiy from/to (0% dan 100% gacha) orqali element rangini silliq o'zgartiruvchi animatsiya tuzing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Keyframes Asoslari</title>
  <style>
    @keyframes colorShift {
      from { background-color: #2563eb; }
      to   { background-color: #ef4444; }
    }
    .box-anim {
      width: 140px;
      padding: 16px;
      color: white;
      text-align: center;
      border-radius: 6px;
      font-family: sans-serif;
      animation-name: colorShift;
      animation-duration: 2s;
    }
  </style>
</head>
<body>
  <div class="box-anim">Rang O'zgarishi</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`@keyframes` animatsiyaning vaqt o'qi bo'yicha holatlarini belgilaydi. `from` (0%) boshlang'ich nuqtani, `to` (100%) esa yakuniy nuqtani ko'rsatadi. `animation-name` va `animation-duration` esa uni elementga bog'laydi.

## Ishlash natijasi:
```text
Ko'k to'rtburchak sahifa ochilganda 2 soniya ichida qizil rangga aylanadi va yana boshlang'ich rangiga qaytadi.
```

---

# 802-Topshiriq: Animation-iteration-count: infinite bilan cheksiz aylanuvchi Spinner
## Topshiriq sharti:
Doiraning to'xtovsiz bir maromda 360 gradusga aylanib turishini infinite orqali ta'minlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Infinite Spin</title>
  <style>
    @keyframes spinCircle {
      from { transform: rotate(0deg); }
      to   { transform: rotate(360deg); }
    }
    .spinner {
      width: 40px;
      height: 40px;
      border: 4px solid #e2e8f0;
      border-top-color: #2563eb;
      border-radius: 50%;
      animation: spinCircle 1s linear infinite;
    }
  </style>
</head>
<body>
  <div class="spinner"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`animation-iteration-count: infinite` animatsiyani cheksiz takrorlaydi. `linear` timing-funksiyasi bilan harakat to'xtovsiz va bir tekis aylanadi.

## Ishlash natijasi:
```text
Ko'k tepadagi chiziqchaga ega halqa tinimsiz soat strelkasi bo'ylab aylanib turadi.
```

---

# 803-Topshiriq: Animation-direction: alternate bilan tebranuvchi harakat
## Topshiriq sharti:
Elementning o'ngga borib, keyin sakrab orqaga qaytuvchi tebranishini alternate orqali quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Alternate Direction</title>
  <style>
    @keyframes oscillate {
      0%   { transform: translateX(0); }
      100% { transform: translateX(100px); }
    }
    .slider-ball {
      width: 32px;
      height: 32px;
      background: #10b981;
      border-radius: 50%;
      animation: oscillate 1.2s ease-in-out infinite alternate;
    }
  </style>
</head>
<body>
  <div class="slider-ball"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`animation-direction: alternate` animatsiya 100% ga yetgach, to'satdan boshiga sakramasdan, teskari tartibda 0% ga ravon qaytishini ta'minlaydi (mayatnik harakati).

## Ishlash natijasi:
```text
Yashil sharcha chapdan o'ngga 100px borib, yana mayinlik bilan chapga qaytib turadi.
```

---

# 804-Topshiriq: Animation-fill-mode: forwards bilan oxirgi holatda qolish
## Topshiriq sharti:
Animatsiya tugagandan so'ng element boshlang'ich holatga qaytmasdan, oxirgi 100% holatida qotib qolsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Fill Mode Forwards</title>
  <style>
    @keyframes fadeSlide {
      0%   { opacity: 0; transform: translateY(20px); }
      100% { opacity: 1; transform: translateY(0); }
    }
    .banner {
      width: 220px;
      padding: 16px;
      background: #0f172a;
      color: white;
      border-radius: 8px;
      font-family: sans-serif;
      animation: fadeSlide 1s ease forwards;
    }
  </style>
</head>
<body>
  <div class="banner">Oxirgi holatda qotgan karta</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`animation-fill-mode: forwards` animatsiya tugagach, oxirgi kadr (`100%`) stilini elementda saqlab qoladi. Sukutda (`none`) element darhol animatsiyadan oldingi holatiga sakrab qaytadi.

## Ishlash natijasi:
```text
To'q qora karta pastdan 20px ko'tarilib ravshanlashadi va o'sha yerda mustahkam qoladi.
```

---

# 805-Topshiriq: Pulse / Yurak urishi (Heartbeat) animatsiyasi
## Topshiriq sharti:
scale(1) dan scale(1.2) ga qisqa vaqtda shishib-qisqaruvchi pulsatsiya effekti yarating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Heartbeat Pulse</title>
  <style>
    @keyframes heartbeat {
      0%   { transform: scale(1); }
      25%  { transform: scale(1.15); }
      40%  { transform: scale(1); }
      60%  { transform: scale(1.15); }
      100% { transform: scale(1); }
    }
    .heart-btn {
      font-size: 32px;
      color: #ef4444;
      display: inline-block;
      animation: heartbeat 1.4s ease-in-out infinite;
    }
  </style>
</head>
<body>
  <span class="heart-btn">&hearts;</span>
</body>
</html>
```

## Tushuntirish va Mantiq:
Keyframeda 25% va 60% da ketma-ket ikki marta masshtab oshirilishi yurakning dub-dub urish ritmini to'liq takrorlaydi.

## Ishlash natijasi:
```text
Qizil yurak belgisi tirik inson yuragidek tinimsiz zarb bilan urib turadi.
```

---

# 806-Topshiriq: Skeleton Loading (Shimmer yaltirash effekti)
## Topshiriq sharti:
Ma'lumot yuklanayotganda kulrang blok ustidan yaltiroq gradient nuri o'tuvchi animatsiya quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Skeleton Loading Shimmer</title>
  <style>
    @keyframes shimmer {
      0%   { background-position: -200% 0; }
      100% { background-position: 200% 0; }
    }
    .skeleton-line {
      width: 240px;
      height: 16px;
      border-radius: 4px;
      background: linear-gradient(90deg, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%);
      background-size: 200% 100%;
      animation: shimmer 1.5s infinite;
      margin-bottom: 8px;
    }
  </style>
</head>
<body>
  <div class="skeleton-line" style="width: 180px;"></div>
  <div class="skeleton-line"></div>
  <div class="skeleton-line" style="width: 140px;"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Kengaytirilgan gradient foni `background-position` ni siljitish orqali chapdan o'ngga yorug'lik o'tish effekti (skeleton shimmer) yaratadi.

## Ishlash natijasi:
```text
Kulrang chiziqchalar ustidan silliq oqish nur to'lqinlari o'tib turadi.
```

---

# 807-Topshiriq: Yozuv mashinkasi effekti (Typing Effect steps() bilan)
## Topshiriq sharti:
Matn harflari birma-bir bosilib chiqayotgandek steps() funksiyasi va miltillovchi kursor yasang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Typing Effect</title>
  <style>
    @keyframes typing {
      from { width: 0; }
      to   { width: 14ch; }
    }
    @keyframes blink {
      50% { border-color: transparent; }
    }
    .typewriter {
      font-family: monospace;
      font-size: 18px;
      white-space: nowrap;
      overflow: hidden;
      border-right: 3px solid #2563eb;
      width: 14ch;
      animation: typing 2.5s steps(14) 1 normal both, blink 0.75s infinite;
    }
  </style>
</head>
<body>
  <div class="typewriter">Salom, Dunyo!</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`steps(14)` harakatni uzluksiz emas, aynan 14 ta alohida qadamga (har bir harf uchun bitta) bo'ladi. `ch` birligi esa belgi kengligini aniq o'lchaydi.

## Ishlash natijasi:
```text
Monospace shriftidagi 'Salom, Dunyo!' matni birma-bir bosilib chiqadi va o'ngdagi ko'k kursor miltillaydi.
```

---

# 808-Topshiriq: Animation-play-state: paused va hoverda to'xtatish
## Topshiriq sharti:
Tinimsiz harakatlanayotgan element ustiga sichqoncha olib kelinganda animatsiyani to'xtating (pauza).

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Animation Play State</title>
  <style>
    @keyframes moveX {
      0%   { transform: translateX(0); }
      100% { transform: translateX(120px); }
    }
    .moving-box {
      width: 100px;
      padding: 12px;
      background: #7c3aed;
      color: white;
      text-align: center;
      border-radius: 6px;
      font-family: sans-serif;
      animation: moveX 2s linear infinite alternate;
      cursor: pointer;
    }
    .moving-box:hover {
      animation-play-state: paused; /* Hoverda to'xtaydi */
    }
  </style>
</head>
<body>
  <div class="moving-box">Meni ushla!</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`animation-play-state: paused` animatsiyani joriy kadrida muzlatadi. Kursor olib ketilishi bilan `running` holatiga qaytib harakatni davom ettiradi.

## Ishlash natijasi:
```text
Harakatdagi binafsha quti ustiga kursor tekkanda darhol to'xtab qoladi.
```

---

# 809-Topshiriq: Sakrovchi to'p (Bouncing Ball) fizikasi
## Topshiriq sharti:
Yuqoridan erkin tushib polga urilib qayta sakrovchi to'p animatsiyasini foizlar bilan quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Bouncing Ball</title>
  <style>
    @keyframes bounce {
      0%, 100% { transform: translateY(0); animation-timing-function: cubic-bezier(0.8, 0, 1, 1); }
      50%      { transform: translateY(80px); animation-timing-function: cubic-bezier(0, 0, 0.2, 1); }
    }
    .ball {
      width: 36px;
      height: 36px;
      background: #f97316;
      border-radius: 50%;
      animation: bounce 1s infinite;
    }
  </style>
</head>
<body>
  <div class="ball"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
50% nuqtada (polga yetganda) timing-funksiyani o'zgartirish orqali tortishish kuchi va qayta sakrash fizikasi haqiqiydek namoyon bo'ladi.

## Ishlash natijasi:
```text
To'q sariq sharcha yuqoridan pastga tushib polga urilib tinimsiz sakrab turadi.
```

---

# 810-Topshiriq: Ripple / Radar to'lqin tarqalishi animatsiyasi
## Topshiriq sharti:
Yashil status nuqtasi atrofidan kattalashib so'nuvchi to'lqin halqasini hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Ripple Ping Animation</title>
  <style>
    @keyframes ping {
      0%   { transform: scale(1); opacity: 0.8; }
      100% { transform: scale(2.5); opacity: 0; }
    }
    .beacon-wrapper {
      position: relative;
      display: inline-block;
      width: 16px;
      height: 16px;
      margin: 20px;
    }
    .beacon-dot {
      width: 100%;
      height: 100%;
      background: #22c55e;
      border-radius: 50%;
    }
    .beacon-ring {
      position: absolute;
      inset: 0;
      background: #22c55e;
      border-radius: 50%;
      animation: ping 1.4s cubic-bezier(0, 0, 0.2, 1) infinite;
    }
  </style>
</head>
<body>
  <div class="beacon-wrapper">
    <div class="beacon-ring"></div>
    <div class="beacon-dot"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`beacon-ring` doirasi `scale(2.5)` gacha shishib, ayni paytda `opacity: 0` ga o'tadi va radar to'lqinini vujudga keltiradi.

## Ishlash natijasi:
```text
Yashil nuqta atrofidan tinimsiz yashil xira halqalar tarqalib so'nib turadi.
```

---

# 811-Topshiriq: Neon nurli sarlavha miltillashi (Glow Flicker)
## Topshiriq sharti:
Matn soyasi (text-shadow) miltillab yonib-o'chuvchi kiberpank neon effektini bering.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Neon Glow Animation</title>
  <style>
    @keyframes neonGlow {
      0%, 100% {
        text-shadow: 0 0 5px #06b6d4, 0 0 10px #06b6d4, 0 0 20px #06b6d4;
      }
      50% {
        text-shadow: 0 0 2px #06b6d4, 0 0 4px #06b6d4;
      }
    }
    body { background: #0f172a; padding: 30px; }
    .neon-text {
      color: #ffffff;
      font-family: sans-serif;
      font-size: 24px;
      font-weight: bold;
      animation: neonGlow 1.5s infinite alternate;
    }
  </style>
</head>
<body>
  <div class="neon-text">CYBER PORTAL</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`text-shadow` ning radiusini 5px dan 20px gacha o'zgartirish neon lampalarining kuchli va kuchsiz yonishini hosil qiladi.

## Ishlash natijasi:
```text
Qora fonda ko'k nur taratib miltillovchi oq sarlavha matni.
```

---

# 812-Topshiriq: Progress Bar qiya chiziqlarining oqishi (Striped Flow)
## Topshiriq sharti:
Progress bar ichidagi diagonal tasmalar background-position orqali cheksiz oqib tursin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Striped Flow Progress</title>
  <style>
    @keyframes moveStripes {
      from { background-position: 0 0; }
      to   { background-position: 30px 0; }
    }
    .stripe-bar {
      width: 240px;
      height: 16px;
      border-radius: 8px;
      background: repeating-linear-gradient(
        45deg,
        #2563eb,
        #2563eb 10px,
        #3b82f6 10px,
        #3b82f6 20px
      );
      background-size: 30px 30px;
      animation: moveStripes 1s linear infinite;
    }
  </style>
</head>
<body>
  <div class="stripe-bar"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`repeating-linear-gradient` yordamida qiya chiziqlar chiziladi va `background-position` ni 30px ga siljitish orqali uzluksiz oqim hosil bo'ladi.

## Ishlash natijasi:
```text
Ko'k chiziqli tasma o'ng tomonga qarab to'xtovsiz harakatlanadi.
```

---

# 813-Topshiriq: Ko'p bosqichli 4 bosqichli rang almashinuvi (0%, 33%, 66%, 100%)
## Topshiriq sharti:
Elementning sariq, yashil, ko'k va qizil ranglarga navbatma-navbat o'tishini foizlar bilan yozing.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Multi-Stage Keyframes</title>
  <style>
    @keyframes colorCycle {
      0%   { background-color: #f59e0b; }
      33%  { background-color: #10b981; }
      66%  { background-color: #2563eb; }
      100% { background-color: #ef4444; }
    }
    .multi-box {
      width: 140px;
      padding: 16px;
      color: white;
      text-align: center;
      border-radius: 8px;
      font-family: sans-serif;
      animation: colorCycle 4s linear infinite alternate;
    }
  </style>
</head>
<body>
  <div class="multi-box">4 Bosqich</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Oradagi foizlar (33%, 66%) orqali animatsiyaning murakkab ko'p qirrali o'zgarish traektoriyasini aniq belgilash mumkin.

## Ishlash natijasi:
```text
Quti sariqdan yashilga, so'ng ko'kka va qizilga silliq o'tib qaytadi.
```

---

# 814-Topshiriq: Pastga tushuvchi bildirishnoma (Drop In Slide)
## Topshiriq sharti:
Ekranning yuqori qismidan translateY(-50px) dan translateY(0) ga silliq tushuvchi alert paneli.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Slide Down Alert</title>
  <style>
    @keyframes dropIn {
      0%   { transform: translateY(-100%); opacity: 0; }
      100% { transform: translateY(0); opacity: 1; }
    }
    .top-alert {
      width: 260px;
      padding: 12px 16px;
      background: #dbeafe;
      border: 1px solid #93c5fd;
      color: #1e40af;
      border-radius: 6px;
      font-family: sans-serif;
      animation: dropIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
  </style>
</head>
<body>
  <div class="top-alert">Yangi xabar keldi!</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`translateY(-100%)` elementni o'z balandligicha tepaga chiqarib berkitadi, `dropIn` esa uni mayinlik bilan ekranga tushiradi.

## Ishlash natijasi:
```text
Tepadagi osmondan silliq pastga tushib o'rnashgan moviy bildirishnoma.
```

---

# 815-Topshiriq: Cheksiz aylanuvchi 3D disk (Flip Coin Infinite)
## Topshiriq sharti:
Tanganing Y o'qi bo'ylab 360 gradusga cheksiz aylanib turishini ta'minlang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Coin Flip 3D</title>
  <style>
    @keyframes flipCoin {
      0%   { transform: rotateY(0deg); }
      100% { transform: rotateY(360deg); }
    }
    .coin-wrap { perspective: 400px; display: inline-block; margin: 30px; }
    .coin {
      width: 50px;
      height: 50px;
      background: #eab308;
      border: 4px solid #ca8a04;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #713f12;
      font-weight: bold;
      animation: flipCoin 2s linear infinite;
    }
  </style>
</head>
<body>
  <div class="coin-wrap">
    <div class="coin">$</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`rotateY(360deg)` tangani 3D fazoda Y o'qi atrofida cheksiz aylantirib, o'yinlardagi tanga animatsiyasini hosil qiladi.

## Ishlash natijasi:
```text
Tillarang doira 3D fazoda to'xtovsiz aylanib turadi.
```

---

# 816-Topshiriq: Animation-delay bilan birin-ketin chiqish (Staggered Animation)
## Topshiriq sharti:
3 ta elementning ketma-ket 0s, 0.2s, 0.4s kechikish bilan ekranga chiqishini ko'rsating.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Staggered List</title>
  <style>
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    .list-item {
      padding: 10px 14px;
      background: #f1f5f9;
      border-radius: 6px;
      margin-bottom: 8px;
      font-family: sans-serif;
      animation: fadeIn 0.4s ease forwards;
      opacity: 0;
    }
    .i1 { animation-delay: 0.1s; }
    .i2 { animation-delay: 0.3s; }
    .i3 { animation-delay: 0.5s; }
  </style>
</head>
<body>
  <div class="list-item i1">1-Qator ma'lumoti</div>
  <div class="list-item i2">2-Qator ma'lumoti</div>
  <div class="list-item i3">3-Qator ma'lumoti</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Har bir elementga ortib boruvchi `animation-delay` berish foydalanuvchiga ro'yxatning dinamik yuklanish effektini (stagger) beradi.

## Ishlash natijasi:
```text
Uchta satr birin-ketin kaskad kabi ekranda paydo bo'ladi.
```

---

# 817-Topshiriq: Kattalashib yo'qoluvchi tugma bosish to'lqini (Click Wave)
## Topshiriq sharti:
Tugma markazidan doiraviy shaffof to'lqin tarqalib yo'qolsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Click Wave Animation</title>
  <style>
    @keyframes waveOut {
      0%   { transform: scale(0.5); opacity: 1; }
      100% { transform: scale(2.2); opacity: 0; }
    }
    .wave-btn {
      position: relative;
      padding: 12px 24px;
      background: #2563eb;
      color: white;
      border: none;
      border-radius: 6px;
      font-family: sans-serif;
      cursor: pointer;
      overflow: hidden;
    }
    .wave-circle {
      position: absolute;
      width: 100px;
      height: 100px;
      top: calc(50% - 50px);
      left: calc(50% - 50px);
      background: rgba(255, 255, 255, 0.4);
      border-radius: 50%;
      animation: waveOut 1.2s ease-out infinite;
    }
  </style>
</head>
<body>
  <button class="wave-btn">
    <span class="wave-circle"></span>
    Harakat Tugmasi
  </button>
</body>
</html>
```

## Tushuntirish va Mantiq:
Tugma ichidagi shaffof doira shishib yo'qolishi foydalanuvchining e'tiborini tortadi.

## Ishlash natijasi:
```text
Ko'k tugma ichidan oq to'lqin doirasi shishib tarqalib turadi.
```

---

# 818-Topshiriq: 3 ta nuqtali yuklanish animatsiyasi (Loading Dots Wave)
## Topshiriq sharti:
3 ta nuqtaning navbatma-navbat yuqoriga sakrab tushishini kechikish bilan hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Loading Dots</title>
  <style>
    @keyframes dotWave {
      0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
      40%           { transform: scale(1.2); opacity: 1; }
    }
    .dots-wrap { display: flex; gap: 6px; align-items: center; }
    .dot {
      width: 10px;
      height: 10px;
      background: #3b82f6;
      border-radius: 50%;
      animation: dotWave 1.4s infinite ease-in-out both;
    }
    .d1 { animation-delay: -0.32s; }
    .d2 { animation-delay: -0.16s; }
    .d3 { animation-delay: 0s; }
  </style>
</head>
<body>
  <div class="dots-wrap">
    <div class="dot d1"></div>
    <div class="dot d2"></div>
    <div class="dot d3"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Manfiy kechikishlar (`-0.32s`, `-0.16s`) animatsiyani allaqachon boshlanib ketgandek ko'rsatib, 3 ta nuqtaning to'lqinsimon tebranishini ta'minlaydi.

## Ishlash natijasi:
```text
Uchta ko'k nuqtacha birin-ketin to'lqin shaklida kattalashib-kichrayib turadi.
```

---

# 819-Topshiriq: Rasm tebranishi (Floating Island / Float effect)
## Topshiriq sharti:
Elementning fazoda vaznsizlikdagi kabi sekin yuqoriga va pastga suzib turishini quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Floating Animation</title>
  <style>
    @keyframes floatElem {
      0%   { transform: translateY(0); }
      50%  { transform: translateY(-12px); }
      100% { transform: translateY(0); }
    }
    .float-card {
      width: 180px;
      padding: 16px;
      background: #8b5cf6;
      color: white;
      border-radius: 10px;
      font-family: sans-serif;
      text-align: center;
      box-shadow: 0 10px 20px rgba(139, 92, 246, 0.3);
      animation: floatElem 3s ease-in-out infinite;
    }
  </style>
</head>
<body>
  <div class="float-card">Suzuvchi Orolcha</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`translateY(-12px)` va `ease-in-out` bilan 3 soniyalik sokin animatsiya havoda muallaq turish hissiyotini uyg'otadi.

## Ishlash natijasi:
```text
Binafsha rangli karta havoda suzgandek mayin yuqoriga-pastga tebranadi.
```

---

# 820-Topshiriq: Xatolik paytida qaltirash animatsiyasi (Form Shake)
## Topshiriq sharti:
Noto'g'ri parol kiritilganda input maydonining chapga-o'ngga qaltirashini bajaring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Error Shake</title>
  <style>
    @keyframes shake {
      0%, 100% { transform: translateX(0); }
      20%, 60% { transform: translateX(-8px); }
      40%, 80% { transform: translateX(8px); }
    }
    .error-input {
      width: 220px;
      padding: 10px;
      border: 2px solid #ef4444;
      border-radius: 6px;
      outline: none;
      font-family: sans-serif;
      animation: shake 0.4s ease-in-out;
    }
  </style>
</head>
<body>
  <input type="password" class="error-input" value="12345">
</body>
</html>
```

## Tushuntirish va Mantiq:
0.4 soniya ichida bir necha marta -8px va 8px ga siljish insonning 'yo'q' deb bosh chayqash harakatini ifodalaydi.

## Ishlash natijasi:
```text
Qizil hoshiyali input maydoni ochilganda tezlik bilan chapga-o'ngga silkinadi.
```

---

# 821-Topshiriq: Aylanuvchi yorug'lik nurlari (Conic Gradient Spin)
## Topshiriq sharti:
Karta orqasida aylanuvchi kamalaksimon chegara nuri animatsiyasini quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Border Beam Spin</title>
  <style>
    @keyframes spinBorder {
      from { transform: rotate(0deg); }
      to   { transform: rotate(360deg); }
    }
    .beam-box {
      position: relative;
      width: 180px;
      height: 100px;
      background: #0f172a;
      border-radius: 8px;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-family: sans-serif;
    }
    .beam-box::before {
      content: "";
      position: absolute;
      width: 250px;
      height: 250px;
      background: conic-gradient(from 0deg, transparent 70%, #38bdf8);
      animation: spinBorder 2s linear infinite;
    }
    .inner {
      position: relative;
      width: calc(100% - 4px);
      height: calc(100% - 4px);
      background: #0f172a;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  </style>
</head>
<body>
  <div class="beam-box">
    <div class="inner">Kiber Ramka</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`conic-gradient` aylanadi va 2px lik ichki oraliqdan ko'rinib aylanuvchi neon chegara effektini beradi.

## Ishlash natijasi:
```text
Qora karta chetida tinimsiz aylanib turuvchi moviy nurli chiziq.
```

---

# 822-Topshiriq: Kattalashib nafas oluvchi fon nuri (Breathing Glow)
## Topshiriq sharti:
Kartochkaning box-shadow nuri 10px dan 30px gacha nafas olgandek shishib tursin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Breathing Glow</title>
  <style>
    @keyframes breathe {
      0%, 100% { box-shadow: 0 0 10px rgba(37,99,235,0.4); }
      50%      { box-shadow: 0 0 30px rgba(37,99,235,0.9); }
    }
    .glow-card {
      width: 160px;
      padding: 20px;
      background: white;
      border-radius: 8px;
      text-align: center;
      font-family: sans-serif;
      animation: breathe 2s ease-in-out infinite;
    }
  </style>
</head>
<body>
  <div class="glow-card">Nafas Oluvchi Nur</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Soya radiusi va xiraligi 2 soniyada kattalashib kichrayadi.

## Ishlash natijasi:
```text
Oq karta atrofida ko'k nur taralib, keyin so'nib turadi.
```

---

# 823-Topshiriq: Avtomatik gorizontal yuguruvchi satr (Marquee Animation)
## Topshiriq sharti:
Matn qatorining ekranning o'ng chetidan kirib chap chetiga qarab uzluksiz oqishini hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>CSS Marquee</title>
  <style>
    @keyframes marquee {
      0%   { transform: translateX(100%); }
      100% { transform: translateX(-100%); }
    }
    .marquee-track {
      width: 260px;
      overflow: hidden;
      background: #f1f5f9;
      padding: 8px 0;
      white-space: nowrap;
      font-family: sans-serif;
      font-weight: bold;
      color: #0f172a;
    }
    .marquee-content {
      display: inline-block;
      animation: marquee 6s linear infinite;
    }
  </style>
</head>
<body>
  <div class="marquee-track">
    <span class="marquee-content">Tezkor Yangilik: Yangi darslar platformaga yuklandi!</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`translateX(100%)` dan `-100%` gacha `linear` harakat qadimgi `marquee` tegi o'rnini toza CSS bilan bosadi.

## Ishlash natijasi:
```text
Kulrang yo'lakcha ichida matn o'ngdan chapga qarab oqib o'tadi.
```

---

# 824-Topshiriq: Tepaga intiluvchi pufakchalar (Floating Bubbles)
## Topshiriq sharti:
Pastdan yuqoriga qarab uchib ketuvchi dumaloq pufakcha animatsiyasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Rising Bubble</title>
  <style>
    @keyframes rise {
      0%   { transform: translateY(60px) scale(0.6); opacity: 0; }
      50%  { opacity: 0.8; }
      100% { transform: translateY(-40px) scale(1.2); opacity: 0; }
    }
    .bubble {
      width: 24px;
      height: 24px;
      background: #38bdf8;
      border-radius: 50%;
      animation: rise 2s ease-in infinite;
      margin: 40px auto;
    }
  </style>
</head>
<body>
  <div class="bubble"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Pufakcha pastda paydo bo'lib, yuqoriga ko'tarilishi bilan shishadi va havoga singib yo'qoladi.

## Ishlash natijasi:
```text
Moviy havo pufakchasi pastdan tepaga ko'tarilib g'oyib bo'ladi.
```

---

# 825-Topshiriq: Chalg'ituvchi qulf ochilishi (Unlock Rotate)
## Topshiriq sharti:
Qulf kishanining 0deg dan 45deg ga aylanib ochilishini ifodalang.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Unlock Animation</title>
  <style>
    @keyframes unlock {
      0%   { transform: rotate(0); }
      100% { transform: rotate(-35deg) translateY(-4px); }
    }
    .lock-icon {
      font-size: 36px;
      display: inline-block;
      animation: unlock 0.6s ease forwards;
    }
  </style>
</head>
<body>
  <span class="lock-icon">&#128275;</span>
</body>
</html>
```

## Tushuntirish va Mantiq:
Kichik burilish va ko'tarilish qulfning ochilganlik xabarini beradi.

## Ishlash natijasi:
```text
Ochiq qulf belgisi burchakka burilib ochiladi.
```

---

# 826-Topshiriq: Aylanuvchi yuklanish doirasi (Dashoffset SVG/CSS)
## Topshiriq sharti:
border-radius va aylanma chegara bilan dairesel yuklanish paneli.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Circular Loader</title>
  <style>
    @keyframes dash {
      0%   { border-top-color: #2563eb; border-right-color: transparent; }
      50%  { border-top-color: #2563eb; border-right-color: #2563eb; }
      100% { border-top-color: transparent; border-right-color: transparent; }
    }
    .circle-loader {
      width: 32px;
      height: 32px;
      border: 3px solid #e2e8f0;
      border-radius: 50%;
      animation: dash 1.5s linear infinite;
    }
  </style>
</head>
<body>
  <div class="circle-loader"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Chegara ranglarini davriy o'zgartirish orqali aylanuvchi to'ldiruvchi halqa hosil qilinadi.

## Ishlash natijasi:
```text
Halqaning qirralari navbatma-navbat yonib-o'chib turadi.
```

---

# 827-Topshiriq: Aylanuvchi qumsoat animatsiyasi (Hourglass Flip)
## Topshiriq sharti:
Qumsoat 180 gradus aylanib, 1 soniya kutib yana aylansin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Hourglass Flip</title>
  <style>
    @keyframes flipGlass {
      0%, 20%   { transform: rotate(0deg); }
      80%, 100% { transform: rotate(180deg); }
    }
    .glass-icon {
      font-size: 32px;
      display: inline-block;
      animation: flipGlass 2s infinite ease-in-out;
    }
  </style>
</head>
<body>
  <span class="glass-icon">&#9203;</span>
</body>
</html>
```

## Tushuntirish va Mantiq:
Boshida va oxirida pauza (20% va 80%) qo'yish qumsoatning qumi to'kilib bo'lgach aylantirilishi mantig'ini beradi.

## Ishlash natijasi:
```text
Qumsoat tinch turadi, so'ng keskin 180 gradus aylanadi va yana to'xtaydi.
```

---

# 828-Topshiriq: Karta ochilishida tebranuvchi silkinish (Tada Effect)
## Topshiriq sharti:
Muvaffaqiyat qozonilganda karta kattalashib tebranib chiqsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Tada Win Effect</title>
  <style>
    @keyframes tada {
      0%       { transform: scale(1); }
      10%, 20% { transform: scale(0.9) rotate(-3deg); }
      30%, 50%, 70%, 90% { transform: scale(1.1) rotate(3deg); }
      40%, 60%, 80%      { transform: scale(1.1) rotate(-3deg); }
      100%     { transform: scale(1) rotate(0); }
    }
    .prize-box {
      width: 140px;
      padding: 16px;
      background: #f59e0b;
      color: white;
      text-align: center;
      border-radius: 8px;
      font-family: sans-serif;
      font-weight: bold;
      animation: tada 1s ease;
    }
  </style>
</head>
<body>
  <div class="prize-box">Yutuq Chiqdi!</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Animate.css ning mashhur 'Tada' effekti: quti kichrayib oladi va keyin quvnoqlik bilan qaltirab nishonlaydi.

## Ishlash natijasi:
```text
Sariq quti quvonchli tebranish bilan ekranga chiqadi.
```

---

# 829-Topshiriq: Yorug'lik chirog'ining xira miltillashi (Glitch Light)
## Topshiriq sharti:
Opasitini 1, 0.4, 0.8, 0.2 qilib eskirgan lampochka miltillashini hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Glitch Flicker</title>
  <style>
    @keyframes flicker {
      0%, 19.999%, 22%, 62.999%, 64%, 64.999%, 70%, 100% { opacity: 1; }
      20%, 21.999%, 63%, 63.999%, 65%, 69.999% { opacity: 0.3; }
    }
    .flicker-text {
      font-size: 24px;
      font-family: sans-serif;
      font-weight: bold;
      color: #ef4444;
      animation: flicker 2s infinite;
    }
  </style>
</head>
<body>
  <div class="flicker-text">XAVF!</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Noaniq vaqt intervallarida opasitini keskin tushirish eskirgan neon chiroqlar effektini yaratadi.

## Ishlash natijasi:
```text
Qizil 'XAVF!' yozuvi kutilmagan lahzalarda miltillab o'chib-yonadi.
```

---

# 830-Topshiriq: Uchuvchi samolyot harakati (Translate diagonal)
## Topshiriq sharti:
Samolyot ikonkasi chap pastdan o'ng yuqoriga uchib o'tib ketsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Flight Animation</title>
  <style>
    @keyframes flyPlane {
      0%   { transform: translate(0, 40px) rotate(-15deg); opacity: 0; }
      50%  { opacity: 1; }
      100% { transform: translate(140px, -40px) rotate(-15deg); opacity: 0; }
    }
    .plane {
      font-size: 28px;
      display: inline-block;
      animation: flyPlane 2.5s ease-in-out infinite;
    }
  </style>
</head>
<body>
  <span class="plane">&#9992;</span>
</body>
</html>
```

## Tushuntirish va Mantiq:
Diagonal `translate(x, y)` koordinatalari parvoz chizig'ini hosil qiladi.

## Ishlash natijasi:
```text
Kichik samolyot diagonal bo'yicha yuqoriga uchib o'tib turadi.
```

---

# 831-Topshiriq: Aylanuvchi fon gradienti (Gradient Background Shift)
## Topshiriq sharti:
Fon gradientining ranglari 3 soniya ichida to'lqinlanib o'zgarib tursin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Gradient Shift</title>
  <style>
    @keyframes gradMove {
      0%   { background-position: 0% 50%; }
      50%  { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
    .grad-banner {
      width: 240px;
      height: 90px;
      background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
      background-size: 400% 400%;
      border-radius: 8px;
      animation: gradMove 5s ease infinite;
    }
  </style>
</head>
<body>
  <div class="grad-banner"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`background-size: 400% 400%` orqali ulkan ranglar palitrasi yaratiladi va uning koordinatalari siljitiladi.

## Ishlash natijasi:
```text
To'rtburchak fonida to'rt xil rang tinimsiz mayin oqib turadi.
```

---

# 832-Topshiriq: Balandlikning noldan ochilishi (Accordion Height Expand)
## Topshiriq sharti:
max-height: 0 dan max-height: 100px ga ochiluvchi animatsiya.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Max Height Animation</title>
  <style>
    @keyframes slideOpen {
      from { max-height: 0; opacity: 0; }
      to   { max-height: 80px; opacity: 1; }
    }
    .acc-panel {
      width: 220px;
      background: #f1f5f9;
      border-radius: 6px;
      overflow: hidden;
      font-family: sans-serif;
      padding: 10px;
      animation: slideOpen 0.5s ease forwards;
    }
  </style>
</head>
<body>
  <div class="acc-panel">Ushbu panel silliq pastga yoyilib ochildi.</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`max-height` va `opacity` orqali panel balandligi noldan boshlab to'liq ochiladi.

## Ishlash natijasi:
```text
Kulrang quti balandligi pastga qarab cho'zilib matnni ochadi.
```

---

# 833-Topshiriq: Pufakcha kursor bosilganda kattalashib yorilishi (Pop Effect)
## Topshiriq sharti:
scale(0) dan scale(1.3) ga chiqib, so'ng scale(1) ga qaytuvchi Pop animatsiyasi.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Pop In Animation</title>
  <style>
    @keyframes popIn {
      0%   { transform: scale(0); opacity: 0; }
      70%  { transform: scale(1.2); }
      100% { transform: scale(1); opacity: 1; }
    }
    .pop-bubble {
      width: 80px;
      height: 80px;
      background: #ec4899;
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: sans-serif;
      font-weight: bold;
      animation: popIn 0.5s ease forwards;
    }
  </style>
</head>
<body>
  <div class="pop-bubble">POP!</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Element noldan boshlab birdaniga kattalashadi va so'ng o'z tabiiy hajmiga qaytadi.

## Ishlash natijasi:
```text
Dumaloq pushti shar 'POP!' yozuvi bilan shishib paydo bo'ladi.
```

---

# 834-Topshiriq: Aylanuvchi yuklanish qutisi (Cube Spin 3D)
## Topshiriq sharti:
rotateX va rotateY bo'yicha cheksiz aylanuvchi 3D kvadrat blok.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>3D Cube Spinner</title>
  <style>
    @keyframes spinCube {
      0%   { transform: rotateX(0deg) rotateY(0deg); }
      50%  { transform: rotateX(180deg) rotateY(0deg); }
      100% { transform: rotateX(180deg) rotateY(180deg); }
    }
    .cube-stage { perspective: 400px; width: fit-content; margin: 30px; }
    .cube-box {
      width: 40px;
      height: 40px;
      background: #6366f1;
      border-radius: 4px;
      animation: spinCube 2s infinite ease-in-out;
    }
  </style>
</head>
<body>
  <div class="cube-stage">
    <div class="cube-box"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
X va Y o'qlari bo'yicha navbatma-navbat 180 gradus aylanish zamonaviy minimalist loader yaratadi.

## Ishlash natijasi:
```text
Kichik binafsha kubik 3D fazoda to'xtovsiz aylanib turadi.
```

---

# 835-Topshiriq: Matn ustidagi ko'tariluvchi tabrik nishoni (Badge Bounce In)
## Topshiriq sharti:
Nishon osmondan tushib bir marta sakrab o'z joyiga qotib qolsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Badge Bounce In</title>
  <style>
    @keyframes bounceIn {
      0%   { transform: translateY(-100px); opacity: 0; }
      60%  { transform: translateY(15px); }
      80%  { transform: translateY(-5px); }
      100% { transform: translateY(0); opacity: 1; }
    }
    .badge {
      display: inline-block;
      background: #10b981;
      color: white;
      padding: 8px 16px;
      border-radius: 20px;
      font-family: sans-serif;
      font-weight: bold;
      animation: bounceIn 0.8s ease forwards;
    }
  </style>
</head>
<body>
  <div class="badge">&#10003; Muvaffaqiyatli!</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
60% va 80% da pastga-yuqoriga siljish tabiiy sakrash inersiyasini hosil qiladi.

## Ishlash natijasi:
```text
Yashil nishon tepadan tushib, polga urilib joyiga o'rnashadi.
```

---

# 836-Topshiriq: Aylanuvchi radar nuri (Radar Sweep)
## Topshiriq sharti:
Doira ichida radar nuri konus shaklida 360 gradusga aylanib tursin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Radar Sweep</title>
  <style>
    @keyframes radarSpin {
      from { transform: rotate(0deg); }
      to   { transform: rotate(360deg); }
    }
    .radar-screen {
      width: 70px;
      height: 70px;
      background: #064e3b;
      border: 2px solid #10b981;
      border-radius: 50%;
      position: relative;
      overflow: hidden;
    }
    .sweep {
      position: absolute;
      inset: 0;
      background: conic-gradient(from 0deg, rgba(16, 185, 129, 0.6) 0deg, transparent 60deg);
      animation: radarSpin 2s linear infinite;
    }
  </style>
</head>
<body>
  <div class="radar-screen">
    <div class="sweep"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`conic-gradient` yashil nurini 360 gradusga aylantirish harbiy va ilmiy radar ekranini beradi.

## Ishlash natijasi:
```text
To'q yashil dumaloq ekran ichida yashil nur aylanib skanerlaydi.
```

---

# 837-Topshiriq: Shrift qalinligining o'zgarishi animatsiyasi (Variable Font Weight Pulse)
## Topshiriq sharti:
Font-weight qiymati 300 dan 900 ga qarab davriy qalinlashsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Font Weight Pulse</title>
  <style>
    @keyframes weightShift {
      0%, 100% { font-variation-settings: 'wght' 300; letter-spacing: 0px; }
      50%      { font-variation-settings: 'wght' 900; letter-spacing: 2px; }
    }
    .variable-text {
      font-family: sans-serif;
      font-size: 28px;
      color: #1e293b;
      animation: weightShift 2s infinite ease-in-out;
    }
  </style>
</head>
<body>
  <div class="variable-text">DIQQAT</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Zamonaviy shriftlarda og'irlik va harflar oralig'ini animatsiya qilish yuqori darajadagi tipografika effektini beradi.

## Ishlash natijasi:
```text
'DIQQAT' so'zi ingichkadan o'ta qalin harflarga silliq o'tib turadi.
```

---

# 838-Topshiriq: Chiqib ketuvchi ro'yxat bandi (Slide Out Left)
## Topshiriq sharti:
Element chap tomonga translateX(-120%) bilan surilib yo'qolsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Slide Out Left</title>
  <style>
    @keyframes slideLeft {
      to { transform: translateX(-120%); opacity: 0; }
    }
    .del-item {
      width: 200px;
      padding: 10px;
      background: #fee2e2;
      border: 1px solid #f87171;
      border-radius: 4px;
      font-family: sans-serif;
      animation: slideLeft 0.5s ease 1s forwards;
    }
  </style>
</head>
<body>
  <div class="del-item">O'chirilgan band</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
1 soniya turgach, 0.5 soniyada chapga surilib yo'qoladi.

## Ishlash natijasi:
```text
Qizg'ish quti chapga qarab sirpanib yo'qolib ketadi.
```

---

# 839-Topshiriq: Doiraviy progress barning to'lib borishi (SVG Stroke Dasharray)
## Topshiriq sharti:
Doira chizig'i 0 dan 100% ga to'lib aylanuvchi progress hosil qiling.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Circle Stroke Fill</title>
  <style>
    @keyframes fillCircle {
      from { stroke-dashoffset: 283; }
      to   { stroke-dashoffset: 70; }
    }
    circle {
      stroke-dasharray: 283;
      stroke-dashoffset: 283;
      transform: rotate(-90deg);
      transform-origin: 50% 50%;
      animation: fillCircle 2s ease forwards;
    }
  </style>
</head>
<body>
  <svg width="100" height="100">
    <circle cx="50" cy="50" r="45" stroke="#e2e8f0" stroke-width="8" fill="none"/>
    <circle cx="50" cy="50" r="45" stroke="#2563eb" stroke-width="8" fill="none"/>
  </svg>
</body>
</html>
```

## Tushuntirish va Mantiq:
`stroke-dashoffset` qiymatini kamaytirish SVG doiraning chizig'ini soat yo'nalishida to'ldiradi.

## Ishlash natijasi:
```text
Oq halqa ustida ko'k chiziq 75% gacha silliq aylanib to'ladi.
```

---

# 840-Topshiriq: Xabarlar sonining sakrab yangilanishi (Badge Bounce Update)
## Topshiriq sharti:
Yangi xabar kelganda qizil badge bir marta shishib joyiga qaytsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Badge Update Bounce</title>
  <style>
    @keyframes badgeBounce {
      0%   { transform: scale(1); }
      50%  { transform: scale(1.6); }
      100% { transform: scale(1); }
    }
    .badge-pop {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 22px;
      height: 22px;
      background: #ef4444;
      color: white;
      border-radius: 50%;
      font-size: 11px;
      font-family: sans-serif;
      font-weight: bold;
      animation: badgeBounce 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
  </style>
</head>
<body>
  <div class="badge-pop">9</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Qizil raqamning `scale(1.6)` ga shishib qaytishi yangi xabar kelganini darhol bildiradi.

## Ishlash natijasi:
```text
Qizil dumaloq '9' nishoni birdaniga shishib o'z hajmiga qaytadi.
```

---

# 841-Topshiriq: Sekin miltillovchi xabardorlik nuqtasi (Beacon Blink)
## Topshiriq sharti:
Yashil nuqtaning xiralashib va ravshanlashib turishini opacity bilan quring.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Beacon Blink</title>
  <style>
    @keyframes blinkDot {
      0%, 100% { opacity: 0.2; }
      50%      { opacity: 1; }
    }
    .beacon {
      width: 12px;
      height: 12px;
      background: #10b981;
      border-radius: 50%;
      animation: blinkDot 1.2s infinite;
    }
  </style>
</head>
<body>
  <div class="beacon"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Yashil nuqtaning xiralashib-ravshanlashishi server holatini ifodalaydi.

## Ishlash natijasi:
```text
Yashil kichik chiroqcha mayin miltillab turadi.
```

---

# 842-Topshiriq: Pastki burchakdagi FAB tugmasining aylanib chiqishi
## Topshiriq sharti:
Tugma scale(0) rotate(-180deg) dan to'liq holatga aylanib chiqsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>FAB Spin In</title>
  <style>
    @keyframes fabIn {
      from { transform: scale(0) rotate(-180deg); opacity: 0; }
      to   { transform: scale(1) rotate(0deg); opacity: 1; }
    }
    .fab {
      width: 50px;
      height: 50px;
      background: #2563eb;
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      box-shadow: 0 4px 10px rgba(37,99,235,0.4);
      animation: fabIn 0.5s ease forwards;
    }
  </style>
</head>
<body>
  <div class="fab">&#43;</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Aylanib kattalashish tugmaga kirish vaqtida jo'shqinlik baxsh etadi.

## Ishlash natijasi:
```text
Ko'k dumaloq '+' tugmasi aylanib ekranga chiqadi.
```

---

# 843-Topshiriq: Gorizontal tebranuvchi navigatsiya kursor chizig'i
## Topshiriq sharti:
Aktiv menyu chizig'i ikki menyu orasida o'tib qaytib tursin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Nav Line Slide</title>
  <style>
    @keyframes slideBar {
      0%, 100% { transform: translateX(0); width: 60px; }
      50%      { transform: translateX(70px); width: 80px; }
    }
    .nav-track { position: relative; height: 30px; font-family: sans-serif; }
    .indicator {
      position: absolute;
      bottom: 0;
      height: 3px;
      background: #2563eb;
      border-radius: 2px;
      animation: slideBar 3s ease-in-out infinite;
    }
  </style>
</head>
<body>
  <div class="nav-track">
    <span>Darslar</span> &nbsp;&nbsp; <span>Loyiha</span>
    <div class="indicator"></div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
`translateX` va `width` birgalikda aktiv bo'limlar ostida chiziqning siljishini beradi.

## Ishlash natijasi:
```text
Ko'k chiziqcha so'zlar ostida u yoqdan bu yoqqa surilib turadi.
```

---

# 844-Topshiriq: Ekranga kirib keluvchi so'rov oynasi (Slide In Right)
## Topshiriq sharti:
O'ng tomondan translateX(100%) dan translateX(0) ga silliq kiruvchi darcha.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Slide In Right</title>
  <style>
    @keyframes slideRight {
      from { transform: translateX(100%); opacity: 0; }
      to   { transform: translateX(0); opacity: 1; }
    }
    .drawer {
      width: 220px;
      padding: 16px;
      background: #1e293b;
      color: white;
      border-radius: 8px;
      font-family: sans-serif;
      animation: slideRight 0.4s ease forwards;
    }
  </style>
</head>
<body>
  <div class="drawer">O'ngdan kirgan panel</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
O'ngdan kirish yon panellar (drawers) uchun eng tabiiy harakat hisoblanadi.

## Ishlash natijasi:
```text
Qora darcha o'ng tomondan silliq sirpanib chiqadi.
```

---

# 845-Topshiriq: Aylanuvchi uzuksiz gradient nuri (Border Glow Ring)
## Topshiriq sharti:
Dumaloq rasm atrofidagi gradient aylana to'xtovsiz aylanib tursin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Glow Ring</title>
  <style>
    @keyframes spinRing {
      to { transform: rotate(360deg); }
    }
    .ring-wrapper {
      position: relative;
      width: 60px;
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .glow-border {
      position: absolute;
      inset: 0;
      border-radius: 50%;
      background: linear-gradient(#f43f5e, #3b82f6);
      animation: spinRing 2s linear infinite;
    }
    .avatar-inner {
      position: relative;
      width: 52px;
      height: 52px;
      background: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: sans-serif;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="ring-wrapper">
    <div class="glow-border"></div>
    <div class="avatar-inner">AI</div>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Orqa qatlam aylanadi, ichki oq qatlam esa uni 4px li nozik aylanuvchi kamalak halqaga aylantiradi.

## Ishlash natijasi:
```text
'AI' doirasi atrofida aylanuvchi pushti-ko'k hoshiya.
```

---

# 846-Topshiriq: Quyi qatlamdan uchib chiquvchi konfeti nishoni
## Topshiriq sharti:
Nishon pastdan yuqoriga sakrab, so'ng sekin pastga tushsin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Confetti Pop</title>
  <style>
    @keyframes shootUp {
      0%   { transform: translateY(50px) scale(0.5); opacity: 0; }
      50%  { transform: translateY(-30px) scale(1.1); opacity: 1; }
      100% { transform: translateY(0) scale(1); opacity: 1; }
    }
    .star-pop {
      font-size: 32px;
      color: #f59e0b;
      display: inline-block;
      animation: shootUp 0.8s ease-out forwards;
    }
  </style>
</head>
<body>
  <div class="star-pop">&#10024;</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Pastdan yuqoriga otilib, biroz tushish konfeti yoki otashin hissiyotini beradi.

## Ishlash natijasi:
```text
Yulduzcha belgisi pastdan otilib chiqib joyiga tushadi.
```

---

# 847-Topshiriq: Aylanuvchi rangli disk (Color Wheel Spin)
## Topshiriq sharti:
Ranglar g'ildiragi to'xtovsiz silliq aylanib tursin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Color Wheel</title>
  <style>
    @keyframes spinWheel {
      to { transform: rotate(360deg); }
    }
    .wheel {
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background: conic-gradient(red, yellow, lime, aqua, blue, magenta, red);
      animation: spinWheel 3s linear infinite;
    }
  </style>
</head>
<body>
  <div class="wheel"></div>
</body>
</html>
```

## Tushuntirish va Mantiq:
To'liq spektrli conic-gradient aylanma harakatda toza ranglar g'ildiragini ko'rsatadi.

## Ishlash natijasi:
```text
Kamalakning barcha ranglari bilan uzluksiz aylanayotgan disk.
```

---

# 848-Topshiriq: Matn soyasining to'lqinlanishi (Shadow Wave)
## Topshiriq sharti:
Karta soyasi pastga va yuqoriga cho'zilib-qisqarib tursin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Shadow Wave</title>
  <style>
    @keyframes shadowPulse {
      0%, 100% { box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
      50%      { box-shadow: 0 16px 24px rgba(0,0,0,0.2); }
    }
    .shadow-box {
      width: 160px;
      padding: 16px;
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      text-align: center;
      font-family: sans-serif;
      animation: shadowPulse 2s infinite ease-in-out;
    }
  </style>
</head>
<body>
  <div class="shadow-box">Soya To'lqini</div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Obyekt qimirlamaydi, faqat uning soyasi chuqurlashadi va yengillashadi.

## Ishlash natijasi:
```text
Oq qutining ostidagi soya kuchayib va xiralashib turadi.
```

---

# 849-Topshiriq: Aylanuvchi vites/shesteronka (Gear Rotation)
## Topshiriq sharti:
Ikkita shesteronka bir-biriga qarama-qarshi yo'nalishda aylansin.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Gears Rotation</title>
  <style>
    @keyframes spinClockwise { to { transform: rotate(360deg); } }
    @keyframes spinCounter { to { transform: rotate(-360deg); } }
    .gears { display: flex; font-size: 32px; gap: 4px; color: #475569; }
    .g1 { display: inline-block; animation: spinClockwise 3s linear infinite; }
    .g2 { display: inline-block; animation: spinCounter 3s linear infinite; }
  </style>
</head>
<body>
  <div class="gears">
    <span class="g1">&#9881;</span>
    <span class="g2">&#9881;</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Biri soat yo'nalishida, ikkinchisi esa teskari yo'nalishda aylanib mexanizm hosil qiladi.

## Ishlash natijasi:
```text
Ikkita tishli g'ildirak o'zaro tutashib qarama-qarshi aylanadi.
```

---

# 850-Topshiriq: To'liq Interaktiv Yuklanish va Muvaffaqiyat Ekrani (Loader to Success)
## Topshiriq sharti:
Avval aylanuvchi spinner ko'rinib, 2 soniyadan so'ng silliq yashil qushchaga aylanuvchi to'liq animatsiya.

## Yechim (HTML va CSS kodi):
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Loader to Success Animation</title>
  <style>
    @keyframes spinState {
      0%   { transform: rotate(0deg); border-color: #cbd5e1; border-top-color: #2563eb; }
      70%  { transform: rotate(720deg); border-color: #cbd5e1; border-top-color: #2563eb; }
      100% { transform: rotate(720deg); border-color: #10b981; background: #10b981; }
    }
    @keyframes checkAppear {
      0%, 75% { opacity: 0; transform: scale(0); }
      100%    { opacity: 1; transform: scale(1); }
    }
    .status-circle {
      width: 48px;
      height: 48px;
      border: 4px solid #cbd5e1;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      animation: spinState 2.5s ease forwards;
      color: white;
      font-size: 24px;
      font-weight: bold;
    }
    .check-mark {
      animation: checkAppear 2.5s ease forwards;
    }
  </style>
</head>
<body>
  <div class="status-circle">
    <span class="check-mark">&#10003;</span>
  </div>
</body>
</html>
```

## Tushuntirish va Mantiq:
Animatsiya birinchi bosqichda 720 gradusga aylanib yuklanishni ko'rsatadi, so'ng `border-color` yashil bo'lib, ichidan oq qushcha chiqib keladi.

## Ishlash natijasi:
```text
Aylanayotgan ko'k halqa to'xtab, yashil tasdiqlangan qushchaga aylanadi.
```

---

