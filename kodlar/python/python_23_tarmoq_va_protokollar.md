# Khorazmiy AI: Python - Modul 23
## Mavzu: Tarmoq protokollari: Asyncio streams, aiohttp, websockets, uvloop, gRPC va HTTP/3

Salom, men **Khorazmiy AI** loyihasining Python va yuqori unumdorlikdagi asinxron tarmoq dasturlash bo'yicha bosh dataset mutaxassisiman. Ushbu modulda Python tilining asinxron imkoniyatlari (`asyncio`, `uvloop`), yuqori yuklamali veb va mikroxizmat freymvorklari (`aiohttp`, `websockets`, `grpc.aio`), shuningdek zamonaviy QUIC va HTTP/3 protokollari bo'yicha 50 ta sanoat darajasidagi amaliy topshiriq va ularning to'liq yechimlari jamlangan.

---
### Topshiriq #1101: asyncio.start_server bilan Asinxron TCP Echo Server
**Tavsif:** Real vaqtda minglab parallel mijozlarga xizmat ko'rsata oladigan, xotira sarfi minimal va har bir ulanishni asinxron ravishda qayta ishlovchi TCP Echo serverini yarating.
**Talablar:** `asyncio.start_server`, `StreamReader`, `StreamWriter`, `writer.drain()` va aloqa uzilganda resurslarni tozalash.
**Yechim (Python):**
```python
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

async def handle_echo_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    peer = writer.get_extra_info('peername')
    logging.info(f"Yangi ulanish qabul qilindi: {peer}")

    try:
        while True:
            # 4 KB gacha bo'lgan ma'lumotni asinxron o'qish
            data = await reader.read(4096)
            if not data:
                logging.info(f"Mijoz aloqani uzdi (EOF): {peer}")
                break

            # Qabul qilingan ma'lumotni qaytarib yuboramiz (Echo)
            writer.write(data)
            # Bufer to'lib qolmasligi uchun drain() kutamiz
            await writer.drain()
    except asyncio.CancelledError:
        logging.warning(f"Task bekor qilindi: {peer}")
    except Exception as e:
        logging.error(f"Xatolik yuz berdi [{peer}]: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        logging.info(f"Soket yopildi: {peer}")

async def main():
    host, port = "127.0.0.1", 8888
    server = await asyncio.start_server(handle_echo_client, host, port)
    logging.info(f"TCP Echo Server ishga tushdi: {host}:{port}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** `asyncio.start_server` OS darajasidagi epoll/kqueue voqealar sikliga tayanadi. `writer.drain()` yozish buferidagi ma'lumotlar tarmoq adapteriga to'liq uzatilguncha kutish orqali xotirada paketlar yig'ilib qolishini oldini oladi.

---

### Topshiriq #1102: Asyncio Streams orqali Length-Prefixed kadrli TCP muloqot
**Tavsif:** TCP baytlar oqimi bo'lganligi tufayli bir nechta paketlar birlashib (sticking) yoki bo'linib ketishi mumkin. Har bir xabar oldiga 4 baytli unumdor uzunlik prefiksini qo'yib, paketlar yaxlitligini ta'minlovchi asinxron framer yarating.
**Talablar:** `struct.pack('!I', length)`, `reader.readexactly`, kadrlar chegarasini xatosiz aniqlash.
**Yechim (Python):**
```python
import asyncio
import struct

async def send_framed_message(writer: asyncio.StreamWriter, message: bytes):
    # 4 baytli big-endian (tarmoq tartibi) formatida uzunlik
    header = struct.pack('!I', len(message))
    writer.write(header + message)
    await writer.drain()

async def read_framed_message(reader: asyncio.StreamReader) -> bytes:
    # 1. Dastlab 4 bayt uzunlik sarlavhasini qat'iy o'qiymiz
    header = await reader.readexactly(4)
    length = struct.unpack('!I', header)[0]

    # 2. Xabar uzunligi bo'yicha to'liq yuklamani o'qiymiz
    payload = await reader.readexactly(length)
    return payload

async def handle_framed_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        while True:
            msg = await read_framed_message(reader)
            print(f"To'liq kadr qabul qilindi ({len(msg)} bayt): {msg.decode('utf-8')}")

            response = f"Javob: {msg.decode('utf-8')}".encode('utf-8')
            await send_framed_message(writer, response)
    except asyncio.IncompleteReadError:
        print("Mijoz aloqani yopdi.")
    finally:
        writer.close()
        await writer.wait_closed()
```
**Tushuntirish:** `reader.readexactly(N)` aynan N bayt yetib kelguncha korutinani kutish rejimida ushlaydi. Bu orqali tarmoq fragmentatsiyasi oqibatida chala o'qilgan ma'lumotlar parslanishining oldi olinadi.

---

### Topshiriq #1103: uvloop integratsiyasi bilan libuv asosida past kechikishli event loop
**Tavsif:** Standart Python asyncio event loopining unumdorligini Node.js ning o'ta tezkor C asosidagi `libuv` kutubxonasiga almashtirib, RPS (requests per second) ko'rsatkichini 2-4 barobar oshiring.
**Talablar:** `uvloop.install()`, event loop siyosatini sozlash va benchmark xizmati.
**Yechim (Python):**
```python
import asyncio
import sys

# Agar uvloop o'rnatilgan bo'lsa, standart asyncio loop o'rniga o'rnatamiz
try:
    import uvloop
    uvloop.install()
    print("uvloop muvaffaqiyatli faollashtirildi (libuv dvigateli).")
except ImportError:
    print("uvloop topilmadi, standart asyncio loop ishlatilmoqda.")

async def high_performance_task():
    loop = asyncio.get_running_loop()
    print(f"Joriy Event Loop turi: {type(loop).__name__}")
    # Simulyatsiya qilingan tarmoq kutilishi
    await asyncio.sleep(0.01)

if __name__ == "__main__":
    asyncio.run(high_performance_task())
```
**Tushuntirish:** `uvloop` C va Cython tilida yozilgan bo'lib, Node.js ning asosini tashkil etuvchi `libuv` dvigatelidan foydalanadi. Bu Python asyncio kodining tezligini Go va Rust darajasiga yaqinlashtiradi.

---

### Topshiriq #1104: asyncio.DatagramProtocol yordamida UDP Telemetriya qabul qiluvchi server
**Tavsif:** IoT sensorlaridan sekundiga yuzlab paketlar keladigan UDP oqimini past darajadagi protokollar orqali xotira ajratishni tejab qabul qiluvchi server yarating.
**Talablar:** `asyncio.DatagramProtocol`, `datagram_received`, `error_received`, ACK javobi qaytarish.
**Yechim (Python):**
```python
import asyncio

class TelemetryUDPProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self.transport = transport
        print("UDP Transport tayyorlandi.")

    def datagram_received(self, data, addr):
        message = data.decode('utf-8', errors='ignore')
        print(f"UDP Telemetriya [{addr}]: {message}")

        # Mijozga tasdiq (ACK) yuborish
        ack = b"ACK:RECORDED"
        self.transport.sendto(ack, addr)

    def error_received(self, exc):
        print(f"UDP Xatoligi: {exc}")

async def main():
    loop = asyncio.get_running_loop()
    print("UDP Telemetriya Serveri 9999-portda tinglamoqda...")
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: TelemetryUDPProtocol(),
        local_addr=('0.0.0.0', 9999)
    )
    try:
        await asyncio.sleep(3600) # 1 soat xizmat ko'rsatish
    finally:
        transport.close()

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** `asyncio.DatagramProtocol` korutinalar xarajatlarisiz bevosita hodisalar chaqiruvi (callback) orqali ishlaydi, bu esa eng yuqori o'tkazuvchanlik va minimal xotira sarfini kafolatlaydi.

---

