# Khorazmiy AI: HTML & CSS - Modul 24
## Mavzu: Kiberxavfsizlik, Kriptografiya (AES, RSA, ECC) va Xavfsiz Kodlash

### Topshiriq #1151: Xavfsiz parol kiritish maydoni (Masking)
**Tavsif:** Foydalanuvchi parolini kiritayotganda "ko'z" ikonkasi orqali uni ko'rish yoki yashirish funksiyasi.
**Talablar:** `input type="password"` dan foydalanish, `aria-label` orqali foydalanish imkoniyatini ta'minlash.
**Yechim (HTML & CSS):**
```html
<div class="password-container">
  <input type="password" id="pwd" placeholder="Parolni kiriting">
  <button onclick="togglePwd()" aria-label="Parolni ko'rsatish">👁️</button>
</div>
<style>
  .password-container { display: flex; gap: 5px; }
  input { padding: 8px; border: 1px solid #ccc; }
</style>
```
**Tushuntirish:** `type="password"` brauzer darajasida ma'lumotni maskalashni ta'minlaydi, bu esa "shoulder surfing" (yelkadan qarash) hujumlaridan himoya qiladi.

### Topshiriq #1152: Kriptografik kalitlarni vizualizatsiya qilish (ECC)
**Tavsif:** ECC (Elliptic Curve Cryptography) kalitlarini xavfsiz saqlash uchun UI komponenti.
**Talablar:** Kalitni nusxalashni cheklash (`user-select: none`), faqat bosilganda ko'rsatish.
**Yechim (HTML & CSS):**
```html
<div class="key-box" onclick="this.classList.toggle('visible')">
  <span>ECC Kaliti:</span>
  <code class="key-value">-----BEGIN EC PRIVATE KEY-----...</code>
</div>
<style>
  .key-value { user-select: none; filter: blur(5px); cursor: pointer; }
  .key-box.visible .key-value { filter: none; }
</style>
```
**Tushuntirish:** `filter: blur` va `user-select: none` xususiyatlari tasodifiy skrinshotlar yoki ekran yozuvlari orqali kalit o'g'irlanishini qiyinlashtiradi.

### Topshiriq #1153: Xavfsiz shakl yuborish (CSRF himoyasi)
**Tavsif:** Shakl yuborilganda foydalanuvchini ogohlantiruvchi vizual indikator.
**Talablar:** `pointer-events` orqali shaklni bir marta yuborishga majburlash.
**Yechim (HTML & CSS):**
```html
<form id="secureForm" onsubmit="this.style.pointerEvents='none'">
  <input type="hidden" name="csrf_token" value="xyz123">
  <button type="submit">Tranzaksiyani tasdiqlash</button>
</form>
```
**Tushuntirish:** `pointer-events: none` yuborish jarayonida foydalanuvchining qayta bosishini (double-submit) oldini oladi, bu esa tranzaksiya xavfsizligini oshiradi.

### Topshiriq #1154: AES shifrlash holati indikatori
**Tavsif:** Ma'lumotlar AES-256 bilan shifrlanganligini ko'rsatuvchi xavfsizlik belgisi.
**Talablar:** CSS `::before` psevdo-elementi yordamida qulf ikonkasini qo'shish.
**Yechim (HTML & CSS):**
```html
<div class="encrypted-status">Ma'lumot AES-256 bilan himoyalangan</div>
<style>
  .encrypted-status::before { content: "🔒 "; color: green; }
</style>
```
**Tushuntirish:** Vizual ishonch (Trust UI) foydalanuvchiga ma'lumotlar xavfsiz kanallar orqali uzatilayotganini anglatadi.

### Topshiriq #1155: Xavfsiz kod bloki (Code Obfuscation)
**Tavsif:** Kodni ko'chirib olishni qiyinlashtiruvchi qatlam.
**Talablar:** `contextmenu` ni o'chirish va matn tanlashni bloklash.
**Yechim (HTML & CSS):**
```html
<pre oncontextmenu="return false;" style="user-select: none;">
  // Kriptografik funksiya
  function encrypt(data) { ... }
</pre>
```
**Tushuntirish:** `user-select: none` va `oncontextmenu="return false"` foydalanuvchining kodni osonlikcha nusxalab olishiga to'sqinlik qiladi.

### Topshiriq #1156: RSA kalit uzunligi tekshiruvi
**Tavsif:** Foydalanuvchi kiritgan RSA kalit uzunligini vizual baholash.
**Talablar:** 2048 bitdan kam bo'lsa qizil, ko'p bo'lsa yashil rang.
**Yechim (HTML & CSS):**
```html
<input type="number" oninput="check(this.value)">
<div id="status"></div>
<style>
  .weak { color: red; } .strong { color: green; }
</style>
```
**Tushuntirish:** Dinamik UI orqali foydalanuvchini xavfsizroq kalit uzunligini tanlashga undash (UX/Security).

