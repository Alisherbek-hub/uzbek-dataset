# Khorazmiy AI: HTML & CSS - Modul 23
## Mavzu: Tarmoq protokollari: TCP/UDP soketlari, HTTP/3, QUIC va WebSockets

### Topshiriq #1101: WebSocket ulanish holatini vizualizatsiya qilish
**Tavsif:** Real vaqt rejimida server bilan WebSocket orqali bog'lanish holatini (Connecting, Open, Closed, Error) foydalanuvchiga interfeys orqali ko'rsatish zarurati.
**Talablar:** CSS animatsiyalari yordamida ulanish holatini ko'rsatuvchi indikator va holat o'zgarganda silliq o'tish (transition) ta'minlanishi kerak.
**Yechim (HTML & CSS):**
```html
<div class="status-container">
  <span class="indicator" id="ws-status"></span>
  <span id="status-text">Ulanmoqda...</span>
</div>

<style>
  .status-container { display: flex; align-items: center; gap: 10px; font-family: sans-serif; }
  .indicator { width: 12px; height: 12px; border-radius: 50%; background: #f39c12; transition: 0.3s; }
  .connected { background: #27ae60; box-shadow: 0 0 8px #27ae60; }
  .disconnected { background: #c0392b; }
</style>
```
**Tushuntirish:** WebSocket holatini vizualizatsiya qilish foydalanuvchi tajribasi (UX) uchun muhim, chunki tarmoq uzilishlarini foydalanuvchi darhol sezishi kerak.

### Topshiriq #1102: HTTP/3 (QUIC) yuklanish indikatori
**Tavsif:** HTTP/3 protokoli tezligini ta'kidlash uchun zamonaviy "Skeleton Screen" yuklanish effektini yaratish.
**Talablar:** CSS `linear-gradient` va `keyframes` yordamida o'zgaruvchan fon effekti.
**Yechim (HTML & CSS):**
```html
<div class="skeleton"></div>

<style>
  .skeleton { width: 100%; height: 20px; background: linear-gradient(90deg, #eee 25%, #f5f5f5 50%, #eee 75%);
    background-size: 200% 100%; animation: loading 1.5s infinite; }
  @keyframes loading { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
</style>
```
**Tushuntirish:** HTTP/3 (QUIC) past kechikish (latency) bilan ishlaydi, shuning uchun yuklanish animatsiyasi tez va silliq bo'lishi kerak.

### Topshiriq #1103: TCP soket xatoliklari uchun ogohlantirish paneli
**Tavsif:** TCP ulanishida yuzaga kelishi mumkin bo'lgan "Timeout" yoki "Refused" xatolarini foydalanuvchiga yetkazish.
**Talablar:** `z-index` va `fixed` pozitsiyalash orqali ekranning yuqori qismida paydo bo'luvchi xabar oynasi.
**Yechim (HTML & CSS):**
```html
<div class="error-toast">TCP Soket xatosi: Serverga ulanib bo'lmadi!</div>

<style>
  .error-toast { position: fixed; top: 20px; right: 20px; background: #e74c3c; color: white; padding: 15px; border-radius: 5px; z-index: 1000; }
</style>
```
**Tushuntirish:** Xatolik xabarlarini foydalanuvchi interfeysidan ajratib turish (z-index) xavfsizlik va foydalanish qulayligi uchun muhim.

### Topshiriq #1104: QUIC protokoli uchun ma'lumotlar oqimi vizualizatsiyasi
**Tavsif:** QUIC protokoli ko'p oqimli (multiplexing) xususiyatini ko'rsatuvchi progress bar.
**Talablar:** Bir nechta progress bar elementlarini parallel boshqarish.
**Yechim (HTML & CSS):**
```html
<div class="stream"><div class="bar" style="width: 70%;"></div></div>

<style>
  .stream { width: 100%; background: #ddd; height: 8px; margin-bottom: 5px; }
  .bar { height: 100%; background: #3498db; transition: width 0.5s ease-in-out; }
</style>
```
**Tushuntirish:** QUIC bir vaqtning o'zida bir nechta oqimni (stream) qo'llab-quvvatlaydi, bu yondashuv ularni vizual ajratishga yordam beradi.

### Topshiriq #1105: WebSocket xavfsiz (WSS) ulanish belgisi
**Tavsif:** WebSocket ulanishi shifrlangan (WSS) ekanligini tasdiqlovchi qulf belgisi.
**Talablar:** CSS `::before` psevdo-elementi yordamida ikonka qo'shish.
**Yechim (HTML & CSS):**
```html
<div class="secure-badge">WSS Ulanish</div>

<style>
  .secure-badge::before { content: '🔒'; margin-right: 5px; }
  .secure-badge { color: #27ae60; font-weight: bold; }
</style>
```
**Tushuntirish:** Xavfsizlikni vizual tasdiqlash foydalanuvchida ishonch uyg'otadi.

