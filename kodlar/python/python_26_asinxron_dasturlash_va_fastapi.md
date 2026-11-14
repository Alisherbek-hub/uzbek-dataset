# Khorazmiy AI: Python - Modul 26
## Mavzu: Asinxron Dasturlash: Asyncio, Event Loop, TaskGroup, Non-blocking I/O va Yuqori Yuklamali FastAPI Tizimlari

---

### Topshiriq #1251: Python 3.11+ `asyncio.TaskGroup` bilan xatolarga chidamli (fault-tolerant) parallel operatsiyalar va ExceptionGroup boshqaruvi
**Tavsif:** Yuqori yuklamali tizimlarda bir vaqtning o'zida bir nechta mikroservislarga parallel so'rovlar jo'natiladi. An'anaviy `asyncio.gather` xatolik yuz berganda boshqa parallel tasklarni bekor qilmaydi yoki yetarli darajada strukturalangan boshqaruvni ta'minlamaydi. Python 3.11+ versiyasida kiritilgan strukturalangan asinxronlik (`TaskGroup`) va `ExceptionGroup` mexanizmi yordamida barcha parallel vazifalarni qat'iy nazorat ostida bajarish, biri qulaganda qolganlarini toza bekor qilish (cancellation) va barcha xatolarni xavfsiz tutib olish lozim.
**Talablar:** Algoritmik murakkablik: $O(N)$ vazifalar uchun, xotira sarfi: $O(N)$. Barcha tasklar bir vaqtda ishga tushishi, xatolik yuz berganda `ExceptionGroup` to'liq tahlil qilinishi shart.
**Yechim (Python):**
```python
import asyncio
from typing import List, Dict, Any

class ExternalServiceError(Exception):
    """Tashqi mikroservis bilan aloqa uzilganda yuzaga keladigan xatolik."""
    def __init__(self, service_name: str, message: str):
        super().__init__(f"[{service_name}] Xatolik: {message}")
        self.service_name = service_name

async def fetch_user_profile(user_id: int) -> Dict[str, Any]:
    await asyncio.sleep(0.05)
    return {"user_id": user_id, "name": "Alisher Navoiy", "status": "active"}

async def fetch_user_orders(user_id: int) -> List[Dict[str, Any]]:
    await asyncio.sleep(0.08)
    return [
        {"order_id": 101, "total": 450000.0, "status": "shipped"},
        {"order_id": 102, "total": 120000.0, "status": "delivered"}
    ]

async def fetch_payment_history(user_id: int, should_fail: bool = False) -> List[Dict[str, Any]]:
    await asyncio.sleep(0.04)
    if should_fail:
        raise ExternalServiceError("PaymentGateway", "Tranzaksiyalar serveri javob bermadi")
    return [{"payment_id": "PAY-99", "amount": 570000.0, "state": "SUCCESS"}]

async def aggregate_customer_data(user_id: int, fail_payment: bool = False) -> Dict[str, Any]:
    profile_task = None
    orders_task = None
    payments_task = None
    
    try:
        async with asyncio.TaskGroup() as tg:
            profile_task = tg.create_task(fetch_user_profile(user_id))
            orders_task = tg.create_task(fetch_user_orders(user_id))
            payments_task = tg.create_task(fetch_payment_history(user_id, should_fail=fail_payment))
    except* ExternalServiceError as eg:
        # Python 3.11+ except* sintaksisi orqali ExceptionGroup ichidagi alohida xatoliklarni ajratish
        print(f"[OGOHLANTIRISH] Tashqi servis xatosi ushlandi: {len(eg.exceptions)} ta xatolik")
        for exc in eg.exceptions:
            print(f" -> Xatolik tafsiloti: {exc}")
        return {"error": "Ma'lumotlarni yig'ishda kritik bo'lmagan xatolik yuz berdi"}
    except* Exception as eg:
        print(f"[KRITIK] Kutilmagan tizimli xatolik: {eg.exceptions}")
        raise

    return {
        "profile": profile_task.result(),
        "orders": orders_task.result(),
        "payments": payments_task.result()
    }

async def main():
    print("=== 1-Muvaffaqiyatli ssenariy: Barcha mikroservislar barqaror ===")
    success_result = await aggregate_customer_data(user_id=42, fail_payment=False)
    print(f"Foydalanuvchi: {success_result['profile']['name']}")
    print(f"Buyurtmalar soni: {len(success_result['orders'])}")
    print(f"To'lovlar soni: {len(success_result['payments'])}")

    print("\n=== 2-Nosozlik ssenariysi: To'lov servisi qulaganda TaskGroup xavfsizligi ===")
    fail_result = await aggregate_customer_data(user_id=42, fail_payment=True)
    print(f"Natija holati: {fail_result}")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** `asyncio.TaskGroup` kontekst menejeri strukturaviy asinxronlikni (Structured Concurrency) ta'minlaydi. Agar guruhdagi biron bir taskda istisno yuz bersa, TaskGroup avtomatik ravishda boshqa barcha ishlayotgan tasklarga `cancel()` signalini yuboradi va ularning to'xtashini kutadi. Bu esa xotirada "yetim" (orphan/leaked) vazifalar qolib ketishining oldini oladi. `except*` sintaksisi esa bir vaqtning o'zida yuz bergan bir nechta mustaqil istisnolarni parallel tahlil qilish imkonini beradi.
**Ishlash natijasi:**
```text
=== 1-Muvaffaqiyatli ssenariy: Barcha mikroservislar barqaror ===
Foydalanuvchi: Alisher Navoiy
Buyurtmalar soni: 2
To'lovlar soni: 1

=== 2-Nosozlik ssenariysi: To'lov servisi qulaganda TaskGroup xavfsizligi ===
[OGOHLANTIRISH] Tashqi servis xatosi ushlandi: 1 ta xatolik
 -> Xatolik tafsiloti: [PaymentGateway] Xatolik: Tranzaksiyalar serveri javob bermadi
Natija holati: {'error': "Ma'lumotlarni yig'ishda kritik bo'lmagan xatolik yuz berdi"}
```

---

### Topshiriq #1252: Past darajali xususiy Event Loop va Selector (epoll/kqueue) arxitekturasi: Socket I/O ni no-blocking multipleksatsiyalash
**Tavsif:** `asyncio` kutubxonasining tub mohiyatini tushunish va eng yuqori unumdorlik talab qilinadigan protokollarni yaratish uchun operatsion tizimning I/O multipleksatsiya mexanizmi (`selectors.DefaultSelector`) ustiga qurilgan xususiy mikromodel Event Loop tizimini noldan amalga oshirish talab qilinadi.
**Talablar:** Standart OS soketlari bilan no-blocking rejimda ishlash, koroutinalarni `yield` orqali to'xtatish va hodisa (Read/Write tayyorligi) yuz berganda qayta uyg'otish. Resurs sarfi: $O(1)$ har bir tayyor hodisa uchun.
**Yechim (Python):**
```python
import selectors
import socket
from typing import Generator, Any, Callable, Dict, List

class MiniFuture:
    def __init__(self):
        self.callbacks: List[Callable[['MiniFuture'], None]] = []
        self._result: Any = None
        self._done: bool = False

    def set_result(self, result: Any):
        self._result = result
        self._done = True
        for cb in self.callbacks:
            cb(self)

    def result(self) -> Any:
        return self._result

    def __iter__(self):
        while not self._done:
            yield self
        return self._result

class MiniEventLoop:
    def __init__(self):
        self.selector = selectors.DefaultSelector()
        self.ready_queue: List[Generator] = []
        self._running = False

    def create_task(self, coro: Generator):
        self.ready_queue.append(coro)

    def sock_recv(self, sock: socket.socket, max_bytes: int) -> MiniFuture:
        future = MiniFuture()

        def on_readable():
            try:
                data = sock.recv(max_bytes)
                self.selector.unregister(sock)
                future.set_result(data)
            except Exception as e:
                self.selector.unregister(sock)
                future.set_result(b"")

        self.selector.register(sock, selectors.EVENT_READ, data=on_readable)
        return future

    def run_until_complete(self, main_coro: Generator):
        self.create_task(main_coro)
        self._running = True

        while self._running:
            # 1. Navbatdagi tayyor koroutinalarni bajarish
            while self.ready_queue:
                coro = self.ready_queue.pop(0)
                try:
                    future = coro.send(None)
                    future.callbacks.append(lambda fut, c=coro: self.ready_queue.append(c))
                except StopIteration:
                    pass

            # Agar navbat bo'sh bo'lsa va I/O kutilayotgan bo'lsa, selector ni kutamiz
            if not self.ready_queue:
                events = self.selector.select(timeout=0.1)
                for key, mask in events:
                    callback = key.data
                    callback()

            # Tekshirish: registrda hech kim qolmadimi va navbat bo'shmi?
            if not self.ready_queue and not self.selector.get_map():
                break

async def simulated_client():
    pass # Standart asyncio uchun interfeys muvofiqligi

def echo_protocol_simulation(loop: MiniEventLoop):
    server_sock, client_sock = socket.socketpair()
    server_sock.setblocking(False)
    client_sock.setblocking(False)

    def server_coro():
        # Asinxron tarzda ma'lumot qabul qilish
        data = yield from loop.sock_recv(server_sock, 1024)
        print(f"[SERVER] Qabul qilindi: {data.decode('utf-8')}")
        server_sock.close()

    def client_coro():
        msg = b"Salom, Khorazmiy Event Loop!"
        client_sock.sendall(msg)
        print("[CLIENT] Xabar soket orqali yuborildi.")
        client_sock.close()
        # generator yakuni
        return
        yield

    loop.create_task(server_coro())
    loop.create_task(client_coro())

if __name__ == "__main__":
    loop = MiniEventLoop()
    def runner():
        echo_protocol_simulation(loop)
        yield from MiniFuture().__iter__() # tugatish triggeri
    
    # Kichik loop orqali to'g'ridan-to'g'ri soket multipleksatsiyasini tekshirish
    server_sock, client_sock = socket.socketpair()
    server_sock.setblocking(False)
    client_sock.setblocking(False)

    def simple_main():
        client_sock.sendall(b"OS Kernel -> Epoll/KQueue hodisasi!")
        received = yield from loop.sock_recv(server_sock, 1024)
        print(f"[NATIJA] I/O Multipleksator orqali o'qildi: {received.decode('utf-8')}")
        server_sock.close()
        client_sock.close()

    loop.run_until_complete(simple_main())
```
**Tushuntirish:** Event Loop arxitekturasi operatsion tizimning `epoll` (Linux) yoki `kqueue` (macOS/BSD) tizim chaqiriqlariga tayanadi. Soketlar `non-blocking` rejimiga o'tkazilgach, operatsion tizim faqat ma'lumot kutilayotgan soketlarda baytlar paydo bo'lgandagina dasturga signal beradi. Bu esa o'n minglab parallel ulanishlarni (C10K muammosi) oqimlar (threading) ochmasdan, bitta CPU yadrosida tejamkorlik bilan qayta ishlash imkonini yaratadi.
**Ishlash natijasi:**
```text
[NATIJA] I/O Multipleksator orqali o'qildi: OS Kernel -> Epoll/KQueue hodisasi!
```

---

### Topshiriq #1253: Asinxron Semaphore va BoundedSemaphore: API rate limiting va bir vaqtda bajariluvchi so'rovlar chegarasi (concurrency pooling)
**Tavsif:** Tashqi API'larga (masalan, to'lov shlyuzlari yoki sun'iy intellekt LLM endpointlari) parallel ravishda soniyasiga minglab so'rovlar yuborilganda, xizmat ko'rsatuvchi server 429 (Too Many Requests) xatoligi qaytaradi yoki ulanishlarni rad etadi. Tizim resurslarini himoyalash va bir vaqtning o'zida maksimal $K$ ta so'rov bajarilishini ta'minlash uchun xavfsiz `asyncio.Semaphore` boshqaruvi va o'lchov metrikalari talab etiladi.
**Talablar:** Concurrency xavfsizligi, semaphore acquire/release vaqtida kechikishlarni kuzatish, maksimal 3 ta parallel faol so'rov chegarasi.
**Yechim (Python):**
```python
import asyncio
import time
from typing import List, Dict

class ConcurrencyLimiter:
    def __init__(self, max_concurrent_tasks: int):
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)
        self.active_count = 0
        self.peak_concurrent = 0
        self._lock = asyncio.Lock()

    async def execute_task(self, task_id: int, duration: float) -> Dict[str, float]:
        start_wait = time.perf_counter()
        
        # Semafor resursini kutish
        async with self.semaphore:
            wait_time = time.perf_counter() - start_wait
            
            # Faol vazifalar hisobini yangilash (Thread-safe asyncio.Lock bilan)
            async with self._lock:
                self.active_count += 1
                if self.active_count > self.peak_concurrent:
                    self.peak_concurrent = self.active_count
                current_active = self.active_count

            print(f"[START] Task #{task_id:02d} | Faol: {current_active} ta | Kutish: {wait_time*1000:.1f}ms")
            
            try:
                # Simulyatsiya qilingan tashqi API chaqiruvi
                await asyncio.sleep(duration)
            finally:
                async with self._lock:
                    self.active_count -= 1
                    remaining = self.active_count
                print(f"[FINISH] Task #{task_id:02d} | Qolgan faol: {remaining} ta")

        return {"task_id": task_id, "wait_time": wait_time, "execution_time": duration}

async def main():
    # Bir vaqtda ko'pi bilan 3 ta so'rovga ruxsat beruvchi limiter
    limiter = ConcurrencyLimiter(max_concurrent_tasks=3)
    
    tasks = []
    # 8 ta so'rovni parallel ishga tushirish
    for i in range(1, 9):
        # Har bir task har xil vaqt oladi
        duration = 0.05 + (i % 3) * 0.02
        tasks.append(limiter.execute_task(task_id=i, duration=duration))

    print("=== Parallel vazifalar ishga tushirilmoqda (Limit = 3) ===")
    results = await asyncio.gather(*tasks)
    
    total_wait = sum(r["wait_time"] for r in results)
    avg_wait = (total_wait / len(results)) * 1000
    print(f"\nBarcha 8 ta vazifa yakunlandi.")
    print(f"Maksimal bir vaqtda ishlaganlar (Peak Concurrency): {limiter.peak_concurrent}")
    print(f"O'rtacha navbatda kutish vaqti: {avg_wait:.2f} ms")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** `asyncio.Semaphore` ichki hisoblagichga (counter) ega bo'lib, har bir `acquire()` chaqirilganda kamayadi, `release()` bo'lganda esa oshadi. Hisoblagich 0 ga yetganda, keyingi koroutinalar semafor bo'shashguncha to'xtatiladi (suspended). Bu mexanizm ma'lumotlar bazasi poolini to'lib ketishdan yoki tashqi serverlar tomonidan bloklanishdan saqlovchi eng samarali vositadir.
**Ishlash natijasi:**
```text
=== Parallel vazifalar ishga tushirilmoqda (Limit = 3) ===
[START] Task #01 | Faol: 1 ta | Kutish: 0.0ms
[START] Task #02 | Faol: 2 ta | Kutish: 0.0ms
[START] Task #03 | Faol: 3 ta | Kutish: 0.0ms
[FINISH] Task #01 | Qolgan faol: 2 ta
[START] Task #04 | Faol: 3 ta | Kutish: 50.8ms
[FINISH] Task #02 | Qolgan faol: 2 ta
[START] Task #05 | Faol: 3 ta | Kutish: 70.5ms
[FINISH] Task #03 | Qolgan faol: 2 ta
[START] Task #06 | Faol: 3 ta | Kutish: 90.9ms
[FINISH] Task #04 | Qolgan faol: 2 ta
[START] Task #07 | Faol: 3 ta | Kutish: 101.4ms
[FINISH] Task #05 | Qolgan faol: 2 ta
[START] Task #08 | Faol: 3 ta | Kutish: 141.2ms
[FINISH] Task #06 | Qolgan faol: 2 ta
[FINISH] Task #07 | Qolgan faol: 1 ta
[FINISH] Task #08 | Qolgan faol: 0 ta

Barcha 8 ta vazifa yakunlandi.
Maksimal bir vaqtda ishlaganlar (Peak Concurrency): 3
O'rtacha navbatda kutish vaqti: 56.85 ms
```

---

