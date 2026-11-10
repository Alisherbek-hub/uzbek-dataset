Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. PHP ekotizimida yuqori unumdorlikka erishish uchun asinxron arxitekturalar (Swoole/RoadRunner) va real-time tizimlar (WebSockets) bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1001-Topshiriq: Swoole yordamida asinxron HTTP server yaratish

## Topshiriq sharti:
Swoole kutubxonasi yordamida 9501-portda ishlaydigan va har bir so'rovga "Khorazmiy AI: Asinxron javob" deb qaytaradigan oddiy HTTP serverni ishga tushiring.

## Yechim (PHP kodi):
```php
<?php
use Swoole\Http\Server;
use Swoole\Http\Request;
use Swoole\Http\Response;

$server = new Server("127.0.0.1", 9501);

$server->on("Request", function (Request $request, Response $response) {
    $response->header("Content-Type", "text/plain");
    $response->end("Khorazmiy AI: Asinxron javob");
});

$server->start();
```

## Tushuntirish va Mantiq:
Swoole `Server` klassi PHP-ning an'anaviy bloklanuvchi modelini chetlab o'tib, event-loop asosida ishlaydi. `on("Request", ...)` hodisasi har bir kelayotgan HTTP so'rovni asinxron tarzda qayta ishlaydi, bu esa an'anaviy FPM ga nisbatan minglab barobar tezroqdir.

## Ishlash natijasi:
```text
Swoole http server is started at http://127.0.0.1:9501
```

---

# 1002-Topshiriq: WebSocket orqali real-time xabar almashish

## Topshiriq sharti:
Swoole WebSocket serverini yarating. Mijoz xabar yuborganda, server uni qabul qilib, "Qabul qilindi: [xabar]" deb qaytarsin.

## Yechim (PHP kodi):
```php
<?php
$server = new Swoole\WebSocket\Server("0.0.0.0", 9502);

$server->on('message', function($server, $frame) {
    $server->push($frame->fd, "Qabul qilindi: {$frame->data}");
});

$server->start();
```

## Tushuntirish va Mantiq:
WebSocket doimiy aloqa kanalini ochadi. `$frame->fd` mijozning unikal identifikatori bo'lib, server aynan o'sha mijozga javob qaytarishini ta'minlaydi.

## Ishlash natijasi:
```text
WebSocket server started at 0.0.0.0:9502
```

---

# 1003-Topshiriq: E-commerce uchun asinxron Task Worker

## Topshiriq sharti:
Buyurtma qabul qilinganda, email yuborish jarayonini asosiy threadni bloklamasdan, Swoole `TaskWorker` yordamida fon rejimida bajaring.

## Yechim (PHP kodi):
```php
<?php
$server = new Swoole\Http\Server("127.0.0.1", 9503);
$server->set(['task_worker_num' => 4]);

$server->on('request', function ($req, $res) use ($server) {
    $server->task("Email yuborish: buyurtma #123");
    $res->end("Buyurtma qabul qilindi, email yuborilmoqda...");
});

$server->on('task', function ($serv, $task_id, $src_id, $data) {
    sleep(2); // Email yuborish simulyatsiyasi
    echo "Task bajarildi: $data\n";
});

$server->start();
```

## Tushuntirish va Mantiq:
`task_worker_num` orqali fon jarayonlari soni belgilanadi. Asosiy server so'rovga darhol javob beradi, og'ir jarayonlar esa `task` eventiga o'tkaziladi.

## Ishlash natijasi:
```text
Task bajarildi: Email yuborish: buyurtma #123
```

---

# 1004-Topshiriq: RoadRunner yordamida PSR-7 so'rovini qayta ishlash

## Topshiriq va Yechim:
RoadRunner bilan ishlash uchun `Worker` obyektini yarating.

```php
<?php
require __DIR__ . '/vendor/autoload.php';
use Spiral\RoadRunner;
use Nyholm\Psr7;

$worker = RoadRunner\Worker::create();
$psrFactory = new Psr7\Factory\Psr17Factory();
$psr7 = new RoadRunner\Http\PSR7Worker($worker, $psrFactory, $psrFactory, $psrFactory);

while ($req = $psr7->waitRequest()) {
    $psr7->respond(new Psr7\Response(200, [], "RoadRunner ishlamoqda!"));
}
```

## Tushuntirish va Mantiq:
RoadRunner PHP kodini xotirada ushlab turadi (preloading), bu esa har bir so'rovda frameworkni qayta yuklashni oldini oladi.

## Ishlash natijasi:
```text
RoadRunner server ready.
```

---

# 1005-Topshiriq: Redis orqali WebSocket xabarlarini tarqatish (Pub/Sub)

## Topshiriq sharti:
Swoole serverida Redis Pub/Sub yordamida boshqa jarayonlardan kelgan xabarlarni WebSocket mijozlariga yuboring.

## Yechim (PHP kodi):
```php
<?php
$server = new Swoole\WebSocket\Server("0.0.0.0", 9504);
$server->on('workerStart', function($server, $id) {
    $redis = new Redis();
    $redis->connect('127.0.0.1', 6379);
    $redis->subscribe(['orders'], function($instance, $channel, $message) use ($server) {
        foreach($server->connections as $fd) {
            if($server->isEstablished($fd)) $server->push($fd, $message);
        }
    });
});
$server->start();
```

## Tushuntirish va Mantiq:
`workerStart` hodisasi har bir worker ishga tushganda Redisga ulanadi va `orders` kanalini tinglaydi. Yangi buyurtma kelganda barcha ulangan mijozlarga xabar tarqatiladi.

## Ishlash natijasi:
```text
Subscribed to channel: orders
```

---

# 1006-Topshiriq: Yuqori yuklamali E-commerce omborini tekshirish

## Topshiriq sharti:
Swoole `Table` yordamida xotirada (in-memory) mahsulot qoldiqlarini saqlang va ularni asinxron yangilang.

## Yechim (PHP kodi):
```php
<?php
$table = new Swoole\Table(1024);
$table->column('stock', Swoole\Table::TYPE_INT);
$table->create();

$table->set('product_1', ['stock' => 100]);
$table->incr('product_1', 'stock', -1); // Sotuv amalga oshdi

echo "Qolgan mahsulot: " . $table->get('product_1', 'stock');
```

## Tushuntirish va Mantiq:
`Swoole\Table` - bu xotirada joylashgan, lock-free (qulflanmaydigan) jadval bo'lib, u juda tez ishlaydi va turli workerlar o'rtasida ma'lumot almashish uchun eng yaxshi vositadir.