### Topshiriq #1106: Tarmoq kechikishini (Latency) ko'rsatuvchi grafik
**Tavsif:** Server javob vaqtini (ms) ko'rsatuvchi dinamik grafik paneli.
**Talablar:** CSS `flex-end` yordamida ustunli grafik yaratish.
**Yechim (HTML & CSS):**
```html
<div class="chart"><div class="col" style="height: 40px;"></div><div class="col" style="height: 80px;"></div></div>

<style>
  .chart { display: flex; align-items: flex-end; gap: 5px; height: 100px; }
  .col { width: 20px; background: #9b59b6; }
</style>
```
**Tushuntirish:** Tarmoq sifatini monitoring qilish uchun ustunli grafik eng tushunarli formatdir.

### Topshiriq #1107: HTTP/3 "0-RTT" holati indikatori
**Tavsif:** HTTP/3 ning 0-RTT (Zero Round Trip Time) funksiyasi faolligini ko'rsatish.
**Talablar:** CSS `badge` uslubi va yorqin ranglar.
**Yechim (HTML & CSS):**
```html
<span class="badge-0rtt">0-RTT Active</span>

<style>
  .badge-0rtt { background: #f1c40f; padding: 2px 8px; border-radius: 12px; font-size: 10px; }
</style>
```
**Tushuntirish:** 0-RTT tezlikni oshiradi, buni interfeysda belgilash tizim optimallashganini ko'rsatadi.

### Topshiriq #1108: WebSocket "Heartbeat" (Ping/Pong) monitori
**Tavsif:** WebSocket ulanishi tirikligini tekshiruvchi "Heartbeat" signali uchun vizual puls effekti.
**Talablar:** `keyframes` yordamida pulsatsiyalanuvchi doira.
**Yechim (HTML & CSS):**
```html
<div class="pulse"></div>

<style>
  .pulse { width: 10px; height: 10px; background: blue; border-radius: 50%; animation: beat 1s infinite; }
  @keyframes beat { 0% { transform: scale(1); } 50% { transform: scale(1.5); } 100% { transform: scale(1); } }
</style>
```
**Tushuntirish:** Puls effekti ulanishning faol va barqarorligini psixologik jihatdan tasdiqlaydi.

### Topshiriq #1109: Tarmoq protokoli tanlash menyusi
**Tavsif:** Foydalanuvchiga HTTP/1.1, HTTP/2 va HTTP/3 orasida tanlov beruvchi interfeys.
**Talablar:** `radio` tugmalari va CSS `label` uslublari.
**Yechim (HTML & CSS):**
```html
<label><input type="radio" name="proto"> HTTP/3</label>

<style>
  label { display: block; padding: 10px; border: 1px solid #ccc; cursor: pointer; }
  input:checked + label { background: #e1f5fe; }
</style>
```
**Tushuntirish:** Protokol tanlash foydalanuvchiga moslashuvchanlik beradi, bu ayniqsa test muhitlarida muhim.

### Topshiriq #1110: Soket ma'lumotlar paketi vizualizatori
**Tavsif:** Kelayotgan TCP paketlarini vizual tarzda ko'rsatish uchun "Log" oynasi.
**Talablar:** `overflow-y: auto` va `monospace` shrift.
**Yechim (HTML & CSS):**
```html
<div class="log-box">TCP: Packet received...</div>

<style>
  .log-box { font-family: monospace; background: #2c3e50; color: #ecf0f1; height: 150px; overflow-y: auto; padding: 10px; }
</style>
```
**Tushuntirish:** Monospace shrifti va qorong'u fon texnik loglarni o'qishni osonlashtiradi va professional ko'rinish beradi.

---

### Topshiriq #1111: Real-vaqtda TCP soket holati monitori
**Tavsif:** Serverdagi TCP ulanishlarining holatini (ESTABLISHED, TIME_WAIT) vizual ko'rsatish uchun dashboard interfeysi.
**Talablar:** CSS Grid yordamida responsiv panellar, holatga qarab rangli indikatorlar.
**Yechim (HTML & CSS):**
```html
<div class="socket-grid">
  <div class="card active">TCP: 8080 - ESTABLISHED</div>
  <div class="card pending">TCP: 443 - TIME_WAIT</div>
</div>
<style>
  .socket-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }
  .card { padding: 15px; border-radius: 8px; color: white; font-family: sans-serif; }
  .active { background: #27ae60; } /* Ulanish faol */
  .pending { background: #f39c12; } /* Kutish holati */
</style>
```
**Tushuntirish:** Grid tizimi ma'lumotlar oqimini vizual tartibga solish uchun eng samarali usuldir.

### Topshiriq #1112: UDP paket yo'qotilishi vizualizatori
**Tavsif:** UDP protokoli "best-effort" bo'lgani uchun paket yo'qotilishini ko'rsatuvchi progress bar.
**Talablar:** CSS animatsiyasi yordamida paket oqimini simulyatsiya qilish.
**Yechim (HTML & CSS):**
```html
<div class="packet-stream"><div class="packet"></div></div>
<style>
  .packet-stream { width: 100%; height: 20px; background: #eee; overflow: hidden; }
  .packet { width: 20px; height: 100%; background: red; animation: move 2s linear infinite; }
  @keyframes move { from { margin-left: 0; } to { margin-left: 100%; } }
</style>
```
**Tushuntirish:** CSS animatsiyasi CPU resursini tejaydi va UDP paketlarining uzluksiz oqimini simulyatsiya qiladi.