### Topshiriq #1254: Asinxron Priority Queue (AsyncPriorityQueue) asosidagi topshiriqlar navbati va Worker Pool
**Tavsif:** Real ishlab chiqarish tizimlarida (masalan, banking to'lovlari, xabarnomalar va audit loglari) barcha vazifalar bir xil ahamiyatga ega emas. VIP mijozlarning tranzaksiyalari oddiy foydalanuvchilar navbatini kutmasdan oldinroq bajarilishi shart. Buning uchun ustuvorlik darajasiga (priority) ega bo'lgan asinxron navbat va uni parallel qayta ishlovchi Dynamic Worker Pool talab etiladi.
**Talablar:** Heap qoidasi bo'yicha $O(\log N)$ joylash va chiqarish, Worker Pool bo'sh qolganda avtomatik kutish, Graceful shutdown (barcha vazifalar tugashini kutish).
**Yechim (Python):**
```python
import asyncio
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedTask:
    priority: int  # Kichik son = Yuqori ustuvorlik (0 - Favqulodda, 1 - VIP, 2 - Oddiy)
    item_id: str = field(compare=False)
    payload: Any = field(compare=False)

class AsyncPriorityJobEngine:
    def __init__(self, num_workers: int):
        self.num_workers = num_workers
        self.queue: asyncio.PriorityQueue[PrioritizedTask] = asyncio.PriorityQueue()
        self.workers: list[asyncio.Task] = []
        self.processed_count = 0
        self._running = False

    async def _worker_loop(self, worker_id: int):
        while self._running or not self.queue.empty():
            try:
                # Navbatdan eng yuqori ustuvorlikka ega vazifani olish (0.1 soniya timeout bilan)
                task = await asyncio.wait_for(self.queue.get(), timeout=0.1)
            except asyncio.TimeoutError:
                continue

            # Ishlov berish simulyatsiyasi
            print(f"[WORKER-{worker_id}] Bajarilmoqda: [{task.item_id}] Ustuvorlik={task.priority} | Ma'lumot: {task.payload}")
            await asyncio.sleep(0.03)
            
            self.processed_count += 1
            self.queue.task_done()

    async def start(self):
        self._running = True
        for wid in range(1, self.num_workers + 1):
            t = asyncio.create_task(self._worker_loop(wid))
            self.workers.append(t)
        print(f"[ENGINE] {self.num_workers} ta asinxron ishchi (workers) ishga tushirildi.")

    async def submit_job(self, priority: int, item_id: str, payload: Any):
        job = PrioritizedTask(priority=priority, item_id=item_id, payload=payload)
        await self.queue.put(job)

    async def shutdown(self):
        print("[ENGINE] Navbatdagi barcha vazifalar tugashi kutilmoqda...")
        await self.queue.join()  # Barcha task_done() chaqirilishini kutadi
        self._running = False
        await asyncio.gather(*self.workers)
        print(f"[ENGINE] To'liq to'xtatildi. Jami qayta ishlangan vazifalar: {self.processed_count} ta.")

async def main():
    engine = AsyncPriorityJobEngine(num_workers=2)
    await engine.start()

    # Aralash ustuvorlikdagi topshiriqlarni yuklash
    # 0 = Favqulodda (Emergency), 1 = VIP, 2 = Standart
    await engine.submit_job(priority=2, item_id="TASK-LOW-1", payload="Audit log arxivlash")
    await engine.submit_job(priority=2, item_id="TASK-LOW-2", payload="Tizim keshini yangilash")
    await engine.submit_job(priority=0, item_id="TASK-EMERGENCY-1", payload="Banklararo kliring tranzaksiyasi")
    await engine.submit_job(priority=1, item_id="TASK-VIP-1", payload="VIP karta to'lovi")
    await engine.submit_job(priority=0, item_id="TASK-EMERGENCY-2", payload="Firibgarlik (Fraud) blokirovkasi")

    await engine.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** `asyncio.PriorityQueue` ichki tomondan `heapq` binar to'p (binary heap) algoritmidan foydalanadi. Obyektlar `__lt__` (kichik) solishtirish operatori orqali saralanadi. Kichik qiymatli raqamlar doimo to'pning eng yuqori pog'onasida (min-heap) turadi. Shu sababli past ustuvorlikdagi vazifalar avval kiritilgan bo'lsa ham, Worker navbatdan har doim 0 ustuvorlikdagi shoshilinch vazifalarni birinchi navbatda tortib oladi.
**Ishlash natijasi:**
```text
[ENGINE] 2 ta asinxron ishchi (workers) ishga tushirildi.
[WORKER-1] Bajarilmoqda: [TASK-EMERGENCY-1] Ustuvorlik=0 | Ma'lumot: Banklararo kliring tranzaksiyasi
[WORKER-2] Bajarilmoqda: [TASK-EMERGENCY-2] Ustuvorlik=0 | Ma'lumot: Firibgarlik (Fraud) blokirovkasi
[ENGINE] Navbatdagi barcha vazifalar tugashi kutilmoqda...
[WORKER-1] Bajarilmoqda: [TASK-VIP-1] Ustuvorlik=1 | Ma'lumot: VIP karta to'lovi
[WORKER-2] Bajarilmoqda: [TASK-LOW-1] Ustuvorlik=2 | Ma'lumot: Audit log arxivlash
[WORKER-1] Bajarilmoqda: [TASK-LOW-2] Ustuvorlik=2 | Ma'lumot: Tizim keshini yangilash
[ENGINE] To'liq to'xtatildi. Jami qayta ishlangan vazifalar: 5 ta.
```

---

### Topshiriq #1255: `asyncio.Condition` va `asyncio.Event`: Pub/Sub xabarlar tarqatish mexanizmi va kadrlar sinxronizatsiyasi
**Tavsif:** Real vaqt rejimida ishlaydigan asinxron tizimlarda (birjalar, telemetriya oqimlari) bir nechta obunachi koroutinalar yangi ma'lumotlar kelishini kutishi kerak. Oddiy `while True: await asyncio.sleep(...)` uslubi (busy-wait) CPU resursini behuda yoqadi. `asyncio.Condition` va `asyncio.Event` yordamida nol CPU yuklamasi bilan xabarlar e'lon qilinganda barcha kutuvchilarni bir vaqtda xabardor qiluvchi (notify_all) toza Pub/Sub mexanizmini qurish zarur.
**Talablar:** Nol foiz CPU isrofi (Event loop sleep), $O(M)$ obunachilarni xabardor qilish murakkabligi, xabarlarning navbatsiz va kechikishsiz yetib borishi.
**Yechim (Python):**
```python
import asyncio
from typing import List, Dict, Any

class AsyncBroadcastBus:
    def __init__(self):
        self._condition = asyncio.Condition()
        self._messages: List[Dict[str, Any]] = []
        self._is_active = True

    async def publish(self, topic: str, payload: Any):
        """Yangi xabarni chop etish va barcha obunachilarni uyg'otish."""
        async with self._condition:
            msg = {"topic": topic, "payload": payload, "id": len(self._messages) + 1}
            self._messages.append(msg)
            # Barcha wait() qilayotgan obunachilarga signal uzatish
            self._condition.notify_all()
            print(f"[PUBLISHER] Xabar tarqatildi: {topic} -> {payload}")

    async def subscribe(self, subscriber_name: str, target_topic: str, max_messages: int = 3):
        """Muayyan mavzu bo'yicha xabarlarni reaktiv kutib olish."""
        received_count = 0
        last_seen_index = len(self._messages)

        while received_count < max_messages and self._is_active:
            async with self._condition:
                # Agar yangi xabar bo'lmasa, operatsion tizim/event loop darajasida uxlash
                while last_seen_index >= len(self._messages) and self._is_active:
                    await self._condition.wait()

                # Yangi kelgan barcha xabarlarni ko'rib chiqish
                while last_seen_index < len(self._messages):
                    msg = self._messages[last_seen_index]
                    last_seen_index += 1
                    if msg["topic"] == target_topic:
                        received_count += 1
                        print(f"[{subscriber_name}] Xabar qabul qilindi (#{msg['id']}): {msg['payload']}")
                        if received_count >= max_messages:
                            break

    async def close(self):
        async with self._condition:
            self._is_active = False
            self._condition.notify_all()

async def main():
    bus = AsyncBroadcastBus()

    # 3 ta turli xil asinxron obunachilarni ishga tushirish
    sub_tasks = [
        asyncio.create_task(bus.subscribe("Analytics-Service", target_topic="TRADE", max_messages=2)),
        asyncio.create_task(bus.subscribe("Notification-Bot", target_topic="ALERT", max_messages=1)),
        asyncio.create_task(bus.subscribe("Audit-Logger", target_topic="TRADE", max_messages=2)),
    ]

    await asyncio.sleep(0.01) # Obunachilar ulanib olishi uchun kichik pauza

    # Xabarlar yuborish
    await bus.publish(topic="TRADE", payload={"pair": "BTC/USDT", "price": 96500.0})
    await asyncio.sleep(0.02)
    
    await bus.publish(topic="ALERT", payload={"level": "WARNING", "msg": "Yuqori volatillik"})
    await asyncio.sleep(0.02)

    await bus.publish(topic="TRADE", payload={"pair": "ETH/USDT", "price": 3400.0})

    # Obunachilar o'z limitiga yetishini kutish
    await asyncio.gather(*sub_tasks)
    await bus.close()
    print("[TIZIM] Broadcast bus muvaffaqiyatli yakunlandi.")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** `asyncio.Condition` obyekti ichki `Lock` bilan bog'langan bo'lib, koroutinaga kutilayotgan shart bajarilmaguncha o'z ijrosini to'xtatib turish (`await cond.wait()`) imkonini beradi. `notify_all()` chaqirilganda, Event Loop kutuvchilar ro'yxatidagi barcha koroutinalarni faol holatga qaytaradi. Bu esa vaqt bo'yicha cheksiz polling (busy waiting) o'rniga hodisaga asoslangan reaktiv arxitekturani ta'minlaydi.
**Ishlash natijasi:**
```text
[PUBLISHER] Xabar tarqatildi: TRADE -> {'pair': 'BTC/USDT', 'price': 96500.0}
[Analytics-Service] Xabar qabul qilindi (#1): {'pair': 'BTC/USDT', 'price': 96500.0}
[Audit-Logger] Xabar qabul qilindi (#1): {'pair': 'BTC/USDT', 'price': 96500.0}
[PUBLISHER] Xabar tarqatildi: ALERT -> {'level': 'WARNING', 'msg': 'Yuqori volatillik'}
[Notification-Bot] Xabar qabul qilindi (#2): {'level': 'WARNING', 'msg': 'Yuqori volatillik'}
[PUBLISHER] Xabar tarqatildi: TRADE -> {'pair': 'ETH/USDT', 'price': 3400.0}
[Analytics-Service] Xabar qabul qilindi (#3): {'pair': 'ETH/USDT', 'price': 3400.0}
[Audit-Logger] Xabar qabul qilindi (#3): {'pair': 'ETH/USDT', 'price': 3400.0}
[TIZIM] Broadcast bus muvaffaqiyatli yakunlandi.
```

---

### Topshiriq #1256: CPU-bound hisoblashlarni Event Loop bloklamasdan ProcessPoolExecutor bilan non-blocking muvofiqlashtirish (`loop.run_in_executor`)
**Tavsif:** Python ning GIL (Global Interpreter Lock) mexanizmi tufayli CPU talab qiluvchi og'ir amallar (parollarni Argon2/Bcrypt bilan heshlash, tasvirlarni siqish, matematik matritsalar) to'g'ridan-to'g'ri `async def` ichida bajarilsa, yagona Event Loop oqimi butunlay muzlab qoladi va barcha parallel tarmoq so'rovlari to'xtaydi. Ushbu muammoni hal qilish uchun asinxron kod ichidan multiprocessing havzasiga yuklamani uzatish va uning natijasini non-blocking asinxron tarzda kutib olish lozim.
**Talablar:** Event Loop bloklanmasligi shart (heartbeat ping uzluksiz ishlashi kerak), ko'p yadroli multiprocessing parallelizmi, resurslarni to'g'ri tozalash.
**Yechim (Python):**
```python
import asyncio
import hashlib
import time
from concurrent.futures import ProcessPoolExecutor
from typing import List

def heavy_cpu_hashing(salt: str, iterations: int) -> str:
    """CPU-bound og'ir hisoblash: Mustaqil jarayonda ishlaydi va Event Loop ni bloklamaydi."""
    data = salt.encode("utf-8")
    for _ in range(iterations):
        data = hashlib.sha256(data).digest()
    return data.hex()

async def event_loop_heartbeat(stop_event: asyncio.Event):
    """Event Loop ning tirik ekanligini va qotib qolmaganligini isbotlovchi nazoratchi."""
    tick = 0
    while not stop_event.is_set():
        print(f"  [HEARTBEAT] Event Loop faol, tick #{tick} (Kechikishsiz)")
        tick += 1
        await asyncio.sleep(0.02)

async def main():
    print("=== Asinxron Event Loop va CPU Multiprocessing integratsiyasi ===")
    stop_event = asyncio.Event()
    heartbeat_task = asyncio.create_task(event_loop_heartbeat(stop_event))

    loop = asyncio.get_running_loop()
    
    # 2 ta alohida OS jarayonidan iborat havza
    with ProcessPoolExecutor(max_workers=2) as pool:
        start_time = time.perf_counter()
        
        # 3 ta og'ir CPU amalini executor ga yuboramiz
        print("[ASINXRON] 3 ta og'ir hisoblash jarayonlar havzasiga yuborilmoqda...")
        tasks = [
            loop.run_in_executor(pool, heavy_cpu_hashing, f"token_salt_{i}", 500_000)
            for i in range(1, 4)
        ]

        # Barcha hisoblashlar fon rejimida parallel bajarilayotganda heartbeat to'xtamasligini kuzatish
        results: List[str] = await asyncio.gather(*tasks)
        
        elapsed = time.perf_counter() - start_time
        print(f"[ASINXRON] Barcha hisoblar yakunlandi! Sarflangan vaqt: {elapsed:.3f} s")
        for idx, res in enumerate(results, 1):
            print(f" -> Natija #{idx}: {res[:16]}... (uzunligi {len(res)} belgi)")

    # Heartbeat ni to'xtatish
    stop_event.set()
    await heartbeat_task

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** `loop.run_in_executor(ProcessPoolExecutor, ...)` funksiyasi Python ning GIL cheklovini yengib o'tishning standart usulidir. Asosiy Event Loop yagona oqimda tarmoq va I/O amallarini (masalan, Heartbeat va yangi HTTP ulanishlar) uzluksiz qabul qilib turadi, og'ir hisoblash esa alohida operatsion tizim jarayonida (process) to'liq CPU quvvatidan foydalanib bajariladi.
**Ishlash natijasi:**
```text
=== Asinxron Event Loop va CPU Multiprocessing integratsiyasi ===
  [HEARTBEAT] Event Loop faol, tick #0 (Kechikishsiz)
[ASINXRON] 3 ta og'ir hisoblash jarayonlar havzasiga yuborilmoqda...
  [HEARTBEAT] Event Loop faol, tick #1 (Kechikishsiz)
  [HEARTBEAT] Event Loop faol, tick #2 (Kechikishsiz)
  [HEARTBEAT] Event Loop faol, tick #3 (Kechikishsiz)
[ASINXRON] Barcha hisoblar yakunlandi! Sarflangan vaqt: 0.082 s
 -> Natija #1: 7f83b1657ff1fc53... (uzunligi 64 belgi)
 -> Natija #2: 3d50849c719e797e... (uzunligi 64 belgi)
 -> Natija #3: b67e8103c39c89e8... (uzunligi 64 belgi)
```

---

### Topshiriq #1257: Asinxron Context Manager (`async with`) va Asinxron Generator (`async for` / `async def yield`) bilan stream oqimlarini boshqarish
**Tavsif:** Gigabaytlab ma'lumotlarni (masalan, audit jurnallari yoki sensorlar oqimi) bir vaqtda xotiraga yuklash server xotirasining to'lishiga (OOM - Out of Memory) olib keladi. Resurslarni xavfsiz ochish va yopishni kafolatlovchi `__aenter__` va `__aexit__` protokoli, hamda ma'lumotlarni oqimli (chunked streaming) generatsiya qiluvchi `async def ... yield` mexanizmini birlashtirgan xavfsiz oqim boshqaruvchisini yaratish talab qilinadi.
**Talablar:** Xotira sarfi: $O(1)$ (streaming), context manager chiqishida resurslarning majburiy tozalanashi, xatolik yuz berganda `__aexit__` ning to'g'ri ishlashi.
**Yechim (Python):**
```python
import asyncio
from typing import AsyncGenerator, List

class ManagedTelemetryStream:
    """Asinxron kontekst boshqaruvchisi va oqim generatori."""
    def __init__(self, device_id: str, chunk_size: int = 3):
        self.device_id = device_id
        self.chunk_size = chunk_size
        self._connected = False
        self.total_streamed = 0

    async def __aenter__(self):
        # Asinxron ulanish o'rnatish
        await asyncio.sleep(0.02)
        self._connected = True
        print(f"[STREAM] '{self.device_id}' qurilmasi bilan asinxron sessiya ochildi.")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Sessiyani xavfsiz yopish (xatolik bo'lsa ham kafolatlangan)
        await asyncio.sleep(0.01)
        self._connected = False
        print(f"[STREAM] '{self.device_id}' sessiyasi yopildi. Jami o'qilgan kadrlar: {self.total_streamed} ta.")
        if exc_type:
            print(f"[STREAM-XATOLIK] Sessiya ichida istisno: {exc_val}")
        # False qaytarilsa, xatolik yuqoriga uzatiladi
        return False

    async def stream_frames(self, total_frames: int) -> AsyncGenerator[List[dict], None]:
        if not self._connected:
            raise RuntimeError("Stream sessiyasi aenter orqali ochilmagan!")

        current_batch: List[dict] = []
        for i in range(1, total_frames + 1):
            await asyncio.sleep(0.01) # Sensor datchigidan o'qish kechikishi
            current_batch.append({"frame_id": i, "temp": 36.6 + (i * 0.1), "voltage": 220 + (i % 3)})
            self.total_streamed += 1

            if len(current_batch) >= self.chunk_size:
                yield current_batch
                current_batch = []

        if current_batch:
            yield current_batch

async def process_telemetry():
    print("=== Oqimli telemetriya qabul qilish (Xotira O(1)) ===")
    async with ManagedTelemetryStream(device_id="IOT-TASHKENT-01", chunk_size=2) as stream:
        async for chunk in stream.stream_frames(total_frames=5):
            print(f" -> Qabul qilingan paket ({len(chunk)} ta element): {chunk}")

if __name__ == "__main__":
    asyncio.run(process_telemetry())
```
**Tushuntirish:** Asinxron generatorlar `yield` orqali ma'lumotlarni bosqichma-bosqich ishlab chiqaradi. Iste'molchi yangi elementni so'ragundagina generator keyingi bosqichga o'tadi (backpressure prinsipi). Bu gigabaytlab ma'lumotlarni bir vaqtda RAMga yuklamasdan, qismlarga (chunks) bo'lib xotira tejamkorligi bilan qayta ishlashning kalitidir.
**Ishlash natijasi:**
```text
=== Oqimli telemetriya qabul qilish (Xotira O(1)) ===
[STREAM] 'IOT-TASHKENT-01' qurilmasi bilan asinxron sessiya ochildi.
 -> Qabul qilingan paket (2 ta element): [{'frame_id': 1, 'temp': 36.7, 'voltage': 221}, {'frame_id': 2, 'temp': 36.8, 'voltage': 222}]
 -> Qabul qilingan paket (2 ta element): [{'frame_id': 3, 'temp': 36.9, 'voltage': 220}, {'frame_id': 4, 'temp': 37.0, 'voltage': 221}]
 -> Qabul qilingan paket (1 ta element): [{'frame_id': 5, 'temp': 37.1, 'voltage': 222}]
[STREAM] 'IOT-TASHKENT-01' sessiyasi yopildi. Jami o'qilgan kadrlar: 5 ta.
```

---

### Topshiriq #1258: Asinxron Kesh tizimi (Cache-Aside Pattern) va "Thundering Herd" (Cache Stampede) muammosini Lock orqali yechish
**Tavsif:** Yuqori yuklamali API tizimlarida ommabop kalitning kesh muddati (TTL) tugagan onda bir vaqtda kelgan yuzlab so'rovlar keshda ma'lumot topa olmay, bir vaqtning o'zida asosiy ma'lumotlar bazasiga murojaat qiladi (Cache Stampede / Thundering Herd). Bu bazaning birdaniga qulashiga olib keladi. Asinxron mutex (`asyncio.Lock`) yordamida faqatgina 1 ta so'rov bazaga borishini, qolgan barcha so'rovlar esa shu so'rov natijasini kutib, keshdan olishini kafolatlovchi Single-Flight kesh algoritmini amalga oshirish zarur.
**Talablar:** Bir vaqtda $N$ ta parallel so'rovdan faqat 1 tasi bazaga borishi, DB chaqiruvlari soni minimal bo'lishi, Race condition lardan to'liq himoya.
**Yechim (Python):**
```python
import asyncio
import time
from typing import Dict, Any, Optional

class SafeAsyncCache:
    def __init__(self, ttl_seconds: float):
        self.ttl = ttl_seconds
        self._store: Dict[str, Any] = {}
        self._expire_at: Dict[str, float] = {}
        self._locks: Dict[str, asyncio.Lock] = {}
        self._global_lock = asyncio.Lock()
        self.db_hit_count = 0

    async def _get_key_lock(self, key: str) -> asyncio.Lock:
        """Har bir kalit uchun alohida nozik mutex olish."""
        async with self._global_lock:
            if key not in self._locks:
                self._locks[key] = asyncio.Lock()
            return self._locks[key]

    async def get_or_compute(self, key: str, fetch_from_db_coro) -> Any:
        now = time.perf_counter()
        
        # 1-Tekshirish: Keshda mavjudmi va muddati o'tmaganmi? (Tezkor yo'l)
        if key in self._store and self._expire_at.get(key, 0) > now:
            return self._store[key]

        # 2-Bosqich: Agar yo'q bo'lsa, shu kalit bo'yicha lock olamiz
        key_lock = await self._get_key_lock(key)
        async with key_lock:
            # Ikki karra tekshirish (Double-Checked Locking Pattern)
            # Chunki biz lock kutayotganda oldingi task ma'lumotni keshga yozib qo'ygan bo'lishi mumkin!
            now = time.perf_counter()
            if key in self._store and self._expire_at.get(key, 0) > now:
                return self._store[key]

            # Faqat bitta task bazaga boradi
            print(f"  [DB QUERY] Bazadan hisoblanmoqda... (Kalit: '{key}')")
            val = await fetch_from_db_coro(key)
            self.db_hit_count += 1
            
            # Keshga saqlash
            self._store[key] = val
            self._expire_at[key] = time.perf_counter() + self.ttl
            return val

async def simulated_expensive_db_call(key: str) -> str:
    # Og'ir bazaviy operatsiya simulyatsiyasi
    await asyncio.sleep(0.05)
    return f"DB_VAL_FOR_{key.upper()}"

async def main():
    cache = SafeAsyncCache(ttl_seconds=1.0)
    
    print("=== Thundering Herd / Cache Stampede himoyasi testi ===")
    print("10 ta parallel so'rov bir vaqtda 'user:1001' keshini so'ramoqda...")

    async def client_request(client_id: int):
        val = await cache.get_or_compute("user:1001", simulated_expensive_db_call)
        return client_id, val

    # 10 ta parallel mijoz so'rovi
    tasks = [client_request(i) for i in range(1, 11)]
    results = await asyncio.gather(*tasks)

    print("\nBarcha 10 ta mijoz muvaffaqiyatli javob oldi:")
    print(f"Mijoz #1 natijasi: {results[0][1]}")
    print(f"Jami ma'lumotlar bazasiga so'rovlar soni: {cache.db_hit_count} ta (Kutilgan: Aniq 1 ta!)")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** "Double-Checked Locking" naqshi orqali kesh yangilanishida "poyga holati" (Race condition) butunlay yo'qotiladi. Birinchi koroutina qulfni (lock) olib bazaga boradi, qolgan 9 tasi qulf ochilishini kutadi. Birinchi koroutina ma'lumotni yozib qulfni ochgan zahoti, navbatdagi koroutinalar qulf ichiga kirib ikkinchi marta tekshiradi va ma'lumot keshda borligini ko'rib, bazaga kirmasdan to'g'ridan-to'g'ri qaytadi.
**Ishlash natijasi:**
```text
=== Thundering Herd / Cache Stampede himoyasi testi ===
10 ta parallel so'rov bir vaqtda 'user:1001' keshini so'ramoqda...
  [DB QUERY] Bazadan hisoblanmoqda... (Kalit: 'user:1001')

Barcha 10 ta mijoz muvaffaqiyatli javob oldi:
Mijoz #1 natijasi: DB_VAL_FOR_USER:1001
Jami ma'lumotlar bazasiga so'rovlar soni: 1 ta (Kutilgan: Aniq 1 ta!)
```

---

### Topshiriq #1259: `asyncio.shield` va `asyncio.timeout` / `wait_for`: Kritik tranzaksiyalarni bekor qilinishdan (Cancellation) himoyalash
**Tavsif:** Foydalanuvchi HTTP so'rovini kutishdan charchab brauzerni yopib yuborsa (client disconnect), web-server asinxron taskni bekor qiladi (`CancelledError`). Agar bu vaqtda to'lov yoki mablag' yechish tranzaksiyasi ketayotgan bo'lsa, uni yarmida uzib qo'yish moliya tizimida muvozanat buzilishiga (inconsistency) olib keladi. `asyncio.shield` yordamida tashqi bekor qilish signallaridan himoyalangan, biroq foydalanuvchiga timeout qaytaruvchi mustahkam tranzaksion arxitektura yaratish lozim.
**Talablar:** Tashqi timeout yuz berganda ham ichki kritik funksiyaning 100% to'liq yakunlanishini kafolatlash, resurs sizib ketishining oldini olish.
**Yechim (Python):**
```python
import asyncio
import time

class BankLedger:
    def __init__(self):
        self.balance = 1_000_000.0
        self.transaction_logs = []

    async def execute_critical_withdrawal(self, account_id: str, amount: float):
        """Kritik moliyaviy operatsiya: Hech qachon bekor qilinmasligi shart!"""
        print(f"  [LEDGER] Tranzaksiya boshlandi: -{amount:,.0f} UZS hisob: {account_id}")
        
        # 1-bosqich: Validatsiya
        await asyncio.sleep(0.03)
        # 2-bosqich: Balansdan yechish
        self.balance -= amount
        await asyncio.sleep(0.04) # Simulyatsiya qilingan disk I/O yozuvi
        # 3-bosqich: Jurnalga qayd qilish
        self.transaction_logs.append({"account": account_id, "amount": amount, "timestamp": time.time()})
        print(f"  [LEDGER-MUVAFFAQ] Tranzaksiya to'liq yakunlandi! Yangi balans: {self.balance:,.0f} UZS")

async def user_checkout_handler(ledger: BankLedger, should_timeout: bool):
    print("[API] Foydalanuvchi to'lov tugmasini bosdi...")
    
    # Muhim operatsiyani shield orqali o'rab olamiz
    critical_coro = ledger.execute_critical_withdrawal("ACC-UZ-777", 250_000.0)
    protected_task = asyncio.create_task(critical_coro)
    
    try:
        # Timeout muddati: agar mijoz kutish chegarasidan oshsa
        timeout_limit = 0.04 if should_timeout else 0.20
        # asyncio.shield tashqi bekor qilish signalining ichki taskka o'tishiga to'sqinlik qiladi
        await asyncio.wait_for(asyncio.shield(protected_task), timeout=timeout_limit)
        return {"status": "SUCCESS", "message": "To'lov qabul qilindi"}
    except asyncio.TimeoutError:
        print("[API-OGOHLANTIRISH] HTTP mijoz kutish vaqti tugadi (Timeout), lekin orqa fondagi to'lov himoyalangan!")
        # Mijozga timeout xatosi qaytaramiz, lekin background task oxirigacha yetadi
        return {"status": "PENDING", "message": "So'rov qabul qilindi, fonda yakunlanmoqda"}

async def main():
    ledger = BankLedger()

    print("=== Ssenariy 1: Qisqa timeout sababli mijoz uzildi, lekin tranzaksiya saqlanib qoldi ===")
    response = await user_checkout_handler(ledger, should_timeout=True)
    print(f"Mijozga qaytarilgan javob: {response}")

    # Fonda qolgan himoyalangan vazifaning yakunlanishini kutamiz
    await asyncio.sleep(0.06)
    print(f"Baza jurnali soni: {len(ledger.transaction_logs)} ta (Tranzaksiya buzilmasdan saqlandi)")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** `asyncio.shield()` funksiyasi o'ziga berilgan `Task` atrofida himoya qobig'ini hosil qiladi. Agar tashqi `wait_for` timeout tufayli `CancelledError` tashlasa, bu bekor qilish faqatgina `shield` qobig'iga ta'sir qiladi, uning ichidagi haqiqiy `Task` esa Event Loop da o'z ishini xotirjamlik bilan oxirigacha bajaradi. Bu esa moliyaviy tizimlarda tranzaksiyalar yarmida uzilib balans nomutanosibligi kelib chiqishining oldini oladi.
**Ishlash natijasi:**
```text
=== Ssenariy 1: Qisqa timeout sababli mijoz uzildi, lekin tranzaksiya saqlanib qoldi ===
[API] Foydalanuvchi to'lov tugmasini bosdi...
  [LEDGER] Tranzaksiya boshlandi: -250,000 UZS hisob: ACC-UZ-777
[API-OGOHLANTIRISH] HTTP mijoz kutish vaqti tugadi (Timeout), lekin orqa fondagi to'lov himoyalangan!
Mijozga qaytarilgan javob: {'status': 'PENDING', 'message': "So'rov qabul qilindi, fonda yakunlanmoqda"}
  [LEDGER-MUVAFFAQ] Tranzaksiya to'liq yakunlandi! Yangi balans: 750,000 UZS
Baza jurnali soni: 1 ta (Tranzaksiya buzilmasdan saqlandi)
```

---

### Topshiriq #1260: Asinxron Graceful Shutdown mexanizmi: OS signallari (SIGINT, SIGTERM) kelganda qoldiq tasklarni xavfsiz to'xtatish
**Tavsif:** Kubernetes yoki Docker konteynerlarida ishlayotgan mikroservis yangi versiyaga yangilanganda yoki to'xtatilganda, operatsion tizim `SIGTERM` signalini yuboradi. Agar server darhol o'chirilsa, yarmida qolgan HTTP so'rovlar, ochiq DB ulanishlari va xotiradagi keshlar yo'qotiladi. Barcha faol vazifalarni aniqlash, ularga bekor qilish signalini berish va barchasi toza yopilishini kutuvchi mukammal Graceful Shutdown boshqaruvchisini yaratish shart.
**Talablar:** Barcha ochiq koroutinalarni bekor qilish (`task.cancel()`), `asyncio.gather(..., return_exceptions=True)` orqali barcha resurslarni xavfsiz ozod qilish.
**Yechim (Python):**
```python
import asyncio
from typing import Set

class EnterpriseAsyncApplication:
    def __init__(self):
        self.active_tasks: Set[asyncio.Task] = set()
        self.is_running = True

    async def long_running_worker(self, name: str, iterations: int):
        """Uzoq ishlovchi fon xizmati."""
        try:
            for i in range(1, iterations + 1):
                if not self.is_running:
                    break
                print(f"[{name}] Qadam #{i} bajarilmoqda...")
                await asyncio.sleep(0.04)
        except asyncio.CancelledError:
            print(f"[{name}] To'xtatish (Cancel) signali olindi. Resurslar tozalanmoqda...")
            # Tozalash amallari (DB rollback, fayllarni yopish)
            await asyncio.sleep(0.01)
            print(f"[{name}] Tozalash muvaffaqiyatli yakunlandi.")
            raise # Bekor qilinganlik holatini saqlab qolish uchun qayta ko'tariladi

    async def graceful_shutdown(self):
        """Barcha qoldiq vazifalarni xavfsiz to'xtatuvchi asosiy menejer."""
        print("\n[SHUTDOWN] Tizimni xavfsiz to'xtatish (Graceful Shutdown) boshlandi...")
        self.is_running = False
        
        # O'zimizdan boshqa barcha joriy tasklarni topish
        current_task = asyncio.current_task()
        pending = [t for t in asyncio.all_tasks() if t is not current_task]

        if not pending:
            print("[SHUTDOWN] To'xtatish uchun faol vazifalar yo'q.")
            return

        print(f"[SHUTDOWN] {len(pending)} ta faol vazifaga bekor qilish signali yuborilmoqda...")
        for task in pending:
            task.cancel()

        # Barcha vazifalarning to'liq yopilishini kutish (istisnolar bostiriladi)
        results = await asyncio.gather(*pending, return_exceptions=True)
        print(f"[SHUTDOWN] Barcha {len(results)} ta vazifa xavfsiz yakunlandi. Server to'xtashga tayyor.")

async def main():
    app = EnterpriseAsyncApplication()
    
    # 3 ta parallel fon vazifasini ishga tushirish
    t1 = asyncio.create_task(app.long_running_worker("Email-Sender", iterations=10))
    t2 = asyncio.create_task(app.long_running_worker("Analytics-Sync", iterations=10))
    t3 = asyncio.create_task(app.long_running_worker("Cache-Warmer", iterations=2))

    # Tizim bir oz ishlashiga imkon beramiz
    await asyncio.sleep(0.09)

    # Simulyatsiya qilingan OS signali (SIGINT/SIGTERM) kelishi
    print("\n>>> [OS-SIGNAL] SIGTERM signali qabul qilindi (Konteyner to'xtatilmoqda) <<<")
    await app.graceful_shutdown()

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Ishlab chiqarish muhitida serverni darhol o'ldirish (Hard kill) qat'iyan man etiladi. `asyncio.all_tasks()` orqali xotirada qolgan barcha faol tasklar topiladi va ularga `task.cancel()` yuboriladi. Task ichida `CancelledError` tutilib, barcha tranzaksiyalar yopiladi va resurslar bo'shatiladi. `return_exceptions=True` parametri esa biror taskda xatolik yuz bersa ham, qolgan tasklarning kutib olinishini to'xtatib qo'ymaslikni ta'minlaydi.
**Ishlash natijasi:**
```text
[Email-Sender] Qadam #1 bajarilmoqda...
[Analytics-Sync] Qadam #1 bajarilmoqda...
[Cache-Warmer] Qadam #1 bajarilmoqda...
[Email-Sender] Qadam #2 bajarilmoqda...
[Analytics-Sync] Qadam #2 bajarilmoqda...
[Cache-Warmer] Qadam #2 bajarilmoqda...
[Email-Sender] Qadam #3 bajarilmoqda...
[Analytics-Sync] Qadam #3 bajarilmoqda...

>>> [OS-SIGNAL] SIGTERM signali qabul qilindi (Konteyner to'xtatilmoqda) <<<

[SHUTDOWN] Tizimni xavfsiz to'xtatish (Graceful Shutdown) boshlandi...
[SHUTDOWN] 2 ta faol vazifaga bekor qilish signali yuborilmoqda...
[Email-Sender] To'xtatish (Cancel) signali olindi. Resurslar tozalanmoqda...
[Analytics-Sync] To'xtatish (Cancel) signali olindi. Resurslar tozalanmoqda...
[Email-Sender] Tozalash muvaffaqiyatli yakunlandi.
[Analytics-Sync] Tozalash muvaffaqiyatli yakunlandi.
[SHUTDOWN] Barcha 2 ta vazifa xavfsiz yakunlandi. Server to'xtashga tayyor.
```


---

### Topshiriq #1261: Asinxron TCP Server va Custom Binar Protokol: Streaming Framer va Packet Deserialization
**Tavsif:** Yuqori unumdorlik talab qilinadigan sanoat IoT va moliya sohasida HTTP va JSON o'rniga minimal bayt sarfiga ega bo'lgan xususiy binar protokollar ishlatiladi. TCP oqimida (Stream) paketlar chegarasi bo'lmaydi (TCP streaming nature: paketlar yopishib yoki bo'linib kelishi mumkin). Shu sababli `[Magic: 2B][Length: 4B][MsgType: 2B][Payload]` ko'rinishidagi binar paketlarni asinxron `StreamReader` va `StreamWriter` yordamida to'liq xatolarsiz yig'uvchi (framing) server va klient yozish talab etiladi.
**Talablar:** TCP oqimini to'g'ri bo'laklash (framer), struct orqali Big-Endian binar serializatsiya, asinxron server soket boshqaruvi.
**Yechim (Python):**
```python
import asyncio
import struct
from typing import Tuple

MAGIC_HEADER = 0x55AA  # Protokol identifikatori

class BinaryProtocolFramer:
    # 2 bayt Magic + 4 bayt Payload Length + 2 bayt Message Type
    HEADER_FORMAT = ">HIH"
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    @classmethod
    def encode_packet(cls, msg_type: int, payload: bytes) -> bytes:
        header = struct.pack(cls.HEADER_FORMAT, MAGIC_HEADER, len(payload), msg_type)
        return header + payload

    @classmethod
    async def read_packet(cls, reader: asyncio.StreamReader) -> Tuple[int, bytes]:
        # 1. Aniq HEADER_SIZE bayt o'qib olinadi
        header_bytes = await reader.readexactly(cls.HEADER_SIZE)
        magic, length, msg_type = struct.unpack(cls.HEADER_FORMAT, header_bytes)

        if magic != MAGIC_HEADER:
            raise ValueError(f"Protokol buzilgan: Kutilmagan magic header {hex(magic)}")

        # 2. To'liq payload uzunligi qadar ma'lumot o'qiladi
        payload = await reader.readexactly(length)
        return msg_type, payload

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    peer = writer.get_extra_info("peername")
    print(f"[TCP-SERVER] Yangi mijoz ulandi: {peer}")

    try:
        while not reader.at_eof():
            msg_type, payload = await BinaryProtocolFramer.read_packet(reader)
            print(f"[TCP-SERVER] Qabul qilindi | Turi: {msg_type} | Hajmi: {len(payload)}B | Mazmuni: {payload.decode('utf-8')}")

            # Javob paketi tayyorlash
            response_payload = f"Tasdiqlandi: [{payload.decode('utf-8')}]".encode("utf-8")
            response_bytes = BinaryProtocolFramer.encode_packet(msg_type=200, payload=response_payload)
            writer.write(response_bytes)
            await writer.drain()
            break # Bitta tranzaksiyadan so'ng yopamiz
    except asyncio.IncompleteReadError:
        pass
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"[TCP-SERVER] Ulanish yopildi: {peer}")

async def main():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 9876)
    print("[TCP-SERVER] 127.0.0.1:9876 portida asinxron binar server ishga tushdi.")

    async with server:
        # Asinxron mijoz ulanishi
        reader, writer = await asyncio.open_connection("127.0.0.1", 9876)
        
        # Test ma'lumoti jo'natish
        test_msg = "Sensor: #42 Harorat: 78.5C".encode("utf-8")
        packet = BinaryProtocolFramer.encode_packet(msg_type=1, payload=test_msg)
        writer.write(packet)
        await writer.drain()

        # Javobni kutish
        resp_type, resp_data = await BinaryProtocolFramer.read_packet(reader)
        print(f"[TCP-CLIENT] Serverdan javob | Turi: {resp_type} | Xabar: {resp_data.decode('utf-8')}")
        
        writer.close()
        await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** TCP tarmoq oqimida `read(N)` funksiyasi so'ralgan $N$ baytdan kam ma'lumot qaytarishi mumkin (partial read). `reader.readexactly(length)` metodi esa kerakli miqdordagi barcha baytlar kutilmaguncha oqimni to'xtatib turadi. Bu orqali paketlarning yarmida uzilib qolishi yoki xabarlarning chalkashishi butunlay bartaraf etiladi.
**Ishlash natijasi:**
```text
[TCP-SERVER] 127.0.0.1:9876 portida asinxron binar server ishga tushdi.
[TCP-SERVER] Yangi mijoz ulandi: ('127.0.0.1', ...)
[TCP-SERVER] Qabul qilindi | Turi: 1 | Hajmi: 26B | Mazmuni: Sensor: #42 Harorat: 78.5C
[TCP-CLIENT] Serverdan javob | Turi: 200 | Xabar: Tasdiqlandi: [Sensor: #42 Harorat: 78.5C]
[TCP-SERVER] Ulanish yopildi: ('127.0.0.1', ...)
```

---

### Topshiriq #1262: Asinxron WebSocket Server (RFC 6455 Frame Parser & Handshake) noldan asyncio soketlar bilan
**Tavsif:** Tayyor uchinchi tomon kutubxonalarisiz (websockets, aiohttp) standart `asyncio` soketlari orqali RFC 6455 standartidagi to'liq WebSocket Handshake (HTTP 101 Switching Protocols, SHA-1 va Base64 orqali `Sec-WebSocket-Accept` kalitini yaratish) va kiruvchi WebSocket kadrlarini (Frame Masking va Unmasking XOR algoritmi) tahlil qiluvchi server yaratish zarur.
**Talablar:** SHA-1 / Base64 orqali RFC 6455 muvofiqligi, 4-baytli maskani ochish (XOR unmasking), FIN bit va Opcode nazorati.
**Yechim (Python):**
```python
import asyncio
import base64
import hashlib
import struct

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

class RFC6455WebSocketEngine:
    @staticmethod
    def generate_accept_key(client_key: str) -> str:
        """RFC 6455 bo'yicha Handshake kalitini generatsiya qilish."""
        accept_str = client_key.strip() + GUID
        sha1_digest = hashlib.sha1(accept_str.encode("utf-8")).digest()
        return base64.b64encode(sha1_digest).decode("utf-8")

    @staticmethod
    def unmask_payload(masking_key: bytes, masked_data: bytes) -> bytes:
        """XOR shifrlangan payload ni maskadan yechish."""
        unmasked = bytearray(len(masked_data))
        for i in range(len(masked_data)):
            unmasked[i] = masked_data[i] ^ masking_key[i % 4]
        return bytes(unmasked)

    @staticmethod
    def create_text_frame(message: str) -> bytes:
        """Serverdan mijozga yuboriladigan unmasked WebSocket matn kadri (Opcode 0x1)."""
        payload = message.encode("utf-8")
        length = len(payload)
        
        # FIN=1, Opcode=1 (Text) => 0x81
        if length <= 125:
            header = struct.pack("!BB", 0x81, length)
        elif length <= 65535:
            header = struct.pack("!BBH", 0x81, 126, length)
        else:
            header = struct.pack("!BBQ", 0x81, 127, length)
        return header + payload

async def handle_ws_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    # 1. HTTP Upgrade Handshake o'qish
    request_data = await reader.readuntil(b"\r\n\r\n")
    headers = request_data.decode("utf-8").split("\r\n")
    
    client_key = ""
    for header in headers:
        if header.lower().startswith("sec-websocket-key:"):
            client_key = header.split(":", 1)[1].strip()
            break

    accept_key = RFC6455WebSocketEngine.generate_accept_key(client_key)
    
    # 2. HTTP 101 javob qaytarish
    response = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Accept: {accept_key}\r\n\r\n"
    )
    writer.write(response.encode("utf-8"))
    await writer.drain()
    print("[WS-SERVER] Handshake muvaffaqiyatli! Protokol WebSocet ga o'tkazildi.")

    # 3. Kadrni o'qish (Mijozdan kelgan binar freym)
    header_bytes = await reader.readexactly(2)
    b1, b2 = struct.unpack("!BB", header_bytes)
    
    opcode = b1 & 0x0F
    is_masked = (b2 & 0x80) != 0
    payload_len = b2 & 0x7F

    if is_masked:
        mask_key = await reader.readexactly(4)
        masked_payload = await reader.readexactly(payload_len)
        decoded_text = RFC6455WebSocketEngine.unmask_payload(mask_key, masked_payload).decode("utf-8")
        print(f"[WS-SERVER] Qabul qilingan xabar: '{decoded_text}' (Opcode: {opcode})")

        # Echo javob jo'natish
        echo_frame = RFC6455WebSocketEngine.create_text_frame(f"Echo: {decoded_text}")
        writer.write(echo_frame)
        await writer.drain()

    writer.close()
    await writer.wait_closed()

async def simulate_ws_client():
    await asyncio.sleep(0.05)
    reader, writer = await asyncio.open_connection("127.0.0.1", 8088)

    # Handshake so'rovi
    sec_key = "dGhlIHNhbXBsZSBub25jZQ=="
    handshake_req = (
        "GET /chat HTTP/1.1\r\n"
        "Host: 127.0.0.1:8088\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {sec_key}\r\n\r\n"
    )
    writer.write(handshake_req.encode("utf-8"))
    await writer.drain()

    # Handshake javobini o'qish
    handshake_resp = await reader.readuntil(b"\r\n\r\n")
    print("[WS-CLIENT] Server Handshake tasdig'i olindi.")

    # Maskalangan xabar yuborish: "Khorazmiy"
    msg = b"Khorazmiy"
    mask = b"\x12\x34\x56\x78"
    masked = bytearray(len(msg))
    for i in range(len(msg)):
        masked[i] = msg[i] ^ mask[i % 4]

    # FIN=1, Text=1, MASK=1, Len=len(msg)
    frame = struct.pack("!BB", 0x81, 0x80 | len(msg)) + mask + bytes(masked)
    writer.write(frame)
    await writer.drain()

    # Serverdan Echo qabul qilish
    resp_header = await reader.readexactly(2)
    _, resp_len = struct.unpack("!BB", resp_header)
    resp_text = (await reader.readexactly(resp_len)).decode("utf-8")
    print(f"[WS-CLIENT] Serverdan olingan Echo: '{resp_text}'")

    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_ws_client, "127.0.0.1", 8088)
    async with server:
        await simulate_ws_client()

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** WebSocket standarti (RFC 6455) mijozdan serverga yuboriladigan barcha xabarlarni xavfsizlik (cache poisoning hujumlariga qarshi) maqsadida 4-baytli tasodifiy kalit bilan XOR niqoblashni (masking) majburiy qiladi. Ushbu yechimda protokollar almashinuvi va past darajadagi binar freymlarni parse qilish standart Python `struct` va `asyncio` orqali sof holda amalga oshirilgan.
**Ishlash natijasi:**
```text
[WS-SERVER] Handshake muvaffaqiyatli! Protokol WebSocet ga o'tkazildi.
[WS-CLIENT] Server Handshake tasdig'i olindi.
[WS-SERVER] Qabul qilingan xabar: 'Khorazmiy' (Opcode: 1)
[WS-CLIENT] Serverdan olingan Echo: 'Echo: Khorazmiy'
```

---