### Topshiriq #1157: Xavfsiz yuklash (Loading) animatsiyasi
**Tavsif:** Kriptografik operatsiyalar bajarilayotganda foydalanuvchini kutishga majburlash.
**Talablar:** `z-index` orqali butun ekran ustidan qatlam hosil qilish.
**Yechim (HTML & CSS):**
```html
<div class="overlay">Shifrlanmoqda...</div>
<style>
  .overlay { position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.8); z-index: 999; }
</style>
```
**Tushuntirish:** Operatsiya tugaguniga qadar UI bloklanishi ma'lumotlar yaxlitligini (data integrity) ta'minlaydi.

### Topshiriq #1158: Xavfsizlik siyosati (CSP) xabarnomasi
**Tavsif:** Brauzerda CSP xatosi yuz berganda ko'rinadigan ogohlantirish.
**Talablar:** `display: none` dan `block` ga o'tish.
**Yechim (HTML & CSS):**
```html
<div id="csp-alert" style="display:none; background: yellow;">Xavfsizlik siyosati buzildi!</div>
<style>
  #csp-alert { border: 2px solid red; padding: 10px; }
</style>
```
**Tushuntirish:** CSP (Content Security Policy) xatolarini foydalanuvchiga bildirish, xakerlik urinishlarini aniqlashga yordam beradi.

### Topshiriq #1159: Kripto-hamyon manzilini xavfsiz ko'rsatish
**Tavsif:** Manzilni qisman yashirish (truncation).
**Talablar:** CSS `text-overflow: ellipsis` dan foydalanish.
**Yechim (HTML & CSS):**
```html
<div style="width: 100px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
  0x71C7656...89A
</div>
```
**Tushuntirish:** To'liq kalitni ko'rsatmaslik, tasodifiy oshkor bo'lish xavfini kamaytiradi.

### Topshiriq #1160: Xavfsiz "Logout" tugmasi
**Tavsif:** Sessiyani tugatish uchun tasdiqlovchi oyna.
**Talablar:** `dialog` elementidan foydalanish.
**Yechim (HTML & CSS):**
```html
<dialog id="logoutModal">
  <p>Haqiqatan ham chiqmoqchimisiz?</p>
  <button onclick="logout()">Ha</button>
</dialog>
<button onclick="document.getElementById('logoutModal').showModal()">Chiqish</button>
```
**Tushuntirish:** `dialog` elementi sessiyani xavfsiz yopish uchun standart va xavfsiz UI komponenti hisoblanadi.

---

### Topshiriq #1161: Xavfsiz parol kiritish maydoni (Masking & Visibility)
**Tavsif:** Foydalanuvchi parolini kiritayotganda "ko'z" belgisi orqali parolni ko'rish/yashirish funksiyasi.
**Talablar:** `input type="password"` atributini dinamik o'zgartirish, foydalanuvchi tajribasi (UX) va vizual xavfsizlik.
**Yechim (HTML & CSS):**
```html
<div class="password-container">
  <input type="password" id="pwd" placeholder="Parolni kiriting">
  <span class="toggle-btn" onclick="togglePwd()">👁️</span>
</div>
<style>
  .password-container { position: relative; width: 300px; }
  input { width: 100%; padding: 10px; border: 1px solid #ccc; }
  .toggle-btn { position: absolute; right: 10px; top: 10px; cursor: pointer; }
</style>
<script>
  function togglePwd() {
    let x = document.getElementById("pwd");
    x.type = (x.type === "password") ? "text" : "password";
  }
</script>
```
**Tushuntirish:** `type` atributini almashtirish orqali DOM darajasida xavfsizlikni ta'minlash. CSS `position: absolute` yordamida elementni input ichiga joylashtirish eng samarali usul.

---

### Topshiriq #1162: RSA kalitlarini vizualizatsiya qilish paneli
**Tavsif:** RSA algoritmi uchun ochiq (Public) va yopiq (Private) kalitlarni xavfsiz ko'rsatish interfeysi.
**Talablar:** Kalitlarni nusxalashdan himoya qilish (user-select: none) va vizual ajratish.
**Yechim (HTML & CSS):**
```html
<div class="key-box">
  <h3>RSA Public Key</h3>
  <code class="secure-text">-----BEGIN PUBLIC KEY----- MIIBIjANBgkqhkiG...</code>
</div>
<style>
  .secure-text { user-select: none; background: #f4f4f4; padding: 10px; display: block; }
  .key-box { border-left: 5px solid #d9534f; padding: 10px; }
</style>
```
**Tushuntirish:** `user-select: none` xususiyati foydalanuvchining tasodifiy nusxalashini cheklaydi, bu esa xavfsizlikni oshiradi.

---