### Topshiriq #1113: HTTP/3 (QUIC) ulanish xavfsizlik indikatori
**Tavsif:** HTTP/3 protokoli UDP ustiga qurilgani uchun xavfsizlik (TLS 1.3) holatini ko'rsatuvchi UI komponenti.
**Talablar:** Shifrlangan ulanish uchun "Qulf" belgisi va QUIC protokoli yorlig'i.
**Yechim (HTML & CSS):**
```html
<div class="quic-badge">QUIC/HTTP3 <span class="lock">🔒</span></div>
<style>
  .quic-badge { padding: 5px 15px; background: #2c3e50; color: #fff; border-radius: 20px; display: inline-flex; align-items: center; }
  .lock { margin-left: 8px; color: #f1c40f; }
</style>
```
**Tushuntirish:** QUIC protokoli tezkorligi bilan birga xavfsizlikni ham talab qiladi, bu vizual element foydalanuvchiga ishonch beradi.

### Topshiriq #1114: WebSocket ulanish holati (Handshake)
**Tavsif:** WebSocket ulanishining "Handshake" bosqichini ko'rsatuvchi status bar.
**Talablar:** Ulanish urinishi va muvaffaqiyatli ulanish holatlari uchun CSS holat sinflari.
**Yechim (HTML & CSS):**
```html
<div class="ws-status connecting">Ulanish o'rnatilmoqda...</div>
<style>
  .ws-status { padding: 10px; border-left: 5px solid #3498db; background: #ecf0f1; }
  .connecting { border-color: #3498db; }
</style>
```
**Tushuntirish:** WebSocket ulanishlari doimiy bo'lgani uchun, status bar foydalanuvchini real vaqtda xabardor qiladi.

### Topshiriq #1115: TCP "Three-way Handshake" diagrammasi
**Tavsif:** TCP ulanish bosqichlarini (SYN, SYN-ACK, ACK) tushuntiruvchi vizual bloklar.
**Talablar:** Flexbox yordamida ketma-ketlikni ko'rsatish.
**Yechim (HTML & CSS):**
```html
<div class="handshake-flow"><div>SYN</div><span>→</span><div>SYN-ACK</div><span>→</span><div>ACK</div></div>
<style>
  .handshake-flow { display: flex; align-items: center; gap: 10px; font-weight: bold; }
</style>
```
**Tushuntirish:** Flexbox elementlarni gorizontal tartibda mukammal joylashtiradi, bu tarmoq protokollari ketma-ketligini tushunishga yordam beradi.

### Topshiriq #1116: QUIC Stream multiplexing vizualizatsiyasi
**Tavsif:** Bir nechta oqimni (stream) bitta ulanishda ko'rsatish.
**Talablar:** Bir nechta rangli chiziqlar (streamlar) bitta asosiy kanal ichida.
**Yechim (HTML & CSS):**
```html
<div class="quic-connection"><div class="stream s1"></div><div class="stream s2"></div></div>
<style>
  .quic-connection { border: 2px dashed #333; height: 50px; display: flex; }
  .stream { flex: 1; height: 100%; }
  .s1 { background: blue; } .s2 { background: green; }
</style>
```
**Tushuntirish:** QUIC ning asosiy ustunligi - Head-of-line blocking muammosini hal qiluvchi multipleksingdir.

### Topshiriq #1117: WebSocket "Heartbeat" (Ping/Pong) indikatori
**Tavsif:** WebSocket ulanishi tirikligini tekshiruvchi puls effekti.
**Talablar:** CSS `pulse` animatsiyasi.
**Yechim (HTML & CSS):**
```html
<div class="pulse"></div>
<style>
  .pulse { width: 10px; height: 10px; background: green; border-radius: 50%; animation: blink 1s infinite; }
  @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } }
</style>
```
**Tushuntirish:** Heartbeat signallari WebSocket ulanishini uzilib qolishdan saqlaydi, vizual indikator esa buni tasdiqlaydi.

### Topshiriq #1118: TCP Window Size vizualizatori
**Tavsif:** TCP oqim nazorati (Flow Control) uchun oynani boshqarish interfeysi.
**Talablar:** Dinamik o'lchamli blok.
**Yechim (HTML & CSS):**
```html
<div class="tcp-window" style="width: 70%;">Window Size: 70%</div>
<style>
  .tcp-window { background: #9b59b6; color: white; padding: 10px; transition: width 0.5s; }
</style>
```
**Tushuntirish:** TCP oynasi hajmi tarmoq tiqilinchini boshqaradi, CSS `transition` esa bu o'zgarishni yumshoq ko'rsatadi.