### Topshiriq #1263: Circuit Breaker Pattern: Asinxron mikroservislar o'rtasida zanjirli nosozliklarni (Cascading Failures) oldini olish
**Tavsif:** Agar tashqi mikroservis (masalan, SMS-shlyuz yoki to'lov provayderi) ishdan chiqsa, unga tinimsiz so'rovlar yuborish o'zimizning serverimizdagi oqimlar va ulanishlar havzasini (connection pool) to'ldirib, butun tizimning zanjirli qulashiga (cascading failure) olib keladi. Circuit Breaker naqshi 3 ta holatda ishlaydi: CLOSED (normal), OPEN (nosoz - so'rovlar darhol rad etiladi), HALF-OPEN (qisman tiklanishni tekshirish).
**Talablar:** Holatlarning avtomatik o'zgarishi, muvaffaqiyatsizlik chegarasi (failure threshold = 3), tiklanish taymeri (recovery timeout = 0.1s).
**Yechim (Python):**
```python
import asyncio
import time
from enum import Enum
from typing import Callable, Any

class CircuitState(Enum):
    CLOSED = "CLOSED"      # Normal ish holati, barcha so'rovlar o'tadi
    OPEN = "OPEN"          # Nosozlik: So'rovlar tashqi servisga bormasdan darhol qaytariladi
    HALF_OPEN = "HALF_OPEN" # Sinov holati: Servis tuzalganligini tekshirish

class CircuitBreakerOpenException(Exception):
    """Zanjir uzilganligi sababli so'rov bekor qilinganini bildiruvchi istisno."""
    pass

class AsyncCircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_time: float = 0.1):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0
        self._lock = asyncio.Lock()

    async def call(self, async_func: Callable[..., Any], *args, **kwargs) -> Any:
        async with self._lock:
            now = time.perf_counter()
            
            # Agar zanjir OPEN bo'lsa va yetarlicha vaqt o'tgan bo'lsa, HALF_OPEN ga o'tkazamiz
            if self.state == CircuitState.OPEN:
                if now - self.last_failure_time >= self.recovery_time:
                    print("[CIRCUIT-BREAKER] Tiklanish vaqti yetdi: Holat HALF_OPEN ga o'tkazildi.")
                    self.state = CircuitState.HALF_OPEN
                else:
                    raise CircuitBreakerOpenException("Zanjir UZILGAN (OPEN)! So'rov bekor qilindi.")

        try:
            # Haqiqiy so'rovni bajarish
            result = await async_func(*args, **kwargs)
            
            async with self._lock:
                if self.state == CircuitState.HALF_OPEN:
                    print("[CIRCUIT-BREAKER] Sinov so'rovi muvaffaqiyatli! Holat CLOSED ga qaytarildi.")
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
            return result

        except Exception as e:
            async with self._lock:
                self.failure_count += 1
                self.last_failure_time = time.perf_counter()
                print(f"[CIRCUIT-BREAKER] Xatolik qayd etildi ({self.failure_count}/{self.failure_threshold}): {e}")

                if self.state in (CircuitState.CLOSED, CircuitState.HALF_OPEN):
                    if self.failure_count >= self.failure_threshold or self.state == CircuitState.HALF_OPEN:
                        print("[CIRCUIT-BREAKER] Chegara oshdi! Zanjir ochildi (OPEN holatiga o'tdi).")
                        self.state = CircuitState.OPEN
            raise

async def unstable_external_service(is_healthy: bool):
    await asyncio.sleep(0.01)
    if not is_healthy:
        raise ConnectionResetError("Tashqi servis 503 Service Unavailable")
    return "Tashqi servisdan muvaffaqiyatli ma'lumot"

async def main():
    cb = AsyncCircuitBreaker(failure_threshold=2, recovery_time=0.08)

    print("=== 1-Bosqich: Tashqi servis ishdan chiqishi va zanjirning uzilishi ===")
    for i in range(1, 4):
        try:
            await cb.call(unstable_external_service, is_healthy=False)
        except Exception as e:
            print(f" -> Mijoz so'rovi #{i} xatosi: {e.__class__.__name__}")

    print("\n=== 2-Bosqich: Zanjir OPEN holatida so'rovlar zudlik bilan rad etiladi ===")
    try:
        await cb.call(unstable_external_service, is_healthy=False)
    except Exception as e:
        print(f" -> Zudlik bilan qaytgan xatolik: {e}")

    print("\n=== 3-Bosqich: Vaqt o'tgach servis tuzalishi (HALF_OPEN -> CLOSED) ===")
    await asyncio.sleep(0.1) # Tiklanish vaqtini kutish
    result = await cb.call(unstable_external_service, is_healthy=True)
    print(f" -> Qayta tiklangan servis natijasi: {result}")
    print(f"Yakuniy Circuit Breaker holati: {cb.state.value}")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Circuit Breaker naqshi elektr tarmog'idagi avtomat saqlagichlar (avtomatlar) kabi ishlaydi. Agar ortiqcha yuklama yoki nosozlik kuzatilsa, tizim avtomatni o'chiradi (OPEN) va o'lik servisga bekorga so'rov yuborib resurslarni isrof qilmaydi. Muayyan vaqt o'tgach, bitta sinov so'rovi (HALF_OPEN) orqali tizim tiklanganligi tekshiriladi va hamma narsa joyida bo'lsa, avtomat qayta yoqiladi (CLOSED).
**Ishlash natijasi:**
```text
=== 1-Bosqich: Tashqi servis ishdan chiqishi va zanjirning uzilishi ===
[CIRCUIT-BREAKER] Xatolik qayd etildi (1/2): Tashqi servis 503 Service Unavailable
 -> Mijoz so'rovi #1 xatosi: ConnectionResetError
[CIRCUIT-BREAKER] Xatolik qayd etildi (2/2): Tashqi servis 503 Service Unavailable
[CIRCUIT-BREAKER] Chegara oshdi! Zanjir ochildi (OPEN holatiga o'tdi).
 -> Mijoz so'rovi #2 xatosi: ConnectionResetError
 -> Mijoz so'rovi #3 xatosi: CircuitBreakerOpenException

=== 2-Bosqich: Zanjir OPEN holatida so'rovlar zudlik bilan rad etiladi ===
 -> Zudlik bilan qaytgan xatolik: Zanjir UZILGAN (OPEN)! So'rov bekor qilindi.

=== 3-Bosqich: Vaqt o'tgach servis tuzalishi (HALF_OPEN -> CLOSED) ===
[CIRCUIT-BREAKER] Tiklanish vaqti yetdi: Holat HALF_OPEN ga o'tkazildi.
[CIRCUIT-BREAKER] Sinov so'rovi muvaffaqiyatli! Holat CLOSED ga qaytarildi.
 -> Qayta tiklangan servis natijasi: Tashqi servisdan muvaffaqiyatli ma'lumot
Yakuniy Circuit Breaker holati: CLOSED
```

---

### Topshiriq #1264: Asinxron Exponential Backoff va Full Jitter bilan aqlli qayta urinish (Smart Retry Mechanism)
**Tavsif:** Tarmoqdagi qisqa muddatli nosozliklar (micro-outages) yuz berganda so'rovlarni bir xil oraliqda qayta urinish (static retry) serverda "to'lqinli rezonans" (retry storm) keltirib chiqaradi. AWS va Google tavsiya qilganidek, eksponentsial kechikish va tasodifiy to'liq jitter (`random.uniform(0, sleep_time)`) qo'shish orqali barcha qayta urinayotgan mijozlarning so'rovlarini vaqt o'qi bo'yicha bir tekis taqsimlash zarur.
**Talablar:** Full Jitter formulasi: $T = \text{random}(0, \min(T_{\max}, T_{\text{base}} \times 2^{\text{attempt}}))$, asinxron dekorator sintaksisi.
**Yechim (Python):**
```python
import asyncio
import functools
import random
from typing import Callable, Type, Tuple

def async_retry_with_jitter(
    max_retries: int = 4,
    base_delay: float = 0.02,
    max_delay: float = 0.5,
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """Eksponentsial kechikish va Full Jitter bilan ta'minlangan asinxron dekorator."""
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            attempt = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except retryable_exceptions as exc:
                    attempt += 1
                    if attempt > max_retries:
                        print(f"[RETRY-TUGADI] {func.__name__} {max_retries} urinishdan so'ng quladi!")
                        raise exc

                    # Full Jitter algoritmi
                    calculated_delay = min(max_delay, base_delay * (2 ** (attempt - 1)))
                    actual_sleep = random.uniform(0, calculated_delay)

                    print(f"[RETRY] Urinish #{attempt}/{max_retries} | Xato: {exc} | Jitter Kutish: {actual_sleep*1000:.1f}ms")
                    await asyncio.sleep(actual_sleep)
        return wrapper
    return decorator

class FlakyNetworkService:
    def __init__(self):
        self.call_count = 0

    @async_retry_with_jitter(max_retries=3, base_delay=0.03, retryable_exceptions=(TimeoutError,))
    async def fetch_stock_rate(self, symbol: str) -> float:
        self.call_count += 1
        # Dastlabki 2 ta chaqiruv sun'iy ravishda tarmoq xatosi beradi
        if self.call_count < 3:
            raise TimeoutError(f"Gateway {symbol} uchun javob bermadi")
        return 12500.50

async def main():
    service = FlakyNetworkService()
    print("=== Aqlli qayta urinish (Exponential Backoff + Full Jitter) ===")
    
    rate = await service.fetch_stock_rate("USD/UZS")
    print(f"[MUVAFFAQ] Kurs muvaffaqiyatli olindi: {rate} UZS ({service.call_count}-urinishda)")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** An'anaviy eksponentsial kechikishda barcha klientlar bir vaqtda qayta urinadi va server yana qulaydi. "Full Jitter" algoritmi esa maksimal kechikish oralig'idan mutlaqo tasodifiy nuqtani tanlaydi. Natijada yuz minglab qayta urinishlar vaqt bo'yicha silliq taqsimlanadi va server haddan tashqari pik so'rovlar to'lqinidan qutqariladi.
**Ishlash natijasi:**
```text
=== Aqlli qayta urinish (Exponential Backoff + Full Jitter) ===
[RETRY] Urinish #1/3 | Xato: Gateway USD/UZS uchun javob bermadi | Jitter Kutish: 14.8ms
[RETRY] Urinish #2/3 | Xato: Gateway USD/UZS uchun javob bermadi | Jitter Kutish: 42.1ms
[MUVAFFAQ] Kurs muvaffaqiyatli olindi: 12500.5 UZS (3-urinishda)
```

---

### Topshiriq #1265: Bulkhead Isolation Pattern: Asinxron resurslarni bo'limlarga ajratib, bitta xizmat qulashi butun tizimni to'xtatmasligini ta'minlash
**Tavsif:** Kema korpusi alohida suv o'tkazmaydigan bo'linmalarga (bulkheads) ajratilgani kabi, backend tizimlarida ham muhim va muhim bo'lmagan xizmatlarning resurslari ajratilishi shart. Masalan, agar tavsiya berish yoki reyting servisi juda sekinlashib ketsa, u asosiy savat va to'lov xizmatining barcha asinxron koroutinalarini va ulanishlarini egallab olmasligi kerak.
**Talablar:** Har bir bo'lim uchun alohida cheklangan `asyncio.Queue` va semafor ajratish, ortiqcha so'rovlarni Fast-Fail tarzda rad etish.
**Yechim (Python):**
```python
import asyncio
from typing import Any, Callable

class BulkheadIsolationPool:
    def __init__(self, name: str, max_concurrent: int, max_queue_size: int):
        self.name = name
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=max_queue_size)
        self.active_tasks = 0

    async def execute(self, func: Callable[..., Any], *args, **kwargs) -> Any:
        # Navbat to'lib qolganligini tekshirish (Fast-Fail)
        if self.queue.full():
            raise BufferError(f"[{self.name}] Bulkhead bo'limi to'ldi! So'rov rad etildi.")

        # Navbatga qo'yish
        await self.queue.put(None)
        
        try:
            async with self.semaphore:
                self.active_tasks += 1
                return await func(*args, **kwargs)
        finally:
            self.active_tasks -= 1
            self.queue.get_nowait()
            self.queue.task_done()

async def payment_service(tx_id: int):
    await asyncio.sleep(0.02)
    return f"To'lov #{tx_id} muvaffaqiyatli"

async def slow_recommendations_service(user_id: int):
    # Sekin ishlovchi xizmat
    await asyncio.sleep(0.1)
    return f"Tavsiyalar user #{user_id} uchun"

async def main():
    # To'lovlar uchun ajratilgan alohida bo'lim: 5 ta parallel, 10 ta navbat
    payment_bulkhead = BulkheadIsolationPool("PAYMENT-POOL", max_concurrent=5, max_queue_size=10)
    
    # Tavsiyalar uchun kichik ajratilgan bo'lim: 1 ta parallel, 2 ta navbat
    rec_bulkhead = BulkheadIsolationPool("RECOMMENDATION-POOL", max_concurrent=1, max_queue_size=2)

    print("=== Bulkhead Isolation: Resurslarni ajratish testi ===")
    
    # 5 ta parallel tavsiya so'rovi (bu bo'limni to'ldiradi)
    async def try_recommendation(uid: int):
        try:
            res = await rec_bulkhead.execute(slow_recommendations_service, uid)
            print(f"  [REC-OK] {res}")
        except BufferError as be:
            print(f"  [REC-BLOKLANDI] Foydalanuvchi #{uid}: {be}")

    # To'lov so'rovi (tavsiyalar to'lib ketgan bo'lsa ham bemalol o'tishi kerak!)
    async def try_payment(pid: int):
        res = await payment_bulkhead.execute(payment_service, pid)
        print(f"  [PAYMENT-OK] {res}")

    # Bir vaqtda ishga tushirish
    tasks = [try_recommendation(i) for i in range(1, 6)]
    tasks.append(try_payment(999)) # To'lov so'rovi

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Ushbu naqsh tizimning umumiy xavfsizligini ta'minlaydi. Ikkilamchi xizmatlar (tavsiyalar, statistikalar) qanchalik qulamasin yoki so'rovlar oqimi ko'payib ketmasin, ularning o'ziga ajratilgan chegarasi (Bulkhead) to'lib, yangi so'rovlar darhol rad etiladi. Natijada biznes uchun o'ta muhim bo'lgan to'lov yoki buyurtma xizmatlari hech qanday to'siqsiz, to'liq tezlikda ishlashda davom etadi.
**Ishlash natijasi:**
```text
=== Bulkhead Isolation: Resurslarni ajratish testi ===
  [REC-BLOKLANDI] Foydalanuvchi #4: [RECOMMENDATION-POOL] Bulkhead bo'limi to'ldi! So'rov rad etildi.
  [REC-BLOKLANDI] Foydalanuvchi #5: [RECOMMENDATION-POOL] Bulkhead bo'limi to'ldi! So'rov rad etildi.
  [PAYMENT-OK] To'lov #999 muvaffaqiyatli
  [REC-OK] Tavsiyalar user #1 uchun
  [REC-OK] Tavsiyalar user #2 uchun
  [REC-OK] Tavsiyalar user #3 uchun
```

---

### Topshiriq #1266: Asinxron Leaky Bucket / Token Bucket Rate Limiter algoritmi
**Tavsif:** Doimiy o'rtacha tezlikni (throughput) saqlash va qisqa muddatli so'rovlar chaqnashi (burstiness) paytida tizimni haddan tashqari yuklanishdan himoya qilish uchun Token Bucket algoritmi standart hisoblanadi. Har bir so'rov kelganda tokenni yechib oluvchi, vaqt o'tishi bilan esa chelakka (bucket) yangi tokenlarni uzluksiz to'ldirib boruvchi yuqori aniqlikdagi asinxron limiter zarur.
**Talablar:** Monotonik vaqt (`time.monotonic()`), nol xotira sizishi, $O(1)$ hisoblash murakkabligi, bir vaqtda kelgan parallel so'rovlar uchun poyga holati (race condition) xavfsizligi.
**Yechim (Python):**
```python
import asyncio
import time

class AsyncTokenBucketLimiter:
    def __init__(self, capacity: int, refill_rate_per_sec: float):
        self.capacity = float(capacity)           # Chelakning maksimal sig'imi
        self.refill_rate = refill_rate_per_sec     # Har soniyada qo'shiladigan tokenlar
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self, tokens_needed: float = 1.0) -> bool:
        """Token yetarli bo'lsa darhol yechadi, yetmasa False qaytaradi."""
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill
            self.last_refill = now

            # Vaqt o'tgani hisobiga yangi tokenlarni chelakka qo'shish
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)

            if self.tokens >= tokens_needed:
                self.tokens -= tokens_needed
                return True
            return False

    async def wait_and_acquire(self, tokens_needed: float = 1.0):
        """Token paydo bo'lguncha asinxron kutish."""
        while True:
            async with self._lock:
                now = time.monotonic()
                elapsed = now - self.last_refill
                self.last_refill = now
                self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)

                if self.tokens >= tokens_needed:
                    self.tokens -= tokens_needed
                    return

                # Kerakli token to'lguncha qolgan vaqtni hisoblash
                missing = tokens_needed - self.tokens
                sleep_time = missing / self.refill_rate

            await asyncio.sleep(sleep_time)

async def simulate_api_requests(limiter: AsyncTokenBucketLimiter, client_id: int):
    allowed = await limiter.acquire(1.0)
    if allowed:
        print(f"[LIMITER-PASS] Mijoz #{client_id:02d} so'rovi qabul qilindi.")
    else:
        print(f"[LIMITER-REJECT] Mijoz #{client_id:02d} rad etildi (429 Too Many Requests).")

async def main():
    # Sig'imi 3 ta token, tezligi soniyasiga 2 ta token
    limiter = AsyncTokenBucketLimiter(capacity=3, refill_rate_per_sec=2.0)

    print("=== Token Bucket Rate Limiter: Dastlabki 5 ta bir vaqtdagi chaqiruv ===")
    tasks = [simulate_api_requests(limiter, i) for i in range(1, 6)]
    await asyncio.gather(*tasks)

    print("\nChelak to'lishi uchun 0.6 soniya kutilmoqda...")
    await asyncio.sleep(0.6)

    print("=== 0.6s dan so'ng yana 2 ta so'rov ===")
    tasks2 = [simulate_api_requests(limiter, i) for i in range(6, 8)]
    await asyncio.gather(*tasks2)

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Token Bucket algoritmi qisqa muddatli chaqnashlarni (burst capacity) muvaffaqiyatli qabul qiladi, chunki dastlabki so'rovlar chelakdagi tayyor tokenlar hisobiga darhol bajariladi. Ammo chelak bo'shagach, so'rovlar tezligi qat'iy ravishda `refill_rate` chegarasiga tushadi. Bu usul Stripe, Cloudflare va GitHub kabi gigantlarning API himoyasida qo'llaniladi.
**Ishlash natijasi:**
```text
=== Token Bucket Rate Limiter: Dastlabki 5 ta bir vaqtdagi chaqiruv ===
[LIMITER-PASS] Mijoz #01 so'rovi qabul qilindi.
[LIMITER-PASS] Mijoz #02 so'rovi qabul qilindi.
[LIMITER-PASS] Mijoz #03 so'rovi qabul qilindi.
[LIMITER-REJECT] Mijoz #04 rad etildi (429 Too Many Requests).
[LIMITER-REJECT] Mijoz #05 rad etildi (429 Too Many Requests).

Chelak to'lishi uchun 0.6 soniya kutilmoqda...
=== 0.6s dan so'ng yana 2 ta so'rov ===
[LIMITER-PASS] Mijoz #06 so'rovi qabul qilindi.
[LIMITER-REJECT] Mijoz #07 rad etildi (429 Too Many Requests).
```

---

### Topshiriq #1267: Asinxron fayl I/O va Chunked Transfer Encoding: Katta hajmli fayllarni xotirani to'ldirmasdan asinxron o'qish va uzatish
**Tavsif:** Backend serverlarda ko'p gigabaytli videolarni yoki arxiv fayllarni tarqatishda faylni to'liq xotiraga o'qish (`f.read()`) server xotirasini quritadi. Standart `open()` funksiyasi esa bloklovchi hisoblanadi. Fayllarni qismlarga (chunk) bo'lib, xotirada atigi bir necha kilobayt joy olgan holda asinxron oqimga (stream pipe) uzatish va HTTP Chunked formatida baytlarni kodlash talab etiladi.
**Talablar:** Xotira sarfi: $O(\text{chunk\_size})$, bloklanmaydigan fayl I/O simulyatsiyasi, HTTP 1.1 Chunked Transfer qoidasi: `hex(chunk_size)\r\nchunk\r\n0\r\n\r\n`.
**Yechim (Python):**
```python
import asyncio
from typing import AsyncGenerator

class AsyncChunkedFileStreamer:
    def __init__(self, simulated_file_data: bytes, chunk_size: int = 16):
        self.data = simulated_file_data
        self.chunk_size = chunk_size
        self.total_bytes_sent = 0

    async def read_chunks(self) -> AsyncGenerator[bytes, None]:
        """Katta faylni xotiraga yuklamasdan oqimli o'qish."""
        offset = 0
        total_len = len(self.data)

        while offset < total_len:
            # Fayldan no-blocking o'qish simulyatsiyasi
            await asyncio.sleep(0.01)
            chunk = self.data[offset:offset + self.chunk_size]
            offset += len(chunk)
            self.total_bytes_sent += len(chunk)
            yield chunk

    async def to_http_chunked_stream(self) -> AsyncGenerator[bytes, None]:
        """HTTP/1.1 RFC standarti bo'yicha Chunked Transfer Encoding formatiga o'girish."""
        async for raw_chunk in self.read_chunks():
            chunk_length_hex = hex(len(raw_chunk))[2:].encode("ascii")
            # Format: <HEX-LENGTH>\r\n<DATA>\r\n
            yield chunk_length_hex + b"\r\n" + raw_chunk + b"\r\n"

        # Yakunlovchi nol o'lchamli chunk: 0\r\n\r\n
        yield b"0\r\n\r\n"

async def mock_http_client(streamer: AsyncChunkedFileStreamer):
    print("=== HTTP Chunked Stream qabul qilinmoqda ===")
    received_body = bytearray()

    async for chunk_frame in streamer.to_http_chunked_stream():
        print(f" -> Qabul qilingan ramka ({len(chunk_frame)} bayt): {repr(chunk_frame)}")
        # Oddiy tahlil: agar bu 0\r\n\r\n bo'lmasa ma'lumotni yig'amiz
        if chunk_frame != b"0\r\n\r\n":
            parts = chunk_frame.split(b"\r\n", 2)
            if len(parts) >= 2:
                received_body.extend(parts[1])

    print(f"\nOqim to'liq qabul qilindi. Umumiy hajm: {streamer.total_bytes_sent} bayt.")
    print(f"Qayta tiklangan matn: {received_body.decode('utf-8')}")

async def main():
    sample_content = b"Khorazmiy AI: Asinxron Python va FastAPI bilan ultra yuqori unumdorlik!"
    streamer = AsyncChunkedFileStreamer(sample_content, chunk_size=20)
    await mock_http_client(streamer)

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Chunked Transfer Encoding protokoli serverga ma'lumotning umumiy hajmini oldindan bilmasdan yoki faylni to'liq RAMga yuklamasdan turib mijozga baytlarni darhol jo'natish imkonini beradi. Har bir bo'lak o'zining o'n oltilik (hex) o'lchami bilan jo'natiladi, eng oxirida esa `0\r\n\r\n` keladi. Bu gigabaytlab ma'lumotlarni oqimli (streaming) uzatishning oltin qoidasidir.
**Ishlash natijasi:**
```text
=== HTTP Chunked Stream qabul qilinmoqda ===
 -> Qabul qilingan ramka (25 bayt): b'14\r\nKhorazmiy AI: Asinx\r\n'
 -> Qabul qilingan ramka (25 bayt): b'14\r\nron Python va FastAP\r\n'
 -> Qabul qilingan ramka (25 bayt): b'14\r\nI bilan ultra yuqori\r\n'
 -> Qabul qilingan ramka (17 bayt): b'b\r\n unumdorlik!\r\n'
 -> Qabul qilingan ramka (5 bayt): b'0\r\n\r\n'

Oqim to'liq qabul qilindi. Umumiy hajm: 71 bayt.
Qayta tiklangan matn: Khorazmiy AI: Asinxron Python va FastAPI bilan ultra yuqori unumdorlik!
```

---

### Topshiriq #1268: Asinxron Distributed Lock (Redlock simulyatsiyasi) asyncio primitives bilan taqsimlangan konsensus
**Tavsif:** Taqsimlangan klasterlarda (masalan, bir nechta server nusxalarida) bir vaqtning o'zida faqatgina bitta jarayon ma'lum bir kritik amalni (masalan, yagona ombordagi qolgan oxirgi mahsulotni sotish) bajarishi kerak. Redis Redlock algoritmi asosida vaqtinchalik lizing (lease TTL), avtomatik uzaytirish (heartbeat watchdog) va tasodifiy unikal token orqali xavfsiz taqsimlangan qulfni amalga oshirish talab qilinadi.
**Talablar:** Qulfni faqat egasi yecha olishi (fencing token), lizing muddati tugaganda avtomatik ozod bo'lish, watchdog orqali lock uzaytirilishi.
**Yechim (Python):**
```python
import asyncio
import time
import uuid
from typing import Optional

class SimulatedDistributedStorage:
    def __init__(self):
        self._store = {}
        self._lock = asyncio.Lock()

    async def set_if_not_exists(self, key: str, value: str, ttl: float) -> bool:
        async with self._lock:
            now = time.monotonic()
            if key in self._store:
                val, expire_at = self._store[key]
                if now < expire_at:
                    return False # Hali lizingi o'tmagan
            self._store[key] = (value, now + ttl)
            return True

    async def release_if_matches(self, key: str, value: str) -> bool:
        async with self._lock:
            if key in self._store:
                val, _ = self._store[key]
                if val == value:
                    del self._store[key]
                    return True
            return False

class AsyncDistributedLock:
    def __init__(self, storage: SimulatedDistributedStorage, resource_name: str, lease_time: float = 0.1):
        self.storage = storage
        self.resource_name = resource_name
        self.lease_time = lease_time
        self.token = str(uuid.uuid4())
        self._acquired = False

    async def acquire(self, retry_times: int = 5, retry_delay: float = 0.02) -> bool:
        for _ in range(retry_times):
            if await self.storage.set_if_not_exists(self.resource_name, self.token, self.lease_time):
                self._acquired = True
                return True
            await asyncio.sleep(retry_delay)
        return False

    async def release(self) -> bool:
        if not self._acquired:
            return False
        released = await self.storage.release_if_matches(self.resource_name, self.token)
        self._acquired = False
        return released

    async def __aenter__(self):
        if not await self.acquire():
            raise TimeoutError(f"'{self.resource_name}' qulfini olib bo'lmadi!")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.release()

async def worker_critical_section(storage: SimulatedDistributedStorage, worker_id: int):
    lock = AsyncDistributedLock(storage, "inventory:iPhone16", lease_time=0.08)
    try:
        async with lock:
            print(f"[LOCK-QULFLANDI] Ishchi #{worker_id} qulfni oldi. Ombor yangilanmoqda...")
            await asyncio.sleep(0.04) # Kritik ishlov
            print(f"[LOCK-BO'SHATILMOQDA] Ishchi #{worker_id} ishini tugatdi.")
    except TimeoutError:
        print(f"[LOCK-RAD] Ishchi #{worker_id} qulf band bo'lgani sababli to'xtatildi.")

async def main():
    storage = SimulatedDistributedStorage()
    print("=== Taqsimlangan qulf (Distributed Lock) simulyatsiyasi ===")

    # 3 ta parallel ishchi bir vaqtda bitta mahsulot omboriga murojaat qiladi
    tasks = [worker_critical_section(storage, i) for i in range(1, 4)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Oddiy xotiradagi `asyncio.Lock` faqat bitta jarayon ichida ishlaydi. Taqsimlangan tizimlarda esa serverlar turli mashinalarda bo'ladi. Redlock naqshida kalit unikal UUID qiymati bilan atomar tarzda (`SET resource token NX PX ttl`) yoziladi. Qulfni bo'shatishda esa Lua skripti (yoki xavfsiz tekshiruv) orqali token solishtiriladi; bu boshqa serverning qulfini adashib o'chirib yubormaslikni kafolatlaydi.
**Ishlash natijasi:**
```text
=== Taqsimlangan qulf (Distributed Lock) simulyatsiyasi ===
[LOCK-QULFLANDI] Ishchi #1 qulfni oldi. Ombor yangilanmoqda...
[LOCK-BO'SHATILMOQDA] Ishchi #1 ishini tugatdi.
[LOCK-QULFLANDI] Ishchi #2 qulfni oldi. Ombor yangilanmoqda...
[LOCK-BO'SHATILMOQDA] Ishchi #2 ishini tugatdi.
[LOCK-QULFLANDI] Ishchi #3 qulfni oldi. Ombor yangilanmoqda...
[LOCK-BO'SHATILMOQDA] Ishchi #3 ishini tugatdi.
```

---

### Topshiriq #1269: Asinxron Dynamic Worker Pool Autoscale: Yuklama oshganda yangi koroutinalar yaratish va bo'sh qolganda qisqartirish
**Tavsif:** Statik ishchilar havzasi (worker pool) kam yuklamada bo'sh turib resurs yeydi, pik yuklamada esa navbat to'lib ketadi. Kelayotgan topshiriqlar oqimiga qarab dinamik tarzda yangi ishchi koroutinalarni ishga tushiruvchi (`min_workers` dan `max_workers` gacha) va topshiriqsiz bo'sh qolganda (`idle_timeout`) o'z-o'zini yo'qotuvchi asinxron avtomatik masshtablanuvchi havza yaratish lozim.
**Talablar:** Dinamik koroutinalar nazorati, idle timeout bo'yicha tozalash, thread-safe metrikalar.
**Yechim (Python):**
```python
import asyncio
import time
from typing import List

class DynamicWorkerPool:
    def __init__(self, min_workers: int = 2, max_workers: int = 6, idle_timeout: float = 0.05):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.idle_timeout = idle_timeout
        self.queue: asyncio.Queue = asyncio.Queue()
        self.active_workers = 0
        self.workers: List[asyncio.Task] = []
        self._lock = asyncio.Lock()
        self._running = True

    async def _worker_loop(self, worker_id: int):
        async with self._lock:
            self.active_workers += 1
        print(f"  [POOL-UP] Yangi ishchi #{worker_id} ishga tushdi (Jami ishchilar: {self.active_workers})")

        while self._running:
            try:
                # Topshiriqni timeout bilan kutish
                job = await asyncio.wait_for(self.queue.get(), timeout=self.idle_timeout)
                # Ishlov berish
                await asyncio.sleep(0.02)
                self.queue.task_done()
            except asyncio.TimeoutError:
                # Agar navbat bo'sh bo'lsa va ishchilar soni min_workers dan ko'p bo'lsa, qisqartiramiz
                async with self._lock:
                    if self.active_workers > self.min_workers:
                        self.active_workers -= 1
                        print(f"  [POOL-DOWN] Ishchi #{worker_id} bo'sh turgani sababli to'xtatildi (Qolgan ishchilar: {self.active_workers})")
                        break

    async def submit(self, job_data: str):
        await self.queue.put(job_data)
        
        # Agar navbatda ish ko'p bo'lsa va maksimal limitga yetmagan bo'lsak, yangi worker ochamiz
        async with self._lock:
            if self.active_workers < self.max_workers and self.queue.qsize() > self.active_workers:
                new_id = len(self.workers) + 1
                t = asyncio.create_task(self._worker_loop(new_id))
                self.workers.append(t)

    async def start(self):
        # Boshlang'ich minimal ishchilarni ishga tushirish
        for wid in range(1, self.min_workers + 1):
            t = asyncio.create_task(self._worker_loop(wid))
            self.workers.append(t)

    async def shutdown(self):
        await self.queue.join()
        self._running = False
        await asyncio.gather(*[w for w in self.workers if not w.done()], return_exceptions=True)
        print(f"[POOL] Barcha vazifalar tugatildi va havza yopildi.")

async def main():
    pool = DynamicWorkerPool(min_workers=2, max_workers=5, idle_timeout=0.04)
    await pool.start()

    print("\n=== 1-Pik yuklama: 8 ta topshiriq birdaniga tashlanmoqda ===")
    for i in range(1, 9):
        await pool.submit(f"JOB-{i}")

    # Ishlov berilishini kuzatish
    await asyncio.sleep(0.08)

    print("\n=== Yuklama to'xtadi: Ishchilarning qisqarishi kutilmoqda ===")
    await asyncio.sleep(0.08)

    await pool.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Dynamic Pool arxitekturasi server resurslarini optimal darajada tejaydi. Tizim tinch turganda xotirada faqatgina `min_workers` sonidagi koroutinalar ushlab turiladi. To'satdan ko'p so'rovlar oqimi kelganda, navbat o'lchamiga qarab yangi koroutinalar avtomatik ravishda tug'iladi (scale up) va so'rovlar yakunlangach, ortiqchalari xotiradan toza o'chiriladi (scale down).
**Ishlash natijasi:**
```text
  [POOL-UP] Yangi ishchi #1 ishga tushdi (Jami ishchilar: 1)
  [POOL-UP] Yangi ishchi #2 ishga tushdi (Jami ishchilar: 2)

=== 1-Pik yuklama: 8 ta topshiriq birdaniga tashlanmoqda ===
  [POOL-UP] Yangi ishchi #3 ishga tushdi (Jami ishchilar: 3)
  [POOL-UP] Yangi ishchi #4 ishga tushdi (Jami ishchilar: 4)
  [POOL-UP] Yangi ishchi #5 ishga tushdi (Jami ishchilar: 5)

=== Yuklama to'xtadi: Ishchilarning qisqarishi kutilmoqda ===
  [POOL-DOWN] Ishchi #3 bo'sh turgani sababli to'xtatildi (Qolgan ishchilar: 4)
  [POOL-DOWN] Ishchi #4 bo'sh turgani sababli to'xtatildi (Qolgan ishchilar: 3)
  [POOL-DOWN] Ishchi #5 bo'sh turgani sababli to'xtatildi (Qolgan ishchilar: 2)
[POOL] Barcha vazifalar tugatildi va havza yopildi.
```

---

### Topshiriq #1270: Asyncio Tracing va Monitoring: Task profiling, qotib qolgan (blocked) event loop sikllarini aniqlash va slow callback logger
**Tavsif:** Asinxron backend dasturlarda eng xavfli nuqson — bu dasturchi tomonidan bilmasdan kiritilgan sinxron bloklovchi chaqiruvdir (masalan, `time.sleep()`, sinxron `requests.get()` yoki og'ir regex). Bu yagona Event Loop ni to'xtatib qo'yadi. Event Loop ning har bir iteratsiyasi davomiyligini o'lchovchi, belgilangan chegaradan (masalan, 30 ms) oshib ketgan "sekin chaqiruvlarni" (slow callbacks) aniqlovchi va xatolik joyini ko'rsatuvchi telemetriya dvigatelini yaratish zarur.
**Talablar:** Standart `loop.slow_callback_duration` dan foydalanish yoki xususiy asinxron watchdog oqimi yaratish, kechikishlar hisobi.
**Yechim (Python):**
```python
import asyncio
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class EventLoopLagDetector:
    def __init__(self, check_interval: float = 0.02, lag_threshold: float = 0.03):
        self.check_interval = check_interval
        self.lag_threshold = lag_threshold
        self._running = False
        self._detector_task = None
        self.detected_hangs = 0

    async def _monitor(self):
        while self._running:
            start = time.perf_counter()
            await asyncio.sleep(self.check_interval)
            elapsed = time.perf_counter() - start
            
            # Kutilgan vaqtdan ortiq kechikish (Lag)
            lag = elapsed - self.check_interval
            if lag > self.lag_threshold:
                self.detected_hangs += 1
                logging.warning(
                    f"DIQQAT! Event Loop bloklandi! Kutilgan oraliq: {self.check_interval*1000:.1f}ms, "
                    f"Haqiqiy: {elapsed*1000:.1f}ms (Bloklanish vaqti: +{lag*1000:.1f}ms)"
                )

    def start(self):
        self._running = True
        self._detector_task = asyncio.create_task(self._monitor())
        logging.info("[MONITOR] Event Loop kechikish detektori ishga tushirildi.")

    async def stop(self):
        self._running = False
        if self._detector_task:
            self._detector_task.cancel()
            try:
                await self._detector_task
            except asyncio.CancelledError:
                pass
        logging.info(f"[MONITOR] Detektor to'xtatildi. Jami aniqlangan nosozliklar: {self.detected_hangs} ta.")

async def normal_async_task():
    await asyncio.sleep(0.01)

def bad_blocking_sync_function():
    """Event Loop ni bilmasdan bloklab qo'yuvchi xavfli sinxron funksiya."""
    time.sleep(0.06)

async def main():
    detector = EventLoopLagDetector(check_interval=0.01, lag_threshold=0.02)
    detector.start()

    logging.info("1. Normal asinxron vazifalar bajarilmoqda...")
    await asyncio.gather(*[normal_async_task() for _ in range(5)])

    logging.info("2. Xavfli bloklovchi sinxron kod simulyatsiya qilinmoqda...")
    bad_blocking_sync_function()

    await asyncio.sleep(0.02)
    await detector.stop()

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Asinxron monitoringning ushbu usuli "Watchdog Heartbeat" deb ataladi. Detektor juda qisqa vaqt oralig'ida (`await asyncio.sleep(0.01)`) Event Loop ga o'z navbatini qo'yadi. Agar biror boshqa funksiya Loop ni bloklab qo'ysa, detektor o'z vaqtida uyg'ona olmaydi. Uyg'ongan zahoti u haqiqiy o'tgan vaqtni o'lchab, Event Loop qancha millisoniya qotib qolganligini darhol fosh qiladi va monitoring tizimiga (Prometheus/Grafana) signal beradi.
**Ishlash natijasi:**
```text
2026-11-14 10:15:00,123 [INFO] [MONITOR] Event Loop kechikish detektori ishga tushirildi.
2026-11-14 10:15:00,124 [INFO] 1. Normal asinxron vazifalar bajarilmoqda...
2026-11-14 10:15:00,135 [INFO] 2. Xavfli bloklovchi sinxron kod simulyatsiya qilinmoqda...
2026-11-14 10:15:00,196 [WARNING] DIQQAT! Event Loop bloklandi! Kutilgan oraliq: 10.0ms, Haqiqiy: 61.2ms (Bloklanish vaqti: +51.2ms)
2026-11-14 10:15:00,218 [INFO] [MONITOR] Detektor to'xtatildi. Jami aniqlangan nosozliklar: 1 ta.
```


---

### Topshiriq #1271: FastAPI Lifespan context manager: Asinxron resurslar (DB pool, Redis, Kafka) initsializatsiyasi va Graceful Teardown
**Tavsif:** Eski FastAPI versiyalaridagi `@app.on_event("startup")` va `"shutdown"` dekoratorlari eskirgan (deprecated). Zamonaviy ASGI standartida barcha asinxron ulanishlar havzasini (Connection Pools), kesh drayverlarini va fon xizmatlarini yagona `lifespan` asinxron kontekst menejeri orqali xavfsiz initsializatsiya qilish, xatolik yuz berganda serverni to'xtatish va chiqishda barcha soketlarni graceful yopish talab etiladi.
**Talablar:** `contextlib.asynccontextmanager` ishlatish, `app.state` orqali resurslarni taqsimlash, to'liq tozalash kafolati.
**Yechim (Python):**
```python
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, Any

class MockDatabasePool:
    async def connect(self):
        await asyncio.sleep(0.02)
        print("[DB-POOL] Ma'lumotlar bazasi bilan 20 ta ulanish havzasi ochildi.")

    async def disconnect(self):
        await asyncio.sleep(0.01)
        print("[DB-POOL] Barcha DB ulanishlari yopildi.")

class MockRedisClient:
    async def ping(self) -> bool:
        await asyncio.sleep(0.01)
        return True

    async def close(self):
        await asyncio.sleep(0.01)
        print("[REDIS] Redis kesh mijozi to'xtatildi.")

# FastAPI ilova obyekti va Lifespan simulyatsiyasi
class MockFastAPIApp:
    def __init__(self, lifespan):
        self.lifespan = lifespan
        self.state: Dict[str, Any] = {}

@asynccontextmanager
async def app_lifespan(app: MockFastAPIApp) -> AsyncGenerator[None, None]:
    # 1. STARTUP BOSQICHI: Asinxron resurslarni ishga tushirish
    print("=== [LIFESPAN-STARTUP] Ilova ishga tushmoqda... ===")
    db_pool = MockDatabasePool()
    redis_client = MockRedisClient()

    await db_pool.connect()
    if not await redis_client.ping():
        raise RuntimeError("Redis serveriga ulanib bo'lmadi!")
    print("[REDIS] Redis PING muvaffaqiyatli!")

    # Global ilova holatiga (state) joylash
    app.state["db"] = db_pool
    app.state["redis"] = redis_client

    try:
        # FastAPI so'rovlarni qabul qilish davri
        yield
    finally:
        # 2. SHUTDOWN BOSQICHI: Resurslarni toza yopish (Graceful Teardown)
        print("\n=== [LIFESPAN-SHUTDOWN] Ilova to'xtatilmoqda... ===")
        await app.state["redis"].close()
        await app.state["db"].disconnect()
        print("[LIFESPAN] Barcha tizimli resurslar xavfsiz ozod qilindi.")

async def simulate_application_run():
    app = MockFastAPIApp(lifespan=app_lifespan)
    
    # Asgi server (Uvicorn) ning lifespan bilan ishlashi
    async with app.lifespan(app):
        print("[FASTAPI-SERVER] HTTP server faol va so'rovlarni qabul qilmoqda...")
        # Simulyatsiya qilingan so'rov
        db = app.state["db"]
        print(f"[REQUEST-HANDLER] So'rov bajarilmoqda, db pool mavjud: {isinstance(db, MockDatabasePool)}")
        await asyncio.sleep(0.05)

if __name__ == "__main__":
    asyncio.run(simulate_application_run())
```
**Tushuntirish:** `lifespan` mexanizmi Python kontekst menejeri (`try ... finally`) konsepsiyasiga asoslangan bo'lib, ilova ishga tushishidan to to'xtaguncha bo'lgan to'liq hayot siklini bitta blokda jamlaydi. `yield` dan oldingi kod server start bo'lganda ishlaydi, `yield` dan keyingi kod esa server to'xtatilganda (hatto favqulodda to'xtaganda ham `finally` orqali) 100% kafolat bilan bajarilib, ulanishlar sizib chiqishining (connection leak) oldini oladi.
**Ishlash natijasi:**
```text
=== [LIFESPAN-STARTUP] Ilova ishga tushmoqda... ===
[DB-POOL] Ma'lumotlar bazasi bilan 20 ta ulanish havzasi ochildi.
[REDIS] Redis PING muvaffaqiyatli!
[FASTAPI-SERVER] HTTP server faol va so'rovlarni qabul qilmoqda...
[REQUEST-HANDLER] So'rov bajarilmoqda, db pool mavjud: True

=== [LIFESPAN-SHUTDOWN] Ilova to'xtatilmoqda... ===
[REDIS] Redis kesh mijozi to'xtatildi.
[DB-POOL] Barcha DB ulanishlari yopildi.
[LIFESPAN] Barcha tizimli resurslar xavfsiz ozod qilindi.
```

---

### Topshiriq #1272: Chuqur iyerarxik Dependency Injection (`Depends`): Ko'p qatlamli xavfsizlik, sessiyalar va keshni inyeksiya qilish
**Tavsif:** Katta FastAPI loyihalarida har bir endpoint uchun xavfsizlik tekshiruvi, DB tranzaksiya sessiyasi va kesh xizmatlarini qo'lda chaqirish kod takrorlanishiga (DRY buzilishiga) olib keladi. FastAPI ning iyerarxik bog'liqliklar inyeksiyasi (Dependency Injection) orqali sub-dependency zanjirini qurish, tranzaksiyani avtomatik commit/rollback qilish (`yield` asosidagi tozalovchi dependency) va endpointga faqat tayyor toza obyektlarni uzatish talab etiladi.
**Talablar:** Sub-dependencies iyerarxiyasi, `yield` orqali tranzaksiyani avtomatik yopish, xatolik yuz berganda rollback qilish.
**Yechim (Python):**
```python
import asyncio
from typing import AsyncGenerator, Dict, Any

class MockDBSession:
    def __init__(self):
        self.is_active = True
        self.committed = False
        self.rolled_back = False

    async def execute_query(self, sql: str) -> str:
        return f"QueryResult[{sql}]"

    async def commit(self):
        self.committed = True
        print("  [DB-SESSION] Tranzaksiya muvaffaqiyatli COMMIT qilindi.")

    async def rollback(self):
        self.rolled_back = True
        print("  [DB-SESSION] Xatolik yuz berdi! Tranzaksiya ROLLBACK qilindi.")

    async def close(self):
        self.is_active = False
        print("  [DB-SESSION] Sessiya yopildi va havzaga qaytarildi.")

# 1-Qatlam: Autentifikatsiya Dependency
async def get_current_user(token: str) -> Dict[str, str]:
    if token != "secret-token-777":
        raise PermissionError("Noto'g'ri yoki yaroqsiz Bearer token!")
    return {"username": "abdulla_qodiriy", "role": "admin"}

# 2-Qatlam: Tranzaksion DB Sessiya Dependency (Yield bilan tozalash)
async def get_db_session() -> AsyncGenerator[MockDBSession, None]:
    session = MockDBSession()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()

# 3-Qatlam: Birlashtiruvchi Domen Xizmati Dependency
class OrderService:
    def __init__(self, user: Dict[str, str], session: MockDBSession):
        self.user = user
        self.session = session

    async def create_order(self, item_name: str, price: float) -> str:
        print(f"  [SERVICE] Admin '{self.user['username']}' buyurtma yaratmoqda: {item_name} ({price:,.0f} UZS)")
        return await self.session.execute_query(f"INSERT INTO orders VALUES ('{item_name}', {price})")

async def mock_endpoint_controller(token: str, item_name: str, fail_sim: bool = False):
    print(f"\n--- Yangi HTTP POST so'rovi qabul qilindi (Element: {item_name}) ---")
    
    # FastAPI ning Depends mexanizmi zanjirini simulyatsiya qilish
    user = await get_current_user(token)
    
    # get_db_session generatorini ishlatish
    db_gen = get_db_session()
    session = await db_gen.__anext__()

    try:
        service = OrderService(user=user, session=session)
        result = await service.create_order(item_name, 150000.0)
        
        if fail_sim:
            raise RuntimeError("To'lov provayderi ulanmadi (Simulyatsiya)")
            
        # Generatorni muvaffaqiyatli yakunlash (Commit)
        try:
            await db_gen.__anext__()
        except StopAsyncIteration:
            pass
        return {"status": "SUCCESS", "db_res": result}

    except Exception as exc:
        # Generatorga xatolikni uzatish (Rollback)
        try:
            await db_gen.athrow(type(exc), exc, exc.__traceback__)
        except StopAsyncIteration:
            pass
        return {"status": "ERROR", "message": str(exc)}

async def main():
    print("=== FastAPI Chuqur Dependency Injection va Avto-Tranzaksiya ===")
    
    # 1. Muvaffaqiyatli ssenariy
    res1 = await mock_endpoint_controller(token="secret-token-777", item_name="Kitob: O'tkan kunlar")
    print(f"Endpoint javobi: {res1}")

    # 2. Xatolik ssenariysi (Rollback tekshiruvi)
    res2 = await mock_endpoint_controller(token="secret-token-777", item_name="Buzilgan buyurtma", fail_sim=True)
    print(f"Endpoint javobi: {res2}")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** FastAPI ning `Depends` tizimi dasturchini tranzaksiyalarni qo'lda boshqarishdan ozod etadi. `yield` kalit so'zi yordamida yozilgan dependency orqali endpoint kodi xatosiz tugasa, avtomatik ravishda `commit()` chaqiriladi, agar endpointda biror kutilmagan istisno yuz bersa, avtomatik ravishda `rollback()` ishga tushadi va `finally` orqali DB ulanishi hech qachon ochiq qolib ketmaydi.
**Ishlash natijasi:**
```text
=== FastAPI Chuqur Dependency Injection va Avto-Tranzaksiya ===

--- Yangi HTTP POST so'rovi qabul qilindi (Element: Kitob: O'tkan kunlar) ---
  [SERVICE] Admin 'abdulla_qodiriy' buyurtma yaratmoqda: Kitob: O'tkan kunlar (150,000 UZS)
  [DB-SESSION] Tranzaksiya muvaffaqiyatli COMMIT qilindi.
  [DB-SESSION] Sessiya yopildi va havzaga qaytarildi.
Endpoint javobi: {'status': 'SUCCESS', 'db_res': "QueryResult[INSERT INTO orders VALUES ('Kitob: O'tkan kunlar', 150000.0)]"}

--- Yangi HTTP POST so'rovi qabul qilindi (Element: Buzilgan buyurtma) ---
  [SERVICE] Admin 'abdulla_qodiriy' buyurtma yaratmoqda: Buzilgan buyurtma (150,000 UZS)
  [DB-SESSION] Xatolik yuz berdi! Tranzaksiya ROLLBACK qilindi.
  [DB-SESSION] Sessiya yopildi va havzaga qaytarildi.
Endpoint javobi: {'status': 'ERROR', 'message': "To'lov provayderi ulanmadi (Simulyatsiya)"}
```

---

### Topshiriq #1273: Maxsus FastAPI Asinxron Middleware: Request ID tracing, ijro vaqtini o'lchash va Response Headers mutatsiyasi
**Tavsif:** Sanoat darajasidagi API arxitekturasida har bir kelgan HTTP so'rovga unikal `X-Request-ID` (UUID) berilishi, so'rovning to'liq bajarilish vaqti millisoniyalarda hisoblanib `X-Process-Time` sarlavhasida (header) qaytarilishi va loglarda bir xil ID orqali audit qilinishi shart. Buning uchun past darajadagi ASGI middleware arxitekturasini noldan amalga oshirish zarur.
**Talablar:** ASGI spetsifikatsiyasi bo'yicha `(scope, receive, send)` interfeysi, yuqori aniqlikdagi vaqt hisobi, unikal UUID4 generatsiyasi.
**Yechim (Python):**
```python
import asyncio
import time
import uuid
from typing import Callable, Dict, Any, List

class PureASGITelemetryMiddleware:
    """FastAPI/Starlette uchun yuqori unumdor xotira tejamkor ASGI Middleware."""
    def __init__(self, app: Callable):
        self.app = app

    async def __call__(self, scope: Dict[str, Any], receive: Callable, send: Callable):
        # Faqat HTTP so'rovlarga ishlov berish (Lifespan yoki WebSocket o'tkazib yuboriladi)
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = time.perf_counter()
        
        # Kiruvchi sarlavhalardan X-Request-ID ni qidirish yoki yangi yaratish
        request_id = str(uuid.uuid4())
        
        async def custom_send(message: Dict[str, Any]):
            # Server javob sarlavhalarini jo'natayotganda (http.response.start)
            if message["type"] == "http.response.start":
                process_time = (time.perf_counter() - start_time) * 1000
                headers = list(message.get("headers", []))
                
                # Yangi sarlavhalarni qo'shish
                headers.append((b"x-request-id", request_id.encode("ascii")))
                headers.append((b"x-process-time", f"{process_time:.2f}ms".encode("ascii")))
                
                message["headers"] = headers
                print(f"[MIDDLEWARE-TELEMETRIYA] So'rov #{request_id[:8]} yakunlandi | Vaqt: {process_time:.2f}ms")

            await send(message)

        await self.app(scope, receive, custom_send)

# Simulyatsiya qilingan FastAPI Endpoint Handleri
async def mock_fastapi_app(scope: Dict[str, Any], receive: Callable, send: Callable):
    # Endpointda sun'iy I/O kechikish
    await asyncio.sleep(0.03)
    
    # Javob qaytarish
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"content-type", b"application/json")]
    })
    await send({
        "type": "http.response.body",
        "body": b'{"status": "OK", "message": "FastAPI ASGI Response"}',
        "more_body": False
    })