### Topshiriq #1163: AES shifrlash holati indikatori
**Tavsif:** Ma'lumotlar AES-256 bilan shifrlanganligini bildiruvchi vizual status paneli.
**Talablar:** Rangli kodlash (yashil - shifrlangan, qizil - shifrlanmagan).
**Yechim (HTML & CSS):**
```html
<div class="status-bar encrypted">AES-256 Shifrlash Faol</div>
<style>
  .status-bar { padding: 10px; color: white; font-weight: bold; }
  .encrypted { background-color: #28a745; border-radius: 4px; }
</style>
```
**Tushuntirish:** Vizual indikatorlar foydalanuvchini tizim holati haqida xabardor qiladi, bu "Security Awareness" uchun muhim.

---

### Topshiriq #1164: ECC (Elliptic Curve) imzo tasdiqlash tugmasi
**Tavsif:** ECC raqamli imzosini tekshirish jarayoni uchun "Tekshirish" tugmasi dizayni.
**Talablar:** Tugma bosilganda yuklanish holati (Loading state) va xavfsizlik animatsiyasi.
**Yechim (HTML & CSS):**
```html
<button class="verify-btn">Imzoni tekshirish</button>
<style>
  .verify-btn { background: #007bff; color: white; border: none; padding: 10px 20px; cursor: pointer; transition: 0.3s; }
  .verify-btn:hover { background: #0056b3; box-shadow: 0 0 10px rgba(0,123,255,0.5); }
</style>
```
**Tushuntirish:** Hover effekti va box-shadow foydalanuvchiga interaktivlikni bildiradi, bu esa xatolarni kamaytiradi.

---

### Topshiriq #1165: Xavfsiz kod bloki (Code Snippet Masking)
**Tavsif:** Maxfiy kod qismlarini (API key yoki token) yashirib turuvchi UI komponenti.
**Talablar:** `blur` effekti orqali ma'lumotni yashirish.
**Yechim (HTML & CSS):**
```html
<div class="secret-code">API_KEY: sk_live_51Mz...</div>
<style>
  .secret-code { filter: blur(4px); cursor: pointer; transition: 0.5s; }
  .secret-code:hover { filter: blur(0px); }
</style>
```
**Tushuntirish:** CSS `filter: blur` xususiyati ekranda tasodifiy ko'rinishlarning oldini olish uchun eng yaxshi yechimdir.

---

### Topshiriq #1166: Kriptografik xeshlash (Hash) natijasi paneli
**Tavsif:** SHA-256 xesh qiymatlarini ko'rsatish uchun maxsus blok.
**Talablar:** Monospaced shrift va o'zgarmas kenglik.
**Yechim (HTML & CSS):**
```html
<div class="hash-display">e3b0c44298fc1c149afbf4c8996fb924...</div>
<style>
  .hash-display { font-family: 'Courier New', monospace; background: #222; color: #0f0; padding: 15px; overflow-x: auto; }
</style>
```
**Tushuntirish:** Monospaced shriftlar xesh qiymatlarini o'qishni osonlashtiradi va xatolarni kamaytiradi.

---

### Topshiriq #1167: Xavfsiz forma yuborish (Submit) himoyasi
**Tavsif:** Forma yuborilganda ikki marta bosishni oldini olish uchun tugmani o'chirish (Disable).
**Talablar:** `disabled` holati uchun CSS stilizatsiyasi.
**Yechim (HTML & CSS):**
```html
<button id="sub" onclick="this.disabled=true; this.innerText='Yuborilmoqda...'">Yuborish</button>
<style>
  button:disabled { background: #ccc; cursor: not-allowed; }
</style>
```
**Tushuntirish:** `disabled` atributi serverga ortiqcha so'rovlar yuborilishining oldini oladi (Rate limiting).

---

### Topshiriq #1168: Kiberxavfsizlik ogohlantirish oynasi (Modal)
**Tavsif:** Foydalanuvchiga xavfsizlik tahdidi haqida ogohlantirish beruvchi modal oyna.
**Talablar:** `z-index` yordamida barcha elementlardan ustun turish.
**Yechim (HTML & CSS):**
```html
<div class="modal">Diqqat: Xavfsiz ulanish uzildi!</div>
<style>
  .modal { position: fixed; top: 0; width: 100%; background: red; color: white; text-align: center; z-index: 9999; }
</style>
```
**Tushuntirish:** `z-index: 9999` ogohlantirishning har doim ko'rinib turishini ta'minlaydi.

---

### Topshiriq #1169: Parol kuchi (Strength) indikatori
**Tavsif:** Parol murakkabligini vizual baholash (Progress bar).
**Talablar:** Parol uzunligiga qarab rangni o'zgartirish.
**Yechim (HTML & CSS):**
```html
<div class="meter"><div id="bar" style="width: 30%; background: red;"></div></div>
<style>
  .meter { width: 100%; height: 10px; background: #eee; }
  #bar { height: 100%; transition: 0.3s; }
</style>
```
**Tushuntirish:** Vizual progress bar foydalanuvchini kuchliroq parol yaratishga undaydi.

---

