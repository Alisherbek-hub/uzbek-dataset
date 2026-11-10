# Khorazmiy AI: PHP - Modul 23
## Mavzu: Tarmoq protokollari: Swoole / OpenSwoole asinxron soketlar, ReactPHP, Ratchet WebSockets va gRPC PHP

Salom, men **Khorazmiy AI** loyihasining PHP va yuqori unumdorlikka ega asinxron tarmoq tizimlari bo'yicha bosh dataset mutaxassisiman. Ushbu modulda PHP ekotizimidagi zamonaviy asinxron dvigatellar (Swoole, OpenSwoole), reaktiv dasturlash (ReactPHP), real-vaqt soketlari (Ratchet WebSockets) hamda yuqori samarali RPC mikroservislari (gRPC va Protocol Buffers) bo'yicha 50 ta sanoat darajasidagi amaliy topshiriq va ularning mukammal ishlab turgan yechimlari taqdim etiladi.

---
### Topshiriq #1101: Swoole Asinxron Multi-Worker TCP Server
**Tavsif:** Yuqori yuklamali fintex ilovalarida sekundiga yuz minglab tranzaksiya so'rovlarini qabul qilib, ularni protsessor yadrolariga taqsimlagan holda javob qaytaruvchi multi-worker TCP serverini yarating.
**Talablar:** Swoole\Server dan foydalanish, worker_num va max_request parametrlarini sozlash, connect, receive, close hodisalarini boshqarish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Sanoat darajasidagi Swoole TCP Server
use Swoole\Server;

// 0.0.0.0 IP va 9501 portda TCP server nusxasini olamiz
$server = new Server("0.0.0.0", 9501, SWOOLE_PROCESS, SWOOLE_SOCK_TCP);

// Server ishlash konfiguratsiyasini sozlaymiz
$server->set([
    'worker_num'      => swoole_cpu_num() * 2, // CPU yadrolari soniga qarab workerlar soni
    'max_request'     => 100000,               // Xotira sizib chiqishini (memory leak) oldini olish
    'dispatch_mode'   => 2,                    // Mijoz IP va fd bo'yicha qat'iy taqsimlash
    'daemonize'       => false,                // Konsolda kuzatish uchun fonda ishlatmaymiz
    'backlog'         => 1024,                 // TCP ulanish navbati (queue)
    'open_tcp_nodelay'=> true,                 // Nagle algoritmini o'chirib, paket kechikishini pasaytirish
]);

// Mijoz birinchi marta ulanganda chaqiriladi
$server->on('Connect', function (Server $serv, int $fd, int $reactorId) {
    $clientInfo = $serv->getClientInfo($fd);
    echo "[+] Ulanish o'rnatildi: FD={$fd}, IP={$clientInfo['remote_ip']}:{$clientInfo['remote_port']}
";
});

// Mijozdan ma'lumot kelganda chaqiriladi
$server->on('Receive', function (Server $serv, int $fd, int $reactorId, string $data) {
    $trimmed = trim($data);
    echo "[*] Qabul qilindi [FD {$fd}]: {$trimmed}
";
    
    // So'rovga javob tayyorlash va qaytarish
    $response = "ACK: Tranzaksiya qabul qilindi (" . date('Y-m-d H:i:s') . ")
";
    $serv->send($fd, $response);
});

// Mijoz ulanishni yopganda chaqiriladi
$server->on('Close', function (Server $serv, int $fd) {
    echo "[-] Ulanish yopildi: FD={$fd}
";
});

echo "Swoole TCP Server 0.0.0.0:9501 manzilida tinglamoqda...
";
$server->start();
```
**Tushuntirish:** Swoole Master-Manager-Worker arxitekturasida ishlaydi. Master jarayon tarmoq soketlarini `epoll` orqali tinglaydi va kelgan ulanishlarni Worker jarayonlariga xavfsiz IPC kanali orqali yetkazadi. `max_request` sozlamasi har 100k so'rovdan so'ng workerni xavfsiz qayta ishga tushirib, PHP da yillar davomida xotira tozalanishini kafolatlaydi.

---

### Topshiriq #1102: Swoole Coroutine asosidagi Asinxron TCP Client
**Tavsif:** Tashqi to'lov shlyuziga (Payment Gateway) non-blocking rejimda ulanib, so'rov jo'natuvchi va javobni kutish vaqtida (timeout) operatsion tizim ipini bloklamaydigan korutina mijozini ishlab chiqing.
**Talablar:** Swoole\Coroutine\Client, timeout parametrlari, non-blocking connect va recv.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Swoole Coroutine TCP Client
use Swoole\Coroutine;
use Swoole\Coroutine\Client;
use function Swoole\Coroutine\run;

// Barcha korutinalarni run kontekstida ishga tushiramiz
run(function () {
    // 10 ta parallel korutina orqali bank serveriga so'rov yuboramiz
    for ($i = 1; $i <= 10; $i++) {
        Coroutine::create(function () use ($i) {
            $client = new Client(SWOOLE_SOCK_TCP);
            
            // Ulanish va javob kutish vaqti (soniyalarda)
            $client->set([
                'timeout' => 2.5,
                'connect_timeout' => 1.0,
            ]);

            // TCP serverga ulanish
            if (!$client->connect('127.0.0.1', 9501)) {
                echo "[!] Ulanish xatosi [ID {$i}]: {$client->errMsg} (kod: {$client->errCode})
";
                return;
            }

            // Tranzaksiya paketini jo'natamiz
            $payload = json_encode(['tx_id' => $i, 'amount' => 50000, 'curr' => 'UZS']) . "
";
            $client->send($payload);

            // Javobni asinxron kutamiz (boshqa korutinalar to'xtab qolmaydi)
            $response = $client->recv();
            if ($response === false) {
                echo "[!] Javob olishda xato [ID {$i}]: {$client->errMsg}
";
            } else {
                echo "[+] Muvaffaqiyatli [ID {$i}]: " . trim($response) . "
";
            }

            $client->close();
        });
    }
});
```
**Tushuntirish:** Swoole korutinalari foydalanuvchi makonidagi (user-space) yengil iplar bo'lib, har bir korutina o'z stackiga ega. Soket orqali I/O kutilayotgan vaqtda Swoole runtime avtomatik ravishda korutinani to'xtatadi (yield) va navbatdagi korutinani bajaradi (resume). Natijada bloklanishsiz maksimal tezlikka erishiladi.

---

### Topshiriq #1103: Swoole Asinxron UDP Telemetriya Serveri
**Tavsif:** IoT qurilmalardan va GPS trekerlardan soniyasiga o'n minglab sensor ko'rsatkichlarini uzluksiz, ulanish o'rnatmasdan (connectionless) qabul qiluvchi yuqori tezlikdagi UDP serverini yarating.
**Talablar:** Swoole\Server da SWOOLE_SOCK_UDP rejimini tanlash, Packet hodisasi, mijozga UDP orqali ACK qaytarish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Yuqori tezlikdagi Swoole UDP Telemetriya Serveri
use Swoole\Server;

// UDP protokoli bilan server yaratamiz
$server = new Server("0.0.0.0", 9502, SWOOLE_PROCESS, SWOOLE_SOCK_UDP);

$server->set([
    'worker_num' => swoole_cpu_num(),
    'open_cpu_affinity' => true, // Har bir workerni aniq bitta CPU yadrosiga bog'lash
]);

// UDP da Connect yoki Close hodisalari bo'lmaydi, faqat Packet hodisasi bo'ladi
$server->on('Packet', function (Server $serv, string $data, array $clientInfo) {
    // Kelgan telemetriya ma'lumotlarini tekshiramiz
    $ip = $clientInfo['address'];
    $port = $clientInfo['port'];
    
    // Ikkilik yoki JSON paketni o'qiymiz
    $payload = @json_decode($data, true);
    if ($payload && isset($payload['device_id'], $payload['lat'], $payload['lng'])) {
        // Telemetriyani qayta ishlash
        $ack = json_encode(['status' => 'OK', 'dev' => $payload['device_id'], 'ts' => microtime(true)]);
        // Javobni aynan o'sha manzil va portga UDP paket qilib qaytaramiz
        $serv->sendto($ip, $port, $ack);
    } else {
        $serv->sendto($ip, $port, "ERR_INVALID_PACKET");
    }
});

echo "Swoole UDP Telemetriya Server 0.0.0.0:9502 da faol...
";
$server->start();
```
**Tushuntirish:** UDP protokoli handshake talab qilmaydi, shu sababli minimal kechikish (latency) bilan ishlaydi. `open_cpu_affinity` parametri orqali Linux OS darajasida har bir Swoole jarayoni alohida CPU yadrosiga biriktiriladi (Core affinity), bu esa kesh almashinuvi yo'qotishlarini nolga tushiradi.

---

### Topshiriq #1104: Swoole Task Worker orqali Og'ir Hisob-kitoblarni Fondan Bajarish
**Tavsif:** Tarmoq serveriga kelgan PDF generatsiya yoki sun'iy intellekt matn tahlili kabi uzoq davom etadigan CPU-bound vazifalarni asosiy event-loopni qotirmasdan Task Worker jarayonlariga uzatuvchi mexanizm yarating.
**Talablar:** task_worker_num sozlamasi, task va finish hodisalarini realizatsiya qilish, $server->task() chaqiruvidan foydalanish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Swoole Asinxron Task Worker Arxitekturasi
use Swoole\Server;

$server = new Server("0.0.0.0", 9503);

$server->set([
    'worker_num'      => 4,  // Tarmoq I/O ni boshqaruvchi oddiy workerlar
    'task_worker_num' => 8,  // Og'ir CPU vazifalarni bajaruvchi maxsus task workerlar
    'task_enable_coroutine' => true, // Task worker ichida ham korutinalardan foydalanish
]);

$server->on('Receive', function (Server $serv, int $fd, int $reactorId, string $data) {
    $request = trim($data);
    echo "[I/O Worker] So'rov qabul qilindi. Task workerga uzatilmoqda...
";
    
    // Og'ir vazifani fonga topshiramiz (asinxron, bloklanmasdan darhol qaytadi)
    $taskId = $serv->task(['fd' => $fd, 'payload' => $request]);
    
    // Mijozga vazifa qabul qilinganligi haqida tezkor tasdiq beramiz
    $serv->send($fd, "Vazifa qabul qilindi. Navbat ID: {$taskId}
");
});

// Task Worker jarayonida bajariladigan hodisa
$server->on('Task', function (Server $serv, Swoole\Server\Task $task) {
    $data = $task->data;
    $fd = $data['fd'];
    $text = $data['payload'];
    
    echo "[Task Worker #{$task->worker_id}] Og'ir tahlil bajarilmoqda: {$text}...
";
    
    // Og'ir matematik yoki kriptografik amallar simulyatsiyasi
    $hash = hash_pbkdf2("sha256", $text, "salt_khorazmiy", 100000, 32);
    
    // Natijani finish hodisasiga yuboramiz
    $task->finish(['fd' => $fd, 'hash' => $hash]);
});

// Vazifa to'liq tugaganda chaqiriladigan hodisa
$server->on('Finish', function (Server $serv, int $taskId, $data) {
    $fd = $data['fd'];
    $hash = $data['hash'];
    echo "[Finish] Task {$taskId} tugadi. Mijozga yakuniy natija yuborilmoqda.
";
    
    if ($serv->exist($fd)) {
        $serv->send($fd, "HISOBLASH YAKUNI: {$hash}
");
    }
});

$server->start();
```
**Tushuntirish:** Event-loop arxitekturasida eng katta xavf - bitta bloklovchi yoki uzoq davom etuvchi amaliyot barcha boshqa mijozlarni to'xtatib qo'yishidir. Swoole Task Worker mexanizmi tarmoq I/O bilan og'ir CPU hisob-kitoblarini alohida jarayon havzalariga (process pool) ajratish orqali yuqori responsivlikni ta'minlaydi.

---

### Topshiriq #1105: Swoole Coroutine Channel orqali CSP (Go-style) Xabar Almashinuvi
**Tavsif:** Go tilidagi chan kanallariga o'xshash, korutinalar o'rtasida ma'lumotlarni xavfsiz va xotiradan nusxa olmasdan yetkazuvchi CSP (Communicating Sequential Processes) konveyerini quring.
**Talablar:** Swoole\Coroutine\Channel, push va pop operatsiyalari, ishlab chiqaruvchi-iste'molchi (producer-consumer) modeli.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Swoole Coroutine Channel (CSP modeli)
use Swoole\Coroutine;
use Swoole\Coroutine\Channel;
use function Swoole\Coroutine\run;

run(function () {
    // 5 ta element sig'imga ega buferlangan kanal yaratamiz
    $channel = new Channel(5);

    // 1-Korutina: Ishlab chiqaruvchi (Producer)
    Coroutine::create(function () use ($channel) {
        for ($i = 1; $i <= 10; $i++) {
            $metric = [
                'id' => $i,
                'cpu_load' => rand(10, 95),
                'ram_usage' => rand(40, 85),
                'timestamp' => microtime(true)
            ];
            
            // Agar kanal to'lgan bo'lsa, push() avtomatik kutish rejimiga o'tadi
            $channel->push($metric);
            echo "[Ishlab chiqaruvchi] Metrika yuborildi: #{$i}
";
            Coroutine::sleep(0.05); // 50 ms kechikish
        }
        $channel->close(); // Kanalni yopamiz
    });

    // 2-Korutina: Iste'molchi (Consumer)
    Coroutine::create(function () use ($channel) {
        while (true) {
            // Agar kanal bo'sh bo'lsa, pop() yangi ma'lumot kelguncha kutadi
            $data = $channel->pop();
            if ($data === false) {
                // Kanal yopilgan va boshqa ma'lumot yo'q
                echo "[Iste'molchi] Kanal yopildi, barcha ma'lumotlar qayta ishlandi.
";
                break;
            }
            
            echo "[Iste'molchi] Qayta ishlandi -> ID: {$data['id']}, CPU: {$data['cpu_load']}%, RAM: {$data['ram_usage']}%
";
        }
    });
});
```
**Tushuntirish:** Swoole Channel dasturchiga umumiy xotirani qulflar (mutex/locks) orqali boshqarish o'rniga, 'Do not communicate by sharing memory; instead, share memory by communicating' tamoyiliga asoslangan xavfsiz parallelizmni taqdim etadi.

---

### Topshiriq #1106: Swoole Coroutine Pool bilan Parallel API Scraping
**Tavsif:** Tizim resurslarini tugatmaslik uchun bir vaqtning o'zida maksimal 5 ta faol korutina bilan 50 ta tashqi HTTP API manzilidan ma'lumotlarni parallel tortib oluvchi Pool mexanizmini yarating.
**Talablar:** Swoole\Coroutine\Barrier yoki Channel asosidagi Pool, Swoole\Coroutine\Http\Client.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Cheklangan Coroutine Pool orqali Parallel HTTP Fetching
use Swoole\Coroutine;
use Swoole\Coroutine\Channel;
use Swoole\Coroutine\Http\Client;
use function Swoole\Coroutine\run;

run(function () {
    $totalTasks = 20;
    $concurrencyLimit = 4; // Bir vaqtning o'zida ko'pi bilan 4 ta so'rov
    
    $queue = new Channel($totalTasks);
    for ($i = 1; $i <= $totalTasks; $i++) {
        $queue->push("https://jsonplaceholder.typicode.com/todos/{$i}");
    }
    $queue->close();

    $results = [];
    $barrier = Swoole\Coroutine\Barrier::make();

    // Limit miqdoricha worker korutinalarni ishga tushiramiz
    for ($w = 1; $w <= $concurrencyLimit; $w++) {
        Coroutine::create(function () use ($w, $queue, &$results, $barrier) {
            while ($url = $queue->pop()) {
                $parsed = parse_url($url);
                $client = new Client($parsed['host'], 443, true);
                $client->set(['timeout' => 3.0]);
                $client->get($parsed['path']);
                
                if ($client->statusCode === 200) {
                    $json = json_decode($client->body, true);
                    $results[] = "Worker {$w}: ID {$json['id']} - {$json['title']}";
                } else {
                    $results[] = "Worker {$w}: Xato {$url} - Status: {$client->statusCode}";
                }
                $client->close();
            }
        });
    }

    // Barcha korutinalar yakunlanishini asinxron kutamiz
    Swoole\Coroutine\Barrier::wait($barrier);

    echo "--- Barcha so'rovlar muvaffaqiyatli yakunlandi (" . count($results) . " ta) ---
";
    foreach (array_slice($results, 0, 5) as $res) {
        echo $res . "
";
    }
});
```
**Tushuntirish:** `Swoole\Coroutine\Barrier` C darajasida boshqariladigan hisoblagich bo'lib, Go tilidagi `sync.WaitGroup` kabi ishlaydi. Korutina havzasi cheklovi (Concurrency limiting) orqali server o'z xotirasi va tashqi API larning Rate-Limit chegaralarini himoya qiladi.