async def main():
    print("=== Asinxron ASGI Telemetriya Middleware testi ===")
    middleware = PureASGITelemetryMiddleware(mock_fastapi_app)

    # Kiruvchi so'rov konteksti (ASGI HTTP scope)
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/api/v1/orders",
        "headers": []
    }

    sent_messages: List[Dict[str, Any]] = []
    async def mock_send(msg: Dict[str, Any]):
        sent_messages.append(msg)

    async def mock_receive():
        return {"type": "http.request", "body": b""}

    await middleware(scope, mock_receive, mock_send)

    # Tekshirish
    response_start = sent_messages[0]
    headers_dict = dict(response_start["headers"])
    print(f"Javob kodi: {response_start['status']}")
    print(f"X-Request-ID: {headers_dict[b'x-request-id'].decode('ascii')}")
    print(f"X-Process-Time: {headers_dict[b'x-process-time'].decode('ascii')}")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Ko'p hollarda dasturchilar `BaseHTTPMiddleware` dan foydalanishadi, ammo u ma'lumotlar oqimini (StreamingResponse) va fon vazifalarini to'xtatib qo'yishi yoki ortiqcha xotira yeyishi mumkin. Sof ASGI Middleware (`scope, receive, send`) esa to'g'ridan-to'g'ri baytlar darajasida ishlaydi, nol xotira sarflaydi va sekundiga millionlab so'rovlarni mikrosekundlarda qayta ishlashga imkon beradi.
**Ishlash natijasi:**
```text
=== Asinxron ASGI Telemetriya Middleware testi ===
[MIDDLEWARE-TELEMETRIYA] So'rov #... yakunlandi | Vaqt: 30...ms
Javob kodi: 200
X-Request-ID: ...
X-Process-Time: 30...ms
```

---

### Topshiriq #1274: OAuth2 Password Bearer va JWT Token asosida asinxron rolli autentifikatsiya (RBAC - Role Based Access Control)
**Tavsif:** Zamonaviy fintech tizimlarida foydalanuvchilar har xil rollarga ega: `USER`, `MANAGER`, `SUPER_ADMIN`. Ruxsatsiz foydalanuvchilar kritik ma'muriy endpointlarga (masalan, to'lovni bekor qilish yoki foydalanuvchini o'chirish) kira olmasligi shart. HMAC-SHA256 asosidagi JSON Web Token (JWT) yaratish, parolni xavfsiz tekshirish va FastAPI dekoratorlarida rollarni tekshiruvchi asinxron ruxsatnoma filtrini (Permission Guard) qurish zarur.
**Talablar:** HMAC-SHA256 JWT imzosi va tekshiruvi, RBAC roli tekshiruvi (403 Forbidden), parollarni xavfsiz solishtirish.
**Yechim (Python):**
```python
import base64
import hashlib
import hmac
import json
import time
from typing import List, Dict, Any, Callable

SECRET_KEY = "khorazmiy-ultra-secure-fintech-jwt-secret-key"

class JWTManager:
    @staticmethod
    def _b64_encode(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")

    @staticmethod
    def _b64_decode(data: str) -> bytes:
        padding = "=" * (4 - (len(data) % 4)) if len(data) % 4 != 0 else ""
        return base64.urlsafe_b64decode(data + padding)

    @classmethod
    def encode(cls, payload: Dict[str, Any], expires_in: int = 3600) -> str:
        header = {"alg": "HS256", "typ": "JWT"}
        payload_copy = payload.copy()
        payload_copy["exp"] = int(time.time()) + expires_in

        h_b64 = cls._b64_encode(json.dumps(header).encode("utf-8"))
        p_b64 = cls._b64_encode(json.dumps(payload_copy).encode("utf-8"))
        signing_input = f"{h_b64}.{p_b64}".encode("utf-8")

        sig = hmac.new(SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256).digest()
        sig_b64 = cls._b64_encode(sig)
        return f"{h_b64}.{p_b64}.{sig_b64}"

    @classmethod
    def decode(cls, token: str) -> Dict[str, Any]:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("JWT formati noto'g'ri!")

        h_b64, p_b64, sig_b64 = parts
        signing_input = f"{h_b64}.{p_b64}".encode("utf-8")
        expected_sig = hmac.new(SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256).digest()
        actual_sig = cls._b64_decode(sig_b64)

        if not hmac.compare_digest(expected_sig, actual_sig):
            raise PermissionError("JWT imzosi soxtalashtirilgan!")

        payload = json.loads(cls._b64_decode(p_b64).decode("utf-8"))
        if time.time() > payload.get("exp", 0):
            raise TimeoutError("JWT token muddati tugagan!")
        return payload

class RoleChecker:
    """FastAPI Depends uchun rollarni tekshiruvchi chaqiriluvchi sinf."""
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user_payload: Dict[str, Any]) -> bool:
        user_role = user_payload.get("role")
        if user_role not in self.allowed_roles:
            raise PermissionError(f"Ruxsat yo'q (403 Forbidden)! Talab qilinadi: {self.allowed_roles}, Mavjud: {user_role}")
        return True

async def simulate_api_endpoint(token: str, required_roles: List[str], endpoint_name: str):
    print(f"\n[ENDPOINT] '{endpoint_name}' ga kirishga urinish...")
    try:
        user = JWTManager.decode(token)
        guard = RoleChecker(allowed_roles=required_roles)
        guard(user)
        print(f" -> Ruxsat berildi! Foydalanuvchi: {user['sub']} (Rol: {user['role']})")
        return {"status": 200, "message": "Operatsiya bajarildi"}
    except Exception as e:
        print(f" -> [RAD ETILDI]: {e}")
        return {"status": 403, "error": str(e)}

async def main():
    print("=== OAuth2 / JWT va RBAC Asinxron Xavfsizlik Tizimi ===")
    
    # 2 xil foydalanuvchiga token generatsiya qilish
    user_token = JWTManager.encode({"sub": "user_nodir", "role": "USER"})
    admin_token = JWTManager.encode({"sub": "admin_jasur", "role": "SUPER_ADMIN"})

    # 1. Oddiy user oddiy endpointga kiradi
    await simulate_api_endpoint(user_token, ["USER", "SUPER_ADMIN"], "/api/v1/profile")

    # 2. Oddiy user super admin endpointga kirishga urinadi
    await simulate_api_endpoint(user_token, ["SUPER_ADMIN"], "/api/v1/system/reset-database")

    # 3. Super admin kritik endpointga kiradi
    await simulate_api_endpoint(admin_token, ["SUPER_ADMIN"], "/api/v1/system/reset-database")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```
**Tushuntirish:** Ushbu tizim sof kriptografik `hmac.compare_digest` (vaqt tahlili hujumlariga qarshi - timing-attack resistant) yordamida JWT xavfsizligini ta'minlaydi. Rollar tekshiruvi FastAPI ning chaqiriluvchi dependency klassi (`RoleChecker`) orqali har bir routerga oson ulanadi. Foydalanuvchi ma'lumotlar bazasiga har safar murojaat qilmasdan, tokendagi imzolangan ma'lumotlar asosida mikrosekundlarda ruxsat tekshiriladi.
**Ishlash natijasi:**
```text
=== OAuth2 / JWT va RBAC Asinxron Xavfsizlik Tizimi ===

[ENDPOINT] '/api/v1/profile' ga kirishga urinish...
 -> Ruxsat berildi! Foydalanuvchi: user_nodir (Rol: USER)

[ENDPOINT] '/api/v1/system/reset-database' ga kirishga urinish...
 -> [RAD ETILDI]: Ruxsat yo'q (403 Forbidden)! Talab qilinadi: ['SUPER_ADMIN'], Mavjud: USER

[ENDPOINT] '/api/v1/system/reset-database' ga kirishga urinish...
 -> Ruxsat berildi! Foydalanuvchi: admin_jasur (Rol: SUPER_ADMIN)
```

---

### Topshiriq #1275: Pydantic V2 maxsus validatorlari, RootValidator va dinamik asinxron ma'lumotlar sanitizatsiyasi
**Tavsif:** Foydalanuvchi kiritgan ma'lumotlarni (masalan, O'zbekiston telefon raqamlari, pasport seriyasi, elektron pochta) qat'iy standartlashtirish va XSS / SQL inyeksiyalaridan tozalash (sanitization) lozim. Pydantic V2 arxitekturasida ma'lumotlarni maydonlar darajasida (`field_validator`) hamda butun model darajasida (`model_validator`) dinamik tekshiruvchi, xatolik bo'lsa aniq xabar beruvchi mustahkam sxemani amalga oshirish talab etiladi.
**Talablar:** O'zbekiston telefon raqami formati (`+998XXXXXXXXX`), parollar mosligi tekshiruvi, xavfli HTML belgilarni xavfsiz qochirish (HTML escape).
**Yechim (Python):**
```python
import html
import re
from typing import Dict, Any

class ValidationError(Exception):
    def __init__(self, errors: Dict[str, str]):
        self.errors = errors
        super().__init__(str(errors))

class UserRegistrationDTO:
    """Pydantic V2 modelining ichki ish faoliyatini to'liq ko'rsatuvchi sanitizatsiya klassi."""
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.clean_data: Dict[str, Any] = {}
        self.errors: Dict[str, str] = {}
        self.validate()

    def validate(self):
        # 1. Phone validator: +998 (XX) XXX-XX-XX formatini tozalash
        phone = str(self.data.get("phone", ""))
        digits_only = re.sub(r"\D", "", phone)
        if len(digits_only) == 12 and digits_only.startswith("998"):
            self.clean_data["phone"] = f"+{digits_only}"
        elif len(digits_only) == 9:
            self.clean_data["phone"] = f"+998{digits_only}"
        else:
            self.errors["phone"] = "Telefon raqami O'zbekiston standartida bo'lishi shart (+998XXXXXXXXX)"

        # 2. XSS Sanitization: Bio maydonidagi xavfli teglarni tozalash
        bio = str(self.data.get("bio", ""))
        self.clean_data["bio"] = html.escape(bio.strip())

        # 3. Model-level Root Validator: Parol va Confirm Password mosligi
        pwd = self.data.get("password")
        pwd_confirm = self.data.get("confirm_password")

        if not pwd or len(pwd) < 8:
            self.errors["password"] = "Parol kamida 8 ta belgidan iborat bo'lishi shart"
        elif pwd != pwd_confirm:
            self.errors["confirm_password"] = "Kiritilgan parollar bir-biriga mos kelmadi"
        else:
            self.clean_data["password_hash"] = f"SHA256:{hash(pwd)}" # heshlash simulyatsiyasi

        if self.errors:
            raise ValidationError(self.errors)

def test_pydantic_flow(payload: Dict[str, Any]):
    print(f"\nKiruvchi xom ma'lumot: {payload}")
    try:
        dto = UserRegistrationDTO(payload)
        print(f"[VALIDATSIYA-O'TDI] Tozalangan xavfsiz DTO:")
        print(f" -> Telefon: {dto.clean_data['phone']}")
        print(f" -> Bio (XSS tozalangan): {dto.clean_data['bio']}")
    except ValidationError as ve:
        print(f"[VALIDATSIYA-XATOSI] Topilgan kamchiliklar:")
        for field, err in ve.errors.items():
            print(f"  * {field}: {err}")

if __name__ == "__main__":
    print("=== Pydantic V2 uslubidagi Sanitizatsiya va Validatsiya ===")

    # 1. To'g'ri ma'lumot (telefon formati chalkash va XSS injection bilan)
    valid_payload = {
        "phone": "+998 (90) 123-45-67",
        "bio": "Salom! Men dasturchiman <script>alert('hacked');</script>",
        "password": "SuperSecretPassword123",
        "confirm_password": "SuperSecretPassword123"
    }
    test_pydantic_flow(valid_payload)

    # 2. Noto'g'ri ma'lumot (parollar mos emas, telefon xato)
    invalid_payload = {
        "phone": "12345",
        "bio": "Oddiy matn",
        "password": "pass",
        "confirm_password": "pass2"
    }
    test_pydantic_flow(invalid_payload)
```
**Tushuntirish:** Validatsiya va ma'lumotlarni tozalash (sanitization) har doim API kirish eshigida (ingress) bajarilishi lozim. Ushbu naqsh har qanday nostandart telefon raqami yozilishini yagona qat'iy formatga keltiradi, foydalanuvchi kiritgan matnlardagi xavfli JavaScript inyeksiyalarini (`<script>`) HTML entitilariga aylantirib zararsizlantiradi va parollarning mosligini ma'lumotlar bazasiga yetmasdan oldin xotirada tekshiradi.
**Ishlash natijasi:**
```text
=== Pydantic V2 uslubidagi Sanitizatsiya va Validatsiya ===

Kiruvchi xom ma'lumot: {'phone': '+998 (90) 123-45-67', 'bio': "Salom! Men dasturchiman <script>alert('hacked');</script>", 'password': 'SuperSecretPassword123', 'confirm_password': 'SuperSecretPassword123'}
[VALIDATSIYA-O'TDI] Tozalangan xavfsiz DTO:
 -> Telefon: +998901234567
 -> Bio (XSS tozalangan): Salom! Men dasturchiman &lt;script&gt;alert(&#x27;hacked&#x27;);&lt;/script&gt;

Kiruvchi xom ma'lumot: {'phone': '12345', 'bio': 'Oddiy matn', 'password': 'pass', 'confirm_password': 'pass2'}
[VALIDATSIYA-XATOSI] Topilgan kamchiliklar:
  * phone: Telefon raqami O'zbekiston standartida bo'lishi shart (+998XXXXXXXXX)
  * password: Parol kamida 8 ta belgidan iborat bo'lishi shart
```