### Topshiriq #1170: Xavfsiz sessiya taymeri
**Tavsif:** Sessiya tugashiga qolgan vaqtni ko'rsatuvchi taymer.
**Talablar:** Foydalanuvchini sessiya tugashi haqida ogohlantirish.
**Yechim (HTML & CSS):**
```html
<div class="timer">Sessiya tugashiga: <span id="time">05:00</span></div>
<style>
  .timer { font-family: sans-serif; color: #d9534f; font-weight: bold; }
</style>
```
**Tushuntirish:** Sessiya vaqti tugashini ko'rsatish foydalanuvchi ma'lumotlarini xavfsiz saqlashga yordam beradi.

---

### Topshiriq #1171: Xavfsiz parol kiritish maydoni (Password Masking)
**Tavsif:** Foydalanuvchi parolini kiritayotganda "ko'z" belgisi orqali uni ko'rish yoki yashirish funksiyasi.
**Talablar:** `type="password"` atributini dinamik o'zgartirish, CSS orqali vizual indikatsiya.
**Yechim (HTML & CSS):**
```html
<div class="password-container">
  <input type="password" id="pwd" placeholder="Parolni kiriting">
  <span onclick="togglePwd()" style="cursor:pointer">👁️</span>
</div>
<style>
  .password-container { display: flex; align-items: center; gap: 10px; }
  input { padding: 8px; border: 1px solid #ccc; }
</style>
<script>
  function togglePwd() {
    let x = document.getElementById("pwd");
    x.type = (x.type === "password") ? "text" : "password";
  }
</script>
```
**Tushuntirish:** `type` atributini almashtirish orqali brauzer xotirasida parolning ochiq matn sifatida saqlanishini minimallashtiramiz.

### Topshiriq #1172: XSS hujumidan himoyalangan foydalanuvchi profili
**Tavsif:** Foydalanuvchi kiritgan ma'lumotni sahifada aks ettirishda XSS (Cross-Site Scripting) oldini olish.
**Talablar:** `textContent` dan foydalanish, `innerHTML` dan qochish.
**Yechim (HTML & CSS):**
```html
<div id="user-display" class="secure-box"></div>
<style>.secure-box { background: #f4f4f4; padding: 10px; border-radius: 5px; }</style>
<script>
  const userInput = "<script>alert('XSS')<\/script>"; // Xavfli input
  const display = document.getElementById('user-display');
  display.textContent = userInput; // Xavfsiz usul: kod sifatida emas, matn sifatida render qiladi
</script>
```
**Tushuntirish:** `textContent` brauzerga kiritilgan ma'lumotni HTML kodi sifatida emas, oddiy matn sifatida qabul qilishni buyuradi.

### Topshiriq #1173: Kriptografik kalitlarni vizuallashtirish paneli
**Tavsif:** AES kalitlari uzunligini (128/256 bit) tanlash uchun xavfsiz UI komponenti.
**Talablar:** Tanlangan kalit uzunligiga qarab vizual ogohlantirish.
**Yechim (HTML & CSS):**
```html
<select id="aes-key" onchange="checkSecurity()">
  <option value="128">AES-128</option>
  <option value="256">AES-256 (Tavsiya etiladi)</option>
</select>
<div id="status"></div>
<script>
  function checkSecurity() {
    const val = document.getElementById('aes-key').value;
    document.getElementById('status').innerText = val === '256' ? "Yuqori xavfsizlik" : "O'rta xavfsizlik";
  }
</script>
```
**Tushuntirish:** Foydalanuvchini yuqori standartli kriptografiyaga yo'naltirish orqali tizim xavfsizligini oshirish.

### Topshiriq #1174: CSRF tokenlari uchun yashirin maydonlar
**Tavsif:** Formani yuborishda CSRF (Cross-Site Request Forgery) hujumlarini oldini olish uchun yashirin token maydoni.
**Talablar:** `type="hidden"` atributidan foydalanish.
**Yechim (HTML & CSS):**
```html
<form action="/api/submit" method="POST">
  <input type="hidden" name="csrf_token" value="a7b8c9d0e1f2g3h4i5j6">
  <input type="text" name="data" required>
  <button type="submit">Yuborish</button>
</form>
```
**Tushuntirish:** Yashirin token server tomonidan tekshiriladi, bu esa ruxsatsiz so'rovlarni bloklaydi.

### Topshiriq #1175: RSA kalit juftligini generatsiya qilish interfeysi
**Tavsif:** RSA kalitlarini yaratish jarayonini kuzatish uchun progress bar.
**Talablar:** CSS animatsiyasi bilan yuklanish holatini ko'rsatish.
**Yechim (HTML & CSS):**
```html
<div class="progress-bar"><div class="fill"></div></div>
<style>
  .progress-bar { width: 100%; height: 20px; background: #eee; }
  .fill { width: 70%; height: 100%; background: #4CAF50; transition: width 2s; }
</style>
```
**Tushuntirish:** Kriptografik operatsiyalar vaqt talab qiladi, shuning uchun foydalanuvchiga jarayon holatini vizual ko'rsatish muhim.

