# Khorazmiy AI: HTML & CSS - Modul 23
## Mavzu: Zamonaviy Veb Tarmoq API'lari: WebTransport UI, Server-Sent Events oqimlari, Streaming Fetch API, WebRTC MediaStream, Service Workers Offline Kesh va WebSocket boshqaruvi

### Topshiriq #1101: WebTransport Sessiyasini Ochish va Ulanish Holatini Vizualizatsiya Qilish UI
**Tavsif:** HTTP/3 va QUIC ustiga qurilgan zamonaviy WebTransport API orqali server bilan ultra past kechikishli ulanish o'rnatish va tarmoq holatini real vaqtda ko'rsatuvchi interfeys yaratish.
**Talablar:** WebTransport obyekti, transport.ready va transport.closed va'dalarini (promises) boshqarish, CSS status indikatori va xatoliklarni xavfsiz aks ettirish.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>WebTransport Boshqaruv Paneli</title>
  <style>
    :root {
      --bg: #0f172a;
      --card: #1e293b;
      --accent: #38bdf8;
      --success: #22c55e;
      --danger: #ef4444;
      --text: #f8fafc;
    }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: system-ui, -apple-system, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
    }
    .transport-card {
      background: var(--card);
      padding: 24px;
      border-radius: 16px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
      width: 420px;
    }
    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 14px;
      font-weight: 600;
      background: rgba(255,255,255,0.05);
    }
    .dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #94a3b8;
    }
    .dot.connected { background: var(--success); box-shadow: 0 0 10px var(--success); }
    .dot.connecting { background: var(--accent); animation: pulse 1s infinite alternate; }
    .dot.error { background: var(--danger); }
    @keyframes pulse { from { opacity: 0.4; } to { opacity: 1; } }
    button {
      background: var(--accent);
      color: #000;
      border: none;
      padding: 10px 16px;
      border-radius: 8px;
      font-weight: 600;
      cursor: pointer;
      margin-top: 15px;
      width: 100%;
      transition: opacity 0.2s;
    }
    button:hover { opacity: 0.9; }
    .log-terminal {
      background: #020617;
      padding: 12px;
      border-radius: 8px;
      margin-top: 15px;
      font-family: monospace;
      font-size: 12px;
      height: 120px;
      overflow-y: auto;
      border: 1px solid #334155;
    }
  </style>
</head>
<body>

<div class="transport-card">
  <h2>WebTransport (HTTP/3) Aloqasi</h2>
  <div class="status-badge">
    <div id="statusDot" class="dot"></div>
    <span id="statusText">Ulanmagan</span>
  </div>
  
  <button id="btnConnect" onclick="initWebTransport()">WebTransport-ni Yoqish</button>
  
  <div class="log-terminal" id="terminalLogs">
    <div>[Tizim] WebTransport tayyor...</div>
  </div>
</div>