### Topshiriq #1119: HTTP/3 Header Compression (QPack) paneli
**Tavsif:** HTTP/3 da header siqilishini ko'rsatuvchi ma'lumotlar paneli.
**Talablar:** Siqilgan va asl ma'lumot hajmini solishtirish.
**Yechim (HTML & CSS):**
```html
<div class="data-box">Original: 1KB <br> Compressed: 0.2KB</div>
<style>
  .data-box { border: 1px solid #ccc; padding: 10px; font-family: monospace; }
</style>
```
**Tushuntirish:** QPack HTTP/3 ning tezligini ta'minlaydi, bu panel esa samaradorlikni ko'rsatadi.

### Topshiriq #1120: Tarmoq protokoli tanlash menyusi
**Tavsif:** Foydalanuvchiga TCP, UDP yoki WebSocket ni tanlash imkonini beruvchi interfeys.
**Talablar:** Hover effektlari va tanlangan holat uchun CSS `:checked` psevdo-sinfi.
**Yechim (HTML & CSS):**
```html
<input type="radio" name="proto" id="tcp"> <label for="tcp">TCP</label>
<style>
  input:checked + label { color: blue; font-weight: bold; }
</style>
```
**Tushuntirish:** `:checked` psevdo-sinfi JavaScriptsiz interaktivlikni ta'minlaydi, bu esa kodni yengil va xavfsiz qiladi.

---

### Topshiriq #1121: Real-time WebSocket Status Monitor
**Tavsif:** WebSocket ulanish holatini (Connected/Disconnected) foydalanuvchi interfeysida real vaqt rejimida vizual aks ettirish.
**Talablar:** CSS animatsiyalari orqali status o'zgarishini ko'rsatish, holat o'zgarganda foydalanuvchini ogohlantirish.
**Yechim (HTML & CSS):**
```html
<div class="status-container">
  <span class="indicator" id="ws-status"></span>
  <span id="status-text">Ulanmoqda...</span>
</div>

<style>
  .status-container { display: flex; align-items: center; gap: 10px; font-family: sans-serif; }
  .indicator { width: 12px; height: 12px; border-radius: 50%; background: orange; }
  /* WebSocket faol bo'lganda yashil rangga o'tish */
  .connected { background: #2ecc71; box-shadow: 0 0 8px #2ecc71; }
  .disconnected { background: #e74c3c; }
</style>
```
**Tushuntirish:** WebSocket ulanish holatini vizualizatsiya qilish foydalanuvchi tajribasini (UX) yaxshilaydi va tarmoq uzilishlarini tez aniqlashga yordam beradi.

### Topshiriq #1122: HTTP/3 (QUIC) Yuklanish Indikatori
**Tavsif:** HTTP/3 protokoli tezligini ta'kidlash uchun zamonaviy yuklanish (loading) animatsiyasini yaratish.
**Talablar:** Minimal resurs sarfi, CSS `keyframes` yordamida optimallashtirilgan harakat.
**Yechim (HTML & CSS):**
```html
<div class="quic-loader"></div>
<style>
  .quic-loader { width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; animation: spin 0.8s linear infinite; }
  @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
</style>
```
**Tushuntirish:** HTTP/3 (QUIC) tezkorligi fonida, UI elementlari ham minimalistik va tezkor animatsiyalarga ega bo'lishi kerak.

### Topshiriq #1123: TCP Soket Xatolik Xabarnomasi
**Tavsif:** Tarmoq soketlari bilan bog'liq xatoliklar yuz berganda foydalanuvchi uchun professional xabar oynasini ko'rsatish.
**Talablar:** `z-index` orqali boshqa elementlar ustida turishi, xavfsizlik uchun "modal" dizayn.
**Yechim (HTML & CSS):**
```html
<div class="error-modal">
  <p>Tarmoq xatosi: Soket ulanishi uzildi.</p>
</div>
<style>
  .error-modal { position: fixed; top: 20px; right: 20px; background: #ff4757; color: white; padding: 15px; border-radius: 5px; z-index: 1000; }
</style>
```
**Tushuntirish:** Soket xatolarini yashirmaslik, balki foydalanuvchiga aniq xabar berish tizim barqarorligini oshiradi.

### Topshiriq #1124: UDP Paket Yo'qotilishi Vizualizatsiyasi
**Tavsif:** UDP protokoli ishonchsizligi sababli ma'lumotlar yo'qolishi mumkinligini ko'rsatuvchi "Packet Loss" indikatori.
**Talablar:** CSS `opacity` va `transition` xossalaridan foydalanish.
**Yechim (HTML & CSS):**
```html
<div class="packet-loss-bar">
  <div class="loss-fill" style="width: 15%;"></div>
</div>
<style>
  .packet-loss-bar { width: 100%; background: #ddd; height: 10px; }
  .loss-fill { height: 100%; background: #f1c40f; transition: width 0.3s ease; }
</style>
```
**Tushuntirish:** UDP orqali uzatiladigan ma'lumotlar oqimida paket yo'qotilishini vizual kuzatish tarmoq sifatini baholashga yordam beradi.