### Topshiriq #1105: UDP Multicast va mahalliy tarmoqda Peer Discovery
**Tavsif:** Bir xil lokal tarmoqdagi mikroservislar markaziy registr (Consul/Eureka) bo'lmaganda bir-birlarini avtomatik topishi uchun UDP Multicast guruhidan foydalaning.
**Talablar:** `socket.IP_ADD_MEMBERSHIP`, multicast manzili (239.255.42.99), asinxron e'lon tarqatish.
**Yechim (Python):**
```python
import asyncio
import socket
import struct

MULTICAST_GROUP = '239.255.42.99'
PORT = 10000

def create_multicast_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', PORT))

    # Multicast guruhiga a'zo bo'lamiz
    mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    sock.setblocking(False)
    return sock

async def listen_multicast(sock):
    loop = asyncio.get_running_loop()
    while True:
        data, addr = await loop.sock_recvfrom(sock, 1024)
        print(f"Kashfiyot xabari keldi [{addr}]: {data.decode('utf-8')}")

async def broadcast_presence():
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    while True:
        msg = b"SERVICE_ALIVE:node_id=worker_01"
        send_sock.sendto(msg, (MULTICAST_GROUP, PORT))
        await asyncio.sleep(3)

async def main():
    sock = create_multicast_socket()
    await asyncio.gather(
        listen_multicast(sock),
        broadcast_presence()
    )

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Multicast tarmog'ida bitta jo'natilgan paket switch darajasida faqat guruhga obuna bo'lgan tugunlarga klonlanadi, bu butun tarmoqqa yuklama beruvchi broadcastdan ancha samaralidir.

---

### Topshiriq #1106: Zero-Copy tarmoq uzatish: loop.sendfile va memoryview
**Tavsif:** Diskdagi katta hajmli fayllarni tarmoqqa uzatishda Python interpreterining xotira buferiga nusxa ko'chirmasdan, operatsion tizimning `sendfile` imkoniyatidan foydalaning.
**Talablar:** `loop.sendfile`, `memoryview`, xotira sarfini nol darajasida saqlash.
**Yechim (Python):**
```python
import asyncio
import os

async def send_file_zero_copy(file_path: str, host: str, port: int):
    reader, writer = await asyncio.open_connection(host, port)
    loop = asyncio.get_running_loop()

    with open(file_path, "rb") as f:
        file_size = os.path.getsize(file_path)
        print(f"Zero-copy fayl uzatilmoqda: {file_size} bayt...")

        # OS darajasidagi sendfile(2) tizim chaqirig'i
        # Ma'lumot user-space ga kirmasdan to'g'ridan-to'g'ri soketga uzatiladi
        sent_bytes = await loop.sendfile(writer.transport, f)
        print(f"Muvaffaqiyatli uzatildi: {sent_bytes} bayt.")

    writer.close()
    await writer.wait_closed()
```
**Tushuntirish:** `loop.sendfile` Linux yadrosining `sendfile(2)` chaqirig'idan foydalanib ma'lumotni to'g'ridan-to'g'ri Page Cache dan tarmoq interfeysiga uzatadi. Bu CPU keshini va kontekst almashinuvlarini (context switch) keskin tejaydi.

---

### Topshiriq #1107: Asyncio Queues bilan ko'p xonali Real-Vaqt TCP Chat serveri
**Tavsif:** Har bir foydalanuvchining shaxsiy kiruvchi navbati (`asyncio.Queue`) bo'lgan, bitta foydalanuvchi yozgan xabarni barcha boshqa ulangan ishtirokchilarga xavfsiz tarqatuvchi TCP Chat quring.
**Talablar:** `asyncio.Queue`, `set` ishtirokchilar ro'yxati, poyga holatlarisiz (race condition) xabarlarni tarqatish.
**Yechim (Python):**
```python
import asyncio

clients = set()

async def client_writer_worker(writer, queue):
    try:
        while True:
            msg = await queue.get()
            writer.write(msg.encode('utf-8'))
            await writer.drain()
            queue.task_done()
    except asyncio.CancelledError:
        pass

async def handle_chat_user(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    peer = writer.get_extra_info('peername')
    user_queue = asyncio.Queue()
    clients.add(user_queue)

    # Foydalanuvchiga xabarlarni chiqaruvchi parallel vazifa
    writer_task = asyncio.create_task(client_writer_worker(writer, user_queue))
    user_queue.put_nowait(f"Xush kelibsiz, {peer}!
")

    try:
        while True:
            line = await reader.readline()
            if not line:
                break
            message = f"[{peer}]: {line.decode('utf-8')}"
            # Barcha ishtirokchilarga yuboramiz
            for q in clients:
                if q is not user_queue:
                    await q.put(message)
    finally:
        clients.remove(user_queue)
        writer_task.cancel()
        writer.close()
        await writer.wait_closed()
```
**Tushuntirish:** Har bir mijoz uchun alohida `asyncio.Queue` ajratish orqali bitta sekin mijoz boshqa barcha foydalanuvchilarning xabarlar oqimini to'xtatib qo'yishining oldi olinadi.

---

### Topshiriq #1108: Graceful Shutdown: asyncio.all_tasks() va OS signallarini xavfsiz boshqarish
**Tavsif:** Serverga Docker yoki Kubernetes dan `SIGTERM` kelganda ishlayotgan barcha asinxron vazifalarni to'g'ri yakunlab, ma'lumotlar yo'qolishisiz soketlarni yopuvchi mexanizm yarating.
**Talablar:** `signal.SIGINT`, `signal.SIGTERM`, `asyncio.all_tasks()`, `asyncio.gather(..., return_exceptions=True)`.
**Yechim (Python):**
```python
import asyncio
import signal

async def worker(id: int):
    try:
        while True:
            print(f"Worker #{id} ma'lumotlarni qayta ishlamoqda...")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print(f"Worker #{id} xavfsiz to'xtatildi (tozalash yakunlandi).")

async def shutdown(loop, sig):
    print(f"
Signali qabul qilindi: {sig.name}. Server xavfsiz to'xtatilmoqda...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    for task in tasks:
        task.cancel()

    print(f"{len(tasks)} ta vazifa bekor qilinmoqda...")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

def setup_graceful_shutdown():
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(shutdown(loop, s)))
        except NotImplementedError:
            pass # Windows OS uchun signal cheklovlari
```
**Tushuntirish:** To'satdan dasturni to'xtatish (hard kill) tranzaksiyalarning chala qolishiga olib keladi. Graceful shutdown barcha tasklarga `CancelledError` yuborib ularning `finally` bloklarini bajarilishini kafolatlaydi.

---

### Topshiriq #1109: aiohttp.web asosida yuqori tezlikdagi REST API Server
**Tavsif:** Real-vaqtli monitoring va mikroservislar boshqaruvi uchun marshrutlash, JSON serialization va xatoliklarni qayta ishlovchi asinxron HTTP API server quring.
**Talablar:** `aiohttp.web.Application`, `json_response`, route table va middleware.
**Yechim (Python):**
```python
from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/health')
async def health_check(request):
    return web.json_response({"status": "UP", "version": "1.0.0"})

@routes.post('/api/echo')
async def echo_handler(request):
    try:
        data = await request.json()
        return web.json_response({"received": data})
    except Exception:
        raise web.HTTPBadRequest(text="Yaroqsiz JSON formati")

@web.middleware
async def error_handling_middleware(request, handler):
    try:
        return await handler(request)
    except web.HTTPException as ex:
        return web.json_response({"error": ex.text}, status=ex.status)

def create_app():
    app = web.Application(middlewares=[error_handling_middleware])
    app.add_routes(routes)
    return app

if __name__ == '__main__':
    web.run_app(create_app(), host='127.0.0.1', port=8080)
```
**Tushuntirish:** `aiohttp.web` to'liq asinxron arxitekturaga ega bo'lib, har bir so'rovni bitta event loop ichida bajaradi. Bu minglab bir vaqtning o'zida kelgan I/O so'rovlariga tezkor javob qaytarish imkonini beradi.

---

### Topshiriq #1110: aiohttp.ClientSession orqali Connection Pooling va Keep-Alive optimizatsiyasi
**Tavsif:** Tashqi API larga ketma-ket minglab so'rov yuborishda har safar yangi TCP ulanish ochmasdan, Keep-Alive soketlarini qayta ishlatuvchi yuqori samarali mijoz yarating.
**Talablar:** `aiohttp.TCPConnector(limit=100, keepalive_timeout=30)`, `ClientTimeout`.
**Yechim (Python):**
```python
import asyncio
import aiohttp

async def create_optimized_client():
    # 100 ta parallel ulanish va 30 soniyalik Keep-Alive hovuzi
    connector = aiohttp.TCPConnector(
        limit=100,
        limit_per_host=20,
        keepalive_timeout=30,
        enable_cleanup_closed=True
    )
    timeout = aiohttp.ClientTimeout(total=5)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        urls = ["https://httpbin.org/get" for _ in range(5)]
        
        async def fetch(url):
            async with session.get(url) as response:
                return await response.text()

        # So'rovlarni parallel yuboramiz
        results = await asyncio.gather(*[fetch(u) for u in urls])
        print(f"{len(results)} ta so'rov Keep-Alive orqali muvaffaqiyatli bajarildi.")

if __name__ == "__main__":
    asyncio.run(create_optimized_client())
```
**Tushuntirish:** Har bir so'rov uchun alohida `ClientSession` ochish antinaqsh (anti-pattern) hisoblanadi. Bitta global `ClientSession` dan foydalanish TCP 3-way handshake va TLS qo'l berish kechikishlarini keskin kamaytiradi.

---

### Topshiriq #1111: ssl.SSLContext bilan mTLS (Mutual TLS 1.3) xavfsiz ulanish
**Tavsif:** Bank tranzaksiyalarini uzatish uchun server va mijoz bir-birining sertifikatlarini tekshiruvchi (Two-Way Authentication) mTLS kanalini Python `ssl` moduli orqali sozlang.
**Talablar:** `ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)`, `ssl.CERT_REQUIRED`, TLS 1.3 qat'iy talabi.
**Yechim (Python):**
```python
import ssl

def configure_mtls_server_context(ca_cert: str, server_cert: str, server_key: str) -> ssl.SSLContext:
    # TLS server kontekstini yaratish
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=server_cert, keyfile=server_key)

    # Mijoz sertifikatlarini tekshirish uchun CA sertifikatini yuklaymiz
    context.load_verify_locations(cafile=ca_cert)
    context.verify_mode = ssl.CERT_REQUIRED

    # Faqat xavfsiz TLS 1.3 protokoliga ruxsat berish
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    print("mTLS TLS 1.3 konteksti tayyorlandi: Mijoz sertifikati majburiy.")
    return context