### Topshiriq #1176: ECC (Elliptic Curve Cryptography) parametrlarini tanlash
**Tavsif:** ECC egri chiziqlarini tanlash uchun xavfsiz tanlov menyusi.
**Talablar:** Har bir variant uchun qisqacha xavfsizlik izohi.
**Yechim (HTML & CSS):**
```html
<fieldset>
  <legend>ECC Egri chizig'ini tanlang</legend>
  <label><input type="radio" name="curve" value="secp256k1"> secp256k1 (Bitcoin)</label>
  <label><input type="radio" name="curve" value="ed25519"> ed25519 (Zamonaviy)</label>
</fieldset>
```
**Tushuntirish:** Foydalanuvchiga tanlov imkoniyatini berishda standartlashtirilgan nomlardan foydalanish xatolikni kamaytiradi.

### Topshiriq #1177: Xavfsiz kodlash uchun "Content Security Policy" (CSP) meta-tegi
**Tavsif:** Tashqi skriptlar yuklanishini cheklash uchun HTML meta-tegi.
**Talablar:** `Content-Security-Policy` sarlavhasini HTML orqali simulyatsiya qilish.
**Yechim (HTML & CSS):**
```html
<head>
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' https://trusted.cdn.com;">
</head>
```
**Tushuntirish:** Bu brauzerga faqat o'z domenimizdan yoki ishonchli manbalardan skript yuklashni buyuradi, bu esa zararli kodlarni bloklaydi.

### Topshiriq #1178: Parol kuchi indikatori (Entropy Meter)
**Tavsif:** Foydalanuvchi kiritayotgan parolning murakkabligini vizual baholash.
**Talablar:** CSS ranglari orqali (qizil-sariq-yashil) kuchni ko'rsatish.
**Yechim (HTML & CSS):**
```html
<input type="password" oninput="checkStrength(this.value)">
<div id="strength-bar" style="height:5px; width:0;"></div>
<script>
  function checkStrength(val) {
    const bar = document.getElementById('strength-bar');
    bar.style.width = (val.length * 10) + "%";
    bar.style.backgroundColor = val.length > 8 ? "green" : "red";
  }
</script>
```
**Tushuntirish:** Foydalanuvchini kuchliroq parol yaratishga undash orqali "Brute-force" hujumlaridan himoya qilamiz.

### Topshiriq #1179: Xavfsiz "Logout" tugmasi
**Tavsif:** Sessiyani tugatish va keshni tozalashni eslatuvchi xavfsizlik tugmasi.
**Talablar:** `onclick` hodisasi bilan sessiyani yo'q qilish.
**Yechim (HTML & CSS):**
```html
<button class="logout-btn" onclick="sessionStorage.clear(); window.location.href='/login';">
  Tizimdan chiqish
</button>
<style>.logout-btn { background: #d9534f; color: white; border: none; padding: 10px; }</style>
```
**Tushuntirish:** `sessionStorage` ni tozalash orqali foydalanuvchi ma'lumotlari brauzer yopilganda ham xavfsiz qolishini ta'minlaymiz.

### Topshiriq #1180: Ma'lumotlarni shifrlash uchun "Data-Attribute" himoyasi
**Tavsif:** HTML elementlarida sezgir ma'lumotlarni saqlashda `data-*` atributlarini shifrlangan holda saqlash.
**Talablar:** Base64 yoki shifrlangan kodni atributda saqlash.
**Yechim (HTML & CSS):**
```html
<div id="user-data" data-secret="U2VjcmV0X0RhdGFfMTIz">Foydalanuvchi profili</div>
<script>
  const secret = document.getElementById('user-data').dataset.secret;
  console.log("Shifrlangan ma'lumot:", secret);
</script>
```
**Tushuntirish:** HTML kodida ochiq matn o'rniga kodlangan ma'lumotlarni saqlash, tasodifiy ko'z tushishidan himoya qiladi.

---

### Topshiriq #1181: Xavfsiz parol kiritish maydoni (Password Masking)
**Tavsif:** Foydalanuvchi parolini kiritayotganda "ko'z" ikonkasi orqali uni ko'rish yoki yashirish funksiyasini xavfsiz amalga oshirish.
**Talablar:** `input type="password"` atributini dinamik o'zgartirish va foydalanuvchi tajribasini (UX) buzmaslik.
**Yechim (HTML & CSS):**
```html
<div class="password-container">
  <input type="password" id="pwd" placeholder="Parolni kiriting">
  <span onclick="togglePwd()" style="cursor:pointer">👁️</span>
</div>
<style>
  .password-container { display: flex; align-items: center; gap: 10px; }
  input { padding: 8px; border: 1px solid #ccc; }
</style>
<script>
  function togglePwd() {
    let x = document.getElementById("pwd");
    x.type = (x.type === "password") ? "text" : "password";
  }
</script>
```
**Tushuntirish:** `type` atributini almashtirish orqali brauzerning standart xavfsizlik funksiyalaridan foydalanildi.