### Topshiriq #1125: WebSocket Chat Xabarlar Paneli
**Tavsif:** WebSocket orqali kelayotgan xabarlarni tartibli ko'rsatish uchun "Chat Bubble" dizayni.
**Talablar:** `flexbox` yordamida xabarlarni o'ng va chap tomonga ajratish.
**Yechim (HTML & CSS):**
```html
<div class="chat-message sent">Salom, server!</div>
<style>
  .chat-message { padding: 10px; margin: 5px; border-radius: 10px; max-width: 70%; }
  .sent { background: #007bff; color: white; align-self: flex-end; margin-left: auto; }
</style>
```
**Tushuntirish:** WebSocket orqali real vaqtda almashinadigan ma'lumotlar uchun `flexbox` eng samarali joylashtirish usulidir.

### Topshiriq #1126: Tarmoq Latentligi (Ping) Monitori
**Tavsif:** Serverga bo'lgan ping vaqtini ko'rsatuvchi dinamik raqamli panel.
**Talablar:** Raqamlar o'zgarganda silliq animatsiya.
**Yechim (HTML & CSS):**
```html
<div class="ping-monitor">Ping: <span id="ping-val">24</span>ms</div>
<style>
  .ping-monitor { font-family: monospace; color: #27ae60; font-weight: bold; }
</style>
```
**Tushuntirish:** Latentlikni ko'rsatish foydalanuvchiga tarmoq sifatini baholash imkonini beradi.

### Topshiriq #1127: QUIC Protokoli Xavfsizlik Belgisi
**Tavsif:** QUIC protokoli orqali shifrlangan ulanishni tasdiqlovchi "Secure" qalqon belgisi.
**Talablar:** CSS `clip-path` yordamida qalqon shaklini chizish.
**Yechim (HTML & CSS):**
```html
<div class="shield"></div>
<style>
  .shield { width: 30px; height: 35px; background: #2ecc71; clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%); }
</style>
```
**Tushuntirish:** QUIC o'z ichiga TLS 1.3 ni oladi, shuning uchun xavfsizlik belgisi foydalanuvchiga ishonch bag'ishlaydi.

### Topshiriq #1128: Soket Ulanish Tugmasi
**Tavsif:** WebSocket ulanishini qo'lda boshlash/to'xtatish uchun interaktiv tugma.
**Talablar:** `:hover` va `:active` holatlari uchun vizual o'zgarishlar.
**Yechim (HTML & CSS):**
```html
<button class="ws-btn">Ulanishni boshlash</button>
<style>
  .ws-btn { padding: 10px 20px; background: #3498db; border: none; color: white; cursor: pointer; transition: 0.3s; }
  .ws-btn:hover { background: #2980b9; }
</style>
```
**Tushuntirish:** Foydalanuvchi nazorati ostidagi ulanishlar resurslarni tejashga yordam beradi.

### Topshiriq #1129: Tarmoq Oqimi (Stream) Vizualizatori
**Tavsif:** WebSocket orqali kelayotgan ma'lumotlar oqimini ko'rsatuvchi progress bar.
**Talablar:** `linear-gradient` yordamida oqimni vizualizatsiya qilish.
**Yechim (HTML & CSS):**
```html
<div class="stream-bar"><div class="progress"></div></div>
<style>
  .stream-bar { width: 100%; height: 5px; background: #eee; overflow: hidden; }
  .progress { width: 50%; height: 100%; background: linear-gradient(to right, #3498db, #9b59b6); }
</style>
```
**Tushuntirish:** Ma'lumotlar oqimini vizualizatsiya qilish foydalanuvchiga jarayon davom etayotganini bildiradi.

### Topshiriq #1130: TCP/IP Port Holati Kartasi
**Tavsif:** Ochilgan portlar holatini ko'rsatuvchi ma'lumotlar kartasi.
**Talablar:** `box-shadow` va `border-left` orqali port holatini (Open/Closed) ajratish.
**Yechim (HTML & CSS):**
```html
<div class="port-card open">Port 8080: Ochiq</div>
<style>
  .port-card { padding: 15px; border-left: 5px solid #ccc; box-shadow: 2px 2px 5px #eee; }
  .open { border-left-color: #2ecc71; }
</style>
```
**Tushuntirish:** Port holatini kartalar ko'rinishida berish tizim administratorlari uchun qulay interfeys yaratadi.

---

### Topshiriq #1131: WebSocket orqali real vaqtda server holatini monitoring qilish
**Tavsif:** Serverdagi TCP soket ulanishlari holatini vizualizatsiya qilish uchun real vaqtda yangilanuvchi dashboard interfeysi.
**Talablar:** CSS Grid yordamida responsiv layout, status indikatorlari uchun CSS animatsiyalari.
**Yechim (HTML & CSS):**
```html
<div class="monitor-grid">
  <div class="status-card active">TCP Soket: <span>Faol</span></div>
  <div class="status-card pending">UDP Soket: <span>Kutilmoqda</span></div>
</div>
<style>
  .monitor-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
  .status-card { padding: 20px; border-radius: 8px; background: #f4f4f9; border-left: 5px solid #ccc; }
  .active { border-color: #2ecc71; animation: pulse 2s infinite; }
  @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
</style>
```
**Tushuntirish:** CSS animatsiyalari serverdan kelayotgan WebSocket signallarini foydalanuvchiga vizual tarzda yetkazish uchun eng yengil usuldir.