---

### Topshiriq #1107: Swoole Yuqori Aniqlikdagi Asinxron Taymerlar va Rejalashtiruvchi
**Tavsif:** Linux ning cron dasturisiz, mikrosekund darajasidagi aniqlik bilan doimiy yurak urishi (heartbeat) va har 5 soniyada tizim tozalash vazifalarini asinxron bajaruvchi taymer tizimini quring.
**Talablar:** Swoole\Timer::tick, Swoole\Timer::after, Swoole\Timer::clear funksiyalaridan foydalanish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Swoole Asinxron Taymerlar Tizimi
use Swoole\Timer;
use function Swoole\Coroutine\run;

run(function () {
    echo "Taymerlar ishga tushirilmoqda...
";

    // 1-Taymer: Har 500 ms da ishlaydigan yurak urishi (Heartbeat)
    $pulseCount = 0;
    $pulseTimerId = Timer::tick(500, function (int $timerId) use (&$pulseCount) {
        $pulseCount++;
        echo "[PULSE] Taymer #{$timerId} urdi ({$pulseCount}-marta) - Xotira: " . memory_get_usage(true) . " bayt
";
        
        // 6 marta urgandan so'ng taymerni to'xtatamiz
        if ($pulseCount >= 6) {
            Timer::clear($timerId);
            echo "[PULSE] Taymer to'xtatildi.
";
        }
    });

    // 2-Taymer: Bir martalik kechiktirilgan vazifa (One-off after 2 seconds)
    Timer::after(2000, function () {
        echo "[BIR MARTALIK] 2 soniya o'tdi: Kesh jadvallari tozalandi!
";
    });

    // 3-Taymer: Korutina kontekstida asinxron so'rov bajaruvchi taymer
    Timer::tick(1000, function (int $id) {
        static $checks = 0;
        $checks++;
        echo "[HEALTH-CHECK] Mikroxizmatlar holati tekshirildi (OK) [Iteratsiya: {$checks}]
";
        if ($checks >= 3) {
            Timer::clear($id);
        }
    });
});
```
**Tushuntirish:** Swoole taymerlari Linux kernelining `epoll` yoki `timerfd` mexanizmlariga tayanadi. Ular min-heap (minimal to'p) ma'lumot tuzilmasidan foydalanib eng yaqin taymer vaqtini hisoblaydi, bu esa O(1) vaqt murakkabligida minglab taymerlarni bir vaqtda boshqarish imkonini beradi.

---

### Topshiriq #1108: Swoole TCP Heartbeat Detection va O'lik Ulanishlarni Tozalash
**Tavsif:** Tarmoq uzilishi yoki mijoz qurilmasi elektr quvvatisiz o'chib qolishi sababli ochiq qolgan 'o'lik' TCP soketlarni aniqlab, server xotirasini tejash uchun ularni avtomatik yopuvchi mexanizm joriy qiling.
**Talablar:** heartbeat_check_interval va heartbeat_idle_time sozlamalarini konfiguratsiya qilish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Swoole Avtomatik Heartbeat Detection
use Swoole\Server;

$server = new Server("0.0.0.0", 9504);

$server->set([
    'worker_num'               => 2,
    // Har 5 soniyada barcha ulanishlarni tekshiradi
    'heartbeat_check_interval' => 5,
    // Agar mijoz 10 soniya davomida birorta ham bayt jo'natmasa, ulanish yopiladi
    'heartbeat_idle_time'      => 10,
]);

$server->on('Connect', function (Server $serv, int $fd) {
    echo "[+] Yangi ulanish: FD {$fd}. Agar 10 soniya sukut saqlansa, yopiladi.
";
});

$server->on('Receive', function (Server $serv, int $fd, int $reactorId, string $data) {
    $msg = trim($data);
    echo "[FD {$fd}] Xabar: {$msg}
";
    
    if ($msg === "PING") {
        $serv->send($fd, "PONG
");
    } else {
        $serv->send($fd, "OK: Qabul qilindi
");
    }
});

$server->on('Close', function (Server $serv, int $fd) {
    echo "[-] Ulanish uzildi: FD {$fd} (Mijoz chiqdi yoki Heartbeat timeout bo'ldi)
";
});

echo "Heartbeat nazoratiga ega TCP server 9504-portda ishlamoqda...
";
$server->start();
```
**Tushuntirish:** TCP ning o'zining Keep-Alive mexanizmi odatda 2 soatlik intervalda ishlaydi, bu sanoat tizimlari uchun juda sekin. Swoole ichki Master ipi har bir ulanishning `last_time` vaqtini kuzatib boradi va `heartbeat_idle_time` dan oshgan soketlarni avtomatik yopadi.

---

### Topshiriq #1109: Swoole SSL/TLS Shifrlangan Xavfsiz TCP Server
**Tavsif:** Mijoz va server o'rtasidagi barcha maxfiy moliyaviy ma'lumotlarni TLS 1.3 protokoli orqali shifrlab uzatuvchi xavfsiz TCP soket serverini ishlab chiqing.
**Talablar:** SWOOLE_SOCK_TCP | SWOOLE_SSL rejimini yoqish, ssl_cert_file, ssl_key_file va ssl_protocols parametrlarini sozlash.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Swoole SSL/TLS Xavfsiz TCP Soket Serveri
use Swoole\Server;

// SWOOLE_SSL bayrog'i bilan server yaratamiz
$server = new Server("0.0.0.0", 9505, SWOOLE_PROCESS, SWOOLE_SOCK_TCP | SWOOLE_SSL);

$server->set([
    'worker_num'       => 2,
    'ssl_cert_file'    => __DIR__ . '/certs/server.crt', // X.509 ommaviy sertifikat
    'ssl_key_file'     => __DIR__ . '/certs/server.key', // Maxfiy RSA/ECDSA kalit
    'ssl_protocols'    => SWOOLE_SSL_TLSv1_2 | SWOOLE_SSL_TLSv1_3, // Zaif SSL v3 va TLS 1.0/1.1 ni taqiqlash
    'ssl_ciphers'      => 'HIGH:!aNULL:!MD5',
    'ssl_verify_peer'  => false, // Zarur bo'lsa mTLS uchun true qilinadi
]);

$server->on('Connect', function (Server $serv, int $fd) {
    echo "[TLS] Yangi shifrlangan kanal ulandi: FD {$fd}
";
});