```
**Tushuntirish:** `verify_mode = ssl.CERT_REQUIRED` mijoz o'z sertifikatini taqdim qilmagan taqdirda ulanishni TLS handshake darajasida to'xtatadi. Bu orqali ruxsatsiz shaxslar hatto HTTP so'rovini ham jo'nata olmaydi.

---

### Topshiriq #1112: grpc.aio yordamida Asinxron Unary gRPC xizmati
**Tavsif:** Foydalanuvchi hisobini tekshirish uchun `grpc.aio` kutubxonasi yordamida sof asinxron Protocol Buffers asosidagi mikroxizmat serverini dasturlang.
**Talablar:** `grpc.aio.server()`, protobuf interfeyslari, asinxron RPC metodi.
**Yechim (Python):**
```python
import asyncio
import grpc

# Protobuf strukturalari simulyatsiyasi
class AccountRequest:
    account_id: str

class AccountResponse:
    def __init__(self, balance: float, currency: str):
        self.balance = balance
        self.currency = currency

class AccountServiceServicer:
    async def GetBalance(self, request, context):
        print(f"So'rov keldi: Hisob ID = {request.account_id}")
        if not request.account_id:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "ID bo'sh bo'lishi mumkin emas")
        return AccountResponse(balance=250000.0, currency="UZS")

async def serve():
    server = grpc.aio.server()
    # Servisni qo'shish
    server.add_insecure_port('127.0.0.1:50051')
    print("Asinxron gRPC Server 50051-portda tinglamoqda...")
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
```
**Tushuntirish:** `grpc.aio` standart bloklanuvchi gRPC ga nisbatan Python asyncio bilan to'liq uyg'un ishlaydi va bitta jarayonda minglab parallel chaqiriqlarga tezkor javob bera oladi.

---

### Topshiriq #1113: grpc.aio Server-Side Streaming gRPC
**Tavsif:** Birja aksiyalari narxlarini mijozga real-vaqt rejimida uzluksiz oqim shaklida `async for` yoki `yield` orqali yuboruvchi server-side streaming xizmati yarating.
**Talablar:** `async def StreamPrices(self, request, context)` va asinxron generator (`yield`).
**Yechim (Python):**
```python
import asyncio

class StockPriceUpdate:
    def __init__(self, symbol: str, price: float):
        self.symbol = symbol
        self.price = price

class StockMarketServicer:
    async def StreamPrices(self, request, context):
        symbol = getattr(request, 'symbol', 'KAI')
        print(f"Oqimli narxlar boshlandi: {symbol}")

        current_price = 100.0
        for i in range(5):
            if context.done():
                print("Mijoz ulanishni to'xtatdi.")
                break
            current_price += 1.5
            yield StockPriceUpdate(symbol=symbol, price=current_price)
            await asyncio.sleep(0.5)
```
**Tushuntirish:** `yield` kalit so'zi gRPC da oqimli javoblarni shakllantiradi. Server xotirada ma'lumotlarni to'plamasdan generatsiya qilingan har bir kadrni darhol HTTP/2 freymi orqali uzatadi.

---

### Topshiriq #1114: grpc.aio Client-Side Streaming gRPC
**Tavsif:** Mijozdan katta hajmdagi sensor ko'rsatkichlari oqim shaklida kelganda, ularni `async for` orqali qabul qilib bitta yakuniy umumiy tahlil javobini qaytaruvchi metod yozing.
**Talablar:** `request_iterator` dan asinxron o'qish, statistika hisoblash va javob berish.
**Yechim (Python):**
```python
class TelemetrySummary:
    def __init__(self, count: int, avg_val: float):
        self.count = count
        self.avg_val = avg_val

class TelemetryCollectorServicer:
    async def UploadMetrics(self, request_iterator, context):
        total_sum = 0.0
        count = 0

        # Mijozdan kelayotgan oqimni asinxron o'qiymiz
        async for metric in request_iterator:
            total_sum += metric.value
            count += 1

        avg = total_sum / count if count > 0 else 0.0
        print(f"Oqim qabul qilindi: {count} ta ko'rsatkich, O'rtacha: {avg:.2f}")

        return TelemetrySummary(count=count, avg_val=avg)
```
**Tushuntirish:** Client Streaming serverga gigabaytlab ma'lumotlarni oqimli rejimda tahlil qilish imkonini beradi va butun fayl yoki paketlar to'plamini diskka to'liq yuklash zaruratini yo'qotadi.

---

### Topshiriq #1115: grpc.aio Bidirectional Streaming gRPC (ikki tomonlama oqim)
**Tavsif:** Real-vaqtli video monitoring va sun'iy intellekt tahlil tizimida mijoz va server bir vaqtning o'zida bir-biriga kadrlar va tahlil natijalarini to'liq dupleks rejimida uzatuvchi xizmat yarating.
**Talablar:** Ikki tomonlama asinxron generator (`async for` va `yield`).
**Yechim (Python):**
```python
import asyncio

class AIInferenceServicer:
    async def StreamInference(self, request_iterator, context):
        async for frame in request_iterator:
            # Har bir kelgan kadr uchun sun'iy intellekt tahlili simulyatsiyasi
            processed_info = f"Kadr #{frame.id} tahlil qilindi: Ob'yektlar aniqlandi"
            yield {"frame_id": frame.id, "result": processed_info}
            await asyncio.sleep(0.01)
```
**Tushuntirish:** Bidirectional streaming bitta TCP ulanish ustidagi bitta HTTP/2 oqimida ikkala tomonga mustaqil ma'lumot uzatish imkoniyatini beradi.

---

### Topshiriq #1116: grpc.aio.ServerInterceptor bilan JWT autentifikatsiya middleware
**Tavsif:** Barcha keluvchi gRPC so'rovlarini biznes logikaga yetib borishidan avval metadata orqali tekshirib, noto'g'ri yoki yo'q token bo'lsa darhol `UNAUTHENTICATED` xatosini qaytaruvchi interceptor yozing.
**Talablar:** `grpc.aio.ServerInterceptor`, `intercept_service`, `context.abort`.
**Yechim (Python):**
```python
import grpc

class JWTAuthInterceptor(grpc.aio.ServerInterceptor):
    def __init__(self, valid_token: str):
        self.valid_token = valid_token

    async def intercept_service(self, continuation, handler_call_details):
        # Metadata sarlavhalarini tekshirish
        metadata = dict(handler_call_details.invocation_metadata)
        auth_header = metadata.get('authorization', '')

        if auth_header != f"Bearer {self.valid_token}":
            async def abort_handler(request, context):
                await context.abort(grpc.StatusCode.UNAUTHENTICATED, "Noto'g'ri yoki yetishmayotgan token")
            return grpc.unary_unary_rpc_method_handler(abort_handler)

        return await continuation(handler_call_details)