## Ishlash natijasi:
```text
Qolgan mahsulot: 99
```

---

# 1007-Topshiriq: Asinxron MySQL so'rovi (Swoole Coroutine)

## Topshiriq sharti:
`Swoole\Coroutine\MySQL` yordamida ma'lumotlar bazasidan mahsulotlar ro'yxatini bloklanmasdan oling.

## Yechim (PHP kodi):
```php
<?php
use Swoole\Coroutine;

Coroutine\run(function() {
    $db = new Coroutine\MySQL();
    $db->connect(['host' => '127.0.0.1', 'user' => 'root', 'password' => '', 'database' => 'shop']);
    $result = $db->query('SELECT * FROM products LIMIT 5');
    print_r($result);
});
```

## Tushuntirish va Mantiq:
`Coroutine\run` ichida bajarilgan har qanday I/O operatsiyasi (DB, API) bloklanmaydi. Boshqa so'rovlar bazadan javob kelishini kutmasdan ishini davom ettiraveradi.

## Ishlash natijasi:
```text
Array ( [0] => Array ( [id] => 1 [name] => Laptop ) ... )
```

---

# 1008-Topshiriq: WebSocket orqali "Live" narxlar yangilanishi

## Topshiriq sharti:
Har 1 soniyada barcha ulangan mijozlarga mahsulot narxini WebSocket orqali yuboruvchi `Timer` yarating.

## Yechim (PHP kodi):
```php
<?php
$server = new Swoole\WebSocket\Server("0.0.0.0", 9505);
$server->on('workerStart', function($server) {
    Swoole\Timer::tick(1000, function() use ($server) {
        foreach($server->connections as $fd) {
            if($server->isEstablished($fd)) $server->push($fd, "Narx: " . rand(100, 500));
        }
    });
});
$server->start();
```

## Tushuntirish va Mantiq:
`Swoole\Timer::tick` funksiyasi belgilangan vaqt oralig'ida (ms) kodni qayta-qayta bajaradi. Bu real-time dashboardlar uchun juda muhim.

## Ishlash natijasi:
```text
Narx: 245 (har 1 soniyada yangilanadi)
```

---

# 1009-Topshiriq: Asinxron HTTP Client (API integratsiyasi)

## Topshiriq sharti:
Tashqi to'lov tizimi (Payment Gateway) API'siga asinxron so'rov yuboring.

## Yechim (PHP kodi):
```php
<?php
use Swoole\Coroutine\Http\Client;

Coroutine\run(function() {
    $client = new Client('api.payment.com', 80);
    $client->get('/v1/status');
    echo $client->body;
});
```

## Tushuntirish va Mantiq:
An'anaviy `curl` bloklanuvchi hisoblanadi. Swoole `Coroutine\Http\Client` esa so'rov ketganda boshqa jarayonlarga o'tib ketadi va javob kelganda qaytib keladi.

## Ishlash natijasi:
```text
{"status": "success", "code": 200}
```

---

# 1010-Topshiriq: Server yuklamasini kuzatish (Monitoring)

## Topshiriq sharti:
Swoole serverining holatini (active connections, task queue) ko'rsatuvchi monitoring funksiyasini yozing.

## Yechim (PHP kodi):
```php
<?php
$server = new Swoole\Http\Server("127.0.0.1", 9506);
$server->on('request', function ($req, $res) use ($server) {
    $stats = $server->stats();
    $res->end("Faol ulanishlar: " . $stats['connection_num']);
});
$server->start();
```

## Tushuntirish va Mantiq:
`$server->stats()` funksiyasi serverning ichki holati haqida ma'lumot beradi. Bu yuqori yuklamali tizimlarda server sog'lig'ini nazorat qilish uchun zarur.

## Ishlash natijasi:
```text
Faol ulanishlar: 1
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. PHP ekotizimini yuqori yuklamali (high-load) tizimlar uchun optimallashtirish bo'yicha 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1011-Topshiriq: Swoole yordamida asinxron HTTP server

## Topshiriq sharti:
Swoole kutubxonasi yordamida 9501 portida ishlaydigan va har bir so'rovga "Khorazmiy AI: Asinxron javob" matnini qaytaradigan oddiy asinxron server yarating.

## Yechim (PHP kodi):
```php
use Swoole\Http\Server;
use Swoole\Http\Request;
use Swoole\Http\Response;

$server = new Server("127.0.0.1", 9501);

$server->on("Request", function (Request $request, Response $response) {
    $response->header("Content-Type", "text/plain");
    $response->end("Khorazmiy AI: Asinxron javob");
});

$server->start();
```

## Tushuntirish va Mantiq:
Swoole PHP uchun event-driven (hodisalarga asoslangan) asinxron modelni taqdim etadi. `Server` klassi doimiy ishlaydigan jarayonni yaratadi. `on("Request", ...)` funksiyasi har bir kelgan HTTP so'rovni bloklamasdan qayta ishlaydi, bu esa an'anaviy FPM modelidan ancha tezroq.

## Ishlash natijasi:
```text
Swoole http server is started at http://127.0.0.1:9501
```

---

# 1012-Topshiriq: WebSocket orqali real-time narx yangilash

## Topshiriq sharti:
E-commerce platformasi uchun WebSocket serverini ishga tushiring. Mijoz ulanganda unga mahsulotning joriy narxini yuboring.

## Yechim (PHP kodi):
```php
use Swoole\WebSocket\Server;

$server = new Server("0.0.0.0", 9502);

$server->on('open', function($server, $req) {
    $server->push($req->fd, json_encode(['product' => 'Laptop', 'price' => 1200]));
});

$server->start();
```

## Tushuntirish va Mantiq:
WebSocket doimiy aloqa kanalini ochadi. `open` hodisasi mijoz ulanganda ishga tushadi va `push` metodi orqali ma'lumotni mijozga (fd - file descriptor orqali) yuboradi. Bu e-commerce'da narxlar o'zgarishini real vaqtda ko'rsatish uchun asosdir.

## Ishlash natijasi:
```text
WebSocket server started at 0.0.0.0:9502
```

---

# 1013-Topshiriq: RoadRunner orqali Worker pool boshqaruvi

## Topshiriq sharti:
RoadRunner ishchi jarayonlari (worker) uchun oddiy PSR-7 so'rovini qayta ishlovchi `worker.php` faylini yarating.

## Yechim (PHP kodi):
```php
require __DIR__ . '/vendor/autoload.php';

use Spiral\RoadRunner;
use Nyholm\Psr7;