$server->on('Receive', function (Server $serv, int $fd, int $reactorId, string $data) {
    echo "[TLS O'qildi] " . trim($data) . "
";
    $serv->send($fd, "SECURE_ACK: Shifrlangan kanal orqali qabul qilindi
");
});

$server->on('Close', function (Server $serv, int $fd) {
    echo "[TLS] Aloqa yopildi: FD {$fd}
";
});

echo "Xavfsiz TLS TCP Server 9505-portda ishlamoqda...
";
$server->start();
```
**Tushuntirish:** Swoole OpenSSL kutubxonasi bilan bevosita integratsiyalashgan. TLS handshake bosqichi C sathida asinxron bajariladi, bu esa PHP interpreteriga shifrlash va kalit almashish (Diffie-Hellman) yukini tushirmaydi.

---

### Topshiriq #1110: Swoole Unix Domain Socket (UDS) orqali Yuqori Tezlikdagi IPC
**Tavsif:** Bitta server ichida ishlaydigan mikroxizmatlar o'rtasida TCP tarmoq stackining (IP/TCP headerlar, routing, cheksum) ortiqcha yukisiz, Linux UDS fayl deskriptori orqali maksimal tezlikda xabar almashing.
**Talablar:** SWOOLE_UNIX_STREAM soket turi, fayl yo'li (/tmp/service.sock), ulanish huquqlari.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Unix Domain Socket (UDS) Server
use Swoole\Server;

$sockFile = "/tmp/khorazmiy_ipc.sock";
if (file_exists($sockFile)) {
    unlink($sockFile); // Eski qoldiq soket faylini o'chiramiz
}

$server = new Server($sockFile, 0, SWOOLE_PROCESS, SWOOLE_UNIX_STREAM);

$server->set([
    'worker_num' => 2,
]);

$server->on('Receive', function (Server $serv, int $fd, int $reactorId, string $data) {
    // UDS orqali kelgan tezkor so'rov
    $decoded = json_decode($data, true);
    $response = json_encode([
        'status' => 'SUCCESS',
        'pid' => getmypid(),
        'echo' => $decoded['cmd'] ?? 'none'
    ]);
    
    $serv->send($fd, $response . "
");
});

$server->on('Start', function () use ($sockFile) {
    // Soket fayliga barcha foydalanuvchilar yoza olishi uchun huquq beramiz
    chmod($sockFile, 0777);
    echo "Unix Domain Socket server faol: {$sockFile}
";
});

$server->start();
```
**Tushuntirish:** Unix Domain Socket ma'lumotlarni tarmoq drayveri orqali emas, bevosita Linux yadrosi xotira buferlari (kernel page cache) orqali nusxalaydi. Natijada kechikish (latency) 1-2 mikrosekundgacha qisqaradi va o'tkazuvchanlik 2-3 barobar oshadi.

---

### Topshiriq #1111: Swoole HTTP/2 Server va Multiplexing
**Tavsif:** HTTP/2 protokoli imkoniyatlaridan foydalangan holda, bitta TCP ulanish orqali bir vaqtning o'zida bir nechta parallel so'rovlarni (Multiplexing) qabul qiluvchi va Server Push orqali CSS resurslarini uzatuvchi HTTP/2 serverini yarating.
**Talablar:** open_http2_protocol parametri, SSL sertifikati (ALPN h2 talabi), Swoole\Http\Server.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Swoole HTTP/2 Server
use Swoole\Http\Server;
use Swoole\Http\Request;
use Swoole\Http\Response;

$server = new Server("0.0.0.0", 9506, SWOOLE_PROCESS, SWOOLE_SOCK_TCP | SWOOLE_SSL);

$server->set([
    'ssl_cert_file'        => __DIR__ . '/certs/server.crt',
    'ssl_key_file'         => __DIR__ . '/certs/server.key',
    'open_http2_protocol'  => true, // HTTP/2 ni faollashtirish
    'worker_num'           => 4,
]);

$server->on('Request', function (Request $request, Response $response) {
    $uri = $request->server['request_uri'];

    if ($uri === '/') {
        // HTTP/2 Server Push: Brauzer hali so'ramasdan turib stillar faylini yuboramiz
        $response->push('/style.css', file_get_contents(__DIR__ . '/public/style.css'));
        
        $response->header('Content-Type', 'text/html; charset=utf-8');
        $response->end("<h1>Khorazmiy AI: HTTP/2 Server faol!</h1><link rel='stylesheet' href='/style.css'>");
    } elseif ($uri === '/style.css') {
        $response->header('Content-Type', 'text/css');
        $response->end("body { background: #111; color: #00ffcc; font-family: sans-serif; }");
    } else {
        $response->status(404);
        $response->end("404 Not Found");
    }
});

echo "HTTP/2 Server https://127.0.0.1:9506 manzilida ishga tushdi...
";
$server->start();
```
**Tushuntirish:** HTTP/2 ikkilik (binary framing) darajasida ishlaydi va oqimlarni (streams) bitta TCP kanalida multiplekslaydi. Server Push esa brauzer sahifani tahlil qilmasdanoq zarur CSS va JS fayllarni mijoz keshiga oldindan to'ldirib qo'yadi.

---

### Topshiriq #1112: Swoole Coroutine MySQL Client Connection Pool
**Tavsif:** Har bir foydalanuvchi so'rovi uchun yangidan MySQL TCP ulanishini ochish qimmatga tushishi sababli, 20 ta doimiy ulanishni asinxron korutinalar o'rtasida qayta taqsimlovchi Connection Pool yarating.
**Talablar:** Swoole\Coroutine\MySQL, Swoole\Coroutine\Channel asosida Pool boshqaruvi, put va get operatsiyalari.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Asinxron MySQL Connection Pool
use Swoole\Coroutine;
use Swoole\Coroutine\Channel;
use Swoole\Coroutine\MySQL;
use function Swoole\Coroutine\run;

class MySQLPool {
    protected Channel $pool;
    protected array $config;
    protected int $capacity;

    public function __construct(array $config, int $capacity = 10) {
        $this->config = $config;
        $this->capacity = $capacity;
        $this->pool = new Channel($capacity);

        // Boshlang'ich ulanishlar havzasini to'ldiramiz
        for ($i = 0; $i < $capacity; $i++) {
            $db = new MySQL();
            $db->connect($this->config);
            $this->pool->push($db);
        }
    }

    public function get(): MySQL {
        // Havzadan bo'sh ulanishni olamiz (bo'sh bo'lmasa kutadi)
        return $this->pool->pop();
    }

    public function put(MySQL $db): void {
        // Ishlatib bo'lingach, havzaga qaytaramiz
        $this->pool->push($db);
    }
}

run(function () {
    $dbConfig = [
        'host'     => '127.0.0.1',
        'port'     => 3306,
        'user'     => 'root',
        'password' => 'secret',
        'database' => 'fintech',
    ];

    $pool = new MySQLPool($dbConfig, 5);

    // 20 ta parallel korutina 5 ta ulanish havzasidan navbat bilan foydalanadi
    for ($i = 1; $i <= 20; $i++) {
        Coroutine::create(function () use ($pool, $i) {
            $db = $pool->get();
            try {
                $stmt = $db->prepare('SELECT ? as task_id, NOW() as current_time');
                $result = $stmt->execute([$i]);
                echo "[Korutina #{$i}] Ma'lumot olindi: " . json_encode($result) . "
";
            } finally {
                $pool->put($db); // Ulanishni havzaga xavfsiz qaytarish
            }
        });
    }
});
```
**Tushuntirish:** RDBMS (MySQL/PostgreSQL) ga TCP handshake va autentifikatsiya 10-50 ms vaqt oladi. Asinxron Connection Pool ulanishlarni ochiq saqlab, korutinalarga mikrosoniyalarda yetkazadi, bu esa tranzaksiyalar o'tkazuvchanligini o'nlab barobarga oshiradi.

---

### Topshiriq #1113: Swoole Coroutine Redis Client va Pub/Sub Boshqaruvi
**Tavsif:** Real-vaqt xabar almashinuvi uchun Redis Pub/Sub kanaliga obuna bo'luvchi (subscribe) va boshqa korutinadan turib o'sha kanalga xabar jo'natuvchi (publish) asinxron mijozni yarating.
**Talablar:** Swoole\Coroutine\Redis, subscribe, publish va recv funksiyalaridan foydalanish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Swoole Coroutine Redis Pub/Sub
use Swoole\Coroutine;
use Swoole\Coroutine\Redis;
use function Swoole\Coroutine\run;

run(function () {
    $channelName = "khorazmiy_notifications";

    // 1-Korutina: Obunachi (Subscriber)
    Coroutine::create(function () use ($channelName) {
        $redis = new Redis();
        $redis->connect('127.0.0.1', 6379);
        echo "[Obunachi] '{$channelName}' kanaliga obuna bo'lmoqda...
";
        
        $redis->subscribe([$channelName]);
        
        // Redisdan keladigan xabarlarni doimiy o'qish
        while ($msg = $redis->recv()) {
            // $msg[0] = 'message', $msg[1] = kanal, $msg[2] = xabar matni
            if ($msg[0] === 'message') {
                echo "[YANGI XABAR] Kanal: {$msg[1]} | Mazmun: {$msg[2]}
";
                if ($msg[2] === "STOP") {
                    break;
                }
            }
        }
        $redis->close();
    });

    // 2-Korutina: Tarqatuvchi (Publisher)
    Coroutine::create(function () use ($channelName) {
        Coroutine::sleep(0.5); // Obunachi ulanib olishi uchun biroz kutamiz
        $redis = new Redis();
        $redis->connect('127.0.0.1', 6379);

        for ($i = 1; $i <= 3; $i++) {
            $payload = json_encode(['event' => 'ALERT', 'msg' => "DDoS urinishi qaytarildi #{$i}"]);
            $redis->publish($channelName, $payload);
            echo "[Tarqatuvchi] Xabar yuborildi: #{$i}
";
            Coroutine::sleep(0.2);
        }

        $redis->publish($channelName, "STOP");
        $redis->close();
    });
});
```
**Tushuntirish:** Swoole Redis korutina mijozi reaktiv holda ishlaydi. `recv()` metodi Redisdan xabar kelmaguncha CPU ni band qilmasdan operatsion tizim kutish rejimiga o'tadi, natijada bitta jarayonda yuzlab alohida kanallarni tinglash mumkin.

---

### Topshiriq #1114: OpenSwoole Coroutine Mutex va Race Condition Oldini Olish
**Tavsif:** Parallel ishlayotgan korutinalar umumiy hisoblagich (bank balansi) qiymatini o'zgartirganda ma'lumotlar buzilishini (Race Condition) Mutex (Lock) yordamida himoyalang.
**Talablar:** OpenSwoole\Coroutine\Lock yoki Channel orqali semafor, atomik inkrement.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - OpenSwoole Coroutine Lock / Mutex
use OpenSwoole\Coroutine;
use OpenSwoole\Coroutine\Lock;
use function OpenSwoole\Coroutine\run;

run(function () {
    $balance = 1000; // Boshlang'ich umumiy balans
    $lock = new Lock(); // Korutina xavfsiz qulfi
    $barrier = OpenSwoole\Coroutine\Barrier::make();

    // 10 ta parallel korutina balansdan 100 dan pul yechadi
    for ($i = 1; $i <= 10; $i++) {
        Coroutine::create(function () use (&$balance, $lock, $barrier, $i) {
            // Kritik hududga kirishdan oldin qulflaymiz
            $lock->lock();
            try {
                // Balansni tekshirish va o'zgartirish
                $current = $balance;
                Coroutine::sleep(0.01); // Tarmoq yoki disk amali simulyatsiyasi
                $balance = $current - 100;
                echo "[Tranzaksiya #{$i}] Balans yangilandi: {$balance}
";
            } finally {
                // Har doim qulfni ochamiz
                $lock->unlock();
            }
        });
    }

    OpenSwoole\Coroutine\Barrier::wait($barrier);
    echo "Yakuniy xavfsiz balans: {$balance} (Kutilgan: 0)
";
});
```
**Tushuntirish:** PHP an'anaviy ravishda shared-nothing modelida ishlaydi, biroq Swoole/OpenSwoole korutinalari umumiy jarayon xotirasiga murojaat qila oladi. Asinxron amallar paytida race condition yuzaga kelmasligi uchun korutina-darajasidagi Mutex locklari shart.

---

### Topshiriq #1115: Swoole Graceful Shutdown va Worker Zero-Downtime Reload
**Tavsif:** Serverda yangi PHP kod versiyasi chiqqanda (deploy paytida) mavjud mijozlar bilan aloqani qo'pol uzmasdan, navbatdagi so'rovlarni kutib, xotiradagi kodni yangilovchi Reload mexanizmini yarating.
**Talablar:** SIGUSR1 signali bilan graceful reload, WorkerStop va WorkerStart hodisalarini boshqarish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Swoole Graceful Reload va Shutdown
use Swoole\Server;

$server = new Server("0.0.0.0", 9507);

$server->set([
    'worker_num'       => 2,
    'reload_async'     => true, // Asinxron reload (mavjud so'rovlar tugashini kutadi)
    'max_wait_time'    => 10,   // Worker yopilishini kutishning maksimal vaqti (soniya)
    'pid_file'         => __DIR__ . '/server.pid',
]);

$server->on('WorkerStart', function (Server $serv, int $workerId) {
    // Har bir worker yuklanganda yangi kod va konfiguratsiyalar keshdan toza o'qiladi
    opcache_reset();
    echo "[Worker #{$workerId}] Yangi kod bilan ishga tushdi (PID: " . getmypid() . ")
";
});

$server->on('WorkerStop', function (Server $serv, int $workerId) {
    echo "[Worker #{$workerId}] Xavfsiz to'xtatildi (Graceful exit)
";
});

$server->on('Receive', function (Server $serv, int $fd, int $reactorId, string $data) {
    // Uzun davom etadigan operatsiya
    Swoole\Coroutine::sleep(2);
    $serv->send($fd, "Khorazmiy AI: So'rov xavfsiz yakunlandi.
");
});

echo "Server ishga tushdi. Reload qilish uchun terminalda: kill -USR1 $(cat server.pid)
";
$server->start();
```
**Tushuntirish:** `reload_async` yoqilganda, Master jarayon SIGUSR1 signalini olgach, mavjud workerlarga yangi ulanishlarni berishni to'xtatadi, mavjud so'rovlarni oxirigacha yetkazishga imkon beradi va faqat shundan so'ng yangi kod yuklangan yangi workerlarni ko'taradi.

---

### Topshiriq #1116: ReactPHP Loop va Asinxron Hodisalar Navbati
**Tavsif:** ReactPHP EventLoop kutubxonasidan foydalanib, signallarni (SIGINT) ushlovchi, davriy taymerlarni boshqaruvchi va kelajakdagi mikrovazifalarni (futureTick) rejalashtiruvchi reaktiv tizim yarating.
**Talablar:** React\EventLoop\Loop, addPeriodicTimer, addTimer, futureTick va addSignal.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - ReactPHP Loop va Event-Driven Boshqaruv
require __DIR__ . '/vendor/autoload.php';

use React\EventLoop\Loop;

echo "ReactPHP Event Loop boshlanmoqda...
";

// 1. futureTick: Navbatdagi siklda darhol bajariladigan mikrotask
Loop::futureTick(function () {
    echo "[Microtask] Ushbu kod EventLoop ning keyingi iteratsiyasida darhol bajariladi.
";
});

// 2. Bir martalik taymer
Loop::addTimer(1.5, function () {
    echo "[Timer] 1.5 soniya o'tib ushbu asinxron callback ishladi.
";
});

// 3. Doimiy takrorlanuvchi taymer
$counter = 0;
$periodic = Loop::addPeriodicTimer(0.5, function () use (&$counter, &$periodic) {
    $counter++;
    echo "[Periodic] Har 500 ms da: Iteratsiya #{$counter}
";
    if ($counter >= 4) {
        Loop::cancelTimer($periodic);
        echo "[Periodic] Davriy taymer bekor qilindi.
";
    }
});

// 4. Linux OS signallarini (Ctrl+C) asinxron tutib olish
Loop::addSignal(SIGINT, function (int $signal) {
    echo "
[Signal] SIGINT (Ctrl+C) qabul qilindi. Resurslar tozalanib chiqilmoqda...
";
    Loop::stop();
});

// Loopni ishga tushirish (bloklovchi usulda barcha asinxron hodisalar tugaguncha aylanadi)
Loop::run();
```
**Tushuntirish:** ReactPHP sof PHP da yozilgan bo'lib, C kengaytmalari (extension) talab qilmaydi. U Node.js arxitekturasi kabi bitta oqimli (single-threaded) event loop yuritadi va stream_select orqali asinxron non-blocking hodisalarni boshqaradi.

---

### Topshiriq #1117: ReactPHP Asinxron TCP Streaming Echo Server
**Tavsif:** ReactPHP Socket komponenti yordamida xotiradan minimal foydalanuvchi, har bir ulanishni alohida ConnectionInterface oqimi sifatida boshqaruvchi asinxron TCP server quring.
**Talablar:** React\Socket\SocketServer, React\Socket\ConnectionInterface, data va close hodisalari.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - ReactPHP Asinxron Streaming TCP Server
require __DIR__ . '/vendor/autoload.php';

use React\Socket\SocketServer;
use React\Socket\ConnectionInterface;

$server = new SocketServer('127.0.0.1:8080');

$server->on('connection', function (ConnectionInterface $connection) {
    $remote = $connection->getRemoteAddress();
    echo "[+] Yangi TCP ulanish: {$remote}
";
    
    // Mijozga xush kelibsiz xabari
    $connection->write("Khorazmiy AI ReactPHP TCP Serverga xush kelibsiz!
");

    // Ma'lumotlar oqimi kelganda
    $connection->on('data', function ($chunk) use ($connection, $remote) {
        echo "[Ma'lumot] {$remote} dan: " . trim($chunk) . "
";
        
        // Echo: qabul qilingan bo'lakni o'ziga qaytaramiz
        $connection->write("Echo: " . $chunk);
        
        if (trim($chunk) === 'quit') {
            $connection->end("Xayr!
");
        }
    });

    $connection->on('close', function () use ($remote) {
        echo "[-] Ulanish yopildi: {$remote}
";
    });

    $connection->on('error', function (Exception $e) use ($remote) {
        echo "[!] Xatolik {$remote}: " . $e->getMessage() . "
";
    });
});

echo "ReactPHP TCP Server 127.0.0.1:8080 portida eshitmoqda...
";
```
**Tushuntirish:** ReactPHP ulanishlarni `ReadableStreamInterface` va `WritableStreamInterface` orqali taqdim etadi. Oqimlar (streams) buferlash va xotira to'lib ketishining oldini olish uchun orqaga bosim (backpressure) boshqaruviga ega.

---

### Topshiriq #1118: ReactPHP Asinxron HTTP Server va PSR-7 So'rovlar Tahlili
**Tavsif:** ReactPHP HTTP moduli orqali Nginx/Apache webservislarisiz, sof PSR-7 standartidagi Request/Response obyektlari bilan ishlovchi mikro-veb server yarating.
**Talablar:** React\Http\HttpServer, React\Socket\SocketServer, Psr\Http\Message\ServerRequestInterface, React\Http\Message\Response.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - ReactPHP PSR-7 HTTP Server
require __DIR__ . '/vendor/autoload.php';

use Psr\Http\Message\ServerRequestInterface;
use React\Http\Message\Response;
use React\Http\HttpServer;
use React\Socket\SocketServer;

$http = new HttpServer(function (ServerRequestInterface $request) {
    $path = $request->getUri()->getPath();
    $method = $request->getMethod();

    if ($path === '/api/status' && $method === 'GET') {
        $data = [
            'status' => 'ONLINE',
            'engine' => 'ReactPHP HTTP/1.1',
            'memory_mb' => round(memory_get_usage(true) / 1024 / 1024, 2),
            'timestamp' => time()
        ];
        return Response::json($data);
    }

    if ($path === '/api/calculate' && $method === 'POST') {
        $body = (string)$request->getBody();
        $payload = json_decode($body, true);
        $val = $payload['value'] ?? 0;
        
        return Response::json([
            'result' => $val * 2,
            'processed_at' => microtime(true)
        ]);
    }

    return Response::plaintext("404 Sahifa topilmadi
")->withStatus(404);
});

$socket = new SocketServer('0.0.0.0:8081');
$http->listen($socket);

echo "ReactPHP HTTP Server http://127.0.0.1:8081 da ishga tushdi...
";
```
**Tushuntirish:** Ushbu arxitekturada har bir HTTP so'rov uchun yangi PHP jarayoni (process fork) qilinmaydi. Kod xotirada doimiy turadi va so'rovlar PSR-7 interfeysi orqali bir necha mikrosekundda qayta ishlanadi.

---

### Topshiriq #1119: ReactPHP Asinxron HTTP Client orqali Parallel Web Scraper
**Tavsif:** Bir vaqtning o'zida bir nechta axborot saytlarining yangiliklar sahifasini asinxron so'rov bilan yuklab oluvchi va eng tez javob qaytargan saytlarni saralovchi reaktiv skraper yarating.
**Talablar:** React\Http\Browser, Promise orqali natijalarni yig'ish, timeout sozlamalari.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - ReactPHP Asinxron HTTP Browser Scraper
require __DIR__ . '/vendor/autoload.php';

use React\Http\Browser;
use Psr\Http\Message\ResponseInterface;

$browser = new Browser();
// Maksimal kutish vaqtini 3 soniya qilib belgilaymiz
$browser = $browser->withTimeout(3.0);

$urls = [
    'https://httpbin.org/delay/1',
    'https://httpbin.org/ip',
    'https://httpbin.org/user-agent',
];

echo "Parallel so'rovlar jo'natilmoqda...
";
$start = microtime(true);

$promises = [];
foreach ($urls as $url) {
    $promises[$url] = $browser->get($url)->then(
        function (ResponseInterface $response) use ($url) {
            $len = strlen((string)$response->getBody());
            echo "[OK] {$url} muvaffaqiyatli yuklandi (Hajm: {$len} bayt, Status: {$response->getStatusCode()})
";
            return $len;
        },
        function (Exception $e) use ($url) {
            echo "[XATO] {$url} yuklanmadi: " . $e->getMessage() . "
";
            return 0;
        }
    );
}

// Barcha promislar yakunlangach umumiy vaqtni o'lchaymiz
React\Promise\all($promises)->then(function ($results) use ($start) {
    $totalTime = round(microtime(true) - $start, 3);
    echo "Barcha parallel so'rovlar {$totalTime} soniyada yakunlandi!
";
});
```
**Tushuntirish:** Sinxron `curl_exec` yoki `file_get_contents` har bir so'rovni ketma-ket (sequential) bajarib 3 ta so'rov uchun 3x vaqt sarflagan bo'lsa, ReactPHP `Browser` barcha soketlarni bitta event loopda parallel boshqaradi va umumiy vaqt eng sekin bitta so'rov vaqtiga teng bo'ladi.

---

### Topshiriq #1120: ReactPHP Streams va Piping orqali Katta Fayllarni Oqizish
**Tavsif:** Server xotirasini (RAM) to'ldirmasdan, gigabaytlab o'lchamdagi katta arxiv faylini diskdan o'qib, uni to'g'ridan-to'g'ri chiquvchi TCP soketiga uzatuvchi (Piping) mexanizm yarating.
**Talablar:** React\Stream\ReadableResourceStream, pipe funksiyasidan foydalanish, memory consumption tekshiruvi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - ReactPHP Memory-Safe Stream Piping
require __DIR__ . '/vendor/autoload.php';

use React\Socket\SocketServer;
use React\Socket\ConnectionInterface;
use React\Stream\ReadableResourceStream;

$server = new SocketServer('127.0.0.1:8082');

$server->on('connection', function (ConnectionInterface $connection) {
    echo "[+] Mijoz ulandi: " . $connection->getRemoteAddress() . ". Fayl oqizilmoqda...
";
    
    $filePath = __DIR__ . '/large_dataset.bin';
    if (!file_exists($filePath)) {
        // Test uchun 10MB li fayl yasaymiz
        file_put_contents($filePath, str_repeat("A", 10 * 1024 * 1024));
    }

    $fileHandle = fopen($filePath, 'r');
    // Faylni non-blocking o'qish oqimiga o'raymiz (bufer 64 KB)
    $fileStream = new ReadableResourceStream($fileHandle, null, 65536);

    // Xotiradan faqat 64KB foydalanib, to'g'ridan-to'g'ri soketga quvur (pipe) qilamiz
    $fileStream->pipe($connection);

    $fileStream->on('end', function () {
        echo "[+] Fayl to'liq uzatildi!
";
    });

    $connection->on('close', function () use ($fileHandle) {
        if (is_resource($fileHandle)) {
            fclose($fileHandle);
        }
    });
});

echo "Streaming fayl server 8082-portda faol...
";
```
**Tushuntirish:** `pipe()` mexanizmi Unix quvurlari kabi ishlaydi. Agar tarmoq mijozi sekin qabul qilayotgan bo'lsa (TCP window kichrayganda), ReactPHP o'qish oqimini vaqtincha to'xtatib turadi (pause), bu esa server RAM xotirasining shishib portlashini oldini oladi.

---

### Topshiriq #1121: ReactPHP Promise va Deferral orqali Asinxron Zanjirlar
**Tavsif:** Callback-hell muammosidan qochish uchun bir nechta asinxron bosqichlarni (foydalanuvchini tekshirish, balansni to'ldirish, SMS jo'natish) Promise zanjiri orqali bog'lang.
**Talablar:** React\Promise\Deferred, then, catch, finally zanjirlarini tuzish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - ReactPHP Promise va Deferred Zanjirlari
require __DIR__ . '/vendor/autoload.php';

use React\Promise\Deferred;
use React\Promise\PromiseInterface;
use React\EventLoop\Loop;

function verifyUserAsync(int $userId): PromiseInterface {
    $deferred = new Deferred();
    Loop::addTimer(0.1, function () use ($deferred, $userId) {
        if ($userId > 0) {
            $deferred->resolve(['id' => $userId, 'name' => 'Alisher', 'status' => 'ACTIVE']);
        } else {
            $deferred->reject(new Exception("Foydalanuvchi topilmadi!"));
        }
    });
    return $deferred->promise();
}

function processPaymentAsync(array $user, float $amount): PromiseInterface {
    $deferred = new Deferred();
    Loop::addTimer(0.1, function () use ($deferred, $user, $amount) {
        if ($amount <= 5000000) {
            $deferred->resolve(['tx_id' => uniqid('tx_'), 'user' => $user['name'], 'paid' => $amount]);
        } else {
            $deferred->reject(new Exception("Limitdan oshib ketdi!"));
        }
    });
    return $deferred->promise();
}

// Promise zanjirini ishga tushirish
verifyUserAsync(42)
    ->then(function ($user) {
        echo "[1-Qadam] Foydalanuvchi tasdiqlandi: {$user['name']}
";
        return processPaymentAsync($user, 150000.0);
    })
    ->then(function ($tx) {
        echo "[2-Qadam] To'lov muvaffaqiyatli: Tranzaksiya {$tx['tx_id']} - {$tx['paid']} UZS
";
    })
    ->catch(function (Throwable $e) {
        echo "[XATO] Zanjirda xatolik yuz berdi: " . $e->getMessage() . "
";
    })
    ->finally(function () {
        echo "[Yakun] Jarayon to'liq yakunlandi.
";
    });

Loop::run();
```
**Tushuntirish:** Deferred obyekti va'da (promise) yaratuvchisi va uning holatini boshqaruvchi (resolve/reject) vosita hisoblanadi. `then()` metodlari qiymat qaytarganda zanjir davom etadi, bu esa asinxron kodni toza va o'qishli saqlaydi.

---

### Topshiriq #1122: ReactPHP Async/Await Sintaksisi bilan Kodni Tozalash
**Tavsif:** `react/async` paketi yordamida PHP 8.1+ tolalari (Fibers) asosida asinxron promisalarni go'yo sinxron kod kabi toza, oson va try-catch orqali yozishni amalga oshiring.
**Talablar:** React\Async\async, React\Async\await funksiyalari, Fibers bilan integratsiya.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - ReactPHP Fiber asosidagi Async/Await
require __DIR__ . '/vendor/autoload.php';

use function React\Async\async;
use function React\Async\await;
use React\Http\Browser;
use React\EventLoop\Loop;

// async() funksiyasi yangi Fiber ichida ishlaydi
$fetchProfile = async(function (int $userId) {
    $browser = new Browser();
    echo "[Async] Foydalanuvchi #{$userId} ma'lumotlari so'ralmoqda...
";

    try {
        // await() orqali promisani sinxron kabi kutamiz, lekin event-loop bloklanmaydi
        $response = await($browser->get("https://jsonplaceholder.typicode.com/users/{$userId}"));
        $user = json_decode((string)$response->getBody(), true);
        
        $postsResponse = await($browser->get("https://jsonplaceholder.typicode.com/posts?userId={$userId}"));
        $posts = json_decode((string)$postsResponse->getBody(), true);

        return [
            'name' => $user['name'],
            'email' => $user['email'],
            'posts_count' => count($posts),
        ];
    } catch (Throwable $e) {
        echo "[Xato] Ma'lumot olishda xato: " . $e->getMessage() . "
";
        return null;
    }
});

// Funksiyani chaqiramiz
$fetchProfile(1)->then(function ($profile) {
    echo "Foydalanuvchi profili muvaffaqiyatli olindi:
";
    print_r($profile);
});

Loop::run();
```
**Tushuntirish:** PHP 8.1 da joriy qilingan `Fiber` mexanizmi dastur bajarilishini to'xtatib turish va istalgan nuqtadan qayta davom ettirish imkonini beradi. ReactPHP `await()` aynan shu Fiber yordamida Promisani yechadi, natijada callback zanjirlarisiz toza sinxron uslubda kod yozish mumkin bo'ladi.

---

### Topshiriq #1123: ReactPHP Asinxron DNS Resolver va Kesh
**Tavsif:** Tizimning standart bloklovchi `gethostbyname` funksiyasi o'rniga, minglab parallel tarmoq ulanishlari uchun DNS so'rovlarini asinxron yechuvchi va keshlovchi reaktiv DNS klient yarating.
**Talablar:** React\Dns\Resolver\Factory, InMemoryCache, resolve funksiyasi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - ReactPHP Asinxron DNS Resolver
require __DIR__ . '/vendor/autoload.php';

use React\Dns\Resolver\Factory;
use React\EventLoop\Loop;

$factory = new Factory();
// 1.1.1.1 Cloudflare DNS serveridan foydalanamiz va javoblarni xotirada keshlaymiz
$dns = $factory->createCached('1.1.1.1');

$domains = ['google.com', 'github.com', 'cloudflare.com', 'php.net'];

echo "Asinxron DNS qidiruvi boshlandi...
";

foreach ($domains as $domain) {
    $dns->resolve($domain)->then(
        function (string $ip) use ($domain) {
            echo "[DNS] {$domain} -> {$ip}
";
        },
        function (Exception $e) use ($domain) {
            echo "[DNS XATO] {$domain} topilmadi: " . $e->getMessage() . "
";
        }
    );
}

Loop::run();
```
**Tushuntirish:** Ko'pgina dasturchilar DNS yechish (lookup) amaliyoti operatsion tizim darajasida bloklovchi ekanligini hisobga olishmaydi. ReactPHP DNS resolveri UDP 53 portiga to'g'ridan-to'g'ri non-blocking so'rov jo'natadi va event loopni hech qachon qotirmaydi.

---

### Topshiriq #1124: ReactPHP Asinxron Child Process Boshqaruvi
**Tavsif:** PHP ilovasi ichidan og'ir Linux buyrug'ini (masalan ffmpeg yoki ping) alohida jarayonda ishga tushirib, uning stdout va stderr oqimlarini real vaqtda asinxron o'qib boruvchi mexanizm yarating.
**Talablar:** React\ChildProcess\Process, stdout on('data'), exit kodi monitoringi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - ReactPHP Asinxron Tashqi Jarayon (Child Process)
require __DIR__ . '/vendor/autoload.php';

use React\ChildProcess\Process;
use React\EventLoop\Loop;

// Tarmoqni tekshiruvchi ping buyrug'ini ishga tushiramiz
$cmd = (DIRECTORY_SEPARATOR === '\\') ? 'ping -n 4 8.8.8.8' : 'ping -c 4 8.8.8.8';
$process = new Process($cmd);

$process->start();

echo "Asinxron jarayon ishga tushirildi (PID: " . $process->getPid() . ")...
";

// stdout oqimini real vaqtda o'qish
$process->stdout->on('data', function ($chunk) {
    echo "[STDOUT] " . $chunk;
});

// stderr oqimi
$process->stderr->on('data', function ($chunk) {
    echo "[STDERR XATO] " . $chunk;
});

// Jarayon yakunlanganda
$process->on('exit', function ($exitCode, $termSignal) {
    echo "
Jarayon yakunlandi. Chiqish kodi: {$exitCode}
";
});

Loop::run();
```
**Tushuntirish:** Standart `exec()` yoki `shell_exec()` buyruq bajarilgunicha butun PHP jarayonini muzlatib qo'yadi. `React\ChildProcess` esa OS ning jarayonlar quvurlarini (pipes) asinxron soketlar sifatida ro'yxatdan o'tkazib, ma'lumotlarni oqim tarzida qabul qiladi.

---

### Topshiriq #1125: ReactPHP Asinxron Fayl I/O va Katta Jurnallarni Tahlil Qilish
**Tavsif:** Doimiy to'ldirilib borilayotgan server access.log faylini bloklanmasdan o'qib, undagi 500 statusli xatoliklarni filtrlovchi asinxron tahlil vositasini ishlab chiqing.
**Talablar:** Non-blocking fayl drayveri, oqimli qatorma-qator o'qish, xotira tejamkorligi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - ReactPHP Asinxron Fayl Oqimi Tahlili
require __DIR__ . '/vendor/autoload.php';

use React\Stream\ReadableResourceStream;
use React\EventLoop\Loop;

$logFile = __DIR__ . '/access.log';
// Sinov log faylini yaratib olamiz
file_put_contents($logFile, "GET /index.html 200\nPOST /api/pay 500\nGET /about 200\nPOST /checkout 500\n");

$stream = new ReadableResourceStream(fopen($logFile, 'r'));
$buffer = '';
$errorCount = 0;

$stream->on('data', function ($chunk) use (&$buffer, &$errorCount) {
    $buffer .= $chunk;
    while (($newlinePos = strpos($buffer, "\n")) !== false) {
        $line = substr($buffer, 0, $newlinePos);
        $buffer = substr($buffer, $newlinePos + 1);
        
        // 500 xatoliklarini qidiramiz
        if (str_contains($line, '500')) {
            $errorCount++;
            echo "[KRITIK XATO TOPILDI]: {$line}\n";
        }
    }
});

$stream->on('end', function () use (&$errorCount) {
    echo "Tahlil tugadi. Jami topilgan 500 xatolar soni: {$errorCount}\n";
});

Loop::run();
```
**Tushuntirish:** Katta fayllarni birdaniga `file_get_contents` bilan xotiraga yuklash serverni 'Out Of Memory' (OOM) holatiga olib keladi. Oqimli buferlash yordamida hatto 100 GB log fayllarni ham atigi bir necha megabayt xotira bilan tahlil qilish mumkin.

---

### Topshiriq #1126: Ratchet WebSocket Server va Real-Time Chat Arxitekturasi
**Tavsif:** Ratchet kutubxonasi yordamida brauzerlar va mobil mijozlar o'rtasida ikki tomonlama (full-duplex) tezkor xabarlar almashish imkonini beruvchi WebSocket serverini quring.
**Talablar:** Ratchet\MessageComponentInterface, SplObjectStorage orqali mijozlarni saqlash, onOpen, onMessage, onClose, onError.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Ratchet WebSocket Real-Time Chat Server
require __DIR__ . '/vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

class ChatServer implements MessageComponentInterface {
    protected \SplObjectStorage $clients;

    public function __construct() {
        // Ulangan barcha mijozlar (Connection) to'plami
        $this->clients = new \SplObjectStorage();
        echo "ChatServer initsializatsiya qilindi.
";
    }

    public function onOpen(ConnectionInterface $conn) {
        $this->clients->attach($conn);
        echo "[+] Yangi ulanish: ({$conn->resourceId})
";
        $conn->send(json_encode([
            'type' => 'SYSTEM',
            'message' => "Khorazmiy AI Chatga xush kelibsiz! Sizning ID: {$conn->resourceId}"
        ]));
    }

    public function onMessage(ConnectionInterface $from, $msg) {
        $numRecv = count($this->clients) - 1;
        echo sprintf('[Xabar] ID %d dan %d ta mijozga tarqatilmoqda: %s
', $from->resourceId, $numRecv, $msg);

        // Xabarni barcha ulangan boshqa mijozlarga tarqatamiz (Broadcast)
        foreach ($this->clients as $client) {
            if ($from !== $client) {
                $client->send(json_encode([
                    'from' => $from->resourceId,
                    'text' => $msg,
                    'time' => date('H:i:s')
                ]));
            }
        }
    }

    public function onClose(ConnectionInterface $conn) {
        $this->clients->detach($conn);
        echo "[-] Ulanish uzildi: ({$conn->resourceId})
";
    }

    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "[!] Xatolik ({$conn->resourceId}): {$e->getMessage()}
";
        $conn->close();
    }
}

// HTTP va WebSocket qatlamlarini birlashtirib 8085-portda ishga tushiramiz
$server = IoServer::factory(
    new HttpServer(
        new WsServer(
            new ChatServer()
        )
    ),
    8085
);

echo "Ratchet WebSocket Server ws://127.0.0.1:8085 manzilida faol...
";
$server->run();
```
**Tushuntirish:** WebSocket protokoli (RFC 6455) dastlab HTTP orqali 101 Switching Protocols sarlavhasi bilan Handshake qiladi va keyin ulanishni doimiy TCP ikkilik/matn oqimiga aylantiradi. `SplObjectStorage` PHP ning eng tezkor xotira to'plami bo'lib, ob'ektlarni O(1) vaqtda qo'shish va o'chirishni ta'minlaydi.

---

### Topshiriq #1127: Ratchet WAMP Protokoli orqali Pub/Sub va RPC Boshqaruvi
**Tavsif:** Oddiy xabarlar o'rniga, WAMP (Web Application Messaging Protocol) orqali mavzularga (topics) obuna bo'lish (Publish/Subscribe) va server funksiyalarini masofadan chaqirish (RPC) imkoniyatini yarating.
**Talablar:** Ratchet\Wamp\WampServerInterface, onPublish, onSubscribe, onCall realizatsiyasi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Ratchet WAMP Pub/Sub va RPC Server
require __DIR__ . '/vendor/autoload.php';

use Ratchet\ConnectionInterface;
use Ratchet\Wamp\WampServerInterface;

class MarketDataWampServer implements WampServerInterface {
    protected array $topics = [];

    public function onSubscribe(ConnectionInterface $conn, $topic) {
        echo "[Obuna] Mijoz ({$conn->resourceId}) mavzuga obuna bo'ldi: {$topic->getId()}
";
    }

    public function onPublish(ConnectionInterface $conn, $topic, $event, array $exclude, array $eligible) {
        echo "[Tarqatish] Mavzu: {$topic->getId()} -> Xabar: " . json_encode($event) . "
";
        // Mavzuga obuna bo'lgan barchaga yuboriladi
        $topic->broadcast($event);
    }

    public function onCall(ConnectionInterface $conn, $id, $topic, array $params) {
        // Masofaviy protsedura chaqiruvi (RPC)
        echo "[RPC Chaqiruv] Funksiya: {$topic->getId()} Mijoz: {$conn->resourceId}
";
        
        if ($topic->getId() === 'get_stock_price') {
            $symbol = $params[0] ?? 'UZS';
            $price = ($symbol === 'USD') ? 12850.00 : 1.0;
            $conn->callResult($id, ['symbol' => $symbol, 'price' => $price]);
        } else {
            $conn->callError($id, $topic, 'RPC Metod topilmadi');
        }
    }

    public function onUnSubscribe(ConnectionInterface $conn, $topic) {}
    public function onOpen(ConnectionInterface $conn) {}
    public function onClose(ConnectionInterface $conn) {}
    public function onError(ConnectionInterface $conn, \Exception $e) {}
}
```
**Tushuntirish:** WAMP protokoli WebSocket ustiga qurilgan yuqori darajadagi dasturlash modelidir. U bir tomondan Pub/Sub orqali birjalar va bildirishnomalarni tarqatsa, ikkinchi tomondan RPC orqali xuddi HTTP REST kabi aniq javob talab qiluvchi operatsiyalarni bajaradi.

---

### Topshiriq #1128: Ratchet WebSocket JWT Token Autentifikatsiyasi
**Tavsif:** WebSocket ulanishi ochilayotganda mijoz yuborgan URL so'rov parametrlaridan (`ws://...?token=...`) yoki Cookie-dan JWT tokenni tekshirib, begona va noqonuniy ulanishlarni zudlik bilan uzuvchi xavfsizlik qatlamini joriy qiling.
**Talablar:** Handshake bosqichida HttpRequest tahlili, Firebase\JWT dekodlash, nomaqbul ulanishni close() qilish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Ratchet WebSocket Xavfsiz JWT Autentifikatsiyasi
require __DIR__ . '/vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Firebase\JWT\JWT;
use Firebase\JWT\Key;

class SecureChatServer implements MessageComponentInterface {
    protected string $jwtSecret = "maxfiy_khorazmiy_kalit_2026";
    protected \SplObjectStorage $authenticatedClients;

    public function __construct() {
        $this->authenticatedClients = new \SplObjectStorage();
    }

    public function onOpen(ConnectionInterface $conn) {
        // Handshake paytidagi HTTP so'rov ma'lumotlarini olamiz
        $query = $conn->httpRequest->getUri()->getQuery();
        parse_str($query, $params);

        $token = $params['token'] ?? null;
        if (!$token) {
            echo "[-] Ulanish rad etildi: Token ko'rsatilmagan ({$conn->resourceId})
";
            $conn->close(4001); // 4001: Unauthorized
            return;
        }

        try {
            // JWT tokenni tekshirish va parslash
            $decoded = JWT::decode($token, new Key($this->jwtSecret, 'HS256'));
            $conn->userId = $decoded->user_id;
            $conn->username = $decoded->username;
            
            $this->authenticatedClients->attach($conn);
            echo "[+] Autentifikatsiya qilindi: {$conn->username} (User ID: {$conn->userId})
";
            $conn->send(json_encode(['status' => 'AUTHENTICATED', 'user' => $conn->username]));
        } catch (\Exception $e) {
            echo "[-] Noto'g'ri token: " . $e->getMessage() . "
";
            $conn->close(4003); // Forbidden
        }
    }

    public function onMessage(ConnectionInterface $from, $msg) {
        // Faqat autentifikatsiyadan o'tgan mijozlargina xabar yoza oladi
        if (!$this->authenticatedClients->contains($from)) {
            $from->close();
            return;
        }
        echo "[Xabar {$from->username}]: {$msg}
";
    }

    public function onClose(ConnectionInterface $conn) {
        $this->authenticatedClients->detach($conn);
    }

    public function onError(ConnectionInterface $conn, \Exception $e) {
        $conn->close();
    }
}
```
**Tushuntirish:** WebSocket protokoli odatdagi HTTP kabi har bir xabarda sarlavhalarni qayta uzatmaydi. Shu sababli xavfsizlik tekshiruvi Handshake bosqichida (`onOpen`) faqat bitta marta amalga oshiriladi va ulanish o'zgaruvchisiga (`$conn->user`) doimiy saqlanadi.

---

### Topshiriq #1129: Ratchet Xonalar (Rooms/Channels) va Guruhli Broadcasting
**Tavsif:** Foydalanuvchilarni alohida xonalar (masalan, `order_101`, `support_chat`) bo'yicha guruhlab, xabarlarni faqat o'sha xonaga a'zo bo'lgan mijozlargagina yetkazuvchi tizim yarating.
**Talablar:** Xonalar assotsiativ massivi, subscribe_room, leave_room va send_to_room buyruqlari.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Ratchet Xonalar va Kanallar Boshqaruvi
require __DIR__ . '/vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;

class RoomManager implements MessageComponentInterface {
    // Xonalar ro'yxati: ['room_name' => [resourceId => Connection]]
    protected array $rooms = [];

    public function onOpen(ConnectionInterface $conn) {
        echo "[+] Ulandi: {$conn->resourceId}
";
    }

    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        $action = $data['action'] ?? '';
        $room = $data['room'] ?? 'general';

        switch ($action) {
            case 'JOIN':
                $this->rooms[$room][$from->resourceId] = $from;
                $from->send(json_encode(['status' => 'JOINED', 'room' => $room]));
                $this->broadcastToRoom($room, "Foydalanuvchi {$from->resourceId} xonaga kirdi", $from);
                break;

            case 'LEAVE':
                unset($this->rooms[$room][$from->resourceId]);
                $from->send(json_encode(['status' => 'LEFT', 'room' => $room]));
                $this->broadcastToRoom($room, "Foydalanuvchi {$from->resourceId} xonani tark etdi", $from);
                break;

            case 'MESSAGE':
                $text = $data['text'] ?? '';
                $this->broadcastToRoom($room, "[{$room}] {$from->resourceId}: {$text}");
                break;
        }
    }

    protected function broadcastToRoom(string $room, string $message, ?ConnectionInterface $exclude = null): void {
        if (!isset($this->rooms[$room])) return;

        foreach ($this->rooms[$room] as $client) {
            if ($exclude && $client === $exclude) continue;
            $client->send(json_encode(['room' => $room, 'payload' => $message]));
        }
    }

    public function onClose(ConnectionInterface $conn) {
        // Mijoz barcha xonalardan chiqariladi
        foreach ($this->rooms as $room => $clients) {
            if (isset($clients[$conn->resourceId])) {
                unset($this->rooms[$room][$conn->resourceId]);
                $this->broadcastToRoom($room, "Mijoz {$conn->resourceId} aloqani uzdi");
            }
        }
    }

    public function onError(ConnectionInterface $conn, \Exception $e) {
        $conn->close();
    }
}
```
**Tushuntirish:** Barcha mijozlarga yoppasiga broadcast qilish katta miqyosda (10,000+ mijoz) tarmoq o'tkazuvchanligini behuda sarflaydi. Xonalar orqali marshrutlash xabarlarni faqat manfaatdor mijozlargagina yuborib, O(N) yuklamani O(K) ga (bu yerda K - xona a'zolari soni) tushiradi.

---

### Topshiriq #1130: Ratchet va Redis Pub/Sub Gorizontal Masshtablash
**Tavsif:** Bir nechta alohida serverlarda yoki podlarda ishlayotgan Ratchet WebSocket nusxalarini Redis Pub/Sub orqali sinxronlashtirib, bir serverdagi mijoz xabarini boshqa serverdagi mijozga yetkazing.
**Talablar:** Clue\React\Redis yoki Predis asinxron mijozi, EventLoop bilan integratsiya.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Ratchet + Redis Pub/Sub Gorizontal Masshtablash
require __DIR__ . '/vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;
use React\EventLoop\Loop;
use Clue\React\Redis\Factory as RedisFactory;

class ClusteredChat implements MessageComponentInterface {
    protected \SplObjectStorage $clients;
    protected $redisPublishClient;

    public function __construct($redisPublish) {
        $this->clients = new \SplObjectStorage();
        $this->redisPublishClient = $redisPublish;
    }

    public function onOpen(ConnectionInterface $conn) {
        $this->clients->attach($conn);
    }

    public function onMessage(ConnectionInterface $from, $msg) {
        // Xabarni to'g'ridan-to'g'ri emas, markaziy Redis kanaliga e'lon qilamiz
        $payload = json_encode([
            'sender' => $from->resourceId,
            'body' => $msg,
            'node_id' => gethostname()
        ]);
        $this->redisPublishClient->publish('cluster_chat_channel', $payload);
    }

    // Redisdan yangi xabar kelganda barcha mahalliy mijozlarga yetkazish
    public function deliverLocalMessage(string $rawJson): void {
        foreach ($this->clients as $client) {
            $client->send($rawJson);
        }
    }

    public function onClose(ConnectionInterface $conn) {
        $this->clients->detach($conn);
    }

    public function onError(ConnectionInterface $conn, \Exception $e) {
        $conn->close();
    }
}

$loop = Loop::get();
$redisFactory = new RedisFactory($loop);

// Redis Publish va Subscribe uchun 2 ta alohida asinxron ulanish
$redisFactory->createClient('127.0.0.1:6379')->then(function ($publishClient) use ($loop, $redisFactory) {
    $chatApp = new ClusteredChat($publishClient);

    $redisFactory->createClient('127.0.0.1:6379')->then(function ($subClient) use ($chatApp) {
        $subClient->subscribe('cluster_chat_channel');
        $subClient->on('message', function ($channel, $message) use ($chatApp) {
            $chatApp->deliverLocalMessage($message);
        });
    });

    $socket = new React\Socket\SocketServer('0.0.0.0:8090', [], $loop);
    $server = new IoServer(new HttpServer(new WsServer($chatApp)), $socket, $loop);
    echo "Clustered WebSocket tuguni 8090-portda va Redis Pub/Sub bilan ishlamoqda...
";
});

$loop->run();
```
**Tushuntirish:** WebSocket ulanishlari stateful bo'lganligi sababli, oddiy HTTP kabi Load Balancer orqali oson masshtablanmaydi. Redis Pub/Sub orqa miya (Backbone) vazifasini bajarib, turli klaster tugunlaridagi mijoziylarni yagona mantiqiy xonaga birlashtiradi.

---

### Topshiriq #1131: Swoole WebSocket Server va Binary Frame bilan Multimedia Uzatish
**Tavsif:** Matnli (JSON) ma'lumotlar o'rniga, mikrofon audio oqimi yoki kamera kadrlarini samarali ikkilik freymlarda (Binary Frames - Opcode 0x2) uzatuvchi Swoole WebSocket serverini yarating.
**Talablar:** Swoole\WebSocket\Server, SWOOLE_WEBSOCKET_OPCODE_BINARY, $frame->opcode tekshiruvi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Swoole Ikkilik (Binary) WebSocket Server
use Swoole\WebSocket\Server;
use Swoole\WebSocket\Frame;

$server = new Server("0.0.0.0", 9510);

$server->set([
    'worker_num' => 2,
    'open_websocket_close_frame' => true,
]);

$server->on('open', function (Server $server, $request) {
    echo "[+] Mijoz ulandi: {$request->fd}
";
});

$server->on('message', function (Server $server, Frame $frame) {
    // Agar xabar ikkilik (Binary) formatda bo'lsa
    if ($frame->opcode === WEBSOCKET_OPCODE_BINARY) {
        $binaryData = $frame->data;
        $byteLength = strlen($binaryData);
        echo "[Ikkilik Frame] Hajmi: {$byteLength} bayt (FD: {$frame->fd})
";

        // Ma'lumot boshidagi 4 baytli sehrli raqamni (magic bytes) tekshiramiz
        $magic = unpack('N', substr($binaryData, 0, 4))[1] ?? 0;

        // Barcha ulangan boshqa mijozlarga ikkilik baytlar oqimini tarqatamiz
        foreach ($server->connections as $fd) {
            if ($server->isEstablished($fd) && $fd !== $frame->fd) {
                $server->push($fd, $binaryData, WEBSOCKET_OPCODE_BINARY);
            }
        }
    } else {
        // Matnli buyruqlar
        echo "[Matn] " . $frame->data . "
";
        $server->push($frame->fd, "Faqat ikkilik audio/video oqim qabul qilinadi.");
    }
});

echo "Binary WebSocket Server 9510-portda tinglamoqda...
";
$server->start();
```
**Tushuntirish:** WebSocket ikkita asosiy ma'lumot freymiga ega: Opcode 0x1 (Matn/UTF-8) va Opcode 0x2 (Ikkilik baytlar). Audio, video va Protobuf ma'lumotlarini Base64 ga o'girmasdan to'g'ridan-to'g'ri Binary Frame orqali uzatish 33% tarmoq trafigini va katta CPU resursini tejaydi.

---

### Topshiriq #1132: Swoole WebSocket Heartbeat va Ping-Pong Mexanizmi
**Tavsif:** Tarmoq provayderlarining NAT oraliq marshrutizatorlari 60 soniya jimlikdan so'ng ulanishni majburiy yopib qo'yishining oldini olish uchun past darajadagi Ping/Pong freymlarini avtomatlashtiring.
**Talablar:** WEBSOCKET_OPCODE_PING va WEBSOCKET_OPCODE_PONG, websocket_subprotocol, avtomatik javob sozlamalari.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Swoole WebSocket Ping/Pong va Keep-Alive
use Swoole\WebSocket\Server;
use Swoole\WebSocket\Frame;
use Swoole\Timer;

$server = new Server("0.0.0.0", 9511);

$server->set([
    'worker_num' => 2,
    'heartbeat_idle_time'      => 60, // 60 soniya harakatsiz qolsa o'chirish
    'heartbeat_check_interval' => 30, // Har 30 soniyada tekshirish
]);

$server->on('open', function (Server $server, $request) {
    echo "[+] Ulandi: {$request->fd}
";
});

$server->on('message', function (Server $server, Frame $frame) {
    // Agar mijoz protokoli darajasidagi Ping yuborsa
    if ($frame->opcode === WEBSOCKET_OPCODE_PING) {
        echo "[PING] Mijoz {$frame->fd} dan keldi. PONG javobi qaytarilmoqda...
";
        $pong = new Frame();
        $pong->opcode = WEBSOCKET_OPCODE_PONG;
        $pong->data = "PONG_ACK";
        $server->push($frame->fd, $pong);
        return;
    }

    echo "[Matn] {$frame->data}
";
});

// Server tomonidan har 25 soniyada barcha mijozlarga nazorat Ping jo'natish
$server->on('WorkerStart', function (Server $server, int $workerId) {
    if ($workerId === 0) {
        Timer::tick(25000, function () use ($server) {
            $ping = new Frame();
            $ping->opcode = WEBSOCKET_OPCODE_PING;
            $ping->data = "HEARTBEAT";

            foreach ($server->connections as $fd) {
                if ($server->isEstablished($fd)) {
                    $server->push($fd, $ping);
                }
            }
        });
    }
});

$server->start();
```
**Tushuntirish:** WebSocket protokoli (RFC 6455) 0x9 (Ping) va 0xA (Pong) boshqaruv freymlarini o'z ichiga oladi. Ular ilova kodi darajasida qayta ishlanmasdan to'g'ridan-to'g'ri brauzer yoki tarmoq adapteri tomonidan avtomatik qaytariladi, bu esa trafikni minimal qiladi.

---

### Topshiriq #1133: Swoole WebSocket Maxsus Subprotokol (STOMP/MQTT) Realizatsiyasi
**Tavsif:** `Sec-WebSocket-Protocol` sarlavhasi orqali STOMP yoki maxsus korporativ protokollarni kelishib oluvchi (Handshake Negotiation) va freymlarni mos formatda qabul qiluvchi server yarating.
**Talablar:** on('handshake') hodisasi, Sec-WebSocket-Protocol sarlavhasi tekshiruvi, Sec-WebSocket-Accept hisoblash.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Maxsus Subprotokol Handshake Boshqaruvi
use Swoole\Http\Request;
use Swoole\Http\Response;
use Swoole\WebSocket\Server;

$server = new Server("0.0.0.0", 9512);

$server->on('handshake', function (Request $request, Response $response) {
    $secWebSocketKey = $request->header['sec-websocket-key'] ?? null;
    $protocols = $request->header['sec-websocket-protocol'] ?? '';

    // Kalit mavjudligini tekshiramiz
    if (empty($secWebSocketKey)) {
        $response->end();
        return false;
    }

    // Biz qo'llab-quvvatlaydigan subprotokol: 'v1.khorazmiy-stomp'
    $supportedProtocol = 'v1.khorazmiy-stomp';
    if (!str_contains($protocols, $supportedProtocol)) {
        echo "[!] Mijoz talab qilgan protokol qo'llab-quvvatlanmaydi: {$protocols}
";
        $response->status(400);
        $response->end("Subprotocol unsupported");
        return false;
    }

    // RFC 6455 bo'yicha Sec-WebSocket-Accept sarlavhasini hisoblaymiz
    $secAccept = base64_encode(sha1($secWebSocketKey . '258EAFA5-E914-47DA-95CA-C5AB0DC85B11', true));

    $response->header('Upgrade', 'websocket');
    $response->header('Connection', 'Upgrade');
    $response->header('Sec-WebSocket-Accept', $secAccept);
    $response->header('Sec-WebSocket-Version', '13');
    $response->header('Sec-WebSocket-Protocol', $supportedProtocol);

    $response->status(101);
    $response->end();

    echo "[+] Subprotokol kelishildi: {$supportedProtocol} (FD: {$request->fd})
";
    return true;
});

$server->on('message', function (Server $server, $frame) {
    echo "[Maxsus Protokol Xabari]: {$frame->data}
";
    $server->push($frame->fd, "STOMP_CONNECTED

 ");
});

$server->start();
```
**Tushuntirish:** Standart `on('open')` avtomatik handshake qiladi, biroq `on('handshake')` dasturchiga HTTP sarlavhalari darajasida to'liq nazorat beradi. Bu esa xavfsizlik tokenlarini, mos subprotokollarni va CORS siyosatini noldan boshqarish imkonini beradi.

---

### Topshiriq #1134: Ratchet WebSocket Rate Limiting (Spam va DoS Himoyasi)
**Tavsif:** Bitta foydalanuvchi yoki bot soniyasiga 10 tadan ortiq xabar yuborishga uringanda uning xabarlarini rad etuvchi va vaqtincha bloklovchi Token Bucket rate limiterini joriy qiling.
**Talablar:** Token Bucket algoritmi, xabarlar soni hisobi, limit oshganda ogohlantirish berish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Ratchet WebSocket Xabar Tezligini Cheklash (Rate Limiter)
require __DIR__ . '/vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;

class RateLimitedChat implements MessageComponentInterface {
    protected array $buckets = []; // [resourceId => ['tokens' => float, 'last' => float]]
    protected float $capacity = 5.0; // Maksimal sig'im
    protected float $refillRate = 2.0; // Sekundiga qo'shiladigan tokenlar miqdori

    public function onOpen(ConnectionInterface $conn) {
        // Yangi mijoz uchun savat ochamiz
        $this->buckets[$conn->resourceId] = [
            'tokens' => $this->capacity,
            'last' => microtime(true)
        ];
    }

    public function onMessage(ConnectionInterface $from, $msg) {
        $id = $from->resourceId;
        $now = microtime(true);
        $bucket = &$this->buckets[$id];

        // O'tgan vaqt hisobiga tokenlarni to'ldiramiz
        $elapsed = $now - $bucket['last'];
        $bucket['last'] = $now;
        $bucket['tokens'] = min($this->capacity, $bucket['tokens'] + $elapsed * $this->refillRate);

        // Token yetarlimi?
        if ($bucket['tokens'] >= 1.0) {
            $bucket['tokens'] -= 1.0;
            // Xabarni qabul qilish
            echo "[Mijoz #{$id}] Xabar: {$msg} (Qolgan token: " . round($bucket['tokens'], 2) . ")
";
            $from->send(json_encode(['status' => 'OK', 'echo' => $msg]));
        } else {
            // Cheklovdan oshdi
            echo "[!] LIMIT OSHDI: Mijoz #{$id} juda ko'p xabar yozmoqda!
";
            $from->send(json_encode([
                'status' => 'RATE_LIMITED',
                'error' => 'Sekinroq yozing! Sekundiga limitdan oshib ketdingiz.'
            ]));
        }
    }

    public function onClose(ConnectionInterface $conn) {
        unset($this->buckets[$conn->resourceId]);
    }

    public function onError(ConnectionInterface $conn, \Exception $e) {
        $conn->close();
    }
}
```
**Tushuntirish:** Token Bucket algoritmi tarmoq chegaralarini silliq nazorat qilish uchun sanoat standartidir. U qisqa muddatli chaqnashlarga (bursts) ruxsat beradi, biroq uzoq muddatli spam oqimlarini qat'iy to'xtatadi.

---

### Topshiriq #1135: Swoole Coroutine WebSocket Client orqali Birjalar Narxini Tinglash
**Tavsif:** Tashqi kriptovalyuta yoki moliya birjasining WebSocket manziliga (masalan Binance) ulanib, real vaqtda BTC/USDT buyurtmalar kitobi (Order Book) oqimini asinxron qabul qiluvchi mijoz yarating.
**Talablar:** Swoole\Coroutine\Http\Client, upgrade() metodi, recv() tsikli.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Swoole Asinxron WebSocket Birja Mijozi
use Swoole\Coroutine;
use Swoole\Coroutine\Http\Client;
use function Swoole\Coroutine\run;

run(function () {
    // Binance kotirovka oqimiga ulanish
    $host = "stream.binance.com";
    $port = 9443;
    $ssl = true;

    $client = new Client($host, $port, $ssl);
    $client->set(['timeout' => 10.0]);

    // WebSocket ga yangilash (Upgrade)
    $ret = $client->upgrade('/ws/btcusdt@trade');
    if (!$ret) {
        echo "[!] WebSocket Handshake xatosi: {$client->errMsg}
";
        return;
    }

    echo "[+] Binance WebSocket bozor oqimiga muvaffaqiyatli ulandi!
";

    // Jonli ma'lumotlarni o'qish (10 ta bitimdan so'ng to'xtaymiz)
    for ($i = 1; $i <= 10; $i++) {
        $frame = $client->recv();
        if ($frame === false) {
            echo "[!] Aloqa uzildi: {$client->errMsg}
";
            break;
        }

        $trade = json_decode($frame->data, true);
        if (isset($trade['p'], $trade['q'])) {
            $price = $trade['p'];
            $qty = $trade['q'];
            $side = $trade['m'] ? 'SOTISH' : 'SOTIB OLISH';
            echo sprintf("[Bitim #%d] Narx: %s USD | Hajm: %s | Yo'nalish: %s
", $i, $price, $qty, $side);
        }
    }

    $client->close();
    echo "Tahlil yakunlandi.
";
});
```
**Tushuntirish:** Swoole WebSocket Client korutina rejimida ishlaydi. Bu orqali bitta PHP jarayonida bir vaqtning o'zida yuzlab turli birjalar va juftliklarni (BTC, ETH, SOL) minimal xotira va nol bloklanish bilan kuzatish mumkin.

---

### Topshiriq #1136: Protocol Buffers (Protobuf) .proto Ta'rifidan PHP Sinflari va Seriyalash
**Tavsif:** Google Protobuf tili yordamida buyurtmalar sxemasini tuzib, uni PHP sinflariga kompilyatsiya qiling hamda JSON ga nisbatan 5 barobar ixcham ikkilik formatga seriyalash va deserializatsiya qilishni ko'rsating.
**Talablar:** .proto shartnomasi, protoc kompilyatori chaqiruvi, serializeToString va mergeFromString.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Google Protocol Buffers (Protobuf) PHP integratsiyasi
// Quyidagi shartnoma 'order.proto' faylida bo'ladi:
/*
syntax = "proto3";
package ecommerce;

message OrderItem {
    int32 product_id = 1;
    string title = 2;
    double price = 3;
    int32 quantity = 4;
}

message OrderRequest {
    int64 order_id = 1;
    string customer_email = 2;
    repeated OrderItem items = 3;
    bool is_paid = 4;
}
*/

// protoc --php_out=. order.proto orqali generatsiya qilingan sinflarni simulyatsiya qilamiz:
namespace Ecommerce {
    use Google\Protobuf\Internal\Message;

    class OrderItem {
        public int $product_id = 0;
        public string $title = '';
        public float $price = 0.0;
        public int $quantity = 0;

        public function __construct(int $id, string $title, float $price, int $qty) {
            $this->product_id = $id;
            $this->title = $title;
            $this->price = $price;
            $this->quantity = $qty;
        }
    }

    class OrderRequest {
        public int $order_id = 0;
        public string $customer_email = '';
        public array $items = [];
        public bool $is_paid = false;

        // Protobuf ikkilik packing simulyatsiyasi
        public function serializeToString(): string {
            return msgpack_pack([
                'id' => $this->order_id,
                'email' => $this->customer_email,
                'items' => $this->items,
                'paid' => $this->is_paid
            ]);
        }

        public function mergeFromString(string $binaryData): void {
            $data = msgpack_unpack($binaryData);
            $this->order_id = $data['id'];
            $this->customer_email = $data['email'];
            $this->is_paid = $data['paid'];
        }
    }
}

// Foydalanish:
$order = new \Ecommerce\OrderRequest();
$order->order_id = 998822;
$order->customer_email = "dev@khorazmiy.uz";
$order->is_paid = true;
$order->items[] = new \Ecommerce\OrderItem(101, "Server Rack 42U", 1200.50, 2);

$binary = $order->serializeToString();
echo "Protobuf ikkilik hajm: " . strlen($binary) . " bayt
";
echo "Oddiy JSON hajm: " . strlen(json_encode($order)) . " bayt
";

$restoredOrder = new \Ecommerce\OrderRequest();
$restoredOrder->mergeFromString($binary);
echo "Tiklandi: Buyurtma ID: {$restoredOrder->order_id}, Email: {$restoredOrder->customer_email}
";
```
**Tushuntirish:** Protobuf har bir maydon nomini emas, faqat uning maydon raqamini (tag) va varint ikkilik kodlanishini uzatadi. Bu esa JSON ga qaraganda tarmoq yuklamasini 60-80% ga kamaytiradi va protsessorda parsing tezligini 10 barobargacha oshiradi.

---

### Topshiriq #1137: gRPC PHP Unary RPC Client (Mikroservis So'rovi)
**Tavsif:** Tashqi billing mikroservisiga gRPC Unary (bitta so'rov - bitta javob) rejimi orqali HTTP/2 ikkilik kanali bo'ylab ulanuvchi rasmiy gRPC mijozi yarating.
**Talablar:** Grpc\BaseStub dan meros olish, ChannelCredentials::createInsecure(), Unary chaqiruv.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - gRPC Unary RPC Mijozi
require __DIR__ . '/vendor/autoload.php';

use Grpc\BaseStub;
use Grpc\ChannelCredentials;

// Generatsiya qilingan gRPC Stub sinfi
class BillingClient extends BaseStub {
    public function __construct(string $hostname, array $opts) {
        parent::__construct($hostname, $opts);
    }

    // Unary RPC: So'rov jo'natib bitta javobni kutadi
    public function ProcessPayment($argument, array $metadata = [], array $options = []) {
        return $this->_simpleRequest(
            '/billing.BillingService/ProcessPayment',
            $argument,
            ['\Billing\PaymentResponse', 'decode'],
            $metadata,
            $options
        );
    }
}

// So'rov ob'ekti simulyatsiyasi
$paymentReq = new class {
    public function serializeToString() {
        return json_encode(['account' => 'ACC_99812', 'amount' => 250000]);
    }
};

// gRPC serverga ulanamiz (127.0.0.1:50051)
$client = new BillingClient('127.0.0.1:50051', [
    'credentials' => ChannelCredentials::createInsecure(),
]);

echo "gRPC Billing xizmatiga Unary so'rov yuborilmoqda...
";
list($reply, $status) = $client->ProcessPayment($paymentReq)->wait();

if ($status->code === \Grpc\STATUS_OK) {
    echo "[+] To'lov muvaffaqiyatli bajarildi!
";
} else {
    echo "[-] gRPC Xatosi: {$status->details} (Kod: {$status->code})
";
}
```
**Tushuntirish:** gRPC asosida transport qatlami sifatida HTTP/2 va shartnoma sifatida Protocol Buffers yotadi. `_simpleRequest` metodi C darajasidagi `grpc.so` kengaytmasi orqali HTTP/2 ikkilik ramkalarini (DATA frames) bevosita uzatadi.

---

### Topshiriq #1138: gRPC PHP Server Streaming orqali Katta Ma'lumotlarni Qabul Qilish
**Tavsif:** Bitta so'rov jo'natib, serverdan javob sifatida keladigan uzluksiz minglab yozuvlarni (Server Streaming RPC) xotirani to'ldirmasdan qadamma-qadam qabul qiling.
**Talablar:** _serverStreamRequest, $call->responses() generatoridan foydalanish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - gRPC Server Streaming RPC Mijozi
require __DIR__ . '/vendor/autoload.php';

use Grpc\BaseStub;
use Grpc\ChannelCredentials;

class AnalyticsClient extends BaseStub {
    public function StreamAuditLogs($argument, array $metadata = [], array $options = []) {
        return $this->_serverStreamRequest(
            '/analytics.AnalyticsService/StreamAuditLogs',
            $argument,
            ['\Analytics\AuditLogEntry', 'decode'],
            $metadata,
            $options
        );
    }
}

$client = new AnalyticsClient('127.0.0.1:50052', [
    'credentials' => ChannelCredentials::createInsecure(),
]);

$filter = new class {
    public function serializeToString() {
        return json_encode(['start_date' => '2026-01-01', 'severity' => 'CRITICAL']);
    }
};

echo "Server Streaming boshlandi. Loglar oqimi kutilmoqda...
";
$call = $client->StreamAuditLogs($filter);

// Serverdan kelayotgan har bir alohida yozuvni oqimda o'qiymiz
$count = 0;
foreach ($call->responses() as $logEntry) {
    $count++;
    echo "[Oqim #{$count}] Log qabul qilindi: ID " . ($logEntry->id ?? $count) . "
";
    if ($count >= 5) break; // Sinov uchun dastlabki 5 tasini o'qiymiz
}

$status = $call->getStatus();
echo "Oqim yakunlandi. Yakuniy status kodi: {$status->code}
";
```
**Tushuntirish:** Server Streaming rejimida mijoz faqat bitta so'rov yuboradi, server esa HTTP/2 DATA ramkalari orqali xohlagancha javob xabarlarini qaytaradi. Bu katta eksportlar yoki telemetriya monitorlari uchun juda samaralidir.

---

### Topshiriq #1139: gRPC PHP Client Streaming RPC orqali Telemetriya Yuklash
**Tavsif:** Mijoz tomonidan doimiy ravishda ko'plab sensor ma'lumotlarini serverga oqim sifatida uzatib borib, yakunda serverdan bitta umumiy statistika xulosasini oling.
**Talablar:** _clientStreamRequest, write() oqimi, wait() orqali yakuniy javobni olish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - gRPC Client Streaming Mijozi
require __DIR__ . '/vendor/autoload.php';

use Grpc\BaseStub;
use Grpc\ChannelCredentials;

class SensorClient extends BaseStub {
    public function UploadSensorStream(array $metadata = [], array $options = []) {
        return $this->_clientStreamRequest(
            '/iot.SensorService/UploadSensorStream',
            ['\Iot\UploadSummary', 'decode'],
            $metadata,
            $options
        );
    }
}

$client = new SensorClient('127.0.0.1:50053', [
    'credentials' => ChannelCredentials::createInsecure(),
]);

/** @var \Grpc\ClientStreamingCall $call */
$call = $client->UploadSensorStream();

echo "Client Streaming orqali 10 ta sensor paketi jo'natilmoqda...
";

for ($i = 1; $i <= 10; $i++) {
    $dataPacket = new class($i) {
        public int $id;
        public function __construct($id) { $this->id = $id; }
        public function serializeToString() {
            return json_encode(['packet_id' => $this->id, 'temperature' => 24.5 + ($this->id * 0.2)]);
        }
    };

    // Oqimga navbatdagi paketni yozamiz
    $call->write($dataPacket);
    echo "[+] Paket #{$i} uzatildi.
";
}

// Barcha ma'lumotlar yuborib bo'lingach, javobni kutamiz
list($summary, $status) = $call->wait();

if ($status->code === \Grpc\STATUS_OK) {
    echo "[Muvaffaqiyatli] Serverdan xulosa qabul qilindi!
";
} else {
    echo "[Xatolik] Status: {$status->details}
";
}
```
**Tushuntirish:** Client Streaming orqali fayllarni kichik bo'laklarga (chunks) bo'lib yuklash yoki IoT qurilmalar ma'lumotlarini ulanishni yopmasdan serverga uzatish amalga oshiriladi. Server barcha ma'lumotlarni to'liq qabul qilib olgach, yakuniy javob qaytaradi.

---

### Topshiriq #1140: gRPC PHP Interceptors va JWT Metadata Autentifikatsiyasi
**Tavsif:** Har bir gRPC so'roviga avtomatik ravishda `Authorization: Bearer <token>` metadata sarlavhasini qo'shuvchi va so'rovlar davomiyligini o'lchovchi Interceptor (Middleware) zanjirini quring.
**Talablar:** Grpc\Interceptor, interceptDatashare yoki call wrapper yozish, metadata massiviga token biriktirish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - gRPC Metadata va Interceptor Arxitekturasi
require __DIR__ . '/vendor/autoload.php';

use Grpc\Interceptor;

class AuthMetadataInterceptor extends Interceptor {
    private string $jwtToken;

    public function __construct(string $token) {
        $this->jwtToken = $token;
    }

    public function interceptUnaryUnary($method, $argument, $deserialize, $continuation, array $metadata = [], array $options = []) {
        // HTTP/2 so'roviga maxfiy avtorizatsiya sarlavhasini ineksiya qilamiz
        $metadata['authorization'] = ['Bearer ' . $this->jwtToken];
        $metadata['x-request-id'] = [uniqid('req_')];

        $start = microtime(true);
        echo "[gRPC Interceptor] Chaqirilmoqda: {$method}...
";

        // Asosiy gRPC chaqiruvni davom ettiramiz
        $call = $continuation($method, $argument, $deserialize, $metadata, $options);
        
        $duration = round((microtime(true) - $start) * 1000, 2);
        echo "[gRPC Interceptor] So'rov davomiyligi: {$duration} ms
";

        return $call;
    }
}

// Interceptorni Stub ga ulash:
// $client = new BillingClient('localhost:50051', ['credentials' => ChannelCredentials::createInsecure()]);
// $authInterceptor = new AuthMetadataInterceptor('jwt_token_bu_yerda');
// $client = \Grpc\Interceptor::intercept($client, $authInterceptor);
echo "AuthMetadataInterceptor tayyorlandi va ro'yxatga olindi.
";
```
**Tushuntirish:** gRPC Interceptor-lari HTTP freymvorklardagi Middleware mexanizmining muqobilidir. Ular orqali chaqiruvlarni loglash, xavfsizlik tokenlarini ulash, keshni tekshirish va xatoliklarni qayta urinish (retry) funksionalligi markazlashtiriladi.

---

### Topshiriq #1141: gRPC PHP Xatoliklarni Boshqarish va Status Kodlari Tahlili
**Tavsif:** Tizimda yuz bergan muammolarni oddiy istisnolar (Exceptions) o'rniga, rasmiy gRPC status kodlari (NOT_FOUND, ALREADY_EXISTS, UNAUTHENTICATED, DEADLINE_EXCEEDED) bilan professional usulda boshqaring.
**Talablar:** Grpc\STATUS_* konstantalari, $status->code va $status->details tahlili.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - gRPC Status Kodlari va Xatoliklarni Boshqarish
require __DIR__ . '/vendor/autoload.php';

function handleGrpcStatus(object $status): void {
    switch ($status->code) {
        case \Grpc\STATUS_OK:
            echo "[200 OK] Amal muvaffaqiyatli bajarildi.
";
            break;

        case \Grpc\STATUS_NOT_FOUND:
            echo "[404 Topilmadi] So'ralgan resurs bazada mavjud emas: {$status->details}
";
            break;

        case \Grpc\STATUS_ALREADY_EXISTS:
            echo "[409 Ziddiyat] Ushbu yozuv allaqachon mavjud!
";
            break;

        case \Grpc\STATUS_UNAUTHENTICATED:
            echo "[401 Rad etildi] Autentifikatsiya tokeni yaroqsiz yoki muddati o'tgan.
";
            break;

        case \Grpc\STATUS_DEADLINE_EXCEEDED:
            echo "[504 Timeout] Mikroservis belgilangan vaqt ichida javob bermadi!
";
            break;

        case \Grpc\STATUS_UNAVAILABLE:
            echo "[503 Xizmat Ishlamayapti] Serverga ulanib bo'lmadi yoki tarmoq uzilgan.
";
            break;

        default:
            echo "[Xatolik Kod: {$status->code}] " . ($status->details ?: 'Noma\'lum xatolik') . "
";
            break;
    }
}

// Simulyatsiya: Masalan server 5 (NOT_FOUND) kodi bilan javob qaytardi
$fakeStatus = (object)[
    'code' => \Grpc\STATUS_NOT_FOUND,
    'details' => 'Foydalanuvchi hisobi #404 topilmadi'
];

handleGrpcStatus($fakeStatus);
```
**Tushuntirish:** gRPC RFC darajasida 16 ta standart status kodiga ega. Bu xizmatlar turli tillarda (Go, Java, Python, PHP, Rust) yozilgan bo'lsa ham, xatoliklarni bir xil semantika bilan bir-biriga yetkazish va tushunishni kafolatlaydi.

---

### Topshiriq #1142: gRPC Deadlines va Timeout Mexanizmi orqali Tarmoq To'xtashlarini Oldini Olish
**Tavsif:** Kaskadli nosozliklarni (Cascading Failure) oldini olish uchun gRPC so'roviga qat'iy Deadline (masalan 200 ms) belgilab, agar shu vaqtda javob kelmasa, resurslarni darhol ozod qilishni ko'rsating.
**Talablar:** timeout parametri (mikrosekundlarda), DEADLINE_EXCEEDED tahlili.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - gRPC Deadlines va So'rov Timeout Nazorati
require __DIR__ . '/vendor/autoload.php';

use Grpc\BaseStub;
use Grpc\ChannelCredentials;

$hostname = '127.0.0.1:50051';
$client = new class($hostname, ['credentials' => ChannelCredentials::createInsecure()]) extends BaseStub {
    public function SlowQuery($arg, $opts) {
        return $this->_simpleRequest('/service/SlowQuery', $arg, ['\Dummy', 'decode'], [], $opts);
    }
};

// Deadline belgilaymiz: Joriy vaqtdan boshlab aniq 250 millisekund (250,000 mikrosekund)
$timeoutUs = 250000;
$options = [
    'timeout' => $timeoutUs
];

echo "gRPC so'rovi 250 ms Deadline bilan jo'natilmoqda...
";
$start = microtime(true);

$dummyArg = new class { public function serializeToString() { return ''; } };
list($response, $status) = $client->SlowQuery($dummyArg, $options)->wait();

$duration = round((microtime(true) - $start) * 1000, 2);

if ($status->code === \Grpc\STATUS_DEADLINE_EXCEEDED) {
    echo "[!] Deadline oshib ketdi ({$duration} ms). So'rov bekor qilindi va ulanish yopildi.
";
} else {
    echo "[+] Javob muvaffaqiyatli keldi ({$duration} ms).
";
}
```
**Tushuntirish:** Deadline - bu shunchaki lokal timeout emas; u gRPC HTTP/2 `grpc-timeout` sarlavhasi orqali butun mikroxizmatlar zanjiri (A -> B -> C -> D) bo'ylab tarqaladi. Agar vaqt tugasa, zanjirdagi barcha oraliq serverlar keraksiz amallarni darhol to'xtatadi.

---

### Topshiriq #1143: OpenSwoole Asinxron gRPC Serverini Qurish
**Tavsif:** PHP da tashqi C yoki Go serverlarisiz, sof PHP va OpenSwoole HTTP/2 imkoniyatlari orqali gRPC so'rovlarini qabul qilib, Protobuf javoblarini qaytaruvchi to'liq gRPC server yarating.
**Talablar:** OpenSwoole\HTTP\Server, open_http2_protocol => true, grpc Content-Type sarlavhalari, Protobuf serialization.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - OpenSwoole Asinxron gRPC Server
use OpenSwoole\HTTP\Server;
use OpenSwoole\HTTP\Request;
use OpenSwoole\HTTP\Response;

$server = new Server("0.0.0.0", 50051, OpenSwoole\Server::POOL_MODE);

$server->set([
    'open_http2_protocol' => true,
    'worker_num' => swoole_cpu_num(),
]);

$server->on('request', function (Request $request, Response $response) {
    $path = $request->server['request_uri'];
    echo "[gRPC So'rov] Path: {$path}
";

    // gRPC sarlavhalarini o'rnatamiz
    $response->header('content-type', 'application/grpc');
    $response->header('grpc-status', '0'); // 0 = OK
    $response->header('grpc-message', '');

    if ($path === '/khorazmiy.AI/GetPrediction') {
        // Protobuf binar freym simulyatsiyasi: 1 bayt kompress bayrog'i + 4 bayt uzunlik + ma'lumot
        $payload = json_encode(['result' => 'DeepLearning_Response_2026', 'confidence' => 0.998]);
        $length = strlen($payload);
        
        // gRPC frame prefix: 0 (not compressed), big-endian 32-bit unsigned length
        $grpcFrame = pack('CN', 0, $length) . $payload;

        $response->end($grpcFrame);
    } else {
        $response->header('grpc-status', '12'); // 12 = UNIMPLEMENTED
        $response->header('grpc-message', 'Metod topilmadi');
        $response->end();
    }
});

echo "OpenSwoole gRPC Server 50051-portda ishlamoqda...
";
$server->start();
```
**Tushuntirish:** OpenSwoole HTTP/2 protokoli sarlavhalari va ikkilik oqimlarini to'liq qo'llab-quvvatlagani uchun PHP ning o'zida ham gRPC serverlarni ko'tarish imkonini beradi. Bu PHP ni mikroxizmatlar arxitekturasida teng huquqli gRPC provayderiga aylantiradi.

---

### Topshiriq #1144: gRPC Protobuf Any va Oneof Tiplari bilan Dinamik Polimorfizm
**Tavsif:** Turli xildagi xabarlarni (masalan, to'lov uchun Karta, Naqd yoki Kriptovalyuta) yagona shartnoma orqali qabul qilish uchun Protobuf `oneof` va `google.protobuf.Any` tiplarini dasturlang.
**Talablar:** Polimorf xabarlar tuzilmasi, turiga qarab tekshirish, Any paketlash (pack/unpack).
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Protobuf Oneof va Any Tiplari Bilan Ishlash
namespace PaymentModel;

class CardPayment {
    public string $pan = "8600 **** **** 1234";
}

class CryptoPayment {
    public string $txHash = "0x9f8b...33a";
}

class UnifiedPaymentRequest {
    public ?CardPayment $card = null;
    public ?CryptoPayment $crypto = null;
    public string $paymentType = 'none';

    public function setCard(CardPayment $card): void {
        $this->card = $card;
        $this->crypto = null;
        $this->paymentType = 'card';
    }

    public function setCrypto(CryptoPayment $crypto): void {
        $this->crypto = $crypto;
        $this->card = null;
        $this->paymentType = 'crypto';
    }

    public function process(): void {
        match ($this->paymentType) {
            'card' => print("[Plastik Karta] To'lov o'tkazildi: {$this->card->pan}
"),
            'crypto' => print("[Kripto] Blokcheyn tasdig'i: {$this->crypto->txHash}
"),
            default => print("[Xato] To'lov turi tanlanmagan!
")
        };
    }
}

$req = new UnifiedPaymentRequest();
$req->setCard(new CardPayment());
$req->process();

$req->setCrypto(new CryptoPayment());
$req->process();
```
**Tushuntirish:** Protobuf dagi `oneof` kalit so'zi bitta xotira maydonida bir nechta alternativ turlardan faqat bittasini saqlash imkonini beradi. Bu ortiqcha maydonlar bilan tarmoqni to'ldirmay, xavfsiz va ixcham polimorfik API lar yaratishga xizmat qiladi.

---

### Topshiriq #1145: gRPC Channel Caching va Connection Pooling
**Tavsif:** Har bir gRPC chaqiruvi uchun yangidan TCP va TLS ulanishini ochish kechikishlarni keskin oshirib yuborishi sababli, gRPC Channel obyektlarini keshlovchi va qayta ishlatuvchi Singleton havza quring.
**Talablar:** gRPC Channel doimiyligi, channel_args parametrlari, qayta ulanish logikasi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - gRPC Channel Caching va Pool
require __DIR__ . '/vendor/autoload.php';

use Grpc\Channel;
use Grpc\ChannelCredentials;

class GrpcChannelPool {
    private static array $channels = [];

    public static function getChannel(string $target): Channel {
        if (!isset(self::$channels[$target])) {
            echo "[ChannelPool] Yangi gRPC Channel ochilmoqda: {$target}
";
            self::$channels[$target] = new Channel($target, [
                'credentials' => ChannelCredentials::createInsecure(),
                'grpc.keepalive_time_ms' => 30000,
                'grpc.keepalive_timeout_ms' => 10000,
                'grpc.http2.max_pings_without_data' => 0,
            ]);
        } else {
            echo "[ChannelPool] Mavjud keshdagi Channel qayta ishlatilmoqda: {$target}
";
        }

        return self::$channels[$target];
    }
}

// Bir xil manzilga bir nechta so'rovlar yuborilganda kanal keshdan olinadi
$ch1 = GrpcChannelPool::getChannel('auth-service:50051');
$ch2 = GrpcChannelPool::getChannel('auth-service:50051');

var_dump($ch1 === $ch2); // true - aynan bitta TCP ulanish qayta ishlatiladi
```
**Tushuntirish:** gRPC Channel obyektlari ostida C sathidagi HTTP/2 aloqa kanali yotadi. Kanalni keshda saqlash har bir so'rovda 30-100 ms gacha bo'lgan TCP/TLS handshake vaqtini tejab, so'rovlarni mikrosekundlar ichida yetkazadi.

---

### Topshiriq #1146: PHP Native Sockets va socket_select orqali Non-Blocking I/O Multiplexing
**Tavsif:** Tashqi kengaytmalarsiz, PHP ning sof `socket_*` funksiyalari va `socket_select` yordamida bitta oqimda bir vaqtning o'zida yuzlab mijozlarga xizmat ko'rsatuvchi I/O multiplexer quring.
**Talablar:** socket_create, socket_set_nonblock, socket_select orqali o'qish/yozish ro'yxatlarini boshqarish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - PHP Sof Soketlar va socket_select Multiplexing
$server = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
socket_set_option($server, SOL_SOCKET, SO_REUSEADDR, 1);
socket_bind($server, '127.0.0.1', 9900);
socket_listen($server, 128);
socket_set_nonblock($server);

echo "PHP Native Sockets Server 127.0.0.1:9900 da tinglamoqda...
";

$clients = [$server];

// Oddiy sinov uchun 10 iteratsiya aylanamiz
$iterations = 0;
while ($iterations < 100) {
    $iterations++;
    $read = $clients;
    $write = null;
    $except = null;

    // Soketlarda o'zgarish bor-yo'qligini 100 ms kutamiz
    if (socket_select($read, $write, $except, 0, 100000) < 1) {
        continue;
    }

    // Server soketida yangi ulanish bormi?
    if (in_array($server, $read)) {
        $newClient = socket_accept($server);
        socket_set_nonblock($newClient);
        $clients[] = $newClient;
        echo "[+] Yangi ulanish qabul qilindi. Jami soketlar: " . count($clients) . "
";
        
        $key = array_search($server, $read);
        unset($read[$key]);
    }

    // Mijozlardan ma'lumot kelgan bo'lsa o'qiymiz
    foreach ($read as $client) {
        $data = @socket_read($client, 1024);
        if ($data === false || $data === '') {
            // Mijoz uzildi
            $key = array_search($client, $clients);
            unset($clients[$key]);
            socket_close($client);
            echo "[-] Mijoz aloqani uzdi.
";
            continue;
        }

        echo "[Ma'lumot] " . trim($data) . "
";
        socket_write($client, "ACK: " . $data);
    }
}

socket_close($server);
```
**Tushuntirish:** `socket_select()` operatsion tizimning `select()` tizim chaqiruviga tayanadi. U dasturchiga bloklanmasdan bir qancha soketlarni monitoring qilish imkonini beradi va Node.js hamda Swoole paydo bo'lishidan avvalgi dastlabki asinxron tarmoq asosi bo'lgan.

---

### Topshiriq #1147: PHP Stream Sockets va Xavfsiz TLS Handshake Boshqaruvi
**Tavsif:** `stream_socket_server` va stream kontekstlari yordamida dinamik sertifikatlar bilan ishlovchi va SSL/TLS shifrlashni bosqichma-bosqich yoquvchi xavfsiz stream server yarating.
**Talablar:** stream_context_create, stream_socket_server, stream_socket_enable_crypto.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - PHP Stream Sockets va SSL/TLS Handshake
$context = stream_context_create([
    'ssl' => [
        'local_cert'        => __DIR__ . '/certs/server.crt',
        'local_pk'          => __DIR__ . '/certs/server.key',
        'verify_peer'       => false,
        'allow_self_signed' => true,
    ]
]);

$errno = 0;
$errstr = '';
$server = stream_socket_server("tcp://0.0.0.0:9901", $errno, $errstr, STREAM_SERVER_BIND | STREAM_SERVER_LISTEN, $context);

if (!$server) {
    die("Xato: {$errstr} ({$errno})
");
}

echo "Stream TCP Server 9901-portda faol...
";

// Bitta mijozni qabul qilish sinovi
$conn = @stream_socket_accept($server, 5);
if ($conn) {
    echo "[+] Mijoz ulandi. TLS Handshake boshlanmoqda...
";
    
    // Ulanishni shifrlangan TLS kanaliga o'tkazamiz
    $cryptoResult = stream_socket_enable_crypto($conn, true, STREAM_CRYPTO_METHOD_TLSv1_2_SERVER | STREAM_CRYPTO_METHOD_TLSv1_3_SERVER);
    
    if ($cryptoResult === true) {
        echo "[+] TLS Handshake muvaffaqiyatli yakunlandi!
";
        fwrite($conn, "Xush kelibsiz! Siz xavfsiz TLS kanalidasiz.
");
    } else {
        echo "[-] TLS Handshake amalga oshmadi!
";
    }
    fclose($conn);
}
fclose($server);
```
**Tushuntirish:** `stream_socket_enable_crypto()` ulanishni ochiq (plaintext) holatda boshlab, mijoz `STARTTLS` kabi buyruq bergandan so'ng dinamik ravishda shifrlangan kanalga aylantirish (upgrade) imkonini beradi (SMTP va FTP protokollarida keng qo'llaniladi).

---

### Topshiriq #1148: Ikkilik Protokollar Parseri: Modbus TCP va MQTT Freymlari Tahlili
**Tavsif:** Sanoat sensorlari va boshqaruv kontrollerlari bilan aloqa qilish uchun Modbus TCP paketining 7 baytli MBAP sarlavhasi va ma'lumotlar maydonini bitwise amallar bilan tahlil qiluvchi binar parser yozing.
**Talablar:** pack, unpack, bitwise operatorlar (&, |, >>), MBAP Header tahlili.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Modbus TCP Ikkilik Paket Tahlilchisi (Binary Parser)
class ModbusParser {
    // MBAP Header (7 bayt):
    // 2 bayt: Transaction ID
    // 2 bayt: Protocol ID (har doim 0)
    // 2 bayt: Qolgan uzunlik (Length)
    // 1 bayt: Unit ID
    // Keyin: Function Code (1 bayt) + Ma'lumotlar
    public static function parse(string $binaryPacket): array {
        if (strlen($binaryPacket) < 8) {
            throw new InvalidArgumentException("Paket hajmi juda qisqa!");
        }

        // 'n' = 16-bit unsigned big-endian, 'C' = 8-bit unsigned char
        $header = unpack('nTransactionId/nProtocolId/nLength/CUnitId/CFunctionCode', $binaryPacket);

        $payload = substr($binaryPacket, 8);
        $funcCode = $header['FunctionCode'];

        $result = [
            'tx_id'     => $header['TransactionId'],
            'proto_id'  => $header['ProtocolId'],
            'unit_id'   => $header['UnitId'],
            'func_code' => $funcCode,
        ];

        // 0x03: Read Holding Registers
        if ($funcCode === 0x03) {
            $regData = unpack('nStartAddress/nQuantity', $payload);
            $result['action'] = 'READ_REGISTERS';
            $result['start_register'] = $regData['StartAddress'];
            $result['register_count'] = $regData['Quantity'];
        }

        return $result;
    }

    public static function buildResponse(int $txId, int $unitId, array $registerValues): string {
        $byteCount = count($registerValues) * 2;
        $mbap = pack('nnnCC', $txId, 0, $byteCount + 2, $unitId, 0x03);
        $pdu = pack('C', $byteCount);
        foreach ($registerValues as $val) {
            $pdu .= pack('n', $val);
        }
        return $mbap . $pdu;
    }
}

// Sinov uchun 0x03 so'rovini quramiz:
// Tx: 100, Proto: 0, Len: 6, Unit: 1, Func: 3, Start: 40001 (0x9C41), Count: 2
$packet = pack('nnnCCnn', 100, 0, 6, 1, 0x03, 40001, 2);
$parsed = ModbusParser::parse($packet);

echo "Modbus TCP Paket tahlili:
";
print_r($parsed);
```
**Tushuntirish:** Sanoat tarmoqlarida JSON yoki XML ishlatilmaydi; u yerda mikrosekundlar va har bir bayt muhim. PHP ning `pack` va `unpack` funksiyalari C tilining `struct` lari kabi xotiradagi ikkilik baytlarni to'g'ridan-to'g'ri o'qish va yaratish imkonini beradi.

---

### Topshiriq #1149: DNS over HTTPS (DoH) Client (RFC 8484 Ikkilik So'rovlar)
**Tavsif:** Provayderlar tomonidan DNS so'rovlarining tahlil qilinishi (DNS snooping) va almashtirilishidan himoyalanish uchun RFC 8484 standartidagi DNS paketini tuzib, HTTPS orqali Cloudflare/Google DoH serveriga jo'nating.
**Talablar:** RFC 1035 binar DNS Frame yaratish, application/dns-message bilan HTTP POST jo'natish, DNS Answer RR larni tahlil qilish.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - RFC 8484 DNS over HTTPS (DoH) Mijozi
class DohClient {
    public static function resolveA(string $domain, string $dohUrl = 'https://cloudflare-dns.com/dns-query'): string {
        // DNS Query Frame (RFC 1035) yasaymiz
        $txId = rand(1000, 65535);
        $flags = 0x0100; // Standart rekursiv so'rov (RD=1)
        $qdCount = 1; // 1 ta savol
        $anCount = 0;
        $nsCount = 0;
        $arCount = 0;

        $header = pack('nnnnnn', $txId, $flags, $qdCount, $anCount, $nsCount, $arCount);

        // Domenni QNAME formatiga o'giramiz (masalan 'khorazmiy.uz' -> 10khorazmiy2uz0)
        $qname = '';
        foreach (explode('.', $domain) as $part) {
            $qname .= chr(strlen($part)) . $part;
        }
        $qname .= " ";

        $qtype = 1;  // Type A (IPv4)
        $qclass = 1; // Class IN (Internet)
        $question = $qname . pack('nn', $qtype, $qclass);

        $dnsMessage = $header . $question;

        // HTTPS orqali jo'natamiz
        $ch = curl_init($dohUrl);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/dns-message',
            'Accept: application/dns-message',
        ]);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $dnsMessage);
        
        $response = curl_exec($ch);
        curl_close($ch);

        if (!$response || strlen($response) < 12) {
            throw new Exception("DoH javobi olinmadi!");
        }

        // Oxirgi 4 baytdan IPv4 manzilini o'qiymiz
        $ipBytes = substr($response, -4);
        return inet_ntop($ipBytes);
    }
}

echo "DoH orqali xavfsiz DNS qidiruvi (google.com)...
";
$ip = DohClient::resolveA('google.com');
echo "[+] Yechilgan IP: {$ip}
";
```
**Tushuntirish:** DoH an'anaviy ochiq UDP 53 portidagi DNS trafigini TLS shifrlangan HTTP/2 va HTTP/3 quvurlari ichiga joylashtiradi. Natijada xakerlar va oraliq provayderlar foydalanuvchi qaysi saytlarga kirayotganini ko'ra olmaydi.

---

### Topshiriq #1150: Leaky Bucket Algoritmi bilan Tarmoq O'tkazuvchanligini Tekislash (Traffic Shaping)
**Tavsif:** Tarmoq soketiga keladigan keskin trafik sakrashlarini (spikes) buferda ushlab, ularni tashqi API yoki quyi tizimlarga qat'iy tekis tezlikda (masalan, sekundiga 50 ta paket) oqizuvchi Leaky Bucket algoritmini quring.
**Talablar:** Oqish tezligi (leakRate), bufer sig'imi, ortiqcha paketlarni drop qilish, asinxron timer integratsiyasi.
**Yechim (PHP):**
```php
<?php
// Khorazmiy AI - Sanoat darajasidagi Leaky Bucket Traffic Shaper
class LeakyBucketShaper {
    protected float $capacity;     // Paqirning maksimal sig'imi
    protected float $leakRate;     // Sekundiga oqib chiqadigan ma'lumot miqdori
    protected float $waterLevel;   // Joriy to'plangan sath
    protected float $lastLeakTime; // Oxirgi oqish vaqti

    public function __construct(float $capacity, float $leakRatePerSec) {
        $this->capacity = $capacity;
        $this->leakRate = $leakRatePerSec;
        $this->waterLevel = 0.0;
        $this->lastLeakTime = microtime(true);
    }

    public function processPacket(float $packetSize): bool {
        $now = microtime(true);
        $elapsed = $now - $this->lastLeakTime;
        $this->lastLeakTime = $now;

        // O'tgan vaqt hisobiga suv sathini kamaytiramiz (Leak)
        $this->waterLevel = max(0.0, $this->waterLevel - ($elapsed * $this->leakRate));

        // Yangi paket buferga sig'adimi?
        if (($this->waterLevel + $packetSize) <= $this->capacity) {
            $this->waterLevel += $packetSize;
            echo sprintf("[Qabul qilindi] Hajm: %.1f | Bufer: %.1f / %.1f
", $packetSize, $this->waterLevel, $this->capacity);
            return true;
        }

        // Sig'madi: Paket tashlab yuborildi (Packet Drop)
        echo sprintf("[DROP] Paket tashlab yuborildi! Hajm: %.1f | Bufer to'lgan: %.1f
", $packetSize, $this->waterLevel);
        return false;
    }
}

// Sinov: Sig'im 100 birlik, oqish tezligi sekundiga 20 birlik
$shaper = new LeakyBucketShaper(100.0, 20.0);

// Keskin yuklama yuboramiz
for ($i = 1; $i <= 6; $i++) {
    $size = 25.0;
    $shaper->processPacket($size);
    usleep(100000); // 100 ms kutish
}
```
**Tushuntirish:** Leaky Bucket algoritmi tarmoq marshrutizatorlari (routers) va yuklama muvozanatlashtiruvchilari (load balancers) uchun poydevor hisoblanadi. U kiruvchi beqaror va tartibsiz trafikni chiqishda qat'iy barqaror va tekis oqimga aylantiradi.

---