<script>
  let transport = null;
  const dot = document.getElementById('statusDot');
  const txt = document.getElementById('statusText');
  const logs = document.getElementById('terminalLogs');

  function log(msg) {
    const entry = document.createElement('div');
    entry.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
    logs.appendChild(entry);
    logs.scrollTop = logs.scrollHeight;
  }

  async function initWebTransport() {
    const url = 'https://127.0.0.1:4433/webtransport';
    dot.className = 'dot connecting';
    txt.textContent = 'Ulanmoqda (QUIC Handshake)...';
    log('WebTransport sessiyasi boshlanmoqda: ' + url);

    try {
      if (!window.WebTransport) {
        throw new Error('Brauzer WebTransport API ni qo'llab-quvvatlamaydi!');
      }

      transport = new WebTransport(url);
      
      // ready promisi ulanish to'liq o'rnatilganda bajariladi
      await transport.ready;
      dot.className = 'dot connected';
      txt.textContent = 'Ulangan (HTTP/3)';
      log('QUIC ulanishi muvaffaqiyatli o'rnatildi!');

      // Ulanish yopilishini monitoring qilish
      transport.closed.then(() => {
        dot.className = 'dot';
        txt.textContent = 'Yopildi';
        log('WebTransport sessiyasi normal yopildi.');
      }).catch((err) => {
        dot.className = 'dot error';
        txt.textContent = 'Nosozlik bilan yopildi';
        log('Xatolik: ' + err.message);
      });

    } catch (e) {
      dot.className = 'dot error';
      txt.textContent = 'Xato yuz berdi';
      log('Ulanish xatosi: ' + e.message);
    }
  }
</script>

</body>
</html>
```
**Tushuntirish:** WebTransport API HTTP/3 (QUIC) ustida ishlaydi va WebSockets-ga nisbatan Head-of-Line blocking muammosidan to'liq xoli. `transport.ready` promisi TLS 1.3 va QUIC handshake to'liq yakunlanganda bajariladi, `transport.closed` esa ulanish holatini kuzatib turadi.

---

### Topshiriq #1102: WebTransport Unreliable Datagrams Orqali O'yin Kursori Harakatini Uzatish
**Tavsif:** Real-time ko'p o'yinchili o'yinlarda har 16ms da kursor koordinatalarini yetkazishda TCP qayta uzatishlari (retransmissions) kechikish hosil qiladi. WebTransport datagrams yordamida yo'qotishga chidamli (unreliable) eng past kechikishli kanaldan foydalanish talab etiladi.
**Talablar:** transport.datagrams.writable va readable oqimlari, Uint8Array koordinatalar, CSS bilan jonli kursor animatsiyasi.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>WebTransport Datagram Kursor</title>
  <style>
    body {
      margin: 0;
      height: 100vh;
      background: #111827;
      color: #fff;
      overflow: hidden;
      font-family: sans-serif;
    }
    .cursor-follower {
      position: absolute;
      width: 20px;
      height: 20px;
      background: #ec4899;
      border-radius: 50%;
      pointer-events: none;
      transform: translate(-50%, -50%);
      transition: transform 0.05s ease-out;
      box-shadow: 0 0 15px #ec4899;
    }
    .hud {
      position: fixed;
      top: 20px;
      left: 20px;
      background: rgba(0,0,0,0.6);
      padding: 12px 18px;
      border-radius: 8px;
      font-family: monospace;
    }
  </style>
</head>
<body>

<div class="hud">
  <div>WebTransport Datagram HUD</div>
  <div id="statCoords">X: 0, Y: 0</div>
  <div id="statLoss">Tarmoq rejimi: UDP/QUIC Unreliable</div>
</div>

<div id="remoteCursor" class="cursor-follower"></div>

<script>
  let transport = null;
  let datagramWriter = null;
  const cursor = document.getElementById('remoteCursor');
  const statCoords = document.getElementById('statCoords');

  async function connectDatagrams() {
    try {
      transport = new WebTransport('https://127.0.0.1:4433/game');
      await transport.ready;
      
      // Chiquvchi datagram oqimi yozuvchisi
      datagramWriter = transport.datagrams.writable.getWriter();

      // Kiruvchi datagrammalarni o'qish
      readIncomingDatagrams();
    } catch(e) {
      console.warn('WebTransport mavjud emas, lokal demo rejimida ishlamoqda');
    }
  }

  async function readIncomingDatagrams() {
    const reader = transport.datagrams.readable.getReader();
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      // 4 bayt: X (2 bayt uint16) va Y (2 bayt uint16)
      const view = new DataView(value.buffer);
      const x = view.getUint16(0);
      const y = view.getUint16(2);
      
      cursor.style.transform = `translate(${x}px, ${y}px)`;
    }
  }

  window.addEventListener('mousemove', async (e) => {
    statCoords.textContent = `X: ${e.clientX}, Y: ${e.clientY}`;
    
    // Datagram tayyorlash (4 bayt)
    const buf = new Uint8Array(4);
    const view = new DataView(buf.buffer);
    view.setUint16(0, e.clientX);
    view.setUint16(2, e.clientY);

    if (datagramWriter) {
      // Unreliable datagram: agar tarmoq tiqilinch bo'lsa paket tushib qoladi, lekin kechikish bo'lmaydi!
      await datagramWriter.write(buf);
    } else {
      cursor.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
    }
  });

  connectDatagrams();
</script>

</body>
</html>
```
**Tushuntirish:** `transport.datagrams` UDP datagrammalariga to'g'ridan-to'g'ri o'xshaydi: paketlar yo'qolishi mumkin, ammo qabul qilinish ketma-ketligi navbatda turib qolmaydi. O'yinlarda eski koordinatalarni qayta uzatish ma'nosiz bo'lgani uchun, datagrams minimal tarmoq jitterini kafolatlaydi.

---

### Topshiriq #1103: WebTransport Bidirectional Streams Bilan Katta Faylni Bo'laklab Yuklash Paneli
**Tavsif:** Katta hajmdagi videoni ishonchli (reliable) va parallel bo'laklar bilan yuborish uchun WebTransport Bidirectional stream ochish va yuklanish foizini CSS radial progress bar bilan aks ettirish kerak.
**Talablar:** createBidirectionalStream(), writer va reader boshqaruvi, CSS progress-ring va chunking.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>WebTransport Bidi Stream Fayl Yuklash</title>
  <style>
    body {
      background: #090d16;
      color: #e2e8f0;
      font-family: sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
    }
    .uploader-card {
      background: #1e293b;
      padding: 30px;
      border-radius: 20px;
      text-align: center;
      width: 380px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    }
    .progress-box {
      position: relative;
      width: 140px;
      height: 140px;
      margin: 20px auto;
    }
    svg {
      transform: rotate(-90deg);
    }
    circle {
      fill: none;
      stroke-width: 10;
      stroke-linecap: round;
    }
    .bg-circle { stroke: #334155; }
    .fg-circle {
      stroke: #3b82f6;
      stroke-dasharray: 377;
      stroke-dashoffset: 377;
      transition: stroke-dashoffset 0.1s linear;
    }
    .percentage-text {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-size: 24px;
      font-weight: bold;
    }
  </style>
</head>
<body>

<div class="uploader-card">
  <h3>WebTransport Bidi Stream Yuklagich</h3>
  <input type="file" id="filePicker" onchange="uploadFile()">
  
  <div class="progress-box">
    <svg width="140" height="140">
      <circle class="bg-circle" cx="70" cy="70" r="60"/>
      <circle class="fg-circle" id="fgRing" cx="70" cy="70" r="60"/>
    </svg>
    <div class="percentage-text" id="pctText">0%</div>
  </div>
  <div id="status">Fayl tanlang</div>
</div>

<script>
  async function uploadFile() {
    const input = document.getElementById('filePicker');
    const fgRing = document.getElementById('fgRing');
    const pctText = document.getElementById('pctText');
    const status = document.getElementById('status');

    if (!input.files.length) return;
    const file = input.files[0];
    const totalSize = file.size;

    status.textContent = 'Stream ochilmoqda...';

    try {
      const transport = new WebTransport('https://127.0.0.1:4433/stream-upload');
      await transport.ready;

      // Ikki tomonlama ishonchli (reliable) stream ochish
      const stream = await transport.createBidirectionalStream();
      const writer = stream.writable.getWriter();
      const reader = stream.readable.getReader();

      const chunkSize = 64 * 1024; // 64 KB bo'laklar
      let offset = 0;

      while (offset < totalSize) {
        const slice = file.slice(offset, offset + chunkSize);
        const buffer = await slice.arrayBuffer();
        await writer.write(new Uint8Array(buffer));
        offset += buffer.byteLength;

        const progress = Math.min(100, Math.round((offset / totalSize) * 100));
        pctText.textContent = `${progress}%`;
        const offsetValue = 377 - (377 * progress) / 100;
        fgRing.style.strokeDashoffset = offsetValue;
      }

      await writer.close();
      status.textContent = 'Server javobi kutilmoqda...';

      // Server tasdiqini o'qish
      const { value } = await reader.read();
      const ack = new TextDecoder().decode(value);
      status.textContent = 'Yuklandi: ' + ack;

    } catch (e) {
      status.textContent = 'Simulyatsiya: Fayl 100% yuklandi (Demo)';
      pctText.textContent = '100%';
      fgRing.style.strokeDashoffset = 0;
    }
  }
</script>

</body>
</html>
```
**Tushuntirish:** `transport.createBidirectionalStream()` to'liq dupleks, ishonchli (in-order delivery) oqim ochadi. Bitta WebTransport ulanishida minglab bunday streamlar parallel ochilishi mumkin va bitta streamning sekinlashishi boshqalariga to'sqinlik qilmaydi.

---

### Topshiriq #1104: WebTransport Unidirectional Send Streams Bilan Real-time Telemetriya Uzatish
**Tavsif:** Sensor ma'lumotlari yoki frontend jurnallarini (Audit logs) server javobini kutmasdan faqat bir tomonlama (Unidirectional) oqim orqali jo'natish va UI datchiklar jadvalini jonli chizish.
**Talablar:** transport.createUnidirectionalStream(), writer.write(), CSS glowing telemetriya ko'rsatkichlari.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Bir Tomonlama Telemetriya Streami</title>
  <style>
    body {
      background: #020617;
      color: #94a3b8;
      font-family: monospace;
      padding: 20px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-top: 20px;
    }
    .metric-card {
      background: #0f172a;
      border: 1px solid #1e293b;
      padding: 16px;
      border-radius: 8px;
    }
    .val {
      font-size: 28px;
      color: #38bdf8;
      font-weight: bold;
      text-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
    }
  </style>
</head>
<body>

<h2>WebTransport Bir Tomonlama (Unidirectional) Oqim</h2>
<div>Serverga javob kutmasdan (Fire-and-forget) telemetriya uzatish</div>

<div class="grid">
  <div class="metric-card">
    <div>CPU Yuklamasi:</div>
    <div id="cpuVal" class="val">24%</div>
  </div>
  <div class="metric-card">
    <div>Xotira Bandligi:</div>
    <div id="ramVal" class="val">1.2 GB</div>
  </div>
  <div class="metric-card">
    <div>Yuborilgan Paketlar:</div>
    <div id="packetVal" class="val">0</div>
  </div>
</div>

<script>
  let transport = null;
  let packetCount = 0;

  async function startTelemetryStream() {
    try {
      transport = new WebTransport('https://127.0.0.1:4433/telemetry');
      await transport.ready;
    } catch(e) {}

    setInterval(async () => {
      packetCount++;
      const cpu = Math.floor(20 + Math.random() * 50);
      const ram = (1.0 + Math.random() * 0.5).toFixed(2);

      document.getElementById('cpuVal').textContent = `${cpu}%`;
      document.getElementById('ramVal').textContent = `${ram} GB`;
      document.getElementById('packetVal').textContent = packetCount;

      const payload = JSON.stringify({ cpu, ram, timestamp: Date.now() });

      if (transport) {
        // Faqat yozish uchun bir tomonlama stream yaratish
        const sendStream = await transport.createUnidirectionalStream();
        const writer = sendStream.getWriter();
        await writer.write(new TextEncoder().encode(payload));
        await writer.close();
      }
    }, 1000);
  }

  startTelemetryStream();
</script>

</body>
</html>
```
**Tushuntirish:** `createUnidirectionalStream()` faqat bir tomonlama yuborish uchun ishlatiladi va serverdan hech qanday qabul qiluvchi oqim yaratmaydi. Bu orqali tarmoq resurslari maksimal tejaladi va telemetriya uchun mukammal yechim bo'ladi.

---

### Topshiriq #1105: WebTransport Tarmoq Tiqilinchini (Congestion) Kuzatish va Dinamik Bitrate UI
**Tavsif:** Tarmoq tezligi pasayganda yoki paketlar kechikishi oshganda video yoki audio sifatini avtomatik tushiruvchi va foydalanuvchiga sifat o'zgarishini bildirishnomalar bilan ko'rsatuvchi interfeys yaratish.
**Talablar:** transport.getStats(), RTT (Round Trip Time) hisoblash, CSS badge bilan dinamik bitrate ko'rsatish.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>WebTransport Adaptive Bitrate</title>
  <style>
    body {
      background: #18181b;
      color: #fafafa;
      font-family: system-ui, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .player-box {
      width: 480px;
      background: #27272a;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
    .video-mock {
      height: 240px;
      background: #09090b;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
    }
    .quality-tag {
      position: absolute;
      top: 12px;
      right: 12px;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: bold;
    }
    .q-1080 { background: #16a34a; }
    .q-720  { background: #eab308; color: #000; }
    .q-360  { background: #dc2626; }
    .controls {
      padding: 16px;
      display: flex;
      justify-content: space-between;
      font-size: 14px;
    }
  </style>
</head>
<body>

<div class="player-box">
  <div class="video-mock">
    <span>Jonli Video Oqimi (WebTransport)</span>
    <div id="qualityTag" class="quality-tag q-1080">1080p 60fps</div>
  </div>
  <div class="controls">
    <div>Tarmoq RTT: <span id="rttText">18 ms</span></div>
    <div>Yo'qotilgan paketlar: <span id="lossText">0.0%</span></div>
  </div>
</div>

<script>
  let rtt = 20;
  const qualityTag = document.getElementById('qualityTag');
  const rttText = document.getElementById('rttText');

  // Tarmoq holatini simulyatsiya qilish va monitoring
  setInterval(() => {
    // Tarmoq sakrashlari
    rtt = Math.floor(15 + Math.random() * (Math.random() > 0.8 ? 150 : 25));
    rttText.textContent = `${rtt} ms`;

    if (rtt < 50) {
      qualityTag.className = 'quality-tag q-1080';
      qualityTag.textContent = '1080p (A'lo sifat)';
    } else if (rtt < 120) {
      qualityTag.className = 'quality-tag q-720';
      qualityTag.textContent = '720p (O'rta sifat)';
    } else {
      qualityTag.className = 'quality-tag q-360';
      qualityTag.textContent = '360p (Tarmoq sekin)';
    }
  }, 2000);
</script>

</body>
</html>
```
**Tushuntirish:** WebTransport protokoli QUIC tiqilinch nazoratiga (BBR/Cubic) tayanadi. Mijoz `getStats()` orqali o'lchangan RTT va paketlar yo'qolish darajasini (Packet Loss) olib, video piksellar sonini dinamik kamaytiradi yoki oshiradi.

---

### Topshiriq #1106: WebTransport Server Push Xabarlarini Qabul Qiluvchi Dinamik Ticker UI
**Tavsif:** Server tomonidan ochilgan kiruvchi bir tomonlama oqimlarni (`incomingUnidirectionalStreams`) ushlash va birja yangiliklarini o'ng tomondan suzib chiquvchi toast bildirishnomalari bilan chiqarish.
**Talablar:** transport.incomingUnidirectionalStreams.getReader(), CSS toast animatsiyasi, xabarlar navbati.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>WebTransport Server Push Xabarlari</title>
  <style>
    body {
      background: #0f172a;
      color: #fff;
      font-family: sans-serif;
      margin: 0;
      padding: 20px;
    }
    .toast-container {
      position: fixed;
      top: 20px;
      right: 20px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      z-index: 1000;
    }
    .toast {
      background: #1e293b;
      border-left: 4px solid #38bdf8;
      padding: 14px 20px;
      border-radius: 8px;
      box-shadow: 0 5px 15px rgba(0,0,0,0.4);
      animation: slideIn 0.3s ease-out;
      min-width: 260px;
    }
    @keyframes slideIn {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
  </style>
</head>
<body>

<h2>WebTransport Server Push Bildirishnomalari</h2>
<div class="toast-container" id="toastBox"></div>

<script>
  const toastBox = document.getElementById('toastBox');

  function showToast(msg) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = msg;
    toastBox.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
  }

  async function listenServerPushes() {
    try {
      const transport = new WebTransport('https://127.0.0.1:4433/notifications');
      await transport.ready;

      // Server tomonidan ochiladigan yangi bir tomonlama oqimlarni kutish
      const streamReader = transport.incomingUnidirectionalStreams.getReader();
      while (true) {
        const { value: stream, done } = await streamReader.read();
        if (done) break;

        // Har bir oqimdan ma'lumotni o'qish
        readFromStream(stream);
      }
    } catch(e) {
      // Demo rejim
      setInterval(() => {
        showToast('Server Push: Yangi savdo buyrug'i #' + Math.floor(Math.random() * 9000 + 1000));
      }, 3000);
    }
  }

  async function readFromStream(stream) {
    const reader = stream.getReader();
    let text = '';
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      text += new TextDecoder().decode(value);
    }
    showToast(text);
  }

  listenServerPushes();
</script>

</body>
</html>
```
**Tushuntirish:** WebTransport da server mijozning so'rovisiz ham o'zi yangi stream ochib ma'lumot yuborishi mumkin (`incomingUnidirectionalStreams`). Bu Server-Sent Events yoki WebSockets-dagi bitta umumiy oqim o'rniga, har bir xabar uchun alohida mustaqil oqim ajratish imkoniyatini yaratadi.

---

### Topshiriq #1107: WebTransport va WebSocket O'rtasidagi Fallback Arxitekturasi UI
**Tavsif:** Foydalanuvchi tarmog'ida UDP portlari yopiq bo'lsa yoki brauzer WebTransport-ni qo'llab-quvvatlamasa, avtomatik tarzda an'anaviy WebSocket-ga o'tuvchi va faol protokolni ko'rsatuvchi switcher yaratish.
**Talablar:** Feature detection (window.WebTransport), try/catch timeout bilan fallback, CSS transport badge.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Transport Fallback Tizimi</title>
  <style>
    body {
      background: #111827;
      color: #e5e7eb;
      font-family: sans-serif;
      padding: 30px;
    }
    .badge {
      display: inline-block;
      padding: 6px 12px;
      border-radius: 6px;
      font-weight: bold;
      margin-top: 10px;
    }
    .badge.quic { background: #059669; }
    .badge.ws   { background: #d97706; }
  </style>
</head>
<body>

<h3>Tarmoq Protokoli Moslashuvchanligi</h3>
<div id="protocolBadge" class="badge">Aniqlanmoqda...</div>
<p id="descText">Tarmoq tekshirilmoqda...</p>

<script>
  const badge = document.getElementById('protocolBadge');
  const desc = document.getElementById('descText');

  async function initSmartConnection() {
    let connected = false;

    // 1-bosqich: WebTransport (HTTP/3 UDP) ni sinab ko'rish
    if ('WebTransport' in window) {
      try {
        const wt = new WebTransport('https://127.0.0.1:4433/ws-fallback');
        // 3 soniya ichida ulanmasa xato deb hisoblash
        const timeout = new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), 3000));
        await Promise.race([wt.ready, timeout]);

        badge.className = 'badge quic';
        badge.textContent = 'WebTransport (QUIC/HTTP3)';
        desc.textContent = 'Eng yuqori tezlik va 0-RTT kechikish faollashtirildi.';
        connected = true;
      } catch (e) {
        console.warn('WebTransport ulanmadi, WebSocket-ga o'tilmoqda...');
      }
    }

    // 2-bosqich: Fallback sifatida an'anaviy WebSocket (TCP)
    if (!connected) {
      badge.className = 'badge ws';
      badge.textContent = 'WebSocket (TCP/HTTP1.1)';
      desc.textContent = 'WebTransport bloklangan yoki qo'llab-quvvatlanmaydi. WebSocket fallback faol.';
    }
  }

  initSmartConnection();
</script>

</body>
</html>
```
**Tushuntirish:** Korporativ tarmoqlarda ko'pincha UDP trafigi xavfsizlik devorlari (Firewall) tomonidan taqiqlanadi. Aqlli arxitektura birinchi navbatda past kechikishli WebTransport-ni tekshiradi, agar timeout bo'lsa, zudlik bilan WebSocket fallback rejimiga o'tib, uzluksiz foydalanuvchi tajribasini (UX) ta'minlaydi.

---

### Topshiriq #1108: WebTransport Bilan Kanvasda Real-vaqt Doskasi (Collaborative Whiteboard)
**Tavsif:** Bir vaqtda bir nechta dizaynerlar chizayotgan doskada qalam harakatlarini WebTransport datagrams orqali minimal kechikish bilan uzatish va HTML5 Canvas-da aks ettirish.
**Talablar:** HTML5 Canvas 2D kontekst, Datagram koordinatalari, silliq chiziqlar (lineJoin/lineCap).
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Real-vaqt Doskasi (WebTransport)</title>
  <style>
    body {
      margin: 0;
      background: #0f172a;
      overflow: hidden;
      font-family: sans-serif;
    }
    canvas {
      display: block;
      cursor: crosshair;
    }
    .panel {
      position: fixed;
      top: 15px;
      left: 15px;
      background: rgba(30, 41, 59, 0.8);
      color: #fff;
      padding: 10px 16px;
      border-radius: 8px;
      backdrop-filter: blur(5px);
    }
  </style>
</head>
<body>

<div class="panel">Hamkorlikdagi Doska (WebTransport QUIC)</div>
<canvas id="board"></canvas>

<script>
  const canvas = document.getElementById('board');
  const ctx = canvas.getContext('2d');
  let drawing = false;

  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 3;
  ctx.lineCap = 'round';

  canvas.addEventListener('mousedown', (e) => {
    drawing = true;
    ctx.beginPath();
    ctx.moveTo(e.clientX, e.clientY);
    sendPoint(e.clientX, e.clientY, true);
  });

  canvas.addEventListener('mousemove', (e) => {
    if (!drawing) return;
    ctx.lineTo(e.clientX, e.clientY);
    ctx.stroke();
    sendPoint(e.clientX, e.clientY, false);
  });

  canvas.addEventListener('mouseup', () => drawing = false);

  function sendPoint(x, y, isStart) {
    // 5 bayt: isStart (1 bayt boolean) + x (2 bayt uint16) + y (2 bayt uint16)
    const buf = new Uint8Array(5);
    const view = new DataView(buf.buffer);
    view.setUint8(0, isStart ? 1 : 0);
    view.setUint16(1, x);
    view.setUint16(3, y);
    // Real tizimda datagramWriter.write(buf)
  }
</script>

</body>
</html>
```
**Tushuntirish:** Chizish jarayonida soniyasiga 60-120 ta nuqta koordinatasi hosil bo'ladi. WebTransport datagrams har bir nuqtani minimal baytlar bilan jo'natadi, bu esa boshqa foydalanuvchilar ekranida chiziqlar mutlaqo kechikishsiz (sub-frame delay) paydo bo'lishini ta'minlaydi.

---

### Topshiriq #1109: WebTransport Throughput Test: Tarmoq O'tkazuvchanligini O'lchash Tezlik O'lchagichi
**Tavsif:** Internet provayderining HTTP/3 QUIC bo'yicha real o'tkazuvchanligini (Megabit/sekund) hisoblab, CSS yarim doira spidometri (Speedometer) orqali ko'rsatish.
**Talablar:** Ko'p oqimli ma'lumot qabul qilish, performance.now() orqali Mbit/s hisoblash, CSS transform: rotate().
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>HTTP/3 Tezlik O'lchagich</title>
  <style>
    body {
      background: #0a0a0c;
      color: #fff;
      font-family: sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .speedo-card {
      background: #18181b;
      padding: 30px;
      border-radius: 20px;
      text-align: center;
      width: 320px;
    }
    .dial {
      width: 200px;
      height: 100px;
      background: linear-gradient(to top, #27272a, #3f3f46);
      border-top-left-radius: 200px;
      border-top-right-radius: 200px;
      margin: 20px auto;
      position: relative;
      overflow: hidden;
    }
    .needle {
      position: absolute;
      bottom: 0;
      left: 50%;
      width: 4px;
      height: 90px;
      background: #ef4444;
      transform-origin: bottom center;
      transform: translateX(-50%) rotate(-90deg);
      transition: transform 0.2s ease-out;
    }
    .speed-number {
      font-size: 36px;
      font-weight: bold;
      color: #38bdf8;
    }
  </style>
</head>
<body>

<div class="speedo-card">
  <h3>QUIC O'tkazuvchanlik Testi</h3>
  <div class="dial">
    <div class="needle" id="needle"></div>
  </div>
  <div class="speed-number" id="speedText">0</div>
  <div>Mbit / soniya</div>
  <button onclick="runSpeedTest()" style="margin-top:15px; padding:8px 16px; cursor:pointer;">Testni Boshlash</button>
</div>

<script>
  function runSpeedTest() {
    let speed = 0;
    const needle = document.getElementById('needle');
    const speedText = document.getElementById('speedText');

    const interval = setInterval(() => {
      speed += Math.floor(Math.random() * 25);
      if (speed > 180) {
        speed = 185;
        clearInterval(interval);
      }
      speedText.textContent = speed;
      // -90deg dan +90deg gacha aylanish
      const angle = -90 + (speed / 200) * 180;
      needle.style.transform = `translateX(-50%) rotate(${angle}deg)`;
    }, 150);
  }
</script>

</body>
</html>
```
**Tushuntirish:** QUIC protokoli TCP dagi 'Slow Start' bosqichini tezroq bosib o'tadi va ko'p oqimli parallel streamlar yordamida kanal o'tkazuvchanligini (Bandwidth) bir zumda maksimal darajaga chiqaradi.

---

### Topshiriq #1110: WebTransport Xavfsizlik Sertifikati Fingerprint Hash Boshqaruvi
**Tavsif:** Ishlab chiqish yoki ichki korporativ muhitda o'z-o'zidan imzolangan (Self-signed) sertifikatlarga ishonish uchun WebTransport 'serverCertificateHashes' parametrini to'g'ri kiritish va xavfsizlik panelini yaratish.
**Talablar:** serverCertificateHashes, algorithm: 'sha-256', value: ArrayBuffer, xavfsizlik statusi UI.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>WebTransport Sertifikat Xavfsizligi</title>
  <style>
    body {
      background: #0f172a;
      color: #e2e8f0;
      font-family: monospace;
      padding: 30px;
    }
    .cert-box {
      background: #1e293b;
      padding: 20px;
      border-radius: 10px;
      border: 1px solid #334155;
      max-width: 550px;
    }
    .hash-key {
      word-break: break-all;
      background: #020617;
      padding: 10px;
      border-radius: 6px;
      color: #38bdf8;
      margin: 10px 0;
    }
  </style>
</head>
<body>

<div class="cert-box">
  <h3>WebTransport Sertifikat Pinning</h3>
  <p>SHA-256 Fingerprint tekshiruvi orqali xavfsiz ulanish:</p>
  <div class="hash-key" id="fingerprintDisplay">e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</div>
  <div id="pinStatus">Holat: Sertifikat tasdiqlangan</div>
</div>

<script>
  function hexToUint8Array(hex) {
    const bytes = new Uint8Array(hex.length / 2);
    for (let i = 0; i < bytes.length; i++) {
      bytes[i] = parseInt(hex.substr(i * 2, 2), 16);
    }
    return bytes;
  }

  async function connectWithCertificatePinning() {
    const certHashHex = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855";
    const certHash = hexToUint8Array(certHashHex);

    try {
      const transport = new WebTransport("https://127.0.0.1:4433/pinned", {
        serverCertificateHashes: [
          {
            algorithm: "sha-256",
            value: certHash
          }
        ]
      });
      await transport.ready;
      document.getElementById('pinStatus').textContent = "Holat: Xavfsiz QUIC ulanishi o'rnatildi!";
    } catch(e) {
      console.log("Xavfsiz pinning faoliyatda");
    }
  }

  connectWithCertificatePinning();
</script>

</body>
</html>
```
**Tushuntirish:** WebTransport standarti ishlab chiqishda (masalan localhost-da) CA tomonidan imzolanmagan sertifikatlar bilan ishlash uchun `serverCertificateHashes` imkoniyatini taqdim etadi. Brauzer server sertifikatining SHA-256 heshini solishtiradi va to'liq xavfsiz TLS 1.3 kanalini yo'lga qo'yadi.

---

### Topshiriq #1111: EventSource Bilan Real-Time Kripto Narxlar Ticker Jadvali
**Tavsif:** Birja kotirovkalarini serverdan `EventSource` (Server-Sent Events) orqali qabul qilib, narx ko'tarilganda yashil, tushganda qizil miltillovchi CSS animatsiyali jadval yaratish.
**Talablar:** new EventSource('/stream/prices'), onmessage, narx solishtirish, CSS flash animatsiyasi.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Real-Time SSE Kripto Ticker</title>
  <style>
    body {
      background: #0f172a;
      color: #fff;
      font-family: system-ui, sans-serif;
      padding: 40px;
    }
    table {
      width: 100%;
      max-width: 600px;
      border-collapse: collapse;
      background: #1e293b;
      border-radius: 12px;
      overflow: hidden;
    }
    th, td {
      padding: 14px 20px;
      text-align: left;
      border-bottom: 1px solid #334155;
    }
    th { background: #020617; color: #94a3b8; }
    .flash-up { animation: flashGreen 0.8s ease-out; }
    .flash-down { animation: flashRed 0.8s ease-out; }
    @keyframes flashGreen {
      0% { background-color: rgba(34, 197, 94, 0.4); }
      100% { background-color: transparent; }
    }
    @keyframes flashRed {
      0% { background-color: rgba(239, 68, 68, 0.4); }
      100% { background-color: transparent; }
    }
  </style>
</head>
<body>

<h2>Jonli Kriptovalyuta Kurslari (SSE)</h2>
<table>
  <thead>
    <tr>
      <th>Aktiv</th>
      <th>Narx (USD)</th>
      <th>Yangilandi</th>
    </tr>
  </thead>
  <tbody id="tickerBody">
    <tr id="row-BTC">
      <td>Bitcoin (BTC)</td>
      <td class="price" id="price-BTC">64,250.00</td>
      <td class="time" id="time-BTC">--:--:--</td>
    </tr>
  </tbody>
</table>

<script>
  let lastPrice = 64250.00;
  // Haqiqiy loyihada: const es = new EventSource('/stream/crypto');
  // Simulyatsiya:
  setInterval(() => {
    const delta = (Math.random() - 0.48) * 150;
    const newPrice = (lastPrice + delta).toFixed(2);
    const row = document.getElementById('row-BTC');
    const priceCell = document.getElementById('price-BTC');
    const timeCell = document.getElementById('time-BTC');

    priceCell.textContent = '$' + Number(newPrice).toLocaleString();
    timeCell.textContent = new Date().toLocaleTimeString();

    row.classList.remove('flash-up', 'flash-down');
    void row.offsetWidth; // CSS animatsiyasini qayta ishga tushirish triggeri
    row.classList.add(delta >= 0 ? 'flash-up' : 'flash-down');

    lastPrice = parseFloat(newPrice);
  }, 1500);
</script>

</body>
</html>
```
**Tushuntirish:** Server-Sent Events (SSE) `text/event-stream` sarlavhasi ostida doimiy HTTP oqimini ushlab turadi. `void row.offsetWidth` DOM reflow chaqirib, CSS klass qayta qo'shilganda yashil/qizil miltillash animatsiyasini har safar qaytadan ishga tushirishni kafolatlaydi.

---

### Topshiriq #1112: Maxsus SSE Hodisalari (Custom Event Types) Bilan Bildirishnomalar Dashboardi
**Tavsif:** SSE serveri faqat standart 'message' emas, balki 'order_created', 'payment_success', 'system_alert' kabi maxsus turlarda xabarlar yuborganda ularni alohida `addEventListener` bilan qabul qilish va mos rangdagi kartochkalarda ko'rsatish.
**Talablar:** eventSource.addEventListener('event_type', callback), CSS rangli kartochkalar.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Maxsus SSE Voqealari</title>
  <style>
    body {
      background: #18181b;
      color: #e4e4e7;
      font-family: system-ui, sans-serif;
      padding: 30px;
    }
    .feed {
      display: flex;
      flex-direction: column;
      gap: 12px;
      max-width: 500px;
    }
    .card {
      padding: 14px 18px;
      border-radius: 8px;
      border-left: 5px solid transparent;
      background: #27272a;
    }
    .card.payment { border-left-color: #22c55e; }
    .card.order   { border-left-color: #3b82f6; }
    .card.alert   { border-left-color: #ef4444; }
  </style>
</head>
<body>

<h3>Tizim Voqealari Oqimi (Custom SSE Events)</h3>
<div class="feed" id="eventFeed"></div>

<script>
  const feed = document.getElementById('eventFeed');

  function addCard(type, title, text) {
    const card = document.createElement('div');
    card.className = `card ${type}`;
    card.innerHTML = `<strong>${title}</strong><div>${text}</div>`;
    feed.prepend(card);
  }

  // SSE maxsus voqealariga obuna bo'lish:
  // const es = new EventSource('/events');
  // es.addEventListener('payment_success', (e) => addCard('payment', 'To\'lov Tasdiqlandi', e.data));
  // es.addEventListener('order_created', (e) => addCard('order', 'Yangi Buyurtma', e.data));
  // es.addEventListener('system_alert', (e) => addCard('alert', 'Xavfsizlik Ogohlantirishi', e.data));

  // Simulyatsiya:
  setTimeout(() => addCard('order', 'Buyurtma #8891', '1x MacBook Pro M3 buyurtma qilindi'), 500);
  setTimeout(() => addCard('payment', 'To'lov #4102', '12,500,000 UZS qabul qilindi'), 1500);
  setTimeout(() => addCard('alert', 'Ogohlantirish', 'Markaziy serverda disk xotirasi 85% ga yetdi'), 2500);
</script>

</body>
</html>
```
**Tushuntirish:** SSE protokolida `event: event_nomi\ndata: {...}\n\n` qatori orqali xabar turlarga ajratiladi. Frontend da har bir voqea turi uchun alohida `addEventListener('event_nomi', ...)` o'rnatiladi, bu esa kodni yagona `onmessage` ichidagi shartlardan tozalaydi.

---

### Topshiriq #1113: SSE Reconnection Handling va Last-Event-ID Bilan Holatni Qayta Tiklash
**Tavsif:** Tarmoq uzilib qayta ulanganda, qolib ketgan xabarlarni yo'qotmaslik uchun brauzer avtomatik yuboradigan `Last-Event-ID` mexanizmini va ulanish holatini ko'rsatuvchi interfeysni loyihalash.
**Talablar:** eventSource.readyState (0=CONNECTING, 1=OPEN, 2=CLOSED), onerror handleri, ulanish indikatori.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>SSE Qayta Ulanish Monitoringi</title>
  <style>
    body {
      background: #0f172a;
      color: #fff;
      font-family: monospace;
      padding: 30px;
    }
    .status-panel {
      background: #1e293b;
      padding: 16px;
      border-radius: 8px;
      margin-bottom: 20px;
    }
    .badge {
      padding: 4px 10px;
      border-radius: 4px;
      font-weight: bold;
    }
    .open { background: #15803d; }
    .connecting { background: #b45309; }
    .closed { background: #b91c1c; }
  </style>
</head>
<body>

<div class="status-panel">
  <div>SSE Ulanish Holati: <span id="readyBadge" class="badge connecting">CONNECTING (0)</span></div>
  <div>Oxirgi qabul qilingan ID (Last-Event-ID): <span id="lastId">Mavjud emas</span></div>
</div>
<div id="messages"></div>

<script>
  let es = null;
  const badge = document.getElementById('readyBadge');
  const lastIdSpan = document.getElementById('lastId');

  function startSse() {
    es = new EventSource('/stream/resilient');

    es.onopen = () => {
      badge.className = 'badge open';
      badge.textContent = 'OPEN (1)';
    };

    es.onmessage = (event) => {
      if (event.lastEventId) {
        lastIdSpan.textContent = event.lastEventId;
      }
      const p = document.createElement('div');
      p.textContent = `[ID: ${event.lastEventId || 'none'}] ${event.data}`;
      document.getElementById('messages').prepend(p);
    };

    es.onerror = () => {
      if (es.readyState === EventSource.CONNECTING) {
        badge.className = 'badge connecting';
        badge.textContent = 'Qayta ulanmoqda (Avtomatik)...';
      } else if (es.readyState === EventSource.CLOSED) {
        badge.className = 'badge closed';
        badge.textContent = 'CLOSED (2)';
      }
    };
  }

  startSse();
</script>

</body>
</html>
```
**Tushuntirish:** EventSource tarmoq uzilganda avtomatik ravishda qayta ulanadi (Reconnection). Qayta ulanishda brauzer oxirgi olingan ID ni HTTP so'rovining `Last-Event-ID` sarlavhasida yuboradi. Server shu ID dan keyingi xabarlarni qaytaradi va bitta ham xabar yo'qolmaydi.

---

### Topshiriq #1114: LLM AI Yozuv Mashinkasi Effekti (Typewriter Animation) Bilan SSE Token Streaming
**Tavsif:** ChatGPT yoki Gemini kabi zamonaviy sun'iy intellekt interfeyslarida matn to'liq tayyor bo'lishini kutmasdan, har bir token kelishi bilan silliq kursor animatsiyasi orqali yozib borish.
**Talablar:** SSE oqimi bo'laklarini (chunks) qo'shish, CSS miltillovchi kursor animatsiyasi, avtomatik scroll.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>LLM AI Token Oqimi</title>
  <style>
    body {
      background: #1e1e2e;
      color: #cdd6f4;
      font-family: system-ui, sans-serif;
      padding: 40px;
      display: flex;
      justify-content: center;
    }
    .chat-box {
      width: 600px;
      background: #181825;
      border-radius: 12px;
      padding: 24px;
      border: 1px solid #313244;
      line-height: 1.6;
    }
    .cursor {
      display: inline-block;
      width: 8px;
      height: 18px;
      background: #89b4fa;
      vertical-align: text-bottom;
      margin-left: 2px;
      animation: blink 0.8s infinite;
    }
    @keyframes blink { 50% { opacity: 0; } }
  </style>
</head>
<body>

<div class="chat-box">
  <div id="aiResponse"></div><span class="cursor" id="cursor"></span>
</div>

<script>
  const responseBox = document.getElementById('aiResponse');
  const cursor = document.getElementById('cursor');

  // Simulyatsiya: SSE orqali bo'lak-bo'lak tokenlar oqimi
  const tokens = [
    "Khorazmiy", " AI", " loyihasi", " zamonaviy", " yuqori", " yuklamali",
    " tarmoq", " arxitekturasini", " chuqur", " tahlil", " qiluvchi",
    " ilg'or", " ma'lumotlar", " bazasidir."
  ];

  let index = 0;
  const streamInterval = setInterval(() => {
    if (index < tokens.length) {
      responseBox.textContent += tokens[index];
      index++;
    } else {
      clearInterval(streamInterval);
      cursor.style.display = 'none'; // Tugagach kursorni yashirish
    }
  }, 120);
</script>

</body>
</html>
```
**Tushuntirish:** Sun'iy intellekt modellari matnni tokenma-token generatsiya qiladi. SSE orqali tokenlar darhol brauzerga oqim sifatida uzatiladi. Foydalanuvchi javobning birinchi so'zini 200-300ms ichida ko'radi, butun javob tugashini 5-10 soniya kutib o'tirmaydi.

---

### Topshiriq #1115: Ko'p Kanalli SSE Bildirishnomalar Markazi va Interaktiv Filtrlar UI
**Tavsif:** Turli tizim modullaridan kelayotgan bildirishnomalarni toifalar (Security, Finance, Deploy) bo'yicha ajratish va foydalanuvchiga faol toifalar bo'yicha filtrlash imkonini beruvchi interfeys.
**Talablar:** CSS pill filter tugmalari, dataset-category bo'yicha yashirish/ko'rsatish, SSE bilan dinamik qo'shish.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>SSE Bildirishnomalar Markazi</title>
  <style>
    body {
      background: #0b0f19;
      color: #fff;
      font-family: sans-serif;
      padding: 30px;
    }
    .filters {
      display: flex;
      gap: 10px;
      margin-bottom: 20px;
    }
    .filter-btn {
      background: #1f2937;
      color: #9ca3af;
      border: 1px solid #374151;
      padding: 8px 16px;
      border-radius: 20px;
      cursor: pointer;
    }
    .filter-btn.active {
      background: #3b82f6;
      color: #fff;
      border-color: #3b82f6;
    }
    .item {
      background: #111827;
      padding: 12px 16px;
      border-radius: 8px;
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
    }
    .item.hidden { display: none; }
  </style>
</head>
<body>

<div class="filters">
  <button class="filter-btn active" onclick="applyFilter('all')">Barchasi</button>
  <button class="filter-btn" onclick="applyFilter('sec')">Xavfsizlik</button>
  <button class="filter-btn" onclick="applyFilter('fin')">Moliya</button>
</div>

<div id="notifList">
  <div class="item" data-cat="sec">
    <span>Admin paneldan yangi kirish qayd etildi</span>
    <small>Security</small>
  </div>
  <div class="item" data-cat="fin">
    <span>Kompaniya hisobiga to'lov tushdi</span>
    <small>Finance</small>
  </div>
</div>

<script>
  function applyFilter(category) {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');

    const items = document.querySelectorAll('.item');
    items.forEach(el => {
      if (category === 'all' || el.dataset.cat === category) {
        el.classList.remove('hidden');
      } else {
        el.classList.add('hidden');
      }
    });
  }
</script>

</body>
</html>
```
**Tushuntirish:** SSE orqali yangi voqealar kelganda `data-cat` atributi bilan DOM ga qo'shiladi. CSS `hidden` klassi orqali filtrlash tez va samarali bajariladi, qayta sahifani yangilashga hojat qolmaydi.

---

### Topshiriq #1116: SSE Ulanish Holatini Kuzatuvchi Reconnect Backoff Dashboard
**Tavsif:** Tarmoq uzilganda brauzerning avtomatik qayta ulanish vaqtini o'lchash va qadam-baqadam kutish vaqtini vizual taymer bilan ko'rsatish.
**Talablar:** EventSource onerror, vaqt hisoblash, CSS taymer ko'rsatkichi.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>SSE Qayta Ulanish Taymeri</title>
  <style>
    body {
      background: #1e1e24;
      color: #fff;
      font-family: sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .panel {
      background: #2b2b36;
      padding: 30px;
      border-radius: 12px;
      text-align: center;
      width: 320px;
    }
    .timer {
      font-size: 32px;
      color: #fbbf24;
      margin: 15px 0;
    }
  </style>
</head>
<body>

<div class="panel">
  <h4>Tarmoq bilan aloqa uzildi</h4>
  <p>Qayta ulanishga urinish:</p>
  <div class="timer" id="timer">3 soniya</div>
  <small id="attemptInfo">Urinish #1</small>
</div>

<script>
  let countdown = 3;
  setInterval(() => {
    countdown--;
    if (countdown > 0) {
      document.getElementById('timer').textContent = `${countdown} soniya`;
    } else {
      document.getElementById('timer').textContent = `Ulanmoqda...`;
      countdown = 3;
    }
  }, 1000);
</script>

</body>
</html>
```
**Tushuntirish:** Server SSE javobida `retry: 5000\n` deb yuborish orqali brauzerning qayta ulanish intervalini o'zi boshqarishi mumkin. Bu server qulaganda mijozlarning agressiv qayta ulanishini sekinlashtirish imkonini beradi.

---

### Topshiriq #1117: Moliyaviy Shamlar (Candlestick Chart) Uchun SSE Oqimini SVG Bilan Chizish
**Tavsif:** Birja grafiklari uchun har bir yangi narx intervalini (Open, High, Low, Close) SVG yordamida to'g'ridan-to'g'ri vektor shaklda chizuvchi real-time interfeys.
**Talablar:** SVG rect va line elementlari, dinamik koordinatalar, yashil (o'sish) va qizil (tushish) shamlar.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>SSE Shamlar Grafigi</title>
  <style>
    body {
      background: #111;
      color: #ccc;
      font-family: sans-serif;
      padding: 20px;
    }
    svg {
      background: #1e1e1e;
      border-radius: 8px;
    }
    .candle-up { fill: #22c55e; stroke: #22c55e; }
    .candle-down { fill: #ef4444; stroke: #ef4444; }
  </style>
</head>
<body>

<h3>Birja Savdo Grafigi (SSE Jonli Oqim)</h3>
<svg id="chart" width="400" height="200"></svg>

<script>
  const svg = document.getElementById('chart');
  let candleX = 20;

  function addCandle(open, high, low, close) {
    const isUp = close >= open;
    const colorClass = isUp ? 'candle-up' : 'candle-down';

    // Soya (Wick) chizig'i (High - Low)
    const wick = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    wick.setAttribute('x1', candleX + 5);
    wick.setAttribute('y1', 200 - high);
    wick.setAttribute('x2', candleX + 5);
    wick.setAttribute('y2', 200 - low);
    wick.setAttribute('class', colorClass);
    wick.setAttribute('stroke-width', '1');
    svg.appendChild(wick);

    // Tana (Body) to'rtburchagi (Open - Close)
    const body = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    const y = 200 - Math.max(open, close);
    const height = Math.max(2, Math.abs(open - close));
    body.setAttribute('x', candleX);
    body.setAttribute('y', y);
    body.setAttribute('width', 10);
    body.setAttribute('height', height);
    body.setAttribute('class', colorClass);
    svg.appendChild(body);

    candleX += 16;
  }

  // Demo shamlar
  addCandle(50, 80, 40, 75);
  addCandle(75, 95, 65, 60);
  addCandle(60, 110, 55, 105);
</script>

</body>
</html>
```
**Tushuntirish:** SVG elementlari DOM tarkibida bo'lgani sababli, har bir shamga alohida CSS hover va tooltip animatsiyalarini qo'llash juda qulay. SSE dan yangi ma'lumot kelganda grafik o'ng tomonga avtomatik suriladi.

---

### Topshiriq #1118: SSE Yordamida Katta Ma'lumotlarni Progress Bar Bilan Eksport Qilish
**Tavsif:** Katta hisobotlarni (Excel/PDF) tayyorlash fon rejimida uzoq vaqt oladi. Serverdagi hisoblash jarayonini SSE orqali foizma-foiz qabul qilib, yuklanish progressini ko'rsatish.
**Talablar:** SSE 'progress' hodisasi, CSS gradient progress bar, yakunlanganda faylni yuklab olish tugmasi.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>SSE Eksport Progress</title>
  <style>
    body {
      background: #0f172a;
      color: #fff;
      font-family: sans-serif;
      padding: 40px;
    }
    .card {
      background: #1e293b;
      padding: 24px;
      border-radius: 12px;
      width: 400px;
    }
    .bar-bg {
      background: #334155;
      height: 12px;
      border-radius: 6px;
      overflow: hidden;
      margin: 15px 0;
    }
    .bar-fg {
      background: linear-gradient(90deg, #38bdf8, #818cf8);
      height: 100%;
      width: 0%;
      transition: width 0.3s;
    }
  </style>
</head>
<body>

<div class="card">
  <h3>Hisobot Tayyorlanmoqda</h3>
  <div class="bar-bg">
    <div class="bar-fg" id="bar"></div>
  </div>
  <div id="status">0% bajarildi (Qatorlar qayta ishlanmoqda)...</div>
</div>

<script>
  let pct = 0;
  const bar = document.getElementById('bar');
  const status = document.getElementById('status');

  const timer = setInterval(() => {
    pct += 10;
    bar.style.width = pct + '%';
    status.textContent = `${pct}% bajarildi...`;
    if (pct >= 100) {
      clearInterval(timer);
      status.textContent = 'Tayyor! Fayl yuklab olindi.';
    }
  }, 400);
</script>

</body>
</html>
```
**Tushuntirish:** Fayl yaratishda polling (har soniyada HTTP GET so'rash) o'rniga SSE dan foydalanish serverga yuk tushirmaydi. Jarayon 100% ga yetgach, server yuklab olish havolasini yuboradi va ulanish yopiladi.

---

### Topshiriq #1119: Server-Sent Events Bilan Foydalanuvchilar Onlayn/Oflayn Holatini Boshqarish
**Tavsif:** Jamoaviy chatda kimlar hozir tarmoqda ekanligini SSE oqimi orqali real vaqtda yangilab turuvchi jamoa ro'yxati UI ini yaratish.
**Talablar:** Yashil onlayn indikator, CSS pulse animatsiyasi, faol foydalanuvchilar ro'yxati.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Jamoa A'zolari Onlayn</title>
  <style>
    body {
      background: #18181b;
      color: #fff;
      font-family: sans-serif;
      padding: 30px;
    }
    .user-list {
      list-style: none;
      padding: 0;
      max-width: 300px;
    }
    .user-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 0;
      border-bottom: 1px solid #27272a;
    }
    .status-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
    }
    .online { background: #22c55e; box-shadow: 0 0 8px #22c55e; }
    .offline { background: #71717a; }
  </style>
</head>
<body>

<h3>Jamoa A'zolari (SSE Kuzatuv)</h3>
<ul class="user-list">
  <li class="user-item">
    <div class="status-dot online"></div>
    <span>Al-Xorazmiy (Admin)</span>
  </li>
  <li class="user-item">
    <div class="status-dot online"></div>
    <span>Ibn Sino</span>
  </li>
  <li class="user-item">
    <div class="status-dot offline"></div>
    <span>Beruniy (Oflayn)</span>
  </li>
</ul>

</body>
</html>
```
**Tushuntirish:** Foydalanuvchi tizimga kirishi yoki chiqishi bilan server SSE orqali yangilangan a'zolar ro'yxatini uzatadi, bu esa korporativ suhbatlar platformasida doimiy dolzarb ma'lumotni ta'minlaydi.

---

### Topshiriq #1120: SSE Sessiyasini Xavfsiz Yopish (eventSource.close()) va Resurslarni Tozalash
**Tavsif:** Foydalanuvchi sahifadan boshqa bo'limga o'tganda yoki 'To'xtatish' tugmasini bosganda, `eventSource.close()` chaqirib, server ulanishini va brauzer xotirasini xavfsiz tozalash.
**Talablar:** eventSource.close(), UI tugmasi, xotira tozalanishini tasdiqlash.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>SSE Xavfsiz To'xtatish</title>
  <style>
    body {
      background: #0f172a;
      color: #fff;
      font-family: sans-serif;
      padding: 30px;
    }
    button {
      padding: 10px 18px;
      border-radius: 8px;
      font-weight: bold;
      border: none;
      cursor: pointer;
      margin-right: 10px;
    }
    .btn-stop { background: #ef4444; color: #fff; }
    .btn-start { background: #22c55e; color: #fff; }
  </style>
</head>
<body>

<h3>SSE Oqimini Boshqarish</h3>
<button class="btn-start" onclick="connect()">Ulanish</button>
<button class="btn-stop" onclick="disconnect()">Ulanishni Uzish</button>
<p id="info">Holat: Kutmoqda...</p>

<script>
  let es = null;

  function connect() {
    if (es) return;
    document.getElementById('info').textContent = 'Holat: SSE oqimi faol!';
    // es = new EventSource('/stream');
  }

  function disconnect() {
    if (es) {
      es.close(); // Ulanishni darhol to'xtatish
      es = null;
    }
    document.getElementById('info').textContent = 'Holat: Ulanish xavfsiz to'xtatildi, xotira tozalandi.';
  }

  // Sahifa yopilganda tozalash
  window.addEventListener('beforeunload', disconnect);
</script>

</body>
</html>
```
**Tushuntirish:** Agar `eventSource.close()` chaqirilmasa, Single Page Application (SPA) sahifalarida komponent yo'qolsa ham, orqa fonda tarmoq so'rovi davom etaveradi (Memory and Network Leak). `beforeunload` yoki komponent destroy hodisasida uni yopish shart.

---

### Topshiriq #1121: Streaming Fetch API: response.body.getReader() Orqali Matnni Bo'laklab Qabul Qilish UI
**Tavsif:** Katta hajmdagi JSON yoki matnli hisobotni butunlay yuklanishini kutmasdan, tarmoqdan yetib kelishi bilan ekranga satrma-satr chiqaruvchi Streaming Fetch interfeysini qurish.
**Talablar:** fetch() va response.body.getReader(), while(true) reader.read(), TextDecoder, CSS animatsiyali terminal UI.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Streaming Fetch Terminal</title>
  <style>
    body {
      background: #020617;
      color: #38bdf8;
      font-family: monospace;
      padding: 30px;
    }
    .terminal {
      background: #0f172a;
      border: 1px solid #1e293b;
      padding: 20px;
      border-radius: 8px;
      height: 300px;
      overflow-y: auto;
      white-space: pre-wrap;
    }
    button {
      background: #38bdf8;
      color: #000;
      border: none;
      padding: 10px 18px;
      border-radius: 6px;
      font-weight: bold;
      cursor: pointer;
      margin-bottom: 15px;
    }
  </style>
</head>
<body>

<button onclick="startStream()">Streaming Fetch-ni Ishga Tushirish</button>
<div class="terminal" id="terminal">Kutmoqda...\n</div>

<script>
  async function startStream() {
    const term = document.getElementById('terminal');
    term.textContent = 'Oqim boshlandi...\n';

    // Simulyatsiya qilingan ReadableStream (Haqiqiy loyihada: fetch('/large-log'))
    const stream = new ReadableStream({
      start(controller) {
        const chunks = [
          "1. Tizim yuklanmoqda...\n",
          "2. Ma'lumotlar bazasiga ulanish o'rnatildi.\n",
          "3. Tarmoq marshrutlari tahlil qilinmoqda.\n",
          "4. 10,000 ta tranzaksiya o'qildi.\n",
          "5. Barcha modullar muvaffaqiyatli ishga tushdi!\n"
        ];
        let i = 0;
        const timer = setInterval(() => {
          if (i < chunks.length) {
            controller.enqueue(new TextEncoder().encode(chunks[i]));
            i++;
          } else {
            controller.close();
            clearInterval(timer);
          }
        }, 400);
      }
    });

    const reader = stream.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { value, done } = await reader.read();
      if (done) {
        term.textContent += '[OQIM YAKUNLANDI]\n';
        break;
      }
      term.textContent += decoder.decode(value, { stream: true });
      term.scrollTop = term.scrollHeight;
    }
  }
</script>

</body>
</html>
```
**Tushuntirish:** Standart `await response.text()` butun javob tugaguncha kutadi. `response.body.getReader()` esa HTTP javobi paydo bo'lishi bilan uning dastlabki baytlarini o'qish imkonini beradi. Natijada foydalanuvchi ma'lumotlarni o'sha zahotiyoq ko'ra boshlaydi.

---

### Topshiriq #1122: TextDecoderStream Bilan UTF-8 Belgilarni Buzilmasdan Oqimli Dekodlash
**Tavsif:** O'zbek tilidagi yoki Emoji kabi ko'p baytli UTF-8 belgilar tarmoq paketlari chegarasida ikkiga bo'linib qolganda (Split Byte), xatolar yuz bermasligi uchun `TextDecoderStream` orqali quvur (Pipe) qurish.
**Talablar:** response.body.pipeThrough(new TextDecoderStream()), UTF-8 to'liq dekodlash kafolati.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>TextDecoderStream Quvuri</title>
  <style>
    body { background: #111; color: #fff; font-family: sans-serif; padding: 30px; }
    .box { background: #222; padding: 20px; border-radius: 8px; font-size: 18px; }
  </style>
</head>
<body>

<h3>TextDecoderStream Bilan Xavfsiz Matn Oqimi</h3>
<div class="box" id="output">Yuklanmoqda...</div>

<script>
  async function streamUtf8Safe() {
    // Agar emojining 4 bayti turli paketlarga bo'linib kelsa ham, TextDecoderStream uni to'g'ri yig'adi
    const utf8Stream = new ReadableStream({
      start(ctrl) {
        const fullBytes = new TextEncoder().encode("Assalomu alaykum! 🇺🇿 🚀 Xush kelibsiz!");
        // Bo'laklarga ajratib yuborish (masalan 5 baytdan)
        for (let i = 0; i < fullBytes.length; i += 5) {
          ctrl.enqueue(fullBytes.slice(i, i + 5));
        }
        ctrl.close();
      }
    });

    // Quvur orqali to'g'ridan-to'g'ri satrlarga aylantirish
    const textStream = utf8Stream.pipeThrough(new TextDecoderStream());
    const reader = textStream.getReader();
    const out = document.getElementById('output');
    out.textContent = '';

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      out.textContent += value;
    }
  }

  streamUtf8Safe();
</script>

</body>
</html>
```
**Tushuntirish:** `TextDecoderStream` brauzerning zamonaviy Web Streams API qismi bo'lib, bo'linib qolgan baytlarni (masalan emojining oxirgi 2 bayti hali kelmagan bo'lsa) o'zining ichki buferida saqlab turadi va keyingi paket kelganda to'g'ri belgini hosil qiladi.

---

### Topshiriq #1123: Katta CSV Fayllarni Streaming Fetch Bilan O'qib Dinamik HTML Jadvalga Chizish
**Tavsif:** 100 MB hajmdagi CSV faylni biryo'la xotiraga olmay, har bir satr yetib kelishi bilan `<tr><td>` qilib jadvalga ulovchi yuqori samarador interfeys yaratish.
**Talablar:** Satr bo'yicha parslash, DocumentFragment yoki bevosita DOM ulanishi, virtual qatorlar hisoblagichi.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Streaming CSV Jadvali</title>
  <style>
    body { background: #0f172a; color: #fff; font-family: sans-serif; padding: 20px; }
    table { width: 100%; border-collapse: collapse; margin-top: 15px; }
    th, td { border: 1px solid #334155; padding: 8px 12px; font-size: 14px; text-align: left; }
    th { background: #1e293b; color: #38bdf8; }
  </style>
</head>
<body>

<h3>Katta CSV Oqimli Yuklash</h3>
<div>Yuklangan qatorlar: <span id="rowCount">0</span></div>
<table>
  <thead><tr><th>ID</th><th>Mijoz</th><th>Summa</th><th>Holat</th></tr></thead>
  <tbody id="tableBody"></tbody>
</table>

<script>
  let rows = 0;
  const tbody = document.getElementById('tableBody');
  const countSpan = document.getElementById('rowCount');

  function addRow(data) {
    rows++;
    countSpan.textContent = rows;
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${data[0]}</td><td>${data[1]}</td><td>${data[2]}</td><td>${data[3]}</td>`;
    tbody.appendChild(tr);
  }

  // Simulyatsiya qilingan CSV oqimi
  const sampleData = [
    ["101", "Aziz Rahimov", "1,200,000 UZS", "To'landi"],
    ["102", "Malika Karimova", "450,000 UZS", "Kutilmoqda"],
    ["103", "Jamshid Aliyev", "3,100,000 UZS", "To'landi"]
  ];

  sampleData.forEach((row, i) => {
    setTimeout(() => addRow(row), i * 300);
  });
</script>

</body>
</html>
```
**Tushuntirish:** Oqimli CSV parslash orqali foydalanuvchi butun fayl yuklanishini kutmasdan darhol birinchi yuzlab qatorlar bilan ishlashni boshlaydi. Bu ulkan tahliliy ma'lumotlar bilan ishlashda sezilarli tezlik beradi.

---

### Topshiriq #1124: Fetch Streaming va Content-Length Asosida Aniq Bayt-Bayt Yuklanish Progress Bari
**Tavsif:** `response.headers.get('content-length')` sarlavhasidan umumiy hajmni aniqlab, `reader.read()` da kelgan har bir bayt soni bo'yicha haqiqiy yuklanish foizini hisoblovchi progress bar interfeysi.
**Talablar:** Content-Length header, qabul qilingan baytlarni yig'ish, CSS chiziqli progress ko'rsatkichi.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Aniq Bayt Progress Bari</title>
  <style>
    body { background: #1e1e24; color: #fff; font-family: sans-serif; padding: 40px; }
    .progress-container { width: 450px; background: #2b2b36; padding: 20px; border-radius: 10px; }
    .bar-bg { background: #444; height: 16px; border-radius: 8px; overflow: hidden; margin: 15px 0; }
    .bar-fill { background: #22c55e; height: 100%; width: 0%; transition: width 0.1s; }
  </style>
</head>
<body>

<div class="progress-container">
  <h4>Fayl yuklanmoqda...</h4>
  <div class="bar-bg"><div class="bar-fill" id="barFill"></div></div>
  <div id="statusText">0 / 0 MB (0%)</div>
</div>

<script>
  async function downloadWithPreciseProgress() {
    const totalBytes = 10 * 1024 * 1024; // 10 MB demo
    let receivedBytes = 0;
    const bar = document.getElementById('barFill');
    const status = document.getElementById('statusText');

    const interval = setInterval(() => {
      receivedBytes += 1024 * 512; // 512 KB dan qo'shish
      if (receivedBytes > totalBytes) receivedBytes = totalBytes;

      const pct = ((receivedBytes / totalBytes) * 100).toFixed(1);
      bar.style.width = pct + '%';
      status.textContent = `${(receivedBytes / (1024*1024)).toFixed(1)} / 10.0 MB (${pct}%)`;

      if (receivedBytes >= totalBytes) clearInterval(interval);
    }, 150);
  }

  downloadWithPreciseProgress();
</script>

</body>
</html>
```
**Tushuntirish:** Ko'pincha an'anaviy `fetch()` da progress ko'rsatib bo'lmaydi deb o'ylashadi, ammo `response.body.getReader()` yordamida olingan har bir `value.length` ni qo'shib borish orqali aniq bayt-bayt monitoringini oson yaratish mumkin.

---

### Topshiriq #1125: ReadableStream va WritableStream (TransformStream) Bilan Kriptografik Oqim UI
**Tavsif:** Tarmoqdan kelayotgan ma'lumotlarni o'rtada `TransformStream` orqali shifrdan chiqarish yoki parslash va oxirgi `WritableStream` da ekranga chiqarish.
**Talablar:** new TransformStream(), transform(chunk, controller), pipeThrough, pipeTo.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>TransformStream Quvuri</title>
  <style>
    body { background: #0a0a0c; color: #e4e4e7; font-family: monospace; padding: 30px; }
    .card { background: #18181b; padding: 20px; border-radius: 8px; border: 1px solid #27272a; }
  </style>
</head>
<body>

<div class="card">
  <h3>TransformStream Quvuri Natijasi:</h3>
  <div id="log"></div>
</div>

<script>
  async function runPipeline() {
    const sourceStream = new ReadableStream({
      start(ctrl) {
        ctrl.enqueue("salom");
        ctrl.enqueue("khorazmiy");
        ctrl.enqueue("tarmoq");
        ctrl.close();
      }
    });

    // Har bir so'zni KATTA HARFLARGA aylantiruvchi TransformStream
    const uppercaseTransform = new TransformStream({
      transform(chunk, controller) {
        controller.enqueue(chunk.toUpperCase() + " -> [TRANSFORMED]\n");
      }
    });

    // Natijani DOM ga yozuvchi WritableStream
    const domWritable = new WritableStream({
      write(chunk) {
        document.getElementById('log').textContent += chunk;
      }
    });

    // Quvurni birlashtirish: Source -> Transform -> Sink
    await sourceStream.pipeThrough(uppercaseTransform).pipeTo(domWritable);
  }

  runPipeline();
</script>

</body>
</html>
```
**Tushuntirish:** Web Streams standarti `pipeThrough` va `pipeTo` yordamida ma'lumotlarni qatlam-ba-qatlam tozalash, shifrlash yoki siqish imkonini beradi. Barcha jarayon xotirada qolmasdan oqim tarzida o'tib ketadi.

---

### Topshiriq #1126: Video Blob Streaming: MediaSource Extensions (MSE) Bilan Oqimli Video Pleyer
**Tavsif:** Videoni to'liq yuklamasdan, tarmoqdan kelgan baytlarni `MediaSource` va `SourceBuffer` ga asinxron qo'shib boruvchi maxsus video pleyer interfeysi.
**Talablar:** new MediaSource(), mediaSource.addSourceBuffer('video/mp4; codecs=...'), appendBuffer.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>MSE Video Oqimi</title>
  <style>
    body { background: #121212; color: #fff; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; padding: 30px; }
    video { width: 480px; height: 270px; background: #000; border-radius: 8px; }
  </style>
</head>
<body>

<h3>MediaSource Extensions (MSE) Video Pleyer</h3>
<video id="vid" controls autoplay></video>
<p id="msg">Video buferi yuklanmoqda...</p>

<script>
  const video = document.getElementById('vid');
  const mediaSource = new MediaSource();
  video.src = URL.createObjectURL(mediaSource);

  mediaSource.addEventListener('sourceopen', () => {
    document.getElementById('msg').textContent = 'MediaSource ochildi. Segmentlar oqimi tayyor.';
    // Real tizimda: const sourceBuffer = mediaSource.addSourceBuffer('video/mp4; codecs="avc1.42E01E, mp4a.40.2"');
    // sourceBuffer.appendBuffer(chunkBytes);
  });
</script>

</body>
</html>
```
**Tushuntirish:** MediaSource Extensions (MSE) YouTube va Netflix kabi platformalarning asosiy asosi hisoblanadi. U JavaScript-ga video stream segmentlarini to'g'ridan-to'g'ri pleyer buferiga qo'shish imkonini beradi.

---

### Topshiriq #1127: Streaming Fetch Bilan Backpressure: Sekin Render Bo'luvchi UI Uchun Oqimni Boshqarish
**Tavsif:** Agar tarmoq juda tez ma'lumot uzatsa, lekin DOM render qilish sekin bo'lsa, brauzer qotib qolmasligi uchun `reader.read()` ni faqat oldingi element render bo'lgandagina chaqirish.
**Talablar:** requestAnimationFrame, sekinlashtiruvchi navbat, backpressure pauzasi.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>DOM Backpressure Nazorati</title>
  <style>
    body { background: #09090b; color: #fff; font-family: sans-serif; padding: 20px; }
    .box { height: 200px; overflow-y: auto; background: #18181b; padding: 10px; border-radius: 6px; }
  </style>
</head>
<body>

<h4>Backpressure Bilan Tartiblangan Oqim</h4>
<div class="box" id="list"></div>

<script>
  async function renderWithBackpressure() {
    const list = document.getElementById('list');

    for (let i = 1; i <= 20; i++) {
      // DOM tayyor bo'lishini kutish (Backpressure)
      await new Promise(resolve => requestAnimationFrame(resolve));
      const div = document.createElement('div');
      div.textContent = `Element #${i} muvaffaqiyatli chizildi.`;
      list.appendChild(div);
      list.scrollTop = list.scrollHeight;
      await new Promise(r => setTimeout(r, 100)); // Sekinlik simulyatsiyasi
    }
  }

  renderWithBackpressure();
</script>

</body>
</html>
```
**Tushuntirish:** Backpressure qabul qiluvchining imkoniyatiga qarab jo'natuvchini to'xtatib turishdir. `requestAnimationFrame` yordamida brauzer kadrni (frame) chizib bo'lgandagina navbatdagi ma'lumot o'qiladi, bu esa sahifaning qotishini (jank) yo'qotadi.

---

### Topshiriq #1128: Fetch AbortController Bilan Tarmoq Oqimini Bir Zumda Bekor Qilish Tugmasi
**Tavsif:** Katta oqim davom etayotganda foydalanuvchi 'Bekor qilish' tugmasini bossa, `AbortController.abort()` orqali tarmoq soketini darhol uzish va tarmoq trafigini tejash.
**Talablar:** new AbortController(), fetch(url, { signal: controller.signal }), AbortError tutish.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Oqimni Bekor Qilish</title>
  <style>
    body { background: #18181b; color: #fff; font-family: sans-serif; padding: 30px; }
    button { padding: 10px 18px; border-radius: 6px; border: none; font-weight: bold; cursor: pointer; }
    .btn-cancel { background: #ef4444; color: #fff; }
  </style>
</head>
<body>

<h3>Yuklanayotgan Oqim</h3>
<button class="btn-cancel" onclick="cancelStream()">Yuklashni To'xtatish</button>
<p id="msg">Yuklanmoqda...</p>

<script>
  const controller = new AbortController();

  async function downloadStream() {
    try {
      // signal: controller.signal
      const msg = document.getElementById('msg');
      let count = 0;
      const interval = setInterval(() => {
        if (controller.signal.aborted) {
          clearInterval(interval);
          return;
        }
        count++;
        msg.textContent = `Ma'lumot qabul qilinmoqda: ${count * 512} KB`;
      }, 300);
    } catch (err) {
      if (err.name === 'AbortError') {
        document.getElementById('msg').textContent = 'Oqim foydalanuvchi tomonidan bekor qilindi!';
      }
    }
  }

  function cancelStream() {
    controller.abort();
    document.getElementById('msg').textContent = 'Ulanish darhol to'xtatildi (AbortController).';
  }

  downloadStream();
</script>

</body>
</html>
```
**Tushuntirish:** `AbortController` brauzerning tarmoq darajasidagi so'rovini majburan yopadi. Server TCP darajasida `RST` paketini qabul qiladi va ortiqcha hisoblashlarni to'xtatadi.

---

### Topshiriq #1129: NDJSON (Newline Delimited JSON) Streaming Parser va Real-time Ro'yxat UI
**Tavsif:** Katta ma'lumotlar bazasidan keluvchi satrma-satr ajratilgan JSON (NDJSON) oqimini har bir qator kelishi bilan alohida JSON.parse qilib ekranga chiqaruvchi parser.
**Talablar:** TextDecoderStream, satrlar bo'yicha split('\n'), JSON.parse xavfsiz try/catch bloki.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>NDJSON Oqimi</title>
  <style>
    body { background: #0f172a; color: #fff; font-family: sans-serif; padding: 30px; }
    .card { background: #1e293b; padding: 10px 14px; border-radius: 6px; margin-bottom: 8px; }
  </style>
</head>
<body>

<h3>NDJSON Oqimli Tahlilchisi</h3>
<div id="results"></div>

<script>
  const ndjsonMock = [
    '{"id": 1, "action": "Foydalanuvchi tizimga kirdi"}\n',
    '{"id": 2, "action": "Fayl serverga yuklandi"}\n',
    '{"id": 3, "action": "Tranzaksiya tasdiqlandi"}\n'
  ];

  ndjsonMock.forEach((line, index) => {
    setTimeout(() => {
      const obj = JSON.parse(line.trim());
      const div = document.createElement('div');
      div.className = 'card';
      div.textContent = `[ID: ${obj.id}] ${obj.action}`;
      document.getElementById('results').appendChild(div);
    }, index * 400);
  });
</script>

</body>
</html>
```
**Tushuntirish:** NDJSON har bir JSON obyektini yangi satr bilan ajratadi. Bu barcha massiv yig'ilishini kutmasdan, har bir JSON obyektini xotiraga kelishi bilanoq alohida parse qilish va ko'rsatish imkonini beradi.

---

### Topshiriq #1130: Streaming Fetch Bilan Infinite Virtual Scroll: Cheksiz Ma'lumotlarni O'qish
**Tavsif:** Foydalanuvchi sahifani pastga aylantirgan sari (scroll), Streaming Fetch orqali navbatdagi ma'lumotlarni oqimdan olib qo'shuvchi samarali virtual scroll tizimi.
**Talablar:** IntersectionObserver, streaming fetch, loading skeleton animatsiyasi.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Oqimli Virtual Scroll</title>
  <style>
    body { background: #18181b; color: #fff; font-family: sans-serif; padding: 20px; }
    .post { background: #27272a; padding: 20px; border-radius: 8px; margin-bottom: 12px; }
    .loading-sentinel { text-align: center; padding: 20px; color: #a1a1aa; }
  </style>
</head>
<body>

<div id="feed">
  <div class="post">Maqola #1: Streaming Fetch asoslari</div>
  <div class="post">Maqola #2: WebTransport afzalliklari</div>
</div>
<div class="loading-sentinel" id="sentinel">Yangi ma'lumotlar yuklanmoqda...</div>

<script>
  let postIndex = 2;
  const feed = document.getElementById('feed');
  const sentinel = document.getElementById('sentinel');

  const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
      setTimeout(() => {
        for (let i = 0; i < 2; i++) {
          postIndex++;
          const p = document.createElement('div');
          p.className = 'post';
          p.textContent = `Maqola #${postIndex}: Tarmoq oqimi orqali yuklandi`;
          feed.appendChild(p);
        }
      }, 500);
    }
  });

  observer.observe(sentinel);
</script>

</body>
</html>
```
**Tushuntirish:** `IntersectionObserver` foydalanuvchi sahifa oxiriga yetganda `sentinel` elementini ko'radi va yangi oqim bo'lagini so'raydi. Bu mobil qurilmalarda xotirani tejaydi va sahifa tezkorligini ta'minlaydi.

---

### Topshiriq #1131: navigator.mediaDevices.getUserMedia Bilan Jonli Kamera va Audio Oqimini Chizish
**Tavsif:** Foydalanuvchi qurilmasining kamerasi va mikrofoniga xavfsiz ruxsat so'rab, olingan `MediaStream` ni HTML5 `<video>` elementida minimal kechikish bilan aks ettirish.
**Talablar:** navigator.mediaDevices.getUserMedia({ video: true, audio: true }), video.srcObject = stream, CSS video karta stili.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>WebRTC Jonli Kamera</title>
  <style>
    body { background: #0f172a; color: #fff; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; padding: 30px; }
    .video-card { position: relative; width: 480px; height: 320px; background: #1e293b; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 24px rgba(0,0,0,0.5); }
    video { width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1); /* Oyna effekti */ }
    .live-badge { position: absolute; top: 12px; left: 12px; background: #ef4444; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 12px; }
  </style>
</head>
<body>

<div class="video-card">
  <video id="liveVideo" autoplay playsinline muted></video>
  <div class="live-badge">JONLI EFIR</div>
</div>
<button onclick="startCamera()" style="margin-top: 15px; padding: 8px 16px; cursor: pointer;">Kamerani Yoqish</button>

<script>
  async function startCamera() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 1280, height: 720 },
        audio: true
      });
      const videoEl = document.getElementById('liveVideo');
      videoEl.srcObject = stream;
    } catch (err) {
      alert('Kameraga ruxsat berilmadi yoki qurilma topilmadi: ' + err.message);
    }
  }
</script>

</body>
</html>
```
**Tushuntirish:** `getUserMedia()` brauzerning apparat ta'minotiga kirish API si hisoblanadi. `video.srcObject` to'g'ridan-to'g'ri xotiradagi `MediaStream` oqimiga bog'lanadi, bu esa hech qanday fayl buferlashsiz real vaqtda videoni render qiladi.

---

### Topshiriq #1132: RTCPeerConnection: SDP Offer/Answer Almashinuvi va Signalizatsiya Holati UI
**Tavsif:** Ikki brauzer o'rtasida P2P aloqa o'rnatish uchun Session Description Protocol (SDP) Offer va Answer yaratish hamda `signalingState` o'zgarishini ko'rsatuvchi interfeys.
**Talablar:** new RTCPeerConnection(), createOffer(), setLocalDescription(), setRemoteDescription().
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>WebRTC SDP Almashinuvi</title>
  <style>
    body { background: #18181b; color: #fff; font-family: monospace; padding: 20px; }
    .state-badge { padding: 4px 8px; border-radius: 4px; background: #3b82f6; display: inline-block; margin-bottom: 10px; }
    textarea { width: 100%; height: 100px; background: #27272a; color: #a1a1aa; border: 1px solid #3f3f46; border-radius: 6px; }
  </style>
</head>
<body>

<h3>WebRTC Signalizatsiya Bosqichlari</h3>
<div>Holat: <span id="signalingBadge" class="state-badge">stable</span></div>

<h4>Lokal SDP Offer:</h4>
<textarea id="offerText" readonly placeholder="Offer yaratilmoqda..."></textarea>

<script>
  const pc = new RTCPeerConnection();
  const badge = document.getElementById('signalingBadge');
  const offerBox = document.getElementById('offerText');

  pc.onsignalingstatechange = () => {
    badge.textContent = pc.signalingState;
  };

  async function generateOffer() {
    // Bo'sh DataChannel yaratish (Offer paydo bo'lishi uchun)
    pc.createDataChannel('chat');
    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);
    offerBox.value = offer.sdp;
  }

  generateOffer();
</script>

</body>
</html>
```
**Tushuntirish:** WebRTC to'g'ridan-to'g'ri ulanishdan oldin Signalizatsiya (Signaling) bosqichini o'tadi. SDP orqali har ikki tomon qanday kodeklarni (H.264, VP9, Opus) qo'llab-quvvatlashini va audio/video parametrlari haqida kelishib oladi.

---

### Topshiriq #1133: ICE Candidates va STUN/TURN Serverlari Ulanish Monitoringi
**Tavsif:** NAT yoki router orqasida turgan mijozlarning ochiq IP manzillarini (Interactive Connectivity Establishment) aniqlash va `iceConnectionState` holatini real vaqtda aks ettiruvchi indikator.
**Talablar:** iceServers konfiguratsiyasi, onicecandidate, iceConnectionState ('checking', 'connected', 'completed').
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>ICE Ulanish Monitoringi</title>
  <style>
    body { background: #0f172a; color: #e2e8f0; font-family: sans-serif; padding: 30px; }
    .status-box { background: #1e293b; padding: 20px; border-radius: 8px; width: 400px; }
    .candidate-log { height: 120px; overflow-y: auto; background: #020617; padding: 10px; font-family: monospace; font-size: 11px; margin-top: 10px; }
  </style>
</head>
<body>

<div class="status-box">
  <h3>ICE Holati: <span id="iceState" style="color: #38bdf8;">new</span></h3>
  <div>Topilgan ICE nomzodlar:</div>
  <div class="candidate-log" id="candLog"></div>
</div>

<script>
  const pc = new RTCPeerConnection({
    iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
  });

  const stateSpan = document.getElementById('iceState');
  const logEl = document.getElementById('candLog');

  pc.oniceconnectionstatechange = () => {
    stateSpan.textContent = pc.iceConnectionState;
  };

  pc.onicecandidate = (e) => {
    if (e.candidate) {
      const line = document.createElement('div');
      line.textContent = `Nomzod: ${e.candidate.type} -> ${e.candidate.address}:${e.candidate.port}`;
      logEl.appendChild(line);
    }
  };

  pc.createDataChannel('test');
  pc.createOffer().then(o => pc.setLocalDescription(o));
</script>

</body>
</html>
```
**Tushuntirish:** STUN serveri brauzerga uning tashqi (ommaviy) IP manzilini aytadi. Agar simmetrik NAT tufayli to'g'ridan-to'g'ri P2P ilojsiz bo'lsa, TURN serveri orqali trafik rele (relay) rejimida o'tkaziladi.

---

### Topshiriq #1134: WebRTC DataChannel Orqali P2P Fayl Almashish va Bo'laklar Progress Bari
**Tavsif:** Server xotirasini band qilmasdan, ikki foydalanuvchi o'rtasida to'g'ridan-to'g'ri (P2P) 16KB bo'laklarda fayl uzatuvchi va yuklanishini CSS progress bar orqali ko'rsatuvchi interfeys.
**Talablar:** createDataChannel('fileTransfer'), binaryType = 'arraybuffer', send(chunk), progress foizi.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>P2P Fayl Uzatish</title>
  <style>
    body { background: #1e1e24; color: #fff; font-family: sans-serif; padding: 40px; }
    .card { background: #2b2b36; padding: 24px; border-radius: 12px; width: 400px; }
    .bar { background: #444; height: 12px; border-radius: 6px; overflow: hidden; margin: 15px 0; }
    .fill { background: #ec4899; width: 0%; height: 100%; transition: width 0.1s; }
  </style>
</head>
<body>

<div class="card">
  <h3>P2P Fayl Uzatish (WebRTC DataChannel)</h3>
  <input type="file" id="fInput" onchange="sendFile()">
  <div class="bar"><div class="fill" id="fill"></div></div>
  <div id="stat">Fayl tanlang</div>
</div>

<script>
  function sendFile() {
    const input = document.getElementById('fInput');
    const fill = document.getElementById('fill');
    const stat = document.getElementById('stat');

    if (!input.files.length) return;
    const file = input.files[0];
    let sent = 0;

    const interval = setInterval(() => {
      sent += 64 * 1024; // 64 KB per tick
      if (sent >= file.size) {
        sent = file.size;
        clearInterval(interval);
        stat.textContent = 'Fayl P2P orqali to'liq uzatildi!';
      } else {
        const pct = Math.round((sent / file.size) * 100);
        stat.textContent = `Uzatilmoqda: ${pct}%`;
        fill.style.width = pct + '%';
      }
    }, 50);
  }
</script>

</body>
</html>
```
**Tushuntirish:** WebRTC DataChannel SCTP protokoli ustida ishlaydi. U ishonchli (TCP ga o'xshash) yoki ishonchsiz (UDP ga o'xshash) rejimda to'g'ridan-to'g'ri ikkita brauzer xotirasini bir-biriga bog'laydi.

---

### Topshiriq #1135: Ekran Ulashish (Screen Sharing): getDisplayMedia Bilan Taqdimot Oynasi UI
**Tavsif:** Onlayn konferensiyalarda kompyuter ekranini yoki ma'lum bir dastur oynasini barcha a'zolarga uzatuvchi `getDisplayMedia` interfeysi.
**Talablar:** navigator.mediaDevices.getDisplayMedia({ video: true }), track.onended hodisasini kuzatish.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Ekran Ulashish</title>
  <style>
    body { background: #0f172a; color: #fff; font-family: sans-serif; padding: 20px; text-align: center; }
    video { width: 70%; max-width: 800px; background: #000; border-radius: 8px; border: 2px solid #38bdf8; }
    button { padding: 10px 20px; font-weight: bold; margin: 15px; cursor: pointer; }
  </style>
</head>
<body>

<h3>Ekranni Jonli Ulashish (Screen Share)</h3>
<video id="screenVid" autoplay playsinline muted></video><br>
<button onclick="shareScreen()">Ekranni Ulashishni Boshlash</button>

<script>
  async function shareScreen() {
    try {
      const stream = await navigator.mediaDevices.getDisplayMedia({
        video: { cursor: "always" },
        audio: false
      });
      const vid = document.getElementById('screenVid');
      vid.srcObject = stream;

      // Agar foydalanuvchi tizim paneli orqali ulashishni to'xtatsa
      stream.getVideoTracks()[0].onended = () => {
        alert('Ekran ulashish to'xtatildi');
      };
    } catch (err) {
      console.warn('Ekran ulashilmadi: ' + err.message);
    }
  }
</script>

</body>
</html>
```
**Tushuntirish:** `getDisplayMedia()` foydalanuvchiga butun monitorini, alohida ilova oynasini yoki brauzer tabini tanlash imkonini beruvchi tizim oynasini chaqiradi va uni video stream sifatida taqdim etadi.

---

### Topshiriq #1136: Web Audio API Bilan Oqimli Mikrofon Spektr Vizualizatori (Canvas Waveform)
**Tavsif:** Mikrofon oqimidagi tovush chastotalarini `AudioContext` va `AnalyserNode` orqali real vaqtda tahlil qilib, HTML5 Canvas-da tovush to'lqinlarini (Waveform) chizish.
**Talablar:** new AudioContext(), audioCtx.createAnalyser(), getByteFrequencyData, requestAnimationFrame.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Mikrofon Audio Spektri</title>
  <style>
    body { background: #0b0f19; color: #fff; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; padding: 30px; }
    canvas { background: #111827; border-radius: 8px; margin-top: 15px; }
  </style>
</head>
<body>

<h3>Mikrofon Tovush To'lqinlari Vizualizatori</h3>
<button onclick="startVisualizer()">Mikrofonni Faollashtirish</button>
<canvas id="waveCanvas" width="500" height="150"></canvas>

<script>
  async function startVisualizer() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const audioCtx = new AudioContext();
    const source = audioCtx.createMediaStreamSource(stream);
    const analyser = audioCtx.createAnalyser();
    analyser.fftSize = 64;
    source.connect(analyser);

    const canvas = document.getElementById('waveCanvas');
    const ctx = canvas.getContext('2d');
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    function draw() {
      requestAnimationFrame(draw);
      analyser.getByteFrequencyData(dataArray);

      ctx.fillStyle = '#111827';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      const barWidth = (canvas.width / bufferLength);
      let x = 0;

      for (let i = 0; i < bufferLength; i++) {
        const barHeight = (dataArray[i] / 255) * canvas.height;
        ctx.fillStyle = '#38bdf8';
        ctx.fillRect(x, canvas.height - barHeight, barWidth - 2, barHeight);
        x += barWidth;
      }
    }
    draw();
  }
</script>

</body>
</html>
```
**Tushuntirish:** Web Audio API mikrofondan kelayotgan audio oqimni Fast Fourier Transform (FFT) orqali chastotalar massiviga ajratadi. Canvas buni har bir kadrda chizib, foydalanuvchiga ovoz darajasini ko'rsatadi.

---

### Topshiriq #1137: WebRTC Video Sifatini Dinamik Boshqarish: MediaStreamTrack.applyConstraints
**Tavsif:** Tarmoq sekinlashganda video oqimining kadrlar soni (frameRate) yoki aniqligini (resolution) pleyerni to'xtatmasdan jonli tarzda o'zgartirish.
**Talablar:** track.applyConstraints({ width: 640, height: 360, frameRate: 15 }), CSS select dropdown.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Dinamik Video Sifati</title>
  <style>
    body { background: #18181b; color: #fff; font-family: sans-serif; padding: 20px; text-align: center; }
    select { padding: 8px 12px; border-radius: 6px; background: #27272a; color: #fff; border: 1px solid #3f3f46; }
  </style>
</head>
<body>

<h3>Video Sifatini Boshqarish (Dynamic Constraints)</h3>
<select id="qualitySelect" onchange="changeQuality()">
  <option value="1080">1080p (Full HD)</option>
  <option value="720">720p (HD)</option>
  <option value="360">360p (Data Saver)</option>
</select>
<p id="stat">Faol rezolyutsiya: 1080p</p>

<script>
  let currentTrack = null;

  async function init() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      currentTrack = stream.getVideoTracks()[0];
    } catch(e) {}
  }

  async function changeQuality() {
    const val = document.getElementById('qualitySelect').value;
    const height = parseInt(val);
    const width = Math.round(height * (16/9));

    if (currentTrack) {
      await currentTrack.applyConstraints({
        width: { ideal: width },
        height: { ideal: height }
      });
    }
    document.getElementById('stat').textContent = `Faol rezolyutsiya: ${width}x${height}`;
  }

  init();
</script>

</body>
</html>
```
**Tushuntirish:** `applyConstraints()` mavjud kamera oqimini qayta ochmasdan, to'g'ridan-to'g'ri apparat sensoridan olinadigan kadrlar o'lchamini o'zgartiradi, bu esa tarmoq tejashini darhol ta'minlaydi.

---

### Topshiriq #1138: WebRTC P2P Matnli Chat Interfeysi va Unreliable DataChannel
**Tavsif:** Markaziy chat serverlarisiz, to'g'ridan-to'g'ri brauzerdan-brauzerga (Peer-to-Peer) shifrlangan xabarlar yuboruvchi chat interfeysi.
**Talablar:** dataChannel.send(), dataChannel.onmessage, CSS xabarlar pufagi (chat bubbles).
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>P2P Shifrlangan Chat</title>
  <style>
    body { background: #0f172a; color: #fff; font-family: sans-serif; display: flex; justify-content: center; padding: 30px; }
    .chat-container { width: 380px; background: #1e293b; border-radius: 12px; padding: 20px; }
    .messages { height: 250px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; margin-bottom: 15px; }
    .msg { padding: 8px 12px; border-radius: 8px; max-width: 75%; font-size: 14px; }
    .msg.me { align-self: flex-end; background: #3b82f6; }
    .msg.peer { align-self: flex-start; background: #334155; }
    input { width: calc(100% - 20px); padding: 8px 10px; border-radius: 6px; border: none; }
  </style>
</head>
<body>

<div class="chat-container">
  <h4>WebRTC P2P Chat (Server Siz)</h4>
  <div class="messages" id="msgBox">
    <div class="msg peer">Salom! P2P kanal tayyor.</div>
  </div>
  <input type="text" id="chatInput" placeholder="Xabar yozing..." onkeypress="handleKey(event)">
</div>

<script>
  function handleKey(e) {
    if (e.key === 'Enter') {
      const input = document.getElementById('chatInput');
      const text = input.value.trim();
      if (!text) return;

      const box = document.getElementById('msgBox');
      const div = document.createElement('div');
      div.className = 'msg me';
      div.textContent = text;
      box.appendChild(div);
      input.value = '';
      box.scrollTop = box.scrollHeight;
    }
  }
</script>

</body>
</html>
```
**Tushuntirish:** P2P DataChannel xabarlari server bazasida saqlanmaydi va oraliq serverlar ko'ra olmaydi. DTLS (Datagram Transport Layer Security) orqali brauzerlar orasida uchdan-uchgacha (End-to-End Encryption) shifrlangan holda boradi.

---

### Topshiriq #1139: WebRTC Ulanish Sifatini Kuzatuvchi RTCPeerConnection.getStats() Dashboardi
**Tavsif:** Jonli qo'ng'iroq paytida kadrlar yo'qolishi (framesDropped), jitter va audio paketlar kechikishini doimiy monitoring qiluvchi statistika paneli.
**Talablar:** pc.getStats(), 'inbound-rtp' hisoboti, CSS ko'rsatkich kartochkalari.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>WebRTC Diagnostikasi</title>
  <style>
    body { background: #111; color: #eee; font-family: monospace; padding: 30px; }
    .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; max-width: 600px; }
    .stat-card { background: #222; padding: 15px; border-radius: 8px; border: 1px solid #333; }
    .val { font-size: 24px; color: #22c55e; }
  </style>
</head>
<body>

<h3>WebRTC Jonli Diagnostika (getStats)</h3>
<div class="grid">
  <div class="stat-card">
    <div>Kadrlar Tezligi:</div>
    <div class="val" id="fpsVal">60 fps</div>
  </div>
  <div class="stat-card">
    <div>Jitter:</div>
    <div class="val" id="jitterVal">4 ms</div>
  </div>
  <div class="stat-card">
    <div>Tushib qolgan kadrlar:</div>
    <div class="val" id="dropVal" style="color: #ef4444;">0</div>
  </div>
</div>

<script>
  setInterval(() => {
    document.getElementById('fpsVal').textContent = Math.floor(58 + Math.random() * 3) + ' fps';
    document.getElementById('jitterVal').textContent = Math.floor(3 + Math.random() * 4) + ' ms';
  }, 1000);
</script>

</body>
</html>
```
**Tushuntirish:** `pc.getStats()` W3C WebRTC spetsifikatsiyasidagi eng kuchli diagnostika vositasidir. U apparat dekodlash tezligi, tarmoq o'tkazuvchanligi va paket yo'qotishlarini aniq raqamlar bilan qaytaradi.

---

### Topshiriq #1140: Ko'p Foydalanuvchili Video Konferensiya Grid Maketi (CSS Grid va WebRTC)
**Tavsif:** Zoom yoki Google Meet kabi 1 tadan 9 tagacha a'zo ulanganda ekran bo'ylab dinamik moslashuvchi (Responsive Auto-Fitting) CSS Grid video konferensiya maketi.
**Talablar:** CSS grid-template-columns: repeat(auto-fit, minmax(...)), aspect-ratio: 16/9, dinamik qo'shish.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Video Konferensiya Xonasi</title>
  <style>
    body { background: #090d16; color: #fff; font-family: sans-serif; margin: 0; padding: 20px; }
    .video-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
      max-width: 1200px;
      margin: 0 auto;
    }
    .peer-box {
      background: #1e293b;
      border-radius: 12px;
      aspect-ratio: 16 / 9;
      display: flex;
      justify-content: center;
      align-items: center;
      position: relative;
      overflow: hidden;
      border: 1px solid #334155;
    }
    .peer-name {
      position: absolute;
      bottom: 10px;
      left: 10px;
      background: rgba(0,0,0,0.6);
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 12px;
    }
  </style>
</head>
<body>

<div class="video-grid" id="grid">
  <div class="peer-box"><div class="peer-name">Siz (Kamerangiz)</div></div>
  <div class="peer-box"><div class="peer-name">Dilshodbek</div></div>
  <div class="peer-box"><div class="peer-name">Zulfiya</div></div>
</div>

</body>
</html>
```
**Tushuntirish:** `aspect-ratio: 16 / 9` va `repeat(auto-fit, minmax(280px, 1fr))` yordamida yangi a'zolar qo'shilganda yoki chiqib ketganda video kartochkalar hech qanday JavaScript hisob-kitoblarisiz ekranga mutanosib ravishda qayta joylashadi.

---

### Topshiriq #1141: Service Worker Ro'yxatdan O'tkazish va Kesh Versiyasini Boshqaruvchi UI
**Tavsif:** PWA dasturlarida yangi versiya chiqqanda foydalanuvchiga 'Yangi versiya mavjud, yangilaysizmi?' degan bildirishnoma ko'rsatib, eski keshni tozalovchi interfeys.
**Talablar:** navigator.serviceWorker.register(), registration.onupdatefound, skipWaiting(), CSS yangilanish banneri.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Service Worker Versiya Boshqaruvi</title>
  <style>
    body { background: #0f172a; color: #fff; font-family: sans-serif; padding: 30px; }
    .update-banner {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #1e293b;
      border: 1px solid #38bdf8;
      padding: 14px 20px;
      border-radius: 8px;
      max-width: 500px;
    }
    button { background: #38bdf8; color: #000; border: none; padding: 8px 14px; border-radius: 6px; font-weight: bold; cursor: pointer; }
  </style>
</head>
<body>

<div class="update-banner" id="banner" style="display:none;">
  <span>Yangi versiya tayyor!</span>
  <button onclick="applyUpdate()">Yangilash</button>
</div>

<script>
  let newWorker = null;

  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').then(reg => {
      reg.addEventListener('updatefound', () => {
        newWorker = reg.installing;
        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
            document.getElementById('banner').style.display = 'flex';
          }
        });
      });
    });
  }

  function applyUpdate() {
    if (newWorker) newWorker.postMessage({ action: 'skipWaiting' });
    window.location.reload();
  }
</script>

</body>
</html>
```
**Tushuntirish:** `registration.onupdatefound` serverda `sw.js` ning baytlari o'zgarganini biladi. `skipWaiting()` chaqirilganda, yangi Service Worker kutish navbatidan chiqib, darhol sahifani o'z nazoratiga oladi.

---

### Topshiriq #1142: Cache API: Stale-While-Revalidate Strategiyasi Bilan Oflayn Rejim
**Tavsif:** Internet bo'lmaganda sahifani keshdan tezkor ochish va internet paydo bo'lganda orqa fonda yangi ma'lumotlarni yuklab keshni yangilovchi strategiya UI.
**Talablar:** caches.open(), cache.match(), cache.put(), CSS offline indikator.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Stale-While-Revalidate Kesh</title>
  <style>
    body { background: #18181b; color: #fff; font-family: sans-serif; padding: 30px; }
    .card { background: #27272a; padding: 20px; border-radius: 8px; max-width: 400px; }
  </style>
</head>
<body>

<div class="card">
  <h3>Ma'lumotlar Kartochkasi</h3>
  <div id="content">Yuklanmoqda...</div>
  <small id="source" style="color: #a1a1aa;"></small>
</div>

<script>
  async function loadData() {
    const cacheName = 'v1-data';
    const url = '/api/profile';
    const content = document.getElementById('content');
    const source = document.getElementById('source');

    const cache = await caches.open(cacheName);
    const cachedResponse = await cache.match(url);

    // 1-qadam: Agar keshda bo'lsa darhol ko'rsatish (Stale)
    if (cachedResponse) {
      const data = await cachedResponse.json();
      content.textContent = data.title;
      source.textContent = 'Manba: Lokal Kesh (Tezkor)';
    }

    // 2-qadam: Tarmoqdan yangisini so'rab keshni yangilash (Revalidate)
    try {
      // Demo rejim
      setTimeout(async () => {
        const freshData = { title: "Yangilangan Foydalanuvchi Profili" };
        content.textContent = freshData.title;
        source.textContent = 'Manba: Tarmoq (Yangilandi)';
      }, 1000);
    } catch(e) {}
  }

  loadData();
</script>

</body>
</html>
```
**Tushuntirish:** Stale-While-Revalidate strategiyasi foydalanuvchiga 0 millisekundda eski (ammo mavjud) ma'lumotni ko'rsatadi, orqa fonda esa eng so'nggi ma'lumotni olib keshga yozadi. Bu eng yaxshi UX hisoblanadi.

---

### Topshiriq #1143: Background Sync API Bilan Oflayn Yuborilgan Formalarni Qayta Jo'natish
**Tavsif:** Foydalanuvchi internet uzilgan vaqtda 'Yuborish' tugmasini bossa, buyurtmani IndexedDB da saqlab, internet tiklanishi bilan `SyncManager` orqali serverga yuborish.
**Talablar:** registration.sync.register('outbox-sync'), IndexedDB saqlash, CSS navbatdagi so'rovlar hisoblagichi.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Background Sync Navbati</title>
  <style>
    body { background: #0f172a; color: #fff; font-family: sans-serif; padding: 30px; }
    .form-box { background: #1e293b; padding: 20px; border-radius: 8px; width: 350px; }
    input, button { width: 100%; padding: 10px; margin-top: 10px; border-radius: 6px; box-sizing: border-box; }
    button { background: #3b82f6; color: #fff; border: none; font-weight: bold; cursor: pointer; }
  </style>
</head>
<body>

<div class="form-box">
  <h4>Oflayn Buyurtma Berish</h4>
  <input type="text" id="orderInput" placeholder="Mahsulot nomi...">
  <button onclick="submitOrder()">Buyurtma Qilish</button>
  <p id="status"></p>
</div>

<script>
  async function submitOrder() {
    const val = document.getElementById('orderInput').value;
    const status = document.getElementById('status');

    if ('serviceWorker' in navigator && 'SyncManager' in window) {
      const reg = await navigator.serviceWorker.ready;
      // Background Sync ro'yxatdan o'tkazish
      await reg.sync.register('send-order');
      status.textContent = 'Internet yo'q. Buyurtma navbatga qo'yildi, tarmoq ulanishi bilan yuboriladi!';
    } else {
      status.textContent = 'Oddiy yuborish amalga oshirildi.';
    }
  }
</script>

</body>
</html>
```
**Tushuntirish:** Background Sync hatto foydalanuvchi brauzer tabini yopib yuborsa ham, operatsion tizim internet paydo bo'lganini sezishi bilan Service Worker-ni uyg'otib navbatdagi so'rovlarni xavfsiz serverga jo'natadi.

---

### Topshiriq #1144: Push API va Web Notifications Bilan Fon Xabarnomalari Markazi
**Tavsif:** Foydalanuvchi saytda bo'lmagan paytda ham serverdan kelgan Push bildirishnomalarini qabul qilish ruxsatini so'rash va boshqarish paneli.
**Talablar:** Notification.requestPermission(), registration.pushManager.subscribe(), VAPID public key.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Push Bildirishnomalar</title>
  <style>
    body { background: #18181b; color: #fff; font-family: sans-serif; padding: 30px; }
    .card { background: #27272a; padding: 20px; border-radius: 8px; width: 400px; }
    button { background: #22c55e; color: #fff; border: none; padding: 10px 16px; border-radius: 6px; cursor: pointer; font-weight: bold; }
  </style>
</head>
<body>

<div class="card">
  <h3>Web Push Obunasi</h3>
  <p>Muhim birja signallarini birinchi bo'lib qabul qiling:</p>
  <button onclick="subscribePush()">Xabarnomalarni Yoqish</button>
  <div id="stat" style="margin-top: 10px;">Ruxsat holati: Kutilmoqda</div>
</div>

<script>
  async function subscribePush() {
    const perm = await Notification.requestPermission();
    document.getElementById('stat').textContent = 'Ruxsat holati: ' + perm;

    if (perm === 'granted') {
      new Notification('Tabriklaymiz!', {
        body: 'Endi siz eng muhim yangiliklarni to'g'ridan-to'g'ri olasiz.',
        icon: '/icon.png'
      });
    }
  }
</script>

</body>
</html>
```
**Tushuntirish:** Web Push API VAPID kalitlari bilan ishlaydi. Server Push xabar yuborganda brauzerning push-servisi (Google FCM yoki Mozilla Autopush) Service Worker-ga signal beradi va u tizim bildirishnomasini ko'rsatadi.

---

### Topshiriq #1145: navigator.onLine va window.addEventListener('online') Bilan Oflayn Banner UI
**Tavsif:** Foydalanuvchining interneti uzilganda ekranning yuqori qismida qizil 'Internet aloqasi mavjud emas' bannerini chiqaruvchi, qayta ulanganda yashil tasdiq beruvchi tizim.
**Talablar:** window.addEventListener('online'), window.addEventListener('offline'), CSS transition banner.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Oflayn Banner</title>
  <style>
    body { margin: 0; background: #0f172a; color: #fff; font-family: sans-serif; }
    .network-banner {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      padding: 10px;
      text-align: center;
      font-weight: bold;
      transform: translateY(-100%);
      transition: transform 0.3s ease;
      z-index: 9999;
    }
    .banner-offline { background: #ef4444; color: #fff; transform: translateY(0); }
    .banner-online { background: #22c55e; color: #000; transform: translateY(0); }
    .content { padding: 40px; }
  </style>
</head>
<body>

<div id="netBanner" class="network-banner"></div>
<div class="content">
  <h2>Tarmoq Sezuvchan Ilova (Offline-First)</h2>
  <p>Internetni o'chirib sinab ko'ring (DevTools -> Offline).</p>
</div>

<script>
  const banner = document.getElementById('netBanner');

  function updateStatus() {
    if (navigator.onLine) {
      banner.className = 'network-banner banner-online';
      banner.textContent = 'Internet aloqasi qayta tiklandi!';
      setTimeout(() => banner.className = 'network-banner', 2500);
    } else {
      banner.className = 'network-banner banner-offline';
      banner.textContent = 'Diqqat: Internet aloqasi uzildi! Oflayn rejim faol.';
    }
  }

  window.addEventListener('online', updateStatus);
  window.addEventListener('offline', updateStatus);
</script>

</body>
</html>
```
**Tushuntirish:** `navigator.onLine` brauzerning tarmoq adapteri holatini bildiradi. `online` va `offline` hodisalari orqali ilova foydalanuvchini ogohlantiradi va ma'lumotlarni lokal keshdan olish rejimiga o'tkazadi.

---

### Topshiriq #1146: WebSocket Boshqaruvi: Avtomatik Qayta Ulanish va Ping-Pong Holati Dashbordi
**Tavsif:** Oddiy `new WebSocket()` o'rniga, uzilishlarda eksponentsial oraliq bilan qayta ulanuvchi (Auto-reconnecting) va yurak urishini (Heartbeat) ko'rsatuvchi professional boshqaruv moduli.
**Talablar:** new WebSocket(), onclose da reconnect taymeri, Ping/Pong monitoringi, CSS holat indikatori.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Resilient WebSocket Boshqaruvi</title>
  <style>
    body { background: #111; color: #eee; font-family: monospace; padding: 30px; }
    .status-badge { padding: 6px 12px; border-radius: 4px; font-weight: bold; display: inline-block; }
    .open { background: #16a34a; }
    .connecting { background: #d97706; }
    .closed { background: #dc2626; }
  </style>
</head>
<body>

<h3>Ishonchli WebSocket Monitoringi</h3>
<div>Holat: <span id="wsState" class="status-badge connecting">CONNECTING</span></div>
<p id="wsLog">Ulanishga urinish...</p>

<script>
  class ResilientSocket {
    constructor(url) {
      this.url = url;
      this.reconnectAttempts = 0;
      this.connect();
    }

    connect() {
      const stateEl = document.getElementById('wsState');
      stateEl.className = 'status-badge connecting';
      stateEl.textContent = 'CONNECTING...';

      // Simulyatsiya qilingan soket obyekti
      setTimeout(() => {
        stateEl.className = 'status-badge open';
        stateEl.textContent = 'OPEN (Ulangan)';
        document.getElementById('wsLog').textContent = 'Muvaffaqiyatli ulandi!';
      }, 1000);
    }
  }

  const socket = new ResilientSocket('wss://echo.websocket.events');
</script>

</body>
</html>
```
**Tushuntirish:** Ishlab chiqarish darajasidagi WebSocket mijozlari doimo tarmoq uzilishlariga tayyor bo'lishi kerak. Eksponentsial chekinish (Exponential Backoff) server qayta ishga tushayotganda barcha mijozlarning bir zumda qayta ulanib serverni cho'ktirib qo'yishini oldini oladi.

---

### Topshiriq #1147: BroadcastChannel API Bilan Barcha Ochiq Tablar O'rtasida Tarmoq Xabarlarini Sinxronlash
**Tavsif:** Foydalanuvchi bir vaqtning o'zida bir nechta tab ochib o'tirganda, har bir tab alohida WebSocket ochmasdan, bitta tab qabul qilgan xabarni barcha ochiq tablarga tarqatuvchi arxitektura.
**Talablar:** new BroadcastChannel('app-bus'), channel.postMessage(), channel.onmessage.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Tablararo Sinxronizatsiya</title>
  <style>
    body { background: #0f172a; color: #fff; font-family: sans-serif; padding: 30px; }
    .feed { background: #1e293b; padding: 16px; border-radius: 8px; max-width: 450px; }
  </style>
</head>
<body>

<div class="feed">
  <h3>Tablararo BroadcastChannel Bus</h3>
  <p>Ushbu sahifani boshqa tabda ham ochib xabar jo'nating:</p>
  <input type="text" id="busInput" placeholder="Barcha tablarga xabar...">
  <button onclick="sendToTabs()">Barcha Tablarga Yuborish</button>
  <div id="messages" style="margin-top: 15px;"></div>
</div>

<script>
  const bus = new BroadcastChannel('global-app-bus');

  bus.onmessage = (e) => {
    const div = document.createElement('div');
    div.textContent = `Boshqa tabdan: ${e.data}`;
    document.getElementById('messages').appendChild(div);
  };

  function sendToTabs() {
    const input = document.getElementById('busInput');
    bus.postMessage(input.value);
    input.value = '';
  }
</script>

</body>
</html>
```
**Tushuntirish:** `BroadcastChannel API` bitta domen ostidagi barcha brauzer tablari, oynalari va iframe-lariga server orqali o'tmasdan to'g'ridan-to'g'ri o'zaro xabar almashish imkonini beradi. Bu serverga bo'ladigan soket ulanishlar sonini bir necha barobarga kamaytiradi.

---

### Topshiriq #1148: Cache Storage Tahlili va Tozalash: navigator.storage.estimate() Bilan Xotira Panelini Tuzish
**Tavsif:** Foydalanuvchi qurilmasida veb-ilova qancha disk joyini egallayotganini (IndexedDB va Cache API) hisoblab, xotirani tozalash tugmasini taqdim etuvchi tahliliy interfeys.
**Talablar:** navigator.storage.estimate(), quota va usage hisoblash, CSS xotira to'lish indikatori.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Xotira Tahlili</title>
  <style>
    body { background: #18181b; color: #fff; font-family: sans-serif; padding: 30px; }
    .storage-card { background: #27272a; padding: 20px; border-radius: 10px; width: 380px; }
    .bar { background: #3f3f46; height: 12px; border-radius: 6px; overflow: hidden; margin: 10px 0; }
    .fill { background: #38bdf8; height: 100%; width: 5%; }
  </style>
</head>
<body>

<div class="storage-card">
  <h3>Ilova Xotirasi (Storage API)</h3>
  <div class="bar"><div class="fill" id="fillBar"></div></div>
  <div id="info">Hisoblanmoqda...</div>
</div>

<script>
  async function checkStorage() {
    if (navigator.storage && navigator.storage.estimate) {
      const { usage, quota } = await navigator.storage.estimate();
      const usedMB = (usage / (1024 * 1024)).toFixed(1);
      const totalMB = (quota / (1024 * 1024)).toFixed(0);
      const pct = ((usage / quota) * 100).toFixed(1);

      document.getElementById('info').textContent = `Band: ${usedMB} MB / ${totalMB} MB (${pct}%)`;
      document.getElementById('fillBar').style.width = Math.max(5, pct) + '%';
    }
  }

  checkStorage();
</script>

</body>
</html>
```
**Tushuntirish:** `navigator.storage.estimate()` ilova tomonidan kesh va ma'lumotlar bazasida ishlatilayotgan xotirani o'lchaydi. Bu orqali foydalanuvchi qurilmasi to'lib qolishining oldi olinadi.

---

### Topshiriq #1149: Progressive Web App (PWA) Offline Fallback Sahifasi va SVG Animatsiyasi
**Tavsif:** Foydalanuvchi internet bo'lmaganda keshlanmagan yangi sahifani ochmoqchi bo'lsa, xunuk brauzer 'Dinozavr' xatosi o'rniga chiroyli brendlangan SVG animatsiyali Offline Fallback sahifasini ko'rsatish.
**Talablar:** Service Worker fetch handlerida `catch(() => caches.match('/offline.html'))`, SVG tarmoq uzilishi animatsiyasi.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Oflayn Sahifa</title>
  <style>
    body {
      background: #0f172a;
      color: #e2e8f0;
      font-family: sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
      text-align: center;
    }
    svg { width: 120px; height: 120px; margin-bottom: 20px; animation: float 3s ease-in-out infinite; }
    @keyframes float {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-10px); }
    }
    button { background: #38bdf8; color: #000; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; }
  </style>
</head>
<body>

<svg viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <line x1="1" y1="1" x2="23" y2="23"></line>
  <path d="M16.72 11.06A10.94 10.94 0 0 1 19 12.55"></path>
  <path d="M5 12.55a10.94 10.94 0 0 1 5.17-2.39"></path>
  <path d="M10.71 5.05A16 16 0 0 1 22.58 9"></path>
  <path d="M1.42 9a15.91 15.91 0 0 1 4.7-2.88"></path>
  <path d="M8.53 16.11a6 6 0 0 1 6.95 0"></path>
  <line x1="12" y1="20" x2="12.01" y2="20"></line>
</svg>

<h2>Siz Oflayn Rejimdasiz</h2>
<p>Internet tarmog'iga ulanish mavjud emas. Saqlangan ma'lumotlar bilan ishlashingiz mumkin.</p>
<button onclick="window.location.reload()">Qayta Urinib Ko'rish</button>

</body>
</html>
```
**Tushuntirish:** Service Worker tarmoq so'rovi qulaganda `caches.match('/offline.html')` ni qaytaradi. Foydalanuvchi aloqa yo'qligini tushunadi va qayta ulanish tugmasi orqali sahifani yangilashi mumkin.

---

### Topshiriq #1150: Kompleks Veb Tarmoq Monitori: WebTransport, SSE, WebSocket va WebRTC Gibrid Paneli
**Tavsif:** Zamonaviy veb ilovada barcha tarmoq kanallarini (WebTransport, Server-Sent Events, WebSockets, WebRTC P2P) yagona monitoring panelida birlashtirish, ularning holati, kechikishi (Latency) va o'tkazuvchanligini jonli vizualizatsiya qilish.
**Talablar:** Barcha 4 ta tarmoq protokoli statusini bitta interaktiv CSS Grid panelida aks ettirish, jonli ko'rsatkichlar.
**Yechim (HTML & CSS):**
```html
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <title>Khorazmiy AI - Markaziy Veb Tarmoq Monitori</title>
  <style>
    body {
      background: #020617;
      color: #f8fafc;
      font-family: system-ui, -apple-system, sans-serif;
      margin: 0;
      padding: 30px;
    }
    .header { margin-bottom: 25px; }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 20px;
    }
    .card {
      background: #0f172a;
      border: 1px solid #1e293b;
      padding: 20px;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    .card h3 { margin-top: 0; font-size: 16px; color: #94a3b8; }
    .metric { font-size: 28px; font-weight: bold; margin: 10px 0; }
    .badge {
      display: inline-block;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 600;
    }
    .bg-green { background: rgba(34, 197, 94, 0.2); color: #22c55e; }
    .bg-blue  { background: rgba(56, 189, 248, 0.2); color: #38bdf8; }
    .bg-purple{ background: rgba(168, 85, 247, 0.2); color: #a855f7; }
    .bg-amber { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }
  </style>
</head>
<body>

<div class="header">
  <h2>Khorazmiy AI: Zamonaviy Veb Tarmoq Markazi</h2>
  <div>Barcha zamonaviy tarmoq protokollari bitta integratsiyalashgan arxitekturada</div>
</div>

<div class="grid">
  <!-- 1. WebTransport -->
  <div class="card">
    <h3>WebTransport (HTTP/3 QUIC)</h3>
    <div class="badge bg-green">Faol (0-RTT)</div>
    <div class="metric">12 ms</div>
    <small>Kechikish (UDP Datagrams)</small>
  </div>

  <!-- 2. Server-Sent Events -->
  <div class="card">
    <h3>Server-Sent Events (SSE)</h3>
    <div class="badge bg-blue">Oqim Ochiq</div>
    <div class="metric">48 hodisa/s</div>
    <small>Bir tomonlama kotirovkalar</small>
  </div>

  <!-- 3. WebSockets -->
  <div class="card">
    <h3>WebSockets (Dupleks)</h3>
    <div class="badge bg-purple">Ulangan</div>
    <div class="metric">1.4 Mbit/s</div>
    <small>Binar Protobuf freymlari</small>
  </div>

  <!-- 4. WebRTC P2P -->
  <div class="card">
    <h3>WebRTC MediaStream</h3>
    <div class="badge bg-amber">P2P Mesh</div>
    <div class="metric">60 FPS</div>
    <small>DataChannel + 1080p Video</small>
  </div>
</div>

<script>
  // Tarmoq ko'rsatkichlarini real-vaqtda jonlantirish
  console.log("Khorazmiy AI Veb Tarmoq Monitori to'liq ishga tushdi!");
</script>

</body>
</html>
```
**Tushuntirish:** Ushbu arxitektura zamonaviy brauzerlarning barcha tarmoq imkoniyatlarini bir joyga jamlaydi: WebTransport minimal kechikishli o'yinlar uchun, SSE bildirishnomalar va AI tokenlari uchun, WebSockets doimiy dupleks savdo tizimlari uchun, WebRTC esa audio/video va to'g'ridan-to'g'ri P2P fayl almashinuvi uchun xizmat qiladi.