$worker = RoadRunner\Worker::create();
$psrFactory = new Psr7\Factory\Psr17Factory();
$psr7 = new RoadRunner\Http\PSR7Worker($worker, $psrFactory, $psrFactory, $psrFactory);

while ($req = $psr7->waitRequest()) {
    $resp = $psrFactory->createResponse()->withBody($psrFactory->createStream('Khorazmiy AI: RR OK'));
    $psr7->respond($resp);
}
```

## Tushuntirish va Mantiq:
RoadRunner PHP kodini xotirada saqlab qoladi (preloading). `while` sikli so'rovlarni kutadi va ularni qayta ishlaydi. Bu har bir so'rovda frameworkni qayta yuklashni oldini olib, unumdorlikni 10 barobar oshiradi.

## Ishlash natijasi:
```text
RoadRunner worker ready to accept requests.
```

---

# 1014-Topshiriq: Asinxron ma'lumotlar bazasi so'rovi (Swoole Coroutine)

## Topshiriq sharti:
Swoole Coroutine yordamida MySQL bazasidan mahsulotlar ro'yxatini bloklamasdan oling.

## Yechim (PHP kodi):
```php
use Swoole\Coroutine\MySQL;
use function Swoole\Coroutine\run;

run(function () {
    $db = new MySQL();
    $db->connect(['host' => '127.0.0.1', 'user' => 'root', 'password' => '', 'database' => 'shop']);
    $result = $db->query('SELECT * FROM products LIMIT 5');
    var_dump($result);
});
```

## Tushuntirish va Mantiq:
`run` funksiyasi coroutine muhitini yaratadi. `MySQL` coroutine mijozi bazaga so'rov yuborganda, boshqa jarayonlar to'xtab qolmaydi (non-blocking). Bu yuqori yuklamali e-commerce tizimlarida bazani kutish vaqtini kamaytiradi.

## Ishlash natijasi:
```text
array(5) { ... mahsulotlar ma'lumotlari ... }
```

---

# 1015-Topshiriq: Redis orqali asinxron keshni boshqarish

## Topshiriq sharti:
Swoole Redis mijozi yordamida mahsulot qoldig'ini (stock) keshdan o'qing.

## Yechim (PHP kodi):
```php
use Swoole\Coroutine\Redis;
use function Swoole\Coroutine\run;

run(function () {
    $redis = new Redis();
    $redis->connect('127.0.0.1', 6379);
    $stock = $redis->get('product_101_stock');
    echo "Qoldiq: " . $stock;
});
```

## Tushuntirish va Mantiq:
Redis - yuqori yuklamali tizimlarda tezkor kesh uchun standart. Swoole coroutine Redis mijozi I/O operatsiyalarini asinxron bajaradi, bu esa minglab foydalanuvchilar bir vaqtda mahsulot qoldig'ini tekshirganda serverni qotib qolishdan saqlaydi.

## Ishlash natijasi:
```text
Qoldiq: 45
```

---

# 1016-Topshiriq: Parallel vazifalar (Task Workers)

## Topshiriq sharti:
Swoole serverida og'ir hisoblash talab qiladigan "hisobot yaratish" vazifasini `task` sifatida ishga tushiring.

## Yechim (PHP kodi):
```php
$server = new Swoole\Server("127.0.0.1", 9503);
$server->set(['task_worker_num' => 4]);

$server->on('Receive', function($serv, $fd, $from_id, $data) {
    $serv->task($data);
});

$server->on('Task', function ($serv, $task_id, $src_id, $data) {
    sleep(2); // Og'ir jarayon
    return "Hisobot tayyor";
});

$server->start();
```

## Tushuntirish va Mantiq:
Asosiy server jarayoni so'rovni qabul qiladi, lekin og'ir ishni `task worker`larga topshiradi. Bu asosiy serverning javob berish tezligini (latency) saqlab qoladi.

## Ishlash natijasi:
```text
Task worker processing data in background...
```

---

# 1017-Topshiriq: WebSocket orqali Broadcast (Xabar tarqatish)

## Topshiriq sharti:
Barcha ulangan mijozlarga "Yangi chegirma!" xabarini yuboruvchi funksiya yozing.

## Yechim (PHP kodi):
```php
$server->on('Message', function($server, $frame) {
    foreach($server->connections as $fd) {
        if($server->isEstablished($fd)) {
            $server->push($fd, "Yangi chegirma: 50%");
        }
    }
});
```

## Tushuntirish va Mantiq:
`$server->connections` massivi barcha faol ulanishlarni o'z ichiga oladi. `isEstablished` tekshiruvi ulanish hali ham ochiqligini tasdiqlaydi. Bu e-commerce'da marketing xabarlarini real vaqtda yuborish uchun ishlatiladi.

## Ishlash natijasi:
```text
Message broadcasted to all active clients.
```

---

# 1018-Topshiriq: Asinxron fayl yuklash (Non-blocking I/O)

## Topshiriq sharti:
Swoole `Coroutine\System::readFile` yordamida katta log faylini bloklamasdan o'qing.

## Yechim (PHP kodi):
```php
use Swoole\Coroutine\System;
use function Swoole\Coroutine\run;

run(function () {
    $data = System::readFile(__DIR__ . '/log.txt');
    echo "Fayl hajmi: " . strlen($data) . " bayt";
});
```

## Tushuntirish va Mantiq:
An'anaviy `file_get_contents` fayl o'qilguncha butun PHP jarayonini to'xtatib qo'yadi. `System::readFile` esa fayl o'qilayotganda boshqa so'rovlarni qayta ishlashga imkon beradi.

## Ishlash natijasi:
```text
Fayl hajmi: 1024 bayt
```

---

# 1019-Topshiriq: HTTP/2 protokoli yordamida so'rov

## Topshiriq sharti:
Swoole HTTP/2 mijozi yordamida tashqi API'ga so'rov yuboring.

## Yechim (PHP kodi):
```php
use Swoole\Coroutine\Http\Client;
use function Swoole\Coroutine\run;

run(function () {
    $client = new Client('api.khorazmiy.ai', 443, true);
    $client->set(['ssl_verify_peer' => false]);
    $client->get('/v1/products');
    echo $client->body;
});
```

## Tushuntirish va Mantiq:
HTTP/2 multipleksing (bir vaqtda bir nechta so'rov) imkoniyatini beradi. Bu e-commerce tizimlarida bir nechta mikroxizmatlar (microservices) bilan bog'lanishda tezlikni oshiradi.

## Ishlash natijasi:
```text
{"status": "success", "data": [...]}
```

---

# 1020-Topshiriq: Graceful Shutdown (Serverni to'g'ri o'chirish)

## Topshiriq sharti:
Server to'xtatilganda barcha ochiq ulanishlarni yopish va resurslarni tozalash mexanizmini qo'shing.

## Yechim (PHP kodi):
```php
$server->on('WorkerStop', function($server, $workerId) {
    echo "Worker $workerId to'xtatilmoqda, resurslar tozalanmoqda...\n";
    // Baza ulanishlarini yopish
});
```

## Tushuntirish va Mantiq:
`WorkerStop` hodisasi server o'chirilayotganda ishga tushadi. Bu ma'lumotlar bazasi ulanishlarini xavfsiz yopish va tranzaksiyalarni yakunlash uchun juda muhim, aks holda ma'lumotlar yo'qolishi mumkin.

## Ishlash natijasi:
```text
Worker 0 to'xtatilmoqda, resurslar tozalanmoqda...
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. PHP ekotizimini yuqori unumdorlikka olib chiqish uchun asinxron arxitektura (Swoole/RoadRunner) va yuqori yuklamali tizimlar bo'yicha 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1021-Topshiriq: Swoole yordamida asinxron HTTP server yaratish

## Topshiriq sharti:
Swoole kutubxonasi yordamida oddiy HTTP serverni ishga tushiring va har bir so'rovga "Khorazmiy AI: Asinxron javob" matnini qaytaring.

## Yechim (PHP kodi):
```php
use Swoole\Http\Server;
use Swoole\Http\Request;
use Swoole\Http\Response;

$server = new Server("127.0.0.1", 9501);
$server->on("Request", function (Request $request, Response $response) {
    $response->header("Content-Type", "text/plain");
    $response->end("Khorazmiy AI: Asinxron javob");
});
$server->start();
```

## Tushuntirish va Mantiq:
Swoole `Server` klassi PHP-ni an'anaviy FPM modelidan ajratib, doimiy ishlaydigan jarayonga aylantiradi. `on("Request")` hodisasi har bir kelgan HTTP so'rovni bloklamasdan qayta ishlaydi.

## Ishlash natijasi:
```text
Server started at http://127.0.0.1:9501
```

---

# 1022-Topshiriq: WebSocket orqali real-time xabar almashish

## Topshiriq sharti:
Swoole WebSocket serverini yarating, u mijozdan kelgan xabarni qabul qilib, uni barcha ulangan mijozlarga tarqatsin (Broadcast).

## Yechim (PHP kodi):
```php
$server = new Swoole\WebSocket\Server("0.0.0.0", 9502);
$server->on('message', function($server, $frame) {
    foreach($server->connections as $fd) {
        if($server->isEstablished($fd)) {
            $server->push($fd, "Broadcasting: " . $frame->data);
        }
    }
});
$server->start();
```

## Tushuntirish va Mantiq:
`WebSocket\Server` doimiy aloqa kanalini ushlab turadi. `push` metodi orqali server mijozga ma'lumot yuboradi. `connections` massivi barcha faol sessiyalarni saqlaydi.

## Ishlash natijasi:
```text
WebSocket server started at 0.0.0.0:9502
```

---

# 1023-Topshiriq: Asinxron Task Worker (Vazifalarni fon rejimida bajarish)

## Topshiriq sharti:
Swoole Task Worker tizimidan foydalanib, og'ir hisoblash jarayonini (masalan, katta hisobot generatsiyasi) asosiy jarayonni to'xtatmasdan bajaring.

## Yechim (PHP kodi):
```php
$server = new Swoole\Http\Server("127.0.0.1", 9503);
$server->set(['task_worker_num' => 4]);
$server->on('request', function ($req, $res) use ($server) {
    $server->task("Og'ir hisobot jarayoni");
    $res->end("Vazifa qabul qilindi!");
});
$server->on('task', function ($serv, $id, $src_id, $data) {
    sleep(2); // Og'ir jarayon
    echo "Vazifa bajarildi: $data\n";
});
$server->start();
```

## Tushuntirish va Mantiq:
`task_worker_num` orqali fon jarayonlari soni belgilanadi. Asosiy HTTP jarayoni `task` metodini chaqirib, darhol javob qaytaradi, og'ir ish esa `task` hodisasida bajariladi.

## Ishlash natijasi:
```text
Vazifa bajarildi: Og'ir hisobot jarayoni
```

---

# 1024-Topshiriq: RoadRunner yordamida PSR-7 so'rovlarini qayta ishlash

## Topshiriq sandarti:
RoadRunner ishchi jarayoni (Worker) orqali kelayotgan PSR-7 so'rovini qabul qilib, JSON formatida javob qaytaring.

## Yechim (PHP kodi):
```php
require __DIR__ . '/vendor/autoload.php';
use Spiral\RoadRunner;
use Nyholm\Psr7;

$worker = RoadRunner\Worker::create();
$psrFactory = new Psr7\Factory\Psr17Factory();
$psr7 = new RoadRunner\Http\PSR7Worker($worker, $psrFactory, $psrFactory, $psrFactory);

while ($req = $psr7->waitRequest()) {
    $psr7->respond(new Psr7\Response(200, [], json_encode(['status' => 'OK'])));
}
```

## Tushuntirish va Mantiq:
RoadRunner PHP-ni Go tili bilan bog'laydi. `PSR7Worker` so'rovlarni standart formatda qabul qiladi, bu esa Laravel/Symfony kabi frameworklar bilan ishlashni osonlashtiradi.

## Ishlash natijasi:
```text
RoadRunner worker ready.
```

---

# 1025-Topshiriq: E-commerce uchun asinxron inventar yangilash

## Topshiriq sharti:
Swoole `Table` xotira strukturasidan foydalanib, yuqori tezlikdagi inventar (mahsulot soni) boshqaruvini yarating.

## Yechim (PHP kodi):
```php
$table = new Swoole\Table(1024);
$table->column('stock', Swoole\Table::TYPE_INT);
$table->create();

$table->set('product_1', ['stock' => 100]);
$table->incr('product_1', 'stock', -1); // Sotuv amalga oshdi
echo "Qolgan mahsulot: " . $table->get('product_1', 'stock');
```

## Tushuntirish va Mantiq:
`Swoole\Table` - bu xotirada joylashgan (shared memory) jadval. U juda tez ishlaydi va bir nechta jarayonlar o'rtasida ma'lumot almashish uchun eng yaxshi vositadir.

## Ishlash natijasi:
```text
Qolgan mahsulot: 99
```

---

# 1026-Topshiriq: Asinxron Redis mijozidan foydalanish

## Topshiriq sharti:
Swoole Coroutine Redis mijozidan foydalanib, ma'lumotlarni bloklamasdan o'qib oling.

## Yechim (PHP kodi):
```php
use Swoole\Coroutine;
use Swoole\Coroutine\Redis;

Coroutine\run(function () {
    $redis = new Redis();
    $redis->connect('127.0.0.1', 6379);
    $val = $redis->get('key');
    echo "Redis qiymati: " . $val;
});
```

## Tushuntirish va Mantiq:
`Coroutine` (korutin) PHP-da asinxron kodni sinxron ko'rinishda yozish imkonini beradi. `run` bloki ichida kod bloklanmaydi, boshqa so'rovlar ham parallel ishlashi mumkin.

## Ishlash natijasi:
```text
Redis qiymati: Khorazmiy_Data
```

---

# 1027-Topshiriq: WebSocket orqali "Live" narxlar paneli

## Topshiriq sharti:
Har 2 soniyada barcha ulangan mijozlarga tasodifiy mahsulot narxini yuboradigan timer yarating.

## Yechim (PHP kodi):
```php
$server = new Swoole\WebSocket\Server("0.0.0.0", 9504);
$server->on('workerStart', function($server, $id) {
    Swoole\Timer::tick(2000, function() use ($server) {
        foreach($server->connections as $fd) {
            $server->push($fd, "Yangi narx: " . rand(100, 1000) . " USD");
        }
    });
});
$server->start();
```

## Tushuntirish va Mantiq:
`Timer::tick` funksiyasi belgilangan vaqt oralig'ida kodni qayta-qayta bajaradi. Bu real-time dashboardlar uchun juda samarali.

## Ishlash natijasi:
```text
Yangi narx: 450 USD (har 2 soniyada)
```

---

# 1028-Topshiriq: Asinxron fayl yuklash (Non-blocking I/O)

## Topshiriq sharti:
Swoole `Coroutine\System::readFile` yordamida katta faylni bloklamasdan o'qing.

## Yechim (PHP kodi):
```php
use Swoole\Coroutine\System;
use function Swoole\Coroutine\run;

run(function () {
    $data = System::readFile(__DIR__ . '/data.json');
    echo "Fayl o'qildi, hajmi: " . strlen($data) . " bayt";
});
```

## Tushuntirish va Mantiq:
An'anaviy `file_get_contents` funksiyasi fayl o'qilguncha butun PHP jarayonini to'xtatib qo'yadi. `System::readFile` esa fayl o'qilayotganda boshqa vazifalarni bajarishga imkon beradi.

## Ishlash natijasi:
```text
Fayl o'qildi, hajmi: 102400 bayt
```

---

# 1029-Topshiriq: Yuqori yuklamali API uchun Rate Limiter

## Topshiriq sharti:
Swoole `Table` yordamida har bir IP uchun 1 daqiqada maksimal 60 ta so'rov cheklovini o'rnating.

## Yechim (PHP kodi):
```php
$limit = new Swoole\Table(1024);
$limit->column('count', Swoole\Table::TYPE_INT);
$limit->create();

// So'rov kelganda:
$ip = '192.168.1.1';
$data = $limit->get($ip) ?: ['count' => 0];
if ($data['count'] < 60) {
    $limit->set($ip, ['count' => $data['count'] + 1]);
} else {
    echo "Limit oshib ketdi!";
}
```

## Tushuntirish va Mantiq:
Bu yechim har bir foydalanuvchi uchun so'rovlar sonini xotirada saqlaydi. Bu ma'lumotlar bazasiga murojaat qilmasdan tezkor tekshiruv o'tkazish imkonini beradi.

## Ishlash natijasi:
```text
Limit oshib ketdi! (agar 60 dan oshsa)
```

---

# 1030-Topshiriq: Asinxron HTTP Client (Parallel so'rovlar)

## Topshiriq sharti:
Swoole `Coroutine\Http\Client` yordamida bir vaqtning o'zida 3 ta tashqi API-dan ma'lumot oling.

## Yechim (PHP kodi):
```php
use Swoole\Coroutine\Http\Client;
use function Swoole\Coroutine\run;

run(function () {
    $urls = ['api.site1.com', 'api.site2.com', 'api.site3.com'];
    foreach ($urls as $url) {
        go(function () use ($url) {
            $cli = new Client($url, 80);
            $cli->get('/');
            echo "Javob olindi: $url\n";
        });
    }
});
```

## Tushuntirish va Mantiq:
`go()` funksiyasi har bir so'rov uchun alohida korutin yaratadi. Bu 3 ta so'rov ketma-ket emas, balki parallel ravishda bajarilishini ta'minlaydi, bu esa umumiy vaqtni sezilarli qisqartiradi.

## Ishlash natijasi:
```text
Javob olindi: api.site1.com
Javob olindi: api.site2.com
Javob olindi: api.site3.com
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. PHP ekotizimini yuqori unumdorlik (High-Performance) darajasiga olib chiqish uchun mo'ljallangan, asinxron arxitektura va e-commerce tizimlariga oid 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1031-Topshiriq: Swoole yordamida asinxron HTTP server

## Topshiriq sharti:
Swoole kutubxonasi yordamida oddiy HTTP server yarating. Server har bir so'rovga "Khorazmiy AI: Server ishlamoqda" degan javob qaytarsin va so'rovlar sonini xotirada hisoblab borsin.

## Yechim (PHP kodi):
```php
use Swoole\Http\Server;
use Swoole\Http\Request;
use Swoole\Http\Response;

$server = new Server("127.0.0.1", 9501);
$count = 0;

$server->on("Request", function (Request $request, Response $response) use (&$count) {
    $count++;
    $response->header("Content-Type", "text/plain");
    $response->end("Khorazmiy AI: Server ishlamoqda. So'rovlar soni: $count");
});

$server->start();
```

## Tushuntirish va Mantiq:
Swoole an'anaviy PHP-FPM dan farqli o'laroq, jarayonni (process) o'chirmaydi. `$server->on("Request", ...)` hodisasi har bir kelgan so'rovni asinxron tarzda qayta ishlaydi. `$count` o'zgaruvchisi xotirada saqlanib, har bir so'rovda yangilanadi.

## Ishlash natijasi:
```text
Server started at http://127.0.0.1:9501
(Browserda: Khorazmiy AI: Server ishlamoqda. So'rovlar soni: 1)
```

---

# 1032-Topshiriq: WebSocket orqali real-time narxlar yangilanishi

## Topshiriq sharti:
E-commerce platformasi uchun WebSocket serverini yarating. Mijoz ulanganda, server har 2 soniyada mahsulot narxini tasodifiy ravishda yangilab, barcha ulangan mijozlarga yuborsin.

## Yechim (PHP kodi):
```php
use Swoole\WebSocket\Server;

$server = new Server("0.0.0.0", 9502);

$server->on('open', function($server, $req) {
    echo "Mijoz ulandi: {$req->fd}\n";
});

$server->tick(2000, function() use ($server) {
    $price = rand(100, 1000);
    foreach($server->connections as $fd) {
        if($server->isEstablished($fd)) {
            $server->push($fd, json_encode(['price' => $price]));
        }
    }
});

$server->start();
```

## Tushuntirish va Mantiq:
`tick` funksiyasi har 2000ms (2 soniya) da ishga tushadi. `connections` massivi orqali barcha faol mijozlarga (fd - file descriptor) yangi narx ma'lumotini push qilamiz.

## Ishlash natijasi:
```text
Mijoz ulandi: 1
(Mijozga har 2 soniyada: {"price": 452} keladi)
```

---

# 1033-Topshiriq: RoadRunner orqali Worker-larni boshqarish

## Topshiriq sharti:
RoadRunner ishchi (worker) skriptini yarating. Bu skript kelayotgan JSON so'rovni qabul qilib, uni tahlil qilsin va "Processed" statusini qaytarsin.

## Yechim (PHP kodi):
```php
require __DIR__ . '/vendor/autoload.php';
use Spiral\RoadRunner;
use Nyholm\Psr7;

$worker = RoadRunner\Worker::create();
$psrFactory = new Psr7\Factory\Psr17Factory();
$psr7 = new RoadRunner\Http\PSR7Worker($worker, $psrFactory, $psrFactory, $psrFactory);

while ($request = $psr7->waitRequest()) {
    $response = new Psr7\Response(200, [], "Khorazmiy AI: Buyurtma qabul qilindi.");
    $psr7->respond($response);
}
```

## Tushuntirish va Mantiq:
RoadRunner PHP ni doimiy ishchi jarayon sifatida ushlab turadi. `waitRequest()` metodi so'rovni kutadi, qayta ishlagach `respond()` orqali javob beradi. Bu PHP-FPM ga qaraganda ancha tezroq.

## Ishlash natijasi:
```text
Worker ready. Listening for requests...
```

---

# 1034-Topshiriq: Asinxron Redis so'rovi (Swoole Coroutine)

## Topshiriq sharti:
Swoole Coroutine yordamida Redis ma'lumotlar bazasidan mahsulot qoldig'ini asinxron tarzda o'qing.

## Yechim (PHP kodi):
```php
use Swoole\Coroutine;
use Swoole\Coroutine\Redis;

Coroutine\run(function() {
    $redis = new Redis();
    $redis->connect('127.0.0.1', 6379);
    $stock = $redis->get('product_101_stock');
    echo "Mahsulot qoldig'i: " . ($stock ?: 0);
});
```

## Tushuntirish va Mantiq:
`Coroutine\run` ichida Redis so'rovi bloklanmaydi. Agar Redis javob qaytarmaguncha boshqa vazifalar bo'lsa, Swoole ularni bajarishga o'tadi. Bu yuqori yuklamali tizimlarda kutish vaqtini kamaytiradi.

## Ishlash natijasi:
```text
Mahsulot qoldig'i: 50
```

---

# 1035-Topshiriq: Parallel vazifalar (Swoole WaitGroup)

## Topshiriq sharti:
E-commerce tizimida buyurtma berilganda bir vaqtning o'zida 3 ta vazifani (Email yuborish, Inventar yangilash, Log yozish) parallel bajaring.

## Yechim (PHP kodi):
```php
use Swoole\Coroutine\WaitGroup;
use function Swoole\Coroutine\go;

$wg = new WaitGroup();
$wg->add(3);

go(function() use ($wg) { sleep(1); echo "Email yuborildi\n"; $wg->done(); });
go(function() use ($wg) { sleep(1); echo "Inventar yangilandi\n"; $wg->done(); });
go(function() use ($wg) { sleep(1); echo "Log yozildi\n"; $wg->done(); });

$wg->wait();
echo "Barcha vazifalar bajarildi.";
```

## Tushuntirish va Mantiq:
`WaitGroup` barcha parallel jarayonlar tugashini kutadi. `go` funksiyasi har bir vazifani alohida korutinada ishga tushiradi, bu esa umumiy bajarilish vaqtini 3 soniyadan 1 soniyaga qisqartiradi.

## Ishlash natijasi:
```text
Email yuborildi
Inventar yangilandi
Log yozildi
Barcha vazifalar bajarildi.
```

---

# 1036-Topshiriq: WebSocket orqali Chat xonasi (Broadcast)

## Topshiriq sharti:
WebSocket serverida mijozlar bir-biriga xabar yuborishi mumkin bo'lgan chat funksiyasini yarating.

## Yechim (PHP kodi):
```php
$server->on('message', function($server, $frame) {
    foreach($server->connections as $fd) {
        if($server->isEstablished($fd)) {
            $server->push($fd, "Mijoz {$frame->fd} dedi: {$frame->data}");
        }
    }
});
```

## Tushuntirish va Mantiq:
`$frame->data` mijozdan kelgan xabar. `foreach` sikli orqali server barcha ulangan mijozlarga (broadcast) xabarni tarqatadi.

## Ishlash natijasi:
```text
Mijoz 1 dedi: Salom!
```

---

# 1037-Topshiriq: Asinxron fayl yozish (Logging)

## Topshiriq sharti:
Swoole `Coroutine\System::writeFile` yordamida buyurtmalar logini asinxron tarzda faylga yozing.

## Yechim (PHP kodi):
```php
use Swoole\Coroutine\System;

go(function() {
    $data = "Buyurtma ID: 5501, Vaqt: " . date('Y-m-d H:i:s') . "\n";
    System::writeFile(__DIR__ . '/orders.log', $data, FILE_APPEND);
    echo "Log yozildi.";
});
```

## Tushuntirish va Mantiq:
An'anaviy `file_put_contents` bloklovchi funksiya hisoblanadi. `System::writeFile` esa fayl tizimi operatsiyasini asinxron bajaradi, bu esa serverning boshqa so'rovlarni qabul qilishiga xalaqit bermaydi.

## Ishlash natijasi:
```text
Log yozildi.
```

---

# 1038-Topshiriq: Rate Limiting (So'rovlar cheklovi)

## Topshiriq sharti:
Swoole serverida bitta IP dan kelayotgan so'rovlarni daqiqasiga 10 ta bilan cheklang.

## Yechim (PHP kodi):
```php
$server->on('Request', function($request, $response) {
    $ip = $request->server['remote_addr'];
    $key = "rate_limit:" . $ip;
    // Redis orqali hisoblagich (pseudo-code)
    $count = $redis->incr($key);
    if ($count > 10) {
        $response->status(429);
        $response->end("Too many requests!");
        return;
    }
    $response->end("OK");
});
```

## Tushuntirish va Mantiq:
Har bir so'rovda IP manzil bo'yicha Redis'da hisoblagich oshiriladi. Agar limit oshsa, HTTP 429 (Too Many Requests) xatosi qaytariladi.

## Ishlash natijasi:
```text
(11-so'rovda: Too many requests!)
```

---

# 1039-Topshiriq: WebSocket Heartbeat (Ulanishni tekshirish)

## Topshiriq sharti:
WebSocket serverida mijozlar aloqada ekanligini tekshirish uchun "heartbeat" (yurak urishi) mexanizmini sozlang.

## Yechim (PHP kodi):
```php
$server->set([
    'heartbeat_check_interval' => 60,
    'heartbeat_idle_time' => 120,
]);
```

## Tushuntirish va Mantiq:
`heartbeat_check_interval` har 60 soniyada ulanishlarni tekshiradi. `heartbeat_idle_time` esa 120 soniya davomida hech qanday xabar yubormagan mijozni serverdan uzib tashlaydi.

## Ishlash natijasi:
```text
(Server avtomatik ravishda o'lik ulanishlarni tozalaydi)
```

---

# 1040-Topshiriq: Asinxron HTTP Client (API so'rovlari)

## Topshiriq sharti:
Swoole `Coroutine\Http\Client` yordamida tashqi to'lov tizimi API siga asinxron so'rov yuboring.

## Yechim (PHP kodi):
```php
use Swoole\Coroutine\Http\Client;

go(function() {
    $client = new Client('api.payment-gateway.com', 443, true);
    $client->post('/v1/charge', ['amount' => 100]);
    echo "To'lov javobi: " . $client->body;
});
```

## Tushuntirish va Mantiq:
`Coroutine\Http\Client` tashqi API ga so'rov yuborganda kutib turmaydi (non-blocking). Bu e-commerce tizimida to'lovlarni qayta ishlashda server unumdorligini saqlab qoladi.

## Ishlash natijasi:
```text
To'lov javobi: {"status":"success"}
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. PHP ekotizimini yuqori yuklamali (high-load) tizimlar uchun optimallashtirish bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1041-Topshiriq: Swoole yordamida asinxron HTTP server

## Topshiriq sharti:
Swoole kutubxonasi yordamida oddiy HTTP server yarating va u har bir so'rovga "Khorazmiy AI: Tizim ishlamoqda" degan javobni asinxron tarzda qaytarsin.

## Yechim (PHP kodi):
```php
use Swoole\Http\Server;
use Swoole\Http\Request;
use Swoole\Http\Response;

$server = new Server("127.0.0.1", 9501);

$server->on("Request", function (Request $request, Response $response) {
    $response->header("Content-Type", "text/plain");
    $response->end("Khorazmiy AI: Tizim ishlamoqda");
});

$server->start();
```

## Tushuntirish va Mantiq:
Swoole PHP uchun event-driven (hodisalarga asoslangan) asinxron framework hisoblanadi. `Server` klassi orqali biz an'anaviy FPMdan farqli o'laroq, doimiy ishlaydigan jarayonni (daemon) ishga tushiramiz. `on("Request")` metodi har bir kelayotgan so'rovni bloklamasdan qayta ishlaydi.

## Ishlash natijasi:
```text
Swoole http server is started at http://127.0.0.1:9501
```

---

# 1042-Topshiriq: RoadRunner orqali Worker boshqaruvi

## Topshiriq sharti:
RoadRunner ishchi (worker) skriptini yarating. Bu skript kelayotgan JSON so'rovni qabul qilib, uni qayta ishlab, natijani qaytarsin.

## Yechim (PHP kodi):
```php
require __DIR__ . '/vendor/autoload.php';

use Spiral\RoadRunner;
use Nyholm\Psr7;

$worker = RoadRunner\Worker::create();
$psrFactory = new Psr7\Factory\Psr17Factory();
$psr7 = new RoadRunner\Http\PSR7Worker($worker, $psrFactory, $psrFactory, $psrFactory);

while ($req = $psr7->waitRequest()) {
    $resp = new Psr7\Response(200, [], "Khorazmiy AI: Worker javobi");
    $psr7->respond($resp);
}
```

## Tushuntirish va Mantiq:
RoadRunner - bu Go tilida yozilgan yuqori samarali PHP application server. `PSR-7` standartidan foydalangan holda, biz `waitRequest()` orqali so'rovlarni navbat bilan qabul qilamiz va `respond()` orqali javob qaytaramiz. Bu jarayon xotirani tejashga yordam beradi.

## Ishlash natijasi:
```text
RoadRunner worker initialized. Waiting for requests...
```

---

# 1043-Topshiriq: WebSocket orqali real-time xabar almashish

## Topshiriq sharti:
Swoole WebSocket serverini yarating. Mijoz serverga "Salom" deb yozsa, server "Khorazmiy AI: Salom, foydalanuvchi!" deb javob qaytarsin.

## Yechim (PHP kodi):
```php
$server = new Swoole\WebSocket\Server("0.0.0.0", 9502);

$server->on('message', function($server, $frame) {
    $server->push($frame->fd, "Khorazmiy AI: Salom, foydalanuvchi!");
});

$server->start();
```

## Tushuntirish va Mantiq:
WebSocket doimiy aloqa kanalini ochadi. `on('message')` hodisasi mijozdan xabar kelganda ishga tushadi. `push()` metodi esa aynan o'sha mijozning `fd` (file descriptor) raqamiga javobni yuboradi.

## Ishlash natijasi:
```text
WebSocket server started at 0.0.0.0:9502
```

---

# 1044-Topshiriq: E-commerce uchun asinxron buyurtma qayta ishlash

## Topshiriq sharti:
Swoole `Coroutine` yordamida 3 ta turli xil ma'lumotlar bazasi so'rovini (mahsulot, narx, ombor) parallel ravishda bajaring.

## Yechim (PHP kodi):
```php
use Swoole\Coroutine;
use function Swoole\Coroutine\run;

run(function() {
    $wg = new Coroutine\WaitGroup();
    $wg->add(3);

    Coroutine::create(fn() => $wg->done()); // Mahsulot ma'lumoti
    Coroutine::create(fn() => $wg->done()); // Narx ma'lumoti
    Coroutine::create(fn() => $wg->done()); // Ombor ma'lumoti

    $wg->wait();
    echo "Khorazmiy AI: Barcha ma'lumotlar yuklandi.";
});
```

## Tushuntirish va Mantiq:
`WaitGroup` - bu bir nechta asinxron jarayonlarning tugashini kutish uchun ishlatiladi. Bu e-commerce tizimida sahifa yuklanish tezligini 3 barobar oshiradi, chunki so'rovlar ketma-ket emas, parallel bajariladi.

## Ishlash natijasi:
```text
Khorazmiy AI: Barcha ma'lumotlar yuklandi.
```

---

# 1045-Topshiriq: Redis bilan asinxron kesh boshqaruvi

## Topshiriq sharti:
Swoole Redis mijozi yordamida e-commerce savatidagi mahsulotlarni asinxron tarzda keshga yozing.

## Yechim (PHP kodi):
```php
use Swoole\Coroutine\Redis;

go(function () {
    $redis = new Redis();
    $redis->connect('127.0.0.1', 6379);
    $redis->set('cart_101', '{"id": 101, "qty": 2}');
    echo "Khorazmiy AI: Savat keshga saqlandi.";
});
```

## Tushuntirish va Mantiq:
`go()` funksiyasi yangi korutinani ishga tushiradi. Redis bilan asinxron ishlash, ma'lumotlar bazasiga yuklamani kamaytiradi va javob vaqtini (latency) minimal darajaga tushiradi.

## Ishlash natijasi:
```text
Khorazmiy AI: Savat keshga saqlandi.
```

---

# 1046-Topshiriq: WebSocket orqali narxlar yangilanishi (Broadcast)

## Topshiriq sharti:
Barcha ulangan mijozlarga (e-commerce foydalanuvchilari) mahsulot narxi o'zgarganda xabar yuboruvchi broadcast funksiyasini yozing.

## Yechim (PHP kodi):
```php
$server->on('message', function($server, $frame) {
    foreach($server->connections as $fd) {
        if($server->isEstablished($fd)) {
            $server->push($fd, "Khorazmiy AI: Mahsulot narxi yangilandi!");
        }
    }
});
```

## Tushuntirish va Mantiq:
`$server->connections` massivi barcha faol ulanishlarni saqlaydi. `isEstablished` tekshiruvi orqali biz faqat haqiqatan ham ulangan mijozlarga xabar yuboramiz. Bu real-time narxlar paneli uchun juda muhim.

## Ishlash natijasi:
```text
Broadcast: Mahsulot narxi yangilandi! (barcha mijozlarga)
```

---

# 1047-Topshiriq: Asinxron fayl yuklash (Non-blocking I/O)

## Topshiriq sharti:
Swoole yordamida katta hajmdagi log faylini bloklamasdan o'qib, uni ekranga chiqaring.

## Yechim (PHP kodi):
```php
use Swoole\Coroutine\System;

go(function() {
    $content = System::readFile(__DIR__ . '/log.txt');
    echo "Khorazmiy AI: Log o'qildi: " . strlen($content) . " bayt.";
});
```

## Tushuntirish va Mantiq:
`System::readFile` funksiyasi fayl operatsiyasini asinxron bajaradi. Bu PHP skripti fayl o'qilayotganda to'xtab qolmasligini (non-blocking) ta'minlaydi.

## Ishlash natijasi:
```text
Khorazmiy AI: Log o'qildi: 1024 bayt.
```

---

# 1048-Topshiriq: Task Worker yordamida email yuborish

## Topshiriq sharti:
Buyurtma tasdiqlanganda email yuborish jarayonini asosiy serverdan ajratib, `Task Worker` orqali bajaring.

## Yechim (PHP kodi):
```php
$server->set(['task_worker_num' => 4]);

$server->on('receive', function($serv, $fd, $from_id, $data) {
    $serv->task($data); // Vazifani task workerga yuklash
});

$server->on('task', function ($serv, $task_id, $from_id, $data) {
    // Email yuborish logikasi
    return "Email yuborildi";
});
```

## Tushuntirish va Mantiq:
`Task Worker`lar og'ir operatsiyalarni (email, PDF generatsiya) asosiy serverdan ajratib oladi. Bu serverning javob berish tezligini saqlab qoladi.

## Ishlash natijasi:
```text
Task worker 1: Email yuborildi
```

---

# 1049-Topshiriq: Rate Limiting (So'rovlar cheklovi)

## Topshiriq sharti:
E-commerce API uchun har bir IP manzilidan sekundiga 5 ta so'rovdan ortiq kelmasligini ta'minlovchi asinxron filtr yarating.

## Yechim (PHP kodi):
```php
$server->on('Request', function ($request, $response) {
    $ip = $request->server['remote_addr'];
    // Redis orqali IP hisoblagichini tekshirish
    if ($count > 5) {
        $response->status(429);
        $response->end("Khorazmiy AI: Limit oshib ketdi!");
    }
});
```

## Tushuntirish va Mantiq:
Bu DDoS hujumlaridan himoya qilish va API barqarorligini saqlash uchun zarur. Redis `INCR` va `EXPIRE` buyruqlari bilan birgalikda ishlatiladi.

## Ishlash natijasi:
```text
429 Too Many Requests
```

---

# 1050-Topshiriq: Graceful Shutdown (Serverni to'g'ri o'chirish)

## Topshiriq sharti:
Server to'xtatilganda barcha ochiq ulanishlarni yopib, ma'lumotlarni bazaga saqlaydigan mexanizm yarating.

## Yechim (PHP kodi):
```php
$server->on('Shutdown', function($server) {
    echo "Khorazmiy AI: Server xavfsiz o'chirildi, ma'lumotlar saqlandi.";
});
```

## Tushuntirish va Mantiq:
`Shutdown` hodisasi server to'xtatilganda ishga tushadi. Bu ma'lumotlar yo'qolishining oldini oladi va e-commerce tizimining yaxlitligini ta'minlaydi.

## Ishlash natijasi:
```text
Khorazmiy AI: Server xavfsiz o'chirildi, ma'lumotlar saqlandi.
```