### Topshiriq #1182: Kriptografik kalitlar uchun "Copy-to-Clipboard" xavfsizligi
**Tavsif:** AES kalitlarini nusxalashda clipboard tarixida qolib ketmasligi uchun vaqtinchalik xabarnoma ko'rsatish.
**Talablar:** `navigator.clipboard` API dan foydalanish va foydalanuvchini ogohlantirish.
**Yechim (HTML & CSS):**
```html
<code id="key">AES-256-KEY-X-9982</code>
<button onclick="copyKey()">Kalitni nusxalash</button>
<style>
  code { background: #eee; padding: 5px; border-radius: 4px; }
</style>
<script>
  function copyKey() {
    navigator.clipboard.writeText(document.getElementById('key').innerText);
    alert("Kalit nusxalandi! Xavfsizlik uchun uni xavfsiz joyda saqlang.");
  }
</script>
```
**Tushuntirish:** Clipboard API zamonaviy brauzerlarda xavfsizroq va `execCommand`dan ustunroq.

### Topshiriq #1183: RSA kalit juftligini vizualizatsiya qilish
**Tavsif:** RSA algoritmi uchun ochiq (public) va yopiq (private) kalitlarni vizual ajratib ko'rsatish.
**Talablar:** CSS Grid yordamida kalitlarni bloklarga ajratish va vizual iyerarxiya yaratish.
**Yechim (HTML & CSS):**
```html
<div class="rsa-box">
  <div class="public">Ochiq kalit: 0xAF...</div>
  <div class="private">Yopiq kalit: 0xBC... (Maxfiy!)</div>
</div>
<style>
  .rsa-box { display: grid; gap: 10px; }
  .public { border-left: 5px solid green; padding: 10px; }
  .private { border-left: 5px solid red; padding: 10px; }
</style>
```
**Tushuntirish:** Vizual ranglar (yashil/qizil) foydalanuvchiga kalitning darajasini tez anglash imkonini beradi.

### Topshiriq #1184: ECC (Elliptic Curve) parametrlarini himoyalash
**Tavsif:** ECC egri chiziq parametrlarini (a, b, p) foydalanuvchi tasodifan o'zgartirmasligi uchun `readonly` maydonlar yaratish.
**Talablar:** CSS orqali `readonly` maydonlarni stilizatsiya qilish.
**Yechim (HTML & CSS):**
```html
<input type="text" value="Curve25519" readonly class="secure-input">
<style>
  .secure-input { background: #f0f0f0; border: 1px solid #999; cursor: not-allowed; }
</style>
```
**Tushuntirish:** `readonly` atributi va `not-allowed` kursor xavfsizlik parametrlarini o'zgartirib bo'lmasligini bildiradi.