### Topshiriq #1132: HTTP/3 (QUIC) yuklanish indikatori
**Tavsif:** HTTP/3 protokoli tezligini ifodalovchi progress bar.
**Talablar:** CSS `conic-gradient` yordamida tezlikni vizualizatsiya qilish.
**Yechim (HTML & CSS):**
```html
<div class="quic-loader" style="--val: 85%"></div>
<style>
  .quic-loader { width: 100px; height: 100px; border-radius: 50%; background: conic-gradient(#3498db var(--val), #eee 0); }
</style>
```
**Tushuntirish:** `conic-gradient` renderlash uchun GPU'dan foydalanadi, bu esa tarmoq protokollari monitoringida resursni tejaydi.

### Topshiriq #1133: WebSocket xavfsizlik ogohlantirish paneli
**Tavsif:** Xavfsiz bo'lmagan (ws://) ulanishlar uchun ogohlantirish interfeysi.
**Talablar:** Z-index boshqaruvi va modal oynalar uchun CSS `backdrop-filter`.
**Yechim (HTML & CSS):**
```html
<div class="modal">Xavfli ulanish aniqlandi! WSS protokoli talab qilinadi.</div>
<style>
  .modal { position: fixed; top: 20px; backdrop-filter: blur(10px); background: rgba(231, 76, 60, 0.8); color: white; padding: 15px; }
</style>
```
**Tushuntirish:** `backdrop-filter` foydalanuvchi diqqatini xavfsizlik masalasiga qaratish uchun zamonaviy va samarali yondashuvdir.

### Topshiriq #1134: UDP paket yo'qotilishi vizualizatori
**Tavsif:** UDP protokoli "best-effort" xususiyatini ko'rsatuvchi vizual element.
**Talablar:** CSS `transition` va `opacity` orqali paketlarning yo'qolishini simulyatsiya qilish.
**Yechim (HTML & CSS):**
```html
<div class="packet-stream"><div class="packet"></div></div>
<style>
  .packet { width: 10px; height: 10px; background: blue; transition: opacity 0.5s; }
  .packet:hover { opacity: 0; } /* Paket yo'qolishi simulyatsiyasi */
</style>
```
**Tushuntirish:** UDP'ning ishonchsizligini ko'rsatish uchun foydalanuvchi interaktivligi (hover) orqali paketlarning "yo'qolishi" simulyatsiya qilindi.

### Topshiriq #1135: QUIC 0-RTT ulanish holati
**Tavsif:** QUIC protokoli 0-RTT (Zero Round Trip Time) xususiyatini ko'rsatuvchi ikonka.
**Talablar:** SVG va CSS transformatsiyalaridan foydalanish.
**Yechim (HTML & CSS):**
```html
<div class="rtt-icon">⚡</div>
<style>
  .rtt-icon { font-size: 2rem; transform: rotate(0deg); transition: transform 0.3s; }
  .rtt-icon:hover { transform: rotate(360deg); }
</style>
```
**Tushuntirish:** 0-RTT tezkorligini ifodalash uchun CSS transformatsiyalari eng tezkor vizual javobni beradi.

### Topshiriq #1136: TCP "Three-way Handshake" diagrammasi
**Tavsif:** TCP ulanish bosqichlarini ko'rsatuvchi CSS timeline.
**Talablar:** `::before` va `::after` psevdo-elementlari yordamida chiziqli bog'lanish.
**Yechim (HTML & CSS):**
```html
<ul class="timeline"><li>SYN</li><li>SYN-ACK</li><li>ACK</li></ul>
<style>
  .timeline { display: flex; list-style: none; }
  .timeline li::after { content: '→'; margin: 0 10px; }
</style>
```
**Tushuntirish:** Murakkab diagrammalar o'rniga CSS psevdo-elementlari yordamida yengil va semantik chiziqli diagramma yaratildi.

### Topshiriq #1137: WebSocket ulanish loglari uchun terminal oynasi
**Tavsif:** WebSocket orqali kelayotgan ma'lumotlar oqimini ko'rsatuvchi qora fonli terminal.
**Talablar:** `overflow-y: auto` va `monospace` shriftlar.
**Yechim (HTML & CSS):**
```html
<div class="terminal"><code>[INFO] WebSocket connected...</code></div>
<style>
  .terminal { background: #000; color: #0f0; font-family: monospace; height: 150px; overflow-y: scroll; }
</style>
```
**Tushuntirish:** `monospace` shrifti ma'lumotlar oqimini o'qishni osonlashtiradi, terminal ko'rinishi esa tizim muhandislari uchun qulay.