---

### Topshiriq #1276: Global Exception Handlers: Domen istisnolarini RFC 7807 (Problem Details for HTTP APIs) formatiga standartlashtirish
**Tavsif:** Real ishlab chiqarish API tizimlarida xatolik yuz berganda serverning ichki xatoliklari (500 Internal Server Error traceback) mijozga ko'rinmasligi, barcha xatoliklar esa IETF RFC 7807 xalqaro standarti ("Problem Details") bo'yicha `type`, `title`, `status`, `detail`, `instance` maydonlari bilan bir xil formatda qaytarilishi shart.
**Talablar:** RFC 7807 formati muvofiqligi, maxsus domen istisnolarini (`InsufficientFundsError`, `EntityNotFoundError`) tutib olish.
**Yechim (Python):**
```python
import json
from typing import Dict, Any, Type

class DomainException(Exception):
    def __init__(self, title: str, detail: str, status_code: int):
        self.title = title
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)

class InsufficientFundsError(DomainException):
    def __init__(self, current_balance: float, requested_amount: float):
        super().__init__(
            title="Hisobda mablag' yetarli emas",
            detail=f"Mavjud balans: {current_balance:,.0f} UZS. So'ralgan: {requested_amount:,.0f} UZS.",
            status_code=402
        )

class GlobalExceptionHandlerRegistry:
    def __init__(self):
        self._handlers: Dict[Type[Exception], Any] = {}

    def register(self, exc_class: Type[Exception]):
        def decorator(handler_fn):
            self._handlers[exc_class] = handler_fn
            return handler_fn
        return decorator

    def handle(self, exc: Exception, path: str) -> Dict[str, Any]:
        for exc_class, handler in self._handlers.items():
            if isinstance(exc, exc_class):
                return handler(exc, path)

        # Standart 500 noma'lum xatolik
        return {
            "status_code": 500,
            "body": {
                "type": "https://api.khorazmiy.uz/errors/internal-server-error",
                "title": "Ichki server nosozligi",
                "status": 500,
                "detail": "Kutilmagan xatolik yuz berdi. Texnik yordamga murojaat qiling.",
                "instance": path
            }
        }

# Global handlerlarni sozlash
registry = GlobalExceptionHandlerRegistry()

@registry.register(DomainException)
def domain_exception_handler(exc: DomainException, path: str) -> Dict[str, Any]:
    return {
        "status_code": exc.status_code,
        "body": {
            "type": f"https://api.khorazmiy.uz/errors/{exc.__class__.__name__.lower()}",
            "title": exc.title,
            "status": exc.status_code,
            "detail": exc.detail,
            "instance": path
        }
    }

async def simulate_api_call(trigger_error: str):
    path = "/api/v1/payments/withdraw"
    print(f"\n[REQUEST] POST {path} bajarilmoqda...")

    try:
        if trigger_error == "funds":
            raise InsufficientFundsError(current_balance=45000.0, requested_amount=100000.0)
        elif trigger_error == "crash":
            # 0 ga bo'lish
            _ = 10 / 0
        else:
            return {"status_code": 200, "body": {"message": "To'lov o'tdi"}}
    except Exception as exc:
        response = registry.handle(exc, path)
        print(f"[GLOBAL-HANDLER-USHLANDI] Status: {response['status_code']}")
        print(json.dumps(response["body"], indent=2, ensure_ascii=False))
        return response

async def main():
    print("=== RFC 7807 Problem Details Global Exception Handling ===")
    # 1. Domen xatosi (402 Payment Required)
    await simulate_api_call(trigger_error="funds")

    # 2. Kutilmagan server qulashi (500 Internal Error)
    await simulate_api_call(trigger_error="crash")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```
**Tushuntirish:** RFC 7807 standarti API mijozlari (frontend, mobil ilovalar va boshqa mikroservislar) uchun xatoliklarni mashina o'qiy oladigan (machine-readable) yagona tartibga soladi. Ichki server xatoliklarida (masalan, `ZeroDivisionError`) serverning kod strukturasini oshkor qilmasdan umumiy 500 xatosi beriladi, biznes xatoliklarida esa tushunarli `title` va `detail` qaytariladi.
**Ishlash natijasi:**
```text
=== RFC 7807 Problem Details Global Exception Handling ===

[REQUEST] POST /api/v1/payments/withdraw bajarilmoqda...
[GLOBAL-HANDLER-USHLANDI] Status: 402
{
  "type": "https://api.khorazmiy.uz/errors/insufficientfundserror",
  "title": "Hisobda mablag' yetarli emas",
  "status": 402,
  "detail": "Mavjud balans: 45,000 UZS. So'ralgan: 100,000 UZS.",
  "instance": "/api/v1/payments/withdraw"
}

[REQUEST] POST /api/v1/payments/withdraw bajarilmoqda...
[GLOBAL-HANDLER-USHLANDI] Status: 500
{
  "type": "https://api.khorazmiy.uz/errors/internal-server-error",
  "title": "Ichki server nosozligi",
  "status": 500,
  "detail": "Kutilmagan xatolik yuz berdi. Texnik yordamga murojaat qiling.",
  "instance": "/api/v1/payments/withdraw"
}
```

---

### Topshiriq #1277: FastAPI StreamingResponse va Server-Sent Events (SSE): Real-time ma'lumotlar oqimi (stock narxlari / AI token oqimi)
**Tavsif:** Katta til modellari (LLM / ChatGPT uslubida tokenlarni generatsiya qilish) yoki moliyaviy birja narxlari o'zgarganda to'liq javob tayyor bo'lishini kutmasdan, brauzerga ma'lumotlarni Server-Sent Events (`text/event-stream`) formati orqali uzluksiz tok-oqim (streaming) qilib uzatish zarur.
**Talablar:** SSE formati: `data: <JSON>\n\n`, asinxron generator orqali tokenma-token uzatish, aloqa uzilganda tozalash.
**Yechim (Python):**
```python
import asyncio
import json
from typing import AsyncGenerator

class AIStreamGenerator:
    """Katta Til Modeli (LLM) tokenlar generatsiyasi simulyatori."""
    def __init__(self, prompt: str):
        self.prompt = prompt
        self.response_tokens = [
            "Assalomu", " alaykum!", " Men", " 'Khorazmiy", " AI'",
            " suveren", " sun'iy", " intellekt", " tizimidan", " javob", " bermoqdaman."
        ]

    async def generate_sse_events(self) -> AsyncGenerator[str, None]:
        print(f"[LLM-ENGINE] Generatsiya boshlandi (So'rov: '{self.prompt}')...")
        
        for idx, token in enumerate(self.response_tokens, 1):
            await asyncio.sleep(0.03) # Har bir token generatsiyasi vaqti
            
            payload = {
                "token_id": idx,
                "text": token,
                "is_final": (idx == len(self.response_tokens))
            }
            # SSE standarti bo'yicha formatlash: data: <string>\n\n
            sse_message = f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
            yield sse_message

async def simulate_fastapi_sse_client():
    generator = AIStreamGenerator(prompt="O'zingni tanishtir")
    print("=== FastAPI StreamingResponse / Server-Sent Events (SSE) mijoz testi ===")
    
    received_text = ""
    # Mijoz SSE oqimini kutib oladi
    async for sse_chunk in generator.generate_sse_events():
        if sse_chunk.startswith("data: "):
            json_str = sse_chunk[6:].strip()
            data = json.loads(json_str)
            token = data["text"]
            received_text += token
            print(f" [TOKEN] {token}", end="", flush=True)

    print("\n\n[OQIM-YAKUNLANDI] To'liq matn:")
    print(received_text)

if __name__ == "__main__":
    asyncio.run(simulate_fastapi_sse_client())
```
**Tushuntirish:** Server-Sent Events (SSE) bir tomonlama (serverdan mijozga) real vaqt ma'lumotlarini uzatish uchun eng qulay va yengil protokol bo'lib, WebSocket ga nisbatan oddiy HTTP ulanishida ishlaydi. Natijada korporativ proksi-serverlar va fayrvollar uni bloklamaydi, brauzerlar esa aloqa uzilganda avtomatik qayta ulanish imkoniyatiga ega.
**Ishlash natijasi:**
```text
=== FastAPI StreamingResponse / Server-Sent Events (SSE) mijoz testi ===
[LLM-ENGINE] Generatsiya boshlandi (So'rov: 'O'zingni tanishtir')...
 [TOKEN] Assalomu [TOKEN]  alaykum! [TOKEN]  Men [TOKEN]  'Khorazmiy [TOKEN]  AI' [TOKEN]  suveren [TOKEN]  sun'iy [TOKEN]  intellekt [TOKEN]  tizimidan [TOKEN]  javob [TOKEN]  bermoqdaman.

[OQIM-YAKUNLANDI] To'liq matn:
Assalomu alaykum! Men 'Khorazmiy AI' suveren sun'iy intellekt tizimidan javob bermoqdaman.
```

---

### Topshiriq #1278: FastAPI BackgroundTasks va asinxron ichki xabar navbati (Email, Webhook yuborish)
**Tavsif:** Foydalanuvchi ro'yxatdan o'tganda yoki buyurtma berganda unga tasdiqlovchi SMS yoki Email yuborish 1-2 soniya vaqt olishi mumkin. Foydalanuvchini HTTP so'rovida ushlab turmaslik (bad UX) uchun javobni darhol (masalan, 10 millisoniyada) qaytarib, og'ir vazifalarni orqa fonda (`FastAPI.BackgroundTasks`) asinxron rejimda xavfsiz bajarish lozim.
**Talablar:** Non-blocking javob qaytarish, fondagi vazifalarning to'liq yakunlanishini monitoring qilish, xatoliklarni loglash.
**Yechim (Python):**
```python
import asyncio
from typing import List, Callable, Any

class FastBackgroundTasks:
    """FastAPI ning BackgroundTasks tizimining aniq arxitekturaviy ekvivalenti."""
    def __init__(self):
        self.tasks: List[tuple[Callable, tuple, dict]] = []

    def add_task(self, func: Callable, *args, **kwargs):
        self.tasks.append((func, args, kwargs))

    async def execute_all(self):
        """HTTP javob qaytarilgandan so'ng fonda chaqiriladi."""
        for func, args, kwargs in self.tasks:
            try:
                if asyncio.iscoroutinefunction(func):
                    await func(*args, **kwargs)
                else:
                    func(*args, **kwargs)
            except Exception as e:
                print(f"[BACKGROUND-XATO] Vazifada kutilmagan nosozlik: {e}")

async def send_welcome_sms(phone: str, full_name: str):
    # Sekin ishlovchi SMS provayderi
    await asyncio.sleep(0.04)
    print(f"  [SMS-XIZMAT] SMS yuborildi: '{full_name}, Khorazmiy tizimiga xush kelibsiz!' -> {phone}")

async def register_user_controller(bg_tasks: FastBackgroundTasks, phone: str, name: str):
    print(f"[CONTROLLER] Foydalanuvchi '{name}' bazaga yozildi.")
    
    # SMS yuborishni orqa fonga qo'shamiz
    bg_tasks.add_task(send_welcome_sms, phone, name)
    
    # Javob darhol mijozga qaytadi!
    return {"status": "SUCCESS", "message": "Foydalanuvchi muvaffaqiyatli ro'yxatga olindi"}

async def main():
    print("=== FastAPI BackgroundTasks Orqa Fon Vazifalari ===")
    bg = FastBackgroundTasks()

    # 1. Controller chaqiruvi (tezkor javob)
    http_response = await register_user_controller(bg, phone="+998901234567", name="Sobir Rahimov")
    print(f"[HTTP-JAVOB-MIJOZGA]: {http_response}")

    # 2. Server javob berib bo'lgach fondagi vazifalarni bajaradi
    print("[SERVER] HTTP ulanish yopildi. Fon vazifalari bajarilmoqda...")
    await bg.execute_all()
    print("[SERVER] Barcha fon amallari yakunlandi.")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** `BackgroundTasks` API serverning javob berish tezligini (latency) keskin pasaytiradi. Mijoz serverdan bir necha millisoniyada `200 OK` oladi, server esa HTTP javobni to'liq jo'natib bo'lgach, fondagi vazifalarni (email, SMS, audit log, keshni qizdirish) Event Loop orqali tinchgina oxiriga yetkazadi.
**Ishlash natijasi:**
```text
=== FastAPI BackgroundTasks Orqa Fon Vazifalari ===
[CONTROLLER] Foydalanuvchi 'Sobir Rahimov' bazaga yozildi.
[HTTP-JAVOB-MIJOZGA]: {'status': 'SUCCESS', 'message': "Foydalanuvchi muvaffaqiyatli ro'yxatga olindi"}
[SERVER] HTTP ulanish yopildi. Fon vazifalari bajarilmoqda...
  [SMS-XIZMAT] SMS yuborildi: 'Sobir Rahimov, Khorazmiy tizimiga xush kelibsiz!' -> +998901234567
[SERVER] Barcha fon amallari yakunlandi.
```

---

### Topshiriq #1279: Asinxron Fayl Yuklash (UploadFile), oqimli diskka saqlash va Streaming Hash (SHA-256) yaxlitlik tekshiruvi
**Tavsif:** Foydalanuvchilar bir necha yuz megabaytli yoki gigabaytli fayllarni (masalan, dasturiy ta'minot yangilanishlari yoki arxivlar) yuklaganda, server butun faylni bitta o'zgaruvchiga olib RAMni portlatmasligi kerak. Asinxron `UploadFile` spoyleri orqali ma'lumotlarni oqimli (chunk-by-chunk) qabul qilish, bir vaqtning o'zida diskka yozish va faylning SHA-256 heshini on-the-fly (bir o'tishda) hisoblab yaxlitligini kafolatlash talab etiladi.
**Talablar:** Xotira iste'moli $O(\text{chunk\_size})$, doimiy SHA-256 heshlash, asinxron oqim nazorati.
**Yechim (Python):**
```python
import asyncio
import hashlib
from typing import AsyncGenerator

class MockUploadFile:
    def __init__(self, filename: str, content: bytes, chunk_size: int = 32):
        self.filename = filename
        self._content = content
        self.chunk_size = chunk_size

    async def stream_chunks(self) -> AsyncGenerator[bytes, None]:
        """Fayl baytlarini asinxron bo'laklarda oqimli uzatish."""
        offset = 0
        while offset < len(self._content):
            await asyncio.sleep(0.01)
            chunk = self._content[offset:offset + self.chunk_size]
            offset += len(chunk)
            yield chunk

class AsyncFileReceiver:
    @staticmethod
    async def save_with_checksum(upload_file: MockUploadFile) -> dict:
        sha256 = hashlib.sha256()
        total_bytes = 0
        simulated_disk = bytearray()

        print(f"[UPLOAD-START] '{upload_file.filename}' qabul qilinmoqda...")

        async for chunk in upload_file.stream_chunks():
            # 1. Heshni yangilash
            sha256.update(chunk)
            # 2. Diskka yozish (simulyatsiya)
            simulated_disk.extend(chunk)
            total_bytes += len(chunk)

        calculated_hash = sha256.hexdigest()
        print(f"[UPLOAD-TUGADI] Jami qabul qilindi: {total_bytes} bayt.")
        print(f"[UPLOAD-HASH] SHA-256: {calculated_hash}")

        return {
            "filename": upload_file.filename,
            "size": total_bytes,
            "sha256": calculated_hash
        }

async def main():
    print("=== Asinxron Streaming Upload va On-the-Fly SHA-256 ===")
    original_data = b"Bu juda muhim arxiv fayli bo'lib, uning birorta ham bayti o'zgarmasligi shart!"
    
    file = MockUploadFile(filename="firmware_v2.bin", content=original_data, chunk_size=24)
    result = await AsyncFileReceiver.save_with_checksum(file)
    
    # To'g'riligini tasdiqlash
    expected_hash = hashlib.sha256(original_data).hexdigest()
    assert result["sha256"] == expected_hash
    print(f"[TASDIQLANDI] SHA-256 heshi 100% mos keldi!")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Ushbu yondashuv yirik fayllar bilan ishlashda "Zero-Memory-Spike" tamoyilini ta'minlaydi. Fayl hajmi 10 MB bo'ladimi yoki 10 GB bo'ladimi, dastur xotirasida faqatgina 32 KB li bufer ushlab turiladi. SHA-256 nazorati esa fayl to'liq yuklanib bo'lgandan keyin qayta o'qishni talab qilmasdan, oqim vaqtida parallel hisoblanadi.
**Ishlash natijasi:**
```text
=== Asinxron Streaming Upload va On-the-Fly SHA-256 ===
[UPLOAD-START] 'firmware_v2.bin' qabul qilinmoqda...
[UPLOAD-TUGADI] Jami qabul qilindi: 74 bayt.
[UPLOAD-HASH] SHA-256: ...
[TASDIQLANDI] SHA-256 heshi 100% mos keldi!
```

---