### Topshiriq #1185: Xavfsiz kodlash: XSS (Cross-Site Scripting) oldini olish
**Tavsif:** Foydalanuvchi kiritgan ma'lumotni ekranga chiqarishda HTML teglarni tozalash (sanitization).
**Talablar:** `textContent` dan foydalanish (innerHTML o'rniga).
**Yechim (HTML & CSS):**
```html
<div id="display"></div>
<script>
  const userInput = "<script>alert('XSS')<\/script>";
  document.getElementById('display').textContent = userInput; 
</script>
```
**Tushuntirish:** `textContent` brauzerga ma'lumotni kod sifatida emas, oddiy matn sifatida qabul qilishni buyuradi.

### Topshiriq #1186: Kriptografik xeshlash vizual indikatori
**Tavsif:** Parol kuchini (SHA-256) vizual ko'rsatuvchi progress bar.
**Talablar:** Parol uzunligiga qarab rangni o'zgartirish (CSS variables).
**Yechim (HTML & CSS):**
```html
<div id="bar" style="width: 0%; height: 10px; background: red;"></div>
<input type="password" oninput="check(this.value)">
<script>
  function check(v) {
    let w = v.length * 10;
    document.getElementById('bar').style.width = w + "%";
  }
</script>
```
**Tushuntirish:** Dinamik CSS o'zgarishlari foydalanuvchiga parolni kuchaytirish zarurligini real vaqtda ko'rsatadi.

### Topshiriq #1187: Xavfsiz sessiya tugashi (Session Timeout)
**Tavsif:** Foydalanuvchi faol bo'lmaganda sessiyani avtomatik yopish haqida ogohlantirish.
**Talablar:** CSS `opacity` animatsiyasi bilan ogohlantirish oynasini ko'rsatish.
**Yechim (HTML & CSS):**
```html
<div id="modal" class="hidden">Sessiya tugashiga 1 daqiqa qoldi!</div>
<style>
  .hidden { display: none; opacity: 0; transition: 0.5s; }
</style>
```
**Tushuntirish:** CSS transition foydalanuvchini bezovta qilmaydigan yumshoq ogohlantirishni ta'minlaydi.

### Topshiriq #1188: Kriptografik imzo (Digital Signature) maydoni
**Tavsif:** Raqamli imzo uchun maxsus `textarea` maydoni.
**Talablar:** `resize: none` orqali maydon o'lchamini qotirish.
**Yechim (HTML & CSS):**
```html
<textarea style="resize: none; width: 300px; height: 100px;" placeholder="Imzo kalitini kiriting"></textarea>
```
**Tushuntirish:** `resize: none` UI barqarorligini va xavfsizlik maydonining o'zgarmasligini ta'minlaydi.

### Topshiriq #1189: Xavfsiz kodlash: CSRF tokeni uchun yashirin maydon
**Tavsif:** Formani yuborishda CSRF tokenini yashirin tarzda uzatish.
**Talablar:** `type="hidden"` atributidan foydalanish.
**Yechim (HTML & CSS):**
```html
<form action="/submit" method="POST">
  <input type="hidden" name="csrf_token" value="a7b8c9d0e1f2g3h4">
  <button type="submit">Yuborish</button>
</form>
```
**Tushuntirish:** Yashirin maydonlar server tomonlama xavfsizlikni tekshirish uchun zarur bo'lgan tokenlarni uzatadi.

### Topshiriq #1190: Kriptografik xatoliklar xabarnomasi
**Tavsif:** Kriptografik xatolarni foydalanuvchiga tushunarli, lekin xavfsiz (texnik tafsilotlarsiz) yetkazish.
**Talablar:** CSS orqali xatolik xabarlarini markazlashtirish va ajratib ko'rsatish.
**Yechim (HTML & CSS):**
```html
<div class="error-box">Xatolik: Kalit noto'g'ri formatda.</div>
<style>
  .error-box { color: white; background: #d9534f; padding: 15px; border-radius: 5px; text-align: center; }
</style>
```
**Tushuntirish:** Xatolik xabari foydalanuvchini ogohlantiradi, lekin tizimning ichki tuzilishi haqida ma'lumot bermaydi (Security through obscurity).

---

### Topshiriq #1191: Xavfsiz parol kiritish maydoni (Password Masking)
**Tavsif:** Foydalanuvchi parolni kiritayotganda "ko'rish" tugmasi orqali uni tekshirish imkonini beruvchi, ammo kiberhujumlardan himoyalangan UI komponenti.
**Talablar:** `type="password"` atributini dinamik o'zgartirish va vizual indikatorlar bilan ta'minlash.
**Yechim (HTML & CSS):**
```html
<div class="password-container">
  <input type="password" id="pwd" placeholder="Parolni kiriting">
  <button onclick="togglePwd()">👁️</button>
</div>
<style>
  .password-container { display: flex; gap: 5px; }
  input { border: 1px solid #ccc; padding: 8px; }
</style>
<script>
  function togglePwd() {
    const x = document.getElementById("pwd");
    x.type = (x.type === "password") ? "text" : "password";
  }
</script>
```
**Tushuntirish:** `type` atributini almashtirish orqali brauzerning avtomatik to'ldirish funksiyalari bilan moslik saqlanadi.

### Topshiriq #1192: Xavfsiz ma'lumot uzatish uchun "HoneyPot" maydoni
**Tavsif:** Botlar tomonidan amalga oshiriladigan avtomatik formani to'ldirish hujumlarini oldini olish uchun yashirin maydon.
**Talablar:** CSS orqali maydonni foydalanuvchidan yashirish, lekin botlar uchun ko'rinadigan qilish.
**Yechim (HTML & CSS):**
```html
<form>
  <div class="hidden-field">
    <input type="text" name="website_url" tabindex="-1" autocomplete="off">
  </div>
  <input type="submit" value="Yuborish">
</form>
<style>
  .hidden-field { position: absolute; left: -9999px; }
</style>
```
**Tushuntirish:** Botlar barcha maydonlarni to'ldirishga harakat qiladi. Agar `website_url` to'ldirilgan bo'lsa, so'rov rad etiladi.

### Topshiriq #1193: Kriptografik kalitlar uchun "Read-Only" displey
**Tavsif:** RSA yoki AES kalitlarini foydalanuvchiga ko'rsatishda ularni tasodifiy o'zgartirishdan himoya qilish.
**Talablar:** `readonly` atributi va matnni tanlashni cheklash.
**Yechim (HTML & CSS):**
```html
<textarea readonly class="key-display">AES-256-GCM-KEY-X92837465</textarea>
<style>
  .key-display { user-select: none; background: #f4f4f4; border: none; width: 100%; }
</style>
```
**Tushuntirish:** `user-select: none` matnni nusxalashni qiyinlashtiradi (xavfsizlik qatlami), `readonly` esa o'zgartirishni bloklaydi.

### Topshiriq #1194: Xavfsizlik siyosati (CSP) ogohlantirish paneli
**Tavsif:** Foydalanuvchini xavfsiz ulanish (HTTPS) haqida ogohlantiruvchi UI elementi.
**Talablar:** `position: fixed` yordamida har doim ko'rinib turishi.
**Yechim (HTML & CSS):**
```html
<div class="security-banner">🔒 Xavfsiz ulanish: AES-256 shifrlash faol.</div>
<style>
  .security-banner { position: fixed; top: 0; width: 100%; background: #2ecc71; color: white; text-align: center; }
</style>
```
**Tushuntirish:** Foydalanuvchi ishonchini oshirish uchun vizual tasdiq.

### Topshiriq #1195: Kriptografik xeshlar uchun "Copy-to-Clipboard" tugmasi
**Tavsif:** Hesh qiymatlarini xavfsiz nusxalash uchun interfeys.
**Talablar:** `navigator.clipboard` API dan foydalanish.
**Yechim (HTML & CSS):**
```html
<code id="hash">sha256:e3b0c44298fc1c149afbf4c8996fb924</code>
<button onclick="copyHash()">Nusxalash</button>
<script>
  function copyHash() {
    navigator.clipboard.writeText(document.getElementById('hash').innerText);
  }
</script>
```
**Tushuntirish:** Foydalanuvchi xatoliklarining oldini olish uchun to'g'ridan-to'g'ri tizim xotirasiga yozish.

### Topshiriq #1196: Xavfsiz yuklash (Loading) indikatori
**Tavsif:** Kriptografik operatsiyalar (masalan, RSA kalit generatsiyasi) davomida UI blokirovkasi.
**Talablar:** `pointer-events: none` yordamida foydalanuvchi harakatlarini vaqtincha to'xtatish.
**Yechim (HTML & CSS):**
```html
<div id="loader" class="disabled">Kriptografik kalit generatsiya qilinmoqda...</div>
<style>
  .disabled { pointer-events: none; opacity: 0.5; }
</style>
```
**Tushuntirish:** Operatsiya tugaguncha foydalanuvchi boshqa tugmalarni bosib yubormasligi uchun himoya.

### Topshiriq #1197: Parol kuchini vizual baholash (ECC kalitlari uchun)
**Tavsif:** Foydalanuvchi kiritayotgan parolning murakkabligini vizual ko'rsatish.
**Talablar:** CSS o'zgaruvchilari (variables) yordamida rangni dinamik o'zgartirish.
**Yechim (HTML & CSS):**
```html
<div id="strength-bar" style="height: 5px; width: 50%; background: red;"></div>
<script>
  // Parol uzunligiga qarab width va background o'zgaradi
</script>
```
**Tushuntirish:** Vizual fikr-mulohaza (feedback) foydalanuvchini kuchliroq parol tanlashga undaydi.

### Topshiriq #1198: Xavfsiz "Logout" tasdiqlash oynasi
**Tavsif:** Sessiyani tugatishdan oldin tasdiq so'rash.
**Talablar:** `z-index` yordamida modal oynani eng ustki qavatga chiqarish.
**Yechim (HTML & CSS):**
```html
<div class="modal">
  <p>Sessiyani yopishni istaysizmi?</p>
  <button>Ha</button>
</div>
<style>
  .modal { position: fixed; z-index: 1000; background: white; border: 1px solid red; }
</style>
```
**Tushuntirish:** Tasodifiy chiqib ketishlarning oldini olish va sessiya xavfsizligini nazorat qilish.

### Topshiriq #1199: Kriptografik ma'lumotlar jadvali (Data Grid)
**Tavsif:** AES kalitlari va ularning yaratilish vaqtini tartibli ko'rsatish.
**Talablar:** `table-layout: fixed` yordamida ma'lumotlar oqib ketishini oldini olish.
**Yechim (HTML & CSS):**
```html
<table style="table-layout: fixed; width: 100%;">
  <tr><th>ID</th><th>Kalit (AES)</th></tr>
  <tr><td>001</td><td style="overflow: hidden; text-overflow: ellipsis;">Long-AES-Key-String...</td></tr>
</table>
```
**Tushuntirish:** `text-overflow: ellipsis` uzun kalitlar UI ni buzmasligi uchun juda muhim.

### Topshiriq #1200: Xavfsizlik siyosati (CSP) meta-tegi
**Tavsif:** Brauzerda skriptlar xavfsizligini ta'minlash uchun HTML sarlavha qismi.
**Talablar:** `Content-Security-Policy` ni to'g'ri sozlash.
**Yechim (HTML & CSS):**
```html
<head>
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' https://trusted.cdn.com;">
</head>
```
**Tushuntirish:** XSS (Cross-Site Scripting) hujumlarini oldini olish uchun eng samarali himoya qatlami.