### Topshiriq #1138: HTTP/3 Header Compression (QPACK) vizualizatori
**Tavsif:** QPACK siqilishini ko'rsatuvchi taqqoslash paneli.
**Talablar:** Flexbox yordamida ikki ustunli taqqoslash interfeysi.
**Yechim (HTML & CSS):**
```html
<div class="compare"><div class="old">HTTP/2: 500b</div><div class="new">HTTP/3: 50b</div></div>
<style>
  .compare { display: flex; justify-content: space-between; width: 300px; }
  .new { color: green; font-weight: bold; }
</style>
```
**Tushuntirish:** QPACK samaradorligini vizual taqqoslash orqali foydalanuvchiga protokollar farqini tushuntirish osonlashadi.

### Topshiriq #1139: Soket portlari uchun xavfsizlik qulfi
**Tavsif:** Ochiq portlarni himoyalashni ko'rsatuvchi vizual qulf belgisi.
**Talablar:** CSS `clip-path` yordamida qulf shaklini yasash.
**Yechim (HTML & CSS):**
```html
<div class="lock"></div>
<style>
  .lock { width: 20px; height: 20px; background: gold; clip-path: polygon(20% 0%, 80% 0%, 100% 100%, 0% 100%); }
</style>
```
**Tushuntirish:** `clip-path` yordamida tasvirlarsiz (image-less) murakkab shakllar yaratish sahifa yuklanishini tezlashtiradi.

### Topshiriq #1140: Tarmoq kechikishi (Latency) uchun rangli indikator
**Tavsif:** Ping vaqtiga qarab rangni o'zgartiruvchi indikator.
**Talablar:** CSS o'zgaruvchilari (variables) va `calc()` funksiyasi.
**Yechim (HTML & CSS):**
```html
<div class="ping-bar" style="--p: 20ms"></div>
<style>
  .ping-bar { width: 100px; height: 10px; background: hsl(calc(120 - var(--p)/2), 100%, 50%); }
</style>
```
**Tushuntirish:** `hsl` rang modeli va `calc()` yordamida kechikish vaqtiga qarab dinamik rang o'zgarishi amalga oshirildi, bu esa kodni minimal darajada saqlaydi.

---

### Topshiriq #1141: WebSocket ulanish holatini vizualizatsiya qilish
**Tavsif:** Real vaqt rejimida server bilan WebSocket aloqasi uzilganda foydalanuvchini ogohlantirish va qayta ulanish jarayonini ko'rsatish.
**Talablar:** CSS animatsiyasi orqali ulanish holatini (online/offline) ko'rsatish, xavfsizlik uchun faqat `wss://` protokolidan foydalanishni nazarda tutish.
**Yechim (HTML & CSS):**
```html
<div id="status-indicator" class="offline">Ulanmoqda...</div>
<style>
  #status-indicator { padding: 10px; color: white; transition: 0.3s; }
  .online { background-color: #27ae60; } /* WebSocket faol */
  .offline { background-color: #c0392b; animation: blink 1s infinite; }
  @keyframes blink { 50% { opacity: 0.5; } }
</style>
```
**Tushuntirish:** `transition` va `keyframes` orqali foydalanuvchi tajribasini (UX) yaxshilash, tarmoq uzilishlarini vizual aniq ko'rsatish.

### Topshiriq #1142: HTTP/3 (QUIC) yuklanish indikatori
**Tavsif:** HTTP/3 protokoli tezligini ta'kidlash uchun "Zero Round Trip Time" (0-RTT) vizualizatsiyasi.
**Talablar:** Minimalist dizayn, CSS `conic-gradient` yordamida tezkor yuklanish animatsiyasi.
**Yechim (HTML & CSS):**
```html
<div class="quic-loader"></div>
<style>
  .quic-loader { width: 50px; height: 50px; border-radius: 50%; 
                 background: conic-gradient(#3498db, transparent); animation: spin 0.5s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }
</style>
```
**Tushuntirish:** HTTP/3 ning past kechikish (latency) xususiyatini ifodalash uchun tezkor aylanish animatsiyasi tanlandi.

### Topshiriq #1143: Soket ma'lumotlar oqimi uchun terminal interfeysi
**Tavsif:** TCP soketlari orqali kelayotgan loglarni HTML jadvalda ko'rsatish.
**Talablar:** `overflow-y: auto` orqali loglar oqimini boshqarish, `monospace` shriftlaridan foydalanish.
**Yechim (HTML & CSS):**
```html
<div class="terminal">
  <pre><code>[TCP] Socket connected: 192.168.1.1:8080</code></pre>
</div>
<style>
  .terminal { background: #000; color: #0f0; padding: 15px; height: 200px; overflow-y: scroll; }
</style>
```
**Tushuntirish:** TCP oqimini kuzatish uchun terminal uslubi ma'lumotlarni tahlil qilishda qulaylik yaratadi.