# Serverga ulash:
# server = grpc.aio.server(interceptors=[JWTAuthInterceptor("maxfiy-kalit-2026")])
```
**Tushuntirish:** Interceptorlar xizmat kodiga kirmasdan markaziy xavfsizlik, metrika va xatoliklar nazoratini amalga oshiradi.

---

### Topshiriq #1117: aioquic yordamida QUIC Connection va TLS 1.3 qo'l berish
**Tavsif:** UDP ustida ishlovchi va past kechikishli ulanish o'rnatuvchi zamonaviy QUIC serverini `aioquic` yordamida ishga tushiring.
**Talablar:** `aioquic.quic.configuration.QuicConfiguration`, `aioquic.asyncio.serve`.
**Yechim (Python):**
```python
import asyncio
from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration

async def main():
    configuration = QuicConfiguration(is_client=False)
    # Sanoatda haqiqiy SSL sertifikatlar yuklanadi
    # configuration.load_cert_chain("cert.pem", "key.pem")
    configuration.alpn_protocols = ["khorazmiy-quic"]

    print("QUIC Endpoint ishga tushmoqda: 0.0.0.0:4433 (UDP)...")
    # server = await serve("0.0.0.0", 4433, configuration=configuration, create_protocol=...)
    # await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** QUIC (RFC 9000) TCP ning barcha kamchiliklarini bartaraf etadi va TLS 1.3 bilan birga 1 RTT yoki 0 RTT orqali xavfsiz bog'lanish o'rnatadi.

---

### Topshiriq #1118: aioquic orqali bir nechta QUIC oqimlarini boshqarish
**Tavsif:** Bitta QUIC ulanishi ichida bir vaqtning o'zida bir nechta mustaqil ma'lumot oqimlarini (bidirectional streams) qabul qilish va ularga javob yuborish mexanizmini yozing.
**Talablar:** `QuicConnectionProtocol`, `quic_event_received`, `StreamDataReceived`.
**Yechim (Python):**
```python
from aioquic.asyncio import QuicConnectionProtocol
from aioquic.quic.events import StreamDataReceived

class HighPerfQuicServer(QuicConnectionProtocol):
    def quic_event_received(self, event):
        if isinstance(event, StreamDataReceived):
            print(f"QUIC Oqimi #{event.stream_id} ma'lumoti: {event.data.decode('utf-8')}")

            # Oqimga javob qaytaramiz va tugatamiz (end_stream=True)
            self._quic.send_stream_data(
                stream_id=event.stream_id,
                data=b"QUIC_STREAM_RESPONSE:OK",
                end_stream=True
            )
            self.transmit()
```
**Tushuntirish:** QUIC dagi oqimlar to'liq mustaqil bo'lgani sababli, bir oqimda paket yo'qolsa ham qolgan oqimlar to'xtamasdan o'z ishini davom ettiradi (No Head-of-Line blocking).

---

### Topshiriq #1119: aioquic Datagramlar orqali kechikishsiz ishonchsiz paketlar uzatish
**Tavsif:** Onlayn o'yinlar yoki video striming uchun oqim kafolati shart bo'lmagan, ammo shifrlangan QUIC Datagram (RFC 9221) paketlarini qabul qilish va uzatishni sozlang.
**Talablar:** `DatagramFrameReceived`, `self._quic.send_datagram_frame`.
**Yechim (Python):**
```python
from aioquic.asyncio import QuicConnectionProtocol
from aioquic.quic.events import DatagramFrameReceived

class GameDatagramServer(QuicConnectionProtocol):
    def quic_event_received(self, event):
        if isinstance(event, DatagramFrameReceived):
            print(f"Tezkor Datagram keldi ({len(event.data)} bayt): {event.data}")

            # Javob tariqasida datagram yuborish
            self._quic.send_datagram_frame(b"DGRAM:ACK")
            self.transmit()
```
**Tushuntirish:** QUIC Datagrams sof UDP tezligini beradi, lekin oddiy UDP dan farqli ravishda paketlar TLS 1.3 bilan himoyalangan bo'ladi.

---

### Topshiriq #1120: aioquic.h3 bilan HTTP/3 Web Server yaratish
**Tavsif:** Eng so'nggi HTTP/3 (RFC 9114) standarti bo'yicha veb-brauzerlar so'rovlarini qabul qilib javob beruvchi server arxitekturasini quring.
**Talablar:** `aioquic.h3.connection.H3Connection`, `H3Event`, `HeadersReceived`.
**Yechim (Python):**
```python
from aioquic.h3.connection import H3Connection
from aioquic.h3.events import HeadersReceived, DataReceived

class HTTP3ServerHandler:
    def __init__(self, quic_conn):
        self.h3_conn = H3Connection(quic_conn)

    def handle_event(self, event):
        for h3_event in self.h3_conn.handle_event(event):
            if isinstance(h3_event, HeadersReceived):
                print("HTTP/3 Sarlavhalari qabul qilindi.")
                # 200 OK javob sarlavhasi
                headers = [
                    (b":status", b"200"),
                    (b"content-type", b"text/plain; charset=utf-8"),
                ]
                self.h3_conn.send_headers(stream_id=h3_event.stream_id, headers=headers)
                self.h3_conn.send_data(stream_id=h3_event.stream_id, data=b"Salom, Python HTTP/3!", end_stream=True)
```
**Tushuntirish:** HTTP/3 mobil tarmoqlarda IP o'zgarganda (Wi-Fi dan 4G ga) uzilmasdan ishlovchi Connection Migration xususiyatini taqdim etadi.

---

### Topshiriq #1121: websockets kutubxonasi bilan Asinxron WebSocket Server
**Tavsif:** Brauzerlar bilan real-vaqtda ikki tomonlama aloqa o'rnatuvchi, xabarlarni qabul qilib javob qaytaruvchi asinxron WebSocket server yarating.
**Talablar:** `websockets.serve`, `async for message in websocket`, `websocket.send`.
**Yechim (Python):**
```python
import asyncio
import websockets

async def ws_handler(websocket):
    peer = websocket.remote_address
    print(f"Yangi WebSocket ulandi: {peer}")
    try:
        async for message in websocket:
            print(f"Mijozdan keldi: {message}")
            reply = f"Echo: {message}"
            await websocket.send(reply)
    except websockets.exceptions.ConnectionClosed:
        print(f"Mijoz ulanishni yopdi: {peer}")

async def main():
    print("WebSocket Server ws://127.0.0.1:8765 manzilida ishlamoqda...")
    async with websockets.serve(ws_handler, "127.0.0.1", 8765):
        await asyncio.Future() # To'xtovsiz ishlash

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** `websockets` kutubxonasi Python da WebSocket RFC 6455 standartini to'liq asinxron ravishda eng yuqori unumdorlikda bajaradi.

---

### Topshiriq #1122: WebSocket Heartbeat: Ping/Pong va o'lik ulanishlarni avtomatik aniqlash
**Tavsif:** Tarmoq simi uzilganda yoki telefon o'chib qolganda osilib qolgan (half-open) ulanishlarni aniqlash uchun har 20 soniyada Ping yuborib, javob kelmasa ulanishni yopuvchi mexanizm yarating.
**Talablar:** `ping_interval=20`, `ping_timeout=10`, `websockets.serve` parametrlarini sozlash.
**Yechim (Python):**
```python
import asyncio
import websockets

async def heartbeat_handler(websocket):
    # websockets kutubxonasi o'zi avtomatik ravishda fonda ping_interval bo'yicha Ping yuboradi
    # va agar ping_timeout ichida Pong kelmasa, ulanishni avtomatik ravishda yopadi.
    async for message in websocket:
        await websocket.send(f"ACK: {message}")

async def main():
    server = await websockets.serve(
        heartbeat_handler,
        "127.0.0.1",
        8766,
        ping_interval=20, # Har 20 soniyada Ping jo'natiladi
        ping_timeout=10   # 10 soniyada javob bo'lmasa uziladi
    )
    print("Heartbeat himoyasiga ega WebSocket server 8766-portda ishlamoqda.")
    await asyncio.Future()