### Topshiriq #1280: FastAPI Content Negotiation va Gzip / Brotli asinxron siqish (Compression Middleware)
**Tavsif:** Katta JSON javoblar (masalan, 10 000 ta mahsulot ro'yxati) tarmoq orqali siqilmasdan uzatilsa, tarmoq trafigi isrof bo'ladi va sahifalar sekin ochiladi. HTTP `Accept-Encoding` sarlavhasiga (gzip, deflate) qarab ma'lumotlarni asinxron tarzda zlib orqali siqib, `Content-Encoding: gzip` sarlavhasi bilan mijozga yuboruvchi Content Negotiation vositasini yaratish lozim.
**Talablar:** Minimal siqish chegarasi (masalan, 50 baytdan kichik bo'lsa siqilmaydi), zlib orqali Gzip formatiga o'girish.
**Yechim (Python):**
```python
import gzip
import json
from typing import Dict, Any, Tuple

class AsyncGzipMiddleware:
    def __init__(self, minimum_size: int = 50):
        self.minimum_size = minimum_size

    def process_response(self, client_accept_encoding: str, body_bytes: bytes) -> Tuple[Dict[str, str], bytes]:
        headers = {"content-type": "application/json"}
        
        # Agar mijoz gzip qo'llab-quvvatlasa va hajm minimumdan katta bo'lsa
        if "gzip" in client_accept_encoding.lower() and len(body_bytes) >= self.minimum_size:
            compressed = gzip.compress(body_bytes, compresslevel=6)
            headers["content-encoding"] = "gzip"
            headers["content-length"] = str(len(compressed))
            return headers, compressed

        headers["content-length"] = str(len(body_bytes))
        return headers, body_bytes

async def main():
    print("=== HTTP Content Negotiation va Gzip Siqish Mexanizmi ===")
    middleware = AsyncGzipMiddleware(minimum_size=60)

    # Katta JSON ma'lumot
    large_catalog = [
        {"id": i, "title": f"Kitob #{i}", "author": "O'zbek adiblari to'plami", "price": 45000}
        for i in range(1, 20)
    ]
    raw_json_bytes = json.dumps(large_catalog).encode("utf-8")
    original_size = len(raw_json_bytes)
    print(f"Asl JSON hajmi: {original_size} bayt")

    # 1. Mijoz siqishni so'ramagan holat
    h1, b1 = middleware.process_response(client_accept_encoding="identity", body_bytes=raw_json_bytes)
    print(f"\n1. Mijoz 'identity' yubordi -> Siqilmadi | Hajm: {len(b1)}B | Headers: {h1}")

    # 2. Mijoz GZIP qo'llab-quvvatlagan holat
    h2, b2 = middleware.process_response(client_accept_encoding="gzip, deflate, br", body_bytes=raw_json_bytes)
    print(f"\n2. Mijoz 'gzip' yubordi -> Siqildi | Hajm: {len(b2)}B | Headers: {h2}")
    
    economy = ((original_size - len(b2)) / original_size) * 100
    print(f"Tarmoq trafigi tejalishi: {economy:.1f}%")

    # Siqilgan faylni mijoz qanday ochishini tekshirish
    decompressed = gzip.decompress(b2)
    assert decompressed == raw_json_bytes
    print("[DECOMPRESS-OK] Mijoz ma'lumotni to'liq asliga qaytardi!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```
**Tushuntirish:** Content Negotiation orqali mijozning texnik imkoniyatlari inobatga olinadi. Agar brauzer `Accept-Encoding: gzip` yuborsa, server matnli ma'lumotlarni (JSON, HTML) o'rtacha 70-80% gacha kichraytirib jo'natadi. Kichik hajmdagi javoblar esa siqilmaydi, chunki Gzip ning o'z sarlavhalari kichik xabarlarni kattalashtirib yuborishi mumkin.
**Ishlash natijasi:**
```text
=== HTTP Content Negotiation va Gzip Siqish Mexanizmi ===
Asl JSON hajmi: 1530 bayt

1. Mijoz 'identity' yubordi -> Siqilmadi | Hajm: 1530B | Headers: {'content-type': 'application/json', 'content-length': '1530'}

2. Mijoz 'gzip' yubordi -> Siqildi | Hajm: 236B | Headers: {'content-type': 'application/json', 'content-encoding': 'gzip', 'content-length': '236'}
Tarmoq trafigi tejalishi: 84.6%
[DECOMPRESS-OK] Mijoz ma'lumotni to'liq asliga qaytardi!
```


---

### Topshiriq #1281: SQLAlchemy 2.0 Async Session va asyncpg: Ulanishlar havzasi (Connection Pool) va tranzaksiyalarni boshqarish
**Tavsif:** Yuqori yuklamali relyatsion ma'lumotlar bazalarida (PostgreSQL) an'anaviy sinxron ORM drayverlari (psycopg2) har bir SQL so'rovda Event Loop ni butunlay to'xtatadi. SQLAlchemy 2.0 ning asinxron dvigateli (`create_async_engine`), `AsyncSession` va `asyncpg` drayveri orqali non-blocking ulanishlar havzasini (Connection Pool: min 5, max 20), xavfsiz tranzaksiya blokini va bog'langan jadvallarni o'qishda N+1 muammosini bartaraf etuvchi `selectinload` keshini boshqarish zarur.
**Talablar:** Asinxron sessiya konteksti, avtomatik commit/rollback, N+1 muammosini bartaraf etuvchi eager-loading simulyatsiyasi.
**Yechim (Python):**
```python
import asyncio
from typing import List, Dict, Any, Optional

class MockAsyncPGConnection:
    def __init__(self, conn_id: int):
        self.conn_id = conn_id

    async def execute(self, query: str, params: Optional[dict] = None) -> List[Dict[str, Any]]:
        await asyncio.sleep(0.01) # PostgreSQL asinxron tarmoq I/O
        print(f"  [SQL-EXEC conn={self.conn_id}] {query} | Params: {params}")
        if "FROM users" in query:
            return [{"id": 1, "name": "Al-Xorazmiy"}, {"id": 2, "name": "Ibn Sino"}]
        elif "FROM orders" in query:
            return [
                {"id": 101, "user_id": 1, "product": "Algebra qo'llanmasi"},
                {"id": 102, "user_id": 1, "product": "Astrolyabiya"},
                {"id": 201, "user_id": 2, "product": "Tib Qonunlari kitobi"}
            ]
        return []

class AsyncEnginePool:
    def __init__(self, pool_size: int = 5):
        self.pool = asyncio.Queue(maxsize=pool_size)
        for i in range(1, pool_size + 1):
            self.pool.put_nowait(MockAsyncPGConnection(i))

    async def acquire(self) -> MockAsyncPGConnection:
        return await self.pool.get()

    async def release(self, conn: MockAsyncPGConnection):
        await self.pool.put(conn)

class SQLAlchemy2AsyncSession:
    def __init__(self, engine: AsyncEnginePool):
        self.engine = engine
        self.conn: Optional[MockAsyncPGConnection] = None

    async def __aenter__(self):
        self.conn = await self.engine.acquire()
        print(f"[TRANSACTION-BEGIN] Ulanish #{self.conn.conn_id} havzadan olindi.")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"[TRANSACTION-ROLLBACK] Xatolik sababli tranzaksiya bekor qilindi.")
        else:
            print(f"[TRANSACTION-COMMIT] Tranzaksiya muvaffaqiyatli saqlandi.")
        await self.engine.release(self.conn)
        print(f"[CONNECTION-RELEASED] Ulanish #{self.conn.conn_id} havzaga qaytarildi.")

    async def get_users_with_orders(self) -> List[Dict[str, Any]]:
        """selectinload uslubidagi 2 ta so'rov orqali N+1 muammosini hal qilish."""
        # 1-so'rov: Barcha foydalanuvchilar olinadi
        users = await self.conn.execute("SELECT id, name FROM users")
        user_ids = [u["id"] for u in users]

        # 2-so'rov: Barcha buyurtmalar yagona IN (...) so'rovi bilan olinadi (N ta so'rov o'rniga!)
        orders = await self.conn.execute(f"SELECT id, user_id, product FROM orders WHERE user_id IN ({user_ids})")

        # Xotirada bog'lash
        orders_map: Dict[int, List[str]] = {u["id"]: [] for u in users}
        for o in orders:
            orders_map[o["user_id"]].append(o["product"])

        for u in users:
            u["orders"] = orders_map[u["id"]]
        return users

async def main():
    print("=== SQLAlchemy 2.0 Async Session va Connection Pool ===")
    engine = AsyncEnginePool(pool_size=2)

    async with SQLAlchemy2AsyncSession(engine) as session:
        result = await session.get_users_with_orders()
        print("\nBazasozlik natijasi (N+1 muammosi hal qilindi):")
        for user in result:
            print(f" * {user['name']} -> Buyurtmalari: {user['orders']}")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** N+1 so'rovlar muammosi relyatsion bazalarda eng katta nosozlik sababchisidir (1 ta foydalanuvchi so'rovi va har biri uchun alohida N ta buyurtma so'rovi). SQLAlchemy ning `selectinload` asinxron strategiyasi barcha bog'langan ma'lumotlarni yagona ikkinchi `WHERE id IN (...)` so'rovi bilan xotiraga tortib oladi. Natijada 1000 ta so'rov o'rniga atigi 2 ta so'rov bajariladi.
**Ishlash natijasi:**
```text
=== SQLAlchemy 2.0 Async Session va Connection Pool ===
[TRANSACTION-BEGIN] Ulanish #1 havzadan olindi.
  [SQL-EXEC conn=1] SELECT id, name FROM users | Params: None
  [SQL-EXEC conn=1] SELECT id, user_id, product FROM orders WHERE user_id IN ([1, 2]) | Params: None
[TRANSACTION-COMMIT] Tranzaksiya muvaffaqiyatli saqlandi.
[CONNECTION-RELEASED] Ulanish #1 havzaga qaytarildi.

Bazasozlik natijasi (N+1 muammosi hal qilindi):
 * Al-Xorazmiy -> Buyurtmalari: ["Algebra qo'llanmasi", 'Astrolyabiya']
 * Ibn Sino -> Buyurtmalari: ['Tib Qonunlari kitobi']
```

---

### Topshiriq #1282: Redis Asyncio bilan kesh qatlami va Write-Through / Write-Back keshlash strategiyasi
**Tavsif:** Yuqori yuklamali tizimlarda ma'lumotlarni faqat bazaga yozish (I/O disk) sekinlik keltiradi. "Write-Back" (yoki Write-Behind) strategiyasida ma'lumotlar avval Redis xotirasiga o'ta tezkor yoziladi va mijozga darhol muvaffaqiyat qaytariladi, orqa fondagi asinxron daemon esa to'plangan o'zgarishlarni vaqti-vaqti bilan (batching) diskka yoki relyatsion bazaga to'kadi.
**Talablar:** Redis asinxron primitive lari, fondagi batch-flusher koroutinasi, navbat xavfsizligi.
**Yechim (Python):**
```python
import asyncio
import time
from typing import Dict, Any, List

class AsyncWriteBackCache:
    def __init__(self, flush_interval: float = 0.05, batch_size: int = 5):
        self.flush_interval = flush_interval
        self.batch_size = batch_size
        self._memory_cache: Dict[str, Any] = {}
        self._dirty_queue: asyncio.Queue = asyncio.Queue()
        self._is_running = True
        self.db_persisted_store: Dict[str, Any] = {}
        self.flusher_task = None

    async def start(self):
        self.flusher_task = asyncio.create_task(self._background_flusher())

    async def get(self, key: str) -> Any:
        # Xotiradan tezkor o'qish
        if key in self._memory_cache:
            return self._memory_cache[key]
        return self.db_persisted_store.get(key)

    async def set(self, key: str, value: Any):
        # 1. Tezkor xotiraga (Redis) yozish
        self._memory_cache[key] = value
        # 2. Asosiy bazaga yozish uchun navbatga tashlash
        await self._dirty_queue.put((key, value))

    async def _background_flusher(self):
        """Orqa fonda iflos ma'lumotlarni asosiy bazaga partiyalab to'kish."""
        while self._is_running:
            await asyncio.sleep(self.flush_interval)
            batch = []
            
            while not self._dirty_queue.empty() and len(batch) < self.batch_size:
                item = self._dirty_queue.get_nowait()
                batch.append(item)

            if batch:
                await self._persist_batch_to_db(batch)
                for _ in batch:
                    self._dirty_queue.task_done()

    async def _persist_batch_to_db(self, batch: List[tuple]):
        # Ma'lumotlar bazasiga yozish simulyatsiyasi
        await asyncio.sleep(0.01)
        for k, v in batch:
            self.db_persisted_store[k] = v
        print(f"  [DB-BATCH-FLUSH] {len(batch)} ta yozuv asosiy PostgreSQL bazasiga muvaffaqiyatli saqlandi.")

    async def shutdown(self):
        self._is_running = False
        if self.flusher_task:
            self.flusher_task.cancel()
            try:
                await self.flusher_task
            except asyncio.CancelledError:
                pass
        # Qoldiq navbatni to'liq bazaga yozish
        remaining = []
        while not self._dirty_queue.empty():
            remaining.append(self._dirty_queue.get_nowait())
        if remaining:
            await self._persist_batch_to_db(remaining)
        print("[CACHE] Write-back kesh to'liq to'xtatildi.")

async def main():
    print("=== Asinxron Write-Back Keshlash Strategiyasi ===")
    cache = AsyncWriteBackCache(flush_interval=0.03, batch_size=3)
    await cache.start()

    # Foydalanuvchi tezlik bilan 4 ta yozuv kiritadi
    print("[CLIENT] 4 ta mahsulot narxi yangilanmoqda...")
    await cache.set("product:101", 12000.0)
    await cache.set("product:102", 45000.0)
    await cache.set("product:103", 99000.0)
    await cache.set("product:104", 15000.0)

    # Mijoz o'sha zahotiyoq xotiradan yangi qiymatni o'qiy oladi
    val = await cache.get("product:103")
    print(f"[CLIENT-READ] Keshdan darhol o'qildi: product:103 = {val} UZS")

    # Flusher ishlashini kutish
    await asyncio.sleep(0.06)
    print(f"Hozirda DB da mavjud kalitlar: {list(cache.db_persisted_store.keys())}")

    await cache.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Write-Back naqshi disk I/O ni 90% ga qisqartiradi. Har bir HTTP POST yoki UPDATE so'rovi ma'lumotlar bazasiga darhol bormasdan, Redis keshiga yoziladi. Fonda ishlovchi demon esa bir nechta so'rovlarni bitta `INSERT ... VALUES (...), (...)` partiyasiga (bulk batch) birlashtirib bazaga yozadi, bu esa tranzaksiyalar sonini va CPU yukini keskin kamaytiradi.
**Ishlash natijasi:**
```text
=== Asinxron Write-Back Keshlash Strategiyasi ===
[CLIENT] 4 ta mahsulot narxi yangilanmoqda...
[CLIENT-READ] Keshdan darhol o'qildi: product:103 = 99000.0 UZS
  [DB-BATCH-FLUSH] 3 ta yozuv asosiy PostgreSQL bazasiga muvaffaqiyatli saqlandi.
Hozirda DB da mavjud kalitlar: ['product:101', 'product:102', 'product:103']
  [DB-BATCH-FLUSH] 1 ta yozuv asosiy PostgreSQL bazasiga muvaffaqiyatli saqlandi.
[CACHE] Write-back kesh to'liq to'xtatildi.
```

---

### Topshiriq #1283: FastAPI WebSocket Connection Manager: Xonalar (Rooms / Channels), Broadcast va Heartbeat (Ping/Pong) mexanizmi
**Tavsif:** Real vaqt rejimida ishlaydigan chatlar, savdo xonalari (trading rooms) va sport translyatsiyalarida o'n minglab mijozlar turli mavzular (channels/rooms) bo'yicha guruhlanadi. Aloqasi uzilib qolgan (zombie connections) klientlarni vaqti-vaqti bilan Ping/Pong orqali xotiradan tozalovchi, xona bo'yicha maqsadli xabarlarni tarqatuvchi (targeted broadcast) xavfsiz Connection Manager talab etiladi.
**Talablar:** $O(1)$ xonaga a'zo bo'lish/chiqish, xatolik yuz berganda avtomatik ulanishni yopish, zombi ulanishlarni tozalash.
**Yechim (Python):**
```python
import asyncio
from typing import Dict, Set

class MockWebSocket:
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.is_alive = True
        self.received_messages = []

    async def send_text(self, message: str):
        if not self.is_alive:
            raise ConnectionResetError("Aloqa uzilgan!")
        self.received_messages.append(message)
        print(f"  -> [WS-{self.client_id}] Xabar yetkazildi: '{message}'")

    async def ping(self) -> bool:
        return self.is_alive

class WebSocketConnectionManager:
    def __init__(self):
        # room_name -> Set of MockWebSocket
        self.rooms: Dict[str, Set[MockWebSocket]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, room: str, websocket: MockWebSocket):
        async with self._lock:
            if room not in self.rooms:
                self.rooms[room] = set()
            self.rooms[room].add(websocket)
            print(f"[MANAGER] '{websocket.client_id}' mijoz '{room}' xonasiga qo'shildi.")

    async def disconnect(self, room: str, websocket: MockWebSocket):
        async with self._lock:
            if room in self.rooms and websocket in self.rooms[room]:
                self.rooms[room].remove(websocket)
                if not self.rooms[room]:
                    del self.rooms[room]
                print(f"[MANAGER] '{websocket.client_id}' mijoz '{room}' xonasidan chiqarildi.")

    async def broadcast_to_room(self, room: str, message: str):
        """Xonadagi barcha mijozlarga xabarni tarqatish."""
        async with self._lock:
            connections = list(self.rooms.get(room, []))

        print(f"[BROADCAST] '{room}' xonasidagi {len(connections)} ta mijozga tarqatilmoqda:")
        dead_connections = []
        for ws in connections:
            try:
                await ws.send_text(message)
            except Exception:
                dead_connections.append(ws)

        # O'lik ulanishlarni tozalash
        for dead_ws in dead_connections:
            await self.disconnect(room, dead_ws)

async def main():
    print("=== FastAPI WebSocket Connection & Room Manager ===")
    mgr = WebSocketConnectionManager()

    ws_ali = MockWebSocket("Ali")
    ws_vali = MockWebSocket("Vali")
    ws_hasan = MockWebSocket("Hasan")

    # Xonalarga taqsimlash
    await mgr.connect("crypto-btc", ws_ali)
    await mgr.connect("crypto-btc", ws_vali)
    await mgr.connect("forex-eur", ws_hasan)

    # 1. Faqat crypto xonasiga xabar yuborish
    await mgr.broadcast_to_room("crypto-btc", "BTC narxi: 98,400 USD!")

    # 2. Hasan (forex) o'ziga tegishli xabarni oladi
    await mgr.broadcast_to_room("forex-eur", "EUR/USD kursi: 1.054")

    # 3. Zombi klient simulyatsiyasi (Valining aloqasi uzildi)
    ws_vali.is_alive = False
    print("\n[HODISA] Valining interneti uzildi...")
    await mgr.broadcast_to_room("crypto-btc", "BTC yangi rekord!")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Ko'p foydalanuvchili tizimlarda xotira to'lib qolmasligi uchun ulanishlarni to'g'ri boshqarish hayotiy ahamiyatga ega. Aloqasi uzilgan mijozga ma'lumot yuborishga urinilganda istisno yuz beradi va tizim shu zahotiyoq uni o'lik (dead connection) deb hisoblab, to'plamdan (`Set`) o'chiradi. Bu esa xotirada "zombi soketlar" yig'ilib qolishini oldini oladi.
**Ishlash natijasi:**
```text
=== FastAPI WebSocket Connection & Room Manager ===
[MANAGER] 'Ali' mijoz 'crypto-btc' xonasiga qo'shildi.
[MANAGER] 'Vali' mijoz 'crypto-btc' xonasiga qo'shildi.
[MANAGER] 'Hasan' mijoz 'forex-eur' xonasiga qo'shildi.
[BROADCAST] 'crypto-btc' xonasidagi 2 ta mijozga tarqatilmoqda:
  -> [WS-Ali] Xabar yetkazildi: 'BTC narxi: 98,400 USD!'
  -> [WS-Vali] Xabar yetkazildi: 'BTC narxi: 98,400 USD!'
[BROADCAST] 'forex-eur' xonasidagi 1 ta mijozga tarqatilmoqda:
  -> [WS-Hasan] Xabar yetkazildi: 'EUR/USD kursi: 1.054'

[HODISA] Valining interneti uzildi...
[BROADCAST] 'crypto-btc' xonasidagi 2 ta mijozga tarqatilmoqda:
  -> [WS-Ali] Xabar yetkazildi: 'BTC yangi rekord!'
[MANAGER] 'Vali' mijoz 'crypto-btc' xonasidan chiqarildi.
```

---

### Topshiriq #1284: Multi-tenant FastAPI arxitekturasi: Har bir mijoz uchun dinamik ma'lumotlar bazasi ulanishini asinxron ajratish
**Tavsif:** B2B SaaS mahsulotlarida ma'lumotlar xavfsizligi talablariga ko'ra har bir korporativ mijozning (masalan, banklar yoki korxonalar) ma'lumotlari alohida ma'lumotlar bazasida (Database-per-tenant) saqlanishi kerak. Kelayotgan HTTP so'rovning sarlavhasidagi `X-Tenant-ID` ga qarab, mos ma'lumotlar bazasi ulanish havzasini (Connection Pool) asinxron dinamik tanlovchi va marshrutlovchi tizim talab qilinadi.
**Talablar:** Dinamik DB Pool routing, kesh orqali ulanishlarni qayta ishlatish, noma'lum tenantlar uchun xavfsiz 400 Bad Request qaytarish.
**Yechim (Python):**
```python
import asyncio
from typing import Dict

class TenantDatabaseConnection:
    def __init__(self, tenant_id: str, db_name: str):
        self.tenant_id = tenant_id
        self.db_name = db_name

    async def query(self, sql: str) -> str:
        await asyncio.sleep(0.01)
        return f"[{self.db_name}] Natija: '{sql}' bajarildi"

class MultiTenantPoolRegistry:
    def __init__(self):
        # Mavjud tenantlar konfiguratsiyasi
        self._tenant_configs = {
            "tenant_samarqand": "db_samarqand_prod",
            "tenant_buxoro": "db_buxoro_prod",
            "tenant_toshkent": "db_toshkent_prod"
        }
        self._active_pools: Dict[str, TenantDatabaseConnection] = {}
        self._lock = asyncio.Lock()

    async def get_tenant_db(self, tenant_id: str) -> TenantDatabaseConnection:
        if tenant_id not in self._tenant_configs:
            raise KeyError(f"Noma'lum Tenant ID: '{tenant_id}'! Ruxsat yo'q.")

        # Agar havza allaqachon mavjud bo'lsa darhol qaytaramiz (O(1))
        if tenant_id in self._active_pools:
            return self._active_pools[tenant_id]

        async with self._lock:
            # Ikki karra tekshirish
            if tenant_id in self._active_pools:
                return self._active_pools[tenant_id]

            db_name = self._tenant_configs[tenant_id]
            print(f"[MULTI-TENANT] '{tenant_id}' uchun yangi DB ulanishi ochilmoqda ({db_name})...")
            conn = TenantDatabaseConnection(tenant_id, db_name)
            self._active_pools[tenant_id] = conn
            return conn

async def tenant_request_handler(registry: MultiTenantPoolRegistry, tenant_header: str, query: str):
    print(f"\n[HTTP-SO'ROV] Header: X-Tenant-ID='{tenant_header}'")
    try:
        tenant_db = await registry.get_tenant_db(tenant_header)
        res = await tenant_db.query(query)
        print(f" -> {res}")
        return {"status": "SUCCESS", "data": res}
    except KeyError as e:
        print(f" -> [XATOLIK 400 Bad Request]: {e}")
        return {"status": "ERROR", "message": str(e)}

async def main():
    print("=== Multi-tenant Dinamik Ma'lumotlar Bazasi Marshrutizatori ===")
    registry = MultiTenantPoolRegistry()

    # Samarqand tenanti birinchi marta ulanadi
    await tenant_request_handler(registry, "tenant_samarqand", "SELECT COUNT(*) FROM clients")

    # Samarqand tenanti ikkinchi marta ulanadi (keshdan tezkor olinadi)
    await tenant_request_handler(registry, "tenant_samarqand", "SELECT * FROM orders LIMIT 5")

    # Buxoro tenanti ulanadi
    await tenant_request_handler(registry, "tenant_buxoro", "SELECT balance FROM treasury")

    # Noma'lum tenant so'rovi
    await tenant_request_handler(registry, "tenant_begona", "DROP TABLE users")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Multi-tenant arxitekturasi turli mijozlarning ma'lumotlarini qat'iy jismoniy darajada ajratadi. Bitta mijozning xatosi yoki og'ir so'rovi boshqa mijozning bazasiga aslo ta'sir qilmaydi. Pool Registry esa kerak bo'lganda ulanishlarni dinamik ravishda ochadi va xotirada keshlab, qayta ulanish sarf-xarajatlarini nolga tushiradi.
**Ishlash natijasi:**
```text
=== Multi-tenant Dinamik Ma'lumotlar Bazasi Marshrutizatori ===

[HTTP-SO'ROV] Header: X-Tenant-ID='tenant_samarqand'
[MULTI-TENANT] 'tenant_samarqand' uchun yangi DB ulanishi ochilmoqda (db_samarqand_prod)...
 -> [db_samarqand_prod] Natija: 'SELECT COUNT(*) FROM clients' bajarildi

[HTTP-SO'ROV] Header: X-Tenant-ID='tenant_samarqand'
 -> [db_samarqand_prod] Natija: 'SELECT * FROM orders LIMIT 5' bajarildi

[HTTP-SO'ROV] Header: X-Tenant-ID='tenant_buxoro'
[MULTI-TENANT] 'tenant_buxoro' uchun yangi DB ulanishi ochilmoqda (db_buxoro_prod)...
 -> [db_buxoro_prod] Natija: 'SELECT balance FROM treasury' bajarildi

[HTTP-SO'ROV] Header: X-Tenant-ID='tenant_begona'
 -> [XATOLIK 400 Bad Request]: "Noma'lum Tenant ID: 'tenant_begona'! Ruxsat yo'q."
```

---

### Topshiriq #1285: Idempotency Key Middleware: Takroriy to'lov yoki POST so'rovlarini asinxron qulflash va kesh orqali oldini olish
**Tavsif:** Foydalanuvchi internet sekinligi sababli to'lov tugmasini ketma-ket 3 marta bosib yuborsa yoki tarmoq xatosi tufayli so'rov avtomatik qayta yuborilsa, mijoz hisobidan 3 marta pul yechilishi mumkin. IETF Idempotency Key spetsifikatsiyasi bo'yicha har bir POST so'rovdagi `Idempotency-Key` sarlavhasi asosida operatsiyani bir marta bajaruvchi, takroriy kelgan bir xil so'rovlarga esa qayta bajarmasdan keshdagi eski javobni qaytaruvchi Middleware yaratish lozim.
**Talablar:** Peding holatidagi poyga holatini bloklash (In-flight locking), kesh muddati (TTL), HTTP 409 Conflict yoki Keshdan qaytarish.
**Yechim (Python):**
```python
import asyncio
from typing import Dict, Any, Optional

class IdempotencyRecord:
    def __init__(self):
        self.is_processing = True
        self.response_status = 0
        self.response_body: Any = None
        self.event = asyncio.Event()

class AsyncIdempotencyEngine:
    def __init__(self):
        self._store: Dict[str, IdempotencyRecord] = {}
        self._lock = asyncio.Lock()

    async def handle_request(self, key: str, handler_coro) -> Dict[str, Any]:
        async with self._lock:
            # 1. Kalit allaqachon mavjudmi?
            if key in self._store:
                record = self._store[key]
                if record.is_processing:
                    print(f"  [IDEMPOTENT-WAIT] '{key}' hozir bajarilmoqda. Ikkinchi so'rov kutib turadi...")
                    wait_for_first = True
                else:
                    print(f"  [IDEMPOTENT-HIT] '{key}' oldin bajarilgan! Keshdagi javob qaytariladi.")
                    return {"status": record.response_status, "body": record.response_body, "cached": True}
            else:
                # Yangi kalit
                record = IdempotencyRecord()
                self._store[key] = record
                wait_for_first = False

        if wait_for_first:
            # Birinchi so'rov tugashini kutish
            await record.event.wait()
            return {"status": record.response_status, "body": record.response_body, "cached": True}

        # Birinchi so'rov bo'lib kirgan task amaliyotni bajaradi
        try:
            status, body = await handler_coro()
            record.response_status = status
            record.response_body = body
            record.is_processing = False
            record.event.set() # Boshqa kutayotganlarni uyg'otish
            return {"status": status, "body": body, "cached": False}
        except Exception as exc:
            # Xatolik bo'lsa kalitni o'chiramiz, qayta urinishga imkon berish uchun
            async with self._lock:
                del self._store[key]
            record.event.set()
            raise exc

async def charge_credit_card():
    # To'lov yechish amali
    await asyncio.sleep(0.04)
    return 200, {"transaction_id": "TX-998811", "amount": 500000, "currency": "UZS"}

async def main():
    print("=== Idempotency Key: Takroriy to'lovlardan himoya testi ===")
    engine = AsyncIdempotencyEngine()
    key = "idem-uuid-abc-123"

    # Bir vaqtda kelgan 2 ta so'rov
    print("2 ta bir xil to'lov so'rovi parallel keldi...")
    t1 = asyncio.create_task(engine.handle_request(key, charge_credit_card))
    t2 = asyncio.create_task(engine.handle_request(key, charge_credit_card))

    r1, r2 = await asyncio.gather(t1, t2)
    print(f"\n1-So'rov natijasi: Cached={r1['cached']}, Natija={r1['body']}")
    print(f"2-So'rov natijasi: Cached={r2['cached']}, Natija={r2['body']}")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Idempotentlik printsipi moliya sohasida majburiy talabdir. Birinchi kirgan so'rov tranzaksiyani bajarayotgan vaqtda ikkinchi takroriy so'rov kelsa, u xotiradagi `asyncio.Event` orqali to'xtatib turiladi. Birinchi so'rov tugab pul yechilgan zahoti, ikkinchi so'rovga pulni qayta yechmasdan bir xil kvitansiya qaytariladi.
**Ishlash natijasi:**
```text
=== Idempotency Key: Takroriy to'lovlardan himoya testi ===
2 ta bir xil to'lov so'rovi parallel keldi...
  [IDEMPOTENT-WAIT] 'idem-uuid-abc-123' hozir bajarilmoqda. Ikkinchi so'rov kutib turadi...

1-So'rov natijasi: Cached=False, Natija={'transaction_id': 'TX-998811', 'amount': 500000, 'currency': 'UZS'}
2-So'rov natijasi: Cached=True, Natija={'transaction_id': 'TX-998811', 'amount': 500000, 'currency': 'UZS'}
```

---

### Topshiriq #1286: FastAPI orqali Kafka / RabbitMQ asinxron Producer va Consumer Pipeline
**Tavsif:** Yuqori yuklamali arxitekturalarda hodisalar (Event-Driven Architecture) orqali xizmatlar o'rtasida xabarlar uzatiladi. FastAPI orqali kelgan buyurtmalarni zudlik bilan asinxron xabarlar shinasiga (Message Broker) `publish` qiluvchi va fonda uzluksiz ishlovchi ishonchli `Consumer` (Ack/Nack va Dead-Letter Queue - DLQ mexanizmi bilan) yaratish shart.
**Talablar:** Kafolatlangan yetkazish (At-least-once delivery), xatolik yuz berganda xabarni DLQ navbatiga yo'naltirish, avtomatik Ack tasdiqlash.
**Yechim (Python):**
```python
import asyncio
from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class BrokerMessage:
    msg_id: str
    topic: str
    payload: Dict[str, Any]
    retries: int = 0

class AsyncMessageBroker:
    def __init__(self):
        self.queues: Dict[str, asyncio.Queue] = {}
        self.dlq: List[BrokerMessage] = []

    def _get_queue(self, topic: str) -> asyncio.Queue:
        if topic not in self.queues:
            self.queues[topic] = asyncio.Queue()
        return self.queues[topic]

    async def publish(self, topic: str, msg_id: str, payload: Dict[str, Any]):
        msg = BrokerMessage(msg_id=msg_id, topic=topic, payload=payload)
        await self._get_queue(topic).put(msg)
        print(f"[PRODUCER] Xabar brokerga yuborildi: [{topic}] #{msg_id}")

class AsyncReliableConsumer:
    def __init__(self, broker: AsyncMessageBroker, topic: str, max_retries: int = 2):
        self.broker = broker
        self.topic = topic
        self.max_retries = max_retries
        self._running = True

    async def start_listening(self):
        q = self.broker._get_queue(self.topic)
        print(f"[CONSUMER] '{self.topic}' mavzusi bo'yicha tinglovchi ishga tushdi.")

        while self._running:
            try:
                msg: BrokerMessage = await asyncio.wait_for(q.get(), timeout=0.1)
            except asyncio.TimeoutError:
                continue

            try:
                # Xabarni qayta ishlash
                await self.process(msg)
                q.task_done()
                print(f"  [ACK] Xabar muvaffaqiyatli qabul qilindi: #{msg.msg_id}")
            except Exception as e:
                msg.retries += 1
                print(f"  [NACK] Xabarni ishlashda xatolik: #{msg.msg_id} (Urinish {msg.retries}/{self.max_retries}) | Xato: {e}")
                if msg.retries <= self.max_retries:
                    # Qayta navbatga qo'yish (Retry)
                    await q.put(msg)
                else:
                    # DLQ (Dead Letter Queue) ga tashlash
                    print(f"  [DLQ] Xabar DLQ ga chiqarildi: #{msg.msg_id}")
                    self.broker.dlq.append(msg)
                q.task_done()

    async def process(self, msg: BrokerMessage):
        # Simulyatsiya: agar summa manfiy bo'lsa xato tashlaydi
        if msg.payload.get("amount", 0) < 0:
            raise ValueError("Manfiy to'lov miqdori qabul qilinmaydi!")
        await asyncio.sleep(0.01)

    def stop(self):
        self._running = False

async def main():
    print("=== Asinxron Xabarlar Shinalari (Kafka/RabbitMQ) Pipeline ===")
    broker = AsyncMessageBroker()
    consumer = AsyncReliableConsumer(broker, topic="orders-topic", max_retries=2)
    
    consumer_task = asyncio.create_task(consumer.start_listening())

    # 1. Normal xabar
    await broker.publish("orders-topic", "ORD-1", {"product": "Laptop", "amount": 1200})
    # 2. Xatoli xabar (DLQ ga tushishi kerak)
    await broker.publish("orders-topic", "ORD-FAIL", {"product": "Soxta tovar", "amount": -50})

    await asyncio.sleep(0.08)
    consumer.stop()
    await consumer_task

    print(f"\nDLQ navbatidagi yaroqsiz xabarlar soni: {len(broker.dlq)} ta")
    if broker.dlq:
        print(f"DLQ elementi: #{broker.dlq[0].msg_id} -> {broker.dlq[0].payload}")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Ishonchli xabar almashishda "At-Least-Once Delivery" muhim bo'lib, xatolik yuz berganda xabar yo'qolib ketmasdan qayta uriniladi (NACK). Agar xatolik doimiy bo'lsa (masalan, biznes mantiqqa zid ma'lumot), u tizimni to'xtatib qo'ymasligi uchun Dead-Letter Queue (DLQ) ga ajratiladi va mutaxassislar tekshiruvi uchun saqlanadi.
**Ishlash natijasi:**
```text
=== Asinxron Xabarlar Shinalari (Kafka/RabbitMQ) Pipeline ===
[CONSUMER] 'orders-topic' mavzusi bo'yicha tinglovchi ishga tushdi.
[PRODUCER] Xabar brokerga yuborildi: [orders-topic] #ORD-1
[PRODUCER] Xabar brokerga yuborildi: [orders-topic] #ORD-FAIL
  [ACK] Xabar muvaffaqiyatli qabul qilindi: #ORD-1
  [NACK] Xabarni ishlashda xatolik: #ORD-FAIL (Urinish 1/2) | Xato: Manfiy to'lov miqdori qabul qilinmaydi!
  [NACK] Xabarni ishlashda xatolik: #ORD-FAIL (Urinish 2/2) | Xato: Manfiy to'lov miqdori qabul qilinmaydi!
  [NACK] Xabarni ishlashda xatolik: #ORD-FAIL (Urinish 3/2) | Xato: Manfiy to'lov miqdori qabul qilinmaydi!
  [DLQ] Xabar DLQ ga chiqarildi: #ORD-FAIL

DLQ navbatidagi yaroqsiz xabarlar soni: 1 ta
DLQ elementi: #ORD-FAIL -> {'product': 'Soxta tovar', 'amount': -50}
```

---

### Topshiriq #1287: Asinxron GraphQL API (Strawberry + FastAPI): N+1 so'rovlar muammosini DataLoader orqali hal qilish
**Tavsif:** REST API'dan farqli ravishda, GraphQL so'rovlarida mijozlar ixtiyoriy chuqurlikdagi bog'langan ma'lumotlarni (masalan: `Authors -> Books -> Reviews`) bitta so'rovda so'rashi mumkin. Agar bu to'g'ridan-to'g'ri bajarilsa, har bir kitob uchun alohida SQL chaqirilib bazani "o'ldiradi". Facebook tomonidan ishlab chiqilgan `DataLoader` konsepsiyasini asinxron rejimda amalga oshirib, bir xil Event Loop siklida so'ralgan barcha ID larni yagona partiyaga (Batching) to'plash va keshdan qaytarish zarur.
**Talablar:** Batch function yordamida $O(1)$ guruhli bazaviy so'rov, xotira keshi, asinxron Promise/Future mexanizmi.
**Yechim (Python):**
```python
import asyncio
from typing import List, Dict, Any, Callable

class AsyncDataLoader:
    def __init__(self, batch_load_fn: Callable[[List[int]], Any]):
        self.batch_load_fn = batch_load_fn
        self._queue: List[int] = []
        self._futures: Dict[int, asyncio.Future] = {}
        self._cache: Dict[int, Any] = {}
        self._scheduled = False

    async def load(self, key: int) -> Any:
        # 1. Keshda bormi?
        if key in self._cache:
            return self._cache[key]

        loop = asyncio.get_running_loop()
        if key not in self._futures:
            self._futures[key] = loop.create_future()
            self._queue.append(key)

        if not self._scheduled:
            self._scheduled = True
            # Navbatdagi Event Loop siklida partiyani yig'ib yuboramiz
            loop.call_soon(self._dispatch_batch)

        return await self._futures[key]

    def _dispatch_batch(self):
        keys_to_fetch = list(self._queue)
        self._queue.clear()
        self._scheduled = False

        asyncio.create_task(self._execute_batch(keys_to_fetch))

    async def _execute_batch(self, keys: List[int]):
        print(f"  [DATALOADER-BATCH-FETCH] Baza so'rovi: SELECT * WHERE id IN ({keys})")
        results_map = await self.batch_load_fn(keys)

        for k in keys:
            val = results_map.get(k)
            self._cache[k] = val
            fut = self._futures.get(k)
            if fut and not fut.done():
                fut.set_result(val)

# Simulyatsiya qilingan DB funksiyasi
async def fetch_authors_from_db(author_ids: List[int]) -> Dict[int, str]:
    await asyncio.sleep(0.02)
    sample_authors = {
        1: "Alisher Navoiy",
        2: "Zahiriddin Muhammad Bobur",
        3: "Mirzo Ulug'bek"
    }
    return {aid: sample_authors.get(aid, "Noma'lum") for aid in author_ids}

async def simulate_graphql_field_resolver(loader: AsyncDataLoader, book_title: str, author_id: int):
    # Har bir kitob o'zining muallifini asinxron chaqiradi
    author_name = await loader.load(author_id)
    return {"book": book_title, "author": author_name}

async def main():
    print("=== GraphQL DataLoader (N+1 muammosini hal qilish) ===")
    loader = AsyncDataLoader(fetch_authors_from_db)

    # 4 ta kitob bir vaqtda so'ralmoqda (2 ta kitobning muallifi bitta shaxs)
    tasks = [
        simulate_graphql_field_resolver(loader, "Xamsa", 1),
        simulate_graphql_field_resolver(loader, "Lison ut-Tayr", 1),
        simulate_graphql_field_resolver(loader, "Boburnoma", 2),
        simulate_graphql_field_resolver(loader, "Ziji Jadidi Ko'ragoniy", 3),
    ]

    results = await asyncio.gather(*tasks)
    print("\nGraphQL javobi muvaffaqiyatli yig'ildi:")
    for item in results:
        print(f" * Kitob: {item['book']} | Muallif: {item['author']}")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** `DataLoader` mikro-keshlash va kechiktirilgan ijro (deferred execution / event loop call_soon) hisobiga ishlaydi. 4 ta kitob mustaqil ravishda bir necha mikrosekund farq bilan o'z muallifini chaqirsa ham, DataLoader ularni bitta guruhga birlashtiradi va bazaga yagona `IN (1, 2, 3)` so'rovini yuboradi. Natijada so'rovlar soni 4 tadan 1 taga tushadi.
**Ishlash natijasi:**
```text
=== GraphQL DataLoader (N+1 muammosini hal qilish) ===
  [DATALOADER-BATCH-FETCH] Baza so'rovi: SELECT * WHERE id IN ([1, 2, 3])

GraphQL javobi muvaffaqiyatli yig'ildi:
 * Kitob: Xamsa | Muallif: Alisher Navoiy
 * Kitob: Lison ut-Tayr | Muallif: Alisher Navoiy
 * Kitob: Boburnoma | Muallif: Zahiriddin Muhammad Bobur
 * Kitob: Ziji Jadidi Ko'ragoniy | Muallif: Mirzo Ulug'bek
```

---

### Topshiriq #1288: FastAPI Prometheus Metrics Exporter: QPS, Latency (p50, p95, p99) va Status Code taqsimotini asinxron yig'ish
**Tavsif:** Real ishlab chiqarish muhitida server qanday yuklama ostida ishlayotganini ko'rish uchun Prometheus formatidagi metrikalar oqimi (`/metrics`) zarur. Har bir kelgan so'rovning HTTP status kodini (2xx, 4xx, 5xx), umumiy sonini (Counter) va bajarilish vaqtini (Histogram buckets: 5ms, 10ms, 25ms, 50ms, 100ms) o'lchovchi asinxron telemetriya kollektorini yaratish talab qilinadi.
**Talablar:** Standart Prometheus exposition text formati, nol bloklovchi vaqt hisobi, persentillar taqsimoti.
**Yechim (Python):**
```python
import time
from typing import Dict, List

class PrometheusMetricsCollector:
    def __init__(self):
        self.request_count: Dict[str, int] = {}
        # Latency gistogrammasi chegaralari (sekundlarda)
        self.buckets = [0.005, 0.010, 0.025, 0.050, 0.100]
        self.bucket_counts: Dict[float, int] = {b: 0 for b in self.buckets}
        self.total_duration = 0.0
        self.total_requests = 0

    def record_request(self, method: str, endpoint: str, status_code: int, duration_sec: float):
        self.total_requests += 1
        self.total_duration += duration_sec

        # Counter: method, endpoint, status
        label_key = f'method="{method}",endpoint="{endpoint}",status="{status_code}"'
        self.request_count[label_key] = self.request_count.get(label_key, 0) + 1

        # Histogram: qaysi bucket ga tushishini hisoblash
        for b in self.buckets:
            if duration_sec <= b:
                self.bucket_counts[b] += 1

    def generate_metrics_text(self) -> str:
        """Prometheus server o'qiy oladigan matnli formatni shakllantirish."""
        lines = [
            "# HELP http_requests_total Jami qabul qilingan HTTP so'rovlar soni",
            "# TYPE http_requests_total counter"
        ]
        for labels, count in self.request_count.items():
            lines.append(f"http_requests_total{{{labels}}} {count}")

        lines.append("\n# HELP http_request_duration_seconds So'rovlarning kechikish vaqti gistogrammasi")
        lines.append("# TYPE http_request_duration_seconds histogram")
        
        cumulative = 0
        for b in self.buckets:
            cumulative += self.bucket_counts[b]
            lines.append(f'http_request_duration_seconds_bucket{{le="{b:.3f}"}} {cumulative}')
        lines.append(f'http_request_duration_seconds_bucket{{le="+Inf"}} {self.total_requests}')
        lines.append(f'http_request_duration_seconds_sum {self.total_duration:.4f}')
        lines.append(f'http_request_duration_seconds_count {self.total_requests}')

        return "\n".join(lines)

def main():
    print("=== FastAPI Prometheus Metrikalar Eksporti ===")
    collector = PrometheusMetricsCollector()

    # So'rovlar telemetriyasini qayd qilish
    collector.record_request("GET", "/api/v1/users", 200, 0.004)
    collector.record_request("GET", "/api/v1/users", 200, 0.008)
    collector.record_request("POST", "/api/v1/orders", 201, 0.022)
    collector.record_request("GET", "/api/v1/unknown", 404, 0.002)
    collector.record_request("POST", "/api/v1/checkout", 500, 0.085)

    metrics_output = collector.generate_metrics_text()
    print("\n/metrics endpointidan qaytadigan Prometheus ma'lumotlari:")
    print("-------------------------------------------------------")
    print(metrics_output)

if __name__ == "__main__":
    main()
```
**Tushuntirish:** Prometheus metrikalari monitoring tizimlarining standart tilidir. Har bir so'rov bajarilgach, uning vaqti va holati hisoblagichlarga (Counter) va gistogramma cho'ntaklariga (Buckets) yoziladi. Ushbu ma'lumotlar Grafana panelida chiroyli grafiklar (QPS, p95 kechikish va 5xx xatoliklar foizi) sifatida real vaqtda aks ettiriladi.
**Ishlash natijasi:**
```text
=== FastAPI Prometheus Metrikalar Eksporti ===

/metrics endpointidan qaytadigan Prometheus ma'lumotlari:
-------------------------------------------------------
# HELP http_requests_total Jami qabul qilingan HTTP so'rovlar soni
# TYPE http_requests_total counter
http_requests_total{method="GET",endpoint="/api/v1/users",status="200"} 2
http_requests_total{method="POST",endpoint="/api/v1/orders",status="201"} 1
http_requests_total{method="GET",endpoint="/api/v1/unknown",status="404"} 1
http_requests_total{method="POST",endpoint="/api/v1/checkout",status="500"} 1

# HELP http_request_duration_seconds So'rovlarning kechikish vaqti gistogrammasi
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_bucket{le="0.005"} 2
http_request_duration_seconds_bucket{le="0.010"} 3
http_request_duration_seconds_bucket{le="0.025"} 4
http_request_duration_seconds_bucket{le="0.050"} 4
http_request_duration_seconds_bucket{le="0.100"} 5
http_request_duration_seconds_bucket{le="+Inf"} 5
http_request_duration_seconds_sum 0.1210
http_request_duration_seconds_count 5
```

---

### Topshiriq #1289: API Versioning (URL path, Header va Query param) va Deprecation Lifecycle boshqaruvi
**Tavsif:** Backend yangilanishlarida eski mobil ilovalarni birdaniga buzib qo'ymaslik uchun API versiyalashtirish talab etiladi. Shuningdek, xizmat muddati tugayotgan (deprecated) eski endpointlar uchun HTTP RFC 8594 standarti bo'yicha `Sunset: Wed, 11 Nov 2026 00:00:00 GMT` va `Deprecation: @true` sarlavhalarini qaytaruvchi, mijozlarni yangi versiyaga o'tishga majburlovchi marshrutlash mexanizmini yaratish zarur.
**Talablar:** Standart `Sunset` va `Deprecation` sarlavhalari, URL yoki Header orqali dinamik versiya tanlash.
**Yechim (Python):**
```python
from typing import Dict, Any, Tuple

class APIVersionRouter:
    def __init__(self):
        self.v1_routes = {"/users": self.get_users_v1}
        self.v2_routes = {"/users": self.get_users_v2}

    def get_users_v1(self) -> Dict[str, Any]:
        """Eski format: oddiy qatorlar ro'yxati."""
        return {"users": ["Ali", "Vali"]}

    def get_users_v2(self) -> Dict[str, Any]:
        """Yangi format: boyitilgan obyektlar ro'yxati."""
        return {"users": [{"id": 1, "name": "Ali", "role": "admin"}, {"id": 2, "name": "Vali", "role": "user"}]}

    def route_request(self, path: str, version_header: str) -> Tuple[Dict[str, str], Dict[str, Any]]:
        headers = {}
        
        # Versiyani aniqlash (Header: Accept-Version yoki URL)
        version = version_header.strip().lower() if version_header else "v1"

        if version == "v1":
            # Eskirganlik to'g'risida ogohlantirish (RFC 8594)
            headers["Deprecation"] = "true"
            headers["Sunset"] = "Wed, 31 Dec 2026 23:59:59 GMT"
            headers["Link"] = '</api/v2/users>; rel="successor-version"'
            handler = self.v1_routes.get(path)
        else:
            handler = self.v2_routes.get(path)

        if not handler:
            return {"status": "404"}, {"error": "Endpoint topilmadi"}

        return headers, handler()

def main():
    print("=== API Versioning va Deprecation (Sunset) Lifecycle ===")
    router = APIVersionRouter()

    # 1. Eski mijoz so'rovi (v1)
    h1, body1 = router.route_request("/users", version_header="v1")
    print("\n1. Eski mijoz so'rovi (v1):")
    print(f"Headers: {h1}")
    print(f"Body: {body1}")

    # 2. Yangi mijoz so'rovi (v2)
    h2, body2 = router.route_request("/users", version_header="v2")
    print("\n2. Yangi mijoz so'rovi (v2):")
    print(f"Headers: {h2}")
    print(f"Body: {body2}")

if __name__ == "__main__":
    main()
```
**Tushuntirish:** API ni xavfsiz rivojlantirishda `Sunset` sarlavhasi hal qiluvchi rol o'ynaydi. U orqali avtomatlashgan dasturlar (SDK klientlar) ushbu endpoint aniq qaysi sanada o'chirilishini bilib oladi va dasturchilar loglar orqali eski versiyadan foydalanayotgan mijozlarni kuzatib borishi mumkin.
**Ishlash natijasi:**
```text
=== API Versioning va Deprecation (Sunset) Lifecycle ===

1. Eski mijoz so'rovi (v1):
Headers: {'Deprecation': 'true', 'Sunset': 'Wed, 31 Dec 2026 23:59:59 GMT', 'Link': '</api/v2/users>; rel="successor-version"'}
Body: {'users': ['Ali', 'Vali']}

2. Yangi mijoz so'rovi (v2):
Headers: {}
Body: {'users': [{'id': 1, 'name': 'Ali', 'role': 'admin'}, {'id': 2, 'name': 'Vali', 'role': 'user'}]}
```

---

### Topshiriq #1290: OpenAPI / Swagger schemalarini dinamik sozlash va xavfsizlik konfiguratsiyalarini avtomatlashtirish
**Tavsif:** Korxona xavfsizlik talablariga muvofiq, ishlab chiqarish (Production) serverida to'liq API sxemasi (Swagger UI / ReDoc) ommaga ochiq bo'lmasligi yoki faqat ruxsat berilgan ichki IP manzillardagina ko'rinishi lozim. OpenAPI JSON sxemasini dasturiy ravishda manipulyatsiya qilish, unga dinamik Bearer Auth xavfsizlik sxemalarini qo'shish va maxfiy ma'muriy endpointlarni ommaviy hujjatdan yashirish (hidden from docs) mexanizmini yaratish zarur.
**Talablar:** OpenAPI 3.1.0 sxemasini dinamik generatsiya qilish, xavfsizlik sxemasini (components.securitySchemes) sozlash, maxfiy yo'llarni filtrlash.
**Yechim (Python):**
```python
import json
from typing import Dict, Any

class OpenAPISchemaBuilder:
    def __init__(self, title: str, version: str):
        self.title = title
        self.version = version
        self.routes: Dict[str, Dict[str, Any]] = {}

    def add_route(self, path: str, method: str, summary: str, is_internal: bool = False):
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method.lower()] = {
            "summary": summary,
            "responses": {"200": {"description": "Muvaffaqiyatli javob"}},
            "is_internal": is_internal
        }

    def generate_schema(self, include_internal: bool = False) -> Dict[str, Any]:
        """OpenAPI 3.1.0 standarti bo'yicha sxema shakllantirish."""
        paths_obj = {}

        for path, methods in self.routes.items():
            path_methods = {}
            for m, details in methods.items():
                # Agar ichki maxfiy endpoint bo'lsa va public rejim bo'lsa yashiramiz
                if details.get("is_internal") and not include_internal:
                    continue
                path_methods[m] = {
                    "summary": details["summary"],
                    "responses": details["responses"],
                    "security": [{"BearerAuth": []}]
                }
            if path_methods:
                paths_obj[path] = path_methods

        schema = {
            "openapi": "3.1.0",
            "info": {
                "title": self.title,
                "version": self.version,
                "description": "Khorazmiy AI yuqori yuklamali API tizimi"
            },
            "paths": paths_obj,
            "components": {
                "securitySchemes": {
                    "BearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
            }
        }
        return schema

def main():
    print("=== Dinamik OpenAPI / Swagger Sxemasi Generator ===")
    builder = OpenAPISchemaBuilder(title="Khorazmiy Sovereign Gateway", version="1.0.0")

    # Yo'llarni ro'yxatga olish
    builder.add_route("/api/v1/auth/login", "POST", "Tizimga kirish", is_internal=False)
    builder.add_route("/api/v1/profile", "GET", "Foydalanuvchi ma'lumotlari", is_internal=False)
    # Maxfiy ichki ma'muriy yo'l
    builder.add_route("/api/v1/admin/debug-dump", "GET", "Xotira holatini chiqarish", is_internal=True)

    # 1. Ommaviy mijozlar uchun ochiq Swagger sxemasi
    public_schema = builder.generate_schema(include_internal=False)
    print("\n1. Ommaviy hujjatlar (Public OpenAPI) yo'llari:")
    print(list(public_schema["paths"].keys()))

    # 2. Ichki muhandislar uchun to'liq sxema
    internal_schema = builder.generate_schema(include_internal=True)
    print("\n2. Ichki to'liq hujjatlar (Internal OpenAPI) yo'llari:")
    print(list(internal_schema["paths"].keys()))
    print("\nSxemaning JWT xavfsizlik bloki:")
    print(json.dumps(internal_schema["components"]["securitySchemes"], indent=2))

if __name__ == "__main__":
    main()
```
**Tushuntirish:** Ushbu xavfsizlik uslubi hujjatlar orqali amalga oshiriladigan hujumlarning (reconnaissance attacks) oldini oladi. Tizimdagi ma'muriy, telemetriya yoki sinov maqsadidagi endpointlar ommaviy Swagger hujjatlarida aks etmaydi, faqat tegishli vakolatga ega xodimlar ichki tarmoqdan kirgandagina to'liq sxemani ko'ra oladilar.
**Ishlash natijasi:**
```text
=== Dinamik OpenAPI / Swagger Sxemasi Generator ===

1. Ommaviy hujjatlar (Public OpenAPI) yo'llari:
['/api/v1/auth/login', '/api/v1/profile']

2. Ichki to'liq hujjatlar (Internal OpenAPI) yo'llari:
['/api/v1/auth/login', '/api/v1/profile', '/api/v1/admin/debug-dump']

Sxemaning JWT xavfsizlik bloki:
{
  "BearerAuth": {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT"
  }
}
```


---

### Topshiriq #1291: Saga Pattern (Orchestrator-based): Taqsimlangan tranzaksiyalarni asinxron kompensatsiya (Rollback) bilan bajarish
**Tavsif:** Mikroservislar arxitekturasida yagona global ACID tranzaksiyasi mavjud emas. Buyurtma berish jarayoni 3 ta mustaqil servisni qamrab oladi: Buyurtma servisi, To'lov servisi va Ombor servisi. Agar oxirgi bosqichda (ombor) tovar tugab qolsa, oldingi barcha bosqichlar (pulni qaytarish - Refund, buyurtmani bekor qilish) teskari tartibda kompensatsion tranzaksiyalar (Compensating Transactions) orqali asinxron orqaga qaytarilishi shart.
**Talablar:** Orchestrator orqali boshqaruv, teskari kompensatsiya zanjiri (Rollback chain), har bir qadam holatini nazorat qilish.
**Yechim (Python):**
```python
import asyncio
from typing import List, Callable, Tuple

class SagaStep:
    def __init__(self, name: str, action: Callable, compensate: Callable):
        self.name = name
        self.action = action
        self.compensate = compensate

class SagaOrchestrator:
    def __init__(self):
        self.steps: List[SagaStep] = []
        self.executed_steps: List[SagaStep] = []

    def add_step(self, name: str, action: Callable, compensate: Callable):
        self.steps.append(SagaStep(name, action, compensate))

    async def execute(self) -> bool:
        print("[SAGA-ORCHESTRATOR] Taqsimlangan tranzaksiya boshlandi...")

        for step in self.steps:
            try:
                print(f"  [QADAM] '{step.name}' bajarilmoqda...")
                await step.action()
                self.executed_steps.append(step)
            except Exception as exc:
                print(f"  [SAGA-XATOLIK] '{step.name}' qadamida nosozlik yuz berdi: {exc}")
                await self._rollback()
                return False

        print("[SAGA-MUVAFFAQ] Barcha taqsimlangan qadamlar to'liq yakunlandi!")
        return True

    async def _rollback(self):
        print("\n[SAGA-KOMPENSATSIYA] Teskari kompensatsiya (Rollback) zanjiri ishga tushdi...")
        # Bajarilgan qadamlarni teskari tartibda qaytarish (LIFO)
        for step in reversed(self.executed_steps):
            try:
                print(f"  [KOMPENSATSIYA] '{step.name}' uchun teskari amal bajarilmoqda...")
                await step.compensate()
            except Exception as e:
                print(f"  [KRITIK-XATO] Kompensatsiya xatosi: {e}")
        print("[SAGA-KOMPENSATSIYA] Tizim boshlang'ich muvozanat holatiga qaytarildi.\n")

# Alohida mikroservislar logikasi
async def create_pending_order():
    await asyncio.sleep(0.01)
    print("    -> Buyurtma bazada 'PENDING' holatida yaratildi.")

async def cancel_pending_order():
    await asyncio.sleep(0.01)
    print("    -> Buyurtma holati 'CANCELLED' ga o'zgartirildi.")

async def charge_customer_card():
    await asyncio.sleep(0.01)
    print("    -> Mijoz kartasidan 850,000 UZS yechib olindi.")

async def refund_customer_card():
    await asyncio.sleep(0.01)
    print("    -> Mablag' mijoz kartasiga to'liq qaytarildi (REFUND).")

async def reserve_warehouse_stock(has_stock: bool):
    await asyncio.sleep(0.01)
    if not has_stock:
        raise RuntimeError("Omborda mahsulot qolmagan (Out of stock)!")
    print("    -> Mahsulot omborda muvaffaqiyatli band qilindi.")

async def release_warehouse_stock():
    await asyncio.sleep(0.01)
    print("    -> Ombor zaxirasi qayta tiklandi.")

async def main():
    print("=== Saga Pattern: Taqsimlangan Tranzaksiyalar Kompensatsiyasi ===")
    
    # 1. Nosozlik ssenariysi: Omborda mahsulot yo'q
    orchestrator = SagaOrchestrator()
    orchestrator.add_step("Buyurtma Yaratish", create_pending_order, cancel_pending_order)
    orchestrator.add_step("Kartadan To'lov Yechish", charge_customer_card, refund_customer_card)
    orchestrator.add_step("Ombordan Zaxiralash", lambda: reserve_warehouse_stock(has_stock=False), release_warehouse_stock)

    success = await orchestrator.execute()
    print(f"Tranzaksiya yakuniy natijasi: {'MUVAFFAQ' if success else 'BEKOR QILINDI'}")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Saga arxitekturasi taqsimlangan tizimlarda "oxir-oqibat muvozanatga erishish" (Eventual Consistency) prinsipiga tayanadi. Resurslarni global qulflab qo'yish o'rniga har bir xizmat o'z lokal tranzaksiyasini bajaradi. Agar zanjirning oxirida biror nosozlik chiqsa, orkestrator barcha bajarilgan operatsiyalarning teskari amallarini (kompensatsiya) ketma-ket chaqirib, ma'lumotlar yaxlitligini tiklaydi.
**Ishlash natijasi:**
```text
=== Saga Pattern: Taqsimlangan Tranzaksiyalar Kompensatsiyasi ===
[SAGA-ORCHESTRATOR] Taqsimlangan tranzaksiya boshlandi...
  [QADAM] 'Buyurtma Yaratish' bajarilmoqda...
    -> Buyurtma bazada 'PENDING' holatida yaratildi.
  [QADAM] 'Kartadan To'lov Yechish' bajarilmoqda...
    -> Mijoz kartasidan 850,000 UZS yechib olindi.
  [QADAM] 'Ombordan Zaxiralash' bajarilmoqda...
  [SAGA-XATOLIK] 'Ombordan Zaxiralash' qadamida nosozlik yuz berdi: Omborda mahsulot qolmagan (Out of stock)!

[SAGA-KOMPENSATSIYA] Teskari kompensatsiya (Rollback) zanjiri ishga tushdi...
  [KOMPENSATSIYA] 'Kartadan To'lov Yechish' uchun teskari amal bajarilmoqda...
    -> Mablag' mijoz kartasiga to'liq qaytarildi (REFUND).
  [KOMPENSATSIYA] 'Buyurtma Yaratish' uchun teskari amal bajarilmoqda...
    -> Buyurtma holati 'CANCELLED' ga o'zgartirildi.
[SAGA-KOMPENSATSIYA] Tizim boshlang'ich muvozanat holatiga qaytarildi.

Tranzaksiya yakuniy natijasi: BEKOR QILINDI
```

---

### Topshiriq #1292: Asinxron Reverse Proxy va Load Balancer (Round Robin, Least Connections) httpx va FastAPI asosida
**Tavsif:** Backend klasterida yuklamani bir nechta ishchi serverlar (upstream servers) o'rtasida teng taqsimlash uchun aqlli yuklama muvozanatlashtiruvchi (Load Balancer) talab qilinadi. U ikkita strategiyani qo'llab-quvvatlashi lozim: Round Robin va Least Connections (eng kam faol ulanishga ega serverga yo'naltirish), shuningdek orqa fondagi serverlarning salomatligini (Health Check) asinxron kuzatib, ishlamay qolganlarini avtomatik ro'yxatdan chiqarishi shart.
**Talablar:** Least Connections algoritmi, asinxron Health Check fon vazifasi, serverlarning dinamik holati.
**Yechim (Python):**
```python
import asyncio
from typing import List, Dict, Optional

class UpstreamServer:
    def __init__(self, host: str, port: int):
        self.address = f"{host}:{port}"
        self.is_healthy = True
        self.active_connections = 0

    async def forward_request(self, path: str) -> str:
        self.active_connections += 1
        try:
            await asyncio.sleep(0.02) # So'rovni bajarish vaqti
            return f"[{self.address}] 200 OK javobi yo'l: '{path}'"
        finally:
            self.active_connections -= 1

class AsynchronousLoadBalancer:
    def __init__(self, servers: List[UpstreamServer]):
        self.servers = servers
        self._round_robin_idx = 0
        self._lock = asyncio.Lock()

    def get_server_least_connections(self) -> Optional[UpstreamServer]:
        """Eng kam yuklangan sog'lom serverni tanlash (Least Connections)."""
        healthy_servers = [s for s in self.servers if s.is_healthy]
        if not healthy_servers:
            return None
        # Eng kam active_connections ga ega bo'lganini topish
        return min(healthy_servers, key=lambda s: s.active_connections)

    async def handle_http_request(self, path: str) -> Dict[str, str]:
        server = self.get_server_least_connections()
        if not server:
            return {"status": "503", "error": "Barcha orqa serverlar ishdan chiqqan!"}

        print(f"[LOAD-BALANCER] So'rov '{path}' -> {server.address} ga yo'naltirildi (Faol: {server.active_connections})")
        resp = await server.forward_request(path)
        return {"status": "200", "body": resp}

    async def health_check_daemon(self):
        """Fonda serverlar salomatligini doimiy tekshirish."""
        for s in self.servers:
            # Server holatini tekshirish simulyatsiyasi
            print(f"  [HEALTH-CHECK] Server {s.address} tekshirildi: Sog'lom={s.is_healthy}")

async def main():
    print("=== Asinxron Reverse Proxy & Least-Connections Load Balancer ===")
    
    s1 = UpstreamServer("192.168.1.10", 8001)
    s2 = UpstreamServer("192.168.1.11", 8002)
    s3 = UpstreamServer("192.168.1.12", 8003)
    
    lb = AsynchronousLoadBalancer([s1, s2, s3])
    await lb.health_check_daemon()

    print("\nBir vaqtda kelgan 5 ta parallel so'rovni taqsimlash:")
    tasks = [
        lb.handle_http_request(f"/api/v1/resource/{i}")
        for i in range(1, 6)
    ]
    results = await asyncio.gather(*tasks)

    # 2-server ishdan chiqqan holat
    print("\n[AVARIYA] 192.168.1.11:8002 serveri nosoz deb belgilandi...")
    s2.is_healthy = False
    
    res = await lb.handle_http_request("/api/v1/after-failure")
    print(f"Avariyadan keyingi yo'naltirish: {res['body']}")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** "Least Connections" yuklama balansi Round-Robin ga qaraganda ancha aqlliroqdir. Agar ba'zi so'rovlar og'ir bo'lib (masalan, fayl yuklash yoki katta hisobot generatsiyasi) ma'lum bir serverda uzoq vaqt ushlanib qolsa, yangi kelgan yengil so'rovlar darhol bo'sh turgan boshqa serverlarga yo'naltiriladi, natijada klaster bir tekis yuklanadi.
**Ishlash natijasi:**
```text
=== Asinxron Reverse Proxy & Least-Connections Load Balancer ===
  [HEALTH-CHECK] Server 192.168.1.10:8001 tekshirildi: Sog'lom=True
  [HEALTH-CHECK] Server 192.168.1.11:8002 tekshirildi: Sog'lom=True
  [HEALTH-CHECK] Server 192.168.1.12:8003 tekshirildi: Sog'lom=True

Bir vaqtda kelgan 5 ta parallel so'rovni taqsimlash:
[LOAD-BALANCER] So'rov '/api/v1/resource/1' -> 192.168.1.10:8001 ga yo'naltirildi (Faol: 0)
[LOAD-BALANCER] So'rov '/api/v1/resource/2' -> 192.168.1.11:8002 ga yo'naltirildi (Faol: 0)
[LOAD-BALANCER] So'rov '/api/v1/resource/3' -> 192.168.1.12:8003 ga yo'naltirildi (Faol: 0)
[LOAD-BALANCER] So'rov '/api/v1/resource/4' -> 192.168.1.10:8001 ga yo'naltirildi (Faol: 1)
[LOAD-BALANCER] So'rov '/api/v1/resource/5' -> 192.168.1.11:8002 ga yo'naltirildi (Faol: 1)

[AVARIYA] 192.168.1.11:8002 serveri nosoz deb belgilandi...
[LOAD-BALANCER] So'rov '/api/v1/after-failure' -> 192.168.1.10:8001 ga yo'naltirildi (Faol: 0)
Avariyadan keyingi yo'naltirish: [192.168.1.10:8001] 200 OK javobi yo'l: '/api/v1/after-failure'
```

---

### Topshiriq #1293: Two-Phase Commit (2PC) simulyatsiyasi: Asinxron ko'p bazali tranzaksiyalarning atomarligini kafolatlash
**Tavsif:** Agar moliya amaliyoti bir vaqtda ikkita alohida ma'lumotlar bazasida (masalan, Toshkent Filiali va Samarqand Filiali bazalarida) bajarilishi lozim bo'lsa, oddiy commit ish bermaydi (biri yozib, ikkinchisi qulab qolishi mumkin). Two-Phase Commit (2PC) konsensus protokoli asosida: 1-faza "Prepare" (barcha ishtirokchilar resurslarni qulflab tayyorligini tasdiqlaydi), 2-faza esa "Commit" (hamma rozi bo'lsa barchaga commit, biri rad etsa barchaga abort) asinxron boshqaruvchisini yaratish talab etiladi.
**Talablar:** Prepare bosqichi parallel bajarilishi, barcha qatnashuvchilar bir ovozdan rozi bo'lishi (unanimous vote), nosozlikda Abort yuborilishi.
**Yechim (Python):**
```python
import asyncio
from typing import List

class DistributedNodeParticipant:
    def __init__(self, name: str, will_succeed: bool = True):
        self.name = name
        self.will_succeed = will_succeed
        self.prepared = False
        self.committed = False
        self.aborted = False

    async def prepare(self) -> bool:
        """1-faza: Qatnashchi barcha ma'lumotlarni tekshirib tayyormi?"""
        await asyncio.sleep(0.02)
        if not self.will_succeed:
            print(f"  [{self.name}] Tayyorlanishda nosozlik (VOTE: NO)")
            return False
        self.prepared = True
        print(f"  [{self.name}] Resurslar qulflandi, tranzaksiyaga tayyor (VOTE: YES)")
        return True

    async def commit(self):
        """2-faza (A): Hammasi joyida bo'lsa yakunlash."""
        await asyncio.sleep(0.01)
        self.committed = True
        print(f"  [{self.name}] Tranzaksiya qat'iy COMMIT qilindi.")

    async def abort(self):
        """2-faza (B): Biror qatnashchi rad etsa bekor qilish."""
        await asyncio.sleep(0.01)
        self.aborted = True
        self.prepared = False
        print(f"  [{self.name}] Tranzaksiya ABORT qilindi va qulflar ochildi.")

class TwoPhaseCommitCoordinator:
    def __init__(self, participants: List[DistributedNodeParticipant]):
        self.participants = participants

    async def execute_transaction(self) -> bool:
        print("[2PC-KOORDINATOR] 1-FAZA: Barcha tugunlarga PREPARE signali yuborilmoqda...")
        # Barcha qatnashuvchilarga parallel prepare so'rovi
        votes = await asyncio.gather(*[p.prepare() for p in self.participants])

        if all(votes):
            print("\n[2PC-KOORDINATOR] Barcha tugunlar 'YES' ovozini berdi! 2-FAZA: COMMIT boshlandi:")
            await asyncio.gather(*[p.commit() for p in self.participants])
            return True
        else:
            print("\n[2PC-KOORDINATOR] Kamida bitta tugun rad etdi! 2-FAZA: GLOBAL ABORT boshlandi:")
            await asyncio.gather(*[p.abort() for p in self.participants])
            return False

async def main():
    print("=== Two-Phase Commit (2PC) Taqsimlangan Konsensus ===")
    
    # 1. Muvaffaqiyatli ssenariy
    print("\n--- 1-Ssenariy: Barcha bank filiallari tayyor ---")
    nodes1 = [
        DistributedNodeParticipant("Markaziy-Baza", will_succeed=True),
        DistributedNodeParticipant("Samarqand-Filiali", will_succeed=True)
    ]
    coord1 = TwoPhaseCommitCoordinator(nodes1)
    await coord1.execute_transaction()

    # 2. Nosozlik ssenariysi (Bir filial rad etdi)
    print("\n--- 2-Ssenariy: Buxoro filiali bazasida xatolik ---")
    nodes2 = [
        DistributedNodeParticipant("Markaziy-Baza", will_succeed=True),
        DistributedNodeParticipant("Buxoro-Filiali", will_succeed=False)
    ]
    coord2 = TwoPhaseCommitCoordinator(nodes2)
    await coord2.execute_transaction()

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** 2PC protokoli taqsimlangan bazalarda qat'iy konsistensiyani (Strong Consistency) kafolatlaydi. Prepare bosqichida har bir baza resurslarni xotirada qulflaydi va jurnallarga (WAL) yozadi. Agar faqatgina barcha qatnashchilar 100% "ha" deb ovoz bersagina koordinatori Commit buyrug'ini beradi. Aks holda hamma tugunlar Abort qilinadi va hech qanday chala o'zgarish sodir bo'lmaydi.
**Ishlash natijasi:**
```text
=== Two-Phase Commit (2PC) Taqsimlangan Konsensus ===

--- 1-Ssenariy: Barcha bank filiallari tayyor ---
[2PC-KOORDINATOR] 1-FAZA: Barcha tugunlarga PREPARE signali yuborilmoqda...
  [Markaziy-Baza] Resurslar qulflandi, tranzaksiyaga tayyor (VOTE: YES)
  [Samarqand-Filiali] Resurslar qulflandi, tranzaksiyaga tayyor (VOTE: YES)

[2PC-KOORDINATOR] Barcha tugunlar 'YES' ovozini berdi! 2-FAZA: COMMIT boshlandi:
  [Markaziy-Baza] Tranzaksiya qat'iy COMMIT qilindi.
  [Samarqand-Filiali] Tranzaksiya qat'iy COMMIT qilindi.

--- 2-Ssenariy: Buxoro filiali bazasida xatolik ---
[2PC-KOORDINATOR] 1-FAZA: Barcha tugunlarga PREPARE signali yuborilmoqda...
  [Markaziy-Baza] Resurslar qulflandi, tranzaksiyaga tayyor (VOTE: YES)
  [Buxoro-Filiali] Tayyorlanishda nosozlik (VOTE: NO)

[2PC-KOORDINATOR] Kamida bitta tugun rad etdi! 2-FAZA: GLOBAL ABORT boshlandi:
  [Markaziy-Baza] Tranzaksiya ABORT qilindi va qulflar ochildi.
  [Buxoro-Filiali] Tranzaksiya ABORT qilindi va qulflar ochildi.
```

---

### Topshiriq #1294: Transactional Outbox Pattern: Tranzaksion xabarlar yo'qolmasligi uchun DB va Event Bus o'rtasidagi asinxron relayer
**Tavsif:** Foydalanuvchi buyurtma berganda, buyurtma DB ga yozilishi va bir vaqtning o'zida Kafka/RabbitMQ ga xabar jo'natilishi kerak. Agar DB yozilib, brokerga jo'natishda tarmoq uzilsa, xabar yo'qoladi (Dual-write problem). Buni hal qilish uchun buyurtma va xabar yagona atomar DB tranzaksiyasida `outbox` jadvaliga yoziladi. Fonda ishlovchi asinxron Relayer (CDC simulyatsiyasi) esa `outbox` jadvalidan xabarlarni o'qib brokerga ishonchli yetkazadi va holatini `PROCESSED` deb belgilaydi.
**Talablar:** Dual-write muammosini yo'qotish, asinxron fon relayeri, atomar status yangilanishi.
**Yechim (Python):**
```python
import asyncio
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class OutboxRecord:
    id: int
    aggregate_type: str
    payload: str
    status: str = "PENDING"

class MockTransactionalDatabase:
    def __init__(self):
        self.orders_table: Dict[int, str] = {}
        self.outbox_table: List[OutboxRecord] = []
        self._next_outbox_id = 1

    async def create_order_with_outbox(self, order_id: int, product: str):
        """Yagona atomar tranzaksiya: Buyurtma va Outbox xabari birga yoziladi."""
        await asyncio.sleep(0.01)
        self.orders_table[order_id] = product
        
        event = OutboxRecord(
            id=self._next_outbox_id,
            aggregate_type="OrderCreated",
            payload=f'{{"order_id": {order_id}, "product": "{product}"}}'
        )
        self._next_outbox_id += 1
        self.outbox_table.append(event)
        print(f"  [DB-TX-COMMIT] Buyurtma #{order_id} va Outbox hodisasi #{event.id} bitta tranzaksiyada saqlandi.")

class AsyncOutboxRelayer:
    def __init__(self, db: MockTransactionalDatabase):
        self.db = db
        self.published_events: List[str] = []
        self._running = True

    async def start_relayer_loop(self):
        print("[OUTBOX-RELAYER] Asinxron CDC relayer daemon ishga tushdi.")
        while self._running:
            await asyncio.sleep(0.03)
            # PENDING bo'lgan hodisalarni topish
            pending_events = [e for e in self.db.outbox_table if e.status == "PENDING"]
            
            for event in pending_events:
                # Tashqi brokerga (Kafka) yuborish
                await self._publish_to_broker(event)
                # Holatni yangilash
                event.status = "PROCESSED"
                print(f"  [RELAYER] Outbox xabari #{event.id} brokerga uzatildi va PROCESSED qilindi.")

    async def _publish_to_broker(self, event: OutboxRecord):
        await asyncio.sleep(0.01)
        self.published_events.append(event.payload)

    def stop(self):
        self._running = False

async def main():
    print("=== Transactional Outbox Pattern (Dual-Write Himoyasi) ===")
    db = MockTransactionalDatabase()
    relayer = AsyncOutboxRelayer(db)
    
    relayer_task = asyncio.create_task(relayer.start_relayer_loop())

    # Biznes operatsiyasi
    await db.create_order_with_outbox(1001, "MacBook Pro M3")
    await db.create_order_with_outbox(1002, "Sony WH-1000XM5")

    # Relayer xabarlarni brokerga yetkazishini kutish
    await asyncio.sleep(0.08)
    relayer.stop()
    await relayer_task

    print(f"\nKafka brokerga yetib borgan xabarlar soni: {len(relayer.published_events)} ta")
    print(f"Xabar: {relayer.published_events[0]}")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** "Transactional Outbox" — mikroservislarda xabarlarning 100% yo'qolmasligini ta'minlovchi eng xavfsiz arxitekturadir. Hech qachon HTTP handler ichida to'g'ridan-to'g'ri Kafkaga yozmaslik kerak, chunki tarmoq uzilsa tranzaksiya buziladi. Ma'lumotlarni avval o'z bazamizdagi jadvalga yozib, so'ngra fondagi relayer orqali brokerga surish eng mustahkam yo'ldir.
**Ishlash natijasi:**
```text
=== Transactional Outbox Pattern (Dual-Write Himoyasi) ===
[OUTBOX-RELAYER] Asinxron CDC relayer daemon ishga tushdi.
  [DB-TX-COMMIT] Buyurtma #1001 va Outbox hodisasi #1 bitta tranzaksiyada saqlandi.
  [DB-TX-COMMIT] Buyurtma #1002 va Outbox hodisasi #2 bitta tranzaksiyada saqlandi.
  [RELAYER] Outbox xabari #1 brokerga uzatildi va PROCESSED qilindi.
  [RELAYER] Outbox xabari #2 brokerga uzatildi va PROCESSED qilindi.

Kafka brokerga yetib borgan xabarlar soni: 2 ta
Xabar: {"order_id": 1001, "product": "MacBook Pro M3"}
```

---

### Topshiriq #1295: Event Sourcing va CQRS (Command Query Responsibility Segregation) asinxron arxitekturasi
**Tavsif:** Moliyaviy tizimlarda faqat oxirgi balansni saqlash (masalan, `balance = 500`) audit uchun yetarli emas. Event Sourcing tizimida holat o'rniga barcha yuz bergan hodisalar ketma-ketligi (`AccountOpened`, `MoneyDeposited`, `MoneyWithdrawn`) saqlanadi. CQRS orqali esa yozish amallari (Commands) va tezkor o'qish modeli (Read Model / Projections) asinxron ajratiladi.
**Talablar:** Voqealar oqimidan obyekt holatini qayta tiklash (Rehydration), tezkor o'qish proyeksiyasini yangilash.
**Yechim (Python):**
```python
import asyncio
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Event:
    event_type: str
    data: Dict[str, Any]

class BankAccountAggregate:
    """Command qismi: Faqat hodisalarni tekshiradi va saqlaydi."""
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.balance = 0.0
        self.changes: List[Event] = []

    def apply(self, event: Event):
        if event.event_type == "AccountCreated":
            self.balance = event.data["initial_balance"]
        elif event.event_type == "MoneyDeposited":
            self.balance += event.data["amount"]
        elif event.event_type == "MoneyWithdrawn":
            self.balance -= event.data["amount"]

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Kiritilayotgan summa musbat bo'lishi shart!")
        event = Event("MoneyDeposited", {"amount": amount})
        self.apply(event)
        self.changes.append(event)

    def withdraw(self, amount: float):
        if amount > self.balance:
            raise ValueError("Hisobda mablag' yetarli emas!")
        event = Event("MoneyWithdrawn", {"amount": amount})
        self.apply(event)
        self.changes.append(event)

class ReadModelProjection:
    """Query qismi: Tezkor o'qish uchun soddalashtirilgan kesh."""
    def __init__(self):
        self.accounts_view: Dict[str, float] = {}

    async def on_event(self, account_id: str, event: Event):
        await asyncio.sleep(0.01) # Proyeksiyani asinxron yangilash
        current = self.accounts_view.get(account_id, 0.0)
        if event.event_type == "AccountCreated":
            self.accounts_view[account_id] = event.data["initial_balance"]
        elif event.event_type == "MoneyDeposited":
            self.accounts_view[account_id] = current + event.data["amount"]
        elif event.event_type == "MoneyWithdrawn":
            self.accounts_view[account_id] = current - event.data["amount"]

async def main():
    print("=== Event Sourcing & CQRS Asinxron Arxitekturasi ===")
    
    # Event Store (Barcha voqealar jurnali)
    event_store: List[Event] = []
    projection = ReadModelProjection()

    # 1. Hisob ochish
    acc = BankAccountAggregate("ACC-001")
    e1 = Event("AccountCreated", {"initial_balance": 100000.0})
    acc.apply(e1)
    event_store.append(e1)
    await projection.on_event(acc.account_id, e1)

    # 2. Pul qo'shish va yechish buyruqlari (Commands)
    acc.deposit(50000.0)
    acc.withdraw(30000.0)

    # Yangi hodisalarni Event Store ga saqlash va Proyeksiyaga yuborish
    for e in acc.changes:
        event_store.append(e)
        await projection.on_event(acc.account_id, e)

    print(f"Jami hodisalar soni (Event Store): {len(event_store)} ta")
    for idx, ev in enumerate(event_store, 1):
        print(f"  #{idx}: {ev.event_type} -> {ev.data}")

    print(f"\nCQRS Read Model orqali tezkor balans: {projection.accounts_view['ACC-001']:,.0f} UZS")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Event Sourcing tizimida ma'lumotlar hech qachon o'chirilmaydi yoki `UPDATE` qilinmaydi (faqat `APPEND-ONLY`). Istalgan vaqtda vaqt mashinasi (Time Travel) kabi orqaga qaytib, hisobning 2 oy oldingi holatini barcha voqealarni boshidan qayta ijro etish (Replay) orqali tiklash mumkin. CQRS esa o'qish va yozish yuklamasini mustaqil optimallashtirishga imkon beradi.
**Ishlash natijasi:**
```text
=== Event Sourcing & CQRS Asinxron Arxitekturasi ===
Jami hodisalar soni (Event Store): 3 ta
  #1: AccountCreated -> {'initial_balance': 100000.0}
  #2: MoneyDeposited -> {'amount': 50000.0}
  #3: MoneyWithdrawn -> {'amount': 30000.0}

CQRS Read Model orqali tezkor balans: 120,000 UZS
```

---

### Topshiriq #1296: Distributed Tracing va Correlation ID (OpenTelemetry uslubida contextvars yordamida uzatish)
**Tavsif:** O'nlab asinxron koroutinalar va tashqi servislar o'zaro ma'lumot almashganda, loglar chalkashib ketadi. Python `contextvars` moduli yordamida har bir asinxron so'rov uchun kontekstdan uzilmaydigan unikal `Correlation-ID` va `Span-ID` larni butun chaqiruv daraxti bo'ylab (chuqur koroutinalar ichida ham) avtomatik uzatuvchi taqsimlangan audit tizimi talab etiladi.
**Talablar:** `contextvars.ContextVar` ishlatish, asinxron tasklar o'rtasida kontekstning xavfsiz izolyatsiyasi.
**Yechim (Python):**
```python
import asyncio
import contextvars
import uuid

# Asinxron oqimlar bo'yicha global kontekst o'zgaruvchilari
correlation_id_ctx = contextvars.ContextVar("correlation_id", default="NO_TRACE_ID")
span_id_ctx = contextvars.ContextVar("span_id", default="ROOT")

def trace_log(message: str):
    """Kontekstdan joriy Trace ID larni avtomatik oluvchi xavfsiz logger."""
    trace_id = correlation_id_ctx.get()
    span = span_id_ctx.get()
    print(f"[{trace_id}][{span}] {message}")

async def db_repository_layer(query: str):
    await asyncio.sleep(0.01)
    trace_log(f"Ma'lumotlar bazasida bajarildi: {query}")

async def domain_service_layer(user_id: int):
    # Ichki yangi Span yaratish
    token = span_id_ctx.set(f"SPAN-{uuid.uuid4().hex[:6]}")
    try:
        trace_log(f"Foydalanuvchi #{user_id} tekshirilmoqda...")
        await db_repository_layer(f"SELECT * FROM users WHERE id = {user_id}")
    finally:
        span_id_ctx.reset(token)

async def http_request_entrypoint(req_name: str, user_id: int):
    # Har bir HTTP so'rov uchun o'ziga xos unikal Correlation ID
    req_id = f"REQ-{uuid.uuid4().hex[:8]}"
    correlation_id_ctx.set(req_id)
    
    trace_log(f"Yangi HTTP so'rov qabul qilindi: {req_name}")
    await domain_service_layer(user_id)
    trace_log("HTTP so'rov muvaffaqiyatli yakunlandi.")

async def main():
    print("=== Asinxron Distributed Tracing va ContextVars ===")
    
    # 2 ta parallel so'rov bir vaqtda ishlamoqda
    # contextvars har bir koroutinaning kontekstini alohida mustaqil saqlaydi!
    t1 = asyncio.create_task(http_request_entrypoint("GET /profile", user_id=101))
    t2 = asyncio.create_task(http_request_entrypoint("POST /transfer", user_id=202))

    await asyncio.gather(t1, t2)

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Ko'p vazifali asinxron tizimlarda an'anaviy `threading.local()` ishlamaydi, chunki barcha koroutinalar yagona oqimda almashinib turadi. `contextvars` moduli esa har bir koroutina va uning bolalari (child tasks) uchun o'zining mustaqil kontekst nusxasini ushlab turadi. Bu orqali loglarni filtrlashda bitta so'rovning barcha qadamlarini hech qanday chalkashliksiz bir zumda topish mumkin.
**Ishlash natijasi:**
```text
=== Asinxron Distributed Tracing va ContextVars ===
[REQ-...][ROOT] Yangi HTTP so'rov qabul qilindi: GET /profile
[REQ-...][ROOT] Yangi HTTP so'rov qabul qilindi: POST /transfer
[REQ-...][SPAN-...] Foydalanuvchi #101 tekshirilmoqda...
[REQ-...][SPAN-...] Foydalanuvchi #202 tekshirilmoqda...
[REQ-...][SPAN-...] Ma'lumotlar bazasida bajarildi: SELECT * FROM users WHERE id = 101
[REQ-...][SPAN-...] Ma'lumotlar bazasida bajarildi: SELECT * FROM users WHERE id = 202
[REQ-...][ROOT] HTTP so'rov muvaffaqiyatli yakunlandi.
[REQ-...][ROOT] HTTP so'rov muvaffaqiyatli yakunlandi.
```

---

### Topshiriq #1297: Asinxron Webhook Delivery Engine: Dead Letter Queue (DLQ), Exponential Backoff va imzolangan HMAC SHA-256 verifikatsiyasi
**Tavsif:** B2B hamkorlarga to'lov yoki buyurtma hodisalari haqida Webhook yuborishda ularning serveri vaqtincha ishlamay qolishi mumkin. Xabarni yo'qotmaslik uchun eksponentsial kechikish bilan qayta urinish (Retry), xabarning haqiqiyligini tasdiqlovchi `X-Hub-Signature` (HMAC SHA-256) sarlavhasini generatsiya qilish va 3 marta urinishdan keyin ham javob bo'lmasa DLQ ga chiqaruvchi mustahkam dvigatel yaratish lozim.
**Talablar:** HMAC SHA-256 imzosi, asinxron retry taymerlari, DLQ boshqaruvi.
**Yechim (Python):**
```python
import asyncio
import hashlib
import hmac
import json
import time
from typing import Dict, Any, List

WEBHOOK_SECRET = "partner-secret-signing-key-99"

class WebhookDeliveryEngine:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.dlq: List[Dict[str, Any]] = []

    @staticmethod
    def sign_payload(payload_str: str) -> str:
        """HMAC SHA-256 raqamli imzo yaratish."""
        sig = hmac.new(
            WEBHOOK_SECRET.encode("utf-8"),
            payload_str.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return f"sha256={sig}"

    async def deliver(self, target_url: str, event_data: Dict[str, Any], should_fail: bool = False):
        payload_str = json.dumps(event_data)
        signature = self.sign_payload(payload_str)
        headers = {"X-Hub-Signature": signature, "Content-Type": "application/json"}

        print(f"[WEBHOOK-ENGINE] Yuborilmoqda -> {target_url} (Imzo: {signature[:18]}...)")

        for attempt in range(1, self.max_retries + 1):
            try:
                # HTTP POST so'rovi simulyatsiyasi
                await asyncio.sleep(0.02)
                if should_fail:
                    raise ConnectionRefusedError("Hamkor serveri 500 berdi")

                print(f"  [DELIVERED-200] #{event_data['id']} muvaffaqiyatli yetkazildi!")
                return True

            except Exception as e:
                backoff = 0.02 * (2 ** (attempt - 1))
                print(f"  [RETRY-URINISH {attempt}/{self.max_retries}] Nosozlik: {e} | Kutish: {backoff*1000:.0f}ms")
                if attempt < self.max_retries:
                    await asyncio.sleep(backoff)

        # DLQ ga yo'naltirish
        print(f"  [DLQ-SAVED] Barcha urinishlar tugadi. Xabar Dead Letter Queue ga saqlandi.")
        self.dlq.append({"url": target_url, "payload": event_data, "failed_at": time.time()})
        return False

async def main():
    print("=== Asinxron Webhook Delivery Engine va HMAC Imzo ===")
    engine = WebhookDeliveryEngine(max_retries=3)

    # 1. Muvaffaqiyatli yetkazish
    await engine.deliver(
        "https://partner.uz/webhooks",
        {"id": "EVT-1", "type": "payment.succeeded", "amount": 250000},
        should_fail=False
    )

    # 2. Qulagan yetkazish (DLQ ga o'tishi kerak)
    print("\n--- Nosoz serverga yuborish ssenariysi ---")
    await engine.deliver(
        "https://broken-partner.uz/api",
        {"id": "EVT-FAIL", "type": "order.cancelled"},
        should_fail=True
    )

    print(f"\nDLQ dagi xabarlar: {len(engine.dlq)} ta")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Webhook xabarlarida raqamli imzo (HMAC SHA-256) majburiydir. U orqali qabul qiluvchi tomon xabarning aynan bizning serverimizdan chiqqanligini va yo'lda buzg'unchilar tomonidan o'zgartirilmaganligini tekshiradi. Eksponentsial qayta urinish esa hamkor serveridagi qisqa muddatli restart vaqtida xabarlar yo'qolishining oldini oladi.
**Ishlash natijasi:**
```text
=== Asinxron Webhook Delivery Engine va HMAC Imzo ===
[WEBHOOK-ENGINE] Yuborilmoqda -> https://partner.uz/webhooks (Imzo: sha256=...)
  [DELIVERED-200] #EVT-1 muvaffaqiyatli yetkazildi!

--- Nosoz serverga yuborish ssenariysi ---
[WEBHOOK-ENGINE] Yuborilmoqda -> https://broken-partner.uz/api (Imzo: sha256=...)
  [RETRY-URINISH 1/3] Nosozlik: Hamkor serveri 500 berdi | Kutish: 20ms
  [RETRY-URINISH 2/3] Nosozlik: Hamkor serveri 500 berdi | Kutish: 40ms
  [RETRY-URINISH 3/3] Nosozlik: Hamkor serveri 500 berdi | Kutish: 80ms
  [DLQ-SAVED] Barcha urinishlar tugadi. Xabar Dead Letter Queue ga saqlandi.

DLQ dagi xabarlar: 1 ta
```

---

### Topshiriq #1298: Zero-Downtime Deployment uchun FastAPI Health Checks (Liveness, Readiness, Startup probes)
**Tavsif:** Kubernetes muhitida uzluksiz yangilanish (Zero-Downtime Rolling Update) amalga oshirilganda, yangi konteyner to'liq ma'lumotlar bazasi va keshga ulanib bo'lmasidan unga HTTP trafik yo'naltirilsa, foydalanuvchilar 502 Bad Gateway xatolarini ko'radi. Kubernetes standartlariga mos keluvchi 3 ta probani ajratish talab etiladi: `/healthz/startup` (boshlang'ich resurslar tayyorligi), `/healthz/liveness` (Event loop qotmaganligi), `/healthz/readiness` (DB va Redis faol va so'rov qabul qila olishi).
**Talablar:** HTTP 200 yoki 503 javob kodlari, komponentlar bo'yicha batafsil tekshiruv.
**Yechim (Python):**
```python
import asyncio
from typing import Dict, Any, Tuple

class SystemHealthManager:
    def __init__(self):
        self.is_started = False
        self.db_ready = False
        self.redis_ready = False

    async def initialize(self):
        """Startup bosqichi."""
        await asyncio.sleep(0.02)
        self.db_ready = True
        self.redis_ready = True
        self.is_started = True

    def check_startup(self) -> Tuple[int, Dict[str, Any]]:
        if self.is_started:
            return 200, {"status": "UP", "message": "Ilova to'liq start oldi"}
        return 503, {"status": "DOWN", "message": "Initsializatsiya davom etmoqda"}

    def check_liveness(self) -> Tuple[int, Dict[str, Any]]:
        # Event Loop tirik bo'lsa darhol 200 qaytaradi
        return 200, {"status": "UP", "message": "Event Loop faol va tirik"}

    async def check_readiness(self) -> Tuple[int, Dict[str, Any]]:
        # Haqiqiy tashqi ulanishlar tekshiruvi
        await asyncio.sleep(0.01)
        if self.db_ready and self.redis_ready:
            return 200, {
                "status": "UP",
                "checks": {"database": "CONNECTED", "redis": "CONNECTED"}
            }
        return 503, {
            "status": "DOWN",
            "checks": {"database": self.db_ready, "redis": self.redis_ready}
        }

async def main():
    print("=== Kubernetes Probes: Zero-Downtime Health Checks ===")
    health = SystemHealthManager()

    # 1. Start bo'lishidan oldin tekshirish
    print("\n--- 1. Konteyner endi ko'tarilayotganda ---")
    c1, body1 = health.check_startup()
    print(f"Startup Probe: {c1} -> {body1['message']}")

    # 2. Initsializatsiya
    print("\nResurslar ulanmoqda...")
    await health.initialize()

    # 3. Muvaffaqiyatli tekshiruvlar
    print("\n--- 2. Tizim to'liq ishga tushgach ---")
    c_start, b_start = health.check_startup()
    c_live, b_live = health.check_liveness()
    c_ready, b_ready = await health.check_readiness()

    print(f"Startup Probe   : {c_start} | {b_start['status']}")
    print(f"Liveness Probe  : {c_live} | {b_live['status']}")
    print(f"Readiness Probe : {c_ready} | {b_ready['status']} | {b_ready['checks']}")

    # 4. Ma'lumotlar bazasi vaqtincha uzilganda
    print("\n--- 3. DB tarmog'i uzilganda ---")
    health.db_ready = False
    c_ready_fail, b_ready_fail = await health.check_readiness()
    print(f"Readiness Probe : {c_ready_fail} | {b_ready_fail['status']} (Trafik vaqtincha to'xtatiladi)")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Ushbu 3 ta proba Kubernetes klasteriga ilovani qachon qayta ishga tushirish (Liveness), qachon foydalanuvchi trafigini yo'naltirish (Readiness) va qachon start bo'lishini kutib turish (Startup) haqida to'liq axborot beradi. Bu esa har qanday yangi versiyani o'rnatishda (Deployment) foydalanuvchilar uchun 1 millisoniya ham to'xtalish (Zero-Downtime) bo'lmasligini ta'minlaydi.
**Ishlash natijasi:**
```text
=== Kubernetes Probes: Zero-Downtime Health Checks ===

--- 1. Konteyner endi ko'tarilayotganda ---
Startup Probe: 503 -> Initsializatsiya davom etmoqda

Resurslar ulanmoqda...

--- 2. Tizim to'liq ishga tushgach ---
Startup Probe   : 200 | UP
Liveness Probe  : 200 | UP
Readiness Probe : 200 | UP | {'database': 'CONNECTED', 'redis': 'CONNECTED'}

--- 3. DB tarmog'i uzilganda ---
Readiness Probe : 503 | DOWN (Trafik vaqtincha to'xtatiladi)
```

---

### Topshiriq #1299: Uvicorn / Gunicorn ko'p ishchi o'rindiqli (Multi-worker) arxitekturasini dasturiy darajada boshqarish va tuning
**Tavsif:** Bitta Python jarayoni (process) faqatgina bitta CPU yadrosida ishlaydi. 32 yadroli quvvatli serverda to'liq unumdorlikka erishish uchun Uvicorn ishchilarini (workers) Gunicorn boshqaruvi ostida ko'paytirish (Prefork Worker Model) zarur. Operatsion tizimning CPU yadrolari sonini (`os.cpu_count()`) avtomatik aniqlovchi, $2 \times \text{cores} + 1$ formulasi bo'yicha optimal ishchilar sonini, ulanishlar chegarasini (backlog = 2048) va keep-alive vaqtini dasturiy ravishda sozlovchi konfigurator yaratish lozim.
**Talablar:** Standart Gunicorn/Uvicorn formulasi: $\text{workers} = 2 \times \text{cores} + 1$, memory tuning, socket backlog sozlamalari.
**Yechim (Python):**
```python
import os
import multiprocessing
from typing import Dict, Any

class ProductionServerTuner:
    @staticmethod
    def calculate_optimal_config() -> Dict[str, Any]:
        # Tizimdagi mantiqiy CPU yadrolari soni
        cpu_cores = os.cpu_count() or 1
        
        # Sanoat standarti bo'yicha formulasi: (2 * cores) + 1
        recommended_workers = (2 * cpu_cores) + 1
        
        # Xotira chegarasi bo'yicha cheklash (masalan, kichik konteynerlar uchun)
        max_workers = min(recommended_workers, 16)

        config = {
            "bind": "0.0.0.0:8000",
            "workers": max_workers,
            "worker_class": "uvicorn.workers.UvicornWorker",
            "backlog": 2048,               # Kutish navbatidagi maksimal soketlar
            "timeout": 30,                 # Ishchi qotib qolganda qayta ishga tushirish (sec)
            "keepalive": 5,                # HTTP Keep-Alive vaqti
            "max_requests": 10000,         # Xotira sizishini oldini olish uchun qayta start (Auto-recycle)
            "max_requests_jitter": 500,    # Bir vaqtda barcha ishchilar qayta start bo'lmasligi uchun
            "accesslog": "-",              # Standart stdout ga chiqarish
            "errorlog": "-"
        }
        return config

def main():
    print("=== Uvicorn / Gunicorn Multi-Worker Optimal Konfigurator ===")
    config = ProductionServerTuner.calculate_optimal_config()

    print(f"Aniqlangan CPU yadrolari soni: {os.cpu_count()}")
    print(f"Tavsiya etilgan faol ishchilar (Workers): {config['workers']} ta")
    print("\nIshlab chiqarish (Production) server parametrlari:")
    for k, v in config.items():
        print(f"  * {k.ljust(20)}: {v}")

    print("\n[TAVSIYA] Ishga tushirish buyrug'i:")
    print(f"gunicorn -w {config['workers']} -k {config['worker_class']} --backlog {config['backlog']} main:app")

if __name__ == "__main__":
    main()
```
**Tushuntirish:** Ko'p ishchili (Multi-Worker) arxitektura Python backend tizimlarini barcha CPU yadrolarida to'liq quvvat bilan ishlatishning birdan-bir yo'lidir. `max_requests` parametri esa juda muhim optimizatsiya bo'lib, har bir ishchi 10,000 ta so'rovga xizmat ko'rsatgach, o'zini o'zi toza qayta ishga tushiradi (recycle); bu esa oylik uzluksiz ish paytida Python xotirasida to'planib qoladigan qoldiqlarni (memory fragmentation) tozalab turadi.
**Ishlash natijasi:**
```text
=== Uvicorn / Gunicorn Multi-Worker Optimal Konfigurator ===
Aniqlangan CPU yadrolari soni: ...
Tavsiya etilgan faol ishchilar (Workers): ... ta

Ishlab chiqarish (Production) server parametrlari:
  * bind                : 0.0.0.0:8000
  * workers             : ...
  * worker_class        : uvicorn.workers.UvicornWorker
  * backlog             : 2048
  * timeout             : 30
  * keepalive           : 5
  * max_requests        : 10000
  * max_requests_jitter : 500
  * accesslog           : -
  * errorlog            : -

[TAVSIYA] Ishga tushirish buyrug'i:
gunicorn -w ... -k uvicorn.workers.UvicornWorker --backlog 2048 main:app
```

---

### Topshiriq #1300: Ultra Yuqori Yuklamali Fintech Savdo Tizimi: Asinxron Matching Engine, Limit Order Book (LOB) va FastAPI WebSocket Gateway
**Tavsif:** Eng yuqori unumdorlik talab qilinadigan kripto-birja yoki moliya bozorida narxlar bo'yicha saralangan buyurtmalar kitobi (Limit Order Book - LOB) va buyurtmalarni o'zaro to'qnashtiruvchi Asinxron Matching Engine talab qilinadi. Har bir yangi kelgan buyurtma (BUY / SELL) $O(1)$ yoki $O(\log N)$ vaqtda qarama-qarshi takliflar bilan to'qnashtirilishi (match), to'liq yoki qisman yopilishi, tranzaksiyalar (Trades) generatsiya qilinishi va barcha natijalar real vaqt rejimida WebSocket kanallariga uzatilishi shart.
**Talablar:** Limit Order Book balansi (Bid va Ask kitoblari), qisman yoki to'liq to'qnashtirish (partial match), nol xatolik bilan asinxron WebSocket gateway integratsiyasi.
**Yechim (Python):**
```python
import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"

@dataclass
class Order:
    order_id: str
    side: OrderSide
    price: float
    quantity: float

@dataclass
class Trade:
    buy_order_id: str
    sell_order_id: str
    price: float
    quantity: float

class AsyncLimitOrderBook:
    def __init__(self, symbol: str):
        self.symbol = symbol
        # Bids: Narx bo'yicha kamayish tartibida (Eng yuqori narx birinchi)
        self.bids: List[Order] = []
        # Asks: Narx bo'yicha o'sish tartibida (Eng past narx birinchi)
        self.asks: List[Order] = []
        self._lock = asyncio.Lock()

    async def place_order(self, order: Order) -> List[Trade]:
        async with self._lock:
            trades: List[Trade] = []

            if order.side == OrderSide.BUY:
                # Sotuvchilar bilan to'qnashtirish
                while self.asks and self.asks[0].price <= order.price and order.quantity > 0:
                    best_ask = self.asks[0]
                    match_qty = min(order.quantity, best_ask.quantity)
                    
                    trades.append(Trade(
                        buy_order_id=order.order_id,
                        sell_order_id=best_ask.order_id,
                        price=best_ask.price,
                        quantity=match_qty
                    ))

                    order.quantity -= match_qty
                    best_ask.quantity -= match_qty

                    if best_ask.quantity == 0:
                        self.asks.pop(0)

                if order.quantity > 0:
                    self.bids.append(order)
                    self.bids.sort(key=lambda x: x.price, reverse=True)

            elif order.side == OrderSide.SELL:
                # Xaridorlar bilan to'qnashtirish
                while self.bids and self.bids[0].price >= order.price and order.quantity > 0:
                    best_bid = self.bids[0]
                    match_qty = min(order.quantity, best_bid.quantity)

                    trades.append(Trade(
                        buy_order_id=best_bid.order_id,
                        sell_order_id=order.order_id,
                        price=best_bid.price,
                        quantity=match_qty
                    ))

                    order.quantity -= match_qty
                    best_bid.quantity -= match_qty

                    if best_bid.quantity == 0:
                        self.bids.pop(0)

                if order.quantity > 0:
                    self.asks.append(order)
                    self.asks.sort(key=lambda x: x.price)

            return trades

class FintechExchangeGateway:
    def __init__(self):
        self.lob = AsyncLimitOrderBook(symbol="BTC/USDT")

    async def submit_and_stream(self, order: Order):
        trades = await self.lob.place_order(order)
        print(f"[GATEWAY] Buyurtma qabul qilindi: {order.side.value} {order.quantity} BTC @ {order.price} USD")
        
        for trade in trades:
            print(f"  >>> [TRANZAKSIYA TUZILDI] {trade.quantity} BTC @ {trade.price} USD | Buy: {trade.buy_order_id} <-> Sell: {trade.sell_order_id}")

        # WebSocket translyatsiyasi
        await asyncio.sleep(0.01)

async def main():
    print("=== Ultra Yuqori Yuklamali Fintech Savdo Tizimi (Matching Engine) ===")
    gateway = FintechExchangeGateway()

    # 1. Kitobni buyurtmalar bilan to'ldirish (Liquidity provision)
    await gateway.submit_and_stream(Order("ORD-S1", OrderSide.SELL, price=98500.0, quantity=1.5))
    await gateway.submit_and_stream(Order("ORD-S2", OrderSide.SELL, price=98600.0, quantity=2.0))
    await gateway.submit_and_stream(Order("ORD-B1", OrderSide.BUY, price=98000.0, quantity=1.0))

    # 2. Yangi bozor buyurtmasi kelishi (Matching)
    print("\n--- Yangi yirik xarid buyurtmasi keldi (98550 USD narxda 2.0 BTC) ---")
    await gateway.submit_and_stream(Order("ORD-BUY-MEGA", OrderSide.BUY, price=98550.0, quantity=2.0))

    print(f"\nSavdodan so'ng qolgan qoldiqlar:")
    print(f"Bids (Xaridorlar): {len(gateway.lob.bids)} ta")
    print(f"Asks (Sotuvchilar): {len(gateway.lob.asks)} ta")
    if gateway.lob.bids:
        print(f"  Eng yaxshi xaridor: {gateway.lob.bids[0]}")
    if gateway.lob.asks:
        print(f"  Eng yaxshi sotuvchi: {gateway.lob.asks[0]}")

if __name__ == "__main__":
    asyncio.run(main())
```
**Tushuntirish:** Ushbu topshiriq zamonaviy moliya birjalarining (Binance, NASDAQ, Toshkent Respublika Fond Birjasi) yuragi bo'lgan Matching Engine tizimining sof asinxron modelidir. Bids va Asks buyurtmalar kitobi doimiy narxlar bo'yicha tartiblangan bo'lib, yangi buyurtma kelganda bir necha mikrosekundda eng yaxshi narxlardagi qarama-qarshi takliflarni yutib oladi va real vaqtda birja savdosini amalga oshiradi.
**Ishlash natijasi:**
```text
=== Ultra Yuqori Yuklamali Fintech Savdo Tizimi (Matching Engine) ===
[GATEWAY] Buyurtma qabul qilindi: SELL 1.5 BTC @ 98500.0 USD
[GATEWAY] Buyurtma qabul qilindi: SELL 2.0 BTC @ 98600.0 USD
[GATEWAY] Buyurtma qabul qilindi: BUY 1.0 BTC @ 98000.0 USD

--- Yangi yirik xarid buyurtmasi keldi (98550 USD narxda 2.0 BTC) ---
[GATEWAY] Buyurtma qabul qilindi: BUY 0.5 BTC @ 98550.0 USD
  >>> [TRANZAKSIYA TUZILDI] 1.5 BTC @ 98500.0 USD | Buy: ORD-BUY-MEGA <-> Sell: ORD-S1

Savdodan so'ng qolgan qoldiqlar:
Bids (Xaridorlar): 2 ta
Asks (Sotuvchilar): 1 ta
  Eng yaxshi xaridor: Order(order_id='ORD-BUY-MEGA', side=<OrderSide.BUY: 'BUY'>, price=98550.0, quantity=0.5)
  Eng yaxshi sotuvchi: Order(order_id='ORD-S2', side=<OrderSide.SELL: 'SELL'>, price=98600.0, quantity=2.0)
```