### Topshiriq #1144: QUIC protokoli xavfsizlik qalqoni
**Tavsif:** QUIC protokoli o'rnatilgan TLS 1.3 shifrlashini vizual tasvirlash.
**Talablar:** Qulf belgisi va CSS `box-shadow` yordamida xavfsizlik darajasini ko'rsatish.
**Yechim (HTML & CSS):**
```html
<div class="secure-badge">QUIC + TLS 1.3 Shifrlangan</div>
<style>
  .secure-badge { border: 2px solid #2ecc71; box-shadow: 0 0 10px #2ecc71; padding: 5px 15px; border-radius: 20px; }
</style>
```
**Tushuntirish:** QUIC'ning xavfsizlik ustunligini foydalanuvchiga vizual tasdiqlash orqali ishonchni oshirish.

### Topshiriq #1145: WebSocket xabar yuborish paneli
**Tavsif:** Foydalanuvchi xabar yuborayotganda soket holatini tekshiruvchi interfeys.
**Talablar:** `disabled` atributi va CSS `opacity` orqali ulanmagan holatda tugmani bloklash.
**Yechim (HTML & CSS):**
```html
<input type="text" placeholder="Xabar...">
<button disabled class="send-btn">Yuborish</button>
<style>
  .send-btn:disabled { opacity: 0.5; cursor: not-allowed; background: #ccc; }
</style>
```
**Tushuntirish:** Soket ulanmaguncha yuborish tugmasini bloklash xatoliklar (socket error) oldini oladi.

### Topshiriq #1146: Tarmoq kechikishi (Latency) grafigi
**Tavsif:** TCP soketidagi RTT (Round Trip Time) qiymatini CSS ustunli diagramma bilan ko'rsatish.
**Talablar:** `flex-end` hizalanishi, dinamik balandlik.
**Yechim (HTML & CSS):**
```html
<div class="chart"><div style="height: 40px;"></div><div style="height: 80px;"></div></div>
<style>
  .chart { display: flex; align-items: flex-end; gap: 5px; height: 100px; }
  .chart div { width: 20px; background: #e67e22; }
</style>
```
**Tushuntirish:** Tarmoq sifatini vizual monitoring qilish uchun eng samarali usul.

### Topshiriq #1147: UDP paket yo'qotilishi ogohlantirishi
**Tavsif:** UDP protokoli "connectionless" bo'lgani uchun paket yo'qotilishini vizual ko'rsatish.
**Talablar:** CSS `filter: grayscale()` yordamida paketlar sifatini pasaytirish.
**Yechim (HTML & CSS):**
```html
<div class="packet lost">Paket #404</div>
<style>
  .packet { padding: 5px; background: #3498db; }
  .lost { filter: grayscale(1); opacity: 0.3; }
</style>
```
**Tushuntirish:** UDP'dagi ishonchsizlikni (packet loss) vizualizatsiya qilish orqali tizimni debug qilishni osonlashtirish.

### Topshiriq #1148: WebSocket "Handshake" animatsiyasi
**Tavsif:** Client va Server o'rtasidagi WebSocket handshake jarayonini ko'rsatish.
**Talablar:** Ikki nuqta o'rtasida harakatlanuvchi CSS element.
**Yechim (HTML & CSS):**
```html
<div class="handshake"><div class="ball"></div></div>
<style>
  .handshake { width: 100px; border-bottom: 2px dashed #000; position: relative; }
  .ball { width: 10px; height: 10px; background: red; position: absolute; animation: move 2s infinite; }
  @keyframes move { 0% { left: 0; } 100% { left: 90px; } }
</style>
```
**Tushuntirish:** Handshake jarayonini vizualizatsiya qilish protokollar ishlash prinsipini tushunishga yordam beradi.

### Topshiriq #1149: HTTP/3 Stream multiplexing vizualizatsiyasi
**Tavsif:** Bir vaqtning o'zida bir nechta so'rovlarni (streams) ko'rsatish.
**Talablar:** `grid` layout va bir vaqtda yuklanuvchi elementlar.
**Yechim (HTML & CSS):**
```html
<div class="streams"><div>S1</div><div>S2</div><div>S3</div></div>
<style>
  .streams { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
  .streams div { background: #9b59b6; color: white; padding: 10px; }
</style>
```
**Tushuntirish:** HTTP/3 ning asosiy ustunligi bo'lgan parallel streamlarni vizual ajratib ko'rsatish.

### Topshiriq #1150: Soket xavfsizlik siyosati (CORS/Origin)
**Tavsif:** WebSocket ulanishida ruxsat etilgan domenlarni tekshirish interfeysi.
**Talablar:** Ruxsat berilgan (yashil) va rad etilgan (qizil) domenlar ro'yxati.
**Yechim (HTML & CSS):**
```html
<ul class="policy">
  <li class="allowed">wss://api.khorazmiy.uz</li>
  <li class="denied">wss://malicious.com</li>
</ul>
<style>
  .allowed { color: green; } .denied { color: red; text-decoration: line-through; }
</style>
```
**Tushuntirish:** Xavfsizlik nuqtai nazaridan soket ulanishlarini oq ro'yxat (whitelist) asosida boshqarishni vizual tasdiqlash.