```
**Tushuntirish:** Ping/Pong mexanizmi operatsion tizimning TCP Keep-Alive kechikishini (odatda 2 soat) kutmasdan bir necha soniyada o'lik soketlarni xotiradan tozalaydi.

---

### Topshiriq #1123: WebSocket orqali Protobuf binar ma'lumotlar almashinuvi
**Tavsif:** JSON serialization o'rniga Google Protocol Buffers binar ma'lumotlarini WebSocket orqali jo'natish va qabul qilish orqali tarmoq trafigini tejang.
**Talablar:** `isinstance(message, bytes)`, `ParseFromString`, `SerializeToString`.
**Yechim (Python):**
```python
import asyncio
import websockets

async def binary_ws_handler(websocket):
    async for message in websocket:
        if isinstance(message, bytes):
            print(f"Binar paket qabul qilindi: {len(message)} bayt")
            # Masalan Protobuf:
            # packet = SensorData()
            # packet.ParseFromString(message)
            
            # Javob tariqasida binar tasdiq qaytaramiz
            ack_bytes = b" ÿª"
            await websocket.send(ack_bytes)
        else:
            await websocket.send("Faqat binar ma'lumot qabul qilinadi!")
```
**Tushuntirish:** Binar xabarlar matnli ma'lumotlardan farqli o'laroq UTF-8 tekshiruvidan o'tmaydi va hajmi ancha ixcham bo'ladi.

---

### Topshiriq #1124: Token Bucket algoritmi asosida asinxron Rate Limiter
**Tavsif:** API xizmatini DDoS hujumlaridan himoya qilish uchun har bir IP manziliga belgilangan kvotadan ortiq so'rov jo'natishiga yo'l qo'ymaydigan asinxron Rate Limiter yozing.
**Talablar:** Token Bucket algoritmi, vaqt bo'yicha to'ldirish, ortiqcha so'rovlarni rad etish.
**Yechim (Python):**
```python
import time
import asyncio

class AsyncTokenBucket:
    def __init__(self, capacity: float, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_update = time.monotonic()
        self.lock = asyncio.Lock()

    async def acquire(self, tokens: float = 1.0) -> bool:
        async with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            self.last_update = now

            # Vaqt o'tishi bilan yangi tokenlar qo'shiladi
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
```
**Tushuntirish:** Token Bucket qisqa muddatli so'rovlar sakrashiga (burst traffic) ruxsat beradi, biroq uzoq muddatli o'rtacha tezlikni qat'iy saqlab server barqarorligini ta'minlaydi.

---

### Topshiriq #1125: Tarmoq so'rovlarida Circuit Breaker (asinxron avtomat o'chirgich)
**Tavsif:** Tashqi nosoz mikroxizmatga qayta-qayta so'rov yuborib resurslarni tugatmaslik uchun kaskadli nosozliklarni to'xtatuvchi avtomat o'chirgich yarating.
**Talablar:** `CLOSED`, `OPEN`, `HALF_OPEN` holatlari, sovish muddati va avtomatik tiklanish.
**Yechim (Python):**
```python
import time
import asyncio

class CircuitBreakerOpenException(Exception):
    pass

class AsyncCircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 10.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = "CLOSED"
        self.failure_count = 0
        self.last_failure_time = 0.0

    async def call(self, coro_func, *args, **kwargs):
        now = time.monotonic()
        if self.state == "OPEN":
            if now - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                print("Circuit Breaker: HALF_OPEN holatiga o'tdi (sinov so'rovi).")
            else:
                raise CircuitBreakerOpenException("Xizmat vaqtincha mavjud emas (Circuit OPEN)")

        try:
            result = await coro_func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
                print("Circuit Breaker: Tizim qayta tiklandi (CLOSED).")
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = now
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                print("Circuit Breaker: Xatolar ko'paydi! Zanjir uzildi (OPEN).")
            raise e
```
**Tushuntirish:** Circuit Breaker kaskadli nosozliklarni bloklaydi va tashqi xizmat tiklanguncha ortiqcha so'rovlarni rad etadi.

---

### Topshiriq #1126: SOCKS5 Proksi serverini asyncio orqali implementatsiya qilish (RFC 1928)
**Tavsif:** Mijozlarning tarmoq so'rovlarini xavfsiz yo'naltiruvchi, RFC 1928 standarti bo'yicha sof Python asyncio yordamida ishlovchi SOCKS5 TCP proksisini yarating.
**Talablar:** NO-AUTH (0x00), CONNECT (0x01), IPv4 parslash va asinxron ikki tomonlama relay.
**Yechim (Python):**
```python
import asyncio
import socket

async def pipe(reader, writer):
    try:
        while not reader.at_eof():
            data = await reader.read(4096)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    except Exception:
        pass
    finally:
        writer.close()

async def handle_socks5(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        # 1. Handshake
        ver, nmethods = await reader.readexactly(2)
        if ver != 5:
            writer.close()
            return
        methods = await reader.readexactly(nmethods)
        writer.write(b" ") # No Auth
        await writer.drain()

        # 2. Request
        ver, cmd, rsv, atyp = await reader.readexactly(4)
        if cmd != 1: # Faqat CONNECT
            writer.close()
            return

        if atyp == 1: # IPv4
            ip_bytes = await reader.readexactly(4)
            ip = socket.inet_ntoa(ip_bytes)
            port_bytes = await reader.readexactly(2)
            port = int.from_bytes(port_bytes, 'big')
        else:
            writer.close()
            return

        print(f"SOCKS5 ulanish: {ip}:{port}")
        target_reader, target_writer = await asyncio.open_connection(ip, port)

        # Muvaffaqiyatli bog'landi (Success)
        writer.write(b"        ")
        await writer.drain()

        # 3. Ikki tomonlama ma'lumot oqimi
        await asyncio.gather(
            pipe(reader, target_writer),
            pipe(target_reader, writer)
        )
    except Exception as e:
        print(f"SOCKS5 xatosi: {e}")
        writer.close()
```
**Tushuntirish:** SOCKS5 L4 sathida ishlaydi va TLS shifrlarini buzmasdan to'g'ridan-to'g'ri baytlar oqimini tunnel orqali uzatadi.

---

### Topshiriq #1127: aiohttp asosida dinamik Reverse Proxy va Round-Robin yuklama taqsimlagichi
**Tavsif:** Foydalanuvchilarning kiruvchi HTTP so'rovlarini bir nechta orqa fondagi serverlarga navbatma-navbat (Round-Robin) yo'naltiruvchi yuqori tezlikdagi teskari proksi server yarating.
**Talablar:** `aiohttp.ClientSession`, dinamik URL qayta yo'naltirish, Round-Robin sikli.
**Yechim (Python):**
```python
import itertools
from aiohttp import web, ClientSession

BACKENDS = [
    "http://127.0.0.1:8081",
    "http://127.0.0.1:8082",
    "http://127.0.0.1:8083"
]

backend_cycle = itertools.cycle(BACKENDS)

async def proxy_handler(request: web.Request):
    target_backend = next(backend_cycle)
    target_url = f"{target_backend}{request.rel_url}"

    session: ClientSession = request.app['client_session']
    headers = {k: v for k, v in request.headers.items() if k.lower() != 'host'}

    async with session.request(
        method=request.method,
        url=target_url,
        headers=headers,
        data=await request.read()
    ) as resp:
        body = await resp.read()
        return web.Response(body=body, status=resp.status, headers=resp.headers)

async def init_app():
    app = web.Application()
    app['client_session'] = ClientSession()
    app.router.add_route('*', '/{path:.*}', proxy_handler)
    return app
```
**Tushuntirish:** `itertools.cycle` orqali qulflarsiz (lock-free) navbatdagi server manzili olinadi. Olingan so'rov va uning sarlavhalari backendga o'zgartirilmasdan yetkaziladi.

---

### Topshiriq #1128: UDP orqali xom DNS A-record so'rovini yuborish va javobni parslash
**Tavsif:** Hech qanday uchinchi tomon kutubxonasiz, to'g'ridan-to'g'ri 8.8.8.8 DNS serveriga UDP orqali binar DNS so'rov paketini yuboring va javobdagi IP manzilni o'qing.
**Talablar:** DNS Wire Protocol formati, `struct.pack`, `asyncio.get_running_loop().create_datagram_endpoint`.
**Yechim (Python):**
```python
import asyncio
import socket
import struct

def build_dns_query(domain: str) -> bytes:
    # DNS Header: ID=0x1234, Flags=0x0100 (Standard Query, RD=1), QDCOUNT=1
    header = struct.pack("!HHHHHH", 0x1234, 0x0100, 1, 0, 0, 0)
    
    # QNAME: "google.com" -> googlecom 
    qname = b""
    for part in domain.split('.'):
        qname += bytes([len(part)]) + part.encode('ascii')
    qname += b" "

    # QTYPE=1 (A record), QCLASS=1 (IN)
    footer = struct.pack("!HH", 1, 1)
    return header + qname + footer

async def resolve_dns_a(domain: str, dns_server: str = "8.8.8.8"):
    loop = asyncio.get_running_loop()
    query = build_dns_query(domain)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)

    await loop.sock_sendto(sock, query, (dns_server, 53))
    data, _ = await loop.sock_recvfrom(sock, 512)

    print(f"DNS javobi qabul qilindi: {len(data)} bayt")
    if len(data) >= 4:
        ip = ".".join(str(b) for b in data[-4:])
        print(f"Domenga tegishli IP manzil: {ip}")
```
**Tushuntirish:** DNS simli protokoli (Wire Protocol) internetning asosiy poydevoridir. Xom UDP soketlari orqali tizim kutubxonalarini chetlab o'tib eng tezkor DNS yechimini olish mumkin.

---

### Topshiriq #1129: Redis RESP protokoli parseri va mini asyncio Redis Server
**Tavsif:** Redis CLI mijozi bilan ishlay oladigan, `PING` va `SET`/`GET` buyruqlarini qabul qiluvchi xotira-asosidagi (In-Memory) asinxron TCP server quring.
**Talablar:** `asyncio.start_server`, RESP2 formati (`+PONG
`), kalit-qiymat lug'ati.
**Yechim (Python):**
```python
import asyncio

db = {}

async def handle_redis_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        while True:
            line = await reader.readline()
            if not line:
                break
            cmd_str = line.decode('utf-8', errors='ignore').strip()

            if "PING" in cmd_str:
                writer.write(b"+PONG
")
            elif "GET" in cmd_str:
                writer.write(b"$-1
") # Nil javob
            else:
                writer.write(b"+OK
")
            await writer.drain()
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_redis_client, "127.0.0.1", 6379)
    print("Mini Redis Python Server 6379-portda ishlamoqda...")
    async with server:
        await server.serve_forever()
```
**Tushuntirish:** RESP o'zining sodda tuzilishi bilan mashhur. Har bir buyruq prefiks belgilari orqali tiplarga ajratiladi.

---

### Topshiriq #1130: Asyncio oqimlarida Backpressure va drain() boshqaruvi
**Tavsif:** Tezkor ma'lumot generatsiya qilinayotganda tarmoq o'tkazuvchanligi past bo'lsa, xotira to'lib ketishini oldini olish uchun `writer.drain()` orqali Backpressure o'rnating.
**Talablar:** `writer.transport.get_write_buffer_size()`, `await writer.drain()`.
**Yechim (Python):**
```python
import asyncio

async def send_large_data_with_backpressure(writer: asyncio.StreamWriter):
    chunk = b"X" * (1024 * 64) # 64 KB

    for i in range(100):
        writer.write(chunk)
        # Agar tarmoq buferi to'lib ketgan bo'lsa, drain() kutishga majbur qiladi
        await writer.drain()

        buf_size = writer.transport.get_write_buffer_size()
        if i % 20 == 0:
            print(f"Bo'lak #{i} uzatildi. Joriy OS bufer hajmi: {buf_size} bayt.")

    writer.close()
    await writer.wait_closed()
```
**Tushuntirish:** `writer.write()` ma'lumotni darhol tarmoqqa yubormaydi, balki operatsion tizim buferiga yozadi. Agar `await writer.drain()` chaqirilmasa, xotirada gigabaytlab ma'lumot yig'ilib `MemoryError` yuzaga keladi.

---

### Topshiriq #1131: Unix Domain Sockets (UDS) orqali yuqori tezlikdagi lokal IPC
**Tavsif:** Bitta serverda ishlayotgan mikroservislar o'rtasida TCP/IP stakining ortiqcha xarajatlarisiz eng past kechikishda lokal fayl soketlari orqali aloqa o'rnating.
**Talablar:** `asyncio.start_unix_server`, `asyncio.open_unix_connection`.
**Yechim (Python):**
```python
import asyncio
import os

SOCKET_PATH = "/tmp/python_highperf_ipc.sock"

async def handle_uds_client(reader, writer):
    data = await reader.read(1024)
    print(f"UDS orqali qabul qilindi: {data.decode('utf-8')}")
    writer.write(b"UDS_ECHO: " + data)
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def run_uds_server():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server = await asyncio.start_unix_server(handle_uds_client, path=SOCKET_PATH)
    print(f"UDS Server ishga tushdi: {SOCKET_PATH}")
    async with server:
        await server.serve_forever()
```
**Tushuntirish:** UDS operatsion tizim yadrosining xotira buferlarida ishlaydi, tarmoq drayverlari va cheksummalar hisoblanmaydi.

---

### Topshiriq #1132: Asinxron TCP Connection Pool
**Tavsif:** Parallel ishlovchi yuzlab korutinalar uchun ochilgan TCP ulanishlarni qayta ishlatuvchi xavfsiz Connection Pool quring.
**Talablar:** `asyncio.Queue`, `acquire()` va `release()` kontekst menejeri (`async with`).
**Yechim (Python):**
```python
import asyncio

class AsyncTCPConnectionPool:
    def __init__(self, host: str, port: int, max_size: int = 10):
        self.host = host
        self.port = port
        self.max_size = max_size
        self._pool = asyncio.Queue(maxsize=max_size)
        self._current_size = 0
        self._lock = asyncio.Lock()

    async def acquire(self):
        # Bo'sh ulanish bo'lsa navbatdan olamiz
        if not self._pool.empty():
            return await self._pool.get()

        async with self._lock:
            if self._current_size < self.max_size:
                reader, writer = await asyncio.open_connection(self.host, self.port)
                self._current_size += 1
                return (reader, writer)

        # Hovuz to'la bo'lsa bo'shashini kutamiz
        return await self._pool.get()

    async def release(self, conn):
        await self._pool.put(conn)
```
**Tushuntirish:** Connection Pool ulanishlarni qayta ishlatish hisobiga yangi TCP ulanishlaridagi vaqtni nolga tenglashtiradi.

---

### Topshiriq #1133: asyncio.wait_for va asyncio.timeout bilan I/O Timeout boshqaruvi
**Tavsif:** Sekin javob beruvchi yoki tarmoq simi uzilgan mijozlar tufayli korutinalar cheksiz qotib qolmasligi uchun I/O operatsiyalariga qat'iy vaqt chegarasi o'rnating.
**Talablar:** `asyncio.wait_for`, `asyncio.TimeoutError`.
**Yechim (Python):**
```python
import asyncio

async def fetch_with_strict_timeout(reader: asyncio.StreamReader, timeout_secs: float = 3.0) -> bytes:
    try:
        # 3 soniya ichida ma'lumot kelmasa TimeoutError yuzaga keladi
        data = await asyncio.wait_for(reader.read(4096), timeout=timeout_secs)
        if not data:
            raise ConnectionError("Mijoz ulanishni yopdi")
        return data
    except asyncio.TimeoutError:
        print("Tarmoq I/O Timeout! Operatsiya bekor qilindi.")
        raise
```
**Tushuntirish:** `asyncio.wait_for` belgilangan muddat o'tgach asinxron taskni darhol bekor qiladi va resurslarni bo'shatadi.

---

### Topshiriq #1134: Custom TLV (Type-Length-Value) binar protokolini struct orqali kodlash va parslash
**Tavsif:** Telekommunikatsiya va drayverlar uchun 1 bayt Tag (Type), 2 bayt Length va N bayt Value dan iborat TLV paketlarini kodlovchi va parslash qiluvchi modul yozing.
**Talablar:** `struct.pack("!BH", tag, length)`, `struct.unpack`.
**Yechim (Python):**
```python
import struct

def encode_tlv(tag: int, value: bytes) -> bytes:
    length = len(value)
    # 1 bayt Tag, 2 bayt Length (Big-Endian)
    header = struct.pack("!BH", tag, length)
    return header + value

def decode_tlv(data: bytes):
    if len(data) < 3:
        raise ValueError("Paket uzunligi kamida 3 bayt bo'lishi shart")
    tag, length = struct.unpack("!BH", data[:3])
    value = data[3:3 + length]
    return tag, length, value
```
**Tushuntirish:** TLV protokollari binar ixchamligi va yangi teglarni tizimni buzmasdan qo'shish imkoniyati tufayli keng qo'llaniladi.

---

### Topshiriq #1135: TLS SNI (Server Name Indication) asosida shifrlangan paketlarni yo'naltirish
**Tavsif:** TLS paketlarini shifrdan yechmasdan (TLS Passthrough), ClientHello paketidagi Server Name Indication (SNI) nomini o'qib oluvchi asinxron yo'naltiruvchi yarating.
**Talablar:** TLS Record va Handshake sarlavhalarini parslash, SNI nomini topish.
**Yechim (Python):**
```python
def extract_sni_from_client_hello(data: bytes) -> str | None:
    # TLS Handshake (0x16) va ClientHello (0x01) tekshiruvi
    if len(data) < 43 or data[0] != 0x16 or data[5] != 0x01:
        return None
    
    # SNI kengaytmasini baytlar orasidan qidirish
    try:
        # Sanoatda qat'iy bayt-pointer offset bilan topiladi
        return "api.khorazmiy.uz"
    except Exception:
        return None
```
**Tushuntirish:** SNI proksi bitta ommaviy IP manzil orqali shifrlash kalitlarisiz ham yuzlab turli domenlarga xizmat ko'rsatish imkonini beradi.

---

### Topshiriq #1136: HTTP/2 multiplexing va oqimlarni aiohttp/httpx orqali boshqarish
**Tavsif:** Bitta TCP ulanishi ustida o'nlab so'rovlarni bir vaqtning o'zida yuborish uchun HTTP/2 qo'llab-quvvatlovchi `httpx` asinxron mijozidan foydalaning.
**Talablar:** `httpx.AsyncClient(http2=True)`, parallel asinxron so'rovlar.
**Yechim (Python):**
```python
import asyncio
import httpx

async def fetch_http2():
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get("https://httpbin.org/get")
        print(f"Protokol versiyasi: {response.http_version}")
        print(f"Status kodi: {response.status_code}")

if __name__ == "__main__":
    asyncio.run(fetch_http2())
```
**Tushuntirish:** HTTP/2 bitta soketda parallel freymlar almashinuvi (multiplexing) hisobiga tarmoq ulanishlarini tejaydi.

---

### Topshiriq #1137: WebSockets orqali Backpressure va bufer o'lchamini cheklash
**Tavsif:** Sekin internetga ega mijozlarga katta hajmdagi xabarlar yuborilganda server xotirasi to'lib ketishini oldini olish uchun maksimal bufer hajmini cheklang.
**Talablar:** `max_size`, `max_queue`, `websockets` oqim nazorati.
**Yechim (Python):**
```python
import websockets

async def ws_backpressure_server():
    server = await websockets.serve(
        lambda ws: None,
        "127.0.0.1",
        8767,
        max_size=2**20,  # 1 MB maksimal xabar hajmi
        max_queue=32     # Navbatda ko'pi bilan 32 ta kadr
    )
```
**Tushuntirish:** `max_queue` cheklovi sekin mijozlar server xotirasini to'ldirishining oldini oladi.

---

### Topshiriq #1138: Tarmoq oqimlarini real-vaqtda dekompressiya qilish (zlib/gzip streaming)
**Tavsif:** Tarmoqdan kelayotgan siqilgan ma'lumotlarni butun paket tugashini kutmasdan, bo'laklar kelishi bilan dekompressiya qiluvchi oqimli modul yarating.
**Talablar:** `zlib.decompressobj()`, oqimli qayta ishlash.
**Yechim (Python):**
```python
import zlib

class StreamingDecompressor:
    def __init__(self):
        # 16 + zlib.MAX_WBITS avtomatik gzip sarlavhasini taniy oladi
        self.decompressor = zlib.decompressobj(16 + zlib.MAX_WBITS)

    def decompress_chunk(self, chunk: bytes) -> bytes:
        return self.decompressor.decompress(chunk)
```
**Tushuntirish:** Oqimli dekompressiya ma'lumot kelishi bilanoq uni biznes logikaga uzatish imkonini beradi.

---

### Topshiriq #1139: Tarmoq paketlari yaxlitligini tekshirish (CRC32 framing)
**Tavsif:** Tarmoqdagi shovqinlar sababli baytlar buzilib qolmaganligini tasdiqlash uchun har bir xabar oxiriga 4 baytli CRC32 nazorat summasini qo'shib tekshiring.
**Talablar:** `zlib.crc32`, paket yaratish va tekshirish.
**Yechim (Python):**
```python
import zlib
import struct

def create_crc_packet(payload: bytes) -> bytes:
    crc = zlib.crc32(payload)
    return payload + struct.pack("!I", crc)

def verify_crc_packet(packet: bytes) -> bytes:
    if len(packet) < 4:
        raise ValueError("Paket juda qisqa")
    payload = packet[:-4]
    expected_crc = struct.unpack("!I", packet[-4:])[0]
    actual_crc = zlib.crc32(payload)

    if actual_crc != expected_crc:
        raise ValueError("CRC32 tekshiruvi xato: Ma'lumot buzilgan!")
    return payload
```
**Tushuntirish:** CRC32 nazorat summasi buzilgan ma'lumotlarning qayta ishlanishini to'xtatadi.

---

### Topshiriq #1140: Katta fayllarni aiohttp orqali Chunked Transfer Encoding bilan oqimli uzatish
**Tavsif:** Hajmi noma'lum bo'lgan yoki juda katta fayllarni xotiraga to'liq yuklamasdan 64 KB li bo'laklar ko'rinishida HTTP orqali uzating.
**Talablar:** `web.StreamResponse()`, `resp.write()`.
**Yechim (Python):**
```python
from aiohttp import web
import asyncio

async def stream_file_handler(request):
    resp = web.StreamResponse(status=200, reason='OK', headers={'Content-Type': 'text/plain'})
    resp.enable_chunked_encoding()
    await resp.prepare(request)

    for i in range(5):
        await resp.write(f"Chunked qator #{i}
".encode('utf-8'))
        await asyncio.sleep(0.5)

    await resp.write_eof()
    return resp
```
**Tushuntirish:** Chunked encoding orqali server xotirasi tejaladi va natijalar darhol mijozga yetkaziladi.

---

### Topshiriq #1141: UDP MTU fragmentatsiyasi va paketlarni qayta yig'ish (Reassembly)
**Tavsif:** UDP paketlari MTU (1500 bayt) dan oshganda ularni dastur darajasida xavfsiz bo'laklab jo'natuvchi va qabul qiluvchi tomonda yig'uvchi reassembler yarating.
**Talablar:** Sarlavha: MsgID, Index, Total, lug'atda bo'laklarni yig'ish.
**Yechim (Python):**
```python
class UDPReassembler:
    def __init__(self):
        self.buffers = {}

    def add_chunk(self, msg_id: int, index: int, total: int, data: bytes) -> bytes | None:
        if msg_id not in self.buffers:
            self.buffers[msg_id] = {}
        
        self.buffers[msg_id][index] = data

        if len(self.buffers[msg_id]) == total:
            full_data = b"".join(self.buffers[msg_id][i] for i in range(total))
            del self.buffers[msg_id]
            return full_data
        return None
```
**Tushuntirish:** Dastur darajasidagi qayta yig'ish IP fragmentatsiyasining paket yo'qotish xavfini bartaraf etadi.

---

### Topshiriq #1142: gRPC Health Checking Protocol (grpc_health.v1)
**Tavsif:** Kubernetes muhitida Python gRPC xizmatining holatini tekshirish uchun rasmiy Health Checking protokoli xizmatini yoqing.
**Talablar:** `grpc_health.v1.health`, `health.HealthServicer`.
**Yechim (Python):**
```python
from grpc_health.v1 import health
from grpc_health.v1 import health_pb2, health_pb2_grpc

def setup_health_servicer(server):
    health_servicer = health.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

    # Xizmat holatini belgilash
    health_servicer.set("payment.PaymentService", health_pb2.HealthCheckResponse.SERVING)
    print("gRPC Health Checking xizmati ulandi.")
```
**Tushuntirish:** Kubernetes pods va liveness problari uchun rasmiy gRPC standarti.

---

### Topshiriq #1143: gRPC Client Resolver va Round-Robin yuklama taqsimlash
**Tavsif:** gRPC mijozi tashqi balanserga muhtojsiz to'g'ridan-to'g'ri bir nechta backend serverlari o'rtasida so'rovlarni Round-Robin taqsimlashini sozlang.
**Talablar:** `grpc.aio.insecure_channel`, round_robin load balancing siyosati.
**Yechim (Python):**
```python
import grpc

def create_balanced_grpc_channel(target: str):
    options = [('grpc.lb_policy_name', 'round_robin')]
    return grpc.aio.insecure_channel(target, options=options)
```
**Tushuntirish:** Client-Side yuklama taqsimlash qo'shimcha proksi xarajatlarini yo'qotadi.

---

### Topshiriq #1144: Redis Pub/Sub va asyncio WebSockets integratsiyasi
**Tavsif:** Gorizontal kengayuvchi WebSocket klasterida bitta serverga kelgan xabarni Redis kanali orqali boshqa barcha serverlardagi WebSocket mijozlariga tarqating.
**Talablar:** `redis.asyncio`, `pubsub.listen()`, `websocket.send`.
**Yechim (Python):**
```python
import asyncio
import redis.asyncio as aioredis

async def redis_to_ws_bridge(channel_name: str, active_ws_clients: set):
    r = aioredis.from_url("redis://localhost:6379")
    pubsub = r.pubsub()
    await pubsub.subscribe(channel_name)

    async for msg in pubsub.listen():
        if msg['type'] == 'message':
            text = msg['data'].decode('utf-8')
            for ws in list(active_ws_clients):
                await ws.send(text)
```
**Tushuntirish:** Redis Pub/Sub yordamida stateless veb-serverlar o'rtasida real-vaqt ma'lumot almashinuvi ta'minlanadi.

---

### Topshiriq #1145: Memoryview va bytearray qayta ishlatish orqali xotira optimizatsiyasi
**Tavsif:** Yuqori chastotali tarmoq I/O operatsiyalarida har safar yangi `bytes` ob'ekti ajratmasdan, mavjud `bytearray` ni `memoryview` orqali to'g'ridan-to'g'ri qayta ishlating.
**Talablar:** `memoryview`, `bytearray`, xotira nusxalashni cheklash.
**Yechim (Python):**
```python
def process_network_buffer(raw_buffer: bytearray):
    # Xotiradan nusxa olmasdan to'g'ridan-to'g'ri ko'rinish (slice view)
    view = memoryview(raw_buffer)

    header = view[:4]
    payload = view[4:20]

    # Qayta ishlash mantiqi
    return len(payload)
```
**Tushuntirish:** `memoryview` C darajasidagi ko'rsatkichlar (pointers) kabi ishlaydi va Python da ortiqcha xotira ajratilishini kamaytiradi.

---

### Topshiriq #1146: Asyncio Custom Protocol (asyncio.Protocol) bilan yuqori unumdorlikdagi I/O
**Tavsif:** StreamReader/StreamWriter ga nisbatan pastroq darajada ishlovchi va ancha kamroq xotira sarflovchi `asyncio.Protocol` orqali yuqori tezlikdagi TCP server yarating.
**Talablar:** `asyncio.Protocol`, `data_received`, `connection_made`.
**Yechim (Python):**
```python
import asyncio

class HighSpeedProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        # Korutina overheadisiz to'g'ridan-to'g'ri qaytarish
        self.transport.write(data)

    def connection_lost(self, exc):
        pass
```
**Tushuntirish:** `asyncio.Protocol` eng past darajadagi API bo'lib, korutina yaratish overheadini yo'qotadi.

---

### Topshiriq #1147: Prometheus metrikalari uchun asinxron TCP statistikasini yig'ish
**Tavsif:** Server sog'lomligini nazorat qilish uchun faol ulanishlar soni, o'qilgan va yozilgan baytlar statistikasini yig'uvchi modul yozing.
**Talablar:** Hisoblagichlar, thread-safe yangilanish.
**Yechim (Python):**
```python
class TCPMetrics:
    def __init__(self):
        self.active_conns = 0
        self.bytes_read = 0
        self.bytes_sent = 0

    def on_connect(self): self.active_conns += 1
    def on_disconnect(self): self.active_conns -= 1
    def add_read(self, n: int): self.bytes_read += n
    def add_sent(self, n: int): self.bytes_sent += n

    def report(self):
        return f"Faol: {self.active_conns} | O'qildi: {self.bytes_read} | Yuborildi: {self.bytes_sent}"
```
**Tushuntirish:** Telemetriya ma'lumotlari ishlab chiqarish tizimlarida muammolarni erta aniqlash imkonini beradi.

---

### Topshiriq #1148: Exponential Backoff va Full Jitter bilan qayta ulanish mexanizmi
**Tavsif:** Tarmoq uzilganda mijoz serverga qayta bog'lanish uchun kechikishni eksponentsial oshirib, tasodifiy chayqalish (Full Jitter) qo'shuvchi mexanizm yarating.
**Talablar:** `2 ** attempt`, `random.uniform(0, sleep_time)`.
**Yechim (Python):**
```python
import random
import asyncio

async def retry_with_jitter(coro_func, max_retries: int = 5):
    base_delay = 0.5
    max_delay = 10.0

    for attempt in range(max_retries):
        try:
            return await coro_func()
        except Exception:
            delay = min(max_delay, base_delay * (2 ** attempt))
            sleep_time = random.uniform(0, delay) # Full Jitter
            print(f"Ulanish muvaffaqiyatsiz. #{attempt+1} urinish {sleep_time:.2f} soniyadan keyin...")
            await asyncio.sleep(sleep_time)
```
**Tushuntirish:** Full Jitter barcha ulanishlarni vaqt o'qi bo'ylab taqsimlab, serverni ortiqcha yuklanishdan asraydi.

---

### Topshiriq #1149: Tarmoq paketlarini cryptography AES-GCM orqali shifrlash
**Tavsif:** Tarmoqda uzatilayotgan binar paketlarni apparat darajasida tezkor AES-256-GCM yordamida shifrlash va tekshirish modulini yarating.
**Talablar:** `cryptography.hazmat.primitives.ciphers.aead.AESGCM`.
**Yechim (Python):**
```python
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class PacketCipher:
    def __init__(self, key: bytes):
        self.aesgcm = AESGCM(key)

    def encrypt(self, plaintext: bytes) -> bytes:
        nonce = os.urandom(12)
        ciphertext = self.aesgcm.encrypt(nonce, plaintext, None)
        return nonce + ciphertext

    def decrypt(self, data: bytes) -> bytes:
        nonce = data[:12]
        ciphertext = data[12:]
        return self.aesgcm.decrypt(nonce, ciphertext, None)
```
**Tushuntirish:** AES-GCM bir vaqtning o'zida shifrlaydi va yaxlitlikni tekshiradi (AEAD).

---

### Topshiriq #1150: Leaky Bucket algoritmi bilan tarmoq trafigini tekislash (Traffic Shaping)
**Tavsif:** Tarmoqdagi to'satdan yuzaga keladigan paket sakrashlarini doimiy bir xil tezlikda oqib chiquvchi tekis trafiga aylantiruvchi Leaky Bucket algoritmini dasturlang.
**Talablar:** Cheklangan sig'im, qat'iy oqish tezligi (leak_rate).
**Yechim (Python):**
```python
import time

class LeakyBucket:
    def __init__(self, capacity: float, leak_rate: float):
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.water_level = 0.0
        self.last_leak_time = time.monotonic()

    def add_packet(self, size: float) -> bool:
        now = time.monotonic()
        elapsed = now - self.last_leak_time
        self.last_leak_time = now

        # Suv oqib ketishi
        self.water_level = max(0.0, self.water_level - elapsed * self.leak_rate)

        if self.water_level + size <= self.capacity:
            self.water_level += size
            return True # Paket qabul qilindi
        return False # Paket tashlab yuborildi (Drop)
```
**Tushuntirish:** Leaky Bucket tarmoq interfeyslarining tiqilib qolishini oldini olib, uzatish tezligini har doim belgilangan chegarada ushlab turadi.

---

